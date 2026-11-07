# Fixed-speed transport uniqueness is not coupled uniqueness

Suppose, conditionally, two native continuations both satisfy the transport
criterion in CONDITIONAL_TRANSPORT.md. Denote their wave fluxes, speeds and
sources by mu_i,lambda_i,q_i. Subtract their exact equations and transport
the difference using the first speed:

    partial_t(delta mu)+partial_x(lambda_1 delta mu)
       =delta q-partial_x[(lambda_1-lambda_2)mu_2].      (1)

The speed difference is continuous, so its product with mu_2 is a defined
finite measure. Its derivative need not be a finite measure. A Cantor part
in mu_2 makes this distinction particularly important; even for integrable
mu_2 there is no derivative estimate from its L1 norm alone. Thus the forced
signed-measure theorem cannot directly turn (1) into a bound for
||delta mu|| by the initial difference. The source estimate for each solution
also does not supply a Lipschitz bound for delta q.

Using total variation as a difference metric is especially restrictive:
small translations of a concentrated measure need not be small in total
variation. One could instead compare integrated gradients/clock states in
L1 or compare flows in a weaker measure metric, but this requires a new
coupled stability argument, including the auxiliary temporal response and
all Einstein constraints. No such argument follows merely from applying
the one-solution estimate twice.

The conditional estimate gives a uniform-in-time bound once its hypotheses
are satisfied; it does not construct approximations satisfying them beyond
breakdown. A full native construction still must preserve the constraints,
compactness and metric curvature class and identify the weak nonlinear limit.
Neither the fixed-speed theorem nor the slice modulus countertest establishes
existence, nonexistence, or two distinct native continuations from the same
incoming data. None forces a new physical term.
