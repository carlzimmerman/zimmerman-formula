#!/usr/bin/env python3
"""
A42 -- THE MINIMAL VACUUM: beta = 0, Lambda_bare = 3 H0^2/c^2, and what the
theory predicts for cosmology.

Lane premise (from the task, and from A33 K16 / THEORY.md P3):
    beta = 0  =>  H^2 = 2 Lambda_bare c^2 / (3(2+3 beta)) = Lambda_bare c^2/3
    Lambda_bare = 3 H0^2/c^2  =>  H = H0,  rho_bare = rho_crit,
    a0 = kappa c sqrt(G rho_crit) = 1.132e-10 m/s^2.

What this script checks, in four blocks:

  T1  the chain, exactly (symbolic where it can be, SI numbers where it cannot);
  T2  the principal-positivity bound beta > 2 eta a0^2/K with eta = gamma =
      K L*^2/2, L* = 24 pc -- including the fact that beta = 0 is a *limit
      point* of the allowed interval, not an interior point;
  T3  the cosmology of Omega_Lambda,eff = 1: pure de Sitter, the census-filled
      flat case, the branch that actually keeps Lambda_bare = rho_crit with
      matter (beta = (2/3) Omega_m), and the beta = 0 + matter (closed) case;
  T4  the dark-energy budget: where the 1.462 excess goes, and whether the
      numbers close at beta = 0 (they do not; they close at beta = (2/3)Omega_m,
      at the price of a 24% shift in the expansion-history matter fraction).

Conventions.  SI throughout; the action's own units are c = 1 (MASTER_ACTION
section 1.1), so every restored-c^2 factor is stated where it enters.  K = 4 pi G.
H0 = 67.4 km/s/Mpc (the value A33/A18 use).  Omega_c = 0.2666, Omega_b = 0.0497
(the task's census), Omega_m = 0.3163, Omega_L = 0.6837.

Exit status 0 iff every check passes.  `--mutate <name>` breaks at least one
check and exits 1 (see MUTATE.md).
"""
import argparse
import json
import math
import sys

import numpy as np
import sympy as s
from scipy.integrate import quad

AP = argparse.ArgumentParser()
AP.add_argument('--mutate', default='none',
                choices=['none', 'beta0', 'kappa1', 'h0_73', 'no_c2',
                         'lam_obs', 'theta_gr'])
AP.add_argument('--json-out', default=None)
ARGS = AP.parse_args()
MUT = None if ARGS.mutate == 'none' else ARGS.mutate

CHECKS = []
NUMBERS = {}
TABLES = {}


def rec(cid, ok, value, threshold, note=''):
    CHECKS.append({'id': cid, 'pass': bool(ok), 'value': str(value),
                   'threshold': str(threshold), 'note': note})
    print('%-58s %s  value=%-30s threshold=%-12s %s'
          % (cid, 'PASS' if ok else 'FAIL', value, threshold, note))


def rel(a, b):
    a, b = float(a), float(b)
    d = max(abs(a), abs(b), 1e-300)
    return abs(a - b) / d


# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------
c = 2.99792458e8
G = 6.67430e-11
Mpc = 3.0856775814913673e22
pc = 3.0856775814913673e16
Gyr = 3.15576e16
H0_kms = 73.0 if MUT == 'h0_73' else 67.4
H0 = H0_kms * 1e3 / Mpc                       # s^-1
Om_c, Om_b = 0.2666, 0.0497
Om_m = Om_c + Om_b                            # 0.3163
Om_L = 1.0 - Om_m                             # 0.6837
kappa = 1.0 if MUT == 'kappa1' else 0.5
Lstar = 24.0 * pc                             # A20/A33: 24 pc (window 24-90)
a0_quoted = 1.132e-10                         # THEORY.md P3 / section 4
a0_quoted_alt = 1.1325e-10                    # task text
Lam_obs = 1.0890e-52                          # m^-2 (A33 table row 2)
Planck_Om = 0.3153                            # Planck 2018 TT,TE,EE+lowE+lens
Planck_Om_err = 0.0073
Planck_Ok = 0.0007                            # Planck 2018, BAO+CMB
Planck_Ok_err = 0.0019
Planck_age = 13.797                           # Gyr, Planck 2018

rho_crit = 3.0 * H0**2 / (8.0 * math.pi * G)
Lam_bare = 3.0 * H0**2 / c**2
if MUT == 'no_c2':
    Lam_bare = 3.0 * H0**2                    # mutation: drop the c^2
if MUT == 'lam_obs':
    Lam_bare = Lam_obs                        # mutation: Lambda_bare = Lambda_obs
rho_bare = Lam_bare * c**2 / (8.0 * math.pi * G)
a0 = kappa * c * math.sqrt(G * rho_bare)

NUMBERS['H0_kms'] = H0_kms
NUMBERS['H0_s'] = H0
NUMBERS['rho_crit_kg_m3'] = rho_crit
NUMBERS['rho_bare_kg_m3'] = rho_bare
NUMBERS['Lam_bare_m2'] = Lam_bare
NUMBERS['Lam_obs_m2'] = Lam_obs
NUMBERS['a0_m_s2'] = a0
NUMBERS['kappa'] = kappa
NUMBERS['Omega_m'] = Om_m
NUMBERS['Omega_L'] = Om_L
NUMBERS['Lstar_pc'] = Lstar / pc

