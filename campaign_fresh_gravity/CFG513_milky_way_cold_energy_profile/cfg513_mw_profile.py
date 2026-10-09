#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG513 -- THE MILKY WAY'S OWN COLD-ENERGY PROFILE vs NFW, AND THE BIAS AN NFW ASSUMPTION PUTS INTO MW-BASED MEASUREMENTS.
Criteria: FROZEN_CRITERIA.md (committed alone first, 548396b05).  In one line each:
  PROFILE  record baryons (6.0e10 primary, 7.3e10 census-high; L172 shapes), nu_mono, phantom = settled cold energy (candidate B),
           PAPER45 zero-knob edge M_ph(<r_edge) = M_b (1-f_b)/(f_ret f_b) with f_ret = 1 and 0.18 (never pooled), bare law reported.
  NFW      N-F = NFW + same baryons fitted to the framework's own V_c at the Ou+24 radii (N-F+T adds M(<50), M(<100)); N-D = fitted
           to the Ou+24 data; literature halos RECALLED, UNVERIFIED.
  BIAS     b = Q(assumed NFW) - Q(true framework), in units of the measurement's quoted error; MATERIAL > 1, MINOR 0.3-1, NONE <= 0.3.
MUTATE (CFG513_MUTATE=1): truth := the assumed NFW of every row -> every bias must vanish.
kappa = 1/2 FITTED.  No dark-matter particle: the cold energy's MASS is still required.  Not theory closed; the data are not said to
favour the framework.
Run: nice -n 15 python3 campaign_fresh_gravity/CFG513_milky_way_cold_energy_profile/cfg513_mw_profile.py   (CFG513_MUTATE=1 for the control)
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "4"
import sys
sys.dont_write_bytecode = True
import io, math, json, re, csv, hashlib, time, warnings
warnings.filterwarnings("ignore", message=".*roundoff.*")
import numpy as np
from scipy.special import i0, i1, k0, k1, j0, j1
from scipy.optimize import brentq, least_squares
from scipy.integrate import quad, solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C                                   # nu_mono (FP1's committed table, read-only), REPO

MUT = os.environ.get("CFG513_MUTATE", "0") == "1"
SLUG = "cfg513" + ("_MUTATE" if MUT else "")
LINES, CHECKS, NUM = [], [], {}
T0 = time.time()


def P(s=""):
    print(s, flush=True); LINES.append(s)


def check(name, detail, ok, lb=True):
    CHECKS.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=lb))
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}\n         {detail}")


def banner(s):
    P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)


P(__doc__.split("Run: nice")[0].strip())
FROZEN = os.path.join(HERE, "FROZEN_CRITERIA.md")
P(f"\n  FROZEN_CRITERIA.md sha256 {hashlib.sha256(open(FROZEN, 'rb').read()).hexdigest()}")
if MUT:
    P("\n  *** MUTATE: the 'true' profile of every row is the assumed NFW of that row; every bias must vanish ***")

# ================================================================================================ constants (kpc, km/s, Msun)
G = 4.30091727e-6
KPC_M = 3.0856775814913673e19
A0 = {"canonical": 9.36e-11 * KPC_M / 1e6, "alt": 1.13e-10 * KPC_M / 1e6}      # (km/s)^2/kpc
A0_SI = {"canonical": 9.36e-11, "alt": 1.13e-10}
FOOTS = ("canonical", "alt")
nu_mono = C.nu_mono
COLD_PER_B = 5.364                                         # (1 - f_b)/f_b, CFG390
F_B = 1.0 / (1.0 + COLD_PER_B)
H = 0.674; H0 = 0.1 * H                                    # km/s/kpc
OM_M = 0.3153; OM_L = 1 - OM_M
RHO_C = 3 * H0 ** 2 / (8 * math.pi * G)                    # Msun/kpc^3
T0_GYR = 13.80
GYR = 3.15576e16 / (KPC_M / 1e3)                           # 1 Gyr in kpc/(km/s)
R0 = 8.178
PC3 = 1e9                                                  # Msun/pc^3 -> Msun/kpc^3
MB_PRIM, MB_HI, MB_M31 = 6.0e10, 7.3e10, 1.2e11
FRETS = (1.0, 0.18)
D_LG, VR_LG, EVR_LG = 780.0, -109.3, 4.4                   # FP11 / CFG30 on-disk inputs


def bary_parts(Mb):
    s = Mb / 6.7e10                                        # L172 ratios 1.0 : 4.5 : 1.2
    return dict(Mbul=1.0e10 * s, abul=0.7, Md=4.5e10 * s, Rd=2.6, Mg=1.2e10 * s, Rg=6.0)


def exp_disc_v2(R, M, Rd):
    R = np.maximum(np.asarray(R, float), 1e-6)
    y = R / (2 * Rd); S0 = M / (2 * math.pi * Rd ** 2)
    return 4 * math.pi * G * S0 * Rd * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y))


def exp_disc_field(R, z, M, Rd):
    """razor-thin exponential disc, Hankel form; returns (g_R, g_z), negative = toward centre / plane."""
    S0 = M / (2 * math.pi * Rd ** 2); pre = 2 * math.pi * G * S0 * Rd ** 2
    kmax = 60.0 / max(z, 1e-3)
    fR = quad(lambda k: k * j1(k * R) * math.exp(-k * z) * (1 + (k * Rd) ** 2) ** -1.5, 0, kmax, limit=800)[0]
    fz = quad(lambda k: k * j0(k * R) * math.exp(-k * z) * (1 + (k * Rd) ** 2) ** -1.5, 0, kmax, limit=800)[0]
    return -pre * fR, -pre * fz


