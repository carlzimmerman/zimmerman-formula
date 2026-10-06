import sys,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from solver import solve
cases=[(160,80,.005,20),(240,128,.0025,40),(320,160,.00125,40),(360,160,.00125,80),(240,128,.0025,40),(100,48,.005,20)]
rows=[]
for i,(nr,nt,ri,ro) in enumerate(cases):
 r=solve(nr=nr,nt=nt,rmin=ri,rmax=ro,tol=1e-10 if i!=4 else 1e-12,linear=i==5,wall=35);rows.append(r);Path(__file__).with_name('scan_a.json').write_text(json.dumps(rows,indent=2));print(i,r['Q2_visible_SI'],r['fits'],r['elapsed'],flush=True)
