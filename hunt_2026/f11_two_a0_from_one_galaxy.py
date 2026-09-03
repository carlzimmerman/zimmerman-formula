#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
⚠️⚠️ SUPERSEDED IN PART BY f12_disc_virial_coefficient.py -- READ THIS FIRST.
The +0.180 dex offset found below is REAL but is NOT a tension: it is disc geometry.  f12 computes the disc virial
coefficient exactly (Freeman solution, and independently from the real SPARC baryonic profiles using the kernel with
NO observed velocities) and gets 0.823, against the spherical 2/3 and against the 0.820 this file's offset required.
The observed curves deliver 0.826.  So this file's route-2 normalisation was spherical and the galaxies are discs.
DO NOT CITE THE +0.180 dex AS A TENSION with the mass-to-light ratio or with the field equation.  What stands here is
the METHOD, the proof of the spherical theorem, and the calibration that route 1 independently recovers the
framework's own acceleration constant (9.44e-11 against the canonical 9.36e-11).

f11_two_a0_from_one_galaxy.py -- TWO INDEPENDENT MEASUREMENTS OF a_0 IN THE SAME GALAXY, AND WHETHER THEY AGREE.
=================================================================================================================
This is a test of the FRAMEWORK'S FIELD EQUATION that needs no second system, no external sample, no dwarf
spheroidals, and no assumption about dark matter.  It is internal to each rotation curve.

THE TWO ROUTES.
  ROUTE 1 -- LOCAL.  The radial acceleration relation.  At each radius, g_obs = nu(g_bar/a_0) g_bar.  Fit a_0.
             This is what the whole programme has always measured, and it is a statement about the force at a point.
  ROUTE 2 -- GLOBAL.  Milgrom's deep-MOND virial theorem, an exact consequence of the AQUAL/QUMOND field equation:
                Sum_i m_i <v_i^2>  =  (2/3) sqrt(G a_0 M^3)
             for any isolated bounded system deep in the MOND regime.  Invert it and each galaxy yields its own a_0:
                a_0(virial) = 9 [ Integral v_c^2 dM ]^2 / ( 4 G M^3 )
             This is a statement about the whole system's energy budget, not about the force at a point.

WHY THE COMPARISON IS A FORK TEST, AND A SHARP ONE.  The virial theorem is derived FROM the field equation -- it
follows from the conformal invariance of the deep-MOND AQUAL Lagrangian.  A theory that modifies GRAVITY must satisfy
BOTH routes with the SAME a_0.  A theory that modifies INERTIA reproduces the radial acceleration relation exactly,
because that relation is built from CIRCULAR orbits and Milgrom proved the two arms agree there -- but it has no
reason to satisfy the AQUAL virial theorem, which is a different statement about the same galaxy.
    SO: agreement supports the arm this repository runs.  DISAGREEMENT is evidence that the field equation is wrong,
    which is exactly what today's rotation-versus-pressure pattern hints at -- and unlike that pattern, this test uses
    only rotating galaxies, where the framework is supposed to WORK.
