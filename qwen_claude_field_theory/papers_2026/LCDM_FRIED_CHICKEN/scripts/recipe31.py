"""A29: LCDM halo machinery in evolving dark-energy backgrounds; tracking gate GT, per ../FROZEN_A29.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, json, time, resource; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.special import gammainc
s4 = open(os.path.join(HERE, 'recipe4.py'), encoding='utf-8').read(); exec(s4[s4.index('def m200k'):s4.index('def gal(')])
src = open(os.path.join(HERE, 'recipe18.py'), encoding='utf-8').read(); exec(src[src.index('K11B ='):src.index('def tune(')])
T0 = time.time(); CK = os.path.join(HERE, 'recipe31.json')
OUT = json.load(open(CK)) if os.path.exists(CK) else {}
def ck(k, v): OUT[k] = v; json.dump(OUT, open(CK, 'w'), indent=1, default=float)
c_ = 2.998e8; MPC = kpc * 1e3; ZS = [0., 1., 1.5, 2.33]; ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
K = K11B; h0 = .674; BASE = cos; RDE0 = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE0); R10 = 10 * kpc
# ---------- backgrounds ----------
OR_H2 = 4.18e-5  # Omega_r h^2, from memory
def ede_w():
    Om, h, ac = .315, .674, 1 / 3501.; Or = OR_H2 / h**2; n = 4.5
    rl_guess = .685; E = .1 / .9 * (Om * ac**-3 + Or * ac**-4 + rl_guess)
    re = lambda a: 2 * E / (1 + (a / ac)**n); rL = (1 - Om) - re(1.)
    def w(z):
        a = 1 / (1 + np.asarray(z, float)); x = (a / ac)**n; r = re(a)
        return -1 + 1.5 * (r / (r + rL)) * x / (1 + x)
    fchk = E / (Om * ac**-3 + Or * ac**-4 + E + rL)
    return w, fchk, re(1.) / (1 - Om)
WEDE, FEDE, EDE_TODAY = ede_w()
BG = {'B0': dict(de_model='lambda'), 'B1': dict(de_model='w0wa', w0=-.752, wa=-.86), 'B1p': dict(de_model='w0wa', w0=-.838, wa=-.62),
      'B1u': dict(de_model='w0wa', w0=-.667, wa=-1.09), 'B2': dict(de_model='w0wa', w0=-.9, wa=-.1), 'B3': dict(de_model='w0wa', w0=-.95, wa=.35),
      'B4': dict(de_model='w0wa', w0=-1.1, wa=.3), 'B5': dict(de_model='user', wz_function=WEDE)}
NC = [0]
def mk(de, s8, H0=67.4, Om0=.315, Ob0=.0493):
    NC[0] += 1
    return cc.Cosmology(name=f'a29_{NC[0]}', flat=True, H0=H0, Om0=Om0, Ob0=Ob0, sigma8=s8, ns=.965, relspecies=False, persistence='', print_warnings=False, **de)
S30 = BASE.sigma(8., 30.)
def mkP(de, H0=67.4, Om0=.315, Ob0=.0493, R=8.):
    C = mk(de, .811, H0, Om0, Ob0); s8 = .811 * S30 / C.sigma(R, 30.); return mk(de, s8, H0, Om0, Ob0), s8
def env(C, z):
    cc.setCurrent(C); h = C.h
    e = dict(rhoc=C.rho_c(z) * h**2 * Msun / kpc**3, cg=np.asarray(CM.concentration(10**LM * h, '200c', z, model='diemer19'), float), z=z,
             rde=C.rho_de(z) * h**2 * Msun / kpc**3, H=C.Hz(z) * 1e3 / MPC, w=float(C.wz(z)), Om=float(C.Om(z)), Ode=float(C.Ode(z)))
    cc.setCurrent(BASE); return e
# ---------- scales ----------
def T1(e): return c_ * e['H'] / (2 * np.pi)
def T2g(e): return c_ * np.sqrt(8 * np.pi * G * e['rde'] / 3) / (2 * np.pi)
def gcen(e, M):
    c = 10**np.interp(np.log10(M), LM, np.log10(e['cg'])); R = (3 * M * Msun / (800 * np.pi * e['rhoc']))**(1 / 3); rs = R / c
    return 2 * np.pi * G * M * Msun / (4 * np.pi * rs**3 * mu(c)) * rs
M2 = np.array([m200_of(g.Ms) for g in GS]); MMED = np.median(M2); LMH = np.arange(11, 12.51, .25)
def m200z(Ms, z):
    dn, dm, db, dg = K[:4]; zt = z / (1 + z); x = 10**LMS / 10**(11.59 + dm + 1.195 * zt)
    s = 2 * (.0351 - .0247 * zt) * 10**dn * 10**LMS / (x**-(1.376 + db - .826 * zt) + x**(.608 + dg + .329 * zt)); i = np.argmax(s)
    return 10**np.interp(np.log10(Ms), np.log10(s[:i + 1]), LMS[:i + 1])
def galx(g, M, en):
    dn, dm, db, dg, le, a1, a2, a4, le0, a3, f0, f1, dc, sc = K
    sb = g.Mb / (g.Rd / kpc)**2 / 1e6 / 100; c = np.interp(np.log10(M), LM, en['cg']) * 10**dc * (M / 1e12)**sc
    fb = min(g.Mb / M, .5); fg = max((g.Mb - g.Ms) / g.Mb, .01)
    e = 10**le * (g.Ms / M / .01)**a1 * sb**a2 * (fg / .5)**a4; n = np.tanh(min(e, 50)); eta = 10**le0 * (g.Ms / 1e9)**a3
    f = np.clip(f0 + f1 * (np.log10(g.Mb) - 9.5), -1, 1)
    R = (3 * M * Msun / (4 * np.pi * 200 * en['rhoc']))**(1 / 3); A = .16
    ein = lambda r: M * Msun * gammainc(3 / A, 2 / A * (r * c / R)**A) / gammainc(3 / A, 2 / A * c**A)
    m0 = np.maximum(ein(g.r), 1e-30); ri = g.r.copy()
    for _ in range(12):
        mi = np.maximum(ein(ri), 1e-30); ri = .5 * ri + .5 * g.r * (g.mb + (1 - fb) * mi) / mi
    m = np.maximum((1 - f) * m0 + f * mi, 1e-3 * m0) * (1 - fb) * np.tanh(g.r / (eta * 1.75 * g.Rd))**n
    return g.gb + G * m / g.r**2
def r11b(en, kind):
    zz = en['z'] if kind == 'Bz' else 0.; cur = [galx(g, m200z(g.Ms, zz), en) for g in GS]; gt = np.concatenate(cur); a = fit_a(ALLB, gt)
    return a, float(np.sqrt(((np.log10(gt) - np.log10(law(ALLB, a)))**2).mean())), cur
def slope(x, y): return float(np.polyfit(np.log(x), np.log(y), 1)[0])
def gt_dev(a, r): return {z: float(np.log10(a[z] / a[0.]) - .5 * np.log10(r[z] / r[0.])) for z in ZB}
P = lambda b: 'PASS' if b else 'FAIL'
print(f'A29 recipe31; c sqrt(G rho_DE0) {AC:.4e}, A0 {A0:.4e}; EDE f at z_c {FEDE:.4f}, EDE share of Ode0 today {EDE_TODAY:.2e}', flush=True)
# control: B0 on footing P reproduces lib's base c-grid and A26's R11b
C0, s80 = mkP(BG['B0']); e00 = env(C0, 0.)
ctl_c = np.abs(e00['cg'] / CG - 1).max(); base_cur = [galx(g, m200k(g.Ms, *K[:4]), e00) for g in GS]
ctl_r = max(np.abs(np.log10(bc) - np.log10(gal3(g, K, []))).max() for g, bc in zip(GS, base_cur))
print(f'control: B0 sigma8 {s80:.4f}; c-grid vs lib max rel {ctl_c:.1e}; R11b galx vs recipe18 gal3 max {ctl_r:.1e} dex; max |log m200z(0) - log m200k| '
      f'{max(abs(np.log10(m200z(g.Ms, 0.) / m200k(g.Ms, *K[:4]))) for g in GS):.1e}', flush=True)
aB, SB, _ = r11b(e00, 'A'); print(f'R11b base a {aB:.4e} ({aB / A0:.4f} A0), S_base {SB:.4f}; shape tolerance {SB + .005:.4f}', flush=True)
# ---------- main backgrounds ----------
RES = {}; ROUTES = ['T1', 'T2g', 'T3', 'U1', 'R11b-Bz', 'R11b-Az']
for foot in ('P', 'S'):
    print(f'\n===== footing {foot} ({"early amplitude fixed at z 30" if foot == "P" else "sigma8 0.811 today"})', flush=True)
    for bn, de in BG.items():
        key = f'{foot}_{bn}'
        if key in OUT: RES[key] = OUT[key]; print(f' {bn}: (from checkpoint)'); continue
        C, s8 = mkP(de) if foot == 'P' else (mk(de, .811), .811); E = {z: env(C, z) for z in ZS}
        r = {z: E[z]['rde'] / E[0.]['rde'] for z in ZS}; H = {z: E[z]['H'] / E[0.]['H'] for z in ZS}
        A = {'T1': {z: T1(E[z]) for z in ZS}, 'T2g': {z: T2g(E[z]) for z in ZS}, 'T3': {z: gcen(E[z], 1e12) for z in ZS}, 'U1': {z: gcen(E[z], MMED) for z in ZS}}
        u1 = np.array([gcen(E[0.], M) for M in M2]); u1sel = (np.log10(M2) >= 11) & (np.log10(M2) <= 12.5)
        rb = {z: r11b(E[z], 'Bz') for z in ZS}; ra = {z: r11b(E[z], 'Az') for z in ZS}
        A['R11b-Bz'] = {z: rb[z][0] for z in ZS}; A['R11b-Az'] = {z: ra[z][0] for z in ZS}
        Smax = {'R11b-Bz': max(rb[z][1] for z in ZS), 'R11b-Az': max(ra[z][1] for z in ZS)}
        ai = np.array([fit_a(g.gb, c) for g, c in zip(GS, rb[0.][2])]); lmk = np.log10([m200k(g.Ms, *K[:4]) for g in GS]); sk = (lmk >= 11) & (lmk <= 12.5)
        g4 = {'T1': 0., 'T2g': 0., 'T3': float(np.log10([gcen(E[0.], 10**m) for m in LMH]).std()), 'U1': float(np.log10(u1[u1sel]).std()),
              'R11b-Bz': float(np.log10(ai[sk]).std()), 'R11b-Az': float(np.log10(ai[sk]).std())}
        k0 = {k: A[k][0.] / AC for k in A}; k0['U1'] = float(np.median(u1) / AC)
        lnr = np.log(max(r.values()) / min(r.values())); meas = lnr >= .1
        e0 = E[0.]; g5 = {'T1': abs(.5 * e0['Om'] + .5 * e0['Ode'] * (1 + 3 * e0['w'])) * e0['H']**2 * R10 / A0, 'T2g_L': 8 * np.pi * G * e0['rde'] / 3 * R10 / A0,
                          'T2g_fluid': 4 * np.pi * G / 3 * e0['rde'] * abs(1 + 3 * e0['w']) * R10 / A0}
        g5z = {z: dict(L=8 * np.pi * G * E[z]['rde'] / 3 * R10 / A0, fl=4 * np.pi * G / 3 * E[z]['rde'] * abs(1 + 3 * E[z]['w']) * R10 / A0) for z in ZB}
        print(f'\n {bn} {de.get("w0", "")} {de.get("wa", "")}: sigma8 {s8:.4f}; rho_DE(z)/rho_DE0 ' + ' '.join(f'{r[z]:.4f}' for z in ZB) + '; sqrt ' + ' '.join(f'{np.sqrt(r[z]):.4f}' for z in ZB)
              + '; H/H0 ' + ' '.join(f'{H[z]:.4f}' for z in ZB) + f'; w(z) ' + ' '.join(f'{E[z]["w"]:+.3f}' for z in ZS) + f'; Omega_DE(2.33) {E[2.33]["Ode"]:.4f}; ln range rho_DE {lnr:.4f} -> G2z {"measurable" if meas else "NOT MEASURABLE"}', flush=True)
        row = {}
        for k in ROUTES:
            a = A[k]; ke = k0[k]; g1 = abs(np.log10(ke / .5)) <= .05; rz = {z: a[z] / a[0.] for z in ZB}; g3 = all(ZB[z][0] <= rz[z] <= ZB[z][1] for z in ZB)
            dv = gt_dev(a, r); gtp = all(abs(v) <= .05 for v in dv.values()); s2 = slope([r[z] for z in ZS], [a[z] for z in ZS]) if meas else None
            g2 = (abs(s2 - .5) <= .05) if meas else None; g4p = g4[k] <= .1
            row[k] = dict(k0=ke, rz=rz, gt=dv, s2z=s2, G1=g1, G3=g3, GT=gtp, G2z=g2, g4=g4[k], G4=g4p, a=a)
            ex = f'; S max {Smax[k]:.4f} [{P(Smax[k] <= SB + .005)} S]' if k in Smax else ''
            print(f'  {k:8s} kappa_eff {ke:.4f} [{P(g1)} G1]; a(z)/a(0) ' + ' '.join(f'{rz[z]:.4f}' for z in ZB) + f' [{P(g3)} G3]; GT dev ' + ' '.join(f'{dv[z]:+.4f}' for z in ZB)
                  + f' [{P(gtp)} GT]; G2z slope ' + (f'{s2:+.4f} [{P(g2)} G2z]' if meas else 'not measurable') + f'; G4 rms {g4[k]:.4f} [{P(g4p)} G4]' + ex, flush=True)
        print(f'  G5: T1 |q| H^2 r at 10 kpc {g5["T1"]:.2e} a0 [{P(g5["T1"] >= .1)} G5]; T2g Lambda form {g5["T2g_L"]:.2e} a0, fluid form {g5["T2g_fluid"]:.2e} a0 [{P(max(g5["T2g_L"], g5["T2g_fluid"]) >= .1)} G5]; '
              'T2g at z ' + ' '.join(f'{z}: {g5z[z]["L"]:.2e}/{g5z[z]["fl"]:.2e}' for z in ZB) + '; T3, U1, R11b halo gravity [PASS G5 by definition]', flush=True)
        RES[key] = dict(r=r, H=H, routes=row, g5=g5, s8=s8, meas=meas, Smax=Smax, Ode233=E[2.33]['Ode'])
        ck(key, RES[key])
# JSON keys come back as strings from the checkpoint; normalise
def fz(d): return {float(k): v for k, v in d.items()}
for key in RES:
    RES[key]['r'] = fz(RES[key]['r'])
    for k in RES[key]['routes']:
        for f in ('rz', 'gt', 'a'): RES[key]['routes'][k][f] = fz(RES[key]['routes'][k][f])
# ---------- G2x across backgrounds ----------
EVO = ['B1', 'B1p', 'B1u', 'B2', 'B3', 'B4']
print('\nG2x: pooled slope of ln[a(z)/a(0)] vs ln[rho_DE(z)/rho_DE0] over B1, B1p, B1u, B2, B3, B4 at z 1, 1.5, 2.33 (18 points)', flush=True)
for foot in ('P', 'S'):
    for k in ROUTES:
        x = [RES[f'{foot}_{b}']['r'][z] for b in EVO for z in ZB]; y = [RES[f'{foot}_{b}']['routes'][k]['rz'][z] for b in EVO for z in ZB]
        s = slope(x, y); print(f' {foot} {k:8s}: slope {s:+.4f} [{P(abs(s - .5) <= .05)} G2x]; ln-range of rho_DE {np.log(max(x) / min(x)):.3f}', flush=True)
# ---------- verdict table ----------
print('\nTRACK/TIE table (footing P): GT per background; tie = G1, G2 (measurable), G3, G4, GT, G5', flush=True)
for k in ROUTES:
    line = []
    for b in BG:
        rr = RES[f'P_{b}']['routes'][k]; line.append(f'{b}:{"T" if rr["GT"] else "-"}')
    print(f' {k:8s} GT ' + ' '.join(line), flush=True)
# ---------- G2t across rho_DE today, in B1's w0, wa ----------
if 'G2t' not in OUT:
    print('\nG2t: B1 w0, wa; rho_DE0 x f on the A26 C1 physical footing', flush=True); FS = [.5, .71, 1., 1.41, 2.]; rows = {k: [] for k in ('T1', 'T3', 'U1', 'R11b')}; rd = []
    for f in FS:
        wm, wb, wd = .315 * h0**2, .0493 * h0**2, f * .685 * h0**2; h = np.sqrt(wm + wd)
        C, s8 = mkP(BG['B1'], 100 * h, wm / h**2, wb / h**2, R=8. * h / h0); e = env(C, 0.); rd.append(e['rde'])
        rows['T1'].append(T1(e)); rows['T3'].append(gcen(e, 1e12)); rows['U1'].append(float(np.median([gcen(e, M) for M in M2])))
        rows['R11b'].append(fit_a(ALLB, np.concatenate([galx(g, m200k(g.Ms, *K[:4]), e) for g in GS])))
        print(f'  f {f}: h {h:.4f}, Om0 {wm / h**2:.4f}, sigma8 {s8:.4f}, rho_DE0/base {e["rde"] / RDE0:.4f}', flush=True)
    G2T = {k: slope(rd, v) for k, v in rows.items()}; ck('G2t', G2T)
else: G2T = OUT['G2t']
for k, s in G2T.items(): print(f' G2t {k}: slope {s:+.4f} [{P(abs(s - .5) <= .05)} G2t]', flush=True)
print(' G2t T2g: slope 0.5 identically [PASS G2t]')
# ---------- (iii) CPL scan for R11b ----------
print(f'\n(iii) CPL scan, footing P, R11b at K11B frozen (time so far {time.time() - T0:.0f} s)', flush=True)
SC = OUT.get('scan', {}); W0 = np.round(np.arange(-1.6, -.15, .1), 3); WA = np.round(np.arange(-3., 2.01, .25), 3)
for w0 in W0:
    for wa in WA:
        key = f'{w0:+.2f}_{wa:+.2f}'
        if key in SC: continue
        try:
            C, s8 = mkP(dict(de_model='w0wa', w0=float(w0), wa=float(wa))); E = {z: env(C, z) for z in ZS}
            r = {z: E[z]['rde'] / E[0.]['rde'] for z in ZS}; rb = {z: r11b(E[z], 'Bz')[:2] for z in ZS}; ra = {z: r11b(E[z], 'Az')[0] for z in ZB}
            SC[key] = dict(w0=float(w0), wa=float(wa), s8=s8, r=[r[z] for z in ZS], a=[rb[z][0] for z in ZS], S=[rb[z][1] for z in ZS], az=[ra[z] for z in ZB], Ode233=E[2.33]['Ode'])
        except Exception as ex: SC[key] = dict(w0=float(w0), wa=float(wa), err=str(ex)[:120])
    ck('scan', SC); print(f'  w0 {w0:+.2f} done ({time.time() - T0:.0f} s, RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB)', flush=True)
hits = []; best = None; nerr = 0
for key, d in SC.items():
    if 'err' in d: nerr += 1; continue
    r = dict(zip(ZS, d['r'])); a = dict(zip(ZS, d['a'])); dv = gt_dev(a, r); wg = max(abs(v) for v in dv.values())
    meas = np.log(max(r.values()) / min(r.values())) >= .1; s2 = slope(list(r.values()), list(a.values())) if meas else np.nan
    g1 = abs(np.log10(a[0.] / AC / .5)) <= .05; okS = max(d['S']) <= SB + .005; okGT = wg <= .05; ok2 = meas and abs(s2 - .5) <= .05
    rz = {z: a[z] / a[0.] for z in ZB}; g3 = all(ZB[z][0] <= rz[z] <= ZB[z][1] for z in ZB)
    rec = dict(key=key, wg=wg, dv=dv, s2=s2, g1=g1, okS=okS, okGT=okGT, ok2=ok2, g3=g3, rz=rz, Smax=max(d['S']), d=d)
    if okGT and ok2 and g1 and okS: hits.append(rec)
    if best is None or wg < best['wg']: best = rec
nGT = sum(1 for key, d in SC.items() if 'err' not in d and max(abs(v) for v in gt_dev(dict(zip(ZS, d['a'])), dict(zip(ZS, d['r']))).values()) <= .05)
print(f' grid {len(SC)} backgrounds ({nerr} errors); pass GT alone: {nGT}; pass GT + G2z + G1 + S: {len(hits)}', flush=True)
def showrec(t, x):
    d = x['d']; print(f'  {t}: w0 {d["w0"]:+.2f} wa {d["wa"]:+.2f}: sqrt(rho_DE ratio) ' + ' '.join(f'{np.sqrt(v):.3f}' for v in d['r'][1:]) + '; a(z)/a(0) ' + ' '.join(f'{x["rz"][z]:.3f}' for z in ZB)
          + '; GT dev ' + ' '.join(f'{x["dv"][z]:+.3f}' for z in ZB) + f' [{P(x["okGT"])} GT]; G2z {x["s2"]:+.3f} [{P(x["ok2"])}]; G1 [{P(x["g1"])}]; G3 [{P(x["g3"])}]; S max {x["Smax"]:.4f} [{P(x["okS"])}]; '
          f'Omega_DE(2.33) {d["Ode233"]:.3f}; DESI-like box {"yes" if -1.2 <= d["w0"] <= -.4 and -2.5 <= d["wa"] <= .5 else "NO"}', flush=True)
showrec('closest to tracking (smallest worst-z GT deviation)', best)
for x in sorted(hits, key=lambda x: x['wg'])[:10]: showrec('HIT', x)
# Least deviation inside the DESI-like box
box = [x for x in [best] + hits]
inb = []
for key, d in SC.items():
    if 'err' in d or not (-1.2 <= d['w0'] <= -.4 and -2.5 <= d['wa'] <= .5): continue
    r = dict(zip(ZS, d['r'])); a = dict(zip(ZS, d['a'])); dv = gt_dev(a, r); inb.append((max(abs(v) for v in dv.values()), key))
if inb:
    wg, key = min(inb); d = SC[key]; r = dict(zip(ZS, d['r'])); a = dict(zip(ZS, d['a'])); dv = gt_dev(a, r); meas = np.log(max(r.values()) / min(r.values())) >= .1
    s2 = slope(list(r.values()), list(a.values())) if meas else np.nan
    showrec('closest inside the DESI-like box', dict(d=d, dv=dv, wg=wg, s2=s2, rz={z: a[z] / a[0.] for z in ZB}, okGT=wg <= .05, ok2=meas and abs(s2 - .5) <= .05,
            g1=abs(np.log10(a[0.] / AC / .5)) <= .05, g3=all(ZB[z][0] <= a[z] / a[0.] <= ZB[z][1] for z in ZB), Smax=max(d['S']), okS=max(d['S']) <= SB + .005))
print(f'\nruntime {time.time() - T0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB')
print('Rival language; adopts nothing. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
