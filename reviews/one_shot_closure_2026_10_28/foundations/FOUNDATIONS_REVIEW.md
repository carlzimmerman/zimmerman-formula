# Foundations audit and exact closure attempt — 2026-10-28

**Normalized claim.** A single specified theory, with acceleration scale tied to dark energy, should produce the same galaxy law, cold-sector structure, and switch rule used in its empirical and formal checks. **Primary verdict: incomplete, with the smallest missing implication being a single set of equations and initial data producing the claimed law and halo/switch predictions.** In addition, the record's explicit equivalence between its two interpolation laws is refuted below.

This review reads the current workspace against requested base `44fd23a71c9888d9ea204c0ee832805829f9c090`. Observed HEAD was `ae0b838549839e35adfc494f93f82e1509d62d7a`. Exact SHA-256 hashes of all 23 reviewed inputs, their base contents, and equality flags are in [INPUTS.json](INPUTS.json). Only `V3S_FINAL_VERDICT_2026-10-24.md` and `THEORY_STATEMENT_2026-10-26.md` differ from that base among these inputs. The interpolation inconsistency is present at the requested base, not introduced by those dirty corrections. No existing theory file was changed.

Review provenance: independently reconstructed by a delegated reviewer from raw source, code and proof files. New derivations below are self-reviewed, with separate symbolic checks. Neither an agent's agreement nor a passing symbolic computation supplies physical validation. Existing Lean files were read but not recompiled in this review.

## 1. Decisive finding: the stated action and the cited certificates describe different laws

Let `a0>0`, `g>0`, `gN>0`, `x=g/a0`, and `y=gN/a0`. Restrict this comparison to the isolated, spherical, stationary limit with `mu_K=0` and no screening contribution. These restrictions are essential: a spherical algebraic relation is not the complete AQUAL field equation for general geometry.

The literal kernel in `covariant_push_2026_10_22/V3_FULL_PICTURE.md:28,45` has

\[
\mu_S(x)=\frac{x}{1+x},\qquad
y=x\mu_S(x)=\frac{x^2}{1+x}.
\]

Therefore its positive solution is

\[
g_S=\frac{g_N+\sqrt{g_N^2+4a_0g_N}}2,
\qquad g_S^2=g_N(g_S+a_0).
\]

This is exactly what `P4_v3_galaxy_tiles/p4_solver.py:29–38` and `CL3_one_number/cl3_one_number.py:28` execute. But `V3_FULL_PICTURE.md:65` calls it equivalent to

\[
g_B^2=g_N^2+a_0g_N,
\qquad \nu_B(y)=\sqrt{1+1/y}.
\]

That second relation has a different inverse function:

\[
\mu_B(x)=\frac{\sqrt{1+4x^2}-1}{2x}.
\]

**Smallest exact counterexample.** Set `a0=1`, `g=1`, and `gN=1/2`. The simple-kernel equation holds, since `1/(1+1)=1/2`. The claimed equivalent equation gives `1=3/4`, which is false.

The certificate cited in the same summary does not resolve this discrepancy. `EQB_A0LINE_uniqueness.lean:12–26` explicitly assumes affine squared excess, proves the B law, and includes `simple_nu_not_linear`, which distinguishes it from the S law. `EQB_S1_rar_landmarks.lean` assumes the B law. Their proofs are not certificates of the S law's landmarks.

| Object | Literal action / P4 / CL3, S | Exact squared-excess line / EQB, B |
|---|---|---|
| `mu(x)` | `x/(1+x)` | `(sqrt(1+4x²)-1)/(2x)` |
| `nu(y)` | `(1+sqrt(1+4/y))/2` | `sqrt(1+1/y)` |
| Isolated identity | `g²=gN(g+a0)` | `g²=gN²+a0*gN` |
| At `gN=a0` | `g/a0=(1+sqrt(5))/2` | `g/a0=sqrt(2)` |
| Newtonian excess | `0<g-gN<a0`, limit `a0` | `0<g-gN<a0/2`, limit `a0/2` |
| Squared-excess ratio `(g²-gN²)/(a0*gN)` | `(1+2x)/(1+x)`, varying from 1 to 2 | 1 |
| Aligned scalar EFE equation | `x²+(e-b)x-b(1+e)=0` | `(x²-b²)(x+e)=b*x` |

Here `b=gN/a0`, and the last row assumes the scalar ansatz `x*mu(x+e)=b`. The B cubic in `EQB_S5_efe_cubic.lean` is explicitly derived for `mu_B`, not `mu_S`. Neither scalar ansatz by itself certifies the full vector/PDE external-field calculation. P4 actually solves the external field as a boundary condition, so the documentary error does not invalidate those numerical solves merely by association.

**Uniform size of the discrepancy.** Express the two predictions at the same `y` using `y=x²/(1+x)` from S:

