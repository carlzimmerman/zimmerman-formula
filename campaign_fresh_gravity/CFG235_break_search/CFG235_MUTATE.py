"""CFG235_MUTATE.py -- MUTATE controls M1-M8 (frozen section 13).  Run as  MUTATE=k python3 CFG235_MUTATE.py  (k = 1..8).
Re-runs the planted-galaxy controls on the SAME planted rows (parameters read from the main controls result) with one
load-bearing cell flipped.  Exit 1 iff the control BITES (a control that passed in the main run now fails); exit 0 means the
mutation did not bite and is itself a control failure, recorded.  Controls that already failed in the main run are not counted."""
import os, sys, json
sys.dont_write_bytecode = True
import CFG235_common as C
import CFG235_01_controls as K

MUT_DESC = {1: "swap the floors: L1 reads nu, F1 reads 1", 2: "drop the M* and dynamical systematics (sigma_sys = 0)",
            3: "drop the trials correction (T0 final: 'confirmed' = T0)", 4: "add measured gas x3 to the PRIMARY floor (drop the one-sided floor)",
            5: "take R_obs from the model output D = 1/(1 - f_DM) instead of V_c", 6: "drop the min-over-cells rule (primary cell only)",
            7: "use the actual footprint (0.049 deg^2) for V_surv", 8: "set m = 31"}
WANT = {1: ["P2.L1_not_T0", "P2.label_T0_framework_only"], 2: ["P5.no_T0"], 3: ["P6.not_confirmed_(T2)"], 4: ["P7.L1_T0_not_fired(tier S)"],
        5: ["P10.no_flag(f_DM-inconsistent row; V_c route)"], 6: ["P11.fragile_no_T0(z_primary>3, z_rob<3)", "P5.no_T0"],
        7: ["P3b.L2_z_primary<=2.0(V_ref)"], 8: ["P6.F1_T1_NOT_fired"]}
k = C.MUT
assert 1 <= k <= 8, "set MUTATE=1..8"
main = json.load(open(os.path.join(C.HERE, "CFG235_01_controls_results.json")))
base_failed = set(main["failed"])
print(f"CFG235_MUTATE M{k}: {MUT_DESC[k]} | repo = <repo> | z_B = {C.Z_B:.3f} m = {C.M_TRIALS}", flush=True)
out = K.run_controls(pp=main["planted"])
new_fail = [n for n, v in out["exp"].items() if (not v["ok"]) and n not in base_failed]
for n in WANT[k]:
    v = out["exp"].get(n)
    print(f"  expected to bite: {n}: {'BITES' if (v and not v['ok']) else 'did NOT bite'}  ({v['detail'] if v else ''})")
print("  all newly failing controls (not failing in the main run):", new_fail if new_fail else "none")
want_bit = [n for n in WANT[k] if out["exp"].get(n) and not out["exp"][n]["ok"]]
missed = [n for n in WANT[k] if n not in want_bit]
json.dump(dict(mutate=k, desc=MUT_DESC[k], new_fail=new_fail, bites=want_bit, expected_but_not_bitten=missed),
          open(os.path.join(C.HERE, f"CFG235_MUTATE_{k}_results.json"), "w"), indent=1)
bit = bool(new_fail)
print(f"  MUTATE M{k}: control {'BITES' if bit else 'DOES NOT BITE'}; exit {1 if bit else 0}")
sys.exit(1 if bit else 0)
