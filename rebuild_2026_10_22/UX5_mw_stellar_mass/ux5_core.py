#!/usr/bin/env python3
"""UX5 part 1 core. Form A (P4's AQUAL), form Q (real QUMOND on the same grid and face fluxes), form R (LW1's round rule). Reads other lanes, writes only here. kappa = 1/2 FITTED; not theory closed."""
import math, os, sys
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"; sys.dont_write_bytecode = True
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np, scipy.sparse.linalg as spl
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, os.path.join(RB, "X5_mw_joint_baryons")); import x5_lib as L
ns = L.load_p4(); F = L.Family(ns); PS = ns["S"]; R0, BR_R, BR_K, BR_E5 = ns["R0_MW"], ns["BR_R"], ns["BR_K"], ns["BR_E5"]; vE, eE = L.eilers_target(ns); G = 4.30091e-6; KZU = 2 * math.pi * G * 1e6; KZ, KZE = 66.4, 2.2; LK, LO = L.LINE_CHI2, 59.89250004508689; HLIT, HE = 2.72, 0.15
ou = np.loadtxt(os.path.join(L.DATA, "mw_rc_ou2024_table1.tsv"), comments="#", skiprows=14); OR, OV = ou[:, 0], ou[:, 1]; OE = np.hypot(0.5 * (ou[:, 2] + ou[:, 3]), np.where(OR <= 22.0, 0.03, 0.15) * OV)
A0 = L.A0_SI
def nu(y, mut=False):
    if mut: return np.ones_like(y)
    return 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-300))
class Lapl:
    """one LU per grid. bo = 0 isolated Dirichlet, as P4's Problem at ge = 0."""
    def __init__(s, g): s.g = g; s.lu = spl.splu(g.Lap.tocsc())
    def newton(s, rho): return s.lu.solve(4 * math.pi * rho)
    def qumond(s, PhiN, mut=False):
        g = s.g; d = g.Dr @ PhiN; t = g.Tr @ PhiN; Fr = nu(np.hypot(d, t), mut) * d
        d2 = g.Dt @ PhiN; t2 = g.Tt @ PhiN; Ft = nu(np.hypot(d2, t2), mut) * d2
        d3 = g.Do @ PhiN; Fo = nu(np.abs(d3), mut) * d3
        return s.lu.solve(g.Divr @ Fr + g.Divt @ Ft + g.Divo @ Fo)
def lines(vc, K, K0, vo):
    K = np.asarray(K); cK = float(np.sum(((K - BR_K) / BR_E5) ** 2)); cO = float(np.sum(((np.asarray(vo) - OV) / OE) ** 2))
    A_ = np.vstack([np.ones_like(BR_R), BR_R - R0]).T; sl = np.linalg.lstsq(A_, np.log(np.maximum(K, 1e-9)), rcond=None)[0][1]; h = float(-1 / sl) if sl < 0 else float("inf")
    return dict(vc=vc, K0=K0, cK=cK, cO=cO, h=h, L1=bool(abs(vc - L.VC_BRIEF) <= L.VC_BRIEF_LINE and abs(vc - vE) <= 2 * eE), L2a=bool(cK <= LK), L2b=bool(abs(K0 - KZ) <= 2 * KZE), L3=bool(cO <= LO), Lh=bool(abs(h - HLIT) <= 2 * HE), D=max(cK / LK, abs(vc - vE) / (2 * eE), cO / LO, abs(K0 - KZ) / (2 * KZE)))
def field_lines(g, Phi, a0):
    o = ns["mw_obs"](g, Phi, a0); vo = L.vc_plane(ns, g, Phi, a0, OR); return lines(o["vc_R0"], o["K"], o["K_R0"], vo)
def rho_struct(sig_b, mbb, rd, ht=None, hk=None, fk=None, rdk=None):
    """X5's family with vertical structure varied: Sigma_b(R0) held, thick share of the stellar column at R0 fk, heights ht, hk, thick length rdk (None: tied)."""
    p = F.params(sig_b, mbb, rd); ZT = ns["ZD_THIN"] if ht is None else ht; ZK = ns["ZD_THICK"] if hk is None else hk; ft = F.f_thin if fk is None else 1 - fk; rk = rd if rdk is None else rdk; ss = p["sig_star_R0"] * 1e6
    st = ft * ss * math.exp(R0 / rd); sk = (1 - ft) * ss * math.exp(R0 / rk); fb = p["fb"]; Mstar = 2 * math.pi * (st * rd * rd + sk * rk * rk) + mbb
    RB_, AB, R0B, RC, Q = ns["RHO0_B"], ns["ALPHA_B"], ns["R0_B"], ns["RCUT_B"], ns["Q_B"]; HI, H2 = ns["S0_HI"], ns["S0_H2"]
    def rho(R, z):
        zz = np.abs(z); rp = np.maximum(np.sqrt(R * R + (zz / Q) ** 2), 1e-7); Rs = np.maximum(R, 1e-6)
        return (st / (2 * ZT)) * np.exp(-zz / ZT - R / rd) + (sk / (2 * ZK)) * np.exp(-zz / ZK - R / rk) + fb * (RB_ / (1 + rp / R0B) ** AB * np.exp(-(rp / RC) ** 2)) + (HI * np.exp(-4.0 / Rs - Rs / 7.0) / (4 * 0.085)) / np.cosh(np.minimum(zz / 0.17, 300)) ** 2 + (H2 * np.exp(-12.0 / Rs - Rs / 1.5) / (4 * 0.045)) / np.cosh(np.minimum(zz / 0.09, 300)) ** 2
    return rho, Mstar
def grid(a0, hi=False):
    Mu = PS.mass_unit(a0); Mt = 6.6e10 / Mu
    if not hi: return ns["mw_grid"](Mt), Mu
    re_ = PS.log_edges(0.005, 300.0 * max(60.0, math.sqrt(Mt)), 60); return PS.Grid(re_, PS.theta_edges(96, full=False, stretch_min=0.001)), Mu
def solve(rhof, a0, g, Mu, LU, forms="QR", mut=False):
    rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); o = {}; PhiN = LU.newton(rho1); a0k = a0 * PS.KPC / 1e6
    oN = ns["mw_obs"](g, PhiN, a0); o["N"] = dict(vc=oN["vc_R0"], K0=oN["K_R0"])
    if "Q" in forms: o["Q"] = field_lines(g, LU.qumond(PhiN, mut), a0)
    if "R" in forms:
        Rall = np.r_[R0, OR, BR_R]; vb = L.vc_plane(ns, g, PhiN, a0, Rall); gb = vb ** 2 / Rall; gc = (0.5 + np.sqrt(0.25 + a0k / np.maximum(gb, 1e-30)) - 1) * gb; nR = 1 + len(OR); vR = np.sqrt(vb ** 2 + Rall * gc); K = np.array(oN["K"]) + gc[nR:] * 1.1 / BR_R / KZU; K0 = oN["K_R0"] + gc[0] * 1.1 / R0 / KZU; o["R"] = lines(float(vR[0]), K, float(K0), vR[1:nR])
    if "A" in forms:
        pr = PS.Problem(g, rho1, 2 * float(np.sum(rho1 * g.vol)), 0.0, Lam=0.0); Phi, res, it = pr.solve_aqual(); o["A"] = field_lines(g, Phi, a0); o["res"] = float(res)
    return o
