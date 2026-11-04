"""A26: tie gates G1-G5 on the full tuned R11b recipe (K11B frozen), cosmology and redshift rebuilds, and the least
added dependence, per ../FROZEN_A26.md. Rival language, adopts nothing, not a framework result.
kappa = 1/2 FITTED; not theory closed."""
import sys, os, json, time, itertools; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.special import gammainc
from scipy.optimize import minimize
from colossus.lss import mass_function as MF
s4 = open(os.path.join(HERE, 'recipe4.py'), encoding='utf-8').read(); exec(s4[s4.index('def m200k'):s4.index('def gal(')])
src = open(os.path.join(HERE, 'recipe18.py'), encoding='utf-8').read(); exec(src[src.index('K11B ='):src.index('def tune(')])
T0 = time.time(); CK = os.path.join(HERE, 'recipe28.json'); OUT = {}
def ck(k, v): OUT[k] = v; json.dump(OUT, open(CK, 'w'), indent=1, default=float)
c_ = 2.998e8; RDE0 = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE0); ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
FS = [.5, .71, 1., 1.41, 2.]; H0B, h0 = 67.4, .674; K = K11B; FAM = ['SHMR', 'FB', 'CORE', 'CONTR', 'CONC']; VARS = ['rhoDE', 'H']
BASE = cos
# ---------- environments ----------
def cgrid(C, z): return np.array([float(CM.concentration(10**m * C.h, '200c', z, model='diemer19')) for m in LM])
def rhoc(C, z): return C.rho_c(z) * C.h**2 * Msun / kpc**3
LMG = np.linspace(8, 16.5, 341)
def ncum(C, z=0.):
    d = MF.massFunction(10**LMG * C.h, z, mdef='200c', model='tinker08', q_out='dndlnM') * C.h**3
    seg = .5 * (d[1:] + d[:-1]) * np.diff(LMG) * np.log(10); return np.append(np.cumsum(seg[::-1])[::-1], 0.) + 1e-300
def mkcos(name, H0, Om0, Ob0, s8):
    return cc.setCosmology(name, dict(flat=True, H0=H0, Om0=Om0, Ob0=Ob0, sigma8=s8, ns=.965, relspecies=False))
cc.setCurrent(BASE); S30 = BASE.sigma(8., 30.); NB = ncum(BASE)
def env_cos(foot, f):
    if foot == 'C1':
        wm, wb, wd = .315 * h0**2, .0493 * h0**2, f * .685 * h0**2; h = np.sqrt(wm + wd)
        C = mkcos(f'a26_C1_{f}_t', 100 * h, wm / h**2, wb / h**2, .811); s8 = .811 * S30 / C.sigma(8. * h / h0, 30.)
        C = mkcos(f'a26_C1_{f}', 100 * h, wm / h**2, wb / h**2, s8)
    else:
        C = mkcos(f'a26_C2_{f}', H0B * np.sqrt(f), .315, .0493, .811); s8 = .811
    e = dict(rhoc=rhoc(C, 0.), cg=cgrid(C, 0.), n=ncum(C), h=C.h, s8=s8, Om0=C.Om0, rde=C.Ode0 * rhoc(C, 0.), z=0.)
    cc.setCurrent(BASE); return e
def env_z(z):
    cc.setCurrent(BASE); return dict(rhoc=rhoc(BASE, z), cg=cgrid(BASE, z), h=BASE.h, z=z, Hr=BASE.Hz(z) / H0B)
# ---------- SHMR ----------
def m200z(Ms, z, dnx=0.):
    dn, dm, db, dg = K[:4]; zt = z / (1 + z); x = 10**LMS / 10**(11.59 + dm + 1.195 * zt)
    s = 2 * (.0351 - .0247 * zt) * 10**(dn + dnx) * 10**LMS / (x**-(1.376 + db - .826 * zt) + x**(.608 + dg + .329 * zt)); i = np.argmax(s)
    return 10**np.interp(np.log10(Ms), np.log10(s[:i + 1]), LMS[:i + 1])
