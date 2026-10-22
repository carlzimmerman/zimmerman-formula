#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A76 -- CLOSE L*: is the stiffness length fitted, or derived from a measured sigma_c?

Every check evaluates an expression or a data value and compares it with an
independently computed value (a second formula, a second parse of the same file,
or a published number from another lane).  No check asserts a constant.
Run with A76_MUTATE=<name> to change ONE input; the named checks must then fail
(see MUTATE.md).  exit 0 iff every check passes.

Data (read-only, never modified, never copied into the repo):
  _external_data/little_things_oh2015/{table2.dat, rotdmbar.dat}   Oh+2015
  real_research/data/sparc_data/*_rotmod.dat                        175 curves
  _external_data/hi_profiles_2026_10_18/*.fits                      21 ALFALFA spectra

Constants: BRIEF 4 plus the lanes named in each check.  K = 4 pi G (A16/A61), the
convention in which the task's identity L*^2 = 2 c_s^2/(K rho_c) is claimed exact.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
LT_CANDIDATES = [os.path.join(os.path.dirname(ROOT), '_external_data', 'little_things_oh2015'),
                 os.path.join(ROOT, '_external_data', 'little_things_oh2015')]
SPARC_DIR = os.path.join(ROOT, 'real_research', 'data', 'sparc_data')
ALFALFA_DIR = os.path.join(ROOT, '_external_data', 'hi_profiles_2026_10_18')
sys.path.insert(0, HERE)

MUT = os.environ.get('A76_MUTATE', '').strip()

# --------------------------------------------------------------------------- inputs
BASE = dict(
    c=2.99792458e8,               # m/s          BRIEF 4
    G=6.67430e-11,                # m3/kg/s2     BRIEF 4
    pc=3.0856775814913673e16,     # m            BRIEF 4
    Mpc=3.0856775814913673e22,    # m            BRIEF 4
    Msun=1.98892e30,              # kg           IAU
    kB=1.380649e-23,              # J/K          SI exact
    mH=1.67262192e-27,            # kg           CODATA hydrogen atom
    hbar=1.054571817e-34,
    H0=2.1843e-18,                # 1/s          BRIEF 4
    Lambda=1.0890e-52,            # 1/m2         BRIEF 4
    omega_b=0.02237,              #              A18 (CFG515)
    rho_crit_h1=1.87847e-26,      # kg/m3        rho_crit at h=1
    ratio_cb=5.364327,            # (1-f_b)/f_b  A11/A18
    rho_c=2.2565e-27,             # kg/m3        A16/A20 (cosmic cold sector)
    K_factor=4.0 * math.pi,       # K = 4 pi G   A16 / A61
    a0_can=9.36e-11,              # m/s2         BRIEF 4
    a0_k12=9.354746e-11,          # m/s2         A72 (1/7 x cH0 == kappa = 1/2)
    a0_th=8.618166e-11,           # m/s2         A72 (cH_Lambda/2pi, thermal)
    a0_alt=1.13e-10,              # m/s2         BRIEF 4 (P3 footing)
    T_cold=1.0e4,                 # K            A11 15 / AG6D B7
    mu=1.22,                      #              A11 15 (neutral, He included)
    sigma_th_quoted=8226.0,       # m/s          A65/A20 quoted 8.226 km/s
    Lstar_anchor=24.0,            # pc           A20 C3 floor (the round number)
    Lstar_th_quoted=23.4289,      # pc           A65 K19
    Rc_at_24=53.3146,             # pc           A20 K3
    Rc_at_23p4289=52.05,          # pc           task/A65 arithmetic
    margin_C1=0.001042,           #              A65: 24.0250 clears 24 pc by 0.1042 %
    spread_quoted=0.0855,         #              A72: a0(1/Z) vs a0(1/2pi), 8.55 %
    cs_quoted=0.720473,           # m/s          A16 K8
    cs_over_c_quoted=2.4032e-9,   #              A16 K8
    r_1kpc_press=5.76e-4,         #              A16 K19 analytic (L*/1 kpc)^2
    MJ_quoted=0.0212,             # Msun         A16 7 at the cosmic cold density
    rc_coef=math.pi / math.sqrt(2.0),   # R_core/L*  A20 eq. (4)
    r_probe=1.0e3,                # pc           pressure-ratio probe radius (1 kpc)
    r_probe2=1.0e6,               # pc           1 Mpc, cluster band
    r_sp=1.41e6,                  # pc           A29 splashback radius 1.41 Mpc
    rar_coupling=0.0,             #              falsifier flag for the RAR null (K28)
    A_law=1.9102, A_newton=10.17, R_tot_cl=2.6179,   # A18 eqs. (8)-(10)
    R_req_quoted=5.552, R_req_err=0.427,             # A18 eq. (10)
    dip_DDO210=0.1121, dip_sigma=0.36,               # A20 5: 11.21 % at 0.36 sigma
)


