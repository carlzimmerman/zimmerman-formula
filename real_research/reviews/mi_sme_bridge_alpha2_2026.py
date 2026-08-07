#!/usr/bin/env python3
r"""mi_sme_bridge_alpha2_2026.py -- LANE G3. THE SME BRIDGE, RE-DERIVED ON THE alpha=2 KERNEL,
component by component, against the CURRENT (v19, Feb 2026) Data Tables.

FRAMEWORK. Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA law with a horizon-tied scale
a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 -> a0 = 9.3614e-11 m/s^2 (canonical), 1.13e-10 (ALT
footing, larger by 1/sqrt(Omega_Lambda) = 1.2082). kappa = 1/2 is FITTED, NOT DERIVED. Nothing here
derives a0, Z or Lambda; a0 enters every number below as an INPUT.

WHY THIS LANE EXISTS. The framework's one concrete link to particle physics is that a preferred
frame IS a Standard-Model-Extension background: the same a0 INDUCES (does not derive) a computable
gravity-sector s^mu_nu. Every published margin was computed on the alpha=1 tail, RETIRED 2026-07-30.
This file re-derives the whole tensor from the kernel in force, from scratch, and confronts all nine
components against the tightest CURRENT bound for each.

------------------------------------------------------------------------------------------------
WHAT IS DERIVED HERE (not copied)
------------------------------------------------------------------------------------------------
S1  The tensor.  s^{mu nu} = A * (u^mu u^nu + eta^{mu nu}/4), A = 1 - mu(|a|) the fractional
    inertia anomaly.  Traceless identically; in the Sun-centred frame the boost of u^mu by
    beta_cmb gives s^TT = A(gamma^2 - 1/4) ~ 3A/4, s^TJ = A gamma^2 beta n^J (DIPOLE, O(beta)),
    s^<JK> = A gamma^2 beta^2 (n^J n^K - delta^{JK}/3) (QUADRUPOLE, O(beta^2)).  Verified by exact
    numeric boost, not by the expansion.
S2  The amplitude, per kernel, EXACTLY and in tail form:
        alpha=1 (retired):  A = 1 - 1/sqrt(1+1/y)          -> a0/(2 g)      [ODD in a0]
        alpha=2 (this lane): A = 1 - sqrt(2/(1+sqrt(1+4/y^2))) -> a0^2/(2 g^2)  [EVEN in a0]
        Route A (in force):  A = exp(-sqrt(y))              -> beyond all orders in a0/g
    y = g_bar/a0.  A_2/A_1 = a0/g exactly in the tail: the collapse factor.
S3  The apex direction n^J, computed by an actual galactic->equatorial rotation of the Planck
    dipole (l,b) = (264.021, 48.253), NOT copied from the corpus's RA/Dec.
S4  The nine-component ledger at Saturn (the lowest-acceleration well-tracked body), both footings,
    all three kernels, each against the tightest CURRENT bound.
S5  A per-SYSTEM ledger: each published bound is confronted at the acceleration that governs ITS
    observable (Saturn 6.5e-5, Moon 2.7e-3, lab 9.8, binary-pulsar orbit ~73, neutron-star interior
    ~1.3e12 m/s^2), because in this framework the coefficient is acceleration-dependent, not
    constant.  This is the honest channel-matched confrontation.
S6  The CPT-even-only theorem under alpha=2: it HOLDS, and it is STRENGTHENED.
S7  Reach.  The falsifiable output.
S8  What this ledger does NOT confront, and the one place the bridge could still fail.

------------------------------------------------------------------------------------------------
BOUNDS USED -- Kostelecky & Russell, "Data Tables for Lorentz and CPT Violation", arXiv:0801.0287
v19 (submitted 5 Feb 2026), Table D50 (gravity sector, d=4), read directly from the PDF.
    [364] Hees et al., Universe 2, 30 (2016) [1610.04682]  -- combined ephemerides+LLR+...
    [363] Bourgoin et al., PRL 119, 201102 (2017) [1706.06294] -- LLR
    [365] Bourgoin et al., PRL 117, 241301 (2016) [1607.00294] -- LLR
    [358] Dong, Wang & Shao, PRD 109, 084024 (2024) [2311.11038] -- pulsars
    [369] Shao, PRL 112, 111103 (2014) -- binary pulsars
    [368] Shao, PRD 90, 122009 (2014) [1412.2320] -- binary pulsars, s^TT
    [360] Xu, Gao & Shao, PRD 103, 084028 (2021) [2012.01320] -- SOLITARY MSP spheroid precession
    [357] Zhang et al., PR Applied 20, 014067 (2023) -- atom interferometry
    [362] Shao et al., PRD 97, 024019 (2018) -- gravimetry
    photon CPT-odd sensitivity |k^(3)_(V)00| ~ 1e-44 GeV (Table S3, v19).
Where a row reads (x +/- sigma) the 1-sigma is used as the bound.  That is the HARSHER choice: a
2-sigma reading would double every margin in the framework's favour.

------------------------------------------------------------------------------------------------
NOT ASSERTED, and deliberately so.  The withdrawn s^TX margins ("~9.6x", "1.50x", "1.24x") are
alpha=1-tail numbers and are NOT re-asserted as live anywhere below; the alpha=1 PREDICTION
8.68e-10 is reproduced once, labelled retired, purely to prove this pipeline reproduces the frozen
normalisation rather than inventing one.  "alpha2_PPN ~ 1e-8 / LIVE" is a reverted double-count and
is not used.  Nothing frozen is read or written by this file.
"""
from __future__ import annotations

import math
import sys

import mpmath as mp
import sympy as sp

mp.mp.dps = 60

# ---------------------------------------------------------------------------------------------
# constants
C = mp.mpf("2.99792458e8")
G = mp.mpf("6.67430e-11")
GM_SUN = mp.mpf("1.32712440018e20")
GM_EARTH = mp.mpf("3.986004418e14")
AU = mp.mpf("1.495978707e11")
MPC = mp.mpf("3.0857e22")
HBAR_GEVS = mp.mpf("6.582119569e-25")          # GeV s
H0_KMSMPC = mp.mpf("67.4")
Z_CONST = mp.sqrt(32 * mp.pi / 3)              # 5.7888100366

A0_CAN = mp.mpf("9.3614e-11")
A0_ALT = mp.mpf("1.13e-10")
FOOTINGS = (("canonical  kappa c sqrt(G rho_L)", A0_CAN), ("ALT        rho_tot / c H0", A0_ALT))

V_CMB = mp.mpf("369.82") * 1000               # m/s, Planck 2018 solar dipole
BETA = V_CMB / C
L_APEX, B_APEX = mp.mpf("264.021"), mp.mpf("48.253")     # galactic, Planck 2018

# accelerations that govern each experiment's observable (m/s^2)
R_SATURN = mp.mpf("9.5826") * AU
G_SATURN = GM_SUN / R_SATURN**2                 # 6.46e-5  -- lowest-a well-tracked body
R_MOON = mp.mpf("3.844e8")
G_MOON = GM_EARTH / R_MOON**2                   # 2.70e-3  -- lunar orbit, the LLR observable
G_LAB = mp.mpf("9.80665")                       # atom interferometry / gravimetry
G_PSR_ORB = mp.mpf("72.8")                      # binary-pulsar relative orbital acceleration
G_NS_INT = mp.mpf("1.29e12")                    # neutron-star interior, GM/R^2 (1.4 Msun, 12 km)
G_GAL = mp.mpf("1.9e-10")                       # Sun's COM acceleration in the Galaxy ~ 2 a0

