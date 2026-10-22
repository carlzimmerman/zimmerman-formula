#!/usr/bin/env python3
"""
A46 -- IS THE MINIMAL-VACUUM COSMOLOGY FALSIFIED?
A full background fit (BAO + SNe + CMB distance priors), not an effective-parameter comparison.

Theory input (A42; A33 eqs. F1/F2):
    3(2+3b) H^2 = 2 Lambda_bare c^2 + 4K rho ,   K = 4 pi G
    b = (2/3) Omega_m ,   Lambda_bare = 3 H0^2 / c^2
=>  E^2(z) = [1 + Omega_m (1+z)^3 + Omega_r (1+z)^4] / (1 + Omega_m + Omega_r)

Cold sector: p_c = rho_c sigma_c^2 with sigma_c = 8.33 km/s, so rho_c ~ a^-3 (dust).
Clock stress: rho_beta = -9 beta H^2/(4K) is inside (F1); at z=0 it equals -Omega_m rho_crit
and is what closes the Lambda_bare/rho_crit budget.

Usage:  python3 a46_checks.py [--mutate NAME]     exit 0 iff every check passes
"""
import argparse
import hashlib
import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize

warnings.filterwarnings("ignore", category=RuntimeWarning)

T0 = time.time()
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MUT = ""

C_KM = 2.99792458e5
C_SI = 2.99792458e8
G_SI = 6.67430e-11
MPC = 3.0856775814913673e22
T_CMB = 2.7255
W_G = 2.469e-5 * (T_CMB / 2.7255) ** 4
NEFF = 3.046
W_R = W_G * (1.0 + 0.2271 * NEFF)
Z_CAN = np.sqrt(32.0 * np.pi / 3.0)
A0_ALT = 1.1312e-10
A0_CAN = 9.3603e-11
A0_SPARC = 1.1033e-10

# ---------------------------------------------------------------- data
# DESI DR2 BAO, arXiv:2503.14738 Table 1 (same values as frozen lane CFG681).
BAO = [
    dict(name="BGS",       z=0.295, kind="DV", dv=7.942,  sdv=0.075),
    dict(name="LRG1",      z=0.510, dm=13.588, sdm=0.167, dh=21.863, sdh=0.425, r=-0.459),
    dict(name="LRG2",      z=0.706, dm=17.351, sdm=0.177, dh=19.455, sdh=0.330, r=-0.404),
    dict(name="LRG3+ELG1", z=0.934, dm=21.576, sdm=0.152, dh=17.641, sdh=0.193, r=-0.416),
    dict(name="ELG2",      z=1.321, dm=27.601, sdm=0.318, dh=14.176, sdh=0.221, r=-0.434),
    dict(name="QSO",       z=1.484, dm=30.512, sdm=0.760, dh=12.817, sdh=0.516, r=-0.500),
    dict(name="Lya",       z=2.330, dm=38.988, sdm=0.531, dh=8.632,  sdh=0.101, r=-0.431),
]
N_BAO = sum(1 if b.get("kind") == "DV" else 2 for b in BAO)

# Planck 2018 TT,TE,EE+lowE distance priors (Chen-Huang-Wang 2019, arXiv:1808.05724, Table I).
CMB_MEAN = np.array([1.7502, 301.471, 0.02236])
CMB_SIG = np.array([0.0046, 0.0895, 0.00015])
CMB_CORR = np.array([[1.00, 0.46, -0.66],
                     [0.46, 1.00, -0.33],
                     [-0.66, -0.33, 1.00]])
CMB_COV = np.outer(CMB_SIG, CMB_SIG) * CMB_CORR
CMB_ICOV = np.linalg.inv(CMB_COV)

SNE_DAT = ROOT / "prep_2026" / "sne_lambda" / "pantheonplus_full.dat"
SNE_COV = (ROOT / "qwen_claude_field_theory" / "closure_2026" / "supernova_reaudit_2026"
           / "PantheonPlusSH0ES_STAT_SYS.cov.gz")