class Prof:
    """A spherical-mass Milky Way: baryons (record) + a dark/cold component (framework phantom or NFW)."""

    def __init__(self, name, Mb=MB_PRIM, kind="F", foot="canonical", fret=1.0, M200=None, c=None, rhos=None, rs=None,
                 bary=None, point=False):
        self.name, self.kind, self.foot, self.fret, self.point = name, kind, foot, fret, point
        self.Mb = Mb
        self.bp = bary_parts(Mb) if bary is None else bary
        self.mwp14 = bary is not None and bary.get("mwp14", False)
        if kind == "NFW":
            if M200 is not None:
                R200 = (3 * M200 / (4 * math.pi * 200 * RHO_C)) ** (1 / 3)
                self.rs = R200 / c; self.rhos = M200 / (4 * math.pi * self.rs ** 3 * (math.log(1 + c) - c / (1 + c)))
                self.M200, self.c = M200, c
            else:
                self.rs, self.rhos = rs, rhos
                self.M200, self.c = self._m200()
        if kind == "F":
            self.a0 = A0[foot]
            self.Mcold = None if fret is None else COLD_PER_B * self.Mb_tot() / fret
            self.redge = np.inf
            if self.Mcold is not None:
                f = lambda lr: self._Mph_raw(10 ** lr) - self.Mcold
                self.redge = 10 ** brentq(f, 0.0, 5.0, xtol=1e-12)

    # ---- baryons
    def Mb_tot(self):
        b = self.bp
        return b["Mbul"] + b["Md"] + (b.get("Mg", 0.0))

    def Mb_enc(self, r):
        r = np.asarray(r, float); b = self.bp
        if self.point:
            return np.full_like(r, self.Mb_tot())
        if self.mwp14:                                     # spherical approximation of MWPotential14-class baryons
            return b["Mbul"] * r ** 2 / (r + b["abul"]) ** 2 + b["Md"] * r ** 3 / (r ** 2 + (b["a"] + b["b"]) ** 2) ** 1.5
        xd, xg = r / b["Rd"], r / b["Rg"]
        return (b["Mbul"] * r ** 2 / (r + b["abul"]) ** 2 + b["Md"] * (1 - (1 + xd) * np.exp(-xd))
                + b["Mg"] * (1 - (1 + xg) * np.exp(-xg)))

    def gN_plane(self, R):
        b = self.bp; R = np.asarray(R, float)
        return (exp_disc_v2(R, b["Md"], b["Rd"]) + exp_disc_v2(R, b["Mg"], b["Rg"]) + G * b["Mbul"] * R / (R + b["abul"]) ** 2) / R

    def rho_b_mid(self, R, hs=0.3, hg=0.1):
        b = self.bp
        Ss = b["Md"] / (2 * math.pi * b["Rd"] ** 2) * math.exp(-R / b["Rd"])
        Sg = b["Mg"] / (2 * math.pi * b["Rg"] ** 2) * math.exp(-R / b["Rg"])
        rb = b["Mbul"] * b["abul"] / (2 * math.pi * R * (R + b["abul"]) ** 3)
        return Ss / (2 * hs) + Sg / (2 * hg) + rb, Ss, Sg

    # ---- dark / cold component
    def _Mph_raw(self, r):
        r = np.asarray(r, float); Mb = self.Mb_enc(r)
        y = G * Mb / (r ** 2 * self.a0)
        return Mb * (nu_mono(y) - 1.0)

    def _m200(self):
        f = lambda lr: (self.M_enc(10 ** lr) / (4 / 3 * math.pi * (10 ** lr) ** 3)) - 200 * RHO_C
        R200 = 10 ** brentq(f, 0.5, 4.0)
        return float(self.Mdark(R200) + self.Mb_enc(R200)), R200 / self.rs

    def M200_total(self):
        f = lambda lr: (self.M_enc(np.array([10 ** lr]))[0] / (4 / 3 * math.pi * (10 ** lr) ** 3)) - 200 * RHO_C
        R200 = 10 ** brentq(f, 0.5, 4.0, xtol=1e-12)
        return float(self.M_enc(np.array([R200]))[0]), R200

    def Mdark(self, r):
        r = np.asarray(r, float)
        if self.kind == "F":
            m = self._Mph_raw(np.minimum(r, self.redge))
            return m
        if self.kind == "NFW":
            x = r / self.rs
            return 4 * math.pi * self.rhos * self.rs ** 3 * (np.log1p(x) - x / (1 + x))
        return np.zeros_like(r)

    def M_enc(self, r):
        return self.Mb_enc(r) + self.Mdark(r)

    def rho_dark(self, r):
        r = np.asarray(r, float)
        if self.kind == "NFW":
            x = r / self.rs
            return self.rhos / (x * (1 + x) ** 2)
        e = 1e-4
        d = (self.Mdark(r * (1 + e)) - self.Mdark(r * (1 - e))) / (2 * r * e)
        return np.where(r < self.redge * (1 - 2e-4), d / (4 * math.pi * r ** 2), 0.0)

    def vc_plane(self, R):
        gN = self.gN_plane(R)
        if self.kind == "F":
            return np.sqrt(R * nu_mono(gN / self.a0) * gN)
        return np.sqrt(R * gN + G * self.Mdark(R) / R)

    def vc_sph(self, r):
        return np.sqrt(G * self.M_enc(r) / r)

    def rho_dark_mid(self, R):
        """midplane cold/dark density.  Framework: algebraic QUMOND (nu - 1) rho_b + |g_N| dnu/dR / (4 pi G).  NFW: rho_NFW."""
        if self.kind != "F":
            return float(self.rho_dark(np.array([R]))[0]), 0.0, 0.0
        rb = self.rho_b_mid(R)[0]
        nu = lambda RR: float(nu_mono(self.gN_plane(np.array([RR]))[0] / self.a0))
        gN = float(self.gN_plane(np.array([R]))[0]); e = 1e-3
        dnu = (nu(R * (1 + e)) - nu(R * (1 - e))) / (2 * R * e)
        t1 = (nu(R) - 1) * rb; t2 = gN * dnu / (4 * math.pi * G)
        return t1 + t2, t1, t2

    def slab_dark(self, R, zmax=1.1):
        """dark surface density within |z| < zmax, as an equivalent constant density over 2 zmax."""
        if self.kind != "F":
            return float(self.rho_dark(np.array([R]))[0])
        rb, Ss, Sg = self.rho_b_mid(R)
        Sb = Ss * (1 - math.exp(-zmax / 0.3)) + Sg * (1 - math.exp(-zmax / 0.1))
        nu = lambda RR: float(nu_mono(self.gN_plane(np.array([RR]))[0] / self.a0))
        gN = float(self.gN_plane(np.array([R]))[0]); e = 1e-3
        dnu = (nu(R * (1 + e)) - nu(R * (1 - e))) / (2 * R * e)
        return (nu(R) - 1) * Sb / (2 * zmax) + gN * dnu / (4 * math.pi * G)

    def dark_force(self, R, z):
        """(g_R, g_z) of the dark/cold part only."""
        if self.kind == "F":
            b = self.bp
            dR, dz = exp_disc_field(R, z, b["Md"], b["Rd"]); gR, gz = dR, dz
            dR, dz = exp_disc_field(R, z, b["Mg"], b["Rg"]); gR += dR; gz += dz
            r = math.hypot(R, z); gb = G * b["Mbul"] / (r + b["abul"]) ** 2
            gR -= gb * R / r; gz -= gb * z / r
            gN = math.hypot(gR, gz); f = float(nu_mono(gN / self.a0)) - 1
            return f * gR, f * gz
        r = math.hypot(R, z); g = G * float(self.Mdark(np.array([r]))[0]) / r ** 2
        return -g * R / r, -g * z / r

    # ---- potential for orbits
    def phi_table(self):
        if hasattr(self, "_phi"):
            return self._phi
        lr = np.linspace(-2, 6, 8001); r = 10 ** lr
        g = G * self.M_enc(r) / r ** 2
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] * r[1:] + g[:-1] * r[:-1]) * np.diff(lr) * math.log(10))])
        phi = cum - cum[-1] - G * self.M_enc(r[-1:])[0] / r[-1]
        self._phi = (lr, phi)
        return self._phi

    def phi(self, r):
        lr, ph = self.phi_table()
        return np.interp(np.log10(r), lr, ph)

    def summary(self):
        if self.kind == "F":
            rM = math.sqrt(G * self.Mb_tot() / self.a0)
            return f"{self.name}: M_b {self.Mb_tot():.2e}, r_M {rM:.1f} kpc, M_cold {self.Mcold if self.Mcold else float('inf'):.3e}, r_edge {self.redge:.1f} kpc"
        return f"{self.name}: NFW M200c {self.M200:.3e}, c {self.c:.2f}, r_s {self.rs:.2f} kpc, rho_s {self.rhos / PC3:.5f} Msun/pc^3"


def verdict(x):
    x = abs(x)
    return "MATERIAL" if x > 1 else ("MINOR" if x > 0.3 else "NONE")


def worst(vs):
    order = {"NONE": 0, "MINOR": 1, "MATERIAL": 2}
    return max(vs, key=lambda v: order[v])


ROWS = []                                                  # the bias table


def row(key, label, cells, sigma_note, touches, extra=""):
    """cells: list of (cell_label, b_over_sigma, frac_bias).  Verdict = worst cell."""
    vs = [verdict(c[1]) for c in cells]
    w = worst(vs)
    bs = [c[1] for c in cells]
    ROWS.append(dict(key=key, label=label, verdict=w, b_sigma_min=float(min(bs)), b_sigma_max=float(max(bs)),
                     frac_min=float(min(c[2] for c in cells)), frac_max=float(max(c[2] for c in cells)),
                     cells=[dict(cell=c[0], b_sigma=float(c[1]), frac=float(c[2]), verdict=v) for c, v in zip(cells, vs)],
                     sigma=sigma_note, touches=touches, extra=extra))
    P(f"  ROW {key} {label}: {w}  (b/sigma {min(bs):+.2f} .. {max(bs):+.2f}; frac {min(c[2] for c in cells):+.3f} .. "
      f"{max(c[2] for c in cells):+.3f}; sigma {sigma_note}; touches {touches})")
    for c, v in zip(cells, vs):
        P(f"        {c[0]:44s} b/sigma {c[1]:+8.3f}  frac {c[2]:+8.4f}  {v}")
    if extra:
        P(f"        {extra}")


# ================================================================================================ 1. the framework's MW
banner("1. THE FRAMEWORK'S MILKY WAY: baryons + nu_mono + settled cold energy (phantom) with the PAPER45 edge")
bp = bary_parts(MB_PRIM)
P(f"  baryons (6.0e10 primary): bulge {bp['Mbul']:.3e} (Hernquist a 0.7), stellar disc {bp['Md']:.3e} (R_d 2.6), gas {bp['Mg']:.3e} (R_d 6.0); "
  f"census-high 7.3e10 scaled the same.  f_b = {F_B:.4f} ((1 - f_b)/f_b = {COLD_PER_B})")
FW = {}
for foot in FOOTS:
    for Mb in (MB_PRIM, MB_HI):
        for fret in FRETS + (None,):
            k = (foot, Mb, fret)
            FW[k] = Prof(f"F|{foot}|Mb{Mb:.1e}|fret{fret if fret else 'bare'}", Mb=Mb, foot=foot, fret=fret)
            P("  " + FW[k].summary())

# C1: point-mass edge
c1 = []
for foot in FOOTS:
    for fret in FRETS:
        pm = Prof("pm", Mb=MB_PRIM, foot=foot, fret=fret, point=True)
        rM = math.sqrt(G * MB_PRIM / A0[foot]); an = rM / math.log(1 + fret * F_B / (1 - F_B))
        c1.append((foot, fret, pm.redge / rM, an / rM, pm.redge / an - 1))
check("C1 nu_mono point-mass edge = r_M/ln(1 + f_ret f_b/(1 - f_b)) within 1% (f_ret = 1 and 0.18, both footings)",
      "; ".join(f"{a} f_ret {b}: {x:.3f} r_M vs {y:.3f} ({d:+.1e})" for a, b, x, y, d in c1), all(abs(d) < 0.01 for *_, d in c1))
# C2
c2, neg = [], []
for foot in FOOTS:
    bare = FW[(foot, MB_PRIM, None)]; pm = Prof("pm", Mb=MB_PRIM, foot=foot, fret=None, point=True)
    c2.append(float(bare.M_enc(np.array([200.0]))[0] / pm.M_enc(np.array([200.0]))[0] - 1))
    for fret in FRETS:
        f = FW[(foot, MB_PRIM, fret)]; rr = np.logspace(-1, math.log10(min(f.redge * 0.999, 500)), 400)
        neg.append(float(np.min(f.rho_dark(rr))))
