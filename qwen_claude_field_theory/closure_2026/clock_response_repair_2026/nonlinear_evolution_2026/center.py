#!/usr/bin/env python3
"""Exact regular-origin limit; no extrapolation of singular evolution rates."""
from functools import lru_cache
import json
import numpy as np
import sympy as s
from equations import derive


@lru_cache(maxsize=1)
def center_expressions():
    raw=derive()["evolution_equations"]
    byname={str(z):z for e in raw for z in e.free_symbols}
    x=s.symbols("radius_limit",positive=True)
    ac,A2,b2,Kc,Qc,Q2,u1,Nc,N2,Hd,Qd=s.symbols("a_c A2 b2 K_c Q_c Q2 u1 N_c N2 Hdot_c Qdot_c",real=True)
    replacement=dict(A=ac+A2*x*x/2,Ar=A2*x,R=ac*x+b2*x**3/2,
                     Rr=ac+3*b2*x*x/2,Rrr=3*b2*x,k=Kc,h=Kc,kr=0,hr=0,
                     Q=Qc+Q2*x*x/2,Qr=Q2*x,Qrr=Q2,cr=u1*x,crr=u1,w=0,
                     N=Nc+N2*x*x/2,Nr=N2*x,Nrr=N2,kd=Hd,hd=Hd,Qd=Qd)
    sub={byname[key]:value for key,value in replacement.items() if key in byname}
    expressions=s.Matrix([s.limit(s.cancel(raw[i].subs(sub,simultaneous=True)),x,0) for i in (0,2,3)])
    coefficients,constant=s.linear_eq_to_matrix(expressions,[Hd,Qd,N2,Nc])
    matrix=coefficients[:,:3];rhs=(-coefficients[:,3]).row_join(constant)
    return matrix,rhs


@lru_cache(maxsize=1)
def compiled_center():
    matrix,rhs=center_expressions();flat=list(matrix)+list(rhs)
    args=sorted(set().union(*(x.free_symbols for x in flat)),key=str)
    return [str(x) for x in args],s.lambdify(args,flat,"numpy",cse=True)


def evaluate_center(values):
    names,func=compiled_center()
    flat=np.asarray(func(*(values[n] for n in names)),dtype=float)
    return flat[:9].reshape(3,3),flat[9:].reshape(3,2)


if __name__=="__main__":
    matrix,rhs=center_expressions()
    print(json.dumps({"scope":"exact spherical regular-origin limit",
                      "matrix":[[str(x) for x in row] for row in matrix.tolist()],
                      "rhs":[[str(x) for x in row] for row in rhs.tolist()]},indent=2))
