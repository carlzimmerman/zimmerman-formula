#!/usr/bin/env python3
"""CFG254 -- an "outside contact" with the dark energy, and "nothing before recombination": a phase-1 hand-check.

Research direction: this lane was directed by the owner (the repository's author), who proposed the idea and asked for it to be tested.
Frozen criteria: ../CFG254_FROZEN_CRITERIA.md (sha256 in CFG254_CRITERIA_SHA256.txt, recorded before this script existed).
kappa = 1/2 FITTED, not derived.  Nothing here says the theory is closed or that any data favour any model.
Literature values not already in a committed file are marked (memory, UNVERIFIED).  No downloads; writes only in this directory.

Readings (scored separately, never pooled):
  R1-lit  nothing before recombination (no dynamics before z*)          R1-om  "created as if" it had a past (UNTESTABLE-AS-STATED)
  R2a     a one-time contact at z_c: step (A), pulse (B), and the paddle = recombination (R2a-rec)
  R2b     a continuing drive: monotone injection (w <= -1), constant-w family, drive-then-leak
  R3      bubble collision / brane contact (anisotropic)
Gates: G1 BBN / pre-recombination; G2 expansion history; G3 flat a0 at z <= 5; G4 sky isotropy; G5 constants count.

Run from the repository root:
  python3 campaign_fresh_gravity/CFG254_outside_contact/CFG254_handcheck.py
  MUTATE=1 python3 campaign_fresh_gravity/CFG254_outside_contact/CFG254_handcheck.py   (every contact amplitude -> 0, full past restored)
"""
import os
import sys
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
MUT = os.environ.get("MUTATE", "").strip() == "1"            # read before the CFG222 prefix pops it
import io
import re
import ast
import json
import math
import time
import contextlib
import warnings
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize, brentq
from scipy.interpolate import RectBivariateSpline
import camb
from camb import bbn as camb_bbn

warnings.filterwarnings("ignore")
T0 = time.time()
LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
SFX = "_MUTATE" if MUT else ""
OUT_TXT, CHK = [], []
RES = {"lane": "CFG254", "mutate": MUT, "checks": {}, "numbers": {}}


def P(s=""):
    print(s, flush=True)
    OUT_TXT.append(str(s))


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def check(name, measured, ok, load_bearing=True):
    ok = bool(ok)
    CHK.append((name, ok, load_bearing))
    RES["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    return ok


def rp(*a):
    return os.path.join(REPO, *a)


P(__doc__.strip())
if MUT:
    P("\n  *** MUTATE=1: every contact amplitude is set to zero (A = 0, B = 0, w = -1) and R1's full past is restored (z_start -> oo).\n"
      "      Required: L1 and L2 FAIL (rc = 1); L3 holds at every grid point; every G3 law reads SAME-AS-FLAT. ***")

# ================================================================================================ constants
c_SI, G_SI = 299792458.0, 6.67430e-11
C_KMS = 299792.458
MPC = 3.0856775814913673e22
EV = 1.602176634e-19
K_B = 1.380649e-23
M_H = 1.6735575e-27          # hydrogen atom mass (kg)
M_E = 9.1093837015e-31
HBAR = 1.054571817e-34
A_RAD = 7.565723e-16         # radiation constant (J m^-3 K^-4)
T_CMB = 2.7255               # K (XR26's value)
RHO_C100 = 3 * (100e3 / MPC) ** 2 / (8 * math.pi * G_SI)   # critical density for h = 1 (kg/m^3)
B_H, B_HE1, B_HE2, E_LYA = 13.598434, 24.587389, 54.417765, 10.19881   # eV
MASS_RATIO_HE_H = 3.9715     # CAMB's
KAPPA = 0.5
H0_FP0, OML_FP0 = 67.4, 0.6847

# ================================================================================================ record inputs (read-only)
FP0 = json.load(open(rp("real_research", "derivation_chain_2026", "FP0_core_postulates_results.json")))["numbers"]
X26 = rp("real_research", "cross_thread_review_2026_09_26")
J26C = json.load(open(os.path.join(X26, "XR26_cmb_results.json")))["numbers"]
J26B = json.load(open(os.path.join(X26, "XR26_bbn_results.json")))["numbers"]
# the lane's copies (checked against the committed files in C3)
P18 = {"omega_b": 0.022383, "omega_cdm": 0.12011, "tau_reio": 0.0543, "ln_A_s_1e10": 3.0448, "n_s": 0.96605}
THETA_MC = 1.040909e-2
DP_MEAN = np.array([1.7502, 301.471, 0.02236, 0.9649])
DP_SIG = np.array([0.0046, 0.0895, 0.00015, 0.0043])
DP_CORR = np.array([[1.0, 0.46, -0.66, -0.74], [0.46, 1.0, -0.33, -0.35], [-0.66, -0.33, 1.0, 0.46], [-0.74, -0.35, 0.46, 1.0]])
DP_COVI = np.linalg.inv(DP_CORR * np.outer(DP_SIG, DP_SIG))
BAO = [(0.295, "DV", 7.93, 0.15), (0.510, "DM", 13.62, 0.25), (0.510, "DH", 20.98, 0.61), (0.706, "DM", 16.85, 0.32),
       (0.706, "DH", 20.08, 0.60), (0.930, "DM", 21.71, 0.28), (0.930, "DH", 17.88, 0.35), (1.317, "DM", 27.79, 0.69),
       (1.317, "DH", 13.82, 0.42), (1.491, "DV", 26.07, 0.67), (2.330, "DM", 39.71, 0.94), (2.330, "DH", 8.52, 0.17)]
THETA_OBS, THETA_SIG = 1.04109, 0.00030        # 100 theta_*, Planck 2018 (as in real_research/reviews/mi_cmb_camb_run_2026.py)
NEFF_OBS, NEFF_SIG = 2.99, 0.17                 # Planck + BAO 2018 (as cited in project_atomos/A05_derived_mass_prediction.py)
YP_OBS, YP_SIG = 0.245, 0.003                   # PDG 2024 (as cited in XR26_bbn.py)
DH_OBS, DH_SIG = 2.547e-5, 0.029e-5             # PDG 2024 (as cited in XR26_bbn.py)
A95_DIPOLE = {"CFG182": 0.43, "CFG192": 0.40}

# ================================================================================================ C0: the footings
banner("CONTROLS")
rhoL_fp0 = OML_FP0 * RHO_C100 * (H0_FP0 / 100) ** 2
rhoT_fp0 = RHO_C100 * (H0_FP0 / 100) ** 2
a0_can = KAPPA * c_SI * math.sqrt(G_SI * rhoL_fp0)
a0_alt = KAPPA * c_SI * math.sqrt(G_SI * rhoT_fp0)
check("C0 kappa = 1/2 with H0 = 67.4, Omega_L = 0.6847 reproduces FP0's canonical and alt (rho_total) a0",
      f"canonical {a0_can:.5e} (FP0 {FP0['a0_canonical']:.5e}); alt {a0_alt:.5e} (FP0 {FP0['a0_rho_total']:.5e})",
      abs(a0_can / FP0["a0_canonical"] - 1) < 1e-4 and abs(a0_alt / FP0["a0_rho_total"] - 1) < 1e-4)

# ================================================================================================ C1: CAMB at the Planck 2018 best fit (XR26's settings)
BBN_PAR = camb_bbn.BBN_table_interpolator("PArthENoPE_880.2_standard.dat")


def camb_bg(omb, omc, H0=None, theta=None):
    p = camb.CAMBparams()
    kw = dict(ombh2=omb, omch2=omc, tau=P18["tau_reio"], mnu=0.06, num_massive_neutrinos=1, nnu=3.046, bbn_predictor=BBN_PAR)
    if theta is not None:
        kw["cosmomc_theta"] = theta
    else:
        kw["H0"] = H0
    p.set_cosmology(**kw)
    p.InitPower.set_params(As=math.exp(P18["ln_A_s_1e10"]) / 1e10, ns=P18["n_s"])
    return p, camb.get_background(p)


PP, RR = camb_bg(P18["omega_b"], P18["omega_cdm"], theta=THETA_MC)
DER = RR.get_derived_params()
ZSTAR, RSTAR, RDRAG, TH_CAMB = DER["zstar"], DER["rstar"], DER["rdrag"], DER["thetastar"]
H_FID = J26C["K1"]["H0"] / 100.0
YHE = float(PP.YHe)
check("C1 CAMB 1.6.6 at the Planck 2018 best fit (XR26's settings) reproduces XR26's committed r_drag, 100 theta_* and z_*",
      f"r_drag {RDRAG:.4f} (XR26 {J26C['K1']['r_drag']:.4f}); 100theta_* {TH_CAMB:.6f} ({J26C['K1']['100theta_star']:.6f}); z_* {ZSTAR:.3f} ({J26C['K1']['zstar']:.3f}); Y_He {YHE:.5f}",
      abs(RDRAG - J26C["K1"]["r_drag"]) < 0.02 and abs(TH_CAMB - J26C["K1"]["100theta_star"]) < 1e-5 and abs(ZSTAR - J26C["K1"]["zstar"]) < 0.01)

# ================================================================================================ C3: the lane's copies equal the committed files
src4 = open(os.path.join(CFG, "CFG4_cosmology.py")).read()
m4 = re.search(r"BAO = (\[.*?\])\nLA", src4, re.S)
bao_file = ast.literal_eval(m4.group(1)) if m4 else None
src26 = open(os.path.join(X26, "XR26_cmb.py")).read()
dp_ok = all(s in src26 for s in ("DP_MEAN = np.array([1.7502, 301.471, 0.02236, 0.9649])", "DP_SIG = np.array([0.0046, 0.0895, 0.00015, 0.0043])",
                                 "DP_CORR = np.array([[1.0, 0.46, -0.66, -0.74], [0.46, 1.0, -0.33, -0.35], [-0.66, -0.33, 1.0, 0.46], [-0.74, -0.35, 0.46, 1.0]])",
                                 'P18 = {"omega_b": 0.022383, "omega_cdm": 0.12011, "tau_reio": 0.0543, "ln_A_s_1e10": 3.0448, "n_s": 0.96605}'))
th_ok = "THETA_FRAC_ERR = 0.00030 / 1.04109" in open(rp("real_research", "reviews", "mi_cmb_camb_run_2026.py")).read()
ne_ok = "N_eff = 2.99 +- 0.17" in open(rp("project_atomos", "A05_derived_mass_prediction.py")).read()
bb_ok = all(s in open(os.path.join(X26, "XR26_bbn.py")).read() for s in ("Y_P = 0.245 +- 0.003", "D/H = (2.547 +- 0.029) x 1e-5"))
check("C3 the lane's copies equal the committed files: DESI DR1 BAO (CFG4), CHW priors and Planck point (XR26), 100theta_* (mi_cmb_camb_run), N_eff (atomos A05), Y_P and D/H (XR26_bbn)",
      f"BAO {bao_file == BAO}; CHW/P18 {dp_ok}; theta {th_ok}; N_eff {ne_ok}; BBN obs {bb_ok}", bao_file == BAO and dp_ok and th_ok and ne_ok and bb_ok)

# ================================================================================================ the background model and its integrator
GLX, GLW = np.polynomial.legendre.leggauss(20)
MODEL = {"kind": "lcdm", "zc": 0.0, "amp": 0.0}


def f_de(z, model):
    """rho_DE(z)/rho_DE0 for the contact models (MUTATE forces zero amplitude)."""
    kind, amp = model["kind"], (0.0 if MUT else model["amp"])
    z = np.asarray(z, float)
    if kind == "lcdm" or amp == 0.0:
        return np.ones_like(z)
    if kind == "step":
        return np.where(z <= model["zc"], 1.0, 1.0 - amp)
    if kind == "pulse":
        g = lambda zz: np.exp(-np.log((1 + zz) / (1 + model["zc"])) ** 2 / (2 * 0.1 ** 2))
        return (1 + amp * g(z)) / (1 + amp * g(0.0))
    if kind == "wconst":           # amp = -(1 + w) >= 0 for a drive
        return (1 + z) ** (-3 * amp)
    raise ValueError(kind)


def breaks(model):
    if MUT or model["kind"] == "lcdm" or model["amp"] == 0.0:
        return []
    u = math.log1p(model["zc"]) if model["kind"] in ("step", "pulse") else None
    if model["kind"] == "step":
        return [u]
    if model["kind"] == "pulse":
        return [u + d for d in (-0.6, -0.3, 0.0, 0.3, 0.6)]
    return []


def seg_nodes(u0, u1, bks, dmax=0.25):
    """Gauss-Legendre nodes on [u0, u1] in u = ln(1+z), split at breakpoints and into pieces <= dmax."""
    pts = sorted(set([u0, u1] + [b for b in bks if u0 < b < u1]))
    xs, ws = [], []
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int(math.ceil((b - a) / dmax)))
        edges = np.linspace(a, b, n + 1)
        for e0, e1 in zip(edges[:-1], edges[1:]):
            xs.append(0.5 * (e1 - e0) * GLX + 0.5 * (e1 + e0))
            ws.append(0.5 * (e1 - e0) * GLW)
    return np.concatenate(xs), np.concatenate(ws)


