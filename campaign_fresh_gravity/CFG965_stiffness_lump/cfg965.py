#!/usr/bin/env python3
"""CFG965: the stiffness-bound cold lump (NEW_ANGLES_SCOUT NA-3).

Part A (derivation): does any formulation on the record give SELF-GRAVITATING cold mass the stiffness pressure
p = (gamma/2) rho^2 = pi G L*^2 rho^2, so that an isolated lump is an n = 1 polytrope of edge R = pi L*/sqrt2?
Primary target: the screened theory v3 (Khronon + -(gamma_L/2)(D.P)^2, BS24 dust mass mu_K, J_x so that the static
limit is AQUAL mu = x/(1+x)). Part B (fit to CFG880's 83 dwarfs) runs only if Part A passes (FROZEN_CRITERIA.md s3).

Run:     OMP_NUM_THREADS=1 nice -n 10 python3 cfg965.py              -> cfg965.out, cfg965_results.json (exit 0 iff all pass)
Mutate:  CFG965_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg965.py -> cfg965_MUTATE.out, cfg965_results_MUTATE.json
         (removes the critical quadratic of the hold / tether, c2 = 0; must flip the outcome; exit 1 by design)

kappa = 1/2 FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s^2, never pooled. AQUAL only (no QUMOND, no EFE recipe).
Cold energy is gravitating mass, not a particle species. Not theory closed.
"""
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import json
import math
import resource

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

MUTATE = os.environ.get("CFG965_MUTATE", "0") == "1"
C2 = 0 if MUTATE else 1          # coefficient of the hold's critical quadratic (theorem D-T forces 1)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
TAG = "_MUTATE" if MUTATE else ""
OUT_TXT = os.path.join(HERE, f"cfg965{TAG}.out")
OUT_JSON = os.path.join(HERE, f"cfg965_results{TAG}.json")
RSS_LIMIT_GB = 1.0

lines = []
checks = {}
res = {"lane": "CFG965", "mutate": MUTATE, "criteria_commit": "40afd03902", "c2": C2}


def say(s=""):
    lines.append(s)
    print(s, flush=True)


def check(name, ok, value, thr):
    checks[name] = {"pass": bool(ok), "value": value, "threshold": thr}
    say(f"{name} {'PASS' if ok else 'FAIL'} {value} {thr}")


def rss_gb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e9 if sys.platform == "darwin" else r * 1024 / 1e9


def guard(stage):
    g = rss_gb()
    if g > RSS_LIMIT_GB:
        say(f"RSS GUARD: {g:.3f} GB > {RSS_LIMIT_GB} GB after {stage}; aborting")
        sys.exit(3)
    return g


def rel(path):
    return os.path.join(REPO, path)


def load(path):
    with open(rel(path)) as f:
        return json.load(f)


# ---------------------------------------------------------------------------------------------------------------------
# constants and record inputs (all read from committed files; string checks below confirm the text inputs)
G = 4.30091e-3            # pc (km/s)^2 / Msun
PC_M = 3.0857e16          # m per pc
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}   # m/s^2, never pooled
A0 = {f: v * PC_M / 1e6 for f, v in FOOT.items()}     # (km/s)^2 / pc
H_PRIMARY, H_BRACKET = 0.674, (0.55, 0.73)
MUK_CAP_H = 14.8          # h/Mpc, BS24 Eq. 39 cap (THEORY_V3_DRAFT line 48)
MUK_GROWTH_H = 411.0      # h/Mpc, M1 (THEORY_V3_DRAFT line 75), reported only
MUK_BBN_H = 1.84e8        # h/Mpc, Q6 literal-K BBN (line 79), reported only
MU_AEST_MAX = 1.0         # Mpc^-1, H2's constraint C3 (L_eq = sqrt2/mu >= 1.41 Mpc), v4 row
XI_HALF = None            # sin(xi)/xi = 1/2 root, computed in K1

cfg877 = load("campaign_fresh_gravity/CFG877_finite_cold_clump/cfg877_results.json")
cfg870 = load("campaign_fresh_gravity/CFG870_cored_component_joint/cfg870_results.json")
d10 = load("doors_push_2026_10_22/D10_native_Lstar/d10_native_lstar_results.json")
cfg938 = load("campaign_fresh_gravity/CFG938_medium_continuum_eft/cfg938_results.json")
RC870 = float(cfg870["rc"])
CL = {f: {"Mcl": float(cfg877[f]["Mcl_Msun"]), "rt": float(cfg877[f]["rt_pc"])} for f in FOOT}
LSTAR = {
    "canonical": {"D10_central": float(d10["band_cells"]["canonical|P1|E_mid"]["L95"]),
                  "E4_native": float(d10["K9_E4_N1"]["canonical"]), "top_90pc": 90.0, "soft_edge": 2040.0},
    "alt": {"D10_central": float(d10["band_cells"]["alt|P1|E_mid"]["L95"]),
            "E4_native": float(d10["K9_E4_N1"]["alt"]), "top_90pc": 90.0, "soft_edge": 2140.0},
}
res["inputs"] = {"a0_kms2_per_pc": A0, "rc870_pc": RC870, "cfg877": CL, "Lstar_pc": LSTAR,
                 "muK_cap_h_per_Mpc": MUK_CAP_H, "muK_growth_h_per_Mpc": MUK_GROWTH_H, "muK_BBN_h_per_Mpc": MUK_BBN_H,
                 "mu_AeST_max_per_Mpc": MU_AEST_MAX, "h_primary": H_PRIMARY, "h_bracket": H_BRACKET}

say(f"CFG965 stiffness-bound cold lump (NA-3). mutate={MUTATE} (hold critical-quadratic coefficient c2 = {C2})")
say("kappa = 1/2 FITTED; footings never pooled; AQUAL mu = x/(1+x) only; not theory closed")
say(f"inputs: rc870 {RC870} pc; CFG877 canonical Mcl {CL['canonical']['Mcl']:.4g} rt {CL['canonical']['rt']:.2f} pc; "
    f"alt Mcl {CL['alt']['Mcl']:.4g} rt {CL['alt']['rt']:.2f} pc")
say(f"inputs: L* canonical {LSTAR['canonical']}; alt {LSTAR['alt']}")
say()

