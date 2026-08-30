#!/usr/bin/env python3
"""SWING the elliptic corner: the 6 OPEN single-metric classes (frame-free, nonlocal, RIEMANNIAN, with
a CONSTRAINED/multiplier scalar sector). They evade the slip-lock DERIVATION because that assumed a
PROPAGATING mode (M PSD <=> ghost-free). A Lagrange multiplier is NON-propagating -> can it supply an
INDEFINITE (Phi,Psi) response WITHOUT being a ghost, achieving eta=1 + enhancement? And at what cost?"""
import sympy as sp

m, rho = sp.symbols('m rho', positive=True)     # m=M_p^2 k^2, source
lam = sp.symbols('lambda', real=True)           # Lagrange multiplier (NON-propagating)
Phi, Psi = sp.symbols('Phi Psi', real=True)
d = sp.symbols('d', real=True)                  # nonlocal MOND enhancement of the time (Phi) equation

print("=== 1. does a MULTIPLIER escape the slip-lock ghost obstruction? ===")
print("   slip-lock: eta=1 needs B=-C, enhancement needs A<C, no-ghost needs M PSD (A>=C) -> ghost.")
print("   KEY: 'no-ghost <=> M PSD' held because the mode PROPAGATES. A multiplier has NO kinetic term")
print("   => it is NOT required to be PSD (a constraint has no propagating mode to be a ghost).")
print("   => the multiplier CAN supply the indefinite response slip-lock forbade. Corner is REAL.\n")

# GR quadratic form + nonlocal enhancement D=diag(d,0) on the time potential; multiplier enforces
# constraint w.X=0 with w=(1,-1) (=> Phi=Psi => eta=1 by construction). Solve the 3x3 system.
Ggr = sp.Matrix([[0, 2*m],[2*m, -2*m]])
D   = sp.Matrix([[d, 0],[0, 0]])
w   = sp.Matrix([1, -1])                         # constraint Phi - Psi = 0
X   = sp.Matrix([Phi, Psi]); s = sp.Matrix([rho, 0])
# metric EOM: (Ggr+D)X - s + lam*w = 0 ; constraint: w^T X = 0
eqs = list((Ggr+D)*X - s + lam*w) + [ (w.T*X)[0] ]
sol = sp.solve(eqs, [Phi, Psi, lam], dict=True)[0]
Phi_s = sp.simplify(sol[Phi]); Psi_s = sp.simplify(sol[Psi]); lam_s = sp.simplify(sol[lam])
print("=== 2. impose eta=1 by the multiplier (Phi=Psi), enhance the time eq by d ===")
print(f"   Phi = {Phi_s}")
print(f"   Psi = {Psi_s}")
print(f"   eta = Psi/Phi = {sp.simplify(Psi_s/Phi_s)}  (=1 by construction -- lensing tracks dynamics)")
Phi_GR = rho/(2*m)
Geff = sp.simplify(Phi_s/Phi_GR)
print(f"   G_eff/G_N = Phi/Phi_GR = {Geff}")
print(f"   at d=0 (no MOND enhancement, pure constraint): G_eff/G_N = {sp.simplify(Geff.subs(d,0))}")

print("\n=== 3. what the toy actually shows (sympy-consistent) ===")
print(f"   G_eff/G_N = 2m/(d+2m): d=0 => G_eff=1 (GR, no problem); ENHANCEMENT (G_eff>1) needs d<0.")
print(f"   eta=1 holds for ALL d (the multiplier enforces it) -- so in this toy, enhancement WITH")
print(f"   correct lensing is achievable. The multiplier genuinely evades the slip-lock ghost wall.")
print(f"   HONEST LIMIT of this toy: it does NOT settle whether the required d<0 nonlocal operator is")
print(f"   HEALTHY. d<0 sits in the Phi-Phi entry (GR value 0); its sign-health, gradient stability,")
print(f"   and Bianchi/diff-invariance consistency are NOT captured here -- that is the real physics.")

print("\n=== 4. the corner is NOT virgin: it CONTAINS the repo York/CMC route ===")
print("   Single-metric + frame-free + constrained-sector + (its lensing fixed by a constraint) is")
print("   exactly the York/CMC family the repo already explored -- which independently FAILED at")
print("   E (G_eff=2G in ITS realization) and F (Cassini). That is one adverse data point INSIDE this")
print("   corner, not a proof the whole corner is dead (different constraint => different G_eff).")

print("\n=== VERDICT (elliptic corner) -- OPEN, NARROWED, honest ===")
print("SOUND: a non-propagating multiplier evades slip-lock's ghost obstruction (that wall assumed a")
print("PROPAGATING mode); eta=1 + enhancement is achievable in the linear toy. So the 6 cells are")
print("GENUINELY OPEN, as Aella found -- NOT a false positive.")
print("NOT SETTLED: whether the required nonlocal enhancement is HEALTHY (sign-correct in the Phi-Phi")
print("kinetic entry, gradient-stable c_s^2>=0, Bianchi-consistent) AND whether it avoids the York")
print("G_eff/Cassini failures that one realization in this corner already hit.")
print("=> THE decisive sub-question for all 6 cells: does a healthy elliptic nonlocal operator give")
print("   G_eff>1 with eta=1 across the acceleration range, gradient-stable, without a York-type G_eff")
print("   or Cassini failure? Needs the ACTUAL constrained action (multiplier + nonlocal kernel + the")
print("   Hamiltonian constraint algebra), not this linear toy. That is the next real calc -- escalate.")
import json
print("CERTIFICATE_JSON:", json.dumps({"gate":"elliptic-corner","status":"OPEN-NARROWED",
 "certificate":("Multiplier (non-propagating) genuinely evades slip-lock's ghost obstruction (which "
   "assumed a PROPAGATING mode); linear toy: eta=1 + enhancement achievable (G_eff=2m/(d+2m), enhancement "
   "needs d<0). 6 cells GENUINELY OPEN, not a false positive. UNSETTLED: health of the required d<0 "
   "nonlocal operator (sign/gradient/Bianchi) + whether it avoids the York-route G_eff=2G/Cassini failures "
   "one realization in this corner already hit. Decisive next calc = full constrained action + Hamiltonian "
   "constraint algebra, NOT this toy."),
 "numeric_values":{"G_eff_toy":"2m/(d+2m)","enhance_needs":"d<0"}}))
