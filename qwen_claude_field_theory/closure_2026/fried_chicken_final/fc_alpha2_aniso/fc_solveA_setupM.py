#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_solveA_setupM.py  --  PHASE 2, route-A: the FULL anisotropic O(w^2) coupled
{E_mn, E_Ai, E_phi} AeST+c_2* preferred-frame solve, Setup M (aether AT REST,
matter source MOVING at w), extraction via the GR-gate-VALIDATED gauge-invariant
combinations a+b and 2b+d (NOT the g_00-alone P_A/P_Aparallel channels, which the
GR gate [I1] proved gauge-dependent/spurious).

WHY SETUP M (not the boosted-aether Setup S the earlier files used):
  * The GR-validation gate fc_aniso_grgate.py validated EXACTLY this realization:
    a boosted PERFECT-FLUID source at velocity w vs the aether rest frame, harmonic
    gauge imposed AFTER the field equations, gauge-invariant extraction a+b, 2b+d.
    Re-using it verbatim inherits 16/16 certs + the boosted-Schwarzschild oracle.
  * Aether background A^mu=(1,0,0,0) is TRIVIAL here (no boosted-background 1/(2+w^2)
    denominator, no wb-truncation of the constraint) so the unit constraint A.A=-1 is
    solved ALGEBRAICALLY and exactly: delta A_0 = h_00/2  (the B1 wall is absent).

THE ACTION (frozen candidate, Maxwell corner + c_2*):
  S=(c^3/16piG)int sqrt(-g)[R -2Lam -(K_B/2)F^2 + c_2s (div A)^2
        + 2(2-K_B) J^mu d_mu phi - (2-K_B)(1+J_Y) Y - K(Q) - lam(A^2+1)] + S_m
  c1=K_B,c3=-K_B,c4=0 ; c_2s = K_B/(1-2K_B) (the (div A)^2 term that shifts the EA
  c_123 = c1+c2+c3 off 0, regularising the pure-vector alpha_2 pole); K(Q)=-2Lam+K2(Q-Q0)^2,
  J_Y = lam_s (scalar kinetic parameter, A_Y=(2-K_B)(1+lam_s); frozen lam_s=1).
  Matter minimally coupled to g only.  Background: A^mu=(1,0,0,0), d_mu phi=(Q0,0,0,0),
  so Q=Q0, Y=0 (certified [A]).  Lambda->0 (flat) at Solar-System scales.

METHOD: genuine sqrt(-g) R (so the Ghat=Gt/(1-K_B/2) normalisation is the committed
typeII one, not a hand-set constant), Fourier plane wave, moving dust source with
rigid retardation omega=k.w, DC (ket-bra) quadratic action, EOMs by variation, harmonic
gauge imposed via the 4 conditions K^mu hbar_{mu nu}=0 (matching the GR gate), solve
order-by-order in the boost la.  NUMERIC (K_B,K2,Q0,J_Y); w kept symbolic; k=(1,0,0).

GATES (alpha_2 WITHHELD unless all pass):
  [GR]  dark OFF  -> reproduce the GR gate: (a,b,d)=(-4,0,-1), alpha_1=alpha_2=0.
  [NW]  Newton O(la^0): h_00=2U.
  [GH]  static isotropic 00-eq -> Ghat = 2Gt/(2-K_B)   (typeII).
  [MP]  static scalar mass m_Psi^2 = K2 Q0^2/(2-K_B)    (typeII).
  [G1]  alpha_1 = -4 K_B  (Foster-Jacobson, c_2s-independent).
  [D2]  the isotropic (w^2 U) and anisotropic ((w.x)^2 U/r^2) determinations of the
        gauge-invariant alpha_2 AGREE.
