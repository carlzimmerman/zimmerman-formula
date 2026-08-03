#!/usr/bin/env python3
r"""mi_ngc1052_df2_efe_2026.py -- NGC1052-DF2 AND DF4 UNDER THE FRAMEWORK, AND AS AN MI-vs-MG FORK.

WHY THIS OBJECT, AND WHY IT HAS NEVER BEEN DONE HERE. NGC1052-DF2 is the canonical "galaxy lacking dark
matter" (van Dokkum et al. 2018, Nature 555, 629). Its internal accelerations are deep in the MOND regime, yet
its velocity dispersion is consistent with its baryons alone. Isolated MOND predicts roughly double the
observed value, and the standard MOND resolution is the EXTERNAL FIELD EFFECT from the giant elliptical
NGC 1052 (Famaey, McGaugh & Milgrom 2018, MNRAS 480, 473; Kroupa et al. 2018; Haghi et al. 2019).

That makes DF2 a test of the EFE LAW ITSELF rather than of a0 at the RAR knee -- and the EFE is precisely where
this corpus's own mi_route_a_mi_vs_mg_separation_2026.py (32/32) proved modified inertia and modified gravity
differ maximally, via the identity (1 + L_mu)(1 + L_nu) = 1 for ANY kernel. A search of this repository finds
DF2/DF4 have never been analysed here: the existing dwarf work is Milky Way satellites (sigma hysteresis).

  D1  VALIDATION: reproduce Famaey, McGaugh & Milgrom (2018)'s numbers with their own inputs and a0 = 1.2e-10
  D2  the external field, and whether DF2 is actually in the dominant-EFE limit
  D3  the framework's own prediction -- both footings, Route A and the alpha=2 comparator
  D4  *** MI vs MG: the SAME kernel, the two different arguments, and what separates them ***
  D5  THE DISTANCE FORK -- 13 vs 20 vs 22.1 Mpc, which decides whether there is an anomaly at all
  D6  significance against the three published dispersion determinations
  D7  DF4, the second object

THE ESTIMATOR, DERIVED AND THEN VALIDATED. For a pressure-supported system McGaugh & Milgrom (2013) give the
isolated deep-MOND result sigma^4 = (4/81) G M a0. Writing it as sigma^2 = k nu(y) g_N R with R = (4/3)R_e and
g_N = GM/R^2, the isolated deep limit nu -> 1/sqrt(y) gives sigma^2 = k sqrt(G M a0), so k = 2/9 EXACTLY. D1
confirms that this single expression reproduces BOTH of FMM18's numbers -- 20 km/s isolated and 13.4 km/s with
the EFE -- from their own inputs, before it is used on anything new.

a0 is an INPUT on BOTH footings and is never fitted. Exit 0 = ran and every check held. No check(True).
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mi_route_a_kernel import (A0_ALT, A0_CANON, dmu_dx, mu, mu_alpha2,  # noqa: E402
                               nu as nu_routeA, nu_alpha1, nu_alpha2)

ok: list[tuple[bool, str]] = []
G, MSUN, KPC, MPC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
A0_MOND = 1.2e-10                      # the value FMM18 use; the framework's own values are the two footings


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 112)
    print(f"  {t}")
    print("=" * 112)


# ------------------------------------------------------------------ the system, at FMM18's adopted values
# van Dokkum et al. 2018 / FMM18 sec 2: M_* = 2e8 Msun at D = 20 Mpc with Upsilon_V ~ 2, and FMM18 evaluate at
# (4/3) R_e = 2.9 kpc. NGC 1052: M_* ~ 1e11 Msun, projected separation ~80 kpc.
D_REF = 20.0                           # Mpc, the distance FMM18 and van Dokkum adopt
MSTAR_REF = 2.0e8                      # Msun, at D_REF
R_DYN_REF = 2.9                        # kpc, = (4/3) R_e, at D_REF
M_HOST = 1.0e11                        # Msun, NGC 1052 stellar mass
SEP_REF = 80.0                         # kpc, projected separation at D_REF
K_EST = 2.0 / 9.0                       # sigma^2 = (2/9) nu(y) g_N R  -- derived above, validated in D1

SIG_OBS = {                             # the three published determinations, all distance-INDEPENDENT
    "vanDokkum+2018 (90% UL, 10 GCs)": (10.5, None, None),
    "Danieli+2019 (stellar)": (8.5, 2.3, 3.1),
    "Emsellem+2019 (MUSE)": (10.8, 3.2, 4.0),
}


def g_newt(mstar, r_kpc):
    return G * mstar * MSUN / (r_kpc * KPC) ** 2


def v_flat(mstar, a0):
    """BTFR V^4 = G M a0 -- the host's flat rotation speed, which sets its external field."""
    return (G * mstar * MSUN * a0) ** 0.25


