# Independent CT09 focused review

**Normalized claim.** For a constant-positive-kinetic-coefficient homogeneous scalar on a slowly evolving closed orbit, phase-dependent collision losses change its action by an orbit covariance, in addition to Hubble dilution. For the specified four-dimensional rigid-tree singlet pole, a positive neutral width matrix and any positive incoming width imply a uniform coherent-resolvent bound. With the specified factorized, gauge-symmetric charged population and entropy-conserving cosmological comparison, this supplies a conditional bound on depletion by that pole alone.

**Primary verdict: correct only after a stated restriction.** The action identity and matrix inequality reconstruct correctly. The numerical pole normalizations also reconstruct. The depletion statement requires the fixed pole coefficients, the six-component uncorrelated ensemble, the conserved reference entropy and the declared starting epoch. It is not an exclusion of the full model, arbitrary pair correlations, an earlier medium history, or the new lower-mu candidate. No physical finite-order resonance alignment or final abundance is established by the separate vacuum-placement profiles.

Review provenance: fresh independent subagent derivation, using `mathbox:proof-audit` and `mathbox:computation-audit`; shared canonical component model explicitly retained as a dependency. All review writes are inside this directory. Exact revisions are the SHA-256 records in `SOURCE_HASHES.json`, captured 2026-11-04. The final independent bounded run is `run_003/manifest.json`, schema v2, status `completed`, checkpoint `2e8b3f8064cb6a0917ec8f637d8bb42fc0caef7b`, dirty workspace. A checkpoint alone does not identify these uncommitted sources; the hashes do.

## Actionable findings

1. State the ensemble restriction wherever the cosmological envelope is described as independent of the distribution. It is independent of the momentum shape within a gauge-covariant, factorized Boltzmann population. It does not bound a general correlated two-particle density matrix. The initial common FD occupation and a singlet background support the needed one-particle symmetry, provided the reduced collision operator preserves it.
2. Retain the epoch qualification for the bosonic-width envelope. At the original protected scale, all-FFS-blocked maximal-pole depletion gives lower-yield/gate ratios about **3.583** from `Tc/mu=.001` and **7.166** from `.0005`, but **0.769** from `.00466`. The earliest comparison therefore does not exclude reaching the gate. An envelope permitting the gate is not an actual successful history.
3. Retain the fixed-width/positive-rate medium restriction. Arbitrary Hermitian real-part mixing inside the four retained poles is covered. Changed absorptive matrices, shifted daughter thresholds, gain in a nonequilibrium retarded self energy, or mixing with extra neutral states are not covered merely by retuning H.
4. Keep the finite local vacuum and matched leading trajectory profiles distinct. Their different epsilon values and truncations cannot be combined into a finite physical resonance claim. The inspected leading-profile script checks separate radial/phase/modulus diagonal curvatures; it does not by those checks alone certify the full mixed neutral Hessian of that new action.

## Claim cards and dependency graph

| Card | Exact statement and hypotheses | Verdict |
|---|---|---|
| A | With K>0 constant, differentiable bound orbit, slowly varying H and collision parameters, fixed comoving momentum labels, and no coherent field recoil, `Idot=-3 H I+P sum_i Cov(epsilon_i,C_i)` to leading averaging order; I is the unnormalized physical-volume action and C_i is the physical density collision term. | Proved as written under these explicit hypotheses. |
| B | For finite matrices `Gamma_o>0`, `Gamma_i>=0`, `H=H†`, `G>=0`, `M>0`, and `E>=m>0`, the fixed model `D=(H+i M(Gamma_o+Gamma_i))^-1` satisfies `sigma_pair v=(2/E)Tr[G D Gamma_o D†] <= 2 Tr[G Gamma_o^-1]/(m M^2)`. | Proved as written for this fixed finite model. |
| C | The real-state projected Gram `G_ab=sum_ij C_aij C_bij/12^2` gives the physical six-by-six particle/antiparticle average `G_pair=2G`; for a charge-symmetric total carrier density, the loss term is `-sigma_pair v n^2/2`. | Correct with the averaging/factorization convention stated. |
| D | With the original protected scale, specified initial yields and start temperatures, constant mass on the fixed pole, no returning neutral carriers, conserved reference entropy, and `H>=H_star/a^2`, integrate the constant maximum rate to obtain a lower remaining yield. | Computationally verified only for the listed comparisons; analytic comparison conditional on those inputs. |
| E | Turning off all FFS widths but retaining the vacuum SSS matrix enlarges the bound to `97360.19095551 mu^-2`; the postcapture original-scale comparisons still miss the gate. | Correct for positive additive rate matrices retaining this bosonic floor. |
| F | Finite local scalar placement and the separately retuned leading profile supply a physical, finite matched resonance or full kinetic abundance. | Not established; explicitly outside the artifacts' stated scope. |

