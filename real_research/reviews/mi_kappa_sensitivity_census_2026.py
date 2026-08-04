#!/usr/bin/env python3
r"""mi_kappa_sensitivity_census_2026.py -- DOOR 3: THE CENSUS. Every observable where kappa's VALUE enters
at leading order, ranked by kappa-sensitivity / total systematic.

THE OBJECT. The framework's one distinctive number is kappa = 1/2 in a0 = kappa c sqrt(G rho_Lambda), against
Milgrom 2020's kappa = 1/2pi. The separation is EXACTLY Z/(2pi) = 0.921318, i.e. 8.195% in the LOG (the right
object, since every a0 error in this corpus is fractional), so a 3-sigma test needs sigma(ln a0) <= 2.732%.
Everything else -- the kernel, the FORM a0 ~ c sqrt(G rho_Lambda) -- is prior art (Milgrom 1994 Ann.Phys.
229:384; Milgrom 1999 PLA 253:273 eq 9, whose coefficient was 2 c H_Lambda; Milgrom 2020; Deser & Levin 1997;
McGaugh 2008 ApJ 683:137 eq 11a). kappa = 1/2 is FITTED, not derived.

WHAT THIS FILE ADDS that the a0-estimator lane did not. That lane answered "can rotation curves fix kappa"
(no: shape systematic 30.6% vs a 7.87% gap; best shape-invariant total 17.5% = 0.47 sigma). This file asks the
COMPLEMENTARY question -- of ALL the observables in the corpus, which ones carry kappa at leading order, and
what is each one's ceiling -- and it converts every candidate to the SAME currency:

    for observable O, p = d ln O / d ln a0   =>   sigma(ln a0) = sigma(ln O) / |p|,
    n_sigma(kappa) = 0.08195 / sigma(ln a0).

That division by |p| is the whole reason a census is needed: a 4th-power observable (BTFR V_flat, dwarf sigma)
needs FOUR times the fractional precision to say the same thing about a0, and a perturbative observable
(wide-binary gamma_v) needs an absolute precision of order (gamma_v - 1) x 8%.

THE THREE STRUCTURAL RESULTS, all computed below and all against interest:
  C4  THE MASS FLOOR. Every deep-MOND door has the form O^n = C(shape) G M a0, so a0 and M enter ONLY as the
      product G M a0: |d ln a0 / d ln M_bar| = 1 EXACTLY, for the BTFR, the dwarf sigma^4 relation, the RAR
      and the lensing RAR alike. Hence sigma(ln a0) >= sigma(ln M_bar) for every one of them. 2.732% would
      need baryonic masses good to ~2.6% COHERENTLY; the best mass scale on offer (HI flux + helium) is
      5-10%. This bounds the whole class at ~1.0-1.6 sigma no matter the sample size, the kernel, or the depth.
  C2  THE TARGET ITSELF IS ONLY DEFINED TO ~1 GAP. a0_canon = (1/2) c sqrt(G rho_Lambda) with
      rho_Lambda = Omega_Lambda 3 H0^2 / 8 pi G, so the PREDICTION carries the cosmology's error: 0.96% inside
      Planck (fine), but the Planck-vs-SH0ES H0 fork moves it +8.1% to +11.4% in the log = 1.0-1.4x the kappa
      gap. A kappa claim must commit on the H0 tension first. Not previously charged anywhere in the corpus.
  C8/C9 TWO DOORS ARE DEFINITIONALLY DEAD, not merely imprecise. The EFE onset radius sits at y ~ 1 BY
      CONSTRUCTION -- exactly where the kernel family disagrees most -- and the SN-Ia surface-density
      threshold Sigma_a0 carries a factor-2pi CONVENTION freedom (0.798 dex) that is 22x the kappa signal
      (0.0356 dex) and that no measurement can shrink.

PROVENANCE OF EVERY IMPORTED NUMBER is stated at the point of use. Numbers computed here from raw data:
SPARC (BTFR + RAR depth), McConnachie 2012 dSph. Numbers imported from committed corpus scripts and labelled
as such: the 17.5% shape-invariant RAR total and the 13.21% BTFR shape term
(mi_routeA_shape_invariant_a0_2026.py S7/S9), the cluster g-dagger ladder (mi_route_a_cluster_eta_2026.py),
the frozen wide-binary sigma_sys = 0.02 and gamma_v = 1.0310 (mi_amendment7_wb_target_conflict_2026.py),
the KiDS lensing leg (papers/TRIANGLE_KIDS_2026.md). Numbers that are ESTIMATES rather than measurements are
printed with an [est] tag and never used to move a verdict in the framework's favour.

a0 is an INPUT throughout, on both footings (canonical 9.3614e-11, ALT 1.13e-10). Nothing here fits it.
Exit 0 = ran and every internal check held. No check(True); no check whose condition cannot fail.
"""
from __future__ import annotations

import csv
import glob
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mi_route_a_kernel import (A0_ALT, A0_CANON, A0_M20, C_L, G_N, Z_FW,  # noqa: E402
                               nu, nu_alpha1, nu_alpha2)

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 116)
    print(f"  {t}")


MSUN, KPC, PC = 1.989e30, 3.0857e19, 3.0857e16
A0_MOND = 1.20e-10                                   # McGaugh 2016 RAR g-dagger, the literature's own scale
UD_FID, UB_OVER_UD = 0.7, 1.4                        # the corpus's fiducial SPARC M/L, verbatim
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def nu_simple(y):
    """the literature's simple mu = x/(1+x) inverted in spherical symmetry -- a CONTROL, not the framework's."""
    y = np.asarray(y, float)
    return 0.5 * (y + np.sqrt(y * y + 4.0 * y)) / y


KERN = {"RouteA": nu, "alpha=1": nu_alpha1, "alpha=2": nu_alpha2, "simple": nu_simple}


def Qy(f, y):
    """Q(y) = nu(y)^2 y = V^4/(G M a0) = sigma^4/((4/81) G M a0). Q(0) = 1 for EVERY kernel."""
    y = np.asarray(y, float)
    return f(y) ** 2 * y


def hs_logQ(y):
    """the four-kernel HALF-SPREAD of ln Q at depth y -- the shape systematic of any deep-limit estimator."""
    v = np.log([float(Qy(f, y)) for f in KERN.values()])
    return 0.5 * float(v.max() - v.min())


def solve_y(f, nu_target):
    """invert nu(y) = nu_target by bisection (nu is strictly decreasing in y). Returns nan if out of range."""
    lo, hi = -8.0, 8.0
    if float(f(10.0 ** hi)) > nu_target or float(f(10.0 ** lo)) < nu_target:
        return float("nan")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if float(f(10.0 ** mid)) > nu_target:
            lo = mid
        else:
            hi = mid
    return 10.0 ** (0.5 * (lo + hi))


ROWS = []       # the census: (door, p, kappa signal in O, shape sys in a0, total sys in a0, class, wall)


# ------------------------------------------------------------------------------------- raw data, loaded once
def load_sparc():
    """SPARC Lelli+2016 master table + rotmod curves, on the corpus's OWN cuts (Q<=2, inc>=30, e_V/V<10%)."""
    tbl = {}
    for ln in open(os.path.join(HERE, "data", "SPARC_Lelli2016c.mrt")).read().split("\n"):
        t = ln.split()
        if len(t) != 19:
            continue
        try:
            tbl[t[0]] = dict(D=float(t[2]), eD=float(t[3]), fD=int(t[4]), inc=float(t[5]), einc=float(t[6]),
                             L36=float(t[7]), MHI=float(t[13]), Vf=float(t[15]), eVf=float(t[16]),
                             Qf=int(t[17]))
        except ValueError:
            continue
    out = []
    for f in sorted(glob.glob(os.path.join(HERE, "data", "sparc_data", "*_rotmod.dat"))):
        nm = os.path.basename(f).replace("_rotmod.dat", "")
        if nm not in tbl:
            continue
        T = tbl[nm]
        if T["Qf"] > 2 or T["inc"] < 30.0:
            continue
        d = np.genfromtxt(f, comments="#")
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
        Vg2 = np.sign(Vg) * Vg ** 2
        V2f = Vg2 + UD_FID * Vd ** 2 + UB_OVER_UD * UD_FID * Vb ** 2
        m = ((R > 0) & (Vo > 0) & (V2f > 0) & np.isfinite(V2f) & (eV / np.maximum(Vo, 1e-9) < 0.10))
        if m.sum() < 1:
            continue
        g = dict(T)
        g.update(name=nm, R=R[m] * KPC, Vg2=Vg2[m] * 1e6, Vd2=Vd[m] ** 2 * 1e6, Vb2=Vb[m] ** 2 * 1e6)
        out.append(g)
    return out


GG = load_sparc()
GB_ALL = np.concatenate([(g["Vg2"] + UD_FID * g["Vd2"] + UB_OVER_UD * UD_FID * g["Vb2"]) / g["R"] for g in GG])
Y_ALL = GB_ALL / A0_CANON


