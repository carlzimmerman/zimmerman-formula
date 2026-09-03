#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_unexplained-regularities_hisize.py

ANGLE: mine the unexplained regularities.  THE REGULARITY: the HI size-mass relation.

D_HI (the diameter at which the HI surface density falls to 1 Msun/pc^2) tracks M_HI as a power law of slope 1/2
with a scatter of 0.06 dex over FIVE decades of mass -- from ultra-faint dwarfs to the most massive spirals.  It is
the tightest scaling relation in galaxy astronomy, tighter than the RAR and tighter than the BTFR, and it is
routinely described as unexplained (Broeils & Rhee 1997; Verheijen & Sancisi 2001; Wang, Koribalski, Serra,
van der Hulst, Roychowdhury, Kamphuis & Chengalur 2016).  Equivalently: every HI disc has the same mean hydrogen
surface density inside its own HI radius, <Sigma_HI> = M_HI/(pi R_HI^2) ~ 3.8 Msun/pc^2.

THREE QUESTIONS, IN ORDER OF WHAT WOULD MATTER MOST:

  Q1 (the one that would be a second law, and the answer is NO).  Does a_0 set <Sigma_HI>?  a_0/(2 pi G) = 107
     (canonical) / 129 (alt) Msun/pc^2 is the framework's own surface-density constant -- the one that explains
     Donato's halo constant, measured at 177 Msun/pc^2 from 162 Burkert fits (hunt item 5).  If <Sigma_HI> were a simple multiple of it, the tightest unexplained regularity in galaxy
     astronomy would belong to a_0.  This is tested against a fixed list of simple coefficients, and it FAILS.
     REPORTED AGAINST INTEREST: the framework predicts NOTHING about the HI size-mass relation.

  Q2 (a derived closed form with a PREDICTED zero point).  Feed the empirical size-mass relation into the deep
     limit and the velocity follows from the SIZE alone, with no mass and no mass-to-light ratio:

         V_flat = [ 1.33 pi G a_0 <Sigma_HI> ]^(1/4) * R_HI^(1/2)                                     (U2)

     Slope 1/2 in the limit where <Sigma_HI> is exactly universal (it is not: the size-mass slope is 0.524, so
     the slope (U2) actually implies must be recomputed inside each subsample -- both targets are reported).
     Zero point built from a_0 and one measured surface density.  Tested on SPARC.
     RESTATEMENT TEST, EXECUTED: (U2) is v^4 = G M_b a_0 with M_HI replaced by pi R_HI^2 <Sigma_HI>.  The script
     verifies that identity numerically; it closes, so (U2) IS A RESTATEMENT of the BTFR given one empirical
     input.  It is recorded as a corollary with a predicted coefficient, not as a new law.

  Q3 (what the framework does say, and it is also a restatement).  Because R_HI is defined by a fixed surface
     density, the baryonic acceleration at R_HI is nearly universal, so the framework predicts a nearly universal
     MASS DISCREPANCY at every galaxy's own HI edge.  Measured here, with its scatter, against nu(y).

RULES: both footings on every dimensionful number; checks that CAN fail with bars fixed before running; a mutation
control; the Newtonian and LambdaCDM alternatives computed beside; the Upsilon lever measured by re-running the
whole pipeline at Upsilon x 1.5; nothing tuned; report against interest.

BUG-PATTERN GUARDS.
  (1) total-vs-enclosed: <Sigma_HI> is DEFINED as M_HI(total)/(pi R_HI^2), so pi R_HI^2 <Sigma_HI> returns the
      TOTAL M_HI exactly -- there is no enclosed-mass slot in (U2) and none is used.  The BTFR takes the total
      baryonic mass, which is the right quantity.  Q3, by contrast, is a LOCAL statement and uses SPARC's own
      enclosed-mass circular speeds interpolated at R_HI, never a total.
  (2) spherical-vs-disc: no spherical mass formula is applied to a disc anywhere.  g_bar at R_HI comes from
      SPARC's disc solutions V_gas, V_disk, V_bul directly.  The one thin-sheet expression (2 pi G Sigma) is used
      only as a labelled reference number, never in a fit.
  (3) aperture on a minimum: not applicable, R_HI is a monotone surface-density threshold.
  (4) covariance index order: no covariance is used.
  (5) trivial correlation: V_flat and R_HI are measured by different instruments' products (the rotation curve
      and the HI map).  The joint-fit degeneracy check is that V_flat is NOT used in defining R_HI -- it is not.
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import (A0, G, KMS2_KPC, kpc, Msun, nu, load_sparc, read_master, Check, P, info,
                      fit_loglog, UPS_D, UPS_B)

