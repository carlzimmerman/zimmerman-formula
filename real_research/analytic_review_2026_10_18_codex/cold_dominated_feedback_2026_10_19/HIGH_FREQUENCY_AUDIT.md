# Independent analytic audit: high-frequency actual feedback

## Normalized claim and verdict

For a fixed actual halo satisfying `BOUNDARY_PAIRING.md` (H1), (H2), (H4), and with each full ordinary-action gradient `grad Omega_i` nonzero on a neighborhood of the complete closed occupied action set, let `Y_gamma=C^gamma(I;C)^2`, `0<gamma<1/2`, `0<beta<gamma^2/(1+gamma)`, `eta=1-beta`, and `p=gamma-(1+gamma)beta/gamma`. The claim is that the full actual feedback operator, including its upper boundary values, obeys

`||K(z)||_{Y_gamma -> C^eta(I;C)^2} <= C (1+|z|)^(-p)`

on `Im z>=0`, and analogously on the lower closed half-plane. Constants may depend on the fixed halo and its positive warmth. Consequently `I-K(z)` has inverse norm at most 2 on `Y_gamma` for all sufficiently large `|z|`.

**Primary verdict: proved as written.** No missing implication was found in this conditional high-frequency theorem. The existence proof for a particular cold-dominated family, finite-frequency inversion, and receiving-work conclusions are outside this focused audit; the high-frequency result does not require those conclusions.

Audited target: `real_research/analytic_review_2026_10_18_codex/cold_dominated_feedback_2026_10_19/HIGH_FREQUENCY_INVERSE.md`.

SHA-256: `6111b7f0f2e2ea0ef1ea80b81c1a1227374bedc270614c50698db830ade8d49c`.

Raw dependency: same directory, `BOUNDARY_PAIRING.md`.

SHA-256: `5b5f2f73d54b034fa014b6efbeeb9acb5cadd9a30f2f40340745569610bba23d`.

## Dependency graph

1. Actual kernel formulas (H4) and radial half-period monotonicity imply the indicator Fourier estimate and `C |r-r'|/|n|` kernel-harmonic estimate. [Internal calculation; passed.]
2. Uniform smooth circular orbit coordinates from (H1) imply both receiving Fourier decay `|n|^-gamma` and the circular product lemma. [Internal calculation, with (H1) as an explicit geometric hypothesis; passed.]
3. Joint Lipschitz kernel regularity implies `||P(r,.)-P(r',.)||_{C^gamma} <= C |r-r'|^(1-gamma)`. Combining the circular product lemma with the pointwise harmonic bound and interpolating in action regularity produces the precise mixed radius/harmonic estimate (6). [Internal; passed.]
4. Full-frequency submersion, compactness, and (H2) give finitely many frequency charts independent of `n` and globally `C^beta` zero-extended pushforward densities. [Internal chart argument; passed.]
5. Uniform closed-half-plane Cauchy estimates imply absolute summability in `B(Y_gamma,C^eta)`. [Elementary singular-integral subtraction; passed.]
6. The low/high harmonic split gives `|z|^-p`; bounded embedding into `Y_gamma` and a Neumann series give large-frequency inversion. [Internal; passed.]

There is no circular use of an inverse, susceptibility smallness, a finite-mode exclusion, or a receiving quotient. There is no load-bearing scientific computation or unchecked external theorem in these implications.

## Obligation matrix and decisive calculations

