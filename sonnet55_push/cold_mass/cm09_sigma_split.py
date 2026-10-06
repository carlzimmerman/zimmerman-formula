"""cm09 (POST HOC, labelled): does the two-level retention (cm08) follow velocity dispersion (cooling-threshold reading) or central/non-central status?
f = cm08's retained fraction at 5 Re (canonical; alt reported); sigma = Alabi+17 Table 1 central stellar dispersion within 1 kpc.
Declared in chat before this run: threshold sigma = 250 km/s (cooling-mass reading, ~10^6.5 K). Reported: medians in the 2x2 table (sigma </>= 250 x central/not);
partial Spearman rho(f, sigma | central) and rho(f, central | sigma). Reading: if sigma drives it, rho(f, sigma | central) > 0 and the 2x2 splits by sigma.
Run: python3 cm09_sigma_split.py | MUTATE=1 shuffles sigma (check C fails)
"""
import os, sys, re, numpy as np
from scipy.stats import spearmanr, rankdata
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cm07_alabi32_hot_halo.py")).read().split("names = sorted(")[0]
exec(src)
sig = {}
for line in tex.split("\\begin{table*}")[1].split("\n"):
    c = [x.strip() for x in line.split("&")]
    if len(c) >= 12 and re.match(r"^\$?\s*\d{3,4}", c[0]):
        sig[num(c[0])] = float(num(c[3]))
COSMIC = 0.1200 / 0.02237; CEN = ("4486", "4472", "1399", "1316", "4374", "4649", "5846", "1407", "4636")
names = sorted(set(t1) & set(t2) & set(sig))
def fr(a0):
    out = []
    for n in names:
        Re, lms = t1[n]; Mt, fd = t2[n]; Ms = max(1 - fd, 0.05) * Mt
        y = G * Ms * Msun / (5 * Re * kpc)**2 / a0; out.append((Mt - nu(y) * Ms) / (COSMIC * Ms))
    return np.array(out)
s = np.array([sig[n] for n in names]); cen = np.array([n in CEN for n in names], float); s_true = s.copy()
if MUTATE: s = np.roll(s, 9)
def partial(a, b, c):
    ra, rb, rc = rankdata(a), rankdata(b), rankdata(c)
    res_ = lambda x: x - np.vstack([rc, np.ones_like(rc)]).T @ np.linalg.lstsq(np.vstack([rc, np.ones_like(rc)]).T, x, rcond=None)[0]
    return float(np.corrcoef(res_(ra), res_(rb))[0, 1])
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    f = fr(a0)
    print(f"   {foot}: N = {len(f)}")
    for lo in (True, False):
        for c_ in (0, 1):
            m = ((s < 250) == lo) & (cen == c_)
            lab = f"sigma {'< 250' if lo else '>= 250'}, {'central' if c_ else 'non-central'}"
            print(f"      {lab:32s} N {m.sum():2d}  median f {np.median(f[m]) if m.sum() else float('nan'):.2f}  " + ", ".join(f"{n}({sig[n]:.0f}:{v:.2f})" for n, v in zip(np.array(names)[m], f[m])))
    rs, rc = partial(f, s, cen), partial(f, cen, s)
    print(f"      rho(f, sigma) = {spearmanr(f, s).correlation:+.2f}; partial rho(f, sigma | central) = {rs:+.2f}; partial rho(f, central | sigma) = {rc:+.2f}")
    if foot == "canonical": keep = (rs, rc)
check("C the sigma values are the true assignment (MUTATE shuffles and must fail)", np.array_equal(s, s_true))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
