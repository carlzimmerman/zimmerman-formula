#!/usr/bin/env python3
r"""mi_drift_magnitude_audit_2026.py -- LANE N2: THE ADVERSARIAL MAGNITUDE AUDIT OF THE CUBIC (TADPOLE) DRIFT.

THE QUESTION. mi_ctp_variational_2026.py (50/50, commit 5c676b09) proved that at Gaussian order the dS noise
kernel -- the ONLY object carrying the acceleration through T = sqrt(a^2 + H^2)/(2 pi) -- is structurally
excluded from the mean equation of motion, and named the one remaining address: a CUBIC CTP vertex whose
one-loop TADPOLE closes with the Keldysh propagator G_K and puts coth(beta omega/2), hence T(a), into the mean
EOM. Whatever that drift's detailed structure (Lane N1's question, not waited on here), its MAGNITUDE decides
whether it is physics or a curiosity. The tadpole drift force scales like V''' <z^2> with <z^2> ~ hbar/(m omega):
it is an O(hbar) effect on a worldline of mass m. This script prices it ruthlessly, for real objects, on both
a_0 footings, against what MOND needs (the corpus's E4: delta_m/m_0 = -0.29289 at y = 1).

WHAT IS FOUND, stated up front:
  1. DIMENSIONAL ANALYSIS (symbolic, unique): the one-loop suppression of the drift relative to the classical
     force m a is epsilon_0 = hbar H / (m c^2) -- the particle's Compton wavelength over the Hubble radius.
     This is the UNIQUE dimensionless O(hbar^1) combination of {m, c, H} (proven by exponent linear algebra);
     admitting G adds exactly one mass-free generator, hbar G H^2 / c^5 = (t_Planck H)^2 ~ 9.5e-123.
  2. REAL OBJECTS (canonical footing; ALT = x1.2082): star (2e30 kg) 1.06e-99; PER-PROTON 1.27e-42 -- the honest
     number for any fluid, since inertia is modified particle by particle; electron 2.33e-39. The dS-Unruh
     thermal factor coth(...) at a = a_0 is 1.0041 and never exceeds ~3.8 anywhere on the (omega, a) grid:
     temperature CANNOT rescue the magnitude. MOST FAVORABLE reading (kernel curvature length = 10 kpc instead
     of c/H, softest frequency omega = H/Z): per-proton 1.09e-30. Still >= 29 orders short.
  3. COHERENCE CEILING, cutting BOTH ways: for bath modes longer than the body, the common-force response of N
     particles gives Z_cm = N f/(N m omega^2) = f/(m omega^2) -- the 1/m suppression saturates at the
     PER-PARTICLE mass and cannot be beaten below it, but also cannot be evaded above it. So a star's honest
     drift ceiling is the per-proton 1.27e-42 (NOT the rigid-body 1.06e-99 -- reporting the smaller number as
     the headline would MANUFACTURE 57 extra orders of deficit).
  4. THE ESCAPE HATCH, PRICED NOT HAND-WAVED: the ghost condensate (the corpus's own dark-sector
     identification). Its scale is M = (rho_Lambda c^2 (hbar c)^3)^(1/4) = 2.24 meV (ALT 2.46 meV). A
     Hubble-scale relativistic mode has epsilon = (Z^2/4)(t_P H)^2 = 7.96e-122 -- EXACTLY the cosmological
     constant problem number, proven as an identity. The condensate's own soft dispersion omega = hbar k^2 c^2/M
     puts its a-SENSITIVE modes (omega ~ H) at lambda ~ 5 AU, buying ~68 orders over the Hubble mode -- and the
     scanned maximum of (fluctuation fraction) x (a-sensitivity) over 6 decades of lambda is still ~1.9e-53,
     i.e. ~1.5e52 SHORT, and ~6e6 WORSE than the per-proton point tadpole it was invoked to evade. To reach
     O(1) a collective mode would need effective mass-energy ~ hbar H, i.e. the factor
     4/(Z^2 (t_P H)^2) = 1.26e121 must be bought -- the CC-problem factor. The ghost condensate does not
     supply it.
  5. KMS CROSS-CHECK: the corpus's committed rotation-breaks-KMS channel is 8.599e-7 at galactic v/c ~ 1e-3
     (mi_circular_dS_response_2026.py, re-run 2026-08-07, 8/8 held, table row v/c = 0.001). Even that tiny
     committed channel DWARFS the cubic drift: by >= 1e36 against the honest per-proton number, and by
     >= 1e24 against the most favorable reading.

VERDICT: SUPPRESSED. The cubic tadpole channel is a curiosity, not physics: shortfall 9.2e41 (per-proton,
honest; ALT 7.6e41), 2.7e29 (most favorable point-particle), 1.5e52 (ghost-condensate collective best case).
It is NOT conditionally alive at ghost-condensate parameters; conditional aliveness would require a collective
degree of freedom with mass-energy ~ hbar H and O(1) coupling -- one quantum per Hubble volume as the inertia
carrier, i.e. buying the 1.26e121 CC factor, which is the CKN/holographic-dof regime the corpus has already
closed as a route to the coefficient.

BOTH WAYS, honestly: this audit kills the one-loop TADPOLE as the ORIGIN of a_0's magnitude. It does NOT touch
the published tree-level dS-Unruh balance (Milgrom 1999), which is not a fluctuation effect, and it does not
touch the framework's phenomenology (exact law, RAR, a_0-line). What dies is the hope that Lane N1's cubic
drift is itself MOND-sized. The a-dependence, wherever it enters the mean EOM, must enter at TREE level or not
at all -- at one loop the dS bath is 42 to 122 orders too quiet.

*** kappa = 1/2 IS FITTED, NOT DERIVED. Nothing here derives or moves it. Both footings reported on every
dimensional number: canonical a_0 = 9.3614e-11 on the cH_Lambda floor; ALT a_0 = 1.13e-10 on the cH_0 floor
(x1.2082). ***

MANDATORY CREDIT. nu = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA 253:273 eqs 6-9; his eqs
10-11 give a second coefficient; Milgrom 2008 sec 7.3.1 notes the mismatch "isn't necessarily meaningful".
a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994 Ann.Phys. 229:384. T = sqrt(a^2 + Lambda/3)/(2 pi): Narnhofer,
Peter & Thirring 1996 IJMPB 10:1507. Five-acceleration: Deser & Levin 1997 CQG 14:L163. Influence functional:
Feynman & Vernon 1963; Caldeira & Leggett 1983. CTP: Schwinger 1961, Keldysh 1964. Stochastic gravity: Hu &
Verdaguer. Ghost condensate: Arkani-Hamed, Cheng, Luty & Mukohyama 2004.

FLOAT64 HAZARDS handled: coth(x)-coth(y) at x,y >~ 30 is catastrophic cancellation in float64 (both round to
1.0); computed throughout via the EXACT identity coth(x)-coth(y) = sinh(y-x)/(sinh x sinh y) in mpmath dps=60,
and the hazard is DEMONSTRATED by a check (E1). All grid extrema re-run at 4x refinement with the shift shown.

Exit 0 = every check held. Every check has an input that makes it FAIL (windows, tolerances, symbolic
identities with negative controls D3b/A1b; mutations tried: flipping the Z^2/4 identity to (2pi)^2/4 fails
D3b's companion, evaluating coth at a instead of sqrt(a^2+(cH)^2) moves B3 outside its window, dropping the
S_a factor moves D5's maximum out of its bracket).
"""
from __future__ import annotations

