#!/usr/bin/env python3
"""CFG630: settling energy feeds dark energy (FROZEN_CRITERIA.md, criteria commit 45dd454a6).

Cosmic settling power Q(z; alpha) = a^-3 dU/dt with
  U(t) = rho_c0 Int dlnM f_ta(M,t) s_c(M,t;alpha) eps_W(M)     (settled potential energy released per comoving volume)
  f_ta     excursion-set mass fraction with the turnaround barrier (PS primary, ST bracket)  -- INHERITED (HMF context)
  s_c      CFG557 rate-limited catchment (cfg557_lib, read-only import), floor 0 when nothing is captured (disclosed change)
  eps_W    c_W V_f^2, c_W = CFG542 overdamped dW/(M_cat V_f^2) (MW -> cluster), V_f = (G M_b a0)^(1/4), M_b = census f_ret f_b M_ta
then d(rho_DE c^2)/dt + 3H(1 + w_b) rho_DE c^2 = +Q, w_b = -1, rho_DE(t0) = rho_DE0; a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0).

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg630.py                  -> cfg630.out, cfg630_results.json, cfg630_prediction.png
      CFG630_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg630.py  -> cfg630_MUTATE.out, cfg630_results_MUTATE.json
Inputs (read-only, on disk; nothing downloaded): cfg557_lib (cosmology, EH spectrum, Epoch/mah/edge/fret_of), CFG541 + CFG542 JSON,
CFG549 results JSON (DESI sigmas, context only), CFG424 TA box JSONs in the external-data folder (K6 native check).
kappa = 1/2 FITTED (cancels in the a0 ratio); footings never pooled; cold energy mass required; no particle species; not theory closed.
"""
import os
import sys
import json
import math
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np                                   # noqa: E402
from scipy.interpolate import PchipInterpolator      # noqa: E402
from scipy.integrate import solve_ivp, quad, cumulative_simpson  # noqa: E402
from scipy.optimize import least_squares             # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
sys.path.insert(0, os.path.join(CFG, "CFG557_settling_catchment_derived"))
import cfg557_lib as L                               # noqa: E402
TRAPZ = getattr(np, "trapezoid", None) or np.trapz

