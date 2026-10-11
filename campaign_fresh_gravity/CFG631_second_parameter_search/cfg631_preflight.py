"""CFG631 pre-flight (step 0b): property tables, coverage, collinearity and the POWER FORECAST.
Uses NO law residual and NO lensing estimate: discs' residual scatter is the recorded CFG584 value (0.130 dex, SPARC,
CFG537 statistic, about its mass fit); KiDS sigma_D is the recorded CFG585/586 K9 error (~0.34) inflated x1.2 (CFG589 null).
Run: nice -n 10 python3 cfg631_preflight.py > cfg631_preflight.out
"""
import os, sys, json, math
import numpy as np
from scipy.stats import norm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg631_common as K  # noqa: E402

OUT = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


SIG_R = 0.130          # CFG584 recorded SPARC outer-residual scatter about its mass fit (CFG537 statistic)
EFF = 0.10             # effect: 0.10 dex change of the residual across the property's 16-84 percentile range
CORE = ("fgas", "bul", "lSig", "T", "inc", "HF")
ADD = ("colour", "env")
WCORE = ("fgas", "lSig", "T", "inc")
M_FAMILY = len(CORE) + len(ADD) + 5          # SPARC 8 + WALLABY 5 properties in one max-T family
ZC = norm.ppf(1 - 0.05 / (2 * M_FAMILY))  # Bonferroni approximation of the max-T critical value (forecast only)


def forecast(rows, props, extra=None, label="", zc=ZC, one_sided=False):
    res = {}
    base = [r for r in rows if r["nout"] >= 2 and all(np.isfinite(r[p]) for p in ("lMb",) + props)]
    for add in ([None] + list(extra or [])):
        pr = props + ((add,) if add else ())
        sub = [r for r in base if add is None or np.isfinite(r[add])]
        X = np.array([[r[p] for p in ("lMb",) + pr] for r in sub]); N = len(sub)
        for j, p in enumerate(pr):
            if add and p != add:
                continue
            xj = X[:, j + 1]; others = np.delete(X, j + 1, axis=1)
            A = np.column_stack([np.ones(N), others]); b = np.linalg.lstsq(A, xj, rcond=None)[0]
            r2 = 1 - np.var(xj - A @ b) / np.var(xj)
            span = 1.0 if set(np.unique(xj)) <= {0.0, 1.0} else np.percentile(xj, 84) - np.percentile(xj, 16)   # binary: category difference
            se = SIG_R / (np.std(xj) * math.sqrt(N) * math.sqrt(max(1 - r2, 1e-6)))
            beta = EFF / span if span > 0 else np.nan
            z1 = norm.ppf(0.95)
            pw = float(norm.cdf(beta / se - zc)) if np.isfinite(beta) else np.nan
            pc = float(norm.cdf(beta / se - z1)) if np.isfinite(beta) else np.nan
            mde = (zc + norm.ppf(0.8)) * se * span; mdc = (z1 + norm.ppf(0.8)) * se * span
            res[p] = dict(N=N, span=float(span), VIF=float(1 / max(1 - r2, 1e-6)), se_dex_per_span=float(se * span),
                          power_discovery_0p1dex=pw, power_confirm_0p1dex=pc, mde80_discovery_dex=float(mde), mde80_confirm_dex=float(mdc))
            P(f"  {label:8s} {p:7s} N {N:3d}  16-84 span {span:7.3f}  VIF {1 / max(1 - r2, 1e-6):5.2f}  SE {se * span:.3f} dex/span  "
              f"power(0.10 dex) discovery {pw:.2f} / confirm {pc:.2f}   MDE80 discovery {mde:.3f} / confirm {mdc:.3f} dex")
    return res


P("=" * 100); P("CFG631 pre-flight: properties, coverage, collinearity, power (NO residuals, NO lensing)"); P("=" * 100)
ns = K.cfg537_head()
S = K.sparc_props(ns); W = K.wallaby_props(ns)
P(f"SPARC (CFG537 sample) N {len(S)}; outer band (R >= 3 R_d) >= 2 points: {sum(r['nout'] >= 2 for r in S)}")
for p in CORE + ADD + ("fbul",):
    v = np.array([r[p] for r in S if r["nout"] >= 2], float)
    P(f"  {p:7s} finite {np.isfinite(v).sum():3d}  sum {np.nansum(v):7.1f}  median {np.nanmedian(v):+.3f}  16/84 {np.nanpercentile(v, 16):+.3f} / {np.nanpercentile(v, 84):+.3f}")
