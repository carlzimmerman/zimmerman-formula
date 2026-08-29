#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_solveB_setupM.py  --  ROUTE B PART B: scalar contribution Delta alpha_2^(phiA), INDEPENDENT
moving-source (Setup M) 1PN solve.  Efficient single-variable (k=zhat) mode.
====================================================================================================
SETUP M: aether AT REST A^mu=(1,0,0,0), phi=Q0 t (Q=Q0,Y=0), flat metric.  SOURCE MOVES at
w=(wx,0,wz) with rigid retardation omega=k.w.  k=zhat (kz=1): omega=wz.  d_0=-i wz, d_3=i, d_1=d_2=0.
wz = PARALLEL, wx = PERP.  Boost-conjugate of route-A (Setup S) => same alpha_1,alpha_2 (the check).
Even-y sector (w has no y-comp): fields H00,H01,H03,H11,H13,H33,H22, a1(=a_x), a3(=a_z), chi; a0 by A.A=-1.

METRIC in HARMONIC form: L_EH=(1/4)d_l h_mn d^l h^mn -(1/8)d_l h d^l h  => all comps dynamical,
2b+d directly readable (fc_aniso_grgate.py method).  Frozen action with c2star(div A)^2, K(Q)=K2(Q-Q0)^2.

EXTRACTION (k=zhat): g_0x=H01 (perp), g_0z=H03 (par); g_00 O(w^2) perp=wx^2, par=wz^2.
  A_V=coeff(H01,wx U); A_V+A_W=coeff(H03,wz U); a=A_V+A_W/2, b=-A_W/2.
  cF=coeff(H00,wx^2 U); cF+dF=coeff(H00,wz^2 U); c=cF+dF/2, d=-dF/2.  gamma=H11_static/H00_static.
  alpha_1=-2(a+b)-(4gamma+4)=-2 A_V-(4gamma+4);  alpha_2=-(2b+d)-1  (gauge-invariant).
  Carl channels: Psi=-H00/2; P_A=-2[wx^2 U]Psi (iso v^2U), P_Apar=-2[wz^2 U]Psi;
                 a2_iso=(P_A+alpha1)/2, a2_aniso=-(P_Apar-P_A)/2.
