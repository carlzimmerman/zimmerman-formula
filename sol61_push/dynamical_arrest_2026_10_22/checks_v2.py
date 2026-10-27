import ast,argparse,json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp,solve_bvp,quad
from scipy.optimize import brentq
from scipy.special import roots_legendre
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);a=pa.parse_args()
p=Path('sol61_push/dynamical_arrest_2026_10_22');old=Path('sol61_push/core_formation_transport_2026_10_22/run/result.json');en=json.loads(old.read_text());r=en['canonical'];checks=[]
def ck(n,b,v):
 checks.append(dict(name=n,passed=bool(b),value=str(v)));print(n,b,v,flush=True)
U,V,Z,J,T,B,D,H,C=sp.symbols('U V Z J T B D H C');E=U+V+Z+J+T+B+C;muM=2*U+2*V+D+2*T-C
us=-3*V+3*Z+J-3*T-2*D+3*B-2*C
expr=sp.expand((muM-E).subs(U,us).subs(V,2*J+2*Z+H/2))
ck('fixed_L_mass_identity',sp.expand(expr-(-4*J-2*Z-H-2*T+2*B-D-4*C))==0,expr)
y,q,d=sp.symbols('y q d',positive=True);f=(1-y)*(y+q)**2
ck('driven_fold',sp.simplify(sp.diff(f,y)-(q+y)*(-q-3*y+2))==0,sp.factor(sp.diff(f,y)))
ck('reciprocal_curvature',sp.simplify(1-2*f/(y+q)**3-(3*y+q-2)/(y+q))==0,'Schur curvature')
tree=ast.parse(Path('sol61_push/compact_surplus_2026_10_22/checks.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['interior','exterior']],type_ignores=[]),'inherited_profile','exec'))
ins,_=interior(r['sc'],0,0,1e-11);R=r['R'];ex=exterior(R,ins.sol(R)[0]/R**2,0,35,1e-8) if False else None
def iw(x):
 Q,s=ins.sol(x);z=Q/x**2;yy=(z+np.sqrt(z*z+4*z))/2;return yy/(1+yy),x*x*yy
ex=exterior(R,iw(R)[0],0,35,2e-8)
I=2/3*(R*R*r['m']-2*quad(lambda x:x*iw(x)[1],1e-10,R,epsabs=1e-11)[0]);kap=I/(r['m']*R*R)
rot=[]
for order in [160,320]:
 gx,gw=roots_legendre(order);xs=[];weights=[];ws=[]
 for lo,hi,outer in [(0,R,False),(R,R+1,True),(R+1,R+5,True),(R+5,R+35,True)]:
  xx=lo+(gx+1)*(hi-lo)/2;ww=gw*(hi-lo)/2
  xs.extend(xx);weights.extend(ww*xx**2);ws.extend(ex.sol(xx)[1] if outer else iw(xx)[0])
 weights=np.array(weights);ws=np.array(ws)
 def pot(t):
  z=t*t*ws;return np.dot(weights,-z-np.log1p(-z))/t**3
 def dp(t):
  z=t*t*ws;return np.dot(weights,2*z*z/(1-z)-3*(-z-np.log1p(-z)))/t**4
 for frac in [0,.01,.05,.1,.2,.4]:
  c=frac*abs(r['U']);df=lambda t:r['U']+3*t*t*r['V']+dp(t)+2*t*c
  t=brentq(df,.05,1.02,xtol=1e-13)
  energy=t*r['U']+t**3*r['V']+pot(t)+t*t*c
  # beta correction of translating polarization scales as t^3 for fixed mass.
  rot.append(dict(order=order,rot_fraction_initial=frac,t=t,edge_pc=R/t*440.4221297174536,E=energy,I=I/t**2,kappa=kap,omega_dimensionless=np.sqrt(2*c/I)*t*t,v_edge_kms=np.sqrt(2*c/I)*t*R*np.sqrt(9.3603e-11*440.4221297174536*3.085677581491367e16)/1000))
ck('zero_spin_profile',abs(rot[6]['t']-1)<1e-6,rot[6])
ck('quadrature_repeat',max(abs(rot[i]['t']/rot[i+6]['t']-1) for i in range(6))<2e-6,'160 versus 320 nodes')
ck('rotational_expansion',all(rot[i+1]['t']<rot[i]['t'] for i in range(6,11)),[z['t'] for z in rot[6:]])
ck('inertia_bounds',0<kap<2/3,kap)
driven=[]
for qq in [.01,.1,1,3]:
 for yy in [.9,.7,.5]:
  dd=(1-yy)*(yy+qq)**2;p0=np.sqrt(2*dd/qq);xx=np.sqrt(qq)*p0/(yy+qq)
  Hess=np.array([[1,xx],[xx,yy+qq]])
  eig=np.linalg.eigvalsh(Hess);stable=3*yy+qq>2
  ck('hessian_%g_%g'%(qq,yy),bool(min(eig)>0)==stable,eig)
  driven.append(dict(q=qq,y=yy,d=dd,stable=stable,velocity_ratio=yy/(yy+qq),min_hessian=float(min(eig))))
trajectories=[]
for qq,yy in [(.01,.9),(.1,.7),(3,.5)]:
 dd=(1-yy)*(yy+qq)**2;p0=np.sqrt(2*dd/qq);xx=np.sqrt(qq)*p0/(yy+qq)
 def rhs(t,Y):
  y,yd,x,xd=Y;return [yd,-(y-1)-x*x/2,xd,-(y+qq)*x+np.sqrt(qq)*p0]
 sol=solve_ivp(rhs,(0,100),[yy+.005,0,xx,0],t_eval=np.linspace(0,100,2001),method='DOP853',rtol=1e-11,atol=1e-13);assert sol.success
 sy,yd,sx,xd=sol.y;ee=.5*(yd**2+xd**2)+.5*(sy-1)**2+.5*sy*sx**2+.5*(p0-np.sqrt(qq)*sx)**2
 err=np.max(abs(ee-ee[0]))/ee[0];ck('conservative_drive_%g'%qq,err<1e-8 and min(sy)>0,err)
 trajectories.append(dict(q=qq,y=yy,energy_error=float(err),late_peak_to_peak=float(np.ptp(sy[1000:])),time=sol.t[::20].tolist(),chi=sy[::20].tolist()))
growth=[];fb=1/6.364;fc=1-fb;N0=-np.log(1101);ai=np.exp(N0)
for yy in [1,.95,.8,2/3,.5]:
 for k in [.1,1]:
  def rhs(N,Y):
   b,bp,c,cp=Y;S=1/(1+(k*.0004404221297174536/np.exp(N))**2/yy);return[bp,-.5*bp+1.5*(fb*b+fc*c),cp,-.5*cp+1.5*(fb*b+fc*S*c)]
  so=solve_ivp(rhs,(N0,0),[ai]*4,method='DOP853',rtol=1e-10,atol=1e-15);assert so.success
  growth.append(dict(y=yy,k=k,amplitude=float(fb*so.y[0,-1]+fc*so.y[2,-1])))
ck('growth_monotone_chi',all(growth[i+2]['amplitude']<growth[i]['amplitude'] for i in range(8)),growth)
ck('growth_baseline',abs(growth[1]['amplitude']-.955654)<2e-6,growth[:2])
rotation_limits=[dict(n=n,speed_tolerance=e,max_f=((1-e)**-2-1)/n) for n in [1,2,3] for e in [.02,.05,.1]]
result=dict(checks=checks,rotation=rot[6:],driven=driven,trajectories=trajectories,growth=growth,rotation_limits=rotation_limits)
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0 if all(z['passed'] for z in checks) else 1)