\[
\left(\frac{g_S}{g_B}\right)^2
=\frac{(1+x)^2}{x^2+x+1}
\leq \frac43,
\]

because `4(x²+x+1)-3(1+x)²=(x-1)²>=0`. Equality occurs at `x=1`, hence `y=1/2`. The largest relative difference is `2/sqrt(3)-1=15.470%`, or `0.062469 dex`. At `gN=a0`, it is `14.412%`, or `0.058473 dex`. These are differences between fixed predictions, not differences in refitted data likelihoods.

**Effect on the conclusions.** The particular P4/CL3 results remain results for S. The affine-excess uniqueness and B-law landmark theorems remain conditional results for B. The record cannot combine their support as if both were one exact law. The inconsistency also appears in `V3S_FINAL_VERDICT_2026-10-24.md`'s claim that the same model has a forced exact a0-line. An exact-law decision is needed before any claim of a unique completion.

## 2. Concrete repair dictionary, with the action integral done

This section is a new algebraic construction, not an audited physical completion. It makes the alternatives reviewable without silently changing the model.

For the nonrelativistic field action

\[
S_\Phi=-\int dt\,d^3r\left[
\frac{a_0^2}{8\pi G}F\!\left(\frac{|\nabla\Phi|^2}{a_0^2}\right)+\rho\Phi\right],
\]

variation with fixed boundary values gives `div(mu grad(Phi))=4*pi*G*rho`, where `mu(x)=dF(z)/dz` at `z=x²`. The two exact primitives, with `F(0)=0`, are

\[
F_S(x^2)=x^2-2x+2\ln(1+x),
\]

\[
F_B(x^2)=\frac{x\sqrt{1+4x^2}}2+
\frac{\operatorname{asinh}(2x)}4-x.
\]

Both have the required `2*x³/3` deep-limit leading term and recover a Newtonian leading quadratic term. The positive-radius elliptic eigenvalues are `mu` and `mu+x*mu'`; both are positive for either kernel. They degenerate at zero field, so this observation is not a uniform-ellipticity or global evolution theorem.

For the covariant notation in the cited khronon source, define the **geometric** acceleration `a_geo=a0/c²`, `Y=A_mu*A^mu/c^4`, and `x=sqrt(Y)/a_geo`. Then

\[
J_S(Y)=\Lambda-2a_{\rm geo}^2[x-\ln(1+x)],
\]

\[
J_B(Y)=\Lambda+a_{\rm geo}^2
\left[\frac{x\sqrt{1+4x^2}}2+
\frac{\operatorname{asinh}(2x)}4-x-x^2\right].
\]

Differentiating gives `1+J_S'(Y)=mu_S(x)` and `1+J_B'(Y)=mu_B(x)` exactly. Writing `a0` in SI units directly where `a_geo` belongs, while also retaining `c` in `Y`, is dimensionally inconsistent; the current summary needs an explicit geometric-unit convention or these factors of `c`.

The derivative identity is independently consistent with Blanchet–Skordis v1, Eq. (45). Its stationary equation is Eq. (44) in that version; the summary's unversioned attribution to “Eq. 35” is not correct for v1. The published-version equation numbering was not checked.

**Minimal proposed correction text, retaining the executed S model:**

> The static isolated spherical limit is the simple-MOND relation `gN=g²/(g+a0)`, equivalently `g²=gN(g+a0)`. Its Newtonian acceleration excess is less than `a0`. It has the deep-limit baryonic Tully–Fisher relation `v⁴=GMa0`. The exact squared-excess a0-line `g²=gN²+a0*gN`, its affine-excess uniqueness certificate, and its scalar EFE cubic refer to a different interpolation kernel and are not evidence for this action.

If the intended model instead prioritizes the exact B line, `J_B` above supplies its stationary kernel. All affected empirical fits and screening/health calculations would then need recomputation. No transfer of S-model goodness of fit is justified. Neither kernel replacement here proves full high-field admissibility, stability, causality, or cosmological success; in particular the source's bounded high-acceleration `J` condition is an additional constraint, not supplied by the integrated weak-field functions.

## 3. Exact obstruction to deriving kappa from the stated premises

For positive constants and vacuum **mass density** `rho_Lambda`, the Einstein conversion is

\[
\rho_\Lambda=\frac{\Lambda c^2}{8\pi G},
\qquad
a_0=\kappa c\sqrt{G\rho_\Lambda}
=\frac{\kappa}{\sqrt{8\pi}}c^2\sqrt\Lambda.
\]

