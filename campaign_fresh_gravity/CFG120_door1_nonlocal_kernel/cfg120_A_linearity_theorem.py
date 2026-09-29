#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG120 script A -- T0 (reproduction/controls), T1a-d (the linearity theorem and the point-mass minimax), T1g (Rahvar-Mashhoon-type
kernels, best case), and the fixed-shape scaling check.  Written to CFG120_FROZEN_CRITERIA.md (commit e8b9fbcdf); no criterion changed.

Claims (CHECKS) are the pre-declared expectations "the obstruction holds"; a FAIL of a check = an expectation that turned out false
(kept, exit 1).  GATE rows are the door's verdicts (do not set the exit code).
MUTATE=a : kernel made mass-dependent (K_M with rM from each mass)  -> the universality claims must FAIL.
MUTATE=b : target made degree 2 in the baryon mass (C' = C_target * M/1e10) -> the scaling / minimax claims must FAIL.
MUTATE=c, d : no bite in this script (declared).
Run: python3 cfg120_A_linearity_theorem.py     (MUTATE=a|b for the controls)
"""
import os, sys, math, json
import numpy as np
import sympy as sp
from scipy.integrate import quad

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg120_common import *

R = Report("cfg120_A_linearity_theorem")
P, check = R.P, R.check
R.head(__doc__.split("Run: python3")[0])
M_REF = 1e10
TSCALE = (lambda M: M / M_REF) if MUTATE == "b" else None
if MUTATE in ("c", "d"):
    P(f"\n  MUTATE={MUTATE}: no bite in script A (declared); main claims are evaluated unchanged.")

# =================================================================================================================== T0
R.banner("T0  reproduction and controls (implementation checks, tolerances declared here)")
# (1) point-mass target: own ODE vs closed form
a0 = A0
Mpt = 1e10
r_M = rM(Mpt, a0)
rr, MD = target_MD_ode(lambda r: Mpt, a0, 1e-3 * r_M, 40 * r_M)
x = rr / r_M
sel = (x >= 0.1) & (x <= 30)
err = np.max(np.abs(MD[sel] / (Mpt * (np.sqrt(1 + x[sel] ** 2) - 1)) - 1))
check("T0.1 point-mass target: ODE dM_D/dr = (a0/G) r M/(M+M_D) reproduces M_D = M(sqrt(1+x^2)-1)", f"max rel err on x in [0.1,30] = {err:.2e} (line 1e-8)", err < 1e-8)
# (2) extended target vs CFG44 Bcommon (read-only)
h0 = 2.0
prof = Bc.exp_sphere(1e10, h0)
rg, w, u, uN = Bc.cold_mass(prof, "encl", a0=a0)
x2 = rg / rM(1e10, a0)
s2 = (x2 >= 0.1) & (x2 <= 30)
rr2, MD2 = target_MD_ode(lambda r: float(Mb_exp(1e10, h0, r)), a0, rg[0], rg[-1], n=len(rg))
e2 = np.max(np.abs(MD2[s2] / (w[s2] / G) - 1))
check("T0.2 extended target (exponential sphere M=1e10, h=2 kpc, Bcommon default) matches CFG44's Bcommon.cold_mass('encl')", f"max rel err on x in [0.1,30] = {e2:.2e} (line 1e-6)", e2 < 1e-6)
# (3) FT of K_M
zs = [0.1, 1.0, 3.0]
e3 = max(abs(F_struve(z) / F_fourier_quad(z) - 1) for z in zs)
zh = [30.0, 100.0]
e3b = max(abs(F_struve(z) / ((1 / z ** 2) * (1 + 1 / z ** 2 + 9 / z ** 4 + 225 / z ** 6)) - 1) for z in zh)
check("T0.3 F(z) = (pi/2z)[I0(z)-L0(z)] equals the defining sine integral (z=0.1,1,3) and its asymptotic series (z=30,100)", f"max rel err {e3:.2e} (line 1e-6) and {e3b:.2e} (line 1e-6)", e3 < 1e-6 and e3b < 1e-6)
# (4) positive control: K_M reproduces the target with R = 1 (harness can pass)
kM = KM(r_M)
Rk = R_point(kM, r_M * XGRID, Mpt, a0)
check("T0.4 POSITIVE CONTROL: K_M reproduces C_target with R = 1 at its own mass", f"max |R-1| = {np.max(np.abs(Rk - 1)):.2e} (line 1e-8)", np.max(np.abs(Rk - 1)) < 1e-8)
# (5) convolution machinery: a tiny exponential sphere must reproduce the point-mass enclosed dark mass m(r)
hh = 1e-3
errs = []
for kern, lab in ((KM(r_M), "K_M"), (RM(1.0, 3.0, 0.1), "RM(1,3,0.1)")):
    rgrid = sphere_grid(hh, rMv=r_M)
    rhoD = rhoD_sphere(kern, exp_rho(Mpt, hh), rgrid, 60 * hh)
    MDn = cum_mass(rgrid, rhoD)
    sel5 = rgrid > 30 * hh
    errs.append((lab, float(np.max(np.abs(MDn[sel5] / (Mpt * kern.m(rgrid[sel5])) - 1)))))
check("T0.5 spherical-convolution formula: an exponential sphere with h = 1e-3 kpc reproduces the point-mass dark mass M m(r)", "max rel err " + ", ".join(f"{l}: {e:.2e}" for l, e in errs) + " (declared line 5e-3)", all(e < 5e-3 for _, e in errs))

# =================================================================================================================== T1a
R.banner("T1a  the scaling theorem (sympy) and the target's density exponent")
lam, r_, Ga, a0s, f, g, b = sp.symbols("lambda r G a0 f g b", positive=True)
# rho_D = lam f, M_D = lam g, M_b = lam b  (LTI kernel, fixed constants); C_model = G r rho_D (M_b + M_D); C_target = (a0/4pi) M_b
Cmod = Ga * r_ * (lam * f) * (lam * b + lam * g)
Ctar = a0s / (4 * sp.pi) * (lam * b)
ratio = sp.simplify((Cmod / Ctar) / ((Cmod / Ctar).subs(lam, 1)))
check("T1a.1 (sympy) any LTI kernel: [C_model/C_target](lambda rho_b) / [C_model/C_target](rho_b) = lambda  (C_model ~ lambda^2, C_target ~ lambda)", f"ratio = {ratio}", sp.simplify(ratio - lam) == 0)
xs, Ms, a0_, G_ = sp.symbols("x M a0 G", positive=True)
rM_s = sp.sqrt(G_ * Ms / a0_)
rr_s = sp.symbols("rr", positive=True)
rho_t = a0_ / (4 * sp.pi * G_ * rr_s * sp.sqrt(1 + rr_s ** 2 / rM_s ** 2))
expo = sp.simplify(sp.diff(sp.log(rho_t), Ms) * Ms)
xexpr = rr_s / rM_s
expo_x = sp.simplify(expo.subs(rr_s, xs * rM_s))
check("T1a.2 (sympy) target density exponent d ln rho_c/d ln M at fixed r = x^2/(2(1+x^2))", f"= {expo_x}", sp.simplify(expo_x - xs ** 2 / (2 * (1 + xs ** 2))) == 0)
ex = lambda xv: xv ** 2 / (2 * (1 + xv ** 2))
P(f"  exponent at x = 0.1: {ex(0.1):.4f};  x = 1: {ex(1):.4f};  x = 30: {ex(30):.4f};  sup over x: 1/2 (linear kernel: exactly 1)")
# numeric finite difference of the exponent
eM = 1e-5
fd = []
for xv in (0.1, 1.0, 30.0):
    rv = xv * rM(1e10, a0)
    fdv = (math.log(a0 / (4 * math.pi * G * rv * math.sqrt(1 + rv ** 2 * a0 / (G * 1e10 * (1 + eM)))))
           - math.log(a0 / (4 * math.pi * G * rv * math.sqrt(1 + rv ** 2 * a0 / (G * 1e10 * (1 - eM)))))) / (2 * eM)
    fd.append(abs(fdv - ex(xv)))
check("T1a.3 numeric finite-difference exponent agrees with x^2/(2(1+x^2))", f"max abs diff {max(fd):.2e} (line 1e-6)", max(fd) < 1e-6)

# =================================================================================================================== T1b
R.banner("T1b  the required kernel K_M: closed form, Fourier transform, asymptotics, mass dependence")
P("  K_M(r) = 1/[4 pi rM r sqrt(r^2+rM^2)],  rM = sqrt(G M/a0);  Khat_M(k) = F(k rM),  F(z) = (pi/2z)[I0(z) - L0(z)]")
for z in (0.01, 0.1, 1.0, 10.0, 100.0):
    P(f"    F({z:g}) = {F_struve(z):.6e};  small-z pi/(2z) = {math.pi / (2 * z):.4e};  large-z 1/z^2 = {1 / z ** 2:.4e}")
k1, k2 = KM(rM(1e9, a0)), KM(rM(1e12, a0))
sv = np.array([0.5, 5.0, 20.0])
diffr = np.abs(k1.K(sv) / k2.K(sv) - 1)
check("T1b.1 K_M depends on the mass (rM ~ M^(1/2)): K_M(1e9) and K_M(1e12) differ at every tested radius", f"K_M(1e9)/K_M(1e12) at r = 0.5, 5, 20 kpc: {np.round(k1.K(sv) / k2.K(sv), 3)}; rM = {rM(1e9, a0):.3f}, {rM(1e12, a0):.3f} kpc", np.all(diffr > 0.1))
Ldum = a0  # keep linter quiet
tail = [(0.3 * rM(1e10, a0), None)]
P(f"  tail check: K_M/(1/(4 pi rM s^2)) = s/sqrt(s^2+rM^2) = 1/sqrt(1+1/x^2): x=3 -> {1 / math.sqrt(1 + 1 / 9):.4f}, x=10 -> {1 / math.sqrt(1 + 1 / 100):.4f}")
Mlam = {lm: a0 * lm ** 2 / G for lm in (3.0, 10.0)}
P(f"  M_lambda = a0 lambda0^2 / G  (mass at which a fixed lambda0 matches the K_M tail): lambda0 = 3 kpc -> {Mlam[3.0]:.3e} Msun; 10 kpc -> {Mlam[10.0]:.3e} Msun  [ESTIMATE in frozen file: 6.0e9, 6.7e10]")
check("T1b.2 the frozen estimates M_lambda = 6.0e9 and 6.7e10 Msun hold", f"{Mlam[3.0]:.3e}, {Mlam[10.0]:.3e}", abs(Mlam[3.0] / 6.0e9 - 1) < 0.02 and abs(Mlam[10.0] / 6.7e10 - 1) < 0.02, load_bearing=False)

# =================================================================================================================== T1c-d
R.banner("T1c-d  point mass: the best a universal kernel can do (exact pointwise minimax over the 13 masses)")
rgrid = np.geomspace(1e-2, 2e3, 6000)
res = {}
for foot, a0f in FOOTINGS.items():
    if MUTATE == "a":
        # mass-dependent kernel: every mass gets its own K_M, so R_i = R_point(K_M,i) (= 1); the "best universal" residual is then max |ln R|
        worst_ln = 0.0
        for M in MASSES:
            rv = rM(M, a0f) * XGRID
            Rv = R_point(KM(rM(M, a0f)), rv, M, a0f)
            worst_ln = max(worst_ln, float(np.max(np.abs(np.log(Rv)))))
        res[foot] = dict(worst_fac=math.exp(worst_ln), span=1.0, overlap=(float("nan"), float("nan")), lin_dev=math.exp(worst_ln) - 1)
        P(f"  [{foot}] MUTATE=a per-mass K_M: worst |ln R| over all masses and x = {worst_ln:.2e}")
        continue
    fac, lnB, cnt, mlo, mhi = minimax_universal(rgrid, MASSES, a0f, TSCALE)
    ok = np.isfinite(fac)
    both = (cnt >= 2) & (mlo == MASSES[0]) & (mhi == MASSES[-1])
    # span (max c / min c) per r and the linear-band minimax deviation (cmax-cmin)/(cmax+cmin)
    span = fac ** 2
    lin = (span - 1) / (span + 1)
    ov = rgrid[both]
    res[foot] = dict(worst_fac=float(np.nanmax(fac)), span=float(np.nanmax(span)), overlap=(float(ov.min()) if ov.size else float("nan"), float(ov.max()) if ov.size else float("nan")),
                     lin_dev=float(np.nanmax(lin)), fac_in_overlap=(float(np.nanmin(fac[both])), float(np.nanmax(fac[both]))) if ov.size else None,
                     r_worst=float(rgrid[np.nanargmax(fac)]))
    P(f"  [{foot}] r range where both 1e9 and 1e12 constrain r: {res[foot]['overlap'][0]:.3f} .. {res[foot]['overlap'][1]:.3f} kpc  (r_M(1e12)*0.1, r_M(1e9)*30)")
    P(f"          ln-centred minimax factor over r: worst {res[foot]['worst_fac']:.4f} (overlap: {res[foot]['fac_in_overlap']}), i.e. R spans 1/f .. f;  sqrt(1000) = {math.sqrt(1000):.4f}")
    P(f"          linear-band minimax deviation max|R-1| (best B per r): worst {res[foot]['lin_dev']:.5f}  (frozen line 0.10)")
    R.num(f"minimax_{foot}", res[foot])
rc = res["canonical"]
main_expect = math.sqrt(1000.0)
if MUTATE != "a":
    check("T1c.1 the best universal kernel leaves a centred residual factor sqrt(M_hi/M_lo) = sqrt(1000) = 31.62 on the overlap (frozen ESTIMATE), both footings",
          "canonical " + ", ".join(f"{k}: {v['worst_fac']:.4f}" for k, v in res.items()) + f" (overlap range {rc['overlap'][0]:.2f}-{rc['overlap'][1]:.2f} kpc)",
          all(abs(v["worst_fac"] / main_expect - 1) < 1e-9 for v in res.values()))
    check("T1c.2 no universal kernel meets the 10 percent line at every r (G1 point mass FAILS)", f"linear-band minimax deviation {rc['lin_dev']:.4f} >> 0.10; ln-centred factor {rc['worst_fac']:.3f}", rc["lin_dev"] > 0.10)
else:
    check("T1c.1 the best universal kernel leaves a centred residual factor sqrt(1000) = 31.62 on the overlap", f"mutated: per-mass K_M gives worst factor {res['canonical']['worst_fac']:.6f}", abs(res["canonical"]["worst_fac"] / main_expect - 1) < 1e-9)
    check("T1c.2 no universal kernel meets the 10 percent line at every r (G1 point mass FAILS)", f"mutated: worst |R-1| {res['canonical']['lin_dev']:.2e}", res["canonical"]["lin_dev"] > 0.10)

# window: largest mass ratio f for which ONE kernel keeps all R in [0.9, 1.1] over both masses' full x-ranges
def window(M1, a0f):
    fs = np.geomspace(1.0001, 1e3, 4000)
    best = 1.0
    for fval in fs:
        M2 = M1 * fval
        rl, rh = max(0.1 * rM(M1, a0f), 0.1 * rM(M2, a0f)), min(30 * rM(M1, a0f), 30 * rM(M2, a0f))
        if rl >= rh:
            best = fval
            continue
        rr_ = np.geomspace(rl, rh, 50)
        cs = np.array([4 * math.pi * rM(Mx, a0f) ** 2 / (1.0 if TSCALE is None else TSCALE(Mx)) for Mx in (M1, M2)])
        spanv = cs.max() / cs.min()
        if MUTATE == "a":
            spanv = 1.0
        if spanv <= BAND[1] / BAND[0] + 1e-12:
            best = fval
        else:
            break
    return best


wins = {foot: [window(M1, a0f) for M1 in (1e9, 1e10, 1e11)] for foot, a0f in FOOTINGS.items()}
P(f"  largest single-kernel mass window (all R in [0.9,1.1] over both masses' full x-range): {wins}   (analytic 1.1/0.9 = {1.1 / 0.9:.4f}; pass line >= 1e3)")
check("T1c.3 a single kernel passes the 10 percent line only over a mass factor <= 1.1/0.9 = 1.222 (frozen: 'about 1.22'); the pass line is >= 1e3", f"windows {wins}", all(abs(w_ - 1.1 / 0.9) < 2e-3 for ws in wins.values() for w_ in ws) if MUTATE == "" or MUTATE in ("c", "d") else all(w_ < 1e3 * 0.99 for ws in wins.values() for w_ in ws))
# M vs 2M
rr_ = np.geomspace(2.0, 30.0, 40)
testk = [RM(1.0, 3.0, 0.1), RM(2.0, 10.0, 0.06), RM(0.5, 1.0, 0.5), build_Kstar(a0, MASSES, TSCALE)[0]]
rat = []
for kern in testk:
    for r0_ in rr_:
        Mbase = 3e10
        Rm1 = R_point(kern, np.array([r0_]), Mbase, a0)[0] / (1.0 if TSCALE is None else TSCALE(Mbase))
        Rm2 = R_point(kern, np.array([r0_]), 2 * Mbase, a0)[0] / (1.0 if TSCALE is None else TSCALE(2 * Mbase))
        if MUTATE == "a":
            Rm1 = R_point(KM(rM(Mbase, a0)), np.array([r0_]), Mbase, a0)[0]
            Rm2 = R_point(KM(rM(2 * Mbase, a0)), np.array([r0_]), 2 * Mbase, a0)[0]
        rat.append(Rm2 / Rm1)
rat = np.array(rat)
P(f"  R(2M)/R(M) at fixed r for 4 universal kernels x 40 radii: min {rat.min():.12f}, max {rat.max():.12f}  (LTI theorem: exactly 2; certificate: best centred residual sqrt2-1 = {math.sqrt(2) - 1:.4f}, linear-band 1/3)")
check("T1c.4 M versus 2M: C_model(2M)/C_model(M)-ratio = 2 for every LTI kernel, so no kernel serves both within 10 percent (best centred residual 41%)", f"ratio range [{rat.min():.10f}, {rat.max():.10f}]", np.all(np.abs(rat - 2.0) < 1e-9))
# universal kernel K*: direct numerical route agrees with 4 pi rM^2 B*
if MUTATE != "a":
    Ks, Bs, rs = build_Kstar(a0, MASSES, TSCALE)
    mx = 0.0
    lnR = 0.0
    for M in MASSES:
        rv = rM(M, a0) * XGRID
        Rd = R_point(Ks, rv, M, a0) / (1.0 if TSCALE is None else TSCALE(M))
        Rf = 4 * math.pi * rM(M, a0) ** 2 * np.interp(np.log(rv), np.log(rs), Bs) / (1.0 if TSCALE is None else TSCALE(M))
        mx = max(mx, float(np.max(np.abs(Rd / Rf - 1))))
        lnR = max(lnR, float(np.max(np.abs(np.log(Rd)))))
    check("T1c.5 the constructed universal kernel K* (B* -> K) realises R = 4 pi rM^2 B*, direct numerical route vs formula", f"max rel diff {mx:.2e} (line 2e-3); its worst |ln R| over the whole G1 domain = {lnR:.4f} (sqrt(1000) -> {math.log(math.sqrt(1000)):.4f} for the ln-centred K*)", mx < 2e-3)
    P("  note (disclosed, not a repair): the grid-built K* has worst |ln R| = %.3f, above the pointwise-minimax value %.3f, because B* jumps at the radii where a mass enters or leaves its x-range and the 6000-point grid interpolates across each jump; the pointwise minimax value (T1c.1, exact) is the certificate, K* is only its constructive check." % (lnR, math.log(math.sqrt(1000))))
    R.num("Kstar_worst_lnR", lnR)

# =================================================================================================================== fixed-shape scaling (numeric convolution)
R.banner("Fixed-shape scaling on exponential spheres: R(M) / R(M') = M / M' at fixed r and fixed h (numerical convolution)")
hfix = 2.0
rgfix = np.geomspace(0.3, 60.0, 60)
Rm = {}
for M in (1e9, 1e10, 1e11):
    kern = KM(rM(M, a0)) if MUTATE == "a" else RM(1.0, 3.0, 0.1)
    _, Rv, _, _, _ = C_ratio_sphere(kern, M, hfix, a0, rgrid=rgfix)
    Rm[M] = Rv / (1.0 if TSCALE is None else TSCALE(M))
sl = [np.max(np.abs((Rm[1e10] / Rm[1e9]) / 10.0 - 1)), np.max(np.abs((Rm[1e11] / Rm[1e10]) / 10.0 - 1))]
check("T1a.4 (numeric) at fixed exponential profile (h = 2 kpc) and fixed kernel, R scales exactly as M_b", f"max |R(10M)/R(M)/10 - 1| = {max(sl):.2e} (line 1e-6)", max(sl) < 1e-6)

# =================================================================================================================== T1g
R.banner("T1g  Rahvar-Mashhoon-type kernels K = A(1+mu s)exp(-mu s)/(4 pi lam s^2) [AS RECALLED], best case over the whole G1 domain")
rm_sets = [(3.0, 0.06), (3.0, 0.1), (10.0, 0.06), (10.0, 0.1)]
out_fits = {}
for foot, a0f in FOOTINGS.items():
    P(f"\n  --- footing {foot}: a0 = {a0f:.2f} (km/s)^2/kpc ---")
    rows = []
    for lam0, mu0 in rm_sets:
        kern = RM(1.0, lam0, mu0)
        per = []
        for M in MASSES:
            Rv = R_point(kern, rM(M, a0f) * XGRID, M, a0f) / (1.0 if TSCALE is None else TSCALE(M))
            per.append((float(Rv.min()), float(Rv.max()), float(np.max(np.abs(np.log(Rv))))))
        best_i = int(np.argmin([p[2] for p in per]))
        allpass = all(p[0] >= BAND[0] and p[1] <= BAND[1] for p in per)
        rows.append(dict(lam=lam0, mu=mu0, closest_mass=float(MASSES[best_i]), closest_maxabslnR=per[best_i][2], passes_all=allpass,
                         Rrange_per_mass=[(float(M), p[0], p[1]) for M, p in zip(MASSES, per)]))
        P(f"    recalled set lambda0={lam0:g} kpc, mu0={mu0:g}/kpc, A=1: closest to target at M = {MASSES[best_i]:.2e} (max|ln R| = {per[best_i][2]:.3f}); R range at 1e9: [{per[0][0]:.3g}, {per[0][1]:.3g}], 1e12: [{per[-1][0]:.3g}, {per[-1][1]:.3g}]; passes all masses: {allpass}")
    out_fits[foot] = dict(recalled=rows)
    if MUTATE == "a":
        P("    MUTATE=a: fits not meaningful for a mass-dependent kernel (skipped, declared)")
        continue
    f3 = fit_rm(a0f, MASSES, None, TSCALE)
    f2 = fit_rm(a0f, MASSES, 1.0, TSCALE)
    out_fits[foot]["fit3"], out_fits[foot]["fit2"] = f3, f2
    for tag, ff in (("3-param (A, lam, mu)", f3), ("2-param (lam, mu), A = 1", f2)):
        kern = RM(ff["A"], ff["lam"], ff["mu"])
        per = [R_point(kern, rM(M, a0f) * XGRID, M, a0f) / (1.0 if TSCALE is None else TSCALE(M)) for M in MASSES]
        dev = max(float(np.max(np.abs(p - 1))) for p in per)
        P(f"    best {tag}: A={ff['A']:.4g}, lambda0={ff['lam']:.4g} kpc, mu0={ff['mu']:.4g}/kpc  -> max|ln R| = {ff['max_abs_lnR']:.4f} (factor {math.exp(ff['max_abs_lnR']):.3f}); max|R-1| over the domain = {dev:.3f}; total integral 2A/(lam mu) = {kern.total():.3f}")
    json.dump(out_fits[foot], open(os.path.join(HERE, f"cfg120_rmfit{'_MUTATE_' + MUTATE if MUTATE else ''}_{foot}.json"), "w"), indent=1)
    R.num(f"rmfit_{foot}", out_fits[foot])
if MUTATE != "a":
    f3c = out_fits["canonical"]["fit3"]
    f2c = out_fits["canonical"]["fit2"]
    check("T1g.1 best-case Rahvar-Mashhoon-type kernel (3-parameter) cannot meet the 10 percent line over 1e9-1e12 (max|R-1| > 0.10 and max|ln R| >= ln 31.6)",
          f"canonical: 3-param max|ln R| = {f3c['max_abs_lnR']:.4f} (>= {math.log(math.sqrt(1000)):.4f}: {f3c['max_abs_lnR'] >= math.log(math.sqrt(1000)) - 1e-3}), 2-param {f2c['max_abs_lnR']:.4f}",
          f3c["max_abs_lnR"] >= math.log(math.sqrt(1000)) - 1e-3 if MUTATE == "" else f3c["max_abs_lnR"] > math.log(1.10))
    check("T1g.2 none of the four recalled parameter sets passes at every mass", "passes: " + str([r["passes_all"] for r in out_fits["canonical"]["recalled"]]), not any(r["passes_all"] for r in out_fits["canonical"]["recalled"]))

# =================================================================================================================== G1 gate row
R.banner("GATE ROW (G1, point mass; extended baryons are in script B)")
if MUTATE == "":
    R.gate("G1(point mass, fixed linear kernel)", "FAIL", f"R = C_model/C_target proportional to M_b exactly; best universal kernel leaves ln-centred factor {rc['worst_fac']:.2f} (R spans {1 / rc['worst_fac']:.3f}..{rc['worst_fac']:.2f}), linear-band deviation {rc['lin_dev']:.3f}; single-kernel mass window {wins['canonical'][0]:.3f} vs 1e3 required")
else:
    R.gate("G1(point mass) under MUTATE=" + MUTATE, "not a door verdict", "control run")
nf = R.write()
sys.exit(1 if nf else 0)
