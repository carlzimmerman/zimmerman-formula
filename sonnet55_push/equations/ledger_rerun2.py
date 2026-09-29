#!/usr/bin/env python3
"""ledger_rerun2.py -- independent re-run of CFG48 (G1-G6), CFG58 and CFG59 from a clean `git archive HEAD` export.

Extracts the needed directories at the current HEAD into a scratch directory (layout preserved, so nothing in the working
tree is touched), runs each script in its main mode and with MUTATE=1, and records exit code + the script's own tally.
Expectations come from the lanes' own READMEs and the CFG48 referee note: G1-G5 main exit 0, G6 main exit 1 (four
pre-declared H failures, disclosed), every MUTATE exit 1; CFG58 main exit 1 (its README: control C1 failed and is kept), CFG59 main exit 0; both MUTATE exit 1.
"""
import json, os, re, subprocess, sys, tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
scratch = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="ledger_rerun2_")
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
paths = ["campaign_fresh_gravity", "real_research/dark_energy_2026", "real_research/g03_audit_2026",
         "real_research/cross_thread_review_2026_09_26", "real_research/derivation_chain_2026",
         "hunt_2026", "data_assembly", "real_research/data", "fable_independent_2026", ":(exclude)fable_independent_2026/lean_2026"]      # CFG58/59 import hunt_2026 code and read real_research/data tables
os.makedirs(scratch, exist_ok=True)
ar = subprocess.Popen(["git", "archive", "HEAD"] + paths, cwd=REPO, stdout=subprocess.PIPE)
subprocess.run(["tar", "-x", "-C", scratch], stdin=ar.stdout, check=True)
print("exported HEAD", head[:9], "to", scratch, flush=True)

C = os.path.join(scratch, "campaign_fresh_gravity")
G48 = os.path.join(C, "CFG48_gap1_switch")
JOBS = [(g, G48, g + ".py", exp_main) for g, exp_main in
        (("G1_gauss_noether", 0), ("G2_boundness_and_top_level", 0), ("G3_history_action_causality", 0),
         ("G4_exchange_action", 0), ("G5_edge_stress_mediator_wall", 0), ("G6_nonlocal_gate_stiffness", 1))]
JOBS += [("CFG58_rule_more_populations", C, "CFG58_rule_more_populations.py", 1)   # its README: main run exits 1, control C1 failed and is kept
        ,
         ("CFG59_universal_debris_fraction", C, "CFG59_universal_debris_fraction.py", 0)]
results = []
for slug, cwd, script, exp_main in JOBS:
    for label, env_add, expect in (("main", {}, exp_main), ("MUTATE=1", {"MUTATE": "1"}, 1)):
        e = dict(os.environ); e.pop("MUTATE", None); e.update(env_add)
        e["CFG58_OUT"] = os.path.join(scratch, "out58"); e["CFG59_OUT"] = os.path.join(scratch, "out59")
        os.makedirs(e["CFG58_OUT"], exist_ok=True); os.makedirs(e["CFG59_OUT"], exist_ok=True)
        try:
            p = subprocess.run([sys.executable, script], cwd=cwd, env=e, capture_output=True, text=True, timeout=1500)
            code, out = p.returncode, p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            code, out = -9, "TIMEOUT"
        tally = ""
        for ln in reversed(out.strip().splitlines()):
            if re.search(r"\b\d+\s*/\s*\d+\b|PASS|FAIL|checks|held|exit|rc *=", ln):
                tally = ln.strip()[:160]; break
        tb = "Traceback" in out
        results.append(dict(slug=slug, mode=label, exit=code, expect=expect, match=(code == expect), traceback=tb, tally=tally))
        print(f"{slug:<34}{label:<10} exit {code:>3} (expected {expect}) {'OK ' if code == expect else 'DIFFERS'}{' TRACEBACK' if tb else ''}  {tally}", flush=True)
json.dump(dict(head=head, results=results), open(os.path.join(scratch, "ledger_rerun2_results.json"), "w"), indent=1)
bad = [r for r in results if not r["match"] or r["traceback"]]
print(f"\n{len(results)} runs at HEAD {head[:9]}; {len(bad)} differ from the lanes' stated expectation or raised a traceback")
for r in bad:
    print("  DIFFERS:", r["slug"], r["mode"], "exit", r["exit"], "expected", r["expect"], "traceback" if r["traceback"] else "")
