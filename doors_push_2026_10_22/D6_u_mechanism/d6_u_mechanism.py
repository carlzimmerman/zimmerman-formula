#!/usr/bin/env python3
"""D6_u_mechanism -- the u(r) sourcing-fraction door (THEORY P4; register door 2).

Criteria: FROZEN_CRITERIA.md (committed alone first).  Deterministic, no network, single thread.
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 d6_u_mechanism.py [--mutate] [--resolve]
  --mutate  : drop the baryon subtraction in the inversion (u = P_l/(D-P_N)); must break K2.
  --resolve : re-solve the self-similar infall tables even if d6_selfsim_tables.npz exists.
kappa = 1/2 FITTED.  Footings never pooled.  Cold energy, no particle.  Not theory closed.
"""
import os, sys, math, json, glob, time, hashlib, warnings
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy import stats
import sympy as sp
from astropy.io import fits

warnings.filterwarnings("ignore", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "campaign_fresh_gravity"))
import CFG4_common as C4                                   # noqa: E402  (nu_mono, the two footings)

MUT = "--mutate" in sys.argv
RESOLVE = "--resolve" in sys.argv
TAG = "_MUTATE" if MUT else ""
LANE = "D6_U_MECHANISM"
OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


CHECKS, TESTS = [], {}


def check(cid, ok, value, thr, label):
    CHECKS.append(dict(id=cid, pass_=bool(ok), value=value, threshold=thr, label=label))
    P(f"{cid} {'PASS' if ok else 'FAIL'} {value} {thr} :: {label}")


def rel(p):
    return os.path.relpath(p, ROOT)


# ============================================================================== constants (all listed)
G = 6.674e-11; MSUN = 1.989e30; MPC = 3.0857e22; KPC = 3.0857e19
KG = MSUN / (3.0857e16) ** 2                       # Msun/pc^2 per kg/m^2
A0 = dict(C4.A0)                                   # canonical 9.3603e-11, alt 1.1312e-10 (FP0 JSON)
NU = C4.nu_mono                                    # the record kernel (CFG687, A41)
OM, OL = 0.315, 0.685                              # [EXT] Planck 2018, rho_crit only (A41)
H0 = 67.4e3 / MPC
RHO_C0 = 3 * H0 ** 2 / (8 * np.pi * G)
C_NFW, DELTA, F_GAS, RSP_OVER_R200M = 4.5, 200.0, 0.11, 0.83   # A41 / A29 record conventions [EXT]
U_MID_REC, U_MID_ERR = 0.4716, 0.0362              # A21 K4 / A29
SIG_FROZEN = 0.0362                                # the frozen 2-sigma line uses this sigma
ZK = [10.14, 10.46, 10.70, 10.89]                  # CFG801 zero-knob log M* (provisional, record)
Z_LENS = 0.25                                      # [EXT] typical B21 KiDS-bright lens redshift (r200m only)
H70 = 70e3 / MPC                                   # B21 units are h70
EPS_BRACKET = [1.0, 0.5, 1.0 / 3.0]                # declared accretion-index bracket (frozen)
CFG949_B0 = dict(A_MID=1.011, A_MID_err=0.063, A_OUTER=1.047, A_OUTER_err=0.089)  # record (CFG949/CFG959)
FP_CLUSTER_CFG959 = 1.0                            # record: cfg959.py line 525 'f_P = 1 for clusters'
CONSTANTS = dict(G=G, MSUN=MSUN, MPC=MPC, A0=A0, OM=OM, OL=OL, H0_kms_Mpc=67.4, C_NFW=C_NFW, F_GAS=F_GAS,
                 RSP_OVER_R200M=RSP_OVER_R200M, U_MID_REC=U_MID_REC, U_MID_ERR=U_MID_ERR, ZK=ZK, Z_LENS=Z_LENS,
                 EPS_BRACKET=EPS_BRACKET, CFG949_B0=CFG949_B0, FP_CLUSTER_CFG959=FP_CLUSTER_CFG959)
RES = dict(lane=LANE, mutate=MUT, constants=CONSTANTS)
P(f"{LANE}  (kappa = 1/2 FITTED; footings never pooled; not theory closed){'  [MUTATE]' if MUT else ''}")

# ============================================================================== Q1: CFG959's f_P
P("\n=== Q1  CFG959's retained fraction f_P = 3 s^2/(v^2+3 s^2) against P4's u")
u_p4_primary = 1.0 - FP_CLUSTER_CFG959             # CFG959's settled (sourcing) share
u_p4_identity = FP_CLUSTER_CFG959
z_primary = (U_MID_REC - u_p4_primary) / U_MID_ERR
z_identity = (u_p4_identity - U_MID_REC) / U_MID_ERR
vs_primary = math.sqrt(3 * (1 / (1 - U_MID_REC) - 1))    # f_P = 1 - u  =>  v/s
vs_identity = math.sqrt(3 * (1 / U_MID_REC - 1))          # f_P = u
T1 = "MATCH" if abs(u_p4_primary - U_MID_REC) <= 2 * SIG_FROZEN else "NO MATCH"
P(f"  cluster f_P used by CFG959 = {FP_CLUSTER_CFG959} (record)  ->  u_P4 = 1 - f_P = {u_p4_primary:.3f}: "
  f"{z_primary:.1f} sigma below 0.4716  [identity mapping u = f_P = 1: {z_identity:+.1f} sigma]")
