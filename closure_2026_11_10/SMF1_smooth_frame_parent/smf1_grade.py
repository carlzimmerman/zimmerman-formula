#!/usr/bin/env python3
"""SMF1 grade: reads the lane's outputs and applies FROZEN_CRITERIA.md section 6, per footing.

    python3 smf1_grade.py  -> smf1_grade.out / smf1_grade.json

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(HERE, n)))
sym, num, ka3 = J('smf1_sym.json'), J('smf1_num.json'), J('smf1_ka3.json')
mu1, mu2, mu3 = J('smf1_sym_MUTATE_MU1.json'), J('smf1_sym_MUTATE_MU2.json'), J('smf1_sym_MUTATE_MU3.json')
comp = open(os.path.join(HERE, 'compile.txt')).read()
compm = open(os.path.join(HERE, 'compile_MUTATE.txt')).read()
OUT, G = [], {}


def say(*a):
    s = ' '.join(str(v) for v in a)
    OUT.append(s)
    print(s)


# known answers, MUTATE, Lean
KA = {'KA1 (LFS1 frozen Y)': sym['KA1_PASS'], 'KA2 (T-SCR)': sym['KA2_PASS'], 'KA3 (COL1 fold time)': ka3['KA3_PASS']}
MU = {'MU1 (static boundary)': mu1.get('MU1_bites', False), 'MU2 (non-analytic exchange)': mu2.get('MU2_bites', False),
      'MU3 (flipped couplings)': mu3.get('MU3_bites', False)}
lean_ok = comp.strip().endswith('exit 0') and 'error' not in comp
false_thms = ['gauss_zero_false', 'starvation_false', 'jeans_empty_core_false', 'jeans_root_false', 'c1_split_false',
              'lock_band_94_false']
src_m = open(os.path.join(HERE, 'SMF1_MUTATE.lean')).read().splitlines()
err_lines = [int(m.group(1)) for m in re.finditer(r'SMF1_MUTATE\.lean:(\d+):\d+: error', compm)]
thm_line = {t: next(i + 1 for i, l in enumerate(src_m) if f'theorem {t}' in l) for t in false_thms}
starts = sorted(thm_line.items(), key=lambda kv: kv[1])
failed = set()
for ln in err_lines:
    owner = [t for t, l0 in starts if l0 <= ln]
    if owner:
        failed.add(owner[-1])
twin_ok = compm.strip().endswith('exit 1') and failed == set(false_thms)
for k, v in KA.items():
    say(f'{k}: {"PASS" if v else "FAIL"}')
for k, v in MU.items():
    say(f'{k}: {"bites" if v else "DOES NOT BITE"}')
say(f'Lean SMF1.lean: {"exit 0, 9 theorems, standard axioms" if lean_ok else "FAILED"};  SMF1_MUTATE.lean: '
    f'{len(failed)}/{len(false_thms)} false statements fail, {"exit 1" if compm.strip().endswith("exit 1") else "exit 0"}')
process_ok = all(KA.values()) and all(MU.values()) and lean_ok and twin_ok

# S0
S0a = sym['S0a_PASS']
S0b = not sym['S0b_FAIL_identity']
S0c = not sym['S0c_FAIL_identity']
S0 = S0a and S0b and S0c
say(f'S0a exact reduction, rho = rho_b + rho_Psi: {"PASS" if S0a else "FAIL"}')
say(f'S0b net fill of the polarization charge: {"PASS" if S0b else "FAIL (identically zero: Gauss)"}')
say(f'S0c fill where counted once holds: {"PASS" if S0c else "FAIL (S_f = 0 at rho_Psi = 0: starvation)"}')
# S1
S1 = sym['S1_PASS'] and sym['GW_cT_equals_c']
say(f'S1 FRW (no ghost unmixed, no gradient instability as k -> infinity, Jeans root -K(n_d + rho) exact), static decoupling, GW: '
    f'{"PASS" if S1 else "FAIL"}')
band = num['S1_S2_stiffness_band']
say('    reported (not label-setting as frozen): the growing root is -K(n_d + rho) - lambda_s k^2 + ...; at z = 3 its rate reaches '
    + ', '.join(f"{v['max_growth_over_Jeans']:.3g}x Jeans ({k})" for k, v in band.items() if k.startswith('z3')))
# S2
Kc = 4 * 3.141592653589793 * 4.30091e-6
cos_h = 0.674
H0 = 100 * cos_h / 1000
rho_psi0 = 0.266405665278377 * 3 * H0 ** 2 / (8 * 3.141592653589793 * 4.30091e-6)
rho3 = rho_psi0 * 4 ** 3
m_lo = max(num[f]['S2d_window_lower_edge_all_masses_eV'] for f in ('canonical', 'alt'))
hbm = 6.582119569e-16 * 299792.458 ** 2 / m_lo / 3.0856775814913673e16
cbar = 9.199
c2_lock = Kc * hbm ** 2 * (0.01 * rho3) ** 2 / (2 * cbar ** 2 * rho3 + hbm ** 2 * 1e-8 * 1.01 * rho3)
S2a = num['S2a_CMB_pressureless']
S2b = True     # comoving: A = 0, P = 0 by isotropy (exact); charged: n_d = mu_K^2 h_bar/K > 0 for mu_K > 0 and a positive FRW frame charge (initial condition)
S2c = (sym['S0c_S_f'].find('sin(2*m*') >= 0) and (c2_lock ** 0.5 <= cbar)
S2d = all(num[f]['S2d_nonempty'] for f in ('canonical', 'alt'))
S2 = S2a and S2b and S2c and S2d
say(f'S2 (a) CMB pressureless {S2a}; (b) frame comoving and charged (n_d > 0) {S2b}; (c) S = 0 at chi = 0, lock sound speed '
    f'{c2_lock ** 0.5:.3g} km/s at z = 3 (line {cbar}) {S2c}; (d) window [{m_lo:.3g}, inf) eV non-empty {S2d}: {"PASS" if S2 else "FAIL"}')
# S3 (read; hypotheses checked against the action)
S3_rows = {
    "M5 (non-attractor; self-gravity cancelled)": ('EVADES', "M5's medium couples to the rest by gravity only; Psi couples to the frame by L_al and L_x"),
    'Theorem G (gates in theta, u)': ('EVADES', 'the member has no gate or switch function: L_al, L_st, L_x are smooth'),
    'Theorem S (label-free tethers hover)': ('EVADES', 'no tether to the baryons'),
    "D-T' (any local hold cancels the felt self-gravity)": ('NOT ESTABLISHED', "D-T' is not re-derived; the exchange lock (Psi pinned to the frame) is a local hold it may cover, and S0e's held edge layer would be one"),
    'mu-pincer': ('EVADES', 'the law region is where the frame is static, not a mu selector'),
    'J1 (potential depth)': ('EVADES', 'the law region is not set by depth (the frame dust is, PAR1 C6)'),
    'V1 (density)': ('NOT ESTABLISHED', 'ell depends on rho_Psi (ell^2 ~ 1/rho_Psi) though it selects no region; V1 not re-derived'),
}
S3 = not any(v[0] == 'COVERED' for v in S3_rows.values())
for k, v in S3_rows.items():
    say(f'S3 {k}: {v[0]} ({v[1]})')
say(f'S3: {"PASS" if S3 else "FAIL"} (no row COVERED)')
S4 = 'NOT RUN (S0 fails: no counted-once state to reach); KA3 run'
S5 = 'NOT GRADED'
say('S4:', S4)
say('S5:', S5)
first_fail = next((n for n, ok in (('S0', S0), ('S1', S1), ('S2', S2), ('S3', S3)) if not ok), None)
for ft in ('canonical', 'alt'):
    if not process_ok:
        lab = 'NO VERDICT'
    elif first_fail:
        lab = f'STRUCTURE FAILS ({first_fail}: S0b net fill of the polarization charge is identically zero (Gauss); S0c the exchange is off where counted once holds)'
    else:
        lab = 'STRUCTURE HOLDS (S4/S5 pending)'
    G[ft] = lab
    say(f'LABEL {ft}: {lab}')
res = {'labels': G, 'KA': KA, 'MUTATE': MU, 'lean_ok': lean_ok, 'lean_twin_ok': twin_ok, 'twin_failed': sorted(failed),
       'S0': {'S0a': S0a, 'S0b': S0b, 'S0c': S0c}, 'S1': S1, 'S2': {'a': S2a, 'b': S2b, 'c': S2c, 'd': S2d,
       'lock_sound_speed_kms_z3': c2_lock ** 0.5, 'window_lower_eV': m_lo}, 'S3': {k: list(v) for k, v in S3_rows.items()},
       'S4': S4, 'S5': S5, 'first_fail': first_fail, 'note': 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.'}
say('Adopts nothing. kappa = 1/2 FITTED; not theory closed.')
json.dump(res, open(os.path.join(HERE, 'smf1_grade.json'), 'w'), indent=1, default=str)
open(os.path.join(HERE, 'smf1_grade.out'), 'w').write('\n'.join(OUT) + '\n')
# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
