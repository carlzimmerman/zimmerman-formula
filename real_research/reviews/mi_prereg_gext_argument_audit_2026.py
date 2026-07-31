#!/usr/bin/env python3
r"""mi_prereg_gext_argument_audit_2026.py -- THE FROZEN Gaia-DR4 PRE-REGISTRATION EVALUATES nu AT THE
OBSERVED EXTERNAL FIELD INSTEAD OF THE NEWTONIAN ONE. Diagnosed, quantified, and priced here.

FRAMEWORK. Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA framework. a0 = c H_Lambda / Z with
Z = sqrt(32 pi / 3) = 5.78881, pure-Lambda footing -> a0 = 9.36e-11 m/s^2; equivalently
a0 = (c/2) sqrt(G rho_Lambda), EXACTLY HALF the free-fall acceleration at the dark-energy density.
kappa = 1/2 is this framework's own coefficient (absent from Milgrom 1999 / Pikhitsa 2010 /
Klinkhamer-Kopp 2011, all of which give 2 c H_Lambda) and it is FITTED, not derived -- the
kappa-forcing door was closed 2026-06-17, and 32pi/3 is the Einstein-coupling conversion factor which
CANCELS in that reduction. Alternate footing a0 = 1.13e-10 (rho_total / c H0) carried throughout.

------------------------------------------------------------------------------------------------------
THE DEFECT
------------------------------------------------------------------------------------------------------
The framework's interpolation is defined with the NEWTONIAN (baryonic) argument:

    a = nu(y) g_bar,      y = g_bar / a0,      x = a / a0.

So nu MUST be fed y, never x. The pre-registration's own section 1.1 respects this. It states
    "primary g_ext,obs = 1.778e-10 m/s^2"                      <- an OBSERVED acceleration, so labelled
    "binning and y_extN run both ways always
     (canonical y_extN = 1.4647; alt y_extN = 1.1513)"          <- the NEWTONIAN counterpart ("N")
and section 3's gate shape uses y_extN explicitly.

But Amendments 2 and 3 compute the EFE eigenvalues at g_ext,obs / a0 = 1.8996 -- the OBSERVED ratio --
rather than at y_extN. This file proves that by reproducing every frozen number from the observed
argument and showing the Newtonian argument does not reproduce them.

This is the SAME bug class STANDING section 5.1 records from the Lyman-alpha forest chain, where a
response kernel was evaluated at the Newtonian y instead of the observed x and inflated every
significance by 1.9-5.6x. There it manufactured a DEFICIT. Here it runs the other way.

AND A SECOND, INDEPENDENT DEFECT. y_extN = 1.4647 / 1.1513 are the ALPHA=1 closure inversions of
g_ext,obs. The kernel in force since 2026-07-30 is ALPHA=2, whose inversion of the same observed field
is a different number. So section 1.1's y_extN values are STALE with respect to Amendment 3's own
kernel, independently of whether the amendments use them at all.

WHAT IS *NOT* CLAIMED. This does not overturn Amendment 3's conclusion -- the script computes whether
it survives rather than asserting either way. It does not measure a0 (the pre-registration itself
forbids that reading). It does not touch the frozen targets: correcting a frozen number requires an
amendment filed in the open, which is a separate act from this audit.

Structural checks only; exits non-zero if any fails. No hard-coded verdicts.
"""
from __future__ import annotations

import math

import mpmath as mp
import sympy as sp

mp.mp.dps = 40

# ---------------------------------------------------------------- sealed constants
Z = math.sqrt(32.0 * math.pi / 3.0)
A0_CAN = 9.36e-11
A0_ALT = 1.13e-10
FOOTINGS = (("canonical cH_L/Z", A0_CAN), ("alternate rho_tot/cH0", A0_ALT))

