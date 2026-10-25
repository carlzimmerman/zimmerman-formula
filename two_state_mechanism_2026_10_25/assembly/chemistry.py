import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.special import logsumexp

G=6.67430e-11;MSUN=1.98847e30;KPC=3.085677581491367e19
C=299792458.;HBAR=1.054571817e-34;EVMASS=1.7826619216279e-36
PROFILES=[(3e5,.3),(1e8,1.),(6e10,3.),(1e14,300.)]
ETA=5.364;M=100.

class Chemistry:
    def __init__(self,spectrum):
        self.B=np.array([v['binding'] for v in spectrum['levels']])
        self.logw=np.log([v['weight'] for v in spectrum['levels']])
        self.muA=M/(M+1);self.muT=M*(M+1)/(2*M+1)
    def state(self,density,T):
        logterms=self.logw+self.B/T;logZ=logsumexp(logterms)
        meanB=float(np.sum(self.B*np.exp(logterms-logZ)))
        la=1.5*np.log(self.muA*T/(2*np.pi))-.5/T-np.log(density)
        lt=1.5*np.log(self.muT*T/(2*np.pi))-logZ-np.log(density)
        def components(lx):
            x=np.exp(lx);rem=np.log(-np.expm1(lx));den=np.logaddexp(np.log(2)+lx,lt)
            logt=lx+rem-den;loga=lt+rem-den
            return loga,logt,np.logaddexp(lx,logt)
        def equation(lx):
            a,t,c=components(lx);return lx+c-la-a
        lo=min(la,lt,-20.)-20.;hi=-1e-15
        if equation(hi)<0: lx=hi
        else: lx=brentq(equation,lo,hi,xtol=1e-12)
        loga,logt,logc=components(lx)
        x,a,t,c=np.exp([lx,loga,logt,logc])
        energy=1.5*T*(1+x)-.5*a-(.5+meanB)*t
        # Ideal-gas checks for the four species with their actual densities/masses.
        deg=max(f*density*(2*np.pi/(mass*T))**1.5 for f,mass in zip([x,c,a,t],[M,1,M+1,2*M+1]))
        plasma=(4*np.pi*(x+c+t)*density/3)**(1/3)/T
        dilution=max(density,t*density*2.493**3)
        upper=1/(2+np.exp(np.clip((lt-la)/2,-700,700)))
        return dict(T=float(T),x=float(x),c=float(c),a=float(a),t=float(t),
                    charged_molecular_mass_fraction=float((2*M+1)/(M+1)*t),
                    energy=float(energy),mean_molecular_binding=meanB,
                    charge_error=float(x+t-c),heavy_count_error=float(x+a+2*t-1),
                    saha_log_error=float(equation(lx)) if lx<hi else None,
                    degeneracy=float(deg),plasma_coupling=float(plasma),dilution=float(dilution),
                    molecule_count_upper_bound=float(upper))
    def endpoint(self,density,Ti):
        target=3*Ti
        T=brentq(lambda T:self.state(density,T)['energy']-target,max(1e-12,Ti*.1),2*Ti+1,xtol=1e-12)
        result=self.state(density,T);result['initial_T']=float(Ti)
        result['energy_residual']=float(result['energy']-target)
        return result

def environment(alpha,mass,Mb,b):
    n=3*ETA*Mb*MSUN/(4*np.pi*(b*KPC)**3*(M+1)*mass*EVMASS)
    aD=HBAR/(mass*EVMASS*C*alpha)
    sigma2=G*(1+ETA)*Mb*MSUN/(6*b*KPC)
    Ti=(M+1)*sigma2/(2*C*C*alpha*alpha)
    return n*aD**3,Ti

def valid(s,alpha):
    return bool(s['degeneracy']<.1 and s['plasma_coupling']<.1 and s['dilution']<.01 and s['T']<=.05 and s['T']*alpha*alpha<.01)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    root=Path(__file__).parent
    spec=json.loads((root/'run_spectrum/results.json').read_text())['spectra'][1]
    ch=Chemistry(spec);rows=[]
    for alpha in np.geomspace(1e-5,.1,25):
        for mass in np.geomspace(.01,1e9,21):
            fixed=[];closed=[];dens=[]
            for Mb,b in PROFILES:
                density,Ti=environment(alpha,mass,Mb,b);dens.append(float(density))
                s=ch.state(density,Ti);s['applicability_screen_passed']=valid(s,alpha);fixed.append(s)
                s=ch.endpoint(density,Ti);s['applicability_screen_passed']=valid(s,alpha);closed.append(s)
            row=dict(alpha=float(alpha),light_mass_eV=float(mass),density_atomic_units=dens,fixed_T=fixed,closed_energy=closed)
            for mode in ['fixed_T','closed_energy']:
                f=[s['charged_molecular_mass_fraction'] for s in row[mode]]
                row[mode+'_target_met']=bool(f[2]>=.8 and max(f[0],f[1],f[3])<=.2)
            rows.append(row)
    summary={}
    for mode in ['fixed_T','closed_energy']:
        eligible=[r for r in rows if all(s['applicability_screen_passed'] for s in r[mode])]
        best=max(rows,key=lambda r:r[mode][2]['charged_molecular_mass_fraction'])
        summary[mode]=dict(common_parameter_points=len(rows),profile_evaluations=4*len(rows),
                           target_count=sum(r[mode+'_target_met'] for r in rows),
                           all_profiles_applicable_count=len(eligible),
                           applicable_target_count=sum(r[mode+'_target_met'] for r in eligible),
                           maximum_disk_proxy_fraction=best[mode][2]['charged_molecular_mass_fraction'],
                           maximizing_alpha=best['alpha'],maximizing_mass_eV=best['light_mass_eV'],
                           fractions_at_maximum=[s['charged_molecular_mass_fraction'] for s in best[mode]],
                           maximum_disk_proxy_fraction_applicable=max((r[mode][2]['charged_molecular_mass_fraction'] for r in eligible),default=None))
    allstates=[s for r in rows for mode in ['fixed_T','closed_energy'] for s in r[mode]]
    summary['max_charge_error']=max(abs(s['charge_error']) for s in allstates)
    summary['max_heavy_count_error']=max(abs(s['heavy_count_error']) for s in allstates)
    summary['max_energy_residual']=max(abs(s['energy_residual']) for r in rows for s in r['closed_energy'])
    summary['max_scaled_energy_residual']=max(abs(s['energy_residual'])/max(3*s['initial_T'],.5) for r in rows for s in r['closed_energy'])
    summary['bound_violation']=max(s['t']-s['molecule_count_upper_bound'] for s in allstates)
    assert len(rows)==525
    assert summary['max_charge_error']<1e-10
    assert summary['max_heavy_count_error']<1e-9
    assert summary['max_scaled_energy_residual']<1e-8
    assert summary['bound_violation']<1e-9
    Path(a.output).write_text(json.dumps(dict(summary=summary,rows=rows),indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
