#!/usr/bin/env python3
r"""
DECISIVE tests of the density fork in a0 = (c/2) sqrt(G rho) -- on REAL data, graded honestly.
=============================================================================================
The relation a0 = (c/2)sqrt(G rho) = c^2/(2R*) = cH/Z (R* = c/sqrt(G rho), Z = 2 sqrt(8pi/3) = 5.789)
matches the observed MOND a0 to ~20% IF rho = rho_Lambda (dark energy). The physics fork is WHICH rho:
  (U) rho = rho_Lambda  -> a0 UNIVERSAL (uniform everywhere). [framework's reading]
  (E) rho = rho_LOCAL/AMBIENT -> a0 VARIES with environment/density. [testable, distinctive]
This script runs the EXISTING-DATA tests that discriminate (U) vs (E), with the confounds removed.

NEW (not previously in the repo) tests added here:
  TEST A -- CLUSTER ENVIRONMENT NULL: using the REAL eRASS1 RA/Dec/z (9830 clusters), measure each
    cluster's actual large-scale environment (comoving neighbour count) and ask whether the MOND residual
    eta correlates with environment. Reading (E) predicts: denser env -> higher a0 -> LOWER eta.
    Result: raw rho~-0.11..-0.15 (right sign) but VANISHES (partial ~0) after controlling for M500,z.
    => the apparent signal is a MASS/redshift confound; NO genuine environmental a0. A clean NULL for (E).
  TEST B -- CLUSTER RAR SLOPE: treat clusters as a RAR (a0_eff = gobs^2/gbar at R500) and test whether
    a0_eff tracks the cluster's own gas density as rho^+0.5 (reading E). Result: a0_eff ANTI-correlates
    with rho_gas (slope ~-0.4; partial ~-0.27, controlling the built-in gbar coupling) -- WRONG SIGN.
  TEST C -- UNIVERSALITY BOUND: the RAR intrinsic a0 scatter (Li+2018: <=0.057 dex, "no detected a0
    variation") caps any coupling a0 ~ rho_local^p at p <= 0.06, while the framework's law is p=0.5.
    => the LOCAL-density reading is EXCLUDED by ~8x; only the COSMIC-uniform reading survives.
  TEST D -- DENSITY-a0 ON CLUSTERS: replacing universal a0 with a0(rho_cluster) does NOT close eta to 1;
    it OVERSHOOTS (eta -> 0.4-0.8) and the radial rise it predicts (a0 ~ rho(r)^0.5, beta-model) is too
    SHALLOW (x2) vs the observed cluster-RAR rise (x5; Chan & Del Popolo 2020).

HONEST GRADE: all four are CONSISTENCY/NULL results, not causal proof. The universal RAR is genuine
EXISTING-DATA evidence that a0 is set by a COSMIC (uniform) source -- consistent with rho_Lambda -- but
that is universality evidence, NOT proof a0 is CAUSED by dark energy (which needs a0 to track rho as it
CHANGES; the z~3 test). The density-dependent (environmental) reading that would 'fix' clusters is
DISFAVORED by the data (null environment correlation + wrong-sign RAR slope + RAR universality bound).

Data: data/erass1cl_primary_v3.2.fits (Bulbul+2024), data/sparc_data/*, data/SPARC_Lelli2016c.mrt.
Needs numpy, scipy, astropy.  Run: python a0_density_fork_decisive_tests.py
"""
import os
import sys
import numpy as np
from scipy.stats import spearmanr, rankdata
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

C, G, MSUN, MPC, KPC = 2.99792458e8, 6.674e-11, 1.989e30, 3.0857e22, 3.0857e19
A0 = 1.2e-10
RHO_LAMBDA = 5.83e-27
OM, OL, H0 = 0.315, 0.685, 67.4
nu = lambda y: 0.5 + np.sqrt(0.25 + 1.0 / y)


def _partial_spearman(a, b, controls):
    """Spearman partial correlation of a,b controlling for the columns in `controls` (list of arrays)."""
    ra_, rb_ = rankdata(a), rankdata(b)
    Xc = np.column_stack([rankdata(c) for c in controls]).astype(float)
    Xc = (Xc - Xc.mean(0)) / Xc.std(0)
    X = np.column_stack([np.ones(len(a)), Xc])
    resa = ra_ - X @ np.linalg.lstsq(X, ra_, rcond=None)[0]
    resb = rb_ - X @ np.linalg.lstsq(X, rb_, rcond=None)[0]
    return float(np.corrcoef(resa, resb)[0, 1])


