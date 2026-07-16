#!/usr/bin/env python3
"""
direction_cones_mc.py -- LANE 2 PHASE-2 HARDENING: Monte Carlo direction-cones for the
175 SPARC g_ext unit vectors (aligned-firing prep, 2026-07-16).

PURPOSE
  The 81 soft-flag rows of gext_vectors.csv (dominant-contributor |g| share < 0.5) have
  no per-row direction uncertainty. This script re-runs the Chae-2021-style vector sum
  N_REAL times per SPARC galaxy with the CATALOG INPUTS perturbed within honest errors,
  and reports the direction-cone half-angle (68% and 90%) of the realization directions
  around the banked central vector.

REUSES (imports, does not re-implement) the frozen estimator:
  /Users/carlzimmerman/new_physics/gext_vectors_2026/src/gext_estimator.py
  (GextEstimator.field_at does the full 2M++ + MCXC sum incl. self-exclusion,
   10 kpc exclusion, cluster R500 interior scaling, and the LF completeness up-weight.)

PERTURBATION MODEL (per realization; every knob stated)
  1. 2M++ galaxy distances: D' = D + N(0, sigma_D), sigma_D = 350/73 = 4.79 Mpc
     (peculiar-velocity scatter ~ +-350 km/s at H0 = 73, the SPARC/Chae H0). D' clipped
     to >= 0.5 Mpc. Positions move RADIALLY (sky position is exact; only the redshift
     distance is uncertain).
  2. 2M++ stellar masses: log10 Mstar' = log10 Mstar + N(0, 0.15) dex (K-band M/L
     scatter, the conservative end of the 0.10-0.15 dex bracket) PLUS the deterministic
     luminosity-distance coupling Mstar' *= (D'/D)^2 (flux is what is observed; if the
     source is truly farther it is truly more luminous). Gas mass is RECOMPUTED from the
     perturbed Mstar via the same deterministic Chae Eqs 7/8 forms used in
     gext_estimator.load_2mpp (lines 137-141 there), so the gas fraction stays
     self-consistent.
  3. MCXC cluster masses: the L500-M500 relation carries ~0.15 dex intrinsic scatter
     (Piffaretti et al. 2011, A&A 534, A109, the MCXC source paper). Chae Eq 4 maps
     M500 -> M_MOND with slope 0.728, so log10 Mmond' = log10 Mmond + 0.728 * N(0, 0.15).
  4. MCXC cluster distances: same +-350 km/s peculiar-velocity scatter as (1)
     [OURS -- an addition beyond the task's minimum list; it is honest (cluster
     distances are also redshift distances) and only WIDENS cones].
  5. Completeness bracket TOGGLED: realizations alternate deterministically between the
     noclu analog (completeness=False) and the maxclu analog (completeness=True), 50/50.
     The x8 missing-baryon factor is a global scalar and cannot change the direction, so
     it is irrelevant here; the 1/f(D) LF up-weight DOES change the direction and is the
     part being toggled.
  NOT perturbed (stated): the SPARC test-point position/distance itself (the banked
  vectors are conditional on the SPARC D), and the 2M++ sky positions (arcsec-exact).

CONE DEFINITION (convention stated)
  central vector u0 = the banked PRIMARY (maxclu-weighting) unit vector from
  gext_vectors.csv (ux_icrs, uy_icrs, uz_icrs), ICRS Cartesian.
  Per realization k: theta_k = arccos( u_k . u0 )  in degrees.
  cone68 = 68th percentile of {theta_k}; cone90 = 90th percentile. These are
  half-angles of the cone around u0 containing 68% / 90% of realizations.

NO HARD-CODED RESULTS. Whatever the cones come out, they are written as-is.
Output: /Users/carlzimmerman/new_physics/prep_2026/aligned_firing/direction_cones.csv
        (name, cone68, cone90, robust/soft flag + extras) and a printed summary.
Exit 0 on success.
"""
import csv
import sys
import time

import numpy as np

sys.path.insert(0, '/Users/carlzimmerman/new_physics/gext_vectors_2026/src')
from gext_estimator import GextEstimator, radec_to_cart  # noqa: E402

BASE_GEXT = '/Users/carlzimmerman/new_physics/gext_vectors_2026'
RAW = BASE_GEXT + '/data/raw'
VEC_CSV = BASE_GEXT + '/data/gext_vectors.csv'
MERGED = ('/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/reviews/'
          'directional_efe_2026/laneB_merged_catalog.csv')
OUT_DIR = '/Users/carlzimmerman/new_physics/prep_2026/aligned_firing'
OUT_CSV = OUT_DIR + '/direction_cones.csv'

