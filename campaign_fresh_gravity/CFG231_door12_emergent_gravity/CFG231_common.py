#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG231_common -- shared machinery for CFG231 (door 12: covariant / elastic completions of emergent gravity vs the CFG44 target).
Frozen in CFG231_FROZEN_CRITERIA.md (sha256 55e3220c...).  Nothing in the repository is edited.

Units for galaxies: kpc, km/s, Msun (G = 4.30091727e-6 kpc (km/s)^2/Msun), as CFG44's Bcommon (imported READ-ONLY for the constants and
for controls only).  kappa = 1/2 is FITTED; nothing here fits anything.

Variants (frozen names):  V0 (canonical vector), V2 (gravitating vector, K1 reference), B1 (Verlinde derivative form), B2 == K2,
B3 (B1 + onset gate), B4 (total-mass reading), K3 (simple wall), K1 (P2 inverse); KODE = the target's own ODE (positive control only).
"""
import os, sys, math, json, time
import numpy as np
from scipy.special import gammainc

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(os.path.join(r, "campaign_fresh_gravity")):
        return os.path.abspath(r)
    d = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(d, "campaign_fresh_gravity", "CFG44_fluid_target")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("CFG231: repo root not found (set ZF_REPO)")


REPO = find_repo()
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG44_fluid_target"))
import Bcommon as BC  # noqa: E402  (read-only import: constants and controls only)

G = BC.G                                  # kpc (km/s)^2 / Msun
KPC_M = BC.KPC_M
C_KMS = BC.C_KMS
A0_SI = {"canonical": 9.3603e-11, "alt": 1.131204e-10}                    # FP0 footings (CFG117's declared values)
AKPC = lambda a_si: a_si * KPC_M / 1e6                                     # m/s^2 -> (km/s)^2/kpc
H0_KMS_MPC, OMEGA_L = 67.4, 0.685                                          # CFG117's declared Planck18 values
MPC_M = 3.0856775814913673e22
C_SI = 299792458.0
H0_SI = H0_KMS_MPC * 1e3 / MPC_M
HL_SI = H0_SI * math.sqrt(OMEGA_L)


def a_V_si(which):
    """a_V = c H / 6 (m/s^2) for H = H_Lambda (primary, tied to Lambda) or H0."""
    return C_SI * (HL_SI if which == "HL" else H0_SI) / 6.0


HCHOICES = ("HL", "H0")
FOOTINGS = ("canonical", "alt")
NORMS = ("shape", "tie_canonical", "tie_alt")
MASSES = [1e9, 3e9, 1e10, 3e10, 1e11, 3e11, 1e12]
H_SPHERE = 2.0                                                             # kpc, at every mass (task spec)
NX = 3001
XGRID = np.geomspace(0.1, 30.0, NX)
XGRID[0], XGRID[-1] = 0.1, 30.0


def norm_a0(norm, a_model_si):
    """the target's a0 (SI) for a normalisation."""
    if norm == "shape":
        return a_model_si
    return A0_SI["canonical" if norm == "tie_canonical" else "alt"]


# ------------------------------------------------------------------ baryons (closed forms, own code)
class PointMass:
    kind = "point"

    def __init__(self, M):
        self.M = M

    def Mb(self, r):
        return self.M * np.ones_like(np.asarray(r, float))

    def rho(self, r):
        return np.zeros_like(np.asarray(r, float))


class ExpSphere:
    kind = "sphere"

    def __init__(self, M, h=H_SPHERE):
        self.M, self.h = M, h

    def Mb(self, r):
        return self.M * gammainc(3.0, np.asarray(r, float) / self.h)

    def rho(self, r):
        r = np.asarray(r, float)
        return self.M / (8 * math.pi * self.h ** 3) * np.exp(-r / self.h)


def gN_of(prof, r):
    r = np.asarray(r, float)
    return G * prof.Mb(r) / r ** 2


# ------------------------------------------------------------------ constitutive laws (E = psi(g_N; a))
def psi_K1(gN, a):
    return np.sqrt(gN ** 2 + a * gN) - gN


def psi_K2(gN, a):
    return np.sqrt(a * gN)


def psi_K3(gN, a):
    return 0.5 * (np.sqrt(gN ** 2 + 4 * a * gN) - gN)


PSI = {"K1": psi_K1, "K2": psi_K2, "K3": psi_K3}


def ddr(f, r, eps=1e-5):
    """central difference in r with relative step eps."""
    r = np.asarray(r, float)
    return (f(r * (1 + eps)) - f(r * (1 - eps))) / (2 * r * eps)


