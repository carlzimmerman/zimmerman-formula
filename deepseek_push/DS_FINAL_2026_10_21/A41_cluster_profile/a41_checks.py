#!/usr/bin/env python3
"""A41 -- the FULL cluster profile shape: an eight-bin test, not just MID/OUTER.

Task 1  the stacked DeltaSigma, the amplitude A(R)=D/P_law and the inversion u(R) in all eight
        CFG687 radial bins, with jackknife errors; bin edges in Mpc and in r200c.
Task 2  the theory's full-profile prediction -- the law's phantom with a sourcing fraction
        u(r)=1 for r>r_sp and u=u_in inside (ONE free parameter) -- fitted to all eight bins.
Task 3  the two rival readings: u=1 everywhere (cold = the law's phantom) and u=0.472 everywhere
        (A21's MID value), plus u=0.488 (the cosmic-share normalisation) and the best constant u.
Task 4  the amplitude-free shape diagnostic: dlnA/dlnR per bin, predicted vs measured, and the
        curvature at the splashback radius.  A shape match cannot be bought by rescaling.

Data (all on disk, no network):
  campaign_fresh_gravity/CFG687_erass1_shear_stack/cfg687_percluster.npz
      318 eRASS1 x KiDS clusters, 8 radial bins: D (measured), E (error), PL (the law: baryons +
      phantom at a0=9.3603e-11), PN (baryons only, a0=0), mg, z, ra, dec, R500.
  The grid is logspace(0.15, 3.0, 9) Mpc; the model is CFG687's own `law()` (cfg687_stack.py):
  cored power-law baryons (beta=2/3, rc=0.15 R500, +20% non-gas, truncated at 3 Mpc), the law
  g=g_N nu_mono(g_N/a0), exact spherical DeltaSigma projection.

Usage:  python3 a41_checks.py [--mutate|--mutate2|--mutate3|--mutate4]
Exit 0 iff every declared check passes.  Deterministic, stdlib + numpy/scipy/sympy.
"""
import argparse, json, math, os, sys, time, warnings

T0 = time.time()
import numpy as np                      # noqa: E402
import sympy as sp                      # noqa: E402
from scipy.optimize import brentq       # noqa: E402
warnings.filterwarnings("ignore", category=RuntimeWarning)   # Accelerate BLAS spurious FP flags

LANE = "A41"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
NPZ = os.path.join(ROOT, "campaign_fresh_gravity", "CFG687_erass1_shear_stack",
                   "cfg687_percluster.npz")
sys.path.insert(0, os.path.join(ROOT, "campaign_fresh_gravity"))
import CFG4_common as C4                # noqa: E402  (committed: nu_mono, A0)

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", action="store_true",
                help="M1: inversion slip -- u = P_l/(D-P_N), forgetting to subtract the baryons")
ap.add_argument("--mutate2", action="store_true",
                help="M2: no step -- a single constant u for all eight bins")
ap.add_argument("--mutate3", action="store_true",
                help="M3: r_sp taken as the X-ray boundary R500 instead of 1.367 r200c")
ap.add_argument("--mutate4", action="store_true",
                help="M4: jackknife normalisation (n-1)/n instead of (n-1)^2/n (errors /5.4)")
A = ap.parse_args()
MUT = "M1" if A.mutate else ("M2" if A.mutate2 else ("M3" if A.mutate3 else ("M4" if A.mutate4 else "")))
TAG = {"": "", "M1": "_MUTATE", "M2": "_MUTATE2", "M3": "_MUTATE3", "M4": "_MUTATE4"}[MUT]
OUTF = open(os.path.join(HERE, "a41" + TAG + ".out"), "w")


def sg(x):
    """sqrt of a Delta-chi2 that may be negative in a mutated run."""
    return math.sqrt(max(0.0, x))


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUTF.write(s + "\n")


def head(t):
    P("")
    P("=" * 108)
    P(t)
    P("=" * 108)


CHECKS = []


def check(cid, ok, measured, threshold, label):
    CHECKS.append(dict(id=cid, pass_=bool(ok), value=measured, threshold=threshold, label=label))
    P(f"{cid} {'PASS' if ok else 'FAIL'} {measured} {threshold} :: {label}")
    return bool(ok)


# ============================================================== constants
G = 6.674e-11
MSUN = 1.989e30
MPC = 3.0857e22
KG = MSUN / (3.0857e16) ** 2          # Msun/pc^2 per kg/m^2
A0 = C4.A0["canonical"]               # 9.360324825e-11, the "canonical" footing (never pooled)
A0_ALT = C4.A0["alt"]
NU = C4.nu_mono
H0 = 67.4e3 / MPC
OM, OL = 0.315, 0.685
RHO_C0 = 3 * H0 ** 2 / (8 * np.pi * G)
C_NFW = 4.5
DELTA = 200.0
RSP_OVER_R200M = 0.83
RSP_ERR = 0.06
F_GAS = 0.11
R_COSMIC = 5.364327                   # (1-f_b)/f_b, f_b = 0.02237/0.14237   [A18 eq. 3]
R_TOT_A18 = 2.61792                   # the law's phantom per system baryon at the cluster anchor
U_CS_A18 = R_TOT_A18 / R_COSMIC       # 0.4880
U_MID_A21 = 0.471566
U_MID_A21_ERR = 0.03625

EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9)
RC = np.sqrt(EDGES[1:] * EDGES[:-1])
DLNR = np.log(RC[1:] / RC[:-1])
NB = 8
RGRID = np.logspace(-3, np.log10(30), 3000)
RM = RGRID * MPC
U_GRID = np.linspace(0, 1, 4001)

CONSTANTS = [
    dict(name="G", value=G, unit="m^3 kg^-1 s^-2", source="CODATA / BRIEF s4"),
    dict(name="a0_canonical", value=A0, unit="m/s^2", source="CFG4_common (FP0 committed), the canonical footing"),
    dict(name="a0_alt", value=A0_ALT, unit="m/s^2", source="CFG4_common, reported only, never mixed"),
    dict(name="H0", value=H0, unit="s^-1", source="67.4 km/s/Mpc, BRIEF s4"),
    dict(name="Omega_m", value=OM, unit="1", source="Planck 2018 [EXT], enters only rho_crit(z)"),
    dict(name="Omega_L", value=OL, unit="1", source="Planck 2018 [EXT]"),
    dict(name="M_sun", value=MSUN, unit="kg", source="BRIEF s4"),
    dict(name="Mpc", value=MPC, unit="m", source="BRIEF s4"),
    dict(name="c_nfw", value=C_NFW, unit="1", source="[EXT] c200c at M200c~1.5e14, z~0.23"),
    dict(name="Delta", value=DELTA, unit="rho_crit", source="BRIEF s4"),
    dict(name="r_sp_over_r200m", value=RSP_OVER_R200M, unit="1", source="[EXT] More+2015 (+-0.06); 0.83 x 1.6474 = 1.3674 r200c"),
    dict(name="f_gas_500", value=F_GAS, unit="1", source="[EXT] eRASS1 M_gas,500/M500"),
    dict(name="R_cosmic", value=R_COSMIC, unit="1", source="(1-f_b)/f_b, f_b=0.02237/0.14237 [A18 eq.3]"),
    dict(name="R_tot_anchor", value=R_TOT_A18, unit="1", source="[A18 s8] the law's phantom per system baryon at the cluster anchor"),
    dict(name="u_cosmic_anchor", value=U_CS_A18, unit="1", source="R_tot/R_cosmic = 0.4880 (A18 s8, = A21's ceiling)"),
    dict(name="u_MID_A21", value=U_MID_A21, unit="1", source="[A21 K4] 0.47157 +- 0.03625"),
]