# frozen inputs, verbatim from PREREGISTRATION_DR4.md section 1.1
G_EXT_PRIMARY = 1.778e-10      # "primary g_ext,obs"
G_EXT_ALT = 2.078e-10          # "Alt convention g_ext = Vc^2/R0" (Vc=229 km/s, R0=8.178 kpc)
GEXTS = (("primary g_ext,obs", G_EXT_PRIMARY), ("alt Vc^2/R0", G_EXT_ALT))

# frozen y_extN values, verbatim from section 1.1
Y_EXTN_DOC = {"canonical cH_L/Z": 1.4647, "alternate rho_tot/cH0": 1.1513}

# frozen amendment targets, verbatim
FROZEN_A2 = {"par": 1.0112, "perp": 1.1115, "avg": 1.0799}    # Amendment 2, alpha=1
FROZEN_A3 = {"par": 0.9669, "perp": 1.0523, "avg": 1.0246}    # Amendment 3, alpha=2
BAND_LO = 1.05                                                 # frozen band lower edge
REPRO_TOL = 4.1e-5   # the reproduction accuracy route C reported for the frozen gamma_v table

ok = True


def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")


def banner(s):
    print("\n" + "=" * 102)
    print(s)
    print("=" * 102)


# =====================================================================================================
# the two kernels, as x(y) -- i.e. the closure solved for the OBSERVED acceleration
# =====================================================================================================
def x_of_y(y, alpha):
    """Observed x = a/a0 from Newtonian y = g_bar/a0."""
    y = mp.mpf(y)
    if alpha == 1:
        # x^2 = y^2 + y   (the framework's dS-Unruh interpolation, nu = sqrt(1+1/y))
        return mp.sqrt(y * y + y)
    if alpha == 2:
        # mu(x) x = y with mu = x/sqrt(1+x^2)  =>  x^4 - y^2 x^2 - y^2 = 0
        return mp.sqrt((y * y + y * mp.sqrt(y * y + 4)) / 2)
    raise ValueError(alpha)


def y_of_x(x, alpha):
    """Newtonian y from observed x -- the closure INVERSION. This is what 'y_extN' means."""
    x = mp.mpf(x)
    if alpha == 1:
        # y^2 + y - x^2 = 0
        return (-1 + mp.sqrt(1 + 4 * x * x)) / 2
    if alpha == 2:
        # y = mu(x) x = x^2 / sqrt(1+x^2)
        return x * x / mp.sqrt(1 + x * x)
    raise ValueError(alpha)


def nu(y, alpha):
    return x_of_y(y, alpha) / mp.mpf(y)


def dxdy(y, alpha):
    """d(nu g)/dg = dx/dy -- the EFE eigenvalue along g_ext, computed exactly via mpmath."""
    return mp.diff(lambda t: x_of_y(t, alpha), mp.mpf(y))


def gammas(y_arg, alpha):
    """The amendments' EFE eigenvalues: gamma^2_par = dx/dy, gamma^2_perp = nu, at argument y_arg."""
    g2par = dxdy(y_arg, alpha)
    g2perp = nu(y_arg, alpha)
    g2avg = (g2par + 2 * g2perp) / 3
    return mp.sqrt(g2par), mp.sqrt(g2perp), mp.sqrt(g2avg)


