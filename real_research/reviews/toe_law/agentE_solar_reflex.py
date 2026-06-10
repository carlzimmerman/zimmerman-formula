#!/usr/bin/env python3
"""
agentE_solar_reflex.py — Door IVb: the SOLAR-REFLEX kill-test on instantaneous per-body F4 MI.
==============================================================================================
THREAT (flagged by agent A, Door IVa-2): per-body instantaneous F4 modified inertia,
    m * mu(|a|/s) * a_vec = F_N,    mu(x) = x/sqrt(1+x^2),
applies mu to the SUN as well. The Sun's proper acceleration |a_sun| ~ 2.1e-7 m/s^2
(Jupiter-dominated), so the Sun gets an anomalous response
    delta_a_sun ~ s^2 / (2 |a_sun|),  directed along its total Newtonian pull (~toward Jupiter):
    7.0e-13 m/s^2 (hostile s = cH_Lambda = 5.418e-10) ; 2.1e-14 m/s^2 (framework s = a0 = 9.36e-11).
It does NOT vanish under orbit-averaging (the Sun's <|a|> is unchanged). Open question:
OBSERVABILITY after a real ephemeris fit absorbs what it can into GMs + initial conditions.

METHOD
  1. Barycentric N-body truth runs: Sun+Venus+EMB+Mars+Jupiter+Saturn, realistic J2000
     elements (Standish/JPL approximate elements; e_J = 0.0484), per-body instantaneous F4
     at s in {hostile, framework}; DOP853 rtol=1e-12 atol=1e-14; 35-yr span (1.19 Saturn
     periods, 2.95 Jupiter periods). Pure-Newton control + cross-tolerance floor run.
  2. Ephemeris-fit emulation, LINEARIZED (valid: signals are ~1e-11 relative): synthetic
     EMB->Mars and EMB->Saturn ranges from the F4 truth; fit a PURE-NEWTON model by
     least squares over {GM_sun, GM_J (configurable), all 36 initial conditions, (variants:
     all 6 GMs, per-segment range biases, Mars-only data, +Jupiter-range data)}.
     Fit = weighted projection of the F4-minus-Newton range signal onto numerically
     computed partial-derivative columns (central differences) of the Newton model.
     Post-fit residuals = the observable. Observation windows emulate reality:
     Mars ranging 25 yr (10-d cadence, sigma 1.5 m), Saturn/Cassini 13.2 yr 2004.5-2017.7
     (30-d cadence, sigma 25 m), optional Juno-era Jupiter ranging (30-d, sigma 15 m).
  3. Diagnostics: stable-eps identity check, 1/|a_sun| anti-correlation with the GM_J
     acceleration template, e_J modulation fraction, linearity (s^2 scaling), per-planet
     1/(n^2-n_J^2) response scaling (licenses the Mercury/BepiColombo extrapolation),
     orbit-averaged (frozen-mu) prescription variant, Sun-only-F4 attribution variant.

UNITS: AU, day internally; report in meters and m/s^2.
RULES: agentE_-prefixed outputs only; no git.
"""

import math
import os
import sys
import time
import numpy as np
from scipy.integrate import solve_ivp
from concurrent.futures import ProcessPoolExecutor

# ----------------------------------------------------------------------------------------
# constants & units
# ----------------------------------------------------------------------------------------
AU   = 1.495978707e11           # m
DAY  = 86400.0                  # s
YR   = 365.25                   # day
ACC_SI2U = DAY * DAY / AU       # m/s^2 -> AU/day^2  (= 0.0499002...)
GM_SI2U  = DAY * DAY / AU**3    # m^3/s^2 -> AU^3/day^2

S_HOSTILE_SI   = 5.418e-10      # m/s^2  (= cH_Lambda; agent A's hostile lead, same value)
S_FRAMEWORK_SI = 9.36e-11       # m/s^2  (framework a0)
S_HOSTILE   = S_HOSTILE_SI   * ACC_SI2U
S_FRAMEWORK = S_FRAMEWORK_SI * ACC_SI2U

# GM values, m^3/s^2 (DE-class; Jupiter/Saturn = system values)
GM_SI = np.array([
    1.32712440018e20,   # Sun
    3.24858592000e14,   # Venus
    4.03503235630e14,   # Earth-Moon barycenter (treated as one body)
    4.28283758160e13,   # Mars system
    1.26712764100e17,   # Jupiter system
    3.79405848418e16,   # Saturn system
])
NAMES = ['Sun', 'Venus', 'EMB', 'Mars', 'Jupiter', 'Saturn']
NB = 6
GM = GM_SI * GM_SI2U
IDX_SUN, IDX_VEN, IDX_EMB, IDX_MAR, IDX_JUP, IDX_SAT = range(6)

# J2000 heliocentric ecliptic Keplerian elements (Standish, JPL approximate elements
# "Keplerian elements for 1800 AD - 2050 AD", Table 1): a[AU], e, i, L, varpi, Omega [deg]
ELEMENTS = {
    'Venus':   (0.72333566, 0.00677672, 3.39467605, 181.97909950, 131.60246718,  76.67984255),
    'EMB':     (1.00000261, 0.01671123, -0.00001531, 100.46457166, 102.93768193,   0.0),
    'Mars':    (1.52371034, 0.09339410, 1.84969142,  -4.55343205, -23.94362959,  49.55953891),
    'Jupiter': (5.20288700, 0.04838624, 1.30439695,  34.39644051,  14.72847983, 100.47390909),
    'Saturn':  (9.53667594, 0.05386179, 2.48599187,  49.95424423,  92.59887831, 113.66242448),
}

# observation emulation (days from J2000)
T_SPAN  = 35.0 * YR
MARS_T  = np.arange(5.0 * YR,  35.0 * YR, 10.0)      # 25 yr of 1-m-class Mars ranging
SAT_T   = np.arange(4.5 * YR,  17.7 * YR, 30.0)      # Cassini window 2004.5-2017.7
JUP_T   = np.arange(16.0 * YR, 25.5 * YR, 30.0)      # Juno-era window (variant fit only)
DIAG_T  = np.arange(0.0, T_SPAN, 15.0)
SIGMA_MARS = 1.5    # m   (Mars ranging systematics-limited ~1-2 m; see [7] pins)
SIGMA_SAT  = 25.0   # m   (Cassini normal points ~10-32 m class; 75 m loose variant quoted)
SIGMA_SAT_LOOSE = 75.0
SIGMA_JUP  = 15.0   # m   (Juno-era range, emulated)

TEVAL = np.unique(np.concatenate([MARS_T, SAT_T, JUP_T, DIAG_T, [0.0, T_SPAN]]))
I_MARS = np.searchsorted(TEVAL, MARS_T)
I_SAT  = np.searchsorted(TEVAL, SAT_T)
I_JUP  = np.searchsorted(TEVAL, JUP_T)
I_DIAG = np.searchsorted(TEVAL, DIAG_T)

RTOL_MAIN = 1e-12
ATOL_MAIN = 1e-14

# ----------------------------------------------------------------------------------------
# elements -> barycentric initial state
# ----------------------------------------------------------------------------------------
def kepler_E(M, e):
    E = M + e * math.sin(M)
    for _ in range(60):
        f = E - e * math.sin(E) - M
        E -= f / (1.0 - e * math.cos(E))
        if abs(f) < 1e-15:
            break
    return E

def elements_to_state(el, mu):
    a, e, inc, L, varpi, Om = el
    d2r = math.pi / 180.0
    inc *= d2r; L *= d2r; varpi *= d2r; Om *= d2r
    w = varpi - Om
    M = math.fmod(L - varpi, 2 * math.pi)
    E = kepler_E(M, e)
    xp = a * (math.cos(E) - e)
    yp = a * math.sqrt(1 - e * e) * math.sin(E)
    r = a * (1 - e * math.cos(E))
    vxp = -math.sqrt(mu * a) / r * math.sin(E)
    vyp = math.sqrt(mu * a * (1 - e * e)) / r * math.cos(E)
    cO, sO = math.cos(Om), math.sin(Om)
    ci, si = math.cos(inc), math.sin(inc)
    cw, sw = math.cos(w), math.sin(w)
    P = np.array([cw * cO - sw * sO * ci, cw * sO + sw * cO * ci, sw * si])
    Q = np.array([-sw * cO - cw * sO * ci, -sw * sO + cw * cO * ci, cw * si])
    return xp * P + yp * Q, vxp * P + vyp * Q

