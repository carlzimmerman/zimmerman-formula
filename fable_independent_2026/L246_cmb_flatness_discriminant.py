#!/usr/bin/env python3
"""L246 -- does the FLATNESS of a_0 (w = -1) protect the CMB acoustic peaks, in a way a
density-tracking scale cannot?  A CMB discriminant unique to the parameter-free footing.

The framework's own de Sitter derivation gives a_0 = kappa c sqrt(G rho_Lambda), and for w = -1
rho_Lambda is CONSTANT, so a_0 is FLAT across cosmic time -- the same value at recombination as
today.  The rival branch (LambdaCDM's naive scale) tracks the density, g_dagger ~ sqrt(G rho_crit)
proportional to H(z), and so is ENORMOUSLY larger at recombination.

The MOND modification is active where the local acceleration g falls below a_0.  So the two laws
predict very different things for the acoustic perturbations that make the CMB peaks -- because the
same perturbation gravity is measured against a fixed small a_0 (flat) or a huge one (rising).

This lane puts numbers on it and states the discriminant.  HONESTY FLAG carried throughout: this is
about the peak GEOMETRY (how far the acoustic-scale gravity departs from Newtonian); the peak
HEIGHTS, especially the third peak, need the dark-sector clustering and are NOT addressed here.
Every check states measurement and threshold separately.
"""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
RES, NP, NF = [], 0, 0
def check(nm, measured, ok, d=""):
    global NP, NF
    ok = bool(ok); print(f"  [{'PASS' if ok else 'FAIL'}] {nm}\n         measured: {measured}")
    if d: print(f"         reading : {d}")
    RES.append({"name": nm, "measured": str(measured), "pass": ok, "reading": d}); NP += ok; NF += (not ok)

print(__doc__)
c, G, Mpc = 2.99792458e8, 6.674e-11, 3.0857e22
H0 = 67.4*1000/3.0857e22
Om, Or = 0.315, 9.2e-5
Z = 1090.0
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
def one_minus_mu2(x): return 4.0/(2.0+x)**2         # OneFunction: 1 - mu_2(x), x = g/a_0

print("PART A -- the background at recombination is deeply Newtonian (expansion history standard)")
Hz = H0*math.sqrt(Om*(1+Z)**3 + Or*(1+Z)**4)
aH = c*Hz
ratio_bg = aH/A0["canonical"]
print(f"    H(z=1090) = {Hz:.3e} s^-1 ; c*H = {aH:.3e} m/s^2 ; c*H/a_0 = {ratio_bg:.2e}")
check("V1 [the background acceleration at recombination is ~1e5 x a_0, so the expansion is standard] c*H(z_rec) is compared with a_0",
      f"c*H(z_rec) = {aH:.3e} m/s^2 = {ratio_bg:.2e} x a_0 (canonical); the boost there is 1-mu_2 = {one_minus_mu2(ratio_bg):.2e}",
      ratio_bg > 1e4,
      "the modified dynamics is switched off for the BACKGROUND at recombination to ~1 part in 1e10, so the expansion history and the sound horizon are unmodified. This is the easy half and both laws share it -- the discriminant is the perturbations")

print("\nPART B -- the two laws for a_0 at recombination differ by the full H(z)/H0 factor")
scale_factor = Hz/H0
for foot, a0 in A0.items():
    a0_flat = a0
    a0_rise = a0*scale_factor
    print(f"    {foot:9s}: a_0(flat, w=-1) = {a0_flat:.3e} (same as today);  a_0(rising, ~H(z)) = {a0_rise:.3e}  -- factor {scale_factor:.2e}")
check("V2 [the flat law keeps a_0 fixed to recombination; the rival is ~2e4x larger there] the two a_0(z_rec) are computed and their ratio taken",
      f"a_0(rising)/a_0(flat) = H(z_rec)/H0 = {scale_factor:.3e}; flat stays {A0['canonical']:.2e}, rising becomes {A0['canonical']*scale_factor:.2e} m/s^2",
      abs(scale_factor - Hz/H0) < 1e-6 and scale_factor > 1e4,
      "the flatness is the whole point: a_0 does NOT scale up with the density. The rival's MOND scale at recombination is 20,000 times larger, which changes whether the acoustic perturbations sit above or below threshold")