# ===========================================================================
# T1 -- THE CHAIN
# ===========================================================================
print('=' * 118)
print('T1  THE CHAIN: beta = 0  =>  H^2 = Lambda_bare c^2/3  =>  H = H0,  rho_bare = rho_crit,'
      '  a0 = 0.5 c sqrt(G rho_crit)')
print('=' * 118)

H2s, Lam, rho_s, Ks, bet = s.symbols('H2 Lambda rho K beta', positive=True)
cs, H0s, Gs, Oms, kap = s.symbols('c H0 G Omega_m kappa', positive=True)

# (F1) of A33/MASTER_ACTION section 3.5, with c restored:
#     3 (2+3 beta) H^2 = 2 Lambda c^2 + 4 K rho
F1 = s.Eq(3 * (2 + 3 * bet) * H2s, 2 * Lam * cs**2 + 4 * Ks * rho_s)
F1_inG = F1.subs(Ks, 4 * s.pi * Gs)          # K = 4 pi G (MASTER_ACTION 1.1)
H2_sol = s.solve(F1, H2s)[0]

# K1: beta = 0, rho = 0  ->  H^2 = Lambda c^2/3
r1 = s.simplify(H2_sol.subs({bet: 0, rho_s: 0}) - Lam * cs**2 / 3)
rec('K1_beta0_gives_H2_eq_Lambda_c2_over_3', r1 == 0, r1, '0',
    'the task chain, from (F1); exact')

# K2: Lambda_bare = 3 H0^2/c^2  ->  H^2 = H0^2 identically
r2 = s.simplify(H2_sol.subs({bet: 0, rho_s: 0, Lam: 3 * H0s**2 / cs**2}) - H0s**2)
rec('K2_Lam_min_sets_H_eq_H0_identically', r2 == 0, r2, '0',
    'H = H0 for every z (empty universe): the de Sitter endpoint')

# K2b: (F1) from the minisuperspace action -- including the MATTER term, which A33's K10
#      (rho = 0) does not test.  This is the coefficient the whole of section 3(c) rests on.
tt = s.symbols('t', positive=True)
aa = s.Function('a')(tt)
ad = s.diff(aa, tt)
Nn = s.symbols('Nn', positive=True)
L_bg = (-3 * (2 + 3 * bet) * aa * ad**2 / (4 * Ks * Nn)
        - Lam * Nn * aa**3 / (2 * Ks) - rho_s * Nn * aa**3)
e_N = s.simplify(s.diff(L_bg, Nn).subs(Nn, 1))
H2_from_L = s.simplify(s.solve(e_N, ad**2)[0] / aa**2)      # c = 1 units
target_matter = (2 * Lam + 4 * Ks * rho_s) / (3 * (2 + 3 * bet))
r2b = s.simplify(H2_from_L - target_matter)
r2b_beta0 = s.simplify(H2_from_L.subs({bet: 0, Ks: 4 * s.pi * Gs})
                       - (Lam / 3 + 8 * s.pi * Gs * rho_s / 3))
rec('K2b_F1_from_minisuperspace_keeps_the_matter_term', (r2b == 0) and (r2b_beta0 == 0),
    'resid %s / %s' % (r2b, r2b_beta0), '0 / 0',
    'vary N of L_bg: 3(2+3beta)H^2 = 2Lambda + 4K rho; at beta=0 it is GR')
print('   => the (2+3 beta) factor multiplies the MATTER term, not only Lambda:')
print('      G_eff = 2G/(2+3beta) at fixed rho; with beta = (2/3)Omega_m, G_eff = G/(1+Omega_m)')

# K3: rho_bare = Lambda_bare c^2/(8 pi G) = rho_crit
ratio3 = rho_bare / rho_crit
rec('K3_rho_bare_eq_rho_crit', abs(ratio3 - 1.0) < 1e-14, '%.15f' % ratio3, '1 +- 1e-14',
    'Lambda_bare c^2/8 pi G = 3H0^2/8 pi G')

# K4 / K5: a0
pct4 = (a0 / a0_quoted - 1.0) * 100.0
pct5 = (a0 / a0_quoted_alt - 1.0) * 100.0
h0_for_quoted = H0_kms * a0_quoted / a0
rec('K4_a0_eq_half_c_sqrt_G_rho_crit', abs(pct4) < 0.2, '%.6e m/s^2' % a0,
    '|dev from 1.132e-10| < 0.2%', 'dev vs 1.132e-10: %+.4g%%' % pct4)
rec('K5_a0_percent_vs_quoted_values', abs(pct5) < 0.2, '%+.4g%% vs 1.1325e-10' % pct5,
    '|dev| < 0.2%', 'H0 that reproduces the quoted value: %.3f km/s/Mpc' % h0_for_quoted)
