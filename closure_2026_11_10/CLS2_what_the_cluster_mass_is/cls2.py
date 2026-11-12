#!/usr/bin/env python3
"""CLS2: what IS the cluster's non-baryonic mass under form B, given CLS1's NO STATE?

Criteria 7630e48454 (committed alone, before this file). Four candidates (a)-(d); kills pre-registered
in FROZEN_CRITERIA.md sections 4-5. TEST lane, quarantined: adopts nothing, relabels nothing.
Footings never pooled. kappa = 1/2 FITTED; not theory closed.

Run:  python3 -I cls2.py [out.json]        (add --mutate for the mutation arm)
"""
import csv
import json
import math
import runpy
import sys
import time
from pathlib import Path

import numpy as np
from astropy.io import fits
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRIOR = runpy.run_path(str(ROOT / 'research_closure_2026_11_10/DT2_response_audit/cluster/check_shape.py'),
                       run_name='dt2_readonly')
G, RHO_BG, A0, NAMES = PRIOR['G'], PRIOR['RHO_BG'], PRIOR['A0'], PRIOR['NAMES']
FOOT = ('canonical', 'alt')
C_KMS = 299792.458
KPC_PER_MPC = 1000.0
MU_CMB_MPC, MU_J_MPC = 198.25, 2.512e4
MU_CMB, MU_J = MU_CMB_MPC / KPC_PER_MPC, MU_J_MPC / KPC_PER_MPC
WIN_LO, WIN_HI = 2.97, 4.43            # CLS1's common cluster window, per Mpc
A0_SI = {'canonical': 9.3603e-11, 'alt': 1.1312e-10}    # DD1's rounded values; DD1 cross-checks only
FB_COSMIC = 0.156                      # XCV1: f_ret <= 1 at the edge <=> f_b <= 1/(1+R)
DD1_L2_XCOP = 14.4                     # DD1's L2 a0 for X-COP, x canonical [13.3, 17.5]
MSTAR_SCH, ALPHA_SCH = 10 ** 10.6, -1.1   # cluster galaxy Schechter, for the reported N_eff band
LINE_PARTIAL, LINE_FAIL = 0.10, 0.30
LN10 = math.log(10.0)

MUT = {k: False for k in ('M1', 'M2', 'M3', 'M4', 'M5')}
_mt = [a for a in sys.argv if a.startswith('--mutate')]
if _mt:
    sel = _mt[0].split('=', 1)[1] if '=' in _mt[0] else ''
    for k in (sel.split(',') if sel else MUT):
        MUT[k] = True
TAG = 'cls2_MUTATE' + ('_' + ''.join(sorted(k for k, v in MUT.items() if v))
                       if any(MUT.values()) else '') if any(MUT.values()) else 'cls2'
OUT = []
RES = dict(lane='CLS2', criteria='7630e48454', tag=TAG,
           note='adopts nothing; kappa = 1/2 FITTED; not theory closed')
T0 = time.time()


def P(s=''):
    OUT.append(str(s))
    print(s, flush=True)


def eff_a0(f):
    return 0.0 if MUT['M2'] else A0[f]


# -------------------------------------------------------------------------------------- the law
def law(gN, a0):
    return 0.5 * gN + math.sqrt(0.25 * gN * gN + a0 * gN)


def M_law(Mb, r, a0):
    if Mb <= 0:
        return 0.0
    return 0.5 * (Mb + math.sqrt(Mb * Mb + 4.0 * Mb * a0 * r * r / G))


def F_src(M, r, a0):
    return M * M / (M + a0 * r * r / G) if M > 0 else 0.0


def f_trunc(g, a0):
    if g <= 0:
        return float('inf')
    return 0.5 * (math.sqrt(1.0 + 4.0 * a0 / g) - 1.0)


def dex(a, b):
    return math.log10(a / b) if a > 0 and b > 0 else float('nan')


# ----------------------------------------------------------------------------------------- data
def interp(r, m, t):
    assert r[0] <= t <= r[-1]
    return float(10 ** np.interp(math.log10(t), np.log10(r), np.log10(m)))


def load_cluster(name):
    d = ROOT / 'real_research/data/xcop' / name
    with fits.open(d / f'{name}_hydro_mass.fits') as fh:
        hyd = fh[1].data.copy()
        r500 = float(fh[1].header['R500'])
        z = float(fh[1].header['REDSHIFT'])
    with fits.open(d / f'{name}_fgas_profile.fits') as fh:
        gas = fh[1].data.copy()
        rg500 = float(fh[1].header['R500'])
    with fits.open(d / f'{name}_mstar.fits') as fh:
        st = fh[2].data.copy()
    return dict(name=name, r500=r500, z=z,
                rg=np.asarray(gas['RADIUS'], float) * rg500, mg=np.asarray(gas['MGAS'], float),
                rs=np.asarray(st['RADIUS'], float), ms=np.asarray(st['MSTAR'], float),
                rh=np.asarray(hyd['RADIUS'], float), mh=np.asarray(hyd['M_FORW'], float),
                eh=np.asarray(hyd['EM_FORW'], float))


