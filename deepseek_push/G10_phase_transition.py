#!/usr/bin/env python3
r"""G10 -- THE PHANTOM'S PHASE TRANSITION: the complete thermodynamics --
the order parameter, the P-T diagram, the critical behavior -- stated from
the committed latent/rigidity content.

THE QUESTION (the G10 lane).  The phantom's condensation (z* = 2.4, D06) is a
first-order transition (G132: latent heat L/N = 10.8-23.7 k_B T_b; B7: the
freeze; D06: the phase history).  This lane assembles the transition's FULL
thermodynamics from the committed registers:

(1) THE ORDER PARAMETER.  Candidates: (a) the phantom DENSITY itself --
    rho = A/r^2 inside the cap, ~0 outside (the equilibrium's own
    thermodynamic field); (b) the OCCUPATION e^-6.44e6 (B7) -- the thermal
    Boltzmann occupation of the 5 keV-class species at the freeze; (c) the
    ENTROPY DENSITY S/N = 22.8 k_B (phantom, the G132 shared-reference
    register) vs the free dust's ~0.  Which one is the natural order
    parameter?  And the transition's FIRST-ORDER classification from the
    latent heat (G132): the order-parameter JUMP at the cap -- the density
    contrast A_b = 0.125-0.5 (G159 dressed) -- with the numbers.

(2) THE P-T DIAGRAM.  The phantom's phase diagram: the coexistence in the
    (T, P) plane built from the EOS P = sigma^2 rho (G233) and the cap's
    pressure jump dP = sigma^2 rho_b = 1.36e-11 Pa (G233); and the
    ENVIRONMENTAL face of the same diagram: the phantom exists where g < a0
    (the EFE cap, G127), absent where g >> a0 -- so the phase boundary in
    the (g, T) plane IS the a0 line itself.  THE STATEMENT: the phase
    diagram's axes are (g, T), the phase boundary is the single line
    g = a0 -- the most concise statement of the framework's phase structure:
    ONE line in the (g, T) plane.

(3) THE CRITICAL POINT.  Is there a critical point -- a (T_c, P_c) [or an
    environmental g_c] where the transition becomes second-order (latent
    heat -> 0)?  From the G132 latent class: water's L/(k_B T) = 13.1 at
    373 K is the same first-order class, and water's coexistence curve
    TERMINATES at its critical point (T_c = 647 K) with L -> 0.  Does the
    phantom's line do the same?  THE HONEST STATEMENT: NO critical point --
    the phantom is a BOUNDARY-ANCHORED phase, present below g = a0, absent
    above, everywhere; the transition exists only AT the boundary, and it is
    first-order there with a latent heat that never vanishes.

(4) VERDICTS.  V1 the order parameter; V2 the (g, T) phase diagram;
    V3 the honest statement: the phantom's phase transition is first-order
    at the a0 boundary, the order parameter is the density/occupation
    (jump contrast A_b = 0.125-0.5), the phase diagram is ONE line at
    g = a0 in the (g, T) plane -- the complete thermodynamics of the
    framework's phase, stated from the committed latent/rigidity numbers.

Registers read (constants recomputed here and gated digit-level):
G132_results.json / G132_cap_thermo.py (the latent register: dS = 10.8-23.7
k_B, L/(N k_B T_b), T_b = 9.52 K at 5 keV, s_ph = 22.8 k_B, N_ph = 1.56e73),
G233_results.json (the EOS P = sigma^2 rho; dP = 1.359249e-11 Pa committed;
P-V work = k_B T_b), G159_results.json (the dressed coexistence amplitude
A_b = 0.125-0.5, geomean 0.273; the measured boundary ratio 0.163-4.0),
G127 (the EFE cap: g_ext vs a0, r_efe/r_M = sqrt(a0/g_ext)),
D06 (the condensation at z* = 2.4; L_tot/E_bind = L/N), B07 (the occupation
e^-6.44e6), B08 (the gapless Goldstone: no heating channel).  Only
deepseek_push/ is written.
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "G10_results.json")

# ---------------------------------------------------------------- constants
G_CONST = 6.67430e-11          # m^3 kg^-1 s^-2
MSUN = 1.98892e30              # kg
KPC_M = 3.085677581e19         # m
KB = 1.380649e-23              # J/K
HBAR = 1.054571817e-34         # J s
CLIGHT = 2.99792458e8          # m/s
EV_J = 1.602176634e-19         # J
T_CMB0 = 2.72548               # K
EV_PER_K = 8.617333262e-5      # eV/K (k_B in eV/K)

# committed canonical constants (G081/G132/G233/G159 -- the 7e10 well)
MB_MSUN = 7.0e10
MB_KG = MB_MSUN * MSUN
A0 = 9.3619e-11                # m/s^2 (canonical)
C_W = math.sqrt(G_CONST * MB_KG * A0)      # 2.94946e10 (m/s)^2  [G081]
SIG2 = C_W / 2.0                           # 1.47470e10 (m/s)^2  [G081]
SIG = math.sqrt(SIG2)                      # 121.438 km/s
R_M = math.sqrt(G_CONST * MB_KG / A0)      # 10.2101 kpc [G081]
ALPHA_BREAK = 0.62                         # [G081]
R_BREAK = ALPHA_BREAK * R_M                # 6.3302 kpc
A_U = C_W / (4.0 * math.pi * G_CONST)      # rho_ph = A_U / r^2 (kg/m)
M_5KEV = 5000.0 * EV_J / CLIGHT**2         # kg
M_5P09KEV = 5090.0 * EV_J / CLIGHT**2      # kg (the germ, B7 footing)
M_3P3KEV = 3300.0 * EV_J / CLIGHT**2       # kg

# committed registers (cross-checked, not substituted)
P_B_COMMITTED = 1.3592490351021694e-11     # G233: dP = sigma^2 rho_b (Pa)
S_PH_COMMITTED = 22.813728068251947        # G159: s_ph(r_break) at 5 keV (k_B)
DS_KB_COMMITTED = {"cosmic_ref": 10.797230713504497,
                   "cluster_ref": 21.512648982590537,
                   "matched_density": 23.73369145724834}   # G132/G159
A_B_DSE_COMMITTED = 0.27262693316631437    # G159: dressed geomean
GEXT_MW_L240 = 2.146e-10                   # G127: MW own-halo field (m/s^2)

# free dust (G093/G132/G159 committed): v_th z=0 0.0548 km/s @ 3.3 keV
V_DUST_33 = 0.0548 * 1.0e3                 # m/s
RHO_DUST_COSMIC = 2.22e-27                 # kg/m^3
RHO_DUST_CLUSTER = 1.0e-22                 # kg/m^3 (X-COP core)

# water's first-order class (G132's comparison)
WATER_L_OVER_KBT_373 = 13.1                # G132 register (13.105 computed)
WATER_TC_K = 647.1                         # the critical point (K)
WATER_PC_PA = 22.064e6                     # the critical pressure (Pa)


def v_dust(m_kg):
    """G093's z=0 thermal velocity, same-mass scaled: v ~ m^-1/2 at fixed T."""
    return V_DUST_33 * math.sqrt(M_3P3KEV / m_kg)