# ---------------------------------------------------------------------------------------------------------------------
# K1  NA-3 hand numbers (scout appendix A3)
say("== K: reproductions")
xi = sp.symbols("xi", positive=True)
theta = sp.sin(xi) / xi
le_res = sp.simplify(sp.diff(theta, xi, 2) + 2 / xi * sp.diff(theta, xi) + theta)
XI_HALF = float(sp.nsolve(sp.sin(xi) / xi - sp.Rational(1, 2), xi, 1.9))
R_over_L = math.pi / math.sqrt(2)
half_over_L = XI_HALF / math.sqrt(2)
mass_int = sp.simplify(sp.integrate(4 * sp.pi * xi**2 * theta, (xi, 0, sp.pi)))   # in units alpha^3 rho_c
L_from_104 = 104.0 / half_over_L
L_from_200 = 200.0 / R_over_L
M_104 = float(mass_int) * (L_from_104 / math.sqrt(2))**3 * 0.6
M_200 = float(mass_int) * (L_from_200 / math.sqrt(2))**3 * 0.6
k1_hand = [abs(L_from_104 / 77.6 - 1), abs(L_from_200 / 90.0 - 1), abs(M_104 / 3.9e6 - 1), abs(M_200 / 6.1e6 - 1)]
k1_ok = (le_res == 0 and sp.simplify(mass_int - 4 * sp.pi**2) == 0 and abs(R_over_L - 2.2214) < 1e-4
         and abs(half_over_L - 1.3403) < 1e-4 and max(k1_hand) < 0.01)
res["K1"] = {"R_over_L": R_over_L, "half_over_L": half_over_L, "xi_half": XI_HALF, "L_from_104": L_from_104,
             "L_from_200": L_from_200, "M_104_rho0.6": M_104, "M_200_rho0.6": M_200}
check("K1_NA3_hand_numbers", k1_ok, f"R/L*={R_over_L:.4f} half/L*={half_over_L:.4f} L*={L_from_104:.1f},{L_from_200:.1f} "
      f"M={M_104:.3g},{M_200:.3g} maxdev={max(k1_hand):.4f}", "LE res 0; 1% on hand numbers")

# K2  NA-3 hydrostatic equation from the enclosed-mass functional
r = sp.symbols("r", positive=True)
Gs, gam, Ls = sp.symbols("G gamma L_s", positive=True)
Mf = sp.Function("M")(r)
f2 = -Gs * Mf**2 / (2 * r**2) + gam * sp.diff(Mf, r)**2 / (8 * sp.pi * r**2)
EL2 = sp.euler_equations(f2, Mf, r)[0].lhs
rho = sp.Function("rho")(r)
EL2_rho = sp.simplify(EL2.subs(sp.Derivative(Mf, (r, 2)), sp.diff(4 * sp.pi * r**2 * rho, r))
                      .subs(sp.Derivative(Mf, r), 4 * sp.pi * r**2 * rho))
target2 = -Gs * Mf / r**2 - gam * sp.diff(rho, r)       # gamma rho' = -G M / r^2
k2a = sp.simplify(EL2_rho - target2)
# differentiate gamma r^2 rho' = -G M:  gamma (r^2 rho')' = -4 pi G r^2 rho  -> lap rho + (4 pi G / gamma) rho = 0
lap = sp.diff(r**2 * sp.diff(rho, r), r) / r**2
k2b = sp.simplify((4 * sp.pi * Gs / gam).subs(gam, 2 * sp.pi * Gs * Ls**2) - 2 / Ls**2)
check("K2_NA3_hydrostatic", k2a == 0 and k2b == 0, f"EL residual {k2a}; 4piG/gamma - 2/L*^2 = {k2b}",
      "both exactly 0")

# K3  H4's v3 dispersion from H4's linear PN system (with the hold coefficient c2)
w, k, rho0, K, gL, muK, Mth = sp.symbols("omega k rho0 K gamma_L mu_K M_theta", positive=True)
dphi, dP, dsig, dXi, drho = sp.symbols("dphi dP dsigma dXi drho")
I = sp.I
M_eff = Mth - (1 - C2)          # longitudinal hold Hessian; c2 = 0 removes the critical quadratic (M -> M - 1)
eqs = [
    sp.Eq(-k**2 * dphi, K * drho),                                   # Poisson
    sp.Eq(drho, I * k * dP - muK**2 * dXi / K),                      # rho_tau = div P - mu_K^2 Xi / K
    sp.Eq(I * k * dXi, K * M_eff * dP + gL * k**2 * dP),             # P eq: grad Xi = hold - gamma_L grad div P
    sp.Eq(-I * w * drho + rho0 * k**2 * dsig, 0),                    # continuity, v = -grad sigma
    sp.Eq(dXi, dphi + I * w * dsig),                                 # Bernoulli: Xi = phi - sigma_t
]
A, _ = sp.linear_eq_to_matrix([e.lhs - e.rhs for e in eqs], [dphi, dP, dsig, dXi, drho])
w2s = sp.symbols("w2", positive=True)
detA = sp.simplify(A.det().subs(w**2, w2s))
w2_sol = sp.solve(sp.Eq(detA, 0), w2s)
chi = k**2 / (K * Mth + gL * k**2) + muK**2 / K
w2_record = rho0 * (k**2 / chi - K)                                   # H4 README
k3_res = sp.simplify(w2_sol[0] - w2_record) if w2_sol else sp.oo
w2_mu0_record = K * rho0 * (Mth - 1 + Ls**2 * k**2 / 2)              # H4 at mu_K = 0, gamma_L = K L*^2/2
k3_res0 = sp.simplify(w2_sol[0].subs(muK, 0).subs(gL, K * Ls**2 / 2) - w2_mu0_record) if w2_sol else sp.oo
check("K3_H4_v3_dispersion", k3_res == 0 and k3_res0 == 0, f"residuals {k3_res} / {k3_res0}", "exactly 0 (H4 README)")
W2_DERIVED = w2_sol[0] if w2_sol else None