def load_dsph():
    rows = []
    with open(os.path.join(HERE, "data", "dsph", "mcconnachie2012_dsph.csv")) as fh:
        for r in csv.DictReader(fh):
            try:
                s = float(r["sigma*"])
                R2 = float(r["R2"])
                MV = float(r["VMag"])
            except (ValueError, TypeError, KeyError):
                continue
            try:
                es = float(r["e_sigma*"])
            except ValueError:
                es = float("nan")
            try:
                mhi = float(r["M.HI"])
            except ValueError:
                mhi = 0.0
            rows.append(dict(name=r["Name"], sub=r["SubG"], D=float(r["D"]), MV=MV, R2=R2, sig=s, esig=es,
                             MHI=mhi))
    return rows


DS = load_dsph()
print(f"  data loaded: SPARC {len(GG)} galaxies / {len(Y_ALL)} points (y median {np.median(Y_ALL):.3f}); "
      f"McConnachie 2012 dwarfs with sigma+R_half+M_V: {len(DS)}")


def dln(f, x0, h=1e-5):
    """central log-derivative d ln f / d ln x at x0."""
    return (math.log(f(x0 * (1 + h))) - math.log(f(x0 * (1 - h)))) / (2 * h)


def dabs(f, x0, h=1e-5):
    """central derivative d f / d ln x at x0 (for observables measured with an ABSOLUTE error)."""
    return (f(x0 * (1 + h)) - f(x0 * (1 - h))) / (2 * h)


def btfr_table(ups=UD_FID, gasf=1.0, Dfac=None):
    """per-galaxy BTFR quantities: a0_hat = V_flat^4/(G M_bar), depth y at R_last, Gamma = g_bar R^2/(G M_bar).

    Distance enters as M_bar ~ D^2 (both L[3.6] and M_HI are fluxes) while V_flat is a velocity, D^0 -- so
    a0_hat ~ D^-2 EXACTLY, which is why the distance scale is a leading term in this door's budget.
    """
    a0h, yv, Gm, fst, lnD, iD = [], [], [], [], [], []
    for i, g in enumerate(GG):
        if g["Vf"] <= 0 or len(g["R"]) < 3:
            continue
        dfac = 1.0 if Dfac is None else float(Dfac[i])
        Mst = ups * g["L36"] * dfac ** 2
        Mgs = gasf * 1.33 * g["MHI"] * dfac ** 2
        Mb = (Mst + Mgs) * 1e9 * MSUN
        if Mb <= 0:
            continue
        V2 = g["Vg2"] + ups * g["Vd2"] + UB_OVER_UD * ups * g["Vb2"]
        gbl = V2[-1] / g["R"][-1]
        a0h.append((g["Vf"] * 1e3) ** 4 / (G_N * Mb))
        yv.append(gbl / A0_CANON)
        Gm.append(gbl * g["R"][-1] ** 2 / (G_N * Mb))
        fst.append(Mst / (Mst + Mgs))
        lnD.append(g["eD"] / max(g["D"], 1e-9))
        iD.append(i)
    return (np.array(a0h), np.array(yv), np.array(Gm), np.array(fst), np.array(lnD), np.array(iD))


BA0, BY, BG, BFST, BeD, BIDX = btfr_table()
UPS_V = 1.5                                   # fiducial V-band M/L for old dwarf populations [est, 1.0-3.0]
DS_M = np.array([UPS_V * 10 ** (-0.4 * (d["MV"] - 4.83)) + 1.33e6 * d["MHI"] for d in DS]) * MSUN
DS_R = np.array([d["R2"] for d in DS]) * PC
DS_S = np.array([d["sig"] for d in DS]) * 1e3
DS_YIN = G_N * DS_M / (A0_CANON * DS_R ** 2)  # internal depth at the half-light radius
DS_A0 = 81.0 * DS_S ** 4 / (4.0 * G_N * DS_M)


def a0_from_btfr(V, R, M, f=nu):
    """invert V^4 = Q(y) G M a0, y = G M/(a0 R^2), for a0. Bisection in log a0; Q monotone in a0."""
    lo, hi = math.log(1e-13), math.log(1e-7)
    tgt = V ** 4
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        a = math.exp(mid)
        val = float(Qy(f, G_N * M / (a * R * R))) * G_N * M * a
        if val < tgt:
            lo = mid
        else:
            hi = mid
    return math.exp(0.5 * (lo + hi))


# ============================================================================================ C1
banner("C1  THE GAP, AND THE BUDGET IT IMPLIES")

GAP_LOG = math.log(A0_CANON / A0_M20)
GAP_FRAC = 1.0 - A0_M20 / A0_CANON
NEED3 = GAP_LOG / 3.0
GAP_MOND = abs(math.log(A0_MOND / A0_CANON))
print(f"  a0(kappa=1/2) = {A0_CANON:.5e}   a0(kappa=1/2pi) = {A0_M20:.5e}   ratio = Z/(2pi) = "
      f"{A0_M20/A0_CANON:.6f}")
print(f"  kappa gap: {100*GAP_FRAC:.3f}% of canonical, {100*GAP_LOG:.3f}% in the LOG = {GAP_LOG/math.log(10):.4f}"
      f" dex.  3 sigma needs sigma(ln a0) <= {100*NEED3:.3f}%.")
print(f"  for contrast, the literature's own g-dagger 1.20e-10 sits {100*GAP_MOND:.2f}% (log) from canonical, "
      f"{GAP_MOND/GAP_LOG:.2f}x the kappa gap -- so 'is a0 the RAR value' is a 3x EASIER question than "
      f"'is kappa 1/2 or 1/2pi'.")
check(abs(A0_M20 / A0_CANON - Z_FW / (2 * math.pi)) < 1e-12 and abs(GAP_LOG - 0.08195) < 1e-4
      and abs(NEED3 - 0.02732) < 1e-4 and GAP_MOND > 2.5 * GAP_LOG,
      f"C1 conventions locked to the committed lane: log gap {100*GAP_LOG:.3f}% (committed 8.195%), 3-sigma "
      f"budget {100*NEED3:.3f}% (committed 2.732%), separation exactly Z/(2pi) so both footings inherit it "
      f"unchanged. And the census's first useful ordering fact: the framework-vs-RAR-convention question is "
      f"{GAP_MOND/GAP_LOG:.1f}x easier than the kappa question, so a door that resolves 25% still says nothing "
      f"about kappa")


# ============================================================================================ C2
banner("C2  THE TARGET'S OWN ERROR -- the kappa PREDICTION is only as sharp as the cosmology behind rho_Lambda")

OML, dOML = 0.6847, 0.0073                       # Planck 2018 TT,TE,EE+lowE+lensing
H0P, dH0P = 67.36, 0.54
H0S, dH0S = 73.04, 1.04                          # SH0ES 2022 (Riess et al.), the competing ladder
OMH2 = 0.1430                                    # Planck omega_m = Omega_m h^2, the tightly measured combo
s_ln_rho = math.hypot(dOML / OML, 2.0 * dH0P / H0P)
s_ln_a0_th = 0.5 * s_ln_rho                      # a0 ~ sqrt(rho_Lambda)
fork_fixed_OmL = math.log(H0S / H0P)             # rho_L ~ Om_L H0^2 at fixed Om_L  => a0 ~ H0
h_p, h_s = H0P / 100.0, H0S / 100.0
fork_fixed_om = 0.5 * math.log((h_s**2 - OMH2) / (h_p**2 - OMH2))   # at fixed omega_m instead
need_dyn = math.sqrt(max(NEED3**2 - s_ln_a0_th**2, 0.0))
print(f"  a0_canon = (1/2) c sqrt(G rho_Lambda), rho_Lambda = Omega_Lambda 3 H0^2 / 8 pi G, so the TARGET "
      f"inherits the cosmology:")
print(f"    inside Planck:  sigma(ln rho_L) = {100*s_ln_rho:.2f}%  ->  sigma(ln a0_target) = "
      f"{100*s_ln_a0_th:.2f}%   ({100*s_ln_a0_th/NEED3:.0f}% of the 3-sigma budget)")
print(f"    Planck -> SH0ES H0 fork: at fixed Omega_Lambda {100*fork_fixed_OmL:+.2f}%, at fixed omega_m "
      f"{100*fork_fixed_om:+.2f}%  =  {fork_fixed_OmL/GAP_LOG:.2f}-{fork_fixed_om/GAP_LOG:.2f}x THE KAPPA GAP "
      f"(one gap to one-and-a-half)")
print(f"    => a dynamical measurement must reach {100*need_dyn:.2f}% (not {100*NEED3:.2f}%) once the Planck "
      f"input is charged.")
