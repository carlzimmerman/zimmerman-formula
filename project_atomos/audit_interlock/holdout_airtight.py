#!/usr/bin/env python3
"""AUDIT (lens gate_b, part b): is the HOLDOUT airtight NOW?

HOLDOUT_KEYS must be {koide_Q_lep, r_tau_mu} and no code path may reintroduce them by name
into a SEARCH pool. A leak lived exactly there once (two hard-coded lists re-added
koide_Q_lep after the dataset-level exclusion).

What this does, all by running / parsing the real code:
  (1) asserts HOLDOUT_KEYS content;
  (2) CALLS every real target-selection function in the repo and prints its membership;
  (3) AST-scans every .py file for the holdout key names and classifies each occurrence
      (search-pool construction vs guard vs comment vs scoring), so a name-based
      reintroduction cannot hide;
  (4) audits the two documented include_holdout=True call sites;
  (5) checks the COMMITTED ARTIFACTS: which recorded depth runs actually swept a holdout key.

Local-only project. Exit 0 unless a live SEARCH path leaks.
"""
from __future__ import annotations
import argparse
import ast
import json
import sqlite3
import sys
import time
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import targets.pdg_constants as pdg                                     # noqa: E402
from targets.pdg_constants import HOLDOUT_KEYS                          # noqa: E402
from exhaust_parallel import sm_target_keys                             # noqa: E402
import run_atomos                                                       # noqa: E402
import grind                                                            # noqa: E402
from engine.scoring import score_value, measurement_tol                 # noqa: E402
from exhaust import resolve_target                                      # noqa: E402

bar = "=" * 104
checks = []
fatal = []


def check(msg, cond, is_fatal=False):
    checks.append(bool(cond))
    if is_fatal and not cond:
        fatal.append(msg)
    print(f"   [{'PASS' if cond else 'FAIL'}] {msg}")


print(bar)
print("HOLDOUT AIRTIGHTNESS AUDIT -- real selection functions, real artifacts")
print(bar)

# ---------------------------------------------------------------------------------------------
print("\n(1) HOLDOUT_KEYS as loaded from targets/pdg_constants.py")
print("-" * 104)
print(f"   HOLDOUT_KEYS = {sorted(HOLDOUT_KEYS)}   (type {type(HOLDOUT_KEYS).__name__})")
check("HOLDOUT_KEYS == {koide_Q_lep, r_tau_mu}",
      set(HOLDOUT_KEYS) == {"koide_Q_lep", "r_tau_mu"}, is_fatal=True)
check("HOLDOUT_KEYS is immutable (frozenset)", isinstance(HOLDOUT_KEYS, frozenset))
ds = pdg.load()
for k in sorted(HOLDOUT_KEYS):
    t = ds.target(k)
    print(f"   {k:14} value={float(t.value):.10g} sigma={float(t.sigma):.3g} "
          f"rel={float(t.rel_precision):.2e} sector={t.sector} units={t.units!r}")
    check(f"{k} is in the dataset and flagged by ds.is_holdout()", ds.is_holdout(k))

# ---------------------------------------------------------------------------------------------
print("\n(2) EVERY real target-selection function, CALLED")
print("-" * 104)
selectors = {}

selectors["exhaust_parallel.sm_target_keys()"] = sm_target_keys()
selectors["exhaust_parallel.sm_target_keys(include_holdout=True)"] = \
    sm_target_keys(include_holdout=True)
selectors["run_atomos.select_targets(--all)"] = \
    [t.key for t in run_atomos.select_targets(argparse.Namespace(target=None), ds)]
selectors["pdg.dimensionless()"] = [t.key for t in ds.dimensionless()]
selectors["pdg.dimensionless(include_holdout=True)"] = \
    [t.key for t in ds.dimensionless(include_holdout=True)]
selectors["pdg.precise_targets(1e-2)"] = [t.key for t in ds.precise_targets(rel_thresh=1e-2)]
selectors["pdg.fittable(1e-2)"] = [t.key for t in ds.fittable(rel_thresh=1e-2)]
selectors["pdg.holdout()"] = [t.key for t in ds.holdout()]
selectors["grind._target_windows()"] = [w[0] for w in grind._target_windows()]

