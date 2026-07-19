#!/usr/bin/env python3
"""
predict_diagram.py -- ZERO-SNe-FITTED-PARAMETER prediction of the Pantheon+ Hubble
diagram from the GALAXY-side dark-energy density.

THE PHYSICS (stated honestly, not blurred):
  Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA framework does NOT modify the
  cosmological background. a0 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z modifies galaxy
  INERTIA, not expansion. Lambda is a genuine constant, so H(z) is STANDARD flat LCDM
  and mu(z) is the standard distance modulus. There is NO framework-native SNe formula.
  What the framework adds is a galaxy-side PREDICTION of Lambda (hence Omega_Lambda),
  which we here propagate INTO the SNe Hubble diagram and compare to the data.

WHAT THIS SCRIPT DOES:
  Galaxy a0 -> Lambda_gal = 32 pi a0^2 / c^4 -> Omega_Lambda(H0) = Lambda_gal c^2/(3H0^2)
  -> flat H(z) = H0 sqrt(Omega_m (1+z)^3 + Omega_Lambda) with Omega_Lambda FIXED BY
  GALAXIES (NOT fit to SNe) and Omega_m FIXED at the SNe/Planck value -> mu(z) with the
  overall (H0, M_B) offset analytically marginalized -> residuals + chi2/dof against the
  Pantheon+ binned Hubble diagram, and Delta-chi2 vs the best-fit flat LCDM (Omega_m fit
  freely to the SAME binned data).

  This is a ZERO-SNe-fitted-shape-parameter prediction: the ONE nuisance (vertical offset,
  = the H0/M_B degeneracy that SNe cannot break) is marginalized; the deceleration/shape
  is set entirely by galaxies (Omega_Lambda) + the shared Omega_m.

HONEST SCOPE: the galaxy model SHARES Omega_m and the offset with LCDM. It is therefore a
  test of Omega_Lambda-FROM-GALAXIES only, not of the whole diagram. And the CANONICAL
  a0=9.355e-11 footing is CIRCULAR: a0 was DEFINED as cH_Lambda/Z from a cosmological
  (Planck) Lambda, so "canonical a0 -> Lambda" is algebra run backwards, not a test. The
  genuine test is the MEASURED a0 (SPARC rotation-curve dynamics ALONE, Lambda-blind).

CREDIT: Milgrom (the a0 kernel nu=sqrt(1+1/y), 1999 PLA 253:273); Brout+2022 / Scolnic
  (Pantheon+SH0ES); Perlmutter, Riess, Schmidt (the acceleration discovery); Sarkar (the
  SNe-leg critique this cross-check is relevant to).

Data: Pantheon+SH0ES.dat (PantheonPlusSH0ES DataRelease), non-calibrator SNe with z>0.01.
Diagonal errors only -> absolute chi2 is optimistic (systematics are correlated); use the
RELATIVE (Delta-chi2 vs best-fit LCDM) comparison as the robust statement.
"""
import numpy as np, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATFILE = os.path.join(HERE, "pantheonplus_full.dat")

# ---- constants (SI) ----
C     = 2.99792458e8        # m/s
G     = 6.67430e-11
MPC   = 3.0856776e22        # m
PC    = 3.0856776e16        # m

# ---- SNe-side input (standard extraction, NOT framework-native) ----
OM_SNE   = 0.334            # Brout+2022 Pantheon+ SNe-only flat-LCDM Omega_m
OM_SNE_E = 0.018

# ---- galaxy-side a0 footings ----
# measured (Lambda-BLIND) from prep_2026/a0_line/fire_slope_results.json budget_gas
A0_GLS   = 1.1814381247770623e-10   # GLS gas-dominated slope estimator
A0_MED   = 9.725607106012755e-11    # median-estimator variant
A0_TOT   = 1.9026066078649394e-11   # total 1-sigma on the GLS a0 (16%)
# reference footings
A0_CANON = 9.354769736111044e-11    # canonical cH_Lambda/Z  -- CIRCULAR (Planck-Lambda defined)
A0_ALT   = 1.1305322040279838e-10   # alt normalization

# ---- two H0 axes (M_B-H0 degeneracy is a SEPARATE axis from Omega_Lambda) ----
H0_KMS = {"H0=67.4(Planck)": 67.4, "H0=73.0(SH0ES)": 73.0}


def lambda_from_a0(a0):
    """Lambda = 32 pi a0^2 / c^4  [1/m^2]  (Carl's a0 = c^2 sqrt(Lambda/32pi))."""
    return 32.0 * np.pi * a0**2 / C**4


def rho_de_from_a0(a0):
    """rho_DE = Lambda c^2/(8 pi G) = 4 a0^2/(G c^2)  [kg/m^3]."""
    return 4.0 * a0**2 / (G * C**2)


