import sympy as s,json,sys
from pathlib import Path
DEST=Path(sys.argv[1]);M,eps,g,lr=s.symbols('M epsilon g lambda_rep',positive=True);D=M*M*eps*eps;lt=lr+g*g/D;Gamma=g*g*eps/(8*s.pi*M);bound=lt*eps**3/(8*s.pi);gap=s.factor(bound-Gamma/M)
checks=[]
def z(n,e):
 r=s.simplify(e);checks.append({'name':n,'passed':r==0,'residual':str(r)})
def y(n,c):checks.append({'name':n,'passed':bool(c),'condition':str(c)})
z('width normalization from p=M epsilon/2',g*g*(M*eps/2)/(4*s.pi*M*M)-Gamma)
z('exact coldness rate margin',gap-lr*eps**3/(8*s.pi));y('margin nonnegative from positive repulsion',gap.is_nonnegative)
z('relative stable-action width bound',s.simplify((Gamma/M)/bound)-g*g/(g*g+lr*D))
z('lifetime floor difference',M/Gamma-8*s.pi/(lt*eps**3)-8*s.pi*lr*M**4*eps/(g*g*(g*g+lr*D)))
y('lifetime floor residual positive',s.simplify(M/Gamma-8*s.pi/(lt*eps**3)).is_nonnegative)
z('repulsion-free saturation',gap.subs(lr,0))
# Bound at fixed lambda_tot is cubic, not a bound on absolute M.
L=s.symbols('lambda_total',positive=True)
z('cubic coldness suppression',s.diff(L*eps**3/(8*s.pi),eps,3)-3*L/(4*s.pi))
out={'checks':checks,'all_passed':all(c['passed'] for c in checks),'formulas':{'epsilon':'sqrt(Delta)/M=2p/M, M²=4m²+Delta','Gamma':str(Gamma),'rate_bound':'Gamma/M <= lambda_tot epsilon³/(8pi)','exact_margin':str(gap),'lifetime_floor':'M*tau >= 8pi/(lambda_tot epsilon³)','coupling_fraction':str(s.simplify((Gamma/M)/bound))},'physical_width_assumptions':['canonical perturbative quantization','Bose daughter asymptotic states','vacuum on-shell tree amplitude2g','identical-state factor1/2','Golden Rule/invariant phase space','weak dilute regime; medium/coherent/loop corrections excluded'],'scope':'Exact algebraic consequence of stability parameters and stipulated perturbative width. No mass/rate/epoch universally excluded.'};(DEST/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['all_passed']
