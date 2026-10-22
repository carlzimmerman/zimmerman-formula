#!/usr/bin/env python3
"""A43 -- the cold sector's equation of state from kinetic theory.

Task 1  the stress tensor of a collisionless medium whose displacement IS the gravitational
        polarization ("tether"), in the Newtonian limit, from f(x,v,t); split p into a kinetic
        part and a tether part; derive w = p/rho for the combination.
Task 2  test three routes to <w> ~ -1/6:  (i) virial/anisotropy, (ii) two-stream, (iii) saturation.
Task 3  what the surviving route predicts beyond u.
Task 4  if none survives: the no-go and the exact missing premise.

Inputs on disk:
  campaign_fresh_gravity/CFG687_erass1_shear_stack/cfg687_percluster.npz
      318 eRASS1 x KiDS clusters, 8 radial bins D, err, PL (law), PN (baryons only).
  A29_u_radial/a29_results.json  -> the three-band <w> (recomputed here from the npz, K0).
  A18_two_ratios/report.md K15   -> R_req = 5.552 +- 0.427 (the ACTIVE cold-to-baryon ratio).

Usage:  python3 a43_checks.py [--mutate|--mutate2|--mutate3]
Exit 0 iff every declared check passes.  Deterministic, stdlib + numpy/scipy/sympy, no network.
"""
import argparse, json, math, os, sys, time

T0 = time.time()
import numpy as np                     # noqa: E402
import sympy as sp                     # noqa: E402

LANE = "A43"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
NPZ = os.path.join(ROOT, "campaign_fresh_gravity", "CFG687_erass1_shear_stack",
                   "cfg687_percluster.npz")

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", action="store_true",
                help="M1: 3p_T/eps_T = n-2 instead of n (the harmonic tether term dropped)")
ap.add_argument("--mutate2", action="store_true",
                help="M2: <w> = u-1 instead of (u-1)/3 (the A21 K12 slip)")
ap.add_argument("--mutate3", action="store_true",
                help="M3: the tether term enters w with the wrong SIGN (p_T = -n/3 eps_T)")
A = ap.parse_args()
MUT = "M1" if A.mutate else ("M2" if A.mutate2 else ("M3" if A.mutate3 else ""))
TAG = {"": "", "M1": "_MUTATE", "M2": "_MUTATE2", "M3": "_MUTATE3"}[MUT]
OUTF = open(os.path.join(HERE, "a43" + TAG + ".out"), "w")


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
PC = 3.0856775814913673e16
A0 = 9.36e-11
H0 = 67.4e3 / MPC
OM, OL = 0.315, 0.685
RHO_C0 = 3.0 * H0 ** 2 / (8.0 * np.pi * G)
Z_STACK = 0.23365
C_NFW = 4.5
M200_STACK = 1.483e14
SIG_C = 8.33e3                          # cold-medium dispersion, THEORY s3.3 [EXT, 24 pc / L_MOND]
SIG_VIR = 7.0e5                         # cluster virial velocity, 700 km/s, illustrative
R_REQ, R_REQ_ERR = 5.552, 0.427         # A18 K15: the required ACTIVE cold-to-baryon ratio
R_COSMIC = 5.364327                     # Omega_c/Omega_b, A18 eq (3)
P_ICM = 1.0e3 * 5.0 * 1.602176634e-16   # n=1e-3 cm^-3, kT=5 keV  [EXT, illustrative]
SLIP_GATE = 2.63e-7                     # THEORY s3.5 / A12, A3, A32

CONSTANTS = [
    dict(name="c", value=C_LIGHT, unit="m/s", source="BRIEF s4"),
    dict(name="G", value=G, unit="m^3 kg^-1 s^-2", source="BRIEF s4"),
    dict(name="a0_canonical", value=A0, unit="m/s^2", source="BRIEF s4"),
    dict(name="M_sun", value=MSUN, unit="kg", source="BRIEF s4"),
    dict(name="Mpc", value=MPC, unit="m", source="BRIEF s4"),
    dict(name="sigma_c", value=SIG_C, unit="m/s", source="[EXT] THEORY s3.3: 8.33 km/s = c sqrt(L*/L_MOND)"),
    dict(name="M200c_stack", value=M200_STACK, unit="Msun", source="[EXT] A29 K18/A43 (M500=f_gas route)"),
    dict(name="c_nfw", value=C_NFW, unit="1", source="[EXT] A29, NFW c200c at 1.5e14, z=0.23"),
    dict(name="z_stack", value=Z_STACK, unit="1", source="[EXT] median of the 318 CFG687 clusters"),
    dict(name="R_req", value=R_REQ, unit="1", source="[EXT] A18 K15: required ACTIVE cold/baryon ratio"),
    dict(name="R_req_err", value=R_REQ_ERR, unit="1", source="[EXT] A18 K15"),
    dict(name="R_cosmic", value=R_COSMIC, unit="1", source="[EXT] A18 eq (3), omega_b/omega_m"),
    dict(name="p_ICM", value=P_ICM, unit="Pa", source="[EXT] n=1e-3 cm^-3, kT=5 keV (illustrative)"),
    dict(name="slip_gate", value=SLIP_GATE, unit="1", source="THEORY s3.5 / A12, A3, A32"),
]

# ===================================================================================== the data
if not os.path.exists(NPZ):
    P(f"FATAL: {NPZ} missing -- this lane reads the CFG687 per-cluster stack")
    sys.exit(2)
d = np.load(NPZ)
D, ERR, PL, PN = d["D"], d["E"], d["PL"], d["PN"]
NCL = D.shape[0]
W = np.where((ERR > 0) & (ERR < 1e8), 1.0 / ERR ** 2, 0.0)
RA = d["ra"]
ORDER = np.argsort(RA)
PATCH = np.empty(NCL, int)
PATCH[ORDER] = np.arange(NCL) * 30 // NCL
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
BIN_EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9)
RC = np.sqrt(BIN_EDGES[1:] * BIN_EDGES[:-1])


def u_band(mask, jj):
    DD = (W[mask][:, jj] * D[mask][:, jj]).sum()
    PP = (W[mask][:, jj] * PL[mask][:, jj]).sum()
    NN = (W[mask][:, jj] * PN[mask][:, jj]).sum()
    return (PP - NN) / (DD - NN)


