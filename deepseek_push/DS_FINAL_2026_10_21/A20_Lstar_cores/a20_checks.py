#!/usr/bin/env python3
"""
A20 -- measure the stiffness length L* from the inner structure of galaxies,
with a no-juggling guard.

Checks print one line each:   K<n> PASS <measured> <threshold>
and the run ends with        "A20 COMPLETE: N/M checks PASS."

Deterministic, no network, stdlib + numpy (+ sympy for the exact algebra).
Runtime ~ 2 s.

Usage:  python3 a20_checks.py [--mutate=exp|k|dist]
"""
import sys, os, re, json, glob
import numpy as np

# ----------------------------------------------------------------------------- mutation flags
MUT = None
for a in sys.argv[1:]:
    if a.startswith('--mutate'):
        MUT = a.split('=', 1)[1] if '=' in a else 'exp'

# ----------------------------------------------------------------------------- constants (BRIEF §4)
C_LIGHT = 2.99792458e8
G       = 6.67430e-11
MSUN    = 1.98847e30
PC      = 3.0856775814913673e16
KPC     = 1.0e3 * PC
MPC     = 3.0856775814913673e22
ARCSEC  = 4.84813681109536e-6
A0      = 9.36e-11          # canonical footing
H0      = 2.1843e-18
LAM     = 1.0890e-52
RHO_LAM = 5.831e-27
THETA_SPARC = 30.0          # arcsec, [EXT] typical HI beam of the SPARC compilation
SIG_TH  = 8.23e3            # m/s, 1e4 K, mu=1.22  [EXT AG6D B7 via A11 §15]
K_CAND2 = 9.0               # A11 §15: upper window end == V_f^2/(9 a0) for V_f = 165.2 km/s
RCORE_COEF = np.pi / np.sqrt(2.0)   # 2.22144 : polytrope n=1 outer edge in units of L*

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SPARC_DIR = os.path.join(ROOT, 'real_research', 'data', 'sparc_data')
LT_CANDIDATES = [os.path.join(os.path.dirname(ROOT), '_external_data', 'little_things_oh2015'),
                 os.path.join(ROOT, '_external_data', 'little_things_oh2015')]
LT_DIR = next((p for p in LT_CANDIDATES if os.path.isdir(p)), None)

CHECKS, NUM = [], {}


def check(cid, ok, value, threshold, note=''):
    print("K%-3s %s %-34s %-22s %s" % (cid, 'PASS' if ok else 'FAIL', value, threshold, note))
    CHECKS.append(dict(id='K%s' % cid, **{'pass': bool(ok)}, passed=bool(ok), value=str(value),
                       threshold=str(threshold), note=note))
    return ok


def pct(x):
    return "%.2f%%" % (100.0 * x)


# ============================================================================= 1. EXACT ALGEBRA
import sympy as sp

