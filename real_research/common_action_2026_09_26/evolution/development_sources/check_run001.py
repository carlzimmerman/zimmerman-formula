#!/usr/bin/env python3
"""CD26-4 conditional evolution bridges; no full-action/PDE certificate."""
import argparse, json, math, sys
from pathlib import Path
import sympy as s
import mpmath as mp


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args()
    checks={}
    def exact(name,expr):
        r=s.factor(s.simplify(expr)); assert r==0,(name,r); checks[name]=str(r)
    a,b,C,k,w=s.symbols('a b C k w',positive=True)
    D=-s.I*w
    psi,phi,beta,U=s.symbols('psi phi beta U')
    equations=[4*k**2*psi-4*k**2*phi-D*(-12*D*psi+4*k**2*beta-6*b*(3*D*psi-k**2*beta)),
               -4*k**2*psi-4*k**2*(U-phi)+2*a*k**2*phi,
               4*k**2*D*psi+2*b*k**2*(3*D*psi-k**2*beta),
               4*k**2*(U-phi)+4*k**2*C*U]
    M=s.Matrix([[s.diff(e,z)for z in [psi,phi,beta,U]]for e in equations])
    det=s.factor(M.det())
    cs2=b*(2-a*(1+C))/((2+3*b)*(a+(a+2)*C))
    exact('full_alpha_dispersion_root',det.subs(w**2,cs2*k**2))
    exact('alpha_zero_positive_C_limit',cs2.subs(a,0)-b/((2+3*b)*C))
    exact('deep_C_negative_limit',s.limit(cs2,C,s.oo)+a*b/((2+3*b)*(a+2)))
    exact('explicit_frozen_threshold_crossing',a*(1+3/a)-(a+3))
    healthy=cs2.subs({a:s.Rational(1,10**9),b:s.Rational(1,100),C:1})
    unhealthy=cs2.subs({a:s.Rational(1,10**9),b:s.Rational(1,100),C:3*10**9})
    assert healthy>0 and unhealthy<0

    z1,z2,gamma=s.symbols('z1 z2 gamma',positive=True)
    u1,u2=z1**2,z2**2; f1,f2=u1+gamma*z1,u2+gamma*z2
    exact('resolvent_secant',(u1-u2)*(z1+z2+gamma)-(f1-f2)*(z1+z2))
    exact('resolvent_complement_secant',((f1-u1)-(f2-u2))*(z1+z2+gamma)-(f1-f2)*gamma)
    exact('resolvent_monotonicity',(f1-f2)*(u1-u2)-(u1-u2)**2-gamma*(z1-z2)**2*(z1+z2))
    x,g=s.symbols('x g',positive=True)
    exact('inverse_quadratic_relation',((s.sqrt(g*g+4*x)-g)/2)**2+g*(s.sqrt(g*g+4*x)-g)/2-x)
    exact('inverse_derivative',s.diff(((s.sqrt(g*g+4*x)-g)/2)**2,x)-(1-g/s.sqrt(g*g+4*x)))

    c1,c2,r,t=s.symbols('c1 c2 r t',real=True)
    S=s.Matrix([[s.Rational(3,4),s.Rational(1,4)],[s.Rational(1,4),s.Rational(3,4)]])
    f=s.Matrix([r,t]); cc=s.Matrix([c1,c2]); sf=S*f; sc=S*cc
    exact('two_site_weighted_Jensen',sum(sc[i]*f[i]**2-cc[i]*sf[i]**2 for i in range(2))-s.Rational(3,16)*(c1+c2)*(r-t)**2)
    T=S*s.diag(100,0)*S
    assert max(T.eigenvals())==s.Rational(125,2)<75
    xx,xi=s.symbols('xx xi',positive=True)
    gauss=2*s.integrate(xx**s.Rational(-1,2)*s.exp(-xx**2/(2*xi**2)),(xx,0,s.oo))/(s.sqrt(2*s.pi)*xi)
    factor=s.gamma(s.Rational(1,4))/(2**s.Rational(1,4)*s.sqrt(s.pi))
    exact('transverse_heat_average',gauss-factor/s.sqrt(xi))
    R=s.symbols('R',positive=True)
    exact('codimension_one_integrability',2*s.integrate(xx**s.Rational(-1,2),(xx,0,R))-4*s.sqrt(R))
    # Monotone bounded gate; positive weighting alone is insufficient when it is varied.
    u,K=s.symbols('u K',positive=True)
    gate=1/(1+s.exp(-K*(u-1))/3)
    E=u**2/2+s.Rational(2,3)*gate*u**s.Rational(3,2)
    exact('dynamic_gate_Hessian',s.diff(E,u,2).subs(u,1)-(s.Rational(11,8)+3*K/8-K*K/16))
    hessian=s.diff(E,u,2).subs({u:1,K:16}); assert hessian==-s.Rational(69,8)
    # Exact positive lapse slice; zero constrained Hamiltonian does not bound contrast.
    A,B,xx=s.symbols('A B xx',positive=True)
    y=s.exp(A*s.cos(xx)); lapse=y*y; AA=-4*B*s.diff(y,xx,2)/y
    exact('positive_lapse_constraint',4*B*s.diff(y,xx,2)+AA*y)
    exact('constraint_energy_total_derivative',AA*y*y-4*B*s.diff(y,xx)**2+4*B*s.diff(y*s.diff(y,xx),xx))
    exact('lapse_contrast',lapse.subs(xx,0)/lapse.subs(xx,s.pi)-s.exp(4*A))
    mp.mp.dps=30
    averages=[]
    for width in [.25,1.,2.]:
        # x=z² removes the integrable singularity from the quadrature.
        quadrature=4/(mp.sqrt(2*mp.pi)*width)*mp.quad(lambda z:mp.exp(-z**4/(2*width**2)),[0,1,mp.inf])
        target=mp.gamma(mp.mpf(1)/4)/(2**mp.mpf('.25')*mp.sqrt(mp.pi*width))
        assert abs(quadrature/target-1)<mp.mpf('1e-20')
        averages.append({'xi':width,'quadrature':float(quadrature),'closed_form':float(target)})
    numerical={'heat_power_constant':float(factor.evalf()),'transverse_averages':averages,
               'two_site_actual_operator_norm':62.5,'two_site_heat_coefficient_bound':75.,'two_site_raw_coefficient_sup':100.,
               'frozen_healthy_cs2':float(healthy),'frozen_unhealthy_cs2':float(unhealthy),
               'dynamic_gate_hessian_at_u1_K16':str(hessian),
               'lapse_normalized_examples':[{'A':a0,'Nmin':float(mp.exp(-2*a0)/mp.besseli(0,2*a0)),
                                             'Nmax':float(mp.exp(2*a0)/mp.besseli(0,2*a0)),
                                             'contrast':float(mp.exp(4*a0))}for a0 in [0,1,4]]}
    out={'runtime':{'python':sys.version,'executable':sys.executable,'sympy':s.__version__,'mpmath':mp.__version__},
         'scope':'Fixed-geometry monotonicity, heat smoothing and exact frozen-block/gate warnings; not nonlinear global evolution',
         'exact_checks':checks,'exact_check_count':len(checks),'determinant':str(det),'cs2':str(cs2),'numerical_controls':numerical,
         'nonclaims':['The frozen small-gradient instability is not an admissible gated-background counterexample',
                      'Positive auxiliary Hessian does not establish coupled lapse/metric/clock health',
                      'Transverse-zero source regularity requires uniform geometry, lapse, gate and interpolation hypotheses',
                      'No all-time existence, invariant region or full action constraint-preservation theorem']}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':True,'exact_checks':len(checks)}))

if __name__=='__main__':main()
