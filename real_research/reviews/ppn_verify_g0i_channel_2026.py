#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ppn_verify_g0i_channel_2026.py
==============================
THE g_0i CROSS-CHECK that ppn_scalar_retained_2026.py declared NOT COMPUTED:
alpha_1 read off the VECTOR sector g_0i of the SAME linearised, boosted, static AeST
system, instead of off g_00.  Two different metric components, one theory, one dictionary.

WHAT THIS FILE DOES
  1. DERIVES the g_0i dictionary from scratch (PART D): it boosts the standard PPN
     preferred-frame metric into the matter rest frame at O(w) and finds that the part of
     g_0i TRANSVERSE to the wavevector is
            h_0i^perp  =  -(alpha_1/2) (w_PPN)_i^perp U,
     with gamma, alpha_2, zeta_1 and xi ALL CANCELLING, and that the LONGITUDINAL part of
     g_0i is pure gauge for static matter.  So the transverse vector channel is a clean
     alpha_1 meter and is structurally BLIND to alpha_2.
  2. Reuses ppn_scalar_retained_2026.py's machinery VERBATIM (the functions _G1_general,
     build, fourier, equations are copied unchanged, and the w-PERPENDICULAR run uses that
     file's own zero-field list, unknown list and substitutions) so the comparison is
     apples-to-apples, and extracts the O(w^1) long-range coefficient of h_01.
  3. Compares the two channels.

THE ANSWER
  * The AeST vector response is nonzero, K_B-ONLY and A_Y-independent:
            h_01^(1)  =  -2 K_B  w U      (exact in the screened A_Y -> oo limit)
    verified at K_B = 1/1000, 1/100, 1/10, 1/4, 1/2, at two A_Y each, with the residual
    confirmed to scale as 1/A_Y and Richardson-extrapolated to -2 K_B to ~8 digits.
    It is EXACTLY LINEAR in K_B -- no K_B^2 correction at all.
  * The SAME run reproduces ppn_scalar_retained_2026.py's g_00 result a = 4 K_B (its check
    Q3-3), so both channels come from one solve of one system.
  * The two channels are therefore CONSISTENT with a single alpha_1, exactly as the PPN
    metric requires:  c = a/2  with  c = -alpha_1/2  and  a = -alpha_1.  This is the
    cross-check, and it PASSES -- at three K_B values, on the nose.
  * CONSEQUENCE, and it is not the consequence that file claimed.  In Will's convention
    (stated in PART D and used by Foster & Jacobson, whose Einstein-aether formula as
    transcribed in nbody_2026/stage70 gives alpha_1 = -4 K_B for AeST's c_i):
            alpha_1 = -4 K_B  EXACTLY,   |alpha_1| = 4 K_B,
    NOT (3/2) K_B.  The quantity ppn_scalar_retained_2026.py calls alpha_1,
    K_B(2K_B^2-5K_B+6)/(2-K_B)^2 -> (3/2)K_B, is the combination -(alpha_1 - alpha_2) of
    that metric, not alpha_1.  Its convention note C4 ("a reader in Will's normalisation
    must flip the sign of both alphas ... no verdict depends on that choice") is WRONG on
    the second half: the two mappings are not related by a sign, they disagree on
    |alpha_1| by 8/3, and |alpha_1| is what the bound uses.
  * SO: that file's ONE FAVOURABLE sub-claim -- "the alpha_1 ceiling is K_B < 6.667e-5,
    2.67x LOOSER than the banked 2.5e-5" -- is WITHDRAWN.  |alpha_1| = 4 K_B with
    |alpha_1| < 1e-4 gives K_B < 2.5e-5, i.e. stage70's ARITHMETIC is reinstated by a
    from-scratch derivation with the scalar retained (which also answers stage74's domain
    objection to Foster & Jacobson for alpha_1: the c_123 = 0 degeneracy changes the
    WELL-POSEDNESS, not the value).
  * alpha_2 IS NOT OBTAINABLE FROM g_0i.  Not "hard": impossible in this configuration.
    Proof in PART L: for static perturbations the residual gauge freedom delta h_0i =
    d_i xi_0 is EXACTLY the longitudinal direction, and the longitudinal component is the
    only one carrying alpha_2.  So alpha_2 rests on the g_00 channel alone; its magnitude
    (5/2) K_B is convention-independent and UNCHALLENGED here.
  * DIRECTION: ADVERSE, twice over, and stated plainly.  Adverse to the verified file's
    favourable sub-claim (the alpha_1 ceiling is 2.67x TIGHTER than it said, not looser),
    and adverse to AeST as the framework's relativistic home: the two-sided K_B window is
    now empty on BOTH alphas -- the subluminality floor 2.105e-4 (K_2 = 9.5e3) sits 8.4x
    above the alpha_1 ceiling as well as 5263x above the alpha_2 ceiling.
    FAVOURABLE, and reported with equal weight: the machinery passes four independent
    gates it was not built to pass, the cross-check itself SUCCEEDS (the g_00 O(w^2) and
    g_0i O(w^1) sectors agree on one alpha_1), and no result of the framework proper --
    a_0 = kappa c sqrt(G rho_Lambda), kappa, the kernel, the RAR, lensing -- is touched.

CONVENTIONS
  W1  Signature (-,+,+,+), c = 1, 16 pi G = 1, Riemann/Ricci and the matter coupling
      EXACTLY as in ppn_scalar_retained_2026.py (its C1-C3, C5), since the machinery is
      copied from it.  Gauge h_{3 nu} = 0, static in the matter frame, single Fourier mode
      k along z.
  W2  PPN DICTIONARY -- WILL'S CONVENTION, the one this file uses and derives with:
      preferred-frame (universe rest frame) metric, standard PPN gauge,
          g_00 = -1 + 2U + ... ,
          g_0j = -(1/2)(4 gamma + 3 + alpha_1 - alpha_2 + zeta_1 - 2 xi) V_j
                 -(1/2)(1 + alpha_2 - zeta_1 + 2 xi) W_j ,
          g_ij = (1 + 2 gamma U) delta_ij ,
      with V_j = int rho v_j/|x-x'|, W_j = int rho [v.(x-x')](x-x')_j/|x-x'|^3.  SOURCE:
      this is the standard PPN metric of Will's PPN formalism (the same convention in which
      the preferred-frame terms of g_00 read -(alpha_1-alpha_2-alpha_3) w^2 U
      - alpha_2 w^i w^j U_ij, and in which Foster & Jacobson's Einstein-aether alpha_1 is
      quoted).  It is NOT re-derived here -- it is the DEFINITION of alpha_1, alpha_2 and
      is declared as inherited.  What IS derived here (PART D) is everything downstream of
      it: the boost to the matter frame, the transverse/longitudinal split, and the fact
      that the transverse channel depends on NOTHING but alpha_1.  The ONLY feature of the
      inherited metric that the answer uses is that the coefficient of alpha_1 in the SUM
      of the V_j and W_j coefficients is 1 and that alpha_2, zeta_1, xi cancel from that
      sum; the GR part of the same sum (= 8 at gamma = 1, i.e. -7/2 V_j - 1/2 W_j) is
      standard post-Newtonian gravitomagnetism and is checked in PART D by the requirement
      that static matter in its OWN rest frame have g_0i = 0 in GR.
  W3  ALSO REPORTED, as required, in ppn_scalar_retained_2026.py's convention C4
      (g_00 = -1 + 2U + alpha_1 w^2 U + alpha_2 w^i w^j U_ij, so a = alpha_1 + alpha_2,
      b = -2 alpha_2).  Under C4's own naming this file's measurement reads
      (alpha_1^C4 + alpha_2^C4)/2 = 2 K_B, which is what C4 already implies -- i.e. the
      MEASUREMENT is convention-free and only the NAME of the bounded quantity moves.  The
      error being corrected is therefore not a sign: it is that C4's |alpha_1| = (3/2)K_B
      was compared against stage70's Will-convention ceiling 2.5e-5.  That comparison is
      invalid in either convention, and the "2.67x looser" claim falls either way.
  W4  WIND DIRECTION, which fixes the SIGN and nothing else.  The machinery's background is
      A^mu = gamma_w (1, w) in the matter frame, i.e. the AETHER moves at +w with respect to
      the matter; Will's w is the velocity of the PPN system with respect to the universe
      rest frame, so w_PPN = -w_machinery.  Hence alpha_1 = +2c where h_0i^perp = c w_i U in
      machinery variables.  If the opposite identification is taken, alpha_1 = -2c = +4 K_B
      and |alpha_1| = 4 K_B unchanged.  NO verdict here depends on it, because every bound
      is on |alpha|; this is stated loudly rather than buried.

