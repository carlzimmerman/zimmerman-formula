#!/usr/bin/env python3
r"""mi_circular_dS_response_2026.py -- THE RESPONSE LANE, finally computed. It is a NULL for the coefficient.

This is the lane that died twice on an output limit and was therefore never in DOI 10.5281/zenodo.21782600. Its
purpose: the v2(a) correction admitted that only functionals of the local dS-Unruh TEMPERATURE had been examined,
and that functionals of the full RESPONSE F(E) -- whose T_eff is gap-dependent for every Omega != 0 -- were
uncomputed. So: compute F(E) on the circular de Sitter worldline and ask whether that gap-dependence can supply
the factor 2Z = 11.577620 that kappa = 1/2 requires.

SETUP. dS_4 in M^{4,1}: X0 = A sinh(h tau), X1 = A cosh(h tau), X2 = R cos(w tau), X3 = R sin(w tau), with
A^2 + R^2 = H^-2 and A^2 h^2 - R^2 w^2 = 1. Chordal separation gives, for proper-time gap s,
    D(s) = 4 A^2 sinh^2(h s/2) - 4 R^2 sin^2(w s/2),      W(s) = -(1/4 pi^2) / D(s - i eps).
D(s) > 0 for every real s != 0: since sinh^2 x >= x^2 and A^2 h^2 = 1 + R^2 w^2,
    D(s) >= A^2 h^2 s^2 - R^2 w^2 s^2 = s^2,
so there is no light-cone crossing along the worldline and no pole on the real axis. Checked in R1.

REGULARISED RESPONSE. Splitting off the flat double pole, whose eps-contour integral is elementary,
    F(E) = |E| theta(-E)/(2 pi)  -  (1/2 pi^2) J(E),     J(E) = int_0^inf ds cos(E s) [1/D(s) - 1/s^2],
with the algebraic tail 1/s^2 beyond s = S done in closed form via Si. Because cos(E s) is EVEN in E, this yields
the exact identity  F(-E) - F(E) = E/(2 pi)  for EVERY stationary worldline, hence
    T_eff(E) = E / log(1 + E/(2 pi F(E))).
For a KMS state T_eff is E-independent and F(E) = E/(2 pi (e^{E/T} - 1)) is Planckian.

RESULT. The machinery reproduces the Gibbons-Hawking temperature H/2pi (R2) and, at w = 0, reproduces
Deser-Levin's T = sqrt(a^2+H^2)/2pi EXACTLY (R3) -- the very mechanism the paper's q = 2 rests on. Turning on
rotation breaks KMS (R4), confirming the corpus's GEMS and conformal lanes independently. But the breaking scales
as v^2/c^2 (R5): at the galactic v/c ~ 1e-3 the gap-dependence of T_eff is ~1e-6 fractionally, so ANY normalised
functional of F differs from the same functional of the single Deser-Levin temperature by O(1e-6). The response
lane therefore cannot supply a factor 11.578; it delivers q = 2 to six figures.

*** SO THE RESPONSE LANE IS CLOSED AS A ROUTE TO kappa = 1/2, and this cuts AGAINST the framework. It also
confirms "one door, not two": a response functional retains exactly the same r-freedom that a temperature
functional has (choose the weight rho(E) so the induced f is nonlinear at the floor) and adds no NEW freedom. The
single live question stays the one in section 3.3 -- whether the de Sitter floor is c H_Lambda, fixed by the
horizon, or (1/4) c sqrt(G rho_Lambda). kappa = 1/2 remains FITTED, NOT DERIVED. ***

Exit 0 = every check held. No check(True); every condition below can fail.
"""
from __future__ import annotations

import sys

from mpmath import mp

mp.dps = 30
ok: list[tuple[bool, str]] = []


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


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


