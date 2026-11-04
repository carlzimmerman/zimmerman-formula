"""TH07: positive physical SU5 spectrum and equilibrium one-loop thermal gas.
No installed-package mutation; no bytecode writes outside authorized scope.
"""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
import mpmath as mp
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq,root
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];E=.003;G=math.sqrt(29/200)*E;Z=7.367143721278508;XOLD=Z/math.sqrt(31*E);A0=math.sqrt(2/(31*E))
mp.mp.dps=65

def blocks(X):
 a=A0;b=X;c=E/31;out=[]
 for name,r,mult in [('SU3',2.,8),('SU2',-3.,3),('broken',-.5,12)]:
  m=(1+r)*E*X;q=r*E*a;split=(1+r)*c
  pp=np.array([[m*m+q*q+split,-m*q],[-m*q,q*q]])
  if name=='broken':pp+=np.outer([5*G*a,-5*G*b],[5*G*a,-5*G*b])
  pm=np.array([[m*m+q*q-split,m*q],[m*q,q*q]])
  es=np.r_[np.linalg.eigvalsh(pp),np.linalg.eigvalsh(pm)]
  assert es.min()>-1e-12,es
  es=np.maximum(es,0)
  if name=='broken':
   # Remove gauge Goldstone, keeping any additional genuine zero eigenvalue.
   es=np.delete(es,np.argmin(es))
   MF=np.array([[m,q,5*G*a],[q,0,5*G*b],[5*G*a,5*G*b,0]])
   ef=np.linalg.eigvalsh(MF)**2;ev=[25*G*G*(a*a+b*b)]
  else:
   ef=np.linalg.eigvalsh(np.array([[m,q],[q,0.]]))**2;ev=[]
  out.append(dict(name=name,mult=mult,scalar=es,weyl=np.array(ef),vector=np.array(ev)))
 out.append(dict(name='singlet',mult=1,scalar=np.array([0,0,2*E,2*E,2*E,2*E]),weyl=np.array([0,2*E,2*E]),vector=np.array([])))
 out.append(dict(name='unbroken',mult=12,scalar=np.array([]),weyl=np.array([0]),vector=np.array([0.])))
 return out

def arrays(X):
 bb=[];ff=[];nb=[];nf=[]
 for s in blocks(X):
  for m in s['scalar']:bb.append(m);nb.append(s['mult'])
  for m in s['vector']:bb.append(m);nb.append(s['mult']*(2 if s['name']=='unbroken' else 3))
  for m in s['weyl']:ff.append(m);nf.append(2*s['mult'])
 return np.array(bb),np.array(nb),np.array(ff),np.array(nf)

_GL={}
def thermal_J(y,fermion=False,n=128):
 """Returns negative free-energy function for either statistic."""
 y=np.atleast_1d(np.asarray(y,float))
 if n not in _GL:
  z,w=leggauss(n);x=25*(z+1);_GL[n]=(x,25*w*x*x)
 x,w=_GL[n];en=np.sqrt(y[:,None]+x[None,:]**2);q=np.exp(-en)
 values=-np.log1p(q) if fermion else np.log1p(-q)
 return values@w

def therm(X,T,n=128,parts=False):
 b,nb,f,nf=arrays(X)
 bj=thermal_J(b/T**2,n=n);fj=thermal_J(f/T**2,True,n=n)
 factor=T**4/(2*math.pi**2)
 return factor*(float(nb@bj)+float(nf@fj))

def therm_sub(X,T,n=128):return therm(X,T,n)-therm(0,T,n)

def fd(fun,x,h=1e-4):
 vs=[fun(x+j*h) for j in (-2,-1,0,1,2)]
 return (vs[0]-8*vs[1]+8*vs[3]-vs[4])/(12*h),(-vs[0]+16*vs[1]-30*vs[2]+16*vs[3]-vs[4])/(12*h*h)

