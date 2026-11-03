# AZ17 — NO VERDICT under frozen convergence gates

κ = ½ FITTED; not theory closed

The first N256 solve reaches the frozen 4000-iteration limit, despite projected gradient 1.5435e-6 and virial residual .00021264. Optimizer success was explicitly required, so it fails that gate. It is not silently discarded because the refined results look better. Seventeen of eighteen checks pass. No physical exclusion or accepted equilibrium is inferred from this numerical failure.

The N512, N1024 and larger-box solves report optimizer convergence. At N1024, F=.08664891583828181, W=-.3465909055109731, energy=-.2599419896726913, rms radius=1.5088337963616631 in synthetic G=M=256lambda=1 units. Virial residual is 1.37275447e-5 against .005; projected gradient 9.24988556e-7 against1e-5. Mesh energy/radius relative differences are 2.6316e-5/2.7475e-5; boundary differences4.3993e-5/4.6006e-5 against .01. These finite-resolution statistics remain provisional because the full frozen acceptance set did not pass. They do not certify stability or global minimality.

The exact uniform-sphere binding control returns -.12 for radius5. The normalized-energy gradient finite-difference relative error is1.6066e-8; MUTATE omitting the same-shell derivative factor2 produces .0115354 error and is rejected. The refined energy lies below the independent Gaussian variational upper bound -.22505271627185458. No physical coefficient was fitted to obtain these synthetic values.

## Discretization and derivative audit

For uniform-density shell [a,b], let D=b³-a³, mass m, and Mprev be interior mass. Direct integration of -4pi G integral rho M(r)r dr gives W_shell=-G[A m Mprev+B m²],

A=3(b²-a²)/(2D),
B=3[(b^5-a^5)/5-a³(b²-a²)/2]/D².

Thus dW/dm_i=-G[A_i Mprev_i+2B_i m_i+sum_{j>i} A_j m_j]. This includes interactions and same-shell energy exactly for the discretized density. Gradient energy is sum4pi r_face² (delta psi)^4/(delta r)^3, with half-cell distance at the fixed-zero outer boundary. The center face has zero area and no flux.

For u>=0, S=sum V u^4 and psi=u S^(-1/4), so mass is one. If g is the unnormalized energy gradient with respect to psi, the normalized-coordinate gradient is S^(-1/4)[g-V psi³ sum(g psi)]. The gradient and exact-shell controls independently test these factors. Normalization leaves an amplitude null direction; a future optimizer formulation should remove it explicitly rather than merely extending iteration counts after seeing this result.

The field has not been evolved, coupled to baryons, or calibrated to a physical mass or lambda. Finite-box, radial-only discretization does not prove a weak-solution existence theorem. a0 cancels, so both footing labels carry the same NO VERDICT. Full empirical rows are NOT EVALUABLE. After six P4 lanes, move to another problem. A future continuation must freeze a mass-constrained optimizer with its null direction removed and independent initial conditions before new graded results; then test time evolution and baryonic contraction. No retuning or extra run is hidden here.
