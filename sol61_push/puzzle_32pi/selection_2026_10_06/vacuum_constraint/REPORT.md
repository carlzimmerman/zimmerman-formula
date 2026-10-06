# Local vacuum sequestering: exact cancellation still leaves a boundary selector

**Result.** Replacing freely gravitating matter vacuum offsets by local four-form sequestering genuinely removes that old counterfamily. It does **not** select `Lambda_geom/a0² = 32 pi`. Below is a different obstruction: an explicitly normalized P2 static response, linked to the sequestering cutoff rather than assigned afterwards, admits distinct residual ratios through four-form data. A smooth, globally nonlinear boundary function with an affine open band permits **exact same-geometry, same-form-field cancellation** of bounded matter vacuum shifts. Thus this obstruction survives even an exact classical cancellation premise, rather than relying on the generic theory's weaker radiative-stability statement.

The response construction is a covariant action term with a verified FRW vacuum branch and its leading static limit. Its full perturbative health, interpolation beyond that limit, and galaxy/cosmology closure are not established. The negative result concerns what these specified equations select, not all possible sequestering completions.

## Input and source scope

Requested base: `276ae422f0fb0b6990b9824a10fa4979c148aff0`. The concurrent checkout had advanced to `ff8b44018e092444c75a972cd9c85183ec2b0477` when the input provenance was recorded. `source_and_inputs.json` pins the actual input hashes; the runner records its actual HEAD and dirty state independently.

Primary source verified: Kaloper, Padilla, Stefanyszyn and Zahariade, *Manifestly Local Theory of Vacuum Energy Sequestering*, published PRL 116, 051302 (2016), [publisher full text](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.116.051302/fulltext), DOI `10.1103/PhysRevLett.116.051302`, pp. 3–4, Eqs. (7)–(10). The local action uses two metric-independent four-form measures to make its vacuum multiplier and gravitational coefficient constant on shell. The source explicitly leaves the residual flux contribution arbitrary, and treats matter loops with classical gravity. Its boundary functions are smooth and otherwise unspecified; nonlinearity allows generic flux data to determine finite coefficients. This report independently derives the constraints and tests a more restricted exact-shift subclass. No graviton-loop cancellation or global literature novelty is claimed.

Project comparison: `VACUUM_OFFSET_SELECTION_RESULTS.md` used a gravitating additive vacuum height; that premise is replaced here. `SHARED_SCALE_RESULTS.md` left `lambda/(xi gamma²)` free, while `TONIGHT_32PI_RESULTS.md` left a response conversion coefficient free. Here even a fixed conversion coefficient leaves a **different**, boundary-flux freedom. The basic arbitrariness of the sequestered residual is already stated by the primary paper; the local contribution is the exact-shift witness and the fully varied scale-link diagnostic, not discovery of that arbitrariness.

## 1. Derivation with signs and regulated averages

Use `c=hbar=1`, metric signature `(-+++)`, and write `K=kappa²>0`. Let `M²=M_Pl²` be the fixed reference cutoff and `mu⁴` the fixed matter cutoff. With `F=dA`, `Fhat=dAhat` locally,

`S = integral sqrt(-g)[ K R/2 - Lambda + L_m + L_resp ] + integral sigma(Lambda/mu⁴) F + integral sigmahat(K/M²) Fhat`.

Our matter Lagrangian convention is plus `L_m`, with constant vacuum contribution `L_m=-V`. Define the Hilbert stress of `L_m+L_resp` so that `T^mu_nu=-V delta^mu_nu+tau^mu_nu`. Four-form terms have no metric stress. Initially `L_resp` is independent of the variables `Lambda,K`.

Varying the three-form potentials gives `sigma' dLambda=0`, `sigmahat' dK=0`. Work only on connected branches with both derivatives nonzero. Scalar and metric variations then give

`F = (mu⁴/sigma') vol_g`,

`Fhat = -(M²/(2 sigmahat')) R vol_g`,

`K G_mu_nu = T_mu_nu - Lambda g_mu_nu`.

Before enforcing constant `K`, the metric equation also contains `(nabla_mu nabla_nu - g_mu_nu box)K`. It vanishes on this branch, not off shell.

Define `Omega=integral vol_g`, `Q=integral F`, `Qhat=integral Fhat`, and a common regulated average when needed. Integrating the two pointwise form equations gives

`Omega = sigma' Q/mu⁴`,

`<R> = -2 mu⁴ sigmahat'/(M² sigma') * Qhat/Q`.

The metric trace is `-K R=T-4 Lambda`. Therefore

`Lambda = <T>/4 + Delta`,

`Delta = K<R>/4 = -mu⁴ K sigmahat'/(2 M² sigma') * Qhat/Q`,