NCLIP = [0]
def amatch(M, en):
    lt = np.interp(np.log10(M), LMG, np.log10(NB)); ln = np.log10(en['n'])
    if lt > ln[0] or lt < ln[-2]: NCLIP[0] += 1
    return 10**np.interp(-lt, -ln, LMG)
# ---------- recipe ----------
def galx(g, M, en, md):
    dn, dm, db, dg, le, a1, a2, a4, le0, a3, f0, f1, dc, sc = K
    sb = g.Mb / (g.Rd / kpc)**2 / 1e6 / 100; c = np.interp(np.log10(M), LM, en['cg']) * 10**dc * (M / 1e12)**sc * md['CONC']
    fb = min(g.Mb / M, .5); fg = max((g.Mb - g.Ms) / g.Mb, .01)
    e = 10**le * (g.Ms / M / .01)**a1 * sb**a2 * (fg / .5)**a4 * md['FB']; n = np.tanh(min(e, 50)); eta = 10**le0 * (g.Ms / 1e9)**a3 * md['CORE']
    f = np.clip(np.clip(f0 + f1 * (np.log10(g.Mb) - 9.5), -1, 1) * md['CONTR'], -1, 1)
    R = (3 * M * Msun / (4 * np.pi * 200 * en['rhoc']))**(1 / 3); A = .16
    ein = lambda r: M * Msun * gammainc(3 / A, 2 / A * (r * c / R)**A) / gammainc(3 / A, 2 / A * c**A)
    m0 = np.maximum(ein(g.r), 1e-30); ri = g.r.copy()
    for _ in range(12):
        mi = np.maximum(ein(ri), 1e-30); ri = .5 * ri + .5 * g.r * (g.mb + (1 - fb) * mi) / mi
    m = np.maximum((1 - f) * m0 + f * mi, 1e-3 * m0) * (1 - fb) * np.tanh(g.r / (eta * 1.75 * g.Rd))**n
    return g.gb + G * m / g.r**2
def mods(spec, X):
    md = {k: 1. for k in FAM}; dnx = 0.
    for fam, (v, p) in spec.items():
        if fam == 'SHMR': dnx += p * np.log10(X[v])
        else: md[fam] = X[v]**p
    return md, dnx
def row(en, kind, spec, idx=None):
    """kind: 'A' fixed SHMR, 'B' abundance matched (cosmology), 'Bz' Moster z-terms, 'Az' SHMR at z=0."""
    X = dict(rhoDE=en.get('f', 1.), H=en.get('Hr', en['h'] / h0)); md, dnx = mods(spec, X); S = GS if idx is None else [GS[i] for i in idx]; cur = []
    for g in S:
        if kind in ('A', 'Az'): M = m200z(g.Ms, 0., dnx)
        elif kind == 'Bz': M = m200z(g.Ms, en['z'], dnx)
        else: M = amatch(m200z(g.Ms, 0., dnx), en)
        cur.append(galx(g, M, en, md))
    gb = np.concatenate([g.gb for g in S]); gt = np.concatenate(cur); a = fit_a(gb, gt)
    return a, np.sqrt(((np.log10(gt) - np.log10(law(gb, a)))**2).mean()), cur
# ---------- build environments ----------
ENV = {}
for foot in ('C1', 'C2'):
    for f in FS:
        e = env_cos(foot, f); e['f'] = f; ENV[(foot, f)] = e
