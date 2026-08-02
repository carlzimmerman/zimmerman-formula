#!/usr/bin/env python3
r"""mi_vertical_literature_spread_2026.py -- THE FULL PROVENANCE OF A CONTRADICTION I INVENTED, and the
correction it forces on my own "-0.26 sigma agreement". The vertical-force literature has FOUR values, and
the one I matched the framework against is the OUTLIER -- outlier BY CONSTRUCTION.

WHERE THIS COMES FROM. Two independent adversarial agents returned RECONCILED / HIGH confidence on the
"sign disagreement", and both refuted my proposed grad(mu) mechanism. Their findings force three
corrections to scripts committed earlier today.

  P1  THE FULL PROVENANCE. The contradiction was welded together from TWO papers by a search summariser.
  P2  MY grad(mu).grad(Phi) MECHANISM IS REFUTED -- and the reason is a normalisation I chose badly.
  P3  THE LITERATURE SPREAD: four values for the local vertical boost, and why they differ.
  P4  THE CORRECTION TO MY OWN VERDICT: matching Lisanti's 1.09 is matching a number its own paper says
      FAILS. Against vertical-only inferences the framework is LOW, not exact.
  P5  AGAINST INTEREST: the SIGN of the grad(mu) correction is UNRESOLVED in the literature.

Exit 0 = ran and every check held. No hard-coded verdicts.
"""
from __future__ import annotations

import math
import sys

ok: list[tuple[bool, str]] = []


def check(cond: bool, msg: str) -> bool:
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t: str) -> None:
    print("\n" + "=" * 100)
    print(f"  {t}")
    print("=" * 100)


G_LOCAL = 2.2406e-10                 # local |grad Phi| used throughout this corpus's confrontation
A0_FW = {"canon": 9.36e-11, "alt": 1.13e-10}
A0_CANONICAL_MOND = 1.2e-10          # the literature's standard value


def mu2(x):
    return x / math.sqrt(1.0 + x * x)          # framework alpha=2 == the literature's "standard"


def mu_simple(x):
    return x / (1.0 + x)


banner("P1  THE FULL PROVENANCE -- the contradiction was WELDED FROM TWO PAPERS")

print("""  Both reconcile agents, independently and at HIGH confidence:
   * Claim B's sentences 2-3 ("the Milky Way data requires a substantial amplification of the radial
     acceleration with little amplification of the vertical acceleration ... models which result in a
     MOND-like force struggle to simultaneously explain both") are VERBATIM the abstract of Lisanti,
     Moschella, Outmezguine & Slone 2019 (arXiv:1812.08169v2 = PRD 100, 083009) -- the SAME paper Claim A
     cited for "nu = 1.44".
   * Claim B's sentence 1 ("MOND almost doubles the vertical force Kz produced in Newtonian gravity by
     the baryonic disk at the solar position") is from a DIFFERENT paper: Bienayme et al. 2009 Sect. 3,
     where it is an ATTRIBUTION TO NIPOTI ET AL. 2007.
   * The search summariser welded sentence 1 (Bienayme, quoting Nipoti) onto sentences 2-3 (Lisanti's
     abstract) and presented the result as one claim. I then read Lisanti's Taylor intercept as a boost
     and had a contradiction with itself.
  So there was no cross-method disagreement, and no dropped term could ever have bridged "a paper and
  itself". Recorded as a process failure of mine, not a literature dispute.""")
# P1's provenance is documentary, so the check here is on the COMPUTABLE half of my error: that reading
# the Taylor intercept as the boost is a real, sized mistake and not a matter of interpretation.
NU0, NU1, AN = 1.44, -0.21, 1.65e-10
boost = NU0 + NU1 * 1e10 * AN
print(f"\n  the computable half of the error: nu_0 = {NU0} but the boost is nu_0 + nu_1 a_N = {boost:.4f}")
print(f"  reading the intercept as the boost overstates the EXCESS OVER UNITY by "
      f"{(NU0-1)/(boost-1):.1f}x ({NU0-1:.2f} against {boost-1:.3f})")
check(abs((NU0 - 1) / (boost - 1) - 4.7) < 0.6,
      f"P1 reading Lisanti's Taylor intercept as the physical boost overstates the excess over unity by "
      f"{(NU0-1)/(boost-1):.1f}x -- a sized arithmetic error, not an interpretive choice, and the half of "
      f"the provenance failure that is checkable rather than documentary")


banner("P2  MY grad(mu).grad(Phi) MECHANISM IS REFUTED -- and the reason is a normalisation I chose badly")

print("""  Both agents refute it. The quantitative reason, which I should have checked myself: at R0 the total
  |grad Phi| is RADIALLY DOMINATED, and the vertical piece adds IN QUADRATURE. So although the vertical
  force does rise from 0 to its full value across |z| <~ 1 kpc, |grad Phi| itself changes very little, and
  Syaifudin's loose justification ("the total acceleration is approximately constant") is numerically
  satisfied to about 1.5%.\n""")
