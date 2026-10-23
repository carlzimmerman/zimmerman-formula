"""X5_mw_joint_baryons shared library (criteria FROZEN_CRITERIA.md, commit 8e5b65bca5).

* P4's MW machinery, used READ-ONLY: `p4_solver.py` is imported and P4's own T4 definitions are executed from
  `p4_v3_galaxy_tiles.py` (the module-level block from `R0_MW = 8.122` to `if want("T4"):` and the data / mw_grid / mw_obs
  part of that block).  P4's script itself is never run (it would overwrite P4's outputs).
* The declared baryon family of question (i): McMillan17 gas and disc vertical structure, both stellar discs with one
  radial scale length R_d normalised to the local column Sigma_b(R0) (discs + gas, all z), McMillan17's bulge shape
  rescaled to the bar + bulge mass M_bb.
* The frozen grid and pass lines.
Nothing here writes outside this lane (PYTHONDONTWRITEBYTECODE is set before any import from another lane).
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed.
"""
import os
import sys
import math
import time
import json
import resource
import importlib
import numpy as np
from scipy.stats import chi2 as CHI2
from scipy.integrate import quad

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data")
CFGD = os.path.join(REPO, "campaign_fresh_gravity")
P4DIR = os.path.join(REPO, "rebuild_2026_10_22", "P4_v3_galaxy_tiles")
S3DIR = os.path.join(REPO, "rebuild_2026_10_22", "S3_v3_mw_seals")
U1DIR = os.path.join(REPO, "rebuild_2026_10_22", "U1_v3_dust_content")
FOOTS = ("canonical", "alt")
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
CRITERIA = "8e5b65bca5"

# ------------------------------------------------------------------ frozen grid and lines (FROZEN_CRITERIA §2)
SIG_B_GRID = [40.3, 43.7, 47.1, 50.5, 53.9]                     # Msun/pc^2, McKee+15 47.1 +- 3.4
MBB_GRID = [1.64e10, 1.76e10, 1.88e10, 2.00e10, 2.12e10]       # Msun, Portail+17 1.88 +- 0.12 (PROVISIONAL)
RD_GRID = [2.6 + k * 0.5 / 1.5 for k in range(-3, 4)]           # kpc, BH&G16 2.6 +- 0.5, +-2 sigma in 2/3 sigma steps
LSTAR_SCORED_KPC = 0.024
LINE_CHI2 = float(CHI2.ppf(0.99, 43))
VC_BRIEF, VC_BRIEF_LINE = 229.1, 9.2
MSTAR_TAG = (3.80e10, 8.36e10)                                   # Licquia & Newman 2015 6.08 +- 1.14, +-2 sigma
RD_TAG = (2.38, 2.90)                                            # Licquia & Newman 2016 2.64 +- 0.13, +-2 sigma


def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6      # macOS: bytes


# ------------------------------------------------------------------ P4 machinery (read-only)
def load_p4():
    """returns a namespace dict with P4's solver module `S` and P4's T4 definitions."""
    sys.path.insert(0, P4DIR)
    PS = importlib.import_module("p4_solver")
    src = open(os.path.join(P4DIR, "p4_v3_galaxy_tiles.py")).read()
    seg1 = "R0_MW = 8.122" + src.split("\nR0_MW = 8.122", 1)[1].split('\nif want("T4"):', 1)[0]
    blk = src.split('\nif want("T4"):', 1)[1].split("    T4 = dict(LINE_chi2_0p99", 1)[0]
    blk = "\n".join(l for l in blk.split("\n") if not l.strip().startswith("P(")) # drop P4's print line
    seg2 = "\n".join(l[4:] if l.startswith("    ") else l for l in blk.split("\n"))
    ns = dict(os=os, math=math, np=np, S=PS, DATA=DATA, CHI2=CHI2)
    exec(compile(seg1, "p4_T4_defs", "exec"), ns)
    exec(compile(seg2, "p4_T4_block", "exec"), ns)
    return ns


