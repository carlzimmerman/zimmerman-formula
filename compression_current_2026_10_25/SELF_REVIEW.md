# Internal derivation and computation review

Review by the implementing primary agent; not an independent referee report.

1. Source identity: the divergence in the first ACTION display must include
   the time derivative of q(rho), not merely the spatial divergence. This is
   clarified in LINEAR_RESPONSE. The pure-T term follows exactly from material
   continuity. It is not an assigned pump.
2. Hamiltonian derivatives: the density-dependent canonical phase changes
   both alignment and kinetic edge forces. Both are retained, independently
   differentiated, and pass directional finite differences. All positive
   squares are included; no linearized connection alone is used.
3. Mass/charge: U(1) mass is conserved in this nonrelativistic model. The
   nonlinear shift charge includes g2 integral rho². Endpoint-average density
   is required in the midpoint coupling. The continuum and semidiscrete
   identities agree. Continuations explicitly rebase the charge reference
   and report the preceding error bound; energy/work histories are cumulative.
4. Static/reservoir statements: the extra kinetic operator leaves relaxed
   static energy unchanged. It adds no quadratic all-F instability. This
   establishes neither arbitrary-amplitude exterior stability nor a freely
   selected population coefficient.
5. Linear response: I=1/(rho0 k²), G=g2rho0 give determinant
   (Omega²-omega²)(c²k²-omega²)-omega²G²/I. Both roots are positive when
   Omega²>0. The fast branch and slowed material branch are real features of
   the truncation. Apparent low-frequency speed greater than bare c is NOT
   a proof of acausality of all UV completions; the nonrelativistic action
   has no certified relativistic front-speed interpretation in the first place.
6. Mode-rate normalization: radial dV=r²dr absorbs4pi. The compact-source
   outgoing amplitude is -g2 M qdot/(c²r). Its power is
   g2² M² Omega^4 A²/(2c³). Added inertia is g2² D/c²; division by full modal
   energy gives eta/(1+eta)² and optimum eta=1. The numerical3.156e6Myr value
   is tied to the chosen tangent and grid, not a universal formation bound.
7. Numerical evidence: exact field work/far-flux ledgers do not prove time
   or spatial spectral accuracy. Compression runs are short wall-limited
   partial histories, with most energy still near the source. The fast central
   spectrum may be underresolved. They cannot rank coupling efficiencies at
   different final times or establish a populated physical cascade.
8. Solver evidence: Picard nonconvergence and the initial SciPy import failure
   are retained. Newton short-step checks pass; accepted live steps obey the
   explicit root/energy guards. Process completion is never equated with the
   requested physical success. No energy projection supplies a cooling term.
9. Physical closure: g2, its density dependence and consistent kinetic
   completion remain hypotheses. No fit or data theorem derives them from
   the formula. The missing nonlinear cascade has not been demonstrated.

All claims in STATUS and HANDOFF were checked against their result files.
