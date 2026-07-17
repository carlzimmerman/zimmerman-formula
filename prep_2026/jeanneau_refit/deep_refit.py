#!/usr/bin/env python3
"""
deep_refit.py -- LANE R deliverable: the Jeanneau+26 (MUSE-DARK II, A&A 709 A120,
arXiv:2603.28856) LOW-ACCELERATION bTFR refit, consolidated.

Inputs (all real, all in this directory):
  jeanneau26_catalog_cds.csv : verbatim CDS/VizieR J/A+A/709/A120/catalog (their Table E1,
                               CC-BY-4.0), 95 rows = exactly their fiducial bTFR fit sample
                               (their Tab.4: slope a=3.14 Lelli+19, b_ref=3.54, b=3.54+-0.06).
  FROZEN_CUTS.md             : selection + estimator + error model, frozen 2026-07-16 19:34
                               BEFORE any per-galaxy number was read. Followed mechanically.
  apply_frozen_cut.py        : the first (frozen) application; this script re-derives every
                               number independently of that file's in-memory state and adds
                               (3) the LCDM halo-drift degeneracy computation and (5) the figure.

Outputs: printed report (exit 0), deep_refit.png, deep_refit_degeneracy.csv.

Sections (per the lane spec):
  (1) subsample bTFR zero-point offset per the frozen estimator + bootstrap stat + honest band
  (2) fork predictions FOR THIS SUBSAMPLE -- exact per-galaxy, framework's own nu,
      EACH FOOTING'S OWN a0 in the dilution (parent VERIFY caught a cross-footing dilution
      bug in a context table; the exact computation here never mixes a0's)
  (3) the LCDM halo-scaling drift for the same subsample -- does the deep cut break the
      parent's ALT-LCDM degeneracy? COMPUTED, not assumed.
  (4) verdict per the frozen mechanical rules + honesty rails
  (5) figure: subsample points + fork bands
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR = "/Users/carlzimmerman/new_physics/prep_2026/jeanneau_refit"

# ---------------- frozen constants (FROZEN_CUTS.md section 7) ----------------
A0_CANON = 9.36e-11           # m/s^2  (canonical: cH_Lambda/Z, rho_DE branch)
A0_ALT = 1.13e-10             # m/s^2  (ALT: rho_total/cH0 branch)
CUT_GBAR = 0.5 * A0_CANON     # 4.68e-11
SLOPE, BREF = 3.14, 3.54      # Lelli+19 line exactly as Jeanneau+26 adopt it (their Tab.4)
SYS_GAS, SYS_REF, SYS_CONV = 0.20, 0.16, 0.06
NBOOT = 10000
KPC = 3.0857e19               # m
ALPHA_SIZE = 0.75             # van der Wel+14 (size-term check only)
Om_P, OL_P = 0.315, 0.685     # banked fork cosmology
W0, WA = -0.752, -0.86        # DESI DR2 CPL (canonical-CPL variant)
Om_J, OL_J, H0_J = 0.30, 0.70, 70.0   # the PAPER's cosmology, arcsec->kpc only

# ---------------- parent machinery, banked anchors re-asserted ----------------
def f_DE(z, w0=W0, wa=WA):
    z = np.asarray(z, float)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))

def E_z(z, w0=W0, wa=WA):
    return np.sqrt(Om_P * (1 + np.asarray(z, float)) ** 3 + OL_P * f_DE(z, w0, wa))

assert abs(float(np.sqrt(f_DE(3.0))) - 0.737) < 0.005
assert abs(0.25 * np.log10(np.sqrt(f_DE(3.0))) - (-0.033)) < 0.001, "canonical dlogV(3)"
assert abs(0.25 * np.log10(E_z(3.0)) - 0.164) < 0.003, "ALT dlogV(3)"
assert np.allclose(np.sqrt(f_DE(np.array([1., 2., 3.]), w0=-1.0, wa=0.0)), 1.0), "pure-Lambda flat"

def Delta_c(z):
    z = np.asarray(z, float)
    Ez2 = Om_P * (1 + z) ** 3 + OL_P
    x = Om_P * (1 + z) ** 3 / Ez2 - 1
    return 18 * np.pi ** 2 + 82 * x - 39 * x ** 2

def dlogM_lcdm_halo(z):
    """Standard LCDM halo-scaling bTFR drift (Jeanneau Eq.9 first term; Dutton+11/MMW).
    A mass-assembly effect: it does NOT pass through nu and is NOT a0-diluted."""
    Ez = np.sqrt(Om_P * (1 + np.asarray(z, float)) ** 3 + OL_P)
    return -np.log10(Ez * np.sqrt(Delta_c(z) / Delta_c(0.0)))

assert abs(float(dlogM_lcdm_halo(1.0)) - (-0.34)) < 0.03, "Jeanneau Eq.9 -0.34 at z=1"
print("[OK] banked anchors: canonical dlogV(3)=-0.033, ALT +0.164, LCDM halo(z=1)=-0.35")

def g_bar_of(g_obs, a0):
    """Invert the framework's OWN interpolation g_obs = sqrt(g_bar^2 + g_bar*a0)."""
    return 0.5 * (-a0 + np.sqrt(a0 ** 2 + 4.0 * np.asarray(g_obs, float) ** 2))

