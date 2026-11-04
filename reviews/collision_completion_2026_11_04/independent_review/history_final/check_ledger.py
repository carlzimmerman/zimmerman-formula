"""Read-only ancestry and orbital error-scale reconstruction; no time evolution."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'reviews/collision_completion_2026_11_04'
sys.path.insert(0,str(BASE/'cascades'))
sys.path.insert(0,str(BASE/'integration'))
from consistent_background import ConsistentVertexBackground
from generic_orbit import GenericOrbit

def main(out):
    start=time.monotonic();names=['integration/run_initial001','integration/run_fresh_exact001','integration/run_fresh_exact002','history/run_advance001','history/run_advance002']
    chain=[json.loads((BASE/n/'result.json').read_text()) for n in names];initial=chain[0];E0=initial['state']['E'];gas0=initial['state']['gas0'];joins=[]
    for i in range(1,len(chain)):
        a=chain[i-1];b=chain[i];x=a['case']['history'][-1];y=b['case']['history'][0]
        joins.append(dict(prior=names[i-1],next=names[i],delta_N=y['N']-x['N'],
            initialY_equal=a['state']['initialY']==b['state']['initialY'],q_equal=a['case']['q']==b['case']['q'],W_equal=a['case']['W']==b['case']['W'],
            boundary_count_L1=float(np.sum(abs(np.array(y['comoving_number_by_group'])-np.array(x['comoving_number_by_group'])))),
            boundary_ledger_difference=y.get('independent_energy_work_residual',0)-x.get('independent_energy_work_residual',0),
            energy_reference=b['state'].get('energy_reference_E',E0)))
    final=chain[-1];s=final['state'];h=final['case']['history'][-1];residual=s['E']+s['independent_work']-s['energy_reference_E']
    q=np.array(final['case']['q']);W=np.array(final['case']['W']);Y=np.array(s['Y']);bg=ConsistentVertexBackground(BASE/'cascades/run_vertices001/result.json');rows=[]
    for phases in (8,16,32):
        model=GenericOrbit(bg,q,W,phases);model.J0=s['J0'];model.last_x=s['xmid'];orb=model.orbit(s['N'],Y,J=s['J'])
        excitation=orb['E']-orb['minimum'];rows.append(dict(phases=phases,E=orb['E'],minimum=orb['minimum'],excitation=excitation,
            omega_J=orb['omega']*orb['J'],stored_absolute_ledger_residual=residual,
            residual_over_excitation=abs(residual)/excitation,residual_over_omegaJ=abs(residual)/(orb['omega']*orb['J']),
            reconstructed_energy_vs_stored=orb['E']-s['E'],x_inner=orb['x_inner'],x_outer=orb['x_outer']))
    trace=json.loads((BASE/'warm_coherence/run_trace001/result.json').read_text());coherence=[]
    for rec in trace['rows']:
        input_data=json.loads((BASE/'integration'/rec['input']/'result.json').read_text());q=np.array(rec['q']);weights=np.array(input_data['case']['W']);t=input_data['case']['history'][-1]['Tc_over_mu'];Wphys=t**3*weights/(2*np.pi**2)
        S=np.array(rec['source_trace_max_mu']);g=np.array(rec['net_damping_gap_min_mu']);Nmax=S/g;actual=np.array(rec['actual_parent_trace']);norm=np.array(rec['charged_matrix_average_operator_norm_mu']);maxnorm=np.array(rec['charged_matrix_maximum_operator_norm_mu'])
        bound=float(Wphys@(norm*(Nmax+actual)));uniform=float(Wphys@(maxnorm*(Nmax+actual)))
        coherence.append(dict(input=rec['input'],input_N=input_data['state']['N'],trace_bound_relative=float(np.max(abs(Nmax/np.array(rec['periodic_parent_trace_upper'])-1))),
            reconstructed_current_bound=bound,pinned_current_bound=rec['arbitrary_PSD_periodic_vs_fixed_actual_parent_current_bound_mu4'],relative=abs(bound/rec['arbitrary_PSD_periodic_vs_fixed_actual_parent_current_bound_mu4']-1),
            reconstructed_uniform_bound=uniform,pinned_fraction=rec['periodic_vs_actual_bound_over_whole25']))
    checks=dict(ancestry_continuity=all(r['delta_N']==0 and r['initialY_equal'] and r['q_equal'] and r['W_equal'] and r['boundary_count_L1']<1e-12 and abs(r['boundary_ledger_difference'])<1e-12 for r in joins),
        common_Eref=all(r['energy_reference']==E0 for r in joins),ledger_matches=abs(residual/gas0-h['independent_energy_work_residual'])<1e-14,
        orbit_reconstruction=abs(rows[0]['reconstructed_energy_vs_stored'])<1e-20,trace_aggregation=max(r['relative'] for r in coherence)<1e-12)
    r=dict(joins=joins,final_normalized_ledger_residual=residual/gas0,final_absolute_ledger_residual=residual,orbit_scales=rows,coherence_aggregation=coherence,
        checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