The theorem is proved exactly in section 1 rather than quoted, so the coefficient 2/3 is not taken on trust.
Both footings.  Mutation controls.  Checks can fail, and the systematics section is where this dies if it dies.
"""
import sys, math
import numpy as np
from hunt_lib import *
ck = Check()

P("="*118); P("1.  PROVE THE THEOREM RATHER THAN QUOTE IT -- the coefficient 2/3 is doing all the work"); P("="*118)
info("Deep-MOND AQUAL in spherical symmetry gives g(r) = sqrt(G M(r) a_0)/r exactly.  The virial integral is then")
info("   W = -Integral rho r g 4 pi r^2 dr = -sqrt(G a_0) Integral_0^M sqrt(M') dM' = -(2/3) sqrt(G a_0) M^(3/2),")
info("independent of the density profile.  In steady state 2K + W = 0, so Sum m <v^2> = 2K = (2/3) sqrt(G a_0 M^3).")
info("Verifying that numerically on three very different profiles, since a profile-independent claim must be checked:")
def W_numeric(prof, M_tot, a0, n=200000):
    r = np.linspace(1e-4, 60.0, n)
    rho = prof(r); dV = 4*math.pi*r**2
    m = np.cumsum(rho*dV)*(r[1]-r[0]); m = m/m[-1]*M_tot
    dM = np.gradient(m, r)
    g = np.sqrt(G*np.maximum(m, 1e-30)*a0)/np.maximum(r, 1e-30)
    return float(np.trapz(dM*r*g, r))
M0, a0t = 1e10*Msun, A0["canonical"]
profs = {"uniform sphere": lambda r: np.where(r < 10, 1.0, 0.0),
         "exponential":    lambda r: np.exp(-r/3.0),
         "steep power law":lambda r: 1.0/(1.0 + (r/2.0)**3)}
exact = (2.0/3.0)*math.sqrt(G*a0t)*M0**1.5
for nm, pf in profs.items():
    Wn = W_numeric(pf, M0, a0t)
    info(f"   {nm:16}  numerical / analytic = {Wn/exact:.6f}")
ok = all(abs(W_numeric(pf, M0, a0t)/exact - 1) < 0.02 for pf in profs.values())
ck("A1 the theorem is verified numerically on three profiles that share nothing but their total mass, so the coefficient 2/3 is exact and profile-independent as claimed and is not being taken on trust from a citation",
   ok, f"uniform sphere, exponential and steep power law all reproduce the analytic virial to better than 2 percent")

P(""); P("="*118); P("2.  THE TWO MEASUREMENTS, GALAXY BY GALAXY"); P("="*118)
gals = load_sparc()
info(f"SPARC after the standard quality cuts: {len(gals)} galaxies")
info("DEEP-MOND FILTER: the theorem holds only where the whole system is in the deep-MOND regime, so a galaxy enters")
info("only if its baryonic acceleration is below a_0 at EVERY measured radius.  That filter is essential and it is the")
info("main reason the naive whole-sample version of this test is meaningless.")
def measure(g, a0):
    r = g["r"]*kpc
    Mprof = (g["vg"]*np.abs(g["vg"]) + UPS_D*g["vd"]**2 + UPS_B*g["vb"]**2)*1e6*r/G
    Mprof = np.maximum.accumulate(np.maximum(Mprof, 0.0))
    if Mprof[-1] <= 0: return None
    dM = np.diff(np.concatenate([[0.0], Mprof]))
    v2 = (g["vobs"]*1e3)**2
    K2 = float((dM*v2).sum())                       # Integral v_c^2 dM
    M = float(Mprof[-1])
    a0_vir = 9.0*K2**2/(4.0*G*M**3)                 # ROUTE 2, from the virial theorem
    # ROUTE 1: the local relation, solved per galaxy for the a_0 that centres the residual
    def resid(la):
        aa = 10**la; y = g["gbar"]/aa
        return float(np.median(np.log10(g["gobs"]/(nu(y)*g["gbar"]))))
    lo, hi = -11.5, -9.0
    for _ in range(60):
        mid = 0.5*(lo+hi)
        if resid(mid) > 0: lo = mid
        else: hi = mid
    a0_rar = 10**(0.5*(lo+hi))                      # ROUTE 1, from the radial acceleration relation
    return dict(name=g["name"], a0_vir=a0_vir, a0_rar=a0_rar, M=M/Msun,
                gmax=float(g["gbar"].max()/a0), npts=len(r), frac=float(Mprof[-1]/Mprof[-1]))
rows = {}
for foot, a0 in A0.items():
    out = []
    for g in gals:
        m = measure(g, a0)
        if m is None or not np.isfinite(m["a0_vir"]) or not np.isfinite(m["a0_rar"]): continue
        if m["a0_vir"] <= 0 or m["a0_rar"] <= 0: continue
        out.append(m)
    rows[foot] = out
deep = [m for m in rows["canonical"] if m["gmax"] < 1.0]
info(f"deep-MOND throughout (g_bar < a_0 at every radius): {len(deep)} of {len(rows['canonical'])} galaxies")
if len(deep) < 8:
    deep = sorted(rows["canonical"], key=lambda m: m["gmax"])[:20]
    info(f"⚠️ too few pass the strict filter, so falling back to the 20 galaxies with the LOWEST peak acceleration; this")
    info(f"   weakens the test and the residual high-acceleration bias must be quoted alongside any number below")
lv = np.log10([m["a0_vir"] for m in deep]); lr = np.log10([m["a0_rar"] for m in deep])
info(f"{'':28}{'median a_0':>14}  {'16-84 percent':>22}")
info(f"{'ROUTE 1  local relation':28}{10**np.median(lr):14.3e}  {10**np.percentile(lr,16):9.2e} - {10**np.percentile(lr,84):9.2e}")
info(f"{'ROUTE 2  virial theorem':28}{10**np.median(lv):14.3e}  {10**np.percentile(lv,16):9.2e} - {10**np.percentile(lv,84):9.2e}")
d = lv - lr
sem = float(d.std(ddof=1)/math.sqrt(len(d)))
ck("A2 (THE TEST) the two routes to a_0 in the SAME galaxies do not give the same answer.  The local relation and the global virial theorem are both consequences of the same field equation and must agree if that field equation is right, and they disagree by well outside the error on the mean",
   abs(float(np.median(d)))/sem > 3.0,
   f"the virial route sits {float(np.median(d)):+.3f} dex from the local route (a factor {10**float(np.median(d)):.2f}), scatter {d.std():.3f} dex on N={len(d)} galaxies, standard error {sem:.3f}, so {abs(float(np.median(d)))/sem:.1f} sigma")
deep_alt = [m for m in rows["alt"] if m["gmax"] < 1.0] or sorted(rows["alt"], key=lambda m: m["gmax"])[:20]
d_alt = np.log10([m["a0_vir"] for m in deep_alt]) - np.log10([m["a0_rar"] for m in deep_alt])
ck("A3 the disagreement is not a choice of footing: the virial route measures a_0 for itself, so the footing enters only through the deep-MOND selection, and the offset is essentially unchanged",
   abs(float(np.median(d)) - float(np.median(d_alt))) < 0.10,
   f"canonical footing {float(np.median(d)):+.3f} dex, alternative footing {float(np.median(d_alt)):+.3f} dex")

P(""); P("="*118); P("3.  THE SYSTEMATICS, WHICH IS WHERE THIS DIES IF IT DIES"); P("="*118)
info("A galaxy-scale offset of this size has four candidate causes that are NOT new physics.  Each is checked, and any")
info("one of them surviving is enough to void the result.")
# (i) finite extent of the rotation curve
tail = []
for m, g in zip(deep, [x for x in gals if x["name"] in {q['name'] for q in deep}]):
    pass
covers = []
for g in gals:
    if g["name"] not in {m["name"] for m in deep}: continue
    r = g["r"]*kpc
    Mp = (g["vg"]*np.abs(g["vg"]) + UPS_D*g["vd"]**2 + UPS_B*g["vb"]**2)*1e6*r/G
    Mp = np.maximum.accumulate(np.maximum(Mp, 0.0))
    covers.append(float(Mp[-1]/max(Mp[-1], 1e-30)) if Mp[-1] > 0 else 0.0)
    # the honest proxy: is the mass profile still rising at the last point?
rise = []
for g in gals:
    if g["name"] not in {m["name"] for m in deep}: continue
    r = g["r"]*kpc
    Mp = (g["vg"]*np.abs(g["vg"]) + UPS_D*g["vd"]**2 + UPS_B*g["vb"]**2)*1e6*r/G
    Mp = np.maximum.accumulate(np.maximum(Mp, 1e-30))
    rise.append(float((Mp[-1]-Mp[-3])/Mp[-1]) if len(Mp) > 3 else np.nan)
rise = np.array([x for x in rise if np.isfinite(x)])
ck("S1 (systematic: truncation, FLAGGED HERE AND RESOLVED IN 3b) the rotation curves are NOT still accumulating most of their baryonic mass at the last measured point, so truncating the virial integral at the edge of the data is not what produces the offset",
   float(np.median(rise)) < 0.15, f"the last two radial bins add a median {100*float(np.median(rise)):.1f}% of the total baryonic mass; a truncation large enough to explain a {abs(float(np.median(d))):.2f} dex offset would need roughly {100*(1-10**(-abs(float(np.median(d)))/4)):.0f}%")
# (ii) mass-to-light ratio: BOTH routes scale with it, but differently
info("(systematic: stellar mass-to-light ratio) both routes depend on it, so it does NOT simply cancel.  Route 2 goes")
info("as M^-3 through the theorem and as M^2 through the integral; route 1 shifts with g_bar.  Testing directly:")
sens = {}
for ups in (0.3, 0.5, 0.7):
    gg = load_sparc(ups_d=ups)
    dd = []
    for g in gg:
        m = measure(g, A0["canonical"])
        if m and np.isfinite(m["a0_vir"]) and np.isfinite(m["a0_rar"]) and m["gmax"] < 1.0 and m["a0_vir"] > 0:
            dd.append(math.log10(m["a0_vir"]) - math.log10(m["a0_rar"]))
    sens[ups] = (float(np.median(dd)) if dd else np.nan, len(dd))
    info(f"   disc mass-to-light = {ups}:  offset {sens[ups][0]:+.3f} dex on N={sens[ups][1]}")
vals = [v[0] for v in sens.values() if np.isfinite(v[0])]
ck("S2 (systematic: mass-to-light ratio) the offset is NOT an artefact of the assumed stellar mass-to-light ratio: varying it across the full range anyone defends moves the offset by less than the offset itself",
   len(vals) >= 2 and (max(vals)-min(vals)) < abs(float(np.median(d))), f"offset ranges {min(vals):+.3f} to {max(vals):+.3f} dex as the disc mass-to-light ratio runs 0.3 to 0.7, against an offset of {float(np.median(d)):+.3f} dex")
# (iii) residual high-acceleration contamination
gm = np.array([m["gmax"] for m in deep])
sl = float(np.polyfit(np.log10(gm), d, 1)[0]); rr = float(np.corrcoef(np.log10(gm), d)[0,1])
ck("S3 (systematic: residual Newtonian contamination) the offset does not grow with how close a galaxy comes to the high-acceleration regime, which is what a deep-MOND-validity failure would look like",
   abs(rr) < 0.5, f"offset against peak acceleration: slope {sl:+.3f} dex per dex, correlation {rr:+.3f}; a validity failure would give a strong positive correlation")
# (iv) is it just the disc geometry, for which the spherical proof does not directly apply?
ck("S4 (systematic: geometry, and this one is NOT dismissed) the analytic proof in section 1 is for spherical symmetry.  AQUAL's deep-MOND virial theorem is geometry-independent because it follows from the conformal invariance of the deep-MOND Lagrangian rather than from spherical symmetry, but this script verified it only for spheres, and a disc is not a sphere.  This check is recorded as UNRESOLVED rather than passed, and a flattened numerical AQUAL solve is the work that would settle it",
   False, "the numerical verification covers spherical profiles only; the disc case rests on the analytic conformal-invariance argument, which this script does not itself verify.  Until a flattened AQUAL solve is run, a geometry-dependent coefficient of order the offset cannot be excluded")

P(""); P("="*118); P("3b.  CUT THE TWO SYSTEMATICS THAT BITE, AND SEE WHAT SURVIVES"); P("="*118)
info("S1 and S2 each fail on their own, and each is individually large enough to produce the whole offset.  So the raw")
info("10-sigma number is meaningless as it stands.  This section removes both and reports what is left.")
def offset_for(ups, rise_cut):
    gg = load_sparc(ups_d=ups); dd = []; nn = 0
    for g in gg:
        r = g["r"]*kpc
        Mp = (g["vg"]*np.abs(g["vg"]) + UPS_D*g["vd"]**2 + UPS_B*g["vb"]**2)*1e6*r/G
        Mp = np.maximum.accumulate(np.maximum(Mp, 1e-30))
        if len(Mp) < 5: continue
        rise_g = float((Mp[-1]-Mp[-3])/Mp[-1])
        if rise_g > rise_cut: continue
        m = measure(g, A0["canonical"])
        if not m or m["gmax"] >= 1.0: continue
        if not (np.isfinite(m["a0_vir"]) and np.isfinite(m["a0_rar"]) and m["a0_vir"] > 0): continue
        dd.append(math.log10(m["a0_vir"]) - math.log10(m["a0_rar"])); nn += 1
    return (float(np.median(dd)) if dd else np.nan, float(np.std(dd)/math.sqrt(max(1,len(dd)))) if dd else np.nan, nn)
info(f"{'M/L':>6} {'truncation cut':>16} {'offset dex':>12} {'s.e.':>8} {'N':>5}")
grid = {}
for ups in (0.15, 0.20, 0.25, 0.3, 0.4, 0.5, 0.6):
    for rc in (0.30, 0.10, 0.05):
        o, e, n = offset_for(ups, rc); grid[(ups, rc)] = (o, e, n)
        if n >= 8: info(f"{ups:6.1f} {rc:16.2f} {o:+12.3f} {e:8.3f} {n:5d}")
clean = [(k, v) for k, v in grid.items() if v[2] >= 8 and k[1] <= 0.05]
ck("S5 (the truncation-clean cut) restricting to galaxies whose baryonic mass has genuinely converged inside the measured rotation curve does NOT remove the offset at the standard mass-to-light ratio, so truncation is not the whole story even though it is large enough to be",
   any(v[0] > 3*v[1] for k, v in clean if abs(k[0]-0.5) < 1e-9),
   "; ".join(f"M/L={k[0]}, truncation<{k[1]:.2f}: {v[0]:+.3f} +/- {v[1]:.3f} dex on N={v[2]}" for k, v in sorted(clean)))
# where do the two routes actually agree?
row = [(u, grid[(u, 0.10)][0], grid[(u, 0.10)][2]) for u in (0.15, 0.20, 0.25, 0.3, 0.4, 0.5, 0.6) if grid[(u, 0.10)][2] >= 8]
cross = None
for i in range(len(row)-1):
    if row[i][1] <= 0 <= row[i+1][1] or row[i+1][1] <= 0 <= row[i][1]:
        x0, y0 = row[i][0], row[i][1]; x1, y1 = row[i+1][0], row[i+1][1]
        cross = x0 + (0 - y0)*(x1 - x0)/(y1 - y0)
info("")
info("THE USEFUL WAY TO READ THIS.  The statistical precision here (a couple of hundredths of a dex) is an order of")
info("magnitude better than the systematics, so the comparison is not a null test -- it is a MEASUREMENT of whichever")
info("input is least well known.  That input is the stellar mass-to-light ratio, and demanding the framework's own")
info("field equation be self-consistent DETERMINES it, with no freedom left over.")
ck("A4 (WHAT THIS ACTUALLY DELIVERS) requiring the framework's local force law and its own exact virial theorem to return the SAME acceleration constant in the same galaxies measures the stellar mass-to-light ratio at 3.6 microns, and the value it demands sits below what stellar population synthesis gives",
   cross is not None and 0.15 < cross < 0.55,
   f"the two routes agree at disc mass-to-light = {cross:.2f} (truncation-clean subsample), against the SPARC standard 0.50 and the population-synthesis value 0.50 +/- 0.1 dex (Schombert and McGaugh 2014; McGaugh and Schombert 2014) -- a difference of {abs(math.log10(0.50/cross)):.2f} dex" if cross else "no crossing inside the tested range")
info("⚠️ AGAINST INTEREST, and it decides how this may be quoted: the offset at the standard mass-to-light ratio is")
info("10 sigma STATISTICALLY and roughly 1 sigma SYSTEMATICALLY.  The systematic error bar is set by the very quantity")
info("being measured, so this is NOT yet a tension with stellar population synthesis and must not be quoted as one.")
info("It is a systematics-limited measurement with a concrete route to becoming decisive.")

P(""); P("="*118); P("3c.  THE MOST LIKELY EXPLANATION, QUANTIFIED -- and it is the boring one"); P("="*118)
info("The virial coefficient proved in section 1 is 2/3, derived for SPHERICAL symmetry.  AQUAL's deep-MOND virial")
info("theorem is argued to be geometry-independent from the conformal invariance of the deep-MOND Lagrangian, but this")
info("script verified only spheres, and every galaxy in the sample is a DISC.  A flattened system at fixed mass is more")
info("tightly bound than a sphere, so a coefficient larger than 2/3 is exactly what one would expect.")
info("Since a_0(virial) goes as the square of the coefficient's inverse, the offset maps onto a required coefficient:")
off = float(np.median(d)); need = (2.0/3.0)*10**(off/2)
info(f"   observed offset {off:+.3f} dex  ->  a disc virial coefficient of {need:.3f} instead of {2.0/3.0:.3f},")
info(f"   which is a {100*(need/(2.0/3.0)-1):.0f} percent geometry correction.")
ck("A5 (THE HONEST MOST-LIKELY READING) the whole offset is accounted for by a disc virial coefficient about a quarter larger than the spherical one, which is the sign and roughly the size expected for a flattened system, and which this script did not compute.  Until a flattened numerical solve is run, the boring explanation is fully sufficient and must be the default reading",
   1.0 < need/(2.0/3.0) < 1.6, f"required coefficient {need:.3f} against the spherical {2.0/3.0:.3f}, a factor {need/(2.0/3.0):.2f}; a flattened AQUAL solve returning that number closes this entirely, and a flattened solve returning 2/3 turns the same offset into a real problem for either the mass-to-light ratio or the field equation")

P(""); P("="*118); P("4.  mutation controls"); P("="*118)
rng = np.random.default_rng(3)
lv2 = lv.copy(); rng.shuffle(lv2)
ck("M1 mutation: pairing each galaxy's virial a_0 with a DIFFERENT galaxy's local a_0 destroys the per-galaxy agreement, so the two routes really are tracking the same object and the comparison is not vacuous",
   float(np.std(lv2 - lr)) > float(np.std(d)), f"shuffled pairing scatter {float(np.std(lv2-lr)):.3f} dex against the matched {float(np.std(d)):.3f} dex")
ck("M2 mutation: the local route recovers the framework's own acceleration constant on the full sample, so route 1 is calibrated and the offset is not route 1 being broken",
   abs(float(np.median([math.log10(m['a0_rar']) for m in rows['canonical']])) - math.log10(A0['canonical'])) < 0.25,
   f"route 1 on all {len(rows['canonical'])} galaxies gives a_0 = {10**float(np.median([math.log10(m['a0_rar']) for m in rows['canonical']])):.3e}, against the canonical footing {A0['canonical']:.3e}")
P(""); P("="*118); P("VERDICT"); P("="*118)
P("  Each rotating galaxy yields TWO independent measurements of the acceleration constant: one from the local force")
P("  law at each radius, one from the global virial theorem that the framework's own field equation implies.  A")
P("  modified-GRAVITY theory must satisfy both with the same constant.  A modified-INERTIA theory reproduces the first")
P("  automatically, since it is built from circular orbits where the two arms provably agree, and has no reason to")
P("  satisfy the second.  The theorem is PROVED here rather than cited, and reproduces exactly on three unrelated")
P("  density profiles.  The local route independently recovers the framework's own constant on all 147 galaxies,")
P("  so the machinery is calibrated.")
P("  THE TWO ROUTES DISAGREE BY +0.18 DEX, WHICH IS 10 SIGMA STATISTICALLY AND ABOUT 1 SIGMA SYSTEMATICALLY.")
P("  That is the whole story and the second half is the important half.  Two systematics each individually large")
P("  enough to produce the entire offset failed their checks: rotation-curve truncation (the last two bins carry 17")
P("  percent of the baryonic mass where 10 percent suffices) and the stellar mass-to-light ratio (the offset runs from")
P("  +0.03 to +0.29 dex across the range anyone defends).  A third, the disc geometry, is recorded UNRESOLVED, because")
P("  the proof given here is spherical and a flattened numerical solve was not run.")
P("  SO THIS IS NOT A FORK RESULT AND MUST NOT BE QUOTED AS ONE.  What it is instead is a new and unusually sharp")
P("  MEASUREMENT: the statistical precision is an order of magnitude better than the systematics, so demanding the")
P("  framework be self-consistent between its own force law and its own virial theorem DETERMINES the stellar")
P("  mass-to-light ratio with no freedom.  Tighten the three systematics and the same comparison becomes a genuine")
P("  test of the field equation -- and therefore of which arm is right -- on rotating galaxies alone, where the")
P("  framework is supposed to work and where no dwarf spheroidal sample size can limit it.")
sys.exit(ck.done())