def omega_lambda(a0, H0_kms):
    """Omega_Lambda = Lambda c^2/(3 H0^2). Depends on H0 (the M_B-H0 axis)."""
    H0 = H0_kms * 1000.0 / MPC        # s^-1
    return lambda_from_a0(a0) * C**2 / (3.0 * H0**2)


# ---------- Pantheon+ binned Hubble diagram ----------
def load_binned(nbin=25):
    names = open(DATFILE).readline().split()
    ix = {n: i for i, n in enumerate(names)}
    rows = [l.split() for l in open(DATFILE).read().splitlines()[1:]]
    z  = np.array([float(r[ix["zHD"]]) for r in rows])
    mu = np.array([float(r[ix["MU_SH0ES"]]) for r in rows])
    e  = np.array([float(r[ix["MU_SH0ES_ERR_DIAG"]]) for r in rows])
    cal = np.array([int(r[ix["IS_CALIBRATOR"]]) for r in rows])
    sel = (cal == 0) & (z > 0.01)
    z, mu, e = z[sel], mu[sel], e[sel]
    # log-spaced bins with inverse-variance weighting
    edges = np.logspace(np.log10(z.min() * 0.999), np.log10(z.max() * 1.001), nbin + 1)
    zb, mub, eb = [], [], []
    for k in range(nbin):
        m = (z >= edges[k]) & (z < edges[k + 1])
        if m.sum() < 3:
            continue
        w = 1.0 / e[m]**2
        zbar = np.sum(w * z[m]) / np.sum(w)
        mubar = np.sum(w * mu[m]) / np.sum(w)
        emean = 1.0 / np.sqrt(np.sum(w))
        zb.append(zbar); mub.append(mubar); eb.append(emean)
    return np.array(zb), np.array(mub), np.array(eb), sel.sum()


# ---------- distance modulus (flat form, as instructed) ----------
def mu_model(zb, Om, OL, H0_kms=70.0):
    """mu(z) for flat-form H(z)=H0 sqrt(Om(1+z)^3+OL). H0 sets only the additive
    offset (absorbed by marginalization), so its value here is irrelevant."""
    H0 = H0_kms * 1000.0 / MPC
    zg = np.linspace(0, zb.max() * 1.001, 4000)
    E = np.sqrt(Om * (1 + zg)**3 + OL)
    invE = 1.0 / E
    cum = np.concatenate([[0], np.cumsum(0.5 * (invE[1:] + invE[:-1]) * np.diff(zg))])
    Dc = np.interp(zb, zg, cum)              # dimensionless comoving distance integral
    dL = (1 + zb) * (C / H0) * Dc            # metres
    return 5.0 * np.log10(dL / (10 * PC))


def chi2_offset_marginalized(data, err, model):
    """chi2 with the single vertical offset (H0/M_B nuisance) marginalized analytically."""
    w = 1.0 / err**2
    delta = np.sum(w * (data - model)) / np.sum(w)   # best offset
    r = data - model - delta
    return np.sum(w * r**2), delta, r


def bestfit_lcdm(zb, mub, eb):
    """Flat LCDM with Omega_m fit freely to the binned data (offset marginalized)."""
    grid = np.linspace(0.05, 0.60, 221)
    best = None
    for Om in grid:
        m = mu_model(zb, Om, 1 - Om)
        c2, _, _ = chi2_offset_marginalized(mub, eb, m)
        if best is None or c2 < best[1]:
            best = (Om, c2)
    return best