EZ = {0.: env_z(0.)}; EZ[0.]['Hr'] = 1.
for z in ZB: EZ[z] = env_z(z)
print(f'A26 recipe28; base OL {cos.Ode0:.3f}, c sqrt(G rho_DE0) {AC:.4e}, A0 {A0:.4e}', flush=True)
for (foot, f), e in ENV.items(): print(f' env {foot} f {f}: h {e["h"]:.4f}, Om0 {e["Om0"]:.4f}, sigma8 {e["s8"]:.4f}, rho_DE/rho_DE0 {e["rde"] / RDE0:.4f}', flush=True)
# control: galx at base reproduces recipe18 gal3 at K11B
ctl = max(np.abs(np.log10(galx(g, m200k(g.Ms, *K[:4]), EZ[0.], {k: 1. for k in FAM})) - np.log10(gal3(g, K, []))).max() for g in GS)
cb = max(abs(np.log10(m200z(g.Ms, 0.) / m200k(g.Ms, *K[:4]))) for g in GS)
print(f'control: max |log galx - log gal3| {ctl:.2e} dex; max |log m200z(z=0) - log m200k| {cb:.2e}; C1 f=1 c-grid vs base max rel {np.abs(ENV[("C1", 1.)]["cg"] / CG - 1).max():.1e}', flush=True)
base_cur = [galx(g, m200k(g.Ms, *K[:4]), EZ[0.], {k: 1. for k in FAM}) for g in GS]
e1 = grade('R11b at K11B, base (control)', base_cur, '(14 knobs frozen)')
aB, SB, _ = row(EZ[0.], 'A', {}); ke = aB / AC; g1 = abs(np.log10(ke / .5)) <= .05
print(f'G1: a_fit {aB:.4e} ({aB / A0:.4f} A0), kappa_eff {ke:.4f} [{"PASS" if g1 else "FAIL"} G1] (by construction: tuned to the law at A0); shape S_base {SB:.4f} dex', flush=True)
ck('base', dict(E1=e1, a=aB, kappa_eff=ke, S=SB, control=ctl))
# ---------- (a) G2 ----------
def g2(foot, kind, spec, idx=None):
    a = []; S = []
    for f in FS:
        r = row(ENV[(foot, f)], kind, spec, idx); a.append(r[0]); S.append(r[1])
    s = np.polyfit(np.log(FS), np.log(a), 1)[0]; return s, a, S
print('\n(a) G2: slope d ln a / d ln rho_DE over f = 0.5, 0.71, 1, 1.41, 2', flush=True)
G2R = {}
for foot in ('C1', 'C2'):
    for kind in ('A', 'B'):
        NCLIP[0] = 0; s, a, S = g2(foot, kind, {}); ps = [np.log(a[i + 1] / a[i]) / np.log(FS[i + 1] / FS[i]) for i in range(4)]; ok = abs(s - .5) <= .05
        G2R[foot + kind] = dict(slope=s, a=a, S=S, ok=ok, clip=NCLIP[0])
        print(f' {foot}-{kind}: a/a_base ' + ' '.join(f'{x / a[2]:.4f}' for x in a) + f'; slope {s:+.4f} [{"PASS" if ok else "FAIL"} G2]; pairwise ' + ' '.join(f'{x:+.3f}' for x in ps)
              + f'; S max {max(S):.4f}' + (f'; AM clipped {NCLIP[0]}' if kind == 'B' else ''), flush=True)
ck('G2', G2R)
# ---------- (b) G3 ----------
print('\n(b) G3: a(z)/a(0), base cosmology, same SPARC baryons', flush=True)
G3R = {}
for kind in ('Bz', 'Az'):
    r = {z: row(EZ[z], kind, {}) for z in ZB}; rz = {z: r[z][0] / aB for z in ZB}; ok = all(ZB[z][0] <= rz[z] <= ZB[z][1] for z in ZB)
    G3R[kind] = dict(r={str(z): v for z, v in rz.items()}, ok=ok, S=[r[z][1] for z in ZB])
    print(f' {kind}: ' + ', '.join(f'z {z}: {rz[z]:.4f}' for z in ZB) + f' [{"PASS" if ok else "FAIL"} G3]; S ' + ' '.join(f'{r[z][1]:.4f}' for z in ZB) + f'; H(z)/H0 ' + ' '.join(f'{EZ[z]["Hr"]:.3f}' for z in ZB), flush=True)
ck('G3', G3R)
# ---------- G4 ----------
ai = np.array([fit_a(g.gb, c) for g, c in zip(GS, base_cur)]); lm = np.log10([m200k(g.Ms, *K[:4]) for g in GS]); sel = (lm >= 11) & (lm <= 12.5)
la = np.log10(ai); atb = int(((la < -11.99) | (la > -8.01)).sum())
g4 = la[sel].std() <= .1
print(f'\nG4: per-galaxy a_i on R11b curves: log M200 11-12.5 ({sel.sum()} galaxies) rms {la[sel].std():.4f} dex, median {np.median(ai[sel]) / A0:.3f} A0 [{"PASS" if g4 else "FAIL"} G4]; '
      f'all 171 rms {la.std():.4f} dex, median {np.median(ai) / A0:.3f} A0, p5-p95 {np.percentile(ai, 5) / A0:.3f}-{np.percentile(ai, 95) / A0:.3f} A0; a_i at fit bound {atb}', flush=True)