def cosmo(omb, omc, h, model):
    """CHW's background: flat, Omega_r = Omega_m/(1 + z_eq), neutrino mass in omega_m; dark energy closes E(0) = 1."""
    omm = omb + omc + 0.06 / 93.14
    tt = (T_CMB / 2.7) ** -4
    zeq = 2.5e4 * omm * tt
    Om = omm / h ** 2
    Orr = Om / (1 + zeq)
    ODE = 1.0 - Om - Orr
    E = lambda z: np.sqrt(Orr * (1 + z) ** 4 + Om * (1 + z) ** 3 + ODE * f_de(z, model))
    return dict(omb=omb, omc=omc, omm=omm, h=h, Om=Om, Orr=Orr, ODE=ODE, E=E, ch=C_KMS / (100 * h), tt=tt, model=model)


def dc(cs, z):
    """comoving distance (Mpc) to z (scalar)"""
    if z <= 0:
        return 0.0
    u, w = seg_nodes(0.0, math.log1p(z), breaks(cs["model"]))
    zz = np.expm1(u)
    return cs["ch"] * float(np.sum(w * (1 + zz) / cs["E"](zz)))


def rs_chw(cs, zs, u_top=math.log(1e9)):
    Rb = 31500 * cs["omb"] * cs["tt"]
    u, w = seg_nodes(math.log1p(zs), u_top, breaks(cs["model"]), dmax=0.5)
    zz = np.expm1(u)
    a = 1 / (1 + zz)
    return cs["ch"] * float(np.sum(w * (1 + zz) / (cs["E"](zz) * np.sqrt(3 * (1 + Rb * a)))))


def zstar_hs(omb, omm):
    g1 = 0.0738 * omb ** -0.238 / (1 + 39.5 * omb ** 0.763)
    g2 = 0.560 / (1 + 21.1 * omb ** 1.81)
    return 1048 * (1 + 0.00124 * omb ** -0.738) * (1 + g1 * omm ** g2)


def chw_x(cs, ns):
    zs = zstar_hs(cs["omb"], cs["omm"])
    dm = dc(cs, zs)
    return np.array([math.sqrt(cs["Om"]) * dm / cs["ch"], math.pi * dm / rs_chw(cs, zs), cs["omb"], ns])


def chi2_chw(x):
    d = x - DP_MEAN
    return float(d @ DP_COVI @ d)