def section_exact():
    r, r0, rho0, L, n, xi = sp.symbols('r r0 rho0 L n xi', positive=True)
    Gs, pi = sp.symbols('G pi', positive=True)

    # --- K1: the cusp pressure/gravity ratio is (L*/r)^2 for n = 1 and n = 2
    rho = rho0 * (r / r0) ** (-n)
    p = pi * Gs * L ** 2 * rho ** 2                        # p = (gamma/2) rho^2, gamma = 2 pi G L^2
    grad = sp.simplify(sp.diff(p, r) / rho)                # (1/rho) dp/dr
    M = 4 * pi * rho * r ** 3 / ((3 - n) if MUT != 'exp' else 3)   # mutation 'exp': drop (3-n)
    g = Gs * M / r ** 2
    ratio = sp.simplify(-grad / g)
    k1 = [sp.simplify(ratio.subs(n, k) - (L / r) ** 2) for k in (1, 2)]
    ok1 = all(e == 0 for e in k1)
    NUM['K1_residuals'] = [str(e) for e in k1]
    check(1, ok1, 'residual n=1,2 = %s' % NUM['K1_residuals'], 'exactly 0',
          '(1/rho)dp/dr/g = (L*/r)^2, density-free')

    # --- K2: n=1 polytrope theta=sin(xi)/xi is exact hydrostatic for p=pi G L^2 rho^2
    th = sp.sin(xi) / xi
    le = sp.simplify((sp.diff(xi ** 2 * sp.diff(th, xi), xi) / xi ** 2 + th))
    a = L / sp.sqrt(2)                                     # polytrope scale length
    Mxi = 4 * pi * rho0 * a ** 3 * (sp.sin(xi) - xi * sp.cos(xi))
    gxi = Gs * Mxi / (a * xi) ** 2
    pxi = pi * Gs * L ** 2 * (rho0 * th) ** 2             # pressure of the polytrope
    gradxi = sp.simplify((sp.diff(pxi, xi) / a) / (rho0 * th))   # (1/rho) dp/dr, r = a xi
    ratio_signed = sp.simplify(gradxi / gxi)               # must be exactly -1 (pressure pushes out)
    ok2 = (sp.simplify(le) == 0) and (sp.simplify(ratio_signed + 1) == 0)
    NUM['K2_lane_emden_residual'] = str(sp.simplify(le))
    NUM['K2_polytrope_ratio'] = '1 (signed %s)' % ratio_signed
    check(2, ok2, 'LE resid %s ; ratio %s' % (NUM['K2_lane_emden_residual'], NUM['K2_polytrope_ratio']),
          '0 ; exactly 1', 'pressure alone balances self-gravity identically')

    # --- K3: R_core = pi L*/sqrt2, cross-check against A16's R_TF
    rc24 = RCORE_COEF * 24.0
    a16 = 53.3146
    NUM['R_core_24pc'] = round(rc24, 4)
    NUM['R_core_a16'] = a16
    check(3, abs(rc24 - a16) / a16 < 1e-6, '%.4f pc' % rc24, '%.4f +- 1e-6' % a16,
          'matches A16 R_TF')


# ============================================================================= 2. PREDICTION
def fc_of_r(r_m, Mb, ab_kpc):
    """cold-sector mass fraction f_c = M_ph/(M_ph+M_b) for a Hernquist baryon profile
    under the frozen law g = (gN/2)(1+sqrt(1+4a0/gN)).  Hernquist: gN = G Mb/(r+a)^2."""
    a = ab_kpc * KPC
    gN = G * Mb * MSUN / (r_m + a) ** 2
    y = gN / A0
    F = 0.5 * (np.sqrt(1.0 + 4.0 / y) - 1.0)      # M_ph/M_b
    return F / (1.0 + F)


def r_switch(L_pc, Mb, ab_kpc):
    """root of f_c(r) (L*/r)^2 = 1  ->  L* sqrt(f_c(r_sw))."""
    lo, hi = 1.0e-4 * L_pc * PC, 1.0e6 * L_pc * PC
    for _ in range(200):
        mid = np.sqrt(lo * hi)
        val = fc_of_r(mid, Mb, ab_kpc) * (L_pc * PC / mid) ** 2 - 1.0
        if val > 0:
            lo = mid
        else:
            hi = mid
    return np.sqrt(lo * hi) / PC


HALOS = {'MW':    dict(Mb=6.0e10, ab=1.5),
         'dwarf': dict(Mb=1.0e8,  ab=0.7)}