ok_count = 0
fail_count = 0


def check(cond: bool, msg: str) -> None:
    global ok_count, fail_count
    cond = bool(cond)
    if cond:
        ok_count += 1
    else:
        fail_count += 1
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")


def banner(s: str) -> None:
    print("\n" + "=" * 108)
    print(s)
    print("=" * 108)


# =============================================================================================
# THE THREE KERNELS.  A = 1 - mu = 1 - g_bar/|a|, the fractional inertia anomaly.  Every form
# below is algebraically rearranged to avoid float64-style cancellation, then evaluated at 60 dps.
# =============================================================================================
def A_alpha1(y: mp.mpf) -> mp.mpf:
    """RETIRED kernel: nu = sqrt(1+1/y), i.e. |a|^2 = g^2 + a0 g."""
    t = 1 / y
    r = mp.sqrt(1 + t)
    return t / ((r + 1) * r)                    # = 1 - 1/sqrt(1+t), stable


def A_alpha2(y: mp.mpf) -> mp.mpf:
    """alpha=2 kernel: mu(x) = x/sqrt(1+x^2)  <=>  y = x^2/sqrt(1+x^2)."""
    t = 1 / y
    w = 2 * t**2 / (mp.sqrt(1 + 4 * t**2) + 1)  # = (sqrt(1+4t^2)-1)/2, stable
    r = mp.sqrt(1 + w)
    return w / ((r + 1) * r)                    # = 1 - 1/sqrt(1+w), stable


def A_routeA(y: mp.mpf) -> mp.mpf:
    """Route A (in force per STANDING rev.5): mu = 1 - exp(-sqrt(y))."""
    return mp.e ** (-mp.sqrt(y))


KERNELS = (("alpha=1 (RETIRED 2026-07-30)", A_alpha1),
           ("alpha=2 (this lane's target)", A_alpha2),
           ("Route A (in force 2026-08-02)", A_routeA))


# =============================================================================================
def s1_the_tensor():
    banner("S1. THE INDUCED TENSOR, DERIVED -- structure, tracelessness, and the beta hierarchy")
    print("  The modification is a fractional change A = 1 - mu of the INERTIAL response along the")
    print("  cosmic 4-velocity u^mu.  The unique traceless rank-2 background built from u and eta is")
    print("      s^{mu nu} = A ( u^mu u^nu - (1/4) eta^{mu nu} (u.u) ) = A ( u^mu u^nu + eta^{mu nu}/4 )")
    print("  with signature (-+++), u.u = -1.  Trace and components, symbolically:")

    A, b = sp.symbols("A beta", positive=True)
    nx, ny, nz = sp.symbols("n_X n_Y n_Z", real=True)
    gam = 1 / sp.sqrt(1 - b**2)
    u = [gam, gam * b * nx, gam * b * ny, gam * b * nz]
    eta = sp.diag(-1, 1, 1, 1)
    s = sp.Matrix(4, 4, lambda i, j: A * (u[i] * u[j] + eta[i, j] / 4))
    # trace with eta_{mu nu}, on the unit-sphere constraint n.n = 1
    tr = sp.simplify(sum(eta[i, j] * s[i, j] for i in range(4) for j in range(4)))
    tr = sp.simplify(tr.subs(nx**2, 1 - ny**2 - nz**2))
    check(sp.simplify(tr) == 0,
          f"trace eta_munu s^munu = {tr} IDENTICALLY, for any A, any beta, any apex direction -- so "
          f"the induced object is a legal s-bar (the SME gravity coefficient is traceless by "
          f"definition) with no subtraction imposed by hand")

    sTT = sp.simplify(s[0, 0])
    sTX = sp.simplify(s[0, 1])
    lead_TT = sp.limit(sTT, b, 0)
    check(sp.simplify(lead_TT - 3 * A / 4) == 0,
          f"s^TT -> {lead_TT} = 3A/4 at beta=0: the ISOTROPIC piece is O(1) in beta and is the "
          f"LARGEST component by ~3 orders")
    check(sp.simplify(sp.limit(sTX / b, b, 0) - A * nx) == 0,
          "s^TJ = A beta n^J + O(beta^3): the boost DIPOLE is first order in beta -- it exists only "
          "because the Sun moves with respect to the preferred frame")
    quad = sp.simplify(s[1, 1] - s[2, 2])
    check(sp.simplify(sp.limit(quad / b**2, b, 0) - A * (nx**2 - ny**2)) == 0,
          "s^XX - s^YY = A beta^2 (n_X^2 - n_Y^2) + O(beta^4): the spatial QUADRUPOLE is second "
          "order, so the spatial channels are beta = 1.23e-3 weaker again than the dipole")
    # MUTATION: a tensor with an ODD number of u's is NOT traceless-compatible with this structure
    s_odd = sp.Matrix(4, 4, lambda i, j: A * (u[i] * u[j] * u[0] + eta[i, j] / 4))
    tr_odd = sp.simplify(sum(eta[i, j] * s_odd[i, j] for i in range(4) for j in range(4)))
    check(sp.simplify(tr_odd) != 0,
          f"MUTATION: inserting one extra factor of u (an odd-in-u structure) breaks the trace "
          f"identity (trace = {sp.simplify(tr_odd)} != 0), so the tracelessness check above is "
          f"testing the structure and is not satisfied by any tensor at all")
    return s


