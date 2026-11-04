#!/usr/bin/env python3
"""FN1b labels under the frozen rule (criteria e6e031a163). Merges fn1b_small.json, fn1b_mw_canonical.json and
fn1b_mw_alt.json (or the _MUTATE set) with KT14's stored source-only Milky Way rows at 0.5, 1.0 and 2.0 kpc.
Run: python3 -I -B fn1b_label.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
MUT = "--mutate" in sys.argv; sfx = "_MUTATE" if MUT else ""; OUT = []; RES = {}
def P(s=""): print(s, flush=True); OUT.append(s)
S = json.load(open(os.path.join(HERE, f"fn1b_small{sfx}.json"))); MW = {f: json.load(open(os.path.join(HERE, f"fn1b_mw_{f}{sfx}.json"))) for f in ("canonical", "alt")}
K14 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "KT14_filtered_phantom_mw", "kt14.json")))
LS = ["0.024", "0.1", "0.25", "0.5", "1.0", "2.0"]; FORMS = ("R", "SO"); FEET = ("canonical", "alt")
P(f"FN1b labels{'  [MUTATE]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")
failed = {"small": S["failed_checks"], **{f"mw_{f}": MW[f]["failed_checks"] for f in FEET}}
P(f"failed checks: {failed}")
ROWS = {}; LAB = {}
for form in FORMS:
    for foot in FEET:
        passes, ne_rows = [], []
        for L in LS:
            sm = S["summary"][f"{form}|{foot}|{L}"]; gates = dict(sm["gates"]); ne = list(sm["not_evaluable"]); flags = []
            if form == "SO":
                if L in MW[foot]["SO"]: n0 = MW[foot]["SO"][L]["n_pass"]; ev0 = MW[foot]["SO_evaluable"][L]; src = "KT14 code, this lane"
                else: n0 = K14[foot][L]["n_pass"]; ev0 = True; src = "kt14.json, carried"
            else:
                n0 = MW[foot]["R"][L]["n_pass"]; ev0 = MW[foot]["V1"][L]["evaluable"]; src = "KT33 engine, full lmax, this lane"
                if not MW[foot]["V1"][L]["c"]["ok"]: flags.append("ENGINE-DEPENDENT")
                if MW[foot]["convergence"][L]["grid_dependent"]: flags.append("GRID-DEPENDENT")
            gates = {"T0": n0 >= 1, **gates}
            if not ev0: ne.insert(0, "T0")
            fails = [t for t, ok in gates.items() if not ok and t not in ne]
            lab = "FAILS: " + ", ".join(fails) if fails else ("NOT EVALUABLE: " + ", ".join(ne) if ne else "ALL FIVE PASS")
            if lab == "ALL FIVE PASS": passes.append(L)
            if lab.startswith("NOT EVALUABLE"): ne_rows.append(L)
            ROWS[f"{form}|{foot}|{L}"] = dict(T0_cells=n0, T0_source=src, gates=gates, not_evaluable=ne, label=lab, flags=flags)
            P(f"  {form:2s} [{foot:9s}] L {float(L):5.3f} kpc: T0 {n0:4d} cells | " + " ".join(f"{t} {'NE' if t in ne else ('P' if v else 'F')}" for t, v in gates.items()) + f"  ->  {lab}" + (f"  [{', '.join(flags)}]" if flags else ""))
        lab = (f"A UNIVERSAL LENGTH PASSES (L = {', '.join(passes)} kpc)" if passes else (f"UNDECIDED (NOT EVALUABLE at L = {', '.join(ne_rows)} kpc)" if ne_rows else "NO UNIVERSAL LENGTH PASSES"))
        LAB[f"{form}|{foot}"] = lab; P(f"LABEL {form} [{foot}]: {lab}")
RES = dict(rows=ROWS, labels=LAB, failed_checks=failed, option_b_static_limit={f: LAB[f"R|{f}"] for f in FEET})
P(f"\nOption (b)'s static-limit label (form R): canonical {LAB['R|canonical']}; alt {LAB['R|alt']}")
P(f"Source-only rule (SO, beside): canonical {LAB['SO|canonical']}; alt {LAB['SO|alt']}")
open(os.path.join(HERE, f"fn1b_label{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"fn1b_label{sfx}.json"), "w"), indent=1)
