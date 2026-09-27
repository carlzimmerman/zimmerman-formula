#!/usr/bin/env python3
"""Perspective carrier variant: joint convexity, positive Schur and domain control."""
import argparse,json,sys
from pathlib import Path
import sympy as s


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();checks={}
 def exact(name,expr):
  r=s.factor(s.simplify(expr));assert r==0,(name,r);checks[name]=str(r)
 t,W,kap,p=s.symbols('t W kap p',positive=True);dp,dt,e,z=s.symbols('dp dt e z',real=True)
 H=((p+e*dp)**2/2+W)/(t+e*dt)
 exact('joint_perspective_Hessian',s.diff(H,e,2).subs(e,0)-(dp-p*dt/t)**2/t-2*W*dt*dt/t**3)
 dot=s.symbols('dot',real=True);L=t*dot*dot/2-W/t
 exact('perspective_Legendre_transform',(p*dot-L).subs(dot,p/t)-(p*p/2+W)/t)
 exact('perspective_source',s.diff(L,t)-(dot*dot/2+W/t**2))
 Hz=kap*z*z+p*p/(2*(1+z));branch=4*kap*z*(1+z)**2
 exact('perspective_two_cell_stationarity',s.diff(Hz,z).subs(p*p,branch))
 exact('perspective_Z_Hessian',s.diff(Hz,z,2).subs(p*p,branch)-2*kap*(1+3*z)/(1+z))
 schur=s.diff(Hz,p,2)-s.diff(Hz,p,z)**2/s.diff(Hz,z,2)
 exact('perspective_positive_momentum_Schur',schur.subs(p*p,branch)-1/(1+3*z))
 exact('perspective_boundary_threshold',branch.subs(z,1)-16*kap)
 exact('perspective_boundary_derivative',s.diff(Hz,z).subs(z,1)-(2*kap-p*p/8))
 assert s.diff(Hz,z).subs({z:1,kap:1,p:5})<0
 out={'runtime':{'python':sys.version,'executable':sys.executable,'sympy':s.__version__},'checks':checks,'count':len(checks),
      'variant':'t=1+P_hZ>0; carrier L=tK-W/t; same gravitational Z square',
      'interior_result':'joint convexity at fixed W>=0 and positive reduced momentum Schur on the declared interior domain',
      'boundary_control':'two cells t1=1+z,t2=1-z: stationary interior branch ends at p²=16*kappa; p=5,kappa=1 has no interior minimizer',
      'nonclaims':['No preservation of t>0 established','No barrier or positive vacuum floor is silently added','Source identity changes from rho to rho/t','No full coupled gravitational Cauchy theorem']}
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':True,'exact_checks':len(checks)}))
if __name__=='__main__':main()
