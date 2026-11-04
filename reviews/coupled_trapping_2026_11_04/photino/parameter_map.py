"""Necessary-gate map at fixed resonance t=sqrt(60)/Z0.

Uses exact tree homogeneity and leading gaugino/current assumptions; passes
are not successful production or stationary gravity packets.
"""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import build_model,ext_basis,threshold,summarize,Z0
E0=.003;MU0=18170662.111498855;NGRAV=2.9999;HBAR=6.582119569e-25;AGE=4.3549488e17
DM=.44e-9;Y0=3.7454384329500086e-7;GS0=3.909;GS=106.75;T0=2.3486541805581e-13
OM=.315;OR=9.2e-5;OL=1-OM-OR;CH=299792.458/67.4


def point(e):
    x=math.sqrt(60/(31*e));g=math.sqrt(29/200)*e
    d=build_model(x,e,e,g,vertices=False);ext,C=ext_basis(d);groups,_=summarize(threshold(d,ext),C)
    return dict(e=e,x=x,mchi_over_mu=abs(groups['U1']['signed_mass']))


def mintravel(mass,ab=1e-18):
    Y=DM/mass;pF=(6*math.pi**2/2*Y*(2*math.pi**2/45*GS0*T0**3))**(1/3);alpha=pF/mass
    def meanv(a):
        b=a/alpha
        if b>30:return 3/(4*b)-1/(4*b**3)+9/(64*b**5)-3/(32*b**7)
        return (1-2*b*b)*math.sqrt(1+b*b)+2*b**3
    val=CH*quad(lambda z:math.exp(z)*meanv(math.exp(z))/math.sqrt(OR+OM*math.exp(z)+OL*math.exp(4*z)),math.log(ab),0,epsabs=1e-14,epsrel=1e-9,limit=200)[0]
    return val*1000