# ------------------------------------------------------------------------------ C2 and C5: the CHW implementation and the integrator
cs_p18 = cosmo(P18["omega_b"], P18["omega_cdm"], H_FID, {"kind": "lcdm", "zc": 0, "amp": 0})
chi_p18 = chi2_chw(chw_x(cs_p18, P18["n_s"]))
check("C2 this lane's CHW 2019 implementation gives XR26's committed LCDM chi^2 at the Planck point",
      f"{chi_p18:.5f} (XR26 {J26C['C2']['chi2_lcdm']:.5f})", abs(chi_p18 - J26C["C2"]["chi2_lcdm"]) < 1e-3)


def quad_dc(cs, z, zc=None):
    f = lambda zz: 1.0 / float(cs["E"](np.array(zz)))
    if zc is not None and 0 < zc < z:
        return cs["ch"] * (quad(f, 0, zc, epsabs=0, epsrel=1e-12, limit=400)[0] + quad(f, zc, z, epsabs=0, epsrel=1e-12, limit=400)[0])
    return cs["ch"] * quad(f, 0, z, epsabs=0, epsrel=1e-12, limit=400)[0]


def quad_rs(cs, zs):
    Rb = 31500 * cs["omb"] * cs["tt"]
    f = lambda a: 1 / (a ** 2 * float(cs["E"](np.array(1 / a - 1))) * math.sqrt(3 * (1 + Rb * a)))
    return cs["ch"] * quad(f, 1e-9, 1 / (1 + zs), limit=400, epsabs=0, epsrel=1e-11)[0]


c5 = 0.0
for mdl in ({"kind": "lcdm", "zc": 0, "amp": 0}, {"kind": "step", "zc": 1.5, "amp": 0.7}):
    cs_ = cosmo(P18["omega_b"], P18["omega_cdm"], H_FID, mdl)
    zs_ = zstar_hs(cs_["omb"], cs_["omm"])
    zc_ = mdl["zc"] if mdl["kind"] == "step" and not MUT else None
    c5 = max(c5, abs(dc(cs_, zs_) / quad_dc(cs_, zs_, zc_) - 1), abs(dc(cs_, 2.33) / quad_dc(cs_, 2.33, zc_) - 1),
             abs(rs_chw(cs_, zs_) / quad_rs(cs_, zs_) - 1))
check("C5 the Gauss-Legendre integrator agrees with scipy quad for D_M(z*), D_M(2.33) and r_s(z*), with and without a step at z_c = 1.5",
      f"max relative difference {c5:.1e}", c5 < 1e-7)

# ------------------------------------------------------------------------------ r_d spline (CAMB) and C4
OB_G = np.linspace(0.0170, 0.0280, 12)
OC_G = np.linspace(0.070, 0.210, 15)
RD_G = np.array([[camb_bg(ob, oc, H0=67.32)[1].get_derived_params()["rdrag"] for oc in OC_G] for ob in OB_G])
RD_SPL = RectBivariateSpline(OB_G, OC_G, RD_G, kx=3, ky=3)


def rd_of(omb, omc):
    return float(RD_SPL(omb, omc)[0, 0])


rng = np.random.default_rng(254)
c4a = 0.0
for _ in range(5):
    ob, oc = rng.uniform(0.0200, 0.0250), rng.uniform(0.100, 0.150)
    c4a = max(c4a, abs(rd_of(ob, oc) / camb_bg(ob, oc, H0=67.32)[1].get_derived_params()["rdrag"] - 1))
c4b = max(abs(camb_bg(P18["omega_b"], P18["omega_cdm"], H0=hh)[1].get_derived_params()["rdrag"] / RDRAG - 1) for hh in (62.32, 72.32))
check("C4 the r_d spline in (omega_b, omega_c) matches CAMB at five off-grid points, and r_d is independent of h at fixed omegas",
      f"spline max relative difference {c4a:.1e}; h +- 5 changes r_d by {c4b:.1e}", c4a < 2e-4 and c4b < 1e-4)


def bao_chi2(cs):
    rd = rd_of(cs["omb"], cs["omc"])
    s = 0.0
    for z, kind, v, e in BAO:
        DM = dc(cs, z)
        DH = cs["ch"] / float(cs["E"](np.array(z)))
        val = {"DM": DM, "DH": DH, "DV": (z * DM * DM * DH) ** (1 / 3)}[kind] / rd
        s += ((val - v) / e) ** 2
    return s


def chi2_tot(q, model):
    omb, omc, h, ns = q
    if not (OB_G[0] < omb < OB_G[-1] and OC_G[0] < omc < OC_G[-1] and 0.40 < h < 1.0 and 0.8 < ns < 1.2):
        return 1e12
    cs = cosmo(omb, omc, h, model)
    if cs["ODE"] <= 0:
        return 1e12
    return chi2_chw(chw_x(cs, ns)) + bao_chi2(cs)


def fit(model, start):
    r = minimize(lambda q: chi2_tot(q, model), start, method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-9, maxiter=8000, maxfev=12000))
    r2 = minimize(lambda q: chi2_tot(q, model), r.x, method="Nelder-Mead", options=dict(xatol=1e-9, fatol=1e-10, maxiter=8000, maxfev=12000))
    best = r2 if r2.fun <= r.fun else r
    return float(best.fun), np.array(best.x)


START = np.array([P18["omega_b"], P18["omega_cdm"], H_FID, P18["n_s"]])
LCDM = {"kind": "lcdm", "zc": 0.0, "amp": 0.0}
CHI_L, Q_L = fit(LCDM, START)
cs_L = cosmo(*Q_L[:3], LCDM)
P(f"\n  LCDM profiled on CHW 2019 + DESI DR1 BAO (12, diagonal): chi^2_min = {CHI_L:.4f} (4 + 12 = 16 numbers, 4 free); "
  f"omega_b {Q_L[0]:.5f}, omega_c {Q_L[1]:.5f}, h {Q_L[2]:.5f}, n_s {Q_L[3]:.4f}; Omega_m {cs_L['Om']:.4f}; r_d {rd_of(Q_L[0], Q_L[1]):.3f} Mpc")
z_acc = (2 * cs_L["ODE"] / cs_L["Om"]) ** (1 / 3) - 1
P(f"  LCDM onset of acceleration (q = 0) at this fit: z_acc = {z_acc:.3f} -- a constant dark energy becomes dominant late with no event needed")
RES["numbers"]["lcdm_fit"] = dict(chi2=CHI_L, q=Q_L.tolist(), Om=cs_L["Om"], rd=rd_of(Q_L[0], Q_L[1]), z_acc=z_acc)

# ================================================================================================ R1
banner("R1  'NOTHING BEFORE RECOMBINATION' against the record's numbers (G1)")
S_STAR = float(RR.sound_horizon(ZSTAR))
DM_STAR = float(RR.comoving_radial_distance(ZSTAR))


def theta_trunc(z_start):
    """100 theta_* when sound waves only start at z_start (fixed Planck parameters); z_start = inf is the full past."""
    tail = 0.0 if not math.isfinite(z_start) else float(RR.sound_horizon(z_start))
    return 100 * (S_STAR - tail) / DM_STAR


Z_START_LIT = math.inf if MUT else ZSTAR * (1 + 1e-12)
th_lit = theta_trunc(Z_START_LIT)
pull_theta = (THETA_OBS - th_lit) / THETA_SIG
P(f"  CAMB (Planck 2018 best fit): r_s(z*) = {S_STAR:.3f} Mpc, D_M(z*) = {DM_STAR:.2f} Mpc, 100theta_* = {100 * S_STAR / DM_STAR:.6f}")
P(f"  (c) acoustic scale: R1-lit {'[MUTATE: full past]' if MUT else '(sound waves start at z*)'} gives 100theta_* = {th_lit:.6f}; "
  f"observed {THETA_OBS} +- {THETA_SIG}: pull {pull_theta:+.1f} sigma")
