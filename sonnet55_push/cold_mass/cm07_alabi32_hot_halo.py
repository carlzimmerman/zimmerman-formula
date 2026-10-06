"""cm07: hot-halo hypothesis on the 32 SLUGGS early types of Alabi+2017 (GC tracer-mass-estimator M_tot(<5 Re), beta = 0 rows; their f_DM gives the stellar mass
inside 5 Re: M*(<5Re) = (1 - f_DM) M_tot) with O'Sullivan+2001 L_X/L_B. Law (kernel nu_mono, canonical a0 = 9.3603e-11; alt reported):
g_N = G M*(<5Re)/(5 Re)^2 (spherical enclosed), M_law = nu(g_N/a0) M*(<5Re); excess = log10(M_tot / M_law).
Declared before the run (same rule as cm05/cm05b): SUPPORTED if rho(excess, log LX/LB) > 0 with one-sided permutation p < 0.05 AND the partial rho given log M*
> 0.3 with p < 0.1. Hot gas is not added to the baryons (CFG57: it moves the law by ~0.01 dex). Stellar M/L is Alabi's (age-dependent), shared by all.
FIX (before any reading): the first run parsed only 16 Table-2 rows (the table continues in a second table* block); kept as cm07_alabi32_hot_halo_v1_16rows.out.
Run: python3 cm07_alabi32_hot_halo.py | MUTATE=1 shuffles L_X/L_B (check S must fail)
"""
import os, re, sys, math, numpy as np
from scipy.stats import spearmanr, rankdata
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
H = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(H, "..", "..", "..", "_external_data")
tex = open(os.path.join(EXT, "alabi2017", "src", "halov3.tex")).read()
num = lambda s: re.sub(r"[^0-9.\-]", "", s.split("^")[0].split("_")[0])
# Table 1
t1 = {}
for line in tex.split("\\begin{table*}")[1].split("\n"):
    c = [x.strip() for x in line.split("&")]
    if len(c) >= 12 and re.match(r"^\$?\s*\d{3,4}", c[0]):
        try: t1[num(c[0])] = (float(num(c[9])), float(num(c[10])))   # Re [kpc], log M*
        except ValueError: pass
# Table 2 (beta = 0 rows)
t2 = {}
for line in (tex.split("\\begin{table*}")[2] + tex.split("\\begin{table*}")[3]).split("\n"):
    c = [x.strip() for x in line.split("&")]
    if len(c) >= 6 and re.match(r"^\$\s*\d{3,4}\s*\$", c[0]) and re.match(r"^\$\s*0\s*\$", c[1]):
        mt = float(c[4].strip("$").split("\\pm")[0]); fd = float(c[5].strip("$").split("\\pm")[0])
        t2[num(c[0])] = (mt * 1e11, fd)
LX = {}
for line in open(os.path.join(EXT, "osullivan2001_lx", "osullivan2001_table3.tsv")):
    if line.startswith("#") or not line.strip(): continue
    c = line.rstrip("\n").split("\t"); m = re.match(r"NGC\s*(\d+)$", c[1].strip())
    if m and c[6].strip():
        try: LX[m.group(1)] = (float(c[6]) - float(c[3]), c[5].strip() == "<")
        except ValueError: pass
G, Msun, kpc = 6.674e-11, 1.989e30, 3.0857e19
def nu(y): return math.sqrt(1 + 1 / y)   # nu_mono is the record's kernel name for this quadrature law
names = sorted(n for n in t1 if n in t2 and n in LX)
print(f"   Alabi Table 1: {len(t1)}, Table 2 (beta = 0): {len(t2)}, with O'Sullivan L_X: {len(names)}; missing L_X: {sorted(set(t1) & set(t2) - set(LX))}")
rows = {}
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    ex, lx, lm = [], [], []
    for n in names:
        Re, lms = t1[n]; Mt, fd = t2[n]; Ms5 = max(1 - fd, 0.05) * Mt
        y = G * Ms5 * Msun / (5 * Re * kpc)**2 / a0
        ex.append(math.log10(Mt / (nu(y) * Ms5))); lx.append(LX[n][0]); lm.append(lms)
    ex, lx, lm = map(np.array, (ex, lx, lm))
    truth = lx.copy()
    if MUTATE: lx = np.roll(lx, 7)
    rng = np.random.default_rng(7)
    r = spearmanr(lx, ex).correlation; p = float(np.mean([spearmanr(rng.permutation(lx), ex).correlation >= r for _ in range(20000)]))
    def resid(a, b): A = np.vstack([b, np.ones_like(b)]).T; return a - A @ np.linalg.lstsq(A, a, rcond=None)[0]
    ro, rx = resid(rankdata(ex), rankdata(lm)), resid(rankdata(lx), rankdata(lm))
    pr = float(np.corrcoef(ro, rx)[0, 1]); pp = float(np.mean([np.corrcoef(ro, rng.permutation(rx))[0, 1] >= pr for _ in range(20000)]))
    k = [i for i, n in enumerate(names) if n not in ("4486", "4472", "1399", "1316", "4374", "4649", "5846", "1407", "4636")]
    rk = spearmanr(lx[k], ex[k]).correlation
    rows[foot] = (r, p, pr, pp, len(names), rk, len(k), float(np.median(ex)), spearmanr(truth, ex).correlation)
    print(f"   {foot}: median excess {np.median(ex):+.3f} dex; rho(excess, LX/LB) = {r:+.2f} (p = {p:.3f}, N = {len(names)}); partial | M* = {pr:+.2f} (p = {pp:.3f});"
          f" without 9 group/cluster-dominant galaxies {rk:+.2f} (N = {len(k)})")
r, p, pr, pp = rows["canonical"][:4]
ok = r > 0 and p < 0.05 and pr > 0.3 and pp < 0.1
print("   VERDICT: " + ("SUPPORTED (excess tracks hot gas beyond mass)" if ok else "NOT SUPPORTED on the larger sample"))
check("S the reported rho is the one from the true L_X assignment (MUTATE shuffles and must fail)", abs(rows["canonical"][0] - rows["canonical"][8]) < 1e-9)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
