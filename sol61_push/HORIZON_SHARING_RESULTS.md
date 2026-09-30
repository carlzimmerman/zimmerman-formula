# Horizon sharing: the missing transfer to physical dynamics

Original goal OPEN, including the definition-dependent r_H²Lambda question. Contract and base: [HORIZON_SHARING_CONTRACT.md](HORIZON_SHARING_CONTRACT.md). This audits a new proposed mechanism rather than rerunning the older entropy routes. It does not rule out every thermodynamic approach.

## Source authentication and exact boundary

Keith Brodie, *The Radial Acceleration Relation from Two-Horizon Entropy Sharing with Zero Free Parameters*, [Zenodo 18677307 v1](https://zenodo.org/records/18677307), published 18 February 2026, PDF dated 17 February. Inspected Sections II–IV and VII. The proposed angular weight produces s=cH/6 and f(a)=a/(a+s). The text explicitly leaves its angular overlap and covariant completion unproved. Its claimed observational fits were not reproduced here. A dimensional inconsistency in printed temperature factors does not affect the audit's use of the stated acceleration law.

Web PDF retrieval failed; the public PDF was read via temporary download and pdftotext. SHA-256: 56fc7e4d0038c52270bb59330f551938dd38177a0f5a2ecfc23d06d2551d1697. No PDF or extracted text was added to the repository or a source cache. Primary mechanism overlap: conditional phenomenological proposal, not an authenticated derivation of 32pi.

## First obstruction: no acceleration coefficient selection

Work in the radius conventions of HORIZON_8PI_AUDIT.md. If a0=cH/6 and Omega_Lambda=Lambda c²/(3H²), algebra gives

Lambda c⁴/a0²=108 Omega_Lambda.

The target requires the additional condition Omega_Lambda=8pi/27. In flat pure de Sitter the coefficient is 108. None of the angular integral or sharing law selects the needed cosmological density parameter or produces vacuum curvature from the same equation.

If one additionally imposes r_H²Lambda=8pi with r_H=c/H, this law instead gives Lambda c⁴/a0²=288pi. The two goal identities together require a0 r_H/c²=1/2, rather than 1/6. If r_H means a density length, it is a different radius and the earlier dictionary applies. No undefined radius is silently renamed.

## Second obstruction: entropy state-function integrability

Take the proposed differential rule omega=eta f(a)dA as a mathematical hypothesis on independent state coordinates A,a, with eta>0 and s>0. Its exterior derivative is

d omega=eta s/(a+s)² da wedge dA,

which is nonzero. A rectangle taking area from zero to A at a=s, then back at a=2s, has integral -eta A/6. Thus omega is not the differential of a state entropy on this two-dimensional state space.

If an entropy S=eta A f(a) is intended instead, its differential contains the additional term eta A f'(a) da. Alternatively, a fixed-a process or an explicit non-equilibrium entropy-production law may be considered. The present result does not forbid those alternatives; it identifies the missing condition when both variables vary. Holding a fixed locally cannot establish a universal state function or its dynamics.

## Third obstruction: null curvature does not give a trace-only covariant completion

Assume a nonzero scalar f is fixed across each local horizon patch, so the modified null relation is

f R_mu_nu k^mu k^nu=8pi G T_mu_nu k^mu k^nu for every null k.

An algebraic tensor lift would have f R_mu_nu+Psi g_mu_nu=8pi G T_mu_nu. With conserved minimally coupled matter, contracted Bianchi requires

partial_nu Psi=W_nu=-R_mu_nu nabla^mu f-(f/2)partial_nu R.

This one-form must be locally exact. It is not an identity for an acceleration-dependent f. Here is an explicit geometric check using actual static-observer proper acceleration, not an arbitrary Killing-generator rescaling:

ds²=-N²dt²+dx²+dy²+dz², N=exp(x)(1+y²),

a=|grad log N|=sqrt(1+4y²/(1+y²)²), f=a/(a+s).

In the stated Ricci convention, R_tt=N laplacian N, R_ij=-partial_i partial_j N/N, and R=-2 laplacian N/N. Direct Christoffel contraction independently verifies them. At y=1,

partial_y W_x-partial_x W_y=-s/[sqrt(2)(sqrt(2)+s)²] !=0.

No scalar Psi has this gradient on a neighborhood of that point. Therefore the trace-only lift needs extra tensor terms or an additional integrability constraint on its solutions. This is not a theorem that no solutions exist: it refutes automatic Bianchi closure for arbitrary states under the stated lift. A scalar/clock action or a non-equilibrium construction could add the required terms and must then be tested in its own right.

## Fourth obstruction: a universal first-derivative inertial action is missing

In one spatial dimension, for any sufficiently differentiable local L(q,v,t) with v=qdot, its Euler–Lagrange expression is

E=L_vt+v L_vq+a L_vv-L_q, a=qddot.

At fixed q,v,t, this is affine in a, so partial²E/partial a²=0. On the positive-acceleration branch the proposed inertial response is m a²/(a+s), whose second derivative is 2m s²/(a+s)³>0. Thus it cannot equal the off-shell Euler–Lagrange inertial expression of a universal first-derivative kinetic action with standard coupling to an arbitrary unmodified force. This is a direct calculus proof, separately self-reviewed; the computation's elementary mass-multiplicativity check is not its proof.

Restriction: equivalent on-shell equations are a weaker question. For a fixed one-dimensional force, solving the algebraic response and redefining a potential can reproduce trajectories with a position/velocity action. That changes the force prescription and does not establish the claimed universal modified-inertia action. No impossibility of all dynamically equivalent actions is asserted.

Acceleration-dependent higher-derivative, nonlocal or extra-field actions remain possible. Their stability, conservation and behavior on noncircular trajectories are new obligations. A circular-orbit algebraic relation alone does not supply them. Modifying a geometric entropy coefficient also does not by itself modify the minimally coupled point-particle action.

## Evidence, corrections and source transfer

The corrected symbolic run passes 20/20 checks. Both manifests validate with input/output hashes. The first run failed one expected-coefficient check: the hand-entered curl coefficient was too large by two. The actual geometric computation and a separate derivative of W_x agreed on the smaller coefficient. The corrected script changes only that expectation. The nonzero-curl conclusion was unchanged; the first input and failed output are retained. No tolerances were changed.

Self-review verdict: the state-function and trace-only closure obstructions are proved under their stated assumptions; the particle-action restriction is exact for a universal first-derivative off-shell inertial expression with unchanged force coupling. The original proposal's transfer is incomplete. No independent reviewer was used. Proofreading covered these new documents, with the numerical normalization repair preserved separately.

Primary comparison: [Jacobson, gr-qc/9504004v2](https://arxiv.org/pdf/gr-qc/9504004), 6 June 1995, pp. 3–5. His heat and temperature use the same boost generator and scale together; the null-curvature relation is completed using matter conservation and an integration constant. Our new variable coefficient requires the separate integrability check above. We do not identify generator normalization with proper acceleration or claim a contradiction from rescaling it.

Additional source checked: [Arata, Liberati and Neri, arXiv:2603.28851v1](https://arxiv.org/html/2603.28851v1), Sections 5–6 and discussion. Their aether horizon balance includes an independent aether contribution. This prevents assuming that a preferred-clock completion automatically retains a pure area entropy. It does not itself calculate the MOND coefficient; its full horizon charge derivation was not reproduced here.

The useful next step is an explicit matter/clock action and a microscopic entropy calculation, not choosing an angular weight to hit the target. The local wall route offers a separate executable continuation: test whether an additional discrete symmetry forbids its rotation-singlet mass while allowing the induced mass triplet. That would advance a real unprotected dependency; it would still leave critical matching and vacuum stress to derive.