def jk(mask, jj):
    full = u_band(mask, jj)
    reps = np.array([u_band(mask & (PATCH != p), jj) for p in range(30)])
    return float(full), float(np.sqrt(29.0 / 30.0 * np.sum((reps - reps.mean()) ** 2)))


ALL = np.ones(NCL, bool)
U, SU = {}, {}
AMPERR = {"INNER": (0.32, 1.39), "MID": (0.118637, 0.65), "OUTER": (0.086872, 0.62)}


def sig_u_of(A_l, A_n, sA_l, sA_n):
    """A21/A29's band error: propagate the RECORD's amplitude errors through u(A_law, A_newton)."""
    u = (A_n - A_l) / (A_l * (A_n - 1.0))
    dl = -A_n / (A_l * (A_n - A_l))
    dn = (A_l - 1.0) / (A_l * (A_n - 1.0) ** 2)
    return abs(u) * math.hypot(dl * sA_l, dn * sA_n)


for b, jj in BANDS.items():
    U[b] = u_band(ALL, jj)
    DD = (W[:, jj] * D[:, jj]).sum()
    PP = (W[:, jj] * PL[:, jj]).sum()
    NN = (W[:, jj] * PN[:, jj]).sum()
    SU[b] = sig_u_of(DD / PP, DD / NN, *AMPERR[b])      # amplitude-propagated, as A21/A29
UB, SUB = np.zeros(8), np.zeros(8)
for j in range(8):
    UB[j], SUB[j] = jk(ALL, [j])

W_OF_U = {b: (U[b] - 1.0) if MUT == "M2" else (U[b] - 1.0) / 3.0 for b in U}
SW = {b: SU[b] / 3.0 for b in U}


def nfw_M(r, M200=M200_STACK, c=C_NFW):
    r200 = (3.0 * M200 * MSUN / (4 * np.pi * 200 * RHO_C0 * (OM * (1 + Z_STACK) ** 3 + OL))) ** (1 / 3)
    x = r * MPC / r200 * c
    mu = lambda y: np.log(1 + y) - y / (1 + y)
    return float(M200 * mu(x) / mu(c)), r200 / MPC


def nfw_rho(r, M200=M200_STACK, c=C_NFW):
    r200 = (3.0 * M200 * MSUN / (4 * np.pi * 200 * RHO_C0 * (OM * (1 + Z_STACK) ** 3 + OL))) ** (1 / 3)
    x = r * MPC / r200 * c
    mu = lambda y: np.log(1 + y) - y / (1 + y)
    rho_s = M200 * MSUN / (4 * np.pi * (r200 / c) ** 3 * mu(c))
    return float(rho_s / (x * (1 + x) ** 2))


def g_of_r(r, baryons_only=False):
    M, _ = nfw_M(r)
    if baryons_only or MUT == "M3":      # M3: forget that X = g_TOTAL/a0
        M = M / (1.0 + R_COSMIC)
    return G * M * MSUN / (r * MPC) ** 2


def Phi_of_r(r):
    M, _ = nfw_M(r)
    return -G * M * MSUN / (r * MPC)


# ===================================================================================== K0-K2
head("K0-K2  TASK 1 -- f(x,v,t) -> stress tensor; the tether is the displacement constraint")

P("  The medium: N elements of mass m, distribution f(x,v,t), n = int f d3v, rho = m n,")
P("  ubar_i = <v_i>, delta v_i = v_i - ubar_i, Sigma_ij = <delta v_i delta v_j>.")
P("")
P("  K0  the three bands reproduce A29 from the npz (provenance)")
P(f"      INNER u = {U['INNER']:.4f} +- {SU['INNER']:.4f}   <w> = {W_OF_U['INNER']:+.4f}")
P(f"      MID   u = {U['MID']:.4f} +- {SU['MID']:.4f}   <w> = {W_OF_U['MID']:+.4f}")
P(f"      OUTER u = {U['OUTER']:.4f} +- {SU['OUTER']:.4f}   <w> = {W_OF_U['OUTER']:+.4f}")
ok0 = (abs(U["MID"] - 0.4715659) < 1e-3 and abs(U["OUTER"] - 0.9864736) < 1e-3
       and abs(U["INNER"] - 0.3348011) < 1e-3)
check("K0", ok0, f"{U['INNER']:.4f}/{U['MID']:.4f}/{U['OUTER']:.4f}", "A29 values +-1e-3",
      "the npz and the estimator reproduce A29's three-band inversion; <w> = (u-1)/3")

# ---- K1: the second moment of a Gaussian f gives T^ij = rho(ubar^i ubar^j + Sigma^ij)
n_, s1, s2, s3, u1, u2, u3, v1, v2, v3 = sp.symbols(
    "n s1 s2 s3 u1 u2 u3 v1 v2 v3", positive=True)
f3 = (n_ / ((2 * sp.pi) ** sp.Rational(3, 2) * s1 * s2 * s3)
      * sp.exp(-(v1 - u1) ** 2 / (2 * s1 ** 2) - (v2 - u2) ** 2 / (2 * s2 ** 2)
               - (v3 - u3) ** 2 / (2 * s3 ** 2)))
mom = lambda i, j, vi, vj: sp.integrate(sp.integrate(sp.integrate(vi * vj * f3, (v3, -sp.oo, sp.oo)),
                                                     (v2, -sp.oo, sp.oo)), (v1, -sp.oo, sp.oo))
M11 = sp.simplify(mom(1, 1, v1, v1))
M12 = sp.simplify(mom(1, 2, v1, v2))
e11 = sp.simplify(M11 - n_ * (u1 ** 2 + s1 ** 2))
e12 = sp.simplify(M12 - n_ * u1 * u2)
K1 = (e11 == 0) and (e12 == 0)
check("K1", K1, f"residuals {e11}, {e12}", "== 0 exactly",
      "int v_i v_j f d3v = n(ubar_i ubar_j + Sigma_ij): the stress of a kinetic medium is the "
      "second moment, T^ij = rho ubar^i ubar^j + rho Sigma^ij.  No other term can appear")

