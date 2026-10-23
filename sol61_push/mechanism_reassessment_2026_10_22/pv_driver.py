import sys,json,subprocess
from pathlib import Path
p=Path(__file__).parent;result=Path(sys.argv[1]);root=result.parent
subprocess.run([sys.executable,str(p/'principal_value.py'),str(root/'pv.json'),'10'],check=True,stdout=subprocess.DEVNULL)
subprocess.run([sys.executable,str(p/'complex_mode_diagnostic.py'),str(root/'complex.json'),str(root/'pv.json')],check=True,stdout=subprocess.DEVNULL)
a=json.load(open(root/'pv.json'));b=json.load(open(root/'complex.json'));checks=dict(a['checks']);checks['dissipative_identity']=all(abs(q['imag']-q['projected_absorption'])<1e-9 for r in b['rows'] for q in r['points'])
out=dict(checks=checks,all_pass=all(checks.values()),principal_value=a,complex_diagnostic=b,scope='principal-value calculation and basis-sensitive real-axis mode diagnostic; no physical lifetime claim')
result.write_text(json.dumps(out,indent=2));print(json.dumps(dict(checks=checks,diagnostics=[{k:v for k,v in r.items() if k!='points'} for r in b['rows']]),indent=2));sys.exit(0 if out['all_pass'] else 1)