check("C2 extended baryons -> point-mass law at 200 kpc within 1% (bare); rho_ph >= 0 inside the edge",
      f"M(<200) ratio - 1: {', '.join(f'{x:+.1e}' for x in c2)}; min rho_ph {min(neg):.3e} Msun/kpc^3",
      all(abs(x) < 0.01 for x in c2) and min(neg) >= 0)

RSPLIT = D_LG * math.sqrt(MB_PRIM) / (math.sqrt(MB_PRIM) + math.sqrt(MB_M31))
P(f"\n  OWNERSHIP: O-MW -> the MW owns its phantom to its edge.  O-LG -> the Local Group is the outermost bound system; the MW-centric "
  f"spherical profile is defined only inside r_split = {RSPLIT:.0f} kpc (deep-law field equality toward M31 at {D_LG:.0f} kpc).")
NUM["r_split_kpc"] = RSPLIT

# ================================================================================================ 2. the NFW references
banner("2. NFW REFERENCES (same baryons, Newtonian).  Literature halos RECALLED, UNVERIFIED")


def read_rc(path, minus_first):
    rows = [l.split() for l in open(path) if not l.startswith("#") and l.strip() and not l.startswith("R_kpc")]
    a = np.array([[float(x) for x in r[:4]] for r in rows])
    R, V = a[:, 0], a[:, 1]
    e = 0.5 * (a[:, 2] + a[:, 3])
    return R, V, e


DATA = os.path.join(C.REPO, "real_research", "data")
R_OU, V_OU, E_OU = read_rc(os.path.join(DATA, "mw_rc_ou2024_table1.tsv"), False)
R_EI, V_EI, E_EI = read_rc(os.path.join(DATA, "mw_rc_eilers2019_table1.tsv"), True)
SYS_OU = np.where(R_OU <= 22, 0.03, 0.15)
P(f"  Ou+24: {len(R_OU)} points {R_OU.min():.2f}-{R_OU.max():.2f} kpc; Eilers+19: {len(R_EI)} points {R_EI.min():.2f}-{R_EI.max():.2f} kpc (on disk)")


def fit_nfw(R, V, eV, Mb=MB_PRIM, tracers=None, x0=(12.0, 1.0)):
    def res(p):
        n = Prof("fit", Mb=Mb, kind="NFW", M200=10 ** p[0], c=10 ** p[1])
        r = (n.vc_plane(R) - V) / eV
        if tracers:
            r = np.concatenate([r, [(n.M_enc(np.array([rt]))[0] - Mt) / (0.15 * Mt) for rt, Mt in tracers]])
        return r
    s = least_squares(res, x0, bounds=([9.0, -0.5], [14.5, 2.0]), xtol=1e-14, ftol=1e-14, gtol=1e-14)
    n = Prof("N-fit", Mb=Mb, kind="NFW", M200=10 ** s.x[0], c=10 ** s.x[1])
    return n, float(np.sum(s.fun ** 2))


# C5: recover a synthetic NFW
syn = Prof("syn", kind="NFW", M200=9.0e11, c=11.0)
fs, _ = fit_nfw(R_OU, syn.vc_plane(R_OU), np.hypot(E_OU, SYS_OU * V_OU), x0=(11.5, 0.8))
check("C5 the N-F fitter recovers a synthetic NFW + baryons curve (M200c 9e11, c 11) to 1e-3",
      f"recovered M200c {fs.M200:.5e}, c {fs.c:.5f}", abs(fs.M200 / 9e11 - 1) < 1e-3 and abs(fs.c / 11 - 1) < 1e-3)

LIT = {
    "N-std (1e12, c 10)": Prof("N-std", kind="NFW", M200=1.0e12, c=10.0),
    "N-McM (McMillan17 rho_s 0.00854, r_s 19.6)": Prof("N-McM", kind="NFW", rhos=0.00854 * PC3, rs=19.6),
}
MWP14 = dict(Mbul=0.5e10, abul=0.5, Md=6.8e10, a=3.0, b=0.28, mwp14=True)
LIT_FRITZ = {k: Prof(k, kind="NFW", M200=M, c=((3 * M / (4 * math.pi * 200 * RHO_C)) ** (1 / 3)) / 16.0, bary=MWP14)
             for k, M in (("N-B08", 0.8e12), ("N-B16", 1.6e12))}
for p in list(LIT.values()) + list(LIT_FRITZ.values()):
    P("  " + p.summary() + "   [RECALLED, UNVERIFIED]")
P("  Eilers+2019 NFW M_vir 7.25e11; Jiao+2023 Einasto ~2e11 (via L172): reported only [RECALLED, UNVERIFIED]")

# N-D: fit to the data
ND, chi_nd = fit_nfw(R_OU, V_OU, np.hypot(E_OU, SYS_OU * V_OU))
P(f"  N-D (NFW + record baryons 6.0e10 fitted to Ou+24 data): {ND.summary()}; chi2 {chi_nd:.1f} / {len(R_OU) - 2}")
NUM["N-D"] = dict(M200=ND.M200, c=ND.c, chi2=chi_nd, ndof=len(R_OU) - 2)

# The framework's own chi^2 against the RC data (TEST, no fit)
P("\n  THE FRAMEWORK'S IN-PLANE V_c AGAINST THE MW DATA (a TEST, nothing fitted; Ou errors random (+) stated systematic):")
RCT = {}
for foot in FOOTS:
    for Mb in (MB_PRIM, MB_HI):
        f = FW[(foot, Mb, 1.0)]
        vo = f.vc_plane(R_OU); ve = f.vc_plane(R_EI)
        chi_o = float(np.sum(((vo - V_OU) / np.hypot(E_OU, SYS_OU * V_OU)) ** 2))
        chi_e = float(np.sum(((ve - V_EI) / np.hypot(E_EI, 0.03 * V_EI)) ** 2))
        RCT[f"{foot}|{Mb:.1e}"] = dict(v8=float(f.vc_plane(np.array([R0]))[0]), v20=float(f.vc_plane(np.array([20.0]))[0]),
                                      v25=float(f.vc_plane(np.array([25.0]))[0]), chi2_ou=chi_o, n_ou=len(R_OU), chi2_ei=chi_e,
                                      n_ei=len(R_EI), med_ratio_ou=float(np.median(V_OU / vo)))
        r = RCT[f"{foot}|{Mb:.1e}"]
        P(f"    {foot:9s} M_b {Mb:.1e}: V(R0) {r['v8']:.1f}, V(20) {r['v20']:.1f}, V(25) {r['v25']:.1f} km/s; chi2 Ou {chi_o:.0f}/{len(R_OU)}, "
          f"Eilers (3% sys) {chi_e:.0f}/{len(R_EI)}; median V_obs/V_F {r['med_ratio_ou']:.3f}")
NUM["rc_test"] = RCT

# N-F: the NFW an RC analysis would infer if the framework were the truth
NF, NFT = {}, {}
for foot in FOOTS:
    for Mb in (MB_PRIM, MB_HI):
        for fret in FRETS:
            truth = FW[(foot, Mb, fret)]
            vF = truth.vc_plane(R_OU); eV = np.hypot(E_OU, SYS_OU * vF)
            n, chi = fit_nfw(R_OU, vF, eV, Mb=Mb)
            tr = [(50.0, float(truth.M_enc(np.array([50.0]))[0])), (100.0, float(truth.M_enc(np.array([100.0]))[0]))]
            nt, chit = fit_nfw(R_OU, vF, eV, Mb=Mb, tracers=tr)
            NF[(foot, Mb, fret)], NFT[(foot, Mb, fret)] = (n, chi), (nt, chit)
            if fret == 1.0:
                P(f"  N-F   for {truth.name}: {n.summary()}; chi2 {chi:.2f}")
                P(f"  N-F+T for {truth.name}: {nt.summary()}; chi2 {chit:.2f}")


def truth_of(key, assumed):
    """MUTATE: the truth is the assumed profile itself."""
    return assumed if MUT else FW[key]


def nf_of(key, tracers=False):
    """the N-F (or N-F+T) fitted to the truth.  In MUTATE the truth is N-F itself, refitted."""
    n = (NFT if tracers else NF)[key][0]
    if not MUT:
        return FW[key], n
    truth = n
    vF = truth.vc_plane(R_OU); eV = np.hypot(E_OU, SYS_OU * vF)
    tr = [(50.0, float(truth.M_enc(np.array([50.0]))[0])), (100.0, float(truth.M_enc(np.array([100.0]))[0]))] if tracers else None
    n2, _ = fit_nfw(R_OU, vF, eV, Mb=key[1], tracers=tr, x0=(math.log10(n.M200), math.log10(n.c)))
    return truth, n2


CELLS = [(foot, MB_PRIM, fret) for foot in FOOTS for fret in FRETS]
CELLS_MB = [(foot, Mb, fret) for foot in FOOTS for Mb in (MB_PRIM, MB_HI) for fret in FRETS]


def clab(k):
    return f"{k[0]}|Mb {k[1]:.1e}|f_ret {k[2]}"


