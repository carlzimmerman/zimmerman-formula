"""A30 post-result diagnostic (NOT a gate, written after seeing KA1 pass E1-E3): why the k-mouflage shape fit works and what it costs.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
c_ = 2.998e8; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); EV, OD = GS[::2], GS[1::2]
def rms(x): return np.sqrt((np.asarray(x)**2).mean())
def kmy(gN, b2, a_s, n):
    S = b2 * np.asarray(gN, float); lS, la = np.log(S), np.log(a_s); lo = lS - np.logaddexp(0, 2 * n * (lS - la)); hi = lS.copy()
    for _ in range(70):
        m = .5 * (lo + hi); f = m + np.logaddexp(0, 2 * n * (m - la)) - lS; hi = np.where(f > 0, m, hi); lo = np.where(f > 0, lo, m)
    return np.exp(.5 * (lo + hi))
KA1 = (10**.4254, 10**-.8991 * A0, .9671)       # recipe32.out KA1 knobs
b, a_s, n = KA1; gst = a_s / (2 * b**2)
print(f'KA1: beta {b:.3f}, a_s {a_s:.3e}, n {n:.4f} (m = {n + 1:.3f}); switch g_* {gst:.3e}; SPARC points with g_b < g_* (unscreened): {(ALLB < gst).sum()} of {len(ALLB)}; min g_b {ALLB.min():.3e}')
print(f' screened asymptote y = (2 beta^2 a_s^(2n) g_N)^(1/(2n+1)), power 1/(2n+1) = {1 / (2 * n + 1):.4f}')
# D1 pure power law control: g = g_b + A g_b^s, 2 knobs
def pl(gs, p): return [g.gb + 10**p[0] * (g.gb / A0)**p[1] * A0 for g in gs]
def fitpl(gs):
    gt = np.concatenate([g.gl for g in gs]); return least_squares(lambda p: np.log10(np.concatenate(pl(gs, p))) - np.log10(gt), [0., .4]).x
p = fitpl(GS); grade('D1 pure power law g_b + A g_b^s (2 knobs)', pl(GS, p), f'(A {10**p[0]:.4f} a0, s {p[1]:.4f})')
ph = fitpl(EV); print(f' D1 holdout unseen {rms(np.log10(np.concatenate(pl(OD, ph))) - np.log10(np.concatenate([g.gl for g in OD]))):.4f}')
yl = ALLL - ALLB; s_loc = np.polyfit(np.log10(ALLB), np.log10(yl), 1)[0]; print(f' law y = g_law - g_b: best single power over SPARC {s_loc:.4f}; local slope at g_b/a0 = 0.01, 0.1, 1, 10: ' +
      ', '.join(f'{(lambda x: (np.log(law(x * 1.01 * A0) - x * 1.01 * A0) - np.log(law(x * A0) - x * A0)) / np.log(1.01))(x):.3f}' for x in (.01, .1, 1, 10)))
# D2 KA1 against the law outside SPARC's range
print('\nD2 KA1 versus the law away from SPARC (g_N in m/s^2; ratio of total g):')
for gN in (1e-14, 1e-13, 1e-12, 1e-11, 1e-10, 1e-9, 1e-8, 1e-6, GMS_ := 1.327e20 / (9.58 * 1.496e11)**2):
    gk = gN + kmy([gN], 2 * b**2, a_s, n)[0]; print(f' g_N {gN:.2e}: KA1/law {gk / law(gN):.4f} ({np.log10(gk / law(gN)):+.3f} dex)')
# D3 the tie bookkeeping
aK = np.sqrt(16 * np.pi) * b * AC; lam = (aK / a_s)**(2 * n); print(f'\nD3 with M^4 = rho_DE: a_K {aK:.3e}, lambda = m K0 = (a_K/a_s)^(2n) = {lam:.3e}, K0 = {lam / (n + 1):.3e}')
aKneed = a_s * (n + 1)**(1 / (2 * n)); print(f' with K0 = 1: M^4/rho_DE = (a_K needed/a_K(rho_DE))^2 = {(aKneed / aK)**2:.3e}')
# D4 cosmology-allowed coupling: beta fixed 0.1 and 0.2, a_s and n fitted
for bf in (.1, .2):
    gt = ALLL
    def res(q): return np.log10(np.concatenate([g.gb + kmy(g.gb, 2 * bf**2, 10**q[0] * A0, q[1]) for g in GS])) - np.log10(gt)
    r = least_squares(res, [0., 2.], bounds=([-4, .25], [4, 10]), diff_step=1e-3)
    grade(f'D4 beta fixed {bf}', [g.gb + kmy(g.gb, 2 * bf**2, 10**r.x[0] * A0, r.x[1]) for g in GS], f'(2 knobs; log a_s/a0 {r.x[0]:.3f}, n {r.x[1]:.3f})')
# D5 canonical m = 3 (n = 2) and m = 2 (n = 1): beta, a_s fitted
for nf in (1., 2.):
    def res(q): return np.log10(np.concatenate([g.gb + kmy(g.gb, 2 * (10**q[0])**2, 10**q[1] * A0, nf) for g in GS])) - np.log10(ALLL)
    r = least_squares(res, [.4, -1.], bounds=([-2, -4], [1.5, 4]), diff_step=1e-3)
    grade(f'D5 n fixed {nf} (m = {nf + 1:.0f})', [g.gb + kmy(g.gb, 2 * (10**r.x[0])**2, 10**r.x[1] * A0, nf) for g in GS], f'(2 knobs; beta {10**r.x[0]:.3f}, log a_s/a0 {r.x[1]:.3f})')
# D6 Earth-Moon, Earth's field alone (Sun's background gradient not superposed, stated)
gM = 3.986e14 / 3.844e8**2; yM = kmy([gM], 2 * b**2, a_s, n)[0]; print(f'\nD6 KA1 at the Moon from the Earth alone: y/g_N {yM / gM:.2e} (y {yM:.2e} m/s^2); the law there: (g_law - g_N)/g_N {(law(gM) - gM) / gM:.2e}')
print('\nPost-result diagnostic only; no gate changes. Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