# =============================================================================================
def s2_the_amplitudes():
    banner("S2. THE AMPLITUDE A = 1 - mu, PER KERNEL: the tails, their parity in a0, and the collapse")
    y = sp.Symbol("y", positive=True)
    a0s, gs = sp.symbols("a_0 g", positive=True)

    x1 = sp.sqrt(y**2 + y)                                       # alpha=1 closure
    x2 = sp.sqrt((y**2 + y * sp.sqrt(y**2 + 4)) / 2)             # alpha=2 closure
    A1 = sp.simplify(1 - y / x1)
    A2 = sp.simplify(1 - y / x2)

    t1 = sp.limit(A1 * y, y, sp.oo)
    t2 = sp.limit(A2 * y**2, y, sp.oo)
    print(f"    alpha=1:  lim y*A   = {t1}    =>  A_1 = a0/(2 g)")
    print(f"    alpha=2:  lim y^2*A = {t2}    =>  A_2 = a0^2/(2 g^2)")
    check(sp.simplify(t1 - sp.Rational(1, 2)) == 0 and sp.simplify(t2 - sp.Rational(1, 2)) == 0,
          "both tails carry the same 1/2, so the ONLY difference is the power: A_2/A_1 = a0/g "
          "exactly -- this single factor is the whole collapse")
    check(sp.limit(A1 * y**2, y, sp.oo) == sp.oo,
          "MUTATION: the alpha=2 diagnostic y^2*A applied to the alpha=1 closure DIVERGES, so the "
          "diagnostic distinguishes the two tails rather than being satisfied by both")

    # parity in a0: substitute y = g/a0 and expand in a0
    ser1 = sp.series(A1.subs(y, gs / a0s), a0s, 0, 4).removeO()
    ser2 = sp.series(A2.subs(y, gs / a0s), a0s, 0, 6).removeO()
    p1 = sorted({sp.degree(term, a0s) for term in sp.Add.make_args(sp.expand(ser1))})
    p2 = sorted({sp.degree(term, a0s) for term in sp.Add.make_args(sp.expand(ser2))})
    print(f"\n    powers of a0 in the alpha=1 expansion: {p1}")
    print(f"    powers of a0 in the alpha=2 expansion: {p2}")
    check(any(int(p) % 2 == 1 for p in p1) and all(int(p) % 2 == 0 for p in p2),
          "the alpha=1 anomaly contains ODD powers of a0 and the alpha=2 anomaly contains ONLY EVEN "
          "powers.  Consequence, and it is a real strengthening: under alpha=2 the induced tensor is "
          "invariant under the sign convention a0 -> -a0, so the predicted SIGN of s^TX no longer "
          "depends on a branch choice.  Under alpha=1 it did")

    # Route A: beyond all orders
    ra = sp.exp(-sp.sqrt(gs / a0s))
    check(sp.limit(ra / a0s**8, a0s, 0, "+") == 0,
          "Route A's anomaly exp(-sqrt(g/a0)) vanishes faster than a0^8 as a0 -> 0, i.e. it is "
          "BEYOND ALL ORDERS in a0/g -- no power-counting margin exists for it at all")

    # ---- float64 hazard, demonstrated rather than asserted
    yy = float(G_SATURN / A0_CAN)
    naive = 1.0 - 1.0 / math.sqrt(1.0 + (math.sqrt(1.0 + 4.0 / yy**2) - 1.0) / 2.0)
    exact = float(A_alpha2(mp.mpf(yy)))
    lost = -math.log10(abs(naive - exact) / exact) if naive != exact else 99.0
    print(f"\n    FLOAT64 HAZARD, shown not asserted.  A_2 at Saturn = {exact:.10e}")
    print(f"      naive float64 '1 - mu' form: {naive:.10e}   -> only ~{lost:.1f} correct digits")
    check(lost < 8.0,
          f"the naive 1-mu float64 evaluation retains only ~{lost:.1f} digits (catastrophic "
          f"cancellation, 1 - (1 - 1e-12)); every number in this file therefore uses the "
          f"algebraically rearranged form at 60 dps.  Route A additionally UNDERFLOWS float64 "
          f"(exp(-830) -> 0.0), which would turn every margin into a fake infinity")

    # exact vs tail, and the observed-vs-Newtonian argument question
    A_ex = A_alpha2(G_SATURN / A0_CAN)
    A_tail = A0_CAN**2 / (2 * G_SATURN**2)
    rel = abs(A_ex - A_tail) / A_ex
    check(rel < mp.mpf("1e-5"),
          f"exact A_2 vs its tail a0^2/(2g^2) differ by {float(rel):.2e} at Saturn, so the recurring "
          f"observed-vs-Newtonian ARGUMENT question (a real bug found four times in this corpus) "
          f"cannot move any number in this lane; the exact form is used regardless")
    A_ex1, A_t1 = A_alpha2(mp.mpf(1)), mp.mpf(1) / 2
    check(abs(A_ex1 - A_t1) / A_ex1 > mp.mpf("0.5"),
          f"MUTATION: at y=1 the same exact-vs-tail comparison differs by "
          f"{float(abs(A_ex1 - A_t1) / A_ex1):.2f}, so the previous check is a statement about "
          f"Saturn's depth and not a tautology about the two expressions")
    return A1, A2


# =============================================================================================
def s3_apex():
    banner("S3. THE APEX DIRECTION n^J -- computed by rotation, not copied")
    ra_ngp, dec_ngp, l_ncp = mp.mpf("192.85948"), mp.mpf("27.12825"), mp.mpf("122.93192")
    d2r = mp.pi / 180
    b, l = B_APEX * d2r, L_APEX * d2r
    dn, rn, ln = dec_ngp * d2r, ra_ngp * d2r, l_ncp * d2r
    sin_dec = mp.sin(dn) * mp.sin(b) + mp.cos(dn) * mp.cos(b) * mp.cos(ln - l)
    dec = mp.asin(sin_dec)
    yq = mp.cos(b) * mp.sin(ln - l)
    xq = mp.cos(dn) * mp.sin(b) - mp.sin(dn) * mp.cos(b) * mp.cos(ln - l)
    ra = (rn + mp.atan2(yq, xq)) % (2 * mp.pi)
    n = (mp.cos(dec) * mp.cos(ra), mp.cos(dec) * mp.sin(ra), sin_dec)
    print(f"  Planck 2018 solar dipole: v = {float(V_CMB/1000):.2f} km/s, (l,b) = "
          f"({float(L_APEX)}, {float(B_APEX)}) deg  ->  beta = {float(BETA):.6e}")
    print(f"  rotated to J2000 equatorial (the SME Sun-centred frame): RA = {float(ra/d2r):.3f} deg, "
          f"Dec = {float(dec/d2r):.3f} deg")
    print(f"  n^X = {float(n[0]):+.6f}   n^Y = {float(n[1]):+.6f}   n^Z = {float(n[2]):+.6f}")
    check(abs(mp.sqrt(sum(c**2 for c in n)) - 1) < mp.mpf("1e-40"),
          "the rotated direction is a unit vector to 40 digits")
    check(abs(float(ra / d2r) - 167.94) < 0.05 and abs(float(dec / d2r) + 6.94) < 0.05,
          f"independent rotation reproduces the corpus's apex RA=167.94, Dec=-6.94 to <0.05 deg -- "
          f"the frame conversion is not being taken on trust")
    check(n[0] < 0 and abs(n[0]) > mp.mpf("0.9"),
          f"n^X = {float(n[0]):+.4f} is NEGATIVE and dominant, which is the entire origin of the "
          f"pre-registered NEGATIVE sign of s^TX and of X being the leading dipole channel.  The "
          f"sign is geometry, not kernel: it survives every kernel switch")
    return n


# =============================================================================================
def components(A: mp.mpf, n) -> dict:
    """Exact components of s^{mu nu} = A(u^mu u^nu + eta^{mu nu}/4) in the Sun-centred frame."""
    g2 = 1 / (1 - BETA**2)
    bx, by, bz = (BETA * c for c in n)
    sJK = lambda i, j: A * (g2 * (BETA * n[i]) * (BETA * n[j]) + (mp.mpf("0.25") if i == j else 0))
    return {
        "s^TT": A * (g2 - mp.mpf("0.25")),
        "s^TX": A * g2 * bx, "s^TY": A * g2 * by, "s^TZ": A * g2 * bz,
        "s^XX-s^YY": sJK(0, 0) - sJK(1, 1),
        "s^XX+s^YY-2s^ZZ": sJK(0, 0) + sJK(1, 1) - 2 * sJK(2, 2),
        "s^XY": sJK(0, 1), "s^XZ": sJK(0, 2), "s^YZ": sJK(1, 2),
    }


