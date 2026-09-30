#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG232_common -- shared machinery for door 13 (BIMOND).  Nothing in the repository is edited; CFG44's Bcommon.py and CFG48's Gcommon.py
are imported read-only.  Repo root: ZF_REPO, else walk up from __file__ to the directory holding campaign_fresh_gravity/.  Every printed
path is <repo>/...; no absolute home path is printed or stored.

Conventions (frozen in CFG232_FROZEN_CRITERIA.md):
  * static weak-field Lagrangian per 1/8piG, c = 1, with the interaction sign sigma_s DEFINED BY THE STATIC LAGRANGIAN (the frozen file's
    action-level sign differs by a sign, sigma_action = -sigma_s; disclosed in README as an erratum; both signs are scored either way)
        L = beta(|dPsi|^2 - 2 dPhi.dPsi) + gamma(|dPsih|^2 - 2 dPhih.dPsih) + sigma_s a0^2 M(Q) - 8 pi G rho Phi ,
        Q = 4(|d dPhi|^2 + 2|d dPsi|^2)/a0^2   (the T4-T1 static value, re-derived in A1)
  * accelerations in units of a0 unless stated.
"""
import os, sys, json, math, time, importlib.util, io
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
    raise SystemExit("CFG232: set ZF_REPO to the repository root (walk-up from __file__ found none)")


REPO = find_repo()


def scrub(s):
    """no absolute path ever reaches an output file"""
    return str(s).replace(REPO, "<repo>").replace(os.path.expanduser("~"), "~")


def _load(name, relpath):
    p = os.path.join(REPO, relpath)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


B = _load("Bcommon", "campaign_fresh_gravity/CFG44_fluid_target/Bcommon.py")
G, A0_KPC, A0_SI_CAN = B.G, B.A0, B.A0_SI
A0_SI_ALT = 1.1312e-10
FOOTS = {"canonical": A0_SI_CAN, "alt": A0_SI_ALT}
KPC_M, C_KMS = B.KPC_M, B.C_KMS
nu_p2, nu_mono = B.nu_p2, B.nu_mono
KERNELS = {"P2": nu_p2, "nu_mono": nu_mono}
OMEGA_C_OVER_B = B.OMEGA_C_OVER_B


def nu_simple(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


KERNELS_ALL = {"P2": nu_p2, "nu_mono": nu_mono, "simple": nu_simple}


def a0_kpc(foot):
    return FOOTS[foot] * KPC_M / 1e6


def load_gcommon():
    return _load("Gcommon", "campaign_fresh_gravity/CFG48_gap1_switch/Gcommon.py")


class Run:
    """tee to a mode-named .out and .json (nothing is overwritten across modes); exit convention in finish()."""

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
        """kind: 'control' = a reproduction/identity check (failure => exit 1); 'result' = a gate verdict item (F/P are results)."""
        ok = bool(ok)
        self.checks.append(dict(name=name, ok=ok, detail=scrub(detail), kind=kind))
        self.P(f"  [{'PASS' if ok else 'FAIL'}] ({kind}) {name}" + (f"   ({scrub(detail)})" if detail else ""))
        return ok

    def num(self, k, v):
        self.nums[k] = v

    def verdict(self, gate, status, why):
        self.nums.setdefault("verdicts", {})[gate] = dict(status=status, why=scrub(why))
        self.P(f"  >>> VERDICT {gate}: {status} -- {scrub(why)}")

    def finish(self, bite_claims=None):
        """main: exit 0 unless a control failed.  MUTATE: exit 1 iff every bite_claims item FAILED as required (the control bites);
        a non-biting MUTATE is a declared control failure (exit 0)."""
        ctrl_fail = [c for c in self.checks if c["kind"] == "control" and not c["ok"]]
        out = dict(slug=self.tag, mutate=self.mutate, runtime_s=round(time.time() - self.t0, 2),
                   checks=self.checks, numbers=self.nums)
        if self.mutate:
            bit = bool(bite_claims) and all(bite_claims)
            out["control_bites"] = bit
            self.P(f"\nMUTATE {self.mutate}: control {'BITES (exit 1)' if bit else 'DOES NOT BITE (declared control failure, exit 0)'}")
            code = 1 if bit else 0
        else:
            self.P(f"\nRESULT: {len(self.checks)} checks, {len(ctrl_fail)} control failure(s): "
                   + ("; ".join(c['name'] for c in ctrl_fail) if ctrl_fail else "none"))
            code = 1 if ctrl_fail else 0
        with open(os.path.join(HERE, f"{self.tag}.out"), "w") as f:
            f.write("\n".join(self.lines) + "\n")

        def clean(o):
            if isinstance(o, dict):
                return {str(k): clean(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [clean(v) for v in o]
            if isinstance(o, (np.floating, np.integer)):
                return o.item()
            if isinstance(o, np.ndarray):
                return clean(o.tolist())
            if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
                return str(o)
            return o
        with open(os.path.join(HERE, f"{self.tag}.json"), "w") as f:
            json.dump(clean(out), f, indent=1)
        sys.exit(code)


# ------------------------------------------------------------------------------------------------ the reduced BIMOND static system
def xq_design(k):
    """positive and negative roots of 32(k+1)x^2 + (4k+12)x - k = 0 (hand H4; re-derived symbolically in A1)."""
    k = np.asarray(k, float)
    disc = np.sqrt((4 * k + 12) ** 2 + 128 * k * (k + 1))
    return (-(4 * k + 12) + disc) / (64 * (k + 1)), (-(4 * k + 12) - disc) / (64 * (k + 1))


def Dfun(x):
    return 1.0 - 4.0 * x - 32.0 * x * x


class Design:
    """M'(Q) designed by inversion of a target nu(y) for (beta, gamma, sigma_s).  Q in units where the argument is 4(dPhi'^2+2dPsi'^2)/a0^2
    with all accelerations in units of a0.  branch 'A': x>0 root (sigma_s=+1); 'B': x<0 root (sigma_s=-1)."""

    def __init__(self, nu, beta=1.0, gamma=1.0, sigma=+1, ny=4001, ylo=1e-8, yhi=1e8):
        self.beta, self.gamma, self.sigma = beta, gamma, sigma
        self.s = 1.0 / beta + 1.0 / gamma
        y = np.geomspace(ylo, yhi, ny)                      # y = g_N / a0 (source acceleration)
        self.y = y
        nuy = nu(y)
        k = (nuy - 1.0) * (1.0 + beta / gamma)
        xp, xm = xq_design(k)
        x = xp if sigma > 0 else xm
        self.x = x
        self.m = x / (sigma * self.s)
        self.D = Dfun(x)
        self.dPsi = y / (beta * self.D)                     # delta Psi' (units a0)
        self.Q = 4.0 * self.dPsi ** 2 * ((1 + 8 * x) ** 2 + 2)
        self.Phi = (y + 4 * sigma * self.m * self.dPsi * (3 + 8 * x)) / beta
        self.Psi = (y + 4 * sigma * self.m * self.dPsi * (1 + 8 * x)) / beta
        self.nu = nu
        # tables for forward use, ordered by increasing Q
        o = np.argsort(self.Q)
        self.Qs, self.ms = self.Q[o], self.m[o]

    def mfun(self, Q):
        """M'(Q) interpolated (log-log), constant m0 below the table and the tail power law above"""
        Q = np.asarray(Q, float)
        lq = np.log(np.maximum(Q, 1e-300))
        lQs = np.log(self.Qs)
        ms = np.maximum(np.abs(self.ms), 1e-300)
        val = np.exp(np.interp(lq, lQs, np.log(ms)))
        lo = Q < self.Qs[0]
        hi = Q > self.Qs[-1]
        val = np.where(lo, np.abs(self.ms[0]), val)
        # tail: extrapolate with the local slope of the last decade
        sl = (np.log(ms[-1]) - np.log(ms[-200])) / (lQs[-1] - lQs[-200])
        val = np.where(hi, ms[-1] * (Q / self.Qs[-1]) ** sl, val)
        return np.sign(self.ms[0]) * val


