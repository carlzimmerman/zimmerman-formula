#!/usr/bin/env python3
"""W4-08 critical endpoint -- numerical part (M4 of FROZEN_CRITERIA.md, committed alone 582bbb7ad).

Static spherical sourced response on the de Sitter state, Newtonian sub-horizon limit derived in derive.py:
    Phi:      2 g - alpha_I(I) a = 2 G M(r)/r^2,                 a = g + w_c,  w_c = v v' - H^2 r
    khronon:  alpha_I(I) K = alpha0 K0 + (-c1/c2) J(r),          J(r) = int_r^rmax v (s^2 alpha_I a)'/s^2 ds,  alpha_I a = 2g - 2GM/s^2
    flow:     K = (r^2 v)'/r^2,  v(0) = 0 (v -> H r outside the source's influence)
    I - I0 = x = [c2 (K^2 - K0^2) - c1 a^2]/m^2 >= 0
Units c = H = 1. Declared parameters (not tuned to any target): c1 = -1, m = 0.15, a_M = 0.2, GM = 1e-13, Plummer b = 1e-8,
r in [1e-9, 1e-2]. Runs: E-cusp (c2 = -1e-5, p = y/(1+y)), E-reg (alpha = 2/(1 + x/x_a)), control L-reg (alpha = 1/(1 + x/x_a)).
W4_08_CE_MUTATE=1: MU1 (alpha0 1.9), MU2 (cusp removed), MU3 (c2 = -1e-3), MU4 (cusp sign reversed); exit 1 when all bite.
Light: numpy + scipy brentq, one core, under a minute. kappa = 1/2 FITTED. Not theory closed.
"""
import json, math, os, sys
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("W4_08_CE_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
OUT, checks = [], []
H, K0, c1, m, aM, GM, bP = 1.0, 3.0, -1.0, 0.15, 0.2, 1e-13, 1e-8
xa = abs(c1) * aM ** 2 / m ** 2
R = np.logspace(-9, -2, 3000)


def P(s=""):
    print(s); OUT.append(str(s))


def check(name, detail, ok):
    checks.append({"name": name, "detail": str(detail), "pass": bool(ok)})
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def alpha_factory(kind):
    """returns alpha(x), dalpha(x) = alpha0 - alpha(x) (analytic, no cancellation), alpha0"""
    sq = lambda x: math.sqrt(max(x, 0.0) / xa)
    li = lambda x: max(x, 0.0) / xa
    if kind == "cusp":                 # alpha = 2(1 - p(y)), p = y/(1+y), y = sqrt(x/x_a)
        return (lambda x: 2.0 / (1.0 + sq(x))), (lambda x: 2.0 * sq(x) / (1.0 + sq(x))), 2.0
    if kind == "reg":                  # regular at I0, F'' != 0
        return (lambda x: 2.0 / (1.0 + li(x))), (lambda x: 2.0 * li(x) / (1.0 + li(x))), 2.0
    if kind == "ctrl":                 # alpha0 = 1 control
        return (lambda x: 1.0 / (1.0 + li(x))), (lambda x: li(x) / (1.0 + li(x))), 1.0
    if kind == "mu1":                  # alpha0 = 1.9
        return (lambda x: 1.9 / (1.0 + li(x))), (lambda x: 1.9 * li(x) / (1.0 + li(x))), 1.9
    if kind == "mu4":                  # cusp sign reversed: p -> -p
        return (lambda x: 2.0 * (1.0 + sq(x) / (1.0 + sq(x)))), (lambda x: -2.0 * sq(x) / (1.0 + sq(x))), 2.0
    raise ValueError(kind)


def solve(kind, c2, maxit=600, tol=1e-11, omega=0.05, phase1_only=False):
    """Perturbation variables only: w = v - H r, dK = K - K0, dalpha = alpha0 - alpha. No background subtraction."""
    alpha, dalpha, a0 = alpha_factory(kind)
    S = 2 * GM * R / (R ** 2 + bP ** 2) ** 1.5           # 2 G M(r)/r^2 for a Plummer sphere
    lam = -c1 / c2                                        # amplification of the back-reaction J
    wc = np.zeros_like(R); J = np.zeros_like(R); g = S / 2; dK = np.zeros_like(R); x = np.zeros_like(R)
    w = np.zeros_like(R)
    status, phase, it_phase1, J1 = "ok", 1, None, None
    for it in range(maxit):
        g_new, dK_new, x_new = np.empty_like(R), np.empty_like(R), np.empty_like(R)
        for i in range(len(R)):
            Si, wi, Ji = S[i], wc[i], J[i]

            def parts(xx):
                al, da = alpha(xx), dalpha(xx)
                two_m_al = (2.0 - a0) + da
                gi = (Si + al * wi) / two_m_al if two_m_al > 0 else (math.inf if two_m_al == 0 else (Si + al * wi) / two_m_al)
                dKi = (K0 * da + lam * Ji) / al
                return al, gi, dKi

            def f(xx):
                al, gi, dKi = parts(xx)
                if not math.isfinite(gi) or abs(gi) > 1e150:
                    return -math.inf
                return m ** 2 * xx + abs(c2) * dKi * (2 * K0 + dKi) - abs(c1) * (gi + wi) ** 2

            lo, hi = None, xa
            for e in range(-40, 1):
                fl = f(xa * 10.0 ** e)
                if math.isfinite(fl):
                    lo = xa * 10.0 ** e if fl < 0 else None
                    break
            if lo is None and a0 < 2 and f(0.0) < 0:
                lo = 0.0
            if lo is None:
                status = "no root"; x_new[i] = 0.0
            else:
                n = 0
                while f(hi) <= 0 and n < 400:
                    hi *= 4.0; n += 1
                x_new[i] = brentq(f, lo, hi, xtol=1e-300, rtol=1e-14, maxiter=500) if f(hi) > 0 else hi
                if f(hi) <= 0:
                    status = "no bracket"
            al, gi, dKi = parts(x_new[i])
            g_new[i], dK_new[i] = gi, dKi
        # flow perturbation: w = r^-2 int_0^r dK s^2 ds; w' = dK - 2w/r; convective perturbation wc = H(r dK - w) + w w'
        integ = dK_new * R ** 2
        cum = np.concatenate([[dK_new[0] * R[0] ** 3 / 3], dK_new[0] * R[0] ** 3 / 3 + np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(R))])
        w = cum / R ** 2
        wp = dK_new - 2 * w / R
        wc_new = H * (R * dK_new - w) + w * wp
        al_arr = np.array([alpha(xx) for xx in x_new])
        aa = g_new + wc_new
        src = np.gradient(R ** 2 * al_arr * aa, R) * (H * R + w) / R ** 2
        J_new = np.concatenate([np.cumsum((0.5 * (src[1:] + src[:-1]) * np.diff(R))[::-1])[::-1], [0.0]])
        if not (np.all(np.isfinite(g_new)) and np.all(np.isfinite(wc_new)) and np.all(np.isfinite(J_new))):
            status = "diverged"; break
        dg = np.max(np.abs(g_new - g) / np.maximum(np.abs(g_new), 1e-300))
        dJ = np.max(np.abs(J_new - J)) * abs(lam) / (a0 * K0) if phase == 2 else 0.0
        g, dK, x, wc = g_new, dK_new, x_new, wc_new
        if phase == 2:
            J = J + omega * (J_new - J)
        if phase == 1 and dg < tol and it > 2:
            it_phase1, J1 = it + 1, J_new.copy()
            if phase1_only:
                break
            phase, J = 2, omega * J_new
            continue
        if phase == 2 and dg < tol and dJ < tol:
            break
    else:
        status = "not converged" if status == "ok" else status
    if J1 is None:
        J1 = J
    al = np.array([alpha(xx) for xx in x])
    resid = np.max(np.abs(((2.0 - a0 + np.array([dalpha(xx) for xx in x])) * g - al * wc) - S) / S)
    slope = np.gradient(np.log(np.abs(g)), np.log(R))
    return dict(kind=kind, c2=c2, g=g, K=K0 + dK, dK=dK, x=x, v=H * R + w, w=w, wc=wc, J=J, alpha=al, S=S, slope=slope, it=it + 1,
                it1=it_phase1, dg=dg, resid=resid, status=status, Pt_rel=(a0 * K0 + lam * J) / (a0 * K0),
                beta1=lam * J1 / (a0 * K0), phase=phase)


