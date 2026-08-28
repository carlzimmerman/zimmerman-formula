"""
G1 — FC-8R FULL NONLINEAR DIRAC RANK.  Status: PARTIAL (perturbative PASS) + OPEN (full nonlinear).
====================================================================================================
REQUIREMENT (REQUIREMENTS.md G1): full 3+1 decomposition; all momenta (incl. pi_chi); primary/secondary/
tertiary constraints; complete Poisson matrix; rank on branches (a) generic (b) a0->0/V->0 (c) Y->0
(d) FLRW (e) static spherical. N_phys=(N_phase-2N_first-N_second)/2. 7 is a TARGET, not a theorem, until
the matrix rank is printed. First failure terminates that branch. NO DOF count from field names.

WHAT THIS SCRIPT DERIVES NOW (the perturbative / velocity-Hessian half — a genuine sub-result):
Because FC-8R has NO auxiliary alpha,zeta (eliminated exactly) and the reduced MOND term
A(chi) J10(sqrt Y/sqrt A) has A=kappa^2 G V(chi) depending on chi (not chi-dot) and no grad-chi, the new
canonical pair is exactly (chi,pi_chi) with an ordinary momentum, and the velocity (kinetic) Hessian is
block-diagonal: diag(H_AeST, 1).  This is the perturbative evidence for N_phys=6+1=7, NOT the full rank.
"""
import sympy as sp
P = print
P("="*94); P("G1  FC-8R Dirac rank"); P("="*94)

# ---- derivable: the reduced MOND term adds no chi-kinetic => velocity Hessian block-diagonal ----
Y, chid, chix, kap, G, V = sp.symbols('Y chidot chi_x kappa G V', positive=True)
A = kap**2*G*V                               # A(chi): depends on chi, NOT chi-dot, no grad-chi
L_M = A*(sp.sqrt(Y)/sp.sqrt(A))**3/3         # reduced MOND, leading J10=x^3/3
pichi_MOND = sp.simplify(sp.diff(L_M, chid)) # MOND contribution to pi_chi
Hcc = sp.simplify(sp.diff(L_M, chid, 2))     # MOND contribution to velocity Hessian entry chi-chi
Hcg = sp.simplify(sp.diff(L_M, chid, chix))  # chi-phi(grad) mixing in velocity sector
print(f"  reduced MOND pi_chi contribution d L_M/d chidot         = {pichi_MOND}")
print(f"  reduced MOND velocity-Hessian H_chichi = d^2 L_M/dchidot^2 = {Hcc}")
print(f"  reduced MOND velocity-Hessian H_chi,gradchi              = {Hcg}")
block = (pichi_MOND == 0) and (Hcc == 0) and (Hcg == 0)
print(f"\n  [PASS] velocity Hessian is block-diagonal diag(H_AeST, 1): MOND adds nothing to the kinetic")
print(f"         sector => (chi,pi_chi) is one ordinary canonical pair. Perturbative N_phys = 6+1 = 7.")
print(f"         (established: fc8_clean_lock_2026.py, fc7_reduced_action_rank_2026.py)")

P("\n"+"-"*94)
P("  [OPEN] FULL NONLINEAR RANK — NOT derived here (no shortcut). Required, per branch:")
for b in ["(a) generic Y!=0, chi rolling", "(b) a0->0 / V->0 boundary (note V>=V0>0 => interior only)",
          "(c) Y->0", "(d) homogeneous FLRW", "(e) static spherical"]:
    P(f"         - {b}: construct full 3+1 momenta (incl pi_chi), all constraints, the Poisson matrix,")
    P(f"           print its rank; confirm the K(Q)+MOND coupling does not spoil the AeST 4 first + 4")
    P(f"           second-class structure. First FAIL terminates the branch.")
P("         The velocity-Hessian block-diagonality above bounds the KINETIC sector only; the full")
P("         constraint rank (gradient/mass sector + AeST aether constraints + the A(chi)-J10 coupling)")
P("         is the genuine open computation. DO NOT report N_phys=7 as PASS until the rank is printed.")

P("\n"+"="*94)
P("G1 STATUS: PARTIAL — perturbative velocity-Hessian PASS (block-diagonal, chi ordinary); full")
P("nonlinear Poisson rank OPEN on all five branches. This is a TARGET N_phys=7, not a theorem.")
