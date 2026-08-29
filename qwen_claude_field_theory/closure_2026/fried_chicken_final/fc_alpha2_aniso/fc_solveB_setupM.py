#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_solveB_setupM.py  --  ROUTE B, PART B: the SCALAR contribution Delta alpha_2^(phiA), via an
INDEPENDENT moving-source (Setup M) 1PN solve.  Cross-checks route-A (Setup S, boosted aether).
====================================================================================================
SETUP M (independent of route-A Setup S): aether AT REST A^mu=(1,0,0,0), phi=Q0 t (Q=Q0,Y=0), flat;
the SOURCE MOVES at w with rigid retardation  omega=k.w  (=> d_0 -> -i k.w).  k=xhat: omega=w1,
w1 PARALLEL, w2 PERP.  Boost conjugate of route-A => must give the SAME alpha_1,alpha_2 (the check).

METRIC in HARMONIC (de Donder) form so ALL 10 components stay dynamical and the gauge-invariant
extraction 2b+d is directly readable (the fc_aniso_grgate.py method):
   L_EH^harm = (1/4) d_lam h_{mn} d^lam h^{mn} - (1/8) d_lam h d^lam h   [=> -(1/2) box hbar_{mn} = source]
Aether a_i (a_0 from A.A=-1 algebraically), scalar chi.  Frozen action with c2star(div A)^2.

EXTRACTION (GR-gate, gauge-invariant):
   g_0i = a V_i + b W_i,  g_00^(w2)= c w^2 U + d (w.x)^2 U/r^2,
   alpha_1 = -2(a+b)-(4gamma+4),  alpha_2 = -(2b+d)-1.
   Fourier (k=xhat): g_0i = A_V w_i U + A_W (k.w)k_i/k^2 U -> a=A_V+A_W/2, b=-A_W/2.
                     A_V = coeff(g_02, w2 U);  A_V+A_W = coeff(g_01, w1 U).
                     g_00^(w2)= c_F w^2 U + d_F (k.w)^2/k^2 U -> c=c_F+d_F/2, d=-d_F/2.
                     c_F = coeff(g_00, w2^2 U);  c_F+d_F = coeff(g_00, w1^2 U).
   ALSO Carl's channels (task):  Psi = -H00/2;  P_A = -2[coeff w_perp^2 U]Psi (isotropic v^2U),
                     P_Apar = -2[coeff w_par^2 U]Psi;  a2_iso=(P_A+alpha1)/2, a2_aniso=-(P_Apar-P_A)/2.

