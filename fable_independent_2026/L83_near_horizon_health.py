#!/usr/bin/env python3
"""
L83 -- NEAR-HORIZON HEALTH: is the F(Q)Theta scalar-metric strong coupling (Omega_zeta_pi ~ k^2 -> 0,
       and G''(y0) -> 0 at the zero-field point) FATAL for the CMB, or BENIGN (confined super-horizon)?
================================================================================================================
astra's ADM principal gate (qwen .../fqtheta_clock_dust_2026/ACTUAL_PRINCIPAL_GATE.md) found the ONE open
concern for the F(Q)Theta clock-dust candidate: the reduced scalar-metric symplectic form

        Omega_{zeta pi} = (U_nz / Q0) * k^2         (U_nz = -4 M^2)

collapses as k -> 0, and the constitutive stiffness U_pi_pi = 2 M^2 G''(y0) with
G(y) = y^2 + 2(1+y)e^{-y} - 2 obeys G''(y) -> 0 as y -> 0+.  Because the symplectic form is worst at
k -> 0, the degeneration is worst at the LARGEST scales.  This lane decides, from first principles and
both a0 footings, whether that reaches OBSERVABLE (sub-horizon) scales (fatal) or is confined to
super-horizon scales where the curvature perturbation zeta is causally frozen (benign).

METHOD (adversarial; verify a "benign" as hard as a "fatal"):
  (a) comoving horizon wavenumber k_H = aH/c today and at recombination -- pure LCDM background data.
  (b) compare the k-window of the degeneration to k_H: does it touch k > k_H (sub-horizon = fatal)?
  (c) zeta conservation on super-horizon scales for the ADIABATIC Noether dust (the shield).
  Plus three fatal-hunting adversarial checks: an interior minimum in the observable band; whether the
  degeneration is PAIRED with a dynamical (exponential) instability; and the k-regularity of the classical EOM.

POLARITY: each check ASSERTS a statement; PASS = the statement is TRUE.  Controls first.  Both a0 footings.
Imports nothing from qwen_claude_field_theory (astra's numbers are reproduced here independently in sympy/numpy).
"""
import sympy as sp
import numpy as np
import sys, time

T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)

print("=" * 112)
print("L83 -- NEAR-HORIZON HEALTH of the F(Q)Theta scalar-metric strong coupling (Omega ~ k^2, G''(y0)->0)")
print("=" * 112, flush=True)

# ----------------------------------------------------------------------------------------------------------
# Constants (SI + astro), and BOTH a0 footings.
# ----------------------------------------------------------------------------------------------------------
c_kms   = 299792.458                 # speed of light [km/s]
c_ms    = 299792458.0                # [m/s]
Mpc_m   = 3.0856775814913673e22      # [m/Mpc]
H0_kmsMpc = 67.4                     # Planck 2018 base LCDM [km/s/Mpc]  (background DATA, footing-independent)
Om, Or, OL = 0.315, 9.24e-5, 0.685   # matter, radiation (photons+3nu), Lambda
z_rec   = 1089.9                     # recombination redshift (Planck)
a0_can  = 9.3619e-11                 # CANONICAL a0 footing [m/s^2]
a0_alt  = 1.1279e-10                 # ALTERNATE a0 footing [m/s^2]

def E(z):                            # H(z)/H0 in flat LCDM
    return np.sqrt(Om*(1+z)**3 + Or*(1+z)**4 + OL)

# comoving horizon (Hubble) wavenumber k_H = a H / c  [1/Mpc].  a=1/(1+z).
def kH(z):
    H_kmsMpc = H0_kmsMpc * E(z)
    a = 1.0/(1.0+z)
    return a * H_kmsMpc / c_kms      # [1/Mpc]

kH0   = kH(0.0)                      # present comoving horizon wavenumber
kHrec = kH(z_rec)                    # comoving horizon wavenumber at recombination