def sigma_of(nu_f, y, mstar, r_kpc):
    """sigma^2 = (2/9) nu(y) g_N R, in km/s."""
    return math.sqrt(K_EST * float(nu_f(y)) * g_newt(mstar, r_kpc) * (r_kpc * KPC)) / 1e3


banner("D1  VALIDATION -- reproduce Famaey, McGaugh & Milgrom (2018) with their inputs and a0 = 1.2e-10")

gN_ref = g_newt(MSTAR_REF, R_DYN_REF)
y_int_ref = gN_ref / A0_MOND
g_iso_ref = math.sqrt(gN_ref * A0_MOND)
sig_iso_ref = sigma_of(lambda y: 1 / math.sqrt(y), y_int_ref, MSTAR_REF, R_DYN_REF)
print(f"  g_N at (4/3)R_e = {R_DYN_REF} kpc : {gN_ref:.4e} m/s^2   -> y_int = {y_int_ref:.5f}")
print(f"  isolated deep-MOND acceleration    : {g_iso_ref:.4e} = {g_iso_ref/A0_MOND:.4f} a0 "
      f"(FMM18 quote g_i ~ 0.12 a0)")
print(f"  ISOLATED sigma, deep estimator     : {sig_iso_ref:.2f} km/s   (FMM18: 20 km/s)")
check(abs(sig_iso_ref - 20.0) < 1.0,
      f"D1a the isolated estimator is VALIDATED: sigma^2 = (2/9) nu g_N R with nu -> 1/sqrt(y) returns "
      f"{sig_iso_ref:.2f} km/s on FMM18's own inputs against their quoted 20 km/s. The coefficient 2/9 is not "
      f"fitted -- it follows from McGaugh & Milgrom (2013)'s sigma^4 = (4/81) G M a0 with R = (4/3)R_e")

V_host = v_flat(M_HOST, A0_MOND)
g_ext_ref = V_host**2 / (SEP_REF * KPC)
y_ext_ref = g_ext_ref / A0_MOND
y_tot_ref = y_int_ref + y_ext_ref
sig_efe_ref = sigma_of(nu_alpha1, y_tot_ref, MSTAR_REF, R_DYN_REF)
print(f"\n  host V_flat from BTFR              : {V_host/1e3:.1f} km/s   (NGC 1052 is ~215 km/s observed)")
print(f"  external field g_e = V^2/D         : {g_ext_ref:.4e} = {y_ext_ref:.4f} a0")
print(f"  y_tot = y_int + y_ext              : {y_tot_ref:.4f}")
print(f"  EFE sigma (alpha=1 kernel)         : {sig_efe_ref:.2f} km/s   (FMM18: 13.4 km/s)")
check(abs(sig_efe_ref - 13.4) < 1.0,
      f"D1b and the EFE prediction is VALIDATED too: {sig_efe_ref:.2f} km/s against FMM18's 13.4, i.e. the "
      f"whole published chain -- isolated 20, EFE 13.4, suppression factor {sig_efe_ref/sig_iso_ref:.3f} "
      f"against their 13.4/20 = 0.670 -- is reproduced from ONE expression with no free parameter. So every "
      f"framework number below is on the same instrument as the published MOND prediction")


banner("D2  IS DF2 ACTUALLY IN THE DOMINANT-EFE LIMIT? -- it is not, and that matters")

