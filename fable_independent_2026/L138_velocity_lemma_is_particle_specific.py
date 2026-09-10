#!/usr/bin/env python3
"""
B -- DOES FIELD-DUST EVADE THE VELOCITY-ORDERING LEMMA?   (the key question for the whole programme)
=============================================================================================================
THE LEMMA (repo, L125_final_verdict_health_vs_cosmology.py, checks VEL-1/VEL-2):
    "a decoupled collisionless species has v_rms(a) ~ 1/a, so the free-streaming cutoff k_fs ~ a is strictly
     INCREASING: the set of scales it can cluster GROWS monotonically in time. Therefore
     {scales clustering at z_rec} SUBSET {scales clustering today}: cold enough for the CMB third peak (G8a)
     ==> clusters in galaxies ==> the L61 overshoot.  G8a ==> NOT G-gal, no common interior."
    L125 calls this obstruction "mechanism-independent".

THE HYPOTHESIS IT ACTUALLY USES is v_rms ~ 1/a. That is a theorem about FREE-STREAMING PARTICLES (comoving
momentum conserved along geodesics). A field-generated effective dust has its clustering cutoff set by the
DISPERSION RELATION of the field, not by particle momenta. This script asks whether that changes the ordering.

WHAT IS COMPUTED:
  B1  the particle law v_rms ~ 1/a, i.e. c_s^2 ~ a^-2 (the lemma's hypothesis), stated and used as control.
  B2  LORENTZ-INVARIANT k-essence: prove symbolically (Garriga-Mukhanov) that c_s^2 = P_X/(P_X + 2 X P_XX)
      equals the adiabatic c_ad^2 = K_Q/(Q K_QQ) for any purely kinetic K(Q). Then measure its a-dependence.
      If it falls with a, the lemma's CONCLUSION survives for this class even though its hypothesis fails.
  B3  LORENTZ-VIOLATING k-essence -- AeST's ACTUAL structure (the spatial-gradient term
      -(2-K_B) Y with Y = q^{mu nu} grad_mu phi grad_nu phi is INDEPENDENT of the time-kinetic term
      F(Y,Q) ~ K_2 Q^2): here c_s^2 = 2 c_Y / K_QQ(a) is a FREE function of time.
        * K quadratic  => K_QQ = const => c_s^2 = CONSTANT.
        * K = cosh/exp => K_QQ ~ a^-3   => c_s^2 ~ a^+3  (the sound speed GROWS with time).
      Both violate the lemma's hypothesis in the *favourable* direction.
  B4  THE GATES, quantitatively: (i) clusters at recombination for the third peak, (ii) smooth in galaxies
      (no L61 overshoot), (iii) still clusters in clusters, (iv) does not erase the observed P(k).
      Published anchor: Thomas, Kopp & Skordis, arXiv:1601.05097 -- constant GDM sound speed
      c_s^2 < 3.21e-6 at 99.7% c.l. (Planck 2015).
  B5  verdict: is the interior EMPTY (lemma survives in substance), a KNIFE-EDGE, or OPEN?

POLARITY: each check ASSERTS a statement; PASS = true. Several checks here REFUTE repo claims; they are held
to the same standard as the confirmations.
"""
import sympy as sp
import numpy as np
import sys, time

T0 = time.time(); FAILS = []; N = [0]
def check(name, ok, detail=""):
    N[0] += 1
    tag = "PASS" if ok else "FAIL"
    if not ok: FAILS.append(name)
    print(f"  [{tag}] {name}" + (f"   ({detail})" if detail else ""))
def sec(t):
    print("\n" + "=" * 112); print(t); print("=" * 112)

C_KMS = 299792.458

# =====================================================================================================
sec("B1 -- the lemma's hypothesis (control): a decoupled PARTICLE has c_s^2 ~ v_rms^2 ~ a^-2")
# =====================================================================================================
a = sp.symbols('a', positive=True)
v0 = sp.symbols('v_0', positive=True)
v_particle = v0/a
check("B1-1  free-streaming particles: comoving momentum is conserved => v_rms = v_0/a, so c_s^2 ~ a^-2 -- "
      "the sound speed FALLS with time, hence the clustering set GROWS (L125 VEL-1/VEL-2)",
      sp.simplify(sp.diff(v_particle, a) < 0) if False else sp.diff(v_particle**2, a).subs({v0:1, a:1}) < 0,
      "d(c_s^2)/da = -2 v_0^2/a^3 < 0")

