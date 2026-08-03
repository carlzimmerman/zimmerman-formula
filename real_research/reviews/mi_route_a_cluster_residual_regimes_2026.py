#!/usr/bin/env python3
r"""LANE 3 -- HOW BIG IS THE ROUTE A CLUSTER RESIDUAL REALLY, AND IS THERE ANY REGIME WHERE IT CLOSES?

WHAT THIS FILE ADDS to the committed cluster standing.  `mi_route_a_cluster_eta_2026.py` (16/16) re-solved
eta(R500) under Route A and priced the kernel switch.  It did NOT do four things, and this file does them:

  (a) a FULL error budget on the residual -- statistical, the systematic floor over its whole range, the
      footing fork, the stellar budget, and two field-theory corrections nobody had costed;
  (b) a REGIME SCAN -- mass, redshift, temperature, morphology and RADIUS -- asking where, if anywhere, Route
      A's clusters are consistent;
  (c) the residual expressed as a REQUIREMENT (baryons / mass calibration / a0), and -- the part that matters
      most for standing -- the SHARED-vs-DISTINCTIVE decomposition against standard MOND on the SAME clusters;
  (d) whether Route A's AQUAL field theory changes the cluster number beyond the kernel VALUE.  Clusters are
      nearly spherical and AQUAL is exactly algebraic when they are exactly spherical, so "nearly" is
      QUANTIFIED here rather than assumed: an exact homoeoidal-spheroid calculation, plus the external field
      effect.  This section was set up expecting the EFE to dominate, and its own arithmetic withdrew that:
      the EFE is first-order along ONE line of sight but CANCELS at first order in the sphere-averaged
      enclosed mass eta is actually built from, leaving a dipole PREDICTION rather than a bias.

  ANCHOR (data + sample, single source of truth):  real_research/reviews/clusters_eta_audit.py
  KERNEL (single source of truth for Route A):     real_research/reviews/mi_route_a_kernel.py
  Neither is modified.  The anchor's loader is exec'd up to its first banner, exactly as the committed Route A
  cluster re-solve does, so the sample is identical by construction (checked: N and median eta must match).

*** THE HEADLINE, AND IT CUTS BOTH WAYS. ***
  FAVOURABLE, and it is the single most useful number in this file: on the SAME 9830 clusters, standard MOND
  (a0 = 1.20e-10, the SAME exponential kernel -- Route A's nu IS McGaugh+2016's RAR function) leaves
  +0.3236 dex of missing mass.  Route A on the canonical footing leaves +0.3728 dex.  So 87% of the cluster
  residual is MOND's forty-year-old shared problem and 13% (0.0492 dex measured, a factor 1.120; the deep-limit
  expectation sqrt(1.2e-10/a0) = 1.132) is the framework's distinctive coefficient.  The distinctive part is
  HALF the tight end of the systematic floor and a SIXTH of the loose end -- i.e. below the resolution at which
  the front can be measured at all.
  UNFAVOURABLE, and it is what the R500-only framing hides: the residual is a PROFILE, not a number.  A
  standard NFW+beta cluster model anchored on this sample's own median M500, R500 and f_bar puts eta at
  1.49-1.78 at R200, 2.26 at R500, 3.2-4.2 at 0.5 R500 and 4.7-9.4 at 0.2 R500.  eta crosses 1 only at
  2.2-3.4 R500 -- outside every measured mass, at or beyond the splashback radius.  There is NO regime inside
  the data where Route A's clusters are consistent: the deficit is flat to ~10% across a factor 317 in mass,
  flat to 9% in temperature, rises 19% with redshift, and its one strong apparent trend (surface-brightness
  concentration) tracks the measured gas fraction, i.e. it is a gas-mass axis, not a dynamical-state one.

BOTH a0 FOOTINGS on every dimensional number:  canonical A0_CANON = 9.3614e-11 (rho_DE, c H_Lambda / Z,
kappa = 1/2); alternative A0_ALT = 1.13e-10 (rho_total, c H_0 / Z).  a0 is an INPUT.  The two places an a0
multiplier or a mass multiplier is solved for are REQUIREMENT calculations, labelled as such, adopted nowhere.

Data: eRASS1 primary cluster catalogue v3.2 (Bulbul et al. 2024), N = 9830 after the anchor's cuts.
Every check below is a falsifiable comparison or a validation against an independent closed form.  Four of them
(C4, C7, C15b, C17) run AGAINST the framework's interest, C5b WITHDRAWS this file's own starting expectation,
and C20 refuses a favourable-looking result as unmeasurable.  Non-zero exit on any failure.
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
from astropy.io import fits
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import spearmanr

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))

from mi_route_a_kernel import (  # noqa: E402  -- the ONE definition of Route A's kernel
    A0_ALT,
    A0_CANON,
    A0_M20,
    mu,
    nu,
    nu_alpha2,
    nu_minus1,
)

# ---------------------------------------------------------------------------------------------------------
# the anchor's loader, verbatim
# ---------------------------------------------------------------------------------------------------------
ANCHOR = REPO / "real_research/reviews/clusters_eta_audit.py"
_src = ANCHOR.read_text()
_G = {"__name__": "anchor"}
exec(compile(_src[: _src.index("# ====")], str(ANCHOR), "exec"), _G)  # noqa: S102
load = _G["load"]
FITSPATH = _G["FITS"]

G_N, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
A0_MOND = 1.20e-10                    # McGaugh+2016 galaxy g_dagger -- "standard MOND" comparator
F_COSMIC = 0.0493 / 0.315             # Planck Omega_b/Omega_m = 0.1565: the cosmic baryon fraction
FLOORS = (0.10, 0.15, 0.20, 0.30)     # this corpus's OWN floor range (cluster_rar_throttle_2026/lane2_data.py)
FOOTINGS = (("canonical rho_DE (cH_L/Z)", A0_CANON), ("alt rho_total (cH_0/Z)", A0_ALT))

# committed standing this file builds on (mi_route_a_cluster_eta_2026.py)
COMMITTED = dict(med=2.153, gm=2.359, dex=0.3728, med_a2=2.364, gm_a2=2.359, ladder_lo=3.88, ladder_hi=23.50)
G_DDAG = 2.02e-9                      # Tian+2020 ApJ 896 70, 20 CLASH clusters, 100-600 kpc, slope fixed 1/2
LADDER = (("lensing 100-600 kpc, 20 CLASH (Tian+2020)", 2.02e-9),
          ("dynamics, 29 HIFLUGCS lo (Tian+2021)", 0.8e-9),
          ("dynamics, 29 HIFLUGCS hi (Tian+2021)", 2.2e-9),
          ("54 BCG stellar MVDR (Tian+2024)", 1.7e-9),
          ("X-ray HSE pooled, 52 NCC (Chan&DelPopolo 2020)", 9.5e-10),
          ("X-ray HSE at r_c (Chan&DelPopolo 2020)", 1.9e-9),
          ("X-ray HSE at 3 r_c (Chan&DelPopolo 2020)", 3.9e-10))

_FAILS: list[str] = []
_RUN: list[str] = []


def chk(label, condition, detail=""):
    ok = bool(condition)
    _RUN.append(label)
    print("   [%s] %s%s" % ("OK" if ok else "FAIL", label, ("  -- " + detail) if detail else ""))
    if not ok:
        _FAILS.append(label)
    return ok


# ---------------------------------------------------------------------------------------------------------
def eta_of(b, a0, kern=nu):
    """eta = M_dyn/M_pred = g_obs / (nu(y) g_bar)."""
    return b["gobs"] / (kern(b["gbar"] / a0) * b["gbar"])


def stats(e):
    le = np.log10(e)
    return dict(med=float(np.median(e)), gm=float(10 ** le.mean()), dex=float(le.mean()),
                sd=float(le.std()), se=float(le.std() / np.sqrt(le.size)), N=le.size)


# ---------------------------------------------------------------------------------------------------------
# spheroidal (homoeoidal) Newtonian field.  rho = rho0 * shape(m),  m^2 = R^2 + z^2/q^2,  lengths in R500.
# Returned in units of (2 pi G rho0 R500): g_R, g_z.  Exterior homoeoidal shells contribute nothing, so no
# truncation radius enters -- the tau-integrand only samples m <= m(point).
# ---------------------------------------------------------------------------------------------------------
BETA_GAS, RC_GAS = 0.65, 0.15          # beta-model gas: rho ~ (1 + (m/rc)^2)^(-3 beta/2), rc in R500 units


def shape_gas(m):
    return (1.0 + (np.asarray(m, float) / RC_GAS) ** 2) ** (-1.5 * BETA_GAS)


def g_spheroid(Rr, zz, q, shape=shape_gas):
    def m2(t):
        return Rr * Rr / (1.0 + t) + zz * zz / (q * q + t)
    iR = quad(lambda t: shape(np.sqrt(m2(t))) / ((1 + t) ** 2 * np.sqrt(t + q * q)), 0, np.inf, limit=400)[0]
    iz = quad(lambda t: shape(np.sqrt(m2(t))) / ((1 + t) * (t + q * q) ** 1.5), 0, np.inf, limit=400)[0]
    return -q * Rr * iR, -q * zz * iz


def m_sphere(r, q, shape=shape_gas, n=64):
    """mass inside the SPHERE of radius r, in units of rho0 R500^3 (2-D Gauss-Legendre)."""
    xg, wg = np.polynomial.legendre.leggauss(n)
    ct, wc = 0.5 * (xg + 1), 0.5 * wg
    rg, wr = np.polynomial.legendre.leggauss(n)
    rr, wrr = 0.5 * r * (rg + 1), 0.5 * r * wr
    tot = 0.0
    for rv, wv in zip(rr, wrr):
        m = np.sqrt((rv * np.sqrt(1 - ct ** 2)) ** 2 + (rv * ct) ** 2 / q ** 2)
        tot += wv * rv * rv * float(np.sum(wc * shape(m)))
    return 4.0 * np.pi * tot


def sphere_nodes(n=48):
    xg, wg = np.polynomial.legendre.leggauss(n)
    return 0.5 * (xg + 1), 0.5 * wg           # cos(theta) in [0,1] with weights summing to 1 (N-S symmetry)


def flux_masses(q, r, a0, mbar_si, r500_si, shape=shape_gas, n=48):
    """Gauss-flux masses on the sphere of radius r (in R500 units) for a spheroidal baryon distribution
    normalised so that the mass inside that sphere is mbar_si.

    Returns (M_newt, M_kernel, M_alg, rms_dev, tilt_max) where
      M_newt   = (1/4 pi G) closed-surface integral of g_N . n     -- must equal mbar_si (Newton's theorem)
      M_kernel = (1/4 pi G) closed-surface integral of nu(|g_N|/a0) g_N . n
                 = the enclosed mass a spherical Gauss reading of the ALGEBRAIC field returns, and (exactly,
                   see section 4) the QUMOND enclosed mass
      M_alg    = the spherical algebraic answer nu(g_sph/a0) g_sph r^2/G built from the same enclosed mass
      aqual    = the AQUAL Gauss identity residual: surface integral of mu(x)x a0 cos(psi) / (4 pi G mbar) - 1
    """
    mu_unit = m_sphere(r, q, shape)                       # units rho0 R500^3
    rho0 = mbar_si / (mu_unit * r500_si ** 3)
    K = 2.0 * np.pi * G_N * rho0 * r500_si                # the g unit
    ct, wc = sphere_nodes(n)
    fn = fk = fa = 0.0
    devs, tilts = [], []
    for c, w in zip(ct, wc):
        st = np.sqrt(1.0 - c * c)
        gR, gz = g_spheroid(r * st, r * c, q, shape)
        gR, gz = gR * K, gz * K
        gn = -(gR * st + gz * c)                          # inward-positive normal component
        gm = float(np.hypot(gR, gz))
        fn += w * gn
        fk += w * float(nu(gm / a0)) * gn
        xa = float(nu(gm / a0)) * gm / a0                 # x of the algebraic field (parallel to g_N)
        fa += w * float(mu(xa)) * xa * a0 * (gn / gm)     # mu(x) x a0 cos(psi)
        devs.append(gn)
        tilts.append(np.sqrt(max(gm * gm - gn * gn, 0.0)) / gn)
    rr = r * r500_si
    M_newt = fn * rr ** 2 / G_N
    M_kern = fk * rr ** 2 / G_N
    g_sph = G_N * mbar_si / rr ** 2
    M_alg = float(nu(g_sph / a0)) * g_sph * rr ** 2 / G_N
    devs = np.array(devs)
    return (M_newt, M_kern, M_alg, float(np.std(devs) / np.mean(devs)), float(max(tilts)),
            fa * rr ** 2 / G_N / mbar_si - 1.0)


# ---------------------------------------------------------------------------------------------------------
# radial cluster model:  NFW total mass + beta-model gas, both anchored on the sample's own medians
# ---------------------------------------------------------------------------------------------------------
def m_nfw(x):
    return np.log1p(x) - x / (1.0 + x)


def gas_shape_int(x, beta, rc):
    return quad(lambda s: (1.0 + (s / rc) ** 2) ** (-1.5 * beta) * s * s, 0.0, float(x), limit=200)[0]


def profile_eta(x, a0, c500, beta, rc, m500, r500, fbar, norm):
    r = x * r500
    md = m500 * m_nfw(c500 * x) / m_nfw(c500)
    mb = fbar * m500 * gas_shape_int(x, beta, rc) / norm
    go, gb = G_N * md / r ** 2, G_N * mb / r ** 2
    return go / (float(nu(gb / a0)) * gb), go, gb, mb / md


# =========================================================================================================
def main():
    W = 108
    print("=" * W)
    print("LANE 3 -- THE ROUTE A CLUSTER RESIDUAL: HONEST SIZE, WHERE IT CLOSES, WHAT IT WOULD TAKE")
    print("  canonical a0 = %.4e   alt a0 = %.4e (%.4fx)   Milgrom-2020 1/2pi comparator = %.4e"
          % (A0_CANON, A0_ALT, A0_ALT / A0_CANON, A0_M20))
    print("  kernel: nu(y) = 1/(1 - e^-sqrt(y)) -- ADOPTED Route A, imported, never redefined here.")
    print("=" * W)

    try:
        base = load(fstar=0.20)
    except Exception as exc:                                                        # pragma: no cover
        print("\nFATAL: cannot read the eRASS1 catalogue via the anchor loader: %r" % exc)
        print("No cluster number can be quoted without it.  NOT fabricating output.")
        sys.exit(2)

    S = {lab: stats(eta_of(base, a0)) for lab, a0 in FOOTINGS}
    can, alt = FOOTINGS[0][0], FOOTINGS[1][0]
    print("\nSample (anchor's cuts: 0<z<1, M500>0, Mgas>0, 0.01<fgas<0.30, fstar=0.20): N = %d" % base["N"])
    print("  canonical: eta median %.4f  geomean %.4f  mean log %+.5f dex  scatter %.5f  SE %.6f"
          % (S[can]["med"], S[can]["gm"], S[can]["dex"], S[can]["sd"], S[can]["se"]))
    print("  alt      : eta median %.4f  geomean %.4f  mean log %+.5f dex  scatter %.5f  SE %.6f"
          % (S[alt]["med"], S[alt]["gm"], S[alt]["dex"], S[alt]["sd"], S[alt]["se"]))

    # ----------------------------------------------------------------- 1. (a) FULL ERROR BUDGET
    print("\n" + "-" * W)
    print("1. (a) THE HONEST RESIDUAL WITH A FULL ERROR BUDGET  -- one number, one interval, no cherry-picking")
    print("-" * W)
    fst = {}
    for fs in (0.0, 0.10, 0.20, 0.30, 0.50):
        b = base if abs(fs - 0.20) < 1e-12 else load(fstar=fs)
        fst[fs] = {lab: stats(eta_of(b, a0)) for lab, a0 in FOOTINGS}
    print("  stellar-budget row (fstar = M_star/M_gas), mean log10 eta in dex:")
    print("    %-10s %14s %14s" % ("fstar", "canonical", "alt"))
    for fs in sorted(fst):
        print("    %-10.2f %14.5f %14.5f" % (fs, fst[fs][can]["dex"], fst[fs][alt]["dex"]))
    d_fstar_hi = fst[0.0][can]["dex"] - fst[0.20][can]["dex"]
    d_fstar_lo = fst[0.50][can]["dex"] - fst[0.20][can]["dex"]

    # the two field-theory corrections, computed in sections 4 below; done here so the budget is one table
    r500_med = float(np.median(np.sqrt(G_N * base["M500"] * 1e13 * MSUN / base["gobs"])))
    m500_med = float(np.median(base["M500"])) * 1e13 * MSUN
    fbar_med = float(np.median(base["gbar"] / base["gobs"]))
    mbar_med = fbar_med * m500_med
    asph = {q: flux_masses(q, 1.0, A0_CANON, mbar_med, r500_med) for q in (1.0, 0.7, 0.6, 0.5, 1.0 / 0.7)}
    d_asph = -np.log10(asph[0.6][1] / asph[0.6][2])       # eta correction = -log10(M_kern/M_alg)

    y_med = float(np.median(base["gbar"] / A0_CANON))
    T_HUB = 1.0 / 2.184e-18
    _xg, _wg = np.polynomial.legendre.leggauss(96)        # cos(angle to g_ext) over the FULL [-1,1]
    CT_E, WC_E = _xg, _wg / 2.0                           # weights sum to 1

    def efe_boosts(y_i, y_e):
        """QUMOND/AQUAL uniform-external-field boost: aligned, anti-aligned, and sphere-averaged."""
        def radial(c):
            yt = np.sqrt(y_i ** 2 + y_e ** 2 + 2 * y_i * y_e * c)
            return float(nu(yt)) * (y_i + y_e * c) - float(nu(y_e)) * y_e * c
        avg = float(np.sum(WC_E * np.array([radial(c) for c in CT_E])))
        return radial(1.0) / y_i, radial(-1.0) / y_i, avg / y_i

    efe = {}
    for vpec in (300e3, 600e3):
        a_ext = vpec / T_HUB                              # actual external acceleration
        x_e = a_ext / A0_CANON
        y_e = float(mu(x_e)) * x_e                        # the NEWTONIAN external field that produces it
        b_al, b_anti, b_avg = efe_boosts(y_med, y_e)
        efe[vpec] = (a_ext, x_e, y_e, b_al, np.log10(float(nu(y_med)) / b_al), b_anti, b_avg,
                     np.log10(float(nu(y_med)) / b_avg))
    d_efe = (efe[300e3][4], efe[600e3][4])                # ALIGNED, i.e. one line of sight
    d_efe_avg = (efe[300e3][7], efe[600e3][7])            # SPHERE-AVERAGED, i.e. the enclosed-mass measure

    print("\n  ERROR BUDGET on mean log10 eta(R500), canonical footing.  Signs are as they act on the RESIDUAL.")
    print("    central value                                   %+.4f dex   (eta = %.3f geomean, %.3f median)"
          % (S[can]["dex"], S[can]["gm"], S[can]["med"]))
    print("    statistical (SE of the mean, N = %d)          +/-%.4f dex   <-- NEVER the number to quote"
          % (S[can]["N"], S[can]["se"]))
    print("    ABSOLUTE MASS-SCALE FLOOR (this corpus's own)   +/-%.2f to %.2f dex   <-- DOMINANT, carried WHOLE"
          % (FLOORS[0], FLOORS[-1]))
    print("    stellar budget fstar 0.20 -> 0.00 / 0.50        %+.4f / %+.4f dex" % (d_fstar_hi, d_fstar_lo))
    print("    a0 footing canonical -> alt (a THEORY fork)     %+.4f dex" % (S[alt]["dex"] - S[can]["dex"]))
    print("    field theory: asphericity at q = 0.6            %+.4f dex   (unfavourable, section 5)" % d_asph)
    print("    field theory: EFE, sphere-averaged mass         %+.1e to %+.1e dex   (CANCELS at first order,"
          % d_efe_avg)
    print("                                                                    section 5)")
    print("    field theory: EFE along one line of sight       %+.4f to %+.4f dex   (a signed DIPOLE, not a"
          % d_efe)
    print("                                                                    bias; section 5)")
    print("    kernel family: max relief ANY kernel can give   -%.4f dex   (a BOUND, not an error; committed)"
          % np.log10(1.245))
    print("\n  THE ONE STATEMENT:  eta(R500) = %.2f (geomean) / %.2f (median) on the canonical footing,"
          % (S[can]["gm"], S[can]["med"]))
    print("  %.2f / %.2f on the alt footing.  As a log residual, %+.3f dex canonical / %+.3f alt, with a"
          % (S[alt]["gm"], S[alt]["med"], S[can]["dex"], S[alt]["dex"]))
    print("  SYSTEMATIC uncertainty of 0.10-0.30 dex that dwarfs everything else in the table:")
    print("    %-30s %s" % ("floor", "  ".join("%.2f dex" % f for f in FLOORS)))
    for lab, _ in FOOTINGS:
        print("    %-30s %s" % (lab, "  ".join("%7.2f s" % (S[lab]["dex"] / f) for f in FLOORS)))
    print("  So the honest interval on the significance is %.2f-%.2f sigma canonical, %.2f-%.2f alt."
          % (S[can]["dex"] / FLOORS[-1], S[can]["dex"] / FLOORS[0],
             S[alt]["dex"] / FLOORS[-1], S[alt]["dex"] / FLOORS[0]))
    print("  Quoting either end alone is the manufactured answer.  The median-based residual is %+.4f dex,"
          % np.log10(S[can]["med"]))
    print("  %.0f%% lower than the mean-log one, which is a further honest %.2f-%.2f sigma reading."
          % (100 * (1 - np.log10(S[can]["med"]) / S[can]["dex"]),
             np.log10(S[can]["med"]) / FLOORS[-1], np.log10(S[can]["med"]) / FLOORS[0]))
    print("  *** AND THE R500-ONLY FRAMING UNDERSTATES IT: section 3 shows the residual grows by a further ***")
    print("  *** 0.2-0.6 dex inward of R500, which is a tension at BOTH ends of the floor range.         ***")

    # ----------------------------------------------------------------- 2. (b) REGIME SCANS ON DATA
    print("\n" + "-" * W)
    print("2. (b) IS THERE A REGIME WHERE IT CLOSES?  PART 1 -- mass, redshift, temperature, morphology")
    print("-" * W)
    d = fits.open(FITSPATH)[1].data
    col = (lambda c: np.array([float(v) if str(v).strip() not in ("", "--") else np.nan for v in d[c]], float))
    z_a, M_a, Mg_a, fg_a, R_a = col("BEST_Z"), col("M500"), col("MGAS500"), col("FGAS500"), col("R500")
    F3_a, F5_a = col("F300kpc"), col("F500")
    okm = ((z_a > 0) & (z_a < 1) & np.isfinite(z_a) & (M_a > 0) & (Mg_a > 0) & (R_a > 0)
           & (fg_a > 0.01) & (fg_a < 0.30))
    csb = (F3_a / F5_a)[okm]
    R500_kpc = R_a[okm]
    e_can = eta_of(base, A0_CANON)
    fbar = base["gbar"] / base["gobs"]
    M, zz, KT = base["M500"], base["z"], base["KT"]

    def bin_table(tag, key, mask, nb=10, fmt="%8.3f"):
        ed = np.percentile(key[mask], np.linspace(0, 100, nb + 1))
        rows = []
        print("  %-26s %6s %10s %10s %9s %9s" % (tag, "N", "eta_med", "eta_gm", "f_bar", "z_med"))
        for i in range(nb):
            m = mask & (key >= ed[i]) & ((key < ed[i + 1]) if i < nb - 1 else (key <= ed[i + 1]))
            if m.sum() < 20:
                continue
            s = stats(e_can[m])
            rows.append((ed[i], ed[i + 1], int(m.sum()), s["med"], s["gm"], float(np.median(fbar[m])),
                         float(np.median(zz[m]))))
            print(("  " + fmt + " - " + fmt + " %6d %10.3f %10.3f %9.4f %9.3f")
                  % (ed[i], ed[i + 1], m.sum(), s["med"], s["gm"], np.median(fbar[m]), np.median(zz[m])))
        return rows

    allm = np.ones(base["N"], bool)
    print("\n  MASS (M500 in 1e13 Msun; the sample spans %.2f to %.1f = a factor %.0f):"
          % (M.min(), M.max(), M.max() / M.min()))
    rows_M = bin_table("M500 decile", M, allm)
    med_M = np.array([r[3] for r in rows_M])
    print("    -> eta spans %.3f to %.3f across a factor-%.0f mass range: a %.1f%% max-min spread, and the"
          % (med_M.min(), med_M.max(), M.max() / M.min(), 100 * (med_M.max() / med_M.min() - 1)))
    print("       LOWEST-mass decile is the WORST (%.3f), because its measured f_bar is the lowest (%.4f)."
          % (rows_M[0][3], rows_M[0][5]))
    print("       No group-scale escape: the deficit is essentially FLAT in mass.  The reason is the deep-limit")
    print("       scaling eta ~ sqrt(g_obs/(a0 f_bar)): g_obs(R500) ~ M500^(1/3) E(z)^(4/3) rises with mass and")
    print("       f_bar rises with mass, and the two cancel to ~10%.")
    print("       CAVEAT ON THE LOW-MASS END, stated because it cuts against the sharpest reading of this row:")
    print("       the bottom decile's f_bar = %.4f is very low even for groups, and eRASS1's MGAS500 there comes"
          % rows_M[0][5])
    print("       from few counts.  If those gas masses are underestimated the low-mass eta falls, so 'groups")
    print("       are the worst' is the weaker claim; 'groups are no better' is the robust one.")

    print("\n  REDSHIFT:")
    rows_z = bin_table("z decile", zz, allm, fmt="%8.3f")
    med_z = np.array([r[3] for r in rows_z])
    print("    -> eta RISES with z, %.3f (lowest decile) to %.3f (highest): +%.1f%%.  Part is the E(z) growth of"
          % (med_z[0], med_z[-1], 100 * (med_z[-1] / med_z[0] - 1)))
    print("       g_obs at fixed mass, part is Malmquist (M_med rises with z in this catalogue).  The BEST")
    print("       redshift bin still sits at eta = %.3f, i.e. %+.3f dex -- no closure at low z either."
          % (med_z.min(), np.log10(med_z.min())))

    kt_ok = np.isfinite(KT) & (KT > 0)
    print("\n  TEMPERATURE (KT available for %.0f%% of the sample):" % (100 * kt_ok.mean()))
    rows_T = bin_table("KT decile [keV]", KT, kt_ok, nb=5, fmt="%8.2f")
    med_T = np.array([r[3] for r in rows_T])
    print("    -> flat to %.1f%% over %.1f-%.1f keV.  No temperature regime closes it."
          % (100 * (med_T.max() / med_T.min() - 1), rows_T[0][0], rows_T[-1][1]))

    print("\n  MORPHOLOGY / DYNAMICAL STATE.  eRASS1 carries no relaxation flag, so the only available proxy is")
    print("  the surface-brightness concentration c_SB = F(<300 kpc)/F(<R500).  It is CONFOUNDED: for clusters")
    print("  with R500 near 300 kpc it saturates at 1 by construction, so it is partly a SIZE proxy.  The scan")
    print("  below therefore restricts to R500 > 800 kpc and splits INSIDE narrow mass bands.")
    csb_rows = []
    sel = R500_kpc > 800.0
    for mlo, mhi in ((15, 25), (25, 40), (40, 200)):
        m0 = sel & (M >= mlo) & (M < mhi)
        if m0.sum() < 100:
            continue
        q3 = np.percentile(csb[m0], [0, 100.0 / 3, 200.0 / 3, 100])
        print("    M500 = %d-%d (1e13), N = %d:" % (mlo, mhi, m0.sum()))
        for i in range(3):
            m = m0 & (csb >= q3[i]) & ((csb < q3[i + 1]) if i < 2 else (csb <= q3[i + 1]))
            s = stats(e_can[m])
            csb_rows.append((mlo, mhi, i, s["med"], float(np.median(fbar[m])), float(np.median(zz[m]))))
            print("      c_SB %.3f-%.3f  N=%4d  eta_med %.3f  f_bar %.4f  z_med %.3f  R500_med %.0f kpc"
                  % (q3[i], q3[i + 1], m.sum(), s["med"], np.median(fbar[m]), np.median(zz[m]),
                     np.median(R500_kpc[m])))
    rho_e, p_e = spearmanr(csb[sel], e_can[sel])
    rho_f, p_f = spearmanr(csb[sel], fbar[sel])
    lowest = min(r[3] for r in csb_rows)
    print("    -> the trend is strong (Spearman rho(c_SB, eta) = %+.3f) but it is very nearly the SAME trend as"
          % rho_e)
    print("       rho(c_SB, f_bar) = %+.3f: high-concentration systems have SMALLER measured gas masses.  Since"
          % rho_f)
    print("       MGAS500 is itself derived from the count rate with an assumed profile, this axis is a")
    print("       gas-mass-MEASUREMENT axis at least as much as a dynamical-state one, and it must not be sold")
    print("       as 'relaxed clusters work'.  Even the most extended third at fixed mass sits at eta = %.3f."
          % lowest)

    # ----------------------------------------------------------------- 3. (b) RADIUS
    print("\n" + "-" * W)
    print("3. (b) PART 2 -- RADIUS, the one axis with real structure.  eRASS1 gives R500 quantities ONLY, so")
    print("   this section is an explicit MODEL: NFW total mass (c500 scanned) + beta-model gas (beta, rc")
    print("   scanned), anchored on this sample's OWN median M500, R500 and f_bar(R500).  Model, not data.")
    print("-" * W)
    print("  anchor: M500 = %.3e Msun,  R500 = %.0f kpc,  f_bar(R500) = %.4f (fstar = 0.20 included)"
          % (m500_med / MSUN, r500_med / KPC, fbar_med))
    CELLS = [(c, b, r) for c in (2.0, 3.2, 5.0) for b, r in ((0.65, 0.15), (0.55, 0.10), (0.75, 0.25))]
    XS = (0.1, 0.2, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0)
    print("\n  %-22s %s   %10s" % ("cell (c500,beta,rc)", "".join("%8.2f" % x for x in XS), "x(eta=1)"))
    xcross, prof = [], {}
    for (c5, bt, rc) in CELLS:
        norm = gas_shape_int(1.0, bt, rc)
        row = [profile_eta(x, A0_CANON, c5, bt, rc, m500_med, r500_med, fbar_med, norm)[0] for x in XS]
        f = (lambda t: profile_eta(t, A0_CANON, c5, bt, rc, m500_med, r500_med, fbar_med, norm)[0] - 1.0)
        xc = brentq(f, 1.2, 8.0, xtol=1e-6) if f(8.0) < 0 < f(1.2) else np.nan
        xcross.append(xc)
        prof[(c5, bt, rc)] = row
        print("  c=%.1f b=%.2f rc=%.2f %s   %10.2f" % (c5, bt, rc, "".join("%8.2f" % v for v in row), xc))
    at = {x: np.array([prof[k][i] for k in prof]) for i, x in enumerate(XS)}
    print("\n  BE CLEAR ABOUT WHAT IS AND IS NOT A VALIDATION: at x = 1 the model is PINNED to the anchor")
    print("  (M = M500, M_bar = f_bar M500), so every cell returns the same eta there BY CONSTRUCTION and the")
    print("  %.1f%% offset from the data-side median is only eta-of-medians vs median-of-eta.  The model earns"
          % (100 * abs(at[1.0].mean() / S[can]["med"] - 1)))
    print("  its keep off-anchor, and only against the independent ladder below.")
    print("\n  READ IT OUTWARD: eta = %.2f-%.2f at R500 (data-side median %.3f, pinned as just said),"
          % (at[1.0].min(), at[1.0].max(), S[can]["med"]))
    print("  anchor point), %.2f-%.2f at ~R200 = 1.5 R500, %.2f-%.2f at 2 R500, and it crosses 1 at x = %.2f-%.2f"
          % (at[1.5].min(), at[1.5].max(), at[2.0].min(), at[2.0].max(), np.nanmin(xcross), np.nanmax(xcross)))
    print("  -- i.e. 1.4-2.2 R200, at or beyond the splashback radius, OUTSIDE every measured cluster mass and")
    print("  in a region where hydrostatic equilibrium fails anyway.  The crossing itself is not a discovery:")
    print("  once f_bar saturates and M(r) flattens, eta ~ sqrt(g_obs) -> 0 by construction.  What is")
    print("  informative is WHERE, and the answer is 'nowhere you can measure'.")
    print("\n  READ IT INWARD: eta = %.2f-%.2f at 0.5 R500 and %.2f-%.2f at 0.2 R500.  The corpus's published"
          % (at[0.5].min(), at[0.5].max(), at[0.2].min(), at[0.2].max()))
    print("  eta(R500) is therefore the MILDEST radius at which the front can be quoted, and quoting only it")
    print("  understates the framework's cluster problem by 0.2-0.6 dex.")
    print("\n  MODEL-vs-LADDER CROSS-CHECK.  The model's required acceleration scale g_obs^2/g_bar (which is")
    print("  what a slope-1/2 fit measures) against the published method+radius ladder, canonical footing:")
    print("    %-16s %12s %12s" % ("x = r/R500", "req/a0 range", "dex"))
    req = {}
    for x in XS:
        vals = []
        for (c5, bt, rc) in CELLS:
            norm = gas_shape_int(1.0, bt, rc)
            _, go, gb, _ = profile_eta(x, A0_CANON, c5, bt, rc, m500_med, r500_med, fbar_med, norm)
            vals.append(go * go / gb / A0_CANON)
        req[x] = (min(vals), max(vals))
        print("    %-16.2f %12s %12s" % (x, "%.1f - %.1f" % req[x],
                                         "%.2f - %.2f" % (np.log10(req[x][0]), np.log10(req[x][1]))))
    print("    published rungs, g/a0 canonical:")
    for nm, g in LADDER:
        print("      %-46s %8.2f  (%.3f dex)" % (nm, g / A0_CANON, np.log10(g / A0_CANON)))
    lad_hi = max(g for _, g in LADDER) / A0_CANON
    print("    -> AGREEMENT where they overlap: at x = 0.5-1.0 the model needs %.1f-%.1f a0, which brackets the"
          % (req[1.0][0], req[0.5][1]))
    print("       pooled X-ray HSE rung (%.1f a0) and sits within %.2f dex of Tian+2020's lensing %.1f a0."
          % (9.5e-10 / A0_CANON, abs(np.log10(req[0.5][1] / (G_DDAG / A0_CANON))), G_DDAG / A0_CANON))
    print("    -> DISAGREEMENT inward, and it is against the model: at x = 0.1-0.2 the model demands %.0f-%.0f a0,"
          % (req[0.2][0], req[0.1][1]))
    print("       ABOVE the ladder's top rung (%.1f a0).  So the model's inner AMPLITUDE is not trustworthy --"
          % lad_hi)
    print("       most likely because eRASS1's weak-lensing-calibrated M500 with an NFW c500 puts more mass in")
    print("       the core than the hydrostatic profiles the inner rungs were measured on.  Only the model's")
    print("       DIRECTION inward (independently confirmed by Chan & Del Popolo's own inward growth) and its")
    print("       x >= 0.5 amplitude are used in the verdict.")

    # ----------------------------------------------------------------- 4. (c) REQUIREMENTS
    print("\n" + "-" * W)
    print("4. (c) WHAT WOULD IT TAKE?  Requirement calculations -- a0 stays an INPUT, nothing here is adopted")
    print("-" * W)
    x_req = base["gobs"] / A0_CANON                      # required x = g_obs/a0
    y_req = mu(x_req) * x_req                            # exact inverse: the g_bar that would produce it
    fac = y_req / (base["gbar"] / A0_CANON)
    fac_med = float(np.median(fac))
    e2_med = float(np.median(e_can ** 2))
    x_req_a = base["gobs"] / A0_ALT
    fac_alt = float(np.median(mu(x_req_a) * x_req_a / (base["gbar"] / A0_ALT)))
    print("  (i) EXTRA BARYONS.  Solve nu(y) y = g_obs/a0 exactly for the g_bar that Route A would need:")
    print("      required M_bar / observed M_bar = %.3f (median, canonical) / %.3f (alt)." % (fac_med, fac_alt))
    print("      The deep-limit guess eta^2 = %.3f OVERSTATES it by %.1f%% -- another reason to invert rather"
          % (e2_med, 100 * (e2_med / fac_med - 1)))
    print("      than rescale.  In baryon-fraction terms: measured f_bar(R500) median %.4f -> required %.4f,"
          % (float(np.median(fbar)), float(np.median(fbar * fac))))
    print("      against the cosmic Omega_b/Omega_m = %.4f.  %.1f%% of the 9830 clusters would need MORE"
          % (F_COSMIC, 100 * float((fbar * fac > F_COSMIC).mean())))
    print("      baryons than the cosmic fraction allows, by a median factor %.2f."
          % float(np.median(fbar * fac) / F_COSMIC))
    print("      IS IT PLAUSIBLE?  No, and the reason is specific to THIS framework rather than to MOND.  In a")
    print("      no-CDM MOND cosmology Omega_b/Omega_m = 1 and the cosmic-fraction bar does not apply; but this")
    print("      framework's own dark sector is a ghost condensate with I0 ~ Omega_dm, so it INHERITS the")
    print("      Planck baryon budget and the bar DOES apply.  Milgrom's own cluster-baryonic-dark-matter")
    print("      proposal (Milgrom 2008, New Astron.Rev. 51:906, 'Marriage a-la-MOND') asks for roughly ONE")
    print("      extra hot-gas mass in dark baryons; Route A needs %.2f of them." % (fac_med - 1))
    print("      [citations carried from the standard MOND-cluster literature; re-verify before publication]")
    dark_need = float(np.median(fbar * (fac - 1.0)))
    dark_lcdm = float(np.median(1.0 - fbar))
    print("\n  (ii) OR A DARK COMPONENT THAT CLUSTERS ON CLUSTER SCALES BUT NOT GALAXY SCALES.  Same arithmetic,")
    print("      read as mass rather than baryons: the missing mass is %.3f of M500 (median), against LambdaCDM's"
          % dark_need)
    print("      %.3f.  So the framework needs %.1fx LESS unseen mass in clusters than LambdaCDM does -- a real"
          % (dark_lcdm, dark_lcdm / dark_need))
    print("      and quotable narrowing, and the honest way to state this front.  Who has argued for exactly")
    print("      this: Sanders (2003, MNRAS 342:901) with ~2 eV neutrinos, and Angus, Famaey & Diaferio (2010,")
    print("      MNRAS 402:395) with 11 eV sterile neutrinos -- hot components that free-stream out of galaxies")
    print("      and settle in clusters.  The framework's own ghost-condensate dark sector is a fluid of just")
    print("      that type, which makes this a live door rather than a dead one; what is NOT established is any")
    print("      derivation of the required scale-dependent clustering, so it stays a door and not a result.")
    lam = {}
    for lab, a0 in FOOTINGS:
        lam[lab] = brentq(lambda L, a0=a0: float(np.median(eta_of(
            dict(gobs=base["gobs"], gbar=base["gbar"]), L * a0))) - 1.0, 1.0, 1e3, xtol=1e-10)
    print("\n  (iii) OR A LARGER a0.  Median eta = 1 needs a0 x %.3f canonical / x %.3f alt = %.3e absolute,"
          % (lam[can], lam[alt], lam[can] * A0_CANON))
    print("      the SAME absolute number on both footings (the footing spread is not a resource here).  That is")
    print("      %.1fx the galaxy value the RAR measures, so this door is shut by galaxies, not by clusters."
          % (lam[can] * A0_CANON / A0_MOND))
    k_need = 1.0 / S[can]["med"]
    print("\n  (iv) OR A MASS-SCALE ERROR.  eRASS1's M500 is a weak-lensing-CALIBRATED count-rate proxy, so the")
    print("      relevant systematic is the WL calibration, not hydrostatic bias (and non-thermal pressure has")
    print("      the WRONG SIGN -- it raises M_true and therefore eta).  Closing the median needs M500 to be")
    print("      over-estimated by %.1f%% (k = %.3f):" % (100 * (1 - k_need), k_need))
    print("        %-8s %10s %10s %12s" % ("k", "eta_med", "dex", "sigma @0.10-0.30"))
    for k in (1.0, 0.90, 0.80, 0.75, 0.70):
        dx = np.log10(k) + S[can]["dex"]
        print("        %-8.2f %10.3f %10.4f %12s"
              % (k, k * S[can]["med"], dx, "%.2f - %.2f" % (dx / FLOORS[-1], dx / FLOORS[0])))
    print("      The WL-vs-hydrostatic literature runs at the 10-30 per cent level, k ~ 0.70-0.90, which lands eta")
    print("      at %.2f-%.2f -- the corpus's banked 'weak-lensing recalibration reaches 1.6-1.8'.  It gets the"
          % (0.70 * S[can]["med"], 0.90 * S[can]["med"]))
    print("      front to %.2f-%.2f sigma at the loose floor but NOT to zero: %.1f%% is needed and ~30%% is the"
          % ((np.log10(0.70) + S[can]["dex"]) / FLOORS[-1], (np.log10(0.90) + S[can]["dex"]) / FLOORS[-1],
             100 * (1 - k_need)))
    print("      most anyone claims.  Route A's own kernel gain, for scale, was %.4f dex."
          % (np.log10(COMMITTED["med_a2"]) - np.log10(COMMITTED["med"])))

    print("\n  (v) *** SHARED OR DISTINCTIVE?  The number that matters most for standing. ***")
    print("      Route A's nu(y) = 1/(1 - e^-sqrt(y)) IS McGaugh+2016's RAR interpolation function, so standard")
    print("      MOND and this framework can be compared on the SAME clusters with the SAME kernel, the ONLY")
    print("      difference being the coefficient -- which is exactly the framework's distinctive content.")
    s_mond = stats(eta_of(base, A0_MOND))
    s_m20 = stats(eta_of(base, A0_M20))
    print("      %-42s %9s %9s %10s" % ("a0", "eta_med", "eta_gm", "mean dex"))
    for lab, a0 in (("standard MOND  1.2000e-10 (McGaugh+16)", A0_MOND),
                    ("framework ALT  1.1300e-10", A0_ALT),
                    ("Milgrom 2020   %.4e (kappa=1/2pi)" % A0_M20, A0_M20),
                    ("framework CANON 9.3614e-11 (kappa=1/2)", A0_CANON)):
        s = stats(eta_of(base, a0))
        print("      %-42s %9.4f %9.4f %10.5f" % (lab, s["med"], s["gm"], s["dex"]))
    d_shared = s_mond["dex"]
    d_dist = S[can]["dex"] - s_mond["dex"]
    print("      SHARED with standard MOND : %+.4f dex = %.0f%% of the residual" % (d_shared, 100 * d_shared / S[can]["dex"]))
    print("      DISTINCTIVE to kappa = 1/2: %+.4f dex = %.0f%% of it, a MEASURED factor %.4f (the deep-limit"
          % (d_dist, 100 * d_dist / S[can]["dex"], 10 ** d_dist))
    print("                                  expectation sqrt(1.2e-10/a0) = %.4f is %.1f%% higher -- see C18)"
          % (np.sqrt(A0_MOND / A0_CANON), 100 * (np.sqrt(A0_MOND / A0_CANON) / 10 ** d_dist - 1)))
    print("      The distinctive part is %.2fx the TIGHT end of the systematic floor and %.2fx the loose end."
          % (d_dist / FLOORS[0], d_dist / FLOORS[-1]))
    print("      READ IT PLAINLY, both ways.  The framework does NOT have a cluster problem of its own making:")
    print("      it inherits MOND's, and its own coefficient adds %.0f%% in mass -- below the resolution at"
          % (100 * (10 ** d_dist - 1)))
    print("      which any cluster mass scale is known.  But the sign is against it every time: a lower a0")
    print("      always predicts less acceleration, so ANY coefficient below McGaugh's costs missing mass here.")
    print("      On that same logic Milgrom 2020's kappa = 1/2pi (a0 = %.4e, LOWER still) is %.4f dex WORSE"
          % (A0_M20, s_m20["dex"] - S[can]["dex"]))
    print("      than kappa = 1/2 -- so this front's sign favours kappa = 1/2, but the gap is only %.0f%% of the"
          % (100 * (s_m20["dex"] - S[can]["dex"]) / FLOORS[0]))
    print("      TIGHT floor end, so clusters cannot arbitrate the coefficient in either direction (C20) and")
    print("      claiming them as evidence for kappa = 1/2 would be manufacturing a win.")

    # ----------------------------------------------------------------- 5. (d) FIELD THEORY
    print("\n" + "-" * W)
    print("5. (d) DOES ROUTE A'S FIELD THEORY CHANGE THE CLUSTER NUMBER BEYOND THE KERNEL VALUE?")
    print("-" * W)
    print("  In EXACT spherical symmetry it cannot: the AQUAL field equation integrates to mu(x) x = y, so the")
    print("  algebraic and field-theory readings are identical (committed as C3 of the Route A cluster file).")
    print("  Three channels can break that, and all three are computed here rather than waved at.")

    print("\n  CHANNEL 1 -- ASPHERICITY, done exactly for homoeoidal spheroids.  Baryons on similar concentric")
    print("  spheroids m^2 = R^2 + z^2/q^2 with this file's beta-model shape, normalised so the mass inside the")
    print("  SPHERE r = R500 is the sample's own M_bar.  The Newtonian field is the exact Chandrasekhar")
    print("  tau-integral (validated against the closed-form homogeneous spheroid, C2, and against Newton's")
    print("  own theorem, C1).  Then two facts make this cheap AND exact:")
    print("    * the ALGEBRAIC field g_alg = nu(g_N/a0) g_N is PARALLEL to g_N, and mu(x_alg) x_alg = y_N")
    print("      pointwise, so its closed-surface AQUAL integral equals 4 pi G M_bar identically -- i.e. the")
    print("      algebraic field satisfies AQUAL's own Gauss law on ANY surface, however aspherical (C3).")
    print("    * QUMOND's enclosed mass on a sphere IS the flux of nu(g_N) g_N, the same integral.  So one")
    print("      number answers the question in both bi-potential readings.")
    print("  %-8s %14s %14s %12s %12s" % ("q", "M_flux/M_alg", "eta shift dex", "rms g_n dev", "max tilt"))
    for q in sorted(asph):
        mn, mk, ma, rms, tilt, aqres = asph[q]
        print("  %-8.3f %14.6f %14.5f %12.5f %12.5f" % (q, mk / ma, -np.log10(mk / ma), rms, tilt))
    q6 = asph[0.6]
    print("  For the flattening cluster lensing and simulations actually find (q ~ 0.6-0.7), the field theory")
    print("  predicts %.3f%%-%.3f%% LESS enclosed mass than the spherical algebraic law -- i.e. eta rises by"
          % (100 * (1 - asph[0.7][1] / asph[0.7][2]), 100 * (1 - q6[1] / q6[2])))
    print("  %+.4f to %+.4f dex.  The sign is UNFAVOURABLE (the tangential 'curl' field raises |g| above its"
          % (-np.log10(asph[0.7][1] / asph[0.7][2]), -np.log10(q6[1] / q6[2])))
    print("  normal component, and nu is decreasing, so the flux loses more than Gauss gives back), and the")
    print("  size is %.0fx below the residual.  'Nearly agree' = agree to better than half a per cent."
          % (S[can]["dex"] / max(1e-12, -np.log10(q6[1] / q6[2]))))
    print("  CAVEAT kept explicit: the true AQUAL field differs from the algebraic one by a curl field, which")
    print("  leaves the AQUAL surface integral unchanged (it is fixed by Gauss) but does move <g.n> at the same")
    print("  quadrupole order.  So the correction is bounded by this order, not computed to all orders.")

    print("\n  CHANNEL 2 -- THE PHANTOM DENSITY, which the field-theory script proved positive everywhere.")
    y_prof = np.array([0.005, 0.01, 0.02, y_med, 0.06, 0.1, 0.3])
    print("    M_phantom(<r)/M_bar(<r) = nu(y) - 1 exactly, evaluated with nu_minus1() (the subtraction")
    print("    nu(y) - 1 is safe at cluster y but dies past y ~ 1300, and this corpus has been bitten):")
    print("    %-10s %14s %14s %14s" % ("y", "nu - 1 (canon)", "needed 1/f_bar-1", "shortfall"))
    need_ratio = 1.0 / fbar_med - 1.0
    for yv in y_prof:
        print("    %-10.4f %14.4f %14.4f %14.4f"
              % (yv, float(nu_minus1(yv)), need_ratio, need_ratio / float(nu_minus1(yv))))
    print("    At the sample's median y = %.4f the phantom mass is %.2fx the baryons; the data want %.2fx."
          % (y_med, float(nu_minus1(y_med)), need_ratio))
    print("    So the field theory's phantom halo supplies %.0f%% of the required unseen mass and no more."
          % (100 * float(nu_minus1(y_med)) / need_ratio))
    print("    Positivity is a HEALTH property (no ghost, no negative-mass relief); it is not a resource, and")
    print("    it is worth saying that a NEGATIVE phantom density would have been the only way the field theory")
    print("    could have made the cluster front better than the algebraic law.")

    print("\n  CHANNEL 3 -- THE EXTERNAL FIELD EFFECT.  This section was set up expecting the EFE to be the")
    print("  LARGEST field-theory correction, and the arithmetic says otherwise; the expectation is recorded")
    print("  and withdrawn.  At R500 the clusters sit at y = %.4f, so h(y) = nu(y) y ~ sqrt(y) is STEEP near" % y_med)
    print("  zero and the QUMOND/AQUAL expression h(y_i + y_e) - h(y_e) loses a term of order sqrt(y_e/y_i) --")
    print("  a LONG TAIL, so ALONG ONE LINE OF SIGHT even a tiny external field costs per cent.  h is concave")
    print("  with h(0) = 0 below the inflexion located in C6, hence SUBADDITIVE, so along the ALIGNED axis the")
    print("  sign is fixed: the boost can only fall.  Anchoring a_ext on observed cluster peculiar velocities")
    print("  over a Hubble time (a_ext = v/t_H, v = 300-600 km/s):")
    print("    %-11s %10s %11s %10s %10s %10s %12s %11s"
          % ("v_pec km/s", "a_ext/a0", "y_e (Newt)", "aligned", "anti", "sphere-av", "aligned dex", "sph-av dex"))
    for vpec in (300e3, 600e3):
        a_ext, x_e, y_e, b_al, dx, b_anti, b_avg, dxa = efe[vpec]
        print("    %-11.0f %10.5f %11.3e %10.4f %10.4f %10.4f %12.4f %11.6f"
              % (vpec / 1e3, x_e, y_e, b_al, b_anti, b_avg, dx, dxa))
    _kg = np.log10(COMMITTED["med_a2"]) - np.log10(COMMITTED["med"])
    print("  READ THE LAST TWO COLUMNS.  Along the acceleration axis the inferred mass moves by %+.1f%% to %+.1f%%"
          % (100 * (10 ** d_efe[0] - 1), 100 * (10 ** d_efe[1] - 1)))
    print("  and the ANTI-aligned direction moves the other way -- but the SPHERE-AVERAGED enclosed mass, which")
    print("  is what an eta measurement actually uses, moves by only %+.2e to %+.2e dex.  The first-order term"
          % d_efe_avg)
    print("  CANCELS: constant vectors have zero flux through a closed surface, and the O(y_e) piece of")
    print("  nu(|y_i + y_e|) is odd in cos(angle).  What survives is O((y_e/y_i)^2) = %.1e, i.e. nothing."
          % ((efe[600e3][2] / y_med) ** 2))
    print("  SO THE HONEST ANSWER TO (d) IS: NEITHER field-theory channel changes the cluster residual at more")
    print("  than the %.3f%% level (asphericity %.4f dex, EFE monopole %.1e dex, against a %.4f dex residual and"
          % (100 * (10 ** d_asph - 1), d_asph, d_efe_avg[1], S[can]["dex"]))
    print("  a %.4f dex kernel gain).  The cluster number is a KERNEL-VALUE statement and the field theory does" % _kg)
    print("  not rescue or worsen it.  What the EFE does predict instead is a signed DIPOLE in cluster mass")
    print("  measurements of +/-%.1f-%.1f%% aligned with each cluster's own peculiar acceleration -- the same"
          % (100 * (10 ** d_efe[0] - 1), 100 * (10 ** d_efe[1] - 1)))
    print("  observable class as the corpus's directional-EFE front (whose AQUAL-class galaxy amplitude is")
    print("  4.3%), not a correction to eta.  Caveats both ways: a_ext is an order-of-magnitude estimate, the")
    print("  uniform-external-field idealisation ignores the tidal part, and the modified-INERTIA reading's own")
    print("  EFE amplitude is NOT computed here.  OPEN, not settled.")

    # ================================================================= CHECKS
    print("\n" + "=" * W)
    print("CHECKS -- validations against independent closed forms, and falsifiable comparisons.")
    print("C4, C7, C15b, C17 run AGAINST the framework's interest; C5b withdraws this file's own expectation;")
    print("C20 refuses a favourable-looking result as unmeasurable.")
    print("=" * W)

    # C0 -- the sample is the anchor's, bit for bit
    chk("C0 this file's own FITS read reproduces the anchor loader's sample exactly (N and the committed "
        "median eta), so every number below is comparable to the committed standing by construction",
        int(okm.sum()) == base["N"] and abs(S[can]["med"] - COMMITTED["med"]) < 1e-3
        and abs(S[can]["dex"] - COMMITTED["dex"]) < 1e-3,
        "N %d vs %d; eta_med %.4f vs committed %.3f; dex %.5f vs %.4f"
        % (okm.sum(), base["N"], S[can]["med"], COMMITTED["med"], S[can]["dex"], COMMITTED["dex"]))

    # C1 -- Newton's theorem on the spheroid machinery
    worst_g = 0.0
    for q in (1.0, 0.8, 0.7, 0.5, 1.0 / 0.7, 2.0):
        mn, _, _, _, _, _ = flux_masses(q, 1.0, A0_CANON, mbar_med, r500_med)
        worst_g = max(worst_g, abs(mn / mbar_med - 1.0))
    chk("C1 the spheroidal Newtonian field satisfies Gauss's law on the sphere r = R500 for oblate AND prolate "
        "shapes: the flux returns the independently quadratured enclosed mass",
        worst_g < 1e-7, "worst |flux/M_enc - 1| over q = 0.5..2 is %.2e" % worst_g)

    # C2 -- and it reproduces the exact closed form for a homogeneous spheroid
    worst_h = 0.0
    for q in (0.9, 0.7, 0.5, 0.3):
        e = np.sqrt(1 - q * q)
        A1 = (np.sqrt(1 - e * e) / e ** 3) * np.arcsin(e) - (1 - e * e) / e ** 2
        A3 = 2.0 / e ** 2 - 2 * np.sqrt(1 - e * e) * np.arcsin(e) / e ** 3
        gR, gz = g_spheroid(0.3, 0.2, q, shape=lambda m: (np.asarray(m, float) <= 1.0) * 1.0)
        worst_h = max(worst_h, abs(gR / (-A1 * 0.3) - 1.0), abs(gz / (-A3 * 0.2) - 1.0),
                     abs(2 * A1 + A3 - 2.0))
    chk("C2 the same field machinery reproduces the CLOSED-FORM interior field of a homogeneous oblate "
        "spheroid, -2 pi G rho (A1 R, A3 z) with 2A1 + A3 = 2, to machine precision -- so the aspherical "
        "correction in section 5 is not a quadrature artefact",
        worst_h < 1e-9, "worst relative deviation over q = 0.3..0.9 is %.2e" % worst_h)

    # C3 -- the algebraic field satisfies AQUAL's Gauss law on aspherical surfaces
    worst_a = max(abs(asph[q][5]) for q in asph)
    chk("C3 the ALGEBRAIC field satisfies AQUAL's own closed-surface identity, integral of mu(x) x a0 cos(psi) "
        "dA = 4 pi G M_bar, on flattened spheres too -- which is what makes the section-5 number an AQUAL "
        "statement and not only a QUMOND one (this exercises the module's mu inversion off-axis)",
        worst_a < 1e-6, "worst |identity - 1| over q = 0.5..1.43 is %.2e" % worst_a)

    # C4 -- AGAINST INTEREST: asphericity always hurts, and by how much
    signs = all(asph[q][1] < asph[q][2] for q in asph if abs(q - 1.0) > 1e-9)
    chk("C4 AGAINST INTEREST -- asphericity always LOWERS the field theory's enclosed mass relative to the "
        "spherical algebraic law (so it always RAISES eta), for oblate and prolate alike, while the q = 1 case "
        "returns the algebraic answer identically",
        signs and abs(asph[1.0][1] / asph[1.0][2] - 1.0) < 1e-9,
        "q=0.6 ratio %.6f, q=0.5 %.6f, prolate %.6f; q=1 residual %.2e"
        % (asph[0.6][1] / asph[0.6][2], asph[0.5][1] / asph[0.5][2],
           asph[1.0 / 0.7][1] / asph[1.0 / 0.7][2], abs(asph[1.0][1] / asph[1.0][2] - 1.0)))

    # C5 -- but it is negligible, and (b) the EFE is NOT as negligible
    chk("C5a the aspherical correction at a realistic q = 0.6 is at least 100x smaller than the residual it "
        "would have to explain, which is the QUANTITATIVE form of 'a cluster is nearly spherical'",
        -np.log10(asph[0.6][1] / asph[0.6][2]) * 100 < S[can]["dex"],
        "%.5f dex vs %.5f dex residual = %.0fx"
        % (-np.log10(asph[0.6][1] / asph[0.6][2]), S[can]["dex"],
           S[can]["dex"] / -np.log10(asph[0.6][1] / asph[0.6][2])))
    kernel_gain = np.log10(COMMITTED["med_a2"]) - np.log10(COMMITTED["med"])
    chk("C5b THE EXPECTATION THAT SET UP CHANNEL 3 IS WITHDRAWN BY ITS OWN ARITHMETIC -- the EFE is first-order "
        "and per-cent-sized along ONE line of sight, but its effect on the SPHERE-AVERAGED enclosed mass (the "
        "quantity eta is built from) cancels at first order and is 100x smaller than even the aspherical term, "
        "so it is a DIPOLE prediction and not a correction to the residual.  Both halves are measured here",
        d_efe[0] > 0.01 and abs(d_efe_avg[1]) < 0.01 * abs(d_asph),
        "aligned +%.4f to +%.4f dex, anti-aligned %+.4f, sphere-averaged %+.6f to %+.6f dex; asphericity "
        "+%.4f dex; kernel gain %.4f dex"
        % (d_efe[0], d_efe[1], np.log10(float(nu(y_med)) / efe[600e3][5]), d_efe_avg[0], d_efe_avg[1],
           d_asph, kernel_gain))

    # C6 -- the EFE sign is a theorem with an EXACT domain, not a numerical accident
    def h2_at(t):                                       # central second difference, relative step
        dd = 1e-3 * t
        hf = lambda v: float(nu(v)) * v
        return (hf(t + dd) - 2.0 * hf(t) + hf(t - dd)) / dd ** 2
    y_star = brentq(h2_at, 4.0, 20.0, xtol=1e-8)
    ycc = np.linspace(1e-3, 0.99 * y_star, 200001)      # uniform grid: a real second derivative
    h2_lo = np.gradient(np.gradient(nu(ycc) * ycc, ycc), ycc)
    # the convex side is checked only out to y = 30: past that h'' ~ e^-sqrt(y) is below float64's noise
    # floor for ANY finite difference, so asserting its sign there would be asserting rounding error.
    ycv = np.linspace(1.01 * y_star, 30.0, 20001)
    h2_hi = np.gradient(np.gradient(nu(ycv) * ycv, ycv), ycv)
    y_max = max(float((base["gbar"] / a0).max()) for _, a0 in FOOTINGS)
    rng = np.random.default_rng(20260803)
    ya = 10 ** rng.uniform(-8, np.log10(y_star / 2), 40000)
    yb = 10 ** rng.uniform(-8, np.log10(y_star / 2), 40000)
    sub = nu(ya) * ya + nu(yb) * yb - nu(ya + yb) * (ya + yb)     # subadditivity gap, must be > 0
    chk("C6 h(y) = nu(y) y is strictly CONCAVE on 0 < y < %.2f and strictly CONVEX from there out to y = 30 (an "
        "EXACT domain, located here rather than assumed: claiming GLOBAL concavity would have been FALSE, since "
        "h -> y from above), h(0) = 0, so h is SUBADDITIVE below the inflexion and h(y_i + y_e) - h(y_e) < "
        "h(y_i) strictly -- the aligned EFE's sign is structural.  Every cluster in the sample lies inside that "
        "domain on both footings (max y = %.3f)" % (y_star, y_max),
        bool(np.all(h2_lo < 0)) and bool(np.all(h2_hi > 0)) and y_max < y_star and bool(np.all(sub > 0))
        and all((float(nu(y_med + ye)) * (y_med + ye) - float(nu(ye)) * ye)
                < float(nu(y_med)) * y_med for ye in (1e-8, 1e-6, 1e-4, 1e-2, 0.1)),
        "inflexion at y* = %.4f (u* = %.4f); max h'' below it %.2e, min h'' above it %.2e; min "
        "subadditivity gap over 40000 random pairs %.2e; sample max y %.3f is %.1fx inside the domain"
        % (y_star, np.sqrt(y_star), float(h2_lo.max()), float(h2_hi.min()), float(sub.min()), y_max,
           y_star / y_max))

    # C7 -- AGAINST INTEREST: the deep-limit shortcut overstates the baryon requirement
    chk("C7 AGAINST INTEREST -- the exact inversion of nu(y) y = g_obs/a0 gives a required baryon factor "
        "MATERIALLY SMALLER than the eta^2 deep-limit shortcut, so the corpus's 'needs eta^2 more baryons' "
        "wording overstates its own problem",
        fac_med < e2_med and abs(e2_med / fac_med - 1) > 0.10
        and float(np.abs(nu(y_req) * y_req / x_req - 1.0).max()) < 1e-9,
        "exact %.4f vs eta^2 %.4f (%.1f%% apart); the inversion round-trips through the OTHER form, "
        "nu(y_req) y_req / (g_obs/a0) - 1, to %.2e on all %d clusters"
        % (fac_med, e2_med, 100 * (e2_med / fac_med - 1),
           float(np.abs(nu(y_req) * y_req / x_req - 1.0).max()), base["N"]))

    # C8 -- the extra-baryon escape is closed by the cosmic fraction
    frac_over = float((fbar * fac > F_COSMIC).mean())
    chk("C8 the extra-baryon escape is shut for essentially the whole sample: >95% of clusters would need a "
        "baryon fraction above the cosmic Omega_b/Omega_m, which this framework inherits because its own dark "
        "sector carries an Omega_dm-sized amount",
        frac_over > 0.95, "%.1f%% of clusters exceed f_cosmic = %.4f; median required f_bar %.4f = %.2f x cosmic"
        % (100 * frac_over, F_COSMIC, float(np.median(fbar * fac)), float(np.median(fbar * fac)) / F_COSMIC))

    # C9 -- FAVOURABLE and falsifiable: less unseen mass than LambdaCDM
    chk("C9 the unseen mass Route A needs in clusters is at least 3x LESS than LambdaCDM needs on the same "
        "clusters -- the front is a shortfall in a theory that already removes most of the dark matter, and "
        "that comparison is quotable",
        dark_lcdm / dark_need > 3.0,
        "Route A needs %.3f of M500 unseen, LambdaCDM %.3f -> %.1fx less" % (dark_need, dark_lcdm, dark_lcdm / dark_need))

    # C10 -- the mass-calibration escape needs more than the literature offers
    chk("C10 closing the front by mass calibration alone needs M500 over-estimated by more than 30%, i.e. "
        "beyond the WL-vs-hydrostatic range anyone claims; at the literature's own 10-30% it lands at "
        "eta = 1.5-1.9, not 1",
        k_need < 0.70 and 0.70 * S[can]["med"] > 1.3,
        "needs k = %.3f (%.1f%% over-estimate); k = 0.70 gives eta %.3f, k = 0.90 gives %.3f"
        % (k_need, 100 * (1 - k_need), 0.70 * S[can]["med"], 0.90 * S[can]["med"]))

    # C11 -- mass uniformity
    chk("C11 the residual is FLAT in mass: across a factor-%.0f range in M500 the median eta varies by under "
        "15 per cent, and the lowest-mass decile is the WORST, so there is no group-scale escape"
        % (M.max() / M.min()),
        (med_M.max() / med_M.min() - 1) < 0.15 and med_M.min() > 1.9 and rows_M[0][3] > np.median(med_M),
        "eta_med spans %.3f-%.3f (%.1f%%); lowest-mass decile %.3f vs sample median %.3f"
        % (med_M.min(), med_M.max(), 100 * (med_M.max() / med_M.min() - 1), rows_M[0][3], np.median(med_M)))

    # C12 -- redshift: rises, and the best bin still fails
    chk("C12 the residual RISES with redshift and the lowest-z decile still sits far above 1, so there is no "
        "low-z escape either (and any a0(z) reading of this front has to fight the mass-z degeneracy in this "
        "catalogue, which is not attempted here)",
        med_z[-1] > med_z[0] and med_z.min() > 1.9,
        "lowest-z decile %.3f -> highest %.3f (+%.1f%%); best bin %.3f = %+.4f dex"
        % (med_z[0], med_z[-1], 100 * (med_z[-1] / med_z[0] - 1), med_z.min(), np.log10(med_z.min())))

    # C13 -- morphology axis is a gas-mass axis
    chk("C13 the surface-brightness-concentration trend is very nearly the gas-fraction trend (both Spearman "
        "coefficients large and of opposite sign), and even the most extended third at fixed mass and size "
        "stays near eta ~ 2, so 'relaxed clusters work' is NOT available",
        abs(rho_f) > 0.5 and rho_e * rho_f < 0 and lowest > 1.8,
        "rho(c_SB, eta) = %+.3f, rho(c_SB, f_bar) = %+.3f; lowest tertile eta = %.3f" % (rho_e, rho_f, lowest))

    # C14 -- the radial model's anchor, with its status stated honestly
    chk("C14 the radial model's x = 1 value is PINNED by the anchor (so this is a consistency statement, NOT an "
        "independent validation, and is labelled as such in the text): every cell agrees to 1e-6 there, and the "
        "residual gap to the data-side median is under 10% -- the eta-of-medians vs median-of-eta difference",
        float(at[1.0].max() / at[1.0].min() - 1) < 1e-6
        and all(abs(v / S[can]["med"] - 1) < 0.10 for v in at[1.0]),
        "all nine cells give %.4f at x=1 (spread %.1e) vs data median %.3f = %.1f%% apart"
        % (at[1.0].mean(), float(at[1.0].max() / at[1.0].min() - 1), S[can]["med"],
           100 * abs(at[1.0].mean() / S[can]["med"] - 1)))

    # C15 -- model vs the published ladder, both ways
    chk("C15a where the model and the published ladder overlap in radius (x = 0.5-1) the model's required "
        "acceleration scale BRACKETS the pooled X-ray HSE rung 9.5e-10 -- an independent, falsifiable "
        "agreement, not a fit",
        req[1.0][0] < 9.5e-10 / A0_CANON < req[0.5][1],
        "model x=1: %.1f-%.1f a0, x=0.5: %.1f-%.1f a0; rung %.1f a0"
        % (req[1.0][0], req[1.0][1], req[0.5][0], req[0.5][1], 9.5e-10 / A0_CANON))
    chk("C15b AGAINST THE MODEL -- inward of 0.2 R500 the model demands MORE than the ladder's top rung, so its "
        "inner amplitude is reported as untrustworthy rather than used; only its direction and its x >= 0.5 "
        "amplitude enter the verdict",
        req[0.2][0] > lad_hi,
        "model x=0.2: %.0f-%.0f a0 vs ladder top rung %.1f a0 (%.1fx over)"
        % (req[0.2][0], req[0.2][1], lad_hi, req[0.2][0] / lad_hi))

    # C16 -- nothing closes inside the data
    chk("C16 eta crosses 1 only well OUTSIDE R500 in every one of the nine model cells (and outside R200 in "
        "all of them), so the radius axis provides no closure anywhere masses are actually measured",
        np.nanmin(xcross) > 1.55 and np.all(np.array([at[1.0]]) > 1.9),
        "crossing radius x = %.2f-%.2f R500 (R200 ~ 1.5 R500); eta(R200) = %.2f-%.2f"
        % (np.nanmin(xcross), np.nanmax(xcross), at[1.5].min(), at[1.5].max()))

    # C17 -- AGAINST INTEREST: the residual grows inward past every floor
    inner = np.log10(at[0.5].min())
    chk("C17 AGAINST INTEREST -- at 0.5 R500, where the model still agrees with the published ladder, the "
        "residual is a tension at BOTH ends of the systematic floor range, which the committed R500-only "
        "headline does not show",
        inner / FLOORS[-1] > 1.5 and inner / FLOORS[0] > 4.5,
        "eta(0.5 R500) = %.2f-%.2f = %+.3f to %+.3f dex -> %.1f-%.1f sigma at the 0.30-0.10 dex floor"
        % (at[0.5].min(), at[0.5].max(), inner, np.log10(at[0.5].max()),
           inner / FLOORS[-1], np.log10(at[0.5].max()) / FLOORS[0]))

    # C18 -- shared vs distinctive, measured against the deep-limit prediction
    pred = np.sqrt(A0_MOND / A0_CANON)
    chk("C18 the framework-vs-standard-MOND penalty on the same clusters tracks the deep-limit sqrt(a0) "
        "scaling to a few per cent -- close enough that the coefficient's cost is understood analytically, far "
        "enough that the split is quoted from the MEASURED %.4f dex and not from the asymptotic guess" % d_dist,
        abs((S[can]["gm"] / s_mond["gm"]) / pred - 1) < 0.03,
        "measured geomean ratio %.4f vs sqrt(1.2e-10/a0) = %.4f (%.1f%% apart -- the clusters are deep but not "
        "asymptotically deep, median y = %.4f)"
        % (S[can]["gm"] / s_mond["gm"], pred, 100 * abs((S[can]["gm"] / s_mond["gm"]) / pred - 1), y_med))

    chk("C19 the DISTINCTIVE part of the cluster residual is smaller than the TIGHT end of the systematic "
        "floor, so the framework's own coefficient is not resolvable on this front -- the honest standing "
        "statement, and it could have come out the other way",
        d_dist < FLOORS[0], "distinctive %.4f dex vs tight floor %.2f dex (%.0f%% of it)"
        % (d_dist, FLOORS[0], 100 * d_dist / FLOORS[0]))

    # C20 -- the kappa question is NON-DIAGNOSTIC on this front, and its sign happens to favour kappa = 1/2
    chk("C20 the cluster front cannot arbitrate the coefficient: the whole gap between kappa = 1/2 and Milgrom "
        "2020's kappa = 1/2pi is smaller than a QUARTER of even the tight end of the systematic floor.  Its "
        "sign does favour kappa = 1/2 (1/2pi means a LOWER a0, hence a bigger deficit), and that must NOT be "
        "sold as cluster evidence for kappa = 1/2 -- the gap is unmeasurable here",
        abs(s_m20["dex"] - S[can]["dex"]) < 0.25 * FLOORS[0] and s_m20["dex"] > S[can]["dex"],
        "kappa=1/2 %+.5f dex vs kappa=1/2pi %+.5f dex: gap %.4f dex = %.0f%% of the tight floor"
        % (S[can]["dex"], s_m20["dex"], s_m20["dex"] - S[can]["dex"],
           100 * (s_m20["dex"] - S[can]["dex"]) / FLOORS[0]))

    # C21 -- float64 hygiene on the phantom-mass identity
    yv = base["gbar"] / A0_CANON
    m_ph_a = nu_minus1(yv)
    m_ph_b = nu(yv) - 1.0
    chk("C21 the phantom-to-baryon ratio nu - 1 is computed through nu_minus1(): it agrees with the naive "
        "subtraction at cluster accelerations (where float64 still holds it) but the naive form is already "
        "dead at y = 1e4, which is why the stable form is used throughout",
        float(np.abs(m_ph_a / m_ph_b - 1).max()) < 1e-12 and (nu(1e4) - 1.0) == 0.0
        and float(nu_minus1(1e4)) > 0.0,
        "worst relative difference at cluster y = %.2e; naive nu(1e4)-1 = %.1f vs nu_minus1 = %.3e"
        % (float(np.abs(m_ph_a / m_ph_b - 1).max()), nu(1e4) - 1.0, float(nu_minus1(1e4))))

    # C22 -- the floor arithmetic, over the full range, both footings
    chk("C22 the loose end of this corpus's own floor range puts the residual below 1.5 sigma while the tight "
        "end puts it above 3, on BOTH footings -- both readings live inside the declared range, which is "
        "exactly why neither may be quoted alone",
        S[can]["dex"] / FLOORS[-1] < 1.5 < 3.0 < S[can]["dex"] / FLOORS[0]
        and S[alt]["dex"] / FLOORS[-1] < 1.5 < 3.0 < S[alt]["dex"] / FLOORS[0],
        "canonical %.2f (0.30 dex) to %.2f (0.10 dex); alt %.2f to %.2f"
        % (S[can]["dex"] / FLOORS[-1], S[can]["dex"] / FLOORS[0],
           S[alt]["dex"] / FLOORS[-1], S[alt]["dex"] / FLOORS[0]))

    # ================================================================= VERDICT
    print("\n" + "=" * W)
    if _FAILS:
        print("RESULT: %d of %d CHECK(S) FAILED -> %s" % (len(_FAILS), len(_RUN), "; ".join(_FAILS)))
        print("=" * W)
        sys.exit(1)
    print("RESULT: all %d checks passed." % len(_RUN))
    print("-" * W)
    print("LANE 3 VERDICT -- THE DEFICIT IS REAL, IT IS %.0f%% MOND'S AND %.0f%% THE FRAMEWORK'S, AND NO REGIME"
          % (100 * d_shared / S[can]["dex"], 100 * d_dist / S[can]["dex"]))
    print("INSIDE THE DATA CLOSES IT.")
    print("  (a) eta(R500) = %.2f geomean / %.2f median canonical (%.2f / %.2f alt) = %+.3f dex canonical,"
          % (S[can]["gm"], S[can]["med"], S[alt]["gm"], S[alt]["med"], S[can]["dex"]))
    print("      %+.3f alt.  Statistical error %.4f dex is irrelevant; the 0.10-0.30 dex absolute mass-scale"
          % (S[alt]["dex"], S[can]["se"]))
    print("      floor dominates and gives %.2f-%.2f sigma canonical, %.2f-%.2f alt.  Two field-theory terms"
          % (S[can]["dex"] / FLOORS[-1], S[can]["dex"] / FLOORS[0],
             S[alt]["dex"] / FLOORS[-1], S[alt]["dex"] / FLOORS[0]))
    print("      previously uncosted are both negligible: asphericity %+.4f dex (unfavourable) and the EFE's"
          % d_asph)
    print("      effect on the sphere-averaged mass %+.1e dex (it cancels at first order)." % d_efe_avg[1])
    print("  (b) NO closing regime inside the data.  Mass: flat to %.0f%% over a factor %.0f, worst at the LOW"
          % (100 * (med_M.max() / med_M.min() - 1), M.max() / M.min()))
    print("      end.  Redshift: rises %.0f%% from z ~ %.02f to z ~ %.2f, best bin still %.2f.  Temperature:"
          % (100 * (med_z[-1] / med_z[0] - 1), rows_z[0][6], rows_z[-1][6], med_z.min()))
    print("      flat to %.0f%%.  Morphology: a %.0f%% trend that tracks the measured gas fraction, not"
          % (100 * (med_T.max() / med_T.min() - 1), 100 * (max(r[3] for r in csb_rows) / lowest - 1)))
    print("      relaxation.  RADIUS is the only axis with structure: eta = %.1f-%.1f at 0.2 R500, %.2f at"
          % (at[0.2].min(), at[0.2].max(), S[can]["med"]))
    print("      R500, %.2f-%.2f at R200, crossing 1 only at %.1f-%.1f R500 -- beyond the splashback radius."
          % (at[1.5].min(), at[1.5].max(), np.nanmin(xcross), np.nanmax(xcross)))
    print("      So the honest narrowing runs the OTHER way: the front is worse inward than the committed")
    print("      R500 headline shows, and at 0.5 R500 it is a tension at both ends of the floor range.")
    print("  (c) REQUIREMENTS: %.2fx the observed baryons (exact inversion; the eta^2 shortcut overstates it by"
          % fac_med)
    print("      %.0f%%), i.e. f_bar = %.3f against a cosmic %.3f, which this framework's Omega_dm-sized dark"
          % (100 * (e2_med / fac_med - 1), float(np.median(fbar * fac)), F_COSMIC))
    print("      sector does NOT let it evade; or M500 over-estimated by %.0f%% against a 10-30%% literature;"
          % (100 * (1 - k_need)))
    print("      or a0 x %.1f, which galaxies forbid.  Read as mass instead of baryons, the requirement is"
          % lam[can])
    print("      %.3f of M500 unseen versus LambdaCDM's %.3f -- %.1fx less, and hot-neutrino-like components"
          % (dark_need, dark_lcdm, dark_lcdm / dark_need))
    print("      (Sanders 2003; Angus+2010) are the argued precedent and the framework's ghost condensate is")
    print("      of that type.  SHARED vs DISTINCTIVE: standard MOND on these same clusters with this same")
    print("      kernel leaves %+.4f dex, so %.0f%% is MOND's forty-year-old problem and %.0f%% (%.4f dex,"
          % (d_shared, 100 * d_shared / S[can]["dex"], 100 * d_dist / S[can]["dex"], d_dist))
    print("      a factor %.3f) is kappa = 1/2 -- HALF the tight floor and a SIXTH of the loose one, i.e. below"
          % (10 ** d_dist))
    print("      the resolution of any cluster mass scale.  The sign of the coefficient's effect is always")
    print("      unfavourable (lower a0 = less acceleration), and on that same logic kappa = 1/2pi is %.4f dex"
          % (s_m20["dex"] - S[can]["dex"]))
    print("      WORSE here than kappa = 1/2 -- but at %.0f%% of the tight floor that is unmeasurable, so this"
          % (100 * (s_m20["dex"] - S[can]["dex"]) / FLOORS[0]))
    print("      front cannot be cited for kappa = 1/2 either.  NON-DIAGNOSTIC of the coefficient.")
    print("  (d) The field theory changes the cluster number NEGLIGIBLY, and the only non-zero term goes the")
    print("      wrong way.  Asphericity at q = 0.6-0.7 costs %.3f%%-%.3f%% of the predicted enclosed"
          % (100 * (1 - asph[0.7][1] / asph[0.7][2]), 100 * (1 - asph[0.6][1] / asph[0.6][2])))
    print("      mass -- 'nearly spherical' now means 'agrees to better than half a per cent', proved with an")
    print("      exact homoeoidal calculation validated twice.  The phantom halo is positive and supplies")
    print("      %.0f%% of the needed unseen mass; positivity is health, not a resource.  The EFE is the"
          % (100 * float(nu_minus1(y_med)) / need_ratio))
    print("      SMALLER term still: %+.4f to %+.4f dex along one line of sight but only %+.1e to %+.1e dex on"
          % (d_efe[0], d_efe[1], d_efe_avg[0], d_efe_avg[1]))
    print("      the sphere-averaged mass eta is built from, because the first-order term cancels by Gauss.")
    print("      The expectation that the EFE would dominate here is WITHDRAWN by its own arithmetic; what it")
    print("      leaves behind is a signed +/-%.1f-%.1f%% DIPOLE prediction in cluster masses, aligned with each"
          % (100 * (10 ** d_efe[0] - 1), 100 * (10 ** d_efe[1] - 1)))
    print("      cluster's peculiar acceleration, in the same observable class as the directional-EFE front.")
    print("  OPEN, and not closed by anything here: the WL mass calibration, the floor itself, the")
    print("  Kelleher-Lelli Eq. (5) modified-inertia caveat, real extra baryons or hot relics, the MI reading's")
    print("  own EFE amplitude, and the AQUAL curl field beyond quadrupole order.")
    print("=" * W)


if __name__ == "__main__":
    main()