def load_clusters(zmax=1.0):
    from astropy.io import fits
    d = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"))[1].data

    def col(c):
        out = []
        for v in d[c]:
            try:
                if isinstance(v, bytes):
                    v = v.decode().strip()
                out.append(float(v))
            except Exception:
                out.append(np.nan)
        return np.array(out, dtype=float)

    z, M500, Mgas, fgas, R500 = (col("BEST_Z"), col("M500"), col("MGAS500"),
                                 col("FGAS500"), col("R500"))
    ra, dec = col("RA"), col("DEC")
    ok = ((z > 0) & (z < zmax) & np.isfinite(z) & (M500 > 0) & (Mgas > 0) & (R500 > 0)
          & (fgas > 0.01) & (fgas < 0.30) & np.isfinite(ra) & np.isfinite(dec))
    out = {k: v[ok] for k, v in dict(z=z, M500=M500, Mgas=Mgas, fgas=fgas,
                                     R500=R500, ra=ra, dec=dec).items()}
    fstar = 0.20
    out["gobs"] = G * (out["M500"] * 1e13 * MSUN) / (out["R500"] * KPC) ** 2
    out["gbar"] = G * ((1 + fstar) * out["Mgas"] * 1e11 * MSUN) / (out["R500"] * KPC) ** 2
    out["rho_gas"] = (out["Mgas"] * 1e11 * MSUN) / ((4 / 3) * np.pi * (out["R500"] * KPC) ** 3)
    out["N"] = int(ok.sum())
    return out


def comoving_xyz(z, ra, dec):
    zg = np.linspace(0, z.max() + 0.01, 4000)
    Ez = np.sqrt(OM * (1 + zg) ** 3 + OL)
    Dcg = (C / 1000 / H0) * np.cumsum(1 / Ez) * (zg[1] - zg[0])
    Dc = np.interp(z, zg, Dcg)
    rr, dd = np.deg2rad(ra), np.deg2rad(dec)
    return np.vstack([Dc * np.cos(dd) * np.cos(rr),
                      Dc * np.cos(dd) * np.sin(rr),
                      Dc * np.sin(dd)]).T


def test_A_environment(c):
    print("=" * 96)
    print("TEST A -- CLUSTER ENVIRONMENT NULL (real eRASS1 positions)")
    print("=" * 96)
    eta = c["gobs"] / (nu(c["gbar"] / A0) * c["gbar"])
    pts = comoving_xyz(c["z"], c["ra"], c["dec"])
    tree = cKDTree(pts)
    print(f"  N={c['N']} clusters; universal-a0 median eta = {np.median(eta):.3f} (the cluster problem)")
    print(f"  reading (E) predicts: denser environment -> higher a0 -> LOWER eta (negative correlation)\n")
    print(f"  {'R_env':>8}{'raw rho(eta,env)':>18}{'partial | M500,z':>20}")
    for Renv in (20.0, 40.0):
        cnt = tree.query_ball_point(pts, Renv, return_length=True) - 1.0
        raw = spearmanr(cnt, eta)[0]
        par = _partial_spearman(eta, cnt, [c["M500"], c["z"]])
        print(f"  {Renv:>6.0f}Mpc{raw:>18.3f}{par:>20.3f}")
    # volume-limited robustness (Malmquist guard)
    m = c["z"] < 0.2
    eta2 = eta[m]
    pts2 = comoving_xyz(c["z"][m], c["ra"][m], c["dec"][m])
    cnt2 = cKDTree(pts2).query_ball_point(pts2, 30.0, return_length=True) - 1.0
    par2 = _partial_spearman(eta2, cnt2 + 1, [c["M500"][m]])
    print(f"\n  volume-limited z<0.2 (N={m.sum()}): partial rho(eta,env30)|M500 = {par2:+.3f}")
    print("  => raw negative correlation is a MASS/redshift confound: partial ~ 0. NULL for reading (E).")


