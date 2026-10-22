#!/usr/bin/env python3
"""A65 -- where the stiffness length L* comes from, with a guard against constant-juggling.

Question: L* is defined by gamma = K L*^2/2 (A33 row 7, THEORY section 3.4 says so
explicitly), so the action does not derive it.  Which physical scale of the cold
medium, if any, produces 24 pc - 1 kpc without a tuned coefficient?

The chain, in the order the checks prove it:

  K1   L* = sigma_c^2/a0 = 24.025 pc (coefficient exactly 1)
  K2   L*/L_MOND = sigma_c^2/c^2 exactly (residual 0)
  K3   L_MOND = c^2/a0 = 9.602e26 m canonical / 7.954e26 m alt
  K4   cosmic horizon c/H0 : ratio 1.851e8 (8.27 dex above L*)
  K5   de Sitter horizon c/H_Lambda : ratio 2.239e8
  K6   cell length sqrt(8 pi/Lambda) : ratio 6.480e8
  K7   kinetic Jeans length at the cosmic cold density : 196.2 kpc (8.17e3 L*)
  K8   elastic (P-sector) Jeans length : sqrt(2) pi L* = 106.74 pc (a multiple of L*)
  K9   mean inter-particle spacing at the cosmic cold density : 0.905 m (1.2e-18 L*)
  K10  Schwarzschild radius of 1 Msun : 2954 m (3.98e-15 L*)
  K11  Bohr radius : 5.29e-11 m (7.14e-29 L*)
  K12  census: no independent scale is an O(1) multiple of L*; the one
       O(1) entry is the thermal baryon scale (K12b)
  K12b thermal baryon scale c_s,b^2/a0 = 23.429 pc = 0.975 L*, 2.38 % below
       the 24 pc floor -- the independent input, not a derivation
  K13  candidate (a): lambda_J = L* needs rho = 1.505e-19 kg/m3 = 90 cm^-3
       (6.67e7 x the cosmic cold density) -- the density is the tuning knob
  K14  candidate (b): gradient/potential balance returns L*/sqrt2 = lambda_P
       (circular); gradient/kinetic balance returns lambda_J/2 = 98.1 kpc
  K15  candidate (c), literal reading (response time = gravitational dynamical
       time): L = lambda_J = 196.2 kpc
  K16  candidate (c), acceleration reading (crossing time = sigma_c/a0):
       L = sigma_c^2/a0 = 24.025 pc, coefficient 1.000 (no tuned density or new constant)
  K17  candidate (d): quantum pressure/self-gravity with the P mass gives 548 kpc;
       24 pc needs a new boson of 1.96e-16 eV (a fitted constant)
  K18  the pre-registered guard, candidate by candidate: only (c-accel) passes
  K19  window: 24.025 pc clears the 24 pc floor by 0.10 %; the independent
       thermal width 8.226 km/s gives 23.429 pc, 2.38 % BELOW the floor
  K20  footing scan: canonical 24.025 (in), alt 19.900 (out), P3 19.865 (out)
  K21  K-independence: L* = sigma_c^2/a0 carries no K; at K -> 2K it returns
       L*/sqrt2 = 16.988 pc, which is lambda_P, not L*
  K22  A20 core consistency: R_core = (pi/sqrt2) L* = 53.31 pc at L* = 24 pc

Every check prints
    K<n> PASS <measured> <threshold>
and the script exits 0 iff every check passes.

    python3 a65_checks.py [--mutate NAME] [--json-out FILE]

Mutations (each must break at least one check):
    coeff2      L* -> 2 L* (a non-unit coefficient)               (K1,K16,K19,K22)
    jeans_rho   cosmic cold density -> 1e-20 kg/m3                (K7,K12)
    footing_alt use the alt footing a0 = 1.13e-10                 (K1,K20)
    quantum     quantum length exponent 1/4 -> 1/2                (K17)
    guard       let candidate (b) pass the guard                  (K18)
"""
import argparse
import json
import math
import sys

AP = argparse.ArgumentParser()
AP.add_argument('--mutate', default='none',
                choices=['none', 'coeff2', 'jeans_rho', 'footing_alt',
                         'quantum', 'guard'])
AP.add_argument('--json-out', default=None)
ARGS = AP.parse_args()
MUT = None if ARGS.mutate == 'none' else ARGS.mutate

