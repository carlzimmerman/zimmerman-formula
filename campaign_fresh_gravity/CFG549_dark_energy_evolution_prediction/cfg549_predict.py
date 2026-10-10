#!/usr/bin/env python3
"""CFG549 stage 1: framework-only predictions for rho_DE(z). NO DESI / DES / SN input (FROZEN_CRITERIA.md section 1).

Inputs: CFG541 JSON (kappa, footings, f_b, cold_per_b, Omega_m, h, E_sink per settled mass), CFG506 JSON (settled fraction 0.162),
CFG493 JSON (fitted kappa, for R3e), Planck 2018 primordial amplitude/tilt through CAMB (declared CMB input).
Outputs: cfg549_predict.out / cfg549_predictions.json (+ PREDICTIONS_HASH.txt); MUTATE -> *_MUTATE.* files.
Run: nice -n 10 python3 cfg549_predict.py   (CFG549_MUTATE=1 for the mutation run)
"""
import hashlib
import json
import math
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np                       # noqa: E402
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
import sympy as sp                       # noqa: E402
from scipy.integrate import solve_ivp, quad, cumulative_trapezoid   # noqa: E402
from scipy.optimize import brentq        # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
MUT = os.environ.get("CFG549_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg549_predict{SUF}.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.write(s + "\n")


# firewall: refuse to run if any DE-data module/path is imported or referenced
for m in list(sys.modules):
    assert "cfg508" not in m and "cfg511" not in m, "firewall: DE-data module imported"

c = 2.99792458e8; G = 6.67430e-11; MSUN = 1.98892e30; MPC = 3.0856775814913673e22; GYR = 3.15576e16
J541 = json.load(open(os.path.join(CFG, "CFG541_cold_energy_equations_precise", "cfg541_results.json")))
J506 = json.load(open(os.path.join(CFG, "CFG506_native_environment", "cfg506_diag_results.json")))
J493 = json.load(open(os.path.join(CFG, "CFG493_kappa_combined", "cfg493_kappa_combined_results.json")))
S = J541["settings"]
KAPPA = S["kappa"]; FOOT = S["footings"]; FB = S["f_b"]; OM = S["Omega_m"]; h = S["h"]; CPB = S["cold_per_b"]
OL = 1 - OM
H0 = 100 * h * 1e3 / MPC
RHOC0 = 3 * H0 ** 2 / (8 * math.pi * G)
RHO_C0 = OM * (1 - FB) * RHOC0                 # cosmic cold energy today (kg/m^3), from the cold amount and f_b
RHO_DE0 = OL * RHOC0
SETTLED_506 = J506["D1"]["TA512_can359"]["settled_mass_frac"]
LN10AS, NS = 3.044, 0.9649                     # Planck 2018 (declared CMB input)
OMBH2 = OM * FB * h * h; OMCH2 = OM * (1 - FB) * h * h

R = {"lane": "CFG549", "stage": "predict (no DE data)", "mutate": MUT,
     "inputs": dict(kappa=KAPPA, footings=FOOT, f_b=FB, Omega_m=OM, h=h, cold_per_b=CPB, ln10As=LN10AS, ns=NS,
                    settled_frac_CFG506=SETTLED_506, declared_CMB_inputs="h, Omega_m (CFG541 settings), ln10^10 As, ns (Planck 2018)"),
     "checks": {}}
P("CFG549 stage 1: framework-only predictions (no DESI/DES/SN).  MUTATE =", MUT)
P(f"inputs: kappa {KAPPA}, footings {FOOT}, f_b {FB:.5f}, Omega_m {OM}, h {h}, cold/b {CPB:.4f}, settled frac (CFG506) {SETTLED_506:.4f}")


def E(a):
    return math.sqrt(OM / a ** 3 + OL)


def Hz(a):
    return H0 * E(a)


# ------------------------------------------------------------------ linear power + Sheth-Tormen
import camb                                     # noqa: E402
pars = camb.CAMBparams()
pars.set_cosmology(H0=100 * h, ombh2=OMBH2, omch2=OMCH2, mnu=0.06, omk=0, tau=0.0544)
pars.InitPower.set_params(As=math.exp(LN10AS) * 1e-10, ns=NS)
pars.set_matter_power(redshifts=[0.0], kmax=200.0)
pars.NonLinear = camb.model.NonLinear_none
res = camb.get_results(pars)
kh, _, pk = res.get_matter_power_spectrum(minkh=1e-4, maxkh=150.0, npoints=1200)
sig8 = float(res.get_sigma8_0())
k = kh * h / MPC                                # 1/m
Pk = pk[0] * (MPC / h) ** 3                     # m^3
RHO_M0 = OM * RHOC0
P(f"CAMB sigma8 = {sig8:.4f}")
R["checks"]["K2_sigma8"] = dict(value=sig8, ok=bool(abs(sig8 - 0.811) <= 0.015))


def sigma_M(M):
    Rr = (3 * M / (4 * math.pi * RHO_M0)) ** (1 / 3)
    x = k * Rr
    W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return math.sqrt(TRAPZ(k ** 3 * Pk * W ** 2 / (2 * math.pi ** 2), np.log(k)))


def growth(a):                                  # linear growth for flat LCDM, normalised D(1) = 1
    f = lambda aa: 1.0 / (aa * E(aa)) ** 3
    return E(a) * quad(f, 0, a)[0] / (E(1) * quad(f, 0, 1)[0])


lnM = np.linspace(math.log(1e4 * MSUN), math.log(1e17 * MSUN), 260)
sig0 = np.array([sigma_M(math.exp(x)) for x in lnM])
DC = 1.686; A_ST, a_ST, p_ST = 0.3222, 0.707, 0.3


def fST(nu):
    return A_ST * math.sqrt(2 * a_ST / math.pi) * (1 + (a_ST * nu * nu) ** (-p_ST)) * np.exp(-a_ST * nu * nu / 2)


# K1 normalisation: integral of fST over nu from tiny to inf
nu_grid = np.linspace(1e-6, 12, 200001)
R["checks"]["K1_ST_norm"] = dict(value=float(TRAPZ(fST(nu_grid), nu_grid)))
R["checks"]["K1_ST_norm"]["ok"] = bool(R["checks"]["K1_ST_norm"]["value"] >= 0.95)


# ------------------------------------------------------------------ e(M): E_sink per unit settled cold mass (CFG541)
def e_table(foot):
    pts = []
    for n in ("MW", "group", "cluster"):
        x = J541["one_d"][foot][n]
        Mtot = J541["systems"][n]["Mb"] * (1 + x["Mcat_over_Mb"])
        pts.append((math.log(Mtot * MSUN), math.log(x["Esink_per_mass"])))
    pts.sort()
    return pts


def e_of_M(lnMkg, pts, zero=False):
    if zero:
        return np.zeros_like(lnMkg)
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    y = np.interp(lnMkg, xs, ys)
    y = np.where(lnMkg < xs[0], ys[0] + 0.5 * (lnMkg - xs[0]), y)
    y = np.where(lnMkg > xs[-1], ys[-1] + 0.5 * (lnMkg - xs[-1]), y)
    return np.exp(y)


AG = np.exp(np.linspace(math.log(1 / 31.0), 0.0, 300))     # a from z = 30 to 0
DG = np.array([growth(a) for a in AG])


def settled_energy(foot, Mmin, branch, zero=False, qscale=1.0):
    """U(a): settled (released) energy per comoving volume, J/m^3 comoving; F(a): settled mass fraction."""
    pts = e_table(foot)
    sel = lnM >= math.log(Mmin * MSUN)
    lm = lnM[sel]; s0 = sig0[sel]
    eM = e_of_M(lm, pts, zero)
    U = np.zeros_like(AG); F = np.zeros_like(AG)
    for i, D in enumerate(DG):
        nu = DC / (s0 * D)
        # mass fraction per ln M = fST(nu) dnu/dlnM
        dF = fST(nu) * np.abs(np.gradient(nu, lm))
        F[i] = TRAPZ(dF, lm) + quad(lambda v: fST(v), nu[-1], 40)[0]     # include M > grid top (negligible)
        U[i] = RHO_C0 * TRAPZ(eM * dF, lm)
    if branch == "B":
        sc = SETTLED_506 / F[-1]
        U = U * sc; F = F * sc
    return U * qscale, F


def trickle(foot, Mmin, branch, zero=False, qscale=1.0):
    U, F = settled_energy(foot, Mmin, branch, zero, qscale)
    t = cumulative_trapezoid(1.0 / (AG * np.array([Hz(a) for a in AG])), AG, initial=0.0)
    dUda = np.gradient(U, AG)
    Qc2 = AG ** -3 * dUda * AG * np.array([Hz(a) for a in AG])         # J/m^3/s physical (dU/dt = dU/da * aH)
    dRho = cumulative_trapezoid(AG ** -3 * dUda, AG, initial=0.0) / c ** 2   # kg/m^3 added to the w = -1 sink
    rho_i = RHO_DE0 - dRho[-1]                                         # today's total fixed at the CMB-closure value
    rhoDE = rho_i + dRho
    onepw = -(Qc2 / c ** 2) / (3 * np.array([Hz(a) for a in AG]) * rhoDE)
    # effective DE (matter normalised today): cold loses U/c^2 per comoving volume
    rho_eff = rhoDE + AG ** -3 * (U[-1] - U) / c ** 2
    return dict(U=U, F=F, Qc2=Qc2, dRho=dRho, rhoDE=rhoDE, onepw=onepw, rho_eff=rho_eff, t=t)


def cpl_project(a, rho_eff):
    z = 1 / a - 1
    m = (z >= 0) & (z <= 2.5)
    zz = z[m]; y = np.log(rho_eff[m] / rho_eff[-1])
    # ln(rho/rho0) = 3(1+w0+wa) ln(1+z) - 3 wa z/(1+z) ; unknowns (1+w0), wa
    A = np.vstack([3 * np.log(1 + zz), 3 * (np.log(1 + zz) - zz / (1 + zz))]).T
    sol, *_ = np.linalg.lstsq(A, y, rcond=None)
    return float(sol[0] - 1), float(sol[1])


def hz_project(a, H_over_H0):
    """Post-freeze projection (disclosed): fit (Om, w0, wa) of flat CPL to the model's H(z)/H0 on z in [0, 2.5] (H0 fixed)."""
    from scipy.optimize import least_squares
    z = 1 / a - 1
    m = (z >= 0) & (z <= 2.5)
    zz = z[m]; y = np.log(H_over_H0[m])
    def r(p):
        Om_, w0_, wa_ = p
        f = (1 + zz) ** (3 * (1 + w0_ + wa_)) * np.exp(-3 * wa_ * zz / (1 + zz))
        return 0.5 * np.log(Om_ * (1 + zz) ** 3 + (1 - Om_) * f) - y
    sol = least_squares(r, [0.31, -1.0, 0.0], xtol=1e-15, ftol=1e-15, gtol=1e-15)
    return float(sol.x[1]), float(sol.x[2]), float(sol.x[0]), float(np.max(np.abs(sol.fun)))


# K6: CPL projection of exact Lambda
ZL = np.linspace(0, 2.5, 51); AL = 1 / (1 + ZL)
w0L, waL = cpl_project(AL[::-1], np.ones_like(AL))
w0H, waH, OmH, _ = hz_project(AL[::-1], np.sqrt(OM * (1 + ZL[::-1]) ** 3 + OL))
R["checks"]["K6_cpl_lambda"] = dict(w0=w0L, wa=waL, w0_H=w0H, wa_H=waH, Om_H=OmH,
                                   ok=bool(abs(w0L + 1) < 1e-6 and abs(waL) < 1e-6 and abs(w0H + 1) < 1e-6 and abs(waH) < 1e-6))


def zsel(arr, z):
    return float(np.interp(1 / (1 + z), AG, arr))


# ------------------------------------------------------------------ R1
P("\n[R1] SETTLING SOURCE: Lambda + settling trickle into a w = -1 sink (maximal accumulation)")
R1 = {}
ceiling = J541["S"]["ii"]["cosmic_drho_over_rho"]
for foot in FOOT:
    for br in ("A", "B"):
        for Mmin in (1e6, 1e8, 1e10):
            tr = trickle(foot, Mmin, br, qscale=(1e6 if MUT else 1.0))
            w0, wa = cpl_project(AG, tr["rho_eff"])
            Hh = np.sqrt((RHO_M0 / AG ** 3 - (tr["U"]) / c ** 2 / AG ** 3 + tr["rhoDE"]) / RHOC0 + 0 * AG)
            w0h, wah, Omh, resh = hz_project(AG, Hh / Hh[-1])
            key = f"{foot}|{br}|Mmin{Mmin:.0e}"
            row = dict(F_z0=float(tr["F"][-1]), drho_over_rho_z0=float(tr["dRho"][-1] / RHO_DE0),
                       rho_ratio={str(z): zsel(tr["rhoDE"], z) / tr["rhoDE"][-1] for z in (0.5, 1, 2, 2.5)},
                       onepw={str(z): zsel(tr["onepw"], z) for z in (0, 0.5, 1, 2, 2.5)},
                       max_abs_onepw_z_le_2p5=float(np.max(np.abs(tr["onepw"][1 / AG - 1 <= 2.5]))),
                       w0_eff=w0, wa_eff=wa, w0_eff_H=w0h, wa_eff_H=wah, Om_H=Omh, U_z0_J_per_m3=float(tr["U"][-1]),
                       eps_settled_over_c2=float(tr["U"][-1] / (RHO_C0 * c ** 2)))
            R1[key] = row
            if Mmin == 1e8 or MUT:
                P(f"  {key:24s} F(0) {row['F_z0']:.3f}  drho_DE/rho_DE(0) {row['drho_over_rho_z0']:.3e}  "
                  f"1+w(0) {row['onepw']['0']:+.2e}  1+w(1) {row['onepw']['1']:+.2e}  max|1+w| {row['max_abs_onepw_z_le_2p5']:.2e}  "
                  f"CPL (w0+1, wa) = ({w0 + 1:+.2e}, {wa:+.2e}); H-fit ({w0h + 1:+.2e}, {wah:+.2e})")
R["R1"] = R1
for foot in FOOT:
    v = R1[f"{foot}|A|Mmin1e+08"]["drho_over_rho_z0"]
    R["checks"][f"K3_ceiling_{foot}"] = dict(value=v, ceiling=ceiling, ok=bool(MUT or v <= ceiling))
P(f"  CFG541 ceiling (all cold energy at the cluster e_max): {ceiling:.3e}")
# MU3 null
trn = trickle("can", 1e8, "A", zero=True)
R["checks"]["MU3_null"] = dict(max_abs_drho=float(np.max(np.abs(trn["dRho"]))), ok=bool(np.max(np.abs(trn["dRho"])) == 0.0))
P(f"  MU3 null e(M) = 0: max |drho| = {R['checks']['MU3_null']['max_abs_drho']}")
# a0 consequence of the trickle (kappa cancels)
pr = R1["can|A|Mmin1e+08"]
R["R1_a0_ratio"] = {z: math.sqrt(v) for z, v in pr["rho_ratio"].items()}
P("  a0(z)/a0(0) under the trickle (can, A): " + ", ".join(f"z{z}: {v:.10f}" for z, v in R["R1_a0_ratio"].items()))

# ------------------------------------------------------------------ M-C4 (CFG360 C4): vacuum -> cold at Gamma = a0(t)/c
P("\n[M-C4] vacuum -> cold at Gamma = a0(t)/c = kappa sqrt(G rho_vac(t)) (zero new constants; CFG360 C4 re-run)")
OMRH2 = 4.18e-5                                  # photons + 3.046 massless nu (standard; early-time only)
RHO_R0 = OMRH2 / h ** 2 * RHOC0
RHO_B0 = OM * FB * RHOC0


def run_c4(a0foot, rho_v_i, ai=1e-3):
    def rhs(lna, y):
        a = math.exp(lna); rv, rcomov = y            # rcomov = rho_c a^3
        rc = rcomov / a ** 3
        H = math.sqrt(8 * math.pi * G / 3 * (RHO_B0 / a ** 3 + rc + max(rv, 0) + RHO_R0 / a ** 4))
        Gam = a0foot / c * math.sqrt(max(rv, 0) / RHO_DE0)
        return [-Gam / H * rv, Gam / H * rv * a ** 3]
    sol = solve_ivp(rhs, [math.log(ai), 0.0], [rho_v_i, RHO_C0], rtol=1e-10, atol=1e-40, dense_output=True)
    return sol


C4 = {}
for foot, a0f in FOOT.items():
    # closure: rho_b0 + rho_c(1) + rho_v(1) + rho_r0 = rho_crit0 (H0 fixed)
    def clos(rvi):
        s = run_c4(a0f, rvi).y[:, -1]
        return RHO_B0 + s[1] + s[0] + RHO_R0 - RHOC0
    # early cold comoving fixed at the CMB value: initial rho_c a^3 = RHO_C0 (CMB-anchored early amount)
    rvi = brentq(clos, 0.3 * RHO_DE0, 3.0 * RHO_DE0, xtol=1e-40, rtol=1e-12)
    sol = run_c4(a0f, rvi)
    lna = np.linspace(math.log(1 / 31.0), 0.0, 300); a = np.exp(lna)
    rv, rcm = sol.sol(lna)
    rc1 = rcm[-1]
    rho_eff = rv + (rcm - rc1) / a ** 3
    neg = bool(np.any(rho_eff <= 0))
    z_cross = float(1 / a[np.where(rho_eff <= 0)[0].max()] - 1) if neg else None
    Hm = np.sqrt(8 * math.pi * G / 3 * (RHO_B0 / a ** 3 + rcm / a ** 3 + rv + RHO_R0 / a ** 4))
    w0, wa, OmH, resH = hz_project(a, Hm / Hm[-1])
    Om_obs = (RHO_B0 + rc1) / RHOC0
    H = np.sqrt(8 * math.pi * G / 3 * (RHO_B0 / a ** 3 + rcm / a ** 3 + rv + RHO_R0 / a ** 4))
    Gam = a0f / c * np.sqrt(rv / rv[-1])
    onepw_vac = Gam / (3 * H)
    C4[foot] = dict(rho_vac_i_over_rhoDE0=rvi / RHO_DE0, rho_vac0_over_rhocrit=float(rv[-1] / RHOC0),
                    Om_obs=float(Om_obs), cold_gain_since_ai=float(rc1 / RHO_C0 - 1),
                    Gamma0_over_H0=float(a0f / c / H0), onepw_vac_z0=float(onepw_vac[-1]),
                    rho_vac_ratio={str(z): float(np.interp(1 / (1 + z), a, rv) / rv[-1]) for z in (0.5, 1, 2, 2.5)},
                    a0_ratio={str(z): float(math.sqrt(np.interp(1 / (1 + z), a, rv) / rv[-1])) for z in (0.5, 1, 2, 2.5)},
                    frozen_projection_defined=not neg, rho_eff_crosses_zero_below_z=z_cross,
                    w0_eff=w0, wa_eff=wa, Om_H=OmH, H_fit_max_resid=resH)
    P(f"  {foot}: frozen rho_eff projection {'UNDEFINED (rho_eff <= 0 at z >= %.2f)' % z_cross if neg else 'defined'}; H-fit Om {OmH:.4f}, max resid {resH:.1e}")
    P(f"  {foot}: Gamma0/H0 {C4[foot]['Gamma0_over_H0']:.4f}; 1+w_vac(0) {onepw_vac[-1]:+.4f}; cold gain {C4[foot]['cold_gain_since_ai']:+.4f}; "
      f"Om_obs {Om_obs:.4f}; CPL (w0, wa)_eff = ({w0:+.4f}, {wa:+.4f}); a0(2.5)/a0(0) {C4[foot]['a0_ratio']['2.5']:.4f}")
R["M_C4"] = C4

# ------------------------------------------------------------------ R3 closure routes (sympy)
P("\n[R3] CLOSURE ROUTES")
a_, t_ = sp.symbols("a t", positive=True)
rho = sp.Function("rho"); w = sp.Function("w"); Q = sp.Function("Q"); Hf = sp.Function("H")
cont = sp.Eq(rho(t_).diff(t_) + 3 * Hf(t_) * (1 + w(t_)) * rho(t_), Q(t_))
sol_w1 = sp.dsolve(cont.subs(w(t_), -1), rho(t_))
R3 = {}
R3["a_energy_conservation"] = dict(
    equation=str(cont), unknown_functions=["rho_DE(t)", "w(t)"], equations=1,
    w_minus1_solution=str(sol_w1.rhs),
    label="FORCES ONLY THE TRICKLE: with w = -1 the sink gives rho_DE = C1 + int Q dt (R1); C1 (= rho_Lambda) is an integration "
          "constant (FREE) and any w(t) != -1 is a second unknown function with no equation (FREE)")
P("  (a) " + str(cont) + " -> one equation, two unknown functions; w = -1: rho = " + str(sol_w1.rhs))
# (e) PAPER42 zero-field energy with nu_mono
s_ = sp.symbols("s", positive=True)
# 1/2 int (nu-1) d(y^2) with y = s^2, nu_mono - 1 = 1/(e^s - 1): = int 2 s^3/(e^s - 1) ds = 2 Gamma(4) zeta(4) (Bose integral)
I_mono = sp.simplify(2 * sp.gamma(4) * sp.zeta(4))
I_quad = quad(lambda x: 2 * x ** 3 / math.expm1(x) if x > 0 else 0.0, 0, 200, limit=400)[0]
ok5 = bool(sp.simplify(I_mono - 2 * sp.pi ** 4 / 15) == 0 and abs(I_quad - float(I_mono)) < 1e-9)
R["checks"]["K5_sympy_nu_mono"] = dict(value=str(I_mono), quad=I_quad, ok=bool(ok5))
kap_imp = math.sqrt(8 * math.pi / float(I_mono))
kfit = J493["combined"]["canonical"]["kappa"]; kfs = J493["combined"]["canonical"]["sigma"]
R3["e_PAPER42_zero_field"] = dict(
    integral=str(I_mono), integral_num=float(I_mono), needed_for_kappa_half=32 * math.pi, kappa_implied=kap_imp,
    kappa_fit_CFG493=kfit, kappa_fit_sigma=kfs, pull_sigma=(kap_imp - kfit) / kfs,
    label="DERIVED but FAILS its coefficient: with the framework kernel nu_mono the zero-field energy fixes Lambda c^4/a0^2 = 2 pi^4/15, "
          "i.e. kappa = sqrt(60/pi^3); it forces rho_DE proportional to a0^2 at fixed kernel, so w = -1 exactly iff a0 is a Lagrangian "
          "constant; it gives no rho_DE(z) beyond Lambda")
P(f"  (e) 1/2 int (nu_mono - 1) d(y^2) = {I_mono} = {float(I_mono):.4f} (needs 32 pi = {32 * math.pi:.2f} for kappa = 1/2); "
  f"implied kappa = {kap_imp:.4f} vs fitted {kfit:.3f} +- {kfs:.3f} ({(kap_imp - kfit) / kfs:+.1f} sigma)")
R3["b_supply_caps"] = dict(label="NO RELATION to rho_DE dynamics: the cap (CFG364/365) compares the phantom with 5.364 M_b/f_ret per galaxy; "
                                 "it contains a0 (so rho_DE) only as a galaxy-level inequality that needs the unknown retention f_ret; it has "
                                 "no time derivative of rho_DE and no cosmic-level content")
R3["c_switch_gate"] = dict(label="NO RELATION: DE1-DE13 use a constant Lambda background (E^2 = Om(1+z)^3 + 1 - Om) and read Omega_L as a "
                                 "threshold; DE7 found the gate ill-posed when varied as an action term; no equation for rho_DE(t)")
R3["d_settled_ratchet"] = dict(
    label="BOUNDS (derived inequality, not a forcing): class A is one-sided (CFG541 open item 5), so if a0 falls after a system settles the "
          "cold energy overfills (rho_c > rho_ph) and is never removed. Then a settled galaxy's dynamical a0 = max of a0(t) since it settled. "
          "Under the framework's own prediction (Lambda + trickle, rho_DE non-decreasing) the ratchet never binds. If rho_DE falls (w > -1), "
          "local galaxies read the past maximum: kappa_fit = kappa_true sqrt(rho_max/rho_0); the size under DESI is evaluated at the test stage")
R3["f_CFG542"] = dict(label="read at the end of the lane (test stage); see README")
R["R3"] = R3
for kk in ("b_supply_caps", "c_switch_gate", "d_settled_ratchet"):
    P(f"  ({kk[0]}) {R3[kk]['label']}")

# ------------------------------------------------------------------ MU2 kappa-ratio invariance
P("\n[MU2] kappa-ratio invariance of a0(z)/a0(0) (on the trickle rho_DE(z), can A)")
tr = trickle("can", 1e8, "A")
rat = {}
for kap in (0.42, 0.5, 0.55):
    a0z = kap * c * np.sqrt(G * tr["rhoDE"])
    rat[str(kap)] = [float(np.interp(1 / (1 + z), AG, a0z) / a0z[-1]) for z in (0.5, 1, 2, 2.5)]
dev = max(abs(rat["0.42"][i] - rat["0.5"][i]) + abs(rat["0.55"][i] - rat["0.5"][i]) for i in range(4))
R["checks"]["MU2_kappa_invariance"] = dict(max_dev=dev, ok=bool(dev <= 1e-12))
P(f"  max deviation across kappa 0.42/0.5/0.55: {dev:.2e}")

# ------------------------------------------------------------------ model provenance table
R["models"] = {
    "M-Lambda (a0 Lagrangian constant / PAPER42 fixed kernel)": dict(provenance="DERIVED", label="PREDICTION (conditional: a0 constant)", w0=-1.0, wa=0.0),
    "M-R1 (Lambda + settling trickle)": dict(provenance="DERIVED", label="PREDICTION", w0=R1["can|A|Mmin1e+08"]["w0_eff"], wa=R1["can|A|Mmin1e+08"]["wa_eff"]),
    "M-C4 (CFG360 C4, Gamma = a0/c)": dict(provenance="DERIVED (record model; re-run here)", label="PREDICTION (posited rate)",
                                          w0=C4["can"]["w0_eff"], wa=C4["can"]["wa_eff"]),
    "CFG507 M1 running vacuum": dict(provenance="RESTATEMENT", label="FREE (nu <= 3e-5 free; amount = nu/a_i)"),
    "CFG511 O1 elastic vacuum": dict(provenance="USES DE DATA", label="FREE (w(z) is an input; Q1c is a mapping, not a rho_DE prediction)"),
    "DE1-DE13 gate lanes": dict(provenance="NO DE DYNAMICS", label="Lambda assumed"),
    "CFG368 F1-F4 flows": dict(provenance="USES DE DATA", label="FREE (Gamma fitted to DESI; best fits not DESI-preferred)"),
    "PAPER42": dict(provenance="DERIVED", label="PREDICTION only of w = -1 given constant a0; coefficient fails with nu_mono (R3e)"),
}
ok = all(v["ok"] for v in R["checks"].values())
P("\nchecks: " + ", ".join(f"{k} {'PASS' if v['ok'] else 'FAIL'}" for k, v in R["checks"].items()))
fn = os.path.join(HERE, f"cfg549_predictions{SUF}.json")
json.dump(R, open(fn, "w"), indent=1)
hsh = hashlib.sha256(open(fn, "rb").read()).hexdigest()
open(os.path.join(HERE, f"PREDICTIONS_HASH{SUF}.txt"), "w").write(f"{hsh}  cfg549_predictions{SUF}.json\n")
P(f"wrote {os.path.basename(fn)} sha256 {hsh}")
OUT.close()
sys.exit(0 if ok else 1)
