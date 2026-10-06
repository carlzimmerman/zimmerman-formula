# Independent tensor and force audit

Accepted the specified exact tensor block and ordered UV force limit. Inspected REPORT.md SHA256 2bdefefc31b89f550ca5b050f0e6b8b5759c52c220480b8063057cfc4b09eac2 and checks.py 90cf73647478cbe3eee85463058e97e5e5e564c9f89cd7ff038f04b52aca0ab4. This is an independent algebra reconstruction, not a sourced low-momentum galaxy calculation.

The original action has two canonical real scalars and F=M-xi sum(phi_a²). On the circular zero-stress background F=M-2xi A/t. In the volume-preserving TT parametrization the trace of extrinsic curvature stays 3H, so its homogeneous Fdot boundary term has no tensor velocity. The traceless extrinsic and spatial-curvature terms both have coefficient F/8 with opposite kinetic/gradient signs. This independently yields qT=F, unit tensor speed and damping 3H+Fdot/F. The exact EdS damping, homogeneous solution and WKB amplitude agree. Tensor WKB only needs the variation rates of F, which has no internal phase oscillation; it should not inherit the stronger scalar-source rotation hierarchy.

Early positivity follows without a numerical scan: F>0 on t>=ti implies alpha=2xi A/M<ti. Therefore the fractional later Planck change is less than ti/tf. Requiring positivity on the entire t>0 exact EdS branch instead forbids nonzero A. These conclusions depend on retaining that same history and action, not on extending EdS across physical radiation domination.

For the frozen local UV source, scalar variation gives Laplacian(delta phi_a)=-F_a deltaR/2. Hence Laplacian(deltaF)=-S deltaR/2, S=sum F_a². The metric trace is F deltaR=rho+3 Laplacian(deltaF), giving (F+3S/2)deltaR=rho. The 00 equation is 2F Laplacian(Phi)=rho+Laplacian(deltaF), while spatial shear gives F(Phi-Psi)=deltaF. Combining them reconstructs both Poisson coefficients and the lensing sum exactly.

The extra force relative to the lensing coupling is (2F+4S)/(2F+3S), bounded between one and four-thirds for positive F,S. Inverting this factor gives the reported lensing/locally calibrated force ratio between three-fourths and one. Uniformly recalibrating Newton's constant does not create additional material density. Time/environment dependence and another response regime are rightly not identified with the same calibration.

The ordered source limit is essential. Individual F_a rotate at Omega even though F does not, so neglecting scalar derivatives/mass in the static equations needs p much larger than Omega and the other stated rates. This hierarchy has not been shown at galaxy scales. The report correctly does not import the UV force enhancement into its low-p sector.

The sourced relative scalar rows also reconstruct directly. With delta chi=chi0(u+iv), 2 chi0dot/chi0+3H=(1+2i omega)/t. Linear Klein-Gordon variation supplies chi0dot(Psidot+3Phidot)-2xi R chi0 Psi-xi chi0 deltaR. Dividing by chi0 yields the displayed radial/phase equations and opposite rotation mixing signs. Their frozen probe determinant gives the slow p²/(2Omega) frequency, whose own adiabatic condition is stronger than p>>H. These rows do not close the Einstein/dust constraints or the finite-scale force.

All four manifests independently validate against current inputs/outputs. No blocking correction was found. The full sourced low-p response, scalar stability, abundance and original 32pi selector remain unproved.