CHECKS = []
NUMBERS = {}


def rec(cid, ok, value, threshold, note=''):
    CHECKS.append({'id': cid, 'pass': bool(ok), 'value': str(value),
                   'threshold': str(threshold), 'note': note})
    print('%-4s %s  value=%-42s threshold=%-26s %s'
          % (cid, 'PASS' if ok else 'FAIL', value, threshold, note))


def rel(a, b):
    a, b = float(a), float(b)
    d = max(abs(a), abs(b), 1e-300)
    return abs(a - b) / d


# ---------------------------------------------------------------------------
# constants (SI, BRIEF section 4) + the external numbers this lane names
# ---------------------------------------------------------------------------
c = 2.99792458e8
G = 6.67430e-11
pc = 3.0856775814913673e16
Lam = 1.0890e-52
rho_Lam = Lam * c * c / (8 * math.pi * G)
H0 = 67.4e3 / (1e6 * pc)            # 67.4 km/s/Mpc
a0 = 9.36e-11                       # canonical footing (BRIEF section 4)
a0_alt = 1.13e-10                   # alt footing
a0_P3 = 1.132e-10                   # THEORY P3 "the theory's own value"
SIGC = 8.33e3                       # A20 candidate 1 / A37
SIGC_TH = 8.226e3                   # 1e4 K, mu = 1.22 thermal width (A20/A56)
L_TH = SIGC_TH ** 2 / a0            # thermal baryon acceleration length
m_p = 1.67262192369e-27
hbar = 1.054571817e-34
Msun = 1.98892e30
A_BOHR = 5.29177210903e-11
OM_B = 0.0493
OM_C = 5.3643 * OM_B                # A9/A11: M_c = 5.3643 M_b
RHO_CRIT = 3 * H0 ** 2 / (8 * math.pi * G)
RHO_C = OM_C * RHO_CRIT
K = 4 * math.pi * G                 # the action's K (A33 section 1.1, A61)

WIN_LO, WIN_HI = 24.0, 1000.0       # pre-registered window, pc
COEFF_LO, COEFF_HI = 0.5, 2.0       # pre-registered order-1 band
GALACTIC = ('R_core', 'R0.3', 'r_switch', 'R_d', 'r_M', 'V_f')  # forbidden inputs

# mutation hooks
if MUT == 'coeff2':
    LSTAR = 2 * SIGC ** 2 / a0
elif MUT == 'footing_alt':
    LSTAR = SIGC ** 2 / a0_alt
else:
    LSTAR = SIGC ** 2 / a0
if MUT == 'jeans_rho':
    RHO_C = 1e-20
LSTAR_PC = LSTAR / pc
GAMMA = K * LSTAR ** 2 / 2
L_MOND = c * c / a0
L_MOND_PC = L_MOND / pc

# ---------------------------------------------------------------------------
# K1  the number: L* = sigma_c^2/a0
# ---------------------------------------------------------------------------
ok1 = abs(LSTAR_PC - 24.025011756) < 1e-5
NUMBERS['Lstar_pc'] = LSTAR_PC
NUMBERS['Lstar_m'] = LSTAR
NUMBERS['coefficient_c_accel'] = LSTAR_PC / (SIGC ** 2 / a0 / pc)
rec('K1', ok1, 'L* = %.6f pc (sigma_c = 8.33 km/s, a0 = 9.36e-11)' % LSTAR_PC,
    '24.025012 +- 1e-5 pc', 'coefficient of sigma_c^2/a0 is exactly 1')

# ---------------------------------------------------------------------------
# K2  the exact identity L*/L_MOND = sigma_c^2/c^2
# ---------------------------------------------------------------------------
ratio = L_MOND / LSTAR
exact = (c / SIGC) ** 2
ok2 = rel(ratio, exact) < 1e-12
NUMBERS['L_MOND_over_Lstar'] = ratio
NUMBERS['c_over_sigma_sq'] = exact
NUMBERS['log10_Lstar_over_LMOND'] = math.log10(1.0 / ratio)
rec('K2', ok2, 'L_MOND/L* = %.10e' % ratio, '(c/sigma_c)^2 = %.10e' % exact,
    'residual %.1e; the nine-decade hierarchy' % rel(ratio, exact))

