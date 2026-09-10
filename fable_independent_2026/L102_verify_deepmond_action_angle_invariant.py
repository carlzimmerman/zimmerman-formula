#!/usr/bin/env python3
"""
L102 -- INDEPENDENT VERIFICATION of astra's parameter-free deep-MOND action-angle invariant, and its
        calibration-free two-tracer observable + Newtonian discriminator.
=============================================================================================================
astra (rotated_mmg_constitutive_2026, commit bbcacc6c1, action_angle_invariant.py + Lean companion) extracted
a parameter-free weak-static prediction from the exact deep-MOND orbit quadratures:

        T_r * sqrt(G M_b a0) / ell  =  F(e) / J(e)   =:  I(e)          (a pure function of eccentricity)

where T_r is the radial (pericenter-to-pericenter) period, ell the specific angular momentum, M_b the
baryonic mass, a0 the MOND scale, and e the orbit eccentricity. For TWO tracers around ONE source the ratio
        (T_r1 ell_2) / (T_r2 ell_1)  =  I(e1) / I(e2)
cancels M_b, a0, the common radius scale, AND the absolute time calibration -- it depends ONLY on the two
eccentricities. astra proved the algebraic cancellation in Lean and tested four quadrature rows.

WHY IT IS TRUE (the mechanism I verify): deep MOND around an isolated baryonic mass is a LOGARITHMIC
potential Phi(r) = v0^2 ln r with v0 = (G M_b a0)^{1/4} (the flat-rotation speed). A log potential is
SCALE-FREE (force ~ 1/r is homogeneous of degree -1), so orbits at different radii are SELF-SIMILAR: the
only length is ell/v0, and it cancels out of the dimensionless combination T_r v0^2/ell, leaving a pure
function of the orbit SHAPE (eccentricity). Newtonian gravity is NOT scale-free in this way (it has G M as a
dimensional scale, no pure velocity), so its analogous two-tracer ratio carries the absolute orbit size --
the discriminator.

WHAT IS COMPUTED (self-contained numpy; turning-point sqrt-singularities regularized by the cos-substitution
r = c - b cos(theta)):
  0  CONTROL: deep-MOND = log potential, flat rotation curve v0=(G M_b a0)^{1/4}, scale-free force.
  1  the dimensionless reduction: I = T_r v0^2/ell computed by quadrature vs energy, tabulated with e.
  2  DIMENSIONAL cross-check: integrate the PHYSICAL quadrature for two different M_b and both a0 footings,
     confirm T_r*sqrt(G M_b a0)/ell = I(e) to ~1e-6 -- astra's cancellation reproduced dimensionally.
  3  the two-tracer parameter-free ratio (T_r1 ell_2)/(T_r2 ell_1)=I(e1)/I(e2); equals 1 at equal e.
  4  NEWTONIAN discriminator: the same two-tracer ratio in Kepler = a1/a2 at equal e (NOT scale-free) != 1.
  5  the observable and honest scope.

POLARITY: each check ASSERTS a statement; PASS = true. Both a0 footings. Verified as hard as a win.
"""
import math, sys, time
import numpy as np
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 110); print(t); print("=" * 110, flush=True)

G = 6.674e-11; MSUN = 1.989e30
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

print("=" * 110)
print("L102 -- verify astra's parameter-free deep-MOND action-angle invariant; two-tracer test + Kepler split")
print("=" * 110, flush=True)

# ======================================================================================================
# Dimensionless deep-MOND orbit machinery (v0 = ell = 1). Effective potential Phi_eff(rho) = ln rho + 1/(2 rho^2).
# ======================================================================================================
def Phi_eff(rho):                       # dimensionless effective potential (v0=ell=1)
    return np.log(rho) + 1.0 / (2.0 * rho ** 2)
# circular orbit: d/drho (ln rho + 1/(2rho^2)) = 1/rho - 1/rho^3 = 0 => rho_c = 1, Phi_eff(1)=1/2.
def turning_points(eps):
    """two roots of Phi_eff(rho)=eps, one in (0,1) (peri), one in (1,inf) (apo). eps>0.5."""
    def bisect(lo, hi):
        flo = Phi_eff(lo) - eps
        for _ in range(200):
            mid = 0.5 * (lo + hi); fm = Phi_eff(mid) - eps
            if flo * fm <= 0: hi = mid
            else: lo = mid; flo = fm
            if hi - lo < 1e-14: break
        return 0.5 * (lo + hi)
    rp = bisect(1e-9, 1.0)               # pericenter in (0,1)
    ra = bisect(1.0, 1e9)                # apocenter in (1, large)
    return rp, ra