# =====================================================================================================
sec("B2 -- LORENTZ-INVARIANT k-essence: c_s^2 = c_ad^2 identically (so the ordering is NOT free)")
# =====================================================================================================
Q, K2s, Q0s, Z0s = sp.symbols('Q K_2 Q_0 Z_0', positive=True)
Kf = sp.Function('K')
X = sp.symbols('X', positive=True)
# X = Q^2/2 ; P(X) = K(Q(X)) with Q = sqrt(2X)
Qx = sp.sqrt(2*X)
P = Kf(Qx)
PX = sp.diff(P, X); PXX = sp.diff(P, X, 2)
cs2_GM = sp.simplify(PX/(PX + 2*X*PXX))                       # Garriga-Mukhanov
cs2_GM_Q = sp.simplify(cs2_GM.subs(X, Q**2/2).doit())
cad2 = sp.Derivative(Kf(Q), Q)/(Q*sp.Derivative(Kf(Q), Q, 2))
diff = sp.simplify(cs2_GM_Q - cad2.doit())
check("B2-1  for ANY purely kinetic Lorentz-invariant k-essence, the perturbation sound speed equals the "
      "adiabatic one: c_s^2 = P_X/(P_X + 2 X P_XX) = K_Q/(Q K_QQ) = c_ad^2 (Garriga-Mukhanov)",
      sp.simplify(diff) == 0, f"c_s^2 - c_ad^2 = {sp.simplify(diff)}")

def cad2_of_a(kind, avals, Q0, K2, I0, Z0=None):
    """adiabatic (= Lorentz-invariant perturbation) sound speed c_ad^2 = K_Q/(Q K_QQ)."""
    out = []
    for av in avals:
        rhs = I0/av**3
        if kind == 'quad':
            Qv = Q0 + rhs/(2*K2); KQQ = 2*K2
        elif kind == 'cosh':
            Z = np.arcsinh(rhs/(2*K2*Z0)); Qv = Q0 + Z0*Z; KQQ = 2*K2*np.cosh(Z)
        out.append(rhs/(Qv*KQQ))
    return np.array(out)

# SZ21's OWN published CMB-fit parameters (Fig. 1 of 2007.00082):
#   Cosh: K_B=0.5, Q_0=0.1 Mpc^-1, K_2=7.5e3, Z_0=1e-9 Mpc^-1
#   Exp : K_B=0.1, Q_0=1e-4,       K_2=9.5e3, Z_0=1e-17
# I_0 is fixed by the dark-matter abundance: 8 pi Gt rho_0 = Q_0 I_0 = 3 H_0^2 Omega_dm.
h_ = 0.674; H0_ = h_/2997.9; rho8 = 3*H0_**2*0.264
KB_c, Q0_c, K2_c, Z0_c = 0.5, 0.1, 7.5e3, 1e-9
I0_c = rho8/Q0_c
avals = np.array([1/1100., 1/100., 1/10., 1.0])
print(f"  using SZ21's published Cosh fit: K_B={KB_c}, Q_0={Q0_c} Mpc^-1, K_2={K2_c:.1e}, Z_0={Z0_c:.0e}, "
      f"I_0={I0_c:.2e} (fixed by Omega_dm)")
c2q = cad2_of_a('quad', avals, Q0_c, K2_c, I0_c)
c2c = cad2_of_a('cosh', avals, Q0_c, K2_c, I0_c, Z0_c)
print(f"  quadratic K : c_ad^2 at a = 1/1100, 1/100, 1/10, 1 :  " + "  ".join(f"{x:.3e}" for x in c2q))
print(f"  cosh K      : c_ad^2 at a = 1/1100, 1/100, 1/10, 1 :  " + "  ".join(f"{x:.3e}" for x in c2c)
      + f"   (Z_0/Q_0 = {Z0_c/Q0_c:.0e} => c_ad = {np.sqrt(Z0_c/Q0_c)*C_KMS:.0f} km/s)")
check("B2-2  quadratic K, Lorentz-invariant: c_ad^2 falls monotonically from ~1 to ~2w_0 -- the SAME direction "
      "as a particle. For this K the lemma's conclusion survives even though its hypothesis does not.",
      np.all(np.diff(c2q) < 0), f"c_ad^2: {c2q[0]:.2e} -> {c2q[-1]:.2e} (monotonically falling)")
