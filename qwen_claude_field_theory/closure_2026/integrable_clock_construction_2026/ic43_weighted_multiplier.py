"""Audit multiplier coordinates before inferring a physical singularity.

Exact regular-bulk pin-sector reduction; a mechanical free-boundary example.
NOT a full gravitational Dirac count or global equivalence across eta=0.
"""
import argparse
from functools import lru_cache
import json
import sympy as s

Q,P,w,pw,ell,pe,wc=s.symbols('Q P w p_w ell p_ell w_c',real=True)
pairs=((Q,P),(w,pw),(ell,pe))


def pb(a,b):
    return s.expand(sum(s.diff(a,q)*s.diff(b,p)-s.diff(a,p)*s.diff(b,q) for q,p in pairs))


def matrix(constraints):
    return s.Matrix([[pb(a,b) for b in constraints] for a in constraints])


@lru_cache(None)
def bulk():
    H0=s.Function('H0')(Q,P,w);F=s.Function('F')(Q,P,w)
    H=H0+F*ell*(w-wc);uw,ue=s.symbols('u_w u_ell')
    constraints=[pw,pe,s.diff(H,w),s.diff(H,ell)]
    def pin(e):return s.simplify(e.subs(ell,-s.diff(H0,w)/F).subs(w,wc))
    C=matrix(constraints).applyfunc(pin);inverse=C.inv()
    left=s.Matrix([[pin(pb(Q,c)) for c in constraints]])
    right=s.Matrix([pin(pb(c,P)) for c in constraints])
    bracket=s.simplify(pb(Q,P)-(left*inverse*right)[0])
    preservation=[pin(pb(c,H+uw*pw+ue*pe)) for c in constraints[2:]]
    multipliers=s.solve(preservation,[uw,ue],dict=True)[0]
    residual=s.simplify(sum(v.subs(multipliers)**2 for v in preservation))
    rank=C.rank();first=len(constraints)-rank
    return dict(constraints=constraints,poisson_matrix=C,determinant=s.factor(C.det()),
        matrix_rank=rank,first_class=first,second_class=rank,
        canonical_pairs_remaining=s.Rational(2*len(pairs)-2*first-rank,2),
        multipliers=multipliers,physical_bracket_error=s.simplify(bracket-1),
        reduced_H_error=s.simplify(pin(H)-H0.subs(w,wc)),preservation_error=residual)


@lru_cache(None)
def repo_pin_identity():
    import ic30_radial_bridge as radial
    d=radial.radial_action();S,ww,QQ,qq,z,sh,beta,ll=d['fields']
    return s.simplify(s.diff(d['L'],ll)-d['J']*d['eta']*s.exp(S)*(ww-d['wc']))


@lru_cache(None)
def example():
    H0=(P**2+Q**2)/2+P**4/2+w*P**2+w**2/2
    # eta=P^4 on P>0, eta identically zero on P<0; wc=0.
    ell_on=s.solve(s.diff(H0,w).subs(w,0)+P**4*ell,ell)[0]
    won=s.Integer(0);woff=s.solve(s.diff(H0,w),w)[0]
    Hplus=s.simplify(H0.subs(w,won));Hminus=s.simplify(H0.subs(w,woff))
    # Off-phase primaries follow from absent auxiliary velocities; only
    # nonzero primary-preservation expressions generate secondary constraints.
    primaries=[pw,pe];secondaries=[-pb(c,H0) for c in primaries if pb(c,H0)!=0]
    constraints=primaries+secondaries
    off=lambda e:s.simplify(e.subs(w,woff))
    C=matrix(constraints).applyfunc(off);rank=C.rank();first=len(constraints)-rank
    uw=s.Symbol('u_w');pres=off(pb(secondaries[0],H0+uw*pw))
    usw=s.solve(pres,uw)[0]
    return dict(H0=H0,ell_on=ell_on,weighted_multiplier=P**4*ell_on,
        weighted_multiplier_error=s.simplify(P**4*ell_on+P**2),w_off=woff,
        H_on=Hplus,H_off=Hminus,zero_phase_constraints=constraints,
        zero_phase_poisson_matrix=C,zero_phase_rank=rank,zero_phase_first_class=first,
        zero_phase_second_class=rank,
        zero_phase_canonical_pairs=s.Rational(2*len(pairs)-2*first-rank,2),
        zero_phase_preservation_error=s.simplify(pres.subs(uw,usw)),
        global_replacement_error=s.simplify(Hplus-Hminus),
        crossing_force_jump=s.limit(s.diff(Hplus,P)-s.diff(Hminus,P),P,0),
        energy_flow_error=pb(Hplus,Hplus)+pb(Hminus,Hminus),
        positive_Hpp_both_sides=bool(s.diff(Hplus,P,2).is_positive and s.diff(Hminus,P,2).is_positive),
        Hpp_on=s.diff(Hplus,P,2),Hpp_off=s.diff(Hminus,P,2),
        third_derivative_jump=s.limit(s.diff(Hplus-Hminus,P,3),P,0),
        fourth_derivative_jump=s.limit(s.diff(Hplus-Hminus,P,4),P,0))


def orbit():
    import numpy as np
    from scipy.integrate import solve_ivp
    def rhs(t,y):return [y[1]+2*max(y[1],0.)**3,-y[0]]
    def crossing(t,y):return y[1]
    crossing.direction=-1
    sol=solve_ivp(rhs,(0,2),[1.,.25],method='DOP853',rtol=1e-11,atol=1e-13,
                  events=crossing,dense_output=True)
    q,p=sol.sol(np.linspace(0,2,401));energy=(q*q+p*p)/2+np.maximum(p,0)**4/2
    return dict(solver_success=sol.success,crossing_times=sol.t_events[0].tolist(),
        relative_energy_drift=float(np.max(abs(energy/energy[0]-1))),
        final_Q=float(q[-1]),final_P=float(p[-1]),samples=401,
        scope='Mechanical reduced-action completion, not a relativistic gravity solution')


def serial(value):
    if isinstance(value,dict):return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [serial(v) for v in value]
    if isinstance(value,(int,float,str,bool)) or value is None:return value
    if isinstance(value,s.MatrixBase):return [[str(v) for v in row] for row in value.tolist()]
    return str(value)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--strict',action='store_true');a=p.parse_args()
    print(json.dumps(serial(dict(bulk=bulk(),repo_pin_identity=repo_pin_identity(),example=example(),
        orbit=orbit(),full_theory='OPEN',non_claim='No global equivalence, full gravitational DOF count, or empirical prediction')),indent=2))
    raise SystemExit(2 if a.strict else 0)
