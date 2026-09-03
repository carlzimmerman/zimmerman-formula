#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k03 -- TWO SHAPE LAWS FOR PRESSURE-SUPPORTED DWARFS (angle 10: "the SHAPE of relations, not their
zero-points"; the zero point of this relation is already a recorded liability -- items 8, 43, 44 --
so the whole question here is whether the SHAPE survives where the normalisation does not).

LAW A (the size-independence law, and its transition).  For an isolated system deep in the MOND regime
Milgrom's virial theorem makes the velocity dispersion depend on the mass ALONE, so

        d log sigma / d log r_half  |_{M fixed}  =  0        (isolated, g << a_0)
        d log sigma / d log r_half  |_{M fixed}  = -1/2      (external field or internal field >> a_0)

    and the framework says WHICH regime a given dwarf is in, using only measured quantities and a_0.
    RESTATEMENT TEST: does this follow from v^4 = G M_b a_0?  YES for the isolated limit -- sigma^4 =
    (4/81) G M a_0 is that law with the virial theorem in place of a circular orbit, so "sigma does not
    depend on size" is a corollary and the isolated half is a RESTATEMENT.  It does NOT close for the
    transition: the location of the switch is set by the external field, which v^4 = G M a_0 knows
    nothing about.  Labelled accordingly: half restatement, half not.

LAW B (the external-field law in the regime where it actually bites).  k02 found that in the Local
    Volume field the external field is 0.009 a_0 and the framework and LambdaCDM are indistinguishable.
    Local Group satellites are the opposite case: g_e/g_internal is of order unity, so

        d log sigma / d log g_e  |_{M fixed}  =  PREDICTED, non-zero    (framework)
                                              =  0 EXACTLY             (GR + CDM, strong equivalence)

    RESTATEMENT TEST: does NOT close.  v^4 = G M_b a_0 is a statement about an isolated system.

UPSILON LEVER: both statistics are recomputed at Upsilon_V = 1, 2 and 5 and the levers are printed.
    The zero point of this relation is known to need Upsilon_V ~ 20-109 (items 8, 43, 44) and that
    liability is NOT re-litigated here; it is restated and then set aside, because a slope at fixed
    luminosity is first-order blind to a constant Upsilon.

BUG PATTERNS: (1) total-vs-enclosed -- the half-light mass M/2 is used inside r_half, not the total;
    (2) spherical-on-a-disc -- these systems are pressure supported and round, so the spherical
    estimator is the right one here; (5) joint-fit degeneracy -- sigma and r_half come from different
    measurements (spectroscopy vs photometry) and M_* comes from photometry alone, so none of the three
    axes is fitted against another.  Upper limits on sigma are dropped, not censored-in.