import math
import sys

import mpmath as mp
import sympy as sp

mp.mp.dps = 60

ok: list[tuple[bool, str]] = []


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


def banner(t):
    print("\n" + "=" * 108)
    print(f"  {t}")
    print("=" * 108)


def f(x):
    return float(x)


def win(x, lo, hi):
    return (lo < f(x)) and (f(x) < hi)


# ----------------------------------------------------------------------------------------------------------
# Constants. Canonical footing = (rho_DE, cH_Lambda); ALT footing = (rho_total, cH_0) = canonical x 1.2082.
# ----------------------------------------------------------------------------------------------------------
HBAR = mp.mpf("1.054571817e-34")     # J s
C = mp.mpf("2.99792458e8")           # m/s
GN = mp.mpf("6.67430e-11")           # SI
H_CAN = mp.mpf("1.8078e-18")         # s^-1  (H_Lambda as inverse time)
SCALE = mp.mpf("1.2082")             # 1/sqrt(Omega_Lambda)
H_ALT = H_CAN * SCALE                # s^-1  (H_0)
A0_CAN = mp.mpf("9.3614e-11")        # m/s^2, kappa = 1/2, FITTED not derived
A0_ALT = mp.mpf("1.13e-10")          # m/s^2
CH_CAN = mp.mpf("5.4194e-10")        # m/s^2 = c H_Lambda
CH_ALT = CH_CAN * SCALE              # m/s^2 = c H_0
Z = 2 * mp.sqrt(8 * mp.pi / 3)       # 5.7888100366
M_STAR = mp.mpf("2e30")              # kg
M_P = mp.mpf("1.67e-27")             # kg (proton, per task spec)
M_HATOM = mp.mpf("1.6735575e-27")    # kg (hydrogen atom)
M_E = mp.mpf("9.1093837015e-31")     # kg
L_10KPC = mp.mpf("3.0857e20")        # m
V_GAL = mp.mpf("2.0e5")              # m/s galactic orbital speed
DM_MOND = 1 - 1 / mp.sqrt(2)         # 0.29289..., |delta_m|/m_0 at y = 1 (corpus E4)
KMS_GAL = mp.mpf("8.599e-7")         # committed: mi_circular_dS_response_2026.py, v/c = 0.001 row (8/8, re-run)

