#!/usr/bin/env python3
"""Coordinator exact checks of phase response and occupied heavy matching."""
import argparse
import json
from pathlib import Path
import resource
import sympy as S


def main(out):
    f,h,l,X,a,b=S.symbols('f h l X a b', positive=True)
    D0=30*h*h+l*l
    V0=(f-15*h*a*a)**2+S.Rational(15,2)*l*l*a**4+30*a*a*(h*X-l*b)**2
    point={a:S.sqrt(2*f*h/D0),b:h*X/l}
    checks={}
    def zero(name,expr):
        checks[name]=S.simplify(expr)==0
        assert checks[name],name
    zero('heavy_a_stationarity',S.diff(V0,a).subs(point))
    zero('heavy_b_stationarity',S.diff(V0,b).subs(point))
    zero('heavy_Haa',S.diff(V0,a,2).subs(point)-120*f*h)
    zero('heavy_Hbb',S.diff(V0,b,2).subs(point)-60*l*l*point[a]**2)
    zero('heavy_Hab',S.diff(V0,a,b).subs(point))

    u,v,F,A,c,cp=S.symbols('u v F A c cp',positive=True)
    N=v-(c+cp/c)*u
    D=v+(c-cp/c)*u
    P_s=v/c-u*cp/c**2-u
    n_log_s=D/(2*u)
    zero('general_pressure_derivative',P_s/n_log_s-2*u*N/(c*D))
    zero('phase_IR_sound_speed',(P_s/n_log_s)/(2*u/c)-N/D)
    zero('phase_canonical_radial_gap',N/(2*A)+c*u/A-D/(2*A))
    y,k=S.symbols('y k',real=True)
    poly=(y-k*k-N/(2*A))*(y-k*k)-(c*u/A)*y
    zero('dispersion_zero_k_gap',poly.subs(k,0)-y*(y-D/(2*A)))
    zero('dispersion_root_product',poly.subs(y,0)-k*k*(k*k+N/(2*A)))
    # A radially stable, negative sound-speed benchmark (not a model data point).
    p=S.Poly(poly.subs({u:1,v:1,c:2,cp:0,A:1,k:S.Rational(1,2)}),y)
    assert p.TC()<0 and -p.nth(1)>0
    checks['one_negative_frequency_squared_benchmark']=True

    delta,q,w,w1,F0,Fb,ja,jb,ha,hb=S.symbols('delta q w w1 F0 Fb ja jb ha hb',positive=True)
    w0=q/(2*F0)
    # n=sqrt(delta)q, omega=sqrt(delta)(w0+delta w1).
    grand=-delta*F0*w*w-delta**2*(ja*ja/ha+(jb-w*w*Fb)**2/hb)/2
    transformed=S.series((grand+delta*w*q).subs(w,w0+delta*w1),delta,0,3).removeO()
    E0=q*q/(4*F0)
    expected=delta*E0-delta**2*(ja*ja/ha+(jb-E0*Fb/F0)**2/hb)/2
    zero('occupied_fixed_charge_grand_Legendre',transformed-expected)
    eps=S.symbols('eps',real=True)
    zero('induced_angular_metric',(F0+30*((b+eps)**2-b*b)-F0).diff(eps).subs(eps,0)-60*b)
    R=S.symbols('R',positive=True)
    zero('coldness_bound_ratio',(1-(1-R))/(1+(1-R))-R/(2-R))
    result={'assertion_tested':'Exact heavy Hessian; general angular phase pressure/dispersion identities; occupied leading-relaxation Legendre transform; one unstable generic benchmark; coldness-bound algebra',
            'checks':checks,'all_checks_pass':all(checks.values()),
            'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'non_claims':['No physical RG root or spectrum calculation here',
                          'Does not bound finite two-loop diagrams or finite kinetic matching',
                          'The coldness inequality also uses the written connected-branch monotonicity proof']}
    Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True)
    main(parser.parse_args().out)
