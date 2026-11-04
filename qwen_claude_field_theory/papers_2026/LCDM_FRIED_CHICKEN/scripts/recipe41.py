"""A40: (a) correlated halo scatter (assembly bias) + M/L trend; (b) microphysical feedback constants and a particle-constant lattice,
per ../FROZEN_A40.md. Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, itertools, time
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from fractions import Fraction as Fr
from scipy.stats import poisson
T0 = time.time()
c_ = 2.998e8; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); AT = .5 * AC
ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}; ZS = [0.] + list(ZB)
# rho_DE(z)/rho_DE0 at z 1, 1.5, 2.33, hard-coded from recipe31.out l.8-71 (A29, footing P)
RHO = {'B0': (1., 1., 1.), 'B1': (1.0175, .8743, .6680), 'B1p': (.9779, .8668, .7037), 'B1u': (1.0628, .8879, .6415), 'B2': (1.1618, 1.1972, 1.2336),
       'B3': (1.3590, 1.5993, 2.0317), 'B4': (.9665, 1.0098, 1.0964), 'B5': (1., 1.0001, 1.0002)}
CK = os.path.join(HERE, 'recipe41.json')
OUT = json.load(open(CK)) if os.path.exists(CK) else {}
def ck(k, v): OUT[k] = v; json.dump(OUT, open(CK, 'w'), indent=1, default=float)
print(f'A40 recipe41; c sqrt(G rho_DE) {AC:.4e}, a_T {AT:.4e}, A0 {A0:.4e}', flush=True)

# ======================= (a) =======================
CGZ = {z: (CG if z == 0 else np.array([float(CM.concentration(10**m * cos.h, '200c', z, model='diemer19')) for m in LM])) for z in ZS}
def cz(M, z): return np.interp(np.log10(M), LM, CGZ[z])
TB = {}
for l in open(os.path.join(D, 'SPARC_Lelli2016c.mrt')):
    p_ = l.split()
    if len(p_) >= 17 and p_[1].isdigit() and len(l) > 90:
        try: TB[p_[0]] = dict(D=float(p_[2]), eD=float(p_[3]), i=float(p_[5]), ei=float(p_[6]), MHI=float(p_[13]))
        except (ValueError, IndexError): pass
for g in GS:
    a = np.loadtxt(os.path.join(D, 'sparc_data', g.n + '_rotmod.dat')); a = a[a[:, 0] > 0]
    vb2 = a[:, 3] * abs(a[:, 3]) + YD * a[:, 4] * abs(a[:, 4]) + YB * a[:, 5] * abs(a[:, 5]); a = a[vb2 > 0]
    g.vg2 = a[:, 3] * abs(a[:, 3]) * 1e6; g.vs2 = (YD * a[:, 4] * abs(a[:, 4]) + YB * a[:, 5] * abs(a[:, 5])) * 1e6; g.ev = a[:, 2] * 1e3; g.vo = a[:, 1] * 1e3
    g.t = TB[g.n]; assert np.allclose(g.vg2 + g.vs2, g.vb2)
lS = np.log10(np.array([g.Mb / (2 * np.pi * (g.Rd / kpc * 1e3)**2) for g in GS])); lMb = np.log10([g.Mb for g in GS])
rs_ = lS - np.polyval(np.polyfit(lMb, lS, 1), lMb); SRES = rs_ / rs_.std()
print(f'(a) surface-density residual: rms {rs_.std():.3f} dex about log Sigma_b(log M_b) line; standardised')
def gbu(g, u): return np.maximum(g.vg2 + 10**u * g.vs2, 1e-3 * g.vb2) / g.r
def observer(gobs):
    lo = [np.log10(x) for x in gobs]; u = np.zeros(len(GS)); la = np.log10(A0)
    for _ in range(6):
        for j, g in enumerate(GS):
            u[j] = minimize_scalar(lambda x: (((lo[j] - np.log10(law(gbu(g, x), 10**la))) / .1)**2).sum() + (x / .1)**2, bounds=(-.3, .3), method='bounded').x
        gbs = [gbu(g, x) for g, x in zip(GS, u)]
        la = minimize_scalar(lambda x: sum(((l - np.log10(law(b, 10**x)))**2).sum() for l, b in zip(lo, gbs)), bounds=(-11, -9), method='bounded').x
    res = np.concatenate([l - np.log10(law(b, 10**la)) for l, b in zip(lo, gbs)])
    return float(np.sqrt((res**2).mean())), float(10**la), res
def nfwz(r, M, c, z):
    rc = cos.rho_c(z) * cos.h**2 * Msun / kpc**3; R = (3 * M * Msun / (800 * np.pi * rc))**(1 / 3); return M * Msun * mu(r * c / R) / mu(c)
def halo(g, gb, M, c, fb, contract, z=0.):
    m0 = (1 - fb) * nfwz(g.r, M, c, z)
    if contract:
        mb = gb * g.r**2 / G; ri = g.r.copy()
        for _ in range(25):
            mi = nfwz(ri, M, c, z); ri = .5 * ri + .5 * g.r * (np.maximum(mb, 0) + (1 - fb) * mi) / mi
        m0 = np.maximum((1 - fb) * nfwz(ri, M, c, z), 1e-3 * m0)
    return gb + G * m0 / g.r**2
def trend(g, p): return p * np.log10(g.Ms / 1e10)
def mock(rcm, rcs, p, seed, contract=False, errors=True, noiseless=False, z=0.):
    rng = np.random.default_rng(seed); out, Ms_ = [], []
    for j, g in enumerate(GS):
        nu, x, e = rng.normal(0, 1, 3); ut = trend(g, p) + (0 if noiseless else .1 * nu)
        gbt = gbu(g, ut); Mst = g.Ms * 10**ut; Mbt = Mst + 1.33 * g.t['MHI'] * 1e9
        M = m200_of(Mst * 10**(0 if noiseless else .15 * x))
        dc = 0 if noiseless else .11 * (rcm * x + rcs * SRES[j] + np.sqrt(max(1 - rcm**2 - rcs**2, 0)) * e)
        c = cz(M, z) * 10**dc; gt = halo(g, gbt, M, c, min(Mbt / M, .5), contract, z); Ms_.append(M)
        if errors:
            vt = np.sqrt(gt * g.r); fD = max(1 + rng.normal(0, g.t['eD'] / g.t['D']), .3); io = np.clip(g.t['i'] + rng.normal(0, g.t['ei']), 15, 89)
            vo = np.maximum(vt * np.sin(np.radians(g.t['i'])) / np.sin(np.radians(io)) + rng.normal(0, 1, len(g.r)) * g.ev, 1e3)
            gt = vo**2 / (g.r * fD)
        out.append(gt)
    return out, np.array(Ms_)
def egates(cur, sel=None):
    sel = range(len(GS)) if sel is None else sel
    d_ = [np.log10(cur[j]) - np.log10(GS[j].gl) for j in sel]; d = np.concatenate(d_)
    gb = np.concatenate([GS[j].gb for j in sel]); per = np.array([np.sqrt((x**2).mean()) for x in d_])
    b = np.floor(np.log10(gb) * 2) / 2; bins = [d[b == x].mean() for x in np.unique(b) if (b == x).sum() >= 50]
    return float(np.sqrt((d**2).mean())), float(np.percentile(per, 95)), float(max(abs(v) for v in bins))
def own_a(cur):
    gt = np.concatenate(cur); a = fit_a(ALLB, gt); return a, float(np.sqrt(np.mean((np.log10(gt) - np.log10(law(ALLB, a)))**2)))
HP = np.concatenate([g.ev / g.vo <= .05 for g in GS])
if 'sparc' not in OUT:
    sS, aS, rS = observer([g.gobs for g in GS]); ck('sparc', dict(s=sS, a=aS, hp=float(np.sqrt((rS[HP]**2).mean()))))
SP = OUT['sparc']; print(f'(a) real SPARC observer fit: scatter all {SP["s"]:.4f}, good points ({HP.sum()} of {len(HP)}) {SP["hp"]:.4f}, a0 {SP["a"]:.3e} (A20: 0.1489, 0.0814, 8.034e-11)', flush=True)
SEEDS = (100, 101, 102)
def cell(rcm, rcs, p, contract=False):
    key = f'{rcm:+.2f}_{rcs:+.2f}_{p:+.2f}_{int(contract)}'
    if key in OUT: return OUT[key]
    obs = [observer(mock(rcm, rcs, p, s, contract)[0]) for s in SEEDS]
    intr = mock(rcm, rcs, p, SEEDS[0], contract, errors=False)[0]; e = egates(intr); ao, ro = own_a(intr)
    ev_, od_ = range(0, len(GS), 2), range(1, len(GS), 2)
    r = dict(s_all=float(np.mean([o[0] for o in obs])), s_hp=float(np.mean([np.sqrt((o[2][HP]**2).mean()) for o in obs])), s_hp_sd=float(np.std([np.sqrt((o[2][HP]**2).mean()) for o in obs])),
             a=float(np.mean([o[1] for o in obs])), E=e, a_own=float(ao), rms_own=ro, ev=egates(intr, ev_)[0], od=egates(intr, od_)[0])
    ck(key, r); return r
t1 = time.time(); _ = cell(0., 0., 0.); print(f'(a) one cell {time.time() - t1:.1f} s (0 if checkpointed)', flush=True)
RCM, RCS, PP = (0., -.3, -.6, -.9), (0., .3, .6), (-.2, -.1, 0., .1, .2)
def show(rcm, rcs, p, r, tag=''):
    b1 = abs(r['s_hp'] - SP['hp']) <= .02; b2 = abs(np.log10(r['a'] / A0)) <= .05; E = r['E']
    print(f' rho_cM {rcm:+.2f} rho_cS {rcs:+.2f} p {p:+.2f}{tag}: scatter all {r["s_all"]:.4f}, good {r["s_hp"]:.4f}+-{r["s_hp_sd"]:.4f} [{"PASS" if b1 else "FAIL"} B1]; '
          f'a0 {r["a"]:.3e} ({np.log10(r["a"] / A0):+.3f} dex) [{"PASS" if b2 else "FAIL"} B2]; intrinsic E1 {E[0]:.4f} E2 {E[1]:.4f} E3 {E[2]:.4f} '
          f'[{"PASS" if E[0] <= .02 and E[1] <= .04 and E[2] <= .02 else "FAIL"} E]; own-a {r["a_own"]:.3e}, rms at own a {r["rms_own"]:.4f}', flush=True)
print('\n(a) GRID, no contraction, 3 realisations per cell (B1 graded on good points vs SPARC ' + f'{SP["hp"]:.4f})')
grid = []
for rcm in RCM:
    for rcs in RCS:
        if rcm**2 + rcs**2 > 1: print(f' rho_cM {rcm:+.2f} rho_cS {rcs:+.2f}: skipped (rho^2 sum > 1)'); continue
        for p in PP:
            r = cell(rcm, rcs, p); show(rcm, rcs, p, r); grid.append((rcm, rcs, p, r))
b1p = [(a, b, c) for a, b, c, r in grid if abs(r['s_hp'] - SP['hp']) <= .02]; b2p = [(a, b, c) for a, b, c, r in grid if abs(np.log10(r['a'] / A0)) <= .05]
ep = [(a, b, c) for a, b, c, r in grid if r['E'][0] <= .02]
print(f' B1 passes: {len(b1p)} of {len(grid)} {b1p}\n B2 passes: {len(b2p)} {b2p}\n intrinsic E1 passes: {len(ep)} {ep}')
best = min(grid, key=lambda x: x[3]['E'][0]); hb = min(grid, key=lambda x: x[3]['ev'])
print(f' best intrinsic E1 cell: rho_cM {best[0]:+.2f} rho_cS {best[1]:+.2f} p {best[2]:+.2f} E1 {best[3]["E"][0]:.4f}')
print(f' holdout: chosen on GS[::2] -> rho_cM {hb[0]:+.2f} rho_cS {hb[1]:+.2f} p {hb[2]:+.2f} (even rms {hb[3]["ev"]:.4f}); unseen GS[1::2] rms {hb[3]["od"]:.4f} [{"PASS" if hb[3]["od"] <= .025 else "FAIL"}]')
bs = min(grid, key=lambda x: abs(x[3]['s_hp'] - SP['hp'])); print(f' closest good-points scatter: rho_cM {bs[0]:+.2f} rho_cS {bs[1]:+.2f} p {bs[2]:+.2f}: {bs[3]["s_hp"]:.4f} vs {SP["hp"]:.4f}')
pb = best[2]
print(f'\n(a) STRENGTH SEARCH, rho_cS 0, p {pb:+.2f}')
for rcm in (0., -.1, -.2, -.3, -.4, -.5, -.6, -.7, -.8, -.9, -.95, -.99): show(rcm, 0., pb, cell(rcm, 0., pb))
print(f' and rho_cM -0.6 with rho_cS up to sqrt(1 - 0.36) = 0.8, p {pb:+.2f}')
for rcs in (.2, .4, .6, .7, .8): show(-.6, rcs, pb, cell(-.6, rcs, pb))
print(f' and maximal compensation rho_cM -0.99 at each p (diagnostic of the floor)')
for p in PP: show(-.99, 0., p, cell(-.99, 0., p))
# best cell in detail
print('\n(a) best cell, printed lib.grade blocks')
bc = best[:3]
grade(f'(a) intrinsic mock seed 100 at rho_cM {bc[0]:+.2f} rho_cS {bc[1]:+.2f} p {bc[2]:+.2f}', mock(*bc, SEEDS[0], errors=False)[0])
nl, Mn = mock(0., 0., bc[2], 0, errors=False, noiseless=True)
grade(f'(a) noiseless mock, p {bc[2]:+.2f} (correlations cannot act)', nl)
grade('(a) noiseless mock, p 0 (A20 control: 0.1419)', mock(0., 0., 0., 0, errors=False, noiseless=True)[0])
rcon = cell(*bc, contract=True); show(*bc, rcon, ' CONTRACTED')
# tie gates on the best cell's noiseless mock
az = {z: fit_a(ALLB, np.concatenate(mock(0., 0., bc[2], 0, errors=False, noiseless=True, z=z)[0])) for z in ZS}
ke = az[0.] / AC; rz = {z: az[z] / az[0.] for z in ZB}
print(f'\n(a) tie gates, noiseless mock p {bc[2]:+.2f}: fitted a {az[0.]:.3e}, kappa_eff {ke:.3f} [{"PASS" if abs(np.log10(ke / .5)) <= .05 else "FAIL"} G1]; a(z)/a(0) '
      + ' '.join(f'{rz[z]:.3f}' for z in ZB) + f' [{"PASS" if all(ZB[z][0] <= rz[z] <= ZB[z][1] for z in ZB) else "FAIL"} G3]')
for bg, rr in RHO.items():
    dv = [np.log10(rz[z]) - .5 * np.log10(x) for z, x in zip(ZB, rr)]
    print(f'  GT {bg:4s} (LCDM a(z) ratio, approximation): dev ' + ' '.join(f'{x:+.3f}' for x in dv) + f' [{"PASS" if max(map(abs, dv)) <= .05 else "FAIL"} GT]')
ai = np.array([fit_a(g.gb, c) for g, c in zip(GS, nl)]); sel = (np.log10(Mn) >= 11) & (np.log10(Mn) <= 12.5)
g4 = np.log10(ai[sel]).std(); print(f'  G4: per-galaxy fitted a over log M200 11-12.5 ({sel.sum()} galaxies) rms {g4:.3f} dex [{"PASS" if g4 <= .1 else "FAIL"} G4]; median {np.median(ai[sel]):.3e}')
print(f'(a) parameters: 3 grid knobs (rho_cM, rho_cS, p) + 3 literature scatter amplitudes; observer 171 u + 1 a0 (applied to SPARC too). Runtime so far {time.time() - T0:.0f} s', flush=True)

# ======================= (b) =======================
print('\n(b) GRUDIC FEEDBACK SCALE')
hbar, mp, me, sT, alp = 1.054572e-34, 1.672622e-27, 9.109384e-31, 6.652459e-29, 1 / 137.035999
pc = kpc / 1e3
F1 = .1 * G * mp / sT; F2 = np.pi * G * 1000 * Msun / pc**2; eta = .1 * AT / F1
GT_const = {bg: [-.5 * np.log10(x) for x in rr] for bg, rr in RHO.items()}
for nm, a in (('F1 0.1 G m_p/sigma_T', F1), ('F2 pi G Sigma_crit (1000 Msun/pc^2)', F2), (f'F1-fit eta {eta:.4f} (1 knob)', AT)):
    print(f' {nm}: a {a:.4e}, kappa_eff {a / AC:.4f} ({np.log10(a / AT):+.3f} dex) [{"PASS" if abs(np.log10(a / AT)) <= .05 else "FAIL"} G1]; G2 slope 0 [FAIL G2]; a(z)/a(0) 1 1 1 [PASS G3, trivial]; G4 mass-free [PASS, trivial]; G5 BY POSIT')
    grade(f'(b) law swap a = {nm}', [law(g.gb, a) for g in GS], '(0 knobs tuned per galaxy)')
    un = np.sqrt(np.mean(np.concatenate([(np.log10(law(GS[j].gb, a)) - np.log10(GS[j].gl))**2 for j in range(1, len(GS), 2)]))); print(f' holdout unseen GS[1::2] rms {un:.4f} [{"PASS" if un <= .025 else "FAIL"}]')
for bg, dv in GT_const.items(): print(f'  GT {bg:4s} (any constant): dev ' + ' '.join(f'{x:+.3f}' for x in dv) + f' [{"PASS" if max(map(abs, dv)) <= .05 else "FAIL"} GT]')

NAMES = ['hbar', 'm_p', 'm_e', 'sigma_T', 'alpha', 'rho_L']
VAL = np.log(np.array([hbar, mp, me, sT, alp, RDE])); DIMS = np.array([(2, -1, 1), (0, 0, 1), (0, 0, 1), (2, 0, 0), (0, 0, 0), (-3, 0, 1)], float)
EXPS = [-2, -1.5, -1, -.5, .5, 1, 1.5, 2]
PREF = {'1': 1., '2': 2., '1/2': .5, 'pi': np.pi, '2pi': 2 * np.pi, '1/2pi': 1 / (2 * np.pi), '4pi': 4 * np.pi, '1/4pi': 1 / (4 * np.pi), '6': 6., '1/6': 1 / 6, 'sqrt3': 3**.5, '1/sqrt3': 3**-.5}
P2 = {}
for (a1, x1), (b1, y1) in itertools.combinations_with_replacement(PREF.items(), 2):
    v_ = round(x1 * y1, 12)
    if v_ not in P2.values(): P2[f'{a1}*{b1}'] = v_
LRAT = {bg: np.log10(np.array(rr)) for bg, rr in RHO.items()}
def lattice(nI, prefs, tag, show_):
    RS, RE = [], []
    for k in (1, 2, 3):
        for S in itertools.combinations(range(nI), k):
            for E in itertools.product(EXPS, repeat=k): RS.append(S + (-1,) * (3 - k)); RE.append(E + (0.,) * (3 - k))
    RS, RE = np.array(RS), np.array(RE); EM = np.zeros((len(RS), nI))
    for j in range(3):
        m = RS[:, j] >= 0; EM[np.where(m)[0], RS[m, j]] = RE[m, j]
    Dm = EM @ DIMS[:nI]; ok = np.abs(Dm.sum(1) + 1) < 1e-9; nall = len(RS)
    EM, RS, RE, Dm = EM[ok], RS[ok], RE[ok], Dm[ok]; q = Dm[:, 2]; p = 1 - 3 * q - Dm[:, 0]
    assert np.allclose(-p - 2 * q + Dm[:, 1], -2)
    base = (p * np.log(c_) + q * np.log(G) + EM @ VAL[:nI]) / np.log(10)
    vals = base[:, None] + np.log10(np.array(list(prefs.values())))[None, :] - np.log10(AT)
    eL = EM[:, 5] if nI == 6 else np.zeros(len(EM))
    g2 = np.abs(eL - .5) <= .05
    gt = np.all([np.all(np.abs((eL[:, None] - .5) * LRAT[bg][None, :]) <= .05, 1) for bg in RHO], 0)
    fullr = g2 & gt  # G3 = 1 and G4 mass-free for every expression here (constants and Lambda)
    g1 = np.abs(vals) <= .05; full = g1 & fullr[:, None]
    print(f'\n==== {tag}: {nI} ingredients, {nall} products, {ok.sum()} dimensionally valid, {len(prefs)} prefactors; N_expr {vals.size}; '
          f'log10(a/a_T) {vals.min():+.1f} to {vals.max():+.1f}; within 1.5 dex {(np.abs(vals) <= 1.5).sum()}')
    print(f' products passing G2 {g2.sum()}, GT(all backgrounds) {gt.sum()}, G2+GT {fullr.sum()}; G3, G4 pass for all (constant, mass-free)')
    ds = np.round(np.arange(-1.5, 1.5001, .01), 2); ds = ds[np.abs(ds) >= .1]
    cnt_in = lambda a, d: np.searchsorted(a, d + .05, 'right') - np.searchsorted(a, d - .05, 'left')
    res = {}
    for nm, arr in (('G1', vals.ravel()), ('full', vals[fullr].ravel())):
        for kind, a in (('distinct 1e-4', np.unique(np.round(arr, 4))), ('distinct 1e-7', np.unique(np.round(arr, 7))), ('expressions', np.sort(arr))):
            K = cnt_in(a, 0.); cnt = np.array([cnt_in(a, d) for d in ds]); m_ = cnt.mean()
            pp = poisson.sf(K - 1, m_) if m_ > 0 else (0. if K else 1.)
            rd = 'WITHIN CHANCE (numerology)' if (K <= np.percentile(cnt, 84) or (m_ > 0 and pp > .01)) else 'BEYOND CHANCE'
            if K == 0 and m_ == 0: rd = 'none, none expected'
            print(f' {nm:4s} [{kind:13s}] observed {K}; slid chance mean {m_:.1f}, 16-84% {np.percentile(cnt, 16):.0f}-{np.percentile(cnt, 84):.0f}, max {cnt.max()}; '
                  f'Poisson P(N>={K}) {pp:.3g}; offsets with >= observed {np.mean(cnt >= K):.3f} -> {rd}')
            res[(nm, kind)] = K
    if show_:
        pk = list(prefs.keys())
        def lab(i, j):
            t = [f'{NAMES[RS[i, k]]}^{Fr(RE[i, k]).limit_denominator(2)}' for k in range(3) if RS[i, k] >= 0]
            return f'{pk[j]} c^{Fr(p[i]).limit_denominator(4)} G^{Fr(q[i]).limit_denominator(4)} ' + ' '.join(t)
        gi = np.argwhere(g1); print(f' G1 hits (expressions) {len(gi)}; closest 12:')
        for i, j in sorted(gi.tolist(), key=lambda x: abs(vals[x[0], x[1]]))[:12]: print(f'   {lab(i, j):60s} {vals[i, j]:+.4f} dex, kappa_eff {.5 * 10**vals[i, j]:.4f}')
        gm = np.where((RS[:, 0] == 1) & (RS[:, 1] == 3) & (RS[:, 2] < 0) & (RE[:, 0] == 1) & (RE[:, 1] == -1))[0]
        if len(gm): print(f' check: G m_p/sigma_T in lattice: {10**(base[gm[0]] - np.log10(AT)):.4f} a_T (0.1 x that = F1 {F1 / AT:.4f} a_T)')
        fi = np.argwhere(full)
        if len(fi):
            g5 = 8 * np.pi * G * RDE / 3 * 10 * kpc
            print(f' full survivors {len(fi)}; all contain rho_L^1/2 (G2); G5: rho_L pull at 10 kpc {g5 / AT:.2e} a_T [FAIL G5]; closest 12:')
            for i, j in sorted(fi.tolist(), key=lambda x: abs(vals[x[0], x[1]]))[:12]: print(f'   {lab(i, j):60s} {vals[i, j]:+.4f} dex')
    return res
lattice(5, PREF, 'PURE particle lattice, PRIMARY single prefactor', True)
lattice(5, P2, 'PURE particle lattice, SENSITIVITY two-element prefactors', False)
lattice(6, PREF, 'HYBRID lattice (+ rho_L), PRIMARY single prefactor', True)
lattice(6, P2, 'HYBRID lattice (+ rho_L), SENSITIVITY two-element prefactors', False)
print(f'\nruntime {time.time() - T0:.0f} s')
print('Rival language. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
