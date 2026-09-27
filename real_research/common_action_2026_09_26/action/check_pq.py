#!/usr/bin/env python3
"""Exact source, projector and actual de Sitter quadratic checks for GNC-PQ."""
import argparse,json
from pathlib import Path
import sympy as s

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();checks={}
    def exact(name,expr):
        value=s.factor(s.simplify(expr));assert value==0,(name,value)
        checks[name]={'passed':True,'residual':str(value)}
    V,zeta,N,z=s.symbols('V zeta N z',positive=True)
    AQ=V*zeta;LQ=-AQ*z*z
    exact('extra_local_Z_source',s.diff(LQ,z)+2*AQ*z)
    exact('extra_fixed_h_lapse_density',-s.diff(N*LQ,N)-AQ*z*z)
    exact('homogeneous_extra_action_zero',LQ.subs(z,0))
    exact('homogeneous_first_variation_zero',s.diff(LQ,z).subs(z,0))
    exact('positive_canonical_Hessian_increment',s.diff(-LQ,z,2)-2*AQ)
    zdot=s.symbols('zdot',real=True)
    exact('quadratic_energy_exchange',s.diff(-LQ,z)*zdot+zdot*s.diff(LQ,z))
    sigma=V/(1+z)**2-2*AQ*z;rho=V/(1+z)+AQ*z*z
    exact('PQ_vacuum_density_susceptibility',s.diff(rho,z).subs(z,0)+V)
    exact('PQ_vacuum_source_susceptibility',s.diff(sigma,z).subs(z,0)+2*V*(1+zeta))

    h1,h2,N1,N2,Z1,Z2=s.symbols('h1 h2 N1 N2 Z1 Z2',positive=True)
    mean=(h1*Z1+h2*Z2)/(h1+h2);z1=Z1-mean;z2=Z2-mean
    meanNz=(h1*N1*z1+h2*N2*z2)/(h1+h2)
    IQ=-AQ*(h1*N1*z1*z1+h2*N2*z2*z2)
    sg1=-2*AQ*z1;sg2=-2*AQ*z2
    msgs=(h1*N1*sg1+h2*N2*sg2)/(h1+h2)
    exact('projected_Z_variation',s.diff(IQ,Z1)-h1*N1*(sg1-msgs/N1))
    exact('projected_source_integral_zero',h1*N1*(sg1-msgs/N1)+h2*N2*(sg2-msgs/N2))
    exact('projected_lapse_density',-s.diff(IQ,N1)/h1-AQ*z1*z1)
    stress1=-AQ*z1*z1+2*AQ*meanNz*z1/N1
    exact('metric_volume_stress_including_projector',s.diff(IQ,h1)-N1*stress1)
    shift=s.symbols('shift',real=True)
    exact('Z_leaf_shift_gauge',IQ.subs({Z1:Z1+shift,Z2:Z2+shift},simultaneous=True)-IQ)

    H,M,K,x,r0,sk,alpha,phi,psi,pd=s.symbols('H M K x r0 S alpha phi psi pd',positive=True)
    r=r0*sk;zetachoice=1/r0-1
    exact('dS_added_quadratic_normalization',(-AQ*z*z*2/M**2).subs({V:3*M*M*H*H,z:r*phi})+6*H*H*zeta*r*r*phi*phi)
    ae=2-(2-alpha)*(1-r)**2
    DP=ae*x+6*H*H*r*(1-r)
    D=ae*x+6*H*H*r0*sk*(1-sk)
    exact('PQ_D_cancellation',DP-6*H*H*zetachoice*r*r-D)
    exact('old_nonzero_IR_D_removed',D.subs({x:0,sk:1}))
    d,dx=s.symbols('d d_x',real=True)
    E=K*H*H+x*d
    L=K*(pd+H*phi)**2+2*x*psi*psi-4*x*phi*psi+x*d*phi*phi
    sol=(2*x*psi-K*H*pd)/E
    A=K*x*d/E;B=4*K*H*x/E;C=2*x-4*x*x/E
    exact('PQ_lapse_stationarity',s.diff(L,phi).subs(phi,sol))
    exact('PQ_reduced_quadratic',L.subs(phi,sol)-(A*pd*pd+B*pd*psi+C*psi*psi))
    # Total derivative along de Sitter redshift xdot=-2Hx; d=d(x).
    Bdot=-2*H*x*(s.diff(B,x)+s.diff(B,d)*dx)
    CI=C-(3*H*B+Bdot)/2
    expected=2*x*x*d/E-4*x*x/E-4*K*H*H*x*x*(d+x*dx)/E**2
    exact('time_integrated_cross_term',CI-expected)
    factored=-2*x*x*(K*H*H*(d+2+2*x*dx)+x*d*(2-d))/E**2
    exact('all_q_stiffness_factorization',CI-factored)
    u,eta=s.symbols('u eta',positive=True);S=s.exp(-u);rr=r0*S
    g=S*(1-S)/u;aeu=2-(2-alpha)*(1-rr)**2
    exact('ae_derivative_bound_identity',2*u*s.diff(aeu,u)+4*(2-alpha)*u*rr*(1-rr))
    exact('g_derivative_bound_identity',u*s.diff(g,u)-(-S+2*S*S-g))
    exact('g_positive_integral_representation',g-s.integrate(s.exp(-s.Symbol('v')*u),(s.Symbol('v'),1,2)))
    exact('upper_d_rational_bound',s.Rational(23,16)+s.Rational(1,10)-s.Rational(123,80))
    exact('upper_d_strict_gap',2-s.Rational(123,80)-s.Rational(37,80))
    exact('positive_derivative_bridge_rational_bound',2-4*s.Rational(1,4)-4*s.Rational(1,10)-s.Rational(3,5))
    exact('exponential_lower_polynomial_bridge',1+u+u*u/2-2*u-((u-1)**2+1)/2)
    out={'claim_id':'CD26_4_PROJECTED_QUADRATIC_REPAIR','number_of_checks':len(checks),'checks':checks,
         'scope':['Exact full-action first variations including mean stress','Actual vacuum de Sitter quadratic addition, relying on evolution ADM expansion','Analytic all-q sign proof recorded in report under alpha<=1,ell<=1,eta<=1/10','No full coupled global evolution, empirical inheritance or zero-mode coercivity']}
    p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'number_of_checks':len(checks),'all_passed':True},indent=2))
if __name__=='__main__':main()