# the per-file sweep lists actually used by each search driver (same call, proven by calling it)
import exhaust_depth4_forced as D4                                      # noqa: E402
import exhaust_depth5_forced as D5m                                     # noqa: E402
import exhaust_depthN_forced as DNm                                     # noqa: E402
import overnight_vocab_search as OV                                     # noqa: E402
import overnight_pair_search as OP                                      # noqa: E402
for name, mod in (("exhaust_depth4_forced", D4), ("exhaust_depth5_forced", D5m),
                  ("exhaust_depthN_forced", DNm), ("overnight_vocab_search", OV),
                  ("overnight_pair_search", OP), ("grind", grind)):
    selectors[f"{name}.sm_target_keys (imported symbol)"] = mod.sm_target_keys()

SEARCH_SELECTORS = [k for k in selectors
                    if "include_holdout=True" not in k and "holdout()" not in k
                    and "_target_windows" not in k and "precise_targets" not in k]

print(f"   {'selector':<56}{'N':>5}  holdout members")
print("   " + "-" * 98)
for name, keys in selectors.items():
    leak = sorted(set(keys) & set(HOLDOUT_KEYS))
    print(f"   {name:<56}{len(keys):>5}  {leak if leak else 'NONE'}")

print()
for name in SEARCH_SELECTORS:
    leak = sorted(set(selectors[name]) & set(HOLDOUT_KEYS))
    check(f"SEARCH path {name} leaks nothing", not leak, is_fatal=True)

# the intentional include-holdout paths must still CONTAIN them (or the replay gate breaks
# and a survivor's out-of-sample prediction can never be scored)
print()
for name in ("exhaust_parallel.sm_target_keys(include_holdout=True)",
             "pdg.holdout()", "grind._target_windows()"):
    has = sorted(set(selectors[name]) & set(HOLDOUT_KEYS))
    check(f"intentional path {name} includes BOTH holdout keys (has {has})", len(has) == 2)

print("\n   *** include_holdout=True IS NOT THE FULL HISTORICAL LIST ANY MORE ***")
ih = selectors["exhaust_parallel.sm_target_keys(include_holdout=True)"]
print(f"   sm_target_keys()                    -> {len(selectors['exhaust_parallel.sm_target_keys()'])} keys")
print(f"   sm_target_keys(include_holdout=True) -> {len(ih)} keys; "
      f"holdout present = {sorted(set(ih) & set(HOLDOUT_KEYS))}")
print("   WHY: sm_target_keys builds `out` from precise_targets INTERSECT dimensionless(),")
print("   and dimensionless() now drops the holdout by default. The hard-coded re-add loop")
print("   names koide_Q_lep but NOT r_tau_mu, so r_tau_mu can never re-enter -- the")
print("   include_holdout=True flag cannot put back what the intersection already removed.")
print("   The docstring's claim ('returns the FULL historical list') is therefore false, and")
print("   the depth-8/9 artifacts below prove the historical list had 21 keys incl. r_tau_mu.")
check("r_tau_mu is UNREACHABLE even with include_holdout=True (a real regression in the "
      "2026-07-27 fix)", "r_tau_mu" not in ih, is_fatal=False)

# precise_targets: NOT holdout-filtered -- a latent hole for any future direct caller
pt_leak = sorted(set(selectors["pdg.precise_targets(1e-2)"]) & set(HOLDOUT_KEYS))
print(f"\n   NOTE  pdg.precise_targets(1e-2) is NOT holdout-filtered: contains {pt_leak}")
print("         (both current callers intersect it with dimensionless() then re-filter, so no")
print("          live leak -- but a new caller using it directly would search the holdout.)")

# scoring path must still work
s, r, p = ds.score_holdout("koide_Q_lep", 2 / 3)
print(f"   score_holdout('koide_Q_lep', 2/3) = {s:.2f} sigma, rel={r:.2e}, pass={p}")
s2, r2, p2 = ds.score_holdout("r_tau_mu", 16.8170)
print(f"   score_holdout('r_tau_mu', 16.8170) = {s2:.2f} sigma, rel={r2:.2e}, pass={p2}")
check("score_holdout works on both held-back targets (the only legitimate use)",
      p and p2)

