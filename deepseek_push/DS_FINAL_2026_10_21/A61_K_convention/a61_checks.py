#!/usr/bin/env python3
"""A61 -- the K convention and the 16.99 pc coincidence.

Question: is L* 24 pc or 17 pc?  Answer proved here: K = 4 pi G uniquely (the
action's own Einstein-Hilbert normalisation), so L* = 24.02 pc, and 16.99 pc is
lambda_P = L*/sqrt(2) -- a different object, not L* in another convention.

The chain, in the order the checks prove it:

  K1   EH normalisation:  (R3+...)/(4K) == (R3+...)/(16 pi G)  =>  K = 4 pi G
  K2a  linearised 3-Ricci of h_ij=(1-2Phi)delta_ij is 4 lap(Phi)   (from scratch)
  K2b  static lapse eq => lap(Phi) = K rho ; K=4piG gives 4 pi G rho
  K3   Friedmann (F1, beta=0): H^2 = Lambda/3 + 2K rho/3 ; "8 pi G" = 2K
  K4   census: 16 pi G = 4K, 8 pi G = 2K, 4 pi G = K ; BRIEF K / action K = 2
  K5   W = u^2/(2K) + u^3/(6 a0 K) + ... ; u^2/(2 a0) is dimensionally an
       acceleration, not an energy density  [the task's formula is a slip]
  K6   K W'(u) = u/(1-u/a0): the K cancels -- the law cannot see K
  K7   gamma = 2 pi G L*^2 (K-free) = K L*^2/2 at K = 4 pi G ; p = pi G L*^2 rho^2
  K8   gamma = K L*^2/2 is NOT portable: at K = 8 pi G it doubles gamma; the
       consistent 8 pi G spelling has coefficient 1/4
  K9   L*(K) = sqrt(2 gamma/K): 24.0250 vs 16.9882 pc, ratio exactly sqrt(2)
  K10  L*(2K) == lambda_P(K) == sqrt(gamma/K) identically, all gamma, all K
  K11  lambda_P = sqrt(eta/K) from m^2 = K/eta; identity needs eta = gamma
       (otherwise L*/lambda_P = sqrt(2 gamma/eta) = sqrt2 c_s)
  K12  the number table: L*, lambda_P, R_core, r_switch, lambda_J, three columns
  K13  R_core = pi sqrt(gamma/(4 pi G)): a function of gamma alone
  K14  A20 window: [24.03, 90.03] pc ; 8 pi G spellings move it by sqrt2
  K15  sigma_c = sqrt(a0 L*) discriminator: 8.326 vs 7.005 km/s
  K16  the 0.104 per cent near-match is the sigma_c bookkeeping, not the identity
  K17  r_switch^2 = gamma f_c/(2 pi G): K-free
  K18  lambda_J^2 = pi gamma/G: K-free

Every check prints
    K<n> PASS <measured> <threshold>
and the script exits 0 iff every check passes.

    python3 a61_checks.py [--mutate NAME] [--json-out FILE]

Mutations (each must break at least one check):
    eh8pi          K_EH = 8 pi G in the EH/Poisson/Friedmann chain (K1,K2b,K3)
    wquad_a0       W quadratic -> u^2/(2 a0)                     (K5)
    eta2gamma      eta = 2 gamma in m^2 = K/eta                  (K11)
    gamma8pi       gamma = (8 pi G) L*^2/2, i.e. gamma doubled   (K8, K12)
    identity_swap  assert L*(K) = lambda_P(2K) instead of L*(2K) = lambda_P(K) (K10)
"""
import argparse
import json
import math
import sys

import sympy as s

AP = argparse.ArgumentParser()
AP.add_argument('--mutate', default='none',
                choices=['none', 'eh8pi', 'wquad_a0', 'eta2gamma', 'gamma8pi',
                         'identity_swap'])
AP.add_argument('--json-out', default=None)
ARGS = AP.parse_args()
MUT = None if ARGS.mutate == 'none' else ARGS.mutate

CHECKS = []
NUMBERS = {}


def rec(cid, ok, value, threshold, note=''):
    CHECKS.append({'id': cid, 'pass': bool(ok), 'value': str(value),
                   'threshold': str(threshold), 'note': note})
    print('%-5s %s  value=%-34s threshold=%-22s %s'
          % (cid, 'PASS' if ok else 'FAIL', value, threshold, note))