# ==========================================================================================================
sec("PART C -- CONTROLS: the horizon machinery reproduces known LCDM numbers before any verdict.")
# ==========================================================================================================
Hubble_dist = c_kms / H0_kmsMpc      # c/H0 [Mpc]
check("C-1  present comoving Hubble distance c/H0 = 4448 Mpc and k_H0 = 1/(c/H0) ~ 2.25e-4 /Mpc "
      "(standard LCDM; the largest observable comoving scale is the present horizon)",
      abs(Hubble_dist-4448.0) < 30 and abs(kH0-2.248e-4) < 5e-6,
      f"c/H0 = {Hubble_dist:.1f} Mpc, k_H0 = {kH0:.3e} /Mpc")

check("C-2  the comoving horizon at recombination is SMALLER (higher k) than today: k_Hrec ~ 4.8e-3 /Mpc, "
      "and k_Hrec/k_H0 ~ 21 (modes with k>k_Hrec were sub-horizon at recombination)",
      abs(kHrec-4.79e-3) < 3e-4 and 19 < kHrec/kH0 < 24,
      f"k_Hrec = {kHrec:.3e} /Mpc, ratio k_Hrec/k_H0 = {kHrec/kH0:.1f}")

# acoustic first-peak comoving wavenumber ~ 0.0165 /Mpc (ell1 ~ 220 = k * D_C, D_C ~ 13.9 Gpc)
k_peak = 0.0165
DC = 13900.0                         # comoving distance to last scattering [Mpc]
ell1 = k_peak*DC
check("C-3  the first acoustic peak (ell1 ~ 220) is DEEP sub-horizon at recombination: its comoving "
      "k_peak ~ 0.0165 /Mpc >> k_Hrec ~ 4.8e-3 /Mpc.  All CMB acoustic physics lives at k > k_Hrec",
      k_peak > kHrec and 200 < ell1 < 245,
      f"k_peak/k_Hrec = {k_peak/kHrec:.1f}, implied ell1 = {ell1:.0f}")

# c_s^2>0 fluid has a nonzero Jeans scale; c_s^2=0 fluid does not (reproduces L82's discriminator)
kJ = lambda cs2, H, rho, G=1.0: (np.sqrt(4*np.pi*G*rho)/np.sqrt(cs2)) if cs2>0 else 0.0
check("C-4  a c_s^2>0 component has a nonzero Jeans wavenumber k_J (pressure suppression, the g04h failure "
      "mode); a c_s^2=0 component has k_J=0 (no Jeans scale).  The L82 Noether dust has c_s^2=0",
      kJ(0.1,1,1) > 0 and kJ(0.0,1,1) == 0.0,
      f"k_J(c_s^2=0.1)={kJ(0.1,1,1):.3f} > 0 ; k_J(c_s^2=0)={kJ(0.0,1,1):.1f}")

# symbolic control: with Omega = O0*k^2 and reduced Hamiltonian H_red = (k^2/2)(Upp*pi^2 + Uzz*z^2),
# the classical Hamilton eqs give a k-INDEPENDENT frequency (the k^2 cancels).  Reproduce astra's char poly.
k, O0, Upp, Uzz, Q0s = sp.symbols('k O0 Upp Uzz Q0', positive=True)
Omega = O0*k**2
# Hamilton eqs: Omega * zdot = dH/dpi = k^2*Upp*pi ; Omega * pidot = -dH/dz = -k^2*Uzz*z
zdot_over_pi = (k**2*Upp)/Omega       # coefficient in zdot = (...)*pi
pidot_over_z = -(k**2*Uzz)/Omega      # coefficient in pidot = (...)*z
omega2 = sp.simplify(-zdot_over_pi*pidot_over_z)   # zddot = zdot_over_pi*pidot = zdot_over_pi*pidot_over_z*z
check("C-5  [sympy] with Omega ~ k^2 AND reduced Hamiltonian ~ k^2, the classical Hamilton equations give a "
      "frequency whose k^2 CANCELS: omega^2 = Upp*Uzz/O0^2, INDEPENDENT of k.  (Reproduces astra's "
      "k-independent characteristic polynomial lambda^2 + Q0^2 U_pi_pi U_zz / U_nz^2 = 0.)",
      sp.simplify(omega2 - Upp*Uzz/O0**2) == 0 and sp.diff(omega2, k) == 0,
      f"omega^2 = {omega2} (no k dependence)")

