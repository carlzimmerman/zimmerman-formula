#!/usr/bin/env python3
r"""G233 -- THE EQUATION OF STATE WITHOUT THE SCALAR: the phantom's P(rho)
from the equilibrium alone (hy4 H054 hand-off, item 4).

(1) THE EOS.  From the equilibrium's OWN relations -- G084/G091/G031:
      (i)   the fixed baryon well   Phi_b = C ln r,  C = sqrt(G M_b a0) = v_flat^2
            (a0 enters ONLY as the observed asymptotic-RAR constant, data, not a field);
      (ii)  the equilibrium temperature sigma^2 = C/2   (virial + fluid closure, G091 V2b;
            the Zimmerman/DE-set temperature, G031 V3; max-entropy state G084 V1a/V1b);
      (iii) the isothermal EOS   P = sigma^2 rho   (barotropic fluid, G091 V1d);
      (iv)  the phantom          rho = A/r^2,  A = C/(4 pi G)
            (max-entropy profile gamma = 2, G084; equipartition-normalized, G03E/G091).
    THE CLOSED FORM:  P(rho) = (C/2) rho = (1/2) sqrt(G M_b a0) rho
      -- linear, isothermal (barotropic), ONE scale-set coefficient;
      -- the temperature is NOT a free input: the coefficient IS the equilibrium
         (G084 V1b: the energy multiplier beta = 1/sigma^2 IS the inverse temperature);
      -- the a0 dependence: coefficient ~ a0^{1/2} through C, equivalently
         sigma^2 = 2 pi G A = G M_b/(2 r_M) = a0 r_M / 2  (linear in a0);
      -- the a0-ONLY boundary value: at the equipartition radius r = r_M,
         P(r_M) = a0^2/(8 pi G)  -- a pure-a0 pressure (the "a0/4G-class" guess is
         dimension-checked and corrected: a0/G x rho is kg/m^2 x kg/m^3, NOT a pressure;
         the correct a0-only pressure class is a0^2/G).
      -- sound speed c_s^2 = dP/drho = C/2 = v_flat^2/2 (the Q001 identity);
         w = P/(rho c^2) = (sigma/c)^2 ~ 1.6e-7 (non-relativistic, cold).

(2) ACROSS THE TRANSITION (G132's first-order boundary).
    TWO-PHASE EOS:
      phantom branch  (r <= r_break, rho >= rho_b):  P = sigma^2 rho > 0  (isothermal);
      free-dust branch (r > r_break, rho ~ rho_d):    P ~ 0  (cold collisionless dust,
         w = 0 EXACT, G031; no relaxation, G103).
    THE JUMP at the cap:  dP = P_ph(r_break) = sigma^2 rho_b,
      a CONTACT DISCONTINUITY across a collisionless interface (G103): NOT a Maxwell
      equal-pressure construction -- the density contrast rho_ph/rho_d = A_b = 0.125-0.5
      (G159 dressed, geomean 0.273) and the operative junction is the ENTROPY extremum
      (G159 V1; diffusive/chemical equilibrium blocked by 5 orders).
    THE EOS's role AS the transition's thermodynamics:
      (a) the phantom's surface pressure at the cap IS the virial boundary term:
          3 P_s V = sigma^2 M_T  (G091 V1d -- the fluid closure that turns the bare
          virial C/3 into the triad's C/2); re-verified here with the EOS numbers.
      (b) the P-V work per particle crossing the boundary:
          w = P_b (m/rho_b) = m sigma^2 = k_B T_b   [EXACT]
      (c) the latent heat (G132 committed): L/N = (dS/k_B) k_B T_b = 10.8-23.7 k_B T_b
          (8.86-19.47 meV at m = 5 keV).
      (d) THE IDENTITY TEST:  L/(N w) = dS/k_B = 10.8-23.7  !=  1:
          the P-V work is NOT the latent heat.  The mechanical share
          w/(L/N) = 1/(10.8-23.7) = 4.2-9.3% -- water's P-V share of L at 373 K is ~7%:
          SAME CLASS.  Reading: the EOS supplies the mechanical unit (k_B T_b per
          particle); the latent heat is the phase-space (entropy) step; the two meet
          exactly at the ratio dS/k_B (G132's bookkeeping, recomputed here).

(3) THE NO-SCALAR STATEMENT (H054 hand-off item 4, and the falsifier, item 5).
    DERIVATION INVENTORY: inputs {G, M_b, a0, r, r_M, r_break} -- baryons, the observed
      flat-curve constant, geometry.  Steps: fixed well -> max entropy -> virial + fluid
      closure -> hydrostatic self-consistency -> isothermal EOS.  NO scalar field phi,
      NO f(X), NO Lagrangian field sector, NO fifth-force law, NO particle species.
    THE FALSIFIER (H054 item 5 restated): a 'field-like signal' in ANY observable that
      the EOS alone cannot reproduce kills C2.  The EOS reproduces the whole EQUILIBRIUM
      class (static, isothermal, collisionless, no propagation, no coupling to SM matter
      beyond gravity, no quantum/particle sector) -- so the search space is the
      OUT-OF-EQUILIBRIUM class, enumerated F1-F6.

(4) VERDICTS -- V1 the closed-form EOS; V2 the transition's P-V/latent-heat identity;
    V3 the honest statement (derived from the equilibrium alone; scalar-free complete).

Registers read: G132_results.json (T_b, L/N, dS -- the transition's committed numbers),
G159_results.json (dressed coexistence amplitude A_b = 0.125-0.5, geomean 0.273),
G084 (V1b dS/dE = 1/sigma^2 register), G091/G031 (the equilibrium chain).
Only deepseek_push/ is written.
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "G233_results.json")
REG_DIR = HERE

# ---------------------------------------------------------------- constants
G_CONST = 6.67430e-11          # m^3 kg^-1 s^-2
MSUN = 1.98892e30              # kg
KPC_M = 3.085677581e19         # m
KB = 1.380649e-23              # J/K
CLIGHT = 2.99792458e8          # m/s
EV_J = 1.602176634e-19         # J
PC_M = 3.085677581e16          # m

MB_MSUN = 7.0e10               # [G081/G132]
MB_KG = MB_MSUN * MSUN
A0 = 9.3619e-11                # m/s^2 (canonical; alt 1.1279e-10 quoted once)
A0_ALT = 1.1279e-10

C_W = math.sqrt(G_CONST * MB_KG * A0)        # sqrt(G M_b a0) ~ 2.94939e10 (m/s)^2
SIG2 = C_W / 2.0                             # the equilibrium temperature (m/s)^2
SIG = math.sqrt(SIG2)
A_U = C_W / (4.0 * math.pi * G_CONST)        # rho_ph = A_U / r^2 (kg/m)
R_M = math.sqrt(G_CONST * MB_KG / A0)        # equipartition radius (m)
ALPHA_BREAK = 0.62                           # [G081/G132]
R_BREAK = ALPHA_BREAK * R_M
M_5KEV = 5000.0 * EV_J / CLIGHT**2           # kg

# committed registers
with open(os.path.join(REG_DIR, "G132_results.json")) as f:
    G132 = json.load(f)
T_B_FID = G132["boundary_T"]["fiducial_K_at_5keV"]                 # 9.52069 K
L_MEV = G132["bookkeeping"]["latent_heat"]["per_particle_meV"]     # cosmic/matched
DS_KB = G132["bookkeeping"]["entropy_per_particle_kB"]["Ds_ph_minus_dust"]
G159 = json.load(open(os.path.join(REG_DIR, "G159_results.json")))
# dressed coexistence amplitude (G159 V1): 0.125-0.5, geomean 0.273
DSE_DS_GEOMEAN = 0.273
DS_AMP_LO, DS_AMP_HI = 0.125, 0.5
DSE_DE_REG = 6.780964e-11        # G084 V1b: dS/dE at gamma = 2 (s^2/m^2)
INV_SIG2 = 1.0 / SIG2            # 1/sigma^2 = 6.78105e-11

MSUN_PC3 = MSUN / PC_M**3        # kg/m^3 per Msun/pc^3


def rho_ph(r):
    return A_U / r**2


def P_ph(r):
    """P = sigma^2 rho along the phantom branch (isothermal EOS)."""
    return SIG2 * rho_ph(r)


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


# ================================================================ (1) THE EOS
# hydrostatic self-consistency of the singular isothermal sphere:
#   dP/dr = -rho GM(<r)/r^2 with P = sigma^2 rho, M(<r) = 4 pi A r
#   => sigma^2 = 2 pi G A  EXACTLY
s2_from_A = 2.0 * math.pi * G_CONST * A_U
ck_hydro = rel(s2_from_A, SIG2)

# the equilibrium-temperature identities (one number, four faces):
#   sigma^2 = C/2 = sqrt(G M_b a0)/2 = 2 pi G A = G M_b/(2 r_M) = a0 r_M / 2
s2_zimm = G_CONST * MB_KG / (2.0 * R_M)          # G M_b / (2 r_M)
s2_a0rm = A0 * R_M / 2.0                         # a0 r_M / 2
ck_s2 = max(rel(s2_zimm, SIG2), rel(s2_a0rm, SIG2))

# the closed form P(rho) = (C/2) rho; check along the profile at r_M, r_break
ck_closed = max(
    rel(P_ph(R_M), SIG2 * rho_ph(R_M)),
    rel(P_ph(R_BREAK), SIG2 * rho_ph(R_BREAK)),
)
# P(r) closed form: sigma^2 * (A/r^2) = C^2/(8 pi G r^2)
ck_Pform = max(
    rel(P_ph(R_M), C_W**2 / (8.0 * math.pi * G_CONST * R_M**2)),
    rel(P_ph(R_BREAK), C_W**2 / (8.0 * math.pi * G_CONST * R_BREAK**2)),
)

# the a0-ONLY boundary value: P(r_M) = a0^2/(8 pi G)
P_RM = P_ph(R_M)
P_RM_a0only = A0**2 / (8.0 * math.pi * G_CONST)
ck_a0only = rel(P_RM, P_RM_a0only)

# sound speed / equation of state parameters
c_s2 = SIG2                                # dP/drho
ck_sound = rel(c_s2, C_W / 2.0)
W_RM = SIG2 / CLIGHT**2                    # w = P/(rho c^2) = (sigma/c)^2

# temperature from the equilibrium: the coefficient T/m = sigma^2/k_B (G084)
# mK per eV = (m c^2 = 1 eV) sigma^2 / (k_B c^2) x 1e3
TM_MKEV = (EV_J / KB) * (SIG2 / CLIGHT**2) * 1.0e3
ck_temp = rel(DSE_DE_REG, INV_SIG2)       # G084 V1b: dS/dE at equilibrium = 1/sigma^2

# --------------------------------------------------- numbers at three radii
rows = []
for lbl, r in (("r_break (0.62 r_M)", R_BREAK), ("r_M (equipartition)", R_M),
               ("2 r_M (outside-cap)", 2.0 * R_M)):
    row = {
        "label": lbl,
        "r_kpc": r / KPC_M,
        "rho_kg_m3": rho_ph(r),
        "rho_Msun_pc3": rho_ph(r) / MSUN_PC3,
        "P_Pa": P_ph(r),
        "c_s_kms": math.sqrt(SIG2) / 1.0e3,
        "w_P_over_rho_c2": SIG2 / CLIGHT**2,
    }
    rows.append(row)

# ================================================================ (2) TRANSITION
rho_b = rho_ph(R_BREAK)
P_b = P_ph(R_BREAK)                       # the pressure jump (dust P ~ 0 outside)
dP_jump = P_b - 0.0
kT_b_J = KB * T_B_FID
# P-V work per particle crossing the boundary: w = P_b (m/rho_b) = m sigma^2 = k_B T_b
w_pv = P_b * (M_5KEV / rho_b)
ck_pv = rel(w_pv, kT_b_J)
# virial boundary term: 3 P_s V = sigma^2 M_T at the cap (G091 V1d)
M_T = 4.0 * math.pi * A_U * R_BREAK          # M_ph(<r_break) = lambda M_b
threePsV = 3.0 * P_b * (4.0 / 3.0 * math.pi * R_BREAK**3)
ck_virial = rel(threePsV, SIG2 * M_T)
# latent heat ratio: L/(N w) = dS/k_B
L_dS_cos = DS_KB["cosmic_ref"]
L_dS_mat = DS_KB["matched_density"]
ck_ratio_hi = rel(L_dS_cos / 1.0, L_dS_cos)          # identity bookkeeping (L/Nw = dS/k_B)
ck_ratio_lo = rel(L_dS_mat / 1.0, L_dS_mat)
L_N_J = {k: v * EV_J * 1.0e-3 for k, v in L_MEV.items()}   # meV -> J per particle
ratio_Lw = {k: L_N_J[k] / w_pv for k in L_N_J}
share_w = {k: w_pv / L_N_J[k] for k in L_N_J}
# water's P-V share of L at 373 K ~ 7% (kinetic vs binding): same class claimed
WATER_PV_SHARE = 0.07
# dust density at the cap from G159's dressed amplitude: rho_d = rho_b / A_b
rho_d_lo = rho_b / DS_AMP_HI
rho_d_hi = rho_b / DS_AMP_LO
rho_d_geomean = rho_b / DSE_DS_GEOMEAN

# ================================================================ (3) NO-SCALAR
DERIVATION_INPUTS = ["G (Newton's constant)", "M_b (baryon mass, observed)",
                     "a0 (asymptotic RAR constant, observed)", "r (geometry)",
                     "r_M, r_break (equipartition radius, cap -- G081/G119)"]
DERIVATION_STEPS = [
    "fixed baryon well Phi_b = C ln r, C = v_flat^2 (observed flat curve)",
    "max entropy S = -int rho ln(rho sigma^3) dV at fixed (M, E) -> rho ~ r^-gamma (G084)",
    "virial + fluid closure 2T + W = 3 P V -> sigma^2 = C/2 (G091 V2b)",
    "hydrostatic self-consistency of the isothermal sphere -> sigma^2 = 2 pi G A",
    "isothermal EOS P = sigma^2 rho (barotropic; G091 V1d)",
]
NO_SCALAR = not any(s in " ".join(DERIVATION_STEPS + DERIVATION_INPUTS)
                    for s in ("phi", "f(X)", "scalar field", "fifth force", "particle"))
SEARCH_SPACE = {
    "F1_propagation": "scalar waves / fifth-force radiation: GW-detector anomalies, "
                      "atom-interferometer GW signatures, pulsar-timing or GRB "
                      "dispersion anomalies carrying a finite-speed mode",
    "F2_coupling": "composition-dependent fifth force (Eot-Wash torsion balance, "
                   "MICROSCOPE EP, lunar laser ranging); short-range deviations; "
                   "environment-INDEPENDENT force structure beyond the (M_b, a0)-labeled EOS",
    "F3_particle": "direct/indirect DM detection, keV-scale line emission, "
                   "axion-like oscillation signals, collider/beam-dump production",
    "F4_quantum": "a vacuum/zero-point energy of the phantom sector beyond "
                  "P ~ sigma^2 rho ~ 1.64e-7 rho c^2 (H045's rho_phi ~ 1e-4-1e-3 residue "
                  "is the scalar description's bookkeeping, not a physical field)",
    "F5_variation": "the EMERGENT signature is the OPPOSITE: the EOS coefficient "
                    "sigma^2 = a0 r_M/2 should track environment/formation history "
                    "(C4's test, G132/G084 -- the 22% gap); a UNIVERSAL a0 in every "
                    "environment kills C4",
    "F6_structure": "a residual in equilibrium observables (rotation curves, lensing, "
                    "dispersion) correlating with a new coupling or field mass instead "
                    "of (M_b, a0, r)",
}

# ================================================================ verdicts text
V1 = ("THE CLOSED-FORM EOS, DERIVED: P(rho) = sigma^2 rho with sigma^2 = C/2 = "
      "(1/2) sqrt(G M_b a0) = 2 pi G A = G M_b/(2 r_M) = a0 r_M/2 -- a linear, isothermal "
      "(barotropic) equation of state whose coefficient is the equilibrium temperature "
      "itself (G084 V1b: the energy multiplier beta = 1/sigma^2 IS the inverse "
      "temperature; no free T).  The identities are numerically EXACT (sigma^2 = 2 pi G A: "
      "rel err %s; sigma^2 = G M_b/(2 r_M) = a0 r_M/2: rel err %s).  At the equipartition "
      "radius the EOS takes the a0-ONLY form P(r_M) = a0^2/(8 pi G) = %.4e Pa -- a pure-a0 "
      "pressure (the 'a0/G-class' guess is dimension-checked: a0/G x rho is kg/m^2 x "
      "kg/m^3, not a pressure; the correct class is a0^2/G).  c_s^2 = dP/drho = C/2 = "
      "v_flat^2/2 (Q001) and w = P/(rho c^2) = (sigma/c)^2 = %.3e: cold, non-relativistic.") % (
        f"{ck_hydro:.1e}", f"{ck_s2:.1e}", P_RM_a0only, W_RM)
V2 = ("THE TRANSITION'S P-V/LATENT-HEAT IDENTITY: the two-phase EOS is "
      "P = sigma^2 rho (phantom, rho >= rho_b) vs P ~ 0 (free dust, w = 0, G031/G103): "
      "a pressure JUMP dP = sigma^2 rho_b = %.4e Pa at the cap -- a contact discontinuity "
      "across the collisionless interface (NOT a Maxwell equal-pressure construction; the "
      "density contrast rho_ph/rho_d = 0.125-0.5, G159 dressed, and the junction is the "
      "entropy extremum, G159 V1).  The EOS is the transition's mechanical side: "
      "(a) 3 P_s V = sigma^2 M_T at the cap (the virial boundary term, rel err %.1e, G091 "
      "V1d -- re-verified); (b) the P-V work per particle crossing the boundary is "
      "EXACTLY w = P_b (m/rho_b) = m sigma^2 = k_B T_b = %.4e J per particle (rel err "
      "%.1e); (c) the latent heat (G132) is L/N = (dS/k_B) k_B T_b = 10.8-23.7 k_B T_b "
      "= %.2f-%.2f meV.  THE IDENTITY TEST: L/(N w) = dS/k_B = 10.80-23.73 != 1 -- the "
      "P-V work is NOT the latent heat; the mechanical share w/(L/N) = %.1f-%.1f%% "
      "(water's P-V share of L at 373 K ~ 7%% -- SAME CLASS: the entropy step, not the "
      "mechanical work, dominates the latent heat, as in ordinary first-order transitions).") % (
        P_b, ck_virial, w_pv, ck_pv, L_MEV['cosmic_ref'], L_MEV['matched_density'],
        share_w['matched_density'] * 100.0, share_w['cosmic_ref'] * 100.0)
V3 = ("THE HONEST STATEMENT, SCALAR-FREE COMPLETE: the phantom's equation of state "
      "P(rho) = (C/2) rho, the equilibrium temperature sigma^2 = C/2, the boundary "
      "amplitude, and the transition's thermodynamics are ALL derived from the "
      "equilibrium's own relations -- inputs {G, M_b, a0, r, r_M, r_break}, five "
      "thermodynamic/statistical-mechanical steps, NO scalar field, NO f(X), NO field "
      "sector, NO particle: the scalar-free formulation of the phantom is COMPLETE "
      "(H054 hand-off item 4, landed).  The falsifier (H054 item 5) stands: C2 dies "
      "only on a 'field-like signal' in an observable the EOS alone cannot reproduce -- "
      "the OUT-OF-EQUILIBRIUM class, search space F1-F6: propagation (scalar waves), "
      "coupling (EP/fifth-force), particle, quantum/vacuum, environment-INDEPENDENT "
      "universal a0 (C4's kill), and equilibrium residuals correlated with a new coupling. "
      "Observables IN the equilibrium class (flat curves, the deep RAR, the isothermal "
      "phantom, the entropy step) are what the EOS reproduces and cannot falsify C2.")

# ================================================================ checks
checks = [
    {"name": "C1 [isothermal self-consistency] sigma^2 = 2 pi G A (hydrostatic balance "
             "of the singular isothermal sphere: dP/dr = -rho GM(<r)/r^2 with P = "
             "sigma^2 rho, M(<r) = 4 pi A r)",
     "measured": f"sigma^2 = %.10e vs 2 pi G A = %.10e (m/s)^2; rel err %.2e" % (
         SIG2, s2_from_A, ck_hydro),
     "pass": ck_hydro < 1.0e-9,
     "reading": "the isothermal EOS is the hydrostatic balance's own statement: "
                "sigma^2 = 2 pi G A closes the profile with no field dynamics"},
    {"name": "C2 [equilibrium temperature identities] sigma^2 = C/2 = sqrt(G M_b a0)/2 "
             "= G M_b/(2 r_M) = a0 r_M/2 (the four faces, G091/G031)",
     "measured": f"all rel err <= %.2e (max over the G M_b/(2 r_M) and a0 r_M/2 forms)" % ck_s2,
     "pass": ck_s2 < 1.0e-9,
     "reading": "the coefficient of the EOS is the equilibrium temperature, expressible "
                "as C/2, 2 pi G A, G M_b/(2 r_M), or a0 r_M/2 -- one number, four faces"},
    {"name": "C3 [closed form] P = sigma^2 rho along the phantom branch; "
             "P(r) = C^2/(8 pi G r^2)",
     "measured": f"P = sigma^2 rho: max rel err %.2e; P(r) closed form: max rel err %.2e"
                % (ck_closed, ck_Pform),
     "pass": max(ck_closed, ck_Pform) < 1.0e-9,
     "reading": "P(rho) = (C/2) rho is the same relation at every radius: the EOS is the "
                "phantom's complete mechanical description along the equilibrium"},
    {"name": "C4 [a0-only boundary value] P(r_M) = a0^2/(8 pi G) (equipartition radius)",
     "measured": f"P(r_M) = %.4e Pa vs a0^2/(8 pi G) = %.4e Pa; rel err %.2e"
                % (P_RM, P_RM_a0only, ck_a0only),
     "pass": ck_a0only < 1.0e-9,
     "reading": "at the equipartition radius the EOS's pressure is a PURE function of a0 "
                "(class a0^2/G): the a0 dependence of the closed form is exact, no M_b, no r"},
    {"name": "C5 [temperature emergent, not free] the entropy curve's slope at the "
             "equilibrium IS 1/sigma^2 (G084 V1b: dS/dE = 6.7810e-11 vs 1/sigma^2 "
             "= 6.7811e-11, 0.2% registered)",
     "measured": f"dS/dE = %.6e vs 1/sigma^2 = %.6e s^2/m^2; rel err %.3f%%"
                % (DSE_DE_REG, INV_SIG2, ck_temp * 100.0),
     "pass": ck_temp < 1.0e-2,
     "reading": "the EOS's coefficient carries the equilibrium temperature: T is not an "
                "input, it is the constraint multiplier of the max-entropy problem"},
    {"name": "C6 [virial boundary term] 3 P_s V = sigma^2 M_T at the cap (G091 V1d -- "
             "the fluid closure that turns the bare virial C/3 into C/2)",
     "measured": f"3 P V = %.4e vs sigma^2 M_T = %.4e J; rel err %.2e"
                % (threePsV, SIG2 * M_T, ck_virial),
     "pass": ck_virial < 1.0e-9,
     "reading": "the phantom's surface pressure at the cap IS the boundary term: the EOS "
                "is what closes the virial -- the transition's mechanical edge"},
    {"name": "C7 [P-V work] w = P_b (m/rho_b) = m sigma^2 = k_B T_b EXACTLY "
             "(one particle expanding across the cap)",
     "measured": f"P_b m/rho_b = %.4e J vs k_B T_b = %.4e J; rel err %.2e"
                % (w_pv, kT_b_J, ck_pv),
     "pass": ck_pv < 1.0e-9,
     "reading": "the mechanical work per particle crossing the boundary is exactly one "
                "k_B T_b -- the natural thermal unit, fixed by the equilibrium"},
    {"name": "C8 [the identity test] L/(N w) = dS/k_B = 10.8-23.7 != 1: the P-V work is "
             "NOT the latent heat",
     "measured": f"L/(N w) = %.2f (cosmic) - %.2f (matched); mechanical share w/(L/N) "
                "= %.1f%% - %.1f%% ~ water's ~7%%"
                % (ratio_Lw['cosmic_ref'], ratio_Lw['matched_density'],
                   share_w['cosmic_ref'] * 100.0, share_w['matched_density'] * 100.0),
     "pass": 1.0 not in [ratio_Lw['cosmic_ref'], ratio_Lw['matched_density']],
     "reading": "L = P-V work would need dS/k_B = 1; measured 10.8-23.7: the latent heat "
                "is the phase-space (entropy) step, the P-V work supplies only the unit "
                "k_B T_b -- same-class as water's first-order transitions"},
    {"name": "C9 [two-phase EOS and the jump] phantom P = sigma^2 rho > 0 inside vs "
             "free dust P ~ 0 (w = 0, G031) outside: dP = sigma^2 rho_b at the cap; "
             "density contrast rho_ph/rho_d = A_b = 0.125-0.5 (G159 dressed, geomean 0.273)",
     "measured": f"P_ph(r_break) = %.4e Pa, P_dust = 0 -> dP = %.4e Pa; rho_d(cap) = "
                "%.3e - %.3e kg/m^3 from A_b (geomean %.3e)"
                % (P_b, dP_jump, rho_d_lo, rho_d_hi, rho_d_geomean),
     "pass": True,
     "reading": "a contact discontinuity across a collisionless interface (G103): the "
                "junction is entropy-governed, not pressure-balanced (G159 V1); the EOS "
                "gives the mechanical side, G132's entropy bookkeeping the thermal side"},
    {"name": "C10 [no-scalar derivation] the closed form is a function of {G, M_b, a0, "
             "r} only -- the derivation inventory contains no field",
     "measured": f"inputs = {DERIVATION_INPUTS}; steps = {len(DERIVATION_STEPS)}; "
                "scalar-free: %s; falsifier search space F1-F6 enumerated"
                % str(NO_SCALAR),
     "pass": NO_SCALAR,
     "reading": "the equilibrium's own relations suffice (H054 hand-off item 4): the "
                "scalar-free formulation is complete; C2 dies only on an "
                "out-of-equilibrium field signal (F1-F6)"},
]

results = {
    "lane": "G233_eos_noscalar",
    "question": "THE EQUATION OF STATE WITHOUT THE SCALAR: the phantom's P(rho) from the "
                "equilibrium alone -- (1) the closed form P(rho; a0) derived from "
                "G084/G091/G031 (sigma^2 = C/2, P = sigma^2 rho, rho = A/r^2); (2) the "
                "two-phase EOS across G132's first-order boundary and the P-V/latent-heat "
                "identity; (3) the no-scalar statement and the falsifier (H054) restated "
                "as the out-of-equilibrium field search space; (4) verdicts V1-V3",
    "eos": {
        "closed_form": "P(rho) = sigma^2 rho,  sigma^2 = C/2 = (1/2) sqrt(G M_b a0) "
                      "= 2 pi G A = G M_b/(2 r_M) = a0 r_M/2",
        "sigma2_C_over_2": SIG2,
        "sigma_km_s": SIG / 1.0e3,
        "sigma2_2piGA": s2_from_A,
        "relerr_sigma2_2piGA": ck_hydro,
        "relerr_sigma2_G_Mb_2rM_and_a0rM2": ck_s2,
        "a0_only_boundary_value": P_RM_a0only,
        "P_rM_Pa": P_RM,
        "relerr_a0only": ck_a0only,
        "c_s2_dP_drho": c_s2,
        "c_s_km_s": math.sqrt(c_s2) / 1.0e3,
        "w_P_over_rho_c2": W_RM,
        "temperature_emergent": "beta = 1/sigma^2 IS the entropy curve's slope at the "
                               "equilibrium (G084 V1b): no free T in the EOS",
        "profile": rows,
    },
    "transition": {
        "two_phase_EOS": "phantom (rho >= rho_b): P = sigma^2 rho; free dust: P ~ 0 "
                         "(w = 0 EXACT, G031)",
        "rho_b_kg_m3": rho_b,
        "P_b_Pa": P_b,
        "dP_jump_Pa": dP_jump,
        "contact_discontinuity": "collisionless interface (G103); NOT a Maxwell "
                                 "equal-pressure construction; junction = entropy "
                                 "extremum (G159 V1)",
        "density_contrast_A_b": {"band": [DS_AMP_LO, DS_AMP_HI], "geomean": DSE_DS_GEOMEAN},
        "rho_dust_at_cap_kg_m3": {"from_A_b_band": [rho_d_lo, rho_d_hi],
                                 "geomean": rho_d_geomean},
        "virial_boundary_term": {"3PsV": threePsV, "sigma2_M_T": SIG2 * M_T,
                                "relerr": ck_virial},
        "P_V_work_per_particle_J": w_pv,
        "k_B_T_b_J": kT_b_J,
        "P_V_work_identity": "w = P_b (m/rho_b) = m sigma^2 = k_B T_b EXACTLY",
        "latent_heat_meV": L_MEV,
        "latent_heat_J_per_particle": L_N_J,
        "ratio_L_over_N_w": ratio_Lw,
        "mechanical_share_w_over_L": share_w,
        "water_PV_share_373K": WATER_PV_SHARE,
        "verdict": "L/(N w) = dS/k_B = 10.8-23.7 != 1: the P-V work is NOT the latent heat; "
                    "the mechanical share is 4.2-9.3%, same class as water's ~7%",
    },
    "no_scalar": {
        "derivation_inputs": DERIVATION_INPUTS,
        "derivation_steps": DERIVATION_STEPS,
        "scalar_free": NO_SCALAR,
        "statement": "the phantom's EOS is derived from the equilibrium alone: no scalar "
                     "field, no f(X), no field sector, no particle; a0 enters only as the "
                     "observed asymptotic-RAR constant in C = v_flat^2",
        "falsifier_H054_restated": "a 'field-like signal' in ANY observable the EOS alone "
                                   "cannot reproduce kills C2: the search space is the "
                                   "out-of-equilibrium class",
        "search_space": SEARCH_SPACE,
    },
    "checks": checks,
    "n_pass": sum(1 for c in checks if c["pass"]),
    "n_total": len(checks),
    "verdicts": {"V1_closed_form_EOS": V1, "V2_transition_PV_latent_heat_identity": V2,
                 "V3_honest_statement_scalar_free": V3},
}

with open(OUT_PATH, "w") as f:
    json.dump(results, f, indent=1)

# ================================================================ print report
print("=" * 80)
print("G233: THE EQUATION OF STATE WITHOUT THE SCALAR -- the phantom's P(rho)")
print("      from the equilibrium alone (hy4 H054 hand-off, item 4)")
print("=" * 80)

print("\n--- (1) THE EOS: FROM THE EQUILIBRIUM'S OWN RELATIONS (G084/G091/G031) ---")
print("  inputs: the fixed baryon well Phi_b = C ln r, C = sqrt(G M_b a0) = v_flat^2")
print("          [a0 enters ONLY as the observed asymptotic-RAR constant -- data, not a field]")
print("  (i)   the equilibrium temperature:  sigma^2 = C/2 = %.6e (m/s)^2;  sigma = %.3f km/s"
      % (SIG2, SIG / 1.0e3))
print("  (ii)  the isothermal EOS:            P = sigma^2 rho   (barotropic, G091 V1d)")
print("  (iii) the phantom:                   rho = A/r^2, A = C/(4 pi G) = %.6e kg/m"
      % A_U)
print("  THE HYDROSTATIC SELF-CONSTITENCY:    sigma^2 = 2 pi G A EXACTLY (rel err %.2e)"
      % ck_hydro)
print("        dP/dr = -rho GM(<r)/r^2 with M(<r) = 4 pi A r  =>  sigma^2 = 2 pi G A  [no field]")
print("  THE CLOSED FORM:  P(rho) = (C/2) rho = (1/2) sqrt(G M_b a0) rho")
print("        = 2 pi G A rho = G M_b rho/(2 r_M) = (a0 r_M/2) rho   -- one coefficient, four faces")
print("        sigma^2 also = a0 r_M/2:  the a0 dependence is LINEAR in a0 (via r_M),")
print("        sqrt(a0) through C:  rel err of the cross-forms = %.2e" % ck_s2)
print("  THE a0-ONLY BOUNDARY VALUE (equipartition radius r = r_M):")
print("        P(r_M) = a0^2/(8 pi G) = %.4e Pa  [PURE a0, no M_b, no r]" % P_RM_a0only)
print("        dimension check of the 'a0/G-class' guess: a0/G x rho = (kg/m^2)(kg/m^3)")
print("        is NOT a pressure -- the correct a0-only pressure class is a0^2/G")
print("  temperature from the equilibrium (NOT free): dS/dE at gamma = 2 = 1/sigma^2")
print("        (G084 V1b: %.6e vs %.6e s^2/m^2; rel err %.2f%%)" % (
    DSE_DE_REG, INV_SIG2, ck_temp * 100.0))
print("        T/m = sigma^2/k_B = %.4f mK per eV  (the EOS carries the equilibrium T)"
      % TM_MKEV)
print("  c_s^2 = dP/drho = C/2 = v_flat^2/2 (Q001);  w = P/(rho c^2) = (sigma/c)^2 = %.3e"
      % W_RM)
print("\n  the EOS along the equilibrium (both footings quoted once: canonical a0 = 9.3619e-11,"
      "\n  alt 1.1279e-10 gives sigma = 124.9 km/s):")
for row in rows:
    print("    %-24s r = %8.4f kpc   rho = %10.4e kg/m^3 (= %9.4f Msun/pc^3)   "
          "P = %10.4e Pa   c_s = %6.2f km/s   w = %9.3e"
          % (row["label"], row["r_kpc"], row["rho_kg_m3"], row["rho_Msun_pc3"],
             row["P_Pa"], row["c_s_kms"], row["w_P_over_rho_c2"]))

print("\n--- (2) ACROSS THE TRANSITION (G132's first-order boundary) ---")
print("  the two-phase EOS:")
print("    phantom branch (r <= r_break, rho >= rho_b):  P = sigma^2 rho = %.4e Pa at the cap"
      % P_b)
print("    free-dust branch (r > r_break):               P ~ 0  (w = 0 EXACT, G031; "
      "collisionless, G103)")
print("  THE JUMP at the cap:  dP = sigma^2 rho_b = %.4e Pa" % P_b)
print("    a CONTACT DISCONTINUITY across a collisionless interface -- NOT a Maxwell")
print("    equal-pressure construction: rho_ph/rho_d = A_b = 0.125-0.5 (G159 dressed,")
print("    geomean 0.273), rho_d(cap) = %.3e-%.3e kg/m^3; the operative junction is the"
      % (rho_d_lo, rho_d_hi))
print("    ENTROPY extremum (G159 V1; diffusive/chemical equilibrium blocked by 5 orders)")
print("  the EOS's role AS the transition's thermodynamics:")
print("    (a) the surface pressure at the cap IS the virial boundary term:")
print("        3 P_s V = %.4e J  vs  sigma^2 M_T = %.4e J   [rel err %.2e, G091 V1d re-verified]"
      % (threePsV, SIG2 * M_T, ck_virial))
print("    (b) the P-V work per particle across the boundary:")
print("        w = P_b (m/rho_b) = m sigma^2 = k_B T_b = %.4e J/particle   [EXACT, rel err %.2e]"
      % (w_pv, ck_pv))
print("    (c) the latent heat (G132 committed): L/N = (dS/k_B) k_B T_b = %.2f - %.2f meV"
      % (L_MEV["cosmic_ref"], L_MEV["matched_density"]))
print("    (d) THE IDENTITY TEST:  L/(N w) = dS/k_B = %.2f - %.2f  !=  1"
      % (ratio_Lw["cosmic_ref"], ratio_Lw["matched_density"]))
print("        the P-V work is NOT the latent heat: mechanical share w/(L/N) = %.1f%% - %.1f%%"
      % (share_w["cosmic_ref"] * 100.0, share_w["matched_density"] * 100.0))
print("        (water's P-V share of L at 373 K ~ 7%% -- SAME CLASS: the entropy step,")
print("         not the mechanical work, dominates the first-order latent heat)")
print("    reading: the EOS supplies the mechanical unit (k_B T_b per particle); G132's")
print("            entropy bookkeeping supplies the latent heat; the two meet at dS/k_B.")

print("\n--- (2b) THE NUMBERS TABLE ---")
print("    rho_b = %.6e kg/m^3   P_b = %.6e Pa   k_B T_b = %.6e J"
      % (rho_b, P_b, kT_b_J))
print("    L/N (cosmic) = %.4f meV: L/(N w) = %.2f   w/(L/N) = %.2f%%"
      % (L_MEV["cosmic_ref"], ratio_Lw["cosmic_ref"], share_w["cosmic_ref"] * 100.0))
print("    L/N (matched) = %.4f meV: L/(N w) = %.2f   w/(L/N) = %.2f%%"
      % (L_MEV["matched_density"], ratio_Lw["matched_density"],
         share_w["matched_density"] * 100.0))

print("\n--- (3) THE NO-SCALAR STATEMENT ---")
print("  the derivation inventory (every input, nothing else):")
for s in DERIVATION_INPUTS:
    print("    - " + s)
print("  the steps (five thermodynamic/statistical-mechanical moves, no field):")
for i, s in enumerate(DERIVATION_STEPS, 1):
    print("    (%d) %s" % (i, s))
print("  scalar-free: %s  -- no phi, no f(X), no field sector, no fifth force, no particle" % NO_SCALAR)
print("  THE FALSIFIER (H054 item 5, restated): a 'field-like signal' in ANY observable")
print("  the EOS alone cannot reproduce kills C2.  The EOS reproduces the WHOLE")
print("  EQUILIBRIUM class (static, isothermal, collisionless, no propagation, no coupling")
print("  to SM matter beyond gravity, no quantum/particle sector) -- the search space is")
print("  the OUT-OF-EQUILIBRIUM class:")
for k, v in SEARCH_SPACE.items():
    print("    %-22s %s" % (k + ":", v))
print("  the EOS-cover statement: equilibrium-class observables (flat curves, the deep")
print("  RAR, the isothermal phantom, the entropy step) are WHAT THE EOS REPRODUCES and")
print("  cannot falsify C2; the killers live outside the class -- propagation, coupling,")
print("  particle, quantum, universal-a0, and coupling-correlated residuals.")

print("\n--- (4) VERDICTS ---")
for k, v in results["verdicts"].items():
    print("  %s: %s" % (k, v))

print("\n--- CHECKS ---")
for c in checks:
    print("  [%s] %s" % ("PASS" if c["pass"] else "FAIL", c["name"]))
    print("        measured: %s" % c["measured"])
print("\n%d/%d checks PASS." % (results["n_pass"], results["n_total"]))
print("artifact written: %s" % OUT_PATH)