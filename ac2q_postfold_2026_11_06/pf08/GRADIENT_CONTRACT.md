# PF08 polarization derivative representation

At n1023, the FFT run stops in its initial constraint solve at residual
3.89e-9, above the unchanged 2e-9 tolerance. Hypothesis: updating nodal P
cannot reliably retain tiny high-mode corrections whose derivative is needed
by the constraint. Test an equivalent variable g=P_x+mean(P). Reconstruct P
with the inverse Fourier derivative (zero mode identity), and evaluate P_x
directly as g-mean(g). This changes coordinates, not the physical constraint.

Validate the new Jacobian-vector product and match dense/P-based constraints
on n31/63. Test initial n1023 at unchanged residual tolerance. Preserve all
failed variants; no numerical tolerance relaxation counts as a resolution.
