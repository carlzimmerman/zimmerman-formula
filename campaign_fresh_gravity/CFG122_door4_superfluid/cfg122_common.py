#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg122_common -- shared machinery for CFG122 (door 4, superfluid dark matter, Berezhiani-Khoury type EFT).
Frozen criteria: campaign_fresh_gravity/CFG122_FROZEN_CRITERIA.md (commit e8b9fbcdf).  Nothing in the repository is edited; the repo is only READ.
Repo root: env ZF_REPO, else searched upward from this file / the cwd.  Outputs are written next to this file.

Natural units hbar = c = 1, everything in eV.  kappa = 1/2 is FITTED (it only enters through the two a0 footings).
Model (static, spherical, NR):   X = mu - m Phi - p^2/(2m),  p = phi'(r);   P(X) = (2 Lam (2m)^(3/2)/3) X sqrt|X|;
   n = P'(X) = Lam (2m)^(3/2) sqrt|X|,  rho_DM = m n;   phonon flux law (Gauss, exact):  (2m)^(3/2) sqrt|X| p = m alpha M_b(<r)/(4 pi r^2 M_Pl)
   [NOTE: the frozen file's 'n phi' = m alpha M_b/(4 pi r^2 M_Pl)' omits a factor Lam on the right; the equation above (Lam cancelled) is the one
    the frozen file's own derivation gives and is what is used.  Disclosed as a typo in the frozen text, not a change of a criterion.]
   Y(r) := mu - m Phi(r);  Y = X + D/|X|,  D = C^2/(16 m^4),  C = m alpha M_b(<r)/(4 pi r^2 M_Pl)  (algebraic in X for given Y, r)
   force on baryons  a_phi = alpha (Lam/M_Pl) p;  tie  a0 = N_a alpha^3 Lam^2 / M_Pl  with N_a = 1 (derived in S0.1).
"""
import os, sys, math, json, time
import numpy as np
from scipy.special import gammainc
from scipy.optimize import brentq

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    cands = []
    if os.environ.get("ZF_REPO"):
        cands.append(os.environ["ZF_REPO"])
    for start in (HERE, os.getcwd()):
        p = os.path.abspath(start)
        for _ in range(8):
            cands.append(p)
            p = os.path.dirname(p)
    for c in cands:
        if os.path.isdir(os.path.join(c, "campaign_fresh_gravity")) and os.path.isdir(os.path.join(c, "real_research")):
            return c
    return None


REPO = find_repo()

# ------------------------------------------------------------------ constants (natural units, eV)
HBARC_EV_M = 1.973269804e-7
HBAR_EV_S = 6.582119569e-16
C_SI = 299792458.0
MPL = 2.435323e27                      # reduced Planck mass [eV]
G_N = 1.0 / (8.0 * math.pi * MPL ** 2)  # eV^-2
MSUN_EV = 1.98892e30 * C_SI ** 2 / 1.602176634e-19
KPC_EV = 3.0856775814913673e19 / HBARC_EV_M     # kpc in eV^-1
AU_EV = 1.495978707e11 / HBARC_EV_M
GYR_EV = 3.15576e16 / HBAR_EV_S                  # Gyr in eV^-1
ZETA32, ZETA52 = 2.6123753486854883, 1.3414872572509171
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
H0_SI = 67.4e3 / 3.0856775814913673e22           # 1/s   (h = 0.674, as the repo's LCDM lanes)
H0_EV = H0_SI * HBAR_EV_S
RHOCRIT0_EV4 = 3 * H0_EV ** 2 * MPL ** 2         # critical density today, eV^4
OMEGA_C_H2, OMEGA_B_H2, H_LITTLE = 0.1200, 0.02237, 0.674
OMEGA_C, OMEGA_B = OMEGA_C_H2 / H_LITTLE ** 2, OMEGA_B_H2 / H_LITTLE ** 2
OMEGA_M = OMEGA_C + OMEGA_B
FOOTINGS = ("canonical", "alt")


def a0_nat(foot):
    return A0_SI[foot] * HBAR_EV_S / C_SI


def lam_tie(m, alpha, a0n):
    """Lambda from the door's stated a0 tie a0 = alpha^3 Lam^2 / M_Pl (N_a = 1)."""
    return np.sqrt(a0n * MPL / np.asarray(alpha, float) ** 3)


def rM(M, a0n):
    return np.sqrt(G_N * M / a0n)


def Vf2(M, a0n):
    return np.sqrt(G_N * M * a0n)          # V_f^2 (c = 1)


def n_crit(m, sig2):
    """critical number density n_c = zeta(3/2) (m T / 2 pi)^(3/2), T = m sigma^2 (the declared convention), hbar = k_B = 1."""
    T = m * sig2
    return ZETA32 * (m * T / (2 * math.pi)) ** 1.5


# ------------------------------------------------------------------ the plane
def plane(n=60, m_lo=-3, m_hi=3, a_lo=-2, a_hi=2):
    mg = 10 ** np.linspace(m_lo, m_hi, n)      # eV
    ag = 10 ** np.linspace(a_lo, a_hi, n)
    Mm, Aa = np.meshgrid(mg, ag, indexing="ij")
    return mg, ag, Mm, Aa


MASSES = (1e9, 1e10, 1e11, 1e12)     # Msun (baryons)


# ------------------------------------------------------------------ baryon profiles (enclosed mass in eV)
class Prof:
    def __init__(self, kind, M_msun, hfac=None, shell=None):
        self.kind, self.M = kind, M_msun * MSUN_EV
        self.hfac, self.shell = hfac, shell          # shell = (R_eV, m_sh_eV) step outside
        self.Msun = M_msun

    def h(self, a0n):
        return self.hfac * rM(self.M, a0n)

    def Mb(self, r, a0n):
        r = np.asarray(r, float)
        if self.kind == "point":
            out = self.M * np.ones_like(r)
        else:
            out = self.M * gammainc(3.0, r / self.h(a0n))
        if self.shell is not None:
            R, msh = self.shell
            out = out + msh * (r > R)
        return out


# ------------------------------------------------------------------ the static solver
BRANCHES = ("B-", "B+hi", "B+lo")


def solveX(Y, D, branch):
    """X from Y = X + D/|X|.  B-: X<0 root.  B+hi / B+lo: the two X>0 roots (exist only for Y>0, Y^2>=4D); nan where absent."""
    with np.errstate(invalid="ignore", divide="ignore", over="ignore"):
        if branch == "B-":
            a = np.where(Y >= 0, 2 * D / (Y + np.sqrt(Y * Y + 4 * D)), (-Y + np.sqrt(Y * Y + 4 * D)) / 2)
            return -a
        disc = Y * Y - 4 * D
        ok = (Y > 0) & (disc >= 0)
        s = np.sqrt(np.where(ok, disc, np.nan))
        if branch == "B+hi":
            return np.where(ok, (Y + s) / 2, np.nan)
        if branch == "B+lo":
            return np.where(ok, 2 * D / (Y + s), np.nan)
    raise ValueError(branch)


def integrate(m, alpha, Lam, prof, r_lo, r_hi, N, Y0, branch, a0n, alpha_c=None, M0=0.0):
    """Integrate outward in s = ln r from r_lo to r_hi (N RK4 steps) the system
         dY/ds = -m G (M_b + M_DM)/r ,   dM_DM/ds = 4 pi r^3 rho_DM ,   rho_DM = m Lam (2m)^1.5 sqrt|X(Y, D(r))|.
       m, alpha, Lam, Y0 are broadcast arrays (any common shape).  alpha_c: the coupling actually used in flux law and force (MUTATE c)
       (default alpha).  Returns dict of arrays with leading axis i = 0..N (grid r_i)."""
    m, alpha, Lam, Y0 = np.broadcast_arrays(np.asarray(m, float), np.asarray(alpha, float), np.asarray(Lam, float), np.asarray(Y0, float))
    ac = alpha if alpha_c is None else np.asarray(alpha_c, float) * np.ones_like(alpha)
    ds = math.log(r_hi / r_lo) / N
    rfull = r_lo * np.exp(0.5 * ds * np.arange(2 * N + 1))
    Mbf = prof.Mb(rfull, a0n)
    pref_rho = m * Lam * (2 * m) ** 1.5
    pref_C = m * ac / (4 * math.pi * MPL)

    def eval_(k, Y, MD):
        r = rfull[k]
        C = pref_C * Mbf[k] / r ** 2
        D = C * C / (16 * m ** 4)
        X = solveX(Y, D, branch)
        aX = np.abs(X)
        rho = pref_rho * np.sqrt(aX)
        dY = -m * G_N * (Mbf[k] + MD) / r
        dM = 4 * math.pi * r ** 3 * rho
        return X, C, rho, dY, dM

    shp = (N + 1,) + Y0.shape
    out = {k: np.full(shp, np.nan) for k in ("X", "rho", "p", "MD", "Y")}
    Y = Y0.copy()
    MD = np.full(Y0.shape, float(M0))
    for i in range(N + 1):
        k = 2 * i
        X, C, rho, dY, dM = eval_(k, Y, MD)
        out["X"][i], out["rho"][i], out["MD"][i], out["Y"][i] = X, rho, MD, Y
        with np.errstate(invalid="ignore", divide="ignore"):
            out["p"][i] = C / ((2 * m) ** 1.5 * np.sqrt(np.abs(X)))
        if i == N:
            break
        k1y, k1m = dY, dM
        X2, _, _, k2y, k2m = eval_(k + 1, Y + 0.5 * ds * k1y, MD + 0.5 * ds * k1m)
        X3, _, _, k3y, k3m = eval_(k + 1, Y + 0.5 * ds * k2y, MD + 0.5 * ds * k2m)
        X4, _, _, k4y, k4m = eval_(k + 2, Y + ds * k3y, MD + ds * k3m)
        Y = Y + ds / 6 * (k1y + 2 * k2y + 2 * k3y + k4y)
        MD = MD + ds / 6 * (k1m + 2 * k2m + 2 * k3m + k4m)
    out["r"] = r_lo * np.exp(ds * np.arange(N + 1))
    out["Mb"] = Mbf[::2]
    out["a_phi"] = alpha_force(out["p"], ac, Lam)
    return out


def alpha_force(p, ac, Lam):
    return ac * Lam / MPL * p


def target_rho(Mb, r, a0n):
    gN = G_N * Mb / r ** 2
    gtot = np.sqrt(gN ** 2 + a0n * gN)
    return a0n * Mb / (4 * math.pi * r ** 3 * gtot)


def g_law(Mb, r, a0n):
    gN = G_N * Mb / r ** 2
    return np.sqrt(gN ** 2 + a0n * gN)


def Y0_grid(m, prof, a0n, ks=None):
    """Y(r_lo) trial values: 0 and +-10^k * (m G M / r_M) (k = -6..6 step 1) -- the per-halo integration constant mu."""
    if ks is None:
        ks = np.arange(-6, 7)
    base = m * G_N * prof.M / rM(prof.M, a0n)
    return base, np.concatenate([[0.0], 10.0 ** ks, -(10.0 ** ks)])


# ------------------------------------------------------------------ the imported LCDM halo (values as the repo's LCDM lanes: CFG73/CFG84 specification)
NA_M, LM1_M, BE_M, GA_M = 0.0351, 11.590, 1.376, 0.608
RHO_C_MSUN_MPC3 = 3 * (67.4e3 / 3.0856775814913673e22) ** 2 / (8 * math.pi * 6.674e-11) / 1.989e30 * (3.0857e22) ** 3


def moster_mstar(Mh):
    x = np.asarray(Mh, float) / 10 ** LM1_M
    return np.asarray(Mh, float) * 2 * NA_M / (x ** (-BE_M) + x ** GA_M)


def halo_mass(Mstar):
    f = lambda lm: math.log10(float(moster_mstar(10 ** lm))) - math.log10(Mstar)
    return 10 ** brentq(f, 9.0, 17.0, xtol=1e-13)


def c_duffy_full(Mh):
    return 5.71 * (Mh / (2e12 / H_LITTLE)) ** (-0.084)


def mfun(t):
    return math.log1p(t) - t / (1 + t)


class NFW:
    """NFW halo of the Moster+2013 mass of stellar mass M_* (= M_b, declared), Duffy+2008 full-200c concentration; all in eV / eV^-1."""

    def __init__(self, Mstar_msun):
        self.Mh_msun = halo_mass(Mstar_msun)
        Mh = self.Mh_msun
        self.c = float(c_duffy_full(Mh))
        R200_kpc = (3 * Mh / (4 * math.pi * 200 * RHO_C_MSUN_MPC3)) ** (1 / 3.0) * 1000.0
        self.R200 = R200_kpc * KPC_EV
        self.rs = self.R200 / self.c
        self.Mh = Mh * MSUN_EV
        self.rho_s = self.Mh / (4 * math.pi * self.rs ** 3 * mfun(self.c))

    def rho(self, r):
        t = np.asarray(r, float) / self.rs
        return self.rho_s / (t * (1 + t) ** 2)

    def M(self, r):
        t = np.asarray(r, float) / self.rs
        return 4 * math.pi * self.rho_s * self.rs ** 3 * (np.log1p(t) - t / (1 + t))

    def Phi(self, r):
        t = np.asarray(r, float) / self.rs
        return -4 * math.pi * G_N * self.rho_s * self.rs ** 3 * np.log1p(t) / np.asarray(r, float)

    def r_of_rho(self, rho_target, rmin=1e-4, capped_at=None):
        """radius where rho_NFW = rho_target; returns (r, flag) with flag 'ok' | 'beyond R200 (capped)' | 'none'."""
        lo, hi = rmin * self.rs, self.R200
        if self.rho(hi) >= rho_target:
            return hi, "capped_R200"
        if self.rho(lo) <= rho_target:
            return 0.0, "none"
        return math.exp(brentq(lambda lr: math.log(self.rho(math.exp(lr))) - math.log(rho_target), math.log(lo), math.log(hi), xtol=1e-12)), "ok"


# ------------------------------------------------------------------ report helper (same conventions as CFG70/72: PASS/FAIL checks + gate verdict lines + JSON)
class Report:
    def __init__(self, slug):
        mut = os.environ.get("MUTATE", "")
        self.mut = mut
        self.slug = slug + (("_MUTATE_" + mut) if mut else "")
        self.lines, self.checks, self.numbers, self.verdicts, self.t0 = [], [], {}, {}, time.time()

    def P(self, s=""):
        print(s, flush=True)
        self.lines.append(str(s))

    def banner(self, s):
        self.P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)

    def check(self, name, detail, ok, load_bearing=True):
        self.checks.append(dict(name=name, detail=str(detail), ok=bool(ok), load_bearing=load_bearing))
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")

    def verdict(self, gate, status, why):
        self.verdicts[gate] = dict(status=status, why=why)
        self.P(f"  >> {gate}: {status} -- {why}")

    def num(self, k, v):
        self.numbers[k] = v

    def write(self):
        nf = sum((not c["ok"]) for c in self.checks if c["load_bearing"])
        self.P(f"\n  {sum(c['ok'] for c in self.checks)}/{len(self.checks)} checks pass; load-bearing check failures: {nf}   ({time.time() - self.t0:.0f} s)")
        gate_fail = sum(1 for v in self.verdicts.values() if v["status"] == "FAIL")
        self.P(f"  gate verdicts: " + ", ".join(f"{k}={v['status']}" for k, v in self.verdicts.items()))

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
            if isinstance(o, np.ndarray):
                return clean(o.tolist())
            return o if isinstance(o, (int, str)) or o is None else str(o)

        json.dump(clean(dict(slug=self.slug, mutate=self.mut, check_failures=nf, gate_fail=gate_fail, checks=self.checks, verdicts=self.verdicts, numbers=self.numbers)),
                  open(os.path.join(HERE, self.slug + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")
        return nf, gate_fail
