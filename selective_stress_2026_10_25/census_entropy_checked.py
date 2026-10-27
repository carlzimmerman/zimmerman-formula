"""Initial F polytrope entropy from a stated 200-critical-density halo."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp,simpson
G=4.30091e-6;A0=9.3603e-11*3.085677581491367e19/1e6;H0=.0674;ratio=53.6432722396066
def initial_entropy(scale):
 Mb=6e10*scale**2;rm=np.sqrt(G*Mb/A0);b=3*scale/rm;Rv=(G*(1+ratio)*Mb/(100*H0**2))**(1/3);R=Rv/rm
 rad=np.geomspace(1e-5,R,600);guess=np.vstack([ratio*(rad/R)**3,(1+ratio)/R*(1-(rad/R)**2)])
 def ode(r,y,p):
  K=np.exp(p[0]);rho=(np.maximum(y[1],0)/(2.5*K))**1.5;B=r**3/(r*r+b*b)**1.5
  return np.vstack([r*r*rho,-(y[0]+B)/r**2])
 def bc(ya,yb,p):return np.r_[ya[0],yb[0]-ratio,yb[1]]
 sol=solve_bvp(ode,bc,rad,guess,p=np.array([np.log(2.*(ratio/5.364)**(2/3))]),tol=2e-7,max_nodes=10000)
 assert sol.success,sol.message;K=float(np.exp(sol.p[0]));rr=np.geomspace(1e-5,R,12000);M,h=sol.sol(rr);rho=(np.maximum(h,0)/(2.5*K))**1.5;mass=float(simpson(rr*rr*rho,x=rr));assert abs(mass-ratio)<1e-5,(mass,ratio)
 return dict(scale=scale,Mb_Msun=Mb,Mdark_Msun=ratio*Mb,H0_kms_Mpc=67.4,mean_density_convention='200 critical, total baryon+F mass',virial_radius_kpc=Rv,virial_radius_dimensionless=R,K_dimensionless=K,central_F_density_dimensionless=float(rho[0]),BVP_residual=float(max(sol.rms_residuals)),mass_check=mass,r_kpc=(rr*rm).tolist(),mass_profile=M.tolist(),rho=rho.tolist(),enthalpy=h.tolist(),qualification='Initial classical gamma5/3 hydrostatic F halo in fixed Plummer baryon potential. No quantum edge correction; mean overdensity is stated input, not a derived cosmological formation solution.')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out={'runs':[initial_entropy(s) for s in [1.]],'non_claims':['Not temperature slaved to desired galaxy law','Initial virial-density and gamma5/3 assumptions are explicit','Not a full cosmological or energy-conserving collapse derivation']};Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
 for r in out['runs']:print({k:v for k,v in r.items() if not isinstance(v,list)},flush=True)
