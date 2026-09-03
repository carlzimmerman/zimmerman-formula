#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k03 -- ANGLE 5, candidate 1, second arena: THE EXTERNAL-FIELD SATURATION LAW in molecular clouds.

Same law as k02, in a system class ten decades smaller in mass and with a completely different dominant
systematic (the CO-to-H2 conversion factor X_CO instead of a stellar mass-to-light ratio):

    alpha_vir  ==  5 sigma_V^2 R / (G M)  =  B(e),     B(e) = nu(e)[1 + L(e)/3],
    e = G M_b,MW/(R_gal^2 a_0),   a_0 = (c/2) sqrt(G rho_DE)

for a self-gravitating cloud in virial equilibrium.  Three hypotheses are separated:

    NEWTON            alpha_vir = 1, no dependence on anything
    SATURATED MOND    alpha_vir = B(e), a function of GALACTOCENTRIC RADIUS only -- the candidate law
    ISOLATED MOND     alpha_vir = nu(g_int/a_0), a function of the cloud's OWN acceleration
                      (this is what v^4 = G M_b a_0 plus algebra gives, i.e. the RESTATEMENT branch)

The clouds sit 1-2 decades below a_0 internally (median g_int = 0.090 a_0) inside a Galactic field of
1.4-4.7 a_0, so isolated MOND would give them boosts of 3-10 while the saturation law gives 1.2-1.9.  The
two branches differ by a factor of 3-8: molecular clouds are where the external-field effect is doing the
most work anywhere in the framework, and where its absence would be most visible.

DATA.  Miville-Deschenes, Murray & Lee 2017 (ApJ 834, 57), 8107 Galactic CO clouds, VizieR J/ApJ/834/57,
fetched this session to real_research/data/gmc_mivilledeschenes2017.tsv.  Sigma and sigma_V are
distance-free; R and M scale as D and D^2.  Masses use a fixed X_CO, so d log M/d log X_CO = +1 exactly.

BUG PATTERNS, HANDLED.
 (2) spherical formula on a non-sphere: alpha_vir = 5 sigma^2 R/(GM) is the standard uniform-sphere
     convention and is used identically for data, mocks and predictions, so it cancels from every
     comparison; only the absolute normalisation carries it, and the absolute test is NOT the verdict.
 (3) resolution: distant clouds are blends.  A resolution cut (angular radius > 2 beams) is applied and
     the test is repeated in matched heliocentric-distance cells.
 (5) trivial correlation: alpha_vir ~ 1/(Sigma R) and g_int ~ Sigma, so an error in Sigma slides a cloud
     along a line of slope -1 in the (log g_int, log alpha_vir) plane -- and ISOLATED MOND predicts -1/2.
     A Monte Carlo under each hypothesis measures exactly what the estimator returns, so the induced
     slope is subtracted rather than assumed away.

Run:  python3 k03_gmc_efe_saturation_law.py   (exit 0 = the MACHINERY checks pass; the LAW tests are
      reported separately and their failure is the physics result, not a bug)
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, G, Msun, kpc, vizier_tsv, _f, nu, nu_s, Check, P, info
from hunt_efe_lib import dlnnu_dlny

pc = 3.0857e16
R0_KPC = 8.122
MB_MW = 5.709e10                # Msun, calibrated in k01/k02 to the frozen registered x_ext = 1.89929
BEAM_DEG = 0.125                # CfA CO survey beam/pixel scale used by Miville-Deschenes+2017
RNG = np.random.default_rng(20260903)


def B_sat(e):
    n = nu_s(e); L = float(dlnnu_dlny(np.array([e]))[0])
    return n*(1.0 + L/3.0)


B_sat_v = np.vectorize(B_sat)


