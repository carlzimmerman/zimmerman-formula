import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args();root=Path(__file__).parent
names=['base','space','time','strong','strong_space','strong_fine','strong_time','early','earlier'];runs={n:json.loads((root/n/'result.json').read_text()) for n in names};last={n:r['rows'][-1] for n,r in runs.items()}
ratio=lambda a,b,key:abs(last[a][key]/last[b][key]-1)
gates=[dict(name='weak_spatial_peak_5pct',passed=ratio('space','base','contrast_c_max')<.05,value=ratio('space','base','contrast_c_max')),dict(name='strong_spatial_peak_5pct',passed=ratio('strong_fine','strong_space','contrast_c_max')<.05,value=ratio('strong_fine','strong_space','contrast_c_max')),dict(name='strong_time_peak_1pct',passed=ratio('strong_time','strong','contrast_c_max')<.01,value=ratio('strong_time','strong','contrast_c_max')),dict(name='start_epoch_stability_10pct',passed=ratio('earlier','early','contrast_c_max')<.1,value=ratio('earlier','early','contrast_c_max')),dict(name='four_cells_per_core_radius',passed=last['strong_fine']['core_radius_cells']>=4,value=last['strong_fine']['core_radius_cells']),dict(name='bound_core_certificate',passed=False,reason='No candidate and inadequate physical resolution; no binding mass partition established'),dict(name='joint_observational_preservation',passed=False,reason='No predicted population; previous growth diagnostic still lacks a pass')]
L=runs['strong_fine']['parameters']['Lcom_Mpc']*1000/(1+10);nmin=4*L/.3214846542759978
out=dict(gates=gates,final=last,required_cells_per_axis_at_z10=nmin,max_work_error=max(r['max_work_error'] for r in runs.values()),no_candidates_all_saved=all(x['groups_ge32']==0 for r in runs.values() for x in r['rows']))
Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
