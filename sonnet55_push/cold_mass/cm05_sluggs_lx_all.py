"""cm05: hot-halo hypothesis on ALL SLUGGS ellipticals of the audit (17 incl. NGC 821) with X-ray luminosities from O'Sullivan+2001 (VizieR J/MNRAS/328/461).
Hot-gas indicator: log(L_X/L_B) (distance-free; total L_X includes discrete sources ~ L_B, so the ratio rises with hot gas). Upper limits used at their value.
Offsets: AUDIT_SLUGGS per-galaxy law offsets, nu_mono canonical (and alt reported).
Declared before the run: prediction rho(offset, log L_X/L_B) > 0; SUPPORTED if one-sided permutation p < 0.05 on the full matched sample, else NOT SHOWN;
robustness rows (reported, no verdict): without M87; without the 4 upper limits; alt footing.
Run: python3 cm05_sluggs_lx_all.py | MUTATE=1 shuffles L_X across galaxies (must fail R)
"""
import os, sys, json, re, numpy as np
from scipy.stats import spearmanr
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
H = os.path.dirname(os.path.abspath(__file__))
pgall = json.load(open(os.path.join(H, "..", "..", "campaign_fresh_gravity", "AUDIT_SLUGGS_2026-10-03", "audit_sluggs_recompute_results.json")))["per_galaxy"]
LX = {}
for line in open(os.path.join(H, "..", "..", "..", "_external_data", "osullivan2001_lx", "osullivan2001_table3.tsv")):
    if line.startswith("#") or not line.strip(): continue
    c = line.rstrip("\n").split("\t")
    m = re.match(r"NGC\s*(\d+)$", c[1].strip())
    if m and c[6].strip():
        try: LX[m.group(1)] = (float(c[6]) - float(c[3]), c[5].strip() == "<")
        except ValueError: pass
rng = np.random.default_rng(5)
def rp(a, b):
    r = spearmanr(a, b).correlation; perm = [spearmanr(a, rng.permutation(b)).correlation for _ in range(20000)]
    return r, float(np.mean(np.array(perm) >= r))
out = {}
for foot in ("canonical", "alt"):
    pg = pgall[f"nu_mono|{foot}"]
    names = sorted(n for n in pg if n in LX)
    off = np.array([pg[n]["off"] for n in names]); lx = np.array([LX[n][0] for n in names]); lim = np.array([LX[n][1] for n in names])
    base = lx.copy()
    if MUTATE: lx = np.roll(lx, 5)
    r, p = rp(lx, off)
    k1 = [i for i, n in enumerate(names) if n != "4486"]; r1, p1 = rp(lx[k1], off[k1])
    k2 = [i for i in range(len(names)) if not lim[i]]; r2, p2 = rp(lx[k2], off[k2])
    out[foot] = (r, p, len(names))
    if foot == "canonical":
        for n, o, l, u in zip(names, off, base, lim): print(f"   NGC {n:5s}: offset {o:+.3f}  log LX/LB {l:5.2f}{' (upper limit)' if u else ''}")
        missing = sorted(set(pg) - set(LX)); print(f"   not in O'Sullivan: {missing}")
    print(f"   {foot}: rho = {r:+.2f} (p = {p:.3f}, N = {len(names)}); without M87 {r1:+.2f} (p = {p1:.3f}); detections only {r2:+.2f} (p = {p2:.3f}, N = {len(k2)})")
r, p, N = out["canonical"]
print("   VERDICT: " + ("SUPPORTED: the ellipticals' excess rises with hot gas" if (r > 0 and p < 0.05) else "NOT SHOWN"))
true_r = spearmanr(np.array([LX[n][0] for n in sorted(n for n in pgall["nu_mono|canonical"] if n in LX)]), np.array([pgall["nu_mono|canonical"][n]["off"] for n in sorted(n for n in pgall["nu_mono|canonical"] if n in LX)])).correlation
check("R the reported rho uses the true L_X assignment (MUTATE shuffles and must fail)", abs(r - true_r) < 1e-9)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