MUT = os.environ.get("CFG630_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
T_START = time.time()
OUT = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


# ------------------------------------------------------------------ constants and record inputs
c = 2.99792458e8; Gsi = 6.67430e-11; MPC = 3.0856775814913673e22
h = L.h; Om = L.Om; OL = L.OL; FB = L.FB
H0 = 100 * h * 1e3 / MPC                              # 1/s
RHOCRIT = 3 * H0 ** 2 / (8 * math.pi * Gsi)
RHO_C0 = Om * (1 - FB) * RHOCRIT                      # cold energy, kg/m^3 comoving
RHO_M0 = Om * RHOCRIT
RHO_DE0 = OL * RHOCRIT
FOOTS = {"can": "canonical", "alt": "alt"}

J541 = json.load(open(os.path.join(CFG, "CFG541_cold_energy_equations_precise", "cfg541_results.json")))
J542 = json.load(open(os.path.join(CFG, "CFG542_dissipative_action", "cfg542_results.json")))
J549 = json.load(open(os.path.join(CFG, "CFG549_dark_energy_evolution_prediction", "cfg549_results.json")))
MB_MW = J541["systems"]["MW"]["Mb"]; MB_CL = J541["systems"]["cluster"]["Mb"]          # Msun
CW = {f: (J542["one_d"][f]["MW"]["od_a1.0"]["dW_per_Mcat_Vf2"], J542["one_d"][f]["cluster"]["od_a1.0"]["dW_per_Mcat_Vf2"]) for f in FOOTS}
QDW = {f: [J542["one_d"][f][n][k]["Q_over_dW"] for n in ("MW", "cluster") for k in ("od_a0.5", "od_a1.0", "od_a2.0")] for f in FOOTS}
SIG_W0 = min(J549["desi_sigmas"]["w0"].values()); SIG_WA = min(J549["desi_sigmas"]["wa"].values())
REQ_A0 = J549["R2"]["required_sigma_log10_a0"]
A0_SEP_DEX = 0.007                                     # frozen threshold (CFG549 R2 smallest required per-bin sigma)
A0_FLOOR_DEX = 0.15                                    # CFG571 per-disc systematic floor (context)
A0_UNSEP_DEX = 0.02                                    # CFG571: F-DESI vs F-flat <= 0.02 dex not separable (context)

ALPHA_BRACKET = [0.5, 0.75, 1.0, 1.186]
ALPHAS = [0.0, 1.0] if MUT else ALPHA_BRACKET + [2.0, math.inf]
HMFS = ("PS", "ST"); MMINS = (1e6, 1e8, 1e10)
Z_EP = [0.0, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0]
LMG = np.arange(8.0, 16.0001, 0.25)                   # log10 M_ta [Msun/h] where s_c is solved
LMF = np.linspace(5.0, 16.5, 1151)                    # fine integration grid

R = dict(lane="CFG630", date="2026-10-11", criteria_commit="45dd454a6", mutate=MUT,
         settings="kappa = 1/2 FITTED (cancels in the a0 ratio); footings 9.3603e-11 / 1.1312e-10 never pooled; candidate B; class A "
                  "overdamped sink (CFG542 Pb); w_b = -1 background; cold energy mass required; no particle species; not theory closed",
         inputs=dict(h=h, Omega_m=Om, f_b=FB, rho_c0=RHO_C0, rho_DE0=RHO_DE0, c_W=CW, Q_over_dW_CFG542=QDW,
                     sigma_w0_context=SIG_W0, sigma_wa_context=SIG_WA, alpha_bracket=ALPHA_BRACKET,
                     inherited=["excursion-set turnaround-barrier mass fraction (PS / ST form), Gaussian ICs",
                                "Eisenstein-Hu linear spectrum (sigma8 0.811) and flat matter+Lambda linear growth (the PM's own input)",
                                "spherical-collapse t_reach with a Lambda term and the EPS main-progenitor history (cfg557_lib, PROVISIONAL)",
                                "DESI DR2 Gaussian sigmas (context only, from CFG549's committed JSON)"]),
         checks={}, disclosures=[])
P(f"CFG630 settling energy feeds dark energy {'(MUTATE)' if MUT else ''} -- FROZEN_CRITERIA.md (45dd454a6)")
P("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
P(f"inputs: h {h}, Omega_m {Om:.5f}, f_b {FB:.5f}, rho_c0 {RHO_C0:.4e} kg/m^3, rho_DE0 {RHO_DE0:.4e} kg/m^3")
P(f"CFG542 overdamped c_W = dW/(M_cat V_f^2): can MW {CW['can'][0]:.4f} cluster {CW['can'][1]:.4f}; alt MW {CW['alt'][0]:.4f} "
  f"cluster {CW['alt'][1]:.4f}; Q/dW in [{min(min(v) for v in QDW.values()):.5f}, {max(max(v) for v in QDW.values()):.5f}] (the sink takes all of dW)")


# ------------------------------------------------------------------ background (matter + Lambda, as cfg557_lib), t in 1/H0
def t_of_a(a):
    return 2.0 / (3.0 * math.sqrt(OL)) * np.arcsinh(np.sqrt(OL / Om) * np.asarray(a) ** 1.5)


def a_of_t(t):
    return (Om / OL) ** (1 / 3) * np.sinh(1.5 * math.sqrt(OL) * np.asarray(t)) ** (2 / 3)


def E_of_a(a):
    return np.sqrt(Om / np.asarray(a) ** 3 + OL)


T0 = float(t_of_a(1.0))
R["checks"]["K0_age"] = dict(analytic=T0, cfg557_lib=L.T0, rel=abs(T0 / L.T0 - 1))


# ------------------------------------------------------------------ catchment s_c (CFG557 fixed point; floor 0; alpha = 0 -> t_cap = inf)
def t_cap(Mb, re, foot, alpha):
    if alpha == 0.0:
        return math.inf
    return L.t_cap(Mb, re, foot, alpha)


def s_catch0(E, Mta, Mb, foot, alpha, mah, tol=1e-6, itmax=200):
    """cfg557_lib.s_catch iteration (same update rule, including its X[0] restart when nothing is captured); the only change is the
    READING of the converged state: if the converged iterate is the 'nothing captured' restart, s_c = 0 (CFG557 reports the 0.02 floor).
    alpha = 0 -> t_cap = inf -> nothing is ever captured -> 0 through this path."""
    X, dL = mah
    RL = L.r_lagr(X * Mta)
    sc = 1.0
    for it in range(itmax):
        re = L.edge(Mb, Mta, sc, foot)
        tr = E.t_reach(dL, re / RL) + t_cap(Mb, re, foot, alpha)
        ok = tr <= E.t_obs
        none = False
        if ok.all():
            new = 1.0
        elif not ok.any():
            new = float(X[0]); none = True
        else:
            i = int(np.nonzero(~ok)[0][0])
            if i == 0:
                new = float(X[0]); none = True
            else:
                t1, t2 = tr[i - 1] - E.t_obs, tr[i] - E.t_obs
                new = float(X[i - 1] + (X[i] - X[i - 1]) * (-t1) / (t2 - t1))
        if abs(new - sc) < tol:
            return (0.0 if none else new), True
        sc = new
    return sc, False


EP = {}
SC = {}            # (foot, alpha) -> array [len(Z_EP), len(LMG)]
nconv = 0; nfail = 0; nfloor_diff = 0
t1 = time.time()
for iz, z in enumerate(Z_EP):
    E = L.Epoch(z)
    EP[z] = dict(d_ta=E.d_ta, Dratio=E.Dratio, t_obs=E.t_obs, Delta_ta=E.Delta_ta)
    for il, lm in enumerate(LMG):
        Mta = 10 ** lm
        Mb = L.fret_of(lm) * L.FB * Mta
        mah = E.mah(Mta)
        for f, fl in FOOTS.items():
            for al in ALPHAS:
                key = (f, al)
                if key not in SC:
                    SC[key] = np.zeros((len(Z_EP), len(LMG)))
                s, conv = s_catch0(E, Mta, Mb, fl, al, mah)
                SC[key][iz, il] = s
                nconv += conv; nfail += (not conv)
    P(f"  epoch z = {z:4.2f}: delta_ta {E.d_ta:.4f}, D/D0 {E.Dratio:.4f}, t {E.t_obs * L.GYR_PER_HINV:6.3f} Gyr, Delta_ta {E.Delta_ta:6.3f}  "
      f"[{time.time() - t1:6.1f}s]")
R["checks"]["catchment_fixed_points"] = dict(converged=int(nconv), not_converged=int(nfail))
P(f"  catchment fixed points: {nconv} converged, {nfail} not converged (last iterate used)")


# ------------------------------------------------------------------ eps_W(M) and the mass fraction
def eps_W(lMta, foot):
    Mta = 10 ** lMta
    Mb = np.array([L.fret_of(x) for x in np.atleast_1d(lMta)]) * L.FB * Mta          # Msun/h
    Vf = (L.G * (Mb / h) * L.A0MPC[FOOTS[foot]]) ** 0.25 * 1e3                            # m/s
    x = np.clip((np.log10(Mb / h) - math.log10(MB_MW)) / (math.log10(MB_CL) - math.log10(MB_MW)), 0.0, 1.0)
    cw = CW[foot][0] + (CW[foot][1] - CW[foot][0]) * x
    return cw * Vf ** 2                                                                    # J/kg


A_ST, a_ST, p_ST = 0.3222, 0.707, 0.3


def fnu(nu, hmf):
    if hmf == "PS":
        return math.sqrt(2 / math.pi) * np.exp(-nu * nu / 2)
    return A_ST * math.sqrt(2 * a_ST / math.pi) * (1 + (a_ST * nu * nu) ** (-p_ST)) * np.exp(-a_ST * nu * nu / 2)


nug = np.linspace(1e-8, 15, 300001)
R["checks"]["K1_PS_norm"] = dict(value=float(TRAPZ(fnu(nug, "PS"), nug)))
R["checks"]["K1_PS_norm"]["ok"] = bool(R["checks"]["K1_PS_norm"]["value"] >= 0.999)
R["checks"]["K1_ST_norm_reported"] = float(quad(lambda v: fnu(v, "ST"), 0, 1, limit=200)[0] + quad(lambda v: fnu(v, "ST"), 1, 40, limit=200)[0])
SIG0F = np.sqrt(L.S0(10 ** LMF))
EPSF = {f: eps_W(LMF, f) for f in FOOTS}


def dFdlnM(z, hmf):
    nu = EP[z]["d_ta"] / (SIG0F * EP[z]["Dratio"])
    return fnu(nu, hmf) * np.gradient(nu, LMF * math.log(10))


def U_epochs(foot, alpha, hmf, Mmin, scale=1.0, settled_mult=1.0):
    """U at each epoch [J/m^3 comoving] and settled cold fraction F (of all cold energy)."""
    sc = SC[(foot, alpha)] * settled_mult
    sel = LMF >= math.log10(Mmin)
    U = np.zeros(len(Z_EP)); F = np.zeros(len(Z_EP))
    for iz, z in enumerate(Z_EP):
        scf = np.interp(LMF, LMG, sc[iz])                    # clamped below 8 and above 16
        dF = dFdlnM(z, hmf) * scf
        x = LMF[sel] * math.log(10)
        F[iz] = TRAPZ(dF[sel], x)
        U[iz] = RHO_C0 * TRAPZ((dF * EPSF[foot])[sel], x) * scale
    return U, F


# ------------------------------------------------------------------ history -> Q(t), rho_DE(t), w, CPL, a0
A_EP = 1.0 / (1.0 + np.array(Z_EP)); T_EP = t_of_a(A_EP)
order = np.argsort(T_EP)
TF = np.linspace(T_EP.min(), T0, 200001)
AF = a_of_t(TF); AF[-1] = 1.0
ZF = 1 / AF - 1
HF = E_of_a(AF)                                       # H/H0


def history(U_ep):
    tt = T_EP[order]; uu = np.maximum.accumulate(U_ep[order])          # ratchet (class A one-sided)
    ratchet_bind = float(np.max(uu - U_ep[order]))
    if np.all(uu == 0):
        Ui = lambda t: np.zeros_like(np.asarray(t, float))              # noqa: E731
        dUi = Ui
    else:
        pc = PchipInterpolator(tt, uu)
        Ui = pc; dUi = pc.derivative()
    UF = Ui(TF); dUF = dUi(TF)
    QF = AF ** -3 * dUF                                               # J/m^3 per (1/H0), physical
    # quadrature: rho_DE c^2 (t) = rho_DE0 c^2 - int_t^t0 Q dt   (w_b = -1)
    cum = cumulative_simpson(QF, x=TF, initial=0.0)
    drho_c2 = cum[-1] - cum                                           # J/m^3 removed going back from today
    rhoDE = RHO_DE0 - drho_c2 / c ** 2
    return dict(U=UF, dU=dUF, Q=QF, drho_c2=drho_c2, rhoDE=rhoDE, Ui=Ui, dUi=dUi, ratchet_bind=ratchet_bind)


def ode_check(hst, wb=-1.0):
    """K2 / K3: integrate d(delta rho c^2)/dt = Q - 3H(1+w_b) rho c^2 and the first-law work term; compare with the quadrature."""
    Ui, dUi = hst["Ui"], hst["dUi"]
    t_lo = TF[0]; U_lo = float(Ui(t_lo))

    def rhs(t, y):
        a = float(a_of_t(t)); Hh = float(E_of_a(a))
        Q = a ** -3 * float(dUi(t))
        ddr = Q - 3 * Hh * (1 + wb) * (RHO_DE0 * c ** 2 + y[0])
        dW = 3 * a ** 2 * (a * Hh) * y[0]                             # d/dt int delta(rho c^2) d(a^3)
        return [ddr, dW]
    scale = max(float(hst["drho_c2"][0]), 1e-300)
    tt = TF[::500]
    # integrate knot to knot (U is a C1 PCHIP: Q has kinks at the epochs; stepping across them costs DOP853 its order)
    knots = np.unique(np.concatenate([[t_lo], T_EP[(T_EP > t_lo) & (T_EP < T0)], [T0]]))
    y = np.zeros((2, len(tt))); y0 = [0.0, 0.0]
    for ka, kb in zip(knots[:-1], knots[1:]):
        sol = solve_ivp(rhs, (ka, kb), y0, method="DOP853", rtol=1e-13, atol=1e-16 * scale, dense_output=True)
        m = (tt >= ka) & (tt <= kb)
        if m.any():
            y[:, m] = sol.sol(tt[m])
        y0 = list(sol.y[:, -1])
    dr_ode = y[0] - y[0][-1]                                          # shift so that delta = 0 today
    dr_quad = -(hst["drho_c2"][::500])
    k2 = float(np.max(np.abs(dr_ode - dr_quad)) / scale) if scale > 1e-300 else 0.0
    aa = a_of_t(tt)
    # first law with the constant shift removed analytically: a^3 y0 - W - (U - U_lo) = 0
    res = aa ** 3 * y[0] - y[1] - (Ui(tt) - U_lo)
    U0 = float(Ui(T0))
    k3 = float(np.max(np.abs(res)) / U0) if U0 > 0 else float(np.max(np.abs(res)))
    return k2, k3


def cpl_project(a, rho):
    z = 1 / a - 1
    m = (z >= 0) & (z <= 2.5)
    zz = z[m]; yy = np.log(rho[m] / rho[-1])
    A = np.vstack([3 * np.log(1 + zz), 3 * (np.log(1 + zz) - zz / (1 + zz))]).T
    sol, *_ = np.linalg.lstsq(A, yy, rcond=None)
    return float(sol[0] - 1), float(sol[1])


def hz_project(a, H_over_H0):
    z = 1 / a - 1
    m = (z >= 0) & (z <= 2.5)
    zz = z[m]; yy = np.log(H_over_H0[m])

    def r(p):
        Om_, w0_, wa_ = p
        f = (1 + zz) ** (3 * (1 + w0_ + wa_)) * np.exp(-3 * wa_ * zz / (1 + zz))
        return 0.5 * np.log(Om_ * (1 + zz) ** 3 + (1 - Om_) * f) - yy
    sol = least_squares(r, [Om, -1.0, 0.0], xtol=1e-15, ftol=1e-15, gtol=1e-15)
    return float(sol.x[1]), float(sol.x[2]), float(sol.x[0])


SUB = slice(None, None, 400)
w0L, waL = cpl_project(AF[SUB], np.ones_like(AF[SUB]))
w0H, waH, _ = hz_project(AF[SUB], np.sqrt(Om / AF[SUB] ** 3 + OL))
R["checks"]["K5_cpl_lambda"] = dict(w0=w0L, wa=waL, w0_H=w0H, wa_H=waH,
                                   ok=bool(abs(w0L + 1) < 1e-6 and abs(waL) < 1e-6 and abs(w0H + 1) < 1e-6 and abs(waH) < 1e-6))


def at_z(arr, z):
    return float(np.interp(z, ZF[::-1], arr[::-1]))


ZREP = (0.0, 0.5, 1.0, 2.0, 3.0)


def summarise(hst, U_ep, F_ep, full=True):
    U0 = float(hst["U"][-1])
    rho = hst["rhoDE"]
    delta = 1.0 - rho / RHO_DE0                                        # >= 0 in the past if Q >= 0
    q = hst["Q"] / (3 * HF * rho * c ** 2)                             # = -(1 + w_DE)
    row = dict(U0_J_per_m3=U0, F_settled_z0=float(F_ep[0]), ratchet_bind_J_per_m3=hst["ratchet_bind"],
               Q_W_per_m3={str(z): at_z(hst["Q"], z) * H0 for z in ZREP},
               Q_over_H0_rhoDE0c2={str(z): at_z(hst["Q"], z) / (RHO_DE0 * c ** 2) for z in ZREP},
               drho_over_rho0={str(z): at_z(delta, z) for z in ZREP if z > 0},
               drho_over_rho0_total_from_z8=float(delta[0]),
               onepw_DE={str(z): -at_z(q, z) for z in ZREP},
               max_q_z_le_3=float(np.max(q[ZF <= 3.0])), min_q=float(np.min(q)),
               a0_ratio_minus_1={str(z): math.sqrt(1 - at_z(delta, z)) - 1 for z in (1.0, 2.0, 3.0)},
               dlog10_a0={str(z): 0.5 * math.log1p(-at_z(delta, z)) / math.log(10) for z in (1.0, 2.0, 3.0)},
               ceiling_all_cold_cluster=float(RHO_C0 * max(CW[f][1] * math.sqrt(Gsi * MB_CL * 1.98892e30 * L.A0[FOOTS[f]]) for f in FOOTS)
                                              / (RHO_DE0 * c ** 2)))
    if full:
        w0d, wad = cpl_project(AF[SUB], rho[SUB])
        rho_eff = rho + AF ** -3 * (U0 - hst["U"]) / c ** 2
        w0e, wae = cpl_project(AF[SUB], rho_eff[SUB])
        Hh = np.sqrt((RHO_M0 / AF ** 3 - hst["U"] / c ** 2 / AF ** 3 + rho) / RHOCRIT)
        w0h, wah, omh = hz_project(AF[SUB], (Hh / Hh[-1])[SUB])
        # CFG511 fork: a0 tracking -p_DE = (1 + q) rho_DE instead of rho_DE
        fork = 0.5 * np.log10((1 + q) * rho / ((1 + q[-1]) * rho[-1])) - 0.5 * np.log10(rho / rho[-1])
        row.update(cpl_DE_own=(w0d, wad), cpl_observer=(w0e, wae), cpl_Hfit=(w0h, wah, omh),
                   fork_minus_p_vs_rho_max_dex_z_le_3=float(np.max(np.abs(fork[ZF <= 3.0]))))
    return row


# ------------------------------------------------------------------ main grid of variants
P("\n[S1] settled catchment s_c(M_ta, z; alpha) at z = 0 and 2 (canonical; log M_ta 10 / 12 / 14 / 15)")
for al in ALPHAS:
    s = SC[("can", al)]
    for z in (0.0, 2.0):
        iz = Z_EP.index(z)
        vals = [float(np.interp(lm, LMG, s[iz])) for lm in (10, 12, 14, 15)]
        P(f"  alpha {al:>5}: z {z}: " + " ".join(f"{v:.3f}" for v in vals))
R["s_c_grid"] = {f"{f}|{al}": dict(z=Z_EP, lM_ta=LMG.tolist(), s_c=SC[(f, al)].tolist()) for (f, al) in SC}

RES = {}
P("\n[R1] cosmic settling power and the dark-energy response (PS / ST x M_min x alpha; both footings)")
for f in FOOTS:
    for hmf in HMFS:
        for Mmin in MMINS:
            for al in ALPHAS:
                U_ep, F_ep = U_epochs(f, al, hmf, Mmin)
                hst = history(U_ep)
                key = f"{f}|{hmf}|Mmin{Mmin:.0e}|alpha{al}"
                primary = (hmf == "PS" and Mmin == 1e8)
                row = summarise(hst, U_ep, F_ep, full=primary or MUT)
                row["U_epochs"] = U_ep.tolist(); row["F_epochs"] = F_ep.tolist()
                if primary:
                    k2, k3 = ode_check(hst)
                    row["K2_ode_vs_quad"] = k2; row["K3_first_law"] = k3
                RES[key] = row
                if primary:
                    P(f"  {key:34s} F(0) {row['F_settled_z0']:.3f}  Q(0) {row['Q_W_per_m3']['0.0']:.3e} W/m^3 "
                      f"(= {row['Q_over_H0_rhoDE0c2']['0.0']:.2e} H0 rho_DE0 c^2)  drho/rho0 z1 {row['drho_over_rho0']['1.0']:.3e} "
                      f"z3 {row['drho_over_rho0']['3.0']:.3e}  1+w(0) {row['onepw_DE']['0.0']:+.2e}  dlog a0 z2 {row['dlog10_a0']['2.0']:+.2e}")
R["R1"] = RES

# ------------------------------------------------------------------ MUTATE identities
if MUT:
    P("\n[MU] mutation controls")
    mu1 = {}
    for f in FOOTS:
        for hmf in HMFS:
            for Mmin in MMINS:
                r0 = RES[f"{f}|{hmf}|Mmin{Mmin:.0e}|alpha0.0"]
                U_ep, F_ep = U_epochs(f, 0.0, hmf, Mmin); hst = history(U_ep)
                mu1[f"{f}|{hmf}|{Mmin:.0e}"] = dict(max_abs_drho=float(np.max(np.abs(RHO_DE0 - hst["rhoDE"]))),
                                                     max_abs_a0_ratio_minus_1=float(max(abs(v) for v in r0["a0_ratio_minus_1"].values())),
                                                     max_Q=float(np.max(np.abs(hst["Q"]))))
    ok1 = all(v["max_abs_drho"] == 0.0 and v["max_abs_a0_ratio_minus_1"] == 0.0 and v["max_Q"] == 0.0 for v in mu1.values())
    R["checks"]["MU1_alpha0_flat"] = dict(cells=mu1, ok=bool(ok1))
    P(f"  MU1 alpha = 0: max |drho_DE| = {max(v['max_abs_drho'] for v in mu1.values())}, max |a0 ratio - 1| = "
      f"{max(v['max_abs_a0_ratio_minus_1'] for v in mu1.values())}, max Q = {max(v['max_Q'] for v in mu1.values())} -> {'PASS' if ok1 else 'FAIL'}")
    mu2 = {}
    for f in FOOTS:
        for hmf in HMFS:
            U1, F1 = U_epochs(f, 1.0, hmf, 1e8); U2, F2 = U_epochs(f, 1.0, hmf, 1e8, settled_mult=2.0)
            h1 = history(U1); h2 = history(U2)
            m = np.abs(h1["Q"]) > 0
            rq = float(np.max(np.abs(h2["Q"][m] / h1["Q"][m] - 2)))
            d1 = RHO_DE0 - h1["rhoDE"]; d2 = RHO_DE0 - h2["rhoDE"]; md = np.abs(d1) > 0
            # compare in the drho_c2 variable (rho_DE0 - x loses digits at 1e-7 relative)
            mc = np.abs(h1["drho_c2"]) > 0
            rd = float(np.max(np.abs(h2["drho_c2"][mc] / h1["drho_c2"][mc] - 2)))
            mu2[f"{f}|{hmf}"] = dict(max_rel_dev_Q=rq, max_rel_dev_drho=rd, drho0_ratio=float(h2["drho_c2"][0] / h1["drho_c2"][0]))
    ok2 = all(v["max_rel_dev_Q"] <= 1e-12 and v["max_rel_dev_drho"] <= 1e-12 for v in mu2.values())
    R["checks"]["MU2_settled_x2_linear"] = dict(cells=mu2, ok=bool(ok2))
    P(f"  MU2 settled mass x2: max rel dev of Q/Q - 2 = {max(v['max_rel_dev_Q'] for v in mu2.values()):.2e}, of drho ratio - 2 = "
      f"{max(v['max_rel_dev_drho'] for v in mu2.values()):.2e} -> {'PASS' if ok2 else 'FAIL'}")

# ------------------------------------------------------------------ main-run analysis
if not MUT:
    prim = {f: [RES[f"{f}|PS|Mmin1e+08|alpha{al}"] for al in ALPHA_BRACKET] for f in FOOTS}
    # controls
    R["checks"]["K2_ode_vs_quad"] = dict(max=max(r["K2_ode_vs_quad"] for f in FOOTS for r in prim[f]))
    R["checks"]["K2_ode_vs_quad"]["ok"] = bool(R["checks"]["K2_ode_vs_quad"]["max"] <= 1e-9)
    R["checks"]["K3_first_law"] = dict(max=max(r["K3_first_law"] for f in FOOTS for r in prim[f]))
    R["checks"]["K3_first_law"]["ok"] = bool(R["checks"]["K3_first_law"]["max"] <= 1e-6)
    k4 = [(r["drho_over_rho0_total_from_z8"], r["ceiling_all_cold_cluster"]) for r in RES.values()]
    R["checks"]["K4_ceiling"] = dict(max_drho=max(x[0] for x in k4), ceiling=k4[0][1], ok=bool(all(x[0] <= x[1] for x in k4)))
    P("\n[K] controls")
    P(f"  K0 age analytic {T0:.6f} vs cfg557_lib {L.T0:.6f} (1/H0): rel {R['checks']['K0_age']['rel']:.1e}")
    P(f"  K1 PS normalisation {R['checks']['K1_PS_norm']['value']:.6f} -> {'PASS' if R['checks']['K1_PS_norm']['ok'] else 'FAIL'} "
      f"(ST {R['checks']['K1_ST_norm_reported']:.4f}, reported)")
    P(f"  K2 ODE vs quadrature (max over primary cells, relative to drho(z=8)): {R['checks']['K2_ode_vs_quad']['max']:.2e} -> "
      f"{'PASS' if R['checks']['K2_ode_vs_quad']['ok'] else 'FAIL'}")
    P(f"  K3 first law a^3 delta(rho c^2) - int delta(rho c^2) d(a^3) - (U - U_i), max / U(0): {R['checks']['K3_first_law']['max']:.2e} -> "
      f"{'PASS' if R['checks']['K3_first_law']['ok'] else 'FAIL'}")
    P(f"  K4 max drho/rho0 over ALL variants {R['checks']['K4_ceiling']['max_drho']:.3e} <= ceiling {R['checks']['K4_ceiling']['ceiling']:.3e} "
      f"-> {'PASS' if R['checks']['K4_ceiling']['ok'] else 'FAIL'}")
    P(f"  K5 CPL of exact Lambda: ({w0L:.2e}, {waL:.2e}), H-fit ({w0H:.2e}, {waH:.2e}) -> {'PASS' if R['checks']['K5_cpl_lambda']['ok'] else 'FAIL'}")

    # ---------------------------------------------------------- K6 native check against the PM's own switch-on mass fraction
    P("\n[K6] native check (REPORTED): PM switch-on mass fraction (CFG424 TA boxes) vs route-H instantaneous (alpha = inf) catchment")
    W424 = os.path.join(EXT, "cfg424_work")
    boxes = {"can": ["FLAT_canonical_N512", "FLAT_canonical_N512_seed360", "FLAT_canonical_N256", "FLAT_canonical_N256_seed360",
                     "FLAT_canonical_N256_seed361"],
             "alt": ["FLAT_alt_N512", "FLAT_alt_N256", "FLAT_alt_N256_seed360", "FLAT_alt_N256_seed361"]}
    K6 = {}
    for f, names in boxes.items():
        for nm in names:
            fn = os.path.join(W424, f"cfg424_RES_TA_MIXA_MASSCONS_fret1_{nm}.json")
            if not os.path.exists(fn):
                K6[nm] = "missing"; continue
            js = json.load(open(fn)); N = int(js["np"]) if "np" in js else (512 if "N512" in nm else 256)
            Lb = float(js["L"]); mp = L.RHO_M * Lb ** 3 / N ** 3
            pm = {z: float(js["snap"][k]["mass_f"]) for z, k in ((0.0, "z0"), (0.5, "z0.5"), (1.0, "z1"))}
            row = dict(N=N, m_p=mp, PM_mass_f=pm)
            for npart in (20, 100):
                Mres = npart * mp
                sc = SC[(f, math.inf)]
                fh = {}
                for z in (0.0, 0.5, 1.0):
                    iz = Z_EP.index(z)
                    scf = np.interp(LMF, LMG, sc[iz]); sel = LMF >= math.log10(Mres)
                    # catchment mass fraction counting baryons too (the PM's mass_f is a fraction of all particles)
                    fh[z] = float(TRAPZ((dFdlnM(z, "PS") * scf)[sel], LMF[sel] * math.log(10)))
                row[f"H_{npart}p"] = fh
                row[f"PM_over_H_{npart}p"] = {str(z): pm[z] / fh[z] for z in fh}
            K6[nm] = row
            P(f"  {nm:30s} m_p {mp:.2e}: PM mass_f z1/0.5/0 = {pm[1.0]:.4f}/{pm[0.5]:.4f}/{pm[0.0]:.4f};  route H (>100 m_p) "
              f"{row['H_100p'][1.0]:.4f}/{row['H_100p'][0.5]:.4f}/{row['H_100p'][0.0]:.4f};  PM/H {row['PM_over_H_100p']['1.0']:.2f}/"
              f"{row['PM_over_H_100p']['0.5']:.2f}/{row['PM_over_H_100p']['0.0']:.2f}")
    R["checks"]["K6_native"] = K6
    # native-anchored variant: rescale the primary U by the 512^3 seed-359 PM/H ratio (100 particles) at z = 0, 0.5, 1
    NAT = {}
    for f, nm in (("can", "FLAT_canonical_N512"), ("alt", "FLAT_alt_N512")):
        if not isinstance(K6.get(nm), dict):
            continue
        rz = K6[nm]["PM_over_H_100p"]
        zz = np.array([0.0, 0.5, 1.0]); rr = np.array([rz["0.0"], rz["0.5"], rz["1.0"]])
        for al in ALPHA_BRACKET:
            U_ep, F_ep = U_epochs(f, al, "PS", 1e8)
            scale = np.interp(Z_EP, zz, rr)
            hst = history(U_ep * scale)
            NAT[f"{f}|alpha{al}"] = summarise(hst, U_ep * scale, F_ep, full=False)
        P(f"  native-anchored ({nm}, PM/H {rr[0]:.2f}/{rr[1]:.2f}/{rr[2]:.2f} at z 0/0.5/1): drho/rho0 z1 = "
          + ", ".join(f"a{al}: {NAT[f'{f}|alpha{al}']['drho_over_rho0']['1.0']:.2e}" for al in ALPHA_BRACKET))
    R["native_anchored"] = NAT

    # ---------------------------------------------------------- prediction tables
    P("\n[PREDICTION] primary (PS turnaround barrier, M_min 1e8 Msun/h) over the alpha bracket [0.5, 1.186]  -- HMF context")
    PRED = {}
    for f in FOOTS:
        P(f"  footing {f} ({L.A0[FOOTS[f]]:.4e} m/s^2):")
        for al, r in zip(ALPHA_BRACKET, prim[f]):
            P(f"    alpha {al:5.3f}: Q(0) {r['Q_W_per_m3']['0.0']:.3e} W/m^3; drho/rho0 z0.5 {r['drho_over_rho0']['0.5']:.3e} z1 "
              f"{r['drho_over_rho0']['1.0']:.3e} z2 {r['drho_over_rho0']['2.0']:.3e} z3 {r['drho_over_rho0']['3.0']:.3e}; "
              f"1+w_DE(0) {r['onepw_DE']['0.0']:+.3e}, max q(z<=3) {r['max_q_z_le_3']:.2e}")
            P(f"                 CPL DE-own (w0+1, wa) ({r['cpl_DE_own'][0] + 1:+.2e}, {r['cpl_DE_own'][1]:+.2e}); observer "
              f"({r['cpl_observer'][0] + 1:+.2e}, {r['cpl_observer'][1]:+.2e}); H-fit ({r['cpl_Hfit'][0] + 1:+.2e}, {r['cpl_Hfit'][1]:+.2e})")
            P(f"                 a0(z)/a0(0) - 1: z1 {r['a0_ratio_minus_1']['1.0']:+.3e} z2 {r['a0_ratio_minus_1']['2.0']:+.3e} z3 "
              f"{r['a0_ratio_minus_1']['3.0']:+.3e}  (dex {r['dlog10_a0']['1.0']:+.2e} / {r['dlog10_a0']['2.0']:+.2e} / {r['dlog10_a0']['3.0']:+.2e})")
        def rng(fn):
            v = [fn(r) for r in prim[f]]
            return [min(v), max(v)]
        PRED[f] = dict(Q0_W_per_m3=rng(lambda r: r["Q_W_per_m3"]["0.0"]),
                       Q0_over_H0_rhoDE0c2=rng(lambda r: r["Q_over_H0_rhoDE0c2"]["0.0"]),
                       drho_over_rho0={z: rng(lambda r, z=z: r["drho_over_rho0"][z]) for z in ("0.5", "1.0", "2.0", "3.0")},
                       onepw0=rng(lambda r: r["onepw_DE"]["0.0"]),
                       w0p1_DE_own=rng(lambda r: r["cpl_DE_own"][0] + 1), wa_DE_own=rng(lambda r: r["cpl_DE_own"][1]),
                       w0p1_observer=rng(lambda r: r["cpl_observer"][0] + 1), wa_observer=rng(lambda r: r["cpl_observer"][1]),
                       w0p1_Hfit=rng(lambda r: r["cpl_Hfit"][0] + 1), wa_Hfit=rng(lambda r: r["cpl_Hfit"][1]),
                       a0_ratio_minus_1={z: rng(lambda r, z=z: r["a0_ratio_minus_1"][z]) for z in ("1.0", "2.0", "3.0")},
                       dlog10_a0={z: rng(lambda r, z=z: r["dlog10_a0"][z]) for z in ("1.0", "2.0", "3.0")},
                       max_q=max(r["max_q_z_le_3"] for r in prim[f]), min_q=min(r["min_q"] for r in prim[f]),
                       fork_dex=max(r["fork_minus_p_vs_rho_max_dex_z_le_3"] for r in prim[f]))
    R["prediction"] = PRED
    # brackets over HMF form and M_min (alpha bracket), both footings
    BR = {}
    for f in FOOTS:
        v = [RES[f"{f}|{hmf}|Mmin{Mmin:.0e}|alpha{al}"]["drho_over_rho0"]["1.0"] for hmf in HMFS for Mmin in MMINS for al in ALPHA_BRACKET]
        v0 = [RES[f"{f}|{hmf}|Mmin{Mmin:.0e}|alpha{al}"]["Q_W_per_m3"]["0.0"] for hmf in HMFS for Mmin in MMINS for al in ALPHA_BRACKET]
        BR[f] = dict(drho_z1=[min(v), max(v)], Q0=[min(v0), max(v0)])
        diag = {str(al): RES[f"{f}|PS|Mmin1e+08|alpha{al}"]["drho_over_rho0"]["1.0"] for al in (2.0, math.inf)}
        BR[f]["diagnostic_outside_bracket_drho_z1"] = diag
    R["brackets"] = BR
    P("\n[BRACKETS] drho/rho0 at z = 1 over PS/ST x M_min {1e6, 1e8, 1e10} x alpha bracket:")
    for f in FOOTS:
        P(f"  {f}: [{BR[f]['drho_z1'][0]:.2e}, {BR[f]['drho_z1'][1]:.2e}]; Q(0) [{BR[f]['Q0'][0]:.2e}, {BR[f]['Q0'][1]:.2e}] W/m^3; "
          f"outside bracket alpha 2: {BR[f]['diagnostic_outside_bracket_drho_z1']['2.0']:.2e}, alpha inf (ceiling): "
          f"{BR[f]['diagnostic_outside_bracket_drho_z1']['inf']:.2e}")

    # ---------------------------------------------------------- verdicts
    allp = [r for f in FOOTS for r in prim[f]]
    m_w0 = max(max(abs(r["cpl_DE_own"][0] + 1), abs(r["cpl_observer"][0] + 1), abs(r["cpl_Hfit"][0] + 1)) for r in allp)
    m_wa = max(max(abs(r["cpl_DE_own"][1]), abs(r["cpl_observer"][1]), abs(r["cpl_Hfit"][1])) for r in allp)
    m_a0 = max(abs(v) for r in allp for v in r["dlog10_a0"].values())
    fr = dict(w0=m_w0 / SIG_W0, wa=m_wa / SIG_WA, a0=m_a0 / A0_SEP_DEX)
    if fr["w0"] >= 1 or fr["wa"] >= 1 or fr["a0"] >= 1:
        tv = "MEASURABLE"
    elif max(fr.values()) < 1e-2:
        tv = "BELOW SENSITIVITY"
    else:
        tv = "MARGINAL"
    n_discs = (0.1 / max(abs(r["dlog10_a0"]["2.0"]) for r in allp)) ** 2
    R["testability"] = dict(max_abs_w0p1=m_w0, max_abs_wa=m_wa, max_abs_dlog10_a0=m_a0, sigma_w0_context=SIG_W0, sigma_wa_context=SIG_WA,
                            a0_threshold_dex=A0_SEP_DEX, fractions_of_threshold=fr, verdict=tv,
                            discs_needed_at_0p1dex_z2_statistical_only=n_discs,
                            a0_drift_over_per_disc_floor=m_a0 / A0_FLOOR_DEX, a0_drift_over_unseparable_0p02=m_a0 / A0_UNSEP_DEX)
    sign_ok = all(r["min_q"] >= 0 for r in allp)
    maxq = max(r["max_q_z_le_3"] for r in allp)
    R["sign"] = dict(verdict="PHANTOM-SIDE" if sign_ok else "CROSSES", min_q=min(r["min_q"] for r in allp), max_q_z_le_3=maxq,
                     crossing_of_minus1=not sign_ok,
                     canonical_partner="regular only where its own 1 + w_phi >> q; the singular band is |1 + w| <~ q_max = %.1e" % maxq)
    P("\n[VERDICTS]")
    P(f"  TESTABILITY: {tv}.  max |1+w0| {m_w0:.2e} = {fr['w0']:.1e} sigma(w0) [{SIG_W0:.3f}, context]; max |wa| {m_wa:.2e} = "
      f"{fr['wa']:.1e} sigma(wa) [{SIG_WA:.3f}]; max |dlog10 a0| (z <= 3) {m_a0:.2e} dex = {fr['a0']:.1e} of 0.007 dex "
      f"({m_a0 / A0_UNSEP_DEX:.1e} of the record's unseparable 0.02 dex; {m_a0 / A0_FLOOR_DEX:.1e} of the 0.15 dex per-disc floor).")
    P(f"  Statistical-only disc count to see the z = 2 drift at 0.1 dex per disc: N ~ {n_discs:.1e} (before any systematic floor).")
    P(f"  SIGN: {R['sign']['verdict']}: Q >= 0 at every z (ratchet), so rho_DE grows toward today, 1 + w_DE = -q <= 0, no crossing of -1. "
      f"max q (z <= 3) = {maxq:.2e}.")
    P(f"  Canonical partner: phi'' + 3H phi' + V' = Q/phi' is singular at phi' = 0 (w = -1). The source is a small perturbation only "
      f"where 1 + w_phi >> q ~ {maxq:.0e}; the observed w_eff = w_phi - q. So a canonical partner can show w_eff < -1 only inside a band "
      f"|1 + w| <~ {maxq:.0e} around -1, i.e. the sink cannot produce or rescue an O(0.1) crossing of -1; with w_phi exactly -1 it is singular.")
    P(f"  CFG511 fork (a0 tracking -p_DE instead of rho_DE) under this prediction: <= {max(PRED[f]['fork_dex'] for f in FOOTS):.1e} dex.")
    P("  CFG549 R1 comparison (instantaneous, E_sink, ST/CAMB): 7.1e-7 / 2.0e-7 (can A / B) today-integrated; R3f scaled ceiling 2.6e-6.")

    # ---------------------------------------------------------- figure
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
        zz = np.linspace(0, 3, 121)
        cols = {"can": "#1f5fa8", "alt": "#c0562a"}
        for f in FOOTS:
            for al, ls in zip(ALPHA_BRACKET, (":", "-.", "-", "--")):
                U_ep, F_ep = U_epochs(f, al, "PS", 1e8); hst = history(U_ep)
                d = 1 - hst["rhoDE"] / RHO_DE0
                dz = np.array([at_z(d, z) for z in zz])
                ax[0].plot(zz, dz * 1e7, ls, color=cols[f], lw=1.4, label=f"{f}, alpha {al}")
                ax[1].plot(zz, 0.5 * np.log1p(-dz) / math.log(10) * 1e8, ls, color=cols[f], lw=1.4)
        ax[0].set_xlabel("z"); ax[0].set_ylabel("[rho_DE(0) - rho_DE(z)] / rho_DE(0)  [x 1e-7]")
        ax[0].set_title("Settling energy added to dark energy since z")
        ax[0].legend(fontsize=7, ncol=2)
        ax[1].set_xlabel("z"); ax[1].set_ylabel("log10 a0(z)/a0(0)  [x 1e-8 dex]")
        ax[1].set_title("a0 drift from settling (flat law = 0)")
        fig.suptitle("CFG630 (HMF context; PS turnaround barrier, M_min 1e8): kappa fitted, cold energy mass required", fontsize=9)
        fig.tight_layout()
        fig.savefig(os.path.join(HERE, "cfg630_prediction.png"), dpi=130)
        P("\n  figure: cfg630_prediction.png")
    except Exception as e:                                             # noqa: BLE001
        P(f"  figure skipped: {e}")

R["disclosures"] = [
    "s_c re-implements cfg557_lib.s_catch with the same iteration; only a converged 'nothing captured' state reads as 0 (CFG557 reports "
    "the 0.02 grid floor). alpha = 0 runs through the same code with t_cap = inf.",
    "Post-first-run fixes (numbers in the first run differed only through these): (1) the first version made s_c = 0 ABSORBING at an "
    "intermediate iterate, which killed real fixed points (e.g. alpha 0.5, z 2, log M_ta 12: 0 instead of CFG557's 0.210); fixed to the "
    "CFG557 restart. (2) K2 first read 1.21e-9 (> 1e-9) because DOP853 stepped across the PCHIP knots; the ODE is now integrated knot to "
    "knot (9.8e-11). No criterion was changed.",
    "eps_W uses CFG542's overdamped dW per catchment mass at FULL settling for every settled fraction; c_W spans 0.77-0.99 V_f^2 (+-13%).",
    "U(t) is a state function of the halo population (re-settling after growth or mergers is not tracked separately); the ratchet keeps Q >= 0.",
    "The background H(z) in the integration is the input matter+Lambda one; the feedback of a 1e-7 change on H is neglected.",
    "f_ta (PS / ST on the turnaround barrier), the EH spectrum, linear growth, spherical-collapse t_reach and the EPS main progenitor are "
    "inherited ingredients; the result is labelled HMF context. DESI sigmas are context only.",
]
R["runtime_s"] = time.time() - T_START
ok_all = all(v.get("ok", True) for k, v in R["checks"].items() if isinstance(v, dict) and "ok" in v)
R["all_checks_pass"] = bool(ok_all)
P(f"\nall frozen checks pass: {ok_all}   runtime {R['runtime_s']:.0f} s")


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


json.dump(_clean(R), open(os.path.join(HERE, f"cfg630_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg630{SUF}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if ok_all else 1)