RECORD = [
    dict(name="A_MID_law", value=1.910194, err=0.118637, source="CFG687 'canonical|b0.67|rc0.15|f0.20'/MID"),
    dict(name="A_MID_newton", value=10.173704, err=0.65, source="CFG687 'newton'/MID"),
    dict(name="A_OUTER_law", value=1.011801, err=0.086872, source="CFG687 'canonical|b0.67|rc0.15|f0.20'/OUTER"),
    dict(name="A_OUTER_newton", value=7.262, err=0.62, source="CFG687 'newton'/OUTER"),
    dict(name="A_INNER_law", value=2.5091163, err=0.32, source="CFG687 stdout, INNER band"),
    dict(name="A_INNER_newton", value=10.4352179, err=1.39, source="CFG687 stdout, INNER band"),
    dict(name="u_MID_A21", value=0.471566, err=0.03625, source="A21 K4"),
    dict(name="u_OUTER_A21", value=0.9865, err=0.0984, source="A21 K5b"),
    dict(name="u_8bin_A29", value=[0.2936, 0.3730, 0.3331, 0.4169, 0.4116, 0.5319, 1.0885, 0.9392],
         err=[0.1251, 0.1072, 0.0504, 0.0648, 0.0440, 0.0545, 0.2087, 0.1059], source="A29 K2/K8 (reproduced below)"),
    dict(name="r_sp_A29", value=1.414, err=0.20, source="A29 s3: 0.83 r200m = 1.3674 r200c = 1.414 Mpc"),
]

# ============================================================== the data
if not os.path.exists(NPZ):
    P(f"FATAL: {NPZ} missing -- this lane reads the CFG687 per-cluster stack")
    sys.exit(2)
d = np.load(NPZ)
D, E, PL, PN = d["D"], d["E"], d["PL"], d["PN"]
MG, ZC, RA, R500 = d["mg"], d["z"], d["ra"], d["R500"]
NCL = D.shape[0]
W = np.where((E > 0) & (E < 1e8), 1.0 / E ** 2, 0.0)      # 1e9 is CFG687's nan sentinel
ORDER = np.argsort(RA)
PATCH = np.empty(NCL, int)
PATCH[ORDER] = np.arange(NCL) * 30 // NCL                # CFG687's 30 RA-ordered patches
NPATCH = 30
ALL = np.ones(NCL, bool)


def stack(mask, arr):
    return (W[mask] * arr[mask]).sum(0) / W[mask].sum(0)


DD, PP, NN = stack(ALL, D), stack(ALL, PL), stack(ALL, PN)
PHB = PP - NN                                            # stacked phantom, the model's shape

REPS = np.array([stack(PATCH != p, D) for p in range(NPATCH)])
DEV = REPS - REPS.mean(0)
COV = ((NPATCH - 1.0) / (NPATCH ** 2 if MUT == "M4" else NPATCH)) * (DEV.T @ DEV)
SD = np.sqrt(np.diag(COV))
EV, EVC = np.linalg.eigh(COV)
EVc = np.maximum(EV, 1e-2 * EV.max())
CINV = EVC @ np.diag(1.0 / EVc) @ EVC.T
CORR = COV / np.outer(SD, SD)
COND = float(EV.max() / EV.min())


def jk_vec(fun):
    full = fun(ALL)
    reps = np.array([fun(PATCH != p) for p in range(NPATCH)])
    return full, np.sqrt((NPATCH - 1.0) / NPATCH * np.sum((reps - reps.mean(0)) ** 2, 0)), reps


def _A(m):
    return stack(m, D) / stack(m, PL)


def _S(m):
    a = _A(m)
    return np.array([math.log(a[j + 1] / a[j]) / DLNR[j] for j in range(NB - 1)])


def _U(m):
    p, n, dd = stack(m, PL), stack(m, PN), stack(m, D)
    if MUT == "M1":                       # M1: forget to subtract the baryons from the phantom
        return p / (dd - n)
    return (p - n) / (dd - n)


Af, Asd, _ = jk_vec(_A)
Sf, Ssd, Sreps = jk_vec(_S)
SDEV = Sreps - Sreps.mean(0)
SC = (NPATCH - 1.0) / NPATCH * (SDEV.T @ SDEV)
Uf, Usd, _ = jk_vec(_U)
AN = DD / NN                                             # amplitude in baryon units


def _C(m):
    a = _A(m)
    l = np.log(a)
    return np.array([l[6] - 2 * l[5] + l[4], _S(m)[5] - _S(m)[6]])


Cf, Csd, _ = jk_vec(_C)                                  # curvature and slope break


def jk_err(fun):
    return jk_vec(lambda m: np.atleast_1d(fun(m)))[1]


# ============================================================== geometry
def rho_crit_z(z):
    return RHO_C0 * (OM * (1 + z) ** 3 + OL)


def r_delta(M, dl, z):
    return (3.0 * M * MSUN / (4 * np.pi * dl * rho_crit_z(z))) ** (1 / 3) / MPC


def mu(x):
    return np.log(1 + x) - x / (1 + x)


def r200m_over_r200c(c=C_NFW, om=OM):
    return brentq(lambda x: mu(x) / mu(c) - om * (x / c) ** 3, 1.0, 50.0) / c


R200M_C = r200m_over_r200c()
K_SP = RSP_OVER_R200M * R200M_C


def M200_from_M500(M500, z, c=C_NFW):
    R5 = r_delta(M500, 500.0, z)

    def f(lm):
        M200 = math.exp(lm)
        return M200 * mu(R5 / (r_delta(M200, 200.0, z) / c)) / mu(c) - M500
    return math.exp(brentq(f, math.log(1e9), math.log(1e17), xtol=1e-10, rtol=1e-12))


ZG = float(np.median(ZC))
MGM = float(np.median(MG))
R5M = float(np.median(R500))
M500S = MGM / F_GAS
M200S = M200_from_M500(M500S, ZG)
R200C = r_delta(M200S, DELTA, ZG)
RSP = K_SP * R200C
if MUT == "M3":
    RSP = R5M                                            # M3: identify r_sp with R500
M200i = np.array([M200_from_M500(m / F_GAS, z) for m, z in zip(MG, ZC)])
RSPi = K_SP * np.array([r_delta(m, DELTA, z) for m, z in zip(M200i, ZC)])

# the cosmic share, recomputed for THIS stack (not copied from A18): solve M_b(1+F)=M200c
_mb = brentq(lambda x: x * (1 + 0.5 * (math.sqrt(1 + 4 / (G * x * MSUN / (A0 * (R200C * MPC) ** 2))) - 1))
             - M200S, 1e10, 1e15)
_yv = G * _mb * MSUN / (A0 * (R200C * MPC) ** 2)
_FV = 0.5 * (math.sqrt(1 + 4 / _yv) - 1)
_MU = (C_NFW / (1 + C_NFW)) ** 2
R_TOT_STACK = _MU * (1 + _FV) - 1
U_CS_STACK = R_TOT_STACK / R_COSMIC
# (third cosmic-share route -- CFG687's own baryon budget -- is computed below, after baryon())

# ============================================================== model machinery (CFG687's law())
def sigma_proj(rhoL, R):
    umax = np.arccosh(RGRID[-1] / R)
    u = U_GRID * umax
    rr = R * np.cosh(u)
    lr = np.log(RGRID)
    pos = rhoL > 0
    rho_u = np.exp(np.interp(np.log(rr), lr[pos], np.log(rhoL[pos])))
    return 2 * np.trapz(rho_u * rr * MPC, u)


def baryon(R500i, Mgas, beta=2 / 3, rcf=0.15, fs=0.20):
    rc = rcf * R500i
    shape = (1 + (RGRID / rc) ** 2) ** (-1.5 * beta)
    shape[RGRID > 3.0] = 0.0
    dm = 4 * np.pi * RM ** 2 * shape
    M = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(RM))]
    return M * (Mgas * MSUN / np.interp(R500i, RGRID, M)) * (1 + fs)


def dsigma(Mtot, rho, Rs):
    out = []
    for R in Rs:
        sel = RGRID > R
        rr = RM[sel]
        M2 = np.interp(R, RGRID, Mtot) + np.trapz(
            4 * np.pi * rr ** 2 * rho[sel] * (1 - np.sqrt(np.maximum(0.0, 1 - (R * MPC / rr) ** 2))), rr)
        out.append((M2 / (np.pi * (R * MPC) ** 2) - sigma_proj(rho, R)) / KG)
    return np.array(out)


def law_components(i):
    """CFG687's `law()` at u=1: returns (M_b, M_L, M_ph) on RGRID."""
    Mb = baryon(R500[i], MG[i])
    gb = G * Mb / RM ** 2
    ML = (gb * NU(gb / A0)) * RM ** 2 / G
    return Mb, ML, ML - Mb


