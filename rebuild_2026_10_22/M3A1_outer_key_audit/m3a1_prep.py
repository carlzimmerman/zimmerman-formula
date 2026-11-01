#!/usr/bin/env python3
"""M3A1 prep (FROZEN_CRITERIA.md): C1a Tweedie shift per cluster from eRASS1's own MGAS500 errors; C1b, C2a pointed gas in a window cut on eRASS1 MGAS500 at M3's edges. Reads other lanes, writes only here.
kappa = 1/2 FITTED, unused; not theory closed."""
import csv, json, os
import numpy as np, warnings; warnings.simplefilter("ignore")
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
MY = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); names = [str(x).strip() for x in MY["name"]]; Mg = np.asarray(MY["Mgas500"], float); z = np.asarray(MY["z"], float)
E = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data; EN = [str(s).strip() for s in E["NAME"]]; ix = {n: i for i, n in enumerate(EN)}; J = np.array([ix[n] for n in names])
mg, lo, hi = (np.asarray(E[k], float) for k in ("MGAS500", "MGAS500_L", "MGAS500_H")); assert np.allclose(mg[J] * 1e11, Mg)
ql = np.quantile(Mg, [1 / 3, 2 / 3]); T = np.digitize(Mg, ql); M3 = T == 2
P(f"M1-M3 edges MGAS500 {ql[0]:.3e} {ql[1]:.3e}; N {[int((T == t).sum()) for t in range(3)]}; M3 lg Mg {np.log10(Mg[M3]).min():.2f}-{np.log10(Mg[M3]).max():.2f}, median {np.median(np.log10(Mg[M3])):.2f}; z {z[M3].min():.3f}-{z[M3].max():.3f}, median {np.median(z[M3]):.3f}")
sl, sh = np.log10(mg[J] / lo[J]), np.log10(hi[J] / mg[J]); good = np.isfinite(sl) & np.isfinite(sh) & (lo[J] > 0) & (hi[J] > lo[J]); sig = np.where(good, 0.5 * (sl + sh), np.nan)
P(f"catalogue error, dex, half of 16-84 as tabulated: finite {int(good.sum())} of {len(sig)}; all median {np.nanmedian(sig):.3f}; by tercile " + ", ".join(f"M{t + 1} median {np.nanmedian(sig[T == t]):.3f}, p84 {np.nanpercentile(sig[T == t], 84):.3f}" for t in range(3)) + f"; asymmetry median H-L {np.nanmedian(sh - sl):+.3f}")
sig = np.where(good, sig, np.nanmedian(sig))
def tweedie(x, s, bw=None, sign=1.0):
    bw = 1.06 * np.std(x) * len(x) ** (-0.2) if bw is None else bw
    d = (x[:, None] - x[None, :]) / bw; k = np.exp(-0.5 * d * d); p = k.sum(1); dp = (-d / bw * k).sum(1); return x + sign * s * s * dp / p, bw
# K5: synthetic, known Gaussian, analytic posterior shift
rng = np.random.default_rng(20261101); xs = rng.normal(14.0, 0.35, 326); ss = 0.07; xo = xs + rng.normal(0, ss, 326); xt, _ = tweedie(xo, np.full(326, ss)); s2 = 0.35 ** 2 + ss ** 2; ana = -ss * ss * (xo - xo.mean()) / s2; top = xo >= np.quantile(xo, 2 / 3); r = (xt - xo)[top].mean() / ana[top].mean(); truth = (xs - xo)[top].mean()
k5 = 0.9 <= r <= 1.1; P(f"K5 synthetic: Tweedie top-tercile mean shift {((xt - xo)[top]).mean():+.4f}, analytic {ana[top].mean():+.4f}, ratio {r:.3f}, realised truth {truth:+.4f}: {'PASS' if k5 else 'FAIL'}")
x = np.log10(Mg); xT, bw = tweedie(x, sig); dx = xT - x
P(f"C1a Tweedie shift, dex, bandwidth {bw:.3f}: mean M1 {dx[T == 0].mean():+.4f}, M2 {dx[T == 1].mean():+.4f}, M3 {dx[M3].mean():+.4f}, M3 median {np.median(dx[M3]):+.4f}, M3 extremes {dx[M3].min():+.4f} {dx[M3].max():+.4f}")
xT2, _ = tweedie(x, sig, bw=bw / 2); xT3, _ = tweedie(x, sig, bw=bw * 2); P(f"  reported, bandwidth x 0.5, x 2: M3 mean {(xT2 - x)[M3].mean():+.4f}, {(xT3 - x)[M3].mean():+.4f}")
S = np.zeros(4000); rg = np.random.default_rng(1)
for i in range(4000):
    xn = xT + rg.normal(0, sig); e = np.quantile(xn, 2 / 3); S[i] = (xT - xn)[xn >= e].mean()