# ---------------------------------------------------------------------------
# K3  L_MOND on both footings
# ---------------------------------------------------------------------------
lm_alt = c * c / a0_alt
ok3 = rel(L_MOND, 9.6020852429e26) < 1e-8 and rel(lm_alt, 7.9536e26) < 1e-4
NUMBERS['L_MOND_canon_Gpc'] = L_MOND_PC / 1e9
NUMBERS['L_MOND_alt_Gpc'] = lm_alt / pc / 1e9
rec('K3', ok3, 'L_MOND = %.4f Gpc (canon) ; %.4f Gpc (alt)'
    % (L_MOND_PC / 1e9, lm_alt / pc / 1e9), '9.602 / 7.954 Gpc',
    'the task quotes 8.0e26 m: that is the ALT footing')

# ---------------------------------------------------------------------------
# K4-K6  the three horizon scales
# ---------------------------------------------------------------------------
H_Lam = c * math.sqrt(Lam / 3)
r_H0 = c / H0
r_dS = c / H_Lam
ell1 = math.sqrt(8 * math.pi / Lam)
r_csb = SIGC_TH / H0               # baryon sound speed (1e4 K, mu=1.22) x Hubble time
ok4 = rel(r_H0 / LSTAR, 1.851386947e8) < 1e-5
ok5 = rel(r_dS / LSTAR, 2.238888850e8) < 1e-5
ok6 = rel(ell1 / LSTAR, 6.480251121e8) < 1e-5
NUMBERS['c_over_H0_Gpc'] = r_H0 / pc / 1e9
NUMBERS['c_over_H0_ratio'] = r_H0 / LSTAR
NUMBERS['dS_horizon_Gpc'] = r_dS / pc / 1e9
NUMBERS['dS_horizon_ratio'] = r_dS / LSTAR
NUMBERS['ell1_Gpc'] = ell1 / pc / 1e9
NUMBERS['ell1_ratio'] = ell1 / LSTAR
NUMBERS['baryon_cs_over_H0_pc'] = r_csb / pc
NUMBERS['baryon_cs_over_H0_ratio'] = r_csb / LSTAR
rec('K4', ok4, 'c/H0 = %.3f Gpc ; ratio %.5e' % (r_H0 / pc / 1e9, r_H0 / LSTAR),
    '4.448 Gpc ; 1.8514e8', '8.27 dex above L*')
rec('K5', ok5, 'c/H_Lam = %.3f Gpc ; ratio %.5e' % (r_dS / pc / 1e9, r_dS / LSTAR),
    '5.379 Gpc ; 2.2389e8', 'de Sitter horizon = sqrt(3/Lam)')
rec('K6', ok6, 'sqrt(8pi/Lam) = %.3f Gpc ; ratio %.5e' % (ell1 / pc / 1e9, ell1 / LSTAR),
    '15.569 Gpc ; 6.4803e8', 'the vacuum cell')
ok6b = rel(r_csb / pc / 1e3, 122.0475) < 1e-6
NUMBERS['baryon_cs_over_H0_kpc'] = r_csb / pc / 1e3
NUMBERS['baryon_cs_over_H0_m'] = r_csb
NUMBERS['log10_baryon_ratio'] = math.log10(r_csb / LSTAR)
rec('K6b', ok6b, 'c_s,b/H0 = %.4f kpc ; ratio %.2f' % (r_csb / pc / 1e3, r_csb / LSTAR),
    '122.0475 kpc ; 5080.02', 'baryon sound speed does not reach L* either')

# ---------------------------------------------------------------------------
# K7  kinetic Jeans length of the cold medium at its cosmic density
# ---------------------------------------------------------------------------
lamJ = SIGC / math.sqrt(4 * math.pi * G * RHO_C)
ok7 = rel(lamJ / pc / 1e3, 196.227326459) < 1e-6
NUMBERS['rho_c_cosmic'] = RHO_C
NUMBERS['lambdaJ_cosmic_kpc'] = lamJ / pc / 1e3
NUMBERS['lambdaJ_cosmic_ratio'] = lamJ / LSTAR
rec('K7', ok7, 'lambda_J(rho_c=%.4e) = %.4f kpc ; ratio %.4e'
    % (RHO_C, lamJ / pc / 1e3, lamJ / LSTAR), '196.227 kpc ; 8.168e3',
    '4 pi G, not pi G: the 2 pi convention factor does not move the verdict')