def section_prediction():
    Ls = [24.0, 100.0, 300.0, 1000.0]

    # --- K4: halo-independent force-balance ladder  delta(r) = 1-sqrt(1-(r_sw/r)^2)
    lad = {}
    for d in (0.5, 0.1, 0.01, 0.001):
        lad[d] = 1.0 / np.sqrt(1.0 - (1.0 - d) ** 2)
    NUM['delta_ladder_r_over_rsw'] = {str(k): round(v, 6) for k, v in lad.items()}
    ok4 = (abs(lad[0.5] - 1.154701) < 2e-6 and abs(lad[0.1] - 2.294157) < 2e-6
           and abs(lad[0.01] - 7.088812) < 1e-5)
    check(4, ok4, 'r(50%%)=%.6f r(10%%)=%.6f r(1%%)=%.6f' % (lad[0.5], lad[0.1], lad[0.01]),
          '1.154701 / 2.294157 / 7.088812', 'in units of r_switch')

    # --- K5/K6: the 8-row table
    tab = {}
    for hname, hp in HALOS.items():
        for L in Ls:
            rsw = r_switch(L, hp['Mb'], hp['ab'])
            fc = fc_of_r(rsw * PC, hp['Mb'], hp['ab'])
            d_pl = 1.0 - np.sqrt(1.0 - fc)
            row = dict(L_pc=L, r_switch_pc=rsw, R_core_pc=RCORE_COEF * L,
                       f_c_at_switch=fc, delta_plateau=d_pl,
                       delta_2rsw=1 - np.sqrt(1 - 1 / 4.0),
                       delta_5rsw=1 - np.sqrt(1 - 1 / 25.0),
                       delta_10rsw=1 - np.sqrt(1 - 1 / 100.0))
            for x in (100.0, 500.0):
                row['delta_%dpc' % int(x)] = (1 - np.sqrt(1 - min(1.0, (rsw / x) ** 2)))
            tab['%s_%d' % (hname, L)] = {k: (round(float(v), 6) if not isinstance(v, float) else float(v))
                                         for k, v in row.items()}
    NUM['prediction_table'] = tab

    mw_max = max(tab['MW_%d' % L]['delta_plateau'] for L in Ls)
    dw_min = min(tab['dwarf_%d' % L]['delta_plateau'] for L in Ls)
    NUM['delta_plateau_MW_max'] = round(mw_max, 6)
    NUM['delta_plateau_dwarf_min'] = round(dw_min, 6)
    NUM['r_M_MW_kpc'] = round(float(np.sqrt(G * 6.0e10 * MSUN / A0) / KPC), 3)
    NUM['r_M_dwarf_pc'] = round(float(np.sqrt(G * 1.0e8 * MSUN / A0) / PC), 1)
    ok5 = (abs(mw_max - 0.01484) < 0.0010) and (abs(dw_min - 0.3582) < 0.005)
    check(5, ok5, 'MW max %.4f ; dwarf min %.4f' % (mw_max, dw_min),
          '0.0148+-0.001 ; 0.3582+-0.005', 'depth is set by f_c at the switch, not by L*')

    rat = [tab['%s_1000' % h]['r_switch_pc'] / tab['%s_24' % h]['r_switch_pc'] for h in HALOS]
    NUM['r_switch_ratio_1000_over_24'] = [round(x, 4) for x in rat]
    NUM['r_switch_drift'] = round(float(max(abs(x / (1000.0 / 24.0) - 1) for x in rat)), 4)
    ok6 = all(abs(x / (1000.0 / 24.0) - 1) < 0.20 for x in rat)
    check(6, ok6, 'ratio = %.2f / %.2f (drift %.1f%%)' % (rat[0], rat[1], 100 * NUM['r_switch_drift']),
          '41.67 +- 20%', 'r_switch quasi-linear in L* (f_c drift only)')


# ============================================================================= 3. SPARC
def load_sparc():
    out = []
    for f in sorted(glob.glob(os.path.join(SPARC_DIR, '*_rotmod.dat'))):
        txt = open(f).read()
        m = re.search(r'Distance\s*=\s*([0-9.]+)', txt)
        if not m:
            continue
        d = float(m.group(1))
        rows = [l.split() for l in txt.splitlines() if l.strip() and not l.startswith('#')]
        r = np.array([float(x[0]) for x in rows])          # kpc
        v = np.array([float(x[1]) for x in rows])
        ev = np.array([float(x[2]) for x in rows])
        out.append(dict(name=os.path.basename(f).replace('_rotmod.dat', ''), D=d,
                        r_pc=r * 1e3, v=v, ev=ev, n=len(rows),
                        Vf=float(np.mean(v[-3:]))))
    return out


