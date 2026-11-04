"""A42: decaying DM (to dark radiation; two-body with a kick), primordial black holes, ETHOS / SIMP, DM-only Yukawa force.
Per ../FROZEN_A42.md. Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, json, time, resource; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
T0 = time.time(); CK = os.path.join(HERE, 'recipe43.json')
OUT = json.load(open(CK)) if os.path.exists(CK) else {}
def ck(k, v): OUT[k] = v; json.dump(OUT, open(CK, 'w'), indent=1, default=float)
c_ = 2.998e8; MPC = kpc * 1e3; RDE0 = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE0); GYR = 3.156e16
ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}; ZS = [0., 1., 1.5, 2.33]; P = lambda b: 'PASS' if b else 'FAIL'
# --- reuse A19's SIDM isothermal-core solver unchanged (recipe21.py core(), mbfun) ---
s21 = open(os.path.join(HERE, 'recipe21.py'), encoding='utf-8').read(); exec(s21[s21.index('TY = 3.156e16'):s21.index('IDX = {id(g)')])
# --- reuse A29's backgrounds (recipe31.py mk, mkP, env) ---
BASE = cos; h0 = .674
s31 = open(os.path.join(HERE, 'recipe31.py'), encoding='utf-8').read(); exec(s31[s31.index('OR_H2 = '):s31.index('# ---------- scales')])
E00 = dict(rhoc=RHOC, cg=CG, z=0., age=float(cos.age(0.)), tf=float(cos.age(2.)))
EVEN, ODD = list(range(0, len(GS), 2)), list(range(1, len(GS), 2))
def ev(idx, cur):
    gsl = [GS[i] for i in idx]; lg = np.concatenate([g.gl for g in gsl]); lb = np.concatenate([g.gb for g in gsl]); lo = np.concatenate([g.gobs for g in gsl])
    gt = np.concatenate(cur); d = np.log10(gt) - np.log10(lg); ob = np.log10(gt) - np.log10(lo)
    per = np.array([np.sqrt(((np.log10(c) - np.log10(g.gl))**2).mean()) for g, c in zip(gsl, cur)])
    b = np.floor(np.log10(lb) * 2) / 2; e3 = max(abs(d[b == x].mean()) for x in np.unique(b) if (b == x).sum() >= 50)
    return dict(e1=float(np.sqrt((d**2).mean())), e2=float(np.percentile(per, 95)), e3=float(e3), obs=float(np.sqrt((ob**2).mean())), a=float(fit_a(lb, gt)))
def hosts(): return [i for i, g in enumerate(GS) if 11 <= np.log10(m200_of(g.Ms)) <= 12.5]
def g4(cur):
    ai = np.array([np.log10(fit_a(GS[i].gb, cur[i])) for i in hosts()]); return float(ai.std()), len(ai)
def halo_e(g, e, dn=0., dc=0., lmhm=None):
    M = m200_of(g.Ms, dn); c = float(np.interp(np.log10(M), LM, e['cg'])) * 10**dc
    if lmhm is not None: c *= (1 + 15 * 10**lmhm / M)**(-.3)
    return M, c
# ======================= engine: shells for decay and Yukawa =======================
NG = {'dr': 200, 'kick': 200, 'yuk': 120}
def shells(i, e, dn, dc, n):
    g = GS[i]; M, c = halo_e(g, e, dn, dc); fb = min(g.Mb / M, .5); R = (3 * M * Msun / (800 * np.pi * e['rhoc']))**(1 / 3); rs = R / c
    r = np.logspace(np.log10(1e-3 * g.r[0]), np.log10(max(R, 3 * g.r[-1])), n); Di = (1 - fb) * M * Msun * mu(r / rs) / mu(c)
    dD = np.diff(Di, prepend=0.); return g, r, Di, dD, MBF[i]
def dfinal(g, rf, m):
    o = np.argsort(rf); cum = np.cumsum(m[o]); rr = rf[o]; ok = cum > 0
    return np.exp(np.interp(np.log(g.r), np.log(rr[ok]), np.log(cum[ok])))
def Fdec(e, ltau, fddm=1.):
    t, tf = e['age'], e['tf']; return 0. if t <= tf else fddm * (1 - np.exp(-(t - tf) / 10**ltau))
def eng_dr(i, e, ltau, dn=0., dc=0., F=None):
    g, r, Di, dD, mbf = shells(i, e, dn, dc, NG['dr']); F = Fdec(e, ltau) if F is None else F; mb0 = mbf(r); L = r * (mb0 + Di); Df = (1 - F) * Di; rf = r.copy()
    for _ in range(40): rf = .5 * rf + .5 * L / (mbf(rf) + Df)
    return g.gb + G * dfinal(g, rf, (1 - F) * dD) / g.r**2
def eng_kick(i, e, ltau, lvk, dn=0., dc=0., F=None):
    g, r, Di, dD, mbf = shells(i, e, dn, dc, NG['kick']); F = Fdec(e, ltau) if F is None else F; vk2 = (10**lvk * 1e3)**2
    mb0 = mbf(r); vc2 = G * (mb0 + Di) / r; esc = vk2 >= vc2; q = np.where(esc, 1 - F, 1.); m = q * dD; Df = np.cumsum(m)
    Ef = np.where(esc, .5 * vc2, .5 * vc2 - .5 * F * vk2); L = r * (mb0 + Di); rf = r.copy()
    for _ in range(40):
        new = np.where(esc, L / (mbf(rf) + Df), G * (mbf(rf) + Df) / (2 * Ef)); rf = .5 * rf + .5 * new
    return g.gb + G * dfinal(g, rf, m) / g.r**2
def gyuk(s, m, beta, lam):
    R, S = s[:, None], s[None, :]; d = np.abs(R - S); mn = np.minimum(R, S); ex = np.exp(-d / lam)
    A = ex * (-np.expm1(-2 * mn / lam)); Ap = -(np.sign(R - S) / lam) * ex + np.exp(-(R + S) / lam) / lam
    K = G * beta * m[None, :] * lam / (2 * S); return (K * (A - R * Ap) / R**2).sum(1)
YRES = []
def eng_yuk(i, e, beta, llam, dn=0., dc=0., passes=30):
    g, r, Di, dD, mbf = shells(i, e, dn, dc, NG['yuk']); lam = 10**llam * kpc; L = r * (mbf(r) + Di); rf = r.copy()
    for k in range(passes):
        o = np.argsort(rf); MY = np.empty_like(rf); MY[o] = rf[o]**2 * gyuk(rf[o], dD[o], beta, lam) / G
        Dc = np.empty_like(rf); Dc[o] = np.cumsum(dD[o]); new = L / np.maximum(mbf(rf) + Dc + MY, 1e-3 * (mbf(rf) + Dc))
        if k == passes - 1: YRES.append(float(np.abs(np.log(new / rf)).max()))
        rf = .7 * rf + .3 * new
    return g.gb + G * dfinal(g, rf, dD) / g.r**2
# ======================= core rows (PBH relaxation, ETHOS, SIMP) =======================
LS = np.linspace(3, 6, 301)  # log10 sigma0 [m/s]
VE = np.log10([30e3, 220e3, 1000e3]); SE = np.log10([.16, .022, .00075]); SL = (SE[2] - SE[1]) / (VE[2] - VE[1])
def sig_ethos(v):
    lv = np.log10(np.maximum(v, 1.)); s = np.interp(lv, VE, SE); s = np.where(lv > VE[2], SE[2] + SL * (lv - VE[2]), s); return 10**s * .1  # m^2/kg
IE = np.array([getattr(np, "trapezoid", getattr(np, "trapz", None))(sig_ethos(XQ * np.sqrt(2) * 10**l) * XQ * np.sqrt(2) * 10**l * FQ, XQ) for l in LS])
def sv_ethos(lA): return lambda s: 10**lA * np.interp(np.log10(s), LS, IE)
def sv_pbh(lm): mk_ = 10**lm * Msun; return lambda s: G**2 * mk_ * 10. / (.34 * s**3)
CORE_INFO = {}
def coremod(i, e, sv, dn=0., dc=0., lmhm=None, tag=None):
    g = GS[i]; M, c = halo_e(g, e, dn, dc, lmhm); fb = min(g.Mb / M, .5); T = min(10., e['age']) * TY
    md, s, r1, mis, _ = core(MBF[i], M, c, fb, sv, T=T, rhoc=e['rhoc'], rd=g.r)
    if tag is not None: CORE_INFO.setdefault(tag, {})[i] = (s, r1, mis)
    return g.gb + G * md / g.r**2
# ======================= rows =======================
ROWS = {
 'DR1': (lambda i, e, k: eng_dr(i, e, k[0]), [2.], [0.], [3.], 25),
 'DR3': (lambda i, e, k: eng_dr(i, e, k[0], k[1], k[2]), [2., 0., 0.], [0., -.3, -.3], [3., .3, .3], 25),
 'K2': (lambda i, e, k: eng_kick(i, e, k[0], k[1]), [1.5, 1.7], [0., .5], [3., 3.], 25),
 'K4': (lambda i, e, k: eng_kick(i, e, k[0], k[1], k[2], k[3]), [1.5, 1.7, 0., 0.], [0., .5, -.3, -.3], [3., 3., .3, .3], 25),
 'P1': (lambda i, e, k: coremod(i, e, sv_pbh(k[0])), [4.], [0.], [8.], 15),
 'P3': (lambda i, e, k: coremod(i, e, sv_pbh(k[0]), k[1], k[2]), [4., 0., 0.], [0., -.3, -.3], [8., .3, .3], 15),
 'C2': (lambda i, e, k: coremod(i, e, sv_ethos(k[1]), lmhm=k[0]), [8., 0.], [6., -2.], [11., 2.], 15),
 'C4': (lambda i, e, k: coremod(i, e, sv_ethos(k[1]), k[2], k[3], lmhm=k[0]), [8., 0., 0., 0.], [6., -2., -.3, -.3], [11., 2., .3, .3], 15),
 'S1': (lambda i, e, k: coremod(i, e, svm(10**k[0])), [0.], [-1.], [1.], 15),
 'S3': (lambda i, e, k: coremod(i, e, svm(10**k[0]), k[1], k[2]), [0., 0., 0.], [-1., -.3, -.3], [1., .3, .3], 15),
 'Y2': (lambda i, e, k: eng_yuk(i, e, k[0], k[1]), [0., 1.], [-.5, -1.], [2., 4.], 25),
 'Y4': (lambda i, e, k: eng_yuk(i, e, k[0], k[1], k[2], k[3]), [0., 1., 0., 0.], [-.5, -1., -.3, -.3], [2., 4., .3, .3], 25)}
def run(fn, k, idx=None, e=E00): idx = range(len(GS)) if idx is None else idx; return [fn(i, e, k) for i in idx]
def tune(fn, x0, lo, hi, nfev, idx):
    lg = np.log10(np.concatenate([GS[i].gl for i in idx])); res = lambda k: np.log10(np.concatenate(run(fn, k, idx))) - lg; best = None
    for s in range(2):
        st = np.array(x0, float) if s == 0 else np.random.default_rng(s).uniform(lo, hi)
        r = least_squares(res, np.clip(st, np.array(lo) + 1e-6, np.array(hi) - 1e-6), bounds=(lo, hi), max_nfev=nfev, diff_step=.02)
        if best is None or r.cost < best.cost: best = r
    return [float(x) for x in best.x], [j for j, (v, a, b) in enumerate(zip(best.x, lo, hi)) if min(v - a, b - v) < 1e-3 * (b - a)]
def head(t): print(f'\n######## {t}  ({time.time() - T0:.0f} s, RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB)', flush=True)
print(f'A42 recipe43; sample {len(GS)} galaxies; c sqrt(G rho_DE0) {AC:.4e}; A0 {A0:.4e}; age today {E00["age"]:.3f} Gyr, at z_f 2 {E00["tf"]:.3f} Gyr', flush=True)
# ======================= controls =======================
head('controls')
cE = max(np.abs(np.log10(eng_dr(i, E00, 2., F=0.)) - np.log10(g.gb + G * (1 - min(g.Mb / m200_of(g.Ms), .5)) * nfw_m(g.r, m200_of(g.Ms), cflat(m200_of(g.Ms), 0, 0))[0] / g.r**2)).max() for i, g in enumerate(GS))
cK = max(np.abs(np.log10(eng_kick(i, E00, 2., 1., F=0.)) - np.log10(eng_dr(i, E00, 2., F=0.))).max() for i in range(len(GS)))
print(f'C_E engine with no effect vs lib (1 - f_b) NFW: max {cE:.2e} dex [{P(cE <= 1e-3)} <= 1e-3]; kick engine at F = 0 vs DR engine: max {cK:.2e} dex', flush=True)
sY = np.logspace(19, 22, 120); mY = np.full(120, 1e38); gl_ = gyuk(sY, mY, 1., 1e6 * kpc); gref = G * (np.cumsum(mY) - mY / 2) / sY**2
cY = np.abs(gl_ / gref - 1).max(); print(f'C_Y Yukawa lambda 1e6 kpc vs beta G D(<r)/r^2 (self half-shell): max rel {cY:.2e} [{P(cY <= 1e-3)} <= 1e-3]', flush=True)
gl2 = gyuk(sY, mY, 1., 1e-3 * kpc); print(f'   lambda 1e-3 kpc (screened) max |g_Y|/(G D/r^2) {np.abs(gl2 / gref).max():.2e}', flush=True)
cur = [coremod(i, E00, svm(1.)) for i in range(len(GS))]; e = grade('C_S control: core solver with recipe21 sv, constant 1 cm^2/g (A19 C0 0.1200)', cur)
print(f'C_S {P(abs(e - .12) <= .002)}: |{e:.4f} - 0.1200| <= 0.002', flush=True)
base = run(lambda i, e_, k: eng_dr(i, e_, 2., F=0.), None); RB = ev(range(len(GS)), base); grade('BASE CDM / P0 PBH-as-CDM (NFW, SHMR, Diemer19, no contraction, 0 knobs)', base)
sd, nh = g4(base); print(f' BASE G4 rms {sd:.3f} over {nh} hosts', flush=True)
# ======================= fixed (0-knob) rows =======================
head('0-knob literature-edge rows')
FIX = {'DR_tau160 (all DM -> DR, tau 160 Gyr, CMB edge from memory)': lambda i, e, k: eng_dr(i, e, np.log10(160.)),
       'K_tau30_vk50 (Peter-Benson edge, tau 30 Gyr, v_k 50 km/s)': lambda i, e, k: eng_kick(i, e, np.log10(30.), np.log10(50.)),
       'C0 ETHOS-4 as published (Table 1 sigma_T(v), log M_hm 8 from memory)': lambda i, e, k: coremod(i, e, sv_ethos(0.), lmhm=8.),
       'P_m10 PBH 10 Msun (near Brandt limit)': lambda i, e, k: coremod(i, e, sv_pbh(1.))}
for t, fn in FIX.items():
    cur = run(fn, None); grade(t, cur); sd, nh = g4(cur); print(f' G4 rms {sd:.3f} over {nh} hosts', flush=True)
print(f' DR at tau 160 Gyr: F(z=0) = {Fdec(E00, np.log10(160.)):.4f}; K at tau 30: F = {Fdec(E00, np.log10(30.)):.4f}', flush=True)
# ======================= tuned rows =======================
RES = {}
for tag, (fn, x0, lo, hi, nfev) in ROWS.items():
    head(f'row {tag}')
    if tag in OUT and 'k' in OUT[tag]: k, atb, ko, atbo = OUT[tag]['k'], OUT[tag]['atb'], OUT[tag]['ko'], OUT[tag]['atbo']
    else:
        k, atb = tune(fn, x0, lo, hi, nfev, list(range(len(GS)))); ko, atbo = tune(fn, x0, lo, hi, nfev, EVEN)
        ck(tag, dict(k=k, atb=atb, ko=ko, atbo=atbo))
    CORE_INFO.pop(tag, None)
    if tag[0] in 'PCS': cur = [coremod(i, E00, *( (sv_pbh(k[0]),) if tag[0] == 'P' else (sv_ethos(k[1]),) if tag[0] == 'C' else (svm(10**k[0]),) ),
                                       *((k[1], k[2]) if tag in ('P3', 'S3') else (k[2], k[3]) if tag == 'C4' else (0., 0.)), lmhm=(k[0] if tag[0] == 'C' else None), tag=tag) for i in range(len(GS))]
    else: YRES.clear(); cur = run(fn, k)
    r = ev(range(len(GS)), cur); grade(f'{tag} tuned on all', cur, f'({len(k)} knobs {np.round(k, 3).tolist()}; at bound {atb})')
    sd, nh = g4(cur); hu = ev(ODD, run(fn, ko, ODD)); r.update(k=k, g4=sd, hold=hu['e1'])
    print(f' {tag}: G4 rms {sd:.3f} over {nh} hosts [{P(sd <= .1)}]; holdout knobs on GS[::2] {np.round(ko, 3).tolist()} (at bound {atbo}), unseen GS[1::2] E1 {hu["e1"]:.4f} [{P(hu["e1"] <= .025)}]', flush=True)
    print(f' {tag}: pooled a_fit {r["a"] / A0:.4f} A0, kappa_eff {r["a"] / AC:.4f} [{P(abs(np.log10(r["a"] / AC / .5)) <= .05)} G1 (tuned)]', flush=True)
    if tag[0] in 'DK':
        F = Fdec(E00, k[0]); tau = 10**k[0] * GYR; print(f' {tag}: tau {10**k[0]:.3g} Gyr, F(z=0) {F:.4f}; native c/tau {c_ / tau / A0:.3e} A0 (kappa_eff {c_ / tau / AC:.3e})'
              + (f'; v_k {10**k[1]:.3g} km/s, v_k/tau {10**k[1] * 1e3 / tau / A0:.3e} A0' if tag[0] == 'K' else '')
              + f'; CMB tau >~ 160 Gyr (memory) {"satisfied" if 10**k[0] >= 160 else "VIOLATED"}' + (f'; Peter-Benson (tau <~ 30 Gyr out for 20-200 km/s) {"VIOLATED" if 10**k[0] < 30 and 20 <= 10**k[1] <= 200 else "satisfied"}' if tag[0] == 'K' else ''), flush=True)
    if tag[0] in 'PCS':
        info = CORE_INFO[tag]; s = np.array([info[i][0] for i in range(len(GS))]); r1 = np.array([info[i][1] for i in range(len(GS))]); gc = s**2 / r1
        print(f' {tag}: core g_c = sigma0^2/r1 median {np.median(gc) / A0:.3f} A0 (kappa_eff {np.median(gc) / AC:.3f}), rms {np.log10(gc).std():.3f} dex; unmatched cores {sum(info[i][2] > .03 * np.log(10) for i in info)}; '
              f'median r1 {np.median(r1) / kpc:.3g} kpc', flush=True)
        if tag[0] in 'CS':
            sm = 10**k[0] if tag[0] == 'S' else .16 * 10**k[1]; ax = G / (sm * .1); print(f' {tag}: native G/(sigma/m) at {sm:.3g} cm^2/g {ax / A0:.3f} A0, kappa_eff {ax / AC:.3f} [{P(abs(np.log10(ax / AC / .5)) <= .05)} G1 native]', flush=True)
        if tag[0] == 'C': print(f' {tag}: half-mode log M_hm {k[0]:.2f}; equivalent m_WDM from M_cut = 1e11 (m/keV)^-4/h (Eq. 6, mass-function cutoff, used loosely): {(1e11 / .674 / 10**k[0])**.25:.2f} keV', flush=True)
        if tag[0] == 'P':
            m = 10**k[0]; sst, frac = [], 0
            for i, g in enumerate(GS):
                M, c = halo_e(g, E00, *((k[1], k[2]) if tag == 'P3' else (0., 0.))); R = (3 * M * Msun / (800 * np.pi * RHOC))**(1 / 3); rs = R / c; rr = 2 * g.Rd
                rho = (1 - min(g.Mb / M, .5)) * M * Msun / (4 * np.pi * rs**3 * mu(c)) / ((rr / rs) * (1 + rr / rs)**2); vc = np.sqrt(np.interp(rr, g.r, cur[i] * g.r))
                sh = vc / np.sqrt(2); tr = .34 * sh**3 / (G**2 * m * Msun * rho * 10.); ss = sh * np.sqrt(min(1., 2 * 10 * TY / tr)); sst.append(ss); frac += ss > .5 * vc
            print(f' {tag}: m_PBH {m:.3g} Msun (Brandt 2016: >~5-10 Msun excluded as all DM); lognormal equivalents m_c = {m * np.exp(-.5):.3g} (s_ln 1), {m * np.exp(-2):.3g} (s_ln 2) Msun; '
                  f'disc heating at 2 R_d: median sigma_* {np.median(sst) / 1e3:.1f} km/s, {frac} of {len(GS)} with sigma_* > 0.5 v_c', flush=True)
    if tag[0] == 'Y':
        Ms_ = np.array([m200_of(g.Ms, *((k[2],) if tag == 'Y4' else (0.,))) for g in GS]); ay = G * abs(k[0]) * Ms_ * Msun / (10**k[1] * kpc)**2
        print(f' {tag}: beta {k[0]:.3f}, lambda {10**k[1]:.3g} kpc; G |beta| M200/lambda^2 median {np.median(ay) / A0:.3e} A0, rms {np.log10(np.maximum(ay, 1e-300)).std():.3f} dex (mass-dependent); '
              f'self-consistency max |dln r| last pass {max(YRES) if YRES else float("nan"):.2e}', flush=True)
    RES[tag] = r
# ======================= z rebuild in A29 backgrounds =======================
head('rebuild at z in the A29 backgrounds (footing P; z = 0 SHMR held; baryons fixed)')
ENV = {}
for b, de in BG.items():
    C, s8 = mkP(de); ENV[b] = {}
    for z in ZS:
        e_ = env(C, z); e_['age'] = float(C.age(z)); e_['tf'] = float(C.age(2.)); ENV[b][z] = e_
    print(f' {b}: sigma8 {s8:.4f}; ages ' + ' '.join(f'{ENV[b][z]["age"]:.3f}' for z in ZS) + f' Gyr; t_f {ENV[b][0.]["tf"]:.3f}', flush=True)
RD = {b: [ENV[b][z]['rde'] / ENV[b][0.]['rde'] for z in ZS] for b in BG}; EVO = ['B1', 'B1p', 'B1u', 'B2', 'B3', 'B4']
ZR = OUT.get('zr', {})
for tag, (fn, *_r) in ROWS.items():
    k = OUT[tag]['k']
    for b in BG:
        key = f'{tag}_{b}'
        if key in ZR: continue
        ZR[key] = [float(fit_a(ALLB, np.concatenate(run(fn, k, None, ENV[b][z])))) for z in ZS]
        ck('zr', ZR)
    print(f' {tag} rebuilt ({time.time() - T0:.0f} s)', flush=True)
head('tie gates per row: G3 (B0), GT per background, G2z, G2x')
for tag in ROWS:
    xs, ys, line = [], [], []
    for b in BG:
        a = ZR[f'{tag}_{b}']; rz = [a[j] / a[0] for j in (1, 2, 3)]; dv = [np.log10(rz[j - 1]) - .5 * np.log10(RD[b][j]) for j in (1, 2, 3)]
        gt = max(map(abs, dv)) <= .05; lnr = np.log(RD[b]); g2z = 'n/m' if lnr.max() - lnr.min() < .1 else f'{np.polyfit(lnr, np.log(a), 1)[0]:+.2f}'
        if b == 'B0': g3 = all(ZB[z][0] <= rz[j] <= ZB[z][1] for j, z in enumerate(ZB)); print(f' {tag}: B0 kappa_eff(0) {a[0] / AC:.4f}; a(z)/a(0) ' + ' '.join(f'{x:.3f}' for x in rz) + f' [{P(g3)} G3]', flush=True)
        line.append(f'{b} {dv[0]:+.3f}/{dv[1]:+.3f}/{dv[2]:+.3f}[{"T" if gt else "-"}] G2z {g2z}')
        if b in EVO: xs += list(np.log(RD[b][1:])); ys += list(np.log(rz))
    sl = np.polyfit(xs, ys, 1)[0]
    print(f'   GT dev z1/z1.5/z2.33: ' + '; '.join(line), flush=True); print(f'   G2x pooled slope {sl:+.3f} [{P(abs(sl - .5) <= .05)}]', flush=True)
print('\nnative-constant reading (tau, v_k, m_PBH, sigma/m, beta, lambda are Lagrangian/particle constants; a flat): GT dev = -0.5 log10 rho_DE ratio:', flush=True)
for b in BG:
    dv = [-.5 * np.log10(RD[b][j]) for j in (1, 2, 3)]; print(f'   {b}: {dv[0]:+.3f} {dv[1]:+.3f} {dv[2]:+.3f} [{P(max(map(abs, dv)) <= .05)} GT]', flush=True)
print(' decay clock F(z) in B0 at DR1/K2 knobs: ' + '; '.join(f'{t}: ' + ' '.join(f'{Fdec(ENV["B0"][z], OUT[t]["k"][0]):.4f}' for z in ZS) for t in ('DR1', 'K2')) + ' (z 0, 1, 1.5, 2.33): follows cosmic time t(z)', flush=True)
print('G2 from the equations: (a) tau, v_k, f_ddm; clock t(z) of the background; (b) m_PBH, ln Lambda; (c) sigma_T(v)/m, M_hm; (d) beta, lambda. rho_DE, Lambda appear in none; native slope 0 [FAIL G2].', flush=True)
print('G5: all four act only through halo gravity at measured radii [PASS by definition]; the native accelerations c/tau, v_k/tau, G/(sigma/m), G M/lambda^2 are not forces [FAIL G5 as scales]. '
      'Cassini: (d) does not act on baryons; (a)-(c) are pure gravity; nothing to grade.', flush=True)
print('\nSUMMARY (tuned on all): row knobs E1 E2 E3 holdout obs G4')
for tag, r in RES.items(): print(f' {tag:4s} {len(r["k"])} {r["e1"]:.4f} {r["e2"]:.4f} {r["e3"]:.4f} {r["hold"]:.4f} {r["obs"]:.4f} {r["g4"]:.3f} [{"EXACT" if r["e1"] <= .02 and r["e2"] <= .04 and r["e3"] <= .02 and r["hold"] <= .025 else "NOT EXACT"}]')
print(f'\nruntime {time.time() - T0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB')
print('Rival language; adopts nothing. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
