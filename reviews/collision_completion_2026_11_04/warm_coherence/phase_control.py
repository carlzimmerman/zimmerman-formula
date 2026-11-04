"""Phase cancellation, common-frame averaged matrix and absolute correction probe."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
import json,time,resource,math,gc
from pathlib import Path
import numpy as np
from matrix_api import *
from angular_fast import exact_events_fast
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/integration'))
from generic_orbit import GenericOrbit

def consistent(data):
    out=dict(data,current_source={k:dict(v) for k,v in data['current_source'].items()});by={g['id']:g for g in data['groups']}
    for name,gid in (('U1','F1_1'),('SU2','F3_0'),('SU3','F8_0')):out['current_source']['gauginos_over_mu'][name]=by[gid]['mass']
    return out

def rhs_loss(data,snap):
    ev=exact_events_fast(data,snap['t'],snap['q'],snap['W'],source=data['current_source'])
    mask=np.repeat([g['charged'] for g in ev.groups],len(snap['q']))
    rhs=ev.number_rhs(snap['f'].ravel(),snap['availability'].ravel())
    return -snap['t']**3*float(mask@rhs),ev.local_energy_residual

def currents(weighted,rhos,snap,channels):
    W=snap['t']**3*snap['W']/(2*math.pi**2);out={}
    for key,w in weighted.items():
        out[key]=float(np.sum(W*np.einsum('pab,pba->p',w['loss']-w['gain'],rhos))) -float(np.sum(W*np.trace(w['gain'],axis1=1,axis2=2)))
    loss=-sum(channels[key]['charged_carriers']*r for key,r in out.items())
    return loss,out

def steady_arrays(weighted):
    L=sum(w['loss'] for w in weighted.values());G=sum(w['gain'] for w in weighted.values());D=L-G
    n=len(D);coh=[];iso=[];diag=[]
    for i in range(n):
        coh.append(solve_sylvester(D[i]/2,D[i]/2,G[i]));iso.append(np.eye(4)*np.trace(G[i])/np.trace(D[i]));diag.append(np.diag(np.diag(G[i])/np.diag(D[i])))
    return np.asarray(coh),np.asarray(iso),np.asarray(diag),D

def main(out):
    start=time.monotonic();rows=[]
    for name in ('run_warm001','run_warm002'):
        snap=snapshot(ROOT/f'reviews/collision_completion_2026_11_04/integration/{name}/result.json');raw=snap['raw'];h=snap['history'];Y=np.asarray(raw['state']['Y'])
        orbit_model=GenericOrbit(snap['bg'],snap['q'],snap['W'],raw['case']['phase_nodes']);orbit_model.J0=raw['state']['J0'];orbit_model.last_x=raw['state']['xmid']
        orbit=orbit_model.orbit(snap['N'],Y,E=raw['state']['E']);H=orbit_model.hubble(snap['N'])
        ref=actual_matrices(snap['x'],snap['bg']);B0=ref['physical_basis'];avg={};parts=[];phase_rows=[];widthmin=math.inf;leakage=0.;maxinterp=0.;maxenergy=0.;coverage=True
        for x,w in zip(orbit['xs'],orbit['weights']):
            p=actual_matrices(float(x),snap['bg']);wm,_=weighted_matrices(p,snap)
            summary=summarize(p,snap,wm);R=B0.T@p['physical_basis'];sv=np.linalg.svd(R,compute_uv=False);leakage=max(leakage,float(max(abs(sv-1))))
            mapped={key:{label:np.einsum('ab,pbc,dc->pad',R,v,R,optimize=True) for label,v in z.items()} for key,z in wm.items()}
            if not avg:avg={key:{label:w*v.copy() for label,v in z.items()} for key,z in mapped.items()}
            else:
                for key,z in mapped.items():
                    if key not in avg:avg[key]={label:np.zeros_like(v) for label,v in z.items()}
                    for label,v in z.items():avg[key][label]+=w*v
            parts.append((float(w),mapped,p['channels']))
            data=snap['bg'].at(float(x));rawloss,er=rhs_loss(data,snap);closs,er2=rhs_loss(consistent(data),snap)
            whole=closs if name=='run_warm002' else rawloss
            maxenergy=max(maxenergy,er,er2);widthmin=min(widthmin,summary['min_net_width']);coverage=coverage and not p['parent_as_daughter_channels'] and not p['parent_as_daughter_background']
            maxinterp=max(maxinterp,max(p['interpolation_width_relative'].values(),default=0.))
            phase_rows.append(dict(x=float(x),weight=float(w),whole25_matching_charged_loss_mu4=whole,
                whole25_common_consistent_charged_loss_mu4=closs,whole25_raw_source_charged_loss_mu4=rawloss,
                P_local_coherent_steady_charged_loss_mu4=summary['coherent_stationary_charged_loss_mu4'],
                P_local_isotropic_steady_charged_loss_mu4=summary['isotropic_stationary_charged_loss_mu4'],
                P_actual_isotropic_charged_loss_mu4=summary['actual_isotropic_charged_loss_mu4'],
                min_net_width=summary['min_net_width']))
            del p,wm,summary,data;gc.collect()
        # All actual phases have the same open parent channel set here.
        rho,riso,rdiag,Davg=steady_arrays(avg);channels=ref['channels']
        C,cc=currents(avg,rho,snap,channels);I,ci=currents(avg,riso,snap,channels);DG,cd=currents(avg,rdiag,snap,channels)
        actual=np.asarray([f*np.eye(4) for f in snap['f'][snap['by'][ref['parent_id']]]]);A,ca=currents(avg,actual,snap,channels)
        whole=sum(r['weight']*r['whole25_matching_charged_loss_mu4'] for r in phase_rows)
        wholecommon=sum(r['weight']*r['whole25_common_consistent_charged_loss_mu4'] for r in phase_rows)
        local_delta=sum(r['weight']*(r['P_local_coherent_steady_charged_loss_mu4']-r['P_local_isotropic_steady_charged_loss_mu4']) for r in phase_rows)
        local_triangle=sum(r['weight']*abs(r['P_local_coherent_steady_charged_loss_mu4']-r['P_local_isotropic_steady_charged_loss_mu4']) for r in phase_rows)
        avg_triangle=0.
        for w,mapped,ch in parts:
            cp,_=currents(mapped,rho,snap,ch);ip,_=currents(mapped,riso,snap,ch);avg_triangle+=w*abs(cp-ip)
        rows.append(dict(input=name,N=snap['N'],phase_nodes=len(phase_rows),phases=phase_rows,
            whole25_phase_average_charged_loss_mu4=whole,whole25_common_consistent_phase_average_charged_loss_mu4=wholecommon,
            phasewise_local_stationary_coherence_difference_mu4=local_delta,
            phasewise_absolute_correction_triangle_mu4=local_triangle,
            phasewise_triangle_over_whole25=local_triangle/abs(whole),
            averaged_matrix_coherent_P_charged_loss_mu4=C,averaged_matrix_isotropic_P_charged_loss_mu4=I,
            averaged_matrix_unequal_diagonal_P_charged_loss_mu4=DG,actual_isotropic_P_phase_average_charged_loss_mu4=A,
            coherent_over_isotropic_averaged_matrix=C/I,coherent_over_unequal_diagonal_averaged_matrix=C/DG,
            averaged_matrix_absolute_triangle_mu4=avg_triangle,averaged_matrix_triangle_over_whole25=avg_triangle/abs(whole),
            averaged_matrix_net_correction_over_whole25=(C-I)/abs(whole),
            coherent_replacement_of_actual_P_over_whole25=(C-A)/abs(whole),
            minimum_damping_over_H=widthmin/H,minimum_damping_over_omega=widthmin/orbit['omega'],
            parent_subspace_max_leakage=leakage,actual_parent_daughter_coverage=coverage,
            exact_phase_energy_residual=maxenergy,maximum_vertex_interpolation_width_error=maxinterp,
            reconstructed_omega_relative=abs(orbit['omega']/h['omega']-1),
            reconstructed_turningpoint_error=max(abs(orbit['x_inner']-h['x_inner']),abs(orbit['x_outer']-h['x_outer'])),
            averaged_matrices={key:{k:v.tolist() for k,v in vals.items()} for key,vals in avg.items()},
            averaged_coherent_density=rho.tolist(),averaged_isotropic_density=riso.tolist(),
            averaged_coherent_channel_currents=cc,averaged_isotropic_channel_currents=ci,
            scope='Frozen actual bath and recorded8-node orbit. Phasewise steady and common-frame averaged matrix steady are separately conditional probes, not a solved periodic density matrix. Triangle bounds apply to their respective tested closures, not arbitrary uncomputed transport.'))
    checks=dict(actual_phase_parent_coverage=all(r['actual_parent_daughter_coverage'] for r in rows),
        common_subspace=all(r['parent_subspace_max_leakage']<1e-12 for r in rows),
        exact_phase_energy=all(r['exact_phase_energy_residual']<1e-11 for r in rows),
        recorded_orbit=all(r['reconstructed_turningpoint_error']<1e-8 and r['reconstructed_omega_relative']<1e-7 for r in rows),
        triangle_consistency=all(abs(r['averaged_matrix_net_correction_over_whole25'])<=r['averaged_matrix_triangle_over_whole25']*(1+1e-10) and abs(r['phasewise_local_stationary_coherence_difference_mu4'])<=r['phasewise_absolute_correction_triangle_mu4']*(1+1e-10) for r in rows))
    result=dict(claim_id='CC10_WARM_COHERENCE_PHASE_CANCELLATION',checks=checks,rows=rows,
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(serialize(result),indent=2)+'\n');print(json.dumps(dict(checks=checks,summaries=[{k:r[k] for k in ('input','whole25_phase_average_charged_loss_mu4','phasewise_triangle_over_whole25','averaged_matrix_triangle_over_whole25','coherent_over_isotropic_averaged_matrix','coherent_over_unequal_diagonal_averaged_matrix','minimum_damping_over_H','minimum_damping_over_omega','parent_subspace_max_leakage')} for r in rows],runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'])));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