# ================================================================================================ 3. the profile itself
banner("3. THE PROFILE: rho(r), M(<r), V_c(r), 0.1-500 kpc (framework vs N-F and literature NFW)")
RR = np.array([1, 2, 5, 8.178, 10, 15, 20, 30, 50, 75, 100, 150, 200, 250, 300, 400, 500.0])
prof_rows = []
for foot in FOOTS:
    P(f"\n  {foot}, M_b 6.0e10:  r [kpc] | M(<r) [1e10]: F f_ret 1 / F f_ret 0.18 / bare / N-F(f1) / N-std / N-McM | V_c,sph: F1 / F0.18 / N-F / N-McM")
    f1, f18, fb = FW[(foot, MB_PRIM, 1.0)], FW[(foot, MB_PRIM, 0.18)], FW[(foot, MB_PRIM, None)]
    nf = NF[(foot, MB_PRIM, 1.0)][0]
    for r in RR:
        a = np.array([r])
        Ms = [p.M_enc(a)[0] / 1e10 for p in (f1, f18, fb, nf, LIT["N-std (1e12, c 10)"], LIT["N-McM (McMillan17 rho_s 0.00854, r_s 19.6)"])]
        Vs = [p.vc_sph(a)[0] for p in (f1, f18, nf, LIT["N-McM (McMillan17 rho_s 0.00854, r_s 19.6)"])]
        flag = "  [beyond r_split: LG-owned under O-LG]" if r > RSPLIT else ""
        P(f"    {r:7.1f} | " + " ".join(f"{m:7.2f}" for m in Ms) + " | " + " ".join(f"{v:6.1f}" for v in Vs) + flag)
# key profile numbers
for foot in FOOTS:
    for fret in FRETS:
        f = FW[(foot, MB_PRIM, fret)]
        NUM[f"profile|{foot}|{fret}"] = dict(r_edge=f.redge, M_cold=f.Mcold, M_tot=f.Mb_tot() + f.Mcold,
                                            M50=float(f.M_enc(np.array([50.0]))[0]), M100=float(f.M_enc(np.array([100.0]))[0]),
                                            M200=float(f.M_enc(np.array([200.0]))[0]), M300=float(f.M_enc(np.array([300.0]))[0]),
                                            rho_R0=float(f.rho_dark(np.array([R0]))[0] / PC3))