N_REAL = 200                      # realizations per galaxy (full sample -- fast enough)
SIGMA_D_MPC = 350.0 / 73.0        # peculiar-velocity distance scatter, Mpc
SIGMA_ML_DEX = 0.15               # 2M++ K-band M/L scatter (conservative end of 0.10-0.15)
SIGMA_LM_DEX = 0.15               # MCXC L500-M500 intrinsic scatter (Piffaretti+ 2011)
CHAE_EQ4_SLOPE = 0.728            # d log Mmond / d log M500 (Chae 2021 Eq 4)
SEED = 20260716


def load_central_vectors(path):
    rows = []
    with open(path) as fh:
        for r in csv.DictReader(fh):
            rows.append(dict(
                name=r['name'], ra=float(r['ra']), dec=float(r['dec']), D=float(r['D']),
                u0=np.array([float(r['ux_icrs']), float(r['uy_icrs']), float(r['uz_icrs'])]),
                dom_share=float(r['dom_share']), flag=r['flag']))
    return rows


def _parses_float(s):
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        return False


def load_firing_names(path):
    """Galaxies with BOTH a signed per-side asymmetry and a Chae e_N (the firing sample),
    read from the frozen merged catalog -- nothing hard-coded.

    FIX 2026-07-16 (lane W2): the old truthiness test `r.get('A_signed','').strip()`
    counted placeholder rows (A_signed == 'UNSIGNED_ONLY', e.g. Ponomareva2016 rows)
    as signed. Both fields must now PARSE AS FLOATS to qualify."""
    names = set()
    with open(path) as fh:
        for r in csv.DictReader(fh):
            if (_parses_float(r.get('A_signed', '').strip())
                    and _parses_float(r.get('log_eN_maxclu', '').strip())):
                names.add(r['galaxy'].strip())
    return names


def gas_from_mstar(Mstar):
    """Deterministic Chae Eqs 7/8 expectation -- same forms as gext_estimator.load_2mpp."""
    lgM = np.log10(np.maximum(Mstar, 1.0))
    f_early = np.clip(0.28 * lgM - 2.12, 0.0, 1.0)
    Mg_cold = 11500.0 * np.maximum(Mstar, 1.0) ** 0.54 + 0.07 * Mstar
    Mg_hot = 10.0 ** (1.47 * lgM - 5.414)
    return (1 - f_early) * Mg_cold + f_early * Mg_hot


