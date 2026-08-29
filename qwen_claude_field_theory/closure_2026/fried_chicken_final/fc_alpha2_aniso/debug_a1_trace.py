import sys
sys.path.insert(0, '.')
import sympy as sp
import fc_alpha2_methodB_opt3 as M
P = lambda *a: print(*a, flush=True)
Uh=M.Uh; subU={M.Rk:-Uh/(4*sp.pi)}

def alpha1_variants(kbv,k2v,q0v,jyv, killfield):
    sub = {M.KB: sp.nsimplify(kbv), M.K2: sp.nsimplify(k2v), M.Q0: sp.nsimplify(q0v),
           M.JY: sp.nsimplify(jyv), M.GT: 1, M.kx: 1, M.ky: 0, M.kz: 0}
    G=dict(M.GAUGE); G.update(killfield)
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
    Psi_s = sp.cancel(s0[M.Psik].subs(subU))
    d1={A:sp.Symbol(f'd1_{A}') for A in KETS}; d2={A:sp.Symbol(f'd2_{A}') for A in KETS}
    subFull={A:s0[A]+M.wb*d1[A]+M.wb**2*d2[A] for A in KETS}
    eqW={A:sp.expand(eqf[A].subs(subFull)) for A in BRAS}
    e1=[sp.expand(eqW[A].coeff(M.wb,1)) for A in BRAS]
    s1=M.lin_solve(e1,list(d1.values()))
    if s1 is None: return None
    B2=sp.expand(d1[M.Bk[1]].subs(s1).subs(subU))
    B3=sp.expand(d1[M.Bk[2]].subs(s1).subs(subU))
    # raw coeff of w2*Uh in H02, and w3*Uh in H03 (should match by symmetry)
    cB2 = sp.cancel(B2.coeff(M.w2*Uh)); cB3 = sp.cancel(B3.coeff(M.w3*Uh))
    a1_Uh = sp.cancel(2*cB2)                      # extraction vs bare Uh
    a1_Psi = sp.cancel(2*cB2*Uh/Psi_s)            # extraction vs actual Newtonian potential Psi_static
    return a1_Uh, a1_Psi, sp.cancel(Psi_s/Uh), sp.simplify(cB2-cB3)

for (kb,k2,q0,jy) in [(0.3,10.,0.2,1.),(0.05,10.,0.2,1.),(0.3,300.,0.9,2.),(0.3,10.,0.9,1.),(0.3,10.,0.2,2.)]:
    r = alpha1_variants(kb,k2,q0,jy, {M.chik:0,M.chib:0})
    if r is None: P(f"KB={kb} K2={k2} Q0={q0} JY={jy}: FAIL"); continue
    a1u,a1p,c,sym = r
    P(f"KB={kb} K2={k2} Q0={q0} JY={jy}: a1(vs Uh)={a1u}  a1(vs Psi_static)={a1p}  Psi/Uh={c}  (target -4KB={-4*kb})  B2==B3sym:{sym==0}")