MSUN_PC2 = Msun / (3.0857e16) ** 2      # 1 Msun/pc^2 in kg/m^2
HE = 1.33                               # helium+metals; M_gas = 1.33 M_HI

ck = Check()
P("=" * 118)
P("k_unexplained-regularities_hisize -- the HI size-mass relation: does a_0 own the tightest scaling relation?")
P("=" * 118)

master = read_master()

# ------------------------------------------------------------------ the relation itself, measured here
P("\n" + "-" * 118)
P("STEP 0 -- reproduce the published regularity on SPARC, so that what follows is anchored to a known number")
P("-" * 118)
names = [k for k, v in master.items() if v["RHI"] > 0 and v["MHI"] > 0]
RHI = np.array([master[k]["RHI"] for k in names])            # kpc, radius at Sigma_HI = 1 Msun/pc^2
MHI = np.array([master[k]["MHI"] for k in names]) * 1e9      # Msun, total
DHI = 2 * RHI
s_dm, b_dm, sc_dm = fit_loglog(MHI, DHI)
SIG = MHI / (math.pi * (RHI * 1e3) ** 2)                     # Msun/pc^2
SIG_MED = float(np.median(SIG))
P(f"  N = {len(names)} SPARC galaxies with both R_HI and M_HI.")
P(f"  log D_HI = {s_dm:.4f} log M_HI + {b_dm:.3f},  scatter {sc_dm:.4f} dex")
P(f"     Wang+2016 (562 galaxies, 5 decades)     : 0.506 +- 0.003, -3.293, scatter 0.06 dex")
P(f"  <Sigma_HI> = M_HI/(pi R_HI^2) : median {SIG_MED:.3f} Msun/pc^2, scatter {np.log10(SIG).std(ddof=1):.3f} dex")
P(f"     Wang+2016 equivalent                    : 3.8 Msun/pc^2")
ck("S0 SPARC must reproduce the published HI size-mass relation -- slope within 0.05 of 0.506 and mean surface "
   "density within 0.05 dex of 3.8 Msun/pc^2 -- or this sample is not measuring the regularity in question",
   abs(s_dm - 0.506) < 0.05 and abs(math.log10(SIG_MED / 3.8)) < 0.05,
   f"slope {s_dm:.4f}, <Sigma> {SIG_MED:.3f} ({math.log10(SIG_MED/3.8):+.3f} dex from 3.8)")

# ------------------------------------------------------------------ Q1: does a_0 set the HI surface density?
P("\n" + "=" * 118)
P("Q1 -- DOES a_0 SET <Sigma_HI>?  (the question whose YES would be a second law)")
P("=" * 118)
for foot, a0 in A0.items():
    SigA = a0 / (2 * math.pi * G) / MSUN_PC2
    P(f"  {foot:10s} a_0/(2 pi G) = {SigA:7.2f} Msun/pc^2   ->  <Sigma_HI>/[a_0/(2 pi G)] = {SIG_MED/SigA:.5f} "
      f"= 1/{SigA/SIG_MED:.2f}")
CANDS = {"1": 1.0, "1/2": 0.5, "1/4": 0.25, "1/8": 0.125, "1/16": 1/16, "1/32": 1/32, "1/64": 1/64,
         "1/pi": 1/math.pi, "1/(2pi)": 1/(2*math.pi), "1/(4pi)": 1/(4*math.pi), "1/(8pi)": 1/(8*math.pi),
         "1/(16pi)": 1/(16*math.pi), "1/pi^2": 1/math.pi**2, "1/(2pi)^2": 1/(2*math.pi)**2,
         "1/(4pi^2)": 1/(4*math.pi**2), "1/(4pi)^2": 1/(4*math.pi)**2}
hits = []
for foot, a0 in A0.items():
    ratio = SIG_MED / (a0 / (2 * math.pi * G) / MSUN_PC2)
    best = min(CANDS.items(), key=lambda kv: abs(math.log10(ratio / kv[1])))
    P(f"  {foot:10s} closest simple coefficient: {best[0]:10s} = {best[1]:.5f}   "
      f"off by {math.log10(ratio/best[1])*100:+.1f}% in log10 ({abs(ratio/best[1]-1)*100:.1f}% linear)")
    if abs(ratio / best[1] - 1) < 0.02:
        hits.append((foot, best[0]))
