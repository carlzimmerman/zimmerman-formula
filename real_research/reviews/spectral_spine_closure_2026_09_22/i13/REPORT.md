# I13: physical radial operator to the algebraic spine

Checked 2026-09-22 against checkpoint `e3af62a453ca6625db8428f6d32957b27a7f1331`.

**Verdict: incomplete, with the smallest missing implication now isolated.**
The universal identification of I13's `omega2` with the fundamental radial eigenvalue is false in general. A genuine comparison is proved below: a normalized I13 expression is the leading post-Newtonian **homologous trial quotient**. It is an upper bound on the lowest eigenvalue of the corresponding variational problem, subject to its operator/domain hypotheses. The exact Newtonian and relativistic forms also give explicit lower bounds through a positive comparison function. These are mathematical derivations, not Lean certifications of the differential operator. The numerical implementation tests the operator itself on synthetic equilibria; it does not import MESA profiles or infer a physical mass ceiling.

## 1. Claim and conventions

Let `xi(r) exp(i Omega t)` be the radial displacement and `eta=xi/r` the fractional displacement. `Omega` is dimensional angular frequency; `lambda0=Omega0²` is the bottom radial eigenvalue. Radius is `R`; density is `rho`; pressure is `P`; adiabatic exponent is `Gamma`; enclosed gravitational mass is `m`; `G` and `c` retain their usual dimensions. Surface compactness is `x=2GM/(Rc²)`.

Assume a spherical static equilibrium, `P>0`, `rho>0` on `(0,R)`, `Gamma>0`, and a regular center. At a vacuum surface impose the natural pressure boundary condition; require all displayed integrations by parts to have vanishing endpoint terms. Smooth compactly supported variations and their closure in the radial energy norm give the form domain. When speaking of an eigenvalue rather than merely a form infimum, additionally assume the corresponding lower-bounded self-adjoint realization has an attained lowest eigenvalue. These hypotheses exclude treating arbitrary functions allowed in I13's moment inequalities as physical equilibria. Rotation, dissipation, nonadiabatic driving, accretion boundary terms, and a central black-hole inner boundary are outside this theorem.

## 2. Exact Newtonian bridge

Linearized Newtonian radial force balance is

`(Gamma P r⁴ eta')' + r³[(3 Gamma-4)P]' eta + Omega² rho r⁴ eta = 0`.

Put `K=3 Gamma-4`, `J[eta]=integral rho r⁴ eta² dr`. Multiplication by `eta` and integration by parts give

`N_N[eta] = integral {Gamma P r⁴ eta'² - r³(KP)' eta²} dr`,

`Omega² = N_N[eta]/J[eta]` for an eigenfunction. For an arbitrary nonzero admissible displacement the quotient is instead a trial value. A second integration by parts, using `[r³KP eta²]_0^R=0`, gives the derivative-free equivalent

`N_N[eta] = integral P{Gamma r⁴ eta'² + 2K r³ eta eta' + 3K r² eta²} dr`.

Equivalently, writing `delta=Gamma-4/3`,

`N_N[eta] = integral P{(4/3)r⁴ eta'² + delta r²(r eta'+3 eta)²} dr`.  (N1)

This last identity is an exact completion of squares, including spatially varying `Gamma`; no derivative of `Gamma` has been dropped. Thus `Gamma>=4/3` pointwise makes the Newtonian form nonnegative. If `Gamma>4/3` on a positive-measure set, its only possible zero-energy function is zero: the first term forces a constant `eta`, and the second then forces that constant to vanish. Under the attained-bottom hypothesis this makes the lowest eigenvalue positive. For `Gamma=4/3` identically, `eta=1` is an exact zero mode and the whole form is nonnegative.

For the homologous trial `eta=1`,

`Q_N[1] = 3 Wbeta/J`,

`Wbeta=integral (3 Gamma-4)P r² dr`, `J=integral rho r⁴ dr`.

