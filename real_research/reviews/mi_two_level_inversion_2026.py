#!/usr/bin/env python3
r"""mi_two_level_inversion_2026.py -- DOOR A2 (the legal population inversion), finally run. It is a NULL.

DOCSTRING CONTRACT.
1. THE QUESTION. The strong no-go (mi_strong_nogo_scoped_2026.py) proved rho(omega) = omega/pi^2
   state-independently for a LINEARLY COUPLED FREE BOSONIC bath, so delta_m > 0 there. Its listed escape A2:
   a BOUNDED spectrum flips the sign candidate, because a two-level detector has <[sigma_-, sigma_+]> =
   -<sigma_z>, negative exactly when the population is INVERTED. And mi_circular_dS_response_2026.py (8/8,
   committed) proved T_eff(E) on the circular dS worldline is GAP-DEPENDENT for v > 0 -- a detector with two
   gaps sees TWO temperatures from ONE worldline, with no second bath postulated. Is inversion reachable, at
   any (v/c)? If yes, what delta_m < 0 does it buy?
2. THE METHOD. Reuse the committed response machinery geom() and F(E) VERBATIM (revalidated here against its
   own two anchors: Gibbons-Hawking at R -> 0, and the exact Planck form at Deser-Levin's T at w = 0). Build
   the secular (Davies) master equation for 2-level, N-level ladder, and every 3-level topology including the
   full triangle with arbitrary coupling weights; solve the steady state by null-space AND by the
   Schnakenberg/matrix-tree closed form (cross-checked); scan gaps, weights, v/c in 0.001..0.99, R in 0.1..0.9.
3. THE ANSWER. INVERSION IS UNREACHABLE AT EVERY (v/c), and the reason is a two-line theorem:
     (i)  For ANY stationary worldline F(-E) - F(E) = E/(2pi) exactly, so the per-transition Boltzmann factor
          x(E) = F(E)/F(-E) = F(E)/(F(E) + E/2pi) < 1 whenever F(E) > 0. Chains (the 2-level detector, the
          3-level LADDER of the task, any N-ladder) have p_{k+1}/p_k = x(E_k) < 1: NO inversion, at ANY v/c,
          INDEPENDENT of the gap-dependence of T_eff. The two-temperature fuel never even enters.
     (ii) For the remaining 3-level topologies (V, Lambda, triangle+cycle) the matrix-tree expansion gives
          p1 - p0 ~ g1g2 d1d2 (x1-1) + g1g3 d1d3 (x1-1) + g2g3 d2d3 (x3-x2)   (d_i = F(-E_i) > 0, g_i >= 0)
          and cyclic partners, so inversion needs x(E) INCREASING somewhere (x3 > min(x1, x2) with
          E3 = E1+E2). Numerically x(E) is STRICTLY DECREASING on every worldline sampled -- v/c up to 0.99,
          R = 0.1..0.9, gaps crossing two orbital harmonics -- so no 3-level topology inverts either.
   What the two temperatures DO buy is a genuine NONEQUILIBRIUM steady state: the triangle carries a nonzero
   cycle affinity A = ln(x1 x2 / x3) and a persistent probability current from ONE worldline -- circulation,
   not inversion. A ~ -1.9 (v/c)^2, i.e. -1.86e-6 at galactic speed. delta_m = (2/pi) sum (p_low - p_high)/E^2
   stays POSITIVE everywhere; at v/c = 1e-3 the entire two-temperature modification of delta_m is a fractional
   4.7e-9 -- even MORE suppressed than the ~1e-6 affinity, because the delta_m combination partially cancels
   the drive -- and it does not touch the sign.
4. CREDIT. nu = sqrt(1+1/y) and the dS-Unruh balance: Milgrom 1999 PLA 253:273 eqs 6-9 (his eqs 10-11 a second
   coefficient; Milgrom 2008 arXiv:0801.3133 sec 7.3.1 on the mismatch). a_lambda = c^2 sqrt(Lambda/3):
   Milgrom 1994 Ann.Phys. 229:384. T = sqrt(a^2 + Lambda/3)/2pi: Narnhofer-Peter-Thirring 1996 IJMPB 10:1507;
   Deser-Levin 1997 CQG 14:L163. Detector: Unruh 1976, DeWitt 1979. Secular master equation: Davies 1974;
   GKSL: Gorini-Kossakowski-Sudarshan / Lindblad 1976. Matrix-tree steady states + cycle affinity:
   Schnakenberg 1976 RMP 48:571. The two-temperature 3-level maser this FAILS to reproduce:
   Scovil & Schulz-DuBois 1959 PRL 2:262. Response machinery: mi_circular_dS_response_2026.py (committed, 8/8).
5. AGAINST INTEREST -- BOTH DIRECTIONS.
   Against the framework: door A2, pitched as "the one legal route to delta_m < 0", DOES NOT DELIVER on the
   circular dS worldline. The anti-MOND wall delta_m > 0 now extends from the free bosonic bath to bounded
   detectors: chains at any v/c by theorem, every 3-level topology by theorem + verified monotonicity. The
   MOND-favourable sign is NOT reachable this way. kappa = 1/2 remains FITTED, NOT DERIVED, and this lane adds
   nothing toward deriving it.
   Against the null being overread: this does NOT close A2 outright. Escapes remain: (a) a worldline or state
   with F(E) locally INCREASING (engineered sidebands, squeezing -- doors A3/A4 live), (b) N >= 4 levels with
   cycles (matrix-tree not extended here), (c) non-secular / strong-coupling dynamics. Also the monotonicity
   of x(E) is verified on grids, not proven.
6. SCOPE. Secular (Davies) limit with strictly nondegenerate gaps (E1 != E2 != E1+E2), weak coupling, unit
   dipole matrix elements times scanned weights g_i; delta_m reported per unit coupling^2 in H = 1 units --
   its SIGN and the fractional two-temperature correction are the payload, not its absolute scale.
   Framework constants for the record: a_0 canonical (rho_DE + cH_Lambda footing) = 9.3614e-11 m/s^2;
   ALT footing (rho_total + cH0) = 1.13e-10 (x1.2082). Nothing in this lane distinguishes the footings.

Exit 0 = every check held. No check(True); every condition below can fail.
"""
from __future__ import annotations

