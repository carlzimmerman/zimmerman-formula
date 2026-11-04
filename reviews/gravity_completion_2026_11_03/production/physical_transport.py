import sys,json,math,time,resource
from pathlib import Path
sys.dont_write_bytecode=True
from boltzmann_v3 import run_case,RHOCHI,TG0,MP
from kernels import widths,profile
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def source_energy_bound(r):
    m=r['m_sigma_GeV'];R=r['R_GeV'];alpha=.01
    T=(90/(math.pi**2*106.75))**.25*math.sqrt(m*MP)
    ai=TG0/T*((43/11)/106.75)**(1/3)
    maxrho=m*m*R*R*alpha*alpha*ai**3
    return dict(alpha_radial_displacement_over_R=alpha,H_equals_m_T_GeV=T,a_initial=ai,maximum_possible_Omega_chi_fraction=maxrho/RHOCHI,scope='Energy-only upper bound: every initial radial energy quantum may become perfectly cold chi; requires isolated post-onset hidden sector with nonnegative averaged pressure')
def main(out):
    start=time.monotonic();krows=json.loads((HERE/'run_kernels/result.json').read_text())['rows'];base=krows[-1];rows=[]
    for p in json.loads((ROOT/'reviews/gravity_completion_2026_11_03/canonical/run_nearfold/result.json').read_text())['threshold_points']:
        if p['nodes']!=29:continue
        r=dict(base)
        for key in ['t','mu_GeV','R_GeV','m_sigma_GeV','m_phase_GeV','m32_GeV','gauginos_GeV']:r[key]=p[key]
        r['photino_GeV']=p['gauginos_GeV']['U1'];r['logmass_slopes']=p['gaugino_log_slopes']['.0025'];r['widths']=widths(r,r['logmass_slopes']);r['source_label']='canonical finite stationary n29 ratio='+str(p['target_ratio']);rows.append(r)
    p=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/protected/run_finite_001/result.json').read_text())['rows'][-1]
    e=.003;mu=18170662.111498855;t=float(p['t']);m0,gap,deg=profile(t,e);slope=[]
    for h in [.001,.0005]:
        vals=[profile(t*math.exp(j*h),e)[0] for j in [-2,-1,1,2]]
        slope.append({k:(vals[0][k]-8*vals[1][k]+8*vals[2][k]-vals[3][k])/(12*h*m0[k]) for k in m0})
    r=dict(t=t,e=e,mu_GeV=mu,R_GeV=float(p['T_GeV']),m_sigma_GeV=p['neutral_scalar_masses_GeV'][1],m_phase_GeV=p['neutral_scalar_masses_GeV'][0],m32_GeV=p['leading_Ward_zeta_GeV'],physical_gravitino_GeV=p['m32_GeV'],photino_GeV=p['photino_GeV'],gauginos_GeV={k:mu*v for k,v in m0.items()},logmass_slopes=slope[-1],min_heavy_gap_GeV=gap*mu,source_label='protected finite stationary n29; GG daughter is uneaten zeta, not gravitino',photino_current_tau_override=p['leading_current_partial_lifetime_seconds'])
    r['widths']=widths(r,r['logmass_slopes']);r['slope_convergence']=max(abs(slope[0][k]/slope[1][k]-1) for k in m0);rows.append(r)
    result=[]
    for r in rows:
        for end in ['collisionless','instant']:
            z=run_case(r,nq=900,dx=.015,angular=24,companion=end,save_spectrum=True)
            z['source_label']=r['source_label'];z['source_row']=r;z['energy_only_small_misalignment_bound']=source_energy_bound(r)
            if 'photino_current_tau_override' in r:
                tau=r['photino_current_tau_override'];z['unavoidable_Ward_partial_tau_s']=tau;z['unavoidable_Ward_survival_13p8Gyr']=math.exp(-4.3549488e17/tau)
                z['protected_GG_scope']='Computed leading matter-Goldstino envelope as uneatenzeta; physical gravitino/mixed neutral scalar couplings need full matching. All-Goldstino partial energy fraction is explicitly recorded and tiny.'
            result.append(z)
    # Resolution check only for actual protected cascade and strongest actual
    # canonical nearthreshold point; do not repeat all cases without need.
    resolution=[]
    for r in [rows[0],rows[-1]]:
        low=run_case(r,nq=600,dx=.03,angular=16)
        hi=next(x for x in result if x['source_label']==r['source_label'] and x['companion_endpoint']=='collisionless')
        resolution.append(dict(source=r['source_label'],FS_relative_difference=abs(low['free_streaming_Mpc']/hi['free_streaming_Mpc']-1),DeltaNeff_absolute_difference=abs(low['snapshots']['recombination_benchmark']['DeltaNeff_pressure_equivalent']-hi['snapshots']['recombination_benchmark']['DeltaNeff_pressure_equivalent'])))
    checks=dict(all_yields_conserved=max(abs(r['yield_normalization_relative_error']) for r in result)<.005,protected_slopes_converged=rows[-1]['slope_convergence']<1e-4,FS_resolutions_agree=max(x['FS_relative_difference'] for x in resolution)<.005,all_small_harmonic_energy_fails=max(r['energy_only_small_misalignment_bound']['maximum_possible_Omega_chi_fraction'] for r in result)<1)
    data=dict(claim_id='GC03_ACTUAL_CANONICAL_PROTECTED_TRANSPORT',checks=checks,cases=result,resolution=resolution,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Actual finite-action stationary data, conditional leading currents; nonabelian endpoints are exploratory budgets; no full nonabelian kinetic solution')
    Path(out).write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(dict(checks=checks,resolution=resolution,selected=[{k:r[k] for k in ['source_label','companion_endpoint','free_streaming_Mpc','neutral_heavy_contact_optical_depth_majorant','maximum_shell_occupation_per_helicity','maximum_phase_Floquet_cross_exponent_for_fitted_late_condensate','max_hidden_to_SM_during_decays','energy_only_small_misalignment_bound']} for r in result]),indent=2));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