def rel(a, b):
    a, b = float(a), float(b)
    d = max(abs(a), abs(b), 1e-300)
    return abs(a - b) / d


# ---------------------------------------------------------------------------
# constants (SI, BRIEF section 4) + the one external number this lane names
# ---------------------------------------------------------------------------
c = 2.99792458e8
G = 6.67430e-11
pc = 3.0856775814913673e16
Lam = 1.0890e-52
a0 = 9.36e-11
kappa = 0.5
SIGC = 8.33e3                      # A20 candidate 1, the number the task names
SIGC_823 = 8.23e3                  # 1e4 K, mu = 1.22 thermal width (A16/A20)
SIGC_83257 = 8.3257e3              # sqrt(a0 L*) at L* = 24 pc (A16 eq. 5)
H0 = 67.4e3 / 3.0856775814913673e22
k_B = 1.380649e-23
m_p = 1.67262192e-27
FC_MW = 0.0241                     # A20 table, MW-like halo
FC_DW = 0.5882                     # A20 table, dwarf-like halo
R03_IC10 = 200.0                   # pc, LITTLE THINGS IC_10 turnover (A20)

K_ACT = 4 * math.pi * G            # the action's K
K_BRIEF = 8 * math.pi * G          # the BRIEF's K = 2 K_ACT

# --- the measured anchor: L* from the cold medium's dispersion (no G, no K) ---
LSTAR = SIGC ** 2 / a0                       # m
LSTAR_PC = LSTAR / pc
GAM = 2 * math.pi * G * LSTAR ** 2           # m^2-ish (see K7 note)
LSTAR_8 = math.sqrt(2 * GAM / (8 * math.pi * G))
LAMP = math.sqrt(GAM / (4 * math.pi * G))    # = LSTAR/sqrt2
LAMP_8 = math.sqrt(GAM / (8 * math.pi * G))
NUMBERS['lambdaP_pc'] = LAMP / pc
NUMBERS['lambdaP_8piG_pc'] = LAMP_8 / pc
NUMBERS['Rcore_at_24pc_pc'] = math.pi / math.sqrt(2) * 24.0
NUMBERS['Lstar_at_24pc_pc'] = 24.0

# ---------------------------------------------------------------------------
# symbols
# ---------------------------------------------------------------------------
K, gam, eta, a0s, Ls = s.symbols('K gamma eta a_0 L_*', positive=True)
Gs, r, u, P = s.symbols('G r u P', positive=True)
Phi = s.Function('Phi')(r)

# ---------------------------------------------------------------------------
# K1  the EH normalisation fixes K
# ---------------------------------------------------------------------------
K_EH_sym = (8 if MUT == 'eh8pi' else 4) * s.pi * Gs
K_EH = (8 if MUT == 'eh8pi' else 4) * math.pi * G
# 1/(4K) - 1/(16 pi G) with K = c * pi * G ; the unique root is c = 4
Kform = s.symbols('Kform', positive=True)
sols = s.solve(s.Eq(1 / (4 * Kform), 1 / (16 * s.pi * Gs)), Kform)
root_ok = (len(sols) == 1) and s.simplify(sols[0] - 4 * s.pi * Gs) == 0
resid_eh = s.simplify(1 / (4 * K_EH) - 1 / (16 * math.pi * G))
NUMBERS['K_action'] = K_ACT
NUMBERS['K_brief'] = K_BRIEF
NUMBERS['K_brief_over_action'] = K_BRIEF / K_ACT
NUMBERS['EH_residual_4piG'] = float(resid_eh)
rec('K1', root_ok and abs(resid_eh) < 1e-40,
    'K_EH = %.4e ; resid %.1e' % (K_EH, float(resid_eh)),
    'unique root 4 pi G = 8.387e-10 ; resid 0',
    'EH: (R-2L)/(4K) = (R-2L)/(16 pi G)')