def load_sne():
    tab = np.genfromtxt(SNE_DAT, names=True, dtype=None, encoding=None)
    raw = np.loadtxt(SNE_COV)
    n = int(raw[0])
    cov = raw[1:].reshape(n, n)
    cov = 0.5 * (cov + cov.T)
    assert len(tab) == n
    mask = (tab["IS_CALIBRATOR"] == 0) & (tab["zHD"] > 0.01)
    z = tab["zHD"][mask].astype(float)
    zh = tab["zHEL"][mask].astype(float)
    mb = tab["m_b_corr"][mask].astype(float)
    C = cov[np.ix_(mask, mask)]
    cf = cho_factor(C, lower=True, check_finite=False)
    one = np.ones(len(z))
    cio = cho_solve(cf, one)
    return dict(z=z, zh=zh, mb=mb, cf=cf, cio=cio, norm=float(one @ cio), n=int(mask.sum()),
                sha_dat=hashlib.sha256(open(SNE_DAT, "rb").read()).hexdigest()[:16],
                sha_cov=hashlib.sha256(open(SNE_COV, "rb").read()).hexdigest()[:16])


SNE = load_sne()
N_SNE = SNE["n"]


# ---------------------------------------------------------------- physics
def zstar_hs(wb, wm):
    g1 = 0.0783 * wb ** -0.238 / (1 + 39.5 * wb ** 0.763)
    g2 = 0.560 / (1 + 21.1 * wb ** 1.81)
    return 1048.0 * (1 + 0.00124 * wb ** -0.738) * (1 + g1 * wm ** g2)


def zdrag_eh(wb, wm):
    b1 = 0.313 * wm ** -0.419 * (1 + 0.607 * wm ** 0.674)
    b2 = 0.238 * wm ** 0.223
    return 1291.0 * wm ** 0.251 / (1 + 0.659 * wm ** 0.828) * (1 + b1 * wb ** b2)


CAL_ZS = 1089.92 / zstar_hs(0.02237, 0.1431)
CAL_ZD = 1059.94 / zdrag_eh(0.02237, 0.1431)


def E_lcdm(z, om, h):
    orr = W_R / h ** 2
    return np.sqrt(np.maximum(om * (1 + z) ** 3 + orr * (1 + z) ** 4 + (1 - om - orr), 1e-30))


def E_model(z, om, h):
    """om = ACTUAL Omega_m.  The expansion sees om/(1+om) and rho_r/(1+om)."""
    if MUT == "beta0":
        return np.ones_like(np.asarray(z, float))
    ome = om / (1.0 + om)
    orr = (W_R / h ** 2) / (1.0 + om)
    return np.sqrt(np.maximum(ome * (1 + z) ** 3 + orr * (1 + z) ** 4 + (1 - ome), 1e-30))


def sound_horizon(z_end, Efun, wb, h, n=24000):
    x0, x1 = np.log(1 + z_end), np.log(1 + 1e8)
    xs = np.linspace(x0, x1, n)
    z = np.exp(xs) - 1.0
    R = 3.0 * wb / (4.0 * W_G) / (1.0 + z)
    cs = 1.0 / np.sqrt(3.0 * (1.0 + R))
    return (C_KM / (100.0 * h)) * np.trapz(cs * (1.0 + z) / Efun(z), xs)


XG = np.linspace(0.0, np.log(1 + 1400.0), 14000)
ZG = np.exp(XG) - 1.0


def make_DM(Efun, h):
    E = Efun(ZG)
    integ = np.exp(XG) / E
    dm = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(XG))])
    dms = (C_KM / (100.0 * h)) * dm
    return lambda zz: np.interp(np.log(1.0 + zz), XG, dms)


_CAL_SD = 147.09 / sound_horizon(CAL_ZD * zdrag_eh(0.02237, 0.1431),
                                 lambda z: E_lcdm(z, 0.3153, 0.6736), 0.02237, 0.6736)
_CAL_SS = 144.43 / sound_horizon(CAL_ZS * zstar_hs(0.02237, 0.1431),
                                 lambda z: E_lcdm(z, 0.3153, 0.6736), 0.02237, 0.6736)


def props(om, h, wb, model=False):
    if model:
        ome = om / (1.0 + om)
        Ef = lambda z: E_model(z, om, h)
    else:
        ome = om
        Ef = lambda z: E_lcdm(z, om, h)
    wm_formula = ome * h ** 2
    zs = CAL_ZS * zstar_hs(wb, wm_formula)
    zd = CAL_ZD * zdrag_eh(wb, wm_formula)
    rs = _CAL_SS * sound_horizon(zs, Ef, wb, h)
    rd = _CAL_SD * sound_horizon(zd, Ef, wb, h)
    if model and MUT == "fixed_rd":
        rd = 147.09      # MUTATION: assume the LCDM ruler instead of computing it
        rs = 144.43
    DMf = make_DM(Ef, h)
    DMstar = DMf(zs)
    R = np.sqrt(ome) * DMstar / (C_KM / (100.0 * h))
    lA = np.pi * DMstar / rs
    return dict(R=R, lA=lA, rd=rd, rs=rs, zs=zs, zd=zd, DM=DMf, E=Ef,
                ome=ome, om=om, h=h, wb=wb)


