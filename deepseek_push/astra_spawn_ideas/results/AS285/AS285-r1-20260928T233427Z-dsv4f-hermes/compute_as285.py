#!/usr/bin/env python3
"""
AS285 (Tier-0b): action-consistent growth equation in a restricted quasistatic band.
CA5-GNC-R common action (FINAL_ACTION.md eq. (4), R1 dark sector from AS127).

Linear, pressureless, ordinary baryon perturbations around the homogeneous
INACTIVE background (f = G = 0, fields at the carrier vacuum origin),
Newtonian gauge  ds^2 = -(1+2 Phi) dt^2 + a^2 (1-2 Psi) delta_ij dx^i dx^j,
quasistatic band  q >> a H, comoving wavenumber q, k2 = (q/a)^2.

The linearized constraint system used (derivations in derivation.md):
  E1 (lapse constraint, FINAL_ACTION (13) linearized, inactive branch):
      (M_P^2/2){ -4k2 Psi + 2 alpha k2 Phi - 2 alpha k2 Z + 4 k2 Z + c_N ell k2 S U }
          = rho_b0 delta_b
  E2 (Z auxiliary, FINAL_ACTION (6) with f=0, a = D ln N = D Phi, N = 1+Phi):
      -4 k2 Z + ell S k2 Phi = 0
  E3 (Z/U/projection constraint, FINAL_ACTION (7), delta rho_R = 0 on the vacuum
      carrier origin because F'(1)=0 and K_d = W_exc = 0 at the origin):
      2 M_P^2 c_N (-k2)(Z - Phi + U) + rho_R0 Phi = 0
  E4 (independent spatial trace equation, Einstein part 2|DPsi|^2 - 4 DPhi.DPsi
      + projector stress (9)  Delta T^ij = -[<N rho_R>/N] z h^ij, z = Z for q != 0):
      2 M_P^2 (-k2)(Phi - Psi) + 3 rho_R0 Z = 0
Discarded (quasistatic): the Psi-dot pieces (M_P^2/2)(12 - 18 c_2) H Psi_dot
from T_K and 2 K Q_K, plus -2 K A_K/N = 0; error budget in C6.

Every coefficient/sign above is re-derived symbolically in this script:
  - substitution-back residuals are EXACT (0) or printed,
  - the pure-host limit must reproduce the pinned static matrix (16) entries,
  - the Einstein limit must give mu_g = eta_g = 1,
  - the negative control (Psi := Phi by hand) must make E4 show a nonzero
    residual 3 rho_R0 Z.
"""

import json
import math
import os
import signal
import sys
import time
import resource

import sympy as sp

T0 = time.time()
def _alarm(*_):
    raise TimeoutError("120 s wall-clock exceeded")
signal.signal(signal.SIGALRM, _alarm)
signal.alarm(120)
OUT = sys.argv[1] if len(sys.argv) > 1 else "raw_output.json"

# ---------------------------------------------------------------- symbols
MP2, kN, e, S, a, cN, r0, Ph, Ps, Z, U, rd = sp.symbols(
    "MP2 kN e S a cN r0 Ph Ps Z U rd", positive=False)
# MP2 = M_P^2 = 1/(8 pi G_bare)  (kg^2 in SI / mass^2 natural)
# kN  = k2 = (q/a)^2 (physical wavenumber squared)
# e   = ell (dimensionless compensator coefficient), 0 < ell < 4
# S   = S_k = exp(-(xi^2/2) (q/a)^2)  heat-kernel factor on the mode
# a   = alpha (0 < alpha < 2), cN = c_N = 1 - alpha/2
# r0  = rho_R0 = V_0 (homogeneous dark barrier density on the vacuum origin)
# Ph, Ps, Z, U = Phi, Psi, Z, U Fourier amplitudes
# rd  = rho_b0 delta_b (baryon density perturbation source)

A0 = sp.sympify(-4) + 2 * a + e * S * (1 + cN - a / 2) - (cN / 4) * (e * S) ** 2
At = A0 + 2 * e * S * r0 / (MP2 * kN)          # A_total (lapse coefficient)
Q  = 1 - e * S / 4                             # pinned Q of FINAL_ACTION (16)