ZS_LIST = [(1 + ZSTAR) * 1.01 - 1, 1200, 1500, 2000, 3000, 5000, 1e4, 3e4, 1e5, 1e6]
trunc = []
P("      truncated sound horizon at fixed Planck parameters (illustrative; no re-fit):")
P(f"      {'z_start':>10s} {'r_s kept (Mpc)':>15s} {'fraction':>9s} {'100theta_*':>11s} {'pull':>9s}")
for zs in ZS_LIST:
    th = theta_trunc(zs)
    trunc.append(dict(z_start=zs, rs=th / 100 * DM_STAR, frac=th / 100 * DM_STAR / S_STAR, theta=th, pull=(th - THETA_OBS) / THETA_SIG))
    P(f"      {zs:10.4g} {th / 100 * DM_STAR:15.3f} {th / 100 * DM_STAR / S_STAR:9.5f} {th:11.6f} {(th - THETA_OBS) / THETA_SIG:+9.1f}")
zs_need = {}
for k in (1, 3, 5):
    try:
        zs_need[k] = 10 ** brentq(lambda lz: (theta_trunc(10 ** lz) - THETA_OBS) / THETA_SIG + k, math.log10(ZSTAR * 1.001), 9)
    except ValueError:
        zs_need[k] = None
P("      sound waves must have started before z_start = " + ", ".join(f"{v:.3g} ({k} sigma)" if v else f"n/a ({k} sigma)" for k, v in zs_need.items())
  + " at fixed parameters (the full-past value itself sits at " + f"{(theta_trunc(math.inf) - THETA_OBS) / THETA_SIG:+.2f} sigma)")
# (d) BAO implied r_d
rdi, sgi = [], []
for z, kind, v, e in BAO:
    DMz = float(RR.comoving_radial_distance(z))
    DHz = C_KMS / float(RR.hubble_parameter(z))
    X = {"DM": DMz, "DH": DHz, "DV": (z * DMz * DMz * DHz) ** (1 / 3)}[kind]
    rdi.append(X / v)
    sgi.append(X / v * e / v)
rdi, sgi = np.array(rdi), np.array(sgi)
wbao = 1 / sgi ** 2
rd_mean, rd_sig = float(np.sum(wbao * rdi) / np.sum(wbao)), float(1 / math.sqrt(np.sum(wbao)))
pull_bao = (rd_mean - (RDRAG if MUT else 0.0)) / rd_sig          # MUTATE: the full past predicts CAMB's r_drag
P(f"  (d) BAO: the 12 DESI DR1 numbers at Planck 2018 distances imply r_d = {rd_mean:.2f} +- {rd_sig:.2f} Mpc (diagonal; CAMB r_drag {RDRAG:.2f}); "
  + (f"R1-lit has no sound horizon (r_d = 0): pull {pull_bao:.1f} sigma" if not MUT else f"[MUTATE: full past, r_d = CAMB r_drag] pull {pull_bao:+.2f} sigma"))
# (a), (b), (e)
YP_BBN = J26B["B2"]["PArthENoPE 2017"]["Y_P"]
DH_BBN = J26B["B2"]["PArthENoPE 2017"]["DH"]
yp_pred, dh_pred, ne_pred = (YP_BBN, DH_BBN, 3.046) if MUT else (0.0, 0.0, 0.0)
pull_yp, pull_dh, pull_ne = (YP_OBS - yp_pred) / YP_SIG, (DH_OBS - dh_pred) / DH_SIG, (NEFF_OBS - ne_pred) / NEFF_SIG
P(f"  (a) helium: R1-lit Y_P = {yp_pred:.4f} vs {YP_OBS} +- {YP_SIG}: pull {pull_yp:+.1f} sigma   (standard BBN, XR26: {YP_BBN:.4f}, {(YP_OBS - YP_BBN) / YP_SIG:+.2f} sigma)")
P(f"  (b) deuterium: R1-lit D/H = {dh_pred:.3e} vs {DH_OBS:.3e} +- {DH_SIG:.1e}: pull {pull_dh:+.1f} sigma   (standard BBN, XR26 PArthENoPE: {DH_BBN:.4e}, {(DH_OBS - DH_BBN) / DH_SIG:+.2f} sigma)")
P(f"  (e) neutrino background: R1-lit N_eff = {ne_pred} vs {NEFF_OBS} +- {NEFF_SIG}: pull {pull_ne:+.1f} sigma (neutrinos decouple at T ~ 1 MeV, z ~ 6e9)")
omb = P18["omega_b"]
rho_b0c2 = omb * RHO_C100 * c_SI ** 2
eps_fuse = (4 * 1.00782503 - 4.00260325) / (4 * 1.00782503)
E_he = eps_fuse * YP_OBS * rho_b0c2
u_g0 = A_RAD * T_CMB ** 4
P(f"      helium-by-stars energetics (reported; the concept is memory, UNVERIFIED): fusing {YP_OBS} of all baryons releases {E_he:.3e} J/m^3 today-equivalent "
  f"= {E_he / u_g0:.2f} x the CMB energy density ({u_g0:.3e}); released at z_f it is diluted by (1 + z_f).  Stellar helium arrives with metals "
  f"(dY/dZ ~ 1-3, memory UNVERIFIED) while Y_P is measured at very low metallicity.")
P("  (f) blackbody (reported, not a pull): FIRAS |mu| < 9e-5, |y| < 1.5e-5 (memory, UNVERIFIED).  A blackbody made in equilibrium at z* is"
  " compatible with R1-om; the acoustic phases and the super-horizon TE correlation (memory, UNVERIFIED) are what separate R1-lit from R1-om.")


def g1class(p):
    p = abs(p)
    return "CONTRADICTS" if p >= 5 else ("TENSION" if p >= 3 else "CONSISTENT")


R1TAB = {"(a) Y_P": pull_yp, "(b) D/H": pull_dh, "(c) theta_*": pull_theta, "(d) BAO r_d": pull_bao, "(e) N_eff": pull_ne}
P("  G1 classes (R1-lit): " + "; ".join(f"{k} {v:+.1f} sigma {g1class(v)}" for k, v in R1TAB.items()))
r1_fails = any(g1class(v) == "CONTRADICTS" for v in R1TAB.values())
P(f"  R1-lit: {'FAILS G1 -> CONTRADICTED' if r1_fails else 'does not fail G1'}{'  [MUTATE: full past restored, the reading is standard cosmology]' if MUT else ''}")
P("  R1-om ('created as if' with a past): matches every observation the standard past matches, by construction -> UNTESTABLE-AS-STATED; a restatement of the standard past.")
RES["numbers"]["R1"] = dict(pulls=R1TAB, classes={k: g1class(v) for k, v in R1TAB.items()}, theta_lit=th_lit, truncation=trunc,
                            z_start_needed=zs_need, rd_bao=[rd_mean, rd_sig], E_he_over_ucmb=E_he / u_g0, fails_G1=r1_fails)

# ================================================================================================ R2a: G2 grid
banner("R2a  A ONE-TIME CONTACT: step (A) and pulse (B) in rho_DE; G2 on CHW 2019 + DESI DR1 BAO (SN not in the repo: not scored)")
ZC_GRID = [0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0, 30.0, 100.0, 1090.0]
A_GRID = [round(0.1 * i, 1) for i in range(11)]
B_GRID = [0.0, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]


def g2class(d):
    return "EXCLUDED" if d >= 9 else ("TENSION" if d >= 4 else ("NON-DIAGNOSTIC" if d < 1 else "ALLOWED"))


def profile(kind, zc, grid, amax):
    rows, start, l3 = [], Q_L.copy(), 0.0
    for a in grid:
        chi, q = fit({"kind": kind, "zc": zc, "amp": a}, start)
        rows.append((a, chi - CHI_L, q))
        start = q
        if a == 0.0 or MUT:
            l3 = max(l3, abs(chi - CHI_L))
    d = [r[1] for r in rows]
    a95 = amax
    for i in range(1, len(rows)):
        if d[i] >= 2.71 > d[i - 1]:
            lo, hi, qs = rows[i - 1][0], rows[i][0], rows[i - 1][2]
            a95 = brentq(lambda a: fit({"kind": kind, "zc": zc, "amp": a}, qs)[0] - CHI_L - 2.71, lo, hi, xtol=1e-3)
            break
    return rows, a95, l3