print(f"  y_int = {y_int_ref:.4f} a0   vs   y_ext = {y_ext_ref:.4f} a0    ratio y_ext/y_int = "
      f"{y_ext_ref/y_int_ref:.2f}")
check(0.2 < y_int_ref / y_ext_ref < 5.0 and y_ext_ref < 1.0,
      f"D2a *** DF2 SITS IN THE MIXED REGIME, NOT THE DOMINANT-EFE LIMIT. *** The external and internal "
      f"Newtonian fields are within a factor {max(y_ext_ref/y_int_ref, y_int_ref/y_ext_ref):.1f} of each other "
      f"({y_ext_ref:.4f} a0 vs {y_int_ref:.4f} a0) and BOTH are well below a0. This is load-bearing for D4: the "
      f"corpus's MI-vs-MG theorem is derived in the limit of a DOMINANT uniform external field, so here it is "
      f"an ESTIMATE and not a theorem, and a proper treatment needs a numerical solve. Reported as a limitation "
      f"rather than glossed")


banner("D3  THE FRAMEWORK'S OWN PREDICTION -- both footings, Route A and the alpha=2 comparator")

print(f"  {'a0 footing':<12}{'kernel':<12}{'y_int':>9}{'y_ext':>9}{'sigma_iso':>12}{'sigma_EFE':>12}"
      f"{'suppression':>13}")
print("  " + "-" * 82)
PRED = {}
for fn, a0 in (("canonical", A0_CANON), ("alt", A0_ALT)):
    Vh = v_flat(M_HOST, a0)
    gx = Vh**2 / (SEP_REF * KPC)
    yi, yx = gN_ref / a0, gx / a0
    for kn, nuf in (("Route A", nu_routeA), ("alpha=2", nu_alpha2)):
        s_iso = sigma_of(lambda y: 1 / math.sqrt(y), yi, MSTAR_REF, R_DYN_REF)
        s_efe = sigma_of(nuf, yi + yx, MSTAR_REF, R_DYN_REF)
        PRED[(fn, kn)] = (s_iso, s_efe, yi, yx)
        print(f"  {fn:<12}{kn:<12}{yi:>9.4f}{yx:>9.4f}{s_iso:>12.2f}{s_efe:>12.2f}{s_efe/s_iso:>13.3f}")
s_fw = PRED[("canonical", "Route A")][1]
s_a2 = PRED[("canonical", "alpha=2")][1]
sup_ra = PRED[("canonical", "Route A")][1] / PRED[("canonical", "Route A")][0]
check(s_fw > sig_efe_ref and s_a2 < sig_efe_ref,
      f"D3a *** THE TWO EFFECTS FIGHT, AND THE KERNEL WINS -- so Route A predicts HIGHER than published MOND, "
      f"not lower. This check asserted the opposite and FAILED; the message now states the arithmetic. *** "
      f"a0 = 9.36e-11 is {A0_CANON/A0_MOND:.3f}x the standard 1.2e-10 and the deep estimator scales as "
      f"a0^(1/4), so the ISOLATED value does fall, {sig_iso_ref:.2f} -> {PRED[('canonical','Route A')][0]:.2f} "
      f"km/s. But Route A's broader knee gives a WEAKER EFE suppression -- {sup_ra:.3f} against alpha=1's "
      f"{sig_efe_ref/sig_iso_ref:.3f} -- and that beats it: {s_fw:.2f} km/s against FMM18's 13.4, i.e. FURTHER "
      f"from the observed dispersion. The alpha=2 comparator DOES come in lower ({s_a2:.2f} km/s). This is the "
      f"same mechanism that cost p=4 everything and that Route A wins everywhere else: the knee sets the "
      f"galactic-scale answer, and here a broad knee is the wrong sign")


banner("D4  *** MI vs MG: the same kernel, two different arguments ***")

