import sys
sys.path.insert(0, '.')
import sympy as sp
import fc_alpha2_methodB_opt3 as M
P = lambda *a: print(*a, flush=True)
Uh=M.Uh; subU={M.Rk:-Uh/(4*sp.pi)}
K2s=M.K2

def alpha1_symK2(kbv,q0v,jyv, kill):
    sub = {M.KB: sp.nsimplify(kbv), M.Q0: sp.nsimplify(q0v), M.JY: sp.nsimplify(jyv),
           M.GT: 1, M.kx: 1, M.ky: 0, M.kz: 0}   # K2 symbolic
    G=dict(M.GAUGE); G.update(kill)
    L = sp.expand(sp.expand(M.L2dc.subs(G)).subs(sub))
    BRAS=[b for b in M.BRAS if b not in G]; KETS=[k for k in M.KETS if k not in G]
    eqf={A:sp.expand(sp.diff(L,A)) for A in BRAS}
    VZ={M.Bk[1]:0,M.Bk[2]:0,M.ak[1]:0,M.ak[2]:0,M.hk[(2,3)]:0}
    su=[k for k in [M.Psik,M.hk[(2,2)],M.hk[(3,3)],M.ak[0],M.chik] if k in KETS]
    sb=[b for b in [M.Psib,M.hb[(2,2)],M.hb[(3,3)],M.ab[0],M.chib] if b in BRAS]
    e0=[sp.expand(eqf[A].coeff(M.wb,0).subs(VZ)) for A in sb]
    s0s=M.lin_solve(e0,su)
    if s0s is None: return None
    s0={**s0s}
    for k in [M.Bk[1],M.Bk[2],M.ak[1],M.ak[2],M.hk[(2,3)]]:
        if k in KETS: s0[k]=sp.S(0)
    d1={A:sp.Symbol(f'd1_{A}') for A in KETS}
    subFull={A:s0[A]+M.wb*d1[A] for A in KETS}
    eqW={A:sp.expand(eqf[A].subs(subFull)) for A in BRAS}
    e1=[sp.expand(eqW[A].coeff(M.wb,1)) for A in BRAS]
    s1=M.lin_solve(e1,list(d1.values()))
    if s1 is None: return None
    B2=sp.expand(d1[M.Bk[1]].subs(s1).subs(subU))
    a1=sp.cancel(2*B2.coeff(M.w2*Uh))
    return a1

for (kb,q0,jy) in [(0.3,0.2,1.0),(0.05,0.2,1.0),(0.3,0.9,2.0)]:
    for kill,label in [({M.chik:0,M.chib:0},'chi=0'),({M.ak[0]:0,M.ab[0]:0},'a1=0')]:
        a1=alpha1_symK2(kb,q0,jy,kill)
        if a1 is None: P(f"KB={kb} Q0={q0} JY={jy} [{label}]: FAIL"); continue
        a1=sp.cancel(a1)
        heavy=sp.limit(a1,K2s,sp.oo); light=sp.limit(a1,K2s,0)
        P(f"KB={kb} Q0={q0} JY={jy} [{label}]: alpha_1(K2->oo)={heavy}  alpha_1(K2->0)={light}  target(-4KB)={-4*kb}")
        P(f"        alpha_1(K2) = {a1}")