GATES (numeric): [G-GR] all-off => alpha=0.  [G-gam] gamma=1.  [G-vec] scalar off + c2star on =>
alpha_1=-4KB, alpha_2=0 (Foster-Jacobson).  [G-D2] channels agree.  Report Delta alpha_2 only if pass.
"""
import sympy as sp, time, sys

T0 = time.time()
P = lambda *a: print(*a, flush=True)

# ---------------- symbols ----------------
eps = sp.Symbol('eps', positive=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
kx, ky, kz = sp.symbols('k_x k_y k_z', real=True)
I = sp.I
eta = sp.diag(-1, 1, 1, 1)
Es, Eis = sp.symbols('E_s E_is')
Uh = sp.Symbol('U_hat')

def Kmu():
    om = kx*w1 + ky*w2 + kz*w3
    return [-om, kx, ky, kz]

def nf(tag):
    ket = sp.Symbol(tag+'k'); bra = sp.Symbol(tag+'b')
    return ket*Es + bra*Eis, ket, bra

def d(f, mu):
    K = Kmu()
    return sp.diff(f, Es)*(I*K[mu]*Es) + sp.diff(f, Eis)*(-I*K[mu]*Eis)

WMAX = 2
def wtrunc(e):
    e = sp.expand(e); out = 0
    for i in range(WMAX+1):
        ci = e.coeff(w1, i)
        for j in range(WMAX+1-i):
            cj = ci.coeff(w2, j)
            for l in range(WMAX+1-i-j):
                out += cj.coeff(w3, l)*w1**i*w2**j*w3**l
    return sp.expand(out)

def te(e):
    e = sp.expand(e); out = 0
    for a in range(3):
        out += wtrunc(e.coeff(eps, a))*eps**a
    return sp.expand(out)

# ---------------- amplitudes: full 10-metric + aether + scalar ----------------
Hs = {}; Hk = {}; Hb = {}
IDX = [(0,0),(0,1),(0,2),(0,3),(1,1),(2,2),(3,3),(1,2),(1,3),(2,3)]
for (i, j) in IDX:
    f, kk, bb = nf(f'H{i}{j}'); Hs[(i, j)] = f; Hs[(j, i)] = f; Hk[(i, j)] = kk; Hb[(i, j)] = bb
af = []; ak = []; ab = []
for i in range(3):
    f, kk, bb = nf(f'a{i+1}'); af.append(f); ak.append(kk); ab.append(bb)
chi, chik, chib = nf('chi')
rho, Rk, Rb = nf('rho')
a0f0, a0k, a0b = nf('a0p')

def build(KBv, K2v, Q0v, JYv, use_c2star=True, scalar_on=True, gr_only=False):
    KB = sp.nsimplify(KBv); K2 = sp.nsimplify(K2v); Q0 = sp.nsimplify(Q0v); JY = sp.nsimplify(JYv)
    c2star = KB/(1 - 2*KB) if use_c2star else sp.S(0)
    if gr_only:
        KB = sp.S(0); c2star = sp.S(0); Q0 = sp.S(0); scalar_on = False

    H = sp.zeros(4, 4)
    for (i, j) in IDX:
        H[i, j] = Hs[(i, j)]; H[j, i] = Hs[(i, j)]
    gd = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps*H[m, n])
    Hup = eta*H*eta
    gu = sp.Matrix(4, 4, lambda a, b: (eta - eps*Hup + eps**2*(Hup*H*eta))[a, b])
    trH = sum(eta[m, n]*H[m, n] for m in range(4) for n in range(4))
    HH = sum(Hup[m, n]*H[m, n] for m in range(4) for n in range(4))
    sqg = 1 + eps*trH/2 + eps**2*(trH**2/8 - HH/4)

    # ---- harmonic (de Donder) EH: L = 1/4 d_l h_mn d^l h^mn - 1/8 d_l h d^l h ----
    def dd(f, g):
        return sum(eta[l, s]*d(f, l)*d(g, s) for l in range(4) for s in range(4))
    L_EH = (sp.Rational(1, 4)*sum(dd(H[m, n], Hup[m, n]) for m in range(4) for n in range(4))
            - sp.Rational(1, 8)*dd(trH, trH))
    L_EH = eps**2*L_EH   # O(eps^2)

    # ---- aether unit constraint fixes a_0 ----
    Aup_bg = sp.Matrix([1, 0, 0, 0]); Adn_bg = eta*Aup_bg
    a0f = a0f0
    Adn = sp.Matrix([Adn_bg[0] - eps*a0f, Adn_bg[1] + eps*af[0],
                     Adn_bg[2] + eps*af[1], Adn_bg[3] + eps*af[2]])
    Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
    C1 = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
    solA = sp.solve([sp.expand(C1).coeff(Es, 1), sp.expand(C1).coeff(Eis, 1)], [a0k, a0b], dict=True)[0]
    a0f = a0f.subs(solA)
    Adn = sp.Matrix([Adn_bg[0] - eps*a0f, Adn_bg[1] + eps*af[0],
                     Adn_bg[2] + eps*af[1], Adn_bg[3] + eps*af[2]])
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
    # div A = nabla_mu A^mu ; linear piece
    sqgA = [te(te(sqg)*AupT[m]) for m in range(4)]
    divA = te(sum(d(sqgA[m], m) for m in range(4)))
    divA1 = divA.coeff(eps, 1)
    C2term = eps**2*c2star*divA1**2

    Jup = [te(sum(AupT[nu]*(d(AupT[al], nu) + sum(GamT[al][nu][r]*AupT[r] for r in range(4)))
             for nu in range(4))) for al in range(4)]
    Jdphi = te(sum(Jup[m]*dphiT[m] for m in range(4)))
    Qc = te(sum(AupT[m]*dphiT[m] for m in range(4)))
    Yc = te(sum((guT[m, n] + AupT[m]*AupT[n])*dphiT[m]*dphiT[n] for m in range(4) for n in range(4)))
    Kq = K2*te((Qc - Q0)**2)

    def grade(e):
        e = sp.expand(e); return [wtrunc(e.coeff(eps, n)) for n in range(3)]
    gF2 = grade(F2); gC2 = grade(C2term); gJ = grade(Jdphi); gY = grade(Yc); gK = grade(Kq)
    gsq = grade(sqg)
    if scalar_on:
        darkS = [-(KB/2)*gF2[n] + gC2[n] + 2*(2-KB)*gJ[n] - (2-KB)*(1+JY)*gY[n] - gK[n]
                 for n in range(3)]
    else:
        darkS = [-(KB/2)*gF2[n] + gC2[n] for n in range(3)]
    L2_dark = wtrunc(sum(gsq[a]*darkS[2-a] for a in range(3)))

    gam = 1 + (w1**2 + w2**2 + w3**2)/2
    u = [gam, gam*w1, gam*w2, gam*w3]
    SRC = 4*sp.pi
    hT = sum(H[m, n]*u[m]*u[n] for m in range(4) for n in range(4))
    L2_matt = SRC*wtrunc(eps**2*rho*hT)

    L2 = sp.expand(wtrunc(te(L_EH)) + L2_dark + L2_matt)
    pol = sp.Poly(L2, Es, Eis); L2dc = 0
    for mon, cc in zip(pol.monoms(), pol.coeffs()):
        if mon[0] == mon[1]:
            L2dc += cc*(Es*Eis)**mon[0]
    L2dc = L2dc.subs(Es*Eis, 1)
    return sp.expand(L2dc.subs({ky: 0, kz: 0, kx: 1}))


def solve(KBv, K2v, Q0v, JYv, use_c2star=True, scalar_on=True, gr_only=False, verbose=False):
    L2dc = build(KBv, K2v, Q0v, JYv, use_c2star, scalar_on, gr_only)
    KETS = [Hk[ij] for ij in IDX] + [ak[0], ak[1], ak[2]] + ([chik] if scalar_on else [])
    BRAS = [Hb[ij] for ij in IDX] + [ab[0], ab[1], ab[2]] + ([chib] if scalar_on else [])
    eqf = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}

    def lin(eqs, unk):
        M, b = sp.linear_eq_to_matrix(eqs, unk)
        s = list(sp.linsolve((M, b), unk))
        return dict(zip(unk, s[0])) if s else None

    def w0(e):
        return sp.expand(e).coeff(w1, 0).coeff(w2, 0).coeff(w3, 0)

    # w=0 static: odd fields (H01,H02,H03,H12,H13,H23,a1,a2,a3) vanish by parity; even block solves
    even_k = [Hk[(0, 0)], Hk[(1, 1)], Hk[(2, 2)], Hk[(3, 3)]] + ([chik] if scalar_on else []) + [ak[0]]
    even_b = [Hb[(0, 0)], Hb[(1, 1)], Hb[(2, 2)], Hb[(3, 3)]] + ([chib] if scalar_on else []) + [ab[0]]
    odd_k = [Hk[(0, 1)], Hk[(0, 2)], Hk[(0, 3)], Hk[(1, 2)], Hk[(1, 3)], Hk[(2, 3)], ak[1], ak[2]]
    VZ = {kk: 0 for kk in odd_k}
    e0 = [w0(eqf[A].subs(VZ)) for A in even_b]
    s0s = lin(e0, even_k)
    if s0s is None:
        return ('static-fail',)
    s0 = {**s0s, **{kk: sp.S(0) for kk in odd_k}}

    # order by order in w
    quad_mon = [('11', w1*w1), ('22', w2*w2), ('33', w3*w3), ('12', w1*w2), ('13', w1*w3), ('23', w2*w3)]
    lin1 = {A: sum(sp.Symbol(f'{A}_1_{v}')*vv for v, vv in [('1', w1), ('2', w2), ('3', w3)]) for A in KETS}
    lin2 = {A: sum(sp.Symbol(f'{A}_2_{tag}')*vv for tag, vv in quad_mon) for A in KETS}
    sub = {A: s0[A] + lin1[A] + lin2[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(sub)) for A in BRAS}

    def cwdeg(e, deg):
        e = sp.expand(e); out = []
        if deg == 1:
            out.append(w0(e.coeff(w1, 1)))
            out.append(w0(e.coeff(w2, 1)))
            out.append(w0(e.coeff(w3, 1)))
            return out
        for tag, vv in quad_mon:
            if tag[0] == tag[1]:
                out.append(w0(e.coeff(vv, 1)))
            else:
                a, b = int(tag[0]), int(tag[1])
                va = {1: w1, 2: w2, 3: w3}[a]; vb = {1: w1, 2: w2, 3: w3}[b]
                out.append(w0(e.coeff(va, 1).coeff(vb, 1)))
        return out

    unk1 = [sp.Symbol(f'{A}_1_{v}') for A in KETS for v in ('1', '2', '3')]
    eq1 = []
    for A in BRAS:
        eq1 += cwdeg(eqW[A], 1)
    s1 = lin(eq1, unk1)
    if s1 is None:
        return ('w1-fail',)
    unk2 = [sp.Symbol(f'{A}_2_{tag}') for A in KETS for tag, _ in quad_mon]
    eq2 = []
    for A in BRAS:
        eq2 += [sp.expand(e).subs(s1) for e in cwdeg(eqW[A], 2)]
    s2 = lin(eq2, unk2)
    if s2 is None:
        return ('w2-fail',)

    def kv(A):
        val = s0[A]
        val += sum(s1[sp.Symbol(f'{A}_1_{v}')]*vv for v, vv in [('1', w1), ('2', w2), ('3', w3)])
        val += sum(s2[sp.Symbol(f'{A}_2_{tag}')]*vv for tag, vv in quad_mon)
        return sp.expand(val)

    subU = {Rk: -Uh/(4*sp.pi)}
    # static: h00, hjj
    H00_0 = w0(kv(Hk[(0, 0)])).subs(subU)          # g_00 static = H00 = 2U ? (calibrate)
    H22_0 = w0(kv(Hk[(2, 2)])).subs(subU)
    Uval = sp.simplify(H00_0/2)                     # define U from static g_00 = 2U
    # g_0i O(w): H02 (perp), H01 (par)
    H02 = sp.expand(kv(Hk[(0, 2)])).subs(subU)
    H01 = sp.expand(kv(Hk[(0, 1)])).subs(subU)
    A_V = sp.expand(H02.coeff(w2, 1).coeff(w1, 0).coeff(w3, 0)).coeff(Uh, 1)
    AVpAW = sp.expand(H01.coeff(w1, 1).coeff(w2, 0).coeff(w3, 0)).coeff(Uh, 1)
    A_W = AVpAW - A_V
    aa = A_V + A_W/2; bb = -A_W/2
    # g_00 O(w^2): H00 perp/par
    H00_2 = sp.expand(kv(Hk[(0, 0)])).subs(subU)
    cF = sp.expand(H00_2.coeff(w2, 2).coeff(w1, 0).coeff(w3, 0)).coeff(Uh, 1)
    cFpdF = sp.expand(H00_2.coeff(w1, 2).coeff(w2, 0).coeff(w3, 0)).coeff(Uh, 1)
    dF = cFpdF - cF
    cc = cF + dF/2; dd_ = -dF/2
    gamma = sp.simplify(H22_0/H00_0*2/2)   # g_ij = 2 gamma U delta ; g_00=2U -> gamma=H22/H00
    res = dict(U=Uval, H00_0=H00_0, H22_0=H22_0, A_V=A_V, A_W=A_W, a=aa, b=bb, cF=cF, dF=dF,
               c=cc, d=dd_, gamma=sp.simplify(H22_0/H00_0))
    # alpha's (gauge invariant)
    g = res['gamma']
    res['alpha1'] = sp.simplify(-2*(aa + bb) - (4*g + 4))
    res['alpha2'] = sp.simplify(-(2*bb + dd_) - 1)
    # Carl's channels from Psi=-H00/2
    Psi2 = sp.expand(-H00_2/2)
    PA = -2*sp.expand(Psi2.coeff(w2, 2).coeff(w1, 0).coeff(w3, 0)).coeff(Uh, 1)
    PApar = -2*sp.expand(Psi2.coeff(w1, 2).coeff(w2, 0).coeff(w3, 0)).coeff(Uh, 1)
    res['a2_iso'] = sp.simplify((PA + res['alpha1'])/2)
    res['a2_aniso'] = sp.simplify(-(PApar - PA)/2)
    return ('ok', res)


def show(tag, r):
    if r[0] != 'ok':
        P(f"  {tag}: {r[0]}"); return None
    d = r[1]
    P(f"  {tag}: gamma={sp.nsimplify(d['gamma'])}  a={sp.nsimplify(d['a'])} b={sp.nsimplify(d['b'])} "
      f"cF={sp.nsimplify(d['cF'])} dF={sp.nsimplify(d['dF'])}")
    P(f"        alpha1={sp.nsimplify(d['alpha1'])}  alpha2(2b+d)={sp.nsimplify(d['alpha2'])}  "
      f"a2_iso={sp.nsimplify(d['a2_iso'])}  a2_aniso={sp.nsimplify(d['a2_aniso'])}")
    return d


if __name__ == '__main__':
    P("="*92); P("ROUTE B PART B: Setup-M solve -- validation gates"); P("="*92)
    P("[G-GR] pure GR (all AeST off):")
    show("GR", solve(0.0, 10.0, 0.0, 1.0, use_c2star=False, scalar_on=False, gr_only=True))
    P(f"  [t={time.time()-T0:.1f}s]")
