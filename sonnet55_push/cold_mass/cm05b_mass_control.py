"""cm05b: confounder check for cm05 (declared after cm05's result, before this run): does the offset-L_X/L_B correlation survive controlling for galaxy mass?
Partial Spearman rho(offset, log LX/LB | log M_JAM-law) on the same 16 galaxies; also rho(offset, log M) and rho(LX/LB, log M).
Reading rule: if the partial rho stays > 0.3 with one-sided permutation p < 0.1 (permuting LX/LB residuals), hot gas carries information beyond mass; otherwise mass may explain cm05.
Run: python3 cm05b_mass_control.py | MUTATE=1 replaces LX/LB by log M (partial must collapse to ~0, check P fails)
"""
import os, sys, json, re, numpy as np
from scipy.stats import spearmanr, rankdata
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cm05_sluggs_lx_all.py")).read().split("rng = np.random")[0]
exec(src)
pg = pgall["nu_mono|canonical"]; names = sorted(n for n in pg if n in LX)
off = rankdata([pg[n]["off"] for n in names]); lm = rankdata([pg[n]["lMjamlaw"] for n in names]); lx = rankdata([LX[n][0] for n in names])
if MUTATE: lx = lm.copy()
def resid(a, b):
    A = np.vstack([b, np.ones_like(b)]).T; return a - A @ np.linalg.lstsq(A, a, rcond=None)[0]
ro, rx = resid(off, lm), resid(lx, lm)
pr = float(np.corrcoef(ro, rx)[0, 1]) if np.std(rx) > 1e-12 else 0.0
rng = np.random.default_rng(6); perm = [np.corrcoef(ro, rng.permutation(rx))[0, 1] if np.std(rx) > 1e-12 else 0 for _ in range(20000)]
p = float(np.mean(np.array(perm) >= pr))
print(f"   rho(offset, log M) = {spearmanr(off, lm).correlation:+.2f};  rho(LX/LB, log M) = {spearmanr(lx, lm).correlation:+.2f}")
print(f"   PARTIAL rho(offset, LX/LB | log M) = {pr:+.2f} (one-sided p = {p:.3f}, N = {len(names)})")
print("   READING: " + ("hot gas carries information beyond mass" if (pr > 0.3 and p < 0.1) else "mass may explain the cm05 correlation"))
check("P the partial correlation stays > 0.3 with p < 0.1 (MUTATE: LX replaced by mass, must fail)", pr > 0.3 and p < 0.1)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
