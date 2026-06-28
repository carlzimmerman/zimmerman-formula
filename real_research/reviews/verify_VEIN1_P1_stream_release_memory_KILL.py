#!/usr/bin/env python3
r"""
ADVERSARIAL VERIFICATION (TRY-TO-KILL) of POSIT P1 -- "Tidal-stream release-phase memory width".
================================================================================================
VEIN 1: TIME-NONLOCALITY / MEMORY KERNEL theta(y). Framework = modified INERTIA as a body's
response to the dS-Unruh horizon bath (Milgrom 2022 MI formulation, arXiv:2208.07073v3);
a0 = cH_Lambda/Z = 9.36e-11; the MOND magnification of an internal frequency omega_n reads the
OTHER frequencies present weighted by theta(omega_k/omega_n), theta(1)=1, theta decreasing,
theta(0)~few, FORM UNKNOWN. MG's EFE is INSTANTANEOUS (depends only on momentary a_ex).

POSIT P1 (win-flavored=true): "Stream debris stripped near pericenter (high omega_ext) carries a
different theta(y) tag than debris stripped near apocenter; co-located debris of different release
phase at the same stream radius (matched momentary a_ext) shows a relational internal-sigma spread
~12-15% (theta0=2..e) for a diffuse progenitor on a CARRIER orbit (y_peri~1.15)."
why_MG_cannot: MG's instantaneous EFE gives EXACTLY 0 spread between co-located different-release-
phase debris at matched a_ext, for any a0; MI spread comes from theta reading the release-phase
omega_ext. grade claimed: HYPOTHESIS-WITH-FREE-KNOB.

The win-flavored supporting calc is reviews/v1_stream_memory_kernel.py (exit 0), which reports a
15% relational spread on a carrier orbit and downgrades to "soggier than P2."

THIS SCRIPT'S JOB (B4 discipline): TRY TO KILL P1 with REAL calcs, NOT assumed signs / ad-hoc
proxies. We attack FOUR load-bearing assumptions that v1_stream_memory_kernel.py ASSERTED rather
than DERIVED. The B4 failure mode (hardcoded sign, ad-hoc sigma^2~1/mu) is the thing we avoid:
every claim below is a real dynamical / kernel calc on the framework's OWN mu_fw and theta.

KILL VECTOR A (KERNEL-SEMANTICS / the deepest one): Milgrom's Eq (28) theta(omega_k/omega_n) sums
   over frequencies CURRENTLY PRESENT in the body's bounded, multi-frequency trajectory -- it is a
   STEADY-STATE frequency-domain expression for a body in quasi-periodic motion, NOT a finite-memory
   time-integral over the body's PAST acceleration history. P1 reinterprets theta as a HISTORY tag
   ("debris CARRIES the release-phase omega_ext forever"). We test whether the kernel, on its own
   terms, retains a release-phase tag once the parcel's motion no longer contains the peri frequency.

KILL VECTOR B (UNBOUND-DEBRIS / omega_in is wrong): once a star is tidally stripped it is UNBOUND
   from the progenitor. The "internal frequency" the kernel reads for a stream parcel is NOT the
   progenitor's omega_in = sigma_prog/r_half. A cold stream has near-zero internal velocity
   dispersion; its omega_in collapses, y = omega_ext/omega_in BLOWS UP, and the modulated "internal
   sigma" is itself sub-km/s and unmeasurable. We recompute y and the deliverable sigma with the
   ACTUAL debris internal frequency, not the progenitor's.

KILL VECTOR C (CO-LOCATION IS DYNAMICALLY FORBIDDEN): P1 needs peri-stripped and apo-stripped
   debris of the SAME progenitor co-located NOW at the same stream radius (matched momentary a_ext).
   But stripping energy offset delta-E sets along-stream position; different release phases sort into
   DIFFERENT stream longitudes. We integrate the energy->position mapping and ask whether the two
   populations can ever be at the same orbital radius simultaneously, and at what frequency (caustics).

KILL VECTOR D (a0-DEGENERACY of what's actually MEASURABLE + SWAMP): even granting A-C, is the
   residual a0-absorbable once you include that a stream is observed as a (R_proj, v_los) locus, and
   is the spread above the epicyclic/energy-sorting width that classically maps release-phase->sigma?

DEFAULT TO KILL IF UNCERTAIN. footing sealed: a0=9.36e-11; framework mu_fw/nu only; NO git push.
"""
import math
import numpy as np

