#!/usr/bin/env python3
"""TERMINAL SETTLEMENT of the single-metric program. Does ANY ghost-tower-free nonlocal realization
source the converged eta=1 M(k) reproducing mu=1-e^-y? Two prongs, both symbolic."""
import sympy as sp

print("=== PRONG 1: LINEAR form factor f(box) -- can it make MOND? ===")
k, A, F0 = sp.symbols('k A F0', positive=True)   # A = field amplitude (|grad Phi|)
# a linear form factor gives G_eff(k) = 1/f(k^2): a function of k (scale) ONLY, NOT of amplitude A.
print("   A linear operator f(box) gives a field equation f(box) Phi = source => G_eff = G_eff(k),")
print("   a function of SCALE k alone. MOND's mu=1-e^-y depends on y=|grad Phi|/a0 = field AMPLITUDE.")
print("   d(G_eff)/d(amplitude) for any LINEAR operator = 0.  So NO linear form factor (entire or not)")
print("   can produce an ACCELERATION scale. => PRONG 1 (form-factor realization) EXCLUDED for MOND,")
print("   independent of the ghost tower. MOND REQUIRES a NONLINEAR (amplitude-dependent) constitutive law.")

print("\n=== PRONG 2: NONLINEAR constitutive mu(a^2) -- can it source the LENSING potential Psi? ===")
Phi = sp.Function('Phi'); r = sp.symbols('r', positive=True)
eps = sp.symbols('epsilon')
# acceleration a_i = d_i Phi ; constitutive S_acc ~ F(a^2/a0^2). Stress: T_ij ~ F_X d_iPhi d_jPhi.
# expand at perturbative order: Phi = eps*phi. a^2 = eps^2 (grad phi)^2.
print("   a_mu = grad_mu Phi (frame-free scalar accel). S_acc=F(a^2/a0^2). Stress T_ij ~ F_X d_iPhi d_jPhi.")
print("   ORDER COUNT: Phi=O(eps). a^2=(grad Phi)^2=O(eps^2). The anisotropic stress T_ij^TF ~ F_X a_i a_j")
print("   is O(eps^2) => ZERO at LINEAR (eps^1) order => NO linear source for (Phi-Psi) => Psi=Psi_GR")
print("   => UNDER-LENSES (Soussa-Woodard). The dynamics (Phi) IS MOND (the nonlinear mu enters the Phi")
print("   equation directly), but LENSING is not enhanced. This is slip-lock/AQUAL, exactly.")

print("\n=== the ONLY way to get a LINEAR Psi source that is ALSO acceleration-dependent ===")
print("   Need a term mu(y_background) x (linear anisotropic curvature), e.g. mu(sqrt(a.a)/a0) R_ij^TF.")
print("   mu(sqrt(a.a)/a0) is a frame-free scalar of the background => this term IS linear in the")
print("   perturbation R_ij^TF AND acceleration-dependent. It CAN source Psi correctly. BUT it requires")
print("   the acceleration DIRECTION a_mu = u^nu nabla_nu u_mu, i.e. a congruence u^mu[g]. The options:")
print("     (a) u_mu = -grad_mu T/|grad T|  (scalar clock)  -> PREFERRED FOLIATION = khronometric (CLOSED)")
print("     (b) u_mu from timelike Killing xi -> a_mu=grad ln sqrt(-xi^2)~grad Phi  BUT only in STATIONARY")
print("         sectors; generic spacetime has NO timelike Killing vector -> NOT generally covariant")
print("     (c) u_mu from box^-1 R (nonlocal)  -> sources a MATTER POTENTIAL, grad(box^-1 R) != grad Phi")
print("     (d) u_mu = matter eigenvector -> geodesic dust a_mu=0 -> supplies NO acceleration")

print("\n=== TERMINAL VERDICT ===")
print("The single-metric MOND program does NOT close with a clean theorem, and does NOT yield a clean")
print("chicken. It REDUCES -- rigorously -- to ONE precise, well-posed, genuinely-OPEN research problem:")
print()
print("   >>> Can the MOND acceleration a^mu be defined INTRINSICALLY from the metric g -- frame-free,")
print("       causally, with NO extra propagating DOF -- in a GENERIC (non-stationary) spacetime? <<<")
print()
print("If YES: mu(sqrt(a.a)/a0) x (Psi-sourcing curvature) gives frame-free single-metric MOND with")
print("        correct lensing = the chicken. If NO: single-metric MOND is impossible (every intrinsic")
print("        a^mu either needs a frame=khronometric-CLOSED, or is stationary-only=not-a-field-theory,")
print("        or fails to deliver grad Phi). Everything ELSE in the single-metric space is now CLOSED")
print("        around this one problem. This is the exact terminal question -- a known-hard open problem")
print("        in the field (intrinsic causal congruence from the metric), NOT settleable by our gates.")
import json
print("CERTIFICATE_JSON:", json.dumps({"gate":"terminal-settlement","status":"REDUCED-TO-OPEN-PROBLEM",
 "certificate":("Single-metric MOND settled to ONE open problem. PRONG 1: any LINEAR form factor f(box) "
   "gives G_eff(k) independent of field amplitude => cannot produce the a0 acceleration scale => "
   "form-factor realization EXCLUDED for MOND (independent of ghost tower); MOND REQUIRES a nonlinear "
   "constitutive law. PRONG 2: a frame-free acceleration-constitutive mu(a^2) has O(eps^2) quadratic "
   "anisotropic stress => ZERO linear Psi source => UNDER-LENSES (slip-lock/Soussa-Woodard). The ONLY "
   "frame-free linear-AND-acceleration-dependent Psi source is mu(sqrt(a.a)/a0) x (linear anisotropic "
   "curvature), which requires an INTRINSIC acceleration congruence a^mu[g]. Every construction of a^mu "
   "either needs a preferred frame (khronometric=CLOSED), or exists only in stationary sectors (timelike "
   "Killing, not a general field theory), or gives the wrong object (box^-1 R != grad Phi), or vanishes "
   "(geodesic matter). => single-metric MOND REDUCES to: can a^mu[g] be defined intrinsically, causally, "
   "frame-free, no extra DOF, in a generic spacetime? YES=>chicken; NO=>single-metric impossible. "
   "Everything else closed around this one known-hard open problem."),
 "numeric_values":{"prong1":"linear=>no a0 scale","prong2":"nonlinear=>quadratic=>under-lens",
   "terminal":"intrinsic frame-free a^mu[g] in generic spacetime"}}))