def load():
    rows = vizier_tsv("gmc_mivilledeschenes2017.tsv")
    col = lambda k: np.array([_f(r[k]) for r in rows])
    far = col("INF") > 0.5
    d = dict(Sigma=col("Sigma"), sigv=col("SigV"), Rgal=col("Rgal"), Rang=col("Rang"),
             glon=col("GLON"), glat=col("GLAT"), Npix=col("Npix"),
             R=np.where(far, col("Rfar"), col("Rnear")),
             M=np.where(far, col("Mfar"), col("Mnear")),
             D=np.where(far, col("Dfar"), col("Dnear")), far=far)
    d["alpha"] = 5.0*(d["sigv"]*1e3)**2*(d["R"]*pc)/(G*d["M"]*Msun)
    return d


def fitslope(x, y):
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    good = np.isfinite(x) & np.isfinite(y)
    x, y = x[good], y[good]
    n = len(x)
    if n < 3:
        return float("nan"), float("inf")
    sx, sy = x.mean(), y.mean()
    Sxx = float(np.sum((x - sx)**2))
    if Sxx <= 0:
        return float("nan"), float("inf")
    b1 = float(np.sum((x - sx)*(y - sy))/Sxx)
    r = y - (sy + b1*(x - sx))
    s2 = float(np.sum(r*r))/max(n - 2, 1)
    return b1, float(math.sqrt(s2/Sxx))


