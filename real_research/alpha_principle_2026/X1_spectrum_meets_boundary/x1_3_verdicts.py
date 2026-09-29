#!/usr/bin/env python3
"""x1_3_verdicts -- reads x1_1_results.json (Track Z) and x1_2_results.json (Track K) and prints the per-pair verdict table (pre-registered in X1_PREREGISTRATION.md).
Per (spectrum, rule) pair: the zero-knob prediction and its miss (Track Z), whether ANY knob choice works and at what parameter cost (Track K), and the verdict in the original scheme
(DEAD / RE-FIT / LEAD) and under amendment A0 (zero knobs; any knob-dependent success is a forbidden RE-FIT).
Run (real):    PYTHONDONTWRITEBYTECODE=1 python3 x1_3_verdicts.py           -> writes x1_3_verdicts.json; exit 0 iff the consistency checks pass (2 otherwise)
Run (control): PYTHONDONTWRITEBYTECODE=1 python3 x1_3_verdicts.py MUTATE    -> one Track-Z record is corrupted (a Z-FAIL turned into Z-PASS) before the tally check: the check must FAIL; exit 1 if the control bites, 3 if it does not.
Needs x1_1_results.json and x1_2_results.json (run x1_1 and x1_2 first).
"""
import sys
sys.dont_write_bytecode = True
import json
import copy
import x1_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
chk = L.Checks(MUT)
Z = json.load(open("x1_1_results.json"))
K = json.load(open("x1_2_results.json"))
zv = copy.deepcopy(Z["variants"])
kv = K["variants"]
if MUT:
    for r in zv:
        if r["verdict"].startswith("Z-FAIL"):
            r["verdict"] = "Z-PASS"
            break
print("=" * 118)
print("X1-3 verdicts -- mode:", "MUTATE (control)" if MUT else "REAL RUN")
print("=" * 118)
chk("C1 Track Z: 52 records, and the stored tally equals a recount of the verdicts", len(zv) == 52 and (sum(r["verdict"].startswith("Z-PASS") for r in zv), sum(r["verdict"].startswith("Z-FAIL") for r in zv), sum(r["verdict"].startswith("Z-DEAD") for r in zv)) == (Z["tally"]["pass_"], Z["tally"]["fail"], Z["tally"]["dead"]))
chk("C2 Track K: 29 records; every record has K_eq, u, m and excess = K_eq - u - m", len(kv) == 29 and all(r["excess"] == r["K_eq"] - r["u"] - r["m"] for r in kv))
chk("C3 grand total 81 = the family size used for lane D's bar", len(zv) + len(kv) == L.N_TRIALS_TOTAL)

# ---------------------------------------------------------------- Track Z summary by (spectrum, rule kind)
print("\nTRACK Z (zero knobs): smallest miss factor |r|/tol over the scale/prescription variants of each (spectrum, rule); a factor > 1 is a miss larger than the running's stated uncertainty")
groups = {}
for r in zv:
    key = (r["spectrum"] + (":" + r["prescription"] if r["prescription"] != "none" else ""), r["kind"])
    groups.setdefault(key, []).append(r)
rowsZ = []
for key, lst in groups.items():
    margins = [r["margin_max"] for r in lst if r["margin_max"] is not None]
    n_pass = sum(r["verdict"].startswith("Z-PASS") for r in lst)
    n_dead = sum(r["verdict"].startswith("Z-DEAD") for r in lst)
    best = min(margins) if margins else None
    rowsZ.append(dict(spectrum=key[0], rule=key[1], n=len(lst), n_pass=n_pass, n_dead=n_dead, best_factor=best))
    print(f"  {key[0]:12s} {key[1]:3s}  variants {len(lst):2d}  Z-PASS {n_pass}  Z-DEAD {n_dead}  smallest miss factor {best if best is None else round(best, 1)}")
print("\n  absolute rules (they alone predict alpha(0)): implied 1/alpha(0) versus 137.036 (CODATA), the running's uncertainty tol_em, and lane D's bar")
for r in zv:
    if "alpha0" in r:
        a = r["alpha0"]
        print(f"    {r['id']} {r['spectrum']}:{r['prescription']} {r['rule']:16s} implied {a['implied_inv']:8.2f} miss {a['delta']:.3f} tol_em {a['tol_em']:.3f} within tol: {a['within_tol']}  bar clears: {a['clears_bar']}  (translation valid: {a['valid_translation']})")
n_bar = sum(1 for r in zv if "alpha0" in r and r["alpha0"]["clears_bar"])
n_in = sum(1 for r in zv if "alpha0" in r and r["alpha0"]["within_tol"])
print(f"  absolute rules with an implied alpha(0): {sum(1 for r in zv if 'alpha0' in r)}; within the running's uncertainty: {n_in}; clearing lane D's bar: {n_bar}")

