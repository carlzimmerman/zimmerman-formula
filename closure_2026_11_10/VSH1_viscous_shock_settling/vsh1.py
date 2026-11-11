#!/usr/bin/env python3
"""VSH1: AKS1's estimate T7, computed. FLD1's shell equation plus Lagrangian hydrodynamics of the clock's charge:
pressure (gamma), traceless shear viscosity nu (implicit), von Neumann-Richtmyer shock capture. See FROZEN_CRITERIA.md.

    python3 vsh1.py ka | grade | scan | mutate

Units: kpc, km/s, Msun; time kpc/(km/s). Reads (read-only) col1_lib.py, kd1.json and aks1_t.json.
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys, time
import numpy as np
from scipy.linalg import solve_banded
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'fable52_push', 'COL1_clock_collapse'))
import col1_lib as L                                                                    # noqa: E402
KD1 = json.load(open(os.path.join(REPO, 'closure_2026_11_06', 'KD1_unpinned_kq_dust', 'kd1.json')))
AKS = json.load(open(os.path.join(REPO, 'toe_2026_11_10', 'AKS1_acceleration_keyed_sink', 'aks1_t.json')))['T7']
EPS = 1.0; CQ = 2.0; CL = 0.3; CFL = 0.3; FOURPI = 4 * math.pi
MASSES = (9.0, 10.5, 11.5)
CAP_STEPS = int(float(os.environ.get('VSH1_CAP_STEPS', '6e7'))); CAP_S = 14400.0; RS = 0.3; FW = 1.2   # A1


def hydro_step(t, dt, r, v, e, dM, dm, grav, nu, gam, heat=True):
    """One staggered step. v is time-centred. Returns r, v, e, heat added by the physical viscosity (sum dM de)."""
    rl = np.concatenate([[0.0], r[:-1]]); vl = np.concatenate([[0.0], v[:-1]])
    V = (FOURPI / 3) * (r ** 3 - rl ** 3); rho = dM / V
    dv = v - vl
    cs = np.sqrt(gam * (gam - 1) * np.maximum(e, 0.0))
    comp = (r * r * v - rl * rl * vl) < 0.0
    q = np.where(comp, rho * (CQ * dv * dv + CL * cs * np.abs(dv)), 0.0)
    p = (gam - 1) * rho * e
    P = p + q
    a = grav(t, r) - FOURPI * r * r * (np.concatenate([P[1:], [0.0]]) - P) / dm
    v = v + dt * a
    hv = 0.0
    if nu > 0.0:
        dr = r - rl
        al = np.zeros_like(r); be = np.zeros_like(r)
        al[1:] = 1.0 / dr[1:]; be[1:] = 1.0 / (r[1:] + rl[1:])
        w = (4.0 / 3.0) * rho * nu * (0.5 * (r + rl)) ** 3; w[0] = 0.0
        pref = FOURPI / (dm * r)
        wn = np.concatenate([w[1:], [0.0]]); aln = np.concatenate([al[1:], [0.0]]); ben = np.concatenate([be[1:], [0.0]])
        U = pref * wn * (aln - ben)
        D = -pref * (wn * (aln + ben) + w * (al - be))
        Lo = pref * w * (al + be)
        ab = np.zeros((3, r.size))
        ab[0, 1:] = -dt * U[:-1]; ab[1, :] = 1.0 - dt * D; ab[2, :-1] = -dt * Lo[1:]
        v = solve_banded((1, 1), ab, v)
        vl2 = np.concatenate([[0.0], v[:-1]])
        s = v * (al - be) - vl2 * (al + be); s[0] = 0.0
        hv = (4.0 / 3.0) * nu * s * s * dt
    rn = r + dt * v
    rln = np.concatenate([[0.0], rn[:-1]])
    Vn = (FOURPI / 3) * (rn ** 3 - rln ** 3)
    if np.any(Vn <= 0.0):
        raise FloatingPointError('zone inverted')
    dV = Vn - V
    if heat:
        en = (e - (0.5 * p + q) * dV / dM + hv) / (1.0 + 0.5 * (gam - 1) * (dM / Vn) * dV / dM)
        en = np.maximum(en, 0.0)
    else:
        en = np.zeros_like(e)
    return rn, v, en, float(np.sum(dM * hv)) if nu > 0.0 else 0.0


def pick_dt(r, v, e, a_est, gam, dt_prev, dt_max):
    rl = np.concatenate([[0.0], r[:-1]]); vl = np.concatenate([[0.0], v[:-1]])
    dr = r - rl; dv = np.abs(v - vl)
    cs = np.sqrt(gam * (gam - 1) * np.maximum(e, 0.0))
    d1 = CFL * np.min(dr / (cs + 2.0 * dv + 1e-30))
    d2 = 0.02 * np.min(r / np.maximum(np.abs(v), 1e-3))
    d3 = 0.05 * np.min(np.sqrt(r / np.maximum(np.abs(a_est), 1e-12)))
    return min(d1, d2, d3, dt_max, 1.2 * dt_prev)


def noh(N=400, gam=5.0 / 3.0, tend=0.6):
    r = np.linspace(1.0 / N, 1.0, N); MX = (FOURPI / 3) * r ** 3
    dM = np.diff(np.concatenate([[0.0], MX])); dm = 0.5 * (dM + np.concatenate([dM[1:], [0.0]]))
    v = -np.ones(N); e = np.full(N, 1e-12)
    E0 = float(np.sum(0.5 * dm * v * v) + np.sum(dM * e))
    grav = lambda t, rr: np.zeros_like(rr)
    t = 0.0; dt = 1e-6; n = 0
    while t < tend - 1e-15:
        dt = min(pick_dt(r, v, e, np.zeros(N), gam, dt, 1e-3), tend - t)
        r, v, e, _ = hydro_step(t, dt, r, v, e, dM, dm, grav, 0.0, gam); t += dt; n += 1
    rl = np.concatenate([[0.0], r[:-1]]); V = (FOURPI / 3) * (r ** 3 - rl ** 3); rho = dM / V; rc = 0.5 * (r + rl)
    hot = rho > 32.0
    rsh = float(rc[hot].max()) if hot.any() else 0.0
    sel = (rc > 0.05 * rsh) & (rc < 0.9 * rsh)
    rho_post = float(np.sum(dM[sel]) / np.sum(V[sel])) if sel.any() else float('nan')
    E1 = float(np.sum(0.5 * dm * v * v) + np.sum(dM * e))
    return {'N': N, 'steps': n, 'r_shock': rsh, 'r_exact': tend / 3.0, 'rho_post': rho_post, 'rho_exact': 64.0,
            'E_rel': abs(E1 - E0) / E0}


def collapse(args):
    (footing, lM, N, nu_fac, gam, heat, baryons, z_end, tag) = args
    T0 = time.time()
    s = KD1['footings'][footing]['setting']; cos = L.Cosmo(s['h'], s['omega_d'], s['omega_b'])
    a0 = L.a0_of(footing); Mb = 10 ** lM; nb0 = cos.nbar0
    row = [x for x in AKS[footing]['rows'] if abs(x['logMb'] - lM) < 1e-9][0]
    re_star = row['r_e_star']; Rcap = row['R_cap']; nuF = AKS[footing]['nu_F']; nu = nu_fac * nuF
    XM = (Mb / ((FOURPI / 3) * nb0)) ** (1 / 3)
    X = np.logspace(math.log10(0.03 * XM), math.log10(15 * XM), N)
    MX = (FOURPI / 3) * nb0 * X ** 3
    dM = np.diff(np.concatenate([[0.0], MX])); dm = 0.5 * (dM + np.concatenate([dM[1:], [0.0]]))
    zi = 10.0; ai = 1 / (1 + zi); ti = cos.t_of_a(ai); tend = cos.t_of_a(1.0 / (1.0 + z_end))
    r = X * ai; v = cos.H_of_a(ai) * r; e = np.zeros(N)
    ramp = 1.0 / L.TU
    Mb_eff = Mb if baryons else 0.0

    def grav(t, rr):
        a = cos.a_of_t(t)
        M = Mb_eff * float(L.smoothstep((t - ti) / ramp))
        g = (-L.G * M * rr / (rr * rr + EPS * EPS) ** 1.5 - L.G * MX / rr ** 2
             + (-(FOURPI / 3) * L.G * cos.rhob0 * a ** -3 + cos.OL * cos.H0 ** 2) * rr)
        y = np.clip(L.G * (MX - (FOURPI / 3) * nb0 * a ** -3 * rr ** 3) / rr ** 2, -0.999999 * a0, 0.999999 * a0)
        return g + a0 * y / (a0 - np.abs(y))

    def diag(t):
        g = grav(t, r); rl = np.concatenate([[0.0], r[:-1]]); rc = 0.5 * (r + rl)
        gz = np.abs(0.5 * (g + np.concatenate([[g[0]], g[:-1]])))
        hot = (gam - 1) * e >= 0.05 * rc * gz
        rsh = float(rc[hot].max()) if hot.any() else 0.0
        return g, rl, rc, gz, hot, rsh

    t = ti; dt = 1e-5; n = 0; status = 'done'; t_pass = None; e_max = 0.0; heat_visc = 0.0
    a_est = grav(t, r)
    try:
        while t < tend - 1e-13:
            dt = min(pick_dt(r, v, e, a_est, gam, dt, 1e-3), tend - t)
            if dt < 1e-10:
                status = 'dt underflow'; break
            r, v, e, hv = hydro_step(t, dt, r, v, e, dM, dm, grav, nu, gam, heat)
            heat_visc += hv
            t += dt; n += 1
            if n % 50 == 0:
                a_est = grav(t, r); e_max = max(e_max, float(e.max()))
                if t_pass is None and n % 200 == 0 and diag(t)[5] >= re_star:
                    t_pass = t
            if n > CAP_STEPS or time.time() - T0 > CAP_S:
                status = 'stopped (cap)'; break
    except FloatingPointError as ex:
        status = str(ex)
    g, rl, rc, gz, hot, rsh = diag(t)
    vz = 0.5 * (v + np.concatenate([[0.0], v[:-1]]))
    inside = rc <= re_star
    S = float(math.sqrt(np.sum(dM[inside] * vz[inside] ** 2) / np.sum(dM[inside] * rc[inside] * gz[inside]))) \
        if inside.any() else None
    infall = v <= 0.0
    Rta = float(r[infall].max()) if infall.any() else 0.0
    V = (FOURPI / 3) * (r ** 3 - rl ** 3); rho = dM / V; P = (gam - 1) * rho * e
    ap = -FOURPI * r * r * (np.concatenate([P[1:], [0.0]]) - P) / dm
    nin = r <= re_star
    hres = float(np.median(np.abs(ap[nin] + g[nin]) / np.abs(g[nin]))) if nin.sum() > 2 else None
    ish = int(np.searchsorted(r, rsh)) if rsh > 0 else 0
    Q_in = float(MX[min(ish, N - 1)] / Mb) if rsh > 0 else 0.0
    Mlaw = math.sqrt(Mb * a0 / L.G) * rsh / Mb if rsh > 0 else 0.0
    settled = bool(status == 'done' and rsh >= re_star and S is not None and S <= 0.10)
    z_pass = (1.0 / cos.a_of_t(t_pass) - 1.0) if t_pass is not None else None
    z_stop = 1.0 / cos.a_of_t(t) - 1.0
    return {'tag': tag, 'footing': footing, 'logMb': lM, 'N': N, 'nu': nu, 'nu_over_nuF': nu_fac, 'gamma': gam,
            'heat': heat, 'baryons': baryons, 'z_end': z_end, 'status': status, 'z_stop': z_stop, 'steps': n,
            'r_e_star': re_star, 'R_cap': Rcap, 'R_ta': Rta, 'R_sh': rsh, 'S': S, 'settled': settled,
            'n_zones_inside': int(inside.sum()), 'hydrostatic_residual': hres, 'z_pass': z_pass,
            't_pass_gyr': (t_pass - ti) * L.TU if t_pass is not None else None,
            'R_sh_over_R_ta': rsh / Rta if Rta > 0 else None, 'R_sh_over_R_cap': rsh / Rcap,
            'charge_inside_R_sh_over_Mb': Q_in, 'law_halo_at_R_sh_over_Mb': Mlaw,
            'charge_over_law_halo': Q_in / Mlaw if Mlaw > 0 else None, 'e_max': max(e_max, float(e.max())),
            'visc_heat_frac': heat_visc / max(float(np.sum(dM * e)), 1e-300), 'seconds': round(time.time() - T0, 1)}


def dust_rta(footing, lM, N=600):
    """A1's KA3': the lane's force law and starting state with every fluid term off. Returns R_ta at z = 0."""
    s = KD1['footings'][footing]['setting']; cos = L.Cosmo(s['h'], s['omega_d'], s['omega_b'])
    a0 = L.a0_of(footing); Mb = 10 ** lM; nb0 = cos.nbar0
    XM = (Mb / ((FOURPI / 3) * nb0)) ** (1 / 3)
    X = np.logspace(math.log10(0.03 * XM), math.log10(15 * XM), N); MX = (FOURPI / 3) * nb0 * X ** 3
    zi = 10.0; ai = 1 / (1 + zi); ti = cos.t_of_a(ai); tend = cos.t_of_a(1.0)
    r = X * ai; v = cos.H_of_a(ai) * r; ramp = 1.0 / L.TU

    def grav(t, rr):
        a = cos.a_of_t(t); M = Mb * float(L.smoothstep((t - ti) / ramp))
        g = (-L.G * M * rr / (rr * rr + EPS * EPS) ** 1.5 - L.G * MX / rr ** 2
             + (-(FOURPI / 3) * L.G * cos.rhob0 * a ** -3 + cos.OL * cos.H0 ** 2) * rr)
        y = np.clip(L.G * (MX - (FOURPI / 3) * nb0 * a ** -3 * rr ** 3) / rr ** 2, -0.999999 * a0, 0.999999 * a0)
        return g + a0 * y / (a0 - np.abs(y))

    t = ti; A = grav(t, r); n = 0
    while t < tend - 1e-13:
        dt = min(0.02 * np.min(r / np.maximum(np.abs(v), 1e-3)), 0.05 * np.min(np.sqrt(r / np.maximum(np.abs(A), 1e-12))),
                 1e-3, tend - t)
        v = v + 0.5 * dt * A; r = r + dt * v
        a = cos.a_of_t(t + dt)
        wall = np.maximum(np.sqrt(L.G * np.maximum(MX - (FOURPI / 3) * nb0 * a ** -3 * r ** 3, 0.0) / a0) * FW, RS)
        hit = r < wall
        r = np.where(hit, wall, r); v = np.where(hit, np.abs(v), v)
        t += dt; A = grav(t, r); v = v + 0.5 * dt * A; n += 1
    infall = v <= 0.0
    return {'footing': footing, 'logMb': lM, 'R_ta': float(r[infall].max()) if infall.any() else 0.0, 'steps': n}