"""
import os, sys, math, csv
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import Check, P, info, A0, DATA, nu

G = 6.674e-11
MSUN = 1.989e30
PC = 3.0856775814913673e16
KPC = 1e3*PC
MSUN_V = 4.83                     # absolute V magnitude of the Sun

HOSTS = {"mw":  ("Milky Way",      6.0e10, "distance_gc"),
         "m31": ("M31",            1.2e11, "distance_host"),
         "lg":  ("Local Group",    1.8e11, "distance_lg")}


def load(fn, branch):
    out = []
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
        try:
            if r["vlos_sigma_ul"].strip(): continue          # upper limit -- dropped, not censored in
            sig = float(r["vlos_sigma"]); rh = float(r["rhalf_physical"]); MV = float(r["M_V"])
            dkey = HOSTS[branch][2]
            dh = float(r[dkey])
        except Exception:
            continue
        if not (sig > 0 and rh > 0 and dh > 0): continue
        out.append(dict(name=r["name"], sigma=sig*1e3, rh=rh*PC, MV=MV, dhost=dh*KPC, branch=branch))
    return out


def build(gal, ups_v, a0):
    LV = np.array([10**(0.4*(MSUN_V - g["MV"])) for g in gal])
    Ms = ups_v*LV*MSUN
    rh = np.array([g["rh"] for g in gal])
    sig = np.array([g["sigma"] for g in gal])
    dh = np.array([g["dhost"] for g in gal])
    Mh = np.array([HOSTS[g["branch"]][1] for g in gal])*MSUN
    gNe = G*Mh/dh**2
    ge = nu(gNe/a0)*gNe                                    # MOND-boosted host field
    # internal Newtonian field of the half-mass inside r_half
    gNin = G*(Ms/2.0)/rh**2
    # Newtonian-equivalent external field (invert nu(yN) yN = y_e)
    y_e = ge/a0
    lo, hi = np.full_like(y_e, 1e-12), np.full_like(y_e, 1e12)
    for _ in range(200):
        mid = np.sqrt(lo*hi); f = nu(mid)*mid
        lo = np.where(f < y_e, mid, lo); hi = np.where(f < y_e, hi, mid)
    gNe_eq = np.sqrt(lo*hi)*a0
    gin = gNin*nu((gNin + gNe_eq)/a0)
    sig_pred = np.sqrt(gin*rh/3.0)                         # Wolf: M_1/2 = 3 sigma^2 r_h / G
    # the isolated deep-MOND closed form, as a cross-check of the coefficient
    sig_iso = ((4.0/81.0)*G*Ms*a0)**0.25
    return dict(LV=LV, Ms=Ms, rh=rh, sig=sig, ge=ge, gNin=gNin, sig_pred=sig_pred, sig_iso=sig_iso,
                branch=np.array([g["branch"] for g in gal]), names=[g["name"] for g in gal])


def partial(y, x1, x2, nboot=4000, seed=5):
    """y = a x1 + b x2 + c.  Returns (a, err_a, b)."""
    rng = np.random.default_rng(seed)
    ok = np.isfinite(y) & np.isfinite(x1) & np.isfinite(x2)
    Y = y[ok]; X = np.vstack([x1[ok], x2[ok], np.ones(ok.sum())]).T
    c = np.linalg.lstsq(X, Y, rcond=None)[0]
    bs = []
    for _ in range(nboot):
        k = rng.integers(0, len(Y), len(Y))
        try: bs.append(np.linalg.lstsq(X[k], Y[k], rcond=None)[0][0])
        except Exception: pass
    return c[0], float(np.std(bs)), c[1]


def main():
    ck = Check()
    P("="*120)
    P("k03 -- TWO SHAPE LAWS FOR PRESSURE-SUPPORTED DWARFS: sigma versus SIZE and versus EXTERNAL FIELD, "
      "both at fixed stellar mass")
    P("="*120)
    gal = (load("lvd_dwarf_mw.csv", "mw") + load("lvd_dwarf_m31.csv", "m31")
           + load("lvd_dwarf_local_field.csv", "lg"))
    nb = {b: sum(1 for g in gal if g["branch"] == b) for b in ("mw", "m31", "lg")}
    info(f"Local Volume Database dwarfs with a measured (not upper-limit) dispersion, a half-light radius and "
         f"an absolute magnitude: N = {len(gal)}  ({nb['mw']} MW satellites, {nb['m31']} M31 satellites, "
         f"{nb['lg']} isolated/field)")

    res = {}
    for foot, a0 in A0.items():
        d = build(gal, 2.0, a0)
        lsig = np.log10(d["sig"]); lrh = np.log10(d["rh"]); lMs = np.log10(d["Ms"])
        lge = np.log10(d["ge"]/a0)
        lsp = np.log10(d["sig_pred"])
        P("")
        P("-"*120)
        P(f"FOOTING {foot}   a_0 = {a0:.3e}   (Upsilon_V = 2.0 for the headline; swept below)")
        P("-"*120)
        info(f"  external field spans g_e/a_0 = {(d['ge']/a0).min():.3f} to {(d['ge']/a0).max():.3f}, "
             f"median {np.median(d['ge']/a0):.3f}   <-- unlike the Local Volume discs of k02, this is O(1)")
        info(f"  internal field spans g_in,N/a_0 = {(d['gNin']/a0).min():.4f} to {(d['gNin']/a0).max():.3f}, "
             f"median {np.median(d['gNin']/a0):.4f}")
        info(f"  ZERO POINT (a known liability, restated not re-litigated): "
             f"mean log(sigma_obs/sigma_pred) = {np.mean(lsig - lsp):+.3f} dex, sd {np.std(lsig-lsp):.3f}")

        # LAW A: size dependence at fixed stellar mass
        aA, eA, _ = partial(lsig, lrh, lMs)
        aAp, eAp, _ = partial(lsp, lrh, lMs)
        info("")
        info(f"  LAW A   d log sigma / d log r_half at fixed log M_*:")
        info(f"      observed   {aA:+.3f} +- {eA:.3f}")
        info(f"      framework  {aAp:+.3f}   (0 if every dwarf were isolated and deep-MOND; -1/2 if Newtonian)")
        info(f"      Newton on the same baryons: -0.500 exactly;  LambdaCDM with cuspy halos: about 0 to +0.5")

        # LAW B: external-field dependence at fixed stellar mass
        aB, eB, _ = partial(lsig, lge, lMs)
        aBp, eBp, _ = partial(lsp, lge, lMs)
        info("")
        info(f"  LAW B   d log sigma / d log(g_e/a_0) at fixed log M_*:")
        info(f"      observed   {aB:+.3f} +- {eB:.3f}")
        info(f"      framework  {aBp:+.3f}   |   GR + cold dark matter (strong equivalence): 0.000 EXACTLY")
        res[foot] = dict(A=(aA, eA, aAp), B=(aB, eB, aBp), d=d, lsig=lsig, lrh=lrh, lMs=lMs, lge=lge, lsp=lsp)

    a0 = A0["canonical"]; r = res["canonical"]; d = r["d"]
    P("")
    P("="*120); P("CHECKS"); P("="*120)

    # 1 -- the isolated closed form must reproduce the Wolf-based prediction where the EFE is off
    iso = d["ge"]/a0 < 0.05
    if iso.sum() >= 3:
        rat = np.log10(d["sig_pred"][iso]/d["sig_iso"][iso])
        ck("k03-1 the machinery reproduces the closed form it must reduce to: for the least-disturbed dwarfs "
           "the Wolf-estimator prediction and Milgrom's isolated deep-MOND sigma^4 = (4/81) G M a_0 must agree "
           "to better than 0.1 dex, or my EFE prescription is doing something the limit forbids",
           abs(np.mean(rat)) < 0.1, f"N = {int(iso.sum())} with g_e < 0.05 a_0, "
           f"mean log(sigma_Wolf/sigma_closed-form) = {np.mean(rat):+.3f} dex")
    else:
        ck("k03-1 the machinery reproduces the closed form it must reduce to", False,
           f"only {int(iso.sum())} dwarfs have g_e < 0.05 a_0 -- the limit cannot be checked on this sample")

    # 2 -- does the sample have a lever in each direction?
    ck("k03-2 POWER, asked before the answer: the framework's OWN predicted size-slope must differ from both "
       "0 and -1/2 by more than the measurement error, or LAW A cannot be tested here",
       min(abs(r["A"][2] - 0.0), abs(r["A"][2] + 0.5)) > r["A"][1],
       f"framework predicts {r['A'][2]:+.3f}; measurement error {r['A'][1]:.3f}; "
       f"distance to 0 is {abs(r['A'][2]):.3f}, to -1/2 is {abs(r['A'][2]+0.5):.3f}")

    ck("k03-3 POWER for LAW B: the framework's own predicted external-field slope must be separated from "
       "LambdaCDM's exact zero by more than the measurement error",
       abs(r["B"][2]) > r["B"][1],
       f"framework predicts {r['B'][2]:+.3f}; measurement error {r['B'][1]:.3f}")

    # 4 -- mutation on the MEASUREMENT, not on the formula: shuffle which dwarf feels which external field
    #      and re-measure the OBSERVED slope.  The shuffled slope must be consistent with zero, or the
    #      +/-0.1 seen in the data is an artefact of the sample's marginal distributions.
    rng = np.random.default_rng(19)
    sh = []
    for _ in range(2000):
        perm = rng.permutation(len(d["ge"]))
        sh.append(partial(r["lsig"], r["lge"][perm], r["lMs"], nboot=1)[0])
    sh = np.array(sh)
    zsh = (r["B"][0] - sh.mean())/sh.std()
    ck("k03-4 MUTATION on the measurement: shuffling which dwarf feels which external field must destroy the "
       "OBSERVED law-B slope.  If the shuffled slope is as large as the real one, the trend is an artefact of "
       "the sample's marginal distributions and not a real dependence on environment",
       abs(zsh) > 2.0, f"real {r['B'][0]:+.3f} vs shuffled {sh.mean():+.3f} +- {sh.std():.3f} -> {zsh:+.1f} sigma")

    # 4b -- branch split: is the observed law-B trend the same around both hosts, or is it a Milky Way effect?
    P("")
    info("LAW B split by host, because tidal heating (in EITHER theory) would concentrate in the best-studied, "
         "closest satellites:")
    for br in ("mw", "m31", "lg"):
        m = d["branch"] == br
        if m.sum() >= 8:
            ab, eb, _ = partial(r["lsig"][m], r["lge"][m], r["lMs"][m])
            apb, _, _ = partial(r["lsp"][m], r["lge"][m], r["lMs"][m])
            info(f"   {HOSTS[br][0]:<12s} N = {int(m.sum()):3d}:  observed {ab:+.3f} +- {eb:.3f}   "
                 f"framework {apb:+.3f}   GR+CDM 0.000")
        else:
            info(f"   {HOSTS[br][0]:<12s} N = {int(m.sum()):3d}:  too few for a slope")

    # 5 -- mutation: a 4x wrong a_0
    d4 = build(gal, 2.0, 4*a0)
    aA4, _, _ = partial(np.log10(d4["sig_pred"]), np.log10(d4["rh"]), np.log10(d4["Ms"]))
    ck("k03-5 MUTATION: a four-times-wrong a_0 must change the framework's predicted size-slope, or the "
       "prediction does not know about a_0 at all and the item is not testing the framework",
       abs(aA4 - r["A"][2]) > 0.02, f"a_0 -> 4 a_0 moves the predicted size-slope {r['A'][2]:+.3f} -> {aA4:+.3f}")

    # 6 -- mutation: kernel off
    dN = build(gal, 2.0, a0)
    sigN = np.sqrt(dN["gNin"]*dN["rh"]/3.0)
    aAN, _, _ = partial(np.log10(sigN), np.log10(dN["rh"]), np.log10(dN["Ms"]))
    ck("k03-6 MUTATION: with the kernel off the predicted size-slope must be exactly -1/2, the Newtonian "
       "value -- this verifies the estimator rather than the physics",
       abs(aAN + 0.5) < 0.02, f"Newtonian predicted size-slope = {aAN:+.4f} against the analytic -0.5")

    # 7 -- Upsilon lever
    P("")
    info("UPSILON LEVER, measured:")
    lev = {}
    for u in (1.0, 2.0, 5.0):
        du = build(gal, u, a0)
        ls = np.log10(du["sig"]); lr = np.log10(du["rh"]); lm = np.log10(du["Ms"]); lg = np.log10(du["ge"]/a0)
        aAu, eAu, _ = partial(ls, lr, lm)
        aBu, eBu, _ = partial(ls, lg, lm)
        aApu, _, _ = partial(np.log10(du["sig_pred"]), lr, lm)
        aBpu, _, _ = partial(np.log10(du["sig_pred"]), lg, lm)
        zp = np.mean(ls - np.log10(du["sig_pred"]))
        lev[u] = (aAu, aBu, aApu, aBpu, zp)
        info(f"   Upsilon_V = {u:.1f}:  LAW A obs {aAu:+.3f} (pred {aApu:+.3f})   "
             f"LAW B obs {aBu:+.3f} (pred {aBpu:+.3f})   zero point {zp:+.3f} dex")
    dlu = math.log10(5.0/1.0)
    dzp = (lev[5.0][4] - lev[1.0][4])/dlu
    dA = (lev[5.0][0] - lev[1.0][0])/dlu
    dB = (lev[5.0][1] - lev[1.0][1])/dlu
    dAp = (lev[5.0][2] - lev[1.0][2])/dlu
    dBp = (lev[5.0][3] - lev[1.0][3])/dlu
    info(f"   d(zero point)/d log Upsilon_V   = {dzp:+.3f} dex per dex     <-- the known liability's own lever")
    info(f"   d(LAW A observed)/d log Upsilon = {dA:+.4f} per dex   d(LAW A predicted)/d log Ups = {dAp:+.4f}")
    info(f"   d(LAW B observed)/d log Upsilon = {dB:+.4f} per dex   d(LAW B predicted)/d log Ups = {dBp:+.4f}")
    ck("k03-7 UPSILON LEVER: the OBSERVED slopes must be essentially blind to Upsilon (they use only measured "
       "sigma, r_half and luminosity, so a constant Upsilon is absorbed in the intercept).  This check verifies "
       "that claim numerically instead of asserting it",
       abs(dA) < 0.01 and abs(dB) < 0.01,
       f"|d LAW A/d log Ups| = {abs(dA):.5f}, |d LAW B/d log Ups| = {abs(dB):.5f} per dex, against a zero-point "
       f"lever of {abs(dzp):.3f} dex per dex")

    rc = ck.done()

    P("")
    P("="*120); P("VERDICT -- k03"); P("="*120)
    for foot in ("canonical", "alt"):
        aA, eA, aAp = res[foot]["A"]; aB, eB, aBp = res[foot]["B"]
        P(f"  {foot}:")
        P(f"    LAW A  size-slope at fixed M_*   observed {aA:+.3f} +- {eA:.3f} | framework {aAp:+.3f} "
          f"({abs(aA-aAp)/eA:.1f} sigma) | Newton -0.500 ({abs(aA+0.5)/eA:.1f} sigma)")
        P(f"    LAW B  field-slope at fixed M_*  observed {aB:+.3f} +- {eB:.3f} | framework {aBp:+.3f} "
          f"({abs(aB-aBp)/eB:.1f} sigma) | GR+CDM 0.000 ({abs(aB)/eB:.1f} sigma)")
    P("")
    P("  LAW A -- a modest PASS.  The framework's mixed-regime prediction sits 1.2 sigma from the data while")
    P("  pure Newton on the same baryons (-1/2) is 3.4 sigma away and a cuspy dark halo (0 to +1/2) is further")
    P("  still.  The size-slope is the one thing in the pressure-supported channel that works.")
    P("")
    P("  LAW B -- a 4 sigma FAILURE, and it is the framework's own distinctive content that fails.  The")
    P("  external-field effect predicts satellites in stronger host fields to have LOWER dispersions at fixed")
    P("  stellar mass; the data show the opposite sign, and around the Milky Way alone -- where the field is")
    P("  strongest and best measured -- the gap is 5 sigma.  GR + cold dark matter's exact zero is 1.7 sigma away.")
    P("  THE CAVEAT, STATED BOTH WAYS: tidal heating and disruption inflate the dispersions of close satellites")
    P("  in EITHER theory, and that confound pushes the measured slope POSITIVE -- i.e. against the framework.")
    P("  So this is a liability recorded at face value, not a clean kill; a tidally-cleaned sample could move it.")
    P("  It points the same way as items 8, 43, 44 (dwarfs need Upsilon_V of 20-109) and item 9 (the Coma")
    P("  ultra-diffuse kill, whose offset also TRACKED the external field).  Four independent Local Group and")
    P("  cluster-dwarf tests now say the same thing about the external-field effect.")
    P("")
    P("  The observed slopes here use ONLY measured quantities -- a spectroscopic dispersion, a photometric")
    P("  half-light radius, an absolute magnitude and a host distance -- and are blind to the stellar")
    P("  mass-to-light ratio by construction (check k03-7).  That is what makes them worth quoting even though")
    P("  the zero point of the same relation is a standing liability of this framework.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