# CSV of the profiles
rg = np.logspace(-1, math.log10(500), 300)
with open(os.devnull if MUT else os.path.join(HERE, "cfg513_profiles.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    cols = [("F_can_fret1", FW[("canonical", MB_PRIM, 1.0)]), ("F_can_fret0.18", FW[("canonical", MB_PRIM, 0.18)]),
            ("F_alt_fret1", FW[("alt", MB_PRIM, 1.0)]), ("F_alt_fret0.18", FW[("alt", MB_PRIM, 0.18)]),
            ("NF_can_fret1", NF[("canonical", MB_PRIM, 1.0)][0]), ("N_std", LIT["N-std (1e12, c 10)"]),
            ("N_McM", LIT["N-McM (McMillan17 rho_s 0.00854, r_s 19.6)"]), ("N_D", ND)]
    w.writerow(["r_kpc"] + [f"{n}_{q}" for n, _ in cols for q in ("rho_dark_Msun_pc3", "M_enc_Msun", "Vc_sph_kms")])
    for r in rg:
        a = np.array([r])
        w.writerow([f"{r:.4f}"] + [f"{x:.6e}" for _, p in cols for x in (p.rho_dark(a)[0] / PC3, p.M_enc(a)[0], p.vc_sph(a)[0])])

# ================================================================================================ 4. the bias catalogue
banner("4. THE BIAS CATALOGUE: b = Q(assumed NFW) - Q(true framework), in units of the quoted error")

# ---------------------------------------------------------------- (a) satellites
P("\n(a) SATELLITE ORBITS -- Fritz+2018 Tables 2 and 3 (on disk), static spherical potentials, exact turning points")
TEX = os.path.join(C.REPO, "..", "_external_data", "cfg433_work", "src", "UFDsmot_arx_final.tex")
txt = open(TEX).read()
P(f"  source sha256 {hashlib.sha256(txt.encode()).hexdigest()}")


def table_rows(label, end=r"\end{array}"):
    i0_ = txt.index(label); i1_ = txt.index(end, i0_)
    out = []
    for line in txt[i0_:i1_].splitlines():
        line = line.strip()
        if "&" not in line or line.startswith("&") or line.startswith("satellite"):
            continue
        c = [x.strip() for x in line.rstrip().rstrip("\\").split("&")]
        if len(c) >= 7:
            out.append(c)
    return out


def pm3(s):
    return [float(v) for v in s.replace(" ", "").split(r"\pm")]


def asym(s):
    s = s.replace(" ", "").rstrip("\\").strip()
    if s.startswith(">"):
        return float(s[1:]), np.nan, np.nan
    m = re.match(r"([-\d.]+)\^\{\+([\d.]+)\}_\{-([\d.]+)\}", s)
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


SAT = {}
for c in table_rows(r"\label{KapSou2}"):
    vr = pm3(c[7]); vt = asym(c[8])
    SAT[c[0]] = dict(d=float(c[1]), vrad=vr[0], vtan=vt[0])
for c in table_rows(r"\label{KapSou3}"):
    if c[0] in SAT:
        SAT[c[0]].update(p16=asym(c[1]), a16=asym(c[2]), p08=asym(c[4]), a08=asym(c[5]))
NAMES = [n for n in SAT if "p08" in SAT[n]]
P(f"  {len(NAMES)} objects with Table 2 + Table 3 entries (galactocentric distance = Fritz's own d_GC column; see README deviation note)")


def peri_apo(prof, r0, vr, vt):
    L = r0 * vt; E = 0.5 * (vr ** 2 + vt ** 2) + prof.phi(r0)
    f = lambda r: 2 * (E - prof.phi(r)) - L ** 2 / r ** 2
    if vt <= 0:
        rp = 0.0
    else:
        lo = 1e-2
        rp = brentq(f, lo, r0 * (1 - 1e-9)) if f(lo) < 0 < f(r0 * (1 - 1e-9)) else (r0 if f(r0 * (1 - 1e-9)) <= 0 else lo)
    hi = 1e6 * 0.999
    if f(hi) > 0:
        ra = np.inf
    else:
        ra = brentq(f, r0 * (1 + 1e-9), hi) if f(r0 * (1 + 1e-9)) > 0 else r0
    return rp, ra


ORB = {}
for nm in NAMES:
    s = SAT[nm]
    ORB[nm] = {}
    for k, p in LIT_FRITZ.items():
        ORB[nm][k] = peri_apo(p, s["d"], s["vrad"], s["vtan"])
    for key in CELLS:
        ORB[nm][key] = peri_apo(FW[key], s["d"], s["vrad"], s["vtan"])
        ORB[nm][(key[0], key[1], None)] = peri_apo(FW[(key[0], key[1], None)], s["d"], s["vrad"], s["vtan"])
# C4
c4 = {}
for k, col in (("N-B08", "p08"), ("N-B16", "p16")):
    d = [abs(ORB[n][k][0] / SAT[n][col][0] - 1) for n in NAMES if SAT[n][col][0] > 0]
    c4[k] = float(np.median(d))
check("C4 the N-B08 / N-B16 spherical orbits reproduce Fritz Table 3 central pericentres: median |dperi|/peri <= 15% each",
      ", ".join(f"{k}: {v:.3f}" for k, v in c4.items()), all(v <= 0.15 for v in c4.values()))
P(f"\n  {'object':8s} {'d_GC':>5s} | peri: Fritz08 B08  B16 | F can f1  F can f.18 F alt f1 | apo: B08  B16  F can f1  F can f.18 | first-infall (apo>300) B08/F1")
for n in NAMES:
    o = ORB[n]; s = SAT[n]
    fa = lambda x: (f"{x:6.0f}" if np.isfinite(x) else "   inf")
    P(f"  {n:8s} {s['d']:5.0f} | {s['p08'][0]:5.0f} {o['N-B08'][0]:5.0f} {o['N-B16'][0]:5.0f} | {o[('canonical', MB_PRIM, 1.0)][0]:6.0f} "
      f"{o[('canonical', MB_PRIM, 0.18)][0]:7.0f} {o[('alt', MB_PRIM, 1.0)][0]:7.0f} | {fa(o['N-B08'][1])} {fa(o['N-B16'][1])} "
      f"{fa(o[('canonical', MB_PRIM, 1.0)][1])} {fa(o[('canonical', MB_PRIM, 0.18)][1])} | "
      f"{'Y' if o['N-B08'][1] > 300 else 'n'}/{'Y' if o[('canonical', MB_PRIM, 1.0)][1] > 300 else 'n'}")


def sat_cells(assumed_key, col):
    cells = []
    for key in CELLS:
        ap = LIT_FRITZ[assumed_key]
        tr = truth_of(key, ap)
        zs, fr = [], []
        for n in NAMES:
            s = SAT[n]
            pa = ORB[n][assumed_key][0]
            pt = peri_apo(tr, s["d"], s["vrad"], s["vtan"])[0] if MUT else ORB[n][key][0]
            sig = 0.5 * (s[col][1] + s[col][2])
            if sig > 0 and pt > 0:
                zs.append((pa - pt) / sig); fr.append(pa / pt - 1)
        zs = np.array(zs)
        med = float(np.median(np.abs(zs))); f1 = float(np.mean(np.abs(zs) > 1))
        eff = med if med > 0.3 or f1 < 0.25 else max(med, 0.31)            # >= 25% beyond 1 sigma -> at least MINOR
        cells.append((f"{clab(key)} [frac>1sig {f1:.2f}]", eff * np.sign(np.median(zs)) if eff else 0.0, float(np.median(fr))))
    return cells


row("a1", "Satellite pericentres, Fritz 0.8e12 NFW potential assumed", sat_cells("N-B08", "p08"),
    "Fritz+18 Table 3 peri errors (on disk)", "satellites (CFG433/CFG463/CFG286), UFD tidal history")
row("a2", "Satellite pericentres, Fritz 1.6e12 NFW potential assumed", sat_cells("N-B16", "p16"),
    "Fritz+18 Table 3 peri errors (on disk)", "satellites, UFD tidal history")
# apocentres / first infall
fi = {}
for k in ["N-B08", "N-B16"] + CELLS:
    fi[str(k)] = int(sum((ORB[n][k][1] > 300) for n in NAMES))
P(f"  first-infall-like (apo > 300 kpc or unbound) counts of {len(NAMES)}: " + ", ".join(f"{k}: {v}" for k, v in fi.items()))
NUM["first_infall_counts"] = fi
# the record's bare law vs the edge (CFG433/CFG463/CFG286 inherit this)
cells = []
for key in CELLS:
    bk = (key[0], key[1], None)
    zs, fr, fa = [], [], []
    for n in NAMES:
        s = SAT[n]; sig = 0.5 * (s["p08"][1] + s["p08"][2])
        pb, pe = ORB[n][bk][0], ORB[n][key][0]
        ab, ae = ORB[n][bk][1], ORB[n][key][1]
        if MUT:
            pb = pe
        if sig > 0 and pe > 0:
            zs.append((pb - pe) / sig); fr.append(pb / pe - 1)
        if np.isfinite(ae) and ae > 0:
            fa.append(ab / ae - 1)
    zs = np.array(zs)
    cells.append((f"{clab(key)} [apo bare/edge-1 median {np.median(fa) if fa else float('nan'):+.3f}]",
                  float(np.median(np.abs(zs))) * (1 if np.median(zs) >= 0 else -1), float(np.median(fr))))
row("a3", "Record's bare-law host (CFG433/463/286) vs the edge profile, pericentres", cells, "Fritz+18 peri errors",
    "satellites, UFD infall order (CFG463)")
# CFG433 V_c at r_med 78 kpc
cells = []
for key in CELLS:
    f, fb = FW[key], FW[(key[0], key[1], None)]
    vt, vb = f.vc_sph(np.array([78.0]))[0], fb.vc_sph(np.array([78.0]))[0]
    if MUT:
        vb = vt
    cells.append((clab(key), (vb - vt) / 21.4, vb / vt - 1))
row("a4", "CFG433 V_c at r_med 78 kpc: bare law (used) vs edge profile", cells, "CFG433's +-21.4 km/s (on disk)", "satellites (CFG433)")

# ---------------------------------------------------------------- (b) MW mass
P("\n(b) MW MASS: NFW fitted to the framework's inner curve (N-F) and with two tracer masses (N-F+T), extrapolated")
for tracers, tag in ((False, "N-F"), (True, "N-F+T")):
    for rr_, sig_ in ((50.0, 0.15), (100.0, 0.15), (200.0, 0.20), (300.0, 0.20)):
        cells = []
        for key in CELLS_MB:
            tr, nf = nf_of(key, tracers)
            Mt, Ma = float(tr.M_enc(np.array([rr_]))[0]), float(nf.M_enc(np.array([rr_]))[0])
            cells.append((clab(key), (Ma / Mt - 1) / sig_, Ma / Mt - 1))
        row(f"b-{tag}-{rr_:.0f}", f"M(<{rr_:.0f} kpc) extrapolated by {tag}", cells, f"{sig_:.0%} (recalled typical)",
            "MW mass; LG timing; satellites' host mass")
    cells = []
    for key in CELLS_MB:
        tr, nf = nf_of(key, tracers)
        Ma, R200a = nf.M200_total()
        if MUT:
            Mt = tr.M200_total()[0]
        else:
            Mt = float(tr.Mb_tot() + tr.Mcold)                  # the framework's whole mass (baryons + all cold energy)
        MtR = float(tr.M_enc(np.array([R200a]))[0])
        cells.append((f"{clab(key)} [M200c inferred {Ma:.2e} (R200 {R200a:.0f}) vs F total {Mt:.2e}; F M(<R200) {MtR:.2e}]",
                      (Ma / Mt - 1) / 0.20, Ma / Mt - 1))
    row(f"b-{tag}-M200", f"'MW halo mass' M200c by {tag} vs the framework's total (M_b + M_cold)", cells, "20% (recalled review)",
        "MW mass; f_ret readings")

# (b2) LG timing
P("\n(b2) LOCAL GROUP TIMING: radial first approach, 0 -> 780 kpc at t0 = 13.80 Gyr")
T0U = T0_GYR * GYR


def coll_time(acc, d0, v0, lam=True, tmax=60.0):
    """time back to d = 0 from (d0, v0), in kpc/(km/s).  acc(d) > 0 = attraction magnitude."""
    def rhs(t, y):
        d = max(y[0], 1e-3)
        a = -acc(d) + (OM_L * H0 ** 2 * d if lam else 0.0)
        return [-y[1], -a]                               # backward time: tau = t0 - t
    ev = lambda t, y: y[0] - 0.05
    ev.terminal = True; ev.direction = -1
    s = solve_ivp(rhs, (0, tmax * GYR), [d0, v0], events=ev, rtol=1e-10, atol=1e-10, max_step=0.05 * GYR)
    if s.t_events[0].size:
        te = s.t_events[0][0]; ye = s.y_events[0][0]
        return te + ye[0] / max(abs(ye[1]), 1e-9) * 0.5      # small remaining piece, ~ d/(2v)
    return tmax * GYR                                    # no collision within tmax: capped (finite for the root finder)


def v_pred(acc, lam=True):
    f = lambda v: coll_time(acc, D_LG, v, lam) - T0U
    lo, hi = -900.0, 600.0
    if f(lo) < 0:
        return np.nan
    return brentq(f, lo, hi, xtol=1e-6)


def kep_acc(M):
    return lambda d: G * M / d ** 2


# C3: analytic Kepler, no Lambda
M_test = 4.0e12; eta = 4.3
A = (D_LG) / (1 - math.cos(eta)); B = math.sqrt(A ** 3 / (G * M_test)); t_an = B * (eta - math.sin(eta))
v_an = A * math.sin(eta) / (B * (1 - math.cos(eta)))
t_num = coll_time(kep_acc(M_test), D_LG, v_an, lam=False)
check("C3 the timing integrator reproduces the analytic radial Kepler solution (no Lambda) to 1e-4 in t0",
      f"analytic t {t_an / GYR:.6f} Gyr (v {v_an:.3f} km/s), integrator {t_num / GYR:.6f} Gyr, rel {t_num / t_an - 1:+.1e}",
      abs(t_num / t_an - 1) < 1e-4)


def kepler_mass(v, lam=True):
    f = lambda lm: coll_time(kep_acc(10 ** lm), D_LG, v, lam) - T0U
    try:
        return 10 ** brentq(f, 10.0, 14.5, xtol=1e-7)
    except ValueError:
        return np.nan


MK = {lam: kepler_mass(VR_LG, lam) for lam in (False, True)}
P(f"  Kepler timing mass from the measured -109.3 km/s at 780 kpc: {MK[False]:.3e} (no Lambda), {MK[True]:.3e} (Lambda) Msun")
NUM["kepler_timing_mass"] = {str(k): v for k, v in MK.items()}

# C7 (reported): deep-MOND two-body at FP11's nominal baryons
FP11 = json.load(open(os.path.join(C.REPO, "real_research", "derivation_chain_2026", "FP11_local_group_flyby_results.json")))["numbers"]
SH = FP11["baryons"]["share_MW"]
c7 = []
for foot in FOOTS:
    m1, m2 = SH * 1.75e11, (1 - SH) * 1.75e11; M = m1 + m2
    Q = (2 / 3) * math.sqrt(G * A0[foot]) * (M ** 1.5 - m1 ** 1.5 - m2 ** 1.5) * M / (m1 * m2)
    acc = lambda d, Q=Q, M=M: max(G * M / d ** 2, Q / d)
    vp = v_pred(acc)
    ref = [b["vr"] for b in FP11["timing_scan"][f"P2/{foot}/1.750e+11"]["A"] if b["k"] == 0][0]
    c7.append((foot, vp, ref))
check("C7 (reported) deep-MOND two-body + Lambda at FP11's nominal 1.75e11 within 10% of FP11's committed P2 first approach",
      "; ".join(f"{f}: {v:.1f} vs FP11 {r:.1f} ({v / r - 1:+.1%})" for f, v, r in c7), all(abs(v / r - 1) <= 0.10 for _, v, r in c7), lb=False)

LGT = {}
cells = []
for foot in FOOTS:
    for fret in FRETS + (None,):
        mw = FW[(foot, MB_PRIM, fret)]
        m31 = Prof("M31", Mb=MB_M31, foot=foot, fret=fret, point=True)
        acc = lambda d, mw=mw, m31=m31: G * float(mw.M_enc(np.array([d]))[0] + m31.M_enc(np.array([d]))[0]) / d ** 2
        vp = v_pred(acc)
        Mtot = (mw.Mb_tot() + mw.Mcold + MB_M31 + m31.Mcold) if fret else np.inf
        mk = kepler_mass(vp) if np.isfinite(vp) else np.nan
        # O-LG: the LG owns one phantom about the barycentre; MW and M31 carry baryons only
        lg = Prof("LG", Mb=MB_PRIM + MB_M31, foot=foot, fret=fret, point=True)
        q1, q2 = MB_M31 / (MB_PRIM + MB_M31), MB_PRIM / (MB_PRIM + MB_M31)
        acc_lg = lambda d, lg=lg: (G * (MB_PRIM + MB_M31) / d ** 2 + G * float(lg.Mdark(np.array([q1 * d]))[0]) / (q1 * d) ** 2
                                   + G * float(lg.Mdark(np.array([q2 * d]))[0]) / (q2 * d) ** 2)
        vlg = v_pred(acc_lg)
        LGT[f"{foot}|{fret}"] = dict(v_OMW=vp, z_OMW=(abs(vp) - abs(VR_LG)) / EVR_LG if np.isfinite(vp) else np.nan,
                                     v_OLG=vlg, z_OLG=(abs(vlg) - abs(VR_LG)) / EVR_LG if np.isfinite(vlg) else np.nan,
                                     M_true_total=Mtot, M_kepler_from_framework_orbit=mk,
                                     edges=(mw.redge, m31.redge, lg.redge))
        P(f"  {foot:9s} f_ret {str(fret):5s}: O-MW v_pred {vp:7.1f} km/s (z vs -109.3: {LGT[f'{foot}|{fret}']['z_OMW']:+.1f}); "
          f"O-LG v_pred {vlg:7.1f} (z {LGT[f'{foot}|{fret}']['z_OLG']:+.1f}); edges MW/M31/LG {mw.redge:.0f}/{m31.redge:.0f}/{lg.redge:.0f} kpc; "
          f"true M_tot {Mtot:.3e}; Kepler mass a point-mass analysis reads off this orbit {mk:.3e}")
        if fret is not None:
            if MUT:
                mk2 = kepler_mass(v_pred(kep_acc(Mtot)))
                cells.append((f"{foot}|f_ret {fret}", (mk2 / Mtot - 1) / 0.20, mk2 / Mtot - 1))
            else:
                cells.append((f"{foot}|f_ret {fret}", (mk / Mtot - 1) / 0.20, mk / Mtot - 1))
NUM["lg_timing"] = LGT
row("b2", "LG timing mass (point-mass Kepler read of the framework's own orbit) vs the framework's true M_MW + M_M31", cells,
    "20% (recalled timing-mass systematic)", "LG timing (CFG20/CFG30); MW mass")

# ---------------------------------------------------------------- (c) local density
P("\n(c) LOCAL COLD-ENERGY DENSITY AT THE SUN (R0 = 8.178 kpc)")
LOC = {}
for which, fn in (("spherical rho(R0)", lambda p: float(p.rho_dark(np.array([R0]))[0])),
                  ("midplane rho (phantom disc)", lambda p: p.rho_dark_mid(R0)[0]),
                  ("slab |z|<1.1 kpc equivalent", lambda p: p.slab_dark(R0))):
    cells = []
    for key in CELLS_MB:
        tr, nf = nf_of(key)
        qt, qa = fn(tr), fn(nf)
        LOC[f"{which}|{clab(key)}"] = dict(framework=qt / PC3, nfw=qa / PC3)
        cells.append((f"{clab(key)} [F {qt / PC3:.4f} vs N-F {qa / PC3:.4f} Msun/pc^3]", (qa / qt - 1) / 0.20, qa / qt - 1))
    row(f"c-{which.split()[0]}", f"Local dark/cold density, {which}: N-F vs framework", cells, "20% (recalled review)",
        "local density; vertical-force / Oort-limit tests")
for key in CELLS[:2]:
    t = FW[key].rho_dark_mid(R0)
    P(f"  {clab(key)}: midplane phantom = (nu-1) rho_b {t[1] / PC3:.4f} + gradient term {t[2] / PC3:.4f} Msun/pc^3; rho_b,mid "
      f"{FW[key].rho_b_mid(R0)[0] / PC3:.4f}; nu(R0) {float(nu_mono(FW[key].gN_plane(np.array([R0]))[0] / FW[key].a0)):.3f}")
P(f"  literature local DM (RECALLED, UNVERIFIED): 0.008-0.013 Msun/pc^3 (0.3-0.5 GeV/cm^3); N-std {LIT['N-std (1e12, c 10)'].rho_dark(np.array([R0]))[0] / PC3:.4f}, "
  f"N-McM {LIT['N-McM (McMillan17 rho_s 0.00854, r_s 19.6)'].rho_dark(np.array([R0]))[0] / PC3:.4f}, N-D {ND.rho_dark(np.array([R0]))[0] / PC3:.4f}")
# C6: CFG484's P2 point-mass host-fluid density at R0 = 8.2
c6 = []
for foot in FOOTS:
    a0 = A0[foot]; RR0 = 8.2
    rM = math.sqrt(G * MB_PRIM / a0); xx = RR0 / rM
    rho = MB_PRIM * xx / (4 * math.pi * RR0 ** 2 * rM * math.sqrt(1 + xx ** 2)) / PC3
    c6.append(rho)
check("C6 (reported) CFG484's host-fluid density at R0 (0.0049 / 0.0057 Msun/pc^3, P2 point mass) reproduced within 5%",
      f"{c6[0]:.5f} / {c6[1]:.5f}", abs(c6[0] / 0.0049 - 1) < 0.05 and abs(c6[1] / 0.0057 - 1) < 0.05, lb=False)
NUM["local_density"] = LOC

# ---------------------------------------------------------------- (d) DR4 / wide binaries
P("\n(d) WIDE BINARIES / GAIA DR4 -- the frozen prereg READ ONLY (prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md)")
PRE = os.path.join(C.REPO, "prep_2026", "gaia_dr4_prep", "PREREGISTRATION_DR4.md")
pre = open(PRE).read()
P(f"  prereg sha256 {hashlib.sha256(pre.encode()).hexdigest()} (read only)")
for s in ("g_ext,obs = 1.778e-10", "Vc^2/R0 = 2.078e-10", "1.6–2.6e-31", "3 × 10⁻⁴", "γ_v = 1.000 (exactly Newtonian)", "γ = 1.000"):
    P(f"    prereg contains '{s}': {s in pre}")
SIG_TOT = 0.1614 / 5.8
P(f"  sigma_tot derived from the prereg's Arm A row: 0.1614/5.8 = {SIG_TOT:.4f}")


def tide(p, R=R0, with_disc=True):
    """Galactic tidal eigenvalues at the Sun (s^-2): radial, azimuthal, vertical (Poisson)."""
    conv = (1e3 / KPC_M) ** 2                              # (km/s/kpc)^2 -> s^-2
    gR = lambda RR: float(p.vc_plane(np.array([RR]))[0] ** 2 / RR)
    e = 1e-3
    lR = -(gR(R * (1 + e)) - gR(R * (1 - e))) / (2 * R * e)
    lP = gR(R) / R
    rb = p.rho_b_mid(R)[0]
    rd = p.rho_dark_mid(R)[0] if with_disc else float(p.rho_dark(np.array([R]))[0])
    lZ = 4 * math.pi * G * (rb + rd) - (-lR) - lP
    return dict(radial=-lR * conv, azim=lP * conv, vertical=lZ * conv, rho_tot=(rb + rd) / PC3)


def dark_tide(p, with_disc=True):
    conv = (1e3 / KPC_M) ** 2
    if p.kind == "F" and with_disc:
        return 4 * math.pi * G * p.rho_dark_mid(R0)[0] * conv
    Md = float(p.Mdark(np.array([R0]))[0]); rd = float(p.rho_dark(np.array([R0]))[0])
    return max(abs(4 * math.pi * G * rd - 2 * G * Md / R0 ** 3), G * Md / R0 ** 3) * conv


DR4 = {}
for key in CELLS:
    tr = FW[key] if not MUT else NF[key][0]
    t_sph, t_disc = dark_tide(tr, False), dark_tide(tr, True)
    r30 = 30e3 * 1.495978707e11; gint = 6.674e-11 * 1.5 * 1.989e30 / r30 ** 2
    gN = float(tr.gN_plane(np.array([R0]))[0]) * 1e6 / KPC_M
    gobs = float(tr.vc_plane(np.array([R0]))[0] ** 2 / R0) * 1e6 / KPC_M
    DR4[clab(key)] = dict(phantom_tide_sph=t_sph, phantom_tide_with_disc=t_disc, tide_over_internal_30kAU=t_disc * r30 / gint,
                          gN_R0=gN, yN=gN / A0_SI[key[0]], gobs_model=gobs)
    P(f"  {clab(key)}: phantom tide spherical {t_sph:.2e}, with phantom disc {t_disc:.2e} s^-2 (prereg 1.6-2.6e-31); tide/internal at "
      f"30 kAU (1.5 Msun) {t_disc * r30 / gint:.1e} (prereg ~3e-4); model g_N(R0) {gN:.3e} (y_N {gN / A0_SI[key[0]]:.3f}), "
      f"model g_obs(R0) {gobs:.3e} vs frozen 1.778e-10 / 2.078e-10")
NUM["dr4"] = DR4
# Bias for DR4 rows.  Arm C / settling: gamma = 1.000 structurally -> the MW model enters only through the tide term.
cells = []
for key in CELLS:
    d = DR4[clab(key)]
    nf = NF[key][0]
    t_nf = dark_tide(nf, True) * (30e3 * 1.495978707e11) / (6.674e-11 * 1.5 * 1.989e30 / (30e3 * 1.495978707e11) ** 2)
    b = (t_nf - d["tide_over_internal_30kAU"]) * 0.5         # gamma_v ~ sqrt(1 + delta g/g): delta gamma ~ delta/2 at most
    if MUT:
        b = 0.0
    cells.append((f"{clab(key)} [tide/internal F {d['tide_over_internal_30kAU']:.1e} vs N-F {t_nf:.1e}]", b / SIG_TOT, b))
row("d1", "DR4 Arm C / settling (gamma = 1.000): the MW-model tide's maximum effect on gamma_v at 30 kAU", cells,
    f"sigma_tot {SIG_TOT:.4f} (prereg)", "DR4 Arm C, Amendment 21 (decisive)")
cells = []
for key in CELLS:
    d = DR4[clab(key)]
    # Arms A/B take the OBSERVED g_ext (frozen, profile-independent); the MW model could shift only a model-based g_ext.
    gF = d["gobs_model"]; gN_ = NF[key][0].vc_plane(np.array([R0]))[0] ** 2 / R0 * 1e6 / KPC_M
    frac = (gN_ - gF) / gF if not MUT else 0.0
    cells.append((f"{clab(key)} [model g_obs F {gF:.3e} vs N-F {gN_:.3e}]", frac / 0.16, frac))
row("d2", "DR4 Arms A/B: the model g_ext at the Sun, N-F vs framework, against the prereg's own g_ext bracket (1.778 -> 2.078: 16%)",
    cells, "the 16% bracket between the two frozen conventions (proxy; the arms use the OBSERVED g_ext)", "DR4 Arms A/B")

# ---------------------------------------------------------------- (e) microlensing
P("\n(e) MICROLENSING OPTICAL DEPTH (halo only); directions and distances RECALLED")
G_C2 = G / 299792.458 ** 2                                   # kpc/Msun


def tau_los(rho_fn, l, b, L, Rsun=R0):
    l, b = math.radians(l), math.radians(b)
    def integrand(D):
        x = Rsun - D * math.cos(b) * math.cos(l); y = D * math.cos(b) * math.sin(l); z = D * math.sin(b)
        r = math.sqrt(x * x + y * y + z * z)
        return float(rho_fn(r)) * D * (L - D) / L
    return 4 * math.pi * G_C2 * quad(integrand, 1e-3, L, limit=400)[0]


SMOD = lambda r: 0.0079 * PC3 * (8.5 ** 2 + 5.0 ** 2) / (r ** 2 + 5.0 ** 2)
LOS = {"LMC": (280.46, -32.89, 49.97), "SMC": (302.8, -44.3, 62.0), "Baade": (1.0, -3.9, 8.5)}
TAU = {}
for tgt, (l, b, L) in LOS.items():
    tS = tau_los(SMOD, l, b, L, Rsun=8.5)
    TAU[tgt] = {"S-model": tS}
    for key in CELLS:
        f = FW[key]
        TAU[tgt][clab(key)] = tau_los(lambda r, f=f: f.rho_dark(np.array([r]))[0], l, b, L)
        TAU[tgt]["NF " + clab(key)] = tau_los(lambda r, n=NF[key][0]: n.rho_dark(np.array([r]))[0], l, b, L)
    P(f"  {tgt}: S-model {tS:.3e}; " + "; ".join(f"{k} {v:.3e}" for k, v in TAU[tgt].items() if k != "S-model"))
NUM["tau"] = TAU
for tgt in ("LMC", "SMC"):
    for ref in ("S-model", "N-F"):
        cells = []
        for key in CELLS:
            tF = TAU[tgt][clab(key)]
            tA = TAU[tgt]["S-model"] if ref == "S-model" else TAU[tgt]["NF " + clab(key)]
            if MUT:
                tF = tA
            frac = tF / tA - 1                                # f_inferred(assumed) / f_true - 1 = tau_true/tau_assumed - 1
            cells.append((f"{clab(key)} [tau F {tF:.2e} vs {ref} {tA:.2e}]", frac / 0.25, frac))
        row(f"e-{tgt}-{ref}", f"{tgt} compact-object halo fraction bound if the {ref} halo is assumed", cells,
            "25% halo-model systematic (recalled)", "PBH reading (CFG510)")

# ---------------------------------------------------------------- (f) streams
P("\n(f) STREAMS: V_c at stream radii, and the flattening of the non-baryonic force at r = 14 kpc, 45 deg")
for nm, rr_ in (("GD-1", 14.0), ("Pal 5", 19.0), ("Orphan 40", 40.0), ("Orphan 60", 60.0), ("Sgr 100", 100.0)):
    cells = []
    for key in CELLS:
        tr, nf = nf_of(key)
        vt, va = tr.vc_sph(np.array([rr_]))[0], nf.vc_sph(np.array([rr_]))[0]
        cells.append((f"{clab(key)} [V_c F {vt:.1f} vs N-F {va:.1f}]", (va / vt - 1) / 0.02, va / vt - 1))
    row(f"f-Vc-{nm}", f"Stream V_c at {nm} ({rr_:.0f} kpc): N-F vs framework", cells, "2% (recalled stream precision)", "streams")
QF = {}
cells = []
for key in CELLS:
    tr = FW[key] if not MUT else NF[key][0]
    Rq = zq = 14.0 / math.sqrt(2)
    gR, gz = tr.dark_force(Rq, zq)
    q = math.sqrt((zq / Rq) * (gR / gz))
    QF[clab(key)] = q
    cells.append((f"{clab(key)} [q_F {q:.3f} vs spherical NFW 1]", (1.0 - q) / 0.05, 1.0 - q))
row("f-q", "Halo flattening at GD-1 (14 kpc): a spherical-NFW analysis (q = 1) vs the framework's phantom force", cells,
    "0.05 (recalled; Bovy+16 0.94 +- 0.05, Koposov+10 0.87 +0.07/-0.04)", "streams; a framework TEST vs measured q")
NUM["q_flattening"] = QF

# ---------------------------------------------------------------- (g) Solar system
P("\n(g) SOLAR SYSTEM: Galactic tidal tensor at the Sun, framework (with phantom disc) vs N-F; Cassini Q2 = (3 +- 3)e-27 s^-2 (PAPER44)")
SS = {}
cells_q, cells_v = [], []
for key in CELLS:
    tr, nf = nf_of(key)
    tF, tN = tide(tr), tide(nf)
    dn = math.sqrt(sum((tF[k] - tN[k]) ** 2 for k in ("radial", "azim", "vertical")))
    SS[clab(key)] = dict(framework=tF, nfw=tN, diff_norm=dn)
    P(f"  {clab(key)}: F tide (R, phi, z) = ({tF['radial']:.2e}, {tF['azim']:.2e}, {tF['vertical']:.2e}) s^-2, rho_0,tot {tF['rho_tot']:.4f}; "
      f"N-F ({tN['radial']:.2e}, {tN['azim']:.2e}, {tN['vertical']:.2e}), rho_0,tot {tN['rho_tot']:.4f}; |diff| {dn:.2e}")
    cells_q.append((clab(key), dn / 3e-27, dn / 3e-27))
    cells_v.append((f"{clab(key)} [4piG rho_0 F/N-F]", (tN["rho_tot"] / tF["rho_tot"] - 1) / 0.20, tN["rho_tot"] / tF["rho_tot"] - 1))
row("g1", "Cassini Q2: Galactic tidal-tensor difference (N-F vs framework)", cells_q, "Cassini 3e-27 s^-2 (PAPER44)",
    "no-EFE claims (PAPER44), Solar system")
row("g2", "Vertical Galactic tide (Oort cloud / detached TNO secular models): 4 pi G rho_0,total, N-F vs framework", cells_v,
    "20% (recalled local-density precision)", "PAPER44 TNO run (Galactic tide term)")
NUM["solar"] = SS

# ---------------------------------------------------------------- (h) EFE rival host field
P("\n(h) EFE-RIVAL HOST FIELD at satellite distances: g_ext = G M(<r)/r^2, N-F vs framework")
for rr_ in (50.0, 100.0, 200.0):
    cells = []
    for key in CELLS:
        tr, nf = nf_of(key)
        gt, ga = tr.M_enc(np.array([rr_]))[0], nf.M_enc(np.array([rr_]))[0]
        dls = -0.5 * math.log10(ga / gt)
        cells.append((f"{clab(key)} [g_ext N-F/F {ga / gt:.3f}]", dls / 0.1, ga / gt - 1))
    row(f"h-{rr_:.0f}", f"EFE rival's deep-regime satellite dispersion at {rr_:.0f} kpc: shift from the host model", cells,
        "0.1 dex (recalled dwarf dispersion error)", "no-EFE claims (satellite EFE rival)")


# ================================================================================================ ADDED AFTER THE FIRST RUN (reported, labelled)
banner("ADDED AFTER THE FIRST RUN (reported only; no verdict input): framework TESTS the bias rows exposed")
P("  These lines were added after run 1 printed the profile (edge 50-61 kpc at f_ret = 1, not the ~175 kpc of the pre-freeze mental note,")
P("  which used a wrong r_M of ~30 kpc; the true r_M is 8.6-10.4 kpc).  They score the framework's own MW against on-disk numbers.")
POST = {}
# (1) CFG433's satellite V_c at 78 kpc under each profile
for key in CELLS + [(f, MB_PRIM, None) for f in FOOTS] + [(f, MB_HI, fr) for f in FOOTS for fr in FRETS + (None,)]:
    v = float(FW[key].vc_sph(np.array([78.0]))[0])
    POST[f"cfg433_D|{clab(key)}"] = (231.9 - v) / 21.4
    P(f"  CFG433 V_c,obs 231.9 +- 21.4 at 78 kpc vs {clab(key):38s}: V_F {v:6.1f} -> D = {(231.9 - v) / 21.4:+.2f} sigma")
# (2) unbound satellites (E >= 0, central values)
for key in ["N-B08", "N-B16"] + CELLS + [(f, MB_PRIM, None) for f in FOOTS]:
    nub = sum(not np.isfinite(ORB[n][key][1]) for n in NAMES)
    n300 = sum(ORB[n][key][1] > 300 for n in NAMES)
    POST[f"unbound|{key}"] = nub
    P(f"  Fritz sample (39): unbound at central values in {str(key):38s}: {nub:2d}; apo > 300 kpc or unbound: {n300:2d}")
# (3) the f_ret the LG timing would need (O-MW), post hoc diagnostic, NOT a fit and not used anywhere
def vp_fret(foot, fr):
    mw = Prof("mw", Mb=MB_PRIM, foot=foot, fret=fr); m31 = Prof("m31", Mb=MB_M31, foot=foot, fret=fr, point=True)
    return v_pred(lambda d: G * float(mw.M_enc(np.array([d]))[0] + m31.M_enc(np.array([d]))[0]) / d ** 2)
for foot in FOOTS:
    try:
        fr = brentq(lambda lf: vp_fret(foot, 10 ** lf) - VR_LG, math.log10(0.1), math.log10(0.9), xtol=1e-4)
        POST[f"lg_fret_needed|{foot}"] = 10 ** fr
        P(f"  LG timing (O-MW, Lambda): the f_ret that gives -109.3 km/s is {10 ** fr:.3f} ({foot}); the census value is 0.18 -- post hoc, not a fit")
    except ValueError:
        P(f"  LG timing: no f_ret in 0.1-0.9 gives -109.3 ({foot})")
# (4) the framework's total midplane density with a RECALLED local baryon density (conditional on the phantom disc)
for foot in FOOTS:
    f = FW[(foot, MB_PRIM, 1.0)]
    nu0 = float(nu_mono(f.gN_plane(np.array([R0]))[0] / f.a0)); t2 = f.rho_dark_mid(R0)[2] / PC3
    for rb in (0.084,):
        rt = nu0 * rb + t2
        POST[f"rho0_tot|{foot}"] = rt
        P(f"  local total midplane density, recalled rho_b {rb} (UNVERIFIED): framework with phantom disc {rt:.3f} Msun/pc^3 (nu {nu0:.3f}); "
          f"without the phantom disc (spherical cold only) {rb + float(f.rho_dark(np.array([R0]))[0]) / PC3:.3f}; recalled measured total ~0.10 +- 0.01 "
          f"-> {(rt - 0.10) / 0.01:+.1f} / {(rb + float(f.rho_dark(np.array([R0]))[0]) / PC3 - 0.10) / 0.01:+.1f} sigma (UNVERIFIED inputs)")
# (5) realisation caveat: in-plane V_c if the cold energy is spherical (not a phantom disc)
for foot in FOOTS:
    for Mb in (MB_PRIM, MB_HI):
        f = FW[(foot, Mb, 1.0)]
        for R in (R0, 20.0):
            a = np.array([R])
            v_law = float(f.vc_plane(a)[0]); v_sph = float(np.sqrt(R * f.gN_plane(a)[0] + G * f.Mdark(a)[0] / R))
            POST[f"vc_inplane_vs_sph|{foot}|{Mb:.1e}|{R}"] = (v_law, v_sph)
            P(f"  {foot:9s} M_b {Mb:.1e} R {R:5.2f}: in-plane law V_c {v_law:6.1f}; disc baryons + SPHERICAL cold energy {v_sph:6.1f} km/s ({v_sph / v_law - 1:+.1%})")
NUM["post_run"] = POST

# ================================================================================================ 5. figure
if not MUT:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
    r = np.logspace(-0.5, math.log10(500), 400)
    sty = [(FW[("canonical", MB_PRIM, 1.0)], "framework, canonical, f_ret 1", "C0", "-"),
           (FW[("canonical", MB_PRIM, 0.18)], "framework, canonical, f_ret 0.18", "C0", "--"),
           (FW[("alt", MB_PRIM, 1.0)], "framework, alt, f_ret 1", "C1", "-"),
           (FW[("alt", MB_PRIM, 0.18)], "framework, alt, f_ret 0.18", "C1", "--"),
           (NF[("canonical", MB_PRIM, 1.0)][0], "N-F (NFW fitted to framework, can)", "C2", "-"),
           (ND, "N-D (NFW fitted to Ou+24 data)", "C3", "-"),
           (LIT["N-McM (McMillan17 rho_s 0.00854, r_s 19.6)"], "McMillan17 NFW (recalled)", "C7", ":"),
           (LIT["N-std (1e12, c 10)"], "NFW 1e12, c 10 (recalled)", "k", ":")]
    for p, lab, col, ls in sty:
        rho = p.rho_dark(r) / PC3
        ax[0].loglog(r[rho > 0], rho[rho > 0], color=col, ls=ls, label=lab)
        ax[1].loglog(r, p.M_enc(r), color=col, ls=ls)
        ax[2].semilogx(r, p.vc_sph(r), color=col, ls=ls)
    rp = np.linspace(4, 30, 80)
    for p, lab, col in ((FW[("canonical", MB_PRIM, 1.0)], "in-plane law, canonical 6.0e10", "C0"), (FW[("alt", MB_HI, 1.0)], "in-plane law, alt 7.3e10", "C1"),
                        (ND, "in-plane N-D", "C3")):
        ax[2].plot(rp, p.vc_plane(rp), color=col, lw=0.9, ls=(0, (1, 1)), label=lab)
    ax[2].errorbar(R_OU, V_OU, yerr=np.hypot(E_OU, SYS_OU * V_OU), fmt="o", ms=3, color="0.3", label="Ou+24 (on disk)")
    ax[2].errorbar(R_EI, V_EI, yerr=E_EI, fmt="s", ms=2, color="0.6", label="Eilers+19 (on disk)")
    for a_ in ax:
        a_.axvline(RSPLIT, color="0.5", lw=0.8, ls="-.")
    ax[0].set_ylabel(r"$\rho_{\rm cold/dark}$ [M$_\odot$ pc$^{-3}$] (spherical)"); ax[1].set_ylabel(r"$M(<r)$ [M$_\odot$]")
    ax[2].set_ylabel(r"$V_c$ [km/s]: thick $\sqrt{GM(<r)/r}$, dotted in-plane")
    for a_ in ax:
        a_.set_xlabel("r [kpc]")
    ax[0].set_ylim(1e-7, 1); ax[2].set_ylim(100, 300)
    ax[0].legend(fontsize=6.5, loc="lower left"); ax[2].legend(fontsize=7)
    fig.suptitle("CFG513: the Milky Way's cold energy (framework, M_b 6.0e10) vs NFW; f_ret 1 density is zero beyond its 50-55 kpc edge; dash-dot = r_split (LG-owned beyond)", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "cfg513_profile.png"), dpi=130)
    P("\n  figure: cfg513_profile.png")

