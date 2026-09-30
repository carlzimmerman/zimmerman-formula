# Horizon-sharing transfer audit — 2026-09-30

Base: 0b629b9745b21299389851d5bc5daa22e93d3683. Previous goal turn is progress: local wall operator and horizon-radius audit were committed and pushed. Current sol61_push revalidated clean before this route. Original target and added undefined-r_H question remain OPEN; prior clarification has not received an answer.

New source: Brodie, Zenodo 18677307 v1, PDF dated 17 February 2026. Source question is whether its entropy-sharing rule can provide the missing exact coefficient and a mathematically complete transfer from horizon thermodynamics to inertia. Prior standard Jacobson/Verlinde audits are not rerun.

Retain the source's f(a)=a/(a+s), s=cH/6 as a hypothesis. Three mathematical checks:

1. Angular integral and source-to-target dictionary: with Hubble radius c/H, compute Lambda c^4/a0²=108 Omega_Lambda, and the condition on Omega_Lambda required for 32pi. Also test simultaneous r_H² Lambda=8pi under that explicit Hubble definition. No cosmological parameter is fitted.
2. Entropy integrability: on independent state coordinates (A,a), check whether the one-form eta f(a)dA is exact. Fixed-a variations are allowed but do not establish global state-function integrability. Compute a closed rectangular path and the missing term if S=eta A f(a).
3. Covariant integrability of the null equation f R_kk=8pi G T_kk. For conserved minimally coupled matter, a trace-only tensor completion f R_mu_nu+Psi g_mu_nu=8pi G T_mu_nu requires an exact divergence one-form. Test a fully specified static lapse N=exp(x)(1+y²), metric diag(-N²,1,1,1), and f built from its static observers' actual proper acceleration |grad log N|. A failed closure is a necessary additional differential constraint or missing tensor contribution, not a proof that the field equations have no solutions.

Arithmetic: exact real symbolic derivatives, and an independent full-Christoffel computation for Ricci components and scalar. Natural units and one coordinate length unit for the counterexample. A point at y=1 has positive finite acceleration. Avoid treating a Killing-generator rescaling as a change in proper acceleration: no such claim is tested.

Resource bounds: 30 seconds, one process, numerical-library threads=1, <=1 MB logs. Primary sources authenticated before source transfer. Finite code success verifies implemented identities; it does not produce an action, matter dynamics, Lambda or stability. The central closure obstruction is proved by the nonzero exterior derivative of the specified one-form.