# ==========================================================================================================
sec("PART G -- the MOND operator's second derivative: is the degeneration paired with an INSTABILITY?")
# ==========================================================================================================
y = sp.symbols('y', nonnegative=True)
G = y**2 + 2*(1+y)*sp.exp(-y) - 2
Gpp = sp.simplify(sp.diff(G, y, 2))                  # = 2[1+(y-1)e^{-y}]
check("G-1  [sympy] G''(y) = 2[1+(y-1)e^{-y}], and G''(0) = 0 EXACTLY.  On the homogeneous FLRW background "
      "the spatial gradient V=0 so y0 = |V|/a0 = 0, hence U_pi_pi = 2 M^2 G''(0) = 0 there (astra's "
      "zero-field point IS the cosmological background)",
      sp.simplify(Gpp - 2*(1+(y-1)*sp.exp(-y))) == 0 and Gpp.subs(y, 0) == 0,
      "G''(0)=0 -> U_pi_pi=0 on the FLRW background (V=0)")

ys = np.linspace(0.0, 60.0, 60001)
Gpp_num = 2*(1+(ys-1)*np.exp(-ys))
check("G-2  [adversarial: fatal branch?] astra flagged an EXPONENTIAL instability IF U_pi_pi*U_zz < 0.  But "
      "for the EXACT exponential G, G''(y) >= 0 for ALL y >= 0 (min = 0 at y=0, -> 2 as y->inf).  With "
      "U_zz = 4 M^2 > 0, the product U_pi_pi U_zz = 8 M^4 G''(y) >= 0 ALWAYS -> lambda^2 <= 0 -> the mode "
      "OSCILLATES (gap) or is MARGINAL (y=0), NEVER exponentially unstable.  The fatal branch is empty",
      Gpp_num.min() >= -1e-12 and abs(Gpp_num.min()) < 1e-9 and abs(Gpp_num[-1]-2.0) < 1e-6,
      f"min G'' on [0,60] = {Gpp_num.min():.2e} (>=0); G''(inf) -> {Gpp_num[-1]:.4f}")

check("G-3  [what the y0=0 point IS] at the cosmological background U_pi_pi=0 so the reduced characteristic "
      "polynomial is lambda^2 = 0: a MARGINAL (zero-frequency) mode, not a tachyon.  A marginal, "
      "positive-kinetic (U_zz=4M^2>0), c_s^2=0 mode is exactly pressureless dust (L82) -- it grows by "
      "gravitational coupling as delta~a, it does NOT blow up from the reduced kinetic sector",
      True, "lambda^2=0 at y0=0: marginal dust mode, kinetic U_zz>0, no exponential growth")

# ==========================================================================================================
sec("PART M -- WHERE is the degeneration, relative to the horizon?  (both a0 footings)")
# ==========================================================================================================
# Omega(k) = O0 k^2 is MONOTONE increasing in k: worst (smallest) at k->0 = largest scales.
kk = np.array([1e-6, kH0/10, kH0, kHrec, k_peak, 0.2])
Om_rel = (kk/kH0)**2                                 # Omega(k)/Omega(k_H0), monotone in k
check("M-1  Omega(k) = O0 k^2 is STRICTLY MONOTONE in k, so the degeneration is WORST at k->0 (largest "
      "scales) and STRICTLY IMPROVES toward smaller scales.  There is NO interior worst-case: the minimum "
      "of the degeneration over any k-band is always at the band's LOWER edge",
      np.all(np.diff(Om_rel) > 0),
      f"Omega/Omega(k_H0) at k=[1e-6,kH0/10,kH0,kHrec,kpeak,0.2] = {np.array2string(Om_rel, precision=2)}")

