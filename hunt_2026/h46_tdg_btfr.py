#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h46_tdg_btfr.py -- HUNT ITEM 46: tidal dwarf galaxies on the baryonic Tully-Fisher relation.
============================================================================================================================
Item 46 is the cleanest paradigm test in the whole hunt list, because the two theories disagree about the SIGN.
    LambdaCDM: a tidal dwarf condenses out of the collisional debris of a merger.  Tidal forces cannot pull hot halo
        particles into a cold tail, so a TDG must be free of non-baryonic dark matter, must have M_dyn/M_bar = 1, and must
        therefore sit OFF the baryonic Tully-Fisher relation, to the low-velocity side.
    The framework: the BTFR is not a coincidence of halo formation, it is the acceleration law.  M_bar = V^4/(G a_0) holds
        for anything in equilibrium, whatever it is made of and however it formed.  A TDG must sit ON the relation.
There is no way for both to be right.  This is a genuine fork, and it is the reason the hunt list gave item 46 "low effort".

DATA: Lelli et al. 2015, A&A 584, A113 (arXiv:1509.05404) -- six bona-fide TDGs around NGC 4694, NGC 5291 and NGC 7252, with
3-D HI disc models, asymmetric-drift-corrected circular velocities, and a full baryonic budget (atomic + molecular + stars).
Transcribed to real_research/data/tdg/lelli2015_tdgs.csv from the paper's own LaTeX tables.

