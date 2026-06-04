#!/usr/bin/env python3
"""
A DISTINCTIVE X-ray test: rising a0 => the galaxy-cluster mass discrepancy must SHRINK with redshift.
====================================================================================================
Carl's instinct: hot X-ray gas. It is the primary cluster mass probe (hydrostatic equilibrium: the gas
temperature + density profile give the gravitating mass). Clusters are MOND's HARDEST regime -- MOND/emergent
gravity under-predicts cluster mass by ~factor 2 (the residual is centrally concentrated, worse in cores).
That is a constraint, not a proof. BUT the framework's rising a0 = cH(z)/Z makes a clean, DISTINCTIVE,
X-ray-testable forward prediction that constant-a0 MOND and LCDM do NOT make:

    Higher a0 at high z => more of the cluster sits in the MOND-boosted regime => MOND-with-baryons explains
    MORE of the dynamics => the UNEXPLAINED missing-mass factor eta(z) = g_obs / [nu(g_bar/a0(z)) * g_bar]
    DECREASES with redshift.

This script (i) computes the predicted eta(z) for constant vs rising a0, (ii) anchors it to the real low-z
cluster numbers, (iii) names the confounders with magnitudes, and (iv) forecasts what homogeneous X-ray
sample (eROSITA/XRISM/Athena era) could detect it. It is a FORECAST, reported as such -- existing
heterogeneous literature (X-COP vs CLASH use different gas treatments) cannot be stacked into a clean z-trend.

Observables (both direct, theory-agnostic): g_obs = (kT/ mu m_p r)(dln rho/dln r + dln T/dln r) from the
X-ray gas; g_bar = G M_bar(<r)/r^2 from gas+stars. MOND: g_obs = nu(g_bar/a0) g_bar; the cluster residual is
eta = g_obs/(nu g_bar). Real anchors: cluster discrepancy ~factor 2 (Sanders 2008); cluster RAR a0 ~ 10x
galaxy (Chae+2020 CLASH); X-COP clusters near the galaxy RAR with careful gas (Eckert+2022) -- the magnitude
is method-dependent, which is exactly why a HOMOGENEOUS z-spanning analysis is required. Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
A0 = 1.2e-10                                   # galaxy a0 at z=0

# modified-gravity (RAR) interpolations: g_obs = nu(y) g_bar, y = g_bar/a0
nu_simple = lambda y: 0.5 + np.sqrt(0.25 + 1/y)
nu_mcg    = lambda y: 1/(1 - np.exp(-np.sqrt(y)))

# a0(z) scenarios
a0_const = lambda z: A0
a0_Ez    = lambda z: A0*E(z)                   # framework: cH(z)/Z
a0_lin   = lambda z: (1.0 + 1.59*z)*1e-10      # MUSE-DARK III observed rate (steeper than E(z))

ETA0 = 1.8                                      # z~0 cluster missing-mass factor (literature ~factor 2)


def eta(z, gbar_over_a00, a0_fn, nu=nu_simple):
    """Missing-mass factor eta(z) = ETA0 * nu(g_bar/a0(0)) / nu(g_bar/a0(z)) at fixed physical g_bar."""
    gbar = gbar_over_a00 * A0
    return ETA0 * nu(gbar/a0_const(0)) / nu(gbar/a0_fn(z))


def main():
    print("#"*92)
    print("# X-RAY CLUSTER TEST -- rising a0 => the cluster mass discrepancy SHRINKS with redshift")
    print("#"*92 + "\n")

    print("="*92); print("(1) THE PREDICTION -- eta(z) for constant vs rising a0 (representative cluster radii)"); print("="*92)
    for gx in (0.3, 0.6, 1.0):
        print(f"  radius with g_bar/a0(0) = {gx} (Newtonian boost nu = {nu_simple(gx):.2f}):")
        print(f"    {'z':>5}{'a0 const':>11}{'a0=E(z)':>10}{'a0=lin(MUSE)':>14}")
        for z in (0.0, 0.5, 1.0, 1.5):
            print(f"    {z:>5.1f}{eta(z,gx,a0_const):>11.2f}{eta(z,gx,a0_Ez):>10.2f}{eta(z,gx,a0_lin):>14.2f}")
        print()
    d_Ez = ETA0 - eta(1.0, 0.6, a0_Ez); d_lin = ETA0 - eta(1.0, 0.6, a0_lin)
    print(f"  => by z=1 the discrepancy drops {d_Ez/ETA0*100:.0f}% (framework E(z)) to {d_lin/ETA0*100:.0f}% (MUSE rate),")
    print(f"     while constant-a0 MOND and LCDM predict NO gravity-driven trend. A distinctive signature.\n")

    print("="*92); print("(2) REAL ANCHORS (low/mid-z) -- and why they cannot yet be stacked into a z-trend"); print("="*92)
    print("""  * z~0.05  X-COP (Eckert+2022): 12 clusters; with careful gas extrapolation they sit NEAR the galaxy
              RAR (scatter 0.11-0.14 dex). Offset "depends strongly on the gas mass extrapolation."
  * z~0.2-0.9 CLASH (Chae+2020): cluster RAR with a0 ~ 9.5e-10 ~ 10x the galaxy a0 (lensing+X-ray+BCG).
  * general  MOND cluster discrepancy ~factor 2, worse in cores (Sanders 2008).
  The magnitude is METHOD-DEPENDENT (gas treatment, lensing vs hydrostatic, mass extrapolation). X-COP and
  CLASH are NOT a clean z-baseline -- different pipelines. => a real test needs ONE homogeneous pipeline run
  across z, not a literature stack. This is a forecast, stated as such.\n""")

    print("="*92); print("(3) CONFOUNDERS (named, with rough magnitudes) -- what could mimic or mask the signal"); print("="*92)
    print("""  * Hydrostatic mass bias evolution (non-thermal pressure, mergers): ~10-20%, and it may GROW with z ->
      the dominant systematic; biases M_dyn, can mimic OR mask the trend. Must be controlled to <10%.
  * Gas/baryon fraction evolution (f_gas): ~10%; relaxed-cluster f_gas is ~constant (f_gas cosmology test)
    but with scatter.
  * Missing baryons (warm-hot gas, depletion): part of the "discrepancy" may be unseen BARYONS, not dark
    mass or a0 -- the X-COP resolution. Confounds the a0 reading directly.
  * Selection (high-z samples favour massive/hot/relaxed): mass-dependent; needs matched samples.
  * a0 universality assumption: the framework's a0 = cH(z)/Z is COSMIC (set by the global horizon), not the
    local cluster overdensity -- the test assumes that, which is itself part of what is being tested.\n""")

    print("="*92); print("(4) FORECAST -- what homogeneous X-ray sample detects the gravity-driven trend"); print("="*92)
    # signal: Delta eta between z~0 and z~1 (rising vs constant). per-cluster eta error ~30% (hydrostatic+baryon).
    sig_Ez = (ETA0 - eta(1.0, 0.6, a0_Ez))/ETA0
    sig_lin = (ETA0 - eta(1.0, 0.6, a0_lin))/ETA0
    sigma_cl = 0.30                              # per-cluster fractional error on eta
    for sig, lab in ((sig_Ez, "E(z)"), (sig_lin, "MUSE rate")):
        # to detect a fractional difference `sig` at 3 sigma between two z-bins: need bin error = sig/3
        need_bin = sig/3
        N = (sigma_cl/need_bin)**2
        print(f"  signal (z=0 vs z=1, {lab}): Delta eta/eta = {sig*100:.0f}%  ->  ~{int(np.ceil(N))} clusters per z-bin for 3 sigma")
    print("""  (per-cluster eta error ~30% from hydrostatic mass + baryon mass.) So ~20-35 well-characterised clusters
  near z~0 and ~20-35 near z~1 -> a 3-sigma test of rising vs constant a0 from CLUSTERS, IF the hydrostatic-
  bias EVOLUTION is held below ~10% (the systematic floor -- it does NOT average down with N). Feasible with
  eROSITA-selected samples + XRISM/Athena temperature profiles on a ~5-10 yr horizon.\n""")

    print("="*92); print("VERDICT"); print("="*92)
    print(f"""  Carl's X-ray instinct lands on a real, distinctive prediction -- but in the framework's HARDEST regime.
  At z~0 the hot-gas data CONSTRAIN us (the ~factor-2 cluster discrepancy MOND can't explain; relocated to the
  dark field). The NEW content: because a0 = cH(z)/Z RISES, the cluster missing-mass factor must DECREASE with
  redshift -- ~{sig_Ez*100:.0f}% by z=1 (E(z)) to ~{sig_lin*100:.0f}% (the steeper MUSE rate) -- a gravity-driven trend with NO
  counterpart in constant-a0 MOND or LCDM (where the cluster dark mass has no a0 to track). It is NOT testable
  on today's heterogeneous literature (X-COP vs CLASH gas treatments differ), and it is systematics-limited
  (hydrostatic-bias evolution). But it is a clean, falsifiable forecast: a homogeneous ~30+30 cluster X-ray
  sample across z=0-1, bias-controlled to <10%, decides it. The honest upgrade: the X-ray gas turns the
  cluster scale from a pure liability into a falsifiable forward test of the rising-a0 bet.""")
    print("="*92)


if __name__ == "__main__":
    main()