def hratio(kind, zc, amp, q, zs=(0.5, 1, 2, 3, 5, 10)):
    cs = cosmo(*q[:3], {"kind": kind, "zc": zc, "amp": amp})
    return {z: float(cs["E"](np.array(z)) * cs["h"] / (cs_L["E"](np.array(z)) * cs_L["h"])) for z in zs}


STEP, PULSE, L3MAX, L1MAX = {}, {}, 0.0, 0.0
P(f"  {'z_c':>7s} {'dchi2(A=0.5)':>13s} {'dchi2(A=1)':>11s} {'class(A=1)':>15s} {'A95':>7s} {'a0 drop at A95 (dex)':>21s}   H/H_LCDM at A = 1, z = 0.5/1/2/3/5/10")
for zc in ZC_GRID:
    rows, a95, l3 = profile("step", zc, A_GRID, 1.0)
    L3MAX = max(L3MAX, l3)
    d1, q1 = rows[-1][1], rows[-1][2]
    hr = hratio("step", zc, 1.0, q1)
    ch_ = cosmo(*q1[:3], {"kind": "step", "zc": zc, "amp": 1.0})
    zz = np.linspace(0, ZSTAR, 4000)
    L1MAX = max(L1MAX, float(np.max(np.abs(ch_["E"](zz) / cosmo(*q1[:3], LCDM)["E"](zz) - 1))))
    drop = 0.5 * math.log10(max(1 - (0.0 if MUT else a95), 1e-18))
    STEP[zc] = dict(dchi2={a: r[1] for a, r in zip(A_GRID, rows)}, A95=a95, class_A1=g2class(d1), H_ratio_A1=hr, a0_drop_dex_at_A95=drop, q_A1=q1.tolist())
    dtxt = "a0 -> 0 allowed" if (a95 >= 1.0 and not MUT) else f"{drop:.3f}"
    P(f"  {zc:7.4g} {rows[5][1]:13.3f} {d1:11.3f} {g2class(d1):>15s} {a95:7.3f} {dtxt:>21s}   " + " ".join(f"{v:.4f}" for v in hr.values()))
P(f"\n  {'z_c':>7s} {'dchi2(B=1)':>11s} {'dchi2(B=5)':>11s} {'class(B=5)':>15s} {'B95':>7s} {'a0 peak/a0(0) at B95':>21s}")
for zc in [z for z in ZC_GRID if z <= 10]:
    rows, b95, l3 = profile("pulse", zc, B_GRID, 5.0)
    L3MAX = max(L3MAX, l3)
    d5 = rows[-1][1]
    bb = 0.0 if MUT else b95
    pk = math.sqrt((1 + bb) / (1 + bb * math.exp(-math.log(1 + zc) ** 2 / 0.02)))
    PULSE[zc] = dict(dchi2={b: r[1] for b, r in zip(B_GRID, rows)}, B95=b95, class_B5=g2class(d5), a0_peak_ratio_at_B95=pk)
    P(f"  {zc:7.4g} {rows[4][1]:11.3f} {d5:11.3f} {g2class(d5):>15s} {b95:7.3f} {pk:21.4f}")
RES["numbers"]["R2a_step"] = {str(k): v for k, v in STEP.items()}
RES["numbers"]["R2a_pulse"] = {str(k): v for k, v in PULSE.items()}
blind = [zc for zc, v in STEP.items() if v["class_A1"] in ("NON-DIAGNOSTIC", "ALLOWED")]
P(f"\n  Step contacts that switch ALL the dark energy on (A = 1) and are not excluded: z_c in {blind}")
P(f"  The largest fractional change of E(z) at z <= z* over the A = 1 fits: {L1MAX:.3e}")
# POST HOC (added after the first debug run showed negative Delta chi^2; reported only, never a verdict)
allpts = [("step", zc, a, d) for zc, v in STEP.items() for a, d in v["dchi2"].items()] + [("pulse", zc, b, d) for zc, v in PULSE.items() for b, d in v["dchi2"].items()]
mn = min(allpts, key=lambda t: t[3])
nneg = sum(1 for t in allpts if t[3] < -1e-6)
P(f"  POST HOC (reported only): {nneg} of {len(allpts)} grid points fit the compressed data BETTER than LCDM; the lowest is {mn[0]} z_c = {mn[1]:g}, "
  f"amplitude {mn[2]:g}: Delta chi^2 = {mn[3]:+.2f} (look-elsewhere over {len(allpts)} points and two shapes; DR1 BAO diagonal, SN not scored, DR2 BAO not in the repo): not a detection")
RES["numbers"]["posthoc_min_dchi2"] = dict(kind=mn[0], zc=mn[1], amp=mn[2], dchi2=mn[3], n_negative=nneg, n_points=len(allpts))

# ================================================================================================ R2a-rec
banner("R2a-rec  THE PADDLE = RECOMBINATION: the injected amount (post-hoc-flagged menu), the missing recombination radiation, the fast-sink kinetics")
zgrid = np.linspace(8000.0, 50.0, 79501)
xe = RR.get_background_redshift_evolution(zgrid, ["x_e"], format="array")[:, 0]
fHe = YHE / (MASS_RATIO_HE_H * (1 - YHE))
nH0 = (1 - YHE) * P18["omega_b"] * RHO_C100 / M_H
zmid = 0.5 * (zgrid[1:] + zgrid[:-1])
nHz = nH0 * (1 + zmid) ** 3
selH = zgrid <= 1800
xH = np.where(selH, np.minimum(xe, 1.0), 1.0)
dxH = -(xH[1:] - xH[:-1])                               # >= 0 as z decreases
E2 = float(np.sum(B_H * EV * nHz * dxH))
y = np.clip(xe - 1.0, 0.0, 2 * fHe)
dy = -(y[1:] - y[:-1])
ymid = 0.5 * (y[1:] + y[:-1])
E_he_rel = float(np.sum(np.where(ymid > fHe, B_HE2, B_HE1) * EV * nHz * dy))
E3 = E2 + E_he_rel
nHs = nH0 * (1 + ZSTAR) ** 3
xe_star = float(np.interp(ZSTAR, zgrid[::-1], xe[::-1]))
Tstar = T_CMB * (1 + ZSTAR)
MENU = {"E1 13.6 eV x n_H(z*)": B_H * EV * nHs,
        "E2 H binding energy released over the recombination history (PRIMARY)": E2,
        "E3 E2 + helium recombination": E3,
        "E4 Lyman-alpha 10.2 eV x n_H(z*)": E_LYA * EV * nHs,
        "E5 gas thermal energy at z*": 1.5 * (nHs * (1 + fHe) + xe_star * nHs) * K_B * Tstar,
        "E6 photon energy density at z*": A_RAD * Tstar ** 4,
        "E7 rho_b(z*) c^2": P18["omega_b"] * RHO_C100 * c_SI ** 2 * (1 + ZSTAR) ** 3,
        "E8 rho_m(z*) c^2": (P18["omega_b"] + P18["omega_cdm"] + 0.06 / 93.14) * RHO_C100 * c_SI ** 2 * (1 + ZSTAR) ** 3}
rhoL_c2 = rhoL_fp0 * c_SI ** 2
rhoT_c2 = rhoT_fp0 * c_SI ** 2
rhoL_p18_c2 = (H_FID ** 2 - (P18["omega_b"] + P18["omega_cdm"] + 0.06 / 93.14)) * RHO_C100 * c_SI ** 2
P(f"  rho_Lambda c^2 = {rhoL_c2:.4e} J/m^3 (FP0: H0 67.4, Omega_L 0.6847); at the CAMB Planck point {rhoL_p18_c2:.4e}; rho_crit c^2 (alt footing) {rhoT_c2:.4e}")
P(f"  n_H0 = {nH0:.4f} m^-3 (Y_He {YHE:.5f}, omega_b {P18['omega_b']}); z* = {ZSTAR:.2f}; x_e(z*) = {xe_star:.4f}; He/H = {fHe:.5f}")
P(f"  {'menu item':70s} {'J/m^3':>11s} {'/rho_L c^2':>11s} {'/rho_crit c^2':>13s}")
for k, v in MENU.items():
    P(f"  {k:70s} {v:11.4e} {v / rhoL_c2:11.4g} {v / rhoT_c2:13.4g}")