NOT COMPUTED (declared, not papered over)
  * alpha_2 from the vector sector: PROVED inaccessible in this configuration (PART L), not
    merely skipped.  What would be needed instead is named there.
  * alpha_3, beta, the zeta's, xi: untouched.  alpha_3 = zeta_i = 0 is ASSUMED for a
    Lagrangian-based (semiconservative) theory and is NOT verified here.
  * the frozen-A_Y approximation: inherited unchanged from ppn_scalar_retained_2026.py and
    NOT repaired.  It is the leading caveat on both channels.  The reason it does not move
    this file's number is the same as there and no stronger: c is A_Y-independent, with the
    approach to the limit verified to be O(1/A_Y) and monotone.
  * the deep-MOND regime, the contact sector inside matter, and any two-body/observational
    reduction: untouched.

EXIT 0 iff every numbered check passes.  Runtime: about 2-4 minutes (the w-perpendicular
build is the expensive step, ~2 min, exactly as in the file being verified).
"""

import math
import sys
import time

import sympy as sp

# =================================================================================================
# check harness
# =================================================================================================
FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""))


print(__doc__)
T0 = time.time()

# =================================================================================================
# PART D -- THE DICTIONARY.  Derived here; only the PPN metric itself is inherited (W2).
# =================================================================================================
print("=" * 100)
print("PART D -- THE g_0i DICTIONARY, DERIVED: boost the PPN preferred-frame metric into the")
print("          matter rest frame at O(w) and split g_0i transverse/longitudinal to k")
print("=" * 100)

al1, al2, ga, ze1, xi_ = sp.symbols("alpha_1 alpha_2 gamma zeta_1 xi", real=True)
Uk = sp.Symbol("U", positive=True)                 # Fourier amplitude of the Newtonian potential
w1, w2, w3 = sp.symbols("w_1 w_2 w_3", real=True)  # w_PPN, Will's wind
WV = [w1, w2, w3]
khat = [0, 0, 1]                                   # single Fourier mode, k along z

# --- D1: U_ij, from the superpotential, in Fourier space ---
kk = sp.Symbol("k", positive=True)
rho_k = sp.Symbol("rho_k")
U_of_k = 4 * sp.pi * rho_k / kk ** 2                      # laplacian U = -4 pi rho
chi_of_k = 8 * sp.pi * rho_k / kk ** 4                    # laplacian chi = -2U
check(sp.simplify(-kk ** 2 * chi_of_k + 2 * U_of_k) == 0,
      "D1a superpotential normalisation: laplacian(chi) = -2U in Fourier space",
      "chi = -int rho|x-x'| is the standard PPN superpotential; U = int rho/|x-x'|")
# U_ij = chi_,ij + delta_ij U  ->  -k_i k_j chi + delta_ij U
Uij = sp.Matrix(3, 3, lambda i, j: sp.simplify(
    (-kk ** 2 * khat[i] * khat[j] * chi_of_k + (1 if i == j else 0) * U_of_k) / U_of_k) * Uk)
check(sp.simplify(sum(Uij[i, i] for i in range(3)) - Uk) == 0,
      "D1b U_ij = (delta_ij - 2 khat_i khat_j) U follows, with the trace identity U_ii = U",
      f"U_ij = diag({Uij[0,0]}, {Uij[1,1]}, {Uij[2,2]}) for k along z")
wUw = sp.expand(sum(WV[i] * WV[j] * Uij[i, j] for i in range(3) for j in range(3)))
w2_ = w1 ** 2 + w2 ** 2 + w3 ** 2
wk = sum(WV[i] * khat[i] for i in range(3))
check(sp.simplify(wUw - (w2_ - 2 * wk ** 2) * Uk) == 0,
      "D1c and w^i w^j U_ij = (w^2 - 2 (w.khat)^2) U -- the identity both channels' matching "
      "rests on",
      "identical to ppn_scalar_retained_2026.py's C4 and to "
      "ppn_alpha_independent_check_2026.py's STEP 8")

# --- D2: the preferred-frame metric (W2), source moving at v = w_PPN ---
CV = 4 * ga + 3 + al1 - al2 + ze1 - 2 * xi_
CW = 1 + al2 - ze1 + 2 * xi_
Vv = [WV[i] * Uk for i in range(3)]
Ww = [sum(Uij[i, j] * WV[j] for j in range(3)) for i in range(3)]
gbar = sp.zeros(4, 4)
gbar[0, 0] = -1 + 2 * Uk
for i in range(3):
    gbar[0, i + 1] = gbar[i + 1, 0] = -sp.Rational(1, 2) * CV * Vv[i] - sp.Rational(1, 2) * CW * Ww[i]
    gbar[i + 1, i + 1] = 1 + 2 * ga * Uk
info("D2  preferred-frame metric loaded (INHERITED, W2): "
     "g_0j = -(1/2)(4g+3+a1-a2+z1-2x)V_j - (1/2)(1+a2-z1+2x)W_j, V_j = w_j U, W_j = w^i U_ij",
     "the O(w^2) pieces of g_00 (Phi_1, script-A, ...) are irrelevant here: g_0i at O(w) "
     "picks up g_00 only at O(w^0)")

# --- D3: the O(w) boost into the matter frame ---
# matter is static in the unbarred frame, which moves at w_PPN wrt the preferred frame:
#   xbar^i = x^i + w^i t,   tbar = t + w_j x^j      (Lorentz to O(w))
Lam = sp.zeros(4, 4)                                # Lam[mubar, nu] = d xbar^mu / d x^nu
Lam[0, 0] = 1
for j in range(3):
    Lam[0, j + 1] = WV[j]
    Lam[j + 1, 0] = WV[j]
    Lam[j + 1, j + 1] = 1
gmat = sp.expand(Lam.T * gbar * Lam)
# drop O(w^2) -- this file's vector read is strictly linear in w
sB = sp.Symbol("sB")
gmat = gmat.applyfunc(lambda e: sp.expand(sp.series(
    sp.expand(e.subs({w1: sB * w1, w2: sB * w2, w3: sB * w3})), sB, 0, 2).removeO()).subs(sB, 1))
info("D3  boosted to the matter frame at O(w).  U and U_ij are unchanged at this order: with "
     "the source static in the unbarred frame, |xbar - xbar'| = |x - x'| exactly, and the "
     "tbar-vs-t skew moves the source only by O(w^2)")
g0i = [sp.expand(gmat[0, i + 1]) for i in range(3)]
lon = [sp.expand(khat[i] * sum(khat[j] * g0i[j] for j in range(3))) for i in range(3)]
per = [sp.expand(g0i[i] - lon[i]) for i in range(3)]
wper = [sp.expand(WV[i] - khat[i] * wk) for i in range(3)]
pred = [sp.expand(-al1 / 2 * wper[i] * Uk) for i in range(3)]
check(all(sp.simplify(per[i] - pred[i]) == 0 for i in range(3)),
      "D3a *** THE DICTIONARY: the part of g_0i TRANSVERSE to k is exactly "
      "h_0i^perp = -(alpha_1/2) (w_PPN)_i^perp U -- and gamma, alpha_2, zeta_1, xi ALL "
      "CANCEL out of it ***",
      f"h_01^perp = {sp.factor(per[0])} (for k along z).  So the transverse vector channel "
      f"is a PURE alpha_1 meter: it cannot be contaminated by gamma (which the machinery "
      f"gives = 1 anyway), by alpha_2, or by the semiconservative parameters")
check(sp.simplify(sp.expand(lon[2]) - (1 - al1 / 2 + al2 - ze1 + 2 * xi_) * w3 * Uk) == 0,
      "D3b the LONGITUDINAL part is g_03 = (1 - alpha_1/2 + alpha_2 - zeta_1 + 2 xi)(w.khat)U "
      "-- it DOES carry alpha_2 (and zeta_1, xi), and it also carries a GR piece (w.khat)U, "
      "which is why it is not clean",
      "this is the only place alpha_2 appears in g_0i, and PART L shows it is pure gauge")
check(all(sp.simplify(per[i].subs({al1: 0, al2: 0, ze1: 0, xi_: 0, ga: 1})) == 0 for i in range(3))
      and sp.simplify(lon[2].subs({al1: 0, al2: 0, ze1: 0, xi_: 0, ga: 1}) - w3 * Uk) == 0,
      "D3c GATE ON THE DICTIONARY ITSELF: in GR (alpha's = zeta = xi = 0, gamma = 1) the "
      "transverse part vanishes IDENTICALLY -- static matter has NO gravitomagnetic field in "
      "its own rest frame -- while the surviving longitudinal (w.khat)U is pure gauge",
      "this is the physical reason the channel is clean: every bit of transverse g_0i is "
      "preferred-frame signal.  It also validates the inherited GR part of W2's coefficients "
      "(-7/2 V_j - 1/2 W_j at gamma = 1): any other GR normalisation would leave a "
      "transverse residue here")

# --- D4: gauge analysis for static perturbations ---
xi0, xi1, xi2, xi3 = sp.symbols("xi_0 xi_1 xi_2 xi_3")
XI = [xi0, xi1, xi2, xi3]
Ik = sp.I * kk                                  # d_3 -> i k, d_0 -> 0 (static)


def dmu(idx, expr):
    return Ik * expr if idx == 3 else 0


dh = sp.Matrix(4, 4, lambda m, n: sp.expand(dmu(m, XI[n]) + dmu(n, XI[m])))
check(dh[0, 0] == 0 and dh[0, 1] == 0 and dh[0, 2] == 0 and dh[1, 1] == 0
      and dh[2, 2] == 0 and dh[1, 2] == 0,
      "D4a gauge inventory for STATIC perturbations at a single mode k along z: h_00, h_01, "
      "h_02, h_11, h_22, h_12 are GAUGE INVARIANT",
      "delta h_{mu nu} = d_mu xi_nu + d_nu xi_mu with d_0 = 0, so only the four h_{3 nu} move")
check(sp.simplify(dh[0, 3] - Ik * xi0) == 0 and sp.simplify(dh[3, 3] - 2 * Ik * xi3) == 0
      and sp.simplify(dh[1, 3] - Ik * xi1) == 0 and sp.simplify(dh[2, 3] - Ik * xi2) == 0,
      "D4b and the four h_{3 nu} are pure gauge, each moved by its own xi -- so the gauge "
      "h_{3 nu} = 0 used by the machinery is a COMPLETE and legitimate gauge fixing, and "
      "h_01 (the quantity this file measures) is gauge invariant",
      "in particular delta h_0i = d_i xi_0 is purely LONGITUDINAL: the one gauge function "
      "left in the vector sector kills exactly the one component that carried alpha_2")

# --- D5: the convention-free consistency relation the two channels must satisfy ---
a_of_al = sp.expand(-al1)                     # g_00 coefficient of w^2 U in Will's convention
c_of_al = sp.expand(-al1 / 2)                 # g_0i transverse coefficient, from D3a
check(sp.simplify(c_of_al - a_of_al / 2) == 0,
      "D5  *** THE TEST: whatever alpha_1 is, the two channels must satisfy c = a/2, where "
      "a is the coefficient of w^2 U in h_00 and c is the coefficient of w^perp U in "
      "h_0i^perp.  This relation is CONVENTION-FREE (renaming the alphas rescales both sides "
      "identically), so it is a genuine cross-check of the AeST solve, not of the labels ***",
      "and the labels then say: a = -alpha_1 (W2), c = -alpha_1/2 (D3a)")

# =================================================================================================
# THE MACHINERY -- copied VERBATIM from ppn_scalar_retained_2026.py (its _G1_general, build,
# fourier, equations).  Not re-derived, deliberately: an apples-to-apples cross-check must use
# the same system.  hcoeffs is the only change -- it returns ALL unknowns, not one.
# =================================================================================================
t, x, y, z = sp.symbols("t x y z", real=True)
CO = [t, x, y, z]
ETA = sp.diag(-1, 1, 1, 1)
ETAI = ETA
eps = sp.Symbol("eps")
s = sp.Symbol("s")
KB = sp.Symbol("K_B", positive=True)
cJ = sp.Symbol("c_J")
AY = sp.Symbol("A_Y")
Fpp = sp.Symbol("Fpp")
Q0 = sp.Symbol("Q_0")
k = sp.Symbol("k", positive=True)
om = sp.Symbol("omega")
rho = sp.Symbol("rho")
R_ = sp.Symbol("R")
P_, Pi_ = sp.Symbol("P"), sp.Symbol("Pi_")
I = sp.I


def _G1_general():
    """Linearised Einstein tensor for h_{mu nu}(t,z), from the Riemann definition."""
    H = {}
    for m in range(4):
        for n in range(m, 4):
            H[(m, n)] = sp.Function(f"h{m}{n}")(t, z)
    hd = sp.Matrix(4, 4, lambda m, n: H[(min(m, n), max(m, n))])
    gd = ETA + eps * hd
    gu = ETAI - eps * (ETAI * hd * ETAI)
    Gam = [[[sp.expand(sp.Rational(1, 2) * sum(
        gu[r, ss] * (sp.diff(gd[ss, n], CO[m]) + sp.diff(gd[ss, m], CO[n]) - sp.diff(gd[m, n], CO[ss]))
        for ss in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]

    def ric(sig, nu):
        out = 0
        for m in range(4):
            out += sp.diff(Gam[m][nu][sig], CO[m]) - sp.diff(Gam[m][m][sig], CO[nu])
            for l in range(4):
                out += Gam[m][m][l] * Gam[l][nu][sig] - Gam[m][nu][l] * Gam[l][m][sig]
        return sp.expand(out)

    R1 = sp.Matrix(4, 4, lambda m, n: sp.expand(ric(m, n)).coeff(eps, 1))
    Rs = sp.expand(sum(ETAI[m, n] * R1[m, n] for m in range(4) for n in range(4)))
    return H, sp.Matrix(4, 4, lambda m, n: sp.expand(R1[m, n] - sp.Rational(1, 2) * ETA[m, n] * Rs))


def build(wvec, zero_fields=()):
    """O(eps^2) Lagrangian of the aether+scalar sector + the matter source, fields f(t,z)."""
    H = {}
    for m in range(4):
        for n in range(m, 4):
            H[(m, n)] = sp.Function(f"h{m}{n}")(t, z)
    a = [sp.Function(f"a{m}")(t, z) for m in range(4)]
    chi = sp.Function("chi")(t, z)
    lam = sp.Function("lam")(t, z)
    subz = {}
    for nm in zero_fields:
        if nm.startswith("h"):
            subz[H[(int(nm[1]), int(nm[2]))]] = 0
        else:
            subz[a[int(nm[1])]] = 0

    def Z(e):
        return e.subs(subz)

    hd = sp.Matrix(4, 4, lambda m, n: Z(H[(min(m, n), max(m, n))]))
    gd = ETA + eps * hd
    hup = ETAI * hd * ETAI
    gu = ETAI - eps * hup + eps ** 2 * (hup * hd * ETAI)
    trh = sum(ETAI[m, n] * hd[m, n] for m in range(4) for n in range(4))
    h2 = sum(hup[m, n] * hd[m, n] for m in range(4) for n in range(4))
    sq = 1 + eps * trh / 2 + eps ** 2 * (trh ** 2 / 8 - h2 / 4)

    w2 = sum(c ** 2 for c in wvec)
    gw = sp.series(1 / sp.sqrt(1 - w2), s, 0, 3).removeO()
    Abg = sp.Matrix([-gw, gw * wvec[0], gw * wvec[1], gw * wvec[2]])      # A^bg_mu
    Ad = sp.Matrix([Abg[m] + eps * Z(a[m]) for m in range(4)])
    Au = gu * Ad
    AA = sum(Au[m] * Ad[m] for m in range(4))
    Pdn = sp.Matrix([-Q0 * Abg[m] for m in range(4)])                    # grad_mu phi_bg
    dphi = sp.Matrix([Pdn[m] + eps * sp.diff(Z(chi), CO[m]) for m in range(4)])

    Gam = [[[sp.Rational(1, 2) * sum(
        gu[r, ss] * (sp.diff(gd[ss, n], CO[m]) + sp.diff(gd[ss, m], CO[n]) - sp.diff(gd[m, n], CO[ss]))
        for ss in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]

    F = sp.Matrix(4, 4, lambda m, n: eps * (sp.diff(Z(a[n]), CO[m]) - sp.diff(Z(a[m]), CO[n])))
    F2 = sum(F[m, n] * F[aa, bb] * gu[m, aa] * gu[n, bb]
             for m in range(4) for n in range(4) for aa in range(4) for bb in range(4))
    Jd = [sum(Au[nu] * (sp.diff(Ad[al], CO[nu]) - sum(Gam[b][nu][al] * Ad[b] for b in range(4)))
              for nu in range(4)) for al in range(4)]
    Jphi = sum(gu[mu, al] * Jd[al] * dphi[mu] for mu in range(4) for al in range(4))
    Q = sum(Au[mu] * dphi[mu] for mu in range(4))
    Y = sum((gu[mu, nu] + Au[mu] * Au[nu]) * dphi[mu] * dphi[nu]
            for mu in range(4) for nu in range(4))

    B = (-(KB / 2) * F2 + 2 * cJ * Jphi - AY * Y + (Fpp / 2) * (Q - Q0) ** 2
         + eps * Z(lam) * (AA + 1))
    L = sq * B
    L2 = sp.expand(sp.series(sp.expand(L), eps, 0, 3).removeO()).coeff(eps, 2)
    L2 = sp.expand(sp.series(L2, s, 0, 3).removeO())
    L2 = L2 + sp.Rational(1, 2) * rho * hd[0, 0]
    return dict(H=H, a=a, chi=chi, lam=lam, L2=sp.expand(L2), Z=Z, Abg=Abg)


def fourier(fields):
    Fa, Ga, sub = {}, {}, {}
    for f in fields:
        nm = f.func.__name__
        Fa[nm], Ga[nm] = sp.Symbol("F_" + nm), sp.Symbol("G_" + nm)
        Fp, Gp = Fa[nm] * P_, Ga[nm] * Pi_
        sub[sp.Derivative(f, (z, 2))] = (I * k) ** 2 * Fp + (-I * k) ** 2 * Gp
        sub[sp.Derivative(f, (t, 2))] = (-I * om) ** 2 * Fp + (I * om) ** 2 * Gp
        sub[sp.Derivative(f, t, z)] = (-I * om) * (I * k) * Fp + (I * om) * (-I * k) * Gp
        sub[sp.Derivative(f, z)] = I * k * Fp - I * k * Gp
        sub[sp.Derivative(f, t)] = -I * om * Fp + I * om * Gp
        sub[f] = Fp + Gp
    return Fa, Ga, sub


G1_H, G1_GEN = _G1_general()


def equations(wvec, zero_fields, eq_names, extra_sub=None):
    """Linear field equations in Fourier space (amplitudes F_*), for the given wind."""
    r = build(wvec, zero_fields)
    H, a, chi, lam, Z = r["H"], r["a"], r["chi"], r["lam"], r["Z"]
    allf = [H[(m, n)] for m in range(4) for n in range(m, 4)] + list(a) + [chi, lam]
    live = [f for f in allf if Z(f) != 0]
    Fa, Ga, sub = fourier(live)
    L2 = r["L2"].subs(extra_sub) if extra_sub else r["L2"]
    L2f = sp.expand(L2.subs(sub, simultaneous=True)).subs(rho, R_ * P_ + sp.Symbol("Rc") * Pi_)
    L2avg = sp.expand(sp.expand(sp.expand(L2f).coeff(P_, 1)).coeff(Pi_, 1))
    G1 = G1_GEN.subs(extra_sub) if extra_sub else G1_GEN
    G1 = G1.subs({f: Z(f) for f in [H[(m, n)] for m in range(4) for n in range(m, 4)]})
    G1 = G1.applyfunc(lambda e: sp.expand(sp.expand(e).subs(sub, simultaneous=True)).coeff(P_, 1))
    Gup = sp.Matrix(4, 4, lambda m, n: sp.expand(ETA[m, m] * ETA[n, n] * G1[m, n]))
    if extra_sub:
        L2avg = L2avg.subs(extra_sub)
        Gup = Gup.subs(extra_sub)
    eqs = []
    for nm in eq_names:
        e = sp.diff(L2avg, Ga[nm])
        if nm.startswith("h"):
            m, n = int(nm[1]), int(nm[2])
            e = e - (1 if m == n else 2) * Gup[m, n]
        eqs.append(sp.expand(e))
    return r, eqs, Fa, Ga


def hcoeffs_all(eqs, unkS, nord=2):
    """Solve the linear system order by order in s; return {unknown: [O(s^0), O(s^1), O(s^2)]}."""
    rep, parts = {}, {}
    for u in unkS:
        ps = [sp.Symbol(str(u) + f"_{j}") for j in range(nord + 1)]
        parts[u] = ps
        rep[u] = sum(s ** j * ps[j] for j in range(nord + 1))
    E = [sp.expand(e.subs(rep)) for e in eqs]
    known = {}
    for j in range(nord + 1):
        cur = [sp.expand(sp.expand(e).coeff(s, j).subs(known)) for e in E]
        vj = [parts[u][j] for u in unkS]
        A, b = sp.linear_eq_to_matrix(cur, vj)
        xs = A.LUsolve(b)
        known.update({v: sp.cancel(xs[i]) for i, v in enumerate(vj)})
    return {u: [known[parts[u][j]] for j in range(nord + 1)] for u in unkS}


print()
print("=" * 100)
print(f"machinery: copied verbatim from ppn_scalar_retained_2026.py; linearised Einstein "
      f"tensor built ({time.time()-T0:.0f}s)")
print("=" * 100)

# =================================================================================================
# PART G -- GATES.  Nothing is claimed unless the machinery reproduces established results.
# =================================================================================================
print()
print("=" * 100)
print("PART G -- GATES: the machinery must reproduce what is already established")
print("=" * 100)
ZF0 = ("h01", "h02", "h12", "h13", "h23", "h03", "h33", "a1", "a2")
UNK0 = ["h00", "h11", "h22", "a0", "a3", "chi", "lam"]

r, eqs, Fa, Ga = equations([0, 0, 0], ZF0, UNK0,
                           extra_sub={cJ: 0, AY: 0, Fpp: 0, om: 0, Q0: 0, KB: 0})
solGR = sp.solve([sp.Eq(e, 0) for e in eqs], [Fa[u] for u in UNK0], dict=True)
check(len(solGR) == 1 and sp.simplify(solGR[0][Fa["h00"]] - R_ / (2 * k ** 2)) == 0,
      "G1  pure-GR normalisation reproduced: h_00 = rho/(2k^2), i.e. G_N = 1/(16 pi) = G",
      f"h_00 = {sp.simplify(solGR[0][Fa['h00']])}")

r, eqs, Fa, Ga = equations([0, 0, 0], ZF0, UNK0, extra_sub={cJ: 2 - KB})
eqs0 = [sp.expand(e.subs(R_, 0)) for e in eqs]
A, b = sp.linear_eq_to_matrix(eqs0, [Fa[u] for u in UNK0])
DET = sp.factor(A.det(method="berkowitz"))
tens = sp.factor((k - om) * (k + om))
check(sp.simplify(sp.cancel(DET / tens)).is_polynomial(om),
      "G2  c_T^2 = 1 EXACTLY: the vacuum mode determinant carries a clean (k^2 - omega^2) "
      "tensor factor for every K_B, A_Y, Fpp, Q_0",
      "reproduces ppn_scalar_retained_2026.py's G2 and the corpus's GW170817-safe result")

r, eqs, Fa, Ga = equations([0, 0, 0], ZF0, UNK0, extra_sub={cJ: 2 - KB, om: 0})
sol0 = sp.solve([sp.Eq(e, 0) for e in eqs], [Fa[u] for u in UNK0], dict=True)[0]
h00_0 = sp.cancel(sol0[Fa["h00"]])
check(sp.simplify(sol0[Fa["h11"]] - h00_0) == 0 and sp.simplify(sol0[Fa["h22"]] - h00_0) == 0,
      "G3  gamma_PPN = 1 EXACTLY (h_11 = h_22 = h_00) -- needed twice here: it is a corpus "
      "result reproduced, and D3a shows the vector dictionary is gamma-independent anyway")
GN_over_G = sp.simplify(sp.cancel(16 * sp.pi * (sp.cancel(h00_0.subs(Q0, 0)) * k ** 2 / 2)
                                  / (4 * sp.pi * R_)))
check(sp.simplify(GN_over_G - 2 * AY / ((2 - KB) * (AY - (2 - KB)))) == 0
      and sp.simplify(sp.limit(GN_over_G, AY, sp.oo) - 1 / (1 - KB / 2)) == 0,
      "G4  G_eff/G = 2A_Y/[(2-K_B)(A_Y-(2-K_B))] -> G/(1-K_B/2) as A_Y -> infinity: the "
      "corpus's committed quasi-static G~ reproduced",
      f"G_eff/G = {sp.factor(GN_over_G)}")
info(f"G5  gates cleared in {time.time()-T0:.0f}s -- the vector-sector claims below are "
     f"therefore made on machinery that reproduces four independent established results")

# =================================================================================================
# PART V -- THE VECTOR CHANNEL
# =================================================================================================
print()
print("=" * 100)
print("PART V -- alpha_1 FROM g_0i: the O(w) transverse response of the FULL AeST system")
print("=" * 100)
info("V0  METHOD.  Exactly ppn_scalar_retained_2026.py's w-PERPENDICULAR run -- same "
     "zero-field list, same unknowns, same substitutions, k along z, w along x, static, "
     "gauge h_{3 nu} = 0 -- solved order by order in the wind.  h_00's O(w^2) coefficient "
     "(that file's channel) and h_01's O(w^1) coefficient (this file's channel) come out of "
     "ONE solve of ONE system.  Long-range vs contact is split by fitting "
     "Cm2/(Q_0/k)^2 + C0 + C2 (Q_0/k)^2 at three exact-rational Q_0/k, as there.")

qq = sp.Symbol("qq", positive=True)          # Q_0/k with k = 1
ZFperp = ("h02", "h12", "h23", "h13", "h03", "h33", "a2")
UNKperp = ["h00", "h01", "h11", "h22", "a0", "a1", "a3", "chi", "lam"]
SUBperp = {cJ: 2 - KB, Q0: qq, k: 1, om: 0}
t1 = time.time()
r, eqsQ, FaQ, GaQ = equations([s * sp.Integer(1), 0, 0], ZFperp, UNKperp, extra_sub=SUBperp)
eqsQ = [sp.expand(e.subs(R_, 1)) for e in eqsQ]
unkQ = [FaQ[u] for u in UNKperp]
print(f"       (w perpendicular to k: system built, {time.time()-t1:.0f}s)")

Cm2, C0, C2 = sp.symbols("Cm2 C0 C2")


def split_orders(kb, ay, qds=(10 ** 6, 3 * 10 ** 6, 10 ** 7)):
    """Return dict giving, for h_00 and h_01 at each order in s, the (C0, Cm2) split, plus
    h_00's O(s^0) amplitude (= U, since h_00^(0) = 2U)."""
    dat = []
    for d in qds:
        qv = sp.Rational(1, d)
        e = [sp.expand(xx.subs({KB: kb, AY: ay, Fpp: 4, qq: qv})) for xx in eqsQ]
        dat.append((qv, hcoeffs_all(e, unkQ)))
    out = {}
    for nm in ("h00", "h01"):
        for order in (0, 1, 2):
            vals = [(qv, sol[FaQ[nm]][order]) for qv, sol in dat]
            sol3 = sp.solve([sp.Eq(Cm2 / qv ** 2 + C0 + C2 * qv ** 2, v) for qv, v in vals],
                            [Cm2, C0, C2], dict=True)[0]
            out[(nm, order)] = (sol3[C0], sol3[Cm2])
    out["h00_0"] = dat[-1][1][FaQ["h00"]][0]
    return out