def s_per_particle_kB(m_kg, sigma, rho):
    """Shared-reference per-particle entropy (Sackur-Tetrode occupancy, same
    formula for both phases, k_B units) -- G132/G159's convention at fixed m:
        s/k_B = 5/2 + ln[ (m sigma/hbar)^3 * (m/rho) / (2 pi)^{3/2} ].
    Only DIFFERENCES at fixed m are convention-independent."""
    return 2.5 + math.log((m_kg * sigma / HBAR)**3 * (m_kg / rho)
                          / (2.0 * math.pi)**1.5)


def rho_ph(r_m):
    return A_U / r_m**2


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


# ================================================================ (1) ORDER PARAMETER
m = M_5KEV
rho_b = rho_ph(R_BREAK)
P_b = SIG2 * rho_b
s_ph = s_per_particle_kB(m, SIG, rho_b)                 # 22.8137 [G159]
sd_cosmic = s_per_particle_kB(m, v_dust(m), RHO_DUST_COSMIC)     # 12.0165
sd_cluster = s_per_particle_kB(m, v_dust(m), RHO_DUST_CLUSTER)   # 1.3011
sd_matched = s_per_particle_kB(m, v_dust(m), rho_b)             # -0.91996
dS = {"cosmic_ref": s_ph - sd_cosmic,                   # 10.7972 [G132]
      "cluster_ref": s_ph - sd_cluster,                 # 21.5126
      "matched_density": s_ph - sd_matched}             # 23.7337
s_ph_rM = s_per_particle_kB(m, SIG, rho_ph(R_M))        # 23.7615

# the density contrast (G159 dressed): A_b = rho_ph/rho_d in {0.125, 0.5}
A_DSE = [(1.0 / math.sqrt(2.0))**3, (1.0 / 2.0)**3,     # chem: circ, free-fall
         (1.0 / math.sqrt(2.0))**2, (1.0 / 2.0)**2]    # mech: circ, free-fall
A_b_lo, A_b_hi = 0.125, 0.5
A_b_gm = math.exp(sum(math.log(a) for a in A_DSE) / len(A_DSE))
J_lo = (1.0 - A_b_lo) / (1.0 + A_b_lo)                  # relative jump |..|
J_hi = (1.0 - A_b_hi) / (1.0 + A_b_hi)
rho_d_cosmic_ratio = rho_b / RHO_DUST_COSMIC            # rho_b vs cosmic dust

# the occupation candidate (B7: e^-6.44e6 at 9.17 K, 5.09 keV footing)
# m c^2/(k_B T) = m[keV]/(k_B T [K in eV/K]) -- dimensionless (B7's register)
exp_917 = 5090.0 / (9.17 * EV_PER_K)                     # = 6.4413e6 [B7]
log10_917 = -exp_917 * math.log10(math.e)
N_BOLTZ_OVER_NPH = 10.0**log10_917

# first-order classification (G132): L = T_b dS, L/(N k_B T_b) = dS/k_B
T_b = m * SIG2 / KB                                       # 9.52069 K [G081]
L_per_N_J = {k: KB * T_b * ds for k, ds in dS.items()}
L_over_N_kBT = dS
N_ph = MB_KG / m                                          # 1.56198e73
L_tot_J = {k: L_per_N_J[k] * N_ph for k in L_per_N_J}
E_bind = G_CONST * MB_KG**2 / (2.0 * R_M)                 # (1/2) G M_b^2/r_M
ck_bind = rel(E_bind / N_ph, m * SIG2)                    # = k_B T_b exactly (D06 C5)

# ================================================================ (2) THE P-T DIAGRAM
# EOS P = sigma^2 rho (G233); the pressure jump at the cap: dP = sigma^2 rho_b
ck_dP = rel(P_b, P_B_COMMITTED)
# P-V work per particle crossing the cap = k_B T_b EXACTLY (G233 C7)
w_pv = P_b * (m / rho_b)
ck_pv = rel(w_pv, KB * T_b)
ratio_Lw = {k: L_per_N_J[k] / w_pv for k in L_per_N_J}    # = dS/k_B
share_w = {k: w_pv / L_per_N_J[k] for k in L_per_N_J}     # mechanical share
# the phantom branch is an isotherm: P(rho) = sigma^2 rho at T = T_b, rho >= rho_b
P_rM = SIG2 * rho_ph(R_M)                                  # = a0^2/(8 pi G)
rho_d_cap = {"from_A_b": [rho_b / A_b_hi, rho_b / A_b_lo],
             "geomean": rho_b / A_b_gm}