import sys

from mpmath import mp

mp.dps = 25
ok: list[tuple[bool, str]] = []


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


def banner(t):
    print("\n" + "=" * 100 + f"\n {t}\n" + "=" * 100)


# ------------------------------------------------------------------------------------------------
# Response machinery copied VERBATIM from the committed mi_circular_dS_response_2026.py (8/8).
# Revalidated below (C1, C2) against the two anchors that script itself established.
# ------------------------------------------------------------------------------------------------
def geom(R, v, H=1):
    """(R, local velocity v) -> (A, h, w, a, T_DL). H = 1."""
    R, v = mp.mpf(R), mp.mpf(v)
    Ns = mp.sqrt(1 - H**2 * R**2)                 # static-patch lapse
    Om = v * Ns / R if R > 0 else mp.mpf(0)
    N = mp.sqrt(1 - H**2 * R**2 - R**2 * Om**2)   # = Ns/gamma
    A = mp.sqrt(1 / H**2 - R**2)
    h, w = H / N, Om / N
    a5sq = A**2 * h**4 + R**2 * w**4              # five-acceleration^2 = a^2 + H^2
    a = mp.sqrt(a5sq - H**2)
    return A, h, w, a, mp.sqrt(a5sq) / (2 * mp.pi)


def F_raw(E, A, h, w, R):
    """Regularised UDW response rate per unit proper time (verbatim from the committed script)."""
    E = mp.mpf(E)
    D = lambda s: 4 * A**2 * mp.sinh(h * s / 2) ** 2 - 4 * R**2 * mp.sin(w * s / 2) ** 2
    P = A**2 * h**4 + R**2 * w**4
    Q = A**2 * h**6 - R**2 * w**6
    s_c = mp.mpf(10) ** -6
    G = lambda s: (-P / 12 + s**2 * (P**2 / 144 - Q / 360)) if s < s_c else (1 / D(s) - 1 / s**2)
    S = 40 / h
    b = abs(E)
    npts = min(300, max(24, int(4 * b * S / mp.pi) + 24))
    pts = [S * k / npts for k in range(npts + 1)]
    pts[0] = mp.mpf(0)
    Jin = mp.quad(lambda s: mp.cos(E * s) * G(s), pts)
    tail = mp.cos(b * S) / S - b * (mp.pi / 2 - mp.si(b * S)) if b > 0 else 1 / S
    J = Jin - tail
    return (abs(E) / (2 * mp.pi) if E < 0 else mp.mpf(0)) - J / (2 * mp.pi**2)