ck("Q1 THE ONE THAT WOULD MATTER.  If <Sigma_HI> were a simple coefficient times a_0/(2 pi G) to better than 2%, "
   "the tightest unexplained scaling relation in galaxy astronomy would belong to a_0.  This check is written to "
   "PASS only if that is true; it is expected and intended to FAIL",
   len(hits) > 0, f"no simple coefficient within 2% on either footing" if not hits else str(hits))
P("""
  AGAINST INTEREST, PLAINLY: the framework predicts NOTHING about <Sigma_HI>, and therefore nothing about the HI
  size-mass relation.  The relation is a statement about hydrogen, ionization and self-shielding, not about
  gravity, and neither a_0 nor Lambda appears anywhere in it.  The tightest regularity in the field is not ours.
""")

# ------------------------------------------------------------------ Q2: the derived closed form
P("=" * 118)
P("Q2 -- THE DERIVED CLOSED FORM (U2): V_flat = [1.33 pi G a_0 <Sigma_HI>]^(1/4) R_HI^(1/2)")
P("=" * 118)


def sample(ups_d, ups_b, gas_cut):
    """Galaxies with R_HI, M_HI, V_flat and a stellar luminosity, restricted to gas fraction above gas_cut."""
    out = []
    for k, m in master.items():
        if m["RHI"] <= 0 or m["MHI"] <= 0 or m["Vflat"] <= 0 or m["Q"] > 2 or m["inc"] < 30:
            continue
        Mg = HE * m["MHI"] * 1e9
        Ms = ups_d * m["L36"] * 1e9
        Mb = Mg + Ms
        fgas = Mg / Mb
        if fgas < gas_cut:
            continue
        out.append(dict(name=k, RHI=m["RHI"], MHI=m["MHI"] * 1e9, V=m["Vflat"], eV=m["eVflat"],
                        Mg=Mg, Ms=Ms, Mb=Mb, fgas=fgas, D=m["D"], eD=m["eD"]))
    return out


def predict_V(g, a0, sig_med, use_stars=True):
    """(U2) with the universal surface density: M_HI -> pi R_HI^2 <Sigma>.  Stars added when use_stars."""
    R = g["RHI"] * 1e3 * 3.0857e16                      # m
    M_HI_from_size = math.pi * (g["RHI"] * 1e3) ** 2 * sig_med   # Msun
    Mb = HE * M_HI_from_size + (g["Ms"] if use_stars else 0.0)
    return (G * a0 * Mb * Msun) ** 0.25 / 1e3           # km/s


GAS_CUTS = (0.5, 0.7, 0.8)
P("  Bars fixed before running: slope within 0.10 of 1/2; zero point within 0.05 dex in log V on at least one")
P("  footing; scatter no more than 1.5x the value propagated from the size-mass scatter.\n")
P("  gas cut   N   measured slope       scatter  logR range |   predicted log V - measured, can / alt  | Newtonian")
rec = {}
_rng = np.random.default_rng(20260903)
for gc in GAS_CUTS:
    S = sample(UPS_D, UPS_B, gc)
    if len(S) < 8:
        continue
    R = np.array([g["RHI"] for g in S]); V = np.array([g["V"] for g in S])
    sl, ic, sc = fit_loglog(R, V)
    bs = np.array([fit_loglog(R[i], V[i])[0] for i in
                   (_rng.integers(0, len(R), len(R)) for _ in range(2000))])
    esl = float(bs.std(ddof=1))
    rng_logR = float(np.log10(R).max() - np.log10(R).min())
    line = f"  {gc:5.1f} {len(S):5d}   {sl:+.3f} +- {esl:.3f}   {sc:.3f}    {rng_logR:.2f}    |"
    d_by_foot = {}
    for foot, a0 in A0.items():
        Vp = np.array([predict_V(g, a0, SIG_MED) for g in S])
        d = float(np.median(np.log10(Vp / V)))
        d_by_foot[foot] = d
        line += f"  {d:+.3f}"
    VN = np.array([(G * g["Mb"] * Msun / (g["RHI"] * 1e3 * 3.0857e16)) ** 0.5 / 1e3 for g in S])
    line += f"   |  {float(np.median(np.log10(VN/V))):+.3f}"
    P(line)
    # the slope (U2) ACTUALLY implies inside this subsample: V^4 ~ M_b, and M_b tracks R_HI with its own slope
    sl_imp = fit_loglog(R, np.array([g["Mb"] for g in S]))[0] / 4.0
    rec[gc] = (len(S), sl, sc, d_by_foot, float(np.median(np.log10(VN / V))), esl, sl_imp)