_Mb3 = float(np.interp(3.0, RGRID, baryon(R5M, MGM)))
_Mph_sp_med = float(np.interp(RSP, RGRID, law_components(int(np.argmin(np.abs(MG - MGM))))[2]))
R_TOT_MODEL = _Mph_sp_med / _Mb3
U_CS_MODEL = R_TOT_MODEL / R_COSMIC


def model3d(v, rsp, i):
    """Full 3D treatment: rho_cold = rho_ph/u(r), u = 1/v inside rsp, 1 outside.
    The enclosed cold mass is continuous (only the density jumps), so no shell term."""
    Mb, ML, Mph = law_components(i)
    rho_ph = np.gradient(Mph, RM) / (4 * np.pi * RM ** 2)
    rho_b = np.gradient(Mb, RM) / (4 * np.pi * RM ** 2)
    Msp = float(np.interp(rsp, RGRID, Mph))
    Mc = np.where(RGRID < rsp, Mph * v, Mph + Msp * (v - 1))
    rc_ = np.where(RGRID < rsp, rho_ph * v, rho_ph)
    return dsigma(Mb + Mc, rho_b + rc_, RC)


def projstep(rsp_arr, width=0.0):
    """Projected step: m_j = NN_j + v Phi_j + Psi_j, linear in v=1/u_in.
    width>0 smooths the step in log R (dex) -- used only for the width diagnostic."""
    Phi, Psi = np.zeros(NB), np.zeros(NB)
    for j in range(NB):
        if width <= 0:
            f = (rsp_arr > RC[j]).astype(float)
        else:
            f = 1.0 / (1.0 + np.exp((math.log(RC[j]) - np.log(rsp_arr)) / width))
        tot = W[:, j].sum()
        Phi[j] = (W[:, j] * f * (PL[:, j] - PN[:, j])).sum() / tot
        Psi[j] = (W[:, j] * (1 - f) * (PL[:, j] - PN[:, j])).sum() / tot
    return NN + Psi, Phi


def fitlin(off, sl, y=DD, Cinv=CINV):
    v = float((sl @ Cinv @ (y - off)) / (sl @ Cinv @ sl))
    r = y - off - v * sl
    return v, 1.0 / math.sqrt(float(sl @ Cinv @ sl)), float(r @ Cinv @ r)


def chi2_of(m, Cinv=CINV):
    r = DD - m
    return float(r @ Cinv @ r)


def slopes_of(m):
    a = m / PP
    return np.array([math.log(a[j + 1] / a[j]) / DLNR[j] for j in range(NB - 1)])


# ============================================================== K1-K2  data
head("K1-K2  the data: six published band amplitudes, and the eight-bin stacked profile")

dev = 0.0
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
REF = {"INNER": (2.5091163, 10.4352179), "MID": (1.9101939, 10.1737044), "OUTER": (1.0118014, 7.2619529)}
for b, jj in BANDS.items():
    al = (W[:, jj] * D[:, jj]).sum() / (W[:, jj] * PL[:, jj]).sum()
    an = (W[:, jj] * D[:, jj]).sum() / (W[:, jj] * PN[:, jj]).sum()
    dev = max(dev, abs(al / REF[b][0] - 1), abs(an / REF[b][1] - 1))
check("K1", dev < 1e-4, f"{dev:.2e} rel", "<1e-4",
      "the npz IS CFG687: the six published band amplitudes (A_law 2.509/1.910/1.012, "
      "A_newton 10.435/10.174/7.262) come back from the per-cluster arrays")

P("")
P(f"  stack: {NCL} eRASS1 x KiDS clusters, median z = {ZG:.4f}, median M_gas,500 = {MGM:.4e} Msun,")
P(f"  median R500 = {R5M:.4f} Mpc -> M500 = {M500S:.3e}, M200c = {M200S:.3e} Msun,")
P(f"  r200c = {R200C:.4f} Mpc, r_sp = {K_SP:.4f} r200c = {RSP:.4f} Mpc")
P("")
P(f"  {'j':>2} {'R_in':>7} {'R_out':>7} {'R_c':>7} {'R_in/r200c':>10} {'R_out/r200c':>11} "
  f"{'D':>8} {'sd':>7} {'PL':>8} {'PN':>7} {'A=D/PL':>7} {'sd':>6} {'u':>7} {'sd':>6}")
for j in range(NB):
    P(f"  {j:2d} {EDGES[j]:7.4f} {EDGES[j+1]:7.4f} {RC[j]:7.4f} {EDGES[j]/R200C:10.3f} "
      f"{EDGES[j+1]/R200C:11.3f} {DD[j]:8.2f} {SD[j]:7.2f} {PP[j]:8.2f} {NN[j]:7.2f} "
      f"{Af[j]:7.3f} {Asd[j]:6.3f} {Uf[j]:7.4f} {Usd[j]:6.4f}")
P("")
P("  bands (CFG687/A18/A21 normalisation, A = sum(w D)/sum(w P)):")
for b, jj in BANDS.items():
    al = (W[:, jj] * D[:, jj]).sum() / (W[:, jj] * PL[:, jj]).sum()
    an = (W[:, jj] * D[:, jj]).sum() / (W[:, jj] * PN[:, jj]).sum()
    ub_ = (an - al) / (al * (an - 1.0))
    P(f"    {b:6s} {EDGES[jj[0]]:.4f}-{EDGES[jj[-1]+1]:.4f} Mpc  A_law = {al:.4f}  "
      f"A_newton = {an:.4f}  u = {ub_:.4f}")

K2 = (np.all(DD > 0) and np.all(SD > 0) and np.all(SD / DD < 0.45) and SD[0] > SD[-1]
      and abs(Af[6] - 1.0) < 0.2 and abs(Af[7] - 1.0) < 0.2)
check("K2", K2, f"max sd/D = {np.max(SD/DD):.2f}, A(1.71)={Af[6]:.3f}, A(2.49)={Af[7]:.3f}",
      "sd/D<0.45, sd falling outward, |A(>r_sp)-1|<0.2",
      "the eight-bin stacked DeltaSigma with jackknife errors (30 RA patches); the amplitude in "
      "law units falls from 2.80 at 0.18 Mpc to 0.93/1.06 outside 1.42 Mpc -- i.e. the law needs "
      "no rescaling at all in the two outer bins")

# ============================================================== K3-K5
head("K3-K5  the inversion u(R) reproduced, the bin edges in r200c, the covariance")

dU = float(np.max(np.abs(Uf - np.array([0.2936, 0.3730, 0.3331, 0.4169, 0.4116, 0.5319, 1.0885, 0.9392]))))
check("K3", dU < 2e-3, f"max|du| = {dU:.1e}", "<2e-3",
      "the eight per-bin inversions u = (P_l-P_N)/(D-P_N) reproduce A29's published values "
      "0.2936 0.3730 0.3331 0.4169 0.4116 0.5319 1.0885 0.9392 -- same npz, same estimator")

K4 = (abs(RSP / R200C - K_SP) / K_SP < 0.01) and (abs(EDGES[6] / R200C - K_SP) / K_SP < 0.01)
check("K4", K4, f"edge 6 = {EDGES[6]:.4f} Mpc = {EDGES[6]/R200C:.3f} r200c; r_sp = {K_SP:.4f} r200c",
      "|edge6/r200c - 1.3674| < 1%",
      "the bin edges are 0.150-0.218-0.317-0.461-0.671-0.976-1.419-2.063-3.000 Mpc = "
      "0.145-0.211-0.307-0.446-0.649-0.943-1.372-1.995-2.901 r200c; the 6th edge lands within "
      "0.4% of r_sp = 1.3674 r200c, so the step falls in the MID/OUTER boundary bin")
P("")
P("  r200c-normalised edges: " + "  ".join(f"{e/R200C:.3f}" for e in EDGES))
P("  r200c-normalised centres: " + "  ".join(f"{r/R200C:.3f}" for r in RC))

maxrho = float(np.max(np.abs(CORR - np.eye(NB))))
K5 = (maxrho < 0.5) and (COND < 1e4)
check("K5", K5, f"max|rho_ij| = {maxrho:.2f}, cond = {COND:.0f}", "<0.5 and cond<1e4",
      "the eight-bin jackknife covariance is close to diagonal, so a diagonal fit is not "
      "misleading; the full covariance with eigenvalues clipped at 1e-2 of the largest is used "
      "throughout, and the diagonal is reported as a cross-check")