NUMBERS['a0_dev_vs_1p132e-10_pct'] = pct4
NUMBERS['a0_dev_vs_1p1325e-10_pct'] = pct5
NUMBERS['H0_for_quoted_a0_kms'] = h0_for_quoted
NUMBERS['a0_sparc_free_fit_A9'] = 1.1033e-10
NUMBERS['a0_dev_vs_A9_pct'] = (a0 / 1.1033e-10 - 1) * 100
NUMBERS['a0_canonical_footing'] = 0.5 * c * math.sqrt(G * Lam_obs * c**2 / (8 * math.pi * G))

# K6: the closure identity Lambda = 32 pi a0^2/c^4 <-> a0 = kappa c sqrt(G rho_bare)
a0s = s.symbols('a0', positive=True)
rho_of_Lam = Lam * cs**2 / (8 * s.pi * Gs)
a0_expr = kap * cs * s.sqrt(Gs * rho_of_Lam)
r6 = s.simplify(a0_expr.subs(kap, s.Rational(1, 2))**2 - Lam * cs**4 / (32 * s.pi))
rec('K6_Lam_eq_32pi_a0sq_over_c4_identity', r6 == 0, r6, '0',
    'identity, not a derivation: kappa = 1/2 <=> Lambda = 32 pi a0^2/c^4')
NUMBERS['Lam_from_32pi_a0sq'] = 32 * math.pi * a0**2 / c**4
NUMBERS['Lam_bare_over_Lam_obs'] = Lam_bare / Lam_obs
NUMBERS['one_over_Omega_L'] = 1.0 / Om_L

# K7: kappa = 1/2 is the normalisation that gives 1.132e-10 (a0 proportional to kappa)
a0_k1 = 1.0 * c * math.sqrt(G * rho_bare)
rec('K7_kappa_half_is_the_normalisation', abs(a0_k1 / a0 - 2.0) < 1e-12,
    'a0(kappa=1)/a0(kappa=1/2) = %.6f' % (a0_k1 / a0), '2',
    'a0 = 2.2624e-10 would be kappa = 1; the quoted value selects kappa = 1/2')
NUMBERS['a0_if_kappa_1'] = a0_k1

# ===========================================================================
# T2 -- PRINCIPAL POSITIVITY
# ===========================================================================
print()
print('=' * 118)
print('T2  PRINCIPAL POSITIVITY: beta > 2 eta a0^2/K with eta = gamma = K L*^2/2, L* = 24 pc')
print('=' * 118)

eta_s, gam_s, Ls = s.symbols('eta gamma Lstar', positive=True)
eta_def = Ks * Ls**2 / 2
rhs_sym = s.simplify(2 * eta_def * a0s**2 / Ks)          # eta = gamma = K L*^2/2
rec('K8_positivity_rhs_eq_a0Lstar_over_c2_sq',
    s.simplify(rhs_sym - Ls**2 * a0s**2) == 0, rhs_sym, 'L*^2 a0^2',
    'in c=1 units a0 has dimension 1/L, so the bound is (a0 L*/c^2)^2 in SI')
bound = (a0 * Lstar / c**2)**2
bound_can = (9.36e-11 * Lstar / c**2)**2
NUMBERS['positivity_rhs'] = bound
NUMBERS['positivity_rhs_canonical_footing'] = bound_can
NUMBERS['Lstar_over_LMOND'] = Lstar / (c**2 / a0)
print('   2 eta a0^2/K  =  (a0 L*/c^2)^2  =  (L*/L_MOND)^2  =  %.4e   [a0 = %.4e]'
      % (bound, a0))
print('   same on the canonical footing a0 = 9.36e-11:            %.4e' % bound_can)
print('   A3 K12 quotes 2(L* a0/c^2)^2 = 1.19e-18 on that footing  ->  %.4e  (cross-check)'
      % (2 * bound_can))

# K9: beta = 0 vs the bound -- indistinguishable at any achievable precision
gap = abs(0.0 - bound)
rec('K9_beta0_satisfies_bound_to_18_digits', gap < 1e-18,
    '|0 - %.4e| = %.4e' % (bound, gap), '< 1e-18',
    'beta = 0 sits below the bound by %.2e: identical at any physical precision' % gap)

# K10: but strictly, beta = 0 is NOT an interior point
rec('K10_strict_positivity_excludes_beta0', (bound > 0) and (bound < 1e-17),
    'violation = %.4e' % bound, '0 < violation < 1e-17',
    'the admissible set is {0} U (%.1e, inf): beta = 0 is a limit point' % bound)

# K11: the matter branch clears the bound by 17 orders
beta_branch = 2.0 * Om_m / 3.0                       # the analytic value (K18)
beta_used = 0.0 if MUT == 'beta0' else beta_branch   # what the cosmology block actually uses
rec('K11_matter_branch_beta_clears_bound', beta_used / bound > 1e16,
    'beta/bound = %.3e' % (beta_used / bound), '> 1e16',
    'beta = (2/3)Omega_m = %.6f' % beta_used)