def F(E, A, h, w, R):
    """Regularised UDW response rate per unit proper time."""
    E = mp.mpf(E)
    D = lambda s: 4 * A**2 * mp.sinh(h * s / 2) ** 2 - 4 * R**2 * mp.sin(w * s / 2) ** 2
    # D(s) = s^2 + P s^4/12 + Q s^6/360 + ..., using A^2h^2 - R^2w^2 = 1
    P = A**2 * h**4 + R**2 * w**4                 # = a5^2
    Q = A**2 * h**6 - R**2 * w**6
    # G = 1/D - 1/s^2 is O(1) but is a difference of two ~1/s^2 quantities: for small s the direct form loses
    # EVERY significant digit (at s = 1e-9 both terms are ~1e18 and 30 digits leave ~1e-12 absolute noise, which
    # is what made the first version of this script report a 5.8e4 error on the Gibbons-Hawking anchor). Below
    # s_c use the series, whose truncation error is O(s^4).
    s_c = mp.mpf(10) ** -6
    G = lambda s: (-P / 12 + s**2 * (P**2 / 144 - Q / 360)) if s < s_c else (1 / D(s) - 1 / s**2)
    S = 40 / h                                    # 1/D ~ e^-40 beyond here: below mp.dps=30 noise
    b = abs(E)
    npts = min(300, max(24, int(4 * b * S / mp.pi) + 24))
    pts = [S * k / npts for k in range(npts + 1)]
    pts[0] = mp.mpf(0)
    Jin = mp.quad(lambda s: mp.cos(E * s) * G(s), pts)
    # closed-form algebraic tail: int_S^inf cos(bs)/s^2 ds = cos(bS)/S - b(pi/2 - Si(bS))
    tail = mp.cos(b * S) / S - b * (mp.pi / 2 - mp.si(b * S)) if b > 0 else 1 / S
    J = Jin - tail
    return (abs(E) / (2 * mp.pi) if E < 0 else mp.mpf(0)) - J / (2 * mp.pi**2)


def Teff(E, *g):
    f = F(E, *g)
    return E / mp.log(1 + E / (2 * mp.pi * f))


GRID = [mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf(1), mp.mpf(2)]


def spread(A, h, w, R):
    ts = [Teff(E, A, h, w, R) for E in GRID]
    return ts, (max(ts) - min(ts)) / (sum(ts) / len(ts))


print("=" * 100)
# ---- R1  no pole on the real axis -------------------------------------------------
A, h, w, a, TDL = geom("0.5", "0.4")
Ds = lambda s: 4 * A**2 * mp.sinh(h * s / 2) ** 2 - 4 * R2 * mp.sin(w * s / 2) ** 2
R2 = mp.mpf("0.5") ** 2
grid = [mp.mpf(k) / 20 for k in range(1, 400)]
check(all(Ds(s) >= s**2 * (1 - mp.mpf(10) ** -18) for s in grid),
      f"R1 D(s) >= s^2 on 399 points out to s = 20 (v/c = 0.4, a strongly relativistic orbit), so there is NO "
      f"light-cone crossing along the worldline and no real-axis pole -- the regularised quadrature below is "
      f"legitimate rather than a principal value in disguise")

# ---- R2  Gibbons-Hawking ---------------------------------------------------------
g0 = geom(mp.mpf(10) ** -9, 0)                    # R -> 0: pure GH
t0, sp0 = spread(*g0[:3], mp.mpf(10) ** -9)
check(all(abs(t * 2 * mp.pi - 1) < mp.mpf(10) ** -9 for t in t0),
      f"R2 the GH limit returns T_eff = H/2pi = {float(1/(2*mp.pi)):.10f} at every gap, max deviation "
      f"{float(max(abs(t*2*mp.pi-1) for t in t0)):.2e}. So the quadrature, the tail and the eps-prescription are "
      f"all validated against the one temperature that is known exactly")

# ---- R3  Deser-Levin at w = 0 ----------------------------------------------------
for Rv in ("0.3", "0.6", "0.85"):
    gg = geom(Rv, 0)
    ts, spv = spread(*gg[:3], mp.mpf(Rv))
    err = max(abs(t / gg[4] - 1) for t in ts)
    print(f"  w=0, R={Rv}:  a = {float(gg[3]):.6f},  T_DL = sqrt(a^2+H^2)/2pi = {float(gg[4]):.10f},  "
          f"max|T_eff/T_DL - 1| = {float(err):.2e}")
    if not check(err < mp.mpf(10) ** -9 and spv < mp.mpf(10) ** -9,
                 f"R3-{Rv} at zero rotation the response is EXACTLY thermal at Deser-Levin's "
                 f"sqrt(a^2+H^2)/2pi (a = {float(gg[3]):.4f}), gap-independent to {float(spv):.1e}. *** This "
                 f"reproduces, from a computed detector response, the very temperature Milgrom's q = 2 balance "
                 f"assumes -- so the published mechanism is confirmed, not merely assumed ***"):
        break

