"""D8 Part 3b -- frozen sigma_c rule on Stilp+2013 (arXiv:1301.1989) superprofile table. Criteria: FROZEN_CRITERIA.md AMENDMENT A2 (95a7ec3a41).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -I d8_stilp2013.py   (D8S_MUTATE=1: corrupt expected sha -> K1 fails). kappa = 1/2 FITTED."""
import os, sys, re, json, math, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("D8S_MUTATE") == "1"
PC = 3.0856775814913673e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
L_CEIL = 90.0
SHA = "155d780cf9064d904529b04924d431519b065933b6844fdc34fce220dfdd5ac1"
if MUT: SHA = "0" * 64
base = json.load(open(os.path.join(HERE, "d8_lstar_value_results.json")))
FLOOR = {f: base["part2"][f]["L95_fine_pc"] for f in A0}
OUT, CH, RES = [], [], {"lane": "D8_Lstar_value/stilp2013", "mutate": MUT, "floor_pc": FLOOR}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(i, ok, v, t, w): CH.append(dict(id=i, ok=bool(ok), value=v, threshold=t, what=w)); P(f"{i} {'PASS' if ok else 'FAIL'} {v} {t}   # {w}")
path = os.path.join(HERE, "stilp2013_table-measurements.tex")
raw = open(path, "rb").read(); h = hashlib.sha256(raw).hexdigest()
body = raw.decode().split("\\startdata")[1].split("\\enddata")[0]
rows = []
for l in body.strip().split("\\\\"):
    l = l.strip()
    if not l: continue
    c = [x.strip() for x in l.split("&")]
    m2 = float(c[1]); cen = re.findall(r"[\d.]+", c[2]); rows.append(dict(name=c[0], s_m2=m2, s_cen=float(cen[0]), e_cen=float(cen[1])))
check("K1", h == SHA and len(rows) == 23, f"sha {h[:12]}..., n {len(rows)}", "sha match, n = 23", "table integrity")
def summ(sig, a0):
    L = np.array([(s * 1e3) ** 2 / a0 / PC for s in sig])
    return dict(n=len(L), median=float(np.median(L)), p16=float(np.percentile(L, 16)), p84=float(np.percentile(L, 84)),
                ratio_84_16=float(np.percentile(L, 84) / np.percentile(L, 16)), min=float(L.min()), max=float(L.max()),
                frac_in_window=float(np.mean((L >= 0) & (L <= L_CEIL))), L_each=[float(x) for x in L])
def cls(s, f):
    if s["median"] < FLOOR[f]: return f"TENSION (below CFG820 floor {FLOOR[f]:.2f} pc)"
    if s["median"] > L_CEIL: return "TENSION (above 90 pc ceiling)"
    return "CONSISTENT"
plant = summ([math.sqrt(A0["canonical"] * 50 * PC) / 1e3] * 23, A0["canonical"])
check("K2", abs(plant["median"] - 50) < 1e-9, f"{plant['median']:.12f}", "50 pc (1e-9)", "planted control")
P(f"sigma_m2: median {np.median([r['s_m2'] for r in rows]):.2f} km/s, range {min(r['s_m2'] for r in rows)}-{max(r['s_m2'] for r in rows)}; "
  f"sigma_central: median {np.median([r['s_cen'] for r in rows]):.2f} km/s")
for lab, key, wt in (("PRIMARY <sigma_m2>", "s_m2", "verdict"), ("SECONDARY sigma_central", "s_cen", "no verdict weight")):
    RES[key] = {}
    for f, a0 in A0.items():
        s = summ([r[key] for r in rows], a0); s["class"] = cls(s, f); s["one_constant"] = s["ratio_84_16"] <= 2
        s["frac_ge_floor"] = float(np.mean(np.array(s["L_each"]) >= FLOOR[f])); s["frac_in_window"] = float(np.mean((np.array(s["L_each"]) >= FLOOR[f]) & (np.array(s["L_each"]) <= L_CEIL)))
        RES[key][f] = s
        P(f"P3b {lab} [{f:9s}] L* median {s['median']:.2f} pc (16-84 {s['p16']:.2f}-{s['p84']:.2f}; 84/16 {s['ratio_84_16']:.3f}; "
          f"min-max {s['min']:.1f}-{s['max']:.1f}); in [floor,90]: {s['frac_in_window']*100:.0f}% -> {s['class']}; "
          f"{'one constant (84/16 <= 2)' if s['one_constant'] else 'NOT one constant'}  [{wt}]")
RES["rows"] = rows; RES["checks"] = CH; n = sum(c["ok"] for c in CH)
P(f"\nD8_STILP2013 COMPLETE: {n}/{len(CH)} checks PASS.")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"d8_stilp2013_results{sfx}.json"), "w"), indent=1)
open(os.path.join(HERE, f"d8_stilp2013{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n == len(CH) else 1)