# ================================================================================================ 6. MUTATE and summary
banner("5. SUMMARY: the bias table (worst cell per row)")
for r_ in ROWS:
    P(f"  {r_['key']:16s} {r_['verdict']:9s} b/sigma {r_['b_sigma_min']:+7.2f} .. {r_['b_sigma_max']:+7.2f}   {r_['label']}")
if MUT:
    mx = max(max(abs(c["b_sigma"]) for c in r_["cells"]) for r_ in ROWS)
    allnone = all(r_["verdict"] == "NONE" for r_ in ROWS)
    check("MUTATE: truth = the assumed NFW in every row -> every bias vanishes (max |b/sigma| <= 1e-3) and every verdict is NONE",
          f"max |b/sigma| {mx:.2e}; all NONE {allnone}", mx <= 1e-3 and allnone)

lb = [c for c in CHECKS if c["load_bearing"]]
nf_ = sum(not c["ok"] for c in lb)
P(f"\n  {sum(c['ok'] for c in CHECKS)}/{len(CHECKS)} checks pass; load-bearing failures: {nf_}   ({time.time() - T0:.0f} s)")


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    return o


json.dump(jclean(dict(slug=SLUG, checks=CHECKS, rows=ROWS, numbers=NUM)), open(os.path.join(HERE, ("cfg513_results_MUTATE.json" if MUT else "cfg513_results.json")), "w"), indent=1)
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LINES) + "\n")
sys.exit(1 if nf_ else 0)
