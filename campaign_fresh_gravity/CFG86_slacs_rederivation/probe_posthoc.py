# POST-HOC probe (after the pre-declared run; reported as post-hoc): halo-off gap, crossing multipliers, paired-error sensitivity
import os, math, numpy as np
src = open("CFG86_lcdm_slacs_rederivation.py").read()
ns = {"__file__": os.path.abspath("CFG86_lcdm_slacs_rederivation.py"), "__name__": "probe"}
pre = src.split("# =============================== CONTROLS")[0]
exec(compile(pre, "probe_pre", "exec"), ns)
run_cfg, Cfg = ns["run_cfg"], ns["Cfg"]
r0 = run_cfg(Cfg(mult=1e-30), nboot=1000)
print("halo OFF (mult 1e-30): Delta %+.4f err %.4f zstat %+.2f" % (r0["delta"], r0["err"], r0["zstat"]))
# multiplier where zstat crosses +2 (z0, solved_salp) and where Delta crosses B's alt-V gap
lo, hi = 0.05, 1.0
for _ in range(30):
    mid = math.sqrt(lo*hi); r = run_cfg(Cfg(mult=mid), nboot=400)
    if r["zstat"] > 2: lo = mid
    else: hi = mid
print("multiplier at which LCDM z_stat=+2 (z0, solved Salp tie): m* ~ %.3f" % math.sqrt(lo*hi))
# fraction of the 54 cells that would pass S_b if the B-LCDM error were the paired 0.016 instead of unpaired
import json
js = json.load(open("CFG86_results_main.json"))
core = [g for g in js["grid"] if float(g["axes"][0]) in (1/3, 1.0, 3.0)]
for be in (0.022, 0.016):
    n = sum(1 for g in core if (0.152 - g["delta"]) > 2 * math.sqrt(be**2 + 0*g["err"]**2 + 0.0**2 + (g["err"]**2 if be==0.022 else 0.0)))
    print("S_b count (B altV) with combined error =", "unpaired" if be==0.022 else "fixed 0.016", n, "/54")
# B-LCDM difference stats over the 54
d = [0.152 - g["delta"] for g in core]
print("B(altV)-LCDM over 54 cells: min %+.3f median %+.3f max %+.3f" % (min(d), np.median(d), max(d)))
d2 = [0.159 - g["delta"] for g in core]
print("B(canV)-LCDM: min %+.3f median %+.3f max %+.3f" % (min(d2), np.median(d2), max(d2)))
# which cells have S_a fail AND are z-consistent
print("z-consistent cells (27): S_a", sum(g["Sa"] for g in core if g["axes"][2]=="full"), " z0 cells:", sum(g["Sa"] for g in core if g["axes"][2]=="z0"))
print("Sa fails among z0 & solved_salp & m=1:", [ (g['axes'][3], round(g['delta'],3)) for g in core if g['axes'][0]=='1.0' and g['axes'][1]=='solved_salp' and g['axes'][2]=='z0'])
