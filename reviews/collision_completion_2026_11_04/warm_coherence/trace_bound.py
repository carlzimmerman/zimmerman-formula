"""Rigorous PSD trace bound for the declared frozen-bath8phase matrix model."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
import json,time,resource,math,gc
from pathlib import Path
import numpy as np
from matrix_api import *

def main(out):
    start=time.monotonic();here=Path(__file__).resolve().parent;phase=json.loads((here/'run_phase001/result.json').read_text());rows=[]
    for rec in phase['rows']:
        snap=snapshot(ROOT/f"reviews/collision_completion_2026_11_04/integration/{rec['input']}/result.json")
        ref=actual_matrices(snap['x'],snap['bg']);B0=ref['physical_basis'];pid=ref['parent_id']
        sources=[];gaps=[];scalar_gaps=[];Anorm=[];weights=[];minimum_gain=math.inf;coverage=True
        for entry in rec['phases']:
            packet=actual_matrices(entry['x'],snap['bg']);wm,_=weighted_matrices(packet,snap);R=B0.T@packet['physical_basis']
            mapped={key:{k:np.einsum('ab,pbc,dc->pad',R,v,R,optimize=True) for k,v in z.items()} for key,z in wm.items()}
            L=sum(v['loss'] for v in mapped.values());G=sum(v['gain'] for v in mapped.values());D=L-G
            A=sum(packet['channels'][key]['charged_carriers']*(v['loss']-v['gain']) for key,v in mapped.items())
            sources.append(np.trace(G,axis1=1,axis2=2));gaps.append(np.linalg.eigvalsh(D)[:,0]);scalar_gaps.append(np.trace(D,axis1=1,axis2=2)/4)
            Anorm.append(np.max(abs(np.linalg.eigvalsh(A)),axis=1));weights.append(entry['weight'])
            minimum_gain=min(minimum_gain,float(np.linalg.eigvalsh(G).min()));coverage=coverage and not packet['parent_as_daughter_channels']
            del packet,wm,mapped;gc.collect()
        Smax=np.max(sources,axis=0);gmin=np.min(gaps,axis=0);dmin=np.min(scalar_gaps,axis=0)
        Nmax=Smax/gmin;Niso_max=Smax/dmin;Nactual=4*snap['f'][snap['by'][pid]]
        avg_norm=np.asarray(weights)@np.asarray(Anorm);max_norm=np.max(Anorm,axis=0)
        W=snap['t']**3*snap['W']/(2*math.pi**2)
        actual_bound=float(W@(avg_norm*(Nmax+Nactual)))
        uniform_actual_bound=float(W@(max_norm*(Nmax+Nactual)))
        periodic_bound=float(W@(avg_norm*(Nmax+Niso_max)))
        initial_trace_bound=float(W@(avg_norm*(np.maximum(Nmax,Nactual)+Nactual)))
        whole=abs(rec['whole25_phase_average_charged_loss_mu4']);observed=abs(rec['averaged_matrix_coherent_P_charged_loss_mu4']-rec['actual_isotropic_P_phase_average_charged_loss_mu4'])
        rho=np.asarray(rec['averaged_coherent_density']);nsteady=np.trace(rho,axis1=1,axis2=2)
        rows.append(dict(input=rec['input'],N=rec['N'],q=snap['q'].tolist(),source_trace_max_mu=Smax.tolist(),net_damping_gap_min_mu=gmin.tolist(),
            periodic_parent_trace_upper=Nmax.tolist(),isotropic_periodic_trace_upper=Niso_max.tolist(),actual_parent_trace=Nactual.tolist(),
            charged_matrix_average_operator_norm_mu=avg_norm.tolist(),charged_matrix_maximum_operator_norm_mu=max_norm.tolist(),
            arbitrary_PSD_periodic_vs_fixed_actual_parent_current_bound_mu4=actual_bound,
            uniform_in_phase_current_bound_mu4=uniform_actual_bound,
            arbitrary_PSD_periodic_vs_isotropic_periodic_bound_mu4=periodic_bound,
            frozen_bath_evolution_same_initial_trace_bound_mu4=initial_trace_bound,
            periodic_vs_actual_bound_over_whole25=actual_bound/whole,
            uniform_phase_bound_over_whole25=uniform_actual_bound/whole,
            two_periodic_bound_over_whole25=periodic_bound/whole,
            same_initial_trace_bound_over_whole25=initial_trace_bound/whole,
            measured_averaged_matrix_vs_actual_difference_mu4=observed,
            observed_difference_over_bound=observed/actual_bound,
            maximum_averaged_steady_trace_over_periodic_bound=float(np.max(nsteady/Nmax)),
            min_damping=float(min(gmin)),minimum_gain_eigenvalue=minimum_gain,actual_parent_coverage=coverage,
            scope='Pointwise trace/charged-current bound for the declared8phase frozen bath and its positive convex interpolants; no instantaneous-steady or particular Hermitian Hamiltonian assumption. Phase-weighted bound uses the declared node durations; phase-uniform version bounds any ordering/duration. Reference actual parent is the stored isotropic fI. No evolving bath/history theorem.'))
    checks=dict(positive_damping=all(r['min_damping']>0 for r in rows),positive_gain=all(r['minimum_gain_eigenvalue']>-1e-18 for r in rows),
        parent_coverage=all(r['actual_parent_coverage'] for r in rows),
        existing_steady_trace=all(r['maximum_averaged_steady_trace_over_periodic_bound']<=1+1e-10 for r in rows),
        observed_current_bound=all(r['observed_difference_over_bound']<=1+1e-10 for r in rows),
        phase_uniform_is_conservative=all(r['uniform_phase_bound_over_whole25']>=r['periodic_vs_actual_bound_over_whole25']*(1-1e-12) for r in rows))
    result=dict(claim_id='CC10_WARM_COHERENCE_PERIODIC_TRACE_ENVELOPE',checks=checks,rows=rows,
        proof='For any PSD rho, Tr rho_dot=Tr G−Tr D rho<=Smax−gamma_min Tr rho; any PSD periodic response therefore has Tr rho<=Smax/gamma_min. Hermitian commutators have zero trace. Net charged current difference at fixed bath is Tr A(rho−rho_ref), bounded by ||A||op(Tr rho+Tr rho_ref). Aggregate positive momentum and declared phase weights. For isotropic periodic trace response use min TrD/4. For finite frozen-bath flow initialized at traceN0 use max(N0,Smax/gamma_min).',
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(serialize(result),indent=2)+'\n');print(json.dumps(dict(checks=checks,summaries=[{k:r[k] for k in ('input','periodic_vs_actual_bound_over_whole25','uniform_phase_bound_over_whole25','two_periodic_bound_over_whole25','same_initial_trace_bound_over_whole25','observed_difference_over_bound')} for r in rows],runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'])));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