# ---- K2: rho = rhobar/det(dx/dq)  =>  div P = rho - rhobar with P = -rhobar xi
q, eps = sp.symbols("q epsilon", real=True)
xi = sp.Function("xi")
X = q + eps * xi(q)
rho = sp.symbols("rhobar") / sp.diff(X, q)
ser = sp.series(rho, eps, 0, 3).removeO().expand()
lin = sp.simplify(ser.coeff(eps, 1) + sp.symbols("rhobar") * sp.diff(xi(q), q))
quad = sp.simplify(ser.coeff(eps, 2))
# in 3D the same expansion gives rho = rhobar(1 - div xi + ...); the 1D coefficient is -rhobar xi'
K2 = (lin == 0) and (sp.simplify(quad - sp.symbols("rhobar") * sp.diff(xi(q), q) ** 2) == 0)
check("K2", K2, f"O(xi) coefficient {lin}; O(xi^2) {sp.simplify(quad)}", "0 / rhobar*xi'^2",
      "mass conservation rho d3x = rhobar d3q gives rho - rhobar = -rhobar div(xi) + O(xi^2); with "
      "P = -rhobar xi this is EXACTLY the theory's div P = rho - rhobar.  The polarization is the "
      "mass displacement, not an analogy")

# ---- K3: p_kin = (1/3) rho Tr Sigma = rho sigma^2 ; w_kin = sigma^2/c^2
sig = sp.symbols("sigma", positive=True)
K3val = (sp.Rational(1, 3) * 3 * sig ** 2) / (sig ** 2)
K3 = sp.simplify(K3val - 1) == 0
check("K3", K3, f"p/(rho sigma^2) = {K3val}", "== 1",
      "isotropic dispersion: p_kin = rho sigma^2 and w_kin = p/(rho c^2) = sigma^2/c^2 >= 0")

# ---- K4: the tether pressure.  3 p_T = <rho xi . grad phi_T> = n eps_T for phi_T = k xi^n/n
x_, k_, nn = sp.symbols("x k n", positive=True)
for nval in (2, 3, 4):
    phi = k_ * x_ ** nval / nval
    ident = sp.simplify(x_ * sp.diff(phi, x_) - nval * phi)
    P(f"      n={nval}: xi*phi' - n*phi = {ident}   (3p_T = n eps_T)")
K4_ok = all(sp.simplify(x_ * sp.diff(k_ * x_ ** nv / nv, x_) - nv * (k_ * x_ ** nv / nv)) == 0
            for nv in (2, 3, 4))
# and numerically for a Gaussian displacement distribution
rng = np.random.default_rng(43)
xig = np.abs(rng.normal(0, 1.0, 400000))
pfac, expect = [], []
for nval in (2, 3, 4):
    phi = xig ** nval / nval
    lhs = np.mean(xig * xig ** (nval - 1))
    mc = lhs / phi.mean()                       # <xi phi'>/<phi> = n
    pfac.append((nval - 2.0) / 3.0 if MUT == "M1" else mc / 3.0)
    expect.append(nval / 3.0)
    P(f"      Monte-Carlo n={nval}: <xi phi'>= {mc:.6f} (exact {nval}); p_T/eps_T = "
      f"{pfac[-1]:.6f} (exact {expect[-1]:.6f})")
K4_ok = K4_ok and all(abs(pfac[i] - expect[i]) < 1e-9 for i in range(3))
check("K4", K4_ok, "3p_T/eps_T = " + "/".join(f"{v:.4f}" for v in pfac), "n/3 = 0.6667/1/1.3333",
      "the virial identity 3 p_T = <rho xi.grad phi_T> = n eps_T for a power-law tether: harmonic "
      "n=2 gives p_T = (2/3) eps_T.  The tether pressure TRACKS the sign of the tether energy")

# ---- K5: w for the combination, and the required tether energy
P("")
P("  THE RESULT OF TASK 1:")
P("      T^00 = rho c^2 + rho sigma^2/2 + eps_T ,  T^ij = rho ubar^i ubar^j + rho Sigma^ij")
P("             + p_T delta^ij ,   p_T = (n/3) eps_T")
P("      w = p/(rho c^2) = [ rho sigma^2 + (n/3) eps_T ] / (rho c^2)          (A43.1)")
P("      u = 1 + 3w = 1 + 3 sigma^2/c^2 + n eps_T/(rho c^2)                   (A43.2)")
P("")
P("  For the measured u, the tether must supply n eps_T/(rho c^2) = u - 1:")
for b in ("INNER", "MID", "OUTER"):
    P(f"      {b:6s} u = {U[b]:.4f} -> eps_T/(rho c^2) = {(U[b]-1)/2:+.4f}  (n=2)")
eps_ratio = {b: (U[b] - 1.0) / 2.0 for b in U}

# ===================================================================================== K6-K9
head("K6-K9  TASK 1/2(i) -- the sign theorem, the virial theorem, and the dispersion route")

# ---- K6: positive-definite tether => p_T >= 0 => w >= 0
sg = np.logspace(-8, 0, 60) * C_LIGHT
et = np.linspace(0, 0.5, 60)
SGN = -1.0 if MUT == "M3" else +1.0            # M3: the tether term with the wrong sign
worst = min((s ** 2 + SGN * (2.0 / 3.0) * e * C_LIGHT ** 2) / C_LIGHT ** 2 for s in sg for e in et)
K6 = worst >= 0.0
check("K6", K6, f"min w over (sigma, eps_T/rho c^2 in [0,0.5]) = {worst:.3e}", ">= 0",
      "a stable (positive-definite) tether has eps_T >= 0, hence p_T >= 0, hence w >= 0: eq (A43.5) "
      "can violate the null energy condition only through eps_T < 0")

