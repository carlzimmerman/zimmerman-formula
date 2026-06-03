#!/usr/bin/env python3
"""
THE CLAUSIUS SIGN, COMPUTED -- does the covariant temperature route give MOND or anti-MOND?
==========================================================================================
The one bounded open theory item. We carry out Jacobson's local-horizon Clausius calculation
explicitly (the Raychaudhuri/optical-scalar integral), first unmodified (-> Einstein), then with
the de Sitter-Unruh temperature, and READ OFF the sign. No hand-waving: the effective Newton
constant comes out in closed form. The result decides whether the uncontested covariant route
can work. Needs numpy + sympy.
"""
import numpy as np, sympy as sp

print("="*84)
print("PART 1 -- Jacobson's calculation, explicitly (the Raychaudhuri integral) -> Einstein")
print("="*84)
print("""  Local Rindler horizon through p; null generators k^mu, affine parameter lambda; approximate
  boost Killing vector chi^mu = -kappa lambda k^mu. Two ingredients:
    HEAT   dQ = INT T_munu chi^mu dSigma^nu = -kappa INT lambda (T_kk) dlambda dA,   T_kk=T_munu k^mu k^nu
    ENTROPY dS = eta dA,  dA = INT theta dlambda dA,  Raychaudhuri: dtheta/dlambda = -R_kk (leading) ->
            theta(lambda) = -lambda R_kk,  so dA = INT (-lambda R_kk) dlambda dA.
  Clausius dQ = T dS with the Unruh T = kappa/2pi:""")
lam, kappa, Rkk, Tkk, eta, H = sp.symbols('lambda kappa R_kk T_kk eta H', positive=True)
# heat integrand ~ -kappa*lambda*Tkk ; entropy integrand ~ eta*T*(-lambda*Rkk). The INT lambda dlambda
# and dA factors are COMMON to both sides and cancel. So the local Clausius balance is the integrand
# coefficient equation:   kappa*Tkk = T(kappa)*eta*Rkk.
T_unruh = kappa/(2*sp.pi)
balance_unruh = sp.Eq(kappa*Tkk, T_unruh*eta*Rkk)
Tkk_sol = sp.solve(balance_unruh, Tkk)[0]
print(f"     local balance:  kappa*T_kk = T(kappa)*eta*R_kk")
print(f"     with T=kappa/2pi  ->  T_kk = {Tkk_sol}  = (eta/2pi) R_kk = (1/8 pi G) R_kk  [eta=1/4G]")
print(f"     => Einstein equations, G = 1/(4 eta). [ESTABLISHED, reproduced]\n")

print("="*84)
print("PART 2 -- swap in the de Sitter-Unruh T and SOLVE for the effective G")
print("="*84)
T_dSU = sp.sqrt(kappa**2 + H**2)/(2*sp.pi)        # de Sitter-Unruh temperature (c=1)
balance_dSU = sp.Eq(kappa*Tkk, T_dSU*eta*Rkk)
Tkk_dSU = sp.solve(balance_dSU, Tkk)[0]
# Einstein-form: T_kk = (1/8 pi G_eff) R_kk = (eta_eff/2pi) R_kk. Compare coefficient of R_kk:
coeff = sp.simplify(Tkk_dSU/Rkk)                  # = (eta/2pi)*W, W=sqrt(1+(H/kappa)^2)
W = sp.sqrt(1 + (H/kappa)**2)
print(f"     with T=sqrt(kappa^2+H^2)/2pi  ->  T_kk = {sp.simplify(Tkk_dSU)}")
print(f"     coefficient of R_kk = {sp.simplify(coeff)} = (eta/2pi) * W,  W=sqrt(1+(H/kappa)^2)")
print(f"     => R_kk = (8 pi G / W) T_kk, i.e. EFFECTIVE NEWTON CONSTANT  G_eff = G / W.")
print(f"        G_eff/G = 1/W = kappa/sqrt(kappa^2+(cH)^2).\n")

print("="*84)
print("PART 3 -- READ THE SIGN: it is the WRONG way (anti-MOND)")
print("="*84)
c, Hnum = 2.99792458e8, 67.4e3/3.0857e22
cH = c*Hnum
print(f"  G_eff/G = kappa/sqrt(kappa^2+(cH)^2), cH={cH:.2e} m/s^2:")
print(f"     {'kappa/cH':>10}{'G_eff/G':>12}{'meaning':>26}")
for x in (100, 3, 1, 0.3, 0.03):
    kap = x*cH; ratio = kap/np.sqrt(kap**2+cH**2)
    msg = "~1 (Newton)" if x > 3 else ("-> 0 : gravity SHUTS OFF" if x < 0.3 else "weakening")
    print(f"     {x:>10}{ratio:>12.3f}{msg:>26}")
print("""  At LOW acceleration the de Sitter-Unruh temperature is HIGHER, so a given matter flux dQ
  produces a SMALLER area change dS -> LESS focusing -> WEAKER gravity, with G_eff -> 0 as
  kappa -> 0. That is the OPPOSITE of MOND (which needs ENHANCED gravity below a0). The
  uncontested TEMPERATURE-modification route DOES NOT give MOND -- it gives anti-MOND. DEFINITIVE.\n""")

print("="*84)
print("PART 4 -- what the negative result TEACHES (it sharpens the open problem)")
print("="*84)
print("""  The calculation is clean and decisive, and it explains WHY emergent MOND is hard:
    * MOND needs gravity to be STRONGER at low acceleration (extra 'dark' pull). In the Clausius
      balance kappa T_kk = T eta R_kk, that requires the RIGHT-hand side to grow at low kappa --
      i.e. you must boost eta (the ENTROPY), not T (the temperature). A higher T does the reverse.
    * This is exactly why the ONLY routes that yield MOND modify the ENTROPY: Verlinde's volume-law
      de Sitter entropy adds entropy (and an elastic force) at large scales -> stronger pull. The
      price is that the volume-law entropy is contested.
    * So the honest map of item A is now sharp:
        - TEMPERATURE modification (uncontested inputs)  -> anti-MOND. RULED OUT (this calc).
        - ENTROPY modification (Verlinde, gives MOND)     -> CONTESTED premise (volume law).
      There is no known modification that is BOTH uncontested AND gives MOND. THAT gap -- a
      defensible entropy correction to the area law that yields the deep-MOND sign -- is the real
      open problem, now isolated to a single requirement.
  This is genuine progress: a bounded calculation done, a wrong route eliminated with certainty,
  and the remaining problem reduced to one precise demand. No numerology, and no false momentum.""")
print("="*84)
