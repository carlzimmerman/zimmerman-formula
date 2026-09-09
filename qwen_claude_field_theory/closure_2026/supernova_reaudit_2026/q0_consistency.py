#!/usr/bin/env python3
"""Conditional background consistency, NOT a new IC-action cosmology."""
import json
from functools import lru_cache
import sympy as sp


@lru_cache(None)
def derive():
    G, c, H, a, rm, rd = sp.symbols('G c H a0 rho_m rho_DE', positive=True)
    w = sp.symbols('w_DE', real=True)
    # Flat GR Friedmann and acceleration equations; dust plus chosen DE fluid.
    friedmann = 8*sp.pi*G*(rm+rd)/3
    acceleration = -4*sp.pi*G*(rm+(1+3*w)*rd)/3
    density_tie = sp.Eq(a*a, c*c*G*rd/4)
    rd_solution = sp.solve(density_tie, rd)[0]
    rm_solution = sp.solve(sp.Eq(H*H, friedmann), rm)[0]
    q_general = sp.factor((-acceleration/H**2).subs(rm, rm_solution).subs(rd, rd_solution))
    q_eliminated = sp.factor(q_general.subs(w, -1))
    q_direct = sp.factor((-acceleration/friedmann).subs(w, -1)
                         .subs(rm, rm_solution).subs(rd, rd_solution))
    roots = sp.solve(sp.Eq(q_eliminated, 0), a)
    if len(roots) != 1:
        raise ValueError('Positive-acceleration-scale boundary is not unique')
    return dict(G=G,c=c,H=H,a=a,w=w,q_direct=q_direct,
                q_eliminated=q_eliminated,q_general=q_general,
                a_critical=roots[0],rho_m=sp.factor(rm_solution.subs(rd,rd_solution)))


def report():
    d = derive()
    mpc = sp.Rational('3.0856775814913673e22')
    rows = []
    for h0 in ('67.4','73.0'):
        common = {d['c']:299792458,d['H']:sp.Rational(h0)*1000/mpc}
        rows.append(dict(H0_km_s_Mpc=h0,
                         largest_a0_for_q0_nonnegative=str(sp.N(d['a_critical'].subs(common),20)),
                         q0_at_input_a0_9p4e_minus11=str(sp.N(d['q_eliminated'].subs(common)
                                                             .subs(d['a'],sp.Rational('9.4e-11')),20))))
    return dict(assumptions=['GR Friedmann and acceleration equations',
                            'Flat background; pressureless matter; radiation neglected at the epoch',
                            'Posited a0=c sqrt(G rho_DE)/2',
                            'w_DE=-1 for the numerical constant-Lambda rows'],
                q0_constant_Lambda=str(d['q_eliminated']),
                q0_general_DE=str(d['q_general']),
                largest_a0_for_deceleration=str(d['a_critical']),rows=rows,
                nonclaims=['No reproduction or adjudication of Sarkar age/frame likelihood',
                           'No IC13/IC14 cosmology is inferred',
                           'Not a new independent law: algebraic consequence of stated assumptions',
                           'Changing expansion dynamics or DE equation of state changes this test'])


if __name__ == '__main__':
    print(json.dumps(report(),indent=2))