NUMBERS['beta_branch'] = beta_branch
NUMBERS['beta_used_in_cosmology'] = beta_used
NUMBERS['beta_branch_over_bound'] = beta_used / bound
# the two readings of the bound's domain
NUMBERS['beta_min_strict'] = bound
NUMBERS['Lam_shift_from_beta_min'] = 1.5 * bound
print('   reading (i):  strict bound -> beta_min = %.4e, Lambda_bare = 3H0^2/c^2 x (1 + %.2e)'
      % (bound, 1.5 * bound))
print('   reading (ii): beta = 0 is the GR point (the deformed scalar is absent, B -> inf in A3 (S1))')
print('                 -> the bound has no domain there; both readings agree to 18 digits')

# ===========================================================================
# cosmology machinery
# ===========================================================================
print()
print('=' * 118)
print('T3  COSMOLOGY: Omega_Lambda,eff = 1 and the three ways to put matter in it')
print('=' * 118)


def E_of_z(z, kind, **kw):
    """E(z) = H(z)/H0 for the four backgrounds.

    'branch' is (F1) itself:  3(2+3 beta) H^2 = 2 Lambda_bare c^2 + 4 K rho_m(z), with
    Lambda_bare = 3 H0^2/c^2 and rho_m(z) = Omega_m rho_crit (1+z)^3, i.e.

        E^2 = 2 [1 + Omega_m (1+z)^3] / (2 + 3 beta).

    The `theta_gr` mutation replaces it by the naive flat-LCDM expression, which is the
    reading the task's phrasing invites (put the census in and set Omega_L = 1 - Omega_m,
    forgetting that Lambda_bare is rho_crit, not rho_DE).
    """
    z = np.asarray(z, dtype=float)
    if kind == 'ds':
        return np.ones_like(z)
    if kind == 'lcdm':
        om = kw['om']
        return np.sqrt(om * (1 + z)**3 + (1 - om))
    if kind == 'branch':
        om = kw['om']
        if MUT == 'theta_gr':
            return np.sqrt(om * (1 + z)**3 + (1 - om))
        bt = kw.get('bet', 2.0 * om / 3.0)
        return np.sqrt(2.0 * (1 + om * (1 + z)**3) / (2.0 + 3.0 * bt))
    if kind == 'closed':
        om = kw['om']
        ok = -om
        return np.sqrt(om * (1 + z)**3 + 1.0 + ok * (1 + z)**2)
    raise ValueError(kind)


def dc_Mpc(z, kind, h0=H0, **kw):
    f = lambda x: 1.0 / float(E_of_z(x, kind, **kw))
    return c / h0 * quad(f, 0.0, z, epsabs=1e-12, epsrel=1e-10, limit=400)[0] / Mpc


def age_Gyr(kind, h0=H0, **kw):
    if kind == 'ds':
        return float('inf')          # past-eternal: no Big Bang, no finite age
    f = lambda z: 1.0 / ((1 + z) * float(E_of_z(z, kind, **kw)))
    return quad(f, 0.0, np.inf, epsabs=1e-13, epsrel=1e-11, limit=800)[0] / h0 / Gyr


def q0(kind, **kw):
    if kind == 'ds':
        return -1.0
    om = kw['om']
    if kind == 'lcdm':
        return 0.5 * om - (1 - om)
    if kind == 'branch':
        ome = om / (1 + om)
        return 0.5 * ome - (1 - ome)
    if kind == 'closed':
        return 0.5 * om - 1.0
    raise ValueError(kind)


ZGRID = [0.0, 0.25, 0.5, 1.0, 2.0, 3.0]
models = {
    'a_pure_deSitter': ('ds', {}),
    'b_flat_census': ('lcdm', {'om': Om_m}),
    'c_branch_Lambar_rho_crit': ('branch', {'om': Om_m, 'bet': beta_used}),
    'd_beta0_plus_matter_closed': ('closed', {'om': Om_m}),
    'planck_lcdm': ('lcdm', {'om': Planck_Om}),
}
tab = {}
for name, (kind, kw) in models.items():
    _age = age_Gyr(kind, **kw)
    tab[name] = {'E': [float(E_of_z(z, kind, **kw)) for z in ZGRID],
                 'dc_Mpc': [dc_Mpc(z, kind, **kw) for z in ZGRID],
                 'age_Gyr': ('inf' if math.isinf(_age) else _age), 'q0': q0(kind, **kw)}
TABLES['z_grid'] = ZGRID
TABLES['backgrounds'] = tab

print('   %-30s %10s %10s %12s %12s %12s %8s' %
      ('model', 'E(0.5)', 'E(1)', 'dC(1) Mpc', 'dC(2) Mpc', 'age Gyr', 'q0'))
for name in models:
    t = tab[name]
    age_str = t['age_Gyr'] if isinstance(t['age_Gyr'], str) else '%.3f' % t['age_Gyr']
    print('   %-30s %10.4f %10.4f %12.1f %12.1f %12s %8.4f'
          % (name, t['E'][ZGRID.index(0.5)], t['E'][ZGRID.index(1.0)],
             t['dc_Mpc'][ZGRID.index(1.0)], t['dc_Mpc'][ZGRID.index(2.0)],
             age_str, t['q0']))