`K G_mu_nu = tau_mu_nu - <tau>/4 g_mu_nu - Delta g_mu_nu`.

The **explicit** constant `V` cancels exactly. The residual gravitating density is `rho_res=Delta+<tau>/4`, not the bare `Lambda`. In a pure vacuum branch `tau=0`, `Lambda_geom=Delta/K`.

If `sigma'` depends on its argument, shifting `V` also shifts `Lambda`. At the same geometry, `K` and same form strengths, the scalar form equation consequently changes. Thus exact cancellation in the projected stress must not be confused with exact same-boundary-data invariance for every nonlinear function. The control `sigma=exp(x)` with `x -> x-.1` changes that form equation by factor `exp(-.1)=0.9048374180`. It is a consistency test of a proposed unchanged geometry, not a solved new cosmology.

## 2. A response scale fixed before evaluating the vacuum ratio

Introduce a preferred foliation scalar `T_f`,

`u_mu=-partial_mu T_f/sqrt(-partial T_f squared)`,

`a_mu=u^nu nabla_nu u_mu`, `s=sqrt(a_mu a^mu)`.

Set the response scale **in the action** to

`a0 = zeta mu²/M`, with fixed positive dimensionless `zeta`.

Define

`W(s;a0) = [s sqrt(s²+a0²/4)+(a0²/4) asinh(2s/a0)]/2 - a0 s/2`,

`L_resp = -2 M²[W(s;a0)-s²/2]`.

This is independent of the varied `Lambda,K`. The source normalization is fixed by minimal baryonic metric coupling, not a post hoc redefinition of `a0`. In the weak static branch `T_f=t`, `s=|grad Phi|` to leading order. The Einstein term supplies `-K |grad Phi|²`; on the branch `K=M²` the total leading potential action is

`S_static=integral [-2 K W(|grad Phi|;a0)-rho_b Phi] d³x dt`.

Its equation is `div[W_s grad Phi/s]=rho_b/(2K)=4 pi G rho_b`, where `G=1/(8 pi K)`. Since

`W_s=sqrt(s²+a0²/4)-a0/2 = b`,

spherical isolated source matching gives `b=G M_b(r)/r²` and exactly

`g²=b²+a0 b`.

This is the declared P2 static law, including its high-acceleration Newton normalization and deep-MOND coefficient. It fixes what `a0` means operationally. The leading static construction at `K=M²` does not prove that the preferred-foliation sector is healthy; in particular cancellation of quadratic static terms requires a separate kinetic and constraint audit. We do not use this action as a proposed healthy completed theory.

For geodesic comoving `u` in FRW, `s=0`. Both the response value and its first variation vanish: `W(0)=0`, and `W-s²/2` starts at quadratic order. Hence this response sector has zero background stress on the vacuum FRW branch. A de Sitter geometry with `T_f=t` and `Lambda_geom=3H²>0` satisfies that branch; the response field's first variation vanishes there too. Perturbations are not inferred from this background fact.

The normalized coefficient is now

`C = Lambda_geom/a0² = -[sigmahat'/sigma'] (Qhat/Q)/(2 zeta²) + M²<tau>/(4 K zeta² mu⁴)`.

For `tau=0`, even with **fixed** `zeta`, boundary functions and flux ratio remain. `C=32 pi` requires

`[sigmahat'/sigma'](Qhat/Q) = -64 pi zeta²`.

That is the exact missing selector. Neither the stress projection nor the local form equations prescribe it. Fixing it by measurement or a boundary condition produces the target as input.

## 3. Exact-shift witness inside globally nonlinear functions

Let `eta(t)=exp(-1/t²)` for `t>0`, zero otherwise; let `L=256`. Choose

`sigma(x)=x+eta(x-L)-eta(-x-L)`,

`sigmahat(y)=y²/2`, with `y=K/M²>0`.

Both functions are smooth and globally nonlinear. `sigma'>=1` everywhere, and `sigma'=1` exactly on `|x|<L`; `sigmahat'=y` is nonzero. This restricted branch does not promise that arbitrary independent boundary fluxes determine every parameter: the affine band imposes `Q=mu⁴ Omega`. That restriction is explicit and does not prevent freely choosing the curvature ratio. It avoids silently replacing the published generic nonlinear class by globally linear functions.

For any solution whose `Lambda/mu⁴` lies in the band, the transformation

`V -> V+delta V`, `Lambda -> Lambda-delta V`

leaves the metric, response fields, `K`, both form strengths and their regulated fluxes unchanged, provided the transformed argument remains in the band. The bulk combination `-Lambda-V` is unchanged; `sigma` changes by a constant times the fixed form flux, with no change of the local Euler equations. This is an exact solution-to-solution statement under fixed flux boundary variations, not a numerical radiative approximation. It does not claim shift invariance across the band's edges or at quantum-gravity level.