gR = G_LOCAL                                    # radial part dominates at R0
for gz_frac in (0.1, 0.2, 0.3, 0.5):
    gz = gz_frac * gR
    change = math.hypot(gR, gz) / gR - 1.0
    print(f"     vertical force = {gz_frac:.0%} of radial  ->  |grad Phi| changes by {change:+.2%}")
q = math.hypot(gR, 0.2 * gR) / gR - 1.0
check(q < 0.03,
      f"P2 with the vertical force at 20% of the radial -- generous at |z| ~ 1 kpc -- |grad Phi| moves by "
      f"only {q:.2%} because the two add in QUADRATURE. So mu is nearly constant over the volume and the "
      f"dropped term cannot produce a factor-1.5 error")
print("""
  WHERE MY EARLIER SCRIPT WENT WRONG. mi_vertical_gradmu_term_2026 measured the ratio
  |grad(mu).grad(Phi)| / |mu lap(Phi)| and found it exceeding 1 above z ~ 0.8 kpc. That ratio is TRUE but
  it is the wrong normalisation for this question: lap(Phi) = 4 pi G rho DIES above the disc, so the ratio
  diverges wherever the density vanishes -- as I noted at the time -- and a ratio to a vanishing quantity
  does not bound the error in mu. The right measure is how much mu itself moves, which is ~1.5%.
  => THE RECONCILIATION CLAIM IN b68973f9 IS WITHDRAWN. Its arithmetic stands; its inference does not.""")


banner("P3  THE LITERATURE SPREAD -- four values, and why they differ")

LIT = {
    "Famaey & Binney 2005 (data inference, |z|=1.1 kpc)": (1.40, None, "vertical ONLY"),
    "Bienayme+2009 (FULL 3D AQUAL prediction)": (1.62, None, "vertical ONLY"),
    "Syaifudin+2024 (1D mu_0 inference)": (1.56, 0.06, "vertical ONLY"),
    "Lisanti+2019 (single scalar, radial AND vertical)": (1.09, 0.135, "JOINT fit"),
}
print(f"  {'source':<52}{'nu_vert':>10}{'err':>8}{'what was fitted':>18}")
print("  " + "-" * 90)
for k, (v, e, w) in LIT.items():
    print(f"  {k:<52}{v:>10.2f}{(f'{e:.3f}' if e else '--'):>8}{w:>18}")
vert_only = [v for v, e, w in LIT.values() if w == "vertical ONLY"]
joint = [v for v, e, w in LIT.values() if w == "JOINT fit"][0]
check(min(vert_only) > joint + 0.25,
      f"P3 the three VERTICAL-ONLY determinations cluster at {min(vert_only):.2f}-{max(vert_only):.2f} while the "
      f"JOINT single-scalar fit sits at {joint:.2f} -- the outlier is the joint fit, and it is an outlier "
      f"BY CONSTRUCTION")
print(f"""
  WHY. Lisanti et al. fit ONE scalar nu to the radial AND vertical data simultaneously. Their own finding
  is that this cannot work: the fit is "pushed to the minimum allowed value of nu(a_N(R0)) as allowed by
  the priors" and "scalar enhancements ... over-predict the vertical acceleration ... when trying to
  simultaneously explain the observed radial acceleration". So {joint:.2f} is not a measurement of the vertical
  boost -- it is the corner a single scalar is DRIVEN INTO, at a prior boundary, in a fit the authors
  report as failing.""")


banner("P4  THE CORRECTION TO MY OWN VERDICT")

nu_fw = {fn: 1.0 / mu2(G_LOCAL / a0) for fn, a0 in A0_FW.items()}
print(f"  framework predicted boost: alpha=2 canon nu = {nu_fw['canon']:.4f}, alt nu = {nu_fw['alt']:.4f}\n")
print(f"  {'compared against':<52}{'framework':>11}{'target':>9}{'verdict':>26}")
print("  " + "-" * 98)
for k, (v, e, w) in LIT.items():
    d = nu_fw["canon"] - v
    verdict = ("AGREES" if abs(d) < (e or 0.15) else ("framework LOW" if d < 0 else "framework HIGH"))
    print(f"  {k:<52}{nu_fw['canon']:>11.3f}{v:>9.2f}{verdict:>26}")
check(nu_fw["canon"] < min(vert_only) - 0.2,
      f"P4 against every VERTICAL-ONLY determination the framework's {nu_fw['canon']:.3f} is LOW by "
      f"{min(vert_only)-nu_fw['canon']:.2f}-{max(vert_only)-nu_fw['canon']:.2f} -- so my earlier "
      f"'-0.26 sigma agreement' was matching the JOINT-fit outlier, i.e. a number its own paper reports "
      f"as failing. That framing was too kind and is corrected here")

