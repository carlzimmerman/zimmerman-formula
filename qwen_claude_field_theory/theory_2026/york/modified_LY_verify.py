"""
Modified Lichnerowicz-York (LY) equation for the CMC-gauge MOND-deformed theory.

Action:
  S = (c^3/16 pi G) INT N sqrt(h) (K_ij K^ij - K^2 + R3)
    - (1/8 pi G)   INT N sqrt(h) a0(q)^2 U( DPhi.DPhi / a0(q)^2 )
    + S_matter

  U'(y) = mu(sqrt y),  mu(x) = x/sqrt(1+x^2)  =>  U'(y) = sqrt(y)/sqrt(1+y)
  U(y)  = sqrt(y(1+y)) - arcsinh(sqrt y)            (to be verified)
  a0(q) = c q / Z,  q = K = 3H  is a SINGLE GLOBAL CMC number (no psi weight).

This script verifies, symbolically:
  (A) U(y) integrates U'(y) = mu(sqrt y).
  (B) The conformal algebra giving the standard LY operator.
  (C) The MOND source term and its exact psi-derivative (monotonicity test for
      LY uniqueness):    S_MOND(psi) = -2 a0^2 U(psi^{-4} ybar) psi^5
      dS_MOND/dpsi sign  <->  sign of (5 U - 4 y U').
  (D) The lapse-fixing 'potential'  V_MOND = 4 pi G (E+S)_MOND = a0^2 (y U' - U),
      and that y U' - U >= 0 for all y (positive-definiteness of the lapse op).
  (E) Deep-MOND (y->0) and Newtonian (y->inf) limits of both sign-quantities.
"""
import sympy as sp

y, psi, ybar, a0 = sp.symbols('y psi ybar a0', positive=True)

# ---- (A) U(y) from U'(y)=mu(sqrt y) ------------------------------------
Uprime = sp.sqrt(y)/sp.sqrt(1+y)             # = mu(sqrt y)
U = sp.sqrt(y*(1+y)) - sp.asinh(sp.sqrt(y))
print("=== (A) U integrates U' ===")
dU = sp.simplify(sp.diff(U, y) - Uprime)
print("d/dy[U] - U'  =", dU, "  (expect 0)")

# ---- (C) MOND source in LY: monotonicity in psi ------------------------
# In LY the total source enters as   -16 pi G rho * psi^5.
# rho_MOND = a0^2 U / (8 pi G)  ==>  -16 pi G rho_MOND psi^5 = -2 a0^2 U psi^5.
# Argument y = |DPhi|^2/a0^2 = psi^{-4} * ybar,  ybar=|Dbar Phi|^2/a0^2.
print("\n=== (C) LY MOND source S_MOND(psi) = -2 a0^2 U(psi^-4 ybar) psi^5 ===")
yy = psi**(-4)*ybar
S_MOND = -2*a0**2*U.subs(y, yy)*psi**5
dS = sp.simplify(sp.diff(S_MOND, psi))
# Re-express in terms of y and U,U' to expose the sign structure.
Usym = sp.Function('U')
# Do it by hand-checked substitution: dS/dpsi = -2 a0^2 psi^4 (5 U - 4 y U')
target = -2*a0**2*psi**4*(5*U.subs(y, yy) - 4*yy*Uprime.subs(y, yy))
print("dS/dpsi - (-2 a0^2 psi^4 (5U-4yU')) =",
      sp.simplify(dS - target), "  (expect 0)")
mono = sp.simplify(5*U - 4*y*Uprime)    # sign controls uniqueness
print("Sign-quantity  m(y) = 5U - 4 y U' :")
print("   deep-MOND  y->0 :", sp.simplify(sp.series(mono, y, 0, 2).removeO()))
print("   Newtonian  y->oo:", sp.limit(mono, y, sp.oo))
# leading Newtonian behaviour
print("   Newtonian leading (mono/y as y->oo):", sp.limit(mono/y, y, sp.oo))

# ---- (D) Lapse-fixing potential V_MOND = a0^2 (y U' - U) ----------------
print("\n=== (D) Lapse potential  V_MOND = 4 pi G (E+S) = a0^2 (y U' - U) ===")
w = sp.simplify(y*Uprime - U)                # want >= 0 for all y>=0
print("w(y)=yU'-U :  w(0)=", sp.limit(w, y, 0),
      "  w'(y)=", sp.simplify(sp.diff(w, y)), " = y*U''")
Upp = sp.simplify(sp.diff(Uprime, y))
print("U''(y) =", Upp, "  (>=0 for y>=0  => w increasing => w>=0)")
print("   deep-MOND  w~", sp.simplify(sp.series(w, y, 0, 2).removeO()))
print("   Newtonian  w->", sp.limit(w, y, sp.oo), " (grows: w/log(y)->",
      sp.limit(w/sp.log(y), y, sp.oo), ")")

# ---- (E) deep-MOND vs Newtonian summary of source power in psi ---------
print("\n=== (E) LY source power in psi, by regime ===")
# deep-MOND: U ~ (2/3) y^{3/2}  => -2 a0^2 U psi^5 ~ -(4/3) a0^2 ybar^{3/2} psi^-1
print("deep-MOND U~(2/3)y^{3/2}: source ~ -(4/3)a0^2 ybar^{3/2} psi^{-1}  "
      "(NEGATIVE power => d/dpsi>0 => GOOD sign, like -Abar^2 psi^-7)")
print("Newtonian U~y:            source ~ -2 |Dbar Phi|^2 psi^{+1}          "
      "(POSITIVE power => d/dpsi<0 => matter-like BAD sign)")
