#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG188_common -- shared helpers for CFG188 (independent referee re-derivation of CFG172's physics core).
kappa = 1/2 is FITTED.  Nothing here says the theory is closed or that data favour the framework.
Repo root: ZF_REPO or walk up from __file__ (printed as <repo>).  No absolute home path is ever printed or stored."""
import os, sys, json, math, importlib.util
import numpy as np
from scipy.optimize import brentq

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = "<scratch>"

def repo_root():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(r):
        return os.path.abspath(r)
    d = HERE
    for _ in range(12):
        if os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    return None

def scrub(s):
    s = str(s)
    for p in (os.path.expanduser("~"), HERE, repo_root() or "@@none@@"):
        if p and p not in ("/",):
            s = s.replace(p, "<repo>" if p == repo_root() else SCR)
    return s

def mode():
    return os.environ.get("MUTATE", "").strip()

def out_json(script_file, obj):
    base = os.path.splitext(os.path.basename(script_file))[0]
    m = mode()
    name = f"{base}_MUTATE_{m}_results.json" if m else f"{base}_results.json"
    with open(os.path.join(HERE, name), "w") as f:
        json.dump(obj, f, indent=1, default=lambda o: float(o) if hasattr(o, "__float__") else str(o))
    return name

class Checks:
    def __init__(self):
        self.rows = []
    def add(self, name, ok, detail=""):
        self.rows.append((name, bool(ok), scrub(detail)))
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {scrub(detail)}")
    def expect(self, name, ok, detail=""):
        """an EXPECTATION (a hand estimate or a verdict), not a reproduction control: recorded, never affects the exit code"""
        self.exps = getattr(self, "exps", [])
        self.exps.append((name, bool(ok), scrub(detail)))
        print(f"  [{'EXPECTATION HELD' if ok else 'EXPECTATION WRONG (kept)'}] {name}  {scrub(detail)}")
    def all_ok(self):
        return all(r[1] for r in self.rows)
    def dump(self):
        return [{"name": n, "ok": o, "detail": d} for n, o, d in self.rows]

def finish(script_file, checks, results, bit_name=None, bit_ok=None):
    """main: exit 0 iff all reproduction controls pass.  MUTATE: exit 1 iff the control bites."""
    results["checks"] = checks.dump()
    results["expectations"] = [{"name": n, "held": o, "detail": d} for n, o, d in getattr(checks, "exps", [])]
    results["mode"] = mode() or "main"
    if mode():
        results["mutate_bites"] = bool(bit_ok)
        results["mutate_claim"] = bit_name
        print(f"MUTATE={mode()}: control '{bit_name}' {'BITES (claim fails as required) -> exit 1' if bit_ok else 'DID NOT BITE (declared control failure) -> exit 0'}")
        out_json(script_file, results)
        sys.exit(1 if bit_ok else 0)
    print("MAIN: reproduction controls " + ("all pass -> exit 0" if checks.all_ok() else "FAILED -> exit 1 (kept)"))
    out_json(script_file, results)
    sys.exit(0 if checks.all_ok() else 1)

def guarded(main):
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # never print a traceback with paths
        print("ERROR:", type(e).__name__, scrub(e))
        sys.exit(2)

# ---------------------------------------------------------------- constants, both footings
G_KPC = 4.30091727e-6            # kpc (km/s)^2 / Msun
KPC_M = 3.0856775814913673e19
C_KMS = 299792.458
C_SI = 299792458.0
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}      # a0 in m/s^2
GM_SUN = 1.32712440018e20         # m^3/s^2
AU = 1.495978707e11
Q2MAX = 5.2e-27                   # s^-2 (gate 4.01, quoted from the record)
H0_SI = 67.4e3 / 3.0856775814913673e22   # s^-1
OMEGA_M, OMEGA_L = 0.3153, 0.6847
def a0_kpc(a0_si):
    return a0_si * KPC_M / 1e6    # (km/s)^2/kpc

# ---------------------------------------------------------------- kernels in units of a0 (y_N = g_N/a0)
def gt_p2(yN):
    return np.sqrt(np.asarray(yN, float) ** 2 + np.asarray(yN, float))
def gt_simple(yN):
    yN = np.asarray(yN, float)
    return yN * (0.5 + np.sqrt(0.25 + 1.0 / yN))
_MONO = {}
def _load_mono():
    if "f" in _MONO:
        return _MONO["f"]
    r = repo_root()
    p = os.path.join(r, "campaign_fresh_gravity", "CFG44_fluid_target", "Bcommon.py") if r else None
    if p and os.path.exists(p):
        spec = importlib.util.spec_from_file_location("Bcommon_ro", p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)          # read-only import (self-contained; imports nothing from the repo)
        _MONO["f"] = m.nu_mono
    else:
        _MONO["f"] = None
    return _MONO["f"]
def gt_mono(yN):
    nu = _load_mono()
    if nu is None:
        raise RuntimeError("CFG44 Bcommon not found (nu_mono unavailable)")
    yN = np.asarray(yN, float)
    return yN * nu(yN)
TARGETS = {"P2": gt_p2, "simple": gt_simple, "nu_mono": gt_mono}

def mu_of_y(gt, y_arr):
    """mu(y_g) = y_N / y_g where g_t(y_N) = y_g (monotone target inverted by brentq)."""
    out = []
    for y in np.atleast_1d(y_arr):
        lo, hi = 1e-16, max(1.0, y) * 1.0
        f = lambda z: float(gt(z)) - y
        while f(hi) < 0:
            hi *= 2
        yN = brentq(f, lo, hi, xtol=1e-300, rtol=1e-14, maxiter=500)
        out.append(yN / y)
    return np.array(out)

def q_p2(y):
    y = np.asarray(y, float)
    return 1.0 - np.where(y > 1e-8, (np.sqrt(1 + 4 * y ** 2) - 1) / (2 * np.maximum(y, 1e-300)), y)

def mb_frac(s):
    return 1.0 - (1.0 + s + s * s / 2.0) * np.exp(-s)   # exponential sphere M_b(<r)/M, s=r/h

def rM_kpc(M, a0_si):
    return math.sqrt(G_KPC * M / a0_kpc(a0_si))