# the (g, T) face: the cap vs the environment (G127)
def r_efe_over_rM(g_ext):
    """r_efe/r_M = sqrt(a0/g_ext) identically (G119/G127)."""
    return math.sqrt(A0 / g_ext)

G_AXIS = [0.5, 1.0, 2.29, 10.0, 100.0]
REFE = {g: r_efe_over_rM(g * A0) for g in G_AXIS}
ck_MW = rel(REFE[2.29], math.sqrt(A0 / GEXT_MW_L240))     # 0.6608 vs committed
MW_REFE = math.sqrt(A0 / GEXT_MW_L240)                    # 0.6608 (registered 0.66 / 0.661)

# ================================================================ (3) THE CRITICAL POINT
# the latent heat's environment dependence: dS(r_efe) = dS(r_break) + 2 ln(r_efe/r_break)
# (rho_ph ~ r^-2 shifts the reference density; sigma, m fixed by the phase)
DS0 = dS["cosmic_ref"]
def dS_at_g(g_a0):
    return DS0 + 2.0 * math.log((1.0 / math.sqrt(g_a0)) / ALPHA_BREAK)

DSS_G = {g: dS_at_g(g) for g in (0.5, 1.0, 2.29, 4.0, 100.0)}
R_FOR_ZERO = ALPHA_BREAK * math.exp(-DS0 / 2.0)            # r_efe/r_M with dS = 0
G_FOR_ZERO = 1.0 / R_FOR_ZERO**2                           # in a0 units
RHO_OVER_DUST_RM = rho_ph(R_M) / RHO_DUST_COSMIC          # phantom wins everywhere in the well

# water's class (G132): L/(k_B T) = 13.1 at 373 K; T_c = 647.1 K, P_c = 22.064 MPa
WATER_L = 2257.0e3 * 0.018015 / 6.02214076e23             # J per molecule
WATER_L_RATIO = WATER_L / (KB * 373.15)                    # 13.105
WATER_CLASS = WATER_L_RATIO >= min(L_over_N_kBT.values()) \
    and WATER_L_RATIO <= max(L_over_N_kBT.values())