# tightest CURRENT bound per component, with the acceleration that governs that observable
# (component, bound, system, ref, governing acceleration)
BOUND_ROWS = [
    ("s^TT", mp.mpf("1.6e-5"), "binary pulsars", "[368]", G_PSR_ORB),
    ("s^TT", mp.mpf("7.7e-5"), "combined eph.+LLR", "[364]", G_SATURN),
    ("s^TX", mp.mpf("1.3e-9"), "combined eph.+LLR", "[364]", G_SATURN),
    ("s^TX", mp.mpf("2.9e-9"), "pulsars", "[358]", G_PSR_ORB),
    ("s^TX", mp.mpf("1.0e-8"), "LLR", "[365]", G_MOON),
    ("s^TX", mp.mpf("7.9e-6"), "atom interferometry", "[357]", G_LAB),
    ("s^TY", mp.mpf("2.3e-9"), "combined eph.+LLR", "[364]", G_SATURN),
    ("s^TY", mp.mpf("3.3e-9"), "pulsars", "[358]", G_PSR_ORB),
    ("s^TZ", mp.mpf("5.5e-9"), "combined eph.+LLR", "[364]", G_SATURN),
    ("s^TZ", mp.mpf("3.2e-9"), "pulsars", "[358]", G_PSR_ORB),
    ("s^XX-s^YY", mp.mpf("2.0e-11"), "combined eph.+LLR", "[364]", G_SATURN),
    ("s^XX-s^YY", mp.mpf("1.1e-11"), "LLR", "[363]", G_MOON),
    ("s^XX-s^YY", mp.mpf("3.9e-11"), "pulsars", "[358]", G_PSR_ORB),
    ("s^XX-s^YY", mp.mpf("2.1e-9"), "atom interferometry", "[357]", G_LAB),
    ("s^XX+s^YY-2s^ZZ", mp.mpf("2.5e-11"), "combined eph.+LLR", "[364]", G_SATURN),
    ("s^XX+s^YY-2s^ZZ", mp.mpf("4.1e-11"), "pulsars", "[358]", G_PSR_ORB),
    ("s^XX+s^YY-2s^ZZ", mp.mpf("1.0e-15"), "solitary MSP precession", "[360]", G_NS_INT),
    ("s^XY", mp.mpf("6.5e-12"), "combined eph.+LLR", "[364]", G_SATURN),
    ("s^XY", mp.mpf("3.6e-12"), "LLR", "[363]", G_MOON),
    ("s^XY", mp.mpf("1.2e-11"), "pulsars", "[358]", G_PSR_ORB),
    ("s^XY", mp.mpf("1.0e-9"), "atom interferometry", "[357]", G_LAB),
    ("s^XZ", mp.mpf("3.9e-12"), "combined eph.+LLR", "[364]", G_SATURN),
    ("s^XZ", mp.mpf("5.9e-12"), "LLR", "[365]", G_MOON),
    ("s^XZ", mp.mpf("5.6e-12"), "pulsars", "[358]", G_PSR_ORB),
    ("s^YZ", mp.mpf("3.4e-12"), "combined eph.+LLR", "[364]", G_SATURN),
    ("s^YZ", mp.mpf("3.0e-12"), "LLR", "[363]", G_MOON),
    ("s^YZ", mp.mpf("1.1e-11"), "pulsars", "[358]", G_PSR_ORB),
]
TIGHTEST_ANY = {  # globally tightest bound on each component, regardless of system
    "s^TT": mp.mpf("1.6e-5"), "s^TX": mp.mpf("1.3e-9"), "s^TY": mp.mpf("2.3e-9"),
    "s^TZ": mp.mpf("3.2e-9"), "s^XX-s^YY": mp.mpf("1.1e-11"),
    "s^XX+s^YY-2s^ZZ": mp.mpf("1.0e-15"), "s^XY": mp.mpf("3.6e-12"),
    "s^XZ": mp.mpf("3.9e-12"), "s^YZ": mp.mpf("3.0e-12"),
}


# =============================================================================================
def s4_ledger(n):
    banner("S4. THE NINE-COMPONENT LEDGER AT SATURN (the lowest-acceleration well-tracked body)")
    print(f"  Saturn: a = 9.5826 AU, g = GM_sun/r^2 = {float(G_SATURN):.5e} m/s^2")
    for fname, a0 in FOOTINGS:
        y = G_SATURN / a0
        print(f"\n  --- {fname}:  a0 = {float(a0):.5e},  y = g/a0 = {float(y):.5e}")
        print(f"      {'A = 1 - mu':<32s}", end="")
        for kname, _ in KERNELS:
            print(f"  {kname.split(' (')[0]:>14s}", end="")
        print()
        As = {kname: kfun(y) for kname, kfun in KERNELS}
        print(f"      {'log10 A':<32s}", end="")
        for kname, _ in KERNELS:
            print(f"  {float(mp.log10(As[kname])):>14.3f}", end="")
        print()
        for comp in TIGHTEST_ANY:
            print(f"      {comp:<20s} bound {float(TIGHTEST_ANY[comp]):>8.1e} ", end="")
            for kname, _ in KERNELS:
                v = abs(components(As[kname], n)[comp])
                print(f"  {float(mp.log10(TIGHTEST_ANY[comp] / v)):>14.1f}", end="")
            print("   <- log10 margin")

    # the load-bearing numbers, alpha=2
    out = {}
    for fname, a0 in FOOTINGS:
        A2 = A_alpha2(G_SATURN / a0)
        comp = components(A2, n)
        out[fname] = (A2, comp)
        print(f"\n  alpha=2, {fname}:  A = {float(A2):.5e}")
        print(f"      {'component':<20s} {'induced':>14s} {'tightest bound':>16s} {'system':>24s} "
              f"{'margin':>11s}")
        for c, v in comp.items():
            m = TIGHTEST_ANY[c] / abs(v)
            sysname = min((r for r in BOUND_ROWS if r[0] == c), key=lambda r: r[1])[2]
            print(f"      {c:<20s} {float(v):>+14.4e} {float(TIGHTEST_ANY[c]):>16.2e} "
                  f"{sysname:>24s} {float(m):>11.3e}")
        print("      (s^TT is the ISOTROPIC piece; the corpus treats it as absorbable into a "
              "metric/units\n       redefinition, in which case its bound does not bite at all.  It "
              "is quoted anyway,\n       both ways: even taken as observable it passes by 2e7.)")

    # reproduce the frozen alpha=1 PREDICTION as a normalisation validation (retired number)
    A1 = A_alpha1(G_SATURN / mp.mpf("9.36e-11"))
    sTX1 = abs(components(A1, n)["s^TX"])
    check(abs(sTX1 - mp.mpf("8.68e-10")) / mp.mpf("8.68e-10") < mp.mpf("0.005"),
          f"normalisation validation: with the RETIRED alpha=1 tail and the corpus's rounded "
          f"a0=9.36e-11 this pipeline returns |s^TX| = {float(sTX1):.4e} against the frozen "
          f"8.68e-10 (0.1%), so the tensor normalisation, the apex projection and beta are the "
          f"frozen ones.  That alpha=1 number and its margin are RETIRED and are not quoted as live")

    A2c = out[FOOTINGS[0][0]][0]
    A2a = out[FOOTINGS[1][0]][0]
    sTXc = abs(out[FOOTINGS[0][0]][1]["s^TX"])
    sTXa = abs(out[FOOTINGS[1][0]][1]["s^TX"])
    check(abs(mp.log10(sTXc / mp.mpf("1.26e-15"))) < mp.mpf("0.02")
          and abs(mp.log10(sTXa / mp.mpf("1.83e-15"))) < mp.mpf("0.02"),
          f"the alpha=2 amplitudes re-derived here from the kernel, {float(sTXc):.3e} canonical and "
          f"{float(sTXa):.3e} ALT, agree with the corpus's banked collapse values 1.26e-15 / "
          f"1.83e-15 -- independent re-derivation, same answer")

    ratio_2 = A2a / A2c
    ratio_1 = A_alpha1(G_SATURN / A0_ALT) / A_alpha1(G_SATURN / A0_CAN)
    check(abs(ratio_2 - (A0_ALT / A0_CAN) ** 2) < mp.mpf("1e-6")
          and abs(ratio_1 - (A0_ALT / A0_CAN)) < mp.mpf("1e-6"),
          f"footing sensitivity DOUBLES under alpha=2: the ALT/canonical ratio is "
          f"{float(ratio_2):.4f} = (a0_ALT/a0_can)^2 instead of {float(ratio_1):.4f} = the first "
          f"power.  Every s-bar number in this lane is twice as footing-sensitive as the alpha=1 one")

    closest = min(TIGHTEST_ANY, key=lambda c: TIGHTEST_ANY[c] / abs(out[FOOTINGS[0][0]][1][c]))
    m_closest = TIGHTEST_ANY[closest] / abs(out[FOOTINGS[0][0]][1][closest])
    print(f"\n  CLOSEST TO ITS BOUND on the globally-tightest reading: {closest} at "
          f"{float(m_closest):.3e}x under")
    check(closest == "s^XX+s^YY-2s^ZZ" and m_closest < mp.mpf("1e4"),
          f"on a GLOBALLY-tightest reading the closest component is NOT s^TX but "
          f"{closest} at only {float(m_closest):.0f}x under -- because the tightest bound on that "
          f"combination, 1e-15, comes from SOLITARY-MSP spheroid precession [360], a system whose "
          f"observable is governed by the neutron star's own 1e12 m/s^2 interior.  Pairing a "
          f"Saturn-acceleration amplitude with a neutron-star bound is a CHANNEL MISMATCH -- the "
          f"same class of artefact that produced this corpus's withdrawn '~2x' and '~9.6x'.  It is "
          f"reported as the conservative corner and is NOT the live margin.  S5 does it properly")
    return out


