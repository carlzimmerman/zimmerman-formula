"""X1_seedfree_abundance lane script: frozen checks K1-K14 (FROZEN_CRITERIA §3 + A1-A3) and physics legs G1-G4 (§4).

Reads the committed artifacts of the lane (validation/, lattice/, handover/, abundance/, x1_stochastic_*.json,
x1_dmc_results.json) and recomputes the cheap checks (K8 resume, K10 Boltzmann equilibrium, K12 network limits,
K13 free X). Prints one line per check, ends 'X1_SEEDFREE_ABUNDANCE COMPLETE: N/M checks PASS.', exit 0 iff all pass.
--mutate: the TW occupation estimator omits the symmetric-ordering -1/2 (K5 must FAIL); outputs *_MUTATE.*
Run: OMP_NUM_THREADS=1 nice -n 15 python3 x1_seedfree_abundance.py [--mutate]
"""
import json, subprocess, sys, os
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
MUT = '--mutate' in sys.argv
OUT = []; RES = dict(checks={}, legs={})
m = .001; M = 2*m*np.sqrt(1+.02**2)


def say(s): OUT.append(s); print(s, flush=True)


def check(k, ok, val, thr):
    RES['checks'][k] = dict(pass_=bool(ok), value=val, threshold=thr)
    say(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}")


def J(p): return json.loads((HERE/p).read_text())


# ---------------- K1 R0 ----------------
st = J('x1_stochastic_kmin0.08_Ne60.json')['R0']
check('K1', st['d_phi'] < 1e-6 and st['d_X'] < 1e-6 and st['samples_bitwise_identical'],
      f"dphi={st['d_phi']:.1e} dX={st['d_X']:.1e} bitwise={st['samples_bitwise_identical']}", '<1e-6')
# ---------------- K2 V0 ----------------
v0 = J('validation/v0.json')
check('K2', v0['pass_'], f"maxdiff={max(v0['max_abs_diff'].values()):.1e} states={v0['states']}", '<1e-12')
# ---------------- K3 exact solvers ----------------
from x1_valsummary import table, errors, nstar
worst_n = 0.; worst_e = 0.
for f in sorted((HERE/'validation').glob('v3_*.json')):
    d = J(f'validation/{f.name}')
    if d.get('skipped') or 'free' in f.name: continue
    worst_n = max(worst_n, float(np.ptp(d['exact']['norm'])))
    worst_e = max(worst_e, float(np.ptp(d['exact']['energy'])/abs(d['exact']['energy'][0])))
v1e = max(J(f'validation/v1b_n{n}.json')['energy_drift'] for n in (1, 2))
v1n = max(abs(J('validation/v1a.json')['exact'][-1]['norm']-1), *[abs(J(f'validation/v1b_n{n}.json')['exact'][-1]['norm']-1) for n in (1, 2)])
check('K3', max(worst_n, v1n) < 1e-8 and max(worst_e, v1e) < 1e-6,
      f"V3 norm {worst_n:.1e} energy {worst_e:.1e}; V1 norm {v1n:.1e} energy {v1e:.1e}", 'norm<1e-8 energy<1e-6')
# ---------------- K4 TW approaches exact ----------------
rows = table('rwa'); k4 = []
for sc in 'AB':
    for nu in (2, 8):
        rr = {r['n']: r for r in rows if r['sc'] == sc and r['nu'] == nu and 'O1' in r}
        nmax = max(rr); mx = lambda r: max(r[k] for k in ('O1', 'O2', 'O3', 'O4', 'O5', 'O6'))
        k4.append((sc, nu, nmax, mx(rr[1]), mx(rr[nmax]), mx(rr[nmax]) < mx(rr[1])))
check('K4', all(x[-1] for x in k4), '; '.join(f"{a}nu{b}: n={c} {e:.3f} vs n=1 {d:.3f}" for a, b, c, d, e, _ in k4),
      'max err at largest n < at n=1')
# ---------------- K5 free limit ----------------
k5 = []
for sc in 'AB':
    d = J(f"validation/v3_{sc}_nu8_n4_full_free{'_MUTATE' if MUT else ''}.json")
    drv = (2, 3) if sc == 'A' else (0, 1)
    te = np.array(d['tw']['N'])[:, drv].sum(1); ee = np.array(d['exact']['N'])[:, drv].sum(1)
    z = np.max(np.abs(te-ee)/np.maximum(np.array(d['tw_sem_Ndriven']), 1e-12)); k5.append(float(z))
check('K5', max(k5) < 4, f"max |TW-exact|/SEM = {max(k5):.2f}", '<4')
# ---------------- K6/K7 lattice ----------------
lat = {}
for f in sorted((HERE/'lattice').glob('P*.json')):
    lat[f.stem] = J(f'lattice/{f.name}')