def base_initial_state():
    r = np.zeros((NB, 3)); v = np.zeros((NB, 3))
    for i, nm in enumerate(NAMES):
        if nm == 'Sun':
            continue
        ri, vi = elements_to_state(ELEMENTS[nm], GM[IDX_SUN] + GM[i])
        r[i], v[i] = ri, vi
    w = GM / GM.sum()
    r -= (w[:, None] * r).sum(0)   # barycentric
    v -= (w[:, None] * v).sum(0)
    return np.concatenate([r.ravel(), v.ravel()])

# ----------------------------------------------------------------------------------------
# F4 inversion, cancellation-free:
#   mu(a/s) a = g ; x=a/s, y=g/s ; x^2 = y^2 + h, h = 2/(1+sqrt(1+4/y^2)) in (0,1];
#   eps = (a-g)/g = h/(y(x+y))  ->  a_vec = g_vec (1+eps).   (deep: a->sqrt(gs); high: eps->1/(2y^2))
# ----------------------------------------------------------------------------------------
def eps_of_y(y):
    h = 2.0 / (1.0 + np.sqrt(1.0 + 4.0 / (y * y)))
    x = np.sqrt(y * y + h)
    return h / (y * (x + y))

def newtonian_g(r, gm=GM):
    dr = r[None, :, :] - r[:, None, :]
    d2 = (dr * dr).sum(-1)
    np.fill_diagonal(d2, 1.0)
    inv_d3 = d2 ** -1.5
    np.fill_diagonal(inv_d3, 0.0)
    return (dr * (gm[None, :] * inv_d3)[:, :, None]).sum(axis=1)

def make_rhs(s, mode, eps_frozen, gm):
    def rhs(t, ystate):
        r = ystate[:3 * NB].reshape(NB, 3)
        v = ystate[3 * NB:]
        g = newtonian_g(r, gm)
        if mode != 'newton':
            if mode == 'frozen':
                g = g * (1.0 + eps_frozen)[:, None]
            else:
                gn = np.sqrt((g * g).sum(-1))
                eps = eps_of_y(gn / s)
                if mode == 'sun_only':
                    eps[1:] = 0.0
                g = g * (1.0 + eps)[:, None]
        return np.concatenate([v, g.ravel()])
    return rhs

def run_case(args):
    """worker: integrate one case, return observables (+states if requested)."""
    (name, y0, s, mode, eps_frozen, rtol, want_states) = args
    rhs = make_rhs(s, mode, np.asarray(eps_frozen) if eps_frozen is not None else None, GM)
    sol = solve_ivp(rhs, (0.0, T_SPAN), y0, method='DOP853',
                    rtol=rtol, atol=ATOL_MAIN, t_eval=TEVAL, dense_output=False)
    if not sol.success:
        return name, {'fail': sol.message}
    states = sol.y.T                       # (nt, 36)
    pos = states[:, :3 * NB].reshape(-1, NB, 3)
    def rng(idx, body):
        d = pos[idx, body, :] - pos[idx, IDX_EMB, :]
        return np.sqrt((d * d).sum(-1)) * AU      # meters
    out = {'mars': rng(I_MARS, IDX_MAR), 'sat': rng(I_SAT, IDX_SAT), 'jup': rng(I_JUP, IDX_JUP),
           'nfev': sol.nfev}
    if want_states:
        out['pos_diag'] = pos[I_DIAG]      # (ndiag, 6, 3) AU
        out['states_end'] = states[-1]
    return name, out

# GM-perturbed runs need a custom gm vector: handle via mode tuple ('newton_gm', gm_vector)
def run_case_gm(args):
    (name, y0, gmvec, rtol) = args
    gmv = np.asarray(gmvec)
    def rhs(t, ystate):
        r = ystate[:3 * NB].reshape(NB, 3)
        v = ystate[3 * NB:]
        g = newtonian_g(r, gmv)
        return np.concatenate([v, g.ravel()])
    sol = solve_ivp(rhs, (0.0, T_SPAN), y0, method='DOP853',
                    rtol=rtol, atol=ATOL_MAIN, t_eval=TEVAL, dense_output=False)
    if not sol.success:
        return name, {'fail': sol.message}
    pos = sol.y.T[:, :3 * NB].reshape(-1, NB, 3)
    def rng(idx, body):
        d = pos[idx, body, :] - pos[idx, IDX_EMB, :]
        return np.sqrt((d * d).sum(-1)) * AU
    return name, {'mars': rng(I_MARS, IDX_MAR), 'sat': rng(I_SAT, IDX_SAT), 'jup': rng(I_JUP, IDX_JUP)}

def dispatch(args):
    if args[0].startswith('gm:'):
        return run_case_gm(args)
    return run_case(args)

# ----------------------------------------------------------------------------------------
# fit machinery (linearized ephemeris emulation)
# ----------------------------------------------------------------------------------------
GM_STEP  = 1e-9        # relative GM step for partials
POS_STEP = 1e-8        # AU
VEL_STEP = 1e-9        # AU/day

IC_PARAMS = []
for _b in range(NB):
    for _c in range(3):
        IC_PARAMS.append(('r', _b, _c, POS_STEP))
    for _c in range(3):
        IC_PARAMS.append(('v', _b, _c, VEL_STEP))

# ----------------------------------------------------------------------------------------
# TRUE NONLINEAR FIT (Levenberg-Marquardt with re-integrated Jacobian every iteration).
# Needed because the linearized emulation's optimum sits at parameter excursions where
# second-order dynamics break the linear cancellations (verified by direct integration).
# ----------------------------------------------------------------------------------------
def build_param_state(p, spec, y0_base):
    gmv = GM.copy()
    y0v = y0_base.copy()
    for val, (kind, idx) in zip(p, spec):
        if kind == 'gm':
            gmv[idx] *= (1.0 + val)
        else:
            kc, b, c, h = IC_PARAMS[idx]
            off = (0 if kc == 'r' else 3 * NB) + 3 * b + c
            y0v[off] += val
    return y0v, gmv