def fmt(x, f='.3g'):
    return 'n/a' if x is None else format(x, f)


def line(d):
    return (f"{d['tag']:>10} {d['footing']:>9} logMb {d['logMb']:>4} N {d['N']} nu/nuF {d['nu_over_nuF']:g} gam {d['gamma']:.3f}: "
            f"{d['status']} (z {d['z_stop']:.2f}); R_ta {d['R_ta']:.1f} R_sh {d['R_sh']:.1f} r_e* {d['r_e_star']:.1f} S {fmt(d['S'])} "
            f"-> {'SETTLED' if d['settled'] else 'not settled'}; z_pass {fmt(d['z_pass'])}; R_sh/R_ta {fmt(d['R_sh_over_R_ta'])}; "
            f"R_sh/R_cap {fmt(d['R_sh_over_R_cap'])}; charge/law halo at R_sh {fmt(d['charge_over_law_halo'])} "
            f"({fmt(d['charge_inside_R_sh_over_Mb'])} vs {fmt(d['law_halo_at_R_sh_over_Mb'])} M_b); hydrostatic res "
            f"{fmt(d['hydrostatic_residual'])}; zones inside {d['n_zones_inside']}; visc heat frac {fmt(d['visc_heat_frac'])}; "
            f"steps {d['steps']}, {d['seconds']} s")


