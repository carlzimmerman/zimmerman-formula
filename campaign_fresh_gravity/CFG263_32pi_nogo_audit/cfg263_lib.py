"""CFG263 shared helpers: a check registry that can FAIL, a results.json writer,
and the frozen classifier / door rule (CFG263_FROZEN_CRITERIA.md sections 3-4).

Written before any audit script was run. c = G = 1 unless stated.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


class Checks:
    """Collects named checks. Each check prints PASS/FAIL; nothing is silently skipped."""

    def __init__(self, lane):
        self.lane = lane
        self.rows = []
        self.values = {}

    def check(self, cid, cond, detail=""):
        ok = bool(cond)
        self.rows.append({"id": cid, "pass": ok, "detail": str(detail)})
        print(f"[{'PASS' if ok else 'FAIL'}] {self.lane}:{cid}  {detail}")
        return ok

    def value(self, key, val):
        """Record a computed number or string for results.json and the compare step."""
        try:
            v = float(val)
        except (TypeError, ValueError):
            v = str(val)
        self.values[key] = v
        print(f"    value {self.lane}:{key} = {val}")
        return val

    def summary(self):
        n = len(self.rows)
        k = sum(r["pass"] for r in self.rows)
        print(f"== {self.lane}: {k}/{n} checks pass")
        return k, n

    def write(self, extra=None):
        """Merge this lane's block into results.json (one key per lane)."""
        # mutation runs redirect here (CFG263_RESULTS) so they never touch the main results.json
        path = os.environ.get("CFG263_RESULTS", os.path.join(HERE, "results.json"))
        data = {}
        if os.path.exists(path):
            with open(path) as fh:
                data = json.load(fh)
        k, n = self.summary()
        block = {"pass": k, "total": n, "checks": self.rows, "values": self.values}
        if extra:
            block.update(extra)
        data[self.lane] = block
        with open(path, "w") as fh:
            json.dump(data, fh, indent=1, sort_keys=True)
        return k == n


# ---------------------------------------------------------------------------
# Frozen classifier (criteria section 3). Inputs are premise flags established by
# the scripts; the order of precedence is ERROR > PREMISE-UNVERIFIED > NARROWER > GENERAL.
# ---------------------------------------------------------------------------
CLASSES = ("CORRECT-GENERAL", "CORRECT-NARROWER-THAN-WORDED", "PREMISE-UNVERIFIED", "ERROR")


def classify(flags):
    """flags: dict with booleans
    step_false            -- a load-bearing step re-derived as false
    premise_unverified    -- conclusion rests on a premise nobody verified, or a unit-dependent
                             pi-count presented as unit-free and load-bearing for the headline
    headline_scope_ok     -- the headline wording's class equals the class the derivation covers
    """
    if flags.get("step_false"):
        return "ERROR"
    if flags.get("premise_unverified"):
        return "PREMISE-UNVERIFIED"
    if not flags.get("headline_scope_ok", False):
        return "CORRECT-NARROWER-THAN-WORDED"
    return "CORRECT-GENERAL"


def door(flags):
    """Criteria section 4. Returns (bool, reason)."""
    if flags.get("step_false") and flags.get("corrected_admits_named_route"):
        return True, "D-a: error whose correction admits a named route"
    narrower = (not flags.get("headline_scope_ok", False)) or flags.get("premise_unverified")
    need = ("specific_route", "route_not_in_record", "route_u_algebraic", "route_no_inserted_target")
    if narrower and all(flags.get(k) for k in need):
        return True, "D-b: narrower class with a specific, uncomputed, u-algebraic route"
    missing = [k for k in need if not flags.get(k)]
    return False, "no door (" + ("narrower; missing " + ", ".join(missing) if narrower else "class as worded") + ")"


def run_main(fn):
    ok = fn()
    sys.exit(0 if ok else 1)
