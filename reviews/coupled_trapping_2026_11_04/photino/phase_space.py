"""CT09 boosted FD source shape, Pauli capacity, and cycle energy controls.

Consumes completed source004 only. No kinetic history is inferred. Source
occupation is deliberately unblocked and its consistency is tested by f<=1.
"""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from scipy.special import spence
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'run_source004/result.json'
GS=106.75;GS0=3.909;GCHI=2;GF=24;XI=.02;T0=2.3486541805581e-13
H0_KMS_MPC=67.4;C_KMS=299792.458;OM=.315;OR=9.2e-5;OL=1-OM-OR
INUM=1.8030853547393915


def tail(z):
    """Integral_z^infinity r/(exp(r)+1) dr, stable at very large z."""
    if z>740:return 0.
    if z>20:
        return sum((-1)**(n+1)*math.exp(-n*z)*(z/n+1/n**2) for n in range(1,5))
    t=math.exp(-z)
    return z*math.log1p(t)-float(spence(1+t))


def occupation(u,m,k,B):
    # Each unpolarized parent has uniform massless daughter energy between
    # k(gamma-beta*gamma) and k(gamma+beta*gamma). f_parent=FD(P/Tc).
    if u<=0:return 0.
    zmin=m*abs(u*u-k*k)/(2*k*u)
    return GF*B/GCHI*m/(2*k*u*u)*tail(zmin)


def free_stream(alpha,ab,post_rec=False):
    """Comoving Mpc for p0/m=alpha, exact v and stated LCDM diagnostic H."""
    if alpha<=0:return 0.
    if post_rec:ab=max(ab,1/1090)
    def integrand(lna):
        a=math.exp(lna)
        v=alpha/math.sqrt(alpha*alpha+a*a)
        return a*v/math.sqrt(OR+OM*a+OL*a**4)
    return C_KMS/H0_KMS_MPC*quad(integrand,math.log(ab),0,epsabs=1e-14,epsrel=2e-9,limit=150)[0]