# K4  H4 (mu_K = 0) == CFG938 S5a, via M_L - 1 = R', M_T - 1 = R/u
x, a0s, u = sp.symbols("x a0 u", positive=True)
Rfun = u**2 / (a0s - u)
uofx = a0s * x / (1 + x)
hold = C2 * u + Rfun                                  # full hold a0 u/(a0-u) when c2 = 1
ML_derived = sp.simplify(sp.diff(hold, u).subs(u, uofx))
MT_derived = sp.simplify((hold / u).subs(u, uofx))
Rp = sp.simplify(sp.diff(Rfun, u).subs(u, uofx))
Ru = sp.simplify((Rfun / u).subs(u, uofx))
k4_L = sp.simplify(ML_derived - 1 - Rp)
k4_T = sp.simplify(MT_derived - 1 - Ru)
k4_rec = sp.simplify((1 + x)**2 - 1 - Rp) == 0 and sp.simplify((1 + x) - 1 - Ru) == 0   # H4 A5: M_L=(1+x)^2, M_T=1+x
check("K4_H4_equals_CFG938", k4_L == 0 and k4_T == 0 and k4_rec,
      f"M_L-1-R' = {k4_L}; M_T-1-R/u = {k4_T}; record M_L,M_T forms ok={k4_rec}", "exactly 0")

# K5  CFG888 S4: (gamma/2)|grad P_L|^2 = (gamma/2) rho^2 + divergence (3-D, longitudinal P = grad chi / K)
X, Y, Z = sp.symbols("X Y Z")
chif = sp.Function("chi")(X, Y, Z)
co = [X, Y, Z]
hess2 = sum(sp.diff(chif, a, b)**2 for a in co for b in co)
lapc = sum(sp.diff(chif, a, 2) for a in co)
div_term = sum(sp.diff(sum(sp.diff(chif, b) * sp.diff(chif, a, b) for b in co) - sp.diff(chif, a) * lapc, a) for a in co)
k5 = sp.simplify(sp.expand(hess2 - lapc**2 - div_term))
k5b = sp.simplify((gam / 2).subs(gam, 2 * sp.pi * Gs * Ls**2) - sp.pi * Gs * Ls**2)
check("K5_CFG888_S4_stiffness_is_rho2", k5 == 0 and k5b == 0, f"identity residual {k5}; gamma/2 - pi G L*^2 = {k5b}",
      "exactly 0")

# K6  CFG888 S1: single-mode on-shell Lagrangian under ID has no C^2 term (the critical quadratic cancels self-gravity)
B, Cc, xx = sp.symbols("B C xx", real=True)
Pm = Cc / k * sp.sin(k * xx)                          # div P = rho_c = C cos kx
Phi_p = K * Pm + K * B / k * sp.sin(k * xx)          # (Phi' - K P)' = K rho_b
Phi = sp.integrate(Phi_p, xx)
# L = -|Phi'|^2/2K + P Phi' - c2 K|P|^2/2 - rho_b Phi  (c2 = 0: the critical quadratic is absent)
Lmode = (-(Phi_p)**2 / (2 * K) + Pm * Phi_p - C2 * K * Pm**2 / 2 - B * sp.cos(k * xx) * Phi)
Lavg = sp.simplify(sp.integrate(Lmode, (xx, 0, 2 * sp.pi / k)) / (2 * sp.pi / k))
cC2 = sp.simplify(sp.Poly(sp.expand(Lavg), Cc).coeff_monomial(Cc**2))
cBC = sp.simplify(sp.Poly(sp.expand(Lavg), Cc, B).coeff_monomial(Cc * B))
k6_ok = cC2 == 0 and sp.simplify(cBC - K / (2 * k**2)) == 0
check("K6_CFG888_S1_no_self_gravity", k6_ok, f"C^2 coeff {cC2}; BC coeff {cBC}", "C^2 = 0, BC = K/2k^2 (Newtonian)")
res["K_symbolic"] = {"w2_derived": str(W2_DERIVED), "ML_derived": str(ML_derived), "MT_derived": str(MT_derived),
                     "Lmode_avg": str(Lavg)}
say(f"   RSS {guard('K'):.3f} GB")
say()

# ---------------------------------------------------------------------------------------------------------------------
say("== D1: v3 exact nonlinear statics, mu_K = 0, spherical")
# v3 PN static Lagrangian (H4 A1 at mu_K = 0, Xi = phi + C, sigma static), radial, per dr, with 4 pi r^2 p = M:
#   Lr = -4 pi r^2 phi'^2/2K + (M + M_b) phi' - 4 pi r^2 W(G M / r^2) - 4 pi r^2 (gamma_L/2) D^2,  D = M'/(4 pi r^2)
Mb = sp.Function("M_b")(r)
php = sp.symbols("phip")
uM = Gs * Mf / r**2
Wsym = sp.Function("W")
Lr = (-4 * sp.pi * r**2 * php**2 / (2 * 4 * sp.pi * Gs) + (Mf + Mb) * php
      - 4 * sp.pi * r**2 * Wsym(uM) - gam / 2 * sp.diff(Mf, r)**2 / (4 * sp.pi * r**2))
php_on = sp.solve(sp.diff(Lr, php), php)[0]
Lr_on = sp.simplify(Lr.subs(php, php_on))
E938 = (-Gs * (Mb + Mf)**2 / (2 * r**2) + 4 * sp.pi * r**2 * Wsym(uM)
        + gam / 2 * sp.diff(Mf, r)**2 / (4 * sp.pi * r**2))          # CFG938 s3.4 E[M_c]
d1_id = sp.simplify(Lr_on + E938)
check("D1a_v3_statics_equal_CFG938_E", d1_id == 0 and sp.simplify(php_on - Gs * (Mf + Mb) / r**2) == 0,
      f"L_onshell + E_938 = {d1_id}; phi' = G(M+M_b)/r^2", "exactly 0")
# Euler-Lagrange with the hold K W'(u) = c2 u + u^2/(a0 - u)
class Wh(sp.Function):
    """W(u) defined by K W'(u) = hold(u) = c2 u + u^2/(a0 - u)  (K = 4 pi G)."""
    def fdiff(self, argindex=1):
        a_ = self.args[0]
        return (C2 * a_ + a_**2 / (a0s - a_)) / (4 * sp.pi * Gs)


f_E = E938.subs(Wsym(uM), Wh(uM))
EL_E = sp.euler_equations(f_E, Mf, r)[0].lhs
Dfun = sp.Function("D")(r)
EL_D = sp.simplify(EL_E.subs(sp.Derivative(Mf, (r, 2)), sp.diff(4 * sp.pi * r**2 * Dfun, r))
                   .subs(sp.Derivative(Mf, r), 4 * sp.pi * r**2 * Dfun))
