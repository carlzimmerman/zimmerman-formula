# Carrier action audit and a conserved constitutive completion

Date: 2026-09-20. Source base: `3aaed026d55f65b38733316cb63c432290a339e1`, with a dirty working tree; exact inputs are pinned by the adjacent run manifests. Sources were not edited.

**Normalized claim.** The single shift-symmetric carrier action in L290 is claimed to supply a positive-density, cosmologically cold component with conserved dust evolution, a gradient-dependent velocity scale inside structures, and the ordinary isotropic hydrostatic constitutive law used downstream. The L291 reduction is intended to validate its FRW evolution.

**Primary verdict: incomplete, with the smallest missing implication identified.** The stated carrier is not connected to those FRW and halo equations by a valid action-level reduction. The background charge equation and the equilibrium-pressure identity already expose exact gaps. There is, however, a constructive universal action that repairs charge conservation and protects the entire homogeneous cosmological trajectory from the switch. Its finite-gradient coupled health and halo solutions remain open.

## Conventions and exact original-action result

Use signature `(-,+,+,+)`, timelike `X=-g^{ab}χ_aχ_b>0`, unit clock `n`, spatial projector `h^{ab}=g^{ab}+n^a n^b`, and `Y=h^{ab}φ_aφ_b≥0`. Write the carrier Lagrangian as pressure function

\[
p(X,Y)=-F(X,Y)=p_1\Delta+\tfrac12 g(Y)\Delta^2,
\qquad \Delta=X-X_0,\quad X_0=C^2,
\]

where `p1=-G1>0`, `g=-G2>0`. This is the actual sign-corrected action at L290:58–63,112–118. Its shift current can be normalized as `j^a=p_X∇^aχ`, with `∇_a j^a=0`. The factor two is immaterial to conservation.

At fixed Y, the density of the perfect-fluid part is

\[
\rho=2Xp_X-p=2X_0p_1+(p_1+2X_0g)\Delta+\tfrac32g\Delta^2,
\qquad
c_\chi^2=\frac{p_X}{p_X+2Xp_{XX}}.
\]

Consequently at `X=X0`, `p=0`, `ρ=2X0 p1>0`, but `cχ²=p1/(p1+2X0g)>0`. It is false that the action implies `p=ρcχ²`. The smallest exact example is `X=X0=p1=g=1`: `p=0`, `ρ=2`, `cχ²=1/3`. Even the affine relation `p=cχ,0²(ρ-ρ0)` holds only to first order for the polynomial action; its exact residual is

\[
p-c_{\chi,0}^2(\rho-\rho_0)
=\frac{g(X-X_0)^2(X_0g-p_1)}{p_1+2X_0g}.
\]

Thus L293's isothermal pressure law is an additional constitutive assumption, not an application of the local mode speed measured in L290:142–165. The actual exact speed in L290 is `(s+δ)/(s+Aδ)`, approaching `s/(s+Aδ)` for `s≫δ`; the prose of its Lean file reverses this ratio, although its algebraic denominator identity is not that reversed assertion.

## Metric stress, scalar exchange, and varying Y

Put `D_aφ=h_a{}^bφ_b=φ_a+Q n_a`, `Q=n^aφ_a`. Varying the normalized clock together with the metric gives

\[
\frac{\partial Y}{\partial g^{ab}}=D_a\phi D_b\phi,
\qquad T^{(\chi)}_{ab}=2p_X\chi_a\chi_b+p g_{ab}-2p_YD_a\phi D_b\phi.
\]

The last term must not be silently omitted. In a static aligned configuration with scalar gradient along the radius, `ρ=2XpX-p`, tangential pressure is `pt=p`, and radial pressure is `pr=p-2YpY`. For the original action, `pY=g_Y Δ²/2` wherever that derivative exists.

Let `τab=2pX χaχb+p gab` denote only the perfect-fluid part. On the χ equation,

