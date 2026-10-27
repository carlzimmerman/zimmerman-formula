import argparse,ast,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,solve_bvp,quad
from scipy.optimize import brentq
import sympy as sp
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);pa.add_argument('--omit-exterior',action='store_true');a=pa.parse_args();prev=Path('sol61_push/compact_surplus_2026_10_22');tree=ast.parse((prev/'checks.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['interior','exterior','one']],type_ignores=[]),str(prev/'checks.py'),'exec'))
checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=str(v)));print(n,b,v,flush=True)
U,V,Z,J,T,B,D,H=sp.symbols('U V Z J T B D H');E=U+V+Z+J+T+B;muM=2*U+2*V+D+2*T
ustar=-3*V+3*Z+J-3*T-2*D+3*B
ck('chemical_minus_energy',sp.expand((muM-E).subs(U,ustar)-(-2*V+2*Z-2*T+2*B-D))==0,'muM-E=-2V+2Z-2T+2B-D')
ck('passive_sign_reduction',sp.expand((muM-E).subs(U,ustar).subs(V,2*J+2*Z+H/2)-(-4*J-2*Z-H-2*T+2*B-D))==0,'negative if D>2B')
w=sp.symbols('w',positive=True);pot=-w-sp.log(1-w)
ck('log_potential_sign',sp.simplify(sp.diff(2*pot-w*sp.diff(pot,w),w)+w*w/(1-w)**2)==0,'(2W-wWprime)prime=-w²/(1-w)²')
cache={}
def energy(sc,lam,tol=2e-7,offset=30):
 key=(float(sc),lam,tol,offset)
 if key in cache:return cache[key]
 row=one(sc,lam,0,tol,offset);R=row['R'];m=row['mass_c'];ins,_=interior(sc,lam,0,tol*.01);ex=exterior(R,row['w_edge'],lam,offset,tol)
 def vals(x,outer):
  if outer:s,w=ex.sol(x)
  else:
   Q,s=ins.sol(x);z=Q/x**2;y=(z+np.sqrt(z*z+4*z))/2;w=y/(1+y)
  W=-w-np.log1p(-w)
  return x*x*np.array([W,.5*s*s+.5*lam*s**4,.25*lam*s**4,w*w/(1-w)])
 def grav(x):
  Q,s=ins.sol(x);z=Q/x**2;y=(z+np.sqrt(z*z+4*z))/2;return x*x*y*y
 U=-.5*(quad(grav,1e-10,R,epsabs=1e-12,epsrel=2e-9)[0]+m*m/R)
 vv=np.array([quad(lambda x:vals(x,False)[i],1e-10,R,epsabs=1e-12,epsrel=2e-8)[0]+(0 if a.omit_exterior else quad(lambda x:vals(x,True)[i],R,R+offset,epsabs=1e-12,epsrel=2e-8)[0]) for i in range(4)])
 B,V,Z,D=vv;E=U+B+V+Z;vir=U+3*V-3*Z+2*D-3*B;chem=row['mu']*m-(2*U+2*V+D)
 result=dict(sc=float(sc),lam=lam,R=R,m=m,mu=row['mu'],U=U,B=B,V=V,Z=Z,D=D,E=E,E_per_mass=E/m,virial_error=float(abs(vir)/max(abs(U),1e-12)),chemical_error=float(abs(chem)/max(abs(U),1e-12)),muM_minus_E=row['mu']*m-E)
 cache[key]=result;return result
rows=[]
for lam in [0.,1.]:
 for sc in [.03,.1,.3,1.,3.,10.]:
  r=energy(sc,lam);rows.append(r);ck('equilibrium_%g_%g'%(lam,sc),max(r['virial_error'],r['chemical_error'])<2e-4 and r['E']<0 and r['muM_minus_E']<0,dict(m=r['m'],E=r['E'],vir=r['virial_error'],chem=r['chemical_error']))
sc=.14820358643718212;central=energy(sc,0);tight=energy(sc,0,2e-8,40)
ck('energy_cutoff_tolerance_repeat',abs(central['E']/tight['E']-1)<2e-5,abs(central['E']/tight['E']-1))
derivatives=[]
for step in [.001,.0002]:
 lo=energy(sc*(1-step),0);hi=energy(sc*(1+step),0);der=(hi['E']-lo['E'])/(hi['m']-lo['m']);derivatives.append(der)
ck('first_law_finite_difference',max(abs(v/central['mu']-1) for v in derivatives)<3e-4,dict(derivative=derivatives,mu=central['mu']))
sc2=brentq(lambda x:energy(x,0)['m']-2*central['m'],sc,1.,xtol=1e-8);double=energy(sc2,0);release=2*central['E']-double['E'];ck('equal_mass_merger_releases_binding_energy',release>0 and abs(double['m']/(2*central['m'])-1)<1e-6,release)
ell=.4404221297174536*3.085677581491367e19;a0=9.3603e-11;G=6.67430e-11;Msun=1.98847e30;Eunit=a0*a0*ell**3/G
out=dict(checks=checks,rows=rows,canonical=central,double_mass=double,merger_release_dimensionless=release,merger_release_J=release*Eunit,merger_release_per_initial_total_mass_kms2=release/(2*central['m'])*a0*ell/1e6,unit_energy_J=Eunit,omit_exterior=a.omit_exterior)
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
