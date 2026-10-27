import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal
from chemistry import Chemistry,environment,valid,PROFILES
from molecule import radial,surfaces


def radiative(L,emax):
    R,U,d,e=radial(dr=.04,L=L)
    ev,vec=eigh_tridiagonal(d,e,select='i',select_range=(0,0),check_finite=False)
    binding=-ev[0];bound=vec[:,0]
    R,U,d,e=radial(dr=.04,L=L,J=1,surface=1)
    ew,v=eigh_tridiagonal(d,e,select='v',select_range=(0,emax),check_finite=False)
    S=surfaces(R)[2];dip=R/(2*np.sqrt(1-S*S));strength=abs((bound*dip)@v)**2
    omega=ew+binding;rows=[]
    for T in [.002,.01,.03]:
        gamma=4/3*float(np.sum(omega**3*strength/np.expm1(np.minimum(omega/T,700))))
        saha=(100*101/201*T/(2*np.pi))**1.5*np.exp(-binding/T)
        rows.append(dict(T=T,photo_rate_over_alpha3=gamma,association_coefficient_over_alpha3=gamma/saha))
    return dict(L=L,dr=.04,energy_cutoff=emax,continuum_count=len(ew),rows=rows)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    root=Path(__file__).parent;specs=json.loads((root/'run_spectrum/results.json').read_text())['spectra']
    bounds=[]
    for s in specs:
        M=s['mass_ratio'];W=sum(l['weight'] for l in s['levels']);Amu=((M+1)**2/(2*M+1))**1.5
        assert max(l['binding'] for l in s['levels'])<.5
        bounds.append(dict(mass_ratio=M,dr=s['dr'],rovibrational_levels=len(s['levels']),rotational_weight=W,
                           uniform_molecular_mass_bound=(2*M+1)/(M+1)/(2+np.sqrt(Amu/W))))
    ch=Chemistry(specs[1]);rows=[]
    for alpha in [.15,.2]:
        for mass in np.geomspace(.01,1e9,21):
            fixed=[];closed=[]
            for Mb,b in PROFILES:
                density,Ti=environment(alpha,mass,Mb,b)
                for target,state in [(fixed,ch.state(density,Ti)),(closed,ch.endpoint(density,Ti))]:
                    state['applicability_screen_passed']=valid(state,alpha);target.append(state)
            rows.append(dict(alpha=alpha,light_mass_eV=float(mass),fixed_T=fixed,closed_energy=closed))
    summary={}
    for mode in ['fixed_T','closed_energy']:
        applicable=[r for r in rows if all(s['applicability_screen_passed'] for s in r[mode])]
        best=max(applicable,key=lambda r:r[mode][2]['charged_molecular_mass_fraction']) if applicable else None
        summary[mode]=dict(parameter_points=len(rows),applicable_count=len(applicable),
                           target_count=sum(r[mode][2]['charged_molecular_mass_fraction']>=.8 and max(r[mode][i]['charged_molecular_mass_fraction'] for i in [0,1,3])<=.2 for r in rows),
                           maximum_applicable_disk_fraction=None if best is None else best[mode][2]['charged_molecular_mass_fraction'],
                           best_applicable_parameters=None if best is None else [best['alpha'],best['light_mass_eV']],
                           best_applicable_fractions=None if best is None else [s['charged_molecular_mass_fraction'] for s in best[mode]])
    rates=[radiative(60,.25),radiative(120,.25),radiative(120,.5)]
    result=dict(uniform_bounds=bounds,summary=summary,rows=rows,radiative=rates)
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(bounds=bounds,summary=summary,rates=rates),indent=2))
if __name__=='__main__':main()