# =============================================================================================
def s5_per_system(n):
    banner("S5. THE CHANNEL-MATCHED LEDGER -- every bound confronted at the acceleration that "
           "governs ITS observable")
    print("  In this framework the coefficient is NOT a constant background: A = 1 - mu(|a|) is a")
    print("  function of the body's own acceleration.  A bound extracted from system S therefore")
    print("  constrains the coefficient AT S's acceleration.  This is the honest confrontation.")
    print(f"\n  {'component':<18s} {'bound':>9s} {'system':<24s} {'a [m/s^2]':>10s} "
          f"{'induced (can)':>14s} {'margin (can)':>13s} {'margin (ALT)':>13s}")
    worst = None
    for comp, bound, sysname, ref, acc in BOUND_ROWS:
        row = []
        for _, a0 in FOOTINGS:
            v = abs(components(A_alpha2(acc / a0), n)[comp])
            row.append((bound / v, v))
        m_can, v_can = row[0]
        m_alt, _ = row[1]
        print(f"  {comp:<18s} {float(bound):>9.1e} {sysname+' '+ref:<24s} {float(acc):>10.2e} "
              f"{float(v_can):>14.3e} {float(m_can):>13.3e} {float(m_alt):>13.3e}")
        if worst is None or m_can < worst[0]:
            worst = (m_can, comp, sysname, ref, acc, m_alt)
    m, comp, sysname, ref, acc, m_alt = worst
    print(f"\n  TIGHTEST CHANNEL-MATCHED MARGIN: {comp} vs {sysname} {ref} at a = {float(acc):.2e} "
          f"m/s^2")
    print(f"      margin = {float(m):.3e}x (canonical), {float(m_alt):.3e}x (ALT)")
    check(comp == "s^TX" and sysname == "combined eph.+LLR",
          f"the closest coefficient to its bound, channel-matched, is s^TX against the combined "
          f"ephemeris+LLR fit [364] evaluated at Saturn -- the same channel the frozen "
          f"pre-registration chose, for the same reason (A is largest at the lowest-acceleration "
          f"well-tracked body).  The alpha=2 switch changes the SIZE of the front, not its location")
    check(m > mp.mpf("1e5") and m_alt > mp.mpf("1e5"),
          f"and that tightest margin is {float(m):.2e}x (canonical) / {float(m_alt):.2e}x (ALT) "
          f"under the bound.  NOT ONE of the {len(BOUND_ROWS)} published bound rows is within 5 "
          f"orders of the alpha=2 prediction")
    # is the binding bound the newest one?  (a real question: Dong+2024 is newer but weaker)
    stx = [(b, sysn, ref) for c, b, sysn, ref, _ in BOUND_ROWS if c == "s^TX"]
    check(min(stx)[2] == "[364]",
          f"and the binding bound is still Hees et al. 2016 [364] at 1.3e-9: the NEWEST s^TX "
          f"analysis in v19, Dong-Wang-Shao 2024 [358], is 2.9e-9 and did NOT beat it.  So the "
          f"decade 2017-2026 produced no tightening of the channel that binds this framework -- "
          f"the front is analysis-limited, and that is a statement about the field, not the theory")
    check(m < mp.mpf("1e7"),
          f"the margin is {float(m):.2e}x and NOT larger than 1e7 -- stated so the claim is "
          f"two-sided: this is a 6-order miss, not an infinite one, and S7 shows exactly what would "
          f"close it")

    # Route A, in force: the same channel, with underflow handled in log space
    lg = mp.log10(mp.mpf("1.3e-9")) - mp.log10(abs(components(A_routeA(G_SATURN / A0_CAN), n)["s^TX"]))
    print(f"\n  THE KERNEL ACTUALLY IN FORCE (Route A, STANDING rev.5 2026-08-02): the same channel "
          f"gives\n      log10 margin = {float(lg):.1f}, i.e. ~1e{int(lg)}x under.  This is beyond "
          f"'safe'; it is DEAD as a solar-system test.")
    check(lg > 300,
          f"Route A's log10 margin at Saturn is {float(lg):.0f} -- the corpus's 'dead, not safe' "
          f"verdict for Route A reproduces here from the kernel.  NOTE the lane brief called "
          f"alpha=2 'in force'; per STANDING rev.5 it is one kernel behind, so both are computed "
          f"and both are reported")
    return worst


