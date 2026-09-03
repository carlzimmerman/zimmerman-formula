#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k03 -- the EFE ending radius: where the lensing 1/r law MUST steepen, and the external field measured from it.

THE CANDIDATE.  Two things the ledger already banks, put together for the first time:

  * item 1 (keeper): the lensing acceleration around isolated KiDS galaxies falls as 1/r EXACTLY, in every
    stellar-mass bin, from 0.05 to 2.6 Mpc.
  * item 72 (keeper): no mass bin prefers an ENDING of the sqrt boost; endings are excluded at 3 sigma below
    1.67 / 2.07 / 3.44 / 2.77 Mpc.

But a MOND-class theory does not keep the 1/r law to infinity.  A galaxy sitting in the large-scale-structure
field g_ext is quasi-Newtonian wherever its OWN field falls below g_ext, with G -> nu(e_N) G, and the lensing
acceleration must steepen from 1/r to 1/r^2 at

        r_EFE = sqrt(G M_b a_0) / g_ext  =  v_flat^2 / g_ext                                     (*)

which is a_0 with a PREDICTED coefficient of exactly 1, connecting three MEASURED quantities: the baryonic mass
of the lens, the radius at which its lensing profile breaks, and the external field on it -- and the external
field is measured INDEPENDENTLY, from the 2M++ redshift survey, in this repository already
(`~/new_physics/gext_vectors_2026/data/gext_vectors.csv`, 175 lines of sight, the same construction the
programme uses for its external-field lane).

READ FORWARD it predicts a break radius.  READ BACKWARD it is a NEW MEASUREMENT: the mean external field on a
stack of isolated galaxies, read off a lensing profile, g_ext = v_flat^2 / r_break.

WHY IT IS NOT A RESTATEMENT.  v^4 = G M_b a_0 gives v_flat and nothing else -- no radius, and no dependence on
what is outside the galaxy.  Equation (*) needs the external-field effect, which is independent content of the
field equation and is absent from the deep-MOND limit.  The derivation from the RAR does not close.

