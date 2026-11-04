import sys,json,math,time,resource,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy.special import roots_laguerre
from scipy.integrate import quad
from boltzmann_v3 import run_case,scale_row,MP,RHOCHI,RHOC,TG0,HB
import controls_v3 as ctrl
HERE=Path(__file__).resolve().parent
def main(out):
    start=time.monotonic();phys=json.loads((HERE/'run_physical/result.json').read_text());protected=phys['cases'][-1]['source_row'];canonical=phys['cases'][0]['source_row'];sens=[]
    for source in [canonical,protected]:
        for factor in [0.,1000.]:
            r=json.loads(json.dumps(source));w=r['widths']
            for k in ['sigma','phase']:w[k]['GG']*=factor
            w['sigma_total']=sum(w['sigma'].values());w['phase_total']=sum(w['phase'].values())
            val=run_case(r,nq=720,dx=.02,angular=20)
            sens.append(dict(source=r['source_label'],scalar_Goldstino_width_factor=factor,FS_Mpc=val['free_streaming_Mpc'],initial_mother_Y=val['initial_mother_Y'],DeltaNeff=val['snapshots']['recombination_benchmark']['DeltaNeff_pressure_equivalent'],neutral_contact_tau=val['neutral_heavy_contact_optical_depth_majorant']))
    # Independent Cartesian/cascade energy and threshold controls.
    angular=[]
    z,w=np.polynomial.legendre.leggauss(24);w=w/2
    for ratio in [1.,2.,10.,100.]:
        E=ratio;M=1.;p=math.sqrt(E*E-M*M)
        for daughter in [.0,.01,.3,.499]:
            b=math.sqrt(1-4*daughter*daughter);ener=E/2+p/2*b*z
            angular.append(dict(parent_gamma=ratio,daughter_over_parent=daughter,number_normalization=2*sum(w),energy_ratio=2*np.dot(w,ener)/E,minimum_energy=float(ener.min()),energy_onshell=bool(np.all(ener>=daughter))))
    bdy=json.loads((HERE/'run_controls_v3/result.json').read_text())['continuous_energy_lifetime_boundary_control']
    base=dict(canonical);s=bdy['e']/base['e'];base=scale_row(base,bdy['e']);base['m_sigma_GeV']=2*base['photino_GeV']*bdy['sigma_over_2mchi']
    from kernels import widths
    base['widths']=widths(base,base['logmass_slopes']);m=base['m_sigma_GeV'];mc=base['photino_GeV'];G=base['widths']['sigma_total'];R=base['R_GeV']
    Nbudget=ctrl.KMAX/(m*math.sqrt(math.pi*ctrl.CMIN/(2*G)))
    occ={}
    ai=ctrl.AI
    for k,di in [('SU3',8),('SU2',3),('U1',1)]:
        mass=base['gauginos_GeV'][k];p=math.sqrt(m*m/4-mass*mass);Gamma=base['widths']['sigma'][k]
        A=2*math.pi**2*Nbudget*Gamma/(di*ctrl.CMIN*p**3)
        a01=A/.01;early=min(1,G*max(ai,a01)**2/(2*ctrl.CMIN))
        occ[k]=dict(initial_occupation_upper=A/ai,occupation_upper_at_mean_decay=A/bdy['mean_decay_a_RD'],a_after_occupation_upper_below_001=a01,decays_before_dilute_region_upper=early)
    # Full-quantile quadrature convergence, holding all other bound data fixed.
    qchecks=[];oldU,oldW=ctrl.LU,ctrl.LW
    for order in [32,64,128,256]:
        ctrl.LU,ctrl.LW=roots_laguerre(order)
        rr=ctrl.energy_bound(base,bdy['sigma_over_2mchi']);qchecks.append(dict(order=order,FS_lower_Mpc=rr['full_quantile_post_recombination_FS_lower_bound_Mpc']))
    ctrl.LU,ctrl.LW=oldU,oldW
    # Away from resonances, an intentionally broad light-scalar cross section
    # envelope y_max^4/(pi mchi²) times10000. It is evaluated at the required
    # budget and the slowest allowable RD dilution. The near-fold source has
    # m_sigma<m_a, so on-shellinverse a production is kinematically absent;
    # inverse sigma from daughters E<=m_sigma/2 requires an endpoint ofzero
    # phase-space measure. This is not a full multi-loop thermal theorem.
    yy=max(abs(base['logmass_slopes'][k])*base['gauginos_GeV'][k]/(math.sqrt(2)*R) for k in ['SU3','SU2','U1'])
    sig=10000*yy**4/(math.pi*mc**2)
    # Number upperNbudget times 2per mother, evaluated only after a source
    # timeai; extremely excessive, because it treats daughters as pre-existing.
    offshell_tau=2*Nbudget*sig/(ctrl.CMIN*ai)
    F=base['mu_GeV']**2/math.sqrt(31);dipole_sig=10000*(mc/F)**4*m*m/math.pi;dipole_tau=2*Nbudget*dipole_sig/(ctrl.CMIN*ai)
    checks=dict(two_body_boost_energy=max(abs(x['energy_ratio']-1) for x in angular)<1e-13,all_on_shell=all(x['energy_onshell'] for x in angular),Goldstino_uncertainty_does_not_make_cold=all(x['FS_Mpc']>.001 for x in sens),birth_streams_dilute_for_contributing_decays=max(v['decays_before_dilute_region_upper'] for v in occ.values())<1e-3,full_quantile_convergence=abs(qchecks[-1]['FS_lower_Mpc']/qchecks[-2]['FS_lower_Mpc']-1)<1e-4,light_offshell_small=offshell_tau<1e-10,dipole_small=dipole_tau<1e-10)
    checks={k:bool(v) for k,v in checks.items()}
    data=dict(claim_id='GC03_PRODUCTION_FINAL_NUMERICAL_CHECKS_V2',checks=checks,Goldstino_width_sensitivity=sens,two_body_energy_controls=angular,budget_boundary_source_occupation=occ,full_quantile_order_comparison=qchecks,offshell_light_scalar_optical_depth_envelope=offshell_tau,Goldstino_dipole_optical_depth_envelope=dipole_tau,near_fold_inverse_a_kinematically_closed=base['m_sigma_GeV']<base['m_phase_GeV'],runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,non_claims=['Nonabelian redistributed thermal occupations and precise collision operators uncomputed','Light-scalar envelope excludes resonant scalar processes; on-shell two-to-one kinematic absence stated for threshold-only source','Protected scalar Goldstino widths remain assumed Ward envelopes, not certified SUGRA cubics'])
    Path(out).write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