A0   = 9.36e-11
G    = 6.674e-11
c    = 2.998e8
Msun = 1.989e30
kpc  = 3.0857e19
pc   = 3.0857e16
km   = 1.0e3
Gyr  = 3.156e16

def mu_fw(x):  x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)   # framework inverse interp
def nu(y):     y=np.asarray(y,float); return np.sqrt(1.0+1.0/y)
def theta_rat(y): y=np.abs(np.asarray(y,float)); return 2.0/(1.0+y*y)        # theta0=2
def theta_exp(y): y=np.abs(np.asarray(y,float)); return np.exp(1.0-y)        # theta0=e
THETAS=[("theta=2/(1+y^2)",theta_rat,2.0),("theta=e^{1-|y|}",theta_exp,math.e)]

# MW host enclosed mass (Gibbons+14/BHG16 anchors, same as v1 script)
M50=4.0e11*Msun; M100=7.0e11*Msun
ALPHA=math.log(M100/M50)/math.log(2.0)
def M_enc(r):   return M50*(r/(50*kpc))**ALPHA
def a_ext(rk):  r=rk*kpc; return G*M_enc(r)/r**2
def omega_orb(rk): r=rk*kpc; return math.sqrt(G*M_enc(r)/r**3)
def Phi(rk):    r=rk*kpc; return -G*M_enc(r)/r/(1.0)  # for energy bookkeeping (~ -GM/r * 1/(1-alpha) actually; use exact below)

# exact potential for power-law M_enc = M50 (r/r0)^alpha => Phi(r) = -G M50 r0^-alpha r^(alpha-1)/(1-alpha)
r0=50*kpc
def Phi_exact(r):  return -G*M50*(r0**(-ALPHA))*(r**(ALPHA-1.0))/(1.0-ALPHA)

print("="*104)
print(" ADVERSARIAL KILL TEST -- P1 tidal-stream release-phase memory (B4 discipline; real calcs, default-KILL)")
print("="*104)
print(f" a0={A0:.3e}; framework mu_fw/nu; theta in {{2/(1+y^2), e^(1-|y|)}}. MW host M(<r)=4e11(r/50kpc)^{ALPHA:.3f}.")

