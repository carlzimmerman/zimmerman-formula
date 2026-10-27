import sympy as s,json,sys
from pathlib import Path
A,B,k,z,mu2,b=s.symbols('A B k z mu2 b',real=True)
f=(k*k+mu2-z)*(B*k*k-A*z)-b*b*z
checks=[]
for name,x in [('boundary factorization',f.subs(B,0)-z*(A*z-A*(k*k+mu2)-b*b)),('zero frequency every k',f.subs({B:0,z:0})),('gapped boundary root',f.subs(B,0).subs(z,k*k+mu2+b*b/A))]:
 checks.append({'name':name,'passed':s.factor(x)==0,'residual':str(s.factor(x))})
r={'checks':checks,'count':len(checks),'all_passed':all(c['passed'] for c in checks),'scope':'spatially degenerate zero branch, not transport health'}
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'count':r['count'],'all_passed':r['all_passed']}));sys.exit(0 if r['all_passed'] else 1)