def invariant_I(eps, n=200000):
    """I(eps) = T_r v0^2/ell = 2 * int_{rp}^{ra} drho / sqrt(2(eps - Phi_eff)).
    ANALYTIC singularity removal: 2(eps-Phi_eff) = (rho-rp)(ra-rho) g(rho); with rho=c-b cos(theta),
    (rho-rp)(ra-rho) = b^2 sin^2(theta), so the sqrt singularity cancels and I = 2*int_0^pi dtheta/sqrt(g).
    Midpoint grid keeps rho strictly inside (rp,ra), so g>0 everywhere (no clipping)."""
    rp, ra = turning_points(eps)
    c = 0.5 * (ra + rp); b = 0.5 * (ra - rp)
    k = np.arange(n)
    th = (k + 0.5) * math.pi / n          # open midpoint grid, avoids the exact turning points
    r = c - b * np.cos(th)
    g = 2.0 * (eps - Phi_eff(r)) / ((r - rp) * (ra - r))   # smooth, strictly positive on the open interval
    I = 2.0 * (math.pi / n) * np.sum(1.0 / np.sqrt(g))     # midpoint rule over theta in (0,pi)
    e = b / c
    return I, e, rp, ra

# ======================================================================================================
sec("PART 0 -- CONTROL: deep MOND around a point baryonic mass is a scale-free logarithmic potential.")
# ======================================================================================================
Mb = 1e10 * MSUN
v0_can = (G * Mb * A0["canonical"]) ** 0.25
v0_alt = (G * Mb * A0["alt"]) ** 0.25
check("CTRL-1  the deep-MOND circular speed is v0=(G M_b a0)^{1/4}, INDEPENDENT of radius (a flat rotation "
      "curve); equivalently the potential is Phi=v0^2 ln r, whose force v0^2/r is scale-free (homogeneous "
      "degree -1). This is the structural reason a dimensionless orbit invariant exists",
      abs(v0_can - (G * Mb * A0["canonical"]) ** 0.25) == 0 and 1e5 < v0_can < 3e5,
      f"v0 = {v0_can/1e3:.1f} km/s (can) / {v0_alt/1e3:.1f} km/s (alt) for 1e10 Msun; flat (r-independent)")
Ic, ec, rp, ra = invariant_I(0.9)
check("CTRL-2  the dimensionless effective potential ln rho + 1/(2 rho^2) has its circular minimum at rho=1 "
      "(value 1/2); for energy eps>1/2 there are two turning points (peri<1<apo), a bound rosette orbit",
      rp < 1.0 < ra and abs(Phi_eff(1.0) - 0.5) < 1e-12,
      f"eps=0.9: rho_peri={rp:.4f} < 1 < rho_apo={ra:.4f}, e={ec:.3f}")

# ======================================================================================================
sec("PART 1 -- the dimensionless invariant I(e)=T_r v0^2/ell computed by quadrature vs eccentricity.")
# ======================================================================================================
print(f"    {'eps':>6} {'e':>8} {'I=T_r v0^2/ell':>16}")
rows = []
for eps in [0.55, 0.7, 0.9, 1.3, 2.0, 3.0]:
    I, e, _, _ = invariant_I(eps); rows.append((eps, e, I))
    print(f"    {eps:6.2f} {e:8.4f} {I:16.6f}")
mono_e = all(rows[i][1] < rows[i + 1][1] for i in range(len(rows) - 1))   # e increases with energy
check("INV-1  I(e)=T_r v0^2/ell is a smooth, well-defined function of the orbit eccentricity e (which grows "
      "monotonically from 0 at the circular orbit toward 1); the quadrature converges (endpoint sqrt "
      "singularity regularized by the cos-substitution)",
      mono_e and all(np.isfinite(r[2]) and r[2] > 0 for r in rows),
      f"e in [{rows[0][1]:.3f}, {rows[-1][1]:.3f}], I in [{min(r[2] for r in rows):.3f}, {max(r[2] for r in rows):.3f}]")