def main(out):
    start=time.monotonic();bound=json.loads((HERE.parent/'gravity_resonance/run_bound001/result.json').read_text());medium=json.loads((HERE.parent/'microphysics/run_medium001/result.json').read_text())
    ref=point(E0);mc0=ref['mchi_over_mu']*MU0
    tau0=HBAR*16*math.pi*MU0**4/(31*mc0**5)*(3/NGRAV)
    critical=brentq(lambda m:mintravel(m)-1,1e-5,1e-3,xtol=1e-16)
    ratio_medium=medium['sigma_pair_v_all_FFS_blocked_uniform_bound_mu_minus2']/bound['sigma_max_mu_minus2']
    refs={t:next(r for r in bound['cases'] if r['kind']=='protected' and r['Tc_start_over_mu']==t and r['initial_yield']>3e-7) for t in (.00466,.0005)}
    scenarios=[]
    # Exact finite-Y term retained. Write w=(mu/mu0)sqrt(e/e0); the pole
    # gate is w² <= gate0*(w/Y0+L0*K), independent of coupling thereafter.
    for width,K in [('vacuum_width',1.),('all_FFS_blocked_SSS_floor',ratio_medium)]:
        for t,old in refs.items():
            gate=old['charged_yield_gate'];L=old['pole_loss_integral_upper']*K
            wmax=(gate/Y0+math.sqrt((gate/Y0)**2+4*gate*L))/2
            for survival,taureq in [('survival99',AGE/(-math.log(.99))),('partial_lifetime_age',AGE)]:
                elo=E0*math.sqrt(critical/(mc0*wmax))
                ehi=E0*(tau0/taureq*mc0/critical)**.1
                examples=[]
                for e,mu in [(E0,2e6),(E0,3e6),(.0025,2.5e6),(.0035,1.5e6),(.004,1e6),(.004,2e6)]:
                    v=e/E0;u=mu/MU0;w=u*math.sqrt(v);mc=mc0*u*v**2.5;tau=tau0/(u*v**12.5)
                    lower=1/(1/Y0+L/w);gatenow=gate/w;ab=.02*T0*(GS0/GS)**(1/3)/(t*math.sqrt(v)*mu)
                    examples.append(dict(e=e,mu_GeV=mu,photino_keV=mc*1e6,charged_mass_GeV=old['m_charged_on_pole_GeV']*w,
                        pole_lower_over_charged_gate=lower/gatenow,partial_lifetime_lower_s=tau,partial_survival_lower=math.exp(-AGE/tau),
                        early_Pauli_minimum_travel_kpc=mintravel(mc,ab),
                        necessary_gates_pass=bool(lower<=gatenow and mc>=critical and tau>=taureq)))
                scan=[]
                for e in np.linspace(.0005,.008,151):
                    v=float(e/E0);lo=MU0*(critical/mc0)*v**-2.5
                    up_pole=MU0*wmax*v**-.5;up_life=MU0*(tau0/taureq)*v**-12.5
                    scan.append(dict(e=float(e),mu_cold_min_GeV=lo,mu_pole_max_GeV=up_pole,mu_partial_survival_max_GeV=up_life,
                        overlap=bool(lo<=min(up_pole,up_life))))
                scenarios.append(dict(width_model=width,sigma_ceiling_multiplier=K,Tc_start_over_mu_at_e0=t,survival_requirement=survival,
                    exact_pole_wmax=wmax,necessary_overlap_e_interval=[elo,ehi],boundary_lower=dict(e=elo,mu_GeV=MU0*(critical/mc0)*(elo/E0)**-2.5),
                    boundary_upper=dict(e=ehi,mu_GeV=MU0*(critical/mc0)*(ehi/E0)**-2.5),scan=scan,examples=examples))
    probes=[point(e) for e in (.0015,.006)]
    checks=dict(gaugino_homogeneity=max(abs(p['mchi_over_mu']/ref['mchi_over_mu']/(p['e']/E0)**2.5-1) for p in probes)<1e-8,
        cold_root=abs(mintravel(critical)-1)<1e-8,
        finite_Y_benchmark=max(abs((1/(1/Y0+r['pole_loss_integral_upper']))/r['charged_yield_gate']/r['lower_over_charged_gate']-1) for r in refs.values())<1e-8,
        all_three_gate_overlap=all(s['necessary_overlap_e_interval'][0]<s['necessary_overlap_e_interval'][1] for s in scenarios),
        cold99_candidate_exists=all(any(z['necessary_gates_pass'] for z in s['examples']) for s in scenarios if s['survival_requirement']=='survival99'))
    result=dict(claim_id='CT09_FIXED_RESONANCE_NECESSARY_PARAMETER_MAP',checks={k:bool(v) for k,v in checks.items()},
        fixed_t=math.sqrt(60)/Z0,reference=dict(e=E0,mu_GeV=MU0,x=ref['x'],photino_keV=mc0*1e6,partial_lifetime_lower_s=tau0,
            pole_mass_charged_GeV=refs[.00466]['m_charged_on_pole_GeV'],cold_1kpc_minimum_photino_keV=critical*1e6,medium_cross_section_multiplier=ratio_medium),
        scaling=dict(mchi='mu e^(5/2)',sigma_max='mu^(-2) e^(-1)',Tc_physical_start='mu sqrt(e)',pole_lower_over_gate_asymptotic='mu^2 e',partial_lifetime_lower='mu^(-1) e^(-25/2)',Pauli_momentum_over_mass='mchi^(-4/3)',travel='quadrature includes radiation-era logarithm; not exactly a power law'),
        probes=probes,scenarios=scenarios,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Necessary gates under fixed-resonance homogeneity, constant final mass early collisionless Pauli transport, fixed leading hidden current, and ideal maximum pole depletion. Passing a pole lower-bound gate does not prove actual depletion. No stationary retuned SUGRA packet, vacuum survival, phase-space source/abundance history, pole-occupation solution, or total photino lifetime is constructed.')
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=result['checks'],reference=result['reference'],scenarios=[{k:v for k,v in z.items() if k not in ('scan','examples')}|{'examples':z['examples']} for z in scenarios],runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes']),indent=2));assert all(checks.values()),checks


if __name__=='__main__':
    try:main(sys.argv[1])
    finally:print('observed_peak_RSS_bytes='+str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),flush=True)
