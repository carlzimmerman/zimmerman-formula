"""A38: dark matter tied to the baryons. (a) dissipative / mirror DM (Foot 2013; Chashchina, Foot & Silagadze 2017),
(b) Famaey, Khoury & Penco 2018 DM-baryon heat balance. Per ../FROZEN_A38.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, json, time, resource; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.integrate import quad, solve_ivp, cumulative_trapezoid
T0 = time.time(); CK = os.path.join(HERE, 'recipe39.json')
OUT = json.load(open(CK)) if os.path.exists(CK) else {}
def ck(k, v): OUT[k] = v; json.dump(OUT, open(CK, 'w'), indent=1, default=float)
c_ = 2.998e8; MPC = kpc * 1e3; RDE0 = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE0); H0SI = cos.H0 * 1e3 / MPC
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
def fitg(fn, x0, lo, hi, gsl, nfev=60, starts=2):
    lg = np.log10(np.concatenate([g.gl for g in gsl]))
    res = lambda k: np.log10(np.concatenate([fn(g, k) for g in gsl])) - lg
    best = None
    for s in range(starts):
        st = np.array(x0, float) if s == 0 else np.random.default_rng(s).uniform(lo, hi)
        r = least_squares(res, np.clip(st, np.array(lo) + 1e-6, np.array(hi) - 1e-6), bounds=(lo, hi), max_nfev=nfev, diff_step=1e-3)
        if best is None or r.cost < best.cost: best = r
    atb = [i for i, (v, a, b) in enumerate(zip(best.x, lo, hi)) if min(v - a, b - v) < 1e-3 * (b - a)]
    return best.x, atb
def hosts():
    return [i for i, g in enumerate(GS) if 11 <= np.log10(m200_of(g.Ms)) <= 12.5]
def g4(cur):
    ai = np.array([np.log10(fit_a(GS[i].gb, cur[i])) for i in hosts()]); return float(ai.std()), float(10**np.median(ai)), len(ai)
print(f'A38 recipe39; sample {len(GS)} galaxies; c sqrt(G rho_DE0) {AC:.4e}; A0 {A0:.4e}', flush=True)
# ======================= (a) Foot dissipative DM =======================
print('\n=== (a) dissipative / mirror DM (Foot 2013; Chashchina, Foot & Silagadze 2017) ===', flush=True)
def fbar(x):  # spherical average of Eq. 11 shape: (1/2) Int exp(-x t) asinh(2t/|1-t^2|) dt
    f = lambda t: np.exp(-x * t) * np.arcsinh(2 * t / max(abs(1 - t * t), 1e-300))
    return .5 * (quad(f, 0, 1, limit=200)[0] + quad(f, 1, np.inf, limit=200)[0])
LX = np.linspace(-4, 3, 351); XX = 10**LX; FB = np.array([fbar(x) for x in XX])
MX = cumulative_trapezoid(XX**3 * FB, LX * np.log(10), initial=0) + XX[0]**3 * FB[0] / 3
print(f'Eq.11 table: x^2 fbar at x=1e3 {XX[-1]**2 * FB[-1]:.4f} (->1), m(x)/x at 1e3 {MX[-1] / XX[-1]:.4f} (->1)', flush=True)
def mtab(x): return np.interp(np.log10(x), LX, MX)
# control C_F: best quasi-isothermal r0/r_D to the spherically averaged Eq. 11 curve over x 0.3-10
xc = np.logspace(np.log10(.3), 1, 80); vF = np.log10(mtab(xc) / xc)
kbest = minimize_scalar(lambda k: ((np.log10((xc - k * np.arctan(xc / k)) / xc) - vF)**2).sum(), bounds=(.2, 10), method='bounded').x
kr = np.sqrt((((np.log10((xc - kbest * np.arctan(xc / kbest)) / xc) - vF))**2).mean())
print(f'control C_F: best quasi-isothermal r0/r_D = {kbest:.3f} (paper ~1.4; consistent window 1.0-2.0: {P(1 <= kbest <= 2)}), rms in log v^2 {kr:.4f} dex', flush=True)
def qiso(g, Sig, k):  # rho0 r0 = Sig [Msun/pc^2], r0 = k R_d
    r0 = k * g.Rd; rho0 = Sig * SIG / r0; x = g.r / r0
    return g.gb + G * 4 * np.pi * rho0 * r0**3 * (x - np.arctan(x)) / g.r**2
def eq11(g, lamR, k):  # lamR in kg/m
    rd = k * g.Rd; x = g.r / rd; return g.gb + G * lamR * mtab(x) / (rd * x**2)
F1f = lambda g, p: qiso(g, 10**p[0], 1.4)
F1bf = lambda g, p: qiso(g, 10**p[0], p[1])
K20 = np.log10(np.sqrt(A0 * 1e10 * Msun / G))
F2f = lambda g, p: eq11(g, 10**p[0] * np.sqrt(g.Mb / 1e10), 1.)
F3f = lambda g, p: eq11(g, 10**p[0] * (g.Mb / 1e10)**p[1], p[2])
RES = {}
cur = [qiso(g, 50., 1.4) for g in GS]; RES['F0'] = show('F0 published 2013 (r0 1.4 R_d, rho0 r0 50 Msun/pc^2)', GS, cur, 0)
sd, am, nh = g4(cur); RES['F0']['g4'] = sd; print(f'  F0 G4 per-galaxy a over {nh} hosts (log M200 11-12.5): rms {sd:.3f} dex [{P(sd <= .1)}], median {am / A0:.3f} A0', flush=True)
ai = np.array([(4 * np.pi * G * 50 * SIG * 1.4 * g.Rd)**2 / (G * g.Mb * Msun) for g in GS])
print(f'  F0 native a_i = (4 pi G Sigma r0)^2/(G M_b): median {np.median(ai) / A0:.3f} A0, rms log {np.log10(ai).std():.3f} dex over 171', flush=True)
for tag, fn, x0, lo, hi in [('F1', F1f, [np.log10(50)], [0], [4]), ('F1b', F1bf, [np.log10(50), 1.4], [0, .2], [4, 10]),
                            ('F2', F2f, [K20], [K20 - 4], [K20 + 4]), ('F3', F3f, [K20, .5, 1.], [K20 - 4, 0, .2], [K20 + 4, 1.5, 10])]:
    if tag in OUT: p, atb, po, atbo = OUT[tag]['p'], OUT[tag]['atb'], OUT[tag]['po'], OUT[tag]['atbo']
    else:
        p, atb = fitg(fn, x0, lo, hi, GS); po, atbo = fitg(fn, x0, lo, hi, EVEN)
        ck(tag, dict(p=list(p), atb=atb, po=list(po), atbo=atbo))
    cur = [fn(g, p) for g in GS]; RES[tag] = show(f'{tag} tuned on all', GS, cur, len(p))
    print(f'  knobs {np.round(p, 4).tolist()} at bound {atb}', flush=True)
    sd, am, nh = g4(cur); RES[tag]['g4'] = sd; print(f'  G4 rms {sd:.3f} dex over {nh} hosts [{P(sd <= .1)}]', flush=True)
    hu = ev(ODD, [fn(g, po) for g in ODD]); RES[tag]['hold'] = hu['e1']
    print(f'  holdout: tuned GS[::2] knobs {np.round(po, 4).tolist()} (at bound {atbo}); unseen GS[1::2] E1 {hu["e1"]:.4f} [{P(hu["e1"] <= .025)}]', flush=True)
    if tag in ('F2', 'F3'):
        K = 10**p[0]; aF = G * K**2 / (1e10 * Msun)
        RES[tag]['aF'] = aF; print(f'  native scale a_F = G K^2/1e10 Msun = {aF:.4e} = {aF / A0:.4f} A0, kappa_eff {aF / AC:.4f}' + (f' (at M_b 1e10; with p={p[1]:.3f} a_i goes as M_b^{2 * p[1] - 1:.3f})' if tag == 'F3' else ''), flush=True)
# per galaxy F4 (lamR_i, k global from F3), F5 (lamR_i, k_i)
k3 = OUT['F3']['p'][2]
if 'F4' not in OUT:
    p4, p5 = [], []
    for g in GS:
        l0 = np.log10(np.sqrt(A0 * g.Mb * Msun / G)); lg = np.log10(g.gl)
        r = least_squares(lambda q: np.log10(eq11(g, 10**q[0], k3)) - lg, [l0], bounds=([l0 - 4], [l0 + 4]), diff_step=1e-4); p4.append(list(r.x))
        r = least_squares(lambda q: np.log10(eq11(g, 10**q[0], q[1])) - lg, [l0, k3], bounds=([l0 - 4, .05], [l0 + 4, 30]), diff_step=1e-4); p5.append(list(r.x))
    ck('F4', p4); ck('F5', p5)
cur4 = [eq11(g, 10**q[0], k3) for g, q in zip(GS, OUT['F4'])]; RES['F4'] = show('F4 per galaxy lamR_i, k global (172 params)', GS, cur4, 172)
cur5 = [eq11(g, 10**q[0], q[1]) for g, q in zip(GS, OUT['F5'])]; RES['F5'] = show('F5 per galaxy lamR_i and k_i (342 params)', GS, cur5, 342)
k5 = np.array([q[1] for q in OUT['F5']]); print(f'  F5 k_i median {np.median(k5):.3f}, 16-84 {np.percentile(k5, 16):.3f}-{np.percentile(k5, 84):.3f}, at bound {int(((k5 < .051) | (k5 > 29.9)).sum())}', flush=True)
aF5 = np.array([G * (10**q[0])**2 / (g.Mb * Msun) for g, q in zip(GS, OUT['F5'])])
print(f'  F5 per-galaxy native a_i = (G lamR_i)^2/(G M_b): median {np.median(aF5) / A0:.3f} A0, rms log {np.log10(aF5).std():.3f} dex', flush=True)
for tag, cc_ in (('F4', cur4), ('F5', cur5)):
    sd, am, nh = g4(cc_); print(f'  {tag} G4 rms {sd:.3f} dex over {nh} hosts', flush=True)
print(f'[{time.time() - T0:.0f}s]', flush=True)
# ======================= (b) Famaey-Khoury-Penco =======================
print('\n=== (b) Famaey, Khoury & Penco 2018 DM-baryon heat balance ===', flush=True)
GK = 4.30091e-6; AU = 3.0857e13  # G in kpc (km/s)^2/Msun; m/s^2 -> (km/s)^2/kpc
def solve_dim(rr, Mbf, rhobf, Ca0, rho0, v02, L):
    """rr kpc array (increasing); Mbf(r) Msun, rhobf(r) Msun/kpc^3; Ca0 (km/s)^2/kpc; returns M_DM(rr), rho, v^2 at rr"""
    rs = min(rr[0], L) * 1e-3; rb0 = rhobf(rs); v0 = np.sqrt(v02)
    y0 = [np.log(rho0), v02, 4 * np.pi / 3 * rho0 * rs**3, Ca0 * rb0 * v0 * rs**3 / 3]
    def f(lr, s):
        r = np.exp(lr); rho = np.exp(s[0]); w = max(s[1], 1e-30); v = np.sqrt(w)
        dw = s[3] / (r**3 * rho * v); dl = -(GK * (s[2] + Mbf(r)) / r**2 + dw) / w
        return [r * dl, r * dw, r * 4 * np.pi * r**2 * rho, r * Ca0 * rhobf(r) * v * r**2]
    so = solve_ivp(f, (np.log(rs), np.log(rr[-1])), y0, t_eval=np.log(rr), method='LSODA', rtol=1e-7, atol=[1e-8, 1e-10 * v02, 1e-12 * rho0 * rs**3, 1e-30])
    if not so.success or so.y.shape[1] != len(rr): return None
    return so.y[2], np.exp(so.y[0]), so.y[1]
# control C_K: nondimensional Eq. 6.5 vs dimensional solver vs simple-IF, exponential baryons, C = 1/16, a0 = 1.2e-10
def solve_nd(R, v02, eps, xs):
    Mbh = lambda x: 1 - (1 + x / 2 * (x + 2)) * np.exp(-x); x0 = 1e-4; v0 = np.sqrt(v02)
    y0 = [np.log(R / 2 * v02), v0, R * x0**3 / 6, v0 / 4 * x0**3 / 3]  # [ln P = ln(q v^2/x^2), v, M, Phi]
    def f(x, s):
        Pq = np.exp(s[0]); v = s[1]; q = Pq * x**2 / v**2
        return [-q * (s[2] + eps * Mbh(x)) / x**4 / Pq, s[3] / (q * v**2 * x), q, v / 4 * x**2 * np.exp(-x)]
    so = solve_ivp(f, (x0, xs[-1]), y0, t_eval=xs, method='LSODA', rtol=1e-8, atol=1e-14)
    return so.y[2], Mbh(xs)
ctl = []
for Mb, L, R, v02 in [(1e8, .5, 5.9, 1.7), (1e9, 1., 5.7, 1.8), (1e10, 2., 5.5, 2.)]:
    C, a0 = 1 / 16, 1.2e-10 * AU; s = np.sqrt(C * a0 * GK * Mb); eps = np.sqrt(GK * Mb / (C * a0 * L**2))
    xs = np.array([.5, 1, 2, 5, 10.]); Mh, Mbh = solve_nd(R, v02, eps, xs); vnd2 = GK * Mb * (Mh / eps + Mbh) / (L * xs)
    Mbf = lambda r: Mb * (1 - (1 + r / L / 2 * (r / L + 2)) * np.exp(-r / L)); rhobf = lambda r: Mb * np.exp(-r / L) / (8 * np.pi * L**3)
    sol = solve_dim(xs * L, Mbf, rhobf, C * a0, R * s / (8 * np.pi * GK * L**2), v02 * s, L); vd2 = GK * (sol[0] + Mbf(xs * L)) / (xs * L)
    gb = GK * Mbf(xs * L) / (xs * L)**2; vl2 = law(gb, a0) * xs * L
    ctl.append((Mb, float(np.abs(np.log10(vd2 / vnd2)).max()), float((vnd2[-1] / vl2[-1])**2 - 1)))
    print(f'control C_K M_b {Mb:.0e} L {L}: dim vs nondim max {ctl[-1][1]:.1e} dex [{P(ctl[-1][1] < 1e-3)}]; V^4(10L)/V^4_simpleIF - 1 = {ctl[-1][2]:+.3f} [{P(abs(ctl[-1][2]) < .1)}]', flush=True)
# SPARC spherical baryons
def bary(g):
    rk = g.r / kpc; Mb = np.maximum.accumulate(np.maximum(g.vb2 * g.r / G / Msun, 1e-6))
    lr, lm = np.log(rk), np.log(Mb); dl = np.gradient(lm, lr); dl = np.clip(dl, 0, None)
    rho = Mb * dl / (4 * np.pi * rk**3); rho0 = 3 * Mb[0] / (4 * np.pi * rk[0]**3)
    def Mbf(r): return Mb[0] * (r / rk[0])**3 if r < rk[0] else float(np.exp(np.interp(np.log(r), lr, lm)))
    def rhobf(r): return rho0 if r < rk[0] else float(np.interp(np.log(r), lr, rho))
    return rk, Mbf, rhobf, Mb[-1]
BAR = [bary(g) for g in GS]
def fkp(i, Ca0, R, v02, full=False):
    g = GS[i]; rk, Mbf, rhobf, Mbt = BAR[i]; L = g.Rd / kpc; s = np.sqrt(Ca0 * GK * Mbt)
    sol = solve_dim(rk, Mbf, rhobf, Ca0, R * s / (8 * np.pi * GK * L**2), v02 * s, L)
    if sol is None: return (g.gl * 10, None) if full else g.gl * 10
    gt = g.gb + GK * sol[0] / rk**2 / AU
    return (gt, sol) if full else gt
IDX = {id(g): i for i, g in enumerate(GS)}
FK = lambda g, p: fkp(IDX[id(g)], 10**p[0], p[1], p[2])
t1 = time.time(); cur = [fkp(i, A0 * AU / 16, 5.7, 1.8) for i in range(len(GS))]
print(f'(one pass over 171 galaxies: {time.time() - t1:.1f}s)', flush=True)
RES['K0'] = show('K0 published (C 1/16, a0 = A0 imposed, R 5.7, v0^2 1.8 for all)', GS, cur, 0)
sd, am, nh = g4(cur); print(f'  K0 G4 rms {sd:.3f} dex over {nh} hosts [{P(sd <= .1)}], median {am / A0:.3f} A0', flush=True)
x0 = [np.log10(A0 * AU / 16), 5.7, 1.8]; lo, hi = [np.log10(1e-13 * AU), .1, .1], [np.log10(1e-8 * AU), 100, 20]
if 'K3' not in OUT:
    p, atb = fitg(FK, x0, lo, hi, GS, nfev=40, starts=1); ck('K3', dict(p=list(p), atb=atb)); print(f'  [K3 all {time.time() - T0:.0f}s]', flush=True)
if 'po' not in OUT['K3']:
    po, atbo = fitg(FK, OUT['K3']['p'], lo, hi, EVEN, nfev=40, starts=1); d = OUT['K3']; d.update(po=list(po), atbo=atbo); ck('K3', d)
p, atb, po, atbo = OUT['K3']['p'], OUT['K3']['atb'], OUT['K3']['po'], OUT['K3']['atbo']
cur = [FK(g, p) for g in GS]; RES['K3'] = show('K3 tuned on all (C a0, R, v0^2 global)', GS, cur, 3)
Ca0 = 10**p[0] / AU; print(f'  knobs {np.round(p, 4).tolist()} at bound {atb}; C a0 = {Ca0:.4e} m/s^2 = {Ca0 / A0:.4f} A0 (with C 1/16: a0 = {16 * Ca0 / A0:.3f} A0); kappa_eff of C a0 {Ca0 / AC:.4f}', flush=True)
sd, am, nh = g4(cur); RES['K3']['g4'] = sd; print(f'  G4 rms {sd:.3f} dex over {nh} hosts [{P(sd <= .1)}]', flush=True)
hu = ev(ODD, [FK(g, po) for g in ODD]); RES['K3']['hold'] = hu['e1']
print(f'  holdout: tuned GS[::2] {np.round(po, 4).tolist()} (at bound {atbo}); unseen GS[1::2] E1 {hu["e1"]:.4f} [{P(hu["e1"] <= .025)}]', flush=True)
# consistency at the last measured radius, K3
tau, sm = [], []
for i, g in enumerate(GS):
    gt, sol = fkp(i, 10**p[0], p[1], p[2], full=True)
    if sol is None: continue
    rk, Mbf, rhobf, _ = BAR[i]; rho, w = sol[1][-1], sol[2][-1]; rb = max(rhobf(rk[-1]), 1e-30)
    tau.append(3 * rho * np.sqrt(w) / (2 * 10**p[0] * rb) * kpc / 1e3)  # (kpc/(km/s)) -> s
    sm.append(Ca0 / (rho * Msun / kpc**3 * w * 1e6) * 10)  # m^2/kg -> cm^2/g
tau, sm = np.array(tau), np.array(sm)
print(f'  K3 at last radius: H0 tau median {np.median(tau * H0SI):.3g}, 16-84 {np.percentile(tau * H0SI, 16):.3g}-{np.percentile(tau * H0SI, 84):.3g}; fraction H0 tau <= 1: {(tau * H0SI <= 1).mean():.3f}', flush=True)
print(f'  K3 FKP sigma/m = C a0/(rho v^2) at last radius: median {np.median(sm):.3g} cm^2/g (16-84 {np.percentile(sm, 16):.3g}-{np.percentile(sm, 84):.3g}); A7 M3 record: 0.63 at g_b = a0, 40 at last point (one exchange in 13 Gyr)', flush=True)
print(f'[{time.time() - T0:.0f}s]', flush=True)
# per galaxy K2g: R_i, v0_i^2 with C a0 from K3
if 'K2g' not in OUT:
    pk = []
    for i, g in enumerate(GS):
        lg = np.log10(g.gl); r = least_squares(lambda q: np.log10(fkp(i, 10**p[0], q[0], q[1])) - lg, [p[1], p[2]], bounds=([.1, .1], [100, 20]), max_nfev=30, diff_step=1e-3)
        pk.append(list(r.x))
    ck('K2g', pk)
pk = np.array(OUT['K2g']); cur = [fkp(i, 10**p[0], *pk[i]) for i in range(len(GS))]
RES['K2g'] = show('K2g per galaxy R_i, v0_i^2 (343 params)', GS, cur, 343)
atk = int(((pk[:, 0] < .101) | (pk[:, 0] > 99.9) | (pk[:, 1] < .101) | (pk[:, 1] > 19.9)).sum())
print(f'  R_i median {np.median(pk[:, 0]):.2f} (16-84 {np.percentile(pk[:, 0], 16):.2f}-{np.percentile(pk[:, 0], 84):.2f}); v0^2 median {np.median(pk[:, 1]):.2f}; galaxies with a knob at bound {atk}', flush=True)
sd, am, nh = g4(cur); print(f'  K2g G4 rms {sd:.3f} dex over {nh} hosts', flush=True)
print(f'[{time.time() - T0:.0f}s]', flush=True)
# ======================= (c) scale, G1-G5, GT in A29 backgrounds =======================
print('\n=== (c) acceleration scale: G1-G5 and GT in the A29 backgrounds ===', flush=True)
s31 = open(os.path.join(HERE, 'recipe31.py'), encoding='utf-8').read(); exec(s31[s31.index('OR_H2 = '):s31.index('S30 = ')])
ZS = [0., 1., 1.5, 2.33]; RD, HZ = {}, {}
for b, de in BG.items():
    C = mk(de, .811); RD[b] = [float(C.rho_de(z) / C.rho_de(0)) for z in ZS]; HZ[b] = [float(C.Hz(z) / C.Hz(0)) for z in ZS]
cc.setCurrent(cos)
psi = lambda z: (1 + z)**2.7 / (1 + ((1 + z) / 2.9)**5.6)  # Madau & Dickinson 2014, from memory
READ = {'flat (Foot r1: lambda, K constant; FKP r1: C a0 constant)': lambda b: [1., 1., 1., 1.],
        'Foot r2: R_SN follows cosmic SFR, a ~ psi^2': lambda b: [(psi(z) / psi(0))**2 for z in ZS],
        'FKP r2: a0 = c H(z)/6': lambda b: HZ[b]}
EVO = ['B1', 'B1p', 'B1u', 'B2', 'B3', 'B4']
for name, fa in READ.items():
    print(f'-- reading {name}', flush=True)
    xs, ys = [], []
    for b in BG:
        ar = fa(b); dev = [np.log10(ar[j]) - .5 * np.log10(RD[b][j]) for j in (1, 2, 3)]
        g3 = all(ZB[z][0] <= ar[j] <= ZB[z][1] for j, z in zip((1, 2, 3), (1., 1.5, 2.33)))
        lnr = np.log(RD[b]); g2z = 'not measurable' if lnr.max() - lnr.min() < .1 else f'{np.polyfit(lnr, np.log(ar), 1)[0]:+.3f}'
        print(f'   {b:4s} rho_DE ratio {RD[b][1]:.3f} {RD[b][2]:.3f} {RD[b][3]:.3f}; a(z)/a(0) {ar[1]:.3f} {ar[2]:.3f} {ar[3]:.3f} [G3 {P(g3)}]; '
              f'GT dev {dev[0]:+.3f} {dev[1]:+.3f} {dev[2]:+.3f} [{P(max(map(abs, dev)) <= .05)}]; G2z {g2z}', flush=True)
        if b in EVO: xs += list(np.log(RD[b][1:])); ys += list(np.log(ar[1:]))
    sl = np.polyfit(xs, ys, 1)[0]; print(f'   G2x pooled slope over {len(xs)} points {sl:+.3f} [{P(abs(sl - .5) <= .05)}]', flush=True)
kh = c_ * H0SI / 6 / AC
print(f'G1 kappa_eff: F2 native a_F {RES["F2"]["aF"] / AC:.4f}; F3 a_F {RES["F3"]["aF"] / AC:.4f}; K3 C a0 {Ca0 / AC:.4f}; FKP r2 cH0/6 {kh:.4f}; '
      f'pooled a_fit F0 {RES["F0"]["a"] / AC:.4f}, K0 {RES["K0"]["a"] / AC:.4f} (a0 = A0 imposed); target 0.5 +- 0.05 dex', flush=True)
for k, v in [('F2 a_F', RES['F2']['aF'] / AC), ('F3 a_F', RES['F3']['aF'] / AC), ('K3 C a0', Ca0 / AC), ('FKP cH0/6', kh), ('F0 a_fit', RES['F0']['a'] / AC), ('K0 a_fit', RES['K0']['a'] / AC)]:
    print(f'   G1 {k}: {v:.4f}, |log(k/0.5)| {abs(np.log10(v / .5)):.3f} [{P(abs(np.log10(v / .5)) <= .05)}]', flush=True)
print('G2 from the equations: Foot scale a_F = G K^2/M (K = lambda R_SN normalisation; lambda from dark photoionisation and cooling cross sections, SN spectrum); '
      'FKP scale C a0 (cross-section normalisation, Eq. 4.1). rho_DE, Lambda, H appear in neither; native slope 0 [FAIL]. a0 = cH0/6 in FKP is an estimate, not derived.', flush=True)
print('G5: both are halo gravity at measured radii, pass by definition. Cassini: not graded (equilibrium on Solar System scales not stated in either source).', flush=True)
print(f'\nruntime {time.time() - T0:.0f}s, peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6:.0f} MB', flush=True)
print('Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