I13 defines `omega2(Wbeta,Wgr,I,Cgr,0)=Wbeta/I`. It equals this physical trial quotient only after specifying **`I=J/3`**. If a conventional modal inertia `4 pi J` is used, the pressure numerator needs the same angular normalization and the factor 3; it cannot be omitted by calling `I` a modal inertia.

The minimum principle gives `lambda0 <= 3 Wbeta/J`. Equality holds only when `eta=1` is a minimizing eigenfunction. Its exact residual is

`L_N 1 = -r³(KP)'`.

Hence equality requires `-(KP)'/(rho r)` to be constant (almost everywhere). If `Gamma` is a constant different from `4/3`, Newtonian hydrostatic balance `P'=-Gm rho/r²` reduces this condition to constancy of `m/r³`. Thus a nonuniform-density `n=3` polytrope with constant `Gamma>4/3` cannot have the I13 trial value as its fundamental eigenvalue. This is an exact obstruction, independent of the numerical solver.

For constant `Gamma>4/3`, a simple genuine enclosure is

`K essinf(Gm/r³) <= lambda0 <= 3 K integral P r² dr/J`.

The lower inequality follows directly from the first form and `Gamma P r⁴ eta'²>=0`. In a decreasing-density star its lower endpoint is `K GM/R³`. More generally the completed-square argument above proves the Newtonian gas-pressure stability statement even when the local residual is not positive.

## 3. Exact relativistic comparison

Source contract: the radial equation and metric conventions are those of Saio et al., arXiv:2406.18040v1, equations (2)–(5). Their density convention omits an additional internal-energy correction. The calculation here uses that same convention; it is not a claim that this omission is a complete stellar equation of state. Source details and the limited extraction are in `source_record.json`.

Define `z=e^(-a) r² xi=e^(-a)r³ eta`. Rearrangement of the source differential equation yields

`-(Pi z')' + V z = sigma² W z`, `Omega=c sigma`,

`Pi = exp(3a+b) Gamma P/r²`,

`V = exp(3a+b)/r² * [4P'/r + 8pi G exp(2b)P(P+rho c²)/c⁴ - P'²/(P+rho c²)]`,

`W = exp(a+3b)(P+rho c²)/r²`.

Consequently the **exact**, untruncated variational comparison is

`lambda0 <= Q_GR[z] := c² integral(Pi z'²+V z²)dr / integral W z² dr`.  (G1)

This is not a renamed definition: the differential equation, displacement transformation, metric factors, potential, weight, and boundary terms have all been identified. Negativity of any admissible trial numerator proves a negative bottom eigenvalue; positivity of one trial numerator does not prove stability.

A lower comparison is available too. For any positive comparison function `u` with the same endpoint compatibility, let `q_u=c²[-(Pi u')'+Vu]/(Wu)`. For every test function `z`, elementary differentiation and integration by parts give the ground-state identity

`integral(Pi z'²+V z²) - integral [-(Pi u')'+Vu] z²/u`

`= integral Pi u² ((z/u)')² >= 0`.  (G2)

The boundary term is `[Pi u' z²/u]_0^R` and must vanish. Therefore

`essinf q_u <= lambda0 <= Q_GR[u]`.  (G3)

If `q_u` is constant, both bounds agree. A positive lower endpoint certifies radial stability. A negative upper endpoint certifies instability. A straddling interval is explicitly inconclusive. This supplies the missing *type* of lower comparison rather than treating a positive Rayleigh value as sufficient. Existence and endpoint assumptions remain explicit.

### A stable formula for computation

Using exact TOV balance `P'=-(P+rho c²)a'` and `a'+b'=4pi G r exp(2b)(P+rho c²)/c⁴`, integrate out the total derivative `4(exp(a+b)Pr³ eta²)'`. Then

`N_GR[eta] = integral exp(a+b) [Gamma P r⁴ eta'²`

`+ 2P r³(K-Gamma r a') eta eta'`

`+ {3KP r² -(6Gamma+2)Pr³a' -2Pr³b' +[(Gamma-1)P-rho c²]r⁴ a'²} eta²] dr`,

`D_GR[eta] = integral exp(-a+3b)(rho+P/c²)r⁴ eta² dr`.