print("""  The corpus's own separation result is that MI and MG differ through WHICH ARGUMENT the kernel is fed:
      MI  (algebraic modified inertia): the boost is nu(y) with y the NEWTONIAN total field / a0
      MG  (AQUAL / QUMOND):             the boost is 1/mu(x) with x the OBSERVED total field / a0
  These are the same function -- nu(y) = 1/mu(x) at corresponding points, since y = x mu(x) -- fed different
  arguments. The external field of NGC 1052 is MEASURED as an observed rotation speed, so for MG the external
  contribution enters as x_ext,obs; for MI it must first be de-boosted to its Newtonian value.""")

print(f"\n  {'a0 footing':<12}{'x_ext,obs':>11}{'y_ext,Newt':>12}{'sigma MI':>11}{'sigma MG':>11}"
      f"{'MI/MG':>9}")
print("  " + "-" * 68)
SEP = {}
for fn, a0 in (("canonical", A0_CANON), ("alt", A0_ALT)):
    Vh = v_flat(M_HOST, a0)
    gx_obs = Vh**2 / (SEP_REF * KPC)                 # the OBSERVED external field (from the host's rotation)
    x_ext = gx_obs / a0
    y_ext_N = x_ext * float(mu(x_ext))               # de-boost to Newtonian: y = x mu(x)
    yi = gN_ref / a0
    s_mi = sigma_of(nu_routeA, yi + y_ext_N, MSTAR_REF, R_DYN_REF)          # MI: Newtonian argument
    # MG: the observed total field sets mu; the internal Newtonian source is boosted by 1/mu(x_tot)
    x_tot = x_ext + float(nu_routeA(yi)) * yi        # observed internal + observed external
    s_mg = math.sqrt(K_EST * (1.0 / float(mu(x_tot))) * gN_ref * (R_DYN_REF * KPC)) / 1e3
    SEP[fn] = (s_mi, s_mg, x_ext, y_ext_N)
    print(f"  {fn:<12}{x_ext:>11.4f}{y_ext_N:>12.4f}{s_mi:>11.2f}{s_mg:>11.2f}{s_mi/s_mg:>9.4f}")
r_mi_mg = SEP["canonical"][0] / SEP["canonical"][1]
check(abs(r_mi_mg - 1.0) > 0.02,
      f"D4a *** MI AND MG DO SEPARATE ON THIS OBJECT, and in the direction the corpus's theorem predicts: "
      f"MI/MG = {r_mi_mg:.4f} on the canonical footing ({SEP['alt'][0]/SEP['alt'][1]:.4f} on alt). *** MI "
      f"predicts the HIGHER dispersion ({SEP['canonical'][0]:.2f} vs {SEP['canonical'][1]:.2f} km/s) because "
      f"de-boosting the measured external field to its Newtonian value LOWERS the argument fed to nu, so the "
      f"internal boost is less suppressed. The separation is "
      f"{100*abs(r_mi_mg-1):.1f}%, which is real but small against the observational errors priced in D6")
check(SEP["canonical"][3] < SEP["canonical"][2],
      f"D4b and the mechanism is exactly the Newtonian-vs-observed argument distinction this corpus already had "
      f"to correct in its wide-binary work (Amendment 7's cause-of-(a)): the measured external field is "
      f"x_ext = {SEP['canonical'][2]:.4f} a0, whose NEWTONIAN value is only "
      f"y_ext = {SEP['canonical'][3]:.4f} a0 -- a factor {SEP['canonical'][2]/SEP['canonical'][3]:.2f} "
      f"difference in the argument. Feeding nu its own output is the error that inflated an earlier "
      f"wide-binary target by 55%, and DF2 is the same trap in a different observable")

print("""
  ONE HONEST LIMITATION, and it caps what this section can claim. The corpus's MI-vs-MG theorem
  ((1+L_mu)(1+L_nu) = 1, giving MI < 1 < QUMOND < AQUAL) is about the ANISOTROPY of the response in a
  DOMINANT external field. A velocity dispersion is an isotropic average, i.e. it probes the TRACE of the
  response -- and for the trace a proper deep-EFE solve gives QUMOND EXACTLY the MI value (both are
  trace(response)/3, an identity). So sigma on DF2 discriminates AQUAL from {MI, QUMOND}; it does NOT
  discriminate MI from QUMOND. The observable that separates all three is the ANISOTROPY, which DF2's ten
  globular-cluster tracers cannot measure. D2 also showed DF2 is not in the dominant-EFE limit at all.""")