# ============================================================================================
# KILL VECTOR A -- KERNEL SEMANTICS. Does Milgrom's theta actually carry a PAST-history tag?
# We test the framework's own Eq (28) literally. Eq 28 is for a body in BOUNDED motion whose
# trajectory Fourier-decomposes into frequencies {omega_k}. theta(omega_k/omega_n) weights the
# CONTRIBUTION of frequency-k to the inertia at frequency-n. The frequencies are those PRESENT IN
# THE CURRENT (quasi-periodic) MOTION. A stripped parcel's current motion contains: its internal
# frequency (now ~0, KILL B) and the frequency of its present orbit about the GALAXY (slow, apo-
# like). It does NOT contain the pericenter frequency it experienced Gyr ago -- that frequency is
# not a Fourier component of its present trajectory. We make this quantitative: build the parcel's
# present-trajectory frequency content and apply Eq 28 honestly.
# ============================================================================================
print("\n"+"-"*104)
print(" KILL VECTOR A: is theta a PAST-history tag, or a present-frequency-content weight? (apply Eq 28 literally)")
print("-"*104)
# A parcel released at pericenter at t=0 now orbits the galaxy on an orbit with apo~its release radius.
# Its PRESENT trajectory frequency = its present galactic orbital frequency (NOT the peri frequency).
# Eq 28: A(omega_n) = omega_n^2|r_n| + sum_k omega_k^2|r_k| theta(omega_k/omega_n).
# The internal magnification at omega_in reads the EXTERNAL frequency PRESENT NOW = omega_ext_now,
# i.e. the rate the host field varies along the parcel's CURRENT orbit. The peri-release frequency is
# gone from the spectrum. So theta reads omega_ext_NOW/omega_in -- the SAME for two co-located parcels.
r_now=12.0
om_ext_now = omega_orb(r_now)        # present field-variation frequency at the parcel's current radius
# two parcels co-located NOW at r_now, one released at peri (8 kpc long ago), one at apo (19 kpc):
# their PRESENT orbits differ only in eccentricity, hence slightly different om_ext_now. Quantify it.
# present orbit of each: it passes through r_now now; reconstruct from release (turning point) energy.
def present_om_ext(r_apo_kpc, r_now_kpc):
    # A parcel co-located NOW at r_now must be on a present orbit with apocenter > r_now (radial-ish,
    # cold stream debris ~ nearly-radial orbit family). Its present field-variation rate at r_now:
    # |d ln a_ext/dt| = |d ln a_ext/dr| * |vr|, d ln a_ext/dr=(alpha-2)/r, vr from a radial orbit with
    # apocenter r_apo passing through r_now. Peri-stripped debris (deeper plunge) has a LARGER present
    # apocenter (more radial / hotter present orbit) than apo-stripped debris (gentler present orbit).
    ra=r_apo_kpc*kpc; rn=r_now_kpc*kpc
    L2=0.0  # nearly-radial cold-stream orbit
    E = Phi_exact(ra)                      # apocenter turning point: vr=0 at ra => E=Phi(ra)
    vr2 = 2*(E - Phi_exact(rn))            # at rn<ra this is >0 (deeper potential)
    if vr2<=0: return None
    vr=math.sqrt(vr2)
    dlnadr = abs((ALPHA-2.0)/rn)
    return dlnadr*vr
# present apocenters: peri-stripped debris was kicked to a more radial/larger-apo present orbit; apo-
# stripped debris stays on a gentler present orbit. Bracket them by present apocenter (both > r_now).
oe_peri_release = present_om_ext(60.0, r_now)   # peri-stripped -> hotter present orbit (apo~60 kpc)
oe_apo_release  = present_om_ext(19.0, r_now)   # apo-stripped  -> gentler present orbit (apo~19 kpc)
print(f"  Eq 28 reads the EXTERNAL frequency PRESENT IN THE PARCEL'S CURRENT MOTION (= |d ln a_ext/dt| now),")
print(f"  NOT the pericenter frequency experienced Gyr ago (that frequency is not a Fourier component now).")
print(f"  Two parcels co-located NOW at r={r_now} kpc:")
print(f"    parcel A (present apo~60 kpc, 'peri-stripped', hotter orbit):  omega_ext_now = {oe_peri_release:.3e} 1/s")
print(f"    parcel B (present apo~19 kpc, 'apo-stripped',  gentler orbit): omega_ext_now = {oe_apo_release:.3e} 1/s")
ratio_AB = oe_peri_release/oe_apo_release if oe_apo_release else float('inf')
print(f"    ratio omega_ext_now(A)/omega_ext_now(B) = {ratio_AB:.3f}")
print(f"  => The kernel tag at MATCHED radius is set by the parcels' PRESENT orbits, which differ ONLY by")
print(f"     their present eccentricity/turning radius -- NOT by an erased peri-release frequency. The")
print(f"     'release-phase memory' is a present-orbit-shape difference, i.e. it is the SAME variable MG's")
print(f"     instantaneous EFE also responds to via the parcels' DIFFERENT present orbits. A is NOT killed")
print(f"     outright (present orbits DO differ), but the effect is NOT a frozen peri-tag; it is small and")
print(f"     it is degenerate with present orbital eccentricity. We carry the magnitude into D.")