CL = {n: load_cluster(n) for n in NAMES}
XS = (0.1, 0.2, 0.3, 0.5, 0.7)
NFINE = 60

ROWS = {}
for n in NAMES:
    cl = CL[n]
    rows = []
    for x in XS:
        rr = x * cl['r500']
        mg = interp(cl['rg'], cl['mg'], rr)
        ms = interp(cl['rs'], cl['ms'], rr)
        rows.append(dict(x=x, r=rr, M=interp(cl['rh'], cl['mh'], rr), E=interp(cl['rh'], cl['eh'], rr),
                         mgas=mg, mstar=ms, B=mg + ms))
    ROWS[n] = rows


def profile_grids(cl):
    lo = max(cl['rg'][0], cl['rs'][0], 0.05 * cl['r500'])
    hi = min(cl['rg'][-1], cl['rs'][-1], 0.90 * cl['r500'])
    r = np.exp(np.linspace(math.log(lo), math.log(hi), NFINE))
    return r, np.array([interp(cl['rg'], cl['mg'], x) for x in r]), \
        np.array([interp(cl['rs'], cl['ms'], x) for x in r])


GRID = {n: profile_grids(CL[n]) for n in NAMES}


# ------------------------------------------------------------------------------------- physics
def potential_depth(r, M):
    """Psi(r_j) = int_{r_j}^{R_out} G M(r)/r^2 dr + G M(R_out)/R_out, on an ascending grid."""
    n = len(r)
    Psi = np.zeros(n)
    for j in range(n - 2, -1, -1):
        Mm = math.sqrt(max(M[j], 0.0) * max(M[j + 1], 0.0))
        Psi[j] = Psi[j + 1] + G * Mm * (1.0 / r[j] - 1.0 / r[j + 1])
    return Psi + G * M[-1] / r[-1]


def cum_mass(r, rho):
    n = len(r)
    out = np.zeros(n)
    out[0] = 4.0 * math.pi / 3.0 * r[0] ** 3 * rho[0]
    for j in range(n - 1):
        out[j + 1] = out[j] + 0.5 * (4.0 * math.pi * r[j] ** 2 * rho[j] +
                                     4.0 * math.pi * r[j + 1] ** 2 * rho[j + 1]) * (r[j + 1] - r[j])
    return out


def dust_response(r, M_obs, mu, niter=60):
    """Leading-order pooled dust of action (A): rho = (mu^2/4 pi G)(Psi - Psi(R_out)).
    Iterated to self-consistency. The first iteration uses the observed well only and is a strict
    LOWER BOUND (the dust's own gravity only deepens the well)."""
    mu2 = mu * mu
    Md1 = None
    prev = None
    growth = float('nan')
    M_tot = np.array(M_obs, float)
    for it in range(niter):
        Psi = potential_depth(r, M_tot)
        rho = mu2 / (4.0 * math.pi * G) * np.maximum(Psi - Psi[-1], 0.0)
        Md = cum_mass(r, rho)
        if it == 0:
            Md1 = Md.copy()
        if prev is not None and prev[-1] > 0:
            growth = Md[-1] / prev[-1]
            if growth >= 1.0:
                return Md1, None, growth, it + 1          # no static pooling: the response diverges
            if abs(growth - 1.0) < 1e-10:
                return Md1, Md, growth, it + 1
        prev = Md.copy()
        M_tot = np.array(M_obs, float) + Md
    return Md1, prev, growth, niter


def at_nodes(r, M, rows):
    return np.array([float(np.interp(q['r'], r, M)) for q in rows])


def schechter_neff(Mtot, mstar=MSTAR_SCH, alpha=ALPHA_SCH):
    """N_eff = (sum sqrt(m_i))^2 / sum m_i for a Schechter mass function of total stellar mass Mtot."""
    return max(1.0, Mtot / mstar * math.gamma(alpha + 1.5) ** 2 / math.gamma(alpha + 2.0) ** 2)


NEFF_SCH = {n: schechter_neff(float(np.mean([q['mstar'] for q in ROWS[n]]))) for n in NAMES}

