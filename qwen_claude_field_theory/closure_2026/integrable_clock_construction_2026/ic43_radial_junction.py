"""Actual IC30 spatial interface flux, including its exceptional zero-u locus."""
import argparse
from functools import lru_cache
import json
import sympy as s
import ic30_radial_bridge as radial


@lru_cache(None)
def derive():
    d=radial.radial_action();r=d['r'];S,w,Q,q,z,sh,beta,ell=d['fields']
    fields=[S,w,Q];gradients=[s.diff(f,r) for f in fields]
    # Separate the shift-advection term: it is linear in gradients and does
    # not contribute to a derivative jump at continuous fields and momenta.
    H=s.hessian(d['L'],gradients).applyfunc(s.simplify)
    amplitude=s.Symbol('jump',real=True);jump=s.Matrix([-amplitude,amplitude,-amplitude])
    flux=[s.simplify(v) for v in H*jump]
    F1,Psi1,u=s.symbols('F1 Psi1 u',real=True)
    a=s.Symbol('w1',real=True)
    kinetic=(s.Matrix(gradients).T*H*s.Matrix(gradients))[0]/2
    transformed=kinetic.subs(dict(zip(gradients,[F1-a,a,-Psi1-a])),simultaneous=True)
    desired=d['m']*r**2*s.exp(S+2*w+Q)*(Psi1**2-2*F1*Psi1+(1-d['u']**2)*F1**2)
    check=s.simplify(transformed-desired)
    # The independent (S,Q) minor controls the generic rank alongside the
    # computed null vector. u=0 means S+2w=0; exclude S+w=0 from this chart.
    minor=s.factor(H.extract([0,2],[0,2]).det())
    rank=H.rank();zero=H.subs(w,-S/2).applyfunc(s.simplify)
    return dict(field_order=['S','w','Q'],spatial_hessian=H,
        generic_rank=rank,independent_minor=minor,zero_u_hessian=zero,zero_u_rank=zero.rank(),
        auxiliary_flux_jump=flux,physical_lapse_jump=s.simplify(jump[0]+jump[1]),
        physical_spatial_jump=s.simplify(jump[2]+jump[1]),physical_gradient_identity=check,
        time_momentum_Q=s.diff(d['L'],d['Qdot']),
        scope='Spatial variational junction test at continuous fields, shift and momenta; not full dynamical or Dirac closure')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--strict',action='store_true');a=p.parse_args()
    from ic43_weighted_multiplier import serial
    print(json.dumps(serial(dict(result=derive(),full_theory='OPEN')),indent=2))
    raise SystemExit(2 if a.strict else 0)
