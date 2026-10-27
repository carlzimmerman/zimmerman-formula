"""Summarize recorded evidence, preserving resource-inconclusive outcomes."""
import json
from pathlib import Path

p=Path(__file__).resolve().parent
out={'pilots':{},'implicit':{},'refinement':{},'bound':{}}
for name in ['pilot','diffuse','contraction','transport']:
    d=json.loads((p/f'run_{name}/results.json').read_text());rows=d['runs']
    completed=[r for r in rows if r['status']=='completed']
    high=[r for r in completed if r['f']==.95]
    out['pilots'][name]=dict(attempted=len(rows),completed=len(completed),
        inconclusive=sum(r['status']=='inconclusive' for r in rows),
        high_coherence_peak=max([r['peak_q'] for r in high],default=None),
        persistent_target_passes=sum(r['late_min_q']>=.95 for r in high),
        max_energy_error=max([r['max_energy_error'] for r in completed],default=None))
for name in ['stiff','stiff3','refinement','lsoda']:
    root=p/f'run_{name}'
    d=json.loads((root/'results.json').read_text());manifest=json.loads((root/'manifest.json').read_text())
    # Runner schema is intentionally read without assuming scientific success.
    h=d['history'];late=[r for r in h if r['t']>=9.6]
    row=dict(trajectory_status=d['status'],run_status=manifest['run']['status'],
        accepted_until=d.get('last_t',0),peak_q=d.get('peak_q'),
        late_min_q=min([r['q'] for r in late],default=None),
        final_q=h[-1]['q'],max_energy_error=d.get('max_energy_error'),
        max_J_error=d.get('max_J_error'))
    out['implicit' if name in ['stiff','stiff3'] else 'refinement'][name]=row
base=json.loads((p/'run_stiff/results.json').read_text())
for name in ['refinement','lsoda']:
    d=json.loads((p/f'run_{name}/results.json').read_text());end=d.get('last_t',0)
    bp=max(r['q'] for r in base['history'] if r['t']<=end+1e-8)
    out['refinement'][name]['same_window_peak_difference']=abs(d['peak_q']-bp)
    out['refinement'][name]['full_refinement_complete']=d['status']=='completed'
b=json.loads((p/'run_bound/results.json').read_text())
out['bound']=dict(checks=b['checks'],evaluations=b['runs'])
(p/'SUMMARY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='bound'},indent=2))