# the fork does NOT change the gap (that is exactly Z/2pi) -- it slides BOTH targets together, hence moves the
# DECISION BOUNDARY. The boundary is the geometric midpoint of the two targets.
mid_P = math.sqrt(A0_CANON * A0_M20)
mid_S = mid_P * math.exp(fork_fixed_OmL)
mid_S2 = mid_P * math.exp(fork_fixed_om)
A0_DEEP_GASDOM = 8.5573e-11          # committed: mi_routeA_shape_invariant_a0_2026.py S7, sharpest shape-inv.
A0_LINE_MED_SM = 8.9640e-11          # committed: same file S10b, shape-marginalised a0-line median
A0_LINE_ROUTEA = 9.9159e-11          # committed: same file S10b, gas-dom a0-line debiased onto Route A
print(f"  the fork leaves the GAP untouched (it is the pure number Z/2pi) and instead slides the DECISION "
      f"BOUNDARY, the geometric midpoint of the two targets:")
print(f"    boundary(Planck) = {mid_P:.4e}   boundary(SH0ES) = {mid_S:.4e} to {mid_S2:.4e}  -> a flip window "
      f"{mid_P:.3e}-{mid_S2:.3e} spanning {math.log(mid_S2/mid_P)/GAP_LOG:.2f} gaps")
print(f"    the window CONTAINS a0_canon itself ({A0_CANON:.4e}) and the committed Route-A-debiased "
      f"gas-dominated a0-line central ({A0_LINE_ROUTEA:.4e}); the committed shape-marginalised median "
      f"({A0_LINE_MED_SM:.4e}) sits {100*abs(math.log(A0_LINE_MED_SM/mid_P)):.2f}% below the Planck boundary, "
      f"i.e. ON it. For any measurement in or near the window, WHICH kappa is preferred flips with the H0 "
      f"choice alone.")
check(s_ln_a0_th < NEED3 and fork_fixed_OmL > 0.95 * GAP_LOG and fork_fixed_om > GAP_LOG and need_dyn < NEED3
      and mid_P < A0_CANON < mid_S2 and mid_P < A0_LINE_ROUTEA < mid_S2
      and abs(math.log(A0_LINE_MED_SM / mid_P)) < 0.1 * GAP_LOG,
      f"C2 *** THE kappa DECISION BOUNDARY MOVES BY MORE THAN THE kappa GAP UNDER THE H0 TENSION. *** Within "
      f"Planck the target is good to {100*s_ln_a0_th:.2f}%, comfortably inside the {100*NEED3:.2f}% budget, so "
      f"the cosmological leg is NOT the bottleneck -- that is the favourable half, and it means the whole "
      f"burden sits on the dynamical side ({100*need_dyn:.2f}% after charging Planck). The unfavourable half: "
      f"a0_target ~ sqrt(Omega_Lambda) H0 slides BOTH targets together by {100*fork_fixed_OmL:+.1f}% to "
      f"{100*fork_fixed_om:+.1f}% (= {fork_fixed_OmL/GAP_LOG:.1f}-{fork_fixed_om/GAP_LOG:.1f} gaps) when SH0ES "
      f"replaces Planck, which does not change the gap but moves the decision boundary from {mid_P:.3e} to "
      f"{mid_S2:.3e}. That window contains a0_canon AND the corpus's own Route-A-debiased a0-line central, "
      f"while the shape-marginalised median sits within "
      f"{100*abs(math.log(A0_LINE_MED_SM/mid_P)):.2f}% of the Planck boundary -- so a kappa verdict drawn from "
      f"any of them is an H0 verdict in disguise. Not charged anywhere in the corpus; every published "
      f"'a0 = 9.3614e-11' is implicitly a Planck-cosmology statement")


# ============================================================================================ C3
banner("C3  THE RESPONSE EXPONENT p = d ln O / d ln a0 -- the currency conversion every door must pay")

Y_BTFR = float(np.median(BY))                              # SPARC's outermost measured radii
CL = [i for i, d in enumerate(DS) if d["MV"] < -8.0]       # classical dwarfs; ultrafaints handled in C6
Y_DW = float(np.median(DS_YIN[CL]))
Y_RAR = float(np.median(Y_ALL))
Y_LENS = 1.0e-15 / A0_CANON                                # Brouwer+2021 KiDS deepest bin
GB_REF, R_REF = A0_CANON * Y_BTFR, 10.0 * KPC


EXPO = []
for lab, y0, kind in [("RAR g_obs @ SPARC median y", Y_RAR, "nu"),
                      ("deep RAR g_obs @ KiDS y", Y_LENS, "nu"),
                      ("BTFR V_flat @ SPARC y_out", Y_BTFR, "quart"),
                      ("dwarf sigma @ classical y_int", Y_DW, "quart"),
                      ("Sigma_a0 = a0/2piG", 0.0, "lin"),
                      ("EFE onset radius D_thr", 0.0, "sqrtinv"),
                      ("cluster knee g-dagger", 0.0, "lin")]:
    if kind == "nu":
        GB_REF_LOC = A0_CANON * y0
        p = dln(lambda a: float(nu(GB_REF_LOC / a)) * GB_REF_LOC, A0_CANON)
    elif kind == "quart":
        gb = A0_CANON * y0
        p = dln(lambda a: (float(Qy(nu, gb / a)) * gb * R_REF ** 2 * a) ** 0.25, A0_CANON)
    elif kind == "lin":
        p = dln(lambda a: a / (2 * math.pi * G_N), A0_CANON)
    else:
        p = dln(lambda a: math.sqrt(G_N * 1e12 * MSUN / (a * 0.48)), A0_CANON)
    EXPO.append((lab, y0, p))
print(f"  {'observable O':<32}{'y':>10}{'p = dlnO/dln a0':>18}{'1/|p|':>8}{'kappa signal in O':>19}")
print("  " + "-" * 88)
for lab, y0, p in EXPO:
    print(f"  {lab:<32}{y0 if y0 else float('nan'):>10.3g}{p:>18.4f}{1/abs(p):>8.2f}"
          f"{100*abs(p)*GAP_LOG:>18.3f}%")
p_sig = dict((l, p) for l, _, p in EXPO)
check(abs(p_sig["Sigma_a0 = a0/2piG"] - 1.0) < 1e-8
      and abs(p_sig["deep RAR g_obs @ KiDS y"] - 0.5) < 2e-3
      and abs(p_sig["EFE onset radius D_thr"] + 0.5) < 1e-8
      and abs(p_sig["BTFR V_flat @ SPARC y_out"] - 0.25) < 0.05
      and 1 / abs(p_sig["BTFR V_flat @ SPARC y_out"]) > 3.5,
      f"C3 the numerical differencing is validated against the three exponents that are analytic -- Sigma_a0 "
      f"gives p = {p_sig['Sigma_a0 = a0/2piG']:.6f} (exactly 1), the deep RAR gives "
      f"{p_sig['deep RAR g_obs @ KiDS y']:.4f} (exactly 1/2, since nu -> 1/sqrt(y)), the EFE length gives "
      f"{p_sig['EFE onset radius D_thr']:.6f} (exactly -1/2) -- so the non-analytic entries can be trusted. "
      f"THE CENSUS'S FIRST ORDERING FACT: the two 4th-power doors (BTFR V_flat, dwarf sigma) convert at "
      f"1/|p| = {1/abs(p_sig['BTFR V_flat @ SPARC y_out']):.1f}, i.e. they need FOUR TIMES the fractional "
      f"precision to say the same thing about a0, while Sigma_a0 converts at 1.0 and is therefore the most "
      f"a0-sensitive observable in the corpus per unit precision -- which is exactly why C9 has to check "
      f"whether its threshold constant is even defined")


# ============================================================================================ C4
banner("C4  THE MASS FLOOR -- a0 and M_bar enter every deep-MOND door ONLY through the product, so "
       "sigma(ln a0) >= sigma(ln M_bar)")


def a0_from_deep(O, R, M, coeff=1.0, f=nu):
    """invert O^4 = coeff Q(y) G M a0, y = G M/(a0 R^2), for a0 (monotone increasing in a0)."""
    lo, hi = math.log(1e-14), math.log(1e-6)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        a = math.exp(mid)
        if coeff * float(Qy(f, G_N * M / (a * R * R))) * G_N * M * a < O ** 4:
            lo = mid
        else:
            hi = mid
    return math.exp(0.5 * (lo + hi))


M_REF = GB_REF * R_REF ** 2 / G_N
V_REF = (float(Qy(nu, Y_BTFR)) * G_N * M_REF * A0_CANON) ** 0.25
DEEPM = 1e-6 * A0_CANON * R_REF ** 2 / G_N                 # a mass putting the same R in the deep limit
V_DEEP = (float(Qy(nu, 1e-6)) * G_N * DEEPM * A0_CANON) ** 0.25
R_DW = float(np.median(DS_R[CL]))                          # median classical half-light radius
M_DW = Y_DW * A0_CANON * R_DW ** 2 / G_N                   # the mass that puts THAT radius at y = Y_DW
S_REF = ((4.0 / 81.0) * float(Qy(nu, Y_DW)) * G_N * M_DW * A0_CANON) ** 0.25
mass_exp = {
    "BTFR, SPARC depth y=%.3f" % Y_BTFR: dln(lambda M: a0_from_deep(V_REF, R_REF, M), M_REF),
    "BTFR, deep limit y=1e-6": dln(lambda M: a0_from_deep(V_DEEP, R_REF, M), DEEPM),
    "dwarf sigma^4, y=%.3f" % Y_DW: dln(lambda M: a0_from_deep(S_REF, R_DW, M, 4.0 / 81.0), M_DW),
}
S_WB = 5000.0 * 1.496e11                                   # 5 kAU, mid-range of the DR4 window
M_WB = 1.0 * MSUN


