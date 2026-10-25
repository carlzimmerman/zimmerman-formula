# Independent read-only review and disposition

The spherical_review subagent inspected sphere/flux/galaxy implementations against baseline87267ee9d9, then inspected v2/v3, budget and kinematic screen. No shared jobs/Git/files were changed by the reviewer.

- Confirmed Hermitian static-carrier radial Hamiltonian, symmetric one-source Green construction and combined kinetic CN, including valid abs(m) factor-cache reuse.
- Found physical spin need not be conserved by the square collocation nonlinear kick. Its regular r^16 Y16,±16 Gaussian counterexample is now executable in alias_control.py. Jz/azimuth diagnostics were added before v2/v3 galaxy runs. Actual late failures are preserved. Full nf refinement remains mandatory; gates alone do not prove rotational accuracy.
- Found absent finite/integrated budgets in v1/v2. v3 now implements signed radial CN mass/matter-Jz transport, independently tested. analyze.py integrates continuum currents and compares canonical shell inventories. Matter-Jz transport is explicitly not total spin transport.
- Confirmed the +Phi d_rPhi/(8piG) shell-energy boundary sign and the Plummer virial coefficient. budget.py now extrapolates the regular origin; the legacy flux derivative's reporting surfaces avoid endpoint elements. No blanket endpoint/boundary accuracy claim.
- Required errors scaled to each shell's transported energy, not just global energy. analysis.json includes those ratios and RESULT explicitly rejects weak outer currents and late unclosed budgets.
- Required frozen initial Fornax/Leo tension to stay separate from stopped late predictions, and the instantaneous virial screen to stay separate from actual stellar heating. Reporting follows that distinction.

The review concludes the mechanism/closure claim remains incomplete. It does not license a final dwarf remnant, stellar-survival claim, particle/nonparticle ontology, or a literal Khronon bridge.
