# One-shape feedback is stable but misses the observed cold mode

Including feedback through the dilation trial potential produces an internally consistent positive spectrum. However, its largest spectral weight lies near frequency1.34–1.37, rather than the cold fundamental .828 and the corresponding live breathing scale. This single-shape restriction is therefore inadequate for identifying that mode or estimating its damping. A passing numerical audit does not resolve this physical limitation.

## Projected closure

Let K be the second variation of the medium potential energy, mapping a density perturbation to its chemical-potential perturbation. For the normalized dilation trial phi=K delta rho_d/Nphi, the dual density is K^-1 phi=delta rho_d/Nphi. Define

    S=<phi,K^-1 phi>.

Restrict the potential perturbation to a scalar multiple of phi and project the kinetic density response against phi. Self-consistency requires

    D(z)=S-Pi(z)=0.

This imposes feedback only in one field shape. It does not enforce the full spatial integral equation pointwise.

Compute S in two ways: integrate phi times its dual density, and evaluate the positive potential-energy Hessian

    S=integral [R'(q)s²/r² + gamma r²(delta rho)²]dr,
    s=r³rho/Nphi.

The values .2513874086436 and .2513874086646 agree to about8.4e-11 relatively. All quantities use the same finite-A10000 equilibrium and normalized trial potential; no independent-field response has been imported.

## Exact finite-sample safeguard

The sampled susceptibility has the form

    Pi(z)=sum_j a_j/(z²-b_j),
    a_j=2 M (n Omega_j)² |phi_nj|²/(Nsample Q_j)>0,
    b_j=(n Omega_j)²>0.

Writing v_j=sqrt(a_j), the feedback spectrum is that of

    B=diag(b)+v v^T/S.

The determinant lemma gives the denominator1-Pi/S. Since S>0, B is real symmetric and positive definite. Thus its squared frequencies are real positive. Equivalently, for complex lambda=z², Im Pi(lambda)=-Im lambda sum a_j/|lambda-b_j|²; Pi cannot equal real positive S away from the real axis. For lambda<0, Pi<0, so there is no negative root either. Coincident orbital frequencies can retain uncoupled real modes; this does not create decay.

This establishes a property of the finite sampled projection, not a proof that continuum kinetic observables cannot damp. Phase cancellation in a continuum, its initial-value problem and appropriate analytic continuation are different from a finite rational function. A root obtained by naively treating finite-broadening absorption as a damping rate would not supply that continuum analysis.

## Numerical spectrum and coherent response

To make the matrix small, group orbit harmonics into512 or1024 uniform-frequency bins. Each bin preserves total a and the a-weighted b moment. This is numerical compression, not physical collisionality. The sampled unbinned positivity argument above does not rely on binning.

| orbit samples | bins | largest-weight frequency | largest individual weight |
|---|---:|---:|---:|
| 1024 | 512 | 1.33836 | .71345 |
| 1024 | 1024 | 1.33851 | .70038 |
| 4096 | 512 | 1.36756 | .74965 |
| 4096 | 1024 | 1.36737 | .62323 |

Individual weights remain sensitive to binning even when the largest-weight frequency is stable. No single-mode residue is claimed to be converged. The feedback resolvent identity

    v^T(z²-B)^-1 v = Pi/(1-Pi/S)

agrees below1e-12 relatively at three tested complex frequencies. All squared eigenfrequencies are positive and spectral weights sum to1.

The normalized collective-vector autocorrelation is sum_j w_j cos(sqrt(lambda_j)t). This corresponds to a particular excitation of the compressed oscillator representation, not the actual canonical-dilation initial-value problem. For4096 samples/1024 bins, its RMS values are .70246 over t0–10, .61048 over30–40 and .47094 over110–120. The512/1024-bin curves differ by .00707 RMS and .02519 maximum over0–120. No damping fit is justified: this finite conservative representation has persistent discrete frequencies and permits recurrence. These windows cannot be compared directly to the live simulation's radius-response ratios.

## What was learned

A prescribed-potential susceptibility plus positive feedback can be assembled consistently, but one dilation field shape does not recover the cold fundamental. The next useful extension is a multi-shape response matrix with its positive stiffness matrix and independent basis convergence. Merely refining orbit count or fitting the current one-shape response would not fix the missing spatial degrees of freedom.

This checkpoint rules out using the one-shape closure as a calibrated damping explanation for the observed cold mode. It does not rule out the full kinetic mechanism, prove a spectral gap in the continuum, explain initial occupation selection, or provide a complete parent theory. Novelty remains unestablished.

## Evidence

projected_feedback_run completes with five passing checks and a valid manifest. The original per-orbit kinetic samples are pinned inputs. The script reuses only the audited continuum background and trial-potential construction from kinetic_weight.py before orbit sampling. The kinetic sampling sum-rule errors documented previously remain in force. Analytic derivation and interpretation are self-reviewed.