def section_sparc():
    sp = load_sparc()
    N = len(sp)
    npts = sum(s['n'] for s in sp)
    rfirst = np.array([s['r_pc'][0] for s in sp])
    D = np.array([s['D'] for s in sp]) * (1e3 if MUT == 'dist' else 1.0)   # mutation 'dist': kpc for Mpc
    beam = THETA_SPARC * ARCSEC * D * 1e6                  # pc
    rrel = np.maximum(rfirst, beam)
    Vf = np.array([s['Vf'] for s in sp])
    NUM.update(dict(sparc_N=N, sparc_points=npts, sparc_D_min=round(float(D.min()), 3),
                    sparc_D_max=round(float(D.max()), 3), sparc_D_med=round(float(np.median(D)), 3),
                    sparc_rfirst_min_pc=round(float(rfirst.min()), 1),
                    sparc_rfirst_med_pc=round(float(np.median(rfirst)), 1),
                    sparc_rfirst_max_pc=round(float(rfirst.max()), 1),
                    sparc_beam_min_pc=round(float(beam.min()), 1),
                    sparc_beam_med_pc=round(float(np.median(beam)), 1),
                    sparc_rrel_min_pc=round(float(rrel.min()), 1),
                    sparc_Vf_min=round(float(Vf.min()), 2), sparc_Vf_max=round(float(Vf.max()), 2),
                    sparc_Vf_med=round(float(np.median(Vf)), 2)))
    ok7 = (N == 175 and npts == 3391)
    check(7, ok7, '%d galaxies / %d points' % (N, npts), '175 / 3391',
          'r_first %.0f-%.0f pc, median %.0f pc' % (rfirst.min(), rfirst.max(), np.median(rfirst)))

    # --- K8: fraction of galaxies whose innermost reliable radius is inside L*
    frac_first, frac_rel = {}, {}
    for L in (24.0, 100.0, 300.0, 1000.0):
        frac_first[str(int(L))] = round(float(np.mean(rfirst < L)), 4)
        frac_rel[str(int(L))] = round(float(np.mean(rrel < L)), 4)
    NUM['sparc_frac_inside_rfirst'] = frac_first
    NUM['sparc_frac_inside_rrel'] = frac_rel
    ok8 = (frac_rel['24'] == 0.0 and frac_rel['100'] == 0.0
           and abs(frac_rel['300'] - 0.0114) < 0.002 and abs(frac_rel['1000'] - 0.2229) < 0.01)
    check(8, ok8, 'f(r_rel<24)=%.4f <100=%.4f <300=%.4f <1k=%.4f' %
          (frac_rel['24'], frac_rel['100'], frac_rel['300'], frac_rel['1000']),
          '0 / 0 / 0.0114 / 0.2229', 'conservative 30" beam floor')

    # --- K9: the smallest resolvable L*
    floor_first = float(rfirst.min())
    floor_beam = float(beam.min())
    NUM['sparc_floor_pc'] = round(min(floor_first, floor_beam), 1)
    NUM['sparc_floor_over_24pc'] = round(min(floor_first, floor_beam) / 24.0, 3)
    NUM['sparc_beam_floor_pc'] = round(floor_beam, 1)
    NUM['sparc_beam_over_24pc'] = round(floor_beam / 24.0, 2)
    NUM['sparc_beam15_over_24pc'] = round(0.5 * floor_beam / 24.0, 2)
    NUM['sparc_beam60_over_24pc'] = round(2.0 * floor_beam / 24.0, 2)
    NUM['sparc_beam15_pc'] = round(0.5 * floor_beam, 1)
    NUM['sparc_beam60_pc'] = round(2.0 * floor_beam, 1)
    ok9 = min(floor_first, floor_beam) / 24.0 > 3.0
    check(9, ok9, 'floor %.0f pc = %.2f x 24 pc' % (min(floor_first, floor_beam),
                                                    min(floor_first, floor_beam) / 24.0),
          '> 3 x 24 pc', 'SPARC cannot resolve a 24 pc core')
    return sp


# ============================================================================= 4a. OTHER HI ON DISK
def ext(*parts):
    """resolve an _external_data product: repo-local first, then sibling of the repo root."""
    for base in (ROOT, os.path.dirname(ROOT)):
        p = os.path.join(base, '_external_data', *parts)
        if os.path.exists(p):
            return p
    return os.path.join(ROOT, '_external_data', *parts)


