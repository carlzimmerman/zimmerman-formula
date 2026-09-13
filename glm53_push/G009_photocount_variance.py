#!/usr/bin/env python3
"""G009 -- THE PHOTOCOUNT VARIANCE SIGNATURE (the user's Question 6).

Is the Mandel photocount identification physics or analogy?  The question,
verbatim: 'Does mu_n = P(>=1 quantum in n modes) predict anything beyond the
RAR shape -- a variance/fluctuation signature in the acceleration field?  Kill:
if it makes no prediction distinguishable from a bare interpolating function,
it's an analogy, not a mechanism, and n=2 stays purely empirical.'

THE DERIVATION (new, this lane).  If mu_2(Y) is literally the probability that
at least one quantum is present among n = 2 independent thermal modes of mean
occupancy Y = g/s, then the acceleration response is not the DETERMINISTIC
function mu_2(Y) g -- it is the EXPECTED response over the mode-occupancy
distribution.  The full count statistics of n independent Bose modes (Mandel's
formula) are:

    P(k total quanta) = C(n+k-1, k) Y^k / (1+Y)^(n+k)

and the response is conditioned on k >= 1.  A deterministic interpolating
function predicts NOTHING about the variance; the photocount reading predicts
a specific one:

    Var(g_response | Y) / <g_response>^2 = [Var(k | k>=1)] / <k | k>=1>^2

THE TEST.  The RAR's observed scatter (0.05-0.11 dex in SPARC, McGaugh+16;
the repo's own floor estimate 0.045 dex intrinsic) must be AT LEAST the
photocount variance at the same Y -- because the photocount shot noise is
irreducible if the reading is a mechanism.  If the predicted shot noise is
LARGER than the observed scatter anywhere on the relation, the reading is
DEAD (the data are quieter than its floor).  If it is smaller everywhere, it
is a live mechanism with a specific, binned, measurable prediction.  If it is
negligible everywhere, it is indistinguishable from a bare interpolating
function -- the user's kill.

Every check states measurement and threshold separately.
"""
import json, math
import numpy as np

RES, NP, NF = [], 0, 0
def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    if ok: NP += 1
    else: NF += 1

print(__doc__)

# ------------------------------------------------------------------ Part A: the exact count statistics of n=2 thermal modes
print("PART A -- the exact count statistics: P(k) for n = 2 independent thermal modes")

def P_k(k, n, Y):
    """Mandel: P(k total quanta among n modes of mean occupancy Y each... """
    # CAREFUL: the mean occupancy per mode is Y; total mean = nY.
    # The NB (negative binomial) distribution: P(k) = C(n+k-1, k) Y^k/(1+Y)^(n+k)
    # gives total mean nY.  This is the standard n-mode thermal photon count.
    from math import comb
    return comb(n + k - 1, k)*Y**k/(1.0 + Y)**(n + k)

def moments(n, Y, kmax=4000):
    """mean and variance of k, conditioned on k >= 1 (the response is on)."""
    ks = np.arange(1, kmax + 1)
    ps = np.array([P_k(k, n, Y) for k in ks])
    p0 = 1.0 - ps.sum()
    # normalise over k>=1
    ps = ps/(1.0 - p0)
    mean = float((ks*ps).sum())
    var = float((ks**2*ps).sum() - mean**2)
    return mean, var

# the response: if the acceleration response is proportional to the count k
# (each quantum contributes equally), then
#   <g>/<g_det> = <k|k>=1>/n ... and Var(g)/<g>^2 = Var(k|k>=1)/<k|k>=1>^2
rows = []
print(f"    {'Y = g/s':>10s} {'<k|on>':>8s} {'Var(k)':>8s} {'sigma_g/<g>':>12s} {'sigma_g [dex]':>14s}")
for Y in (0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0):
    m, v = moments(2, Y)
    rel = math.sqrt(v)/m
    rows.append((Y, m, v, rel, rel/math.log(10)))
    print(f"    {Y:10.2f} {m:8.3f} {v:8.3f} {rel:12.4f} {rel/math.log(10):14.4f}")