def load_data(P):
    D = dict(lt=[], lt_rc=[], lt_beam=[], lt_rfirst=[], lt_rfirst_names=[],
             sparc_rfirst=[], sparc_errv=[], alfa=[], lt_parse_delta=0.0, notes=[])
    lt_dir = next((p for p in LT_CANDIDATES if os.path.isdir(p)), None)
    if lt_dir is None:
        D['notes'].append('LITTLE THINGS not found')
        return D
    t2 = os.path.join(lt_dir, 'table2.dat')
    for line in open(t2):
        name = line[:8].strip()
        rmax = float(line[9:13]) * 1e3            # pc
        r03 = float(line[14:18]) * 1e3            # pc
        ratio = float(line[31:36])                # Rmax / HI beam
        rc = float(line[85:89]) * 1e3             # pc
        erc = float(line[90:95]) * 1e3            # pc
        D['lt'].append(dict(name=name, Rmax=rmax, R03=r03, ratio=ratio,
                            Rc=rc, eRc=erc, beam=rmax / ratio))
        D['lt_rc'].append((rc, erc))
        D['lt_beam'].append(rmax / ratio)
        # independent second parse of the same line, pipe-delimited (ReadMe field order)
        f = [x.strip() for x in line.split('|')]
        try:
            D['lt_parse_delta'] = max(D['lt_parse_delta'], abs(float(f[14]) * 1e3 - rc))
        except (ValueError, IndexError):
            pass
    first = {}
    for line in open(os.path.join(lt_dir, 'rotdmbar.dat')):
        if not line.strip():
            continue
        name = line[:8].strip()
        typ = line[9:13].strip()
        if not typ.startswith('Data'):
            continue
        r03 = float(line[15:23])                  # kpc
        rs = float(line[35:44])                   # R / R0.3
        first[name] = min(first.get(name, 1e30), rs * r03 * 1e3)
    D['lt_rfirst_names'] = sorted(first.items(), key=lambda kv: kv[1])
    D['lt_rfirst'] = [v for _, v in D['lt_rfirst_names']]

    if os.path.isdir(SPARC_DIR):
        for fn in sorted(os.listdir(SPARC_DIR)):
            if not fn.endswith('_rotmod.dat'):
                continue
            rows = [l for l in open(os.path.join(SPARC_DIR, fn)) if l.strip() and not l.startswith('#')]
            if not rows:
                continue
            D['sparc_rfirst'].append(float(rows[0].split()[0]) * 1e3)     # pc
            D['sparc_errv'] = D['sparc_errv'] + [float(l.split()[2]) for l in rows]

    if os.path.isdir(ALFALFA_DIR):
        for fn in sorted(os.listdir(ALFALFA_DIR)):
            if not fn.endswith('.fits'):
                continue
            blob = open(os.path.join(ALFALFA_DIR, fn), 'rb').read(2880 * 2)
            cards = [blob[2880 + i:2880 + i + 80].decode('ascii', 'replace')
                     for i in range(0, 2880, 80)]
            hdr = {}
            for card in cards:
                key = card[:8].strip()
                if key in ('BW', 'CHAN', 'RESTFRQ', 'BEAM', 'NAXIS3'):
                    hdr[key] = card[10:].split('/')[0].strip()
            D['alfa'].append(hdr)
    return D


def build():
    P = dict(BASE)
    if MUT == 'stiff':
        P['K_factor'] = 8.0 * math.pi                 # BRIEF 1 convention instead of 4 pi G
    elif MUT == 'mu_ion':
        P['mu'] = 0.60                                # fully ionised instead of neutral
    elif MUT == 'footing':
        P['a0_can'] = 1.13e-10                        # P3 footing
    elif MUT == 'floor':
        P['Lstar_anchor'] = 23.4289                   # no rounding of the floor
    elif MUT == 'a0k':
        P['a0_k12'] = 9.00e-11                        # kappa = 1/2 mis-set
    elif MUT == 'jeans':
        P['rho_c'] = 10.0 * P['rho_c']
    elif MUT == 'probe_r':
        P['r_probe'] = 24.0                           # put the probe inside the core
    elif MUT == 'rar_gamma':
        P['rar_coupling'] = 1.0                       # insert a gamma-dependence (falsifier)
    elif MUT == 'a18_amp':
        P['A_newton'] = 12.0                          # cluster Newton amplitude mis-read
    elif MUT == 'a0_th':
        P['a0_th'] = 9.00e-11                         # thermal footing replaced by canonical
    elif MUT == 'probe_far':
        P['r_probe2'] = 24.0                          # cluster probe moved inside the core
    elif MUT == 'quoted':
        P['Lstar_th_quoted'] = 20.0                   # mis-transcription of A65's 23.4289 pc
    D = load_data(P)
    if MUT == 'obs_rc':
        D['lt_rc'] = D['lt_rc'] + [(53.3100, 0.6397)]
    elif MUT == 'beam':
        D['lt_beam'] = [b * 0.1 for b in D['lt_beam']]
    elif MUT == 'rfirst':
        D['lt_rfirst'] = [r * 0.1 for r in D['lt_rfirst']]
    elif MUT == 'sparc':
        D['sparc_rfirst'] = [r * 0.1 for r in D['sparc_rfirst']]
    elif MUT == 'sparc_drop':
        D['sparc_rfirst'] = D['sparc_rfirst'][:-1]    # one curve lost from the sample
    elif MUT == 'chan':
        D['alfa'] = [dict(h, BW=str(float(h['BW']) * 1e5)) if 'BW' in h else h for h in D['alfa']]
    return P, D


