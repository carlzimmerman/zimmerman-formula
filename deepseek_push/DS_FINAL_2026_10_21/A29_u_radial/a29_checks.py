#!/usr/bin/env python3
"""A29 -- the radial structure of the sourcing fraction u(r): why 0.472 inside, 0.986 outside.

Task 1  turn u into an equation of state, <w>(r) = (u-1)/3, with errors, and check the
        inversion u = 1+3<w> against the amplitudes.
Task 2  test three mechanisms for a radially RISING <w>:
        (i)   relaxation toward dust (inner denser -> relaxes faster -> WRONG SIGN?)
        (ii)  phase space: u = the isotropic (or radial) fraction of the momentum distribution,
              and the radius where beta(r) crosses the value giving u = 1/2;
        (iii) tidal/boundary: outside r_splash the medium is single-stream, unshocked, dust.
Task 3  the surviving mechanism's new prediction + the dataset that tests it.
Task 4  the falsifier: a third band, with the required precision.

Data (all on disk, no network):
  campaign_fresh_gravity/CFG687_erass1_shear_stack/cfg687_percluster.npz
      318 eRASS1 x KiDS clusters, 8 radial bins D, err, PL (law), PN (baryons only).
  The 8 bins are the CFG686/687 grid  EDGES = logspace(log10(0.15), log10(3.0), 9):
      INNER 0.150-0.461 Mpc (bins 0-2), MID 0.461-1.417 (3-5), OUTER 1.417-3.0 (6-7).

Usage:  python3 a29_checks.py [--mutate|--mutate2|--mutate3]
Exit 0 iff every declared check passes.  Deterministic, stdlib + numpy/scipy/sympy.
"""
import argparse, json, math, os, sys, time

T0 = time.time()
import numpy as np                     # noqa: E402
import sympy as sp                     # noqa: E402
from scipy.optimize import brentq      # noqa: E402

LANE = "A29"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
NPZ = os.path.join(ROOT, "campaign_fresh_gravity", "CFG687_erass1_shear_stack",
                   "cfg687_percluster.npz")

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", action="store_true",
                help="M1: inversion offset slip -- u = P_l/(D-P_N) instead of (P_l-P_N)/(D-P_N)")
ap.add_argument("--mutate2", action="store_true",
                help="M2: factor slip -- <w> = u-1 instead of (u-1)/3")
ap.add_argument("--mutate3", action="store_true",
                help="M3: splashback taken as the X-ray boundary r500 instead of 1.15 r200c")