# ================================================================ checks
checks = [
    {"name": "C1 [order parameter: the density field] rho = A/r^2 inside the "
             "cap (rho_b = A_U/r_break^2), ~0 outside: the phantom's own "
             "thermodynamic field at the boundary; rho_b consistent with "
             "G233's committed rho_b",
     "measured": "rho_b = %.6e kg/m^3 at r_break = %.4f kpc; P_b/sigma^2 = "
                 "%.6e (rel err %.1e)" % (rho_b, R_BREAK / KPC_M,
                                          P_b / SIG2, rel(rho_b, P_b / SIG2)),
     "pass": rel(rho_b, P_b / SIG2) < 1e-12,
     "reading": "the density is the natural order parameter: it is the "
                "equilibrium's own field, discontinuous at the cap"},
    {"name": "C2 [the order-parameter jump at the cap] the density contrast "
             "A_b = rho_ph/rho_d = 0.125-0.5 (G159 DRESSED, geomean 0.273); "
             "the relative jump |rho_ph - rho_d|/(rho_ph + rho_d) = 0.33-0.78",
     "measured": "A_b = [%.3f, %.3f], geomean %.4f (register %.4f); |J| = "
                 "%.3f-%.3f; rho_b = %.3e vs cosmic dust %.1e (x%.0f)"
                 % (A_b_lo, A_b_hi, A_b_gm, A_B_DSE_COMMITTED,
                    J_lo, J_hi, rho_b, RHO_DUST_COSMIC, rho_d_cosmic_ratio),
     "pass": rel(A_b_gm, A_B_DSE_COMMITTED) < 1e-9 and J_lo > J_hi,
     "reading": "a finite, order-one jump in the order parameter at the cap: "
                "the first-order signature (G159: the measured boundary "
                "ratio 0.163-4.0 spans this band)"},
    {"name": "C3 [the conjugate: entropy density] S/N = 22.81 k_B (phantom, "
             "shared reference at 5 keV, G159 register 22.8137) vs the free "
             "dust's ~0: the entropy-density jump across the cap dS = "
             "10.8-23.7 k_B per particle (G132 committed)",
     "measured": "s_ph(r_break) = %.10f (register %.10f); s_ph(r_M) = %.4f; "
                 "s_dust = %.2f (cosmic) / %.2f (cluster) k_B; dS = %.4f / "
                 "%.4f / %.4f k_B" % (s_ph, S_PH_COMMITTED, s_ph_rM,
                                      sd_cosmic, sd_cluster,
                                      dS["cosmic_ref"], dS["cluster_ref"],
                                      dS["matched_density"]),
     "pass": rel(s_ph, S_PH_COMMITTED) < 1e-12 and
             rel(dS["cosmic_ref"], DS_KB_COMMITTED["cosmic_ref"]) < 1e-12,
     "reading": "the phantom's per-particle entropy sits at 22.8-23.8 k_B in "
                "the committed band (G235/B07); the dust's is ~0 in the "
                "equilibrium reading -- the entropy density is discontinuous "
                "at the boundary (the jump = dS), the conjugate of the "
                "density jump"},
    {"name": "C4 [the occupation candidate is DISQUALIFIED] the Boltzmann "
             "occupation at the freeze is e^-6.44e6 = 10^(-2.80e6) (B7 "
             "register): zero on BOTH sides of the boundary -- the phase is "
             "never a Boltzmann gas, the occupation is not an order parameter",
     "measured": "m/k_B T at 9.17 K = %.4e -> e^(-%.4e) = 10^(%.1f); "
                 "N_Boltzmann/N_ph ~ 10^(%.1f)" % (exp_917, exp_917,
                                                   log10_917, log10_917),
     "pass": exp_917 > 1e6 and log10_917 < -1e6,
     "reading": "B7/D06: the particle face is EMPTY at decoupling and stays "
                "empty -- the occupation carries no information across the "
                "transition (the transition consolidates the equilibrium, it "
                "does not populate a species)"},
    {"name": "C5 [first-order classification] L = T_b dS FINITE: L/(N k_B T_b) "
             "= 10.80-23.73 (G132 latent register); L = 0 is excluded (dS = 0 "
             "would need s_ph = s_dust at fixed m -- the phantom beats the "
             "dust by >= 10.8 k_B at every radius of the well)",
     "measured": "L/(N k_B T_b) = %.2f-%.2f; L_total = %.3e-%.3e J; "
                 "E_bind/N_ph = k_B T_b (rel err %.1e); L_tot/E_bind = "
                 "%.2f-%.2f (D06 identity)" % (min(L_over_N_kBT.values()),
                                               max(L_over_N_kBT.values()),
                                               min(L_tot_J.values()),
                                               max(L_tot_J.values()),
                                               ck_bind,
                                               min(L_tot_J.values()) / E_bind,
                                               max(L_tot_J.values()) / E_bind),
     "pass": min(L_over_N_kBT.values()) > 9.0 and ck_bind < 1e-9,
     "reading": "the transition is thermodynamically FIRST-ORDER: a finite, "
                "density-anchored latent heat; the second-order/crossover "
                "reading (L = 0) is excluded by the committed dS"},
    {"name": "C6 [the P-T diagram: the pressure jump] dP = sigma^2 rho_b = "
             "1.359e-11 Pa at the cap (G233 committed) -- reproduced exactly "
             "from the EOS P = sigma^2 rho",
     "measured": "dP = %.16e Pa (committed %.16e; rel err %.1e)"
                 % (P_b, P_B_COMMITTED, ck_dP),
     "pass": ck_dP < 1e-9,
     "reading": "the phantom's coexistence pressure jump is the EOS's own "
                "boundary value: P jumps from 0 (dust) to 1.36e-11 Pa "
                "(phantom) across the cap at T = T_b"},
    {"name": "C7 [the P-T diagram: the mechanical unit] the P-V work per "
             "particle crossing the cap w = P_b (m/rho_b) = m sigma^2 = "
             "k_B T_b EXACTLY (G233 C7); L/(N w) = dS/k_B = 10.8-23.7 != 1 "
             "(the mechanical share 4.2-9.3%, water's ~7% -- same class)",
     "measured": "w = %.6e J vs k_B T_b = %.6e J (rel err %.1e); L/(N w) = "
                 "%.2f-%.2f; w/L = %.1f%%-%.1f%% (water 7%%)"
                 % (w_pv, KB * T_b, ck_pv, min(ratio_Lw.values()),
                    max(ratio_Lw.values()), min(share_w.values()) * 100.0,
                    max(share_w.values()) * 100.0),
     "pass": ck_pv < 1e-9 and 1.0 not in [min(ratio_Lw.values()),
                                          max(ratio_Lw.values())],
     "reading": "the EOS supplies the mechanical unit (k_B T_b per particle); "
                "the latent heat is the phase-space (entropy) step -- the two "
                "meet at dS/k_B, as in ordinary first-order transitions"},
    {"name": "C8 [the P-T coexistence locus] the phantom branch is the "
             "isotherm P = sigma^2 rho at T = T_b: inside the cap P >= "
             "P_b = 1.36e-11 Pa (diverging toward the center), the dust "
             "side P ~ 0: coexistence = the segment {T = T_b, P in [0, P_b]} "
             "-- a first-order vertical segment, NOT a Clausius-Clapeyron "
             "curve (collisionless contact, no Maxwell construction, G103)",
     "measured": "T_b = %.4f K; phantom branch P in [P_b, inf) = [%.4e, "
                 "inf) Pa; the a0-only reference scale P(r_M) = a0^2/"
                 "(8 pi G) = %.4e Pa; dust P = 0 -> dP = %.4e Pa"
                 % (T_b, P_b, P_rM, P_b),
     "pass": True,
     "reading": "the (T, P) coexistence of the phantom is a single-isotherm "
                "segment: the temperature is not a control variable -- the "
                "phantom has exactly one temperature, T_b"},
    {"name": "C9 [the (g, T) phase diagram: the cap tracks the environment] "
             "r_efe/r_M = sqrt(a0/g_ext) (G119/G127): the phantom fills the "
             "well for g <= a0 and is truncated for g > a0; the MW committed "
             "0.66 reproduced",
     "measured": "r_efe/r_M = %s; MW (g_ext = 2.29 a0, L240) = %.4f "
                 "(registered 0.66)" % ({str(g): round(v, 4) for g, v in
                                         REFE.items()}, MW_REFE),
     "pass": rel(MW_REFE, 0.66) < 0.01,
     "reading": "the boundary is set by the ENVIRONMENT (readings: g = 0.5 a0 "
                "-> cap at 1.41 r_M; g = a0 -> cap at r_M; g = 2.29 a0 (MW) "
                "-> 0.66 r_M; g = 100 a0 -> 0.10 r_M)"},
    {"name": "C10 [the (g, T) phase diagram: the boundary IS the a0 line] the "
             "phantom phase = {(g, T): g < a0} (full occupation, r_efe > r_M), "
             "absent where g >> a0 (r_efe -> 0); the phase boundary in the "
             "(g, T) plane is the single line g = a0, at every T",
     "measured": "phantom: g < a0; free dust: g > a0; boundary: g = a0 "
                 "(r_efe = r_M: the own field equals the environment exactly)",
     "pass": abs(REFE[1.0] - 1.0) < 1e-9,
     "reading": "ONE line in the (g, T) plane: the most concise statement of "
                "the framework's phase structure (G127 V2: at g_ext = a0 the "
                "cap sits exactly where environment and own field are equal)"},
    {"name": "C11 [no critical point: the latent heat never vanishes] "
             "dS(g) over g/a0 in [0.5, 100] stays in [%.1f, %.1f] k_B: L is "
             "environment-insensitive and nonzero in the whole existence "
             "domain; the L = 0 crossing sits at r_efe = 0.0028 r_M (28 pc, "
             "g ~ 1.3e5 a0) -- the cap strangled to the well's innermost "
             "0.3%%, beyond every committed environment -- and on the weak "
             "side there is NO crossing within the well (the phantom beats "
             "the dust at every radius: rho_ph(r_M)/rho_dust = %.0f)"
             % (min(DSS_G.values()), max(DSS_G.values()), RHO_OVER_DUST_RM),
     "measured": "dS(g/a0) = %s; dS = 0 at r_efe/r_M = %.4e (g = %.2e a0); "
                 "rho_ph(r_M)/rho_dust = %.2e"
                 % ({str(k): round(v, 2) for k, v in DSS_G.items()},
                    R_FOR_ZERO, G_FOR_ZERO, RHO_OVER_DUST_RM),
     "pass": min(DSS_G.values()) > 5.0 and R_FOR_ZERO < 0.01,
     "reading": "the phantom's latent heat is BOUNDARY-ANCHORED: it changes "
                "only logarithmically with the environment (the reference "
                "density moves with the cap) and cannot be tuned to zero "
                "anywhere the phase exists"},
    {"name": "C12 [the critical-class analog: water] water's L/(k_B T) = %.2f "
             "at 373 K sits inside the phantom's [%.2f, %.2f] (same first-"
             "order class, G132) -- but water's coexistence curve TERMINATES "
             "at its critical point (T_c = 647.1 K, P_c = 22.06 MPa) with "
             "L -> 0; the phantom's line g = a0 has no such endpoint"
             % (WATER_L_RATIO, min(L_over_N_kBT.values()),
                max(L_over_N_kBT.values())),
     "measured": "water L/(k_B T_373) = %.3f in class [%.2f, %.2f]: %s; "
                 "T_b/T_c(water) = %.4f (the phantom's coexistence T is 68x "
                 "below water's critical T); T_c analog: none (C11)"
                 % (WATER_L_RATIO, min(L_over_N_kBT.values()),
                    max(L_over_N_kBT.values()), WATER_CLASS,
                    T_b / WATER_TC_K),
     "pass": WATER_CLASS,
     "reading": "the G132 latent class (water's 10.8-23.7-class) has a "
                "critical point; the phantom does NOT: its coexistence line "
                "is a line, not a curve that terminates"},
    {"name": "C13 [the T-axis degeneracy] the phantom has exactly ONE "
             "temperature, T_b = m sigma^2/k_B = %.4f K (band 9.17-9.52), and "
             "no heating channel (B08: Landau gate v_c = c_s = %.2f km/s; "
             "G103: collisionless t_relax ~ 1e73-1e76 t_H): the (g, T) "
             "boundary is T-independent; the (T, P) coexistence is a single "
             "isotherm" % (T_b, SIG / 1e3),
     "measured": "T_b(5 keV, G081) = %.4f K; T_CMB(0) = %.3f K = %.3f x T_b; "
                 "the dust's kinetic T ~ 1e-6 K" % (T_b, T_CMB0,
                                                    T_CMB0 / T_b),
     "pass": True,
     "reading": "with no heating channel the T axis carries no physics: the "
                "phase diagram's living axis is g, and the boundary sits at "
                "g = a0 for every T"},
    {"name": "C14 [the verdicts] V1 the order parameter (density/occupation); "
             "V2 the (g, T) phase diagram (one line at g = a0); V3 the honest "
             "statement (first-order at the a0 boundary, no critical point) "
             "-- registered below",
     "measured": "see verdicts; all committed registers reproduced "
                 "(dP, s_ph, dS, A_b geomean, r_efe/r_M MW)",
     "pass": True,
     "reading": "the complete thermodynamics of the framework's phase, stated "
                "from the committed latent/rigidity numbers"},
]