P(f"  forward check: noise added to the shifted values, cut at the top tercile, mean(true - observed) {S.mean():+.4f} +- {S.std():.4f}; same stat on M3's Tweedie {dx[M3].mean():+.4f}")
json.dump({n: float(10 ** a) for n, a in zip(names, dx)}, open(os.path.join(HERE, "m3a1_factor_C1a.json"), "w"), indent=0)
json.dump({n: float(10 ** (-a)) if t == 2 else 1.0 for n, a, t in zip(names, dx, T)}, open(os.path.join(HERE, "m3a1_factor_C1a_MUTATE.json"), "w"), indent=0)
json.dump({n: float(10 ** a) if t == 2 else 1.0 for n, a, t in zip(names, dx, T)}, open(os.path.join(HERE, "m3a1_factor_C1a_M3.json"), "w"), indent=0)
json.dump({n: float(10 ** a) if (t == 2 and s_ <= 0.2) else 1.0 for n, a, t, s_ in zip(names, dx, T, sig)}, open(os.path.join(HERE, "m3a1_factor_C1a_cap.json"), "w"), indent=0)
P(f"  M1 shift extremes {dx[T == 0].min():+.2f} {dx[T == 0].max():+.2f}, why Mall reads nonsense under C1a on all 326; M3 with error above 0.2 dex: {int(((T == 2) & (sig > 0.2)).sum())}; M3 shift mean without them {dx[(T == 2) & (sig <= 0.2)].mean():+.4f}; applied to all M3 {dx[M3].mean():+.4f}")
# C1b, C2a
R = list(csv.DictReader(open(os.path.join(RB, "GS4_pointed_gas_offset", "gs4_matched.csv"))))
for r in R:
    r["j"] = int(r["j"]); r["d"] = float(r["d"]); r["z"] = float(r["z"]); r["lgM"] = float(r["lgM"]); r["mg"] = mg[r["j"]] * 1e11; r["sg"] = float(np.log10(hi[r["j"]] / lo[r["j"]]) / 2) if lo[r["j"]] > 0 else np.nan; r["inlens"] = EN[r["j"]] in names
    assert EN[r["j"]] == r["erass"].strip()
def uniq(rows):
    D = {}
    for r in rows:
        if r["cat"] == "V09": continue
        D.setdefault(r["j"], []).append(r)
    return D
def boot(v, n=4000):
    v = np.asarray(v); rg = np.random.default_rng(0); i = rg.integers(0, len(v), (n, len(v))); return float(np.median(v)), float(np.std(np.median(v[i], axis=1)))
def row(lab, rows):
    D = uniq(rows); v = np.array([np.median([r["d"] for r in L]) for L in D.values()]); lg = np.array([np.log10(L[0]["mg"]) for L in D.values()]); zz = np.array([L[0]["z"] for L in D.values()])
    if len(v) < 2: P(f"  {lab}: N {len(v)}"); return dict(n=len(v))
    m, se = boot(v); sl = np.polyfit(lg - np.median(lg), v, 1)[0]; rg = np.random.default_rng(0); B = [np.polyfit(lg[i] - np.median(lg), v[i], 1)[0] for i in (rg.integers(0, len(v), len(v)) for _ in range(1000))]
    P(f"  {lab}: N {len(v)}, median d {m:+.3f} +- {se:.3f}, rms {np.std(v):.3f}, slope against lg Mg {sl:+.3f} +- {np.std(B):.3f}, median z {np.median(zz):.3f}, median lg Mg {np.median(lg):.2f}"); return dict(n=len(v), med=m, se=se, rms=float(np.std(v)), slope=float(sl), slope_se=float(np.std(B)), z=float(np.median(zz)), lg=float(np.median(lg)))
LOm, HIm = Mg[M3].min(), Mg[M3].max(); zlo, zhi = z[M3].min(), z[M3].max(); RES = {}
P(f"GS4 rows {len(R)}; window: eRASS1 MGAS500 in M3's range {LOm:.2e}-{HIm:.2e}, z {zlo:.3f}-{zhi:.3f}")
W = [r for r in R if LOm <= r["mg"] <= HIm and zlo <= r["z"] <= zhi]
RES["window"] = row("M3 window, cut on eRASS1 gas (C1b)", W)
RES["z_lo"] = row("  z below M3's median", [r for r in W if r["z"] < np.median(z[M3])]); RES["z_hi"] = row("  z above M3's median", [r for r in W if r["z"] >= np.median(z[M3])])
medw = np.median(np.log10(Mg[M3])); RES["lo"] = row("  below M3's median gas", [r for r in W if np.log10(r["mg"]) < medw]); RES["hi"] = row("  above M3's median gas", [r for r in W if np.log10(r["mg"]) >= medw])
sc = np.nanmedian([r["sg"] for r in W]); RES["clean"] = row("  catalogue error below the window's median", [r for r in W if r["sg"] < sc]); RES["noisy"] = row("  catalogue error above it", [r for r in W if r["sg"] >= sc])
RES["inlens"] = row("  in the 326", [r for r in W if r["inlens"]]); RES["inM3"] = row("  in M3 itself", [r for r in W if r["inlens"] and T[names.index(EN[r["j"]])] == 2])
RES["M500win"] = row("GS4's own M500 window, for comparison (4.4e13-5.6e14)", [r for r in R if 4.4e13 <= 10 ** r["lgM"] <= 5.6e14])
RES["M500_M3"] = row("GS4's M3 tercile by lensing M500, above 2.39e14", [r for r in R if 2.39e14 <= 10 ** r["lgM"] <= 5.6e14])
RES["belowM3"] = row("cut below M3, same z", [r for r in R if r["mg"] < LOm and zlo <= r["z"] <= zhi])
P("  catalogue-to-catalogue split is GS4's; not repeated")
d = RES["window"]["med"]; se = RES["window"]["se"]
for tag, dd in (("C2a", d), ("C2a_plus", d + se), ("C2a_minus", d - se)):
    json.dump({n: (10 ** (dd - 0.005) if t == 2 else 1.0) for n, t in zip(names, T)}, open(os.path.join(HERE, f"m3a1_factor_{tag}.json"), "w"), indent=0)
json.dump(dict(edges=ql.tolist(), sig_M3=float(np.median(sig[M3])), tweedie_M3=float(dx[M3].mean()), bw=float(bw), bw_half=float((xT2 - x)[M3].mean()), bw_twice=float((xT3 - x)[M3].mean()), k5=bool(k5), gs4=RES), open(os.path.join(HERE, "m3a1_prep.json"), "w"), indent=1)
open(os.path.join(HERE, "m3a1_prep.out"), "w").write("\n".join(OUT) + "\n")