# ---------------------------------------------------------------------------------------------
print("\n(3) AST SCAN: every .py file, every literal occurrence of a holdout key name")
print("-" * 104)
py_files = [p for p in _ROOT.rglob("*.py")
            if "QFTCert" not in str(p) and "__pycache__" not in str(p)]
print(f"   scanning {len(py_files)} .py files under {_ROOT}")

occurrences = []
for p in py_files:
    try:
        src = p.read_text()
        tree = ast.parse(src)
    except Exception as e:
        print(f"   (skip unparsable {p.name}: {e})")
        continue
    lines = src.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and node.value in HOLDOUT_KEYS:
            ln = getattr(node, "lineno", 0)
            occurrences.append((p.relative_to(_ROOT).as_posix(), ln,
                                node.value, lines[ln - 1].strip() if ln else ""))

print(f"   AST string-literal occurrences of a holdout key: {len(occurrences)}")
print(f"\n   {'file':<40}{'line':>6}  key            source")
print("   " + "-" * 98)
for f, ln, key, txt in sorted(occurrences):
    print(f"   {f:<40}{ln:>6}  {key:<14} {txt[:60]}")

# classify: which occurrences sit inside a list/tuple literal used to ADD targets?
print("\n   classification (a name-based re-add is a LIST/TUPLE of target keys "
      "feeding a search pool):")
GUARDED = {
    ("exhaust_parallel.py", 95): "hard-coded re-add loop -- but the function's LAST line "
                                 "re-filters with HOLDOUT_KEYS (verified by calling it above)",
    ("run_atomos.py", 1031): "hard-coded re-add loop -- select_targets() re-filters on its "
                             "LAST line (verified by calling it above)",
}
unguarded = []
seen_bucket = {}
for f, ln, key, txt in sorted(occurrences):
    tag = GUARDED.get((f, ln))
    if tag:
        bucket = f"GUARDED  {f}:{ln}  {tag}"
    elif f.startswith("audit_interlock/"):
        bucket = f"AUDIT    {f}  (this audit's own scripts -- not a search pool)"
    elif f.startswith("targets/pdg_constants.py") or f == "BITS_RULE.py" \
            or f == "GATE_POWER_ANALYSIS.py":
        bucket = f"BENIGN   {f}  definition / holdout-exclusion / power-analysis label"
    elif f == "grind.py":
        bucket = f"BENIGN   {f}  committed replay ground-truth constant (not a pool)"
    elif f == "exhaust.py":
        bucket = f"BENIGN   {f}  --target usage string in a docstring/error message"
    elif f == "run_atomos.py":
        bucket = f"BENIGN   {f}  koide mass-triple lookup / holdout scoring, not a pool"
    elif f == "calibration/charged_lepton_search.py":
        bucket = (f"** LEAK-CHANNEL ** {f}:{ln}  a SEARCH script with its OWN hard-coded "
                  f"TARGETS dict -- bypasses pdg_constants entirely, so HOLDOUT_KEYS "
                  f"cannot reach it")
        unguarded.append((f, ln, key, txt))
    else:
        bucket = f"** REVIEW ** {f}:{ln}  {key}  ->  {txt[:70]}"
        unguarded.append((f, ln, key, txt))
    if bucket not in seen_bucket:
        seen_bucket[bucket] = 0
        print("   " + bucket)
    seen_bucket[bucket] += 1

check("no name-based occurrence outside {definition, guarded re-add, scoring, replay "
      "ground truth, audit scripts} remains in the CAMPAIGN code",
      not [u for u in unguarded if not u[0].startswith("calibration/")], is_fatal=True)
if unguarded:
    print("\n   the flagged occurrences, examined individually:")
    for f, ln, key, txt in unguarded:
        print(f"      {f}:{ln}  {key}: {txt[:90]}")
    print("   calibration/charged_lepton_search.py is a pre-holdout (2026-06) calibration")
    print("   brute-force over its OWN hard-coded TARGETS dict containing r_tau_mu and")
    print("   koide_Q; it is not invoked by grind/run_atomos/VERIFY_ALL, but nothing in the")
    print("   repo stops it from being run as a search on a held-back target.")