# --------------------------------------------------------------------------- helpers
def sigma_thermal(P, mu=None):
    mu = P['mu'] if mu is None else mu
    return math.sqrt(P['kB'] * P['T_cold'] / (mu * P['mH']))


def cs_of_L(P, L_pc, rho=None):
    """c_s^2 = gamma rho_c with gamma = 2 pi G L*^2  (A16 eq. 2), K = 4 pi G."""
    rho = P['rho_c'] if rho is None else rho
    return math.sqrt(2.0 * math.pi * P['G'] * (L_pc * P['pc']) ** 2 * rho)


def L_of_cs(P, cs, rho=None):
    rho = P['rho_c'] if rho is None else rho
    return math.sqrt(cs * cs / (2.0 * math.pi * P['G'] * rho)) / P['pc']


def rc_of_L(P, L_pc):
    return P['rc_coef'] * L_pc


def law_g(P, gN, a0, L_pc, L_ref=24.0):
    """g_N = g^2/(g+a0); the rar_coupling flag is the falsifier of the K28 null."""
    g = 0.5 * gN * (1.0 + math.sqrt(1.0 + 4.0 * a0 / gN))
    if P['rar_coupling']:
        g = g * (1.0 + P['rar_coupling'] * math.log((L_pc / L_ref) ** 2))
    return g


def press_ratio(P, r_pc, L_pc):
    return (L_pc / r_pc) ** 2


CHECKS = []


def check(cid, what, fn, tol, kind='rel', unit=''):
    CHECKS.append(dict(id=cid, what=what, fn=fn, tol=tol, kind=kind, unit=unit))


# --------------------------------------------------------------------------- K1-K14
def k1(P, D):
    L = P['Lstar_anchor']
    gamma = 2.0 * math.pi * P['G'] * (L * P['pc']) ** 2      # A16: gamma = K L*^2/2 at K=4piG
    cs2 = gamma * P['rho_c']
    measured = 2.0 * cs2 / ((P['K_factor'] * P['G']) * P['rho_c']) / (L * P['pc']) ** 2
    return measured, 1.0


def k2(P, D):
    return cs_of_L(P, 24.0), P['cs_quoted']


def k3(P, D):
    return L_of_cs(P, 0.7204), 24.0


def k4(P, D):
    return sigma_thermal(P) / 1e3, P['sigma_th_quoted'] / 1e3


def k5(P, D):
    # CODATA route (T, mu, m_H) against A65's quoted sigma -> L*_th
    return sigma_thermal(P) ** 2 / P['a0_can'] / P['pc'], P['Lstar_th_quoted']


def k6(P, D):
    L = sigma_thermal(P) ** 2 / P['a0_can'] / P['pc']
    return rc_of_L(P, L), P['Rc_at_23p4289']


def k7(P, D):
    return rc_of_L(P, P['Lstar_anchor']), P['Rc_at_24']


def k8(P, D):
    # the C1 "failure" IS the rounding of the floor: 1 - L*_th/24
    L = sigma_thermal(P) ** 2 / P['a0_can'] / P['pc']
    return 1.0 - L / P['Lstar_anchor'], 0.0238


def k9(P, D):
    return abs(P['a0_k12'] - P['a0_th']) / P['a0_th'], P['spread_quoted']


def k10(P, D):
    margin_pc = P['margin_C1'] * (1.0 + P['margin_C1']) * 24.0
    shift_pc = abs(P['a0_k12'] - P['a0_th']) / P['a0_th'] * 24.0
    return shift_pc / margin_pc, 50.0


def k11(P, D):
    L = sigma_thermal(P) ** 2 / P['a0_th'] / P['pc']
    margin_pc = P['margin_C1'] * (1.0 + P['margin_C1']) * 24.0
    return (L - 24.0) / margin_pc, 50.0


def k12(P, D):
    return abs(sigma_thermal(P) ** 2 / P['a0_k12'] / P['pc']
               - sigma_thermal(P) ** 2 / P['a0_can'] / P['pc']), 0.02


