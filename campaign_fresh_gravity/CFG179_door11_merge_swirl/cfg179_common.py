#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg179_common -- shared harness and constants for CFG179 (door 11: merging rivers and a swirled river).

Frozen question: FROZEN_QUESTION.md (written, hashed in FROZEN_QUESTION_SHA256.txt, before any script).
Nothing outside this directory is written.  Committed files elsewhere are only READ.

Harness: each script tees its stdout to <slug>.out (MUTATE=1 -> <slug>_MUTATE.out), records named checks with a
load-bearing flag, prints 'N/M checks pass; load-bearing failures: K', writes <slug>_results.json
(<slug>_MUTATE_results.json) and exits 1 when a load-bearing check fails.

kappa = 1/2 is FITTED.  P2 is nu(y) = sqrt(1 + 1/y) (DOOR11 Erratum 1).  Both a0 footings.
"""
import os, sys, json, math, time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"

# ------------------------------------------------------------------------------------------------ constants (SI)
C_SI = 299792458.0
G_SI = 6.67430e-11
MSUN = 1.98847e30
PC = 3.0856775814913673e16
KPC = 1e3 * PC
YR = 365.25 * 86400.0
MAS_PER_RAD = 180.0 / math.pi * 3600.0 * 1e3
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}     # CHARTER footings
FOOTS = ("canonical", "alt")
KAPPA = 0.5                                             # FITTED
Z_FRAME = math.sqrt(32.0 * math.pi / 3.0)              # 5.7888 (Z == kappa's form)
RAR_SCATTER_95 = (0.043, 0.048)                         # GATES 1.02 (95%); strict edge first
SJ_EARTH, SJ_MARS = 3.66e-14, 3.72e-14                  # Sereno-Jetzer 2 sigma monopole bounds (record's inversion)
Q2_BOUND = 5.2e-27                                      # GATES 4.01 (2 sigma), s^-2
SIGMA_TOT_DR4 = 0.028                                   # PREREGISTRATION_DR4 section-1 convention


def rho_lambda(foot):
    """rho_Lambda (kg/m^3) with H_foot = Z a0 / c (kappa = 1/2 tie)."""
    H = Z_FRAME * A0[foot] / C_SI
    return 3.0 * H * H / (8.0 * math.pi * G_SI)


# ------------------------------------------------------------------------------------------------ P2 kernel (numeric)
def nu_p2(y):
    return math.sqrt(1.0 + 1.0 / y)


def F_p2(z):
    """observed field / a0 from Newtonian field / a0:  F(z) = nu(z) z = sqrt(z^2 + z)."""
    return math.sqrt(z * z + z)


def M_p2(x):
    """inverse of F (the mu-form):  M(x) = (sqrt(1 + 4 x^2) - 1)/2."""
    return (math.sqrt(1.0 + 4.0 * x * x) - 1.0) / 2.0


def L_p2(z):
    """L = d ln nu / d ln z for P2 = -1/(2(1+z))."""
    return -1.0 / (2.0 * (1.0 + z))


def mu_fw(x):
    """the equation book's MI inertia dressing (exact inverse of P2's nu):  mu_fw(x) = (sqrt(1+4x^2)-1)/(2x)."""
    return (math.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)


def e7_root(b, e7):
    """unique positive root x of the E7 cubic x^3 + e7 x^2 - b(b+1) x - b^2 e7 = 0 (e7 = sqrt2 g_ext/a0)."""
    import numpy as np
    r = np.roots([1.0, e7, -b * (b + 1.0), -b * b * e7])
    pos = [float(v.real) for v in r if abs(v.imag) < 1e-9 * max(1.0, abs(v)) and v.real > 0]
    assert len(pos) == 1, (b, e7, r)
    return pos[0]


def qumond1d(b, e):
    """aligned 1-D merged P2 law (Chae 2020 eq. 6 construction):  x = F(b + z_e) - e, e = F(z_e)."""
    ze = M_p2(e)
    return F_p2(b + ze) - e


# ------------------------------------------------------------------------------------------------ harness
class Run:
    def __init__(self, slug):
        self.slug = slug
        self.mode = "MUTATE" if MUTATE else "main"
        suffix = "_MUTATE" if MUTATE else ""
        self.out_path = os.path.join(HERE, f"{slug}{suffix}.out")
        self.json_path = os.path.join(HERE, f"{slug}{suffix}_results.json")
        self._fh = open(self.out_path, "w")
        self.checks, self.numbers = [], {}
        self.t0 = time.time()
        self.P(f"{slug}  mode = {self.mode}  (kappa = 1/2 FITTED; P2 nu = sqrt(1 + 1/y); footings "
               f"canonical {A0['canonical']:.4e}, alt {A0['alt']:.4e} m/s^2)")

    def P(self, s=""):
        print(s, flush=True)
        self._fh.write(s + "\n")

    def banner(self, t):
        self.P("")
        self.P("=" * 110)
        self.P(t)
        self.P("=" * 110)

    def check(self, name, ok, detail="", load_bearing=True):
        ok = bool(ok)
        tag = "PASS" if ok else "FAIL"
        lb = "" if load_bearing else " (reported)"
        self.P(f"  [{tag}]{lb} {name}")
        if detail:
            self.P(f"         {detail}")
        self.checks.append(dict(name=name, ok=ok, detail=detail, load_bearing=load_bearing))
        return ok

    def num(self, key, value):
        self.numbers[key] = value
        return value

    def finish(self):
        n = len(self.checks)
        npass = sum(c["ok"] for c in self.checks)
        lbf = [c["name"] for c in self.checks if c["load_bearing"] and not c["ok"]]
        secs = time.time() - self.t0
        self.P("")
        self.P(f"{npass}/{n} checks pass; load-bearing failures: {len(lbf)}   ({secs:.1f} s, mode {self.mode})")
        for nm in lbf:
            self.P(f"   load-bearing FAIL: {nm}")
        res = dict(slug=self.slug, mode=self.mode,
                   summary=dict(n_checks=n, n_pass=npass, load_bearing_failures=len(lbf), failed=lbf, seconds=secs),
                   checks=self.checks, numbers=self.numbers)
        with open(self.json_path, "w") as f:
            json.dump(res, f, indent=1, default=float)
        self._fh.close()
        sys.exit(1 if lbf else 0)