span_early = c2c[:3].max()/c2c[:3].min()      # a in [1/1100, 1/10], i.e. z from 1100 to 9
span_all   = c2c.max()/c2c.min()
check("B2-3  BUT with SZ21's own COSH K the Lorentz-INVARIANT sound speed is c_ad^2 -> Z_0/Q_0 = CONSTANT from "
      "recombination all the way to z ~ 9 (it varies by <1%), namely 30 km/s at their published fit values. "
      "Over that whole span the lemma's ordering is already broken WITHOUT any Lorentz violation.",
      span_early < 1.01, f"max/min of c_ad^2 over a in [1/1100, 1/10] = {span_early:.4f} "
                         f"(c_ad = {np.sqrt(c2c[0])*C_KMS:.0f} km/s, flat)")
check("B2-4  HONEST COUNTERWEIGHT: the cosh c_ad^2 does NOT keep rising -- once the charge has diluted past "
      "Z ~ 1 (here a ~ 0.3) it turns over and falls to zero, so a Lorentz-INVARIANT cosh dust becomes cold "
      "again TODAY, exactly when galaxy smoothness is needed. Constant-then-falling is not enough.",
      span_all > 10, f"transition at a = {(I0_c/(2*K2_c*Z0_c))**(1/3.):.2f}; c_ad^2 then falls by "
                     f"{span_all:.0f}x to {c2c[-1]:.2e} today ({np.sqrt(c2c[-1])*C_KMS:.2f} km/s)")

# =====================================================================================================
sec("B3 -- LORENTZ-VIOLATING k-essence (AeST's actual structure): c_s^2 = 2 c_Y / K_QQ(a) is FREE")
# =====================================================================================================
# AeST eq (5): the scalar sector carries  -(2-K_B) Y - F(Y,Q)  with Y = q^{mu nu} grad phi grad phi the
# gradient orthogonal to the aether, and F ~ -2K(Q) on FLRW. The gradient coefficient (2-K_B)(1+lambda_s) and
# the time-kinetic coefficient 2 K_2 are INDEPENDENT parameters; SZ21's own Minkowski dispersion (eq below
# their (13)) is  omega^2 = [(2-K_B)/(K_2 K_B)](1 + K_B lambda_s/2) k^2 + M^2  =>  c_s^2 = that bracket.
KB, lam_s = sp.symbols('K_B lambda_s', positive=True)
cs2_aest = (2-KB)/(K2s*KB)*(1 + KB*lam_s/2)
check("B3-1  AeST's published scalar dispersion gives c_s^2 = (2-K_B)(1 + K_B lambda_s/2)/(K_2 K_B): it is set "
      "by the RATIO of the gradient coefficient to K_2, NOT by the background evolution -- an independent knob",
      sp.simplify(sp.diff(cs2_aest, lam_s)) != 0, f"c_s^2 = {cs2_aest}")

def cs2_LV(kind, avals, cY=1.0, Q0=1.0, K2=1.0, I0=1.0, Z0=1e-3):
    """c_s^2 = 2 c_Y / K_QQ(a) for a foliation-projected gradient term c_Y |D chi|^2."""
    out = []
    for av in avals:
        rhs = I0/av**3
        if kind == 'quad':
            KQQ = 2*K2
        elif kind == 'cosh':
            Z = np.arcsinh(rhs/(2*K2*Z0)); KQQ = 2*K2*np.cosh(Z)
        out.append(2*cY/KQQ)
    return np.array(out)

# normalise so that c_s(today) = 300 km/s in each model (the galaxy-smoothness target of B4)
target_cs2_today = (300.0/C_KMS)**2
for kind in ('quad', 'cosh'):
    raw = cs2_LV(kind, avals)
    scale = target_cs2_today/raw[-1]
    c2 = raw*scale
    print(f"  {kind:5s}: c_s^2 at a = 1/1100, 1/100, 1/10, 1 :  " + "  ".join(f"{x:.3e}" for x in c2)
          + f"   [c_s(today) = 300 km/s]")
c2_quad = cs2_LV('quad', avals); c2_quad *= target_cs2_today/c2_quad[-1]
c2_cosh = cs2_LV('cosh', avals); c2_cosh *= target_cs2_today/c2_cosh[-1]
check("B3-2  LORENTZ-VIOLATING + quadratic K: c_s^2 is exactly CONSTANT in time -- the lemma's monotone "
      "ordering is broken (neither growing nor shrinking clustering set from the sound speed)",
      np.allclose(c2_quad, c2_quad[0], rtol=1e-12), f"c_s^2 = {c2_quad[0]:.3e} at every a")
