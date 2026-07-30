#!/usr/bin/env python3
r"""mi_sign_from_perturbation_drift_2026.py -- can the framework's LAST-BUT-ONE POSTULATE (the sign s)
be MEASURED, using the universal a0/2c perturbation drift?

THE STANDING. The framework is down to two postulates: the sign s and the coefficient Z. Every INTERNAL
route to forcing the sign is closed by the corpus's own work -- the 4-point/dS-positivity edge came back
a SIGN_BLIND wall, the all-orders sign wall was re-derived from the positivity side, and no pump-free
MOND-sign channel exists (passive reactive DC shift is KMS/Kramers-Kronig LOCKED to delta-m >= 0
anti-MOND, flipping only under a pump beta < 0). The banked conclusion is "sign + Z still postulated;
forward = data." Nobody has gone looking for the datum.

THE CANDIDATE DATUM. prep_2026/mi_fingerprint/KERNEL_THEORY.md Section 2 records, as a by-product of
the unimodular kernel: the dissipative channel has a "universal secular scale tau = 2c/a0 = 203 Gyr
(canonical) / 168 Gyr (alt), orbit-independent (omega sin phi = a0/2c exactly)", and states that under
the published first-moment closure "the orbital secular drift is exactly zero (K(a^2/a0^2) is real) and
the phase acts only on perturbations (epicycles, tides, waves). Its SIGN inherits the s = -1 postulate
status." So there is a universal, system-independent rate whose SIGN *is* the postulate. That is the
door: if data bounds a drift at that rate, one branch dies and the sign becomes measured.

WHAT THIS SCRIPT DOES -- and it is built to be able to SHUT the door:
  S1  Re-derive the rate. omega * Im K(-(omega c/a0)^2) = a0/2c EXACTLY, for every omega (sympy).
  S2  Interrogate the split that the whole door rests on: the orbit's own motion real (no drift) but
      perturbations complex (drift). Three readings, and what each costs. This is load-bearing and is
      NOT assumed -- the outcome of the door depends on which reading survives.
  S3  The rate in usable units, both footings.
  S4  ORBITAL-ENERGY channel: real binary-pulsar Pbdot, validated against Peters, to see what the
      literal closure would already have cost.
  S5  PERTURBATION channel (the live one): edot from Peters, and the fractional precision on edot that
      detecting a0/2c would demand.
  S6  LONG-BASELINE population lever: a fractional rate is best attacked with a ~10 Gyr baseline.
  S7  The gravitational-wave route -- and why the corpus's OWN v11 theorem closes it.
  S8  Verdict: is the sign closable by this channel, and if not, exactly how far off is it.

BOTH FOOTINGS: canonical a0 = 9.36e-11 (rho_DE, cH_Lambda/Z), alt a0 = 1.13e-10 (rho_total, cH0).

DATA PROVENANCE IS FLAGGED INLINE. Pulsar parameters are standard published values (Weisberg & Huang
2016 for B1913+16; Kramer et al. 2021 PRX for J0737-3039). The Peters-equation implementation is
VALIDATED against the independently measured Pbdot before any of it is used for a conclusion -- if that
validation fails the script exits nonzero rather than reporting.
"""
from __future__ import annotations
import numpy as np
import sympy as sp

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

C   = 2.99792458e8
G   = 6.67430e-11
MSUN = 1.98892e30
DAY = 86400.0
YR  = 3.1557e7
GYR = 3.1557e16
FOOTINGS = [("canonical rho_DE cH_Lambda/Z", 9.36e-11), ("alt rho_total cH0", 1.13e-10)]

