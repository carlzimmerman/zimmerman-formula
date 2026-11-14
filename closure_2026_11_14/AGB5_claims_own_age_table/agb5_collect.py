"""AGB5 collector: applies the known-answer checks and the frozen word of FROZEN_CRITERIA.md to the outputs of
agb5_run.py. Writes agb5_results.json; prints the tables (redirect to agb5_collect.out). It fits nothing."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUTDIR = sys.argv[1] if len(sys.argv) > 1 else HERE
TAG = "_boot" if len(sys.argv) > 2 and sys.argv[2] == "boot" else ""; NOTE = " (amendment 1)" if TAG else ""   # AMENDMENT_1.md: bootstrap errors
load = lambda n: json.load(open(os.path.join(OUTDIR, f"agb5_{n}{TAG if n in ('K4', 'L') else ''}.json")))


def word6(d0, d1):
    if d1 >= 9 and d0 < 4: return "AGE BIAS EXCLUDED AT 3 SIGMA"
    if 4 <= d1 < 9 and d0 < 4: return "AGE BIAS DISFAVOURED"
    if d0 >= 9 and d1 < 4: return "AGE BIAS REQUIRED AT 3 SIGMA"
    if 4 <= d0 < 9 and d1 < 4: return "AGE BIAS FAVOURED"
    if d0 < 4 and d1 < 4: return "UNDECIDED"
    return "NEITHER"


KA, K1, K3, K4, L = (load(k) for k in ("KA", "K1", "K3", "K4", "L")); pf = lambda b: "PASS" if b else "FAIL"; res = dict(lane="AGB5")
print("AGB5 known-answer checks")
print(f"  KA published slopes: plain {KA['plain_t2']['beta']:+.4f}, {KA['plain_t1']['beta']:+.4f}, combined {KA['combined']['slope']:+.4f} (A {KA['combined']['A']:+.3f} +- {KA['combined']['sd_A']:.3f});"
      f" structural {KA['struct_t2']['beta']:+.4f}, {KA['struct_t1']['beta']:+.4f}, {KA['struct_t1_orig']['beta']:+.4f} -> {pf(KA['passed'])}")
print(f"  K1 tables: {K1['n1']} and {K1['n2']} rows, {K1['shared']} shared -> {pf(K1['passed'])}")
print(f"  K3 twins: {sum(t['passed'] for t in K3['twins'])} of {len(K3['twins'])} -> {pf(K3['passed'])}")
for t in ("table1", "table2"):
    if TAG: print(f"  K4 amended {t}: bootstrap / sigma {K4[t]['bootstrap_over_sigma']:.3f}; shuffle with the fitted signal removed / sigma {K4[t]['shuffle_no_signal_over_sigma']:.3f} -> {pf(K4[t]['passed'])}")
    else: print(f"  K4 {t}: shuffle mean {K4[t]['mean_over_sigma']:+.3f} sigma; shuffle scatter / sigma {K4[t]['shuffle_over_sigma']:.3f}; bootstrap / sigma {K4[t]['bootstrap_over_sigma']:.3f} -> {pf(K4[t]['passed'])}")
ok = all((KA["passed"], K1["passed"], K3["passed"], K4["passed"])); res["checks"] = dict(KA=KA["passed"], K1=K1["passed"], K3=K3["passed"], K4=K4["passed"])
F = L["fits"]; first = word6(F["primary"]["D_A0"], F["primary"]["D_A1"]); oth = {k: word6(v["D_A0"], v["D_A1"]) for k, v in F.items() if k != "primary"}
print(f"\nL1, plain line with a mass step free ({'evaluable' if ok else 'NOT EVALUABLE'}); A in units of the published slope")
print(f"  no step (the published configuration): A {KA['combined']['A']:+.3f} +- {KA['combined']['sd_A']:.3f}" + (f"; with bootstrap errors {L['no_step']['A']:+.3f} +- {L['no_step']['sd_A']:.3f}" if TAG else ""))
for k, v in F.items(): print(f"  {k:20s} A {v['A']:+.3f} +- {v['sd_A']:.3f}  dchi2(A=0) {v['D_A0']:6.2f}  dchi2(A=1) {v['D_A1']:6.2f}   {first if k == 'primary' else oth[k]}")
bad = [k for k, w in oth.items() if w != first]; sec = "ROBUST" if not bad else "FRAGILE (" + "; ".join(f"{k}: {oth[k]}" for k in bad) + ")"
res["L1"] = dict(fit=F["primary"], first=first, forks=oth, word=f"{first} / {sec}{NOTE}" if ok else "NOT EVALUABLE"); print(f"  -> L1: {res['L1']['word']}")
print("\nReported only"); R = L["reported"]
for t in ("table1", "table2"):
    r = R[t]; print(f"  {t}: no step {r['no_step']['beta']:+.4f} +- {r['no_step']['sd_beta']:.4f}; with step {F['primary'][t]['beta']:+.4f} +- {F['primary'][t]['sd_beta']:.4f} and g {F['primary'][t]['g']:+.3f} +- {F['primary'][t]['sd_g']:.3f};"
                        f" step alone {r['step_only'][0]:+.3f} +- {r['step_only'][1]:.3f}; inside low-mass {r['slope_low_mass']['beta']:+.4f} +- {r['slope_low_mass']['sd_beta']:.4f}, inside the others {r['slope_high_mass']['beta']:+.4f} +- {r['slope_high_mass']['sd_beta']:.4f}")
for k in ("M0", "M1"): print(f"  these ages on Pantheon+ magnitudes {k}: A {R['pantheon_' + k]['A']:+.3f} +- {R['pantheon_' + k]['sd_A']:.3f} (n {R['pantheon_' + k]['n']})")
res["reported"] = R; json.dump(res, open(os.path.join(OUTDIR, f"agb5_results{TAG}.json"), "w"), indent=1, default=float); print(f"\nwrote agb5_results{TAG}.json")