gb = Gs * Mb / r**2
target_D1 = -(gam * sp.diff(Dfun, r) - (uM**2 / (a0s - uM) - (1 - C2) * uM - gb))   # gamma D' = u^2/(a0-u) - (1-c2)u - g_b
d1_eq = sp.simplify(EL_D - target_D1)
d1_eq_alt = sp.simplify(EL_D + target_D1)
d1_ok = (d1_eq == 0) or (d1_eq_alt == 0)
check("D1b_v3_static_equation", d1_ok,
      f"gamma_L D' = u^2/(a0-u) {'- u ' if C2 == 0 else ''}- g_N,b (residual {d1_eq if d1_eq == 0 else d1_eq_alt})",
      "exactly 0")
# gamma -> 0: the static equation must be the law g_N = g^2/(g + a0) with g = g_N,b + u (and u = a0 g/(a0 + g));
# with gamma > 0 and c2 = 1 it reads R(u) = g_N,b + gamma_L D' (CFG938 S2d2, the screened law)
gs_ = sp.symbols("g_tot", positive=True)
u_law = a0s * gs_ / (a0s + gs_)
law_res = sp.simplify((C2 * u_law + u_law**2 / (a0s - u_law)) - u_law - (gs_ - u_law))   # EL at gamma=0 with g_b = g - u
law_res2 = sp.simplify((gs_ - u_law) - gs_**2 / (gs_ + a0s))
check("D1c_gamma0_limit_is_the_law", law_res == 0 and law_res2 == 0,
      f"EL(gamma=0) residual at u = a0 g/(a0+g): {law_res}; g_b - g^2/(g+a0) = {law_res2}", "exactly 0")


def lump_ode(c2):
    """Dimensionless (L* = a0 = G = 1, gamma_L = 2 pi): M' = 4 pi r^2 D, 2 pi D' = u^2/(1-u) - (1-c2) u, u = M/r^2."""
    def rhs(rr, y):
        M_, D_ = y
        uu = M_ / rr**2
        return [4 * math.pi * rr**2 * D_, (uu**2 / (1 - uu) - (1 - c2) * uu) / (2 * math.pi)]
    return rhs


def integrate_lump(c2, uL, rmax=60.0):
    Dc = uL / (4 * math.pi / 3)
    r0 = 1e-6
    y0 = [4 * math.pi / 3 * Dc * r0**3, Dc]

    def ev_edge(rr, y):
        return y[1]
    ev_edge.terminal, ev_edge.direction = True, -1

    def ev_cap(rr, y):
        return y[0] / rr**2 - 0.999
    ev_cap.terminal, ev_cap.direction = True, 1
    sol = solve_ivp(lump_ode(c2), (r0, rmax), y0, method="DOP853", rtol=1e-11, atol=1e-14,
                    events=[ev_edge, ev_cap], dense_output=False, max_step=0.05)
    edge = sol.t_events[0][0] if len(sol.t_events[0]) else None
    cap = sol.t_events[1][0] if len(sol.t_events[1]) else None
    D = sol.y[1]
    dD = np.diff(D)
    umax = float(np.max(sol.y[0][1:] / sol.t[1:]**2))
    return {"uL": uL, "edge_over_Lstar": edge, "cap_radius_over_Lstar": cap, "D_monotone_nondecreasing": bool(np.all(dD >= -1e-14 * abs(D[0]))),
            "D_end_over_Dc": float(D[-1] / D[0]), "r_end": float(sol.t[-1]), "umax": umax, "status": int(sol.status)}


d1_rows = [integrate_lump(C2, uL) for uL in (1e-3, 0.05, 0.2, 0.5)]
for row in d1_rows:
    say(f"   u(L*)/a0 = {row['uL']:<6}: edge {row['edge_over_Lstar']}  hold-cap radius {row['cap_radius_over_Lstar']}  "
        f"D monotone non-decreasing {row['D_monotone_nondecreasing']}  D_end/D_c {row['D_end_over_Dc']:.4g}")
v3_lump_exists = any(rw["edge_over_Lstar"] is not None for rw in d1_rows)
small = d1_rows[0]["edge_over_Lstar"]
v3_na3_D1 = v3_lump_exists and small is not None and abs(small / R_over_L - 1) < 0.01
res["D1"] = {"rows": d1_rows, "v3_isolated_lump_exists": v3_lump_exists, "v3_na3_from_D1": v3_na3_D1}
if C2 == 1:
    check("D1d_no_isolated_v3_lump", (not v3_lump_exists) and all(rw["D_monotone_nondecreasing"] for rw in d1_rows),
          f"edges found: {[rw['edge_over_Lstar'] for rw in d1_rows]}", "no edge; density rises outward until the hold cap")
else:
    check("D1d_no_isolated_v3_lump", (not v3_lump_exists), f"edges found: {[rw['edge_over_Lstar'] for rw in d1_rows]} "
          f"(small-u edge / (pi/sqrt2) = {small / R_over_L if small else None})", "no edge (mutate expects FAIL)")
say(f"   RSS {guard('D1'):.3f} GB")
say()

# ---------------------------------------------------------------------------------------------------------------------
say("== D2: v3 with the BS dust mass mu_K (linear statics: omega = 0 of K3)")
ks2 = sp.symbols("ks2", positive=True)
Kn = 1  # units 4 pi G = K = 1 for the algebra; gamma_L = L*^2/2
marg = sp.simplify(sp.numer(sp.together((W2_DERIVED / rho0).subs(k**2, ks2).subs(k, sp.sqrt(ks2)))))
marg_poly = sp.Poly(sp.expand(marg.subs({K: 1, gL: Ls**2 / 2})), ks2)
marg_poly = sp.Poly(sp.expand(marg_poly.as_expr() * (Ls**2 / 2) / marg_poly.LC()), ks2)   # leading coeff gamma_L
say(f"   marginal condition (K = 1, gamma_L = L*^2/2): {sp.factor(marg_poly.as_expr())} = 0")
roots = sp.solve(marg_poly.as_expr(), ks2)
# s* : value of mu_K L* at which k_s^2 = 2/L*^2 (the NA-3 wavenumber)
ssym = sp.symbols("s", positive=True)
sstar_expr = sp.solve(sp.Eq(marg_poly.as_expr().subs(ks2, 2 / Ls**2).subs(muK, ssym / Ls), 0), ssym)
sstar_expr = [sp.simplify(e) for e in sstar_expr]
say(f"   mu_K L* giving the NA-3 radius: s* = {sstar_expr}")
res["D2_symbolic"] = {"marginal_poly": str(marg_poly.as_expr()), "sstar": [str(e) for e in sstar_expr]}
marg_f = sp.lambdify((ks2, muK, Ls, Mth), marg_poly.as_expr(), "math")