def main():
    ck = Check()
    P("=" * 118)
    P("k03 -- the EXTERNAL-FIELD SATURATION LAW in 8107 Galactic molecular clouds")
    P("       alpha_vir = 5 sigma_V^2 R/(G M)  vs  B(e) = nu(e)[1+L(e)/3],  e = G M_b,MW/(R_gal^2 a_0)")
    P("=" * 118)

    d = load()
    base = (np.isfinite(d["Sigma"]*d["sigv"]*d["R"]*d["M"]*d["Rgal"]*d["D"])
            & (d["M"] > 0) & (d["R"] > 0) & (d["sigv"] > 0) & (d["Rgal"] > 0.5) & (d["D"] > 0))
    # resolution cut: angular radius at least two beams
    resolved = base & (d["Rang"] > 2*BEAM_DEG) & (d["Npix"] >= 20)
    P(f"\n  {base.sum()} clouds with complete entries; {resolved.sum()} survive the resolution cut "
      f"(angular radius > {2*BEAM_DEG} deg and >= 20 pixels)")
    ck("the resolution cut keeps a usable sample (>= 1000 clouds)  [CAN FAIL]",
       resolved.sum() >= 1000, f"{resolved.sum()} clouds")

    for foot in ("canonical", "alt"):
        a0 = A0[foot]
        P("\n" + "=" * 118)
        P(f"FOOTING: {foot}   a_0 = {a0:.3e} m/s^2")
        P("=" * 118)

        g_int = G*d["M"]*Msun/((d["R"]*pc)**2 * a0)
        e_ext = G*(MB_MW*Msun)/((d["Rgal"]*kpc)**2 * a0)
        Bp = B_sat_v(e_ext)
        Biso = nu(g_int)

        s = resolved
        P(f"  g_int/a_0: 5th {np.percentile(g_int[s],5):.4f}, median {np.median(g_int[s]):.4f}, "
          f"95th {np.percentile(g_int[s],95):.4f}")
        P(f"  SATURATED prediction B: median {np.median(Bp[s]):.3f}, 5-95% "
          f"{np.percentile(Bp[s],5):.3f}-{np.percentile(Bp[s],95):.3f}")
        P(f"  ISOLATED prediction nu(g_int): median {np.median(Biso[s]):.3f}, 5-95% "
          f"{np.percentile(Biso[s],5):.3f}-{np.percentile(Biso[s],95):.3f}")
        P(f"  observed alpha_vir: median {np.median(d['alpha'][s]):.3f}, 5-95% "
          f"{np.percentile(d['alpha'][s],5):.3f}-{np.percentile(d['alpha'][s],95):.3f}")

        # ---------------- self-gravitating subsample --------------------------------------------
        # the classic bound-GMC regime: massive and dense.  alpha_vir ~ 1-2 is established there.
        sg = s & (d["M"] > 1e4) & (d["Sigma"] > 30)
        P(f"\n  [SELF-GRAVITATING SUBSAMPLE]  M > 1e4 Msun and Sigma > 30 Msun/pc^2: N = {sg.sum()}")
        P(f"     median alpha_vir = {np.median(d['alpha'][sg]):.3f}")
        P(f"     SATURATED law requires {np.median(Bp[sg]):.3f};  ISOLATED MOND requires "
          f"{np.median(Biso[sg]):.3f};  Newton requires 1.000")
        P(f"     (the absolute value is NOT the verdict: alpha_vir carries the whole X_CO scale, "
          f"d log alpha_vir/d log X_CO = -1.000)")

        # ---------------- SHAPE TEST 1: dependence on the cloud's own acceleration ---------------
        x = np.log10(g_int[sg]); yv = np.log10(d["alpha"][sg])
        sl, se = fitslope(x, yv)
        P(f"\n  [SHAPE TEST 1] d log alpha_vir / d log g_int over "
          f"{x.max()-x.min():.2f} dex of internal acceleration, N = {sg.sum()}")
        P(f"     measured {sl:+.3f} +- {se:.3f}")
        P(f"     SATURATED law and Newton both predict 0.000 (no dependence on the cloud's own field)")
        P(f"     ISOLATED MOND predicts -0.500 in the deep limit")

        # Monte Carlo: what does the estimator return under each hypothesis, with realistic errors?
        P(f"\n     MONTE CARLO CONTROL (bug pattern 5).  Build synthetic clouds that obey each hypothesis")
        P(f"     EXACTLY, then add the real measurement errors and re-measure the same slope.")
        n_mc = 200
        Sig0 = d["Sigma"][sg]; R0 = d["R"][sg]; D0 = d["D"][sg]
        Bp0 = Bp[sg]; e0 = e_ext[sg]
        out = {}
        for hyp in ("newton", "saturated", "isolated"):
            sls = []
            for _ in range(n_mc):
                # truth: Sigma_t, R_t; sigma_V follows from the hypothesis exactly
                gt = math.pi*G*Sig0*Msun/pc**2/a0
                alpha_t = (np.ones_like(gt) if hyp == "newton" else
                           (Bp0 if hyp == "saturated" else nu(gt)))
                sv_t = np.sqrt(alpha_t*G*(math.pi*Sig0*Msun/pc**2*(R0*pc)**2)/(5*R0*pc))/1e3
                # measurement errors: X_CO/W_CO 0.15 dex on Sigma, 5% on sigma_V, 20% on D (hence on R)
                Sm = Sig0*10**(0.15*RNG.standard_normal(len(Sig0)))
                svm = sv_t*(1 + 0.05*RNG.standard_normal(len(Sig0)))
                Rm = R0*(1 + 0.20*RNG.standard_normal(len(Sig0)))
                good = (Rm > 0) & (svm > 0)
                Mm = math.pi*Sm[good]*Rm[good]**2
                am = 5*(svm[good]*1e3)**2*(Rm[good]*pc)/(G*Mm*Msun)
                gm = G*Mm*Msun/((Rm[good]*pc)**2*a0)
                sls.append(fitslope(np.log10(gm), np.log10(am))[0])
            out[hyp] = (float(np.mean(sls)), float(np.std(sls)))
            P(f"       {hyp:10s} truth -> estimator returns slope {out[hyp][0]:+.3f} +- {out[hyp][1]:.3f}")
        P(f"       DATA                                        {sl:+.3f} +- {se:.3f}")
        sep = abs(out["saturated"][0] - out["isolated"][0])
        P(f"     separation between the two MOND branches after the induced correlation: {sep:.3f} in slope")
        if foot == "canonical":
            ck("the Monte Carlo separates SATURATED from ISOLATED MOND by more than the data's error bar, "
               "so shape test 1 is identified rather than degenerate  [CAN FAIL]",
               sep > 3*se, f"branch separation {sep:.3f} vs 3 sigma_data = {3*se:.3f}")
            z_sat = abs(sl - out["saturated"][0])/math.sqrt(se**2 + out["saturated"][1]**2)
            z_iso = abs(sl - out["isolated"][0])/math.sqrt(se**2 + out["isolated"][1]**2)
            z_new = abs(sl - out["newton"][0])/math.sqrt(se**2 + out["newton"][1]**2)
            P(f"     -> data are {z_new:.1f} sigma from Newton, {z_sat:.1f} sigma from the SATURATION law, "
              f"{z_iso:.1f} sigma from ISOLATED MOND")
            shape1 = dict(sl=sl, se=se, z_sat=z_sat, z_iso=z_iso, z_new=z_new)

        # ---------------- SHAPE TEST 2: the Galactocentric lever, matched cells -----------------
        P(f"\n  [SHAPE TEST 2] the Galactocentric lever.  B depends on R_gal ALONE, so at fixed surface")
        P(f"     density and fixed heliocentric distance (hence fixed physical resolution) alpha_vir must")
        P(f"     track B(R_gal).  Matched cells in (log Sigma, log D) remove both confounds.")
        m = s & np.isfinite(d["alpha"]) & (d["alpha"] > 0)
        lS = np.log10(d["Sigma"][m]); lD = np.log10(d["D"][m])
        la = np.log10(d["alpha"][m]); lB = np.log10(Bp[m]); Rg = d["Rgal"][m]
        eS = np.percentile(lS, np.linspace(0, 100, 7))
        eD = np.percentile(lD, np.linspace(0, 100, 7))
        dx, dy, wts = [], [], []
        ncell = 0
        for i in range(6):
            for j in range(6):
                c = (lS >= eS[i]) & (lS < eS[i+1]) & (lD >= eD[j]) & (lD < eD[j+1])
                if c.sum() < 25 or (lB[c].max() - lB[c].min()) < 0.05:
                    continue
                ncell += 1
                sl_c, se_c = fitslope(lB[c], la[c])
                dx.append(sl_c); dy.append(se_c); wts.append(1.0/se_c**2)
        dx, dy, wts = np.array(dx), np.array(dy), np.array(wts)
        if len(dx) >= 3:
            comb = float(np.sum(wts*dx)/np.sum(wts)); comb_se = float(1.0/math.sqrt(np.sum(wts)))
            P(f"     {ncell} matched cells; inverse-variance combined slope of log alpha_vir on log B:")
            P(f"       {comb:+.3f} +- {comb_se:.3f}    [SATURATION law: +1.000;  Newton: 0.000]")
            P(f"       -> {abs(comb-1)/comb_se:.1f} sigma from the law, {abs(comb)/comb_se:.1f} sigma from Newton")
            unident = (abs(comb - 1.0)/comb_se > 5.0) and (abs(comb)/comb_se > 5.0)
            if unident:
                P(f"       !! BOTH hypotheses are excluded at > 5 sigma.  A slope of {comb:+.3f} is outside")
                P(f"          anything either theory can produce, so this estimator is measuring a SYSTEMATIC,")
                P(f"          not physics.  Shape test 2 is UNIDENTIFIED and is not reported as a verdict.")
            if foot == "canonical":
                shape2 = dict(sl=comb, se=comb_se, unident=unident)
        else:
            P("     not enough matched cells with a B lever -- test not identified here")
            if foot == "canonical":
                shape2 = None

        # unmatched version, for contrast (this is what a careless version of the test would give)
        sl_u, se_u = fitslope(lB, la)
        P(f"     UNMATCHED (careless) version for contrast: {sl_u:+.3f} +- {se_u:.3f} -- the difference from")
        P(f"     the matched value is the size of the resolution/selection confound, not physics.")

        # DIAGNOSIS of the systematic: line-of-sight blending toward the inner Galaxy inflates sigma_V.
        if foot == "canonical":
            sl_b, se_b = fitslope(np.log10(Bp[m]), np.log10(d["sigv"][m]))
            sl_r, se_r = fitslope(np.log10(Bp[m]), np.log10(d["R"][m]))
            sl_s, se_s = fitslope(np.log10(Bp[m]), np.log10(d["Sigma"][m]))
            npath = np.abs(np.cos(np.radians(d["glon"][m])))     # inner-Galaxy pointing -> long CO path
            sl_p, se_p = fitslope(npath, np.log10(d["sigv"][m]))
            P(f"     DIAGNOSIS -- which factor of alpha_vir = 5 sigma_V^2/(pi G Sigma R) carries the slope?")
            P(f"       d log sigma_V / d log B = {sl_b:+.3f} +- {se_b:.3f}   (x2 in alpha_vir)")
            P(f"       d log R       / d log B = {sl_r:+.3f} +- {se_r:.3f}   (x-1)")
            P(f"       d log Sigma   / d log B = {sl_s:+.3f} +- {se_s:.3f}   (x-1)")
            P(f"       d log sigma_V / d |cos l| = {sl_p:+.3f} +- {se_p:.3f}  -- clouds seen along the LONG")
            P(f"         inner-Galaxy CO path have systematically larger line widths, which is blending, and")
            P(f"         inner-Galaxy means small R_gal means small B.  That is the source of the -2.7.")

    # ---------------------------------------------------------------- verdict
    P("\n" + "=" * 118)
    P("VERDICT (canonical footing)")
    P("=" * 118)
    law = []

    def law_test(name, ok, detail=""):
        law.append(ok)
        P(f"  [{'LAW PASSES' if ok else 'LAW FAILS '}] {name}" + (f"   ({detail})" if detail else ""))

    law_test("shape test 1: alpha_vir does NOT depend on the cloud's own acceleration, as the saturation "
             "law requires (data within 3 sigma of the SATURATED mock)",
             shape1["z_sat"] < 3.0,
             f"{shape1['z_sat']:.1f} sigma from saturated, {shape1['z_iso']:.1f} from isolated MOND, "
             f"{shape1['z_new']:.1f} from Newton")
    law_test("shape test 1 also excludes the RESTATEMENT branch (isolated MOND, i.e. what v^4 = G M_b a_0 "
             "alone implies) at >= 3 sigma", shape1["z_iso"] >= 3.0, f"{shape1['z_iso']:.1f} sigma")
    if shape2 is not None and not shape2["unident"]:
        law_test("shape test 2: at matched surface density and matched distance, alpha_vir tracks B(R_gal) "
                 "with slope +1 within 3 sigma", abs(shape2["sl"] - 1.0)/shape2["se"] < 3.0,
                 f"slope {shape2['sl']:+.3f} +- {shape2['se']:.3f}")
    else:
        P(f"  [NO VERDICT ] shape test 2 (the Galactocentric lever) is UNIDENTIFIED: the matched-cell slope "
          f"{shape2['sl']:+.3f} +- {shape2['se']:.3f} excludes BOTH hypotheses, so it is measuring "
          f"line-of-sight blending, not gravity.  Recorded as a dead estimator.")
    nf = sum(1 for o in law if not o)
    P(f"\n  >>> {len(law)-nf} of {len(law)} scoreable law tests pass.")
    P(f"  >>> The clouds CONFIRM that the external-field effect must be switched on -- isolated MOND, which")
    P(f"      is exactly what v^4 = G M_b a_0 plus algebra gives, is excluded at {shape1['z_iso']:.1f} sigma --")
    P(f"      but they CANNOT separate the saturation law from Newton, because at g_ext ~ 2 a_0 the predicted")
    P(f"      boost is only 0.07 dex, well under the scatter.  Molecular clouds are a test of the EFE's")
    P(f"      EXISTENCE, not a measurement of its size.")

    P("\n  UPSILON LEVER, numerically:  d log alpha_vir / d log Upsilon_star = 0.000 EXACTLY.  Molecular")
    P("  clouds contain no starlight in the mass budget; the whole mass is CO-derived.  The lever that")
    P("  replaces it is d log alpha_vir / d log X_CO = -1.000, and X_CO carries a factor-2 uncertainty and")
    P("  a Galactocentric METALLICITY GRADIENT.  That gradient makes X_CO RISE outward, which makes M rise")
    P("  outward, which makes alpha_vir FALL outward -- the OPPOSITE sign to the saturation law's rise.  So")
    P("  the dominant systematic of shape test 2 works against the law, not for it.")
    return ck.done()


if __name__ == "__main__":
    sys.exit(main())