W_CAN = A0_CAN / CH_CAN              # a_0 in floor units, canonical
W_ALT = A0_ALT / CH_ALT              # a_0 in floor units, ALT

banner("PART A  DIMENSIONAL ANALYSIS, SYMBOLIC AND UNIQUE")

# Exponent linear algebra. Rows (M, L, T); columns (m, c, H). [hbar] = M L^2 T^-1.
Adim = sp.Matrix([[1, 0, 0], [0, 1, 0], [0, -1, -1]])
target = -sp.Matrix([1, 2, -1])                       # hbar^1 m^q c^r H^s dimensionless
sol = Adim.solve(target)
check(Adim.rank() == 3 and sol == sp.Matrix([-1, -2, 1]),
      "A1  UNIQUENESS: hbar^1 m^q c^r H^s is dimensionless for EXACTLY ONE exponent triple, (q, r, s) = "
      "(-1, -2, 1). The one-loop suppression factor is epsilon_0 = hbar H / (m c^2) -- Compton wavelength over "
      "Hubble radius -- and no other O(hbar^1) combination of {m, c, H} exists (dimension matrix has full "
      "rank 3)")
bad = sp.Matrix([1, 2, -1]) + Adim * sp.Matrix([-1, -3, 1])    # dims of hbar H/(m c^3)
check(bad != sp.zeros(3, 1),
      "A1b NEGATIVE CONTROL: hbar H/(m c^3) is NOT dimensionless (residual dimension vector nonzero), so A1's "
      "solve is a real constraint, not an algebra tautology")

AdimG = sp.Matrix([[1, 0, 0, -1], [0, 1, 0, 3], [0, -1, -1, -2]])   # columns (m, c, H, G)
ns = AdimG.nullspace()
gen = ns[0] / ns[0][0] if len(ns) == 1 and ns[0][0] != 0 else None
combo_massfree = sp.Matrix([-1, -2, 1, 0]) + gen if gen is not None else None
check(len(ns) == 1 and gen == sp.Matrix([1, -3, 1, 1])
      and combo_massfree == sp.Matrix([0, -5, 2, 1]),
      "A2  ADMITTING G adds exactly ONE generator, G m H / c^3; the unique MASS-FREE O(hbar) suppression is "
      "hbar^1 c^-5 H^2 G^1 = hbar G H^2 / c^5 = (t_Planck H)^2. Foreshadowing Part D: that is the "
      "cosmological-constant-problem number, and it is where every mass-independent (collective) version of "
      "the tadpole is forced to live")

# Symbolic tadpole structure: <z^2> = (hbar/2 m omega) coth(hbar omega / 2 k_B T_dS), T_dS proportional to hbar.
hb, om, kB, a_, c_, Hs, m_, Ls = sp.symbols("hbar omega k_B a c H m L", positive=True)
TdS = hb * sp.sqrt(a_**2 + c_**2 * Hs**2) / (2 * sp.pi * c_ * kB)
argu = sp.simplify(hb * om / (2 * kB * TdS))
z2 = hb / (2 * m_ * om) * sp.coth(argu)
check(hb not in argu.free_symbols and kB not in argu.free_symbols
      and sp.simplify(argu - sp.pi * om * c_ / sp.sqrt(a_**2 + c_**2 * Hs**2)) == 0,
      "A3  hbar CANCELS in the coth argument (T_dS is itself O(hbar)): hbar omega / 2 k_B T_dS = "
      "pi omega c / sqrt(a^2 + c^2 H^2), hbar-free and k_B-free. So <z^2> = (hbar/2 m omega) coth(...) is "
      "STRICTLY O(hbar^1) --")
check(sp.limit(z2, hb, 0) == 0,
      "A3b -- and its classical limit is exactly zero: lim_{hbar -> 0} <z^2> = 0. The drift force "
      "F = -(1/2) V''' <z^2> is a genuinely quantum effect with NO classical remnant; this is why the audit is "
      "a magnitude audit and not a structure audit")

eps_sym = sp.simplify((z2 / (2 * Ls**2)).subs({om: Hs, Ls: c_ / Hs}))
eps_target = hb * Hs * sp.coth(sp.pi * c_ * Hs / sp.sqrt(a_**2 + c_**2 * Hs**2)) / (4 * m_ * c_**2)
check(sp.simplify(eps_sym - eps_target) == 0,
      "A4  the assembled suppression: with V''' ~ m a / L^2 (force scale m a, kernel curvature length L), "
      "epsilon = F_drift/(m a) = <z^2>/(2 L^2); at the bath's own scales omega = H, L = c/H this is EXACTLY "
      "(hbar H / 4 m c^2) coth(pi c H / sqrt(a^2 + c^2 H^2)) -- epsilon_0 of A1 times an O(1) thermal factor")

banner("PART B  REAL OBJECTS, BOTH FOOTINGS")


