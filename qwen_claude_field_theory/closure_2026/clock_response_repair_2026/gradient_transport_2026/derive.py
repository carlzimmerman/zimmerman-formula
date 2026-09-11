#!/usr/bin/env python3
"""Exact same-action radial current and algebraic timelike sign reduction."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent


def derive():
    spec = importlib.util.spec_from_file_location('unfixed_action', HERE.parent/'spherical_baryon_bridge/action/derive.py')
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    q, k, qb, Hb = s.symbols('q k qb Hb', real=True)
    N, A, R, u, Nr, Rr = m.N, m.A, m.R, m.u, m.Nr, m.Rr
    sub = {m.ct:q, m.jets['c',1,1]:0, m.At:N*A*k}
    sub.update({z:0 for (f,i,j),z in m.jets.items() if f=='v'})
    current = s.cancel(m.j.subs(sub, simultaneous=True)*A/(2*N*R**2))
    Q=q/N; Y=u**2/A**2; X=Q**2-Y
    expected = u*(-m.PX+m.WY/N) + m.gamma*(2*Q*k*u+X*Nr/N-2*Rr*Y/R)
    checks = {'current_from_unrestricted_action':s.cancel(current-expected)==0}
    px0 = s.symbols('PX0')
    source = (2*Q*k-3*qb*Hb)*u+X*Nr/N-2*Rr*Y/R
    gap = px0-m.WY/N
    checks['finite_cubic_transport_identity'] = s.cancel(
        current.subs(m.PX,px0+3*m.gamma*qb*Hb)+gap*u-m.gamma*source)==0
    # P_X0=d*B/(B-X), W_Y=d/sqrt(1+Y/ell), B=q^2+2ell.
    n, ell, B, y, d, a, z, t = s.symbols('n ell B y d a z t', positive=True)
    F=n*z-1+(q*q/n**2-ell*(z*z-1))/B
    F0=F.subs(z,1); F1=F.subs(z,t)
    chord=((t-z)*F0+(z-1)*F1)/(t-1)
    checks['exact_positive_chord_remainder'] = s.factor(F-chord-ell/B*(z-1)*(t-z))==0
    checks['endpoint_cubic_identity'] = s.expand(n**3-n**2+a-
        ((n-s.Rational(2,3))**2*(n+s.Rational(1,3))+a-s.Rational(4,27)))==0
    C=d*B/(B-q*q/n**2+y)-d/(n*z)
    checks['gap_sign_numerator'] = s.factor(C*(B-q*q/n**2+y)*n*z/(d*B)
        -(n*z-1+(q*q/n**2-y)/B))==0
    checks['endpoint_timelike'] = s.factor(F1.subs(q*q,n*n*ell*(t*t-1))-(n*t-1))==0
    if not all(checks.values()): raise AssertionError(checks)
    return dict(checks=checks, inherited_action_checks=len(m.checks),
                normalized_radial_current=str(expected), cubic_source=str(source),
                gap_numerator=str(F), full_theory='OPEN',
                exclusions=['instantaneous chi_t spatially constant', 'timelike chi X>=0',
                            'positive log denominator', '0<m<=2 for uniform sign theorem'],
                non_claims=['not a solution of metric constraints', 'not zero current from regularity'])


if __name__=='__main__': print(json.dumps(derive(),indent=2))