def main():
    t_start = time.time()
    rng = np.random.default_rng(SEED)

    targets = load_central_vectors(VEC_CSV)
    firing = load_firing_names(MERGED)
    print(f"targets: {len(targets)} SPARC galaxies "
          f"({sum(1 for t in targets if t['flag'] == 'robust')} robust, "
          f"{sum(1 for t in targets if t['flag'] == 'soft')} soft); "
          f"firing-sample flags matched: "
          f"{sum(1 for t in targets if t['name'] in firing)}/{len(firing)}")

    est = GextEstimator(RAW + '/2mpp_vizier.tsv', RAW + '/mcxc.tsv', gas=True,
                        ez_sqrt=False, c115_weight=False, catalog_mode='full')
    print(f"catalog loaded: {est.n_gal} 2M++ sources, {est.n_clu} MCXC clusters")

    # ---- pristine copies + fixed unit sky directions (sky positions are exact) ----
    D0_gal = est.gal['D'].copy()
    Mstar0 = est.gal['Mstar'].copy()
    unit_gal = radec_to_cart(est.gal['ra'], est.gal['dec'])          # (n_gal, 3)
    D0_clu = est.clu['D'].copy()
    Mmond0 = est.clu['Mmond'].copy()
    unit_clu = radec_to_cart(est.clu['ra'], est.clu['dec'])

    n_t = len(targets)
    angles = np.full((n_t, N_REAL), np.nan)

    for k in range(N_REAL):
        # --- (1)+(4) distances (radial moves) ---
        Dp_gal = np.clip(D0_gal + rng.normal(0.0, SIGMA_D_MPC, est.n_gal), 0.5, None)
        Dp_clu = np.clip(D0_clu + rng.normal(0.0, SIGMA_D_MPC, est.n_clu), 0.5, None)
        # --- (2) 2M++ masses: M/L scatter + luminosity-distance coupling; gas recomputed ---
        Mstar_p = (Mstar0 * (Dp_gal / D0_gal) ** 2
                   * 10.0 ** rng.normal(0.0, SIGMA_ML_DEX, est.n_gal))
        Mgas_p = gas_from_mstar(Mstar_p)
        # --- (3) MCXC masses through Chae Eq 4 slope ---
        Mmond_p = Mmond0 * 10.0 ** (CHAE_EQ4_SLOPE
                                    * rng.normal(0.0, SIGMA_LM_DEX, est.n_clu))
        # --- install the perturbed catalog into the (reused) estimator ---
        est.gal['D'] = Dp_gal                     # feeds lf_visible_fraction + self-mask
        est.gal_mass = Mstar_p + Mgas_p
        est.gal_pos = unit_gal * Dp_gal[:, None]
        est.clu['Mmond'] = Mmond_p
        est.clu_pos = unit_clu * Dp_clu[:, None]
        # --- (5) completeness bracket toggle: exact 50/50 alternation ---
        completeness = (k % 2 == 0)

        for i, t in enumerate(targets):
            gvec, _ = est.field_at(t['ra'], t['dec'], t['D'],
                                   completeness=completeness, n_top=1)
            mag = np.linalg.norm(gvec)
            if mag <= 0:
                continue
            u = gvec / mag
            angles[i, k] = np.degrees(np.arccos(np.clip(np.dot(u, t['u0']), -1.0, 1.0)))

        if (k + 1) % 20 == 0:
            print(f"  realization {k + 1}/{N_REAL}  "
                  f"({time.time() - t_start:.0f} s elapsed)", flush=True)

    # restore pristine state (hygiene; est not used further)
    est.gal['D'] = D0_gal
    est.gal['Mstar'] = Mstar0
    est.clu['Mmond'] = Mmond0

    # ---- per-galaxy cones ----
    out_rows = []
    for i, t in enumerate(targets):
        a = angles[i]
        a = a[np.isfinite(a)]
        c68 = float(np.percentile(a, 68.0))
        c90 = float(np.percentile(a, 90.0))
        out_rows.append(dict(
            name=t['name'], flag=t['flag'], dom_share=t['dom_share'],
            firing='yes' if t['name'] in firing else 'no',
            n_real=len(a), cone68_deg=c68, cone90_deg=c90,
            median_theta_deg=float(np.median(a))))

    with open(OUT_CSV, 'w', newline='') as fh:
        cols = ['name', 'flag', 'dom_share', 'firing', 'n_real',
                'cone68_deg', 'cone90_deg', 'median_theta_deg']
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in out_rows:
            w.writerow({k: (f"{v:.4g}" if isinstance(v, float) else v)
                        for k, v in r.items()})
    print(f"\nwrote {OUT_CSV} ({len(out_rows)} rows)")

    # ---- summary (computed, not asserted) ----
    def med(key, flag):
        v = [r[key] for r in out_rows if r['flag'] == flag]
        return np.median(v), len(v)

    print("\n================ DIRECTION-CONE SUMMARY (N=%d per galaxy) ================"
          % N_REAL)
    for flag in ('robust', 'soft'):
        m68, n = med('cone68_deg', flag)
        m90, _ = med('cone90_deg', flag)
        print(f"  {flag:6s} rows (n={n:3d}): median cone68 = {m68:6.2f} deg | "
              f"median cone90 = {m90:6.2f} deg")
    soft = [r for r in out_rows if r['flag'] == 'soft']
    hard = [r for r in soft if r['cone68_deg'] < 30.0]
    print(f"\n  soft rows with cone68 < 30 deg (HARDEN to usable for the aligned "
          f"statistic): {len(hard)}/{len(soft)}")
    for thr in (10.0, 20.0, 45.0):
        print(f"    (context) soft rows with cone68 < {thr:.0f} deg: "
              f"{sum(1 for r in soft if r['cone68_deg'] < thr)}/{len(soft)}")
    fir = [r for r in out_rows if r['firing'] == 'yes']
    if fir:
        print(f"\n  firing-sample galaxies (n={len(fir)}):")
        for r in sorted(fir, key=lambda r: r['cone68_deg']):
            print(f"    {r['name']:10s} [{r['flag']:6s}] cone68 = {r['cone68_deg']:6.2f} "
                  f"deg | cone90 = {r['cone90_deg']:6.2f} deg | dom_share = "
                  f"{r['dom_share']:.3f}")
    worst = sorted(out_rows, key=lambda r: -r['cone68_deg'])[:5]
    print("\n  5 widest cones overall:")
    for r in worst:
        print(f"    {r['name']:10s} [{r['flag']:6s}] cone68 = {r['cone68_deg']:6.2f} deg")
    print(f"\ntotal runtime: {time.time() - t_start:.0f} s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