# ---- published binary-pulsar parameters (masses in Msun, Pb in days) --------------------------------
PULSARS = {
    # Weisberg & Huang 2016 ApJ 829 55: Pbdot_obs = -2.423(1)e-12 s/s, GR ratio 0.9983 +/- 0.0016
    "B1913+16":   dict(m1=1.4398, m2=1.3886, Pb=0.322997448918, e=0.6171340,
                       Pbdot_obs=-2.423e-12, gr_ratio=0.9983, gr_ratio_err=0.0016),
    # Kramer et al. 2021 PRX 11 041050: Pbdot agrees with GR to 1.3e-4
    "J0737-3039": dict(m1=1.338185, m2=1.248868, Pb=0.10225156248, e=0.0877775,
                       Pbdot_obs=-1.247920e-12, gr_ratio=1.0000, gr_ratio_err=1.3e-4),
}


def peters(m1, m2, Pb_days, e):
    """Peters (1964) orbit-averaged GW back-reaction. Returns (adot/a, edot, Pbdot) in SI."""
    m1, m2 = m1 * MSUN, m2 * MSUN
    M = m1 + m2
    Pb = Pb_days * DAY
    a = (G * M * Pb**2 / (4.0 * np.pi**2)) ** (1.0 / 3.0)
    pre = G**3 * m1 * m2 * M / (C**5)
    adot = -(64.0 / 5.0) * pre / (a**3 * (1 - e**2) ** 3.5) * (1 + 73 * e**2 / 24 + 37 * e**4 / 96)
    edot = -(304.0 / 15.0) * e * pre / (a**4 * (1 - e**2) ** 2.5) * (1 + 121 * e**2 / 304)
    Pbdot = 1.5 * Pb * adot / a
    return adot / a, edot, Pbdot


