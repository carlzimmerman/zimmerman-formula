#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A7 -- pre-registered n=1 vs n=2 discriminator on SPARC (see FROZEN_CRITERIA.md, frozen
2026-10-21T21:28:48Z before any chi^2 in this lane was computed).

Laws (g = total acceleration, gN = baryonic acceleration, a0 fixed per footing):
  n=1 canonical : gN = g^2/(g+a0)      =>  g = (gN/2)(1 + sqrt(1 + 4 a0/gN))
  n=2 a0-line   : g^2 - gN^2 = a0 gN   =>  g = sqrt(gN^2 + a0 gN)

Baryonic source, identical for both laws and both footings:
  Vbar^2(U) = Vgas^2 + U*(Vdisk^2 + Vbul^2)   [km^2/s^2]
  gN        = Vbar^2 * 1e6 / r_m              [m/s^2]
One free parameter per galaxy: a single stellar Upsilon at 3.6 micron applied to disk and
bulge alike, U in [0.05, 2.50]. Error model sigma^2 = errV^2 + (0.05 Vobs)^2. Chi^2 in
velocity space. Decision rule (frozen): |dchi2_tot| >= 9 kills the disfavoured law at 3 sigma,
and only if both footings agree in sign.

Usage:
  python3 a7_checks.py            # primary run -> a7_results.json
  python3 a7_checks.py --mutate   # laws swapped    -> a7_results_MUTATE.json (sign must flip)