# ---------------------------------------------------------------------------------------------
print("\n(4) the two intentional include_holdout=True call sites, audited")
print("-" * 104)
import inspect                                                          # noqa: E402
src_tw = inspect.getsource(grind._target_windows)
src_rp = inspect.getsource(grind.cmd_replay)
print("   grind._target_windows  (RETENTION):  include_holdout=True present ->",
      "include_holdout=True" in src_tw)
print("   grind.cmd_replay       (REPLAY):     include_holdout=True present ->",
      "include_holdout=True" in src_rp)
print("   grind.run_depth        (the SEARCH):  uses bare sm_target_keys() ->",
      "sm_target_keys()" in inspect.getsource(grind.run_depth))
print("   grind.cmd_deep_sample  (the SEARCH):  uses bare sm_target_keys() ->",
      "sm_target_keys()" in inspect.getsource(grind.cmd_deep_sample))
check("run_depth (the exhaustive search) calls the holdout-EXCLUDING selector",
      "include_holdout" not in inspect.getsource(grind.run_depth), is_fatal=True)
check("cmd_deep_sample (the sampled search) calls the holdout-EXCLUDING selector",
      "include_holdout" not in inspect.getsource(grind.cmd_deep_sample), is_fatal=True)
print("\n   NOTE  cmd_replay runs the FULL gate (validate) on holdout-target hits, because it")
print("         must reproduce committed depth-6/7 ground truth whose tightest hit IS")
print("         koide_Q_lep. It fits nothing and selects nothing, but its n_certified count")
print(f"         is taken over {len(selectors['exhaust_parallel.sm_target_keys(include_holdout=True)'])} "
      f"targets including the holdout -- so a CERTIFIED holdout hit would surface there.")
print(f"   REPLAY_COMMITTED tightest_target: "
      f"{ {d: grind.REPLAY_COMMITTED[d]['tightest_target'] for d in grind.REPLAY_COMMITTED} }")
print("   AND the replay's own label 'in-window hits (21 targets)' is now wrong: it sweeps")
print(f"   {len(selectors['exhaust_parallel.sm_target_keys(include_holdout=True)'])} "
      f"targets. It still reproduces the committed 259/1248 only because r_tau_mu")
print("   happens to contribute 0 hits at depths 6-7 (verified: `grind.py --replay 6` PASSes,")
print("   see audit_interlock/REPLAY6_AUDIT.txt).")

# ---------------------------------------------------------------------------------------------
print("\n(5) COMMITTED ARTIFACTS: which recorded runs actually swept a holdout key?")
print("-" * 104)
rg = _ROOT / "results_grind"
for d in (8, 9, 10):
    dd = rg / f"depth_{d}"
    if not dd.exists():
        continue
    vj = dd / "VERDICT.json"
    v = json.loads(vj.read_text()) if vj.exists() else {}
    pt = [t["target"] for t in (v.get("per_target") or [])]
    swept_holdout = sorted(set(pt) & set(HOLDOUT_KEYS))
    tfiles = sorted(p.stem for p in (dd / "targets").glob("*.json")) \
        if (dd / "targets").is_dir() else []
    file_holdout = sorted(set(tfiles) & set(HOLDOUT_KEYS))
    print(f"   depth {d}: VERDICT per_target={len(pt)} targets, holdout in VERDICT="
          f"{swept_holdout or 'NONE'}; target report files={len(tfiles)}, "
          f"holdout files={file_holdout or 'NONE'}  "
          f"(VERDICT mtime {time.strftime('%F', time.localtime(vj.stat().st_mtime)) if vj.exists() else '-'})")

d8 = json.loads((rg / "depth_8" / "VERDICT.json").read_text())
d9 = json.loads((rg / "depth_9" / "VERDICT.json").read_text())
d10 = json.loads((rg / "depth_10" / "VERDICT.json").read_text())
h8 = [t for t in d8["per_target"] if t["target"] in HOLDOUT_KEYS]
h9 = [t for t in d9["per_target"] if t["target"] in HOLDOUT_KEYS]
print(f"\n   depth 8 holdout sweeps recorded: "
      f"{[(t['target'], t['n_hits'], t['n_certified']) for t in h8]}")