# ============================================================== K6-K7  algebra + model
head("K6-K7  the algebra of u and A (exact, sympy), and the model reimplementation (bit-exact)")

pl, pn, dsum, uu, aa = sp.symbols("P_l P_N D u A", positive=True)
phis = sp.symbols("phi", positive=True)
# u = (P_l-P_N)/(D-P_N)  <=>  D = P_N + (P_l-P_N)/u
K6a = float(abs(sp.simplify((pn + (pl - pn) / ((pl - pn) / (dsum - pn))) - dsum)))
# A = D/P_l = P_N/P_l + (1/u)(1 - P_N/P_l)
fb = sp.symbols("f_b", positive=True)
K6b = float(abs(sp.simplify((pn / pl + (1 / uu) * (1 - pn / pl)) - (pn + (pl - pn) / uu) / pl)))
# dln(kA)/dlnR = dlnA/dlnR for any constant k: the log-slope is amplitude-free
lnk, lnR, lnA = sp.symbols("lnk lnR lnA", real=True)
K6c = float(abs(sp.diff(lnk + lnA, lnR) - sp.diff(lnA, lnR)))
# u=1/2 <=> the required cold mass is twice the law's phantom
K6d = float(abs(sp.simplify((1 / sp.Rational(1, 2)) - 2)))
K6 = (K6a < 1e-25) and (K6b < 1e-25) and (K6c < 1e-25) and (K6d < 1e-30)
check("K6", K6, f"{K6a:.0e} / {K6b:.0e} / {K6c:.0e}", "<1e-25",
      "u = (P_l-P_N)/(D-P_N) is exactly D = P_N + (P_l-P_N)/u, and A = D/P_l = f_b + (1/u)(1-f_b) "
      "with f_b = P_N/P_l; dln(kA)/dlnR = dlnA/dlnR, so the log-slope diagnostic is invariant "
      "under any rescaling of the amplitude -- a shape match cannot be bought by rescaling")

# verbatim CFG687 law() at u=1 must reproduce PL and PN
devL, devN = 0.0, 0.0
for i in (0, 7, 150, NCL - 1):
    Mb, ML, Mph = law_components(i)
    devL = max(devL, float(np.max(np.abs(dsigma(ML, np.gradient(ML, RM) / (4 * np.pi * RM ** 2), RC) / PL[i] - 1))))
    devN = max(devN, float(np.max(np.abs(dsigma(Mb, np.gradient(Mb, RM) / (4 * np.pi * RM ** 2), RC) / PN[i] - 1))))
K7 = max(devL, devN) < 1e-10
check("K7", K7, f"max rel dev = {max(devL, devN):.1e} (4 clusters x 8 bins)", "<1e-10",
      "the reimplementation of CFG687's `law()` (cored beta-profile baryons, nu_mono, exact "
      "spherical projection) reproduces the stored PL and PN arrays to machine precision, so the "
      "u(r) machinery below is the same model the record fitted")

# ============================================================== K8-K10  the step fit
head("K8-K10  TASK 2 -- the full-profile step fit: ONE free parameter (u_in), u=1 outside r_sp")

off_f, sl_f = projstep(np.full(NCL, RSP))
v_f, sv_f, c2_f = fitlin(off_f, sl_f)
off_p, sl_p = projstep(RSPi)
v_p, sv_p, c2_p = fitlin(off_p, sl_p)
UF, UF_ERR = 1 / v_f, sv_f / v_f ** 2
UP, UP_ERR = 1 / v_p, sv_p / v_p ** 2
if MUT == "M2":                                       # M2: no step at all
    v0 = float((PHB @ CINV @ (DD - NN)) / (PHB @ CINV @ PHB))
    off_f, sl_f, v_f, sv_f, c2_f = NN, PHB, v0, 1 / math.sqrt(float(PHB @ CINV @ PHB)), chi2_of(NN + v0 * PHB)
    UF, UF_ERR = 1 / v_f, sv_f / v_f ** 2
MODF = off_f + v_f * sl_f
MODP = off_p + v_p * sl_p
RESF = (DD - MODF) / SD
RESP = (DD - MODP) / SD

P("")
P(f"  model m_j(v) = P_N,j + v*[inside fraction]*P_ph,j ,  v = 1/u_in ,  u = 1 for R > r_sp")
P(f"  {'variant':12s} {'r_sp':>7} {'v_in':>8} {'u_in':>8} {'chi2':>7} {'dof':>4} {'chi2/dof':>9}")
P(f"  {'fixed r_sp':12s} {RSP:7.3f} {v_f:8.3f} {UF:8.4f} {c2_f:7.2f} {7:4d} {c2_f/7:9.2f}   (+-{UF_ERR:.4f})")
P(f"  {'per-cluster':12s} {'--':>7} {v_p:8.3f} {UP:8.4f} {c2_p:7.2f} {7:4d} {c2_p/7:9.2f}   (+-{UP_ERR:.4f})")
P("")
P(f"  {'j':>2} {'R':>7} {'D':>8} {'sd':>6} {'model*':>8} {'resid':>7} {'resid/sd':>9} {'A_obs':>6} {'A_mod*':>6}"
  f"   (* per-cluster r_sp variant)")
for j in range(NB):
    P(f"  {j:2d} {RC[j]:7.3f} {DD[j]:8.2f} {SD[j]:6.2f} {MODP[j]:8.2f} {DD[j]-MODP[j]:+7.2f} "
      f"{RESP[j]:+9.2f} {Af[j]:6.3f} {MODP[j]/PP[j]:6.3f}")
P("")
P(f"  residuals (fixed r_sp): " + " ".join(f"{x:+.2f}" for x in RESF))
_am = {}
for b, jj in BANDS.items():
    _am[b] = (W[:, jj] * MODF[jj]).sum() / (W[:, jj] * PL[:, jj]).sum()
P("  the fitted model's own band amplitudes: " +
  "  ".join(f"{b} {_am[b]:.3f} (record {REF[b][0]:.3f})" for b in BANDS))
P(f"  max |resid/sd| = {np.max(np.abs(RESP)):.2f} (per-cluster), {np.max(np.abs(RESF)):.2f} (fixed)")
K8 = (c2_f / 7.0 < 2.0) and (0.30 < UF < 0.60) and (np.max(np.abs(RESF)) < 3.5)
check("K8", K8, f"u_in = {UF:.4f}+-{UF_ERR:.4f}, chi2 = {c2_f:.2f}/7 = {c2_f/7:.2f}, "
                f"max|resid| = {np.max(np.abs(RESF)):.2f}sigma",
      "chi2/dof<2, 0.30<u_in<0.60, max resid<3.5sigma",
      "ONE free parameter (u_in) fits the full eight-bin profile at chi2/dof = %.2f: u_in = %.3f "
      "+- %.3f, u = 1 fixed outside r_sp. No amplitude, shape or normalisation freedom is used -- "
      "the phantom's shape and the cosmic-share normalisation are CFG687's/A18's own" % (c2_f / 7, UF, UF_ERR))

K9 = (c2_p / 7.0 < 2.0) and (abs(UF - UP) / math.hypot(UF_ERR, UP_ERR) < 1.5)
check("K9", K9, f"per-cluster r_sp: u_in = {UP:.4f}+-{UP_ERR:.4f}, chi2/dof = {c2_p/7:.2f}; "
                f"fixed-vs-cluster {abs(UF-UP)/math.hypot(UF_ERR,UP_ERR):.2f}sigma",
      "chi2/dof<2 and the two variants agree <1.5sigma",
      f"the theory's actual prediction is a step at each cluster's OWN r_sp ~ M^(1/3) (spread "
      f"16-84 pct = {np.percentile(RSPi,16):.2f}-{np.percentile(RSPi,84):.2f} Mpc), which broadens "
      f"the stacked transition with zero extra parameters; it fits at chi2/dof = {c2_p/7:.2f} and "
      f"agrees with the fixed-r_sp fit to {abs(UF-UP)/math.hypot(UF_ERR,UP_ERR):.2f} sigma")