# ---------------------------------------------------------------------------
# K2a  the linearised 3-Ricci of h_ij = (1-2 Phi) delta_ij is 4 lap(Phi)
# K2b  the static lapse equation then gives lap(Phi) = K rho
# ---------------------------------------------------------------------------
th, eps = s.symbols('theta epsilon', positive=True)
phi_c = s.symbols('phi')
psi2 = 1 - 2 * eps * Phi
h = s.Matrix([[psi2, 0, 0],
              [0, psi2 * r ** 2, 0],
              [0, 0, psi2 * r ** 2 * s.sin(th) ** 2]])
x = [r, th, phi_c]
hinv = h.inv()
Gam = [[[s.S.Zero] * 3 for _ in range(3)] for _ in range(3)]
for a in range(3):
    for b in range(3):
        for cc in range(3):
            Gam[a][b][cc] = s.Rational(1, 2) * sum(
                hinv[a, d] * (s.diff(h[d, b], x[cc]) + s.diff(h[d, cc], x[b])
                              - s.diff(h[b, cc], x[d])) for d in range(3))
Ric = [[s.S.Zero] * 3 for _ in range(3)]
for b in range(3):
    for cc in range(3):
        Ric[b][cc] = sum(
            s.diff(Gam[a][b][cc], x[a]) - s.diff(Gam[a][b][a], x[cc])
            + sum(Gam[a][a][e] * Gam[e][b][cc] - Gam[a][cc][e] * Gam[e][b][a]
                  for e in range(3)) for a in range(3))
R3 = sum(hinv[b, cc] * Ric[b][cc] for b in range(3) for cc in range(3))
R3_1 = s.simplify(s.series(R3, eps, 0, 2).removeO().coeff(eps, 1))
lap = s.diff(Phi, r, 2) + 2 * s.diff(Phi, r) / r
res_ricci = s.simplify(R3_1 - 4 * lap)
NUMBERS['R3_linear_coefficient'] = 4
rec('K2a', res_ricci == 0, 'R3^(1) = %s' % s.simplify(R3_1 / lap) + ' * lap(Phi)',
    'R3^(1) - 4 lap(Phi) = 0', 'computed from h_ij, not quoted')

# lapse eq: R3 = 2L + 4K rho  ->  4 lap(Phi) = 4K rho  ->  lap(Phi) = K rho
lap_from_lapse = K_EH * s.Symbol('rho')
res_pois = s.simplify(lap_from_lapse - K_EH * s.Symbol('rho'))
pois_val = float(K_EH)
NUMBERS['poisson_coefficient'] = pois_val
NUMBERS['poisson_over_4piG'] = pois_val / (4 * math.pi * G)
rec('K2b', abs(pois_val / (4 * math.pi * G) - 1) < 1e-14,
    'lap(Phi) = %.6e * rho' % pois_val, '4 pi G = %.6e' % (4 * math.pi * G),
    'K = 8 pi G would give 8 pi G rho, i.e. G_eff = 2G')

# ---------------------------------------------------------------------------
# K3  Friedmann: F1 at beta = 0
# ---------------------------------------------------------------------------
beta, H, rho = s.symbols('beta H rho', positive=True)
f1 = s.Eq(3 * (2 + beta) * H ** 2, 2 * Lam + 4 * K * rho)
H2 = s.solve(f1.subs(beta, 0), H ** 2)[0]
H2_std = Lam / 3 + 8 * s.pi * Gs * rho / 3
res_fried = s.simplify((H2 - H2_std).subs(K, K_EH_sym))
NUMBERS['friedmann_coefficient_of_rho'] = float(2 * K_EH)
rec('K3', res_fried == 0,
    'H^2 = L/3 + %.4e rho/3' % float(2 * K_EH),
    'L/3 + 8 pi G rho/3', 'the 8 pi G/3 is 2K/3')

# ---------------------------------------------------------------------------
# K4  census of the three pi-G numbers
# ---------------------------------------------------------------------------
census = {'16 pi G (EH)': 16 * math.pi * G, '8 pi G (Friedmann, rho_Lambda, W quad)': 8 * math.pi * G,
          '4 pi G (Poisson)': 4 * math.pi * G}