# Cache: every worldline is keyed by its (R, v) STRINGS; only E > 0 is ever computed. The committed script
# proved F(-E) - F(E) = E/(2pi) holds BY CONSTRUCTION of this regularisation (cos(Es) is even in E), so the
# down-rate is F(-E) = F(E) + E/(2pi) EXACTLY. NOTE: for that very reason "check the identity numerically"
# would be a check that CANNOT FAIL and it is deliberately absent; what CAN fail, and is checked instead, is
# (C2) that F reproduces the exact Planck form at w = 0 and (C3) that every up-rate F(E) is positive.
_cache: dict = {}
_geoms: dict = {}


def wl(Rs, vs):
    if (Rs, vs) not in _geoms:
        _geoms[(Rs, vs)] = geom(Rs, vs)
    return _geoms[(Rs, vs)]


def Fp(Rs, vs, E):
    """Up-rate F(E), E > 0, cached per worldline."""
    key = (Rs, vs, float(E))
    if key not in _cache:
        A, h, w, a, TDL = wl(Rs, vs)
        _cache[key] = F_raw(mp.mpf(E), A, h, w, mp.mpf(Rs))
    return _cache[key]


def Fm(Rs, vs, E):
    """Down-rate F(-E) = F(E) + E/2pi (exact, by construction of the regularisation)."""
    return Fp(Rs, vs, E) + mp.mpf(E) / (2 * mp.pi)


def lnx(Rs, vs, E):
    """ln of the per-transition Boltzmann factor x(E) = F(E)/F(-E) = exp(-E/T_eff(E))."""
    f = Fp(Rs, vs, E)
    return mp.log(f / (f + mp.mpf(E) / (2 * mp.pi)))


def xfac(Rs, vs, E):
    return mp.e ** lnx(Rs, vs, E)


# ------------------------------------------------------------------------------------------------
# Steady states. Secular (Davies) master equation with nondegenerate gaps = Pauli rate equations;
# coherences decay at rates >= 0 (positive half-sums of the F's, C3) and the steady rho is DIAGONAL.
# ------------------------------------------------------------------------------------------------
def steady(n, edges):
    """edges: list of (i, j, k_ij, k_ji) with k_ij the rate i->j. Returns populations from null space."""
    W = mp.zeros(n, n)
    for i, j, kij, kji in edges:
        W[j, i] += kij
        W[i, i] -= kij
        W[i, j] += kji
        W[j, j] -= kji
    M = mp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            M[i, j] = W[i, j]
    for j in range(n):
        M[n - 1, j] = mp.mpf(1)          # replace last row by normalisation
    rhs = mp.zeros(n, 1)
    rhs[n - 1, 0] = mp.mpf(1)
    p = mp.lu_solve(M, rhs)
    return [p[i, 0] for i in range(n)]


all_steady_states = []                    # every solved p-vector, for the C13 positivity sweep


def record(p):
    all_steady_states.append(p)
    return p


# ================================================================================================
banner("S1  REVALIDATE THE COMMITTED MACHINERY (anchors it itself established)")
GRID = [mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf(1), mp.mpf(2)]

# C1: Gibbons-Hawking at R -> 0: T_eff = H/2pi at every gap.
t0 = [mp.mpf(E) / mp.log(Fm("1e-9", "0", E) / Fp("1e-9", "0", E)) for E in GRID]
dev = max(abs(t * 2 * mp.pi - 1) for t in t0)
check(dev < mp.mpf(10) ** -9,
      f"C1 GH anchor: R->0 gives T_eff = H/2pi at all 4 gaps, max dev {float(dev):.2e} < 1e-9 -- the copied "
      f"quadrature+tail machinery reproduces the one exactly known temperature")

# C2: w = 0, R = 0.6: F(E) must equal the exact Planck form E/(2pi(e^{E/T_DL}-1)) at Deser-Levin's T.
# This is STRONGER than a T_eff check: it tests the absolute magnitude of F, not just the up/down ratio.
A6, h6, w6, a6, TDL6 = wl("0.6", "0")
perr = mp.mpf(0)
for E in (mp.mpf("0.5"), mp.mpf(1), mp.mpf(2)):
    planck = E / (2 * mp.pi * (mp.e ** (E / TDL6) - 1))
    perr = max(perr, abs(Fp("0.6", "0", E) / planck - 1))
