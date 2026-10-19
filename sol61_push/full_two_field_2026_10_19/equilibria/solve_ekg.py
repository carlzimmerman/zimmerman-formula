"""Full two-amplitude polar-areal EKG BVP, scaled fields sqrt(4 pi G)."""
import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp,cumulative_trapezoid
from scipy.special import expit
p=argparse.ArgumentParser();p.add_argument('--G',type=float,default=1.);p.add_argument('--central',type=float,default=.05);p.add_argument('--R',type=float,default=120.);p.add_argument('--tol',type=float,default=1e-6);p.add_argument('--g-fraction',type=float,default=1.);p.add_argument('--seed');p.add_argument('--output',required=True);args=p.parse_args()
G=args.G;m=1.;lam=1.;u=.02;ratio=2.;M2=4*(1+u*u);g=math.sqrt(4*u*u/(1+ratio))*args.g_fraction
scale=math.sqrt(4*math.pi*G);L=lam/(4*math.pi*G);c=g/scale;fc=args.central;r0=1e-5

def freq(q): return expit(q[0])

def fun(r,y,p):
 F,Fp,H,Hp,U,b=y; w=freq(p); N=1-2*U/r; alpha2=np.exp(2*b)
 S=F*F+4*H*H; V=F*F+M2*H*H-2*c*H*F*F+L*F**4; grad=Fp*Fp+Hp*Hp
 e=w*w*S/alpha2+N*grad+V; pr=w*w*S/alpha2+N*grad-V
 Up=r*r*e;bp=(U/r**2+r*pr)/N;ap=(Up/r-U/r**2)/N;B=2/r+bp-ap
 return np.vstack([Fp,-B*Fp+((1-w*w/alpha2)*F-2*c*H*F+2*L*F**3)/N,
 Hp,-B*Hp+((M2-4*w*w/alpha2)*H-c*F*F)/N,Up,bp])

def bc(ya,yb,p):
 w=freq(p);N0=1-2*ya[4]/r0; A02=np.exp(2*ya[5]);S0=ya[0]**2+4*ya[2]**2
 V0=ya[0]**2+M2*ya[2]**2-2*c*ya[2]*ya[0]**2+L*ya[0]**4
 e0=w*w*S0/A02+V0
 fdd=((1-w*w/A02)*ya[0]-2*c*ya[2]*ya[0]+2*L*ya[0]**3)/3
 hdd=((M2-4*w*w/A02)*ya[2]-c*ya[0]**2)/3
 kf=math.sqrt(max(1-w*w,1e-15));kh=math.sqrt(max(M2-4*w*w,1e-15));R=args.R
 nu=yb[4]*(2*w*w-1)/kf
 return np.array([ya[0]-.5*r0*r0*fdd-fc,ya[1]-r0*fdd,ya[3]-r0*hdd,
 ya[4]-e0*r0**3/3,yb[1]+(kf+(1-nu)/R)*yb[0],yb[3]+(kh+1/R)*yb[2],yb[5]-.5*np.log(1-2*yb[4]/R)])

r=np.linspace(r0,args.R,800)
if args.seed:
 d=np.load(args.seed);oldr=d['r']; y=np.vstack([np.interp(r,oldr,d[k]) for k in ['F','Fp','H','Hp','U','b']]);pars=np.array([float(d['logit_w'])])
 ratioF=fc/y[0,0];y[0:2]*=ratioF
else:
 width=2/math.sqrt(fc);F=fc*np.exp(-r*r/width**2);Fp=-2*r/width**2*F
 w=.97;H=c*F*F/(M2-4*w*w);Hp=2*H*Fp/np.maximum(F,1e-100)
 V=F*F+M2*H*H-2*c*H*F*F+L*F**4;e=(w*w*(F*F+4*H*H)+Fp*Fp+Hp*Hp+V)
 U=cumulative_trapezoid(r*r*e,r,initial=0);b=-U[-1]/np.sqrt(r*r+width**2)
 y=np.vstack([F,Fp,H,Hp,U,b]);pars=np.array([math.log(w/(1-w))])
sol=solve_bvp(fun,bc,r,y,p=pars,tol=args.tol,max_nodes=20000,verbose=0)
print('status',sol.status,sol.message,'nodes',len(sol.x),'maxres',max(sol.rms_residuals),'w',freq(sol.p))
if not sol.success:raise SystemExit(1)
r=np.linspace(r0,args.R,6001);Y=sol.sol(r);F,Fp,H,Hp,U,b=Y;w=freq(sol.p);N=1-2*U/r;alpha=np.exp(b)
qscaled=2*w*(F*F+4*H*H)/alpha
Q=cumulative_trapezoid(r*r*qscaled/np.sqrt(N),r,initial=0)/G
R99=np.interp(.99*U[-1],U,r);mass=U[-1]/G
record=dict(G=G,m=m,lambda_total=lam,u_star=u,r_lambda=(None if g==0 else lam*4*u*u/(g*g)-1),continuation_target_r_lambda=ratio,M=math.sqrt(M2),g=g,g_fraction=args.g_fraction,
 central_F=fc,omega=w,ADM_mass=mass,Q=Q[-1],mass_over_mQ=mass/Q[-1],R99=R99,C99=U[-1]/R99,
 F_min=F.min(),H_min=H.min(),H_max=H.max(),alpha_center=alpha[0],omega_local_center=w/alpha[0],max_residual=float(max(sol.rms_residuals)),bc_max=float(max(abs(bc(sol.y[:,0],sol.y[:,-1],sol.p)))),nodes=len(sol.x),tol=args.tol,Rbox=args.R)
out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
np.savez(str(out)+'.npz',r=r,F=F,Fp=Fp,H=H,Hp=Hp,U=U,b=b,f=F/scale,fp=Fp/scale,h=H/scale,hp=Hp/scale,alpha=alpha,a=1/np.sqrt(N),Q=Q,omega=w,G=G,m=m,lambda_total=lam,g=g,M=math.sqrt(M2),logit_w=sol.p[0])
Path(str(out)+'.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