# ================================================================================== KA: sympy
P('CLS2: what IS the cluster non-baryonic mass under form B?  criteria 7630e48454')
P(f'mutate: {any(MUT.values())}  flags {[k for k, v in MUT.items() if v]}')
P('')
P('KA: exact algebra (sympy)')
KA = {}
Mb_, r_, a0_, m_, g_, N_, mu_, R_, x_ = sp.symbols('M_b r a_0 m g N mu R x', positive=True)
GG = sp.Symbol('G', positive=True)
ML = (Mb_ + sp.sqrt(Mb_ ** 2 + 4 * Mb_ * a0_ * r_ ** 2 / GG)) / 2
FS = sp.Symbol('M', positive=True)
FSRC = FS ** 2 / (FS + a0_ * r_ ** 2 / GG)
FF = (sp.sqrt(1 + 4 * a0_ / g_) - 1) / 2

KA['KA2_inverse'] = bool(sp.simplify(FSRC.subs(FS, ML) - Mb_) == 0)
KA['KA2_ratio'] = bool(sp.simplify(ML / Mb_ - (1 + FF.subs(g_, GG * Mb_ / r_ ** 2))) == 0)
KA['KA3_superposition'] = bool(sp.simplify(N_ * ML.subs(Mb_, Mb_ / N_) - ML.subs(a0_, N_ * a0_)) == 0)
KA['KA4_truncation'] = bool(sp.simplify(ML.subs({Mb_: m_, r_: sp.sqrt(GG * m_ / g_)}) - m_ - m_ * FF) == 0)
Mdust_pm = mu_ ** 2 / GG * sp.integrate((GG * Mb_ / x_ - GG * Mb_ / R_) * x_ ** 2, (x_, 0, R_))
Mph_deep = R_ * sp.sqrt(Mb_ * a0_ / GG)
KA['KA5_M_dust_pointmass'] = sp.sstr(sp.simplify(Mdust_pm))
KA['KA5_ratio_closed'] = sp.sstr(sp.simplify(Mdust_pm / Mph_deep))
KA['KA5_ratio_is_mu2R2_over_6'] = bool(sp.simplify(
    Mdust_pm / Mph_deep - (mu_ * R_) ** 2 / 6 * sp.sqrt(GG * Mb_ / R_ ** 2 / a0_)) == 0)
for k, v in KA.items():
    P(f'  {k}: {v}')
RES['KA_sympy'] = {k: str(v) for k, v in KA.items()}

# ====================================================================== baseline: the law (KA1)
P('')
P('BASELINE: the bare law, DT2/CLS1 convention (mean over the 35 graded nodes)')
base = {}
for f in FOOT:
    a0 = eff_a0(f)
    per = {}
    for n in NAMES:
        d = [dex(q['M'], M_law(q['B'], q['r'], a0)) for q in ROWS[n]]
        per[n] = dict(per_node=d, mean=float(np.mean(d)),
                      err=float(np.sqrt(sum((q['E'] / (q['M'] * LN10)) ** 2 for q in ROWS[n])) / len(XS)))
    flat = [v for n in NAMES for v in per[n]['per_node']]
    base[f] = dict(per_cluster={n: per[n]['mean'] for n in NAMES},
                   err_cluster={n: per[n]['err'] for n in NAMES},
                   mean35=float(np.mean(flat)),
                   median=float(np.median([per[n]['mean'] for n in NAMES])),
                   range=[min(per[n]['mean'] for n in NAMES), max(per[n]['mean'] for n in NAMES)])
    P(f'  {f}: mean35 {base[f]["mean35"]:.8f}  median {base[f]["median"]:.4f}  '
      f'range {base[f]["range"][0]:.4f}..{base[f]["range"][1]:.4f}')
    P('    per cluster: ' + '  '.join(f'{n} {per[n]["mean"]:+.3f}' for n in NAMES))
RES['baseline_law'] = base
KA1_EXP = {'canonical': 0.46749899, 'alt': 0.43452310}
ka1_ok = bool(all(abs(base[f]['mean35'] - KA1_EXP[f]) < 1e-6 for f in FOOT))
P(f'  KA1 (DT2/CLS1 0.46749899 / 0.43452310): {"PASS" if ka1_ok else "FAIL"}')
RES['KA1'] = dict(pass_=ka1_ok, got={f: base[f]['mean35'] for f in FOOT}, expected=KA1_EXP)

