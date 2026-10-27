"""One-thread bounded timing and targeted generator audit, not new evolution.

The old CTMC already stores radius counts, not a particle edge table. This
compares actual count-only cKDTree construction/draws with cell construction
and null proposals. Synthetic replicated states are labelled, not high-N runs.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import argparse,json,resource,time,unittest
from pathlib import Path
import numpy as np
import cell2_scatter as cell
import cell_scatter as previous
import null_scatter as old

HERE=Path(__file__).resolve().parent


def target_hazards(x,v,mass,h,target,neighbors):
    d=x[target]-x[neighbors];radius=np.linalg.norm(d,axis=1)
    keep=(radius>0.)&(radius<h);neighbors=neighbors[keep];d=d[keep];radius=radius[keep]
    order=np.argsort(neighbors);neighbors=neighbors[order];d=d[order];radius=radius[order]
    w=v[target]-v[neighbors];z=np.sum(w*w,axis=1)/(2*.02*306601.39378555055)**2
    ratio=((2-z/(1-z))/2)**2/(1+.02**2*z)
    incoming=np.maximum(-np.sum(w*d/radius[:,None],axis=1),0.)
    rate=3*mass*.3*.0002088420524663771/(np.pi*h**3)*ratio*incoming
    return neighbors,rate


def generator_audit(graph,reference,x,v,mass,h,rng):
    n=len(x);targets=np.unique(np.r_[rng.choice(n,min(256,n),replace=False),np.argsort(reference.counts,kind='stable')[-min(64,n):]])
    inverse=np.empty(n,np.int64);inverse[graph.particles]=np.arange(n)
    total=0.;active=0;selected_pairs=0;max_error=0.
    for i in targets:
        row=int(np.searchsorted(graph.starts,inverse[i],side='right')-1)
        columns=graph.neighbors[row];columns=columns[columns>=0]
        candidates=np.concatenate([graph.particles[graph.starts[c]:graph.starts[c]+graph.counts[c]] for c in columns])
        a,ra=target_hazards(x,v,mass,h,i,candidates)
        b,rb=target_hazards(x,v,mass,h,i,np.asarray(reference.tree.query_ball_point(x[i],h),np.int64))
        if not np.array_equal(a,b):raise AssertionError('selected target support differs from independent radius tree')
        if not np.array_equal(ra,rb):raise AssertionError('selected target same-state physical rates differ')
        selected_pairs+=len(a);active+=int(np.count_nonzero(ra));total+=float(ra.sum())
        max_error=max(max_error,float(np.max(abs(ra-rb))) if len(ra) else 0.)
    return dict(targets=len(targets),directed_target_neighbors=selected_pairs,active_directed_target_neighbors=active,
        selected_target_participation_rate_sum_per_Myr=total,maximum_hazard_absolute_difference=max_error,
        interpretation='Exact rates on stated random+dense targets only; selected sum is not a global rate estimator')


def invariants(x,before,after,m):
    scaleE=.5*float(np.sum(m[:,None]*before*before));delta=after-before
    P=np.sum(m[:,None]*delta,axis=0);J=np.sum(np.cross(x,m[:,None]*delta),axis=0)
    pscale=float(np.sum(m*np.linalg.norm(before,axis=1)));jscale=float(np.sum(m*np.linalg.norm(x,axis=1)*np.linalg.norm(before,axis=1)))
    return dict(relative_energy_defect=float(abs(.5*np.sum(m[:,None]*(after*after-before*before)))/scaleE),
        normalized_momentum_defect=float(np.linalg.norm(P)/pscale),normalized_vectorJ_defect=float(np.linalg.norm(J)/max(jscale,1.e-100)))


def main(output):
    start=time.monotonic();result=dict(rows=[],test_summary=None,native_backend=cell.backend_metadata(),
        interpretation='Frozen-snapshot finite-h C22 proposal feasibility; no new physical trajectory or convergence result',
        old_method='cKDTree radius degree counts; selected neighbor list per proposal; no edge table',
        new_method='NativeC hashgrid width2h27neighborcell table and exact integer ticket lookup; same nulls/rates ascellv1',
        resources=dict(max_CPU_threads=1,wall_cap_seconds=60),synthetic_seed=78307)
    suite=unittest.defaultTestLoader.loadTestsFromNames(('test_null_scatter','test_cell_scatter','test_cell2_scatter'))
    tick=time.monotonic();test=unittest.TextTestRunner(verbosity=2).run(suite)
    result['test_summary']=dict(tests_run=test.testsRun,failures=len(test.failures),errors=len(test.errors),seconds=time.monotonic()-tick)
    if not test.wasSuccessful():raise AssertionError('cell unit tests failed')
    prepared=np.load(HERE/'initial_n262144_s87319'/'initial.npz')
    frozen=np.load(HERE/'run_pilot_gpu8k_iso'/'final.npz')
    rng=np.random.default_rng(78307)
    copies=32
    sx=np.tile(frozen['x'],(copies,1))+rng.normal(size=(len(frozen['m'])*copies,3))*.01
    sv=np.tile(frozen['v'],(copies,1));sm=np.tile(frozen['m']/copies,copies);sc=np.tile(frozen['cold'],copies)
    cases=[('actual_prepared_initial_cold262144',prepared['x'],prepared['v'],prepared['m'],prepared['cold'],25.,False),
        ('actual_frozen8k_endpoint',frozen['x'],frozen['v'],frozen['m'],frozen['cold'],25.,False),
        ('synthetic32jittered_copies_of8k_endpoint',sx,sv,sm,sc,25.,True),
        ('synthetic32jittered_copies_of8k_endpoint_h100',sx,sv,sm,sc,100.,True)]
    for label,x,v,m,cold,h,synthetic in cases:
        xc,vc=x[cold],v[cold];ticks=[]
        for _ in range(3):
            tick=time.perf_counter();graph=cell.CellProposal(xc,h);ticks.append(time.perf_counter()-tick)
        new_build=float(np.median(ticks))
        tick=time.perf_counter();prior=previous.CellProposal(xc,h);prior_build=time.perf_counter()-tick
        if graph.oriented_count!=prior.oriented_count:raise AssertionError('native and previous candidate measure differs')
        tick=time.perf_counter();ref=old.NeighborProposal(xc,h);old_build=time.perf_counter()-tick
        audit=generator_audit(graph,ref,xc,vc,m[cold][0],h,rng)
        draws=[]
        for proposal in (graph,prior,ref):
            tick=time.perf_counter()
            for _ in range(2000):proposal.draw(rng)
            draws.append((time.perf_counter()-tick)/2000)
        row=dict(case=label,synthetic=synthetic,Ncold=int(cold.sum()),Ntotal=len(m),h_pc=h,
            new_build_seconds=new_build,native_build_three_timings_seconds=ticks,previous_cell_build_seconds=prior_build,old_degree_build_seconds=old_build,
            build_speedup_old_over_new=old_build/new_build,new_oriented_candidates=graph.oriented_count,
            old_oriented_radius_candidates=ref.oriented_count,occupied_cells=len(graph.counts),
            new_candidate_storage_bytes=sum(a.nbytes for a in (graph.particles,graph.starts,graph.cells,graph.counts,graph.neighbors,graph.adjacent_particle_counts,graph.weights,graph.cumulative)),
            mean_draw_seconds_cell=draws[0],mean_draw_seconds_previous_cell=draws[1],mean_draw_seconds_old=draws[2],generator_audit=audit,scatter_steps=[])
        for name,operator in (('native_cell',cell.scatter),('previous_cell',previous.scatter),('old_radius',old.scatter)):
            vv=v.copy();tick=time.perf_counter();report=operator(x,vv,m,cold,.5,h,np.random.default_rng(78308))
            check=invariants(x,v,vv,m)
            if max(check.values())>1.e-12:raise AssertionError('C22 global invariant gate failed')
            row['scatter_steps'].append(dict(method=name,seconds=time.perf_counter()-tick,report=report,**check))
        row['performance_goal_pass']=(new_build<.05 if synthetic else new_build<=old_build if 'prepared' in label else True)
        row['performance_goal_scope']='Syntheticdenseproxy construction<.05s or actualdiffuseprepared notslowerthanold; noisolatedhardware guarantee'
        result['rows'].append(row);result['wall_seconds']=time.monotonic()-start
        result['peak_RSS_bytes']=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        Path(output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
        result['all_performance_goals_pass']=all(r['performance_goal_pass'] for r in result['rows'])
        Path(output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
        print(json.dumps({k:row[k] for k in ('case','new_build_seconds','old_degree_build_seconds','build_speedup_old_over_new','new_oriented_candidates','old_oriented_radius_candidates')}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