The ratio is the dimensional `Omega²` trial quotient. The removed boundary term vanishes for the center and vacuum surface used here. The script independently assembles this formula and the original form (G1); the maximum matrix-entry difference in the tested model is about `2.36e-12`. This provides a numerical check on the cancellation and signs, not a substitute for the derivation.

## 4. Post-Newtonian trial spine with its actual error scope

Take a weak-field sequence around a fixed Newtonian equilibrium, with `Gamma-4/3=O(epsilon)` and `Gm/(rc²)=O(epsilon)`. Evaluate leading integrals on that Newtonian background. For `eta=1`, expansion of the exact formula gives

`N_GR[1] = 3 Wbeta - H/c² + O(epsilon²)` in the corresponding pressure-work scale,

`H = integral [8G P m r + 8pi G P rho r⁴ + G² rho m²] dr > 0`,

`D_GR[1] = J + O(epsilon)` in the inertia scale.

All three positive terms in `H` are necessary; this is a structure integral, not a universal Coulomb constant. Since the numerator is already first order, the inertia correction contributes only at second order to the frequency.

Thus the leading trial quotient has exactly I13's algebraic form if

`I=J/3`, `Cgr=H R/(6GM Wgr)`, `Wgr=integral P r² dr`:

`Q_PN[1] = (Wbeta-Cgr*x*Wgr)/(J/3)`.

Here `Cgr` is computed from the chosen profile. The identity is a first-order expansion, not exact linear dependence of the physical eigenvalue on compactness. Along an evolving stellar sequence, even the background moments, radius, density shape, and effective coefficient can change.

A strict negative numerator certifies instability **for the truncated variational model**. To transfer the sign to the full GR operator one needs either its exact trial numerator or an explicit remainder bound. If `|N_GR[1]-(3Wbeta-H/c²)|<=E`, the sufficient full-model criterion is `3Wbeta-H/c²+E<0`. No finite-compactness remainder estimate is hidden in the `O(epsilon²)` notation. Near equality the first-order test alone is inconclusive.

For a smooth perturbation of the Newtonian `Gamma=4/3` simple zero mode, ordinary eigenvalue perturbation theory also gives first-order agreement of the fundamental eigenvalue with this trial quotient. Such agreement requires the stated simple isolated eigenvalue and regular perturbation hypotheses; it is not exact equality away from the limit, and those analytic hypotheses are not formalized here.

## 5. Actual benchmarks and counterexample to the proposed identification

The script generates its own equilibria, solves the two-variable TOV/Lane–Emden system, and assembles continuous piecewise-linear Rayleigh–Ritz forms with eight-point Gauss quadrature. Its grid is uniform in radius. No endpoint is a quadrature node. Its form domain imposes the natural surface condition, not an artificial zero displacement at the surface. Binary64 and adaptive numerical integration mean computed numbers are not rigorous interval enclosures.

* Uniform-density Newtonian star, `G=rho=R=1`: `eta=1` is an exact fundamental eigenfunction with `Omega²=(3Gamma-4)*4pi/3`. The code checks `Gamma=1.2,4/3,5/3`. An independent exact rational integration gives the uniform-density PN threshold coefficient `19/42`, so the I13-normalized coefficient is `19/14`. This also shows why an asserted universal `[2.25,3.35]` band cannot be transferred across coefficient conventions.
* Newtonian `n=3`: radius `6.89684861937`, dimensionless mass moment `2.01823595097`. At `Gamma=4/3`, the zero mode is recovered. At `Gamma=1.5`, the homologous value is `0.512946931993`, while the 256-cell Ritz value is `0.425923510859`, a `20.43%` excess of the trial value. Nested 32/64/128/256-cell spaces lower the Ritz value monotonically; this is a convergence check, not a lower eigenvalue bound.
* Integrating the PN correction on `n=3` gives `H R/(18GM Wgr)=1.124474311979`, which rounds to the independent `1.1245` source benchmark. Therefore `Cgr=3.373422935937`. The previously recorded `3.35` upper endpoint is too low under I13's stated `3Gamma-4` normalization. This result uses no fitted parameter.
* Full TOV `n=3`, `s=Pc/(rho_c c²)=0.001`, compactness `0.002325278673`: at `Gamma=1.335967888598`, the homogeneous trial is `+2.41886e-7`, while the 256-cell Ritz value is `-2.42086e-7`. Thus a numerically obtained admissible displacement has negative work while the homogeneous displacement has positive work. The critical `Gamma` is stable to `7.8e-12` between 128 and 256 cells; the raw and stabilized forms agree. The example is numerical evidence, not a validated-interval counterexample.
* The full-operator critical slope `(Gamma_crit-4/3)/x` tends toward the independently integrated PN coefficient as `s` decreases over `1e-3,3e-4,1e-4,3e-5`.