# =============================================================================================
def s6_cpt():
    banner("S6. THE CPT-EVEN-ONLY THEOREM UNDER alpha=2 -- it holds, and it is a KERNEL-CLASS theorem")
    tau = sp.Symbol("tau", real=True)
    w = sp.Function("w")(tau)
    u = sp.Matrix([sp.cosh(w), sp.sinh(w), 0, 0])           # any timelike unit worldline, boosted
    a = u.diff(tau)
    eta = sp.diag(-1, 1, 1, 1)
    au = sp.simplify((u.T * eta * a)[0, 0])
    aa = sp.simplify((a.T * eta * a)[0, 0])
    check(sp.simplify(au) == 0,
          f"a.u = {au} IDENTICALLY on any unit-normalised worldline (it is d(u.u)/dtau = 0).  So at "
          f"first-derivative order there is NO scalar invariant LINEAR in u for a kernel to depend "
          f"on -- the only invariant available is a.a, which is QUARTIC and hence EVEN in u")
    check(sp.simplify(aa - w.diff(tau) ** 2) == 0,
          f"a.a = (dw/dtau)^2 = {sp.simplify(aa)}, manifestly even under u -> -u (w -> -w)")
    print("\n  THEOREM (kernel-class, not per-kernel).  Let the modification be any functional of the")
    print("  invariant a.a/a0^2 with a^mu = u^nu grad_nu u^mu.  Then every induced SME background")
    print("  coefficient carries an EVEN number of u's, so all CPT-ODD coefficients (a_mu, b_mu,")
    print("  k_AF = k^(3)_(V)jm) vanish identically.  alpha=1, alpha=2 and Route A are all of this")
    print("  form, so the theorem is INDIFFERENT to the kernel switch -- it is not a property that")
    print("  had to be re-earned, and that is worth saying because most of this corpus's other")
    print("  alpha=1 results DID have to be re-earned.")
    print("\n  WHERE IT WOULD BREAK, stated concretely so the theorem is falsifiable.  The one odd")
    print("  invariant available at this order is the expansion scalar theta = grad_mu u^mu = 3H.")
    print("  The dS-Unruh construction contains H only through a0 ~ c H_Lambda entering as a0^2 in")
    print("  z = a.a/a0^2, i.e. through H^2.  A kernel with a term LINEAR in H (or in theta) would")
    print("  induce CPT-odd coefficients at the natural scale hbar H, and:")
    kaf_bound = mp.mpf("1e-44")
    hb_H0 = HBAR_GEVS * (H0_KMSMPC * 1000 / MPC)
    hb_a0 = HBAR_GEVS * A0_CAN / C
    hb_a0_alt = HBAR_GEVS * A0_ALT / C
    print(f"      hbar H0      = {float(hb_H0):.3e} GeV   -> {float(hb_H0/kaf_bound):>7.1f}x ABOVE "
          f"the photon CPT-odd sensitivity {float(kaf_bound):.0e} GeV")
    print(f"      hbar a0/c    = {float(hb_a0):.3e} GeV   -> {float(hb_a0/kaf_bound):>7.1f}x ABOVE "
          f"(canonical);  {float(hb_a0_alt/kaf_bound):.1f}x (ALT)")
    check(hb_H0 / kaf_bound > 10 and hb_a0 / kaf_bound > 10,
          f"BOTH natural CPT-odd scales are ALREADY EXCLUDED, by {float(hb_H0/kaf_bound):.0f}x and "
          f"{float(hb_a0/kaf_bound):.0f}x.  So the CPT-even structure is LOAD-BEARING, not "
          f"decorative: a CPT-odd realisation of the same physics would be dead on arrival.  The "
          f"framework passes here by structure, and the test has teeth")
    print("\n  AND A GENUINE STRENGTHENING UNDER alpha=2 (see S2).  A_1 = (1/2) sqrt(a0^2/(a.a)) is")
    print("  even but NON-ANALYTIC -- it needs a positive-branch choice, and it is ODD in a0, so the")
    print("  predicted sign of s^TX inherited a sign convention.  A_2 = a0^2/(2 a.a) is a RATIONAL")
    print("  function of the invariants: even by analyticity, term by term, with no branch and no")
    print("  a0-sign dependence.  Route A's exp(-sqrt(y)) is the least analytic of the three (an")
    print("  essential zero at a0 = 0) though still even.  So of the three kernels, alpha=2 is the")
    print("  one on which the CPT-even theorem is MANIFEST rather than argued.")


# =============================================================================================
def s7_reach(n, worst):
    banner("S7. IS ANY COEFFICIENT WITHIN REACH? -- the falsifiable output of the lane")
    m_can = worst[0]
    need = m_can * 2               # 2x below the bound = a ~2-sigma detection channel
    print(f"  Detecting the alpha=2 s^TX at Saturn needs sigma(s^TX) improved by ~{float(need):.1e}x")
    print(f"  from today's 1.3e-9 to ~{float(mp.mpf('1.3e-9')/need):.2e}.  Historical rate on this")
    print("  coefficient: 1e-6 (atom interferometry, 2023) -> 1e-8 (LLR, 2016) -> 1.3e-9 (combined,")
    print("  2016) -- roughly one order per decade, and NOTHING published 2017-2026 has beaten")
    print("  1.3e-9.  At one order per decade a 1e6 improvement is ~60 years away.  Gaia DR4 solar-")
    print("  system-object astrometry (~2028-2032) is projected to reach ~1e-9: same order as now.")
    check(need > mp.mpf("1e5"),
          f"so the answer to the lane's central question is NO: no coefficient is within reach of a "
          f"near-term experiment, on any footing, and the shortfall is {float(need):.1e}x.  A bridge "
          f"that cannot be tested is not a bridge -- the SME link is a CONSISTENCY statement and "
          f"should be described as one")

    print("\n  BUT THERE IS A REAL, NEW, FALSIFIABLE STATEMENT, and it is the lane's actual output.")
    print("  A_2 = a0^2/(2 g^2) with g = GM/r^2 gives s^TX proportional to r^4 -- where the retired")
    print("  alpha=1 tail gave only r^2.  The alpha=2 switch did not merely shrink the front; it")
    print("  made it FOUR times steeper in log r.  So the front moves OUTWARD rather than dying:")
    print(f"\n  {'kernel':<30s} {'break-even r (can)':>20s} {'break-even r (ALT)':>20s} {'lever':>12s}")
    A_need = mp.mpf("1.3e-9") / (BETA * abs(n[0]))          # A that puts s^TX exactly at the bound
    rows = {}
    for kname, kfun in KERNELS:
        rr = []
        for _, a0 in FOOTINGS:
            # log A(r) is monotone INCREASING in r (larger r -> smaller g -> larger anomaly):
            # bisect in log r, which is immune to the underflow that kills a float64 root-find.
            lo, hi = mp.mpf("1e10"), mp.mpf("1e17")
            f = lambda r: mp.log(kfun(GM_SUN / (r**2 * a0))) - mp.log(A_need)
            assert f(lo) < 0 < f(hi), "bracketing failed"
            for _ in range(200):
                mid = mp.sqrt(lo * hi)
                if f(mid) < 0:
                    lo = mid
                else:
                    hi = mid
            r = mp.sqrt(lo * hi)
            rr.append(r / AU)
        lever = {"alpha=1 (RETIRED 2026-07-30)": "r^2",
                 "alpha=2 (this lane's target)": "r^4",
                 "Route A (in force 2026-08-02)": "exp(-c/r)"}[kname]
        rows[kname] = rr
        print(f"  {kname:<30s} {float(rr[0]):>17.0f} AU {float(rr[1]):>17.0f} AU {lever:>12s}")
    r2 = rows["alpha=2 (this lane's target)"]
    r1 = rows["alpha=1 (RETIRED 2026-07-30)"]
    rA = rows["Route A (in force 2026-08-02)"]
    check(abs(float(r1[0]) - 11.7) < 1.5,
          f"CONTROL: the retired alpha=1 kernel's break-even radius comes out at "
          f"{float(r1[0]):.1f} AU -- just outside Saturn's 9.58 AU, which is exactly why the frozen "
          f"pre-registration found an O(1) margin there.  The r-scan reproduces the frozen "
          f"situation from the kernel alone, so its alpha=2 and Route A rows are trustworthy")
    check(200 < float(r2[0]) < 400 and float(r2[1]) < float(r2[0]),
          f"under alpha=2 the framework's s^TX reaches TODAY'S bound at r = {float(r2[0]):.0f} AU "
          f"(canonical) / {float(r2[1]):.0f} AU (ALT) -- roughly twice Voyager 1's present 165 AU, "
          f"and inside the 300-1000 AU range of every published interstellar-probe concept.  The "
          f"ALT footing is CLOSER because a larger a0 means a larger anomaly")
    check(float(rA[0]) > float(r2[0]),
          f"and even Route A, which is 1e354x under AT SATURN, reaches the same bound at "
          f"{float(rA[0]):.0f} AU (canonical) / {float(rA[1]):.0f} AU (ALT), because its anomaly "
          f"exp(-sqrt(GM/a0)/r) has an enormous r-lever.  *** THIS QUALIFIES the corpus's own "
          f"'s^TX: dead, retire as a test'.  It is dead as an INNER-solar-system test.  As a "
          f"deep-outer-solar-system test it is not dead on ANY of the three kernels, and the three "
          f"kernels predict break-even radii {float(r1[0]):.0f} / {float(r2[0]):.0f} / "
          f"{float(rA[0]):.0f} AU that a single ranged probe would DISCRIMINATE ***")

    print("\n  THE CAVEAT THAT KEEPS THAT HONEST, and it is not small.  'Reaches today's bound at")
    print("  306 AU' is a statement about the size of the PREDICTION at 306 AU.  It is NOT a claim")
    print("  that a ranging campaign to a probe at 306 AU would ACHIEVE sigma(s^TX) = 1.3e-9: the")
    print("  sensitivity of an orbital fit to s^TX is strongly body-dependent (under the retired")
    print("  alpha=1 tail the corpus's own per-body ladder ran Saturn 1x, Mars 59x, Earth 138x,")
    print("  Mercury 918x), and no such per-body sensitivity analysis is done here.  What is")
    print("  established is the r^4 lever and the three break-even radii; converting them into a")
    print("  mission requirement needs a covariance analysis this file does not attempt.")

    # the one kernel-independent distinctive signature
    print("\n  THE OTHER SURVIVING STATEMENT, and it is kernel-INDEPENDENT: at a <~ a0 the anomaly")
    print("  saturates at O(1) and the apex dipole becomes an observable fractional modulation of")
    print("  the acceleration.  Deep-limit slope d ln|a| / d ln a0 (all three kernels):")
    # |a| = g / mu = g / (1 - A(y)), y = g/a0.  d ln|a| / d ln a0 at FIXED g, by exact derivative.
    G_FIX = mp.mpf("1e-16")

    def dln_a_dln_a0(kfun, y_target):
        la0 = mp.log(G_FIX / y_target)
        h = lambda x: mp.log(G_FIX / (1 - kfun(G_FIX / mp.e ** x)))
        return mp.diff(h, la0)

    slopes, slopes_hi = [], []
    for kname, kfun in KERNELS:
        s_deep = dln_a_dln_a0(kfun, mp.mpf("1e-6"))
        slopes.append((kname, s_deep))
        slopes_hi.append(dln_a_dln_a0(kfun, mp.mpf("1e6")))
        print(f"      {kname:<30s} d ln|a|/d ln a0 = {float(s_deep):.6f}   (deep limit, y = 1e-6)")
    check(all(abs(s - mp.mpf("0.5")) < mp.mpf("1e-3") for _, s in slopes),
          "all three kernels give exactly 1/2 in the deep limit (|a| -> sqrt(g a0)), so the "
          "framework's ONE distinctive prediction -- a fixed-apex cos(psi) dipole of amplitude "
          "beta/2 = 6.17e-4 in low-acceleration dynamics -- is KERNEL-INDEPENDENT and was NOT "
          "damaged by either kernel switch")
    check(all(abs(s) < mp.mpf("1e-3") for s in slopes_hi),
          f"MUTATION: the same derivative at y = 1e6 is {float(max(abs(s) for s in slopes_hi)):.2e} "
          f"~ 0, not 1/2 -- so the previous check measures the deep limit specifically and is not "
          f"an identity satisfied everywhere")
    print("  That signature sits at a <~ a0, where NO SME experiment operates, and its sharpest")
    print("  probe (a weak-lensing RAR dipole) is limited by a sky-correlated M/L systematic ~100-")
    print("  400x the target.  Unreachable this decade -- but unreachable for a reason that is a")
    print("  systematic, not a statistic.")
    return rows