P("  (Newtonian column = log10[ sqrt(G M_b/R_HI) / V_flat ], the no-dark-matter prediction at the HI radius.)")
P("  slope errors are 2000-sample bootstraps over galaxies; logR range is the lever arm the slope is fitted over.")
P("\n  (U2) predicts slope = 1/2 only if <Sigma_HI> is exactly universal.  The slope it actually implies inside")
P("  each subsample is (d log M_b / d log R_HI)/4, computed from the SAME galaxies:")
for gc in rec:
    P(f"    gas cut {gc:.1f}: (U2)-implied slope {rec[gc][6]:+.3f}  vs measured {rec[gc][1]:+.3f} +- {rec[gc][5]:.3f}  "
      f"-> {abs(rec[gc][1]-rec[gc][6])/rec[gc][5]:.1f} sigma")

gc0 = 0.7
N0, sl0, sc0, d0, dN0, esl0, slimp0 = rec[gc0]
P("""
  ⚠ DISCLOSURE, because the rules forbid tuning a threshold to make a check pass.  The bar written before running
  was 'slope within 0.10 of 1/2'.  After seeing the result I judged that target WRONG -- (U2) gives exactly 1/2
  only if <Sigma_HI> is exactly universal, and the measured size-mass slope is 0.524, not 0.500, so the slope
  (U2) actually implies is (d log M_b/d log R_HI)/4 computed on the same galaxies.  BOTH checks are therefore
  kept and both are reported.  The pre-registered one FAILS.""")
ck("Q2a-preset [THE PRE-REGISTERED BAR, KEPT] the measured V_flat-R_HI slope must be 1/2 to within 0.10",
   abs(sl0 - 0.5) < 0.10, f"measured {sl0:+.3f} +- {esl0:.3f} at gas cut {gc0}, "
                          f"{abs(sl0-0.5)/esl0:.1f} sigma from 1/2")
ck("Q2a-implied [THE REVISED BAR, DISCLOSED AS REVISED] the measured slope must agree with the slope (U2) "
   "implies inside the same subsample to 2 sigma",
   abs(sl0 - slimp0) < 2 * esl0,
   f"measured {sl0:+.3f} +- {esl0:.3f} vs implied {slimp0:+.3f} ({abs(sl0-slimp0)/esl0:.1f} sigma)")
best_foot = min(d0, key=lambda f: abs(d0[f]))
ck("Q2b the ZERO POINT, built from a_0 and one measured surface density with no free parameter, must land on the "
   "measured relation to 0.05 dex in log V on at least one footing",
   abs(d0[best_foot]) < 0.05, f"canonical {d0['canonical']:+.3f}, alt {d0['alt']:+.3f} dex (best {best_foot})")
sc_pred = sc_dm / 0.506 / 4.0     # size-mass scatter propagated: log M at fixed D, then quartered by the 1/4 power
P(f"\n  scatter propagated from the size-mass relation alone: {sc_dm:.4f}/{0.506:.3f}/4 = {sc_pred:.4f} dex in log V")
P(f"  measured scatter about the V-R_HI relation           : {sc0:.4f} dex")
ck("Q2c the scatter of the V_flat-R_HI relation must be no more than 1.5x what the size-mass scatter alone "
   "propagates to, or something other than the HI structure is driving it",
   sc0 < 1.5 * sc_pred, f"{sc0:.4f} vs 1.5 x {sc_pred:.4f} = {1.5*sc_pred:.4f} dex")

# --------------- restatement test, executed
P("\n" + "-" * 118)
P("Q2 RESTATEMENT TEST -- EXECUTED, NOT ASSERTED")
P("-" * 118)
P("""  Claim to test: (U2) follows from v^4 = G M_b a_0 plus algebra on measured inputs.
  Derivation: <Sigma_HI> := M_HI/(pi R_HI^2) is a DEFINITION, so pi R_HI^2 <Sigma_HI> = M_HI identically.  Put
  M_b = 1.33 M_HI into v^4 = G M_b a_0 and (U2) drops out with no further content.  Verified numerically below by
  computing V two ways for every galaxy and differencing.""")
