import argparse,json
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();p=Path(__file__).parent
runs={k:json.loads((p/k/'result.json').read_text())for k in ['r511','r511_half','r1023_a']}
rows={k:min(d['records'],key=lambda x:abs(x['time']-1.4))for k,d in runs.items()}
errors={}
for label,key in [('time','r511_half'),('space','r1023_a')]:
 errors[label]={field:abs(rows['r511'][field]-rows[key][field])/max(abs(rows[key][field]),1e-100)for field in ['q_min','q_max','q_gradient']}
checks={'shared_time':all(abs(x['time']-1.4)<1e-10 for x in rows.values()),'time_gradient':errors['time']['q_gradient']<1e-3,'space_gradient':errors['space']['q_gradient']<1e-2,'charge_extrema':all(errors[z][f]<1e-5 for z in errors for f in ['q_min','q_max'])}
result=dict(all_pass=all(checks.values()),checks=checks,rows=rows,relative_errors=errors,non_claims=['Endpoint diagnostics only, not a norm of complete fields','No converged singularity time','Fine run inherits valid earlier n1023 checkpoint'])
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'all_pass':result['all_pass'],'relative_errors':errors}));raise SystemExit(0 if result['all_pass']else 1)