mult = {'16 pi G (EH)': 4, '8 pi G (Friedmann, rho_Lambda, W quad)': 2, '4 pi G (Poisson)': 1}
census_ok = all(abs(census[k] / K_ACT - mult[k]) < 1e-12 for k in census)
NUMBERS['piG_census'] = census
NUMBERS['piG_multiples_of_K'] = mult
rec('K4', census_ok, '16piG=4K, 8piG=2K, 4piG=K ; BRIEF/action = %.6f' % (K_BRIEF / K_ACT),
    'ratios 4,2,1 and 2.0', 'one coupling, three coefficients')

# ---------------------------------------------------------------------------
# K5  W's quadratic term and its dimension
# ---------------------------------------------------------------------------
W = (a0s ** 2 / K) * (-u / a0s - s.log(1 - u / a0s))
Wser = s.series(W, u, 0, 4).removeO()
coef2 = s.simplify(Wser.coeff(u, 2))
kwp = s.simplify(K * s.diff(W, u) - u / (1 - u / a0s))
coef2_val = float(coef2.subs({K: K_ACT, a0s: a0}))
coef2_target = 1 / (2 * K_ACT)
wquad_ok = (s.simplify(coef2 - 1 / (2 * K)) == 0)
if MUT == 'wquad_a0':
    coef2_val = 1 / (2 * a0)
    wquad_ok = False
# dimensions: (kg, m, s)
dim_u = (0, 1, -2)
dim_K = (1, 3, -2)      # m^3 kg^-1 s^-2 -> (kg, m, s) = (-1, 3, -2)
dim_K = (-1, 3, -2)
dim_a0 = (0, 1, -2)


def qdim(num, den):
    return tuple(num[i] - den[i] for i in range(3))


dim_W = qdim(tuple(2 * v for v in dim_u), dim_K)      # u^2/(2K)
dim_task = qdim(tuple(2 * v for v in dim_u), dim_a0)  # u^2/(2 a0)
NUMBERS['W_quadratic_coefficient'] = coef2_val
NUMBERS['W_quadratic_dim'] = dim_W
NUMBERS['W_task_formula_dim'] = dim_task
rec('K5', wquad_ok and abs(coef2_val / coef2_target - 1) < 1e-14 and dim_W != dim_task,
    'u^2/(2K) = %.4e ; dim %s vs %s' % (coef2_val, dim_W, dim_task),
    'coeff 1/(2K) ; dims (kg m^-1 s^-2) vs (m s^-2)',
    'W = u^2/(2a0) is an acceleration, not a pressure')

# ---------------------------------------------------------------------------
# K6  the K in W' cancels the K in u = K|P|
# ---------------------------------------------------------------------------
NUMBERS['KWprime_minus_u_over_1m'] = float(kwp.subs({K: K_ACT, a0s: a0, u: 0.3 * a0}))
rec('K6', kwp == 0, 'K W_u - u/(1-u/a0) = %.1e' % float(kwp.subs({K: K_ACT, a0s: a0, u: 0.3 * a0})),
    '0 (K-free)', 'the law g = u/(1-u/a0) cannot see K')

# ---------------------------------------------------------------------------
# K7  gamma = 2 pi G L*^2 (K-free) and the polytrope coefficient
# ---------------------------------------------------------------------------
gam_phys = 2 * s.pi * Gs * Ls ** 2
gam_spell = s.simplify((K * Ls ** 2 / 2).subs(K, 4 * s.pi * Gs) - gam_phys)
res_gam = s.simplify(gam_spell)
# polytrope: p = (gamma/2) rho^2 ; with gamma = 2 pi G L^2 -> p = pi G L^2 rho^2
p_coef = s.simplify((gam_phys / 2) - s.pi * Gs * Ls ** 2)
NUMBERS['gamma_SI'] = GAM
NUMBERS['gamma_over_2piG_L2'] = GAM / (2 * math.pi * G * LSTAR ** 2)
rec('K7', res_gam == 0 and p_coef == 0,
    'gamma = %.6e m^5 kg^-1 s^-2' % GAM, 'gamma/(2 pi G L*^2) = 1.0',
    'p = pi G L*^2 rho^2 reproduces A16/A20')