Thus `kappa=1/2` is equivalent to the displayed coefficient `1/sqrt(32*pi)`. It does not follow from the conversion. For every `kappa>0`, either action kernel above can use `a_geo=kappa*sqrt(Lambda/(8*pi))` without changing covariance, the interpolation's dimensionless shape, or its deep/Newtonian limits. This is an explicit counterfamily to selection by those principles alone, not a no-go theorem for a new microscopic theory.

The record has a stronger, already-existing countermodel for its four-form route. `KAPPA_LOGIC_2026_10_20.lean` states

\[
\kappa^2=\frac{2\beta^2}{Z+2b_0\beta^2}.
\]

Set `beta=1` and `Z=2/kappa²-2*b0`. For every `kappa>0` with `b0*kappa²<1`, `Z>0` and the equation holds identically. With `b0=9/500`, both `kappa=1/2` and `kappa=1/3` satisfy these premises. The same file proves that imposing the proposed `32*pi` area relation is algebraically equivalent to imposing `kappa²=1/4`.

**What was achieved here:** the attempted closure returns an exact obstruction. Selecting `1/2` requires an independently justified additional condition that fixes a dimensionless coupling or boundary datum. A fit can provide it as a phenomenological parameter; renaming that fit “geometry” does not turn it into a derivation. A predictive physical theory is allowed fitted parameters, but this particular first-principles claim would remain open.

## 4. Core and switch closure: what the latest lanes establish

The latest relevant evidence is internally more cautious than several old headline summaries:

| Lane | Actual scope and consequence |
|---|---|
| X43 | Burkert mass matching gives `eta=4*c_f^(5/4)/(3*B(1))` **conditional on** the assumed `9/4` infall slope, chosen core radius, and profile. `c_f=4` is external. This is not a derivation of the core-radius selection or the surface-density floor. |
| X44 | A particular timing-core definition gives `c_f=2^(8/9)=1.852`; it misses the required phenomenology. Pure power-law infall has no slope-2 radius selecting a formation concentration. |
| X47 | The peak-pull threshold is a restatement of the fixed surface density by construction. The local reading cannot retain an at-floor core and destroys late growth. The object reading avoids those tests by prescription; its action is missing. |
| X48 A2 | Nine-seed medians are `11.63/8.22/7.31`; 8/27 slope-2 radii are resolution-limited. Inserting them into X43 fails SPARC's mass-to-light criterion and three cluster keys. It is not a converged measurement establishing the required core parameter. |
| DT1 | Its seven specified candidate thresholds fail to derive the desired native threshold. This finite candidate menu is not an exhaustive no-go theorem. |
| CL2/CL3 | Scaling a chosen native concentration shape by external level `L`, then defining `T` from its crossover, leaves one calibrated number. Selected canonical aggregate lines pass at `L=3.75/3.9`. All three held-out suites fail, and the tested MW/lensing requirements `T<10^11.9` and `T>10^12.15` do not overlap. |
| CA1 | Selected covariant operators can conditionally match a velocity-power slope, but the amplitude requires a new coupling/mass. Pair-potential coefficients and the existence/sign of the proposed potentials are disclosed as recalled and unverified. Algebraic dimensional counting does not establish those physical arrows. |

CL3's reduction from two fitted numbers to one is genuine parameter compression, but **not parameter derivation**. Write locally `Sigma_coll=A*(M/Mref)^alpha` and `eta=C*L^(5/4)`. The definition `eta*Sigma_coll(T)=Sigma_floor` gives

\[
T=M_{\rm ref}\left[\frac{\Sigma_{\rm floor}}{CA L^{5/4}}\right]^{1/\alpha},
\qquad
\frac{d\ln T}{d\ln L}=-\frac{5}{4\alpha}.
\]

At `alpha=0.23` the sensitivity is `-5.43`. This local-power approximation is explanatory; CL3 actually solves the numerical collapse table. The threshold remains strongly dependent on the externally selected concentration level. The construction additionally assumes that the **profile crossover** is the **force-law switch**; equality of two densities alone gives no dynamical reason for switching which force acts.

There is a separate exact limitation on the emergent-law claim. Suppose an isolated spherical baryon profile has `rho_b(0)>0` finite and the halo is also cored with finite central density. Then `M_b(r)=4*pi*rho_b(0)*r³/3+o(r³)` and the total Newtonian acceleration is `O(r)`. Either MOND law above requires `g~sqrt(a0*gN)=O(sqrt(r))` with nonzero coefficient. The ratio of the cored model to the required law tends to zero at the origin. Thus a finite Burkert core cannot reproduce an exact isolated deep-MOND law at every radius of such a baryonic core. This does not exclude approximate fits over measured radii, nonspherical systems, external-field dominated systems, or cusped/pointlike baryons.

The old statement “no constants tuned” must be read together with its chosen profile family, compact root/saturation rule, collapse convention, external or numerically unresolved concentration, halo–baryon relation, and floor. Some are model assumptions rather than scalar fit parameters, but they still affect predictions. Calling the cold component a field changes no gravitating observable until its stress tensor, dynamics and initial data differ from the dust model being used.