WHY THIS ITEM IS SPECIAL AS A CODE TEST: Lelli+2015 did the MOND calculation themselves, with the QUMOND one-dimensional
external-field formula (their eq. 8 = Famaey & McGaugh 2012 eq. 60) and the McGaugh 2008 nu_n family.  Their n = 1 member is
IDENTICAL to this repository's Route A kernel.  Their table therefore contains a published, independent computation of exactly
what this script computes -- at their a_0 = 1.30e-10 m/s^2.  Section 1 reproduces it before anything else is claimed.
Both footings.  Newtonian / LambdaCDM alternative computed beside the framework.  Checks CAN fail.  Mutation controls at the end.
"""
import sys, math, csv
import numpy as np
from hunt_lib import *
ck = Check()

A0_LELLI = 1.30e-10                                   # the a_0 Lelli+2015 used -- 39% above the canonical footing

def _erfinv(y):
    """inverse error function by bisection -- no scipy dependency, and only used to quote a p-value in sigma."""
    lo, hi = 0.0, 10.0
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if math.erf(mid) < y: lo = mid
        else: hi = mid
    return 0.5*(lo + hi)

def a_int(gNi, gNe, a0):
    """QUMOND 1-D external-field formula, Famaey & McGaugh 2012 eq. 60 / Lelli+2015 eq. 8."""
    nt = nu_s((gNi + gNe)/a0); ne = nu_s(gNe/a0) if gNe > 0 else 0.0
    return gNi*nt + gNe*(nt - ne)

tdg = []
for r in csv.DictReader(l for l in open(os.path.join(DATA, "tdg", "lelli2015_tdgs.csv")) if not l.startswith("#")):
    d = {k: (r[k] if k == "name" else float(r[k])) for k in r}
    d["Mbar_kg"] = d["Mbar"]*1e8*Msun; d["eMbar_kg"] = d["eMbar"]*1e8*Msun
    d["Rout_m"] = d["Rout"]*kpc; d["eRout_m"] = d["eRout"]*kpc
    tdg.append(d)

def V_pred(d, a0, efe=True, Mbar_kg=None, Rout_m=None, kernel=True, gNe_over_a0=None):
    """Circular velocity at R_out.  gNi from the baryons; gNe from the host, taken from the paper's own tabulated
    g_Ne/a_0 -- which is a fixed PHYSICAL acceleration, so it is rescaled when a_0 changes, not held at the same ratio."""
    M = d["Mbar_kg"] if Mbar_kg is None else Mbar_kg
    R = d["Rout_m"] if Rout_m is None else Rout_m
    gNi = G*M/R**2
    gNe_phys = (d["gNe_a0"] if gNe_over_a0 is None else gNe_over_a0)*A0_LELLI
    a = a_int(gNi, gNe_phys if efe else 0.0, a0) if kernel else gNi
    return math.sqrt(a*R)/1e3

P("="*128); P("1. VALIDATION -- reproduce Lelli+2015's own MOND columns with the Route A kernel before claiming anything"); P("="*128)
info("Lelli+2015 Table 5 gives V_ISO and V_EFE for nu_n with n = 1, which is exactly Route A, at a_0 = 1.30e-10 m/s^2.")
riso, refe = [], []
for d in tdg:
    vi = V_pred(d, A0_LELLI, efe=False); ve = V_pred(d, A0_LELLI, efe=True)
    gNi_chk = G*d["Mbar_kg"]/d["Rout_m"]**2/A0_LELLI
    riso.append(vi/d["VISO1"]); refe.append(ve/d["VEFE1"])
    info(f"  {d['name']:11} g_Ni/a0 here {gNi_chk:.3f} (paper {d['gNi_a0']:.3f}) | V_ISO here {vi:5.1f} (paper {d['VISO1']:4.0f}) "
         f"| V_EFE here {ve:5.1f} (paper {d['VEFE1']:4.0f}) | MEASURED V_circ {d['Vcirc']:4.0f} +- {d['eVcirc']:.0f}")
riso, refe = np.array(riso), np.array(refe)
gchk = np.array([G*d["Mbar_kg"]/d["Rout_m"]**2/A0_LELLI/d["gNi_a0"] for d in tdg])
ck("46-V1 the internal Newtonian accelerations recomputed from the published M_bar and R_out reproduce the paper's own "
   "g_Ni/a_0 column, so the transcribed table is internally consistent",
   abs(gchk.mean() - 1.0) < 0.05, f"ratio {gchk.mean():.4f} +- {gchk.std():.4f} over {len(tdg)} TDGs")
ck("46-V2 GOLD-STANDARD VALIDATION of the external-field machinery used in h43/h44/h45 as well as here: at the paper's own a_0 "
   "the Route A kernel reproduces Lelli+2015's published isolated AND external-field MOND velocities to better than 2%.  This "
   "is an independent check of the QUMOND eq.-60 implementation against a careful published calculation",
   abs(riso.mean() - 1.0) < 0.02 and abs(refe.mean() - 1.0) < 0.02 and riso.std() < 0.02 and refe.std() < 0.02,
   f"V_ISO ratio {riso.mean():.4f} +- {riso.std():.4f}; V_EFE ratio {refe.mean():.4f} +- {refe.std():.4f}")

P(""); P("="*128); P("2. THE TEST at the framework's own footings"); P("="*128)
def table(a0, label, efe=True, kernel=True):
    z, rows = [], []
    for d in tdg:
        vp = V_pred(d, a0, efe=efe, kernel=kernel)
        # error on the prediction: M_bar and R_out varied ONE AT A TIME and added in quadrature (they are not correlated;
        # varying them together lets the deep-MOND M and R dependences cancel and gives absurdly small error bars)
        dM = 0.5*abs(V_pred(d, a0, efe=efe, kernel=kernel, Mbar_kg=d["Mbar_kg"] + d["eMbar_kg"])
                     - V_pred(d, a0, efe=efe, kernel=kernel, Mbar_kg=d["Mbar_kg"] - d["eMbar_kg"]))
        dR = 0.5*abs(V_pred(d, a0, efe=efe, kernel=kernel, Rout_m=d["Rout_m"] + d["eRout_m"])
                     - V_pred(d, a0, efe=efe, kernel=kernel, Rout_m=max(d["Rout_m"] - d["eRout_m"], 0.2*d["Rout_m"])))
        evp = math.hypot(dM, dR)
        s = (vp - d["Vcirc"])/math.hypot(d["eVcirc"], evp)
        z.append(s); rows.append((d["name"], vp, evp, d["Vcirc"], d["eVcirc"], s))
    z = np.array(z)
    for n, vp, evp, vo, evo, s in rows:
        info(f"  {label:26} {n:11} predicted {vp:5.1f} +- {evp:4.1f} | measured {vo:4.0f} +- {evo:.0f} km/s | {s:+5.2f} sigma")
    info(f"  {label:26} {'COMBINED':11} mean tension {z.mean():+.2f} sigma per TDG, sum/sqrt(N) = "
         f"{z.sum()/math.sqrt(len(z)):+.2f} sigma, chi^2 = {np.sum(z**2):.1f} on {len(z)} points")
    return z, np.array([r[1] for r in rows])
Z = {}
for foot, a0 in A0.items():
    Z[(foot, "efe")], V_efe = table(a0, f"{foot} + EFE")
    Z[(foot, "iso")], V_iso = table(a0, f"{foot} isolated", efe=False)
    P("")
Z[("newton", "n")], V_N = table(A0["canonical"], "Newtonian (no dark matter)", kernel=False)
zl, _ = table(A0_LELLI, "Lelli a_0 = 1.30e-10 + EFE")

zc = Z[("canonical", "efe")]; za = Z[("alt", "efe")]; zn = Z[("newton", "n")]
ck("46a THE RESULT, and it is a LIABILITY: the framework over-predicts the rotation of every one of the six tidal dwarfs, on "
   "both footings, with the external-field effect included.  The LambdaCDM expectation -- that a TDG is dark-matter free and "
   "obeys plain Newtonian gravity with its observed baryons -- fits them, and the framework does not",
   zc.mean() > 0.7 and za.mean() > 0.7 and abs(zn.mean()) < 0.7,
   f"canonical + EFE: mean {zc.mean():+.2f} sigma per TDG, combined {zc.sum()/math.sqrt(len(zc)):+.2f} sigma, chi^2 "
   f"{np.sum(zc**2):.1f}/{len(zc)}; alt + EFE: {za.mean():+.2f} / {za.sum()/math.sqrt(len(za)):+.2f} sigma; "
   f"Newtonian: {zn.mean():+.2f} / {zn.sum()/math.sqrt(len(zn)):+.2f} sigma, chi^2 {np.sum(zn**2):.1f}/{len(zn)}")
ck("46b the framework's own a_0 footings make the tension SMALLER than the a_0 = 1.30e-10 that Lelli+2015 used, because a lower "
   "a_0 predicts lower velocities -- so part of the published 'MOND fails on TDGs' result is an a_0 choice, and that part is "
   "quantified here rather than left implicit.  It is not enough to remove the liability",
   zc.sum()/math.sqrt(len(zc)) < zl.sum()/math.sqrt(len(zl)) and zc.sum()/math.sqrt(len(zc)) > 1.0,
   f"combined tension {zl.sum()/math.sqrt(len(zl)):+.2f} sigma at a_0 = 1.30e-10 (the paper's value), "
   f"{zc.sum()/math.sqrt(len(zc)):+.2f} sigma at 9.36e-11 (canonical), {za.sum()/math.sqrt(len(za)):+.2f} sigma at 1.13e-10 (alt)")

P(""); P("="*128); P("3. what it would take to save it -- stated so the size of the gap is explicit"); P("="*128)
for d in tdg:
    lo, hi = 0.02*d["Mbar_kg"], 3.0*d["Mbar_kg"]
    for _ in range(80):
        mid = math.sqrt(lo*hi)
        if V_pred(d, A0["canonical"], Mbar_kg=mid) > d["Vcirc"]: hi = mid
        else: lo = mid
    d["Mneed"] = math.sqrt(lo*hi)/(1e8*Msun)
    lo, hi = 1.0*d["Rout_m"], 60.0*d["Rout_m"]
    for _ in range(80):
        mid = math.sqrt(lo*hi)
        if V_pred(d, A0["canonical"], Rout_m=mid) < d["Vcirc"]: hi = mid
        else: lo = mid
    d["Rneed"] = math.sqrt(lo*hi)/kpc
    info(f"  {d['name']:11} needs M_bar = {d['Mneed']:5.2f}e8 Msun instead of the measured {d['Mbar']:5.2f} +- {d['eMbar']:.1f}e8 "
         f"({d['Mneed']/d['Mbar']:.2f}x, i.e. {abs(math.log10(d['Mneed']/d['Mbar'])):.2f} dex), or an external field "
         f"{'>' if d['Rneed'] > 50*d['Rout'] else ''}far stronger than the host can supply")
mn = np.array([d["Mneed"]/d["Mbar"] for d in tdg])
ck("46d the size of the gap, stated plainly: to put these six TDGs on the framework's law their baryonic masses would have to "
   "be 2-5x SMALLER than measured -- and their baryon budgets are HI-dominated, directly measured from resolved 21-cm maps, and "
   "would have to be wrong by more than the total molecular plus stellar content to close it",
   mn.max() < 0.75 and mn.min() > 0.1,
   f"required M_bar/measured M_bar = {mn.min():.2f}-{mn.max():.2f} (median {np.median(mn):.2f}); the measured M_bar errors are "
   f"{np.mean([d['eMbar']/d['Mbar'] for d in tdg])*100:.0f}% on average")

P(""); P("="*128); P("4. the same thing said as a BTFR position -- which is how the hunt list posed it"); P("="*128)
info("The hunt list's promotion criterion for item 46 was 'all TDGs within 0.15 dex of the line'.  The BTFR line the framework")
info("predicts is M_bar = V_circ^4/(G a_0), with NO external-field correction -- the EFE version is quoted beside it.")
for foot, a0 in A0.items():
    off, offe = [], []
    for d in tdg:
        Mb_line = (d["Vcirc"]*1e3)**4/(G*a0)/Msun
        off.append(math.log10(d["Mbar"]*1e8/Mb_line))
        offe.append(math.log10(d["Mbar"]/d["Mneed"]))  # dex in mass, EFE-corrected: solved numerically in section 3
    off, offe = np.array(off), np.array(offe)
    info(f"{foot:10} offset from the bare BTFR line M_bar = V^4/(G a_0): {off.min():+.2f} to {off.max():+.2f} dex in M_bar "
         f"(median {np.median(off):+.2f}) -- the TDGs are TOO BARYON-RICH for their rotation.  With the external field folded in "
         f"(canonical solve): median {np.median(offe):+.2f} dex")
    if foot == "canonical": OFF, OFFE = off, offe
ck("46c the hunt list's own promotion criterion is missed, by a lot and in the direction LambdaCDM predicts: the TDGs sit far "
   "to the low-velocity side of the framework's BTFR, i.e. they are too baryon-rich for their rotation.  Not one of the six is "
   "within the 0.15 dex the item asked for",
   np.median(OFF) > 0.15 and (np.abs(OFF) < 0.15).sum() == 0,
   f"canonical: median offset {np.median(OFF):+.2f} dex in M_bar from the bare line ({(np.abs(OFF)<0.15).sum()}/{len(OFF)} "
   f"within 0.15 dex), {np.median(OFFE):+.2f} dex once the external field is folded in")

P(""); P("="*128); P("5. the honest defences, computed rather than asserted"); P("="*128)
info("(a) EQUILIBRIUM.  Lelli+2015's own strongest caveat: these HI discs have completed less than one orbit since the merger")
info(f"    (t_merg/t_orb = 0.2-0.8), so V_circ may not trace the potential.  If the discs are still expanding, the true")
info("    equilibrium velocity would be HIGHER than measured and the tension would shrink.  This is not a defence the data can")
info("    settle, and it applies equally to the LambdaCDM reading, which is why the paper reports both.")
info("(b) WHICH KINEMATICS.  Milgrom (2007) and Gentile et al. (2007) found MOND SUCCEEDED on the same three NGC 5291 TDGs,")
info("    using Bournaud et al. 2007's kinematics.  Lelli+2015's 3-D disc models lowered V_rot by ~2x and raised M_gas by")
info("    ~1.5-2x, which is what turned the success into a failure.  So item 46's verdict is a bet on whose HI modelling is")
info("    right, not on the acceleration law -- and this script bets on the newer, resolved, 3-D-modelled analysis.")
# The B07-era numbers are taken from Lelli+2015's OWN Appendix A rather than guessed: "adopting the kinematical parameters of
# B07 (i = 45 deg, sigma_HI = 10 km/s, and V_rot from 50 to 70 km/s depending on the TDG)", and "we estimate both higher values
# of M_gas (by factors of ~1.5 to ~2) and lower values of V_rot (by a factor of ~2)".  An earlier draft of this script scaled
# V_circ by 2 per galaxy and printed the product as "B07-era V_rot"; that was a fabrication and is removed -- only the
# published range is quoted, and the B07-era baryon budget is shown as the 1.5x-2x band, not a single invented factor.
B07_VROT = (50.0, 70.0)
B07_MGAS = (1.5, 2.0)
vB = []
for d in tdg:
    if d["name"].startswith("NGC5291"):
        vB.append((d["name"], V_pred(d, A0["canonical"], Mbar_kg=d["Mbar_kg"]/B07_MGAS[1]),
                   V_pred(d, A0["canonical"], Mbar_kg=d["Mbar_kg"]/B07_MGAS[0]), d["Vcirc"]))
for n, vlo, vhi, vo in vB:
    info(f"    {n:11} with a B07-era gas budget (M_bar / {B07_MGAS[0]:.1f}-{B07_MGAS[1]:.1f}) the framework predicts "
         f"{vlo:.0f}-{vhi:.0f} km/s; B07's own V_rot for these three was {B07_VROT[0]:.0f}-{B07_VROT[1]:.0f} km/s (Lelli+2015 "
         f"App. A), against {vo:.0f} km/s now -- the older numbers were consistent, the newer ones are not")
info("(c) THE EXTERNAL FIELD is already included, with the paper's own g_Ne, and it is what brings the prediction down from")
info(f"    {np.mean([V_pred(d, A0['canonical'], efe=False) for d in tdg]):.0f} to {np.mean([V_pred(d, A0['canonical']) for d in tdg]):.0f} km/s on average against a measured mean of "
     f"{np.mean([d['Vcirc'] for d in tdg]):.0f}.  A stronger field cannot be invoked: it is set by the host's")
info("    measured K-band luminosity and the projected separation, and the projected separation is a LOWER bound on the true one,")
info("    so the true field is if anything WEAKER and the true prediction HIGHER.  That defence is closed.")
# BUG FOUND AND FIXED IN THIS SCRIPT: an infinitely strong external field drives a_int -> g_Ni, i.e. the prediction bottoms out
# at the NEWTONIAN velocity and cannot go below it.  For any TDG whose measured V_circ is already below its Newtonian floor no
# external field of any strength reaches it, and a naive bisection then just returns its own upper bracket.  The first version
# of this script did exactly that and printed "29411x" for two of the six, which is a bracket artefact and not a number.
gNe_needed, unreachable = [], []
for d in tdg:
    vN = V_pred(d, A0["canonical"], kernel=False)
    if vN >= d["Vcirc"]:
        unreachable.append((d["name"], vN, d["Vcirc"], (vN - d["Vcirc"])/d["eVcirc"]))
        continue
    lo, hi = d["gNe_a0"], 5000.0
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        if V_pred(d, A0["canonical"], gNe_over_a0=mid) < d["Vcirc"]: hi = mid
        else: lo = mid
    gNe_needed.append(math.sqrt(lo*hi)/d["gNe_a0"])
gNe_needed = np.array(gNe_needed)
for n, vN, vo, s in unreachable:
    info(f"    {n:11} has NO finite external field that works: even the Newtonian floor {vN:.1f} km/s exceeds the measured "
         f"{vo:.0f} km/s (by {s:+.2f} sigma, i.e. not significantly -- these two are the two TDGs the framework misses least)")
ck("46e the external-field escape is CLOSED, quantitatively: saving the framework by strengthening the host field alone would "
   f"need external fields {gNe_needed.min():.0f}-{gNe_needed.max():.0f}x the ones the hosts' measured luminosities supply for the "
   f"{len(gNe_needed)} TDGs where a finite field exists at all, and for the other {len(unreachable)} there is no such field at any "
   "strength because the prediction bottoms out at the Newtonian floor.  The projected separations used are lower bounds, so the "
   "true fields are weaker still and the true predictions higher",
   len(gNe_needed) > 0 and gNe_needed.min() > 3.0 and len(unreachable) == 2,
   f"required g_Ne / published g_Ne = {gNe_needed.min():.1f}x to {gNe_needed.max():.1f}x (median {np.median(gNe_needed):.1f}x) "
   f"for {len(gNe_needed)}/{len(tdg)}; unreachable at any field strength: {', '.join(n for n, *_ in unreachable)}")

P(""); P("="*128); P("5b. the combined significance, taken apart -- AGAINST the liability this script is booking"); P("="*128)
info("The +4.2 sigma 'combined' number above adds six z-scores as if they were six independent experiments.  They are not:")
info("three of them share NGC 5291's data cube, distance, inclination convention and host mass, two share NGC 7252's.  Both")
info("weakenings and strengthenings of the liability are computed here, and the weakening is stated first.")
hostof = lambda n: "NGC5291" if n.startswith("NGC5291") else ("NGC7252" if n.startswith("NGC7252") else "VCC2062")
groups = {}
for i, d in enumerate(tdg): groups.setdefault(hostof(d["name"]), []).append(zc[i])
gz = np.array([np.mean(v) for v in groups.values()])
comb_naive, comb_host = zc.sum()/math.sqrt(len(zc)), gz.sum()/math.sqrt(len(gz))
info(f"  per-host mean tension: " + ", ".join(f"{k} {np.mean(v):+.2f} sigma (N={len(v)})" for k, v in groups.items()))
info(f"  combining ONE point per host instead of one per TDG: {comb_host:+.2f} sigma, against {comb_naive:+.2f} sigma naive.")
tstat = gz.mean()/(gz.std(ddof=1)/math.sqrt(len(gz)))
p_two = 1.0 - tstat/math.sqrt(tstat*tstat + 2.0)          # exact two-sided p for Student t with nu = 2
sig_t = math.sqrt(2.0)*_erfinv(1.0 - p_two)
info(f"  a Student t on the three host means alone gives t = {tstat:+.2f} on 2 d.o.f., i.e. p = {p_two:.3f} two-sided = "
     f"{sig_t:.2f} sigma -- with only three independent systems the t distribution's tails are fat and the large t buys little")
# what single coherent error would erase it?  V_pred scales as sqrt(D) (M_bar ~ D^2, R_out ~ D, so g_Ni and g_Ne are both
# distance-invariant and V^2 = a_int R ~ D), while the measured V_circ does not depend on distance at all.
ratio = np.array([V_pred(d, A0["canonical"])/d["Vcirc"] for d in tdg])
f_need = float(np.median(ratio))
info(f"  the coherent error that WOULD erase it: every prediction would have to come down by a factor {f_need:.2f} (median of "
     f"{ratio.min():.2f}-{ratio.max():.2f}).  V_pred scales as sqrt(D) here, so that is a distance error of {f_need**2:.1f}x;")
info(f"  Lelli+2015 bound the distance error on these systems at <12% (Hubble flow at V_sys > 4300 km/s; Virgo for VCC 2062),")
info(f"  which moves V_pred by only {100*(1.12**0.5 - 1):.0f}%.  Alternatively every inclination would have to be wrong by enough to")
info(f"  raise the measured velocities {f_need:.2f}x, i.e. sin(i) too large by that factor -- for NGC 7252E, i = 80 deg, sin i = 0.98,")
info(f"  which cannot be reduced by more than {100*(1-0.98):.0f}% at all.  Neither coherent escape is available.")
ck("46f AGAINST THE LIABILITY, reported before it is banked: the headline '+4.2 sigma combined' is an over-statement, because "
   "the six TDGs are three host systems and their errors are not independent.  Collapsing to one point per host gives "
   f"{comb_host:+.2f} sigma, and a t-test on three host means alone lands under 3 sigma.  The liability survives on the SIGN and "
   "on the size of the offset (a factor 1.6 in velocity, 2.8 in mass), not on the naive combined significance, and this script "
   "will not quote that combined number without this line attached",
   comb_host < comb_naive and comb_host > 2.0 and sig_t < 3.0,
   f"naive {comb_naive:+.2f} sigma on 6 TDGs -> {comb_host:+.2f} sigma on 3 hosts, {sig_t:.2f} sigma by a t-test on the host "
   f"means (p = {p_two:.3f}); per-host means " +
   ", ".join(f"{k} {np.mean(v):+.2f}" for k, v in groups.items()) +
   f"; the coherent velocity error needed to erase it is {f_need:.2f}x = a {f_need**2:.1f}x distance error against a published 12% bound")

P(""); P("="*128); P("6. mutation controls"); P("="*128)
ck("M1 mutation -- switching the kernel off (nu = 1, plain Newton with the same baryons) must CHANGE the answer, and here it "
   "must change it in the direction of agreement, since that is the LambdaCDM expectation being tested",
   abs(zn.mean()) < abs(zc.mean()) - 0.3, f"mean tension {zc.mean():+.2f} sigma with the kernel, {zn.mean():+.2f} sigma without")
z10 = np.array([(V_pred(d, 10*A0["canonical"]) - d["Vcirc"])/d["eVcirc"] for d in tdg])
ck("M2 mutation -- a_0 raised 10x must make the over-prediction much worse (V ~ a_0^{1/4} in the deep-MOND limit)",
   z10.mean() > zc.mean() + 0.5, f"mean tension {zc.mean():+.2f} -> {z10.mean():+.2f} sigma at 10 a_0")
rng = np.random.default_rng(46)
perm = rng.permutation([d["Vcirc"] for d in tdg])
zsh = np.array([(V_pred(d, A0["canonical"]) - perm[i])/d["eVcirc"] for i, d in enumerate(tdg)])
ck("M3 mutation -- shuffling which TDG gets which measured velocity must inflate the scatter of the tension, i.e. the "
   "systematic over-prediction must not be a fluke of six numbers that would look the same in any order",
   zsh.std() > zc.std(), f"shuffled scatter {zsh.std():.2f} vs real {zc.std():.2f} sigma per TDG")

P(""); P("="*128); P("VERDICT"); P("="*128)
P("  ITEM 46 -- a LIABILITY, and the sharpest one in this pass, because the two paradigms disagree about the sign and the data")
P("  come down on the other side.")
P(f"  All six of Lelli et al. 2015's bona-fide tidal dwarfs rotate more slowly than the framework requires.  With the external")
P(f"  field included and no free parameter, the canonical footing over-predicts by {zc.mean():+.2f} sigma per galaxy "
  f"({comb_naive:+.2f} sigma if the six are")
P(f"  treated as independent, {comb_host:+.2f} sigma collapsed to their three independent host systems, which is the number to quote;")
P(f"  chi^2 = {np.sum(zc**2):.1f} on {len(zc)} points); the alt footing by {za.mean():+.2f} sigma.  A dark-matter-free Newtonian prediction using the same")
P(f"  measured baryons fits them at {zn.mean():+.2f} sigma per galaxy -- which is exactly what LambdaCDM says a tidal dwarf should do.")
P(f"  On the hunt list's own criterion -- all TDGs within 0.15 dex of the BTFR -- the score is 0 of 6, median offset {np.median(OFF):+.2f} dex.")
P("  Two things are reported in the framework's favour and neither rescues it:")
P(f"    * the repository's a_0 footings are LOWER than the 1.30e-10 the paper used, which cuts the published tension from")
P(f"      {zl.sum()/math.sqrt(len(zl)):+.2f} sigma to {zc.sum()/math.sqrt(len(zc)):+.2f} sigma combined.  Smaller, still there.")
P("    * the older kinematics (Bournaud+2007), on which Milgrom 2007 and Gentile+2007 declared a MOND success for the same")
P("      three NGC 5291 objects, WOULD have agreed.  Item 46's verdict therefore rides on trusting Lelli+2015's 3-D HI disc")
P("      models over the earlier position-velocity estimates.  This script trusts the newer analysis and says so.")
P("  The two escapes that could be closed here are closed: the external field is already included at the hosts' own measured")
P(f"  luminosities and would have to be {np.median(gNe_needed):.0f}x stronger to work on the four TDGs where any finite field works at all")
P(f"  (for {' and '.join(n for n, *_ in unreachable)} no field of any strength reaches the measurement, because the prediction")
P(f"  bottoms out at the Newtonian floor), and the baryon budgets would have to be {1/np.median(mn):.1f}x too high when they")
P("  are HI-dominated and directly mapped.  The one escape that stays open is dynamical equilibrium: these discs have completed")
P("  less than one orbit since the merger, and Lelli+2015 say so themselves.  That caveat is the reason this is booked as a")
P("  LIABILITY on the ledger rather than as a kill.")
P("  Code note: section 1 reproduces the paper's own published MOND velocities to better than 2% with the Route A kernel, which")
P("  validates the QUMOND external-field implementation shared with h43/h44/h45.")
sys.exit(ck.done())