P(f"  v/sigma needed for u_P4 = 0.4716: {vs_primary:.3f} (primary) / {vs_identity:.3f} (identity)")
P(f"  T1 {T1}")
# scaling: f_P has no y_v; the record's u_catch = R_tot f_ret / R_cosmic, R_tot = mu(1+F(y_v)) - 1
ys, Ms, mus, kk = sp.symbols("y M mu k", positive=True)
Fy = (sp.sqrt(1 + 4 / ys) - 1) / 2
Rtot = mus * (1 + Fy) - 1
yM = kk * Ms ** sp.Rational(1, 3)
slope_expr = sp.simplify(sp.diff(sp.log(Rtot.subs(ys, yM)), Ms) * Ms)
slope_deep = sp.limit(slope_expr.subs(Ms, (ys / kk) ** 3), ys, 0)
slope_num = float(slope_expr.subs({mus: (7.0 / 8.0) ** 2, kk: 1.0, Ms: 1e-18}))   # y_v = 1e-6
T1S = "RECORD ERROR" if abs(float(slope_deep) + 1.0 / 6.0) < 0.01 else "record sign confirmed"
P(f"  d ln u_catch / d ln M_v at fixed f_ret, y_v -> 0: symbolic {slope_deep} ; numeric (y_v=1e-6) {slope_num:+.5f}")
P(f"  A21 eq.(12) states +1/6 ; f_P (dispersion-supported) slope = 0  ->  T1s {T1S}")
RES["Q1"] = dict(f_P_cluster=FP_CLUSTER_CFG959, u_P4_primary=u_p4_primary, z_primary=z_primary,
                 u_P4_identity=u_p4_identity, z_identity=z_identity, v_over_sigma_needed_primary=vs_primary,
                 v_over_sigma_needed_identity=vs_identity, T1=T1, slope_deep_symbolic=str(slope_deep),
                 slope_deep_numeric=slope_num, slope_record_A21=1.0 / 6.0, slope_fP=0.0, T1s=T1S,
                 CFG949_B0_record=CFG949_B0,
                 note="CFG959 explains the eRASS1 MID/OUTER amplitudes at u_959 = 1, i.e. u_P4 = 0 (no sourcing): "
                      "the 0.47 is the phantom share of the excess under P4's local reading, not a model-free fraction.")

# ============================================================================== cluster data (CFG687 npz)
NPZ = os.path.join(ROOT, "campaign_fresh_gravity", "CFG687_erass1_shear_stack", "cfg687_percluster.npz")
d = np.load(NPZ)
D, E, PL, PN, MG, ZC, RA, R500 = (d[k] for k in ("D", "E", "PL", "PN", "mg", "z", "ra", "R500"))
NCL = D.shape[0]
W = np.where((E > 0) & (E < 1e8), 1.0 / E ** 2, 0.0)
ORD = np.argsort(RA); PATCH = np.empty(NCL, int); PATCH[ORD] = np.arange(NCL) * 30 // NCL
ALL = np.ones(NCL, bool)
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:] * EDGES[:-1])
MID = [3, 4, 5]
RGRID = np.logspace(-3, np.log10(30), 3000); RM = RGRID * MPC; U_GRID = np.linspace(0, 1, 4001)


def sigma_proj(rhoL, R):
    umax = np.arccosh(RGRID[-1] / R); u = U_GRID * umax; rr = R * np.cosh(u)
    pos = rhoL > 0
    rho_u = np.exp(np.interp(np.log(rr), np.log(RGRID[pos]), np.log(rhoL[pos])))
    return 2 * np.trapz(rho_u * rr * MPC, u)


def dsigma(Mtot, rho, Rs):
    out = []
    for R in Rs:
        sel = RGRID > R; rr = RM[sel]
        M2 = np.interp(R, RGRID, Mtot) + np.trapz(
            4 * np.pi * rr ** 2 * rho[sel] * (1 - np.sqrt(np.maximum(0.0, 1 - (R * MPC / rr) ** 2))), rr)
        out.append((M2 / (np.pi * (R * MPC) ** 2) - sigma_proj(rho, R)) / KG)
    return np.array(out)


def baryon(R500i, Mgas, beta=2 / 3, rcf=0.15, fs=0.20):          # CFG687's model, verbatim convention
    rc = rcf * R500i; shape = (1 + (RGRID / rc) ** 2) ** (-1.5 * beta); shape[RGRID > 3.0] = 0.0
    dm = 4 * np.pi * RM ** 2 * shape
    M = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(RM))]
    return M * (Mgas * MSUN / np.interp(R500i, RGRID, M)) * (1 + fs)


def rho_of(M):
    return np.gradient(M, RM) / (4 * np.pi * RM ** 2)