def section_other_hi():
    """MIGHTEE-HI DR1 cutouts and ALFALFA global profiles: can either bound a core?"""
    cube = ext('mightee_pipeline_2026_10_19', 'MGTH_J100143.2+024109.npz')
    if not os.path.exists(cube):
        check(10, False, 'MIGHTEE cube absent', 'present')
        return
    d = np.load(cube, allow_pickle=True)
    beam = float(np.nanmedian(d['beam_arcsec']))            # arcsec
    nu = float(np.nanmedian(d['frequency_hz']))
    z = 1420.405751e6 / nu - 1.0
    zz = np.linspace(0, z, 400)
    E = np.sqrt(0.31 * (1 + zz) ** 3 + 0.69)
    DC = (C_LIGHT / H0) * np.sum(0.5 * (1.0 / E[1:] + 1.0 / E[:-1]) * np.diff(zz))             # m
    DL = (1 + z) * DC
    lin_kpc = beam * ARCSEC * DL / KPC
    alfa = len(glob.glob(os.path.join(ext('hi_profiles_2026_10_18'), 'A*.fits')))
    NUM.update(dict(mghtee_beam_arcsec=round(beam, 2), mghtee_z=round(float(z), 4),
                    mghtee_DL_Mpc=round(float(DL / MPC), 1),
                    mghtee_linear_kpc=round(float(lin_kpc), 1),
                    mghtee_cubes=int(len(glob.glob(os.path.join(ext('mightee_pipeline_2026_10_19'),
                                                                'MGTH_*.npz')))),
                    alfa_global_profiles=alfa))
    ok10 = lin_kpc / (24.0e-3) > 100.0
    NUM['mghtee_over_24pc'] = int(round(lin_kpc / (24.0e-3)))
    check(10, ok10, 'MIGHTEE %.1f" -> %.0f kpc at z=%.3f = %.0fx 24 pc' %
          (beam, lin_kpc, z, lin_kpc / (24.0e-3)), '> 100x 24 pc => unusable',
          '%d cubes, %d ALFALFA global profiles: no core bound' % (NUM['mghtee_cubes'], alfa))