# ------------------------------------------------------------------ the variants: each returns dict(M_D, M_dark, rho_D, g_tot, gN)
def variant(name, prof, r, a, H_a0_gate=None):
    """a = the model's scale in (km/s)^2/kpc.  Solved from prof's M_b(<r) (and rho_b) ONLY."""
    r = np.asarray(r, float)
    gN = gN_of(prof, r)
    if name in ("K1", "K2", "K3"):
        psi = PSI[name]
        MD = lambda rr: rr ** 2 * psi(gN_of(prof, rr), a) / G
        Md = MD(r)
        rhoD = ddr(MD, r) / (4 * math.pi * r ** 2)
        return dict(M_dark=Md, rho_D=rhoD, g_tot=G * (prof.Mb(r) + Md) / r ** 2, gN=gN)
    if name == "V2":
        d = V2_dark(prof, r, a, law="K1", sign=-1.0)
        return dict(M_dark=d["M_dark"], rho_D=d["rho_D"], g_tot=d["g_tot"], gN=d["gN"])
    if name == "V0":
        # canonical vector, attractive-sign convention (see A3: attraction needs a ghost-sign kinetic term), eps = 1, Yukawa range c/H_Lambda:
        # E = g_N (1+m r) exp(-m r)  (point charge; sphere: same factor to (m r)^2, m r ~ 1e-12), so M_D = M_b to 1e-24.
        MD = lambda rr: prof.Mb(rr)
        Md = MD(r)
        rhoD = ddr(MD, r) / (4 * math.pi * r ** 2)
        return dict(M_dark=Md, rho_D=rhoD, g_tot=G * (prof.Mb(r) + Md) / r ** 2, gN=gN)
    if name in ("B1", "B2", "B3", "B1raw"):
        def MDf(rr, deriv=True):
            Mb = prof.Mb(rr)
            Mbp = 4 * math.pi * rr ** 2 * prof.rho(rr)
            arg = (a * rr ** 2 / G) * ((Mb + rr * Mbp) if deriv else Mb)
            return np.sqrt(arg)
        deriv = name != "B2"
        MDr = MDf(r, deriv)
        rho_raw = ddr(lambda rr: MDf(rr, deriv), r) / (4 * math.pi * r ** 2)
        if name == "B3":
            on = gN < 0.5 * H_a0_gate       # g_N < cH/2 = a0V/2, a0V = cH = 6 a_V
            MDr = np.where(on, MDr, 0.0)
            rho_raw = np.where(on, rho_raw, 0.0)
        return dict(M_dark=MDr, rho_D=rho_raw, g_tot=G * (prof.Mb(r) + MDr) / r ** 2, gN=gN)
    if name in ("B4", "B4d"):
        def Mtot(rr):
            Mb = prof.Mb(rr)
            Mbp = 4 * math.pi * rr ** 2 * prof.rho(rr)
            return np.sqrt((a * rr ** 2 / G) * ((Mb + rr * Mbp) if name == "B4d" else Mb))
        Mt = Mtot(r)
        Md = Mt - prof.Mb(r)
        rhoD = ddr(Mtot, r) / (4 * math.pi * r ** 2) - prof.rho(r)
        return dict(M_dark=Md, rho_D=rhoD, g_tot=G * Mt / r ** 2, gN=gN)
    raise ValueError(name)


def energy_density_scale(name):
    return None


def V2_dark(prof, r, a, law="K1", sign=-1.0):
    """gravitating vector: M_D = int 4 pi r^2 u/c^2 dr, u = sign*(1/4 pi G)(E D - int_0^E D dE'), D(E) = g_N (Gauss law).
    sign = -1 is the attractive (ghost) convention of A3; the magnitude is what G3 uses.  Returns dict like variant()."""
    r = np.asarray(r, float)
    gN = gN_of(prof, r)
    E = PSI[law](gN, a)
    intD = int_D(law, E, a)
    u = sign * (E * gN - intD) / (4 * math.pi * G)                      # Msun (km/s)^2 / kpc^3
    rho = u / C_KMS ** 2                                                # Msun/kpc^3
    # cumulative mass on the (log-spaced) grid by trapezoid in r, starting from r[0] (the mass below r[0] is O(rho r^3), neglected & stated)
    Md = np.concatenate([[0.0], np.cumsum(0.5 * (rho[1:] * r[1:] ** 2 + rho[:-1] * r[:-1] ** 2) * 4 * math.pi * np.diff(r))])
    return dict(M_dark=Md, rho_D=rho, g_tot=G * (prof.Mb(r) + Md) / r ** 2, gN=gN, u=u)


