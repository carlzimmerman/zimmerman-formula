#!/usr/bin/env python3
"""Bounded source/statistical audit of committed L191; no parameter scan."""
import argparse, hashlib, json, math, subprocess, time
from pathlib import Path
import numpy as np

REV='9b97161a6'
FILES=['fable_independent_2026/L191_c003_orbit_integration.py',
       'fable_independent_2026/L191_results.json',
       'fable_independent_2026/L190_c003_radial_kids_and_cluster_shape.py']


def source_audit():
    texts={p:subprocess.check_output(['git','show',REV+':'+p]) for p in FILES}
    sources={p:dict(revision=REV,sha256=hashlib.sha256(v).hexdigest(),
                    current_file_matches=Path(p).read_bytes()==v) for p,v in texts.items()}
    assert all(s['current_file_matches'] for s in sources.values())
    j=json.loads(texts[FILES[1]])
    rows=[]
    for name,row in j['res'].items():
        rows.append(dict(selection=name,**row,spiral_strict_pass=row['f'][0]<=.105,
                         spiral_relaxed_pass=row['f'][0]<=.105*1.35))
    assert all(not r['spiral_strict_pass'] for r in rows)
    return dict(sources=sources,selections=rows,
      same_absorbing_pair_both_footings=j['res']['absorb|canonical']['vk']==j['res']['absorb|alt']['vk'],
      canonical_boundary_comparison_holds_vk_fixed=j['res']['absorb|canonical']['vk']==j['res']['free|canonical']['vk'],
      original_spiral_ceiling=.105,relaxed_spiral_ceiling=.105*1.35,
      original_parameters=dict(vk=650.,n=2.3077948724637416),
      new_parameters=dict(canonical_vk=700.,alt_vk=1000.,n=2.),
      n2_zero_count_probability=math.exp(-2),
      n2_floor_excess_above_original_ceiling=math.exp(-2)-.105,
      equality_condition='All particles with at least one kick contribute zero mass to the chosen final observable.',
      source_estimator='End-time annulus 0.3<=r/ra<1; independent initial/control seeds, not enclosed mass.',
      source_initial_condition='Spatially truncated isothermal DF is not stationary under free Hamiltonian flow or absorbing boundary.',
      L190_latest_KiDS_convention='One-halo mass within R200, not the earlier 100-300kpc shell; observational adequacy not authenticated here.')


def acc(x):
    return -x/np.maximum(np.sum(x*x,axis=-1),1e-12)[...,None]


def ic(n,seed):
    rng=np.random.default_rng(seed)
    r=np.exp(rng.uniform(np.log(.3),np.log(1.53),n))
    d=rng.normal(size=(n,3));d/=np.linalg.norm(d,axis=1)[:,None]
    return r[:,None]*d,rng.normal(scale=1/np.sqrt(2),size=(n,3)),r/r.sum()