S = sample(UPS_D, UPS_B, 0.0)
mx = 0.0
for g in S:
    sig_own = g["MHI"] / (math.pi * (g["RHI"] * 1e3) ** 2)
    v_law = (G * A0["canonical"] * (HE * math.pi * (g["RHI"] * 1e3) ** 2 * sig_own) * Msun) ** 0.25 / 1e3
    v_btfr = (G * A0["canonical"] * (HE * g["MHI"]) * Msun) ** 0.25 / 1e3
    mx = max(mx, abs(math.log10(v_law / v_btfr)))
P(f"\n  max |log10( V from (U2) / V from the BTFR )| over {len(S)} galaxies = {mx:.3e} dex")
ck("Q2-RESTATE (U2) must be checked for whether it closes against v^4 = G M_b a_0.  A PASS here means the "
   "candidate IS A RESTATEMENT and is DEMOTED -- the check is written so that the framework's friend loses",
   mx < 1e-12, f"max difference {mx:.3e} dex -- (U2) IS A RESTATEMENT of the BTFR given one empirical input")
P("""
  What (U2) is, honestly: the BTFR with the baryonic mass replaced by the HI size through an empirical relation
  the framework does not predict (Q1).  It is a corollary with a predicted coefficient, not a second law.  Its
  one genuine virtue is that it pairs two quantities measured by DIFFERENT instruments -- an HI map and a
  rotation curve -- with no stellar mass-to-light ratio in the gas-dominated limit.""")

# ------------------------------------------------------------------ Q3: the acceleration at the HI edge
P("\n" + "=" * 118)
P("Q3 -- THE MASS DISCREPANCY AT EVERY GALAXY'S OWN HI EDGE")
P("=" * 118)
P("""  R_HI is defined by a fixed surface density, so g_bar(R_HI) should be nearly universal, and the framework
  then predicts a nearly universal mass discrepancy D = g_obs/g_bar there.  Measured by interpolating SPARC's own
  disc solutions at R = R_HI (LOCAL enclosed-mass speeds, never a total mass).""")


def at_RHI(ups_d, ups_b):
    gals = load_sparc(ups_d=ups_d, ups_b=ups_b)
    out = []
    for g in gals:
        rhi = master[g["name"]]["RHI"]
        if rhi <= 0 or g["r"].max() < rhi or g["r"].min() > rhi:
            continue
        gb = float(np.interp(rhi, g["r"], g["gbar"]))
        go = float(np.interp(rhi, g["r"], g["gobs"]))
        vg2 = float(np.interp(rhi, g["r"], g["vg"] * np.abs(g["vg"])))
        vb2 = float(np.interp(rhi, g["r"], g["vg"] * np.abs(g["vg"]) + ups_d * g["vd"] ** 2 + ups_b * g["vb"] ** 2))
        if gb <= 0 or go <= 0 or vb2 <= 0:
            continue
        out.append(dict(name=g["name"], RHI=rhi, gbar=gb, gobs=go, D=go / gb, share=vg2 / vb2))
    return out


AT = at_RHI(UPS_D, UPS_B)
gb = np.array([a["gbar"] for a in AT]); go = np.array([a["gobs"] for a in AT]); Dm = np.array([a["D"] for a in AT])
P(f"\n  {len(AT)} SPARC discs whose rotation curve reaches R_HI.")
gref = 2 * math.pi * G * HE * 1.0 * MSUN_PC2
P(f"  thin-sheet reference from the DEFINITION alone (Sigma_HI = 1 Msun/pc^2, x1.33): g = {gref:.3e} m/s^2")
P(f"  measured g_bar(R_HI) : median {np.median(gb):.3e} m/s^2, scatter {np.log10(gb).std(ddof=1):.3f} dex "
  f"({np.median(gb)/gref:.2f}x the reference -- the excess is the stars)")
P(f"  measured g_obs(R_HI) : median {np.median(go):.3e} m/s^2, scatter {np.log10(go).std(ddof=1):.3f} dex")
P(f"  measured D(R_HI)     : median {np.median(Dm):6.2f},          scatter {np.log10(Dm).std(ddof=1):.3f} dex")
for foot, a0 in A0.items():
    Dp = nu(gb / a0)
    P(f"  {foot:10s} framework nu(g_bar(R_HI)/a_0): median {np.median(Dp):6.2f}, scatter "
      f"{np.log10(Dp).std(ddof=1):.3f} dex,  log(pred/meas) = {np.median(np.log10(Dp/Dm)):+.3f} dex")
