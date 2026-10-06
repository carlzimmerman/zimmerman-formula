# Independent mathematical and numerical solar-matching review

Accepted as a **bounded conservative NR experiment**, not a continuum-certified quadrupole or a full covariant solar solution. I reconstructed the actual axisymmetric operator, flux normalization, boundary conditions and physical quadrupole conversion from solver.py before reading the reported result. No blocking implementation error was found in that declared surrogate. The important continuum, source and constraint limitations are preserved by the final report.

## Frozen inspected inputs

- REPORT.md SHA256 f2ee9725a76eba640152881565317d27b0847491efed944d9bcb854426c48315.
- solver.py SHA256 8d76d7184e6ca8297b8afa9f65e6c9ce7338644f2b19ae074332a875cdbf64bf.
- checks.py SHA256 b8bb7933592b72d96fad39fa438cbb45704a3991dd0fe5b7d29a0dec0dc74e24.
- contract.json SHA256 03498f5ae487d9f58d2b62faebbf33f2442f869a14d7508e8a282925a2db67d9.
- PROVENANCE.json SHA256 9f094b4da8f27378f192f511a2edb3f1cfa20d594ce0805c2fce39fd76a6537a.

All five current a manifests were independently validated against the repository root and current hashes: main78/78, fine17/17, and half/QUMOND/source controls9/10 with only the intended false assertion failing. REPORT is an execution input here; RUNS.json is outside it. No author input was modified or author solver run by this reviewer. Development records were read as historical rather than silently promoted to authoritative results.

## Actual force operator and conservative discretization

With zero twin source the projected action gives div[μ∇φ*]=4πGρ and Δφ+=4πGρ, with visible φ=(φ++φ*)/2. The source kernel μ(x(y))=1/(2ν(y)−1), x=y(2ν−1), is not a QUMOND divergence source. Its interpolation/inversion therefore belongs inside the nonlinear constitutive flux, as implemented.

For t=cosθ and no azimuth dependence, multiply the spherical divergence equation by r² to obtain ∂r(r²μφ_r)+∂t[(1−t²)μφ_t]=0 in the annulus. The physical gradient magnitude is sqrt(φ_r²+(1−t²)φ_t²/r²). The radial faces use a radial difference plus interpolated angular derivative; angular faces use an angular difference plus interpolated radial derivative. Both components enter μ. This avoids incorrectly assigning μ from the radial component alone.

The radial conductance is r_face² μ Δt/Δr_center. The angular conductance is (1−t_face²)μ Δr/Δt. Each internal face appears with equal/opposite contributions in adjacent cells, producing the symmetric conductance matrix and exact telescoping flux identity. Angular endpoint conductances vanish at t=±1. At positive sampled μ, the outer Dirichlet condition makes this frozen matrix positive definite. That statement is about a frozen Picard linear solve, not guaranteed nonlinear iteration convergence or continuum uniform ellipticity.

The outer RHS has conductance times φ_bc; the inner source enters with minus its outward-radial prescribed flux, with the sign consistent with a potential −1/r having φ_r>0. Summing the angular radial flux and dividing by two converts the omitted 2π azimuth factor into the full4π mass normalization: (1/2)∫r²μφ_r dt=1. The uniform dipole integrates to zero. Thus the measured radial/outer mass checks test the actual source charge rather than the amplitude of an initialized monopole.

## Constitutive table and boundaries

The rationalized expression for sqrt(1+1/y)−1 avoids subtractive cancellation at large y. The log-PCHIP table spans y=exp(−50)..exp(50), with deep μ=x/4 and UV μ=1 beyond it. No positive artificial floor is imposed. The sampled inverse substitution diagnostic and analytic x_y lower bound justify the chosen branch in their scope; the latter is positive at all declared cutoffs. A table-value test is not a uniform interpolation-derivative error bound. The actual star operator degenerates at zero gradient; positive minimum μ at mesh faces does not exclude a continuous saddle between them.

The inner condition is rmin²μφ_r=1+xe rmin²t. It is a high-acceleration excised monopole with a Newtonian uniform dipole, not a resolved positive-pressure solar interior. Finite-radius inner quadrupole forcing is omitted; the r^-3 fit term can absorb an inner image as well as discretization error and should not be interpreted as an independently measured physical image amplitude. Source-radius sensitivity is a useful empirical control, not a proof of universality across source profiles.

