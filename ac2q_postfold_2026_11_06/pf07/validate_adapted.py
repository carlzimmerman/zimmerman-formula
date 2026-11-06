import argparse,json,sys
from pathlib import Path
import numpy as np
import sympy as S
from scipy.integrate import solve_ivp
from dealias import Padded,transfer
from evolve_projected import rk4
from evolve_adapted import System as Adapted
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'coupled'))
from evolve_adm_v2 import System as Original
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out={};checks={}
pl,r,M,l,b,ss=S.symbols('pl r M l b S',nonzero=True);C=2*M*M*S.exp(4*b)/pl;vol=S.exp(l+2*b);pb=r+C*ss
checks['Hamiltonian_cancellation']=bool(S.simplify((pl*pl-2*pl*pb)/(4*M*vol**2)+M*S.exp(-2*l)*ss-(pl*pl-2*pl*r)/(4*M*vol**2))==0)
s=Adapted(31,128);y=s.initial(True);th=2*np.pi*np.arange(31)/31;y[1:32]+=1e-7*np.cos(th);y[63:]+=1e-4*np.sin(th)
f=s.constrain(y);v=s.rhs(y);yo=y.copy();yo[63:]=f['pb'];o=Original(31,128);o.P=s.P.copy();vo=o.rhs(yo)
_,bb,pp,rr=s.unpack(y);_,bt,pt,rt=s.unpack(v);bx=s.dx(bb);cs=2*s.M**2*np.exp(4*bb)/pp;sp=2*s.dxx(bb)+3*bx**2
recon=rt+cs*(4*bt-pt/pp)*sp+cs*(2*s.dxx(bt)+6*bx*s.dx(bt))
err=float(max(np.max(abs(v[:63]-vo[:63])),np.max(abs(recon-vo[63:]))));out['chain_rule_max_abs']=err;checks['canonical_chain']=err<1e-7
s=Padded(31);y=s.initial(True)
for _ in range(40):y=rk4(s,y,.0025)
t=.1;ss=.01;V=.01;g=.1;K=.5;H0=np.sqrt((ss/2+V)/3);yy=np.sqrt(2*V/ss)*np.sinh(np.arcsinh(np.sqrt(ss/(2*V)))-np.sqrt(3*ss/2)*t);B=-np.log(yy)/3;H=np.sqrt((ss/2+V*np.exp(6*B))/3)
err=max(abs(y[0]-B),np.max(abs(y[1:32]-B)),np.max(abs(y[32:63]+2*H)),np.max(abs(y[63:]+4*H)))
out['padded_FRW_error']=float(err);checks['padded_FRW']=err<1e-8
rows=[]
def rhs(t,y):
 B,H,b,n=y;v2=np.exp(6*B);X=ss/(2*v2);Q2=512**2*np.exp(-2*B);c=1-2*g*X;z=K+g*Q2;E=2*X*z+c*c*Q2;A=z/E
 zd=-2*g*H*Q2;cd=12*g*H*X;Ed=-12*H*X*z+2*X*zd+2*c*cd*Q2-2*H*c*c*Q2;Hd=V*v2
 return [H,Hd,H*n,(zd/z-Ed/E+Hd/H-6*H)*n-A*ss*Q2*b/H]
for eps in [1e-8,1e-9]:
 ref=solve_ivp(rhs,[0,.01],[0,H0,eps,0],method='DOP853',rtol=1e-12,atol=[1e-14,1e-14,1e-24,1e-24])
 s=Padded(31);y=s.initial(True);wave=np.cos(4*th);y[1:32]+=eps*wave;y[32:63]-=4*H0*eps*wave;y[63:]-=8*H0*eps*wave
 for _ in range(16):y=rk4(s,y,.000625)
 B,H,bb,nn=ref.y[:,-1];error=float(np.max(abs(y[1:32]-B-bb*wave))/eps)
 rows.append(dict(amplitude=eps,beta_reference=float(bb),beta_projected=float(2*np.mean((y[1:32]-B)*wave)),beta_relative_error=error));checks[f'linear_{eps}']=error<1e-2
out['linear']=rows;out['checks']=checks;out['all_pass']=all(checks.values());open(a.output,'w').write(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if out['all_pass']else 1)