check(perr < mp.mpf(10) ** -8,
      f"C2 Deser-Levin anchor: at w=0, R=0.6 (a = {float(a6):.4f}) the computed F(E) matches the exact "
      f"Planck form at T_DL = sqrt(a^2+H^2)/2pi to {float(perr):.2e} at E = 0.5, 1, 2 -- magnitude AND "
      f"ratio validated, so the rates fed to every master equation below are the committed, validated ones")

# ================================================================================================
banner("S2  CONTROL -- single bath, two-level detector: detailed balance must forbid inversion")
# Secular 2-level: dp1/dt = F(Om) p0 - F(-Om) p1. Steady <sigma_z> = p1 - p0 = -(1-x)/(1+x) < 0 iff x < 1.
ctrl_pts = [("0.5", "0.001"), ("0.5", "0.5"), ("0.5", "0.9"), ("0.5", "0.99"), ("0.9", "0.8"), ("0.1", "0.9")]
worst_sz, worst_at, cons_err = mp.mpf(-1), None, mp.mpf(0)
for (Rs, vs) in ctrl_pts:
    for Om in (mp.mpf("0.25"), mp.mpf("0.75"), mp.mpf("1.5")):
        p = record(steady(2, [(0, 1, Fp(Rs, vs, Om), Fm(Rs, vs, Om))]))
        sz = p[1] - p[0]
        x = xfac(Rs, vs, Om)
        cons_err = max(cons_err, abs(sz + (1 - x) / (1 + x)))
        if sz > worst_sz:
            worst_sz, worst_at = sz, (Rs, vs, float(Om))
check(cons_err < mp.mpf(10) ** -15,
      f"C4a consistency: the null-space steady state reproduces the closed form <sigma_z> = -(1-x)/(1+x) to "
      f"{float(cons_err):.2e} at all 18 control points -- solver and rates agree")
check(worst_sz < 0,
      f"C4b CONTROL HOLDS: <sigma_z> < 0 at every (Omega, v/c, R) -- 18 points, v/c up to 0.99, R 0.1-0.9. "
      f"Closest approach to inversion <sigma_z> = {float(worst_sz):.3e} at (R, v, Om) = {worst_at}. One "
      f"thermal-ish bath never inverts a two-level detector: the exact identity F(-E)-F(E) = E/2pi makes the "
      f"down-rate exceed the up-rate whenever F(E) > 0, at ANY v/c. No bug; proceed to the real question")

# ================================================================================================
banner("S3  THE FUEL IS REAL -- two gaps DO see two temperatures -- but x(E) stays MONOTONE")
# C5: recompute the gap-dependence at v = 0.5 (committed R4 said it exists; here is its size).
teffs = [mp.mpf(E) / mp.log(Fm("0.5", "0.5", E) / Fp("0.5", "0.5", E)) for E in GRID]
spread = (max(teffs) - min(teffs)) / (sum(teffs) / len(teffs))
check(spread > mp.mpf("0.05"),
      f"C5 two-temperature fuel confirmed: at v/c = 0.5 the effective temperatures at gaps 0.25..2 span "
      f"{float(spread)*100:.1f}% (T_eff = {', '.join(f'{float(t):.4f}' for t in teffs)}). A detector with two "
      f"gaps genuinely sees two temperatures from ONE worldline -- the premise of door A2 stands")

# C6: monotonicity of ln x(E) = -E/T_eff(E). Inversion in ANY shared-level topology needs x increasing.
mono_grids = [
    ("0.5", "0.5",  [mp.mpf(k) / 4 for k in range(1, 17)]),
    ("0.5", "0.9",  [mp.mpf(k) / 4 for k in range(1, 17)]),
    ("0.5", "0.99", [mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf("0.75"), mp.mpf(1)]
                    + [mp.mpf(3) * k / 2 for k in range(1, 21)]),          # to E=30, crosses w=14.0 and 2w
    ("0.9", "0.8",  [mp.mpf("0.25"), mp.mpf("0.5")] + [mp.mpf(k) for k in range(1, 13)]),
    ("0.1", "0.9",  [mp.mpf("0.5"), mp.mpf(1), mp.mpf(2)] + [mp.mpf(4) * k for k in range(1, 16)]),  # to 60, w=20.6
]
n_pairs, worst_delta, worst_pair = 0, mp.mpf(-1e9), None
for (Rs, vs, Es) in mono_grids:
    vals = [(E, lnx(Rs, vs, E)) for E in Es]
    for (E1, l1), (E2, l2) in zip(vals, vals[1:]):
        n_pairs += 1
        d = l2 - l1                       # must be < 0 (strictly decreasing)
        if d > worst_delta:
            worst_delta, worst_pair = d, (Rs, vs, float(E1), float(E2))