# K12: pure de Sitter -- E = 1, dC = (c/H0) z, and NO finite age (past-eternal)
ds = tab['a_pure_deSitter']
t_H = 1.0 / H0 / Gyr
t_part = lambda zmax: math.log(1.0 + zmax) / H0 / Gyr      # the divergent integral, cut at zmax
ok12 = (max(abs(np.array(ds['E']) - 1.0)) < 1e-15
        and rel(ds['dc_Mpc'][ZGRID.index(2.0)], 2.0 * c / H0 / Mpc) < 1e-10
        and rel(t_part(1e6) - t_part(1e3), math.log(1e3) / H0 / Gyr) < 1e-3
        and t_part(1e6) > 100.0)
rec('K12_deSitter_Ez_eq_one_no_big_bang', ok12,
    't(1e3)=%.1f, t(1e6)=%.1f Gyr (diverges)' % (t_part(1e3), t_part(1e6)),
    'E=1, no finite age', 'q0 = -1; dC = (c/H0) z; age integral = ln(1+z)/H0 -> inf')
NUMBERS['ds_hubble_time_Gyr'] = t_H
NUMBERS['ds_age_partial_1e3_Gyr'] = t_part(1e3)
NUMBERS['ds_age_partial_1e6_Gyr'] = t_part(1e6)

# K13: the flat census case must satisfy the closed-form flat-LCDM identities
fb = tab['b_flat_census']
t0_closed = (2.0 / (3.0 * H0 * math.sqrt(Om_L))) * math.asinh(math.sqrt(Om_L / Om_m)) / Gyr
q0_closed = 0.5 * Om_m - Om_L
E_closed = lambda z: math.sqrt(Om_m * (1 + z)**3 + Om_L)
ok13 = (rel(fb['age_Gyr'], t0_closed) < 1e-9
        and abs(fb['q0'] - q0_closed) < 1e-15
        and max(abs(float(E_of_z(z, 'lcdm', om=Om_m)) - E_closed(z)) for z in ZGRID) < 1e-14)
rec('K13_flat_census_matches_closed_form', ok13,
    'age=%.4f (closed form %.4f), q0=%.4f' % (fb['age_Gyr'], t0_closed, fb['q0']),
    '1e-9 / 1e-15',
    't0 = 2/(3H0 sqrt(OL)) asinh(sqrt(OL/Om)); dC1=%.1f, dC2=%.1f'
    % (fb['dc_Mpc'][ZGRID.index(1.0)], fb['dc_Mpc'][ZGRID.index(2.0)]))

# K14: integrator validation against Planck's own age
age_check = age_Gyr('lcdm', h0=67.36e3 / Mpc, om=Planck_Om)
rec('K14_integrator_validated_on_Planck_age', abs(age_check - Planck_age) < 0.05,
    '%.4f Gyr vs Planck %.3f' % (age_check, Planck_age), '|dev| < 0.05 Gyr',
    'radiation neglected: 0.03% on the age, <1e-4 on dC(z<3)')

# K15: de Sitter vs Planck-LCDM
pl = tab['planck_lcdm']
f15 = [(ds['dc_Mpc'][ZGRID.index(z)] / fb['dc_Mpc'][ZGRID.index(z)] - 1) * 100 for z in (1.0, 2.0)]
rec('K15_deSitter_vs_Planck_distance_fractions', min(f15) > 1.0,
    'z=1: %+.2f%%, z=2: %+.2f%%' % (f15[0], f15[1]), '> 1% both',
    'measurable, but the model has no matter: excluded by existence, not by distance')
NUMBERS['ds_vs_planck_dc_pct'] = f15
NUMBERS['ds_hubble_vs_planck_age_pct'] = (t_H / pl['age_Gyr'] - 1) * 100

# K16: fitting the observed expansion with beta = 0 forces Lambda_bare = Lambda_obs
#      (solve (F1) for Lambda at beta=0, H=H0, rho=rho_m) and hence a0 = 9.354e-11
Lam_needed = s.solve(F1_inG.subs({bet: 0, H2s: H0s**2,
                                  rho_s: Oms * 3 * H0s**2 / (8 * s.pi * Gs)}), Lam)[0]
Lam_needed_num = 3.0 * H0**2 * (1.0 - Om_m) / c**2
a0_b = 0.5 * c * math.sqrt(G * Lam_needed_num * c**2 / (8 * math.pi * G))
r16 = s.simplify(Lam_needed - 3 * H0s**2 * (1 - Oms) / cs**2)
rec('K16_case_b_forces_Lam_obs_and_a0_9p35e-11',
    (r16 == 0) and (abs(Lam_needed_num / Lam_obs - 1.0) < 2e-3) and (a0_b / a0_quoted < 0.9),
    'Lam_bare=%.4e, a0=%.4e' % (Lam_needed_num, a0_b), 'Lam_obs +- 0.2%, a0 < 0.9x',
    'so case (b) is exactly LCDM at the same Omega_m (difference 0) but loses the 1.132e-10 value')
NUMBERS['Lam_needed_case_b'] = Lam_needed_num
NUMBERS['a0_case_b'] = a0_b
NUMBERS['a0_case_b_dev_pct'] = (a0_b / a0_quoted - 1) * 100