Dependency graph:

```text
scalar equation + parameter-dependent action derivatives
  -> phase covariance + expansion work -> A
canonical SU5 component potential/model + real/complex normalization
  -> cubic/Yukawa tensors -> projected G and unordered SS/FF widths -> C
Gamma_o>0 + Gamma_i>=0 + Hermitian H + G>=0 -> B
B + C + fixed mass/scale + start epoch + conserved entropy + H floor -> D
Gamma_SSS>0 + nonnegative additional widths -> enlarged B -> E
finite normal/two-loop vacuum calculation -> local finite placement
separate rigid-valley tree-gravity+CW action -> leading placement
neither placement branch -> finite quantum pole or full collision network
```

The canonical component model and its input superpotential/generator conventions remain a shared input, not a new audit of all prior finite-matching or gravity claims. The fresh control checks a load-bearing cubic directly against the underlying scalar potential rather than only comparing two contractions of the same exported vertex tensor.

## Decisive reconstruction

### Action, collisions and expansion

Use physical densities n_i in fixed comoving momentum cells, so `ndot_i=-3H n_i+C_i`, and write

```text
U=V(x)+sum_i n_i epsilon_i(x,a),
I=closed_integral K xdot dx, P=I_E,
I_ni=-P <epsilon_i>, I_a=-P <U_a>.
```

The field equation is `K(xddot+3H xdot)+U_x=0`. Hence

```text
Edot=-3H K xdot^2 + sum_i epsilon_i(-3H n_i+C_i) + U_a adot.
```

Insert this into `Idot=P Edot+sum I_ni ndot_i+I_a adot` and average at fixed slow parameters. The explicit a derivative cancels. The phase-independent `-3H n_i` terms cancel against their parameter derivatives. Finally `P<K xdot^2>=I`, giving A. Thus the comoving canonical action obeys

```text
d(a^3 I)/dt = a^3 P sum_i Cov(epsilon_i,C_i).
```

If occupations f_i rather than physical densities are used, the a^-3 weights stay outside each covariance, as in the inspected kinetic derivation. These two representations must not be mixed. The emitted energy must appear once in the daughter/radiation ledger. A number-only sink does not fix the covariance or the momentum-dependent daughter force.

For `epsilon=m0+alpha x^2/2` and `C=-gamma n(1+beta x^2)`, `Var(x^2)=A^4/8` gives `Cov=-gamma n alpha beta A^4/16`. There is no universal sign: beta>0 cools the action, beta<0 heats it, while beta=0 has zero leading collision covariance. Disappearance of the bound orbit, a separatrix crossing, or rates not slow relative to the orbital frequency invalidate this averaging step.

### Resolvent order and mixing

Let `Gamma=Gamma_o+Gamma_i`, `S=Gamma^-1/2`, and `B=S H S=B†`. Then

```text
D=S (B+i M I)^-1 S,
D Gamma D† = S (B^2+M^2 I)^-1 S <= Gamma^-1/M^2.
```

Congruence preserves positive order, so `D Gamma_o D†<=D Gamma D†`. Inversion reverses positive order, giving `Gamma^-1<=Gamma_o^-1`. Taking the trace against `G>=0` and using `E>=m` proves B. No commutativity of H, G or either width is required. Equality is attained at `H=0`, `Gamma_i=0`, `E=m`. Positive definiteness of Gamma_o is essential to the displayed inverse; a singular-width case would require a separate support/kernel analysis.