# ------------------------------------------------------------------ Part B: the floor vs the observed RAR scatter
print()
print("PART B -- the photocount shot-noise floor vs the observed RAR scatter")

# SPARC's observed RAR scatter: 0.11 dex total (McGaugh+16), intrinsic ~0.06 dex
# (the repo carries 0.045 dex intrinsic floor and 0.108 dex total).  The
# relevant comparison is at the Y where galaxies actually sit: the RAR spans
# Y ~ 0.01 (the deep dwarfs) to Y ~ 100 (the high-surface-brightness centres),
# with the bulk of points at Y in [0.03, 10].
OBS_SCATTER_TOTAL = 0.108    # dex, SPARC total
OBS_SCATTER_INTRIN = 0.045   # dex, the repo's intrinsic floor estimate

# the photocount floor at the RAR's central band (Y ~ 0.1-1, where the
# relation bends): take the max over the sampled Y range that covers the bulk
floor_bulk = max(r[4] for r in rows if 0.05 <= r[0] <= 2.0)
Y_at_floor = [r[0] for r in rows if 0.05 <= r[0] <= 2.0 and r[4] == floor_bulk][0]

check("V1 [the photocount floor is BELOW the observed scatter everywhere on the "
      "bulk of the relation] the maximum predicted shot-noise scatter over the "
      "RAR's central band (Y in [0.05, 2]) is compared with the observed total "
      "scatter and the intrinsic floor",
      f"max photocount sigma = {floor_bulk:.4f} dex at Y = {Y_at_floor} against "
      f"the observed total 0.108 dex and the intrinsic floor 0.045 dex",
      floor_bulk < OBS_SCATTER_INTRIN,
      "the measured verdict, and it is a KILL: the photocount floor (max "
      f"{floor_bulk:.3f} dex over the bulk band) OVER-PREDICTS the observed "
      "intrinsic scatter (0.045 dex) by a factor of several and even the TOTAL "
      "scatter (0.108 dex) by ~2.5x. If the acceleration response were "
      "proportional to the quantum count, the RAR would be visibly looser than "
      "it is. The literal mechanism is falsified by the relation's own "
      "tightness -- the strongest form of the user's pre-registered kill")

check("V2 [THE KILL TEST: is the photocount variance distinguishable from a bare "
      "interpolating function?] the predicted shot-noise contribution at the "
      "RAR's central band is compared with the precision of the best current "
      "RAR scatter measurement (the intrinsic floor 0.045 dex) and with the "
      "per-bin precision achievable by stacking 2788 SPARC points in Y-bins",
      f"photocount floor {floor_bulk:.4f} dex vs intrinsic scatter 0.045 dex "
      f"vs stacked-bin precision {0.108/math.sqrt(2788/50):.4f} dex (50 bins "
      f"over 2788 points) -- the photocount term is "
      f"{floor_bulk/(0.108/math.sqrt(2788/50)):.1f}x the stacked-bin precision",
      floor_bulk > 0.108/math.sqrt(2788/50),
      "the verdict the arithmetic gives: if the photocount term exceeds the "
      "stacked-bin precision, the reading predicts a MEASURABLE extra scatter "
      "floor at small Y that a bare interpolating function does not -- physics, "
      "not analogy, and testable by binning the existing SPARC data")

# ------------------------------------------------------------------ Part C: the shape of the floor (the distinguishing signature)
print()
print("PART C -- the floor's SHAPE: sigma(Y) falls as 1/sqrt(<k>) -- a specific curve")

# deep MOND (small Y): <k|on> -> 1 (at least one quantum), Var -> small;
# the floor DIVERGES as Y -> 0 in relative terms (Poisson of a rare event)
ys = np.logspace(-3, 1.5, 40)
floor_curve = []
for Y in ys:
    m, v = moments(2, Y)
    floor_curve.append((Y, math.sqrt(v)/m/math.log(10)))
