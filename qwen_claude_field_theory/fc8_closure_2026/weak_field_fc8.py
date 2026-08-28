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
P("  derivable context (NOT a PASS): FC-FINAL has NO sigma, and a0 is constant, so the MOND term is a fixed")
P("  function of Y = a0^2 J10(sqrt Y/a0) -- a standard AeST-type MOND term. This makes it PLAUSIBLE that")
P("  FC-FINAL inherits the AeST two-potential Phi=Psi structure -- but that is inheritance, not derivation,")
P("  and is FORBIDDEN as a PASS by the discipline (the free function is MODIFIED => re-derive).")
P("\n  [OPEN] Required and NOT done here:")
for s in ["Write the FC-FINAL traceless ij field equation with the a0^2 J10(sqrt Y/a0) term retained.",
          "Solve the coupled weak-field system {Phi,Psi,phi,A_0,A_i} to the needed order.",
          "COMPUTE Phi-Psi explicitly and classify PASS / PARTIAL / FAIL.",
          "Check whether the MOND term's anisotropic-stress contribution (via grad phi, the aether A_i)",
          "  cancels in the traceless equation as in baseline AeST, or leaves a residual slip for n=10 J10."]:
    P(f"         - {s}")
P("\n  Note: full NONLINEAR Phi=Psi is tied to G4 (spherical solution). Keep OPEN until Phi-Psi is produced.")
P("\n"+"="*94); P("G3 STATUS: OPEN.")