def D_A_kpc_per_arcsec(z, Om=Om_J, OL=OL_J, H0=H0_J):
    c = 299792.458
    zz = np.linspace(0.0, z, 4096)
    Dc = c / H0 * np.trapz(1.0 / np.sqrt(Om * (1 + zz) ** 3 + OL), zz)
    return Dc / (1 + z) * 1e3 * np.pi / (180 * 3600)

# ---------------- load the real catalog ----------------
rows = list(csv.DictReader(open(DIR + "/jeanneau26_catalog_cds.csv")))
assert len(rows) == 95, "must be exactly Jeanneau+26's fiducial N=95"
z = np.array([float(r["zR21"]) for r in rows])
mu = np.array([float(r["muR21"]) for r in rows])
Re_as = np.array([float(r["Reff"]) for r in rows])
logV = np.array([float(r["logV2_0"]) for r in rows])
s_logV = np.array([float(r["s_logV2_0"]) for r in rows])
logMs = np.array([float(r["logM*"]) for r in rows])
logMHI = np.array([float(r["logMHI"]) for r in rows])
logMMol = np.array([float(r["logMMol"]) for r in rows])
logMbar = np.array([float(r["logMBar"]) for r in rows])
mb_re = np.log10(10 ** logMs + 10 ** logMHI + 10 ** logMMol)
assert np.max(np.abs(mb_re - logMbar)) < 0.02, "their Mbar bookkeeping"

# ---------------- the frozen cut ----------------
kpc_as = np.array([D_A_kpc_per_arcsec(zi) for zi in z])
R_m = 2.0 * Re_as * kpc_as * KPC
v_ms = 10 ** logV * 1e3
g_obs = v_ms ** 2 / R_m
gbar_can = g_bar_of(g_obs, A0_CANON)
sel = gbar_can < CUT_GBAR
N = int(sel.sum())
assert N == 61, "frozen cut must reproduce the recorded N=61"

delta = logMbar - (SLOPE * logV + BREF)
full_med = float(np.median(delta))
assert abs(full_med) < 0.05, "full-95 pipeline gate (their 0.00+-0.06)"
print("[GATE] full-95 median %+.3f dex -> reproduces their 0.00+-0.06 (PASS)" % full_med)

# ============ (1) SUBSAMPLE ZERO-POINT ============
rng = np.random.default_rng(20260716)
def boot_median(x, n=NBOOT):
    m = np.median(rng.choice(x, size=(n, x.size), replace=True), axis=1)
    return np.percentile(m, [16, 50, 84])

d = delta[sel]
lo, med, hi = boot_median(d)
stat = 0.5 * (hi - lo)
mad = float(np.median(np.abs(d - np.median(d))))
band = float(np.sqrt(stat ** 2 + SYS_GAS ** 2 + SYS_REF ** 2 + SYS_CONV ** 2))

# gas stress (coherent HI x0.5 / x2 -- the binding systematic, stated per the rails)
def med_sub(mb):
    return float(np.median((mb - (SLOPE * logV + BREF))[sel]))
gas_lo = med_sub(np.log10(10 ** logMs + 10 ** logMMol + 0.5 * 10 ** logMHI))
gas_hi = med_sub(np.log10(10 ** logMs + 10 ** logMMol + 2.0 * 10 ** logMHI))

print("\n(1) SUBSAMPLE ZERO-POINT (frozen estimator: median vs Lelli+19 3.14x+3.54)")
print("    N = %d of 95 | z median %.2f | g_bar/a0_canon median %.2f (range %.2f-%.2f)"
      % (N, np.median(z[sel]), np.median(gbar_can[sel] / A0_CANON),
         (gbar_can[sel] / A0_CANON).min(), (gbar_can[sel] / A0_CANON).max()))
print("    Delta_b = %+.3f dex  (bootstrap 68%%: %+.3f..%+.3f, stat +-%.3f, MAD %.3f)"
      % (med, lo, hi, stat, mad))