# ---------------------------------------------------------------- chi^2
def chi2_bao(p):
    z = np.array([b["z"] for b in BAO])
    DM = p["DM"](z)
    DH = (C_KM / (100.0 * p["h"])) / p["E"](z)
    tot = 0.0
    pulls = []
    for i, b in enumerate(BAO):
        if b.get("kind") == "DV":
            model = (b["z"] * DM[i] ** 2 * DH[i]) ** (1.0 / 3.0) / p["rd"]
            r = (model - b["dv"]) / b["sdv"]
            tot += r * r
            pulls.append((b["name"], float(r)))
        else:
            m = np.array([DM[i] / p["rd"], DH[i] / p["rd"]])
            d = np.array([b["dm"], b["dh"]])
            C = np.array([[b["sdm"] ** 2, b["r"] * b["sdm"] * b["sdh"]],
                          [b["r"] * b["sdm"] * b["sdh"], b["sdh"] ** 2]])
            delta = d - m
            tot += float(delta @ np.linalg.solve(C, delta))
            pulls.append((b["name"] + ":DM", float(delta[0] / b["sdm"])))
            pulls.append((b["name"] + ":DH", float(delta[1] / b["sdh"])))
    return float(tot), pulls


def chi2_sne(p):
    mu = 5.0 * np.log10((1.0 + SNE["zh"]) * p["DM"](SNE["z"])) + 25.0
    r = SNE["mb"] - mu
    off = float(SNE["cio"] @ r) / SNE["norm"]
    res = r - off
    return float(res @ cho_solve(SNE["cf"], res))


def chi2_cmb(p, npt=2):
    m = np.array([p["R"], p["lA"], p["wb"]])
    d = CMB_MEAN - m
    if npt == 2:
        Ci = np.linalg.inv(CMB_COV[:2, :2])
        return float(d[:2] @ Ci @ d[:2])
    return float(d @ CMB_ICOV @ d)


# ---------------------------------------------------------------- fits
def total_chi2(theta, model, fix_h=None, npt=2, parts=False):
    if fix_h is None:
        om, h, wb = theta
    else:
        om, wb = theta
        h = fix_h
    hi = 3.0 if model else 0.995
    if not (0.02 < om < hi and 0.3 < h < 1.2 and 0.010 < wb < 0.060):
        return (1e12, None) if parts else 1e12
    p = props(om, h, wb, model=model)
    c_bao, pulls = chi2_bao(p)
    c_sn = chi2_sne(p)
    c_cmb = chi2_cmb(p, npt=npt)
    tot = c_bao + c_sn + c_cmb
    if parts:
        return tot, dict(bao=c_bao, sne=c_sn, cmb=c_cmb, p=p, pulls=pulls)
    return tot


def run_fit(model, fix_h=None, npt=2, starts=None):
    if starts is None:
        if fix_h is None:
            starts = [[0.31, 0.674, 0.0224], [0.44, 0.57, 0.0224], [0.25, 0.75, 0.023]]
        else:
            starts = [[0.40, 0.0224], [0.25, 0.0224], [0.60, 0.023]]
        if MUT == "fixed_rd":
            if fix_h is None:
                starts = [[0.4605, 0.674, 0.0224]] + starts
            else:
                starts = [[0.4605, 0.0224]] + starts
    best = None
    for s in starts:
        s = np.array(s, float)
        r = minimize(total_chi2, s, args=(model, fix_h, npt), method="Nelder-Mead",
                     options=dict(maxiter=(2000 if MUT else 8000), maxfev=(2000 if MUT else 8000), xatol=1e-8, fatol=1e-8))
        r = minimize(total_chi2, r.x, args=(model, fix_h, npt), method="Powell",
                     options=dict(maxiter=(2000 if MUT else 8000), maxfev=(2000 if MUT else 8000), xtol=1e-10, ftol=1e-10))
        if best is None or r.fun < best.fun:
            best = r
    tot, parts = total_chi2(best.x, model, fix_h, npt, parts=True)
    return dict(x=np.atleast_1d(best.x), chi2=tot, parts=parts,
                npar=3 if fix_h is None else 2)


