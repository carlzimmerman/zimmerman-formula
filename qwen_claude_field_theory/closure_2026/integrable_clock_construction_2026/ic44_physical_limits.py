"""Independent compact transmission formulas and exceptional-source tests."""
import argparse
from functools import lru_cache
import json
import sympy as s
import ic44_second_transmission as second


@lru_cache(None)
def derive():
    d=second.derive();S,w=d['S'],d['w'];Q=s.Symbol('Q',real=True)
    m=s.Symbol('m',real=True);lam=d['reaction'];V=d['speed']+d['beta']
    u=(S+2*w)/(S+w);K=2*m*s.exp(S+2*w-2*Q)
    gamma=s.Function('A')(S)**2/(2*d['Fz']);tau=2*s.exp(S-2*w)/m
    j=d['jumps'];F=s.factor(j['S_rr']+j['w_rr']);Psi=s.factor(-j['Q_rr']-j['w_rr'])
    predicted=dict(S_rr=-(2-u**2)*lam/(K*u**2)+gamma*lam/(2*V**2),
        w_rr=(1-u**2)*lam/(K*u**2)-gamma*lam/(2*V**2),
        Q_rr=gamma*lam/(2*V**2),q_r=-lam/(2*V),shear_r=lam/(4*V),beta_rr=-tau*lam/(4*V))
    errors={k:s.simplify(j[k]-value) for k,value in predicted.items()}
    errors['physical_lapse']=s.simplify(F+lam/(K*u**2))
    errors['physical_spatial']=s.simplify(Psi+(1-u**2)*lam/(K*u**2))
    # Proposed left-null certificates, verified against the actual six-row
    # matrix. These are not assigned ranks or evidence by assertion.
    left0=s.Matrix([[-2,1,0,0,0,0]])
    leftV=s.Matrix([[-1,1,-1,0,0,0]])
    zero0=left0*d['matrix'].subs(w,-S/2)
    zeroV=leftV*d['matrix'].subs(d['speed'],-d['beta'])
    errors.update({f'zero_u_left_null_{i}':s.simplify(v) for i,v in enumerate(zero0)})
    errors.update({f'zero_V_left_null_{i}':s.simplify(v) for i,v in enumerate(zeroV)})
    U,vv,L=s.symbols('u V L',real=True)
    chart={w:S*(U-1)/(2-U),d['speed']:vv-d['beta'],lam:U**2*vv**2*L}
    scaledF=s.simplify(F.subs(chart,simultaneous=True))
    scaledQ=s.simplify(j['Q_rr'].subs(chart,simultaneous=True))
    limitF=s.limit(scaledF,U,0);limitQ=s.limit(scaledQ,vv,0)
    return dict(definitions=dict(u=u,K=K,gamma=gamma,tau=tau,V=V),
        physical_lapse_jump=F,physical_spatial_jump=Psi,compact_jumps=predicted,
        compact_identity_errors=errors,
        zero_u_left_null_certificate=left0,zero_V_left_null_certificate=leftV,
        zero_u_reaction_coefficient=s.simplify((left0*d['rhs'])[0]/lam),
        zero_V_reaction_coefficient=s.simplify((leftV*d['rhs'])[0]/lam),
        bounded_jump_sufficient_scaling='lambda=u^2 V^2 L with bounded L, K away from zero and finite gamma,tau',
        scaled_physical_lapse=scaledF,scaled_spatial_metric_Q=scaledQ,
        scaled_physical_lapse_limit_error=s.simplify(limitF+vv**2*L/K.subs(w,-S/2)),
        scaled_spatial_metric_limit_error=s.simplify(limitQ-gamma*U**2*L/2),
        scope='Controls only these local transmission jumps; does not prove dynamics enforces lambda scaling, perturbative stability, or global rank preservation')


if __name__=='__main__':
    from ic43_weighted_multiplier import serial
    p=argparse.ArgumentParser();p.add_argument('--strict',action='store_true');args=p.parse_args()
    print(json.dumps(serial(dict(result=derive(),full_theory='OPEN')),indent=2))
    raise SystemExit(2 if args.strict else 0)