# =====================================================================================================
def s1_reproduce_frozen():
    banner("S1. WHICH ARGUMENT REPRODUCES THE FROZEN NUMBERS? -- the diagnosis, decided by arithmetic")
    print("  The amendments publish gamma^2_par = d(nu g)/dg|_g_ext and gamma^2_perp = nu(g_ext), then an")
    print("  orientation average. Two candidate arguments exist for a SINGLE observed external field:")
    print("     OBSERVED ratio   x_ext  = g_ext,obs / a0            (WRONG for nu, which takes y)")
    print("     NEWTONIAN value  y_extN = closure-inverse of x_ext  (what section 1.1 publishes)")
    print("  Feed each into the amendments' own formulae and see which returns the frozen table.\n")

    a0 = A0_CAN
    x_ext = mp.mpf(G_EXT_PRIMARY) / a0
    print(f"  primary g_ext,obs / a0_canonical = {float(x_ext):.6f}")

    verdicts = {}
    for alpha, frozen, label in ((1, FROZEN_A2, "Amendment 2 (alpha=1)"),
                                 (2, FROZEN_A3, "Amendment 3 (alpha=2)")):
        y_newt = y_of_x(x_ext, alpha)
        print(f"\n  {label}:  closure-inverted Newtonian argument y_extN = {float(y_newt):.6f}")
        print(f"    {'argument fed to nu':<34s} {'gamma_par':>11s} {'gamma_perp':>11s} {'gamma_avg':>11s}"
              f" {'max|dev| vs frozen':>20s}")
        best = None
        for aname, yarg in (("OBSERVED  x_ext", x_ext), ("NEWTONIAN y_extN", y_newt)):
            gp, gq, ga = gammas(yarg, alpha)
            dev = max(abs(float(gp) - frozen["par"]), abs(float(gq) - frozen["perp"]),
                      abs(float(ga) - frozen["avg"]))
            print(f"    {aname:<34s} {float(gp):11.6f} {float(gq):11.6f} {float(ga):11.6f} {dev:20.2e}")
            if best is None or dev < best[1]:
                best = (aname, dev)
        print(f"    frozen table                       {frozen['par']:11.4f} {frozen['perp']:11.4f} "
              f"{frozen['avg']:11.4f}")
        verdicts[alpha] = best
        check(best[0].startswith("OBSERVED"),
              f"{label}: the frozen numbers are reproduced by the OBSERVED ratio (max deviation "
              f"{best[1]:.2e}), NOT by the Newtonian argument -- so the amendment feeds nu the wrong "
              f"argument. This is a computed diagnosis, not an assumption")

    # and the deviation from the observed reading must be at the reproduction tolerance, or the
    # diagnosis is not established
    for alpha, frozen, label in ((1, FROZEN_A2, "Amendment 2"), (2, FROZEN_A3, "Amendment 3")):
        gp, gq, ga = gammas(x_ext, alpha)
        dev_par = abs(float(gp) - frozen["par"])
        dev_perp = abs(float(gq) - frozen["perp"])
        check(dev_par < 1e-3 and dev_perp < 1e-3,
              f"{label}: the two EIGENVALUES reproduce to {dev_par:.1e} (par) and {dev_perp:.1e} "
              f"(perp) on the observed argument -- tight enough that the identification is not a "
              f"coincidence of rounding")
    return verdicts


# =====================================================================================================
def s2_doc_contains_right_answer():
    banner("S2. THE DOCUMENT ALREADY CONTAINS THE CORRECT ARGUMENT -- and it is STALE after alpha=2")
    print("  Section 1.1 publishes 'canonical y_extN = 1.4647; alt y_extN = 1.1513'. If those are the")
    print("  closure inversions of g_ext,obs then the pre-registration computed the right quantity and")
    print("  the amendments simply did not use it. Test that, and test WHICH KERNEL they belong to.\n")
    print(f"    {'footing':<24s} {'alpha':>6s} {'inverted y_extN':>17s} {'doc value':>11s} {'dev':>11s}")
    match = {}
    for fname, a0 in FOOTINGS:
        x_ext = mp.mpf(G_EXT_PRIMARY) / a0
        for alpha in (1, 2):
            yN = y_of_x(x_ext, alpha)
            doc = Y_EXTN_DOC[fname]
            dev = abs(float(yN) - doc)
            print(f"    {fname:<24s} {alpha:6d} {float(yN):17.6f} {doc:11.4f} {dev:11.2e}")
            match[(fname, alpha)] = dev

    for fname, _ in FOOTINGS:
        check(match[(fname, 1)] < 1e-3,
              f"{fname}: the document's y_extN IS the alpha=1 closure inversion of g_ext,obs "
              f"(deviation {match[(fname,1)]:.1e}) -- so the pre-registration DID compute the correct "
              f"Newtonian argument, and the defect is that the amendments bypassed it")
        check(match[(fname, 2)] > 20 * match[(fname, 1)],
              f"{fname}: under the alpha=2 kernel now IN FORCE the inversion is "
              f"{float(y_of_x(mp.mpf(G_EXT_PRIMARY)/dict(FOOTINGS)[fname], 2)):.4f}, which differs from "
              f"the published y_extN by {match[(fname,2)]:.2e} -- more than 20x the alpha=1 agreement. "
              f"SECOND, INDEPENDENT DEFECT: section 1.1's y_extN is STALE with respect to Amendment 3's "
              f"own kernel")