# ==================================================================== KA6/KA7: DD1 cross-checks
P('')
P('KA6/KA7: DD1 frozen table cross-check (read-only)')
dd = {}
dd1 = ROOT / 'fable52_push/DD1_deduce_from_data/dd1_table.csv'
if dd1.exists():
    with open(dd1) as fh:
        lines = [l for l in fh if not l.startswith('#')]
    rows = list(csv.DictReader(lines))
    for cls in ('X-COP', 'CLASH'):
        sub = [q for q in rows if q['cls'] == cls]
        for f in FOOT:
            a0 = A0_SI[f]
            off = [float(q['lgo']) - math.log10(law(10 ** float(q['lgb']), a0)) for q in sub]
            dd[(cls, f)] = dict(n=len(sub), mean=float(np.mean(off)), median=float(np.median(off)))
    for k in sorted(dd, key=lambda k: (k[0], k[1])):
        P(f'  {k[0]:7s} {k[1]:9s}: n {dd[k]["n"]:3d}  mean {dd[k]["mean"]:+.3f} dex  '
          f'median {dd[k]["median"]:+.3f} dex')
    ka6 = bool(0.40 <= dd[('X-COP', 'canonical')]['mean'] <= 0.55)
    ka7 = bool(dd[('CLASH', 'canonical')]['mean'] >= 0.30 and dd[('CLASH', 'alt')]['mean'] >= 0.30)
    P(f'  KA6 (X-COP 0.42-0.55): {"PASS" if ka6 else "FAIL"};   '
      f'KA7 (CLASH >= 0.30 both footings): {"PASS" if ka7 else "FAIL"}')
    RES['KA6_KA7'] = dict(pass_KA6=ka6, pass_KA7=ka7, table={f'{k[0]}|{k[1]}': v for k, v in dd.items()})
else:
    P('  dd1_table.csv absent: KA6/KA7 NOT EVALUABLE')
    RES['KA6_KA7'] = dict(pass_KA6=False, pass_KA7=False)

# ================================================================================== (a) non-HSE
P('')
P('(a) NON-HYDROSTATIC SUPPORT')
a_res = {}
hecs_p = ROOT.parent / '_external_data/hecs_omnibus_2026_11_10/table2.tsv'
HECS_ID = {'A85': 'A85', 'A1795': 'A1795', 'ZW1215': 'Zw1215', 'A2029': 'A2029', 'A2142': 'A2142',
           'A2319': 'A2319', 'A644': 'A644'}
Qd = {}
if hecs_p.exists():
    with open(hecs_p) as fh:
        lines = [l.rstrip('\n') for l in fh if not l.startswith('#') and l.strip()]
    head = lines[0].split('\t')
    for l in lines[3:]:
        p = [c.strip() for c in l.split('\t')]
        if len(p) < len(head):
            continue
        try:
            Qd[p[head.index('ID')]] = dict(R200=float(p[head.index('R200')]),
                                           M200=float(p[head.index('M200')]))
        except (ValueError, IndexError):
            pass
qrows = {}
for n in NAMES:
    h = Qd.get(HECS_ID.get(n, ''), None)
    if not h:
        continue
    R = h['R200'] * 1000.0
    cl = CL[n]
    if not (cl['rh'][0] <= R <= cl['rh'][-1]):
        continue
    qrows[n] = dict(R200=R, Mcaus=h['M200'] * 1e14, Mforw=interp(cl['rh'], cl['mh'], R),
                    Q=h['M200'] * 1e14 / interp(cl['rh'], cl['mh'], R))
qs = sorted(v['Q'] for v in qrows.values())
a_res['a1'] = dict(per_cluster={k: v['Q'] for k, v in qrows.items()}, n=len(qs),
                   median=float(np.median(qs)) if qs else float('nan'),
                   all_below_one=bool(qs and max(qs) < 1.0))
P(f"  a1 HeCS caustic / hydrostatic at the same R200: n {a_res['a1']['n']}, "
  f"median Q {a_res['a1']['median']:.3f}, every cluster below 1: {a_res['a1']['all_below_one']}")
P('     ' + '  '.join(f'{k} {v:.3f}' for k, v in sorted(a_res['a1']['per_cluster'].items())))
a_res['a1_wrong_sign_dex'] = -math.log10(a_res['a1']['median']) if a_res['a1']['median'] > 0 else float('nan')
P(f"  a1 => (a) moves the residual the WRONG WAY, by {a_res['a1_wrong_sign_dex']:+.3f} dex")
a_res['a2_proof'] = ('CLS1 S2a: the clock stress is a perfect fluid (sympy residual 0) - one velocity '
                     'per point, isotropic p = n x / 2, zero momentum density. No dispersion support.')
a_res['a3_clash'] = {f: dd.get(('CLASH', f), {}).get('mean', float('nan')) for f in FOOT}
P(f"  a3 CLASH lensing residual (makes no HSE assumption): "
  f"{a_res['a3_clash']['canonical']:+.3f} / {a_res['a3_clash']['alt']:+.3f} dex")
a_res['kills'] = dict(K_A1=bool(a_res['a1']['all_below_one']), K_A2=True,
                      K_A3=bool(a_res['a3_clash']['canonical'] >= 0.30 and a_res['a3_clash']['alt'] >= 0.30))