check(worst_delta < 0,
      f"C6 x(E) is STRICTLY DECREASING on all 5 worldlines ({n_pairs} consecutive pairs; v/c to 0.99, R "
      f"0.1-0.9, gaps crossing TWO orbital harmonics of w). Least-negative step Delta ln x = "
      f"{float(worst_delta):.3e} at (R, v, E1->E2) = {worst_pair}. This is the single fact that kills every "
      f"shared-level inversion below -- and it is a GRID fact, not a proof; scope stated in the docstring")

# C7: float-hazard rule -- refine the closest-to-flat interval 4x and disclose the shift.
Rs, vs, E1w, E2w = worst_pair
sub = [mp.mpf(E1w) + (mp.mpf(E2w) - mp.mpf(E1w)) * k / 8 for k in range(9)]
subv = [(E, lnx(Rs, vs, E)) for E in sub]
sub_worst = max(l2 - l1 for (_, l1), (_, l2) in zip(subv, subv[1:]))
check(sub_worst < 0,
      f"C7 refinement holds: subdividing the least-negative interval 8x still shows strict decrease "
      f"(worst refined step {float(sub_worst):.3e} vs coarse {float(worst_delta):.3e}); no unsampled "
      f"local increase is hiding at the grid scale")

# ================================================================================================
banner("S4  THE TASK'S 3-LEVEL LADDER -- two gaps, two temperatures, and STILL no inversion, at ANY v/c")
# Chain 0-1-2 with gaps E1, E2. Steady state is detailed-balanced: p1/p0 = x(E1), p2/p1 = x(E2), both < 1
# by the exact identity ALONE. The two-temperature fuel never enters a chain. Verified against the solver:
ladder_cfgs = [("0.25", "0.5"), ("0.5", "0.75"), ("0.5", "1.0"), ("1.0", "0.25")]
speeds = ["0.001", "0.05", "0.2", "0.5", "0.9"]
lad_ok, lad_cons, lad_margin = True, mp.mpf(0), mp.mpf(-1e9)
for vs in speeds:
    for (E1s, E2s) in ladder_cfgs:
        E1, E2 = mp.mpf(E1s), mp.mpf(E2s)
        p = record(steady(3, [(0, 1, Fp("0.5", vs, E1), Fm("0.5", vs, E1)),
                              (1, 2, Fp("0.5", vs, E2), Fm("0.5", vs, E2))]))
        lad_cons = max(lad_cons, abs(p[1] / p[0] - xfac("0.5", vs, E1)),
                       abs(p[2] / p[1] - xfac("0.5", vs, E2)))
        m = max(p[1] - p[0], p[2] - p[1], p[2] - p[0])
        lad_margin = max(lad_margin, m)
        lad_ok = lad_ok and (m < 0)
check(lad_cons < mp.mpf(10) ** -15,
      f"C8a ladder consistency: solver population ratios equal x(E1), x(E2) to {float(lad_cons):.2e} over "
      f"{len(speeds)*len(ladder_cfgs)} configs -- the steady state IS the product of per-edge Boltzmann factors")
check(lad_ok,
      f"C8b LADDER THEOREM CONFIRMED: no pair inverted in any of {len(speeds)*len(ladder_cfgs)} configs "
      f"(4 gap pairs x v/c = 0.001..0.9). Closest approach max(p_high - p_low) = {float(lad_margin):.3e} < 0. "
      f"p_(k+1)/p_k = x(E_k) < 1 needs only F > 0 and the exact identity -- so a chain of ANY length can "
      f"NEVER invert on ANY stationary worldline at ANY v/c. The task's two-gap ladder is closed by theorem")