def k_static(mu, L, M):
    """Positive root k_s of the marginal condition (units 1/pc); None if no static (Jeans-marginal) wavenumber."""
    # gamma_L k^4 + [K(M-1) - mu^2 gamma_L] k^2 - K M mu^2 = 0 (signs from the sympy polynomial)
    a, b, c = L**2 / 2, (M - 1) - mu**2 * L**2 / 2, -M * mu**2
    if a == 0:
        return None
    disc = b * b - 4 * a * c
    if disc < 0:
        return None
    k2 = (-b + math.sqrt(disc)) / (2 * a)
    if k2 <= 0:
        return None
    assert abs(marg_f(k2, mu, L, M + (1 - C2))) < 1e-9 * max(1.0, abs(a * k2 * k2), abs(c)), "root check"
    return math.sqrt(k2)


def mu_required(kt, L, M):
    """mu_K giving static wavenumber kt: mu^2 = k^2 (M - 1 + L^2 k^2/2) / (M + L^2 k^2/2)."""
    num = kt**2 * (M - 1 + L**2 * kt**2 / 2)
    den = M + L**2 * kt**2 / 2
    return math.sqrt(num / den) if num > 0 and den > 0 else None


# check the polynomial against the closed form used in k_static
coeffs = sp.Poly(marg_poly.as_expr(), ks2).all_coeffs()
cf_a = sp.simplify(coeffs[0] - Ls**2 / 2)
cf_b = sp.simplify(coeffs[1] - ((Mth - (1 - C2)) - 1 - muK**2 * Ls**2 / 2))
cf_c = sp.simplify(coeffs[2] + (Mth - (1 - C2)) * muK**2)
check("D2a_marginal_quadratic", cf_a == 0 and cf_b == 0 and cf_c == 0,
      f"coeffs vs gamma_L k^4 + [K(M_eff-1) - mu^2 gamma_L] k^2 - K M_eff mu^2 : {cf_a}, {cf_b}, {cf_c}",
      "exactly 0 (M_eff = M_theta - (1 - c2))")
# limits at M = 1 (c2 = 1)
s_lim = sp.symbols("s_lim", positive=True)
k2_M1 = sp.solve(sp.Eq((Ls**2 / 2) * ks2**2 - muK**2 * Ls**2 / 2 * ks2 - muK**2, 0), ks2)
k2_M1 = [e for e in k2_M1 if sp.simplify(e.subs({muK: 1, Ls: 1})) > 0][0]
lim_big = sp.limit(k2_M1.subs(muK, s_lim / Ls) / (s_lim / Ls)**2, s_lim, sp.oo)        # -> 1 : k_s = mu_K
lim_small = sp.limit(k2_M1.subs(muK, s_lim / Ls) / (sp.sqrt(2) * (s_lim / Ls) / Ls), s_lim, 0)  # -> 1 : k_s^2 = sqrt2 mu_K/L*
check("D2b_limits_M1", sp.simplify(lim_big - 1) == 0 and sp.simplify(lim_small - 1) == 0,
      f"mu_K L* >> 1: k_s^2/mu_K^2 -> {lim_big}; mu_K L* << 1: k_s^2/(sqrt2 mu_K/L*) -> {lim_small}", "both 1")
# profile: D ~ sin(k r)/(k r) and rho_tau = (M + L*^2 k^2/2) D
rho_tau_factor = sp.simplify((Mth - (1 - C2)) + Ls**2 * k**2 / 2)
Dprof = sp.sin(k * r) / (k * r)
lapD = sp.simplify(sp.diff(r**2 * sp.diff(Dprof, r), r) / r**2)
check("D2c_profile_sin_kr_over_kr", sp.simplify(lapD + k**2 * Dprof) == 0,
      f"lap D = -k^2 D; rho_tau = ({rho_tau_factor}) D (same zeros)", "exactly 0")