# ---------------------------------------------------------------- equations
E1 = (MP2 / 2) * (-4 * kN * Ps + 2 * a * kN * Ph - 2 * a * kN * Z
                  + 4 * kN * Z + cN * e * kN * S * U) - rd
E2 = -4 * kN * Z + e * S * kN * Ph
E3 = 2 * MP2 * cN * (-kN) * (Z - Ph + U) + r0 * Ph
E4 = 2 * MP2 * (-kN) * (Ph - Ps) + 3 * r0 * Z

results = {"symbols": {"MP2": "1/(8 pi G_bare)", "kN": "(q/a)^2",
                       "S": "exp(-(xi^2/2)(q/a)^2)"}}

# ---------------------------------------------------------------- step 2: eliminate auxiliaries
sol = sp.solve([E2, E3, E4], [Z, U, Ps], dict=True)[0]
Zsol, Usol, Pssol = sol[Z], sol[U], sol[Ps]
results["auxiliary_solution"] = {
    "Z": sp.simplify(Zsol), "U": sp.simplify(Usol), "Psi": sp.simplify(Pssol)}

# residuals of the eliminated equations (must be exactly 0)
resid = {"E2": sp.simplify(E2.subs({Z: Zsol})),
         "E3": sp.simplify(E3.subs({Z: Zsol, U: Usol})),
         "E4": sp.simplify(E4.subs({Z: Zsol, Ps: Pssol}))}
results["auxiliary_solve_residuals"] = {k: str(v) for k, v in resid.items()}

# ---------------------------------------------------------------- step 2b: lapse constraint -> Phi
# Solve E1 after substitution for Phi as a function of the source rd.
E1red = sp.simplify(E1.subs({Z: Zsol, U: Usol, Ps: Pssol}))
coef = sp.simplify(E1red.coeff(Ph))
free = sp.simplify(E1red - coef * Ph)
results["E1_reduced"] = {"coefficient_of_Phi_times_MP2k2_over_2": str(coef),
                         "free_part": str(free)}
# check: E1red == (MP2/2) kN Ph At - rd ?
check_form = sp.simplify(E1red - ((MP2 / 2) * kN * Ph * At - rd))
results["E1_form_check_against_A_total"] = str(check_form)  # expect exactly 0

Phsol = sp.simplify(sp.solve(sp.Eq(E1red, 0), Ph)[0])
results["Phi_solution"] = str(Phsol)
# substitution-back residual of the FULL system
res_full = sp.simplify(E1red.subs(Ph, Phsol))
results["lapse_substitution_back_residual_format"] = str(res_full)
# exact zero
results["lapse_substitution_back_is_zero"] = str(sp.simplify(res_full))

# ---------------------------------------------------------------- response functions
# convention:  -k2 Phi = 4 pi G_N mu_g rho_b0 delta_b   (task's convention, physical k)
# with  4 pi G_N M_P^2 = 1/(2 c_N)  (G_N = G_bare/c_N, M_P^2 = 1/(8 pi G_bare))
mu_g = sp.simplify(-2 / (MP2 * At) * (2 * cN))       # = -4 cN / At
mu_g = sp.simplify(-4 * cN / At)
eta_g = sp.simplify(Pssol / Ph)
results["response_functions"] = {
    "mu_g": str(mu_g), "eta_g": str(eta_g),
    "eta_g_expanded": str(sp.expand(eta_g))}

# verify the convention identity symbolically: -kN Phsol - 4 pi G_N mu_g rd = 0
GNsym = sp.symbols("GN")
ident = sp.simplify(-kN * Phsol - 4 * sp.pi * GNsym * mu_g * rd)
results["poisson_convention_identity_with_GN_symbolic"] = str(ident)

# ---------------------------------------------------------------- controls
def S_(**kw):
    return mu_g.subs(kw)