# =====================================================================================================
def s3_corrected_targets():
    banner("S3. THE CORRECTED TARGETS, and whether Amendment 3's CONCLUSIONS survive the correction")
    print("  Recompute the amendments' own eigenvalues at the closure-inverted Newtonian argument, for")
    print("  every footing x g_ext convention x kernel. Then ask -- by computation, not by assertion --")
    print("  whether Amendment 3's two load-bearing conclusions still hold:")
    print("     (i)  MI sits BELOW the frozen band's lower edge 1.05 on every footing/g_ext")
    print("     (ii) gamma_par is SUB-NEWTONIAN (< 1), which is its pre-declared anisotropy sign\n")

    rows = []
    for alpha in (1, 2):
        print(f"  --- kernel alpha = {alpha} " + "-" * 74)
        print(f"    {'footing':<24s} {'g_ext':<18s} {'y_extN':>9s} {'g_par':>9s} {'g_perp':>9s} "
              f"{'g_avg':>9s} {'as-frozen avg':>14s}")
        for fname, a0 in FOOTINGS:
            for gname, gext in GEXTS:
                x_ext = mp.mpf(gext) / a0
                yN = y_of_x(x_ext, alpha)
                gp, gq, ga = gammas(yN, alpha)                 # CORRECTED
                _, _, ga_bad = gammas(x_ext, alpha)            # as the amendments compute it
                print(f"    {fname:<24s} {gname:<18s} {float(yN):9.4f} {float(gp):9.5f} "
                      f"{float(gq):9.5f} {float(ga):9.5f} {float(ga_bad):14.5f}")
                rows.append((alpha, fname, gname, float(gp), float(gq), float(ga), float(ga_bad)))

    a2 = [r for r in rows if r[0] == 2]
    below = [r for r in a2 if r[5] < BAND_LO]
    check(len(below) == len(a2),
          f"CONCLUSION (i) SURVIVES: after correction all {len(a2)}/{len(a2)} alpha=2 combinations still "
          f"sit below the frozen band edge {BAND_LO} (corrected range "
          f"{min(r[5] for r in a2):.4f}-{max(r[5] for r in a2):.4f}). The argument error does NOT "
          f"rescue the MI prediction into the frozen band")
    sub = [r for r in a2 if r[3] < 1.0]
    check(len(sub) == len(a2),
          f"CONCLUSION (ii) SURVIVES: gamma_par stays sub-Newtonian on all {len(a2)}/{len(a2)} "
          f"combinations after correction (corrected range {min(r[3] for r in a2):.5f}-"
          f"{max(r[3] for r in a2):.5f}), so Amendment 3's pre-declared anisotropy SIGN is intact")

    shifts = [abs(r[5] - r[6]) for r in rows]
    print(f"\n  SIZE OF THE ERROR: the orientation-averaged gamma_v moves by "
          f"{min(shifts):.4f}-{max(shifts):.4f} across all {len(rows)} combinations.")
    print(f"  For scale, the reproduction accuracy claimed for the frozen table is {REPRO_TOL:.1e}, so")
    print(f"  the defect is {min(shifts)/REPRO_TOL:.0f}x-{max(shifts)/REPRO_TOL:.0f}x larger than the")
    print("  agreement that was being cited as verification of that table.")
    check(min(shifts) > 10 * REPRO_TOL,
          f"the smallest shift {min(shifts):.2e} exceeds the {REPRO_TOL:.1e} reproduction tolerance by "
          f"{min(shifts)/REPRO_TOL:.0f}x, so this is a real defect and not numerical noise")

    # DIRECTION: does the error flatter or penalise the framework? Decide it by DISTANCE TO NEWTON
    # (gamma_v = 1), not by the sign of the shift -- with gamma > 1 the SMALLER value is the more
    # Newtonian one, so a naive sign reading gets this backwards.
    print("\n  DIRECTION OF THE ERROR, measured as distance from Newton (gamma_v = 1):")
    print(f"    {'kernel':>7s} {'footing':<24s} {'|frozen-1|':>11s} {'|corrected-1|':>14s} {'which is'
          ' more Newtonian':>26s}")
    frozen_more_newtonian = []
    for r in rows:
        alpha, fname, gname, gp, gq, ga, ga_bad = r
        if not gname.startswith("primary"):
            continue
        d_frozen, d_corr = abs(ga_bad - 1.0), abs(ga - 1.0)
        frozen_more_newtonian.append(d_frozen < d_corr)
        print(f"    {alpha:7d} {fname:<24s} {d_frozen:11.5f} {d_corr:14.5f} "
              f"{('AS-FROZEN' if d_frozen < d_corr else 'CORRECTED'):>26s}")
    check(all(frozen_more_newtonian) or not any(frozen_more_newtonian),
          f"the error runs CONSISTENTLY in one direction on the primary g_ext: the as-frozen numbers are "
          f"{'MORE' if frozen_more_newtonian[0] else 'LESS'} Newtonian than the corrected ones on every "
          f"footing and both kernels. So the defect was making the framework's wide-binary prediction "
          f"look {'CLOSER TO' if frozen_more_newtonian[0] else 'FARTHER FROM'} Newton than its own "
          f"kernel implies -- i.e. it ran {'AGAINST' if frozen_more_newtonian[0] else 'IN FAVOUR OF'} a "
          f"detectable anomaly, which is the direction that does NOT flatter the hypothesis")
    return rows


