#!/usr/bin/env python3
"""LW1 Milky Way stress, POST-RESULT: form R's pass tested as hard as a fail. No line moved, no grade changed. Same Newton fields. Checks: Eilers chi2 and K scale length (X5's reported lines, not UR3's gate), g_c at r in place of R, the passing cells. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
sys.argv = [sys.argv[0], "--stress"]; HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "lw1_mw.py")).read(); src = src[:src.index('if "--grade" in sys.argv:')]; exec(compile(src, "lw1_mw_head", "exec"))
EIL_R, EIL_V, EIL_E = ns["EIL_R"], ns["EIL_V"], ns["EIL_E"]; A_ = np.vstack([np.ones_like(BR_R), BR_R - R0]).T; OUT = []; RES = {}
P("LW1 MW stress, post-result; form R only unless said. X5's reported lines: chi2_RC <= 61.2 (Eilers), h 2.72 +- 0.15, K_z(R0) 66.4 +- 2.2. kappa = 1/2 FITTED; not theory closed")
for foot in ("canonical", "alt"):
    a0 = L.A0_SI[foot]; a0k = a0 * PS.KPC / 1e6; pas = []; pas_r = 0; rows = []
    for c, rhof in spec():
        Mu = PS.mass_unit(a0); g = ns["mw_grid"](6.6e10 / Mu); rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); Mt = 2 * float(np.sum(rho1 * g.vol)); pr = PS.Problem(g, rho1, Mt, 0.0, Lam=0.0); Phi = pr.solve_newton(); oN = ns["mw_obs"](g, Phi, a0)
        Rall = np.r_[R0, OR, BR_R]; vb = L.vc_plane(ns, g, Phi, a0, Rall); gb = vb ** 2 / Rall; nu1 = lambda x: 0.5 + np.sqrt(0.25 + a0k / np.maximum(x, 1e-30)); gc = (nu1(gb) - 1) * gb; nR = 1 + len(OR); vR = np.sqrt(vb ** 2 + Rall * gc); K = np.array(oN["K"]) + gc[nR:] * 1.1 / BR_R / KZU; K0 = oN["K_R0"] + gc[0] * 1.1 / R0 / KZU; a = lines(float(vR[0]), K, float(K0), vR[1:nR])
        ve = L.vc_plane(ns, g, Phi, a0, EIL_R); gbe = ve ** 2 / EIL_R; vE2 = np.sqrt(ve ** 2 * nu1(gbe)); cR = float(np.sum(((vE2 - EIL_V) / EIL_E) ** 2)); sl = np.linalg.lstsq(A_, np.log(np.maximum(K, 1e-9)), rcond=None)[0][1]; h = -1 / sl if sl < 0 else float("inf")
        # g_c at r = hypot(R, 1.1): the speed curve interpolated in R, spherical-equivalent, as UR3's halo term
        rk = np.hypot(BR_R, 1.1); r00 = math.hypot(R0, 1.1); gbr = np.interp(rk, Rall[np.argsort(Rall)], gb[np.argsort(Rall)]); gcr = (nu1(gbr) - 1) * gbr; Kv = np.array(oN["K"]) + gcr * 1.1 / rk / KZU; gb0 = float(np.interp(r00, Rall[np.argsort(Rall)], gb[np.argsort(Rall)])); K0v = oN["K_R0"] + (float(nu1(gb0)) - 1) * gb0 * 1.1 / r00 / KZU; b = lines(float(vR[0]), Kv, float(K0v), vR[1:nR])
        ok = all(a[l] for l in ("L1", "L2a", "L2b", "L3")); ok2 = all(b[l] for l in ("L1", "L2a", "L2b", "L3")); pr_ = c["tag_Rd_IN"] and c["tag_Mstar_IN"]; pas_r += int(ok2 and pr_)
        if ok: pas.append(dict(c, vc=a["vc_R0"], K0=a["K_R0"], chiK=a["chi2_Kz"], chiO=a["chi2_Ou"], chiRC=cR, h=h, inprior=pr_, v_ok=ok2, Mb=Mt * Mu))
    n_i = [x for x in pas if x["inprior"]]; RES[foot] = dict(passing=pas, n=len(pas), n_inprior=len(n_i), n_inprior_gc_at_r=pas_r, n_rc_ok=sum(x["chiRC"] <= 61.2 for x in pas), n_rc_ok_inprior=sum(x["chiRC"] <= 61.2 for x in n_i))
    P(f"[{foot}] form R all four {len(pas)}, in priors {len(n_i)}; g_c at r instead of R, in priors {pas_r}; of the all-four, chi2_RC <= 61.2: {RES[foot]['n_rc_ok']}, in priors {RES[foot]['n_rc_ok_inprior']}")
    for x in n_i: P(f"   in-prior: Sig_b {x['sig_b']} M_bb {x['M_bb']:.3g} R_d {x['R_d']:.2f} M* {x['Mstar']:.2e} V_c {x['vc']:.1f} K(R0) {x['K0']:.1f} ({(x['K0'] - 66.4) / 2.2:+.1f} sigma) chi2_Kz {x['chiK']:.1f} chi2_Ou {x['chiO']:.1f} chi2_RC {x['chiRC']:.1f} h {x['h']:.2f} ({(x['h'] - 2.72) / 0.15:+.1f} sigma)")
json.dump(RES, open(os.path.join(HERE, "lw1_mw_stress.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "lw1_mw_stress.out"), "w").write("\n".join(OUT) + "\n")