The outer potential is the correctly normalized star external-dominated Green monopole plus uniform xe r t. It is imposed only at the outer surface, while the interior remains nonlinear. Higher far terms and finite-boundary reconstruction errors are not zero by definition; doubling the domain tests their observed impact. The background star and Newton-sum axes and magnitudes are aligned by the declared dictionary, not derived from an actual galactic source model.

## Projection, inner fit and physical Q2

The exact cell weight is ∫cell P2(t)dt=(Δt³_endpoint−Δt_endpoint)/2. Multiplying the weighted sum by5/2 extracts the continuum Legendre coefficient in the refinement limit. It exactly removes any isotropic cell profile; parity removes the uniform l1 component. Independently summing the weights against midpoint P2 samples gives

(5/2)Σ P2(t_i)∫cell P2=(Nt−2)(Nt−1)(Nt+1)(Nt+2)/Nt⁴
=1−5/Nt²+4/Nt⁴.

This is a consistent angular bias, not unity at finite resolution. The final report includes it and changes angular resolution in the refinement cases. Radial and angular errors are not independently separated or rigorously extrapolated.

The harmonic high-force inner l2 solution has A2_star r² plus a possible r^-3 term. The two-column least-squares solve is scaled to avoid disparate column norms. Window spread and retained larger-window fits probe sensitivity, but cannot certify that all nonharmonic/interpolation/discretization contamination is absent. A low fit residual is an empirical description of the extracted discrete profile.

Restoring units, φ*_quadrupole=a0 rM A2_star(r_phys/rM)²P2. The Newton-plus potential for the declared spherical source/uniform field has no l2 part. Visible φ is half φ*, so matching φ_Q=−Q2 r_phys²P2/3 yields exactly Q2=−(3/2)A2_star a0/rM. Both the sign and factor one half are correct. The solar GM is explicitly Claude's AU/year convention, not an independently fitted solar parameter.

## What convergence and controls establish

The final residual reassembles face μ from the final solution and then computes the actual nonlinear algebraic equations, so it is not merely the previous frozen-linear residual. Its global-RHS scaled norm does not estimate local continuum truncation error. Relative potential updates alone likewise do not establish a continuum solution. These diagnostics, conservative mass flux, boundary/source changes and grid refinement jointly support the finite surrogate.

Current main/fine records give Q2≈2.83×10^(−26) s^(−2). Their finest paired refinement changes it by about0.27%; medium/reference differ about0.089%, while matched source-radius/domain tests are much smaller and tighter Picard tolerance is negligible. These are observed changes, not confidence intervals or error bounds. The decreasing minimum face μ under refinement makes the report's degenerate-saddle caveat especially relevant.

Newton and zero-source controls give essentially zero even quadrupole; they check extraction/geometric contamination and source dependence. The zero-source test also benefits from odd reflection symmetry, so it does not independently validate every uniform-field face reconstruction or odd multipole. Specifically the outer angular derivative is averaged between boundary and last-cell values: for the exact uniform field it is xe(R+r_last)/2 instead of xeR. Its tangential ratio is (3+exp(−Δln r))/4, with fractional defect (1−exp(−Δln r))/4 (about2.3% for the100-row zero-source case). This is a consistent boundary truncation term controlled empirically by radius/grid changes; a tiny even Q2 does not certify the whole zero-source field. The mutated half-factor and borrowed-QUMOND value are rejected; the cutoff8/256 examples recompute the boundary background at fixed physical external field. None is a target fit or proof that changing high-force tails can never change the quadrupole.

## Remaining physical arrow

The conservative NR annulus experiment is a real advance over transferring a QUMOND solar number from a spherical law. It remains conditional on the stationary NR source branch and external boundary. In particular it does not establish the full covariant two-metric/common-clock constraints, regular matter interior, continuum solution/error or solar likelihood. The separate finite-k clock obstruction elsewhere is not automatically a verdict on this static sourced branch; neither is force ellipticity a proof of full admission. The report correctly leaves that actual sourced covariant matching problem open and does not attach a statistical exclusion or32π selection to the bounded numerical value.
