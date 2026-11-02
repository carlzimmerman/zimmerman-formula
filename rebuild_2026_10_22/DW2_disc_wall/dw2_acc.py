#!/usr/bin/env python3
"""Runs RQ2's acceptance.py unedited in logic, with outputs and caches redirected into this lane. Usage: python3 dw2_acc.py cand_max.py [--no-keys] [--no-bullet]; result tag from DW2_TAG."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RQ = os.path.join(os.path.dirname(HERE), "RQ2_framework_acceptance"); p = os.path.join(RQ, "acceptance.py"); s = open(p).read()
a = 'HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)'; assert s.count(a) == 2; s = s.replace(a, f'HERE = {RQ!r}; OUTD = {os.path.join(HERE, "acc")!r}; RB = os.path.dirname(HERE)', 1)
for x in ('os.path.join(HERE, "cache_crg", "p")', 'os.path.join(HERE, "cache_crg", "c")', 'os.path.join(HERE, f"cache_keys", f"{name}{TAG}_{tag}")', 'os.path.join(HERE, "results")', 'os.path.join(HERE, "results", f"{tag}{TAG}.out")', 'os.path.join(HERE, "results", f"{tag}{TAG}.json")'):
    assert s.count(x) >= 1, x; s = s.replace(x, x.replace("os.path.join(HERE,", "os.path.join(OUTD,"))
g = {"__name__": "__main__", "__file__": p}; exec(compile(s, p, "exec"), g)