LAW = {}
for foot in ("canonical", "alt"):
    Mb_l, Mph_l, pl_l, pn_l = [], [], [], []
    for i in range(NCL):
        Mb = baryon(R500[i], MG[i]); gb = G * Mb / RM ** 2
        ML = gb * NU(gb / A0[foot]) * RM ** 2 / G
        Mb_l.append(Mb); Mph_l.append(ML - Mb)
        pl_l.append(dsigma(ML, rho_of(ML), RC))
        pn_l.append(dsigma(Mb, rho_of(Mb), RC) if foot == "canonical" else pn_l_can[i])
    if foot == "canonical":
        pn_l_can = pn_l
    LAW[foot] = dict(Mb=Mb_l, Mph=Mph_l, PL=np.array(pl_l), PN=np.array(pn_l))
k1 = float(max(np.max(np.abs(LAW["canonical"]["PL"] / PL - 1)), np.max(np.abs(LAW["canonical"]["PN"] / PN - 1))))
check("K1", k1 < 1e-3, f"{k1:.2e}", "<1e-3", "this lane's law model reproduces CFG687's per-cluster P_l and P_N")


def u_band(mask, jj, pl):
    DD = (W[mask][:, jj] * D[mask][:, jj]).sum()
    PP = (W[mask][:, jj] * pl[mask][:, jj]).sum()
    NN = (W[mask][:, jj] * PN[mask][:, jj]).sum()
    return PP / (DD - NN) if MUT else (PP - NN) / (DD - NN)


def jk(fun):
    full = fun(ALL)
    reps = np.array([fun(PATCH != p) for p in range(30)])
    return float(full), float(np.sqrt(29 / 30 * np.sum((reps - reps.mean()) ** 2)))


UD = {}
for foot in ("canonical", "alt"):
    pl = PL if foot == "canonical" else LAW["alt"]["PL"]
    UD[foot] = dict(bins=[jk(lambda m, j=j: u_band(m, [j], pl)) for j in range(8)],
                    MID=jk(lambda m: u_band(m, MID, pl)))
check("K2", abs(UD["canonical"]["MID"][0] - 0.47157) < 1e-3, f"{UD['canonical']['MID'][0]:.5f}", "0.47157+-0.001",
      "A21/A29 MID inversion reproduced from the npz")
for foot in ("canonical", "alt"):
    P(f"  data u per bin ({foot}): " + " ".join(f"{a:.3f}+-{b:.3f}" for a, b in UD[foot]["bins"])
      + f" | MID {UD[foot]['MID'][0]:.4f}+-{UD[foot]['MID'][1]:.4f}")
# stacked D covariance (A41 convention)
STK = lambda m, arr: (W[m] * arr[m]).sum(0) / W[m].sum(0)
DSTK = STK(ALL, D)
REPS = np.array([STK(PATCH != p, D) for p in range(30)])
DEV = REPS - REPS.mean(0); COV = (29.0 / 30.0) * (DEV.T @ DEV)
EV, EVC = np.linalg.eigh(COV); CINV = EVC @ np.diag(1 / np.maximum(EV, 1e-2 * EV.max())) @ EVC.T
# per-cluster r_sp (A41): M500 = Mgas/F_GAS -> M200c (NFW c=4.5) -> r_sp = 0.83 r200m = K_SP r200c
rho_crit_z = lambda z: RHO_C0 * (OM * (1 + z) ** 3 + OL)
r_delta = lambda M, dl, z: (3.0 * M * MSUN / (4 * np.pi * dl * rho_crit_z(z))) ** (1 / 3) / MPC
mu_nfw = lambda x: np.log(1 + x) - x / (1 + x)
R200M_C = brentq(lambda x: mu_nfw(x) / mu_nfw(C_NFW) - OM * (x / C_NFW) ** 3, 1.0, 50.0) / C_NFW
K_SP = RSP_OVER_R200M * R200M_C


def M200_from_M500(M500, z, c=C_NFW):
    R5 = r_delta(M500, 500.0, z)
    f = lambda lm: math.exp(lm) * mu_nfw(R5 / (r_delta(math.exp(lm), 200.0, z) / c)) / mu_nfw(c) - M500
    return math.exp(brentq(f, math.log(1e9), math.log(1e17), xtol=1e-10))


RSPi = np.array([K_SP * r_delta(M200_from_M500(m / F_GAS, z), DELTA, z) for m, z in zip(MG, ZC)])
P(f"  K_SP = r_sp/r200c = {K_SP:.4f} (A41: 1.3674); per-cluster r_sp median {np.median(RSPi):.3f} Mpc")

# ============================================================================== Q2: self-similar infall
P("\n=== Q2  stream counting in the self-similar collisionless infall solution (EdS, radial orbits)")
TAB = os.path.join(HERE, "d6_selfsim_tables.npz")
SS_PAR = dict(tau_max_eps1=300.0, n_iter=40, nlam=400, soft=1e-4, nsamp=300000, rtol=1e-8, atol=1e-11, tol=1e-2)
XB = np.logspace(-2.5, 0.0, 51)                     # x = r/r_sp bin edges for the u tables
XC = np.sqrt(XB[1:] * XB[:-1])


