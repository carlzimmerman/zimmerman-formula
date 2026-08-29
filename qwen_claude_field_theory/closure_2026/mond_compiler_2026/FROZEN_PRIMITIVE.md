# FROZEN PRIMITIVE — nonlocal pure-metric MOND, exact 1-e^{-y} kernel (2026-08-29)

The candidate branch to carry forward (Carl's decision): a SINGLE physical metric with a CAUSAL NONLOCAL
MOND invariant (Deffayet-Esposito-Farese-Woodard lineage), matter minimally coupled to g.  This branch
evades BOTH committed no-gos LEGITIMATELY by violating LOCALITY (an explicit hypothesis of the Part-I
lensing theorem, and outside the local-auxiliary-carrier T3 theorem entirely).

## The frozen primitive (VERIFIED sympy, this file's check):
  Box_ret Phi = R_mu_nu U^mu U^nu ;  Z = (4 c^4 / a0^2) * grad(Phi).grad(Phi) ;  y = g/a0 (=> Z = 4 y^2)
  F+(Z) = 4 [ 1 - (1 + sqrt(Z)/2) e^{-sqrt(Z)/2} ]
  => 2 F+'(Z) = e^{-sqrt(Z)/2} = e^{-y}   =>   mu(y) = 1 - 2 F+'(4 y^2) = 1 - e^{-y}   EXACT.
  small-Z: F+ = Z/2 - Z^{3/2}/6 + Z^2/32 - Z^{5/2}/240 + ...
  NOTE: F+ is NOT y^2 e^{-y} (that gives mu(1)=0.816, not 0.632); and NOT the 2026 DEFW
  f(Z)=(1/2)Z e^{-sqrt|Z|/3} (their cosmology<->bound interpolator).  These are three distinct functions
  in the same y^2*(exponential) family; only F+ reproduces Carl's exact 1-e^{-y}.

## Status: primitive PASS.  Full theory NOT closed.
  PASS (established for the architecture / this kernel): single metric; causal nonlocal; MOND weak-field;
       BTFR; leading spherical lensing a=r b'; c_T=1 at quadratic TT order.
  OPEN (the closure gates -- none run yet): causal variational formulation; localization; full nonlinear
       DOF/Dirac rank; alpha_1, alpha_2; Z<0 / cosmological closure.
  WARNING (banked): a previous localization of the closely-related causal nonlocal model found a genuine
       scalar characteristic omega^2 = (1/2) c^2 k^2 even after removing the naive localization ghost --
       so localization is NOT automatically harmless; the exact F+ theory must be tested, not assumed.

## Decisive next experiment (Carl's, not yet launched):
  exact F+  ->  causal variation  ->  localize (aux fields for each Box_ret^{-1})  ->  Dirac rank / DOF
            ->  c_T  ->  1PN alpha_1, alpha_2.
  The localization->Dirac step is the make-or-break (DEFW's own flagged risks live there).