def analyze(c,vac):
    r=c['source'];t=c['t'];M=r['light_fermion_over_mu'];k0=r['mean_photino_pstar_over_mu']
    if k0 is None:return None
    m=M/t;k=k0/t;B=r['photino_branching_upper_given_gauge_channels'];mc=vac['photino_GeV'];mu=vac['mu_GeV']
    umax=k*(math.sqrt(1+(70/m)**2)+70/m)
    umin=k*(math.sqrt(1+(70/m)**2)-70/m)
    f=lambda u:occupation(u,m,k,B)
    def integ(power,clip=False):
        return quad(lambda u:u**power*(min(1.,f(u)) if clip else f(u)),umin,umax,points=[k],epsabs=1e-10,epsrel=2e-8,limit=400)[0]
    norm=integ(2);expect=GF*B/GCHI*INUM
    mean=integ(3)/norm
    peak=minimize_scalar(lambda z:-f(math.exp(z)),bounds=(math.log(umin),math.log(umax)),method='bounded',options={'xatol':1e-13})
    peakf=f(math.exp(peak.x))
    p0_over_u=XI*T0*(GS0/GS)**(1/3)
    ab=XI*T0*(GS0/GS)**(1/3)/(t*mu)
    travel=quad(lambda u:u*u*f(u)*free_stream(u*p0_over_u/mc,ab),umin,umax,points=[k],epsabs=1e-11,epsrel=1e-7,limit=200)[0]/norm
    post=quad(lambda u:u*u*f(u)*free_stream(u*p0_over_u/mc,ab,True),umin,umax,points=[k],epsabs=1e-11,epsrel=1e-7,limit=200)[0]/norm
    cycles=vac['target_photino_yield']/(vac['initial_charged_yield']*B)
    mean_energy_over_mu=mean*t
    # Gauge daughters are degenerate in the leading phase space, so one chi
    # requires 1/B total gaugino emissions and at least their emitted energy.
    energy_per_initial=cycles*mean_energy_over_mu
    # Pauli minimum is a filled ball. qF is in p/T_SM at the birth epoch.
    qF=(6*math.pi**2/GCHI*(2*math.pi**2/45*GS)*vac['target_photino_yield'])**(1/3)
    alphaF=qF*T0*(GS0/GS)**(1/3)/mc
    mintravel=3*quad(lambda z:z*z*free_stream(z*alphaF,ab),0,1,epsabs=1e-11,epsrel=1e-8)[0]
    minpost=3*quad(lambda z:z*z*free_stream(z*alphaF,ab,True),0,1,epsabs=1e-11,epsrel=1e-8)[0]
    fscaled=peakf*vac['target_photino_yield']/(vac['initial_charged_yield']*B)
    clipped=integ(2,True)/norm
    # Uniform source exposure with fixed parent shape gives f=1-exp(-A),
    # rather than min(1,A). This is a source-only Pauli diagnostic, not a
    # self-consistent solution for disappearing/repopulated parent particles.
    blocked_norm=quad(lambda u:u*u*(-math.expm1(-f(u))),umin,umax,points=[k],epsabs=1e-10,epsrel=1e-7,limit=400)[0]
    # Fixed field energy and number identities for the complete prompt source.
    mean_gamma=c['momentum']['mean_parent_gamma']
    expected_mean=k*mean_gamma
    return dict(kind=c['kind'],t=t,x=c['x'],M_over_Tc=m,pstar_over_Tc=k,
        Bchi_upper=B,one_pass_fmax_unblocked=peakf,fmax_if_scaled_to_all_DM=fscaled,
        peak_p_over_TSM=math.exp(peak.x)*XI,
        one_pass_yield=vac['initial_charged_yield']*B,
        clipped_naive_shape_yield_fraction=clipped,
        fixed_exposure_source_only_Pauli_yield_fraction=blocked_norm/norm,
        mean_p_over_TSM=mean*XI,mean_v0=mean*p0_over_u/mc,
        naive_unblocked_mean_travel_kpc=travel*1000,naive_unblocked_postrec_travel_kpc=post*1000,
        target_filled_sphere_pF_over_TSM=qF,target_minimum_mean_p_over_TSM=.75*qF,
        target_Pauli_minimum_early_birth_travel_kpc=mintravel*1000,target_Pauli_minimum_postrec_travel_kpc=minpost*1000,
        required_gauge_emissions_per_initial_carrier=cycles,required_full_two_conversion_cycles_per_initial_carrier=cycles/2,
        mean_gaugino_energy_over_mu=mean_energy_over_mu,
        required_emitted_energy_over_mu_per_initial_carrier=energy_per_initial,
        emitted_energy_over_present_parent_rest=energy_per_initial/M,
        emitted_energy_per_entropy_GeV=vac['target_photino_yield']/B*mean_energy_over_mu*mu,
        checks=dict(number_relative_error=abs(norm/expect-1),mean_boost_relative_error=abs(mean/expected_mean-1),
            Pauli_minimum_dominates_naive_source_mean=mintravel>travel),
        scope='Early fixed-background one-pass source, unblocked shape only; Pauli minimum holds for isotropic spin-balanced collisionless chi with same final mass/Y and production no later than stated early epoch. No bound on arbitrary late production or subsequent cooling/interactions. Repeated-emission energy uses only leading gauge channel energy, no universal history bound.')


def main(out):
    start=time.monotonic();d=json.loads(SOURCE.read_text());v={r['kind']:r for r in d['vacua']}
    rows=[analyze(c,v[c['kind']]) for c in d['conditional_stationary_examples']];rows=[r for r in rows if r is not None]
    tail_error=max(abs(tail(z)-quad(lambda p:p*math.exp(-p)/(1+math.exp(-p)),z,max(100,z+70),epsabs=1e-18)[0])/max(tail(z),1e-300) for z in (0,1,8,20,35))
    checks=dict(tail_identity=tail_error<1e-8,source_number=max(r['checks']['number_relative_error'] for r in rows)<1e-7,
        source_boost_moment=max(r['checks']['mean_boost_relative_error'] for r in rows)<1e-7,
        raw_source_Pauli_inconsistent=all(r['one_pass_fmax_unblocked']>1 for r in rows),
        diagnostic_early_minimum=all(r['checks']['Pauli_minimum_dominates_naive_source_mean'] for r in rows))
    result=dict(claim_id='CT09_PHOTINO_PHASESPACE_AND_CYCLE_CONTROL',checks=checks,tail_identity_relative_error=tail_error,cases=rows,
        cosmology=dict(H0_km_s_Mpc=H0_KMS_MPC,Omega_m=OM,Omega_r=OR,Omega_Lambda=OL,Tgamma0_GeV=T0,g_s_birth=GS,g_s0=GS0),
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Conditional source distribution and exact Pauli/rearrangement necessary control with stated cosmology and early collisionless propagation. No all-history no-go, no kinetic abundance or branching closure.')
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values()),checks


if __name__=='__main__':main(sys.argv[1])