def main():
    zb, mub, eb, nsn = load_binned()
    nb = len(zb)
    dof_gal = nb - 1                          # 1 marginalized offset, 0 fitted shape params
    Om_bf, chi2_bf = bestfit_lcdm(zb, mub, eb)
    dof_bf = nb - 2                           # offset + Omega_m

    footings = {
        "measured_GLS(genuine)":  A0_GLS,
        "measured_median":        A0_MED,
        "canonical(CIRCULAR)":    A0_CANON,
        "alt":                    A0_ALT,
    }

    out = {
        "nsn_cosmology": int(nsn), "nbins": nb,
        "Om_SNe": OM_SNE,
        "bestfit_LCDM": {"Om": round(Om_bf, 4),
                         "chi2": round(chi2_bf, 2),
                         "chi2_per_dof": round(chi2_bf / dof_bf, 3),
                         "dof": dof_bf},
        "rho_DE_galaxy": {}, "predictions": {},
    }

    print("=" * 78)
    print("ZERO-SNe-FITTED-PARAMETER GALAXY -> Pantheon+ HUBBLE-DIAGRAM PREDICTION")
    print("=" * 78)
    print(f"Pantheon+ cosmology SNe (non-cal, z>0.01): {nsn}   binned -> {nb} points")
    print(f"Omega_m (shared, Brout+2022 SNe-only): {OM_SNE}")
    print(f"Best-fit flat LCDM (Om fit to binned data): Om={Om_bf:.4f}  "
          f"chi2={chi2_bf:.2f}  chi2/dof={chi2_bf/dof_bf:.3f}  (dof={dof_bf})")
    print("-" * 78)

    for label, a0 in footings.items():
        rho = rho_de_from_a0(a0)
        out["rho_DE_galaxy"][label] = {"a0": a0, "Lambda": lambda_from_a0(a0),
                                       "rho_DE_kg_m3": rho}
        print(f"\n[{label}]  a0={a0:.4e}  Lambda={lambda_from_a0(a0):.4e}  "
              f"rho_DE={rho:.4e} kg/m^3")
        for hlab, H0v in H0_KMS.items():
            OL = omega_lambda(a0, H0v)
            m = mu_model(zb, OM_SNE, OL)
            c2, delta, r = chi2_offset_marginalized(mub, eb, m)
            dchi2 = c2 - chi2_bf                   # vs best-fit LCDM
            # residual pattern: sign of slope of residual vs z (high-z pull)
            hi = zb > np.median(zb)
            resid_hi = float(np.mean(r[hi]))
            out["predictions"].setdefault(label, {})[hlab] = {
                "Omega_Lambda_gal": round(float(OL), 4),
                "Om_plus_OL": round(float(OM_SNE + OL), 4),
                "chi2": round(float(c2), 2),
                "chi2_per_dof": round(float(c2 / dof_gal), 3),
                "delta_chi2_vs_bestfit_LCDM": round(float(dchi2), 2),
                "mean_highz_residual_mag": round(resid_hi, 4),
            }
            print(f"   {hlab:16s} OL_gal={OL:6.3f}  Om+OL={OM_SNE+OL:5.3f}  "
                  f"chi2/dof={c2/dof_gal:6.3f}  dChi2(vs LCDM)={dchi2:+7.2f}  "
                  f"<resid_hiZ>={resid_hi:+.3f} mag")

    # reference: SNe best-fit-Om flat LCDM held at OL=1-Om (the concordance curve)
    m_conc = mu_model(zb, OM_SNE, 1 - OM_SNE)
    c2_conc, _, _ = chi2_offset_marginalized(mub, eb, m_conc)
    out["reference_flatLCDM_Om0.334"] = {"OL": round(1 - OM_SNE, 3),
                                         "chi2": round(float(c2_conc), 2),
                                         "chi2_per_dof": round(float(c2_conc / dof_gal), 3)}
    print("-" * 78)
    print(f"Reference flat-LCDM at SNe Om={OM_SNE} (OL={1-OM_SNE:.3f}): "
          f"chi2/dof={c2_conc/dof_gal:.3f}")

    with open(os.path.join(HERE, "predict_diagram_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("\nwrote predict_diagram_results.json")

    # ---- figure (optional, non-fatal) ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True,
                                       gridspec_kw={"height_ratios": [2, 1]})
        zline = np.linspace(zb.min(), zb.max(), 300)
        # data
        m_bf = mu_model(zb, Om_bf, 1 - Om_bf)
        _, off_bf, _ = chi2_offset_marginalized(mub, eb, m_bf)
        ax1.errorbar(zb, mub, yerr=eb, fmt="o", ms=4, color="k", label="Pantheon+ binned",
                     zorder=5)
        m_bfL = mu_model(zline, Om_bf, 1 - Om_bf) + off_bf
        ax1.plot(zline, m_bfL, "-", color="C0", lw=2,
                 label=f"best-fit LCDM (Om={Om_bf:.3f})")
        for label, a0, col in [("measured_GLS(genuine)", A0_GLS, "C3"),
                               ("measured_median", A0_MED, "C2")]:
            OL = omega_lambda(a0, 67.4)
            mm = mu_model(zb, OM_SNE, OL)
            _, offm, _ = chi2_offset_marginalized(mub, eb, mm)
            ax1.plot(zline, mu_model(zline, OM_SNE, OL) + offm, "--", color=col, lw=1.8,
                     label=f"{label} OL={OL:.2f} (H0=67.4)")
            ax2.plot(zb, mub - (mu_model(zb, OM_SNE, OL) + offm), "o--", color=col, ms=3)
        ax2.errorbar(zb, mub - m_bfL if False else mub - (m_bf + off_bf), yerr=eb,
                     fmt="o", ms=3, color="k")
        ax2.axhline(0, color="C0", lw=1)
        ax1.set_xscale("log"); ax2.set_xscale("log")
        ax1.set_ylabel("distance modulus mu"); ax2.set_ylabel("data - model [mag]")
        ax2.set_xlabel("redshift z"); ax1.legend(fontsize=8)
        ax1.set_title("Galaxy-predicted Omega_Lambda on the Pantheon+ Hubble diagram")
        fig.tight_layout()
        fig.savefig(os.path.join(HERE, "predict_diagram_fig.png"), dpi=110)
        print("wrote predict_diagram_fig.png")
    except Exception as e:
        print("figure skipped:", e)


if __name__ == "__main__":
    main()