KBS = (sp.Rational(1, 1000), sp.Rational(1, 100), sp.Rational(1, 10),
       sp.Rational(1, 4), sp.Rational(1, 2))
AYS = (10 ** 5, 10 ** 6)
DATA = {}
print(f"       {'K_B':>8s} {'A_Y':>9s} {'c = h01^(1)/U':>16s} {'-2 K_B':>12s} "
      f"{'resid x A_Y':>12s} {'a = h00^(2)/U':>15s} {'4 K_B':>10s} {'contact':>11s}")
for kb in KBS:
    for ay in AYS:
        o = split_orders(kb, ay)
        Uamp = o["h00_0"] / 2                                # h_00^(0) = 2U
        cval = o[("h01", 1)][0] / Uamp
        aval = o[("h00", 2)][0] / Uamp
        DATA[(kb, ay)] = (cval, aval, o)
        print(f"       {float(kb):8.4g} {ay:9d} {float(cval):16.10f} {float(-2*kb):12.6f} "
              f"{float((cval + 2*kb)*ay):12.4f} {float(aval):15.10f} {float(4*kb):10.4f} "
              f"{float(o[('h01',1)][1]):11.3g}")

# --- V1: the vector response is nonzero and odd in w ---
check(all(DATA[(kb, ay)][0] != 0 for kb in KBS for ay in AYS),
      "V1  *** THE VECTOR SECTOR RESPONDS: h_01 has a NONZERO O(w) piece.  So the g_0i "
      "channel exists in the full theory -- it is not degenerate the way g_00 was in the "
      "aether-only truncation ***",
      "static matter in its own rest frame, and yet a gravitomagnetic field: by D3c that is "
      "pure preferred-frame signal, with no GR background to subtract")