k6 = {k: v['energy_residual'] for k, v in lat.items()}
check('K6', all(v < 1e-4 for v in k6.values()), ' '.join(f"{k}:{v:.1e}" for k, v in k6.items()), '<1e-4')
k7 = {k: v['charge_drift']/max(v['charge_scale'], 1e-300) for k, v in lat.items()}
check('K7', all(v < 1e-10 for v in k7.values()), f"max {max(k7.values()):.1e}", '<1e-10')
# ---------------- K8 resume (rerun here at 32^3, tau 600) ----------------
rd = HERE/'lattice_resume_check'; rd.mkdir(exist_ok=True)
env = dict(os.environ, OMP_NUM_THREADS='1')
base = [sys.executable, str(HERE/'x1_lattice.py'), '--N', '32', '--tau-end', '600', '--outdir', 'lattice_resume_check']
codes = []
for job, extra in (('U', []), ('I', ['--stop-after-steps', '1777']), ('I', ['--resume', '--stop-after-steps', '1500']),
                   ('I', ['--resume']), ('I', ['--resume'])):
    if job == 'U' and (rd/'U.json').exists(): codes.append(0); continue
    codes.append(subprocess.run(base+['--job', job]+extra, env=env, capture_output=True).returncode)
u = J('lattice_resume_check/U.json'); i = J('lattice_resume_check/I.json')
rel = max(float(np.max(np.abs(np.array(a['nbar'])-np.array(b['nbar']))/np.maximum(np.abs(np.array(a['nbar'])), 1e-300)))
          for a, b in zip(u['rows'], i['rows']))
check('K8', u['final_state_sha256'] == i['final_state_sha256'] and codes[1:] == [75, 75, 0, 0] and rel < 1e-12,
      f"sha_equal={u['final_state_sha256'] == i['final_state_sha256']} exits={codes[1:]} diag_rel={rel:.1e}",
      'byte-identical state; 75,75,0,0; diag<1e-12')
# ---------------- K9 time step ----------------
a = lat['P32_TW_p50_s1']['rows']; b = lat['P32_TW_p50_s1_dt2']['rows']
ta = np.array([r['tau'] for r in a]); tb = np.array([r['tau'] for r in b])
fa = a[int(np.argmin(abs(ta-500)))]['f0_phi']; fb = b[int(np.argmin(abs(tb-500)))]['f0_phi']
wa = np.mean([r['f0_phi'] for r in a if 400 < r['tau'] <= 500]); wb = np.mean([r['f0_phi'] for r in b if 400 < r['tau'] <= 500])
check('K9', abs(fa-fb) < .02, f"f0(500) {fa:.4f} vs {fb:.4f} (window means {wa:.4f}/{wb:.4f})", '<0.02')
# ---------------- K10 Boltzmann ----------------
from x1_boltzmann import Boltz
B = Boltz(pmax=8., Np=96); p = B.p; m2 = 0.
for _ in range(50):
    f = 1/np.expm1(np.sqrt(p*p+m2)); m2 = B.hartree(f)
f = 1/np.expm1(np.sqrt(p*p+m2)); C, _ = B.collision(f, m2)
fn = f*(1+.3*np.exp(-(p-2)**2)); Cn, _ = B.collision(fn, B.hartree(fn)); eqr = float(np.max(np.abs(C))/np.max(np.abs(Cn)))
ho = J('handover/P64_TW_p50_s1_nstar10.json'); tr = ho['E2']['trajectory']
dn = abs(tr[-1]['n']/tr[0]['n']-1); dr = abs(tr[-1]['rho']/tr[0]['rho']-1)
check('K10', eqr < 1e-6 and dn < 1e-6 and dr < 1e-6, f"eq {eqr:.1e} number {dn:.1e} energy {dr:.1e} "
      f"(max projection/collision {ho['E2']['info']['max_projection']:.1f})", '<1e-6')
# ---------------- K11 overlap ----------------
ov = ho['overlap_K11']
check('K11', ov['L1_boltzmann_vs_tw'] < .15, f"L1 {ov['L1_boltzmann_vs_tw']:.3f} (no-evolution {ov['L1_no_evolution']:.3f}; "
      f"f0 window {ov['f0_window_at_tau_a']:.2f}->{ov['f0_window_at_tau_b']:.2f})", '<0.15')
