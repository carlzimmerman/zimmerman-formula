#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_alpha2_aniso_numeric.py  --  NUMERIC fallback for the anisotropic alpha_2 solve.
Reuses the cached quadratic Lagrangian L2dc (built by fc_alpha2_anisotropic_solve_2026.py)
and does the order-by-order-in-wb solve with NUMERIC (K_B,K_2,Q_0,J_Y) so the 10-field
linsolve is trivial.  Reports alpha_1, and alpha_2 from BOTH channels over a param grid.
Purpose: if the symbolic solve is intractable, still deliver the verdict (magnitude +
the [D2] perp==par agreement).  Cache MUST exist (run the symbolic script far enough first).
"""
import sympy as sp, pickle, os, sys, itertools

CACHE = 'L2dc_aniso_cache.pkl'
if not os.path.exists(CACHE):
    print("no cache yet -- run the symbolic script until 'DC extracted + cached'"); sys.exit(2)
L2dc = pickle.load(open(CACHE, 'rb'))

# reconstruct the SAME symbols/amplitudes the symbolic script used (names must match)
eps, wb = sp.symbols('eps w_b', positive=True)
KB, Q0, K2, LAM, GT, JY = sp.symbols('K_B Q_0 K_2 Lambda G_t J_Y', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
kx, ky, kz = sp.symbols('k_x k_y k_z', real=True)
Es, Eis = sp.symbols('E_s E_is')
def kb_(t): return sp.Symbol(t+'k'), sp.Symbol(t+'b')
Psik,Psib = kb_('Psi')
Bk=[sp.Symbol(f'B{i+1}k') for i in range(3)]; Bb=[sp.Symbol(f'B{i+1}b') for i in range(3)]
hk={};hb={}
for (i,j) in [(1,1),(2,2),(3,3),(1,2),(1,3),(2,3)]:
    hk[(i,j)]=sp.Symbol(f'h{i}{j}k'); hb[(i,j)]=sp.Symbol(f'h{i}{j}b')
ak=[sp.Symbol(f'a{i+1}k') for i in range(3)]; ab=[sp.Symbol(f'a{i+1}b') for i in range(3)]
chik,chib = kb_('chi'); Rk,Rb = kb_('rho'); a0k,a0b = kb_('a0p')

GAUGE = {Bk[0]:0,Bb[0]:0, hk[(1,1)]:0,hb[(1,1)]:0, hk[(1,2)]:0,hb[(1,2)]:0, hk[(1,3)]:0,hb[(1,3)]:0}
L2dc = sp.expand(L2dc.subs(GAUGE))
BRAS = [Psib,Bb[1],Bb[2],hb[(2,2)],hb[(3,3)],hb[(2,3)],ab[0],ab[1],ab[2],chib]
KETS = [Psik,Bk[1],Bk[2],hk[(2,2)],hk[(3,3)],hk[(2,3)],ak[0],ak[1],ak[2],chik]
eq = {A: sp.expand(sp.diff(L2dc,A)) for A in BRAS}
Uh = sp.Symbol('U_hat')

def run(kbv,k2v,q0v,jyv):
    NUM = {ky:0,kz:0,kx:1,GT:1,LAM:0, KB:kbv,K2:k2v,Q0:q0v,JY:jyv}
    eqf = {A: sp.expand(eq[A].subs(NUM)) for A in BRAS}
    def lin(eqs,unk):
        M,b = sp.linear_eq_to_matrix(eqs,unk); s=list(sp.linsolve((M,b),unk))
        return dict(zip(unk,s[0])) if s else None
    VZ = {Bk[1]:0,Bk[2]:0,ak[1]:0,ak[2]:0,hk[(2,3)]:0}
    su = [Psik,hk[(2,2)],hk[(3,3)],ak[0],chik]
    e0 = [sp.expand(eqf[A].coeff(wb,0).subs(VZ)) for A in [Psib,hb[(2,2)],hb[(3,3)],ab[0],chib]]
    s0s = lin(e0,su)
    if s0s is None: return ('static-fail',None,None,None)
    s0 = {**s0s, Bk[1]:sp.S(0),Bk[2]:sp.S(0),ak[1]:sp.S(0),ak[2]:sp.S(0),hk[(2,3)]:sp.S(0)}
    d1={A:sp.Symbol(f'd1_{A}') for A in KETS}; d2={A:sp.Symbol(f'd2_{A}') for A in KETS}
    sub={A:s0[A]+wb*d1[A]+wb**2*d2[A] for A in KETS}
    eqW={A:sp.expand(eqf[A].subs(sub)) for A in BRAS}
    s1=lin([sp.expand(eqW[A].coeff(wb,1)) for A in BRAS], list(d1.values()))
    if s1 is None: return ('w1-fail',None,None,None)
    e2=[sp.expand(eqW[A].coeff(wb,2)).subs(s1) for A in BRAS]
    s2=lin(e2, list(d2.values()))
    if s2 is None: return ('w2-fail',None,None,None)
    kv=lambda A: sp.expand(s0[A]+wb*d1[A].subs(s1)+wb**2*d2[A].subs(s2))
    subU={Rk:-Uh/(4*sp.pi)}
    b2=sp.expand(kv(Bk[1]).coeff(wb,1).subs(subU)); a1=sp.cancel(2*b2.coeff(w2*Uh))
    ps2=sp.expand(kv(Psik).coeff(wb,2).subs(subU))
    PA=sp.cancel(-2*ps2.coeff(w2**2*Uh)); PApar=sp.cancel(-2*ps2.coeff(w1**2*Uh))
    a2p=sp.cancel((PA+a1)/2); a2l=sp.cancel(-(PApar-PA)/2)
    return ('ok', complex(a1), complex(a2p), complex(a2l))

print(f"{'K_B':>6} {'K2':>6} {'Q0':>5} {'JY':>4} | {'alpha_1':>12} {'a2_perp':>14} {'a2_par':>14}  D2")
for kbv,k2v,q0v,jyv in itertools.product([0.05,0.3],[10.0,300.0],[0.2,0.9],[1.0,2.0]):
    st,a1,a2p,a2l = run(kbv,k2v,q0v,jyv)
    if st!='ok':
        print(f"{kbv:6} {k2v:6} {q0v:5} {jyv:4} | {st}"); continue
    d2diff = abs(a2p-a2l)
    print(f"{kbv:6} {k2v:6} {q0v:5} {jyv:4} | {a1.real:12.5f} {a2p.real:14.6g} {a2l.real:14.6g}  {'OK' if d2diff<1e-7 else f'DIFF={d2diff:.1e}'}")