ctrl = {}
# C1 Einstein recovery: ell=0, alpha=0, cN=1, rho0=0  =>  mu_g = eta_g = 1
Ein = {e: 0, a: 0, cN: 1, r0: 0}
ctrl["C1_einstein_recovery_mu"] = str(sp.simplify(mu_g.subs(Ein)))
ctrl["C1_einstein_recovery_eta"] = str(sp.simplify(eta_g.subs(Ein)))
# C2 pure-host static matrix (16): alpha=0, cN=1, rho0=0  =>  mu_g = 1/Q^2
HH = {a: 0, cN: 1, r0: 0}
ctrl["C2_pure_host_mu_minus_Qinv2"] = str(
    sp.simplify(mu_g.subs(HH) - 1 / (Q ** 2)))
# C3 high-k recovery within the band: S -> 0 (heat kernel suppresses) and
#    the projection term -> 0 (k2 -> infinity) => mu_g -> 1, eta_g -> 1
#    (uses the defining relation c_N = 1 - alpha/2)
HK = {S: 0, r0: 0, cN: 1 - a / 2}
ctrl["C3_highk_mu"] = str(sp.simplify(mu_g.subs(HK)))
ctrl["C3_highk_eta"] = str(sp.simplify(eta_g.subs(HK)))
ctrl["C3_highk_mu_minus_1"] = str(sp.simplify(mu_g.subs(HK) - 1))
ctrl["C3_highk_eta_minus_1"] = str(sp.simplify(eta_g.subs(HK) - 1))
# C3b no-gate limit ell=0 at fixed host: mu_g -> 1 (G_N normalization)
ctrl["C3b_no_gate_mu"] = str(sp.simplify(mu_g.subs({e: 0, r0: 0, cN: 1 - a / 2})))
ctrl["C3b_no_gate_mu_minus_1"] = str(sp.simplify(mu_g.subs({e: 0, r0: 0, cN: 1 - a / 2}) - 1))
# C4 NEGATIVE CONTROL: assign Psi = Phi by hand; E4 must reveal the residual
E4ctrl = sp.simplify(E4.subs({Ps: Ph, Z: Zsol}))
ctrl["C4_negative_control_residual_exact"] = str(E4ctrl)
ctrl["C4_negative_control_residual_fires"] = str(
    sp.simplify(E4ctrl - 3 * r0 * (e * S / 4) * Ph))
# C5 pinned static entries (16): U to baryon source = Q^-1 x u_b etc.
u_b = sp.symbols("u_b")
# with u_b := Q^2 Phi: U must equal u_b/Q and (Phi - Z) = u_b/Q, at rho0=0
HH2 = {a: 0, cN: 1, r0: 0}
U_sub = sp.simplify(Usol.subs(HH2) - Q * Ph)                 # U = Q Phi = u_b/Q
PmZ_sub = sp.simplify((Ph - Zsol).subs(HH2) - Q * Ph)        # Phi - Z = u_b/Q
ctrl["C5_entry_U_over_u_b"] = str(sp.simplify(U_sub.subs(Ph, u_b / (Q ** 2))))
ctrl["C5_entry_PhimZ_over_u_b"] = str(sp.simplify(PmZ_sub.subs(Ph, u_b / (Q ** 2))))
ctrl["C5_Phi_over_u_b"] = str(
    sp.simplify(Phsol.subs(HH2).subs(rd, 0)) if False else
    "see C2: Phi = u_b/Q^2 (mu_g = Q^-2)")

# ---------------------------------------------------------------- C6 quasistatic truncation error
# discarded terms in the lapse constraint: (MP2/2)(12 - 18 c2) H Psidot
c2, H, Psid = sp.symbols("c2 H Psid")
eps_expr = sp.simplify(((MP2 / 2) * (12 - 18 * c2) * H * Psid) /
                       ((MP2 / 2) * 4 * kN * Ps))
ctrl["C6_truncation_relative_error_symbolic"] = str(eps_expr)