d2 = {}
for f in FOOT:
    a0f = A0[f]
    Mcl, rt = CL[f]["Mcl"], CL[f]["rt"]
    xcl = G * Mcl / (rt**2 * a0f)
    Mlist = {"M=1": 1.0, "M=1+x": 1.0 + xcl, "M=(1+x)^2": (1.0 + xcl)**2}
    targets = {"edge_rt": math.pi / rt, "half_rc870": XI_HALF / RC870}
    rows = []
    for lname, L in LSTAR[f].items():
        for mname, M in Mlist.items():
            Me = M - (1 - C2)
            for tname, kt in targets.items():
                mu = mu_required(kt, L, Me)
                row = {"Lstar_name": lname, "Lstar_pc": L, "M_name": mname, "M_theta": M, "M_eff": Me, "target": tname,
                       "R_target_pc": (math.pi if tname == "edge_rt" else XI_HALF) / kt}
                if mu is None:
                    row.update({"mu_req_per_pc": None})
                else:
                    mu_Mpc = mu * 1e6
                    eps = 1e-4
                    kp, km = k_static(mu, L * (1 + eps), Me), k_static(mu, L * (1 - eps), Me)
                    elast = -(math.log(kp) - math.log(km)) / (2 * eps) if kp and km else None
                    row.update({"mu_req_per_pc": mu, "inv_mu_pc": 1 / mu, "mu_req_per_Mpc": mu_Mpc,
                                "mu_req_h_per_Mpc": mu_Mpc / H_PRIMARY,
                                "ratio_to_cap": mu_Mpc / H_PRIMARY / MUK_CAP_H,
                                "ratio_to_cap_most_favourable_h": mu_Mpc / H_BRACKET[1] / MUK_CAP_H,
                                "ratio_to_growth_411": mu_Mpc / H_PRIMARY / MUK_GROWTH_H,
                                "ratio_to_BBN_literalK": mu_Mpc / H_PRIMARY / MUK_BBN_H,
                                "ratio_to_AeST_max_v4": mu_Mpc / MU_AEST_MAX,
                                "muK_Lstar": mu * L, "dlnR_dlnLstar": elast})
                rows.append(row)
    # NA-3 radius needs mu_K L* = s*(M); BS-cap lump scales
    cap_rows = []
    mu_cap = MUK_CAP_H * H_PRIMARY / 1e6       # per pc
    for lname, L in LSTAR[f].items():
        for mname, M in Mlist.items():
            Me = M - (1 - C2)
            kc = k_static(mu_cap, L, Me)
            sst = math.sqrt(2 * Me / (1 + Me)) if Me > 0 else 0.0
            cap_rows.append({"Lstar_name": lname, "Lstar_pc": L, "M_name": mname, "M_eff": Me,
                             "R_edge_at_cap_pc": (math.pi / kc) if kc else None,
                             "sstar": sst, "muK_for_NA3_radius_h_per_Mpc": (sst / L) * 1e6 / H_PRIMARY,
                             "NA3_needs_ratio_to_cap": (sst / L) * 1e6 / H_PRIMARY / MUK_CAP_H})
    d2[f] = {"x_cl": xcl, "M_list": Mlist, "targets_k_per_pc": targets, "rows": rows, "cap_rows": cap_rows}
    say(f"   [{f}] x_cl = G M_cl/(r_t^2 a0) = {xcl:.4f}; targets R_edge = r_t = {rt:.2f} pc, R_half = rc870 = {RC870} pc")
    for rw in rows:
        if rw["mu_req_per_pc"] is None:
            say(f"     L* {rw['Lstar_pc']:8.2f} {rw['M_name']:10s} {rw['target']:10s}: no mu_K gives this static scale")
            continue
        el = f"{rw['dlnR_dlnLstar']:.3f}" if rw["dlnR_dlnLstar"] is not None else "n/a"
        say(f"     L* {rw['Lstar_pc']:8.2f} {rw['M_name']:10s} {rw['target']:10s}: 1/mu_K {rw['inv_mu_pc']:8.1f} pc  "
            f"mu_K {rw['mu_req_h_per_Mpc']:9.4g} h/Mpc = {rw['ratio_to_cap']:7.1f} x cap (x{rw['ratio_to_growth_411']:.2f} "
            f"growth-411)  dlnR/dlnL* {el}")
    for cr in cap_rows:
        say(f"     at the BS cap: L* {cr['Lstar_pc']:8.2f} {cr['M_name']:10s}: R_edge {cr['R_edge_at_cap_pc']} pc;  "
            f"NA-3 radius needs mu_K L* = {cr['sstar']:.4f} -> mu_K {cr['muK_for_NA3_radius_h_per_Mpc']:.4g} h/Mpc "
            f"({cr['NA3_needs_ratio_to_cap']:.4g} x cap)")
res["D2"] = d2

# allowed-range test for A-PARTIAL (v3: BS cap; v4: H2's mu <= 1 Mpc^-1), most favourable h and every cell
all_rows = [rw for f in FOOT for rw in d2[f]["rows"] if rw["mu_req_per_pc"] is not None]
min_ratio_cap = min(rw["ratio_to_cap_most_favourable_h"] for rw in all_rows)
min_ratio_v4 = min(rw["ratio_to_AeST_max_v4"] for rw in all_rows)
v3_partial_allowed = min_ratio_cap <= 1.0
v4_partial_allowed = min_ratio_v4 <= 1.0
# NA-3 structure in v3 at mu_K = 0: a marginal k exists iff M_eff < 1 ... the NA-3 dispersion needs M_eff -> 0 at x -> 0
k_na3_mu0 = k_static(0.0, 1.0, 1.0 - (1 - C2))        # L* = 1, x -> 0
v3_na3_D2 = (k_na3_mu0 is not None) and abs(k_na3_mu0 / math.sqrt(2) - 1) < 0.10
res["D2_summary"] = {"min_required_over_cap_most_favourable_h": min_ratio_cap,
                     "min_required_over_v4_AeST_max": min_ratio_v4, "v3_partial_allowed": v3_partial_allowed,
                     "v4_partial_allowed": v4_partial_allowed, "mu0_static_k_at_x0_Lstar1": k_na3_mu0,
                     "v3_na3_from_D2": v3_na3_D2}
say(f"   smallest required mu_K / BS cap over all cells (h = {H_BRACKET[1]}): {min_ratio_cap:.4g}; "
    f"smallest required mu / v4 bound: {min_ratio_v4:.4g}")
say(f"   mu_K = 0, x -> 0: static wavenumber {k_na3_mu0} (NA-3 needs sqrt2/L*)")
if C2 == 1:
    check("D2d_v3_needs_muK_outside_cap", not v3_partial_allowed,
          f"min ratio {min_ratio_cap:.4g}", "> 1 in every cell (no allowed mu_K)")
    check("D2e_v3_mu0_no_static_scale", k_na3_mu0 is None, f"k_s(mu_K=0, x->0) = {k_na3_mu0}",
          "None: the hold cancels self-gravity, no Jeans-marginal scale")
else:
    check("D2e_v3_mu0_no_static_scale", k_na3_mu0 is None, f"k_s(mu_K=0, x->0) = {k_na3_mu0}",
          "None (mutate expects FAIL: NA-3 scale sqrt2/L*)")
say(f"   RSS {guard('D2'):.3f} GB")
say()

# ---------------------------------------------------------------------------------------------------------------------
say("== D3: CFG941 R1 (W_full -> W_rem; rejected, NOT REPAIRABLE): self-gravity + stiffness + residual tether")
# EL of E[M] with W_rem: gamma rho' = -u + u^2/(a0 - u) ; identical to the c2 = 0 v3 equation (computed in any mode)
d3_rows = [integrate_lump(0, uL) for uL in (1e-4, 0.05, 0.1, 0.2)]
for row in d3_rows:
    e = row["edge_over_Lstar"]
    say(f"   u(L*)/a0 = {row['uL']:<6}: edge R/L* = {e}  (R/(pi L*/sqrt2) = {e / R_over_L if e else None})  "
        f"max u/a0 = {row['umax']:.3f}")
r1_small = d3_rows[0]["edge_over_Lstar"]
check("D3_R1_lump_is_NA3", r1_small is not None and abs(r1_small / R_over_L - 1) < 0.01,
      f"R/L* at u->0: {r1_small}", "pi/sqrt2 = 2.2214 to 1% (R1 is a rejected variant: law FAIL 1.64 / 1.88, CFG941)")
res["D3"] = {"rows": d3_rows}
say()