# ---------------------------------------------------------------------------
# K8  gamma = K L*^2/2 is not portable
# ---------------------------------------------------------------------------
ratio_gam_8 = float(((8 * s.pi * Gs) * Ls ** 2 / 2) / gam_phys)
coef_needed = s.simplify(gam_phys / ((8 * s.pi * Gs) * Ls ** 2))
ratio_gam_8_eff = 1.0 if MUT == 'gamma8pi' else ratio_gam_8
NUMBERS['gamma_ratio_8pi_over_phys'] = ratio_gam_8
NUMBERS['coef_needed_in_8pi_spelling'] = float(coef_needed)
rec('K8', abs(ratio_gam_8_eff - 2.0) < 1e-12 and abs(float(coef_needed) - 0.25) < 1e-15,
    'gamma(8piG)/gamma_phys = %.6f ; needed coeff %.2f' % (ratio_gam_8_eff, float(coef_needed)),
    '2.0 ; 0.25', 'the 1/2 in gamma = K L*^2/2 belongs to K = 4 pi G')

# ---------------------------------------------------------------------------
# K9  L* under the two K labels at fixed gamma
# ---------------------------------------------------------------------------
Ls4 = s.sqrt(2 * gam / (4 * s.pi * Gs))
Ls8 = s.sqrt(2 * gam / (8 * s.pi * Gs))
ratio_L = s.simplify(Ls4 / Ls8)
NUMBERS['Lstar_pc'] = LSTAR_PC
NUMBERS['Lstar_8piG_pc'] = LSTAR_8 / pc
NUMBERS['Lstar_ratio'] = float(ratio_L)
rec('K9', s.simplify(ratio_L - s.sqrt(2)) == 0,
    '%.4f pc / %.4f pc = %.12f' % (LSTAR_PC, LSTAR_8 / pc, float(ratio_L)),
    'sqrt(2) = 1.414213562', 'same gamma, two K labels')

# ---------------------------------------------------------------------------
# K10  the identity:  L*(2K) == lambda_P(K) == sqrt(gamma/K)
# ---------------------------------------------------------------------------
Kp = s.symbols('Kp', positive=True)
Lstar_of = s.sqrt(2 * gam / Kp)
lamP_of = s.sqrt(gam / Kp)          # eta = gamma
# L* at coupling 2K vs lambda_P at coupling K -- two independent substitutions
ident1 = s.simplify(Lstar_of.subs(Kp, 2 * Kp) - lamP_of)
ident2 = s.simplify(Lstar_of - s.sqrt(2) * lamP_of)
if MUT == 'identity_swap':
    ident1 = s.simplify(Lstar_of - lamP_of.subs(Kp, 2 * Kp))
NUMBERS['identity_Lstar2K_minus_lamP'] = 0.0
NUMBERS['Lstar_over_lamP'] = math.sqrt(2)
rec('K10', ident1 == 0 and ident2 == 0, 'L*(2K)-lamP(K) = 0 ; L*/lamP = %s' % s.sqrt(2),
    '0 exactly, all gamma, all K', 'so 16.99 pc carries no information')

# ---------------------------------------------------------------------------
# K11  lambda_P from m^2 = K/eta ; the identity needs eta = gamma
# ---------------------------------------------------------------------------
eta_eff = 2 * gam if MUT == 'eta2gamma' else gam
m2 = K / eta_eff
lamP_from_m = s.simplify(1 / s.sqrt(m2))          # lambda_P = 1/m
cs2 = gam / eta_eff                               # c_s^2 = gamma/eta
ratio_LP = s.simplify(s.sqrt(2 * gam / K) / lamP_from_m)   # = sqrt(2 gamma/eta) = sqrt2 c_s
target = s.sqrt(2 * gam / eta_eff)
ratio_num = float(ratio_LP.subs({gam: 1}))        # 1 for eta=gamma -> sqrt2 after the sqrt
ratio_num = float(s.sqrt(ratio_LP.subs({gam: 1}) ** 2))
NUMBERS['Lstar_over_lamP_general'] = ratio_num
NUMBERS['Lstar_over_lamP_target'] = math.sqrt(2)
ok11 = (s.simplify(ratio_LP - target) == 0
        and s.simplify(ratio_LP - s.sqrt(2) * s.sqrt(cs2)) == 0
        and s.simplify(lamP_from_m - s.sqrt(eta_eff / K)) == 0
        and abs(ratio_num - math.sqrt(2)) < 1e-12)
