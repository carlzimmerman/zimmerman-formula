# IO-4: test apparent force-safe fronts against their negative mode

IO-3 eta30 candidates at n256 pass the fraction and frozen-density force gates
but have negative lowest phase Hessian eigenvalue. Never call these stable.
Take the stored large-disk Rj5b and8b eta30 configurations. Normalize the lowest
generalized eigenvector to maxabs1; compare energies at x +/- .01v and the
central second difference. Evolve the lower-energy perturbed state for3000
internal units, no phase clipping or box constraint. h(x) remains in[0,1]
for every real angle. This tests the same angle energy beyond the optimizer's
principal-box restriction; crossing endpoints must not be silently prohibited.

Record independently integrated heat, endpoint phase fractions/forces, actual
phase gradient and lowest Hessian, and the initial negative-mode localization.
This is fixed-density phase evolution, not live mass or baryon preservation.
An exact finite-grid energy-lowering direction refutes energetic stability of
the sampled candidate; it does not exclude all nearby solutions or couplings.
