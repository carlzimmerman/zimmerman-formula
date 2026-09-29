#!/usr/bin/env python3
"""ledger_rerun.py -- independent re-run of rows 1-10 of campaign_fresh_gravity/closure_map/EQUATION_LEDGER_2026-09-28.md.

Copies the four lane directories to a scratch directory (so no committed output file in another lane is touched),
runs each script's main mode and its MUTATE control(s) with the environment variable the script documents, and records
the exit code plus the script's own final tally line. Expected: main exit 0 (or the declared exit 1), every MUTATE exit 1
(CFG50: MUTATE=a fails D1 only, MUTATE=b fails D2 only). Row 11 (ChainCert, Lean) is run separately in place.
Writes a machine-readable table to stdout; it changes nothing under campaign_fresh_gravity/.
"""
import os, re, shutil, subprocess, sys, tempfile, json

SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "campaign_fresh_gravity"))
scratch = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="ledger_rerun_")
dst = os.path.join(scratch, "campaign_fresh_gravity")
os.makedirs(dst, exist_ok=True)
for d in ("CFG43_fluid_tie", "CFG44_fluid_target", "CFG47_unruh_matching", "CFG50_tidal_closure"):
    shutil.copytree(os.path.join(SRC, d), os.path.join(dst, d), dirs_exist_ok=True)

# (row, dir, script, [(mode label, env, expect_exit)])
JOBS = [
    (1, "CFG43_fluid_tie", "A1_action_field_equations_dof.py", [("main", {}, 0), ("MUTATE=1", {"MUTATE": "1"}, 1), ("MUTATE=2", {"MUTATE": "2"}, 1)]),
    (2, "CFG43_fluid_tie", "A2_frw_flat_a0_and_dust_limit.py", [("main", {}, 0), ("MUTATE=1", {"MUTATE": "1"}, 1), ("MUTATE=2", {"MUTATE": "2"}, 1)]),
    (5, "CFG43_fluid_tie", "A3_cap_entry_form_and_obstruction.py", [("main", {}, 0), ("MUTATE=1", {"MUTATE": "1"}, 1), ("MUTATE=2", {"MUTATE": "2"}, 1)]),
    (7, "CFG44_fluid_target", "B1_target_and_hydrostatics.py", [("main", {}, 0), ("MUTATE=1", {"MUTATE": "1"}, 1)]),
    (8, "CFG44_fluid_target", "B2_barotropic_nogo.py", [("main", {}, 0), ("MUTATE=1", {"MUTATE": "1"}, 1)]),
    (8, "CFG44_fluid_target", "B3_local_closures.py", [("main", {}, 0), ("MUTATE=1", {"MUTATE": "1"}, 1)]),
    (8, "CFG44_fluid_target", "B4_actions_reciprocity.py", [("main", {}, 0), ("MUTATE=1", {"MUTATE": "1"}, 1)]),
    (9, "CFG50_tidal_closure", "D1_action_reciprocity.py", [("main", {}, 0), ("MUTATE=a", {"MUTATE": "a"}, 1), ("MUTATE=b", {"MUTATE": "b"}, 0)]),
    (9, "CFG50_tidal_closure", "D2_wellposed_nogo.py", [("main", {}, 0), ("MUTATE=a", {"MUTATE": "a"}, 0), ("MUTATE=b", {"MUTATE": "b"}, 1)]),
    (10, "CFG47_unruh_matching", "CFG47_unruh_matching.py", [("main", {}, 0), ("MUTATE=1", {"MUTATE": "1"}, 1), ("MUTATE=2", {"MUTATE": "2"}, 1)]),
]
results = []
for row, d, script, modes in JOBS:
    for label, env, expect in modes:
        e = dict(os.environ); e.pop("MUTATE", None); e.update(env)
        try:
            p = subprocess.run([sys.executable, script], cwd=os.path.join(dst, d), env=e, capture_output=True, text=True, timeout=900)
            code, out = p.returncode, (p.stdout + p.stderr)
        except subprocess.TimeoutExpired:
            code, out = -9, "TIMEOUT"
        tally = ""
        for ln in reversed(out.strip().splitlines()):
            if re.search(r"\b\d+\s*/\s*\d+\b|PASS|FAIL|checks|held", ln):
                tally = ln.strip()[:150]; break
        results.append(dict(row=row, script=script, mode=label, exit=code, expect=expect, match=(code == expect), tally=tally))
        print(f"row {row:>2}  {script:<40}{label:<10} exit {code:>3} (expected {expect})  {'OK ' if code == expect else 'MISMATCH'}  {tally}", flush=True)
json.dump(results, open(os.path.join(scratch, "ledger_rerun_results.json"), "w"), indent=1)
bad = [r for r in results if not r["match"]]
print(f"\n{len(results)} runs; {len(bad)} exit codes differ from the ledger's stated expectation")
for r in bad:
    print("  DIFFERS:", r["row"], r["script"], r["mode"], "exit", r["exit"], "expected", r["expect"])
print("scratch dir:", scratch)