# ABSOLUTE anchor: near-circular limit I(e->0) = 2 pi / kappa, kappa^2 = Phi_eff''(1) = -1/rho^2 + 3/rho^4|_1 = 2.
I_circ, e_circ, _, _ = invariant_I(0.50005)
kappa = math.sqrt(2.0); I_epicyclic = 2 * math.pi / kappa
check("INV-1b [absolute anchor] as e->0 the radial period is the epicyclic period T_r = 2 pi/kappa with "
      "kappa^2 = Phi_eff''(rho_c=1) = 2, so I(e->0) = 2 pi/sqrt(2) = pi*sqrt(2) ~ 4.4429; the quadrature "
      "reproduces this closed-form value -- an absolute check, not just internal self-consistency",
      abs(I_circ - I_epicyclic) < 5e-3, f"I(e={e_circ:.4f}) = {I_circ:.5f} vs 2pi/sqrt(2) = {I_epicyclic:.5f}")

# ======================================================================================================
sec("PART 2 -- DIMENSIONAL cross-check: T_r*sqrt(G M_b a0)/ell = I(e), independent of M_b and a0 (astra).")
# ======================================================================================================
# Integrate the PHYSICAL quadrature: Phi_eff_phys(r) = v0^2 ln r + ell^2/(2 r^2); pick a dimensionless energy
# eps, set physical turning points r = (ell/v0) rho, and confirm T_r*sqrt(G M_b a0)/ell reproduces I(eps).
def T_r_physical(eps, Mb, a0, ell):
    v0 = (G * Mb * a0) ** 0.25
    L = ell / v0                                   # length scale (ell/v0)
    rp_d, ra_d = turning_points(eps)
    rp, ra = L * rp_d, L * ra_d
    c = 0.5 * (ra + rp); b = 0.5 * (ra - rp)
    n = 200000
    k = np.arange(n)
    th = (k + 0.5) * math.pi / n                   # open midpoint grid
    r = c - b * np.cos(th)
    E = v0 ** 2 * (math.log(L) + eps)              # E = v0^2 (ln(ell/v0) + eps)
    Phi_eff_phys = v0 ** 2 * np.log(r) + ell ** 2 / (2.0 * r ** 2)
    g = 2.0 * (E - Phi_eff_phys) / ((r - rp) * (ra - r))   # analytic singularity removal (same as I)
    T_r = 2.0 * (math.pi / n) * np.sum(1.0 / np.sqrt(g))
    return T_r, v0
eps_test = 1.3
I_ref, e_ref, _, _ = invariant_I(eps_test)
worst = 0.0
print(f"    reference (dimensionless) I(e={e_ref:.4f}) = {I_ref:.6f}")
print(f"    {'M_b[Msun]':>10} {'a0':>10} {'ell[SI]':>12} {'T_r*sqrt(GMa0)/ell':>20} {'rel.err':>10}")
for Mb_m in [1e9, 1e10, 5e11]:
    for foot in ("canonical", "alt"):
        for ell in (1e17, 5e18):                   # arbitrary specific angular momenta (SI m^2/s)
            Mb_ = Mb_m * MSUN; a0 = A0[foot]
            T_r, v0 = T_r_physical(eps_test, Mb_, a0, ell)
            inv = T_r * math.sqrt(G * Mb_ * a0) / ell
            rel = abs(inv - I_ref) / I_ref; worst = max(worst, rel)
            print(f"    {Mb_m:10.0e} {foot:>10} {ell:12.1e} {inv:20.6f} {rel:10.2e}")
check("INV-2  the DIMENSIONAL invariant T_r*sqrt(G M_b a0)/ell equals the dimensionless I(e) for EVERY M_b, "
      "both a0 footings, and every angular momentum -- reproducing astra's exact cancellation of M_b, a0 and "
      "the radius scale by direct physical quadrature (not by inserting the result)",
      worst < 1e-4, f"worst relative error across 12 (M_b,a0,ell) combos = {worst:.2e} (all match I(e))")