## 5. Minimum contract for a physically predictive completion

1. **One versioned model identity:** choose S or B, distinguish v3s, route E and the hybrid, and tag every likelihood and theorem with that choice. State SI/geometric units and a0 footing explicitly.
2. **Closed dynamics:** give an action or complete conserved evolution equations for the metric, cold component, acceleration field if present, and any switch/core physics. Derive energy–momentum transfer and the source seen by baryons and lensing. A profile-selection rule alone is not this.
3. **Inputs and parameter policy:** declare `kappa`, abundance, initial perturbations, core parameters, screening lengths and free functions. A mechanism may predict them or a fixed calibration may measure them. Object-by-object hidden prescriptions must be represented in that accounting.
4. **Well-defined solutions:** specify initial/boundary conditions, multistream or caustic treatment, and a domain where the coupled dynamics exists and remains stable. A convex stationary leaf problem is weaker than a globally well-posed spacetime evolution.
5. **One forward prediction map:** the same halo population and source law must generate rotation curves, vertical force, dwarf dispersion, lensing, and cosmological growth. Include profile scatter and selection assumptions before inference.
6. **Out-of-sample viability and numerical convergence:** confront held-out constraints under predeclared uncertainties and show concentration/core predictions converge. Existing CL3 held-out failures preclude closure of that model even if its single constant were derived exactly tomorrow.

These are separate obligations. Fixing the law/certificate dictionary is cheap and necessary. Deriving `kappa=1/2` alone would not supply the missing cold-sector dynamics. Conversely, a successful closed dynamics with fitted `kappa` could be physically predictive without having derived the coefficient.

## 6. Dependency and obligation record

`(Lambda,rho_Lambda)` —Einstein conversion→ `a0=kappa*c*sqrt(G*rho_Lambda)` —**free kappa**→ acceleration scale.

`J_S` —stationary spherical reduction→ **S law** —P4/CL3 implementations→ S-model data results.

`affine squared excess` —EQB algebra→ **B law** —EQB landmarks/EFE certificates→ B-model conditional claims.

The asserted edge joining S and B is **failed**. The deep-limit BTFR is common to both; exact finite-acceleration shape is not.

`collapse input P(k), formation convention, core-radius selection, Burkert profile` → `eta*Sigma_coll`; **postulated floor** → `max(floor,collapse)`; **chosen concentration level** → **defined crossover**; **extra switch postulate** → hybrid law. No audited action here closes these last three arrows.

| Obligation | Status |
|---|---|
| Algebraic S/B equivalence | **Failed:** exact `x=1,y=1/2` counterexample |
| Correct derivatives of the two action kernels | **Passed:** explicit differentiation; symbolic check |
| kappa fixed by conversion/covariance/limits | **Failed as an implication:** continuous counterfamily |
| kappa fixed by the recorded four-form premises | **Failed as an implication:** explicit positive-parameter countermodels |
| X43 eta normalization from its stated matching assumptions | **Conditional:** assumptions retained, numeric coefficient checked; external infall theorem not re-audited here |
| X48 concentration convergence | **Not established:** record explicitly reports unresolved radii/resolution |
| CL3 threshold physically selected | **Incomplete:** crossover-as-switch and L remain inputs |
| Same CL3 model passes held-out tests | **Failed in recorded tests:** no production rerun here |
| Full modified-gravity/cold-sector cosmology | **Not addressed by the new kernel integrals; remains open/failed in named existing models** |

## 7. Verification and residual scope

The self-contained [check_foundations.py](check_foundations.py) checks 13 exact symbolic identities. It extracts only `nu1` and `g_from_gN` from P4's AST and checks their agreement at 2,001 positive points from `1e-10` to `1e10`. It imports no simulation engine. The universal mismatch bound and coefficient underdetermination have handwritten algebraic proofs above; the finite grid is a source-to-dictionary check only.

The bounded run completed in [run_001/manifest.json](run_001/manifest.json); numerical details are in [run_001/result.json](run_001/result.json). Its input hashes were checked before and after execution. Reproduce with the exact argv recorded in that manifest; the mathematical contract is [CONTRACT.json](CONTRACT.json). No heavy simulations, data-fitting jobs, commits or pushes were performed.

Sources and exact application limits are recorded in [SOURCE_CHECKS.md](SOURCE_CHECKS.md). The cheapest next action is the documentary S/B correction above, followed by a single selected-model forward contract. More parameter tournaments cannot substitute for the missing action-to-observable implication.

Self-proofreading covered this report and the source note: notation, dimensions, scope qualifications, displayed algebra and references. No original manuscript tokens were changed.