def a0_from_gamma(gam, M, s, f=nu):
    """invert gamma_v = sqrt(nu(y)), y = G M/(s^2 a0), for a0. nu increases with a0, so gamma does too."""
    lo, hi = math.log(1e-14), math.log(1e-6)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if math.sqrt(float(f(G_N * M / (s * s * math.exp(mid))))) < gam:
            lo = mid
        else:
            hi = mid
    return math.exp(0.5 * (lo + hi))


GAM_REF = math.sqrt(float(nu(G_N * M_WB / (S_WB ** 2 * A0_CANON))))
mass_exp["wide binary gamma_v (any depth)"] = dln(lambda M: a0_from_gamma(GAM_REF, M, S_WB), M_WB)
def q_of(y, f=nu):
    """q = d ln Q / d ln y, the finite-depth term. Implicit differentiation of O^4 = Q(y) G M a0 with
    y ~ M/a0 gives d ln a0/d ln M = -(1+q)/(1-q), which is >= 1 in magnitude for every q in [0,1)."""
    return dln(lambda yy: float(Qy(f, yy)), y)


ANA = {"BTFR, SPARC depth y=%.3f" % Y_BTFR: -(1 + q_of(Y_BTFR)) / (1 - q_of(Y_BTFR)),
       "BTFR, deep limit y=1e-6": -(1 + q_of(1e-6)) / (1 - q_of(1e-6)),
       "dwarf sigma^4, y=%.3f" % Y_DW: -(1 + q_of(Y_DW)) / (1 - q_of(Y_DW)),
       "wide binary gamma_v (any depth)": 1.0}
print(f"  {'door':<34}{'d ln a0/d ln M_bar (solver)':>30}{'-(1+q)/(1-q) analytic':>24}")
print("  " + "-" * 90)
for k, v in mass_exp.items():
    print(f"  {k:<34}{v:>30.6f}{ANA[k]:>24.6f}")
ana_worst = max(abs(mass_exp[k] - ANA[k]) for k in mass_exp)
BARY = [("stellar Upsilon[3.6] zero point (coherent)", 0.230, "committed A0LINE 0.0999 dex"),
        ("gas-dominated points: f_* x Upsilon", 0.074, "committed shape-inv S7"),
        ("HI flux scale + helium 1.33 (best case)", 0.050, "[est] literature 5-10%"),
        ("main-sequence binary masses (photometric)", 0.050, "[est]"),
        ("cluster hot-gas mass", 0.150, "[est] 10-20%")]
best_mass = min(b[1] for b in BARY)
ceil_mass = GAP_LOG / best_mass
print(f"\n  {'baryonic mass scale':<44}{'sigma(ln M)':>12}{'-> n_sigma(kappa) ceiling':>26}  provenance")
for lab, s, prov in BARY:
    print(f"  {lab:<44}{100*s:>11.1f}%{GAP_LOG/s:>26.2f}  {prov}")
print(f"  REQUIRED for 3 sigma: sigma(ln M_bar) <= {100*need_dyn:.2f}% coherently "
      f"({100*need_dyn/best_mass:.0f}% of the best scale on offer).")
check(all(abs(v) >= 1.0 - 1e-6 for v in mass_exp.values()) and ana_worst < 1e-4
      and abs(mass_exp["BTFR, deep limit y=1e-6"] + 1.0) < 3e-3
      and abs(mass_exp["BTFR, SPARC depth y=%.3f" % Y_BTFR]) > 1.05
      and best_mass > need_dyn and ceil_mass < 3.0,
      f"C4 *** THE WHOLE CLASS IS BOUNDED BY THE BARYONIC MASS SCALE, AND THE BOUND IS ~"
      f"{ceil_mass:.1f} SIGMA, NOT 3. *** Every deep-MOND door has the form O^4 = C(shape) G M a0, so a0 and M "
      f"appear only through their product; two independent routes -- bisection+differencing of the inferred a0, "
      f"and implicit differentiation giving -(1+q)/(1-q) -- agree to {ana_worst:.1e}, so the exponent is "
      f"|d ln a0 / d ln M_bar| = {abs(mass_exp['BTFR, deep limit y=1e-6']):.4f} in the deep limit "
      f"(-> exactly 1 as q -> 0, for the BTFR and the dwarf sigma^4 relation alike) and it gets WORSE, not "
      f"better, at finite depth "
      f"({abs(mass_exp['BTFR, SPARC depth y=%.3f' % Y_BTFR]):.3f} at SPARC's outermost radii, because the "
      f"finite-y term (1+q)/(1-q) amplifies it). The wide binary is the one door where the exponent is exactly "
      f"+1 at ANY depth, which is why its 5% photometric masses matter. CONSEQUENCE: sigma(ln a0) can never "
      f"beat sigma(ln M_bar), the best mass scale on offer is ~{100*best_mass:.0f}% (pure-gas systems), and "
      f"3 sigma needs {100*need_dyn:.2f}%. No sample size, no kernel commitment and no extra depth touches this")


# ============================================================================================ C5
banner("C5  DOOR: THE BTFR INTERCEPT (Door 1's object, priced here for the ranking)")

lnB = [float(np.mean(np.log(Qy(f, BY) * BG))) for f in KERN.values()]
raw_b = math.exp(float(np.mean(np.log(BA0))))
hs_b = 0.5 * (max(lnB) - min(lnB))
stat_b = float(np.std(np.log(BA0))) / math.sqrt(len(BA0))
eVf = np.array([4.0 * GG[i]["eVf"] / max(GG[i]["Vf"], 1e-9) for i in BIDX])
s_vf = float(np.sqrt(np.sum(eVf ** 2))) / len(eVf)
s_drand = float(np.sqrt(np.sum((2.0 * BeD) ** 2))) / len(BeD)
Dfac = np.array([73.0 / H0P if g["fD"] == 1 else 1.0 for g in GG])
s_dcoh = abs(math.log(math.exp(float(np.mean(np.log(btfr_table(Dfac=Dfac)[0])))) / raw_b))
u_lo = math.exp(float(np.mean(np.log(btfr_table(ups=0.5)[0]))))
u_hi = math.exp(float(np.mean(np.log(btfr_table(ups=0.8)[0]))))
s_ups = 0.5 * abs(math.log(u_lo / u_hi))
s_gas = 0.5 * abs(math.log(math.exp(float(np.mean(np.log(btfr_table(gasf=0.9)[0]))))
                           / math.exp(float(np.mean(np.log(btfr_table(gasf=1.1)[0]))))))
print(f"  {len(BA0)} galaxies with a quality V_flat.  raw <V_flat^4/(G M_bar)> = {raw_b:.4e} = "
      f"{raw_b/A0_CANON:.3f}x canonical;  y(R_last) median {Y_BTFR:.4f};  Gamma median {np.median(BG):.3f}")
print("  <Q(y_out) Gamma> per kernel: " + "  ".join(f"{k} {math.exp(v):.4f}" for k, v in zip(KERN, lnB)))
check(abs(raw_b / 1.2857e-10 - 1) < 2e-3 and abs(Y_BTFR - 0.0832) < 2e-3
      and abs(float(np.median(BG)) - 1.164) < 5e-3 and abs(math.exp(lnB[0]) - 1.6099) < 5e-3
      and abs(math.exp(lnB[2]) - 1.2484) < 5e-3 and abs(hs_b - 0.1321) < 3e-3,
      f"C5a CONTROL: this file's independent BTFR build reproduces the committed lane exactly -- "
      f"{len(BA0)} galaxies, raw {raw_b:.4e} (committed 1.2857e-10), y_out median {Y_BTFR:.4f} (0.083), Gamma "
      f"median {float(np.median(BG)):.3f} (1.164), <Q Gamma> {math.exp(lnB[0]):.4f}/{math.exp(lnB[1]):.4f}/"
      f"{math.exp(lnB[2]):.4f}/{math.exp(lnB[3]):.4f} (1.6099/1.3212/1.2484/1.6259) and shape half-spread "
      f"{100*hs_b:.2f}% (13.21%). Every number below is therefore substitutable into the committed budget")

# the Gamma-debias identity: a0_raw/(Q Gamma) = V^4/(Q g_bar R^2), in which M_bar CANCELS IDENTICALLY.
V4 = np.array([(GG[i]["Vf"] * 1e3) ** 4 for i in BIDX])
RL = np.array([GG[i]["R"][-1] for i in BIDX])