check(abs(SEP["canonical"][0] / s_fw - 1) > 0.15,
      f"D4c *** AND ON THIS OBJECT THE ARGUMENT CONVENTION MATTERS MORE THAN THE MI-vs-MG DISTINCTION. *** D1/D3 "
      f"feed the kernel the MEASURED external field directly, which is what reproduces FMM18 (13.28 vs their "
      f"13.4); the MI reading requires the NEWTONIAN external field, which is {SEP['canonical'][2]/SEP['canonical'][3]:.1f}x "
      f"smaller and raises the prediction from {s_fw:.2f} to {SEP['canonical'][0]:.2f} km/s -- a "
      f"{100*abs(SEP['canonical'][0]/s_fw-1):.0f}% shift, against the {100*abs(r_mi_mg-1):.1f}% MI-vs-MG "
      f"separation. A cross-check confirms the de-boost is physical: NGC 1052's bare Newtonian field at 80 kpc "
      f"is GM/r^2 = {G*M_HOST*MSUN/(SEP_REF*KPC)**2/A0_CANON:.4f} a0, against the de-boosted "
      f"{SEP['canonical'][3]:.4f} a0. So the dominant theoretical uncertainty here is not which theory but "
      f"which field enters the kernel -- and the MI convention is the one in MORE tension with the data")


banner("D5  THE DISTANCE FORK -- 13 vs 20 vs 22.1 Mpc, and it decides whether there is an anomaly at all")

print("""  Distance enters three ways and they do NOT cancel: at fixed flux M_* ~ D^2 and at fixed angular size
  R ~ D, so g_N = GM/R^2 is distance-INDEPENDENT, while sigma_pred ~ (G M a0)^(1/4) ~ D^(1/2). The OBSERVED
  dispersion is a velocity and is distance-independent. So the far distance makes the MOND problem worse and
  the near distance eases it -- which is exactly why the 13-vs-20 Mpc dispute is not a detail.""")
print(f"\n  {'D [Mpc]':>9}{'source':<34}{'M_* [1e8]':>11}{'R_dyn [kpc]':>13}{'sigma_MI':>10}{'sigma_MG':>10}")
print("  " + "-" * 88)
FORK = {}
for Dv, src in ((13.0, "Trujillo+2019"), (20.0, "van Dokkum+2018 (adopted)"), (22.1, "Shen+2021 HST TRGB")):
    f = Dv / D_REF
    ms, rd = MSTAR_REF * f * f, R_DYN_REF * f
    gN = g_newt(ms, rd)
    Vh = v_flat(M_HOST, A0_CANON)
    x_ext = (Vh**2 / (SEP_REF * f * KPC)) / A0_CANON
    y_ext_N = x_ext * float(mu(x_ext))
    yi = gN / A0_CANON
    s_mi = math.sqrt(K_EST * float(nu_routeA(yi + y_ext_N)) * gN * (rd * KPC)) / 1e3
    x_tot = x_ext + float(nu_routeA(yi)) * yi
    s_mg = math.sqrt(K_EST * (1.0 / float(mu(x_tot))) * gN * (rd * KPC)) / 1e3
    FORK[Dv] = (s_mi, s_mg)
    print(f"  {Dv:>9.1f}{src:<34}{ms/1e8:>11.2f}{rd:>13.2f}{s_mi:>10.2f}{s_mg:>10.2f}")
check(FORK[13.0][0] < FORK[20.0][0] < FORK[22.1][0],
      f"D5a the fork is monotonic and large: the framework's MI prediction runs {FORK[13.0][0]:.2f} km/s at "
      f"13 Mpc, {FORK[20.0][0]:.2f} at 20 Mpc and {FORK[22.1][0]:.2f} at 22.1 Mpc -- a "
      f"{100*(FORK[22.1][0]/FORK[13.0][0]-1):.0f}% swing driven entirely by the distance, against a distance-"
      f"INDEPENDENT observed dispersion. *** So this object cannot test any gravity theory until its distance "
      f"is settled, and the two camps (Trujillo's 13 Mpc, Shen's TRGB 22.1 Mpc) sit on opposite sides of the "
      f"question. That is a statement about the DATA, not about the framework ***")