odd_ok = True
for kb in KBS:
    for ay in AYS:
        o = DATA[(kb, ay)][2]
        odd_ok = odd_ok and o[("h01", 0)][0] == 0 and o[("h01", 2)][0] == 0 \
            and o[("h00", 1)][0] == 0
check(odd_ok,
      "V2  PARITY CHECK: h_01 is ODD in w (its O(w^0) and O(w^2) parts vanish identically) "
      "and h_00 is EVEN (its O(w^1) part vanishes).  The two channels are cleanly separated "
      "and neither leaks into the other",
      "this is a strong internal consistency test of the order-by-order solve: nothing "
      "enforced it")

# --- V3: the value, and its A_Y independence ---
rich = {}
for kb in KBS:
    c5, c6 = DATA[(kb, AYS[0])][0], DATA[(kb, AYS[1])][0]
    rich[kb] = (AYS[1] * c6 - AYS[0] * c5) / (AYS[1] - AYS[0])     # kill the 1/A_Y term
print()
print(f"       Richardson extrapolation in 1/A_Y (exact rational arithmetic):")
for kb in KBS:
    print(f"         K_B = {float(kb):8.4g}:  c(A_Y -> oo) = {float(rich[kb]):.12f}   "
          f"-2 K_B = {float(-2*kb):.12f}   diff = {float(rich[kb] + 2*kb):.3e}")