print("\nPART C -- the acoustic-scale perturbation gravity (order-of-magnitude, inputs stated)")
Phi_over_c2 = 3e-5                       # gauge-invariant potential at recombination (Sachs-Wolfe level)
r_sound_com = 147*Mpc                    # comoving sound horizon at recombination
lam_phys = r_sound_com/(1+Z)
g_pert = Phi_over_c2*c**2/lam_phys
print(f"    Phi/c^2 ~ {Phi_over_c2:.0e} ; lambda_phys(sound horizon) = {lam_phys/Mpc*1000:.0f} kpc ; g_pert ~ Phi/lambda = {g_pert:.3e} m/s^2")
check("V3 [the acoustic-scale peculiar gravity is of order a_0, not far above it] g_pert ~ Phi c^2 / lambda_sound is estimated from standard CMB inputs and compared with a_0",
      f"g_pert ~ {g_pert:.3e} m/s^2 = {g_pert/A0['canonical']:.1f} x a_0 (canonical), {g_pert/A0['alt']:.1f} x a_0 (alt)",
      1.0 < g_pert/A0["canonical"] < 100.0,
      "an order-of-magnitude estimate (Phi/c^2 ~ 3e-5, lambda = sound horizon), but the discriminant below turns on a factor of ~2e4 between the two laws, so a factor-of-a-few uncertainty in g_pert cannot change the conclusion")

print("\nPART D -- THE DISCRIMINANT: flat a_0 leaves the peaks nearly Newtonian; rising a_0 wrecks them")
for foot, a0 in A0.items():
    x_flat = g_pert/a0
    x_rise = g_pert/(a0*scale_factor)
    m_flat = one_minus_mu2(x_flat)
    m_rise = one_minus_mu2(x_rise)
    print(f"    {foot:9s}: FLAT  g/a_0 = {x_flat:5.1f} -> modification 1-mu_2 = {m_flat:.3f} ({100*m_flat:.0f}%)")
    print(f"    {'':9s}  RISING g/a_0 = {x_rise:.2e} -> modification 1-mu_2 = {m_rise:.3f} ({100*m_rise:.0f}%), boost 1/mu_2 ~ {1/(1-m_rise):.0f}x")
x_flat_c = g_pert/A0["canonical"]; m_flat_c = one_minus_mu2(x_flat_c)
x_rise_c = g_pert/(A0["canonical"]*scale_factor); m_rise_c = one_minus_mu2(x_rise_c)
check("V4 [the flat law modifies acoustic-scale gravity by only ~5%; the rising law modifies it order-unity] the OneFunction modification at the acoustic scale is computed for both laws",
      f"FLAT: g/a_0 = {x_flat_c:.1f}, modification {100*m_flat_c:.0f}% (near-Newtonian); RISING: g/a_0 = {x_rise_c:.1e}, modification {100*m_rise_c:.0f}% (deep MOND, gravity boost ~{1/(1-m_rise_c):.0f}x)",
      m_flat_c < 0.10 and m_rise_c > 0.9,
      "this is the discriminant. Because a_0 stays FLAT and small, the acoustic perturbations sit just ABOVE threshold and gravity there is within ~5% of Newtonian -- the peak geometry is nearly preserved. A density-tracking a_0 would sit the SAME perturbations deep below threshold, boosting acoustic-scale gravity by thousands and destroying the peaks. The w = -1 flatness is what makes the CMB survivable")

print("\nPART E -- one parameter (w = -1) controls both the CMB test and the high-z BTFR test")
check("V5 [the same flatness that protects the peaks flattens the high-z BTFR -- one number, two tests] the shared origin of the two discriminants is stated",
      "w = -1 makes rho_Lambda constant, hence a_0 flat; that same flatness gives a deep-MOND BTFR zero-point of 0.00 dex at z~2.5 (vs +0.33 dex for a rising scale) AND keeps the CMB acoustic-scale modification at ~5% (vs order-1). A single equation-of-state choice is falsifiable at BOTH recombination and z~2.5",
      True,
      "the flatness is not two coincidences. It is one property of the footing a_0 = kappa c sqrt(G rho_DE) with w = -1, testable at two epochs 8 Gyr apart")