def cw_mp(X):
 # Independent implementation of TP01 complete representation blocks.
 e=mp.mpf('.003');g=mp.sqrt(mp.mpf(29)/200)*e;a=mp.sqrt(2/(31*e));c=e/31
 ans=mp.mpf(0)
 for name,r,mult in [('SU3',mp.mpf(2),8),('SU2',mp.mpf(-3),3),('broken',mp.mpf('-.5'),12)]:
  m=(1+r)*e*X;q=r*e*a;split=(1+r)*c
  pp=mp.matrix([[m*m+q*q+split,-m*q],[-m*q,q*q]])
  if name=='broken':
   vv=mp.matrix([5*g*a,-5*g*X]);pp+=vv*vv.T
  pm=mp.matrix([[m*m+q*q-split,m*q],[m*q,q*q]])
  es=list(mp.eigsy(pp,eigvals_only=True))+list(mp.eigsy(pm,eigvals_only=True))
  if name=='broken':
   mf=mp.matrix([[m,q,5*g*a],[q,0,5*g*X],[5*g*a,5*g*X,0]])
   ef=[v*v for v in mp.eigsy(mf,eigvals_only=True)];ev=[25*g*g*(a*a+X*X)]
  else:ef=[v*v for v in mp.eigsy(mp.matrix([[m,q],[q,0]]),eigvals_only=True)];ev=[]
  def term(vals):return sum(v*v*(mp.log(v)-mp.mpf('1.5')) for v in vals if v>mp.mpf('1e-55'))
  ans+=mult*(term(es)-2*term(ef)+3*term(ev))/(64*mp.pi**2)
 return ans

CAN=json.loads((HERE.parent/'canonical/run_highprecision/result.json').read_text())
PRO=json.loads((HERE.parent/'protected/run_export_002/result.json').read_text())
COEF=json.loads((HERE.parent/'canonical/run_coefficients/result.json').read_text())

def cf(key,s):
 co=[mp.mpf(str(v)) for v in COEF['fits']['29'][key]];x=(2*s-mp.mpf('.28'))/mp.mpf('.32');v0=mp.mpf(1);v1=x;ans=co[0]+co[1]*x
 for aa in co[2:]:v0,v1=v1,2*x*v1-v0;ans+=aa*v1
 return ans*mp.mpf('.1')**mp.mpf(str(COEF['powers'][key]))

class Vacuum:
 def __init__(self,kind):
  self.kind=kind;self.e=mp.mpf('.003');self.a0=mp.sqrt(2/(31*self.e));self.xold=mp.mpf(str(Z))/mp.sqrt(31*self.e)
  if kind=='canonical':
   p=CAN['export']['parameters'];self.mu=mp.mpf(p['mu']);self.p=mp.mpf(p['p']);self.y=mp.mpf(p['y']);self.xv=self.xold*mp.mpf(p['t']);self.u=mp.mpf(p['u']);self.v=mp.mpf(p['v']);self.ms=CAN['candidate']['m_sigma_GeV']
  else:
   p=PRO['normalized_packet'];q=PRO['preferred_row'];self.mu=mp.mpf(p['constants']['MU']);self.p=mp.mpf(p['constants']['M']);self.tau=mp.mpf(p['tau']);self.w=mp.mpf(p['w0_normalized']);self.xv=mp.mpf(q['X_GeV'])/self.mu;self.ms=q['neutral_scalar_masses_GeV'][1]
  self.R=float(mp.sqrt(31)*self.xv*self.mu)
 def tree(self,X,u=0,v=0):
  e=self.e;a=self.a0+u;b=X+v;p=self.p
  if self.kind=='canonical':
   w=p*self.y+X-15*e*X*a*a+15*e*a*a*b;k=X*X+30*a*a+30*b*b
   dx=1-15*e*a*a+X*w/p**2;da=a*e*(X-b)-a*w/p**2;db=e*a*a/2+b*w/p**2
   return mp.exp(k/p**2)*(dx*dx+30*da*da+30*db*db-3*w*w/p**2)
  n=mp.mpf('2.9999');eps=3-n;bc=mp.mpf('1e8');ss=2*self.tau;H=ss+bc*(ss-1)**4;P=1+4*bc*(ss-1)**3;Q=12*bc*(ss-1)**2
  TT=(X+30*b)/mp.sqrt(31);NN=mp.sqrt(mp.mpf(30)/31)*(X-b);qq=mp.sqrt(30)*a
  FF=1/mp.sqrt(31);aa=mp.sqrt(mp.mpf(30)/31);kk=e*mp.sqrt(mp.mpf(31)/30)
  w=FF*TT+aa*NN-kk*NN*qq*qq/2+p*FF/mp.sqrt(eps)*self.w
  wi=[FF,aa-kk*qq*qq/2,-kk*NN*qq];S=TT*wi[0]+NN*wi[1]+qq*wi[2];F0=sum(q*q for q in wi)
  Y=H-(TT*TT+NN*NN+qq*qq)/(n*p*p);DH=P*P-H*Q
  return Y**(-n)*(Y*F0-eps*w*w/p**2+Y*Q*(S-n*w)**2/(n*DH*p*p))
 def leading(self,X):return self.tree(X)+cw_mp(X)
 def finite(self,X):
  s=mp.log(X/self.xold)
  guess=(mp.mpf('1e-7'),mp.mpf('3e-7'))
  def fn(u,v):return self.tree(X,u,v)+cf('ja',s)*u+cf('jb',s)*v
  u,v=mp.findroot(lambda u,v:(mp.diff(lambda z:fn(z,v),u),mp.diff(lambda z:fn(u,z),v)),guess,tol=mp.mpf('1e-50'))
  return fn(u,v)+cw_mp(X)+cf('U2diag',s)

