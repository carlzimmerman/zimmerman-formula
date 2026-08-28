"""
Gate A — FC-FINAL HAMILTONIAN RANK.  Status: PARTIAL (kinetic-sector PASS) + OPEN (full nonlinear rank).
========================================================================================================
REQUIREMENT: take the known AeST 3+1 system and replace ONLY F(Y,Q) -> F_Q^star(Q) + a0^2 J10(sqrt Y/a0),
a0 CONSTANT (no sigma). Recompute momenta, all constraints, the complete Poisson matrix, its rank on the
regular branch. Target N_phys = 6 (established AeST count) IFF the modified F preserves the 4-first/4-second
-class degeneracy. Do NOT count DOF from field names. First failure terminates the branch.

WHAT THIS SCRIPT DERIVES NOW (a genuine sub-result): the modification is a function of Y ONLY (a0 constant),
and Y = (g+AA)grad phi grad phi carries NO phi-dot (aether-orthogonal projector). So the MOND term
contributes ZERO to every velocity (kinetic) Hessian entry => it does NOT add a propagating mode and does
NOT change the AeST kinetic-sector rank. FC-FINAL adds no field => target N_phys = 6, not 7.
"""
import sympy as sp
P = print
P("="*94); P("Gate A  FC-FINAL Hamiltonian rank"); P("="*94)

# derivable: F_M = a0^2 J10(sqrt Y/a0) has no time derivative => zero velocity-Hessian contribution
N, h1, h2, h3, pt, px, a0, Y = sp.symbols('N h1 h2 h3 phi_t phi_x a0 Y', real=True, positive=True)
ginv = sp.diag(-1/N**2, 1/h1, 1/h2, 1/h3); Aup = sp.Matrix([1/N,0,0,0])
Ycal = (sp.Matrix([pt,px,0,0]).T*(ginv+Aup*Aup.T)*sp.Matrix([pt,px,0,0]))[0]
F_M = a0**2*(sp.sqrt(Ycal)/a0)**3/3
print(f"  Y (aether-orthogonal) = {sp.simplify(Ycal)}  => dY/dphi_t = {sp.simplify(sp.diff(Ycal,pt))}")
print(f"  d F_M / d phi_t = {sp.simplify(sp.diff(F_M, pt))}  (no phi-dot => zero velocity-Hessian entry)")
print(f"\n  [PASS] kinetic sector: the modification adds NO velocity-Hessian contribution and NO new field.")
print(f"         => it cannot add a propagating mode; target N_phys = 6 (the AeST count). No '6+1' inflation.")
print(f"         (established: fc7_reduced_action_rank_2026.py projector result)")

P("\n"+"-"*94)
P("  [OPEN — THE KEY GATE] Y=0 DEGENERATE BRANCH. The AeST 6-DOF theorem (PRD 110.044015) holds for a")
P("  general F(Y,Q) *provided the auxiliary 2x2 Hessian is nondegenerate*. For J10~x^3/3 we have")
P("  F_YY ~ 1/(4 sqrt(Y) a0) -> INFINITY as Y->0 (verified: fc8_symbolic_audit.py A7). So the constitutive")
P("  Hessian is REGULAR on the generic Y>0 branch (=> 6-DOF expectation applies there) but SINGULAR exactly")
P("  on the homogeneous Y=0 background used for the vacuum/cosmology expansion. Because F_M=O(Y^{3/2}) the")
P("  first and second variations vanish (delta S_M=delta^2 S_M=0 at Y=0), so this is NOT an automatic ghost")
P("  -- but the analytic-Hessian Dirac argument FAILS there and Y=0 requires its OWN degenerate-branch")
P("  constraint analysis. Report OPEN, not PASS and not FAIL. This is the last fundamental field-theory gate.")

P("\n  [OPEN] FULL NONLINEAR RANK on the remaining branches — NOT derived here (no shortcut). Required:")
for s in ["Take the AeST 3+1 constraint system (4 first-class + 4 second-class, PRD 110.044015).",
          "Replace F(Y,Q) -> F_Q^star(Q) + a0^2 J10(sqrt Y/a0) and RE-DERIVE all constraints + the",
          "  complete Poisson-bracket matrix (the modification enters the CONSTRAINT/gradient sector via",
          "  the Y-dependence of F_Y = a0^2 J10'/(2 sqrt Y), even though it is kinetically inert).",
          "Print rank on branches (a) generic Y!=0 (b) Y->0 (c) FLRW (d) static spherical.",
          "Confirm the modified F preserves the degeneracy that gives 4-first/4-second-class => N_phys=6.",
          "The key risk: a Y-dependent F_Y can change the second-class pair structure at Y->0 (the deep-MOND",
          "  zero-acceleration locus) or on the static spherical branch. DO NOT report N_phys=6 until printed."]:
    P(f"         - {s}")
P("\n"+"="*94)
P("Gate A STATUS: PARTIAL — kinetic-sector PASS (modification adds no velocity-Hessian entry, no new field,")
P("target N_phys=6); full nonlinear constraint rank OPEN on all branches. 6 is a TARGET, not a theorem.")