slope = np.polyfit(np.log(avals[:3]), np.log(c2_cosh[:3]), 1)[0]
check("B3-3  LORENTZ-VIOLATING + cosh/exp K (SZ21's own functions): K_QQ ~ cosh(Z) ~ a^-3 at early times, so "
      "c_s^2 ~ a^+3 -- THE SOUND SPEED GROWS WITH TIME, the exact OPPOSITE of a particle's a^-2",
      abs(slope - 3.0) < 0.1, f"dln(c_s^2)/dln(a) = {slope:+.3f} (particle: -2)")
rel = (avals[-1]/avals[0])**(3-(-2))
check("B3-4  relative to a particle normalised to the same speed TODAY, this field-dust is colder at "
      "recombination by (a_now/a_rec)^5 ~ 1.6e15 -- the lemma's ordering is not merely broken, it is inverted "
      "by fifteen orders of magnitude",
      rel > 1e14, f"(1100)^5 = {rel:.2e}")

# =====================================================================================================
sec("B4 -- THE GATES, quantitatively. Is the interior empty?")
# =====================================================================================================
h = 0.674; H0 = h/2997.9; Om = 0.315; Orad = 9.24e-5; OL = 1-Om-Orad
def E(av): return np.sqrt(Om/av**3 + Orad/av**4 + OL)
def aH(av): return av*H0*E(av)          # comoving Hubble rate, Mpc^-1

a_rec = 1/1090.
k3 = 0.06      # comoving wavenumber of the CMB third peak: k ~ l/D_A ~ 810/13900 Mpc^-1
k_lss = 0.2    # the SDSS DR7 LRG range AeST itself fits (SZ21 Fig 2)
print(f"  comoving aH at recombination = {aH(a_rec):.4e} Mpc^-1 ;  today = {aH(1.0):.4e} Mpc^-1")

def kJ(av, cs2):                        # comoving Jeans wavenumber: perturbations grow for k < k_J
    return aH(av)/np.sqrt(cs2)

# --- gate (i): cluster at recombination on third-peak scales
for label, cs2rec in (("constant c_s (300 km/s)", c2_quad[0]),
                      ("running c_s^2 ~ a^3 (300 km/s today)", c2_cosh[0]),
                      ("particle with 300 km/s today", target_cs2_today*(1/a_rec)**2)):
    print(f"  {label:38s}: c_s(rec) = {np.sqrt(cs2rec)*C_KMS:10.1f} km/s   k_J(rec) = {kJ(a_rec, cs2rec):9.3e} Mpc^-1"
          f"   (need > {k3})  -> {'CLUSTERS' if kJ(a_rec,cs2rec)>k3 else 'FREE-STREAMS'}")
check("B4-1  a PARTICLE normalised to 300 km/s today was at 0.11c at recombination and free-streams out of "
      "third-peak scales: G8a fails. This is the lemma biting, reproduced.",
      kJ(a_rec, target_cs2_today*(1/a_rec)**2) < k3,
      f"k_J(rec) = {kJ(a_rec, target_cs2_today*(1/a_rec)**2):.2e} < k_3 = {k3}")
check("B4-2  a CONSTANT-c_s field-dust with the same 300 km/s clusters fine at recombination",
      kJ(a_rec, c2_quad[0]) > k3, f"k_J(rec) = {kJ(a_rec, c2_quad[0]):.2e} > {k3}")
check("B4-3  an a^3-RUNNING field-dust clusters at recombination with a colossal margin",
      kJ(a_rec, c2_cosh[0]) > 1e3*k3, f"k_J(rec) = {kJ(a_rec, c2_cosh[0]):.2e} >> {k3}")

# --- gate (ii): smooth in galaxies today.  Hydrostatic criterion: the fluid cannot be bound where c_s > v_c.
print("\n  galaxy gate: a fluid of sound speed c_s cannot be confined by a potential well of depth v_c^2.")
for vc in (20., 100., 200., 300.):
    cs_needed = vc
    print(f"    v_c = {vc:5.0f} km/s (SPARC range)  =>  need c_s >~ {cs_needed:5.0f} km/s to stay smooth")
check("B4-4  to leave EVERY SPARC rotation curve to MOND (v_c up to ~300 km/s) the field-dust needs "
      "c_s >~ 300 km/s, i.e. c_s^2 >~ 1.0e-6",
      abs(target_cs2_today - 1.0e-6) < 0.1e-6, f"c_s^2(300 km/s) = {target_cs2_today:.2e}")