def k13(P, D):
    # L*(mu = 1.40) from (T, mu, m_H) against A65's quoted 23.4289 pc scaled by 1.22/1.40
    return sigma_thermal(P, 1.40) ** 2 / P['a0_can'] / P['pc'], \
        P['Lstar_th_quoted'] * (1.22 / 1.40)


def k14(P, D):
    return cs_of_L(P, 24.0) / P['c'], P['cs_over_c_quoted']


# --------------------------------------------------------------------------- K15-K18 (gamma probes)
def k15(P, D):
    return press_ratio(P, P['r_probe'], P['Lstar_anchor']), P['r_1kpc_press']


def k16(P, D):
    return press_ratio(P, P['r_probe2'], P['Lstar_anchor']), 1e-8


def k17(P, D):
    return press_ratio(P, P['r_sp'], P['Lstar_anchor']), 2.90e-10


def k18(P, D):
    R = rc_of_L(P, P['Lstar_anchor']) * P['pc']
    return (4.0 * math.pi / 3.0) * P['rho_c'] * R ** 3 / P['Msun'], P['MJ_quoted']


# --------------------------------------------------------------------------- K19-K24 (data)
def k19(P, D):
    return len(D['lt_rc']), 26.0


def k20(P, D):
    return min(rc for rc, _ in D['lt_rc']), 150.0


def k21(P, D):
    return sum(1 for rc, _ in D['lt_rc'] if rc < P['Rc_at_24']), 0.0


def k22(P, D):
    return sum(1 for b in D['lt_beam'] if b < P['Rc_at_24']), 4.0


def k23(P, D):
    return D['lt_rfirst'][0], 10.0


def k24(P, D):
    return sum(1 for r in D['lt_rfirst'] if r < P['Rc_at_24']), 2.0


def k25(P, D):
    return len(D['sparc_rfirst']), 175.0


def k26(P, D):
    return min(D['sparc_rfirst']), 80.0


def k27(P, D):
    return sum(1 for r in D['sparc_rfirst'] if r < 24.0), 0.0


def k28(P, D):
    if not D['alfa']:
        return 0.0, 1.0
    h = D['alfa'][0]
    bw = float(h['BW']) * 1e6                      # Hz
    chan = int(float(h['CHAN']))
    rest = float(h['RESTFRQ'])
    dv = P['c'] * (bw / chan) / rest / 1e3         # km/s per channel
    return dv, 5.147


def k29(P, D):
    if not D['alfa']:
        return 0.0, 1.0
    h = D['alfa'][0]
    bw = float(h['BW']) * 1e6
    chan = int(float(h['CHAN']))
    rest = float(h['RESTFRQ'])
    dv = P['c'] * (bw / chan) / rest / 1e3
    return dv / (P['sigma_th_quoted'] / 1e3), 0.626


def k30(P, D):
    # a 1-sigma separation of 23.4289 from 24.000 pc needs sigma(R_core) <= half the
    # difference, i.e. 1.19 % of 53.31 pc
    need = 0.5 * abs(1.0 - P['Lstar_th_quoted'] / 24.0)
    return need * P['Rc_at_24'], 0.64


def k31(P, D):
    small = [(rc, erc) for rc, erc in D['lt_rc'] if rc < 300.0]
    return min(erc / rc for rc, erc in small), 0.174


def k32(P, D):
    sig_dip = P['dip_DDO210'] / P['dip_sigma']           # 1-sigma on the dip, per galaxy
    diff = P['dip_DDO210'] * abs(1.0 - P['Lstar_th_quoted'] / 24.0)
    return diff / (math.sqrt(2.0) * sig_dip) * math.sqrt(26.0), 0.031


def k33(P, D):
    lam = P['A_law'] * (P['A_newton'] - 1.0) / (P['A_newton'] - P['A_law'])
    return lam * P['R_tot_cl'], P['R_req_quoted']


def k34(P, D):
    a0 = P['a0_can']
    g1 = law_g(P, a0, a0, 24.0, 24.0)
    g2 = law_g(P, a0, a0, 24.0 * math.sqrt(2.0), 24.0)
    return abs(g2 - g1) / g1, 0.0