# =============================================================================================
def s8_not_confronted(n):
    banner("S8. WHAT THIS LEDGER DOES *NOT* CONFRONT -- and the one direction the bridge can fail")
    print("  1. THE GRAVITATIONAL-WAVE ROWS.  Table D50 also bounds s^(4)_jm, the d=4 gravity-sector")
    print("     coefficients governing GW propagation, at |s^(4)_00| ~ 5e-15 (LIGO/Virgo, [355]).")
    print("     Those rows are NOT confronted above and must not be counted as passes: the induced")
    print("     tensor derived here is a property of a MASSIVE BODY's inertial response at its own")
    print("     acceleration, and a propagating wave has no such acceleration.  The framework has no")
    print("     derived graviton sector -- the covariant MI action programme carries three standing")
    print("     no-goes (2026-08-01).  This is a GAP in the bridge's coverage, not a clean bill.")
    A_deep = A_alpha2(mp.mpf("1"))
    leak = A_deep / mp.mpf("5e-15")
    print(f"\n     AND IT IS THE DIRECTION IN WHICH THE BRIDGE COULD FAIL, with a number attached.")
    print(f"     At a ~ a0 the anomaly saturates: A_2(y=1) = {float(A_deep):.4f}.  Any completion in")
    print(f"     which the SAME u^mu background enters the graviton kinetic operator with that")
    print(f"     ambient-acceleration amplitude predicts |s^(4)| ~ {float(A_deep):.2f}, which is")
    print(f"     {float(leak):.1e}x = {float(mp.log10(leak)):.1f} ORDERS above the GW bound.")
    check(mp.log10(leak) > 13,
          f"so a REQUIREMENT ON ANY FUTURE COVARIANT COMPLETION falls out, and it is falsifiable "
          f"rather than hopeful: the completion must suppress the leak of the O(1) deep-acceleration "
          f"amplitude into the graviton sector by at least {float(mp.log10(leak)):.1f} orders, i.e. "
          f"it must make the graviton sector Lorentz-invariant to <~5e-15 while the matter inertia "
          f"is modified at O(1) at the SAME accelerations.  This is a sharp structural constraint on "
          f"the action programme, derived from a measurement, and it is the kind of statement this "
          f"lane exists to produce")
    print("\n  2. THE COMMON-MODE GALACTIC PIECE -- the load-bearing PREMISE of the whole ledger.")
    A_gal_2 = A_alpha2(G_GAL / A0_CAN)
    A_gal_1 = A_alpha1(G_GAL / A0_CAN)
    print(f"     The Sun's COM acceleration in the Galaxy is ~{float(G_GAL):.1e} ~ 2 a0, where the")
    print(f"     anomaly is O(1): A_2 = {float(A_gal_2):.4f} (alpha=1: {float(A_gal_1):.4f}).  Its")
    print(f"     dipole projection would be A beta |n_X| = "
          f"{float(A_gal_2*BETA*abs(n[0])):.2e}, which is "
          f"{float(A_gal_2*BETA*abs(n[0])/mp.mpf('1.3e-9')):.1e}x OVER the s^TX bound.")
    check(A_gal_2 * BETA * abs(n[0]) / mp.mpf("1.3e-9") > 1e4,
          f"stated against interest: the ledger passes ONLY because that piece is common to every "
          f"solar-system body and therefore absorbable -- a uniform rescaling of inertia is exactly "
          f"degenerate with a rescaling of GM_sun, which is fitted.  If that absorption argument "
          f"fails, the framework is not 1e6x safe on s^TX but ~1e5x EXCLUDED.  This premise is "
          f"kernel-INDEPENDENT (alpha=1 gives {float(A_gal_1):.3f}, alpha=2 {float(A_gal_2):.3f}), "
          f"so the alpha=2 switch neither creates nor repairs it, and it is the single most "
          f"load-bearing unproved step in the bridge")
    print("\n  3. THE MATTER SECTOR.  Universal c_mu_nu is removable by a metric redefinition and the")
    print("     modification is composition-independent (modified INERTIA gives Eotvos eta = 0")
    print("     exactly), so the 1e-27..1e-33 matter bounds do not apply.  That resolution is")
    print("     inherited from the corpus, was not re-derived here, and is why the confrontation is")
    print("     with s-bar and not with c_mu_nu.")


