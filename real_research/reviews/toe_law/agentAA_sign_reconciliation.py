#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agentAA — N-series SIGN RECONCILIATION for the inertia-deficit channel (2026-06-11).

Task: reconcile N3's "MOND-signed deficit channel for m^2 < 2H^2" against agentV's Sec 5.2 flag
("Quinn/Yukawa-anchored convention gives deficit <=> M^2 > 2H^2"), in ONE fixed convention,
anchored to agentN1's exact closed-form commutator. Report-only artifact; no repo files patched.

THE FIXED CONVENTION (used for every line below; stated once):
  * signature (-,+,+,+); hbar = c = 1; dS4 with Hubble H; effective mass M^2 = m^2 + 12 xi H^2.
  * worldline coupling: S_int = -Int q phi(z(tau)) dtau  (quintessence m(phi) = m0 + q phi; this is
    N3's coupling, and the soft/charge-type limit of the detector coupling with q^2 <-> lambda^2 <Q^2>,
    exactly the sector N2 [E6] / agentV Sec 1.1 select).
  * field normalization canonical; EOM (Box - M^2) phi = + q mu(x), mu = Int delta^4(x-z) dtau /sqrt(-g);
    Green function (Box - M^2) G_ret = - delta^4/sqrt(-g)  ==>  flat static G = e^{-mr}/(4 pi r)
    ==> phi_self = - q Int G_ret dtau'        [N3's stated convention, verified self-consistent]
  * Hadamard split G_ret = U delta_+ + V theta(inside cone); V = the retarded TAIL, repo normalization
    (BHP Gaussian / 4pi):  V_MMC = +H^2/(4 pi);  V(0+) = -(1/8pi)[m^2 + (xi - 1/6) R]   (N2 [C]).
  * Wightman cut density T(u) = Im W(Z = 1+u-i0), u = Z-1 > 0 the timelike cut. N1's exact commutator
       C_tail(s) = (i/8pi)(M^2-2H^2) sgn(s) 2F1(3/2+nu, 3/2-nu; 2; -u/2),  C = 2i Im W
    ==> T(u) = (M^2-2H^2)/(16 pi) * 2F1(3/2+nu, 3/2-nu; 2; -u/2),   T(0+) = (M^2-2H^2)/(16 pi)
    Dictionary: G_ret = i theta(s) C = -2 theta(s) Im W   ==>   V = -2 T.       [agentV Sec 5.2's V=-2ImW]
  * Deser-Levin family: Z(s) = 1 + 2 beta sinh^2(kappa s/2); kappa = sqrt(a^2+H^2); beta = H^2/kappa^2;
    t = 2 beta = 2H^2/kappa^2 in (0,2]; u(s) = t sinh^2(kappa s/2); du = kappa sqrt(u(u+t)) ds.
  * THE OBSERVABLE (what "inertia deficit" must mean): the total adiabatic stationary inertia
    m_eff = F_ext,e^/a on the family. From the worldline EOM  m(phi) a^mu = -q P^{mu nu} grad_nu phi_self
    + F_ext^mu  (P = g + uu), the EXHAUSTIVE O(q^2) decomposition is
        m_eff - m0 = dm_dress + m_force,
        dm_dress = q phi_self,sat = - q^2 Int_0^inf V ds  = +(2 q^2/kappa) Int T(u) u^{-1/2}(u+t)^{-1/2} du
        m_force  = - F_self,e^ / a                        = -(2 q^2/kappa) Int T(u) dnu_t,
                   dnu_t = (t/2) u^{-1/2}(u+t)^{-3/2} du  (a probability measure; agentV's m_ind EXACTLY)
        TOTAL:   m_eff - m0 = +(2 q^2/kappa) Int_0^inf T(u) (u + t/2) u^{-1/2} (u+t)^{-3/2} du
    The total weight is POSITIVE; the force weight is pointwise <= 1/2 of the dressing weight.
    ==> for an endpoint-dominated/one-signed tail:  DEFICIT <=> T < 0 <=> V > 0 <=> M^2 < 2H^2.

Sections:
  [S0] the slot identity e^.grad_1 Z = a (Z-1), re-derived from the explicit static-patch embedding (sympy)
  [S1] dictionary identities: Hadamard v0 = -(M^2-2H^2)/8pi = -2 T(0+); measure & weight algebra (sympy)
  [S2] FLAT-SPACE YUKAWA ANCHOR (decisive): the scalar cloud's finite dressing is POSITIVE (an EXCESS),
       three independent routes (worldline tail / statics / 2nd-order PT); the four static numbers
       labeled; the -q^2 m/8pi agentV quotes is the FIELD-ENERGY-ONLY piece (scalar) or the TOTAL for
       the VECTOR (Proca) case -- not the scalar inertia dressing. Flat space has M^2 = m^2 > 0 = 2H^2
       (heavy side) ==> rule predicts EXCESS: consistent.
  [S3] BHP dS ANCHOR: MMC (M^2 = 0 < 2H^2): d(dm)/dtau = -q^2 H^2/4pi < 0 (BHP mass loss) ==> DEFICIT.
  [S4] numerics on the family: dressing/force/total for M^2/H^2 on both sides of 2, both series,
       t in {0.2, 1.0, 1.9}; one-signedness scans; by-parts echo of agentV's force formula (finite-U0
       exact identity); |force| <= |dressing|/2; sign(total) = sign(M^2-2H^2).
  [S5] corrected-kernel structural echo: the TOTAL-inertia kernel is analytic in t at t = 2 (slope -> 1
       in a^2), so agentV's NO-KERNEL theorem at a -> 0 survives the kernel correction verbatim.
  [S6] the sign-knee disjointness numbers (deficit window mass ceiling vs N2's knee window), both footings.

Units: H = 1, q = 1 in [S4]/[S5]. Every check prints PASS/FAIL; summary at the end.
"""

import sys, time
import sympy as sp
import mpmath as mp

T0 = time.time()
PASS, FAIL = [], []

def emit(*args):
    print(" ".join(str(a) for a in args))

def check(name, cond):
    (PASS if cond else FAIL).append(name)
    emit(("[PASS]" if cond else "[FAIL]"), name)

emit("=" * 110)
emit("[S0] The slot identity e^.grad_1 Z = a (Z-1) on the Deser-Levin family -- re-derived from the embedding (sympy)")
emit("=" * 110)
# Static-patch comoving-at-r0 worldline, embedding X.X = 1/H^2 in 5D Minkowski (-,+,+,+,+).
# Variables: rho = H r0 in (0,1); theta = kappa tau; sigma = kappa s; kappa = H/sqrt(1-rho^2).
H, rho = sp.symbols('H rho', positive=True)
th, sg = sp.symbols('theta sigma', positive=True)
A = sp.sqrt(1 - rho**2) / H
kap = H / sp.sqrt(1 - rho**2)

def Xemb(t):
    return sp.Matrix([A * sp.sinh(t), A * sp.cosh(t), rho / H, 0, 0])

eta5 = sp.diag(-1, 1, 1, 1, 1)
def dot5(v, w):
    return (v.T * eta5 * w)[0, 0]

Xt, Xp = Xemb(th), Xemb(th - sg)
u_vec = kap * sp.diff(Xt, th)                  # d/dtau = kappa d/dtheta
acc   = kap**2 * sp.diff(Xt, th, 2)
check("S0.1 u.u = -1 (proper-time normalization)", sp.simplify(dot5(u_vec, u_vec) + 1) == 0)
check("S0.2 xdd.X = 1 (constraint curvature term)", sp.simplify(dot5(acc, Xt) - 1) == 0)
a_intr = acc - H**2 * dot5(acc, Xt) * Xt       # project out the embedding normal n = H X (n.n = 1)
a_prop = H * rho / sp.sqrt(1 - rho**2)          # proper acceleration a = H^2 r0 / sqrt(1 - H^2 r0^2)
check("S0.3 a_intr^2 = a^2 = kappa^2 - H^2", sp.simplify(dot5(a_intr, a_intr) - a_prop**2) == 0)
check("S0.4 e^.X(tau) = 0 (e^ tangent)", sp.simplify(dot5(a_intr, Xt)) == 0)
Z = H**2 * dot5(Xt, Xp)
beta = H**2 / (a_prop**2 + H**2)
check("S0.5 Z = 1 + 2 beta sinh^2(kappa s/2)  [N1 [A1] pullback]",
      sp.simplify(Z - (1 + 2 * beta * sp.sinh(sg / 2)**2)) == 0)
# Unnormalized (radical-free) form: e^ = a_intr/a  =>  a * (e^.grad_1 Z) = H^2 (a_intr.X'), so the slot
# identity e^.grad_1 Z = a (Z-1) is equivalent to  H^2 (a_intr.X') = a^2 (Z-1)  with a^2 rational in rho:
check("S0.6a H^2 (a_intr.X') = a^2 (Z - 1)   [the slot identity, unnormalized, SIGN INCLUDED]",
      sp.simplify(H**2 * dot5(a_intr, Xp) - a_prop**2 * (Z - 1)) == 0)
# and the normalized form numerically (sympy's radical denesting balks; the residual is machine zero):
lhs = H**2 * dot5(a_intr / sp.sqrt(dot5(a_intr, a_intr)), Xp)   # e^.grad_1 Z = H^2 (e^.X')
fnum = sp.lambdify((H, rho, th, sg), lhs - a_prop * (Z - 1), 'mpmath')
probes = [(1.0, 0.5, 0.3, 0.7), (2.0, 0.9, 1.1, 0.2), (0.7, 0.2, 2.0, 1.5)]
resid = max(abs(fnum(*p)) for p in probes)
check("S0.6b e^.grad_1 Z = a (Z - 1) numerically at 3 probes (max residual %.1e)" % float(resid),
      resid < 1e-12)
emit("  => for any invariant F(Z): e^.grad_1 F = a (Z-1) F'(Z). Both agentV's in-in force and the classical")
emit("     gradient self-force -q e^.grad phi_self use THIS identity: F_e^ = -2 q^2 a Int (Z-1) ImW'(Z) ds,")
emit("     i.e. agentV's <F> = -2 lambda^2 Im Int g e^.grad_1 W with g -> <Q^2> real. Same formula, same sign.")

emit("")
emit("=" * 110)
emit("[S1] Dictionary identities (sympy): N1 coefficient -> T(0+), V = -2T, Hadamard v0; measure algebra")
emit("=" * 110)
m2, xi, u, t = sp.symbols('m2 xi u t', positive=True)
M2 = m2 + 12 * xi * H**2
RdS = 12 * H**2
v0_hadamard = -(sp.Rational(1, 8) / sp.pi) * (m2 + (xi - sp.Rational(1, 6)) * RdS)
check("S1.1 Hadamard v0 = -(1/8pi)[m^2+(xi-1/6)R] = -(M^2-2H^2)/8pi  (xi folds into M^2; flip point is M^2=2H^2)",
      sp.simplify(v0_hadamard + (M2 - 2 * H**2) / (8 * sp.pi)) == 0)
# N1: C_tail coefficient (i/8pi)(M^2-2H^2) sgn(s); C = 2i ImW  => T(0+) = (M^2-2H^2)/16pi;  V = -2T:
T0p = (M2 - 2 * H**2) / (16 * sp.pi)
check("S1.2 V(0+) = -2 T(0+) reproduces the Hadamard v0 exactly (N1 <-> N2/N3 <-> V dictionaries agree)",
      sp.simplify(v0_hadamard - (-2 * T0p)) == 0)
emit("  MMC check: M^2=0 => V(0+) = +H^2/4pi (BHP constant tail, N1 S4/N3 S1), T(0+) = -H^2/8pi.")
emit("  Conformal check: M^2 = 2H^2 => both zero (agentF's Huygens corner).")
w_d = 1 / (sp.sqrt(u) * sp.sqrt(u + t))                       # dressing weight (from du = kappa sqrt(u(u+t)) ds)
w_f = t / (2 * sp.sqrt(u) * (u + t)**sp.Rational(3, 2))       # force weight = dnu_t/du (agentV's measure)
check("S1.3 d/du[sqrt(u)/sqrt(u+t)] = w_f  (the by-parts identity behind agentV [V-A4])",
      sp.simplify(sp.diff(sp.sqrt(u) / sp.sqrt(u + t), u) - w_f) == 0)
check("S1.4 Int_0^inf dnu_t = 1 (probability measure)",
      sp.simplify(sp.integrate(w_f, (u, 0, sp.oo)) - 1) == 0)
check("S1.5 w_d - w_f = (u + t/2) u^{-1/2}(u+t)^{-3/2}  > 0  (the TOTAL-inertia weight: positive everywhere)",
      sp.simplify((w_d - w_f) - (u + t / 2) / (sp.sqrt(u) * (u + t)**sp.Rational(3, 2))) == 0)
check("S1.6 w_f/w_d = (t/2)/(u+t) <= 1/2  (force piece pointwise bounded by HALF the dressing)",
      sp.simplify(w_f / w_d - t / (2 * (u + t))) == 0)
emit("  => TOTAL = dressing + force = +(2q^2/kappa) Int T(u) (u+t/2) u^{-1/2}(u+t)^{-3/2} du.")
emit("     The force piece (agentV's m_ind) is OPPOSITE-signed to the dressing and can never flip the total:")
emit("     total/dressing in [1/2, 1] for one-signed T. The deficit assignment is therefore the DRESSING's.")

emit("")
emit("=" * 110)
emit("[S2] FLAT-SPACE YUKAWA ANCHOR (the decisive external pin): scalar cloud dressing is an EXCESS, +q^2 m")
emit("=" * 110)
mm, s_, r_, k_, Lam = sp.symbols('m s r k Lambda', positive=True)
# Route 1 -- worldline tail: V_flat(s) = -(m/4pi) J1(ms)/s  (the H->0 limit of the dictionary; N1 [D2]):
J_int = sp.integrate(sp.besselj(1, mm * s_) / s_, (s_, 0, sp.oo))
check("S2.1 Int_0^inf J1(ms)/s ds = 1  =>  Int V_flat ds = -m/4pi", sp.simplify(J_int - 1) == 0)
emit("  dm_dress = -q^2 Int V ds = +q^2 m/(4 pi)  > 0   [worldline route: EXCESS]")
# Route 2 -- statics: phi_self = -q G_static, G_static = e^{-mr}/4pi r; finite (m-dependent) part:
finite = sp.limit((sp.exp(-mm * r_) - 1) / (4 * sp.pi * r_), r_, 0)
check("S2.2 static Green finite part: (e^{-mr}-1)/(4pi r) -> -m/4pi  (equals the tail integral: same object)",
      sp.simplify(finite + mm / (4 * sp.pi)) == 0)
emit("  phi_self,finite = -q*(-m/4pi) = +q m/4pi;  dm_dress = q phi_self = +q^2 m/(4 pi)  [statics: EXCESS]")
# Route 3 -- second-order perturbation theory (independent regularization):
I_PT = sp.integrate(k_**2 / (k_**2 + mm**2), (k_, 0, Lam))
check("S2.3 Int_0^Lam k^2/(k^2+m^2) dk = Lam - m atan(Lam/m)   [-> Lam - pi m/2]",
      sp.simplify(I_PT - (Lam - mm * sp.atan(Lam / mm))) == 0)
emit("  Delta E = -q^2 Int d^3k/((2pi)^3 2 w_k^2) = -(q^2/4pi^2) Lam + q^2 m/(8 pi):")
emit("  the divergence is NEGATIVE (cloud binding -> renormalized into m0, = N1's universal contact term);")
emit("  the m-dependent FINITE part is +q^2 m/(8 pi) > 0  [energy route: EXCESS; half the EOM dressing, same sign]")
emit("")
emit("  THE STATIC LEDGER (per q^2; scalar exchange is ATTRACTIVE, phi_self < 0), all four numbers:")
emit("    E_field (field energy only)      finite part = - m/8pi   <-- the number agentV Sec 5.2 quotes")
emit("    E_int   (interaction term)       finite part = + m/4pi")
emit("    E_total (= the self-energy)      finite part = + m/8pi   EXCESS")
emit("    q phi_self (EOM inertia dressing)            = + m/4pi   EXCESS  (the Quinn dynamical-mass object)")
emit("  VECTOR (Proca) CONTRAST: repulsive exchange, E_total finite = - m/8pi  (a deficit) -- the sign agentV's")
emit("  'Yukawa cloud negative self-energy -q^2 m/8pi (a deficit)' anchor actually belongs to. For the SCALAR")
emit("  worldline coupling every memo here uses, the inertia-relevant finite parts are POSITIVE.")
emit("")
emit("  Consistency with the deficit rule: flat space has 2H^2 = 0, so M^2 = m^2 > 2H^2 ALWAYS (heavy side);")
emit("  rule 'deficit <=> M^2 < 2H^2' predicts EXCESS in flat space -- confirmed by all three routes.")
emit("  (Corollary: the deficit channel is intrinsically de Sitter -- it needs M^2 < 2H^2, impossible at H=0.)")

emit("")
emit("=" * 110)
emit("[S3] BHP dS ANCHOR: MMC (M^2 = 0 < 2H^2) -- the deficit side, literature-pinned")
emit("=" * 110)
emit("  V_MMC = +H^2/4pi (constant inside the cone; N1 S4 = BHP gr-qc/0201020 eq 6.1 / 4pi).")
emit("  d(dm_dress)/dtau = -q^2 V = -q^2 H^2/(4 pi) < 0: secular mass LOSS = BHP eq 6.8 (dm/dtau = -q^2 H^2,")
emit("  Gaussian) -- 'the charge loses all its mass in finite proper time'. DEFICIT, exactly as N3 carries it.")
emit("  T(0+) = -H^2/8pi < 0: the deficit-iff-T<0 rule reproduces it. Both anchors (S2 flat-excess, S3 dS-deficit)")
emit("  sit on OPPOSITE sides of M^2 = 2H^2 and BOTH land on N3's assignment.")

emit("")
emit("=" * 110)
emit("[S4] Numerics on the Deser-Levin family: dressing / force / total across M^2/H^2 and t (mpmath)")
emit("=" * 110)
mp.mp.dps = 15

_tcache = {}
def Tcut(x, uu):
    """T(u) = (x-2)/(16 pi) 2F1(3/2+nu, 3/2-nu; 2; -u/2), x = M^2/H^2, H = 1."""
    key = (x, mp.nstr(uu, 12))
    if key in _tcache:
        return _tcache[key]
    xm = mp.mpf(x)
    nu2 = mp.mpf(9) / 4 - xm
    if nu2 >= 0:
        nu = mp.sqrt(nu2)
        f = mp.hyp2f1(mp.mpf(3) / 2 + nu, mp.mpf(3) / 2 - nu, 2, -uu / 2)
    else:
        nu = mp.mpc(0, 1) * mp.sqrt(-nu2)
        f = mp.hyp2f1(mp.mpf(3) / 2 + nu, mp.mpf(3) / 2 - nu, 2, -uu / 2)
        assert abs(mp.im(f)) < 1e-10 * (1 + abs(f)), "principal-series 2F1 not real"
        f = mp.re(f)
    val = (xm - 2) / (16 * mp.pi) * f
    _tcache[key] = val
    return val

def integrals(x, tval, U0=mp.mpf('1e8')):
    """Return (I_dress, I_force, I_total, tailnote) where
       I_dress = Int_0^inf T u^{-1/2}(u+t)^{-1/2} du   (m_dress  = +(2/kappa) I_dress)
       I_force = Int_0^inf T dnu_t                      (m_force = -(2/kappa) I_force; agentV's E_t[T])
       I_total = I_dress - I_force                       (m_total = +(2/kappa) I_total)
       computed in w = sqrt(u) (regular at 0) on [0, sqrt(U0)] + analytic large-u tail (complementary)."""
    tv = mp.mpf(tval)
    W0 = mp.sqrt(U0)
    segs = [mp.mpf(0), mp.mpf('0.5'), 2, 8, 30, 120, 500, 2500, W0]
    fd = lambda w: 2 * Tcut(x, w * w) / mp.sqrt(w * w + tv)
    ff = lambda w: 2 * Tcut(x, w * w) * (tv / 2) / (w * w + tv)**mp.mpf('1.5')
    I_d = mp.quad(fd, segs)
    I_f = mp.quad(ff, segs)
    tailnote = "tail<1e-10"
    nu2 = mp.mpf(9) / 4 - mp.mpf(x)
    if x != 2.0 and nu2 > 0:
        nu = mp.sqrt(nu2)
        hm, hp = mp.mpf(3) / 2 - nu, mp.mpf(3) / 2 + nu
        Am = mp.gamma(2 * nu) / (mp.gamma(mp.mpf(3) / 2 + nu) * mp.gamma(mp.mpf(1) / 2 + nu))
        Ap = mp.gamma(-2 * nu) / (mp.gamma(mp.mpf(3) / 2 - nu) * mp.gamma(mp.mpf(1) / 2 - nu))
        pref = (mp.mpf(x) - 2) / (16 * mp.pi)
        Tas = pref * (Am * (U0 / 2)**-hm + Ap * (U0 / 2)**-hp)
        rel = abs(Tas - Tcut(x, U0)) / (abs(Tcut(x, U0)) + mp.mpf('1e-60'))
        tail_d = tail_f = mp.mpf(0)
        for A_, h_ in ((Am, hm), (Ap, hp)):
            tail_d += pref * A_ * 2**h_ * (U0**-h_ / h_ - (tv / 2) * U0**(-1 - h_) / (1 + h_))
            tail_f += pref * A_ * 2**h_ * (tv / 2) * U0**(-1 - h_) / (1 + h_)
        I_d += tail_d
        I_f += tail_f
        tailnote = "tail_d/I_d=%s asym-relerr=%s" % (mp.nstr(tail_d / (I_d + mp.mpf('1e-60')), 3), mp.nstr(rel, 3))
    return I_d, I_f, I_d - I_f, tailnote

# --- one-signedness scans -------------------------------------------------------------------------
emit("One-signedness of T(u) (33-point log grid, u in [1e-6, 1e10]):")
for x in (0.5, 1.0, 1.9, 2.2):
    sgns = set()
    for i in range(33):
        uu = mp.mpf(10)**(-6 + i * 0.5)
        sgns.add(int(mp.sign(Tcut(x, uu))))
    expected = int(mp.sign(x - 2))
    check("S4.0 T one-signed = sign(M^2-2H^2) at M^2/H^2=%s (complementary)" % x, sgns == {expected})
for x in (4.0, 9.0):
    firstflip, prevs = None, None
    T00 = Tcut(x, mp.mpf('1e-6'))
    for i in range(33):
        uu = mp.mpf(10)**(-6 + i * 0.5)
        sg_ = int(mp.sign(Tcut(x, uu)))
        if prevs is not None and sg_ != prevs and firstflip is None:
            firstflip = (uu, abs(Tcut(x, uu)) / abs(T00))
        prevs = sg_
    if firstflip:
        emit("  M^2/H^2=%s (principal): T oscillates; first sign change near u ~ %s where |T|/|T(0+)| ~ %s"
             % (x, mp.nstr(firstflip[0], 3), mp.nstr(firstflip[1], 3)))
    else:
        emit("  M^2/H^2=%s (principal): no sign change found on the grid" % x)

# --- the main table --------------------------------------------------------------------------------
emit("")
emit("Main table (H = 1, q = 1; m_dress = +(2/kappa) I_d, m_force = -(2/kappa) I_f, m_total = +(2/kappa) I_tot):")
emit("%-8s %-6s %-8s %12s %12s %12s %10s %9s  %s" %
     ("M^2/H^2", "t", "a/H", "m_dress", "m_force", "m_total", "|f|/|d|", "verdict", "tail"))
rows_ok_sign, rows_ok_half, rows_ok_opp = True, True, True
for x in (0.5, 1.0, 1.9, 2.0, 2.2, 4.0, 9.0):
    for tval in (0.2, 1.0, 1.9):
        kappa = mp.sqrt(mp.mpf(2) / tval)
        aH = mp.sqrt(mp.mpf(2) / tval - 1)
        if x == 2.0:
            emit("%-8s %-6s %-8s %12s %12s %12s %10s %9s  %s" %
                 (x, tval, mp.nstr(aH, 4), "0 (exact)", "0 (exact)", "0 (exact)", "-", "CONFORMAL",
                  "T == 0 identically (the Huygens point)"))
            continue
        I_d, I_f, I_tot, note = integrals(x, tval)
        m_d = 2 / kappa * I_d
        m_f = -2 / kappa * I_f
        m_tot = 2 / kappa * I_tot
        verdict = "DEFICIT" if m_tot < 0 else "EXCESS"
        expected = "DEFICIT" if x < 2 else "EXCESS"
        ratio = abs(I_f) / abs(I_d)
        rows_ok_sign &= (verdict == expected)
        rows_ok_half &= (ratio <= 0.5 + 1e-9)
        rows_ok_opp &= (mp.sign(m_f) == -mp.sign(m_d))
        emit("%-8s %-6s %-8s %12s %12s %12s %10s %9s  %s" %
             (x, tval, mp.nstr(aH, 4), mp.nstr(m_d, 6), mp.nstr(m_f, 6), mp.nstr(m_tot, 6),
              mp.nstr(ratio, 4), verdict, note))
check("S4.1 sign(m_total) = sign(M^2-2H^2) on EVERY row: DEFICIT <=> M^2 < 2H^2 (both series, all t)",
      rows_ok_sign)
check("S4.2 |I_force| <= |I_dress|/2 on every row (the pointwise bound, integrated)", rows_ok_half)
check("S4.3 m_force opposite-signed to m_dress on every row (agentV's piece is real -- and subdominant)",
      rows_ok_opp)

# --- by-parts echo: agentV's force formula vs the T'-route, exact at finite U0 ----------------------
emit("")
emit("By-parts echo of agentV [V-A4] (finite-U0 exact identity, boundary terms included):")
mp.mp.dps = 25
_tcache.clear()
for (x, tval) in ((1.0, 1.0), (4.0, 0.5)):
    tv = mp.mpf(tval)
    U0 = mp.mpf(100)

    def Tprime(uu):
        xm = mp.mpf(x)
        nu2 = mp.mpf(9) / 4 - xm
        nu = mp.sqrt(nu2) if nu2 >= 0 else mp.mpc(0, 1) * mp.sqrt(-nu2)
        f = mp.hyp2f1(mp.mpf(5) / 2 + nu, mp.mpf(5) / 2 - nu, 3, -uu / 2)
        f = mp.re(f) if isinstance(f, mp.mpc) else f
        return -(xm - 2) * xm / (64 * mp.pi) * f   # d/du of T via d2F1: (h+ h-)=x, c=2 -> 3, chain rule -1/2

    lhsI = mp.quad(lambda uu: Tprime(uu) * mp.sqrt(uu) / mp.sqrt(uu + tv), [0, 1, 10, U0])
    rhsI = (Tcut(x, U0) * mp.sqrt(U0) / mp.sqrt(U0 + tv)
            - mp.quad(lambda uu: Tcut(x, uu) * (tv / 2) / (mp.sqrt(uu) * (uu + tv)**mp.mpf('1.5')),
                      [0, 1, 10, U0]))
    rel = abs(lhsI - rhsI) / abs(rhsI)
    check("S4.4 Int_0^U0 T' sqrt(u)/sqrt(u+t) du = [T sqrt(u)/sqrt(u+t)]_0^U0 - Int_0^U0 T dnu_t  "
          "(x=%s, t=%s; rel %s)" % (x, tval, mp.nstr(rel, 3)), rel < mp.mpf('1e-12'))
mp.mp.dps = 15
_tcache.clear()

emit("")
emit("=" * 110)
emit("[S5] Corrected-kernel structural echo: the TOTAL-inertia kernel stays analytic at t = 2 (a -> 0)")
emit("=" * 110)
# agentV's NO-KERNEL theorem at the geodesic used analyticity of Int T (u+t)^{-1/2}-type transforms at the
# interior point t = 2. The corrected (total-inertia) kernel (u+t/2) u^{-1/2}(u+t)^{-3/2} is of the same
# class. Echo of agentV [V-D]: log-log slope of [E(2-eps) - E(2)] vs eps -> 1 (linear in a^2) for a test tail.
def Etot_test(tv):
    return mp.quad(lambda w: 2 * mp.exp(-w * w) * (w * w + tv / 2) / (w * w + tv)**mp.mpf('1.5'),
                   [0, 1, 5, 30])
base = Etot_test(mp.mpf(2))
slopes = []
prev = None
for k in range(1, 5):
    eps = mp.mpf(10)**(-k)
    d = Etot_test(2 - eps) - base
    if prev is not None:
        slopes.append(mp.log(prev / d) / mp.log(10))
    prev = d
emit("  test tail T = e^{-u}: slopes of log10|E(2-eps)-E(2)| per decade of eps: %s"
     % ", ".join(mp.nstr(s_, 8) for s_ in slopes))
check("S5.1 slope -> 1.000 (analytic, linear in 2-t prop a^2): NO-KERNEL theorem survives the kernel fix",
      abs(slopes[-1] - 1) < mp.mpf('1e-3'))

emit("")
emit("=" * 110)
emit("[S6] The sign-knee disjointness, under the RECONCILED sign (echo of agentI 2c-i / WHITEPAPER line 194)")
emit("=" * 110)
hbar_eVs = 6.582119569e-16
for label, Hval in (("H_Lambda footing", 1.81e-18), ("H_0 footing (hostile)", 2.19e-18)):
    mc2_max = mp.sqrt(2) * hbar_eVs * Hval     # deficit window ceiling: M < sqrt(2) H
    floor_N2 = 1.3e-29                          # N2's knee-window mass floor [eV]
    dec = mp.log(floor_N2 / mc2_max) / mp.log(10)
    emit("  %s: deficit-window ceiling mc^2 = sqrt(2) hbar H = %s eV; N2 knee floor 1.3e-29 eV"
         % (label, mp.nstr(mc2_max, 4)))
    emit("    => the deficit window sits %s decades BELOW the knee window [1.3e-29, 1.6e-24] eV: DISJOINT."
         % mp.nstr(dec, 3))
emit("  (Echoes N2's 'misses the floor by 3.9 decades (3.8 on the H_0 footing)' EXACTLY -- same gap, now read")
emit("   as the sign-knee one-field contradiction. Under agentV's flipped flag the contradiction would have")
emit("   DISSOLVED (knee-window masses would be MOND-signed); under the reconciled sign it STANDS.)")
emit("  Working-rule note: every sign statement above is structural (no footing, a0-convention, weighting or")
emit("  Upsilon dependence); the only convention-sensitive numbers are the eV ceilings, quoted both footings.")

emit("")
emit("=" * 110)
emit("SUMMARY: %d PASS, %d FAIL%s" % (len(PASS), len(FAIL), "" if not FAIL else "  FAILURES: " + "; ".join(FAIL)))
emit("=" * 110)
emit("DECISIVE LINE (fixed Quinn/PPV convention, anchored to N1's exact (M^2-2H^2) coefficient):")
emit("  total stationary adiabatic inertia  m_eff - m0 = +(2q^2/kappa) Int T(u) (u+t/2) u^{-1/2}(u+t)^{-3/2} du")
emit("  = dressing [+(2q^2/kappa) Int T w_d, the Quinn dynamical-mass piece, N3's object: deficit <=> M^2 < 2H^2]")
emit("  + force    [-(2q^2/kappa) E_t[T],   the gradient self-force,      agentV's object: opposite sign]")
emit("  with |force| <= dressing/2 pointwise and on every computed row: THE TOTAL CARRIES THE DRESSING'S SIGN.")
emit("  ==> THE DEFICIT (MOND-SIGNED) CHANNEL IS  M^2 = m^2 + 12 xi H^2 < 2H^2  (minimal coupling: m^2 < 2H^2).")
emit("  The chain line stands; agentV Sec 5.2's flag rested on the vector-signed (Proca/field-energy-only)")
emit("  Yukawa number and on reading the force-only piece as the inertia. Verdicts of V are sign-independent")
emit("  (its own statement) and survive; only the flag sentence needs retiring.")
emit("runtime: %.1f s" % (time.time() - T0))