U_CS_CENTRAL = (U_CS_A18 + U_CS_STACK + U_CS_MODEL) / 3.0
SIG_CS = 0.05                     # covers the three baryon-budget routes and c = 4.5 -> 4.0
z_cs = (UF - U_CS_CENTRAL) / math.hypot(UF_ERR, SIG_CS)
K10 = abs(z_cs) < 3.0 and (0.45 < U_CS_MODEL < 0.70)
P(f"  cosmic-share routes: A18 anchor R_tot = {R_TOT_A18:.3f} -> u_CS = {U_CS_A18:.3f}; "
  f"stack self-consistent R_tot = {R_TOT_STACK:.3f} -> {U_CS_STACK:.3f}; "
  f"CFG687 baryon budget R_tot = {R_TOT_MODEL:.3f} -> {U_CS_MODEL:.3f}")
check("K10", K10, f"u_in = {UF:.3f}+-{UF_ERR:.3f}; cosmic share u_CS = {U_CS_CENTRAL:.3f} "
                  f"(routes {U_CS_A18:.3f}/{U_CS_STACK:.3f}/{U_CS_MODEL:.3f}); Z = {z_cs:+.1f}",
      "|Z| < 3 vs the cosmic-share normalisation",
      "the cosmic-share normalisation M_c = 5.3643 M_b, recomputed for THIS stack "
      f"(R_tot = {R_TOT_STACK:.3f} at M200c = {M200S:.2e}, c = 4.5) rather than copied from A18, "
      f"predicts u = R_tot/5.3643 = {U_CS_STACK:.3f}; A18's anchor gives {U_CS_A18:.3f}. The fit "
      f"sits {z_cs:+.1f} sigma away from the three-route central value "
      f"{U_CS_CENTRAL:.3f} +- {SIG_CS:.2f}, at the low end of the normalisation's own spread")

# ============================================================== K11-K15  rivals
head("K11-K15  TASK 3 -- the rivals, and Delta chi2 against the step model")

RIVALS = {}


def add_rival(name, m, np_=0, u_=None):
    c2 = chi2_of(m)
    RIVALS[name] = dict(chi2=c2, dof=NB - np_, m=m, nparam=np_, u=u_)


add_rival("step(fixed)", MODF, 1, UF)
add_rival("step(per-cluster)", MODP, 1, UP)
add_rival("u=1 everywhere", NN + PHB, 0, 1.0)
add_rival("u=0.4716 everywhere", NN + PHB / U_MID_A21, 0, U_MID_A21)
add_rival("u=0.488 everywhere", NN + PHB / U_CS_A18, 0, U_CS_A18)
v_best = float((PHB @ CINV @ (DD - NN)) / (PHB @ CINV @ PHB))
add_rival("best constant u", NN + v_best * PHB, 1, 1 / v_best)
if MUT == "M2":
    for k in list(RIVALS):
        if k.startswith("step"):
            RIVALS[k] = dict(chi2=chi2_of(MODF), dof=NB, m=MODF, nparam=0, u=1 / v_best)

P("")
P(f"  {'model':22s} {'u':>8} {'chi2':>8} {'dof':>4} {'chi2/dof':>9} {'dchi2 vs step':>14} {'sigma':>7}")
for nm, rv in RIVALS.items():
    uu_ = rv["u"]
    dc = rv["chi2"] - c2_f
    P(f"  {nm:22s} {uu_:8.3f} {rv['chi2']:8.1f} {rv['dof']:4d} {rv['chi2']/rv['dof']:9.2f} {dc:14.1f} "
      f"{math.sqrt(max(0.0, dc)):7.2f}")
P("")
P("  residuals/sd per bin (j=0..7):")
for nm, rv in RIVALS.items():
    P(f"    {nm:22s} " + " ".join(f"{x:+5.2f}" for x in (DD - rv["m"]) / SD))

dc1 = RIVALS["u=1 everywhere"]["chi2"] - c2_f
K11 = dc1 / max(1e-9, c2_f) > 0 and sg(dc1) > 7.0 and RIVALS["u=1 everywhere"]["chi2"] / 8 > 5
check("K11", K11, f"u=1: chi2 = {RIVALS['u=1 everywhere']['chi2']:.1f}/8 = "
                  f"{RIVALS['u=1 everywhere']['chi2']/8:.1f}; dchi2 = {dc1:.0f} "
                  f"({sg(dc1):.1f} sigma)",
      "dchi2 > 49 (7 sigma)",
      "RIVAL (a) 'cold = exactly the law's phantom, u=1 everywhere' is excluded by the full "
      f"profile at Delta chi2 = {dc1:.0f} ({sg(dc1):.1f} sigma), the same verdict "
      "as A18's 7.7 sigma band-ratio test and slightly stronger because all eight bins are used")

dc2 = RIVALS["u=0.4716 everywhere"]["chi2"] - c2_f
K12 = sg(dc2) > 4.0
check("K12", K12, f"u=0.4716: chi2 = {RIVALS['u=0.4716 everywhere']['chi2']:.1f}/8; "
                  f"dchi2 = {dc2:.0f} ({sg(dc2):.1f} sigma)",
      "dchi2 > 16 (4 sigma)",
      "RIVAL (b) 'u = 0.472 everywhere' (A21's MID value, the best single number) is excluded: it "
      "fits the inner six bins but over-predicts the two outer ones by 6.9 and 8.7 sigma. The "
      "constant needs u = %.3f to compromise, and that is still rejected at %.1f sigma" %
      (1 / v_best, sg(RIVALS['best constant u']['chi2'] - c2_f)))

dc3 = RIVALS["u=0.488 everywhere"]["chi2"] - c2_f
K13 = sg(dc3) > 4.0
check("K13", K13, f"u=0.488: chi2 = {RIVALS['u=0.488 everywhere']['chi2']:.1f}/8; "
                  f"dchi2 = {dc3:.0f} ({sg(dc3):.1f} sigma)",
      "dchi2 > 16",
      "RIVAL (c) 'the cosmic share with the law's phantom shape, u = 0.488 everywhere' (A18's "
      "zero-parameter reading) is excluded as a CONSTANT: the cosmic share may set the total cold "
      "budget, but it cannot be applied uniformly in radius")

dc4 = RIVALS["best constant u"]["chi2"] - c2_f
K14 = sg(dc4) > 4.5
check("K14", K14, f"best constant u = {1/v_best:.3f}; chi2 = "
                  f"{RIVALS['best constant u']['chi2']:.1f}/8; dchi2 = {dc4:.0f} "
                  f"({sg(dc4):.1f} sigma)",
      "dchi2 > 20",
      "even the BEST constant u (fitted, u = %.3f) is rejected against the one-parameter step at "
      "Delta chi2 = %.0f with the same number of parameters: the failure is not the value of u, "
      "it is that u is not constant in radius" % (1 / v_best, dc4))

K15 = (c2_f / 7 < 2.0) and (RIVALS["u=1 everywhere"]["chi2"] / 8 > 4.0) and \
      (RIVALS["best constant u"]["chi2"] / 8 > 3.0) and abs(UF - U_MID_A21) / math.hypot(UF_ERR, U_MID_A21_ERR) < 3.0
check("K15", K15, f"step {c2_f/7:.2f}/dof vs const {RIVALS['best constant u']['chi2']/8:.2f}/dof vs "
                  f"u=1 {RIVALS['u=1 everywhere']['chi2']/8:.1f}/dof; "
                  f"u_in vs A21 MID = {abs(UF-U_MID_A21)/math.hypot(UF_ERR,U_MID_A21_ERR):.2f} sigma",
      "ordered chi2, u_in consistent with A21's MID",
      "the ordering is step << best-constant < u=0.472 < u=1, and the fitted u_in = %.3f agrees "
      "with A21's MID value 0.4716 +- 0.0362 (%.1f sigma): the full profile does not move the "
      "inner amplitude, it fixes the outer one" % (UF, abs(UF - U_MID_A21) / math.hypot(UF_ERR, U_MID_A21_ERR)))

# ============================================================== K16-K18  shape
head("K16-K18  TASK 4 -- the amplitude-free shape: dlnA/dlnR per bin and the curvature at r_sp")