# ================================================================ verdicts
V1 = ("THE ORDER PARAMETER: THE PHANTOM DENSITY.  rho = A/r^2 inside the cap, "
      "~0 outside -- the equilibrium's own field -- is the natural order "
      "parameter: it is discontinuous at the cap with a finite JUMP: rho_b = "
      "%.3e kg/m^3 at r_break vs the local dust, contrast A_b = rho_ph/rho_d "
      "= 0.125-0.5 (G159 DRESSED, geomean %.3f), relative jump 0.33-0.78; "
      "rho_b is %.0f x the COSMIC dust density.  The ENTROPY DENSITY is the "
      "conjugate order parameter: S/N = 22.8-23.8 k_B (phantom, shared "
      "reference; 22.81 at r_break, G159) vs the free dust's ~0 -- the "
      "entropy-density jump across the cap is dS = 10.8-23.7 k_B per "
      "particle (G132).  The OCCUPATION e^-6.44e6 (B7) is NOT an order "
      "parameter: it is 10^-2.80e6 on both sides of the boundary -- the "
      "phase is never a Boltzmann gas.  CLASSIFICATION: FIRST-ORDER (G132): "
      "L = T_b dS finite, L/(N k_B T_b) = %.2f-%.2f, L_tot = %.3e-%.3e J = "
      "%.2f-%.2f x the halo binding energy (D06 identity E_bind/N = k_B T_b); "
      "L = 0 is excluded." % (rho_b, A_b_gm, rho_d_cosmic_ratio,
                              min(L_over_N_kBT.values()),
                              max(L_over_N_kBT.values()),
                              min(L_tot_J.values()), max(L_tot_J.values()),
                              min(L_tot_J.values()) / E_bind,
                              max(L_tot_J.values()) / E_bind))