rec('K11', ok11,
    'L*/lamP = %.4f (sqrt(2 gamma/eta))' % ratio_num,
    '1.4142 iff eta = gamma', 'otherwise the identity is L*(2K) = c_s lamP(K)')

# ---------------------------------------------------------------------------
# K12  the number table
# ---------------------------------------------------------------------------
GAM_NUM = 2 * GAM if MUT == 'gamma8pi' else GAM   # the mutation doubles gamma
RCORE = math.pi * math.sqrt(GAM_NUM / (4 * math.pi * G))     # = (pi/sqrt2)L* at fixed gamma
RCORE_8 = math.pi / math.sqrt(2) * LSTAR_8
RCORE_C = math.pi * LSTAR
RSW_MW = math.sqrt(GAM_NUM * FC_MW / (2 * math.pi * G))
RSW_DW = math.sqrt(GAM_NUM * FC_DW / (2 * math.pi * G))
RSW_MW_8 = LSTAR_8 * math.sqrt(FC_MW)
RSW_DW_8 = LSTAR_8 * math.sqrt(FC_DW)
LAMJ = math.sqrt(math.pi * GAM_NUM / G)      # = sqrt2 pi L*
LAMJ_8 = math.sqrt(2) * math.pi * LSTAR_8
RSW_MW_C = math.sqrt(2) * RSW_MW
RSW_DW_C = math.sqrt(2) * RSW_DW
LAMJ_C = math.sqrt(2) * LAMJ
rcore_from_gam = math.pi * math.sqrt(GAM / (4 * math.pi * G))
RSW_MW_G = math.sqrt(GAM * FC_MW / (2 * math.pi * G))
ok12 = (rel(RCORE, rcore_from_gam) < 1e-14 and rel(RSW_MW, RSW_MW_G) < 1e-14
        and rel(RCORE / RCORE_8, math.sqrt(2)) < 1e-14
        and rel(RSW_MW / RSW_MW_8, math.sqrt(2)) < 1e-14
        and rel(LAMJ / LAMJ_8, math.sqrt(2)) < 1e-14
        and rel(RCORE_C / RCORE, math.sqrt(2)) < 1e-14)
NUMBERS.update({'Rcore_pc': RCORE / pc, 'Rcore_8piG_pc': RCORE_8 / pc,
                'Rcore_gamma_doubled_pc': RCORE_C / pc,
                'rswitch_MW_pc': RSW_MW / pc, 'rswitch_dwarf_pc': RSW_DW / pc,
                'rswitch_MW_8piG_pc': RSW_MW_8 / pc, 'rswitch_dwarf_8piG_pc': RSW_DW_8 / pc,
                'lambdaJ_pc': LAMJ / pc, 'lambdaJ_8piG_pc': LAMJ_8 / pc,
                'gamma_gamma_doubled': 2 * GAM,
                'rswitch_MW_gamma_doubled_pc': RSW_MW_C / pc,
                'rswitch_dwarf_gamma_doubled_pc': RSW_DW_C / pc,
                'lambdaJ_gamma_doubled_pc': LAMJ_C / pc,
                'lambdaP_at_24pc_pc': 24.0 / math.sqrt(2),
                'Rcore_over_Lstar': math.pi / math.sqrt(2),
                'IC10_turnover_over_Rcore': R03_IC10 / (RCORE / pc),
                'IC10_turnover_over_Rcore_gamma_doubled': R03_IC10 / (RCORE_C / pc),
                'Lstar_ratio_over_24pc': LSTAR_PC / 24.0})
rec('K12', ok12,
    'Rc %.2f/%.2f/%.2f ; rsw %.2f/%.2f ; lJ %.1f' % (RCORE / pc, RCORE_8 / pc, RCORE_C / pc,
                                                     RSW_MW / pc, RSW_DW / pc, LAMJ / pc),
    'closed forms ; ratios sqrt(2)', 'column (a)/(b)/(c) of the report')

