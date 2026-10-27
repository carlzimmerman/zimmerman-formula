import sympy as s,json,sys,ast,math,hashlib
import numpy as np
from scipy import optimize
from pathlib import Path
base=Path('sol61_push/framework_certification_2026_10_12/nonspherical_admission')
G,M,a=s.symbols('G M a',positive=True);x,y,z=s.symbols('x y z',real=True)
coords=[x,y,z]
potentials=[-G*M/s.sqrt((x-sign*a)**2+y*y+z*z) for sign in [1,-1]]
phi=sum(potentials);g=s.Matrix([s.diff(phi,q) for q in coords]);H=g.jacobian(coords)
checks=[]
def eq(name,expr):
 expr=s.simplify(expr);checks.append({'name':name,'passed':expr==0,'residual':str(expr)})
def test(name,result,evidence=None):checks.append({'name':name,'passed':bool(result),'evidence':evidence})
for i,p in enumerate(potentials):eq('actual source vacuum Laplacian '+str(i),sum(s.diff(p,q,2) for q in coords))
for i in range(3):
 for j in range(i):eq('actual potential curl '+str(i)+str(j),H[i,j]-H[j,i])
p0={x:0,y:a/4,z:0}
g0=s.simplify(g.subs(p0));H0=s.simplify(H.subs(p0))
gy=32*G*M/(17*s.sqrt(17)*a*a);slope=1792*G*M/(289*s.sqrt(17)*a**3)
eq('midpoint actual g_y',g0[1]-gy)
eq('midpoint actual slope',H0[1,1]-slope)
eq('midpoint g_x',g0[0]);eq('midpoint g_z',g0[2])
eq('midpoint Hessian trace',s.trace(H0))
test('midpoint positive field',gy.is_positive)
test('midpoint positive slope',slope.is_positive)
gradnorm0=s.simplify(H0*g0/gy)
eq('midpoint geometric directional factor',g0.dot(gradnorm0)-gy*slope)
for i in [0,2]:eq('midpoint gradient norm alignment '+str(i),gradnorm0[i])
Y=s.symbols('Y',positive=True);nu=1/(1-s.exp(-s.sqrt(Y)));nup=s.diff(nu,Y)
eq('own lowbranch derivative',nup+s.exp(-s.sqrt(Y))/(2*s.sqrt(Y)*(1-s.exp(-s.sqrt(Y)))**2))
eq('own derivative at1',nup.subs(Y,1)+s.E/(2*(s.E-1)**2))
nup1=-s.E/(2*(s.E-1)**2)
test('own derivative1 strict negative',nup1.is_negative)
rhoph=nup1*slope/(4*s.pi*G)
eq('exact target normalized',rhoph*4*s.pi*a**3/M+896*s.E/(289*s.sqrt(17)*(s.E-1)**2))
test('exact target strict negative',rhoph.is_negative)
# Offsymmetry fixed point, no host external field. Normalization G=M=a=1.
p1={x:s.Rational(1,8),y:s.Rational(1,4),z:0,a:1,G:1,M:1}
g1=s.simplify(g.subs(p1));H1=s.simplify(H.subs(p1));n1=s.sqrt(s.simplify(g1.dot(g1)))
cross=s.simplify((H1*g1).cross(g1)[2]/n1)
eq('offsymmetry vacuum trace',s.trace(H1))
test('offsymmetry cross exact nonzero',cross.equals(0) is False,str(cross))
a0num=gy.subs({G:1,M:1,a:1});Y1=s.simplify(n1/a0num)
test('offsymmetry inside lowbranch',bool(Y1.evalf(40)>1 and Y1.evalf(40)<2),str(Y1.evalf(30)))
curl=s.diff(nu,Y).subs(Y,Y1)*cross/a0num
test('literal vectorboost curl nonzero',abs(float(curl.evalf(30)))>s.Rational(1,10000),str(curl.evalf(30)))
# Compactsource spherical control: exteriorg=GM/r² ->d_r g<0,
# grad(nu).g gives positive density for negative nuprime.
r=s.symbols('r',positive=True)
sphereG=G*M/(r*r)
eq('spherical extra divergence product rule',s.diff(r*r*(nu.subs(Y,sphereG/a0num)-1)*sphereG,r)/(r*r)-sphereG*s.diff(nu.subs(Y,sphereG/a0num),r))
# At ykernel1 substitute formalnuprime, use exactradialg'/negative.
sphereRho=nup1*(-2*G*M/r**3)/(4*s.pi*G)
test('spherical nonnegative control',sphereRho.is_positive)
test('clipping differs from exact negative target',rhoph.is_negative and s.Max(rhoph,0)==0)
cold=s.symbols('cold',nonnegative=True)
eq('deficit zero at negative target',s.Max(rhoph-cold,0))
# Only sourcekernel nodes; no cosmology or main program import.
def load_nodes(path,defnames,assignnames):
 raw=Path(path).read_text();tree=ast.parse(raw);nodes=[]
 for node in tree.body:
  if isinstance(node,ast.FunctionDef) and node.name in defnames:nodes.append(node)
  elif isinstance(node,ast.Assign):
   names={t.id for t in node.targets if isinstance(t,ast.Name)}
   if names and names<=assignnames:nodes.append(node)
 module=ast.Module(body=nodes,type_ignores=[])
 ns={'np':np,'math':math,'brentq':optimize.brentq,'optimize':optimize}
 exec(compile(module,str(path),'exec'),ns)
 return ns,hashlib.sha256(ast.unparse(module).encode()).hexdigest()