distinct = {"E1/E2/E4": MENU["E2 H binding energy released over the recombination history (PRIMARY)"],
            "E3": E3, "E5": MENU["E5 gas thermal energy at z*"], "E6": MENU["E6 photon energy density at z*"],
            "E7": MENU["E7 rho_b(z*) c^2"], "E8": MENU["E8 rho_m(z*) c^2"]}
within2 = [k for k, v in MENU.items() if 0.5 <= v / rhoL_c2 <= 2.0]
span = math.log10(max(distinct.values()) / min(distinct.values()))
p1 = math.log10(4) / span
Kd = len(distinct)
p_le = 1 - (1 - p1) ** Kd
E2r = E2 / rhoL_c2
P(f"  within a factor 2 of rho_Lambda c^2: {len(within2)} of {len(MENU)} items ({'; '.join(k.split(' ')[0] for k in within2)})")
P(f"  look-elsewhere: K = {Kd} distinct items spanning {span:.2f} dex; chance that at least one lands within x2 under a log-uniform prior: {p_le:.3f}")
P(f"  PRIMARY E2/rho_Lambda c^2 = {E2r:.4f} (canonical), {E2 / rhoT_c2:.4f} against rho_crit (alt).  Grade: p* (POST-HOC-FLAGGED, criteria section 0), whatever the ratio.")
frac_rad = E2 / MENU["E6 photon energy density at z*"]
P(f"  missing recombination radiation: E2 / rho_gamma(z*) = {frac_rad:.2e}.  In standard physics this energy ends in photons (the cosmological recombination lines,"
  " amplitude of order 1e-9 of the CMB, memory UNVERIFIED), far below FIRAS: UNTESTABLE with present data; a genuine prediction for future spectral-distortion experiments.")
# fast-sink limit: Saha
def saha_x(z):
    T = T_CMB * (1 + z)
    S = (M_E * K_B * T / (2 * math.pi * HBAR ** 2)) ** 1.5 * math.exp(-B_H * EV / (K_B * T)) / (nH0 * (1 + z) ** 3)
    return 0.5 * (-S + math.sqrt(S * S + 4 * S))


z_saha = brentq(lambda z: saha_x(z) - 0.5, 900, 2500)
zH = zgrid[selH]
xHs = np.minimum(xe[selH], 1.0)
z_camb = float(np.interp(0.5, xHs[::-1], zH[::-1]))
zs_fast = (1 + ZSTAR) * (1 + z_saha) / (1 + z_camb) - 1
th_fast = 100 * float(RR.sound_horizon(zs_fast)) / float(RR.comoving_radial_distance(zs_fast))
pull_fast = (th_fast - THETA_OBS) / THETA_SIG
P(f"  fast-sink limit (reported, not load-bearing): Saha x_e = 0.5 at z = {z_saha:.1f} vs CAMB {z_camb:.1f}; z* -> {zs_fast:.1f}; "
  f"100theta_* -> {th_fast:.5f}, {pull_fast:+.0f} sigma at fixed parameters (illustrative: a modified recombination code and the Planck likelihood are needed)")
RES["numbers"]["R2a_rec"] = dict(menu={k: [v, v / rhoL_c2, v / rhoT_c2] for k, v in MENU.items()}, E2_ratio=E2r, within2=within2,
                                 lookelsewhere=dict(K=Kd, span_dex=span, p=p_le), frac_rad=frac_rad,
                                 fast_sink=dict(z_saha=z_saha, z_camb=z_camb, zstar_fast=zs_fast, theta=th_fast, pull=pull_fast),
                                 step_zc1090=STEP[1090.0])

# ================================================================================================ R2b: the DESI chains
banner("R2b  A CONTINUING DRIVE against the committed DESI DR2 w0-wa chains (CPL)")
sys.path.insert(0, CFG)
import CFG6_common as C6
J195 = json.load(open(os.path.join(CFG, "CFG195_de_flow_referee", "CFG195_desi_bound_results.json")))["numbers"]
R2B, c6 = {}, 0.0
x25 = 2.5 / 3.5
for nm in C6.DESI_ORDER:
    wt, w0, wa, om = C6.load_chain(nm)
    om1 = 1 + w0
    mono = (w0 <= -1) & (w0 + wa * x25 <= -1)
    f_mono = float(wt[mono].sum() / wt.sum())
    p_w0 = float(wt[w0 < -1].sum() / wt.sum())
    cross = (om1 * (om1 + wa * x25) < 0)
    fc = float(wt[cross].sum() / wt.sum())
    xc = om1 / (-wa + 1e-30)
    zc = xc / (1 - xc)
    zc[~cross] = np.nan
    zc[xc >= 1] = np.nan
    sel = cross & np.isfinite(zc)
    zmed = float(C6.wpct(zc[sel], wt[sel], [50])[0])
    ref = J195[f"{nm}_I2"]
    c6 = max(c6, abs(fc - ref["cross_frac"]), abs(zmed - ref["zcross_med"]), abs(p_w0 - ref["p_w0_lt_m1"]))
    R2B[nm] = dict(f_mono=f_mono, p_w0_lt_m1=p_w0, cross_frac=fc, zcross_med=zmed)
    P(f"  {nm:10s} f_mono (w <= -1 for all z in [0, 2.5]) = {f_mono:.2e}; p(w0 < -1) = {p_w0:.2e}; crossing fraction {fc:.4f}, median z_cross {zmed:.3f}")
check("C6 the chains reproduce CFG195's committed crossing fractions, median z_cross and p(w0 < -1) (same definitions)", f"max |difference| {c6:.1e}", c6 < 1e-6)
fm = [v["f_mono"] for v in R2B.values()]
cls_mono = "EXCLUDED" if all(f < 0.0027 for f in fm) else ("TENSION" if all(f < 0.05 for f in fm) else "ALLOWED")
P(f"  G2 class R2b-mono (and its members R2b-const): {cls_mono}.  R2b-leak (drive then leakage): the chains' own CPL shape, whose rho_DE maximum is the"
  " w = -1 crossing -> CONSISTENT by construction, NON-DIAGNOSTIC (a restatement of the fit), and it needs a phantom epoch (CFG176/CFG195).")
P("  The committed example of a drive: CFG176's accumulation (a0 ~ t, rho_DE ~ t^2), phantom at every z, excluded at 27-36 sigma (Gaussian proxy).")
W_DRIVE = [-1.05, -1.10, -1.20, -1.50]
for w in W_DRIVE:
    P(f"  R2b-const w = {w}: a0(z)/a0(0) = (1+z)^({1.5 * (1 + w):+.3f}) -> " + ", ".join(f"z={z}: {(0 if MUT else 1.5 * (1 + w)) * math.log10(1 + z):+.3f} dex" for z in (0.85, 1.5, 2.5, 5.0)))
RES["numbers"]["R2b"] = dict(chains=R2B, class_mono=cls_mono)

# ================================================================================================ G3: the high-z data through the CFG222 machinery
banner("G3  THE FLAT a0 AT z <= 5: theory (a0 = kappa c sqrt(G rho_DE), canonical tie) and the data (CFG222 machinery: RC100, CRISTAL)")
p222 = os.path.join(CFG, "CFG222_lcdm_proxy", "cfg222_lcdm_proxy.py")
s222 = open(p222).read()
ns = {"__file__": p222, "__name__": "cfg222_prefix"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s222[:s222.index("\n# ------------------------------------------------------------------------------------------------ controls")], p222, "exec"), ns)
ALL = ns["ALL"]
FMIN = 1e-9