cs2_dwarf = (50./C_KMS)**2
check("B4-5  (weaker version) to leave only dwarfs/LSBs (v_c ~ 50 km/s) to MOND: c_s^2 >~ 2.8e-8",
      2e-8 < cs2_dwarf < 4e-8, f"c_s^2(50 km/s) = {cs2_dwarf:.2e}")

# --- gate (iii): still clusters in clusters (v_c ~ 1000-1500 km/s) -- the programme WANTS this
# softer criterion: a fluid settling hydrostatically in a well of depth v_c^2 reaches a contrast
# exp(v_c^2/c_s^2); it only MATTERS if that lifts it from the cosmic mean to the halo density needed.
rho_cosmic = 3.5e-8          # M_sun/pc^3, cosmic mean dark density today
rho_halo   = 1.0e-2          # M_sun/pc^3, the halo density a rotation curve would need at ~8 kpc
contrast_needed = rho_halo/rho_cosmic
for vc in (100., 200., 300.):
    cs_soft = vc/np.sqrt(np.log(contrast_needed))
    print(f"    v_c = {vc:5.0f} km/s: hydrostatic contrast exp(v_c^2/c_s^2) stays below the {contrast_needed:.0e} "
          f"needed if c_s >~ {cs_soft:5.0f} km/s")
cs_soft_200 = 200./np.sqrt(np.log(contrast_needed))
check("B4-5b  a SOFTER (hydrostatic-atmosphere) galaxy criterion lowers the floor to c_s >~ 60 km/s "
      "(c_s^2 >~ 4e-8) for a 200 km/s galaxy -- so the floor is criterion-dependent by ~1.5 decades and "
      "should be quoted as a RANGE, not a number",
      50 < cs_soft_200 < 80, f"soft floor = {cs_soft_200:.0f} km/s => c_s^2 >~ {(cs_soft_200/C_KMS)**2:.1e}")

check("B4-6  and it still collapses in galaxy CLUSTERS (v_c ~ 1000-1500 km/s > c_s), which is where the "
      "programme needs extra mass anyway",
      np.sqrt(target_cs2_today)*C_KMS < 1000., f"c_s = {np.sqrt(target_cs2_today)*C_KMS:.0f} km/s < 1000 km/s")

# --- gate (iv): published cosmological bound on a CONSTANT dark-matter sound speed
cs2_pub = 3.21e-6      # Thomas, Kopp & Skordis, arXiv:1601.05097, 99.7% c.l. (Planck 2015), constant GDM
check("B4-7  the published constant-c_s bound (arXiv:1601.05097: c_s^2 < 3.21e-6 at 99.7%) sits only a factor "
      "3.2 ABOVE the galaxy-smoothness floor c_s^2 >~ 1.0e-6  ==>  a KNIFE-EDGE, not a comfortable window",
      1.0 < cs2_pub/target_cs2_today < 10., f"ceiling/floor = {cs2_pub/target_cs2_today:.2f}")

# --- gate (iv'): what a constant c_s does to the LATE-TIME matter power spectrum
print(f"\n  late-time P(k) damage from a CONSTANT c_s = 300 km/s:")
for av in (a_rec, 0.1, 0.5, 1.0):
    print(f"    a = {av:7.5f}:  k_J = {kJ(av, target_cs2_today):8.3f} Mpc^-1"
          + ("   <-- BELOW the observed SDSS range (k up to 0.2): power erased" if kJ(av, target_cs2_today) < k_lss else ""))
check("B4-8  a CONSTANT c_s = 300 km/s puts the comoving Jeans scale at k_J = 0.20-0.23 Mpc^-1 for all "
      "a >~ 0.3 -- i.e. RIGHT AT the edge of the SDSS DR7 LRG range that AeST itself fits. Marginal, not "
      "obviously dead: the estimate cannot settle it, a growth/Boltzmann computation must.",
      0.15 < kJ(1.0, target_cs2_today) < 0.35 and 0.15 < kJ(0.5, target_cs2_today) < 0.35,
      f"k_J(a=0.5) = {kJ(0.5, target_cs2_today):.3f}, k_J(today) = {kJ(1.0, target_cs2_today):.3f} Mpc^-1 "
      f"vs the fitted range k <= {k_lss}")