# ---------------- K12 network limits ----------------
import x1_relic as R, x1_abundance as A
amps = A.patch_amps(); E = A.lattice_E(); H = A.H_PRIMARY
vis, fx, rhoPhi = A.onset(H, None, amps['p50']['X'], E['p50'], amps['p50']['Phi'])
R.RATE_SCALE[0] = 0.; r0 = R.run_plasma(vis, fx['a_on'], fx['rho_on']+rhoPhi)
W0 = r0['hist'][0]['W']; cons0 = abs(r0['W']/W0-1)
R.RATE_SCALE[0] = 1e3; r3 = R.run_plasma(vis, fx['a_on'], fx['rho_on']+rhoPhi); R.RATE_SCALE[0] = 1.
dev = 0.
for h in r3['hist']:
    if h['T'] >= m/30:
        te = R.eq_state(h['T']); weq = (te['nP']+2*te['nX'])*np.exp(3*h['x'])
        dev = max(dev, abs(h['W']/weq-1))
dev_fast = 0.
for h in r3['hist']:
    if h['T'] >= m/30 and h['G4H'] > 10:
        te = R.eq_state(h['T']); dev_fast = max(dev_fast, abs(h['W']/((te['nP']+2*te['nX'])*np.exp(3*h['x']))-1))
check('K12', dev < .01 and cons0 < 1e-8, f"x1e3 max|W/Weq-1| (T>=m/30) {dev:.2e} [diagnostic, only where scaled "
      f"r4/H>10: {dev_fast:.2e}]; x0 |dW/W| {cons0:.1e}", '<1% and <1e-8')
# ---------------- K13 free X ----------------
fx1 = R.free_X(R.Vis(H), H); ex = R.free_X_exact_rd(H, H)
check('K13', abs(fx1['Na3']/ex-1) < 1e-4, f"{abs(fx1['Na3']/ex-1):.1e}", '<1e-4')
# ---------------- K14 conformal control ----------------
ct = J('abundance/ctrl_H1.3445177278709404e10_Tinst.json')
check('K14', abs(ct['ratio_half_to_full']-1) < .01, f"half-line/full-line {ct['ratio_half_to_full']:.4f}", '|r-1|<0.01')

# ================= physics legs =================
TARGET = .12
def ab(tag):
    f = HERE/'abundance'/f'{tag}.json'
    return J(f'abundance/{tag}.json') if f.exists() else None
prim = ab('primary_p50')
legs = RES['legs']
legs['primary'] = {c: dict(Y=v['Y'], Omega=v['Omega']) for c, v in prim['res'].items()}
legs['primary']['free_condensate_Omega'] = prim['Omega_free_condensate']
legs['primary']['K_absorption_Gamma_over_H'] = prim['res']['K']['extra'].get('W_absorption_Gamma_over_H_onset')
sens = {}
for t in ('sens_pb', 'sens_crossed', 'sens_powerlaw', 'sens_relcut', 'patch_p10', 'patch_p90', 'patch_xq10', 'patch_xq90'):
    d = ab(t)
    if d: sens[t] = {c: v['Omega'] for c, v in d['res'].items()}
legs['sensitivities'] = sens
iso = ab('iso_primary')
if iso:
    legs['G2_isocurvature_primary'] = iso['iso']
gmap = []
for line in (HERE/'abundance/jobs.txt').read_text().splitlines():
    if not line.startswith('point') or '--tag map_' not in line: continue
    d = ab(line.split('--tag ')[1])
    if not d: continue
    oL, oK, oC = (d['res'][c]['Omega'] for c in 'LKC')
    g1 = 'BELOW' if oC < TARGET else ('ABOVE' if oL > TARGET else 'BRACKETS')
    ctl = ab(line.split('--tag ')[1].replace('map_', 'ctrl_'))
    im = ab(line.split('--tag ')[1].replace('map_', 'isomap_'))
    gmap.append(dict(Hinf=d['Hinf'], Trh=d['Trh'], OmegaL=oL, OmegaK=oK, OmegaC=oC, G1=g1,
                     K_status=d['res']['K']['extra'].get('W_status', 'ok'),
                     K_Gamma_over_H=d['res']['K']['extra'].get('W_absorption_Gamma_over_H_onset'),
                     Omega_xi16=(ctl['Omega'] if ctl else None),
                     G2={c: dict(P_S=v['P_S'], pass_=v['pass_']) for c, v in im['iso'].items()} if im else None))