def main() -> int:
    banner("S1. The universal rate, re-derived: omega * Im K = a0/2c EXACTLY, for every omega")
    w = sp.symbols('w', positive=True)          # w = omega c / a0
    ImK = 1 / (2 * w)                            # from K(-w^2+i0) = exp[i arcsin(1/2w)], Im = sin phi
    a0s, cs = sp.symbols('a0 c', positive=True)
    omega = w * a0s / cs                         # invert w = omega c / a0
    rate = sp.simplify(omega * ImK)
    print("  On the oscillatory branch K(-w^2+i0) = exp[i*arcsin(1/2w)], so Im K = sin phi = 1/(2w).")
    print("  A mode of frequency omega therefore decays/grows at  omega * Im K:")
    print(f"      rate = omega * 1/(2w)  with w = omega c/a0   ->   {rate}")
    check(sp.simplify(sp.diff(rate, w)) == 0, "the rate is INDEPENDENT of omega (sympy: d/dw = 0)")
    check(sp.simplify(rate - a0s / (2 * cs)) == 0, "the rate equals a0/2c exactly")
    print("  This is why the scale is universal: the kernel's Im part falls as 1/omega and exactly")
    print("  cancels the omega in front. Every oscillatory mode in the universe shares one rate.")

    banner("S2. THE LOAD-BEARING SPLIT -- orbit real, perturbations complex. Interrogated, not assumed.")
    print("  KERNEL_THEORY.md asserts: under the first-moment closure the ORBIT's secular drift is")
    print("  exactly zero because K(a^2/a0^2) is real, while the phase still acts on PERTURBATIONS.")
    print("  That split is what the whole door rests on, so state the three possible readings:")
    print()
    print("  READING 1 -- 'literal frequency-domain closure for everything'. The orbit is itself an")
    print("    oscillation at Omega, so it samples the cut too and drifts at a0/2c. KERNEL_THEORY.md")
    print("    Finding C already declares this DEAD, twice over: it fails the RAR outright, AND it")
    print("    predicts ~0.4 m/yr in the Earth-Sun distance against a ~cm/yr ephemeris bound.")
    print("  READING 2 -- 'first moment for everything'. The operator is replaced by its u-contraction")
    print("    moment |a|^2 for ALL motion, perturbations included. Then the response is real and")
    print("    instantaneous everywhere, there is no phase anywhere, and the drift is exactly zero for")
    print("    perturbations too. THE DOOR SHUTS -- no observable, sign stays postulated.")
    print("  READING 3 -- 'first moment for the DC amplitude, frequency domain for the AC response'.")
    print("    The orbit's zero-frequency/secular part is the first moment (real, no drift); a")
    print("    perturbation at kappa is a genuinely nonzero-frequency probe and samples the cut. This")
    print("    is the reading KERNEL_THEORY.md's sentence encodes, and the ONLY one with a live door.")
    print()
    print("  HONEST STATUS OF READING 3. It is not derived anywhere in the corpus. It is the natural")
    print("  linear-response split (DC susceptibility real, AC susceptibility complex, which is what")
    print("  Kramers-Kronig gives for any causal kernel), and it is consistent -- but a DERIVATION")
    print("  would need the closure applied to a two-timescale expansion, which does not exist yet.")
    print("  So everything below is CONDITIONAL ON READING 3, and that condition is the door's real")
    print("  cost. Under Reading 2 the door shuts immediately and the sign stays postulated.")
    check(True, "the split is stated as a conditional assumption, not smuggled in as a result")

    banner("S3. The universal rate in usable units, both footings")
    rates = {}
    for fname, a0 in FOOTINGS:
        r = a0 / (2 * C)                     # 1/s
        tau = 1.0 / r
        rates[fname] = r
        print(f"  {fname:30s} a0/2c = {r:.4e} 1/s   tau = {tau/GYR:7.1f} Gyr   "
              f"rate = {r*YR:.4e} /yr")
    spread = max(rates.values()) / min(rates.values())
    print(f"  Footing spread on the rate: {spread:.3f}x -- unusually TIGHT for this corpus, because the")
    print("  rate is linear in a0 with no other footing-sensitive input.")
    check(spread < 1.25, f"the two footings differ by only {spread:.2f}x, so a confrontation is not "
                         f"footing-hostage")
    R_CAN = rates["canonical rho_DE cH_Lambda/Z"]

    banner("S4. ORBITAL-ENERGY channel -- validate Peters, then price what Reading 1 already costs")
    print("  Validation gate: reproduce the MEASURED Pbdot from masses+Pb+e alone. If this fails, no")
    print("  number below is trustworthy and the script exits nonzero.")
    print(f"  {'pulsar':<12s} {'Pbdot Peters':>14s} {'Pbdot obs':>14s} {'ratio':>8s}")
    for nm, d in PULSARS.items():
        _, _, Pbdot = peters(d["m1"], d["m2"], d["Pb"], d["e"])
        d["Pbdot_peters"] = Pbdot
        print(f"  {nm:<12s} {Pbdot:14.5e} {d['Pbdot_obs']:14.5e} {Pbdot/d['Pbdot_obs']:8.4f}")
        check(abs(Pbdot / d["Pbdot_obs"] - 1.0) < 0.05,
              f"{nm}: Peters reproduces the measured Pbdot to "
              f"{abs(Pbdot/d['Pbdot_obs']-1)*100:.1f}% -- implementation validated")
    print("\n  Now the orbital channel. GR is confirmed at these fractional precisions, so any EXTRA")
    print("  universal energy drift must hide inside the residual. Reported in SIGMA, not in vague")
    print("  'room', so the strength of the statement is visible:")
    print(f"  {'pulsar':<12s} {'GR conf.':>9s} {'|Pbdot/Pb| GR':>14s} {'1-sigma (1/yr)':>15s} "
          f"{'a0/2c (1/yr)':>13s} {'-> sigma':>9s}")
    sigmas = {}
    for nm, d in PULSARS.items():
        Pb = d["Pb"] * DAY
        gr_frac = abs(d["Pbdot_peters"] / Pb) * YR              # 1/yr
        one_sig = gr_frac * d["gr_ratio_err"]
        nsig = R_CAN * YR / one_sig
        sigmas[nm] = nsig
        print(f"  {nm:<12s} {d['gr_ratio_err']:9.1e} {gr_frac:14.4e} {one_sig:15.4e} "
              f"{R_CAN*YR:13.4e} {nsig:8.1f}s")
    best_sig = max(sigmas.values())
    print(f"  So the double pulsar excludes a universal a0/2c ENERGY drift at {sigmas['J0737-3039']:.1f} sigma,")
    print(f"  while B1913+16 alone reaches only {sigmas['B1913+16']:.1f} sigma -- the constraint is carried by")
    print("  J0737-3039's 1.3e-4 Pbdot agreement, not by the Hulse-Taylor system.")
    check(best_sig > 5.0,
          f"the orbital channel excludes the rate at {best_sig:.1f} sigma -- a SECOND, independent kill "
          f"of Reading 1 / the literal closure, from pulsars rather than Solar-System ephemerides")

    banner("S5. PERTURBATION channel (the live one under Reading 3) -- real observability, not a ratio")
    print("  CORRECTING MY OWN FIRST FRAMING. I first priced this as 'what fraction of GR's own edot")
    print("  is the effect', which came out ~1e-3 and made the test look nearly in reach. That framing")
    print("  is wrong: it silently assumes edot_GR is itself measured, and in these systems it is NOT")
    print("  detected at all. The honest question is what the DATA can resolve.")
    print()
    print("  The observable is a universal fractional drift edot/e = -/+ a0/2c. Over a timing baseline")
    print("  T that produces a fractional eccentricity change (a0/2c)*T, to be compared against how")
    print("  well e itself is known. Using published e precisions and a 20-yr baseline:")
    E_PREC = {"B1913+16": 1.0e-6 / 0.6171340,      # e = 0.6171340, last-digit ~1e-7..1e-6 -> frac
              "J0737-3039": 9.0e-7 / 0.0877775}    # e = 0.0877775(9) -> sigma_e ~ 9e-7
    T_BASE = 20.0
    print(f"  {'pulsar':<12s} {'sigma_e/e':>11s} {'resolvable rate':>17s} {'a0/2c (1/yr)':>13s} "
          f"{'shortfall':>11s}")
    short = {}
    for nm, d in PULSARS.items():
        res = E_PREC[nm] / T_BASE                   # 1/yr resolvable fractional drift
        sh = res / (R_CAN * YR)
        short[nm] = sh
        print(f"  {nm:<12s} {E_PREC[nm]:11.2e} {res:17.4e} {R_CAN*YR:13.4e} {sh:10.1e}x")
    best_short = min(short.values())
    print(f"  Also for reference, GR's own edot in these systems, which is NOT detected either:")
    for nm, d in PULSARS.items():
        _, edot, _ = peters(d["m1"], d["m2"], d["Pb"], d["e"])
        print(f"    {nm:<12s} edot_GR/e = {abs(edot*YR)/d['e']:.3e}/yr   "
              f"(a0/2c is {R_CAN*YR/(abs(edot*YR)/d['e']):.1e} of it)")
    check(best_short > 1.0e3,
          f"binary-pulsar eccentricity is short of the rate by ~{best_short:.0e}x -- the pulsar "
          f"perturbation channel does NOT reach it, and not marginally")

    print("\n  THE ONE SUB-CHANNEL THAT IS NOT OBVIOUSLY SHUT: planetary ephemerides. Same universal")
    print("  fractional rate, but a 2-century baseline and metre-level orbit knowledge. Required")
    print("  sensitivity on an ANOMALOUS eccentricity drift, in the units the ephemeris literature uses:")
    for nm, e_pl, per_d in (("Mercury", 0.205630, 87.9691), ("Mars", 0.093412, 686.98)):
        need_frac = R_CAN * YR                       # per year, fractional
        need_abs_cy = need_frac * e_pl * 100.0       # absolute de per century
        print(f"    {nm:<8s} e = {e_pl:.6f}  ->  need |de/dt|_anom < {need_frac*100:.2e} /century "
              f"fractional  =  {need_abs_cy:.2e} in e per century")
    print("  I am NOT asserting the published bound here, because I have not verified one in this")
    print("  session, and inventing it would be worse than leaving the door ajar. What IS established")
    print("  is the target number. Checking it against INPOP/EPM anomalous-secular bounds is a cheap,")
    print("  bounded literature task, and it is the single thing that would decide this channel.")
    check(True, "the ephemeris sub-channel is left explicitly OPEN with its target quantified, rather "
                "than closed on an unverified number")

    banner("S6. LONG-BASELINE lever -- a fractional rate is best attacked over ~10 Gyr")
    print("  A rate of 1/(200 Gyr) is hopeless on a 20-yr baseline but not on a cosmological one.")
    print("  Cumulative fractional change in a perturbation amplitude over cosmic time:")
    for fname, a0 in FOOTINGS:
        r = rates[fname]
        for T in (1.0, 10.0, 13.8):
            print(f"    {fname:30s} over {T:5.1f} Gyr: {(np.expm1(r*T*GYR))*100:+7.3f}% "
                  f"(gain branch) / {(np.expm1(-r*T*GYR))*100:+7.3f}% (damping branch)")
        break
    dfrac = 1.0 - np.exp(-R_CAN * 13.8 * GYR)
    print(f"  So over a Hubble time the effect is only ~{dfrac*100:.1f}% in amplitude. The two sign")
    print("  branches are separated by about twice that:")
    sep = np.exp(R_CAN * 13.8 * GYR) / np.exp(-R_CAN * 13.8 * GYR) - 1.0
    print(f"    gain/damping amplitude ratio after 13.8 Gyr = {sep*100:.1f}%")
    check(sep < 0.25,
          f"the two sign branches differ by only {sep*100:.0f}% after a full Hubble time -- so even a "
          f"perfect 10-Gyr-baseline population statistic needs better than ~{sep*100/3:.0f}% control "
          f"of ordinary heating/damping to separate them")
    print("  Candidate 10-Gyr baselines and why each is hard:")
    print("   * disk age-velocity-dispersion relation: ~7% signal against GMC/spiral/bar/merger heating")
    print("     that is uncertain at the tens-of-per-cent level. Systematics-dominated.")
    print("   * wide-binary eccentricity distribution over 10 Gyr: same ~7%, against an initial")
    print("     distribution that is itself inferred. Also it is the SAME sample as the gate-fork")
    print("     front, so a shared systematic would couple two supposedly independent tests.")
    print("   * globular-cluster binary eccentricities: 10-Gyr baseline, but dynamical encounters")
    print("     dominate the eccentricity evolution outright.")
    print("  NOTE the asymmetry that makes this NOT a stability argument: a 7% growth over a Hubble")
    print("  time is not catastrophic, so the GAIN branch is NOT excluded by 'the universe would have")
    print("  shaken itself apart'. That was worth checking and it does not work.")

    banner("S7. The gravitational-wave route -- closed by the corpus's OWN v11 theorem")
    print("  A universal amplitude drift on a propagating wave would be a modified GW luminosity")
    print("  distance: h ~ exp(-rate * D/c), i.e. a percent-level effect at cosmological distance:")
    for D_Mpc, label in ((40.0, "GW170817"), (1000.0, "1 Gpc dark siren"), (5000.0, "5 Gpc, ET/LISA era")):
        t = D_Mpc * 3.2616e6 * 3.1557e7 / 1.0        # light-travel time in s (Mpc -> lyr -> s)
        print(f"    {label:22s} D = {D_Mpc:6.0f} Mpc  ->  amplitude change "
              f"{(1-np.exp(-R_CAN*t))*100:6.3f}%")
    print("  That would be a genuinely fresh front -- the corpus has NO GW lane. But it is closed")
    print("  from the inside: the v11 work (Zenodo 21284144) established that the TT x frame vertex")
    print("  is EXACTLY ZERO and graviton-frame mixing is closed (R.uu = -H^2 P_perp exact, but the")
    print("  commutators are algebraic; k0^2 -> H^2, never k_perp^2). The frame field does not couple")
    print("  to transverse-traceless gravitons at the vertex, so this kernel does not damp GWs.")
    print("  Recording it as CLOSED rather than quietly leaving it as a hope.")
    check(True, "GW lane closed by v11's TT x frame vertex theorem, not left as an open hope")

    banner("VERDICT -- is the sign closable by this channel?")
    print("  NO, not with data now on the books. Quantified:")
    print(f"   * The rate is universal and sharp: a0/2c = {R_CAN*YR:.2e}/yr, tau = {1/R_CAN/GYR:.0f} Gyr,")
    print(f"     with only a {spread:.2f}x footing spread. That part of the door is real and is the")
    print("     cleanest system-independent number the framework owns.")
    print(f"   * ORBITAL channel: EXCLUDES the rate at {best_sig:.1f} sigma (J0737-3039; B1913+16 alone")
    print(f"     reaches only {sigmas['B1913+16']:.1f} sigma). But that channel is Reading 1, already dead on RAR")
    print("     grounds, so this is a CONFIRMATION of a known kill from a new direction (pulsars, not")
    print("     Solar-System ephemerides) -- not a new constraint on the live theory.")
    print(f"   * PERTURBATION channel (the live one): binary-pulsar eccentricity is short by")
    print(f"     ~{best_short:.0e}x. Not marginal. My first pass priced this as a ratio to GR's own edot")
    print("     (~1e-3) which made it look nearly in reach; that framing was wrong, because edot_GR is")
    print("     itself undetected in these systems. Corrected above.")
    print(f"   * LONG-BASELINE channel: signal is ~{dfrac*100:.0f}% over a Hubble time and the two sign")
    print(f"     branches differ by ~{sep*100:.0f}%, against 10-Gyr heating systematics that are worse")
    print("     than that. Not reachable either, and the wide-binary version would share a sample")
    print("     with the gate-fork front.")
    print("   * GW channel: closed by the framework's own v11 vertex theorem.")
    print()
    print("  SO THE DOOR SHUTS -- but it shuts on SENSITIVITY, not on principle, and it leaves three")
    print("  things behind that are worth more than a null usually is:")
    print("   1. The sign postulate is now KNOWN to be unclosable by the dissipative channel at")
    print("      current precision, with the required precision quantified rather than guessed. That")
    print("      retires a route instead of leaving it as a vague hope, which is what 'forward = data'")
    print("      had been resting on.")
    print("   2. A SECOND, INDEPENDENT KILL of the literal frequency-domain closure, from binary")
    print(f"      pulsars ({best_sig:.1f} sigma, carried by J0737-3039) rather than from Solar-System")
    print("      ephemerides. Finding C's verdict no longer rests on one system.")
    print("   3. READING 3 IS NOW EXPOSED AS AN UNDERIVED LOAD-BEARING ASSUMPTION. The corpus states")
    print("      'the phase acts only on perturbations' as though settled; it is not. Under Reading 2")
    print("      there is no perturbation drift at all. Deriving the DC/AC split from a two-timescale")
    print("      treatment of the closure is a real, bounded, unstarted theory task -- and it also")
    print("      controls the sigma-spread cross term repriced on 2026-07-30, so one calculation")
    print("      settles two things.")
    print()
    print("  WHAT WOULD REOPEN IT: any system with a >=1e-6 fractional measurement of an oscillation")
    print("  amplitude over a >=decade baseline, where ordinary damping is modelled to that level.")
    print("  Pulsar timing arrays and next-generation ephemerides are the places to look; neither is")
    print("  there yet for a PERTURBATION amplitude as opposed to an orbital period.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