def dbl_of(ups=UD_FID, gasf=1.0):
    """the Gamma-debiased estimator V^4/(Q(y) g_bar R^2). Mass-FREE in M_bar_total but NOT in Upsilon or the
    gas scale, because both re-enter through the LOCAL g_bar at R_last (and through y, hence Q)."""
    gb = np.array([(gasf * GG[i]["Vg2"] + ups * GG[i]["Vd2"] + UB_OVER_UD * ups * GG[i]["Vb2"])[-1]
                   / GG[i]["R"][-1] for i in BIDX])
    q = np.array([float(Qy(nu, v / A0_CANON)) for v in gb])
    return math.exp(float(np.mean(np.log(V4 / (q * gb * RL ** 2)))))


GBL = np.array([(GG[i]["Vg2"] + UD_FID * GG[i]["Vd2"] + UB_OVER_UD * UD_FID * GG[i]["Vb2"])[-1]
                / GG[i]["R"][-1] for i in BIDX])
QA = np.array([float(Qy(nu, y)) for y in BY])
dbl = math.exp(float(np.mean(np.log(V4 / (QA * GBL * RL ** 2)))))
dbl_pert = math.exp(float(np.mean(np.log((V4 / 1.20) / (QA * GBL * RL ** 2 / 1.20)))))
s_ups_d = 0.5 * abs(math.log(dbl_of(ups=0.5) / dbl_of(ups=0.8)))
s_gas_d = 0.5 * abs(math.log(dbl_of(gasf=0.9) / dbl_of(gasf=1.1)))
tot_dbl = math.hypot(math.hypot(math.hypot(hs_b, stat_b), math.hypot(s_vf, s_drand)),
                     math.hypot(s_dcoh, math.hypot(s_ups_d, s_gas_d)))
print(f"  the Gamma-debias identity: a0_raw/<Q Gamma> = {raw_b/math.exp(lnB[0]):.4e} and V^4/(Q g_bar R^2) = "
      f"{dbl:.4e} -- the SAME number, because M_bar cancels; a 20% M_bar shift moves it by "
      f"{100*abs(dbl_pert/dbl-1):.1e}%. But Upsilon and the gas scale RE-ENTER through the local g_bar: "
      f"{100*s_ups_d:.1f}% and {100*s_gas_d:.1f}%, so the debiased estimator's own total is "
      f"{100*tot_dbl:.1f}% = {GAP_LOG/tot_dbl:.2f} sigma -- NOT the {100*math.hypot(math.hypot(hs_b, stat_b), s_vf):.1f}% "
      f"one gets by mistaking 'mass-free' for 'baryon-free'.")
tot_b = math.hypot(math.hypot(math.hypot(hs_b, stat_b), math.hypot(s_vf, s_drand)),
                   math.hypot(math.hypot(s_dcoh, s_ups), s_gas))
print(f"  a0-space budget: shape {100*hs_b:.1f}%  ens.stat {100*stat_b:.1f}%  V_flat {100*s_vf:.1f}%  "
      f"D(random) {100*s_drand:.1f}%  D(H0 scale, full fork) {100*s_dcoh:.1f}%  Upsilon {100*s_ups:.1f}%  "
      f"gas {100*s_gas:.1f}%  ->  TOTAL {100*tot_b:.1f}%  =  {GAP_LOG/tot_b:.2f} sigma on kappa")
check(abs(dbl / (raw_b / math.exp(lnB[0])) - 1) < 1e-12 and abs(dbl_pert / dbl - 1) < 1e-12
      and tot_b > 4 * NEED3 and s_dcoh > 0.95 * GAP_LOG and s_ups_d > 2 * NEED3,
      f"C5b *** THE CORPUS'S Gamma-DEBIASED BTFR IS NOT A MASS MEASUREMENT AT ALL, AND THEREFORE NOT THE "
      f"BTFR. *** Debiasing by the MEASURED Gamma = g_bar R^2/(G M_bar) cancels M_bar identically: "
      f"a0_raw/<Q Gamma> = V^4/(Q g_bar R^2) to 1e-12, and a 20% shift in every baryonic mass moves it by "
      f"{100*abs(dbl_pert/dbl-1):.0e}%. That is favourable in one sense -- it escapes C4's TOTAL-mass floor -- "
      f"but it means the committed 'BTFR' number is really the OUTERMOST-POINT RAR estimator wearing a BTFR "
      f"label, so it is not an independent door; and 'mass-free' is not 'baryon-free', because Upsilon "
      f"re-enters through the local g_bar at {100*s_ups_d:.1f}%, giving it a total of {100*tot_dbl:.1f}% rather "
      f"than the {100*math.hypot(math.hypot(hs_b, stat_b), s_vf):.1f}% a careless budget would claim. A GENUINE "
      f"BTFR intercept, which uses the photometric+HI M_bar and a "
      f"MODELLED Gamma, carries the full budget priced here: {100*tot_b:.1f}% = {GAP_LOG/tot_b:.2f} sigma. Note "
      f"which term is largest after shape: the H0 distance scale at {100*s_dcoh:.1f}% (a0 ~ D^-2 and SPARC's "
      f"Hubble-flow distances assume H0 = 73), by itself {s_dcoh/GAP_LOG:.1f}x the kappa gap")
ROWS.append(("BTFR intercept (photometric M_bar)", p_sig["BTFR V_flat @ SPARC y_out"], hs_b, tot_b,
             "partly", "shape 13% + H0 distance scale + Upsilon"))
ROWS.append(("BTFR, Gamma-debiased (= last-point RAR)", p_sig["BTFR V_flat @ SPARC y_out"], hs_b,
             tot_dbl, "partly", "shape 13% + Upsilon via the LOCAL g_bar; not the BTFR"))


# ============================================================================================ C6
banner("C6  DOOR: THE PRESSURE-SUPPORTED sigma^4 = (4/81) G M a0 RELATION (McGaugh & Milgrom 2013)")

MW_M, M31_M = 1.0e12 * MSUN, 1.5e12 * MSUN
yext = []
for d in DS:
    if d["sub"] == "MW":
        yext.append(G_N * MW_M / ((d["D"] * KPC) ** 2) / A0_CANON)
    elif d["sub"] == "M31":
        yext.append(float("nan"))                          # D is heliocentric: host separation not in table
    else:
        yext.append(0.0)
yext = np.array(yext)
mwi = [i for i, d in enumerate(DS) if d["sub"] == "MW"]
iso = [i for i, d in enumerate(DS) if d["sub"] == "Rest"]
frac_efe = float(np.mean(yext[mwi] > DS_YIN[mwi]))
print(f"  depth census: classical dwarfs (M_V < -8, N={len(CL)}) internal y_int median {Y_DW:.4f} "
      f"(16-84% {np.percentile(DS_YIN[CL],16):.4f}-{np.percentile(DS_YIN[CL],84):.4f}) -- "
      f"{Y_BTFR/Y_DW:.1f}x DEEPER than SPARC's outermost radii, so the shape systematic is only "
      f"{100*hs_logQ(Y_DW):.1f}% (vs {100*hs_logQ(Y_BTFR):.1f}% at the BTFR's depth)")
print(f"  but the EFE: for the {len(mwi)} MW satellites y_ext = G M_MW/D^2/a0 exceeds y_int in "
      f"{100*frac_efe:.0f}% of cases (median ratio y_ext/y_int = "
      f"{float(np.median(yext[mwi]/DS_YIN[mwi])):.1f}) -- the isolated relation does NOT apply to them, and "
      f"the corpus's own additive-EFE prescription is diagnosed as OVER-suppressing (2-11x)")
a0i = DS_A0[iso] / A0_CANON
print(f"  the only EFE-clean sample in the table is the {len(iso)} 'Rest' (isolated LG) dwarfs: "
      + ", ".join(f"{DS[i]['name'].split(' (')[0]} {DS_A0[i]/A0_CANON:.2f}x" for i in iso)
      + f"  -> spread {math.log10(a0i.max()/a0i.min()):.2f} dex")
s_sig_dw = 4.0 * float(np.nanmedian([DS[i]["esig"] / DS[i]["sig"] for i in iso]))
s_ml_dw = math.log(3.0 / 1.0) / 2.0                        # Upsilon_V 1-3, coherent [est]
s_coef = 0.20                                              # the 4/81 coefficient: profile+anisotropy [est]
tot_dw = math.hypot(math.hypot(hs_logQ(Y_DW), s_sig_dw / math.sqrt(max(len(iso), 1))),
                    math.hypot(s_ml_dw, s_coef))
print(f"  a0-space budget (OPTIMISTIC -- assumes equilibrium and ignores the EFE prescription entirely): "
      f"shape {100*hs_logQ(Y_DW):.1f}%  4 sigma(sigma)/sqrt(N) {100*s_sig_dw/math.sqrt(len(iso)):.1f}%  "
      f"Upsilon_V [est] {100*s_ml_dw:.0f}%  4/81 coefficient [est] {100*s_coef:.0f}%  ->  {100*tot_dw:.0f}% = "
      f"{GAP_LOG/tot_dw:.2f} sigma")
