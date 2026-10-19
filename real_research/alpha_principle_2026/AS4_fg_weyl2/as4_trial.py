"""AS4 trial (AS4_PREREGISTRATION.md).  Graded: EH + C^2 + R^2 with SM matter (BMS 0902.4630 scheme, type-I matter).
Reference (reported, not graded): EH with SM matter, same scheme.
Usage: python3 as4_trial.py
(0) gates re-run (G-PUB, G-MAT-C2, G0); any failure -> NOT COMPLETED.  (1) flat-space f_g with the C^2 term by kernel restriction.
(2) SM fixed points on the frozen grids, admissibility (spin-2 incl. C^2 and spin-0 denominators), selection.  (3) f_g, numerical beta-limit
check (stop rule), P, classes (same-class rule).  (4) reported systematics."""
import sys
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
import as4_common as A
import as4_gates as GT
import functools
print = functools.partial(print, flush=True)

C1 = A.C1
SM = {A.NS: 4, A.ND: sp.Rational(45, 2), A.NV: 12}
XI, E_ = A.FG1.xi, A.FG1.e


def select_class(Ps, Pref):
    cls = [A.A2.classify2(p, Pref)[0] for p in Ps]
    return (cls[0] if len(set(cls)) == 1 else "NOT DIAGNOSTIC"), cls


def fg_at(fgx, r, xi_val=1):
    g2 = r[2] if len(r) > 2 else 0.0
    g3 = r[3] if len(r) > 3 else 0.0
    sub = {A.U0: r[0], A.U1: r[1], A.U2: g2, A.U3: g3, A.U1d: 2 * r[1], A.U2d: 0, A.U3d: 0}
    v = fgx.subs(sub)
    return float(v.subs(XI, xi_val)) if xi_val is not None else v


