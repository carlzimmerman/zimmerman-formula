#!/usr/bin/env python3
"""GRW1 known answers KA1-KA6 (criteria 11c19a2c5f section 4; amendment A1 4dfa022e34, POST HOC: KA2(b) on CLASS's own
physics, KA5(a) in exact rationals; the as-frozen values are printed too). Usage: python3 grw1_ka.py -> grw1_ka.json / grw1_ka.out.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grw1_lib as GL
import grw1_obs as GO

OUT = []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))
RES = dict(lane="GRW1", criteria="11c19a2c5f", amendment_A1="4dfa022e34", note=GO.kappa_note, KA={})
from fractions import Fraction as Fr
wb, wc = GL.OB / (GL.OB + GL.OD), GL.OD / (GL.OB + GL.OD)

# KA1 ------------------------------------------------------------------------------------------------------------------
r1 = [abs(GO.AX0 / GO.SV5["A_X0"] - 1), abs(GO.SIGREL / GO.SV5["sigma_A_rel"] - 1), abs(GO.CHI2_X0 / GO.CHI2_REC - 1)]
ok1 = bool(r1[0] <= 1e-6 and r1[1] <= 1e-6 and r1[2] <= 1e-3)
RES["KA"]["KA1"] = dict(A_X0=GO.AX0, sigma_A_rel=GO.SIGREL, chi2_X0=GO.CHI2_X0, record=[GO.SV5["A_X0"], GO.SV5["sigma_A_rel"], GO.CHI2_REC],
                        rel=r1, line_L1=GO.LINE_L1, pass_=ok1)
P(f"KA1 PR4 row: A_X0 {GO.AX0:.7f} (record {GO.SV5['A_X0']:.7f}), sigma_A,rel {GO.SIGREL:.7f} (record {GO.SV5['sigma_A_rel']:.7f}), "
  f"chi2 {GO.CHI2_X0:.4f} (record {GO.CHI2_REC:.4f}) -> {'PASS' if ok1 else 'FAIL'}; L1 line |r_eff - 1| <= {GO.LINE_L1:.6f}")

# KA2 ------------------------------------------------------------------------------------------------------------------
Mref = GL.run_class(None); bgref = GL.Background(Mref)
icref = GL.transfer_ic(Mref, GL.ZSTART, "d_cdm")
ref = GL.Run(bgref, "off", GL.A0["canonical"], GL.const_cs(0.0), icref).solve()
z = ref["z"]; dl = wb * ref["db"][:, 0, :] + wc * ref["dc"][:, 0, :]; Dl = wb * ref["Db"][:, 0, :] + wc * ref["Dc"][:, 0, :]
lk = np.log(GL.KGRID); i01 = lambda arr: np.interp(math.log(0.1), lk, arr)
j0 = GO.zindex(z, 0.0)
rows2 = []
for zz in (0.0, 0.295, 0.51, 0.706, 0.919, 1.5, 2.0, 3.0):
    j = GO.zindex(z, zz)
    D = i01(dl[:, j]) / i01(dl[:, j0]); f = i01(Dl[:, j]) / i01(dl[:, j])
    Pz = GO.Pk(GO.KS, zz); V = GO.interp_k((ref["Db"][:, 0, j] / dl[:, j]) ** 2)
    fs8 = math.sqrt(GO.sigma2(Pz * V))
    clD = Mref.scale_independent_growth_factor(zz) / Mref.scale_independent_growth_factor(0.0)
    clf = Mref.scale_independent_growth_factor_f(zz); clfs8 = clf * GO.ML.sigma(GO.R8, zz)
    rows2.append(dict(z=zz, D=D, D_class=clD, f=f, f_class=clf, fs8=fs8, fs8_class=clfs8,
                      rel=max(abs(D / clD - 1), abs(f / clf - 1), abs(fs8 / clfs8 - 1))))
ka2a = max(r["rel"] for r in rows2)
def cl_delta(M, zz, key):
    T = M.get_transfer(zz); k = T["k (h/Mpc)"] * GL.h
    return np.interp(lk, np.log(k), wb * T["d_b"] + wc * T[key])
rows2b = []; m04 = GL.KGRID >= 0.04
for zz in (0.0, 1.0, 2.0, 3.0):
    j = GO.zindex(z, zz); r = (dl[:, j] / cl_delta(Mref, zz, "d_cdm")) ** 2
    rows2b.append(dict(z=zz, max_dev_k04=float(np.max(np.abs(r[m04] - 1))), at_k={f"{k:.4g}": float(x) for k, x in zip(GL.KGRID[::7], r[::7])}))
ka2b = max(r["max_dev_k04"] for r in rows2b)
bg0 = GL.Background(Mref); bg0.cIGM = 0.0                                   # A1a: CLASS's own baryon physics
ref0 = GL.Run(bg0, "off", GL.A0["canonical"], GL.const_cs(0.0), icref).solve()
rows2b_A1 = []
for zz in (0.0, 1.0, 2.0, 3.0):
    j = GO.zindex(ref0["z"], zz); r = ((wb * ref0["db"][:, 0, j] + wc * ref0["dc"][:, 0, j]) / cl_delta(Mref, zz, "d_cdm")) ** 2
    rows2b_A1.append(dict(z=zz, max_dev_k04=float(np.max(np.abs(r[m04] - 1)))))
ka2b_A1 = max(r["max_dev_k04"] for r in rows2b_A1)
ok2_frozen = bool(ka2a <= 2e-3 and ka2b <= 1e-2)
ok2 = bool(ka2a <= 2e-3 and ka2b_A1 <= 1e-2)
RES["KA"]["KA2"] = dict(a=rows2, a_max_rel=ka2a, b=rows2b, b_max=ka2b, b_A1=rows2b_A1, b_max_A1=ka2b_A1, pass_frozen=ok2_frozen, sigma8_mine=math.sqrt(GO.sigma2(GO.PREF[0.0])), sigma8_class=GO.ML.sigma8(),
                        nfev=ref["nfev"], pass_=ok2)
P(f"KA2 cold reference, law off, engine from z {GL.ZSTART:.0f} vs CLASS: (a) D, f, f sigma8 at 8 z max rel {ka2a:.2e} (line 2e-3); "
  f"(b) P ratio k >= 0.04 at z 0-3 max |dev| as frozen (engine with IGM heating vs CLASS without) {ka2b:.2e} -> {'PASS' if ok2_frozen else 'FAIL'} as frozen; "
  f"A1a (heating zeroed, CLASS's own physics) {ka2b_A1:.2e} (line 1e-2) -> {'PASS' if ok2 else 'FAIL'}")
P("     f sigma8 mine / CLASS: " + ", ".join(f"z {r['z']:g} {r['fs8']:.5f}/{r['fs8_class']:.5f}" for r in rows2))
P("     P ratio at z 0 (reported incl. k < 0.04): " + ", ".join(f"{k} {v:.4f}" for k, v in rows2b[0]["at_k"].items()))
P(f"     sigma8 from my top-hat on CLASS P: {RES['KA']['KA2']['sigma8_mine']:.5f} vs CLASS {GO.ML.sigma8():.5f}")

# KA3 ------------------------------------------------------------------------------------------------------------------
def eds_slope(f, tr, cfix=None, q2fix=0.0):
    run = GL.Run(GL.EdS(f), tr, 1.0, GL.const_cs(0.0), [np.ones(1), np.full(1, 0.3), np.zeros(1), np.zeros(1)],
                 kgrid=[1.0], q2fix=q2fix, cfix=cfix)
    so = solve_ivp(run.rhs, (0.0, 20.0), run.y0, method="DOP853", rtol=1e-12, atol=1e-14)
    Y = so.y[:, -1].reshape(4, 1, len(GL.MU)); return float(Y[1, 0, 0] / Y[0, 0, 0]), so.nfev
rows3 = []
for f in (0.157, 0.05, 0.5):
    pb = (-1 + math.sqrt(1 + 24 * f)) / 4
    lam = (f + math.sqrt(f * f + 4 * f * (1 - f))) / 2; pA = (-0.5 + math.sqrt(0.25 + 6 * lam)) / 2
    sa, _ = eds_slope(f, "smooth"); sb, _ = eds_slope(f, "TA", cfix=1.0, q2fix=1e8); sc, nfc = eds_slope(f, "TA", cfix=0.0, q2fix=1e7)
    rows3.append(dict(f=f, p_baryons=pb, slope_a=sa, p_TA_c1=pA, slope_b=sb, slope_c=sc, nfev_c=nfc,
                      err=[abs(sa - pb), abs(sb - pA), abs(sc - pb)]))
ka3 = max(max(r["err"]) for r in rows3); ok3 = bool(ka3 <= 1e-6)
RES["KA"]["KA3"] = dict(rows=rows3, max_err=ka3, pass_=ok3)
P("KA3 EdS late slopes: " + "; ".join(f"f {r['f']}: smooth {r['slope_a']:.8f} vs {r['p_baryons']:.8f}, TA c=1 {r['slope_b']:.8f} vs {r['p_TA_c1']:.8f}, "
                                        f"TA c=0 q->inf {r['slope_c']:.8f}" for r in rows3) + f"; max err {ka3:.1e} -> {'PASS' if ok3 else 'FAIL'}")

# KA4 ------------------------------------------------------------------------------------------------------------------
rows4 = []
for cs in (1000.0, 4481.0):
    M = GL.run_class(cs); bg = GL.Background(M); ic = GL.transfer_ic(M, GL.ZSTART, "d_fld")
    o = GL.Run(bg, "off", GL.A0["canonical"], GL.const_cs(cs), ic).solve()
    for zz in (0.0, 1.0, 3.0):
        j = GO.zindex(o["z"], zz)
        mine = wb * o["db"][:, 0, j] + wc * o["dc"][:, 0, j]
        cl = cl_delta(M, zz, "d_fld"); clref = cl_delta(Mref, zz, "d_cdm")
        err = np.abs(mine - cl) / np.abs(clref)
        rows4.append(dict(cs=cs, z=zz, max_err_k04=float(np.max(err[m04])), P_warm_over_ref_class={f"{k:.3g}": float(x) for k, x in zip(GL.KGRID[::9], ((cl / clref) ** 2)[::9])},
                          P_mine_over_class={f"{k:.3g}": float(x) for k, x in zip(GL.KGRID[::9], ((mine / cl) ** 2)[::9])}, nfev=o["nfev"]))
    M.struct_cleanup()
ka4 = max(r["max_err_k04"] for r in rows4); ok4 = bool(ka4 <= 1e-2)
RES["KA"]["KA4"] = dict(rows=rows4, max_err=ka4, pass_=ok4)
P(f"KA4 warm law-off engine vs CLASS fluid (c_s 1000, 4481; z 0, 1, 3): max |d_mine - d_CLASS| / |d_ref| over k >= 0.04 = {ka4:.2e} (line 1e-2) -> {'PASS' if ok4 else 'FAIL'}")
for r in rows4:
    P(f"     c_s {r['cs']:.0f} z {r['z']:g}: err {r['max_err_k04']:.1e}; CLASS P_warm/P_ref " + " ".join(f"{k}:{v:.2e}" for k, v in r["P_warm_over_ref_class"].items()))

# KA5 ------------------------------------------------------------------------------------------------------------------
rng = np.random.default_rng(11)
e5a = 0.0; e5b = 0.0; e5a_exact = 0
for _ in range(100):
    x = 10 ** rng.uniform(-4, 3); mu = rng.uniform(0, 1)
    X, U = Fr(x), Fr(mu); cX = (1 / (1 + X)) * (1 - X * U ** 2 / (1 + X))
    if (1 - cX) - (X / (1 + X)) * (1 + U ** 2 / (1 + X)) != 0: e5a_exact += 1
    c = (1 / (1 + x)) * (1 - x * mu ** 2 / (1 + x)); me = x / (1 + x); Le = 1 / (1 + x)
    e5a = max(e5a, abs((1 - c) - me * (1 + Le * mu ** 2)) / (me * (1 + Le * mu ** 2)))
    q = 10 ** rng.uniform(-2, 2); eps = rng.uniform(0, 1); muK = 10 ** rng.uniform(-1, 1); k = q * muK
    e5b = max(e5b, abs((1 - q * q / (1 + eps * q * q)) - (1 - k * k / (muK * muK + eps * k * k))))
def Fsimple(g): return g * g / (g + 1.0)                           # mu(g) g in units a0 = 1
def Finv(s):
    return brentq(lambda g: Fsimple(g) - s, 0.0, abs(s) + 2.0, xtol=1e-15, rtol=1e-14) if s > 0 else -brentq(lambda g: Fsimple(g) + s, 0.0, abs(s) + 2.0, xtol=1e-15, rtol=1e-14)
rows5c = []
N = 512; xs = np.arange(N) / N * 2 * math.pi; sn = np.sin(xs)
for xe in (0.03, 0.3, 3.0):
    amp = 1e-5 * xe                                              # Newtonian perturbation field amplitude (relative 1e-5)
    # along: mu(|g|) g = F(xe) + amp sin; mean of g fixed to xe by the constant
    def along(C): return np.array([Finv(C + amp * s) for s in sn])
    C = brentq(lambda C: along(C).mean() - xe, Fsimple(xe) - 10 * amp, Fsimple(xe) + 10 * amp, xtol=1e-18)
    dg = along(C) - xe; B1 = 2 * np.mean(dg * sn) / amp
    # across: field (u, xe); mu(sqrt(u^2 + xe^2)) u = amp sin
    def ux(s):
        if s == 0: return 0.0
        f = lambda u: (math.hypot(u, xe) / (math.hypot(u, xe) + 1.0)) * u - s
        return brentq(f, -10 * abs(s) / (xe / (1 + xe)) - 1e-30, 10 * abs(s) / (xe / (1 + xe)) + 1e-30, xtol=1e-20)
    du = np.array([ux(amp * s) for s in sn]); B0 = 2 * np.mean(du * sn) / amp
    me = xe / (1 + xe); Le = 1 / (1 + xe)
    rows5c.append(dict(x=xe, B_along=B1, B_along_formula=1 / (me * (1 + Le)), B_across=B0, B_across_formula=1 / me,
                       rel=[abs(B1 * me * (1 + Le) - 1), abs(B0 * me - 1)]))
e5c = max(max(r["rel"]) for r in rows5c)
ok5_frozen = bool(e5a <= 1e-12 and e5b <= 1e-12 and e5c <= 1e-3)
ok5 = bool(e5a_exact == 0 and e5b <= 1e-12 and e5c <= 1e-3)
RES["KA"]["KA5"] = dict(a_max=e5a, a_exact_mismatches=e5a_exact, b_max=e5b, c=rows5c, c_max=e5c, pass_frozen=ok5_frozen, pass_=ok5)
P(f"KA5 (a) 1 - c = mu_e (1 + L_e mu^2): float {e5a:.3e} (as frozen, line 1e-12: {'PASS' if e5a <= 1e-12 else 'FAIL'}); A1b exact rationals: {e5a_exact} mismatches of 100; (b) TA coefficient = TPA1 4.4 form: {e5b:.1e}; (c) 1-D AQUAL: "
  + ", ".join(f"x {r['x']}: along {r['B_along']:.5f}/{r['B_along_formula']:.5f} across {r['B_across']:.5f}/{r['B_across_formula']:.5f}" for r in rows5c)
  + f" -> {'PASS' if ok5 else 'FAIL'}")

# KA6 ------------------------------------------------------------------------------------------------------------------
Sc = GO.S_of_kz(lambda k, zz: np.full(np.shape(k), 1.37 ** 2)); e6a = float(np.max(np.abs(Sc[2:] / 1.37 ** 2 - 1)))
XA = GO.X_abs(); rows6b = [dict(L=L, rel=float(XA[L] / GO.X0[L] - 1)) for L in (100, 200, 300, 400)]; e6b = max(abs(r["rel"]) for r in rows6b)
Rz = 1 + 0.1 * np.exp(-GO.zg) + 0.02 * np.sin(GO.zg)
tab = np.repeat((Rz ** 2)[None, :], len(GL.KGRID), axis=0)
S1 = GO.S_of_z(Rz); S2 = GO.S_of_kz(GO.ratio_interp(tab, GO.zg)); e6c = float(np.max(np.abs(S1 - S2)))
ok6 = bool(e6a <= 1e-10 and e6b <= 0.02 and e6c <= 1e-10)
RES["KA"]["KA6"] = dict(a=e6a, b=rows6b, c=e6c, pass_=ok6)
P(f"KA6 Limber: (a) constant R: {e6a:.1e}; (b) absolute X_L vs CLASS X0: " + ", ".join(f"L {r['L']} {r['rel']:+.4f}" for r in rows6b)
  + f"; (c) z-only vs k-code: {e6c:.1e} -> {'PASS' if ok6 else 'FAIL'}")

allok = all(v["pass_"] for v in RES["KA"].values())
allok_frozen = all(v.get("pass_frozen", v["pass_"]) for v in RES["KA"].values())
RES["all_pass"] = allok; RES["all_pass_as_frozen"] = allok_frozen
P(f"As frozen (before A1): all pass {allok_frozen}  -> {'NO VERDICT as frozen' if not allok_frozen else 'ok'}")
P(f"Known answers all pass under A1: {allok}   ({time.time() - T0:.0f} s)")
P(GO.kappa_note)
json.dump(RES, open(os.path.join(HERE, "grw1_ka.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "grw1_ka.out"), "w").write("\n".join(OUT) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
