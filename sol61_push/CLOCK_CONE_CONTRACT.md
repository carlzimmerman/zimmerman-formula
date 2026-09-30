# Spatial-cone audit of the retarded clock kernel

Base 0c4c5778d8056bd619ff6c1055102650126b1f79; previous goal turn was progress. Audit the exact extrapolation of RETARDED_CLOCK_RESULTS.md, G_R=1/[Akin(omega^2-gamma*k^2*B_R)], gamma>0, B_R the isotropic square-root average. Distinguish this extrapolation from an EFT valid only in a bounded real/complex frequency-momentum domain.

Necessary source theorem: for a retarded tempered local response supported inside |x|<=c*t, its Fourier-Laplace transform is analytic for Im omega>c*|Im k|. Check Creminelli et al. arXiv:2512.10843v2 Section 3 Eq.3.10 and Appendix A.3. Only the necessary analytic implication is used.

Mathematical discriminator: continue omega=i*s,k=i*kappa with s>v*kappa. Prove the denominator has a zero in (gamma*kappa^2/2,gamma*kappa^2) for kappa>4v/(sqrt(3)*gamma). This refutes every finite signal cone for the exact extrapolation, without refuting all UV completions or proving a real-momentum growing mode.

Finite checks gamma=1, v={0.2,1}, kappa={3,10,30}; independent quadrature and closed angular integral agree within 1e-10 relative. Root residual tolerance 1e-10 relative to s^2; root must lie in the analytic interval. Verify a concrete c=1 tube point using kappa=4/gamma, v<=1. A formal v=0 heat-kernel benchmark tests positive response at r={1,3,10}, t=1, gamma=1; this is a mathematical limit, not a zero-speed fermion model. Timeout 30 seconds, one thread, no randomness. No full de Sitter audit, observational exclusion, microscopic UV repair or 32pi selection is claimed.