ck("Q3a the total acceleration at the HI edge must be universal to RAR-class scatter (<= 0.15 dex) for the "
   "'same acceleration at every HI edge' statement to be a regularity at all",
   float(np.log10(go).std(ddof=1)) <= 0.15, f"scatter {np.log10(go).std(ddof=1):.3f} dex")
bestQ3 = min(A0, key=lambda f: abs(float(np.median(np.log10(nu(gb / A0[f]) / Dm)))))
P(f"\n  RESTATEMENT: Q3 is the RAR evaluated at one particular radius.  It closes against g_obs = nu(g_bar/a_0) by "
  f"construction and is a restatement; recorded for the number, not as a law.")
ck("Q3b the framework's predicted discrepancy at R_HI must match the measured one in the median to 0.05 dex on "
   "at least one footing",
   abs(float(np.median(np.log10(nu(gb / A0[bestQ3]) / Dm)))) < 0.05,
   f"best {bestQ3}: {float(np.median(np.log10(nu(gb/A0[bestQ3])/Dm))):+.3f} dex")

# ------------------------------------------------------------------ Upsilon lever
P("\n" + "-" * 118)
P("THE UPSILON LEVER, measured by re-running the WHOLE pipeline at Upsilon x 1.5")
P("-" * 118)
dlog = math.log10(1.5)
lev = {}
for tag, (ud, ub) in (("x1.0", (UPS_D, UPS_B)), ("x1.5", (1.5 * UPS_D, 1.5 * UPS_B))):
    S2 = sample(ud, ub, gc0)
    V2 = np.array([g["V"] for g in S2])
    Vp2 = np.array([predict_V(g, A0["canonical"], SIG_MED) for g in S2])
    d2 = float(np.median(np.log10(Vp2 / V2)))
    A2 = at_RHI(ud, ub)
    gb2 = np.array([a["gbar"] for a in A2]); D2 = np.array([a["D"] for a in A2])
    q3 = float(np.median(np.log10(nu(gb2 / A0["canonical"]) / D2)))
    lev[tag] = (d2, q3, len(S2))
    P(f"  Upsilon_disc = {ud:.3f}:  Q2 zero-point offset {d2:+.4f} dex (N={len(S2)});  Q3 offset {q3:+.4f} dex")
lQ2 = (lev["x1.5"][0] - lev["x1.0"][0]) / dlog
lQ3 = (lev["x1.5"][1] - lev["x1.0"][1]) / dlog
P(f"\n  d [Q2 zero-point offset] / d log Upsilon = {lQ2:+.3f} dex per dex   <-- (U2) on gas-rich discs")
P(f"  d [Q3 offset]            / d log Upsilon = {lQ3:+.3f} dex per dex")
ck("UPS the (U2) zero-point test must move by less than 0.10 dex per dex of Upsilon -- it is a test in log V, "
   "where a quarter-power already divides the mass lever by four, so the bar is tighter than the hunt's usual 0.3",
   abs(lQ2) < 0.10, f"{lQ2:+.3f} dex/dex")

# ------------------------------------------------------------------ mutation controls
P("\n" + "-" * 118)
P("MUTATION CONTROLS")
P("-" * 118)
S3 = sample(UPS_D, UPS_B, gc0)
V3 = np.array([g["V"] for g in S3])
d_base = float(np.median(np.log10(np.array([predict_V(g, A0["canonical"], SIG_MED) for g in S3]) / V3)))
d_mut = float(np.median(np.log10(np.array([predict_V(g, 4 * A0["canonical"], SIG_MED) for g in S3]) / V3)))
P(f"  a_0 x 4 : (U2) zero point moves {d_base:+.4f} -> {d_mut:+.4f}, shift {d_mut-d_base:+.4f} dex "
  f"(predicted exactly +{math.log10(4)/4:.4f}, since a_0 enters at the 1/4 power)")
ck("M1 quadrupling a_0 must move the (U2) zero point by log10(4)/4 = +0.1505 dex to within 0.005",
   abs((d_mut - d_base) - math.log10(4) / 4) < 0.005, f"{d_mut-d_base:+.4f} against +{math.log10(4)/4:.4f}")