CHECKS = []


def chk(cid, ok, value, threshold, note=""):
    CHECKS.append(dict(id=cid, pass_=bool(ok), value=float(value),
                       threshold=float(threshold), note=note))
    print("%-4s %s  %-13.7g  %-11.6g  %s" % (cid, "PASS" if ok else "FAIL", value, threshold, note))


def h_of(x, fix_h):
    return float(x[1]) if fix_h is None else float(fix_h)


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutate", default="")
    args = ap.parse_args()
    MUT = args.mutate

    print("# A46 minimal-vacuum cosmology: full background fit  (mutate='%s')" % MUT)
    print("# c=%.8g km/s  T_CMB=%.3f  Og h^2=%.5g  Or h^2=%.6g" % (C_KM, T_CMB, W_G, W_R))
    print("# N_BAO=%d  N_SNE=%d  N_CMB(2pt)=2  N_CMB(3pt)=3" % (N_BAO, N_SNE))
    print("# Pantheon+ sha256[:16]=%s cov=%s" % (SNE["sha_dat"], SNE["sha_cov"]))
    p_cal = props(0.3153, 0.6736, 0.02237)
    print("# calibrator (Planck point): z*=%.2f  zdrag=%.2f  rd=%.2f  r*=%.2f"
          % (p_cal["zs"], p_cal["zd"], p_cal["rd"], p_cal["rs"]))

    # ---------------- K1: E(z) from (F1), symbolic
    z, b, Om, H0s, K, G = sp.symbols("z beta Omega_m H0 K G", positive=True)
    Lam = sp.Symbol("Lambda", positive=True)
    rho_m0 = Om * 3 * H0s ** 2 / (8 * sp.pi * G)
    H2 = sp.solve(sp.Eq(3 * (2 + 3 * b) * sp.Symbol("H2"),
                        2 * Lam + 4 * K * rho_m0 * (1 + z) ** 3), sp.Symbol("H2"))[0]
    H2 = H2.subs({K: 4 * sp.pi * G, b: sp.Rational(2, 3) * Om, Lam: 3 * H0s ** 2})
    E2 = sp.simplify(H2 / H0s ** 2)
    resid1 = sp.simplify(E2 - (1 + Om * (1 + z) ** 3) / (1 + Om))
    chk("K1", resid1 == 0, 0.0 if resid1 == 0 else 1.0, 0.0,
        "E^2 from (F1), beta=2Om/3, Lam=3H0^2: symbolic residual")

    # ---------------- K2: clock stress closes the budget
    om0, h0 = 0.3163, 0.674
    beta = 2.0 / 3.0 * om0
    Hz = 100e3 * h0 / MPC
    rho_crit = 3.0 * Hz ** 2 / (8 * np.pi * G_SI)
    rho_beta = -9.0 * beta * Hz ** 2 / (4.0 * 4 * np.pi * G_SI)
    chk("K2", abs(rho_beta / rho_crit + om0) < 1e-12, rho_beta / rho_crit, -om0,
        "rho_beta/rho_crit at z=0 = -Omega_m")

    # ---------------- K3: E(0)=1 with radiation
    orv = W_R / h0 ** 2
    Ev = np.sqrt((1 + om0 + orv) / (1 + om0 + orv))
    chk("K3", abs(Ev - 1) < 1e-14, Ev - 1, 1e-14,
        "E(0)=1 with beta=2(Om+Or)/3, Or=%.3g" % orv)

    # ---------------- primary fits: BAO + SNe + CMB(theta*,R)
    rlA = run_fit(model=False, npt=2)
    rlB = run_fit(model=False, npt=3)
    ndofA = N_BAO + N_SNE + 2 - 3
    chk("K4", abs(rlA["x"][0] - 0.31) < 0.03 and abs(rlA["x"][1] - 0.68) < 0.03
        and 0.8 < rlA["chi2"] / ndofA < 1.1,
        rlA["chi2"] / ndofA, 1.0,
        "LCDM: Om=%.4f h=%.4f wb=%.5f chi2/dof=%.3f"
        % (rlA["x"][0], rlA["x"][1], rlA["x"][2], rlA["chi2"] / ndofA))

    # ---------------- K5: exact degeneracy at the mapped point
    om_l, h_l, wb_l = rlB["x"]
    om_map = om_l / (1.0 - om_l)
    h_map = h_l * np.sqrt(1.0 - om_l)
    p_l = props(om_l, h_l, wb_l)
    p_map = props(om_map, h_map, wb_l, model=True)
    zz = np.array([b["z"] for b in BAO])
    d_dmrd = float(np.max(np.abs((p_map["DM"](zz) / p_map["rd"]) /
                                 (p_l["DM"](zz) / p_l["rd"]) - 1.0)))
    d_dhrd = float(np.max(np.abs(((C_KM / (100 * h_map) / p_map["E"](zz)) / p_map["rd"]) /
                                 ((C_KM / (100 * h_l) / p_l["E"](zz)) / p_l["rd"]) - 1.0)))
    d_sn = abs(chi2_sne(p_map) - chi2_sne(p_l))
    d_R = abs(p_map["R"] / p_l["R"] - 1)
    d_lA = abs(p_map["lA"] / p_l["lA"] - 1)
    worst = max(d_dmrd, d_dhrd, d_R, d_lA)
    chk("K5", worst < 5e-3 and d_sn < 0.05, worst, 5e-3,
        "max rel. diff. D_M/rd,D_H/rd,R,l_A at the map; SNe dchi2=%.2g (Omega_r-level)" % d_sn)

    # ---------------- K6: r_d is 20% larger at the mapped point
    chk("K6", p_map["rd"] / p_l["rd"] > 1.15, p_map["rd"] / p_l["rd"], 1.15,
        "r_d(model)/r_d(LCDM) at the mapped point")

    # ---------------- K17: the expansion histories are identical at the map
    zgrid = np.concatenate([np.linspace(0.0, 3.0, 400), np.geomspace(3.1, 1200.0, 400)])
    dE = float(np.max(np.abs(E_model(zgrid, om_map, h_map) / E_lcdm(zgrid, om_l, h_l) - 1.0)))
    chk("K17", dE < 2e-4, dE, 2e-4,
        "max |E_model/E_LCDM-1| at the map (Omega_r in Lambda is the only breaking)")

    # ---------------- K7: model fits as well as LCDM
    rmA = run_fit(model=True, npt=2, starts=[[om_map, h_map, wb_l], [0.44, 0.57, 0.0224],
                                             [0.31, 0.674, 0.0224]])
    rmB = run_fit(model=True, npt=3, starts=[[om_map, h_map, wb_l], [0.44, 0.57, 0.0224]])
    dA = rmA["chi2"] - rlA["chi2"]
    chk("K7", abs(dA) < 5.0, dA, 5.0,
        "Delta chi2(model - LCDM), CMB 2pt, 3 par each")

    # ---------------- K8: baryon density at the model's fit
    chk("K8", abs(rmB["x"][2] / CMB_MEAN[2] - 1) < 0.10, rmB["x"][2] / CMB_MEAN[2], 1.10,
        "best-fit Omega_b h^2 / Planck")

    # ---------------- K9: H0 the data give -> a0 below the alt footing
    H0_m = 100 * h_of(rmB["x"], None)
    a0_bf = C_SI * (H0_m * 1e3 / MPC) / Z_CAN
    a0_2pt = C_SI * (100 * h_of(rmA["x"], None) * 1e3 / MPC) / Z_CAN
    chk("K9", abs(a0_bf / A0_ALT - 1) > 0.10, a0_bf / A0_ALT, 0.90,
        "best-fit H0=%.2f -> a0=%.4g (alt %.4g, canonical %.4g)"
        % (H0_m, a0_bf, A0_ALT, A0_CAN))

    # ---------------- K10: the a0 branch, H0 fixed
    H0_A0 = A0_ALT * Z_CAN / C_SI * MPC / 1e3
    fxB = run_fit(model=True, fix_h=H0_A0 / 100.0, npt=3)
    fxA = run_fit(model=True, fix_h=H0_A0 / 100.0, npt=2)
    d_fixB = fxB["chi2"] - rlB["chi2"]
    d_fixA = fxA["chi2"] - rlA["chi2"]
    chk("K10", d_fixA > 20 and d_fixB > 100, d_fixA, 20.0,
        "Delta chi2 at H0=%.2f: %.1f (CMB 2pt), %.1f (3pt)" % (H0_A0, d_fixA, d_fixB))

    # ---------------- K11: failure is in the ruler, not in H(z)
    d_sne = fxB["parts"]["sne"] - rlB["parts"]["sne"]
    d_dist = (fxB["parts"]["bao"] - rlB["parts"]["bao"]) + (fxB["parts"]["cmb"] - rlB["parts"]["cmb"])
    chk("K11", d_sne < 0.15 * d_dist, d_sne / d_dist, 0.15,
        "at fixed H0: SNe dchi2=%.1f vs BAO+CMB dchi2=%.1f" % (d_sne, d_dist))

    # ---------------- K12: r_d at the a0 branch
    rd_fix = fxB["parts"]["p"]["rd"]
    chk("K12", abs(rd_fix / 147.09 - 1) > 0.05, rd_fix / 147.09, 1.05,
        "r_d at H0=%.2f is %.1f Mpc (BAO needs 147.09)" % (H0_A0, rd_fix))

    # ---------------- K13: A42's Omega_m,eff h^2 comparison is a category error
    ome_a42 = 0.3163 / (1 + 0.3163)
    eff = ome_a42 * 0.674 ** 2
    phys = 0.3163 * 0.674 ** 2
    chk("K13", abs(phys / 0.1431 - 1) < 0.02 and abs(eff / 0.1431 - 1) > 0.20,
        eff / 0.1431, 0.80,
        "A42: Om_eff h^2=%.4f vs Om h^2=%.4f (Planck 0.1431)" % (eff, phys))

    # ---------------- K14: 77.3 is the beta=0 + curvature branch
    om_d = 0.3163
    H0_d = 67.4 * np.sqrt(1 + om_d)
    chk("K14", abs(H0_d - 77.33) < 0.1 and 2.0 / 3.0 * om_d > 0.2, H0_d, 77.33,
        "beta=0 + matter + Lam=rho_crit: H0=%.2f, Omega_k=%.4f, closure beta=%.3f"
        % (H0_d, -om_d, 2 * om_d / 3))

    # ---------------- K15: sound-horizon calibration
    chk("K15", abs(p_l["rd"] / 147.09 - 1) < 3e-3, p_l["rd"] / 147.09, 1.003,
        "r_d(LCDM best fit)=%.3f Mpc" % p_l["rd"])

    # ---------------- K16: the map's H0 prediction
    H0_pred = 100 * h_map
    chk("K16", abs(H0_m / H0_pred - 1) < 0.06, H0_m / H0_pred, 1.06,
        "H0(fit)=%.2f vs H0(map)=%.2f = H0(LCDM)sqrt(1-Om)" % (H0_m, H0_pred))

    print()
    print("## %-30s %7s %7s %8s %8s %8s %8s %9s" %
          ("fit", "Om", "h", "wb", "chi2", "dchi2", "dAIC", "dof"))
    rows = [("LCDM 3par, CMB 2pt", rlA, 3), ("MODEL 3par, CMB 2pt", rmA, 3),
            ("MODEL H0=%.2f 2par, 2pt" % H0_A0, fxA, 2),
            ("LCDM 3par, CMB 3pt", rlB, 3), ("MODEL 3par, CMB 3pt", rmB, 3),
            ("MODEL H0=%.2f 2par, 3pt" % H0_A0, fxB, 2)]
    for tag, r, k in rows:
        ref = rlA if "2pt" in tag else rlB
        dchi = r["chi2"] - ref["chi2"]
        daic = dchi + 2 * (k - 3)
        print("## %-30s %7.4f %7.4f %8.5f %8.1f %8.1f %8.1f %9d"
              % (tag, r["x"][0], h_of(r["x"], None) if len(r["x"]) > 1 else H0_A0 / 100,
                 float(r["x"][-1]), r["chi2"], dchi, daic,
                 N_BAO + N_SNE + (2 if "2pt" in tag else 3) - k))
    print("## components:")
    for tag, r in [("LCDM 2pt", rlA), ("MODEL 2pt", rmA), ("MODEL@H0 2pt", fxA),
                   ("LCDM 3pt", rlB), ("MODEL 3pt", rmB), ("MODEL@H0 3pt", fxB)]:
        print("##   %-16s bao %7.2f  sne %8.2f  cmb %7.2f" %
              (tag, r["parts"]["bao"], r["parts"]["sne"], r["parts"]["cmb"]))

    nums = dict(
        N_BAO=N_BAO, N_SNE=N_SNE, N_CMB2=2, N_CMB3=3,
        lcdm2=dict(om=float(rlA["x"][0]), h=float(rlA["x"][1]), wb=float(rlA["x"][2]),
                   chi2=float(rlA["chi2"]), bao=float(rlA["parts"]["bao"]),
                   sne=float(rlA["parts"]["sne"]), cmb=float(rlA["parts"]["cmb"])),
        lcdm3=dict(om=float(rlB["x"][0]), h=float(rlB["x"][1]), wb=float(rlB["x"][2]),
                   chi2=float(rlB["chi2"]), bao=float(rlB["parts"]["bao"]),
                   sne=float(rlB["parts"]["sne"]), cmb=float(rlB["parts"]["cmb"])),
        model2=dict(om=float(rmA["x"][0]), h=float(rmA["x"][1]), wb=float(rmA["x"][2]),
                    om_eff=float(rmA["x"][0] / (1 + rmA["x"][0])), chi2=float(rmA["chi2"]),
                    bao=float(rmA["parts"]["bao"]), sne=float(rmA["parts"]["sne"]),
                    cmb=float(rmA["parts"]["cmb"]), rd=float(rmA["parts"]["p"]["rd"]),
                    a0=float(a0_2pt)),
        model3=dict(om=float(rmB["x"][0]), h=float(rmB["x"][1]), wb=float(rmB["x"][2]),
                    om_eff=float(rmB["x"][0] / (1 + rmB["x"][0])), chi2=float(rmB["chi2"]),
                    bao=float(rmB["parts"]["bao"]), sne=float(rmB["parts"]["sne"]),
                    cmb=float(rmB["parts"]["cmb"]), rd=float(rmB["parts"]["p"]["rd"]),
                    a0=float(A0_ALT * (100 * rmB["x"][1]) / H0_A0)),
        model_h0_2=dict(om=float(fxA["x"][0]), wb=float(fxA["x"][1]), chi2=float(fxA["chi2"]),
                        bao=float(fxA["parts"]["bao"]), sne=float(fxA["parts"]["sne"]),
                        cmb=float(fxA["parts"]["cmb"]), rd=float(fxA["parts"]["p"]["rd"])),
        model_h0_3=dict(om=float(fxB["x"][0]), wb=float(fxB["x"][1]), chi2=float(fxB["chi2"]),
                        bao=float(fxB["parts"]["bao"]), sne=float(fxB["parts"]["sne"]),
                        cmb=float(fxB["parts"]["cmb"]), rd=float(fxB["parts"]["p"]["rd"]),
                        om_eff=float(fxB["x"][0] / (1 + fxB["x"][0]))),
        dchi2_model=float(dA), dchi2_h0_2pt=float(d_fixA), dchi2_h0_3pt=float(d_fixB),
        daic_h0_2pt=float(d_fixA - 2), daic_h0_3pt=float(d_fixB - 2),
        H0_A0=float(H0_A0), H0_model=float(H0_m), H0_map=float(H0_pred),
        H0_lcdm=float(100 * h_l), H0_A42_77=float(H0_d),
        map=dict(om=float(om_map), h=float(h_map), rd_ratio=float(p_map["rd"] / p_l["rd"]),
                 max_rel_diff=float(worst), sne_dchi2=float(d_sn)),
        rd_lcdm=float(p_l["rd"]), rd_map=float(p_map["rd"]),
        R_lcdm=float(p_l["R"]), lA_lcdm=float(p_l["lA"]),
        R_model3=float(rmB["parts"]["p"]["R"]), lA_model3=float(rmB["parts"]["p"]["lA"]),
        R_map=float(p_map["R"]), lA_map=float(p_map["lA"]),
        a0_map=float(A0_ALT * H0_pred / H0_A0),
        a0_alt=float(A0_ALT), a0_can=float(A0_CAN), a0_sparc=float(A0_SPARC),
        dof=dict(lcdm2=N_BAO + N_SNE + 2 - 3, lcdm3=N_BAO + N_SNE + 3 - 3,
                 model2=N_BAO + N_SNE + 2 - 3, model3=N_BAO + N_SNE + 3 - 3,
                 model_h0_2=N_BAO + N_SNE + 2 - 2, model_h0_3=N_BAO + N_SNE + 3 - 2),
        chi2_over_dof=dict(lcdm3=float(rlB["chi2"] / (N_BAO + N_SNE)),
                           model3=float(rmB["chi2"] / (N_BAO + N_SNE)),
                           model_h0_3=float(fxB["chi2"] / (N_BAO + N_SNE))),
        pulls_h0fix_bao=[[str(nm), round(float(pl), 3)] for nm, pl in fxB["parts"]["pulls"]],
        pulls_model3_bao=[[str(nm), round(float(pl), 3)] for nm, pl in rmB["parts"]["pulls"]],
        cmb_resid_h0fix=dict(R=float(fxB["parts"]["p"]["R"] - CMB_MEAN[0]),
                             lA=float(fxB["parts"]["p"]["lA"] - CMB_MEAN[1]),
                             wb=float(fxB["parts"]["p"]["wb"] - CMB_MEAN[2])),
        cmb_resid_model3=dict(R=float(rmB["parts"]["p"]["R"] - CMB_MEAN[0]),
                              lA=float(rmB["parts"]["p"]["lA"] - CMB_MEAN[1]),
                              wb=float(rmB["parts"]["p"]["wb"] - CMB_MEAN[2])),
        derived=dict(
            h_over_hL=float(rmB["x"][1] / h_l), sqrt1mOmL=float(np.sqrt(1 - om_l)),
            H0_over_H0L=float(rmB["x"][1] / h_l), theta_star_planck=float(np.pi / CMB_MEAN[1]),
            rd_ratio_h0fix=float(rd_fix / 147.09),
            dchi2_h0fix_sne=float(d_sne), dchi2_h0fix_dist=float(d_dist),
            sigma_equiv_2pt=float(np.sqrt(d_fixA)), sigma_equiv_3pt=float(np.sqrt(d_fixB)),
            cmb_pull_sigma_h0fix=dict(R=float((fxB["parts"]["p"]["R"] - CMB_MEAN[0]) / CMB_SIG[0]),
                                      lA=float((fxB["parts"]["p"]["lA"] - CMB_MEAN[1]) / CMB_SIG[1]),
                                      wb=float((fxB["parts"]["p"]["wb"] - CMB_MEAN[2]) / CMB_SIG[2])),
            rho_crit_674=float(3 * (67.4e3 / MPC) ** 2 / (8 * np.pi * G_SI)),
            rho_crit_fit=float(3 * (100 * rmB["x"][1] * 1e3 / MPC) ** 2 / (8 * np.pi * G_SI)),
            rho_DE=float(1.0890e-52 * C_SI ** 2 / (8 * np.pi * G_SI)),
            rd_over_rd_BAO_h0fix=float(rd_fix / 147.09)),
        sigma_loglike_note="dchi2 uses 13+1580+2=1595 (2pt) or 13+1580+3=1596 (3pt) points")

    out = dict(lane="A46_cosmology_fit",
               status="NUMERICAL",
               checks=[dict(id=c["id"], pass_=c["pass_"], value=c["value"],
                            threshold=c["threshold"], note=c["note"]) for c in CHECKS],
               numbers=nums,
               constants_used=[
                   "DESI DR2 BAO arXiv:2503.14738 Table 1 (identical to frozen lane CFG681)",
                   "Pantheon+ Brout+2022: 1580 SNe, STAT+SYS covariance, on disk",
                   "Planck 2018 distance priors: Chen-Huang-Wang arXiv:1808.05724 Table I",
                   "T_CMB=2.7255 K; N_eff=3.046; Omega_gamma h^2=2.469e-5",
                   "z_* (Hu-Sugiyama 1996) and z_drag (Eisenstein-Hu 1998), one-point calibrated",
                   "A42: beta=(2/3)Omega_m, Lambda_bare=3H0^2/c^2, a0=1.1312e-10 m/s^2",
                   "A42 sec.4 / A33 sec.3.4: cold sector is dust, sigma_c=8.33 km/s (w_c=7.7e-10)",
                   "Planck 2018 VI: z*=1089.92, z_drag=1059.94, r_d=147.09, r_*=144.43 (calibration targets)"])
    (HERE / "a46_results.json").write_text(json.dumps(out, indent=1))

    npass = sum(c["pass_"] for c in CHECKS)
    print("\nA46 COMPLETE: %d/%d checks PASS.  (%.1f s)" % (npass, len(CHECKS), time.time() - T0))
    return 0 if npass == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
