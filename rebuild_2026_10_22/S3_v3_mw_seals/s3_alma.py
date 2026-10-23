"""S3_v3_mw_seals Part D library: CFG571's algebraic requirement (my implementation) and the AQUAL-disc requirement.
Criteria FROZEN_CRITERIA.md §5 (8f6c6587e1) + A1, A2.  kappa = 1/2 FITTED; not theory closed."""
import os
import sys
import math
import numpy as np
from scipy.optimize import brentq
from scipy.special import i0, i1, k0, k1
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s3_aqual as S

Gk = 4.30091e-6
U = 1e6 / 3.0857e19                       # 1 (km/s)^2/kpc in m/s^2 (CFG571)
FOOT = {"canon 9.36e-11": 9.3603e-11, "alt 1.13e-10": 1.1312e-10}


def Bf(y):
    return y * y * (i0(y) * k0(y) - i1(y) * k1(y))


def v2_exp(M, Rd, R):
    return 2 * Gk * M / Rd * Bf(R / (2 * Rd))


def m_from_v2(v2, Rg, R):
    return v2 * Rg / (2 * Gk * Bf(R / (2 * Rg)))


def gbar_req(gobs, a0_si, C=1.0):
    """root of C nu1(gb/A) gb = gobs."""
    A = a0_si / U
    f = lambda gb: C * float(S.nu1(gb / A)) * gb - gobs
    return brentq(f, gobs * 1e-8 / C, gobs * (1 + 1e-12) / min(C, 1.0) + 1e-300, xtol=gobs * 1e-12, rtol=1e-12)


def alg_cell(R, Vc, Mstar, Rd, a0_si):
    gobs = Vc ** 2 / R
    vb2 = gbar_req(gobs, a0_si) * R; vs2 = v2_exp(Mstar, Rd, R); vg2 = vb2 - vs2
    d = dict(logVbar2R_G=math.log10(vb2 * R / Gk), floor=bool(vg2 <= 0))
    for gs, k in (("Rg=Rd", 1.0), ("Rg=1.5Rd", 1.5)):
        d["logMgas_" + gs] = math.log10(m_from_v2(vg2, k * Rd, R)) if vg2 > 0 else None
    return d


# ------------------------------------------------------------------ AQUAL grid per target (units kpc, scaled to R_d)
def make_grid(Rd, fine=False):
    if fine:
        return S.Grid(0.0025 * Rd, 1.035, 1000 * Rd, 0.0012 * Rd, 1.05, 1000 * Rd)
    return S.Grid(0.004 * Rd, 1.06, 1000 * Rd, 0.002 * Rd, 1.08, 1000 * Rd)


def disc_rho(g, M, Rd, thick=None):
    """exponential disc of mass M: cell-integrated Sigma; razor-thin (central layer) or sech^2(z/z0)/(2 z0)."""
    Menc = M * (1 - (1 + g.Re / Rd) * np.exp(-g.Re / Rd))
    Sig = np.diff(Menc) / (math.pi * (g.Re[1:] ** 2 - g.Re[:-1] ** 2))
    rho = np.zeros((g.nR, g.nz))
    if thick is None:
        rho[:, g.jc] = Sig / g.dz[g.jc]
    else:
        prof = 1.0 / np.cosh(g.zc / thick) ** 2 / (2 * thick)
        prof = prof / np.sum(prof * g.dz)          # discrete normalisation per column
        rho = Sig[:, None] * prof[None, :]
    return rho


class Disc:
    def __init__(self, Rd, fine=False, thick=None):
        self.g = make_grid(Rd, fine)
        self.Rd, self.thick = Rd, thick
        self.rs1 = disc_rho(self.g, 1.0, Rd, None if thick is None else thick * Rd)
        self.cache = {}

    def gas_rho(self, Rg):
        k = ("gas", Rg)
        if k not in self.cache:
            self.cache[k] = disc_rho(self.g, 1.0, Rg, None if self.thick is None else self.thick * self.Rd)
        return self.cache[k]

    def C_at(self, R, Mstar, Mgas, Rg, a0_si):
        """C = AQUAL / nu1-algebraic in-plane at R on this grid (cached)."""
        ck = (round(R, 9), Mstar, Mgas, Rg, a0_si)
        if ck in self.cache:
            return self.cache[ck]
        g = self.g
        rho = Mstar * self.rs1 + (Mgas * self.gas_rho(Rg) if Mgas > 0 else 0.0)
        M = S.total_mass(g, rho)
        a0 = a0_si / U
        PBN = S.bc_newton(g, M); PhiN = g.newton(rho, PBN)
        Phi, info = g.aqual(rho, a0, S.bc_aqual_iso(g, M, a0), Phi_init_N=PhiN, PB_N=PBN)
        gN = g.gR_plane(PhiN, np.array([R]))[0]
        gA = g.gR_plane(Phi, np.array([R]))[0]
        self.cache[ck] = (gA / (float(S.nu1(gN / a0)) * gN), info)
        return self.cache[ck]