class Family:
    """the declared baryon family (FROZEN_CRITERIA §2), built on P4's McMillan17 constants."""

    def __init__(self, ns):
        self.ns = ns
        R0 = ns["R0_MW"]
        self.R0 = R0
        self.sig_thin_mcm = ns["S0_THIN"] * math.exp(-R0 / ns["RD_THIN"])          # Msun/kpc^2
        self.sig_thick_mcm = ns["S0_THICK"] * math.exp(-R0 / ns["RD_THICK"])
        self.f_thin = self.sig_thin_mcm / (self.sig_thin_mcm + self.sig_thick_mcm)
        self.sig_gas_R0 = ns["S0_HI"] * math.exp(-4.0 / R0 - R0 / 7.0) + ns["S0_H2"] * math.exp(-12.0 / R0 - R0 / 1.5)
        self.sig_b_mcm = (self.sig_thin_mcm + self.sig_thick_mcm + self.sig_gas_R0) / 1e6   # Msun/pc^2
        q, r0, al, rc, rho0 = ns["Q_B"], ns["R0_B"], ns["ALPHA_B"], ns["RCUT_B"], ns["RHO0_B"]
        f = lambda r: rho0 / (1 + r / r0) ** al * math.exp(-(r / rc) ** 2) * r * r
        m = 0.0
        for a, b in ((0, 0.01), (0.01, 0.1), (0.1, 1.0), (1.0, 3.0), (3.0, 20.0)):
            m += quad(f, a, b, limit=400, epsabs=0, epsrel=1e-12)[0]
        self.M_bulge_mcm = 4 * math.pi * q * m

    def params(self, sig_b, M_bb, Rd):
        ns = self.ns
        sig_star = sig_b * 1e6 - self.sig_gas_R0                                # Msun/kpc^2 at R0
        st = self.f_thin * sig_star * math.exp(self.R0 / Rd)
        sk = (1 - self.f_thin) * sig_star * math.exp(self.R0 / Rd)
        fb = M_bb / self.M_bulge_mcm
        M_thin, M_thick = 2 * math.pi * st * Rd * Rd, 2 * math.pi * sk * Rd * Rd
        return dict(st=st, sk=sk, fb=fb, Rd=Rd, M_thin=M_thin, M_thick=M_thick, M_bb=M_bb,
                    Mstar=M_thin + M_thick + M_bb, sig_star_R0=sig_star / 1e6)

    def rho(self, sig_b, M_bb, Rd):
        ns = self.ns
        p = self.params(sig_b, M_bb, Rd)
        st, sk, fb = p["st"], p["sk"], p["fb"]
        ZT, ZK = ns["ZD_THIN"], ns["ZD_THICK"]
        RHO0_B, ALPHA_B, R0_B, RCUT_B, Q_B = ns["RHO0_B"], ns["ALPHA_B"], ns["R0_B"], ns["RCUT_B"], ns["Q_B"]
        S0_HI, S0_H2 = ns["S0_HI"], ns["S0_H2"]

        def rho(R, z):
            zz = np.abs(z)
            thin = (st / (2 * ZT)) * np.exp(-zz / ZT - R / Rd)
            thick = (sk / (2 * ZK)) * np.exp(-zz / ZK - R / Rd)
            rp = np.maximum(np.sqrt(R * R + (zz / Q_B) ** 2), 1e-7)
            bulge = fb * (RHO0_B / (1 + rp / R0_B) ** ALPHA_B * np.exp(-(rp / RCUT_B) ** 2))
            Rs = np.maximum(R, 1e-6)
            hi = (S0_HI * np.exp(-4.0 / Rs - Rs / 7.0) / (4 * 0.085)) / np.cosh(np.minimum(zz / (2 * 0.085), 300)) ** 2
            h2 = (S0_H2 * np.exp(-12.0 / Rs - Rs / 1.5) / (4 * 0.045)) / np.cosh(np.minimum(zz / (2 * 0.045), 300)) ** 2
            return thin + thick + bulge + hi + h2
        return rho, p

    def gas_mass(self):
        ns = self.ns
        f = lambda R: 2 * math.pi * R * (ns["S0_HI"] * math.exp(-4.0 / R - R / 7.0) + ns["S0_H2"] * math.exp(-12.0 / R - R / 1.5))
        return quad(f, 1e-6, 200.0, limit=400, epsrel=1e-12)[0]


def columns(rhof, R0):
    """baryon columns at R0: all z (to 30 kpc) and |z| < 1.1 kpc, Msun/pc^2 (direct quadrature)."""
    z = np.concatenate([np.linspace(0, 1.1, 22001), np.linspace(1.1, 30.0, 30001)[1:]])
    r = rhof(np.full_like(z, R0), z)
    m11 = z <= 1.1
    s_all = 2 * np.trapz(r, z) / 1e6
    s11 = 2 * np.trapz(r[m11], z[m11]) / 1e6
    return s_all, s11


def solve_cell(ns, rhof, foot, Lam_kpc=LSTAR_SCORED_KPC, mutate=False, keep_L0=True, full=False, ge=0.0):
    """P4's T4 path for one baryon model: P4 grid, P4 quadrature, P4 Problem; returns (obs_L0, obs_L, info)."""
    PS = ns["S"]
    a0 = A0_SI[foot]
    Mu = PS.mass_unit(a0)
    Mt0 = 6.6e10 / Mu
    g = ns["mw_grid"](Mt0, full=full)
    rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4)
    Mt = float(np.sum(rho1 * g.vol)) * (1 if full else 2)
    t0 = time.time()
    pr = PS.Problem(g, rho1, Mt, ge, Lam=(0.0 if mutate else Lam_kpc), mutate=mutate)
    Phi0, res0, it0 = pr.solve_aqual()
    obs0 = ns["mw_obs"](g, Phi0, a0, ge=ge) if keep_L0 else None
    info = dict(Mb_Msun=Mt * Mu, res_L0=float(res0), it_L0=int(it0))
    if (not mutate) and Lam_kpc > 0 and ge == 0.0:
        pr.solve(U0=Phi0)
        obsL = ns["mw_obs"](g, pr.Phi, a0, ge=ge)
        info.update(res_L=float(pr.res), it_L=int(pr.it))
    else:
        obsL = obs0
        info.update(res_L=float(res0), it_L=int(it0))
    info["solve_s"] = round(time.time() - t0, 2)
    return obs0, obsL, info


def eilers_target(ns):
    vE = float(np.interp(ns["R0_MW"], ns["EIL_R"], ns["EIL_V"]))
    eE = float(np.interp(ns["R0_MW"], ns["EIL_R"], ns["EIL_E"]))
    return vE, eE


def cell_pass(chi2_kz, vc, vE, eE):
    ok = (chi2_kz <= LINE_CHI2) and (abs(vc - VC_BRIEF) <= VC_BRIEF_LINE) and (abs(vc - vE) <= 2 * eE)
    D = max(chi2_kz / LINE_CHI2, abs(vc - vE) / (2 * eE))
    return bool(ok), float(D)


def slim(obs):
    """drop the per-MAP list for compact storage (kept for the scored L* cell only)."""
    return {k: v for k, v in obs.items() if k != "K"}