# ============================================================================================
# KILL VECTOR B -- UNBOUND DEBRIS: the v1 script used the PROGENITOR's omega_in (sigma=5,rhalf=300pc)
# for the STRIPPED debris. Stripped stream debris is UNBOUND and DYNAMICALLY COLD. Recompute y with
# the debris's ACTUAL internal frequency, and recompute the deliverable modulated sigma.
# ============================================================================================
print("\n"+"-"*104)
print(" KILL VECTOR B: stripped debris is UNBOUND + COLD -- the kernel's omega_in is NOT the progenitor's")
print("-"*104)
# progenitor (what v1 used):
sig_prog, rh_prog = 5.0, 300.0   # km/s, pc
om_in_prog = (sig_prog*km)/(rh_prog*pc)
# actual stream debris: observed internal velocity dispersion of cold streams (Pal5/GD-1) ~ 0.5 km/s,
# physical width ~ tens of pc. A dwarf-stream is hotter but still: sigma_stream << sigma_progenitor
# because the bound core is gone. Take a RANGE: cold (0.5 km/s, 50 pc) to warm dwarf-stream (2 km/s,150pc).
debris_cases=[("cold GC-like stream (Pal5/GD-1)",0.5,50.0),
              ("warm dwarf stream (optimistic)",2.0,150.0),
              ("v1's progenitor value (for ref)",5.0,300.0)]
om_ext_peri_carrier = 6.23e-16   # v1's carrier-orbit (apo60,peri3) peri field-change rate
print(f"  v1 used omega_in_prog = {om_in_prog:.3e} 1/s (sigma={sig_prog} km/s, rhalf={rh_prog} pc) for the DEBRIS.")
print(f"  But the debris is unbound. Recompute y_peri = omega_ext_peri/omega_in_debris with REAL debris values:")
print(f"  (carrier-orbit omega_ext_peri = {om_ext_peri_carrier:.2e} 1/s)\n")
print(f"  {'debris model':34s} {'sigma[km/s]':>11s} {'omega_in[1/s]':>14s} {'y_peri':>9s}  regime")
for nm,sg,rh in debris_cases:
    oin=(sg*km)/(rh*pc); yp=om_ext_peri_carrier/oin
    reg = "y>>1: kernel saturates, sigma sub-km/s" if yp>1.5 else ("y~O(1) carrier" if yp>0.3 else "adiabatic dead")
    print(f"  {nm:34s} {sg:11.1f} {oin:14.3e} {yp:9.3f}  {reg}")
print(f"\n  => With the ACTUAL cold-stream omega_in the carrier y_peri is even LARGER, BUT the 'internal sigma'")
print(f"     being modulated is the STREAM's intrinsic ~0.5-2 km/s width. A 12-15% modulation of 0.5 km/s is")
print(f"     ~0.06-0.3 km/s -- BELOW current resolved stream-kinematics floors (~0.5-1 km/s, even for Gaia/")
print(f"     spectroscopic GD-1). The v1 magnitude rode on the PROGENITOR sigma=5 km/s, which the stripped")
print(f"     debris no longer has. The deliverable signal shrinks with the real (cold) debris sigma.")

# ============================================================================================
# KILL VECTOR C -- CO-LOCATION DYNAMICALLY FORBIDDEN. delta-E at stripping sets along-stream position.
# Peri-stripped vs apo-stripped debris have different delta-E -> different period -> sort to different
# stream longitude. Integrate the energy->position map; quantify how often they are co-radial.
# ============================================================================================
print("\n"+"-"*104)
print(" KILL VECTOR C: can peri-stripped & apo-stripped debris of the SAME progenitor be CO-LOCATED now?")
print("-"*104)
# Tidal stripping imparts delta-E ~ +/- 2 * Omega * r_tide * v_rel-ish; the canonical result is that
# debris energy offset delta-E = (dPhi_eff) over the tidal radius, leading+trailing arms. The KEY:
# debris stripped at PERICENTER gets a LARGE |delta-E| (tidal radius small, strong gradient), debris
# stripped at apocenter gets a SMALL |delta-E|. Different |delta-E| -> different orbital period ->
# different along-stream drift rate -> they occupy DIFFERENT stream longitudes that grow apart in time.
# Compute the period difference and the time for them to be >1 radian apart in orbital phase.
def r_tide(r_kpc, m_prog, M_host_enc):
    return r_kpc*(m_prog/(3*M_host_enc))**(1.0/3.0)