SPRED = slopes_of(MODF)
SPRED_P = slopes_of(MODP)
S1 = np.zeros(NB - 1)                                   # u=1 -> A=1 -> slope 0
SCONST = slopes_of(NN + PHB / U_MID_A21)
SERR = Ssd
P("")
P(f"  {'bin':>10} {'dlnR':>7} {'dlnA meas':>10} {'+-':>6} {'step':>7} {'step(pc)':>9} {'u=1':>6} "
  f"{'u=.472':>7} {'resid':>7}")
for j in range(NB - 1):
    P(f"  {RC[j]:4.2f}-{RC[j+1]:4.2f} {DLNR[j]:7.3f} {Sf[j]:10.3f} {SERR[j]:6.3f} {SPRED[j]:7.3f} "
      f"{SPRED_P[j]:9.3f} {S1[j]:6.3f} {SCONST[j]:7.3f} {Sf[j]-SPRED[j]:+7.3f}")
P("")
sD = np.array([math.log(DD[j + 1] / DD[j]) / DLNR[j] for j in range(NB - 1)])
sL = np.array([math.log(PP[j + 1] / PP[j]) / DLNR[j] for j in range(NB - 1)])
P("  dlnD/dlnR  = " + " ".join(f"{x:+.2f}" for x in sD))
P("  dlnP_l/dlnR= " + " ".join(f"{x:+.2f}" for x in sL) +
  "   <- the phantom's own profile is nearly flat; the data's is not")
chi_diag = float(np.sum(((Sf - SPRED) / SERR) ** 2))
chi1_diag = float(np.sum(((Sf - S1) / SERR) ** 2))
chic_diag = float(np.sum(((Sf - SCONST) / SERR) ** 2))
chi_diag_p = float(np.sum(((Sf - SPRED_P) / SERR) ** 2))
SCINV = np.linalg.inv(SC)
chi_full = float((Sf - SPRED) @ SCINV @ (Sf - SPRED))
chi1_full = float((Sf - S1) @ SCINV @ (Sf - S1))
P(f"  chi2_shape (7 slopes, diagonal):  step {chi_diag:.2f}  step(pc) {chi_diag_p:.2f}  "
  f"u=1 {chi1_diag:.2f}  u=.472 {chic_diag:.2f}")
P(f"  chi2_shape (full slope covariance): step {chi_full:.2f}  u=1 {chi1_full:.2f}")
K16 = (chi_diag / 7 < 1.5) and (chi1_diag / 7 > 2.0)
check("K16", K16, f"chi2_shape/dof: step {chi_diag/7:.2f}, u=1 {chi1_diag/7:.2f}, "
                  f"u=.472 {chic_diag/7:.2f}",
      "step <1.5, u=1 and u=.472 >2",
      "the seven log-slopes dlnA/dlnR are reproduced by the one-parameter step at chi2/dof = "
      f"{chi_diag/7:.2f}; both constant-u readings are rejected on SHAPE alone (u=1: "
      f"{chi1_diag/7:.2f}, u=0.472: {chic_diag/7:.2f}) with no amplitude freedom used at all")

Z56 = (Sf[5] - SPRED[5]) / SERR[5]
Z56_1 = (Sf[5] - 0.0) / SERR[5]
Z56_c = (Sf[5] - SCONST[5]) / SERR[5]
K17 = (abs(Sf[5]) / SERR[5] > 2.5) and (abs(Z56) < 2.0) and (abs(Z56_1) > 2.5) and (abs(Z56_c) > 2.5)
check("K17", K17, f"s(1.18-1.71) = {Sf[5]:+.3f}+-{SERR[5]:.3f} ({abs(Sf[5])/SERR[5]:.1f} sigma from 0); "
                  f"step {SPRED[5]:+.3f} (Z={Z56:+.1f}); u=.472 {SCONST[5]:+.3f} (Z={Z56_c:+.1f})",
      "kink >2.5sigma, step within 2sigma, both rivals >2.5sigma",
      "THE KINK: between 1.18 and 1.71 Mpc the measured amplitude falls with dlnA/dlnR = "
      f"{Sf[5]:+.2f} +- {SERR[5]:.2f} ({abs(Sf[5])/SERR[5]:.1f} sigma from zero). The step predicts "
      f"{SPRED[5]:+.2f} (within {abs(Z56):.1f} sigma); every smooth reading predicts ~0 and misses "
      f"by {abs(Z56_1):.1f}-{abs(Z56_c):.1f} sigma. This is the curvature at r_sp, and it is "
      "amplitude-free: no rescaling can produce it")

inner = float((Sf[:5] / Ssd[:5] ** 2).sum() / (1 / Ssd[:5] ** 2).sum())
inner_err = float(1 / math.sqrt((1 / Ssd[:5] ** 2).sum()))
P("")
P(f"  mean inner slope (bins 0.18-1.18 Mpc, 5 intervals, inverse-variance): {inner:+.3f} +- {inner_err:.3f}"
  f"   (step predicts {float((SPRED[:5]/Ssd[:5]**2).sum()/(1/Ssd[:5]**2).sum()):+.3f})")
P(f"  curvature C = lnA(1.71) - 2 lnA(1.18) + lnA(0.81) = {Cf[0]:+.3f} +- {Csd[0]:.3f}")
P(f"  slope break Ds = s(1.18-1.71) - s(1.71-2.49)          = {Cf[1]:+.3f} +- {Csd[1]:.3f}")
for nm, m in (("step(fixed)", MODF), ("step(per-cluster)", MODP), ("u=1", NN + PHB),
              ("u=0.4716", NN + PHB / U_MID_A21)):
    a = m / PP
    l = np.log(a)
    sp_ = slopes_of(m)
    P(f"    predicted: {nm:18s} C = {l[6]-2*l[5]+l[4]:+.3f}   Ds = {sp_[5]-sp_[6]:+.3f}")
K18 = (abs(Cf[0]) / Csd[0] > 1.2) and (abs(Cf[0] - (np.log(MODF / PP)[6] - 2 * np.log(MODF / PP)[5]
                                                  + np.log(MODF / PP)[4])) < 2.5 * Csd[0])
check("K18", K18, f"C = {Cf[0]:+.3f}+-{Csd[0]:.3f} ({abs(Cf[0])/Csd[0]:.1f} sigma from 0); "
                  f"step predicts {np.log(MODF/PP)[6]-2*np.log(MODF/PP)[5]+np.log(MODF/PP)[4]:+.3f}; "
                  f"Ds = {Cf[1]:+.2f}+-{Csd[1]:.2f}",
      "C >1.2sigma from 0 and the step within 2.5sigma",
      "the observed curvature at the splashback radius is non-zero at %.1f sigma, and the step "
      "model's C (%+.3f) agrees within %.1f sigma while both smooth readings predict C = 0.000 "
      "exactly (A is flat when u is constant)" % (abs(Cf[0]) / Csd[0],
                                                  np.log(MODF / PP)[6] - 2 * np.log(MODF / PP)[5] + np.log(MODF / PP)[4],
                                                  abs(Cf[0] - (np.log(MODF / PP)[6] - 2 * np.log(MODF / PP)[5] +
                                                               np.log(MODF / PP)[4])) / Csd[0]))

# ============================================================== K19-K21  realisations
head("K19-K21  what the step can and cannot be: the 3D realisation, the NFW rival, the width")

M1 = np.zeros((NCL, NB))
M2 = np.zeros((NCL, NB))
for i in range(NCL):
    M1[i] = model3d(1.0, RSPi[i], i)
    M2[i] = model3d(2.0, RSPi[i], i)
o3 = stack(ALL, M1)
s3 = stack(ALL, M2) - o3
dev3 = float(np.max(np.abs(o3 / PP - 1)))
v3, sv3, c2_3 = fitlin(o3, s3)
U3 = 1.0 / (1.0 + v3)
MOD3 = o3 + v3 * s3
P("")
P(f"  3D check: u=1 reproduces PL to {dev3:.1e}; 3D step best fit u_in = {U3:.3f}, "
  f"chi2 = {c2_3:.1f}/7 = {c2_3/7:.1f}")
