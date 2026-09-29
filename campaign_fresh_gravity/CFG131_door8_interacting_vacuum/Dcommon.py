# -*- coding: utf-8 -*-
"""Shared helpers for CFG131 (Door 8). Self-contained: nothing is imported from the repository.
Units where stated. kappa = 1/2 is FITTED (never derived); canonical a0 = 9.3603e-11 m/s^2.
MUTATE env var: 0 (default) or 1/2/3 as defined in FROZEN_QUESTION.md. Every script writes <name>[_MUTATEk].out next to itself and exits 1 if a load-bearing check failed."""
import os, sys, math, hashlib
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = int(os.environ.get("MUTATE", "0"))

G_KPC = 4.30091727e-6                 # kpc (km/s)^2 / Msun
KPC_M = 3.0856775814913673e19
A0_SI = 9.3603e-11
A0 = A0_SI * KPC_M / 1e6              # (km/s)^2/kpc  = 2888.3
C_KMS = 299792.458


def frozen_hash():
    return hashlib.sha256(open(os.path.join(HERE, "FROZEN_QUESTION.md"), "rb").read()).hexdigest()


class Run:
    def __init__(self, name):
        self.name = name
        tag = "" if MUTATE == 0 else "_MUTATE%d" % MUTATE
        self.path = os.path.join(HERE, name + tag + ".out")
        self._f = open(self.path, "w", encoding="utf-8")
        self.results = []
        self.fail_lb = 0
        self.P("FROZEN_QUESTION.md sha256 = " + frozen_hash())
        self.P("MUTATE = %d" % MUTATE)

    def P(self, *a):
        s = " ".join(str(x) for x in a)
        print(s)
        self._f.write(s + "\n")
        self._f.flush()

    def banner(self, t):
        self.P("")
        self.P("=" * 110)
        self.P(t)
        self.P("=" * 110)

    def check(self, tag, statement, measured, ok, reading="", load_bearing=True):
        ok = bool(ok)
        self.results.append((tag, ok, load_bearing))
        if (not ok) and load_bearing:
            self.fail_lb += 1
        st = "PASS" if ok else ("FAIL" if load_bearing else "FAIL(reported)")
        self.P("  [%s] %s %s" % (st, tag, statement))
        self.P("         measured: " + str(measured))
        if reading:
            self.P("         reading:  " + reading)

    def finish(self):
        n = len(self.results)
        npass = sum(1 for r in self.results if r[1])
        self.P("")
        self.P("SUMMARY %s (MUTATE=%d): %d/%d checks pass; load-bearing failures = %d" % (self.name, MUTATE, npass, n, self.fail_lb))
        for tag, ok, lb in self.results:
            if not ok:
                self.P("   failed: %s %s" % (tag, "(load-bearing)" if lb else "(reported)"))
        self._f.close()
        sys.exit(1 if self.fail_lb else 0)


# ------------------------------------------------------------------------------------------------ cosmology shared by D2, D3, D4
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

H0_KMS = 67.4                                   # km/s/Mpc  [declared input, as CFG43]
OC, OB, OL, OR = 0.265, 0.050, 0.685, 9.1e-5     # CFG43's declared inputs (Omega_c = the harness's 0.265)
OM = OC + OB


def E2_lcdm(a):
    return OM / a ** 3 + OR / a ** 4 + OL


def background(xi, a_i=1e-3, a_end=1.0, Qform="lambda_only", n_exp=0.0):
    """Units: M_P^2 = 1/(8 pi G) = 1, H0_ref = 1 (rho_crit,ref = 3).  Flat FRW, 3 H^2 = rho_c + rho_b + rho_r + rho_L.
    Q = xi H_L rho_L with H_L = sqrt(rho_L/3) (a function of Lambda ONLY, Q_rho = 0), Qform='lambda_only';
    rho_c' = -3 rho_c + Q/H, rho_L' = -Q/H (prime = d/dln a).  Initial data: rho_c(a_i) a_i^3, rho_b, rho_r equal to the LCDM reference; rho_L(a_i) SHOT so that
    rho_L(a = 1) = 3 OL (the observed a0 anchor: a0(0) fixed).  Returns dict with callables of ln a."""
    rb0, rr0 = 3 * OB, 3 * OR

    def rhs(la, y):
        rc, rl = y
        a = math.exp(la)
        rl_ = max(rl, 1e-300)
        H = math.sqrt((rc + rb0 / a ** 3 + rr0 / a ** 4 + rl_) / 3.0)
        Q = xi * math.sqrt(rl_ / 3.0) * rl_
        return [-3 * rc + Q / H, -Q / H]

    def run(rl_i, dense=False):
        return solve_ivp(rhs, [math.log(a_i), math.log(a_end)], [3 * OC / a_i ** 3, rl_i], method="DOP853", rtol=1e-11, atol=1e-14, dense_output=dense)

    f = lambda rl_i: run(rl_i).y[1, -1] - 3 * OL
    rl_i = brentq(f, 3 * OL * 0.2, 3 * OL * 5.0, xtol=1e-14, rtol=1e-13)
    sol = run(rl_i, dense=True)
    return dict(sol=sol, rl_i=rl_i, xi=xi, a_i=a_i, rb0=rb0, rr0=rr0)