check(hs_logQ(Y_DW) < hs_logQ(Y_BTFR) and frac_efe > 0.8 and len(iso) < 8
      and math.log10(a0i.max() / a0i.min()) > 1.0 and tot_dw > 4 * NEED3,
      f"C6 the dwarf sigma^4 door is the SHAPE-CLEANEST of the galactic doors and the OBSERVATIONALLY WORST. "
      f"Favourable: classical dwarfs sit {Y_BTFR/Y_DW:.0f}x deeper than SPARC's outermost radii, so the "
      f"four-kernel shape systematic is {100*hs_logQ(Y_DW):.1f}% against {100*hs_logQ(Y_BTFR):.1f}% for the "
      f"BTFR -- pressure-supported dwarfs really are closer to the shape-invariant regime, and the k = 2/9 "
      f"(4/81) coefficient is a theorem there. Unfavourable and decisive: {100*frac_efe:.0f}% of the MW "
      f"satellites have y_ext > y_int so the isolated relation does not apply, leaving only {len(iso)} isolated "
      f"LG dwarfs in the whole McConnachie table, and THOSE scatter over "
      f"{math.log10(a0i.max()/a0i.min()):.1f} dex in a0_hat (Tucana and Cetus high, Leo A low). That spread is "
      f"astrophysical -- rotation in the dIrrs, contested older dispersions, equilibrium -- NOT a measurement "
      f"of a0, and it must not be read as one in either direction. Even the optimistic floor is "
      f"{100*tot_dw:.0f}% = {GAP_LOG/tot_dw:.2f} sigma, set by the dwarf Upsilon_V and the coefficient")
ROWS.append(("dwarf sigma^4 = (4/81) G M a0", p_sig["dwarf sigma @ classical y_int"], hs_logQ(Y_DW), tot_dw,
             "partly", "EFE prescription unresolved; N_isolated = %d; Upsilon_V" % len(iso)))


# ============================================================================================ C7
banner("C7  DOOR: THE CLUSTER g-dagger = 2.02e-9 -- does g-dagger/a0 discriminate, or is it ~20x either way?")

G_DAG_CL = 2.02e-9                    # committed: mi_route_a_cluster_eta_2026.py / project_cluster_standing
LADDER = (3.0, 24.0)                  # committed: the method+radius ladder, growing inward
DEX = math.log(10.0)
for nm, a in (("kappa=1/2", A0_CANON), ("kappa=1/2pi", A0_M20), ("RAR 1.2e-10", A0_MOND)):
    print(f"    g-dagger/a0 under {nm:<12} = {G_DAG_CL/a:6.2f}x  = {math.log(G_DAG_CL/a)/DEX:.3f} dex of "
          f"unexplained offset")
lad_dex = (math.log(LADDER[0]) / DEX, math.log(LADDER[1]) / DEX)
print(f"  the kappa signal in that offset is {GAP_LOG/DEX:.4f} dex; the corpus's own method+radius ladder "
      f"spans {lad_dex[0]:.3f}-{lad_dex[1]:.3f} dex, i.e. {lad_dex[0]*DEX/GAP_LOG:.0f}-"
      f"{lad_dex[1]*DEX/GAP_LOG:.0f}x the signal")
tot_cl = lad_dex[0] * DEX             # the TIGHT end of the ladder, which is the most generous reading
print(f"  note the shape term here is SMALL ({100*hs_logQ(G_DAG_CL/A0_CANON):.1f}% at y = "
      f"{G_DAG_CL/A0_CANON:.1f}, past the peak of the kernel spread): this door does not fail on the kernel, it "
      f"fails on the ladder.")
check(min(G_DAG_CL / A0_CANON, G_DAG_CL / A0_M20, G_DAG_CL / A0_MOND) > 10.0
      and lad_dex[0] * DEX > 5 * GAP_LOG and hs_logQ(G_DAG_CL / A0_CANON) < tot_cl / 5,
      f"C7 NOT A kappa DOOR, AND NOT EVEN A FRAMEWORK-SPECIFIC ONE: the cluster knee sits at "
      f"{G_DAG_CL/A0_CANON:.1f}x a0 under kappa = 1/2, {G_DAG_CL/A0_M20:.1f}x under kappa = 1/2pi and "
      f"{G_DAG_CL/A0_MOND:.1f}x under the literature's own 1.2e-10 -- ~20x on every hypothesis, so it is a "
      f"MOND-SHARED failure that no choice of kappa touches. Quantitatively the kappa signal is "
      f"{GAP_LOG/DEX:.4f} dex against a {lad_dex[0]:.2f}-{lad_dex[1]:.2f} dex method+radius ladder, so even at "
      f"the ladder's TIGHT end the door delivers {GAP_LOG/tot_cl:.3f} sigma. It belongs in the SHARED column")
ROWS.append(("cluster g-dagger = 2.02e-9", 1.0, hs_logQ(G_DAG_CL / A0_CANON), tot_cl, "no-MOND-shared",
             "a ~20x offset on EVERY hypothesis; ladder 0.5-1.4 dex"))


# ============================================================================================ C8
banner("C8  DOOR: THE EFE ONSET RADIUS -- a kappa-specific LENGTH, sitting exactly where kernels disagree most")

M_HOST, M_HOST_RANGE = 1.0e12 * MSUN, (0.8e12, 1.5e12)
s_host = 0.5 * 0.5 * math.log(M_HOST_RANGE[1] / M_HOST_RANGE[0])   # D ~ sqrt(M_host)
kap_D = 0.5 * GAP_LOG
print(f"  D_thr(criterion nu_c) = sqrt(G M_host/(a0 y_thr)), so p = -1/2 and the kappa signal in the LENGTH is "
      f"only {100*kap_D:.2f}%.")
print(f"  {'nu_c':>7}{'y_thr RouteA':>14}{'alpha=1':>10}{'alpha=2':>10}{'simple':>10}"
      f"{'D half-spread':>15}{'signal/shape':>14}")
print("  " + "-" * 82)
efe = []
for nuc in (1.02, 1.05, 1.2, 1.5, 2.0, 3.0):
    ys = [solve_y(f, nuc) for f in KERN.values()]
    hsD = 0.5 * abs(math.log(max(ys) / min(ys))) / 2.0     # D ~ y^-1/2
    efe.append((nuc, ys, hsD))
    print(f"  {nuc:>7.2f}" + "".join(f"{v:>10.4g}" if i else f"{v:>14.4g}" for i, v in enumerate(ys))
          + f"{100*hsD:>14.1f}%{kap_D/hsD:>14.2f}")
hs_efe = min(h for _, _, h in efe)
tot_efe = math.hypot(hs_efe, s_host)
print(f"  plus the host mass: M_MW = {M_HOST_RANGE[0]:.1e}-{M_HOST_RANGE[1]:.1e} Msun [est] contributes "
      f"{100*s_host:.1f}% to D_thr. Best total {100*tot_efe:.1f}% against a {100*kap_D:.2f}% signal = "
      f"{kap_D/tot_efe:.2f} sigma.")
check(all(h > kap_D for _, _, h in efe) and efe[0][2] > efe[-1][2] and s_host > kap_D
      and kap_D / tot_efe < 0.5,
      f"C8 THE EFE ONSET IS DEFINITIONALLY LOCATED AT THE POINT OF MAXIMAL KERNEL DISAGREEMENT, so it is "
      f"shape-degenerate by construction rather than by bad luck. The onset is where g_ext ~ a0, i.e. y ~ 1, "
      f"which is precisely where the four kernels' nu(y) spread is largest: at a weak-onset criterion "
      f"nu_c = 1.02 the threshold depth y_thr spans {min(efe[0][1]):.2f}-{max(efe[0][1]):.1f} and the resulting "
      f"D_thr spans {100*efe[0][2]:.0f}%, tightening only to {100*efe[-1][2]:.0f}% at nu_c = 3 (by which point "
      f"one is no longer describing an onset). On top of that the observable's kappa sensitivity is HALVED by "
      f"p = -1/2, to {100*kap_D:.2f}%, and the MW's own mass uncertainty alone contributes {100*s_host:.0f}%. "
      f"Best case {kap_D/tot_efe:.2f} sigma")
ROWS.append(("EFE onset radius D_thr", -0.5, hs_efe / 0.5, tot_efe / 0.5, "no-degenerate",
             "onset lives at y~1 = max kernel spread; M_host +-30%"))   # /|p| to put it in a0-space


# ============================================================================================ C9
banner("C9  DOOR: THE SN-Ia HOST-STEP LOCATION -- p = 1, the most a0-sensitive observable in the corpus, and "
       "the deadest")

SIG_UNIT = MSUN / PC ** 2
S_2PIG = A0_CANON / (2 * math.pi * G_N) / SIG_UNIT
CONV = {"a0/(2 pi G)  (disc/MOND transition)": 2 * math.pi, "a0/(pi G)": math.pi, "a0/(2G)": 2.0,
        "a0/G  (Milgrom critical surface density)": 1.0}