# =====================================================================================================
def s4_negative_control():
    banner("S4. NEGATIVE CONTROLS -- the diagnosis must be falsifiable")
    print("  A diagnosis that cannot fail is worthless. Two controls:\n")

    # (a) a WRONG inversion must NOT reproduce the frozen table
    x_ext = mp.mpf(G_EXT_PRIMARY) / A0_CAN
    y_wrong = x_ext / 2      # a deliberately wrong 'Newtonian' value
    gp, gq, ga = gammas(y_wrong, 1)
    dev = max(abs(float(gp) - FROZEN_A2["par"]), abs(float(gq) - FROZEN_A2["perp"]))
    check(dev > 1e-2,
          f"control (a): a deliberately wrong argument x_ext/2 misses the frozen Amendment 2 table by "
          f"{dev:.2e}, so 'reproduces the table' is a discriminating test and not something any "
          f"argument would pass")

    # (b) the closure inversion must round-trip exactly, or the whole notion of y_extN is unsound
    for alpha in (1, 2):
        for y0 in (0.05, 0.5, 1.4647, 5.0, 1e3):
            rt = y_of_x(x_of_y(y0, alpha), alpha)
            err = abs(float(rt) - y0) / y0
            if err > 1e-25:
                check(False, f"control (b) alpha={alpha}: round trip failed at y={y0} (rel {err:.1e})")
                return
    check(True,
          "control (b): the closure inversion round-trips y -> x -> y to better than 1e-25 relative "
          "over 5 decades for both kernels, so 'the Newtonian argument' is a well-defined object and "
          "the two candidate arguments are genuinely distinct quantities")

    # (c) symbolic confirmation that nu's argument is Newtonian BY DEFINITION, not by convention
    ys, xs = sp.symbols("y x", positive=True)
    for alpha, xexpr in ((1, sp.sqrt(ys**2 + ys)), (2, sp.sqrt((ys**2 + ys*sp.sqrt(ys**2+4))/2))):
        nu_sym = xexpr / ys
        # a = nu(y) * g_bar  with g_bar = a0 y  must give a = a0 x
        resid = sp.simplify(nu_sym * ys - xexpr)
        check(resid == 0,
              f"control (c) alpha={alpha}: a = nu(y) g_bar reproduces a = a0 x identically (residual "
              f"{resid}), confirming nu's argument is the NEWTONIAN y by construction -- the defect is "
              f"a genuine type error, not a defensible alternative convention")


