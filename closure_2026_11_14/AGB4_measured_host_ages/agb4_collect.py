"""AGB4 collector: applies the known-answer checks and the frozen words of FROZEN_CRITERIA.md to the outputs of
agb4_run.py. Writes agb4_results.json; prints the tables (redirect to agb4_collect.out). It fits nothing."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUTDIR = sys.argv[1] if len(sys.argv) > 1 else HERE
load = lambda n: json.load(open(os.path.join(OUTDIR, f"agb4_{n}.json")))


def word6(d0, d1):
    if d1 >= 9 and d0 < 4: return "AGE BIAS EXCLUDED AT 3 SIGMA"
    if 4 <= d1 < 9 and d0 < 4: return "AGE BIAS DISFAVOURED"
    if d0 >= 9 and d1 < 4: return "AGE BIAS REQUIRED AT 3 SIGMA"
    if 4 <= d0 < 9 and d1 < 4: return "AGE BIAS FAVOURED"
    if d0 < 4 and d1 < 4: return "UNDECIDED"
    return "NEITHER"


def uword(a, d1):
    if d1 < 4: return "HOSTS AS LARGE AS THE SLOPE NEEDS"
    if a < 1: return "SLOPE OVERPREDICTS THE HOSTS AT 3 SIGMA" if d1 >= 9 else "SLOPE OVERPREDICTS THE HOSTS (2 SIGMA)"
    return "HOSTS LARGER THAN THE SLOPE NEEDS"


def second(first, others):
    bad = [k for k, w in others.items() if w != first]
    return "ROBUST" if not bad else "FRAGILE (" + "; ".join(f"{k}: {others[k]}" for k in bad) + ")"


K1, K2, K3, K4, KR, M = (load(k) for k in ("K1", "K2", "K3", "K4", "KR", "M")); pf = lambda b: "PASS" if b else "FAIL"; res = dict(lane="AGB4")
print("AGB4 known-answer checks")
print(f"  K1 match: {K1['n_matched']} matched, {K1['n_pp']} with an age; max dz {K1['max_dz']:.4f}; mass correlation {K1['corr_mass']:.3f} -> {pf(K1['passed'])}")
print(f"  K2 ages against stretch: low-stretch share {K2['share_old']:.3f} at 6 Gyr and above, {K2['share_young']:.3f} below (difference {K2['diff']:.3f}, needs 0.15) -> {pf(K2['passed'])}")
print(f"  K3 twins: {sum(t['passed'] for t in K3['twins'])} of {len(K3['twins'])} -> {pf(K3['passed'])}")
for k in ("M0", "M1"): print(f"  K4 {k}: mean {K4[k]['mean_over_sigma']:+.3f} sigma; shuffle scatter / sigma {K4[k]['sd_over_sigma']:.3f}; sandwich / sigma {K4[k]['sandwich_over_sigma']:.3f} -> {pf(K4[k]['passed'])}")
print(f"  KR Rose et al.'s age step: {KR['step_weighted']:+.4f} mag (published 0.114 +- 0.039, tolerance 0.04) -> {pf(KR['passed'])}  (does not void the lane)")
base = K1["passed"] and K2["passed"] and K3["passed"]; res["checks"] = dict(K1=K1["passed"], K2=K2["passed"], K3=K3["passed"], K4={k: K4[k]["passed"] for k in ("M0", "M1")}, KR=KR["passed"])
row = lambda lab, r, w="": print(f"  {lab:12s} A {r['A']:+.3f} +- {r['sd_A']:.3f} (sandwich {r['sandwich_sd_A']:.3f})  dchi2(A=0) {r['D_A0']:6.2f}  dchi2(A=1) {r['D_A1']:6.2f}"
                                 + (f"  g {r['g']:+.4f} +- {r['sd_g']:.4f}" if "g" in r else "") + f"  n {r['n']}   {w}")
for k, title, wf in (("M0", "no mass step", lambda r: uword(r["A"], r["D_A1"])), ("M1", "mass step free", lambda r: word6(r["D_A0"], r["D_A1"]))):
    F = M["fits"][k]; first = wf(F["primary"]); oth = {n: wf(F[n]) for n in ("reading_P", "bins12", "big", "narrow")}
    print(f"\n{k}, {title} ({'evaluable' if base and K4[k]['passed'] else 'NOT EVALUABLE'}):")
    row("primary", F["primary"], first)
    for n in oth: row(n, F[n], oth[n])
    res[k] = dict(fit=F["primary"], first=first, forks=oth, word=f"{first} / {second(first, oth)}" if base and K4[k]["passed"] else "NOT EVALUABLE")
    print(f"  -> {k}: {res[k]['word']}")
print("\nReported only")
R = M["reported"]
for n in ("rose_global", "rose_local", "pegase", "big_spec"):
    for k in ("M0", "M1"):
        if f"{n}_{k}" in R: row(f"{n} {k}", R[f"{n}_{k}"], "" if KR["passed"] or not n.startswith("rose") else "(Rose rows NOT EVALUABLE: KR failed)")
for lab in ("pp", "big"):
    for k in ("M0", "M1"):
        r = R[f"split6_{lab}_{k}"]; print(f"  split at 6 Gyr, {lab} {k}: below {r['A_below']:+.3f} +- {r['sd_below']:.3f}; above {r['A_above']:+.3f} +- {r['sd_above']:.3f} ({r['n_above']} hosts above)")
q = R["reliability"]; print(f"  reliability of the FSPS age: {q['unconditional'][0]:.3f} +- {q['unconditional'][1]:.3f}; inside M0 {q['inside_M0'][0]:.3f} +- {q['inside_M0'][1]:.3f}; inside M1 {q['inside_M1'][0]:.3f} +- {q['inside_M1'][1]:.3f};"
                            f" amplitudes divided by it: M0 {q['M0_corrected']:+.3f}, M1 {q['M1_corrected']:+.3f}")
res["reported"] = R
json.dump(res, open(os.path.join(OUTDIR, "agb4_results.json"), "w"), indent=1, default=float); print("\nwrote agb4_results.json")
