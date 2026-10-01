#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG244 common helpers: repository discovery (ZF_REPO or walk up from __file__), read-only access to the record's lane code,
a small Report class that never prints an absolute home path, and JSON cleaning.  The repository is READ, never written."""
import os, sys, json, math, io, contextlib, time

sys.dont_write_bytecode = True      # never leave a __pycache__ in the repository
HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    z = os.environ.get("ZF_REPO")
    if z and os.path.isdir(os.path.join(z, "campaign_fresh_gravity")):
        return os.path.abspath(z)
    p = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(p, "campaign_fresh_gravity")) and os.path.isdir(os.path.join(p, "hunt_2026")):
            return p
        p = os.path.dirname(p)
    raise SystemExit("cannot find the repository: set ZF_REPO to the repository root")


REPO = find_repo()
LANES = os.path.join(REPO, "campaign_fresh_gravity")
HOME = os.path.expanduser("~")


def scrub(s):
    s = str(s)
    for a, b in ((REPO, "<repo>"), (HERE, "<lane>"), (HOME, "~")):
        if a and a != "/":
            s = s.replace(a, b)
    return s


def use_lane_code():
    sys.path.insert(0, LANES)
    sys.path.insert(0, os.path.join(REPO, "hunt_2026"))


def jclean(o):
    import numpy as np
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.floating,)):
        o = float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    if isinstance(o, float):
        if math.isnan(o) or math.isinf(o):
            return None if math.isnan(o) else ("inf" if o > 0 else "-inf")
    return o


def exec_prefix(fname, marker, replace=None):
    """Read-only exec of the part of a lane script that precedes `marker` (its MUTATE forced off, stdout silenced)."""
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    src = open(os.path.join(LANES, fname)).read()
    pre = src[:src.index(marker)]
    for a, b in (replace or []):
        assert pre.count(a) == 1
        pre = pre.replace(a, b)
    g = {"__file__": os.path.join(LANES, fname), "__name__": "lane_" + fname}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(pre, fname, "exec"), g)
    finally:
        os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return g


BAR = "# ================================================================================================ "


class Report:
    def __init__(self, slug):
        self.slug = slug; self.lines = []; self.numbers = {}; self.checks = []; self.t0 = time.time()

    def P(self, s=""):
        s = scrub(s); print(s, flush=True); self.lines.append(s)

    def banner(self, s):
        self.P("\n" + "=" * 110 + "\n" + s + "\n" + "=" * 110)

    def check(self, name, detail, ok, kind="control"):
        self.checks.append(dict(name=name, detail=scrub(detail), ok=bool(ok), kind=kind))
        self.P(f"  [{'PASS' if ok else 'FAIL'}] ({kind}) {name}\n         {detail}")

    def num(self, k, v):
        self.numbers[k] = v

    def write(self, extra=None):
        d = dict(slug=self.slug, repo_label="<repo>", numbers=self.numbers, checks=self.checks,
                 seconds=round(time.time() - self.t0, 1))
        if extra:
            d.update(extra)
        json.dump(jclean(d), open(os.path.join(HERE, self.slug + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")
