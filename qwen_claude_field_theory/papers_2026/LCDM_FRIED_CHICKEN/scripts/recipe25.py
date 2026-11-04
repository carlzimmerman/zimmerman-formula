"""A23: dipolar dark matter (gravitational polarisation, Blanchet; Blanchet & Le Tiec), per ../FROZEN_A23.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
c_ = 2.998e8; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
EV, OD = GS[::2], GS[1::2]
def cat(gs, f): return np.concatenate([f(g) for g in gs])
LL = lambda gs: cat(gs, lambda g: g.gl)
print(f'cosmology OL {cos.Ode0:.3f}: c sqrt(G rho_DE) {AC:.4e}, lib A0 {A0:.4e} (kappa {A0 / AC:.4f})')
# --- galactic limit: g = g_N + y, g_N = W'(y) - y, u = y/a0, x = g_N/a0
UG = np.linspace(0, 4, 40001)
def taylor_g(gb, a, b):
    f = UG**2 + sum(bk * UG**(k + 3) for k, bk in enumerate(b)); x = gb / a
    reach = np.nonzero(f >= x.max())[0]
    if len(reach) == 0: return None
    j = reach[0] + 1
    if np.any(np.diff(f[:j]) <= 0): return None
    return gb + a * np.interp(x, f[:j], UG[:j])
def pade_g(gb, a, q): return gb + .5 * (-q * gb + np.sqrt(q**2 * gb**2 + 4 * a * gb))
def rms(x): return np.sqrt((x**2).mean())
def fitter(gs, model, x0, lo, hi):
    gb, gt = cat(gs, lambda g: g.gb), LL(gs)
    def res(p):
        gm = model(gb, p)
        return np.full(len(gb), 1.) if gm is None else np.log10(gm) - np.log10(gt)
    best = None
    for s in range(4):
        st = np.array(x0, float) if s == 0 else np.random.default_rng(s).uniform(lo, hi)
        if s == 1: st = np.array(x0, float); st[1:] = 0.
        r = least_squares(res, np.clip(st, np.array(lo) + 1e-6, np.array(hi) - 1e-6), bounds=(lo, hi), x_scale=1., diff_step=1e-4, max_nfev=400)
        if best is None or r.cost < best.cost: best = r
    atb = [i for i, (v, a, b) in enumerate(zip(best.x, lo, hi)) if min(v - a, b - v) < 1e-3 * (b - a)]
    return best.x, atb
def run(tag, model, x0, lo, hi, nk):
    p, atb = fitter(GS, model, x0, lo, hi); cur = [model(g.gb, p) for g in GS]
    if any(c is None for c in cur): print(f'\n== {tag}: best-fit W not invertible on some galaxy; FAIL'); return None
    e1 = grade(tag, cur, f'({nk} knobs; p = {np.round(p, 4).tolist()}; a0 = {10**p[0]:.4e}; at bound {atb})')
    ph, _ = fitter(EV, model, p, lo, hi); gu = [model(g.gb, ph) for g in OD]
    ho = rms(np.log10(np.concatenate(gu)) - np.log10(LL(OD))) if all(c is not None for c in gu) else np.inf
    per = np.array([rms(np.log10(model(g.gb, p)) - np.log10(g.gl)) for g in GS]); d = np.log10(np.concatenate(cur)) - np.log10(ALLL)
    b = np.floor(np.log10(ALLB) * 2) / 2; e3 = max(abs(d[b == x].mean()) for x in np.unique(b) if (b == x).sum() >= 50)
    ok = e1 <= .02 and np.percentile(per, 95) <= .04 and e3 <= .02 and ho <= .025
    print(f' holdout: tuned on GS[::2] p = {np.round(ph, 4).tolist()}; unseen rms to law {ho:.4f} [{"PASS" if ho <= .025 else "FAIL"} holdout]; ALL E1-E3 + holdout: {"PASS" if ok else "FAIL"}')
    return dict(p=p, ok=ok, e1=e1, ho=ho)
# (a) paper's own truncated W, a0 one knob
print('\n### (a) paper-truncated W = W0 + 2 pi G Pi^2 + (16 pi^2 G^2/3 a0) Pi^3 taken as exact: g = g_N + sqrt(a0 g_N)')
ra = run('(a) cubic W, a0 global', lambda gb, p: pade_g(gb, 10**p[0], 0.), [np.log10(A0)], [-11], [-9], 1)
gbo = ALLB; aobs = 10**minimize_scalar(lambda x: ((np.log10(pade_g(gbo, 10**x, 0.)) - np.log10(ALLO))**2).sum(), bounds=(-12, -8), method='bounded').x
print(f' diagnostic: cubic W a0 fitted to observed {aobs:.4e} ({np.log10(aobs / A0):+.3f} dex vs lib A0); rms to observed {rms(np.log10(pade_g(gbo, aobs, 0.)) - np.log10(ALLO)):.4f}; law with A0 rms to observed {rms(np.log10(ALLL) - np.log10(ALLO)):.4f}')
# (b) W freedom
print('\n### (b) W(P) freedom')
first = None; RT = {}
for n in range(3, 9):
    nb = n - 2; x0 = [np.log10(A0)] + [1.] * nb
    r = run(f'(b) T_{n} Taylor W\' = y + y^2/a0 + sum_k=3..{n} b_k y^k/a0^(k-1)', lambda gb, p: taylor_g(gb, 10**p[0], p[1:]), x0, [-11] + [-5] * nb, [-9] + [5] * nb, 1 + nb)
    RT[n] = r
    if r is not None and r['ok'] and first is None: first = n
print(f'\nT_n first passing order: {first} ({"none up to 8" if first is None else f"{first - 1} knobs: a0 + {first - 2} coefficients"})')
rp = run('(b) P Pade one-parameter (q=0 cubic, q=1 law)', lambda gb, p: pade_g(gb, 10**p[0], p[1]), [np.log10(A0), .5], [-11, -1], [-9, 2], 2)
grade('(b) control: the law as a W, W\' = y/(1 - y/a0), a0 = A0 (one function choice, 0 tuned)', [pade_g(g.gb, A0, 1.) for g in GS])
gs_ = G * Msun / (9.58 * 1.496e11)**2
print(f'\ndiagnostic (not a gate) Saturn g_N {gs_:.3e}: y/g_N cubic {np.sqrt(A0 * gs_) / gs_:.2e}; law {(pade_g(gs_, A0, 1.) - gs_) / gs_:.2e}' +
      (f'; best T_{first} {(taylor_g(np.array([gs_]), 10**RT[first]["p"][0], RT[first]["p"][1:])[0] - gs_) / gs_ if taylor_g(np.array([gs_]), 10**RT[first]["p"][0], RT[first]["p"][1:]) is not None else float("nan"):.2e}' if first else ''))
# (c) swoop
print('\n### (c) Lambda-a0 at face value')
kL = np.sqrt(8 * np.pi / 3) / (2 * np.pi); aL = kL * AC
for lab, k in (('(i) paper alpha 0.8, a0 = a_Lambda/0.8', kL / .8), ('(ii) alpha 1, a0 = a_Lambda', kL)):
    print(f' G1 {lab}: kappa_eff {k:.4f}, {np.log10(k / .5):+.4f} dex [{"PASS" if abs(np.log10(k / .5)) <= .05 else "FAIL"} G1]; a0 {k * AC:.4e}')
ka = 10**ra['p'][0] / AC
print(f' G1 (iii) model as written, a0 = fitted W3 constant (a): kappa_eff {ka:.4f} ({np.log10(ka / .5):+.4f} dex) -- a fit, not a tie; alpha = a_Lambda/a0 = {aL / 10**ra["p"][0]:.3f}')
print(f' alpha implied by lib A0: a_Lambda/A0 = {aL / A0:.3f} (paper quotes ~0.8, provisional)')
print(' G2 slope: as written W0 = Lambda/8 pi G and W3 = 32 pi^2 G^2/a0 are independent constants -> 0 [FAIL G2]; naturalness imposed -> 0.5 [PASS G2 by hand, 1 hand term]')
zr = {z: 1. for z in ZB}
print(' G3 a(z)/a(0) (Lambda and W3 constant, a0 does not follow H): ' + ', '.join(f'{z}: {v:.2f}' for z, v in zr.items()) + f' [{"PASS" if all(ZB[z][0] <= 1 <= ZB[z][1] for z in ZB) else "FAIL"} G3]')
print(' G4 one constant across hosts: universal W coefficient [PASS G4 by construction]; G5 operative at galaxy radii via W3 [PASS G5]')
print(' (c) verdict: NO NATIVE TIE -- relation is an order-of-magnitude naturalness claim, not derived; G2 only by hand; G1 passes only at alpha = 1, not at the paper\'s 0.8')
print('\nNot run: relativistic cosmology of the dipolar medium, CMB, clusters, Solar System with external field, ghost analysis.')
print('Rival language. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
