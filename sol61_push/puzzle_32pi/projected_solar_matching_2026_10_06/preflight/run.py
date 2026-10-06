import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from solver import solve
r=solve(nr=100,nt=48,maxiter=120,wall=35)
p=Path(__file__).with_name('results_a.json');p.write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if k!='history'}))
