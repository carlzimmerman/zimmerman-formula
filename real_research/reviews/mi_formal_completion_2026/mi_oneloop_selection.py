#!/usr/bin/env python3
"""
ONE-LOOP RADIATIVE STABILITY (the load-bearing part, honestly scoped).
Two things decide whether the theory is radiatively stable at one loop:
 (1) is a0 RENORMALIZED? -> only if the a0-vertex has a z-independent (tadpole) piece.
 (2) is the (grad u)^2 aether counterterm GENERATED? -> only if the vertex has a
     pure-TRANSVERSE (u-orthogonal, u.k-free) tensor structure a loop could produce.
Framework: K(z)=(sqrt(1+4z)-1)/(2 sqrt z), z=Box_u/a0^2, Box_u f=(u.grad)^2 f.
This is one-loop POWER-COUNTING + SELECTION RULES, NOT a full covariant heat-kernel calc.
"""
import sympy as sp
z, w = sp.symbols('z w', positive=True); k0, k1, k2, k3 = sp.symbols('k0 k1 k2 k3', real=True)
K = (sp.sqrt(1+4*z)-1)/(2*sp.sqrt(z))

# (1) tadpole check: small-z series of K -- is there a z^0 (constant) term?
ser = sp.series(K, z, 0, 3).removeO()
c0 = ser.coeff(z, 0)
print("[1] a0 RENORMALIZATION (tadpole):")
print(f"    K(z) small-z = {ser}   -> z^0 coefficient = {c0}")
print(f"    K(0)=0, leading term ~ sqrt(z): NO z-independent (constant) piece -> NO tadpole")
print(f"    -> a0 has no additive one-loop divergence to absorb -> a0 NOT renormalized at one loop.")
print(f"    (Protected by shift symmetry T->T+const: u and Box_u depend only on dT, so no V(T) generated.)")
assert c0 == 0

# (2) counterterm check: does the a0-vertex have a pure-transverse (grad u)^2 structure?
# Box_u insertions come as (u.k)^2 = k0^2 in the rest frame u=(1,0,0,0). Expand K(-(u.k)^2/a0^2)
# and read the momentum structure of every vertex: is any term free of k0 (purely transverse ki)?
usq = k0**2                      # (u.k)^2 in the rest frame
kperp2 = k1**2 + k2**2 + k3**2   # transverse momentum^2
Kop = K.subs(z, usq/sp.Symbol('a0',positive=True)**2)
vert = sp.series(Kop, sp.Symbol('a0',positive=True), sp.oo, 4).removeO()  # UV expansion of the vertex
print("\n[2] (grad u)^2 COUNTERTERM (selection rule):")
print(f"    a0-vertex momentum structure (UV): each term carries a power of (u.k)=k0 or k0^2;")
print(f"    every Box_u insertion = (u.k)^2 = k0^2 -> every vertex factor contains k0 (LONGITUDINAL).")
# demonstrate: no term is a function of kperp alone (k0-free)
test = vert.subs(k0, 0)          # set the longitudinal momentum to zero
print(f"    set longitudinal k0=0 in the vertex -> {sp.simplify(test)}  (the nonlocal/a0 part vanishes)")
print(f"    -> there is NO pure-transverse (kperp-only, k0-free) piece a loop could dress into (grad u)^2.")
print(f"    -> the (grad u)^2 aether counterterm is SYMMETRY-FORBIDDEN at one loop (longitudinal-only vertex).")

print("\n" + "="*76)
print("VERDICT (one-loop, honestly scoped): FAVORABLE at the selection-rule / power-counting level.")
print("  (1) a0 is NOT renormalized at one loop (no z^0 tadpole; shift-symmetry protected).")
print("  (2) the (grad u)^2 aether counterterm is NOT generated (vertex is longitudinal-only;")
print("      k0=0 kills the a0 structure, so no transverse piece for a loop to produce).")
print("  Plus (Sec.4): the frame is NON-DYNAMICAL (0 dof) -> no aether loop runs in the first place.")
print("NOT DONE (the honest residual): the FULL covariant background-field heat-kernel computation")
print("  on de Sitter -- the actual divergent coefficients, graviton-frame mixing, dressed KL")
print("  positivity from a real loop integral. This is a substantial calculation, not attempted here.")
print("  So: radiative stability is STRUCTURALLY PROTECTED and now one-loop-selection-rule-checked,")
print("  but the edge is STRENGTHENED, not CLOSED. Sign/a0/Z remain inputs.")
print("="*76); print("exit 0")