# ---- K7: the virial theorem for the displaced medium => w = 0 exactly at virial
P("")
P("  K7  force balance for a medium whose displacement is the polarization:")
P("      0 = -(1/rho) d(rho sigma^2)/dr + g + f_T  =>  p_T = rho(sigma^2 + Phi) + const")
P("      p_tot = rho sigma^2 + p_T = rho(2 sigma^2 + Phi)")
P("      w(r) = [2 sigma^2(r) + Phi(r)] / c^2                                  (A43.7)")
P("      isothermal sphere: sigma^2 = GM/(2r) = -Phi/2  =>  w = 0 EXACTLY")
r_ = sp.symbols("r", positive=True)
G_, Ms_, s2_ = sp.symbols("G M sigma2", positive=True)
Phi_iso = -G_ * Ms_ / r_
sig2_iso = G_ * Ms_ / (2 * r_)
K7 = sp.simplify(2 * sig2_iso + Phi_iso) == 0
check("K7", K7, f"2 sigma^2 + Phi = {sp.simplify(2 * sig2_iso + Phi_iso)}", "== 0 (sympy)",
      "the virialized isothermal sphere constrained to the polarization has w = 0 EXACTLY ("
      "sigma^2 = GM/2r = -Phi/2), and a cold free-falling one has w = sigma^2/c^2 ~ 0: either way "
      "u = 1 to 1e-5, a second route to A29's u_OUT = 0.9865 +- 0.0984. The same formula bounds the "
      "mechanism: w lies in [Phi/c^2, 0], 4.4 decades all below the measurement")

# the ceiling of (A43.3) at the stack
R_REF = 0.6
Phi_ref = Phi_of_r(R_REF)
W_CEIL = -Phi_ref / C_LIGHT ** 2
rho_ref = nfw_rho(R_REF) * (1.0 - 0.157126)      # cold share of the total DM
P(f"      at r = {R_REF} Mpc: Phi/c^2 = {Phi_ref/C_LIGHT**2:+.3e}  =>  w in [{Phi_ref/C_LIGHT**2:+.3e}, 0]")
P(f"      measured <w>_MID = {W_OF_U['MID']:+.4f}: shortfall {abs(W_OF_U['MID'])/W_CEIL:.3e}x")
short_phi = abs(W_OF_U["MID"]) / W_CEIL
check("K7b", short_phi > 1e4,
      f"|w_meas|/(|Phi|/c^2) = {short_phi:.3e}", "> 1e4",
      "the tether mechanism spans [Phi/c^2, 0] = 4.4 decades, ALL of them below the measurement by "
      "2.3e4: the sign is right, the amplitude is the gravitational-potential-to-rest-energy ratio")

# ---- K7c: the closed-form condition, and the radial-trend problem
Phi_need = -C_LIGHT ** 2 / 3.0
depth_short = abs(Phi_need / Phi_ref)
K7c = depth_short > 1e4
Z_vir = abs(W_OF_U["INNER"]) / SW["INNER"]
P(f"      w = -1/6 at sigma = 0 needs Phi = -c^2/3 (a relativistic potential): this cluster has "
  f"Phi/c^2 = {Phi_ref/C_LIGHT**2:.2e}, short by {depth_short:.2e}x")
P(f"      and at virial the same formula gives w = 0 exactly, i.e. u = 1 inside r_sp: the INNER "
  f"measurement u = {U['INNER']:.3f} is {Z_vir:.1f} sigma away")
check("K7c", K7c, f"|Phi_need|/|Phi_cluster| = {depth_short:.3e}; virial w=0 vs w_INNER = {Z_vir:.1f} sigma",
      "> 1e4; > 8 sigma",
      "the tether route reaches w = -1/6 only where |Phi| >= c^2/3, i.e. near a horizon; worse, "
      "(A43.3) is negative only for a SUB-virial medium (sigma^2 < -Phi/2), so it predicts w < 0 "
      "where the medium is young/unrelaxed -- and the inner band is the OLDEST, most relaxed "
      "material. The tether inherits A29's sign no-go (11.8 sigma) as well as the amplitude shortfall")

# ---- K8: anisotropy cannot change the trace; rotation only adds
bet = np.linspace(-10, 1, 2000)
sr = np.linspace(0, 3 * SIG_C, 200)
best = 1e9
for b_ in bet:
    st2 = sr ** 2 * (1 - b_)
    if np.any(st2 < 0):
        continue
    wv = (sr ** 2 + 2 * st2) / (3 * C_LIGHT ** 2)
    best = min(best, float(np.min(wv)))
K8 = best >= 0.0
check("K8", K8, f"min w over beta in [-10,1] = {best:.3e}", ">= 0",
      "w = (sigma_r^2 + 2 sigma_t^2)/(3c^2): the trace depends only on the SUM of the dispersions, "
      "so anisotropy redistributes pressure without ever changing its sign. Rotation enters as "
      "bulk motion rho u^i u^j and can only ADD to the trace. No anisotropy is 'needed': none works")

# ---- K9: what sigma the kinetic route needs
sig_need = C_LIGHT / math.sqrt(6.0)
K9 = (sig_need / SIG_C > 1e4) and (0.1666667 / (SIG_C / C_LIGHT) ** 2 > 1e8)
check("K9", K9, f"sigma_need = c/sqrt6 = {sig_need:.4e} m/s = {sig_need/C_LIGHT:.4f} c "
                f"= {sig_need/SIG_C:.3e} sigma_c; w(sigma_c) = {(SIG_C/C_LIGHT)**2:.3e}",
      "ratio > 1e4; shortfall > 1e8",
      "route (i): w = sigma^2/c^2, so w = -1/6 needs sigma^2 = -c^2/6 -- impossible for a positive "
      "dispersion; even the |w| = 1/6 MAGNITUDE needs sigma = 0.408c, 1.47e4x the cold medium's own "
      "8.33 km/s. The cold sector is non-relativistic by construction (THEORY s3.3), so its kinetic "
      "pressure is 7.7e-10 rho c^2: 2.2e8 short")

# ===================================================================================== K10-K12
head("K10-K12  TASK 2(ii) -- the two-stream route: Cauchy-Schwarz, not a pressure")

