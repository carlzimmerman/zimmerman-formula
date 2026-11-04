"""Orthogonal checks of CT09 source and Pauli travel controls."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource,hashlib
from scipy.integrate import quad
HERE=Path(__file__).resolve().parent


def main(out):
    start=time.monotonic();s=json.loads((HERE/'run_source004/result.json').read_text());p=json.loads((HERE/'run_phase001/result.json').read_text())
    cos=p['cosmology'];om=cos['Omega_m'];orr=cos['Omega_r'];ol=cos['Omega_Lambda'];T=cos['Tgamma0_GeV'];gs0=cos['g_s0'];cH=299792.458/cos['H0_km_s_Mpc']
    rows=[]
    for v in s['vacua']:
        Y=v['target_photino_yield'];mc=v['photino_GeV'];pF=(6*math.pi**2/2*Y*(2*math.pi**2/45*gs0*T**3))**(1/3);alpha=pF/mc
        # Interchange integrations and integrate the exact filled-ball mean
        # velocity directly, independent of the per-momentum travel routine.
        def meanv(a):
            b=a/alpha
            if b>30:
                return 3/(4*b)-1/(4*b**3)+9/(64*b**5)-3/(32*b**7)
            return (1-2*b*b)*math.sqrt(1+b*b)+2*b**3
        ab=.02*T*(gs0/cos['g_s_birth'])**(1/3)/(.003*v['mu_GeV'])
        travel=cH*quad(lambda l:math.exp(l)*meanv(math.exp(l))/math.sqrt(orr+om*math.exp(l)+ol*math.exp(4*l)),math.log(ab),0,epsabs=1e-14,epsrel=1e-10,limit=200)[0]
        expected=next(r for r in p['cases'] if r['kind']==v['kind'])['target_Pauli_minimum_early_birth_travel_kpc']/1000
        rows.append(dict(kind=v['kind'],pF0_GeV=pF,travel_Mpc=travel,recorded_travel_Mpc=expected,relative_error=abs(travel/expected-1)))
    # Each width is averaged over 12 Takagi parent states. Independent
    # Casimir identity is algebraic: (3,2), qY²5/12, C2=3/4,C3=4/3.
    ratio=(5/12)/((5/12)+(3/4)+(4/3))
    normalization=abs(ratio-1/6)
    checks=dict(Pauli_minimum_integration_order=max(r['relative_error'] for r in rows)<1e-7,
        full_grid_gauge_branching=all(abs(r['massless_widths_over_mu']['U1']/sum(r['massless_widths_over_mu'].values())-ratio)<1e-9 for r in s['grid'] if r['massless_widths_over_mu']['U1']>0),
        representation_branching=normalization<1e-16,
        one_pass_vs_cycles=all(abs(v['one_pass_DM_fraction_using_gauge_branching_upper']*next(r for r in p['cases'] if r['kind']==v['kind'])['required_gauge_emissions_per_initial_carrier']-1)<1e-7 for v in s['vacua']))
    result=dict(claim_id='CT09_PHOTINO_ORTHOGONAL_CONTROLS',checks=checks,Pauli_floor_controls=rows,
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Independent present-density normalization and integration-order control of conditional constant-mass early-birth Pauli travel floor; exact representation branching algebra. No full plasma evolution or full SUGRA 1PI solution.')
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values()),checks


if __name__=='__main__':main(sys.argv[1])
