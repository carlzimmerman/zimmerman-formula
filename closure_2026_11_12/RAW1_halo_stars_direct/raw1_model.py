#!/usr/bin/env python3
"""
RAW1 model module: radial accelerations of the models in FROZEN_CRITERIA.md section D.
Baryons: McMillan 2017 spherical enclosed mass, copied (not imported) from
closure_2026_11_12/MWJ1_milky_way_joint_window/mwj1.py (function M_sph), split into stars and cold gas.
Framework line (no external field, per the 2026-11-12 owner note): g = nu(g_b / a0) g_b,
nu(y) = 1 / (1 - exp(-sqrt(y))).
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import math
import numpy as np
TRAPZ = getattr(np, "trapezoid", None) or np.trapz

G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
PC = KPC / 1000.0; MSUN_PC2 = MSUN / PC ** 2
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
MSTAR_CENSUS = 5.49e10
MSTAR_RC = {"canonical": 7.08e10, "alt": 6.42e10}

MC = dict(thin =dict(S0=896.0*MSUN_PC2, Rd=2.50*KPC, zd=0.300*KPC, Rm=0.0, vert="exp"),
          thick=dict(S0=183.0*MSUN_PC2, Rd=3.02*KPC, zd=0.900*KPC, Rm=0.0, vert="exp"),
          HI   =dict(Sfid=10.0*MSUN_PC2, Rfid=8.33*KPC, Rd=7.00*KPC, zd=0.085*KPC, Rm=4.0*KPC,  vert="sech2"),
          H2   =dict(Sfid= 2.0*MSUN_PC2, Rfid=8.33*KPC, Rd=1.50*KPC, zd=0.045*KPC, Rm=12.0*KPC, vert="sech2"))
STARS = ("thin", "thick"); GAS = ("HI", "H2")
MBULGE, ABULGE = 9.23e9 * MSUN, 0.70 * KPC

def S0_of(c): return c["S0"] if "S0" in c else c["Sfid"] / math.exp(-c["Rm"] / c["Rfid"] - c["Rfid"] / c["Rd"])
def sigma_of_R(c, R):
    R = np.maximum(np.asarray(R, float), 1e-6 * KPC); return S0_of(c) * np.exp(-c.get("Rm", 0.0) / R - R / c["Rd"])
def zcum(c, n=1201):
    zg = np.linspace(-10 * c["zd"], 10 * c["zd"], n)
    zz = (np.exp(-np.abs(zg) / c["zd"]) / (2 * c["zd"]) if c["vert"] == "exp" else 1.0 / np.cosh(zg / (2 * c["zd"])) ** 2 / (4 * c["zd"]))
    cum = np.concatenate([[0.0], np.cumsum((zz[1:] + zz[:-1]) / 2 * np.diff(zg))]); return zg, cum / cum[-1]

_MS = {}
def M_parts(r_kpc):
    """(stars, gas) spherical enclosed mass in kg at r_kpc (same integral as mwj1.M_sph)."""
    key = float(r_kpc)
    if key not in _MS:
        r = key * KPC; st = MBULGE * r ** 2 / (r + ABULGE) ** 2; gs = 0.0
        Rg = np.linspace(1e-4 * KPC, min(r, 60 * KPC), 4000); h = np.sqrt(np.maximum(r ** 2 - Rg ** 2, 0.0))
        for k, c in MC.items():
            zg, cum = zcum(c); m = float(TRAPZ(2 * np.pi * Rg * sigma_of_R(c, Rg) * np.interp(h, zg, cum), Rg))
            if k in STARS: st += m
            else: gs += m
        _MS[key] = (st, gs)
    return _MS[key]
def M_sph(r_kpc):
    s, g = M_parts(r_kpc); return s + g

def nu_fw(y): return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(y, float), 1e-14))))

# A tabulated baryon mass on a log grid (the disc integral is cut at 60 kpc as in mwj1.py; beyond, mass is flat)
RTAB = np.logspace(math.log10(0.5), math.log10(2.0e4), 700)
_TAB = None
def _tab():
    global _TAB
    if _TAB is None:
        st = np.array([M_parts(r)[0] if r <= 200 else np.nan for r in RTAB]); gs = np.array([M_parts(r)[1] if r <= 200 else np.nan for r in RTAB])
        last = np.where(RTAB <= 200)[0][-1]; st[last + 1:] = st[last]; gs[last + 1:] = gs[last]
        _TAB = (st, gs)
    return _TAB

def g_model(r_kpc, model, footing=None, a0_mult=1.0):
    """Radial acceleration (m/s^2) at r_kpc (array). model in {'FW_census','FW_rc','N','H','flat200'}."""
    r = np.asarray(r_kpc, float); rm = r * KPC
    if model == "flat200":
        return (200e3) ** 2 / rm
    if model == "H":   # DESI NFW total mass: M200c 1.19e12, c 12, h 0.6777
        h = 0.6777; H0 = 100 * h * 1e3 / (1e3 * KPC); rhoc = 3 * H0 ** 2 / (8 * math.pi * G)
        M200 = 1.19e12 * MSUN; r200 = (3 * M200 / (4 * math.pi * 200 * rhoc)) ** (1 / 3); rs = r200 / 12.0
        m = lambda x: np.log1p(x) - x / (1 + x)
        return G * M200 * m(rm / rs) / m(12.0) / rm ** 2
    st, gs = _tab()
    Ms = np.interp(np.log(r), np.log(RTAB), st); Mg = np.interp(np.log(r), np.log(RTAB), gs)
    if model == "FW_rc": Ms = Ms * MSTAR_RC[footing] / MSTAR_CENSUS
    gb = G * (Ms + Mg) / rm ** 2
    if model == "N": return gb
    a0 = A0[footing] * a0_mult
    return nu_fw(gb / a0) * gb

def M_of_g(g, r_kpc):
    return g * (np.asarray(r_kpc, float) * KPC) ** 2 / G / MSUN

if __name__ == "__main__":
    for r in (20, 30, 40, 50, 80):
        s, gg = M_parts(r)
        print(r, "stars %.3e gas %.3e" % (s / MSUN, gg / MSUN),
              "FW census can/alt [1e11]:", [round(float(M_of_g(g_model(r, "FW_census", f), r)) / 1e11, 3) for f in A0],
              "FW rc:", [round(float(M_of_g(g_model(r, "FW_rc", f), r)) / 1e11, 3) for f in A0],
              "N:", round(float(M_of_g(g_model(r, "N"), r)) / 1e11, 3), "H:", round(float(M_of_g(g_model(r, "H"), r)) / 1e11, 3))