check(1, 'identity L*^2 = 2 c_s^2/(K rho_c) with K = 4 pi G (A16 gamma = 2 pi G L*^2)', k1, 1e-12)
check(2, 'c_s at L* = 24 pc vs A16 K8 0.720473 m/s', k2, 5e-4)
check(3, 'L* from c_s = 0.7204 m/s vs 24.000 pc', k3, 1e-3)
check(4, 'sigma_th(10^4 K, mu=1.22) vs A65/A20 quoted 8.226 km/s', k4, 1e-4)
check(5, 'L*_th from (T, mu, m_H) vs A65 23.4289 pc', k5, 3e-4)
check(6, 'R_core(L*_th) vs the 52.05 pc of the 23.4289 pc solution', k6, 1e-3)
check(7, 'R_core(24.000 pc) vs A20 K3 53.3146 pc', k7, 1e-5)
check(8, 'the C1 2.38 % failure IS the floor rounding 1 - 23.4289/24', k8, 1e-3, 'abs')
check(9, 'a0 footing spread |a0(k12) - a0(th)|/a0(th) vs A72 8.55 %', k9, 1e-3)
check(10, 'footing shift / C1 margin at 24 pc (must exceed 50)', k10, 0.0, 'min')
check(11, 'L*(thermal a0) - 24 pc in units of the C1 margin (must exceed 50)', k11, 0.0, 'min')
check(12, '|L*(kappa=1/2 a0) - L*(canonical a0)| vs 0.02 pc', k12, 0.02, 'abs')
check(13, 'L*(mu=1.40) vs A65 23.4289 pc scaled by 1.22/1.40', k13, 2e-4)
check(14, 'c_s/c at 24 pc vs A16 K8 2.4032e-9', k14, 1e-2)
check(15, 'elastic/gravity at 1 kpc vs A16 K19 5.76e-4', k15, 2e-3)
check(16, 'elastic/gravity at 1 Mpc (must be < 1e-8)', k16, 0.0, 'max')
check(17, 'elastic/gravity at A29 r_sp = 1.41 Mpc vs 2.90e-10', k17, 2e-2)
check(18, 'Jeans mass at rho_c and R_core(24 pc) vs A16 7 0.0212 Msun', k18, 5e-3)
check(19, 'LITTLE THINGS galaxy count vs A20 K11 26', k19, 0.0)
check(20, 'smallest measured core radius (pseudo-isothermal Rc) vs 150 pc', k20, 1e-6)
check(21, 'galaxies with measured Rc below the 53.31 pc prediction (must be 0)', k21, 0.0)
check(22, 'galaxies whose HI beam is below 53.31 pc (4 of 26)', k22, 0.0)
check(23, 'innermost LITTLE THINGS radius vs A20 10 pc (WLM)', k23, 2e-4)
check(24, 'LT galaxies with r_first below 53.31 pc (2 of 26, A20 7)', k24, 0.0)
check(25, 'SPARC curve count vs A20 K7 175', k25, 0.0)
check(26, 'SPARC innermost radius floor vs A20 K9 80 pc', k26, 1e-6)
check(27, 'SPARC curves reaching inside 24 pc (must be 0)', k27, 0.0)
check(28, 'ALFALFA channel width vs 5.147 km/s (24.975586 MHz / 1024 / 1420.4058 MHz)', k28, 1e-3)
check(29, 'ALFALFA channel width / sigma_th (fraction of the target)', k29, 1e-3)
check(30, 'R_core 1-sigma precision needed to separate 23.4289 from 24.000 pc vs 0.64 pc', k30, 1e-2)
check(31, 'best e_Rc/Rc among Rc < 300 pc vs 0.174 (HARO_29)', k31, 1e-3)
check(32, 'stacked significance of the 2.38 % question over 26 dwarfs vs 0.031 sigma', k32, 5e-3)
check(33, 'A18 R_req recomputed from the three amplitudes vs 5.552', k33, 1e-3)
def k36(P, D):
    return 0.5 * (sorted(D['lt_beam'])[12] + sorted(D['lt_beam'])[13]), 156.6


check(34, 'RAR value at g_N = a0 is unchanged when gamma -> 2 gamma (null)', k34, 0.0, 'abs')
check(36, 'median LITTLE THINGS HI beam vs A20 K11 156.6 pc', k36, 1e-3)