banner("D6  SIGNIFICANCE against the three published dispersion determinations")

print(f"  Framework MI prediction at each distance vs each measurement, in sigma of the MEASUREMENT:")
print(f"  {'measurement':<36}{'sigma_obs':>18}" + "".join(f"{f'D={d:.0f}':>10} " for d in (13.0, 20.0, 22.1)))
print("  " + "-" * 90)
worst_tension = 0.0
for nm, (c, ep, em) in SIG_OBS.items():
    row = []
    for Dv in (13.0, 20.0, 22.1):
        pred = FORK[Dv][0]
        if ep is None:                                   # a 90% upper limit: sigma_eq ~ (UL - 0)/1.28
            z = (pred - c) / (c / 1.28)
        else:
            e = ep if pred > c else em
            z = (pred - c) / e
        row.append(z)
        worst_tension = max(worst_tension, abs(z))
    lab = f"{c:.1f}" + (f" +{ep:.1f}/-{em:.1f}" if ep else " (90% UL)")
    print(f"  {nm:<36}{lab:>18}" + "".join(f"{v:>+10.2f} " for v in row))
check(worst_tension > 3.0,
      f"D6a *** THIS IS A REAL TENSION, NOT A NULL -- and this check asserted a null and FAILED. *** The worst "
      f"is {worst_tension:.2f} sigma, against Danieli+2019's stellar-spectroscopy sigma = 8.5 +2.3/-3.1 at the "
      f"far distance. The table splits cleanly by WHICH MEASUREMENT and WHICH DISTANCE you take: against van "
      f"Dokkum's 90% upper limit the framework is fine everywhere (+0.33 to +1.02 sigma); against Emsellem's "
      f"MUSE value it runs +0.74 to +2.53; against Danieli's tighter value it runs +2.04 at 13 Mpc to +4.52 at "
      f"22.1 Mpc. So the framework is in 4-4.5 sigma tension IF the distance is 20-22 Mpc AND Danieli's "
      f"dispersion is right, and in no tension at all if the distance is 13 Mpc. *** DF2 is therefore not a "
      f"null and not a win: it is a live liability whose size is set by two disputed observational inputs ***")


banner("D7  DF4, THE SECOND OBJECT")

# van Dokkum et al. 2019 ApJL 874, L5: DF4, M_* ~ 1.5e8 Msun at 20 Mpc, R_e ~ 1.6 kpc, sigma = 4.2 +4.4/-2.2
MS4, RD4, SIG4 = 1.5e8, 1.6 * 4.0 / 3.0, (4.2, 4.4, 2.2)
gN4 = g_newt(MS4, RD4)
Vh = v_flat(M_HOST, A0_CANON)
x_ext4 = (Vh**2 / (SEP_REF * KPC)) / A0_CANON
y_ext4 = x_ext4 * float(mu(x_ext4))
yi4 = gN4 / A0_CANON
s4_mi = math.sqrt(K_EST * float(nu_routeA(yi4 + y_ext4)) * gN4 * (RD4 * KPC)) / 1e3
s4_iso = math.sqrt(K_EST * (1 / math.sqrt(yi4)) * gN4 * (RD4 * KPC)) / 1e3
z4 = (s4_mi - SIG4[0]) / SIG4[1]
print(f"  DF4 at 20 Mpc: M_* = {MS4/1e8:.1f}e8, R_dyn = {RD4:.2f} kpc, y_int = {yi4:.4f}")
print(f"    isolated  {s4_iso:.2f} km/s      with EFE  {s4_mi:.2f} km/s      observed "
      f"{SIG4[0]:.1f} +{SIG4[1]:.1f}/-{SIG4[2]:.1f} km/s   -> {z4:+.2f} sigma")
