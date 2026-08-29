import sys
sys.path.insert(0, '.')
import sympy as sp
import fc_alpha2_methodB_opt3 as M
P = lambda *a: print(*a, flush=True)
Uh=M.Uh; subU={M.Rk:-Uh/(4*sp.pi)}

def run(kbv,k2v,q0v,jyv, kill_a1=False, kill_chi=False):
    sub = {M.KB: sp.nsimplify(kbv), M.K2: sp.nsimplify(k2v), M.Q0: sp.nsimplify(q0v),
           M.JY: sp.nsimplify(jyv), M.GT: 1, M.kx: 1, M.ky: 0, M.kz: 0}
    G = dict(M.GAUGE)
    if kill_a1: G.update({M.ak[0]:0, M.ab[0]:0})
    if kill_chi: G.update({M.chik:0, M.chib:0})
    L = sp.expand(sp.expand(M.L2dc.subs(G)).subs(sub))
    BRAS=[b for b in M.BRAS if b not in G]; KETS=[k for k in M.KETS if k not in G]
    eqf = {A: sp.expand(sp.diff(L, A)) for A in BRAS}
    VZ = {M.Bk[1]:0, M.Bk[2]:0, M.ak[1]:0, M.ak[2]:0, M.hk[(2,3)]:0}
    # even (static) subset among remaining
    su=[k for k in [M.Psik,M.hk[(2,2)],M.hk[(3,3)],M.ak[0],M.chik] if k in KETS]
    sb=[b for b in [M.Psib,M.hb[(2,2)],M.hb[(3,3)],M.ab[0],M.chib] if b in BRAS]
    e0=[sp.expand(eqf[A].coeff(M.wb,0).subs(VZ)) for A in sb]
    s0s=M.lin_solve(e0,su)
    if s0s is None: return ('static-fail',)
    s0={**s0s}
    for k in [M.Bk[1],M.Bk[2],M.ak[1],M.ak[2],M.hk[(2,3)]]:
        if k in KETS: s0[k]=sp.S(0)
    d1={A:sp.Symbol(f'd1_{A}') for A in KETS}
    d2={A:sp.Symbol(f'd2_{A}') for A in KETS}
    subFull={A:s0[A]+M.wb*d1[A]+M.wb**2*d2[A] for A in KETS}
    eqW={A:sp.expand(eqf[A].subs(subFull)) for A in BRAS}
    e1=[sp.expand(eqW[A].coeff(M.wb,1)) for A in BRAS]
    Am,bm=sp.linear_eq_to_matrix(e1,list(d1.values()))
    r,ar=Am.rank(),Am.row_join(bm).rank()
    s1=M.lin_solve(e1,list(d1.values()))
    if s1 is None: return ('w1-fail', r, ar, len(d1))
    B2=sp.expand(d1[M.Bk[1]].subs(s1).subs(subU)); a1v=sp.cancel(2*B2.coeff(M.w2*Uh))
    # go to w^2 for alpha_2
    e2=[sp.expand(eqW[A].coeff(M.wb,2)).subs(s1) for A in BRAS]
    s2=M.lin_solve(e2,list(d2.values()))
    if s2 is None: return ('w2-fail', a1v)
    Psi2=sp.expand(d2[M.Psik].subs(s2).subs(subU))
    PA=sp.cancel(-2*Psi2.coeff(M.w2**2*Uh)); PAp=sp.cancel(-2*Psi2.coeff(M.w1**2*Uh))
    a2p=sp.cancel((PA+a1v)/2); a2l=sp.cancel(-(PAp-PA)/2)
    return ('ok', a1v, a2p, a2l)

for label,ka,kc in [("keep a1&chi",False,False),("a1=0",True,False),("chi=0",False,True)]:
    r=run(0.3,10.0,0.2,1.0, kill_a1=ka, kill_chi=kc)
    P(f"[{label}] -> {r}")
