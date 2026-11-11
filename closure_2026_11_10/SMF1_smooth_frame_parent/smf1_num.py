#!/usr/bin/env python3
"""SMF1 numbers, per footing: S2 (m window, CMB pressure check, the stiffness band reported with S1), S0c (trade between the
counted-once violation and the fill rate), S0d (detuning and lock of the exchange in a static multi-stream well), S0e (what
a counted-once static state would need at the edge).

    python3 smf1_num.py  -> smf1_num.out / smf1_num.json

Inputs (read-only): PAR1 par1_numbers.json (C9 wells, forest line, C15), LFS1 lfs1_num.json (A1 fill rates, A2 edge
charges), smf1_sym.json (the FRW dispersion coefficients A, B, C). Units: kpc, km/s, Msun, Gyr, eV. Criteria:
FROZEN_CRITERIA.md sections 2 and 3. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, time
import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
T0 = time.time()
PAR1 = json.load(open(os.path.join(HERE, '../PAR1_parent_action_spec/par1_numbers.json')))
LFS1 = json.load(open(os.path.join(HERE, '../LFS1_leafwise_flux_supply/lfs1_num.json')))
SYM = json.load(open(os.path.join(HERE, 'smf1_sym.json')))
OUT, RES = [], {}


def say(*a):
    s = ' '.join(str(v) for v in a)
    OUT.append(s)
    print(s, flush=True)


# constants (SI cross-checked below)
G = 4.30091e-6                 # kpc (km/s)^2 / Msun
C_KMS = 299792.458
HBARC2 = 6.582119569e-16 * C_KMS ** 2          # eV s (km/s)^2
KPC_KM = 3.0856775814913673e16
GYR_S = 3.15576e16
A0 = {'canonical': 9.3603e-11, 'alt': 1.1312e-10}   # m/s^2
MASSES = ['9.4', '10.45', '10.7', '10.9']
CBAR = PAR1['S9_cbar_forest_kms']                   # 9.199 km/s, the record's forest line (PAR1 C9)
M_FOREST = PAR1['S15_m_min_record_forest_eV']       # 4.20e-24 eV (PAR1 C15)
M_LIT = PAR1['S15_m_min_literature_bracket_eV']     # 2e-21 eV (PROVISIONAL, reported only)
DELTA_MAX = 5.56 / 59.5                             # SHP1 R4 allowance


def hbar_over_m(m_eV):
    """hbar/m in kpc km/s."""
    return HBARC2 / m_eV / KPC_KM


def a0_kpc(a0_si):
    """a0 in (km/s)^2/kpc."""
    return a0_si * KPC_KM * 1e3 / 1e6


# SI cross-check of hbar/m (feedback: verify in SI): hbar/m [m^2/s] = 1.054571817e-34 / (m_eV * 1.602176634e-19 / c^2)
m_test = 1e-22
si = 1.054571817e-34 / (m_test * 1.602176634e-19 / 299792458.0 ** 2)
RES['SI_check_hbar_over_m_1e-22'] = {'kpc_kms': hbar_over_m(m_test), 'SI_m2_s': si,
                                    'SI_to_kpc_kms': si / (KPC_KM * 1e3) / 1e3, 'agree': abs(si / (KPC_KM * 1e3) / 1e3 / hbar_over_m(m_test) - 1) < 1e-6}
say(f"SI check: hbar/m at 1e-22 eV = {hbar_over_m(m_test):.5g} kpc km/s; SI {si:.5g} m^2/s -> {si / (KPC_KM * 1e3) / 1e3:.5g} kpc km/s")

for ft in ('canonical', 'alt'):
    say(f'\n=== footing {ft} (a0 = {A0[ft]:g} m/s^2) ===')
    R = {}
    a0k = a0_kpc(A0[ft])
    depth = PAR1['S9_sqrt_depth_kms'][ft]
    # ---- S2(d): the m window
    win = {}
    for ms in MASSES:
        Mb = 10 ** float(ms)
        sigma = (G * Mb * a0k) ** 0.25 / math.sqrt(2)        # the law's isothermal dispersion (FB1: sigma^2 = sqrt(G M a0)/2)
        m_ell = 2 * math.pi * HBARC2 / (sigma * 1.0 * KPC_KM)  # lambda_dB = 2 pi hbar/(m sigma) <= ell <= 1 kpc
        win[ms] = {'sigma_kms': sigma, 'm_min_ell_eV': m_ell, 'm_min_eV': max(m_ell, M_FOREST),
                   'lit_2e-21_inside': M_LIT >= max(m_ell, M_FOREST)}
        say(f"S2(d) log M_b {ms}: sigma {sigma:.1f} km/s; lambda_dB <= 1 kpc needs m >= {m_ell:.3g} eV; window [{max(m_ell, M_FOREST):.3g}, inf) eV;"
            f" published forest 2e-21 inside: {M_LIT >= max(m_ell, M_FOREST)}")
    m_lo = max(v['m_min_eV'] for v in win.values())
    R['S2d_window'] = win
    R['S2d_window_lower_edge_all_masses_eV'] = m_lo
    R['S2d_nonempty'] = True
    say(f"S2(d) window for every graded mass: [{m_lo:.3g}, inf) eV (no upper edge: C15 binds B-Tm-fine only). NON-EMPTY.")
    # ---- S0d: detuning and lock in the static well (depth from 10 kpc to R_ta, PAR1 C9)
    lam_need = {}
    for ms in MASSES:
        grid = LFS1['A'][ft][ms]['grid']
        lam_need[ms] = {f"{g['R_kpc']:.0f}_z{g['z']:g}": g['lam_s_perGyr'] for g in grid}
    s0d = {}
    for ms in MASSES:
        dphi = depth[ms]['10kpc_to_Rta'] ** 2              # (km/s)^2
        rows = {}
        for mv in (m_lo, 1e-22, M_LIT):
            w_det = dphi / hbar_over_m(mv)                  # (km/s)/kpc  (= m dPhi/hbar)
            T_det_gyr = 2 * math.pi / w_det * KPC_KM / GYR_S
            lam0 = min(v for k, v in lam_need[ms].items() if k.endswith('z0'))
            N_cyc = (1 / lam0) / T_det_gyr
            rows[f'{mv:.3g}'] = {'detuning_period_Myr': T_det_gyr * 1e3, 'cycles_per_fill_time_z0': N_cyc}
        band = {f'{g:g}': g / dphi for g in (CBAR ** 2, 30.0 ** 2, 100.0 ** 2)}
        s0d[ms] = {'depth_kms2': dphi, 'rows': rows, 'lock_band_fraction_gx_over_depth': band}
        say(f"S0d log M_b {ms}: depth {math.sqrt(dphi):.0f}^2 (km/s)^2; detuning period at m = {m_lo:.2g} / 1e-22 / 2e-21 eV: "
            + ' / '.join(f"{v['detuning_period_Myr']:.3g}" for v in rows.values()) + ' Myr; cycles per z0 fill time: '
            + ' / '.join(f"{v['cycles_per_fill_time_z0']:.3g}" for v in rows.values())
            + f"; lock band g_x/depth at g_x = 9.2^2 / 30^2 / 100^2: " + ' / '.join(f'{v:.2g}' for v in band.values()))
    R['S0d'] = s0d
    # ---- S0c trade: delta >= lam_need hbar/(g_x m f), f = duty (1 locked; g_x/depth unlocked, band average)
    s0c = {}
    for ms in MASSES:
        dphi = depth[ms]['10kpc_to_Rta'] ** 2
        lam0 = max(v for k, v in lam_need[ms].items() if k.endswith('z0'))
        lam2 = max(v for k, v in lam_need[ms].items() if k.endswith('z2'))
        out = {}
        for mv in (m_lo, M_LIT):
            q = lambda lam: lam / (GYR_S) * (HBARC2 / mv)        # (km/s)^2: lam_need * hbar/m in velocity^2
            locked = {'z0': q(lam0) / dphi, 'z2': q(lam2) / dphi}      # g_x = depth (just locked)
            gx_needed_unlocked = {'z0': math.sqrt(q(lam0) * dphi / DELTA_MAX), 'z2': math.sqrt(q(lam2) * dphi / DELTA_MAX)}
            out[f'{mv:.3g}'] = {'delta_min_locked': locked, 'gx_needed_unlocked_kms2_at_delta_max': gx_needed_unlocked,
                                'sqrt_gx_needed_kms': {k: math.sqrt(v) for k, v in gx_needed_unlocked.items()}}
        s0c[ms] = out
        o = out[f'{m_lo:.3g}']
        say(f"S0c log M_b {ms} (m = {m_lo:.2g} eV): locked delta_min {o['delta_min_locked']['z0']:.2g} (z0) / {o['delta_min_locked']['z2']:.2g} (z2);"
            f" unlocked band average needs sqrt(g_x) >= {o['sqrt_gx_needed_kms']['z0']:.3g} / {o['sqrt_gx_needed_kms']['z2']:.3g} km/s for delta <= {DELTA_MAX:.3f}")
    R['S0c_trade'] = s0c
    # ---- S0e: what a counted-once static state needs at the edge (LFS1 A2 read; Jeans; spin; frame dust)
    s0e = {}
    for ms in MASSES:
        e = LFS1['A'][ft][ms]['edge']['R_ta']
        s0e[ms] = {'R_s_kpc': e['R_s_kpc'], 'edge_charge_over_Mb': e['q_edge_over_Mb'], 'real_charge_needed_over_Mb': e['dust_needed_over_Mb'],
                   'cosmic_share': e['cosmic_share'], 'muK1_frame_dust_over_C': e.get('muK1_dust_over_C')}
        say(f"S0e log M_b {ms}: R_s = R_ta = {e['R_s_kpc']:.0f} kpc; polarization edge {e['q_edge_over_Mb']:.1f} M_b; real cold charge needed in the edge layer"
            f" {e['dust_needed_over_Mb']:.1f} M_b; frame dust at mu_K = 1/Mpc inside R_s: {e.get('muK1_dust_over_C', float('nan')):.3g} of it (LFS1 A2, read)")
    lam_req = 1 / math.sqrt(2)
    R['S0e'] = {'edge': s0e, 'spin_needed_for_centrifugal_shell_at_Rvir': lam_req, 'typical_spin_PROVISIONAL': 0.035,
                'ratio': lam_req / 0.035}
    say(f"S0e a Psi shell held by rotation at R_s ~ R_vir needs spin lambda' = j/(sqrt2 R V) = {lam_req:.2f}; accreted Psi has about 0.035"
        f" (Bullock+2001, PROVISIONAL): {lam_req / 0.035:.0f}x short. Psi made by the exchange is phase-locked to the frame (v = grad phi_f): zero circulation.")
    RES[ft] = R

# ---- S2(a) and the S1 stiffness band, in physical units at z = 3 and z = 1100 (footing-independent: a0 does not enter)
K, mu, hb, m, al, lam, gx, nd, rb, k = sp.symbols('K mu_K hbar m alpha lambda_s g_x n_d rhobar k', positive=True)
loc = {'K': K, 'mu_K': mu, 'hbar': hb, 'm': m, 'alpha': al, 'lambda_s': lam, 'g_x': gx, 'n_d': nd, 'rhobar': rb, 'k': k}
cf = [sp.lambdify((K, mu, hb, m, al, lam, gx, nd, rb, k), sp.sympify(SYM['S1_det_coeffs'][c], locals=loc), 'mpmath') for c in 'ABC']
mp.mp.dps = 40
cos = PAR1['cosmology']
H0 = 100 * cos['h'] / 1000                       # km/s/kpc
rho_crit0 = 3 * H0 ** 2 / (8 * math.pi * G)      # Msun/kpc^3
rho_psi0 = cos['Omega_c'] * rho_crit0
Kc = 4 * math.pi * G
MU_K = 1e-4        # 0.1 per Mpc (COL1's S4 galaxy bound) in 1/kpc; frame dust n_d = 0.01 rho_Psi; g_x = cbar^2; alpha = 1
# the grading form depends on hbar and m only through hbar/m: m = 1 and hbar = hbar/m below
m_lo = max(RES[f]['S2d_window_lower_edge_all_masses_eV'] for f in ('canonical', 'alt'))
band = {}
for z in (3.0, 1100.0):
    rho_z = rho_psi0 * (1 + z) ** 3
    for mv in (m_lo, M_LIT):
        hbm = hbar_over_m(mv)
        for ell_gal in (1.0, 0.1):
            # ell = 1 (or 0.1) kpc at the law's halo density at 10 kpc of log M_b 10.45 (rho ~ v^2/(4 pi G r^2), v = 137 km/s)
            rho_gal = 137.0 ** 2 / (4 * math.pi * G * 10.0 ** 2)
            lam_s = Kc * 1.0 * rho_gal * ell_gal ** 2          # (km/s)^2, alpha = 1
            vals = []
            for lk in [x / 8 for x in range(-24, 41)]:
                kv = mp.mpf(10) ** lk                             # 1/kpc physical
                a_, b_, c_ = [f(Kc, MU_K, hbm, 1.0, 1.0, lam_s, CBAR ** 2, 0.01 * rho_z, rho_z, kv) for f in cf]
                disc = b_ * b_ - 4 * a_ * c_
                lo = (-b_ - mp.sqrt(disc)) / (2 * a_)
                vals.append((float(kv), float(lo)))
            jeans = Kc * 1.01 * rho_z
            kmin = min(vals, key=lambda p: p[1])
            key = f'z{z:g}_m{mv:.2g}_ell{ell_gal:g}kpc'
            band[key] = {'lambda_s_kms2': lam_s, 'max_growth_over_Jeans': math.sqrt(-kmin[1] / jeans), 'at_k_per_kpc': kmin[0],
                         'ell_at_mean_kpc': math.sqrt(lam_s / (Kc * rho_z)),
                         'growth_over_Jeans_at_k_0.1_per_Mpc_comoving': None}
            # CMB-scale check (S2a): k = 0.1 per Mpc comoving
            kc = 1e-4 * (1 + z)
            a_, b_, c_ = [f(Kc, MU_K, hbm, 1.0, 1.0, lam_s, CBAR ** 2, 0.01 * rho_z, rho_z, mp.mpf(kc)) for f in cf]
            lo = (-b_ - mp.sqrt(b_ * b_ - 4 * a_ * c_)) / (2 * a_)
            band[key]['growth_over_Jeans_at_k_0.1_per_Mpc_comoving'] = math.sqrt(-float(lo) / jeans)
            say(f"S1/S2 band {key}: lambda_s = {lam_s:.3g} (km/s)^2 (ell at the mean density {band[key]['ell_at_mean_kpc']:.3g} kpc);"
                f" max growth rate / Jeans = {band[key]['max_growth_over_Jeans']:.3g} at k = {kmin[0]:.3g}/kpc;"
                f" at k = 0.1/Mpc comoving: {band[key]['growth_over_Jeans_at_k_0.1_per_Mpc_comoving']:.6f}")
RES['S1_S2_stiffness_band'] = band
RES['S2a_CMB_pressureless'] = all(abs(v['growth_over_Jeans_at_k_0.1_per_Mpc_comoving'] - 1) < 1e-3 for kk_, v in band.items() if kk_.startswith('z1100'))
say(f"S2(a) growth at k = 0.1/Mpc comoving, z = 1100, equals Jeans to 1e-3 in every row: {RES['S2a_CMB_pressureless']}")
RES['runtime_s'] = time.time() - T0
RES['note'] = 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.'
say(f'runtime {RES["runtime_s"]:.1f} s')
say('Adopts nothing. kappa = 1/2 FITTED; not theory closed.')
json.dump(RES, open(os.path.join(HERE, 'smf1_num.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'smf1_num.out'), 'w').write('\n'.join(OUT) + '\n')
# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
