"""Conditional late charged-pair loss envelope and required enhancement."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
ROOT=Path(__file__).resolve().parents[3]
E=.003;G=math.sqrt(29/200)*E;GST=106.75;GS0=3.909
MP=2.435e18;XI=.02;T0=2.3486541805581e-13;DM=.44e-9

def cfd(n):
    z,w=leggauss(n);p=25*(z+1);ww=25*w
    f=1/(np.exp(p)+1);N=float(ww@(p*p*f))
    # Independent double quadrature, angular average is 1/max(p,q).
    val=float((ww*p*p*f)@(1/np.maximum(p[:,None],p[None,:]))@(ww*p*p*f))/N**2
    return val,N

def main(output):
    start=time.monotonic()
    rows=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/run_charged/result.json').read_text())['cases']
    rows=[r for r in rows if r['name'] in ('canonical','protected')]
    N=1.5*1.202056903159594
    integ=lambda p:quad(lambda q:q*q/(math.exp(q)+1),0,p,epsabs=1e-12)[0]
    C=2*quad(lambda p:p/(math.exp(p)+1)*integ(p),0,55,epsabs=1e-11)[0]/N**2
    # Double Gauss has a diagonal derivative kink; comparison tolerance tracks it.
    repeats=[dict(n=n,C=cfd(n)[0],N=cfd(n)[1]) for n in (128,256,512)]
    checks=dict(FD_number_normalization=abs(repeats[-1]['N']/N-1)<1e-12,
                independent_CFD_quadratures=abs(repeats[-1]['C']/C-1)<2e-4,
                Coulomb_envelope=all(z/(-math.expm1(-z))<=1+z+1e-12
                                    for z in np.geomspace(1e-8,1e4,200)))
    cases=[]
    for r in rows:
        mu=r['mu_GeV'];m=r['min_charged_scalar_GeV'];gate=.1*DM/m
        for t in (.003,.001,.0005,.0001):
            Tc=t*mu;Tsm=Tc/XI
            H=math.sqrt(math.pi**2*GST/90)*Tsm*Tsm/MP
            entropy=2*math.pi**2/45*GST*Tsm**3
            afinal=Tsm/T0*(GST/GS0)**(1/3)
            alpha=2.5*G*G/(4*math.pi)
            sigma0=13*G**4/(128*math.pi*m*m)
            B=2*math.pi*alpha*(m/Tc)*C
            L=entropy*sigma0/(2*H)*(1-1/afinal+B*math.log(afinal))
            Lunit=entropy/(2*H)*4*math.pi/(m*Tc)*C*math.log(afinal)
            # Integrate the same scale-factor comparison directly after u=log a.
            direct=entropy*sigma0/(2*H)*quad(lambda u:math.exp(-u)+B,0,math.log(afinal),epsabs=1e-9)[0]
            checks['analytic_scale_integral']=bool(abs(direct/L-1)<1e-11)
            for initial in (3.74544e-7,1e-9,1e-11,1e-13):
                if initial<=gate:continue
                final=1/(1/initial+L)
                required=(1/gate-1/initial)/L
                cases.append(dict(kind=r['name'],mu_GeV=mu,m_GeV=m,
                    Tc_start_over_mu=t,T_SM_start_GeV=Tsm,m_over_Tc=m/Tc,
                    initial_yield=initial,charged_yield_gate=gate,
                    alpha_gauge_max=alpha,FD_inverse_relative_speed_constant=C,
                    sigma0_GeVm2=sigma0,Coulomb_B=B,scale_factor_to_present=afinal,
                    radiation_only_loss_integral_upper=L,
                    remaining_yield_lower_in_prescribed_gauge_closure=final,
                    fractional_loss_upper=1-final/initial,
                    required_gauge_envelope_multiplier=required,
                    single_swave_unitarity_loss_integral_upper=Lunit,
                    single_swave_remaining_yield_lower=1/(1/initial+Lunit)))
    checks['nonrelativistic_domain']=all(r['m_over_Tc']>3 for r in cases)
    checks['annihilation_reduces_number']=all(0<r['remaining_yield_lower_in_prescribed_gauge_closure']<=r['initial_yield'] for r in cases)
    checks={k:bool(v) for k,v in checks.items()}
    result=dict(claim_id='CT09_CONDITIONAL_LATE_GAUGE_DEPLETION',checks=checks,
                CFD=C,quadrature_controls=repeats,cases=cases,
                scope='Prescribed redshifting FD shape, symmetric charged scalar population, pure gauge NR annihilation plus Coulomb envelope, generous radiation-only expansion. No all-channel, scalar exchange, bound-state, kinetic redistribution or capture theorem.',
                runtime_seconds=time.monotonic()-start,
                peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=checks,CFD=C,cases=len(cases),runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'])))
    assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