"""
import sympy as sp, time, sys

T0 = time.time()
P = lambda *a: print(*a, flush=True)

# ---------------- symbols ----------------
I = sp.I
kx, ky, kz = sp.symbols('k_x k_y k_z', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
wv = [w1, w2, w3]
la = sp.Symbol('la', positive=True)          # boost/w-order counter (omega=la k.w, u^i=la w^i)
eps = sp.Symbol('eps', positive=True)         # field-order counter (truncate eps^2)
Es, Eis = sp.symbols('E_s E_is')              # plane-wave ket / bra bookkeepers
Uh = sp.Symbol('U_hat')
eta = sp.diag(-1, 1, 1, 1)
kvec = [kx, ky, kz]
k2 = kx**2 + ky**2 + kz**2
kw = kx*w1 + ky*w2 + kz*w3
w2s = w1**2 + w2**2 + w3**2
om = la*kw
Kd = [-I*om, I*kx, I*ky, I*kz]                # lower d_mu  (K_0=-omega)
Ku = [sum(eta[a, b]*Kd[b] for b in range(4)) for a in range(4)]

def d(f, mu):
    """derivative of a ket/bra field amplitude: ket -> i K_mu ket, bra -> -i K_mu bra."""
    return sp.diff(f, Es)*(Kd[mu]*Es) + sp.diff(f, Eis)*(-Kd[mu]*Eis)

def trla(e, n=2):
    e = sp.expand(e)
    return sum(e.coeff(la, j)*la**j for j in range(n+1))

def te(e):
    """double truncation: keep eps^i la^j, i,j in {0,1,2}."""
    e = sp.expand(e)
    out = 0
    for i in range(3):
        ci = e.coeff(eps, i)
        for j in range(3):
            out += ci.coeff(la, j)*eps**i*la**j
    return out


# ============================================================================
# field amplitudes (module-level; shared)
# ============================================================================
def nf(tag):
    ket = sp.Symbol(tag+'k'); bra = sp.Symbol(tag+'b')
    return ket*Es + bra*Eis, ket, bra

# metric perturbation h_{mn} (g = eta + eps h), 10 generic components
hh = {}; hk = {}; hb = {}
for m in range(4):
    for n in range(m, 4):
        f, kk, bb = nf(f'h{m}{n}'); hh[(m, n)] = f; hh[(n, m)] = f; hk[(m, n)] = kk; hb[(m, n)] = bb
# aether spatial perturbation a_i (lower), i=1,2,3 ; a_0 from unit constraint
af = []; ak = []; ab = []
for i in range(3):
    f, kk, bb = nf(f'a{i+1}'); af.append(f); ak.append(kk); ab.append(bb)
# scalar perturbation varphi ; source rho
vp, vpk, vpb = nf('vp')
rho, Rk, Rb = nf('rho')

ALLK = [hk[(m, n)] for m in range(4) for n in range(m, 4)] + ak + [vpk]
ALLB = [hb[(m, n)] for m in range(4) for n in range(m, 4)] + ab + [vpb]

def DC(e):
    """diagonal ket-bra part (|amplitude|^2) : keep monomials with equal Es,Eis powers."""
    e = sp.expand(e)
    pol = sp.Poly(e, Es, Eis)
    out = 0
    for mon, cc in zip(pol.monoms(), pol.coeffs()):
        if mon[0] == mon[1]:
            out += cc*(Es*Eis)**mon[0]
    return out.subs(Es*Eis, 1) if out != 0 else out


def build_L2(KBv, K2v, Q0v, JYv, c2sv, dark_on):
    """assemble the DC-reduced quadratic Lagrangian L2 (Gt=1)."""
    KB = sp.nsimplify(KBv); K2 = sp.nsimplify(K2v); Q0 = sp.nsimplify(Q0v)
    JY = sp.nsimplify(JYv); c2s = sp.nsimplify(c2sv)
    # metric
    H = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            H[m, n] = hh[(m, n)]
    gd = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps*H[m, n])
    Hup = eta*H*eta
    gu = sp.Matrix(4, 4, lambda a, b: (eta - eps*Hup + eps**2*(Hup*H*eta))[a, b])
    trH = sum(eta[m, n]*H[m, n] for m in range(4) for n in range(4))
    HH = sum(Hup[m, n]*H[m, n] for m in range(4) for n in range(4))
    sqg = 1 + eps*trH/2 + eps**2*(trH**2/8 - HH/4)

    # aether lower A_mu = (-1,0,0,0) + eps(dA0, a1,a2,a3), dA0 from constraint A.A=-1
    dA0 = sp.Symbol('dA0_tmp')
    Adn0 = sp.Matrix([-1 + eps*dA0, eps*af[0], eps*af[1], eps*af[2]])
    Aup0 = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn0[k] for k in range(4)))
    C1 = sp.expand(te(sum(Aup0[i]*Adn0[i] for i in range(4)) + 1)).coeff(eps, 1)
    dA0sol = sp.solve(sp.expand(C1).coeff(Es, 1), dA0)
    dA0v = dA0sol[0] if dA0sol else sp.S(0)
    Adn = sp.Matrix([-1 + eps*dA0v, eps*af[0], eps*af[1], eps*af[2]])
    Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))

    # scalar phi = Q0 t + eps varphi ; d_mu phi (lower)
    dphi = sp.Matrix([Q0 + eps*d(vp, 0), eps*d(vp, 1), eps*d(vp, 2), eps*d(vp, 3)])

    # ---- EH: genuine sqrt(-g) R (truncated) ----
    gdT = sp.Matrix(4, 4, lambda m, n: te(gd[m, n]))
    guT = sp.Matrix(4, 4, lambda m, n: te(gu[m, n]))
    Gam = [[[te(sp.Rational(1, 2)*sum(guT[r, s]*(d(gdT[s, n], m)+d(gdT[s, m], n)-d(gdT[m, n], s))
             for s in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]

    def ric(a, b):
        o = 0
        for m in range(4):
            o += d(Gam[m][b][a], m) - d(Gam[m][m][a], b)
            for l in range(4):
                o += te(Gam[m][m][l]*Gam[l][b][a] - Gam[m][b][l]*Gam[l][m][a])
        return te(o)
    Rsc = te(sum(guT[m, n]*ric(m, n) for m in range(4) for n in range(4)))

    def grade(e):
        e = sp.expand(e); return [trla(e.coeff(eps, n)) for n in range(3)]
    gsq = grade(sqg); gR = grade(Rsc)
    L2 = trla(sum(gsq[a]*gR[2-a] for a in range(3)))     # sqrt(-g) R at eps^2

    if dark_on:
        AupT = sp.Matrix(4, 1, lambda i, j: te(Aup[i]))
        dphiT = sp.Matrix(4, 1, lambda i, j: te(dphi[i]))
        # F_{mn}=d_m A_n - d_n A_m ; F^2
        Fmn = sp.Matrix(4, 4, lambda m, n: sp.expand(d(Adn[n], m) - d(Adn[m], n)))
        F1 = sp.Matrix(4, 4, lambda m, n: Fmn[m, n].coeff(eps, 1))
        F2 = eps**2*sum(F1[m, n]*F1[a, b]*eta[m, a]*eta[n, b]
                        for m in range(4) for n in range(4) for a in range(4) for b in range(4))
        # covariant divergence div A = d_mu A^mu + Gam^mu_{mu r} A^r
        divA = te(sum(d(AupT[m], m) for m in range(4))
                  + sum(Gam[m][m][r]*AupT[r] for m in range(4) for r in range(4)))
        divA2 = te(divA**2)
        # J^mu = A^nu(d_nu A^mu + Gam^mu_{nu r} A^r)
        Jup = [te(sum(AupT[nu]*(d(AupT[al], nu) + sum(Gam[al][nu][r]*AupT[r] for r in range(4)))
                     for nu in range(4))) for al in range(4)]
        Jdphi = te(sum(Jup[m]*dphiT[m] for m in range(4)))
        Qc = te(sum(AupT[m]*dphiT[m] for m in range(4)))
        Yc = te(sum((guT[m, n] + AupT[m]*AupT[n])*dphiT[m]*dphiT[n]
                    for m in range(4) for n in range(4)))
        dQ = Qc - Q0
        Kq = K2*te(dQ**2)
        gF2 = grade(F2); gdivA2 = grade(divA2); gJ = grade(Jdphi)
        gY = grade(Yc); gK = grade(Kq)
        gDark = [-(KB/2)*gF2[n] + c2s*gdivA2[n] + 2*(2-KB)*gJ[n]
                 - (2-KB)*(1+JY)*gY[n] - gK[n] for n in range(3)]
        L2 += trla(sum(gsq[a]*gDark[2-a] for a in range(3)))

    # ---- moving-dust matter: L_matter = 8 pi Gt sum h_mn T^{mn}, T^{mn}=rho u^m u^n ----
    gam = 1 + la**2*w2s/2
    uup = [gam, la*gam*w1, la*gam*w2, la*gam*w3]
    Tup = {(m, n): trla(rho*uup[m]*uup[n]) for m in range(4) for n in range(4)}
    Lmatt = 8*sp.pi*trla(sum(H[m, n]*Tup[(m, n)] for m in range(4) for n in range(4)))
    L2 = sp.expand(L2 + Lmatt)
    # fix k=(1,0,0)
    L2 = sp.expand(L2.subs({ky: 0, kz: 0, kx: 1}))
    return DC(L2)


# ============================================================================
# harmonic-gauge conditions (k=(1,0,0)): omega hbar_{0n} + hbar_{1n} = 0
# ============================================================================
def harmonic_conditions_ket():
    """4 conditions in the h KET symbols; om = la*w1 (since k=(1,0,0), k.w=w1)."""
    omv = la*w1
    trHk = sum(eta[a, b]*hk[(a, b)] for a in range(4) for b in range(4))
    def hbar(m, n): return hk[(m, n)] - sp.Rational(1, 2)*eta[m, n]*trHk
    return [sp.expand(omv*hbar(0, n) + hbar(1, n)) for n in range(4)]


def lin_solve(eqs, unks):
    M, b = sp.linear_eq_to_matrix(eqs, unks)
    sol = list(sp.linsolve((M, b), unks))
    return dict(zip(unks, sol[0])) if sol else None


def solve(KBv, K2v, Q0v, JYv, c2sv, dark_on):
    L2 = build_L2(KBv, K2v, Q0v, JYv, c2sv, dark_on)
    # active field bras / kets
    if dark_on:
        active_b = ALLB
        active_k = ALLK
    else:
        active_b = [hb[(m, n)] for m in range(4) for n in range(m, 4)]
        active_k = [hk[(m, n)] for m in range(4) for n in range(m, 4)]
    # EOMs: vary each active bra
    eqs_eom = [sp.expand(sp.diff(L2, B)) for B in active_b]
    harm = harmonic_conditions_ket()
    eqs = eqs_eom + harm
    # order-by-order in la solve
    c0 = {A: sp.Symbol(f'c0_{A}') for A in active_k}
    c1 = {A: sp.Symbol(f'c1_{A}') for A in active_k}
    c2 = {A: sp.Symbol(f'c2_{A}') for A in active_k}
    sub = {A: c0[A] + la*c1[A] + la**2*c2[A] for A in active_k}
    eqsub = [sp.expand(trla(e.subs(sub))) for e in eqs]
    # la^0
    e0 = [sp.expand(e.coeff(la, 0)) for e in eqsub]
    e0 = [e for e in e0 if e != 0]
    s0 = lin_solve(e0, list(c0.values()))
    if s0 is None:
        return ('static-fail',)
    # la^1
    e1 = [sp.expand(e.coeff(la, 1).subs(s0)) for e in eqsub]
    e1 = [e for e in e1 if e != 0]
    s1 = lin_solve(e1, list(c1.values()))
    if s1 is None:
        return ('w1-fail',)
    # la^2
    e2 = [sp.expand(e.coeff(la, 2).subs(s0).subs(s1)) for e in eqsub]
    e2 = [e for e in e2 if e != 0]
    s2 = lin_solve(e2, list(c2.values()))
    if s2 is None:
        return ('w2-fail',)

    def kv(A):
        return sp.expand(c0[A].subs(s0) + la*c1[A].subs(s1) + la**2*c2[A].subs(s2))
    hsol = {(m, n): kv(hk[(m, n)]) for m in range(4) for n in range(m, 4)}
    return ('ok', hsol)


# ============================================================================
# PPN extraction (GR-gate validated): a+b, 2b+d
# ============================================================================
def extract(hsol):
    """read (A_V,A_W) from g_0i (la^1) and (c_F,d_F) from g_00 (la^2); form a,b,c,d.
    Newton normalisation: h_00(la^0) = 2 Uhat defines Uhat.  k=(1,0,0)."""
    def H(m, n): return hsol[(m, n)] if (m, n) in hsol else hsol[(n, m)]
    # Newton: h00 at la^0 -> 2 Uhat.  Express solution amplitude in Uhat via Rk relation.
    h00_0 = sp.expand(H(0, 0).coeff(la, 0))
    # h00_0 is linear in Rk; define Uhat = h00_0/2 -> substitute Rk so h00_0 = 2 Uhat
    # (source Rk cancels in the ratios a,b,c,d, so just read coefficients relative to h00_0/2)
    # g_0i (la^1)
    AV, AW = sp.symbols('A_V A_W')
    g0 = [sp.expand(H(0, i+1).coeff(la, 1)) for i in range(3)]
    # k=(1,0,0): (k.w)k_i/k^2 = w1 delta_{i,1}.  structures: w_i and w1 delta_{i1}
    # g_01 = (AV+AW) w1 ; g_02 = AV w2 ; g_03 = AV w3
    AV_val = sp.expand(g0[1]).coeff(w2)          # from g_02 = AV w2
    tot01 = sp.expand(g0[0]).coeff(w1)           # = AV+AW
    AW_val = sp.expand(tot01 - AV_val)
    # normalise by Uhat = h00_0/2
    Uh_amp = h00_0/2
    a = sp.simplify((AV_val + AW_val/2)/Uh_amp)
    b = sp.simplify((-AW_val/2)/Uh_amp)
    # g_00 (la^2): g00w = cF w^2 + dF w1^2  (since (k.w)^2/k^2 = w1^2)
    g00w = sp.expand(H(0, 0).coeff(la, 2))
    cF = sp.expand(g00w).coeff(w2**2)            # transverse w^2 coeff
    tot_w1 = sp.expand(g00w).coeff(w1**2)        # = cF + dF
    dF = sp.expand(tot_w1 - cF)
    c = sp.simplify((cF + dF/2)/Uh_amp)
    d = sp.simplify((-dF/2)/Uh_amp)
    return a, b, c, d


if __name__ == '__main__':
    P("="*80); P("GR-LIMIT GATE (dark OFF): must reproduce GR gate (a,b,d)=(-4,0,-1), alpha=0")
    P("="*80)
    r = solve(0, 0, 0, 0, 0, dark_on=False)
    if r[0] != 'ok':
        P(f"  SOLVE FAILED: {r[0]}"); sys.exit(1)
    a, b, c, d = extract(r[1])
    P(f"  (a,b,c,d) = ({a}, {b}, {c}, {d})")
    al1 = sp.simplify(-2*(a+b) - 8)
    al2 = sp.simplify(-(2*b+d) - 1)
    P(f"  a+b = {sp.simplify(a+b)}   (GR expects -4)")
    P(f"  2b+d = {sp.simplify(2*b+d)}  (GR expects -1)")
    P(f"  alpha_1 = {al1}   alpha_2 = {al2}")
    P(f"  [runtime {time.time()-T0:.1f}s]")