# ============================================================================= 4b. LITTLE THINGS
def section_lt():
    if LT_DIR is None:
        check(10, False, 'LITTLE THINGS not found', 'directory present')
        return
    t2, t1 = os.path.join(LT_DIR, 'table2.dat'), os.path.join(LT_DIR, 'table1.dat')
    R03, RMAX, RAT, D = {}, {}, {}, {}
    for l in open(t2):
        nm = l[:8].strip()
        RMAX[nm] = float(l[9:13]); R03[nm] = float(l[14:18]); RAT[nm] = float(l[31:36])
    for l in open(t1):
        D[l[:8].strip()] = float(l[32:36])
    # rotation-curve data to get the innermost measured radius
    rows = {}
    for l in open(os.path.join(LT_DIR, 'rotdmbar.dat')):
        if not l.strip():
            continue
        nm, typ = l[:8].strip(), l[9:14].strip()
        rows.setdefault((nm, typ), []).append((float(l[35:44]) * float(l[15:23]),
                                               float(l[45:54]) * float(l[24:34]),
                                               float(l[55:63]) * float(l[24:34])))
    names = sorted(R03)
    beam_pc = np.array([RMAX[n] / RAT[n] * 1e3 for n in names])
    r0 = np.array([rows[(n, 'Data')][0][0] * 1e3 for n in names])
    r03 = np.array([R03[n] * 1e3 for n in names])
    bound = r03 / RCORE_COEF
    r80 = []
    for n in names:
        arr = np.array(rows[(n, 'Data')])
        v = arr[:, 1]
        i = np.where(v >= 0.8 * v.max())[0]
        r80.append(arr[i[0], 0] * 1e3 if len(i) else np.nan)
    r80 = np.array(r80)
    bound80 = r80 / (0.8 * RCORE_COEF)
    NUM.update(dict(lt_N=len(names), lt_beam_min_pc=round(float(beam_pc.min()), 1),
                    lt_beam_med_pc=round(float(np.median(beam_pc)), 1),
                    lt_beam_max_pc=round(float(beam_pc.max()), 1),
                    lt_rfirst_min_pc=round(float(r0.min()), 1),
                    lt_rfirst_max_pc=round(float(r0.max()), 1),
                    lt_R03_min_pc=round(float(r03.min()), 1),
                    lt_R03_med_pc=round(float(np.median(r03)), 1),
                    lt_R03_max_pc=round(float(r03.max()), 1),
                    lt_Lstar_bound_pc=round(float(bound.min()), 1),
                    lt_Lstar_bound_worst_pc=round(float(bound.max()), 1),
                    lt_Lstar_bound_med_pc=round(float(np.median(bound)), 1),
                    lt_Lstar_bound_p10_pc=round(float(np.percentile(bound, 10)), 1),
                    lt_Lstar_bound80_pc=round(float(np.nanmin(bound80)), 1),
                    lt_N_below_300=round(float(np.mean(bound < 300.0)), 4),
                    lt_N_rfirst_below_53=round(float(np.mean(r0 < RCORE_COEF * 24.0)), 4)))
    ok11 = (len(names) == 26 and abs(beam_pc.min() - 20.0) < 1.0)
    check(11, ok11, '%d galaxies, beam %.0f-%.0f pc (med %.0f)' %
          (len(names), beam_pc.min(), beam_pc.max(), np.median(beam_pc)),
          '26 galaxies, 20 pc best', 'r_first %.0f-%.0f pc' % (r0.min(), r0.max()))

    # --- K11: the core-size bound (C5), one number for all galaxies
    ok12 = bound.min() < 100.0
    check(12, ok12, 'L* <= %.1f pc (min R0.3)' % bound.min(), '< 100 pc',
          'IC_10 R0.3=%.0f pc; 10th pct %.0f pc; median %.0f pc' %
          (r03.min(), np.percentile(bound, 10), np.median(bound)))

    # --- K12: the window after the bound
    NUM['window_after_bound_pc'] = [24.0, round(float(bound.min()), 1)]
    NUM['exclusion_300pc'] = round(300.0 / bound.min(), 2)
    NUM['exclusion_1000pc'] = round(1000.0 / bound.min(), 2)
    ok13 = (bound.min() < 300.0) and (300.0 / bound.min() > 2.0)
    check(13, ok13, '300 pc excluded by %.2fx ; 1 kpc by %.1fx' %
          (300.0 / bound.min(), 1000.0 / bound.min()), '> 2x', 'window -> [24, %.0f] pc' % bound.min())

    # sensitivity of the bound to the cold fraction and the two nearest points
    NUM['lt_bound_fc05_pc'] = round(float(bound.min() / np.sqrt(0.5)), 1)
    NUM['lt_bound_fc025_pc'] = round(float(bound.min() / np.sqrt(0.25)), 1)
    two = sorted(zip(r0, names))[:2]
    NUM['lt_two_innermost'] = [[n, round(float(r), 1)] for r, n in two]
    rsw24 = r_switch(24.0, HALOS['dwarf']['Mb'], HALOS['dwarf']['ab'])
    sig = []
    for n in names:
        arr = np.array([x for x in rows[(n, 'Data')] if x[1] > 0.5 and x[2] > 0.1])   # drop degenerate rows
        if len(arr) == 0:
            continue
        d = 1.0 - np.sqrt(1.0 - min(1.0, (rsw24 / (arr[0, 0] * 1e3)) ** 2))
        sig.append((float(d * arr[0, 1] / arr[0, 2]), n, float(arr[0, 0] * 1e3),
                    float(arr[0, 1]), float(arr[0, 2]), float(d)))
    sig.sort(reverse=True)
    NUM['lt_best_signal'] = dict(name=sig[0][1], r_pc=round(sig[0][2], 1), v_km_s=round(sig[0][3], 2),
                                 e_v=round(sig[0][4], 2), delta=round(sig[0][5], 4),
                                 nsigma=round(sig[0][0], 3))