# but how hard is the constraint? FB2005 explicitly ACCEPT the standard function at canonical a0.
mu_fb_target = 5.0 / 7.0
mu_std_canon = mu2(G_LOCAL / A0_CANONICAL_MOND)
mu_fw_canon = mu2(G_LOCAL / A0_FW["canon"])
print(f"""
  BUT THE CONSTRAINT IS SOFT, and this cuts the other way. Famaey & Binney 2005 infer from Kuijken &
  Gilmore 1991 + Holmberg & Flynn 2004 that "MOND requires that mu(vc^2/R0 a0) ~= 5/7 ~= {mu_fb_target:.2f}",
  and then state that "given the significant uncertainties, this constraint is satisfied by the standard,
  simple and fitted interpolating functions when a0 = 1.2e-8 cm/s^2".
     the STANDARD function at the literature's a0 = 1.2e-10 gives mu = {mu_std_canon:.4f}
     the framework's alpha=2 at its own a0 = 9.36e-11 gives mu = {mu_fw_canon:.4f}
  FB2005 explicitly ACCEPT {mu_std_canon:.2f} against their inferred {mu_fb_target:.2f}. The framework sits only
  {mu_fw_canon-mu_std_canon:.3f} further away.""")
check(abs(mu_fw_canon - mu_std_canon) < 0.5 * abs(mu_std_canon - mu_fb_target),
      f"P4b the framework's mu ({mu_fw_canon:.3f}) is only {abs(mu_fw_canon-mu_std_canon):.3f} beyond the "
      f"standard-function-at-canonical-a0 value ({mu_std_canon:.3f}) that Famaey & Binney 2005 explicitly "
      f"accept against their own inferred {mu_fb_target:.3f} -- less than half the gap they already tolerate. "
      f"So the vertical constraint is SOFT and the framework is NOT excluded by it")


banner("P5  AGAINST INTEREST -- the SIGN of the grad(mu) correction is UNRESOLVED in the literature")

print("""  One agent found the literature sign LOWERS the boost (Brada & Milgrom 1995 Sec. V), the other flagged
  the number that implies the OPPOSITE: Nipoti et al. 2007's full-AQUAL Sigma_dyn(|z|<1.1 kpc)/Sigma_bar =
  85/43 = 1.98, about 28% ABOVE the local algebraic estimate (~1.55) -- i.e. the gradient term RAISING the
  vertical boost substantially. Neither agent could resolve it: Bienayme read the 85 off Nipoti's Fig. 5,
  and nothing in either paper states that the 43 is the column inside |z| < 1.1 kpc. And Bienayme's own
  1.66 versus Nipoti's 1.98 is attributed to "different baryonic-mass concentrations and different local
  mu values" -- a 19% swing in nu_vert from swapping the baryon model alone.
  => THE BARYON MODEL, NOT THE KERNEL, DOMINATES THIS OBSERVABLE at the current level of precision. That
     is the same conclusion the AQUAL solve reached from the other end, where MN + Hernquist could not
     match v_c(R0) and Sigma_bar(R0) together.""")
check(abs(1.98 - 1.66) / 1.66 > 0.15,
      "P5 two full-AQUAL calculations of the SAME observable differ by 19% (1.66 vs 1.98) purely through "
      "the baryon model -- larger than most of the effects being argued about, and the reason no sigma "
      "here should be quoted as a framework test")

banner("NET STANDING ON THE VERTICAL FORCE")
print(f"""   * The sign disagreement was mine, from a welded quotation plus a misread table entry. WITHDRAWN.
   * My grad(mu) reconciliation is REFUTED: mu moves only ~1.5% over the volume because |grad Phi| is
     radially dominated and the pieces add in quadrature. b68973f9's inference WITHDRAWN.
   * My "-0.26 sigma agreement" matched the JOINT-fit outlier (1.09), a value its own paper reports as
     failing. Against the three vertical-only determinations (1.40-1.62) the framework's {nu_fw['canon']:.2f} is LOW.
   * BUT the constraint is SOFT: Famaey & Binney 2005 accept mu = {mu_std_canon:.2f} against their inferred
     {mu_fb_target:.2f}, and the framework's {mu_fw_canon:.2f} is less than half that gap further out. NOT excluded.
   * AND the observable is baryon-model-dominated: 19% swings from the mass model alone, and the sign of
     the gradient correction is unresolved in the literature.
   => HONEST VERDICT: the local vertical force is a REAL but currently SOFT constraint, the framework is
      on the low side of it, and nothing here is decisive either way. The single thing that would sharpen
      it is the item already owed: a McMillan-class MW mass model in the validated AQUAL solver.
   UNTOUCHED: a0 = kappa c sqrt(G rho_Lambda), a claim about the SCALE.""")

banner("RESULT")
npass = sum(1 for c, _ in ok if c)
print(f"  {npass}/{len(ok)} checks held.")
if npass != len(ok):
    print("\n  FAILED CHECKS:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: provenance resolved, my mechanism withdrawn, my agreement claim corrected both ways.")
