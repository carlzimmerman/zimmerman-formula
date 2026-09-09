"""Vary both spherical metric components before isotropy, retaining w(r).

Unlike IC33's pinned flow, this is usable on both IC44 phases. It checks the
independent angular transmission condition but is not an evolution solver.
"""
import argparse
from functools import lru_cache
import json
import sympy as s
import ic30_radial_bridge as radial
import ic44_second_transmission as transmission


@lru_cache(None)
def derive():
    d=radial.radial_action();r=d['r'];S,w,Q,q,z,sh,beta,ell=d['fields']
    ar,bt=(s.Function(n)(r) for n in ('ar','bt'))
    ad,bd,qd,sd=s.symbols('adot bdot q_t shear_t',real=True)
    J=r**2*s.exp(ar+2*bt);v=d['v'];tau=d['t'];ap,bp=s.diff(ar,r),s.diff(bt,r)
    R=s.exp(-2*ar)*(-4*s.diff(bt,r,2)-6*bp**2+4*ap*bp
        +4*ap/r-12*bp/r-2/r**2)+2*s.exp(-2*bt)/r**2
    mixed=2*d['u']*d['xi']*s.diff(d['xi'],r)*s.diff(d['u'],r)+d['xi']**2*s.diff(d['u'],r)**2
    density=2*(q+2*sh)*ad/3+4*(q-sh)*bd/3-2*tau*sh**2/3+tau*q**2/6
    density+=d['A']*q*z+s.exp(S)*d['P0']+d['D']*z**2+d['E4']*z**4
    density-=2*(q+2*sh)*(s.diff(beta,r)+beta*ap)/3
    density-=4*(q-sh)*beta*(bp+1/r)/3
    L=J*(density+v*R+2*v*s.exp(-2*ar)*mixed)
    Ea=radial.euler(L,ar,r,2)-2*J*(qd+2*sd+(ad+2*bd)*(q+2*sh))/3
    Eb=radial.euler(L,bt,r,2)-4*J*(qd-sd+(ad+2*bd)*(q-sh))/3
    def iso(expr):
        return s.simplify(expr.subs({ar:Q,bt:Q,ad:d['Qdot'],bd:d['Qdot']},simultaneous=True).doit())
    Ea,Eb=iso(Ea/J),iso(Eb/J)
    shear_eq=s.simplify((2*Ea-Eb)/4)
    trace_eq=s.simplify((Ea+Eb)/2)
    Qflow=-tau*q/6-d['A']*z/2+(s.diff(beta,r)+3*beta*s.diff(Q,r)+2*beta/r)/3
    shear_eq=s.simplify(shear_eq.subs(d['Qdot'],Qflow))
    trace_eq=s.simplify(trace_eq.subs(d['Qdot'],Qflow))
    boundary=4*r**2*s.exp(Q)*v*s.diff(Q,r)
    action_error=s.simplify(iso(L)-d['L'].subs(ell,0)+s.diff(boundary,r))
    old_trace=radial.radial_equations()['Q'].subs(ell,0)/d['J']
    trace_error=s.simplify(Ea+Eb-old_trace.subs(d['qdot'],qd))
    fields=s.symbols('S w Q q z shear beta',real=True)
    grads=s.symbols('S_r w_r Q_r q_r z_r shear_r beta_r',real=True)
    seconds=s.symbols('S_rr w_rr Q_rr q_rr z_rr shear_rr beta_rr',real=True)
    old=d['fields'][:-1]
    mapping={**dict(zip(old,fields)),**dict(zip([s.diff(f,r) for f in old],grads)),
             **dict(zip([s.diff(f,r,2) for f in old],seconds))}
    shear_eq=shear_eq.xreplace(mapping)
    first=transmission.derive();speed=first['speed'];j=first['jumps']
    ds,dw,dc,dh=s.symbols('dS_rr dw_rr dQ_rr dshear_r',real=True)
    sub={seconds[0]:seconds[0]+ds,seconds[1]:seconds[1]+dw,seconds[2]:seconds[2]+dc,
         grads[5]:grads[5]+dh,sd:sd-speed*dh}
    jump=s.simplify(shear_eq.subs(sub,simultaneous=True)-shear_eq)
    K=2*d['m']*s.exp(fields[0]+2*fields[1]-2*fields[2])
    expected=(speed+fields[6])*dh+K*(ds+2*dw+dc)/4
    residual=s.simplify(jump.subs({ds:j['S_rr'],dw:j['w_rr'],dc:j['Q_rr'],dh:j['shear_r']}))
    return dict(curvature_identity=s.simplify(radial.static_geometry()['R']-R),
        action_boundary_identity=action_error,trace_identity=trace_error,
        Q_flow=Qflow.xreplace(mapping),q_flow=trace_eq.subs(qd,0).xreplace(mapping),
        shear_equation=shear_eq,shear_flow=shear_eq.subs(sd,0),
        shear_jump=jump,shear_jump_identity=s.simplify(jump-expected),
        ic44_angular_residual=residual,
        scope='Independent unpinned spherical metric variation and local transmission; no full 3D or time-evolution closure')


if __name__=='__main__':
    from ic43_weighted_multiplier import serial
    p=argparse.ArgumentParser();p.add_argument('--strict',action='store_true');args=p.parse_args()
    print(json.dumps(serial(dict(result=derive(),full_theory='OPEN')),indent=2))
    raise SystemExit(2 if args.strict else 0)