print(f"   depth 9 holdout sweeps recorded: "
      f"{[(t['target'], t['n_hits'], t['n_certified']) for t in h9]}")
print(f"   depth 8 total n_hits {d8['n_hits']:,} over {len(d8['per_target'])} targets "
      f"(incl. holdout: {sum(t['n_hits'] for t in h8)} hits)")
print(f"   depth 9 total n_hits {d9['n_hits']:,} over {len(d9['per_target'])} targets "
      f"(incl. holdout: {sum(t['n_hits'] for t in h9)} hits)")
print(f"   depth 10 n_targets={d10.get('n_targets')} n_hits={d10['n_hits']:,} "
      f"(post-fix: holdout excluded)")
check("depth 10 (the headline exhaustive null) swept 19 targets, holdout excluded",
      d10.get("n_targets") == 19)
check("depths 8 and 9 DID sweep both holdout keys (pre-fix artifacts, still on disk "
      "and still the basis of the 'depths 3-9 clean null' claim)",
      len(h8) == 2 and len(h9) == 2)

# how much of the depth-10 record retention exists only for the holdout windows?
print("\n   depth-10 retention accounting (records.sqlite is retained with the holdout INCLUDED):")
vals = np.fromfile(rg / "depth_10" / "values.f64", dtype=np.float64)
con = sqlite3.connect(str(rg / "depth_10" / "records.sqlite"))
n_rec = con.execute("SELECT COUNT(*) FROM records").fetchone()[0]
hit_search, hit_hold = set(), {}
for k in sm_target_keys(include_holdout=True):
    ts = resolve_target(k)
    tol = measurement_tol(ts.pdg_target)
    tv = float(ts.value)
    idxs = np.nonzero(np.abs(vals - tv) <= abs(tv) * tol * (1.0 + 1e-9))[0]
    keep = {int(i) for i in idxs if score_value(float(vals[i]), ts.pdg_target).rel_error <= tol}
    if k in HOLDOUT_KEYS:
        hit_hold[k] = keep
    else:
        hit_search |= keep
hold_all = set().union(*hit_hold.values()) if hit_hold else set()
print(f"   retained records                          : {n_rec:,}")
print(f"   distinct values hitting a SEARCH target   : {len(hit_search):,}")
print(f"   distinct values hitting a HOLDOUT target  : "
      f"{ {k: len(v) for k, v in hit_hold.items()} } (union {len(hold_all)})")
print(f"   holdout-only retained values (never swept): {len(hold_all - hit_search):,}")
check("koide_Q_lep-window values exist in retention but were NEVER swept at depth 10 "
      "(retention != search -- the intended design)", len(hold_all) > 0)

# THE r_tau_mu CONSEQUENCE, measured: is anything retained near it at all?
print("\n   consequence of the r_tau_mu omission, measured on the depth-10 value set:")
for k in sorted(HOLDOUT_KEYS):
    ts = resolve_target(k)
    tol = measurement_tol(ts.pdg_target)
    tv = float(ts.value)
    idxs = np.nonzero(np.abs(vals - tv) <= abs(tv) * tol * (1.0 + 1e-9))[0]
    wb = [int(i) for i in idxs
          if score_value(float(vals[i]), ts.pdg_target).rel_error <= tol]
    got = sum(1 for i in wb
              if con.execute("SELECT 1 FROM records WHERE idx=?", (i,)).fetchone())
    print(f"   {k:14} tol={tol:.3e}  values inside its window = {len(wb):>3}  "
          f"of which RETAINED (formula recoverable) = {got:>3}")
    if k == "r_tau_mu":
        rt_wb, rt_got = len(wb), got
check(f"r_tau_mu: {rt_wb} depth-10 values land in its window and {rt_got} have a retained "
      f"record -> a survivor's out-of-sample prediction for the INFORMATIVE holdout "
      f"cannot be scored from the committed artifacts", rt_got == 0, is_fatal=False)
con.close()

print("\n" + bar)
n_fail = checks.count(False)
print(f"CHECKS: {len(checks) - n_fail}/{len(checks)} PASS")
if fatal:
    print("FATAL (a live search path leaks the holdout):")
    for m in fatal:
        print("   " + m)
print(bar)
sys.exit(1 if fatal else 0)