"""
import sys, os, json, glob, math
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import binomtest, spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(ROOT, "real_research", "data", "sparc_data")
MUT = "--mutate" in sys.argv

# ---- constants (BRIEF section 4; external inputs, not fitted) ---------------------------------
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}       # m/s^2
KPC_M = 3.0856775814913673e19                       # m per kpc
FLOOR = 0.05                                        # 5% of Vobs added in quadrature
UMIN, UMAX = 0.05, 2.50
NG = 400                                            # log10 U grid points (primary)

OUT = []


def P(s=""):
    print(s)
    OUT.append(s)


# ---- laws -------------------------------------------------------------------------------------
def g_n1(gN, a0):
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * a0 * gN))


def g_n2(gN, a0):
    return np.sqrt(gN * gN + a0 * gN)


LAWF = {"n1": g_n1, "n2": g_n2}
# The mutation swaps which physical law carries which label. Everything downstream (fits,
# totals, Upsilon distributions, forecast) is computed from this mapping, so a real relabel
# happens through the identical code path.
ASSIGN = {"n1": "n1", "n2": "n2"}
if MUT:
    ASSIGN = {"n1": "n2", "n2": "n1"}
INV = {ASSIGN[l]: l for l in ASSIGN}      # inverse map: physical law -> label carrying it


def law_of(label):
    return LAWF[ASSIGN[label]]


# ---- data -------------------------------------------------------------------------------------
def load():
    files = sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat")))
    gals, nrows = [], 0
    for f in files:
        try:
            d = np.genfromtxt(f, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        d = d[np.all(np.isfinite(d[:, :6]), axis=1)]
        nrows += d.shape[0]
        name = os.path.basename(f).replace("_rotmod.dat", "")
        R, Vobs, eV, Vgas, Vdisk, Vbul = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
        Vgas2 = Vgas ** 2
        Vstar2 = Vdisk ** 2 + Vbul ** 2
        # frozen point selection: identical for both laws / footings / all U
        keep = (Vobs > 0) & (eV > 0) & ((Vgas2 + UMIN * Vstar2) > 0) & (R > 0)
        gals.append(dict(name=name, R=R[keep], Vobs=Vobs[keep], eV=eV[keep],
                         Vgas2=Vgas2[keep], Vstar2=Vstar2[keep],
                         Vdisk2=Vdisk[keep] ** 2, Vbul2=Vbul[keep] ** 2,
                         n=int(keep.sum())))
    return gals, len(files), nrows


def prep(g):
    g["rm"] = g["R"] * KPC_M
    g["sig"] = np.sqrt(g["eV"] ** 2 + (FLOOR * g["Vobs"]) ** 2)
    return g


# ---- chi^2 ------------------------------------------------------------------------------------
def chi2_grid(U, g, law, a0, Vgas2=None, Vstar2=None, sig=None):
    """U: (m,) array; g: galaxy dict; returns (m,) chi^2."""
    vg = g["Vgas2"] if Vgas2 is None else Vgas2
    vs = g["Vstar2"] if Vstar2 is None else Vstar2
    sg = g["sig"] if sig is None else sig
    Vbar2 = vg[None, :] + U[:, None] * vs[None, :]
    Vbar2 = np.maximum(Vbar2, 0.0)
    gN = Vbar2 * 1e6 / g["rm"][None, :]
    gp = law(gN, a0)
    Vp = np.sqrt(np.maximum(gp, 0.0) * g["rm"][None, :]) / 1e3
    r = (g["Vobs"][None, :] - Vp) / sg[None, :]
    return np.sum(r * r, axis=1)


def fit(g, law, a0, ngrid=NG, Vgas2=None, Vstar2=None, sig=None, mask=None):
    """Deterministic global scan + bounded Brent. Returns dict."""
    gg = dict(g)
    if mask is not None:
        for k in ("Vobs", "eV", "Vgas2", "Vstar2", "rm", "sig"):
            gg[k] = g[k][mask]
        Vgas2 = Vstar2 = sig = None
    if Vgas2 is not None:
        gg["Vgas2"] = Vgas2
    if Vstar2 is not None:
        gg["Vstar2"] = Vstar2
    if sig is not None:
        gg["sig"] = sig
    g = gg
    Ug = np.logspace(math.log10(UMIN), math.log10(UMAX), ngrid)
    c = chi2_grid(Ug, g, law, a0)
    i = int(np.argmin(c))
    cbf, Ubf = float(c[i]), float(Ug[i])
    lo = Ug[max(i - 1, 0)]; hi = Ug[min(i + 1, ngrid - 1)]
    if hi > lo:
        res = minimize_scalar(lambda lu: float(chi2_grid(np.array([10.0 ** lu]), g, law, a0)[0]),
                              bounds=(math.log10(lo), math.log10(hi)), method="bounded",
                              options={"xatol": 1e-10})
        if res.fun <= cbf:
            cbf, Ubf = float(res.fun), float(10.0 ** res.x)
    at_edge = (abs(Ubf - UMIN) <= 1e-6 * UMIN) or (abs(Ubf - UMAX) <= 1e-6 * UMAX)
    return dict(chi2=cbf, U=Ubf, edge=bool(at_edge), nmax=len(g["Vobs"]))


def vpred(U, g, law, a0):
    Vbar2 = g["Vgas2"] + U * g["Vstar2"]
    gN = np.maximum(Vbar2, 0.0) * 1e6 / g["rm"]
    return np.sqrt(np.maximum(law(gN, a0), 0.0) * g["rm"]) / 1e3


# ===============================================================================================
gal, nfiles, nrows = load()
gal = [prep(g) for g in gal]
gal_fit = [g for g in gal if g["n"] >= 5]
ndrop = len(gal) - len(gal_fit)
npts = int(sum(g["n"] for g in gal_fit))

P("A7: pre-registered n=1 vs n=2 discriminator on SPARC" + ("   *** MUTATE: LAWS SWAPPED ***" if MUT else ""))
P("Frozen criteria: FROZEN_CRITERIA.md (2026-10-21T21:28:48Z). Constants: a0_can 9.36e-11, a0_alt 1.13e-10 m/s^2;")
P("KPC=3.0856775814913673e19 m; U in [%.2f,%.2f] one per galaxy (disk=bulge); sigma^2=errV^2+(0.05 Vobs)^2." % (UMIN, UMAX))

# ---------- K1: data integrity -----------------------------------------------------------------
ok1 = (nfiles == 175 and nrows == 3391 and len(gal_fit) >= 165)
P("K1 %s nfiles=%d nrows=%d ngal>=5=%d (dropped %d) npts=%d | threshold 175 files, 3391 rows, >=165 galaxies"
  % ("PASS" if ok1 else "FAIL", nfiles, nrows, len(gal_fit), ndrop, npts))

# ---------- K2: law algebra --------------------------------------------------------------------
yy = 1e-8
gN0 = yy
r1 = (g_n1(gN0, 1.0) ** 2) / (g_n1(gN0, 1.0) + 1.0)          # round trip n=1 with a0=1
r2 = (g_n2(gN0, 1.0) ** 2 - gN0 ** 2) / gN0                  # round trip n=2
deep = abs(g_n1(gN0, 1.0) / g_n2(gN0, 1.0) - 1.0)
hi = 1e4
anom = (g_n1(hi, 1.0) - hi) / (g_n2(hi, 1.0) - hi)
ok2 = (abs(r1 - gN0) < 1e-12 and abs(r2 - 1.0) < 1e-12 and deep < 1e-3 and abs(anom - 2.0) < 1e-3)
P("K2 %s roundtrip_n1=%.3e roundtrip_n2=%.3e deep|g1/g2-1|@y=1e-8=%.2e anomaly_ratio@y=1e4=%.6f | thresholds 1e-12,1e-12,1e-3,|r-2|<1e-3"
  % ("PASS" if ok2 else "FAIL", abs(r1 - gN0), abs(r2 - 1.0), deep, anom))

# ---------- main fits --------------------------------------------------------------------------
def run_fits(ngrid=NG, mode="primary"):
    """mode: primary | nobs_floor | m2l14 | fixed05 | transition"""
    res = {}
    for foot, a0 in A0.items():
        for lab in ("n1", "n2"):
            law = law_of(lab)
            rows = []
            for g in gal_fit:
                if mode == "m2l14":
                    vs = g["Vdisk2"] + 1.4 * g["Vbul2"]
                    f = fit(g, law, a0, ngrid, g["Vgas2"], vs, g["sig"])
                elif mode == "nobs_floor":
                    sg = g["eV"].copy()
                    f = fit(g, law, a0, ngrid, None, None, sg)
                elif mode == "fixed05":
                    f = fit(g, law, a0, ngrid)
                elif mode == "transition":
                    y = (g["Vgas2"] + 0.5 * g["Vstar2"]) * 1e6 / g["rm"] / a0
                    m = (y >= 0.1) & (y <= 3.0)
                    if m.sum() < 3:
                        f = dict(chi2=np.nan, U=np.nan, edge=False, nmax=int(m.sum()))
                    else:
                        f = fit(g, law, a0, ngrid, mask=m)
                else:
                    f = fit(g, law, a0, ngrid)
                f["name"] = g["name"]
                rows.append(f)
            res[(foot, lab)] = rows
    return res


FIT = run_fits()

# ---------- K3: local optimality ----------------------------------------------------------------
bad = 0
for foot, a0 in A0.items():
    for lab in ("n1", "n2"):
        law = law_of(lab)
        for g, f in zip(gal_fit, FIT[(foot, lab)]):
            if f["edge"] or not np.isfinite(f["U"]):
                continue
            for fac in (1.02, 0.98):
                U2 = f["U"] * fac
                if U2 < UMIN or U2 > UMAX:
                    continue
                c2 = float(chi2_grid(np.array([U2]), g, law, a0)[0])
                if c2 < f["chi2"] - 1e-9:
                    bad += 1
P("K3 %s interior best fits locally minimal (violations=%d) | threshold 0"
  % ("PASS" if bad == 0 else "FAIL", bad))

# ---------- totals, wins, distribution ----------------------------------------------------------
NUM = {}
for foot in A0:
    c1 = np.array([f["chi2"] for f in FIT[(foot, "n1")]])
    c2 = np.array([f["chi2"] for f in FIT[(foot, "n2")]])
    d = c2 - c1
    u1 = np.array([f["U"] for f in FIT[(foot, "n1")]])
    u2 = np.array([f["U"] for f in FIT[(foot, "n2")]])
    e1 = np.array([f["edge"] for f in FIT[(foot, "n1")]])
    e2 = np.array([f["edge"] for f in FIT[(foot, "n2")]])
    n2wins = int((d < 0).sum()); n1wins = int((d > 0).sum()); ties = int((d == 0).sum())
    bt = binomtest(n2wins, n2wins + n1wins, 0.5)
    rng = np.random.default_rng(20261021)
    idx = rng.integers(0, len(d), size=(10000, len(d)))
    sb = d[idx].sum(axis=1).std(ddof=1)
    NUM[foot] = dict(
        chi2_n1=float(c1.sum()), chi2_n2=float(c2.sum()), dchi2=float(d.sum()),
        n1_wins=n1wins, n2_wins=n2wins, ties=ties, ngal=len(d),
        sign_p=float(bt.pvalue), boot_sd=float(sb),
        z_boot=float(d.sum() / sb) if sb > 0 else float("nan"),
        dchi2_pct={q: float(np.percentile(d, q)) for q in (5, 16, 25, 50, 75, 84, 95)},
        dchi2_mean=float(d.mean()), dchi2_std=float(d.std(ddof=1)),
        dchi2_min=float(d.min()), dchi2_max=float(d.max()),
        dchi2_hist=dict(edges=[-1e9, -50, -20, -9, -3, -1, 0, 1, 3, 9, 20, 50, 1e9],
                        counts=[int(x) for x in np.histogram(d, bins=[-1e9, -50, -20, -9, -3, -1, 0, 1, 3, 9, 20, 50, 1e9])[0]]),
        U1_med=float(np.median(u1)), U2_med=float(np.median(u2)),
        U1_mean=float(u1.mean()), U2_mean=float(u2.mean()),
        U1_min=float(u1.min()), U1_max=float(u1.max()),
        U2_min=float(u2.min()), U2_max=float(u2.max()),
        U1_p16=float(np.percentile(u1, 16)), U1_p84=float(np.percentile(u1, 84)),
        U2_p16=float(np.percentile(u2, 16)), U2_p84=float(np.percentile(u2, 84)),
        U1_in_phys=float(((u1 >= 0.1) & (u1 <= 1.0)).mean()),
        U2_in_phys=float(((u2 >= 0.1) & (u2 <= 1.0)).mean()),
        U1_edge=float(e1.mean()), U2_edge=float(e2.mean()),
        U1_edge_lo=float((u1 <= UMIN * 1.000001).mean()), U1_edge_hi=float((u1 >= UMAX * 0.999999).mean()),
        U2_edge_lo=float((u2 <= UMIN * 1.000001).mean()), U2_edge_hi=float((u2 >= UMAX * 0.999999).mean()),
        frac_U_shift_gt20=float((np.abs(u2 / u1 - 1.0) > 0.20).mean()),
        n_absdchi2_lt1=int((np.abs(d) < 1).sum()), n_absdchi2_lt3=int((np.abs(d) < 3).sum()),
        dchi2_share_edge_lo=float(np.abs(d[(u1 <= UMIN * 1.000001) | (u2 <= UMIN * 1.000001)]).sum() / np.abs(d).sum()),
    )
    # per-galaxy table kept for the residual stage
    NUM[foot]["_U1"] = u1; NUM[foot]["_U2"] = u2; NUM[foot]["_d"] = d

# ---------- K4: arithmetic ---------------------------------------------------------------------
a4 = all(abs(NUM[f]["dchi2"] - NUM[f]["_d"].sum()) < 1e-8 and
         NUM[f]["n1_wins"] + NUM[f]["n2_wins"] + NUM[f]["ties"] == NUM[f]["ngal"] for f in A0)
P("K4 %s sum(dchi2_g)=dchi2_tot and wins sum to ngal | threshold 1e-8"
  % ("PASS" if a4 else "FAIL"))

P("")
P("=== PRIMARY: total chi^2 (a single Upsilon per galaxy, both laws, each footing separately) ===")
for foot in A0:
    n = NUM[foot]
    P("  [%s] a0=%.3e  chi2_n1=%.2f  chi2_n2=%.2f  dchi2(n2-n1)=%+.3f  |  n1 wins %d  n2 wins %d  ties %d of %d"
      % (foot, A0[foot], n["chi2_n1"], n["chi2_n2"], n["dchi2"], n["n1_wins"], n["n2_wins"], n["ties"], n["ngal"]))
    P("        per-galaxy dchi2: median %+.3f  mean %+.3f  sd %.3f  [p5 %+.3f, p95 %+.3f, min %+.3f, max %+.3f]"
      % (n["dchi2_pct"][50], n["dchi2_mean"], n["dchi2_std"], n["dchi2_pct"][5], n["dchi2_pct"][95],
         n["dchi2_min"], n["dchi2_max"]))
    P("        sign test p=%.3g ; bootstrap sd of total %.2f -> z=%+.2f"
      % (n["sign_p"], n["boot_sd"], n["z_boot"]))
    P("        histogram (dchi2_g): <-50 %d | -50..-20 %d | -20..-9 %d | -9..-3 %d | -3..-1 %d | -1..0 %d | 0..1 %d | 1..3 %d | 3..9 %d | 9..20 %d | 20..50 %d | >50 %d"
      % tuple(n["dchi2_hist"]["counts"]))
    P("        Upsilon: n1 median %.3f [p16 %.3f, p84 %.3f] range [%.3f,%.3f], in [0.1,1]: %.0f%%, at edge %.1f%%"
      % (n["U1_med"], n["U1_p16"], n["U1_p84"], n["U1_min"], n["U1_max"], 100 * n["U1_in_phys"], 100 * n["U1_edge"]))
    P("                  n2 median %.3f [p16 %.3f, p84 %.3f] range [%.3f,%.3f], in [0.1,1]: %.0f%%, at edge %.1f%%"
      % (n["U2_med"], n["U2_p16"], n["U2_p84"], n["U2_min"], n["U2_max"], 100 * n["U2_in_phys"], 100 * n["U2_edge"]))
    P("        edge split: n1 %.1f%% low / %.1f%% high ; n2 %.1f%% low / %.1f%% high ; |U2/U1-1|>20%% in %.0f%% of galaxies"
      % (100 * n["U1_edge_lo"], 100 * n["U1_edge_hi"], 100 * n["U2_edge_lo"], 100 * n["U2_edge_hi"],
         100 * n["frac_U_shift_gt20"]))
    P("        galaxies stuck at the LOW Upsilon edge contribute %.0f%% of sum|dchi2_g| (their Upsilon is unconstrained: gas-dominated)"
      % (100 * n["dchi2_share_edge_lo"]))

# ---------- reported diagnostics: fit quality and concentration of the total --------------------
DIAG = {}
names = [g["name"] for g in gal_fit]
dof = npts - len(gal_fit)
for foot in A0:
    d = np.asarray(NUM[foot]["_d"], dtype=float)
    order = np.argsort(-np.abs(d))
    DIAG[foot] = dict(
        chi2_dof_n1=float(NUM[foot]["chi2_n1"] / dof),
        chi2_dof_n2=float(NUM[foot]["chi2_n2"] / dof),
        top5=[[names[i], float(d[i])] for i in order[:5]],
        top5_abs_share=float(np.abs(d[order[:5]]).sum() / np.abs(d).sum()),
        dchi2_drop_top5=float(d.sum() - d[order[:5]].sum()),
        n_absdchi2_lt1=int((np.abs(d) < 1).sum()), n_absdchi2_lt3=int((np.abs(d) < 3).sum()),
        U2_over_U1_med=float(np.median(NUM[foot]["_U2"] / NUM[foot]["_U1"])),
        n_edge_any=int(np.sum((NUM[foot]["_U1"] <= UMIN * 1.000001) | (NUM[foot]["_U2"] <= UMIN * 1.000001) |
                              (NUM[foot]["_U1"] >= UMAX * 0.999999) | (NUM[foot]["_U2"] >= UMAX * 0.999999))),
        dchi2_excl_edge=float(d[~((NUM[foot]["_U1"] <= UMIN * 1.000001) | (NUM[foot]["_U2"] <= UMIN * 1.000001) |
                                  (NUM[foot]["_U1"] >= UMAX * 0.999999) | (NUM[foot]["_U2"] >= UMAX * 0.999999))].sum()),
    )
    P("        fit quality: chi2/dof = %.2f (n1) / %.2f (n2), dof=%d; Upsilon(n2)/Upsilon(n1) median = %.3f"
      % (DIAG[foot]["chi2_dof_n1"], DIAG[foot]["chi2_dof_n2"], dof, DIAG[foot]["U2_over_U1_med"]))
    P("        5 largest |dchi2_g| carry %.0f%% of the total: " % (100 * DIAG[foot]["top5_abs_share"]) +
      ", ".join("%s %+.1f" % (n, v) for n, v in DIAG[foot]["top5"]) +
      " ; dchi2 dropping them = %+.1f" % DIAG[foot]["dchi2_drop_top5"])
    P("        %d galaxies touch a Upsilon bound; dchi2 excluding all of them = %+.1f"
      % (DIAG[foot]["n_edge_any"], DIAG[foot]["dchi2_excl_edge"]))
    P("        |dchi2_g|<1 in %d/%d galaxies, <3 in %d/%d"
      % (DIAG[foot]["n_absdchi2_lt1"], len(gal_fit), DIAG[foot]["n_absdchi2_lt3"], len(gal_fit)))

FOOTPREF = dict(
    dchi2_n1_alt_minus_can=float(NUM["alt"]["chi2_n1"] - NUM["canonical"]["chi2_n1"]),
    dchi2_n2_alt_minus_can=float(NUM["alt"]["chi2_n2"] - NUM["canonical"]["chi2_n2"]),
)
P("        footing preference (alt minus canonical chi^2): n1 %+.1f, n2 %+.1f  (positive = canonical a0 preferred)"
  % (FOOTPREF["dchi2_n1_alt_minus_can"], FOOTPREF["dchi2_n2_alt_minus_can"]))

# ---------- per-galaxy table (physical laws: invariant under --mutate) --------------------------
PG = []
for j, g in enumerate(gal_fit):
    medy = float(np.median((g["Vgas2"] + 0.5 * g["Vstar2"]) * 1e6 / g["rm"] / A0["canonical"]))
    PG.append(dict(name=g["name"], n=int(g["n"]), med_y_can=medy,
                   dchi2_can=float(FIT[("canonical", INV["n2"])][j]["chi2"] - FIT[("canonical", INV["n1"])][j]["chi2"]),
                   dchi2_alt=float(FIT[("alt", INV["n2"])][j]["chi2"] - FIT[("alt", INV["n1"])][j]["chi2"]),
                   U1_can=float(FIT[("canonical", INV["n1"])][j]["U"]),
                   U2_can=float(FIT[("canonical", INV["n2"])][j]["U"]),
                   U1_alt=float(FIT[("alt", INV["n1"])][j]["U"]),
                   U2_alt=float(FIT[("alt", INV["n2"])][j]["U"])))
ys = np.array([p["med_y_can"] for p in PG])
dc = np.array([p["dchi2_can"] for p in PG]); da = np.array([p["dchi2_alt"] for p in PG])
rc = spearmanr(ys, dc); ra = spearmanr(ys, da)
low = ys < 0.1; high = ys > 1.0
CORR = dict(spearman_rho_can=float(rc.correlation), spearman_p_can=float(rc.pvalue),
            spearman_rho_alt=float(ra.correlation), spearman_p_alt=float(ra.pvalue),
            n_medy_lt_0p1=int(low.sum()), n_medy_gt_1=int(high.sum()),
            mean_dchi2_can_low=float(dc[low].mean()), mean_dchi2_can_high=float(dc[high].mean()),
            mean_dchi2_alt_low=float(da[low].mean()), mean_dchi2_alt_high=float(da[high].mean()))
P("        regime split: %d galaxies with median y<0.1 (mean dchi2: can %+.2f, alt %+.2f); %d with median y>1 (mean: can %+.2f, alt %+.2f)"
  % (CORR["n_medy_lt_0p1"], CORR["mean_dchi2_can_low"], CORR["mean_dchi2_alt_low"],
     CORR["n_medy_gt_1"], CORR["mean_dchi2_can_high"], CORR["mean_dchi2_alt_high"]))
P("        Spearman(median y, dchi2): can %+.3f (p=%.2g), alt %+.3f (p=%.2g)"
  % (CORR["spearman_rho_can"], CORR["spearman_p_can"], CORR["spearman_rho_alt"], CORR["spearman_p_alt"]))

# ---------- K7: finiteness ---------------------------------------------------------------------
fin = True
for foot in A0:
    for lab in ("n1", "n2"):
        arr = np.array([f["chi2"] for f in FIT[(foot, lab)]])
        fin = fin and np.all(np.isfinite(arr)) and np.all(arr >= 0) and len(arr) == len(gal_fit)
P("K7 %s all chi^2 finite, >=0, one fit per galaxy per law per footing | threshold all"
  % ("PASS" if fin else "FAIL"))

# ---------- K8: theory-level max velocity difference --------------------------------------------
ygr = np.logspace(-4, 4, 40001)
gg = ygr * 1.0
v1 = np.sqrt(0.5 * (1.0 + np.sqrt(1.0 + 4.0 / ygr)))     # V/Vbar at fixed baryonic source, a0=1
v2 = np.sqrt(np.sqrt(1.0 + 1.0 / ygr))
dv = np.abs(v2 / v1 - 1.0)
imax = int(np.argmax(dv))
dvmax, ymax = float(dv[imax]), float(ygr[imax])
ok8 = (0.03 <= dvmax <= 0.15) and (0.1 <= ymax <= 3.0)
P("K8 %s max|V2-V1|/V1 at fixed baryonic source = %.4f%% at gN/a0=%.3f | thresholds [3%%,15%%], y in [0.1,3]"
  % ("PASS" if ok8 else "FAIL", 100 * dvmax, ymax))
dv_alt = float(np.max(np.abs(v1 / v2 - 1.0)))     # the same difference, normalised by n=2
P("     prior lane's 7.46%%: reproduced as |V1-V2|/V2 = %.4f%% at the SAME y=%.3f (denominator n=2);"
  % (100 * dv_alt, ymax))
P("     normalised by V1 the same point is %.4f%%. 7.46%% and 6.94%% are one number, two denominators."
  % (100 * dvmax))

# ---------- stacked residuals in gN/a0 bins -----------------------------------------------------
BIN_EDGES = np.array([1e-2, 3.16e-2, 1e-1, 3.16e-1, 1.0, 3.16, 10.0, 31.6, 100.0])
BINS = []
for foot in A0:
    a0 = A0[foot]
    U1 = NUM[foot]["_U1"]; U2 = NUM[foot]["_U2"]
    # residuals at each law's own best fit
    rec = {b: dict(n=0, s1=0.0, w1=0.0, s2=0.0, w2=0.0, st=0.0, wt=0.0,
                   l1=[], l2=[], lt=[]) for b in range(len(BIN_EDGES))}
    for j, g in enumerate(gal_fit):
        V1 = vpred(U1[j], g, law_of("n1"), a0)
        V2 = vpred(U2[j], g, law_of("n2"), a0)
        d1 = (g["Vobs"] - V1) / g["Vobs"]
        d2 = (g["Vobs"] - V2) / g["Vobs"]
        # theory difference at FIXED baryonic source: canonical's own best-fit Upsilon
        V1f = vpred(U1[j], g, LAWF["n1"], a0)
        V2f = vpred(U1[j], g, LAWF["n2"], a0)
        dt = (V2f - V1f) / V1f
        gN = (g["Vgas2"] + U1[j] * g["Vstar2"]) * 1e6 / g["rm"]
        y = gN / a0
        w = 1.0 / g["sig"] ** 2
        bi = np.digitize(y, BIN_EDGES) - 1
        for k in range(len(g["Vobs"])):
            if 0 <= bi[k] < len(BIN_EDGES):
                b = rec[bi[k]]
                b["n"] += 1
                b["s1"] += w[k] * d1[k]; b["w1"] += w[k]
                b["s2"] += w[k] * d2[k]; b["w2"] += w[k]
                b["st"] += w[k] * dt[k]; b["wt"] += w[k]
                b["l1"].append(d1[k]); b["l2"].append(d2[k]); b["lt"].append(dt[k])
    rows = []
    for k in range(len(BIN_EDGES)):
        b = rec[k]
        if b["n"] == 0:
            continue
        rows.append(dict(lo=float(BIN_EDGES[k]) if k > 0 else float(1e-2),
                         hi=float(BIN_EDGES[k + 1]) if k + 1 < len(BIN_EDGES) else float(100.0),
                         n=int(b["n"]), mean_d1=float(b["s1"] / b["w1"]),
                         mean_d2=float(b["s2"] / b["w2"]), mean_theory=float(b["st"] / b["wt"]),
                         med_d1=float(np.median(b["l1"])), med_d2=float(np.median(b["l2"])),
                         med_theory=float(np.median(b["lt"]))))
    BINS.append((foot, rows))

P("")
P("=== STACKED RESIDUALS (median fractional residual (Vobs-Vmodel)/Vobs, by gN/a0) ===")
P("    bin gN/a0        npts   med d_n1   med d_n2   wmean d_n1  wmean d_n2  <dV_theory> (V2-V1)/V1")
for foot, rows in BINS:
    P("  [%s]" % foot)
    for r in rows:
        P("    %7.3f-%-7.3f %5d  %+.4f    %+.4f     %+.4f     %+.4f     %+.4f"
          % (r["lo"], r["hi"], r["n"], r["med_d1"], r["med_d2"], r["mean_d1"], r["mean_d2"], r["mean_theory"]))

# ---------- forecast ---------------------------------------------------------------------------
P("")
P("=== FORECAST: expected dchi^2 (non-centrality) under each truth ===")
FC = {}
for truth in ("n1", "n2"):
    other = "n2" if truth == "n1" else "n1"
    for foot in A0:
        a0 = A0[foot]
        lam = []
        for j, g in enumerate(gal_fit):
            Ut = FIT[(foot, truth)][j]["U"]
            Vtrue = vpred(Ut, g, law_of(truth), a0)
            gg = dict(g); gg["Vobs"] = Vtrue
            f = fit(gg, law_of(other), a0)
            lam.append(f["chi2"])
        lam = np.array(lam)
        FC[(truth, foot)] = dict(lam_tot=float(lam.sum()), lam_mean=float(lam.mean()),
                                 lam_med=float(np.median(lam)),
                                 lam_p84=float(np.percentile(lam, 84)),
                                 ntrip=float(9.0 / lam.mean()) if lam.mean() > 0 else float("inf"),
                                 err_factor=float(math.sqrt(lam.sum() / 9.0)) if lam.sum() > 0 else float("inf"))
        P("  truth=%s [%s]: lambda_tot=%.3f  mean/gxy=%.4f  median/gxy=%.4f  N(3sigma)=%.0f gxy (have %d)  errors x %.3f"
          % (truth, foot, lam.sum(), lam.mean(), np.median(lam), 9.0 / lam.mean() if lam.mean() > 0 else -1,
             len(gal_fit), math.sqrt(lam.sum() / 9.0) if lam.sum() > 0 else float("nan")))

P("")
P("=== FORECAST F2 (scatter-calibrated; POST-UNBLINDING addition, FROZEN_CRITERIA AMENDMENT 1) ===")
P("    signal per galaxy = F1 lambda_g ; noise per galaxy = measured sd of dchi2_g over SPARC")
F2 = {}
for truth in ("n1", "n2"):
    for foot in A0:
        lam = FC[(truth, foot)]["lam_mean"]
        sd = NUM[foot]["dchi2_std"]
        N3 = (3.0 * sd / lam) ** 2 if lam > 0 else float("inf")
        F2[f"{truth}|{foot}"] = dict(lam_mean=lam, sd_dchi2=sd, snr=lam / sd, N3=float(N3),
                                     N3_over_171=float(N3 / len(gal_fit)),
                                     expected_sd_model=float(2.0 * math.sqrt(1.0 + 2.0 * lam)))
        P("  truth=%s [%s]: lambda/gxy=%.4f, sd(dchi2_g)=%.2f -> per-galaxy SNR %.3f, N(3sigma)=%.0f galaxies"
          % (truth, foot, lam, sd, lam / sd, N3))

# ---------- variants ---------------------------------------------------------------------------
P("")
P("=== VARIANTS (reported, not decisive) ===")
VAR = {}
def dchi2_of(res, foot):
    c1 = np.array([f["chi2"] for f in res[(foot, "n1")]])
    c2 = np.array([f["chi2"] for f in res[(foot, "n2")]])
    return float(np.nansum(c2 - c1))


V1 = run_fits(mode="m2l14"); V2 = run_fits(mode="nobs_floor"); V5 = run_fits(mode="transition")
for nm, res in (("V1 U_bul=1.4 U_disk", V1), ("V2 no 5% floor", V2), ("V5 transition 0.1<=y<=3 (refit)", V5)):
    VAR[nm] = {foot: dchi2_of(res, foot) for foot in A0}
    P("  %-32s " % nm + "  ".join("dchi2[%s]=%+.2f" % (f, VAR[nm][f]) for f in A0))
# V4: fixed Upsilon 0.5
V4 = {}
for foot in A0:
    tot = {}
    for lab in ("n1", "n2"):
        c = np.array([float(chi2_grid(np.array([0.5]), g, law_of(lab), A0[foot])[0]) for g in gal_fit])
        tot[lab] = c.sum()
    V4[foot] = float(tot["n2"] - tot["n1"])
VAR["V4 fixed U=0.5"] = V4
VAR["V4_absorbed_frac"] = {f: float((V4[f] - NUM[f]["dchi2"]) / V4[f]) if V4[f] != 0 else None for f in A0}
P("  %-32s " % "V4 fixed U=0.5" + "  ".join("dchi2[%s]=%+.2f" % (f, V4[f]) for f in A0))

# ---------- K6: grid convergence ---------------------------------------------------------------
FIT800 = run_fits(ngrid=800)
d400 = {f: NUM[f]["dchi2"] for f in A0}
d800 = {f: dchi2_of(FIT800, f) for f in A0}
dev = max(abs(d400[f] - d800[f]) for f in A0)
ok6 = dev < 0.5
P("")
P("K6 %s dchi2(400-pt grid) vs dchi2(800-pt grid): max |diff| = %.4f | threshold 0.5" % ("PASS" if ok6 else "FAIL", dev))
P("     dchi2 400: " + " ".join("%s %+.3f" % (f, d400[f]) for f in A0))
P("     dchi2 800: " + " ".join("%s %+.3f" % (f, d800[f]) for f in A0))

# ---------- K5: mutation sign flip -------------------------------------------------------------
# FIT is keyed by LABEL; under the run's map, label L carries law ASSIGN[L]. To score an arbitrary
# label->law map from the same fits, read each law from the label that carries it in this run.
def score(foot):
    """Physical dchi2 = chi2(law n2) - chi2(law n1), read from the label that carries each law."""
    c1 = np.array([f["chi2"] for f in FIT[(foot, INV["n1"])]])
    c2 = np.array([f["chi2"] for f in FIT[(foot, INV["n2"])]])
    return float(np.sum(c2 - c1))


d_rep = {f: NUM[f]["dchi2"] for f in A0}      # label-based, what this run reports
d_swp = {f: score(f) for f in A0}             # law-based, independent of the labelling
dev5 = max(abs(d_rep[f] + d_swp[f]) for f in A0) if MUT else max(abs(d_rep[f] - d_swp[f]) for f in A0)
base = None
try:
    with open(os.path.join(HERE, "a7_results.json")) as fh:
        base = json.load(fh)
except Exception:
    base = None
dev5b = None
if MUT and base is not None:
    dev5b = max(abs(d_rep[f] + base["numbers"][f]["dchi2"]) for f in A0)
ok5 = dev5 < 1e-9 and (dev5b is None or dev5b < 1e-9)
P("K5 %s mutation=%s ; %s dchi2 %s ; %s dchi2 %s ; residual=%.2e | threshold 1e-9 (exact sign flip)"
  % ("PASS" if ok5 else "FAIL", MUT,
     "reported(label-based)" if MUT else "label-based",
     " ".join("%s %+.3f" % (f, d_rep[f]) for f in A0),
     "physical(law-based)" if MUT else "law-based (independent recompute)",
     " ".join("%s %+.3f" % (f, d_swp[f]) for f in A0), dev5))
if MUT and base is not None:
    P("     vs committed baseline a7_results.json: max |mutated + baseline| = %.2e (threshold 1e-9)" % dev5b)

# ---------- verdict ----------------------------------------------------------------------------
def verdict(d):
    if d >= 9.0:
        return "n=2 KILLED (3sigma, canonical preferred)"
    if d <= -9.0:
        return "n=1 KILLED (3sigma, n=2 preferred)"
    return "NOT DECIDED (degenerate at SPARC precision)"


VER = {f: verdict(NUM[f]["dchi2"]) for f in A0}
same = (abs(NUM["canonical"]["dchi2"]) >= 9 and abs(NUM["alt"]["dchi2"]) >= 9 and
        np.sign(NUM["canonical"]["dchi2"]) == np.sign(NUM["alt"]["dchi2"]))
P("")
P("=== VERDICT (frozen rule: |dchi2|>=9 kills; both footings must agree) ===")
for f in A0:
    P("  [%s] dchi2 = %+.3f  ->  %s   [literal rule; bootstrap says %.2f sigma from zero]"
      % (f, NUM[f]["dchi2"], VER[f], abs(NUM[f]["z_boot"])))
P("  combined: %s" % ("SPARC DECIDES n at 3sigma on both footings (same sign, both >=9)" if same else
                      "NO KILL: the two laws are not separated at 3sigma on both footings"))

# ---------- summary numbers --------------------------------------------------------------------
NUM_OUT = {}
for f in A0:
    n = {k: v for k, v in NUM[f].items() if not k.startswith("_")}
    NUM_OUT[f] = n
NUM_OUT["max_dV_frac"] = dvmax
NUM_OUT["max_dV_pct"] = 100.0 * dvmax
NUM_OUT["max_dV_frac_denom_n2"] = dv_alt
NUM_OUT["max_dV_pct_denom_n2"] = 100.0 * dv_alt
NUM_OUT["max_dV_y"] = ymax
NUM_OUT["dof"] = int(dof)
NUM_OUT["upsilon_range"] = [UMIN, UMAX]
NUM_OUT["n_boot"] = 10000
NUM_OUT["bootstrap_seed"] = 20261021
NUM_OUT["ugrid_points"] = [NG, 800]
NUM_OUT["error_floor_frac"] = FLOOR
NUM_OUT["a0_footings_m_s2"] = dict(A0)
NUM_OUT["diagnostics"] = DIAG
NUM_OUT["footing_preference"] = FOOTPREF
NUM_OUT["regime_correlation"] = CORR
NUM_OUT["per_galaxy"] = PG
NUM_OUT["dropped_galaxies"] = [g["name"] for g in gal if g["n"] < 5]
NUM_OUT["forecast_F2_scatter_calibrated"] = F2
NUM_OUT["nfiles"] = nfiles
NUM_OUT["nrows"] = nrows
NUM_OUT["ngal"] = len(gal_fit)
NUM_OUT["ngal_dropped"] = ndrop
NUM_OUT["npts"] = npts
NUM_OUT["forecast"] = {f"{t}|{f}": v for (t, f), v in FC.items()}
NUM_OUT["variants"] = VAR
NUM_OUT["bins"] = {f: rows for f, rows in BINS}
NUM_OUT["verdict"] = VER
NUM_OUT["decides_both_footings"] = bool(same)
NUM_OUT["mutation"] = bool(MUT)

checks = [
    dict(id="K1", passed=bool(ok1), value=f"{nfiles} files, {nrows} rows, {len(gal_fit)} galaxies, {npts} pts",
         threshold="175 files / 3391 rows / >=165 galaxies"),
    dict(id="K2", passed=bool(ok2), value=f"rt1={abs(r1-gN0):.1e}, rt2={abs(r2-1.0):.1e}, deep={deep:.1e}, anom={anom:.6f}",
         threshold="1e-12 / 1e-12 / 1e-3 / |anom-2|<1e-3"),
    dict(id="K3", passed=bool(bad == 0), value=f"{bad} local-optimality violations", threshold="0"),
    dict(id="K4", passed=bool(a4), value="sum and win counts consistent", threshold="1e-8"),
    dict(id="K5", passed=bool(ok5), value=f"max |label-based -+ law-based| = {dev5:.2e}" + (f", vs baseline {dev5b:.2e}" if dev5b is not None else ""),
         threshold="1e-9 exact sign flip"),
    dict(id="K6", passed=bool(ok6), value=f"max |dchi2(400)-dchi2(800)| = {dev:.4f}", threshold="0.5"),
    dict(id="K7", passed=bool(fin), value="all chi2 finite and >=0", threshold="all"),
    dict(id="K8", passed=bool(ok8), value=f"max dV/V = {100*dvmax:.4f}% at y={ymax:.3f}", threshold="[3%,15%], y in [0.1,3]"),
]
npass = sum(c["passed"] for c in checks)
P("")
P("A7 COMPLETE: %d/%d checks PASS." % (npass, len(checks)))

res = dict(lane="A7", status="NUMERICAL", mutate=bool(MUT), criteria="FROZEN_CRITERIA.md",
           checks=[dict(id=c["id"], **{"pass": bool(c["passed"])}, passed=bool(c["passed"]),
                        value=c["value"], threshold=c["threshold"]) for c in checks],
           numbers=NUM_OUT,
           constants_used=[
               "a0_canonical = 9.36e-11 m/s^2 (BRIEF section 4)",
               "a0_alt = 1.13e-10 m/s^2 (BRIEF section 4)",
               "kpc = 3.0856775814913673e19 m (BRIEF section 4: 1 pc = 3.0856775814913673e16 m)",
               "G = 6.67430e-11 (not used: fit is in acceleration space)",
               "error floor = 0.05*Vobs (declared)",
               "Upsilon range [0.05, 2.50] (declared)",
               "n=2 mock bootstrap seed 20261021 (declared)",
           ])
fn = "a7_results_MUTATE.json" if MUT else "a7_results.json"
with open(os.path.join(HERE, fn), "w") as fh:
    json.dump(res, fh, indent=1)
with open(os.path.join(HERE, "a7_MUTATE.out" if MUT else "a7.out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(checks) else 1)