FP=base/'inputs/real_research/derivation_chain_2026/FP1_static_sector.py'
fp,hfp=load_nodes(FP,{'_h_rar','_dh_rar','nu_mono'},{'Y_P','H_P','LYG','_YG','_DH','_HM'})
PM=base/'inputs/campaign_fresh_gravity/CFG650_theory_v2_combined_pm/cfg650_pm.py'
pm,hpm=load_nodes(PM,{'h_rar','dh_rar','nu_mono'},{'Y_P','H_P','DELTA','LYG','YG','DH_MONO','H_MONO'})
CONT=base/'inputs/campaign_fresh_gravity/CFG233_rc100_referee/CFG233_common.py'
cont,hcont=load_nodes(CONT,{'_h_rar','_dh','nu_mono'},{'_YP','_HP','_DELTA','_YS'})
expected=float(nu.subs(Y,1).evalf(30));dex=float(nup1.evalf(30));table={}
for name,ns,hcode,key in [('FP1',fp,hfp,'_HM'),('CFG650',pm,hpm,'H_MONO')]:
 yy=ns['LYG'];hh=ns[key];i=int(np.argmin(abs(yy)));val=float(ns['nu_mono'](1))
 sl=[float((hh[i]-hh[i-1])/(yy[i]-yy[i-1])/math.log(10)-hh[i]),float((hh[i+1]-hh[i])/(yy[i+1]-yy[i])/math.log(10)-hh[i])]
 test(name+' gridnode1',abs(float(yy[i]))<1e-12)
 test(name+' value tolerance',abs(val-expected)<1e-6,val)
 for q,dv in enumerate(sl):
  test(name+' both one-sided slopes negative '+str(q),-.47<dv<-.45,dv)
  test(name+' derivative fidelity '+str(q),abs(dv-dex)<2e-4,dv)
 table[name]={'value':val,'slopes':sl,'isolated_ast_sha256':hcode}
test('continuous ownsplice1 below switch',float(cont['_YS'])>1,float(cont['_YS']))
test('continuous ownkernel1',abs(float(cont['nu_mono'](1))-expected)<1e-12)
result={'claim':'bounded ownkernel nonspherical admission','count':len(checks),'checks':checks,'all_passed':all(c['passed'] for c in checks),'exact_mid':{'g':str(gy),'slope':str(slope),'nuprime1':str(nup1),'rhoph':str(rhoph),'rhoph_units_GMa1':str(rhoph.subs({G:1,M:1,a:1}).evalf(30))},'offaxis':{'Y':str(Y1.evalf(30)),'geometriccross':str(cross),'vectorcurl':str(curl.evalf(30))},'kernel':{'tables':table,'continuous_splice':float(cont['_YS']),'continuous_ast_sha256':hcont},'scope':'signed literal target/vector diagnostics; round/clip/field existing alternativeinterpretations, no wholeframeworkrefutation'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'count':len(checks),'all_passed':result['all_passed']}));sys.exit(0 if result['all_passed'] else 1)