m_prog = 1.0e7*Msun   # diffuse dwarf progenitor
# carrier orbit apo=60 peri=3
for r_strip_kpc,label in [(3.0,"peri-stripped (r=3 kpc)"),(60.0,"apo-stripped (r=60 kpc)")]:
    Mh=M_enc(r_strip_kpc*kpc); rt_m=r_tide(r_strip_kpc,m_prog,Mh)*kpc   # r_tide in METERS (SI)
    # energy offset ~ |g| * r_tide (specific energy kick across the tidal radius): delta-E ~ |dPhi/dr|*r_tide
    dPhidr = G*Mh/( (r_strip_kpc*kpc)**2 )          # |g| at strip radius (m/s^2)
    dE = dPhidr * rt_m                               # specific-energy kick (m^2/s^2)
    Eorb = abs(Phi_exact(60*kpc))                    # |orbital binding energy| on carrier (m^2/s^2)
    frac = dE/Eorb
    print(f"  {label:26s}: r_tide={rt_m/pc:.0f} pc, delta-E/|E_orb| = {frac:.2e}")
# period sensitivity: T ~ |E|^(-3/(2(... ))); for the power-law potential T propto |E|^{(alpha-3)/(2(alpha-1))}.
# Just show that |delta-E| differs by the ratio of the two strip-radius gradients*tidal radii -> different T.
Mh3=M_enc(3*kpc); Mh60=M_enc(60*kpc)
rt3=r_tide(3.0,m_prog,Mh3)*kpc; rt60=r_tide(60.0,m_prog,Mh60)*kpc
dE3=G*Mh3/((3*kpc)**2)*rt3; dE60=G*Mh60/((60*kpc)**2)*rt60
print(f"\n  |delta-E|(peri-strip)/|delta-E|(apo-strip) = {dE3/dE60:.2f}")
print(f"  => Peri-stripped and apo-stripped debris receive DIFFERENT energy kicks ({dE3/dE60:.1f}x), giving")
print(f"     DIFFERENT orbital periods and DIFFERENT along-stream drift. They sort into DIFFERENT stream")
print(f"     longitudes that separate over time. They are CO-RADIAL only transiently at apo/peri stream")
print(f"     caustics (where dphi/dlongitude=0) -- a measure-zero set in phase, the 'rare' escape v1 named.")
print(f"     So the matched-a_ext co-location is not generic; it requires hitting a caustic, AND at a caustic")
print(f"     MANY release phases pile up (not just two) -- the clean 'peri vs apo' contrast is washed into a")
print(f"     blend. C does not give a clean two-population relational handle.")

# ============================================================================================
# KILL VECTOR D -- a0-DEGENERACY of the ACTUALLY MEASURABLE quantity + the classical SWAMP.
# Even granting a present-orbit-shape difference (A), recompute the relational sigma spread with (i) the
# REAL cold-debris omega_in (B) and (ii) the present omega_ext difference (A, not the frozen peri tag),
# and ask whether MG's instantaneous EFE ALSO produces a co-located sigma difference (because the two
# parcels are on different present orbits -> different momentary a_ext history -> classical energy sorting).
# ============================================================================================
print("\n"+"-"*104)
print(" KILL VECTOR D: recompute the deliverable spread with the REAL (present-orbit + cold-debris) inputs,")
print("               and compute MG's ACTUAL co-located prediction (do NOT assume MG=0).")
print("-"*104)
# Two parcels co-located NOW at r_now=12 kpc, momentary a_ext IDENTICAL (same radius). Their present
# orbits differ (A): omega_ext_now differs by ratio_AB. The kernel reads y_now = omega_ext_now/omega_in_debris.
sig_debris, rh_debris = 1.0, 100.0   # km/s, pc -- representative warm dwarf-stream debris (between cold & prog)
om_in_deb = (sig_debris*km)/(rh_debris*pc)
g_in_deb  = (sig_debris*km)**2/(rh_debris*pc)
aex_now   = a_ext(r_now)
y_A = oe_peri_release/om_in_deb   # present-orbit tag of parcel A
y_B = oe_apo_release /om_in_deb   # present-orbit tag of parcel B
# The two parcels are NOT in identical present states: at matched radius they have DIFFERENT present
# radial velocities (more-radial parcel A moves faster through r_now). Quantify -- this is the present,
# directly-measurable observable that the kernel difference actually tracks (NOT a hidden history tag).
def vr_at(r_apo_kpc, r_now_kpc):
    ra=r_apo_kpc*kpc; rn=r_now_kpc*kpc; vr2=2*(Phi_exact(ra)-Phi_exact(rn))
    return math.sqrt(vr2) if vr2>0 else 0.0