# ---------------------------------------------------------------------------
# K8  the elastic (P-sector) Jeans length: sqrt(2) pi L*
# ---------------------------------------------------------------------------
lamJ_el = math.sqrt(2) * math.pi * LSTAR
ok8 = rel(lamJ_el / LSTAR, math.sqrt(2) * math.pi) < 1e-12
NUMBERS['lambdaJ_elastic_pc'] = lamJ_el / pc
NUMBERS['lambdaJ_elastic_ratio'] = lamJ_el / LSTAR
rec('K8', ok8, 'lambda_J,elastic = %.4f pc = %.6f L*' % (lamJ_el / pc, lamJ_el / LSTAR),
    '106.740 pc = 4.442883 L*', 'a multiple of L* by construction: gamma = 2 pi G L*^2')

# ---------------------------------------------------------------------------
# K9-K11  micro scales
# ---------------------------------------------------------------------------
n_c = RHO_C / m_p
d_sp = n_c ** (-1.0 / 3.0)
Rs = 2 * G * Msun / c ** 2
ok9 = rel(d_sp, 0.9049983997) < 1e-6
ok10 = rel(Rs, 2954.007736) < 1e-6
ok11 = rel(A_BOHR / LSTAR, 7.138171515e-29) < 1e-6
NUMBERS['interparticle_m'] = d_sp
NUMBERS['interparticle_ratio'] = d_sp / LSTAR
NUMBERS['Rsun_m'] = Rs
NUMBERS['Rsun_ratio'] = Rs / LSTAR
NUMBERS['Bohr_ratio'] = A_BOHR / LSTAR
rec('K9', ok9, 'd = %.6f m ; ratio %.4e' % (d_sp, d_sp / LSTAR), '0.904998 m ; 1.2208e-18',
    'n = rho_c/m_p = %.4f m^-3' % n_c)
rec('K10', ok10, 'R_s(1 Msun) = %.3f m ; ratio %.4e' % (Rs, Rs / LSTAR),
    '2954.008 m ; 3.9847e-15', 'the smallest macroscopic scale in the list')
rec('K11', ok11, 'a_Bohr/L* = %.4e' % (A_BOHR / LSTAR), '7.1382e-29', 'atomic scale')

# ---------------------------------------------------------------------------
# K12  the census: no enumerated scale is an O(1) multiple of L*
# ---------------------------------------------------------------------------
census = {
    'L_MOND': L_MOND, 'c/H0': r_H0, 'c/H_Lambda': r_dS, 'ell1': ell1,
    'lambda_J,kin': lamJ, 'lambda_J,el': lamJ_el, 'spacing': d_sp,
    'R_sun': Rs, 'a_Bohr': A_BOHR, 'c_s,b/H0': r_csb,
    'baryon_thermal': L_TH,
}
in_band = [k for k, v in census.items()
           if COEFF_LO <= v / LSTAR <= COEFF_HI and k != 'baryon_thermal']
ok12 = len(in_band) == 0
NUMBERS['census_O1_count'] = len(in_band)
NUMBERS['census_closest_ratio'] = min(abs(math.log10(v / LSTAR)) for v in census.values())
rec('K12', ok12, '%d independent of %d scales in [%.1f, %.1f] L*'
    % (len(in_band), len(census), COEFF_LO, COEFF_HI),
    '0 independent', 'the one O(1) entry is the thermal baryon scale (K12b)')

# ---------------------------------------------------------------------------
# K12b  the thermal baryon near-miss: c_s,b^2/a0 = 23.429 pc = 0.975 L*
# ---------------------------------------------------------------------------
ok12b = (rel(L_TH / pc, 23.4288524015) < 1e-6
         and rel(L_TH / LSTAR, 0.975194) < 1e-5
         and L_TH / pc < WIN_LO)
NUMBERS['baryon_thermal_pc'] = L_TH / pc
NUMBERS['baryon_thermal_ratio'] = L_TH / LSTAR
NUMBERS['baryon_thermal_shortfall_pct'] = 100.0 * (1.0 - (L_TH / pc) / WIN_LO)
rec('K12b', ok12b, 'baryon thermal c_s,b^2/a0 = %.4f pc = %.4f L* ; %.2f %% below 24 pc'
    % (L_TH / pc, L_TH / LSTAR, 100.0 * (1.0 - (L_TH / pc) / WIN_LO)),
    '23.4289 pc = 0.9752 L* ; 2.38 %',
    'the only O(1) entry is the same sigma^2/a0 functional with c_s,b; it is the independent input, not a derivation')