# ---------------------------------------------------------------------------------------------------------------------
say("== D4: CFG938 local-EOS form (a) + tether off (rejected variant + unwritten switch)")
rr_, eps_ = sp.symbols("rho_ eps_", positive=True)
eint = gam / 2 * rr_**2                                 # internal energy per volume
p_eos = sp.simplify(rr_ * sp.diff(eint, rr_) - eint)   # p = rho de/drho - e
check("D4_local_EOS_pressure", sp.simplify(p_eos - gam / 2 * rr_**2) == 0 and
      sp.simplify(p_eos.subs(gam, 2 * sp.pi * Gs * Ls**2) - sp.pi * Gs * Ls**2 * rr_**2) == 0,
      f"p = {p_eos} = pi G L*^2 rho^2; with Newtonian self-gravity -> K2 (NA-3 exactly)", "exactly 0")
bbn = cfg938["S2"]["early_universe_local_EoS"]
res["D4"] = {"bbn_ratio_24pc": bbn["24pc"]["ratio_at_zBBN"], "bbn_ratio_1000pc": bbn["1000pc"]["ratio_at_zBBN"],
             "z10pct_24pc": bbn["24pc"]["z_where_10pct_of_radiation"],
             "z10pct_1000pc": bbn["1000pc"]["z_where_10pct_of_radiation"]}
say(f"   CFG938 S2d3: eps_stiff/eps_rad at z_BBN = {bbn['24pc']['ratio_at_zBBN']:.4g} (24 pc) / "
    f"{bbn['1000pc']['ratio_at_zBBN']:.4g} (1 kpc); 10% of radiation at z = {bbn['24pc']['z_where_10pct_of_radiation']:.3g} / "
    f"{bbn['1000pc']['z_where_10pct_of_radiation']:.3g}. A population born free after z ~ 8e4 would escape BBN, but no "
    f"formulation writes the switch (CFG938 B1) or gives the free population this term.")
say()

# ---------------------------------------------------------------------------------------------------------------------
say("== D5: formulation table (record strings verified in their files)")
CITES = {
    "S2": ("campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md", "(γ/2)|∇P|²"),
    "S4": ("campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md", "It stays as collisionless mass bound by"),
    "S4nd": ("campaign_fresh_gravity/THEORY_CANONICAL_2026-10-18.md", "S4 is NOT derivable from the single medium"),
    "888": ("campaign_fresh_gravity/CFG888_clump_self_gravity_from_action/README.md", "It cannot bind anything."),
    "938cancel": ("campaign_fresh_gravity/CFG938_medium_continuum_eft/DERIVATION.md",
                  "The self-gravity −Kρ₀ is cancelled exactly, and over-cancelled, by the tether."),
    "938bbn": ("campaign_fresh_gravity/CFG938_medium_continuum_eft/DERIVATION.md",
               "Excluded at BBN for the whole L* window if the medium exists then."),
    "938B1": ("campaign_fresh_gravity/CFG938_medium_continuum_eft/DERIVATION.md", "S4 untethering not derived"),
    "939": ("campaign_fresh_gravity/CFG939_lagrangian_displacement_shell_crossing/README.md", "Newtonian control λ_J = √2πL*"),
    "941R1": ("campaign_fresh_gravity/CFG941_self_gravity_repair/README.md", "W_full → W_rem (dust gravity kept"),
    "941R2": ("campaign_fresh_gravity/CFG941_self_gravity_repair/README.md", "tether sector on n_t only"),
    "941R3": ("campaign_fresh_gravity/CFG941_self_gravity_repair/README.md", "s(ρ_c)·[W_full + stiffness]"),
    "941DT": ("campaign_fresh_gravity/CFG941_self_gravity_repair/README.md", "Hence **(a) ⟹ no linear self-gravity**"),
    "638": ("campaign_fresh_gravity/CFG638_cold_energy_fluid_equations/README.md", "∇²Φ = 4πG(ρ_b + ρ_c)"),
    "638p": ("campaign_fresh_gravity/CFG638_cold_energy_fluid_equations/README.md", "(Π_ij − ρ_cσ_J²δ_ij)"),
    "848": ("campaign_fresh_gravity/CFG848_maxent_partition/README.md", "zero-stiffness force is used at all r"),
    "953": ("campaign_fresh_gravity/CFG953_source_changing_theory/README.md", "the dust untethered, so ∇_μ𝒮^{μν} = 0"),
    "953R9": ("campaign_fresh_gravity/CFG953_source_changing_theory/README.md", "| R9 | no action principle"),
    "v3": ("covariant_push_2026_10_22/THEORY_V3_DRAFT.md", "one stiffness term −(γ_L/2)(D·P)², γ_L = K L★²/2"),
    "v3cap": ("covariant_push_2026_10_22/THEORY_V3_DRAFT.md", "BS24 Eq. 39 caps μ_K ≤ 14.8 h/Mpc"),
    "v3growth": ("covariant_push_2026_10_22/THEORY_V3_DRAFT.md", "Reaching σ₈ ≈ 0.95 needs μ_K ≥ 411 h/Mpc"),
    "v3bbn": ("covariant_push_2026_10_22/THEORY_V3_DRAFT.md", "BBN (ΔN_eff,equiv ≤ 0.5 at 1 MeV) needs μ_K ≥ 1.84×10⁸ h/Mpc"),
    "v3halo": ("covariant_push_2026_10_22/THEORY_V3_DRAFT.md", "above it the dust forms galaxy halos and double-counts"),
    "v3top": ("covariant_push_2026_10_22/THEORY_V3_DRAFT.md", "Upper edge ~90 pc (LITTLE THINGS)"),
    "v4S4": ("covariant_push_2026_10_22/THEORY_V3_DRAFT.md",
             "In spherical symmetry the Khronon static equation is H2's AeST system with μ → μ_K"),
    "H4": ("rebuild_2026_10_22/H4_v3_saddle_stability/README.md", "**ω² = 4πG ρ_τ (M_θ − 1 + L★²k²/2)**"),
    "U1": ("rebuild_2026_10_22/U1_v3_dust_content/README.md", "held dust is self-repulsive at m > 0 and neutral at m → 0"),
    "H2poly": ("rebuild_2026_10_22/H2_aest_clusters/README.md", "Its natural extent is the n = 1 polytrope radius π/μ"),
    "H2C3": ("rebuild_2026_10_22/H2_aest_clusters/README.md", "C3 (L_eq = √2/μ ≥ 1.41 Mpc ⇔ μ ≤ 1)"),
    "soft": ("campaign_fresh_gravity/THEORY_CANONICAL_2026-10-21_DRAFT.md", "A soft upper edge 2.04 / 2.14 kpc"),
}
cite_ok = {}
for key, (path, s) in CITES.items():
    try:
        with open(rel(path), encoding="utf-8") as fh:
            txt = fh.read().split("\n")
        hit = [i + 1 for i, ln in enumerate(txt) if s in ln]
    except FileNotFoundError:
        hit = []
    cite_ok[key] = {"file": path, "string": s, "lines": hit}
    say(f"   cite {key:9s}: {path}:{hit[0] if hit else 'MISSING'}")