def law_step(zc, A):
    s = math.sqrt(max(1 - (0.0 if MUT else A), 0.0))
    return lambda z: 1.0 if z <= zc else max(s, FMIN)


def law_pulse(zc, B):
    b = 0.0 if MUT else B
    g = lambda z: math.exp(-math.log((1 + z) / (1 + zc)) ** 2 / 0.02)
    return lambda z: math.sqrt((1 + b * g(z)) / (1 + b * g(0.0)))


def law_w(w):
    e = 0.0 if MUT else 1.5 * (1 + w)
    return lambda z: (1 + z) ** e


LAWS = {}
for zc in (0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0):
    LAWS[f"STEP z_c={zc} A=1"] = law_step(zc, 1.0)
    a95 = STEP[zc]["A95"]
    if 0.01 < a95 < 1.0:
        LAWS[f"STEP z_c={zc} A95={a95:.3f}"] = law_step(zc, a95)
for zc in (1.0, 2.0, 3.0, 5.0):
    LAWS[f"PULSE z_c={zc} B95={PULSE[zc]['B95']:.3f}"] = law_pulse(zc, PULSE[zc]["B95"])
for w in W_DRIVE:
    LAWS[f"DRIVE w={w}"] = law_w(w)
for k, f in LAWS.items():
    ALL[k] = f
PRIM, CELLS = ns["PRIM"], ns["CELLS"]
DS = ns["load_rc100"](ns["RC_PATH"]["committed"])
DSc = ns["load_rc100"](ns["RC_PATH"]["corrected"])
ids12 = [g["id"] for g in ns["cr"] if g["id"] not in ns["EXCL"]]
six = list(ns["DET"])
ROWS = {"RC100 committed (n = 100)": ("RC", DS), "CRISTAL R_e, fit route, n = 12": ("CR", ns["rows_Re"](ids12, "fit")),
        "CRISTAL R_e, independent route, six class-A": ("CR", ns["rows_Re"](six, "ind")),
        "CRISTAL R_out, fit route, six": ("CR", ns["rows_Rout"]("table_Rout", six, "fit")),
        "CRISTAL R_out, independent route, six": ("CR", ns["rows_Rout"]("table_Rout", six, "ind"))}


def row_stat(kind, data, law, cell, B=None):
    B = B or ns["NB"]
    if kind == "RC":
        d, s, bs = ns["rc_slopes"](data, law, cell, B=B)
        return s, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), float(np.std(bs))
    m, lo, hi, sd, d = ns["cr_med"](data, law, cell, B=B)
    return m, lo, hi, sd


J222 = json.load(open(os.path.join(CFG, "CFG222_lcdm_proxy", "cfg222_lcdm_proxy_results.json")))["main"]
c7 = 0.0
REF = {}
for lab, (kind, data) in list(ROWS.items()) + [("RC100 corrected (n = 100)", ("RC", DSc))]:
    for law in ("FLAT", "H(z)"):
        s, lo, hi, sd = row_stat(kind, data, law, PRIM)
        REF[(lab, law)] = (s, lo, hi, sd)
        cm = J222[lab][law]
        c7 = max(c7, abs(s - cm["stat"]), abs(lo - cm["lo"]), abs(hi - cm["hi"]))
check("C7 the exec'd CFG222 machinery reproduces CFG222's committed FLAT and H(z) primary-cell statistics and CIs on all six rows",
      f"max |difference| {c7:.1e}", c7 < 1e-9)


def zrange(kind, data):
    z = data["z"] if kind == "RC" else np.array([r["z"] for r in data])
    return z


def same_as_flat(law):
    return all(all(abs(ALL[law](float(z)) - 1.0) < 1e-12 for z in zrange(k, d)) for k, d in ROWS.values())


def theory_row(f):
    return {z: math.log10(max(f(z), FMIN)) for z in (0.85, 1.5, 2.5, 5.0)}


G3 = {}
P(f"  primary cell nu_mono canonical; verdict from the bootstrap 95% CI (CFG222's rule); SAME-AS-FLAT laws reuse FLAT's rows")
for law in ["FLAT", "H(z)"] + list(LAWS):
    th = theory_row(ALL[law])
    keeps = all(abs(v) <= 0.05 for v in th.values())
    saf = law not in ("FLAT", "H(z)") and same_as_flat(law)
    rows = {}
    for lab, (kind, data) in ROWS.items():
        if law == "FLAT" or saf:
            s, lo, hi, sd = REF[(lab, "FLAT")]
        elif law == "H(z)":
            s, lo, hi, sd = REF[(lab, "H(z)")]
        else:
            s, lo, hi, sd = row_stat(kind, data, law, PRIM)
        oth = {}
        if law not in ("FLAT", "H(z)") and not saf:
            for cell in CELLS[1:]:
                s2, l2, h2, sd2 = row_stat(kind, data, law, cell)
                oth[f"{cell[0]}|{cell[1]}"] = s2 / sd2
        rows[lab] = dict(stat=s, lo=lo, hi=hi, sd=sd, verdict=ns["verdict"](lo, hi), z_own_other_cells=oth)
    G3[law] = dict(theory_dex=th, keeps_flat=keeps, same_as_flat=saf, rows=rows)


def g3class(law):
    if G3[law]["same_as_flat"]:
        return "SAME-AS-FLAT"
    R, F = G3[law]["rows"], G3["FLAT"]["rows"]
    dis = lambda r: r["verdict"].startswith("DISFAV")
    for a, b in (("CRISTAL R_e, fit route, n = 12", "CRISTAL R_e, independent route, six class-A"),
                 ("CRISTAL R_out, fit route, six", "CRISTAL R_out, independent route, six")):
        if dis(R[a]) and dis(R[b]) and not (dis(F[a]) and dis(F[b])):
            return "WORSE-THAN-FLAT-ROBUST"
    for lab in R:
        if dis(R[lab]) and (not dis(F[lab]) or (R[lab]["verdict"] == F[lab]["verdict"] and abs(R[lab]["stat"]) > abs(F[lab]["stat"]) + 1e-9)):   # 1e-9: a floating-point tie is not 'larger' (disclosed)
            return "WORSE-THAN-FLAT-ROUTE-DEPENDENT"
    return "NOT-WORSE"


SHORT = ["RC100 slope", "R_e fit", "R_e ind", "R_out fit", "R_out ind"]
P(f"\n  {'law':32s} {'a0(z)/a0(0) dex at z=0.85/1.5/2.5/5':38s} {'flat?':6s} " + " ".join(f"{s:>14s}" for s in SHORT) + "  G3-data")
for law in G3:
    g = G3[law]
    cls = "(reference)" if law in ("FLAT", "H(z)") else g3class(law)
    g["class"] = cls
    P(f"  {law:32s} " + "/".join(f"{v:+.2f}" for v in g["theory_dex"].values()).ljust(38) + f" {'yes' if g['keeps_flat'] else 'no':6s} "
      + " ".join(f"{r['stat']:+.3f}{r['verdict'][:1] if r['verdict'] == 'CONSISTENT' else ('o' if r['verdict'].endswith('over') else 'u'):>1s}".rjust(14) for r in g["rows"].values()) + f"  {cls}")
P("  (row entries: statistic then C = CONSISTENT, o = DISFAVOURED-over, u = DISFAVOURED-under; RC100 = slope of delta on z, CRISTAL = median delta)")
P("  other three kernel/footing cells, z(own) per row, for the non-flat laws:")
for law in LAWS:
    if G3[law]["same_as_flat"]:
        continue
    P(f"    {law:32s} " + " | ".join(",".join(f"{v:+.1f}" for v in r["z_own_other_cells"].values()) for r in G3[law]["rows"].values()))
RES["numbers"]["G3"] = G3