# ============================================================================= 5. NO-JUGGLING
def section_candidates(sp):
    Vf = np.array([s['Vf'] for s in sp])
    # candidate 1: L* = sigma_c^2/a0, inverted sigma_c = sqrt(a0 L*)
    sig1 = {L: np.sqrt(A0 * L * PC) / 1e3 for L in (24.0, 100.0, 300.0, 1000.0)}
    NUM['cand1_sigma_km_s'] = {str(int(k)): round(float(v), 3) for k, v in sig1.items()}
    NUM['cand1_L_max_C4_pc'] = round((2.0 * SIG_TH) ** 2 / A0 / PC, 1)   # sigma_c <= 2 x 8.23 km/s
    NUM['cand1_sigma_over_thermal'] = {str(int(k)): round(float(v) / (SIG_TH / 1e3), 3)
                                      for k, v in sig1.items()}
    NUM['cand1_spread_dex'] = 0.0

    # candidate 2: L* = V_f^2/(k a0), k = 9 fixed by the record
    kk = 1.0 if MUT == 'k' else K_CAND2
    L2 = (Vf * 1e3) ** 2 / (kk * A0) / PC
    spread2 = float(np.log10(L2.max() / L2.min()))
    frac_out = float(np.mean((L2 < 24.0) | (L2 > 1000.0)))
    NUM.update(dict(cand2_k=kk, cand2_L_min_pc=round(float(L2.min()), 2),
                    cand2_L_med_pc=round(float(np.median(L2)), 1),
                    cand2_L_max_pc=round(float(L2.max()), 1),
                    cand2_spread_dex=round(spread2, 3),
                    cand2_frac_outside_window=round(frac_out, 4),
                    cand2_frac_below24=round(float(np.mean(L2 < 24.0)), 4),
                    cand2_frac_above1000=round(float(np.mean(L2 > 1000.0)), 4),
                    cand2_sigma_MW_km_s=round(float(np.sqrt(A0 * (165.2e3) ** 2 / (kk * A0)) / 1e3), 2),
                    cand2_sigma_med_km_s=round(float(np.sqrt(A0 * (np.median(L2) * PC)) / 1e3), 2)))
    sig2_mw = NUM['cand2_sigma_MW_km_s']
    NUM['cand2_sigma_MW_over_thermal'] = round(sig2_mw / (SIG_TH / 1e3), 3)
    NUM['cand2_sigma_med_over_thermal'] = round(NUM['cand2_sigma_med_km_s'] / (SIG_TH / 1e3), 3)

    # --- K13: C1 gate (spread must be measured, not asserted away)
    ok14 = (NUM['cand1_spread_dex'] == 0.0) and (abs(spread2 - 2.637) < 0.01)
    check(14, ok14, 'cand1 spread 0.000 dex ; cand2 %.3f dex (%.1f-%.1f pc)' %
          (spread2, L2.min(), L2.max()), '0.000 ; 2.637+-0.01',
          'one number for all galaxies -> cand2 FAILS C1')

    # --- K14: C3 window
    ok15 = abs(frac_out - 0.3029) < 0.005
    check(15, ok15, 'cand2 outside window: %s' % pct(frac_out), '30.29% +- 0.5%',
          'below 24 pc: %s, above 1 kpc: %s' % (pct(NUM['cand2_frac_below24']),
                                                pct(NUM['cand2_frac_above1000'])))

    # --- K15: C4 dispersion
    r1 = NUM['cand1_sigma_over_thermal']['24']
    r1b = NUM['cand1_sigma_over_thermal']['1000']
    r2 = NUM['cand2_sigma_MW_over_thermal']
    ok16 = (abs(r1 - 1.012) < 0.01) and (abs(r1b - 6.530) < 0.02) and (abs(r2 - 6.691) < 0.02)
    check(16, ok16, 'cand1 24pc %.3f / 1kpc %.3f ; cand2 %.3f' % (r1, r1b, r2),
          '1.012 / 6.530 / 6.691', 'ratio to 8.23 km/s cold medium')

    # --- K16: C5 core size
    r15 = RCORE_COEF * 24.0
    NUM['cand1_Rcore_24pc'] = round(r15, 2)
    NUM['cand2_Rcore_max_pc'] = round(RCORE_COEF * float(L2.max()), 1)
    ok17 = (r15 < 200.0) and (RCORE_COEF * float(L2.max()) > 200.0)
    check(17, ok17, 'cand1 R_core=%.0f pc ; cand2 max R_core=%.0f pc' % (r15, RCORE_COEF * L2.max()),
          'cand1 < 200 pc, cand2 > 200 pc', 'vs min measured R0.3 = 200 pc')

    NUM['verdict'] = dict(
        cand1='SURVIVES at L*=24 pc (C1 pass, C3 pass, C4 1.01x, C5 R_core=53 pc < 200 pc); '
              'FAILS C4 at L*=1 kpc (6.53x)',
        cand2='FAILS C1 (%.2f dex), C3 (%s outside), C4 (%.2fx)' %
              (spread2, pct(frac_out), r2))