a_res['verdict'] = 'KILLED BY PROOF' if a_res['kills']['K_A2'] else (
    'FAILS' if any(a_res['kills'].values()) else 'PARTIAL')
P(f"  (a) verdict: {a_res['verdict']}   kills {a_res['kills']}")
RES['a_nonhydrostatic'] = a_res

# ============================================================================ (b) dust over-capture
P('')
P('(b) THE DUST TERM POOLED IN THE WELL')
b_res = {}
mu_b = (WIN_LO / KPC_PER_MPC) if MUT['M3'] else MU_CMB
mu_b_mpc = mu_b * KPC_PER_MPC
Rb, mufit, detail = {}, {}, {}
for n in NAMES:
    r, mg, ms = GRID[n]
    Mb = mg + ms
    Mob = np.array([interp(CL[n]['rh'], CL[n]['mh'], x) for x in r])
    Mnb = Mob - Mb
    Md1, Mdc, gr, nit = dust_response(r, Mob, mu_b)
    Md1n = at_nodes(r, Md1, ROWS[n])
    Mnbn = at_nodes(r, Mnb, ROWS[n])
    Rb[n] = float(np.median(Md1n / Mnbn))
    mufit[n] = float(np.median(mu_b_mpc * np.sqrt(Mnbn / np.maximum(Md1n, 1e-300))))
    detail[n] = dict(R_b=Rb[n], mu_fit_per_Mpc=mufit[n],
                     growth_per_iter=None if not np.isfinite(gr) else float(gr),
                     converged=bool(Mdc is not None), iters=int(nit),
                     R_b_per_node=(Md1n / Mnbn).tolist())
    P(f'  {n:7s}: R_b(mu={mu_b_mpc:g}/Mpc) {Rb[n]:.3e}   mu_fit {mufit[n]:.4g}/Mpc   '
      f'growth/iter {gr:.3e}   {"CONVERGES" if Mdc is not None else "DIVERGES"}')
b_res['detail'] = detail
b_res['R_b_median'] = float(np.median(list(Rb.values())))
b_res['R_b_log10'] = math.log10(b_res['R_b_median'])
b_res['mu_fit_median_per_Mpc'] = float(np.median(list(mufit.values())))
b_res['mu_fit_below_CMB'] = bool(b_res['mu_fit_median_per_Mpc'] < MU_CMB_MPC)
b_res['mu_fit_in_CLS1_window'] = bool(WIN_LO <= b_res['mu_fit_median_per_Mpc'] <= WIN_HI)
b_res['diverges_all'] = bool(not any(d['converged'] for d in detail.values()))
P(f'  median R_b {b_res["R_b_median"]:.3e}  (log10 {b_res["R_b_log10"]:+.2f} dex, + is over-capture)')
P(f'  median mu_fit {b_res["mu_fit_median_per_Mpc"]:.4g}/Mpc: below the CMB line {MU_CMB_MPC}: '
  f'{b_res["mu_fit_below_CMB"]}; in CLS1 window {WIN_LO}-{WIN_HI}: {b_res["mu_fit_in_CLS1_window"]}')
P(f'  the self-consistent pooling iteration DIVERGES on all seven: {b_res["diverges_all"]}')
Rb_J = {}
for n in NAMES:
    r, mg, ms = GRID[n]
    Mob = np.array([interp(CL[n]['rh'], CL[n]['mh'], x) for x in r])
    Md1, _, _, _ = dust_response(r, Mob, MU_J)
    Rb_J[n] = float(np.median(at_nodes(r, Md1, ROWS[n]) / at_nodes(r, Mob - (mg + ms), ROWS[n])))
b_res['R_b_median_at_muJ'] = float(np.median(list(Rb_J.values())))
P(f'  at the CMB-lensing line mu_J {MU_J_MPC:g}/Mpc: median R_b {b_res["R_b_median_at_muJ"]:.3e}')
# b3: the same dust against the LAW'S PHANTOM - the direct analogue of AKS1 T5's quoted 3.6-8.4
Rp = {}
for f in FOOT:
    a0 = eff_a0(f)
    per = {}
    for n in NAMES:
        r, mg, ms = GRID[n]
        Mb = mg + ms
        Mob = np.array([interp(CL[n]['rh'], CL[n]['mh'], x) for x in r])
        Md1, _, _, _ = dust_response(r, Mob, mu_b)
        Md1n = at_nodes(r, Md1, ROWS[n])
        ph = np.array([M_law(q['B'], q['r'], a0) - q['B'] for q in ROWS[n]])
        per[n] = float(np.median(Md1n / ph))
    Rp[f] = dict(per_cluster=per, median=float(np.median(list(per.values()))))
    P(f'  b3 {f}: M_dust / the law\'s phantom, median {Rp[f]["median"]:.3e}   '
      + '  '.join(f'{n} {per[n]:.2e}' for n in NAMES))