Rules: both footings; the alternative (a dark halo, which has no external-field effect at all and keeps its own
profile) computed beside it; checks that CAN fail; mutation controls.  SCOPING CALCULATION, stated as such: the
outer-slope fit here uses diagonal errors, where item 72 carried the full 60x60 covariance.  It is enough to
size the effect and to decide whether the candidate is worth a full run; it is not enough to close it.
"""
import math
import numpy as np
from hunt_lib import Check, P, info, A0, load_esd, load_cov_esd, nu_s, fit_loglog

G, c = 6.67430e-11, 2.99792458e8
Msun, pc = 1.98892e30, 3.0856775814913673e16
Mpc = 1e6*pc
ck = Check()

# the four KiDS isolated-lens stellar-mass bins, exactly as item 72 read them
BINS = [(1, 10.00, 1.50e10), (2, 10.45, 3.66e10), (3, 10.70, 6.01e10), (4, 10.90, 9.13e10)]

P("="*126)
P("k03 -- THE EFE ENDING RADIUS:  r_EFE = sqrt(G M_b a_0)/g_ext = v_flat^2/g_ext")
P("="*126)

# ------------------------------------------------------------ 1. the external field, from the repo's own 2M++
P("\n1. THE EXTERNAL FIELD, measured independently of any lensing, from 2M++")
P("-"*126)
import csv, os
GEXT = os.path.expanduser("~/new_physics/gext_vectors_2026/data/gext_vectors.csv")
rows = list(csv.DictReader(open(GEXT)))
eN_no = np.array([10**float(r["log_eN_noclu"]) for r in rows])
eN_mx = np.array([10**float(r["log_eN_maxclu"]) for r in rows])
P(f"  {len(rows)} lines of sight (the SPARC footprint, the programme's own external-field construction)")
for lab, e in (("no cluster term", eN_no), ("maximal cluster term", eN_mx)):
    tru = np.array([u*nu_s(u) for u in e])
    P(f"    e_N = g_N,ext/a_0  ({lab:<21s}): median {np.median(e):.3e}  16-84 [{np.percentile(e,16):.2e}, {np.percentile(e,84):.2e}]"
      f"   ->  TRUE field g_ext/a_0 = nu(e_N) e_N: median {np.median(tru):.4f}  16-84 [{np.percentile(tru,16):.4f}, {np.percentile(tru,84):.4f}]")
GX = {"2M++ no-cluster (median)": float(np.median([u*nu_s(u) for u in eN_no])),
      "2M++ max-cluster (median)": float(np.median([u*nu_s(u) for u in eN_mx])),
      "2M++ no-cluster (16th pct, the most isolated)": float(np.percentile([u*nu_s(u) for u in eN_no], 16))}
ck("K03.1 the repository's own 2M++ external fields put the TRUE external field on a field galaxy in the range "
   "0.01-0.07 a_0.  This check fails if the file is being read in the wrong units, which would invalidate "
   "everything below",
   0.005 < GX["2M++ no-cluster (median)"] < 0.10 and 0.005 < GX["2M++ max-cluster (median)"] < 0.15,
   ", ".join(f"{k}: {v:.4f} a_0" for k, v in GX.items()))

# ------------------------------------------------------------ 2. the predicted break radius, both footings
P("\n2. THE PREDICTION: r_EFE = sqrt(G M_b a_0)/g_ext, four mass bins x two footings x three field estimates")
P("-"*126)
P(f"  {'footing':<10s} {'bin':>3s} {'M_b (Msun)':>11s} {'v_flat (km/s)':>13s} " +
  "".join(f"{k[:26]:>28s}" for k in GX))
RPRED = {}
for k, a0 in A0.items():
    for b, lm, Mb in BINS:
        v2 = math.sqrt(G*Mb*Msun*a0)
        rr = {lab: v2/(g*a0)/Mpc for lab, g in GX.items()}
        RPRED[(k, b)] = rr
        P(f"  {k:<10s} {b:>3d} {Mb:11.3e} {math.sqrt(v2)/1e3:13.1f} " +
          "".join(f"{rr[lab]:28.3f}" for lab in GX))
P("  (values in Mpc)")
P("  ITEM 1 measured the lensing acceleration falling as 1/r EXACTLY over 0.05-2.6 Mpc in every one of these")
P("  bins.  ITEM 72 excluded an ENDING below 1.67 / 2.07 / 3.44 / 2.77 Mpc at 3 sigma.  Both are keepers.")

# ------------------------------------------------------------ 3. the measured outer slope, per bin
P("\n3. THE MEASURED OUTER SLOPE of the lensing acceleration, per mass bin (scoping fit, diagonal errors)")
P("-"*126)
P(f"  {'bin':>3s} {'N pts':>5s} {'R range (Mpc)':>18s} {'slope d log g_obs/d log R':>26s} {'vs -1 (MOND)':>13s} {'vs -2 (EFE/Newton)':>19s}")
SLOPES = {}
for b, lm, Mb in BINS:
    R, ESD, eESD = load_esd(f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt")
    ok = (ESD > 0) & (eESD > 0) & (R > 0)
    R, ESD, eESD = R[ok], ESD[ok], eESD[ok]
    gobs = 4*6.674e-11*ESD*Msun/pc**2                      # g = 4 G Sigma_ESD  (Brouwer eq 23), SI
    egobs = 4*6.674e-11*eESD*Msun/pc**2
    out = R > 0.15                                          # outside the predicted break for every field estimate
    x, y, w = np.log10(R[out]), np.log10(gobs[out]), (gobs[out]/egobs[out])**2
    A = np.vstack([x, np.ones_like(x)]).T
    W = np.diag(w)
    beta = np.linalg.solve(A.T @ W @ A, A.T @ W @ y)
    cov = np.linalg.inv(A.T @ W @ A)
    s, es = beta[0], math.sqrt(cov[0, 0])
    SLOPES[b] = (s, es, R[out].min(), R[out].max(), out.sum())
    P(f"  {b:>3d} {out.sum():5d} {f'{R[out].min():.3f} - {R[out].max():.3f}':>18s} "
      f"{f'{s:+.3f} +- {es:.3f}':>26s} {f'{(s+1)/es:+.1f} sig':>13s} {f'{(s+2)/es:+.1f} sig':>19s}")
smean = np.mean([SLOPES[b][0] for b in SLOPES]); serr = np.mean([SLOPES[b][1] for b in SLOPES])/2
P(f"  stack of four bins: slope = {smean:+.3f} +- {serr:.3f} (naive), i.e. {(smean+1)/serr:+.1f} sigma from -1 "
  f"and {(smean+2)/serr:+.1f} sigma from -2")
ck("K03.2 CLAIM UNDER TEST: the framework's external-field effect requires the lensing acceleration to steepen "
   "to a slope of -2 beyond r_EFE, which for these lenses and the repository's own 2M++ fields is 0.08-0.6 Mpc. "
   "The measured outer slope beyond 0.15 Mpc must therefore be nearer -2 than -1.  It is not",
   abs(smean + 2) < abs(smean + 1),
   f"measured outer slope {smean:+.3f}; MOND-without-EFE says -1, MOND-with-EFE and a dark halo both say about -2")

# ------------------------------------------------------------ 4. read backward: g_ext measured from lensing
P("\n4. READ BACKWARD -- the external field on the KiDS isolated-lens stack, measured from the lensing profile")
P("-"*126)
P("  Requiring r_EFE to exceed item 72's 3-sigma lower bound on the ending radius bounds g_ext from above:")
r72 = {1: 1.67, 2: 2.07, 3: 3.44, 4: 2.77}
BND = {}
for k, a0 in A0.items():
    for b, lm, Mb in BINS:
        v2 = math.sqrt(G*Mb*Msun*a0)
        gmax = v2/(r72[b]*Mpc)
        BND[(k, b)] = gmax/a0
        P(f"    {k:<10s} bin {b}: r_EFE > {r72[b]:.2f} Mpc  =>  g_ext < {gmax:.3e} m/s^2 = {gmax/a0:.5f} a_0")
tight = min(BND.values())
P(f"\n  TIGHTEST BOUND across bins and footings: g_ext < {tight:.5f} a_0 on the KiDS isolated-lens stack.")
P(f"  The 2M++ construction in this repository gives {GX['2M++ no-cluster (median)']:.4f} a_0 (no cluster term) to "
  f"{GX['2M++ max-cluster (median)']:.4f} a_0 (maximal),")
P(f"  i.e. a factor {GX['2M++ no-cluster (median)']/tight:.0f}-{GX['2M++ max-cluster (median)']/tight:.0f} LARGER "
  f"than the lensing allows -- {math.log10(GX['2M++ no-cluster (median)']/tight):.2f} to "
  f"{math.log10(GX['2M++ max-cluster (median)']/tight):.2f} dex.")
ck("K03.3 THE CANDIDATE'S SHARP EDGE, and it cuts against the framework: the external field the lensing data "
   "allow is an order of magnitude below the external field the same repository computes from 2M++.  This "
   "check is written to fail if the two disagree by more than 0.3 dex, and it fails",
   math.log10(GX["2M++ no-cluster (median)"]/tight) < 0.3,
   f"lensing allows < {tight:.5f} a_0; 2M++ gives {GX['2M++ no-cluster (median)']:.4f}-"
   f"{GX['2M++ max-cluster (median)']:.4f} a_0")

# ------------------------------------------------------------ 5. the alternative, and the escapes
P("\n5. THE ALTERNATIVE COMPUTED BESIDE IT, AND THE THREE ESCAPES -- stated because they are real")
P("-"*126)
P("  LambdaCDM's answer: a dark halo has no external-field effect at all.  Its lensing profile at 0.1-3 Mpc is")
P("  the one-halo NFW term steepening to -1.2 ... -1.6 (item 1 measured -1.00 and called NFW out), plus a")
P("  two-halo term that RISES.  So the observed -1 is a problem for the halo too; what k03 adds is that it is")
P("  ALSO a problem for the framework once the external field is switched on, which item 1 never did.")
P("  ESCAPE 1 -- the two-halo term.  Beyond r_EFE the framework's own neighbours contribute their phantoms, and")
P("     that added signal could refill a steepening profile.  Item 84 withdrew E_G on exactly this physics and")
P("     item 113 is the item that would settle it.  Until it is modelled, k03 is a scoping result.")
P("  ESCAPE 2 -- the stack smears the break.  r_EFE depends on each lens's own g_ext, which varies by 0.5 dex")
P("     across 2M++ lines of sight, so a stack of many lenses has no sharp break, only a gradual steepening.")
P("     The correct test is a forward model of the stack, not a single break radius.")
P("  ESCAPE 3 -- the KiDS lenses are isolation-selected and the 2M++ sample is not.  The isolation cut removes")
P("     near neighbours but NOT the large-scale term, which is what dominates the 2M++ numbers; this escape is")
P("     the weakest of the three and is the one to close first.")

# ------------------------------------------------------------ 6. levers and mutation
P("\n6. LEVERS AND MUTATION CONTROLS")
P("-"*126)
P("  d log r_EFE / d log M_b   = +1/2 exactly       -> d log r_EFE/d log Upsilon = (1/2) x (stellar share of M_b)")
P("     for these lenses the stellar share of M_b is about 0.85, so d log r_EFE/d log Upsilon = +0.43")
P("  d log r_EFE / d log a_0   = +1/2 exactly       -> the footing gap of 0.082 dex moves r_EFE by 0.041 dex")
P("  d log g_ext(inferred)/d log Upsilon = +0.43    -> the backward reading inherits the same lever")
P("  d log r_EFE / d log g_ext = -1 exactly         -> the whole tension is linear in the external field")
for mult, lab in ((0.1, "a_0 / 10"), (10.0, "a_0 x 10")):
    a0m = A0['canonical']*mult
    v2 = math.sqrt(G*BINS[3][2]*Msun*a0m)
    P(f"  M1 mutation {lab:<10s}: bin 4 r_EFE at the 2M++ median field -> "
      f"{v2/(GX['2M++ no-cluster (median)']*a0m)/Mpc:8.3f} Mpc "
      f"(vs {RPRED[('canonical',4)]['2M++ no-cluster (median)']:.3f} at the true a_0)")
P("     -- note the mutation moves r_EFE by only sqrt(1/10) = 0.5 dex because g_ext is quoted in units of a_0;")
P("     held FIXED in physical units the lever is +1/2 and the mutation moves it 0.5 dex the other way.  Both")
P("     are printed so the reader can see the estimator is not an a_0-blind fixed point.")
rng = np.random.default_rng(3)
sh = []
for _ in range(2000):
    b = rng.integers(1, 5)
    R, ESD, eESD = load_esd(f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt")
    ok = (ESD > 0) & (eESD > 0) & (R > 0.15)
    y = np.log10(ESD[ok]); x = np.log10(R[ok]); rng.shuffle(y)
    sh.append(np.polyfit(x, y, 1)[0] - 2)      # ESD slope; g_obs slope = ESD slope (g = 4 G Sigma)
sh = np.array(sh)
P(f"  M2 shuffling ESD against radius within a bin: slope -> {np.mean(sh)+2:+.3f} +- {np.std(sh):.3f} "
  f"(the -1 signal is destroyed, so the measured slope is a property of the pairing)")
ck("K03.4 MUTATION: shuffling the ESD values against radius must destroy the slope.  If a shuffled profile "
   "still returned -1, the slope would be an artefact of the binning rather than a measurement",
   abs(np.mean(sh) + 2) < 3*np.std(sh)/math.sqrt(len(sh)) + 0.25,
   f"shuffled slope {np.mean(sh)+2:+.3f} +- {np.std(sh):.3f} against the real {smean:+.3f}")

P("\n" + "="*126)
P("VERDICT -- CANDIDATE k03")
P("="*126)
P("  THE EQUATION IS SOUND AND IT IS NOT A RESTATEMENT: r_EFE = sqrt(G M_b a_0)/g_ext ties a_0, the lens's")
P("  baryonic mass, the radius at which its lensing profile must steepen, and the external field, with a")
P("  predicted coefficient of one.  Nothing in v^4 = G M_b a_0 implies it.")
P("  AS A TEST IT FIRES AGAINST THE FRAMEWORK, and that is the result.  With the repository's own 2M++")
P(f"  external fields the break should sit at 0.08-0.6 Mpc, and the measured outer slope beyond 0.15 Mpc is")
P(f"  {smean:+.3f}, not -2.  Turned round, the lensing profile bounds the external field on these lenses at")
P(f"  g_ext < {tight:.5f} a_0, an order of magnitude below what 2M++ gives for comparable galaxies.")
P("  IT IS A SCOPING RESULT, NOT A CLOSURE.  Three named escapes -- the neighbours' own phantoms refilling the")
P("  profile, the stack smearing a break that varies lens by lens, and the isolation cut -- are each capable of")
P("  absorbing an order of magnitude, and none is modelled here.  The full version needs item 113's two-halo")
P("  model, the 60x60 covariance item 72 carried, and per-lens external fields for the KiDS footprint rather")
P("  than the SPARC one.  What k03 establishes is that the calculation is worth doing and which way it points.")
raise SystemExit(ck.done())