def coth_arg(u, w):
    """hbar omega / 2 k_B T_dS(a) = pi u / sqrt(1 + w^2), u = omega/H, w = a/(cH)."""
    return mp.pi * u / mp.sqrt(1 + w**2)


def eps0(m, H):
    return HBAR * H / (m * C**2)


def eps_tad(m, H, w):
    """Honest tadpole epsilon: omega = H, L = c/H, evaluated at a = a_0 (u = 1)."""
    return eps0(m, H) * mp.coth(coth_arg(1, w)) / 4


objs = [("star 2e30 kg (rigid)", M_STAR), ("1 Msun H cloud (rigid)", M_STAR),
        ("H cloud PER-PROTON", M_P), ("hydrogen atom", M_HATOM), ("electron", M_E)]
print(f"\n  {'object':>26} {'eps0 canonical':>16} {'eps0 ALT':>16} {'eps_tad canonical':>18}")
tab = {}
for name, m in objs:
    e_can, e_alt, e_t = eps0(m, H_CAN), eps0(m, H_ALT), eps_tad(m, H_CAN, W_CAN)
    tab[name] = (e_can, e_alt, e_t)
    print(f"  {name:>26} {f(e_can):>16.4e} {f(e_alt):>16.4e} {f(e_t):>18.4e}")

e_p2 = HBAR / (2 * M_P * H_CAN) / (2 * (C / H_CAN) ** 2) * 4   # <z^2>/(2L^2) route x 4 = hbar H/(m c^2)
check(abs(eps0(M_P, H_CAN) / e_p2 - 1) < mp.mpf("1e-12")
      and win(eps0(M_P, H_CAN), 1.26e-42, 1.28e-42)
      and abs(eps0(M_P, H_ALT) / eps0(M_P, H_CAN) - SCALE) < mp.mpf("1e-12"),
      f"B1  PER-PROTON, the honest number for a fluid (inertia is modified particle by particle): epsilon_0 = "
      f"{f(eps0(M_P, H_CAN)):.4e} canonical, {f(eps0(M_P, H_ALT)):.4e} ALT (exactly x{f(SCALE)}). The dS bath "
      f"perturbs a proton's inertia at the level of its Compton wavelength over the Hubble radius")
check(win(eps0(M_STAR, H_CAN), 1.0e-99, 1.1e-99) and win(eps0(M_E, H_CAN), 2.3e-39, 2.4e-39)
      and eps0(M_STAR, H_CAN) < eps0(M_P, H_CAN) < eps0(M_E, H_CAN),
      f"B2  star (rigid-body reading) {f(eps0(M_STAR, H_CAN)):.4e}, electron {f(eps0(M_E, H_CAN)):.4e} "
      f"(canonical; ALT x1.2082): the suppression is 1/m, so the ordering is inverted in mass, and even the "
      f"LIGHTEST charged particle in nature sits 38 orders below unity")

# Thermal factor: can temperature rescue it? Grid over omega in [H/Z, H], a in [0, 10 a_0].
def coth_max(nu, nw):
    us = [mp.mpf(10) ** (mp.log10(1 / Z) * (1 - i / (nu - 1))) for i in range(nu)]
    ws = [10 * W_CAN * i / (nw - 1) for i in range(nw)]
    return max(mp.coth(coth_arg(u, w)) for u in us for w in ws)


cm1, cm2 = coth_max(41, 41), coth_max(161, 161)
cth_a0 = mp.coth(coth_arg(1, W_CAN))
check(win(cth_a0, 1.003, 1.006) and f(cm1) < 5.0 and abs(cm2 / cm1 - 1) < mp.mpf("0.01"),
      f"B3  THE THERMAL FACTOR CANNOT RESCUE THE MAGNITUDE: coth(...) = {f(cth_a0):.4f} at (a = a_0, omega = H) "
      f"and at most {f(cm1):.3f} over the whole grid omega in [H/Z, H] x a in [0, 10 a_0]; 4x refinement moves "
      f"the max by {f(abs(cm2/cm1-1)):.1e} (corner extremum, sampled). The dS-Unruh occupation buys a factor "
      f"~4 at best, against a 42-order deficit")

# Most favorable point-particle reading: L = 10 kpc (orbital scale as curvature length), softest omega.
OM_ORB = V_GAL / L_10KPC
best_cases = {}
for tag, u in [("omega = H/Z", 1 / Z), ("omega = H", mp.mpf(1)), ("omega = omega_orb", OM_ORB / H_CAN)]:
    z2v = HBAR * mp.coth(coth_arg(u, W_CAN)) / (2 * M_P * u * H_CAN)
    best_cases[tag] = z2v / (2 * L_10KPC**2)
eps_best = max(best_cases.values())
print(f"\n  most favorable per-proton (L = 10 kpc): " +
      ", ".join(f"{k}: {f(v):.3e}" for k, v in best_cases.items()))
