#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG324 shared harness: tee to the lane's own .out, named checks, results JSON, rc.  MUTATE = env CFG324_MUTATE=1
(outputs suffixed _MUTATE).  Nothing here writes outside this folder."""
import os, sys, json, math, time, builtins
import numpy as np

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
DATA = os.path.join(REPO, "real_research", "data")
MUTATE = os.environ.get("CFG324_MUTATE", "0") == "1"
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}           # the standing footings; kappa = 1/2 FITTED, fixed
FOOTS = ("canonical", "alt")
trapz = getattr(np, "trapezoid", None) or np.trapz


def jclean(o):
    if isinstance(o, dict):
        return {(k if isinstance(k, str) else str(k)): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    if isinstance(o, np.floating):
        o = float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return str(o)
    return o


class Run:
    def __init__(self, slug):
        suf = "_MUTATE" if MUTATE else ""
        self.out_path = os.path.join(HERE, f"{slug}{suf}.out")
        self.json_path = os.path.join(HERE, f"{slug}{suf}_results.json")
        self._f = builtins.open(self.out_path, "w", encoding="utf-8")
        self._stdout = sys.stdout
        sys.stdout = self
        self.t0 = time.time()
        self.OUT = {"lane": "CFG324", "script": slug, "mutate": MUTATE, "checks": {}, "numbers": {}}
        self.CH = []

    def write(self, t):
        self._stdout.write(t)
        self._f.write(t)

    def flush(self):
        self._stdout.flush()
        self._f.flush()

    def P(self, *a):
        print(*a, flush=True)

    def banner(self, t):
        self.P("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)

    def check(self, name, measured, ok, load_bearing=True, reading=""):
        ok = bool(ok)
        key = name.split()[0]
        k2, j = key, 1
        while k2 in self.OUT["checks"]:
            j += 1
            k2 = f"{key}#{j}"
        self.CH.append((k2, ok, load_bearing))
        self.OUT["checks"][k2] = {"ok": ok, "load_bearing": load_bearing, "measured": str(measured), "name": name}
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
        if reading:
            self.P(f"         reading:  {reading}")
        return ok

    def num(self, key, value):
        self.OUT["numbers"][key] = jclean(value)
        return value

    def finish(self):
        npass = sum(1 for _, ok, _ in self.CH if ok)
        nlb = sum(1 for _, ok, lb in self.CH if (not ok) and lb)
        self.OUT["summary"] = {"n_checks": len(self.CH), "n_pass": npass, "load_bearing_failures": nlb,
                               "failed": [k for k, ok, _ in self.CH if not ok], "seconds": round(time.time() - self.t0, 1)}
        with builtins.open(self.json_path, "w", encoding="utf-8") as fh:
            json.dump(jclean(self.OUT), fh, indent=1)
        self.P(f"\n  {npass}/{len(self.CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(self.json_path)} "
               f"({time.time() - self.t0:.0f} s)")
        rc = 1 if nlb else 0
        self.P(f"rc = {rc}")
        sys.stdout = self._stdout
        self._f.close()
        return rc
