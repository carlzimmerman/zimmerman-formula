"""A39: clustering dark energy (c_s = 0) and dark scattering (DE-DM momentum exchange) as carriers of rho_DE into halos, per ../FROZEN_A39.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, json, time, resource; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.special import gammainc
from scipy.integrate import solve_ivp
s4 = open(os.path.join(HERE, 'recipe4.py'), encoding='utf-8').read(); exec(s4[s4.index('def m200k'):s4.index('def gal(')])
src = open(os.path.join(HERE, 'recipe18.py'), encoding='utf-8').read(); exec(src[src.index('K11B ='):src.index('def tune(')])
s31 = open(os.path.join(HERE, 'recipe31.py'), encoding='utf-8').read()
exec(s31[s31.index('c_ = 2.998e8'):s31.index('# ---------- scales ----------')])
exec(s31[s31.index('M2 = np.array'):s31.index('def r11b(')])
T0 = time.time(); CK = os.path.join(HERE, 'recipe40.json')
OUT = json.load(open(CK)) if os.path.exists(CK) else {}
def ck(k, v): OUT[k] = v; json.dump(OUT, open(CK, 'w'), indent=1, default=float)
P = lambda b: 'PASS' if b else 'FAIL'
TRAP = getattr(np, 'trapezoid', None) or np.trapz
BGEV = 0.05609  # m^2/kg per b/GeV
GYR = 3.156e16; RHOC0 = RHOC  # kg/m^3, base h (same H0 in all backgrounds)
EVO = ['B1', 'B1p', 'B1u', 'B2', 'B3', 'B4']
LMK = np.log10([m200k(g.Ms, *K[:4]) for g in GS]); SEL4 = (LMK >= 11) & (LMK <= 12.5)
RADM = [(g.r >= kpc) & (g.r <= 30 * kpc) for g in GS]
# ---------------- background tables ----------------
def bgtab(C):
    cc.setCurrent(C); la = np.linspace(np.log(5e-4), np.log(2.), 4000); z = 1 / np.exp(la) - 1
    E = np.asarray(C.Ez(z), float); f = np.asarray(C.rho_de(z), float) / float(C.rho_de(0.)); w = np.asarray(C.wz(z), float)
    zt = np.linspace(0, 12, 2401); age = np.asarray(C.age(zt), float); rde = np.asarray(C.rho_de(zt), float) * C.h**2 * Msun / kpc**3; wt = np.asarray(C.wz(zt), float)
    D = lambda zz: float(C.growthFactor(zz)); out = dict(la=la, E=E, f=f, w=w, Om=C.Om0, Ode=C.Ode0, zt=zt, age=age, rde=rde, wt=wt, D=D)
    cc.setCurrent(BASE); return out
def ip(T, k, s): return np.interp(s, T['la'], T[k])
# ---------------- route (a): spherical collapse with c_s = 0 dark energy ----------------
AI = .01
def rhs(s, y, T, di):
    R, V, x = y; H = ip(T, 'E', s); f = ip(T, 'f', s); w = ip(T, 'w', s); rm = T['Om'] * (1 + di) / R**3
    return [V / H, -.5 * (rm + T['Ode'] * (x + 3 * w * f)) * R / H, -3 * (V / R) * (x + w * f) / H]
def collapse(T, di, dde=None, smax=np.log(2.), ai=None):
    ai = AI if ai is None else ai; si = np.log(ai); f = ip(T, 'f', si); w = ip(T, 'w', si); H = ip(T, 'E', si)
    dd = (1 + w) / (1 - 3 * w) * di if dde is None else dde
    y0 = [ai, H * ai * (1 - di / 3), f * (1 + dd)]
    ta = lambda s, y, *a: y[1]; ta.terminal = True; ta.direction = -1
    r1 = solve_ivp(rhs, (si, smax), y0, args=(T, di), events=ta, rtol=1e-9, atol=1e-13, method='LSODA')
    if not r1.t_events[0].size: return None
    st = r1.t_events[0][0]; yt = r1.y_events[0][0]; Rta = yt[0]
    hv = lambda s, y, *a: y[0] - Rta / 2; hv.terminal = False; hv.direction = -1
    hc = lambda s, y, *a: y[0] - 1e-3 * Rta; hc.terminal = True; hc.direction = -1
    r2 = solve_ivp(rhs, (st, smax), yt, args=(T, di), events=(hv, hc), rtol=1e-9, atol=1e-13, method='LSODA')
    if not r2.t_events[1].size or not r2.t_events[0].size: return None
    sv = r2.t_events[0][0]; yv = r2.y_events[0][0]
    return dict(sta=st, sv=sv, sc=r2.t_events[1][0], xv=yv[2], rmv=T['Om'] * (1 + di) / yv[0]**3, wv=ip(T, 'w', sv), fv=ip(T, 'f', sv))
def collapse_at(T, ac, ai=None):
    def g(di):
        r = collapse(T, di, ai=ai); return (np.log(2.) + 1 if r is None else r['sc']) - np.log(ac)
    di = brentq(g, 2e-4, .4, xtol=1e-12); r = collapse(T, di, ai=ai); r['di'] = di; r['ai'] = AI if ai is None else ai; return r
def eps_of(T, ac, aobs, ai=None):
    r = collapse_at(T, ac, ai); fo = ip(T, 'f', np.log(aobs))
    drho = T['Ode'] * (r['xv'] - fo)  # rho_crit0 units, frozen DE density minus background at observation
    r.update(epsM=drho / r['rmv'], epsY=T['Ode'] * (r['xv'] + r['wv'] * r['fv']) / r['rmv'], drho=drho,
             Dv=r['rmv'] / (T['Om'] / ac**3), dlin=r['di'] * T['D'](1 / ac - 1) / (T['D'](99.) * r['ai'] / .01))  # D proportional to a in the matter era below z 99
    return r
# ---------------- R11b halo on arbitrary radii ----------------
class FG: pass
def mdm_grid(g, M, en):
    rg = np.logspace(np.log10(g.r[0] / 300), np.log10(g.r[-1] * 300), 400); lr = np.log(rg); l0 = np.log(g.r)
    mb = np.exp(np.interp(lr, l0, np.log(g.mb))); mb[rg < g.r[0]] = g.mb[0] * (rg[rg < g.r[0]] / g.r[0])**3; mb[rg > g.r[-1]] = g.mb.max()
    f = FG(); f.r = rg; f.mb = mb; f.gb = 0.; f.Rd = g.Rd; f.Ms = g.Ms; f.Mb = g.Mb
    md = galx(f, M, en) * rg**2 / G; return dict(lr=lr, lmd=np.log(np.maximum(md, 1e-30)), lmb=np.log(mb))
def drag_m(g, gr, tau):
    lr0 = np.log(g.r); mdi = lambda l: np.exp(np.interp(l, gr['lr'], gr['lmd'])); mbi = lambda l: np.exp(np.interp(l, gr['lr'], gr['lmb']))
    k = np.exp(2 * tau); lo = lr0 - 5.; hi = lr0 + 5.
    F = lambda l: np.exp(l) * (mbi(l) + mdi(l)) - k * g.r * (g.mb + mdi(l))
    flo, fhi = F(lo), F(hi); bad = int(((flo > 0) | (fhi < 0)).sum())
    for _ in range(60):
        mid = .5 * (lo + hi); fm = F(mid); up = fm > 0; hi = np.where(up, mid, hi); lo = np.where(up, lo, mid)
    return mdi(.5 * (lo + hi)), bad
def tau1(T, zobs):  # tau per unit xi (xi in m^2/kg), from max(t-10 Gyr, t(z=10)) to t(zobs)
    tob = np.interp(zobs, T['zt'], T['age']); ts = max(tob - 10., np.interp(10., T['zt'], T['age']))
    zs = np.interp(-ts, -T['age'], T['zt']); m = (T['zt'] >= zobs) & (T['zt'] <= zs)
    zz = np.concatenate([[zobs], T['zt'][m], [zs]]); t = np.interp(zz, T['zt'], T['age']) * GYR
    it = (1 + np.interp(zz, T['zt'], T['wt'])) * np.interp(zz, T['zt'], T['rde']) * c_
    return float(-TRAP(it, t)), tob - ts
# ---------------- grading helpers ----------------
def quiet_grade(cur):
    gt = np.concatenate(cur); d = np.log10(gt) - np.log10(ALLL); idx = np.cumsum([0] + [len(c) for c in cur])
    per = np.array([np.sqrt((d[idx[i]:idx[i + 1]]**2).mean()) for i in range(len(cur))]); b = np.floor(np.log10(ALLB) * 2) / 2
    e3 = max(abs(d[b == x].mean()) for x in np.unique(b) if (b == x).sum() >= 50)
    return float(np.sqrt((d**2).mean())), float(np.percentile(per, 95)), float(e3)
def e1_sub(cur, ids):
    d = np.concatenate([np.log10(cur[i]) - np.log10(GS[i].gl) for i in ids]); return float(np.sqrt((d**2).mean()))
def ade(base, cur):
    v = []
    for i, (b, c) in enumerate(zip(base, cur)):
        if not RADM[i].any(): v.append(np.nan); continue
        dg = (c - b)[RADM[i]]; v.append(dg[np.argmax(np.abs(dg))])
    v = np.array(v); return v
def ashape(cur):
    gt = np.concatenate(cur); a = fit_a(ALLB, gt); return a, float(np.sqrt(((np.log10(gt) - np.log10(law(ALLB, a)))**2).mean()))
def slope(x, y): return float(np.polyfit(np.log(x), np.log(y), 1)[0])
ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
def gates(tag, a, r, extra=''):  # a: {z: value}, r: {z: rho_DE ratio}
    aa = {z: abs(a[z]) for z in a}
    if min(aa.values()) == 0:
        print(f'   {tag:22s} identically zero at some z (w = -1 control): G1, G2, G3, GT, G5 not gradable [FAIL as a carrier]', flush=True); return dict(a=a, rz={z: np.nan for z in ZB}, dv={}, s2=None, G1=False, G3=False, GT=False)
    ke = aa[0.] / AC; g1 = abs(np.log10(ke / .5)) <= .05 if ke > 0 else False
    rz = {z: aa[z] / aa[0.] for z in ZB}; g3 = all(ZB[z][0] <= rz[z] <= ZB[z][1] for z in ZB)
    dv = {z: float(np.log10(rz[z]) - .5 * np.log10(r[z])) for z in ZB}; gtp = all(abs(x) <= .05 for x in dv.values())
    meas = np.log(max(r.values()) / min(r.values())) >= .1; s2 = slope([r[z] for z in ZS], [aa[z] for z in ZS]) if meas else None
    print(f'   {tag:22s} a(0) {a[0.] / A0:+.3e} a0, kappa_eff {ke:.3e} [{P(g1)} G1]; a(z)/a(0) ' + ' '.join(f'{rz[z]:.4f}' for z in ZB) + f' [{P(g3)} G3]; GT dev '
          + ' '.join(f'{dv[z]:+.4f}' for z in ZB) + f' [{P(gtp)} GT]; G2z ' + (f'{s2:+.4f} [{P(abs(s2 - .5) <= .05)}]' if meas else 'not measurable') + extra, flush=True)
    return dict(a=a, rz=rz, dv=dv, s2=s2, G1=g1, G3=g3, GT=gtp)
print(f'A39 recipe40; c sqrt(G rho_DE0) {AC:.4e}; 1 b/GeV = {BGEV} m^2/kg', flush=True)
# ---------------- controls ----------------
C0, _ = mkP(BG['B0']); T00 = bgtab(C0); e0c = eps_of(T00, 1., 1.)
print(f'control B0: eps_M {e0c["epsM"]:.2e}, eps_y {e0c["epsY"]:.2e} (must be 0); linear delta_c at z 0 {e0c["dlin"]:.4f} [{P(1.66 <= e0c["dlin"] <= 1.70)} 1.66-1.70]; Delta_v {e0c["Dv"]:.1f}', flush=True)
print('DIAGNOSTIC after the delta_c control failed (not frozen): same code started at a_i 1e-3', flush=True)
for bq in ('B0', 'B1'):
    Tq = bgtab(mkP(BG[bq])[0])
    for zq in (0., 2.33):
        q1 = eps_of(Tq, 1 / (1 + zq), 1 / (1 + zq)); q3 = eps_of(Tq, 1 / (1 + zq), 1 / (1 + zq), ai=1e-3)
        print(f'  {bq} z {zq}: a_i 0.01: delta_c lin {q1["dlin"]:.4f}, eps_M {q1["epsM"]:+.4e}, eps_y {q1["epsY"]:+.4e}, Delta_v {q1["Dv"]:.1f} | a_i 0.001: delta_c lin {q3["dlin"]:.4f}, eps_M {q3["epsM"]:+.4e}, eps_y {q3["epsY"]:+.4e}, Delta_v {q3["Dv"]:.1f}', flush=True)
Cw = mk(dict(de_model='w0wa', w0=-.9, wa=0.), .811); Tw = bgtab(Cw); dl = 1e-4
sol = solve_ivp(rhs, (np.log(AI), np.log(.1)), [AI, ip(Tw, 'E', np.log(AI)) * AI * (1 - dl / 3), ip(Tw, 'f', np.log(AI))], args=(Tw, dl), rtol=1e-10, atol=1e-14, method='LSODA')
R, V, x = sol.y[:, -1]; dm = (1 + dl) * (.1 / R)**3 - 1; dde = x / ip(Tw, 'f', np.log(.1)) - 1; att = .1 / 3.7
print(f'control w -0.9: delta_DE/delta_m at a 0.1 from delta_DE,i 0: {dde / dm:.5f} vs (1+w)/(1-3w) {att:.5f} [{P(abs(dde / dm / att - 1) <= .02)} 2 %]', flush=True)
e00 = env(C0, 0.); g0 = GS[0]; gr0 = mdm_grid(g0, m200z(g0.Ms, 0.), e00); m_t0, _ = drag_m(g0, gr0, 0.)
dir0 = (galx(g0, m200z(g0.Ms, 0.), e00) - g0.gb) * g0.r**2 / G
print(f'control drag tau 0 on {g0.n}: max |log m_solver - log m_galx| {np.abs(np.log10(m_t0 / dir0)).max():.1e} dex [{P(np.abs(np.log10(m_t0 / dir0)).max() < 1e-3)} 1e-3]', flush=True)
tB0, _ = tau1(T00, 0.); print(f'control B0: tau per unit xi {tB0:.2e} (must be 0)', flush=True)
if os.environ.get('A39_CONTROLS_ONLY'): sys.exit(0)
# ---------------- main loop ----------------
RES = OUT.get('RES', {})
for bn, de in BG.items():
    if bn in RES: print(f'\n {bn}: from checkpoint', flush=True); continue
    C, s8 = mkP(de); T = bgtab(C); E = {z: env(C, z) for z in ZS}; r = {z: E[z]['rde'] / E[0.]['rde'] for z in ZS}; w0 = E[0.]['w']
    print(f'\n===== {bn} w0 {de.get("w0", "-")} wa {de.get("wa", "-")}: sigma8 {s8:.4f}; rho_DE(z)/rho_DE0 ' + ' '.join(f'{r[z]:.4f}' for z in ZB) + f'; 1+w0 {1 + w0:+.4f}', flush=True)
    MZ = {z: [m200z(g.Ms, z) for g in GS] for z in ZS}
    base = {z: [galx(g, M, E[z]) for g, M in zip(GS, MZ[z])] for z in ZS}
    dmb = {z: [(b - g.gb) * g.r**2 / G for g, b in zip(GS, base[z])] for z in ZS}
    row = dict(r=r, w0=w0)
    # ----- route (a)
    eps = {z: eps_of(T, 1 / (1 + z), 1 / (1 + z)) for z in ZS}; es = eps_of(T, .5, 1.)
    for z in ZS: print(f'  (a) z {z}: delta_i {eps[z]["di"]:.5f}, delta_c lin {eps[z]["dlin"]:.4f}, Delta_v {eps[z]["Dv"]:.1f}, eps_M {eps[z]["epsM"]:+.4e}, eps_y {eps[z]["epsY"]:+.4e}; '
                      f'(1+w) Ode/Om at collapse {(1 + E[z]["w"]) * E[z]["Ode"] / E[z]["Om"]:+.4e}', flush=True)
    print(f'  (a) sensitivity, collapse at z 1, seen at z 0: eps_M {es["epsM"]:+.4e}, eps_y {es["epsY"]:+.4e}, delta rho_DE {es["drho"]:+.3e} rho_crit0', flush=True)
    ra = {}
    for rd, lab in (('R1', 'R1 top hat'), ('R2', 'R2 tracer (upper bound)')):
        cur = {}
        for z in ZS:
            ez = eps[z]; rhom = RHOC0 * T['Om'] * (1 + z)**3
            if rd == 'R1': cur[z] = [b + 4 * np.pi * G / 3 * ez['epsM'] * ez['Dv'] * rhom * g.r for g, b in zip(GS, base[z])]
            else: cur[z] = [g.gb + (1 + ez['epsY']) * G * m / g.r**2 - 4 * np.pi * G / 3 * (1 + E[z]['w']) * E[z]['rde'] * g.r for g, m in zip(GS, dmb[z])]
        e = quiet_grade(cur[0.]); at = {z: ashape(cur[z]) for z in ZS}; ad = {z: ade(base[z], cur[z]) for z in ZS}
        med = {z: float(np.nanmedian(ad[z])) for z in ZS}; mx = float(np.nanmax(np.abs(ad[0.]))); g4 = float(np.nanstd(np.log10(np.abs(ad[0.][SEL4]))))
        print(f'  (a) {lab}: SPARC z0 E1 {e[0]:.4f} [{P(e[0] <= .02)}] E2 {e[1]:.4f} [{P(e[1] <= .04)}] E3 {e[2]:.4f} [{P(e[2] <= .02)}]; S max {max(at[z][1] for z in ZS):.4f}; '
              f'a_DE median {med[0.] / A0:+.3e} a0, max galaxy {mx / A0:.3e} a0 [{P(abs(med[0.]) >= .1 * A0)} G5]; G4 rms {g4:.4f} [{P(g4 <= .1)} G4]', flush=True)
        ga = gates('a_tot', {z: at[z][0] for z in ZS}, r); gd = gates('a_DE', med, r)
        if rd == 'R1': print(f'   R1 at Saturn (9.58 AU): {4 * np.pi * G / 3 * abs(eps[0.]["epsM"]) * eps[0.]["Dv"] * RHOC0 * T["Om"] * 9.58 * 1.496e11 / A0:.2e} a0', flush=True)
        ra[rd] = dict(E=e, tot=ga, de=gd, g4=g4, mx=mx)
    row['a'] = ra; row['eps'] = {str(z): dict(epsM=eps[z]['epsM'], epsY=eps[z]['epsY'], Dv=eps[z]['Dv']) for z in ZS}; row['eps_sens'] = dict(epsM=es['epsM'], epsY=es['epsY'])
    # ----- route (b)
    t1 = {z: tau1(T, z) for z in ZS}
    print('  (b) tau per (b/GeV) of xi: ' + ' '.join(f'z {z}: {t1[z][0] * BGEV:+.4e} over {t1[z][1]:.2f} Gyr' for z in ZS), flush=True)
    if abs(1 + w0) < 1e-3: print('  (b) 1 + w0 ~ 0: drag rows skipped (effect is zero to the precision of the background)', flush=True); RES[bn] = row; ck('RES', RES); continue
    grids = {z: [mdm_grid(g, M, E[z]) for g, M in zip(GS, MZ[z])] for z in ZS}
    def curb(z, xi):
        out = []; nb = 0
        for g, gr in zip(GS, grids[z]):
            m, b = drag_m(g, gr, xi * BGEV * t1[z][0]); nb += b; out.append(g.gb + G * m / g.r**2)
        return out, nb
    xmax = 200 / abs(1 + w0); rb = {}
    def tune(ids):
        # fixed after the first full run: bounded Brent alone landed at the bound in B3 (E1 2.16 vs 0.0275 at xi 0); now a grid scan incl. xi = 0, then Brent between neighbours
        f = lambda x: e1_sub(curb(0., x)[0], ids); xs = np.concatenate([[0.], xmax * np.logspace(-4, 0, 25)]); fs = np.array([f(x) for x in xs]); j = int(np.argmin(fs))
        lo, hi = xs[max(j - 1, 0)], xs[min(j + 1, len(xs) - 1)]
        rr = minimize_scalar(f, bounds=(lo, hi), method='bounded', options=dict(xatol=max(hi - lo, 1e-9) * 1e-3, maxiter=40))
        return float(rr.x) if rr.fun <= fs[j] else float(xs[j])
    xT = tune(range(len(GS))); xH = tune(range(0, len(GS), 2))
    curH = curb(0., xH)[0]; hold = e1_sub(curH, range(1, len(GS), 2))
    for lab, xi in (('L literature A_ds 10.6', 10.6 / abs(1 + w0)), ('T tuned', xT)):
        cur = {}; nbad = 0
        for z in ZS: cur[z], nb = curb(z, xi); nbad += nb
        e = quiet_grade(cur[0.]); at = {z: ashape(cur[z]) for z in ZS}; ad = {z: ade(base[z], cur[z]) for z in ZS}
        med = {z: float(np.nanmedian(ad[z])) for z in ZS}; mx = float(np.nanmax(np.abs(ad[0.]))); g4 = float(np.nanstd(np.log10(np.abs(ad[0.][SEL4]))))
        A = xi * (1 + w0); Gam = xi * BGEV * (1 + w0) * E[0.]['rde'] * c_
        print(f'  (b) {lab}: xi {xi:.2f} b/GeV, A_ds {A:+.2f} b/GeV' + (' [AT BOUND]' if lab[0] == 'T' and xi > .999 * xmax else '') + f'; Gamma/H0 today {Gam / E[0.]["H"]:+.4f}; tau(z0) {xi * BGEV * t1[0.][0]:+.4f}; '
              f'bracket misses {nbad}; SPARC z0 E1 {e[0]:.4f} [{P(e[0] <= .02)}] E2 {e[1]:.4f} [{P(e[1] <= .04)}] E3 {e[2]:.4f} [{P(e[2] <= .02)}]; S max {max(at[z][1] for z in ZS):.4f} '
              f'[{P(max(at[z][1] for z in ZS) <= .0325)}]; a_DE median {med[0.] / A0:+.3e} a0, max galaxy {mx / A0:.3e} a0 [{P(abs(med[0.]) >= .1 * A0)} G5]; G4 rms {g4:.4f} [{P(g4 <= .1)} G4]; '
              f'bulk drag at 300 km/s {abs(Gam) * 3e5 / A0:.2e} a0', flush=True)
        if lab[0] == 'T': print(f'   holdout: xi tuned on GS[::2] {xH:.2f} b/GeV, unseen GS[1::2] E1 {hold:.4f} [{P(hold <= .025)} holdout]', flush=True)
        ga = gates('a_tot', {z: at[z][0] for z in ZS}, r); gd = gates('a_DE', med, r)
        rb[lab[0]] = dict(xi=xi, E=e, tot=ga, de=gd, g4=g4, mx=mx, hold=hold if lab[0] == 'T' else None)
    row['b'] = rb; RES[bn] = row; ck('RES', RES)
    print(f'  ({time.time() - T0:.0f} s, RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB)', flush=True)
# ---------------- G2x across backgrounds ----------------
print('\nG2x: pooled slope of ln[|a|(z)/|a|(0)] vs ln[rho_DE(z)/rho_DE0], B1, B1p, B1u, B2, B3, B4, z 1, 1.5, 2.33', flush=True)
for path in (('a', 'R1'), ('a', 'R2'), ('b', 'L'), ('b', 'T')):
    for sc in ('tot', 'de'):
        xs, ys = [], []
        for b in EVO:
            rr = RES[b]; d = rr[path[0]].get(path[1]) if path[0] in rr else None
            if d is None: continue
            for z in ('1.0', '1.5', '2.33'):
                rz = d[sc]['rz']; xs.append(rr['r'][z] if z in rr['r'] else rr['r'][float(z)]); ys.append(rz[z] if z in rz else rz[float(z)])
        if xs: s = slope(xs, ys); print(f' ({path[0]}) {path[1]} {sc:3s}: slope {s:+.4f} [{P(abs(s - .5) <= .05)} G2x] over {len(xs)} points', flush=True)
# ---------------- G2t: rho_DE today scaled, B1 w0 wa ----------------
if 'G2t' not in OUT:
    xiT = RES['B1']['b']['T']['xi']; xiL = RES['B1']['b']['L']['xi']; rows = {k: [] for k in ('aR1', 'aR2', 'bL', 'bT', 'totR2', 'totbT')}; rd = []
    for f in [.5, .71, 1., 1.41, 2.]:
        wm, wb, wd = .315 * h0**2, .0493 * h0**2, f * .685 * h0**2; h = np.sqrt(wm + wd)
        C, s8 = mkP(BG['B1'], 100 * h, wm / h**2, wb / h**2, R=8. * h / h0); e = env(C, 0.); T = bgtab(C); rd.append(e['rde'])
        Ms = [m200k(g.Ms, *K[:4]) for g in GS]; base = [galx(g, M, e) for g, M in zip(GS, Ms)]; dmb = [(b - g.gb) * g.r**2 / G for g, b in zip(GS, base)]
        ez = eps_of(T, 1., 1.); rhom = e['rhoc'] * e['Om']
        c1 = [b + 4 * np.pi * G / 3 * ez['epsM'] * ez['Dv'] * rhom * g.r for g, b in zip(GS, base)]
        c2 = [g.gb + (1 + ez['epsY']) * G * m / g.r**2 - 4 * np.pi * G / 3 * (1 + e['w']) * e['rde'] * g.r for g, m in zip(GS, dmb)]
        t1z, _ = tau1(T, 0.); grids = [mdm_grid(g, M, e) for g, M in zip(GS, Ms)]
        cb = lambda xi: [g.gb + G * drag_m(g, gr, xi * BGEV * t1z)[0] / g.r**2 for g, gr in zip(GS, grids)]
        cL, cT = cb(xiL), cb(xiT)
        rows['aR1'].append(abs(np.nanmedian(ade(base, c1)))); rows['aR2'].append(abs(np.nanmedian(ade(base, c2))))
        rows['bL'].append(abs(np.nanmedian(ade(base, cL)))); rows['bT'].append(abs(np.nanmedian(ade(base, cT))))
        rows['totR2'].append(ashape(c2)[0]); rows['totbT'].append(ashape(cT)[0])
        print(f'  f {f}: h {h:.4f}, sigma8 {s8:.4f}, eps_M {ez["epsM"]:+.3e}, eps_y {ez["epsY"]:+.3e}, tau/xi {t1z * BGEV:+.3e} per b/GeV', flush=True)
    G2T = {k: slope(rd, v) for k, v in rows.items()}; ck('G2t', G2T)
else: G2T = OUT['G2t']
for k, s in G2T.items(): print(f' G2t {k}: slope {s:+.4f} [{P(abs(s - .5) <= .05)} G2t]', flush=True)
print(f'\nruntime {time.time() - T0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB')
print('Rival language; adopts nothing. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