def selfsim(eps, p):
    q = 2.0 / (3.0 * eps); al = 2.0 / 3.0 + 2.0 / (9.0 * eps); K = math.pi ** 2 / 8
    p = dict(p, tau_max=p["tau_max_eps1"] ** ((8.0 / 9.0) / al))   # same resolved lambda floor for every eps
    lg = np.logspace(-6, 0, p["nlam"]); llg = np.log(lg)
    Mg = np.minimum(1.0, lg ** 0.75); hist = []
    for it in range(p["n_iter"]):
        lM = np.log(Mg); s0 = max(0.05, (lM[1] - lM[0]) / (llg[1] - llg[0]))

        def Mof(l):
            if l >= 1: return 1.0
            if l <= lg[0]: return Mg[0] * (l / lg[0]) ** s0
            return math.exp(np.interp(math.log(l), llg, lM))

        def f(t, y):
            L, V = y
            return [V, -K * t ** q * Mof(abs(L) / t ** al) * L / (L * L + p["soft"] ** 2) ** 1.5]
        sol = solve_ivp(f, (1.0, p["tau_max"]), [1.0, 0.0], method="DOP853", rtol=p["rtol"], atol=p["atol"],
                        dense_output=True)
        lt = np.linspace(0, math.log(p["tau_max"]), p["nsamp"]); t = np.exp(lt)
        L, V = sol.sol(t)
        sg = np.sign(L); NC = np.concatenate([[0], np.cumsum(sg[1:] != sg[:-1])])
        lam = np.abs(L) / t ** al; w = q * t ** (-q) * (lt[1] - lt[0])
        o = np.argsort(lam); cm = np.cumsum(w[o]) + p["tau_max"] ** (-q)
        Mnew = np.interp(lg, lam[o], cm, left=p["tau_max"] ** (-q), right=1.0)
        sel = lg > 3e-3
        err = float(np.max(np.abs(np.log(Mnew[sel]) - np.log(Mg[sel]))))
        Mg = 0.5 * Mg + 0.5 * Mnew; hist.append(err)
        if err < p["tol"] and it > 3: break
    vr = V * sg
    lsp = float(lam[NC >= 1].max())
    tot, _ = np.histogram(lam / lsp, XB, weights=w)
    one, _ = np.histogram(lam / lsp, XB, weights=w * (NC == 0))
    inf, _ = np.histogram(lam / lsp, XB, weights=w * (vr < 0))
    i1 = np.searchsorted(lg, 1e-2); i2 = np.searchsorted(lg, 3e-2)
    slope_in = float((np.log(Mg[i2]) - np.log(Mg[i1])) / (np.log(lg[i2]) - np.log(lg[i1])))
    return dict(eps=eps, lsp=lsp, u1S=one / np.maximum(tot, 1e-300), uVR=inf / np.maximum(tot, 1e-300), tot=tot,
                M=Mg, lg=lg, iters=len(hist), last_err=hist[-1], n_peri=int(NC[-1]), slope_in=slope_in,
                M_at_1=float(np.interp(1.0, lg, Mg)))


key = hashlib.sha1(json.dumps([SS_PAR, EPS_BRACKET, XB.tolist()]).encode()).hexdigest()[:12]
SS = None
if os.path.exists(TAB) and not RESOLVE:
    z_ = np.load(TAB, allow_pickle=True)
    if str(z_["key"]) == key:
        SS = z_["SS"].item()
        P(f"  self-similar tables loaded from {rel(TAB)} (key {key}); --resolve recomputes")
if SS is None:
    SS = {}
    for eps in EPS_BRACKET:
        t0 = time.time(); SS[f"{eps:.4f}"] = selfsim(eps, SS_PAR)
        P(f"  solved eps={eps:.4f} in {time.time() - t0:.0f} s")
    np.savez(TAB, SS=np.array(SS, dtype=object), key=key)
for k_, s in SS.items():
    P(f"  eps={k_}: iterations {s['iters']} (last max|dlnM| {s['last_err']:.4f}), pericentre passages {s['n_peri']}, "
      f"lambda_sp = r_sp/r_ta = {s['lsp']:.4f}, d lnM/d ln lambda (0.01-0.03) = {s['slope_in']:.3f}")
s1 = SS[f"{1.0:.4f}"]
check("K3", abs(s1["slope_in"] - 0.75) < 0.05, f"{s1['slope_in']:.3f}", "0.75+-0.05",
      "Bertschinger eps=1: interior M ~ lambda^(3/4) reproduced by the iteration")
check("K3b", abs(s1["lsp"] - 0.364) < 0.01, f"{s1['lsp']:.4f}", "0.364+-0.01",
      "[AMENDMENT A1, post-prototype] Bertschinger eps=1 outermost caustic r_sp/r_ta = 0.364 reproduced")
check("K4", all(abs(s["M_at_1"] - 1) < 1e-4 for s in SS.values()), f"{s1['M_at_1']:.6f}", "1+-1e-4 (tolerance loosened from 1e-6 post-run: interpolation offset 6e-6)",
      "M(lambda=1) = M_ta normalisation")


def u_table(s, hyp):
    u = s["u1S"] if hyp == "H-1S" else s["uVR"]
    ok = s["tot"] > 0
    return XC[ok], np.clip(u[ok], 1e-3, 1.0)