# ================================================================================================
banner("S5  ALL REMAINING 3-LEVEL TOPOLOGIES -- triangle with arbitrary weights (V and Lambda are limits)")
# Levels 0, E1, E1+E2. Edges a=(0,1,gap E1,weight g1), b=(1,2,gap E2,g2), c=(0,2,gap E3=E1+E2,g3).
# Matrix-tree (Schnakenberg):  with d_i = F(-E_i), x_i = F(E_i)/F(-E_i):
#   p0 ~ g1g2 d1d2      + g1g3 d1d3      + g2g3 x2 d2d3
#   p1 ~ g1g2 x1 d1d2   + g1g3 x1 d1d3   + g2g3 x3 d2d3
#   p2 ~ g1g2 x1x2 d1d2 + g1g3 x3 d1d3   + g2g3 x2x3 d2d3
# so p1-p0 ~ (x1-1)[..] + (x3-x2)[..],  p2-p1 ~ x1(x2-1)[..] + (x3-x1)[..] + x3(x2-1)[..],
#    p2-p0 ~ (x1x2-1)[..] + (x3-1)[..] + x2(x3-1)[..]  -- ALL negative iff x_i < 1 and x3 < min(x1, x2).
weight_sets = [("1", "1", "1"), ("1", "1", "10"), ("10", "0.1", "1"), ("0.1", "10", "1"), ("1", "10", "0.1")]
tri_cons, tri_margin, prem_margin, tri_ok, prem_ok = mp.mpf(0), mp.mpf(-1e9), mp.mpf(-1e9), True, True
n_tri = 0
for vs in speeds:
    for (E1s, E2s) in ladder_cfgs:
        E1, E2 = mp.mpf(E1s), mp.mpf(E2s)
        E3 = E1 + E2
        x1, x2, x3 = xfac("0.5", vs, E1), xfac("0.5", vs, E2), xfac("0.5", vs, E3)
        d1, d2, d3 = Fm("0.5", vs, E1), Fm("0.5", vs, E2), Fm("0.5", vs, E3)
        pm = x3 - min(x1, x2)             # theorem premise: must be < 0
        prem_margin = max(prem_margin, pm)
        prem_ok = prem_ok and (pm < 0)
        for (g1s, g2s, g3s) in weight_sets:
            g1, g2, g3 = mp.mpf(g1s), mp.mpf(g2s), mp.mpf(g3s)
            n_tri += 1
            p = record(steady(3, [(0, 1, g1 * x1 * d1, g1 * d1),
                                  (1, 2, g2 * x2 * d2, g2 * d2),
                                  (0, 2, g3 * x3 * d3, g3 * d3)]))
            # matrix-tree closed form, cross-check:
            q0 = g1 * g2 * d1 * d2 + g1 * g3 * d1 * d3 + g2 * g3 * x2 * d2 * d3
            q1 = g1 * g2 * x1 * d1 * d2 + g1 * g3 * x1 * d1 * d3 + g2 * g3 * x3 * d2 * d3
            q2 = g1 * g2 * x1 * x2 * d1 * d2 + g1 * g3 * x3 * d1 * d3 + g2 * g3 * x2 * x3 * d2 * d3
            Zq = q0 + q1 + q2
            tri_cons = max(tri_cons, abs(p[0] - q0 / Zq), abs(p[1] - q1 / Zq), abs(p[2] - q2 / Zq))
            m = max(p[1] - p[0], p[2] - p[1], p[2] - p[0])
            tri_margin = max(tri_margin, m)
            tri_ok = tri_ok and (m < 0)
check(prem_ok,
      f"C9a theorem premise holds on every config: x(E1+E2) - min(x(E1), x(E2)) <= {float(prem_margin):.3e} "
      f"< 0 across {len(speeds)*len(ladder_cfgs)} (gap, v/c) points -- the harmonic transition is always the "
      f"most suppressed, as strict monotonicity (C6) requires")
check(tri_cons < mp.mpf(10) ** -12,
      f"C9b matrix-tree cross-check: Schnakenberg closed form equals the null-space solve to "
      f"{float(tri_cons):.2e} over all {n_tri} triangle configs -- two independent routes to every steady state")
check(tri_ok,
      f"C9c NO 3-LEVEL TOPOLOGY INVERTS: {n_tri} configs (4 gap pairs x 5 speeds x 5 weight sets incl. "
      f"g -> 0.1 and 10 limits that cover V and Lambda systems), closest approach max(p_high - p_low) = "
      f"{float(tri_margin):.3e} < 0. With x < 1 and x3 < min(x1,x2) every matrix-tree bracket is negative, "
      f"so this is the theorem confirmed, not a scan that got lucky")

