# -*- coding: utf-8 -*-
"""CFG124 (door 10, mimetic gravity) shared helpers.  Nothing in the repository is edited; other lanes are imported READ-ONLY.
Path independence: the repository root is ZF_REPO if set, else found by walking up from this file until
campaign_fresh_gravity/CFG44_fluid_target/Bcommon.py exists.  Outputs go next to the script (HERE).
MUTATE env var: '' (main), 'a' (hand-supplied support / force), 'b' (sound speed / window), 'c' (designed sink), '1' (all).
Convention (as CFG48/CFG72): every check is a CLAIM (mostly the pre-declared expectation); a load-bearing claim that is false
makes the script exit 1; the MUTATE modes are built to make at least one load-bearing claim false.
kappa = 1/2 is FITTED; nothing here fits kappa.  Units: kpc, km/s, Msun, Gyr where stated.
"""
import os, sys, json, time, math
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUTATE", "")
assert MUT in ("", "a", "b", "c", "1"), "MUTATE must be '', a, b, c or 1"


def MU(letter):
    """True when the mutation `letter` is active (mode '1' activates all)."""
    return MUT == "1" or MUT == letter


def find_repo():
    env = os.environ.get("ZF_REPO")
    marker = os.path.join("campaign_fresh_gravity", "CFG44_fluid_target", "Bcommon.py")
    if env and os.path.exists(os.path.join(env, marker)):
        return os.path.abspath(env)
    p = HERE
    for _ in range(8):
        if os.path.exists(os.path.join(p, marker)):
            return p
        p = os.path.dirname(p)
    raise RuntimeError("repository not found: set ZF_REPO to the zimmerman-formula checkout")


def repo():
    return find_repo()          # lazy: T0 (sympy only) does not need the repository


def import_bcommon():
    sys.path.insert(0, os.path.join(repo(), "campaign_fresh_gravity", "CFG44_fluid_target"))
    import Bcommon  # read-only import (target, profiles, kernels)
    return Bcommon


def tag():
    return "" if MUT == "" else "_MUTATE_" + MUT


class Report:
    def __init__(self, slug):
        self.slug = slug + tag()
        self.lines, self.checks, self.numbers, self.t0 = [], [], {}, time.time()

    def P(self, s=""):
        print(s, flush=True)
        self.lines.append(str(s))

    def banner(self, s):
        self.P("\n" + "=" * 110 + "\n" + s + "\n" + "=" * 110)

    def check(self, name, claim, measured, ok, load_bearing=True):
        self.checks.append(dict(name=name, claim=claim, measured=str(measured), ok=bool(ok), load_bearing=load_bearing))
        self.P("  [%s]%s %s  %s\n         measured: %s" % ("PASS" if ok else "FAIL", "" if load_bearing else " (reported)", name, claim, measured))

    def num(self, k, v):
        self.numbers[k] = v

    def write(self):
        lb = [c for c in self.checks if c["load_bearing"]]
        nf = sum(not c["ok"] for c in lb)
        self.P("\n  %d/%d checks pass; load-bearing failures: %d   (%.0f s)   MUTATE=%r" % (sum(c["ok"] for c in self.checks), len(self.checks), nf, time.time() - self.t0, MUT))

        def clean(o):
            if isinstance(o, dict):
                return {str(k): clean(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [clean(v) for v in o]
            try:
                import numpy as np
                if isinstance(o, np.ndarray):
                    return clean(o.tolist())
                if isinstance(o, np.generic):
                    return clean(o.item())
            except Exception:
                pass
            if isinstance(o, float):
                return o if math.isfinite(o) else str(o)
            return o if isinstance(o, (int, str, bool)) or o is None else str(o)

        json.dump(clean(dict(slug=self.slug, mutate=MUT, load_bearing_failures=nf, checks=self.checks, numbers=self.numbers)),
                  open(os.path.join(HERE, self.slug + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, self.slug + ".out"), "w", encoding="utf-8").write("\n".join(self.lines) + "\n")
        return nf