_XG = np.unique(np.concatenate([np.linspace(-4, 4, 160001), np.linspace(0.124, 0.126, 4001), np.linspace(-0.251, -0.249, 4001)]))


def forward(mfun, beta, gamma, sigma, gN, ghN=0.0, Qadd=0.0, pick="smallest"):
    """Solve the spherical BIMOND static system for source accelerations gN (baryons + g-coupled cold) and ghN (g-hat-coupled), in units
    of a0, given M'(Q)=mfun.  Unknown x = sigma*m*s (x-space scan, vectorised): dPsi' = S/(beta D(x)) with S = gN/beta*beta.. see below,
    Q = Qadd + 4 dPsi'^2 ((1+8x)^2+2), consistency x = sigma s M'(Q).  All roots returned; the one with smallest |dPsi'| is chosen.
    Equations (hand, re-derived symbolically in A1):  dPsi' D(x) = gN/beta - ghN/gamma ;  dPhi' = dPsi'(1+8x) ;
    Psi' = (gN + 4 sigma m dPhi')/beta ;  Phi' = Psi' + 8 sigma m dPsi'/beta ;  Phi^' = ...  Qadd = R-add background."""
    s = 1.0 / beta + 1.0 / gamma
    S = gN / beta - ghN / gamma
    x = _XG
    D = Dfun(x)
    ok = np.abs(D) > 1e-10
    xx = x[ok]
    d = S / (beta * D[ok]) if False else S / D[ok]
    d = d  # dPsi' D = S  (S already includes 1/beta: S = gN/beta - ghN/gamma)
    Q = Qadd + 4 * d * d * ((1 + 8 * xx) ** 2 + 2)
    F = xx - sigma * s * np.asarray(mfun(Q), float)
    idx = np.where((F[:-1] * F[1:] < 0) & (np.abs(xx[1:] - xx[:-1]) < 2e-3))[0]
    roots = []
    for i in idx:
        lo, hi = xx[i], xx[i + 1]
        def Ff(xv):
            dv = S / Dfun(xv)
            Qv = Qadd + 4 * dv * dv * ((1 + 8 * xv) ** 2 + 2)
            return xv - sigma * s * float(mfun(Qv))
        flo = Ff(lo)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            fm = Ff(mid)
            if flo * fm <= 0:
                hi = mid
            else:
                lo, flo = mid, fm
        xr = 0.5 * (lo + hi)
        roots.append((abs(S / Dfun(xr)), xr))
    if not roots:
        return dict(ok=False, roots=[])
    roots.sort()
    dabs, xr = roots[0]
    dPsi = S / Dfun(xr)
    m = xr / (sigma * s)
    dPhi = dPsi * (1 + 8 * xr)
    Psi = (gN + 4 * sigma * m * dPhi) / beta
    Phi = Psi + 8 * sigma * m * dPsi / beta
    return dict(ok=True, Phi=Phi, Psi=Psi, dPsi=dPsi, dPhi=dPhi, x=xr, m=m, nroots=len(roots),
                roots=[r[1] for r in roots], Q=Qadd + 4 * dPsi ** 2 * ((1 + 8 * xr) ** 2 + 2))