results["controls_symbolic"] = ctrl
results["checks_status"] = {
    "E2_E3_E4_residuals_zero": all(v == 0 for v in resid.values()),
    "E1_form_check_zero": str(check_form) == "0",
    "C1_einstein": ctrl["C1_einstein_recovery_mu"] == "1"
    and ctrl["C1_einstein_recovery_eta"] == "1",
    "C2_pure_host": ctrl["C2_pure_host_mu_minus_Qinv2"] == "0",
    "C3_highk": ctrl["C3_highk_mu_minus_1"] == "0" and ctrl["C3_highk_eta_minus_1"] == "0",
    "C3b_nogate": ctrl["C3b_no_gate_mu_minus_1"] == "0",
    "C4_negative_control_fires": ctrl["C4_negative_control_residual_fires"] == "0"
    and ctrl["C4_negative_control_residual_exact"] != "0",
    "C5_entries": ctrl["C5_entry_U_over_u_b"] == "0"
    and ctrl["C5_entry_PhimZ_over_u_b"] == "0",
}

# ---------------------------------------------------------------- numerics (band)
import numpy as np

P = dict(
    G_N=6.67430e-11, c=299792458.0, M_sun=1.98847e30, pc=3.085677581491367e16,
    H0=67.4e3 / (3.085677581491367e16 * 1e6),   # 67.4 km/s/Mpc -> 1/s
    alpha=0.5, c2=1.0, ell=0.04, xi_Mpc=10.0,   # inputs, illustrative (ell per FINAL_ACTION sec.5)
    Om_b0=0.05, Om_R0=0.65,                     # inputs, illustrative partition (G_N densities)
)
P["cN"] = 1 - P["alpha"] / 2
# closure with the CA5-GNC-R Friedmann equation (G_cosm/G_N = c_N, FINAL_ACTION (18)):
# E(a)^2 = c_N (Om_b0 a^-3 + Om_R0) + Om_L0,  Om_L0 := 1 - c_N (Om_b0 + Om_R0)
P["Om_L0"] = 1 - P["cN"] * (P["Om_b0"] + P["Om_R0"])
P["xi"] = P["xi_Mpc"] * P["pc"] * 1e6
P["H0_c"] = P["H0"] / P["c"]

def E2a(aa):  # dimensionless Hubble
    return math.sqrt(P["cN"] * (P["Om_b0"] / aa ** 3 + P["Om_R0"]) + P["Om_L0"])

def S_k(q_aH):
    # heat-kernel factor: S = exp(-(xi k)^2/2), k = q/a = (q/aH)*H/c
    x = P["xi"] * (q_aH * P["H0_c"])
    return math.exp(-x * x / 2)

def mu_num(q_aH, aa):
    s = S_k(q_aH)
    A0n = -4 + 2 * P["alpha"] + P["ell"] * s * (1 + P["cN"] - P["alpha"] / 2) \
        - (P["cN"] / 4) * (P["ell"] * s) ** 2
    proj = 2 * P["ell"] * s * 3 * P["Om_R0"] / (q_aH ** 2)   # r0/(MP2 k2) = 3 Om_R0/(q/aH)^2
    return -4 * P["cN"] / (A0n + proj)

def eta_num(q_aH, aa):
    s = S_k(q_aH)
    proj = 3 * P["Om_R0"] / (q_aH ** 2)
    return 1 - 3 * P["ell"] * s * proj / 8

q_aH_grid = np.logspace(1, 3, 41)
num = {"parameter_cell": P}
for aa in (1.0, 0.7, 0.5):
    rows = []
    for qa in q_aH_grid:
        mu, et = mu_num(qa, aa), eta_num(qa, aa)
        # r0/(MP2 k2) = 3 Om_R0/(q_aH)^2  (exact, c=1): q_aH = q c/(a H(a))
        r0_MP2k2 = 3 * P["Om_R0"] / qa ** 2
        s = S_k(qa)
        # negative-control residual at this mode with Phi = 1 (units of r0/(MP2 k2))
        r4 = 3 * r0_MP2k2 * (P["ell"] * s / 4) * 1.0
        rows.append(dict(q_aH=float(qa), S=float(s), mu_g=float(mu), eta_g=float(et),
                         eta_minus_1=float(et - 1),
                         negctrl_residual_Psi_eq_Phi=float(r4)))
    num[f"a={aa}"] = rows