P(f"WALLABY (CFG537 build) N {len(W)}; outer >= 2: {sum(r['nout'] >= 2 for r in W)}")
for p in WCORE + ("W12",):
    v = np.array([r[p] for r in W if r["nout"] >= 2], float)
    P(f"  {p:7s} finite {np.isfinite(v).sum():3d}  median {np.nanmedian(v):+.3f}  16/84 {np.nanpercentile(v, 16):+.3f} / {np.nanpercentile(v, 84):+.3f}")
Xc = np.array([[r[p] for p in ("lMb",) + CORE] for r in S if r["nout"] >= 2 and all(np.isfinite(r[p]) for p in ("lMb",) + CORE)])
P("SPARC core correlation matrix (lMb, " + ", ".join(CORE) + "):")
for row in np.corrcoef(Xc.T):
    P("   " + " ".join(f"{x:+.2f}" for x in row))

P(f"\n== POWER FORECAST: sigma_r {SIG_R} dex (CFG584 record), effect {EFF} dex across the 16-84 range, "
  f"discovery critical |t| ~ {ZC:.2f} (Bonferroni over {M_FAMILY} properties; the real test uses the permutation max-T); confirmation one-sided 1.645 (before Holm)")
FS = forecast(S, CORE, ADD, "SPARC")
FW = forecast(W, WCORE, ("W12",), "WALLABY")

P("\n== KiDS f30 early types (properties only; no lensing)")
A, B = K.kids_heads()
raw, part, E2, qid = K.kids_props(A, B)
P(f"f30 early {int(A['E'].sum())}; with all five properties finite {int(E2.sum())} (dropped: SFR sentinel / bad r-Ks)")
cm = np.corrcoef(np.array([raw[k][E2] for k in K.KPROPS] + [A['LMSL'][E2]]))
P("raw correlation (" + ", ".join(K.KPROPS) + ", logM*):")
for row in cm:
    P("   " + " ".join(f"{x:+.2f}" for x in row))
KF = {}
for k in K.KPROPS:
    v = part[k]; t1, t2 = np.nanquantile(v[E2], [1 / 3, 2 / 3]); hi, lo = E2 & (v > t2), E2 & (v < t1)
    lm, z = A["LMSL"], raw["z"]
    sep_raw = np.median(raw[k][hi]) - np.median(raw[k][lo])
    KF[k] = dict(n_hi=int(hi.sum()), n_lo=int(lo.sum()), dlogM=float(np.median(lm[hi]) - np.median(lm[lo])),
                 dz=float(np.median(z[hi]) - np.median(z[lo])), sep_raw=float(sep_raw), sd_partial_over_raw=float(np.nanstd(v[E2]) / np.nanstd(raw[k][E2])))
    P(f"  {k:6s} HIGH {hi.sum():5d} / LOW {lo.sum():5d}  median dlogM* {KF[k]['dlogM']:+.3f}  dz {KF[k]['dz']:+.3f}  raw separation {sep_raw:+.3f}  "
      f"partial sd / raw sd {KF[k]['sd_partial_over_raw']:.2f}")
old585, young585 = A["OLD"], A["YOUNG"]
v = part["ur"]; t1, t2 = np.nanquantile(v[E2], [1 / 3, 2 / 3])
hi = E2 & (v > t2); lo = E2 & (v < t1)
P(f"  overlap with CFG585 groups: HIGH-ur in CFG585 OLD {np.sum(hi & old585) / hi.sum():.2f}; LOW-ur in CFG585 YOUNG {np.sum(lo & young585) / lo.sum():.2f}")
sD = 0.34 * 1.2
for D in (0.26, 0.45, 0.90):
    P(f"  KiDS forecast (K9, sigma_D {sD:.2f} = 0.34 x 1.2): D {D:+.2f} -> expected Z {D / sD:.2f}, P(Z >= 2) {norm.cdf(D / sD - 2):.2f}   "
      f"(D 0.26 = a 0.1 dex mass difference)")
json.dump(dict(sparc=FS, wallaby=FW, kids=KF, sig_r=SIG_R, zc=ZC), open(os.path.join(K.HERE, "cfg631_preflight.json"), "w"), indent=1)
open(os.path.join(K.HERE, "cfg631_preflight.out"), "w").write("\n".join(OUT) + "\n")