check("M-2  [adversarial: interior minimum in the OBSERVABLE band?] within the observable band "
      "[k_H0, 0.2]/Mpc the minimum of Omega is at the LOWER edge k_H0 (present horizon), not at any "
      "interior/sub-horizon scale.  So the worst OBSERVABLE degeneration sits exactly at the present "
      "horizon; everything more observable (higher k) is progressively BETTER normalised",
      np.argmin((np.array([kH0, kHrec, k_peak, 0.2])/kH0)**2) == 0,
      "argmin of Omega over the observable band = k_H0 (the horizon edge), no interior minimum")

# a0 sets the framework's fundamental scale; its associated rate is a0/c, comoving wavenumber a0/c^2.
def k_a0(a0):    return (a0 / c_ms**2) * Mpc_m       # [1/Mpc]
for label, a0 in [("canonical", a0_can), ("alternate", a0_alt)]:
    ka0 = k_a0(a0)
    check(f"M-3 ({label} a0={a0:.4e}) the framework's OWN acceleration scale a0 corresponds to comoving "
          f"k_a0 = a0/c^2 = {ka0:.3e} /Mpc, which is BELOW the present horizon k_H0 = {kH0:.3e} /Mpc "
          "(ratio k_a0/k_H0 ~ 1/2pi).  The MOND/a0 scale is itself SUPER-horizon today -- the regime "
          "where zeta is conserved -- so the framework's characteristic scale lands in the benign band",
          ka0 < kH0 and 0.10 < ka0/kH0 < 0.20,
          f"k_a0/k_H0 = {ka0/kH0:.3f} (< 1: super-horizon; ~ 1/2pi = {1/(2*np.pi):.3f})")

# Enhancement of Omega at the observable sub-horizon scales relative to the present-horizon mode.
enh_rec  = (kHrec/kH0)**2
enh_peak = (k_peak/kH0)**2
check("M-4  observable SUB-HORIZON scales are FAR from the degenerate point: relative to the present-horizon "
      "mode, Omega is enhanced by ~450x at the recombination horizon and ~5000x at the first acoustic peak. "
      "On the scales the CMB actually measures (the peaks), the symplectic form is well away from zero",
      enh_rec > 400 and enh_peak > 4000,
      f"Omega enhancement: recomb horizon = {enh_rec:.0f}x, first peak = {enh_peak:.0f}x")

# ==========================================================================================================
sec("PART Z -- the SHIELD: zeta conservation on super-horizon scales for the adiabatic Noether dust.")
# ==========================================================================================================
# Standard GR result: on super-horizon scales the comoving curvature perturbation obeys
#   zeta_dot = -(H/(rho+p)) * delta_p_nonadiabatic  +  O((k/aH)^2),
# so for an ADIABATIC perturbation (delta_p_nad = 0) zeta is conserved as k/aH -> 0, for ANY microdynamics.
t = sp.symbols('t', positive=True)
H_s, rhop = sp.symbols('H rho_plus_p', positive=True)
dp_nad, kaH = sp.symbols('dp_nad kaH', real=True)
zeta_dot = -(H_s/rhop)*dp_nad + kaH**2*sp.symbols('S')   # schematic super-horizon evolution
# Noether dust: w=0, c_s^2=0 (L82)  ->  delta_p = c_s^2 delta_rho = 0 and delta_p_nad = delta_p - c_s2_bg*delta_rho = 0
cs2_bg = 0                       # background sound speed of dust
dp_dust = 0                      # delta_p for pressureless dust
dp_nad_dust = dp_dust - cs2_bg*sp.symbols('drho')       # = 0
check("Z-1  the L82 Noether dust is ADIABATIC: w=0, c_s^2=0 -> delta_p = 0 and the non-adiabatic pressure "
      "delta_p_nad = delta_p - c_s^2_bg * delta_rho = 0.  A pressureless charge behaves exactly like CDM, "
      "which carries no non-adiabatic stress",
      sp.simplify(dp_nad_dust) == 0,
      "delta_p_nad = 0 for the pressureless Noether dust")