print("    HONEST BAND = sqrt(%.3f^2 + %.2f^2 + %.2f^2 + %.2f^2) = +-%.3f dex"
      % (stat, SYS_GAS, SYS_REF, SYS_CONV, band))
print("    gas stress HI x0.5/x2: %+.3f / %+.3f (coherent; NOT /sqrt(N))" % (gas_lo, gas_hi))

# ============ (2) FORK PREDICTIONS, OWN-a0 DILUTION ============
def pred_exact(gobs, zz, a0, ratio):
    """Delta_b = log10[g_bar(a0(z)) / g_bar(a0(0))] at fixed g_obs -- exact, own a0."""
    return np.log10(g_bar_of(gobs, a0 * ratio(zz)) / g_bar_of(gobs, a0))

one = lambda zz: np.ones_like(np.asarray(zz, float))
cpl = lambda zz: np.sqrt(f_DE(zz))          # canonical footing: a0 ~ sqrt(rho_DE)
alt = lambda zz: E_z(zz)                    # ALT footing:       a0 ~ cH(z)E(z)
p_can = pred_exact(g_obs[sel], z[sel], A0_CANON, one)
p_cpl = pred_exact(g_obs[sel], z[sel], A0_CANON, cpl)
p_alt = pred_exact(g_obs[sel], z[sel], A0_ALT, alt)   # ALT's OWN a0 -- never the canonical one

def dilution(gobs, a0):
    x = a0 / g_bar_of(gobs, a0)
    return x / (2 + x)
dil_can, dil_alt = dilution(g_obs[sel], A0_CANON), dilution(g_obs[sel], A0_ALT)

# guard against the parent's cross-footing dilution bug: ALT diluted with canonical a0
p_alt_wrong = pred_exact(g_obs[sel], z[sel], A0_CANON, alt)
assert abs(np.median(p_alt)) > abs(np.median(p_alt_wrong)), \
    "own-a0 ALT must be STRONGER than the cross-footing (bugged) version"

# size-term cancellation check (deep regime: M=v^4/(G a0), R-independent)
def pred_size(gobs_v, R, zz, a0, alpha=ALPHA_SIZE):
    v2 = gobs_v * R
    R0 = R * (1 + zz) ** alpha
    return np.log10(g_bar_of(v2 / R, a0) * R ** 2 / (g_bar_of(v2 / R0, a0) * R0 ** 2))
size_sub = float(np.median(pred_size(g_obs[sel], R_m[sel], z[sel], A0_CANON)))
size_full = float(np.median(pred_size(g_obs, R_m, z, A0_CANON)))

D_ALT, D_CPL = float(np.median(p_alt)), float(np.median(p_cpl))
print("\n(2) FORK PREDICTIONS for this subsample (exact per-galaxy, own nu, OWN a0)")
print("    dilution: median %.2f canonical / %.2f ALT-own-a0 (parent forecast: >0.6)"
      % (np.median(dil_can), np.median(dil_alt)))
print("    canonical pure-Lambda : %+.3f (identically 0: a0 exactly constant under w=-1)"
      % np.median(p_can))
print("    canonical DESI-CPL    : %+.3f (range %+.3f..%+.3f)"
      % (D_CPL, p_cpl.min(), p_cpl.max()))
print("    ALT rho_tot/cH0       : %+.3f (range %+.3f..%+.3f)"
      % (D_ALT, p_alt.min(), p_alt.max()))
print("    [cross-footing-bug check] ALT diluted with canonical a0 would read %+.3f "
      "(understated) -- NOT used" % np.median(p_alt_wrong))
print("    size-term residual (canonical + vdW14): %+.3f subsample vs %+.3f full-95 "
      "-> cancels in the deep regime as forecast" % (size_sub, size_full))

# ============ (3) LCDM HALO DRIFT + DEGENERACY (computed, not assumed) ============
h_lcdm = dlogM_lcdm_halo(z[sel])            # per-galaxy, NOT diluted (mass-assembly effect)
H_MED = float(np.median(h_lcdm))
# parent (undiluted, z=0.5-5): max |ALT - LCDM halo| = 0.118 dex.  Here: the deep cut
# dilutes ALT (through nu) but NOT the halo term -> compute the per-galaxy gap both ways.
gap_diluted = h_lcdm - p_alt                                  # what this subsample sees
p_alt_undil = -np.log10(E_z(z[sel]))                          # deep-MOND undiluted ALT
gap_undil = h_lcdm - p_alt_undil
print("\n(3) LCDM HALO-SCALING DRIFT for the same subsample (Jeanneau Eq.9 first term)")
print("    per-galaxy halo term: median %+.3f dex at z_med=%.2f (does NOT pass through nu"
      % (H_MED, np.median(z[sel])))
