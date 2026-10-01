#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG242_common -- shared machinery for lane CFG242 (Gaps 1 + 2: a legal owned object).  Nothing in the repository is edited; committed
lanes (CFG44 Bcommon, CFG48 Gcommon, CFG7_common) are imported READ-ONLY.  Repo root: ZF_REPO, else walk up from __file__ to the
directory that holds campaign_fresh_gravity/.  Every printed path is <repo>/...; no absolute home path is printed or stored.

Units: kpc, km/s, Msun (G = 4.30091727e-6 kpc (km/s)^2/Msun, as in Bcommon).  Canonical a0 = 9.3603e-11 m/s^2, alt 1.1312e-10.
kappa = 1/2 is FITTED.  The Lambda tie rho_Lambda = (a0/(kappa c))^2 / G is the CFG43 tie read backwards (a0 is the input, as everywhere
in the record); nothing here fits anything.  Nothing here says the theory is closed; the cold mass is still required.

Run: tees to a mode-named .out and .json (no mode overwrites another).  Exit convention: main exits 0 iff every 'control' check passes;
MUTATE=<m> exits 1 iff the control BITES (every claim handed to finish() is True), else 0 (a declared control failure, kept).
"""
import os, sys, json, math, time, importlib.util
import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    env = os.environ.get("ZF_REPO")
    if env and os.path.isdir(os.path.join(env, "campaign_fresh_gravity")):
        return os.path.abspath(env)
    d = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("CFG242: set ZF_REPO to the repository root (walk-up from __file__ found none)")


REPO = find_repo()


def scrub(s):
    s = str(s).replace(REPO, "<repo>")
    home = os.path.expanduser("~")
    s = s.replace(home, "~")
    return s.replace(HERE, "<lane>")


def _load(name, relpath):
    p = os.path.join(REPO, relpath)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


B = _load("Bcommon", "campaign_fresh_gravity/CFG44_fluid_target/Bcommon.py")
G, A0, A0_SI_CAN, KPC_M, C_KMS = B.G, B.A0, B.A0_SI, B.KPC_M, B.C_KMS
A0_SI_ALT = 1.1312e-10
OMEGA_C_OVER_B = B.OMEGA_C_OVER_B
KAPPA = 0.5
GYR_PER_KPC_KMS = KPC_M / 1e3 / 3.15576e16 / 1e0      # 1 kpc/(km/s) in Gyr
GYR_PER_KPC_KMS = KPC_M / 1e3 / (3.15576e7 * 1e9)
OM, HH, DELTA_TA48 = 0.3153, 0.6736, 11.81            # CFG48's convention
RHOC0_MPC = 2.775e11 * HH ** 2
RHO_L = (A0 / (KAPPA * C_KMS)) ** 2 / G               # Msun/kpc^3 (canonical tie)
SQRT_G_RHO_L = math.sqrt(G * RHO_L)                   # (km/s)/kpc
TAU_L_GYR = 1.0 / (KAPPA * SQRT_G_RHO_L) * GYR_PER_KPC_KMS   # tau_L = 1/(kappa sqrt(G rho_Lambda)) in Gyr
T0_GYR = 13.79
MASSES = (1e9, 1e10, 1e11, 1e12)


def r_M_kpc(Mb):
    return math.sqrt(G * Mb / A0)


def r_ta48_kpc(Mb):
    Mcol = Mb * (1.0 + OMEGA_C_OVER_B)
    return 1e3 * (3.0 * Mcol / (4.0 * math.pi * OM * RHOC0_MPC * DELTA_TA48)) ** (1.0 / 3.0)


def load_c7():
    sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
    import CFG7_common as C7                        # read-only import (B's committed r_ta_law)
    return C7


class Run:
    def __init__(self, slug):
        self.slug = slug
        self.mutate = os.environ.get("MUTATE", "").strip()
        self.tag = slug + (f"_MUTATE_{self.mutate}" if self.mutate else "")
        self.lines, self.checks, self.nums = [], [], {}
        self.t0 = time.time()
        self.P(f"# {self.tag}   repo = <repo>   mode = {self.mutate or 'main'}")

    def P(self, s=""):
        s = scrub(s)
        print(s, flush=True)
        self.lines.append(s)

    def banner(self, s):
        self.P("\n" + "=" * 100 + f"\n{s}\n" + "=" * 100)

    def check(self, name, ok, detail="", kind="control"):
        """kind 'control' = reproduction/identity check (failure => main exit 1); 'result' = a gate cell (a FAIL is a result)."""
        ok = bool(ok)
        self.checks.append(dict(name=name, ok=ok, detail=scrub(detail), kind=kind))
        self.P(f"  [{'PASS' if ok else 'FAIL'}] ({kind}) {name}" + (f"   ({scrub(detail)})" if detail else ""))
        return ok

    def num(self, k, v):
        self.nums[k] = v

    def verdict(self, gate, status, why):
        self.nums.setdefault("verdicts", {})[gate] = dict(status=status, why=scrub(why))
        self.P(f"  >>> {gate}: {status} -- {scrub(why)}")

    def main_cells(self):
        """the main run's checks (for MUTATE comparison); {} if the main run has not been written."""
        p = os.path.join(HERE, f"{self.slug}.json")
        if not os.path.exists(p):
            return {}
        return {c["name"]: c["ok"] for c in json.load(open(p))["checks"]}

    def finish(self, bite_claims=None):
        ctrl_fail = [c for c in self.checks if c["kind"] == "control" and not c["ok"]]
        out = dict(slug=self.tag, mutate=self.mutate, runtime_s=round(time.time() - self.t0, 2), checks=self.checks, numbers=self.nums)
        if self.mutate:
            bit = bool(bite_claims) and all(bite_claims)
            out["control_bites"] = bit
            self.P(f"\nMUTATE {self.mutate}: control {'BITES (exit 1)' if bit else 'DOES NOT BITE (declared control failure, exit 0)'}")
            code = 1 if bit else 0
        else:
            self.P(f"\nRESULT: {len(self.checks)} checks, {len(ctrl_fail)} control failure(s): "
                   + ("; ".join(c['name'] for c in ctrl_fail) if ctrl_fail else "none") + f"   ({time.time() - self.t0:.0f} s)")
            code = 1 if ctrl_fail else 0

        def clean(o):
            if isinstance(o, dict):
                return {str(k): clean(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [clean(v) for v in o]
            if isinstance(o, (np.floating, np.integer)):
                return o.item()
            if isinstance(o, np.bool_):
                return bool(o)
            if isinstance(o, np.ndarray):
                return clean(o.tolist())
            if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
                return str(o)
            return o
        with open(os.path.join(HERE, f"{self.tag}.out"), "w") as f:
            f.write("\n".join(self.lines) + "\n")
        with open(os.path.join(HERE, f"{self.tag}.json"), "w") as f:
            json.dump(clean(out), f, indent=1)
        sys.exit(code)