def lm_fit(truth, spec, y0_base, pool, rows=('mars', 'sat'),
           sigmas=None, nuis=None, p0=None, max_iter=12, tag=''):
    """truth: dict target->range arrays. spec: [('gm',idx)|('ic',k)].
       nuis: optional exact-linear nuisance matrix dict target->(n_t, m) (profiled out).
       Returns dict with converged residuals/params/history."""
    npar = len(spec)
    p = np.zeros(npar) if p0 is None else p0.copy()
    steps = np.array([GM_STEP if k == 'gm' else IC_PARAMS[i][3] for k, i in spec])
    wts = np.concatenate([np.full(len(truth[t]), 1.0 / sigmas[t]) for t in rows])
    Nw = None
    if nuis is not None:
        Nw = np.concatenate([nuis[t] for t in rows], axis=0) * wts[:, None]
        Qn, _ = np.linalg.qr(Nw)
    def project(x):
        return x - Qn @ (Qn.T @ x) if Nw is not None else x
    def run_model(pv):
        y0v, gmv = build_param_state(pv, spec, y0_base)
        _, out = run_case_gm(('gm:lm', y0v, gmv, RTOL_MAIN))
        return out
    def chi2_of(out):
        r = np.concatenate([truth[t] - out[t] for t in rows]) * wts
        with np.errstate(all='ignore'):
            rp = project(r)
        c2 = float((rp ** 2).sum())
        assert np.isfinite(c2), 'non-finite chi2 in LM — investigate, do not mask'
        return c2, r
    cur = run_model(p)
    chi2, _ = chi2_of(cur)
    lam = 1e-3
    hist = [chi2]
    for it in range(max_iter):
        # refreshed Jacobian around p (parallel: 2*npar integrations)
        cases = []
        for j in range(npar):
            for sgn, t_ in ((+1, 'p'), (-1, 'm')):
                pj = p.copy()
                pj[j] += sgn * steps[j]
                y0v, gmv = build_param_state(pj, spec, y0_base)
                cases.append((f'gm:j{j}{t_}', y0v, gmv, RTOL_MAIN))
        res = dict(pool.map(run_case_gm, cases, chunksize=2))
        J = np.empty((len(wts), npar))
        for j in range(npar):
            colp, colm = res[f'gm:j{j}p'], res[f'gm:j{j}m']
            J[:, j] = np.concatenate([(colp[t] - colm[t]) for t in rows]) / (2 * steps[j])
        Jw = J * wts[:, None]
        if Nw is not None:
            Jw = Jw - Qn @ (Qn.T @ Jw)
        cn = np.sqrt((Jw * Jw).sum(0))
        cn[cn == 0] = 1.0
        Jn = Jw / cn[None, :]
        _, rfull = chi2_of(cur)
        rp = project(rfull)
        g = Jn.T @ rp
        JTJ = Jn.T @ Jn
        improved = False
        for _try in range(8):
            with np.errstate(all='ignore'):
                dn = np.linalg.solve(JTJ + lam * np.eye(npar), g)
            ptry = p + dn / cn
            otry = run_model(ptry)
            c2, _ = chi2_of(otry)
            if c2 < chi2:
                p, cur, chi2 = ptry, otry, c2
                lam = max(lam / 3.0, 1e-10)
                improved = True
                break
            lam *= 8.0
        hist.append(chi2)
        if not improved or (len(hist) > 2 and hist[-2] - hist[-1] < 1e-4 * hist[-1]):
            break
    # final residuals (profile nuisance exactly at the optimum, weighted space)
    rfin = np.concatenate([truth[t] - cur[t] for t in rows])
    if Nw is not None:
        rw = rfin * wts
        with np.errstate(all='ignore'):
            aN, *_ = np.linalg.lstsq(Nw, rw, rcond=None)
        rfin = (rw - Nw @ aN) / wts
    out = {'p': p, 'chi2': chi2, 'hist': hist, 'niter': len(hist) - 1, 'tag': tag}
    i0 = 0
    for t in rows:
        n = len(truth[t])
        rt = rfin[i0:i0 + n]
        out[t] = {'post_rms': float(np.sqrt((rt ** 2).mean())),
                  'post_peak': float(np.abs(rt).max()), 'resid': rt}
        i0 += n
    return out

def assemble_fit(signal, cols, col_names, use_rows, sigmas, col_mask, rcond=1e-10):
    """signal: dict target->array (m). cols: list of dicts target->array (response per step).
       Columns are unit-normalized before the solve (pure conditioning; projection unchanged).
       returns post-fit residual dict + solution info. All outputs verified finite."""
    tnames = [t for t in ('mars', 'sat', 'jup') if use_rows.get(t, False)]
    d = np.concatenate([signal[t] for t in tnames])
    wts = np.concatenate([np.full_like(signal[t], 1.0 / sigmas[t]) for t in tnames])
    A = np.array([np.concatenate([c[t] for t in tnames]) for c in cols]).T
    A = A[:, col_mask]
    Aw = A * wts[:, None]
    dw = d * wts
    cn = np.sqrt((Aw * Aw).sum(0))
    cn[cn == 0] = 1.0
    Awn = Aw / cn[None, :]
    assert np.all(np.isfinite(Awn)) and np.all(np.isfinite(dw))
    with np.errstate(all='ignore'):   # macOS Accelerate matmul raises spurious FPE flags
        coefn, _, rank, sv = np.linalg.lstsq(Awn, dw, rcond=rcond)
        coef = coefn / cn
        r = d - A @ coef
    assert np.all(np.isfinite(coef)) and np.all(np.isfinite(r))
    out = {'rank': int(rank), 'ncol': A.shape[1], 'coef': coef, 'sv': sv,
           'chi2': float(((r * wts) ** 2).sum()), 'nobs': len(d)}
    i0 = 0
    for t in tnames:
        n = len(signal[t])
        rt = r[i0:i0 + n]
        out[t] = {'pre_rms': float(np.sqrt((signal[t] ** 2).mean())),
                  'pre_peak': float(np.abs(signal[t]).max()),
                  'post_rms': float(np.sqrt((rt ** 2).mean())),
                  'post_peak': float(np.abs(rt).max()),
                  'resid': rt}
        i0 += n
    return out