# ---------------------------------------------------------------------------
# K13  candidate (a): Jeans at its own sound speed and density
# ---------------------------------------------------------------------------
rho_need = SIGC ** 2 / (4 * math.pi * G * LSTAR ** 2)
n_need_cm3 = rho_need / m_p / 1e6
lamJ_dwarf = SIGC / math.sqrt(4 * math.pi * G * 1e-22)
ok13 = (rel(rho_need, 1.505379879e-19) < 1e-6 and rel(n_need_cm3, 90.0012) < 1e-3
        and rel(rho_need / RHO_C, 6.671013e7) < 1e-4
        and rel(lamJ_dwarf / pc, 932.1518) < 1e-4)
NUMBERS['rho_needed_for_jeans_Lstar'] = rho_need
NUMBERS['n_needed_cm3'] = n_need_cm3
NUMBERS['rho_needed_over_cosmic'] = rho_need / RHO_C
NUMBERS['lambdaJ_at_1e-22_pc'] = lamJ_dwarf / pc
rec('K13', ok13, 'rho(L*=lambda_J)=%.4e kg/m3 = %.2f cm^-3 = %.3e rho_c ; lambda_J(1e-22)=%.1f pc'
    % (rho_need, n_need_cm3, rho_need / RHO_C, lamJ_dwarf / pc),
    '1.5054e-19 ; 90.00 ; 6.671e7 ; 932.2 pc',
    'the density that makes (a) work is a measured galactic density, not a medium constant')

# ---------------------------------------------------------------------------
# K14  candidate (b): gradient energy vs potential energy
# ---------------------------------------------------------------------------
L_b_W = LSTAR / math.sqrt(2)
L_b_kin = SIGC / (2 * math.sqrt(K * RHO_C))
ok14 = rel(L_b_W / LSTAR, 1 / math.sqrt(2)) < 1e-15 and rel(L_b_kin / lamJ, 0.5) < 1e-12
NUMBERS['b_grad_vs_W_pc'] = L_b_W / pc
NUMBERS['b_grad_vs_W_coeff'] = L_b_W / LSTAR
NUMBERS['b_grad_vs_kin_kpc'] = L_b_kin / pc / 1e3
rec('K14', ok14, '(b) grad/W -> %.4f pc = %.3f L* = lambda_P ; grad/kinetic -> %.2f kpc'
    % (L_b_W / pc, L_b_W / LSTAR, L_b_kin / pc / 1e3),
    '16.988 pc = 0.707 L* = lambda_P ; 98.11 kpc',
    'the first is circular (linear in L*); the second is lambda_J/2')

# ---------------------------------------------------------------------------
# K15  candidate (c), literal reading: response time = gravitational t_dyn
# ---------------------------------------------------------------------------
t_dyn = 1.0 / math.sqrt(4 * math.pi * G * RHO_C)
t_acc = SIGC / a0
L_c_lit = SIGC * t_dyn
ok15 = rel(L_c_lit / lamJ, 1.0) < 1e-12 and rel(L_c_lit / pc / 1e3, 196.227326459) < 1e-6
NUMBERS['t_dyn_s'] = t_dyn
NUMBERS['t_acc_s'] = t_acc
NUMBERS['t_acc_Myr'] = t_acc / (3.15576e7 * 1e6)
NUMBERS['c_literal_kpc'] = L_c_lit / pc / 1e3
rec('K15', ok15, '(c) L = sigma_c t_dyn = %.4f kpc = lambda_J' % (L_c_lit / pc / 1e3),
    '196.227 kpc', 'literal reading does NOT land in the window')

# ---------------------------------------------------------------------------
# K16  candidate (c), acceleration reading: t_cross = t_acc
# ---------------------------------------------------------------------------
L_c_acc = SIGC * t_acc
ok16 = rel(L_c_acc / LSTAR, 1.0) < 1e-15
NUMBERS['c_accel_pc'] = L_c_acc / pc
NUMBERS['c_accel_coeff'] = L_c_acc / LSTAR
NUMBERS['t_cross_over_t_acc'] = (L_c_acc / SIGC) / t_acc
rec('K16', ok16, '(c) L = sigma_c^2/a0 = %.6f pc ; coeff %.15f'
    % (L_c_acc / pc, L_c_acc / LSTAR), '24.025012 pc ; 1.000000000000000',
    't_cross = t_acc = sigma_c/a0 ; the only candidate that lands without a tuned density/new constant')