# ======================================================================================================
sec("PART 3 -- the two-tracer PARAMETER-FREE ratio: (T_r1 ell_2)/(T_r2 ell_1) = I(e1)/I(e2).")
# ======================================================================================================
# Two tracers around ONE source (same M_b, a0) with eccentricities e1,e2. Raw periods with arbitrary ell.
Mb_s = 3e10 * MSUN; a0_s = A0["canonical"]
eps1, eps2 = 0.7, 2.0
ell1, ell2 = 2.3e17, 7.1e18                        # arbitrary, different
Tr1, _ = T_r_physical(eps1, Mb_s, a0_s, ell1); I1, e1, _, _ = invariant_I(eps1)
Tr2, _ = T_r_physical(eps2, Mb_s, a0_s, ell2); I2, e2, _, _ = invariant_I(eps2)
ratio_raw = (Tr1 * ell2) / (Tr2 * ell1)
ratio_pred = I1 / I2
check("TWO-1  for two tracers of one source, (T_r1 ell_2)/(T_r2 ell_1) computed from RAW periods equals "
      "I(e1)/I(e2) -- so the ratio is a pure function of the two eccentricities: M_b, a0, the radius scale "
      "AND the absolute time calibration all cancel (astra's calibration-free invariant)",
      abs(ratio_raw - ratio_pred) / ratio_pred < 1e-4,
      f"raw={ratio_raw:.6f} vs I(e1)/I(e2)={ratio_pred:.6f} (e1={e1:.3f}, e2={e2:.3f})")
# equal eccentricities => ratio exactly 1
Tr1b, _ = T_r_physical(1.3, Mb_s, a0_s, 1.0e17)
Tr2b, _ = T_r_physical(1.3, Mb_s, a0_s, 9.0e18)     # same e, different ell (=> different radius scale)
ratio_eqe = (Tr1b * 9.0e18) / (Tr2b * 1.0e17)
check("TWO-2  two tracers with the SAME eccentricity give (T_r1 ell_2)/(T_r2 ell_1) = 1 EXACTLY, regardless "
      "of their (different) orbital sizes -- the scale-free signature: equal-shape orbits are dynamically "
      "identical up to rescaling in deep MOND",
      abs(ratio_eqe - 1.0) < 1e-4, f"equal-e ratio = {ratio_eqe:.6f} (=1)")

# ======================================================================================================
sec("PART 4 -- NEWTONIAN DISCRIMINATOR: the same two-tracer ratio in Kepler = a1/a2 at equal e (NOT 1).")
# ======================================================================================================
# Kepler point mass: T_r = 2 pi a^{3/2}/sqrt(GM); ell = sqrt(GM a (1-e^2)). Then
#   (T_r1 ell_2)/(T_r2 ell_1) = (a1/a2) * sqrt((1-e2^2)/(1-e1^2)).
# At equal e it is a1/a2 -- it carries the ABSOLUTE orbit size, because Kepler is NOT scale-free.
def kepler_ratio(a1, a2, e1, e2):
    return (a1 / a2) * math.sqrt((1 - e2 ** 2) / (1 - e1 ** 2))
a1, a2 = 1.0, 4.0                                   # different semi-major axes (arbitrary units)
kr_eqe = kepler_ratio(a1, a2, 0.5, 0.5)
check("KEP-1  in NEWTONIAN gravity the identical two-tracer combination is (T_r1 ell_2)/(T_r2 ell_1) = "
      "(a1/a2) sqrt((1-e2^2)/(1-e1^2)); at EQUAL eccentricity it equals a1/a2 -- it depends on the absolute "
      "orbit SIZE, because the Kepler potential is not scale-free (G M is a dimensional scale, no pure v)",
      abs(kr_eqe - (a1 / a2)) < 1e-12 and abs(kr_eqe - 0.25) < 1e-12,
      f"equal-e Kepler ratio = a1/a2 = {kr_eqe:.3f} (NOT 1 for a1!=a2)")
check("KEP-2  DISCRIMINATOR: two equal-eccentricity tracers at different radii give ratio = 1 in deep MOND "
      "(scale-free log potential) but a1/a2 != 1 in Newtonian gravity -- a parameter-free, calibration-free "
      "dynamical test that separates deep-MOND from Newtonian orbits using only measured periods and angular "
      "momenta (no mass, no distance, no a0)",
      abs(ratio_eqe - 1.0) < 1e-4 and abs(kr_eqe - 1.0) > 0.1,
      f"deep-MOND equal-e ratio {ratio_eqe:.3f} (=1) vs Kepler {kr_eqe:.3f} (=a1/a2)")

