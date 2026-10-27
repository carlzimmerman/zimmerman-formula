# Formation/transport normalization gate — independent scoped review

Observed HEAD: `7508a42da0fd2ccbf3b28c5882769e2856302cf2`.
Review provenance: independent reading/reconstruction by `final_physics_gate`; root independently checked the center expansion, interior rescaling, dimensions and normalization algebra; see AUDIT.md. No shared research files edited, external theorem imported, numerical rerun or broad search performed.

**Normalized claim:** Do the stated logarithmic hydrostatic phase, stable core mode and reciprocal outgoing-wave transport imply `kappa=1/2` at a fixed physical vacuum energy density?

**Primary verdict: incomplete, with the smallest missing implication `A = rho_Lambda c^2/(4 pi xi4^2)`.** The existing reports accurately disclose this gap. If instead asserted as a universal consequence of the supplied closure, the implication is refuted by the free-A family below.

## 1. Exact static obstruction

Write `u_Lambda=rho_Lambda c^2>0`. For the specified active barotrope,

    P = P_ref + A ln(rho/rho_ref),  A>0,
    theta=rho_c/rho,
    r=xi sqrt[A/(4 pi G)]/rho_c,
    theta''+2theta'/xi=1/theta.

With the quarter-density convention `theta(xi4)=4`,

    Sigma=rho_c r_quarter=xi4 sqrt[A/(4 pi G)].

Define `a_eff=2 pi G Sigma` and `a_eff=kappa_eff c sqrt(G rho_Lambda)`. Exactly,

    kappa_eff^2 = pi xi4^2 A/u_Lambda.

Thus `kappa_eff=1/2` is equivalent to the missing coefficient relation above. The reported `xi4=5.84477267596` gives `A/u_Lambda=0.002329458`; this numerical approximation is inherited evidence, not independently rerun here. The algebra does not require that approximation.

The mode outlet is

    L=mu(qdot^2-omega0^2 q^2)/2 + L_chi + qdot integral J chi.

At `qdot=chidot=0`, its reaction force `-integral J chidot` vanishes. With regular, finite-energy, no-source static mediator boundary data, `chi=0` is admissible. Consequently the outlet preserves the equilibria of the assumed core energy; it supplies no equation for A. The half-line realization gives `mu qddot+Gamma qdot+mu omega0^2 q=0`, `Gamma>0`, and damps every stable mode regardless of A. It therefore cannot distinguish A from 4A: both have the same dimensionless hydrostatic shape and contrast-four stability problem, while their surface densities and effective kappas differ by a factor two. This compares two allowed parameter choices at one fixed u_Lambda, not two solutions of an action whose A has already been independently fixed.

Even a future exact proof of nonlinear formation and attraction for each admissible A would not by itself calculate this free constitutive coupling. It would establish formation conditional on A. A microscopic relation, or other independently specified parameter-selection principle, is required.

The field parent reinforces this: additive `V0` changes gravitating vacuum energy while leaving its local scalar activation threshold unchanged. The current assumptions contain no identity tying this free vacuum term to A.

## 2. Supplementary exact conditional homology lemma (self-derived; independently reconstructed by root)

Assume spherical Newtonian self-gravity, isotropic barotropic stress, no baryons/anisotropy/external tidal force in the equilibrium equation, and a single differentiable EOS P(rho). Suppose an open interval of central densities admits a common smooth cored shape

    rho(r)=rho_c F(r/r0),
    F(0)=1, F'(0)=0, F''(0)<0,
    rho_c r0=Sigma_* >0.

Regular-center expansions give

    rho'(r)=rho_c F''(0) r/r0^2+o(r),
    M(r)=4 pi rho_c r^3/3+o(r^3).

In `P'(rho)rho'=-G M rho/r^2`, divide by r and take the center limit:

    P'(rho_c) rho_c F''(0)/r0^2 = -(4 pi G/3) rho_c^2,
    P'(rho_c) = -4 pi G Sigma_*^2/[3 F''(0) rho_c] = A/rho_c,
    A=-4 pi G Sigma_*^2/[3F''(0)]>0.

