#!/usr/bin/env python3
r"""
U01_ed2.py -- deterministic E[D^2]: runner for the second-level closure.

Battery + ladders + payoff + volume port + MC cross-checks.  See
U01_ed2_solver.py for the solver and the derivations.
"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, '/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push')
from U01_ed2_solver import RaySolver2, solve_hierarchy, kappa_profile
from K05_ray_solver import run_closed_forms, run_mugrid_crosscheck
from J02_moment_hierarchy import simulate, simulate_Q


def vacuum_checks():
    """kappa=0 homogeneous limit: F10 = r mu, F20 = r^2 mu^2/2, F04 = 0."""
    out = {}
    for (Nr, Nq, L, Nt) in ((80, 48, 12, 24), (160, 64, 16, 32)):
        s = RaySolver2(Nr, Nq, L, Nt, 0.0, 0.0)
        F10, _, _ = s.solve_equation('S10', bc_kind='mu', tol=1e-12,
                                     max_iter=3)
        F20, _, _ = s.solve_equation('S20', bc_kind='mu2half',
                                     psi_src=(s.project(F10),), tol=1e-12,
                                     max_iter=3)
        F02v, _, _ = s.solve_equation('S02', bc_kind='zero', tol=1e-12,
                                       max_iter=3)
        F04, _, _ = s.solve_equation('S04', bc_kind='zero',
                                     psi_src=(s.project(F02v),), tol=1e-12,
                                     max_iter=3)
        rm = s.rnodes[:, None]*s.mu[None, :]
        r2m2 = 0.5*s.rnodes[:, None]**2*s.mu[None, :]**2
        out[f'V_Um_{Nr}_{Nq}_{L}_{Nt}'] = dict(
            err_F10=float(np.max(np.abs(F10 - rm))),
            err_F20=float(np.max(np.abs(F20 - r2m2))),
            max_F04=float(np.max(np.abs(F04))),
            E_D=float(-np.mean(F10[0])), E_D2=float(2.0*np.mean(F20[0])),
            E_v4=float(6.0*np.mean(F04[0])))
    return out


def run_ladder(cfgs, q, tau0, with_variants=False):
    rows = []
    for cfg in cfgs:
        s = RaySolver2(*cfg, tau0, q)
        t0 = time.time()
        r = solve_hierarchy(s, with_variants=with_variants)
        m = r['moments']
        row = dict(cfg=list(cfg), q=q, tau0=tau0,
                   E_D=m['E_D'], E_v2=m['E_v2'], E_Dv2=m['E_Dv2'],
                   E_D2=m['E_D2'], E_v4=m['E_v4'],
                   iters=[r['info'][k]['iters'] for k in
                          ('i10', 'i02', 'i12', 'i20', 'i04')],
                   gaps=[r['info'][k]['gap'] for k in
                         ('i10', 'i02', 'i12', 'i20', 'i04')],
                   secs=time.time() - t0)
        if with_variants:
            row['variants'] = r['variants']
        rows.append(row)
        print(f"  cfg {cfg} q={q}: E[D]={m['E_D']:.6f} E[v2]={m['E_v2']:.6f} "
              f"E[Dv2]={m['E_Dv2']:.6f} E[D2]={m['E_D2']:.6f} "
              f"E[v4]={m['E_v4']:.4f}  iters={row['iters']} "
              f"({time.time()-t0:.1f}s)")
        sys.stdout.flush()
    return rows


def run_tau0_scan():
    tau0s = (0.25, 0.5, 1.0, 2.0, 4.0)
    cfg = (160, 64, 16, 32)
    out = []
    for tau0 in tau0s:
        s = RaySolver2(*cfg, tau0, 0.0)
        r = solve_hierarchy(s)
        m = r['moments']
        out.append(dict(tau0=tau0,
                        E_D=m['E_D'], E_D2=m['E_D2'],
                        E_D2_minus_ED2=m['E_D2'] - m['E_D']**2))
        print(f"  tau0={tau0}: E[D]={m['E_D']:.8f} E[D^2]={m['E_D2']:.8f} "
              f"Var(D)={m['E_D2']-m['E_D']**2:.8f}")
    return out


def payoff(rows, mc):
    """Deterministic U, corr, slack on the q=0/3/10 clouds (central)."""
    out = {}
    for row in rows:
        q = int(row['q'])
        E_D, E_v2 = row['E_D'], row['E_v2']
        E_Dv2, E_D2, E_v4 = row['E_Dv2'], row['E_D2'], row['E_v4']
        E_ang = E_v2/2.0
        E_Dang = E_Dv2/2.0
        E_ang2 = E_v4/12.0
        VarD = E_D2 - E_D**2
        VarA = E_ang2 - E_ang**2
        U = np.sqrt(VarD)/E_D
        rho0 = E_Dang/np.sqrt(E_D2*E_ang2)
        slack = E_D2*E_ang2/E_Dang**2
        B1 = 3.0*E_Dv2**2/E_v4
        rhoP = (E_Dang - E_D*E_ang)/np.sqrt(VarD*VarA)
        d = dict(
            E_D=E_D, E_D2=E_D2, E_v2=E_v2, E_Dv2=E_Dv2, E_v4=E_v4,
            U=U, VarD=VarD,
            E_ang=E_ang, E_Dang=E_Dang, E_ang2=E_ang2,
            rho0=rho0, rhoP=rhoP, slack=slack, B1=B1,
            slack_minus_1rho0_2=slack - 1.0/rho0**2,
            slack_rho0_sq=slack*rho0**2,
            slack_over_1rhoP_2=slack*rhoP**2, inv_rhoP2=1.0/rhoP**2,
            mc_slack=float(mc[f'q{q}']['slack']),
            mc_slack_SE=float(mc[f'q{q}'].get('s_slack', np.nan)),
            mc_E_D2=float(mc[f'q{q}']['E_D2']),
            z_slack=abs(slack - mc[f'q{q}']['slack'])
            / max(1e-12, float(mc[f'q{q}'].get('s_slack', 0.01))),
            pct_vs_mc=100.0*(E_D2 - mc[f'q{q}']['E_D2'])
            / mc[f'q{q}']['E_D2'])
        d['pass_identity'] = bool(abs(slack*rho0**2 - 1.0) < 1e-9)
        out[f'q{q}'] = d
    return out


def mc_verify():
    """Quick MC re-verification: central q=0 E[D^2] and D = tau - Q."""
    out = {}
    n = 400000
    r = simulate(n, 1.0, 0.0, 'central', seed=20260925)
    D = r['D']
    E_D2 = float(np.mean(D**2))
    sD2 = float(np.std(D**2, ddof=1)/np.sqrt(n))
    E_D = float(np.mean(D))
    U = float(np.sqrt(np.mean(D**2) - E_D**2)/E_D)
    out['central_q0'] = dict(n=n, E_D2=E_D2, sE_D2=sD2, E_D=E_D, U=U,
                             refs=dict(E_D2=0.7661, E_D=0.5, U=1.437))
    rq = simulate_Q(150000, 1.0, 0.0, 'central', seed=7)
    Q, X, tau = rq['Q'], rq['X'], rq['elapsed']
    out['Q_bookkeeping'] = dict(max_abs_Q_minus_X=float(np.max(np.abs(Q - X))),
                                E_D_from_tau_Q=float(np.mean(tau) - np.mean(Q)),
                                E_tau=float(np.mean(tau)), E_Q=float(np.mean(Q)))
    return out


def main():
    t_start = time.time()
    out = {}
    print("=" * 78)
    print("U01 -- DETERMINISTIC E[D^2]: second-level closure of the moment"
          " hierarchy")
    print("=" * 78)

    print("[1] K05 honesty battery (V1-V3 projectors/geometry;"
          " V4 collision quadrature)")
    v = run_closed_forms()
    out['closed_forms'] = v
    print("    V1/V2/V3:", {k: (round(v[k], 3) if isinstance(v[k], float)
                               else v[k]) for k in v})

    print("[2] kappa=0 homogeneous (vacuum) limit -- closed-form fields")
    out['vacuum'] = vacuum_checks()
    for k, val in out['vacuum'].items():
        print(f"    {k}: {val}")

    print("[3] q=0 ladder (tau0=1), E[D^2] vs MC 0.7661 (+-1%)")
    rows0 = run_ladder([(80, 48, 12, 24), (160, 64, 16, 32),
                        (240, 80, 20, 40)], 0.0, 1.0, with_variants=True)
    out['ladder_q0'] = rows0
    best0 = rows0[-1]
    out['targets_q0'] = dict(E_D2=best0['E_D2'], mc=0.7661,
                             pct=100.0*abs(best0['E_D2'] - 0.7661)/0.7661,
                             pass_1pct=abs(best0['E_D2'] - 0.7661)
                             < 0.01*0.7661,
                             variants=rows0[0]['variants'])

    print("[4] q=3 and q=10 (tau0=1): E[D^2] vs MC 3.3724 / 16.2167 (+-1%)")
    rows3 = run_ladder([(160, 64, 16, 32), (240, 80, 20, 40)], 3.0, 1.0)
    rows10 = run_ladder([(160, 64, 16, 32), (240, 80, 20, 40)], 10.0, 1.0)
    out['ladder_q3'] = rows3
    out['ladder_q10'] = rows10
    for q, rows, mc in ((3, rows3, 3.3724), (10, rows10, 16.2167)):
        best = rows[-1]
        out[f'targets_q{q}'] = dict(E_D2=best['E_D2'], mc=mc,
                                    pct=100.0*abs(best['E_D2'] - mc)/mc,
                                    pass_1pct=abs(best['E_D2'] - mc)
                                    < 0.01*mc)

    print("[5] kappa-dependence at q=0: E[D^2](tau0) for tau0 = "
          "0.25..4 (fit c2 t^2 + c1 t + c0)")
    scan = run_tau0_scan()
    out['tau0_scan'] = scan
    ts = np.array([r['tau0'] for r in scan])
    ys = np.array([r['E_D2'] for r in scan])
    A = np.vstack([ts**2, ts, np.ones_like(ts)]).T
    coef, *_ = np.linalg.lstsq(A, ys, rcond=None)
    pred = A @ coef
    resid = float(np.max(np.abs(pred - ys)))
    rel = float(np.max(np.abs(pred - ys)/np.maximum(ys, 1e-12)))
    out['tau0_fit'] = dict(c2=float(coef[0]), c1=float(coef[1]),
                           c0=float(coef[2]), max_abs_resid=resid,
                           max_rel_resid=rel)
    print(f"    fit: E[D^2] = {coef[0]:.8f} t^2 + {coef[1]:.8f} t "
          f"+ {coef[2]:.2e},  max rel resid {rel:.2e}")

    print("[6] volume port (q=0), deterministic -- targets E[D]=0.3376,"
          " E[D^2]=0.5251, U=1.893")
    vol = {}
    cfg = (80, 48, 12, 24)
    sv = RaySolver2(*cfg, 1.0, 0.0)
    hv = solve_hierarchy(sv, with_volume=True)
    vp = hv['volume']
    mv = hv['moments']
    vp['cfg'] = list(cfg)
    vp['E_D2_det_fine'] = mv['E_D2']
    vol[str(cfg)] = vp
    print(f"    {cfg}: E[D]_vol={vp['E_D_vol']:.5f} (mc 0.3376), "
          f"E[D^2]_vol(det+B)={vp['E_D2_vol']:.5f} (mc 0.5251), "
          f"U_vol={vp['U_vol']:.5f} (mc 1.893)")
    print(f"    M-tensor status: {vp['M_tensor_status']}")
    out['volume'] = vol

    print("[7] payoff: U, corr(D,ang), slack at full deterministic precision")
    mc_refs = {'q0': dict(E_D2=0.7661, slack=1.2430, s_slack=0.003),
               'q3': dict(E_D2=3.3724, slack=1.1322, s_slack=0.003),
               'q10': dict(E_D2=16.2167, slack=1.0701, s_slack=0.002)}
    pay = payoff([rows0[-1], rows3[-1], rows10[-1]], mc_refs)
    out['payoff'] = pay
    for k, vv in pay.items():
        print(f"    {k}: U={vv['U']:.5f} rho0={vv['rho0']:.5f} "
              f"rhoP={vv['rhoP']:.5f} slack={vv['slack']:.5f} "
              f"(mc {vv['mc_slack']})  slack*rho0^2={vv['slack_rho0_sq']:.3e}"
              f"  slack*rhoP^2={vv['slack_over_1rhoP_2']:.4f}"
              f"  E[D2]%vs mc={vv['pct_vs_mc']:.3f}")

    print("[8] MC re-verification: E[D^2] and D = tau - Q bookkeeping")
    mc = mc_verify()
    out['mc_verify'] = mc
    print(f"    {mc['central_q0']}")
    print(f"    {mc['Q_bookkeeping']}")

    out['total_seconds'] = time.time() - t_start
    with open('U01_results.json', 'w') as fh:
        json.dump(out, fh, indent=1)
    print("=" * 78)
    print(f"total wall {out['total_seconds']:.1f}s; U01_results.json written")
    return 0


if __name__ == '__main__':
    sys.exit(main())