b_res['b3_dust_over_phantom'] = Rp
P('  (AKS1 T5 quotes 3.6-8.4 for this ratio at SPARC radii; the point-mass form is '
  '(mu R)^2/6 x sqrt(g_N/a0), so at fixed mu it grows as R^2.)')
b_res['kills'] = dict(K_B1=bool(b_res['R_b_log10'] > LINE_FAIL),
                      K_B2=bool(b_res['mu_fit_below_CMB'] or not b_res['mu_fit_in_CLS1_window']),
                      K_B3=True)
b_res['verdict'] = 'KILLED BY PROOF' if b_res['kills']['K_B3'] else (
    'FAILS' if any(b_res['kills'].values()) else 'PARTIAL')
P(f'  (b) verdict: {b_res["verdict"]}   kills {b_res["kills"]}')
RES['b_dust_pooled'] = b_res

# ============================================================================== (c) gas census
P('')
P('(c) THE GAS IS UNDER-COUNTED')
c_res = {}
gasfac = 3.0 if MUT['M4'] else 1.0
for f in FOOT:
    a0 = eff_a0(f)
    res, rgs, fb = {}, {}, {}
    for n in NAMES:
        rr = ROWS[n]
        B = np.array([q['B'] + (gasfac - 1.0) * q['mgas'] for q in rr])
        req = np.array([F_src(q['M'], q['r'], a0) for q in rr])
        res[n] = float(np.mean([dex(q['M'], M_law(B[i], q['r'], a0)) for i, q in enumerate(rr)]))
        rgs[n] = float(np.mean(req / B))
        fb[n] = float(np.mean(req / np.array([q['M'] for q in rr])))
    c_res[f] = dict(residual=res, R_gas=rgs, f_b_req=fb,
                    median_R_gas=float(np.median(list(rgs.values()))),
                    median_f_b=float(np.median(list(fb.values()))),
                    all_f_b_over_cosmic=bool(all(v > FB_COSMIC for v in fb.values())))
    P(f'  {f}: median R_gas {c_res[f]["median_R_gas"]:.3f}   median f_b,req {c_res[f]["median_f_b"]:.4f} '
      f'(cosmic share {FB_COSMIC})   all seven over the cosmic share: {c_res[f]["all_f_b_over_cosmic"]}')
    P('    R_gas per cluster:  ' + '  '.join(f'{n} {rgs[n]:.2f}' for n in NAMES))
    P('    f_b,req per cluster:' + '  '.join(f'{n} {fb[n]:.3f}' for n in NAMES))
    P(f'    residual if the gas were multiplied by {gasfac:.0f}: '
      + '  '.join(f'{n} {res[n]:+.3f}' for n in NAMES))
kills_c = {f: dict(K_C1=bool(c_res[f]['all_f_b_over_cosmic']),
                   K_C2=bool(c_res[f]['median_R_gas'] > 3.0)) for f in FOOT}
for f in FOOT:
    c_res[f]['kills'] = kills_c[f]
    c_res[f]['verdict'] = 'FAILS' if any(kills_c[f].values()) else 'PARTIAL'
    P(f'  (c) verdict {f}: {c_res[f]["verdict"]}   kills {c_res[f]["kills"]}')
RES['c_gas_census'] = c_res

# ============================================================== (d) superposition of galaxy halos
P('')
P('(d) SUPERPOSITION OF GALAXY HALOS, ONE PER MEMBER')
P(f'  Schechter N_eff (log M* {math.log10(MSTAR_SCH):.1f}, alpha {ALPHA_SCH}): '
  + '  '.join(f'{n} {NEFF_SCH[n]:.0f}' for n in NAMES))