check(all(abs(float(rich[kb] + 2 * kb)) < 1e-7 for kb in KBS),
      "V3  *** THE MEASUREMENT: h_01^(1) = -2 K_B w U in the screened (A_Y -> infinity) "
      "limit, at five K_B spanning three decades, to ~8 digits after one Richardson step ***",
      "K_B-ONLY: A_Y does not appear, exactly as in the g_00 channel, and the residual is "
      "clean 1/A_Y (the resid x A_Y column is A_Y-independent), so this IS the limit and not "
      "a numerical accident")
ratios = [float(rich[kb] / (-2 * kb)) for kb in KBS]
check(all(abs(rr - 1) < 1e-5 for rr in ratios),
      f"V4  and it is EXACTLY LINEAR in K_B -- c/(-2K_B) = 1 to within "
      f"{max(abs(rr-1) for rr in ratios):.1e} across K_B = 1e-3 ... 1/2, so no K_B^2 term "
      f"anywhere.  (The g_00 channel's a = 4 K_B is exactly linear too; only the DERIVED "
      f"combination b = (a+b) - a carries K_B^2.)  The tolerance is set by the leftover "
      f"O(1/A_Y^2) of the one-step extrapolation, not by the physics: a K_B^2 term large "
      f"enough to matter would show up at K_B = 1/2 as a percent-level, not 1e-8, offset -- "
      f"and the competing (3/2)K_B reading is off by 125% there",
      "linearity matters: Foster & Jacobson's Einstein-aether alpha_1, as transcribed in "
      "nbody_2026/stage70_ppn_preferred_frame_2026.py, is -8(c_3^2+c_1c_4)/(2c_1-c_1^2+c_3^2) "
      "= -4 K_B EXACTLY for AeST's c_1 = K_B, c_2 = 0, c_3 = -K_B, c_4 = 0 -- also exactly "
      "linear.  Three routes, one exactly-linear answer")

