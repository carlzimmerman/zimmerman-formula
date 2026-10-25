import json, math
from pathlib import Path
p=Path(__file__).resolve().parent
src=json.loads((p/'run/result.json').read_text())
qout=2*math.asin(1/math.sqrt(6))
def V(q,d):
    f=math.cos(q/2)**2
    y=4*math.sin(q/2)**2
    return (1+(y-1)**2)/f**2+d/math.sqrt(f)
rows=[]
for r in src['rows']:
    d=r['gas_d']
    excess=-.4+d*(math.sqrt(6/5)-1)
    assert abs(excess-(V(qout,d)-V(0,d)))<1e-11
    assert excess>0
    rows.append({k:r[k] for k in ['name','model','footing','shell']} | {
        'sudden_excess_over_D':excess,
        'sudden_over_required':excess/r['required_source_over_D']})
s=dict(cases=len(rows),energy_over_D_range=[min(r['sudden_excess_over_D'] for r in rows),max(r['sudden_excess_over_D'] for r in rows)],ratio_range=[min(r['sudden_over_required'] for r in rows),max(r['sudden_over_required'] for r in rows)],cases_at_least_requirement=sum(r['sudden_over_required']>=1 for r in rows))
(p/'sudden_result.json').write_text(json.dumps(dict(summary=s,rows=rows),indent=2)+'\n')
print(json.dumps(s,indent=2))