# ================================================================================================
banner("S6  WHAT THE TWO TEMPERATURES ACTUALLY BUY -- circulation, not inversion")
# Cycle affinity A = ln(x1 x2 / x3): identically 0 for one KMS temperature; nonzero here = genuine NESS.
E1, E2 = mp.mpf("0.5"), mp.mpf("0.75")
E3 = E1 + E2


def affinity(vs):
    return lnx("0.5", vs, E1) + lnx("0.5", vs, E2) - lnx("0.5", vs, E3)


def cycle_current(vs):
    x1, x2, x3 = xfac("0.5", vs, E1), xfac("0.5", vs, E2), xfac("0.5", vs, E3)
    d1, d2, d3 = Fm("0.5", vs, E1), Fm("0.5", vs, E2), Fm("0.5", vs, E3)
    p = record(steady(3, [(0, 1, x1 * d1, d1), (1, 2, x2 * d2, d2), (0, 2, x3 * d3, d3)]))
    Ja = p[0] * x1 * d1 - p[1] * d1       # net 0->1
    Jb = p[1] * x2 * d2 - p[2] * d2       # net 1->2
    Jc = p[0] * x3 * d3 - p[2] * d3       # net 0->2
    return p, Ja, Jb, Jc


A05 = affinity("0.5")
p5, Ja, Jb, Jc = cycle_current("0.5")
kirchhoff = max(abs(Ja - Jb), abs(Ja + Jc))
check(abs(A05) > mp.mpf("0.01") and abs(Ja) > mp.mpf(10) ** -6,
      f"C10a the NESS is REAL: at v/c = 0.5 the cycle affinity A = ln(x1 x2/x3) = {float(A05):+.4f} and a "
      f"persistent probability current J = {float(Ja):.3e} circulates (one worldline, no second bath, pure "
      f"gap-dependence of T_eff). Two temperatures produce CIRCULATION -- the maser mechanism's fuel -- but "
      f"with x(E) monotone the circulation can never pile population uphill")
check(kirchhoff < mp.mpf(10) ** -20,
      f"C10b Kirchhoff: the three edge currents agree around the cycle to {float(kirchhoff):.2e} "
      f"(J_a = J_b = -J_c), so the solved state is a true steady state, not a solver artefact")

print(f"\n  {'v/c':>8}{'affinity A':>16}{'A/(v/c)^2':>14}")
print("  " + "-" * 40)
ratios = []
for vs in ("0.05", "0.2", "0.5"):
    Av = affinity(vs)
    ratios.append(Av / mp.mpf(vs) ** 2)
    print(f"  {vs:>8}{float(Av):>16.6e}{float(ratios[-1]):>14.4f}")
A_gal = affinity("0.001")
print(f"  {'0.001':>8}{float(A_gal):>16.6e}{float(A_gal/mp.mpf('0.001')**2):>14.4f}")
rspan = max(abs(r) for r in ratios) / min(abs(r) for r in ratios)
check(rspan < 4,
      f"C11a the drive is quadratic in v/c: A/(v/c)^2 spans only a factor {float(rspan):.2f} over "
      f"v/c = 0.05-0.5, matching the committed (v/c)^2 law for the T_eff spread")
check(mp.mpf(10) ** -8 < abs(A_gal) < mp.mpf(10) ** -4,
      f"C11b GALACTIC MAGNITUDE, reported not hidden: at v/c = 1e-3 the entire two-temperature drive is "
      f"A = {float(A_gal):.3e} -- nonzero, (v/c)^2-suppressed, exactly as the committed spread (8.6e-7) "
      f"predicted. Even if inversion were reachable it would have this much fuel; it is not reachable at all")

# ================================================================================================
banner("S7  delta_m -- the sign door A2 was opened FOR. It stays shut")
# Bounded-spectrum spectral weight per line: w_i = (p_low - p_high) |m_i|^2 at omega = E_i; inversion would
# make some w_i < 0 and delta_m = (2/pi) sum_i w_i / E_i^2 could go negative. Unit matrix elements, H = 1.


def delta_m(p):
    return (2 / mp.pi) * ((p[0] - p[1]) / E1**2 + (p[1] - p[2]) / E2**2 + (p[0] - p[2]) / E3**2)


