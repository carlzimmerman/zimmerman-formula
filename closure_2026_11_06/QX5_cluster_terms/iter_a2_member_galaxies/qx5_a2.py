#!/usr/bin/env python3
"""QX5 iter a2 (criteria 51ef07f3cc): class a's lead on Coma UDGs. python3 qx5_a2.py [--mutate]
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import csv, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar"))
import d10_solver as S  # read-only
MUT = "--mutate" in sys.argv; TAG = "qx5_a2_MUTATE" if MUT else "qx5_a2"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
S1 = os.path.join(REPO, "rebuild_2026_10_22", "S1_v3_hosted_small")
rows = list(csv.DictReader(open(os.path.join(S1, "s1_coma_per_galaxy.csv"))))
R1 = json.load(open(os.path.join(S1, "s1_v3_hosted_small_results.json")))["coma"]
Q5 = json.load(open(os.path.join(HERE, "..", "qx5.json")))
G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
GR = S.Grid2D(nper=24, Nt=16); rf = GR.re[1:-1]
def woN(y): return S.jeans(rf, S.plummer_gN(rf, y), [])[2]
RES = dict(tag=TAG, note="kappa = 1/2 FITTED; not theory closed")
for f, a0 in A0.items():
    gal = [r for r in rows if r["footing"] == f]
    st = R1[f"{f}|S4 v3 dmean L*floor E-W"]; stot = math.hypot(st["se"], st["sigma_sys"])
    Fr = Q5["a"][f]["XCOP_F_required"]; Fs = dict(F1=1.0, F_med=Fr["median"], F_max=Fr["max"]) if not MUT else dict(F30=30.0)
    per = []
    for r in gal:
        y = float(r["y_plummer"]); E = float(r["E_v3_dmean"]); sig = float(r["sigma"]) * 1e3; a = float(r["Re_kpc"]) * 1e3 * PC
        wo_v3 = sig ** 2 * math.exp(-E) / (a0 * a); rN = woN(y) / wo_v3
        per.append(dict(name=r["name"], E_v3=E, rN=rN))
    out = {}
    for lab, F in Fs.items():
        EF = [p["E_v3"] - math.log(p["rN"] + F * (1 - p["rN"])) for p in per]; m = sum(EF) / len(EF)
        out[lab] = dict(F=F, meanE=m, z=m / stot)
        P(f"[{f}] {lab} F={F:.2f}: mean E_F {m:+.3f} ln ({m / math.log(10):+.3f} dex), z {m / stot:+.2f} (sigma_tot {stot:.3f})")
    lo, hi = 1.0, 1e4
    def mE(F): return sum(p["E_v3"] - math.log(p["rN"] + F * (1 - p["rN"])) for p in per) / len(per)
    for _ in range(100):
        mid = math.sqrt(lo * hi); lo, hi = (mid, hi) if mE(mid) > 0 else (lo, mid)
    F0 = math.sqrt(lo * hi)
    P(f"[{f}] REPORTED: F for mean E_F = 0: {F0:.1f}; r_N range {min(p['rN'] for p in per):.3f}-{max(p['rN'] for p in per):.3f}")
    if not MUT:
        ka = abs(out["F1"]["meanE"] - st["meanE"]); P(f"[{f}] KA F=1 vs S1 mean {st['meanE']:+.6f}: |d| {ka:.1e} -> {'PASS' if ka <= 1e-6 else 'FAIL'}")
        zmax, zmed = out["F_max"]["z"], out["F_med"]["z"]
        lab = "LEAD KILLED" if zmax >= 3 else ("LEAD ALIVE" if abs(zmed) < 3 else "UNDECIDED")
        out.update(KA=ka, F_zero=F0, verdict_footing=lab); P(f"[{f}] footing reading: {lab}")
    else:
        out["bites"] = out["F30"]["meanE"] < 1.0; P(f"[{f}] MUTATE F=30 mean E_F < +1.0: {'BITES' if out['bites'] else 'NO BITE'}")
    RES[f] = dict(per=per, **out)
if not MUT:
    v = [RES[f]["verdict_footing"] for f in A0]
    RES["label"] = "LEAD KILLED (class a DEAD-BY-MEMBERS)" if all(x == "LEAD KILLED" for x in v) else ("LEAD ALIVE (CLUSTER-SET)" if all(x == "LEAD ALIVE" for x in v) else "UNDECIDED")
    P(f"LABEL: {RES['label']}")
json.dump(RES, open(os.path.join(HERE, f"{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n")