print('G5: halo gravity at the measured radii, operative by definition [PASS G5]')
ck('G4', dict(rms_sel=la[sel].std(), n_sel=int(sel.sum()), rms_all=la.std(), at_bound=atb))
# ---------- (c) reverse engineering ----------
def evals(spec, idx=None):
    s, a, S1 = g2('C1', 'A', spec, idx); a0 = a[2]; rz = {}; S2 = []
    for z in ZB:
        r = row(EZ[z], 'Bz', spec, idx); rz[z] = r[0] / a0; S2.append(r[1])
    J = ((s - .5) / .05)**2 + sum((np.log10(rz[z]) / .05)**2 for z in ZB)
    ok2 = abs(s - .5) <= .05; ok3 = all(ZB[z][0] <= rz[z] <= ZB[z][1] for z in ZB); okS = max(S1 + S2) <= SB + .005
    return dict(J=J, s=s, rz=rz, Smax=max(S1 + S2), ok=(ok2, ok3, okS))
def show(tag, spec, p, r):
    at = [k for k, v in zip(spec, p) if abs(abs(v) - 5) < 1e-3]
    print(f' {tag}: ' + ', '.join(f'{k}~{v[0]}^{q:+.3f}' for (k, v), q in zip(spec.items(), p)) + f' | slope {r["s"]:+.4f} [{"P" if r["ok"][0] else "F"}] a(z)/a(0) ' + ' '.join(f'{r["rz"][z]:.3f}' for z in ZB)
          + f' [{"P" if r["ok"][1] else "F"}] Smax {r["Smax"]:.4f} [{"P" if r["ok"][2] else "F"}] J {r["J"]:.2f}' + (f' AT BOUND {at}' if at else ''), flush=True)
OPTS = [(f, v) for f in FAM for v in VARS]
def fitspec(opts, x0=None):
    def J(p):
        if np.any(np.abs(p) > 5): return 1e9
        return evals({f: (v, q) for (f, v), q in zip(opts, p)})['J']
    if len(opts) == 1:
        r = minimize_scalar(lambda q: J(np.array([q])), bounds=(-5, 5), method='bounded', options=dict(xatol=1e-3)); p = np.array([r.x])
    else:
        x0 = np.zeros(len(opts)) if x0 is None else np.array(x0, float); sim = [x0] + [x0 + .5 * np.eye(len(opts))[i] for i in range(len(opts))]
        r = minimize(J, x0, method='Nelder-Mead', options=dict(maxfev=200, initial_simplex=sim, xatol=1e-3, fatol=1e-3)); p = np.clip(r.x, -5, 5)
    spec = {f: (v, q) for (f, v), q in zip(opts, p)}; return spec, p, evals(spec)
print('\n(c1) single exponent, one knob family x one variable (fit on C1-A cosmology rows + Bz redshift rows)', flush=True)
res = []
for o in OPTS:
    spec, p, r = fitspec([o]); show(f'{o[0]}-{o[1]}', spec, p, r); res.append(([o], p, r))
