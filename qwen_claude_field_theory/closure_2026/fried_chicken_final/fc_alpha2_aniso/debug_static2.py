import sys
sys.path.insert(0, '.')
import sympy as sp
import fc_alpha2_methodB_opt3 as M
P = lambda *a: print(*a, flush=True)
Uh=M.Uh; subU={M.Rk:-Uh/(4*sp.pi)}
KB,K2,Q0,JY = M.KB,M.K2,M.Q0,M.JY
mP2 = K2*Q0**2/(2-KB)

def static(kill):
    sub = {M.GT:1, M.kx:1, M.ky:0, M.kz:0}
    G=dict(M.GAUGE); G.update(kill)
    L = sp.expand(sp.expand(M.L2dc.subs(G)).subs(sub))
    BRAS=[b for b in M.BRAS if b not in G]; KETS=[k for k in M.KETS if k not in G]
    eqf={A:sp.expand(sp.diff(L,A)) for A in BRAS}
    VZ={M.Bk[1]:0,M.Bk[2]:0,M.ak[1]:0,M.ak[2]:0,M.hk[(2,3)]:0}
    su=[k for k in [M.Psik,M.hk[(2,2)],M.hk[(3,3)],M.ak[0],M.chik] if k in KETS]
    sb=[b for b in [M.Psib,M.hb[(2,2)],M.hb[(3,3)],M.ab[0],M.chib] if b in BRAS]
    e0=[sp.expand(eqf[A].coeff(M.wb,0).subs(VZ)) for A in sb]
    # use a raw matrix solve so we can see rank
    Am,bm=sp.linear_eq_to_matrix(e0,su)
    P(f"  static matrix {Am.shape} rank {Am.rank()} aug {Am.row_join(bm).rank()}")
    s0=M.lin_solve(e0,su)
    if s0 is None: P("  static-fail"); return
    Psis=sp.cancel(s0[M.Psik].subs(subU))
    h22s=sp.cancel(s0[M.hk[(2,2)]].subs(subU))
    chis=sp.cancel(s0[M.chik].subs(subU)) if M.chik in s0 else 'killed'
    P(f"  Psi_static={sp.simplify(Psis)}")
    P(f"  gamma=-h22/(2Psi)={sp.simplify(-h22s/(2*Psis))}")
    P(f"  chi_static={sp.simplify(chis) if chis!='killed' else 'killed'}")
    expect = Uh/(1-KB/2)/(1+mP2)
    P(f"  Psi/expected(typeII)={sp.simplify(Psis/expect)}")

P("=== keep a1, keep chi (default) ==="); static({})
P("=== a1=0 ==="); static({M.ak[0]:0,M.ab[0]:0})
P("=== chi=0 ==="); static({M.chik:0,M.chib:0})