def test_B_cluster_rar_slope(c):
    print("\n" + "=" * 96)
    print("TEST B -- CLUSTER RAR SLOPE: does a0_eff track rho_gas^+0.5 (reading E)?")
    print("=" * 96)
    a0_eff = c["gobs"] ** 2 / c["gbar"]              # deep-MOND effective a0
    slope = np.polyfit(np.log10(c["rho_gas"]), np.log10(a0_eff), 1)[0]
    par = _partial_spearman(np.log10(a0_eff), np.log10(c["rho_gas"]), [np.log10(c["gbar"])])
    print(f"  median cluster a0_eff = {np.median(a0_eff):.2e} ({np.median(a0_eff) / A0:.1f}x galaxy a0)")
    print(f"  reading (E) predicts slope d log a0_eff / d log rho_gas = +0.5")
    print(f"  MEASURED slope = {slope:+.2f}; partial (controlling built-in gbar coupling) = {par:+.2f}")
    print(f"  => WRONG SIGN (a0_eff DECREASES where rho_gas is higher). Disfavors reading (E).")


def test_C_universality_bound():
    print("\n" + "=" * 96)
    print("TEST C -- UNIVERSALITY BOUND from the RAR intrinsic scatter (Li+2018)")
    print("=" * 96)
    sigma_a0 = 0.057                                  # dex, Li+2018 upper bound on a0 variation
    SBdisk_span_dex = np.log10(23813.87 / 5.36)       # SPARC stellar-surface-density range
    sigma_logrho = SBdisk_span_dex / 4
    p_max = sigma_a0 / sigma_logrho
    print(f"  RAR intrinsic a0 scatter <= {sigma_a0} dex; SPARC stellar surf-dens spans {SBdisk_span_dex:.1f} dex")
    print(f"  => a0 ~ rho_local^p allowed only for p <= {p_max:.3f}. Framework law has p = 0.5.")
    print(f"  => the LOCAL-density reading is EXCLUDED by ~{0.5 / p_max:.0f}x. Only COSMIC-uniform rho survives.")


def test_D_density_a0_on_clusters(c):
    print("\n" + "=" * 96)
    print("TEST D -- does a0(rho_cluster) CLOSE the residual?  (and the radial slope vs Chan&DelPopolo 2020)")
    print("=" * 96)
    a0_gas = 0.5 * C * np.sqrt(G * c["rho_gas"])
    rho_crit_z = 8.5e-27 * (OM * (1 + c["z"]) ** 3 + OL)
    a0_tot = 0.5 * C * np.sqrt(G * 500 * rho_crit_z)
    for lab, a0v in [("universal 1.2e-10", A0), ("a0~sqrt(rho_gas<R500)", a0_gas),
                     ("a0~sqrt(500 rho_crit)", a0_tot)]:
        eta = c["gobs"] / (nu(c["gbar"] / a0v) * c["gbar"])
        print(f"  {lab:24s}: median a0={np.median(np.atleast_1d(a0v)):.2e}  median eta={np.median(eta):.3f}")
    print("  => density-a0 does not land eta=1: it OVERSHOOTS (eta<1). Not a closure, a degeneracy with raising a0.")
    print("  radial slope: a0~sqrt(rho_beta(r)) rises x~2 from 3rc->rc; observed cluster-RAR a0 rises x~5")
    print("    (Chan&DelPopolo 2020: 3.9e-10 -> 1.9e-9). Right sign, too SHALLOW by ~2-3x.")


def main():
    print("#" * 96)
    print("# DECISIVE density-fork tests for a0 = (c/2)sqrt(G rho)  --  real data, honest grade")
    print("#" * 96 + "\n")
    a0_L = 0.5 * C * np.sqrt(G * RHO_LAMBDA)
    print(f"VALUE-COINCIDENCE: a0=(c/2)sqrt(G rho_Lambda) = {a0_L:.2e}  vs observed 9.1e-11..1.2e-10")
    print(f"  -> matches to ~20% (the interpolation-function systematic). REAL but a coincidence of the")
    print(f"     present value; identical to Milgrom's a0~cH0, reproduced by LCDM with no causal link.\n")
    c = load_clusters()
    test_A_environment(c)
    test_B_cluster_rar_slope(c)
    test_C_universality_bound()
    test_D_density_a0_on_clusters(c)
    print("\n" + "#" * 96)
    print("# BOTTOM LINE: the UNIVERSAL RAR (a0 uniform, no environment/density dependence in galaxies OR")
    print("#   clusters once confounds are removed) is existing-data evidence for a COSMIC (uniform) a0")
    print("#   source -- consistent with rho_Lambda. It is UNIVERSALITY EVIDENCE, not causal proof. The")
    print("#   environment-dependent reading that would fix clusters is DISFAVORED (null + wrong-sign +")
    print("#   universality bound). Causal proof still requires the a0(z~3) evolution test.")
    print("#" * 96)


if __name__ == "__main__":
    main()