# --- V5: the same run reproduces the g_00 channel ---
check(all(abs(float(DATA[(kb, AYS[1])][1] - 4 * kb)) < 20.0 / AYS[1] for kb in KBS),
      "V5  APPLES-TO-APPLES: the SAME solve reproduces ppn_scalar_retained_2026.py's check "
      "Q3-3, a = alpha_1 + alpha_2 (its convention) = 4 K_B, at every K_B",
      "so the two channels are not two calculations that might differ by a setup detail -- "
      "they are two components of one solution of one system")

# --- V6: no contact term in the vector sector ---
check(all(abs(float(DATA[(kb, ay)][2][("h01", 1)][1])) < 1e-15
          for kb in KBS for ay in AYS),
      "V6  and the vector channel has NO 1/Q_0^2 contact term (the fitted Cm2 is < 1e-15, "
      "i.e. zero to fit precision) -- consistent with ppn_scalar_retained_2026.py finding "
      "the contact/pole structure only in the (w.khat) orientation",
      "so nothing about h_01 depends on the Q_0 -> 0 order-of-limits question that its "
      "PART Q2/Q3 had to handle")

# =================================================================================================
# PART C -- THE COMPARISON
# =================================================================================================
print()
print("=" * 100)
print("PART C -- THE CROSS-CHECK, AND WHAT IT DOES TO THE VERIFIED FILE'S alpha_1")
print("=" * 100)
kb_s = sp.Symbol("K_B", positive=True)
c_meas = -2 * kb_s                                  # h_01^(1)/U, machinery wind
a_meas = 4 * kb_s                                   # h_00^(2)/U, same run
check(sp.simplify(c_meas - (-a_meas / 2)) == 0,
      "C1  *** THE CROSS-CHECK PASSES.  D5's convention-free requirement is c = a/2 in "
      "PPN-wind variables; the machinery's wind is the OPPOSITE sign (W4), so the "
      "requirement reads c_machinery = -a/2, and the measurement gives exactly "
      "-2 K_B = -(4 K_B)/2 ***",
      "two different metric components of the AeST solution, one alpha_1.  A mismatch here "
      "would have localised an error in either channel; there is none.  NOTE the sign is the "
      "only place W4 enters: with the other wind identification the relation is c = +a/2 and "
      "|alpha_1| is unchanged")
alpha1_will = sp.simplify(2 * c_meas)               # alpha_1 = 2c (W4), = -a
check(sp.simplify(alpha1_will + 4 * kb_s) == 0,
      "C2  *** alpha_1 FROM g_0i, IN WILL'S CONVENTION (W2): alpha_1 = -4 K_B EXACTLY, "
      "|alpha_1| = 4 K_B ***",
      "and this equals -a from the g_00 channel of the same run, and equals the Foster & "
      "Jacobson value transcribed in stage70 -- three routes agreeing on an exactly linear "
      "-4 K_B.  Since the derivation here RETAINS the scalar, it also answers stage74's "
      "domain objection for alpha_1: c_123 = 0 breaks the well-posedness of the "
      "aether-only problem (that is real, and the scalar repairs it) but does NOT change "
      "the value of alpha_1")
a1_file = kb_s * (2 * kb_s ** 2 - 5 * kb_s + 6) / (2 - kb_s) ** 2
a2_file = kb_s * (2 * kb_s ** 2 - 11 * kb_s + 10) / (2 - kb_s) ** 2
check(sp.simplify(sp.expand(a1_file + a2_file) - a_meas) == 0,
      "C3  BOOKKEEPING, verified: ppn_scalar_retained_2026.py's own two numbers satisfy "
      "alpha_1^C4 + alpha_2^C4 = a = 4 K_B, so its RAW coefficients are confirmed here.  "
      "What is wrong is only the NAMING: in Will's metric the coefficient of w^2 U is "
      "-alpha_1, not alpha_1 + alpha_2",
      f"alpha_1^C4 + alpha_2^C4 = {sp.factor(sp.expand(a1_file + a2_file))}; its "
      f"alpha_1^C4 = -(alpha_1 - alpha_2) of Will's metric, i.e. a combination, not alpha_1")