legs['G1_map'] = gmap
# G3 coherence / non-Gaussianity through bath formation (E1 prototypes)
g3 = {}
for k, v in lat.items():
    rr = v['rows']; t = np.array([r['tau'] for r in rr])
    def wmean(key, t0, t1, f=lambda r, key: r[key]):
        sel = [f(r, key) for r in rr if t0 < r['tau'] <= t1]; return float(np.mean(sel)) if sel else None
    exk = lambda r, key: r[key][2]/r[key][0]**2
    if abs(rr[-1]['Ephi_phys']) < 1e-3:      # XI16: vacuum-only state, no condensate; coherent fractions undefined
        g3[k] = dict(note='conformal vacuum state, no condensate; TW outside its window (all n < 1)',
                     frac_low_n1_end=rr[-1]['frac_low'][0], Ephi=rr[-1]['Ephi_phys']); continue
    g3[k] = dict(f0_phi_window={str(T): wmean('f0_phi', T-100, T) for T in (100, 500, 1000, 2000)},
                 f0_X_end=rr[-1]['f0_x'], g4_window_end=wmean('g4', 1900, 2000),
                 exkurt_re_window_end=wmean('cum_re', 1900, 2000, exk),
                 frac_low_n10_end=float(np.interp(np.log(10), np.log([1, 2, 3, 5, 10, 20, 50, 100]), rr[-1]['frac_low'])),
                 frac_low_n16_end=float(np.interp(np.log(16), np.log([1, 2, 3, 5, 10, 20, 50, 100]), rr[-1]['frac_low'])),
                 mH2_end=rr[-1]['mH2'], Ephi=rr[-1]['Ephi_phys'])
legs['G3_E1'] = g3
vr = table('rwa'); legs['G4_validation'] = dict(rows_rwa=vr, rows_full=table('full'), nstar_frozen=nstar(vr)[0],
                                                nstar_10=nstar(vr, .10, .20)[0])
occ_only = None
for n in (1, 2, 4, 8, 16, 32):
    rs = [r for r in vr if r['n'] == n and 'O1' in r]
    if len(rs) == 4 and all(max(r['O1'], r['O2'], r['O3'], r['O4']) < .05 for r in rs):
        occ_only = n; break
legs['G4_validation']['nstar_occupation_only_diagnostic'] = occ_only
legs['E2'] = dict(conditional=ho['E2']['conditional'], r_at_on_kinetic=ho['E2']['final']['r_at_on'],
                  r_at_on_mu0=ho['endpoints']['mu0']['r_at_on'], mH2_on_kinetic=ho['E2']['final']['mH2'],
                  overpopulation=ho['endpoints']['number_conserving']['n_over_n_mu0'])
# final word (frozen §4): SCOPED NO-GO iff every xi = 0 point fails G2 (every closure evaluated there) and every
# xi = 1/6 point is BELOW; a missing evaluation counts as not established
g2_all = [g['G2'] for g in gmap]
g2_complete = all(x is not None and set(x) == {'L', 'K', 'C'} for x in g2_all)
xi0_fail_computed = all(x is not None and all(not v['pass_'] for v in x.values()) for x in g2_all) and \
    (all(not v['pass_'] for v in iso['iso'].values()) if iso else False)
xi16_below = all(g['Omega_xi16'] is not None and g['Omega_xi16'] == g['Omega_xi16'] and g['Omega_xi16'] < TARGET for g in gmap)
word = 'SCOPED NO-GO' if (xi0_fail_computed and g2_complete and xi16_below) else 'UNDETERMINED'
legs['word_inputs'] = dict(g2_all_computed_fail=xi0_fail_computed, g2_complete_all_closures=g2_complete,
                           xi16_all_below=xi16_below, map_points=len(gmap))
legs['final_word'] = word
say(f"G1 primary Omega_L {legs['primary']['L']['Omega']:.3e} Omega_K {legs['primary']['K']['Omega']:.3e} "
    f"Omega_C {legs['primary']['C']['Omega']:.3e} -> {'BRACKETS' if legs['primary']['L']['Omega'] < TARGET < legs['primary']['C']['Omega'] else 'see map'}")
if iso:
    say('G2 isocurvature primary ' + ' '.join(f"{c}: P_S={v['P_S']:.2e} ({v['ratio_to_bound']:.1e} x bound) {'PASS' if v['pass_'] else 'FAIL'}"
                                            for c, v in iso['iso'].items()))
say(f"G4 n*(frozen) {legs['G4_validation']['nstar_frozen']} n*_10 {legs['G4_validation']['nstar_10']} "
    f"occupation-only {occ_only}")
say(f"FINAL WORD {word}")
npass = sum(v['pass_'] for v in RES['checks'].values()); ntot = len(RES['checks'])
say(f"X1_SEEDFREE_ABUNDANCE COMPLETE: {npass}/{ntot} checks PASS.")
suf = '_MUTATE' if MUT else ''
(HERE/f'x1_seedfree_abundance{suf}.out').write_text('\n'.join(OUT)+'\n')
(HERE/f'x1_seedfree_abundance_results{suf}.json').write_text(json.dumps(RES, indent=1, default=float))
sys.exit(0 if npass == ntot else 1)