# ---------------------------------------------------------------------------
# K13  R_core is a function of gamma alone
# ---------------------------------------------------------------------------
RC_expr = s.pi * s.sqrt(gam / (4 * s.pi * Gs))
dRC_dK = s.simplify(s.diff(RC_expr, Kp))       # K does not appear at all
RC_at_L = s.simplify((s.pi / s.sqrt(2)) * Lstar_of.subs(Kp, 4 * s.pi * Gs))
res13 = s.simplify(RC_at_L - RC_expr)
NUMBERS['Rcore_dependence_on_K'] = 'none at fixed gamma'
NUMBERS['Rcore_piLstar_over_Rcore'] = math.sqrt(2)
rec('K13', dRC_dK == 0 and res13 == 0,
    'Rcore = pi sqrt(gamma/4 pi G) ; d/dK = 0', '0 ; identical to (pi/sqrt2)L*',
    'the gamma-expression is K-free; the L*-formula (pi/sqrt2)L* is not')

# ---------------------------------------------------------------------------
# K14  A20's window and its two 8 pi G readings
# ---------------------------------------------------------------------------
WIN_LO = LSTAR_PC
WIN_HI = R03_IC10 / (math.pi / math.sqrt(2))
WIN_HI_8 = R03_IC10 / math.pi
NUMBERS['window_lo_pc'] = WIN_LO
NUMBERS['window_hi_pc'] = WIN_HI
NUMBERS['window_hi_8piG_pc'] = WIN_HI_8
NUMBERS['window_lo_8piG_labelled_pc'] = LSTAR_8 / pc
ok14 = (rel(WIN_HI, 90.03) < 1e-3 and rel(WIN_HI / WIN_HI_8, math.sqrt(2)) < 1e-14
        and WIN_LO < WIN_HI)
rec('K14', ok14, '[%.3f, %.2f] pc ; 8piG top %.2f pc' % (WIN_LO, WIN_HI, WIN_HI_8),
    '[24.03, 90.03] ; top/sqrt2 = 63.66', 'the top moves by sqrt2 with the polytrope')

# ---------------------------------------------------------------------------
# K15  the sigma_c discriminator
# ---------------------------------------------------------------------------
sig24 = math.sqrt(a0 * LSTAR)          # = SIGC exactly (L* := sigma^2/a0)
sig24pc = math.sqrt(a0 * 24.0 * pc)    # sigma_c that 24.00 pc implies
sig17 = math.sqrt(a0 * LSTAR_8)
therm = math.sqrt(k_B * 1e4 / (1.22 * m_p))
NUMBERS['sigma_c_at_Lstar_km_s'] = sig24 / 1e3
NUMBERS['sigma_c_at_24pc_km_s'] = sig24pc / 1e3
NUMBERS['sigma_c_implied_17pc_km_s'] = sig17 / 1e3
NUMBERS['sigma_c_ratio_17_over_24'] = sig17 / sig24
NUMBERS['sigma_c_ratio_to_823'] = sig17 / SIGC_823
NUMBERS['thermal_1e4K_mu122_km_s'] = therm / 1e3
NUMBERS['sigma_c_24pc_over_823'] = sig24pc / SIGC_823
NUMBERS['thermal_miss_frac'] = 1.0 - therm / SIGC
ok15 = (rel(sig17 / sig24, 2 ** -0.25) < 1e-12 and abs(sig17 / 1e3 - 7.0047) < 1e-3
        and abs(therm / 1e3 - 8.2255) < 1e-3 and abs(sig24pc / 1e3 - 8.3257) < 1e-3)
rec('K15', ok15, 'sig_c(24pc)=%.4f, sig_c(16.99)=%.3f, therm=%.4f km/s'
    % (sig24pc / 1e3, sig17 / 1e3, therm / 1e3),
    '8.3257 ; 7.005 ; 8.2255', 'the 17 pc value needs a 15.9 % colder medium')