| Obligation | Status | Independent calculation |
|---|---|---|
| Actual indicator coefficient, including turning/circular limits | Passed | The set with radius below the output radius is `[0,theta_r) union (2pi-theta_r,2pi]`; its nonzero coefficient is `sin(n theta_r)/(pi n)`. It is zero outside the turning interval and at a circular orbit. |
| Weak kernel derivative and output difference | Passed | The three Newtonian entries have derivative `(G/r^2)1_{u<r}`; the tethered entry has derivative `-(2G^2 M_t(r)/(a_0 r^4))1_{u<r}`. Integrating bounded derivative coefficients against the indicator coefficient gives `|Delta_r P_n|<=C d/|n|`, uniformly through circular limits. |
| Receiving harmonic decay | Passed | The uniform orbit maps make `theta -> phi(r(theta,q))` uniformly `C^gamma`; the Fourier translation identity gives `|phi_n|<=C|n|^-gamma ||phi||`. |
| Radial interpolation | Passed | `f_d=P(r,.)-P(r',.)` has sup norm `O(d)` and uniformly bounded Lipschitz seminorm. Hence `||f_d||_{C^gamma}<=C d^(1-gamma)` on the fixed bounded shell. |
| Ordinary-action circular product and zero extension | Passed | Each nonzero orbital coefficient vanishes at `a=0` and is uniformly `C^gamma` in `(a,L)`. The product difference at fixed `L` is bounded by `C(a^gamma+b^gamma)|a-b|^gamma <= C|a^2-b^2|^gamma`. Its size is `O(J^gamma)`, so extension by zero to `J<0` remains `C^gamma`. Joint changes follow by splitting the `J` and `L` changes. |
| Precise interpolation exponent | Passed | Interpolating `C^0` size `d |n|^(-1-gamma)` against `C^gamma` size `d^(1-gamma)` at exponent `beta/gamma` gives `d^(1-beta)|n|^{-(1+gamma)(1-beta/gamma)}=d^eta |n|^(-1-p)`. Multiplication by fixed `w_i Omega_i` and chart cutoffs preserves both bounds. |
| Uniform coarea constants | Passed | Use `y=Omega_i`, never `n Omega_i`. Compactness and a nonzero full gradient yield one finite cover and bounded chart Jacobians independent of `n`. Integrating a globally zero-extended `C^beta` amplitude in the complementary coordinate preserves its `C^beta` norm with a fixed constant. Circular tangencies are covered even if `partial_L Omega_i=0`. |
| Boundary/corner amplitudes | Passed | The product vanishes at `J=0`; (H2) supplies smooth zero extension at cap and angular-momentum ends. Thus no moving-domain term or unaccounted boundary density enters the pushforward. |
| Cancellation of the harmonic factor | Passed | `n Omega_i/(n Omega_i-z)=Omega_i/(Omega_i-z/n)`. With `Omega_i` included in the amplitude, equation (7) has neither an extra factor `n` nor a missing factor `1/n`. Negative `n` simply exchanges Cauchy half-planes. |
| Cauchy estimate uniform for all closed-half-plane arguments | Passed | The direct subtraction calculation below controls both boundary principal values and all nonreal arguments by the global `C^beta` norm on a fixed support. |
| Fractional output norm and absolute harmonic summation | Passed | The density estimate holds for each output difference with factor `d^eta`. The Cauchy estimate therefore gives the `C^eta` seminorm bound `C|n|^(-1-p)`. Every nonzero `P_n(R,.)` is zero, controlling the full norm. Since `p>0`, the harmonic series converges absolutely in the claimed operator space. |
| Identification with the actual full operator | Passed | Finite harmonic truncations have the actual source-form representation. Off the real axis, the original source series converges by orbitwise Parseval; applying the bounded actual kernel agrees with the absolutely convergent stronger-norm series. At each real frequency the submersion boundary construction gives the same limit. Uniform absolute convergence of the stronger-norm series justifies taking the boundary value there. |
| High-frequency split and exponent | Passed | For `|n|<=|z|/(2Omega_+)`, the reverse triangle inequality gives `|y-z/n|>=|z|/(2|n|)`. The direct integral bound gains `|n|/|z|`; summing the low part and the remaining `|n|^(-1-p)` tail gives `C|z|^-p` since `0<p<1`. |
| Large-frequency inverse | Passed | `eta>gamma`, so the fixed embedding makes `||K(z)||_{Y_gamma->Y_gamma}<=C'(1+|z|)^-p`. For sufficiently large modulus this is at most `1/2`, and the ordinary geometric Neumann series has norm at most 2. |
| Global frequency continuity addendum | Passed | The compact-density Cauchy transform is `C^alpha` on each closed half-plane for `0<alpha<beta`; scaling the argument by `1/n` gives the factor `|n|^-alpha`, so the stated harmonic sum converges. No frequency derivative is being inferred. |

### Explicit uniform Cauchy bound

Let a globally `C^beta` density `b` have support in one fixed finite interval and put `zeta=x+iv`. Choose a fixed smooth even cutoff `rho`, supported in `[-1,1]` and equal to one near zero. Write

`integral b(x+s)/(s-iv) ds`

as the sum of the local difference term, a far term, and `b(x) integral rho(s)/(s-iv) ds`. In the local difference term the numerator is bounded by `C||b||_{C^beta}|s|^beta`; `|s-iv|>=|s|` gives the integrable bound `C|s|^(beta-1)`. The far term has denominator bounded away from zero and fixed support length. In the constant term, evenness cancels the real odd part; its remaining magnitude is bounded by `|v| integral rho(s)/(s^2+v^2) ds <= pi ||rho||_infinity`. At `v=0` use the corresponding principal value and signed delta limit. This proves a uniform bound independent of `x,v`, including support endpoints and both signs of `v`. The same norm inequalities apply to bounded-linear-operator-valued densities. Thus no positivity or scalar cancellation of different harmonics is required.

### Explicit split

For `N` comparable to `|z|` and at least 1,

`|z|^-1 sum_{1<=|n|<=N}|n|^-p <= C |z|^-1 N^(1-p)`,

`sum_{|n|>N}|n|^(-1-p) <= C N^-p`.

Both are `O(|z|^-p)`. The uniform summable bound handles bounded `|z|`; there is no uncovered small-modulus region.

## Source checks, remaining gap, and safe scope

The raw target and raw `BOUNDARY_PAIRING.md` were read directly. Applicable `AGENTS.md` instructions were searched; none were found in the repository ancestry or `real_research` tree. Text reads, text searches, and SHA-256 hashing were used; no scientific code, numerical arrays, numerical integration, or scientific process operations were used. No proof file was edited.

**Exact remaining gap for the normalized high-frequency claim: none found.** The strongest safe statement is the complete conditional theorem displayed above, including the high-frequency Neumann inverse, for each fixed halo satisfying the explicitly assumed smoothness, support-extension, and full-gradient hypotheses. This audit does not certify the separate geometric construction as a theorem about every possible halo, and it does not infer finite-frequency inversion or bounded work.

Cheapest next check if the bound is to enter a larger argument: verify that the particular fixed equilibrium used there satisfies the stated full-gradient hypothesis on its entire closed occupied set. No additional high-frequency calculation is needed by this proof.

## Provenance

Independent fresh subagent audit, performed analytically from the raw target and dependency rather than from an author verdict. The two hashes above identify the exact revisions audited. This is one independent reasoning pass, not a formal proof certificate.