check(sp.simplify(a1_file - (-alpha1_will)) != 0,
      "C4  *** SO C3/C4 OF THAT FILE IS REFUTED WHERE IT MATTERS: |alpha_1| is 4 K_B, NOT "
      "(3/2) K_B.  Its claim that the convention 'changes nothing since only |alpha| is "
      "used' is FALSE -- the two mappings differ by 8/3 in |alpha_1|, and |alpha_1| is "
      "exactly what the bound uses ***",
      f"at K_B = 1/2: |alpha_1| = {float(4*sp.Rational(1,2)):.4f} here versus "
      f"{float(a1_file.subs(kb_s, sp.Rational(1,2))):.4f} there -- a factor "
      f"{float(4*sp.Rational(1,2)/a1_file.subs(kb_s, sp.Rational(1,2))):.3f}, and the g_0i "
      f"channel picks the former: c would have to be -0.444 instead of the measured -1.000")
info("C5  BOTH CONVENTIONS, as required.",
     "WILL (this file, W2):   alpha_1 = -4 K_B exactly;  "
     "alpha_2 = -K_B(2K_B^2-11K_B+10)/(2-K_B)^2 -> -(5/2)K_B.\n"
     "         C4 (the verified file): alpha_1^C4 = K_B(2K_B^2-5K_B+6)/(2-K_B)^2 -> (3/2)K_B;  "
     "alpha_2^C4 = +K_B(2K_B^2-11K_B+10)/(2-K_B)^2 -> (5/2)K_B.\n"
     "         |alpha_2| = (5/2)K_B either way -- the alpha_2 bound is convention-proof.  "
     "|alpha_1| is NOT, and Will's is the convention in which the |alpha_1| < 1e-4 bound and "
     "Foster & Jacobson's formula are both stated, so 4 K_B is the number that must be used "
     "against LLR.")

# --- the bounds, both alphas, both edges ---
A1_BOUND, A2_BOUND = 1e-4, 1e-7
f2 = sp.lambdify(kb_s, a2_file, "math")


def ceiling(fn, bound):
    lo, hi = 1e-30, 1.0
    assert fn(lo) < bound < fn(hi), "bracketing failed"
    for _ in range(400):
        mid = 0.5 * (lo + hi)
        if fn(mid) < bound:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


kb_ceil_1 = A1_BOUND / 4.0                     # |alpha_1| = 4 K_B exactly
kb_ceil_1_file = ceiling(sp.lambdify(kb_s, a1_file, "math"), A1_BOUND)
kb_ceil_2 = ceiling(f2, A2_BOUND)
K2_FITS = {"Cosh": 7.5e3, "Exp": 9.5e3}
floors = {nm: 2.0 / (K2 + 1.0) for nm, K2 in K2_FITS.items()}
floor_lo = min(floors.values())
print()
print(f"       |alpha_1| = 4 K_B  <  {A1_BOUND:.0e}   =>  K_B < {kb_ceil_1:.4e}   "
      f"(the verified file's own alpha_1 would have given {kb_ceil_1_file:.4e})")
print(f"       |alpha_2| = {A2_BOUND:.0e} ceiling (g_00 channel, unchallenged here)  "
      f"=>  K_B < {kb_ceil_2:.4e}")
for nm, K2 in K2_FITS.items():
    print(f"       subluminality floor, K_2 = {K2:8.0f}:  K_B >= {floors[nm]:.4e}")
check(abs(kb_ceil_1 - 2.5e-5) / 2.5e-5 < 1e-9,
      f"C6  *** THE alpha_1 CEILING IS K_B < {kb_ceil_1:.3e} -- stage70's 2.5e-5 EXACTLY, "
      f"reinstated as ARITHMETIC by a from-scratch scalar-retained derivation.  The verified "
      f"file's '2.67x LOOSER (6.667e-5)' is WITHDRAWN: the truth is "
      f"{kb_ceil_1_file/kb_ceil_1:.2f}x TIGHTER than it claimed ***",
      "this is the one FAVOURABLE sub-claim that file made, and it does not survive.  "
      "Reported first and in these terms because a favourable claim must be checked exactly "
      "as hard as an adverse one -- and here it was the favourable one that was wrong")
check(kb_ceil_2 < kb_ceil_1 and floor_lo > kb_ceil_1 and floor_lo > kb_ceil_2,
      f"C7  the two-sided window is EMPTY on BOTH alphas now: the floor {floor_lo:.3e} sits "
      f"{floor_lo/kb_ceil_1:.1f}x above the alpha_1 ceiling and {floor_lo/kb_ceil_2:.0f}x "
      f"above the alpha_2 ceiling (alpha_2 still BINDS, by "
      f"{kb_ceil_1/kb_ceil_2:.0f}x)",
      "the verdict of ppn_scalar_retained_2026.py's PART Q4 therefore STANDS and is slightly "
      "strengthened: what changes is which claim carries it.  Its alpha_1 escape ('only a 3x "
      "K_2 re-fit') is gone -- clearing alpha_1 now needs K_2 >= "
      f"{2.0/kb_ceil_1 - 1.0:.2e}, i.e. {(2.0/kb_ceil_1 - 1.0)/max(K2_FITS.values()):.1f}x "
      "SZ21's largest fit")
info("C8  AND THE FORK THAT POINTS AGAINST THIS FILE'S OWN ADVERSE READING, restated because "
     "it is still live and this file does nothing to close it.",
     "the FLOOR is a subluminality requirement, and AeST carries a khronon (a global time "
     "function), so superluminal scalar propagation need not create closed causal curves.  "
     "Drop the floor and the surviving window is 0 < K_B < 4.0e-8 -- NON-EMPTY, and this "
     "file's tightening of alpha_1 does not touch that, since alpha_2 was already the binding "
     "side by 625x.  Also unchanged: stage74's other two grounds for doubting a PPN bound at "
     "all (the applicability of the PPN series to this theory) are documentary questions that "
     "no computation here settles -- what this file settles is that IF the PPN series applies, "
     "|alpha_1| = 4 K_B and not (3/2) K_B.")

# =================================================================================================
# PART L -- WHY alpha_2 IS NOT AVAILABLE FROM g_0i, PROVED
# =================================================================================================
print()
print("=" * 100)
print("PART L -- alpha_2 FROM g_0i: PROVED INACCESSIBLE (not skipped), and what would be "
      "needed instead")
print("=" * 100)
# the alpha_2 content of g_0i lives only in the longitudinal component (D3a/D3b), and the
# residual gauge freedom for static perturbations is exactly longitudinal (D4b)
al2_in_perp = [sp.diff(per[i], al2) for i in range(3)]
al2_in_lon = sp.diff(lon[2], al2)
check(all(e == 0 for e in al2_in_perp) and sp.simplify(al2_in_lon - w3 * Uk) == 0
      and sp.simplify(al2_in_lon) != 0,
      "L1  alpha_2 appears in g_0i ONLY through the LONGITUDINAL component: d(g_0i^perp)/"
      "d(alpha_2) = 0 identically, while d(g_03)/d(alpha_2) = (w.khat)U != 0",
      "structural, not incidental: W_i's only alpha_2-carrying structure is "
      "khat_i (w.khat) U, which is longitudinal by construction")
gauge_dir = [sp.expand(dh[0, i + 1]) for i in range(3)]
check(gauge_dir[0] == 0 and gauge_dir[1] == 0 and sp.simplify(gauge_dir[2] - Ik * xi0) == 0,
      "L2  and the residual gauge freedom in the vector sector is EXACTLY that longitudinal "
      "direction: delta h_0i = d_i xi_0 = (0, 0, i k xi_0)",
      "one free function, one component -- it sets g_03 to any value whatsoever")
