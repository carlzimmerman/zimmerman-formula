# Cubic-channel self-review

Scope: new `RESULT.md` only, all eight sections. This is author review,
not independent certification. No old source was edited.

Mathematical checks performed directly from the definitions:

- `Q=N_a+2N_b` is preserved by `B†aa` and by every displayed spectator
  channel. A source is not a one-daughter label.
- The two ordered distinct-mode terms yield `2c3 I`; the same-mode
  normalized pair yields `sqrt(2)c3 I`. Fock factorial factors were
  checked before the continuum rate limit. The flat phase-space integral
  gives `Gamma_NR=c3²m sqrt(mdelta)/pi`, agreeing with the relativistic
  width to the declared NR order.
- The source orbital energy excludes `delta`; `d_A=delta+epsilon_A`
  adds it exactly once. This explicit orbital-operator notation was
  clarified during author review before final hashing.
- In the fixed continuum daughter bath, the stimulated gain and loss
  terms cancel their quadratic bath product from the coefficient of
  `n_X`, leaving `Lambda=integral dgamma(1+f_i+f_j)>=gamma_vac`.
  Thus a large equilibrium source population is not protection of its
  initial population information. The fixed-bath factorization and
  continuum kinetic regime are retained as explicit hypotheses.
- The continuum source threshold is the one-bound/one-free threshold,
  not just the two-free threshold. The three Coulomb boundaries are
  exact algebraic implications; approximate labels are not load-bearing.
- Two-level diagonalization gives the same Rabi probability forward
  and backward. A dressed subcontinuum pole is distinguished from its
  bare source. Direct capture closes by the same energy delta when
  there is no receiver.
- The sample `V3 G V4` spectator term respects the charge-three sectors;
  the reverse time ordering vanishes on bare states because it leaves
  fewer than two daughters for the contact. Strong dressing and other
  orders are explicitly retained as unresolved amplitude work.
- Mobile-cluster and fixed-site kernels have different units. Their
  density equations and rate ratios are not interchanged. The capture-
  versus-survival inequality is necessary; the exact write condition
  contains destruction during writing.
- The fixed-generator preparation contrast is `exp[-(a+b)t]`. Combining
  the exact empty-write and contrast conditions gives (24), including
  the direction of its second inequality. Driven and cooperative models
  are expressly outside that statement.
- The detailed-balance partition ratio (25) has the fixed-host volume
  factor `lambda_T^6`; a mobile cluster would require its center-of-mass
  trace and a different factor. No physical Gibbs state is inferred from
  collisionless halo equations.

Proofreading: notation, energy offsets, equation references, displayed
inequality ranges, prose and Markdown were reviewed within the new report.
No manuscript or unrelated source was changed. No compiler is required.
No new numerical simulation, symbolic run, parameter scan or fitted
coefficient was used. Source hashing is provenance only.

Unresolved physical obligations: the actual host and incoming distribution,
all allowed receiver channels, evaluated matrix-element kernels, Markov
validity, the field-to-canonical-label map, state count, and a physical
retention target. No lifetime is certified from an unevaluated kernel.
