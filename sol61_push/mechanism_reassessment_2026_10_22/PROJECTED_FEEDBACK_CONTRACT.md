# One-shape kinetic feedback

Prior turn made progress: derivative-weighted prescribed response and sum-rule checks. Restrict the self-consistent field to the finite-A dilation trial potential phi=K delta rho_d / max|K delta rho_d|. Compute S=<phi,K^-1 phi> from that same density variation. The projected dispersion denominator is D(z)=S-Pi(z). This is a single-field-shape Galerkin restriction, not full kinetic closure.

For finite positive sample weights, Pi(z)=sum a_j/(z²-b_j), a_j>0,b_j>0. Verify its feedback spectrum is equivalent to diag(b)+v v^T/S, v_j=sqrt(a_j), hence real positive; no damped finite-sample eigenvalues. Explore the projected coherent response using moment-preserving frequency bins at512/1024 bins, comparing1024/4096 orbit samples. Report binning and sample differences. A decreasing observable can be phase cancellation; do not report a Landau pole from the finite rational function or call binning a physical collision model.