# ================================================================================================ R3 / G4
banner("R3 / G4  BUBBLE COLLISION / BRANE CONTACT: what the repo can say (no CMB map in the repo)")
dists = []
with open(rp("real_research", "data", "SPARC_Lelli2016c.mrt")) as fh:
    for ln in fh:
        if len(ln) > 30 and re.match(r"^\s*\S+\s+\d+\s+\d", ln[:20] + " "):
            try:
                dists.append(float(ln.split()[2]))           # Galaxy, T, D (Mpc), ... (whitespace-separated)
            except ValueError:
                pass
d_max = max(dists) if dists else float("nan")
eps_need = {k: 2 * v * DM_STAR / d_max for k, v in A95_DIPOLE.items()}
P(f"  SPARC: {len(dists)} distances read, largest {d_max:.1f} Mpc; D_M(z*) = {DM_STAR:.0f} Mpc")
P(f"  local DE contrast across the SPARC volume: a0 ~ sqrt(rho_DE) -> dipole D = eps/2; A95 = 0.43 (0.40) -> eps < {2 * 0.43:.2f} ({2 * 0.40:.2f})")
P(f"  a horizon-scale gradient needs a total contrast eps = {eps_need['CFG182']:.0f} ({eps_need['CFG192']:.0f}) to reach A95 at the SPARC depth -> NON-DIAGNOSTIC (> 1)")
P("  CMB: NOT TESTED BY THE REPO.  Literature (memory, UNVERIFIED): Feeney, Johnson, Mortlock & Peiris 2011 searched WMAP7 for collision discs, flagged four"
  " candidates, evidence did not favour collisions (expected number of observable collisions bounded at order 1.6, 68%); follow-ups (Feeney et al. 2013;"
  " Osborne, Senatore & Smith 2013 on WMAP9; Planck isotropy papers 2013 XXIII, 2015 XVI, 2018 VII) report no detection; the large-angle anomalies sit at ~2-3 sigma"
  " with look-elsewhere caveats.  The owner's R3 names no direction, size, amplitude or time -> UNTESTABLE-AS-STATED.")
RES["numbers"]["R3"] = dict(sparc_dmax=d_max, DM_star=DM_STAR, eps_local_max={k: 2 * v for k, v in A95_DIPOLE.items()}, eps_horizon_needed=eps_need)

# ================================================================================================ load-bearing checks
banner("LOAD-BEARING CHECKS")
check("L1 the contact bites: some R2a grid point (A = 1) changes E(z) by more than 1e-3 at some z <= z*", f"max |E/E_LCDM - 1| = {L1MAX:.3e}", L1MAX > 1e-3)
check("L2 R1-lit contradicts the measured acoustic angle at >= 5 sigma", f"pull {pull_theta:+.1f} sigma", abs(pull_theta) >= 5)
l3a = max(abs(STEP[z]["dchi2"][0.0]) for z in STEP) if not MUT else L3MAX
l3a = max(l3a, max(abs(PULSE[z]["dchi2"][0.0]) for z in PULSE))
l3b = max(abs(ALL[k](z) - 1.0) for k in LAWS for z in (0.3, 1.2, 2.2, 4.4, 5.6)) if MUT else max(abs(f(z) - 1) for f in (law_step(2.0, 0.0), law_pulse(2.0, 0.0), law_w(-1.0)) for z in (0.3, 1.2, 2.2, 4.4, 5.6))
check("L3 LCDM is recovered exactly at zero amplitude (A = 0, B = 0, w = -1): Delta chi^2 = 0 and a0(z)/a0(0) = 1" + (" -- at EVERY grid point (MUTATE)" if MUT else ""),
      f"max |Delta chi^2| {l3a:.1e}; max |a0 ratio - 1| {l3b:.1e}", l3a < 1e-9 and l3b == 0.0)
if MUT:
    allsaf = all(G3[k]["same_as_flat"] for k in LAWS)
    check("M every G3 law reads SAME-AS-FLAT under MUTATE", f"{allsaf}", allsaf)

# ================================================================================================ verdicts
banner("VERDICT PER READING (never pooled; restatement is not a pass)")
stepA1 = {zc: v["class_A1"] for zc, v in STEP.items()}
excl_z = [zc for zc, c in stepA1.items() if c == "EXCLUDED"]
V = {}
V["R1-lit"] = "CONTRADICTED (G1: " + ", ".join(f"{k} {v:+.0f} sigma" for k, v in R1TAB.items()) + ")" if r1_fails else "not contradicted (MUTATE: the full past is the standard cosmology)"
V["R1-om"] = "UNTESTABLE-AS-STATED (a restatement of the standard past)"
V["R2a-step"] = (f"CONSTRAINED: A = 1 EXCLUDED for z_c in {excl_z}; A95 = " + ", ".join(f"{STEP[z]['A95']:.2f}@{z:g}" for z in ZC_GRID)
                 + f"; NON-DIAGNOSTIC/ALLOWED at A = 1 for z_c in {blind} on the repo's distances; G3: at A = 1 every z_c <= 5 run is "
                 + ", ".join(sorted(set(G3[k]["class"] for k in LAWS if k.startswith("STEP") and k.endswith("A=1")))) + " (framework-conditional: the a0 ~ sqrt(rho_DE) tie)")
V["R2a-pulse"] = "CONSTRAINED: B95 = " + ", ".join(f"{PULSE[z]['B95']:.2f}@{z:g}" for z in PULSE)
V["R2a-rec"] = (f"distances NON-DIAGNOSTIC (step at 1090, A = 1: dchi2 {STEP[1090.0]['dchi2'][1.0]:.2e}); flat a0 kept (restatement below z*); "
                f"amount E2/rho_L = {E2r:.3f}: p* (post-hoc); missing recombination radiation: UNTESTABLE now; fast-sink kinetics {pull_fast:+.0f} sigma at fixed parameters (illustrative)")
V["R2b-mono"] = f"{cls_mono} on the DESI DR2 CPL chains (f_mono = " + "/".join(f"{f:.1e}" for f in fm) + ")"
V["R2b-leak"] = "NON-DIAGNOSTIC (the CPL fits' own shape; needs a phantom epoch)"
V["R3"] = "UNTESTABLE-AS-STATED; the a0 dipole is NON-DIAGNOSTIC for a horizon-scale contact; CMB not in the repo"
for k, v in V.items():
    P(f"  {k:10s} {v}")
P("  G5 (declared, criteria 4.5): R1 +0; R2a-step +2; R2a-pulse +2; R2a-rec 0 added but its amount is post-hoc (no reduction credited); R2b >= +1; R3 >= +4.  No reading PASSES G5.")
P("  kappa = 1/2 FITTED.  No reading is graded as supported.")
RES["verdicts"] = V
head = ("HEADLINE: " + ("[MUTATE] zero amplitude recovers LCDM exactly at every grid point; the full past restores theta_*; L1 and L2 fail as required"
                        if MUT else f"R1-lit CONTRADICTED ({pull_theta:+.0f} sigma theta_*, {pull_yp:+.0f} Y_P, {pull_dh:+.0f} D/H); a step contact that switches all DE on is "
                        f"EXCLUDED for z_c in {excl_z[0] if excl_z else '-'}..{excl_z[-1] if excl_z else '-'} and invisible to the repo's distances above, while on the a0 = kappa c sqrt(G rho_DE) tie the z ~ 5 rows see it for z_c <= 5; R2b-mono {cls_mono}; recombination amount E2/rho_L = {E2r:.3f} (p*)"))
P("\n" + head)
nlb = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nlb}; {time.time() - T0:.0f} s")
RES["headline"] = head
rc = 0 if nlb == 0 else 1
P(f"rc = {rc}")
json.dump(RES, open(os.path.join(LANE, f"CFG254_handcheck_results{SFX}.json"), "w"), indent=1, default=lambda o: float(o) if isinstance(o, (np.floating,)) else str(o))
open(os.path.join(LANE, f"CFG254_handcheck{SFX}.out"), "w").write("\n".join(OUT_TXT).replace(REPO, "<repo>") + "\n")
sys.exit(rc)