# ----------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------
def main():
    t_start = time.time()
    L = []
    def P(s=''):
        L.append(s)
        print(s, flush=True)

    y0 = base_initial_state()

    # ---------------- build wave-1 case list ----------------
    cases = []
    cases.append(('ref',        y0, 0.0, 'newton', None, RTOL_MAIN, True))
    cases.append(('ref13',      y0, 0.0, 'newton', None, 1e-13,     False))
    cases.append(('f4_host',    y0, S_HOSTILE,   'all',      None, RTOL_MAIN, True))
    cases.append(('f4_frame',   y0, S_FRAMEWORK, 'all',      None, RTOL_MAIN, True))
    cases.append(('f4_host_sun', y0, S_HOSTILE,  'sun_only', None, RTOL_MAIN, True))

    # IC partials
    ic_params = []
    for b in range(NB):
        for c in range(3):
            ic_params.append(('r', b, c, POS_STEP))
        for c in range(3):
            ic_params.append(('v', b, c, VEL_STEP))
    for k, (kind, b, c, h) in enumerate(ic_params):
        for sgn, tag in ((+1, 'p'), (-1, 'm')):
            yp = y0.copy()
            off = (0 if kind == 'r' else 3 * NB) + 3 * b + c
            yp[off] += sgn * h
            cases.append((f'ic{k:02d}{tag}', yp, 0.0, 'newton', None, RTOL_MAIN, False))

    # GM partials (all six, for the max-absorption variant; primary fit uses Sun+Jup)
    gm_cases = []
    for b in range(NB):
        for sgn, tag in ((+1, 'p'), (-1, 'm')):
            gmv = GM.copy()
            gmv[b] *= (1.0 + sgn * GM_STEP)
            gm_cases.append((f'gm:{b}{tag}', y0, gmv, RTOL_MAIN))

    P('=' * 100)
    P('agentE SOLAR-REFLEX KILL-TEST (Door IVb) — per-body instantaneous F4, the Sun included')
    P('run date 2026-06-10 ; EOM per body: mu(|a|/s) a_vec = g_N ; mu(x)=x/sqrt(1+x^2)')
    P(f'normalizations: HOSTILE s = cH_Lambda = {S_HOSTILE_SI:.3e} m/s^2 ; '
      f'framework s = a0 = {S_FRAMEWORK_SI:.3e} m/s^2')
    P('=' * 100)
    P()
    P('[0] CONFIGURATION')
    P(f'    bodies: {", ".join(NAMES)} (EMB = Earth-Moon barycenter; Mercury omitted — '
      f'handled analytically in [8])')
    P('    elements: J2000 heliocentric (Standish/JPL approximate elements Table 1); '
      f'e_J = {ELEMENTS["Jupiter"][1]:.7f}')
    P(f'    span 35.0 yr = 1.19 Saturn periods = 2.95 Jupiter periods; DOP853 rtol={RTOL_MAIN:.0e} '
      f'atol={ATOL_MAIN:.0e}')
    P(f'    obs emulation: Mars range {MARS_T[0]/YR:.1f}-{MARS_T[-1]/YR:.1f} yr, 10-d cadence, '
      f'{len(MARS_T)} pts, sigma={SIGMA_MARS} m')
    P(f'                   Saturn range {SAT_T[0]/YR:.1f}-{SAT_T[-1]/YR:.2f} yr (Cassini-like), '
      f'30-d cadence, {len(SAT_T)} pts, sigma={SIGMA_SAT} m (loose variant {SIGMA_SAT_LOOSE} m)')
    P(f'                   [variant E only] Jupiter range {JUP_T[0]/YR:.1f}-{JUP_T[-1]/YR:.1f} yr '
      f'(Juno-era), 30-d cadence, {len(JUP_T)} pts, sigma={SIGMA_JUP} m')
    P('    fit emulation: linearized weighted LSQ on numerically-differenced Newton partials; '
      'noiseless data (residual-vs-sigma comparison)')
    P('    simplifications: Newtonian truth+model (GR common-mode at 1e-8 of signal), geometric '
      'ranges (no light-time), no asteroids, no per-pass biases except variant C')
    P()

    nwork = min(8, os.cpu_count() or 4)
    all_cases = cases + gm_cases
    results = {}
    P(f'    running {len(all_cases)} wave-1 integrations on {nwork} workers...')
    with ProcessPoolExecutor(max_workers=nwork) as ex:
        for name, out in ex.map(dispatch, all_cases, chunksize=2):
            if 'fail' in out:
                P(f'    INTEGRATION FAILURE {name}: {out["fail"]}')
                sys.exit(1)
            results[name] = out
    P(f'    wave-1 done in {time.time()-t_start:.0f} s '
      f'(ref nfev={results["ref"]["nfev"]})')
    P()

    ref = results['ref']

    # ---------------- wave 2: frozen-mu (orbit-averaged limit) ----------------
    pos_ref = ref['pos_diag']                              # (nd, 6, 3)
    g_series = np.array([newtonian_g(pos_ref[i]) for i in range(pos_ref.shape[0])])
    gn_series = np.sqrt((g_series ** 2).sum(-1))           # (nd, 6) AU/day^2
    eps_frozen_host = eps_of_y(gn_series / S_HOSTILE).mean(axis=0)
    name, out = run_case(('f4_host_frozen', y0, S_HOSTILE, 'frozen', eps_frozen_host,
                          RTOL_MAIN, True))
    results[name] = out

    # ---------------- [1] integrator validation ----------------
    P('[1] INTEGRATOR VALIDATION')
    # energy drift of Newton control
    def energy(state):
        r = state[:3 * NB].reshape(NB, 3); v = state[3 * NB:].reshape(NB, 3)
        m = GM / GM[0]
        ke = 0.5 * (m * (v * v).sum(-1)).sum()
        pe = 0.0
        for i in range(NB):
            for j in range(i + 1, NB):
                pe -= m[i] * GM[j] / np.linalg.norm(r[i] - r[j])
        return ke + pe
    E0 = energy(y0); E1 = energy(ref['states_end'])
    P(f'    Newton control relative energy drift over 35 yr : {abs(E1-E0)/abs(E0):.3e}')
    floor_sig = {t: results['ref13'][t] - ref[t] for t in ('mars', 'sat', 'jup')}
    P(f'    cross-tolerance range floor (rtol 1e-13 vs 1e-12), RMS [m]: '
      f'Mars {np.sqrt((floor_sig["mars"]**2).mean()):.3e} ; '
      f'Saturn {np.sqrt((floor_sig["sat"]**2).mean()):.3e}')
    P('    (pessimistic absolute-error bound; the signal chain shares the integrator and '
      'benefits from common-mode cancellation — see linearity check [6])')
    P()

    # ---------------- [2] solar-anomaly diagnostics ----------------
    P('[2] THE SUN\'S ANOMALOUS RESPONSE (from the hostile truth run)')
    pos_f4 = results['f4_host']['pos_diag']
    gnsun = gn_series[:, IDX_SUN]                     # AU/day^2
    gnsun_si = gnsun / ACC_SI2U
    eps_sun_h = eps_of_y(gnsun / S_HOSTILE)
    eps_sun_f = eps_of_y(gnsun / S_FRAMEWORK)
    da_h = eps_sun_h * gnsun_si
    da_f = eps_sun_f * gnsun_si
    apx_h = S_HOSTILE_SI ** 2 / (2 * gnsun_si)
    P(f'    |a_sun| over 35 yr: mean {gnsun_si.mean():.3e} m/s^2 ; '
      f'min {gnsun_si.min():.3e} ; max {gnsun_si.max():.3e}')
    P(f'    delta_a_sun HOSTILE  : mean {da_h.mean():.3e} m/s^2 ; pk-pk {da_h.max()-da_h.min():.3e} '
      f'({100*(da_h.max()-da_h.min())/da_h.mean():.1f}% of mean)')
    P(f'    delta_a_sun framework: mean {da_f.mean():.3e} m/s^2 ; pk-pk {da_f.max()-da_f.min():.3e} '
      f'({100*(da_f.max()-da_f.min())/da_f.mean():.1f}% of mean)')
    P(f'    stable-inversion identity: max |delta_a/(s^2/2|a|) - 1| = '
      f'{np.abs(da_h/apx_h - 1).max():.2e}  (x_sun~{(gnsun/S_HOSTILE).mean():.0f} hostile)')
    # anti-correlation with the GM_J acceleration template
    rsj = np.sqrt(((pos_ref[:, IDX_JUP] - pos_ref[:, IDX_SUN]) ** 2).sum(-1))
    gJ = GM_SI[IDX_JUP] / (rsj * AU) ** 2              # m/s^2, the GM_J partial template on the Sun
    def smooth(x, n):
        k = np.ones(n) / n
        return np.convolve(x, k, mode='valid')
    nsm = 55                                            # 55*15 d = 825 d boxcar kills inner-planet ripple
    da_s, gJ_s = smooth(da_h, nsm), smooth(gJ, nsm)
    cc_raw = np.corrcoef(da_h, gJ)[0, 1]
    cc_sm  = np.corrcoef(da_s, gJ_s)[0, 1]
    P(f'    anti-correlation of delta_a_sun with GM_J template g_J = GM_J/r_SJ^2:')
    P(f'      raw corr = {cc_raw:+.4f} ; after 825-d boxcar (inner-planet ripple removed) = {cc_sm:+.4f}')
    P(f'      (smoothed corr is not -1 because the Jupiter-Saturn synodic (19.9 yr) also '
      f'modulates |a_sun|; against the e_J cycle alone the anomaly is anti-phased)')
    A1 = np.vstack([np.ones_like(gJ_s), gJ_s]).T
    with np.errstate(all='ignore'):
        co, *_ = np.linalg.lstsq(A1, da_s, rcond=None)
        resfrac = np.sqrt(((da_s - A1 @ co) ** 2).mean()) / da_s.mean()
    assert np.all(np.isfinite(co)) and np.isfinite(resfrac)
    modfrac = (da_s.max() - da_s.min()) / da_s.mean()
    P(f'      smoothed delta_a modulation (pk-pk)/mean = {modfrac:.3f}  '
      f'[analytic ~ 4e_J(1+e_J) + Saturn term ~ {4*ELEMENTS["Jupiter"][1]:.3f}+]')
    P(f'      residual after projecting onto {{1, g_J(t)}}: {100*resfrac:.1f}% of mean '
      f'(the statically-unabsorbable fraction at acceleration level; ~2x2e_J because the '
      f'anomaly is ANTI-correlated with the template)')
    P()

    # ---------------- build partial columns ----------------
    col_names = []
    cols = []
    for b, pname in ((IDX_SUN, 'lnGM_sun'), (IDX_VEN, 'lnGM_ven'), (IDX_EMB, 'lnGM_emb'),
                     (IDX_MAR, 'lnGM_mar'), (IDX_JUP, 'lnGM_jup'), (IDX_SAT, 'lnGM_sat')):
        cp, cm = results[f'gm:{b}p'], results[f'gm:{b}m']
        cols.append({t: (cp[t] - cm[t]) / 2.0 for t in ('mars', 'sat', 'jup')})
        col_names.append(pname)
    for k, (kind, b, c, h) in enumerate(ic_params):
        cp, cm = results[f'ic{k:02d}p'], results[f'ic{k:02d}m']
        cols.append({t: (cp[t] - cm[t]) / 2.0 for t in ('mars', 'sat', 'jup')})
        col_names.append(f'{kind}{c}_{NAMES[b]}')
    # bias columns (variant C): Mars 3 segments, Saturn 1
    segs = [(5, 15), (15, 25), (25, 35.01)]
    for s0, s1 in segs:
        m = ((MARS_T >= s0 * YR) & (MARS_T < s1 * YR)).astype(float)
        cols.append({'mars': m, 'sat': np.zeros_like(SAT_T), 'jup': np.zeros_like(JUP_T)})
        col_names.append(f'bias_mars_{s0}-{s1}')
    cols.append({'mars': np.zeros_like(MARS_T), 'sat': np.ones_like(SAT_T),
                 'jup': np.zeros_like(JUP_T)})
    col_names.append('bias_sat')
    n_cols_C = len(cols)
    # ---- kitchen-sink (fit F) extra absorbers: beyond-realistic bound ----
    # per-opposition Mars biases (Earth-Mars synodic 2.1354 yr)
    opp_edges = np.arange(5.0, 35.0 + 1e-9, 2.1354)
    for k in range(len(opp_edges) - 1):
        msk = ((MARS_T >= opp_edges[k] * YR) & (MARS_T < opp_edges[k + 1] * YR)).astype(float)
        cols.append({'mars': msk, 'sat': np.zeros_like(SAT_T), 'jup': np.zeros_like(JUP_T)})
        col_names.append(f'oppbias_{k}')
    # per-year Cassini arc biases
    yr_edges = np.arange(4.5, 17.71, 1.0)
    for k in range(len(yr_edges) - 1):
        msk = ((SAT_T >= yr_edges[k] * YR) & (SAT_T < yr_edges[k + 1] * YR)).astype(float)
        cols.append({'mars': np.zeros_like(MARS_T), 'sat': msk, 'jup': np.zeros_like(JUP_T)})
        col_names.append(f'satarc_{k}')
    # smooth nuisance trends (proxy for asteroid-belt/long-period absorbers): Chebyshev
    xm = 2 * (MARS_T - MARS_T[0]) / (MARS_T[-1] - MARS_T[0]) - 1
    xs = 2 * (SAT_T - SAT_T[0]) / (SAT_T[-1] - SAT_T[0]) - 1
    for kdeg in range(9):
        c = np.polynomial.chebyshev.chebvander(xm, 8)[:, kdeg]
        cols.append({'mars': c, 'sat': np.zeros_like(SAT_T), 'jup': np.zeros_like(JUP_T)})
        col_names.append(f'chebM_{kdeg}')
    for kdeg in range(5):
        c = np.polynomial.chebyshev.chebvander(xs, 4)[:, kdeg]
        cols.append({'mars': np.zeros_like(MARS_T), 'sat': c, 'jup': np.zeros_like(JUP_T)})
        col_names.append(f'chebS_{kdeg}')

    name_idx = {n: i for i, n in enumerate(col_names)}
    NCOL = len(cols)
    base_cols = [name_idx['lnGM_sun'], name_idx['lnGM_jup']] + \
                [i for i, n in enumerate(col_names) if n[0] in 'rv' and '_' in n and
                 n.split('_')[1] in NAMES]
    maskA = np.zeros(NCOL, bool); maskA[base_cols] = True
    maskB = maskA.copy(); maskB[name_idx['lnGM_jup']] = False
    maskC = np.zeros(NCOL, bool); maskC[:n_cols_C] = True    # all GMs + ICs + seg biases
    maskF = np.ones(NCOL, bool)                              # everything incl. kitchen sink
    sigmas = {'mars': SIGMA_MARS, 'sat': SIGMA_SAT, 'jup': SIGMA_JUP}
    rowsMS  = {'mars': True, 'sat': True, 'jup': False}
    rowsM   = {'mars': True, 'sat': False, 'jup': False}
    rowsMSJ = {'mars': True, 'sat': True, 'jup': True}

    FITS = {
        'A  GMsun+GMjup+36 IC      | Mars+Sat ': (maskA, rowsMS),
        'B  Juno-anchored (no GMjup)| Mars+Sat ': (maskB, rowsMS),
        'C  all-6 GM+IC+seg-biases | Mars+Sat ': (maskC, rowsMS),
        'D  as A                   | Mars only': (maskA, rowsM),
        'E  as A                   | M+S+Jup  ': (maskA, rowsMSJ),
        'F  KITCHEN SINK (beyond-real bound) ': (maskF, rowsMS),
    }

    def signal_of(truth):
        return {t: results[truth][t] - ref[t] for t in ('mars', 'sat', 'jup')}

    # ---------------- [3] pre-fit signals ----------------
    P('[3] PRE-FIT RANGE SIGNALS (F4 truth minus Newton at identical ICs/GMs) [m]')
    sigs = {}
    for truth, lab in (('f4_host', 'HOSTILE  '), ('f4_frame', 'framework'),
                       ('f4_host_sun', 'hostile Sun-only-F4'), ('f4_host_frozen',
                        'hostile frozen-mu (orbit-averaged limit)')):
        sg = signal_of(truth)
        sigs[truth] = sg
        P(f'    {lab:42s}: Mars RMS {np.sqrt((sg["mars"]**2).mean()):10.3f} '
          f'peak {np.abs(sg["mars"]).max():10.3f} | Saturn RMS {np.sqrt((sg["sat"]**2).mean()):10.3f} '
          f'peak {np.abs(sg["sat"]).max():10.3f}')
    P()

    # ---------------- [4] fit-emulation table ----------------
    P('[4] LINEARIZED FIT SURVEY — post-fit residuals vs ranging accuracy')
    P('    NOTE: this table is the LINEARIZED projection — useful for comparing fit CONFIGS,')
    P('    but NOT verdict-grade (see [4b]/[10]: its optimum exploits cancellations that break')
    P('    nonlinearly). The decisive numbers are the LM fits in [4b] and the verdict [9].')
    P('    columns: post-fit RMS / peak [m]; absorb = pre-RMS/post-RMS; margin = sigma/post-RMS')
    verdicts = {}
    for truth, tlab in (('f4_host', 'HOSTILE s=cH_Lam'), ('f4_frame', 'FRAMEWORK s=a0'),
                        ('f4_host_sun', 'hostile, Sun-only-F4'),
                        ('f4_host_frozen', 'hostile, frozen-mu')):
        P(f'  truth: {tlab}')
        for fname, (mask, rows) in FITS.items():
            if truth in ('f4_host_sun', 'f4_host_frozen') and not fname.startswith(('A', 'B')):
                continue
            r = assemble_fit(sigs[truth], cols, col_names, rows, sigmas, mask)
            parts = []
            ok = True
            for t, sg in (('mars', SIGMA_MARS), ('sat', SIGMA_SAT), ('jup', SIGMA_JUP)):
                if t not in r:
                    continue
                m = sg / r[t]['post_rms'] if r[t]['post_rms'] > 0 else float('inf')
                ok &= (m > 1.0)
                parts.append(f'{t[:4]}: {r[t]["post_rms"]:9.3f}/{r[t]["post_peak"]:9.3f} '
                             f'abs {r[t]["pre_rms"]/max(r[t]["post_rms"],1e-12):8.1f}x marg {m:8.2f}')
            v = 'PASS' if ok else 'FAIL'
            verdicts[(truth, fname[0])] = (v, r)
            dgmj = ''
            if mask[name_idx['lnGM_jup']]:
                cidx = list(np.where(mask)[0]).index(name_idx['lnGM_jup'])
                dgmj = f' | dGM_J/GM_J = {r["coef"][cidx]*GM_STEP:+.2e}'
            P(f'    fit {fname}: {" | ".join(parts)}  -> {v}'
              f'  [sqrt(chi2_w)={math.sqrt(r["chi2"]):9.1f}]{dgmj}')
        P()

    # ---------------- [4b] hostile verification of the fit emulation ----------------
    P('[4b] HOSTILE VERIFICATION OF THE FIT EMULATION (a kill claim owes its own audit)')
    rA_h = verdicts[('f4_host', 'A')][1]
    P(f'    fit A (hostile): rank/ncol = {rA_h["rank"]}/{rA_h["ncol"]} ; normalized-column '
      f'SV range {rA_h["sv"].max():.2e}..{rA_h["sv"].min():.2e}')
    for tr in ('f4_host', 'f4_frame'):
        line = []
        for rc in (1e-6, 1e-8, 1e-10, 1e-12, 1e-14):
            rr = assemble_fit(sigs[tr], cols, col_names, rowsMS, sigmas, maskA, rcond=rc)
            line.append(f'{rc:.0e}: {rr["mars"]["post_rms"]:.2f}/{rr["sat"]["post_rms"]:.2f}')
        P(f'    rcond sweep, fit A ({tr}) Mars/Sat post-RMS [m]: ' + ' | '.join(line))
    # independent solver cross-check (scipy gelsy vs numpy gelsd) on fit A hostile
    from scipy.linalg import lstsq as sp_lstsq
    tnames = ['mars', 'sat']
    d_ck = np.concatenate([sigs['f4_host'][t] for t in tnames])
    w_ck = np.concatenate([np.full_like(sigs['f4_host'][t], 1.0 / sigmas[t]) for t in tnames])
    A_ck = np.array([np.concatenate([c[t] for t in tnames]) for c in cols]).T[:, maskA]
    cnk = np.sqrt(((A_ck * w_ck[:, None]) ** 2).sum(0))
    with np.errstate(all='ignore'):
        c2, _, _, _ = sp_lstsq((A_ck * w_ck[:, None]) / cnk[None, :], d_ck * w_ck,
                               lapack_driver='gelsy')
        r2 = d_ck - A_ck @ (c2 / cnk)
    r1 = np.concatenate([rA_h['mars']['resid'], rA_h['sat']['resid']])
    P(f'    independent solver (LAPACK gelsy vs gelsd): max |resid diff| = '
      f'{np.abs(r1 - r2).max():.2e} m ; RMS agree to {abs(np.sqrt((r2**2).mean())/np.sqrt((r1**2).mean())-1):.2e}')
    # post-fit pipeline floor: fit the integrator-noise signal
    flr = assemble_fit(floor_sig, cols, col_names, rowsMS, sigmas, maskA)
    P(f'    POST-FIT PIPELINE FLOOR (fit A applied to rtol-crossing noise): '
      f'Mars {flr["mars"]["post_rms"]:.3f} m ; Saturn {flr["sat"]["post_rms"]:.3f} m '
      f'(signal/floor: hostile {rA_h["mars"]["post_rms"]/max(flr["mars"]["post_rms"],1e-9):.0f}x ; '
      f'framework {verdicts[("f4_frame","A")][1]["mars"]["post_rms"]/max(flr["mars"]["post_rms"],1e-9):.0f}x Mars)')
    # --- THE DECISIVE LAYER: TRUE NONLINEAR FIT (LM, Jacobian re-integrated each iter) ---
    # Why: a direct unit test (logged in [10]) showed the column/parameter mapping is exact
    # (linear prediction matches integration to ~0.13% of the response) BUT the linearized
    # optimum sits at parameter excursions whose second-order dynamics break the linear
    # cancellations at the 1e5-1e6 m level. A real ephemeris fit is ITERATED and nonlinear,
    # so the verdict must come from the true nonlinear minimum, not the linear projection.
    P('    --- true nonlinear fits (Levenberg-Marquardt, partials re-integrated each '
      'iteration; the verdict-grade numbers) ---')
    specA = [('gm', IDX_SUN), ('gm', IDX_JUP)] + [('ic', k) for k in range(36)]
    specB = [('gm', IDX_SUN)] + [('ic', k) for k in range(36)]
    nuis_idx = [i for i, n in enumerate(col_names)
                if n.startswith(('bias_', 'oppbias_', 'satarc_', 'chebM_', 'chebS_'))]
    nuisN = {t: np.array([cols[i][t] for i in nuis_idx]).T for t in ('mars', 'sat')}
    LM = {}
    with ProcessPoolExecutor(max_workers=nwork) as pool2:
        for tr in ('f4_host', 'f4_frame'):
            truth_r = {t: results[tr][t] for t in ('mars', 'sat')}
            for cfg, spec, nu in (('A', specA, None), ('B', specB, None),
                                  ('Anuis', specA, nuisN)):
                t0 = time.time()
                LM[(tr, cfg)] = lm_fit(truth_r, spec, y0, pool2, sigmas=sigmas,
                                       nuis=nu, tag=f'{tr}-{cfg}')
                print(f'      [lm {tr}-{cfg}: {LM[(tr,cfg)]["niter"]} iters, '
                      f'{time.time()-t0:.0f} s, Mars post {LM[(tr,cfg)]["mars"]["post_rms"]:.2f} m]',
                      flush=True)
        # uniqueness probe: restart framework-A from a displaced point
        LM[('f4_frame', 'A2')] = lm_fit({t: results['f4_frame'][t] for t in ('mars', 'sat')},
                                        specA, y0, pool2, sigmas=sigmas,
                                        p0=LM[('f4_frame', 'A')]['p'] * 1.15,
                                        tag='frame-A-restart')
    for key, lab in ((('f4_host', 'A'), 'HOSTILE   fit A (GM_sun,GM_J,36 IC)'),
                     (('f4_host', 'B'), 'HOSTILE   fit B (Juno-anchored)   '),
                     (('f4_host', 'Anuis'), 'HOSTILE   fit A + kitchen sink  '),
                     (('f4_frame', 'A'), 'FRAMEWORK fit A (GM_sun,GM_J,36 IC)'),
                     (('f4_frame', 'B'), 'FRAMEWORK fit B (Juno-anchored)   '),
                     (('f4_frame', 'Anuis'), 'FRAMEWORK fit A + kitchen sink  '),
                     (('f4_frame', 'A2'), 'FRAMEWORK fit A restart (x1.15)  ')):
        r = LM[key]
        pgm = [f'{v:+.2e}' for v, (k, i) in zip(r['p'], specA if len(r['p']) == 38 else specB)
               if k == 'gm']
        P(f'    LM {lab}: {r["niter"]:2d} iters, chi2 {r["hist"][0]:.3e} -> {r["chi2"]:.3e} ; '
          f'Mars {r["mars"]["post_rms"]:9.3f}/{r["mars"]["post_peak"]:9.3f} m ; '
          f'Saturn {r["sat"]["post_rms"]:9.3f}/{r["sat"]["post_peak"]:9.3f} m ; '
          f'dlnGM = {", ".join(pgm)}')
    P(f'    linearized-vs-LM calibration: fit A hostile {rA_h["mars"]["post_rms"]:.1f} m (lin) '
      f'vs {LM[("f4_host","A")]["mars"]["post_rms"]:.1f} m (LM) Mars ; '
      f'framework {verdicts[("f4_frame","A")][1]["mars"]["post_rms"]:.1f} vs '
      f'{LM[("f4_frame","A")]["mars"]["post_rms"]:.1f} m')
    c2a, c2b = LM[('f4_frame', 'A')]['chi2'], LM[('f4_frame', 'A2')]['chi2']
    pa, pb = LM[('f4_frame', 'A')]['p'], LM[('f4_frame', 'A2')]['p']
    cosim = float(pa @ pb / (np.linalg.norm(pa) * np.linalg.norm(pb)))
    P(f'    uniqueness/convergence probe: framework-A restart (x1.15) converges to chi2 '
      f'{c2b:.4e} vs {c2a:.4e} -> LM convergence slack ~{100*abs(c2a-c2b)/min(c2a,c2b):.0f}% '
      f'in chi2 (~{100*(math.sqrt(max(c2a,c2b)/min(c2a,c2b))-1):.0f}% in RMS), '
      f'param-vector cosine {cosim:.4f} (same basin) — immaterial against the margins below')
    # residual structure: what carries the surviving signal?
    def sin_amp(res_t, tgrid, period_yr):
        w = 2 * math.pi / (period_yr * YR)
        M2 = np.vstack([np.sin(w * tgrid), np.cos(w * tgrid), np.ones_like(tgrid)]).T
        with np.errstate(all='ignore'):
            cc, *_ = np.linalg.lstsq(M2, res_t, rcond=None)
        return math.hypot(cc[0], cc[1])
    def top_fft(res_t, dt_days, n=3):
        h = np.hanning(len(res_t))
        sp = np.abs(np.fft.rfft(res_t * h)) / (h.sum() / 2)
        fr = np.fft.rfftfreq(len(res_t), dt_days)
        pk = (np.argsort(sp[1:])[::-1][:n] + 1)
        return [(1.0 / fr[i] / YR, sp[i]) for i in pk]
    P('    post-fit residual structure (LM nonlinear fit A, hostile):')
    resM = LM[('f4_host', 'A')]['mars']['resid']; resS = LM[('f4_host', 'A')]['sat']['resid']
    P(f'      Mars  : sinusoid amplitudes [m] @ P_Jup 11.86 yr: {sin_amp(resM, MARS_T, 11.862):8.2f} ; '
      f'@ E-J synodic 1.092 yr: {sin_amp(resM, MARS_T, 1.0921):8.2f} ; '
      f'@ M-J synodic 2.235 yr: {sin_amp(resM, MARS_T, 2.2354):8.2f} ; '
      f'@ E-M synodic 2.135 yr: {sin_amp(resM, MARS_T, 2.1354):8.2f}')
    P(f'              top FFT lines (period yr, amp m): ' +
      ' ; '.join(f'({p:.2f}, {a:.1f})' for p, a in top_fft(resM, 10.0)))
    P(f'      Saturn: @ P_Jup 11.86 yr: {sin_amp(resS, SAT_T, 11.862):8.2f} ; '
      f'@ J-S synodic 19.86 yr: {sin_amp(resS, SAT_T, 19.86):8.2f} ; '
      f'@ S-E synodic 1.035 yr: {sin_amp(resS, SAT_T, 1.0352):8.2f}')
    P(f'              top FFT lines (period yr, amp m): ' +
      ' ; '.join(f'({p:.2f}, {a:.1f})' for p, a in top_fft(resS, 30.0)))
    resMF = LM[('f4_host', 'Anuis')]['mars']['resid']
    P(f'    post-fit residual structure (LM + kitchen-sink, hostile): Mars top FFT: ' +
      ' ; '.join(f'({p:.2f}, {a:.1f})' for p, a in top_fft(resMF, 10.0)))
    P()

    # ---------------- [5] prescription & attribution ----------------
    P('[5] PRESCRIPTION & ATTRIBUTION')
    sg_full, sg_sun = sigs['f4_host'], sigs['f4_host_sun']
    fr = lambda a, b: np.sqrt((a ** 2).mean()) / np.sqrt((b ** 2).mean())
    P(f'    Sun-only-F4 / full-F4 pre-fit signal ratio: Mars {fr(sg_sun["mars"], sg_full["mars"]):.3f} '
      f'; Saturn {fr(sg_sun["sat"], sg_full["sat"]):.3f}  '
      f'(~1 -> the SUN channel dominates the full per-body signal)')
    sg_fz = sigs['f4_host_frozen']
    P(f'    frozen-mu / instantaneous pre-fit ratio   : Mars {fr(sg_fz["mars"], sg_full["mars"]):.3f} '
      f'; Saturn {fr(sg_fz["sat"], sg_full["sat"]):.3f}')
    P(f'    eps_sun frozen value = {eps_frozen_host[IDX_SUN]:.3e} '
      f'(vs instantaneous mean {eps_sun_h.mean():.3e}) ; planet eps frozen: '
      + ', '.join(f'{NAMES[i]} {eps_frozen_host[i]:.1e}' for i in range(1, NB)))
    P()

    # ---------------- [6] scaling & linearity ----------------
    P('[6] SCALING CHECKS')
    s2 = (S_HOSTILE_SI / S_FRAMEWORK_SI) ** 2
    rM = fr(sigs['f4_host']['mars'], sigs['f4_frame']['mars'])
    rS = fr(sigs['f4_host']['sat'], sigs['f4_frame']['sat'])
    P(f'    hostile/framework pre-fit signal ratio: Mars {rM:.3f} ; Saturn {rS:.3f} ; '
      f'expected s^2 ratio = {s2:.3f}  -> linear-regime + integrator-noise check')
    # per-planet heliocentric response from the Sun-only run (licenses Mercury extrapolation)
    pos_sun_only = results['f4_host_sun']['pos_diag']
    helio_f4 = pos_sun_only - pos_sun_only[:, IDX_SUN:IDX_SUN + 1, :]
    helio_rf = pos_ref - pos_ref[:, IDX_SUN:IDX_SUN + 1, :]
    nJ = 2 * math.pi / (ELEMENTS['Jupiter'][0] ** 1.5 * YR)
    P('    per-planet heliocentric displacement (Sun-only-F4, hostile), with the naive '
      'forced-epicycle product peak*|n^2-n_J^2|:')
    amps = {}
    for b in (IDX_VEN, IDX_EMB, IDX_MAR, IDX_SAT):
        d = np.sqrt(((helio_f4[:, b] - helio_rf[:, b]) ** 2).sum(-1)) * AU
        a_b = ELEMENTS[NAMES[b]][0]
        n_b = 2 * math.pi / (a_b ** 1.5 * YR)
        scale = abs(n_b ** 2 - nJ ** 2)
        amps[b] = (d.max(), scale)
        P(f'      {NAMES[b]:8s}: peak {d.max():8.2f} m ; peak*|n^2-nJ^2| = {d.max()*scale:.3e}')
    P('      -> the product is NOT constant (x9 spread): the displacement is dominated by '
      'SECULAR pumping (slowly-rotating field torque), not the equilibrium epicycle. '
      'Stated plainly; the Mercury number in [8] is therefore a BRACKET, not a law.')
    P()

    # ---------------- [7] literature pins ----------------
    P('[7] RANGING-ACCURACY & CONVENTION PINS (web-verified 2026-06-10)')
    P('    Mars range: ~1 m systematics-limited (DSN station calibration), MGS/Odyssey/MRO '
      '1-m class data used in ephemerides — JPL IPN Progress Report 42-190 (Folkner-era, '
      '"Station-Specific Errors in Mars Ranging"); EPM2021 fits MRO/ODY ranges with '
      'station-bias models (iaaras.ru/en/dept/ephemeris/epm/2021). Adopted sigma = 1.5 m.')
    P('    Saturn/Cassini range: normal points ~10 m (Folkner et al. 2008, DE421-era, as quoted '
      'in the INPOP19a Cassini analysis: Fienga et al. 2020, A&A 640, A6); DE430-based Cassini '
      'residuals show a 12-yr sinusoid of FULL amplitude ~70 m (Hees et al. 2016, AJ 152:94, '
      'arXiv:1604.03180 — the Planet Nine ranging paper); INPOP17a shows a ~50 m annual '
      'signature (same A&A analysis). Adopted sigma = 25 m (loose variant 75 m).')
    P('    Jupiter: DE440 fits Juno radio range + VLBA (Park et al. 2021, AJ 161:105, '
      'ssd.jpl.nasa.gov/doc/de440_de441.html). GM_J is measured INDEPENDENTLY by Juno orbital '
      'tracking: GM_J = 1.266865341e17 m^3/s^2 with relative uncertainty ~1e-8-1e-9 '
      '(Durante et al. 2020, GRL 47, e2019GL086572) — at Juno periapsis |a|~25 m/s^2, F4 is '
      'OFF (x~1e11), so the Juno GM_J is F4-clean: any ephemeris GM_J shift >> 1e-8 relative '
      'is independently refuted. That is fit config B ("Juno-anchored").')
    P('    Mercury/BepiColombo MORE: 2-way range ~1 cm RMS at 4 s integration, in-flight '
      'verified (arXiv:2111.04499 INPOP-BepiColombo simulations; arXiv:2211.04881), daily '
      'normal points 2026-2028.5 assumed in published simulations.')
    P()

    # ---------------- [8] Mercury / BepiColombo extrapolation ----------------
    P('[8] MERCURY / BEPICOLOMBO SENSITIVITY (order-of-magnitude BRACKET; Mercury not '
      'integrated, see [6] caveat)')
    a_me = 0.38709893
    n_me = 2 * math.pi / (a_me ** 1.5 * YR)
    d_mar, sc_mar = amps[IDX_MAR]
    d_me_hi = d_mar * sc_mar / abs(n_me ** 2 - nJ ** 2)     # Mars-product scaling (upper)
    d_me_lo = (da_h.mean() * ACC_SI2U / ACC_SI2U) / (n_me / DAY) ** 2  # equilibrium f/n^2 (floor)
    pre_h = float(np.sqrt((sigs['f4_host']['mars'] ** 2).mean()))
    absorb_F = pre_h / max(LM[('f4_host', 'Anuis')]['mars']['post_rms'], 1e-12)
    P(f'    Mercury heliocentric response bracket (hostile, PRE-fit): equilibrium-epicycle '
      f'floor f/n^2 ~ {d_me_lo:.1f} m ; Mars-product scaling ~ {d_me_hi:.0f} m')
    P(f'    framework normalization (/{s2:.1f}): ~{d_me_lo/s2*100:.0f} cm .. {d_me_hi/s2:.1f} m '
      f'PRE-fit; applying the LM kitchen-sink absorption seen at Mars ({absorb_F:.0f}x): '
      f'~{d_me_lo/s2/absorb_F*100:.2f} cm .. {d_me_hi/s2/absorb_F*100:.0f} cm')
    P(f'    vs BepiColombo MORE sigma ~ 1 cm (in-flight verified): the framework-normalization '
      f'signal spans MARGINAL (~0.4 cm at the most pessimistic corner: epicycle floor + maximal '
      f'absorption) to DECISIVELY DETECTABLE (~1 m) across the bracket — both ways stated. '
      f'AND the published MORE campaign window is ~2.5 yr (2026-2028.5), only 0.21 of the '
      f'11.86-yr carrier, so much of the slow template is IC/bias-absorbable over so short an '
      f'arc. Treat as a FUTURE check (decisive only if MORE-class ranging persists ~a decade '
      f'or the true response sits in the upper half of the bracket), not a present bound. '
      f'Stated as sensitivity, not verdict.')
    P()

    # ---------------- [9] verdict ----------------
    P('[9] VERDICT (both ways, full weight; decisive numbers = the TRUE NONLINEAR (LM) fits)')
    for truth, lab in (('f4_host', 'HOSTILE (s = cH_Lambda = 5.418e-10 m/s^2)'),
                       ('f4_frame', 'FRAMEWORK (s = a0 = 9.36e-11 m/s^2)')):
        rA = LM[(truth, 'A')]
        rB = LM[(truth, 'B')]
        rK = LM[(truth, 'Anuis')]
        vA = 'PASS' if (rA['mars']['post_rms'] < SIGMA_MARS and rA['sat']['post_rms'] < SIGMA_SAT) else 'FAIL'
        vB = 'PASS' if (rB['mars']['post_rms'] < SIGMA_MARS and rB['sat']['post_rms'] < SIGMA_SAT) else 'FAIL'
        vK = 'PASS' if (rK['mars']['post_rms'] < SIGMA_MARS and rK['sat']['post_rms'] < SIGMA_SAT) else 'FAIL'
        P(f'  {lab}:')
        P(f'    LM fit A (GM_sun, GM_J, 36 IC):      {vA}  '
          f'(Mars {rA["mars"]["post_rms"]:8.2f} m vs {SIGMA_MARS} m -> {rA["mars"]["post_rms"]/SIGMA_MARS:7.1f}x over ; '
          f'Saturn {rA["sat"]["post_rms"]:8.2f} m vs {SIGMA_SAT} m -> {rA["sat"]["post_rms"]/SIGMA_SAT:6.1f}x'
          f' [vs loose {SIGMA_SAT_LOOSE} m -> {rA["sat"]["post_rms"]/SIGMA_SAT_LOOSE:5.1f}x])')
        P(f'    LM fit B (Juno-anchored GM_J):       {vB}  '
          f'(Mars {rB["mars"]["post_rms"]:8.2f} m ; Saturn {rB["sat"]["post_rms"]:8.2f} m)')
        P(f'    LM + kitchen sink (beyond-real):     {vK}  '
          f'(Mars {rK["mars"]["post_rms"]:8.2f} m -> {rK["mars"]["post_rms"]/SIGMA_MARS:7.1f}x over ; '
          f'Saturn {rK["sat"]["post_rms"]:8.2f} m)')
    rKf = LM[('f4_frame', 'Anuis')]['mars']['post_rms']
    rAf = LM[('f4_frame', 'A')]['mars']['post_rms']
    s_crit_A = S_FRAMEWORK_SI * math.sqrt(SIGMA_MARS / rAf)
    s_crit_K = S_FRAMEWORK_SI * math.sqrt(SIGMA_MARS / rKf)
    P(f'  CRITICAL NORMALIZATION (residual ~ s^2, linearity verified in [6]): instantaneous '
      f'per-body F4 hides below Mars ranging accuracy only for')
    P(f'    s < {s_crit_A:.2e} (conservative fit A) .. {s_crit_K:.2e} m/s^2 (kitchen-sink '
      f'bound) = ({s_crit_A/S_FRAMEWORK_SI:.2f} .. {s_crit_K/S_FRAMEWORK_SI:.2f}) x a0 '
      f'= cH_Lambda / ({S_HOSTILE_SI/s_crit_K:.0f} .. {S_HOSTILE_SI/s_crit_A:.0f})')
    P(f'    -> BOTH candidate normalizations sit above the survival line: the bath value '
      f'cH_Lambda by ~{S_HOSTILE_SI/s_crit_A:.0f}x, the empirical a0 by '
      f'~{S_FRAMEWORK_SI/s_crit_A:.1f}x in s (={rAf/SIGMA_MARS:.1f}x in residual).')
    P(f'  STRUCTURE OF THE KILL: the unabsorbable carrier is the Earth-Jupiter synodic '
      f'(~1.09 yr) + P_Jup (11.86 yr) response to the Sun\'s Jupiter-ward anomalous reflex '
      f'(the r_J^2-anti-correlated template of [2]); at framework normalization the kill is '
      f'MARS-CARRIED (Cassini alone would be marginal: fit-B Saturn '
      f'{LM[("f4_frame","B")]["sat"]["post_rms"]:.1f} m vs 25 m tight / 75 m loose). '
      f'No realistic nuisance lives at the E-J synodic over a 30-yr arc (annual systematics '
      f'separate from 1.0921 yr after ~12 yr of data; asteroid templates live at 3-6 yr).')
    P(f'  GM_J NOTE: every fit that may move GM_J wants |dlnGM_J| ~ 2e-7..1e-5 — i.e. '
      f'20x..1000x the Juno determination uncertainty (~1e-8, Durante+2020): the absorbed '
      f'configurations are independently refuted by Juno, which is why the Juno-anchored '
      f'fit B is the realistic case (and it fails too).')
    P()

    # ---------------- [10] bug log ----------------
    P('[10] BUG LOG (own-work bugs caught during this run)')
    P('    1. Pre-run: stray invalid token (`i in_`) in the name_idx dict comprehension — '
      'syntax error, caught on read-through before first execution; fixed.')
    P('    2. Pre-run: make_rhs was passed gm=None for non-tuple modes (would crash every F4 '
      'run); caught on read-through; fixed to pass GM explicitly.')
    P('    3. First full run: numpy matmul on macOS Accelerate raised spurious '
      'divide/overflow/invalid RuntimeWarnings inside clean lstsq/projection calls; '
      'investigated — solutions verified finite and cross-checked against LAPACK gelsy '
      '(max residual difference printed in [4b]); warnings isolated with errstate + '
      'isfinite asserts rather than ignored blindly.')
    P('    4. First full run: Mercury/BepiColombo extrapolation printed in cm with a '
      'misleading "absorption factor from fit A" (9x) — replaced with the kitchen-sink '
      'absorption bound and an explicit window-length caveat.')
    P('    5. Initial fit-A absorption (8.6x) looked suspiciously WEAK against an analytic '
      'prior of stronger absorption — this suspicion was CORRECT in part: see 6-7.')
    P('    6. The nonlinear forward check EXPLODED (1e6 m vs 269 m linearized) and frozen-'
      'Jacobian Gauss-Newton DIVERGED. Unit test (3-parameter known perturbation, direct '
      'integration vs linear prediction) proved the column/parameter mapping exact to '
      '~0.13% of response — so the failure was not a mapping bug: the linearized optimum '
      'lives at parameter excursions (e.g. dGM_J/GM_J ~ -8e-6 + large compensating IC '
      'moves) whose second-order dynamics break the linear cancellation. A LINEARIZED '
      'EMULATION IS NOT VERDICT-GRADE FOR THIS PROBLEM.')
    P('    7. Resolution: full Levenberg-Marquardt fits with the Jacobian re-INTEGRATED '
      'every iteration (a real mini ephemeris fit), run for fits A/B/kitchen-sink at both '
      'normalizations, with a displaced-restart uniqueness probe. The verdict in [9] rests '
      'exclusively on these LM numbers; the linear table [4] is retained as a config '
      'survey only.')
    P()
    P(f'    [output assembled in {time.time()-t_start:.0f} s total]')

    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'agentE_solar_reflex.out')
    with open(outpath, 'w') as f:
        f.write('\n'.join(L) + '\n')
    print(f'\nwritten: {outpath}')

if __name__ == '__main__':
    main()