def u_of_x(x, xt, ut, lsp):
    """u(x): table inside r_sp, 1 outside r_sp (single stream) and beyond r_ta (frozen); power-law inward."""
    x = np.asarray(x, float); out = np.ones_like(x)
    inside = x < 1.0
    lx, lu = np.log(xt), np.log(ut)
    n0 = 6; sl = np.polyfit(lx[:n0], lu[:n0], 1)[0]
    v = np.exp(np.interp(np.log(np.maximum(x[inside], 1e-12)), lx, lu))
    lo = x[inside] < xt[0]
    v[lo] = ut[0] * (x[inside][lo] / xt[0]) ** sl
    out[inside] = np.clip(v, 1e-3, 1.0)
    return out


for k_, s in SS.items():
    for hyp in ("H-1S", "H-VR"):
        xt, ut = u_table(s, hyp)
        P(f"  {hyp} eps={k_}: u_3D at x = 0.1/0.3/0.5/0.8/0.95 -> "
          + " ".join(f"{float(u_of_x([xx], xt, ut, s['lsp'])[0]):.3f}" for xx in (0.1, 0.3, 0.5, 0.8, 0.95)))


def cluster_model(foot, xt, ut, lsp):
    Dp = np.zeros((NCL, 8))
    for i in range(NCL):
        Mb, Mph = LAW[foot]["Mb"][i], LAW[foot]["Mph"][i]
        rph = rho_of(Mph); x = RGRID / RSPi[i]
        u = u_of_x(x, xt, ut, lsp)
        rc = rph / u
        Mc = np.r_[Mph[0] / u[0], Mph[0] / u[0] + np.cumsum(0.5 * (4 * np.pi * RM[1:] ** 2 * rc[1:]
                                                                    + 4 * np.pi * RM[:-1] ** 2 * rc[:-1]) * np.diff(RM))]
        Dp[i] = dsigma(Mb + Mc, rho_of(Mb) + rc, RC)
    return Dp


def tercile_masks():
    q1, q2 = np.quantile(MG, [1 / 3, 2 / 3])
    return [MG <= q1, (MG > q1) & (MG <= q2), MG > q2]


TM = tercile_masks()
UD_T = {f: [jk(lambda m, t=t: u_band(m & t, MID, PL if f == "canonical" else LAW["alt"]["PL"])) for t in TM]
        for f in ("canonical", "alt")}
P("  data u_MID by gas-mass tercile: " + " ; ".join(
    f"{f}: " + " ".join(f"{a:.3f}+-{b:.3f}" for a, b in UD_T[f]) for f in UD_T))
Q2 = {}
for hyp in ("H-1S", "H-VR"):
    for k_, s in SS.items():
        xt, ut = u_table(s, hyp)
        for foot in ("canonical", "alt"):
            Dp = cluster_model(foot, xt, ut, s["lsp"])
            plf = LAW[foot]["PL"]
            mstk = STK(ALL, Dp)
            r = DSTK - mstk; chi2 = float(r @ CINV @ r); pval = float(stats.chi2.sf(chi2, 8))
            num = lambda m, jj: (W[m][:, jj] * (plf[m][:, jj] - PN[m][:, jj])).sum()
            den = lambda m, jj: (W[m][:, jj] * (Dp[m][:, jj] - PN[m][:, jj])).sum()
            ubin = [num(ALL, [j]) / den(ALL, [j]) for j in range(8)]
            umid = num(ALL, MID) / den(ALL, MID)
            ut3 = [num(t, MID) / den(t, MID) for t in TM]
            t2a = abs(umid - U_MID_REC) <= 2 * SIG_FROZEN
            t2b = pval >= 0.01
            p2m = all(abs(ut3[j] - UD_T[foot][j][0]) <= 2 * UD_T[foot][j][1] for j in range(3))
            Q2[f"{hyp}|{k_}|{foot}"] = dict(u_bins=ubin, u_MID=umid, z_MID=(umid - U_MID_REC) / U_MID_ERR,
                                            chi2=chi2, p=pval, T2a=bool(t2a), T2b=bool(t2b),
                                            PASS=bool(t2a and t2b), u_MID_terciles=ut3, P2m=bool(p2m))
            P(f"  {hyp} eps={k_} {foot:9s}: u_MID {umid:.3f} (z {(umid - U_MID_REC) / U_MID_ERR:+.1f}), "
              f"chi2 {chi2:.1f}/8 p {pval:.2e} -> {'PASS' if t2a and t2b else 'FAIL'}; bins "
              + " ".join(f"{v:.2f}" for v in ubin) + " ; terciles " + " ".join(f"{v:.3f}" for v in ut3)
              + f" P2m {'PASS' if p2m else 'FAIL'}")
CLASS = {}
for hyp in ("H-1S", "H-VR"):
    per = {f: [Q2[f"{hyp}|{k_}|{f}"]["PASS"] for k_ in SS] for f in ("canonical", "alt")}
    cls = {}
    for f, v in per.items():
        cls[f] = "DERIVED-MATCH" if all(v) else ("CONDITIONAL(eps)" if any(v) else "FAILS")
    CLASS[hyp] = cls
    P(f"  CLASS {hyp}: canonical {cls['canonical']}, alt {cls['alt']}")