# K17: case (b) at the census vs Planck at its own Omega_m
f17 = [(fb['dc_Mpc'][ZGRID.index(z)] / pl['dc_Mpc'][ZGRID.index(z)] - 1) * 100 for z in (1.0, 2.0)]
rec('K17_case_b_vs_Planck_Om_not_measurable', max(abs(x) for x in f17) < 0.3,
    'z=1: %+.4f%%, z=2: %+.4f%%' % (f17[0], f17[1]), '< 0.3% (Euclid)',
    'dOm = 0.0010: below any planned distance measurement')
NUMBERS['b_vs_planck_dc_pct'] = f17
NUMBERS['b_vs_planck_age_pct'] = (fb['age_Gyr'] / pl['age_Gyr'] - 1) * 100

# K18: the branch that keeps Lambda_bare = rho_crit with matter: beta = (2/3) Omega_m
beta_sol = s.solve(s.Eq(3 * (2 + 3 * bet) * H0s**2,
                        2 * (3 * H0s**2) + 4 * (4 * s.pi * Gs) * (Oms * 3 * H0s**2 / (8 * s.pi * Gs))), bet)
beta_sol = [s.simplify(b) for b in beta_sol]
rec('K18_matter_branch_beta_eq_two_thirds_Om',
    (len(beta_sol) == 1 and s.simplify(beta_sol[0] - 2 * Oms / 3) == 0
     and abs(beta_used - 2 * Om_m / 3) < 1e-15),
    '%s (used: %.6f)' % (beta_sol, beta_used), '2 Omega_m/3',
    'unique root of (F1) at H=H0, Lambda_bare = 3H0^2/c^2')
bet_num = float(beta_sol[0].subs(Oms, Om_m))
NUMBERS['beta_branch_symbolic_root'] = str(beta_sol[0])

# K19: the branch's E(z) is flat LCDM with Omega_m/(1+Omega_m)
Om_eff = Om_m / (1.0 + Om_m)
res19 = 0.0
for z in np.linspace(0, 5, 501):
    e1 = float(E_of_z(z, 'branch', om=Om_m, bet=beta_used))
    e2 = float(E_of_z(z, 'lcdm', om=Om_eff))
    res19 = max(res19, abs(e1 - e2))
# symbolic: (1+Om x)/(1+Om) = Om_eff x + 1 - Om_eff
xx = s.symbols('x', positive=True)
res19s = s.simplify((1 + Oms * xx) / (1 + Oms) - (Oms / (1 + Oms) * xx + 1 - Oms / (1 + Oms)))
rec('K19_branch_Ez_eq_LCDM_with_Om_over_1pOm',
    (res19 < 1e-13) and (res19s == 0),
    'Om_eff=%.6f, max|dE|=%.1e' % (Om_eff, res19), '< 1e-13',
    'the (2+3beta) factor rescales the matter term: Omega_m,eff = Omega_m/(1+Omega_m)')
NUMBERS['Omega_m_eff_branch'] = Om_eff
NUMBERS['G_eff_over_G_branch'] = 2.0 / (2.0 + 3.0 * beta_used)

# K20: the branch vs Planck-LCDM at the SAME Omega_m -- measurable and excluded
cb = tab['c_branch_Lambar_rho_crit']
f20 = [(cb['dc_Mpc'][ZGRID.index(z)] / fb['dc_Mpc'][ZGRID.index(z)] - 1) * 100 for z in (1.0, 2.0)]
h20 = [(cb['E'][ZGRID.index(z)] / fb['E'][ZGRID.index(z)] - 1) * 100 for z in (1.0, 2.0)]
f20p = [(cb['dc_Mpc'][ZGRID.index(z)] / pl['dc_Mpc'][ZGRID.index(z)] - 1) * 100 for z in (1.0, 2.0)]
h20p = [(cb['E'][ZGRID.index(z)] / pl['E'][ZGRID.index(z)] - 1) * 100 for z in (1.0, 2.0)]
sig20 = (Planck_Om - Om_eff) / Planck_Om_err
rec('K20_branch_vs_Planck_measurable_and_excluded',
    (min(f20) > 1.0) and (sig20 > 5.0),
    'dC: %+.2f%%/%+.2f%%; dH: %+.2f%%/%+.2f%%; %.1f sigma' % (f20[0], f20[1], h20[0], h20[1], sig20),
    '> 1% and > 5 sigma', 'same Omega_m = %.4f; vs Planck own Omega_m: dC %+.2f%%/%+.2f%%'
    % (Om_m, f20p[0], f20p[1]))
