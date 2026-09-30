# Bulk finite-mass response — 2026-09-30

Base ea962ad3a. Original 32pi and common-theory goals remain OPEN. Continue the declared isotropic eight-band spectral toy E²=k³/mu+m²; no sheet kernel transfer. All writes sol61_push. No subagents.

First discriminator: derive the exact small-q longitudinal/transverse stiffness coefficients around a uniform nonzero polarization and compare them to a direct momentum/angular integral. Frequency integral is performed analytically. Subtract q=0 curvature symmetrically, preserving the renormalized homogeneous cubic potential. Track trace dimension d=8, occupied count nu=4, mass m=y|p|, vertex factor y².

Route A: Taylor-expand the convergent subtracted integral at finite m. Integrate radial powers with Euler beta functions; derive signs and any exact ratio, with independent radial quadrature. Avoid interpreting a stiffness sign as full covariant stability.

Route B: integrate the full static uniform-mass kernels over physical k and angle. Use stable differences and the squared radial map learned in the preceding massless run. Test orders 256,512,1024 (raise to 2048 only if a declared tolerance fails, recording the change); q/momentum-scale values 0.03,0.1,0.3,1,3,10; m=mu=y=1 for the base run. Verify refinement relative tolerance 2e-4, low-q analytic agreement 1e-3 at q=0.03, positivity at the tested q only. Retain every failure. A separate scale check uses m=0.25,4 and q=m^(2/3), retaining the dimensionally required mu^(1/3)m^(-1/3) stiffness.

A physical response still requires spatially varying backgrounds and a causal UV completion. The critical p² counterterm, absolute vacuum constant, and spectral exponent remain inputs. Even a correct exact stiffness ratio is not a derivation of Lambda/a0². Do not count symbolic identities or refinement alone as a complete theory.

Continuation C after the uniform kernels pass: construct the leading local derivative energy consistent with internal rotational invariance, using separate gradients of magnitude P and direction n. Its coefficients are the fermion-loop contributions only; independent bare derivative operators may change them. Vary the radial hedgehog P(r)n with n=rhat, derive the gradient force and the first far-field correction about P=A/r. Predeclare checks of the radial Euler variation, signs, asymptotic exponents and the gap hierarchy. This is a formal derivative-expansion asymptotic branch, not a global nonuniform determinant or formation/stability proof.

Continuation D: test protection of the critical p² cancellation under linear internal norm-preserving symmetries of the cubic |p|³ potential. Any such symmetry also preserves p². This excludes only that protection mechanism, not scale symmetry, nonlinearly realized symmetry, constrained fields or dynamical criticality. Distinguish the calculated cubic coefficient from the still-independent quadratic counterterm and absolute vacuum constant.