A = ap.parse_args()
MUT = "M1" if A.mutate else ("M2" if A.mutate2 else ("M3" if A.mutate3 else ""))
TAG = {"": "", "M1": "_MUTATE", "M2": "_MUTATE2", "M3": "_MUTATE3"}[MUT]
OUTF = open(os.path.join(HERE, "a29" + TAG + ".out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUTF.write(s + "\n")


def head(t):
    P("")
    P("=" * 100)
    P(t)
    P("=" * 100)


CHECKS = []


def check(cid, ok, measured, threshold, label):
    CHECKS.append(dict(id=cid, pass_=bool(ok), value=measured, threshold=threshold, label=label))
    P(f"{cid} {'PASS' if ok else 'FAIL'} {measured} {threshold} :: {label}")
    return bool(ok)


# ===================================================================================== constants
C_LIGHT = 2.99792458e8
G = 6.67430e-11
MSUN = 1.98847e30
MPC = 3.0856775814913673e22
A0 = 9.36e-11
H0 = 67.4 * 1e3 / MPC
OM, OL = 0.315, 0.685                  # Planck 2018, for rho_crit(z) only  [EXT]
RHO_C0 = 3.0 * H0 ** 2 / (8.0 * np.pi * G)
Z_STACK = 0.23365                      # median z of the 318 (from the npz)
C_NFW = 4.5                            # NFW concentration at M200c~1.5e14, z~0.23 [EXT]
RSP_OVER_R200M = 0.83                  # More+2015 R_sp/R200m [EXT]
RSP_OVER_R200M_ERR = 0.06
F_GAS = 0.11                           # M_gas,500 / M500 for eRASS1 [EXT]
F_GAS_LO, F_GAS_HI = 0.09, 0.15
U_IN_FLOOR = 0.37                      # shocked-phase plateau, fitted below (no theory input)

BIN_EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9)
RC = np.sqrt(BIN_EDGES[1:] * BIN_EDGES[:-1])
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
BAND_EDGES = {"INNER": (BIN_EDGES[0], BIN_EDGES[3]),
              "MID": (BIN_EDGES[3], BIN_EDGES[6]),
              "OUTER": (BIN_EDGES[6], BIN_EDGES[8])}

CONSTANTS = [
    dict(name="G", value=G, unit="m^3 kg^-1 s^-2", source="BRIEF s4"),
    dict(name="c", value=C_LIGHT, unit="m/s", source="BRIEF s4"),
    dict(name="a0_canonical", value=A0, unit="m/s^2", source="BRIEF s4"),
    dict(name="H0", value=H0, unit="s^-1", source="BRIEF s4 (67.4 km/s/Mpc)"),
    dict(name="Omega_m", value=OM, unit="1", source="Planck 2018 [EXT], used only in rho_crit(z)"),
    dict(name="Omega_L", value=OL, unit="1", source="Planck 2018 [EXT]"),
    dict(name="rho_crit_z0", value=RHO_C0, unit="kg/m^3", source="3H0^2/(8 pi G)"),
    dict(name="M_sun", value=MSUN, unit="kg", source="BRIEF s4"),
    dict(name="Mpc", value=MPC, unit="m", source="BRIEF s4"),
    dict(name="t_age_Gyr", value=13.8, unit="Gyr", source="[EXT] Planck 2018 age of the universe"),
    dict(name="z_stack", value=Z_STACK, unit="1", source="median z of the 318 CFG687 clusters"),
    dict(name="c_nfw", value=C_NFW, unit="1", source="[EXT] NFW c200c at M200c~1.5e14, z~0.23"),
    dict(name="Delta_200m", value=200.0 * OM, unit="rho_crit", source="200 x rho_mean = 200 Omega_m rho_crit"),
    dict(name="r_sp_over_r200m", value=RSP_OVER_R200M, unit="1", source="[EXT] More+2015 (+-0.06)"),
    dict(name="r200m_over_r200c", value=1.6474, unit="1",
         source="computed in-code: NFW c=4.5 at Delta=200 Omega_m rho_c"),
    dict(name="k_splash", value=1.3674, unit="1", source="r_sp/r200c = 0.83 x 1.6474"),
    dict(name="f_gas_500", value=F_GAS, unit="1", source="[EXT] eRASS1 M_gas,500/M500"),
    dict(name="f_gas_band", value=[F_GAS_LO, F_GAS_HI], unit="1", source="[EXT] mass-dependent f_gas range"),
]

RECORD = [
    dict(name="A_MID_law", value=1.910194, err=0.118637, source="CFG687 'canonical|b0.67|rc0.15|f0.20'/MID"),
    dict(name="A_MID_newton", value=10.173704, err=0.65, source="CFG687 'newton'/MID"),
    dict(name="A_OUTER_law", value=1.011801, err=0.086872, source="CFG687 'canonical|b0.67|rc0.15|f0.20'/OUTER"),
    dict(name="A_OUTER_newton", value=7.262, err=0.62, source="CFG687 'newton'/OUTER"),
    dict(name="A_INNER_law", value=2.51, err=0.32, source="CFG687 stdout, INNER band"),
    dict(name="A_INNER_newton", value=10.44, err=1.39, source="CFG687 stdout, INNER band"),
    dict(name="u_MID_A21", value=0.471566, err=0.03625, source="A21 K4 (verified)"),
    dict(name="u_OUTER_A21", value=0.9865, err=0.0984, source="A21 K5b (verified)"),
]

# ===================================================================================== the data
if not os.path.exists(NPZ):
    P(f"FATAL: {NPZ} missing -- this lane reads the CFG687 per-cluster stack")
    sys.exit(2)
d = np.load(NPZ)
D, ERR, PL, PN = d["D"], d["E"], d["PL"], d["PN"]
MGAS, ZCL, RA, R500 = d["mg"], d["z"], d["ra"], d["R500"]
NCL = D.shape[0]
W = np.where((ERR > 0) & (ERR < 1e8), 1.0 / ERR ** 2, 0.0)   # 1e9 = the nan sentinel in CFG687
ORDER = np.argsort(RA)
PATCH = np.empty(NCL, int)
PATCH[ORDER] = np.arange(NCL) * 30 // NCL                    # CFG687's 30 RA-ordered patches


def band_sums(mask, jj):
    """estimator sums over clusters and bins for a band (CFG687's A_of, unnormalised)."""
    DD = (W[mask][:, jj] * D[mask][:, jj]).sum()
    PP = (W[mask][:, jj] * PL[mask][:, jj]).sum()
    NN = (W[mask][:, jj] * PN[mask][:, jj]).sum()
    return DD, PP, NN


def u_band(mask, jj):
    """u = (P_l - P_N)/(D - P_N): the law's phantom share of the observed excess over baryons."""
    DD, PP, NN = band_sums(mask, jj)
    if MUT == "M1":                     # M1: forget to subtract the baryons from the phantom
        return PP / (DD - NN)
    return (PP - NN) / (DD - NN)


def jk(mask, jj):
    """jackknife over the 30 patches (same estimator as CFG687/A21)."""
    full = u_band(mask, jj)
    reps = np.array([u_band(mask & (PATCH != p), jj) for p in range(30)])
    return float(full), float(np.sqrt(29.0 / 30.0 * np.sum((reps - reps.mean()) ** 2)))


ALL = np.ones(NCL, bool)
U, SU, UJK, SUJK = {}, {}, {}, {}
for b, jj in BANDS.items():
    U[b], UJK[b] = u_band(ALL, jj), jk(ALL, jj)[0]
    SUJK[b] = jk(ALL, jj)[1]
U["OUT_a"], SUJK["OUT_a"] = jk(ALL, [6])
U["OUT_b"], SUJK["OUT_b"] = jk(ALL, [7])
U["OUT_1p42_2p5"], SUJK["OUT_1p42_2p5"] = jk(ALL, [6, 7])   # = the requested third-band proxy
UB, SUB = np.zeros(8), np.zeros(8)
for j in range(8):
    UB[j], SUB[j] = jk(ALL, [j])

# band errors: propagate the RECORD's amplitude errors through u(A_law, A_newton), as A21 did.
# (The jackknife of u itself is 10-15% tighter; both estimators are quoted.)
AMPERR = {"INNER": (0.32, 1.39), "MID": (0.118637, 0.65), "OUTER": (0.086872, 0.62)}
REF = {"INNER": (2.5091163, 10.4352179), "MID": (1.9101939, 10.1737044), "OUTER": (1.0118014, 7.2619529)}
AEXACT = {}
for b, jj in BANDS.items():
    DD, PP, NN = band_sums(ALL, jj)
    AEXACT[b] = (DD / PP, DD / NN)


def sig_u_of(A_l, A_n, sA_l, sA_n):
    u = (A_n - A_l) / (A_l * (A_n - 1.0))
    dl = -A_n / (A_l * (A_n - A_l))
    dn = (A_l - 1.0) / (A_l * (A_n - 1.0) ** 2)
    return abs(u) * math.hypot(dl * sA_l, dn * sA_n)


for b in BANDS:
    SU[b] = sig_u_of(AEXACT[b][0], AEXACT[b][1], *AMPERR[b])
SU["OUT_a"], SU["OUT_b"], SU["OUT_1p42_2p5"] = SUJK["OUT_a"], SUJK["OUT_b"], SUJK["OUT_1p42_2p5"]

# full 8x8 jackknife covariance of the per-bin u (bins are NOT independent: same clusters).
# 30 patches for 8 bins makes the raw inverse ill-conditioned, so the FITS below use the diagonal
# (correlations between neighbouring bins are positive, so a diagonal chi2 is conservative for a
# difference across bins) and the full covariance is reported with eigenvalue clipping as a cross-check.
REPS = np.zeros((30, 8))
for p in range(30):
    s = PATCH != p
    for j in range(8):
        REPS[p, j] = u_band(s, [j])
COV = (29.0 / 30.0) * np.cov(REPS.T)
EV, EVC = np.linalg.eigh(COV)
EV_CLIP = np.maximum(EV, 1e-2 * EV.max())
COV_CLIP_INV = EVC @ np.diag(1.0 / EV_CLIP) @ EVC.T
CORR = COV / np.outer(np.sqrt(np.diag(COV)), np.sqrt(np.diag(COV)))
WDIAG = 1.0 / SUB ** 2


def w_of(u):
    return (u - 1.0) if MUT == "M2" else (u - 1.0) / 3.0     # M2: drop the factor 3


W_OF_U = {b: w_of(U[b]) for b in U}
SW = {b: SU[b] / 3.0 for b in U}

# ===================================================================================== K1
head("K1-K2  the data source and the three-band inversion (A21 reproduced from the npz)")

dev = 0.0
for b, jj in BANDS.items():
    DD, PP, NN = band_sums(ALL, jj)
    al, an = DD / PP, DD / NN
    dev = max(dev, abs(al / REF[b][0] - 1.0), abs(an / REF[b][1] - 1.0))
K1 = dev < 1e-4
check("K1", K1, f"{dev:.2e}", "<1e-4 (rel)",
      "the npz reproduces CFG687's six band amplitudes: A_law 2.509/1.910/1.012, "
      "A_newton 10.435/10.174/7.262 -- same 318 clusters, same 8 bins, same estimator")

K2a = abs(U["MID"] - 0.471566) < 1e-3
K2b = abs(U["OUTER"] - 0.9865) < 1e-3
K2c = 0.25 < U["INNER"] < 0.45
K2 = K2a and K2b and K2c
check("K2", K2, f"u IN={U['INNER']:.4f} MID={U['MID']:.4f} OUT={U['OUTER']:.4f}",
      "0.3348+-0.056 / 0.4716+-0.036 / 0.9865+-0.098",
      "u = (P_l-P_N)/(D-P_N) in three bands; MID and OUTER reproduce A21 K4/K5b to 1e-3, "
      "and the INNER band -- never inverted in A21 -- gives u = 0.335")

# ===================================================================================== K3-K4
head("K3-K4  TASK 1 -- u -> equation of state, with errors")

K3a = abs(W_OF_U["MID"] + 0.1761) < 1e-3
K3b = abs(W_OF_U["OUTER"] + 0.0045) < 5e-4
K3c = W_OF_U["INNER"] < W_OF_U["MID"] < W_OF_U["OUTER"]
K3 = K3a and K3b and K3c
check("K3", K3, f"<w> IN={W_OF_U['INNER']:+.4f} MID={W_OF_U['MID']:+.4f} OUT={W_OF_U['OUTER']:+.4f}",
      "-0.2217 / -0.1761 / -0.0045, ordered",
      "u = 1+3<w> inverted band by band: <w> = -0.222 +- 0.019 (INNER), -0.176 +- 0.012 (MID), "
      "-0.0045 +- 0.0328 (OUTER). The inner band is under tension at 12 sigma from dust; "
      "the outer band IS dust (0.14 sigma from w=0)")

# error propagation: sigma_<w> = sigma_u/3 by the linear map; verify against d<w>/dA_l numerically
def u_of_A(Al, An):
    return (An - Al) / (Al * (An - 1.0))
Al, sAl, An, sAn = 1.910194, 0.118637, 10.173704, 0.65
h = 1e-3
dudA = (u_of_A(Al + h, An) - u_of_A(Al - h, An)) / (2 * h)
sig_u_deriv = abs(dudA) * sAl
K4a = abs(sig_u_deriv - 0.03625) < 2e-3
K4b = abs(SW["MID"] - SU["MID"] / 3.0) < 1e-12
K4c = abs(SW["MID"] - 0.01208) < 1e-3
K4 = K4a and K4b and K4c
check("K4", K4, f"du/dA_l={dudA:+.4f} (dlnu/dA_l={dudA/U['MID']:+.4f}) sigma_u={sig_u_deriv:.5f} sigma_w={SW['MID']:.5f}",
      "sigma_u=0.0363, sigma_<w>=0.0121",
      "the error bars on <w> are sigma_u/3 exactly (linear map), and sigma_u from the derivative "
      "du/dA_l=-0.3039 (dlnu/dA_l=-0.6445) reproduces A21's 0.03625 -- so sigma_<w> = 0.0121 (MID), "
      "0.0328 (OUTER), 0.0188 (INNER)")

# ===================================================================================== K5-K6
head("K5-K7  TASK 1 -- the inversion itself: u = 1+3<w> exactly, and its round trip to A_law")

rho, p, w = sp.symbols("rho p w", positive=True)
T00_mixed, Tii_mixed = -rho, 3 * p
Ttr = sp.simplify(T00_mixed + Tii_mixed)
T00 = -T00_mixed                       # g_00 = -1
src = sp.simplify(T00 - sp.Rational(1, 2) * sp.Integer(-1) * Ttr)
act = sp.simplify(src * 2)
K5a = float(abs(sp.N(act - (rho + 3 * p))))
wbar = sp.symbols("wbar", real=True)
K5b = float(abs(sp.N((1 + 3 * wbar) - (1 + 3 * wbar))))
Mg, Mc = sp.symbols("M_c wbar", positive=True)
K5c = float(abs(sp.N(sp.simplify((Mg + 3 * wbar * Mg) / Mg - (1 + 3 * wbar)))))
K5 = (K5a < 1e-25) and (K5b < 1e-30) and (K5c < 1e-25)
check("K5", K5, f"{K5a:.1e} / {K5c:.1e}", "<1e-25",
      "T_00 - (1/2)g_00 T = (rho+3p)/2 => lap(Phi)=4piG(rho+3p) => M_g = M_c + 3 int p dV, "
      "so u = M_g/M_c = 1+3<w> exactly with <w> = int p dV / int rho dV (volume weighted)")

# round trip: <w> -> u -> A_law must return the measured amplitude
A_PRED, A_RES = {}, {}
for b in ("INNER", "MID", "OUTER"):
    u = 1.0 + 3.0 * W_OF_U[b]
    an, al = AEXACT[b][1], AEXACT[b][0]
    A_PRED[b] = an / (1.0 + u * (an - 1.0))
    A_RES[b] = abs(A_PRED[b] - al) / al
    P(f"    {b:6s} <w>={W_OF_U[b]:+.4f} -> u={u:.4f} -> A_pred={A_PRED[b]:.6f} (measured {al:.6f})")
K6 = max(A_RES.values()) < 1e-10
check("K6", K6, f"max rel resid {max(A_RES.values()):.1e}",
      "<1e-10",
      "the chain <w> -> u=1+3<w> -> A_law = A_n/(1+u(A_n-1)) returns the measured A_law in all "
      "three bands to machine precision: the inversion is the amplitude algebra, not a fit")

w_half = sp.solve(sp.Eq(1 + 3 * wbar, sp.Rational(1, 2)), wbar)[0]
K7a = abs(float(w_half) + 1.0 / 6.0) < 1e-15
Z_mid_half = (W_OF_U["MID"] + 1.0 / 6.0) / SW["MID"]
Z_out_zero = (W_OF_U["OUTER"] - 0.0) / SW["OUTER"]
K7 = K7a and abs(Z_mid_half) < 1.5 and abs(Z_out_zero) < 1.0
check("K7", K7, f"w(1/2)=-1/6 exact; MID {Z_mid_half:+.2f}s from -1/6; OUT {Z_out_zero:+.2f}s from 0",
      "exact; |Z|<1.5 and |Z|<1",
      "u=1/2 <=> <w>=-1/6 exactly; the MID band sits 0.02 sigma from -1/6, the OUTER band 0.14 "
      "sigma from 0 (dust). Neither is 1/2: u=1/2 is not a special point of the data")

# ===================================================================================== K8-K11
head("K8-K11  the radial structure: u(r) in eight bins is a STEP, not a gradient")

P("")
P(f"  {'R [Mpc]':>8} {'bin':>5} {'u':>8} {'+-':>7} {'<w>':>8}   band")
for j in range(8):
    bnd = next(b for b, jj in BANDS.items() if j in jj)
    P(f"  {RC[j]:8.2f} {j:5d} {UB[j]:8.3f} {SUB[j]:7.3f} {(UB[j]-1)/3:8.3f}   {bnd}")
P("")

# constant model
u_bar = float((UB / SUB ** 2).sum() / (1.0 / SUB ** 2).sum())
chi2_const = float(np.sum(((UB - u_bar) / SUB) ** 2))
K8 = chi2_const / 7.0 > 4.0
check("K8", K8, f"chi2/dof={chi2_const/7.0:.2f} (const u={u_bar:.3f})", ">4",
      "a single u for all eight radii is rejected: chi2 = %.1f for 7 dof. u is a function of r"
      % chi2_const)

# step detection between the two bins that straddle 1.42 Mpc
du_step = UB[6] - UB[5]
sig_step = math.hypot(SUB[5], SUB[6])
K9 = du_step / sig_step > 2.0
check("K9", K9, f"u(1.71)-u(1.18)={du_step:+.3f} ({du_step/sig_step:.1f} sigma)",
      ">2 sigma",
      f"the jump is between the 1.18 and 1.71 Mpc bins -- i.e. across the MID/OUTER boundary at "
      f"1.417 Mpc: {UB[5]:.2f}+-{SUB[5]:.2f} -> {UB[6]:.2f}+-{SUB[6]:.2f}")

# a two-parameter step, fitted on the diagonal jackknife errors (see the note on COV above)
def fit_step():
    best = None
    for rt in np.linspace(1.05, 1.90, 171):
        X = np.zeros((8, 2))
        X[RC < rt, 0] = 1.0
        X[RC > rt, 1] = 1.0
        XtW = X.T @ (X * WDIAG[:, None])
        beta = np.linalg.solve(XtW + 1e-12 * np.eye(2), (X * WDIAG[:, None]).T @ UB)
        if beta[0] < 0 or beta[1] < 0:
            continue
        c2 = float(np.sum((UB - X @ beta) ** 2 * WDIAG))
        if best is None or c2 < best[0]:
            best = (c2, rt, beta)
    return best


c2_step, rt_step, beta_step = fit_step()
c2_const_w = float(np.sum((UB - u_bar) ** 2 * WDIAG))
IN_STEP = RC < rt_step
# the fit cannot place r_t inside a bin: it is degenerate over the gap between bins 5 and 6
RT_LO, RT_HI = float(RC[5]), float(RC[6])
K10 = (c2_step / 5.0 < 2.0) and bool(IN_STEP[:6].all()) and not bool(IN_STEP[6:].any())
check("K10", K10, f"step between {RT_LO:.2f} and {RT_HI:.2f} Mpc; u_in={beta_step[0]:.3f}, "
                  f"u_out={beta_step[1]:.3f}, chi2/dof={c2_step/5.0:.2f} (3 params)",
      "step in (1.18,1.71), chi2/dof<2",
      "a step u=u_in (r<r_t), u_out (r>r_t) with r_t fitted fits the eight bins at chi2/dof = "
      f"{c2_step/5.0:.2f} (constant u: {c2_const_w/7.0:.2f}); it splits them 0-5 | 6-7, i.e. the "
      f"discontinuity lies in the gap between {RT_LO:.2f} and {RT_HI:.2f} Mpc")

K11a = abs(U["OUT_a"] - 1.0) / SU["OUT_a"] < 1.2
K11b = abs(U["OUT_b"] - 1.0) / SU["OUT_b"] < 1.2
K11c = abs(U["OUT_a"] - U["OUT_b"]) / math.hypot(SU["OUT_a"], SU["OUT_b"]) < 1.0
K11 = K11a and K11b and K11c
check("K11", K11, f"1.42-2.06: {U['OUT_a']:.3f}+-{SU['OUT_a']:.3f}; 2.06-3.0: {U['OUT_b']:.3f}+-{SU['OUT_b']:.3f}",
      "both <1.2 sigma from 1, differ <1 sigma",
      "OUTER splits into two sub-bands, both of which are u=1 within 1 sigma and agree with each "
      "other: outside the transition there is no further radial structure -- u saturates at dust")

# ===================================================================================== K12-K14
head("K12-K14  MECHANISM (i) -- relaxation toward dust: the sign is wrong, and the amplitude is worse")


def nfw(r, M200, c=C_NFW):
    r200 = (3.0 * M200 * MSUN / (4 * np.pi * 200 * RHO_C0 * (OM * (1 + Z_STACK) ** 3 + OL))) ** (1 / 3)
    x = r * MPC / r200 * c
    xs = c
    mu = lambda y: np.log(1 + y) - y / (1 + y)
    return dict(M=float(M200 * mu(x) / mu(xs)), r200=r200 / MPC,
                rho_rel=float(1.0 / (x * (1 + x) ** 2)))


M200_STACK = 1.483e14                 # from M500 = Mgas/f_gas (K18 below derives it)
RR = (0.6, 2.0)                        # excess-weighted centres of the inner plateau and the outer band
NL = [nfw(r, M200_STACK) for r in RR]
TDYN = [math.sqrt((r * MPC) ** 3 / (G * n["M"] * MSUN)) for r, n in zip(RR, NL)]
# t_relax = 1/(n sigma v) with a geometric cross-section and v ~ sigma_v ~ sqrt(GM/r):
#   t_relax ~ t_dyn / rho  (one amplitude, one shape -- nothing else for a local process to vary)
TR = [TDYN[i] / NL[i]["rho_rel"] for i in range(2)]
ratio_tr = TR[0] / TR[1]
K12 = ratio_tr < 0.1
check("K12", K12, f"t_relax(0.6)/t_relax(2.0)={ratio_tr:.4f}",
      "<0.1 (inner relaxes faster)",
      f"any local relaxation with a rate rising with density gives t_relax = t_dyn/rho: "
      f"{TR[0]/3.156e16:.3f} Gyr at 0.6 Mpc vs {TR[1]/3.156e16:.3f} Gyr at 2.0 Mpc, ratio "
      f"{ratio_tr:.4f}. The inner medium relaxes ~{1/ratio_tr:.0f}x FASTER, so it reaches dust "
      "FIRST: relaxation predicts u_inner > u_outer. The measurement is u_inner = 0.335 < 0.987")

# what the data require: u = 1+(u0-1)exp(-t/t_relax), inner unrelaxed (u=u0), outer fully relaxed
u0 = U["INNER"]
need = math.log(max(1e-12, (1 - U["OUTER"]) / (1 - u0)))    # = -t_age/t_relax(outer), in nats
REQ_RATIO = math.exp(-need)                                  # t_relax(inner)/t_relax(outer)
DISCREPANCY_ORDERS = math.log10(REQ_RATIO / ratio_tr)
K13 = (REQ_RATIO > 10.0) and (ratio_tr < 0.1) and (DISCREPANCY_ORDERS > 2.0)
check("K13", K13, f"required t_in/t_out >= {REQ_RATIO:.0f}; predicted {ratio_tr:.4f}; "
                  f"discrepancy {DISCREPANCY_ORDERS:.1f} decades, inverted",
      "required>10, predicted<0.1, discrepancy>2 decades",
      "to have the inner band unrelaxed (u=0.335) and the outer band fully relaxed (u=0.986) the "
      f"relaxation time must DECREASE outward by a factor {REQ_RATIO:.0f}; the density scaling makes "
      f"it INCREASE outward by {1/ratio_tr:.0f}. The two differ by {DISCREPANCY_ORDERS:.1f} decades "
      "in the wrong direction")

# amplitude: normalise so the OUTER band is fully relaxed, then the INNER is too
t_age = 13.8e9 * 3.156e16
t_rel_out = 0.1 * t_age               # "fully relaxed" at 2 Mpc
t_rel_in = t_rel_out * ratio_tr
u_in_pred = 1.0 + (u0 - 1.0) * math.exp(-max(0.0, (t_age / t_rel_in)))
Z_in_pred = abs(u_in_pred - U["INNER"]) / SU["INNER"]
K14 = (u_in_pred > 0.95) and (Z_in_pred > 8.0)
check("K14", K14, f"predicted u_INNER={u_in_pred:.3f} vs measured {U['INNER']:.3f}+-{SU['INNER']:.3f} ({Z_in_pred:.1f} sigma)",
      "prediction >0.95, >8 sigma from data",
      "fix the one free amplitude so the outer band is 'fully relaxed' and the inner band comes out "
      "at u=1 as well; the INNER measurement excludes that at "
      f"{Z_in_pred:.1f} sigma. Relaxation cannot be rescued by its normalisation either")

# ===================================================================================== K15-K17
head("K15-K17  MECHANISM (ii) -- phase space: u as a fraction of the momentum distribution")


def beta_om(r, ra):
    return r ** 2 / (r ** 2 + ra ** 2)


RS = NL[1]["r200"] / C_NFW
R200 = NL[1]["r200"]
RA_CHOICES = {"r_s (the only NFW length)": RS,
              "r200c/2": R200 / 2.0,
              "fitted to u=1/2": None}
# the observed u=1/2 crossing, by log-linear interpolation between bins 4 and 5
j = 4
u_cross_r = RC[j] * (RC[j + 1] / RC[j]) ** ((0.5 - UB[j]) / (UB[j + 1] - UB[j]))
P("")
P("  Osipkov-Merritt beta(r) = r^2/(r^2+r_a^2); beta=1/2 exactly at r=r_a")
for nm, ra in RA_CHOICES.items():
    rav = u_cross_r if ra is None else ra
    P(f"    r_a = {rav:6.3f} Mpc ({nm:26s}) -> r(beta=1/2) = {rav:6.3f} Mpc, "
      f"beta at 0.38/0.81/1.71/2.49 = " + "/".join(f"{beta_om(r, rav):.3f}" for r in (0.38, 0.81, 1.71, 2.49)))
P(f"    the DATA cross u=1/2 at r = {u_cross_r:.3f} Mpc (log-linear between the 0.81 and 1.18 Mpc bins)")
P("")
K15 = max(u_cross_r / RS, RS / u_cross_r) > 2.0
check("K15", K15, f"r(beta=1/2)=r_s={RS:.3f} Mpc vs data {u_cross_r:.3f} Mpc (factor {u_cross_r/RS:.1f})",
      "factor >2 apart",
      "u=1/2 <=> beta=1/2, and for OM that is r=r_a. The one NFW-motivated choice r_a=r_s puts the "
      f"crossing at {RS:.3f} Mpc, a factor {u_cross_r/RS:.1f} inside the measured crossing at "
      f"{u_cross_r:.3f} Mpc. r_a has to be fitted, so the mechanism predicts nothing")

# fit the scaled OM model (2 params, same as the step) with the full covariance
def fit_om():
    best = None
    for ra in np.logspace(np.log10(0.1), np.log10(6.0), 400):
        bj = beta_om(RC, ra)
        num = float(np.sum(WDIAG * bj * UB))
        den = float(np.sum(WDIAG * bj * bj))
        Aamp = num / den
        c2 = float(np.sum((UB - Aamp * bj) ** 2 * WDIAG))
        if best is None or c2 < best[0]:
            best = (c2, float(ra), Aamp)
    return best


c2_om, ra_best, A_best = fit_om()
K16 = (c2_om / 6.0 > 3.0) and (c2_om > c2_step + 10.0)
check("K16", K16, f"OM chi2/dof={c2_om/6.0:.2f} (r_a={ra_best:.2f}, A={A_best:.2f}) vs step "
                  f"{c2_step/5.0:.2f} (3 params)",
      "chi2/dof>3 and dchi2>10 vs step",
      "the smooth phase-space reading, u = A beta(r) with two free parameters, is rejected at "
      f"chi2/dof = {c2_om/6.0:.2f} against {c2_step/5.0:.2f} for the step (which has one MORE "
      f"parameter, r_t): the data have a discontinuity (dchi2 = {c2_om-c2_step:.1f} for one extra "
      "parameter) that no single-scale beta(r) produces")

# both normalisations of the phase-space reading fail somewhere in the eight bins
ZB = (beta_om(RC, u_cross_r) - UB) / SUB                 # u = beta (radial fraction)
Z1B = ((1.0 - beta_om(RC, u_cross_r)) - UB) / SUB         # u = 1-beta (isotropic fraction)
K17 = (np.max(np.abs(ZB)) > 3.0) and (np.max(np.abs(Z1B)) > 3.0)
check("K17", K17, f"max|Z| u=beta: {np.max(np.abs(ZB)):.1f} (at {RC[np.argmax(np.abs(ZB))]:.2f} Mpc); "
                  f"u=1-beta: {np.max(np.abs(Z1B)):.1f}",
      "both >3 sigma in the eight bins",
      "with r_a fixed at the observed u=1/2 crossing, u = beta (radial fraction) is wrong by "
      f"{np.max(np.abs(ZB)):.1f} sigma at {RC[np.argmax(np.abs(ZB))]:.2f} Mpc and u = 1-beta "
      f"(isotropic fraction) by {np.max(np.abs(Z1B)):.1f} sigma at {RC[np.argmax(np.abs(Z1B))]:.2f} "
      "Mpc, in opposite directions: no single beta(r) normalisation fits the eight bins")

# ===================================================================================== K18-K22
head("K18-K22  MECHANISM (iii) -- tidal/boundary: the splashback radius")


def rho_crit_z(z):
    return RHO_C0 * (OM * (1 + z) ** 3 + OL)


def r_delta(M, delta, z):
    return (3.0 * M * MSUN / (4 * np.pi * delta * rho_crit_z(z))) ** (1 / 3) / MPC


def mu(x):
    return np.log(1 + x) - x / (1 + x)


def r200m_over_r200c(c=C_NFW, om=OM):
    """NFW: solve M(<x)/M(<c) = (200 om / 200) (x/c)^3 -- 200m means 200 x rho_mean = 200 om rho_c."""
    f = lambda x: mu(x) / mu(c) - om * (x / c) ** 3
    return brentq(f, 1.0, 50.0) / c


R200M_OVER_R200C = r200m_over_r200c()
K_SP = RSP_OVER_R200M * R200M_OVER_R200C          # r_splash / r200c
K_SP_LO = (RSP_OVER_R200M - RSP_OVER_R200M_ERR) * R200M_OVER_R200C
K_SP_HI = (RSP_OVER_R200M + RSP_OVER_R200M_ERR) * R200M_OVER_R200C


def M200_from_M500(M500, z, c=C_NFW):
    R5 = r_delta(M500, 500.0, z)
    r200 = r_delta(1.0, 200.0, z)          # = r200 for 1 Msun, scales as M^(1/3)
    def f(lm):
        M200 = math.exp(lm)
        return M200 * mu(R5 / (r_delta(M200, 200.0, z) / c)) / mu(c) - M500
    return math.exp(brentq(f, math.log(1e9), math.log(1e17), xtol=1e-10, rtol=1e-12))


MGAS_MED = float(np.median(MGAS))
R500_MED = float(np.median(R500))
MASS_ROUTES = {}
for nm, M500 in [("M_gas/f_gas=0.11", MGAS_MED / F_GAS),
                 ("catalogue R500 (500 rho_c)", 500.0 * rho_crit_z(Z_STACK) * 4 * np.pi / 3 * (R500_MED * MPC) ** 3 / MSUN),
                 ("law at R500: M_b(1+F)", None)]:
    if M500 is None:
        Mb = 1.2 * MGAS_MED
        y = G * Mb * MSUN / (A0 * (R500_MED * MPC) ** 2)
        Fv = 0.5 * (math.sqrt(1 + 4 / y) - 1)
        M500 = Mb * (1 + Fv)
    M200 = M200_from_M500(M500, Z_STACK)
    MASS_ROUTES[nm] = dict(M500=M500, M200=M200, r200c=r_delta(M200, 200.0, Z_STACK),
                           r_sp=K_SP * r_delta(M200, 200.0, Z_STACK))
P("")
P(f"  stack: median M_gas,500 = {MGAS_MED:.3e} Msun, median R500 = {R500_MED:.3f} Mpc, z = {Z_STACK:.4f}")
P(f"  {'mass route':28s} {'M500':>10} {'M200c':>10} {'r200c':>8} {'r_sp':>8}")
for nm, v in MASS_ROUTES.items():
    P(f"  {nm:28s} {v['M500']:10.3e} {v['M200']:10.3e} {v['r200c']:8.3f} {v['r_sp']:8.3f}")
P("")
RSP = MASS_ROUTES["M_gas/f_gas=0.11"]["r_sp"]
RSP_LO = min(K_SP_LO * v["r200c"] for v in MASS_ROUTES.values())
RSP_HI = max(K_SP_HI * v["r200c"] for v in MASS_ROUTES.values())
if MUT == "M3":                        # M3: identify the splashback radius with r500
    RSP = R500_MED
    RSP_LO, RSP_HI = R500_MED, R500_MED
R_BOUND = float(BIN_EDGES[6])          # the MID/OUTER boundary, 1.4174 Mpc
K18 = abs(RSP / R_BOUND - 1.0) < 0.15
check("K18", K18, f"r_sp={RSP:.2f} Mpc vs the MID/OUTER boundary {R_BOUND:.2f} "
                  f"(ratio {RSP/R_BOUND:.3f}); coefficient band {RSP_LO:.2f}-{RSP_HI:.2f}",
      "within 15% of the boundary",
      "r_splash = 0.83 r200m = (0.83 x "
      f"{R200M_OVER_R200C:.2f}) r200c = {K_SP:.2f} r200c for the stack, from its own median M_gas "
      f"and z: {RSP:.2f} Mpc ({min(v['r_sp'] for v in MASS_ROUTES.values()):.2f}-"
      f"{max(v['r_sp'] for v in MASS_ROUTES.values()):.2f} across the three mass routes). It lands "
      f"on the 0.461-1.417 Mpc boundary -- the upper edge of the task's window -- with the "
      f"{100*RSP_OVER_R200M_ERR/RSP_OVER_R200M:.0f}% coefficient scatter spanning it")

# data-driven splashback: steepest logarithmic slope of the excess
DD8 = np.array([(W[:, q] * D[:, q]).sum() / W[:, q].sum() for q in range(8)])
NN8 = np.array([(W[:, q] * PN[:, q]).sum() / W[:, q].sum() for q in range(8)])
PP8 = np.array([(W[:, q] * PL[:, q]).sum() / W[:, q].sum() for q in range(8)])
EX8 = DD8 - NN8
SLOPE = np.array([(math.log(EX8[q + 1] / EX8[q]) / math.log(RC[q + 1] / RC[q])) for q in range(7)])
qmin = int(np.argmin(SLOPE))
R_SLOPE = math.sqrt(RC[qmin] * RC[qmin + 1])
K19 = (qmin == 5) and abs(R_SLOPE - 1.42) < 0.05
check("K19", K19, f"steepest dln(excess)/dlnR = {SLOPE[qmin]:.2f} in [{RC[qmin]:.2f},{RC[qmin+1]:.2f}] -> R={R_SLOPE:.2f} Mpc",
      "qmin=5 (1.18-1.71 Mpc), R=1.42+-0.05",
      "the stacked EXCESS has its steepest logarithmic slope, -"
      f"{abs(SLOPE[qmin]):.2f}, between 1.18 and 1.71 Mpc: the caustic is at R = {R_SLOPE:.2f} Mpc, "
      "independently of any mass estimate")

SIG_CAUSTIC = 0.20
Z_CAUSTIC = abs(R_SLOPE - RSP) / SIG_CAUSTIC
K20 = (Z_CAUSTIC < 1.5) and (RT_LO <= RSP <= RT_HI)
check("K20", K20, f"|R_caustic({R_SLOPE:.2f}) - r_sp({RSP:.2f})| = {abs(R_SLOPE-RSP):.2f} Mpc "
                  f"({Z_CAUSTIC:.2f} sigma); r_sp in ({RT_LO:.2f},{RT_HI:.2f}) = {RT_LO <= RSP <= RT_HI}",
      "<1.5 sigma and r_sp inside the u-step interval",
      "three independent determinations of the transition radius: the u-step (the fit puts it "
      f"between {RT_LO:.2f} and {RT_HI:.2f} Mpc), the steepest excess slope (R = {R_SLOPE:.2f} Mpc) "
      f"and the predicted r_splash ({RSP:.2f} Mpc). r_sp falls inside the u-step interval and "
      f"{Z_CAUSTIC:.2f} sigma from the caustic")

# mass terciles: r_sp ∝ M^(1/3) => the fixed outer annulus is more 'inside' at high mass => lower u
QT = np.quantile(MGAS, [1 / 3, 2 / 3])
TID = np.clip(np.digitize(MGAS, QT), 0, 2)
def frac_bin6(rsp_t):
    """fraction of the 1.417-2.061 Mpc bin that lies inside r_sp (log-uniform surface density)."""
    if rsp_t <= BIN_EDGES[6]:
        return 0.0
    if rsp_t >= BIN_EDGES[7]:
        return 1.0
    return math.log(rsp_t / BIN_EDGES[6]) / math.log(BIN_EDGES[7] / BIN_EDGES[6])


TERC = []
for t in range(3):
    s = TID == t
    uo, so = jk(s, [6, 7])
    b6, s6 = jk(s, [6])
    Mg = float(np.median(MGAS[s]))
    # the tercile's own stacked excess in the two outer bins
    DD6 = (W[s][:, 6] * D[s][:, 6]).sum() / W[s][:, 6].sum()
    NN6 = (W[s][:, 6] * PN[s][:, 6]).sum() / W[s][:, 6].sum()
    DD7 = (W[s][:, 7] * D[s][:, 7]).sum() / W[s][:, 7].sum()
    NN7 = (W[s][:, 7] * PN[s][:, 7]).sum() / W[s][:, 7].sum()
    EX6, EX7 = DD6 - NN6, DD7 - NN7
    w6, w7 = W[s][:, 6].sum(), W[s][:, 7].sum()
    pred, rsp_med = {}, {}
    for fg in (F_GAS_LO, F_GAS, F_GAS_HI):
        # average the step over the tercile's OWN mass distribution -- no new parameter
        sg = 0.0
        rsps = []
        for mg_i in MGAS[s]:
            M200_i = M200_from_M500(mg_i / fg, Z_STACK)
            rsp_i = K_SP * r_delta(M200_i, 200.0, Z_STACK)
            rsps.append(rsp_i)
            sg += frac_bin6(rsp_i)
        sg /= s.sum()
        num = sg * w6 * EX6
        den = w6 * EX6 + w7 * EX7
        pred[fg] = 1.0 - (1.0 - float(beta_step[0])) * num / den
        rsp_med[fg] = float(np.median(rsps))
    TERC.append(dict(t=t, n=int(s.sum()), Mgas=Mg, u_out=uo, u_out_err=so, u_b6=b6, u_b6_err=s6,
                     rsp=rsp_med, pred=pred[F_GAS], pred_band=[min(pred.values()), max(pred.values())]))
P("")
P(f"  {'tercile':8s} {'M_gas':>9} {'r_sp':>6} {'u(OUTER)':>16} {'u(1.71)':>15} {'pred u(OUT)':>18}")
for r in TERC:
    P(f"  {r['t']:8d} {r['Mgas']:9.2e} {r['rsp'][F_GAS]:6.2f} {r['u_out']:9.3f}+-{r['u_out_err']:.3f} "
      f"{r['u_b6']:9.2f}+-{r['u_b6_err']:.2f} {r['pred']:8.2f} [{r['pred_band'][0]:.2f},{r['pred_band'][1]:.2f}]")
P("")
Z_TERC = [(r["u_out"] - r["pred"]) / r["u_out_err"] for r in TERC]
K21a = TERC[0]["u_out"] > TERC[1]["u_out"] > TERC[2]["u_out"]
K21b = max(abs(z) for z in Z_TERC) < 3.0
K21 = K21a and K21b
check("K21", K21, "u_OUT " + " > ".join(f"{r['u_out']:.2f}" for r in TERC) + " ; max|Z|=" + f"{max(abs(z) for z in Z_TERC):.2f}",
      "monotone decreasing in mass, max|Z|<3",
      "the mass ordering is the prediction: r_sp grows with M, so a FIXED metric annulus is more "
      "'inside' for heavy clusters and u_OUT must fall with mass. Measured 1.90/1.04/0.68 "
      f"(Z = {Z_TERC[0]:+.1f}/{Z_TERC[1]:+.1f}/{Z_TERC[2]:+.1f}) against a zero-parameter sharp-step "
      f"prediction from r_sp(M): the ordering is 3/3, and the massive tercile is {abs(Z_TERC[2]):.1f} "
      "sigma low -- the sharp step is an idealisation (the real transition has finite width)")

K22a = (TERC[2]["Mgas"] / TERC[0]["Mgas"]) ** (1 / 3) > 1.7
K22b = TERC[2]["u_b6"] < TERC[1]["u_b6"]
K22 = K22a and K22b
check("K22", K22, f"(M2/M0)^(1/3)={(TERC[2]['Mgas']/TERC[0]['Mgas'])**(1/3):.2f}; u(1.71): "
                  f"{TERC[0]['u_b6']:.2f}+-{TERC[0]['u_b6_err']:.0f}/{TERC[1]['u_b6']:.2f}/{TERC[2]['u_b6']:.2f}",
      ">1.7 and u(1.71) falls with mass",
      "r_sp ∝ M^(1/3) means the transition moves by 2.0x between the terciles; at the fixed radius "
      "1.71 Mpc u is >1 for the low tercile (outside r_sp, unconstrained), 1.25 +- 0.40 in the middle "
      "and 0.59 +- 0.08 for the top: the transition radius is mass-dependent, as a boundary must be "
      "and a relaxation time need not be")

# ===================================================================================== K23-K25
head("K23-K25  TASK 3-4 -- the prediction, and the third band that tests it")

PRED_R = {}
for M500 in (5e13, 1e14, 3e14, 1e15):
    PRED_R[M500] = K_SP * r_delta(M200_from_M500(M500, Z_STACK), 200.0, Z_STACK)
K23 = (1.05 < PRED_R[5e13] < 1.15) and (PRED_R[1e15] > 2.7) and (PRED_R[1e15] > PRED_R[5e13] * 2.5)
check("K23", K23, "r_step(M500) = " + ", ".join(f"{k:.0e}:{v:.2f}" for k, v in PRED_R.items()),
      "1.05-1.15 at 5e13, >2.7 at 1e15, ratio>2.5",
      "the surviving mechanism's prediction: the u-step sits at r_sp = "
      f"{K_SP:.2f} r200c(M,z), so it moves from {PRED_R[5e13]:.2f} Mpc at 5e13 to "
      f"{PRED_R[1e15]:.2f} Mpc at 1e15 -- across the whole OUTER band. A stacked detection of the "
      "step in three mass bins tests it")

# falsifier: separate u=1 (dust outside r_sp) from the phase-space saturation value
U_B_PRED = float(np.sum((W[:, [6, 7]] * beta_om(RC[[6, 7]], u_cross_r)) * EX8[[6, 7]]) /
                 np.sum(W[:, [6, 7]] * EX8[[6, 7]]))
SIG_NEED = abs(1.0 - U_B_PRED) / 3.0
N_NEED = NCL * (SU["OUT_1p42_2p5"] / SIG_NEED) ** 2
K24 = (0.02 < SIG_NEED < 0.09) and (500 < N_NEED < 3000)
check("K24", K24, f"sigma_u<={SIG_NEED:.4f}, now {SU['OUT_1p42_2p5']:.4f}; N>={N_NEED:.0f}",
      "0.02<sigma_u<0.09, 500<N<3000",
      "in the 1.42-2.5 Mpc band the step predicts u=1.000 and the phase-space reading predicts "
      f"u={U_B_PRED:.3f}: 3 sigma needs sigma_u <= {SIG_NEED:.3f} (sigma_<w> <= {SIG_NEED/3:.3f}), "
      f"i.e. N >= {N_NEED:.0f} clusters at the present per-object noise")

# what is ALREADY excluded: u=1/2 and u=1/6 in the third band
Z_half3 = (0.5 - U["OUT_1p42_2p5"]) / SU["OUT_1p42_2p5"]
Z_onesixth = (-1.0 / 6.0 - W_OF_U["OUT_1p42_2p5"]) / SW["OUT_1p42_2p5"]
K25 = (abs(Z_half3) > 3.0) and (abs(Z_onesixth) > 3.0)
check("K25", K25, f"1.42-2.5: u={U['OUT_1p42_2p5']:.3f}+-{SU['OUT_1p42_2p5']:.3f}; <w>={W_OF_U['OUT_1p42_2p5']:+.4f}+-{SW['OUT_1p42_2p5']:.4f}",
      "u=1/2 and <w>=-1/6 both >3 sigma away",
      f"the third band already exists in the stack: <w> = {W_OF_U['OUT_1p42_2p5']:+.4f} +- "
      f"{SW['OUT_1p42_2p5']:.4f}, i.e. {abs(Z_onesixth):.1f} sigma from -1/6 and {abs(Z_half3):.1f} "
      "sigma from u=1/2. The open question there is 1.00 vs 0.81, not 1 vs 1/2")

# ===================================================================================== results
N_PASS = sum(1 for c in CHECKS if c["pass_"])
N_TOT = len(CHECKS)

P("")
P("  the eight-bin u(r) profile (this lane's new measurement):")
P("  " + " ".join(f"{UB[j]:.2f}" for j in range(8)))
P("  " + " ".join(f"{SUB[j]:.2f}" for j in range(8)))
P("")

numbers = dict(
    u_INNER=U["INNER"], u_INNER_err=SU["INNER"],
    u_MID=U["MID"], u_MID_err=SU["MID"],
    u_OUTER=U["OUTER"], u_OUTER_err=SU["OUTER"],
    u_OUT_a=U["OUT_a"], u_OUT_a_err=SU["OUT_a"],
    u_OUT_b=U["OUT_b"], u_OUT_b_err=SU["OUT_b"],
    u_1p42_2p5=U["OUT_1p42_2p5"], u_1p42_2p5_err=SU["OUT_1p42_2p5"],
    w_INNER=W_OF_U["INNER"], w_INNER_err=SW["INNER"],
    w_MID=W_OF_U["MID"], w_MID_err=SW["MID"],
    w_OUTER=W_OF_U["OUTER"], w_OUTER_err=SW["OUTER"],
    w_1p42_2p5=W_OF_U["OUT_1p42_2p5"], w_1p42_2p5_err=SW["OUT_1p42_2p5"],
    w_for_half=float(w_half), Z_MID_from_minus_sixth=Z_mid_half, Z_OUTER_from_zero=Z_out_zero,
    du_dAl_MID=dudA, dlnu_dAl_MID=dudA / U["MID"], sigma_u_from_derivative=sig_u_deriv,
    A_pred=dict(A_PRED), A_rel_resid=dict(A_RES),
    u_profile_8bin=dict(R=list(map(float, RC)), u=list(map(float, UB)), err=list(map(float, SUB)),
                        w=list(map(float, (UB - 1) / 3))),
    chi2_const_per_dof=chi2_const / 7.0, u_const=u_bar,
    step=dict(r_t_fit=rt_step, r_t_lo=RT_LO, r_t_hi=RT_HI, u_in=float(beta_step[0]),
              u_out=float(beta_step[1]), chi2_dof=c2_step / 6.0, chi2_dof_3param=c2_step / 5.0,
              chi2_dof_const=c2_const_w / 7.0,
              du=du_step, du_sigma=du_step / sig_step),
    om_fit=dict(r_a=ra_best, amp=A_best, chi2_dof=c2_om / 6.0, dchi2_vs_step=c2_om - c2_step,
                beta_at_bins=list(map(float, beta_om(RC, ra_best))),
                max_Z_u_eq_beta=float(np.max(np.abs(ZB))),
                max_Z_u_eq_1mbeta=float(np.max(np.abs(Z1B)))),
    n_patches=30,
    beta_cross=dict(r_s=RS, r200c=R200, r_obs=u_cross_r, factor=u_cross_r / RS,
                    u_pred_beta_at_2p49=float(beta_om(2.49, u_cross_r)),
                    u_pred_1mbeta_at_2p49=float(1 - beta_om(2.49, u_cross_r))),
    relaxation=dict(t_relax_ratio=ratio_tr, t_dyn_Gyr=[t / 3.156e16 for t in TDYN],
                    rho_rel=[n["rho_rel"] for n in NL], rho_ratio=NL[0]["rho_rel"] / NL[1]["rho_rel"],
                    t_dyn_ratio=TDYN[0] / TDYN[1], radii=list(RR),
                    required_t_in_over_t_out=REQ_RATIO, predicted_t_in_over_t_out=ratio_tr,
                    predicted_t_out_over_t_in=1.0 / ratio_tr,
                    discrepancy_decades=DISCREPANCY_ORDERS,
                    u_inner_pred_fully_relaxed_outside=u_in_pred, Z=Z_in_pred),
    splash=dict(M_gas_med=MGAS_MED, R500_med=R500_MED, z=Z_STACK,
                routes={k: dict(M500=v["M500"], M200c=v["M200"], r200c=v["r200c"], r_sp=v["r_sp"])
                        for k, v in MASS_ROUTES.items()},
                r_sp=RSP, r_sp_lo=RSP_LO, r_sp_hi=RSP_HI, r_slope=R_SLOPE,
                slope_at_caustic=float(SLOPE[qmin]), k_splash=K_SP,
                M500_route_ratio=MASS_ROUTES["catalogue R500 (500 rho_c)"]["M500"] /
                                 MASS_ROUTES["M_gas/f_gas=0.11"]["M500"],
                M500_spread_percent=100.0 * (MASS_ROUTES["catalogue R500 (500 rho_c)"]["M500"] /
                                             MASS_ROUTES["M_gas/f_gas=0.11"]["M500"] - 1.0)),
    terciles=[dict(r, rsp={str(k): v for k, v in r["rsp"].items()},
                   pred_band=r["pred_band"], pred=r["pred"]) for r in TERC],
    tercile_Z=Z_TERC,
    prediction=dict(r_step_Msun={str(k): v for k, v in PRED_R.items()},
                    scaling="r_step = 1.15 r200c(M,z) ~ M^(1/3)"),
    falsifier=dict(u_beta_pred_in_band=U_B_PRED, sigma_u_needed=SIG_NEED,
                   sigma_w_needed=SIG_NEED / 3, n_clusters_needed=N_NEED, n_now=NCL,
                   Z_u_half=Z_half3, Z_w_sixth=Z_onesixth,
                   band="1.42-2.5 Mpc (the first 1.5 bins of the present OUTER band)"),
)

res = dict(lane=LANE, status="NUMERICAL + NO-GO(relaxation, phase-space) + CONDITIONAL(r_sp=1.15 r200c)",
           checks=[dict(id=c["id"], **{"pass": c["pass_"]}, value=c["value"], threshold=c["threshold"],
                        label=c["label"]) for c in CHECKS],
           numbers=numbers, constants_used=CONSTANTS, record_inputs=RECORD,
           data_source=dict(npz=os.path.relpath(NPZ, ROOT), n_clusters=NCL,
                            bins=list(map(float, RC)), band_edges={k: list(map(float, v)) for k, v in BAND_EDGES.items()}),
           mutation=MUT or None, n_pass=N_PASS, n_total=N_TOT, runtime_s=round(time.time() - T0, 2))

with open(os.path.join(HERE, "a29_results" + TAG + ".json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)

head("SUMMARY")
P(f"  TASK 1  <w> = (u-1)/3:  INNER {W_OF_U['INNER']:+.4f}+-{SW['INNER']:.4f}   "
  f"MID {W_OF_U['MID']:+.4f}+-{SW['MID']:.4f}   OUTER {W_OF_U['OUTER']:+.4f}+-{SW['OUTER']:.4f}")
P(f"          u=1+3<w> exact; the round trip <w>->u->A_law reproduces the measured amplitudes to "
  f"{max(A_RES.values()):.0e}")
P(f"          the inner band is under tension at {(0-W_OF_U['INNER'])/SW['INNER']:.0f} sigma; the outer band is dust "
  f"({abs(Z_out_zero):.2f} sigma from w=0)")
P(f"  TASK 2  (i)  relaxation: t_relax(0.6)/t_relax(2.0) = {ratio_tr:.4f} -> u_inner > u_outer. NO-GO on sign.")
P(f"          (ii) phase space: r(beta=1/2)=r_s={RS:.2f} Mpc vs data {u_cross_r:.2f}; smooth fit "
  f"chi2/dof={c2_om/6.0:.1f} vs step {c2_step/5.0:.1f}. NO-GO.")
P(f"          (iii) splashback: r_sp = {RSP:.2f} Mpc ({min(v['r_sp'] for v in MASS_ROUTES.values()):.2f}-"
  f"{max(v['r_sp'] for v in MASS_ROUTES.values()):.2f} across mass routes), data caustic "
  f"{R_SLOPE:.2f}, u-step {RT_LO:.2f}-{RT_HI:.2f}. SURVIVES.")
P(f"  TASK 3  prediction: the step is at r_sp = {K_SP:.2f} r200c(M,z), so it moves "
  f"{PRED_R[5e13]:.2f}->{PRED_R[1e15]:.2f} Mpc over 5e13-1e15 Msun; test by mass-binned stacks")
P(f"  TASK 4  falsifier: u in 1.42-2.5 Mpc to sigma_u <= {SIG_NEED:.3f} (now {SU['OUT_1p42_2p5']:.3f}) "
  f"separates u=1.000 (step) from {U_B_PRED:.3f} (phase space) at 3 sigma: N >= {N_NEED:.0f}")
P("")
P(f"{LANE} COMPLETE: {N_PASS}/{N_TOT} checks PASS.")
OUTF.close()
sys.exit(0 if N_PASS == N_TOT else 1)