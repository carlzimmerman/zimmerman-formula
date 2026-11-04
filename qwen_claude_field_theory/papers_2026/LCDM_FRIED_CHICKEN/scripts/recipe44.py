"""A43: (a) baryon-tracing dark mass (Hoekstra, van Albada & Sancisi 2001 HI scaling; Pfenniger-Combes cold gas),
(b) DM-baryon scattering halos, heavy and light (millicharged-range), sigma ~ v^n, n = -4, -2, 0, 2. Per ../FROZEN_A43.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, json, time, resource; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
T0 = time.time(); CK = os.path.join(HERE, 'recipe44.json')
OUT = json.load(open(CK)) if os.path.exists(CK) else {}
def ck(k, v): OUT[k] = v; json.dump(OUT, open(CK, 'w'), indent=1, default=float)
c_ = 2.998e8; MPC = kpc * 1e3; RDE0 = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE0); GYR = 3.156e16
ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}; P = lambda b: 'PASS' if b else 'FAIL'
SIG = Msun / (3.0857e16)**2  # 1 Msun/pc^2 in kg/m^2
EVEN, ODD = GS[::2], GS[1::2]
def ev(gsl, cur):
    lg = np.concatenate([g.gl for g in gsl]); lb = np.concatenate([g.gb for g in gsl]); lo = np.concatenate([g.gobs for g in gsl])
    gt = np.concatenate(cur); d = np.log10(gt) - np.log10(lg); ob = np.log10(gt) - np.log10(lo)
    per = np.array([np.sqrt(((np.log10(c) - np.log10(g.gl))**2).mean()) for g, c in zip(gsl, cur)])
    b = np.floor(np.log10(lb) * 2) / 2; e3 = max(abs(d[b == x].mean()) for x in np.unique(b) if (b == x).sum() >= 50)
    return dict(e1=float(np.sqrt((d**2).mean())), e2=float(np.percentile(per, 95)), e3=float(e3), obs=float(np.sqrt((ob**2).mean())), a=float(fit_a(lb, gt)))
def show(tag, gsl, cur, nk):
    r = ev(gsl, cur)
    print(f'{tag}: knobs {nk}; E1 {r["e1"]:.4f} [{P(r["e1"] <= .02)}] E2 {r["e2"]:.4f} [{P(r["e2"] <= .04)}] E3 {r["e3"]:.4f} [{P(r["e3"] <= .02)}]; '
          f'rms to observed {r["obs"]:.4f}; a_fit {r["a"]:.4e} = {r["a"] / A0:.4f} A0, kappa_eff {r["a"] / AC:.4f}', flush=True)
    return r
HOSTS = [i for i, g in enumerate(GS) if 11 <= np.log10(m200_of(g.Ms)) <= 12.5]
def g4(cur):
    ai = np.array([np.log10(fit_a(GS[i].gb, cur[i])) for i in HOSTS]); return float(ai.std()), float(10**np.median(ai)), len(ai)
def e1of(gsl, cur):
    d = np.concatenate([np.log10(c) - np.log10(g.gl) for g, c in zip(gsl, cur)]); return float(np.sqrt((d**2).mean()))
# ---- re-read gas and stars with lib's mask; SPARC table R_HI ----
TAB = {}
for l in open(os.path.join(D, 'SPARC_Lelli2016c.mrt')):
    p = l.split()
    if len(p) >= 17 and p[1].isdigit() and len(l) > 90:
        try: TAB[p[0]] = dict(MHI=float(p[13]), RHI=float(p[14]))
        except (ValueError, IndexError): pass
for g in GS:
    a = np.loadtxt(os.path.join(D, 'sparc_data', g.n + '_rotmod.dat')); a = a[a[:, 0] > 0]
    vb2 = a[:, 3] * abs(a[:, 3]) + YD * a[:, 4] * abs(a[:, 4]) + YB * a[:, 5] * abs(a[:, 5]); ok = vb2 > 0
    g.ggas = a[ok, 3] * abs(a[ok, 3]) * 1e6 / g.r; g.gst = g.gb - g.ggas
    assert np.allclose(a[ok, 0] * kpc, g.r)
    g.MHI = TAB[g.n]['MHI'] * 1e9 * Msun; g.RHI = TAB[g.n]['RHI'] * kpc
print(f'A43 recipe44; sample {len(GS)} galaxies, {sum(len(g.r) for g in GS)} points; c sqrt(G rho_DE0) {AC:.4e}; A0 {A0:.4e}; hosts {len(HOSTS)}', flush=True)
print(f'points with V_gas^2 < 0: {sum(int((g.ggas < 0).sum()) for g in GS)}', flush=True)
RES = {}
# ======================= (a) HI-scaling dark mass =======================
print('\n=== (a) baryon-tracing dark mass: g = g_b + eta g_gas + eps g_star ===', flush=True)
NFL = [0]
def hmod(g, eta, eps=0., count=False):
    gt = g.gb + eta * g.ggas + eps * g.gst; fl = gt < 1e-3 * g.gb
    if count: NFL[0] += int(fl.sum())
    return np.where(fl, 1e-3 * g.gb, gt)
def fitH(gsl, x0, lo, hi, two):
    lg = np.log10(np.concatenate([g.gl for g in gsl]))
    res = lambda k: np.log10(np.concatenate([hmod(g, k[0], k[1] if two else 0.) for g in gsl])) - lg
    r = least_squares(res, x0, bounds=(lo, hi), diff_step=1e-4); atb = [i for i, (v, a, b) in enumerate(zip(r.x, lo, hi)) if min(v - a, b - v) < 1e-3 * (b - a)]
    return r.x, atb
def native(cur, eta_list):
    adg, aout = [], []
    for g, c, e in zip(GS, cur, eta_list):
        if g.RHI > 0: adg.append(2 * np.pi * G * (1 + e) * 1.33 * g.MHI / (np.pi * g.RHI**2))
        aout.append((c[-1] * g.r[-1])**2 / (G * g.mbtot))
    return np.array(adg), np.array(aout)
def scales(tag, cur, eta_list):
    adg, aout = native(cur, eta_list); la = np.log10(adg); lo_ = np.log10(aout)
    sd, am, nh = g4(cur)
    print(f'  {tag} scales: native a_dg = 2 pi G (1+eta) Sigma_gas: median {10**np.median(la) / A0:.4f} A0 (kappa_eff {10**np.median(la) / AC:.4f}), spread {la.std():.3f} dex over {len(la)}; '
          f'outer a_out = V_last^4/(G M_b): median {10**np.median(lo_) / A0:.4f} A0, spread {lo_.std():.3f} dex; G4 per-galaxy fit_a rms {sd:.3f} dex over {nh} hosts [{P(sd <= .1)}], median {am / A0:.4f} A0', flush=True)
    return dict(adg=float(10**np.median(la)), adg_sd=float(la.std()), g4=sd)
SUN_ETA = 20 / 13.7
NFL[0] = 0; cur = [hmod(g, 7., count=True) for g in GS]
RES['H0'] = show('H0 published HvAS 2001 eta = 7 (0 fitted)', GS, cur, 0); print(f'  floored points {NFL[0]}', flush=True)
RES['H0'].update(scales('H0', cur, [7.] * len(GS)))
print(f'  C_loc: eta x 13.7 Msun/pc^2 = {7 * 13.7:.1f} vs room 20 [{P(7 <= SUN_ETA)}]', flush=True)
for tag, two, x0, lo, hi in [('H1 global eta', False, [7.], [0.], [50.]), ('H2 global eta + eps', True, [7., .5], [0., 0.], [50., 10.])]:
    p, atb = fitH(GS, x0, lo, hi, two); NFL[0] = 0
    cur = [hmod(g, p[0], p[1] if two else 0., count=True) for g in GS]
    k = tag.split()[0]; RES[k] = show(tag + ' tuned on all', GS, cur, len(p))
    print(f'  knobs {np.round(p, 4).tolist()} at bound {atb}; floored points {NFL[0]}', flush=True)
    RES[k].update(scales(k, cur, [p[0]] * len(GS))); RES[k]['p'] = list(map(float, p))
    po, atbo = fitH(EVEN, x0, lo, hi, two); hu = ev(ODD, [hmod(g, po[0], po[1] if two else 0.) for g in ODD]); RES[k]['hold'] = hu['e1']
    print(f'  holdout: tuned GS[::2] {np.round(po, 4).tolist()} (at bound {atbo}); unseen GS[1::2] E1 {hu["e1"]:.4f} [{P(hu["e1"] <= .025)}]', flush=True)
    print(f'  C_loc: eta x 13.7 = {p[0] * 13.7:.1f} Msun/pc^2 vs room 20 [{P(p[0] <= SUN_ETA)}]' + (f' (plus eps x stellar ~35: {p[1] * 35:.1f})' if two else ''), flush=True)
for tag, two in [('H3 per-galaxy eta (171)', False), ('H4 per-galaxy eta + eps (342)', True)]:
    pk = []
    for g in GS:
        lg = np.log10(g.gl)
        r = least_squares(lambda k: np.log10(hmod(g, k[0], k[1] if two else 0.)) - lg, [7., .5] if two else [7.], bounds=([0., 0.] if two else [0.], [200., 20.] if two else [200.]), diff_step=1e-4)
        pk.append(r.x)
    pk = np.array(pk); cur = [hmod(g, q[0], q[1] if two else 0.) for g, q in zip(GS, pk)]
    k = tag.split()[0]; RES[k] = show(tag, GS, cur, 171 * (2 if two else 1))
    atk = int(((pk[:, 0] < .01) | (pk[:, 0] > 199)).sum()) + (int(((pk[:, 1] < .001) | (pk[:, 1] > 19.9)).sum()) if two else 0)
    print(f'  eta median {np.median(pk[:, 0]):.2f} (16-84 {np.percentile(pk[:, 0], 16):.2f}-{np.percentile(pk[:, 0], 84):.2f})' + (f'; eps median {np.median(pk[:, 1]):.3f} (16-84 {np.percentile(pk[:, 1], 16):.3f}-{np.percentile(pk[:, 1], 84):.3f})' if two else '') +
          f'; knobs at bound {atk}; fraction with eta <= C_loc limit {SUN_ETA:.2f}: {(pk[:, 0] <= SUN_ETA).mean():.3f}', flush=True)
    RES[k].update(scales(k, cur, list(pk[:, 0])))
print(f'[{time.time() - T0:.0f}s]', flush=True)
# ======================= (b) DM-baryon scattering halos =======================
print('\n=== (b) DM-baryon scattering: heavy (100 GeV) dark disc and light (10 MeV) heated core ===', flush=True)
MP = 1.6726e-27; GEV = 1.7827e-27; SG = 8e3; VREF = 1e5; TT = 10 * GYR
BR = {'heavy': 100 * GEV, 'light': .01 * GEV}
NG = 200
class HB: pass
def prep(g, dc):
    h = HB(); M = m200_of(g.Ms); c = cflat(M, dc, 0.); fb = min(g.Mb / M, .5)
    R = np.exp(np.linspace(np.log(.05 * g.r[0]), np.log(g.r[-1]), NG)); lR = np.log(R); lr = np.log(g.r)
    MN = (1 - fb) * nfw_m(R, M, c)[0]; h.MNd = (1 - fb) * nfw_m(g.r, M, c)[0]
    gbR = np.interp(lR, lr, g.gb); ins = R < g.r[0]; gbR[ins] = g.gb[0] * R[ins] / g.r[0]
    Mg = np.maximum.accumulate(np.maximum(g.ggas * g.r**2 / G, 0.)); h.Mgt = Mg[-1]
    MgR = np.interp(lR, lr, Mg); MgR[ins] = Mg[0] * (R[ins] / g.r[0])**3
    rhog = np.gradient(MgR, R) / (4 * np.pi * R**2); rhog = np.maximum(rhog, 0.)
    Vc2 = gbR * R + G * MN / R; vrel = np.sqrt(Vc2 + 3 * Vc2 / 2 + 3 * SG**2)
    h.R, h.MN, h.gbR, h.rhog, h.vrel = R, MN, gbR, rhog, vrel; h.dMN = np.diff(np.concatenate([[0.], MN]))
    return h
PRE = {}
def getpre(dc):
    k = round(dc, 4)
    if k not in PRE: PRE.clear(); PRE[k] = [prep(g, dc) for g in GS]
    return PRE[k]
def Nrate(h, s, n, mchi, tfac=1.):
    mf = mchi**2 / (mchi + MP)**2
    return 2 * h.rhog * (10**s * .1) * h.vrel * (h.vrel / VREF)**n * mf * TT * tfac
LR0 = np.linspace(-30, -14, 49)
def isoM(h, r1i, sig, lrho0):
    R = h.R[:r1i + 1]; lx = np.log(R); dx = lx[1] - lx[0]; rho0 = 10**lrho0; s2 = sig**2
    M = 4 * np.pi / 3 * rho0 * R[0]**3; lr = np.zeros_like(rho0); out = np.empty((len(R), len(rho0)))
    for i in range(len(R)):
        out[i] = M; r = R[i]
        lr = lr - dx * r * (h.gbR[i] + G * M / r**2) / s2; M = M + 4 * np.pi * rho0 * np.exp(lr) * r**3 * dx
    return out
def light_m(h, N, sig):
    w = np.where(N >= 1)[0]
    if len(w) == 0: return None, 0
    r1i = int(w[-1])
    if r1i < 2: return None, 0
    tgt = np.log(h.MN[r1i]); m = isoM(h, r1i, sig, LR0); y = np.log(np.maximum(m[-1], 1e-300)) - tgt
    j = np.where(np.diff(np.sign(y)) > 0)[0]
    if len(j) == 0: k = int(np.argmin(abs(y))); return m[:, k], 1 if abs(y[k]) > .01 else 0
    l2 = np.linspace(LR0[j[0]], LR0[j[0] + 1], 25); m2 = isoM(h, r1i, sig, l2); y2 = np.log(np.maximum(m2[-1], 1e-300)) - tgt
    k = int(np.argmin(abs(y2))); return m2[:, k], 0
def bmod(i, g, h, s, n, br, tfac=1., info=None):
    mchi = BR[br]; N = Nrate(h, s, n, mchi, tfac)
    if br == 'heavy':
        f = 1 - np.exp(-np.minimum(N, 700)); unc = (1 - f) * h.dMN; Mu = np.cumsum(unc); Mc = (f * h.dMN).sum()
        Mud = np.interp(np.log(g.r), np.log(h.R), Mu); Mud[g.r < h.R[0]] = h.MNd[g.r < h.R[0]]
        gt = g.gb + G * Mud / g.r**2 + (Mc / h.Mgt if h.Mgt > 0 else 0.) * g.ggas
        if info is not None: info.append(Mc / h.MN[-1])
    else:
        sig = SG * np.sqrt(MP / mchi); m, bad = light_m(h, N, sig)
        if m is None: Md = h.MNd
        else:
            r1 = h.R[len(m) - 1]; Md = np.where(g.r <= r1, np.interp(np.log(g.r), np.log(h.R[:len(m)]), m), h.MNd)
        gt = g.gb + G * Md / g.r**2
        if info is not None: info.append((0. if m is None else h.MN[len(m) - 1] / h.MN[-1], bad))
    return np.maximum(gt, 1e-3 * g.gb)
def model(s, n, br, dc=0., idx=None, tfac=1., info=None):
    pre = getpre(dc); idx = range(len(GS)) if idx is None else idx
    return [bmod(i, GS[i], pre[i], s, n, br, tfac, info) for i in idx]
IE, IO = list(range(0, len(GS), 2)), list(range(1, len(GS), 2))
def tune1(n, br, dc=0., idx=None):
    gsl = GS if idx is None else [GS[i] for i in idx]
    sg = np.arange(-8, 10.01, .5); ee = [e1of(gsl, model(s, n, br, dc, idx)) for s in sg]; k = int(np.argmin(ee))
    lo, hi = sg[max(k - 1, 0)], sg[min(k + 1, len(sg) - 1)]
    r = minimize_scalar(lambda s: e1of(gsl, model(s, n, br, dc, idx)), bounds=(lo, hi), method='bounded', options=dict(xatol=1e-3))
    s = float(r.x) if r.fun <= min(ee) else float(sg[k]); return s, min(float(r.fun), min(ee)), bool(s <= -7.99 or s >= 9.99)
cur = model(-20, 0, 'heavy'); RES['N0'] = show('N0 base halo, no coupling (SHMR + Diemer19 NFW, 0 knobs)', GS, cur, 0)
LIM = {}
def lims(br, n):
    m_g = BR[br] * 1e3; mgev = BR[br] / GEV
    if n == 0:
        if br == 'heavy': return 10**(np.log10(1.7e-25) + (np.log10(mgev) - 0) / 3 * (np.log10(1.6e-23) - np.log10(1.7e-25))), 'CMB n=0 (interp 1 GeV-1 TeV)'
        return 10**(np.log10(3e-26) + (np.log10(mgev * 1e3) - 0) / 3 * (np.log10(1.7e-25) - np.log10(3e-26))), 'CMB n=0 (interp 1 MeV-1 GeV); MW satellites 8.8e-29 at 100 MeV stronger'
    base = {-2: 2.3e-33, -4: 1.7e-41, 2: 1.4e-23}[n]
    if br == 'light': return base, {-2: 'CMB n=-2 (m<10 MeV)', -4: 'CMB n=-4 (m<10 MeV)', 2: 'MW satellites n=2 at 10 MeV'}[n]
    if n == 2: return base * BR[br] / (.01 * GEV), 'ESTIMATE: n=2 10 MeV limit x m/10 MeV (heavy n=2 not retrieved)'
    return base * BR[br] / MP, f'ESTIMATE: n={n} limit on sigma0/m matched at m_p (from memory)'
best = None
for br in ('heavy', 'light'):
    for n in (-4, -2, 0, 2):
        key = f'{br}_n{n:+d}'
        if key not in OUT:
            s, e, atb = tune1(n, br); so, eo, atbo = tune1(n, br, idx=IE); ck(key, dict(s=s, atb=atb, so=so, atbo=atbo))
        d = OUT[key]; s = d['s']; info = []
        cur = model(s, n, br, info=info); RES[key] = r = show(f'{key}: s = log10(sigma_ref/m at 100 km/s) tuned on all', GS, cur, 1)
        hu = e1of(ODD, model(d['so'], n, br, idx=IO)); r['hold'] = hu; r['s'] = s
        sd, am, nh = g4(cur); r['g4'] = sd
        if br == 'heavy': cf = np.array(info); fr = f'coupled DM fraction (within r_last) median {np.median(cf):.3f} (16-84 {np.percentile(cf, 16):.3f}-{np.percentile(cf, 84):.3f}); eta_eff = M_c/M_gas median {np.median([OUT_ for OUT_ in [0]]):.0f}'
        else: cf = np.array([x[0] for x in info]); nb = sum(x[1] for x in info); fr = f'DM fraction inside r1 (heated/cooled region) median {np.median(cf):.3f}; galaxies with r1 > 0: {(cf > 0).sum()}; unmatched mass {nb}'
        if br == 'heavy':
            pre = getpre(0.); et = np.array([(1 - np.exp(-np.minimum(Nrate(h, s, n, BR[br]), 700))) @ h.dMN / h.Mgt for h in pre if h.Mgt > 0]); fr = fr.split('; eta_eff')[0] + f'; eta_eff = M_c/M_gas median {np.median(et):.2f} (16-84 {np.percentile(et, 16):.2f}-{np.percentile(et, 84):.2f}); fraction with eta_eff <= C_loc {SUN_ETA:.2f}: {(et <= SUN_ETA).mean():.3f}'
        lim, src = lims(br, n); s0 = 10**s * BR[br] * 1e3 * (c_ / VREF)**n; slim_g = lim * (VREF / c_)**n / (BR[br] * 1e3)
        r['ratio'] = s0 / lim
        print(f'  knob s {s:.3f} at bound {d["atb"]}; holdout tuned GS[::2] s {d["so"]:.3f}, unseen E1 {hu:.4f} [{P(hu <= .025)}]; G4 {sd:.3f} over {nh} [{P(sd <= .1)}]', flush=True)
        print(f'  {fr}', flush=True)
        print(f'  bounds: sigma_ref/m {10**s:.3g} cm^2/g at 100 km/s -> sigma0 (v in c) {s0:.3g} cm^2 at m {BR[br] / GEV:g} GeV; limit {lim:.3g} ({src}) = {slim_g:.3g} cm^2/g at 100 km/s; needed/limit {s0 / lim:.3g} [{"ALLOWED" if s0 <= lim else "EXCLUDED"}]'
              f'{"; 0.4 % subcomponent loophole " + ("usable" if np.median(cf) <= .004 else "not usable (needs " + f"{np.median(cf):.3f} of DM)") if n == -4 else ""}; A7 M3 record 0.63 (g_b = a0), 40 (last point)', flush=True)
        if best is None or r['e1'] < RES[best]['e1']: best = key
print(f'[{time.time() - T0:.0f}s] best (b) row by E1: {best}', flush=True)
br, n = best.split('_n')[0], int(best.split('_n')[1])
if 'X2' not in OUT:
    rows = []
    for dc in np.linspace(-.5, .5, 11):
        s, e, atb = tune1(n, br, dc); rows.append((e, float(dc), s))
    e, dc, s = min(rows); so_rows = []
    for dco in np.linspace(-.5, .5, 11):
        so, eo, _ = tune1(n, br, dco, idx=IE); so_rows.append((eo, float(dco), so))
    eo, dco, so = min(so_rows); ck('X2', dict(dc=dc, s=s, dco=dco, so=so)); PRE.clear()
d = OUT['X2']; cur = model(d['s'], n, br, d['dc']); RES['X2'] = show(f'X2 {best} + global log c offset (2 knobs)', GS, cur, 2)
hu = e1of(ODD, model(d['so'], n, br, d['dco'], idx=IO)); sd, _, nh = g4(cur)
print(f'  knobs s {d["s"]:.3f}, dc {d["dc"]:+.2f} (s at bound {d["s"] <= -7.99 or d["s"] >= 9.99}, dc at bound {abs(d["dc"]) >= .5}); holdout tuned s {d["so"]:.3f} dc {d["dco"]:+.2f}, unseen E1 {hu:.4f} [{P(hu <= .025)}]; G4 {sd:.3f} [{P(sd <= .1)}]', flush=True)
PRE.clear()
if 'X3' not in OUT:
    ps = []
    for i, g in enumerate(GS):
        sg = np.arange(-8, 10.01, .5); ee = [e1of([g], model(s, n, br, 0., [i])) for s in sg]; k = int(np.argmin(ee))
        r = minimize_scalar(lambda s: e1of([g], model(s, n, br, 0., [i])), bounds=(sg[max(k - 1, 0)], sg[min(k + 1, len(sg) - 1)]), method='bounded', options=dict(xatol=1e-3))
        ps.append(float(r.x) if r.fun <= ee[k] else float(sg[k]))
    ck('X3', ps)
ps = np.array(OUT['X3']); cur = [model(ps[i], n, br, 0., [i])[0] for i in range(len(GS))]
RES['X3'] = show(f'X3 {best} per-galaxy s (171, freedom only)', GS, cur, 171)
print(f'  s median {np.median(ps):.2f} (16-84 {np.percentile(ps, 16):.2f}-{np.percentile(ps, 84):.2f}), spread {ps.std():.2f} dex in sigma/m; at bound {int(((ps <= -7.99) | (ps >= 9.99)).sum())}', flush=True)
print(f'[{time.time() - T0:.0f}s]', flush=True)
# ======================= (c) scale, G1-G5, GT in A29 backgrounds =======================
print('\n=== (c) acceleration scale: G1-G5 and GT in the A29 backgrounds ===', flush=True)
s31 = open(os.path.join(HERE, 'recipe31.py'), encoding='utf-8').read(); exec(s31[s31.index('OR_H2 = '):s31.index('S30 = ')])
ZS = [0., 1., 1.5, 2.33]; RD, AGE = {}, {}
for b, de in BG.items():
    C = mk(de, .811); RD[b] = [float(C.rho_de(z) / C.rho_de(0)) for z in ZS]; AGE[b] = [float(C.age(z) / C.age(0)) for z in ZS]
cc.setCurrent(cos)
s_b = RES[best]['s']; a0b = fit_a(ALLB, np.concatenate(model(s_b, n, br)))
if 'agez' not in OUT:
    az = {}
    for b in BG: az[b] = [1.] + [float(fit_a(ALLB, np.concatenate(model(s_b, n, br, tfac=AGE[b][j]))) / a0b) for j in (1, 2, 3)]
    ck('agez', az)
AZ = OUT['agez']
READ = {'(a) r1 / (b) r1 flat: eta, Sigma, sigma microphysics constant': lambda b: [1., 1., 1., 1.],
        '(a) r2 gas surface density follows Omega_HI(z) ~ (1+z)^0.57': lambda b: [(1 + z)**.57 for z in ZS],
        f'(b) r2 coupling time = cosmic age(z), best row {best} re-run': lambda b: AZ[b]}
EVO = ['B1', 'B1p', 'B1u', 'B2', 'B3', 'B4']
for name, fa in READ.items():
    print(f'-- reading {name}', flush=True)
    xs, ys = [], []
    for b in BG:
        ar = fa(b); dev = [np.log10(ar[j]) - .5 * np.log10(RD[b][j]) for j in (1, 2, 3)]
        g3 = all(ZB[z][0] <= ar[j] <= ZB[z][1] for j, z in zip((1, 2, 3), (1., 1.5, 2.33)))
        lnr = np.log(RD[b]); g2z = 'not measurable' if lnr.max() - lnr.min() < .1 else f'{np.polyfit(lnr, np.log(ar), 1)[0]:+.3f}'
        print(f'   {b:4s} rho_DE ratio {RD[b][1]:.3f} {RD[b][2]:.3f} {RD[b][3]:.3f}; age ratio {AGE[b][1]:.3f} {AGE[b][2]:.3f} {AGE[b][3]:.3f}; a(z)/a(0) {ar[1]:.3f} {ar[2]:.3f} {ar[3]:.3f} [G3 {P(g3)}]; '
              f'GT dev {dev[0]:+.3f} {dev[1]:+.3f} {dev[2]:+.3f} [{P(max(map(abs, dev)) <= .05)}]; G2z {g2z}', flush=True)
        if b in EVO: xs += list(np.log(RD[b][1:])); ys += list(np.log(ar[1:]))
    sl = np.polyfit(xs, ys, 1)[0]; print(f'   G2x pooled slope over {len(xs)} points {sl:+.3f} [{P(abs(sl - .5) <= .05)}]', flush=True)
print('G1 kappa_eff (target 0.5, 0.05 dex):', flush=True)
for k, v in [('H0 a_fit', RES['H0']['a']), ('H1 a_fit', RES['H1']['a']), ('H2 a_fit', RES['H2']['a']), ('H4 a_fit', RES['H4']['a']),
             ('H0 native a_dg median', RES['H0']['adg']), ('H1 native a_dg median', RES['H1']['adg']), ('N0 base a_fit', RES['N0']['a']),
             (f'{best} a_fit', RES[best]['a']), ('X2 a_fit', RES['X2']['a']), ('X3 a_fit', RES['X3']['a'])]:
    kk = v / AC; print(f'   {k}: {kk:.4f}, |log(k/0.5)| {abs(np.log10(kk / .5)):.3f} [{P(abs(np.log10(kk / .5)) <= .05)}]', flush=True)
print('G2 from the equations: (a) scale from eta (dimensionless dark/gas ratio) and Sigma_gas (HI surface density, set by gas physics and the HI edge column); '
      '(b) scale from sigma/m_chi, m_chi, t_age, gas temperature, rho_gas and the SHMR/NFW halo. rho_DE, Lambda, H appear in none (H enters (b) only through t_age reading r2); native slope 0 [FAIL].', flush=True)
print('G5: dark-mass gravity at measured radii, pass by definition. Cassini: not graded (no gas, so no term at AU scale, in either family).', flush=True)
print(f'\nruntime {time.time() - T0:.0f}s, peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6:.0f} MB', flush=True)
print('Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