def int_D(law, E, a):
    """int_0^E D(E') dE' with D the constitutive function of the law (closed forms; checked in A1 against quad)."""
    E = np.asarray(E, float)
    if law == "K2":
        return E ** 3 / (3 * a)
    if law == "K1":       # D = E^2/(a - 2E)
        return -E ** 2 / 4 - a * E / 4 - (a ** 2 / 8) * np.log1p(-2 * E / a)
    if law == "K3":       # D = E^2/(a - E) = -E - a + a^2/(a - E)
        return -E ** 2 / 2 - a * E - a ** 2 * np.log1p(-E / a)
    raise ValueError(law)


# ------------------------------------------------------------------ G1 evaluation
def r_M_kpc(M, a0_kpc):
    return math.sqrt(G * M / a0_kpc)


def G1_cell(vname, geom, M, a_model_si, norm, Hgate_si=None, h=H_SPHERE):
    """returns dict for one cell: R over XGRID, admissibility, and G1-P2 reading."""
    a = AKPC(a_model_si)
    a0t = AKPC(norm_a0(norm, a_model_si))
    rM = r_M_kpc(M, a0t)
    r = XGRID * rM
    prof = PointMass(M) if geom == "point" else ExpSphere(M, h)
    v = variant(vname, prof, r, a, H_a0_gate=(AKPC(Hgate_si) if Hgate_si else None))
    Mb = prof.Mb(r)
    R = 4 * math.pi * r ** 3 * v["rho_D"] * v["g_tot"] / (a0t * Mb)
    scale = np.max(np.abs(v["rho_D"])) + 1e-300
    adm = dict(rho_ok=bool(np.all(v["rho_D"] >= -1e-9 * scale)),
               mass_ok=bool(np.all(v["M_dark"] >= -1e-9 * np.max(np.abs(v["M_dark"]) + 1e-300))),
               g_ok=bool(np.all(v["g_tot"] >= v["gN"] * (1 - 1e-9))))
    adm["all"] = adm["rho_ok"] and adm["mass_ok"] and adm["g_ok"]
    inb = np.abs(R - 1) <= 0.10
    gP2 = v["gN"] * np.sqrt(1 + a / v["gN"])
    g2 = float(np.max(np.abs(v["g_tot"] / gP2 - 1)))
    idx = [int(np.argmin(np.abs(XGRID - x))) for x in (0.1, 1, 3, 10, 30)]
    bad = np.where(~inb)[0]
    if len(bad) == 0:
        rng = 0.1
    elif bad[-1] == NX - 1:
        rng = None
    else:
        rng = float(XGRID[bad[-1] + 1])
    return dict(maxdev=float(np.max(np.abs(R - 1))), all_in_band=bool(inb.all()), x_from=rng, R_at=[float(R[i]) for i in idx],
                adm=adm, G1P2_maxdev=g2, pass_strict=bool(inb.all() and adm["all"]), R_only=bool(inb.all()), rM=rM)


# ------------------------------------------------------------------ reporting
class Report:
    def __init__(self, slug, mutate=None):
        self.slug = slug + (f"_MUTATE_{mutate}" if mutate else "")
        self.mutate = mutate
        self.lines, self.checks, self.numbers, self.t0 = [], [], {}, time.time()

    def P(self, s=""):
        print(s, flush=True)
        self.lines.append(s)

    def banner(self, s):
        self.P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)

    def check(self, name, detail, ok, load_bearing=True):
        self.checks.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=load_bearing))
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")

    def num(self, k, v):
        self.numbers[k] = v

    def write(self):
        lb = [c for c in self.checks if c["load_bearing"]]
        nf = sum(not c["ok"] for c in lb)
        self.P(f"\n  {sum(c['ok'] for c in self.checks)}/{len(self.checks)} checks pass; load-bearing failures: {nf}   ({time.time() - self.t0:.0f} s)")

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
            return o if isinstance(o, (int, str)) or o is None else str(o)

        outdir = os.environ.get("CFG231_OUT", HERE)
        json.dump(clean(dict(slug=self.slug, load_bearing_failures=nf, checks=self.checks, numbers=self.numbers)),
                  open(os.path.join(outdir, self.slug + "_results.json"), "w"), indent=1)
        open(os.path.join(outdir, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")
        return nf


def header(R, title):
    R.P(title)
    R.P(f"  repo = <repo>   (constants and controls import <repo>/campaign_fresh_gravity/CFG44_fluid_target/Bcommon.py read-only)")
    R.P(f"  mode = {R.mutate or 'MAIN'};  a0 footings: canonical {A0_SI['canonical']:.4e}, alt {A0_SI['alt']:.4e} m/s^2;  H0 = {H0_KMS_MPC}, Omega_L = {OMEGA_L}")
    R.P(f"  a_V(H_Lambda) = {a_V_si('HL'):.4e}, a_V(H0) = {a_V_si('H0'):.4e} m/s^2;  kappa = 1/2 FITTED; nothing here says the theory is closed or that data favour it.")