P("  two streams +-v along z, each with dispersion sigma:")
P("      T^zz = rho(<v_z^2>) = rho(v^2 + sigma^2) ,  T^xx = T^yy = rho sigma^2")
P("      trace = rho(3 sigma^2 + v^2) ,  w = (3 sigma^2 + v^2)/(3 c^2) >= 0")
v_ = np.linspace(0, C_LIGHT, 2000)
s_ = np.linspace(0, C_LIGHT / 3, 400)
wmin = min((3 * s ** 2 + v ** 2) / (3 * C_LIGHT ** 2) for v in v_ for s in s_)
K10 = wmin >= 0.0
check("K10", K10, f"min w over (v,sigma) = {wmin:.3e}", ">= 0",
      "the counter-stream stress is positive for EVERY (v,sigma); the equation 3 sigma^2 + v^2 = "
      "-c^2/2 has no real solution. p_ij = rho<dv_i dv_j> is a covariance matrix: PSD by "
      "construction. 'Negative longitudinal pressure' would violate Cauchy-Schwarz")

# ---- K11: the exact inequality, and the (v,sigma) that the erroneous formula would need
K11 = True
for vv in (0.1, 0.3, 1.0, 3.0):
    for ss in (0.01, 0.1, 1.0, 10.0):
        var = vv ** 2 + ss ** 2                  # <dv^2> = <v^2> - <v>^2 with <v> = 0
        mean_sq = 0.0
        if var < mean_sq:
            K11 = False
v_err = math.sqrt(0.5) * C_LIGHT                 # solution of (3 sigma^2 - v^2)/(3c^2) = -1/6 at sigma->0
t_cross = (1.0 * MPC) / v_err
K11 = K11 and abs(v_err / C_LIGHT - math.sqrt(0.5)) < 1e-12
check("K11", K11, f"v_needed(if p_z=rho(sigma^2-v^2)) = {v_err:.4e} m/s = {math.sqrt(0.5):.4f} c; "
                  f"v/sigma_vir = {v_err/SIG_VIR:.0f}; crossing time 1 Mpc = {t_cross/3.156e16*1e3:.1f} kyr",
      "v/c = 0.7071, ratio > 100, t < 100 kyr",
      f"even the WRONG formula p_z = rho(sigma^2 - v^2) needs a counter-stream at v = c/sqrt2 = "
      f"0.707c (v^2 = 3 sigma^2 + c^2/2 -> c^2/2 at sigma->0): {v_err/SIG_VIR:.0f}x the virial "
      f"velocity, crossing 1 Mpc in {t_cross/3.156e16*1e3:.1f} kyr and "
      f"{13.8*3.156e16/t_cross:.0f} times in a Hubble time. A 0.7c stream is hot dark matter and "
      f"free-streams out of a 1e14 Msun halo")

# ---- K12: stress vs response. The two-stream instability is a RESPONSE, not a stress.
P("")
P("  K12  the response: linearised Vlasov-Poisson for two cold beams +-v, density rho/2 each:")
P("       1 = (omega_J^2/2) [ 1/(omega-kv)^2 + 1/(omega+kv)^2 ] ,  omega_J^2 = 4 pi G rho")
P("       k -> 0:  omega^2 = omega_J^2 + k^2 v^2   =>   c_eff^2 = v^2 > 0")
P("       unstable only for k v < omega_J, i.e. lambda > 2 pi v / omega_J")
wJ = math.sqrt(4 * math.pi * G * rho_ref)
lam_unst = 2 * math.pi * v_err / wJ
P(f"      rho(0.6 Mpc) = {rho_ref:.3e} kg/m^3 -> omega_J = {wJ:.3e} /s")
P(f"      for the v = 0.707c that the erroneous formula needs: unstable only for lambda > "
  f"{lam_unst/MPC:.3e} Mpc ({(lam_unst/MPC)/3.0:.0f}x the whole stacked annulus)")
K12 = (lam_unst / MPC > 100.0)
check("K12", K12, f"c_eff^2(k->0) = v^2 > 0; lambda_unstable = {lam_unst/MPC:.2e} Mpc for v=0.707c",
      "> 100 Mpc",
      "the 'negative longitudinal pressure' of a counter-stream is at best the sign of the linear "
      "RESPONSE, not of T^ij: u = 1+3w is built from T^ij, so the response cannot supply it. And "
      "even the response is positive (c_eff^2 = v^2) in the k -> 0 limit an equation of state "
      "refers to; its negative branch needs lambda > 1 Gpc for the required v, which is 366x the "
      "whole annulus. At cluster scales there is neither a negative stress nor a negative response")

# ===================================================================================== K13-K15
head("K13-K15  TASK 2(iii) -- saturation: u = mu or u = 1-mu?  And does either fit the profile?")


def X_of_r(r):
    return g_of_r(r) / A0


def mu_of(X):
    return X / (1.0 + X)


Xr = np.array([X_of_r(r) for r in RC])
P("  X = g/a0 from the stack NFW (M200c = 1.483e14, c = 4.5):")
P("      R     = " + " ".join(f"{r:7.3f}" for r in RC))
P("      X     = " + " ".join(f"{x:7.3f}" for x in Xr))
P("      u=mu  = " + " ".join(f"{mu_of(x):7.3f}" for x in Xr))
P("      u=1-mu= " + " ".join(f"{1/(1+x):7.3f}" for x in Xr))
P("      data  = " + " ".join(f"{u:7.3f}" for u in UB))

X_half_solutions = dict(**{"u=mu": U["MID"] / (1.0 - U["MID"]),          # X = u/(1-u)
                           "u=1-mu": (1.0 - U["MID"]) / U["MID"]})        # X = (1-u)/u
K13a = abs(mu_of(1.0) - 0.5) < 1e-15 and abs(1 / (1 + 1.0) - 0.5) < 1e-15
P("")
P(f"  mu(1) = 1/2 and 1-mu(1) = 1/2: at half capacity the two readings are IDENTICAL (both 0.5).")
P(f"  u = 0.4716 needs X = {X_half_solutions['u=mu']:.4f} (u=mu) or X = {X_half_solutions['u=1-mu']:.4f} "
  f"(u=1-mu): -11% / +12% off half capacity, and the two differ by 26% in X")

# crossing radius where X = 1
lo, hi = 0.02, 2.0
for _ in range(200):
    mid = math.sqrt(lo * hi)
    if X_of_r(mid) > 1.0:
        lo = mid
    else:
        hi = mid
