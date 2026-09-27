#!/usr/bin/env python3
"""Canonical Z convexity and scoped carrier/auxiliary Schur diagnostics."""
import argparse,json,sys
from pathlib import Path
import sympy as s


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();checks={}
 def exact(name,e):
  r=s.factor(s.simplify(e));assert r==0,(name,r);checks[name]=str(r)
 alpha,a,z,u=s.symbols('alpha a z u',real=True);cN=1-alpha/2
 Va=alpha*(a-z)**2+4*a*z-2*z*z-4*cN*z*u
 exact('Z_gravitational_completed_square',Va-(alpha*a*a-2*cN*(z-(a-u))**2+2*cN*(a-u)**2))
 N,V,pp,dot,W=s.symbols('N V pp dot W',positive=True)
 L=V*s.exp(z)*dot*dot/(2*N)-N*V*s.exp(-z)*W
 velocity=pp*N*s.exp(-z)/V
 exact('carrier_canonical_momentum',s.diff(L,dot).subs(dot,velocity)-pp)
 exact('carrier_Hamiltonian',(pp*dot-L).subs(dot,velocity)-N*V*s.exp(-z)*(pp*pp/(2*V*V)+W))
 eps,s0,dZ=s.symbols('eps s0 dZ',real=True)
 exact('canonical_exponential_Hessian',s.diff(s.exp(-z-s0*dZ)*eps,s0,2).subs(s0,0)-s.exp(-z)*eps*dZ*dZ)
 # Mean-zero two-cell canonical minimization: globally convex in its one auxiliary.
 kap,p=s.symbols('kap p',positive=True);zz=s.symbols('zz',positive=True)
 H=kap*zz*zz+s.exp(-zz)*p*p/2
 branch=4*kap*zz*s.exp(zz)
 exact('two_cell_stationarity',s.diff(H,zz).subs(p*p,branch))
 exact('two_cell_Z_Hessian',s.diff(H,zz,2).subs(p*p,branch)-2*kap*(1+zz))
 exact('two_cell_reduced_energy',H.subs(p*p,branch)-kap*zz*(zz+2))
 Hpp=s.diff(H,p,2)-s.diff(H,p,zz)**2/s.diff(H,zz,2)
 exact('two_cell_momentum_Schur',Hpp.subs(p*p,branch)-s.exp(-zz)*(1-zz)/(1+zz))
 assert (s.exp(-zz)*(1-zz)/(1+zz)).subs(zz,2)<0
 # Off-shell flat fixed-velocity diagnostic, with all auxiliary variables kept until Schur reduction.
 K,r,T,d,U,j=s.symbols('K r T d U j',real=True)
 Qaux=K*((r-1)*d*d-2*d*U+T*U*U)+j*d
 Hess=s.hessian(Qaux,(d,U))/(2*K)
 exact('joint_auxiliary_determinant',Hess.det()-((r-1)*T-1))
 sol=s.solve([s.diff(Qaux,d),s.diff(Qaux,U)],[d,U],dict=True)[0]
 exact('auxiliary_eliminated_source',Qaux.subs(sol)+j*j*T/(4*K*((r-1)*T-1)))
 v=s.symbols('v',real=True)
 kin=s.Rational(1,2)-v*v*T/(4*K*((r-1)*T-1))
 exact('fixed_velocity_momentum_coefficient',kin.subs(v*v,4*K*r)-(1+(r+1)*T)/(2*(1+(1-r)*T)))
 # The h-volume projection's second-order mean correction cancels the psi*Z density cross.
 psi,Z,Phi=s.symbols('psi Z Phi',real=True)
 density=s.expand(v*v*(Z-Phi-3*psi)**2/4)
 corrected=s.expand(density+3*v*v*psi*Z/2)
 exact('projection_density_cross_cancellation',s.diff(corrected,psi,Z))
 out={'runtime':{'python':sys.version,'executable':sys.executable,'sympy':s.__version__},'checks':checks,'count':len(checks),
      'two_cell_example':{'z':2,'p_squared':'8*kappa*exp(2)','Z_Hessian':'6*kappa','reduced_momentum_Hessian':'-exp(-2)/3'},
      'canonical_result':'Strong convexity and unique mean-zero variational Z solve at fixed N,h,U,canonical carrier data under stated integrability bounds',
      'nonclaims':['The two-cell kinetic counterexample is not a completed gravitational solution','The fixed-velocity flat diagnostic is not a physical FRW instability theorem','A convex Z solve alone does not establish positive reduced momentum Hessian or all-time coupled evolution']}
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':True,'exact_checks':len(checks)}))
if __name__=='__main__':main()