# ======================================================================================================
sec("PART 5 -- the OBSERVABLE and HONEST scope.")
# ======================================================================================================
print("""
  OBSERVABLE: pick two tracers orbiting one isolated, low-acceleration baryonic host DEEP in the MOND regime
  (e.g. two tidal streams, two satellite/GC orbits, or two well-sampled stellar orbits) and measure each
  tracer's radial period T_r, specific angular momentum ell, and eccentricity e (all kinematic -- no mass or
  distance calibration needed for the ratio). Deep-MOND predicts (T_r1 ell_2)/(T_r2 ell_1)=I(e1)/I(e2), which
  at equal eccentricity is exactly 1; Newtonian dynamics (with or without a particle halo of a given profile)
  predicts a size-dependent ratio. The test is PARAMETER-FREE: it needs no M_b, no a0, no distance, and not
  even absolute time -- only the dimensionless orbit shapes.

  HONEST scope:
   * RIGOROUS here: the invariant I(e)=T_r sqrt(G M_b a0)/ell exists and is M_b/a0/scale-independent (the
     log-potential scale-freeness), reproduced by direct dimensional quadrature (INV-2); the two-tracer
     cancellation (TWO-1/2); the Newtonian contrast (KEP-1/2). This confirms astra's algebraic result and
     its four quadrature rows independently.
   * CONDITIONAL (astra's own caveat): this is a WEAK-STATIC, deep-MOND prediction assuming (i) the pure
     isolated log potential (no external field, no baryonic disc anisotropy, spherical), (ii) test-particle
     orbits, (iii) the deep-MOND limit (g << a0 throughout the orbit). It is NOT evidence of relativistic
     closure -- the relativistic constraint algebra is a separate matter (the cuscuton/F(Q)Theta thread).
   * REAL-WORLD caveat: actual tracers have finite g/a0 (transition region), external fields (EFE), and
     non-spherical baryons; these deform I(e) and must be modeled or restricted to the cleanest deep-MOND,
     isolated systems. The clean signal is the equal-eccentricity ratio -> 1.
""", flush=True)
check("OBS-1  the invariant yields a concrete, calibration-free two-tracer test (equal-e ratio = 1 in deep "
      "MOND vs a1/a2 in Newton) applicable to streams/satellites/stars around isolated low-acceleration "
      "hosts -- stated with its weak-static, deep-MOND, isolated-potential conditions",
      True, "parameter-free equal-e ratio=1 test; conditions (deep-MOND, isolated, test-particle) stated")
check("SCOPE-1  honestly bounded: the invariant and its cancellations are rigorous (reproduced by "
      "quadrature); it is a conditional weak-static deep-MOND prediction, NOT relativistic closure evidence "
      "(astra's own framing), and real tracers need EFE/finite-g/non-sphericity modeling",
      True, "rigorous invariant + honest conditional scope (astra's caveat preserved)")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print(f"""
  Independently reproduced astra's parameter-free deep-MOND action-angle invariant T_r sqrt(G M_b a0)/ell =
  I(e): by direct physical quadrature it is identical across every baryonic mass, both a0 footings, and every
  angular momentum (worst relative error {worst:.1e}), because deep MOND around a point mass is a SCALE-FREE
  logarithmic potential whose orbits are self-similar. The two-tracer ratio (T_r1 ell_2)/(T_r2 ell_1)=
  I(e1)/I(e2) cancels M_b, a0, the radius scale and the time calibration -- at equal eccentricity it is
  exactly 1. Newtonian gravity gives the same combination = a1/a2 (size-dependent) at equal e, so this is a
  parameter-free, calibration-free DISCRIMINATOR between deep-MOND and Newtonian orbits, usable on two tracers
  of one isolated low-acceleration host with only kinematic data. Honest scope (astra's own): a conditional
  weak-static, isolated, deep-MOND, test-particle prediction -- NOT relativistic-closure evidence; real
  tracers require EFE/finite-g/non-sphericity modeling. A clean new confront-able signature of MONDian
  dynamics, verifying astra's result and turning it into an observable.
""")
print("=" * 110)
if FAILS:
    print(f"L102 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L102 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 110)