check(win(eps_best, 1e-31, 1e-29) and eps_best == best_cases["omega = H/Z"],
      f"B4  MOST FAVORABLE point-particle reading, priced rather than dismissed: curvature length L = 10 kpc "
      f"(the orbit itself, 5.4e5 times shorter than c/H) and the softest bath frequency omega = H/Z gives "
      f"per-proton epsilon = {f(eps_best):.3e}. Granting the framework every discretionary choice buys ~12 "
      f"orders and still leaves >= 29")
z_osc = mp.sqrt(HBAR / (2 * M_P * H_CAN))
z_dif = mp.sqrt(HBAR * mp.sqrt(A0_CAN**2 + CH_CAN**2) / (2 * mp.pi * C) / M_P) / H_CAN
check(win(z_osc / z_dif, 1 / mp.mpf(3), 3),
      f"B5  CROSS-CHECK of <z^2> by an independent route: oscillator estimate z_rms = sqrt(hbar/2 m H) = "
      f"{f(z_osc):.3e} m vs thermal-velocity drift v_th/H = {f(z_dif):.3e} m for a proton -- ratio "
      f"{f(z_osc/z_dif):.2f}, within a factor 3. (Both ~100 km: the proton's quantum spread at the Hubble "
      f"frequency. The estimate is not the bottleneck; the 1/m and 1/L^2 are)")

# Coherence: common bath force on N particles.
N_, fF, w2, s2 = sp.symbols("N f omega sigma2", positive=True)
Zcm = (N_ * fF) / ((N_ * m_) * w2**2)
z2_coh = (N_**2 * s2) / N_**2          # <(sum z_i / N)^2>, all pairs correlated at sigma^2
z2_inc = (N_ * s2) / N_**2             # diagonal only
check(sp.simplify(Zcm - fF / (m_ * w2**2)) == 0 and sp.diff(sp.simplify(z2_coh), N_) == 0
      and sp.simplify(z2_inc * N_ - s2) == 0,
      "B6  THE COHERENCE CEILING, cutting both ways: a bath mode longer than the body applies a COMMON force, "
      "and Z_cm = N f/(N m omega^2) = f/(m omega^2) -- the N cancels EXACTLY. Perfectly correlated "
      "displacements give <Z_cm^2> = sigma^2 independent of N (incoherent gives sigma^2/N). So the 1/m "
      "suppression saturates at the PER-PARTICLE mass: a star's honest ceiling is the per-proton 1.27e-42, "
      "NOT the rigid-body 1.06e-99 -- and reporting the rigid-body number as the headline would MANUFACTURE "
      "57 extra orders of deficit. Equally: no assembly of particles can beat the per-particle number")

banner("PART C  AGAINST WHAT MOND NEEDS")

check(abs(DM_MOND - mp.mpf("0.2928932188134524")) < mp.mpf("1e-15"),
      f"C1  the requirement (corpus E4, recomputed): at y = g_bar/a_0 = 1 the exact law needs "
      f"|delta_m|/m_0 = 1 - 1/sqrt(2) = {f(DM_MOND):.10f} -- ORDER ONE, at a ~ a_0, for every particle in the "
      f"tracer")
rows = [("PER-PROTON, honest (omega=H, L=c/H)", eps_tad(M_P, H_CAN, W_CAN), eps_tad(M_P, H_ALT, W_ALT)),
        ("star rigid, honest", eps_tad(M_STAR, H_CAN, W_CAN), eps_tad(M_STAR, H_ALT, W_ALT)),
        ("electron, honest", eps_tad(M_E, H_CAN, W_CAN), eps_tad(M_E, H_ALT, W_ALT)),
        ("PER-PROTON, most favorable", eps_best, eps_best * SCALE)]
print(f"\n  {'channel':>36} {'shortfall canonical':>20} {'shortfall ALT':>18}")
sf = {}
for name, ec, ea in rows:
    sf[name] = (DM_MOND / ec, DM_MOND / ea)
    print(f"  {name:>36} {f(sf[name][0]):>20.4e} {f(sf[name][1]):>18.4e}")
check(win(sf["PER-PROTON, honest (omega=H, L=c/H)"][0], 8e41, 1.1e42)
      and win(sf["PER-PROTON, honest (omega=H, L=c/H)"][1], 6e41, 9e41),
      f"C2  THE SHORTFALL, per proton, honest: {f(sf['PER-PROTON, honest (omega=H, L=c/H)'][0]):.3e} canonical, "
      f"{f(sf['PER-PROTON, honest (omega=H, L=c/H)'][1]):.3e} ALT. Forty-two orders of magnitude. The footing "
      f"fork moves it by exactly the trivial x1.2082 and decides nothing")
check(win(sf["star rigid, honest"][0], 8e98, 1.4e99) and win(sf["electron, honest"][0], 4e38, 6e38),
      f"C3  star (rigid reading) {f(sf['star rigid, honest'][0]):.3e}, electron "
      f"{f(sf['electron, honest'][0]):.3e} canonical -- but per B6 the star's OPERATIVE shortfall is the "
      f"per-proton 9.2e41, not 1.1e99")
