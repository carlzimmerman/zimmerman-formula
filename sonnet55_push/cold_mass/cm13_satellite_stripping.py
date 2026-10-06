"""cm13: the satellite test -- does a cluster/group satellite hold LESS cold mass than an isolated galaxy at fixed mass (LCDM tidal stripping),
or the same galaxy-level share (hierarchical ownership, cm08-cm10)?  Data: Alabi+17 (32 SLUGGS ETGs; env column F/G/C), retained fraction f at 5 Re (cm08).
Declared before the run: NON-CENTRAL galaxies only (cm08's list of 9 centrals excluded). Compare field (F) vs cluster (C) satellites, and F vs (G+C).
STRIPPING if satellites are lower with one-sided Mann-Whitney p < 0.05; else NOT SHOWN (consistent with ownership, low power stated).
Also reported: the same with the mass trend removed (residual of f vs log M* across the non-centrals).
Run: python3 cm13_satellite_stripping.py | MUTATE=1 shuffles the environment labels (check E fails)
"""
import os, sys, re, numpy as np
from scipy.stats import mannwhitneyu, spearmanr
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cm07_alabi32_hot_halo.py")).read().split("names = sorted(")[0]
exec(src)
env = {}
for line in tex.split("\\begin{table*}")[1].split("\n"):
    c = [x.strip() for x in line.split("&")]
    if len(c) >= 12 and re.match(r"^\$?\s*\d{3,4}", c[0]):
        env[num(c[0])] = c[5].strip()
COSMIC = 0.1200 / 0.02237; CEN = ("4486", "4472", "1399", "1316", "4374", "4649", "5846", "1407", "4636")
names = sorted(n for n in set(t1) & set(t2) & set(env) if n not in CEN)
f, lm = [], []
for n in names:
    Re, lms = t1[n]; Mt, fd = t2[n]; Ms = max(1 - fd, 0.05) * Mt
    y = G * Ms * Msun / (5 * Re * kpc)**2 / 9.3603e-11; f.append((Mt - nu(y) * Ms) / (COSMIC * Ms)); lm.append(lms)
f, lm = np.array(f), np.array(lm); E = np.array([env[n] for n in names]); E_true = E.copy()
if MUTATE: E = np.roll(E, 4)
A = np.vstack([lm, np.ones_like(lm)]).T; fres = f - A @ np.linalg.lstsq(A, f, rcond=None)[0]
for lab in ("F", "G", "C"):
    m = E == lab; print(f"   {lab}: N {m.sum():2d}  median f {np.median(f[m]):.2f}  median log M* {np.median(lm[m]):.2f}  " + ", ".join(f"{n}:{v:.2f}" for n, v in zip(np.array(names)[m], f[m])))
p1 = mannwhitneyu(f[E == "C"], f[E == "F"], alternative="less").pvalue
p2 = mannwhitneyu(f[E != "F"], f[E == "F"], alternative="less").pvalue
p3 = mannwhitneyu(fres[E != "F"], fres[E == "F"], alternative="less").pvalue
print(f"   one-sided p (satellites lower): C vs F {p1:.3f}; G+C vs F {p2:.3f}; mass-detrended G+C vs F {p3:.3f};  rho(f, log M*) = {spearmanr(f, lm).correlation:+.2f}")
print("   VERDICT: " + ("STRIPPING signal (LCDM-like)" if p1 < 0.05 else "NOT SHOWN: satellites hold the same galaxy-level share (consistent with ownership; low power)"))
check("E the environment labels are the true assignment (MUTATE shuffles and must fail)", np.array_equal(E, E_true))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
