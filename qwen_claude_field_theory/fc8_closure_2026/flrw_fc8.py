"""
Gate G — FC-FINAL COSMOLOGY / FLRW PERTURBATIONS.  Status: OPEN (with derivable framing).
=========================================================================================
REQUIREMENT: use F_Q^star(Q) to reproduce the established AeST cosmology (CMB + matter power at linear
scales for suitable K(Q)); do NOT make a0 responsible for dark energy (a0 is CONSTANT in FC-FINAL).
Derive the full quadratic FLRW system; require K_i>0, c_i^2>=0 for EVERY propagating mode; check the
NONDYNAMICAL AeST mode separately (low-k, Hamiltonian sign flips at k_*, 2109.13287).
"""
P = print
P("="*94); P("Gate G  FC-FINAL cosmology / FLRW perturbations"); P("="*94)
P("  framing (FC-FINAL removes the FC-8R cosmology headache):")
P("   - a0 = CONSTANT => NO sigma field, NO potential-domination question, NO a0(z) drift to certify.")
P("   - the MOND term a0^2 J10(sqrt Y/a0) is O(Y^{3/2})=O(delta^3) on FLRW (Y=0 background) => it does NOT")
P("     enter the quadratic FLRW action (Gate 0 A3). So linear cosmology is PURE AeST with K(Q)=F_Q^star.")
P("   - dark sector / dark energy is carried by the AeST Q-sector K(Q), exactly as in published AeST.")
P("\n  [OPEN] Required and NOT done here:")
for s in ["Solve the FLRW background with K(Q)=-2Lambda+K2(Q-Q0)^2 (or a re-frozen cosh/exp K(Q), A&A 676 A100).",
          "Derive the FULL quadratic scalar system (metric+aether+phi); require K_i>0 and c_i^2>=0 per mode.",
          "Check the AeST NONDYNAMICAL low-k mode: Hamiltonian sign vs wavelength, the k_* transition",
          "  (2109.13287). FC-FINAL inherits it; NOT closed by the propagating-mode check.",
          "Reproduce the AeST CMB + matter-power behavior at linear scales (PRL 127.161302).",
          "Confirm the a0^2 J10 term stays sequestered (O(delta^3)) through the epochs of interest,",
          "  so the galactic MOND modification does not leak into linear cosmology."]:
    P(f"         - {s}")
P("\n  NOTE: a0^2 = kappa^2 G rho_DE is NOT tested here -- it is a cross-sector hypothesis, not part of the")
P("        FC-FINAL action. FC-FINAL predicts a0=const; whether observed a0 tracks rho_DE is a separate test.")
P("\n"+"="*94); P("Gate G STATUS: OPEN (linear cosmology reduces to AeST-with-K(Q); full stability + k_* mode OPEN).")