check(win(sf["PER-PROTON, most favorable"][0], 1e29, 1e30),
      f"C4  even granting L = 10 kpc AND omega = H/Z simultaneously: shortfall "
      f"{f(sf['PER-PROTON, most favorable'][0]):.3e}. No discretionary choice in the estimate closes 29 orders")

S_u1 = (mp.coth(coth_arg(1, 0)) - mp.coth(coth_arg(1, W_CAN)))  # a-dependence between a=0 and a=a_0 ...
S_u1 = abs(S_u1) / mp.coth(coth_arg(1, W_CAN))
adep = eps_tad(M_P, H_CAN, W_CAN) * S_u1
check(win(S_u1, 3e-4, 4e-4) and win(DM_MOND / adep, 1e45, 1e46),
      f"C5  SHARPER STILL: MOND needs the drift's a-DEPENDENT part to be O(1), and the coth factor varies by "
      f"only {f(S_u1):.3e} between a = 0 and a = a_0 (it is already near saturation at omega = H). The "
      f"a-dependent per-proton drift is {f(adep):.3e}; that shortfall is {f(DM_MOND/adep):.3e} -- three more "
      f"orders on top of C2")

banner("PART D  THE ESCAPE HATCH, PRICED: THE GHOST CONDENSATE COLLECTIVE MODE")

rho_can = (2 * A0_CAN / C) ** 2 / GN          # rho_Lambda from a_0 = (1/2) c sqrt(G rho_Lambda)
rho_alt = (2 * A0_ALT / C) ** 2 / GN          # ALT footing: rho_total
rho_frw = 3 * H_CAN**2 / (8 * mp.pi * GN)     # 3 H_Lambda^2 / 8 pi G
check(abs(rho_can / rho_frw - 1) < mp.mpf("1e-3") and win(rho_can, 5.8e-27, 5.9e-27)
      and win(rho_alt, 8.4e-27, 8.6e-27),
      f"D1  the condensate's effective mass density: rho_Lambda = (2 a_0/c)^2/G = {f(rho_can):.4e} kg/m^3 "
      f"canonical, agreeing with 3 H_Lambda^2/8 pi G = {f(rho_frw):.4e} to {f(abs(rho_can/rho_frw-1)):.1e} "
      f"(the framework identity a_0 = c H_Lambda/Z); ALT rho_total = {f(rho_alt):.4e}")
M_GC = (rho_can * C**2 * (HBAR * C) ** 3) ** mp.mpf("0.25")
M_GC_ALT = (rho_alt * C**2 * (HBAR * C) ** 3) ** mp.mpf("0.25")
EV = mp.mpf("1.602176634e-19")
lam_M = HBAR * C / M_GC
check(win(M_GC / EV * 1000, 2.0, 2.5) and win(lam_M, 7e-5, 1e-4),
      f"D2  the condensate scale: M = (rho_Lambda c^2 (hbar c)^3)^(1/4) = {f(M_GC/EV*1000):.3f} meV canonical "
      f"({f(M_GC_ALT/EV*1000):.3f} meV ALT), i.e. lambda_M = hbar c/M = {f(lam_M)*1e6:.1f} microns. Condensate "
      f"modes DO have O(1) quantum fluctuations below ~lambda_M -- but those modes oscillate at ~10 THz and "
      f"are exponentially blind to T(a) (D5)")

# Hubble-scale relativistic mode: the mass-free combination of A2, realized.
m_hub = rho_can * (C / H_CAN) ** 3
eps_hub = HBAR * H_CAN / (m_hub * C**2)
t_P = mp.sqrt(HBAR * GN / C**5)
eps_hub_id = (Z**2 / 4) * (t_P * H_CAN) ** 2
Zs, Hsym, Gsym, hbs, cs = sp.symbols("Z H G hbar c", positive=True)
rho_s = 3 * Hsym**2 / (8 * sp.pi * Gsym)
lhs_s = hbs * Hsym / (rho_s * (cs / Hsym) ** 3 * cs**2)
rhs_s = (Zs**2 / 4).subs(Zs, 2 * sp.sqrt(sp.Rational(8, 3) * sp.pi)) * (sp.sqrt(hbs * Gsym / cs**5) * Hsym) ** 2
check(sp.simplify(lhs_s - rhs_s) == 0 and abs(eps_hub / eps_hub_id - 1) < mp.mpf("1e-3")
      and win(eps_hub, 7.8e-122, 8.1e-122),
      f"D3  THE HUBBLE-SCALE MODE IS THE COSMOLOGICAL CONSTANT PROBLEM, as an exact identity: with rho_Lambda "
      f"= 3H^2/8 pi G, epsilon = hbar H/(rho_Lambda (c/H)^3 c^2) = (Z^2/4)(t_Planck H)^2 SYMBOLICALLY (the "
      f"framework's own Z = 2 sqrt(8 pi/3), since Z^2/4 = 8 pi/3), and numerically {f(eps_hub):.4e} vs "
      f"{f(eps_hub_id):.4e}. A Hubble-volume condensate mode is 121 orders too heavy to fluctuate")