This proof permits any Hermitian four-by-four H, including coherent mixing among the retained singlets. It does not preserve the numerical bound if additional poles are introduced, if their elimination changes the effective absorptive matrix, or if the physical self energies are energy/medium dependent beyond the stated fixed coefficients. The velocity tables use `2/m` and the on-shell matrices as a narrow near-threshold packet; they are not an exact arbitrary-energy relativistic amplitude calculation. The mathematical envelope remains valid for the declared fixed-coefficient model with the physical `2/E` prefactor.

### Physical pair and total-density normalization

For one complex component `C=(r1+i r2)/sqrt(2)`, the invariant interaction `-kappa S |C|^2` is `-kappa S(r1^2+r2^2)/2`. On a six-dimensional irreducible charged multiplet, singlet couplings are proportional to the identity. The real ordered sum has twelve terms, while the physical complex particle-antiparticle sum has six. Consequently

```text
G_real=(12 kappa_a kappa_b)/12^2=kappa_a kappa_b/12,
G_pair=(6 kappa_a kappa_b)/6^2=kappa_a kappa_b/6=2 G_real.
```

The physical incoming flux in `sigma v_rel` is `4E^2`. The integrated neutral final-state tensor is `2 sqrt(s) Gamma_o`, with `sqrt(s)=2E`. Multiplying by the physical pair Gram produces `(2/E)Tr[G D Gamma_o D†]`. At rest, the incoming charged-pair width vanishes at exact threshold, so the stated rest value saturates the fixed-width bound. The independent unordered width reconstruction uses `1/(1+delta_ij)` explicitly, reproducing the ordered identical-state factors.

For an uncorrelated gas, each event removes two carriers, so `ndot+3Hn=-2 sigma_pair v n_+ n_-`. Charge symmetry gives `n_+=n_-=n/2`, and hence the factor `1/2` in the total-n equation. Charge asymmetry would reduce the maximum loss at fixed n, but arbitrary gauge-component composition or pair correlations require their own cross-section average.

For the admitted kinetic closure, SU3 x SU2 covariance and irreducibility imply `rho_+(p)=f_+(p) I_6` and `rho_-(p)=f_-(p) I_6` by Schur's lemma. Factorization then gives exactly the six-by-six pair average, without requiring an FD momentum shape. Covariance alone does not fix a general two-particle density matrix: `6 tensor 6bar` admits different invariant pair channels. For illustration, concentrating an uncorrelated product population in one aligned component enhances the singlet production relative to the uniform average by six; a normalized coherent singlet pair has an enhancement of thirty-six. These examples are outside the factorized gauge-symmetric population used in D, and no such enhancement is claimed to arise in this model's prescribed initial history.

### Cosmological scope and thermal blocking

With `Y=n/s`, `s=s_star/a^3` and no entropy dilution, the forward-only comparison gives

```text
d(1/Y)/dt = s sigma_pair v/2,
L <= s_star sigma_max/(2 H_star) integral_1^af da/a^2,
Yf >= (1/Ystar+L)^-1.
```

The Hubble floor uses the redshifted initial visible radiation; extra positive gravitating sources increase H and reduce the allowed loss integral. The entropy assumption is separate: late visible entropy production would change Y and is not bounded by this argument. The mass and microphysical scale are held fixed at the chosen pole. The envelope favors loss by keeping every carrier scalar, every phase/velocity maximally aligned, and all neutral products permanently removed. It does not compare self-consistent force histories for other channels or prove that the same alignment persists in the physical orbit.

For `mu=18170662.111498855 GeV`, `mC=703746.71747 GeV` and the chosen 10%-DM charged gate `Ygate=6.25224941126e-17`, the recorded original-protected comparisons at `Ystar=3.74544e-7` are:

| Start Tc/mu | Vacuum-width Ylower/Ygate | All FFS blocked Ylower/Ygate |
|---:|---:|---:|
| .00466 | 4.7553 | .76887 |
| .003 | 7.3866 | 1.1943 |
| .001 | 22.1597 | 3.5830 |
| .0005 | 44.3193 | 7.1659 |

The SSS matrix remains positive definite, with smallest eigenvalue `5.15133059e-11 mu`, and supplies the finite enlarged envelope even when every FFS contribution is deleted. This covers positive Pauli suppression of those fermion rates, retaining vacuum bosonic thresholds/couplings and at least spontaneous SSS widths. It does not cover negative retarded damping/gain, displaced thresholds that close the SSS exits, general medium vertex changes, or a different production residue. Inverse processes remain part of the missing physical history; deleting them is favorable to depletion in the stated loss comparison.

The new `mu=2e6 GeV` candidate changes the dimensionful cross section and charged-yield gate. The original protected-scale obstruction cannot be transferred to it. Likewise, the gate-passing earliest blocked envelope supplies no affirmative abundance prediction.

## Fresh computation and provenance

The fresh control imports `model.py` and its `spectrum.py` dependency, **not** `pole_network.py`, `pole_matrix_v2.py` or `pole_medium.py`. It constructs the real signed-charge rotation generator, projects its six positive and six negative eigenvectors, sums unordered SSS/FFS final states, checks a cubic against a direct mixed third derivative of `V_F+V_D`, and tests 128 fresh noncommuting matrix controls. Its oscillator includes Hubble friction, physical-density dilution, explicit redshifted particle kinetic energy, radiation and integrated Hubble work.

Final run (`run_003`): **completed**, 180-s wall cap, 175-s CPU cap, conventional numerical-library thread cap one; no CPU-affinity cap or memory cap was claimed. Runner wall time **7.642634 s**, measured program time **5.415881 s**, measured macOS peak RSS **185729024 bytes**. Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4; all actual project input hashes are observed before/after in the v2 manifest. `validate_manifest.py --root PROJECT` passes. The original five reviewed runs also have completed status and their input/output hashes were rechecked with no mismatches at review time.

| Fresh finite check | Result |
|---|---:|
| Signed charge eigenvalues | six each of `+/-sqrt(5/12)` |
| `G_pair=2G` relative error | `3.73e-16` |
| Potential derivative vs exported cubic relative error | `2.14e-12` |
| Reconstructed vacuum peak | `15741.9998372461 mu^-2` |
| Reconstructed SSS-floor peak | `97360.1909555103 mu^-2` |
| Minimum normalized PSD residual, 128 controls | `.00653798` |
| Maximum expansion/action relative error, three beta cases | `4.21e-9` |
| Maximum total work/energy ledger error | `6.71e-10` |
| Error on omitting collision covariance, beta nonzero | about `.00183-.00184` |

The random matrix cases are finite implementation controls, not the proof. The oscillator controls verify a deliberately simple analytic example, not the SU5 collision operator. No uniform floating-point error certificate or full kinetic network is inferred.

Execution history is retained: `run_001` failed while serializing NumPy booleans and did not create its result; it is not evidence of a mathematical failure. `run_002` completed, but its `correlated_component_upper_multiplier=6` label applied only to aligned product states and was too broad. `control_v3.py`/`run_003` correctly distinguish the product-state factor six from the coherent-singlet example factor thirty-six. No failed or intermediate record was overwritten.

Reproduction command is exactly the argv in `run_003/manifest.json`, after verifying its contract and input hashes; the bounded launch is documented by `contract_v3.json`. A rerun requires a new output directory. Validator:

```text
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/coupled_trapping_2026_11_04/independent_review/run_003/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

## Placement-profile scope and remaining obligations

Read-only source inspection confirms that `place.py`/`place_candidate.py` solve the finite local normal/two-loop scalar problem and export a separate leading rigid-valley global potential. A finite target `x=tree_pole-.001` does not force that different potential to have the same minimum. `LEADING_PROFILE_CONTRACT.md` now records this mismatch. `leading_profile.py` constructs its own tree-gravity-plus-CW action and solves its own stationarity and normalization at the rigid tree threshold, with dense near-pole force samples. Its epsilon is `.02486163225414`, while the lighter finite local candidate uses `.02492017415003`. The distinct scope labels are scientifically necessary.

This supplementary placement inspection was not a fresh reproduction of the high-precision vacuum solves, nor an audit of every upstream finite-normal action. Separate positive diagonal curvatures in the leading profile do not prove positivity of a mixed Hessian; the finite local eight-scalar positivity result belongs to its separately parameterized action. Neither result computes the finite quantum heavy-pole mass, medium detuning, transverse fermion/current matching, or the coupled charged/scalar/neutral/gaugino distribution history.

Strongest safe statement: the phase-covariance correction and normalized fixed-pole matrix envelope are sound, and the original-scale **postcapture**, positive-rate SSS-floor comparison still misses the chosen charged gate within the specified ensemble and cosmology. The earliest blocked envelope and lower-mu candidates remain open. Cheapest remaining checks are to state the ensemble/entropy restrictions beside the envelope, check the mixed radial/modulus Hessian if full leading-profile stability is claimed, and retain explicit separation between finite local placement, leading conditional dynamics and the still-uncomputed physical collision history.

## Addendum: mixed stability of the restricted leading action

The open mixed-Hessian leaf above is now addressed by the subsequently supplied `gravity_resonance/leading_stability.py` and `run_stability001`. This addendum preserves the earlier criticism as its chronological provenance; **restricted mixed local stability is now computationally verified** for the exact leading-profile constants. It does not change the core action/pole verdict or establish a full heavy-normal quantum action.

Raw source inspection confirms that the new program reloads all constants, the position, modulus and W0 coordinate from the same `run_leading001/result.json` packet. It extends precisely that rigid-valley tree-gravity-plus-rigid-CW potential to complex X and complex tau, rather than borrowing the distinct finite local candidate. It differentiates all four real directions and every mixed second derivative at 110-digit precision, with

```text
X = X_star + (r0+i r2)/sqrt(62),
tau = tau_star + (r1+i r3)/(sqrt(2 NEXP) M).
```

The corresponding linear rescaling is nonsingular. Positive definiteness of the Hessian therefore establishes a strict local minimum within these four real rigid-valley directions independently of whether the small-field scaling is the exact local kinetic normalization. The quoted masses retain the script's explicit small-field canonical-coordinate qualification.

All four recorded checks pass: stationarity in the four directions, the complete restricted Hessian's positive eigenvalues, and positive radial/modulus and phase/modulus Schur complements. The serialized minimum eigenvalue is `2.9540590286965e-17 mu^2`. The nonzero radial/modulus cross entry is `9.1958074777543e-27 mu^2`, and is included in the eigenvalue computation. The masses in the stated coordinates are

```text
(0.01087025120, 0.04347258513, 0.12963909486, 0.12963909486) GeV.
```

`run_stability001/manifest.json` is schema v2, status `completed`; root-based manifest validation passes with current input/output hashes. Its recorded runner wall time is `.709333 s`, program time `.193462292 s`, and measured macOS peak RSS `49512448 bytes`. This addendum audits the raw implementation/output and validates the recorded execution; it is not an independent fresh rerun of that high-precision solve. The new exact hashes are appended under `addenda` in `SOURCE_HASHES.json`, including:

```text
leading_stability.py:
bc47f25748cd58ff2005b9ae46f7310e6ded0c86266cd3d1f001ccd7f409afab
run_stability001/result.json:
8d26dc2373f70b3aa8392beadc0620c6fbdb74d5b6eefb93ce73d0bb08e466cb
run_stability001/manifest.json:
6611a72d277840b4814c108463368f738835722ff0a68cbefb19b2fe3da6eebb
```

Remaining scope: the four directions are complex X and tau with the heavy normal coordinates held on the rigid valley. This establishes neither the full transverse/heavy-normal Hessian of the separately parameterized finite quantum action nor a matched physical resonance, full collision network or abundance prediction.