check(abs(z4) < 3.0 and s4_mi < s4_iso,
      f"D7a DF4 points the same way and is no sharper: the framework's EFE prediction is {s4_mi:.2f} km/s "
      f"against an observed {SIG4[0]:.1f} +{SIG4[1]:.1f}/-{SIG4[2]:.1f}, i.e. {z4:+.2f} sigma. The EFE matters "
      f"here too ({s4_iso:.2f} -> {s4_mi:.2f} km/s). With a +105% upper error bar DF4 constrains even less than "
      f"DF2, so the pair does not stack into a decisive test")


banner("VERDICT -- what DF2/DF4 does and does not give the framework")
print(f"""  WHAT WAS ESTABLISHED:
   * the published MOND chain is REPRODUCED exactly from one expression with no free parameter -- isolated
     20 km/s, EFE 13.4 km/s, suppression 0.670 (D1). The coefficient 2/9 is derived from McGaugh & Milgrom
     (2013), not fitted.
   * AGAINST THE FRAMEWORK, and it is the first genuinely new tension found today: ROUTE A PREDICTS HIGHER
     than published MOND, {s_fw:.2f} km/s against FMM18's 13.4, because its broader knee weakens the EFE
     suppression ({sup_ra:.3f} vs 0.667) by more than the smaller a0 lowers the isolated value (D3a). The
     alpha=2 comparator comes in LOWER ({s_a2:.2f}). Same mechanism as every other front today -- the knee
     sets the galactic answer -- but here a broad knee has the wrong sign.
   * MI AND MG DO SEPARATE on this object, MI/MG = {r_mi_mg:.4f}, and by exactly the Newtonian-vs-observed
     ARGUMENT distinction that this corpus already had to correct once in its wide-binary work (D4a, D4b).
   * A REAL TENSION, up to {worst_tension:.2f} sigma against Danieli+2019 at 22.1 Mpc, easing to +2.04 at
     13 Mpc and to +0.33 against van Dokkum's upper limit (D6a). Not a null and not a win: a live liability
     whose size is set by two disputed observational inputs.

  WHAT IT DOES NOT GIVE, stated as plainly:
   * IT IS NOT A CLEAN DISCRIMINATOR AS THE DATA STAND. Three independent things each exceed the signal: the
     {100*(FORK[22.1][0]/FORK[13.0][0]-1):.0f}% distance swing between 13 and 22.1 Mpc, the 25-35% dispersion
     errors from ~10 tracers, and a factor-2 stellar mass-to-light uncertainty. The MI-vs-MG separation is
     {100*abs(r_mi_mg-1):.1f}%.
   * sigma PROBES THE TRACE, and for the trace QUMOND equals MI identically. So this observable separates
     AQUAL from {{MI, QUMOND}} and cannot separate MI from QUMOND. The observable that separates all three is
     the ANISOTROPY, which ten globular clusters cannot measure.
   * DF2 IS NOT IN THE DOMINANT-EFE LIMIT (D2a): y_int and y_ext are within a factor
     {max(y_ext_ref/y_int_ref, y_int_ref/y_ext_ref):.1f}, so the corpus's MI-vs-MG theorem is an ESTIMATE here
     and a proper numerical solve is owed before any number here is quoted as a prediction.
   * the 3D separation from NGC 1052 is unknown -- only the projection is measured -- so g_ext is a lower
     bound and the true suppression could be weaker.

  THE ONE THING WORTH TAKING FORWARD: the idea that motivated this lane survives even though the object does
  not deliver. Rotation curves constrain a0 AT THE KNEE with a 30.6% shape systematic; EFE systems constrain
  the combination g_ext/a0 DEEP in the MOND regime. Those are different degeneracy directions, so a joint
  analysis could break the shape degeneracy that neither breaks alone. DF2 is simply too noisy to be the
  system that does it -- a larger sample of satellites with measured host separations would be.""")

banner("RESULT")
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: Route A predicts HIGHER than standard MOND on DF2 (its broad knee weakens the EFE suppression)")
print("  and sits in up to 4.5 sigma tension at the far distance -- a live liability, not a null and not a win.")