def window(sol, lo=-1.05, hi=-0.95, rmin=2e-8):
    sel = (sol["slope"] >= lo) & (sol["slope"] <= hi) & (R > rmin)
    if not sel.any():
        return 0.0, None
    gs = np.abs(sol["g"][sel])
    return float(np.log10(gs.max() / gs.min())), (float(R[sel].min()), float(R[sel].max()))


def mu_closed(gv, c2):
    """frozen M3 closed form for the declared cusp p = y/(1+y), back-reaction and convection dropped"""
    C1, C2 = abs(c1), abs(c2)
    y = (-C2 * K0 ** 2 + np.sqrt(C1 ** 2 * aM ** 2 * gv ** 2 + C1 * C2 * K0 ** 2 * gv ** 2 + C2 ** 2 * K0 ** 4)) / (C1 * aM ** 2 + C2 * K0 ** 2)
    return y / (1 + y)


def report(sol, label):
    pick = lambda rr: int(np.argmin(np.abs(np.log(R / rr))))
    P(f"\n[{label}] {sol['kind']}, c2 = {sol['c2']:g}: {sol['it']} iterations (phase 1 converged at {sol['it1']}), last relative change {sol['dg']:.1e}, "
      f"Phi-equation residual {sol['resid']:.1e}, status {sol['status']}")
    for rr in (3e-8, 1e-7, 3e-7, 1e-6, 1e-5, 1e-4, 1e-3, 3e-3, 1e-2):
        i = pick(rr)
        P(f"   r {R[i]:.2e}: g {sol['g'][i]:+.4e}  slope {sol['slope'][i]:+.3f}  mu_eff {1 - sol['alpha'][i] / 2:.4e}  "
          f"dK/K0 {sol['dK'][i] / K0:+.4e}  w {sol['w'][i]:+.3e}  wc/g {sol['wc'][i] / sol['g'][i]:+.2e}  beta {sol['beta1'][i]:+.3e}")
    dec, rng = window(sol)
    P(f"   MOND window (local slope -1 +- 0.05, r > 2e-8): {dec:.2f} decades in g" + (f", r in [{rng[0]:.2e}, {rng[1]:.2e}]" if rng else ""))
    P(f"   max |w| {np.max(np.abs(sol['w'])):.2e};  max |beta| (back-reaction on the leading solution) {np.max(np.abs(sol['beta1'])):.3g}")
    return dec