d_res = {}
for f in FOOT:
    a0 = eff_a0(f)
    dtr, dtrs, need_med, need_spread, atL2, atsch, need_all = {}, {}, {}, {}, {}, {}, {}
    for n in NAMES:
        r, mg, ms = GRID[n]
        Mb = mg + ms
        rows = ROWS[n]
        gN = G * Mb / r ** 2
        fmid = np.array([f_trunc(0.5 * (gN[max(i - 1, 0)] + gN[i]), a0) for i in range(len(r))])
        if MUT['M1']:
            fmid = np.full_like(r, f_trunc(gN[-1], a0))
        # d-TRUNC: every baryon in a member, each halo truncated by the local cluster field
        integ = np.empty(len(r))
        integ[0] = fmid[0] * Mb[0]
        integ[1:] = integ[0] + np.cumsum(fmid[1:] * np.diff(Mb))
        Mt = Mb + integ
        dtr[n] = float(np.mean([dex(q['M'], float(np.interp(q['r'], r, Mt))) for q in rows]))
        # d-TRUNC-s: only the stars in members; the gas keeps its cluster-level share
        integs = np.empty(len(r))
        integs[0] = fmid[0] * ms[0]
        integs[1:] = integs[0] + np.cumsum(fmid[1:] * np.diff(ms))
        Mts = Mb + integs + mg * np.array([f_trunc(x, a0) for x in gN])
        dtrs[n] = float(np.mean([dex(q['M'], float(np.interp(q['r'], r, Mts))) for q in rows]))
        # d-FREE: N_eff equal members == the law with a0 -> N_eff a0 on the stellar mass
        need = []
        for q in rows:
            Mstar, Mgas, R, Mo = q['mstar'], q['mgas'], q['r'], q['M']
            gshare = M_law(Mgas, R, a0)
            tot = lambda Ne: M_law(Mstar, R, Ne * a0) + gshare
            if MUT['M5'] or tot(1.0) >= Mo:
                need.append(1.0)
                continue
            lo, hi = 1.0, 2.0
            while tot(hi) < Mo and hi < 1e9:
                hi *= 2.0
            if tot(hi) < Mo:
                need.append(1e9)          # no finite N_eff closes it (a0 -> 0 case)
                continue
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if tot(mid) < Mo:
                    lo = mid
                else:
                    hi = mid
            need.append(0.5 * (lo + hi))
        need_all[n] = need
        need_med[n] = float(np.median(need))
        need_spread[n] = float(max(need) / max(min(need), 1e-12))
        atL2[n] = float(np.mean([dex(q['M'], M_law(q['mstar'], q['r'], DD1_L2_XCOP * a0)
                                     + M_law(q['mgas'], q['r'], a0)) for q in rows]))
        atsch[n] = float(np.mean([dex(q['M'], M_law(q['mstar'], q['r'], NEFF_SCH[n] * a0)
                                      + M_law(q['mgas'], q['r'], a0)) for q in rows]))
    d_res[f] = dict(d_trunc=dtr, d_trunc_s=dtrs, N_eff_req=need_med, N_eff_req_all=need_all,
                    N_eff_req_spread=need_spread, res_at_DD1_L2=atL2, res_at_schechter=atsch,
                    median_d_trunc=float(np.median(list(dtr.values()))),
                    median_d_trunc_s=float(np.median(list(dtrs.values()))),
                    median_N_eff_req=float(np.median(list(need_med.values()))),
                    median_N_eff_spread=float(np.median(list(need_spread.values()))),
                    median_res_at_L2=float(np.median(list(atL2.values()))),
                    median_res_at_schechter=float(np.median(list(atsch.values()))))
    P(f'  {f}: d-TRUNC median residual {d_res[f]["median_d_trunc"]:+.3f} dex   '
      f'(bare law {base[f]["median"]:+.3f});  d-TRUNC-s {d_res[f]["median_d_trunc_s"]:+.3f}')
    P('    d-TRUNC per cluster: ' + '  '.join(f'{n} {dtr[n]:+.3f}' for n in NAMES))
    P(f'    d-FREE N_eff required (median {d_res[f]["median_N_eff_req"]:.1f}, '
      f'radial spread max/min median {d_res[f]["median_N_eff_spread"]:.1f}):')
    for n in NAMES:
        P(f'      {n:7s} ' + '  '.join(f'{v:.1f}' for v in need_all[n]))
    P(f'    d-FREE residual at DD1 L2 N_eff = {DD1_L2_XCOP}: {d_res[f]["median_res_at_L2"]:+.3f} dex;   '
      f'at the Schechter N_eff: {d_res[f]["median_res_at_schechter"]:+.3f} dex')
for f in FOOT:
    d_res[f]['kills'] = dict(K_D1=bool(d_res[f]['median_d_trunc'] >= base[f]['median'] - LINE_PARTIAL),
                             K_D2=bool(d_res[f]['median_N_eff_req'] > 100.0), K_D3=True)
    d_res[f]['verdict'] = 'KILLED BY PROOF' if d_res[f]['kills']['K_D3'] else (
        'FAILS' if any(d_res[f]['kills'].values()) else 'PARTIAL')
    P(f'  (d) verdict {f}: {d_res[f]["verdict"]}   kills {d_res[f]["kills"]}')
RES['d_superposition'] = d_res

