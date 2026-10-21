#!/usr/bin/env python3
"""W4-15 -- does W4-14's outward a0 decline follow the external field (Chae+2021 environmental e_N)?
Criteria: FROZEN_CRITERIA.md (committed alone, 5bc61b902). Per-galaxy WLS slope s of log a0_i vs log g_bar (simple mu, Upsilon 0.5).
Light: numpy/scipy, one process. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_15_outward_decline_vs_external_field/w4_15.py > .../w4_15.out
    W4_15_MUTATE=1 ... > .../w4_15_MUTATE.out   (M1 planted rho ~ 0.3 power; M2 e_N shuffle; exit 1 when both behave)
kappa = 1/2 FITTED. Not theory closed.
"""
import contextlib, csv, io, json, math, os, sys
import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
MUT = os.environ.get("W4_15_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
KPC = 3.0857e19
OUT = []


def P(s=""):
    print(s); OUT.append(str(s))


env = {r["galaxy"]: r for r in csv.DictReader(open(os.path.join(REPO, "real_research/reviews/directional_efe_2026/laneB_data/chae21_env.csv")))}


def slope(g, inv="simple"):
    R = g["R"] * KPC
    gb = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2) * 1e6 / R
    go = (g["Vobs"] * 1e3) ** 2 / R
    m = (gb > 0) & (go > gb) & (g["Vobs"] > 0)
    if m.sum() < 8:
        return None
    gb, go = gb[m], go[m]
    if inv == "simple":
        a0 = go * (go - gb) / gb
        lev = 1 + go / (go - gb)
    else:
        a0 = gb / np.log(1 - gb / go) ** 2
        lev = 1 + go / (go - gb)                                  # same lever approximation, cross-check only
    sl = 2 * np.clip(g["eV"][m], 1, None) / (np.clip(g["Vobs"][m], 1, None) * math.log(10))
    w = 1 / (lev * sl) ** 2
    x, y = np.log10(gb), np.log10(a0)
    xm, ym = np.sum(w * x) / w.sum(), np.sum(w * y) / w.sum()
    return float(np.sum(w * (x - xm) * (y - ym)) / np.sum(w * (x - xm) ** 2))


def spearman(a, b):
    ra, rb = rankdata(a), rankdata(b)
    return float(np.corrcoef(ra, rb)[0, 1])


def perm_p(a, b, n=10000, seed=64):
    r0 = spearman(a, b)
    rng = np.random.default_rng(seed)
    ra, rb = rankdata(a), rankdata(b)
    cnt = 0
    for _ in range(n):
        if abs(np.corrcoef(ra, rng.permutation(rb))[0, 1]) >= abs(r0) - 1e-12:
            cnt += 1
    return r0, (cnt + 1) / (n + 1)


rows = []
for g in C.load_sparc():
    m = g["meta"]
    if not m or m["Q"] > 2 or m["Inc"] < 30 or g["name"] not in env:
        continue
    s = slope(g)
    if s is None:
        continue
    e = env[g["name"]]
    fg = m["MHI"] / (m["MHI"] + 0.5 * m["L36"]) if (m["MHI"] + m["L36"]) > 0 else float("nan")
    rows.append(dict(name=g["name"], s=s, s_rar=slope(g, "rar"), eN_max=float(e["log_eN_maxclu"]), eN_no=float(e["log_eN_noclu"]),
                     fgas=fg, logSB=math.log10(m["SBdisk"]) if m["SBdisk"] > 0 else float("nan")))
s = np.array([r["s"] for r in rows]); x = np.array([r["eN_max"] for r in rows]); x2 = np.array([r["eN_no"] for r in rows])
P("W4-15  outward a0 decline vs environmental external field (Chae+2021)" + ("  [MUTATE]" if MUT else ""))
P(f"obs lane. kappa = 1/2 FITTED. Not theory closed.\n\nsample: {len(rows)} SPARC galaxies (Q <= 2, i >= 30, >= 8 valid points, in Chae's table)")
P(f"outward decline: mean slope d log a0 / d log g_bar = {np.mean(s):+.3f} (median {np.median(s):+.3f}; s > 0 = a0 falls outward); "
  f"RAR cross-check median {np.median([r['s_rar'] for r in rows]):+.3f}")
res = {}
if not MUT:
    rho, p = perm_p(s, x)
    rho2, p2 = perm_p(s, x2)
    hi = s[x >= np.median(x)]; lo = s[x < np.median(x)]
    rng = np.random.default_rng(64)
    bs = [np.median(rng.choice(hi, len(hi))) - np.median(rng.choice(lo, len(lo))) for _ in range(2000)]
    dsplit = float(np.median(hi) - np.median(lo)); sds = float(np.std(bs))
    ok = np.isfinite([r["fgas"] for r in rows]); okb = np.isfinite([r["logSB"] for r in rows])
    rf = spearman(s[ok], np.array([r["fgas"] for r in rows])[ok]); rs = spearman(s[okb], np.array([r["logSB"] for r in rows])[okb])
    P(f"PRIMARY  Spearman rho(s, log e_N maxclu) = {rho:+.3f}, permutation p = {p:.4f}")
    P(f"secondary rho(s, log e_N noclu) = {rho2:+.3f}, p = {p2:.4f}; median split (high - low e_N) {dsplit:+.3f} +- {sds:.3f}")
    P(f"nuisance (report only): rho(s, gas fraction) = {rf:+.3f}; rho(s, log SBdisk) = {rs:+.3f}")
    verdict = "EFE-CONSISTENT" if (rho > 0 and p < 0.0027) else ("NO EFE SIGNAL" if p > 0.05 else "INTERMEDIATE")
    P(f"LANE VERDICT: {verdict}")
    res = dict(n=len(rows), mean_s=float(np.mean(s)), median_s=float(np.median(s)), rho=rho, p=p, rho_noclu=rho2, p_noclu=p2,
               split=dsplit, split_sd=sds, rho_fgas=rf, rho_SB=rs, verdict=verdict, rows=rows)
else:
    beta = 0.3 * np.std(s) / np.std(x)
    sp = s + beta * (x - x.mean())
    rho1, p1 = perm_p(sp, x)
    xs = np.random.default_rng(64).permutation(x)
    rho2, p2 = perm_p(s, xs)
    P(f"M1 planted (beta {beta:.3f}): rho {rho1:+.3f}, p {p1:.4f} -> {'detected at 3 sigma' if p1 < 0.0027 else 'detected at p<0.05' if p1 < 0.05 else 'NOT detected'}")
    P(f"M2 e_N shuffled: rho {rho2:+.3f}, p {p2:.4f} -> {'null as expected' if p2 > 0.05 else 'spurious'}")
    res = dict(M1=dict(beta=float(beta), rho=rho1, p=p1), M2=dict(rho=rho2, p=p2))
json.dump(dict(mutate=MUT, **res), open(os.path.join(HERE, f"w4_15_results{SUF}.json"), "w"), indent=1, default=float)
if MUT:
    sys.exit(1 if (res["M1"]["p"] < 0.05 and res["M2"]["p"] > 0.05) else 2)
sys.exit(0)
