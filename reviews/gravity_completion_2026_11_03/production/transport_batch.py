import sys,json,math,time,resource
from pathlib import Path
sys.dont_write_bytecode=True
from boltzmann_v2 import run_case,scale_row
from kernels import widths
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def finite_row():
    r=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/canonical/run_solve/result.json').read_text())['points'][-1]
    old=json.loads((HERE/'run_kernels/result.json').read_text())['rows'][4];q=dict(old)
    for k in ['t','e','mu_GeV','R_GeV','m32_GeV','gauginos_GeV']:q[k]=r[k]
    q['m_sigma_GeV']=r['rows'][-1]['m_sigma_GeV'];q['m_phase_GeV']=r['rows'][-1]['m_phase_GeV'];q['photino_GeV']=r['gauginos_GeV']['U1'];q['logmass_slopes']=r['gaugino_log_slopes']['.0025'];q['widths']=widths(q,q['logmass_slopes']);q['stationary_scope']='canonical n29 finite fixed-loop-order candidate, see canonical source checks'
    return q
def main(out,mode):
    start=time.monotonic();rows=json.loads((HERE/'run_kernels/result.json').read_text())['rows'];res=[]
    if mode=='finite_scaling':
        r=finite_row()
        for e in [.003,.004,.005,.006,.01]:
            for end in ['collisionless','instant']:
                q=scale_row(r,e);res.append(run_case(q,companion=end,nq=640,dx=.02,angular=16))
        for idx in [0,1,2,6]:res.append(run_case(rows[idx],nq=640,dx=.02,angular=16))
    elif mode=='threshold_control':
        base=rows[-1];base=dict(base);base['mu_GeV']=600578.1441860184;base['R_GeV']=base['mu_GeV']*7.367143721278508/math.sqrt(.003)*1.2667398670622447
        ratio=2.6131896076866507e-5/base['gauginos_GeV']['U1'];base['gauginos_GeV']={k:v*ratio for k,v in base['gauginos_GeV'].items()};base['photino_GeV']=base['gauginos_GeV']['U1']
        for e in [.003,.004]:
            for rr in [10.,5.,2.,math.sqrt(2),1.1,1.01,1.0001,1.000001,1.00000001,1.0000000001]:
                for end in ['collisionless','instant']:
                    q=scale_row(base,e);q['m_sigma_GeV']=2*q['photino_GeV']*rr;q['widths']=widths(q,q['logmass_slopes'])
                    z=run_case(q,companion=end,nq=640,dx=.02,angular=12);z['sigma_over_2mchi']=rr;z['scope']='Synthetic near-fold mass control; not an actual stationary point';res.append(z)
    checks=dict(yield_conservation=max(abs(r['yield_normalization_relative_error']) for r in res)<.005,phase_complete=max(r['remaining_phase'] for r in res)<1e-8)
    data=dict(claim_id='GC03_TRANSPORT_'+mode,checks=checks,cases=res,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(dict(checks=checks,cases=[{k:r[k] for k in ['e','m_sigma_GeV','mchi_GeV','companion_endpoint','free_streaming_Mpc','initial_radial_fraction','max_hidden_to_SM_during_decays','Omega_species_energy','maximum_phase_Floquet_cross_exponent_for_fitted_late_condensate','neutral_heavy_contact_optical_depth_majorant']} for r in res]),indent=2));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1],sys.argv[2])
