#!/usr/bin/env python3
"""DP6 (criteria FROZEN_CRITERIA.md, ee74edfda2): the filed Amendment 17 cut 12 (NSS screen) inside the frozen builder.

NEW file. No frozen file is edited. The frozen `catalog_builder/build_catalog.py` frozen_cuts computes the NSS screen from
a per-star column that DR4's gaia_source does not have (DP3 open issue O8). This module builds a patched frozen_cuts from
the frozen function's own source text. Exactly one line is replaced:

    nss = (S["non_single_star"][a] > 0) | (S["non_single_star"][b] > 0)
 -> nss = _DP6_NSS(S, a, b)

`_DP6_NSS` returns `cut12_nss_union.run_a17(manifest, ids_a, ids_b)[reading]`. That is the binding A17 reading (default
'A17_primary'; never chosen from the data), pair by pair, so the own-pair exemption applies to that pair only. Results are
cached by the sha256 of the two id arrays.

The patched source is registered in linecache, so inspect.getsource works on it and CFG816's patched_frozen_cuts
(drop_nss / smax, DP1's rung) composes on top.

  install(manifest_path_or_dict, reading="A17_primary")   puts the patched function into the builder module (= the driver's B)
  uninstall()                                             restores the frozen function object
  last_report()                                           run_a17's report for the most recent distinct pair set
  write_per_star(stage_a, out)                            stage A + non_single_star = 0 (R input, D7 N5: --declare-neutral)
"""
import sys
sys.dont_write_bytecode = True
import copy, hashlib, inspect, json, linecache
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PREP = REPO / "prep_2026" / "gaia_dr4_prep"
for p in (PREP / "catalog_builder", PREP, PREP / "dr4_ready_1"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
import build_catalog as B                                   # read-only: the same module object the driver imports
import cut12_nss_union as U                                 # read-only

NSS_SRC = '    nss = (S["non_single_star"][a] > 0) | (S["non_single_star"][b] > 0)\n'
NSS_NEW = '    nss = _DP6_NSS(S, a, b)\n'
CUT_LINE = '        "NSS screen": ~nss,\n'
FILENAME = "<dp6 a17 frozen_cuts>"
_MUTATE = None                                              # test hook only: "screen_off"
_STATE = dict(original=None, patched=None, reading=None, report=None)


def patched_source(orig_fn=None):
    src = inspect.getsource(orig_fn or B.frozen_cuts)
    if src.count(NSS_SRC) != 1:
        raise RuntimeError("the frozen NSS line is not found exactly once: refusing to patch")
    if src.count(CUT_LINE) != 1:
        raise RuntimeError("the frozen 'NSS screen' cut line is not found exactly once: refusing to patch")
    return src.replace(NSS_SRC, NSS_NEW)


def _make_nss(c12, reading):
    cache = {}

    def nss(S, a, b):
        ia = np.asarray(S["source_id"][a], np.int64)
        ib = np.asarray(S["source_id"][b], np.int64)
        key = hashlib.sha256(ia.tobytes() + b"|" + ib.tobytes()).hexdigest()
        if key not in cache:
            flags, rep = U.run_a17({"cut12_nss": copy.deepcopy(c12)}, ia, ib)
            if reading not in flags:
                raise KeyError(f"reading {reading!r} not produced by run_a17")
            cache[key] = np.asarray(flags[reading], bool)
            _STATE["report"] = dict(reading=reading, n_pairs=int(len(ia)), n_rejected=int(cache[key].sum()), a17_report=rep)
        r = cache[key]
        if _MUTATE == "screen_off":
            return np.zeros(len(r), bool)
        return r.copy()
    return nss


def install(manifest, reading="A17_primary"):
    man = json.loads(Path(manifest).read_text()) if not isinstance(manifest, dict) else manifest
    c12 = man.get("cut12_nss") or {}
    readings = c12.get("readings") or {}
    if readings and reading not in readings:
        raise KeyError(f"reading {reading!r} is not declared in cut12_nss.readings ({sorted(readings)})")
    if _STATE["original"] is None:
        _STATE["original"] = B.frozen_cuts
    orig = _STATE["original"]
    src = patched_source(orig)
    linecache.cache[FILENAME] = (len(src), None, src.splitlines(True), FILENAME)
    ns = B.__dict__
    ns["_DP6_NSS"] = _make_nss(c12, reading)
    exec(compile(src, FILENAME, "exec"), ns)               # defines frozen_cuts in the builder's own namespace
    _STATE.update(patched=ns["frozen_cuts"], reading=reading, report=None)
    return ns["frozen_cuts"]


def uninstall():
    if _STATE["original"] is not None:
        B.frozen_cuts = _STATE["original"]
        B.__dict__.pop("_DP6_NSS", None)
    _STATE.update(original=None, patched=None, reading=None)


def last_report():
    return _STATE["report"]


def write_per_star(stage_a, out):
    z = np.load(stage_a)
    d = {k: z[k] for k in z.files}
    if "non_single_star" in d:
        raise ValueError("stage A already has non_single_star: not a DR4 extract, refusing to overwrite it")
    d["non_single_star"] = np.zeros(len(d["source_id"]), np.int16)
    np.savez(out, **d)
    return out
