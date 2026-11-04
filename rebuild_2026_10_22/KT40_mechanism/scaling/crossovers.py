"""Independent exact chi=1 roots for the external-field point source."""
import argparse,json,math
from pathlib import Path
from scipy.optimize import brentq

HERE=Path(__file__).resolve().parent


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args()
    data=json.loads((HERE/'run_002/results.json').read_text());p=data['power'];ell=data['ell_kpc']
    out=dict(power=p,ell_kpc=ell,solar={},plummer_mass_thresholds=[],all_checks_pass=False)
    for foot,d in data['solar'].items():
        lam=d['lambda_'];eta=d['eta'];rm=d['rM_kpc']
        approx=d['external_field_chi1_radius_kpc']/rm
        rows=[]
        for mu in [-1.,0.,1.]:
            def logchi(logr):
                r=math.exp(logr);u=r**-2
                x=eta*eta+2*eta*u*mu+u*u
                return p*math.log(6*lam*lam/r**6)-math.log(x)
            logr=brentq(logchi,math.log(.9*approx),math.log(1.1*approx),xtol=1e-14)
            r=math.exp(logr);error=abs(r/approx-1)
            assert error<1e-4 and abs(logchi(logr))<1e-12
            rows.append(dict(mu=mu,radius_kpc=r*rm,relative_approximation_error=error,logchi_residual=logchi(logr)))
        # Isolated radial point mass has an exact algebraic crossing.
        rr=d['solar_only_chi1_radius_kpc']/rm
        chi=(6*lam*lam/rr**6)**p/(rr**-4)
        assert abs(chi-1)<1e-12
        out['solar'][foot]=dict(external_roots=rows,isolated_exact_chi=chi)
    for d in data['dwarfs']:
        if d['upsilon']!=3:continue
        c=d['local'][1]['chi']
        # At fixed Plummer a and ell, chi(a) scales as M^(2p-2).
        critical=d['mass_Msun']*c**(-1/(2*p-2))
        out['plummer_mass_thresholds'].append(dict(name=d['name'],footing=d['footing'],
            a_kpc=d['a_kpc'],mass_at_U3=d['mass_Msun'],chi_at_a=c,
            toy_fixed_size_mass_for_chi1_Msun=critical,
            qualification='Mathematical rescaling at fixed size, not a physical refit or an observational claim.'))
    out['all_checks_pass']=True
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(solar=out['solar'],all_checks_pass=True),indent=2))


if __name__=='__main__':main()
