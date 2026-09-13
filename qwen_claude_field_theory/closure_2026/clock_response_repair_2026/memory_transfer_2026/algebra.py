#!/usr/bin/env python3
"""Legendre transform, memory generator, and determinant derivative: exact algebra."""
import json
import sympy as s


def derive():
    A,B,D,fv,fu,C,u,v,p=s.symbols('A B D fv fu C u v p',real=True)
    L=A*v*v/2+B*u*v+D*u*u/2+C*(fv*v+fu*u)
    momentum=s.diff(L,v)
    velocity=s.solve(p-momentum,v)[0]
    Ham=s.factor((p*v-L).subs(v,velocity))
    rhs=s.Matrix([s.diff(Ham,p),-s.diff(Ham,u)])
    F=rhs.jacobian([u,p]);b=rhs.subs({u:0,p:0})
    w,x,y,z=s.symbols('w x y z',real=True);matrix=s.Matrix([[w,x],[y,z]])
    rate=F*matrix
    detrate=s.expand(sum(s.diff(matrix.det(),a)*r for a,r in zip(matrix,rate)))
    Om=s.Matrix([[0,1],[-1,0]])
    # Independently verify Hamiltonian inverse evolution and source cancellation.
    checks=dict(legendre_velocity=s.factor(s.diff(Ham,p)-velocity)==0,
        generator_trace=s.factor(s.trace(F))==0,
        symplectic_generator=all(s.factor(x)==0 for x in F.T*Om+Om*F),
        determinant_derivative=s.factor(detrate)==0,
        affine_decomposition=all(s.factor(x)==0 for x in rhs-F*s.Matrix([u,p])-b),
        common_source_difference=all(s.factor(x)==0 for x in rhs-rhs.subs(C,0)-b))
    if not all(checks.values()):raise AssertionError(checks)
    return dict(checks=checks,Lagrangian=str(L),Hamiltonian=str(Ham),
        generator=str(F),forcing=str(b),
        scope='A!=0; one reduced Fourier mode; ODE existence/uniqueness hypotheses are separate')


if __name__=='__main__':print(json.dumps(derive(),indent=2))