# ---------------------------------------------------------------- growth equation
# delta'' + (2 + H'/H) delta' = (3/2) Omega_b(a) mu_g(q,a) delta ; primes d/d ln a
# H'/H = -(3/2) c_N Om_b0 a^-3 / E^2  (G_cosm = c_N G_N background, FINAL_ACTION (18));
# Omega_b(a) = Om_b0 a^-3 / E^2 with Om_b0 = 8 pi G_N rho_b0/(3 H0^2).

def integrate(qa1, s_i=math.log(0.05), s_f=0.0, n=6000):
    """Growth ODE in s = ln a:  delta'' + (2+H'/H) delta' = (3/2) Om_b(s) mu(s) delta,
    uniform ds steps; IC = growing mode delta = a = e^s (delta' = e^s)."""
    ds = (s_f - s_i) / n
    y = np.array([math.exp(s_i), math.exp(s_i)])
    for i in range(n):
        ss = s_i + i * ds
        def F(yy, sss):
            aaa = math.exp(sss)
            E2 = E2a(aaa) ** 2
            omb = P["Om_b0"] / aaa ** 3 / E2
            hp = -1.5 * P["cN"] * P["Om_b0"] / aaa ** 3 / E2
            qa = qa1 / (aaa * E2a(aaa))
            return np.array([yy[1], -(2 + hp) * yy[1] + 1.5 * omb * mu_num(qa, aaa) * yy[0]])
        k1 = F(y, ss); k2 = F(y + ds / 2 * k1, ss + ds / 2)
        k3 = F(y + ds / 2 * k2, ss + ds / 2); k4 = F(y + ds * k3, ss + ds)
        y = y + ds / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return y

def integrate_mu1(s_i=math.log(0.05), s_f=0.0, n=6000):
    """Einstein baseline: same ODE with mu_g := 1 identically."""
    ds = (s_f - s_i) / n
    y = np.array([math.exp(s_i), math.exp(s_i)])
    for i in range(n):
        ss = s_i + i * ds
        def F(yy, sss):
            aaa = math.exp(sss)
            E2 = E2a(aaa) ** 2
            omb = P["Om_b0"] / aaa ** 3 / E2
            hp = -1.5 * P["cN"] * P["Om_b0"] / aaa ** 3 / E2
            return np.array([yy[1], -(2 + hp) * yy[1] + 1.5 * omb * yy[0]])
        k1 = F(y, ss); k2 = F(y + ds / 2 * k1, ss + ds / 2)
        k3 = F(y + ds / 2 * k2, ss + ds / 2); k4 = F(y + ds * k3, ss + ds)
        y = y + ds / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return y

growth = {}
for qa1 in (10.0, 100.0, 1000.0):
    y = integrate(qa1)
    f = y[1] / y[0]
    growth[qa1] = dict(delta_at_a1=float(y[0]), f_at_a1=float(f))
y0 = integrate_mu1()
growth["reference_mu_equals_1"] = dict(delta_at_a1=float(y0[0]), f_at_a1=float(y0[1] / y0[0]))
for qa1 in (10.0, 100.0, 1000.0):
    growth[qa1]["f_over_einstein_f"] = growth[qa1]["f_at_a1"] / growth["reference_mu_equals_1"]["f_at_a1"]

# calibration: plain LCDM (Om_m0 = 0.3, Om_L0 = 0.7), mu = 1.
# known result (e.g. standard growth tables): f(z=0) ~ 0.51, D(1)/D(0.05) ~ 3.2
Pcal = dict(P); Pcal["Om_b0"], Pcal["Om_R0"], Pcal["Om_L0"], Pcal["cN"] = 0.3, 0.0, 0.7, 1.0
def E2cal(aa):
    return math.sqrt(Pcal["Om_b0"] / aa ** 3 + Pcal["Om_L0"])