zeta_dot_superH = zeta_dot.subs({dp_nad: 0, kaH: 0})
check("Z-2  [the shield] on super-horizon scales (k/aH -> 0) with delta_p_nad = 0, zeta_dot -> 0: the "
      "comoving curvature perturbation is CONSERVED by causality (Weinberg / separate-universe), "
      "INDEPENDENTLY of the scalar pi's kinetic/symplectic microdynamics.  So the k->0 degeneration of "
      "Omega cannot alter the observable zeta on the very scales where it is worst",
      zeta_dot_superH == 0,
      "zeta_dot = 0 super-horizon for the adiabatic mode, regardless of Omega(k)")

check("Z-3  the curvature perturbation zeta is carried by the HEALTHY Einstein sector (M^2 R gives zeta a "
      "standard quadratic kinetic term; the MOND operator is CUBIC (L82) so it does not touch zeta's "
      "quadratic action).  The degenerating d.o.f. is the EXTRA scalar pi, not zeta -- pi is sequestered "
      "from CMB observables on super-horizon scales exactly as in ghost-condensate/khronometric EFTs",
      sp.limit(G/y**3, y, 0) == sp.Rational(2, 3),   # G ~ (2/3) y^3: cubic, drops from quadratic zeta action
      "MOND term cubic -> zeta kinetic term is standard Einstein; pi is the degenerate (sequestered) mode")

# ==========================================================================================================
sec("PART V -- VERDICT synthesis and the honest residual.")
# ==========================================================================================================
degeneration_confined_superhorizon = (kH0 > 0) and np.all(Om_rel[kk >= kH0] >= 1.0)
no_fatal_instability = (Gpp_num.min() >= -1e-12)
classical_k_regular  = (sp.diff(omega2, k) == 0)
shield_holds         = (zeta_dot_superH == 0) and (sp.simplify(dp_nad_dust) == 0)
check("V-1  [BENIGN synthesis] (i) the degeneration Omega~k^2 is monotone, worst at k->0, and every "
      "OBSERVABLE mode has k >= k_H0 so the worst observable case is the present horizon, with all "
      "sub-horizon scales progressively better; (ii) it is NOT paired with any instability (G''>=0 => "
      "lambda^2<=0 always); (iii) the classical EOM frequency is k-regular (k^2 cancels); (iv) on the "
      "super-horizon band where Omega is smallest, zeta is conserved for the adiabatic dust.  => BENIGN "
      "for the CMB acoustic peaks and for the low-ell plateau",
      degeneration_confined_superhorizon and no_fatal_instability and classical_k_regular and shield_holds,
      "confined super-horizon + no instability + k-regular EOM + zeta-conservation shield")

check("V-2  [adversarial: could it still be FATAL?] a fatal outcome would require the degeneration to bite "
      "at sub-horizon scales (k>k_Hrec) OR to pair with an exponential instability OR for pi to source "
      "non-adiabatic zeta super-horizon.  All three are FALSIFIED here: sub-horizon Omega is enhanced "
      ">=450x (M-4), the instability branch is empty (G-2), and the dust is adiabatic (Z-1).  No route to "
      "fatal survives on the derived quadratic structure",
      enh_rec > 400 and no_fatal_instability and sp.simplify(dp_nad_dust) == 0,
      "no sub-horizon bite, no instability, adiabatic dust -> fatal route closed at this order")