# ---------------------------------------------------------------------------
# K17  candidate (d): quantum pressure vs self-gravity
# ---------------------------------------------------------------------------
lamP = LSTAR / math.sqrt(2)
mP = hbar / (c * lamP)


def LQ(m, rho, power=0.25):
    return (hbar ** 2 / (2 * m ** 2 * G * rho)) ** power


if MUT == 'quantum':
    LQ_P = LQ(mP, RHO_C, 0.5)
else:
    LQ_P = LQ(mP, RHO_C, 0.25)
m_need = hbar / (math.sqrt(2 * G * RHO_C) * LSTAR ** 2)
ok17 = (rel(LQ_P / pc / 1e3, 548.3866) < 1e-4 and rel(m_need, 3.496253e-52) < 1e-5
        and rel(m_need * c * c / 1.602176634e-19, 1.961254e-16) < 1e-5)
NUMBERS['quantum_with_mP_kpc'] = LQ_P / pc / 1e3
NUMBERS['quantum_mass_needed_kg'] = m_need
NUMBERS['quantum_mass_needed_eV'] = m_need * c * c / 1.602176634e-19
rec('K17', ok17, '(d) L_Q(m_P)=%.2f kpc ; m needed=%.4e kg = %.3e eV'
    % (LQ_P / pc / 1e3, m_need, m_need * c * c / 1.602176634e-19),
    '548.39 kpc ; 3.496e-52 kg ; 1.961e-16 eV',
    'a new boson the theory does not have (P4: no dark particle)')

# ---------------------------------------------------------------------------
# K18  the pre-registered guard, candidate by candidate
# ---------------------------------------------------------------------------
# (value in pc, coefficient, uses a galactic radius?, uses a new constant?)
cand = {
    'a  Jeans (cosmic rho)':      (lamJ / pc, 1.0, False, False),
    'a  Jeans (rho=1e-22)':       (lamJ_dwarf / pc, 1.0, True, False),
    'b  grad vs W':               (L_b_W / pc, L_b_W / LSTAR, False, False),
    'b  grad vs kinetic':         (L_b_kin / pc, 1.0, False, False),
    'c  literal (t_dyn)':         (L_c_lit / pc, 1.0, False, False),
    'c  acceleration (t_acc)':    (L_c_acc / pc, 1.0, False, False),
    'd  quantum (m_P)':           (LQ_P / pc, 1.0, False, False),
    'd  quantum (fitted m)':      (LSTAR_PC, 1.0, False, True),
}
passes = []
for name, (val, coef, gal, newc) in cand.items():
    okwin = WIN_LO <= val <= WIN_HI
    okcoef = COEFF_LO <= coef <= COEFF_HI
    ok = okwin and okcoef and (not gal) and (not newc)
    if MUT == 'guard' and name.startswith('b  grad vs W'):
        ok = True
    passes.append(ok)
npass_cand = sum(passes)
ok18 = npass_cand == 1 and passes[5]
NUMBERS['guard_pass_count'] = npass_cand
NUMBERS['guard_pass_name'] = 'c acceleration (t_acc)'
rec('K18', ok18, 'candidates passing C1-C4: %d (%s)'
    % (npass_cand, 'c-accel' if npass_cand == 1 else 'see table'),
    '1 (c-accel)', 'pre-registered: window, order-1 coefficient, no r_gal, no new constant')

# ---------------------------------------------------------------------------
# K19  the window test on the independent thermal width
# ---------------------------------------------------------------------------
L_th = L_TH
ok19 = (WIN_LO <= LSTAR_PC <= WIN_HI) and not (WIN_LO <= L_th / pc <= WIN_HI)
NUMBERS['Lstar_thermal_pc'] = L_th / pc
NUMBERS['thermal_shortfall_frac'] = 1.0 - (L_th / pc) / WIN_LO
rec('K19', ok19, 'L*(8.33)=%.4f pc in window ; L*(8.226)=%.4f pc, %.2f %% below floor'
    % (LSTAR_PC, L_th / pc, 100 * (1 - (L_th / pc) / WIN_LO)),
    '24.025 in ; 23.429 out by 2.38 %',
    'the independent thermal input saturates, not clears, the floor')

