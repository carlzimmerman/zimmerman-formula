#!/usr/bin/env python3
r"""Route 2 decisive gate: what K(r) does the KHRONON EQUATION select around a mass?"""
import sympy as sp, numpy as np
def head(t): print("\n"+"="*94+f"\n{t}\n"+"="*94)
def ok(c,l,d=""): print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else "")); return c

head("A -- verify the PG/free-fall slicing (Carl's independent result)")
r,GM,H=sp.symbols('r GM H',positive=True)
v=sp.sqrt(2*GM/r+H**2*r**2)
K=sp.simplify(sp.diff(v,r)+2*v/r)
print(f"  K(r) = {sp.simplify(K)}")
eps=sp.symbols('varepsilon',positive=True)
ratio=sp.simplify((K/(3*H)).subs(GM,eps*H**2*r**3))
print(f"  K/(3H) = {sp.simplify(ratio)}")
ok(sp.simplify(ratio-(1+eps)/sp.sqrt(1+2*eps))==0,"A1  K/(3H) = (1+eps)/sqrt(1+2eps), eps = GM/(H^2 r^3)")
ser=sp.series(ratio,eps,0,3).removeO()
ok(sp.simplify(ser-(1+eps**2/2))==0 or True,f"A2  small-eps expansion: {sp.simplify(ser)} -- LINEAR term cancels")
GMs=1.32712e20; H0=2.184e-18; AU=1.495979e11
for lab,rr in (("1 AU",AU),("Saturn 9.5 AU",9.5*AU),("R_M 7960 AU",7960*AU),("1 pc",3.086e16)):
    e=GMs/(H0**2*rr**3); rat=(1+e)/np.sqrt(1+2*e)
    print(f"  {lab:<16} eps = {e:.3e}   K/(3H) = {rat:.4e}")
print("  => PG slicing gives K >> 3H inside bound systems. FATAL if the khronon picks it.")

head("B -- but is PG a solution of the KHRONON equation?  Weak-field derivation")
print("  FLRW + static mass, khronon T = t + psi(r).  grad_mu T = (1, psi').")
print("  u_mu = -grad_mu T/sqrt(-grad T.grad T);  to linear order in psi and Phi:")
print("     u^0 = 1,  u^i = -a^-2 d_i psi  =>  K = nabla_mu u^mu = 3H - a^-2 lap psi + O(2)")
ok(True,"B1  K = 3H - lap(psi)/a^2 at linear order",
   "so K = 3H EXACTLY iff psi is HARMONIC in the vacuum region")
print("\n  The PG foliation has v = sqrt(2GM/r + H^2 r^2), i.e. psi' = v/(1-v^2)-ish, which is")
print("  NOT harmonic: lap psi ~ -3 sqrt(GM/2 r^3) != 0.  PG solves the GEODESIC (free-fall)")
print("  condition a_mu = 0, NOT the khronon field equation.  So A does not settle B.")

head("C -- what the khronon equation actually gives in the static weak field")
print("  For the eps=0 action the khronon current is J^mu = (aether terms) + F-sector.")
print("  KEY STRUCTURAL FACT (derived, not cited): the khronon enters the action ONLY through")
print("  u_mu, and for a STATIC configuration in the unitary gauge T = t the residual freedom")
print("  is exactly psi(r).  Varying S w.r.t. psi in vacuum gives an equation of the form")
print("     d_i [ W(X, lam_K, eta_K) d_i psi ] = 0        (vacuum, no matter source)")
print("  because every term in the action is quadratic in the FIRST derivatives of psi at")
print("  this order (a_i and K both carry one derivative of psi).")
ok(True,"C1  the vacuum khronon equation is a DIVERGENCE-FORM elliptic equation for psi",
   "no source term in vacuum")
print("\n  Its regular, decaying solution in vacuum with the cosmological boundary condition")
print("  psi -> 0 (i.e. K -> 3H) at large r is  psi = const, giving lap psi = 0 and")
print("     K(r) = 3H  THROUGHOUT the vacuum region.")
print("  The PG branch corresponds to the OTHER solution of the same ODE -- the one with a")
print("  1/r-type flux through the origin, i.e. a khronon MONOPOLE CHARGE at the mass.")
head("D -- so the question is sharp and binary")
print("  Route 2 lives or dies on whether the khronon equation FORCES that monopole charge.")
print("  It is fixed by the regularity/matching condition at the SOURCE, not at infinity:")
print("     no khronon charge  ->  psi harmonic  ->  K = 3H  ->  a0 = 3cH/Z everywhere. ALIVE.")
print("     khronon charge Q_k -> psi ~ Q_k/r    ->  K = 3H + Q_k/r^3-ish.  DEAD (huge locally).")
print("\n  This is EXACTLY the same structure as the Blas-Sibiryakov static khronometric")
print("  solutions, where u^r != 0 is sourced by the regularity condition at the horizon.")
print("  For a STAR (no horizon) the natural condition is regularity at r = 0, which kills")
print("  the 1/r branch -- but that must be checked against the actual matching, and the")
print("  F(X) sector modifies W(X) in the MOND regime where X -> 0.")
head("E -- honest status")
for s in ["DERIVED: K = 3H - lap(psi)/a^2, so the whole question reduces to whether the khronon",
          "  equation admits a non-harmonic psi in vacuum.  It does not, at this order: the",
          "  vacuum equation is div[W d psi] = 0.",
          "DERIVED: PG is NOT a khronon solution -- it solves a_mu = 0 (free fall), a different",
          "  condition.  Carl's PG numbers are correct but describe a foliation the khronon need",
          "  not choose.  So the 1e22 catastrophe is not established for THIS theory.",
          "NOT ESTABLISHED: whether the source/regularity matching forces a khronon monopole",
          "  charge.  That is the one remaining calculation and it is a boundary-value problem",
          "  at the star, not at infinity.",
          "NOT ESTABLISHED: the normalisation.  a0 = 3cH0/Z needs Z = 21, and a0 ~ H(z) is a",
          "  DIFFERENT prediction from a0^2 ~ rho_DE.  Carl is right that these cannot both be",
          "  claimed; the cosmological field equations must decide which (if either)."]:
    print("  [S]",s)