NUMBERS['branch_vs_planck_dc_pct'] = f20
NUMBERS['branch_vs_planck_E_pct'] = h20
NUMBERS['branch_vs_planckown_dc_pct'] = f20p
NUMBERS['branch_vs_planckown_E_pct'] = h20p
NUMBERS['branch_Om_eff_sigma'] = sig20
NUMBERS['branch_age_Gyr'] = cb['age_Gyr']
NUMBERS['branch_q0'] = cb['q0']
NUMBERS['b_age_Gyr'] = fb['age_Gyr']
NUMBERS['b_q0'] = fb['q0']
NUMBERS['ds_age_Gyr'] = ds['age_Gyr']
NUMBERS['ds_dc1_Mpc'] = ds['dc_Mpc'][ZGRID.index(1.0)]
NUMBERS['ds_dc2_Mpc'] = ds['dc_Mpc'][ZGRID.index(2.0)]
NUMBERS['b_dc1_Mpc'] = fb['dc_Mpc'][ZGRID.index(1.0)]
NUMBERS['b_dc2_Mpc'] = fb['dc_Mpc'][ZGRID.index(2.0)]
NUMBERS['branch_dc1_Mpc'] = cb['dc_Mpc'][ZGRID.index(1.0)]
NUMBERS['branch_dc2_Mpc'] = cb['dc_Mpc'][ZGRID.index(2.0)]
NUMBERS['planck_dc1_Mpc'] = pl['dc_Mpc'][ZGRID.index(1.0)]
NUMBERS['planck_dc2_Mpc'] = pl['dc_Mpc'][ZGRID.index(2.0)]
NUMBERS['planck_age_Gyr'] = pl['age_Gyr']
NUMBERS['planck_q0'] = pl['q0']
NUMBERS['c_over_H0_Mpc'] = c / H0 / Mpc

# K21: beta = 0 + matter + Lambda_bare = rho_crit is a CLOSED universe
cl = tab['d_beta0_plus_matter_closed']
Ok21 = 1.0 - (1.0 + Om_m)
H0_implied = H0 * math.sqrt(1.0 + Om_m)
a0_if_flat = kappa * c * math.sqrt(G * (1.0 + Om_m) * rho_crit)
rec('K21_beta0_plus_matter_gives_Omega_k_minus_Om', abs(Ok21 + Om_m) < 1e-15,
    'Omega_k = %+.4f, H0_implied = %.2f km/s/Mpc' % (Ok21, H0_implied * Mpc / 1e3),
    'Omega_k = -Omega_m',
    'equivalently flat with a0 = %.3e (%+.1f%%): the same mismatch, seen from a0'
    % (a0_if_flat, (a0_if_flat / a0 - 1) * 100))
NUMBERS['Omega_k_beta0_matter'] = Ok21
NUMBERS['H0_implied_beta0_matter_kms'] = H0_implied * Mpc / 1e3
NUMBERS['a0_if_flat_beta0_matter'] = a0_if_flat
NUMBERS['a0_if_flat_dev_pct'] = (a0_if_flat / a0_quoted - 1) * 100
NUMBERS['a0_if_flat_dev_vs_A9_pct'] = (a0_if_flat / 1.1033e-10 - 1) * 100

# K22: that curvature is excluded
sig22 = (Planck_Ok - Ok21) / Planck_Ok_err
rec('K22_Omega_k_excluded_by_Planck', sig22 > 50,
    'Omega_k = %+.4f  ->  %.0f sigma' % (Ok21, sig22), '> 50 sigma',
    'Planck+BAO: Omega_k = %.4f +- %.4f' % (Planck_Ok, Planck_Ok_err))
NUMBERS['Omega_k_sigma'] = sig22

# ===========================================================================
# T4 -- THE DARK-ENERGY BUDGET
# ===========================================================================
print()
print('=' * 118)
print('T4  THE BUDGET: where the 1.462 goes, and whether the numbers close at beta = 0')
print('=' * 118)

# K23: rho_beta = -9 beta H^2/(4K) is an exact rewriting of (F1), and at the branch it is -Omega_m rho_crit
rhob = s.symbols('rho_beta', real=True)
F1_rewritten = s.Eq(3 * H2s, Lam * cs**2 + 8 * s.pi * Gs * (rho_s - 9 * bet * H2s / (16 * s.pi * Gs)))
r23a = s.simplify(s.solve(F1_rewritten, H2s)[0] - s.solve(F1_inG, H2s)[0])
rho_beta_branch = -9.0 * beta_used * H0**2 / (4.0 * 4 * math.pi * G)
r23b = (rho_bare + rho_beta_branch) / ((1 - Om_m) * rho_crit)
rec('K23_rho_beta_identity_and_closure', (r23a == 0) and abs(r23b - 1.0) < 1e-14,
    'rho_beta/rho_crit = %.6f, (rho_bare+rho_beta)/rho_DE = %.12f'
    % (rho_beta_branch / rho_crit, r23b), '0 / 1',
    'the clock stress is exactly -Omega_m rho_crit at beta = (2/3)Omega_m')
NUMBERS['rho_beta_branch_kg_m3'] = rho_beta_branch
NUMBERS['rho_beta_over_rho_crit'] = rho_beta_branch / rho_crit
NUMBERS['rho_DE_kg_m3'] = (1 - Om_m) * rho_crit

# K24: the 1.462 excess is exactly the matter fraction
exc = (rho_crit - (1 - Om_m) * rho_crit) / rho_crit
rec('K24_excess_1p462_eq_one_over_Omega_DE',
    abs(exc - Om_m) < 1e-15 and abs(Lam_bare / Lam_obs - 1.0 / Om_L) < 1e-3,
    'Lam_bare/Lam_obs = %.5f vs 1/Omega_L = %.5f' % (Lam_bare / Lam_obs, 1.0 / Om_L),
    'agree to 1e-3',
    '(rho_crit - rho_DE)/rho_crit = Omega_m = %.4f exactly' % exc)
