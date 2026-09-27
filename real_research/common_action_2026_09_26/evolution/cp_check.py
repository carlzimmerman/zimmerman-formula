#!/usr/bin/env python3
"""Compensated lapse-independent convex gate: exact frozen principal repair."""
import argparse,json,sys,itertools
from pathlib import Path
import sympy as s


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();checks={}
 def exact(name,expr):
  z=s.factor(s.simplify(expr));assert z==0,(name,z);checks[name]=str(z)
 a,ell,f,h,C,G2,J1,k=s.symbols('a ell f h C G2 J1 k',real=True)
 cN=1-a/2;A=2*cN;Q=1-(1-f)*ell*h/4
 D=1+f*C*h*h+G2*h*h*(J1*J1+ell*ell*k*k)/4
 ae=2-A*Q*Q/D
 phi,U=s.symbols('phi U',real=True)
 quad=2*phi**2+A*D*U**2-2*A*Q*phi*U
 exact('CP_auxiliary_stationarity',s.diff(quad,U).subs(U,Q*phi/D))
 exact('CP_Schur_coefficient',quad.subs(U,Q*phi/D)-ae*phi*phi)
 exact('CP_lower_gap',ae-a-(2-a)*(D-Q*Q)/D)
 exact('CP_upper_gap',2-ae-(2-a)*Q*Q/D)
 exact('CP_UV_limit',ae.subs(h,0)-a)
 exact('CP_full_on_plateau',ae.subs({f:1,G2:0})-(a+2*C*h*h)/(1+C*h*h))
 exact('CP_off_branch_Q',Q.subs(f,0)-(1-ell*h/4))
 exact('CP_uncompensated_comparison',(1+f*ell*h/4)-Q-ell*h/4)
 # Full-on weighted action identity: compensation cancels the affine Delta_h term.
 x=s.symbols('x');N=s.Function('N')(x);W=s.Function('W')(x)
 exact('CP_plateau_boundary_identity',N*ell*s.diff(W,x,2)+ell*s.diff(N,x)*s.diff(W,x)-ell*s.diff(N*s.diff(W,x),x))
 # Exact N=e^n compensation second jet and its principal cross coefficient.
 e,n,nx,a0,w0,sw,c=s.symbols('e n nx a0 w0 sw c',real=True)
 Nc=1+e*n+e*e*n*n/2
 comp=Nc*c*ell*(a0+e*nx)*(w0+e*sw)
 exact('CP_compensation_second_jet',s.diff(comp,e,2).subs(e,0)-c*ell*(a0*w0*n*n+2*n*(a0*sw+w0*nx)+2*nx*sw))
 exact('CP_principal_cross',-4*c+ell*c*(1-f)*h+4*c*Q)
 # The source and U equations in the off branch imply the calibrated response.
 source=s.symbols('source',real=True);q=s.symbols('q',positive=True)
 sol=s.solve([q*U-source,U-q*phi],[U,phi],dict=True)[0]
 exact('CP_off_static_response',sol[phi]-source/(q*q))
 # Fixed N coercivity bridges, with r=||DU||_N, A0=||a||_N.
 r,A0,beta=s.symbols('r A0 beta',real=True)
 exact('CP_base_coercivity_identity',2*(r-A0)**2-r*r+2*A0*A0-(r-2*A0)**2)
 exact('CP_linear_Young_identity',r*r/2+beta*beta*A0*A0/2-beta*A0*r-(r-beta*A0)**2/2)
 examples=[]
 for fv,hv,cv,gv in itertools.product([0,s.Rational(1,2),1],[0,s.Rational(1,2),1],[0,1,100],[0,s.Rational(35,16)]):
  sub={a:s.Rational(1,10),ell:s.Rational(1,50),f:fv,h:hv,C:cv,G2:gv,J1:3,k:2};v=s.factor(ae.subs(sub));assert s.Rational(1,10)<=v<2
  examples.append(str(v))
 off_bound=s.factor((1-s.Rational(1,10**6)/4)**(-2)-1)
 out={'runtime':{'python':sys.version,'executable':sys.executable,'sympy':s.__version__},'checks':checks,'count':len(checks),
      'Q':str(Q),'D':str(D),'alpha_eff':str(ae),'positive_block_controls':len(examples),'example_min_alpha_eff':str(min(map(s.Rational,examples))),'example_max_alpha_eff':str(max(map(s.Rational,examples))),
      'ell_1e6_off_fractional_bound':str(off_bound),'ell_1e6_off_fractional_bound_float':float(off_bound),
      'scope':'Frozen derivative block with Nmeasure compensation; exact full-on boundary cancellation and off-branch calibration',
      'nonclaims':['No full lower-order curved-background spectral stability','No constraint-preservation or nonlinear all-time existence theorem','The off-branch scale-dependent response is a changed prediction, not already observationally certified']}
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':True,'exact_checks':len(checks),'positive_block_controls':len(examples)}))
if __name__=='__main__':main()