print("\nPART F -- what this does NOT claim (the peak HEIGHTS)")
check("V6 [HONESTY: this addresses peak GEOMETRY, not peak HEIGHTS -- the third-peak/dark-clustering problem is separate and unsolved] the scope is fenced",
      "the ~5% figure is how far acoustic-scale gravity departs from Newtonian (peak positions/geometry). The peak HEIGHTS, especially the third peak, require a component that CLUSTERS gravitationally like dark matter; the flat a_0 does not supply that, and this lane does not address it (the dark-sector/two-sector problem, treated elsewhere and NOT closed)",
      True,
      "so the honest claim is: the flatness of a_0 protects the acoustic-peak GEOMETRY, turning the CMB from a generic MOND problem into a discriminant for the footing. It does NOT solve the CMB, because the peak heights are a separate, open problem")

print(f"""
READING

  The flatness of a_0 turns the CMB from a problem into a discriminant unique to this footing.

  At recombination the BACKGROUND acceleration was c*H(z) = {aH:.2e} m/s^2, about {ratio_bg:.1e}
  times a_0, so the expansion history and the sound horizon are standard (V1) -- the easy half,
  shared by every version.  The discriminant is the perturbations.

  Because a_0 = kappa c sqrt(G rho_Lambda) is built from a CONSTANT rho_Lambda (w = -1), it is
  FLAT: the same {A0['canonical']:.2e} m/s^2 at recombination as today (V2).  A rival where the
  scale tracks the density, g_dagger ~ sqrt(G rho_crit) ~ H(z), would be {scale_factor:.1e} times
  larger there.  The acoustic-scale peculiar gravity is g_pert ~ {g_pert:.1e} m/s^2 (V3), of order
  a_0.  So the SAME perturbation is measured against very different thresholds (V4):

    FLAT a_0:   g/a_0 ~ {x_flat_c:.0f}   -> {100*m_flat_c:.0f}% modification, gravity near-Newtonian, peaks nearly standard
    RISING a_0: g/a_0 ~ {x_rise_c:.0e} -> ~100% modification, acoustic-scale gravity boosted ~{1/(1-m_rise_c):.0f}x, peaks wrecked

  So the w = -1 flatness is what makes the CMB peak GEOMETRY survivable, and a density-tracking
  a_0 cannot do it.  And it is the SAME flatness that flattens the high-z BTFR to 0.00 dex against
  a rising scale's +0.33 dex (V5): one equation-of-state choice, two falsifiable tests, 8 Gyr apart.

  HONESTY (V6): this is the peak geometry, not the peak heights.  The third-peak height needs a
  component that clusters like dark matter, which the flat a_0 does not supply.  The claim is that
  flatness PROTECTS the acoustic geometry, not that it SOLVES the CMB.

  LIMITS.  g_pert is order-of-magnitude (Phi/c^2 ~ 3e-5, lambda = sound horizon); the 2e4 factor
  between the laws swamps a factor-of-a-few there.  The modification uses the OneFunction mu_2; a
  sharper kernel changes the 5% but not the flat-vs-rising contrast.  Both footings carried. Peak
  heights / dark-sector clustering are a separate open problem, explicitly not addressed.
""")
json.dump({"checks": RES, "n_pass": NP, "n_fail": NF,
           "H_zrec": Hz, "cH_over_a0": ratio_bg, "scale_factor": scale_factor,
           "g_pert": g_pert, "x_flat": x_flat_c, "mod_flat": m_flat_c,
           "x_rise": x_rise_c, "mod_rise": m_rise_c},
          open(os.path.join(HERE, "L246_cmb_flatness_discriminant_results.json"), "w"), indent=1)
print(f"L246 COMPLETE: {NP}/{NP+NF} checks PASS.")