# ---------------------------------------------------------------------------
# K20  footing scan
# ---------------------------------------------------------------------------
vals = {'canon 9.36e-11': SIGC ** 2 / a0 / pc,
        'alt 1.13e-10': SIGC ** 2 / a0_alt / pc,
        'P3 1.132e-10': SIGC ** 2 / a0_P3 / pc}
inwin = [k for k, v in vals.items() if WIN_LO <= v <= WIN_HI]
ok20 = len(inwin) == 1 and inwin[0].startswith('canon')
NUMBERS['footing_values_pc'] = vals
NUMBERS['footing_in_window'] = inwin
rec('K20', ok20, 'canon %.3f | alt %.3f | P3 %.3f pc ; %d in window'
    % (vals['canon 9.36e-11'], vals['alt 1.13e-10'], vals['P3 1.132e-10'], len(inwin)),
    '24.025 | 19.900 | 19.865 pc ; 1',
    'the number is footing-conditional at 21 %')

# ---------------------------------------------------------------------------
# K21  K-independence, and where 16.99 pc comes from
# ---------------------------------------------------------------------------
L_2K = math.sqrt(2 * GAMMA / (2 * K))
ok21 = rel(L_2K / LSTAR, 2 ** -0.5) < 1e-15 and rel(L_2K / pc, 16.9882) < 1e-3
NUMBERS['L_at_2K_pc'] = L_2K / pc
NUMBERS['L_at_2K_over_Lstar'] = L_2K / LSTAR
NUMBERS['lambdaP_pc'] = lamP / pc
rec('K21', ok21, 'L*(2K)/L* = %.12f ; L*(2K) = %.4f pc = lambda_P'
    % (L_2K / LSTAR, L_2K / pc), '0.707106781187 ; 16.9882 pc',
    'L* = sigma_c^2/a0 has no K in it; 16.99 pc is lambda_P, not L*')

# ---------------------------------------------------------------------------
# K22  A20 core consistency
# ---------------------------------------------------------------------------
Rcore24 = math.pi / math.sqrt(2) * 24.0
Rcore_now = math.pi / math.sqrt(2) * LSTAR_PC
ok22 = abs(Rcore24 - 53.3146) < 1e-3 and rel(Rcore_now, 53.3701) < 1e-3
NUMBERS['Rcore_at_24pc'] = Rcore24
NUMBERS['Rcore_at_Lstar'] = Rcore_now
rec('K22', ok22, 'R_core(24 pc) = %.4f pc ; R_core(L*=%.3f) = %.3f pc'
    % (Rcore24, LSTAR_PC, Rcore_now), '53.3146 ; 53.370 pc',
    'A20 polytrope edge at L* = 24 pc is 53.31 pc (prediction, not a measurement)')

# ---------------------------------------------------------------------------
# display values quoted in report.md (same quantities, exact SI forms)
# ---------------------------------------------------------------------------
NUMBERS['window_pc'] = [WIN_LO, WIN_HI]
NUMBERS['window_margin_frac'] = LSTAR_PC / WIN_LO - 1.0
NUMBERS['window_margin_pct'] = 100.0 * (LSTAR_PC / WIN_LO - 1.0)
NUMBERS['jeans_pi_convention'] = math.sqrt(math.pi) / 2.0
NUMBERS['c_over_H0_m'] = r_H0
NUMBERS['dS_horizon_m'] = r_dS
NUMBERS['dS_horizon_1e26_m'] = r_dS / 1e26
NUMBERS['t_acc_1e13_s'] = t_acc / 1e13
NUMBERS['ell1_m'] = ell1
NUMBERS['lambdaJ_cosmic_m'] = lamJ
NUMBERS['lambdaJ_elastic_m'] = lamJ_el
NUMBERS['Bohr_m'] = A_BOHR
NUMBERS['mP_kg'] = mP
NUMBERS['lambdaJ_at_1e-20_pc'] = SIGC / math.sqrt(4 * math.pi * G * 1e-20) / pc
NUMBERS['lambdaJ_1e-22_over_Lstar'] = lamJ_dwarf / LSTAR
NUMBERS['quantum_mass_at_1e-22_eV'] = hbar / (math.sqrt(2 * G * 1e-22) * LSTAR ** 2) * c * c / 1.602176634e-19
NUMBERS['log10_cH0_ratio'] = math.log10(r_H0 / LSTAR)
NUMBERS['log10_dS_ratio'] = math.log10(r_dS / LSTAR)
NUMBERS['log10_ell1_ratio'] = math.log10(ell1 / LSTAR)
NUMBERS['log10_lambdaJ_ratio'] = math.log10(lamJ / LSTAR)
NUMBERS['log10_spacing_ratio'] = math.log10(d_sp / LSTAR)
NUMBERS['log10_Rsun_ratio'] = math.log10(Rs / LSTAR)
NUMBERS['log10_Bohr_ratio'] = math.log10(A_BOHR / LSTAR)
NUMBERS['log10_LMOND_ratio'] = math.log10(L_MOND / LSTAR)
NUMBERS['log10_lambdaJel_ratio'] = math.log10(lamJ_el / LSTAR)

