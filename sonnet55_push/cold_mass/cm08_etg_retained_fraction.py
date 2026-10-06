"""cm08: express the early types' extra mass (cm07) as the SAME retained cold fraction used for groups/clusters (cm02/cm03 definition A, calibrated on X-COP):
f = (M_tot - M_law) / ((Omega_c/Omega_b) M_b), with M_b = M*(<5Re) (Alabi+17; hot gas negligible inside 5 Re, CFG57). Compare: spirals <= 0.105 (ledger),
Milky Way 0.14, groups 0.55 (X-ray) / 1.38 (WL-bias, def A; 0.60 def B), X-COP clusters 0.576.  Reported, no verdict (descriptive).
Note: v1's check R (median in [0.2, 1]) could not fail under MUTATE (0.45 is in band); replaced before writing up.
Run: python3 cm08_etg_retained_fraction.py | MUTATE=1 drops the law's phantom (M_law = M_b): f must rise (check R fails)
"""
import os, sys, math, numpy as np
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cm07_alabi32_hot_halo.py")).read().split("names = sorted(")[0]
exec(src)
COSMIC = 0.1200 / 0.02237
out = {}
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    fs, cen = [], []
    for n in sorted(set(t1) & set(t2)):
        Re, lms = t1[n]; Mt, fd = t2[n]; Ms = max(1 - fd, 0.05) * Mt
        y = G * Ms * Msun / (5 * Re * kpc)**2 / a0
        Ml = Ms if MUTATE else nu(y) * Ms
        fs.append((Mt - Ml) / (COSMIC * Ms)); cen.append(n in ("4486", "4472", "1399", "1316", "4374", "4649", "5846", "1407", "4636"))
    fs, cen = np.array(fs), np.array(cen)
    out[foot] = float(np.median(fs))
    print(f"   {foot}: retained f at 5 Re, all 32: median {np.median(fs):.2f} (16-84% {np.percentile(fs,16):.2f}..{np.percentile(fs,84):.2f});"
          f" group/cluster centrals {np.median(fs[cen]):.2f} (N {cen.sum()}); others {np.median(fs[~cen]):.2f} (N {(~cen).sum()})")
nophant = []
for n in sorted(set(t1) & set(t2)):
    Re, lms = t1[n]; Mt, fd = t2[n]; Ms = max(1 - fd, 0.05) * Mt; nophant.append((Mt - Ms) / (COSMIC * Ms))
check("R the reported fractions include the law's phantom (differ from the no-phantom value by > 0.05; MUTATE removes the phantom and must fail)", abs(out["canonical"] - float(np.median(nophant))) > 0.05)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
