#!/usr/bin/env python3
"""Exact inactive de Sitter scalar repair; no numerical spectrum scan."""
import argparse,json,sys
from pathlib import Path
import sympy as s

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();checks={}
 def exact(name,expr):
  z=s.factor(s.simplify(expr));assert z==0,(name,z);checks[name]=str(z)
 H,K,x,xi,r0,alpha,eta,u,zeta=s.symbols('H K x xi r0 alpha eta u zeta',positive=True)
 d,dp,dpp=s.symbols('d dp dpp',real=True)
 S=s.exp(-u);r=r0*S;ae=2-(2-alpha)*(1-r)**2;g=(S-S*S)/u
 dq=ae+eta*g
 Dold=x*ae+6*H*H*r*(1-r)
 Dnew=Dold-6*H*H*(1/r0-1)*r*r
 exact('new_vacuum_stiffness_D',Dnew-(x*ae+6*H*H*r0*S*(1-S)))
 exact('D_equals_x_d',Dnew.subs(u,xi*xi*x/2)-x*dq.subs({u:xi*xi*x/2,eta:3*H*H*xi*xi*r0}))
 exact('IR_constant_before_tuning',s.limit((Dold-6*H*H*zeta*r*r).subs(u,xi*xi*x/2),x,0)-6*H*H*r0*(1-(1+zeta)*r0))
 exact('IR_tuning_roundtrip',(6*H*H*r0*(1-(1+zeta)*r0)).subs(zeta,1/r0-1))
 F=K*H*H+x*d;A=K*x*d/F;B=4*K*H*x/F;C=2*x-4*x*x/F
 total=lambda f:s.diff(f,x)+s.diff(f,d)*dp
 Ceff=C-(3*H*B-2*H*x*total(B))/2
 numerator=K*H*H*(2+d+2*x*dp)+x*d*(2-d)
 exact('integrated_PQ_stiffness',Ceff+2*x*x*numerator/F**2)
 friction=3*H-2*H*x*total(A)/A
 exact('PQ_friction',friction-H*(3-2*K*H*H/F*(1+x*dp/d)))
 exact('PQ_friction_lower_decomposition',friction-H-2*H*x*d/F+2*H*K*H*H*x*dp/(F*d))
 exact('filter_integral_representation',s.integrate(s.exp(-s.Symbol('v')*u),(s.Symbol('v'),1,2))-g)
 exact('g_derivative_identity',2*u*s.diff(g,u)-2*(-S+2*S*S-g))
 exact('alpha_derivative_identity',2*u*s.diff(ae,u)+4*(2-alpha)*u*r*(1-r))
 exact('PQ_d_IR',s.limit(dq,u,0)-(2-(2-alpha)*(1-r0)**2+eta))
 exact('PQ_d_derivative_IR',s.limit(s.diff(dq,u),u,0)-(-2*(2-alpha)*r0*(1-r0)-s.Rational(3,2)*eta))
 exact('rational_upper_bound',s.Rational(23,16)+s.Rational(1,10)-s.Rational(123,80))
 exact('rational_derivative_margin',2-4*s.Rational(1,4)-4*s.Rational(1,10)-s.Rational(3,5))
 exact('PQ_kinetic_IR',s.limit(A/x,x,0)-d/H**2)
 exact('PQ_IR_speed',s.limit(-Ceff/(A*x),x,0)-2*(d+2)/(K*d))
 exact('PQ_UV_speed',s.limit((-Ceff/(A*x)).subs({d:alpha,dp:0}),x,s.oo)-2*(2-alpha)/(K*alpha))
 # Independent rational witnesses for the sufficient sign conditions, not a scan.
 exact('PQ_sufficient_margin_witness',numerator.subs({K:8,H:1,x:1,d:1,dp:-s.Rational(1,2)})-17)
 out={'runtime':{'python':sys.version,'executable':sys.executable,'sympy':s.__version__},'checks':checks,'count':len(checks),
      'parameter_domain':'0<alpha<=1, 0<ell<=1, r0=ell/4, xi>0, H>0, c2>0, eta=3 H² xi² r0<=1/10',
      'analytic_bounds':{'d':'0<d<=123/80<2','derivative_margin':'2+d+2u*d_u>=3/5','kinetic':'A=Kxd/(KH²+xd)>0 at x>0','integrated_gradient':'Ceff<0 at every x>0','future_friction':'>=H using d_x<0'},
      'nonclaims':['Not uniform positive kinetic at q=0: A~d0 q²/H²','Not nonlinear global PDE closure','All-q proof uses analytic inequalities in report, not finite sampling','Counterpart without the new quadratic vacuum term retains its infrared negative stiffness']}
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':True,'exact_checks':len(checks)}))
if __name__=='__main__':main()
