"""
G3 — FC-8R WEAK FIELD / GRAVITATIONAL SLIP Phi - Psi.  Status: OPEN.
===================================================================
REQUIREMENT: expand Phi,Psi,phi,A_0,A_i,chi consistently; COMPUTE Phi-Psi. Three outputs only:
  PASS    Phi-Psi = 0 from the traceless field equation;
  PARTIAL Phi-Psi nonzero but bounded by an explicit expression;
  FAIL    an unavoidable O(1) slip.
No "AeST normally has Phi=Psi, therefore PASS."
"""
P = print
P("="*94); P("G3  FC-8R weak-field slip Phi-Psi"); P("="*94)
P("  derivable context (NOT a PASS): on the intended branch chi=chi0 => grad_i chi = 0, so the NEW canonical")
P("  scalar contributes NO static spatial-gradient anisotropic stress. The reduced MOND term A(chi)J10(sqrt Y/..)")
P("  has A=const on this branch, so it reduces to a standard AeST-type MOND term with a fixed a0. This makes it")
P("  PLAUSIBLE that FC-8R inherits the AeST two-potential Phi=Psi structure -- but that is inheritance, not")
P("  derivation, and is FORBIDDEN as a PASS by the discipline.")
P("\n  [OPEN] Required and NOT done here:")
for s in ["Write the FC-8R traceless ij field equation with the A(chi)J10(sqrt Y/sqrt A) term retained.",
          "Solve the coupled weak-field system {Phi,Psi,phi,A_0,A_i,chi} to the needed order.",
          "COMPUTE Phi-Psi explicitly and classify PASS / PARTIAL / FAIL.",
          "Check whether the MOND term's anisotropic-stress contribution (via grad phi, the aether A_i)",
          "  cancels in the traceless equation as it does in baseline AeST, or leaves a residual slip."]:
    P(f"         - {s}")
P("\n  Note: full NONLINEAR Phi=Psi is tied to G4 (spherical solution). Keep OPEN until Phi-Psi is produced.")
P("\n"+"="*94); P("G3 STATUS: OPEN.")