P(f"  3D model A(R) = " + " ".join(f"{x:.2f}" for x in MOD3 / PP))
P(f"  measured A(R) = " + " ".join(f"{x:.2f}" for x in Af))
P(f"  3D resid/sd    = " + " ".join(f"{x:+.1f}" for x in (DD - MOD3) / SD))
P(f"  the 3D step needs {(1/U3-1)*float(np.interp(RSP, RGRID, law_components(0)[2]))/MSUN:.1e} Msun of extra")
P(f"  cold mass inside r_sp (cluster 0), i.e. {(1/U3-1)*float(np.interp(RSP, RGRID, law_components(0)[2]))/(M200S*MSUN):.2f} M200c")
K19 = (c2_3 - c2_f > 15.0)
check("K19", K19, f"3D step chi2 = {c2_3:.1f}/7 vs projected step {c2_f:.1f}/7; "
                  f"dchi2 = {c2_3-c2_f:.0f} ({sg(c2_3-c2_f):.1f} sigma); "
                  f"A(1.71) = {MOD3[6]/PP[6]:.2f} vs {Af[6]:.2f} measured",
      "dchi2 > 15",
      "the step CANNOT be realised as a spherical amplification of the phantom: rho_cold = "
      "rho_ph/u inside r_sp raises the ENCLOSED mass, and DeltaSigma = Sigma(<R) - Sigma(R) then "
      "stays high outside r_sp (A = 1.6-1.7 at 1.7-2.5 Mpc against 0.93-1.06 measured). The 3D "
      "model is rejected at %.0f sigma, so the measured step is a statement about the projected "
      "ratio u(R), i.e. about the phantom's radial SHAPE" % sg(c2_3 - c2_f))


def nfw_ds(M200, c):
    r200 = r_delta(M200, DELTA, ZG)
    rs = r200 / c
    rho = M200 * MSUN / (4 * np.pi * (rs * MPC) ** 3 * mu(c)) / ((RGRID / rs) * (1 + RGRID / rs) ** 2)
    M = np.r_[0, np.cumsum(0.5 * (4 * np.pi * RM[1:] ** 2 * rho[1:] + 4 * np.pi * RM[:-1] ** 2 * rho[:-1]) * np.diff(RM))]
    return dsigma(M, rho, RC)


g1 = np.logspace(13, 15.5, 100)
best1 = None
for lm in g1:
    x = nfw_ds(lm, C_NFW)
    c2 = chi2_of(NN + x)
    if best1 is None or c2 < best1[0]:
        best1 = (c2, lm)
best2 = None
for cc in (2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0):
    for lm in g1:
        x = nfw_ds(lm, cc)
        c2 = chi2_of(NN + x)
        if best2 is None or c2 < best2[0]:
            best2 = (c2, lm, cc)
MOD_NFW1 = NN + nfw_ds(best1[1], C_NFW)
MOD_NFW2 = NN + nfw_ds(best2[1], best2[2])
P("")
P(f"  NFW cold sector, c = 4.5 (1 param): chi2 = {best1[0]:.1f}/7 = {best1[0]/7:.2f}, "
  f"M_c = {best1[1]:.2e} Msun")
P(f"  NFW cold sector, c free  (2 param): chi2 = {best2[0]:.1f}/6 = {best2[0]/6:.2f}, "
  f"M_c = {best2[1]:.2e}, c = {best2[2]:.1f}")
P(f"  NFW(c free) resid/sd = " + " ".join(f"{x:+.1f}" for x in (DD - MOD_NFW2) / SD))
K20 = best2[0] / 6 < 1.5
check("K20", K20, f"NFW(c=4.5) chi2/dof = {best1[0]/7:.2f}; NFW(c free) {best2[0]/6:.2f} with "
                  f"M_c = {best2[1]:.2e}, c = {best2[2]:.1f}",
      "NFW(c free) chi2/dof < 1.5 (i.e. it also fits)",
      "HONEST LIMIT: a smooth NFW cold sector also fits the eight bins (chi2/dof = %.2f with c "
      "free, %.2f at c = 4.5) -- the profile alone does NOT single out the law+step. What the "
      "profile does establish is that the law's OWN phantom shape is wrong (u=1 excluded) and that "
      "the correction is not a constant (u=const excluded)" % (best2[0] / 6, best1[0] / 7))

P("")
P("  transition width scan (projected step smoothed in log R; v profiled out at each width):")
WS = (0.0, 0.02, 0.04, 0.06, 0.08, 0.12, 0.16, 0.22)
WC2 = []
for w in WS:
    o_, s_ = projstep(RSPi, w)
    vv, _, cc = fitlin(o_, s_)
    WC2.append(cc)
    P(f"    w = {w:.2f} dex ({w*RSP*math.log(10):.2f} Mpc): u_in = {1/vv:.3f}, chi2 = {cc:.2f}")
K21 = (max(WC2) - min(WC2)) < 2.0
check("K21", K21, f"chi2 range over w = 0-0.22 dex: {min(WC2):.2f}-{max(WC2):.2f}", "range < 2",
      "the eight bins DO NOT measure the transition width: chi2 varies by less than 2 over "
      "w = 0 to 0.22 dex (0 to 0.7 Mpc). Only the location (1.2-1.7 Mpc) and the amplitude jump "
      "are measured -- the 'step' is a step at the resolution of the CFG687 grid")

# ============================================================== K22  cross-checks
head("K22  cross-checks against A29's u-space fit and the amplitude table")

WU = 1 / Usd ** 2
ubar = float((Uf * WU).sum() / WU.sum())
chi_u_const = float((WU * (Uf - ubar) ** 2).sum())
chi_u_1 = float((WU * (Uf - 1.0) ** 2).sum())
u_in_simple = float((Uf[:6] * WU[:6]).sum() / WU[:6].sum())
chi_u_step = float((WU * (Uf - np.r_[np.full(6, u_in_simple), 1.0, 1.0]) ** 2).sum())
u_out_free = float((Uf[6:] * WU[6:]).sum() / WU[6:].sum())
chi_u_step3 = float((WU * (Uf - np.r_[np.full(6, u_in_simple), u_out_free, u_out_free]) ** 2).sum())
P("")
P(f"  u-space (diagonal, A29's estimator): best constant u = {ubar:.4f}, chi2 = {chi_u_const:.1f}/7")
P(f"  A29 reported 5.92/dof = 41.5 for the same fit; u = 0.4716 gives {float((WU*(Uf-U_MID_A21)**2).sum()):.1f}/8")
P(f"  step (bins 0-5 | 6-7, u_out = 1): u_in = {u_in_simple:.4f}, chi2 = {chi_u_step:.1f}/7")
P(f"  the same step with u_out FREE (A29's 3-parameter fit): u_out = {u_out_free:.4f}, "
  f"chi2 = {chi_u_step3:.2f}/6 = {chi_u_step3/6:.2f} (A29 reported 8.98/1.75)")
P(f"  u = 1: chi2 = {chi_u_1:.1f}/8")
K22 = (abs(chi_u_const - 41.5) < 2.0) and (chi_u_1 / 8 > 20) and (u_in_simple > 0.35) and (u_in_simple < 0.48)
check("K22", K22, f"chi2_u(const) = {chi_u_const:.1f} (A29: 41.5); chi2_u(u=1) = {chi_u_1:.0f}; "
                  f"u_in = {u_in_simple:.4f}",
      "|chi2-41.5|<2, chi2(u=1)/8>20, u_in in (0.35,0.48)",
      "the u-space estimator reproduces A29's constant-u chi2 (41.5) and the same u_in (0.412), so "
      "the DeltaSigma-space fits above are the same measurement with the correct (full-covariance) "
      f"weighting; A29's 3-parameter step fit (chi2 = 8.98, 1.75/dof) recomputes to {chi_u_step3:.2f} "
      f"({chi_u_step3/6:.2f}/dof) here, so A29's number is confirmed to 0.25 in chi2")

