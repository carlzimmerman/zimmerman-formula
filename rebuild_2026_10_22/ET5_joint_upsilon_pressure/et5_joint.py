#!/usr/bin/env python3
"""ET5_joint_upsilon_pressure: Upsilon trend, pressure support and beam cut together against the flat floor.
python3 et5_joint.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, sys
HERE5 = os.path.dirname(os.path.abspath(__file__)); REB5 = os.path.dirname(HERE5); ET3D = os.path.join(REB5, "ET3_low_mass_systematics")
MUT5 = "--mutate" in sys.argv; SRC3 = open(os.path.join(ET3D, "et3_sys.py")).read()
__file__ = os.path.join(ET3D, "et3_sys.py"); sys.argv = [sys.argv[0]]; exec(compile(SRC3[:SRC3.index('W(f"ET3 systematics')], "et3_head", "exec"))
L5 = []; _W = W
def W(s): print(s, flush=True); L5.append(s)
def iu_of(v, s): return int(np.argmin(abs(UPS - np.clip(0.50 * (v / 80) ** s, UPS[0], UPS[-1]))))
def real(s, sig, fw, tag):
    S = []
    for q in SAMPLE:
        i = iu_of(TAB[q["name"]]["vf"], s); c, go = var(q, fw=fw, sig=sig)
        S.append(fit(c, i, go)[0] if c["OK"][:, i].sum() >= 5 else None)
    r = grade(NM5, S, tag); r["S"] = S; return r
def contains(r, v): return all(b["ci"][0] <= v <= b["ci"][1] for b in r["bins"].values())
def fwd(S0, s, sig, fw, tag, fit_trend=False):
    global iu
    S = []
    for q in SAMPLE:
        iu = iu_of(TAB[q["name"]]["vf"], s); g = forward(q, S0, fw, sig)
        if fit_trend:
            c = dict(q); S.append(fit(c, iu, np.log10(10 ** g + (sig * KM) ** 2 / rd(q)))[0])
        else: S.append(fit(q, I05, g)[0])
    return grade(NM5, S, tag)
NM5 = [q["name"] for q in SAMPLE]
W(f"ET5 joint; kappa = 1/2 FITTED; footings never pooled; not theory closed{' [MUTATE]' if MUT5 else ''}\nsample {len(SAMPLE)}")
RES = dict(mutate=MUT5); code = 0
if MUT5:
    r = fwd(FL["canonical"], 0.25, 12, 0, "exact fit", True); ok = all(98 <= b["med"] <= 118 for b in r["bins"].values()) and r["p"] >= 0.01; code = int(not ok); RES["mut"] = r; W(f"MUTATE recovered floor and no rise: {ok}")
else:
    et2 = json.load(open(os.path.join(REB5, "ET2_free_core_low_mass", "et2_results.json")))["ups"]["0.50"]["gal"]; e3 = json.load(open(os.path.join(ET3D, "et3_results.json")))["P1"]; e4 = json.load(open(os.path.join(REB5, "ET4_upsilon_trend", "et4_results.json")))["T1"]["0.25"]
    W("\nPart 1 real curves"); C = {}
    for s in (0, 0.25, 0.5):
        for sig in (0, 8, 12):
            for fw in (0, 30): C[f"s{s}_p{sig}_b{fw}"] = real(s, sig, fw, f"s{s} p{sig} b{fw}")
    k1 = all(x == et2[n]["S"] for x, n in zip(C["s0_p0_b0"]["S"], NM5)); W(f"\nK1 equals ET2 per galaxy: {'PASS' if k1 else 'FAIL'}"); code |= not k1
    def same(a, b): return abs(a["rho"] - b["rho"]) < 1e-9 and all(abs(a["bins"][k]["med"] - b["bins"][k]["med"]) < 1e-9 for k in a["bins"])
    k2 = [same(C["s0.25_p0_b0"], e4), same(C["s0_p12_b0"], e3["P12"]), same(C["s0_p0_b30"], e3["B30"])]; W(f"K2 reproduce ET4 s 0.25, ET3 P12, B30: {k2}: {'PASS' if all(k2) else 'FAIL'}"); code |= not all(k2)
    V = {}
    for f, v in FL.items():
        rec = {k: contains(r, v) and r["p"] >= 0.01 for k, r in C.items()}; con = {k: contains(r, v) for k, r in C.items()}; al = [k for k in C if not k.startswith("s0.5_")]; be = [k for k in C if k.startswith("s0.5_")]
        a = [k for k in al if rec[k]]; b = [k for k in be if rec[k]]; c = [k for k in al if con[k]]
        vd = "JOINT EXPLAINS IT" if a else ("JOINT EXPLAINS IT ONLY BEYOND THE BAND" if b else ("FLOOR CONSISTENT, RISE REMAINS" if c else "NOT RECONCILED")); V[f] = dict(verdict=vd, reconciled_allowed=a, reconciled_beyond=b, contains_allowed=c, contains_beyond=[k for k in be if con[k]]); W(f"VERDICT {f}: {vd}\n   reconciled allowed {a}\n   reconciled beyond {b}\n   floor contained, allowed {c}; beyond {V[f]['contains_beyond']}")
    W("\nPart 2 forward"); F = {}
    for f, v in FL.items():
        F[f] = {}
        for s in (0.25, 0.5):
            for sig in (8, 12):
                for fw in (0, 30):
                    r = fwd(v, s, sig, fw, f"{f[:3]} s{s} p{sig} b{fw}"); a_, c_ = r["bins"]["20-60"]["med"], r["bins"]["100-150"]["med"]; r["verdict"] = ("FAKED" if a_ <= 77.3 and c_ >= 136.6 else "PARTIAL") if r["rise"] else "NOT FAKED"; F[f][f"s{s}_p{sig}_b{fw}"] = r; W(f"   -> {r['verdict']}")
        od = ("NOT FAKED", "PARTIAL", "FAKED")
        for s in ("0.25", "0.5"): W(f"WORST {f} s {s}: {max((r['verdict'] for k, r in F[f].items() if k.startswith('s' + s + '_')), key=od.index)}")
    RES.update(C=C, V=V, F=F, K=dict(K1=k1, K2=k2))
t = "_MUTATE" if MUT5 else ""
json.dump(RES, open(os.path.join(HERE5, f"et5_results{t}.json"), "w"), indent=1, default=lambda o: o.item()); open(os.path.join(HERE5, f"et5{t}.out"), "w").write("\n".join(L5) + "\n"); sys.exit(int(code))