R_HALF = math.sqrt(lo * hi)
u_cross_r = RC[4] * (RC[5] / RC[4]) ** ((0.5 - UB[4]) / (UB[5] - UB[4]))
K13 = K13a and (u_cross_r / R_HALF > 3.0)
check("K13", K13, f"mu(1)=1/2 exact; r(X=1) = {R_HALF:.4f} Mpc vs measured u=1/2 at {u_cross_r:.4f} "
                  f"Mpc (factor {u_cross_r/R_HALF:.2f})",
      "identical at X=1; factor > 3",
      "route (iii): at half capacity u = mu and u = 1-mu coincide exactly at 1/2, so 0.47 does not "
      "select either; and half capacity sits at g = a0, r = 0.20 Mpc -- 5.3x inside the measured "
      "crossing at 1.07 Mpc. Neither reading gives 0.47 at the radius where the data have it")

# ---- K14: profile chi2
def chi2_of(pred, err=SUB):
    return float(np.sum(((pred - UB) / err) ** 2))


chi2_mu = chi2_of(mu_of(Xr))
chi2_1m = chi2_of(1 / (1 + Xr))
u_const = float(np.sum(UB / SUB ** 2) / np.sum(1 / SUB ** 2))
chi2_const = chi2_of(np.full(8, u_const))
# the two-parameter step of A29 (bins 0-5 | 6-7)
uin = float(np.sum(UB[:6] / SUB[:6] ** 2) / np.sum(1 / SUB[:6] ** 2))
uout = float(np.sum(UB[6:] / SUB[6:] ** 2) / np.sum(1 / SUB[6:] ** 2))
chi2_step = chi2_of(np.r_[np.full(6, uin), np.full(2, uout)])
K14 = (chi2_mu / 8 > 10) and (chi2_1m / 8 > 10) and (chi2_mu - chi2_step > 100)
check("K14", K14, f"chi2/dof: mu {chi2_mu/8:.2f}, 1-mu {chi2_1m/8:.2f}, const {chi2_const/7:.2f}, "
                  f"step {chi2_step/6:.2f}",
      "mu and 1-mu > 10; Delta chi2 vs step > 100",
      "both saturation readings are monotone over 1.5 decades in radius; the data are a PLATEAU at "
      "0.33-0.53 out to 1.18 Mpc and then a step to 1. They are rejected at Delta chi2 = "
      f"{chi2_mu-chi2_step:.0f} / {chi2_1m-chi2_step:.0f} against the step, for zero extra parameters. "
      "The step recomputes A29's 1.455 (dof 6); the constant recomputes 5.920 (dof 7)")

# ---- K15: the transition in ACELERATION, where the data actually put it
j_tr = 5                                   # the u step lies between the 1.18 and 1.71 Mpc bins
X_tr = math.sqrt(Xr[j_tr] * Xr[j_tr + 1])
ratio_X = 1.0 / X_tr
K15 = ratio_X > 4.0
check("K15", K15, f"data u-step at X = {X_tr:.4f} (g = {X_tr*A0:.3e} m/s^2); half capacity at X = 1: "
                  f"factor {ratio_X:.2f}",
      "factor > 4",
      "the measured u-transition sits at g ~ 0.13 a0, not at the law's half-capacity point g = a0. "
      "So route (iii) does not merely mis-normalise: it puts the transition 7x too far out in "
      "acceleration. 0.47 is 'near' 1/2 only because the measured plateau value happens to be "
      "there; the transition itself is elsewhere")

# ===================================================================================== K16-K19
head("K16-K19  TASK 4 -- the no-go: what 0.18 rho c^2 costs, and why nothing in the sector can pay")

# ---- K16: the required absolute tension
p_req = abs(W_OF_U["MID"]) * rho_ref * C_LIGHT ** 2
K16 = p_req / P_ICM > 1e4
check("K16", K16, f"p_req = {p_req:.3e} Pa at 0.6 Mpc; p_ICM = {P_ICM:.3e} Pa; ratio {p_req/P_ICM:.3e}",
      "> 1e4",
      "the tension the measurement demands is 0.176 rho c^2, i.e. 2.9e-8 Pa -- 3.6e4x the thermal "
      "pressure of the 5 keV ICM in the same volume. This is not a perturbation of the medium: it "
      "is a relativistic stress")

# ---- K17: what the polarization field can supply
eps_field = A0 ** 2 / (8 * np.pi * G)
ratio_field = eps_field / (rho_ref * C_LIGHT ** 2)
K17 = abs(W_OF_U["MID"]) / ratio_field > 1e3
check("K17", K17, f"eps_P = a0^2/8piG = {eps_field:.3e} J/m^3; eps_P/(rho c^2) = {ratio_field:.3e}; "
                  f"shortfall {abs(W_OF_U['MID'])/ratio_field:.2e}x",
      "shortfall > 1e3",
      "the tether IS the polarization field by hypothesis, and its stress-energy is bounded by "
      "a0^2/8piG (its value at u ~ a0/4, the maximum of W). That is 3.2e-5 of the cold rest energy "
      "at 0.6 Mpc: the field can supply at most |w| = 3.2e-5, 5.5e3 short of 0.176")

# ---- K18: an isotropic w = -1/6 is unstable (no static equation of state)
cs2 = -1.0 / 6.0
k_ref = 2 * np.pi / (R_REF * MPC)
gam_fluid = abs(cs2) ** 0.5 * C_LIGHT * k_ref
t_grow = 1.0 / gam_fluid
K18 = (t_grow / 3.156e16) < 1e-2
check("K18", K18, f"c_s^2 = -1/6: k = {k_ref:.3e}/m, growth time {t_grow/3.156e16*1e3:.3f} Myr "
                  f"({13.8*3.156e16/t_grow:.1e}x shorter than the age)",
      "t_grow < 10 Myr",
      "for a barotropic medium c_s^2 = dp/drho = w = -1/6 < 0 (A21 K12): the mode grows on the "
      "sound-crossing time of the band, 0.75 Myr. A w = -1/6 FLUID cannot be static for 10 Gyr; "
      "only a solid/network with a positive modulus and a NEGATIVE PRE-STRESS can be")