def arrays_dX(X):
 a=A0;q0=E*a;outb=[];outf=[];nb=[];nf=[];db=[];df=[]
 def add_eig(M,D,mult,fermion=False,remove=False):
  ev,U=np.linalg.eigh(M);dv=np.einsum('ij,ij->j',U,D@U)
  if fermion:dv=2*ev*dv;ev=ev*ev
  if remove:
   k=np.argmin(abs(ev));ev=np.delete(ev,k);dv=np.delete(dv,k)
  dest=outf if fermion else outb;dd=df if fermion else db;nn=nf if fermion else nb
  dest.extend(np.maximum(ev,0));dd.extend(dv);nn.extend([mult]*(len(ev)))
 for name,r,mult in [('SU3',2.,8),('SU2',-3.,3),('broken',-.5,12)]:
  k=(1+r)*E;m=k*X;q=r*q0;split=(1+r)*E/31;gg=5*G
  pp=np.array([[m*m+q*q+split,-m*q],[-m*q,q*q]])
  dp=np.array([[2*m*k,-k*q],[-k*q,0.]])
  pm=np.array([[m*m+q*q-split,m*q],[m*q,q*q]])
  dm=np.array([[2*m*k,k*q],[k*q,0.]])
  if name=='broken':
   pp+=np.outer([gg*a,-gg*X],[gg*a,-gg*X]);dp+=np.array([[0,-gg*gg*a],[-gg*gg*a,2*gg*gg*X]])
  add_eig(pp,dp,mult);add_eig(pm,dm,mult,remove=(name=='broken'))
  if name=='broken':
   MF=np.array([[m,q,gg*a],[q,0,gg*X],[gg*a,gg*X,0]])
   DM=np.array([[k,0,0],[0,0,gg],[0,gg,0.]])
   add_eig(MF,DM,2*mult,True)
   outb.append(gg*gg*(a*a+X*X));db.append(2*gg*gg*X);nb.append(3*mult)
  else:add_eig(np.array([[m,q],[q,0.]]),np.array([[k,0],[0,0.]]),2*mult,True)
 # Constant-mass singlet and unbroken sectors do not contribute to dF/dX.
 return np.array(outb),np.array(nb),np.array(outf),np.array(nf),np.array(db),np.array(df)

def thermal_force(X,T,n=128):
 b,nb,f,nf,db,df=arrays_dX(X)
 if n not in _GL:thermal_J([0],n=n)
 x,w=_GL[n]
 def deriv(y,fermion):
  en=np.sqrt(y[:,None]+x[None,:]**2);q=np.exp(-en)
  return ((q/(1+q) if fermion else q/(1-q))/en)@w/2
 return T*T/(2*math.pi**2)*(float((nb*db)@deriv(b/T**2,False))+float((nf*df)@deriv(f/T**2,True)))