# =============================================================================================
def main() -> int:
    banner("LANE G3 -- THE SME BRIDGE RECOMPUTED ON THE alpha=2 KERNEL (Data Tables v19, Feb 2026)")
    print(f"  a0 = kappa c sqrt(G rho_Lambda) = c H_Lambda / Z,  Z = sqrt(32 pi/3) = "
          f"{float(Z_CONST):.10f}")
    print(f"  canonical a0 = {float(A0_CAN):.5e} m/s^2   ALT footing a0 = {float(A0_ALT):.5e} "
          f"(x{float(A0_ALT/A0_CAN):.4f})")
    print("  kappa = 1/2 is FITTED, NOT DERIVED.  a0 is an INPUT to every number below; nothing")
    print("  here derives a0, Z, Lambda or any Standard-Model quantity.  All arithmetic at 60 dps.")

    s1_the_tensor()
    s2_the_amplitudes()
    n = s3_apex()
    s4_ledger(n)
    worst = s5_per_system(n)
    s6_cpt()
    s7_reach(n, worst)
    s8_not_confronted(n)

    banner("VERDICT")
    print("  1. THE TENSOR, RE-DERIVED.  s^{mu nu} = A(u^mu u^nu + eta^{mu nu}/4), A = 1 - mu, exactly")
    print("     traceless, with s^TT ~ 3A/4 isotropic, s^TJ = A beta n^J a boost DIPOLE, s^<JK> an")
    print("     O(beta^2) quadrupole.  Under alpha=2 the amplitude is A = a0^2/(2 g^2), one power of")
    print("     a0/g smaller than the retired alpha=1 a0/(2g).  Structure unchanged, amplitude not.")
    print()
    print("  2. NINE COMPONENTS vs THE CURRENT (v19) BOUNDS, channel-matched.  Every one of the 27")
    print("     published bound rows passes by at least 5 orders.  CLOSEST: s^TX against the combined")
    print("     ephemeris+LLR fit [364] evaluated at Saturn -- 1.03e6x under (canonical), 7.1e5x")
    print("     (ALT).  Same channel as the frozen pre-registration, six orders weaker.  The")
    print("     conservative cross-channel corner (Saturn amplitude vs the 1e-15 solitary-MSP bound")
    print("     on s^XX+s^YY-2s^ZZ) is ~650x, and is a channel mismatch, not the live margin.")
    print()
    print("  3. THE CPT-EVEN-ONLY THEOREM HOLDS, and it is kernel-CLASS: any kernel that depends on")
    print("     the invariant a.a induces only even-in-u backgrounds, because a.u = 0 identically and")
    print("     the only odd invariant available, theta = 3H, enters solely as H^2 through a0^2.  It")
    print("     is also STRENGTHENED: under alpha=2 the amplitude is RATIONAL in the invariants, so")
    print("     evenness is manifest term-by-term and the predicted sign of s^TX no longer depends on")
    print("     the a0 sign convention, as it did under alpha=1.  The theorem has teeth: both natural")
    print("     CPT-odd scales (hbar H0 = 1.4e-42 GeV, hbar a0/c = 2.1e-43 GeV) are ALREADY EXCLUDED")
    print("     by 144x and 21x against the photon k^(3)_(V)00 sensitivity 1e-44 GeV.")
    print()
    print("  4. IS ANYTHING WITHIN REACH?  NO -- and that is the honest answer the lane asked for.")
    print("     s^TX would need sigma improved by ~2e6, from 1.3e-9 to ~6e-16.  Nothing published")
    print("     2017-2026 has beaten 1.3e-9; Gaia DR4 SSO astrometry projects the same order; at the")
    print("     historical one-order-per-decade this is ~60 years out.  As a NEAR-TERM test the SME")
    print("     bridge is a consistency statement, not a test, and calling it a live falsifier would")
    print("     be false.  ON THE KERNEL ACTUALLY IN FORCE (Route A) the same channel sits at log10")
    print("     margin 354.7 canonical / 322.4 ALT, reproducing the corpus's ~1e354 order.")
    print()
    print("  5. THE ONE THING THAT DID CONVERT, and it is new.  Because A_2 ~ 1/g^2, s^TX scales as")
    print("     r^4 instead of alpha=1's r^2.  The front therefore MOVES OUTWARD rather than dying:")
    print("     it reaches today's bound at 306 AU (canonical) / 278 AU (ALT) under alpha=2, and at")
    print("     580 / 527 AU even under Route A.  The control is that the same scan puts alpha=1's")
    print("     break-even at 11.7 AU, just outside Saturn -- reproducing the frozen situation from")
    print("     the kernel alone.  So: 's^TX is dead, retire the test' is right for the INNER solar")
    print("     system and WRONG as a class statement.  A ranged deep-outer-solar-system probe would")
    print("     DISCRIMINATE the three kernels by their break-even radii (12 / 306 / 580 AU), and")
    print("     that is a pre-registrable prediction with no free parameter beyond the a0 footing.")
    print("     CAVEAT, load-bearing: that is the size of the PREDICTION at those radii, not a claim")
    print("     that a probe there would achieve sigma = 1.3e-9.  Sensitivity is body-dependent and")
    print("     no covariance analysis is attempted here.")
    print()
    print("  6. THE FAILURE DIRECTION, priced.  Two things carry the ledger and neither is proved:")
    print("     (a) the O(1) common-mode galactic anomaly (A = 0.088 at 2 a0 on alpha=2, 0.18 on")
    print("         alpha=1) must be absorbable into GM_sun, or the framework is ~8e4x EXCLUDED")
    print("         rather than 1e6x safe -- kernel-independent, and the most load-bearing unproved")
    print("         step in the whole bridge;")
    print("     (b) the completion must keep that same O(1) deep-acceleration amplitude OUT of the")
    print("         graviton sector by >=14 orders (|s^(4)| <~ 5e-15).  That is a sharp, measurement-")
    print("         derived requirement on the action programme, and it is this lane's provable-or-")
    print("         falsifiable residue.")
    print()
    print("  NOT CLAIMED: that a0, Z or Lambda is derived (kappa = 1/2 stays FITTED); that the SME")
    print("  bounds confirm or refute the framework (neither -- it passes, unobservably); that any")
    print("  Standard-Model quantity is predicted; that the theory is closed.  The withdrawn ~9.6x,")
    print("  1.50x and 1.24x margins are not re-asserted, and alpha2_PPN is ~1e-13, not live.")
    print("=" * 108)

    total = ok_count + fail_count
    print(f"\n{ok_count}/{total} checks held.")
    return 1 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())
