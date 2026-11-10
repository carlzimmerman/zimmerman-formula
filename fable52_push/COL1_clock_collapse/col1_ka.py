#!/usr/bin/env python3
"""COL1 known answers KA2-KA7 for the shell solver (KA1 = col1_system.py).

    python3 col1_ka.py [KA2a KA2b KA3 KA4 KA5 KA6 KA7]   -> col1_ka.json / col1_ka.out (merged per item)

Criteria: FROZEN_CRITERIA.md section 4. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import col1_lib as L
import col1_shell as S

KD1 = json.load(open(os.path.join(HERE, '../../closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json')))
JS = (1200, 2400)
OUTJ = os.path.join(HERE, 'col1_ka.json')
RES = json.load(open(OUTJ)) if os.path.exists(OUTJ) else {}
LOG = []


def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def nodes(xin, xout, J):
    return L.log_nodes(xin, xout, J)


def static_model_uniform(X, rho, mu_Mpc, a0, kind, hb, Mb=0.0, eps=1.0, rout=None):
    m, Mlag, alpha = S.charges_uniform(X, rho)
    md = S.ShellModel(mu_Mpc, a0, kind, X.copy(), np.zeros_like(X), m, Mlag, (lambda t: hb) if not callable(hb) else hb,
                      'static', Mb=Mb, eps=eps, rout_fn=rout or (lambda t: X[-1]), gap_ref=lambda t: np.diff(X), alpha=alpha)
    md.h = np.full(len(X), hb if not callable(hb) else hb(0.0))
    md.X = X
    return md


def ka2a():
    rho, R = 1e4, 100.0
    M = rho * 4 * math.pi / 3 * R ** 3
    tff = math.pi * math.sqrt(R ** 3 / (8 * L.G * M))
    cyc_t = lambda eta: math.sqrt(R ** 3 / (8 * L.G * M)) * (eta + math.sin(eta))

    def frac(t):            # r/R on the cycloid
        lo, hi = 0.0, math.pi
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if cyc_t(mid) < t:
                lo = mid
            else:
                hi = mid
        return (1 + math.cos(0.5 * (lo + hi))) / 2
    out = {}
    for J in JS:
        X = nodes(1.0, R, J)
        mu = 1e6
        md = static_model_uniform(X, rho, mu, L.a0_of('canonical'), 'off', lambda t: L.K * rho * frac(t) ** -3 / (mu / 1000) ** 2,
                                  rout=lambda t: R * frac(t))
        t1 = 0.95 * tff
        t, steps, ev = md.run(0.0, t1, 1e-3, t1)
        f = frac(t1)
        err = float(np.max(np.abs(md.r[1:-1] / X[1:-1] - f)) / f)
        out[J] = {'t_ff': tff, 'r_over_X_expected': f, 'max_rel_err': err, 'steps': steps, 'event': ev}
        P(f'KA2a top-hat J {J}: at 0.95 t_ff every node r/X = {f:.6f} expected; max rel err {err:.2e} (line 1e-3); steps {steps}; event {ev}')
    ok = all(v['max_rel_err'] <= 1e-3 and not v['event'] for v in out.values())
    return {'rows': out, 'pass': ok}


def ka2b():
    Mb, rho = 1e11, 1e-6
    out = {}
    for J in JS:
        X = nodes(10.0, 100.0, J)
        mu = 1e6
        md = static_model_uniform(X, rho, mu, L.a0_of('canonical'), 'off', L.K * rho / (mu / 1000) ** 2, Mb=Mb, eps=1e-6)
        tff = lambda q: (math.pi / 2) * math.sqrt(q ** 3 / (2 * L.G * Mb))

        def r_kepler(q, t):
            k = math.sqrt(q ** 3 / (8 * L.G * Mb))
            lo, hi = 0.0, math.pi
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if k * (mid + math.sin(mid)) < t:
                    lo = mid
                else:
                    hi = mid
            return q * (1 + math.cos(0.5 * (lo + hi))) / 2
        t1 = 0.9 * tff(X[1])
        md.run(0.0, t1, 1e-3, t1)
        exp = np.array([r_kepler(q, t1) for q in X[1:-1]])
        err1 = float(np.max(np.abs(md.r[1:-1] - exp) / exp))
        t, steps, ev = md.run(t1, 2 * tff(X[1]), 1e-3, 10.0, dt_floor=1e-22)
        tc = ev['t'] if ev else float('nan')
        err2 = abs(tc - tff(X[1])) / tff(X[1])
        out[J] = {'max_rel_err_at_0.9tff': err1, 'centre_arrival_t': tc, 't_ff': tff(X[1]), 'rel_err_arrival': err2, 'event': ev}
        P(f'KA2b point-mass cycloid J {J}: max rel err of r at 0.9 t_ff(q1) {err1:.2e}; first shell reaches the centre (E1) at'
          f' {tc:.6f} vs t_ff {tff(X[1]):.6f}: rel {err2:.2e} (line 1e-3); event {ev and ev.get("kind")}')
    ok = all(v['max_rel_err_at_0.9tff'] <= 1e-3 and v['rel_err_arrival'] <= 1e-3 for v in out.values())
    return {'rows': out, 'pass': ok}


def ka3():
    mu = 3.71 / 1000; hc = 600.0 ** 2
    Rout = 0.9 * math.pi / mu
    rr = np.concatenate([[0.0], np.logspace(-3, math.log10(Rout), 400001)])
    x = mu * rr
    MN = (4 * math.pi * hc / (L.K * mu)) * (np.sin(x) - x * np.cos(x))
    hR = hc * math.sin(mu * Rout) / (mu * Rout)
    tcross = Rout / 600.0
    out = {}
    for J in JS:
        X = nodes(1.0, Rout, J)
        def Mf(x):          # (4 pi hc/(K mu)) (sin y - y cos y), y = mu x; series below y = 0.05 (no cancellation)
            y = mu * np.asarray(x, dtype=float)
            ser = y ** 3 / 3 - y ** 5 / 30 + y ** 7 / 840 - y ** 9 / 45360
            return (4 * math.pi * hc / (L.K * mu)) * np.where(y < 0.05, ser, np.sin(y) - y * np.cos(y))
        md = S.static_model(X, Mf, 3.71, L.a0_of('canonical'), 'off', hR)
        vmax = [0.0]

        def snap(mm, t, acc, final=False):
            vmax[0] = max(vmax[0], float(np.abs(mm.v).max()))
        t, steps, ev = md.run(0.0, 10 * tcross, 1e-2, tcross / 20, on_snap=snap)
        out[J] = {'max_v_over_cs0': vmax[0] / 600.0, 'steps': steps, 'event': ev, 't_end': t}
        P(f'KA3 static n=1 polytrope (law off, mu 3.71/Mpc, c_s0 600 km/s) J {J}: max |v|/c_s0 over 10 crossings {vmax[0] / 600:.2e}; steps {steps}; event {ev}')
    a, b = out[JS[0]]['max_v_over_cs0'], out[JS[1]]['max_v_over_cs0']
    ok = a <= 1e-3 and b <= a / 3 and not any(v['event'] for v in out.values())
    return {'rows': out, 'ratio': a / max(b, 1e-300), 'pass': ok}


def static_setup(mu_Mpc, J, xin=0.5, Rout=300.0, Mb=10 ** 10.45, footing='canonical', kind='law', eps=1.0):
    a0 = L.a0_of(footing)
    rr, h, MN, Md = L.static_law_profile(Mb, a0, mu_Mpc, Rout, 0.0, eps=eps, lawkind=kind)
    X = nodes(xin, Rout, J)
    Mf = L.static_law_profile.last_MNf
    md = S.static_model(X, Mf, mu_Mpc, a0, kind, 0.0, Mb=Mb, eps=eps)
    md.h = np.interp(X, rr, h)
    return md, rr, h, MN


def ka4():
    """A3: graded on nodes with r >= RC = 3 kpc (3 eps); r >= 0.1 kpc and all-node values reported."""
    RC = 3.0
    out = {}
    for mu in (0.1, 3.71):
        out[mu] = {}
        for J in JS:
            md, rr, h, MN = static_setup(mu, J)
            acc, ah, ag, av = md.accel(0.0, md.r, md.v, want=True)
            sel = (md.r >= RC); sel[0] = sel[-1] = False
            s01 = (md.r >= 0.1); s01[0] = s01[-1] = False
            allm = np.ones_like(sel); allm[0] = allm[-1] = False
            res01 = float(np.max(np.abs(acc[s01]) / np.abs(ag[s01])))
            res = float(np.max(np.abs(acc[sel]) / np.abs(ag[sel])))
            res_all = float(np.max(np.abs(acc[allm]) / np.abs(ag[allm])))
            vc = np.sqrt(np.abs(ag) * md.r)
            vmax = [0.0, 0.0, 0.0]

            def snap(mm, t, a_, final=False):
                vmax[0] = max(vmax[0], float(np.max(np.abs(mm.v[sel]) / vc[sel])))
                vmax[1] = max(vmax[1], float(np.max(np.abs(mm.v[allm]) / vc[allm])))
                vmax[2] = max(vmax[2], float(np.max(np.abs(mm.v[s01]) / vc[s01])))
            t, steps, ev = md.run(0.0, 2.0 / L.TU, 1e-3, 0.05 / L.TU, on_snap=snap, dt_floor=1e-20)
            out[mu][J] = {'residual_acc_over_g_r_ge_3': res, 'residual_r_ge_0.1': res01, 'residual_all_nodes': res_all,
                          'max_v_over_vc_2Gyr_r_ge_3': vmax[0], 'max_v_over_vc_r_ge_0.1': vmax[2],
                          'max_v_over_vc_all_nodes': vmax[1], 'steps': steps, 'event': ev}
            P(f'KA4 static law state mu {mu}/Mpc J {J}: residual |dv/dt|/g at r >= {RC} kpc {res:.2e} (r >= 0.1: {res01:.2e}; all nodes {res_all:.2e}; line 1e-3);'
              f' 2 Gyr max |v|/v_c at r >= {RC} {vmax[0]:.2e} (r >= 0.1: {vmax[2]:.2e}; all {vmax[1]:.2e}; line 0.01); steps {steps}; event {ev}')
    ok = all(out[mu][JS[0]]['residual_acc_over_g_r_ge_3'] <= 1e-3
             and out[mu][JS[1]]['residual_acc_over_g_r_ge_3'] <= out[mu][JS[0]]['residual_acc_over_g_r_ge_3'] / 3
             and all(out[mu][J]['max_v_over_vc_2Gyr_r_ge_3'] <= 0.01 and not out[mu][J]['event'] for J in JS) for mu in out)
    return {'rows': {str(k_): v for k_, v in out.items()}, 'graded_on': 'r >= 3 kpc (A3)', 'pass': ok}


def ka5():
    out = {}
    for J in JS:
        md0, rr, h, MN = static_setup(0.0, J, xin=5.0, eps=5.0)      # A3: eps 5 kpc (eps 1 puts the discrete core over the cap)
        md1, _, _, _ = static_setup(0.0, J, xin=5.0, eps=5.0)
        j0 = int(np.searchsorted(md0.r, 30.0))
        d = 1e-3 * (md1.r[j0 + 1] - md1.r[j0])
        md1.r[j0] += d
        a0 = md0.a0
        acc, ah, ag, av = md0.accel(0.0, md0.r, md0.v, want=True)
        g = abs(ag[j0]); u = g / a0
        # exact local shell frequency at fixed enclosed charge, softened baryons (frozen definition -d/dr[-g_b - y + U(y)])
        Mb_, ep = 10 ** 10.45, 5.0
        menc = md0.Mlag[j0]                           # thin-shell enclosed clock charge (M_<j + m_j/2)
        def fsh(R):
            yv = L.G * menc / R ** 2
            return -L.G * Mb_ * R / (R * R + ep * ep) ** 1.5 - yv + a0 * yv / (a0 - yv)
        R0 = md0.r[j0]; dR = 1e-5 * R0
        w2 = -(fsh(R0 + dR) - fsh(R0 - dR)) / (2 * dR)
        w2_pm = 2 * a0 * u * u / md0.r[j0]
        T = 2 * math.pi / math.sqrt(w2)
        ts, x0, x1 = [], [], []
        md0.run(0.0, 5 * T, 1e-3, T / 200, on_snap=lambda mm, t, a_, final=False: (ts.append(t), x0.append(mm.r[j0])))
        md1.run(0.0, 5 * T, 1e-3, T / 200, on_snap=lambda mm, t, a_, final=False: x1.append(mm.r[j0]))
        n = min(len(ts), len(x0), len(x1))
        ts = np.array(ts[:n]); dx = np.array(x1[:n]) - np.array(x0[:n])
        zc = [ts[i] - dx[i] * (ts[i + 1] - ts[i]) / (dx[i + 1] - dx[i]) for i in range(n - 1) if dx[i] * dx[i + 1] < 0]
        Tm = 2 * float(np.mean(np.diff(zc))) if len(zc) > 2 else float('nan')
        w2m = (2 * math.pi / Tm) ** 2
        out[J] = {'r_node': float(md0.r[j0]), 'u': u, 'omega2_expected_softened': w2, 'omega2_point_mass_form': w2_pm,
                  'omega2_measured': w2m, 'rel_err': abs(w2m - w2) / w2, 'zero_crossings': len(zc)}
        P(f'KA5 shell frequency (mu 0, static law state, node at {md0.r[j0]:.2f} kpc, u = g/a0 {u:.4f}) J {J}: omega^2 measured {w2m:.5g}'
          f' vs -d/dr[-g_b - y + U(y)] (eps 5 kpc) {w2:.5g} (point-mass form 2 a0 u^2/r {w2_pm:.5g}): rel {abs(w2m - w2) / w2:.2e} (line 2e-2); zero crossings {len(zc)}')
    sysj = json.load(open(os.path.join(HERE, 'col1_system.json')))
    ok = all(v['rel_err'] <= 0.02 for v in out.values()) and sysj['R5']['pass']
    return {'rows': out, 'R5_scs1_identity': sysj['R5']['pass'], 'pass': ok}


def ka6():
    """A3: graded at mu_K 0.1 (law-dominated); mu_K 3.71 reported to its first event. Snapshots every 100 fixed steps."""
    out = {}
    for mu in (0.1, 3.71):
        out[mu] = {}
        for J in JS:
            out[mu][J] = {}
            for dt in (2e-4, 1e-4):
                md, rr, h, MN = static_setup(mu, J, xin=2.0)
                acc, ah, ag, av = md.accel(0.0, md.r, md.v, want=True)
                vc = np.sqrt(np.abs(ag) * md.r)
                x = (md.r - md.r[1]) / (md.r[-1] - md.r[1])
                md.v = 0.1 * vc * np.sin(math.pi * np.clip(x, 0, 1)); md.v[0] = md.v[-1] = 0.0
                E = []

                def snap(mm, t, a_, final=False):
                    k_, U, W = mm.energy(t); E.append((t, k_, U, W))
                nsteps = int(round(2.0 / L.TU / dt / 100)) * 100
                t, steps, ev = md.run(0.0, nsteps * dt, 1e-3, 100 * dt, on_snap=snap, fixed_dt=dt)
                E = np.array(E)
                tot = E[:, 1] + E[:, 2] + E[:, 3]
                scale = np.abs(E[0, 1]) + np.abs(E[0, 2]) + np.abs(E[0, 3])
                err = float(np.max(np.abs(tot - tot[0])) / scale)
                out[mu][J][dt] = {'max_rel_energy_err': err, 'event': ev, 't_end_gyr': t * L.TU, 'steps': steps}
                P(f'KA6 energy (mu {mu}, static state + 10% kick) J {J} dt {dt}: max |dE|/(|KE|+|U|+|W|) {err:.2e} (line 1e-4) to t {t * L.TU:.3f} Gyr; event {ev}')
    ok = True
    for J in JS:
        e1, e2 = out[0.1][J][2e-4]['max_rel_energy_err'], out[0.1][J][1e-4]['max_rel_energy_err']
        out[0.1][J]['ratio'] = e1 / max(e2, 1e-300)
        ok = ok and e1 <= 1e-4 and e2 <= 1e-4 and e1 / max(e2, 1e-300) >= 3 and not out[0.1][J][2e-4]['event']
    return {'rows': {str(m_): {str(J): {str(k_): v for k_, v in d.items()} for J, d in dd.items()} for m_, dd in out.items()},
            'graded_on': 'mu_K 0.1 (A3)', 'pass': ok}


def ka7():
    out = {}
    for mu in (3.71, 0.1):
        md, ti, t0, cos = S.hubble_model(mu, 'canonical', -300.0, JS[0], KD1)
        t, steps, ev = md.run(ti, t0, 1e-3, (t0 - ti))
        a = cos.a_of_t(t)
        err = float(np.max(np.abs(md.r[1:-1] / (a * md.X[1:-1]) - 1)))
        out[mu] = {'max_rel_dev_from_hubble': err, 'event': ev, 'steps': steps, 'z_end': 1 / a - 1}
        P(f'KA7 background (M_b = 0) mu {mu}/Mpc J {JS[0]}: max |r/(a X) - 1| at z {1 / a - 1:.3f} = {err:.2e} (line 1e-3); event {ev}')
    ok = all(v['max_rel_dev_from_hubble'] <= 1e-3 and not v['event'] for v in out.values())
    return {'rows': {str(k): v for k, v in out.items()}, 'pass': ok}


if __name__ == '__main__':
    todo = sys.argv[1:] or ['KA2a', 'KA2b', 'KA3', 'KA4', 'KA5', 'KA6', 'KA7']
    fn = {'KA2a': ka2a, 'KA2b': ka2b, 'KA3': ka3, 'KA4': ka4, 'KA5': ka5, 'KA6': ka6, 'KA7': ka7}
    for k in todo:
        T = time.time()
        r = fn[k]()
        r['wall_s'] = time.time() - T
        RES[k] = r
        P(f'{k}: {"PASS" if r["pass"] else "FAIL"}  ({r["wall_s"]:.1f}s)\n')
        json.dump(RES, open(OUTJ, 'w'), indent=1, default=str)
        with open(os.path.join(HERE, 'col1_ka.out'), 'a') as f:
            f.write('\n'.join(LOG) + '\n'); LOG.clear()