def aqual_cell(D, R, Vc, Mstar, Rd, a0_si, alg):
    """returns dict like alg_cell for the AQUAL-disc requirement + diagnostics."""
    gobs = Vc ** 2 / R
    A = a0_si / U
    out = {"iters": {}}
    # stars alone
    Cs, info = D.C_at(R, Mstar, 0.0, Rd, a0_si)
    vs2 = v2_exp(Mstar, Rd, R)
    gs = vs2 / R
    floor = bool(Cs * float(S.nu1(gs / A)) * gs >= gobs)
    out["C_stars"] = Cs
    out["floor"] = floor
    if floor:
        # the requirement on V_bar (FLOOR: stars exceed it); reported with C at the stars-only configuration
        gb = gbar_req(gobs, a0_si, Cs)
        out["logVbar2R_G"] = math.log10(gb * R * R / Gk)
        out["logMgas_Rg=Rd"] = out["logMgas_Rg=1.5Rd"] = None
        out["C_final"] = {"Rg=Rd": Cs, "Rg=1.5Rd": Cs}
        return out
    out["C_final"] = {}
    for gsn, k in (("Rg=Rd", 1.0), ("Rg=1.5Rd", 1.5)):
        Rg = k * Rd
        lmg = alg["logMgas_" + gsn]
        if lmg is None:                          # algebraic FLOOR but AQUAL not: start from the C = Cs requirement
            gb = gbar_req(gobs, a0_si, Cs); vg2 = gb * R - vs2
            lmg = math.log10(max(m_from_v2(vg2, Rg, R), 1e6))
        hist = [lmg]
        C = Cs
        for it in range(12):
            C, info = D.C_at(R, Mstar, 10 ** lmg, Rg, a0_si)
            gb = gbar_req(gobs, a0_si, C)
            vg2 = gb * R - vs2
            if vg2 <= 0:
                new = None
                break
            new = math.log10(m_from_v2(vg2, Rg, R))
            hist.append(new)
            if abs(new - lmg) <= 0.002:
                lmg = new
                break
            lmg = new
        out["logMgas_" + gsn] = lmg if new is not None else None
        out["C_final"][gsn] = C
        out["iters"][gsn] = hist
        out["logVbar2R_G_" + gsn] = math.log10(gb * R * R / Gk)
        if gsn == "Rg=Rd":
            out["logVbar2R_G"] = math.log10(gb * R * R / Gk)
    return out




def job_cell(Rd, R, Vc, Mstar, a0_si, alg, thick=None, fine=False):
    """child job: one AQUAL-disc requirement cell."""
    return aqual_cell(Disc(Rd, fine=fine, thick=thick), R, Vc, Mstar, Rd, a0_si, alg)


def job_controls(Rd):
    """child job: D2 (Freeman) and D3 (Kuzmin, A1 form) on the ALMA grid for this R_d."""
    Dd = Disc(Rd)
    g = Dd.g
    rho = 1e10 * Dd.rs1
    PhiN = g.newton(rho, S.bc_newton(g, S.total_mass(g, rho)))
    Rr = np.linspace(0.5, 5.0, 40) * Rd
    d2 = float(np.max(np.abs(g.vc2(PhiN, Rr) / v2_exp(1e10, Rd, Rr) - 1)))
    a = Rd; Mk = 1e11
    Menc = Mk * (1 - a / np.sqrt(g.Re ** 2 + a ** 2)); rk = np.zeros((g.nR, g.nz))
    rk[:, g.jc] = np.diff(Menc) / (math.pi * (g.Re[1:] ** 2 - g.Re[:-1] ** 2)) / g.dz[g.jc]
    MK = S.total_mass(g, rk); a0 = 9.3603e-11 / U
    PBN = S.bc_newton(g, MK); PN = g.newton(rk, PBN)
    PK, _ = g.aqual(rk, a0, S.bc_aqual_iso(g, MK, a0), Phi_init_N=PN, PB_N=PBN, mufun=S.mu_true)
    Rr = np.geomspace(0.3, 20, 15) * a
    gNR = Gk * MK * Rr / (Rr ** 2 + a ** 2) ** 1.5; gNm = Gk * MK / (Rr ** 2 + a ** 2)
    d3 = float(np.max(np.abs(g.gR_plane(PK, Rr) / (S.nu1(gNm / a0) * gNR) - 1)))
    return dict(d2=d2, d3=d3, nR=g.nR, nz=g.nz)