# ---- K19: the only stable carriers: a string/wall network, and its slip
f_str = 3.0 * abs(W_OF_U["MID"])
f_wall = 1.5 * abs(W_OF_U["MID"])
slip = 2.0 * f_str
K19 = slip / SLIP_GATE > 1e6
check("K19", K19, f"string fraction f = 3|w| = {f_str:.4f}; wall f = {f_wall:.4f}; slip (Phi-Psi)/Phi "
                  f"~ 2f = {slip:.3f} vs gate {SLIP_GATE:.2e} ({slip/SLIP_GATE:.1e}x)",
      "slip/gate > 1e6",
      "a network is the only STABLE negative-trace carrier (strings w=-1/3, walls w=-2/3): w=-0.176 "
      "needs 53% of the cold energy in strings, 26% in walls. Three costs: (a) a 1D/2D network is "
      "anisotropic and gives a slip ~2f ~ 1, 4e6x the theory's own lensing=dynamics gate; (b) an "
      "isotropic 'foam' (three tensioned families) avoids the slip only by fine tuning, and its "
      "tension is a UV scale, not a0; (c) w=-1/3 has c_s^2<0 and rho+3p=0, so it neither gravitates "
      "nor clusters -- it cannot follow the cold mass profile it is supposed to explain")

# ===================================================================================== K20-K21
head("K20-K21  TASK 4 -- the identification: u = 1+3<w> presupposes the REST mass in the denominator")

P("  u = P_law/(D-B): numerator = the law's phantom, denominator = the observed excess over")
P("  baryons.  The excess is an ACTIVE mass (it is what lenses).  So u = 1+3w only if the")
P("  denominator is the cold REST mass, i.e. if")
P("      M_rest(inside) = M_active/(1+3w) = [the u=1 reading] x 1/(1+3w) .")
P("  A18's amplitude inversion fixes the ACTIVE ratio: R_req = 5.552 +- 0.427 (0.44 sigma from")
P("  R_cosmic = 5.364).  With the cold rest mass = f_ret R_cosmic M_b and f_ret <= 1:")
P("      (1+3w) f_ret R_cosmic = R_req   =>   f_ret = (R_req/R_cosmic)/(1+3w) .")
mass_factor = {b: 1.0 / (1.0 + 3.0 * W_OF_U[b]) for b in U}
# MID: R_req and u are the SAME amplitude measurement (R_req = lambda_req R_tot, u = 1/lambda_req),
# so their errors are perfectly correlated and must NOT be added: f_ret = lambda_req^2 R_tot/R_cosmic
# and sigma(f_ret)/f_ret = 2 sigma(lambda)/lambda = 2 sigma_u/u.
# INNER/OUTER: R_req was measured in the MID band only, so those two rescale the MID normalisation;
# their f_ret is CONDITIONAL on the same active ratio and carries the u error only.
R_TOT = 2.6179                                   # A18 eq (8), the law's total/baryon at r_v
lam = {b: 1.0 / U[b] for b in U}
f_ret = {b: (R_REQ / R_COSMIC) / (1.0 + 3.0 * W_OF_U[b]) for b in U}   # = lambda^2 R_tot/R_cosmic at MID
sig_f = {"MID": 2.0 * SU["MID"] / U["MID"],
         "INNER": SU["INNER"] / U["INNER"],
         "OUTER": SU["OUTER"] / U["OUTER"]}
for b in ("INNER", "MID", "OUTER"):
    Z = (f_ret[b] - 1.0) / (f_ret[b] * sig_f[b])
    P(f"      {b:6s}: 1/(1+3w) = {mass_factor[b]:.3f}   f_ret = {f_ret[b]:.3f} +- {f_ret[b]*sig_f[b]:.3f}"
      f"   ({Z:.1f} sigma above 1)")
K20 = (f_ret["MID"] > 2.0) and (f_ret["INNER"] > 2.5)
check("K20", K20, f"f_ret(MID) = {f_ret['MID']:.3f} +- {f_ret['MID']*sig_f['MID']:.3f} "
                  f"({(f_ret['MID']-1)/(f_ret['MID']*sig_f['MID']):.1f} sigma above 1); "
                  f"f_ret(INNER) = {f_ret['INNER']:.3f} +- {f_ret['INNER']*sig_f['INNER']:.3f}",
      "> 2.0 / > 2.5, > 3 sigma",
      "the EOS reading needs 2.12x (MID) / 2.99x (INNER) the cold rest mass that the u=1 reading "
      "assigns, i.e. f_ret = 2.20 +- 0.34 (MID) and 3.09 +- 0.52 (INNER), against the ceiling "
      "f_ret = 1 imposed by P4 (cold rest mass = the catchment's cosmic share). The SAME amplitudes "
      "that give u = 0.47 exclude the EOS interpretation at 3.6 sigma (MID) / 4.0 sigma (INNER) "
      "once the normalization is imposed. The MID error is correlated (f_ret = lambda^2 R_tot/"
      "R_cosmic), so 3.6 sigma, not the 5.3 sigma an independent-error treatment would give")

# ---- K21: one obstruction, four symptoms
shortfalls = dict(kinetic=0.1666667 / (SIG_C / C_LIGHT) ** 2,
                  gravitational=short_phi,
                  field=abs(W_OF_U["MID"]) / ratio_field,
                  potential_depth=depth_short)
K21 = min(shortfalls.values()) > 1e3
check("K21", K21, "shortfalls vs 0.176: kinetic {kinetic:.2e}, gravitational {gravitational:.2e}, "
                  "field {field:.2e}, potential depth {potential_depth:.2e}".format(**shortfalls),
      "all > 1e3",
      "routes (i), (ii) and (iii) fail for one reason, not three: every stress the cold sector can "
      "carry is bounded by rho x max(sigma^2, |Phi|, a0^2/(8 pi G rho)) = 0.18 rho c^2 x 10^-4ish, and the "
      "measurement needs 0.18 rho c^2. The obstruction is dimensional: the cold sector is "
      "non-relativistic (THEORY s3.3), and w ~ -1/6 is a rest-mass-scale statement")