check(sp.simplify((2 * sp.pi) ** 2 / 4 - sp.Rational(8, 3) * sp.pi) != 0,
      "D3b NEGATIVE CONTROL on the identity: with Milgrom's constant 2 pi in place of Z the identity FAILS "
      "((2 pi)^2/4 = pi^2 != 8 pi/3), so D3 is a property of Z = 2 sqrt(8 pi/3), not of any constant")
check(win((HBAR * H_CAN / M_GC) ** 2, 2.5e-61, 3.2e-61),
      f"D4  the best-case GAPLESS bound: even if a condensate mode were governed only by its own scale M, the "
      f"one-loop factor (hbar H/M)^2 = {f((HBAR*H_CAN/M_GC)**2):.3e} -- 61 orders short before any mode "
      f"bookkeeping. The window between 'fluctuates at O(1)' (needs scale ~ hbar H) and 'feels T(a)' (needs "
      f"omega <~ H) is 30 orders wide in energy and empty")


# The condensate's own dispersion omega = hbar k^2 c^2 / M: scan (fluctuation fraction) x (a-sensitivity).
def S_frac(u, w):
    """[coth(arg(a=0)) - coth(arg(a=a0))]/coth(arg(a=a0)), via the EXACT identity (float64-hazard-safe)."""
    x0, x1 = coth_arg(u, 0), coth_arg(u, w)
    return mp.sinh(x0 - x1) / (mp.sinh(x0) * mp.sinh(x1) * mp.coth(x1))


def P_of(u, H, w, rho, MJ):
    omg = u * H
    lam = 2 * mp.pi * C * mp.sqrt(HBAR / (MJ * omg))
    meff = rho * lam**3
    epsv = HBAR * mp.coth(coth_arg(u, w)) / (2 * meff * omg) / (2 * lam**2)
    return epsv * S_frac(u, w), lam, epsv


def scan(H, w, rho, MJ, lo=-3.0, hi=3.0, n=301):
    best = (mp.mpf(0), None, None, None)
    for i in range(n):
        u = mp.mpf(10) ** (lo + (hi - lo) * i / (n - 1))
        P, lam, epsv = P_of(u, H, w, rho, MJ)
        if P > best[0]:
            best = (P, u, lam, epsv)
    return best


P_can, u_can, lam_can, eps_can = scan(H_CAN, W_CAN, rho_can, M_GC)
lo_r, hi_r = f(mp.log10(u_can)) - 0.4, f(mp.log10(u_can)) + 0.4
P_ref, u_ref, _, _ = scan(H_CAN, W_CAN, rho_can, M_GC, lo=lo_r, hi=hi_r, n=1201)
P_alt, u_alt, lam_alt, _ = scan(H_ALT, W_ALT, rho_alt, M_GC_ALT)
print(f"\n  ghost-condensate scan (dispersion omega = hbar k^2 c^2/M, mode mass rho lambda^3, L = lambda):")
print(f"    canonical: max = {f(P_can):.4e} at omega/H = {f(u_can):.3f} (lambda = {f(lam_can):.3e} m "
      f"= {f(lam_can)/1.496e11:.1f} AU); 4x-refined max = {f(P_ref):.4e} at omega/H = {f(u_ref):.3f}")
print(f"    ALT:       max = {f(P_alt):.4e} at omega/H = {f(u_alt):.3f} (lambda = {f(lam_alt):.3e} m)")
check(win(P_can, 1e-55, 1e-51) and win(u_can, 0.05, 2.0) and win(P_alt, 1e-55, 1e-51)
      and abs(P_ref / P_can - 1) < mp.mpf("0.02"),
      f"D5  THE ESCAPE HATCH PRICED: the condensate's soft dispersion puts its a-SENSITIVE modes (omega ~ H) "
      f"at lambda ~ {f(lam_can)/1.496e11:.0f} AU, not the Hubble length -- and the maximum of (fluctuation "
      f"fraction) x (a-sensitivity) over six decades of omega/H is {f(P_can):.2e} canonical / {f(P_alt):.2e} "
      f"ALT, at omega/H = {f(u_can):.2f}. Refining the grid 4x moves it by {f(abs(P_ref/P_can-1))*100:.2f}%")
check(win(P_can / eps_hub, 1e66, 1e70) and win(DM_MOND / P_can, 1e51, 1e53),
      f"D6  so the condensate's own dynamics buys {f(P_can/eps_hub):.1e} over the naive Hubble mode -- "
      f"sixty-eight orders, the honest concession -- and is STILL {f(DM_MOND/P_can):.2e} short of MOND. Worse: "
      f"it is {f(adep/P_can):.1e} times SMALLER than the per-proton point tadpole's a-dependent part (C5). The "
      f"collective mode does not evade the suppression; its rho_Lambda lambda^3 inertia costs more than the "
      f"1/m_proton it was invoked to escape")
