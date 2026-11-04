"""A41: SIDM gravothermal collapse branch (both branches, per-galaxy choice, parametric model), BEC Thomas-Fermi core,
mixed CDM+FDM and CDM+WDM, per ../FROZEN_A41.md. Rival language, adopts nothing, not a framework result.
kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, json, time, io, resource; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.integrate import cumulative_trapezoid
t00 = time.time()
src = open(os.path.join(HERE, 'recipe21.py'), encoding='utf-8').read(); exec(src[src.index('c_ = 2.998e8'):src.index("head('C0")])
BASE = cos; h0 = .674; MPC = kpc * 1e3
s31 = open(os.path.join(HERE, 'recipe31.py'), encoding='utf-8').read(); exec(s31[s31.index('OR_H2 = 4.18e-5'):s31.index('# ---------- scales')])
HBAR, EV = 1.0546e-34, 1.602e-19
ZS = [0., 1., 1.5, 2.33]; EVO = ['B1', 'B1p', 'B1u', 'B2', 'B3', 'B4']
CK = os.path.join(HERE, 'recipe42.json'); OUT = json.load(open(CK)) if os.path.exists(CK) else {}
class Tee:
    def __init__(s): s.b = io.StringIO()
    def write(s, x): s.b.write(x); sys.__stdout__.write(x)
    def flush(s): sys.__stdout__.flush()
def sec(key, fn):
    if key in OUT: print(OUT[key]['txt'], end=''); print(f' [{key} reprinted from checkpoint]', flush=True); return OUT[key]['val']
    t = Tee(); sys.stdout = t
    try: val = fn()
    finally: sys.stdout = sys.__stdout__
    OUT[key] = dict(txt=t.b.getvalue(), val=val); json.dump(OUT, open(CK, 'w'), default=float); return val
def hd(t): print(f'\n######## {t}  ({time.time() - t00:.0f} s, RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB)', flush=True)
P = lambda b: 'PASS' if b else 'FAIL'
EV_ = np.arange(len(GS)) % 2 == 0  # GS[::2] mask
def rmsS(S, cur): return float(np.sqrt((np.concatenate([np.log10(c) - np.log10(g.gl) for g, c in zip(S, cur)])**2).mean()))
def pgr(g, c): return float(np.sqrt(((np.log10(c) - np.log10(g.gl))**2).mean()))
def gr(tag, cur, extra=''):
    grade(tag, cur, extra); gt = np.concatenate(cur); d = np.log10(gt) - np.log10(ALLL); ob = np.log10(gt) - np.log10(ALLO)
    per = np.array([pgr(g, c) for g, c in zip(GS, cur)]); b = np.floor(np.log10(ALLB) * 2) / 2
    e3 = max(abs(d[b == x].mean()) for x in np.unique(b) if (b == x).sum() >= 50)
    return dict(e1=float(np.sqrt((d**2).mean())), e2=float(np.percentile(per, 95)), e3=float(e3), obs=float(np.sqrt((ob**2).mean())))
def hold(tag, e): print(f' {tag} holdout: unseen GS[1::2] rms to law {e:.4f} dex [{P(e <= .025)} <= 0.025]', flush=True); return e
def g14(tag, sc, Ms):
    sc = np.asarray(sc, float); ok = np.isfinite(sc) & (sc > 0); lm = np.log10(Ms); sel = ok & (lm >= 11) & (lm <= 12.5)
    ke = np.median(sc[ok]) / AC; g4 = float(np.log10(sc[sel]).std())
    print(f' {tag}: median {np.median(sc[ok]) / A0:.3g} a0, kappa_eff {ke:.4g} [{P(abs(np.log10(ke / .5)) <= .05)} G1]; rms over {sel.sum()} hosts log M200 11-12.5 {g4:.3f} dex [{P(g4 <= .1)} G4]; over all {ok.sum()} {np.log10(sc[ok]).std():.3f} dex', flush=True)
    return dict(ke=float(ke), g4=g4)
SB = np.array([np.log10(g.Mb / (g.Rd / kpc)**2) for g in GS]); M0S = np.array([m200_of(g.Ms) for g in GS]); MMED = float(np.median(M0S))
ZERO = lambda r: np.full_like(r, 1e-30)

# ================= (a) SIDM: isothermal Jeans with both branches =================
NRH = 40; DRH = np.linspace(0, 8, NRH) * np.log(10)
def core2(mb, M, c, fb, sv, T=T10, rhoc=RHOC, rd=None, branch='low'):
    """A19 core() with the rho0 grid extended to 8 dex and a branch choice: 'low' = lowest rho0 root, 'high' = highest."""
    R = (3 * M * Msun / (800 * np.pi * rhoc))**(1 / 3); rs = R / c; rhos = M * Msun / (4 * np.pi * rs**3 * mu(c)); w = 1 - fb
    rN = lambda r: w * rhos / ((r / rs) * (1 + r / rs)**2); mN = lambda r: w * M * Msun * mu(r / rs) / mu(c)
    xs = np.logspace(-4, np.log10(50), 400) * rs; lrN = np.log(rN(xs)); Vmax = np.sqrt(G * M * Msun * mu(2.163) / mu(c) / (2.163 * rs))
    def r1of(s):
        lk = -np.log(np.maximum(sv(s) * T, 1e-300)); return np.exp(np.interp(lk, lrN[::-1], np.log(xs)[::-1]))
    S = Vmax * SG; r1 = r1of(S); r = r1[:, None] * RG[None, :]; B = mb(r)
    lr0 = np.log(rN(r1))[:, None] + DRH[None, :]
    lre, Mm = integ(lr0, S[:, None], r[:, None, :] * np.ones((1, NRH, 1)), B[:, None, :] * np.ones((1, NRH, 1)))
    f = lre - np.log(rN(r1))[:, None]; h = np.log(Mm[..., -1]) - np.log(mN(r1))[:, None]; q = f**2 + h**2
    near = np.argwhere(q < .05)
    if len(near):
        if branch == 'low': j, k = min(near, key=lambda jk: (lr0[jk[0], jk[1]], q[jk[0], jk[1]]))
        else: j, k = max(near, key=lambda jk: (lr0[jk[0], jk[1]], -q[jk[0], jk[1]]))
    else: j, k = np.unravel_index(np.argmin(q), q.shape)
    top = bool(k >= NRH - 2); x = np.array([lr0[j, k], np.log(S[j])]); d = 1e-3
    def F(X):
        ss = np.exp(X[:, 1]); rr1 = r1of(ss); rr = rr1[:, None] * RG[None, :]; le, Mp = integ(X[:, 0], ss, rr, mb(rr))
        return np.stack([le - np.log(rN(rr1)), np.log(Mp[:, -1]) - np.log(mN(rr1))], -1)
    for _ in range(12):
        Fx = F(np.array([x, x + [d, 0], x + [0, d]])); J = np.stack([(Fx[1] - Fx[0]) / d, (Fx[2] - Fx[0]) / d], -1)
        if np.abs(Fx[0]).max() < 1e-3: break
        try: st = -np.linalg.solve(J, Fx[0])
        except np.linalg.LinAlgError: break
        x = x + st * min(1., .5 / max(np.abs(st).max(), 1e-12))
    lr0s, s = x[0], np.exp(x[1])
    r1s = float(r1of(np.array([s]))[0]); rr = r1s * RG; le, Mp = integ(np.array([lr0s]), np.array([s]), rr[None, :], mb(rr)[None, :])
    mis = max(abs(le[0] - np.log(rN(r1s))), abs(np.log(Mp[0, -1] / mN(r1s))))
    out = dict(s=float(s), r1=r1s, mis=float(mis), lr=float(lr0s - np.log(rN(r1s))), top=top)
    if rd is not None: out['md'] = np.where(rd < r1s, np.exp(np.interp(np.log(rd), np.log(rr), np.log(np.maximum(Mp[0], 1e-300)))), mN(rd))
    return out
def jeans(i, g, sm, br, dlm=0., dlc=0.):
    M = M0S[i] * 10**dlm; c = float(cflat(M0S[i], 0., 0.)) * 10**dlc; fb = min(g.Mb / M, .5)
    o = core2(MBF[i], M, c, fb, svm(sm), rd=g.r, branch=br); return g.gb + G * o['md'] / g.r**2, o
SMJ = [.5, 1., 3., 10., 30.]
JE = {}
def sec_a01():
    hd('(a) precompute: isothermal Jeans cores, base halo, both branches, sigma/m in {0.5, 1, 3, 10, 30} cm^2/g')
    for sm in SMJ:
        for br in ('low', 'high'): JE[(sm, br)] = [jeans(i, g, sm, br) for i, g in enumerate(GS)]
        lo, hi = JE[(sm, 'low')], JE[(sm, 'high')]
        dist = sum(abs(h[1]['lr'] - l[1]['lr']) > .5 for l, h in zip(lo, hi)); top = sum(h[1]['top'] for h in hi)
        um = [sum(o[1]['mis'] > .03 * np.log(10) for o in JE[(sm, b)]) for b in ('low', 'high')]
        print(f'  sigma/m {sm}: rms to law low {rmsS(GS, [o[0] for o in lo]):.4f}, high {rmsS(GS, [o[0] for o in hi]):.4f}; high root distinct (|d ln rho0| > 0.5) in {dist} of 171; '
              f'high roots at grid top {top}; unmatched low {um[0]}, high {um[1]}; median ln(rho0/rho_N(r1)) low {np.median([o[1]["lr"] for o in lo]):.2f}, high {np.median([o[1]["lr"] for o in hi]):.2f}  ({time.time() - t00:.0f} s)', flush=True)
    hd('a0 control: low branch, sigma/m 1, base halo, against A19 C0 0.1200')
    r = gr('a0 control', [o[0] for o in JE[(1., 'low')]]); print(f' a0 {P(abs(r["e1"] - .12) <= .005)}: |{r["e1"]:.4f} - 0.1200| = {abs(r["e1"] - .12):.4f} <= 0.005')
    hd('a1 collapsed (high-density) branch, one constant sigma/m from the grid')
    rr = {sm: rmsS(GS, [o[0] for o in JE[(sm, 'high')]]) for sm in SMJ}; s1 = min(rr, key=rr.get)
    out = JE[(s1, 'high')]; ra1 = gr(f'a1 collapsed branch, sigma/m {s1}', [o[0] for o in out], '(1 knob, from grid)')
    sc1 = [o[1]['s']**2 / o[1]['r1'] for o in out]; t1 = g14('a1 K1 sigma0^2/r1', sc1, M0S)
    s1t = min(SMJ, key=lambda s: rmsS([g for g, e in zip(GS, EV_) if e], [o[0] for o, e in zip(JE[(s, 'high')], EV_) if e]))
    h1 = hold(f'a1 (sigma/m {s1t} on GS[::2])', rmsS(GS[1::2], [o[0] for o in JE[(s1t, 'high')][1::2]]))
    print(' a1 per-sigma rms (high branch): ' + ', '.join(f'{s}: {v:.4f}' for s, v in rr.items()))
    hd('a2 per-galaxy branch choice (171 binary + 1)')
    best = None
    for sm in SMJ:
        ch = [min((JE[(sm, b)][i] for b in ('low', 'high')), key=lambda o: pgr(g, o[0])) for i, g in enumerate(GS)]
        e = rmsS(GS, [o[0] for o in ch]); nh = sum(pgr(g, JE[(sm, 'high')][i][0]) < pgr(g, JE[(sm, 'low')][i][0]) for i, g in enumerate(GS))
        print(f'  sigma/m {sm}: per-galaxy branch rms {e:.4f}, collapsed chosen in {nh} of 171')
        if best is None or e < best[0]: best = (e, sm, ch, nh)
    ra2 = gr(f'a2 per-galaxy branch, sigma/m {best[1]}', [o[0] for o in best[2]], f'(172 parameters; collapsed in {best[3]})')
    t2 = g14('a2 K1 sigma0^2/r1', [o[1]['s']**2 / o[1]['r1'] for o in best[2]], M0S)
    TH = np.concatenate([[-np.inf], np.sort(SB) + 1e-9, [np.inf]])
    def rule(sm, th, sel): return [JE[(sm, 'high' if SB[i] > th else 'low')][i][0] for i in range(len(GS)) if sel[i]]
    def ruletune(sel):
        S = [g for g, s in zip(GS, sel) if s]; return min(((rmsS(S, rule(sm, th, sel)), sm, th) for sm in SMJ for th in TH[::2]), key=lambda t: t[0])
    ea, sma, tha = ruletune(np.ones(len(GS), bool))
    rra = gr(f'a2 rule: collapsed if log Sigma_b > {tha:.3f}, sigma/m {sma}', rule(sma, tha, np.ones(len(GS), bool)), '(2 knobs)')
    et, smt, tht = ruletune(EV_); h2 = hold(f'a2 rule (sigma/m {smt}, threshold {tht:.3f} on GS[::2])', rmsS(GS[1::2], rule(smt, tht, ~EV_)))
    print(f' a2 rule collapsed in {int((SB > tha).sum())} of 171')
    rulethr = {}
    for sm in (.5, 3., 10.):
        S = [g for g, s in zip(GS, EV_) if s]; rulethr[str(sm)] = float(min(((rmsS(S, rule(sm, th, EV_)), th) for th in TH[::2]), key=lambda t: t[0])[1])
    return dict(s1=s1, ra1=ra1, t1=t1, h1=h1, s2=best[1], ra2=ra2, t2=t2, rra=rra, sma=sma, tha=float(tha), h2=h2, smt=smt, tht=float(tht), rulethr=rulethr,
                k1rule=dict(sm=sma))
A01 = sec_a01()
if not JE:  # restart: rebuild JE for later use
    for sm in SMJ:
        for br in ('low', 'high'): JE[(sm, br)] = [jeans(i, g, sm, br) for i, g in enumerate(GS)]

def sec_a3():
    hd('a3 Ren-style per-galaxy M200, c, with per-galaxy branch; sigma/m in {0.5, 3, 10} (514 parameters)')
    def pgj(i, g, sm, br):
        fn = lambda k: np.log10(jeans(i, g, sm, br, k[0], k[1])[0]) - np.log10(g.gl)
        r = least_squares(fn, [0., 0.], bounds=([-.6, -.22], [.6, .22]), max_nfev=8, diff_step=.05); y, o = jeans(i, g, sm, br, *r.x); return y, o, r.x
    RES = {}
    for sm in (.5, 3., 10.):
        ch = []
        for i, g in enumerate(GS):
            a, b = pgj(i, g, sm, 'low'), pgj(i, g, sm, 'high'); ch.append((a, 'low') if pgr(g, a[0]) <= pgr(g, b[0]) else (b, 'high'))
        RES[sm] = ch; e = rmsS(GS, [c[0][0] for c in ch]); ee = rmsS(GS[::2], [c[0][0] for c in ch[::2]])
        print(f'  sigma/m {sm}: rms to law all {e:.4f}, GS[::2] {ee:.4f}; collapsed chosen {sum(c[1] == "high" for c in ch)}  ({time.time() - t00:.0f} s)', flush=True)
    sm = min(RES, key=lambda s: rmsS(GS, [c[0][0] for c in RES[s]])); ch = RES[sm]
    r = gr(f'a3 per-galaxy M200, c, branch; sigma/m {sm}', [c[0][0] for c in ch], '(514 parameters)')
    kk = np.array([c[0][2] for c in ch]); nb = int(np.isclose(abs(kk[:, 0]), .6, atol=6e-4).sum() + np.isclose(abs(kk[:, 1]), .22, atol=2.2e-4).sum())
    print(f' a3 at bound {nb} of 342 continuous; collapsed chosen {sum(c[1] == "high" for c in ch)}; dlogM p16/50/84 {np.round(np.percentile(kk[:, 0], [16, 50, 84]), 3).tolist()}, dlogc {np.round(np.percentile(kk[:, 1], [16, 50, 84]), 3).tolist()}')
    t3 = g14('a3 K1 sigma0^2/r1', [c[0][1]['s']**2 / c[0][1]['r1'] for c in ch], M0S * 10**kk[:, 0])
    smt = min(RES, key=lambda s: rmsS(GS[::2], [c[0][0] for c in RES[s][::2]])); th = A01['rulethr'][str(smt)]
    h = hold(f'a3 gated (sigma/m {smt} on GS[::2], GS[1::2] at prior centre, branch by the GS[::2] rule threshold {th:.3f})',
             rmsS(GS[1::2], [JE[(smt, 'high' if SB[i] > th else 'low')][i][0] for i in range(1, len(GS), 2)]))
    print(f' a3 not gated: GS[1::2] refitted per galaxy at {smt}: {rmsS(GS[1::2], [c[0][0] for c in RES[smt][1::2]]):.4f}')
    return dict(sm=sm, r=r, nb=nb, t3=t3, h=h)
A3 = sec_a3()

# ---- parametric gravothermal model (Yang et al. 2023) ----
def para_m(r, M, c, fb, sm, T=T10, rhoc=RHOC):
    R = (3 * M * Msun / (800 * np.pi * rhoc))**(1 / 3); rs0 = R / c; rhos0 = (1 - fb) * M * Msun / (4 * np.pi * rs0**3 * mu(c))
    tc = (150 / .75) / (sm * .1 * rhos0 * rs0) / np.sqrt(4 * np.pi * G * rhos0); tau = min(T / tc, 1.); L = np.log(tau + .001) / np.log(.001)
    rhos = rhos0 * (2.033 + .7381 * tau + 7.264 * tau**5 - 12.73 * tau**7 + 9.915 * tau**9 + (1 - 2.033) * L)
    rs = rs0 * (.7178 - .1026 * tau + .2474 * tau**2 - .4079 * tau**3 + (1 - .7178) * L)
    rc = rs0 * (2.555 * np.sqrt(tau) - 3.632 * tau + 2.131 * tau**2 - 1.415 * tau**3 + .4683 * tau**4)
    x = np.logspace(np.log10(rs0 * 1e-5), np.log10(max(np.max(r), R) * 1.01), 600); rho = rhos / (((x**4 + rc**4)**.25 / rs) * (1 + x / rs)**2)
    m = cumulative_trapezoid(4 * np.pi * x**3 * rho, np.log(x), initial=0) + 2 * np.pi * rhos * rs * x[0]**2
    return np.exp(np.interp(np.log(r), np.log(x), np.log(m))), tau, 2 * np.pi * G * rhos * rs
def pmod(i, g, k, kind):
    if kind == 'pg': sm, dlm, dlc = k; M = M0S[i] * 10**dlm; c = float(cflat(M0S[i], 0., 0.)) * 10**dlc
    else:
        ls, dn, dc = (list(k) + [0., 0.])[:3]; sm = 10**ls; M = m200_of(g.Ms, dn); c = float(cflat(M, dc, 0.))
    fb = min(g.Mb / M, .5); m, tau, gs = para_m(g.r, M, c, fb, sm); return g.gb + G * m / g.r**2, tau, gs
def fit1(S, ids, f, lo, hi):
    return float(minimize_scalar(lambda x: rmsS(S, [f(i, g, [x]) for i, g in zip(ids, S)]), bounds=(lo, hi), method='bounded', options=dict(xatol=.01)).x)
def fitS(S, ids, f, x0s, lo, hi, nfev=15):
    lo, hi = np.array(lo, float), np.array(hi, float); fn = lambda k: np.concatenate([np.log10(f(i, g, k)) - np.log10(g.gl) for i, g in zip(ids, S)]); best = None
    for x0 in x0s:
        r = least_squares(fn, np.clip(x0, lo + 1e-4, hi - 1e-4), bounds=(lo, hi), max_nfev=nfev, diff_step=.05)
        if best is None or r.cost < best.cost: best = r
    return best.x.tolist()
def atb(x, lo, hi): return [i for i, (v, a, b) in enumerate(zip(x, lo, hi)) if min(v - a, b - v) < 1e-3 * (b - a)]
IA = list(range(len(GS))); IE, IO = IA[::2], IA[1::2]
def pergal(f, x0, lo, hi):
    out = []
    for i, g in enumerate(GS):
        r = least_squares(lambda k: np.log10(f(i, g, k)) - np.log10(g.gl), x0, bounds=(lo, hi), max_nfev=8, diff_step=.05); out.append((f(i, g, r.x), r.x))
    return out
def sec_a4():
    hd('a4 parametric gravothermal SIDM (Yang et al. 2023), dark-only profile, t = 10 Gyr')
    f1 = lambda i, g, k: pmod(i, g, k, 'g')[0]
    sc = [(ls, rmsS(GS, [f1(i, g, [ls]) for i, g in enumerate(GS)])) for ls in np.arange(-1, 2.51, .25)]
    print(' a4-1 scan log sigma/m: ' + ' '.join(f'{a:.2f}:{b:.4f}' for a, b in sc), flush=True)
    j = int(np.argmin([b for _, b in sc])); k1 = fit1(GS, IA, f1, sc[max(j - 1, 0)][0], sc[min(j + 1, len(sc) - 1)][0])
    o1 = [pmod(i, g, [k1], 'g') for i, g in enumerate(GS)]; tau = np.array([o[1] for o in o1])
    r1 = gr(f'a4-1 parametric, sigma/m {10**k1:.3g} cm^2/g', [o[0] for o in o1], f'(1 knob; at bound {atb([k1], [-1], [2.5])})')
    print(f' a4-1 tau: median {np.median(tau):.3f}, > 0.5 in {(tau > .5).sum()}, at the cap 1 in {(tau >= 1).sum()} of 171')
    tk1 = g14('a4-1 K1p 2 pi G rho_s r_s', [o[2] for o in o1], M0S)
    kt = fit1(GS[::2], IE, f1, -1, 2.5); e1h = hold(f'a4-1 (log sigma/m {kt:.3f} on GS[::2])', rmsS(GS[1::2], [f1(i, g, [kt]) for i, g in zip(IO, GS[1::2])]))
    lo, hi = [-1, -.3, -.3], [2.5, .3, .3]
    k3 = fitS(GS, IA, f1, [[k1, 0, 0], [0., 0, 0]], lo, hi); o3 = [pmod(i, g, k3, 'g') for i, g in enumerate(GS)]; tau3 = np.array([o[1] for o in o3])
    r3 = gr('a4-3 parametric + dn, dc', [o[0] for o in o3], f'(3 knobs {np.round(k3, 3).tolist()}, sigma/m {10**k3[0]:.3g}; at bound {atb(k3, lo, hi)})')
    print(f' a4-3 tau: median {np.median(tau3):.3f}, > 0.5 in {(tau3 > .5).sum()}, at cap {(tau3 >= 1).sum()}')
    tk3 = g14('a4-3 K1p', [o[2] for o in o3], [m200_of(g.Ms, k3[1]) for g in GS])
    k3t = fitS(GS[::2], IE, f1, [k3], lo, hi); e3h = hold('a4-3', rmsS(GS[1::2], [f1(i, g, k3t) for i, g in zip(IO, GS[1::2])]))
    PG = {}
    for sm in (1., 10., 30., 100.):
        fp = lambda i, g, k, sm=sm: pmod(i, g, [sm, k[0], k[1]], 'pg')[0]; PG[sm] = pergal(fp, [0., 0.], [-.6, -.22], [.6, .22])
        print(f'  a4-pg sigma/m {sm}: rms all {rmsS(GS, [o[0] for o in PG[sm]]):.4f}, GS[::2] {rmsS(GS[::2], [o[0] for o in PG[sm][::2]]):.4f}  ({time.time() - t00:.0f} s)', flush=True)
    smp = min(PG, key=lambda s: rmsS(GS, [o[0] for o in PG[s]])); kk = np.array([o[1] for o in PG[smp]])
    rp = gr(f'a4-pg per-galaxy M200, c; sigma/m {smp}', [o[0] for o in PG[smp]], '(343 parameters)')
    taup = np.array([pmod(i, g, [smp, *kk[i]], 'pg')[1] for i, g in enumerate(GS)])
    nb = int(np.isclose(abs(kk[:, 0]), .6, atol=6e-4).sum() + np.isclose(abs(kk[:, 1]), .22, atol=2.2e-4).sum())
    print(f' a4-pg at bound {nb} of 342; tau median {np.median(taup):.3f}, > 0.5 in {(taup > .5).sum()}, at cap {(taup >= 1).sum()}')
    smt = min(PG, key=lambda s: rmsS(GS[::2], [o[0] for o in PG[s][::2]]))
    eph = hold(f'a4-pg gated (sigma/m {smt} on GS[::2], prior centre)', rmsS(GS[1::2], [pmod(i, g, [smt, 0., 0.], 'pg')[0] for i, g in zip(IO, GS[1::2])]))
    return dict(k1=k1, r1=r1, tk1=tk1, e1h=e1h, k3=k3, r3=r3, tk3=tk3, e3h=e3h, smp=smp, rp=rp, eph=eph, nb=nb)
A4 = sec_a4()

# ================= (b) BEC Thomas-Fermi core =================
NRC, NRR = 48, 400
def bint(lrc, r, B, Bm, K2):
    rho = np.exp(lrc); m = 4 / 3 * np.pi * rho * r[0]**3; Rh, Ms = [rho], [m]
    for i in range(len(r) - 1):
        dr = r[i + 1] - r[i]; rm = np.sqrt(r[i] * r[i + 1])
        k1r = -G * (B[i] + m) / r[i]**2 / K2; k1m = 4 * np.pi * r[i]**2 * rho
        rh, mh = np.maximum(rho + .5 * dr * k1r, 0), m + .5 * dr * k1m
        rho = np.maximum(rho - dr * G * (Bm[i] + mh) / rm**2 / K2, 0); m = m + dr * 4 * np.pi * rm**2 * rh; Rh.append(rho); Ms.append(m)
    return np.array(Rh).T, np.array(Ms).T
def bec_core(mb, M, c, fb, R, rhoc=RHOC, rd=None):
    R2 = (3 * M * Msun / (800 * np.pi * rhoc))**(1 / 3); rs = R2 / c; rhos = M * Msun / (4 * np.pi * rs**3 * mu(c)); w = 1 - fb
    rN = lambda r: w * rhos / ((r / rs) * (1 + r / rs)**2); mN = lambda r: w * M * Msun * mu(r / rs) / mu(c)
    K2 = 4 * G * R**2 / np.pi; r = np.logspace(np.log10(R * 1e-4), np.log10(R * 1.2), NRR); B = mb(r); Bm = mb(np.sqrt(r[:-1] * r[1:]))
    def ev(lrc):
        Rh, Ms = bint(np.atleast_1d(lrc), r, B, Bm, K2); s = Rh - rN(r)[None, :]; out = []
        for t in range(len(Rh)):
            idx = np.where((s[t, :-1] > 0) & (s[t, 1:] <= 0))[0]
            if not len(idx): out.append((np.nan, np.nan, Ms[t])); continue
            j = idx[-1]; u = s[t, j] / (s[t, j] - s[t, j + 1]); lrt = np.log(r[j]) + u * (np.log(r[j + 1]) - np.log(r[j])); rt = np.exp(lrt)
            mc = np.exp(np.interp(lrt, np.log(r), np.log(np.maximum(Ms[t], 1e-300)))); out.append((np.log(mc) - np.log(mN(rt)), rt, Ms[t]))
        return out
    LR = np.linspace(np.log(rN(R)) - 1, np.log(rN(R * 1e-3)) + 3, NRC); E = ev(LR); hh = np.array([e[0] for e in E])
    k = [j for j in range(NRC - 1) if np.isfinite(hh[j]) and np.isfinite(hh[j + 1]) and np.sign(hh[j]) != np.sign(hh[j + 1])]
    if not k: return None
    a, b = LR[k[0]], LR[k[0] + 1]; ha = hh[k[0]]
    for _ in range(14):
        mid = .5 * (a + b); hm = ev(mid)[0][0]
        if not np.isfinite(hm): break
        if np.sign(hm) == np.sign(ha): a, ha = mid, hm
        else: b = mid
    lrc = .5 * (a + b); h, rt, Ms = ev(lrc)[0]
    if not np.isfinite(h): return None
    mc = np.exp(np.interp(np.log(rt), np.log(r), np.log(np.maximum(Ms, 1e-300)))); out = dict(rt=rt, gc=G * mc / rt**2, lrc=float(lrc), mis=float(abs(h)))
    if rd is not None:
        mi = np.where(rd < r[0], Ms[0] * (rd / r[0])**3, np.exp(np.interp(np.log(rd), np.log(r), np.log(np.maximum(Ms, 1e-300)))))
        out['md'] = np.where(rd < rt, mi, mN(rd))
    return out
NOSOL = [0]
def bmod(i, g, k, kind='g'):
    if kind == 'pg': lR, dlm, dlc = k; M = M0S[i] * 10**dlm; c = float(cflat(M0S[i], 0., 0.)) * 10**dlc
    else: lR, dn, dc = (list(k) + [0., 0.])[:3]; M = m200_of(g.Ms, dn); c = float(cflat(M, dc, 0.))
    fb = min(g.Mb / M, .5); o = bec_core(MBF[i], M, c, fb, 10**lR * kpc, rd=g.r)
    if o is None: NOSOL[0] += 1; return g.gb + G * (1 - fb) * nfw_m(g.r, M, c)[0] / g.r**2, np.nan
    return g.gb + G * o['md'] / g.r**2, o['gc']
def sec_b():
    hd('b0 control: Thomas-Fermi integrator without baryons against rho_c sin(kr)/(kr)')
    R = 1. * kpc; K2 = 4 * G * R**2 / np.pi; r = np.logspace(np.log10(R * 1e-4), np.log10(R * 1.2), NRR); z = np.zeros_like(r)
    Rh, Ms = bint(np.array([np.log(1e-21)]), r, z, z[:-1], K2); k = np.pi / R
    an = lambda x: 4 * np.pi * 1e-21 / k**3 * (np.sin(k * x) - k * x * np.cos(k * x)); errs = [abs(np.interp(x, r, Ms[0]) / an(x) - 1) for x in (R / 2, R)]
    print(f' b0 M(R/2), M(R) relative error {errs[0]:.1e}, {errs[1]:.1e} [{P(max(errs) <= 1e-3)} <= 1e-3]; first zero of rho at {r[np.argmax(Rh[0] <= 0)] / R:.4f} R', flush=True)
    hd('b1 BEC Thomas-Fermi core + NFW envelope, one global knob log10 R/kpc')
    f1 = lambda i, g, k: bmod(i, g, k)[0]
    sc = [(lr, rmsS(GS, [f1(i, g, [lr]) for i, g in enumerate(GS)])) for lr in np.arange(-2, 1.51, .25)]
    print(' b1 scan log R/kpc: ' + ' '.join(f'{a:.2f}:{b:.4f}' for a, b in sc), flush=True)
    j = int(np.argmin([b for _, b in sc])); NOSOL[0] = 0; k1 = fit1(GS, IA, f1, sc[max(j - 1, 0)][0], sc[min(j + 1, len(sc) - 1)][0])
    NOSOL[0] = 0; o1 = [bmod(i, g, [k1]) for i, g in enumerate(GS)]
    r1 = gr(f'b1 BEC, R = {10**k1:.3g} kpc', [o[0] for o in o1], f'(1 knob; at bound {atb([k1], [-2], [1.5])}); no core solution (pure NFW) in {NOSOL[0]} of 171')
    tb1 = g14('b1 K1b G M_core(r_t)/r_t^2', [o[1] for o in o1], M0S)
    kt = fit1(GS[::2], IE, f1, -2, 1.5); eh1 = hold(f'b1 (log R {kt:.3f} on GS[::2])', rmsS(GS[1::2], [f1(i, g, [kt]) for i, g in zip(IO, GS[1::2])]))
    lo, hi = [-2, -.3, -.3], [1.5, .3, .3]
    k3 = fitS(GS, IA, f1, [[k1, 0, 0], [0., 0, 0]], lo, hi); NOSOL[0] = 0; o3 = [bmod(i, g, k3) for i, g in enumerate(GS)]
    r3 = gr('b3 BEC + dn, dc', [o[0] for o in o3], f'(3 knobs {np.round(k3, 3).tolist()}, R {10**k3[0]:.3g} kpc; at bound {atb(k3, lo, hi)}); no core in {NOSOL[0]}')
    tb3 = g14('b3 K1b', [o[1] for o in o3], [m200_of(g.Ms, k3[1]) for g in GS])
    k3t = fitS(GS[::2], IE, f1, [k3], lo, hi); eh3 = hold('b3', rmsS(GS[1::2], [f1(i, g, k3t) for i, g in zip(IO, GS[1::2])]))
    PG = {}
    for lR in sorted(set([round(k1, 3), np.log10(.3), 0., np.log10(3.)])):
        fp = lambda i, g, k, lR=lR: bmod(i, g, [lR, k[0], k[1]], 'pg')[0]; PG[lR] = pergal(fp, [0., 0.], [-.6, -.22], [.6, .22])
        print(f'  b-pg R {10**lR:.3g} kpc: rms all {rmsS(GS, [o[0] for o in PG[lR]]):.4f}, GS[::2] {rmsS(GS[::2], [o[0] for o in PG[lR][::2]]):.4f}  ({time.time() - t00:.0f} s)', flush=True)
    lp = min(PG, key=lambda s: rmsS(GS, [o[0] for o in PG[s]])); kk = np.array([o[1] for o in PG[lp]])
    rp = gr(f'b-pg per-galaxy M200, c; R {10**lp:.3g} kpc', [o[0] for o in PG[lp]], '(343 parameters)')
    nb = int(np.isclose(abs(kk[:, 0]), .6, atol=6e-4).sum() + np.isclose(abs(kk[:, 1]), .22, atol=2.2e-4).sum()); print(f' b-pg at bound {nb} of 342')
    lt = min(PG, key=lambda s: rmsS(GS[::2], [o[0] for o in PG[s][::2]]))
    ehp = hold(f'b-pg gated (R {10**lt:.3g} kpc on GS[::2], prior centre)', rmsS(GS[1::2], [bmod(i, g, [lt, 0., 0.], 'pg')[0] for i, g in zip(IO, GS[1::2])]))
    return dict(k1=k1, r1=r1, tb1=tb1, eh1=eh1, k3=k3, r3=r3, tb3=tb3, eh3=eh3, lp=float(lp), rp=rp, ehp=ehp, nb=nb, b0=errs)
B_ = sec_b()

# ================= (c) mixed dark matter =================
XS = np.concatenate([[0], np.logspace(-4, 4, 4000)]); FS = cumulative_trapezoid(4 * np.pi * XS**2 / (1 + .091 * XS**2)**8, XS, initial=0)
def msol(r, rho0, rc): return rho0 * rc**3 * np.interp(r / rc, XS, FS)
def mixed(i, g, f, kind, x, dn=0., dc=0., dlm=0., dlc=0., sm=None):
    if dlm or dlc: M = M0S[i] * 10**dlm; c = float(cflat(M0S[i], 0., 0.)) * 10**dlc
    else: M = m200_of(g.Ms, dn); c = float(cflat(M, dc, 0.))
    Mhm = 3.8e10 * 10**(-4 / 3 * x) if kind == 'fdm' else 10**x; c *= (1 + 15 * Mhm / M)**(-.3 * f); fb = min(g.Mb / M, .5)
    if sm is not None: o = core2(MBF[i], M, c, fb, svm(sm), rd=g.r); return g.gb + G * o['md'] / g.r**2, np.nan
    R = (3 * M * Msun / (4 * np.pi * 200 * RHOC))**(1 / 3) / kpc; rs = R / c; rhos = (1 - fb) * M / (4 * np.pi * rs**3 * mu(c)); rk = g.r / kpc
    mn = lambda r: (1 - fb) * M * mu(r / rs) / mu(c); m = mn(rk); gc = np.nan
    if kind == 'fdm' and f >= .1:
        m22 = 10**x; rc = 1.6 / m22 * (M / 1e9)**(-1 / 3); rho0 = f**2 * .019e9 / m22**2 / rc**4
        rg = np.logspace(-3, np.log10(R), 300); xx = rg / rs; d = rho0 / (1 + .091 * (rg / rc)**2)**8 - f * rhos / (xx * (1 + xx)**2)
        idx = np.where(d > 0)[0]; rt = rg[idx[-1]] if len(idx) else 0.
        if rt > 0:
            m = (1 - f) * mn(rk) + np.where(rk < rt, msol(rk, rho0, rc), msol(rt, rho0, rc) + f * (mn(rk) - mn(rt)))
            gc = G * msol(rc, rho0, rc) * Msun / (rc * kpc)**2
    return g.gb + G * m * Msun / g.r**2, gc
def mhm_to_mwdm(Mhm):
    rhom = .315 * RHOC; nu = 1.12; hh = cos.h
    def lam(mk): a = .049 * mk**-1.11 * (.265 / .25)**.11 * (hh / .7)**1.22 / hh * MPC; return 2 * np.pi * a * (2**(nu / 5) - 1)**(-1 / (2 * nu))
    return 10**brentq(lambda lm: np.log(4 * np.pi / 3 * rhom * (lam(10**lm) / 2)**3 / Msun / Mhm), -3, 3)
def sec_c():
    hd('(c) control: f = 0 must reproduce R1 base 0.1419')
    e0 = rmsS(GS, [mixed(i, g, 0., 'fdm', 0.)[0] for i, g in enumerate(GS)]); print(f' c control {P(abs(e0 - .1419) <= .001)}: {e0:.4f}')
    R = {}
    hd('c1 CDM + FDM (f, log m22)')
    f2 = lambda i, g, k: mixed(i, g, k[0], 'fdm', k[1])[0]; lo, hi = [0, -1], [1, 2]
    gridv = min(((rmsS(GS, [f2(i, g, [f, lm]) for i, g in enumerate(GS)]), f, lm) for f in (.1, .3, .6, 1.) for lm in (-1, -.5, 0, .5, 1, 2)), key=lambda t: t[0])
    print(f' c1 coarse grid best: f {gridv[1]}, log m22 {gridv[2]}, rms {gridv[0]:.4f}', flush=True)
    k = fitS(GS, IA, f2, [[gridv[1], gridv[2]], [.5, 0.]], lo, hi); o = [mixed(i, g, k[0], 'fdm', k[1]) for i, g in enumerate(GS)]
    R['c1'] = gr('c1 CDM + FDM', [x[0] for x in o], f'(2 knobs f {k[0]:.3f}, m22 {10**k[1]:.3g}; at bound {atb(k, lo, hi)}); soliton present in {sum(np.isfinite(x[1]) for x in o)} of 171')
    tc1 = g14('c1 soliton g_c', [x[1] for x in o], M0S) if sum(np.isfinite(x[1]) for x in o) > 5 else None
    kt = fitS(GS[::2], IE, f2, [k], lo, hi); hc1 = hold('c1', rmsS(GS[1::2], [f2(i, g, kt) for i, g in zip(IO, GS[1::2])])); kc1 = k
    f4 = lambda i, g, k: mixed(i, g, k[0], 'fdm', k[1], k[2], k[3])[0]; lo4, hi4 = [0, -1, -.3, -.3], [1, 2, .3, .3]
    k = fitS(GS, IA, f4, [kc1 + [0, 0], [.5, 0., 0, 0]], lo4, hi4); o = [mixed(i, g, k[0], 'fdm', k[1], k[2], k[3]) for i, g in enumerate(GS)]
    R['c1-4'] = gr('c1-4 CDM + FDM + dn, dc', [x[0] for x in o], f'(4 knobs {np.round(k, 3).tolist()}; at bound {atb(k, lo4, hi4)}); soliton present in {sum(np.isfinite(x[1]) for x in o)}')
    kt = fitS(GS[::2], IE, f4, [k], lo4, hi4); hc14 = hold('c1-4', rmsS(GS[1::2], [f4(i, g, kt) for i, g in zip(IO, GS[1::2])])); kc14 = k
    hd('c2 CDM + WDM (f, log M_hm)')
    w2 = lambda i, g, k: mixed(i, g, k[0], 'wdm', k[1])[0]; lo, hi = [0, 6], [1, 12]
    k = fitS(GS, IA, w2, [[1., 9.9], [.5, 9.]], lo, hi); o = [mixed(i, g, k[0], 'wdm', k[1]) for i, g in enumerate(GS)]
    R['c2'] = gr('c2 CDM + WDM', [x[0] for x in o], f'(2 knobs f {k[0]:.3f}, log M_hm {k[1]:.3f}, m_WDM {mhm_to_mwdm(10**k[1]):.3g} keV (thermal, from memory); at bound {atb(k, lo, hi)})')
    kt = fitS(GS[::2], IE, w2, [k], lo, hi); hc2 = hold('c2', rmsS(GS[1::2], [w2(i, g, kt) for i, g in zip(IO, GS[1::2])])); kc2 = k
    w4 = lambda i, g, k: mixed(i, g, k[0], 'wdm', k[1], k[2], k[3])[0]; lo4, hi4 = [0, 6, -.3, -.3], [1, 12, .3, .3]
    k = fitS(GS, IA, w4, [kc2 + [0, 0], [.5, 9., 0, 0]], lo4, hi4); o = [w4(i, g, k) for i, g in enumerate(GS)]
    R['c2-4'] = gr('c2-4 CDM + WDM + dn, dc', o, f'(4 knobs {np.round(k, 3).tolist()}; at bound {atb(k, lo4, hi4)})')
    kt = fitS(GS[::2], IE, w4, [k], lo4, hi4); hc24 = hold('c2-4', rmsS(GS[1::2], [w4(i, g, kt) for i, g in zip(IO, GS[1::2])]))
    w3 = lambda i, g, k: mixed(i, g, k[0], 'wdm', k[1], sm=10**k[2])[0]; lo3, hi3 = [0, 6, -1], [1, 12, 2]
    k = fitS(GS, IA, w3, [kc2 + [-.26]], lo3, hi3, nfev=12); o = [w3(i, g, k) for i, g in enumerate(GS)]
    R['c2s'] = gr('c2s CDM + WDM + constant SIDM core', o, f'(3 knobs f {k[0]:.3f}, log M_hm {k[1]:.3f}, sigma/m {10**k[2]:.3g}; at bound {atb(k, lo3, hi3)})')
    kt = fitS(GS[::2], IE, w3, [k], lo3, hi3, nfev=8); hc2s = hold('c2s', rmsS(GS[1::2], [w3(i, g, kt) for i, g in zip(IO, GS[1::2])]))
    print(f' ({time.time() - t00:.0f} s)', flush=True)
    for tag, kind, kg in (('c1-pg', 'fdm', kc1), ('c2-pg', 'wdm', kc2)):
        fp = lambda i, g, k, kind=kind, kg=kg: mixed(i, g, kg[0], kind, kg[1], dlm=k[0] + 1e-12, dlc=k[1])[0]; o = pergal(fp, [0., 0.], [-.6, -.22], [.6, .22])
        kk = np.array([x[1] for x in o]); nb = int(np.isclose(abs(kk[:, 0]), .6, atol=6e-4).sum() + np.isclose(abs(kk[:, 1]), .22, atol=2.2e-4).sum())
        R[tag] = gr(f'{tag} per-galaxy M200, c at the {tag[:2]} globals', [x[0] for x in o], f'(343 parameters; at bound {nb} of 342; gated holdout = the {tag[:2]} row holdout)')
    return dict(R=R, kc1=kc1, kc14=kc14, kc2=kc2, h=dict(c1=hc1, c14=hc14, c2=hc2, c24=hc24, c2s=hc2s), tc1=tc1, e0=e0)
C_ = sec_c()

# ================= tie gates: G1, G3, G4, GT, G2z, G2x, G2t, G5 =================
def env2(C, z): e = env(C, z); cc.setCurrent(C); e['age'] = float(C.age(z)); cc.setCurrent(BASE); return e
def cz(e): return 10**np.interp(np.log10(MMED), LM, np.log10(e['cg']))
def zeta(Om): x = Om - 1; return (18 * np.pi**2 + 82 * x - 39 * x**2) / Om
Z0B = zeta(float(cos.Om(0.)))
def dscale(fam, e, p):
    c = cz(e); T = min(10., e['age']) * TY
    if fam in ('Jhigh', 'Jlow'): o = core2(ZERO, MMED, c, 0., svm(p), T=T, rhoc=e['rhoc'], branch=fam[1:].lower()); return o['s']**2 / o['r1']
    if fam == 'para': return para_m(np.array([kpc]), MMED, c, 0., p, T, e['rhoc'])[2]
    if fam == 'bec':
        o = bec_core(ZERO, MMED, c, 0., p * kpc, e['rhoc']); return o['gc'] if o else np.nan
    if fam == 'sol':
        f, lm = p; m22 = 10**lm; rr = (1 + e['z'])**-.5 * (zeta(e['Om']) / Z0B)**(-1 / 6); rc = 1.6 / m22 * (MMED / 1e9)**(-1 / 3) * rr; rho0 = f**2 * .019e9 / m22**2 / rc**4
        return G * msol(rc, rho0, rc) * Msun / (rc * kpc)**2
    if fam == 'k4': R = (3 * 10**p * Msun / (800 * np.pi * e['rhoc']))**(1 / 3); return G * 10**p * Msun / R**2
    if fam.startswith('const'): return p  # particle constant: no cosmological input
def slope(x, y): return float(np.polyfit(np.log(x), np.log(y), 1)[0])
FAMS = {'Jhigh': ('a1 Jeans collapsed-branch core sigma0^2/r1', A01['s1']), 'Jlow': ('a2-rule Jeans cored-branch core at its sigma/m', A01['sma']),
        'para': ('a4-1 parametric 2 pi G rho_s r_s', 10**A4['k1']), 'bec': ('b1 BEC core G M_c/r_t^2', 10**B_['k1']),
        'sol': ('c1 mixed-FDM soliton g_c', tuple(C_['kc1'])), 'k4': ('c2 mixed-WDM g200(M_hm)', C_['kc2'][1]),
        'const_x1': ('K2 G/(sigma/m) at a1', G / (A01['s1'] * .1)), 'const_x4': ('K2 G/(sigma/m) at a4-1', G / (10**A4['k1'] * .1))}
def sec_tie():
    hd('tie gates in A29 backgrounds, footing P (dark-only halo at the median SPARC M200, base halo knobs)')
    print(f' median SPARC M200 {np.log10(MMED):.3f}; per-galaxy G1/G4 lines printed in each row above')
    T = {}; Rr = {}
    for bn, de in BG.items():
        C, s8 = mkP(de); E = {z: env2(C, z) for z in ZS}; r = {z: E[z]['rde'] / E[0.]['rde'] for z in ZS}; Rr[bn] = r
        meas = np.log(max(r.values()) / min(r.values())) >= .1; T[bn] = {}
        print(f'\n {bn}: rho_DE(z)/rho_DE0 ' + ' '.join(f'{r[z]:.4f}' for z in ZB) + f'; age(0) {E[0.]["age"]:.3f} Gyr; G2z {"measurable" if meas else "NOT MEASURABLE"}', flush=True)
        for fam, (lab, p) in FAMS.items():
            a = {z: dscale(fam, E[z], p) for z in ZS}
            if not all(np.isfinite(v) and v > 0 for v in a.values()): print(f'  {fam:9s} scale undefined at some z: {a}'); continue
            rz = {z: a[z] / a[0.] for z in ZB}; dv = {z: float(np.log10(rz[z]) - .5 * np.log10(r[z])) for z in ZB}; gtp = all(abs(v) <= .05 for v in dv.values())
            g3 = all(ZB[z][0] <= rz[z] <= ZB[z][1] for z in ZB); s2 = slope([r[z] for z in ZS], [a[z] for z in ZS]) if meas else None
            T[bn][fam] = dict(rz=rz, dv=dv, GT=gtp, G3=g3, s2=s2, k0=a[0.] / AC)
            print(f'  {fam:9s} {lab}: a(0) {a[0.] / A0:.3g} a0, kappa_eff(dark-only) {a[0.] / AC:.3g}; a(z)/a(0) ' + ' '.join(f'{rz[z]:.3f}' for z in ZB) + f' [{P(g3)} G3]; GT dev '
                  + ' '.join(f'{dv[z]:+.3f}' for z in ZB) + f' [{P(gtp)} GT]; G2z ' + (f'{s2:+.3f} [{P(abs(s2 - .5) <= .05)}]' if meas else 'n/m'), flush=True)
    print('\n G2x pooled over B1, B1p, B1u, B2, B3, B4 (18 points):')
    G2X = {}
    for fam in FAMS:
        try:
            x = [Rr[b][z] for b in EVO for z in ZB]; y = [T[b][fam]['rz'][z] for b in EVO for z in ZB]; G2X[fam] = slope(x, y)
            print(f'  {fam:9s} slope {G2X[fam]:+.4f} [{P(abs(G2X[fam] - .5) <= .05)} G2x]')
        except KeyError: print(f'  {fam:9s} not computable')
    print('\n G2t across rho_DE0 x f in B1 w0, wa (A29 physical footing), z = 0:')
    FSs = [.5, .71, 1., 1.41, 2.]; rows = {fam: [] for fam in FAMS}; rd = []
    for f in FSs:
        wm, wb, wd = .315 * h0**2, .0493 * h0**2, f * .685 * h0**2; h = np.sqrt(wm + wd)
        C, s8 = mkP(BG['B1'], 100 * h, wm / h**2, wb / h**2, R=8. * h / h0); e = env2(C, 0.); rd.append(e['rde'])
        for fam, (lab, p) in FAMS.items(): rows[fam].append(dscale(fam, e, p))
    G2T = {}
    for fam in FAMS:
        if not all(np.isfinite(rows[fam])): print(f'  {fam:9s} undefined in some cosmology'); continue
        G2T[fam] = slope(rd, rows[fam]); print(f'  {fam:9s} slope {G2T[fam]:+.4f} [{P(abs(G2T[fam] - .5) <= .05)} G2t]' + ('  (particle constant: identical values ' + ', '.join(f'{v:.4e}' for v in rows[fam][:2]) + ' ...)' if fam.startswith('const') else ''))
    print('\n G5: halo-gravity scales (Jhigh, Jlow, para, bec, sol, k4) PASS by definition at measured radii; particle constants (const_*) exert no force: FAIL (not operative).')
    mq = HBAR / np.sqrt((10**B_['k1'] * kpc)**3 * .5 * AC) * c_**2 / EV / 1e-22
    print(f' BEC: R is a length; (hbar/m)^2/R^3 = 0.5 c sqrt(G rho_DE) at the b1 R needs m22 = {mq:.3g} (a hand choice; no rho_DE in the particle).')
    return dict(T={b: {f: dict(GT=v['GT'], G3=v['G3'], dv=list(v['dv'].values()), s2=v['s2']) for f, v in d.items()} for b, d in T.items()}, G2X=G2X, G2T=G2T)
TIE = sec_tie()

hd('summary')
rows = [('a0 control low branch sigma/m 1', 0, None, None), ('a1 collapsed branch', 1, A01['ra1'], A01['h1']), ('a2 per-galaxy branch', 172, A01['ra2'], None),
        ('a2 branch rule', 2, A01['rra'], A01['h2']), ('a3 per-galaxy M200, c, branch', 514, A3['r'], A3['h']), ('a4-1 parametric', 1, A4['r1'], A4['e1h']),
        ('a4-3 parametric + dn, dc', 3, A4['r3'], A4['e3h']), ('a4-pg parametric per-galaxy', 343, A4['rp'], A4['eph']), ('b1 BEC R', 1, B_['r1'], B_['eh1']),
        ('b3 BEC R + dn, dc', 3, B_['r3'], B_['eh3']), ('b-pg BEC per-galaxy', 343, B_['rp'], B_['ehp']), ('c1 CDM+FDM', 2, C_['R']['c1'], C_['h']['c1']),
        ('c1-4 CDM+FDM + dn, dc', 4, C_['R']['c1-4'], C_['h']['c14']), ('c2 CDM+WDM', 2, C_['R']['c2'], C_['h']['c2']), ('c2-4 CDM+WDM + dn, dc', 4, C_['R']['c2-4'], C_['h']['c24']),
        ('c2s CDM+WDM + SIDM', 3, C_['R']['c2s'], C_['h']['c2s']), ('c1-pg per-galaxy', 343, C_['R']['c1-pg'], C_['h']['c1']), ('c2-pg per-galaxy', 343, C_['R']['c2-pg'], C_['h']['c2'])]
for t, n, r, h in rows[1:]:
    ex = r['e1'] <= .02 and r['e2'] <= .04 and r['e3'] <= .02 and (h is not None and h <= .025)
    print(f' {t:34s} knobs {n:4d}: E1 {r["e1"]:.4f} E2 {r["e2"]:.4f} E3 {r["e3"]:.4f} obs {r["obs"]:.4f} holdout {("%.4f" % h) if h is not None else "  n/a "} -> {"EXACT" if ex else "NOT EXACT"}')
print(f'\nruntime {time.time() - t00:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB')
print('Rival language; adopts nothing. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
