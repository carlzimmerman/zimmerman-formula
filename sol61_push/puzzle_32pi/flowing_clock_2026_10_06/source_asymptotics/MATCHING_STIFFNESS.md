# Radial stiffness of the flowing-clock MOND candidate

The inner exact ODE system has a fast **oscillatory** radial pair at leading order, rather than a leading real growing mode. Local frozen Jacobians of the exact system at two formal inner profiles corroborate this and show negative real parts. This is a conditioning diagnosis, not a proof that a globally matched branch exists or is dynamically stable in time. The frozen trial data are not exact solutions.

Use x=ln r, n=ln N, b=ln B, w=−V/(H*rN), k=rN'/N, η=c/(3K_EH*²). Work in weak inner deep-MOND fields, nonzero w≈η, k≈L=√(mA), μ=W_aa=a/√(a²+A²/4)>0, and m/(H*²r³)≫1. The exact current identity in REPORT.md permits replacing the lapse equation by zero current once the other two exact stationary metric equations are enforced. Its leading reduction, with the tiny H/flow terms reserved for subleading corrections, is

    b_dot=k(η/w−1),
    (1−μ) k_dot=[η/w−1−μ]k+2rW_a,
    w_dot=(k−b)/(H*²r²w)+terms not enhanced by1/(H*²r²).

Here dot denotes x derivative, not cosmic time. The first line is the original momentum constraint. The second is the stationary zero-current equation and must not be replaced by an imposed scalar-charge constant. The third follows the radial B equation. Terms small in a gravitational mass flux can still be indispensable to the exact scalar equation; these displayed equations are only the leading stiffness block.

At a formal P2 profile a=√[s(s+A)],s=m/r², the momentum-determined flow is w≈η(1+s/A) and k≈ra. Let d=δk−δb. To leading order in the fast sector,

    δw_dot=d/(H*²r²w),
    d_dot=−η k μ δw/[w²(1−μ)].

Thus the frozen leading pair has

    λ_x²=−ω_x²,
    ω_x²=ηkμ/[H*²r²w³(1−μ)]>0,
    ω_x²≈2m/(η²H*²r³) in the deep limit.

The large frequency is logarithmic-radial, not a physical temporal propagation frequency. It grows rapidly inward as r^-3/2. The response criticality μ→0 does not permit setting it to zero: the μ term multiplies the enormous geometric1/(H*²r²) coefficient. Dropping it incorrectly removes the fast pair. No all-regime real-part theorem follows from this leading matrix; lower-order coefficients determine damping.

## Independent bounded exact-Jacobian check

The current main-agent integrate.py response/equations were copied verbatim into matching_stiffness/reference_integrate.py and SHA-pinned. Only those two functions are compiled from its AST; its CLI and batch code are never executed. I independently checked their algebraic B',V',N'' isolation against the full stationary Euler equations before using them as a numeric reference. Probe parameters are H*=A=1,η=.5,m=10^-12, r/r_M=10 and30. Initial formal profiles use the exact P2 inverse and exact leading flow, rather than dropping its0.5% force correction at10r_M.

The finite-difference frozen eigenpairs are approximately

| r/r_M | Fast pair in ln r |
|---|---|
|10|−4.2941±97.7780i|
|30|−4.2774±17.3468i|

Three centered finite-difference step scales give frequencies agreeing within~10^-6 relative. Remaining slow eigenvalues are small, step-sensitive and not classified here. RHS at each trial is nonzero: the matrix is a local stiffness diagnostic, not a linear stability operator about an exact background solution. The leading deep formula gives frequencies89.44 and17.21; its expected finite-a/curvature corrections are visible, especially at10r_M. The exact μ,w formula retains finite-a corrections; lower-order curvature terms can remain significant, so it need not monotonically improve the frequency estimate. Raw matrices, steps, eigenvalues and trial residuals are recorded, not only eigenvalue summaries. A negative control reverses the μ term and is rejected by the necessary imaginary-pair sign test.

## Mathematically informed continuation

The eigenpair supports outward integration: observed fast radial modes decay outward, while reversal makes those same locally damped modes grow inward. This is a bounded diagnostic, not a universal shooting-direction theorem. Prefer a scaled multiple-shooting/collocation BVP, or outward slow-manifold data with verified error, rather than declaring a boundary obstruction from a capped explicit solve. A cosmological inward shot must explicitly control the fast phases and amplitudes.

Several repairs have concrete mathematical targets:

1. Set the exact P2 clock-gradient and forced-flow initial data, then solve the **exact B Euler equation** for B at the initial radius while prescribing the slow-profile V'. This incorporates tiny H²r² and post-Newton corrections that are divided by H²r² in w_dot. It reduces excitation of the fast pair; it is not by itself a full slow-manifold construction.
2. Use cancellation-safe curvature algebra: N−(N+2rN')/B²=N[−expm1(−2b)−2k exp(−2b)], and B−1/B=2sinh b. Near the proposed inner data these terms nearly cancel. Ordinary binary64 subtraction can produce an RHS noise floor far above a strict requested tolerance. The logarithmic variables alone do not repair these subtractions.
3. Evaluate derivative/Jacobian convergence and compare a representative Radau/BDF solve with relaxed but physically justified tolerances or higher precision. Implicit integration does not eliminate unresolved high-frequency oscillations or a noisy RHS. Tolerances must be compared with weak potential amplitudes and accumulated mass-flux/current residuals, not merely solver success.
4. Enforce the actual cosmic vacuum normalization N→1 and outer clock V/(−H*r)→1 through boundary data. A post-hoc lapse renormalization changes the chosen q/ρ_v relation. The formal inner flow differs from the outer flow by η; the transition must be solved, not removed by settingη=1 at the singular health endpoint.

No matching calculation has yet selected A/H*. The next useful deliverable is one converged, residual-controlled exterior continuation or an explicit boundary mismatch that survives solver and initial-data refinement, followed by the conserved regular interior and physical Newton calibration. Existing ODE evaluation caps are failed numerical routes, not mathematical nonexistence results.

Current proof/evidence revisions are separate: REPORT.md/checks.py main_b remains frozen. This stiffness probe has its own contract, source snapshot and run manifests in matching_stiffness/. It performs no peer-folder writes.
