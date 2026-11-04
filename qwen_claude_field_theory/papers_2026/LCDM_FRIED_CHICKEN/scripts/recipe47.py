"""A46: relativistic MOND (TeVeS, generalised Einstein-aether, AeST), MOG/STVG, conformal gravity, BIMOND, per ../FROZEN_A46.md.
Rival modified-gravity routes, not LCDM. Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, time, resource; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.special import i1e, k1e
T0 = time.time()
s31 = open(os.path.join(HERE, 'recipe31.py'), encoding='utf-8').read(); exec(s31[s31.index('OR_H2 ='):s31.index('S30 =')])  # A29 backgrounds, unchanged
c_ = 2.998e8; MPC = kpc * 1e3; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); LAM = 8 * np.pi * G * RDE / c_**2
H0S = cos.H0 * 1e3 / MPC; ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}; ZS = [0., 1., 1.5, 2.33]
P = lambda b: 'PASS' if b else 'FAIL'
A12 = 1.2e-10
print(f'A46 recipe47; c sqrt(G rho_DE) {AC:.4e} (A0/that {A0 / AC:.4f}); cH0 {c_ * H0S:.4e}; conventional a0 1.2e-10 = {A12 / A0:.3f} A0')
ev, od, al = list(range(0, len(GS), 2)), list(range(1, len(GS), 2)), list(range(len(GS)))
def rl(cur, sel): return np.sqrt(np.mean(np.concatenate([(np.log10(np.maximum(cur[j], 1e-14)) - np.log10(GS[j].gl))**2 for j in sel])))
def fitk(model, x0, lo, hi, sel, tag=''):
    def res(k): return np.concatenate([np.log10(np.maximum(model(GS[j], k), 1e-14)) - np.log10(GS[j].gl) for j in sel])
    best = None
    for s in range(3):
        st = np.array(x0, float) if s == 0 else np.random.default_rng(s).uniform(lo, hi)
        r = least_squares(res, np.clip(st, np.array(lo) + 1e-6 * (np.array(hi) - np.array(lo)), np.array(hi) - 1e-6 * (np.array(hi) - np.array(lo))), bounds=(lo, hi), max_nfev=60)
        if best is None or r.cost < best.cost: best = r
    atb = [i for i, (v, a, b) in enumerate(zip(best.x, lo, hi)) if min(v - a, b - v) < 1e-3 * (b - a)]
    return best.x, atb
def run_free(tag, model, x0, lo, hi, show):
    k, atb = fitk(model, x0, lo, hi, al); ke, _ = fitk(model, x0, lo, hi, ev)
    grade(f'{tag}, tuned on all', [np.maximum(model(g, k), 1e-14) for g in GS], f'({len(k)} knobs: {show(k)}; at bound {atb})')
    hu = rl([model(g, ke) for g in GS], od); print(f' holdout: tuned on GS[::2] ({show(ke)}); unseen rms to law on GS[1::2] {hu:.4f} [{P(hu <= .025)}]')
    return k
# ---------------- (a) relativistic MOND ----------------
def tev(gb, a): return gb + np.sqrt(a * gb)                         # Bekenstein mu_0 inverted exactly
def mu_al(x, al_): return 2 * x / (1 + (2 - al_) * x + np.sqrt((1 - al_ * x)**2 + 4 * x))
def g_alpha(gb, a, al_):  # solve g mu_alpha(g/a) = gb by bisection in log g; alpha = 0 is the slowest (largest g)
    lo, hi = np.log(gb), np.log(gb + np.sqrt(a * gb) + 1e-3 * gb)
    for _ in range(60):
        m = .5 * (lo + hi); gm = np.exp(m); f = gm * mu_al(gm / a, al_) - gb; lo = np.where(f < 0, m, lo); hi = np.where(f < 0, hi, m)
    return np.exp(.5 * (lo + hi))
def g_n(gb, a, n): y = gb / a; return gb * ((1 + np.sqrt(1 + 4 * y**-n)) / 2)**(1 / n)
print('\n(a) relativistic MOND')
grade('TV0 TeVeS published function (alpha = 0): g_b + sqrt(a0 g_b), a0 1.2e-10, 0 knobs', [tev(g.gb, A12) for g in GS])
ktv = run_free('TV1 TeVeS function, a0 free', lambda g, k: tev(g.gb, 10**k[0]), [-10.], [-12.], [-8.], lambda k: f'a0 {10**k[0]:.4e} = {10**k[0] / A0:.4f} A0')
grade('GE0 GEA example (simple mu, a0 = M = 1.2e-10), 0 knobs', [law(g.gb, A12) for g in GS])
kge = run_free('GE1 GEA example, M free', lambda g, k: law(g.gb, 10**k[0]), [-10.], [-12.], [-8.], lambda k: f'a0 {10**k[0]:.4e} = {10**k[0] / A0:.4f} A0')
chk = np.max(np.abs(g_alpha(ALLB, A0, 0.) / tev(ALLB, A0) - 1)), np.max(np.abs(g_alpha(ALLB, A0, 1.) / law(ALLB, A0) - 1))
print(f'\n check: alpha-family bisection vs closed forms, max rel err alpha=0 {chk[0]:.1e}, alpha=1 {chk[1]:.1e}')
run_free('AE F-alpha (alpha-family, a0 and alpha free, alpha in [0,1])', lambda g, k: g_alpha(g.gb, 10**k[0], k[1]), [-10., .5], [-12., 0.], [-8., 1.], lambda k: f'a0 {10**k[0] / A0:.4f} A0, alpha {k[1]:.4f}')
run_free('AE F-n (n-family, a0 and n free, n in [0.5,4])', lambda g, k: g_n(g.gb, 10**k[0], k[1]), [-10., 1.5], [-12., .5], [-8., 4.], lambda k: f'a0 {10**k[0] / A0:.4f} A0, n {k[1]:.4f}')
run_free('AE n = 2 standard mu, a0 free', lambda g, k: g_n(g.gb, 10**k[0], 2.), [-10.], [-12.], [-8.], lambda k: f'a0 {10**k[0] / A0:.4f} A0')
rC = []
for g in GS:
    rM = np.sqrt(G * g.mbtot / A0); rC.append(g.r[-1] / (rM * MPC**2)**(1 / 3))
rC = np.array(rC); print(f'\n AeST diagnostic, mu^-1 = 1 Mpc: r_last/r_C median {np.median(rC):.3f}, max {rC.max():.3f} (oscillation beyond r_C; {(rC > .5).sum()} galaxies with r_last > 0.5 r_C)')
# ---------------- (b) MOG ----------------
NSH = 2000
for g in GS:
    M = g.vb2 * g.r / G; e = np.union1d(np.linspace(0, g.r[-1], NSH + 1), g.r); Me = np.interp(e, np.r_[0., g.r], np.r_[0., M])
    g.sh_s = .5 * (e[1:] + e[:-1]); g.sh_dm = np.diff(Me)
def gyuk(r, s, dm, mu):  # Yukawa e^-mu d/d attraction (inward positive) at radii r from shells (s, dm)
    R = r[:, None]; S = s[None, :]; ms = mu * S; mr = mu * R
    out = (np.exp(mu * (S - R)) - np.exp(-mu * (S + R))) / 2 / ms * (1 + mr) / R**2
    inn = -(np.exp(mu * (R - S)) * (mr - 1) + np.exp(-mu * (R + S)) * (mr + 1)) / 2 / ms / R**2  # e^-ms [mr cosh mr - sinh mr]/(ms R^2), outward
    return G * ((np.where(R > S, out, inn)) * dm[None, :]).sum(1)
def mog(g, al_, mu_kpc): mu = mu_kpc / kpc; return (1 + al_) * g.gb - al_ * gyuk(g.r, g.sh_s, g.sh_dm, mu)
# check the shell machinery: mu -> 0 limit gives the Newtonian shell sum; point-mass test
g0 = GS[0]; nchk = gyuk(g0.r, g0.sh_s, g0.sh_dm, 1e-8 / kpc) / g0.gb
rr = np.array([1., 5., 20.]) * kpc; pm = gyuk(rr, np.array([1e-3 * kpc]), np.array([1e10 * Msun]), .042 / kpc); x = .042 * rr / kpc
print(f'\n(b) MOG; shell check: mu->0 Yukawa/Newton on {g0.n} ratio {nchk.min():.4f}-{nchk.max():.4f}; point-mass vs (1+x)e^-x: ' + ' '.join(f'{v:.6f}' for v in pm / (G * 1e10 * Msun / rr**2) / ((1 + x) * np.exp(-x))))
_mg = [mog(g, 8.89, .042) for g in GS]; print(f' MG0 points with g <= 0 (floored at 1e-14 in grade, disclosed deviation): {sum(int((m <= 0).sum()) for m in _mg)}')
grade('MG0 MOG universal alpha 8.89, mu 0.042 /kpc, 0 knobs (M/L fixed 0.5/0.7)', [np.maximum(m, 1e-14) for m in _mg])
kmg = run_free('MG2 MOG alpha, mu free', lambda g, k: mog(g, k[0], 10**k[1]), [8.89, np.log10(.042)], [0., -3.], [50., np.log10(2.)], lambda k: f'alpha {k[0]:.3f}, mu {10**k[1]:.4f} /kpc')
# disc vs sphere diagnostic
Md, Rd = 1e10 * Msun, 3 * kpc; Rr = (np.arange(1200) + .5) * 15 * Rd / 1200; dR = Rr[1] - Rr[0]; NPH = 720; ph = (np.arange(NPH) + .5) * 2 * np.pi / NPH
Sig = Md / (2 * np.pi * Rd**2) * np.exp(-Rr / Rd); dmr = Sig * Rr * dR * 2 * np.pi / NPH
RF = np.array([1., 2., 3., 5., 8., 12., 20., 30.]) * kpc + .37 * dR
gNd, gYd = [], []
for Rf in RF:
    dx = Rf - Rr[:, None] * np.cos(ph)[None, :]; d = np.sqrt(Rf**2 + Rr[:, None]**2 - 2 * Rf * Rr[:, None] * np.cos(ph)[None, :])
    w = dmr[:, None] * dx / d**3; gNd.append(G * w.sum()); gYd.append(G * (w * (1 + .042 / kpc * d) * np.exp(-.042 / kpc * d)).sum())
gNd, gYd = np.array(gNd), np.array(gYd); bd = (1 + 8.89) - 8.89 * gYd / gNd
Me = gNd * RF**2 / G; e = np.linspace(0, RF[-1], 4001); Mi = np.interp(e, np.r_[0., RF], np.r_[0., Me]); ss = .5 * (e[1:] + e[:-1])
bs = (1 + 8.89) - 8.89 * gyuk(RF, ss, np.diff(Mi), .042 / kpc) / gNd
print(' DIAG disc vs sphere (1e10 Msun thin exp disc, R_d 3 kpc, universal alpha mu): R kpc ' + ' '.join(f'{v / kpc:.1f}' for v in RF))
print('  boost g_MOG/g_N thin disc   ' + ' '.join(f'{v:.3f}' for v in bd)); print('  boost spherical shells      ' + ' '.join(f'{v:.3f}' for v in bs))
print('  log10 sphere/disc boost     ' + ' '.join(f'{np.log10(a / b):+.3f}' for a, b in zip(bs, bd)))
# ---------------- (c) conformal gravity ----------------
CM_ = 1e-2; GST, GAM0, KAP = 5.42e-41 / CM_, 3.06e-30 / CM_, 9.54e-54 / CM_**2
NNEG = [0]
def cg(g, gs, g0, kp, Nst):
    xx = g.r / (2 * g.Rd); gl = Nst * gs * c_**2 * xx * i1e(xx) * k1e(xx)
    out = g.gb + gl + g0 * c_**2 / 2 - kp * c_**2 * g.r; NNEG[0] += int((out <= 0).sum()); return out
print(f'\n(c) conformal gravity; gamma* c^2/2 per Msun {GST * c_**2 / 2:.3e}, gamma0 c^2/2 {GAM0 * c_**2 / 2:.3e} m/s^2 = {GAM0 * c_**2 / 2 / A0:.4f} A0, kappa c^2 x 10 kpc {KAP * c_**2 * 10 * kpc / A0:.4f} A0')
NNEG[0] = 0; grade('CGs conformal gravity published gamma*, gamma0, kappa; N* = stars only, 0 knobs', [cg(g, GST, GAM0, KAP, g.Ms) for g in GS]); print(f' points with g <= 0 floored: {NNEG[0]}')
NNEG[0] = 0; grade('CGb same, N* = stars + 1.33 M_HI, 0 knobs', [cg(g, GST, GAM0, KAP, g.Mb) for g in GS]); print(f' points with g <= 0 floored: {NNEG[0]}')
NNEG[0] = 0
kcg = run_free('CG3 gamma*, gamma0, kappa free (N* = stars + gas)', lambda g, k: cg(g, 10**k[0] / CM_, 10**k[1] / CM_, k[2] * 1e-52 / CM_**2, g.Mb), [np.log10(5.42e-41), np.log10(3.06e-30), .954], [-43., -32., 0.], [-38., -28., 10.],
               lambda k: f'gamma* {10**k[0]:.3e} cm^-1, gamma0 {10**k[1]:.3e} cm^-1, kappa {k[2] * 1e-52:.3e} cm^-2')
print(f' (floored points counted over all CG3 evaluations, incl. random starts: {NNEG[0]})'); NNEG[0] = 0; _ = [cg(g, 10**kcg[0] / CM_, 10**kcg[1] / CM_, kcg[2] * 1e-52 / CM_**2, g.Mb) for g in GS]; print(f' floored points at the CG3 best fit: {NNEG[0]}')
# ---------------- tie gates ----------------
def rde_J(OLx, H0x): Hs = H0x * 1e3 / MPC; return OLx * 3 * Hs**2 / (8 * np.pi * G)
COS = [(.70, 67.4), (.685, 73.), (.65, 73.)]; r0 = rde_J(*COS[0])
def slopes(aJ): return [np.log(aJ[i] / aJ[0]) / np.log(rde_J(*COS[i]) / r0) for i in (1, 2)]
M2 = np.array([m200_of(g.Ms) for g in GS]); sel = (np.log10(M2) >= 11) & (np.log10(M2) <= 12.5)
gsat = 1.327e20 / (9.537 * 1.496e11)**2; rsat = 9.537 * 1.496e11; THR = 1e-3 * A0; gN10 = G * 1e10 * Msun / (10 * kpc)**2
def kap(a): ke = a / AC; return f'kappa_eff {ke:.4f} ({np.log10(ke / .5):+.3f} dex) [{P(abs(np.log10(ke / .5)) <= .05)} G1]'
def g4(curves):
    ae = np.array([fit_a(g.gb, c) for g, c in zip(GS, curves)]); sp = np.log10(ae[sel]).std(); return ae, f'per-galaxy effective a over {sel.sum()} hosts median {np.median(ae[sel]) / A0:.3f} A0, rms {sp:.3f} dex [{P(sp <= .1)} G4]'
print(f'\nTIE GATES (A13 G1-G5, A24/A37 rules); Saturn g_N {gsat:.3e}, threshold {THR:.2e}')
hJ = [h for _, h in COS]; sH = slopes([h for h in hJ])
print(f' constants as written (TeVeS l, GEA M, AeST a0, MOG alpha mu, CG gamma0, BIMOND a0): slope 0 [FAIL G2]; a(z)/a(0) 1.000 at z 1, 1.5, 2.33 [PASS G3]')
print(f' GEA reading a0 ~ cH0 (and CG curvature reading c H0 sqrt(Omega_k), Omega_k held): slopes {sH[0]:+.3f} {sH[1]:+.3f} [{P(all(abs(s - .5) <= .05 for s in sH))} G2]')
_, t4 = g4([tev(g.gb, A12) for g in GS]); bt = np.sqrt(A12 * gsat)
print(f'TV0 TeVeS alpha=0 at 1.2e-10: {kap(A12)}; {t4}; G5 boost at 10 kpc {np.sqrt(A12 * gN10) / A0:.2f} a0 [{P(np.sqrt(A12 * gN10) >= .1 * A0)}]; Saturn anomaly sqrt(a0 g_N) {bt:.2e} = {bt / A0:.1f} a0 [{P(bt < THR)} Cassini] -> NO TIE (slope 0)')
print(f'TV1 fitted a0 {10**ktv[0] / A0:.4f} A0: {kap(10**ktv[0])} (a fit, not a tie)')
_, t4 = g4([law(g.gb, A12) for g in GS]); bl = 2 * A12 * gsat / (np.sqrt(gsat**2 + 4 * A12 * gsat) + gsat)
print(f'GE0 GEA simple mu at 1.2e-10: {kap(A12)}; {t4}; Saturn anomaly {bl:.2e} = {bl / A0:.2f} a0 [{P(bl < THR)} Cassini] (same as the bare-law control)')
print(f'GE1 fitted M {10**kge[0] / A0:.4f} A0: {kap(10**kge[0])} (a fit of the law, not a tie); GEA a0 ~ cH0: {kap(c_ * H0S)}; AeST remark a0 ~ cH0/6: {kap(c_ * H0S / 6)}')
mg0 = [np.maximum(mog(g, 8.89, .042), 1e-14) for g in GS]; ae, t4 = g4(mg0); xs = .042 / kpc * rsat; bm = 8.89 * (xs**2 / 2 - xs**3 / 3) * gsat; x10 = .42; b5 = 8.89 * (1 - (1 + x10) * np.exp(-x10)) * gN10
print(f'MG0 MOG universal: {t4}; median effective a {kap(np.median(ae[sel]))}; G2 slope 0 (alpha, mu constants, no cosmology link in S5) [FAIL]; G3 flat [PASS]; G5 boost at 10 kpc {b5 / A0:.3f} a0 [{P(b5 >= .1 * A0)}]; Saturn anomaly {bm:.2e} = {bm / A0:.1e} a0 [{P(bm < THR)} Cassini]')
print(f'   MOG effective a vs host: Spearman with log Mb over hosts {__import__("scipy.stats", fromlist=["x"]).spearmanr(np.log10([g.Mb for g in GS])[sel], np.log10(ae[sel]))[0]:+.3f}; natural accelerations: c^2 mu {c_**2 * .042 / kpc / A0:.2e} A0')
cgb = [cg(g, GST, GAM0, KAP, g.Mb) for g in GS]; ae, t4 = g4(cgb); a0c = GAM0 * c_**2 / 2; b5c = GST * 1e10 * c_**2 / 2 + a0c - KAP * c_**2 * 10 * kpc
bc = GST * c_**2 / 2 + a0c - KAP * c_**2 * rsat; bc1 = GST * c_**2 / 2 - KAP * c_**2 * rsat
OK_ = (c_ * np.sqrt(GAM0**2 / 4) / H0S)**2
print(f'CGb conformal gravity: gamma0 c^2/2 {kap(a0c)}; {t4}; median effective a {kap(np.median(ae[sel]))}; G5 boost at 10 kpc {b5c / A0:.3f} a0 [{P(b5c >= .1 * A0)}]; Saturn anomaly with gamma0 term {bc:.2e} = {bc / A0:.3f} a0 [{P(abs(bc) < THR)} Cassini]; without gamma0 {bc1:.2e} = {bc1 / A0:.1e} a0 [{P(abs(bc1) < THR)}]')
print(f'   curvature reading gamma0/2 = sqrt(-K): Omega_k = (c sqrt(-K)/H0)^2 = {OK_:.2e}; physical curvature ~ (1+z): a(z)/a(0) 2.000 2.500 3.330 [FAIL G3]')
for M0 in (1., 8 * np.pi / .25):
    a_b = c_**2 * np.sqrt(LAM / M0); print(f'BIMOND Lambda = a0^2 |M(0)|/c^4 at |M(0)| = {M0:.2f}: a0 {a_b / A0:.3f} A0, {kap(a_b)}; slope 0.5 only with M(0) held fixed (free additive constant as written: 0)')
print(f'   |M(0)| needed for kappa 1/2 = 32 pi = {32 * np.pi:.1f}; with lib A0: {c_**4 * LAM / A0**2:.1f}')
# ---------------- GT in A29 backgrounds ----------------
print('\nGT in A29 backgrounds: FLAT (a constant), HZ (a ~ H(z), GEA hand reading), CURV (1+z, CG curvature reading), HAND (a ~ sqrt(rho_DE), BIMOND inverted with M(0) fixed)')
for bn, de in BG.items():
    C = mk(de, .811); cc.setCurrent(C)
    r = {z: C.rho_de(z) / C.rho_de(0.) for z in ZS}; H = {z: C.Hz(z) / C.Hz(0.) for z in ZS}; meas = np.log(max(r.values()) / min(r.values())) >= .1
    R = {'FLAT': {z: 1. for z in ZS}, 'HZ': H, 'CURV': {z: 1 + z for z in ZS}, 'HAND': {z: np.sqrt(r[z]) for z in ZS}}
    print(f' {bn} {de.get("w0", "")} {de.get("wa", "")}: rho_DE(z)/rho_DE0 ' + ' '.join(f'{r[z]:.4f}' for z in ZB) + f'; G2z {"measurable" if meas else "NOT MEASURABLE"}')
    for k, a in R.items():
        dv = {z: np.log10(a[z]) - .5 * np.log10(r[z]) for z in ZB}; gtp = all(abs(v) <= .05 for v in dv.values()); g3 = all(ZB[z][0] <= a[z] <= ZB[z][1] for z in ZB)
        s2 = float(np.polyfit(np.log([r[z] for z in ZS]), np.log([a[z] for z in ZS]), 1)[0]) if meas else None
        print(f'  {k:4s} a(z)/a(0) ' + ' '.join(f'{a[z]:.4f}' for z in ZB) + f' [{P(g3)} G3]; GT dev ' + ' '.join(f'{dv[z]:+.4f}' for z in ZB) + f' [{P(gtp)} GT]; G2z ' + (f'{s2:+.4f} [{P(abs(s2 - .5) <= .05)}]' if meas else 'not measurable'))
    cc.setCurrent(cos)
print(f'\nruntime {time.time() - T0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB (macOS bytes)')
print('Rival modified-gravity routes, not LCDM. Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