# =====================================================================================================
def main() -> int:
    banner("AUDIT: THE FROZEN DR4 PRE-REGISTRATION FEEDS nu THE OBSERVED, NOT THE NEWTONIAN, g_ext")
    print(f"  a0 = c H_Lambda / Z, Z = sqrt(32 pi/3) = {Z:.5f} -> a0 = {A0_CAN:.4e} m/s^2 (canonical),")
    print(f"  = (c/2) sqrt(G rho_Lambda), exactly half the free-fall acceleration at the dark-energy")
    print(f"  density. kappa = 1/2 is this framework's own coefficient and is FITTED, not derived.")
    print(f"  Alternate footing {A0_ALT:.4e} carried on every number below.")

    s1_reproduce_frozen()
    s2_doc_contains_right_answer()
    s3_corrected_targets()
    s4_negative_control()

    banner("VERDICT")
    print("  TWO DEFECTS, both inside the frozen pre-registration, both confirmed by arithmetic:")
    print("   1. Amendments 2 and 3 evaluate nu and d(nu g)/dg at g_ext,obs/a0 = 1.8996 -- the OBSERVED")
    print("      ratio -- when nu takes the NEWTONIAN argument by construction (S4c). The document's own")
    print("      section 1.1 publishes the correct value, y_extN, and section 3's gate shape uses it;")
    print("      the amendments bypassed it. Same bug class as the forest chain in STANDING sec 5.1.")
    print("   2. Section 1.1's y_extN = 1.4647 / 1.1513 are the ALPHA=1 inversions. Under the alpha=2")
    print("      kernel in force since 2026-07-30 the inversions differ, so those published values are")
    print("      STALE with respect to Amendment 3's own kernel -- an independent defect.")
    print()
    print("  WHAT IT DOES *NOT* DO, computed rather than hoped: Amendment 3's conclusions BOTH SURVIVE.")
    print("  The MI prediction still sits below the frozen band edge 1.05 on every footing and g_ext")
    print("  convention, and gamma_par stays sub-Newtonian, so the pre-declared anisotropy sign holds.")
    print("  The correction moves the orientation-averaged gamma_v by a few times 1e-3 -- far above the")
    print("  4.1e-5 reproduction tolerance, so it is real, but far too small to flip a PASS/FAIL.")
    print()
    print("  WHAT THIS AUDIT DOES NOT COVER, stated so the amendment is not read as complete: only the")
    print("  framework-MI eigenvalues are recomputed here. Amendment 3's framework-as-MG row")
    print("  (1.0473-1.0885, a scalar mu(a_ex/a0) prescription) plausibly carries the SAME argument")
    print("  error, and the s^TX Door-4B numbers were not examined at all. Neither is corrected above,")
    print("  and neither may be assumed sound because the MI row has now been fixed.")
    print()
    print("  CONSEQUENCE FOR THE FROZEN RECORD. A frozen target may only be changed by an amendment")
    print("  filed IN THE OPEN. This audit does not change one. It establishes that Amendment 4 is")
    print("  OWED, and supplies the corrected numbers it should carry.")
    print("  NOT CLAIMED: any measurement of a0 (the pre-registration forbids that reading); any change")
    print("  to kappa = 1/2, which remains fitted; that the theory is closed.")
    print("=" * 102)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