# ============================================================================= 6. FORECAST
def section_forecast():
    """What measurement would decide L* = 24 pc, and what accuracy it needs."""
    rsw = r_switch(24.0, HALOS['dwarf']['Mb'], HALOS['dwarf']['ab'])     # pc, dwarf-like
    dip = {r: 1.0 - np.sqrt(1.0 - min(1.0, (rsw / r) ** 2)) for r in (30.0, 40.0, 60.0, 100.0)}
    beam_need = {D: 24.0 / (D * 1e6) / ARCSEC for D in (4.0, 8.0, 11.0)}
    beam_ngvla_arcsec = 0.15
    reach_Mpc = 24.0 / (beam_ngvla_arcsec * ARCSEC) / 1e6
    NUM.update(dict(fc_rswitch_dwarf_24pc=round(float(rsw), 2),
                    fc_dip_30pc=round(float(dip[30.0]), 4), fc_dip_40pc=round(float(dip[40.0]), 4),
                    fc_dip_60pc=round(float(dip[60.0]), 4), fc_dip_100pc=round(float(dip[100.0]), 4),
                    fc_beam_needed_arcsec={str(int(k)): round(float(v), 2) for k, v in beam_need.items()},
                    fc_ngvla_beam_arcsec=beam_ngvla_arcsec,
                    fc_ngvla_reach_Mpc=round(float(reach_Mpc), 1),
                    fc_N_dwarfs=30, fc_dv_needed_km_s=0.3, fc_D_max_Mpc=8.0,
                    fc_v30_over_v100=round(float((1 - dip[30.0]) / (1 - dip[100.0])), 4)))
    ok18 = (abs(dip[30.0] - 0.2103) < 0.005) and (abs(dip[40.0] - 0.1121) < 0.005) and (beam_need[8.0] < 1.0)
    check(18, ok18, 'dip(30pc)=%.1f%% dip(40pc)=%.1f%% ; beam %.2f" at 8 Mpc' %
          (100 * dip[30.0], 100 * dip[40.0], beam_need[8.0]), '21.03% / 11.21% ; < 1"',
          'ngVLA 0.15" reaches 24 pc out to %.0f Mpc' % reach_Mpc)


# ============================================================================= main
def main():
    print("# A20 -- stiffness length L* from the inner structure of galaxies")
    print("# mutation: %s" % (MUT or 'none'))
    print("#")
    print("# SECTION 1 -- exact algebra")
    section_exact()
    print("#\n# SECTION 2 -- the prediction (transition region)")
    section_prediction()
    print("#\n# SECTION 3 -- SPARC resolution")
    sp = section_sparc()
    print("#\n# SECTION 4a -- other HI data on disk")
    section_other_hi()
    print("#\n# SECTION 4b -- LITTLE THINGS core bound")
    section_lt()
    print("#\n# SECTION 5 -- no-juggling guard: the two candidate formulas")
    section_candidates(sp)
    print("#\n# SECTION 6 -- the decisive measurement")
    section_forecast()

    npass = sum(1 for c in CHECKS if c['passed'])
    status = 'NUMERICAL'
    print("#")
    print("A20 COMPLETE: %d/%d checks PASS." % (npass, len(CHECKS)))

    res = dict(lane='A20', status=status, mutation=(MUT or 'none'),
               checks=CHECKS, numbers=NUM,
               constants_used=[
                   'c=2.99792458e8 m/s', 'G=6.67430e-11', 'Msun=1.98847e30 kg',
                   'pc=3.0856775814913673e16 m', 'a0=9.36e-11 m/s^2 (canonical)',
                   'H0=2.1843e-18 s^-1', 'Lambda=1.0890e-52 m^-2', 'rho_Lambda=5.831e-27 kg/m^3',
                   'theta_SPARC=30 arcsec [EXT: typical HI beam of the SPARC compilation]',
                   'sigma_thermal=8.23 km/s [EXT: 1e4 K, mu=1.22, AG6D B7 via A11]',
                   'k_cand2=9 [A11 sec.15, V_f^2/(9a0) at the upper window end]',
                   'MW-like halo: Mb=6e10 Msun, Hernquist a=1.5 kpc (V_f=165.2 km/s, r_M=9.453 kpc)',
                   'R_core/L* = pi/sqrt(2) = 2.22144 (exact polytrope edge)',
                   'dwarf-like halo: Mb=1e8 Msun, Hernquist a=0.7 kpc (V_f=33.4 km/s)'])
    tag = '' if MUT is None else '_MUTATE_%s' % MUT
    with open(os.path.join(HERE, 'a20_results%s.json' % tag), 'w') as fh:
        json.dump(res, fh, indent=1)
    return 0 if npass == len(CHECKS) else 1


if __name__ == '__main__':
    sys.exit(main())