p_gal, _, _, _ = cycle_current("0.001")
dm_rel, dm_gal = delta_m(p5), delta_m(p_gal)
# single-temperature reference: Gibbs at the Deser-Levin temperature of the SAME worldline
TDL_gal = wl("0.5", "0.001")[4]
zg = 1 + mp.e ** (-E1 / TDL_gal) + mp.e ** (-E3 / TDL_gal)
pG = [1 / zg, mp.e ** (-E1 / TDL_gal) / zg, mp.e ** (-E3 / TDL_gal) / zg]
dm_G = delta_m(pG)
frac = abs(dm_gal / dm_G - 1)
check(dm_rel > 0 and dm_gal > 0,
      f"C12a delta_m stays POSITIVE: {float(dm_rel):.6f} at v/c = 0.5 and {float(dm_gal):.6f} at v/c = 1e-3 "
      f"(per unit coupling^2, H = 1). Every spectral line keeps p_low > p_high, so the bounded-spectrum "
      f"commutator <[sigma_-, sigma_+]> = -<sigma_z> never flips sign: door A2 does NOT deliver delta_m < 0")
check(frac < mp.mpf(10) ** -4,
      f"C12b and the two-temperature CORRECTION at galactic speed is fractionally {float(frac):.3e} against "
      f"the single-T_DL Gibbs reference -- reported, not hidden: even SMALLER than the ~1e-6 (v/c)^2 affinity "
      f"because the delta_m combination partially cancels the drive; either way it carries no sign content")
# control on the control: the SAME statistic at v/c = 0.5, against Gibbs at THAT worldline's T_DL, must be
# large -- otherwise C12b's smallness would be a comparison blind by construction, not physics of v -> 0.
TDL_rel = wl("0.5", "0.5")[4]
zr = 1 + mp.e ** (-E1 / TDL_rel) + mp.e ** (-E3 / TDL_rel)
pGr = [1 / zr, mp.e ** (-E1 / TDL_rel) / zr, mp.e ** (-E3 / TDL_rel) / zr]
frac_rel = abs(dm_rel / delta_m(pGr) - 1)
check(frac_rel > mp.mpf(10) ** -3,
      f"C12c control on the control: at v/c = 0.5 the identical statistic is |delta_m/delta_m_Gibbs - 1| = "
      f"{float(frac_rel):.3e} > 1e-3, so the comparison CAN see two-temperature physics when it is there -- "
      f"C12b's part-per-million smallness is the v -> 0 suppression, not blindness")

# ================================================================================================
banner("S8  COMPLETE POSITIVITY -- every steady state is a physical density matrix")
# Secular Davies generator with rates F(+-E) >= 0 is GKSL, hence CP; steady rho = diag(p) + decaying
# coherences. Numerically: all populations >= 0, traces = 1, and every rate used was positive (C3).
min_pop = min(min(p) for p in all_steady_states)
max_tr = max(abs(sum(p) - 1) for p in all_steady_states)
check(min_pop > 0 and max_tr < mp.mpf(10) ** -15,
      f"C13 all {len(all_steady_states)} solved steady states are physical: min population "
      f"{float(min_pop):.3e} > 0, max |tr - 1| = {float(max_tr):.2e}. Diagonal rho with nonneg populations "
      f"= valid density matrix; with C3 the generator is GKSL so the dynamics is completely positive")

neg_rates = [(k, v) for k, v in _cache.items() if not v > 0]
check(len(neg_rates) == 0,
      f"C3 every up-rate computed in this run is strictly positive: {len(_cache)} cached F(E) values across "
      f"all worldlines and gaps, min = {float(min(_cache.values())):.3e}. F > 0 is what turns the exact "
      f"identity into x < 1, i.e. into the no-inversion lemma; it is also the GKSL condition for C13")

# ================================================================================================
print("\n" + "=" * 100)
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("""  Exit 0. DOOR A2 RUN, AND IT IS A NULL: on the circular dS worldline no bounded detector inverts.
  Chains (incl. the task's two-gap ladder) can never invert at ANY v/c -- pure consequence of the exact
  identity F(-E)-F(E) = E/2pi. Every 3-level topology with arbitrary weights is blocked because x(E) is
  strictly decreasing (grid fact, v/c to 0.99). The two-temperature fuel is real but buys a persistent
  CURRENT (A ~ -1.9 (v/c)^2, -1.86e-6 galactic), not inversion. delta_m stays POSITIVE; the anti-MOND wall
  extends to this bounded class. Escapes that remain honest: engineered non-monotone F(E) (A3/A4),
  N >= 4 cycles, strong coupling. kappa = 1/2 remains FITTED, NOT DERIVED.""")
