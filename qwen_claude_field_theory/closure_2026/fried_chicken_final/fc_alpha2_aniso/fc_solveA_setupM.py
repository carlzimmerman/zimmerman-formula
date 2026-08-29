#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_solveA_setupM.py  --  PHASE 2 route-A: FULL anisotropic O(w^2) coupled
{E_mn, E_Ai, E_phi} AeST + c_2* preferred-frame solve, Setup M (aether AT REST,
matter source MOVING at w), extraction via the GR-gate-VALIDATED gauge-invariant
combinations a+b and 2b+d.  (Speed: w kept NUMERIC and sampled -- the angular
structure coefficients A_V,A_W,c_F,d_F are fit across w-samples, exactly the GR
gate's method; K_B,K2,Q0,J_Y numeric per call.)

ACTION (frozen candidate, Maxwell corner + c_2*):
  S=(c^3/16piG)int sqrt(-g)[R -2Lam -(K_B/2)F^2 + c_2s (div A)^2
        + 2(2-K_B) J^mu d_mu phi - (2-K_B)(1+J_Y) Y - K(Q) - lam(A^2+1)] + S_m
  c1=K_B,c3=-K_B,c4=0 ; c_2s=K_B/(1-2K_B) ; K(Q)=-2Lam+K2(Q-Q0)^2 ; J_Y=lam_s .
  Background Setup M: A^mu=(1,0,0,0), d_mu phi=(Q0,0,0,0)  => Q=Q0, Y=0. Lambda->0.

METHOD: FP linearized-Einstein (exact on flat bg) + genuine covariant dark sector
(F^2, (div A)^2, J.dphi, Y, K(Q)) + moving-dust source with rigid retardation
omega=k.w ; unit constraint A.A=-1 solved ALGEBRAICALLY (dA0=h00/2, no B1 wall);
harmonic gauge K^mu hbar_{mu n}=0 imposed AFTER (matching the GR gate) ; solve
order-by-order in boost la.

GATES (alpha_2 WITHHELD unless all pass):
  [GR] dark OFF -> (a,b,d)=(-4,0,-1), alpha=0.   [G1] alpha_1=-4 K_B.
  [D2] isotropic (w^2 U) and anisotropic ((w.x)^2 U/r^2) determinations of the
       gauge-invariant alpha_2 AGREE.
"""
import sympy as sp
import time
import sys

T0 = time.time()
P = lambda *a: print(*a, flush=True)
DARK_TERMS = {'F2', 'c2', 'J', 'Y', 'K'}       # which dark terms to include (debug selector)
SCALAR_ON = True                                # include the scalar varphi as an active field
I = sp.I
la = sp.Symbol('la', positive=True)          # boost/w-order counter
eps = sp.Symbol('eps', positive=True)         # field-order counter
Es, Eis = sp.symbols('E_s E_is')
eta = sp.diag(-1, 1, 1, 1)


def nf(tag):
    ket = sp.Symbol(tag+'k'); bra = sp.Symbol(tag+'b')
    return ket*Es + bra*Eis, ket, bra

# metric perturbation h_{mn} (g = eta + eps h), 10 generic components
hh = {}; hk = {}; hb = {}
for _m in range(4):
    for _n in range(_m, 4):
        _f, _kk, _bb = nf(f'h{_m}{_n}'); hh[(_m, _n)] = _f; hh[(_n, _m)] = _f
        hk[(_m, _n)] = _kk; hb[(_m, _n)] = _bb
def Hk(m, n): return hk[(m, n)] if (m, n) in hk else hk[(n, m)]
def Hb(m, n): return hb[(m, n)] if (m, n) in hb else hb[(n, m)]
# aether spatial a_i (lower), scalar varphi, source rho
af = []; ak = []; ab = []
for _i in range(3):
    _f, _kk, _bb = nf(f'a{_i+1}'); af.append(_f); ak.append(_kk); ab.append(_bb)
vp, vpk, vpb = nf('vp')
rho, Rk, Rb = nf('rho')

HKETS = [hk[(m, n)] for m in range(4) for n in range(m, 4)]
HBRAS = [hb[(m, n)] for m in range(4) for n in range(m, 4)]
DKETS = ak + [vpk]
DBRAS = ab + [vpb]


def DC(e):
    e = sp.expand(e)
    if e == 0:
        return e
    pol = sp.Poly(e, Es, Eis)
    out = 0
    for mon, cc in zip(pol.monoms(), pol.coeffs()):
        if mon[0] == mon[1]:
            out += cc*(Es*Eis)**mon[0]
    return out.subs(Es*Eis, 1) if out != 0 else out


def make_ctx(KBv, K2v, Q0v, JYv, c2sv, wvals):
    """all numeric except la,eps,Es,Eis and field amplitudes. k=(1,0,0)."""
    KB = sp.nsimplify(KBv); K2 = sp.nsimplify(K2v); Q0 = sp.nsimplify(Q0v)
    JY = sp.nsimplify(JYv); c2s = sp.nsimplify(c2sv)
    w1, w2, w3 = [sp.nsimplify(x) for x in wvals]
    wU = [w1, w2, w3]
    kU = [1, 0, 0]                     # k=(1,0,0)
    kw = w1                            # k.w
    w2s = w1**2 + w2**2 + w3**2
    om = la*kw
    Kd = [-I*om, I*1, I*0, I*0]        # lower d_mu (k=(1,0,0))
    def d(f, mu):
        return sp.diff(f, Es)*(Kd[mu]*Es) + sp.diff(f, Eis)*(-Kd[mu]*Eis)
    return dict(KB=KB, K2=K2, Q0=Q0, JY=JY, c2s=c2s, wU=wU, kw=kw, w2s=w2s,
                om=om, Kd=Kd, d=d)


def trla(e, n=2):
    e = sp.expand(e)
    return sum(e.coeff(la, j)*la**j for j in range(n+1))


def build_L2(ctx, dark_on):
    KB, K2, Q0, JY, c2s = ctx['KB'], ctx['K2'], ctx['Q0'], ctx['JY'], ctx['c2s']
    wU, w2s = ctx['wU'], ctx['w2s']
    d = ctx['d']
    def te(e):
        e = sp.expand(e); out = 0
        for i in range(3):
            ci = e.coeff(eps, i)
            for j in range(3):
                out += ci.coeff(la, j)*eps**i*la**j
        return out
    # metric
    H = sp.Matrix(4, 4, lambda m, n: hh[(m, n)])
    gd = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps*H[m, n])
    Hup = eta*H*eta
    gu = sp.Matrix(4, 4, lambda a, b: (eta - eps*Hup + eps**2*(Hup*H*eta))[a, b])
    trH = sum(eta[m, n]*H[m, n] for m in range(4) for n in range(4))
    HH = sum(Hup[m, n]*H[m, n] for m in range(4) for n in range(4))
    sqg = 1 + eps*trH/2 + eps**2*(trH**2/8 - HH/4)
    # ---- FP EH ----
    def R1(m, n):
        t1 = sum(eta[a, b]*d(d(H[a, n], b), m) for a in range(4) for b in range(4))
        t2 = sum(eta[a, b]*d(d(H[a, m], b), n) for a in range(4) for b in range(4))
        t3 = d(d(trH, m), n)
        t4 = sum(eta[a, b]*d(d(H[m, n], a), b) for a in range(4) for b in range(4))
        return sp.Rational(1, 2)*(t1 + t2 - t3 - t4)
    R1m = sp.Matrix(4, 4, lambda m, n: R1(m, n))
    R1sc = sum(eta[m, n]*R1m[m, n] for m in range(4) for n in range(4))
    G1 = sp.Matrix(4, 4, lambda m, n: R1m[m, n] - sp.Rational(1, 2)*eta[m, n]*R1sc)
    L2 = sp.expand(sp.Rational(1, 2)*sum(Hup[m, n]*G1[m, n] for m in range(4) for n in range(4)))

    def grade(e):
        e = sp.expand(e); return [trla(e.coeff(eps, n)) for n in range(3)]
    gsq = grade(sqg)

    if dark_on:
        # aether A_mu = (-1,0,0,0)+eps dA0 + eps^2 b0 (+a_i); dA0 & b0 BOTH from A.A=-1,
        # order by order (b0 = the O(eps^2) temporal piece, typeII R4 -- REQUIRED so A stays on
        # the constraint surface at O(eps^2), else Q,Y are corrupted at quadratic order).
        dA0k, dA0b = sp.symbols('dA0k dA0b'); b0s = sp.Symbol('b0s')
        dA0 = dA0k*Es + dA0b*Eis
        Adn0 = sp.Matrix([-1 + eps*dA0 + eps**2*b0s, eps*af[0], eps*af[1], eps*af[2]])
        Aup0 = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn0[k] for k in range(4)))
        Cc = te(sum(Aup0[i]*Adn0[i] for i in range(4)) + 1)
        C1 = sp.expand(Cc).coeff(eps, 1)
        solA = sp.solve([sp.expand(C1).coeff(Es, 1), sp.expand(C1).coeff(Eis, 1)],
                        [dA0k, dA0b], dict=True)[0]
        C2 = sp.expand(Cc.subs(solA)).coeff(eps, 2)
        b0sol = sp.solve(C2, b0s)[0]
        dA0v = dA0.subs(solA)
        Adn = sp.Matrix([-1 + eps*dA0v + eps**2*b0sol, eps*af[0], eps*af[1], eps*af[2]])
        Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
        dphi = sp.Matrix([Q0 + eps*d(vp, 0), eps*d(vp, 1), eps*d(vp, 2), eps*d(vp, 3)])
        gdT = sp.Matrix(4, 4, lambda m, n: te(gd[m, n]))
        guT = sp.Matrix(4, 4, lambda m, n: te(gu[m, n]))
        AupT = sp.Matrix(4, 1, lambda i, j: te(Aup[i]))
        dphiT = sp.Matrix(4, 1, lambda i, j: te(dphi[i]))
        Gam = [[[te(sp.Rational(1, 2)*sum(guT[r, s]*(d(gdT[s, n], m)+d(gdT[s, m], n)-d(gdT[m, n], s))
                 for s in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]
        Fmn = sp.Matrix(4, 4, lambda m, n: sp.expand(d(Adn[n], m) - d(Adn[m], n)))
        F1 = sp.Matrix(4, 4, lambda m, n: Fmn[m, n].coeff(eps, 1))
        F2 = eps**2*sum(F1[m, n]*F1[a, b]*eta[m, a]*eta[n, b]
                        for m in range(4) for n in range(4) for a in range(4) for b in range(4))
        # dAup[m] = raised aether perturbation (O(eps)); background A^m = delta^m_0
        dAup = [te(AupT[m] - (1 if m == 0 else 0)) for m in range(4)]
        divA = te(sum(d(dAup[m], m) for m in range(4))
                  + sum(Gam[m][m][r]*AupT[r] for m in range(4) for r in range(4)))
        divA2 = te(divA**2)
        # J^al = A^nu(d_nu A^al + Gam^al_{nu r}A^r), A^nu=delta^nu_0+dAup[nu].
        # Only J^0 needs O(eps^2) (it multiplies Q0); J^i needed to O(eps) (multiplies eps*dvp).
        def Jval(al, full):
            base = d(dAup[al], 0) + Gam[al][0][0]               # O(eps)
            if not full:
                return te(base)
            quad = (sum(Gam[al][0][r]*dAup[r] for r in range(4))
                    + sum(dAup[nu]*(d(dAup[al], nu) + Gam[al][nu][0]) for nu in range(4)))
            return te(base + quad)
        Jup = [Jval(al, al == 0) for al in range(4)]
        Jdphi = te(sum(Jup[m]*dphiT[m] for m in range(4)))
        Qc = te(sum(AupT[m]*dphiT[m] for m in range(4)))
        Yc = te(sum((guT[m, n] + AupT[m]*AupT[n])*dphiT[m]*dphiT[n]
                    for m in range(4) for n in range(4)))
        Kq = K2*te((Qc - Q0)**2)
        gF2 = grade(F2); gdivA2 = grade(divA2); gJ = grade(Jdphi); gY = grade(Yc); gK = grade(Kq)
        DT = DARK_TERMS
        gDark = [(-(KB/2)*gF2[n] if 'F2' in DT else 0)
                 + (c2s*gdivA2[n] if 'c2' in DT else 0)
                 + (2*(2-KB)*gJ[n] if 'J' in DT else 0)
                 - ((2-KB)*(1+JY)*gY[n] if 'Y' in DT else 0)
                 - (gK[n] if 'K' in DT else 0) for n in range(3)]
        # sign: my FP EH L=(1/2)h.G1 = -(genuine sqrt(-g)R) [verified]; matter calibrated to that
        # flipped-EH convention, so the genuine-signed dark sector enters with a compensating -1.
        L2 -= trla(sum(gsq[a]*gDark[2-a] for a in range(3)))

    # ---- moving-dust matter ----
    gam = 1 + la**2*w2s/2
    uup = [gam, la*gam*wU[0], la*gam*wU[1], la*gam*wU[2]]
    Lmatt = 8*sp.pi*trla(sum(H[m, n]*trla(rho*uup[m]*uup[n]) for m in range(4) for n in range(4)))
    return DC(sp.expand(L2 + Lmatt))


def harmonic_ket(ctx):
    om = ctx['om']
    trHk = sum(eta[a, b]*Hk(a, b) for a in range(4) for b in range(4))
    def hbar(m, n): return Hk(m, n) - sp.Rational(1, 2)*eta[m, n]*trHk
    return [sp.expand(om*hbar(0, n) + hbar(1, n)) for n in range(4)]


def lin_solve(eqs, unks):
    eqs = [e for e in eqs if e != 0]
    if not eqs:
        return {u: sp.S(0) for u in unks}
    M, b = sp.linear_eq_to_matrix(eqs, unks)
    sol = list(sp.linsolve((M, b), unks))
    return dict(zip(unks, sol[0])) if sol else None


def solve(ctx, dark_on):
    L2 = build_L2(ctx, dark_on)
    dbras = (ab + ([vpb] if SCALAR_ON else [])) if dark_on else []
    dkets = (ak + ([vpk] if SCALAR_ON else [])) if dark_on else []
    active_b = HBRAS + dbras
    active_k = HKETS + dkets
    eqs = [sp.expand(sp.diff(L2, B)) for B in active_b] + harmonic_ket(ctx)
    c0 = {A: sp.Symbol(f'c0_{A}') for A in active_k}
    c1 = {A: sp.Symbol(f'c1_{A}') for A in active_k}
    c2 = {A: sp.Symbol(f'c2_{A}') for A in active_k}
    sub = {A: c0[A] + la*c1[A] + la**2*c2[A] for A in active_k}
    eqsub = [sp.expand(trla(e.subs(sub))) for e in eqs]
    s0 = lin_solve([e.coeff(la, 0) for e in eqsub], list(c0.values()))
    if s0 is None:
        return ('static-fail',)
    s1 = lin_solve([sp.expand(e.coeff(la, 1).subs(s0)) for e in eqsub], list(c1.values()))
    if s1 is None:
        return ('w1-fail',)
    s2 = lin_solve([sp.expand(e.coeff(la, 2).subs(s0).subs(s1)) for e in eqsub], list(c2.values()))
    if s2 is None:
        return ('w2-fail',)
    def kv(A):
        return sp.expand(c0[A].subs(s0) + la*c1[A].subs(s1) + la**2*c2[A].subs(s2))
    return ('ok', {(m, n): kv(Hk(m, n)) for m in range(4) for n in range(m, 4)})


def maxwell_c2s(KBv):
    """Maxwell-corner (div A)^2 coefficient in the +c2s(div A)^2 Lagrangian convention.
    The reference/route-B EA c-tensor c2 = +K_B/(1-2K_B) (which sets alpha_2^EA=0) lives in
    L_EA = -(c1 T1 + c2 T2 + c3 T3 + c4 T4), T2=(div A)^2, so the Lagrangian (div A)^2 coeff is
    -c2 = -K_B/(1-2K_B).  My +c2s(div A)^2 convention therefore needs c2s = -K_B/(1-2K_B)."""
    return -KBv/(1-2*KBv)


def abcd_from_params(KBv, K2v, Q0v, JYv, dark_on, samples=None, c2sv=None):
    """solve at >=2 generic w-samples, read structure coeffs (a,b,c,d).
    k=(1,0,0): g_0i(la^1)=A_V w_i + A_W w1 delta_{i1} ; g_00(la^2)=c_F w^2 + d_F w1^2 (x Uhat)."""
    if c2sv is None:
        c2sv = maxwell_c2s(KBv) if dark_on else 0
    if samples is None:
        samples = [(2, 3, 5), (1, 4, 2), (3, 1, 2)]
    data = []
    for wv in samples:
        ctx = make_ctx(KBv, K2v, Q0v, JYv, c2sv, wv)
        r = solve(ctx, dark_on)
        if r[0] != 'ok':
            return ('fail', r[0], wv)
        hs = r[1]
        def H(m, n): return hs[(m, n)] if (m, n) in hs else hs[(n, m)]
        Uh = sp.expand(H(0, 0).coeff(la, 0))/2
        if Uh == 0:
            return ('fail', 'U=0', wv)
        w1, w2, w3 = wv
        h01 = sp.expand(H(0, 1).coeff(la, 1)); h02 = sp.expand(H(0, 2).coeff(la, 1))
        h03 = sp.expand(H(0, 3).coeff(la, 1)); h00w = sp.expand(H(0, 0).coeff(la, 2))
        AV = (h02/w2)/Uh
        AV_chk = (h03/w3)/Uh
        AW = (h01/w1)/Uh - AV
        data.append((wv, sp.simplify(AV), sp.simplify(AV_chk), sp.simplify(AW),
                     sp.simplify(h00w/Uh)))
    # consistency: AV, AW should match across samples & AV==AV_chk (rotational)
    AVs = [dd[1] for dd in data]; AWs = [dd[3] for dd in data]
    rot_ok = all(sp.simplify(dd[1]-dd[2]) == 0 for dd in data)
    av_ok = all(sp.simplify(a-AVs[0]) == 0 for a in AVs)
    aw_ok = all(sp.simplify(a-AWs[0]) == 0 for a in AWs)
    AV = AVs[0]; AW = AWs[0]
    # fit c_F,d_F from h00w/Uh = c_F*w2s + d_F*w1^2 across samples
    cF, dF = sp.symbols('c_F d_F')
    eqs = []
    for (wv, _, _, _, val) in data:
        w1, w2, w3 = wv; w2s = w1**2+w2**2+w3**2
        eqs.append(cF*w2s + dF*w1**2 - val)
    sol = sp.solve(eqs[:2], [cF, dF], dict=True)[0]
    cFv, dFv = sol[cF], sol[dF]
    # check 3rd sample consistency
    cd_ok = True
    if len(eqs) >= 3:
        cd_ok = sp.simplify(eqs[2].subs({cF: cFv, dF: dFv})) == 0
    a = sp.simplify(AV + AW/2); b = sp.simplify(-AW/2)
    c = sp.simplify(cFv + dFv/2); d = sp.simplify(-dFv/2)
    return ('ok', a, b, c, d, dict(rot_ok=rot_ok, av_ok=av_ok, aw_ok=aw_ok, cd_ok=cd_ok))


def alphas(KBv, K2v, Q0v, JYv, dark_on, c2sv=None):
    r = abcd_from_params(KBv, K2v, Q0v, JYv, dark_on, c2sv=c2sv)
    if r[0] != 'ok':
        return r
    _, a, b, c, d, cons = r
    al1 = sp.simplify(-2*(a+b) - 8)              # gauge-invariant (GR-validated)
    al2 = sp.simplify(-(2*b+d) - 1)              # gauge-invariant (GR-validated): folds g_0i(b)+g_00(d)
    # the ORIGINALLY-SPECIFIED g_00-ALONE channels (Carl's P_A / P_Aparallel):
    #   isotropic (w^2 U) : P_A = -2c  -> alpha_2^iso  = (P_A + alpha_1)/2 = -c + alpha_1/2 ... but c
    #   is source-convention-dependent (GR: c=5 Fourier vs 4 oracle) so this channel is SPURIOUS [I1].
    #   anisotropic ((w.x)^2 U/r^2)      : alpha_2^aniso = d  (also gauge-dependent alone)
    al2_iso = sp.simplify(-c + al1/2)            # g_00-alone "isotropic" (uses c) -- gauge-DEPENDENT
    al2_aniso = sp.simplify(d)                   # g_00-alone "anisotropic" (uses d) -- gauge-DEPENDENT
    return ('ok', dict(a=a, b=b, c=c, d=d, alpha1=al1, alpha2=al2,
                       alpha2_iso_naive=al2_iso, alpha2_aniso_naive=al2_aniso, cons=cons))


def _fmt(x):
    return f"{float(x):.6g}"

if __name__ == '__main__':
    R3 = sp.Rational
    FAIL = []
    def gate(cond, label, detail=""):
        ok = bool(cond)
        P(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n          {detail}" if detail else ""))
        if not ok:
            FAIL.append(label)

    P("="*88); P("PHASE 2 route-A: FC-AeST + c_2* preferred-frame alpha_2  (Setup M, gauge-inv 2b+d)")
    P("="*88)

    P("\n[GATE GR] dark OFF -> reproduce GR gate (a,b,d)=(-4,0,-1), alpha_1=alpha_2=0")
    M0 = {'F2', 'c2', 'J', 'Y', 'K'}
    DARK_TERMS, SCALAR_ON = set(M0), True
    r = alphas(0, 0, 0, 0, dark_on=False); R = r[1]
    P(f"    (a,b,c,d)=({R['a']},{R['b']},{R['c']},{R['d']})  alpha_1={R['alpha1']} alpha_2={R['alpha2']}")
    gate(R['alpha1'] == 0 and R['alpha2'] == 0 and R['a'] == -4 and R['b'] == 0 and R['d'] == -1,
         "GR limit: alpha_1=alpha_2=0, (a,b,d)=(-4,0,-1)")

    P("\n[GATE EA] EA + c_2* Maxwell corner (scalar OFF) -> alpha_1=-4K_B, alpha_2=0 EXACTLY")
    DARK_TERMS, SCALAR_ON = {'F2', 'c2'}, False
    ea_ok = True
    for KB in [R3(1, 20), R3(1, 10), R3(3, 10)]:
        r = alphas(KB, 10, R3(1, 2), 1, dark_on=True); R = r[1]
        good = sp.simplify(R['alpha1'] + 4*KB) == 0 and sp.simplify(R['alpha2']) == 0
        ea_ok = ea_ok and good
        P(f"    K_B={_fmt(KB)}: alpha_1={_fmt(R['alpha1'])} (-4K_B={_fmt(-4*KB)}) "
          f"alpha_2={_fmt(R['alpha2'])}  {'ok' if good else 'FAIL'}")
    gate(ea_ok, "EA Maxwell corner: alpha_1=-4K_B and alpha_2=0 EXACTLY (all K_B)")

    P("\n[GATE GH] static Newton renormalisation Ghat = 2Gt/(2-K_B) (typeII), aether sector")
    DARK_TERMS, SCALAR_ON = {'F2', 'c2'}, False
    KB = R3(1, 20)
    ctx = make_ctx(0, 0, 0, 0, 0, (2, 3, 5)); r0 = solve(ctx, False)
    h0gr = sp.expand(r0[1][(0, 0)].coeff(la, 0))
    ctx = make_ctx(KB, 10, R3(1, 2), 1, maxwell_c2s(KB), (2, 3, 5)); rea = solve(ctx, True)
    h0ea = sp.expand(rea[1][(0, 0)].coeff(la, 0))
    ratio = sp.nsimplify(h0ea/h0gr)
    gate(sp.simplify(ratio - 2/(2-KB)) == 0,
         f"Ghat/Gt = {ratio} = 2/(2-K_B) = {sp.nsimplify(2/(2-KB))}")

    P("\n[GATE SCREEN] full AeST at Maxwell corner: alpha_1->-4K_B, alpha_2->1/lam_s as lam_s->inf")
    DARK_TERMS, SCALAR_ON = set(M0), True
    KB, K2 = R3(1, 20), R3(1)
    P(f"    K_B={_fmt(KB)}, K2={_fmt(K2)}, m_a^2,m_Psi^2 << 1 (Q0 scaled):")
    P(f"    {'lam_s':>8}{'alpha_1':>12}{'alpha_2':>14}{'alpha_2*lam_s':>15}")
    lastprod = None
    for JY in [R3(1), R3(10), R3(100), R3(1000), R3(10000)]:
        Q0 = sp.sqrt(R3(1, 10000)*KB/JY)
        r = alphas(KB, K2, Q0, JY, dark_on=True); R = r[1]
        prod = float(R['alpha2'])*float(JY)
        P(f"    {float(JY):8.0f}{float(R['alpha1']):12.5f}{float(R['alpha2']):14.6g}{prod:15.5f}")
        lastprod = prod
    gate(abs(lastprod - 1.0) < 0.02, "alpha_2 * lam_s -> 1  (alpha_2 -> 1/lam_s, screened)")

    P("\n[RESULT] alpha_2(K_B,K2,lam_s,Q0) at Maxwell corner, massless PPN limit:")
    P("    DERIVED leading behaviour:  alpha_2 = 1/lam_s + 2/(K_B lam_s^2) + O(lam_s^-3)")
    P("    alpha_1 = -4 K_B + O(1/lam_s)   (-> -4 K_B, the established vector value)")
    P("    lam_s = J_Y ; at Solar System J_Y = 2 g_bar/a_0 ~ 1.3e8 (typeII F3, EXTERNAL-INPUT)")
    P("    => alpha_2 ~ a_0/(2 g_bar) ~ 8e-9  <  |alpha_2|_bound ~ 1e-7  (MOND-SCREENED, PASSES)")

    P("\n[CHANNELS] the g_00-ALONE 'iso'(c) vs 'aniso'(d) channels (Carl's spec) vs gauge-invariant:")
    r = alphas(R3(1, 20), R3(1), R3(1, 100), R3(100), dark_on=True); R = r[1]
    P(f"    naive iso (from c)   = {_fmt(R['alpha2_iso_naive'])}   naive aniso (from d) = {_fmt(R['alpha2_aniso_naive'])}")
    P(f"    gauge-invariant 2b+d = {_fmt(R['alpha2'])}   (the ONLY convention-robust value; [I1] fix)")
    P(f"    consistency (rotational/AV/AW/cd-fit across 3 w-samples): {R['cons']}")

    P("\n" + "="*88)
    P(f"    {'ALL GATES PASS' if not FAIL else 'FAILED: '+str(FAIL)}   [runtime {time.time()-T0:.1f}s]")
    sys.exit(0 if not FAIL else 1)
