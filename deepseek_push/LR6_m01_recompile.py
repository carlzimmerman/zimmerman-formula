#!/usr/bin/env python3
"""LR6 -- M01 recompile + stale-register disposition audit (Z8-wave; owns LR6_*).
Door: register rows 12/17/18/19 carry Lean status "open (M01)"; the Z6/Z7 ops
notes listed LR-class certs for them as candidate doors. Conductor audit this
tick (Z8-WAVE_BRIEF.md door-audit 3): rows 17/19 are ALREADY certified inside
M01_alg_spine.lean (sections 4/5); row 12 is model-input (K01 A-class); row 18
has no closed form (its thin-window numerator is the LR4c/MC5 leg). This lane
verifies M01 still compiles clean TODAY and writes the disposition.
Gates (Z8-WAVE_BRIEF.md): fresh lake rc 0, zero sorry, all printed axiom sets
subset {propext, Classical.choice, Quot.sound}; j10i_window_decomp and the k04_*
family present in the file. Kill: recompile fails -> exit 1 (honest audit finding).
"""
import json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.join(HERE, "..", "fable_independent_2026", "lean_2026")
OUT = os.path.join(HERE, "LR6_m01_recompile.out")
RESF = os.path.join(HERE, "LR6_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time()-_T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="LR6 M01 recompile + stale-register disposition",
               pre_registration="Z8-WAVE_BRIEF.md LR6 gates",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF,"w"), indent=1, default=str)
    with open(OUT,"a") as f: f.write("\n".join(LOG)+"\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

src = open(os.path.join(LEAN, "M01_alg_spine.lean")).read()
must = ["j10i_window_decomp", "k04_tau0Hat_eq", "k04_qHat_eq", "k04_recover_s",
        "k04_recover_d", "k04_roundtrip_tau", "k04_window_forward",
        "k04_window_backward", "k04_qhat_gt_neg_one", "k04_refutes_ed_three_halves"]
missing = [t for t in must if t not in src]
log("G0: k04/j10i theorem presence in M01_alg_spine.lean: %s" %
    ("ALL PRESENT" if not missing else "MISSING %s" % missing))
if missing: finish(1, "G0-FAIL: expected M01 theorems missing: %s" % missing)

p = subprocess.run(["lake", "env", "lean", "M01_alg_spine.lean"], cwd=LEAN,
                   capture_output=True, text=True, timeout=600)
stdout = p.stdout + p.stderr
with open(os.path.join(HERE, "LR6_lean_stdout.txt"), "w") as f: f.write(stdout)
log("G1: lake rc=%d (%d chars)" % (p.returncode, len(stdout)))
if p.returncode != 0:
    finish(1, "G1-FAIL: M01 recompile rc %d -- blocker verbatim:\n%s" % (p.returncode, stdout[-2000:]))
if re.search(r"\bsorry\b", stdout):
    finish(1, "G1-FAIL: sorry in M01")
axs = re.findall(r"'([A-Za-z0-9_]+)' depends on axioms: \[(.*)\]", stdout)
log("G1: %d axiom prints" % len(axs))
dirty = [(n, a) for n, a in axs
         if not set(x.strip() for x in a.split(",")) <= {"propext", "Classical.choice", "Quot.sound"}]
if dirty: finish(1, "G1-FAIL: dirty axioms: %s" % dirty)
log("G1 PASS (rc 0, zero sorry, %d theorems axiom-clean)" % len(axs))

disposition = {
  "row17_J10_window": "Lean leg CERTIFIED via M01_alg_spine.lean section 4 "
      "(j10i_window_decomp: window in [(4/3)(r_B/R), 2(r_B/R)]), recompile-verified this tick",
  "row19_K04_inversion": "Lean leg CERTIFIED via M01_alg_spine.lean section 5 "
      "(full bijection incl. corrected boundary k04_qhat_gt_neg_one and the honest "
      "refutation k04_refutes_ed_three_halves), recompile-verified this tick",
  "row12_atom_law": "model-input / consistency-family (K01 A-class): A = exp(-tau0(1+q/3)) "
      "restates the engine's own sampling rule; a Lean certificate would be a definition "
      "restatement -- recorded NOT lane-worthy; empirical legs J09/K03 stand",
  "row18_J11_volume_window": "stays MEASURED (quadrature+MC, no closed form at finite tau0); "
      "its tau0->0 numerator (chord 3/4 + q*5/12) is certified by LR4c this wave and "
      "engine-tested by MC5 this wave",
}
finish(0, "AUDIT LANDED: M01 recompiles clean today (%d theorems, axiom-clean); "
          "register rows 17/19 Lean legs CERTIFIED-via-M01 (disposition recorded); "
          "row 12 dispositioned LABEL-ONLY (not lane-worthy); row 18 stays MEASURED "
          "with its thin-window leg closed by LR4c/MC5" % len(axs),
       dict(theorems_clean=len(axs), disposition=disposition))
