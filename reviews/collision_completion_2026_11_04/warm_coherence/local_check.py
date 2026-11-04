"""Finite actual warm-state four-singlet gain/loss matrix check."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
import time,resource,json,math
from pathlib import Path
import numpy as np
from matrix_api import *

def thermal_test(packet,snap,T=.01):
    q=snap['q'];t=snap['t'];eta=np.asarray([1 if g['kind']=='S' else -1 for g in snap['groups']])[:,None]
    energies=np.asarray([np.sqrt(packet['masses'][g['id']]**2+(t*q)**2) for g in snap['groups']])
    f=1/(np.exp(energies/T)-eta);av=1+eta*f
    wm,_=weighted_matrices(packet,snap,f_override=f,av_override=av)
    loss=sum(w['loss'] for w in wm.values());gain=sum(w['gain'] for w in wm.values());EP=np.sqrt(packet['M']**2+(t*q)**2)
    errors=[];balance=[]
    for i in range(len(q)):
        D=loss[i]-gain[i];rho=solve_sylvester(D/2,D/2,gain[i]);want=1/math.expm1(EP[i]/T)
        errors.append(float(np.linalg.norm(rho-want*np.eye(4))/(2*want)))
        balance.append(float(np.linalg.norm(gain[i]-math.exp(-EP[i]/T)*loss[i])/max(np.linalg.norm(gain[i]),1e-300)))
    return dict(T_bath=T,maximum_thermal_isotropy_relative=max(errors),maximum_channel_KMS_relative=max(balance))

def angle_test(packet,snap):
    q=snap['q'];t=snap['t'];en={g:np.sqrt(m*m+(t*q)**2) for g,m in packet['masses'].items()};errors=[]
    for key,mat in packet['matrices'].items():
        ch=packet['channels'][key];j,k=ch['first'],ch['second'];jj=snap['by'][j];kk=snap['by'][k]
        for i in (0,16,24,31,39):
            args=(packet['M'],packet['masses'][j],packet['masses'][k],t*q[i],en[j],en[k],snap['f'][jj],snap['f'][kk],snap['availability'][jj],snap['availability'][kk])
            exact=angular_factors(*args);g16=angular_factors(*args,gauss=16);g32=angular_factors(*args,gauss=32)
            scale=max(exact[0]+exact[1],1e-100)
            errors.append(dict(channel=key,parent_node=i,GL16_relative=(abs(g16[0]-exact[0])+abs(g16[1]-exact[1]))/scale,
                          GL32_relative=(abs(g32[0]-exact[0])+abs(g32[1]-exact[1]))/scale))
    return dict(max_GL16=max(x['GL16_relative'] for x in errors),max_GL32=max(x['GL32_relative'] for x in errors),cases=len(errors),worst_GL32=max(errors,key=lambda x:x['GL32_relative']))

def main(out):
    start=time.monotonic();rows=[]
    for name in ('run_warm001','run_warm002'):
        path=ROOT/f'reviews/collision_completion_2026_11_04/integration/{name}/result.json';snap=snapshot(path);h=snap['history']
        packet=actual_matrices(snap['x'],snap['bg']);wm,cov=weighted_matrices(packet,snap);result=summarize(packet,snap,wm)
        frame=[]
        for x in (h['x_inner'],h['x_outer']):
            B=basis_at(float(x),packet['P']);singular=np.linalg.svd(packet['physical_basis'].T@B,compute_uv=False)
            frame.append(dict(x=x,parent_subspace_singular_values=singular.tolist(),maximum_subspace_leakage=float(max(abs(1-singular)))))
        # Actual scalar total loss/source matrices retained for root integration.
        mats={key:dict(loss=w['loss'].tolist(),gain=w['gain'].tolist(),vacuum=packet['matrices'][key].tolist()) for key,w in wm.items()}
        manifest=json.loads((path.parent/'manifest.json').read_text())
        rows.append(dict(input=str(path.relative_to(ROOT)),upstream_run_status=manifest['run']['status'],N=snap['N'],x=snap['x'],Tc=snap['t'],
             parent_id=packet['parent_id'],parent_indices=packet['P'],parent_mass=packet['M'],hole_source=snap['hole_source'],
             current_parent_f=snap['f'][snap['by'][packet['parent_id']]].tolist(),physical_basis=packet['physical_basis'].tolist(),
             matrices=mats,summary=result,thermal=thermal_test(packet,snap),angular=angle_test(packet,snap),basis_turning_controls=frame,
             parent_as_daughter_channels=packet['parent_as_daughter_channels'],parent_as_daughter_background=packet['parent_as_daughter_background'],
             vacuum_width_interpolation_relative=packet['interpolation_width_relative'],
             max_angular_omitted_fraction=max(float(max(1-v)) for v in cov.values()),
             minimum_weighted_loss_eigenvalue=min(float(np.linalg.eigvalsh(v['loss']).min()) for v in wm.values()),
             minimum_weighted_gain_eigenvalue=min(float(np.linalg.eigvalsh(v['gain']).min()) for v in wm.values())))
    pole=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/microphysics/run_pole002/result.json').read_text())
    pp=actual_matrices(pole['xpole']);ours=np.linalg.eigvalsh(sum(pp['matrices'].values()));ref=np.asarray(pole['Gamma_other_eigenvalues_mu'])
    pole_error=float(np.max(abs(ours/ref-1)))
    checks=dict(actual_parent_identity=all(x['parent_id']=='S1_1' and len(x['parent_indices'])==4 for x in rows),
        actual_parent_channel_coverage=all(not x['parent_as_daughter_channels'] and not x['parent_as_daughter_background'] for x in rows),
        weighted_positive_matrices=all(x['minimum_weighted_loss_eigenvalue']>-1e-18 and x['minimum_weighted_gain_eigenvalue']>-1e-18 for x in rows),
        exact_angular_control=all(x['angular']['max_GL32']<1e-5 for x in rows),
        thermal_detailed_balance=all(x['thermal']['maximum_channel_KMS_relative']<1e-10 and x['thermal']['maximum_thermal_isotropy_relative']<1e-8 for x in rows),
        actual_pole_spectrum_control=pole_error<1e-8,
        stationary_matrix_equation=all(max(r.get('stationary_trace_residual',0.) for r in x['summary']['momentum_rows'])<1e-10 for x in rows),
        steady_PSD=all(min(r.get('minimum_rho_eigenvalue',0.) for r in x['summary']['momentum_rows'])>-1e-12 for x in rows))
    result=dict(claim_id='CC10_WARM_ACTUAL_FOUR_SINGLET_COHERENCE',checks={k:bool(v) for k,v in checks.items()},rows=rows,
        pole_width_eigenvalue_relative_error=pole_error,
        scope='Actual-x full-basis cubic/Yukawa matrices, same warm common daughter masses, exact angular entropy projection, actual stored occupations/holes. Frozen-bath local bosonic matrix gain/loss diagnostic with bare degenerate H=MI. No full periodic/orbit transport, dispersive selfenergy or complete kinetic history claim.',
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(serialize(result),indent=2)+'\n')
    print(json.dumps(dict(checks=result['checks'],runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'],summaries=[dict(N=r['N'],x=r['x'],charged_loss_coherent=r['summary']['coherent_stationary_charged_loss_mu4'],charged_loss_isotropic=r['summary']['isotropic_stationary_charged_loss_mu4'],ratio=r['summary']['coherent_over_isotropic_stationary_charged_loss'],parent_number_ratio=r['summary']['parent_number_coherent_mu3']/r['summary']['parent_number_isotropic_mu3'],angular=r['angular'],thermal=r['thermal'],min_net_width=r['summary']['min_net_width'],subspace_leakage=max(c['maximum_subspace_leakage'] for c in r['basis_turning_controls'])) for r in rows])))
    assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