def benchmark(n=8192):
    begin=time.time()
    # Exactly the two reported absorbing best choices, not a scan or joint pair.
    feet=[('canonical',9.3619e-11,700.),('alt',1.1279e-10,1000.)]
    rows=[(f,a,v,absorb,pop) for f,a,v in feet for absorb in [False,True]
          for pop in ['kicked','paired_control','independent_control']]
    original_x,original_v,w=ic(n,882103)
    independent_x,independent_v,iw=ic(n,991047)
    x=np.array([independent_x if r[4]=='independent_control' else original_x for r in rows])
    v=np.array([independent_v if r[4]=='independent_control' else original_v for r in rows])
    weights=np.array([iw if r[4]=='independent_control' else w for r in rows])
    init_r=np.linalg.norm(x,axis=-1)
    initial_energy=.5*np.sum(v*v,axis=-1)+np.log(init_r)
    vf=np.array([(4.301e-9*(r[1]*3.086e22/1e6)*1.4e14)**.25 for r in rows])
    Tc=10*vf/(1.38*978.)
    steps=int(np.ceil(Tc.max()/.003));h=Tc/steps
    # Poisson count independent of initial conditions; common events in both boundaries/footings.
    rng=np.random.default_rng(771023)
    count=rng.poisson(2.,n);ids=np.repeat(np.arange(n),count)
    times=rng.uniform(size=len(ids));dirs=rng.normal(size=(len(ids),3));dirs/=np.linalg.norm(dirs,axis=1)[:,None]
    order=np.argsort(times);times=times[order];ids=ids[order];dirs=dirs[order]
    kick_rows=np.array([i for i,r in enumerate(rows) if r[4]=='kicked'])
    us=np.array([r[2] for r in rows])/vf
    absorbing=np.array([r[3] for r in rows])
    alive=np.ones((len(rows),n),dtype=bool)
    a=acc(x);cursor=0;coalesced=0
    for s in range(steps):
        v+=.5*h[:,None,None]*a;x+=h[:,None,None]*v;a=acc(x);v+=.5*h[:,None,None]*a
        stop=np.searchsorted(times,(s+1)/steps,side='right')
        if stop>cursor:
            coalesced+=(stop-cursor)-len(np.unique(ids[cursor:stop]))
            for k in range(cursor,stop):
                v[kick_rows,ids[k]]+=us[kick_rows,None]*dirs[k]
        cursor=stop
        gone=(np.sum(x*x,axis=-1)>1.53**2)&absorbing[:,None]
        alive[gone]=False
        x[gone]=15.3;v[gone]=0;a=acc(x)
    radius=np.linalg.norm(x,axis=-1)
    observables={'annulus':(radius>=.3)&(radius<1), 'enclosed_anchor':radius<1,
                 'enclosed_R200':radius<1.53}
    start_observables={'annulus':(init_r>=.3)&(init_r<1),'enclosed_anchor':init_r<1,
                       'enclosed_R200':init_r<1.53}
    results=[]
    for k in kick_rows:
        for name,region in observables.items():
            kval=weights[k]*alive[k]*region[k]
            cval=weights[k+1]*alive[k+1]*region[k+1]
            ival=weights[k+2]*alive[k+2]*region[k+2]
            ratio=kval.sum()/cval.sum()
            # Delta-method particle SE; paired control covariance retained.
            paired_se=np.sqrt(n*np.var(kval-ratio*cval,ddof=1))/cval.sum()
            independent_ratio=kval.sum()/ival.sum()
            independent_se=np.sqrt(n*np.var(kval,ddof=1)+independent_ratio**2*n*np.var(ival,ddof=1))/ival.sum()
            zero=kval*(count==0)
            zero_ratio=zero.sum()/cval.sum()
            check_zero=np.max(np.abs(kval[count==0]-cval[count==0]))
            assert check_zero < 1e-14
            initial_control=np.sum(weights[k+1]*start_observables[name][k+1])
            results.append(dict(footing=rows[k][0],vk=rows[k][2],n=2.,boundary='absorb' if rows[k][3] else 'free',
                observable=name,paired_retention=float(ratio),paired_particle_se=float(paired_se),
                independent_control_retention=float(independent_ratio),independent_control_particle_se=float(independent_se),
                zero_kick_contribution=float(zero_ratio),positive_kick_contribution=float(ratio-zero_ratio),
                no_kick_identity_max_error=float(check_zero),
                control_end_over_initial_mass=float(cval.sum()/initial_control),
                matched_zero_count_floor=bool(ratio>=zero_ratio-1e-14)))
    control_energy=[]
    en=.5*np.sum(v*v,axis=-1)+np.log(radius)
    for i,r in enumerate(rows):
        if not r[3] and r[4]!='kicked':
            drift=np.abs(en[i]-initial_energy[i])/np.maximum(1,np.abs(initial_energy[i]))
            control_energy.append(dict(footing=r[0],population=r[4],p99=float(np.quantile(drift,.99)),max=float(drift.max())))
    return dict(n_per_population=n,particle_population_count=len(rows),steps=steps,
      max_dimensionless_dt=float(h.max()),runtime_seconds=time.time()-begin,
      seeds=dict(initial=882103,independent_control=991047,counts_events=771023),
      mean_count=float(count.mean()),zero_count_fraction=float(np.mean(count==0)),
      coalesced_extra_events_if_L191_step_approximation_used=coalesced,
      controls_energy=control_energy,results=results,
      limits='One finite cluster benchmark, fixed log potential, exact vector events, source spatial IC cutoff, no timestep or particle-count convergence; errors are approximate sampling errors only.')


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    result=dict(source=source_audit(),benchmark=benchmark())
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