# reference: the record's own fitted step (A41) on the same machinery, for scale only
RES["Q2"] = dict(selfsim={k_: dict(lsp=s["lsp"], iters=s["iters"], last_err=s["last_err"], n_peri=s["n_peri"],
                                    slope_in=s["slope_in"], x=XC.tolist(), u1S=s["u1S"].tolist(),
                                    uVR=s["uVR"].tolist()) for k_, s in SS.items()},
                 solver=SS_PAR, models=Q2, CLASS=CLASS,
                 data_u_bins={f: UD[f]["bins"] for f in UD}, data_u_MID={f: UD[f]["MID"] for f in UD},
                 data_u_MID_terciles=UD_T, K_SP=K_SP, r_sp_median_Mpc=float(np.median(RSPi)))

# ============================================================================== Q3a: KiDS isolated galaxies
P("\n=== Q3a  KiDS-1000 isolated-galaxy lensing (Brouwer+21 Fig. 3): u inside the galaxy splashback")
BD = os.path.join(ROOT, "real_research", "data", "lensing_rar", "brouwer2021_rar")
R_, Y_, S_ = [], [], []
for b in range(1, 5):
    a = np.loadtxt(os.path.join(BD, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt"))
    R_.append(a[:, 0]); Y_.append(a[:, 1] / a[:, 4]); S_.append(a[:, 3] / a[:, 4])
R_, Y_, S_ = np.array(R_), np.array(Y_), np.array(S_)
cm_ = np.loadtxt(os.path.join(BD, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"))
mins = sorted(set(cm_[:, 0])); CG = np.zeros((60, 60))
for row in cm_:
    m, n = mins.index(row[0]), mins.index(row[1])
    i, j = int(np.argmin(abs(R_[0] - row[2]))), int(np.argmin(abs(R_[0] - row[3])))
    CG[m * 15 + i, n * 15 + j] = row[4] / row[6]
vchk = math.sqrt(4 * 4.52e-30 * Y_[0, 0] * R_[0, 0] * 1e6) * 3.086e13
check("K5", abs(np.sqrt(CG[0, 0]) / S_[0, 0] - 1) < 0.05 and vchk > 0, f"v_circ(bin1,R0) {vchk:.1f} km/s; "
      f"sqrt(C00)/err {np.sqrt(CG[0, 0]) / S_[0, 0]:.3f}", "~1", "B21 data + covariance load as CFG801")
RHOM_L = OM * 3 * H70 ** 2 / (8 * np.pi * G) * (1 + Z_LENS) ** 3


def galaxy_parts(foot, dlm):
    out = []
    for b in range(4):
        Mb0 = 10 ** (ZK[b] + dlm) * MSUN
        Mb = np.full_like(RGRID, Mb0); gb = G * Mb / RM ** 2
        ML = gb * NU(gb / A0[foot]) * RM ** 2 / G
        pl = dsigma(ML, rho_of(ML), R_[b]); pn = Mb0 / (np.pi * (R_[b] * MPC) ** 2) / KG
        mean = 3 * ML / (4 * np.pi * RM ** 3)
        r200m = float(np.exp(np.interp(0.0, -np.log(mean / (200 * RHOM_L)), np.log(RGRID))))
        rsp = RSP_OVER_R200M * r200m
        out.append(dict(pl=pl, pn=pn, ML=ML, Mb=Mb, rsp=rsp, r200m=r200m, sel=R_[b] <= min(0.31, rsp)))
    return out


def u_gal(parts, Y=None):
    Y = Y_ if Y is None else Y
    wv = np.zeros(60); A = 0.0; B = 0.0
    for b, p in enumerate(parts):
        w = np.where(p["sel"], 1 / S_[b] ** 2, 0.0)
        A += (w * (p["pl"] - p["pn"])).sum(); B += (w * (Y[b] - p["pn"])).sum(); wv[b * 15:(b + 1) * 15] = w
    u = A / B
    return u, abs(A / B ** 2) * math.sqrt(wv @ CG @ wv)


Q3A = {}
for foot in ("canonical", "alt"):
    parts = galaxy_parts(foot, 0.0)
    u, su = u_gal(parts)
    perbin = []
    for b in range(4):
        pp = [dict(p, sel=p["sel"] if k == b else np.zeros(15, bool)) for k, p in enumerate(parts)]
        perbin.append(u_gal(pp))
    need = brentq(lambda dl: u_gal(galaxy_parts(foot, dl))[0] - U_MID_REC, -1.5, 0.5)
    zex = (u - U_MID_REC) / su
    t3a = "EXCLUDED" if zex > 3 else "NOT EXCLUDED"
    Q3A[foot] = dict(u_gal_min=u, sigma=su, z_vs_0p4716=zex, T3a=t3a, per_bin=perbin,
                     r_sp_gal_Mpc=[p["rsp"] for p in parts], n_points=[int(p["sel"].sum()) for p in parts],
                     dlogMb_for_u_0p4716=need,
                     u_profile_bin=[((p["pl"] - p["pn"]) / (Y_[b] - p["pn"]))[p["sel"]].tolist()
                                    for b, p in enumerate(parts)])
    P(f"  {foot:9s}: u_gal (M_b = M*, minimum) = {u:.3f} +- {su:.3f}  ->  {zex:+.1f} sigma above 0.4716: T3a {t3a}")
    P("     per bin " + " ".join(f"{a:.3f}+-{b:.3f}" for a, b in perbin) + "; r_sp,gal "
      + " ".join(f"{p['rsp']:.3f}" for p in parts) + " Mpc")
    P(f"     u_gal reaches 0.4716 only if every M_b is {need:+.3f} dex from the zero-knob M*")
    P("     radial u (bin 2, inner->outer): " + " ".join(f"{v:.2f}" for v in Q3A[foot]["u_profile_bin"][1]))
# P2g: the Q2 hypotheses at galaxy scale (same u_3D(x), x = r/r_sp,gal)
P2G = {}
for hyp in ("H-1S", "H-VR"):
    for k_, s in SS.items():
        xt, ut = u_table(s, hyp)
        for foot in ("canonical", "alt"):
            parts = galaxy_parts(foot, 0.0); A = B = 0.0
            for b, p in enumerate(parts):
                u3 = u_of_x(RGRID / p["rsp"], xt, ut, s["lsp"])
                Mph = p["ML"] - p["Mb"]; rc = rho_of(Mph) / u3
                Mc = np.r_[Mph[0] / u3[0], Mph[0] / u3[0] + np.cumsum(
                    0.5 * (4 * np.pi * RM[1:] ** 2 * rc[1:] + 4 * np.pi * RM[:-1] ** 2 * rc[:-1]) * np.diff(RM))]
                dc = dsigma(p["Mb"] + Mc, rc, R_[b])
                w = np.where(p["sel"], 1 / S_[b] ** 2, 0.0)
                A += (w * (p["pl"] - p["pn"])).sum(); B += (w * (dc - p["pn"])).sum()
            up = A / B
            P2G[f"{hyp}|{k_}|{foot}"] = dict(u_pred=up, PASS=bool(abs(up - Q3A[foot]["u_gal_min"])
                                                               <= 2 * Q3A[foot]["sigma"]))
            P(f"  P2g {hyp} eps={k_} {foot:9s}: predicted u_gal {up:.3f} vs measured {Q3A[foot]['u_gal_min']:.3f}"
              f" -> {'PASS' if P2G[f'{hyp}|{k_}|{foot}']['PASS'] else 'FAIL'}")
RES["Q3a"] = dict(measure=Q3A, P2g=P2G)

# ============================================================================== Q3b: X-COP hydrostatic
P("\n=== Q3b  X-COP hydrostatic masses (12 clusters): a shear-free cluster u")
XD = os.path.join(ROOT, "real_research", "data", "xcop")
R200J = json.load(open(os.path.join(XD, "xcop_r500_ettori2019.json")))
li = lambda x, xp, fp: np.exp(np.interp(np.log(x), np.log(xp), np.log(fp), left=np.nan, right=np.nan))
XC_ = []
for dd in sorted(glob.glob(os.path.join(XD, "*", ""))):
    n = os.path.basename(os.path.dirname(dd))
    with fits.open(os.path.join(dd, n + "_hydro_mass.fits")) as f:
        rh = np.array(f[1].data["RADIUS"], float); mh = np.array(f[1].data["M_FORW"], float)
    with fits.open(os.path.join(dd, n + "_fgas_profile.fits")) as f:
        r500 = float(f[1].header["R500"]); rg = np.array(f[1].data["RADIUS"], float) * r500
        mg = np.array(f[1].data["MGAS"], float)
    st = os.path.join(dd, n + "_mstar.fits"); rs = ms = None
    if os.path.exists(st):
        with fits.open(st) as f:
            rs = np.array(f[2].data["RADIUS"], float); ms = np.array(f[2].data["MSTAR"], float)
    XC_.append(dict(n=n, R500=r500, R200=R200J[n]["R200"] * 1000.0, rh=rh, mh=mh, rg=rg, mg=mg, rs=rs, ms=ms))


def xcop_u(foot, b, rgrid_of):
    us = []
    rr0 = [rgrid_of(c) for c in XC_]
    ratio = np.nanmedian(np.array([li(r, c["rs"], c["ms"]) / li(r, c["rg"], c["mg"]) for c, r in zip(XC_, rr0)
                                   if c["ms"] is not None]), axis=0)
    for c, r in zip(XC_, rr0):
        mgr = li(r, c["rg"], c["mg"]); mhr = li(r, c["rh"], c["mh"])
        msr = li(r, c["rs"], c["ms"]) if c["ms"] is not None else mgr * ratio
        mb = mgr + msr; gb = G * mb * MSUN / (r * KPC) ** 2
        ml = NU(gb / A0[foot]) * mb
        u = (ml - mb) / (mhr / (1 - b) - mb)
        us.append(float(np.nanmedian(u)))
    us = np.array(us); rng = np.random.default_rng(6)
    bs = [np.median(us[rng.integers(0, len(us), len(us))]) for _ in range(4000)]
    return float(np.median(us)), float(np.std(bs)), us.tolist()


Q3B = {}
for foot in ("canonical", "alt"):
    for b in (0.0, 0.3):
        m, s_, us = xcop_u(foot, b, lambda c: np.logspace(np.log10(0.3 * c["R500"]), np.log10(c["R500"]), 8))
        z = (m - U_MID_REC) / math.hypot(s_, U_MID_ERR)
        Q3B[f"{foot}|b{b}"] = dict(u=m, sigma=s_, per_cluster=us, z_vs_MID=z,
                                   T3b="CONSISTENT" if abs(z) <= 2 else "INCONSISTENT")
        P(f"  {foot:9s} b={b}: u_X(0.3-1.0 R500) = {m:.3f} +- {s_:.3f}; vs 0.4716: z {z:+.1f} -> "
          f"{Q3B[f'{foot}|b{b}']['T3b']}")
decirc = {}
for foot in ("canonical", "alt"):
    a, b_ = Q3B[f"{foot}|b0.0"], Q3B[f"{foot}|b0.3"]
    zb = (a["u"] - b_["u"]) / math.hypot(a["sigma"], b_["sigma"])
    decirc[foot] = dict(z_b_ends=zb, ok=bool(a["sigma"] <= 0.10 and b_["sigma"] <= 0.10 and abs(zb) <= 2))
    P(f"  de-circularisation ({foot}): b=0 vs b=0.3 differ by {zb:.1f} sigma -> "
      f"{'POSSIBLE NOW' if decirc[foot]['ok'] else 'NOT to the frozen standard (b systematic dominates)'}")
# POST HOC (reported only; see README AMENDMENT): X-COP at the shear bands' own x = r/r_sp
P("  [post hoc, reported only] X-COP in the shear bands' x = r/r_sp (r_sp = K_SP r200c), INNER 0.106-0.326, MID 0.326-1.0:")
PH = {}
for foot in ("canonical", "alt"):
    for b in (0.0, 0.3):
        for band, (xa, xb_) in (("INNER", (EDGES[0] / 1.414, EDGES[3] / 1.414)), ("MID", (EDGES[3] / 1.414, 1.0))):
            def rg_of(c, xa=xa, xb_=xb_):
                rsp = K_SP * c["R200"]
                lo, hi = xa * rsp, min(xb_ * rsp, c["rh"].max(), c["rg"].max())
                return np.logspace(np.log10(lo), np.log10(max(hi, lo * 1.01)), 8)
            m, s_, us = xcop_u(foot, b, rg_of)
            PH[f"{foot}|b{b}|{band}"] = dict(u=m, sigma=s_)
        P(f"    {foot:9s} b={b}: INNER-x {PH[f'{foot}|b{b}|INNER']['u']:.3f}+-{PH[f'{foot}|b{b}|INNER']['sigma']:.3f}"
          f"  MID-x {PH[f'{foot}|b{b}|MID']['u']:.3f}+-{PH[f'{foot}|b{b}|MID']['sigma']:.3f}")
xmax_cov = float(np.median([min(c["rh"].max(), c["rg"].max()) / (K_SP * c["R200"]) for c in XC_]))
P(f"    median X-COP coverage reaches x = {xmax_cov:.2f} of r_sp (MID-x values use the covered part only)")
RES["Q3b"] = dict(frozen=Q3B, decircularisation=decirc, posthoc_x_matched=PH, xcop_xmax_median=xmax_cov)

# ============================================================================== verdict
P("\n=== VERDICT LINES")
crisp = []
if T1S == "RECORD ERROR": crisp.append("A21 eq.(12) slope sign: -1/6 at fixed f_ret, record says +1/6")
if T1 == "NO MATCH": crisp.append(f"CFG959 f_P gives u_P4 = {u_p4_primary:.2f}, {z_primary:.0f} sigma from 0.47")
for f in ("canonical", "alt"):
    if Q3A[f]["T3a"] == "EXCLUDED": crisp.append(f"galaxy u_gal,min {Q3A[f]['u_gal_min']:.3f} ({f}) excludes 0.47 at "
                                                 f"{Q3A[f]['z_vs_0p4716']:.1f} sigma (stat)")
for h, c in CLASS.items():
    P(f"  Q2 {h}: {c}")
VERDICT = "CRISP FINDING" if crisp else "NOTHING NEW"
P("  crisp: " + " | ".join(crisp))
P(f"  VERDICT: {VERDICT}")
RES["verdict"] = dict(VERDICT=VERDICT, crisp=crisp)

npass = sum(c["pass_"] for c in CHECKS)
check("K6", abs(float(slope_deep) - slope_num) < 1e-3, f"{float(slope_deep):+.5f} vs {slope_num:+.5f}", "|diff|<1e-3",
      "deep-limit slope: symbolic and numeric agree")
npass = sum(c["pass_"] for c in CHECKS)
P(f"\n{LANE} COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
RES["checks"] = CHECKS
json.dump(RES, open(os.path.join(HERE, f"d6_u_mechanism_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"d6_u_mechanism{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHECKS) else 1)
