"""Matched backend admission; descriptive800–1000Myr profiles, no core claim."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent

def summarize(times,values):
    values=np.asarray(values,float);duration=times[-1]-times[0]
    mean=np.trapz(values,times,axis=0)/duration
    std=np.sqrt(np.maximum(0,np.trapz((values-mean)**2,times,axis=0)/duration))
    return dict(mean=mean.tolist(),time_RMS=std.tolist(),minimum=values.min(axis=0).tolist(),maximum=values.max(axis=0).tolist())

def main(output):
    olddir=HERE/'run_pilot_gpu8k_iso';newdir=HERE/'run_tile2_admission8k_iso_dt05_1Gyr'
    old=json.loads((olddir/'results.json').read_text());new=json.loads((newdir/'results.json').read_text())
    keys=('ncold','seed','collision_seed','eps','h','dt','duration','record_interval','host','collisionless','collision_method')
    if any(old['args'][key]!=new['args'][key] for key in keys):raise ValueError('unmatched physical/integrator/RNG argument')
    with np.load(olddir/'initial.npz') as a,np.load(newdir/'initial.npz') as b:
        if any(not np.array_equal(a[k],b[k]) for k in ('x','v','m','cold')):raise ValueError('initial arrays differ')
        digest=hashlib.sha256(b['x'].tobytes()+b['v'].tobytes()+b['m'].tobytes()).hexdigest()
    if digest!=old['initial_conditions']['relative_state_sha256'] or digest!=new['initial_conditions']['relative_state_sha256']:raise ValueError('state digest mismatch')
    selected=[]
    for result in (old,new):
        rows=[r for r in result['snapshots'] if 800.<=r['time_Myr']<=1000.]
        times=np.array([r['time_Myr'] for r in rows]);selected.append((rows,times))
    if not np.array_equal(selected[0][1],selected[1][1]) or not np.array_equal(selected[0][1],np.arange(800.,1001.,10.)):raise ValueError('window grid mismatch')
    times=selected[0][1];a,b=(item[0] for item in selected)
    edges=np.array(a[0]['profile']['edges']);radius=np.array(a[0]['profile']['radius'])
    if any(not np.array_equal(row['profile']['edges'],edges) for row in a+b):raise ValueError('shell edges mismatch')
    summaries=[]
    for result,rows in ((old,a),(new,b)):
        summaries.append(dict(M100=summarize(times,[r['M100'] for r in rows]),M300=summarize(times,[r['M300'] for r in rows]),
            density=summarize(times,[r['profile']['density'] for r in rows]),
            cumulative_mass=summarize(times,[r['profile']['enclosed_mass_at_edges'] for r in rows]),
            collisions=result['collisions'],maxima=result['maxima'],runtime_seconds=result['runtime_seconds']))
    da,db=(np.array(s['density']['mean']) for s in summaries)
    delta=np.divide(db-da,da,out=np.full_like(da,np.nan),where=da!=0.)
    massdiff={k:summaries[1][k]['mean']/summaries[0][k]['mean']-1. for k in ('M100','M300')}
    gate_mask=(edges[:-1]>=250.)&(edges[1:]<=2000.)
    precision=json.loads((newdir/'precision_checks.json').read_text())['evolved_state_precision_checks']
    if not precision or any(p.get('passed') is not True for p in precision):raise ValueError('missing/failed same-state precision check')
    # These are bounded backend-admission gates, not finite-N physical convergence.
    gates=dict(energy=new['maxima']['E']<.001,
        momentum_angular_momentum=max(new['maxima']['P'],new['maxima']['Jtotal'])<1.e-8,
        all_scheduled_CPU_DS_checks_pass=all(p['passed'] for p in precision),
        late_M300_within10percent=abs(massdiff['M300'])<.1,
        late_density250to2000pc_within10percent=bool(np.all(abs(delta[gate_mask])<.1)))
    record=dict(initial_relative_state_sha256=digest,matched_arguments={k:old['args'][k] for k in keys},
        window_Myr=[800.,1000.],snapshot_count=len(times),averaging='Trapezoidal time averages; timeRMS is correlated variation, not an uncertainty on the mean',
        reference=summaries[0],tile2=summaries[1],M_relative_change=massdiff,
        edges_pc=edges.tolist(),radius_pc=radius.tolist(),late_density_relative_change=[float(z) if np.isfinite(z) else None for z in delta],
        undefined_density_relative_change_reason='Reference time-mean density is zero',
        density_admission_interval_pc=[250.,2000.],density_admission_mask=gate_mask.tolist(),
        precision_comparisons=len(precision),maximum_same_state_force_L2=max(p['force_relative_L2'] for p in precision),
        maximum_same_state_force_max=max(p['force_relative_max'] for p in precision),
        gates=gates,all_declared_admission_gates_pass=all(gates.values()),
        nonclaims=['One matched finite8k1Gyr backend check is not density/core/host-remnant convergence',
            '250to2000pc agreement does not admit an unresolved innercore or later10Gyr evolution',
            'Identical CTMC seed is not a shared-event coupling after phase trajectories diverge',
            'Snapshot timeRMS is not independent sampling uncertainty; all radii retained in output'])
    Path(output).write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(gates=gates,M_relative_change=massdiff,max_density_change250to2000=float(np.max(abs(delta[gate_mask]))),events=[old['collisions'],new['collisions']])) ,flush=True)
    if not all(gates.values()):raise AssertionError('Declared bounded tile2 admission gate failed')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
