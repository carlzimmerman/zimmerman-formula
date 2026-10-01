# FGF-025 independent reconciliation

2026-09-30. Reviewed result SHA256
`ca42d5780edfe908280f2a56155ece28250f23ceba8af3fb7831a16e7e21825d`;
final derivation SHA256
`8422512f6d1d2b4b0dcd88ae3a5b7a47de1db5de2220024bfd35f902ae0e206a`.
Declared source/artifact hashes match; actual agent completed. The root
proposed this route and the worker reconstructed/extended it with attribution.
A separate agent audited root's candidate without reading the new worker
proof. This is independent verification, not independent discovery.

Accepted: for each existing smooth compact Q/R hydrostatic slab with positive
rho, lambda, q, J, cs², kinetic coefficients, and w=chi'>0 on the CLOSED
interval, the full fixed-wall quadratic energy is coercively positive.
Differentiating the equilibrium gives Jw''=Mw-C R, R=rho q/lambda.
Product-rule expansion gives

J eta'²+M eta²+C R(w xi²+2xi eta)
 =Jw²[(eta/w)']²+(CR/w)(eta+w xi)²+[J(w'/w)eta²]'.

The endpoint contribution vanishes for Dirichlet eta, since min(w)>0.
Together with the original fluid and potential squares this proves the claim.
The independent audit supplies explicit coercivity estimates using eta/w;
constants depend on the patch and deteriorate near w=0 or changing length.
This removes the previous explicit shortness criterion in this sign domain,
not an existence restriction on solutions. No actual longer domain where
that old bound fails was constructed or computed.

Root independently checked the additional static reduction. With Z=integral
1/lambda and l=q/lambda, L_eta=-J partial²+M+(l tensor l)/Z includes the
positive wall compatibility term. Its positivity follows from the squares,
not U'' alone. The source s_xi=C R xi-l(integral C rho xi/lambda)/Z gives
eta_*=-L_eta^(-1)s_xi; the reduced quadratic subtraction is
-<s_xi,L_eta^(-1)s_xi>/C. These factors and signs are consistent. No dynamic
field is discarded merely by static minimization.

The separate audited turning-point control shows that w=0 is not itself
instability: data B,rho>0,chi=w=0 at an interior point give w'=-T/J<0 and
a smooth transverse crossing. The earlier general short-domain bound proves
positive energy on sufficiently short symmetric induced-wall patches. This
is a different local family, not proof that one entire continued slab remains
stable past its first zero. The weighted formula was not extended through it.

Proof-only evidence, no numeric experiment or new manifest claimed. Independent
report: campaign_fresh_gravity_astra/stage_10/monotone_scale/audit_result.json,
SHA256 `50f0bc95450558faed7fe8eae87c5217cfc2319be90794922447797583506974`.

No literal pointwise constant-vacuum local-scale repair, filtered-MONO metric,
photon coupling, arbitrary-long existence, 3D/nonlinear or observational result
is accepted. Both a0 footings, separate frozen-H/constant reference histories
and MOND Q/R flux remain explicit; no M action is assumed.

Next: audit the first endpoint zero of w on a selected entire continuation,
including boundary traces and coercivity of the nonsingular original form.
A local stable crossing does not close that full-domain question.
