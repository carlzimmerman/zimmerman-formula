"""cm04: the hot-halo hypothesis (cold mass retained only where a hot X-ray atmosphere exists) on the SLUGGS ellipticals with MEASURED hot gas.
Inputs (committed, read-only): per-galaxy outer-GC law offsets log(sigma_obs/sigma_law), nu_mono canonical (AUDIT_SLUGGS_2026-10-03 results json);
hot-gas masses within 20 kpc from CFG57 (Lakhchaura+18 / Fukazawa+06; the 7 covered galaxies); stellar/JAM mass lMjamlaw (same json).
Prediction declared before the run: offset rises with the hot-gas fraction x = M_gas(<20 kpc)/M_* (Spearman rho > 0). Power is low (N = 7): the check is
only that the SIGN and size are reported with a permutation p-value; a positive rho with p < 0.05 = SUPPORTED, else NOT SHOWN (not 'refuted').
Also reported: the same with M_gas(<20) unnormalised, and a leave-out of M87 (cluster centre, its GCs may include intracluster ones).
Run: python3 cm04_sluggs_hot_halo.py | MUTATE=1 shuffles the gas values across galaxies (rho must change)
"""
import os, sys, json, numpy as np
from scipy.stats import spearmanr
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
CFG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "campaign_fresh_gravity")
pg = json.load(open(os.path.join(CFG, "AUDIT_SLUGGS_2026-10-03", "audit_sluggs_recompute_results.json")))["per_galaxy"]["nu_mono|canonical"]
txt = open(os.path.join(CFG, "CFG57_sluggs_hot_gas.out")).read()
import re
gas = {m.group(1): float(m.group(2)) for m in re.finditer(r"NGC(\d+) src\d M_gas\(<r12\) [0-9.e+]+, \(<20 kpc\) ([0-9.e+]+)", txt)}
names = sorted(gas)
off = np.array([pg[n]["off"] for n in names]); mg = np.array([gas[n] for n in names]); ms = np.array([10**pg[n]["lMjamlaw"] for n in names])
if MUTATE: mg = np.roll(mg, 3)
x = mg / ms
rng = np.random.default_rng(4)
def rho_p(a, b):
    r = spearmanr(a, b).correlation; perm = [spearmanr(a, rng.permutation(b)).correlation for _ in range(20000)]
    return r, float(np.mean(np.array(perm) >= r))
for n, o, g, f in zip(names, off, mg, x): print(f"   NGC {n:5s}: offset {o:+.3f} dex  M_gas(<20 kpc) {g:.2e}  gas/M* {f:.4f}")
r1, p1 = rho_p(x, off); r2, p2 = rho_p(mg, off)
keep = [i for i, n in enumerate(names) if n != "4486"]; r3, p3 = rho_p(x[keep], off[keep])
print(f"   rho(offset, gas/M*) = {r1:+.2f} (p = {p1:.3f});  rho(offset, M_gas) = {r2:+.2f} (p = {p2:.3f});  without M87: {r3:+.2f} (p = {p3:.3f})")
print("   VERDICT: " + ("SUPPORTED (offset rises with hot gas)" if (r1 > 0 and p1 < 0.05) else "NOT SHOWN at N = 7"))
base = spearmanr(np.array([gas[n] for n in names]) / ms, off).correlation
check("R the reported rho is the one computed from the unshuffled gas values (MUTATE shuffles them and must fail)", np.isfinite(r1) and abs(r1 - base) < 1e-9)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