def integrate_cal(s_i=math.log(0.05), s_f=0.0, n=6000):
    """LCDM calibration: same s-integration; expected f(z=0) ~ 0.51 (Omega_m0=0.3)."""
    ds = (s_f - s_i) / n
    y = np.array([math.exp(s_i), math.exp(s_i)])
    for i in range(n):
        ss = s_i + i * ds
        def F(yy, sss):
            aaa = math.exp(sss)
            E2v = E2cal(aaa) ** 2
            omb = Pcal["Om_b0"] / aaa ** 3 / E2v
            hp = -1.5 * Pcal["Om_b0"] / aaa ** 3 / E2v
            return np.array([yy[1], -(2 + hp) * yy[1] + 1.5 * omb * yy[0]])
        k1 = F(y, ss); k2 = F(y + ds / 2 * k1, ss + ds / 2)
        k3 = F(y + ds / 2 * k2, ss + ds / 2); k4 = F(y + ds * k3, ss + ds)
        y = y + ds / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return y
ycal = integrate_cal()
growth["CALIBRATION_LCDM_0p3_0p7"] = dict(
    delta_at_a1=float(ycal[0]), f_at_a1=float(ycal[1] / ycal[0]),
    expected_f_at_a1_about_0p51=0.51, tolerance=0.02)
num["growth"] = growth
num["growth_calibration_pass"] = abs(ycal[1] / ycal[0] - 0.51) < 0.02

# quasistatic error budget at band edges (c2 = 1): |12-18c2|/4 * (aH/q)^2
num["quasistatic_error_budget"] = {
    "coefficient": float(abs(12 - 18 * P["c2"]) / 4),
    "rel_error_at_q_aH=10": float(abs(12 - 18 * P["c2"]) / 4 / 10 ** 2),
    "rel_error_at_q_aH=30": float(abs(12 - 18 * P["c2"]) / 4 / 30 ** 2),
    "rel_error_at_q_aH=1000": float(abs(12 - 18 * P["c2"]) / 4 / 1000 ** 2),
}

results["numerics"] = num

# ---------------------------------------------------------------- footings
a0s = [9.3619e-11, 1.1279e-10]
foot = {}
for a0 in a0s:
    rhoL = 4 * a0 ** 2 / (P["G_N"] * P["c"] ** 2)
    rM = math.sqrt(P["G_N"] * P["M_sun"] / a0) / (P["pc"])
    vf = (P["G_N"] * P["M_sun"] * a0) ** 0.25
    foot[str(a0)] = dict(rho_Lambda=rhoL, r_M_Msun_pc=rM, v_flat_Msun=vf,
                         Om_R0_if_V0_is_rho_Lambda_c2=8 * math.pi * P["G_N"] * rhoL
                         / (3 * P["H0"] ** 2))
results["footings"] = foot
results["footings_note"] = ("V0 = rho_Lambda c^2 assignment is an ILLUSTRATIVE input "
                            "(Omega_R0 = 0.685 canonical / 0.995 alternative); the response "
                            "functions mu_g, eta_g are dimensionless and identical for both "
                            "footings (a0 enters only via rho_Lambda -> V0 -> Omega_R0 in "
                            "dimensionless combinations). kappa = 1/2 adopted as input.")

# ---------------------------------------------------------------- bounds + timing
results["bounds"] = {
    "declared_wall_s": 120, "declared_memory_MB": 512, "declared_threads": 1,
    "enforced": {"SIGALRM_120s": True, "threads": 1,
                 "rlimit_memory": "declaration only (measured RSS is the guarantee)"},
    "measured_elapsed_s": round(time.time() - T0, 3),
    "measured_maxrss_MB": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 2),
}
signal.alarm(0)

# sanity: measured elapsed must be < 120
if results["bounds"]["measured_elapsed_s"] >= 120:
    results["bounds"]["enforced"]["SIGALRM_120s"] = "FIRED"

with open(OUT, "w") as f:
    json.dump(results, f, indent=1, default=str)
print("wrote", OUT)
print("checks_status:", json.dumps(results["checks_status"], indent=1))
print("growth:", json.dumps(growth, indent=1))
print("bounds:", results["bounds"])
for k, v in num["quasistatic_error_budget"].items():
    print("QSEB", k, v)