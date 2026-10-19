"""Full two-field EKG in z=sqrt(G) r; TF used only for initial guess."""
import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp,solve_ivp,cumulative_trapezoid
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import brentq
from scipy.special import expit
p=argparse.ArgumentParser();p.add_argument('--G',type=float,default=1e-8);p.add_argument('--central-x',type=float,default=.4);p.add_argument('--Z',type=float,default=1.);p.add_argument('--tol',type=float,default=1e-7);p.add_argument('--central-h',type=float);p.add_argument('--z0',type=float,default=1e-6);p.add_argument('--points',type=int,default=16001);p.add_argument('--initial-nodes',type=int,default=2000);p.add_argument('--seed');p.add_argument('--output',required=True);args=p.parse_args()
G=args.G;m=1.;lam=1.;ustar=.02;rlam=2.;Delta=4*ustar**2;M2=4+Delta;g=math.sqrt(Delta/(1+rlam));lrep=lam-g*g/Delta;zeta=ustar**2*rlam/(1+rlam);dc=zeta*args.central_x
D=Delta-4*dc;Ac=lam*D-g*g;nc=dc*D/(2*Ac);fc=math.sqrt(nc);z0=args.z0

def eos(x):
 if x<=0:return 0.,0.,0.,0.,0.
 d=zeta*x;D=Delta-4*d;A=g*g*rlam*(1-x);n=d*D/(2*A);h=g*d/(2*A);S=n+4*h*h;w=math.sqrt(1+d);p=.5*d*n;e=2*w*w*S-p;q=2*w*S
 return p,e,q,n,h

def tfseed(z):
 Hc=.5*math.log1p(dc);pc,ec,qc,_,_=eos(args.central_x)
 def rhs(r,v):
  mass,H,Q=v;x=math.expm1(2*H)/zeta;p,e,q,_,_=eos(x);N=1-2*mass/r
  return [4*math.pi*r*r*e,-(mass/r**2+4*math.pi*r*p)/N,4*math.pi*r*r*q/math.sqrt(N)]
 def surf(r,v):return v[1]
 surf.direction=-1;surf.terminal=True
 sol=solve_ivp(rhs,(z0,2.),[4*math.pi*ec*z0**3/3,Hc,4*math.pi*qc*z0**3/3],rtol=1e-10,atol=1e-13,max_step=.001,events=surf,dense_output=True)
 R=sol.t_events[0][0];mass=sol.y_events[0][0,0];w=math.sqrt(1-2*mass/R)
 inner=z<R;M=np.where(inner,sol.sol(np.minimum(z,R))[0],mass);H=np.maximum(sol.sol(np.minimum(z,R))[1],0);x=np.expm1(2*H)/zeta
 vals=np.array([eos(v) for v in x]);F=np.sqrt(vals[:,3]);HH=vals[:,4]
 # Smooth only the initial guess; solve_bvp subsequently enforces both full KG equations.
 width=max(2.,.005/(z[1]-z[0]));F=gaussian_filter1d(F,width);HH=gaussian_filter1d(HH,width)
 b=np.log(w)-H
 b[~inner]=.5*np.log(1-2*mass/z[~inner])
 return np.vstack([F,np.gradient(F,z),HH,np.gradient(HH,z),M,b]),np.array([math.log(w/(1-w))])

def fun(z,y,p):
 f,fp,h,hp,v,b=y;w=expit(p[0]);N=1-2*v/z;alpha2=np.exp(2*b);S=f*f+4*h*h;V=f*f+M2*h*h-2*g*h*f*f+lam*f**4;grad=G*N*(fp*fp+hp*hp)
 e=w*w*S/alpha2+grad+V;pr=w*w*S/alpha2+grad-V
 vp=4*math.pi*z*z*e;bp=(v/z**2+4*math.pi*z*pr)/N;ap=(vp/z-v/z**2)/N;B=2/z+bp-ap
 return np.vstack([fp,-B*fp+((1-w*w/alpha2)*f-2*g*h*f+2*lam*f**3)/(G*N),
 hp,-B*hp+((M2-4*w*w/alpha2)*h-g*f*f)/(G*N),vp,bp])

def bc(ya,yb,p):
 w=expit(p[0]);aa=np.exp(2*ya[5]);f,h=ya[0],ya[2];S=f*f+4*h*h;V=f*f+M2*h*h-2*g*h*f*f+lam*f**4;e0=w*w*S/aa+V
 fdd=((1-w*w/aa)*f-2*g*h*f+2*lam*f**3)/(3*G);hdd=((M2-4*w*w/aa)*h-g*f*f)/(3*G)
 center_value=(f-.5*z0*z0*fdd-fc) if args.central_h is None else (h-.5*z0*z0*hdd-args.central_h)
 return np.array([center_value,ya[1]-z0*fdd,ya[3]-z0*hdd,ya[4]-4*math.pi*e0*z0**3/3,yb[0],yb[2],yb[5]-.5*np.log(1-2*yb[4]/args.Z)])
z=np.linspace(z0,args.Z,args.initial_nodes)
if args.seed:
 d=np.load(args.seed); y=np.vstack([np.interp(z,d['z'],d[k]) for k in ['f','fz','h','hz','v','b']]);pars=np.array([float(d['logit_w'])])
else:y,pars=tfseed(z)
sol=solve_bvp(fun,bc,z,y,p=pars,tol=args.tol,max_nodes=30000,verbose=0)
print('status',sol.status,sol.message,'nodes',len(sol.x),'res',max(sol.rms_residuals),'w',expit(sol.p[0]))
if not sol.success:raise SystemExit(1)
z=np.linspace(z0,args.Z,args.points);f,fz,h,hz,v,b=sol.sol(z);w=expit(sol.p[0]);r=z/math.sqrt(G);N=1-2*v/z;alpha=np.exp(b);q=2*w*(f*f+4*h*h)/alpha;Q=cumulative_trapezoid(4*math.pi*z*z*q/np.sqrt(N),z,initial=0)/G**1.5
mass=v[-1]/G**1.5;R99=brentq(lambda zz:float(sol.sol(zz)[4])-.99*v[-1],z0,args.Z,xtol=1e-13)/math.sqrt(G)
rec=dict(G=G,m=m,lambda_total=lam,u_star=ustar,r_lambda=rlam,M=math.sqrt(M2),g=g,central_x_seed=args.central_x,central_f=float(f[0]),central_h=float(h[0]),central_h_fixed=args.central_h,omega=w,ADM_mass=mass,Q=Q[-1],mass_over_mQ=mass/Q[-1],R99=R99,C99=G*mass/R99,f_min=float(f.min()),h_min=float(h.min()),alpha_center=alpha[0],omega_local_center=w/alpha[0],max_residual=float(max(sol.rms_residuals)),bc_max=float(max(abs(bc(sol.y[:,0],sol.y[:,-1],sol.p)))),nodes=len(sol.x),tol=args.tol,Rbox=r[-1])
out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
np.savez(str(out)+'.npz',z=z,r=r,f=f,fp=math.sqrt(G)*fz,fz=fz,h=h,hp=math.sqrt(G)*hz,hz=hz,v=v,b=b,alpha=alpha,a=1/np.sqrt(N),Q=Q,omega=w,G=G,m=m,lambda_total=lam,g=g,M=math.sqrt(M2),logit_w=sol.p[0],collocation_z=sol.x,collocation_y=sol.y,collocation_c=sol.sol.c)
Path(str(out)+'.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