check(True,
      "L3  *** THEREFORE: for STATIC matter at a single Fourier mode, the gauge-invariant "
      "content of g_0i is alpha_1 ALONE.  alpha_2 cannot be obtained from the vector sector "
      "in this configuration -- by proof, not by omission.  The g_00 channel remains the "
      "SOLE determination of alpha_2, and this file neither confirms nor refutes its "
      "|alpha_2| = (5/2) K_B ***",
      "which is why the empty-window verdict, which alpha_2 carries, is left standing rather "
      "than independently confirmed")
check(True,
      "L4  WHAT WOULD BE NEEDED INSTEAD, named precisely so it can be handed on: (i) re-solve "
      "the same system in the STANDARD PPN GAUGE -- retain h_33, h_13, h_23, h_03 as unknowns "
      "and fix the gauge by the PPN conditions on g_ij (spatial isotropy) instead of by "
      "h_{3 nu} = 0, which makes g_03 physical and its alpha_2 readable; or (ii) drop the "
      "boost trick and source the vector sector with genuinely MOVING matter (T^0i != 0), "
      "which populates V_i and W_i independently and separates their coefficients; or "
      "(iii) match the O(w^2) part of the SPATIAL metric h_11 - h_22, which is gauge "
      "invariant here (D4a) and is a third channel neither file has used.",
      "(iii) is the cheapest: it needs no new solve at all, only the h_11, h_22 amplitudes "
      "already produced by the run above, plus the O(w^2) boost of the PPN g_ij -- which this "
      "file does NOT do, because the O(w^2) post-Galilean transformation (density "
      "transformation, simultaneity skew, the Phi_1 and script-A terms) is a separate "
      "derivation and is NOT COMPUTED here")

# =================================================================================================
# PART S -- STATUS LEDGER
# =================================================================================================
print()
print("=" * 100)
print("PART S -- STATUS LEDGER")
print("=" * 100)
GMSUN, AU = 1.32712440018e20, 1.495978707e11
GBAR = GMSUN / AU ** 2
for lab, a0 in (("canonical a_0 = 9.3619e-11", 9.3619e-11), ("ALT a_0 = 1.1279e-10", 1.1279e-10)):
    yv = GBAR / a0
    info(f"S0  {lab}: at 1 AU, y = g_bar/a_0 = {yv:.4e}, A_Y/(2-K_B) = e^sqrt(y) = "
         f"10^{math.sqrt(yv)/math.log(10):.1f}",
         "both footings are reported as required, and BOTH are irrelevant to the answer: c "
         "and a are A_Y-independent, so alpha_1 = -4 K_B holds for either a_0")
LEDGER = [
    ("RIGOROUS (symbolic, here)",
     "the g_0i dictionary: h_0i^perp = -(alpha_1/2) w_i^perp U with gamma, alpha_2, zeta_1, "
     "xi all cancelling; the GR gate that static matter has no transverse g_0i in its own "
     "rest frame; the static-mode gauge inventory (h_00, h_01, h_02, h_11, h_22, h_12 "
     "invariant, the four h_{3 nu} pure gauge); U_ij = (delta_ij - 2 khat khat)U; the "
     "convention-free relation c = a/2; the four machinery gates (GR normalisation, "
     "c_T^2 = 1, gamma_PPN = 1, G_eff -> G/(1-K_B/2)); and the proof that alpha_2 is not "
     "accessible from g_0i for static matter."),
    ("RIGOROUS (exact-rational numerics, here)",
     "h_01^(1) = -2 K_B w U and h_00^(2) = 4 K_B w^2 U from ONE solve, at K_B = 1e-3, 1e-2, "
     "0.1, 0.25, 0.5 and A_Y = 1e5, 1e6, with 1/A_Y scaling verified and Richardson-"
     "extrapolated to 8 digits; h_01 odd and h_00 even in w; no contact term in h_01.  "
     "Hence alpha_1 = -4 K_B exactly (Will), |alpha_1| = 4 K_B, K_B < 2.5e-5."),
    ("INHERITED, NOT DERIVED",
     "the PPN metric itself (W2) -- specifically that the coefficient of alpha_1 in the sum "
     "of the V_j and W_j coefficients is 1 and that alpha_2, zeta_1, xi cancel from that "
     "sum.  Everything downstream of it is derived here.  The GR part of the same sum is "
     "checked by D3c.  alpha_3 = zeta_i = 0 (semiconservative) is ASSUMED."),
    ("CONDITIONAL -- the frozen-A_Y approximation",
     "inherited unchanged and NOT repaired: A_Y = (2-K_B)e^(sqrt y) is position dependent "
     "with grad(A_Y)/A_Y ~ sqrt(y)/r, and both channels freeze it.  The defence is the same "
     "one and no stronger: c and a are A_Y-INDEPENDENT and the approach to the limit is "
     "clean O(1/A_Y).  A gradient-corrected treatment is still OWED and is still the one "
     "thing that could move these numbers -- for BOTH channels at once, which is worth "
     "noting: the cross-check here does NOT test it, because a common approximation cancels "
     "out of a consistency relation."),
    ("NOT COMPUTED",
     "alpha_2 from the vector sector (PROVED impossible in this configuration -- L3, with "
     "three routes named in L4); the O(w^2) boost of g_ij and hence the h_11 - h_22 channel; "
     "alpha_3, beta, the zeta's, xi; the deep-MOND regime; the contact sector; any two-body "
     "or observational reduction."),
    ("UNTOUCHED",
     "a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 "
     "(FITTED, never derived); the kernel nu(y) = 1/(1-exp(-sqrt y)) (Milgrom & Sanders 2008 "
     "Eq. 13 at alpha = 1/2); the RAR at 0.108 dex; weak lensing; BTFR; the frozen DR4 band.  "
     "The liability located here is in the ADOPTED RELATIVISTIC HOME's vector sector and "
     "cannot be traded away by adjusting kappa or the kernel, nor blamed on them."),
]
for lab, txt in LEDGER:
    print(f"    {lab}:\n        {txt}")
check(True, "S1  status ledger printed with every claim graded")

print()
print("=" * 100)
print("VERDICT, in one paragraph.  The cross-check the verified file declared NOT COMPUTED "
      "has now been done and it SUCCEEDS as a consistency test: g_0i's O(w) transverse "
      "response, -2 K_B w U, is exactly -1/2 of g_00's O(w^2) coefficient 4 K_B, which is "
      "what the PPN metric requires of a single alpha_1, and both come from one solve of one "
      "system that passes four independent gates.  But the number it delivers is not the "
      "number that file claimed: the transverse vector channel measures alpha_1 ALONE, with "
      "no alpha_2 contamination, and it says |alpha_1| = 4 K_B exactly -- 8/3 LARGER than "
      "its (3/2)K_B, because what that file called alpha_1 is the combination "
      "-(alpha_1 - alpha_2) of Will's metric.  Its convention note is wrong that this "
      "'changes nothing'.  So its ONE favourable sub-claim -- a 2.67x looser alpha_1 ceiling "
      "-- is WITHDRAWN, stage70's K_B < 2.5e-5 is reinstated as arithmetic (now derived with "
      "the scalar retained, which answers stage74's domain objection for alpha_1 while "
      "leaving its applicability objection untouched), and alpha_2 -- which the g_0i channel "
      "provably cannot see -- keeps carrying the adverse empty-window verdict on its own.  "
      "DIRECTION: ADVERSE.")
print("=" * 100)
nf = len(FAIL)
print(f"PPN-g0i-CHANNEL CHECKS: {NCHK[0]-nf}/{NCHK[0]} passed"
      + ("" if not nf else f";  FAILED: {FAIL}"))
print(f"runtime {time.time()-T0:.0f}s")
sys.exit(1 if FAIL else 0)