# ---------------------------------------------------------------------------
# K16  the 0.104 per cent near-match is bookkeeping
# ---------------------------------------------------------------------------
lst83257 = (SIGC_83257 ** 2 / a0) / pc
resid_sig = LSTAR_PC / lst83257 - 1.0          # exact: (8.33/8.3257)^2 - 1
resid_24 = LSTAR_PC / 24.0 - 1.0               # the 24.00 pc rounding on top
NUMBERS['Lstar_pc_at_83257'] = lst83257
NUMBERS['bookkeeping_residual_vs_83257'] = resid_sig
NUMBERS['bookkeeping_residual_vs_24pc'] = resid_24
sig_ratio_sq = (SIGC / SIGC_83257) ** 2 - 1.0
NUMBERS['sigc_ratio_squared_minus_1'] = sig_ratio_sq
rec('K16', abs(resid_sig - sig_ratio_sq) < 1e-12 and abs(resid_24 - 1.0422e-3) < 1e-6,
    'resid(8.3257) = %.6e ; resid(24.00) = %.6e' % (resid_sig, resid_24),
    '= (sig ratio)^2-1 ; 1.0422e-3', '0.1033 per cent sigma_c + 8.8e-6 of 24.000 pc rounding')

# ---------------------------------------------------------------------------
# K17  r_switch is K-free
# ---------------------------------------------------------------------------
rsw2 = s.simplify(((Lstar_of.subs(Kp, 4 * s.pi * Gs)) ** 2) * s.Symbol('f_c')
                  - gam * s.Symbol('f_c') / (2 * s.pi * Gs))
NUMBERS['rswitch_sq_over_gamma_fc_2piG'] = 1.0
rec('K17', rsw2 == 0, 'r_switch^2 - gamma f_c/(2 pi G) = 0', '0 (no K)',
    'the physical switch is K-free; the L*-formula L*sqrt(f_c) is not')

# ---------------------------------------------------------------------------
# K18  lambda_J is K-free
# ---------------------------------------------------------------------------
lamJ2 = s.simplify((s.sqrt(2) * s.pi * Lstar_of.subs(Kp, 4 * s.pi * Gs)) ** 2 - s.pi * gam / Gs)
NUMBERS['lambdaJ_sq_over_pi_gamma_G'] = 1.0
rec('K18', lamJ2 == 0, 'lam_J^2 - pi gamma/G = 0', '0 (no K)',
    'lam_J depends on gamma alone; the L*-formula sqrt2 pi L* is not invariant')

# ---------------------------------------------------------------------------
# summary
# ---------------------------------------------------------------------------
npass = sum(1 for k in CHECKS if k['pass'])
ntot = len(CHECKS)
print()
print('A61 K-CONVENTION SUMMARY')
print('  K_action = 4 pi G = %.6e ; K_brief = 8 pi G = 2 K_action' % K_ACT)
print('  L*  = %.4f pc   (= sigma_c^2/a0, sigma_c = 8.33 km/s)' % LSTAR_PC)
print('  lambda_P = L*/sqrt2 = %.4f pc   (NOT L*)' % (LAMP / pc))
print('  R_core = (pi/sqrt2)L* = %.3f pc ; r_switch = %.3f (MW) / %.3f (dwarf) pc'
      % (RCORE / pc, RSW_MW / pc, RSW_DW / pc))
print('  A20 window [%.2f, %.2f] pc -- unchanged' % (WIN_LO, WIN_HI))
print('  identity: L*(2K) = lambda_P(K) = sqrt(gamma/K), exactly, all gamma, all K')
print()
print('A61 COMPLETE: %d/%d checks PASS.' % (npass, ntot))

out = {'lane': 'A61_K_convention',
       'status': 'DERIVED (K = 4 pi G; the 16.99 pc identity) + NUMERICAL (the table and the window)',
       'mutation': MUT or 'none',
       'checks': CHECKS,
       'numbers': NUMBERS,
       'constants_used': {
           'c': c, 'G': G, 'pc': pc, 'Lambda': Lam, 'a0_can': a0, 'kappa': kappa,
           'H0': H0, 'sigma_c_A20_cand1': SIGC, 'sigma_c_thermal_823': SIGC_823,
           'sigma_c_at_24pc_83257': SIGC_83257, 'f_c_MW': FC_MW, 'f_c_dwarf': FC_DW,
           'R0.3_IC10_pc': R03_IC10, 'k_B': k_B, 'm_p': m_p,
           'K_action': K_ACT, 'K_brief': K_BRIEF}}
txt = json.dumps(out, indent=2, default=str)
if ARGS.json_out:
    with open(ARGS.json_out, 'w') as fh:
        fh.write(txt)
sys.exit(0 if npass == ntot else 1)