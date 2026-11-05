#!/usr/bin/env python3
"""WG6 SHAPE DIAGNOSTIC (POST-RESULT; no frozen criteria): per-bin model/data of the CMB-lensing bandpowers (Planck PR4 8-400, PLAIN W
binning) for the law-alone runs of WG2, WG3, WG4 and WG6, with resolution pairs. WG2-WG6 graded one best-fit amplitude r; this shows the
shape that amplitude hid. Projection copied unchanged from WG2 (as wg6_grade.py). Run: python3 wg6_shape_diag.py.
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, glob
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.stats import chi2 as CHI2
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB); RUNS = os.path.join(HERE, "runs")
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG917_cmb_lensing_gate")); import cfg917_lib as LB   # read only
sys.path.insert(0, HERE); import wg6_pm; PM = wg6_pm.B
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)

# ---------------------------------------------------------------- copied unchanged from WG2's wg2_grade.py (lines 21-83)
H = PM.H; CH = 2997.92458 / H                      # c / H0 in Mpc
ZS = 1090.0
LS = np.arange(8, LB.LMAX + 1); L4 = (LS * (LS + 1.0)) ** 2 / (2 * math.pi)
D = LB.load_pr4()

# ------------------------------------------------------------------ geometry and Limber (WG1's engine, same E(a) as the runs)
def geom(bg):
    E, _ = PM.background(bg)
    z = np.concatenate([np.linspace(0.0, 10.0, 8001), np.geomspace(10.0, ZS, 4001)[1:]])
    f = CH / np.array([E(1 / (1 + zz)) for zz in z])
    chi = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(z))]); chis = float(chi[-1])
    cg = np.concatenate([np.geomspace(1e-3, 100.0, 160), np.linspace(100.0, chis, 700)[1:]])
    w = np.zeros_like(cg); w[1:] += 0.5 * np.diff(cg); w[:-1] += 0.5 * np.diff(cg)
    q = 2.0 * (chis - cg) / (cg * chis)
    return dict(cg=cg, zg=np.interp(cg, chi, z), ker=w * q ** 2 / cg ** 2, chis=chis)
GEO = {bg: geom(bg) for bg in ("B1", "B2", "B1D", "B2D")}   # B1D, B2D as WG4

def snap_tables(run):
    """per snapshot: z, log k (1/Mpc), log Delta^2_Psi on bins up to k_cut = 0.5 k_Ny, and the high-k slope."""
    kny = math.pi * run["N"] / run["L"] * H; kcut = 0.5 * kny; tabs = []
    for s in sorted(run["snaps"], key=lambda s: s["z"]):
        k = np.array(s["k"]) * H; Pp = np.array(s["P_psi"]) / H ** 3
        d2 = k ** 3 * Pp / (2 * math.pi ** 2); m = (k <= kcut) & (d2 > 0)
        lk, ld = np.log(k[m]), np.log(d2[m])
        hi = (k[m] >= kcut / 2)
        slope = float(np.polyfit(lk[hi], ld[hi], 1)[0]) if hi.sum() >= 3 else -4.0
        tabs.append(dict(z=s["z"], lk=lk, ld=ld, slope=slope))
    return tabs, kcut

def logd2(t, lkq, zero_beyond):
    lk, ld = t["lk"], t["ld"]
    out = np.interp(lkq, lk, ld)                                           # flat below the first bin (np.interp clamps)
    hi = lkq > lk[-1]
    out = np.where(hi, ld[-1] + t["slope"] * (lkq - lk[-1]), out)
    return out, (hi if zero_beyond else np.zeros_like(hi)), (lkq >= lk[0]) & (lkq <= lk[-1])

def project(run, zero_beyond=False):
    g = GEO[run["bg"]]; tabs, kcut = snap_tables(run)
    zs = np.array([t["z"] for t in tabs]); lz = np.log1p(zs)
    C = np.zeros(len(LS)); Cin = np.zeros(len(LS))
    for chi, z, kw in zip(g["cg"], g["zg"], g["ker"]):
        k = (LS + 0.5) / chi; lkq = np.log(k)
        if z >= zs[-1]:
            i0 = i1 = len(tabs) - 1; t = 0.0
        else:
            i1 = int(np.searchsorted(zs, z)); i0 = max(i1 - 1, 0); t = 0.0 if i1 == i0 else (math.log1p(z) - lz[i0]) / (lz[i1] - lz[i0])
        a0_, z0_, in0 = logd2(tabs[i0], lkq, zero_beyond); a1_, z1_, in1 = logd2(tabs[i1], lkq, zero_beyond)
        ld = (1 - t) * a0_ + t * a1_
        Pk = 2 * math.pi ** 2 * np.exp(ld) / k ** 3
        Pk = np.where(z0_ | z1_, 0.0, Pk)
        C += kw * Pk; Cin += kw * Pk * (in0 & in1)
    X = np.zeros(LB.LMAX + 1); X[LS] = L4 * C
    Xin = np.zeros(LB.LMAX + 1); Xin[LS] = L4 * Cin
    return X, Xin

def grade_X(X):
    A, sA = LB.pr4_amp(D, X); c2 = LB.pr4_chi2(D, X)
    u = LB.wsum(D["W"], X); b = LB.qform(u, D["Cinv"]); Ap = LB.qform(u, D["Cinv"], D["d"]) / b
    return dict(r=1 / A, A_fit=A, sA=sA, chi2_unscaled=c2, p_unscaled=float(CHI2.sf(c2, D["n"])), r_plain=1 / Ap)

def run_label(r):
    return "FAILS LOW" if r < 0.5 else ("FAILS HIGH" if r > 2 else "WITHIN x2")



R = REB
CASES = [("WG2 R0 law off, B2, A_s 1e-9, 128^3", "WG2_bare_law_web_lensing/runs/R0_TIE_B2_As1e-09_N128_s200_zon50_canonical.json"),
         ("WG2 R1 a0 flat, B2, A_s 2.1e-9, 128^3", "WG2_bare_law_web_lensing/runs/R1_TIE_B2_As2.1e-09_N128_s200_zon50_canonical.json"),
         ("WG2 R1 a0 flat, B2, A_s 2.1e-9, 192^3", "WG2_bare_law_web_lensing/runs/R1_TIE_B2_As2.1e-09_N192_s200_zon50_canonical.json"),
         ("WG3 T1tau0, B2, A_s 1e-9, 128^3", "WG3_bound_only_web_rule/runs/T1T0_TIE_B2_As1e-09_N128_s200_zon50_canonical.json"),
         ("WG4 R1 a0 tracks rho_DE, B2D, A_s 2.1e-9, 128^3", "WG4_a0_tracks_de_web/runs/R1_DE_B2D_As2.1e-09_N128_s200_zon50_canonical.json"),
         ("WG4 R1 a0 tracks rho_DE, B2D, A_s 2.1e-9, 192^3", "WG4_a0_tracks_de_web/runs/R1_DE_B2D_As2.1e-09_N192_s200_zon50_canonical.json"),
         ("WG6 screened 100 Mpc, B2D, A_s 1e-9, 128^3", "WG6_screened_phantom_web/runs/R1Y0.01_DE_B2D_As1e-09_N128_s200_zon50_canonical.json"),
         ("WG6 screened 33 Mpc, B2D, A_s 2.1e-9, 128^3", "WG6_screened_phantom_web/runs/R1Y0.03_DE_B2D_As2.1e-09_N128_s200_zon50_canonical.json"),
         ("WG6 screened 33 Mpc, B2D, A_s 2.1e-9, 192^3", "WG6_screened_phantom_web/runs/R1Y0.03_DE_B2D_As2.1e-09_N192_s200_zon50_canonical.json")]
P("WG6 SHAPE DIAGNOSTIC (post-result): model / data per PR4 bin (PLAIN W), law alone from a baryons-only start.")
P("  bin L_av: " + " ".join("%7.0f" % x for x in D["Lav"]))
RB = {}
for nm, f in CASES:
    run = json.load(open(os.path.join(R, f))); X, Xin = project(run); rb = LB.wsum(D["W"], X) / D["d"]; RB[nm] = rb
    A, _ = LB.pr4_amp(D, X); c2 = LB.qform(LB.pr4_binned(D, A * X) - D["d"], D["Cinv"]); fin = LB.wsum(D["W"], Xin) / LB.wsum(D["W"], X)
    P(f"  {nm:<50} " + " ".join("%7.3g" % x for x in rb) + f" | r {1 / A:.3g} | shape chi2 after best amplitude {c2:.0f} (8 dof) | in-box bins 1/9 {fin[0]:.2f}/{fin[-1]:.2f}")
q = RB["WG4 R1 a0 tracks rho_DE, B2D, A_s 2.1e-9, 128^3"] / RB["WG2 R1 a0 flat, B2, A_s 2.1e-9, 128^3"]
P("  WG4 / WG2 per bin (a0 tracking rho_DE over a0 flat, 128^3): " + " ".join("%.3f" % x for x in q) + f"  (range {q.min():.2f}-{q.max():.2f})")
P(f"  law off (WG2 R0 B2) largest per-bin value: {RB['WG2 R0 law off, B2, A_s 1e-9, 128^3'].max():.2e}")
P("Reading: every law-alone rule gets the shape wrong. With QUMOND on, lensing is about 14 times the measured value at L ~ 28 and 0.08 at L ~ 377,")
P("converged from 128^3 to 192^3. WG3's T1tau0 'within x2' and the 'factor 1/2' were artifacts of grading one amplitude.")
P("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
open(os.path.join(HERE, "wg6_shape_diag.out"), "w").write("\n".join(OUT) + "\n")
