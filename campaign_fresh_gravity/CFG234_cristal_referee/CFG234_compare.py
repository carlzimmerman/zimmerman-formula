"""CFG234 POST-COMPARISON (written AFTER my own main/MUTATE/attack runs were saved; not part of any frozen result): cell-by-cell comparison with CFG213's
committed results JSON (opened only now), and a reading of its C2 control. Reports; exit 0."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG234_common import *
t = start("CFG234_compare")
J = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG213_dysmalpy_two_sided", "cfg213_two_sided_results.json")))["numbers"]
# my recompute of every cell CFG213 reports: Z5 (12 disks; alpha 3.36/1.68/0; fit + route(recompute); kernel; footing; law) and Z1.4
df = load_cristal(); d12 = df.loc[ID12]; d9 = df.loc[ROUTE9]; rf9 = route_factor(d9)
dn = load_noema(); fn, Vrot2 = noema_frame(dn); rn = noema_route_factor(fn)
B = 10000
worst = dict(med=0.0, lo=0.0, hi=0.0); nc = 0; nclass = 0; where = {}
for binname, cellfun in (("Z5 (CRISTAL primary)", "z5"), ("Z1.4 (NOEMA3D)", "z14")):
    for key, v in J[binname].items():
        a, rt, kn, ft, law = key.split("|"); a = float(a)
        if cellfun == "z5":
            if rt == "fit": dl = cell(d12, k=a, kernel=kn.replace("nu_mono", "mono").replace("P2", "p2"), foot=ft, rival=(law == "rival"))[0]
            else: dl = cell(d9, k=a, kernel=kn.replace("nu_mono", "mono").replace("P2", "p2"), foot=ft, rival=(law == "rival"), gbar_mul=rf9, route="recompute")[0]
        else:
            if rt == "fit": dl = cell_noema(fn, Vrot2, k=a, kernel=kn.replace("nu_mono", "mono").replace("P2", "p2"), foot=ft, rival=(law == "rival"))[0]
            else: dl = cell_noema(fn, Vrot2, k=a, kernel=kn.replace("nu_mono", "mono").replace("P2", "p2"), foot=ft, rival=(law == "rival"), gbar_mul=rn, route="recompute")[0]
        s = stat(dl, 234, B)
        dm, dlo, dhi = abs(s["med"] - v["med"]), abs(s["lo"] - v["lo"]), abs(s["hi"] - v["hi"])
        for k_, d_ in (("med", dm), ("lo", dlo), ("hi", dhi)):
            if d_ > worst[k_]: worst[k_] = d_; where[k_] = (binname, key)
        lab = {"over": "DISFAVOURED-over", "under": "DISFAVOURED-under", "CONS": "CONSISTENT"}[s["cls"]]
        nc += 1; nclass += int(lab != v["v"])
print(f"cells compared: {nc}; class labels different: {nclass}")
print("largest |mine - CFG213| over all cells: median {med:.2e}, CI lower edge {lo:.2e}, CI upper edge {hi:.2e}".format(**worst))
print("where:", where)
print("(bootstrap: mine default_rng seed 234, its default_rng seed 213 with one index array per n; the CI-edge differences are Monte Carlo, the medians are deterministic.)")
src = open(os.path.join(REPO, "campaign_fresh_gravity", "CFG213_dysmalpy_two_sided", "cfg213_two_sided.py")).read()
i = src.index("c2 = []"); print("\nCFG213's C2 as written:\n" + src[i:i + 640])
print("-> Dexact and the compared prediction are both nu1(nu, gb / a0) at the SAME argument: log10(x / x) = 0 by construction, so the check cannot fail (the same construction as CFG216's C1, CFG233 section 3 / CFG217).")
print("   Its C1 (kernel round trip through ystar) is a real check; its C3 is 'reported' with load_bearing=False and a hard-coded True; its MUTATE (every D x 1.5 raises every median by log10 1.5) is an identity of the median and cannot fail.")
