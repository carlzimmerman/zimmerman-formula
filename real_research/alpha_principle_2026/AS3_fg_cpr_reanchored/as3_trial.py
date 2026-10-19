"""AS3 trial (AS2_PREREGISTRATION.md + Amendment 1 as incorporated by AS3_PREREGISTRATION.md).
Graded: EH + R^2 (n = 2) with SM matter.  Reference (reported, not graded): EH (n = 1) with SM matter, same scheme.
Usage: python3 as3_trial.py     (no MUTATE control is pre-registered for the trial itself; MUTATE_1..3 live in the gate / classifier scripts)
Order: (0) all gates re-run here (G-MAT, HK-CPR, G-CPR-EH (i)+(ii re-anchored), G-CPR-R2 (i)+(ii), G0); any failure -> NOT COMPLETED, stop.
(1) f_g formula on the flat background in CPR's gauge (rho = 0, alpha = 0, |beta| -> inf) with the eta convention; stop rule.
(2) SM fixed points n = 1, 2: all real roots from the frozen grids, domain, admissibility, edge flags, selection.
(3) f_g*, P, classification; (4) reported-not-graded systematics.
Exit 0 iff the gates pass and the pipeline completes (whatever the class)."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
_AS2 = Path(__file__).resolve().parent.parent / "AS2_fg_cpr_scheme"
if str(_AS2) not in sys.path:
    sys.path.insert(0, str(_AS2))
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
import as2_common as A
import as2_gmat
import as3_gcpr as G

C1 = A.C1
RG = C1.RG
SM = {A.NS: 4, A.ND: sp.Rational(45, 2), A.NV: 12}
XI = A.FG1.xi
E_ = A.FG1.e


def gates():
    print("(0) GATES (re-run here)")
    ok_mat, _, _ = as2_gmat.run(verbose=False)
    for f_ in as2_gmat.fails:
        print("   G-MAT failure:", f_)
    print(f"   G-MAT: {'PASS' if ok_mat else 'FAIL'}")
    ok_cpr, _ = G.run("NORMAL", verbose=False)
    print(f"   HK-CPR, G-CPR-EH (i), (ii re-anchored), G-CPR-R2 (i), (ii): {'PASS' if ok_cpr else 'FAIL ' + str(G.fails)}")
    b3 = C1.laneB_b3()
    g0ok = (abs(C1.downstream_P(b3.fg) - b3.c5) < 1e-9 and abs(C1.downstream_P(0.04795) / 92.914 - 1) < 1e-4
            and abs(C1.downstream_P(0.009805) / 137.036 - 1) < 1e-4 and abs(C1.downstream_P(b3.f_needed) - b3.c6) < 1e-9)
    print(f"   G0: {'PASS' if g0ok else 'FAIL'}")
    return ok_mat and ok_cpr and g0ok


def scan(n, HK, Xm_SM):
    X = A.X_gravity(HK, with_eta=True, order_f=n) + Xm_SM
    bet = A.beta_system(X, n)
    roots, f, J = A.find_roots(bet, n, grid=True)
    rows = []
    for r in roots:
        glb = A.to_glb(r)
        dom, edge = A.in_domain(glb)
        adm = A.admissible(glb)
        th = A.crit_exponents(J, r)
        rows.append(dict(gt=np.array(r), glb=glb, dom=dom, edge=edge, adm=adm and dom, theta=th))
    return rows, bet


def fg_at(fg_expr, gt, xi_val=1):
    g2v = gt[2] if len(gt) > 2 else 0.0
    sub = {A.F0: gt[0], A.F1: gt[1], A.F2: 2 * g2v, A.dF1: 2 * gt[1], A.dF2: 0}
    e = fg_expr.subs(sub)
    return float(e.subs(XI, xi_val)) if xi_val is not None else e


def two_loop_P(gYs, b2):
    """Lane B's b2 rhs (by import): up-run of the measured couplings M_Z -> M_Pl (two loop), then down-run with g1 = sqrt(5/3) g_Y*."""
    y0 = np.array([np.sqrt(4 * np.pi / b2.a1), np.sqrt(4 * np.pi / b2.a2), np.sqrt(4 * np.pi / b2.a3), 0.94])
    up = solve_ivp(b2.rhs, [np.log(RG.MZ), np.log(RG.MPL)], y0, args=(True,), rtol=1e-11, atol=1e-13)
    yP = up.y[:, -1].copy()
    yP[0] = np.sqrt(5 / 3) * gYs
    out = {}
    for tl in (True, False):
        dn = solve_ivp(b2.rhs, [np.log(RG.MPL), np.log(RG.MZ)], yP, args=(tl,), rtol=1e-11, atol=1e-13)
        g1MZ = dn.y[0, -1]
        aYinv = (5 / 3) * 4 * np.pi / g1MZ**2
        out[tl] = aYinv + C1.laneB_b3().a2_mz + RG.DELTA_0_MZ
    return out[True], out[False]