GATES: [G-GR] all-off=>0. [G-gam] gamma=1. [G-vec] scalar off,c2star on=>alpha1=-4KB,alpha2=0.
"""
import sympy as sp, time, sys

T0 = time.time()
P = lambda *a: print(*a, flush=True)
I = sp.I
eta = sp.diag(-1, 1, 1, 1)
eps = sp.Symbol('eps', positive=True)
wx, wz = sp.symbols('wx wz', real=True)
Es, Eis = sp.symbols('E_s E_is')
Uh = sp.Symbol('U_hat')

# k=zhat.  Setup M (moving source): omega=wz => K_mu=(-wz,0,0,1).
# Setup S (boosted aether, static source): static => K_mu=(0,0,0,1).
KV = [-wz, 0, 0, 1]
def d(f, mu):
    return sp.diff(f, Es)*(I*KV[mu]*Es) + sp.diff(f, Eis)*(-I*KV[mu]*Eis)

def wtrunc(e):
    e = sp.expand(e); out = 0
    for i in range(3):
        ci = e.coeff(wx, i)
        for j in range(3-i):
            out += ci.coeff(wz, j)*wx**i*wz**j
    return sp.expand(out)

def te(e):
    e = sp.expand(e); out = 0
    for a in range(3):
        out += wtrunc(e.coeff(eps, a))*eps**a
    return sp.expand(out)

def nf(tag):
    kk = sp.Symbol(tag+'k'); bb = sp.Symbol(tag+'b'); return kk*Es + bb*Eis, kk, bb

# fields (even-y): metric 7, aether a1,a3, scalar chi ; a0 from constraint
MIDX = [(0,0),(0,1),(0,3),(1,1),(1,3),(3,3),(2,2)]
Hf = {}; Hk = {}; Hb = {}
for ij in MIDX:
    f, kk, bb = nf(f'H{ij[0]}{ij[1]}'); Hf[ij] = f; Hf[(ij[1],ij[0])] = f; Hk[ij] = kk; Hb[ij] = bb
a1f, a1k, a1b = nf('ax')     # a_x
a3f, a3k, a3b = nf('az')     # a_z
chi, chik, chib = nf('chi')
rho, Rk, Rb = nf('rho')
a0f0, a0k, a0b = nf('a0p')

def build(KBv, K2v, Q0v, JYv, use_c2star=True, scalar_on=True, gr_only=False, c2_val=None, Jcoup=1,
          setupS=False):
    global KV
    KV = [0, 0, 0, 1] if setupS else [-wz, 0, 0, 1]     # static (Setup S) vs retarded (Setup M)
    KB = sp.nsimplify(KBv); K2 = sp.nsimplify(K2v); Q0 = sp.nsimplify(Q0v); JY = sp.nsimplify(JYv)
    Jc = sp.nsimplify(Jcoup)   # multiplier on the 2(2-K_B)J.dphi coupling (1=on, 0=off) for diagnosis
    c2star = KB/(1 - 2*KB) if use_c2star else sp.S(0)
    if c2_val is not None:
        c2star = sp.nsimplify(c2_val)
    if gr_only:
        KB = sp.S(0); c2star = sp.S(0); Q0 = sp.S(0); scalar_on = False

    H = sp.zeros(4, 4)
    for ij in MIDX:
        H[ij[0], ij[1]] = Hf[ij]; H[ij[1], ij[0]] = Hf[ij]
    Hup = eta*H*eta
    trH = sum(eta[m, n]*H[m, n] for m in range(4) for n in range(4))

    def dd(f, g):   # d_l f d^l g = -d_0 f d_0 g + d_3 f d_3 g
        return -d(f, 0)*d(g, 0) + d(f, 3)*d(g, 3)
    # harmonic-gauge EH = Fierz-Pauli of R in de Donder gauge = -(1/4)(dh)^2+(1/8)(dtrh)^2
    # (SAME sign as route-A's (1/2)h G1, so the dark sector's relative sign is correct)
    L_EH = (-sp.Rational(1, 4)*sum(dd(H[m, n], Hup[m, n]) for m in range(4) for n in range(4))
            + sp.Rational(1, 8)*dd(trH, trH))

    # matter source. Setup M: moving dust u=gamma(1,w). Setup S: static dust u=(1,0,0,0).
    gam = 1 + (wx**2 + wz**2)/2
    u = [1, 0, 0, 0] if setupS else [gam, gam*wx, 0, gam*wz]
    hT = sum(H[m, n]*u[m]*u[n] for m in range(4) for n in range(4))
    L2_matt = -4*sp.pi*wtrunc(rho*hT)

    if gr_only:
        L2 = sp.expand(wtrunc(L_EH) + L2_matt)
    else:
        gd = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps*H[m, n])
        gu = sp.Matrix(4, 4, lambda a, b: (eta - eps*Hup + eps**2*(Hup*H*eta))[a, b])
        HH = sum(Hup[m, n]*H[m, n] for m in range(4) for n in range(4))
        sqg = 1 + eps*trH/2 + eps**2*(trH**2/8 - HH/4)
        # Setup M: aether at rest. Setup S: aether BOOSTED at w (source static) -- route-A frame.
        if setupS:
            Aup_bg = sp.Matrix([1 + (wx**2 + wz**2)/2, wx, 0, wz])
        else:
            Aup_bg = sp.Matrix([1, 0, 0, 0])
        Adn_bg = eta*Aup_bg
        a0f = a0f0
        Adn = sp.Matrix([Adn_bg[0] - eps*a0f, Adn_bg[1] + eps*a1f, Adn_bg[2] + 0, Adn_bg[3] + eps*a3f])
        Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
        C1 = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
        solA = sp.solve([sp.expand(C1).coeff(Es, 1), sp.expand(C1).coeff(Eis, 1)], [a0k, a0b], dict=True)[0]
        a0f = a0f.subs(solA)
        Adn = sp.Matrix([Adn_bg[0] - eps*a0f, Adn_bg[1] + eps*a1f, Adn_bg[2] + 0, Adn_bg[3] + eps*a3f])
        Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
        dphi_bg = -Q0*Adn_bg
        dphi = sp.Matrix([dphi_bg[m] + eps*d(chi, m) for m in range(4)])
        gdT = sp.Matrix(4, 4, lambda m, n: te(gd[m, n]))
        guT = sp.Matrix(4, 4, lambda m, n: te(gu[m, n]))
        AupT = sp.Matrix(4, 1, lambda i, j: te(Aup[i]))
        dphiT = sp.Matrix(4, 1, lambda i, j: te(dphi[i]))
        GamT = [[[te(sp.Rational(1, 2)*sum(guT[r, s]*(d(gdT[s, n], m)+d(gdT[s, m], n)-d(gdT[m, n], s))
                 for s in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]
        Fmn = sp.Matrix(4, 4, lambda m, n: sp.expand(d(Adn[n], m) - d(Adn[m], n)))
        F1 = sp.Matrix(4, 4, lambda m, n: Fmn[m, n].coeff(eps, 1))
        F2 = eps**2*sum(F1[m, n]*F1[a, b]*eta[m, a]*eta[n, b]
                        for m in range(4) for n in range(4) for a in range(4) for b in range(4))
        sqgA = [te(te(sqg)*AupT[m]) for m in range(4)]
        divA = te(sum(d(sqgA[m], m) for m in range(4)))
        divA1 = divA.coeff(eps, 1)
        C2term = eps**2*c2star*divA1**2
        Jup = [te(sum(AupT[nu]*(d(AupT[al], nu) + sum(GamT[al][nu][r]*AupT[r] for r in range(4)))
                 for nu in range(4))) for al in range(4)]
        Jdphi = te(sum(Jup[m]*dphiT[m] for m in range(4)))
        Qc = te(sum(AupT[m]*dphiT[m] for m in range(4)))
        Yc = te(sum((guT[m, n] + AupT[m]*AupT[n])*dphiT[m]*dphiT[n] for m in range(4) for n in range(4)))
        Kcal = K2*te((Qc - Q0)**2)                # K_cal(Q) (Lambda->0); action term is +2 K_cal
        def grade(e):
            e = sp.expand(e); return [wtrunc(e.coeff(eps, n)) for n in range(3)]
        gF2 = grade(F2); gC2 = grade(C2term); gsq = grade(sqg)
        if scalar_on:
            gJ = grade(Jdphi); gY = grade(Yc); gK = grade(Kcal)
            # SZ21-correct signs: -F_cal ⊃ +2 K_cal ; time-kinetic +2K2 chi_dot^2 (healthy, NOT ghost).
            darkS = [-(KB/2)*gF2[n] + gC2[n] + Jc*2*(2-KB)*gJ[n] - (2-KB)*(1+JY)*gY[n] + 2*gK[n]
                     for n in range(3)]
        else:
            darkS = [-(KB/2)*gF2[n] + gC2[n] for n in range(3)]
        L2_dark = wtrunc(sum(gsq[a]*darkS[2-a] for a in range(3)))
        L2 = sp.expand(wtrunc(L_EH) + L2_dark + L2_matt)

    pol = sp.Poly(L2, Es, Eis); L2dc = 0
    for mon, cc in zip(pol.monoms(), pol.coeffs()):
        if mon[0] == mon[1]:
            L2dc += cc*(Es*Eis)**mon[0]
    return sp.expand(L2dc.subs(Es*Eis, 1))


def solve(KBv, K2v, Q0v, JYv, use_c2star=True, scalar_on=True, gr_only=False, c2_val=None, Jcoup=1,
          setupS=False):
    L2dc = build(KBv, K2v, Q0v, JYv, use_c2star, scalar_on, gr_only, c2_val, Jcoup, setupS)
    KETS = [Hk[ij] for ij in MIDX] + [a1k, a3k] + ([chik] if scalar_on else [])
    BRAS = [Hb[ij] for ij in MIDX] + [a1b, a3b] + ([chib] if scalar_on else [])
    eqf = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}

    def lin(eqs, unk):
        M, b = sp.linear_eq_to_matrix(eqs, unk)
        s = list(sp.linsolve((M, b), unk))
        return dict(zip(unk, s[0])) if s else None
    def w0(e):
        return sp.expand(e).coeff(wx, 0).coeff(wz, 0)

    # static (w=0): perp-odd fields (H01,H13,a1) vanish; solve even block
    perp_odd = [Hk[(0, 1)], Hk[(1, 3)], a1k]
    VZ = {kk: 0 for kk in perp_odd}
    even_b = [Hb[(0, 0)], Hb[(1, 1)], Hb[(3, 3)], Hb[(2, 2)], Hb[(0, 3)]] + ([chib] if scalar_on else []) + [a3b]
    even_k = [Hk[(0, 0)], Hk[(1, 1)], Hk[(3, 3)], Hk[(2, 2)], Hk[(0, 3)]] + ([chik] if scalar_on else []) + [a3k]
    e0 = [w0(eqf[A].subs(VZ)) for A in even_b]
    s0s = lin(e0, even_k)
    if s0s is None:
        return ('static-fail',)
    s0 = {**s0s, **{kk: sp.S(0) for kk in perp_odd}}

    mons2 = [('xx', wx*wx), ('zz', wz*wz), ('xz', wx*wz)]
    lin1 = {A: sp.Symbol(f'{A}_1x')*wx + sp.Symbol(f'{A}_1z')*wz for A in KETS}
    lin2 = {A: sum(sp.Symbol(f'{A}_2{tg}')*vv for tg, vv in mons2) for A in KETS}
    sub = {A: s0[A] + lin1[A] + lin2[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(sub)) for A in BRAS}

    def cwdeg(e, deg):
        e = sp.expand(e); out = []
        if deg == 1:
            out.append(w0(e.coeff(wx, 1))); out.append(w0(e.coeff(wz, 1))); return out
        for tg, vv in mons2:
            if tg == 'xz':
                out.append(w0(e.coeff(wx, 1).coeff(wz, 1)))
            else:
                out.append(w0(e.coeff(vv, 1)))
        return out

    unk1 = [sp.Symbol(f'{A}_1{v}') for A in KETS for v in ('x', 'z')]
    eq1 = []
    for A in BRAS:
        eq1 += cwdeg(eqW[A], 1)
    s1 = lin(eq1, unk1)
    if s1 is None:
        return ('w1-fail',)
    unk2 = [sp.Symbol(f'{A}_2{tg}') for A in KETS for tg, _ in mons2]
    eq2 = []
    for A in BRAS:
        eq2 += [sp.expand(e).subs(s1) for e in cwdeg(eqW[A], 2)]
    s2 = lin(eq2, unk2)
    if s2 is None:
        return ('w2-fail',)

    def kv(A):
        val = s0[A] + s1[sp.Symbol(f'{A}_1x')]*wx + s1[sp.Symbol(f'{A}_1z')]*wz
        val += sum(s2[sp.Symbol(f'{A}_2{tg}')]*vv for tg, vv in mons2)
        return sp.expand(val)

    subU = {Rk: -Uh/(4*sp.pi)}
    H00s = w0(kv(Hk[(0, 0)])).subs(subU)
    H11s = w0(kv(Hk[(1, 1)])).subs(subU)
    Uref = sp.simplify(H00s/2)                 # define U from the actual static potential g_00=2U
    gamma = sp.simplify(H11s/H00s)             # g_ij=2 gamma U delta ; = H11s/(2 Uref)=H11s/H00s
    H01 = sp.expand(kv(Hk[(0, 1)])).subs(subU)
    H03 = sp.expand(kv(Hk[(0, 3)])).subs(subU)
    A_V = sp.simplify(H01.coeff(wx, 1).coeff(wz, 0)/Uref)
    AVpAW = sp.simplify(H03.coeff(wz, 1).coeff(wx, 0)/Uref)
    A_W = A_V - AVpAW if False else AVpAW - A_V
    aa = A_V + A_W/2; bb = -A_W/2
    H00_2 = sp.expand(kv(Hk[(0, 0)])).subs(subU)
    cF = sp.simplify(H00_2.coeff(wx, 2).coeff(wz, 0)/Uref)
    cFpdF = sp.simplify(H00_2.coeff(wz, 2).coeff(wx, 0)/Uref)
    dF = cFpdF - cF
    dd_ = -dF/2
    a1v = sp.simplify(-2*(aa + bb) - (4*gamma + 4))
    a2v = sp.simplify(-(2*bb + dd_) - 1)
    Psi2 = sp.expand(-H00_2/2)
    PA = sp.simplify(-2*Psi2.coeff(wx, 2).coeff(wz, 0)/Uref)
    PApar = sp.simplify(-2*Psi2.coeff(wz, 2).coeff(wx, 0)/Uref)
    a2_iso = sp.simplify((PA + a1v)/2)
    a2_aniso = sp.simplify(-(PApar - PA)/2)
    return ('ok', dict(gamma=gamma, A_V=A_V, A_W=A_W, a=aa, b=bb, cF=cF, dF=dF, d=dd_,
                       alpha1=a1v, alpha2=a2v, a2_iso=a2_iso, a2_aniso=a2_aniso,
                       H00s=H00s, H11s=H11s))


def show(tag, r):
    if r[0] != 'ok':
        P(f"  {tag:26s}: {r[0]}"); return None
    d = r[1]
    P(f"  {tag:26s}: gamma={sp.nsimplify(d['gamma'])} A_V={sp.nsimplify(d['A_V'])} A_W={sp.nsimplify(d['A_W'])} "
      f"dF={sp.nsimplify(d['dF'])}")
    P(f"  {'':26s}  alpha1={sp.nsimplify(d['alpha1'])} alpha2={sp.nsimplify(d['alpha2'])} "
      f"a2_iso={sp.nsimplify(d['a2_iso'])} a2_aniso={sp.nsimplify(d['a2_aniso'])}")
    return d


if __name__ == '__main__':
    P("="*92); P("ROUTE B PART B: Setup-M solve -- validation gates + vector diagnostics"); P("="*92)
    show("[G-GR] pure GR", solve(0.0, 10.0, 0.0, 1.0, gr_only=True))
    P(f"  [t={time.time()-T0:.1f}s]")
    P("  --- vector sector (scalar OFF), c2* ON, sweep K_B (expect alpha1=-4KB, alpha2=0): ---")
    for kb in [sp.Rational(1,4), sp.Rational(1,10), sp.Rational(1,100), sp.Rational(1,1000)]:
        r = solve(kb, 10.0, sp.Rational(1,5), 1.0, use_c2star=True, scalar_on=False)
        if r[0] == 'ok':
            P(f"    K_B={float(kb):.4g}: alpha1={sp.nsimplify(r[1]['alpha1'])}  alpha2={float(r[1]['alpha2']):+.6e}"
              f"  (target a1={-4*float(kb):+.4g}, a2=0)")
        else:
            P(f"    K_B={float(kb)}: {r[0]}")
    P(f"  [t={time.time()-T0:.1f}s]")
    P("  --- vector sector, c2* OFF (bare Maxwell, expect alpha2 SINGULAR ~1/K_B or large): ---")
    for kb in [sp.Rational(1,10), sp.Rational(1,100)]:
        r = solve(kb, 10.0, sp.Rational(1,5), 1.0, use_c2star=False, scalar_on=False)
        if r[0] == 'ok':
            P(f"    K_B={float(kb):.4g}: alpha1={sp.nsimplify(r[1]['alpha1'])}  alpha2={float(r[1]['alpha2']):+.6e}")
    P(f"  [t={time.time()-T0:.1f}s]")
