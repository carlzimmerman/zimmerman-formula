# Scalar-dependent clock coupling: a constructive homogeneous probe

Base c941c63d91. This changes the action: replace constant lambda by lambda(q), retain constant M²=1/(8πG), Z>0, the canonical scalar and U=A/q²+Bq². It addresses the constant-coupling assumption behind CLOCK_COEFFICIENT_BOUND.md. No exact coefficient, galaxy matching, observational viability or full perturbative health is established.

## Derive the coupled background first

Write S(q)=3lambda(q)−1 and H=adot/(aN). On flat homogeneous slices the lapse-dependent reduced Lagrangian is

    L=−(3M²/2)S(q)a adot²/N + a³Z qdot²/(2N) −Na³U(q).

Add minimally coupled ordinary matter with density rho and pressure p, conserving rho_dot+3H(rho+p)=0. After lapse variation, in N=1,

    (3M²/2)S H²=rho+U+Z qdot²/2,
    Z(qddot+3H qdot)+U'+(3M²/2)S' H²=0,
    M²S Hdot=−(rho+p+Z qdot²)−M²S'H qdot.

The last equation follows by differentiating the constraint and using the scalar and matter equations; it is not obtained by simply substituting a time-dependent lambda into the constant-lambda acceleration equation. The force proportional to S' means the old potential minimum cannot generally stay fixed through radiation domination.

For a vacuum de Sitter solution q=q*, H=H*,

    H*²=2U(q*)/[3M²S(q*)],
    (S U)'(q*)=0.

At qdot=0 the linearized lapse constraint gives deltaH/H*=−S'/S deltaq, using U'/U=−S'/S. Substituting into the scalar equation gives

    deltaq_ddot+3H* deltaq_dot+m_hom² deltaq=0,
    m_hom²=(S U)''/(Z S), evaluated at q*.

Thus a strict minimum of S U with U,S,Z positive is stable against this homogeneous scalar perturbation. This is a vacuum homogeneous result; it does not establish health of the inhomogeneous preferred-time scalar or its mixing with q.

## An explicit trial with different early and late force balances

Choose dimensionless illustrative units A=B=M²=Z=1, q>0 and lambda(q)=1+ell q, ell>0. This ansatz is assumed, not derived. Then

    W=S U=2/q²+2q²+3ell/q+3ell q³,
    W''=12/q⁴+4+6ell/q³+18ell q>0.

W diverges at both positive-domain ends and is strictly convex, so its stationary vacuum is unique and homogeneously stable. Its root lies strictly between 3^(−1/4) and 1: W' is negative at the first endpoint and positive at the second. The old minimum q0=1 has nonzero curvature-induced force.

For ell={0.1,1,10}, the computed late lambda values are approximately {1.09687,1.86492,8.79547}, with positive homogeneous masses. At fixed radiation density rho=10^8 and qdot=0, the instantaneous zero-force roots have lambda approximately {1.00051,1.00237,1.01104}.

As rho grows, the force-balance asymptotic is q³ approximately 4/(3ell rho), so lambda−1 tends toward zero. This is a stationary-force diagnostic. A time-dependent radiation solution cannot remain at an exactly stationary root while that root moves: its velocity, acceleration and kinetic energy must be included. No tracking trajectory or BBN abundances have yet been computed.

The free ell and the potential parameters remain. The trial does not fix 32π. Moreover q* differs from the static flat-slicing q0: a cosmological-to-galaxy solution must determine the local scalar boundary condition before using any previous a0 calibration. Inhomogeneous scalar mixing, strong coupling near lambda=1 and the causal surface-response obstruction are separate open requirements.

## Verification and source boundary

variable_clock.py passes 16 checks: lapse variation, scalar-force sign, de Sitter stationarity, constraint-reduced homogeneous mass, and four checks at each of three ell values. Exact positivity and convexity above prove the homogeneous claims; finite roots illustrate them. runs/variable_clock records execution provenance. This is self-reviewed.

SciSpace discovery on scalar-dependent extrinsic-curvature couplings returned adjacent scalar-tensor and vacuum-selection models; no returned abstract supplies or proves these equations. A web discovery pass likewise found running-coupling Hořava cosmology but no authenticated matching theorem. No external result is used as a proof leaf and no novelty claim is made.

Next discriminating computation: integrate the coupled radiation-plus-scalar equations with the lapse constraint, including the scalar kinetic density, to determine whether the moving early force balance is dynamically reachable and evolves to the stable vacuum. A successful background trajectory would still require a local galaxy solution and a mechanism selecting the coefficient.