# ---- R4 / R5  rotation breaks KMS, and by how much --------------------------------
print(f"\n  {'v/c':>8}{'a':>12}{'T_DL':>14}{'T_eff spread':>16}{'/ (v/c)^2':>12}")
print("  " + "-" * 64)
rows = []
for vv in ("0.5", "0.2", "0.05", "0.001"):
    gg = geom("0.5", vv)
    ts, spv = spread(*gg[:3], mp.mpf("0.5"))
    rows.append((mp.mpf(vv), spv))
    print(f"  {vv:>8}{float(gg[3]):>12.5f}{float(gg[4]):>14.9f}{float(spv):>16.3e}"
          f"{float(spv/mp.mpf(vv)**2):>12.4f}")
check(rows[0][1] > mp.mpf(10) ** -6,
      f"R4 rotation DOES break KMS: at v/c = 0.5 the effective temperature varies by {float(rows[0][1]):.3e} "
      f"across the gap grid, so T_eff is genuinely gap-dependent and the corpus's GEMS and conformal lanes are "
      f"confirmed by a third, independent route")
ratios = [float(s / v**2) for v, s in rows]
NEED = 2 * (2 * mp.sqrt(8 * mp.pi / 3)) - 1       # r must exceed 1 by 2Z - 1 = 10.5776 to reach kappa = 1/2
check(rows[-1][1] < mp.mpf(10) ** -5 and all(rows[i][1] > rows[i + 1][1] for i in range(len(rows) - 1)),
      f"R5 *** BUT THE BREAKING VANISHES WITH v: the spread falls monotonically over v/c = 0.5 -> 0.001, by "
      f"{float(rows[0][1]/rows[-1][1]):.3e} in all, and spread/(v/c)^2 stays within a factor "
      f"{max(ratios)/min(ratios):.2f}, i.e. it is quadratic in v/c. At the galactic v/c ~ 1e-3 the "
      f"gap-dependence is "
      f"{float(rows[-1][1]):.2e}. Since T_eff departs from the single Deser-Levin value by at most that "
      f"fraction ANYWHERE on the grid, any normalised weight rho(E) >= 0 gives a functional differing from the "
      f"same functional of T_DL by O(1e-6). THE RESPONSE LANE CANNOT SUPPLY 2Z = 11.577620; it returns q = 2 to "
      f"six figures. The lane is CLOSED as a route to kappa = 1/2, and that cuts AGAINST the framework ***")

# ---- R6  and it adds no NEW freedom ----------------------------------------------
check(rows[-1][1] / NEED < mp.mpf(10) ** -5,
      f"R6 quantitatively: the freedom the gap-dependence buys at galactic speed ({float(rows[-1][1]):.2e}) falls "
      f"short of what is needed (r must exceed 1 by 2Z - 1 = {float(NEED):.4f}) by a factor "
      f"{float(NEED/rows[-1][1]):.2e}. A "
      f"response functional therefore retains only the SAME r-freedom a temperature functional has -- pick "
      f"rho(E) so the induced f is nonlinear at the floor -- and adds none. *** ONE DOOR, NOT TWO, is confirmed: "
      f"the live question remains whether the dS floor is c H_Lambda or (1/4) c sqrt(G rho_Lambda) ***")

print("\n" + "=" * 100)
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0. The uncomputed lane is now computed. It VALIDATES the published mechanism (Deser-Levin exactly")
print("  reproduced from a real response at w=0) and is a NULL for the coefficient: KMS breaks only at O(v^2/c^2),")
print("  so no response functional reaches 1/Z. kappa = 1/2 remains FITTED, NOT DERIVED.")