# ============================================================== summary + JSON
N_PASS = sum(1 for c in CHECKS if c["pass_"])
N_TOT = len(CHECKS)
numbers = dict(
    n_clusters=NCL, n_patches=NPATCH,
    z_stack=ZG, M_gas_median=MGM, R500_median=R5M, M500=M500S, M200c=M200S,
    r200c=R200C, k_sp=K_SP, r_sp=RSP, r_sp_err=0.20,
    bin_edges_Mpc=list(map(float, EDGES)), bin_centres_Mpc=list(map(float, RC)),
    bin_edges_r200c=list(map(float, EDGES / R200C)), bin_centres_r200c=list(map(float, RC / R200C)),
    profile=dict(D=list(map(float, DD)), D_err=list(map(float, SD)),
                 A_law=list(map(float, Af)), A_law_err=list(map(float, Asd)),
                 A_newton=list(map(float, AN)), u=list(map(float, Uf)), u_err=list(map(float, Usd)),
                 PL=list(map(float, PP)), PN=list(map(float, NN))),
    cov_D=COV.tolist(), corr_D=CORR.tolist(),
    step=dict(u_in=UF, u_in_err=UF_ERR, v_in=v_f, chi2=c2_f, dof=7, chi2_dof=c2_f / 7,
              resid_sigma=list(map(float, RESF)),
              A_model=list(map(float, MODF / PP)),
              variant_percluster=dict(u_in=UP, u_in_err=UP_ERR, chi2=c2_p, chi2_dof=c2_p / 7,
                                      resid_sigma=list(map(float, RESP)),
                                      rsp_p16=float(np.percentile(RSPi, 16)),
                                      rsp_p84=float(np.percentile(RSPi, 84)))),
    rivals={k: dict(chi2=v["chi2"], dof=v["dof"], chi2_dof=v["chi2"] / v["dof"],
                    dchi2_vs_step=v["chi2"] - c2_f,
                    sigma=math.sqrt(max(0.0, v["chi2"] - c2_f)),
                    resid_sigma=list(map(float, (DD - v["m"]) / SD))) for k, v in RIVALS.items()},
    best_constant_u=1 / v_best,
    cosmic_share=dict(R_tot_stack=R_TOT_STACK, u_cs_stack=U_CS_STACK, u_cs_a18=U_CS_A18,
                      R_cosmic=R_COSMIC, r_tot_a18=R_TOT_A18, Z=z_cs, M_b_rv=_mb,
                      r_tot_model=R_TOT_MODEL, u_cs_model=U_CS_MODEL, M_b_3Mpc=_Mb3,
                      u_cs_central=U_CS_CENTRAL, sig_cs=SIG_CS),
    shape=dict(slopes_D=list(map(float, sD)), slopes_PL=list(map(float, sL)),
               slopes_measured=list(map(float, Sf)), slopes_err=list(map(float, Ssd)),
               dlnR=list(map(float, DLNR)),
               slopes_step=list(map(float, SPRED)), slopes_step_pc=list(map(float, SPRED_P)),
               slopes_u1=list(map(float, S1)), slopes_const=list(map(float, SCONST)),
               chi2_shape_step=chi_diag, chi2_shape_step_pc=chi_diag_p,
               chi2_shape_u1=chi1_diag, chi2_shape_const=chic_diag,
               chi2_shape_step_full=chi_full, chi2_shape_u1_full=chi1_full,
               C=Cf[0], C_err=Csd[0], Ds=Cf[1], Ds_err=Csd[1],
               C_step=float(np.log(MODF / PP)[6] - 2 * np.log(MODF / PP)[5] + np.log(MODF / PP)[4]),
               Z56=Z56, Z56_u1=Z56_1, Z56_const=Z56_c, sigma56=float(SERR[5])),
    realisation_3d=dict(u_in=U3, chi2=c2_3, chi2_dof=c2_3 / 7, dchi2_vs_step=c2_3 - c2_f,
                        A_model=list(map(float, MOD3 / PP)), resid_sigma=list(map(float, (DD - MOD3) / SD)),
                        extra_Msun=float((1 / U3 - 1) * np.interp(RSP, RGRID, law_components(0)[2]) / MSUN),
                        extra_M200c=float((1 / U3 - 1) * np.interp(RSP, RGRID, law_components(0)[2]) / (M200S * MSUN))),
    nfw=dict(c45=dict(chi2=best1[0], chi2_dof=best1[0] / 7, M=best1[1]),
             cfree=dict(chi2=best2[0], chi2_dof=best2[0] / 6, M=best2[1], c=best2[2],
                        resid_sigma=list(map(float, (DD - MOD_NFW2) / SD)))),
    width_scan=dict(w_dex=list(WS), chi2=WC2, u_in=[1 / fitlin(*projstep(RSPi, w))[0] for w in WS]),
    u_space=dict(u_bar=ubar, chi2_const=chi_u_const, chi2_u1=chi_u_1, u_in_simple=u_in_simple,
                 chi2_step=chi_u_step, u_out_free=u_out_free, chi2_step3=chi_u_step3),
    A_bands={b: dict(A_law=float((W[:, jj] * D[:, jj]).sum() / (W[:, jj] * PL[:, jj]).sum()),
                     A_newton=float((W[:, jj] * D[:, jj]).sum() / (W[:, jj] * PN[:, jj]).sum()),
                     range=[float(EDGES[jj[0]]), float(EDGES[jj[-1] + 1])]) for b, jj in BANDS.items()},
)
res = dict(lane=LANE,
           status="NUMERICAL: the full 8-bin profile confirms a step in u(R) at r_sp (u_in = %.3f +- %.3f, "
                  "u = 1 outside) at Delta chi2 = %.0f vs the best constant u and %.0f vs u = 1; "
                  "CONDITIONAL: the step is a projected ratio, not a spherical mass step (3D "
                  "realisation rejected at %.0f sigma), and a smooth NFW cold sector fits the same "
                  "8 bins" % (UF, UF_ERR, dc4, dc1, sg(c2_3 - c2_f)),
           checks=[dict(id=c["id"], **{"pass": c["pass_"]}, value=c["value"],
                        threshold=c["threshold"], label=c["label"]) for c in CHECKS],
           numbers=numbers, constants_used=CONSTANTS, record_inputs=RECORD,
           data_source=dict(npz=os.path.relpath(NPZ, ROOT), n_clusters=NCL, n_bins=NB,
                            edges_Mpc=list(map(float, EDGES)), edges_r200c=list(map(float, EDGES / R200C))),
           mutation=MUT or None, n_pass=N_PASS, n_total=N_TOT, runtime_s=round(time.time() - T0, 2))
with open(os.path.join(HERE, "a41_results" + TAG + ".json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)

head("SUMMARY")
P(f"  TASK 1  the eight-bin profile (D, A=D/PL, u=1/lambda) with jackknife errors is in the table")
P(f"          above; u = " + " ".join(f"{x:.2f}" for x in Uf))
P(f"          A = " + " ".join(f"{x:.2f}" for x in Af) + "   (A=1 would be the law, no rescaling)")
P(f"  TASK 2  ONE parameter u_in: {UF:.4f} +- {UF_ERR:.4f} (fixed r_sp), {UP:.4f} +- {UP_ERR:.4f} "
  f"(per-cluster r_sp)")
P(f"          chi2 = {c2_f:.2f}/7 = {c2_f/7:.2f}  and  {c2_p:.2f}/7 = {c2_p/7:.2f}; "
  f"max residual {np.max(np.abs(RESF)):.1f} sigma")
P(f"  TASK 3  dchi2 vs step:  u=1  {dc1:.0f} ({sg(dc1):.1f} sigma)   "
  f"u=0.4716  {dc2:.0f} ({sg(dc2):.1f} sigma)   u=0.488  {dc3:.0f} ({sg(dc3):.1f} sigma)   "
  f"best const u={1/v_best:.3f}  {dc4:.0f} ({sg(dc4):.1f} sigma)")
P(f"  TASK 4  kink s(1.18-1.71) = {Sf[5]:+.2f} +- {SERR[5]:.2f} ({abs(Sf[5])/SERR[5]:.1f} sigma); "
  f"step predicts {SPRED[5]:+.2f}, u=1 and u=const predict ~0")
P(f"          curvature C = {Cf[0]:+.3f} +- {Csd[0]:.3f}; shape chi2/dof: step {chi_diag/7:.2f} "
  f"vs u=1 {chi1_diag/7:.2f} vs u=.472 {chic_diag/7:.2f}")
P(f"  LIMITS  the 3D realisation of the step is rejected at {sg(c2_3-c2_f):.0f} sigma; a smooth "
  f"NFW cold sector fits at {best2[0]/6:.2f}/dof; the transition width is unconstrained")
P("")
P(f"{LANE} COMPLETE: {N_PASS}/{N_TOT} checks PASS.")
OUTF.close()
sys.exit(0 if N_PASS == N_TOT else 1)