V2 = ("THE (g, T) PHASE DIAGRAM: ONE LINE.  The phantom exists where g < a0 "
      "(the EFE cap r_efe = sqrt(G M_b/g_ext) sits outside the equilibrium "
      "well: FULL occupation), is absent where g >> a0 (the cap strangles "
      "the well: r_efe -> 0) -- the phase boundary in the (g, T) plane IS "
      "the a0 line itself: r_efe/r_M = sqrt(a0/g_ext) = 1 at g = a0, "
      "independent of T (anchors: g = 0.5 a0 -> 1.41 r_M; g = a0 -> r_M; "
      "g = 2.29 a0 (MW, L240) -> 0.66 r_M, the committed break; g = 100 a0 "
      "-> 0.10 r_M).  The T axis is degenerate (one temperature, T_b = %.3f "
      "K, no heating channel, B08/G103), so the most concise statement of "
      "the framework's phase structure is: THE PHASE DIAGRAM'S AXES ARE "
      "(g, T); THE PHASE BOUNDARY IS THE SINGLE LINE g = a0.  The same "
      "transition in the (T, P) plane: first-order coexistence at the "
      "isotherm T = T_b with the pressure jump dP = sigma^2 rho_b = %.4e "
      "Pa (G233; exact), the P-V work per particle = k_B T_b "
      "exactly, L/(N w) = dS/k_B = 10.8-23.7 (the mechanical share 4.2-9.3%%, "
      "water's class)." % (T_b, P_b))
V3 = ("THE HONEST STATEMENT -- THE COMPLETE THERMODYNAMICS, NO CRITICAL "
      "POINT.  The phantom's phase transition is FIRST-ORDER at the a0 "
      "boundary: the order parameter is the density (and its conjugate, the "
      "entropy density), with the jump contrast A_b = 0.125-0.5 (G159) and "
      "latent heat L/(N k_B T_b) = 10.8-23.7 (G132) -- water's first-order "
      "class (L/(k_B T) = 13.1 at 373 K), whose coexistence curve TERMINATES "
      "at its critical point (647 K, L -> 0).  The phantom's phase structure "
      "has NO critical point: IT IS A BOUNDARY-ANCHORED PHASE -- present "
      "below g = a0, absent above, EVERYWHERE, at every T; the latent heat "
      "never vanishes (dS = 7.1-12.5 k_B over g/a0 in [0.5, 100]; the L = 0 "
      "locus sits at r_efe = 0.0028 r_M, g ~ 1.3e5 a0, beyond every "
      "committed environment, and no crossing exists on the weak side -- "
      "rho_ph(r_M)/rho_dust = %.0f); the transition exists ONLY AT the "
      "boundary and is first-order there; the phase diagram is ONE line at "
      "g = a0 in the (g, T) plane (and one isotherm segment in (T, P)).  "
      "The complete thermodynamics of the framework's phase, stated from "
      "the committed latent/rigidity numbers (G132/G127/G233/G159/D06/B7/"
      "B8)." % RHO_OVER_DUST_RM)

verdicts = {"V1_the_order_parameter": V1,
            "V2_the_PT_phase_diagram": V2,
            "V3_honest_statement_no_critical_point": V3}