if __name__ == "__main__":
    print("MODE: NORMAL")
    print("(0) GATES")
    ok_g, _, HK = GT.run("NORMAL", verbose=False)
    b3 = C1.laneB_b3()
    g0ok = (abs(C1.downstream_P(b3.fg) - b3.c5) < 1e-9 and abs(C1.downstream_P(0.04795) / 92.914 - 1) < 1e-4
            and abs(C1.downstream_P(0.009805) / 137.036 - 1) < 1e-4)
    print(f"   gates G-PUB + G-MAT-C2: {'PASS' if ok_g else 'FAIL ' + str(GT.fails)};  G0: {'PASS' if g0ok else 'FAIL'}")
    if not (ok_g and g0ok):
        print("\nVERDICT: NOT COMPLETED (a gate failed; the trial is not run)")
        sys.exit(1)

    print("\n(1) flat-space f_g with the C^2 term (kernel restriction: TT + conformal mode + photon; BMS gauge rho = 0, hard limit)")
    fgx, ker_ok, mats = A.fg_flat_bms()
    print(f"   gauge-fixing kernel check: {ker_ok}")
    if not ker_ok:
        print("\nVERDICT: NOT COMPLETED (stop rule: kernel restriction invalid)")
        sys.exit(1)
    print(f"   f_g = {fgx}")
    print(f"   free symbols: {sorted(map(str, fgx.free_symbols))};  d f_g/d xi = {sp.simplify(sp.diff(fgx, XI))}")

    tr = A.bms_traces(HK)
    sc, di, ve = A.matter_type_I(HK)
    mat = {c: sp.nsimplify(4 * sc[c] + sp.Rational(45, 2) * di[c] + 12 * ve[c]) for c in ("1", "R", "R2", "W")}
    print(f"\n(2) SM matter (type I, Einstein space), (16 pi^2/V) d_t Gamma: {mat}")
    out = {}
    for case in ("EH", "HD"):
        eh = case == "EH"
        t_ = A.bms_traces(HK, eh=True) if eh else tr
        tot = {}
        for part in (t_["S_2T"], t_["S_hh"], t_["S_1T"], t_["S_0"], mat):
            tot = A.add(tot, part)
        fB = A.beta_numeric(tot, eh=eh)
        nvar = 2 if eh else 4
        roots = A.find_roots_num(fB, A.grid_starts(nvar))
        lab = "EH reference (reported)" if eh else "EH + C^2 + R^2 with SM matter (GRADED)"
        print(f"\n   {lab}: {len(roots)} real root(s) from the frozen grid")
        rows = []
        for r in roots:
            gl = A.to_glb(r)
            dom, edge = A.in_domain(r)
            d2, d0 = A.denominators(r)
            adm = A.admissible(r) and dom
            th = A.crit_num(fB, r)
            fgv = fg_at(fgx, r)
            Pv = C1.downstream_P(fgv) if fgv > 0 else None
            rows.append(dict(r=r, gl=gl, dom=dom, edge=edge, adm=adm, th=th, fg=fgv, P=Pv, d2=d2, d0=d0))
            print(f"     g = {np.array2string(np.array(r), precision=7)}  (g, lambda) = ({gl[0]:.6g}, {gl[1]:.6g})  in-domain {dom}  edge {edge}")
            print(f"        denominators: spin-2 (2g3 - g1 - g0) = {d2:.6g}, spin-0 -(6g2 + g1 + 2g0/3) = {d0:.6g}  -> admissible {adm};"
                  f"  theta = {np.array2string(th, precision=4)}")
            print(f"        f_g = {fgv:.8f}" + (f", g_Y* = {C1.gY_star_from_fg(fgv):.6f}, P = {Pv:.5f}" if Pv is not None else ", f_g <= 0: no P")
                  + ("" if adm else "  [not admissible: reported only]"))
        adm_rows = [x for x in rows if x["adm"]]
        if not adm_rows:
            status = "NOT PREDICTED (no admissible root)"
        elif any(x["fg"] <= 0 for x in adm_rows):
            status = "NOT PREDICTED (f_g* <= 0 at an admissible root)"
        elif len(adm_rows) == 1:
            status = "FP"
        else:
            status = "SEVERAL"
        out[case] = dict(rows=rows, adm=adm_rows, status=status)
        print(f"   selection: {status} ({len(adm_rows)} admissible)")

    # stop rule: numerical beta-limit convergence at every admissible root of both cases
    print("\n(3) stop rule: finite-beta full traces converge to the kernel-restricted f_g")
    stop = False
    for case in ("EH", "HD"):
        for x in out[case]["adm"]:
            r = x["r"]
            vals = {A.U0: r[0], A.U1: r[1], A.U2: (r[2] if len(r) > 2 else 0), A.U3: (r[3] if len(r) > 3 else 0),
                    A.U1d: 2 * r[1], A.U2d: 0, A.U3d: 0, E_: 1, XI: 1}
            import mpmath as mp
            ratv = {k_: (sp.Rational(float(v_)) if not isinstance(v_, (int, sp.Integer)) else v_) for k_, v_ in vals.items()}
            fexact = mp.mpf(str(sp.N(fgx.subs(ratv).subs(XI, 1), 40)))       # restricted value at the same exact rational couplings
            seq = []
            for bv in (1e3, 1e5, 1e7):
                fn = A.fg_numeric_full(mats, vals, bv)
                seq.append(float(abs(fn / fexact - 1)))
                print(f"   {case} root g = {np.array2string(np.array(r), precision=5)}: beta = {bv:.0e}: f_g(full) = {mp.nstr(fn, 15)},"
                      f" restricted {mp.nstr(fexact, 15)}, rel. diff {seq[-1]:.2e}")
            conv = seq[2] < 1e-4 and seq[2] <= seq[1] <= seq[0]
            print(f"   convergence: {conv}")
            stop = stop or not conv
    if stop:
        print("\nVERDICT: NOT COMPLETED (stop rule: the beta -> infinity limit does not converge to the restricted value)")
        sys.exit(1)

    print("\n(4) CLASSIFICATION")
    eh = out["EH"]
    Pref = eh["adm"][0]["P"] if eh["status"] == "FP" else None
    print(f"   EH reference: {eh['status']}" + (f", P_EH = {Pref:.5f}" if Pref is not None else " -> CLOSER reference falls back to 44.12"))
    hd = out["HD"]
    if hd["status"].startswith("NOT"):
        verdict = hd["status"]
    else:
        verdict, cls = select_class([x["P"] for x in hd["adm"]], Pref)
        for x, c in zip(hd["adm"], cls):
            print(f"   admissible root (g, lambda, g2, g3) = ({x['gl'][0]:.6g}, {x['gl'][1]:.6g}, {x['r'][2]:.6g}, {x['r'][3]:.6g}): P = {x['P']:.5f},"
                  f" Delta = {(x['P']/C1.ALPHA_INV0-1)*100:+.3f} %, class of this root: {c}")
    print(f"   CLASS (graded): {verdict}")

    print("\n(5) reported, not graded: systematics")
    b2 = C1._exec_lane_b_script("b2_required_boundary.py")
    import as4_systematics as H
    for case in ("EH", "HD"):
        for x in out[case]["rows"]:
            if x["P"] is None or not x["dom"]:
                continue
            gYs = C1.gY_star_from_fg(x["fg"])
            P2, P1 = H.two_loop_P(gYs, b2)
            Pr = H.reduced_planck_P(x["fg"])
            print(f"   {case} root (g, lambda) = ({x['gl'][0]:.5g}, {x['gl'][1]:.5g}){' [admissible]' if x['adm'] else ' [not admissible]'}: P = {x['P']:.5f};"
                  f" two-loop {P2:.5f} ({P2 - x['P']:+.5f}, 1-loop switch check {P1 - x['P']:+.1e}); reduced Planck {Pr:.5f} ({Pr - x['P']:+.5f});"
                  f" theta_Y = {-2*x['fg']:.6f}")
    print(f"\nVERDICT (graded EH + C^2 + R^2 trial): {verdict}")
    print("Meaning (frozen): AGREES would NOT be a derivation of alpha; CLOSER / NO IMPROVEMENT = the route is not supported at this truncation;"
          " NOT PREDICTED / NOT DIAGNOSTIC / NOT COMPLETED = no statement about alpha; kappa and Z enter nowhere.")
    sys.exit(0)
