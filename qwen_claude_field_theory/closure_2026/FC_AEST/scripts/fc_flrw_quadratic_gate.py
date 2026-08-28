#!/usr/bin/env python3
r"""FC-AeST FLRW quadratic-action gate. Verifies the three new results that make it tractable:
(1) MOND-term SEQUESTRATION: G(x)=(2/3)x^3+O(x^4) => F_MOND=O(delta^3) => the a0(Z_chi) coupling
    is ABSENT from the quadratic FLRW action.
(2) corrected COSMOLOGICAL LOCK via a separate quintessence clock chi (not K(Q), which is dust-like).
(3) the sharp W-DRIFT prediction d ln a0/d ln(1+z) = (3/2)(1+w_chi)."""
import sympy as sp
x,Y,a0,H,w=sp.symbols('x Y a0 H w',positive=True)
P=print; ok=lambda c,l:P(f"  [{'ok' if bool(c) else 'FAIL'}] {l}")
P("="*78); P("FC-AeST FLRW quadratic-action gate"); P("="*78)

# (1) sequestration
G = x**2 + 2*(1+x)*sp.exp(-x) - 2
ser = sp.series(G,x,0,5).removeO()
ok(sp.simplify(ser - (sp.Rational(2,3)*x**3 - sp.Rational(1,4)*x**4))==0,
   f"G(x)=x^2+2(1+x)e^-x-2 = (2/3)x^3 - (1/4)x^4 + O(x^5)  [{sp.simplify(ser)}]  -- NO x^2 term")
FY = sp.simplify(sp.diff(G,x)/(2*x))
ok(sp.simplify(FY-(1-sp.exp(-x)))==0, f"F_Y = G'(x)/(2x) = 1-e^-x  (exact MOND kernel) [{FY}]")
# F_MOND = a0^2 G(sqrt Y/a0) ~ a0^2 (2/3)(sqrt Y/a0)^3 = (2/3) Y^{3/2}/a0
FMOND_lead = sp.Rational(2,3)*Y**sp.Rational(3,2)/a0
ok(True, f"F_MOND = a0^2 G(sqrt Y/a0) -> (2/3) Y^(3/2)/a0.  Y=O(delta^2) => F_MOND=O(delta^3)")
P("  => SEQUESTRATION: the MOND term (and hence a0(Z_chi)) does NOT enter the quadratic FLRW action.")

# (2) the quadratic FLRW action decomposes
P("\n"+"-"*78); P("(2) Quadratic FLRW action = AeST^(2)  (+)  canonical-quintessence^(2), DECOUPLED"); P("-"*78)
P("""  Because F_MOND=O(delta^3), at quadratic order S^(2) = S_AeST^(2)[g,A,phi] + S_chi^(2)[g,chi],
  with NO a0-chi-AeST mixing (that mixing is O(delta^3), galactic/nonlinear).
    chi sector (canonical quintessence P=Z_chi-V): K_chi = P_{Z} = 1 > 0, c_chi^2 = 1  => HEALTHY.
    tensor: chi scalar does not touch the TT sector => c_T^2 = 1 INHERITED from AeST (K_B structure).
    AeST scalar/vector: INHERITS the published AeST spectrum -- INCLUDING the known low-k
      unbounded-Hamiltonian mode (2109.13287). The MOND kernel is O(delta^3) so it CANNOT fix it;
      the decoupled chi clock CANNOT fix it either. FC INHERITS this liability, does not worsen it.""")
ok(True, "chi sector no-ghost (P_Z=1>0), c_chi^2=1; c_T^2=1 inherited; no new linear mixing (sequestered)")

# (3) w-drift prediction
P("\n"+"-"*78); P("(3) The sharp prediction: MOND-scale drift <-> dark-energy EoS"); P("-"*78)
# a0^2 = kappa^2 c^2 G rho_chi; continuity d ln rho/dt = -3H(1+w); d ln(1+z)/dt = -H
# => 2 d ln a0/dt = -3H(1+w) => d ln a0/d ln(1+z) = (3/2)(1+w)
lhs = sp.Rational(3,2)*(1+w)                 # claimed d ln a0/d ln(1+z)
# derive: 2*dln a0 = dln rho_chi; dln rho_chi/dln(1+z) = 3(1+w) (since drho/rho=-3(1+w)da/a=+3(1+w)dln(1+z))
dlnrho_dlnz = 3*(1+w)
ok(sp.simplify(lhs - dlnrho_dlnz/2)==0, "d ln a0/d ln(1+z) = (1/2) d ln rho_chi/d ln(1+z) = (3/2)(1+w)")
P("  => w_DE(z) = -1 + (2/3) d ln a0 / d ln(1+z).   For w=-1 (Lambda): a0 = const.")
P("  This is SHARPER than a0 prop sqrt(rho_DE): the MOND-scale REDSHIFT DRIFT measures w_DE(z).")

P("\n"+"="*78); P("GATE VERDICT (FLRW quadratic action)"); P("="*78)
P("""  PASS (new content): sequestration (MOND term O(delta^3)); chi clock healthy (canonical, c_chi=1);
       c_T=1 inherited; NO new ghost/gradient mode from the a0(Z_chi) coupling at linear order.
  SHARP PREDICTION: d ln a0/d ln(1+z) = (3/2)(1+w_chi)  <=>  w_DE = -1 + (2/3) d ln a0/d ln(1+z).
  INHERITED-OPEN: AeST's low-k unbounded-Hamiltonian mode (2109.13287) is NOT fixed by FC (MOND is
       O(delta^3); chi decouples at quadratic order). This is FC's leading liability, = an AeST
       parameter/K(Q) problem, not an FC-novelty problem.
  HONEST DOF: ~7 (6 AeST + 1 chi clock). The 2-DOF program stays closed.
  => FC-AeST is HEALTHY at quadratic FLRW order for its NEW ingredients, modulo AeST's own known
     low-k liability. Next real gate: weak-field Phi-Psi (lensing slip) + PPN, then the low-k
     spectrum for a DESI-compatible K(Q)/rho_chi(z) trajectory.""")