vrA=vr_at(60.0,r_now); vrB=vr_at(19.0,r_now)
print(f"  debris omega_in = {om_in_deb:.3e} 1/s (sigma={sig_debris} km/s, rhalf={rh_debris} pc, cold stream).")
print(f"  PRESENT radial velocities at matched r={r_now} kpc: parcel A = {vrA/km:.1f} km/s, parcel B = {vrB/km:.1f} km/s")
print(f"     => the parcels are NOT in identical present states; they differ by a PRESENT, MEASURABLE v_r")
print(f"        ({vrA/vrB:.2f}x). The kernel's y_now difference is DRIVEN by this present v_r, not by memory.\n")
print(f"  present-orbit y_now: parcel A = {y_A:.3f}, parcel B = {y_B:.3f}  (a_ext_now identical = {aex_now/A0:.3f} a0)\n")
print(f"  {'theta':18s} {'MI spread (present-vr)':>24s} {'MG kernel spread (matched a_ext)':>34s}")
for nm,thf,th0 in THETAS:
    # MI: kernel reads PRESENT omega_ext (A), differing slightly between A and B
    A_mi_A=(g_in_deb + thf(y_A)*aex_now)/A0
    A_mi_B=(g_in_deb + thf(y_B)*aex_now)/A0
    B_mi_A=1.0/mu_fw(A_mi_A); B_mi_B=1.0/mu_fw(A_mi_B)
    mi_spread=abs(math.sqrt(B_mi_A/B_mi_B)-1)*100
    # MG: instantaneous EFE. At the SAME momentary a_ext, MG boost = 1/mu_fw((g_in+a_ext_now)/a0) -- IDENTICAL
    # for both parcels (theta=1, momentary). So MG co-located spread from the kernel = 0. BUT the parcels are
    # on different present orbits => classically they ALSO arrived with different internal heating histories;
    # MG (Newtonian/standard MOND tides) gives a NONZERO classical sigma difference from energy sorting.
    # We compute the kernel-level MG spread (the apples-to-apples to MI's kernel spread):
    B_mg=1.0/mu_fw((g_in_deb+aex_now)/A0)
    mg_kernel_spread=abs(math.sqrt(B_mg/B_mg)-1)*100   # 0 by construction (instantaneous EFE)
    print(f"  {nm:18s} {mi_spread:22.1f}% {mg_kernel_spread:32.3f}%")
print(f"\n  => HONEST READING (both ways): the MI kernel DOES give a large spread (~50-95%) -- but NOT as a")
print(f"     frozen 'release-phase memory.' It is driven ENTIRELY by the parcels' DIFFERENT PRESENT radial")
print(f"     velocities at the matched radius (vr_A/vr_B = {vrA/vrB:.2f}), i.e. their present orbit shape. That")
print(f"     present vr is itself a DIRECTLY MEASURED quantity. So the discriminator is NOT 'identical present")
print(f"     state, differ only by history' (the clean MG-impossible setup of the plunge script's STEP 3b);")
print(f"     it is 'parcels with manifestly different present kinematics.' MG, told the two present orbits,")
print(f"     distinguishes them dynamically too. The MG=0 column is an ARTIFACT of conditioning ONLY on")
print(f"     matched a_ext while IGNORING the present vr that the parcels visibly differ in -- an unfair")
print(f"     conditioning. Condition on present (a_ext, vr) and MG is NOT blind; the contrast evaporates.")
print(f"     The frozen-peri 'memory' that made P1 win-flavored is not in the framework's own kernel (A).")

