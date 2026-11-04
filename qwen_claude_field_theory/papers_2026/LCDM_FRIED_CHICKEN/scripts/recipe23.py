"""A21: "the law simply emerges in LCDM hydrodynamic simulations", per ../FROZEN_A21.md.
Grades PUBLISHED simulation RAR reports (provisional web look-ups, see FROZEN_A21.md table) on SPARC and on tie gates G1-G4.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
c_ = 2.998e8; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
MPC = 3.0857e22
def acp(OL, H0): return c_ * (H0 * 1e3 / MPC) * np.sqrt(3 * OL / (8 * np.pi))   # c sqrt(G rho_DE) in the paper's cosmology
def mcg(gb, gd): return gb / (1 - np.exp(-np.sqrt(gb / gd)))
def pwl(gb, A, B): return 10**(A * np.log10(gb) + B)
print(f'lib cosmology OL {cos.Ode0:.3f}: c sqrt(G rho_DE) {AC:.4e}; A0 {A0:.4e}')
print(f'law on SPARC at A0: rms to observed {np.sqrt(np.mean((np.log10(ALLO) - np.log10(ALLL))**2)):.4f} dex')
# name, curve(gb), OL, H0, quoted error on g_dag (1e-10) or None, provenance tag
E = [
 ('McGaugh16 SPARC g_dag 1.20 (reference, observational)', lambda b: mcg(b, 1.20e-10), cos.Ode0, 67.4, .02, 'OBS'),
 ('MUGS2 Keller&Wadsley17 (no fit; SPARC 1.20 accepted)', lambda b: mcg(b, 1.20e-10), .76, 73., None, 'EMERGENT, not fitted'),
 ('EAGLE Ludlow17 raw fit g_dag 2.6', lambda b: mcg(b, 2.6e-10), .693, 67.77, None, 'CALIBRATED GSMF+sizes'),
 ('EAGLE Ludlow17 g_dag 3.0 (as quoted by others)', lambda b: mcg(b, 3.0e-10), .693, 67.77, None, 'CALIBRATED GSMF+sizes'),
 ('MBII Tenneti18 power law full', lambda b: pwl(b, .6849, -2.759), .725, 70.2, None, 'EMERGENT'),
 ('MBII Tenneti18 McGaugh full g_dag 2.01', lambda b: mcg(b, 2.01e-10), .725, 70.2, .004, 'EMERGENT'),
 ('MBII Tenneti18 McGaugh faint g_dag 1.151', lambda b: mcg(b, 1.151e-10), .725, 70.2, .003, 'EMERGENT'),
 ('NIHAO Dutton19 (no fit; SPARC 1.20 compared)', lambda b: mcg(b, 1.20e-10), .6825, 67.1, None, 'CALIBRATED SMHR (memory)'),
 ('ZOMG Garaldi18 centrals g_dag 1.40', lambda b: mcg(b, 1.40e-10), .692, 67.8, .07, 'matches SMHR (calib. not stated)'),
 ('ZOMG Garaldi18 centrals ODR g_dag 1.19', lambda b: mcg(b, 1.19e-10), .692, 67.8, .02, 'matches SMHR (calib. not stated)'),
 ('Magneticum Mayer22 z=0.1 RAR g_dag 1.14', lambda b: mcg(b, 1.14e-10), .728, 70.4, .04, 'calibration unknown'),
 ('FIRE-2 Mercado24 (no fit; SPARC 1.20 compared)', lambda b: mcg(b, 1.20e-10), .69, 68., None, 'EMERGENT (memory)'),
 ('Navarro17 analytic a0 ~1.0 (McGaugh form, order of magnitude)', lambda b: mcg(b, 1.0e-10), .693, 67.77, None, 'analytic, halo scale'),
 ('Grudic20 feedback scale pi G Sigma_crit ~1.0 (McGaugh form)', lambda b: mcg(b, 1.0e-10), cos.Ode0, 67.4, None, 'analytic, no cosmology'),
]
od = range(1, len(GS), 2); rows = []
for nm, f, OL, H0, er, tag in E:
    cur = [f(g.gb) for g in GS]; e1 = grade(nm, cur, f'[{tag}]')
    hu = np.sqrt(np.mean(np.concatenate([(np.log10(cur[j]) - np.log10(GS[j].gl))**2 for j in od])))
    ae = fit_a(ALLB, np.concatenate(cur)); k = ae / AC; kp = ae / acp(OL, H0); d1 = np.log10(k / .5); d1p = np.log10(kp / .5)
    print(f' holdout (no tuning): unseen rms to law GS[1::2] {hu:.4f} [{"PASS" if hu <= .025 else "FAIL"}]')
    print(f' a0_equiv {ae:.3e}; G1 kappa_eff lib cosmology {k:.3f} ({d1:+.3f} dex) [{"PASS" if abs(d1) <= .05 else "FAIL"}]; own cosmology (OL {OL}, H0 {H0}) {kp:.3f} ({d1p:+.3f} dex) [{"PASS" if abs(d1p) <= .05 else "FAIL"}]')
    if er:
        tol = np.sqrt(.05**2 + (er / (np.log(10) * float(nm.split('g_dag ')[-1].split()[0]) if 'g_dag' in nm else 1.))**2)
        print(f' G1 with quoted error in quadrature: tol {tol:.3f} dex -> [{"PASS" if abs(d1p) <= tol else "FAIL"}] (diagnostic)')
    rows.append((nm, ae, OL, H0, tag, e1, hu))

print('\nG2 (slope d ln a0 / d ln rho_DE): NO suite with RAR at two Lambda values found (Barnes/Salcido 2018 EAGLE varied-Lambda report no RAR, concentration, Vmax or size vs Lambda). NOT TESTABLE.')
fit_rows = [r for r in rows if r[0].split()[0] in ('EAGLE', 'MBII', 'ZOMG', 'Magneticum') and ('fit' in r[0] or 'full' in r[0] or 'centrals g_dag' in r[0] or 'z=0.1' in r[0]) and 'power' not in r[0] and '3.0' not in r[0]]
x = np.log10([r[2] * r[3]**2 for r in fit_rows]); y = np.log10([r[1] for r in fit_rows]); s = np.polyfit(x, y, 1)[0]
print(' DIAG cross-suite (different feedback, NOT a gate):', '; '.join(f'{r[0].split()[0]} rho_DE~{r[2] * r[3]**2:.0f} a0_eq {r[1]:.2e}' for r in fit_rows))
print(f' DIAG cross-suite slope {s:+.2f} over {x.max() - x.min():.3f} dex in rho_DE vs {y.max() - y.min():.3f} dex in a0_equiv (feedback dominates; meaningless as G2)')

print('\nG3 redshift (a0_equiv(z)/a0_equiv(0) on SPARC g_b, from reported g_dag(z)):')
def ratio(gz, g0): return fit_a(ALLB, mcg(ALLB, gz)) / fit_a(ALLB, mcg(ALLB, g0))
for lab, A_, B_ in (('ZOMG centrals', -.84, 2.23), ('ZOMG satellites', -.72, 2.11)):
    g0 = (A_ + B_) * 1e-10; out = []
    for z in ZB:
        a = 1 / (1 + z); r = ratio((A_ * a + B_) * 1e-10, g0); out.append((z, r, ZB[z][0] <= r <= ZB[z][1], a < .33))
    print(f' {lab} g_dag(a) = ({A_}a + {B_})e-10, valid 0.33<=a<=1: ' + ', '.join(f'z {z}: {r:.3f} [{"PASS" if p else "FAIL"}{" extrap" if ex else ""}]' for z, r, p, ex in out))
for zr in (2.0, 2.3, 2.8):   # Magneticum: factor ~3 relative to z 0.1; paper inconsistent on which z
    n = np.log(3.) / np.log((1 + zr) / 1.1); out = []
    for z in ZB:
        gz = 1.14e-10 * ((1 + z) / 1.1)**n; g0 = 1.14e-10 * (1 / 1.1)**n; r = ratio(gz, g0); out.append((z, r, ZB[z][0] <= r <= ZB[z][1]))
    print(f' Magneticum ESTIMATE, x3 at z {zr} vs z 0.1, power law in (1+z), n {n:.2f}: ' + ', '.join(f'z {z}: {r:.3f} [{"PASS" if p else "FAIL"}]' for z, r, p in out))
print(' MUGS2: "significant redshift dependence", g_dag higher in the past (qualitative): NOT TESTABLE numerically, direction leans FAIL.')
print(' EAGLE: progenitor relations "very similar" at four higher z, slight systematic residual (qualitative): NOT TESTABLE numerically, leans flat.')
print(' MBII, NIHAO, FIRE-2: z~0 only: NOT TESTABLE.')

print('\nG4 one constant across hosts (rms of log a0_equiv <= 0.1 dex):')
sub = [(n, v) for n, v in (('full', 2.01), ('bright', 3.05), ('faint', 1.151), ('centrals Mh>1e12/h', 3.491))]
la = np.log10([fit_a(ALLB, mcg(ALLB, v * 1e-10)) for _, v in sub])
print(' MBII subsamples (luminosity / central split, not host-mass bins): ' + ', '.join(f'{n} {v}' for n, v in sub) + f'; rms over bright/faint/centrals {la[1:].std():.3f} dex, range {la.max() - la.min():.3f} dex [FAIL, PARTIAL proxy]')
lz = np.log10([fit_a(ALLB, mcg(ALLB, v * 1e-10)) for v in (1.40, 1.48)])
print(f' ZOMG centrals 1.40 vs satellites 1.48: diff {abs(lz[1] - lz[0]):.3f} dex (environment split, not host mass; PARTIAL proxy, within 0.1)')
print(' EAGLE (feedback variants move galaxies ALONG the relation), NIHAO (scatter by M*, no g_dag per bin), MUGS2, Magneticum, FIRE-2: NOT TESTABLE.')
print(' Reported intrinsic RAR scatter (not G4): MUGS2 0.06, EAGLE 0.08, NIHAO 0.079 (0.04 at M* 1e9.3-1e11, 0.11 below), ZOMG centrals 0.048, satellites 0.192, MBII ~0.1 full.')
print('\nG5 operative: halo + baryon gravity in every simulation: PASS by definition. Grudic20 scale built from G, m_p, sigma_T: carries no rho_DE, so G2 slope 0 if it were the mechanism.')
print('\nRival language. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