\[
\nabla^a\tau_{ab}=p_Y\nabla_bY.
\]

For a stationary carrier aligned with static observers in lapse `N(r)`, this gives

\[
p'=-(\rho+p)(\log N)' +p_Y Y'.
\]

This equation describes the perfect-fluid part's exchange; the full carrier stress above also carries anisotropic stress and exchanges with the clock/scalar sector. A complete isolated carrier conservation law is not implied when `pY≠0`. Substituting `p'=pX X'+pY Y'` gives `X'/X=-2(log N)'`, consistent with `χ=μt` and `X=μ²/N²`. This is a useful exact hydrostatic integrability relation, independent of an assumed isothermal atmosphere.

## Why the quoted cosmological reduction does not establish the claim

1. For homogeneous χ, conserved charge is `a³pX χdot=constant`. With fixed coefficients, `X=X0=C²`, `χdot=C`, and `Y=0`, this is `a³p1 C`; its derivative is `3a² adot p1 C`, nonzero in expansion. L291:48–53 instead prescribes `G1,G2∝a^-3`. It does not derive this from a fixed covariant L290 action.
2. `clock_action_build.py:265` makes G1 and G2 constant SymPy symbols. Euler–Lagrange differentiation at :307–322 therefore omits coefficient derivatives. Inserting `a^-3` afterward, as L291:48–53 does, is not equivalent to varying time-dependent coefficients. For `p1=p10/a³`, `g=(A-1)p10/(2C²a³)`, the missing χ-equation contribution from the quadratic carrier action is

   `6 p10 H [ A(χdot−C Ψ)−3C Φ ]`.

   This difference is an exact symbolic identity. Even externally prescribed coefficients would require these terms; a covariant completion must also vary their underlying fields.
3. The returned equation order is lapse, momentum, trace, **clock**, **scalar**, χ (`clock_action_build.py:308,320–325`). L291:76 and :96 inspect/use `Eq[3]` as the scalar equation. This is the clock equation. The actual cold scalar equation is index 4 and gives

   `2(2−KB) k² a [ Ψ−Tdot−β P ]=0`,

   hence `P=(Ψ−Tdot)/β` for `a>0`, `k≠0`, `β≠0`, `KB≠2`. The clock equation does contain `Pdot`; the actual scalar equation does not. The cached six-equation system verifies this independently of the reduction.
4. L291:167 compares an eigenvalue already divided by H with `10 H`, rather than with 10. At :175 the purported 30% test permits 90%. At :197–207 the observable is a Euclidean norm of mixed field/velocity variables, not the χ density contrast, and only an upper bound of six is checked. The source's current stored result has zero maximal growth throughout its scan and errors for all three late integrations. No successful growth prediction is inferred from it.
5. The cache is keyed only by `/tmp/L291_frw_odes_chi.pkl`, not source hashes (L291:29–38). Our cache-based source check uses a pinned snapshot and is explicitly not a fresh full-builder run.

An algebraic cold scalar need not by itself imply strong coupling: here its spatial constraint is invertible at nonzero k and β. Conversely, bare zero entries between χ and the scalar/clock do not prove that metric-mediated eigenmodes are unchanged. L290:135–176 checks direct matrix entries, while both sectors share lapse/metric constraints. The full Schur complement and a nonlinear cutoff analysis remain separate obligations. No strong-coupling scale is established here.

The cold scalar quadratic block is `d k²/a²[2(Ψ−Tdot)P−βP²]`, `d=2−KB`. Eliminating P adds `d/β·k²/a²(Ψ−Tdot)²`. In clock-unitary gauge the lapse-gradient coefficient is therefore `αeff=α+d/β=2` at `β=d/(2−α)`. This scalar-block identity is checked; the full gravitational/shift/carrier Schur complement is not certified by this report.

## Constructive completion: conserve charge and protect every homogeneous X

Assume `ρ0>0`, `X0>0`, `A>1`, `Yd=(δ a0tilde)²>0`, `X>0`, `Y≥0`. Define

\[
B(Y)=\left[1+\left(\frac{Y}{Y_d}\right)^2\right]^{1/4},
\quad m(Y)=1+\frac{A-1}{2B(Y)},
\quad
p_\star(X,Y)=\frac{\rho_0}{2m(Y)}
\left[\left(\frac{X}{X_0}\right)^{m(Y)}-1\right].
\]

This is one universal constitutive function. It introduces no independent scale beyond the original `A`, `δ`, `a0tilde`, `X0` and density normalization. It changes the interpolation near the switch; it is a candidate replacement, not a statement that the old action already had these properties.

At every fixed Y,

\[
p_{\star X}=\frac{\rho_0}{2X}(X/X_0)^m>0,\quad
K_\chi=p_{\star X}+2Xp_{\star XX}=(2m-1)p_{\star X}>0,
\]

\[
c_\chi^2=\frac1{2m-1}=\frac1{1+(A-1)/B},\qquad
p_\star=c_\chi^2(\rho-\rho_0).
\]

The positive-K statement is for the isolated carrier at fixed Y. For fixed finite Y and A>1, m>1 and K tends to zero as X approaches zero, so this is not a uniform kinetic bound at the boundary. At `X=X0`, its Taylor coefficients are `p=0`, `ρ=ρ0`, `pX=ρ0/(2X0)` and `pXX=ρ0(m-1)/(2X0²)`. Thus it integrates precisely the same sign-correct local carrier jet, using the smooth replacement stiffness `g(Y)=ρ0(A-1)/(4X0²B)`.

The key improvement is trajectory-wide protection:

\[
m_Y(0)=0
\quad\Longrightarrow\quad
p_{\star Y}(X,0)=p_{\star XY}(X,0)=p_{\star XXY}(X,0)=0
\quad\text{for every }X>0.
\]

For homogeneous φ and clock, `Y=O(ε²)` in perturbations. Since `p★(X,Y)=p★(X,0)+O(Y²)` for every X in a compact positive-X neighborhood, the switch first enters at order `ε⁴`, even while the background X rolls. It therefore adds no quadratic scalar-gradient term and no direct quadratic χ–φ/clock coupling along the whole homogeneous solution. Metric coupling remains.

At `Y=0`, `m=(A+1)/2` is constant. Normalize the homogeneous conserved charge so that `X(1)=X0`. Then

\[
X(a)=X_0a^{-6/A},\quad
\rho(a)=\frac{\rho_0}{A+1}\left[A a^{-3(1+1/A)}+1\right],\quad
p(a)=\frac{\rho_0}{A+1}\left[a^{-3(1+1/A)}-1\right].
\]

Both `a³ pX sqrt(X)=constant` and `aρ_a+3(ρ+p)=0` hold exactly; `cs²=1/A` at every epoch. This is nearly dust, not exact pressureless dust. For `A=10^10`, the density relative to `ρ0a^-3` differs by about `2.0×10^-9` at `a=10^-3`. The density also contains a fixed small constant term `ρ0/(A+1)` whose gravitational effect must be counted rather than double-counted in a cosmological fit.

For `s=√Y/a0tilde≫δ`, `B~s/δ` and `cs²~s/[s+(A−1)δ]`, giving the original high-gradient scaling. At the checked physical s values `0.05,0.28,0.315,0.39,0.8`, the relative change from the original exact speed is between `−0.080%` and `−0.005%`. These are bounded illustrative comparisons, not a halo-retention result.

### Why the superficially simpler switches fail to protect the trajectory

Keeping the original `B=1+s/δ` in the integrated action creates a cusp at zero spatial scalar gradient once `X≠X0`. Write `z=log(X/X0)`; then

\[
p_m=\frac{\rho_0}{2m^2}\left[(mz-1)e^{mz}+1\right].
\]

The bracket is strictly positive for `z≠0`, so `p_s(0)≠0`. The action contains a nonzero `|∇φ|` term and has no ordinary first derivative there. An exact example is `A=3`, `ρ0=δ=a0tilde=1`, `X/X0=2`: left and right derivatives in the scalar gradient are `log(2)-3/8` and `3/8-log(2)`. The quadratic expansion about a rolling cosmology is not justified.

Replacing B with `sqrt(1+Y/Yd)` removes the cusp but yields `mY(0)=−(A−1)/(4Yd)`, so `pY(X,0)≠0` during rolling. It changes the MOND scalar's spatial coefficient. If the old scalar Lagrangian is `−J(Y)`, cancellation would require `Jnew,Y=Jold,Y+pY(X(a),0)`. A J(Y)-only term cannot cancel this X-dependent correction for every epoch. The quartic-in-gradient switch above avoids that specific issue because its derivative at Y=0 vanishes identically along all X.

## Dependency and obligation record

| Implication | Status | Evidence / remaining condition |
|---|---|---|
| Sign-correct carrier gives positive reference density | Passed | Direct variation, symbolic identities, Lean reference-density lemma |
| Mode speed equals equilibrium pressure/density | Failed | Exact rational counterexample, Lean |
| Fixed χ=Ct and fixed L290 coefficients conserve expanding-FRW charge | Failed | Exact derivative; Lean obstruction |
| L291 varies its prescribed time-dependent coefficients | Failed | Builder treats them as constant symbols; exact omitted term |
| L291 uses actual scalar constraint | Failed | Wrong index; pinned source/cache audit |
| No direct switch coupling at original X=X0 | Correct only after restriction | Second variation exists at that reference background; metric mixing remains |
| Original sqrt(Y) switch works on rolling X≠X0 | Failed | Explicit cusp counterexample |
| Completed action conserves homogeneous current | Passed under stated positive-domain hypotheses | Exact analytic solution and symbolic checks |
| Smooth completed action protects all homogeneous X | Passed under stated positive-domain hypotheses | Chain-rule proof and all-X symbolic identities; Lean composition lemma assumes smooth outer function |
| Isolated carrier K>0 | Passed | Positive-domain formula and Lean inequality |
| Full coupled finite-Y stability, cutoff, and halo data | Not addressed | Requires reduced principal symbol and actual nonlinear field solution |
| Constant-Y power-law construction is novel | Not claimed | Parent is checking affine-k-essence literature; novelty is outside these algebraic checks |

## Reproducible evidence and limits

`check_carrier.py` verifies 25 exact symbolic identities, a rational pressure counterexample, a cusp counterexample, four cosmological sample points, and six switch sample points. `check_L291_source.py` audits the pinned cached equation order, types and cold scalar constraint, and records the source's stored output. `CarrierIdentities.lean` gives nine exact lemmas; it does not formalize the metric variation, the power-function differentiability hypotheses, or full field equations.

The adjacent `constitutive_run`, `source_run`, and `lean_run` manifests record actual commands, input hashes, output hashes, versions, and bounds. The symbolic constitutive derivation does not depend on L291's cache. Source reconstruction does, and is labeled accordingly. The reports remain evidence about exactly these mathematical obligations, not a complete theory certificate.

All three bounded runs completed, and all three manifests passed `validate_manifest.py --root` on 2026-09-20. Lean 4.34.0-rc2 compiled all nine lemmas without diagnostics; no `sorry`, `admit`, or added axiom occurs in the file. Mathematical self-proofreading covered this report and the new Lean comments/statements; no unresolved notation or display issue was found. Substantive open obligations are recorded above rather than treated as proofreading errors.

**Cheapest discriminating next check:** derive the full finite-Y coupled principal symbol using `p★`, including `pXY` and the longitudinal scalar correction `pY+2YpYY`, while retaining the actual background equations. Then integrate the resulting static equations with the anisotropic stress/current relation above. The existing simple isothermal atmosphere cannot substitute for that check.