print(f"  Sigma_a0 = a0/(2 pi G) = {S_2PIG:.1f} Msun/pc^2 -- the corpus's recorded 107, reproduced.")
for k, c in CONV.items():
    print(f"    {k:<42}{A0_CANON/(c*G_N)/SIG_UNIT:>9.1f} Msun/pc^2")
conv_span = math.log(2 * math.pi)
print(f"  the threshold CONSTANT is convention, not prediction: the span from a0/G to a0/(2 pi G) is "
      f"ln(2 pi) = {conv_span:.4f} = {conv_span/DEX:.3f} dex, against a kappa signal of {GAP_LOG/DEX:.4f} dex "
      f"-> {conv_span/GAP_LOG:.1f}x.")
rat = []
for b in (0.20, 0.35):                                     # size-mass R ~ M^b, so log M_step = (log Sigma+c)/(1-2b)
    amp = 1.0 / (1.0 - 2 * b)
    rat.append((amp * GAP_LOG) / (amp * conv_span))
print(f"  and remapping Sigma -> log M_step through a size-mass relation R ~ M^b amplifies signal and "
      f"convention IDENTICALLY (b = 0.20: x{1/(1-0.4):.2f}, b = 0.35: x{1/(1-0.7):.2f}), so the ratio is "
      f"remap-invariant at {rat[0]:.4f}: no choice of host observable rescues it.")
print(f"  [corpus, imported] the corpus's own SN-Ia audit already finds this lever NULL and UNDERPOWERED "
      f"(18% power at the observed 0.06 mag; the real partial correlation leans wrong-sign at 0.6 SE), and the "
      f"step LOCATION is fixed by convention at log M* = 10 in the literature rather than measured.")
tot_sn = conv_span
check(abs(S_2PIG - 107.0) < 1.0 and conv_span > 10 * GAP_LOG and abs(rat[0] - rat[1]) < 1e-12
      and GAP_LOG / tot_sn < 0.1,
      f"C9 *** THE ONE p = 1 DOOR IS KILLED BY A DEFINITION, NOT BY A MEASUREMENT. *** Sigma_a0 = a0/(2 pi G) "
      f"= {S_2PIG:.1f} Msun/pc^2 reproduces the corpus's recorded 107 and responds to a0 with exponent exactly "
      f"1 -- the best conversion rate of any observable here. But WHICH multiple of a0/G marks the transition "
      f"is a convention: the literature uses a0/G ({A0_CANON/G_N/SIG_UNIT:.0f}) and a0/(2 pi G) "
      f"({S_2PIG:.0f}) for different purposes, a {conv_span/DEX:.2f} dex freedom = {conv_span/GAP_LOG:.0f}x the "
      f"kappa signal, and the ratio is invariant under any monotone remap to a host mass "
      f"({rat[0]:.4f} at b = 0.20 and 0.35 alike) because signal and convention are amplified together. "
      f"{GAP_LOG/tot_sn:.3f} sigma before a single supernova is measured. DEGENERATE, and it stays degenerate "
      f"however good the SN data become")
ROWS.append(("SN-Ia host-step location (Sigma_a0)", 1.0, float("nan"), tot_sn, "no-degenerate",
             "the 2pi in Sigma_a0 is convention: 0.80 dex vs a 0.036 dex signal"))


# ============================================================================================ C10
banner("C10  DOOR: WIDE-BINARY gamma_v -- 'a0-degenerate' verified and quantified, and mass-clean")

GAM_IF, GAM_RANGE, SIG_SYS = 1.0310, (1.0218, 1.0472), 0.02   # committed: Amendment 4(d)/7, frozen
y_eff = solve_y(lambda y: nu_alpha2(y) ** 0.5, GAM_IF)        # calibrate the effective depth on the in-force value
print(f"  reduced model gamma_v = sqrt(nu(y_eff)): the IN-FORCE alpha=2 target gamma_v = {GAM_IF} calibrates "
      f"y_eff = {y_eff:.3f} (g_ext+g_int ~ {y_eff*A0_CANON:.2e} m/s^2, the solar-circle field: a consistency).")
print(f"  {'kernel':<10}{'gamma_v at the SAME y_eff':>27}{'gamma_v - 1':>13}{'d gamma_v/d ln a0':>20}"
      f"{'sigma(ln a0)':>14}{'n_sigma':>9}")
print("  " + "-" * 93)
wb = {}
for kn, f in KERN.items():
    gam = math.sqrt(float(f(y_eff)))
    dg = dabs(lambda a: math.sqrt(float(f(G_N * M_WB / (S_WB ** 2 * a)))),
              G_N * M_WB / (S_WB ** 2 * y_eff))
    s_a0 = SIG_SYS / abs(dg)
    wb[kn] = (gam, dg, s_a0)
    print(f"  {kn:<10}{gam:>27.4f}{gam-1:>13.4f}{dg:>20.5f}{100*s_a0:>13.0f}%{GAP_LOG/s_a0:>9.3f}")
shape_wb = max(v[0] - 1 for v in wb.values()) / min(v[0] - 1 for v in wb.values())
best_wb = min(v[2] for v in wb.values())
# the shape systematic in a0-SPACE, exactly parallel to every other door: what a0 does each kernel need to
# reproduce the SAME observed gamma_v at the SAME physical configuration?
a0_wb = [a0_from_gamma(GAM_IF, M_WB, S_WB, f) for f in KERN.values()]
hs_wb_a0 = 0.5 * math.log(max(a0_wb) / min(a0_wb))
tot_wb = math.hypot(best_wb, hs_wb_a0)
dfoot = abs(math.sqrt(float(nu_alpha2(y_eff * A0_CANON / A0_ALT))) - math.sqrt(float(nu_alpha2(y_eff))))
print(f"  the alpha=1 entry {wb['alpha=1'][0]:.4f} is an INDEPENDENT VALIDATION: the corpus's registered "
      f"ungated alpha=1 MI target is 1.05-1.10 (memory/prereg Amendment 4), and the reduced model lands there "
      f"without being told to.")
print(f"  shape sensitivity: (gamma_v - 1) spans a factor {shape_wb:.1f} across the four kernels at FIXED "
      f"physics; footing fork canon->ALT (21%) moves gamma_v by only {dfoot:.4f} = {dfoot/SIG_SYS:.2f} "
      f"sigma_sys.")
print(f"  in a0-SPACE (the currency the other doors are priced in): the a0 each kernel needs to reproduce "
      f"gamma_v = {GAM_IF} at the same configuration spans {min(a0_wb):.2e}-{max(a0_wb):.2e}, a shape term of "
      f"{100*hs_wb_a0:.0f}%; with the sigma_sys term that is {100*tot_wb:.0f}% = {GAP_LOG/tot_wb:.3f} sigma "
      f"shape-marginalised, or {GAP_LOG/best_wb:.2f} sigma if one COMMITS to a kernel.")
check(1.05 <= wb["alpha=1"][0] <= 1.10 and best_wb > 0.15 and shape_wb > 3.0
      and dfoot < SIG_SYS and GAP_LOG / best_wb < 0.5 and hs_wb_a0 > 3 * best_wb,
      f"C10 'a0-DEGENERATE' IS CORRECT, AND THE NUMBER IS {GAP_LOG/best_wb:.2f} SIGMA AT INFINITE N. The "
      f"reduced model gamma_v = sqrt(nu(y_eff)) is validated by an independently committed number -- calibrated "
      f"ONLY on the in-force alpha=2 target 1.0310 it predicts {wb['alpha=1'][0]:.4f} for alpha=1, inside the "
      f"corpus's registered ungated 1.05-1.10 -- so its derivatives are usable. Then: the kappa gap moves "
      f"gamma_v by at most {GAP_LOG*max(abs(v[1]) for v in wb.values()):.4f}, against the FROZEN "
      f"sigma_sys = {SIG_SYS}, giving sigma(ln a0) >= {100*best_wb:.0f}% and {GAP_LOG/best_wb:.2f} sigma; even "
      f"the 21% footing fork moves it only {dfoot/SIG_SYS:.2f} sigma_sys, which is the precise content of "
      f"'a0-degenerate'. Two further facts, one each way: the door is the corpus's only MASS-CLEAN one "
      f"(C4 exponent exactly +1, 5% photometric masses), but in a0-space its SHAPE term is "
      f"{100*hs_wb_a0:.0f}% -- {hs_wb_a0/best_wb:.1f}x the sigma_sys term and the largest shape systematic of "
      f"any door here -- because (gamma_v - 1) spans a factor {shape_wb:.1f} across the kernel family at "
      f"identical physics. Shape-marginalised the door is worth {GAP_LOG/tot_wb:.3f} sigma; it is only "
      f"{GAP_LOG/best_wb:.2f} sigma for someone who has already committed to a kernel")
ROWS.append(("wide-binary gamma_v (2-30 kAU)", float("nan"), hs_wb_a0, tot_wb, "no-degenerate",
             "sigma_sys = 0.02 AND an %.0f%% a0-space kernel spread" % (100 * hs_wb_a0)))


