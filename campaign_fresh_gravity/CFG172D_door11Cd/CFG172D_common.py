#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG172D_common -- shared machinery for door 11C-d (V0 / C-H/K with its region gate replaced by the flow's expansion theta).
Read-only imports from the repository (CFG44 Bcommon, CFG48 Gcommon, L352's constants, the DE12 result JSON); nothing is written
into the repository.  kappa = 1/2 is FITTED.  Units: kpc, km/s, Msun for the radial solves; SI for the DE12-style layer code.
"""
import os, sys, math, json, time, io, contextlib
import numpy as np
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    env = os.environ.get("ZF_REPO")
    if env and os.path.isdir(os.path.join(env, "campaign_fresh_gravity")):
        return os.path.abspath(env)
    d = HERE
    for _ in range(12):
        if os.path.isdir(os.path.join(d, "campaign_fresh_gravity", "CFG44_fluid_target")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("repo root not found: set ZF_REPO")


REPO = find_repo()
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG44_fluid_target"))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG48_gap1_switch"))
from Bcommon import G, A0, A0_SI, KPC_M, C_KMS, nu_p2, nu_mono, OMEGA_C_OVER_B  # noqa: E402
from Gcommon import r_ta_kpc, r_M_kpc  # noqa: E402


def rel(p):
    """print a repo path as <repo>/..."""
    p = os.path.abspath(p)
    return "<repo>/" + os.path.relpath(p, REPO) if p.startswith(REPO) else "<scratch>/" + os.path.basename(p)


# ----------------------------------------------------------------- the two footings (a0 in (km/s)^2/kpc)
A0_FOOT = {"canonical": A0, "alt": 1.1312e-10 * KPC_M / 1e6}

# ----------------------------------------------------------------- the smooth-transition gate W and derivatives (DE12's Wd)


def Wd(t):
    t = np.asarray(t, float)
    inside = (t > 0) & (t < 1)
    tt = np.where(inside, t, 0.5)
    ell = np.clip(1 / tt - 1 / (1 - tt), -700, 700)
    W = 1 / (1 + np.exp(ell))
    gq = 1 / tt ** 2 + 1 / (1 - tt) ** 2
    gp = -2 / tt ** 3 + 2 / (1 - tt) ** 3
    W1 = W * (1 - W) * gq
    W2 = W * (1 - W) * ((1 - 2 * W) * gq ** 2 + gp)
    W = np.where(t >= 1, 1.0, np.where(t <= 0, 0.0, W))
    return W, np.where(inside, W1, 0.0), np.where(inside, W2, 0.0)


# ----------------------------------------------------------------- L352's constants (read-only exec of its prefix), as DE12 does
def load_l352():
    P52 = os.path.join(REPO, "real_research", "g03_audit_2026", "L352_switch_gauss_compensation.py")
    L52 = {"__name__": "l352", "__file__": P52}
    s = open(P52).read().split('banner("Z1')[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(s, "l352_prefix", "exec"), L52)
    return L52


L52 = load_l352()
G_SI, H0, Om, OL, rho_crit0, A0_L = [L52[k] for k in ("G", "H0", "Om", "OL", "rho_crit0", "A0")]
LYG, YG, HM, DH = [L52[k] for k in ("LYG", "YG", "HM", "DH")]
MS = 1.98892e30
KPC = L52["Mpc"] / 1e3
CLIGHT = L52["c"]
KB, MP = 1.380649e-23, 1.67262e-27
FB = 0.02237 / (0.02237 + 0.1200)
hh = 0.6736
E2 = lambda z: 0.3138 * (1 + z) ** 3 + 0.6862                       # L359's gate background (the record's x_c,eff = x_c0 E^(2p))
Hz = lambda z: H0 * math.sqrt(Om * (1 + z) ** 3 + OL)
h_of = lambda y: np.interp(np.log10(y), LYG, HM)
dh_of = lambda y: np.interp(np.log10(y), LYG, DH)
QG = 2.0 * ((2.0 / 3.0) * YG[0] ** 1.5 + np.concatenate([[0.0], np.cumsum(0.5 * (HM[1:] + HM[:-1]) * np.diff(YG))]))
q_of = lambda y: np.interp(np.log10(y), LYG, QG)                    # q(y^2) = 2 int_0^y h
nu_of = lambda y: 1.0 + h_of(y) / y
ynup_of = lambda y: dh_of(y) - h_of(y) / y
CS = {"1e5K": math.sqrt(KB * 1e5 / (0.6 * MP)), "1e6K": math.sqrt(KB * 1e6 / (0.6 * MP)), "cold10": 10e3}   # m/s
V_CAP = 325e3
Lam = 3 * OL * H0 ** 2 / CLIGHT ** 2                                 # Lambda (1/m^2)
THETA_L = math.sqrt(3 * Lam)                                         # theta_Lambda (1/m)
RHO_L = OL * rho_crit0                                               # rho_Lambda (kg/m^3)


def theta_bar(z):
    return 3 * Hz(z) / CLIGHT


# ----------------------------------------------------------------- the DE12 host (NFW) and gas (re-implemented copy of DE12's host())
def host(Mb, z):
    M200 = Mb / (0.3 * FB) if Mb < 1e13 else Mb / FB
    rhoc = rho_crit0 * E2(z) * (Hz(z) / (H0 * math.sqrt(E2(z)))) ** 2
    c = 10 ** (0.905 - 0.101 * math.log10(M200 / (1e12 / hh))) * (1 + z) ** -0.5
    r200 = (3 * M200 * MS / (4 * math.pi * 200 * rhoc)) ** (1 / 3); rs = r200 / c
    rho_s = M200 * MS / (4 * math.pi * rs ** 3 * (math.log(1 + c) - c / (1 + c)))
    return dict(M200=M200, r200=r200, rs=rs, rho_s=rho_s)


# ----------------------------------------------------------------- the gate variable of 11C-d
def u_theta(theta, z, p=1, zscale=True):
    """u_theta = D(theta) * E(z)^(-2p), D = (thetabar/theta)^2 - 1  (declared, criteria 1.1)."""
    tb = theta_bar(z)
    D = (tb / theta) ** 2 - 1.0
    return D * (E2(z) ** (-p) if zscale else 1.0)


def t_of_u(u, w, xc0=2.5):
    return (u / xc0 - 1.0) / (2 * w) + 0.5


def theta_at_edge(z, xc0=2.5, p=1, zscale=True):
    """theta/thetabar at t = 1/2 (u = xc0)"""
    D = xc0 * (E2(z) ** p if zscale else 1.0)
    return 1.0 / math.sqrt(1.0 + D)


# ----------------------------------------------------------------- Report helper
class Report:
    def __init__(self, slug, mutate=None):
        self.slug = slug + (f"_MUTATE_{mutate}" if mutate else "")
        self.mutate = mutate
        self.lines, self.checks, self.numbers, self.verdicts, self.t0 = [], [], {}, {}, time.time()

    def P(self, s=""):
        print(s, flush=True); self.lines.append(str(s))

    def banner(self, s):
        self.P("\n" + "=" * 110 + "\n" + s + "\n" + "=" * 110)

    def check(self, name, detail, ok, load_bearing=True):
        self.checks.append(dict(name=name, detail=str(detail), ok=bool(ok), load_bearing=load_bearing))
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")
        return bool(ok)

    def verdict(self, key, status, why):
        self.verdicts[key] = dict(status=status, why=why)
        self.P(f"  >> {key}: {status} -- {why}")

    def num(self, k, v):
        self.numbers[k] = v

    def write(self, outdir=HERE):
        def clean(o):
            if isinstance(o, dict):
                return {str(k): clean(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [clean(v) for v in o]
            if isinstance(o, (np.floating, float)):
                return float(o) if np.isfinite(o) else str(o)
            if isinstance(o, np.integer):
                return int(o)
            if isinstance(o, (np.bool_, bool)):
                return bool(o)
            return o
        lb = [c for c in self.checks if c["load_bearing"]]
        nf = sum(not c["ok"] for c in lb)
        self.P(f"\n  {sum(c['ok'] for c in self.checks)}/{len(self.checks)} checks pass; load-bearing failures: {nf}   ({time.time() - self.t0:.0f} s)")
        with open(os.path.join(outdir, self.slug + "_results.json"), "w") as f:
            json.dump(clean(dict(slug=self.slug, mutate=self.mutate, checks=self.checks, numbers=self.numbers,
                                 verdicts=self.verdicts)), f, indent=1)
        with open(os.path.join(outdir, self.slug + ".out"), "w") as f:
            f.write("\n".join(self.lines) + "\n")
        return nf