ck('c1', [dict(opts=o, p=list(p), J=r['J'], s=r['s'], ok=r['ok']) for o, p, r in res])
passing = [x for x in res if all(x[2]['ok'])]
if not passing:
    print(f'\n(c2) pairs from distinct families (time so far {time.time() - T0:.0f} s)', flush=True); pr = []
    for o1, o2 in itertools.combinations(OPTS, 2):
        if o1[0] == o2[0]: continue
        spec, p, r = fitspec([o1, o2]); show(f'{o1[0]}-{o1[1]} + {o2[0]}-{o2[1]}', spec, p, r); pr.append(([o1, o2], p, r))
    ck('c2', [dict(opts=o, p=list(p), J=r['J'], s=r['s'], ok=r['ok']) for o, p, r in pr]); res += pr
    passing = [x for x in pr if all(x[2]['ok'])]
    if not passing:
        print(f'\n(c3) triples: five best pairs + one more distinct family (time so far {time.time() - T0:.0f} s)', flush=True); tr = []
        for os_, p0, _ in sorted(pr, key=lambda x: x[2]['J'])[:5]:
            for o in OPTS:
                if o[0] in [q[0] for q in os_]: continue
                spec, p, r = fitspec(os_ + [o], list(p0) + [0.]); show(' + '.join(f'{a}-{b}' for a, b in os_ + [o]), spec, p, r); tr.append((os_ + [o], p, r))
        ck('c3', [dict(opts=o, p=list(p), J=r['J'], s=r['s'], ok=r['ok']) for o, p, r in tr]); res += tr
        passing = [x for x in tr if all(x[2]['ok'])]
if passing:
    n0 = min(len(x[0]) for x in passing); best = min([x for x in passing if len(x[0]) == n0], key=lambda x: x[2]['J']); opts, p, r = best
    spec = {f: (v, q) for (f, v), q in zip(opts, p)}
    print(f'\n(c) MINIMAL PASSING SOLUTION: {len(opts)} exponent(s): ' + ', '.join(f'{f} x ({v}/{v}0)^{q:+.3f}' for (f, v), q in zip(opts, p)), flush=True)
    for foot, kind in (('C1', 'B'), ('C2', 'A'), ('C2', 'B')):
        s, a, S = g2(foot, kind, spec); print(f'  untuned footing {foot}-{kind}: slope {s:+.4f} [{"PASS" if abs(s - .5) <= .05 else "FAIL"} G2], S max {max(S):.4f}', flush=True)
    rz = {z: row(EZ[z], 'Az', spec)[0] / aB for z in ZB}; print('  untuned Az: ' + ' '.join(f'{rz[z]:.3f}' for z in ZB) + f' [{"PASS" if all(ZB[z][0] <= rz[z] <= ZB[z][1] for z in ZB) else "FAIL"} G3]')
    ev, od = list(range(0, len(GS), 2)), list(range(1, len(GS), 2))
    def Jh(q):
        if np.any(np.abs(q) > 5): return 1e9
        return evals({f: (v, x) for (f, v), x in zip(opts, q)}, ev)['J']
    if len(opts) == 1: qh = np.array([minimize_scalar(lambda q: Jh(np.array([q])), bounds=(-5, 5), method='bounded').x])
    else: qh = minimize(Jh, p, method='Nelder-Mead', options=dict(maxfev=200, initial_simplex=[p] + [p + .3 * np.eye(len(p))[i] for i in range(len(p))])).x
    rh = evals({f: (v, x) for (f, v), x in zip(opts, qh)}, od)
    print(f'  holdout: exponents tuned on GS[::2] {np.round(qh, 3).tolist()}; on GS[1::2] slope {rh["s"]:+.4f} [{"PASS" if rh["ok"][0] else "FAIL"} G2], a(z)/a(0) ' + ' '.join(f'{rh["rz"][z]:.3f}' for z in ZB) + f' [{"PASS" if rh["ok"][1] else "FAIL"} G3]', flush=True)
    hand = [f for (f, v) in opts if v == 'rhoDE']; print(f'  hand terms (carry rho_DE explicitly): {hand or "none"}; H-terms: {[f for (f, v) in opts if v == "H"] or "none"}')
    ck('minimal', dict(opts=opts, p=list(p), holdout=list(qh), hold_s=rh['s'], hold_rz=list(rh['rz'].values())))
else:
    b = min(res, key=lambda x: x[2]['J']); print(f'\n(c) NO SOLUTION passes G2, G3 and S within the frozen search; best J {b[2]["J"]:.2f}: {b[0]} {np.round(b[1], 3).tolist()}')
print(f'\nruntime {time.time() - T0:.0f} s')
print('Rival language; adopts nothing. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