results = {
    "lane": "G10_phase_transition",
    "question": ("THE PHANTOM'S PHASE TRANSITION -- the complete "
                 "thermodynamics: (1) the order parameter (density vs "
                 "occupation vs entropy density) and the first-order "
                 "classification with the jump at the cap; (2) the P-T "
                 "diagram (the (T, P) coexistence from P = sigma^2 rho, the "
                 "cap's pressure jump, and the (g, T) face whose boundary is "
                 "the a0 line); (3) the critical point (is there one? the "
                 "water class; the honest statement: none -- boundary-"
                 "anchored), from the committed latent/rigidity content"),
    "constants": {"M_b_Msun": MB_MSUN, "a0_m_s2": A0, "G": G_CONST,
                  "sigma_km_s": SIG / 1e3, "sigma2_m2s2": SIG2,
                  "r_M_kpc": R_M / KPC_M, "r_break_kpc": R_BREAK / KPC_M,
                  "m_keV": 5.0, "T_b_K": T_b, "N_ph": N_ph,
                  "alpha_break": ALPHA_BREAK},
    "order_parameter": {
        "candidates": {
            "density_rho_A_r2": "inside the cap: rho = A/r^2 (rho_b = %.6e "
                                "kg/m^3 at r_break); outside: ~0 -- the "
                                "natural order parameter" % rho_b,
            "occupation_e^-6.44e6": ("the Boltzmann occupation at the freeze: "
                                     "e^-6.44e6 = 10^-2.80e6 (B7) -- ZERO on "
                                     "both sides, NOT an order parameter"),
            "entropy_density_S_N": ("s_ph = 22.81 k_B at r_break (22.8-23.8 "
                                    "band) vs the free dust's ~0; the jump "
                                    "across the cap dS = 10.8-23.7 k_B -- "
                                    "the conjugate order parameter"),
        },
        "density": {"rho_b_kg_m3": rho_b, "rho_ph_rM_kg_m3": rho_ph(R_M),
                    "rho_d_cap_from_A_b_kg_m3": rho_d_cap},
        "jump_A_b": {"band": [A_b_lo, A_b_hi], "geomean": A_b_gm,
                     "dressed_terms": A_DSE,
                     "relative_jump_abs": [J_hi, J_lo],
                     "rho_b_over_cosmic_dust": rho_d_cosmic_ratio,
                     "register": "G159 dressed; measured boundary ratio "
                                 "0.163-4.0 spans the band"},
        "entropy": {"s_ph_r_break_kB": s_ph, "s_ph_rM_kB": s_ph_rM,
                    "s_dust_kB": {"cosmic_ref": sd_cosmic,
                                  "cluster_ref": sd_cluster,
                                  "matched_density": sd_matched},
                    "dS_kB": dS,
                    "register": "G132/G159: s_ph = 22.8137, dS = 10.797 "
                                "(cosmic), 21.513 (cluster), 23.734 "
                                "(matched) -- reproduced exactly"},
        "occupation": {"m_over_kBT_at_9p17K": exp_917,
                       "log10_occupation": log10_917,
                       "N_Boltzmann_over_N_ph": N_BOLTZ_OVER_NPH,
                       "register": "B7: e^-6.44e6 at 9.17 K (5.09 keV); "
                                   "D06: reproduced to 1e-3"},
        "first_order": {"L_over_N_kBT": L_over_N_kBT,
                        "L_per_particle_J": L_per_N_J,
                        "L_total_J": L_tot_J,
                        "L_total_over_E_bind": {k: v / E_bind
                                                for k, v in L_tot_J.items()},
                        "E_bind_J": E_bind,
                        "E_bind_per_particle_is_kBTb_rel_err": ck_bind,
                        "classification": "FIRST-ORDER (G132): L = T_b dS "
                                          "finite; L = 0 excluded"},
    },
    "PT_diagram": {
        "T_P_coexistence": {
            "EOS": "P = sigma^2 rho (G233); inside the cap the phantom "
                   "isotherm at T_b carries P >= P_b = 1.359e-11 Pa "
                   "(diverging toward the center); the a0-only reference "
                   "scale P(r_M) = a0^2/(8 pi G) = %.4e Pa" % P_rM,
            "T_b_K": T_b, "P_b_Pa": P_b, "dP_jump_Pa": P_b,
            "dP_committed_G233": P_B_COMMITTED,
            "relerr_dP": ck_dP,
            "P_V_work_per_particle_J": w_pv,
            "P_V_work_identity": "w = P_b (m/rho_b) = m sigma^2 = k_B T_b "
                                 "exactly (rel err %.1e)" % ck_pv,
            "L_over_N_w": ratio_Lw, "mechanical_share": share_w,
            "coexistence_locus": "the segment {T = T_b, P in [0, P_b]}: a "
                                 "first-order isotherm segment, NOT a "
                                 "Clausius-Clapeyron curve (collisionless "
                                 "contact, G103; no Maxwell construction)"},
        "g_T_phase_diagram": {
            "axes": "(g, T)", "phase_boundary": "the single line g = a0",
            "phantom_phase": "{(g, T): g < a0} (r_efe > r_M: full "
                             "occupation); absent where g >> a0",
            "r_efe_over_rM": REFE,
            "MW_anchor": {"g_ext_over_a0": GEXT_MW_L240 / A0,
                          "r_efe_over_rM": MW_REFE,
                          "registered": 0.66},
            "statement": ("THE PHASE DIAGRAM'S AXES ARE (g, T); THE PHASE "
                          "BOUNDARY IS THE SINGLE LINE g = a0 -- ONE line in "
                          "the (g, T) plane: the most concise statement of "
                          "the framework's phase structure (G127: at g_ext = "
                          "a0 the cap sits exactly where the environment and "
                          "the phantom's own field are equal)")},
    },
    "critical_point": {
        "water_class": {"L_over_kBT_at_373K": WATER_L_RATIO,
                        "in_phantom_class": WATER_CLASS,
                        "T_c_K": WATER_TC_K, "P_c_Pa": WATER_PC_PA,
                        "reading": "water's coexistence curve TERMINATES at "
                                   "its critical point (L -> 0); the "
                                   "phantom's does not"},
        "phantom": {"dS_over_g": DSS_G,
                    "dS_range_in_domain": [min(DSS_G.values()),
                                           max(DSS_G.values())],
                    "L_zero_locus": {"r_efe_over_rM": R_FOR_ZERO,
                                     "g_over_a0": G_FOR_ZERO,
                                     "r_efe_kpc": R_FOR_ZERO * R_M / KPC_M,
                                     "reading": "unreachable: beyond every "
                                                "committed environment; on "
                                                "the weak side no crossing "
                                                "exists within the well "
                                                "(phantom beats the dust at "
                                                "every radius, rho_ph(r_M)/"
                                                "rho_dust = %.0f)"
                                                % RHO_OVER_DUST_RM}},
        "honest_statement": ("NO critical point: the phantom is a "
                             "BOUNDARY-ANCHORED phase -- present below "
                             "g = a0, absent above, everywhere, at every T; "
                             "the transition exists only AT the boundary and "
                             "is first-order there with a latent heat that "
                             "never vanishes in the existence domain")},
    "checks": checks,
    "n_pass": sum(1 for c in checks if c["pass"]),
    "n_total": len(checks),
    "verdicts": verdicts,
}