floor_curve = np.array(floor_curve)

# where does the floor cross 0.045 dex (the intrinsic scatter)?
cross = None
for (y1, s1), (y2, s2) in zip(floor_curve, floor_curve[1:]):
    if s1 >= 0.045 > s2:
        t = (s1 - 0.045)/(s1 - s2)
        cross = math.exp(math.log(y1) + t*(math.log(y2) - math.log(y1)))
        break
print(f"    the photocount floor crosses the 0.045-dex intrinsic scatter at "
      f"Y = {cross:.3f}" if cross else "    the floor stays above 0.045 dex for all Y < sampled")

check("V3 [the signature: the predicted scatter floor is LARGER than the "
      "intrinsic scatter in the deep regime, giving a measurable Y-dependence] "
      "the floor curve is evaluated and its crossing with the intrinsic scatter "
      "located; the prediction is that binned SPARC scatter must RISE toward "
      "small Y as the photocount floor takes over",
      f"floor at Y = 0.001: {[f'{s:.4f}' for y, s in floor_curve if y < 0.0011][0]} dex; "
      f"at Y = 0.01: {[f'{s:.4f}' for y, s in floor_curve if 0.009 < y < 0.011][0]} dex; "
      f"at Y = 1: {[f'{s:.4f}' for y, s in floor_curve if 0.9 < y < 1.1][0]} dex; "
      f"crossing of 0.045 dex at Y = {cross:.3f}" if cross else "no crossing",
      cross is not None and cross < 0.1,
      "the measured shape: the floor curve is NON-MONOTONIC -- ~0.05 dex at "
      "Y = 0.01, RISING to ~0.31 dex by Y ~ 1, asymptoting there (the "
      "negative-binomial relative variance approaches 1/sqrt(2)).  It NEVER "
      "falls below the intrinsic scatter anywhere in the RAR's bulk: the "
      "predicted floor is above the data EVERYWHERE, which is the kill.  The "
      "shape is specific and would have been measurable by binning the 2788 "
      "SPARC points in Y -- instead the existing measurement already answers "
      "it: the flat 0.045-dex intrinsic floor contradicts a rising 0.3-dex "
      "photocount floor")

print()
print("READING")
print("""
  THE ANSWER TO QUESTION 6, AND IT IS THE KILL.  The Mandel photocount reading
  DOES make a prediction beyond the RAR shape -- a specific, irreducible
  scatter floor, sigma_g/<g> = sqrt(Var(k|on))/<k|on> -- and that prediction is
  WRONG: at the RAR's central band the predicted floor is ~0.3 dex against the
  observed 0.108 dex TOTAL scatter and 0.045 dex intrinsic floor.  The radial
  acceleration relation is roughly three times TIGHTER than the literal
  per-quantum mechanism allows.

  So the verdict on the identification: it is an ANALOGY, not a mechanism.
  The n-mode thermal formula correctly predicts the MEAN (the shape mu_2), but
  the variance the mechanism demands is excluded by the data already in hand.
  Any surviving mechanism must be effectively deterministic at fixed Y -- the
  occupation numbers must be enormous (the classical limit), in which case the
  'mode count' reading loses its quantum content and n = 2 stays purely
  empirical, exactly as the user's kill condition states.

  This is the honest close of the photocount thread: the reading was beautiful
  (it explained the integer) and it is falsified as physics by its own variance.
  The exponent n = 2 remains a measured number with no known derivation --
  four structural searches failed, the dimensional route closed (L239), and now
  the count-statistics route is killed by the RAR's tightness.
""")
print(f"G009 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES,
           "floor_curve": [[float(y), float(s)] for y, s in floor_curve]},
          open("G009_results.json", "w"), indent=1)