res = {}
P("W4-08 critical endpoint: numerical sourced response on the de Sitter state" + ("  [MUTATE MU1-MU4]" if MUT else ""))
P(f"units c = H = 1; K0 = 3H; c1 = {c1}, m = {m}, a_M = {aM}, x_a = {xa:.4f}, GM = {GM}, Plummer b = {bP}")
if not MUT:
    runs = {k: solve(kd, -1e-5, phase1_only=True) for k, kd in (("E-cusp", "cusp"), ("E-reg", "reg"), ("L-reg", "ctrl"))}
    P("\nPHASE 1 (khronon back-reaction J off: the leading-order M3 system, convective term v v' kept)")
    win = {k: report(s_, k) for k, s_ in runs.items()}
    ec = runs["E-cusp"]
    eta = abs(-1e-5) * K0 ** 2 / (abs(c1) * aM)
    i3 = np.where((R > 1e-4) & (R < 3e-3))[0]
    ratio = runs["L-reg"]["g"][i3] / (2 * GM / R[i3] ** 2)
    check("K3 control alpha0 = 1 reproduces G_bg = G/(1 - alpha/2) = 2G in the far field (1%; phase 1)",
          f"g/(2GM/r^2) in [{ratio.min():.4f}, {ratio.max():.4f}]", np.all(np.abs(ratio - 1) < 0.01))
    check("K5 Phi-equation residual < 1e-8 and converged (phase 1, all runs)", {k: f"{s_['resid']:.1e}/{s_['dg']:.1e}" for k, s_ in runs.items()},
          all(s_["resid"] < 1e-8 and s_["dg"] < 1e-8 for s_ in runs.values()))
    i6 = np.where(R > 3e-8)[0]
    mu_num = np.array([alpha_factory('cusp')[1](xx) for xx in ec['x'][i6]]) / 2
    dev = np.abs(mu_num / mu_closed(np.abs(ec["g"][i6] + ec["wc"][i6]), -1e-5) - 1)
    check("K6 frozen closed-form mu_eff matches E-cusp numerics within 2% (r > 3e-8; phase 1 = the closed form's own limit)",
          f"max deviation {dev.max():.2e}", dev.max() < 0.02)
    quart = np.where(R > 3e-3)[0]
    P(f"\n   E-cusp quartic far field: slope at r > 3e-3 in [{ec['slope'][quart].min():.3f}, {ec['slope'][quart].max():.3f}] (closed form -2/3);"
      f" h_c = 2 eta = {2 * eta:.2e} vs a_M = {aM}")
    reg_far = runs["E-reg"]["slope"][np.where((R > 1e-5) & (R < 1e-2))[0]]
    P(f"   E-reg far-field slope in [{reg_far.min():.3f}, {reg_far.max():.3f}] (quartic -2/3; no -1 plateau)")
    # size of the neglected khronon back-reaction, evaluated on the leading-order solution
    P("\nBACK-REACTION (the term phase 1 drops): beta(r) = (-c1/c2) J(r)/(alpha0 K0), J = int_r^rmax v (s^2 alpha_I a)'/s^2 ds")
    PhiN = GM / np.sqrt(R ** 2 + bP ** 2)
    for k, s_ in runs.items():
        b1 = s_["beta1"]
        iN = np.where((R > 3 * bP) & (R < 0.1 * math.sqrt(GM / aM)))[0]
        coef = np.median(b1[iN] / ((abs(c1) / abs(-1e-5)) * PhiN[iN])) if len(iN) else float("nan")
        P(f"   {k}: max beta {np.max(np.abs(b1)):.3g}; beta at r = 1e-7, 1e-6, 1e-4: "
          f"{np.interp(np.log(1e-7), np.log(R), b1):.3g}, {np.interp(np.log(1e-6), np.log(R), b1):.3g}, {np.interp(np.log(1e-4), np.log(R), b1):.3g};"
          f" Newtonian-core beta/((|c1|/|c2|) Phi_N) = {coef:.3f}")
        s_["beta_coef"] = coef
    P("\nPHASE 2 (back-reaction on, under-relaxed omega = 0.05; reported, no verdict weight unless converged)")
    full = {}
    for k, kd in (("E-cusp", "cusp"),):
        f2 = solve(kd, -1e-5)
        full[k] = f2
        P(f"   {k}: status {f2['status']} after {f2['it']} iterations (phase {f2['phase']})")
        if f2["status"] == "ok":
            report(f2, k + " full")
    conv = full["E-cusp"]["status"] == "ok"
    w_lead = win["E-cusp"]
    w_full = window(full["E-cusp"])[0] if conv else None
    if conv:
        lane = "MOND WINDOW AT THE ENDPOINT" if w_full >= 1.0 and np.all(full["E-cusp"]["g"] > 0) else "NO MOND AT THE ENDPOINT"
    else:
        lane = "UNDETERMINED"
    P(f"\nENDPOINT VERDICT: {lane}  (leading-order E-cusp window {w_lead:.2f} decades; E-reg {win['E-reg']:.2f}; control {win['L-reg']:.2f};"
      f" full system {'converged, window %.2f' % w_full if conv else 'NOT converged'})")
    # POST-HOC DIAGNOSTIC (after seeing the frozen run; no verdict weight): truncate the grid inside r_w = 0.82 (GM a_M)^(1/4)/H
    r_w = 0.82 * (GM * aM) ** 0.25 / H
    resid_terms = {k: float(np.max(np.abs((2 - s_["alpha"]) * s_["g"] - s_["alpha"] * s_["wc"] - s_["S"]) /
                                  np.maximum.reduce([np.abs(s_["S"]), np.abs(s_["alpha"] * s_["wc"]), np.abs((2 - s_["alpha"]) * s_["g"])])))
                   for k, s_ in runs.items()}
    P(f"\nPOST-HOC (no verdict weight): Phi-equation residual relative to the largest term (K5 used S alone): {resid_terms}")
    P(f"POST-HOC (no verdict weight): convective crossover r_w = 0.82 (GM a_M)^(1/4)/H = {r_w:.2e}; rerun E-cusp on r in [1e-9, 1e-4]")
    R_full = R
    globals()["R"] = np.logspace(-9, -4, 2200)
    ph1 = solve("cusp", -1e-5, phase1_only=True)
    report(ph1, "post-hoc E-cusp r<=1e-4, phase 1")
    iN = np.where((R > 3 * bP) & (R < 0.1 * math.sqrt(GM / aM)))[0]
    PhiNt = GM / np.sqrt(R ** 2 + bP ** 2)
    core = float(np.median(ph1["beta1"][iN] / ((abs(c1) / abs(-1e-5)) * PhiNt[iN])))
    P(f"   Newtonian-core beta/((|c1|/|c2|) Phi_N) = {core:.3f}")
    ph2 = solve("cusp", -1e-5)
    P(f"   full system (back-reaction on): status {ph2['status']} after {ph2['it']} iterations")
    if ph2["status"] == "ok":
        report(ph2, "post-hoc E-cusp r<=1e-4, full")
    posthoc = dict(r_w=r_w, resid_rel_largest=resid_terms, trunc_phase1_window=window(ph1)[0], trunc_core_beta_coef=core,
                   trunc_max_beta=float(np.max(np.abs(ph1["beta1"]))), trunc_full_status=ph2["status"],
                   trunc_full_window=(window(ph2)[0] if ph2["status"] == "ok" else None))
    globals()["R"] = R_full
    res = {k: dict(window_decades_phase1=win[k], resid=float(s_["resid"]), max_w=float(np.max(np.abs(s_["w"]))),
                   max_beta_phase1=float(np.max(np.abs(s_["beta1"]))), beta_core_coef=float(s_["beta_coef"])) for k, s_ in runs.items()}
    res["E-cusp_full"] = dict(status=full["E-cusp"]["status"], window=w_full)
    res["verdict"] = lane
    res["K6_closed_form_dev"] = float(dev.max())
    res["posthoc"] = posthoc