def run_set(name, jobs, procs=6):
    with Pool(min(procs, len(jobs))) as pool:
        res = pool.map(collapse, jobs)
    out = [line(d) for d in res]
    return res, out


def save(name, obj, out):
    json.dump(obj, open(os.path.join(HERE, f'vsh1_{name}.json'), 'w'), indent=1)
    out.append('Adopts nothing. kappa = 1/2 FITTED; not theory closed.')
    open(os.path.join(HERE, f'vsh1_{name}.out'), 'w').write('\n'.join(out) + '\n')
    print('\n'.join(out))


G53 = 5.0 / 3.0
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'ka':
        out = []; res = {}
        k1 = noh(); ok1 = (abs(k1['r_shock'] / k1['r_exact'] - 1) <= 0.05 and abs(k1['rho_post'] / 64 - 1) <= 0.15
                           and k1['E_rel'] <= 0.02)
        res['KA1'] = dict(k1, **{'pass': bool(ok1)})
        out.append(f"KA1 Noh: r_shock {k1['r_shock']:.4f} (exact {k1['r_exact']:.4f}), post-shock density {k1['rho_post']:.2f} "
                   f"(64), energy drift {k1['E_rel']:.2e} -> {'PASS' if ok1 else 'FAIL'}")
        jobs = [('canonical', 10.5, 600, 1.0, G53, True, False, 0.0, 'KA2'),
                ('canonical', 10.5, 300, 1.0, G53, True, True, 0.0, 'KA4lo'),
                ('canonical', 10.5, 600, 1.0, G53, True, True, 0.0, 'KA4hi')]
        rr, lines = run_set('ka', jobs); out += lines
        d = {x['tag']: x for x in rr}
        ok2 = d['KA2']['status'] == 'done' and (G53 - 1) * d['KA2']['e_max'] <= 1e-6 and d['KA2']['R_sh'] == 0.0
        k3a = dust_rta('canonical', 9.0); k3b = dust_rta('canonical', 11.5)
        ok3 = (abs(k3a['R_ta'] / 88.0 - 1) <= 0.03 and abs(k3b['R_ta'] / 600.0 - 1) <= 0.03)
        lo, hi = d['KA4lo'], d['KA4hi']
        ok4 = (hi['R_sh'] > 0 and abs(lo['R_sh'] / hi['R_sh'] - 1) <= 0.10 and lo['settled'] == hi['settled'])
        res.update({'KA2': dict(d['KA2'], **{'pass': bool(ok2)}), 'KA3prime': {'a': k3a, 'b': k3b, 'pass': bool(ok3)},
                    'KA4': {'lo': lo, 'hi': hi, 'pass': bool(ok4)}})
        out.append(f"KA2 Hubble flow (no baryons): max (gamma-1)e {(G53 - 1) * d['KA2']['e_max']:.2e}, R_sh {d['KA2']['R_sh']:.1f} "
                   f"-> {'PASS' if ok2 else 'FAIL'}")
        out.append(f"KA3' (A1) fluid terms off, R_ta(z 0): {k3a['R_ta']:.1f} (FLD1 88) and {k3b['R_ta']:.1f} (FLD1 600) -> "
                   f"{'PASS' if ok3 else 'FAIL'}")
        out.append(f"KA4 resolution: R_sh {lo['R_sh']:.1f} (N 300) vs {hi['R_sh']:.1f} (N 600); settled {lo['settled']} / "
                   f"{hi['settled']} -> {'PASS' if ok4 else 'FAIL'}")
        res['all_pass'] = bool(ok1 and ok2 and ok3 and ok4)
        out.append(f"known answers: {'ALL PASS' if res['all_pass'] else 'FAIL'}")
        save('ka', res, out)
    elif mode == 'grade':
        jobs = [(f, m, 600, 1.0, G53, True, True, 0.0, 'grade') for f in ('canonical', 'alt') for m in MASSES]
        rr, out = run_set('grade', jobs)
        ka = json.load(open(os.path.join(HERE, 'vsh1_ka.json')))['all_pass']
        lab = {}
        for f in ('canonical', 'alt'):
            st = [x['settled'] for x in rr if x['footing'] == f]
            lab[f] = 'NO VERDICT' if not ka else ('SETTLES BY SHOCK' if all(st) else 'DOES NOT SETTLE')
            out.append(f'LABEL {f}: {lab[f]} (settled at log M_b 9 / 10.5 / 11.5: {st}; known answers pass: {ka})')
        save('grade', {'runs': rr, 'label': lab, 'known_answers_pass': ka}, out)
    elif mode == 'scan':
        jobs = [('canonical', m, 600, nf, G53, True, True, 0.0, f'nu{nf:g}') for nf in (0.0, 0.1) for m in MASSES]
        jobs += [('canonical', 11.5, 600, 10.0, G53, True, True, 0.0, 'nu10'),
                 ('canonical', 11.5, 600, 1.0, 4.0 / 3.0, True, True, 0.0, 'gam4/3')]
        rr, out = run_set('scan', jobs, procs=5)
        save('scan', {'runs': rr}, out)
    elif mode == 'mutate':
        jobs = [('canonical', m, 600, 1.0, G53, False, True, 0.0, 'M1') for m in MASSES]
        jobs += [('canonical', m, 600, 1.0, G53, True, False, 0.0, 'M2') for m in MASSES]
        jobs += [('canonical', 11.5, 600, 1.0, G53, True, True, 6.0, 'M3')]
        rr, out = run_set('MUTATE', jobs, procs=7)
        b1 = not any(x['settled'] for x in rr if x['tag'] == 'M1')
        b2 = not any(x['settled'] for x in rr if x['tag'] == 'M2')
        b3 = not any(x['settled'] for x in rr if x['tag'] == 'M3')
        out.append(f"M1 heat removed: {'BITES' if b1 else 'DOES NOT BITE'}; M2 no baryons: {'BITES' if b2 else 'DOES NOT BITE'}; "
                   f"M3 stopped at z 6: {'BITES' if b3 else 'DOES NOT BITE'}")
        save('MUTATE', {'runs': rr, 'bites': {'M1': b1, 'M2': b2, 'M3': b3}}, out)