check("D5a_citations_present", all(v["lines"] for v in cite_ok.values()),
      f"{sum(1 for v in cite_ok.values() if v['lines'])}/{len(cite_ok)}", "all present")
res["citations"] = cite_ok

v3_na3 = v3_na3_D1 or v3_na3_D2
FORMS = [
    # name, live, carries stiffness on own density, linear self-gravity, na3, extra-constant partial allowed, note, cites
    ("v3 screened theory (Khronon + gamma_L, BS dust mu_K) [primary]", True, True, "only for k < ~mu_K (BS dust)",
     v3_na3, v3_partial_allowed,
     "hold cancels self-gravity (M_theta >= 1): isolated mu_K = 0 statics give gamma_L D' = u^2/(a0-u) >= 0, no lump (D1); "
     "with mu_K the static scale needs mu_K far outside the BS cap (D2)", ["v3", "H4", "U1", "v3cap"]),
    ("v4 AeST + gamma_L (capped F)", True, True, "only for k < ~mu (AeST dust)", v3_na3, v4_partial_allowed,
     "spherical statics = v3 with mu_K -> mu (S4); hydrostatic dust is an n = 1 polytrope of radius pi/mu (H2), "
     "mu <= 1 Mpc^-1 (H2 C3); v4 is ill-posed off symmetry (I1)", ["v4S4", "H2poly", "H2C3"]),
    ("canonical S2 + S3 (ID) + S4", True, True, "tethered: none (critical quadratic); S4 free: Newtonian, no action",
     v3_na3_D1, False, "statics = D1 (identical E[M]); S4's free population has no written action, so no stiffness",
     ["S2", "S4", "S4nd", "888"]),
    ("CFG938 covariant parent (chi-tidal stiffness, adopted)", True, True, "none (cancelled by the tether)", v3_na3_D1,
     False, "S5a: self-gravity cancelled exactly; untethering not derived (B1)", ["938cancel", "938B1"]),
    ("CFG938 local EOS (a) + tether off", False, True, "Newtonian", True, False,
     "NA-3 exactly (D4) but rejected: BBN if the medium exists then; switch unwritten", ["938bbn", "938B1"]),
    ("CFG939 single medium", True, True, "none (D-T)", v3_na3_D1, False,
     "its Newtonian lambda_J = sqrt2 pi L* is a tether-off control", ["939"]),
    ("CFG941 R1 (W_full -> W_rem)", False, True, "Newtonian", True, False,
     "NA-3 lump (D3) but NOT REPAIRABLE: the law fails (1.64 / 1.88)", ["941R1"]),
    ("CFG941 R2 (two populations, tether sector on n_t)", False, False, "free: Newtonian", False, False,
     "free population carries no stiffness; NOT REPAIRABLE", ["941R2"]),
    ("CFG941 R3n / R3theta / R3l (switch multiplies W_full + stiffness)", False, False, "where switched off: Newtonian",
     False, False, "untethered regions lose the stiffness with the tether; R3theta has a ghost", ["941R3", "941DT"]),
    ("class A (CFG541/638/882)", True, False, "Newtonian", False, False,
     "pressure = bath sigma_J^2 relaxation; no gamma stiffness", ["638", "638p"]),
    ("CFG848 two-population functional", False, False, "free: Newtonian", False, False,
     "zero-stiffness force; WRONG SIGN / ILL-POSED", ["848"]),
    ("SCT (CFG953; SCT-M retired after CFG960 SC1x)", False, False, "Newtonian (untethered dust)", False, False,
     "no stiffness in R0-R9; no action principle", ["953", "953R9"]),
]
table = []
for nm, live, stiff, sg, na3, part, note, cites in FORMS:
    table.append({"formulation": nm, "live": live, "stiffness_on_own_density": stiff, "linear_self_gravity": sg,
                  "NA3_structure": bool(na3), "partial_allowed": bool(part), "note": note, "cites": cites})
    say(f"   {nm}\n      live={live} stiffness={stiff} self-gravity: {sg}; NA-3={bool(na3)} partial-allowed={bool(part)}; {note}")
res["formulations"] = table

a_pass = any(t["live"] and t["NA3_structure"] for t in table)
a_partial = (not a_pass) and any(t["live"] and t["partial_allowed"] for t in table)
if a_pass:
    part_a = "A-PASS"
elif a_partial:
    part_a = "A-PARTIAL"
else:
    part_a = "NO FORMULATION"
res["part_A"] = part_a
res["part_B"] = ("NOT RUN (Part A = NO FORMULATION; FROZEN_CRITERIA s3)" if part_a == "NO FORMULATION"
                 else "WOULD RUN (not run in this mode)" if MUTATE else "PENDING")
lane_class = "NO FORMULATION" if part_a == "NO FORMULATION" else f"{part_a} -> Part B required"
res["class"] = lane_class
say()
say(f"PART A OUTCOME: {part_a}")
say(f"PART B: {res['part_B']}")
say("The lane does not address the lump MASS (supply), which stays open whatever the class.")
if C2 == 1:
    check("OUTCOME_rule_applied", part_a in ("A-PASS", "A-PARTIAL", "NO FORMULATION"), part_a, "frozen s3 rule")
else:
    check("OUTCOME_unchanged_by_mutation", part_a == "NO FORMULATION", part_a,
          "NO FORMULATION (mutate expects FAIL: the outcome must flip)")

res["rss_gb"] = guard("end")
res["checks"] = checks
npass = sum(1 for c in checks.values() if c["pass"])
say()
say(f"CFG965 COMPLETE: {npass}/{len(checks)} checks PASS. Peak RSS {res['rss_gb']:.3f} GB.")
with open(OUT_TXT, "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(OUT_JSON, "w") as fh:
    json.dump(res, fh, indent=1, default=str)
sys.exit(0 if npass == len(checks) else 1)