else:
    runs = {"MU1": solve("mu1", -1e-5, phase1_only=True), "MU2": solve("reg", -1e-5, phase1_only=True),
            "MU3": solve("cusp", -1e-3, phase1_only=True), "MU4": solve("mu4", -1e-5, phase1_only=True)}
    win = {k: report(s, k) for k, s in runs.items()}
    base = json.load(open(os.path.join(HERE, "solve_results.json")))["results"]
    far = np.where((R > 1e-4) & (R < 1e-2))[0]
    mu = {"MU1 alpha0 1.9: linear far field (slope -> -2)": abs(np.median(runs["MU1"]["slope"][far]) + 2) < 0.05,
          "MU2 cusp removed: MOND window lost": win["MU2"] < base["E-cusp"]["window_decades_phase1"] - 0.3,
          "MU3 c2 -1e-3: window shrinks (h_c x100)": win["MU3"] < base["E-cusp"]["window_decades_phase1"] - 0.3,
          "MU4 cusp sign reversed: no attractive solution": runs["MU4"]["status"] != "ok" or np.any(runs["MU4"]["g"] <= 0)}
    for k, ok in mu.items():
        P(f"MUTATE {k}: {ok}")
    res = {k: dict(window_decades=win[k], status=s["status"], gmin=float(np.min(s["g"]))) for k, s in runs.items()}
    json.dump(dict(mutate=True, results=res, controls={k: bool(v) for k, v in mu.items()}),
              open(os.path.join(HERE, f"solve_results{SUF}.json"), "w"), indent=1)
    sys.exit(1 if all(mu.values()) else 2)
json.dump(dict(mutate=False, results=res, checks=checks), open(os.path.join(HERE, f"solve_results{SUF}.json"), "w"), indent=1)
P(f"\nchecks: {sum(c['pass'] for c in checks)}/{len(checks)} pass")
sys.exit(0 if all(c["pass"] for c in checks) else 1)