def bg_state(bg, a):
    rc, rl = bg["sol"].sol(math.log(a))
    H = math.sqrt((rc + bg["rb0"] / a ** 3 + bg["rr0"] / a ** 4 + rl) / 3.0)
    return rc, rl, H


def growth_ratio(k_mpc, cs2_of_a, bg=None, zi=1000.0, a_end=1.0, gamma_on=True):
    """Two-fluid sub-horizon linear growth in CFG43's conventions (cold fluid + pressureless baryons, start delta = a at z_i, total-matter delta at a_end).
    Equations (derived in D3, sympy-checked; ' = d/dln a; gamma = (Q/rho_c)(1-n), n = rho_c Q_rho/Q):
        d_c'' + (2 + dlnH/dlna + gamma/H) d_c' = (3/2)(Om_c d_c + Om_b d_b) - [c_s^2 k^2/(aH)^2 + 2 gamma/H + (dgamma/dlna)/H] d_c
        d_b'' + (2 + dlnH/dlna) d_b' = (3/2)(Om_c d_c + Om_b d_b)
    bg=None: the LCDM background of CFG43 (E^2 = Om/a^3 + Or/a^4 + OL) and gamma = 0.  Returns (Oc d_c + Ob d_b)/Om-like weighted total at a_end (weights = Om_c, Om_b at that time)."""
    a_i = 1.0 / (1 + zi)
    ckh = C_KMS / H0_KMS                            # c/H0 in Mpc

    def state(la):
        a = math.exp(la)
        if bg is None:
            e2 = E2_lcdm(a)
            dlnH = -(3 * OM / a ** 3 + 4 * OR / a ** 4) / (2 * e2)
            return a, math.sqrt(e2), dlnH, OC / a ** 3 / e2, OB / a ** 3 / e2, 0.0, 0.0
        rc, rl, H = bg_state(bg, a)
        h = 1e-4
        _, _, Hp = bg_state(bg, a * math.exp(h)); _, _, Hm = bg_state(bg, a * math.exp(-h))
        dlnH = (math.log(Hp) - math.log(Hm)) / (2 * h)
        Q = bg["xi"] * math.sqrt(rl / 3.0) * rl
        gam = Q / rc if gamma_on else 0.0                # n = 0 (Q_rho = 0): gamma = Gamma
        # d gamma/dlna numerically
        def gam_at(la_):
            aa = math.exp(la_); rc_, rl_, H_ = bg_state(bg, aa); return bg["xi"] * math.sqrt(rl_ / 3.0) * rl_ / rc_
        dgam = (gam_at(la + h) - gam_at(la - h)) / (2 * h) if gamma_on else 0.0
        return a, H, dlnH, rc / (3 * H ** 2), (bg["rb0"] / a ** 3) / (3 * H ** 2), gam, dgam

    def rhs(la, y):
        a, H, dlnH, Omc, Omb, gam, dgam = state(la)
        dc, dcp, db, dbp = y
        src = 1.5 * (Omc * dc + Omb * db)
        pr = cs2_of_a(a) * (k_mpc * ckh / (a * H)) ** 2
        return [dcp, -(2 + dlnH + gam / H) * dcp + src - (pr + 2 * gam / H + dgam / H) * dc, dbp, -(2 + dlnH) * dbp + src]

    s = solve_ivp(rhs, [math.log(a_i), math.log(a_end)], [a_i, a_i, a_i, a_i], rtol=1e-9, atol=1e-14, method="LSODA")
    dc, _, db, _ = s.y[:, -1]
    a, H, dlnH, Omc, Omb, gam, dgam = state(math.log(a_end))
    return (Omc * dc + Omb * db) / (Omc + Omb)
