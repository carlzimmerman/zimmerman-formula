# Independent comparison audit of FGF052

Normalized claim: fixed positive coefficients and a compatible smooth positive hydrostatic background, with the exact original C1,1 velocity packet and zero initial field velocities, give exactly hydrostatic protected exterior traces through every fixed B_dagger ell/V for sufficiently large N. On any existing compatible positive whole classical branch, complete mass, first-moment and coupled momentum balances imply a contradiction under the exact signed transfer threshold. Actual upper-horizon closure requires that transfer threshold to be proved for the dynamics.

Primary verdict: **conditional on a named input** — the signed integrated field-momentum budget, equivalently the weighted correlated-force excess, in author equations (18) or (19)-(20). The complete conditional theorem, exact trace result and rigorous but insufficient energy estimate are correct as written. No author correction is required. This verdict must not be read as an unconditional lifespan theorem.

## Target and independence

The frozen raw author proof is `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-052/fgf052_run_001/DERIVATION.md`, SHA256 `3f9b23a5ceba551241db18b93a46e32d4a70974033de9746f96d88fc2b75d628`. Its hash was checked before it was read, and the full raw proof was read before result metadata. The result and external freeze hashes match the coordinator-supplied pins in AUTHOR_EXPOSURE.json.

The reviewer independently reconstructed the critical objects, traces, momentum signs, moment capacity and energy shortfall in INDEPENDENT_DERIVATION.md, SHA256 `377262c0995702b52c0ad38b41552c0dd614061637a96fcd78a544ea991e3a97`, and sent the exact freeze pins before reading any new author or coordinator proof. After that freeze the reviewer read the coordinator momentum note and its separately preserved equality correction; author exposure followed. The final comparison is therefore after-exposure review anchored to a genuinely earlier frozen derivation, not a new blind derivation. The old FGF051 theorem is a pinned dependency, not independently rediscovered here.

## Dependency graph

Actual equations and initial data -> accepted FGF051 local edge theorem -> strictly exterior shrinking subcones -> local uniqueness against stationary hydrostatics -> exact endpoint tuple and potential traces.

Actual fluid/Q/scale equations -> individual momentum densities/stresses and exchanges -> total conservation -> stationary pressure/field stress cancellation at boundaries -> M=M0, P+F=P0 and I'=P.

Exact f integrals and varying-background Taylor bounds -> explicit initial capacity Delta0 and P0 -> positivity I<M0 D_N -> exact signed criterion J<=P0T-Delta0 -> large-N fractional sufficient criterion for B_dagger>15/[8(1-eta)].

Actual energy balance plus endpoint traces -> conserved complete energy -> entropy and interaction lower bounds -> positive energy ceiling H_N -> scale gradient and endpoint bound on a -> Q and scale momentum inequalities -> J<=O(N^-5). This last bound does not imply the required O(N^-6) smallness. No circular use of a desired lifespan estimate is present. All leaves are internal pinned results, direct algebra, analytic inequalities or explicit unproved hypotheses; there is no external literature or computation leaf.

## Obligation matrix

| Obligation and exact locator | Status | Audit evidence |
|---|---|---|
| Actual equations, positive chart and original joins, (1)-(3) | passed | Same C1,1 polynomial, fixed coefficients, pressure, dynamic Q and scale sources |
| Exterior geometric buffer, (4)-(6) | passed | nearest support gap rh, outer strip margin R_i/4, residual cone radius >rh/2 |
| Exact stationarity via uniqueness, (7)-(8) | passed | actual bounded edge characteristics and homogeneous difference estimate |
| Whole-branch comparison | passed | only on common classical domains, finite competitor derivative; no whole speed premise |
| Matter momentum, (9) | passed | continuity produces pressure flux c_s^2 n and force -ng |
| Q/scale momentum signs and stresses, (10)-(11) | passed | -tau pg/C, -sigma wk/C; exchanges +Tk/C,-Tk/C; scale stress -U |
| All fixed-interval balances, (12)-(13) | passed | pressure, both stresses and separate exchanges retained before cancellation |
| Polynomial integrals, (14) | passed | direct expansions give 16/15,16/105,256/315,256/3465 |
| Varying rho and width errors, (15)-(16) | passed | Taylor remainder times nonnegative weights gives displayed factors |
| Exact moment threshold and equality, (17)-(18) | passed | n>0 gives strict I<M0 D_N; equality in J threshold contradicts survival |
| Fractional and finite-N criteria, (19)-(20) | passed | correct strict asymptotic margin and conservative explicit finite-N gate |
| Energy with interaction and both field fluxes, (21) | passed | +np, -np-Tw/C, +Tw/C cancel; endpoint v=p=w=0 |
| Energy ceiling and scale bound, (22)-(23) | passed | e>=-c_s^2 nref, phi>=phi_min, endpoint chi and int k^2 control |
| Q coercivity and momentum estimate, (24)-(25) | passed | W>=g^2/4-a^2/4, Cauchy-Schwarz, scale arithmetic-geometric inequality |
| Actual transfer closure, (26)-(27) | conditional | proved O(N^-5) ceiling cannot certify required O(N^-6) budget |
| Zero-velocity control | passed | force/pressure and Q/scale terms separately balance; threshold not triggered |
| Two a0 choices, fixed histories and evolving work | passed | separate compatible backgrounds; protocol work -T alpha_ref/C |
| Q/RAR/registered M/filtered MONO and physical exclusions | passed | no model substitution or promotion |