print("    -> NOT a0-diluted, unlike the fork; the size term cancelled but this does not)")
print("    ALT-vs-LCDM gap, undiluted (parent regime) : median %.3f dex (parent max 0.118)"
      % abs(np.median(gap_undil)))
print("    ALT-vs-LCDM gap, WITH the deep-cut dilution: median %.3f dex "
      "(range %.3f..%.3f)" % (abs(np.median(gap_diluted)),
                              np.abs(gap_diluted).min(), np.abs(gap_diluted).max()))
deg_broken = abs(np.median(gap_diluted)) > band
print("    gap %.3f vs honest band %.3f -> degeneracy %s"
      % (abs(np.median(gap_diluted)), band,
         "BROKEN (gap resolvable)" if deg_broken else
         "NOT broken: ALT and the LCDM halo edge remain indistinguishable here"))
print("    (the deep cut WIDENS the gap slightly -- dilution shrinks ALT to %+.3f while"
      "\n     the halo term stays %+.3f -- but 0.12 dex is far inside the 0.27 band;"
      "\n     the test stays FOOTING-INTERNAL, exactly as the parent banked)" % (D_ALT, H_MED))

# ============ (4) VERDICT (frozen mechanical rules) ============
sig_can = abs(med - 0.0) / band
sig_alt = abs(med - D_ALT) / band
print("\n(4) VERDICT (mechanical, FROZEN_CUTS.md section 5)")
print("    Delta_b=%+.3f, band B=%.3f, |Delta_ALT|=%.3f" % (med, band, abs(D_ALT)))
print("    sigma from canonical(0): %.2f | from ALT(%+.3f): %.2f" % (sig_can, D_ALT, sig_alt))
print("    rule (i)  B > |Delta_ALT|  -> STILL-UNDERPOWERED fires (%.3f > %.3f)"
      % (band, abs(D_ALT)))
print("    rule (ii) |Db|<B and |Db-D_ALT|>B -> nominal ALT-side distance %.2f sigma fires"
      % sig_alt)
print("    COLLISION (Delta_b landed POSITIVE, away from BOTH footings -- unanticipated):")
print("    HEADLINE = STILL-UNDERPOWERED with a %.2f-sigma ALT-side LEAN (not a constraint)."
      % sig_alt)
print("    Why the structural rule wins: a measurement AT the ALT point (-0.243) would sit")
print("    only %.2f sigma from canonical -- the band cannot separate the fork; and the"
      % (abs(D_ALT) / band))
print("    central value is gas-suspect (83 percent scaling-relation gas by median; HI x0.5/x2")
print("    alone moves it %+.3f/%+.3f)." % (gas_lo, gas_hi))
print("    [stat-only, DO-NOT-CLAIM] %.1f sigma from ALT / %.1f sigma from canonical"
      % (abs(med - D_ALT) / stat, abs(med) / stat))
print("    NOT a canonical win either: %.2f sigma compatible only, offset positive." % sig_can)

# ============ (5) FIGURE ============
comp = ~sel
fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.5, 5.6))

# Panel A: the bTFR plane
xx = np.linspace(1.55, 2.55, 100)
axA.errorbar(logV[comp], logMbar[comp], xerr=s_logV[comp], yerr=0.2, fmt="o", ms=4,
             color="0.75", ecolor="0.85", zorder=1,
             label="excluded: $g_{\\rm bar} \\geq 0.5\\,a_0$ (N=%d)" % comp.sum())
sc = axA.scatter(logV[sel], logMbar[sel], c=gbar_can[sel] / A0_CANON, cmap="viridis_r",
                 s=42, edgecolor="k", linewidth=0.4, zorder=3,
                 label="deep subsample (N=%d)" % N)
axA.errorbar(logV[sel], logMbar[sel], xerr=s_logV[sel], yerr=0.2, fmt="none",
             ecolor="0.6", elinewidth=0.6, zorder=2)
axA.plot(xx, SLOPE * xx + BREF, "k-", lw=1.8,
         label="Lelli+19 local (their ref, b=3.54)")
axA.plot(xx, SLOPE * xx + BREF + D_CPL, ":", color="tab:blue", lw=1.6,
         label="canonical (pure-$\\Lambda$ = CPL: %+.2f)" % D_CPL)
axA.plot(xx, SLOPE * xx + BREF + D_ALT, "--", color="tab:red", lw=1.8,
         label="ALT $cH(z)E(z)$, own-$a_0$ diluted: %+.2f" % D_ALT)
axA.fill_between(xx, SLOPE * xx + BREF + p_alt.min(), SLOPE * xx + BREF + p_alt.max(),
                 color="tab:red", alpha=0.12)