NUMBERS['excess_over_rho_crit'] = exc
NUMBERS['excess_kg_m3'] = rho_crit - (1 - Om_m) * rho_crit

# K25: the only beta = 0 closure is a constant NEGATIVE vacuum energy -Omega_m rho_crit
rho_x = -Om_m * rho_crit
res25 = 0.0
for z in np.linspace(0, 5, 501):
    e_cl = math.sqrt((Om_m * (1 + z)**3 * rho_crit + rho_crit + rho_x) / rho_crit)
    res25 = max(res25, abs(e_cl - float(E_of_z(z, 'lcdm', om=Om_m))))
rec('K25_only_beta0_closure_is_negative_vacuum', res25 < 1e-12,
    'rho_x = %.3e kg/m3, max|dE| = %.1e' % (rho_x, res25), '< 1e-12',
    'rho_x = -Omega_m rho_crit = -%.4f rho_bare: not in the action, and negative' % Om_m)
NUMBERS['rho_x_required_kg_m3'] = rho_x
NUMBERS['rho_x_over_rho_bare'] = rho_x / rho_bare

# the task's suggested resolution, taken with a POSITIVE cold vacuum: it overshoots
H0_pos_vac = H0 * math.sqrt(1.0 + Om_L)
NUMBERS['H0_if_positive_cold_vacuum_kms'] = H0_pos_vac * Mpc / 1e3
NUMBERS['Om_eff_h2'] = Om_eff * (H0_kms / 100.0)**2
NUMBERS['Planck_Om_h2'] = Planck_Om * (67.36 / 100.0)**2
print('   a positive cold vacuum of rho_DE on top of rho_bare would give H0 = %.1f km/s/Mpc'
      % (H0_pos_vac * Mpc / 1e3))
print('   the branch\'s Omega_m,eff h^2 = %.4f against Planck 0.1430 +- 0.0011'
      % (Om_eff * (H0_kms / 100.0)**2))

# K26: parameter count -- with Lambda_bare = 3H0^2/c^2 the background has ONE input
roots = s.solve(F1_inG.subs({Lam: 3 * H0s**2 / cs**2, H2s: H0s**2}), bet)
root_as_om = [s.simplify(r.subs(rho_s, Oms * 3 * H0s**2 / (8 * s.pi * Gs))) for r in roots]
rec('K26_one_cosmological_input_Omega_m',
    len(roots) == 1 and s.simplify(root_as_om[0] - 2 * Oms / 3) == 0,
    'beta = %s' % root_as_om, '2 Omega_m/3 (one root)',
    'inputs: Omega_m (census) + H0 (measured); Lambda_bare is tied to a0, beta is then predicted')
NUMBERS['cosmological_free_parameters'] = 1
NUMBERS['branch_prediction_E1'] = cb['E'][ZGRID.index(1.0)]
NUMBERS['branch_prediction_E2'] = cb['E'][ZGRID.index(2.0)]

# ===========================================================================
# summary
# ===========================================================================
print()
print('=' * 118)
npass = sum(1 for c_ in CHECKS if c_['pass'])
print('A42 COMPLETE: %d/%d checks PASS.' % (npass, len(CHECKS)))
if MUT:
    print('MUTATION: %s' % MUT)
print('=' * 118)

NUMBERS['n_checks'] = len(CHECKS)
NUMBERS['n_pass'] = npass

out = {
    'lane': 'A42_minimal_vacuum',
    'status': ('NO-GO(beta=0 as a cosmology: it forces Omega_m = 0); '
               'DERIVED(the chain, Lambda_bare = 3H0^2/c^2, a0 = 1.1312e-10, beta = (2/3)Omega_m); '
               'NUMERICAL(the background table and the 8.7% H(z=1) discrepancy)'),
    'mutation': str(MUT),
    'checks': CHECKS,
    'numbers': NUMBERS,
    'tables': TABLES,
    'constants_used': {
        'c': c, 'G': G, 'H0_kms': H0_kms, 'Omega_c': Om_c, 'Omega_b': Om_b,
        'Omega_m': Om_m, 'Lambda_obs_m2': Lam_obs, 'kappa': kappa,
        'Lstar_pc': 24.0, 'a0_quoted': a0_quoted,
        'Planck_Omega_m': Planck_Om, 'Planck_Omega_m_err': Planck_Om_err,
        'Planck_Omega_k': Planck_Ok, 'Planck_Omega_k_err': Planck_Ok_err,
        'Planck_age_Gyr': Planck_age,
    },
}
path = ARGS.json_out or 'a42_results.json'
if MUT:
    path = ARGS.json_out or ('a42_results_%s.json' % MUT.upper())
with open(path, 'w') as f:
    json.dump(out, f, indent=1)
print('wrote %s' % path)

sys.exit(0 if npass == len(CHECKS) else 1)