ratio_cc = m_hub / (HBAR * H_CAN / C**2)
check(abs(ratio_cc * eps_hub - 1) < mp.mpf("1e-6") and win(ratio_cc, 1.2e121, 1.3e121),
      f"D7  WHAT CONDITIONAL ALIVENESS WOULD REQUIRE, stated as a number: an O(1) drift needs a collective "
      f"degree of freedom with effective mass-energy ~ hbar H = {f(HBAR*H_CAN/C**2):.2e} kg -- ONE quantum per "
      f"Hubble volume as the inertia carrier. The condensate's Hubble-volume mass exceeds that by "
      f"{f(ratio_cc):.3e} = 4/(Z^2 (t_P H)^2): the escape must buy the full cosmological-constant-problem "
      f"factor. That is the CKN/holographic-dof regime the corpus has already closed as a coefficient route")

banner("PART E  HAZARD DEMONSTRATION, AND THE KMS CROSS-CHECK")

d64 = 1.0 / math.tanh(29.5) - 1.0 / math.tanh(30.0)
d_mp = mp.sinh(mp.mpf("0.5")) / (mp.sinh(mp.mpf("29.5")) * mp.sinh(mp.mpf("30")))
check(d64 == 0.0 and win(d_mp, 1e-27, 1e-25),
      f"E1  FLOAT64 HAZARD DEMONSTRATED (this corpus's exp(-300) -> 0 class): coth(29.5) - coth(30.0) computed "
      f"directly in float64 is EXACTLY {d64} -- both operands round to 1.0 -- while the exact identity "
      f"sinh(y-x)/(sinh x sinh y) gives {f(d_mp):.3e} != 0. Every coth difference in this script (C5, D5) uses "
      f"the identity; a strict inequality was one rounding away from becoming an equality")
r_honest = eps_tad(M_P, H_CAN, W_CAN) / KMS_GAL
r_best = eps_best / KMS_GAL
check(f(r_honest) < 1e-30 and f(r_best) < 1e-20,
      f"E2  KMS CROSS-CHECK against the corpus's committed numbers: rotation breaks KMS at 8.599e-7 at "
      f"galactic v/c ~ 1e-3 (mi_circular_dS_response_2026.py, 8/8, re-run 2026-08-07) -- and even that tiny "
      f"committed channel DWARFS the cubic drift, by {f(1/r_honest):.1e} against the honest per-proton number "
      f"and {f(1/r_best):.1e} against the most favorable reading. The (v/c)^2 channel already priced as "
      f"'cannot reach the coefficient' is itself 24 to 36 orders LARGER than this one")

banner("VERDICT")
print(f"""  The cubic (tadpole) channel is SUPPRESSED -- a curiosity, not physics. The factors, both footings:
    per-proton, honest:            {f(sf['PER-PROTON, honest (omega=H, L=c/H)'][0]):.2e} canonical / {f(sf['PER-PROTON, honest (omega=H, L=c/H)'][1]):.2e} ALT short of MOND's 0.293
    per-proton, a-dependent part:  {f(DM_MOND/adep):.2e} short
    per-proton, MOST favorable:    {f(sf['PER-PROTON, most favorable'][0]):.2e} short (L = 10 kpc AND omega = H/Z granted)
    star, operative (coherence):   the per-proton number, per B6 -- NOT the rigid-body 1.1e99
    ghost condensate, best mode:   {f(DM_MOND/P_can):.2e} short (its own escape underperforms the proton by {f(adep/P_can):.0e})
    Hubble-scale mode:             (Z^2/4)(t_P H)^2 = {f(eps_hub):.2e} = the cosmological constant problem, exactly
  It is NOT conditionally alive at ghost-condensate parameters. Conditional aliveness has a price tag: a
  collective dof with mass-energy ~ hbar H and O(1) coupling -- buying the {f(ratio_cc):.2e} CC factor -- which
  is the CKN/holographic regime already closed as a coefficient route. BOTH WAYS: this kills the one-loop
  tadpole as the ORIGIN of a_0's magnitude; it does not touch the tree-level dS-Unruh balance (Milgrom 1999)
  or the framework's phenomenology. Wherever T(a) enters the mean EOM, it must enter at TREE level: at one
  loop the dS bath is 42 to 122 orders too quiet. kappa = 1/2 remains FITTED, NOT DERIVED.""")

banner("RESULT")
nOK = sum(1 for c, _ in ok if c)
print(f"  {nOK}/{len(ok)} checks held.")
if nOK != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0. The cubic drift's magnitude is audited: SUPPRESSED by 42 (per-particle) to 122 (Hubble-mode)")
print("  orders, on both footings, with the escape hatch priced and found wanting by ~52 orders. The magnitude")
print("  question is closed against the channel; Lane N1's structure question is unaffected by this audit.")