Pure de Sitter FRW supplies an explicit background branch: `R=4 Lambda_geom`, `F=(mu⁴/sigma') vol_g`, `Fhat=-2 M² Lambda_geom/sigmahat' vol_g`. The two form strengths are constant multiples of the same volume form, so their flux ratio is independent of any **common** regulator. Individual fluxes can diverge on eternal de Sitter; no finite division of two unspecified infinities is used. Compact spatial-volume and temporal cutoffs merely evaluate this constant pointwise ratio. A finite-domain action with its own variable gravitational boundary terms would require a separately declared boundary variational principle.

Bounded controls fix `K=M²=zeta=1`, `mu⁴=.01`, `a0=.1`. They use `C=16 pi,32 pi,64 pi` and `V/mu⁴=-10,0,10`. For each chosen `C`, the same geometry and form data survive all three shifts, while every case remains in the affine band. Their ratios `Qhat/Q=-2C` are respectively approximately `-100.5309649,-201.0619298,-402.1238597`. The physically normalized P2 response is the same for all nine cases. The background curvature changes **between** coefficient families, as it should; it does not change **within** a vacuum-shift triplet.

Flux quantization or a quantum boundary state is outside these premises. Such an addition might restrict the continuum, but would still have to derive the particular above ratio instead of merely postulating it.

## 4. Attempted repair: linking to bare Lambda changes the variational problem

Try `a0²=epsilon Lambda/K`, with positive `Lambda` and fixed `epsilon`. This is a different action. Denote its response Lagrangian derivatives at fixed metric and other fields by `L_Lambda`, `L_K`. The three-form variations still force constant `Lambda,K`, but scalar variations now give

`(sigma'/mu⁴) F=(1-L_Lambda) vol_g`,

`(sigmahat'/M²) Fhat=-(R/2+L_K) vol_g`.

Consequently

`Omega(1-<L_Lambda>)=sigma' Q/mu⁴`,

`Delta=K<R>/4=-K<L_K>/2 - [mu⁴ K sigmahat'/(2 M² sigma')](Qhat/Q)(1-<L_Lambda>)`.

The trace identity defining `Delta` remains valid, with the **total** response stress included. Reusing the unmodified flux formula would drop two necessary derivatives.

For the specified response,

`a0 W_a0=2W-sW_s`,

`L_Lambda=-(M²/Lambda)(2W-sW_s)`,

`L_K=(M²/K)(2W-sW_s)`.

These terms generally do not vanish on a sourced response. Even on the zero-response FRW vacuum background where they vanish, the bare `Lambda=Delta-V` tracks the matter vacuum shift. Thus `d(a0²)/dV=-epsilon/K`: geometry can stay protected while the operational MOND scale changes. This does not solve a vacuum-independent ratio. Identifying `Delta`, rather than bare `Lambda`, inside a new local response would require an additional local constraint/sector implementing the global invariant. Merely substituting the on-shell average or flux ratio into an off-shell Lagrangian would be a new, potentially nonlocal theory.

## 5. Evidence, controls and checkpoint

`checks.py` verifies the trace/projection and flux identities symbolically, the P2 action derivative and response identity, scale homogeneity, the cutoff-normalized ratio, and the modified global constraints. Its deterministic controls are the nine shift/flux cases, five positive source values, a nonlinear-function fixed-geometry failure, and a dropped-response-derivative mutation.

Authoritative runs: `runs/main_b` completed, all implemented assertions pass; `runs/control_b` exits 1 and rejects the omitted derivative. Both standard computation-audit manifests validate against the current inputs and outputs. `runs/main_a` is retained as a **historical failed implementation**: a factor of two was missing in the `L_K` contribution to `Delta`; the exact trace check caught it. Its script hash differs from the repaired file, so it is not fresh evidence. The corrected coefficient is `-K<L_K>/2`, as follows directly from `R/2+L_K` in the scalar variation.

Bounded calculations authenticate these implementations, not the existence or stability of a full galaxy-plus-cosmology completion. The exact conclusion instead follows from the explicit equations and the within-band solution mapping: protected matter-vacuum cancellation does not constrain the independent residual boundary ratio, even with an action-level, operationally normalized response scale.

**Next missing implication:** a physical boundary-state/flux equation or a new sequestering-invariant local scale constraint must enforce `[sigmahat'/sigma'](Qhat/Q)=-64 pi zeta²`, while preserving response normalization and perturbative health. No such selector has been derived here. This is a substantive changed-premise obstruction checkpoint, not closure of the 32pi puzzle.
