"""Leading inclusive eaten+uneaten photino-current bound for new candidate.

No transverse neutral 1PI pole or current matching. Unknown pole masses are
maximized by their massless phase space, keeping the specified current norm.
"""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
import mpmath as mp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import build_model,ext_basis,threshold,summarize
HBAR=6.582119569e-25;AGE=4.3549488e17;MP=2.435e18


def main(out):
    start=time.monotonic();mp.mp.dps=90
    old=json.loads((HERE.parent/'gravity_resonance/run_candidate001/result.json').read_text());r=old['rows'][-1];co={k:mp.mpf(v) for k,v in r['constants'].items()};z=list(map(mp.mpf,r['normalized']['z']));w=mp.mpf(r['normalized']['w']);Y=mp.mpf(r['Y'])
    W=co['F']*z[0]+co['AA']*z[1]-co['KK']*z[1]*z[2]**2/2+co['WBASE']*w
    m32=float(Y**(-co['NEXP']/2)*W/co['M']**2*co['MU']);mu=float(co['MU']);e=float(co['E']);eps=float(co['EPS']);n=float(co['NEXP']);x=float(r['actual_x'])
    d=build_model(x,e,e,float(co['G']),vertices=False);ext,C=ext_basis(d);groups,_=summarize(threshold(d,ext),C);mc=abs(groups['U1']['signed_mass'])*mu
    Fhidden=mu*mu/math.sqrt(31);Gamma0=mc**5/(16*math.pi*Fhidden**2)
    ce=Fhidden**2/(3*MP**2*m32*m32);cu=n/3;rr=(m32/mc)**2
    P=(1-rr)**3*(1+3*rr) if rr<1 else 0.
    width_eaten=mc**5/(48*math.pi*MP**2*m32*m32)*P if rr<1 else 0.
    norm=ce+cu;norm_with_actual_gravitino=ce*P+cu
    tau_fixed_norm=HBAR/Gamma0
    tau_with_exact_gravitino_and_massless_uneaten=HBAR/(Gamma0*norm_with_actual_gravitino)
    max99=(HBAR*16*math.pi*Fhidden**2*(-math.log(.99))/AGE)**.2
    enhancement99=math.sqrt(tau_fixed_norm*(-math.log(.99))/AGE)
    rs=np.linspace(0,1,10001);poly=(1-rs)**3*(1+3*rs)
    checks=dict(positive_current_weights=0<ce<1 and 0<cu<1,
        geometric_completeness=abs(eps/3+cu-1)<1e-14,
        exact_eaten_vs_geometric=abs(ce/(eps/3)-1)<1e-6,
        gravitino_factor_bounded=min(poly)>=0 and max(poly)<=1,
        gravitino_factor_monotone=max(np.diff(poly))<=0,
        exact_supergravity_normalization=abs(width_eaten/(Gamma0*ce*P)-1)<1e-12,
        candidate_current_survival99=math.exp(-AGE/tau_fixed_norm)>.99,
        current_mass_gate=mc<max99)
    result=dict(claim_id='CT09_LEADING_INCLUSIVE_PHOTINO_CURRENT_BOUND',checks={k:bool(v) for k,v in checks.items()},
        candidate=dict(e=e,mu_GeV=mu,x=x,epsilon=eps,n=n,mchi_keV=mc*1e6,m32_keV=m32*1e6,
            Fhidden_GeV2=Fhidden,geometric_eaten_weight=eps/3,geometric_uneaten_weight=cu,eaten_weight_from_actual_m32=ce,
            gravitino_mass_squared_ratio=rr,gravitino_kinematic_factor=P,actual_gravitino_width_GeV=width_eaten,
            massless_full_hidden_current_width_GeV=Gamma0,uneaten_plus_exact_eaten_massless_norm=norm,
            leading_width_upper_with_exact_eaten_factor_GeV=Gamma0*norm_with_actual_gravitino,
            fixed_unit_current_inclusive_lifetime_lower_s=tau_fixed_norm,
            fixed_unit_current_inclusive_survival_lower=math.exp(-AGE/tau_fixed_norm),
            lifetime_lower_with_exact_gravitino_and_massless_uneaten_s=tau_with_exact_gravitino_and_massless_uneaten,
            maximum_photino_keV_for99_at_fixed_mu_full_unit_current=max99*1e6,
            maximum_common_current_amplitude_multiplier_for99_at_candidate=enhancement99),
        analytic_obligations=dict(gravitino_factor='P(r)=(1-r)^3(1+3r), dP/dr=-12r(1-r)^2 <=0 on[0,1]',
            uneaten_factor='(1-rj)^3<=1 for any open spin1/2 daughter; zero when closed',
            norm='sum_j |c_j|²=1 for complete orthonormal redistribution of a fixed unit hidden current, including its eaten direction',
            bound='Gamma_eaten+sum_Gamma_uneaten <= mchi^5/(16piFhidden²) at that fixed leading operator norm'),
        primary_source=dict(url='https://arxiv.org/pdf/hep-ph/0312262v4',equation='4',accessed='2026-11-04',scope='Physical gravitino plus photon width; pure photino C_chigamma=1'),
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Inclusive bound only for the specified leading photon+neutral-fermion/gravitino current. No full physical total lifetime: transverse1PI residues/current matching, other operators and other channels remain unbounded. No TT-only uneaten mass inserted. Common amplitude tolerance is conditional on changing only this operator norm.')
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values()),checks


if __name__=='__main__':
    try:main(sys.argv[1])
    finally:print('observed_peak_RSS_bytes='+str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),flush=True)
