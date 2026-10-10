"""CFG584: does the law's outer residual grow with baryonic mass? Criteria: FROZEN_CRITERIA.md (dc1d7398a).
Executes cfg537_wallaby.py UNEDITED up to (not including) its power-forecast section: data build + helper functions only;
no CFG537 output is written. MUTATE: CFG584_MUTATE=1 injects +0.10 dex per dex (log M_b - 10) into WALLABY d_out.
"""
import os, sys, json, math, io, contextlib
import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "CFG537_outer_excess_independent", "cfg537_wallaby.py"))
src = open(SRC).read()
cut = "# ================================================================== power forecast"
assert src.count(cut) == 1
os.environ.pop("CFG537_MUTATE", None)
ns = {"__file__": SRC, "__name__": "cfg537_head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src.split(cut)[0], SRC, "exec"), ns)
GALS, SPR, A0SI, residual_rows, matched, E_ = ns["GALS"], ns["SPR"], ns["A0SI"], ns["residual_rows"], ns["matched"], ns["E_"]

MUTATE = os.environ.get("CFG584_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


def slope(x, y, cov=None):
    X = np.column_stack([np.ones_like(x), x - 10] + ([cov] if cov is not None else []))
    return np.linalg.lstsq(X, y, rcond=None)[0]


def boot(x, y, cov=None, n=2000, seed=584):
    rng = np.random.default_rng(seed); s = []
    for _ in range(n):
        i = rng.integers(0, len(x), len(x))
        s.append(slope(x[i], y[i], None if cov is None else cov[i])[1])
    return float(np.std(s, ddof=1))


P("=" * 100)
P(f"CFG584  mass trend of the law's outer residual  {'*** MUTATE: +0.10 dex/dex injected ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)
P(f"WALLABY sample from CFG537 (executed unedited): {len(GALS)} galaxies; early (T<=3) {int(E_.sum())}")

# ---------------- power forecast (no WALLABY residual used)
P("\n== POWER FORECAST (SPARC scatter about its own fit x WALLABY log M_b spread; printed before any WALLABY slope) ==")
FC = {}
lmw_all = np.array([g["lMb"] for g in GALS]); okw = np.array([g["nout"] >= 2 for g in GALS])
for f in ("canonical", "alt"):
    r = SPR[f]; x = np.array([q["lMb"] for q in r]); y = np.array([q["d_out"] for q in r]); m = np.isfinite(y)
    b = slope(x[m], y[m]); resid = y[m] - (b[0] + b[1] * (x[m] - 10)); sd = float(np.std(resid, ddof=2))
    se = sd / (np.std(lmw_all[okw]) * math.sqrt(okw.sum()))
    FC[f] = dict(sparc_slope=float(b[1]), sparc_scatter=sd, expected_se=se, expected_Z=0.065 / se, power=float(norm.cdf(0.065 / se - 2)))
    P(f"  [{f}] SPARC (discovery, CFG537 statistic) slope {b[1]:+.3f}; scatter {sd:.3f}; WALLABY expected SE {se:.4f}; "
      f"expected Z at 0.065 = {0.065 / se:.2f}; P(Z>=2) {FC[f]['power']:.2f}")
LOWP = any(FC[f]["power"] < 0.5 for f in FC)
P(f"  LOW POWER label (P(Z>=2) < 0.5 on either footing): {LOWP}")

# ---------------- controls
P("\n== controls ==")
ROWS = {f: residual_rows(GALS, A0SI[f]) for f in ("canonical", "alt")}
ref = {"canonical": 0.026, "alt": 0.029}
dev = max(abs(matched(ROWS[f], "d_out", E_)["diff"] - ref[f]) for f in ref)
check(dev <= 0.002, "C1 CFG537's matched early-late d_out reproduced: " + ", ".join(f"{f} {matched(ROWS[f], 'd_out', E_)['diff']:+.3f}" for f in ref) + f" (max dev {dev:.4f})")
nvalid = {f: int(np.isfinite([q["d_out"] for q in ROWS[f]]).sum()) for f in ROWS}
check(min(nvalid.values()) >= 60, f"C2 galaxies with a valid outer residual: {nvalid} (>= 60)")

# ---------------- scoring
P("\n== SCORING (frozen) ==")
RESU, calls = {}, {}
for f in ("canonical", "alt"):
    rows = ROWS[f]
    x = np.array([q["lMb"] for q in rows]); y = np.array([q["d_out"] for q in rows]); T = np.array([q["T"] for q in rows])
    fg = np.array([q["fgas"] for q in rows]); m = np.isfinite(y)
    x, y, T, fg = x[m], y[m], T[m], fg[m]
    if MUTATE:
        y = y + 0.10 * (x - 10)
    s = slope(x, y)[1]; se = boot(x, y); Z = s / se
    sE = slope(x, y, (T <= 3).astype(float))[1]; seE = boot(x, y, (T <= 3).astype(float))
    sG = slope(x, y, fg)[1]; seG = boot(x, y, fg)
    calls[f] = "CONFIRMED" if (s > 0 and Z >= 2) else ("CONTRADICTED" if (s < 0 and Z <= -2) else "NOT CONFIRMED")
    RESU[f] = dict(n=int(m.sum()), slope=float(s), se=se, Z=float(Z), slope_with_early=float(sE), se_with_early=seE,
                   slope_with_fgas=float(sG), se_with_fgas=seG, lMb_range=[float(x.min()), float(x.max())])
    P(f"  [{f}] N {m.sum()}  log M_b {x.min():.2f}-{x.max():.2f}  slope {s:+.3f} +- {se:.3f} (Z {Z:+.2f}) -> {calls[f]}")
    P(f"          with early-type covariate: {sE:+.3f} +- {seE:.3f};  with f_gas covariate: {sG:+.3f} +- {seG:.3f}")
overall = calls["canonical"] if calls["canonical"] == calls["alt"] else "SPLIT"
P(f"\nVERDICT: {overall}{'  [LOW POWER]' if LOWP and overall != 'CONFIRMED' else ''}")
if MUTATE:
    P("MUTATE reading: the injected +0.10 dex/dex must be CONFIRMED.")
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(verdict=overall, calls=calls, low_power=LOWP, forecast=FC, results=RESU, checks=CHECKS),
          open(os.path.join(HERE, f"cfg584_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg584_mass{TAG}.out"), "w").write("\n".join(OUT) + "\n")