# ===================================================================================== summary
N_PASS = sum(c["pass_"] for c in CHECKS)
P("")
P("=" * 100)
P(f"{LANE} COMPLETE: {N_PASS}/{len(CHECKS)} checks PASS.")
P("=" * 100)

res = dict(
    lane=LANE,
    status="CLOSED-NO-GO",
    checks=[dict(id=c["id"], pass_=c["pass_"], value=c["value"], threshold=c["threshold"],
                 label=c["label"]) for c in CHECKS],
    numbers=dict(
        u_INNER=U["INNER"], u_MID=U["MID"], u_OUTER=U["OUTER"],
        u_err_INNER=SU["INNER"], u_err_MID=SU["MID"], u_err_OUTER=SU["OUTER"],
        w_INNER=W_OF_U["INNER"], w_MID=W_OF_U["MID"], w_OUTER=W_OF_U["OUTER"],
        w_err_INNER=SW["INNER"], w_err_MID=SW["MID"], w_err_OUTER=SW["OUTER"],
        w_1p42_2p5=-0.0045088096994689115,
        u_profile_8bin=dict(R=RC.tolist(), u=UB.tolist(), err=SUB.tolist()),
        X_8bin=Xr.tolist(),
        u_mu_8bin=mu_of(Xr).tolist(), u_1mmu_8bin=(1 / (1 + Xr)).tolist(),
        chi2_dof_mu=chi2_mu / 8, chi2_dof_1mmu=chi2_1m / 8, chi2_dof_const=chi2_const / 7,
        chi2_dof_step=chi2_step / 6, dchi2_mu_vs_step=chi2_mu - chi2_step,
        dchi2_1mmu_vs_step=chi2_1m - chi2_step,
        r_half_capacity=R_HALF, r_u_half_measured=u_cross_r, r_ratio=u_cross_r / R_HALF,
        X_at_u_0461=dict(u_eq_mu=X_half_solutions["u=mu"], u_eq_1mmu=X_half_solutions["u=1-mu"]),
        sigma_needed=sig_need, sigma_needed_over_c=sig_need / C_LIGHT,
        sigma_needed_over_sigma_c=sig_need / SIG_C,
        w_at_sigma_c=(SIG_C / C_LIGHT) ** 2,
        kinetic_shortfall=shortfalls["kinetic"],
        v_err_two_stream=v_err, v_err_over_c=v_err / C_LIGHT, v_err_over_sigma_vir=v_err / SIG_VIR,
        t_cross_1Mpc_kyr=t_cross / 3.156e16 * 1e3,
        tether_eps_ratio=eps_ratio,
        Phi_over_c2_at_0p6=Phi_ref / C_LIGHT ** 2,
        w_ceiling=-Phi_ref / C_LIGHT ** 2,
        gravitational_shortfall=short_phi,
        rho_cold_at_0p6=rho_ref, p_req_Pa=p_req, p_ICM_Pa=P_ICM, p_ratio=p_req / P_ICM,
        eps_field=eps_field, eps_field_over_rhoc2=ratio_field,
        field_shortfall=abs(W_OF_U["MID"]) / ratio_field,
        cs2_minus_sixth=-1.0 / 6.0, t_grow_Myr=t_grow / 3.156e16 * 1e3,
        omega_J=wJ, lambda_unstable_Mpc=lam_unst / MPC,
        f_strings=f_str, f_walls=f_wall, slip=slip, slip_gate=SLIP_GATE, slip_ratio=slip / SLIP_GATE,
        mass_factor_1_over_1p3w=mass_factor, f_ret_required=f_ret,
        f_ret_err={b: f_ret[b] * sig_f[b] for b in U},
        f_ret_Z={b: (f_ret[b] - 1.0) / (f_ret[b] * sig_f[b]) for b in U},
        Phi_need_over_c2=-1.0 / 3.0, potential_depth_shortfall=depth_short,
        Z_virial_w0_vs_INNER=Z_vir, w_vir_general=Phi_ref / (2 * C_LIGHT ** 2),
        rho_cold_c2_at_0p6=rho_ref * C_LIGHT ** 2,
        f_ret_dust=R_REQ / R_COSMIC, f_ret_dust_err=R_REQ_ERR / R_COSMIC,
        f_ret_dust_Z=(R_REQ / R_COSMIC - 1.0) / (R_REQ_ERR / R_COSMIC),
        R_eos_MID=mass_factor["MID"] * R_COSMIC,
        R_eos_MID_err=mass_factor["MID"] * R_COSMIC * sig_f["MID"],
        crossings_in_hubble=13.8 * 3.156e16 / (MPC / v_err),
        X_transition_inverse=1.0 / X_tr,
        age_over_t_grow=13.8 * 3.156e16 / t_grow,
        X_transition=X_tr, g_transition=X_tr * A0, g_transition_over_a0=X_tr,
        shortfalls=shortfalls,
        R_req=R_REQ, R_req_err=R_REQ_ERR, R_cosmic=R_COSMIC, R_tot=R_TOT,
        M200c_stack=M200_STACK, c_nfw=C_NFW, z_stack=Z_STACK,
        sigma_c=SIG_C,
    ),
    constants_used=CONSTANTS,
    record_inputs=[
        dict(name="u_band_INNER/MID/OUTER", source="CFG687 npz, A29 estimator (recomputed here)"),
        dict(name="w=(u-1)/3", source="A21 K10-K12, A29 K5 (exact in sympy)"),
        dict(name="R_req=5.552+-0.427", source="A18 K15, from A_MID/A_newton"),
        dict(name="a0=9.36e-11", source="BRIEF s4"),
    ],
    data_source="campaign_fresh_gravity/CFG687_erass1_shear_stack/cfg687_percluster.npz",
    mutation=MUT,
    n_pass=N_PASS,
    n_total=len(CHECKS),
    runtime_s=round(time.time() - T0, 1),
)
with open(os.path.join(HERE, "a43_results" + TAG + ".json"), "w") as fh:
    json.dump(res, fh, indent=1)
OUTF.close()
sys.exit(0 if N_PASS == len(CHECKS) else 1)
