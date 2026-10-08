#!/usr/bin/env python3
"""CFG461: what sets the cold fluid's temperature, sigma^4 = G M_b a0 / 4?  (criteria: FROZEN_CRITERIA.md, committed first)

kappa = 1/2 is FITTED.  Both footings scored separately.  No dark-matter particle is added; the cold fluid's mass is still
required and its amount (Omega_c/Omega_b = 5.364) is an input.  This is not "theory closed".

Run:  python3 cfg461_temperature.py            (writes cfg461.out, cfg461_results.json; exit 0 iff controls K1-K4 pass)
      CFG461_MUTATE=1 python3 cfg461_temperature.py   (a0 -> 2 a0 and M_b dependence dropped inside every mechanism;
                                                       writes *_MUTATE.*; exit 1 iff every class and R0 fail G-b)
"""
import os, sys, math, json
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import CFG4_common as C  # noqa: E402  (record constants; nu_mono = FP1's committed kernel, read-only)

TRAP = C._trap
MUT = os.environ.get("CFG461_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg461{TAG}.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.write(s + "\n")


G, CL, MSUN, KPC = C.G_SI, C.C_SI, C.MSUN, C.KPC
HBAR, KB, EV = 1.054571817e-34, 1.380649e-23, 1.602176634e-19
A0 = C.A0
FOOTS = C.FOOTS
SHARE = 5.364                       # Omega_c / Omega_b (input)
FB = 1.0 / (1.0 + SHARE)            # 0.15713
LOGMB = [9.0, 10.5, 11.5]
MB = [10 ** x * MSUN for x in LOGMB]
GYR = 3.15576e16
T_H = 13.8 * GYR
H0 = 67.4e3 / (1e3 * KPC)           # s^-1 (cosmological background input, C4 only)
OM = 0.315
RHO_CRIT0 = 3 * H0 ** 2 / (8 * math.pi * G)
TOL_DEX = 0.10
MB_MUT = 10 ** 10.5 * MSUN          # MUTATE: baryon dependence dropped


def sig4_target(mb, a0):
    return G * mb * a0 / 4.0


def mech_inputs(mb, a0):
    """what a mechanism sees: MUTATE doubles a0 and drops the baryon dependence."""
    return (MB_MUT, 2.0 * a0) if MUT else (mb, a0)


results = {"lane": "CFG461", "mutate": MUT, "kappa": "1/2 FITTED", "controls": {}, "classes": {}}
P("=" * 100)
P(f"CFG461 settling-temperature mechanism   MUTATE={MUT}")
P("target sigma_t^4 = G M_b a0 / 4  (deep SIS, sigma^2 = V_f^2/2); f_b = %.5f; share %.3f" % (FB, SHARE))
P("=" * 100)

# =====================================================================================================  K1 sympy
P("\n[K1] symbolic identities (sympy)")
Gs, M, a0s, sig, r, R, V = sp.symbols("G M a0 sigma r R V", positive=True)
rho_sis = sig ** 2 / (2 * sp.pi * Gs * r ** 2)
Msis = sp.integrate(4 * sp.pi * r ** 2 * rho_sis, (r, 0, r))           # 2 sigma^2 r / G
Vc2 = sp.simplify(Gs * Msis / r)
k1a = sp.simplify(Vc2 - 2 * sig ** 2) == 0                                 # V^2 = 2 sigma^2
k1b = sp.simplify((sp.Rational(1, 2) * sp.sqrt(Gs * M * a0s)) ** 2 - Gs * M * a0s / 4) == 0   # sigma^2=V_f^2/2 -> sigma^4=GMa0/4
# truncated SIS energy: K = (3/2) M sigma^2, W = -int G M(r)/r dM
Mtot = Msis.subs(r, R)
W = -sp.integrate(Gs * Msis / r * sp.diff(Msis, r), (r, 0, R))
E = sp.Rational(3, 2) * Mtot * sig ** 2 + W
k1c = sp.simplify(E + Gs * Mtot ** 2 / (4 * R)) == 0
lamJ2 = sp.pi * sig ** 2 / (Gs * rho_sis)
k1d = sp.simplify(lamJ2 - 2 * sp.pi ** 2 * r ** 2) == 0
P(f"  V_c^2 = 2 sigma^2 for SIS: {k1a};  sigma^2 = V_f^2/2 <=> sigma^4 = G M a0/4: {k1b}")
P(f"  truncated SIS E = -G M^2/(4R): {k1c};  Jeans lambda_J^2 = 2 pi^2 r^2 (sigma-free): {k1d}")
K1 = bool(k1a and k1b and k1c and k1d)
results["controls"]["K1"] = K1

# ---- C2c: mismatch functional  F = (G/2) int (Mc - Mph)^2 / r^2 dr  -> EL
Mc_f, Mph_f = sp.Function("Mc")(r), sp.Function("Mph")(r)
Lag = Gs / 2 * (Mc_f - Mph_f) ** 2 / r ** 2
EL = sp.euler_equations(Lag, Mc_f, r)[0]
c2c_min = sp.solve(EL.lhs, Mc_f)
P(f"  C2c Euler-Lagrange of the mismatch functional: Mc(r) = {c2c_min}  (needs Mph = the law's target as input)")
# ---- C2d: tracer in the law's deep baryon field + its own Newtonian self-gravity, SIS ansatz
Vf = sp.symbols("V_f", positive=True)
bal = sp.simplify(sig ** 2 * 2 / r - (Vf ** 2 / r + 2 * sig ** 2 / r))       # isothermal balance for rho ~ r^-2
P(f"  C2d self-gravitating tracer in law field: SIS balance residual = {bal}  -> requires V_f = 0 (no SIS)")
slope_tracer = -Vf ** 2 / sig ** 2
P(f"  C2d non-self-gravitating tracer: log-slope = {slope_tracer}  (= -2 only if sigma^2 = V_f^2/2 is CHOSEN)")
# ---- C3b: vacuum stress boundary P = a0^2/(8 pi G) on an SIS
Psis = rho_sis * sig ** 2
rcap = sp.solve(sp.Eq(Psis, a0s ** 2 / (8 * sp.pi * Gs)), r)[0]
Mcap = sp.simplify(Msis.subs(r, rcap))
c3b_identity = sp.simplify(sig ** 4 - Gs * Mcap * a0s / 4) == 0
P(f"  C3b r_cap = {rcap}; M_SIS(<r_cap) = {Mcap}; sigma^4 = G M_SIS(<r_cap) a0/4 for EVERY sigma: {c3b_identity}")
results["sympy"] = {"C2c_minimiser": str(c2c_min), "C2d_balance_residual": str(bal), "C3b_rcap": str(rcap),
                    "C3b_identity_all_sigma": bool(c3b_identity), "C5_lambdaJ2": "2 pi^2 r^2 (sigma-free)"}

# ---- c-scaling theorem (dimensional): sigma^4 / (G M sqrt(G rho_L)) has units of velocity; target = kappa c / 4
P("\n[c-test] target sigma_t^4 = G M_b kappa c sqrt(G rho_L)/4 is LINEAR in c.  A mechanism built only from")
P("  Newtonian gravity + Lambda (G, masses, radii, energies, H, rho_L) is c-independent -> d ln sigma^4/d ln c = 0.")
U_req = KB * 0  # placeholder to keep namespace tidy
U_req = C.KAPPA * CL / 4.0
P(f"  required universal velocity U = sigma^4/(G M_b sqrt(G rho_L)) = kappa c/4 = {U_req/1e3:.0f} km/s for every galaxy")

# =====================================================================================================  K2 Emden spiral
P("\n[K2 / C1b] Emden isothermal spiral (self-gravitating, no baryons, box): G = M = R = 1")


def emden(xmax=2e4):
    def f(x, y):
        psi, dpsi = y
        return [dpsi, math.exp(-psi) - 2 * dpsi / x] if x > 0 else [0, 1 / 3.0]
    x0 = 1e-6
    sol = solve_ivp(f, (x0, xmax), [x0 ** 2 / 6, x0 / 3], rtol=1e-10, atol=1e-12, dense_output=True, method="DOP853")
    return sol


em = emden()


def lam_and_S(xR):
    """bounded isothermal truncated at xi_R, rescaled to G = M = R = 1: return lambda = RE/(GM^2), contrast, entropy."""
    xs = np.linspace(1e-6, xR, 40001)
    psi = em.sol(xs)[0]
    dpsi = em.sol(xs)[1]
    m_dimless = xs ** 2 * dpsi                      # M(xi) / (4 pi rho0 r0^3)
    r0 = 1.0 / xR
    rho0 = 1.0 / (4 * math.pi * r0 ** 3 * m_dimless[-1])
    s2 = 4 * math.pi * rho0 * r0 ** 2               # sigma^2 = 4 pi G rho0 r0^2
    rr = xs * r0
    rho = rho0 * np.exp(-psi)
    Mr = 4 * math.pi * rho0 * r0 ** 3 * m_dimless
    dM = 4 * math.pi * rr ** 2 * rho
    W = -TRAP(np.where(rr > 0, Mr / np.maximum(rr, 1e-300), 0) * dM, rr)
    K = 1.5 * s2
    lam = K + W
    S = TRAP(rho * (1.5 * math.log(2 * math.pi * s2) + 1.5 - np.log(rho)) * 4 * math.pi * rr ** 2, rr)
    return lam, math.exp(psi[-1]), S, s2


xg = np.logspace(-0.5, 3.3, 900)
lams = np.array([lam_and_S(x)[0] for x in xg])
imin = int(np.argmin(lams))
lam_min, D_min = lams[imin], lam_and_S(xg[imin])[1]
# refine
from scipy.optimize import minimize_scalar  # noqa: E402
ref = minimize_scalar(lambda lx: lam_and_S(10 ** lx)[0], bracket=(math.log10(xg[imin - 3]), math.log10(xg[imin]),
                                                                    math.log10(xg[imin + 3])))
lam_min = ref.fun
D_min = lam_and_S(10 ** ref.x)[1]
K2a = abs(lam_min + 0.335) / 0.335 < 0.01 and abs(D_min - 709) / 709 < 0.03
lam_tail = lams[-1]
P(f"  min lambda = {lam_min:.4f} at contrast {D_min:.1f} (Antonov -0.335, 709); lambda at xi=2000: {lam_tail:.4f} (SIS -1/4)")
# entropy at the SIS energy lambda = -1/4: first (low-contrast) branch vs the SIS
x1 = brentq(lambda x: lam_and_S(x)[0] + 0.25, 0.5, xg[imin])
lam1, D1, S1, s21 = lam_and_S(x1)
# SIS: sigma^2 = 1/2, rho = 1/(4 pi r^2), r in (0,1]
rr = np.linspace(1e-9, 1, 400001)
rho_s = 1 / (4 * math.pi * rr ** 2)
S_sis = TRAP(rho_s * (1.5 * math.log(2 * math.pi * 0.5) + 1.5 - np.log(rho_s)) * 4 * math.pi * rr ** 2, rr)
P(f"  at lambda = -1/4: low-contrast equilibrium (contrast {D1:.2f}, sigma^2 {s21:.4f}) S = {S1:.4f};  SIS (sigma^2 0.5) S = {S_sis:.4f}")
C1b_SIS_is_max = S_sis >= S1
P(f"  -> SIS is the entropy maximum at its own energy: {C1b_SIS_is_max}  (Lynden-Bell & Wood: the SIS is the spiral centre, unstable)")
K2 = bool(K2a and abs(lam_tail + 0.25) < 0.01)
results["controls"]["K2"] = K2
results["C1b"] = {"lambda_min": lam_min, "contrast_at_min": D_min, "S_low_contrast": S1, "S_SIS": S_sis,
                  "contrast_low": D1, "SIS_is_entropy_max": bool(C1b_SIS_is_max)}

# =====================================================================================================  MOND isothermal
P("\n[K3 / C2b] isothermal cold fluid when the law's action acts on ALL real mass (units G = a0 = M_b = 1)")


def mond_iso(sig2, rho0, a_h, kernel, mb=1.0, rmax=1e6):
    """isothermal sphere; g = nu(g_N) g_N with g_N from Hernquist baryons (mass mb, scale a_h) + cold fluid."""
    def f(lr, y):
        rr = math.exp(lr)
        lnrho, Mc = y
        Mbr = mb * rr ** 2 / (rr + a_h) ** 2 if mb > 0 else 0.0
        gN = (Mbr + Mc) / rr ** 2
        g = float(kernel(np.array([gN]))[0]) * gN
        rho = math.exp(lnrho)
        return [-g * rr / sig2, 4 * math.pi * rr ** 3 * rho]
    r0 = 1e-5
    sol = solve_ivp(f, (math.log(r0), math.log(rmax)), [math.log(rho0), 4 / 3 * math.pi * rho0 * r0 ** 3],
                    rtol=1e-9, atol=1e-14, method="LSODA", dense_output=True)
    lnrho_end, Mc_end = sol.y[0, -1], sol.y[1, -1]
    # tail beyond rmax: rho ~ r^-alpha with alpha = g r/sigma^2
    rr = rmax
    Mbr = mb
    gN = (Mbr + Mc_end) / rr ** 2
    alpha = float(kernel(np.array([gN]))[0]) * gN * rr / sig2
    tail = 4 * math.pi * math.exp(lnrho_end) * rr ** 3 / (alpha - 3) if alpha > 3 else float("inf")
    if not (alpha > 3.0):
        tail = float("inf")
    return Mc_end + tail, sol, alpha


deep = lambda y: np.maximum(y, 1e-300) ** -0.5  # noqa: E731
# K3: pure deep, no baryons: sigma^4 / M -> 4/81 for any rho0
k3 = []
for rho0 in (1e-3, 1e-1):
    Mtot_k3, _, alpha_k3 = mond_iso(1.0, rho0, 1.0, deep, mb=0.0, rmax=1e8)
    k3.append(1.0 / Mtot_k3)
K3 = all(abs(q / (4 / 81) - 1) < 0.02 for q in k3)
P(f"  K3 deep-MOND isothermal, no baryons: sigma^4/(G M a0) = {', '.join(f'{q:.5f}' for q in k3)}  (4/81 = {4/81:.5f})  PASS={K3}")
results["controls"]["K3"] = {"pass": bool(K3), "Q": k3}

nu = C.nu_mono
c2b_rows = []
for a_h in (0.3, 1.0):
    for rho0 in (1e-3, 1e-2, 1e-1, 1.0, 10.0):
        def mass_minus(ls):
            return mond_iso(math.exp(ls), rho0, a_h, nu)[0] - SHARE
        try:
            ls = brentq(mass_minus, math.log(0.01), math.log(20.0), xtol=1e-7)
        except ValueError:
            P(f"  a={a_h} rho0={rho0}: no sigma gives Mc = {SHARE}")
            continue
        s2 = math.exp(ls)
        Mt, sol, alpha = mond_iso(s2, rho0, a_h, nu)
        Mfin = float(sol.y[1, -1])
        tailfrac = 1.0 - Mfin / Mt if np.isfinite(Mt) else 1.0
        if not (alpha > 3.1 and tailfrac < 0.02 and abs(Mt - SHARE) < 1e-3):
            P(f"  a={a_h} rho0={rho0}: root rejected (far slope -{alpha:.2f}, tail fraction {tailfrac:.3f}): spurious (alpha -> 3 pole)")
            continue
        lr = np.log(np.array([2.0, 5.0]))
        lnr = sol.sol(lr)[0]
        slope = (lnr[1] - lnr[0]) / (lr[1] - lr[0])
        ratio = s2 ** 2 / 0.25               # sigma^4 / (G M_b a0 / 4)
        Q = s2 ** 2 / (1 + SHARE)
        c2b_rows.append(dict(a=a_h, rho0=rho0, sigma2=s2, slope_2_5=slope, ratio=ratio, Q_tot=Q, alpha_far=alpha,
                             tail_fraction=tailfrac))
        P(f"  a={a_h:3.1f} rho0={rho0:7.0e}: sigma^2={s2:.4f}  slope[2,5 r_M]={slope:+.3f}  "
          f"sigma^4/target={ratio:.3f} ({math.log10(ratio):+.3f} dex)  sigma^4/(G M_tot a0)={Q:.4f}  far slope -{alpha:.2f}")
results["C2b_rows"] = c2b_rows

# =====================================================================================================  per-galaxy numbers
P("\n[numbers] three galaxies x two footings")


def r_M(mb, a0):
    return math.sqrt(G * mb / a0)


def redge(mb, a0):
    return r_M(mb, a0) / math.log(1 / (1 - FB))


def sig4_R0(mb, a0, cs=1.0):
    a0e = a0 * cs
    m, a = mech_inputs(mb, a0e)
    R_ = redge(m, a)
    return (G * m * (1 + SHARE) / (2 * R_)) ** 2


def sig4_R0_coldonly(mb, a0, cs=1.0):
    m, a = mech_inputs(mb, a0 * cs)
    return (G * m * SHARE / (2 * redge(m, a))) ** 2


def R_ta(mtot, zc):
    rho_ta = (9 * math.pi ** 2 / 16) * OM * RHO_CRIT0 * (2 ** (2 / 3) * (1 + zc)) ** 3
    return (3 * mtot / (4 * math.pi * rho_ta)) ** (1 / 3)


def sig4_C4(mb, a0, zc, cs=1.0):        # c-free: cs unused by construction (no c in Newtonian collapse)
    m, _ = mech_inputs(mb, a0)
    mt = m / FB
    Rv = 5 / 12 * R_ta(mt, zc)
    return (G * mt / (2 * Rv)) ** 2


def sig4_C4_r200(mb, a0, zc, cs=1.0):
    m, _ = mech_inputs(mb, a0)
    mt = m / FB
    rho = 200 * RHO_CRIT0 * (OM * (1 + zc) ** 3 + 1 - OM)
    R2 = (3 * mt / (4 * math.pi * rho)) ** (1 / 3)
    return (G * mt / (2 * R2)) ** 2


def sig4_C2b(mb, a0, cs=1.0, Q=None):
    m, a = mech_inputs(mb, a0 * cs)
    return Q * G * m * (1 + SHARE) * a


T_U = lambda a: HBAR * a / (2 * math.pi * CL * KB)  # noqa: E731
# C3a best case: one particle mass tuned to the middle galaxy on the canonical footing (declared best case)
m_C3 = KB * T_U(A0["canonical"]) / math.sqrt(sig4_target(MB[1], A0["canonical"]))


def sig4_C3a(mb, a0, cs=1.0):
    m_, a = mech_inputs(mb, a0 * cs)
    cl = CL * cs
    s2 = HBAR * a / (2 * math.pi * cl * m_C3)       # Unruh temperature at a0 (mb does not enter)
    return s2 ** 2


Q_rep = [row["Q_tot"] for row in c2b_rows if row["a"] == 1.0]
Q_mid = float(np.median(Q_rep)) if Q_rep else float("nan")

mechs = {
    "C1a_LB_at_collapse_energy_zc1": lambda mb, a0, cs=1.0: sig4_C4(mb, a0, 1.0, cs),
    "C2a_heatflow_box_r200_z0": lambda mb, a0, cs=1.0: sig4_C4_r200(mb, a0, 0.0, cs),
    "C2b_law_on_all_mass_a1": lambda mb, a0, cs=1.0: sig4_C2b(mb, a0, cs, Q_mid),
    "C3a_unruh_bath_best_m": sig4_C3a,
    "C4_virial_zc0": lambda mb, a0, cs=1.0: sig4_C4(mb, a0, 0.0, cs),
    "C4_virial_zc1": lambda mb, a0, cs=1.0: sig4_C4(mb, a0, 1.0, cs),
    "C4_virial_zc3": lambda mb, a0, cs=1.0: sig4_C4(mb, a0, 3.0, cs),
    "R0_restatement_r_edge": sig4_R0,
    "R0_coldonly_r_edge": sig4_R0_coldonly,
}

num = {}
for name, fn in mechs.items():
    rows = {}
    for f in FOOTS:
        dex = [math.log10(fn(mb, A0[f]) / sig4_target(mb, A0[f])) for mb in MB]
        s4 = [fn(mb, A0[f]) for mb in MB]
        e_M = (math.log(s4[2]) - math.log(s4[0])) / (math.log(MB[2]) - math.log(MB[0]))
        e_c = (math.log(fn(MB[1], A0[f], 1.2)) - math.log(fn(MB[1], A0[f], 1.0))) / math.log(1.2)
        rows[f] = dict(dex=dex, e_M=e_M, e_c=e_c,
                       sigma_kms=[s ** 0.25 / 1e3 for s in s4],
                       target_kms=[sig4_target(mb, A0[f]) ** 0.25 / 1e3 for mb in MB])
    num[name] = rows
    for f in FOOTS:
        rw = rows[f]
        P(f"  {name:32s} {f:9s} dex(sigma^4/target) = {', '.join(f'{d:+.3f}' for d in rw['dex'])}  "
          f"dlns4/dlnMb={rw['e_M']:+.3f}  dlns4/dlnc={rw['e_c']:+.3f}  sigma[km/s]={', '.join(f'{s:.1f}' for s in rw['sigma_kms'])}"
          f" (target {', '.join(f'{s:.1f}' for s in rw['target_kms'])})")
results["numbers"] = num

# C3a: required particle mass per galaxy (Unruh at a0) and Gibbons-Hawking
P("\n[C3a] particle mass a0-Unruh / de Sitter baths would need (m = k T / sigma_t^2)")
H_L = math.sqrt(8 * math.pi * G * C.RHO_LAMBDA / 3)
c3 = {}
for f in FOOTS:
    mU = [KB * T_U(A0[f]) / math.sqrt(sig4_target(mb, A0[f])) * CL ** 2 / EV for mb in MB]
    mGH = [KB * (HBAR * H_L / (2 * math.pi * KB)) / math.sqrt(sig4_target(mb, A0[f])) * CL ** 2 / EV for mb in MB]
    c3[f] = dict(T_U_K=T_U(A0[f]), m_unruh_eV=mU, m_GH_eV=mGH, spread_dex=math.log10(mU[0] / mU[2]))
    P(f"  {f}: T_U(a0) = {T_U(A0[f]):.2e} K; m needed = {', '.join(f'{x:.2e}' for x in mU)} eV "
      f"(spread {math.log10(mU[0]/mU[2]):.2f} dex); Gibbons-Hawking: {', '.join(f'{x:.2e}' for x in mGH)} eV")
results["C3a"] = c3

# G-e: crossing time at r_edge
P("\n[G-e] crossing time r_edge / V_f (relaxation ~ few crossings)")
ge = {}
for f in FOOTS:
    tc = [redge(mb, A0[f]) / (G * mb * A0[f]) ** 0.25 / GYR for mb in MB]
    ge[f] = tc
    P(f"  {f}: r_edge = {', '.join(f'{redge(mb, A0[f])/KPC:.1f}' for mb in MB)} kpc; t_cross = {', '.join(f'{t:.2f}' for t in tc)} Gyr")
results["Ge_tcross_Gyr"] = ge
GE_time_ok = all(5 * t < 13.8 for f in FOOTS for t in ge[f])

# ---- POST-FREEZE REPORT (not a verdict input): how far must the virialised fluid contract to reach r_edge?
P("\n[post-freeze report, not a verdict input] SIS contraction factor R_vir/r_edge = (sigma^4_R0/sigma^4_C4)^(1/2);")
P("  the binding energy of a truncated SIS is G M^2/(4R), so the fluid must shed (R_vir/r_edge - 1) x its virial binding energy")
contr = {}
for zc in (0, 1, 3):
    for f in FOOTS:
        fac = [math.sqrt(sig4_R0(mb, A0[f]) / sig4_C4(mb, A0[f], float(zc))) for mb in MB]
        contr[f"zc{zc}_{f}"] = fac
        P(f"  z_c={zc} {f:9s}: R_vir/r_edge = {', '.join(f'{x:.2f}' for x in fac)}")
results["postfreeze_contraction_Rvir_over_redge"] = contr

# =====================================================================================================  gate table


def gb_numeric(name):
    """G-b parts 3 and 4 from the numbers."""
    ok3 = all(abs(d) <= TOL_DEX for f in FOOTS for d in num[name][f]["dex"])
    ok4 = all(0.9 <= num[name][f]["e_M"] <= 1.1 and 0.9 <= num[name][f]["e_c"] <= 1.1 for f in FOOTS)
    return ok3, ok4


c2b_shape = bool(c2b_rows) and all(-2.15 <= rw["slope_2_5"] <= -1.85 for rw in c2b_rows)
c2b_amp = bool(c2b_rows) and all(abs(math.log10(rw["ratio"])) <= TOL_DEX for rw in c2b_rows)

T = {}


def row(cls, Ga, Gb1, Gb2, name, Gc, Gd, Ge, note):
    ok3, ok4 = gb_numeric(name) if name else (False, False)
    if name and name.startswith("C2b"):
        Gb2 = c2b_shape
        ok3 = c2b_amp and ok3
    Gb = bool(Gb1 and Gb2 and ok3 and ok4)
    T[cls] = dict(G_a=Ga, G_b=Gb, G_b_parts=dict(output=Gb1, sis=Gb2, amplitude=ok3, scaling=ok4), G_c=Gc, G_d=Gd,
                  G_e=Ge, PASS=bool(Ga is True and Gb and Gc is True and Gd is True and Ge is True), note=note)


row("C1a Lynden-Bell (Newtonian, E from collapse)", True, True, True, "C1a_LB_at_collapse_energy_zc1", True, True,
    GE_time_ok, "sigma = multiplier set by E; c-free so dlns4/dlnc = 0; with E from collapse it is C4")
row("C1b LB entropy max in a box (no baryons)", True, False, bool(C1b_SIS_is_max), None, True, True, GE_time_ok,
    "at the SIS's own energy a cored state has higher entropy; sigma set by E")
row("C2a T10 mu-heat flow, conserved mass, cosmological box", True, True, True, "C2a_heatflow_box_r200_z0", False,
    True, GE_time_ok, "amplitude = M_c/(4 pi R): set by the box; T10's drift inserts the target's shape (G-c)")
row("C2b law's action on all real mass + entropy", True, True, False, "C2b_law_on_all_mass_a1", True, True, False,
    "sigma^4 ~ G M_tot a0 (selected) but not an SIS, M_tot not M_b (double count, A12); acts on all mass (growth)")
row("C2c mismatch functional |g_N[b+c]-g_law[b]|^2", True, True, True, None, False, True, None,
    "minimiser = rho_ph exactly, because g_law is inserted; G-a holds only if the supply equals M_ph(<r_edge); G-e not scorable (static)")
row("C2d tracer in law field + Newtonian self-gravity", True, False, False, None, True, True, None,
    "self-gravitating: no SIS; tracer: slope -V_f^2/sigma^2, sigma free (A11 reaction)")
row("C3a Unruh/de Sitter bath at a0", True, True, False, "C3a_unruh_bath_best_m", False, True, False,
    "universal T: sigma^2 independent of M_b; c cancels; needs a particle mass; acts everywhere")
row("C3b vacuum stress boundary a0^2/8piG", True, False, True, None, True, True, None,
    "identity sigma^4 = G M_SIS(<r_cap) a0/4 for every sigma: restates the BTFR as M_SIS(<r_cap) = M_b")
row("C4 cosmological virialisation z_c=0", True, True, True, "C4_virial_zc0", True, True, GE_time_ok,
    "sigma^4 ~ M^(4/3), c-free")
row("C4 cosmological virialisation z_c=1", True, True, True, "C4_virial_zc1", True, True, GE_time_ok, "")
row("C4 cosmological virialisation z_c=3", True, True, True, "C4_virial_zc3", True, True, GE_time_ok, "")
row("C5 Jeans marginality", True, False, True, None, True, True, None, "lambda_J^2 = 2 pi^2 r^2 for every sigma")
T["C6 phonon coupling (BK, fork arm a)"] = dict(G_a=None, G_b=None, G_c=False, G_d=False, G_e=None, PASS=False,
                                               note="NOT computed; fails G-d (direct dark-baryon coupling) and G-c (BK constants) by construction")
row("R0 RESTATEMENT r_edge (control)", True, False, True, "R0_restatement_r_edge", False, True, GE_time_ok,
    "r_edge is the law's own output: G-c fails by construction; G-b parts 2-4 must pass (K4)")
row("R0 cold-only variant", True, False, True, "R0_coldonly_r_edge", False, True, GE_time_ok, "sigma^2 = G M_c/(2 r_edge)")
results["classes"] = T

K4 = bool(T["R0 RESTATEMENT r_edge (control)"]["G_b_parts"]["amplitude"] and
          T["R0 RESTATEMENT r_edge (control)"]["G_b_parts"]["scaling"])
results["controls"]["K4"] = K4 if not MUT else "n/a in MUTATE"

P("\n[gate table]  (G-b parts: output / SIS / amplitude / scaling)")
for k, v in T.items():
    gb = v.get("G_b_parts")
    gbs = "/".join("Y" if gb[p] else "n" for p in ("output", "sis", "amplitude", "scaling")) if gb else "  -    "
    yn = lambda x: "PASS" if x is True else ("FAIL" if x is False else " -- ")  # noqa: E731
    P(f"  {k:52s} G-a {yn(v['G_a'])}  G-b {yn(v['G_b'])} [{gbs}]  G-c {yn(v['G_c'])}  G-d {yn(v['G_d'])}  "
      f"G-e {yn(v['G_e'])}  => {'PASS' if v['PASS'] else 'FAIL'}")
    if v["note"]:
        P(f"      {v['note']}")

cands = [k for k in T if not k.startswith("R0")]
any_pass = any(T[k]["PASS"] for k in cands)
verdict = "MECHANISM FOUND" if any_pass else "NO CLASS PASSES"
results["verdict"] = verdict
P(f"\nVERDICT: {verdict}")
P(f"controls: K1 {K1}  K2 {K2}  K3 {K3}  K4 {results['controls']['K4']}")

if MUT:
    all_fail_gb = all(not T[k]["G_b"] for k in T if T[k]["G_b"] is not None)
    P(f"MUTATE: every class and R0 fail G-b: {all_fail_gb}  (R0 amplitude/scaling under MUTATE: "
      f"{T['R0 RESTATEMENT r_edge (control)']['G_b_parts']})")
    results["mutate_detected"] = bool(all_fail_gb)
    rc = 1 if all_fail_gb else 0
else:
    rc = 0 if (K1 and K2 and K3 and K4) else 1


def jclean(o):
    if isinstance(o, dict):
        return {k: jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    return o


json.dump(jclean(results), open(os.path.join(HERE, f"cfg461_results{TAG}.json"), "w"), indent=1)
P(f"exit {rc}")
OUT.close()
sys.exit(rc)
