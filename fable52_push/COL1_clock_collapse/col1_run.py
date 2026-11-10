#!/usr/bin/env python3
"""COL1 Part 2 driver: one evolution row.

    python3 col1_run.py --mode hubble --mu 3.71 --footing canonical --logMb 10.45 --J 1200 [--visc 2] [--law law|off|neg|flip|lin]
                        [--xout 8000] [--tag NAME] [--snapdir DIR]

Writes runs/<name>.json (summary, reads every 0.25 Gyr, the event) and <snapdir>/<name>.npz (snapshots, kept outside the
repo). Criteria: FROZEN_CRITERIA.md section 5. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import argparse, json, math, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import col1_lib as L
import col1_shell as S

KD1 = json.load(open(os.path.join(HERE, '../../closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json')))
RADII = [10.0, 30.0, 100.0, 300.0]
DT_FLOOR = 1e-20          # tu; a STALL below it is numerical, not a frozen event


def mph_law(R, Mb, a0, eps):
    gN = L.G * Mb * R / (R * R + eps * eps) ** 1.5
    return R * R * (L.law_g(gN, a0) - gN) / L.G


def reads(md, t, acc, cos, mode, ti):
    r, v, h = md.r, md.v, md.h
    accf, ah, ag, av = md.accel(t, r, v, want=True)
    Mb = md.Mb_t(t)
    Md = md.Md_nodes()
    g = np.abs(ag); vc = np.sqrt(np.maximum(g * r, 1e-300))
    # Phi relative to 300 kpc from the gravitational acceleration (trapezoid on the nodes)
    out = {'t_gyr': t * L.TU, 't_since_start_gyr': (t - ti) * L.TU, 'Mb_now': Mb}
    if mode == 'hubble':
        out['z'] = 1 / cos.a_of_t(t) - 1
    out['rmin_kpc'] = float(r[1])
    rows = {}
    seg = 0.5 * (np.abs(ag[1:]) + np.abs(ag[:-1])) * np.diff(r)
    cumPhi = np.concatenate([[0.0], np.cumsum(seg)])           # Phi(r_j) - Phi(0) along the nodes
    for R in RADII:
        if R >= r[-1]:
            continue
        sel = (r > 0) & (r <= R)
        sel[0] = False; sel[-1] = False
        MN = float(np.interp(R, r, md.Mlag)); MdR = float(np.interp(R, r, Md))
        Mph = float(mph_law(R, Mb, md.a0, md.eps)) if Mb > 0 else 0.0
        d = {'M_N': MN, 'M_d': MdR, 'M_Pi': MN - MdR, 'M_ph_law': Mph,
             'M_N_over_M_ph': MN / Mph if Mph > 0 else None, 'M_N_over_Mb': MN / Mb if Mb > 0 else None}
        if sel.any():
            d['max_v_over_vc'] = float(np.max(np.abs(v[sel]) / vc[sel]))
            d['max_acc_over_g'] = float(np.max(np.abs(accf[sel]) / np.maximum(g[sel], 1e-300)))
            d['n_nodes'] = int(sel.sum())
        if md.mu > 0:
            hR = float(np.interp(R, r, h)); h300 = float(np.interp(300.0, r, h))
            phiR = float(np.interp(R, r, cumPhi)); phi300 = float(np.interp(300.0, r, cumPhi))
            nst = h300 + (phi300 - phiR)
            d['n_d_over_static'] = hR / nst if nst != 0 else None
        rows[f'{R:g}'] = d
    out['radii'] = rows
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', default='hubble'); ap.add_argument('--mu', type=float, required=True)
    ap.add_argument('--footing', default='canonical'); ap.add_argument('--logMb', type=float, default=10.45)
    ap.add_argument('--J', type=int, default=1200); ap.add_argument('--visc', type=float, default=0.0)
    ap.add_argument('--law', default='law'); ap.add_argument('--xout', type=float, default=8000.0)
    ap.add_argument('--tag', default=''); ap.add_argument('--snapdir', default=os.environ.get('COL1_SNAPDIR', '/tmp'))
    ap.add_argument('--tmax_gyr', type=float, default=None)
    a = ap.parse_args()
    name = a.tag or f'{a.mode}_mu{a.mu:g}_{a.footing}_M{a.logMb:g}_J{a.J}' + (f'_visc{a.visc:g}' if a.visc else '') + \
        ('' if a.law == 'law' else f'_{a.law}') + ('' if a.xout == 8000.0 else f'_X{a.xout:g}')
    os.makedirs(os.path.join(HERE, 'runs'), exist_ok=True)
    os.makedirs(a.snapdir, exist_ok=True)
    T = time.time()
    if a.mode == 'hubble':
        md, ti, tend, cos = S.hubble_model(a.mu, a.footing, a.logMb, a.J, KD1, lawkind=a.law, Xout=a.xout, visc=a.visc)
    else:
        md, ti, tend, cos = S.rest_model(a.mu, a.footing, a.logMb, a.J, KD1, lawkind=a.law, Xout=a.xout, visc=a.visc)
    if a.tmax_gyr:
        tend = min(tend, ti + a.tmax_gyr / L.TU)
    R, SN = [], {'t': [], 'r': [], 'v': [], 'h': []}

    def snap(m, t, acc, final=False):
        try:
            R.append(reads(m, t, acc, cos, a.mode, ti))
        except Exception as ex:      # e.g. after shells crossed
            R.append({'t_gyr': t * L.TU, 'error': str(ex)})
        SN['t'].append(t); SN['r'].append(m.r.copy()); SN['v'].append(m.v.copy()); SN['h'].append(m.h.copy())
    t, steps, ev = md.run(ti, tend, 1e-3, 0.25 / L.TU, on_snap=snap, dt_floor=DT_FLOOR)
    if ev and 't' in ev:
        ev['t_gyr'] = ev['t'] * L.TU; ev['t_since_start_gyr'] = (ev['t'] - ti) * L.TU
        if 'r_kpc' in ev:
            ev['core'] = bool(ev['r_kpc'] < 3.0)
        if a.mode == 'hubble':
            ev['z'] = 1 / cos.a_of_t(ev['t']) - 1
    res = {'name': name, 'args': {k: v for k, v in vars(a).items() if k != 'snapdir'}, 'X': md.X.tolist() if a.J <= 1300 else None, 'steps': steps,
           'newton_solves': md.nsolve, 'newton_iterations': md.newton_its, 'wall_s': time.time() - T,
           't_start_gyr': ti * L.TU, 't_end_gyr': t * L.TU, 'event': ev, 'reads': R,
           'note': 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.'}
    json.dump(res, open(os.path.join(HERE, 'runs', name + '.json'), 'w'), indent=1, default=float)
    np.savez_compressed(os.path.join(a.snapdir, name + '.npz'), t=np.array(SN['t']), r=np.array(SN['r']),
                        v=np.array(SN['v']), h=np.array(SN['h']), X=md.X, m=md.m, Mlag=md.Mlag)
    e = ev or {'kind': 'none'}
    last = next((x['radii'] for x in reversed(R) if 'radii' in x), {})
    print(f'{name}: steps {steps}, wall {time.time() - T:.1f}s, end t {(t - ti) * L.TU:.4f} Gyr after start; event {e.get("kind")} '
          f'{e.get("reason", "")} r {e.get("r_kpc", float("nan")):.4g} kpc; last read M_N/M_ph at 10/30/100/300: '
          + ' / '.join(f'{last[k]["M_N_over_M_ph"]:.3g}' if k in last and last[k]['M_N_over_M_ph'] else '-' for k in ('10', '30', '100', '300')))


if __name__ == '__main__':
    main()