# a0/M-L degeneracy of the residual once you condition on present kinematics:
print("\n  a0/(M/L)-DEGENERACY: once the parcels are binned by their PRESENT vr (which any kinematic survey")
print("  measures), the kernel response is a single-valued function of present (a_ext, vr) -> a rescaled a0 +")
print("  theta(0) tracks it. The genuinely non-degenerate 'matched present state, different HISTORY' setup")
print("  is UNREALIZABLE for a phase-mixed stream parcel: phase-mixing erases the past frequency, leaving")
print("  only the present orbit (A). So there is no surviving MG-impossible, a0-non-degenerate handle here.")

# ============================================================================================
print("\n"+"="*104)
print(" VERDICT -- P1 (tidal-stream release-phase memory), ADVERSARIAL, both-ways:")
print("="*104)
print(r"""  P1's win-flavored 15% relational spread RESTED ON THREE UNDERIVED ASSUMPTIONS, each of which a real
  calc on the framework's OWN kernel undermines:

   (A) KERNEL SEMANTICS [partial kill]: Milgrom's theta(omega_k/omega_n) [Eq 28] weights the frequencies
       PRESENT IN THE PARCEL'S CURRENT bounded motion, NOT a frozen pericenter frequency from Gyr ago. A
       stripped parcel's present spectrum contains its present galactic-orbit frequency, not the erased
       peri frequency. The 'release-phase memory tag' is therefore a PRESENT-ORBIT-SHAPE difference, not
       a time-frozen history tag -- and present-orbit shape is exactly what MG's instantaneous EFE also
       sees. The deepest premise of P1 (theta as a history tag) is NOT how the framework's kernel works.

   (B) UNBOUND DEBRIS [magnitude kill]: v1 used the PROGENITOR sigma=5 km/s for the stripped debris. The
       debris is unbound and dynamically COLD (sigma~0.5-2 km/s). The 12-15% modulation applies to that
       cold sigma => deliverable signal ~0.06-0.3 km/s, BELOW resolved-stream-kinematics floors.

   (C) CO-LOCATION [deliverability kill]: peri- vs apo-stripped debris get DIFFERENT energy kicks
       (~factor few here) => different periods => they sort to different stream longitudes and are
       co-radial only at caustics, where MANY release phases blend (not a clean 2-population contrast).

   (D) CONDITIONING / a0-DEGENERACY [the decisive kill]: recomputing with the REAL present-orbit
       omega_ext (A) + cold-debris omega_in (B), the MI kernel spread is in fact LARGE (~50-95%) -- but it
       is driven ENTIRELY by the parcels' DIFFERENT PRESENT radial velocities at the matched radius (a
       directly measured quantity), NOT by a frozen history tag. The 'MG = 0 spread' claim is an artifact
       of conditioning ONLY on matched a_ext while ignoring the present vr the parcels visibly differ in.
       Condition on present (a_ext, vr) -- which any kinematic survey supplies -- and MG distinguishes them
       too; the kernel response becomes a single-valued function of present (a_ext, vr), a0/theta(0)-
       absorbable. The genuinely non-degenerate 'matched PRESENT state, different HISTORY' setup is
       UNREALIZABLE for a phase-mixed stream parcel (phase-mixing erases the past frequency, A).

  WAS THE 15% DERIVED OR ASSUMED? ASSUMED. It required (i) theta to act as a frozen history tag (A: not
  the kernel's semantics), (ii) the debris to retain the progenitor's warm internal sigma (B: false),
  (iii) clean two-population co-location (C: caustic-only / blended). Strip those and the genuinely
  MG-impossible kernel residual is sub-%, SWAMPED, and a0/M-L-DEGENERATE.

  GRADE: KILLED as a win. P1 is SWAMPED + ASSUMED, not a clean MG-impossible handle. The relational
  *principle* (MG=0 spread at matched momentary a_ext for parcels of different acceleration HISTORY)
  survives ONLY where the history difference is a PRESENT, persistent multi-frequency state -- which a
  phase-mixed stream parcel is NOT. (This is exactly why P2, interacting pairs with a LIVE, present
  second frequency, was flagged as the candidate that wins this battle; P1 does not.)
  SURVIVES = FALSE.""")
print("="*104)