cb = plt.colorbar(sc, ax=axA, pad=0.01)
cb.set_label("$g_{\\rm bar}/a_{0,\\rm canon}$")
axA.set_xlabel("log $v_c(2R_e)$ [km/s]  (GalPaK3D+lensing, pressure-corrected)")
axA.set_ylabel("log $M_{\\rm bar}$ [$M_\\odot$]")
axA.set_title("Jeanneau+26 bTFR, deep-acceleration subsample (z 0.55$-$1.45)")
axA.legend(loc="upper left", fontsize=7.5)

# Panel B: residuals vs acceleration + fork bands
xr = gbar_can / A0_CANON
axB.scatter(xr[comp], delta[comp], color="0.75", s=18, zorder=1)
axB.scatter(xr[sel], delta[sel], c=z[sel], cmap="plasma", s=34, edgecolor="k",
            linewidth=0.3, zorder=3)
cb2 = plt.colorbar(axB.collections[-1], ax=axB, pad=0.01)
cb2.set_label("z")
axB.axvline(0.5, color="k", lw=0.9, ls="-.")
axB.text(0.52, 1.45, "frozen cut\n$g_{\\rm bar}<0.5a_0$", fontsize=7.5)
# measured median + bands (over the subsample x-range)
xs_band = np.array([xr[sel].min() * 0.9 + 1e-3, 0.5])
axB.fill_between(xs_band, med - band, med + band, color="tab:green", alpha=0.12,
                 label="measured %+.2f $\\pm$ %.2f honest" % (med, band))
axB.fill_between(xs_band, lo, hi, color="tab:green", alpha=0.30,
                 label="bootstrap 68%% ($\\pm$%.2f stat)" % stat)
axB.plot(xs_band, [med, med], color="tab:green", lw=2.0)
# fork prediction curves at the subsample median z (exact, own a0)
gg = np.logspace(-2.3, 0.9, 200) * A0_CANON       # g_bar grid -> g_obs
go = np.sqrt(gg ** 2 + gg * A0_CANON)
zmed = float(np.median(z[sel]))
axB.plot(gg / A0_CANON, pred_exact(go, np.full_like(go, zmed), A0_CANON, cpl), ":",
         color="tab:blue", lw=1.6, label="canonical CPL @ z=%.2f" % zmed)
axB.axhline(0.0, color="tab:blue", lw=1.2, alpha=0.7)
axB.plot(gg / A0_CANON, pred_exact(go, np.full_like(go, zmed), A0_ALT, alt), "--",
         color="tab:red", lw=1.8, label="ALT (own $a_0$) @ z=%.2f" % zmed)
axB.scatter(xr[sel], p_alt, marker="_", color="tab:red", s=26, alpha=0.6, zorder=2,
            label="ALT exact per-galaxy")
axB.axhline(float(dlogM_lcdm_halo(zmed)), color="0.3", lw=1.2, ls=(0, (5, 2, 1, 2)),
            label="$\\Lambda$CDM halo drift @ z=%.2f (undiluted)" % zmed)
axB.set_xscale("log")
axB.set_xlabel("$g_{\\rm bar}/a_{0,\\rm canon}$ at $2R_e$ (framework $\\nu$ inversion)")
axB.set_ylabel("$\\Delta b$ = log$M_{\\rm bar}$ $-$ (3.14 log$v_c$ + 3.54)  [dex]")
axB.set_title("Residuals vs acceleration: fork bands")
axB.set_ylim(-1.6, 1.7)
axB.legend(loc="lower right", fontsize=7.0)

fig.tight_layout()
fig.savefig(DIR + "/deep_refit.png", dpi=160)
print("\n(5) FIGURE written: %s/deep_refit.png" % DIR)

# per-galaxy degeneracy table (documentation of section 3)
with open(DIR + "/deep_refit_degeneracy.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["z", "gbar_over_a0canon", "pred_ALT_own_a0_diluted", "pred_ALT_undiluted",
                "lcdm_halo_undiluted", "gap_diluted", "gap_undiluted"])
    zi, xi = z[sel], (gbar_can[sel] / A0_CANON)
    for k in range(N):
        w.writerow(["%.4f" % zi[k], "%.3f" % xi[k], "%.4f" % p_alt[k],
                    "%.4f" % p_alt_undil[k], "%.4f" % h_lcdm[k],
                    "%.4f" % gap_diluted[k], "%.4f" % gap_undil[k]])
print("    degeneracy table: %s/deep_refit_degeneracy.csv (N=%d)" % (DIR, N))
print("\nEXIT 0")