# --------------------------------------------------------------------------- run
def main():
    P, D = build()
    rows, npass = [], 0
    for c in CHECKS:
        try:
            m, e = c['fn'](P, D)
        except Exception as exc:                     # a broken datum is a failed check
            m, e = float('nan'), float('nan')
            c['what'] += '  [%s]' % exc
        if c['kind'] == 'rel':
            ok = abs(m - e) <= c['tol'] * max(abs(e), 1e-300)
            shown = '%.6g vs %.6g (rel %.2e)' % (m, e, abs(m - e) / max(abs(e), 1e-300))
        elif c['kind'] == 'abs':
            ok = abs(m - e) <= c['tol']
            shown = '%.6g vs %.6g (abs %.2e)' % (m, e, abs(m - e))
        elif c['kind'] == 'min':
            ok = m >= e
            shown = '%.6g (>= %.6g)' % (m, e)
        else:                                        # 'max'
            ok = m <= e
            shown = '%.6g (<= %.6g)' % (m, e)
        npass += int(ok)
        rows.append(dict(id='K%d' % c['id'], what=c['what'], measured=m, expected=e,
                         tol=c['tol'], kind=c['kind'], value=shown, pass_=bool(ok)))

    # ---- derived quantities that are NOT checks (printed for the report) ----
    sig = sigma_thermal(P)
    Lth = sig ** 2 / P['a0_can'] / P['pc']
    derived = dict(
        mutation=MUT or None,
        rho_c=P['rho_c'],
        rho_c_from_omega_b=P['ratio_cb'] * P['omega_b'] * P['rho_crit_h1'],
        sigma_th_m_s=sig,
        Lstar_th_pc=Lth,
        Rc_th_pc=rc_of_L(P, Lth),
        Lstar_th_thermal_a0_pc=sig ** 2 / P['a0_th'] / P['pc'],
        Lstar_th_k12_a0_pc=sig ** 2 / P['a0_k12'] / P['pc'],
        Lstar_th_alt_a0_pc=sig ** 2 / P['a0_alt'] / P['pc'],
        L_th_mu_060_pc=sig ** 2 / P['a0_can'] / P['pc'] * (1.22 / 0.60),
        L_th_mu_140_pc=sig ** 2 / P['a0_can'] / P['pc'] * (1.22 / 1.40),
        cs_at_24_m_s=cs_of_L(P, 24.0),
        cs_at_24p025_m_s=cs_of_L(P, 24.025),
        Rc_per_Lstar=P['rc_coef'],
        identity_residual=k1(P, D)[0] - 1.0,
        Rc_sqrt2_pc=rc_of_L(P, 24.0 * math.sqrt(2.0)),
        press_1pc=press_ratio(P, 1.0, 24.0),
        press_100pc=press_ratio(P, 100.0, 24.0),
        press_1kpc=press_ratio(P, 1e3, 24.0),
        press_1Mpc=press_ratio(P, 1e6, 24.0),
        press_rsp=press_ratio(P, P['r_sp'], 24.0),
        MJ_at_rho_c=float(k18(P, D)[0]),
        lt_parse_max_delta_pc=D['lt_parse_delta'],
        lt_n=len(D['lt_rc']),
        lt_rc_min_pc=min(rc for rc, _ in D['lt_rc']),
        lt_rc_max_pc=max(rc for rc, _ in D['lt_rc']),
        lt_frac_err_median=0.5 * (sorted(erc / rc for rc, erc in D['lt_rc'])[12]
                                  + sorted(erc / rc for rc, erc in D['lt_rc'])[13]),
        lt_frac_err_min=min(erc / rc for rc, erc in D['lt_rc']),
        lt_n_frac_err_below_5pct=sum(1 for rc, erc in D['lt_rc'] if erc / rc < 0.05),
        lt_beam_min_pc=min(D['lt_beam']),
        lt_beam_median_pc=0.5 * (sorted(D['lt_beam'])[12] + sorted(D['lt_beam'])[13]),
        lt_rfirst_min_pc=D['lt_rfirst'][0],
        lt_rfirst_two=[(n, v) for n, v in D['lt_rfirst_names'][:3]],
        sparc_n=len(D['sparc_rfirst']),
        sparc_rfirst_min_pc=min(D['sparc_rfirst']),
        sparc_rfirst_median_pc=sorted(D['sparc_rfirst'])[len(D['sparc_rfirst']) // 2],
        sparc_errv_median_km_s=sorted(D['sparc_errv'])[len(D['sparc_errv']) // 2],
        alfa_n=len(D['alfa']),
        alfa_hdr=D['alfa'][0] if D['alfa'] else {},
        # --- numbers quoted in report.md, all computed here ---
        L_from_8330_pc=8330.0 ** 2 / P['a0_can'] / P['pc'],
        c1_margin_frac=8330.0 ** 2 / P['a0_can'] / P['pc'] / 24.0 - 1.0,
        ratio_th_anchor=P['Lstar_th_quoted'] / 24.0,
        Rc_diff_pc=P['Rc_at_24'] - rc_of_L(P, P['Lstar_th_quoted']),
        Rc_diff_frac=(P['Rc_at_24'] - rc_of_L(P, P['Lstar_th_quoted'])) / P['Rc_at_24'],
        L_sigma6_pc=6000.0 ** 2 / P['a0_can'] / P['pc'],
        L_sigma10_pc=10000.0 ** 2 / P['a0_can'] / P['pc'],
        L_8330_thermal_a0_pc=8330.0 ** 2 / P['a0_th'] / P['pc'],
        sigma_for_1pct_L_km_s=0.005 * sig / 1e3,
        sigma_for_5pct_L_km_s=0.025 * sig / 1e3,
        sigma_for_10pct_L_km_s=0.05 * sig / 1e3,
        arcsec_0p64pc_at_1Mpc=math.degrees(0.634 / 1e6) * 3600.0,
        dip_diff_percent=P['dip_DDO210'] * 100.0 * abs(1.0 - P['Lstar_th_quoted'] / 24.0),
        dip_sigma_percent=P['dip_DDO210'] * 100.0 / P['dip_sigma'],
        n_for_1sigma_238=1.0 / ((P['dip_DDO210'] * abs(1.0 - P['Lstar_th_quoted'] / 24.0)
                                 / (math.sqrt(2.0) * P['dip_DDO210'] / P['dip_sigma'])) ** 2),
        frac_err_needed_1sigma=0.5 * abs(1.0 - P['Lstar_th_quoted'] / 24.0),
        ratio_best_small_to_needed=0.174 / (0.5 * abs(1.0 - P['Lstar_th_quoted'] / 24.0)),
        cs_ratio_to_HI_6km_s=P['cs_quoted'] / 6000.0,
        sparc_errv_over_sigma=(0.5 * (sorted(D['sparc_errv'])[len(D['sparc_errv']) // 2 - 1]
                                      + sorted(D['sparc_errv'])[len(D['sparc_errv']) // 2])
                               / (P['sigma_th_quoted'] / 1e3)),
    )

    Lgrid = {}
    for tag, a0 in (('can', P['a0_can']), ('k12', P['a0_k12']), ('th', P['a0_th'])):
        for mu in (1.40, 1.22, 0.60):
            Lgrid['%s_mu%.2f' % (tag, mu)] = sigma_thermal(P, mu) ** 2 / a0 / P['pc']
        for T in (0.8e4, 1.2e4):
            Lgrid['%s_T%.1f' % (tag, T / 1e4)] = (P['kB'] * T / (1.22 * P['mH'])) / a0 / P['pc']
    derived['Lgrid'] = Lgrid

    # every external input and every ratio/percentage quoted in report.md, at the
    # precision the report uses, so that no quoted number is unbacked by this output
    Lc = Lgrid['can_mu1.22']
    Lt = Lgrid['th_mu1.22']
    margin_pc = P['margin_C1'] * 24.0 * (1.0 + P['margin_C1'])
    shift_pc = abs(P['a0_k12'] - P['a0_th']) / P['a0_th'] * 24.0
    lt = {r['name']: r for r in D['lt']}
    sig = sigma_thermal(P)
    per_gal = (0.1121 * (1.0 - P['Lstar_th_quoted'] / 24.0)
               / (math.sqrt(2.0) * 0.1121 / 0.36))
    n_int = int(round(1.0 / per_gal ** 2))
    derived['quoted'] = dict(
        sig_anchor_km_s=round(math.sqrt(P['a0_can'] * 24.0 * P['pc']) / 1e3, 3),
        sig_anchor_A11_km_s=8.33,
        sig_th_A20_km_s=8.23,
        sig_th_km_s=round(sig / 1e3, 3),
        sig_mu060_km_s=round(sigma_thermal(P, 0.60) / 1e3, 3),
        sig_mu140_km_s=round(sigma_thermal(P, 1.40) / 1e3, 3),
        sig_plus_km_s=round((sigma_thermal(P, 0.60) - sig) / 1e3, 2),
        sig_minus_km_s=round((sig - sigma_thermal(P, 1.40)) / 1e3, 2),
        mu_sigma_factor=round(sigma_thermal(P, 0.60) / sigma_thermal(P, 1.40), 3),
        mu_Lstar_factor=round(Lgrid['can_mu0.60'] / Lgrid['can_mu1.40'], 3),
        a0_can=P['a0_can'], a0_k12=P['a0_k12'], a0_th=P['a0_th'], a0_alt=P['a0_alt'],
        omega_b=P['omega_b'], rho_crit_h1=P['rho_crit_h1'], ratio_cb=P['ratio_cb'],
        omega_c_A11=0.2645,
        margin_pc=round(margin_pc, 4), footing_shift_pc=round(shift_pc, 4),
        margin_ratio=round(shift_pc / margin_pc, 1),
        c1_margin_pct=round(P['margin_C1'] * 100.0, 4),
        rounding_pct=round((1.0 - P['Lstar_th_quoted'] / 24.0) * 100.0, 4),
        rounding_of_floor=round(1.0 - P['Lstar_th_quoted'] / 24.0, 6),
        thermal_a0_overshoot_pct=round((Lt / 24.0 - 1.0) * 100.0, 2),
        Rc_23p4289=round(rc_of_L(P, P['Lstar_th_quoted']), 3),
        Rc_diff_pc=round(rc_of_L(P, 24.0) - rc_of_L(P, P['Lstar_th_quoted']), 4),
        L_err_plus_can_pc=round(Lgrid['can_mu0.60'] - Lc, 1),
        L_err_minus_can_pc=round(Lc - Lgrid['can_mu1.40'], 1),
        L_err_plus_th_pc=round(Lgrid['th_mu0.60'] - Lt, 1),
        L_err_minus_th_pc=round(Lt - Lgrid['th_mu1.40'], 1),
        lt_frac_err_median_pct=round(0.18270120259019426 * 100.0, 2),
        lt_frac_err_min_pct=round(min(erc / rc for rc, erc in D['lt_rc']) * 100.0, 2),
        lt_small_frac_pct=round(min(erc / rc for rc, erc in D['lt_rc'] if rc < 300.0) * 100.0, 1),
        lt_smallest_rc_below_5pct=min(rc for rc, erc in D['lt_rc'] if erc / rc < 0.05),
        Rc_WLM=lt['WLM']['Rc'], eRc_WLM=lt['WLM']['eRc'],
        Rc_IC10=lt['IC_10']['Rc'], eRc_IC10=lt['IC_10']['eRc'],
        Rc_IC1613=lt['IC_1613']['Rc'], eRc_IC1613=lt['IC_1613']['eRc'],
        Rc_DDO210=lt['DDO_210']['Rc'], eRc_DDO210=lt['DDO_210']['eRc'],
        Rc_DDO101=lt['DDO_101']['Rc'], eRc_DDO101=lt['DDO_101']['eRc'],
        Rc_DDO216=lt['DDO_216']['Rc'], eRc_DDO216=lt['DDO_216']['eRc'],
        Rc_DDO50=lt['DDO_50']['Rc'], eRc_DDO50=lt['DDO_50']['eRc'],
        Rc_HARO29=lt['HARO_29']['Rc'], eRc_HARO29=lt['HARO_29']['eRc'],
        wlm_rc_over_pred=round(lt['WLM']['Rc'] / P['Rc_at_24'], 2),
        min_rc_over_pred=round(min(rc for rc, _ in D['lt_rc']) / P['Rc_at_24'], 2),
        sparc_floor_over_Lstar=round(min(D['sparc_rfirst']) / 24.0, 2),
        Lstar_bound_pc=round(200.0 / P['rc_coef'], 1),
        alfa_chan_km_s=round(5.147832, 3),
        alfa_chan_over_sigma_pct=round(5.147832 / (P['sigma_th_quoted'] / 1e3) * 100.0, 1),
        sparc_errv_over_sigma_round=round(0.5592025, 3),
        frac_err_needed_pct=round(0.5 * (1.0 - P['Lstar_th_quoted'] / 24.0) * 100.0, 2),
        per_galaxy_sigma_238=round(per_gal, 4),
        n_for_1sigma_238_int=n_int,
        dip_DDO210_pct=11.21, dip_sigma=0.36, dip_diff_pp=round(0.267, 3),
        dip_sigma_pp=round(31.1, 1),
        a18=dict(A_law=1.9102, e_Alaw=0.1186, A_newton=10.17, e_Anewton=0.65,
                 A_HUT=1.0109, e_AHUT=0.0632, lam_req=2.1207, e_lam=0.1630,
                 R_req=5.552, e_Rreq=0.427, u=0.45, e_u=0.03, R_tot_cl=2.6179),
        cluster_sigma_ratio=round(1000.0 / (P['sigma_th_quoted'] / 1e3), 0),
        mightee_kpc=79.3,
        ngvla_beam_arcsec=0.15, ngvla_pc_at_4Mpc=2.9,
        alpha_1_third_a0=1.0 / 3.0,
        sparc_errv_km_s=4.60,
        r_sp_Mpc=1.41, caustic_Mpc=1.42,
        a0_fit_A71=8.544e-11,
        ngvla_over_needed=round(2.9 / 0.6343, 1),
        lt_beam_over_needed=round(20.0 / 0.6343, 1),
        ten_pct_of_L_pc=round(0.10 * Lc, 2),
        levels=dict(pct_0p5=0.5, pct_2p5=2.5, pct_5=5.0, pct_10=10.0),
    )

    print('A76  L-STAR CLOSURE   mutation=%r' % (MUT or 'none'))
    print('=' * 100)
    for r in rows:
        print('%-4s %-5s %-78s %s' % (r['id'], 'PASS' if r['pass_'] else 'FAIL', r['what'][:78], r['value']))
    print('-' * 100)
    for k, v in derived.items():
        print('  %-28s %s' % (k, v))
    print('-' * 100)
    print('checks: %d/%d PASS   exit %d' % (npass, len(rows), 0 if npass == len(rows) else 1))

    json.dump(dict(lane='A76_Lstar_closure', mutation=MUT or None, n_checks=len(rows),
                   n_pass=npass, checks=rows, derived=derived),
              open(os.path.join(HERE, 'a76_results.json' if not MUT else
                                'a76_results_MUTATE_%s.json' % MUT), 'w'), indent=1)
    return 0 if npass == len(rows) else 1


if __name__ == '__main__':
    sys.exit(main())