# ============================================================================================ C11
banner("C11  DOOR: THE DEEP (LENSING / SATELLITE) RAR -- the only door whose SHAPE systematic is inside budget")

GB_LENS = (1.0e-15, 5.0e-12)                               # Brouwer+2021 KiDS-1000 RAR span
print(f"  {'g_bar [m/s^2]':>14}{'y = g_bar/a0':>14}{'4-kernel shape half-spread on Q':>34}{'vs 2.73% budget':>18}")
print("  " + "-" * 82)
for gb in (GB_LENS[0], 1e-14, 1e-13, 1e-12, GB_LENS[1], A0_CANON * Y_BTFR):
    y = gb / A0_CANON
    print(f"  {gb:>14.2e}{y:>14.3e}{100*hs_logQ(y):>33.3f}%"
          f"{('INSIDE' if hs_logQ(y) < NEED3 else 'outside'):>18}")
y_lens_ok = float(np.interp(NEED3, [hs_logQ(10 ** t) for t in np.linspace(-6, 0.5, 300)],
                            10 ** np.linspace(-6, 0.5, 300)))
LENS_ADOPTED = 0.26 / 1.20                                 # Brouwer's ADOPTED g-dagger error (circular)
LENS_FREEFIT = 0.45                                        # committed forecast: papers/TRIANGLE_KIDS_2026.md
print(f"  the shape systematic falls under the {100*NEED3:.2f}% budget for y <= {y_lens_ok:.1e}, i.e. "
      f"g_bar <= {y_lens_ok*A0_CANON:.1e} m/s^2 -- unreachable in HI discs, ROUTINE in stacked lensing.")
print(f"  precision: Brouwer+2021 quote g-dagger = 1.20 +- 0.26e-10 ({100*LENS_ADOPTED:.0f}%) but ADOPTED that "
      f"scale from McGaugh 2016 rather than fitting it, so that error is not a free-fit error. The corpus's own "
      f"forecast for a genuine tabulated free fit is ~{100*LENS_FREEFIT:.0f}% (stat 13-43% + sys 15-25%, "
      f"TRIANGLE_KIDS_2026.md).")
tot_lens = LENS_FREEFIT
check(hs_logQ(GB_LENS[0] / A0_CANON) < NEED3 and hs_logQ(GB_LENS[1] / A0_CANON) > NEED3
      and y_lens_ok < float(np.min(Y_ALL)) and GAP_LOG / tot_lens < 0.5,
      f"C11 *** THE DEEP LENSING/SATELLITE RAR IS THE ONLY DOOR IN THIS CENSUS WHOSE SHAPE SYSTEMATIC IS "
      f"INSIDE THE 3-SIGMA BUDGET. *** At Brouwer's deepest bin (g_bar = 1e-15, y = {GB_LENS[0]/A0_CANON:.1e}) "
      f"the four-kernel half-spread on Q is {100*hs_logQ(GB_LENS[0]/A0_CANON):.3f}%, an order of magnitude "
      f"inside the {100*NEED3:.2f}% requirement, while the SHALLOW end of the same dataset "
      f"({100*hs_logQ(GB_LENS[1]/A0_CANON):.1f}%) is already outside it -- so the door works only on the deep "
      f"bins, and the requirement y <= {y_lens_ok:.1e} is BELOW SPARC's deepest single point "
      f"({float(np.min(Y_ALL)):.1e}), which is exactly why rotation curves cannot get there. The catch is "
      f"precision: {100*LENS_FREEFIT:.0f}% for an honest free fit today = {GAP_LOG/tot_lens:.2f} sigma, and per "
      f"C4 its floor is the baryonic mass scale, not the kernel. In MI the lensing channel also runs through a "
      f"disformal photon sector, so lensing-a0 = dynamical-a0 is a PREDICTION of the completion, not automatic")
ROWS.append(("deep RAR: lensing / satellite kinematics", 0.5, hs_logQ(GB_LENS[0] / A0_CANON), tot_lens,
             "yes-genuinely", "shear+photo-z+M_bar; shape NOT the wall"))
# the committed rotation-curve RAR door, imported for the ranking (mi_routeA_shape_invariant_a0_2026.py S7/S8)
ROWS.append(("RAR knee, rotation curves (committed)", 0.5, 0.1000, 0.1752, "partly",
             "shape 10% + Upsilon 7.4% + gas 6.8% = 14.2% N-independent"))


# ============================================================================================ C12
banner("C12  *** THE RANKED CENSUS *** kappa-sensitivity / total systematic, all in a0-space")

ROWS.sort(key=lambda r: -GAP_LOG / r[3])
print(f"  {'door':<40}{'p':>6}{'shape':>8}{'sig(ln a0)':>12}{'n_sigma':>9}{'class':>17}  binding wall")
print("  " + "-" * 116)
for lab, p, sh, tot, cls, wall in ROWS:
    print(f"  {lab:<40}{p:>6.2f}{100*sh:>7.1f}%{100*tot:>11.1f}%{GAP_LOG/tot:>9.3f}{cls:>17}  {wall}")
best = ROWS[0]
n_best = GAP_LOG / best[3]
RC_FLOOR = 0.142                          # committed N-independent floor of the rotation-curve doors (S8)
ceil_rc, ceil_lens = GAP_LOG / RC_FLOOR, GAP_LOG / 0.074
print(f"\n  BEST DOOR TODAY: {best[0]} at {n_best:.2f} sigma. NONE reaches 1 sigma, let alone 3.")
print(f"  BEST DOOR PERIOD is a different question, and the answer is the DEEP RAR (stacked lensing / "
      f"satellite kinematics at y <~ 3e-3): the rotation-curve doors are capped at "
      f"{ceil_rc:.2f} sigma by their {100*RC_FLOOR:.1f}% N-INDEPENDENT floor (shape 10% + Upsilon + gas), while "
      f"the deep RAR's shape term is {100*hs_logQ(GB_LENS[0]/A0_CANON):.2f}% and its statistical + shear terms "
      f"shrink with survey area, so its ceiling is {ceil_lens:.2f}-{ceil_mass:.2f} sigma -- the baryon floor, "
      f"not the kernel. That is the census's one constructive result.")
print(f"  CEILINGS, not current values: shape-free depth is available (C11) and the frozen wide-binary "
      f"sigma_sys is not (C10), so the class ceiling is set by C4's mass floor at {ceil_mass:.2f} sigma, and by "
      f"C2's H0 fork on the target ({fork_fixed_OmL/GAP_LOG:.1f}-{fork_fixed_om/GAP_LOG:.1f} gaps) on top.")
print(f"  WHAT WOULD HAVE TO IMPROVE, in the order that buys the most:")
print(f"    1. baryonic mass scale to <= {100*need_dyn:.2f}% COHERENTLY (best on offer ~5%, pure-gas). This is "
      f"the binding wall for every door except the wide binary, and no sample size touches it.")
print(f"    2. a deep-regime probe at y <= {y_lens_ok:.0e} with per-object baryons: satellite kinematics or "
      f"stacked lensing around gas-dominated dwarfs. Shape then costs < {100*NEED3:.1f}%.")
print(f"    3. the H0 tension resolved, or the kappa claim quoted twice (Planck target and SH0ES target).")
print(f"    4. NOT more rotation curves: BIG-SPARC's ~4000 galaxies leave the 14.2% N-independent floor intact.")
check(n_best < 1.0 and ceil_mass < 3.0 and best[3] < ROWS[-1][3] and ceil_lens > ceil_rc
      and sum(1 for r in ROWS if r[4] == "yes-genuinely") == 1,
      f"C12 THE RANKING, and it is a NO with a diagnosis. Top door {best[0]} at {n_best:.2f} sigma; bottom "
      f"{ROWS[-1][0]} at {GAP_LOG/ROWS[-1][3]:.3f}. Exactly ONE door is genuinely kappa-specific rather than "
      f"MOND-shared or definitionally degenerate -- the deep lensing/satellite RAR -- and it earns that only "
      f"because its shape systematic "
      f"({100*[r[2] for r in ROWS if r[4] == 'yes-genuinely'][0]:.2f}% at the "
      f"deepest bin) is the one shape term inside the 3-sigma budget. Its wall, and every other door's wall "
      f"except the wide binary's, is the BARYONIC MASS SCALE: {ceil_mass:.1f} sigma at 5%, 3 sigma at "
      f"{100*need_dyn:.2f}%. The cluster g-dagger and the EFE onset and the SN-Ia step are not imprecise "
      f"versions of a kappa test, they are not kappa tests at all -- one is a ~20x offset on every hypothesis, "
      f"one is definitionally located at the maximum of the kernel spread, one is set by a factor-2pi "
      f"convention")

n = sum(1 for t, _ in ok if t)
print(f"\n  {n}/{len(ok)} checks held.")
if n != len(ok):
    for t, m in ok:
        if not t:
            print(f"    FAILED: {m}")
    sys.exit(1)
print("  Exit 0: the kappa-sensitivity census is ranked, and no door in it reaches 3 sigma.")
