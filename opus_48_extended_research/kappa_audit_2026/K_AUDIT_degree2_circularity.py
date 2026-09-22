#!/usr/bin/env python3
"""
K_AUDIT (deep dive) -- the DEGREE-2 leg of the kappa=1/2 derivation (PD22 T1 + G084).

PD22 T1 proves: P1(symmetry)+P2(one-channel exactness)+P3(saturation)+P4(degree-2) force the
OR-composition C(p,q)=p+q-pq uniquely. This script isolates P4 and shows it is the load-bearing,
least-justified premise -- three ways, reproducibly:

  (A) P4 IS ESSENTIAL: without the degree-2 restriction, P1+P2+P3 admit an infinite family
      (a counterexample tower), so the OR-composition is NOT unique. Only P4 kills the tower.
  (B) G084 DOES NOT JUSTIFY P4: G084's "2" is a spatial density-falloff exponent (rho ~ r^-2);
      P4 is the polynomial degree of the channel-COMPOSITION function. Different objects
      (category mismatch), and G084's gamma=2 itself only holds at sigma^2=C/2 (eta=1/2).
  (C) THE ONLY REAL JUSTIFICATION FOR DEGREE-2 IS CIRCULAR: the exact form p+q-pq is what
      independent-channel probabilistic OR gives -- but "independent channels combining as OR"
      IS the OR-identification the theorem claims to derive.

Fair credit: PD22 T6a/T6b genuinely prove that WITHIN the degree-2 class the four principles are
independent and select the OR uniquely. That content is real -- it is "given degree-2". Degree-2
itself is the unproven joint.

Run: python3 opus_48_extended_research/kappa_audit_2026/K_AUDIT_degree2_circularity.py   (needs sympy)
"""
import sympy as sp

p, q, k, delta = sp.symbols('p q k delta', real=True)
C_or = p + q - p*q

print("="*92)
print("DEGREE-2 (P4) -- the load-bearing, least-justified premise of PD22's uniqueness theorem")
print("="*92)

# ---- (A) P4 is essential: a degree-4 counterexample tower survives P1+P2+P3 for every k ----
print("\n(A) IS P4 ESSENTIAL?  Test C_k = p+q-pq + k*p*q*(1-p)*(1-q)  against P1,P2,P3 (NOT P4):")
C_k = C_or + k*p*q*(1-p)*(1-q)
P1 = sp.simplify(C_k - C_k.subs({p: q, q: p}, simultaneous=True))   # symmetry
P2 = sp.simplify(C_k.subs(q, 0) - p)                                # one-channel exactness (all p)
P3 = sp.simplify(C_k.subs({p: 1, q: 1}) - 1)                        # saturation
deg = sp.Poly(sp.expand(C_k), p, q).total_degree()
print(f"    P1 (symmetry)            C_k(p,q)-C_k(q,p) = {P1}")
print(f"    P2 (one-channel exact)   C_k(p,0)-p        = {P2}")
print(f"    P3 (saturation)          C_k(1,1)-1        = {P3}")
print(f"    total degree of C_k = {deg}  (degree-4 when k!=0)")
essential = (P1 == 0 and P2 == 0 and P3 == 0)
print(f"    -> P1,P2,P3 hold for EVERY k: [{'CONFIRMED' if essential else 'NO'}]. The OR is recovered only at k=0.")
print("    => P1+P2+P3 do NOT force the OR-composition. P4 (degree<=2) is the premise that kills k!=0.")
print("       PD22's uniqueness rests entirely on P4.")

# ---- fair credit: PD22 T6 -- WITHIN degree-2, the principles are independent and select OR ----
print("\n    FAIR CREDIT (PD22 T6a/T6b): within the degree-2 family p+q+delta*p*q,")
famsym = sp.simplify((p+q+delta*p*q) - (q+p+delta*q*p))
sel = sp.solve(sp.Eq((p+q+delta*p*q).subs({p: 1, q: 1}), 1), delta)
print(f"       symmetric for all delta ({famsym==0}); saturation selects delta = {sel} (= -1 => OR).")
print("       That within-degree-2 uniqueness is a genuine theorem. The gap is degree-2 itself.")

# ---- (B) G084's '2' is a different object, and not free-standing ----
print("\n(B) DOES G084 JUSTIFY P4?  G084: rho ~ r^-gamma with gamma = C/sigma^2 (a DENSITY exponent).")
Cc, s2 = sp.symbols('C sigma2', positive=True)
gamma = Cc/s2
print(f"    gamma = C/sigma^2 = {gamma}; gamma=2 only at sigma^2 = C/2 (eta=1/2): gamma={sp.simplify(gamma.subs(s2, Cc/2))}")
print("    P4 is the polynomial degree of the channel-COMPOSITION C(p,q) -- a different object than a")
print("    spatial density falloff. Citing gamma=2 for P4 is a category mismatch; and gamma=2 itself")
print("    is conditional on eta=1/2, so it is not even a free-standing 2.")

# ---- (C) the exact OR form comes from assuming independent-channel OR = circular ----
print("\n(C) WHAT ACTUALLY GIVES DEGREE-2?  Independent-channel probabilistic OR:")
pr, qr = sp.symbols('p q', real=True)
C_indep = sp.expand(1 - (1-pr)*(1-qr))
print(f"    P(at least one of two independent channels) = 1-(1-p)(1-q) = {C_indep}  (exactly p+q-pq, degree 2)")
print("    So degree-2 (indeed the exact OR) follows from ASSUMING independent channels combining as OR")
print("    -- which is the OR-identification the theorem sets out to derive. That justification is circular.")

print("\n" + "="*92)
print("VERDICT: P4 (degree-2) is load-bearing (A), mis-justified by G084 (B, category mismatch +")
print("eta=1/2-conditional), and its only genuine justification is the OR-structure being derived (C,")
print("circular). PD22's uniqueness is real GIVEN degree-2; degree-2 is the unproven joint. This is the")
print("weakest of the three kappa=1/2 legs -- sharper than 'borrows eta=1/2': the cited support is the")
print("wrong object, and the real support is circular.")
assert essential, "counterexample tower did not validate -- investigate before trusting the verdict"