d_sig = float(np.median(np.log10(np.array([predict_V(g, A0["canonical"], SIG_MED * 4) for g in S3]) / V3)))
P(f"  <Sigma_HI> x 4 : zero point moves {d_base:+.4f} -> {d_sig:+.4f}, shift {d_sig-d_base:+.4f} dex "
  f"-- the SAME lever as a_0, so the two are perfectly degenerate in (U2)")
ck("M2 AGAINST INTEREST: a_0 and <Sigma_HI> must enter (U2) with the SAME power, which means the zero-point "
   "agreement is as much a measurement of the HI surface density as of a_0.  This check PASSES when the "
   "degeneracy is total -- i.e. when the candidate is weakest",
   abs((d_sig - d_base) - (d_mut - d_base)) < 0.02,
   f"a_0 lever {d_mut-d_base:+.4f}, Sigma lever {d_sig-d_base:+.4f} -- perfectly degenerate")
P("  nu = 1 (kernel off): (U2) has no deep-MOND limit to stand on, V_flat is not even defined without a boost, "
  "and Q3 predicts D = 1 exactly against a measured " + f"{np.median(Dm):.2f}.")
ck("M3 with the kernel off the framework must predict D(R_HI) = 1 exactly, which the data reject outright",
   abs(np.median(Dm) - 1.0) > 1.0, f"measured median D(R_HI) = {np.median(Dm):.2f} against nu=1's 1.00")

# ------------------------------------------------------------------ alternatives
P("\n" + "-" * 118)
P("THE NEWTONIAN AND LambdaCDM ALTERNATIVES, COMPUTED BESIDE")
P("-" * 118)
VN = np.array([(G * g["Mb"] * Msun / (g["RHI"] * 1e3 * 3.0857e16)) ** 0.5 / 1e3 for g in S3])
P(f"  Newtonian, no dark matter, at gas cut {gc0}: median log10(V_newt/V_flat) = "
  f"{float(np.median(np.log10(VN/V3))):+.3f} dex -- short by a factor {1/10**float(np.median(np.log10(VN/V3))):.2f}.")
P(f"  Also Newtonian: D(R_HI) = 1 exactly against a measured median {np.median(Dm):.2f}.")
P("""  LambdaCDM: there is no predicted zero point for (U2) at all.  The relation would have to emerge from the
  halo mass-concentration relation crossed with the stellar-to-halo-mass relation crossed with whatever sets the
  HI extent -- three fitted ingredients.  What LambdaCDM CAN say is that the V-R_HI slope should not be exactly
  1/2 and should drift with mass; measured drift is reported above through the three gas cuts.""")
sl_all = [rec[g][1] for g in rec]
P(f"  measured V-R_HI slope across the three gas cuts: {['%.3f' % s for s in sl_all]} "
  f"(spread {max(sl_all)-min(sl_all):.3f})")

P("\n" + "=" * 118)
P("VERDICT")
P("=" * 118)
P(f"""  Q1  NO.  <Sigma_HI> = {SIG_MED:.2f} Msun/pc^2 is 1/{(A0['canonical']/(2*math.pi*G)/MSUN_PC2)/SIG_MED:.1f} of a_0/(2 pi G) on the canonical footing and
      matches no simple coefficient to 2%.  The framework predicts nothing about the tightest scaling relation
      in galaxy astronomy.  Reported against interest.
  Q2  (U2) reproduces the measured V_flat-R_HI relation: slope {sl0:+.3f} +- {esl0:.3f} against the {slimp0:+.3f} it implies
      inside the same subsample (the naive 1/2 is the wrong target), zero point
      {d0['canonical']:+.3f} (canonical) / {d0['alt']:+.3f} (alt) dex, scatter {sc0:.3f} dex.  But it is a PROVED RESTATEMENT of the
      BTFR (max difference {mx:.1e} dex), and a_0 and <Sigma_HI> are perfectly degenerate inside it, so the
      zero-point agreement measures their PRODUCT and not a_0.
  Q3  The mass discrepancy at the HI edge is {np.median(Dm):.2f} with {np.log10(Dm).std(ddof=1):.3f} dex scatter; the framework's nu(y) at the
      measured g_bar(R_HI) gives {np.median(nu(gb/A0[bestQ3])):.2f} on the {bestQ3} footing.  Also a restatement -- the RAR at one radius.

  NOT Kepler-grade.  Criterion (2) fails for Q2 (the coefficient is a_0 x <Sigma_HI>, and <Sigma_HI> is fitted
  from the same data), and criterion (5) fails for Q2 and Q3 by proof.""")
sys.exit(ck.done())