# ---------------------------------------------------------------- Track K summary
print("\nTRACK K (knobs allowed): per variant class, over N27 = 1, 3 and the S4 variants")
byvar = {}
for r in kv:
    byvar.setdefault(r["variant"].split("-")[0] + ("-" + r["variant"].split("-")[1] if r["variant"].startswith("S4") else ""), []).append(r)
rowsK = []
for v, lst in byvar.items():
    cl = [("REFIT" if x["verdict"].startswith("K-REFIT") else "LEAD" if "LEAD" in x["verdict"] else "DEAD" if x["verdict"].startswith("K-DEAD") else "OPEN") for x in lst]
    ex = sorted({x["excess"] for x in lst})
    rowsK.append(dict(variant=v, n=len(lst), classes=cl, excess=ex))
    print(f"  {v:8s} n={len(lst)} classes={cl} nominal excess={ex}")
lead = [r["id"] for r in kv if "LEAD" in r["verdict"]]
refit = [r["id"] for r in kv if r["verdict"].startswith("K-REFIT")]
opn = [r["id"] for r in kv if r["verdict"].startswith("K-OPEN")]
print(f"  K-LEAD: {lead}   K-REFIT: {refit}   K-OPEN: {opn}")
chk("C4 no Track-K record is left OPEN (every target either solved or shown unreachable)", not opn)

# ---------------------------------------------------------------- pair verdicts
print("\nPAIR VERDICTS (original scheme / amendment A0)")
pairs = []


def zclass(spec, rules):
    lst = [r for r in zv if r["spectrum"] == spec and r["kind"] in rules]
    return lst


def add(pair, orig, a0, note):
    pairs.append(dict(pair=pair, original=orig, A0=a0, note=note))
    print(f"  {pair:44s} original: {orig:9s} A0: {a0:24s} {note}")


for spec, label, rules, dnote in (("S1", "SM+nu_R", ("RC", "RD", "RF", "RG"), "no knobs exist (nu_R neutral)"), ("S2", "Spin(10) 16", ("RA", "RB", "RD", "RE"), "no knobs exist (complete multiplets, desert)")):
    for kind in rules:
        lst = zclass(spec, (kind,))
        anypass = any(r["verdict"].startswith("Z-PASS") for r in lst)
        add(f"{label} x {kind}", "LEAD?" if anypass else "DEAD", "Z-PASS?" if anypass else "Z-FAIL/DEAD", dnote)
kz_by_kind = {}
for kind in ("RA", "RB", "RD", "RE", "RF", "RG"):
    lst = [r for r in zv if r["spectrum"] == "S3" and r["kind"] == kind]
    kz_by_kind[kind] = lst
kmap = {"RA": ("KA",), "RB": ("KA",), "RD": ("KD",), "RE": ("KE",), "RF": ("KF",), "RG": ("KG",)}
for kind, lst in kz_by_kind.items():
    kk = [x for x in kv if x["spectrum"] == "S3" and x["variant"].split("-")[0] in kmap[kind]]
    refit_k = [x for x in kk if x["verdict"].startswith("K-REFIT")]
    lead_k = [x for x in kk if "LEAD" in x["verdict"]]
    anypass = any(r["verdict"].startswith("Z-PASS") for r in lst)
    if lead_k:
        orig = "LEAD"
    elif refit_k:
        orig = "RE-FIT"
    else:
        orig = "DEAD"
    a0 = "Z-PASS?" if anypass else ("RE-FIT-forbidden" if refit_k else "Z-FAIL/DEAD")
    note = f"K: {len(refit_k)} of {len(kk)} knob variants feasible" + (" (" + "; ".join(f"{x['id']}: {x['verdict'][:60]}" for x in refit_k) + ")" if refit_k else "")
    add(f"E6 27 x {kind}", orig, a0, note)
kk = [x for x in kv if x["spectrum"] == "S4"]
add("SM + gauged B-L (Spin(10) chain) x R-A/R-B", "DEAD" if all(x["verdict"].startswith("K-DEAD") for x in kk) else "RE-FIT", "Z-FAIL/DEAD", "M_BL cannot move a_Y")
n_lead = sum(1 for p in pairs if p["original"].startswith("LEAD"))
n_refit = sum(1 for p in pairs if p["original"] == "RE-FIT")
n_dead = sum(1 for p in pairs if p["original"] == "DEAD")
print(f"\nPair tally (original scheme): {n_lead} LEAD, {n_refit} RE-FIT, {n_dead} DEAD of {len(pairs)} (spectrum, rule) pairs.  Under A0: no pair has a zero-knob pass; knob-dependent successes are forbidden RE-FITs.")
chk("C5 no zero-knob pair passes T-JOINT (A0 headline) and no pair is a LEAD", Z["tally"]["pass_"] == 0 and n_lead == 0)
with open("x1_3_verdicts_MUTATE.json" if MUT else "x1_3_verdicts.json", "w") as f:
    json.dump(dict(pairs=pairs, trackZ=rowsZ, trackK=rowsK, n_lead=n_lead, n_refit=n_refit, n_dead=n_dead, mutate=MUT), f, indent=1)
chk.finish("X1-3")
