#!/usr/bin/env python3
"""
grind.py — the RESUMABLE DEPTH-ESCALATION GRINDER for the constructive Gate-B-passable
dimensionless forced-interlock search (depths >= 8), under the OWNER-AUTHORIZED 40 GB memory cap.

RULE 3 (project law, held): gate/, engine/, exhaust.py, exhaust_parallel.py,
exhaust_depth4_forced.py, exhaust_depth5_forced.py, exhaust_depthN_forced.py have ZERO git diff.
This file IMPORTS them VERBATIM and adds only new functionality:

  * a STREAMED build (`streamed_build`) that enumerates EXACTLY the same constructive candidates
    as exhaust_depthN_forced.constructive_gate_b_reachables — same budget splits
    (DN.budget_splits), same skeleton layer (DN._skeleton_value_nodes), same canonical germ
    recipes (DN._germ_recipes), same evaluate/filter/value-dedup order — but keeps in RAM only
    the distinct-value-key set + a float64 array of the distinct values, and spills formula
    records to sqlite ONLY for values inside a (slightly widened) window of one of the 21
    targets. In-window hits are later reported with their formulas by re-lookup + exact ExprNode
    REBUILD (skeleton index + canonical germ recipe), so every hit still goes through the REAL
    committed gates (exhaust.gate_candidate_for -> gate.validate), never a reimplementation.
    The committed depth-8 wall (5.77 GB) was the materialized `reach` list of Reachable objects;
    a value-only build stays far below that (the honest caveat in
    notes/DEPTH6PLUS_ESCALATION_VERDICT.md). The streamed path is validated by the REPLAY GATE:
    `--replay 6` / `--replay 7` must reproduce the committed depth-6/7 numbers EXACTLY
    (distinct 107,719 / 498,848; in-window hits 259 / 1,248; tightest koide_Q_lep 9.23e-06)
    and exit nonzero on ANY mismatch.

  * MEMORY CAP (owner-authorized, 2026-07-21): GRIND_MEM_CAP_GB = 40.0 on a 64 GB machine
    (>= 24 GB headroom, never touch swap). RULE 3 forbids editing the imported files, so the
    imported depth-5 watchdog's module attributes (HARD_MEM_CAP_GB / _MEM_CAP_MB) are overridden
    AT RUNTIME below — an in-process attribute set, zero file diff. Every ledger / verdict entry
    records mem_cap_gb actually in force: the committed depth-6/7 CLEAN NULLS were produced under
    the old HARD 6 GB brief and must NEVER be conflated with 40-GB-era results.

  * BOTH-WAYS RULE (non-negotiable): NULL (0 certified) is the expected/valid outcome and is
    reported as CLEAN NULL, never dressed up; any all-gates survivor is CANDIDATE-NEEDING-
    SCRUTINY (escalation STOPS for human scrutiny), never a discovery claim; a sampled search
    can NEVER claim a null and any sampled hit is 'CANDIDATE (sampled, non-exhaustive)'.
    Every in-window hit is evaluated by the REAL committed gate code via the verbatim imports.

  * VALIDATION per depth, never skipped: (a) DN.constructive_completeness_selfcheck (memory-
    light: it holds only skeleton value-key sets; its cost is TIME — the b_s = D-4 brute is
    ~30^(D-4)-sized). If it cannot be run (memory watchdog trip), the depth is recorded
    UNVALIDATED and escalation STOPS rather than reporting an unvalidated null.
    (b) DN.a0_validity_depthN. (c) the 21-target sweep on the streamed value set.

  * RESUMABILITY: results_grind/state.json is written atomically (tmp+rename) at every phase and
    every target boundary; the ledger (results_grind/LEDGER.jsonl) is append-only. Artifact
    files (completeness.json, a0.json, build_meta.json + values.f64 + records.sqlite,
    targets/<key>.json) are the resume truth: on restart, completed phases/targets are skipped
    and at most the in-flight phase/target is redone. SIGINT/SIGTERM: state on disk is always
    the last completed boundary, so the handler just exits 0; kill -9 loses at most the
    in-flight phase's partial work and can never corrupt the append-only ledger or the
    atomically-renamed state file.

DEEP-SAMPLE MODE (`--deep-sample --depth D --trials N [--seed S]`, D up to 14):
    Random sampling of the SAME constructive candidate space at depth D. THE SAMPLER'S ACTUAL
    DISTRIBUTION (fixed, seeded, documented — NOT exactly uniform over distinct values):
      1. a budget split (b_s, g_s) is drawn with probability proportional to
         (11 * 30**b_s) * germ_recipe_count(g_s)  — i.e. proportional to the number of
         GENERATOR TUPLES in the split: 11 base leaves x 30^b_s left-fold skeleton step
         sequences (the same 30-entry step menu as DN._skeleton_value_nodes: 11 leaves x
         {MUL,DIV} + 5 pow exponents + 3 unaries) times the exact canonical germ-recipe count
         (DN._germ_recipe_count).
      2. a skeleton is drawn as (uniform base leaf) + b_s uniform steps from that menu; draws
         whose skeleton is not dimensionless/finite/positive are REJECTED and redrawn (so the
         final distribution is uniform over VALID generator tuples, which tilts the split mix
         toward splits with higher skeleton-validity rates).
      3. a canonical germ recipe is drawn UNIFORMLY over the enumerator's canonical recipe set:
         free germ key uniform; composition (n0,n1,n2) of g_s with probability proportional to
         prod_i |_net_exps(n_i)|; net exponents uniform per key; realized via DN._realize_net.
    Consequence (documented honestly): a distinct VALUE is weighted by its number of valid
    generator tuples — values with many constructive derivations are oversampled relative to a
    uniform-over-distinct-values draw. Per-trial RNG: random.Random(f"grind:{seed}:{trial}")
    (str seeding is sha512-based -> deterministic across processes), so resume needs only the
    trial counter, checkpointed in state.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import signal
import sqlite3
import subprocess
import sys
import threading
import time
from array import array
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import mpmath as mp

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

# --- IMPORT VERBATIM (RULE 3): the whole committed machinery, unmodified -----------------------
import exhaust_depthN_forced as DN                      # noqa: E402
import exhaust_depth5_forced as D5                      # noqa: E402
from engine.expr_tree import ExprNode, OpType           # noqa: E402
from engine.scoring import score_value, measurement_tol # noqa: E402
from exhaust import (                                   # noqa: E402
    build_alphabet, Alphabet, Reachable, _value_key,
    gate_candidate_for, resolve_target,
    _POW_EXPONENTS, _UNARY_PLAIN,
)
from gate import validate                               # noqa: E402
from exhaust_parallel import sm_target_keys             # noqa: E402
from exhaust_depth5_forced import N_TARGETS             # noqa: E402

mp.mp.dps = 40  # same precision as the committed runs (DN sets this too; re-assert)

# =============================================================================
# MEMORY CAP — owner-authorized 40 GB (2026-07-21). RUNTIME attribute override of the imported
# depth-5 watchdog module (zero file diff; RULE 3 intact). exhaust_depth5_forced._mem_watchdog
# reads its OWN module globals, so this changes the effective cap for every verbatim-reused
# code path (constructive_gate_b_reachables, completeness, a0 legs) in this process.
# =============================================================================
GRIND_MEM_CAP_GB = 40.0
D5.HARD_MEM_CAP_GB = GRIND_MEM_CAP_GB
D5._MEM_CAP_MB = GRIND_MEM_CAP_GB * 1024.0
DN.HARD_MEM_CAP_GB = GRIND_MEM_CAP_GB   # DN's from-import copy (used in its prints)

# Output root. Env-overridable (ATOMOS_RESULTS_DIR) so several deep-sample workers can run
# CONCURRENTLY without sharing state.json -- which is written atomically, so it never CORRUPTS, but
# concurrent read-modify-write silently LOSES UPDATES -- or the append-only SAMPLE_LEDGER.jsonl, where
# interleaved lines would corrupt the hit record itself. Added 2026-07-27 to use idle cores: the
# deep-sample path is single-threaded (99% of one core, 0.08 GB) on a 16-core box.
# Unset => the original path, so the in-flight campaign is unaffected.
RESULTS = Path(os.environ.get("ATOMOS_RESULTS_DIR") or (_HERE / "results_grind"))
LEDGER_PATH = RESULTS / "LEDGER.jsonl"
SAMPLE_LEDGER_PATH = RESULTS / "SAMPLE_LEDGER.jsonl"
REPLAY_LEDGER_PATH = RESULTS / "REPLAY_LEDGER.jsonl"   # replay-gate audit trail (separate from
                                                       # LEDGER.jsonl so depth parsing stays clean)
STATE_PATH = RESULTS / "state.json"

# =============================================================================
# COMMITTED GROUND TRUTH (results_exhaust_depthN + notes/DEPTH*_VERDICT.md, 6-GB-era).
# The replay gate must reproduce these EXACTLY or exit nonzero.
# =============================================================================
REPLAY_COMMITTED = {
    6: dict(raw=236_624, distinct=107_719, hits=259, n_certified=0, n_relabeled=0,
            tightest_target="koide_Q_lep", tightest_rel=9.232869166816987e-06,
            tightest_formula="(((((c / c) / 3) * sqrt(8pi/3)) / sqrt(8pi/3)) * 2)",
            committed_wall_s=13.2, committed_mem_cap_gb=6.0),
    7: dict(raw=1_566_116, distinct=498_848, hits=1248, n_certified=0, n_relabeled=0,
            tightest_target="koide_Q_lep", tightest_rel=9.232869166816987e-06,
            tightest_formula="((((((c / c) / 3) * sqrt(8pi/3)) / sqrt(8pi/3)) * (2)^1/2) * (2)^1/2)",
            committed_wall_s=95.3, committed_mem_cap_gb=6.0),
}

_CTX = {"mode": None, "depth": None, "phase": None}   # for the monitor thread + status
_LAST_PS_CHECK = [0.0]


# =============================================================================
# small utilities: atomic state, append-only ledger, RSS
# =============================================================================

def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _atomic_write_json(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, default=str))
    os.replace(tmp, path)   # atomic rename — kill -9 can never leave a corrupt file


def _append_jsonl(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(obj, default=str) + "\n"
    with open(path, "a") as f:
        f.write(line)
        f.flush()
        os.fsync(f.fileno())


def _read_jsonl(path: Path) -> List[dict]:
    """Append-only ledger reader, tolerant of a torn trailing line (kill -9 mid-append)."""
    if not path.exists():
        return []
    out = []
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            print(f"[ledger] WARNING: skipping torn line in {path.name}: {ln[:60]!r}", flush=True)
    return out


def _read_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def _write_state(mode: str, sub: dict):
    """Atomic read-modify-write of state.json, keyed by mode ('run' / 'sample')."""
    st = _read_state()
    st[mode] = {**sub, "updated": _now(), "mem_cap_gb": GRIND_MEM_CAP_GB}
    st["last_mode"] = mode
    _atomic_write_json(STATE_PATH, st)


def _current_rss_gb() -> float:
    """CURRENT RSS via ps (ru_maxrss is a monotonic PEAK — useless for detecting recovery)."""
    try:
        out = subprocess.run(["ps", "-o", "rss=", "-p", str(os.getpid())],
                             capture_output=True, text=True, timeout=10)
        return int(out.stdout.strip()) / (1024.0 * 1024.0)
    except Exception:
        return 0.0


class MemoryWall(Exception):
    """Raised when CURRENT RSS breaches GRIND_MEM_CAP_GB. Recorded, never retried blindly."""


def _grind_watchdog(where: str):
    """Cap enforcement at explicit checkpoints (time-gated: at most one ps call / 5 s).
    ALSO runs the verbatim depth-5 peak-RSS watchdog (now at the overridden 40 GB cap)."""
    now = time.time()
    if now - _LAST_PS_CHECK[0] >= 5.0:
        _LAST_PS_CHECK[0] = now
        rss = _current_rss_gb()
        if rss > GRIND_MEM_CAP_GB:
            raise MemoryWall(f"{where}: current RSS {rss:.2f} GB > cap {GRIND_MEM_CAP_GB:.0f} GB")
    D5._mem_watchdog(where)   # verbatim peak-based watchdog, cap overridden to 40 GB above


def _record_memory_wall(where: str, rss_gb: float):
    entry = dict(ts=_now(), depth=_CTX.get("depth"), phase=_CTX.get("phase"),
                 verdict="MEMORY-WALL", rss_gb=round(rss_gb, 2),
                 mem_cap_gb=GRIND_MEM_CAP_GB, note=f"cap breached @ {where}")
    path = SAMPLE_LEDGER_PATH if _CTX.get("mode") == "sample" else LEDGER_PATH
    _append_jsonl(path, entry)
    print(f"\n[MEMORY-WALL] {entry}", flush=True)


def _start_monitor_thread():
    """Daemon monitor: logs current RSS every 60 s; hard-aborts (record + exit 3) on cap breach
    even inside long verbatim-reused phases that have no explicit checkpoint."""
    def _loop():
        last_log = 0.0
        while True:
            time.sleep(20)
            rss = _current_rss_gb()
            now = time.time()
            if now - last_log >= 60:
                last_log = now
                print(f"[rss] {rss:.2f} GB (cap {GRIND_MEM_CAP_GB:.0f} GB) "
                      f"depth={_CTX.get('depth')} phase={_CTX.get('phase')}", flush=True)
            if rss > GRIND_MEM_CAP_GB:
                _record_memory_wall("monitor-thread", rss)
                os._exit(3)   # do NOT thrash swap; state on disk = last boundary (resumable)
    t = threading.Thread(target=_loop, daemon=True)
    t.start()


def _install_signal_handlers():
    """SIGINT/SIGTERM: exit 0 immediately. Correct because state.json is only ever written
    ATOMICALLY at completed boundaries — the on-disk state is always consistent, and the ledger
    is append-only; a resume redoes at most the in-flight phase/target."""
    def _h(signum, frame):
        print(f"\n[signal] {signal.Signals(signum).name}: state on disk is the last completed "
              f"boundary; exiting 0 (resume with --run / --deep-sample).", flush=True)
        os._exit(0)
    signal.signal(signal.SIGINT, _h)
    signal.signal(signal.SIGTERM, _h)


# =============================================================================
# THE STREAMED BUILD — exact same candidate stream as DN.constructive_gate_b_reachables,
# memory-light: RAM holds {value-key set + float64 value array}; in-window formula records
# spill to sqlite. Validated exact by the replay gate (--replay 6/7).
# =============================================================================

def _target_windows() -> List[Tuple[str, float, float, float]]:
    """(target_key, target_value, tol, widened_abs_window) for the 21 sweep targets.
    Retention uses |v - tv| <= tol*|tv|*(1+1e-9): a strict SUPERSET of the exact hit predicate
    score_value(...).rel_error <= tol (margin 1e-9 >> 1 ulp), so every hit has a record."""
    wins = []
    # include_holdout=True: retention is not a search. Values near a held-back target must be
    # RETAINED or a survivor's out-of-sample prediction for it can never be scored.
    for k in sm_target_keys(include_holdout=True):
        ts = resolve_target(k)
        tol = measurement_tol(ts.pdg_target)
        wins.append((k, float(ts.value), tol, abs(float(ts.value)) * tol * (1.0 + 1e-9)))
    return wins


def _recipe_to_json(recipe) -> str:
    return json.dumps([[gk, op.name, mp.nstr(mp.mpf(e), 20)] for (gk, op, e) in recipe])


def _rebuild_node(alpha: Alphabet, skeleton_provider, b_s: int, skeleton_idx: int,
                  recipe_json: str) -> ExprNode:
    """Rebuild the EXACT ExprNode from (b_s, skeleton index, canonical germ recipe). The
    skeleton list (DN._skeleton_value_nodes) is deterministic, so the index is stable."""
    node = skeleton_provider(b_s)[skeleton_idx].node
    for gk, opname, estr in json.loads(recipe_json):
        node = DN._decorate(node, OpType[opname], gk, mp.mpf(estr))
    return node


def _db_open(path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(str(path))
    con.execute("CREATE TABLE IF NOT EXISTS records ("
                "idx INTEGER PRIMARY KEY, value_key TEXT, value REAL, formula TEXT, "
                "b_s INTEGER, skeleton_idx INTEGER, recipe TEXT)")
    return con


def streamed_build(alpha: Alphabet, depth: int, ddir: Path, verbose: bool = True) -> dict:
    """Build the depth-D distinct dimensionless value set, STREAMED. Writes to ddir:
      values.f64      — the distinct values as raw float64, in first-seen (dedup) order
      records.sqlite  — formula records for every value inside a widened target window
      build_meta.json — counts + wall + peak RSS + mem cap (written LAST => completion marker)
    Returns the meta dict. The enumeration order is IDENTICAL to the verbatim
    DN.constructive_gate_b_reachables generator (same splits / skeletons / canonical recipes /
    filter order), so distinct counts, first-seen formulas and hit sets match exactly."""
    ddir.mkdir(parents=True, exist_ok=True)
    # fresh start: a partial previous build (no build_meta.json) is discarded wholesale
    for f in ("values.f64", "records.sqlite", "build_meta.json"):
        p = ddir / f
        if p.exists():
            p.unlink()

    free_keys = D5._free_germ_keys(alpha)
    splits = DN.budget_splits(depth)
    wins = _target_windows()

    con = _db_open(ddir / "records.sqlite")
    pending: List[tuple] = []

    seen_value = set()
    vals = array("d")
    raw = 0
    n_skeletons_total = 0
    n_retained = 0
    t0 = time.time()
    last_progress = t0
    skeleton_cache: Dict[int, list] = {}

    def _flush():
        nonlocal pending
        if pending:
            con.executemany("INSERT OR REPLACE INTO records VALUES (?,?,?,?,?,?,?)", pending)
            con.commit()
            pending = []

    for (b_s, g_s) in splits:
        skeletons = DN._skeleton_value_nodes(alpha, b_s)   # verbatim skeleton layer
        skeleton_cache[b_s] = skeletons
        n_skeletons_total += len(skeletons)
        recipes = list(DN._germ_recipes(alpha, free_keys, g_s))   # verbatim canonical recipes
        if verbose:
            print(f"[build d{depth}] split (b_s={b_s}, g_s={g_s}): {len(skeletons)} skeletons "
                  f"x {len(recipes)} canonical recipes", flush=True)
        for si, sk in enumerate(skeletons):
            for recipe in recipes:
                node = sk.node
                for (gk, op, e) in recipe:
                    node = DN._decorate(node, op, gk, e)
                raw += 1
                # --- filter order copied from DN.constructive_gate_b_reachables (verbatim) ---
                try:
                    value, label = node.evaluate(alpha)
                except Exception:
                    continue
                try:
                    if not mp.isfinite(value) or value <= 0:
                        continue
                except Exception:
                    continue
                if not label.is_dimensionless():
                    continue
                vk = _value_key(value)
                if vk in seen_value:
                    continue
                seen_value.add(vk)
                fv = float(value)
                vals.append(fv)
                # retention: spill a formula record iff fv is inside ANY widened target window
                for (_tk, tv, _tol, wabs) in wins:
                    if abs(fv - tv) <= wabs:
                        pending.append((len(vals) - 1, vk, fv, node.to_string(alpha),
                                        b_s, si, _recipe_to_json(recipe)))
                        n_retained += 1
                        if len(pending) >= 1000:
                            _flush()
                        break
                if (len(vals) & 0x3FFF) == 0:
                    _grind_watchdog(f"grind-build/depth{depth}")
                    now = time.time()
                    if now - last_progress >= 60:
                        last_progress = now
                        if _CTX.get("mode") == "run":   # replay must not touch run state
                            _write_state("run", {"depth": depth, "phase": "build",
                                                 "build_raw": raw, "build_distinct": len(vals)})
                        if verbose:
                            print(f"[build d{depth}] raw={raw:,} distinct={len(vals):,} "
                                  f"retained={n_retained} rss={_current_rss_gb():.2f}GB "
                                  f"t={now - t0:.0f}s", flush=True)
    _flush()
    con.close()
    _grind_watchdog(f"grind-build/depth{depth}/end")

    with open(ddir / "values.f64", "wb") as f:
        vals.tofile(f)
        f.flush()
        os.fsync(f.fileno())

    meta = dict(
        depth=depth, complete=True, build="streamed",
        raw_candidates=raw, distinct_by_value=len(vals),
        n_splits=len(splits), splits=[list(s) for s in splits],
        n_skeletons_total=n_skeletons_total, n_retained_records=n_retained,
        wall_s=round(time.time() - t0, 1),
        peak_rss_self_gb=round(D5._peak_mem_mb() / 1024.0, 2),
        mem_cap_gb=GRIND_MEM_CAP_GB, ts=_now(),
    )
    _atomic_write_json(ddir / "build_meta.json", meta)   # completion marker, written LAST
    if verbose:
        print(f"[build d{depth}] DONE raw={raw:,} distinct={len(vals):,} retained={n_retained} "
              f"wall={meta['wall_s']}s peakRSS(self)={meta['peak_rss_self_gb']}GB "
              f"(cap {GRIND_MEM_CAP_GB:.0f}GB)", flush=True)
    meta["_skeleton_cache"] = skeleton_cache   # in-process reuse only (not serialized)
    return meta


def _load_values(ddir: Path) -> np.ndarray:
    return np.fromfile(ddir / "values.f64", dtype=np.float64)


def _make_skeleton_provider(alpha: Alphabet, cache: Optional[Dict[int, list]] = None):
    cache = dict(cache) if cache else {}

    def provider(b_s: int):
        if b_s not in cache:
            cache[b_s] = DN._skeleton_value_nodes(alpha, b_s)
        return cache[b_s]
    return provider


# =============================================================================
# THE SWEEP on the streamed value set — hit predicate + report EXACTLY mirroring
# DN.run_target_depthD; every hit goes through the REAL gates via node rebuild.
# =============================================================================

def sweep_target_streamed(alpha: Alphabet, target_key: str, values: np.ndarray,
                          ddir: Path, skeleton_provider, build_meta: dict,
                          verbose: bool = True) -> dict:
    tspec = resolve_target(target_key)
    tol = measurement_tol(tspec.pdg_target)
    tv = float(tspec.value)
    # numpy prefilter on a widened window (superset of the exact predicate); the EXACT hit
    # decision below is the REAL score_value(...).rel_error <= tol, same as run_target_depthD.
    idxs = np.nonzero(np.abs(values - tv) <= abs(tv) * tol * (1.0 + 1e-9))[0]

    con = _db_open(ddir / "records.sqlite")
    hits: List[DN.HitN] = []
    for i in idxs:                       # ascending index == first-seen (reach) order
        fv = float(values[i])
        card = score_value(fv, tspec.pdg_target)
        if card.rel_error > tol:
            continue
        row = con.execute("SELECT value_key, value, formula, b_s, skeleton_idx, recipe "
                          "FROM records WHERE idx=?", (int(i),)).fetchone()
        if row is None:
            raise RuntimeError(f"RETENTION BUG: hit idx {i} (value {fv!r}, target {target_key}) "
                               f"has no spilled record — the widened-window superset failed.")
        vk, stored_fv, formula, b_s, si, recipe_json = row
        node = _rebuild_node(alpha, skeleton_provider, b_s, si, recipe_json)
        v_mpf, lab = node.evaluate(alpha)
        if float(v_mpf) != fv or node.to_string(alpha) != formula:
            raise RuntimeError(f"REBUILD MISMATCH at idx {i}: stored ({fv!r}, {formula!r}) vs "
                               f"rebuilt ({float(v_mpf)!r}, {node.to_string(alpha)!r})")
        r = Reachable(value=v_mpf, label=lab, formula=formula,
                      canonical=node.canonical_hash(), node=node)
        gc = gate_candidate_for(r, alpha, target_key, tspec.pdg_target, N_TARGETS)
        v = validate(gc)                 # THE REAL COMMITTED GATE — never reimplemented
        hits.append(DN.HitN(
            formula=r.formula, value=fv, rel_error=card.rel_error, n_sigma=card.n_sigma,
            status=v.status, fdr_bits=v.fdr.bits, fdr_mode=v.fdr.mode,
            kernel_passed=v.kernel.passed, interlock_passed=v.interlock.passed,
            gate_tell=v.tell))
    con.close()
    hits.sort(key=lambda h: h.rel_error)         # stable, same as run_target_depthD
    certified = [h for h in hits if h.status == "CERTIFIED"]
    relabeled = [h for h in hits if h.status == "REAL-PUZZLE-RE-LABELED"]

    report = {
        "target": target_key, "target_value": tspec.value, "target_dimension": tspec.label_name,
        "depth": build_meta["depth"], "tol": tol,
        "n_leaves": len(alpha.leaves), "n_germs": len(alpha.germs),
        "fdr_uses_full_library": (len(alpha.germs) == 25),
        "constructive_raw_per_target": build_meta["raw_candidates"],
        "constructive_splits": build_meta["splits"],
        "constructive_distinct_values": build_meta["distinct_by_value"],
        "n_hits": len(hits), "n_certified": len(certified), "n_relabeled": len(relabeled),
        "hits": [h.__dict__ for h in hits[:20]],
        "build": "streamed", "mem_cap_gb": GRIND_MEM_CAP_GB,
    }
    if verbose:
        tight = f"{hits[0].rel_error:.2e} ({hits[0].formula[:60]})" if hits else "-"
        print(f"[sweep d{build_meta['depth']}] {target_key:18} hits={len(hits):>4} "
              f"CERT={len(certified)} RELAB={len(relabeled)} tightest={tight}", flush=True)
    return report


def _aggregate_reports(reports: List[dict]) -> dict:
    n_hits = sum(r["n_hits"] for r in reports)
    n_cert = sum(r["n_certified"] for r in reports)
    n_rel = sum(r["n_relabeled"] for r in reports)
    tightest = None
    for r in reports:
        if r["hits"]:
            h = r["hits"][0]
            if tightest is None or h["rel_error"] < tightest["rel_error"]:
                tightest = {"target": r["target"], **h}
    return dict(n_hits=n_hits, n_certified=n_cert, n_relabeled=n_rel, tightest=tightest)


# =============================================================================
# REPLAY GATE — the streamed build must reproduce the committed 6-GB-era depth-6/7 numbers
# EXACTLY (counts, hit totals, tightest hit incl. formula). Exit nonzero on ANY mismatch.
# =============================================================================

def cmd_replay(depth: int) -> int:
    if depth not in REPLAY_COMMITTED:
        print(f"--replay supports depths {sorted(REPLAY_COMMITTED)} (the committed nulls) only.")
        return 2
    com = REPLAY_COMMITTED[depth]
    print(f"REPLAY GATE depth {depth}: streamed build vs the COMMITTED 6-GB-era numbers "
          f"(this run's cap: {GRIND_MEM_CAP_GB:.0f} GB — recorded, never conflated).", flush=True)
    t0 = time.time()
    ddir = RESULTS / f"replay_{depth}"
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25 and len(alpha.leaves) == 11
    meta = streamed_build(alpha, depth, ddir, verbose=True)
    values = _load_values(ddir)
    provider = _make_skeleton_provider(alpha, meta.pop("_skeleton_cache", None))
    # include_holdout=True: the REPLAY GATE is a machinery check against committed ground truth,
    # not a search. It must sweep the full historical target list or it cannot reproduce the
    # committed hit count (see sm_target_keys docstring).
    reports = [sweep_target_streamed(alpha, k, values, ddir, provider, meta, verbose=True)
               for k in sm_target_keys(include_holdout=True)]
    agg = _aggregate_reports(reports)
    wall = time.time() - t0

    checks = [
        ("raw candidates", meta["raw_candidates"], com["raw"],
         meta["raw_candidates"] == com["raw"]),
        ("distinct values", meta["distinct_by_value"], com["distinct"],
         meta["distinct_by_value"] == com["distinct"]),
        ("in-window hits (21 targets)", agg["n_hits"], com["hits"], agg["n_hits"] == com["hits"]),
        ("CERTIFIED", agg["n_certified"], com["n_certified"],
         agg["n_certified"] == com["n_certified"]),
        ("RE-LABELED", agg["n_relabeled"], com["n_relabeled"],
         agg["n_relabeled"] == com["n_relabeled"]),
    ]
    t = agg["tightest"]
    checks.append(("tightest target", t["target"] if t else None, com["tightest_target"],
                   bool(t) and t["target"] == com["tightest_target"]))
    rel_ok = bool(t) and abs(t["rel_error"] - com["tightest_rel"]) <= 1e-12 * com["tightest_rel"]
    checks.append(("tightest rel_err", f"{t['rel_error']:.15e}" if t else None,
                   f"{com['tightest_rel']:.15e}", rel_ok))
    checks.append(("tightest formula", t["formula"] if t else None, com["tightest_formula"],
                   bool(t) and t["formula"] == com["tightest_formula"]))

    print("\n" + "=" * 100)
    print(f"REPLAY depth {depth} — computed vs committed  "
          f"(wall {wall:.1f}s vs committed {com['committed_wall_s']}s 12-way-parallel/6GB-era; "
          f"peak RSS self {D5._peak_mem_mb()/1024.0:.2f} GB, cap {GRIND_MEM_CAP_GB:.0f} GB)")
    print("-" * 100)
    all_ok = True
    for name, got, want, ok in checks:
        all_ok = all_ok and ok
        print(f"  {name:28} computed={got!s:<55.55} committed={want!s:<45.45} "
              f"{'PASS' if ok else '** FAIL **'}")
    print("-" * 100)
    print(f"REPLAY depth {depth}: {'PASS — streamed build is EXACT' if all_ok else 'FAIL — DO NOT TRUST the streamed path'}")
    print("=" * 100, flush=True)
    # persist the verdict so the audit trail can PROVE the replay gate ran and passed
    # (reviewer finding #8: console-only evidence is not an artifact)
    verdict = dict(ts=_now(), kind="replay", depth=depth, all_pass=all_ok, wall_s=round(wall, 1),
                   peak_rss_gb=round(D5._peak_mem_mb() / 1024.0, 3), mem_cap_gb=GRIND_MEM_CAP_GB,
                   checks=[dict(name=n, computed=str(g), committed=str(w), ok=ok)
                           for n, g, w, ok in checks])
    (ddir / "REPLAY_VERDICT.json").write_text(json.dumps(verdict, indent=2))
    _append_jsonl(REPLAY_LEDGER_PATH, verdict)
    return 0 if all_ok else 1


# =============================================================================
# --run: the resumable escalation loop (depth >= 8)
#   phases per depth: completeness -> a0 -> build -> sweep (per-target) -> verdict
#   artifact files are the resume truth; state.json tracks the in-flight position.
# =============================================================================

def _depth_dir(depth: int) -> Path:
    return RESULTS / f"depth_{depth}"


def _set_phase(depth: int, phase: str, extra: Optional[dict] = None):
    _CTX.update(depth=depth, phase=phase)
    _write_state("run", {"depth": depth, "phase": phase, **(extra or {})})


FAST_COMPLETENESS = False   # set by --fast-completeness; recorded per depth, never silent


def run_depth(depth: int) -> dict:
    """One full validated depth. Returns the ledger entry (already appended)."""
    ddir = _depth_dir(depth)
    ddir.mkdir(parents=True, exist_ok=True)
    walls = {}
    t_depth = time.time()

    # ---- phase (a): constructive-completeness self-check (NEVER skipped) --------------------
    comp_path = ddir / "completeness.json"
    if comp_path.exists() and json.loads(comp_path.read_text()).get("constructive_complete"):
        comp = json.loads(comp_path.read_text())
        print(f"[skip] depth {depth} completeness already verified "
              f"(ok, {comp.get('wall_s', '?')}s)", flush=True)
    else:
        _set_phase(depth, "completeness")
        print(f"\n[phase] depth {depth} completeness self-check (b_s={depth-4} brute is "
              f"~30^{depth-4}-sized; this can dominate the depth's wall)", flush=True)
        t0 = time.time()
        try:
            if FAST_COMPLETENESS:
                import fast_completeness as FC
                print(f"[fast] depth {depth}: INDUCTIVE certificate (brute SKIPPED — sound only "
                      f"above a brute-verified anchor; method recorded in the verdict)", flush=True)
                cert = FC.certify(depth, verbose=True)
                comp = dict(constructive_complete=bool(cert.get("certified")),
                            method="inductive-certificate", certificate=cert,
                            wall_s=cert.get("wall_s"))
            else:
                comp = DN.constructive_completeness_selfcheck(depth, verbose=True)
                comp["method"] = "exhaustive-brute"
        except (MemoryWall, SystemExit) as e:
            # cannot run the completeness check => UNVALIDATED, STOP escalating (never report
            # an unvalidated null). Any non-memory SystemExit is a real failure — re-raise.
            msg = str(e)
            if isinstance(e, SystemExit) and ("MEMORY WATCHDOG" not in msg and "VALUE-CAP" not in msg):
                raise
            entry = dict(ts=_now(), depth=depth, verdict="UNVALIDATED",
                         note=f"completeness self-check could not run: {msg[:160]}",
                         mem_cap_gb=GRIND_MEM_CAP_GB)
            _append_jsonl(LEDGER_PATH, entry)
            return entry
        comp["wall_s"] = round(time.time() - t0, 1)
        comp["mem_cap_gb"] = GRIND_MEM_CAP_GB
        _atomic_write_json(comp_path, comp)
        if not comp["constructive_complete"]:
            entry = dict(ts=_now(), depth=depth, verdict="INVALID",
                         note="constructive completeness FAILED — the null would be invalid; HALT",
                         mem_cap_gb=GRIND_MEM_CAP_GB)
            _append_jsonl(LEDGER_PATH, entry)
            raise SystemExit(f"COMPLETENESS FAILED at depth {depth} — HALT (scheme broken).")
    walls["completeness"] = comp.get("wall_s")

    # ---- phase (b): a0 validity (verbatim) --------------------------------------------------
    a0_path = ddir / "a0.json"
    if a0_path.exists() and json.loads(a0_path.read_text()).get("a0_ok"):
        a0 = json.loads(a0_path.read_text())
        print(f"[skip] depth {depth} a0-validity already verified (ok)", flush=True)
    else:
        _set_phase(depth, "a0")
        t0 = time.time()
        a0 = DN.a0_validity_depthN(depth, verbose=True)
        a0["wall_s"] = round(time.time() - t0, 1)
        a0["mem_cap_gb"] = GRIND_MEM_CAP_GB
        _atomic_write_json(a0_path, a0)
        if not a0["a0_ok"]:
            entry = dict(ts=_now(), depth=depth, verdict="INVALID",
                         note="a0-validity FAILED — search broken; HALT",
                         mem_cap_gb=GRIND_MEM_CAP_GB)
            _append_jsonl(LEDGER_PATH, entry)
            raise SystemExit(f"a0-VALIDITY FAILED at depth {depth} — HALT.")
    walls["a0"] = a0.get("wall_s")

    # ---- phase (c1): the streamed build -----------------------------------------------------
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25, "FDR non-smuggle: full 25-germ library required"
    meta_path = ddir / "build_meta.json"
    skeleton_cache = None
    if meta_path.exists() and json.loads(meta_path.read_text()).get("complete"):
        meta = json.loads(meta_path.read_text())
        print(f"[skip] depth {depth} build already complete "
              f"(distinct={meta['distinct_by_value']:,}, {meta['wall_s']}s, "
              f"cap {meta['mem_cap_gb']}GB)", flush=True)
    else:
        _set_phase(depth, "build")
        meta = streamed_build(alpha, depth, ddir, verbose=True)
        skeleton_cache = meta.pop("_skeleton_cache", None)
    walls["build"] = meta["wall_s"]

    # ---- phase (c2): the 21-target sweep, sequential, build shared (like sweep_all) ---------
    values = _load_values(ddir)
    assert len(values) == meta["distinct_by_value"], \
        f"values.f64 length {len(values)} != build_meta distinct {meta['distinct_by_value']}"
    provider = _make_skeleton_provider(alpha, skeleton_cache)
    tdir = ddir / "targets"
    tdir.mkdir(exist_ok=True)
    t0 = time.time()
    reports = []
    targets = sm_target_keys()
    for i, k in enumerate(targets):
        tp = tdir / f"{k}.json"
        if tp.exists():
            reports.append(json.loads(tp.read_text()))
            continue
        _set_phase(depth, "sweep", {"target": k, "target_idx": i, "targets_total": len(targets)})
        rep = sweep_target_streamed(alpha, k, values, ddir, provider, meta, verbose=True)
        _atomic_write_json(tp, rep)
        _grind_watchdog(f"sweep/depth{depth}/{k}")
        reports.append(rep)
    walls["sweep"] = round(time.time() - t0, 1)

    # ---- phase (d): verdict + ledger (idempotent; ledger append is deduped) -----------------
    _set_phase(depth, "verdict")
    agg = _aggregate_reports(reports)
    # BOTH-WAYS RULE: null is the valid expected outcome; a survivor is a candidate for
    # scrutiny, never a discovery.
    if agg["n_certified"] > 0 or agg["n_relabeled"] > 0:
        verdict = "CANDIDATE-NEEDING-SCRUTINY"
    else:
        verdict = "CLEAN NULL"
    walls["total"] = round(time.time() - t_depth, 1)
    verdict_obj = dict(
        ts=_now(), depth=depth, verdict=verdict,
        raw=meta["raw_candidates"], distinct=meta["distinct_by_value"],
        n_hits=agg["n_hits"], n_certified=agg["n_certified"], n_relabeled=agg["n_relabeled"],
        tightest=agg["tightest"], build="streamed",
        wall_s=walls, peak_rss_self_gb=round(D5._peak_mem_mb() / 1024.0, 2),
        mem_cap_gb=GRIND_MEM_CAP_GB,
        validation=dict(completeness_method=comp.get("method", "exhaustive-brute"), completeness_ok=bool(comp.get("constructive_complete")),
                        a0_ok=bool(a0.get("a0_ok"))),
        per_target=[{kk: r[kk] for kk in
                     ("target", "n_hits", "n_certified", "n_relabeled", "tol")}
                    for r in reports],
    )
    _atomic_write_json(ddir / "VERDICT.json",
                       {**verdict_obj, "target_reports": reports})
    already = [e for e in _read_jsonl(LEDGER_PATH)
               if e.get("depth") == depth and e.get("verdict") == verdict]
    if not already:
        _append_jsonl(LEDGER_PATH, verdict_obj)
    print(f"\n[depth {depth}] VERDICT: {verdict}  raw={meta['raw_candidates']:,} "
          f"distinct={meta['distinct_by_value']:,} hits={agg['n_hits']} "
          f"CERT={agg['n_certified']} RELAB={agg['n_relabeled']} wall={walls['total']}s "
          f"(mem cap {GRIND_MEM_CAP_GB:.0f} GB)", flush=True)
    return verdict_obj


_TERMINAL_VERDICTS = ("CLEAN NULL", "CANDIDATE-NEEDING-SCRUTINY")


def _ledger_by_depth() -> Dict[int, dict]:
    out: Dict[int, dict] = {}
    for e in _read_jsonl(LEDGER_PATH):
        if "depth" in e and e["depth"] is not None:
            out[int(e["depth"])] = e     # last entry per depth wins
    return out


def cmd_run(force_depth: Optional[int]) -> int:
    RESULTS.mkdir(exist_ok=True)
    _CTX["mode"] = "run"
    _install_signal_handlers()
    _start_monitor_thread()
    print(f"grind --run  (mem cap {GRIND_MEM_CAP_GB:.0f} GB, owner-authorized 2026-07-21; "
          f"the committed depth-6/7 nulls were 6-GB-era — kept distinct in every record)",
          flush=True)
    led = _ledger_by_depth()
    D = 8
    while D in led and led[D].get("verdict") in _TERMINAL_VERDICTS:
        D += 1
    while True:
        prior = led.get(D)
        if prior and prior.get("verdict") not in _TERMINAL_VERDICTS and force_depth != D:
            print(f"depth {D} previously ended {prior.get('verdict')!r} "
                  f"({prior.get('note', '')}). Not retrying blindly — rerun with "
                  f"--force-depth {D} to retry it.", flush=True)
            return 1
        _CTX.update(depth=D)
        try:
            entry = run_depth(D)
        except MemoryWall as e:
            _record_memory_wall(str(e), _current_rss_gb())
            return 2
        except SystemExit as e:
            msg = str(e)
            if "MEMORY WATCHDOG" in msg or "VALUE-CAP" in msg:
                _record_memory_wall(msg[:160], _current_rss_gb())
                return 2
            raise
        v = entry.get("verdict")
        if v == "CANDIDATE-NEEDING-SCRUTINY":
            print(f"\n*** depth {D}: an all-gates survivor exists. This is a CANDIDATE needing "
                  f"scrutiny, NOT a discovery. Escalation STOPPED for human review "
                  f"(results_grind/depth_{D}/VERDICT.json). ***", flush=True)
            return 4
        if v in ("UNVALIDATED", "INVALID"):
            print(f"depth {D} ended {v}; escalation STOPPED.", flush=True)
            return 1
        led = _ledger_by_depth()
        D += 1
        _write_state("run", {"depth": D, "phase": "pending"})


# =============================================================================
# --deep-sample: seeded random sampling of the SAME constructive space (distribution
# documented in the module docstring). NEVER a null; hits are candidates only.
# =============================================================================

_SAMPLE_MAX_ATTEMPTS_PER_TRIAL = 1000


def _sample_step_menu(alpha: Alphabet) -> List[Tuple]:
    """The SAME 30-entry skeleton step menu as DN._skeleton_value_nodes (mirrored here for
    random access; the exhaustive paths use the verbatim function)."""
    menu: List[Tuple] = []
    for lk in alpha.leaves:
        for op in (OpType.MUL, OpType.DIV):
            menu.append(("app", lk, op))
    for e in _POW_EXPONENTS:
        menu.append(("pow", e, None))
    for u in _UNARY_PLAIN:
        menu.append(("un", u, None))
    return menu


def _apply_step(node: ExprNode, step: Tuple) -> ExprNode:
    kind = step[0]
    if kind == "app":
        _, lk, op = step
        return ExprNode(op, children=[node, D5._leaf_node(lk)])
    if kind == "pow":
        _, e, _ = step
        return ExprNode(OpType.POW, children=[node], exp=e)
    _, u, _ = step
    return ExprNode(u, children=[node])


def _weighted_pick(rng: random.Random, items: list, weights: List[float]):
    x = rng.random() * sum(weights)
    for it, w in zip(items, weights):
        x -= w
        if x <= 0:
            return it
    return items[-1]


def _draw_candidate(alpha, depth, rng, menu, splits, split_weights, free_keys, comp_tables):
    """One sampled candidate from the constructive space, or None after the attempt cap.
    Returns (node, value_mpf, attempts_used)."""
    forced = D5._forced_keys_present(alpha)
    for attempt in range(1, _SAMPLE_MAX_ATTEMPTS_PER_TRIAL + 1):
        b_s, g_s = _weighted_pick(rng, splits, split_weights)
        node = D5._leaf_node(alpha.leaves[rng.randrange(len(alpha.leaves))])
        for _ in range(b_s):
            node = _apply_step(node, menu[rng.randrange(len(menu))])
        try:
            v, lab = node.evaluate(alpha)
        except Exception:
            continue
        try:
            if not mp.isfinite(v) or v <= 0 or not lab.is_dimensionless():
                continue
        except Exception:
            continue
        free = free_keys[rng.randrange(len(free_keys))]
        comps, cweights = comp_tables[g_s]
        comp = _weighted_pick(rng, comps, cweights)
        keys = (forced[0], forced[1], free)
        steps = []
        for key, ni in zip(keys, comp):
            nets = DN._net_exps(ni)
            steps.extend(DN._realize_net(key, ni, nets[rng.randrange(len(nets))]))
        for (gk, op, e) in steps:
            node = DN._decorate(node, op, gk, e)
        try:
            value, label = node.evaluate(alpha)
        except Exception:
            continue
        try:
            if not mp.isfinite(value) or value <= 0 or not label.is_dimensionless():
                continue
        except Exception:
            continue
        return node, value, attempt
    return None, None, _SAMPLE_MAX_ATTEMPTS_PER_TRIAL


def cmd_deep_sample(depth: int, trials: int, seed: int) -> int:
    if not (5 <= depth <= 18):
        print("--deep-sample supports depth 5..18")
        return 2
    RESULTS.mkdir(exist_ok=True)
    _CTX.update(mode="sample", depth=depth, phase="sample")
    _install_signal_handlers()
    _start_monitor_thread()

    sdir = RESULTS / f"sample_d{depth}_s{seed}"
    sdir.mkdir(parents=True, exist_ok=True)
    hits_path = sdir / "hits.jsonl"
    # resume-safety: trials between the last 500-trial checkpoint and an interrupt are redone
    # deterministically (per-trial RNG), so their hits would re-append byte-identical lines
    # (reviewer finding #9). Dedup by (seed, trial, target): load keys already on disk, skip re-appends.
    seen_hits = {(h.get("seed"), h.get("trial"), h.get("target"))
                 for h in _read_jsonl(hits_path)} if hits_path.exists() else set()

    # resume from the trial counter in state (per-trial RNG => no replay needed)
    st = _read_state().get("sample", {})
    start_trial = 0
    attempts_total = 0
    n_hits = 0
    completed0 = 0
    if st.get("depth") == depth and st.get("seed") == seed:
        start_trial = int(st.get("next_trial", 0))
        attempts_total = int(st.get("attempts", 0))
        n_hits = int(st.get("hits", 0))
        completed0 = int(st.get("completed", start_trial))
        if start_trial:
            print(f"[resume] deep-sample d{depth} seed {seed}: continuing at trial "
                  f"{start_trial:,}/{trials:,}", flush=True)

    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25
    menu = _sample_step_menu(alpha)
    free_keys = D5._free_germ_keys(alpha)
    splits = DN.budget_splits(depth)
    n_free = len(free_keys)
    split_weights = [11.0 * (30.0 ** b_s) * DN._germ_recipe_count(alpha, n_free, g_s)
                     for (b_s, g_s) in splits]
    comp_tables = {}
    for (_b, g_s) in splits:
        comps = list(DN._compositions(g_s, 3))
        cweights = [float(len(DN._net_exps(n0)) * len(DN._net_exps(n1)) * len(DN._net_exps(n2)))
                    for (n0, n1, n2) in comps]
        comp_tables[g_s] = (comps, cweights)
    tspecs = [(k, resolve_target(k)) for k in sm_target_keys()]
    tols = {k: measurement_tol(ts.pdg_target) for k, ts in tspecs}

    print(f"deep-sample depth {depth} seed {seed}: trials {start_trial:,}->{trials:,} "
          f"(sampler: uniform over VALID generator tuples — see grind.py docstring; a sampled "
          f"search can NEVER claim a null)", flush=True)
    t0 = time.time()
    completed = completed0
    for trial in range(start_trial, trials):
        rng = random.Random(f"grind:{seed}:{trial}")   # deterministic (sha512 str seeding)
        node, value, att = _draw_candidate(alpha, depth, rng, menu, splits, split_weights,
                                           free_keys, comp_tables)
        attempts_total += att
        if node is None:
            continue   # a failed trial (attempt cap) — counted in attempts, not completed
        completed += 1
        fv = float(value)
        for k, ts in tspecs:
            card = score_value(fv, ts.pdg_target)
            if card.rel_error > tols[k]:
                continue
            _v, lab = node.evaluate(alpha)
            r = Reachable(value=value, label=lab, formula=node.to_string(alpha),
                          canonical=node.canonical_hash(), node=node)
            gc = gate_candidate_for(r, alpha, k, ts.pdg_target, N_TARGETS)
            gv = validate(gc)            # THE REAL GATE
            n_hits += 1
            hit = dict(
                ts=_now(), depth=depth, seed=seed, trial=trial, target=k,
                formula=r.formula, value=fv, rel_error=card.rel_error, n_sigma=card.n_sigma,
                gate_status=gv.status, fdr_bits=gv.fdr.bits, fdr_mode=gv.fdr.mode,
                kernel_passed=gv.kernel.passed, interlock_passed=gv.interlock.passed,
                gate_tell=gv.tell,
                label="CANDIDATE (sampled, non-exhaustive)",
                trials_completed_at_hit=completed, attempts_at_hit=attempts_total,
                mem_cap_gb=GRIND_MEM_CAP_GB,
                multiplicity_note=(
                    f"SAMPLED-TRIALS multiplicity: {completed:,} completed trials x "
                    f"{N_TARGETS} targets at hit time. Conservative E_chance accounting must "
                    f"multiply any per-candidate chance by this multiplicity; the gate FDR "
                    f"above does NOT include it. A sampled search can NEVER establish a null; "
                    f"this is a candidate requiring exhaustive/independent verification, not a "
                    f"discovery."),
            )
            hk = (seed, trial, k)
            if hk not in seen_hits:
                seen_hits.add(hk)
                _append_jsonl(hits_path, hit)
            print(f"[sample HIT] trial {trial:,} {k} rel={card.rel_error:.2e} "
                  f"gate={gv.status} -> {hit['label']}", flush=True)
        if (trial + 1) % 500 == 0:
            _write_state("sample", dict(depth=depth, seed=seed, trials_target=trials,
                                        next_trial=trial + 1, completed=completed,
                                        attempts=attempts_total, hits=n_hits))
            _grind_watchdog(f"deep-sample/d{depth}")
            if (trial + 1) % 10000 == 0:
                rate = (trial + 1 - start_trial) / max(1e-9, time.time() - t0)
                print(f"[sample] {trial + 1:,}/{trials:,} trials ({rate:,.0f}/s) "
                      f"hits={n_hits} rss={_current_rss_gb():.2f}GB", flush=True)

    wall = round(time.time() - t0, 1)
    entry = dict(ts=_now(), depth=depth, seed=seed, verdict="SAMPLED (non-exhaustive — no null claim possible)",
                 trials_requested=trials, trials_completed=completed,
                 attempts=attempts_total, n_hits=n_hits, hits_file=str(hits_path.relative_to(RESULTS)),
                 wall_s=wall, mem_cap_gb=GRIND_MEM_CAP_GB,
                 sampler="uniform over valid generator tuples (see grind.py docstring)",
                 rng=f"random.Random('grind:{seed}:<trial>')")
    _append_jsonl(SAMPLE_LEDGER_PATH, entry)
    _write_state("sample", dict(depth=depth, seed=seed, trials_target=trials,
                                next_trial=trials, completed=completed,
                                attempts=attempts_total, hits=n_hits, done=True))
    print(f"\n[deep-sample] depth {depth} seed {seed}: {completed:,} trials completed "
          f"({attempts_total:,} attempts), {n_hits} in-window hits — ALL labeled "
          f"'CANDIDATE (sampled, non-exhaustive)'. A sampled search NEVER claims a null. "
          f"wall={wall}s", flush=True)
    return 0


# =============================================================================
# --status
# =============================================================================

def cmd_status() -> int:
    print("=" * 100)
    print("GRIND STATUS — resumable depth-escalation grinder "
          f"(cap {GRIND_MEM_CAP_GB:.0f} GB, owner-authorized 2026-07-21)")
    print("-" * 100)
    print("Committed 6-GB-era ground truth (results_exhaust_depthN, notes/DEPTH*_VERDICT.md):")
    print("  D6 CLEAN NULL raw 236,624 / distinct 107,719 / hits 259 / CERT 0 (13.2 s, cap 6 GB)")
    print("  D7 CLEAN NULL raw 1,566,116 / distinct 498,848 / hits 1,248 / CERT 0 (95.3 s, cap 6 GB)")
    print("  D8 = the OLD 6-GB wall (5.77 GB materialized build) — superseded by this grinder's")
    print("       streamed build under the 40 GB cap; entries below record their own mem_cap_gb.")
    print("-" * 100)
    entries = _read_jsonl(LEDGER_PATH)
    if not entries:
        print("LEDGER: empty (no grinder depth completed yet). First run starts at depth 8.")
    else:
        print("LEDGER (results_grind/LEDGER.jsonl):")
        for e in entries:
            if e.get("verdict") in _TERMINAL_VERDICTS:
                w = e.get("wall_s", {})
                print(f"  D{e['depth']}: {e['verdict']:26} raw={e.get('raw', 0):,} "
                      f"distinct={e.get('distinct', 0):,} hits={e.get('n_hits', 0)} "
                      f"CERT={e.get('n_certified', 0)} RELAB={e.get('n_relabeled', 0)} "
                      f"wall={w.get('total', '?')}s cap={e.get('mem_cap_gb')}GB")
                t = e.get("tightest")
                if t:
                    print(f"       tightest: {t['target']} rel={t['rel_error']:.2e} "
                          f"[{t['status']}] {t['formula'][:70]}")
            else:
                print(f"  D{e.get('depth')}: {e.get('verdict')}  {e.get('note', '')[:90]} "
                      f"cap={e.get('mem_cap_gb')}GB")
    st = _read_state()
    if st.get("run"):
        print(f"state.run    : {json.dumps(st['run'])}")
    if st.get("sample"):
        print(f"state.sample : {json.dumps(st['sample'])}")
    sentries = _read_jsonl(SAMPLE_LEDGER_PATH)
    if sentries:
        print("SAMPLE_LEDGER:")
        for e in sentries:
            print(f"  D{e.get('depth')} seed={e.get('seed')} "
                  f"trials={e.get('trials_completed', '?')}/{e.get('trials_requested', '?')} "
                  f"hits={e.get('n_hits')} ({e.get('verdict', '')})")
    print("-" * 100)
    print("ETA notes (honest ranges, NOT precision):")
    done = [e for e in entries if e.get("verdict") in _TERMINAL_VERDICTS]
    if done:
        last = done[-1]
        w = last.get("wall_s", {}).get("total")
        print(f"  last completed depth D{last['depth']} took {w}s under this grinder.")
    print("  raw candidate growth is ~4-5x per depth (measured D6->D7->D8), so each further")
    print("  depth is ~4-5x slower on the build/sweep alone; ON TOP of that the completeness")
    print("  brute for the b_s=D-4 split is ~30^(D-4)-sized (~30x per depth) and DOMINATES from")
    print("  D~10 (b_s=5 measured ~1-2 h; b_s=6 projects to DAYS single-threaded).")
    print("  Exhaustive D14 is not realistic — use --deep-sample for depths beyond the wall.")
    print("=" * 100)
    return 0


# =============================================================================
# CLI
# =============================================================================

def main():
    ap = argparse.ArgumentParser(description="Resumable depth-escalation grinder (40 GB cap; "
                                             "verbatim imports of the committed machinery).")
    ap.add_argument("--run", action="store_true", help="escalate from the first depth >=8 not in the ledger")
    ap.add_argument("--replay", type=int, default=None, help="replay gate: 6 or 7; exit nonzero on ANY mismatch")
    ap.add_argument("--fast-completeness", action="store_true",
                    help="certify completeness by the INDUCTIVE certificate (fast_completeness.py) "
                         "instead of the ~30^(D-4) exhaustive brute. Sound but weaker: use only for "
                         "depths ABOVE a brute-verified anchor, and re-run a full brute every few "
                         "depths. The method used is recorded per depth in the ledger/verdict.")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--deep-sample", action="store_true")
    ap.add_argument("--depth", type=int, default=None, help="deep-sample depth (<=14)")
    ap.add_argument("--trials", type=int, default=None, help="deep-sample trial count")
    ap.add_argument("--seed", type=int, default=0, help="deep-sample seed (default 0)")
    ap.add_argument("--force-depth", type=int, default=None,
                    help="retry a depth previously recorded MEMORY-WALL/UNVALIDATED")
    args = ap.parse_args()

    if args.replay is not None:
        sys.exit(cmd_replay(args.replay))
    global FAST_COMPLETENESS
    FAST_COMPLETENESS = bool(getattr(args, 'fast_completeness', False))
    if args.status:
        sys.exit(cmd_status())
    if args.deep_sample:
        if args.depth is None or args.trials is None:
            ap.error("--deep-sample requires --depth D and --trials N")
        sys.exit(cmd_deep_sample(args.depth, args.trials, args.seed))
    if args.run:
        sys.exit(cmd_run(args.force_depth))
    ap.print_help()


if __name__ == "__main__":
    main()
