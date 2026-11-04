"""Companion-energy/late-travel inequalities and gravitational source controls."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,math,time,resource
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import kv,roots_laguerre,zeta
from boltzmann_v3 import MP,HB,TG0,TN0,RHOC,RHOCHI,RAD,MPC_GEV,H0,scale_row
from kernels import widths
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
LU,LW=roots_laguerre(64)
def energy_bound(row,r):
    q=dict(row);q['m_sigma_GeV']=2*q['photino_GeV']*r;q['widths']=widths(q,q['logmass_slopes'])
    m=q['m_sigma_GeV'];mc=q['photino_GeV'];G=q['widths']['sigma_total'];B=q['widths']['sigma']['U1']/G
    ar=1/1101;rhoNu=7*math.pi**2/120*TN0**4
    Kmax=1.1*RHOCHI*ar+.3*rhoNu
    C=math.sqrt(math.exp(float(RAD(0)))/(3*MP**2));Cmax=math.sqrt((math.exp(float(RAD(0)))+Kmax)/(3*MP**2))
    amed=math.sqrt(2*C*math.log(2)/G);amean=math.sqrt(math.pi*C/(2*G));n0=RHOCHI/(2*B*mc)
    Kmin=n0*m*amean
    beta=math.sqrt(max(0,1-1/r**2));qmed=mc*math.sqrt(r*r-1)*amed
    def hmax(a):return math.sqrt((math.exp(float(RAD(math.log(a))))+.05*RHOC/a**3+.685*RHOC+Kmax/ar/a**3)/(3*MP**2))
    remaining_at_rec=math.exp(-min(745,G*ar*ar/(2*Cmax)))
    coefficient=max(0,.5-remaining_at_rec)
    val,err=quad(lambda x:(qmed/math.exp(x))/math.sqrt(mc*mc+(qmed/math.exp(x))**2)/(math.exp(x)*hmax(math.exp(x))),math.log(ar),0,epsabs=0,epsrel=2e-8)
    FS=coefficient*val/MPC_GEV
    # Stronger full-quantile bound, not Jensen on mean momentum. For an
    # exponential decay u=Gamma*t has measure exp(-u)du. H>=H_SM moves every
    # birth quantile later in a. The allowed energy bound makes production
    # complete at recombination up to the explicitly bounded exponential tail.
    qq=mc*math.sqrt(r*r-1)*np.sqrt(2*C*LU/G)
    def full_integrand(x):
        a=math.exp(x);p=qq/a
        return float(np.dot(LW,p/np.sqrt(mc*mc+p*p)))/(a*hmax(a))
    full,fullerr=quad(full_integrand,math.log(ar),0,epsabs=0,epsrel=2e-8)
    fullFS=max(0,full/MPC_GEV-remaining_at_rec*1e5)
    F=q['mu_GeV']**2/math.sqrt(31);tau=HB*16*math.pi*F*F/mc**5
    return dict(e=q['e'],sigma_over_2mchi=r,mchi_GeV=mc,Gamma_sigma_GeV=G,Bchi=B,beta_chi=beta,mean_decay_a_RD=amean,minimum_hidden_K_over_allowed=Kmin/Kmax,necessary_energy_budget_pass=Kmin<=Kmax,post_recombination_FS_lower_bound_Mpc=FS,full_quantile_post_recombination_FS_lower_bound_Mpc=fullFS,late_unproduced_fraction_upper=remaining_at_rec,Ward_survival=math.exp(-4.3549488e17/tau),Ward_tau_s=tau)
def grav_source():
    # Tang/Wu1708.05138v2 eq3.7,3.15: massless photons to Majorana pair.
    # kappa=2/Mp; sigma=s/(640pi Mp^4). Identical incoming-pair1/2
    # cancels two produced Majoranas in the number source.
    kval=1/(640*math.pi)
    integral,err=quad(lambda z:z**6*kv(1,z),0,100,epsabs=1e-9,epsrel=2e-10)
    Cnum=kval*integral/(4*math.pi**4)
    Cexact=3/(20*math.pi**5)
    gs=106.75;A=2*math.pi**2/45*gs*math.sqrt(math.pi**2*gs/90)
    C_yield=Cnum/(3*A)
    # All massless SM initial species:4realHiggs,45Weyl,12gauge generators.
    # Derivation uses the TableI kernels and explicit identical-pair factors.
    Csm_MB=(4/80+45*3/80+12*3/20)/math.pi**5
    Csm_quantum=((4/80+12*3/20)*float(zeta(4))**2+(45*3/80)*(7/8*float(zeta(4)))**2)/math.pi**5
    Csm_yield=Csm_quantum/(3*A)
    # Intentionally generous all-initial-state envelope: 128^2 distinguishable
    # initial polarization pairs, each sigma<=s/(8pi Mp^4). This is looser
    # than every massless-SM amplitude in the authenticated TableI, counts
    # disallowed mixed pairs, and therefore is not an exact SM rate.
    C_upper=128**2*48/(8*math.pi*math.pi**4)
    yield_upper=C_upper/(3*A)
    s0=2*math.pi**2/45*(43/11)*TG0**3
    rows=[]
    for mc in [2.6153172511e-5,1e-4,1e-3]:
        Y=RHOCHI/(mc*s0)
        rows.append(dict(mchi_GeV=mc,Y_required=Y,photon_only_reheat_over_Mp=(Y/C_yield)**(1/3),all_SM_direct_reheat_over_Mp=(Y/Csm_yield)**(1/3),all_SM_direct_abundance_fraction_at_TR_001Mp=Csm_yield*1e-6/Y,all_SM_envelope_reheat_over_Mp_minimum=(Y/yield_upper)**(1/3),all_SM_envelope_abundance_fraction_at_TR_001Mp=yield_upper*1e-6/Y))
    return dict(source='https://arxiv.org/pdf/1708.05138v2',photon_source_C_T8_over_Mp4=Cnum,analytic_C=Cexact,relative_control=abs(Cnum/Cexact-1),Bessel_integral=integral,Bessel_exact=384.,photon_yield_C_TR3_over_Mp3=C_yield,all_SM_MB_source_C=Csm_MB,all_SM_BE_FD_source_C=Csm_quantum,all_SM_direct_yield_C=Csm_yield,all_SM_loose_yield_upper_coefficient=yield_upper,TR_over_Mp_cap=.01,examples=rows,interpretation='Concrete direct SM gravitational scattering fails abundance in this declared weak-gravity thermal-history control. The full hidden heavy-spectrum source and cascade is uncomputed; this direct-source failure is not a theorem about every gravitational history.')
def main(out):
    start=time.monotonic();p=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/canonical/run_nearfold/result.json').read_text())['threshold_points'][-1]
    base=json.loads((HERE/'run_kernels/result.json').read_text())['rows'][-1];base=dict(base)
    for k in ['t','mu_GeV','R_GeV','m_sigma_GeV','m_phase_GeV','m32_GeV','gauginos_GeV']:base[k]=p[k]
    base['photino_GeV']=p['gauginos_GeV']['U1'];base['logmass_slopes']=p['gaugino_log_slopes']['.0025']
    grid=[]
    for e in np.linspace(.002,.006,33):
        row=scale_row(base,float(e))
        for delta in np.geomspace(1e-12,30,180):grid.append(energy_bound(row,1+float(delta)))
    allowed=[r for r in grid if r['necessary_energy_budget_pass'] and r['Ward_survival']>=.99]
    minimum=min(allowed,key=lambda x:x['full_quantile_post_recombination_FS_lower_bound_Mpc'])
    # Continuous optimum at the most permissive survival boundary: minimize r
    # by saturating K while current scalings remain those of this branch.
    emax=brentq(lambda e:energy_bound(scale_row(base,e),1.1)['Ward_survival']-.99,.003,.006,xtol=1e-14)
    optimum_r=brentq(lambda r:energy_bound(scale_row(base,emax),r)['minimum_hidden_K_over_allowed']-1,1+1e-8,1.1,xtol=1e-13)
    boundary=energy_bound(scale_row(base,emax),optimum_r)
    grav=grav_source();checks=dict(gravitational_Bessel_normalization=grav['relative_control']<1e-10,nonempty_energy_lifetime_gate=bool(allowed),all_tested_allowed_thresholds_fail_1kpc=minimum['post_recombination_FS_lower_bound_Mpc']>.001)
    result=dict(claim_id='GC03_ENERGY_TRAVEL_GRAV_SOURCE_CONTROLS_V2',checks=checks,minimum_allowed=minimum,continuous_energy_lifetime_boundary_control=boundary,grid_count=len(grid),allowed_count=len(allowed),selected=[energy_bound(scale_row(base,e),r) for e in [.003,.004,.005] for r in [1.000001,1.0001,1.01,1.1,math.sqrt(2),2,5]],gravitational_source=grav,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Finite parameter scan plus analytic necessary energy/travel inequalities, conditional collisionless neutral photino. No actual nonabelian collision operator or full high-TR hidden cascade.')
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
