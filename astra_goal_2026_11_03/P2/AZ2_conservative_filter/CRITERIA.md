# AZ2 — conservative local filter operator

κ = ½ FITTED; not theory closed

Pre-result. Record: ls KT25–KT28 and AZ1; git log through b811c3f178 and concurrent KT28 completion 55efbef27f; rg variable-width, variable-coefficient, self-adjoint, mass-conserving filter. Nearest KT28 uses an output-radius Gaussian; I1/H4 discuss variable stiffness, not this normalized filter comparison. Scope is a new conservative operator, not a rerun of KT28.

Hypothesis: replace rho_f(x)=integral K_{xi(x)}(x-y)rho(y)dy with (I-div[D(x)grad])rho_f=rho, zero normal flux. D=xi^2 is a prescribed positive field for this first test. This is a resolvent, NOT the same kernel as a Gaussian even at constant width. Integrating the PDE preserves mass; its bilinear form is symmetric positive, and constants are fixed. A later action must vary D if it depends on the gravitational fields: freezing it is not an action derivation.

Decisive finite check on a unit periodic line, N=64: finite-volume flux matrix with face D=0.01*(1+0.5*cos(2pi x)), solve rho=1+0.5 cos(2pi x). The coordinate profile and 0.01,0.5 are synthetic test coefficients, not galaxy fits; no physical length has been selected. Repeat independently on canonical and alt labels (operator algebra independent of a0). Known answer: for constant D=0.01 a Fourier mode is reduced by 1/(1+D*4 sin^2(pi/N)/h^2), tolerance 1e-11. Mass, constant preservation and reciprocity relative/absolute tolerances 1e-11. Positivity min rho_f>=-1e-12. These are exact identity tolerances, not observational pass lines.

MUTATE: replace conservative flux with I-diag(D)*Laplacian. It still fixes constants but must fail mass preservation or reciprocity at >1e-6 on the declared profile. If it does not bite, NO VERDICT. Output results.json (declared before execution), plus a manifest. PASS means survives these operator gates only. All twelve and 96 RQ3 rows remain NOT EVALUABLE; no observed-error threshold is substituted with an identity check. No scan, no imports executing older lanes.