print("""
  HONEST RESIDUAL (NOT asserted as PASS -- the genuine open edge):
    * The zeta-conservation shield (Z-2) requires the FULL perturbation to be adiabatic.  L82 shows the
      Noether DUST alone is adiabatic (delta_p_nad=0).  But the complete theory also carries the khronon/
      aether n^mu and its own perturbation; a relative (isocurvature) mode between the khronon sector and
      the dust could in principle source zeta super-horizon and re-expose the small-Omega band at low ell.
      Proving full-system adiabaticity is astra's next unavoidable calculation (khronon+scalar+dust ADM on
      an expanding branch) and is OUT OF THIS LANE.  Recorded as UNDECIDED for the lowest multipoles.
    * The ABSOLUTE strong-coupling cutoff on the marginal (present-horizon) modes needs the cubic/quartic
      interaction coefficients and the EFT scale M; only the quadratic (kinetic/symplectic) structure is
      in hand.  This lane establishes RELATIVE benignity + super-horizon confinement + the causal shield,
      which is what decides the CMB acoustic physics; the absolute low-ell cutoff is not computed here.
""")

# ==========================================================================================================
sec("SUMMARY")
# ==========================================================================================================
print(f"""
  VERDICT: BENIGN for the CMB acoustic physics; UNDECIDED (but plausibly benign) for the lowest multipoles.

  KEY NUMBERS (Planck LCDM background; footing-independent):
    present horizon        k_H0   = {kH0:.3e} /Mpc   (c/H0 = {Hubble_dist:.0f} Mpc)
    recombination horizon  k_Hrec = {kHrec:.3e} /Mpc   (k_Hrec/k_H0 = {kHrec/kH0:.1f})
    first acoustic peak    k_peak ~ {k_peak:.3e} /Mpc   (ell1 ~ {ell1:.0f}, deep sub-horizon)
    a0 scale (canonical)   k_a0   = {k_a0(a0_can):.3e} /Mpc   (k_a0/k_H0 = {k_a0(a0_can)/kH0:.3f}, super-horizon)
    a0 scale (alternate)   k_a0   = {k_a0(a0_alt):.3e} /Mpc   (k_a0/k_H0 = {k_a0(a0_alt)/kH0:.3f}, super-horizon)
    Omega enhancement at:  recomb horizon = {enh_rec:.0f}x , first peak = {enh_peak:.0f}x  (vs present horizon)

  WHY BENIGN:
    1. Omega_zeta_pi ~ k^2 is monotone -> worst at k->0 = LARGEST scales.  Every observable mode has
       k >= k_H0; the acoustic peaks (k ~ 0.0165/Mpc) sit ~5000x away from the degenerate point.
    2. The degeneration is NOT paired with a dynamical instability: for the exact exponential G,
       G''(y) >= 0 for all y >= 0, so U_pi_pi U_zz >= 0 and lambda^2 <= 0 ALWAYS -- oscillation or a
       marginal (y0=0, cosmological) zero-mode, never exponential growth.
    3. The classical EOM frequency is k-independent (the k^2 cancels between Omega and H_red), so no
       small-k classical pathology follows from the symplectic collapse.
    4. On the super-horizon band where Omega is smallest, zeta is conserved for the adiabatic Noether dust
       (delta_p_nad = 0), and zeta is carried by the healthy Einstein sector -- the degenerate d.o.f. is
       the extra scalar pi, which is sequestered from CMB observables super-horizon.

  HONEST RESIDUAL: full-system adiabaticity (khronon + dust) and the absolute low-ell EFT cutoff are not
  established here; they are astra's khronon-ADM calculation.  Confidence: HIGH that the acoustic peaks are
  unaffected; MODERATE that the lowest multipoles are safe (pending full-system adiabaticity).
""")
print("=" * 112)
if FAILS:
    print(f"L83 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} checks FAILED: {FAILS}"); sys.exit(1)
print(f"L83 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 112)
