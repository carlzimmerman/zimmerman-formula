#!/usr/bin/env python3
"""V03b -- TRIO DECISION-TREE FIX-FORWARD (V03 died at V03_trio.py:623,
KeyError 'central'; crash preserved verbatim in V03_trio.out, committed 699ca4388).
This driver: (1) reads V03_trio.py, applies the three registered patches to a NEW
file V03b_trio_fix_run.py (V03_trio.py untouched -- house rule 7), (2) runs it,
(3) reports. Patches (pre-registered in Y-WAVE_BRIEF.md before any run):
  P1 the KILL-B and UNDET-B branches append their tree rows (they are verdicts
     too; the locked md-0.6 tree emits a verdict at node 1, the old code only
     recorded rows reaching node 2/3) and continue;
  P2 the confusion counter is robust (setdefault) -- the recorded KeyError
     'central' cannot recur regardless of its precise trigger;
  P3 output renamed V03b_trio_results.json + a partial tree dump after the
     decision tree so a later crash cannot lose it.
Falsifiers: V03_PRE.txt verbatim. No fabrication: whatever the rerun prints is
the record. No git commit (lane rule).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "V03_trio.py")
DST = os.path.join(HERE, "V03b_trio_fix_run.py")

src = open(SRC).read()

def patch1(text, anchor, insertion):
    n = text.count(anchor)
    assert n == 1, "anchor count %d for %r" % (n, anchor[:60])
    return text.replace(anchor, anchor + insertion)

src = patch1(src, '            tree = "KILL-B"; fail = []',
             '\n            tree_rows.append((tag, qh, tree, fail, atlas)); continue')
src = patch1(src, '            tree = "UNDET-B"; fail = ["B_gate_n_too_small"]',
             '\n            tree_rows.append((tag, qh, tree, fail, atlas)); continue')
src = patch1(src, '        conf[key][tree] = conf[key].get(tree, 0) + 1',
             '\n        if key not in conf:\n            conf[key] = {}')
src = src.replace('WROTE V03_results.json', 'WROTE V03b_trio_results.json')
# rename outputs + add partial dump before the min-n section
src = src.replace('V03_results.json', 'V03b_trio_results.json')
anchor_p3 = '    # ---------------- minimum n per falsifier per cell --------------------'
assert src.count(anchor_p3) == 1
partial = ('    json.dump(dict(decision_tree=dict(confusion=conf, rows=tree_payload)),\n'
           '               open(os.path.join(HERE, "V03b_tree_partial.json"), "w"),\n'
           '               indent=1, default=str)\n')
src = src.replace(anchor_p3, partial + anchor_p3)

open(DST, "w").write(src)
print("V03b: patched copy written ->", DST)

out_path = os.path.join(HERE, "V03b_trio_fix.out")
with open(out_path, "w") as fo:
    rc = subprocess.call([sys.executable, "-u", DST], stdout=fo,
                         stderr=subprocess.STDOUT, cwd=HERE)
print("V03b: rerun rc =", rc)

tail = open(out_path).read()[-3000:]
report = dict(lane="V03b_trio_fix", run_rc=rc,
              doorB_consistent_open=("doorB verdict: CONSISTENT-OPEN" in tail),
              wrote_results=os.path.exists(os.path.join(HERE, "V03b_trio_results.json")),
              tail=tail[-1200:])
json.dump(report, open(os.path.join(HERE, "V03b_results.json"), "w"), indent=1)
print("V03b: report written; doorB reproduced:", report["doorB_consistent_open"])
sys.exit(0 if (rc == 0 and report["wrote_results"]) else 1)