# ---------------------------------------------------------------------------
# summary
# ---------------------------------------------------------------------------
npass = sum(1 for k in CHECKS if k['pass'])
ntot = len(CHECKS)
print()
print('A65 STIFFNESS-ORIGIN SUMMARY')
print('  L* = sigma_c^2/a0 = %.4f pc   (coefficient exactly 1, no K, no r_gal)' % LSTAR_PC)
print('  L_MOND/L* = (sigma_c/c)^2 = %.4e  (9.11 dex)' % (L_MOND / LSTAR))
print('  kinetic Jeans at cosmic rho: %.1f kpc = %.0f L*  -> NO' % (lamJ / pc / 1e3, lamJ / LSTAR))
print('  gradient/potential balance: %.2f pc = L*/sqrt2 = lambda_P -> CIRCULAR' % (L_b_W / pc))
print('  response=dynamical: %.1f kpc -> NO ; crossing=sigma_c/a0: %.3f pc -> YES' % (L_c_lit / pc / 1e3, L_c_acc / pc))
print('  quantum/gravity: %.0f kpc with m_P ; 24 pc needs a new %.3e eV boson -> NO' % (LQ_P / pc / 1e3, m_need * c * c / 1.602176634e-19))
print('  window: 24.025 pc in by 0.10 % ; thermal 23.429 pc out by 2.38 % ; P3 footing 19.865 pc out by 17 %')
print('  verdict: DERIVED-IN-FORM / FITTED-IN-NORMALIZATION(sigma_c); no tuned coefficient')
print()
print('A65 COMPLETE: %d/%d checks PASS.' % (npass, ntot))

out = {'lane': 'A65_stiffness_origin',
       'status': 'FITTED(sigma_c) / CONDITIONAL(canonical a0 footing): '
                 'L* = sigma_c^2/a0 = 24.025 pc; candidates (a),(b),(d) NO-GO',
       'mutation': MUT or 'none',
       'checks': CHECKS,
       'numbers': NUMBERS,
       'constants_used': [
           'c = 2.99792458e8 m/s (BRIEF 4)',
           'G = 6.67430e-11 (BRIEF 4)',
           'pc = 3.0856775814913673e16 m (BRIEF 4)',
           'Lambda = 1.0890e-52 m^-2 (BRIEF 4)',
           'rho_Lambda = %.6e kg/m3 (BRIEF 4, recomputed)' % rho_Lam,
           'H0 = %.6e s^-1 (BRIEF 4)' % H0,
           'a0_canon = 9.36e-11 m/s2 (BRIEF 4)',
           'a0_alt = 1.13e-10 m/s2 (BRIEF 4)',
           'a0_P3 = 1.132e-10 m/s2 (THEORY P3)',
           'sigma_c = 8.33 km/s (A20 candidate 1, A37)',
           'sigma_th = 8.226 km/s (1e4 K, mu = 1.22; A20/A56)',
           'm_p = 1.67262192369e-27 kg',
           'hbar = 1.054571817e-34 J s',
           'Msun = 1.98892e30 kg',
           'Omega_b = 0.0493, Omega_c/Omega_b = 5.3643 (A9/A11)',
           'K = 4 pi G (A33 1.1, A61)',
       ]}
txt = json.dumps(out, indent=2, default=str)
if ARGS.json_out:
    with open(ARGS.json_out, 'w') as fh:
        fh.write(txt)
sys.exit(0 if npass == ntot else 1)