Because rho_c ranges over the open interval, integration gives `P(rho)=A ln(rho/rho_ref)+B` on that interval. This establishes a necessary EOS for an EXACT common homologous shape with constant column, not a theorem that every family with constant column must be logotropic. Varying shape, anisotropic stresses, baryons, nonlocal constitutive response and additional forces evade these premises. The proof applies only on densities swept by the allowed central densities. A physical finite envelope and its external-pressure condition are not supplied by the lemma.

Alternative interior scaling check: `rho_lambda(r)=lambda rho(lambda r)` gives `M_lambda(r)=lambda^-2 M(lambda r)`. Hydrostatic RHS scales by lambda, whereas its density derivative scales by lambda^2, so a common EOS requires `P'(lambda rho)=P'(rho)/lambda` wherever these profiles overlap and rho' is nonzero. This gives the same logarithmic derivative. It does not impose a common external pressure across that rescaled family.

Crucially, A is the positive integration coefficient. Deriving the logotropic functional form from this homology does not select its numerical value or connect it to u_Lambda. If Sigma_* is inserted as the observed target in the lemma, its resulting A is a repackaging of that target.

## 3. Dependency and obligation check

- Common smooth homologous interior + constant column -> logotropic EOS on the swept interval: analytic conditional lemma above; root independently checked its restricted statement.
- Assumed logotropic EOS -> constant column: passed analytically under the stated Newtonian core hypotheses.
- Contrast-four moving-pressure core -> positive radial mode: inherited finite numerical evidence; not rerun, and not stability of a live halo/envelope.
- Reciprocal wave outlet -> energy conservation and zero static force: passed by direct variation.
- Damped positive core mode -> arbitrary cold-collapse formation: not established.
- A related uniquely to measured total u_Lambda -> kappa=1/2: exact final algebra passed; antecedent remains unchecked/absent.
- M6 population/forest corrections -> this microscopic coefficient: no implication; independent observational/ancestry gaps remain.

The cheapest decisive next check is an independently specified parent identity fixing A/u_Lambda, including any additive vacuum term. Longer normalized relaxation runs do not test that missing identity. This does not rule out future parents, alternative nonhomologous mechanisms, or a physical completion.

## 4. Direct code evidence and frozen inputs

`eos_route/diagnostic.py:76–85` starts from adopted a0 and computes `a_req=a0*a0/(pi*G*xi4*xi4)`. Its surface-density agreement is therefore a conditional scaling check, not coefficient discovery. Line 86 computes rho_lambda from the adopted canonical identity. `eos_route/homology.py:25` reports `final_Sigma_over_target=y**-2`; returning y to one only demonstrates return to the preselected target.

SHA-256 (paths relative to repository `/Users/carlzimmerman/new_physics/zimmerman-formula`):

- `closure_program_2026_10_27/RESULTS.md`: `aa4248959b04153847f2665cb11c8b32b0295642be78782a26f00dc940d9867e`
- `multistream_mechanism_2026_10_27/eos_route/DERIVATION.md`: `1670e8f210ceb356acddd131d37dde177a6ce0e833072cbd113c80eb4739e7a9`
- `multistream_mechanism_2026_10_27/field_route/REPORT.md`: `1b04ae408fe0d088cf101f17028ffd1d6ae0d980ad375e0cc9b5ca9274129110`
- `multistream_mechanism_2026_10_27/field_route/continuation/RESULT.md`: `706bdec5cb9ae8d111f1232438a425164ab91b584c4002df70989abf0f7253bc`
- `reviews/claude_closure_audit_2026_10_27/REPORT.md`: `316d1a91242b21a056da1706c537d4340bf21748f8b4d02fd82d115878483ca2`
- `multistream_mechanism_2026_10_27/eos_route/diagnostic.py`: `c1f63e7f3ac8979f978d30420ddb96d7f7a0756a50a4c85b34f8929f1c690d09`
- `multistream_mechanism_2026_10_27/eos_route/homology.py`: `cf009d7b5d082d5b2656caeb6187ce23cbad7a6c61dc717ec351c53814f4d740`
- `multistream_mechanism_2026_10_27/eos_route/wave_outlet.py`: `293f96cd2011f627caf7cffac5939e241249fcd6967a711b39e98b98cec09529`