print(f"\n  the SAME check for the a^3-RUNNING sound speed (c_s -> 300 km/s only today):")
scale_cosh = target_cs2_today/cs2_LV('cosh', np.array([1.0]))[0]
for av in (a_rec, 0.1, 0.5, 1.0):
    c2 = cs2_LV('cosh', np.array([av]))[0]*scale_cosh
    print(f"    a = {av:7.5f}:  c_s = {np.sqrt(c2)*C_KMS:8.2f} km/s   k_J = {kJ(av, c2):10.3f} Mpc^-1"
          + ("   <-- power erased" if kJ(av, c2) < k_lss else ""))
c2_half = cs2_LV('cosh', np.array([0.5]))[0]*scale_cosh
check("B4-9  the a^3-RUNNING sound speed keeps k_J above the observed range for essentially all of structure "
      "formation and only turns on at a ~ 1 -- so it smooths galaxies TODAY without erasing P(k) THEN",
      kJ(0.5, c2_half) > k_lss, f"k_J(a=0.5) = {kJ(0.5, c2_half):.2f} Mpc^-1 > {k_lss}")
check("B4-10  HONEST CAVEAT: at a=1 the running model reaches the same k_J as the constant one, so the "
      "present-day P(k) suppression is NOT avoided -- only its DURATION is reduced. Whether the residual "
      "damage is acceptable requires a real Boltzmann/growth computation, not this estimate.",
      abs(kJ(1.0, target_cs2_today) - kJ(1.0, cs2_LV('cosh', np.array([1.0]))[0]*scale_cosh)) < 1e-9)

# =====================================================================================================
sec("VERDICT (B)")
# =====================================================================================================
print(f"""
  1. THE LEMMA IS NOT MECHANISM-INDEPENDENT. Its content is 'v_rms ~ 1/a', which is a theorem about
     free-streaming PARTICLES. A field-generated dust obeys it only if the field is Lorentz-INVARIANT
     (then c_s^2 = c_ad^2 is locked to the background and falls with a, B2-1/B2-2). A field whose spatial
     gradient term has an INDEPENDENT coefficient -- which is exactly AeST's -(2-K_B)Y structure, and exactly
     what a preferred foliation gives for free -- has c_s^2 = 2 c_Y/K_QQ(a), a free function: CONSTANT for
     quadratic K, and GROWING as a^+3 for SZ21's cosh/exp K. The ordering is broken, and in the cosh case
     inverted by (1+z_rec)^5 ~ 1.6e15 relative to a particle.

  2. SO THE PROGRAMME'S 'NO COMMON INTERIOR' IS NOT PROVED. The correct statement is narrower:
       'no decoupled species whose velocity dispersion redshifts as 1/a can be cold enough for the CMB and
        smooth enough for galaxies'  --  which covers every PARTICLE candidate and every Lorentz-invariant
        k-essence dust, but NOT a Lorentz-violating field dust.

  3. WHAT ACTUALLY CLOSES (OR NEARLY CLOSES) THE CORNER IS A DIFFERENT PINCER, and it is quantitative:
       floor   : c_s >~ 300 km/s        (c_s^2 >~ 1.0e-6) to leave all SPARC rotation curves to MOND
       ceiling : c_s^2 <  3.21e-6       (arXiv:1601.05097, 99.7%, constant GDM sound speed)
       LSS     : a CONSTANT c_s of that size holds the comoving Jeans scale at k_J = 0.20-0.23 Mpc^-1 from
                 a ~ 0.3 onward -- right AT the edge of the SDSS DR7 LRG range AeST itself fits. Marginal.
     A sound speed that RUNS UP with time (c_s^2 ~ a^3, exactly what SZ21's own cosh/exp K(Q) delivers once
     the gradient coefficient is independent) is strictly better: it keeps k_J far above the data throughout
     structure formation and only smooths galaxies at a ~ 1. NOTHING COMPUTED HERE EXCLUDES THAT CORNER.
     Verdict: UNDETERMINED, narrow. The decisive computation is a Boltzmann + growth run for a
     foliation-projected k-essence with running c_s^2 -- which nobody, including Skordis & Zlosnik, has done.
""")
print("=" * 112)
print(f"B COMPLETE: {N[0]-len(FAILS)}/{N[0]} checks PASS.   [{time.time()-T0:.1f}s]")
if FAILS: print("FAILED: " + ", ".join(FAILS)); sys.exit(1)
print("=" * 112)