## Decisive checks and comparison

For the local uniqueness step, the author need not separately enlarge S to dominate hydrostatic speeds. Formula (7) is integrated along the actual edge characteristics, which FGF051 bounds by v0 S, and the stationary state's derivative is only a coefficient in the difference equation. All backward paths remain in the shrinking exterior cone. This is sound and slightly more economical than the reviewer's auxiliary S_h construction.

The author uses I=int(x-a)n whereas the independent proof uses a moment centered at x*. The available upper capacity is identical: author Delta0=int(b-x)rho equals reviewer (b-x*)M-I0. Thus the shared limiting coefficient 15/8 is not an artifact of the origin choice. The explicit rho'' errors improve the reviewer O estimates and have correct constants: multiplying the Taylor remainder H2 ell^2 y^2/2 by V ell gives 8H2 ell^3V/105; multiplying by V^2 ell/2 gives 64H2 ell^3V^2/3465. The interval capacity error H2 R_N^4/3 follows by integrating (R_N-z)z^2.

Field signs were independently reconstructed without appealing to the author's conclusion: (gB-W)_x=gB_x+Tk, so -tau(pg)_t/C plus its Q stress gives ng+Tk/C; the scale stress gives -Tk/C. Their sum cancels matter -ng. At the boundary pressure is generally unequal, and only its difference plus the combined hydrostatic field stresses cancels. A claim that each boundary stress vanished would be false; no such claim is made.

The author correctly uses strict positivity to admit equality at the exact finite-N obstruction threshold. This avoids the coordinator original's overly broad ancillary equality statement. The coordinator original and its corrected scope are separately pinned in ROOT_COMPARISON_AUDIT.md; the author proof did not need that correction.

For energy, H_N bounds the sum of positive kinetic/field terms because e(n)+n phi is bounded below by -c_s^2 nref D_N+M0 phi_min. Gauge constants cancel. Fixed endpoint chi and int k^2<=2C H_N/J give |chi|<=chi_bd+sqrt(2C D_N H_N/J), hence uniformly bounded a. The Q estimate is

    |Q| <= sqrt(2tau H_N/C)*sqrt(4C H_N+A_N^2D_N),

and the scale arithmetic-geometric bound is |K|<=sqrt(sigma/J)H_N. The latter is sharper than the reviewer's conservative factor 2 but consistent. All coefficient dimensions and the factor 1/C agree. Since H_N has a positive N^-1 leading kinetic term and P0 is N^-2, the explicit bound cannot close the fixed fractional criterion; this conclusion concerns the estimate, not actual transfer size.

## Commands, evidence and remaining implication

The author verifier was read before execution and performs only filesystem reads, SHA256 and contract checks. Executed:

    python3 deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-052/fgf052_run_001/verify_metadata.py
    python3 campaign_fresh_gravity_astra/stage_39/independent_audit/verify_metadata.py

Both returned PASS. All ten ancestry pins and author source/artifact/freeze pins match. These checks establish byte ancestry and contract consistency, not a machine proof. Zero mathematical executable computations, numerical tests or external sources were used. Six failed shortcuts remain in the author's frozen FAILED_ESTIMATES.md, including the one-power energy shortfall. No frozen source was edited.

The smallest unresolved implication is a non-circular estimate of

    -(1/C) int_0^T int_a^b (tau phi_t phi_x+sigma chi_t chi_x) dx dt

at the signed threshold P0T-Delta0, or a strictly sufficient fractional version, on actual candidate whole classical continuations through the fixed comparison horizon. Exact stationarity, total momentum and initial zero field velocities alone do not supply it. The strongest safe result is the exterior trace theorem plus complete conditional finite-interval obstruction and the explicit nonclosing energy bound. The cheapest new check is a dynamical estimate using zero initial field velocities or a favorable signed cancellation of the core products; merely repeating unsigned energy would not advance the missing implication. No endpoint, whole-core existence or physical theory closure follows.