# ==================================================================================== labels
P('')
P('LABELS (per footing)')
verd = {f: dict(a=a_res['verdict'], b=b_res['verdict'], c=c_res[f]['verdict'], d=d_res[f]['verdict'])
        for f in FOOT}
best = {}
for f in FOOT:
    resd = {'a': base[f]['median'] + a_res['a1_wrong_sign_dex'],
            'b': -b_res['R_b_log10'],
            'c': float(np.median(list(c_res[f]['residual'].values()))),
            'd': d_res[f]['median_d_trunc']}
    ok = [k for k in 'abcd' if verd[f][k] == 'SUPPLIES THE MASS']
    part = [k for k in 'abcd' if verd[f][k] == 'PARTIAL']
    bk = min('abcd', key=lambda k: abs(resd[k]))
    if ok:
        lab = f'{ok[0].upper()} SUPPLIES THE MASS'
    elif part:
        lab = f'BEST IS ({min(part, key=lambda k: abs(resd[k]))}), ' \
              f'RESIDUAL {resd[min(part, key=lambda k: abs(resd[k]))]:+.2f} dex'
    else:
        nq = d_res[f]['median_N_eff_req']
        lab = ('NO CANDIDATE; (d) truncated by the cluster field reads '
               f'{resd["d"]:+.2f} dex' if nq <= 1.001 else
               f'NO CANDIDATE; (d)-FREE would need N_eff {nq:.0f} (0.00 dex by construction) but the '
               f'cluster field truncates it to N_eff = 1, where (d) reads {resd["d"]:+.2f} dex')
    best[f] = dict(label=lab, verdicts=verd[f], residual_dex=resd, best_candidate=bk,
                   best_residual_dex=resd[bk])
    P(f'  {f}: {lab}')
    P(f'    verdicts {verd[f]}')
    P('    residual in dex against M_FORW (+ = the candidate still falls short): '
      + '  '.join(f'{k} {v:+.3f}' for k, v in resd.items()))
RES['labels'] = best

if any(MUT.values()):
    P('')
    P('MUTATE: every twin must move a graded number by >= 0.10 dex or flip a verdict')
    main = HERE / 'cls2.json'
    if main.exists():
        try:
            with open(main) as fh:
                B = json.load(fh)
        except Exception:
            B = None
        if B:
            A = RES
            rows = [
                ('baseline law mean35 canonical',
                 A['baseline_law']['canonical']['mean35'] - B['baseline_law']['canonical']['mean35']),
                ('(b) log10 R_b',
                 A['b_dust_pooled']['R_b_log10'] - B['b_dust_pooled']['R_b_log10']),
                ('(b) mu_fit per Mpc',
                 A['b_dust_pooled']['mu_fit_median_per_Mpc'] - B['b_dust_pooled']['mu_fit_median_per_Mpc']),
                ('(c) median R_gas canonical',
                 A['c_gas_census']['canonical']['median_R_gas'] - B['c_gas_census']['canonical']['median_R_gas']),
                ('(c) median f_b,req canonical',
                 A['c_gas_census']['canonical']['median_f_b'] - B['c_gas_census']['canonical']['median_f_b']),
                ('(d) d-TRUNC median canonical',
                 A['d_superposition']['canonical']['median_d_trunc'] -
                 B['d_superposition']['canonical']['median_d_trunc']),
                ('(d) N_eff required canonical',
                 A['d_superposition']['canonical']['median_N_eff_req'] -
                 B['d_superposition']['canonical']['median_N_eff_req']),
            ]
            P('    flags on: ' + ','.join(k for k, v in MUT.items() if v))
            P('    number                                change (this twin - main)')
            for nm, dv in rows:
                P(f'    {nm:36s} {dv:+.4f}')
            bit = any(abs(dv) >= LINE_PARTIAL for _, dv in rows)
            P(f'    at least one graded number moved by >= {LINE_PARTIAL} dex: {bit}  '
              f'({"BITES" if bit else "DOES NOT BITE"})')
            RES['mutate_deltas'] = {nm: float(dv) for nm, dv in rows}
            RES['mutate_bites'] = bool(bit)
        else:
            P('    cls2.json absent: run the main pass first')
    else:
        P('    cls2.json absent: run the main pass first')
RES['mutate_flags'] = MUT
RES['footings_pooled'] = False
RES['runtime_s'] = time.time() - T0

out = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else f'{TAG}.json'
with open(HERE / out, 'w') as fh:
    json.dump(RES, fh, indent=1, default=str)
with open(HERE / (TAG + '.out'), 'w') as fh:
    fh.write('\n'.join(OUT) + '\n')
P('')
P(f'wrote {out} and {TAG}.out in {RES["runtime_s"]:.1f} s')
P('Adopts nothing. kappa = 1/2 FITTED; not theory closed.')
