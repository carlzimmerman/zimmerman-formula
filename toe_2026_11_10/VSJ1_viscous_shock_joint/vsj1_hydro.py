#!/usr/bin/env python3
"""VSJ1 hydro: spherical Lagrangian hydrodynamics of the clock's charge, with this lane's own time stepping
(two-stage predictor-corrector, nodes and velocities at the same time level). See FROZEN_CRITERIA.md.

    python3 vsj1_hydro.py ka1                               Noh
    python3 vsj1_hydro.py ka2                               FLD1's R_ta with every fluid term off
    python3 vsj1_hydro.py ka4                               EdS self-similar collisional infall
    python3 vsj1_hydro.py seed  <footing> <logMb> <N> [tag] [heat 0/1] [nu_fac]
    python3 vsj1_hydro.py cosmo <footing> <A> [N] [tag]     at log M_b 10.5; other masses by scaling

Units kpc, km/s, Msun; time kpc/(km/s). Reads (read-only) col1_lib.py, kd1.json, aks1_t.json. Writes runs/*.json.
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, signal, sys, time
import numpy as np
from scipy.linalg import solve_banded

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'fable52_push', 'COL1_clock_collapse'))
import col1_lib as L                                                                    # noqa: E402
KD1 = json.load(open(os.path.join(REPO, 'closure_2026_11_06', 'KD1_unpinned_kq_dust', 'kd1.json')))
AKS = json.load(open(os.path.join(REPO, 'toe_2026_11_10', 'AKS1_acceleration_keyed_sink', 'aks1_t.json')))['T7']
RUNS = os.path.join(HERE, 'runs')
CKPT = os.environ.get('VSJ1_CKPT', '')
FOURPI = 4 * math.pi
CQ, CL, CFL = 2.0, 0.3, 0.25
GAM = 5.0 / 3.0
STOP = {'flag': False}
signal.signal(signal.SIGTERM, lambda *a: STOP.update(flag=True))


class EdS:
    """Einstein-de Sitter background with the interface of col1_lib.Cosmo (dust only, no baryons)."""

    def __init__(self, h=0.7):
        self.H0 = 0.1 * h; self.OL = 0.0; self.Om = 1.0
        self.rhoc0 = 3 * self.H0 ** 2 / (8 * math.pi * L.G); self.nbar0 = self.rhoc0; self.rhob0 = 0.0

    def t_of_a(self, a): return (2.0 / 3.0) * a ** 1.5 / self.H0

    def a_of_t(self, t): return (1.5 * self.H0 * t) ** (2.0 / 3.0)

    def H_of_a(self, a): return self.H0 * a ** -1.5


def inner(x, first=0.0):
    return np.concatenate([[first], x[:-1]])


def zones(r, v, e, dM, gam):
    rl = inner(r); vl = inner(v)
    V = (FOURPI / 3) * (r ** 3 - rl ** 3)
    rho = dM / V
    dv = v - vl
    cs = np.sqrt(gam * (gam - 1) * np.maximum(e, 0.0))
    comp = (r * r * v - rl * rl * vl) < 0.0
    q = np.where(comp, rho * (CQ * dv * dv + CL * cs * np.abs(dv)), 0.0)
    return V, rho, (gam - 1) * rho * e, q


def pforce(r, P, dm):
    return -FOURPI * r * r * (np.concatenate([P[1:], [0.0]]) - P) / dm


def visc_solve(r, rho, vstar, dt, nu, dm):
    """Backward Euler for the traceless shear stress sigma_rr = (4/3) rho nu (dv/dr - v/r). Returns v, heat per mass."""
    rl = inner(r)
    al = np.zeros_like(r); be = np.zeros_like(r)
    al[1:] = 1.0 / (r[1:] - rl[1:]); be[1:] = 1.0 / (r[1:] + rl[1:])
    w = (4.0 / 3.0) * rho * nu * (0.5 * (r + rl)) ** 3; w[0] = 0.0
    pref = FOURPI / (dm * r)
    wn = np.concatenate([w[1:], [0.0]]); aln = np.concatenate([al[1:], [0.0]]); ben = np.concatenate([be[1:], [0.0]])
    up = pref * wn * (aln - ben)
    di = -pref * (wn * (aln + ben) + w * (al - be))
    lo = pref * w * (al + be)
    ab = np.zeros((3, r.size))
    ab[0, 1:] = -dt * up[:-1]; ab[1, :] = 1.0 - dt * di; ab[2, :-1] = -dt * lo[1:]
    v = solve_banded((1, 1), ab, vstar)
    s = v * (al - be) - inner(v) * (al + be); s[0] = 0.0
    return v, (4.0 / 3.0) * nu * s * s * dt


def step(t, dt, r0, v0, e0, dM, dm, grav, nu, gam, heat=True):
    """One predictor-corrector step. Raises FloatingPointError if a zone inverts."""
    V0, rho0, p0, q0 = zones(r0, v0, e0, dM, gam)
    P0 = p0 + q0
    g0 = grav(t, r0)
    v1 = v0 + dt * (g0 + pforce(r0, P0, dm))
    h1 = 0.0
    if nu > 0.0:
        v1, h1 = visc_solve(r0, rho0, v1, dt, nu, dm)
    r1 = r0 + 0.5 * dt * (v0 + v1)
    V1 = (FOURPI / 3) * (r1 ** 3 - inner(r1) ** 3)
    if np.any(V1 <= 0.0):
        raise FloatingPointError('zone inverted (predictor)')
    e1 = np.maximum(e0 - P0 * (V1 - V0) / dM + h1, 0.0) if heat else np.zeros_like(e0)
    _, rho1, p1, q1 = zones(r1, v1, e1, dM, gam)
    Ph = 0.5 * (P0 + p1 + q1); rh = 0.5 * (r0 + r1)
    v2 = v0 + dt * (0.5 * (g0 + grav(t + dt, r1)) + pforce(rh, Ph, dm))
    h2 = 0.0
    if nu > 0.0:
        Vh = (FOURPI / 3) * (rh ** 3 - inner(rh) ** 3)
        v2, h2 = visc_solve(rh, dM / Vh, v2, dt, nu, dm)
    r2 = r0 + 0.5 * dt * (v0 + v2)
    V2 = (FOURPI / 3) * (r2 ** 3 - inner(r2) ** 3)
    if np.any(V2 <= 0.0):
        raise FloatingPointError('zone inverted (corrector)')
    e2 = np.maximum(e0 - Ph * (V2 - V0) / dM + h2, 0.0) if heat else np.zeros_like(e0)
    return r2, v2, e2, (float(np.sum(dM * h2)) if nu > 0.0 else 0.0)


def pick_dt(r, v, e, a_est, gam, dt_prev, dt_max):
    dr = r - inner(r); dv = np.abs(v - inner(v))
    cs = np.sqrt(gam * (gam - 1) * np.maximum(e, 0.0))
    d1 = CFL * np.min(dr / (cs + 4.0 * dv + 1e-30))
    d2 = 0.02 * np.min(r / np.maximum(np.abs(v), 1e-3))
    d3 = 0.05 * np.min(np.sqrt(r / np.maximum(np.abs(a_est), 1e-12)))
    return min(d1, d2, d3, dt_max, 1.1 * dt_prev)


# ------------------------------------------------------------------ KA1
def noh(N=400, gam=GAM, tend=0.6):
    r = np.linspace(1.0 / N, 1.0, N); MX = (FOURPI / 3) * r ** 3
    dM = np.diff(np.concatenate([[0.0], MX])); dm = 0.5 * (dM + np.concatenate([dM[1:], [0.0]]))
    v = -np.ones(N); e = np.full(N, 1e-12)
    E0 = float(np.sum(0.5 * dm * v * v) + np.sum(dM * e))
    grav = lambda t, rr: np.zeros_like(rr)
    t = 0.0; dt = 1e-6; n = 0
    while t < tend - 1e-15:
        dt = min(pick_dt(r, v, e, np.zeros(N), gam, dt, 1e-3), tend - t)
        r, v, e, _ = step(t, dt, r, v, e, dM, dm, grav, 0.0, gam); t += dt; n += 1
    rl = inner(r); V = (FOURPI / 3) * (r ** 3 - rl ** 3); rho = dM / V; rc = 0.5 * (r + rl)
    hot = rho > 32.0
    rsh = float(rc[hot].max()) if hot.any() else 0.0
    sel = (rc > 0.05 * rsh) & (rc < 0.9 * rsh)
    rho_post = float(np.sum(dM[sel]) / np.sum(V[sel])) if sel.any() else float('nan')
    E1 = float(np.sum(0.5 * dm * v * v) + np.sum(dM * e))
    return {'N': N, 'steps': n, 'r_shock': rsh, 'r_exact': tend / 3.0, 'rho_post': rho_post, 'rho_exact': 64.0,
            'E_rel': abs(E1 - E0) / abs(E0)}


# ------------------------------------------------------------------ set-up
def make_cos(footing):
    s = KD1['footings'][footing]['setting']
    return L.Cosmo(s['h'], s['omega_d'], s['omega_b'])


def make_grav(mode, cos, a0, Mb, MX, ti, eps, ramp):
    nb0 = cos.nbar0

    def grav(t, rr):
        a = cos.a_of_t(t)
        M = Mb * float(L.smoothstep((t - ti) / ramp)) if ramp > 0 else Mb
        g = (-L.G * M * rr / (rr * rr + eps * eps) ** 1.5 - L.G * MX / rr ** 2
             + (-(FOURPI / 3) * L.G * cos.rhob0 * a ** -3 + cos.OL * cos.H0 ** 2) * rr)
        if mode == 'seed':                     # FLD1's law term: the clock's own polarization, U(y) = a0 y/(a0 - |y|)
            y = np.clip(L.G * (MX - (FOURPI / 3) * nb0 * a ** -3 * rr ** 3) / rr ** 2, -0.999999 * a0, 0.999999 * a0)
            g = g + a0 * y / (a0 - np.abs(y))
        return g
    return grav


def diagnose(t, r, v, e, dM, MX, grav, gam, Mb_now, re_star):
    """VSH1's quantities (its own definitions) and this lane's standing statistic."""
    g = grav(t, r); rl = inner(r); rc = 0.5 * (r + rl)
    gz = np.abs(0.5 * (g + inner(g, g[0])))
    hot = (gam - 1) * e >= 0.05 * rc * gz
    R_sh = float(rc[hot].max()) if hot.any() else 0.0
    vz = 0.5 * (v + inner(v))
    S = None
    if re_star is not None:
        ins = rc <= re_star
        S = float(math.sqrt(np.sum(dM[ins] * vz[ins] ** 2) / np.sum(dM[ins] * rc[ins] * gz[ins]))) if ins.any() else None
    vref2 = L.G * (Mb_now + MX) / rc
    Sc = np.sqrt(np.cumsum(dM * vz ** 2) / np.cumsum(dM * vref2))
    ok = np.where(Sc <= 0.10)[0]
    ist = int(ok.max()) if ok.size else -1
    R_st = float(r[ist]) if ist >= 0 else 0.0
    hot2 = (gam - 1) * e >= 0.05 * vref2
    R_hot = float(rc[hot2].max()) if hot2.any() else 0.0
    infall = v <= 0.0
    R_ta = float(r[infall].max()) if infall.any() else 0.0
    return {'R_sh': R_sh, 'S': S, 'R_st': R_st, 'i_st': ist, 'R_hot_vref': R_hot, 'R_ta': R_ta,
            'n_zones_inside_re': int((rc <= re_star).sum()) if re_star is not None else None}


def evolve(name, cos, r, v, e, dM, MX, grav, nu, gam, heat, ti, tend, Mb, ramp, re_star, cap_s=28800.0):
    dm = 0.5 * (dM + np.concatenate([dM[1:], [0.0]]))
    T0 = time.time(); t = ti; dt = 1e-5; n = 0; status = 'done'; t_pass = None; hv_tot = 0.0; e_max = 0.0
    ck = os.path.join(CKPT, name + '.npz') if CKPT else ''
    if ck and os.path.exists(ck):
        z = np.load(ck); r, v, e = z['r'], z['v'], z['e']; t = float(z['t']); dt = float(z['dt']); n = int(z['n'])
        hv_tot = float(z['hv']); t_pass = float(z['tp']) if float(z['tp']) > 0 else None; e_max = float(z['emax'])
    a_est = grav(t, r); last = time.time()
    try:
        while t < tend - 1e-13:
            dt = min(pick_dt(r, v, e, a_est, gam, dt, 1e-3), tend - t)
            if dt < 1e-11:
                status = 'dt underflow'; break
            r, v, e, hv = step(t, dt, r, v, e, dM, dm, grav, nu, gam, heat)
            hv_tot += hv; t += dt; n += 1
            if n % 50 == 0:
                a_est = grav(t, r); e_max = max(e_max, float(e.max()))
                if re_star is not None and t_pass is None and n % 500 == 0:
                    Mn = Mb * float(L.smoothstep((t - ti) / ramp)) if ramp > 0 else Mb
                    if diagnose(t, r, v, e, dM, MX, grav, gam, Mn, re_star)['R_sh'] >= re_star:
                        t_pass = t
                if ck and (time.time() - last > 300 or STOP['flag']):
                    np.savez(ck, r=r, v=v, e=e, t=t, dt=dt, n=n, hv=hv_tot, tp=t_pass or -1.0, emax=e_max); last = time.time()
                if STOP['flag']:
                    status = 'stopped (SIGTERM, checkpointed)'; break
                if time.time() - T0 > cap_s:
                    status = 'stopped (wall-clock guard)'; break
    except FloatingPointError as ex:
        status = str(ex)
    d = diagnose(t, r, v, e, dM, MX, grav, gam, Mb, re_star)
    d.update({'status': status, 'steps': n, 'z_stop': 1.0 / cos.a_of_t(t) - 1.0,
              'z_pass': (1.0 / cos.a_of_t(t_pass) - 1.0) if t_pass is not None else None,
              'visc_heat_frac': hv_tot / max(float(np.sum(dM * e)), 1e-300), 'e_max': max(e_max, float(e.max())),
              'seconds': round(time.time() - T0, 1)})
    if status == 'done' and ck and os.path.exists(ck):
        os.remove(ck)
    return d, r, v, e


def run_seed(footing, lM, N, tag='', heat=True, nu_fac=1.0, z_end=0.0):
    cos = make_cos(footing); a0 = L.a0_of(footing); Mb = 10 ** lM; nb0 = cos.nbar0
    row = [x for x in AKS[footing]['rows'] if abs(x['logMb'] - lM) < 1e-9][0]
    nu = nu_fac * AKS[footing]['nu_F']
    XM = (Mb / ((FOURPI / 3) * nb0)) ** (1 / 3)
    X = np.logspace(math.log10(0.03 * XM), math.log10(15 * XM), N)
    MX = (FOURPI / 3) * nb0 * X ** 3; dM = np.diff(np.concatenate([[0.0], MX]))
    ai = 1 / 11.0; ti = cos.t_of_a(ai); tend = cos.t_of_a(1.0 / (1.0 + z_end)); ramp = 1.0 / L.TU
    r = X * ai; v = cos.H_of_a(ai) * r; e = np.zeros(N)
    grav = make_grav('seed', cos, a0, Mb, MX, ti, 1.0, ramp)
    name = f'seed_{footing}_{lM:g}_N{N}{tag}'
    d, r, v, e = evolve(name, cos, r, v, e, dM, MX, grav, nu, GAM, heat, ti, tend, Mb, ramp, row['r_e_star'])
    d['settled_vsh1_rule'] = bool(d['status'] == 'done' and d['R_sh'] >= row['r_e_star'] and d['S'] is not None and d['S'] <= 0.10)
    d.update({'name': name, 'mode': 'seed', 'footing': footing, 'logMb': lM, 'N': N, 'nu': nu, 'nu_over_nuF': nu_fac,
              'heat': heat, 'gamma': GAM, 'a0': a0, 'Mb': Mb, 'eps': 1.0, 'r_e_star': row['r_e_star'], 'R_cap': row['R_cap'],
              'r': r.tolist(), 'v': v.tolist(), 'e': e.tolist(), 'MX': MX.tolist()})
    return d


def run_cosmo(footing, A, N=300, tag='', cos=None, lM=10.5, zi=30.0, cap=0.3, xlo=0.03, ramp_gyr=1.0, eps=1.0,
              name=None):
    cos = cos or make_cos(footing); Mb = 10 ** lM; nb0 = cos.nbar0
    XM = (Mb / ((FOURPI / 3) * nb0)) ** (1 / 3)
    fac = max(1.0, 23.0 * abs(A)) ** (1 / 3)
    X = np.logspace(math.log10(xlo * XM), math.log10(15 * XM * fac), N)
    MX = (FOURPI / 3) * nb0 * X ** 3; dM = np.diff(np.concatenate([[0.0], MX]))
    ai = 1 / (1.0 + zi); ti = cos.t_of_a(ai); tend = cos.t_of_a(1.0); ramp = ramp_gyr / L.TU
    dbar = np.clip(A * Mb / MX, -cap, cap)
    r = X * ai * (1 - dbar / 3); v = cos.H_of_a(ai) * X * ai * (1 - 2 * dbar / 3); e = np.zeros(N)
    grav = make_grav('cosmo', cos, 0.0, Mb, MX, ti, eps, ramp)
    name = name or f'cosmo_{footing}_A{A:g}_N{N}{tag}'
    d, r, v, e = evolve(name, cos, r, v, e, dM, MX, grav, 0.0, GAM, True, ti, tend, Mb, ramp, None)
    ist = d['i_st']
    d.update({'name': name, 'mode': 'cosmo', 'footing': footing, 'logMb': lM, 'N': N, 'A': A, 'zi': zi, 'cap': cap,
              'gamma': GAM, 'Mb': Mb, 'eps': eps, 'host_over_Mb': float(MX[ist] / Mb) if ist >= 0 else 0.0,
              'r': r.tolist(), 'v': v.tolist(), 'e': e.tolist(), 'MX': MX.tolist()})
    return d


def dust_rta(footing, lM, N=600):
    """KA2: this lane's seed force law and starting state with every fluid term off (independent shells, velocity
    Verlet; shells inside the flux-cap wall max(1.2 sqrt(G Q_ex/a0), 0.3 kpc) held at the wall, as FLD1 A1)."""
    cos = make_cos(footing); a0 = L.a0_of(footing); Mb = 10 ** lM; nb0 = cos.nbar0
    XM = (Mb / ((FOURPI / 3) * nb0)) ** (1 / 3)
    X = np.logspace(math.log10(0.03 * XM), math.log10(15 * XM), N); MX = (FOURPI / 3) * nb0 * X ** 3
    ai = 1 / 11.0; ti = cos.t_of_a(ai); tend = cos.t_of_a(1.0); ramp = 1.0 / L.TU
    r = X * ai; v = cos.H_of_a(ai) * r
    grav = make_grav('seed', cos, a0, Mb, MX, ti, 1.0, ramp)
    t = ti; n = 0
    while t < tend - 1e-13:
        acc = grav(t, r)
        dt = min(0.02 * np.min(r / np.maximum(np.abs(v), 1e-3)), 0.05 * np.min(np.sqrt(r / np.maximum(np.abs(acc), 1e-12))),
                 1e-3, tend - t)
        rn = r + dt * v + 0.5 * dt * dt * acc
        a = cos.a_of_t(t + dt)
        wall = np.maximum(1.2 * np.sqrt(L.G * np.maximum(MX - (FOURPI / 3) * nb0 * a ** -3 * rn ** 3, 0.0) / a0), 0.3)
        hit = rn < wall
        rn = np.where(hit, wall, rn)
        vn = v + 0.5 * dt * (acc + grav(t + dt, rn))
        v = np.where(hit, np.abs(vn), vn); r = rn; t += dt; n += 1
    infall = v <= 0.0
    return {'footing': footing, 'logMb': lM, 'R_ta': float(r[infall].max()) if infall.any() else 0.0, 'steps': n}


def ka4(N=300):
    """EdS, point seed from the start (no ramp), self-gravitating cold fluid, gamma 5/3, shock capture only."""
    cos = EdS(); Ms = 1e10
    d = run_cosmo('EdS', 0.0, N=N, cos=cos, lM=10.0, zi=300.0, xlo=0.3, ramp_gyr=0.0, eps=1.0, name=f'ka4_EdS_N{N}')
    r = np.array(d['r']); MX = np.array(d['MX']); e = np.array(d['e'])
    rl = inner(r); rc = 0.5 * (r + rl); dM = np.diff(np.concatenate([[0.0], MX])); V = (FOURPI / 3) * (r ** 3 - rl ** 3)
    rho = dM / V; Rta = d['R_ta']
    sel = (rc >= 0.02 * Rta) & (rc <= 0.2 * Rta)
    slope = float(np.polyfit(np.log(rc[sel]), np.log(rho[sel]), 1)[0]) if sel.sum() > 3 else float('nan')
    d.update({'shock_over_Rta': d['R_hot_vref'] / Rta if Rta > 0 else None, 'Rst_over_Rta': d['R_st'] / Rta if Rta > 0 else None,
              'rho_slope': slope, 'n_slope_zones': int(sel.sum()), 'M_ta_over_seed': float(MX[np.searchsorted(r, Rta)] / Ms)})
    return d


def save(d):
    os.makedirs(RUNS, exist_ok=True)
    json.dump(d, open(os.path.join(RUNS, d['name'] + '.json'), 'w'))
    keys = [k for k in d if k not in ('r', 'v', 'e', 'MX')]
    print(json.dumps({k: d[k] for k in keys}))


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'ka1':
        os.makedirs(RUNS, exist_ok=True)
        k = noh(); k['name'] = 'ka1_noh'
        k['pass'] = bool(abs(k['r_shock'] / k['r_exact'] - 1) <= 0.05 and abs(k['rho_post'] / 64 - 1) <= 0.15 and k['E_rel'] <= 0.02)
        json.dump(k, open(os.path.join(RUNS, 'ka1_noh.json'), 'w')); print(json.dumps(k))
    elif mode == 'ka2':
        os.makedirs(RUNS, exist_ok=True)
        a = dust_rta('canonical', 9.0); b = dust_rta('canonical', 11.5)
        k = {'name': 'ka2_rta', 'a': a, 'b': b, 'fld1': [88.0, 600.0],
             'pass': bool(abs(a['R_ta'] / 88.0 - 1) <= 0.03 and abs(b['R_ta'] / 600.0 - 1) <= 0.03)}
        json.dump(k, open(os.path.join(RUNS, 'ka2_rta.json'), 'w')); print(json.dumps(k))
    elif mode == 'ka4':
        save(ka4(int(sys.argv[2]) if len(sys.argv) > 2 else 300))
    elif mode == 'seed':
        f, lM, N = sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
        tag = sys.argv[5] if len(sys.argv) > 5 else ''
        heat = (sys.argv[6] != '0') if len(sys.argv) > 6 else True
        nuf = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
        save(run_seed(f, lM, N, tag, heat, nuf))
    elif mode == 'cosmo':
        f, A = sys.argv[2], float(sys.argv[3])
        N = int(sys.argv[4]) if len(sys.argv) > 4 else 300
        tag = sys.argv[5] if len(sys.argv) > 5 else ''
        save(run_cosmo(f, A, N, tag))