## 6. Dependency/obligation audit and remaining work

| Obligation | Status | Evidence |
|---|---|---|
| Gas+radiation algebraic kernel | existing Lean result | I13, unchanged theorem statements |
| Newtonian operator to exact work form | proved by integration by parts | section 2, endpoint assumptions explicit |
| Newtonian nonnegative-form criterion | proved | completed-square identity (N1) |
| Homology is fundamental mode generally | refuted | residual condition; nonuniform constant-Gamma polytrope |
| GR ODE to self-adjoint work form | derived from checked source equation | section 3 |
| Correct instability comparison | proved under the specified spectral/domain contract | (G1)–(G3) |
| Positive homology trial implies stability | invalid in general | lower bound required; numerical TOV example |
| Leading PN structural coefficient | derived; numerical n=3 evaluation | section 4 and benchmark output |
| Full GR finite-compactness PN remainder | not bounded | use exact form or supply `E` |
| MESA/GENEC physical profiles | unavailable locally in searched filenames | no fabricated data |
| Actual accreting SMS or BH-envelope eigenvalue | not computed | equilibrium, EOS, boundary data required |
| Mass cutoff `10^5–10^6 M_sun` from I13 alone | not established | no mass sequence or profile import |

The next necessary input is an authenticated equilibrium sequence with `r,m,rho,P,Gamma1` and its density/internal-energy conventions, plus inner/outer mechanical boundary conditions. For a BH envelope the inner boundary cannot be replaced silently by a regular stellar center. Compute the exact GR form and solve or rigorously bracket the lowest radial mode for each model. A profile-weighted `beta` moment by itself is insufficient. A mass–radius relation and evolution track are also necessary to turn an instability condition into a mass ceiling.

## 7. Reproduction and provenance

`radial_bridge.py` is the complete deterministic solver and benchmark suite. `contract.json` declares the bounds. `run/manifest.json` captures input hashes, command, repository checkpoint, environment, resource caps, outputs, and actual exit status. `run/results.json` contains scientific results; `run/stdout.txt` is the preserved raw output. `symbolic_identities.py` independently checks four exact local identities, with its own `symbolic_run/manifest.json` and output. These checks do not prove boundary conditions or spectral existence. `verification.json` records the Lean run and confirms the theorem/proof text is unchanged after comment removal. `source_record.json` pins the literature version and interpretation. `hashes.sha256` pins the final artifacts.

The numerical result is **implementation and finite assertion verified in the stated range, conditional on binary64 tolerances and SciPy**, not a universal proof or an interval-certified spectrum. The derivations were self-reviewed; no independent human or external theorem prover has checked the differential analysis.

Reproduction from the repository root:

```sh
python3 real_research/reviews/spectral_spine_closure_2026_09_22/i13/radial_bridge.py --output /tmp/i13_results.json
python3 real_research/reviews/spectral_spine_closure_2026_09_22/i13/symbolic_identities.py /tmp/i13_symbolic_results.json
cd fable_independent_2026/lean_2026
lake env lean I13_bhstar_pulsation.lean
```

The preserved runs contain 17 successful numerical assertions and four exact symbolic checks. The Lean verification exits 0 and prints only `propext`, `Classical.choice`, and `Quot.sound` for its listed certificates. No new spectral theorem is claimed as Lean-certified.