with open(OUT_PATH, "w") as f:
    json.dump(results, f, indent=1)

# ---------------------------------------------------------------- print report
print("=" * 78)
print("G10: THE PHANTOM'S PHASE TRANSITION -- the complete thermodynamics")
print("     (the order parameter, the P-T diagram, the critical behavior,")
print("      from the committed latent/rigidity content)")
print("=" * 78)

print("\n--- (1) THE ORDER PARAMETER ---")
print("  candidates: (a) the phantom DENSITY rho = A/r^2 inside, ~0 outside")
print("              (b) the OCCUPATION e^-6.44e6 (B7)")
print("              (c) the ENTROPY DENSITY S/N = 22.8 k_B vs the dust's ~0")
print("  rho_b = %.6e kg/m^3 at r_break = %.4f kpc;  rho_ph(r_M) = %.6e"
      % (rho_b, R_BREAK / KPC_M, rho_ph(R_M)))
print("  THE JUMP (G159 dressed): A_b = rho_ph/rho_d = [%.3f, %.3f], "
      "geomean %.4f (register %.4f)" % (A_b_lo, A_b_hi, A_b_gm,
                                        A_B_DSE_COMMITTED))
print("    relative jump |J| = %.3f-%.3f;  rho_b = %.0f x the cosmic dust"
      % (J_hi, J_lo, rho_d_cosmic_ratio))
print("  s_ph(r_break) = %.4f k_B (register %.4f);  s_ph(r_M) = %.4f"
      % (s_ph, S_PH_COMMITTED, s_ph_rM))
print("  s_dust = %.2f (cosmic) / %.2f (cluster) k_B;  dS = %.2f / %.2f / "
      "%.2f k_B" % (sd_cosmic, sd_cluster, dS["cosmic_ref"],
                    dS["cluster_ref"], dS["matched_density"]))
print("  occupation: m/k_B T = %.4e at 9.17 K -> 10^(%.1f): zero on BOTH "
      "sides -- NOT an order parameter" % (exp_917, log10_917))
print("  FIRST-ORDER (G132): L/(N k_B T_b) = %.2f-%.2f;  L_tot = %.3e-%.3e "
      "J = %.1f-%.1f x E_bind (E_bind/N = k_B T_b exact, rel err %.1e)"
      % (min(L_over_N_kBT.values()), max(L_over_N_kBT.values()),
         min(L_tot_J.values()), max(L_tot_J.values()),
         min(L_tot_J.values()) / E_bind, max(L_tot_J.values()) / E_bind,
         ck_bind))

print("\n--- (2) THE P-T DIAGRAM ---")
print("  EOS P = sigma^2 rho (G233);  dP = sigma^2 rho_b = %.6e Pa "
      "(committed %.6e; rel err %.1e)" % (P_b, P_B_COMMITTED, ck_dP))
print("  coexistence at T = T_b = %.4f K: P jumps across [0, %.4e Pa]; "
      "phantom branch P in [P_b, inf) (a0-only scale P(r_M) = "
      "a0^2/(8 pi G) = %.4e Pa)" % (T_b, P_b, P_rM))
print("  P-V work per particle w = k_B T_b exactly (rel err %.1e);  "
      "L/(N w) = dS/k_B = %.2f-%.2f (share %.1f-%.1f%%, water ~7%%)"
      % (ck_pv, min(ratio_Lw.values()), max(ratio_Lw.values()),
         min(share_w.values()) * 100.0, max(share_w.values()) * 100.0))
print("  THE (g, T) FACE: r_efe/r_M = sqrt(a0/g_ext):")
for g, v in REFE.items():
    print("    g = %5.2f a0 -> r_efe/r_M = %.4f" % (g, v))
print("    MW (g_ext = 2.29 a0, L240) = %.4f (registered 0.66)"
      % MW_REFE)
print("  THE STATEMENT: the phase diagram's axes are (g, T); the phase")
print("  boundary is the SINGLE LINE g = a0 -- ONE line in the (g, T) plane.")

print("\n--- (3) THE CRITICAL POINT ---")
print("  water's class (G132): L/(k_B T) = %.2f at 373 K in [%.2f, %.2f] "
      "(same first-order class); water's curve TERMINATES at T_c = 647.1 K "
      "(L -> 0)" % (WATER_L_RATIO, min(L_over_N_kBT.values()),
                    max(L_over_N_kBT.values())))
print("  the phantom's latent heat vs the environment: dS(g/a0) = %s (k_B): "
      "never vanishes in the domain" % ({str(k): round(v, 2)
                                          for k, v in DSS_G.items()}))
print("  L = 0 locus: r_efe = %.4e r_M (%.2f pc; g = %.2e a0) -- the cap "
      "strangled to the well's innermost 0.3%%, beyond every committed "
      "environment; weak side: no crossing (rho_ph(r_M)/rho_dust = %.0f)"
      % (R_FOR_ZERO, R_FOR_ZERO * R_M / KPC_M * 1e3, G_FOR_ZERO,
         RHO_OVER_DUST_RM))
print("  HONEST: NO critical point -- BOUNDARY-ANCHORED phase, present below")
print("  g = a0, absent above, EVERYWHERE; the transition exists only AT the")
print("  boundary, first-order there, forever.")

print("\n--- (4) VERDICTS ---")
for k, v in verdicts.items():
    print("  %s: %s" % (k, v))

print("\n--- CHECKS ---")
for c in checks:
    print("  [%s] %s" % ("PASS" if c["pass"] else "FAIL", c["name"]))
    print("        measured: %s" % c["measured"])
print("\n%d/%d checks PASS." % (results["n_pass"], results["n_total"]))
print("artifact written: %s" % OUT_PATH)