def reduced_planck_P(fg):
    b3 = C1.laneB_b3()
    saved = b3.MPL
    try:
        b3.MPL = RG.MPL_RED
        return C1.downstream_P(fg)
    finally:
        b3.MPL = saved


if __name__ == "__main__":
    print("MODE: NORMAL")
    if not gates():
        print("\nVERDICT: NOT COMPLETED (a gate failed; the trial is not run)")
        sys.exit(1)

    print("\n(1) f_g on the flat background, CPR gauge rho = 0, alpha = 0, |beta| -> infinity, eta terms d_t f', d_t f''")
    fg_expr, info = A.fg_flat_cpr()
    print(f"   beta-limit: numerator degree {info['deg_num']}, denominator degree {info['deg_den']}, divergent = {info['divergent']}")
    if fg_expr is None or info.get("divergent"):
        print("\nVERDICT: NOT COMPLETED (stop rule: the |beta| -> infinity limit of the F-bar^2 coefficient diverges)")
        sys.exit(1)
    print(f"   beta -> +inf and -inf limits equal: {info['minus_inf_equal']}; parity (SD = ASD weight): {info['parity_ok']}")
    if not info["parity_ok"]:
        print("\nVERDICT: NOT COMPLETED (f_g computation inconsistent: parity check failed)")
        sys.exit(1)
    fg_expr = sp.simplify(fg_expr)
    print(f"   free symbols: {sorted(map(str, fg_expr.free_symbols))}")
    print(f"   f_g(F0 = f, F1 = f', F2 = f'', dF1 = d_t f', dF2 = d_t f'', xi) = {sp.factor(fg_expr)}")
    dxi = sp.simplify(sp.diff(fg_expr, XI))
    print(f"   d f_g / d xi = {sp.factor(dxi)}")

    HK = G.heat_kernels()
    Xm, parts = A.X_matter(HK)
    Xm_SM = sp.expand(Xm.subs(SM))
    print(f"\n(2) SM matter (type I), (16 pi^2/V) d_t Gamma contribution: {sp.nsimplify(Xm_SM)}")
    results = {}
    for n in (1, 2):
        rows, bet = scan(n, HK, Xm_SM)
        lab = "EH reference (n = 1)" if n == 1 else "R^2 trial (n = 2), GRADED"
        print(f"\n   {lab}: {len(rows)} real root(s) from the frozen grid")
        for r in rows:
            gl = r["glb"]
            print(f"     g~ = {np.array2string(r['gt'], precision=7)}  (g, lambda{', b' if n == 2 else ''}) = "
                  f"({gl[0]:.6g}, {gl[1]:.6g}{', %.6g' % gl[2] if n == 2 else ''})  in-domain {r['dom']}  edge {r['edge']}  admissible {r['adm']}"
                  f"  theta = {np.array2string(r['theta'], precision=4)}")
        adm = [r for r in rows if r["adm"]]
        if len(adm) == 1:
            fp = adm[0]
            fgv = fg_at(fg_expr, fp["gt"])
            status = "FP"
        elif len(adm) == 0:
            fp, fgv, status = None, None, "NOT PREDICTED (no admissible root)"
        else:
            fp, fgv, status = None, None, "NOT DIAGNOSTIC (several admissible roots)"
        P_ = None
        if fp is not None:
            if fgv <= 0:
                status = "NOT PREDICTED (f_g* <= 0)"
            else:
                P_ = C1.downstream_P(fgv)
        results[n] = dict(fp=fp, fg=fgv, P=P_, status=status)
        print(f"   selection: {status}")
        if fp is not None:
            fg_xi0 = sp.limit(fg_at(fg_expr, fp["gt"], xi_val=None), XI, 0)
            print(f"   f_g* = {fgv:.8f}  (xi = 1, frozen); xi -> 0: {float(fg_xi0):.8f}; d f_g/d xi at the FP: "
                  f"{float(dxi.subs({A.F0: fp['gt'][0], A.F1: fp['gt'][1], A.F2: 2 * (fp['gt'][2] if n == 2 else 0), A.dF1: 2 * fp['gt'][1], A.dF2: 0, XI: 1})):.3e}")
            print(f"   f_g*/0.04795 = {fgv/0.04795:.5f}; f_g*/0.009805 = {fgv/0.009805:.5f}; theta_Y = -2 f_g* = {-2*fgv:.6f} "
                  f"({'g_Y* IR-attractive (UV-repulsive)' if fgv > 0 else 'n/a'})")
            if P_ is not None:
                print(f"   g_Y* = {C1.gY_star_from_fg(fgv):.6f};  P = alpha^-1(0) = {P_:.5f}")

    print("\n(3) CLASSIFICATION")
    rR2, rEH = results[2], results[1]
    if rR2["P"] is None:
        verdict = rR2["status"]
        print(f"   graded R^2 trial: {verdict}")
    else:
        Pref = rEH["P"]
        cls, delta = A.classify2(rR2["P"], Pref)
        verdict = cls
        print(f"   P_R2 = {rR2['P']:.5f}; P_EH (reference) = {('%.5f' % Pref) if Pref is not None else 'none -> 44.12 used'}")
        print(f"   Delta = {delta*100:+.3f} %;  |P_R2 - 137.036| = {abs(rR2['P']-C1.ALPHA_INV0):.5f};  "
              f"|P_EH - 137.036| = {(abs(Pref-C1.ALPHA_INV0) if Pref is not None else 44.12):.5f}")
        if Pref is not None:
            print(f"   truncation shift |P_R2 - P_EH| = {abs(rR2['P'] - Pref):.5f}")
        print(f"   CLASS: {cls}")

    print("\n(4) reported, not graded: systematics")
    b2 = C1._exec_lane_b_script("b2_required_boundary.py")
    for n, lab in ((2, "R^2 trial"), (1, "EH reference")):
        r = results[n]
        if r["P"] is None:
            continue
        gYs = C1.gY_star_from_fg(r["fg"])
        P2, P1chk = two_loop_P(gYs, b2)
        Pred = reduced_planck_P(r["fg"])
        print(f"   {lab}: one-loop P = {r['P']:.5f}; one-loop switch of the two-loop integrator = {P1chk:.5f} (check, diff {P1chk - r['P']:+.1e});"
              f" two-loop P = {P2:.5f} (shift {P2 - r['P']:+.5f}); run started at the reduced Planck mass: P = {Pred:.5f} (shift {Pred - r['P']:+.5f})")
    print(f"\nVERDICT (graded R^2 trial): {verdict}")
    print("Meaning (frozen): AGREES would NOT be a derivation of alpha (alpha_2, the hadronic offset and the masses are measured; convergence"
          " untested); CLOSER / NO IMPROVEMENT = the route is not supported at this truncation; kappa and Z enter nowhere.")
    sys.exit(0)
