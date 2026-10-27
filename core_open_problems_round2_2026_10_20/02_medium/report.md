# MEDIUM round 2: derived microscopic pieces, physical selection still open

Checkpoint MEDIUM-R2-A. Frozen parent: 8aa3f7046a7ae14a99f3515fd42df5bf061fb1db. The actual computation observed live HEAD 523a099545069cf8a2b9b428f0425b583febdb2f; this lane made no Git changes. Frozen round-1 source hashes are in source_provenance.json. Only this lane's directory was written.

**The gravitational medium and n selection remain incomplete.** This round advances two of the actual missing steps: an explicit finite-state Markov chain supplies its exact source-dependent distribution and reaction affinity, including zero source; a specified gapless vector-mass Hamiltonian supplies a positive cubic free-energy term. Neither is promoted into a derivation of the full gravitational law.

## 1. Exact stochastic realization and its source limitation

The states j=0,...,N count active slots. With dimensionless pump intensity h and rate scale κ, take activation B_j=κh(N−j) and collective deactivation D_j=κj²/N. These transition rules determine

\[
\pi_j=Z_N^{-1}\frac{(Nh)^j N!}{(N-j)!(j!)^2},\qquad
\frac{B_j}{D_{j+1}}=\frac{Nh(N-j)}{(j+1)^2}.
\]

The coarse chain obeys detailed balance at positive h. The source dependence of its bare edge affinity is log h; an effective thermal energy would couple count j to −kBT log h, not polarization to acceleration. At h=0 the stationary state is exactly empty, and mean absorption time from full occupancy is (N/κ)∑j^−2. This is an absorbing-state limit with a singular effective chemical source. Hidden pump dissipation cannot be calculated without specifying its reservoir channels.

The macroscopic response is x²=h(1−x), x=j/N. Defining u=bx, b=a0/n and h=n gbar/b reproduces the round-1 root. **That last source dictionary is still assumed.** The count is scalar and the chain has no orientation operator; a gravitational vector response is not obtained merely by renaming x. The model also does not derive the conservative mechanical free energy from the mixing distribution: stationary roots alone do not equate their conjugate forces.

The finite model adds a new falsifiable qualification. Exactly,

\[
h(1-\langle x\rangle)=\langle x^2\rangle,
\quad \langle x\rangle\le x_*,
\quad \langle x\rangle\sim Nh\ (h\to0,\ N\text{ fixed}).
\]

Thus an ideal square-root law requires N√h≫1. It crosses to linear response at gbar of order b/(nN²). At fixed h in the large-N limit,

\[
\frac{\operatorname{Var}(j)}{\langle j\rangle}
\longrightarrow \frac{1-x_*}{2-x_*}.
\]

For N=1000 and h=0.01 the exact Fano factor is 0.47628865 versus asymptotic 0.47503119. At h=10^-10 it is 0.99994995 rather than the macroscopic 0.49999750, illustrating the finite-size crossover. These are predictions of the proposed chain, conditional on an observable that measures its occupancy. They are not an existing gravitational measurement or a selection of n.

## 2. Positive cubic from an explicit gapless spectrum

Use five anticommuting 4×4 Hermitian matrices and the two-dimensional Hamiltonian

\[
H=v k_x\Gamma_1+v k_y\Gamma_2+
\lambda\sum_{a=1}^3u_a\Gamma_{a+2},\qquad |vk|\le\Lambda.
\]

At zero chemical potential and zero temperature, the two negative-energy bands give the exact sea difference per sheet area

\[
\Delta F_f=-\frac{(\Lambda^2+\lambda^2u^2)^{3/2}
-\Lambda^3-\lambda^3|u|^3}{3\pi v^2}.
\]

After multiplying by sheet area per volume η and adding a tuned bare quadratic, the remainder begins

\[
W_{\rm rem}=\frac{\eta\lambda^3}{3\pi v^2}|u|^3
-\frac{\eta\lambda^4}{8\pi v^2\Lambda}u^4+O(u^6).
\]

This is a concrete positive-cubic mechanism, not a fit to the target. The microscopic source operator is λψ†Γ_(a+2)ψ. Coefficient matching would require ηλ³/(πv²)=1/(Ka0); neither this equality nor the quadratic tuning is predicted. The internal mass vector must still be physically identified with spatial polarization and coupled to gravity. A homogeneous three-dimensional medium would additionally need a reason for this two-dimensional density of states. Ordinary three-dimensional linear modes yield a fourth-order logarithm instead.

The candidate fails the full target already at quartic order: n>0 requires a positive quartic, while this determinant gives a negative one. It also lacks a finite capacity. The parent independently reconstructed the cubic integral and identified the quartic mismatch; both checks agree with the raw derivation. That review covers the spectral algebra, not the physical source bridge.

Finite temperature provides another discriminator. The exactly integrated derivative contains a difference of log cosh terms. At every fixed T>0, after subtracting its actual quadratic coefficient, the small-u remainder force is O(u³), not O(u²). The desired law is restricted to T≪λu≪Λ. In the normalized check with T=0.1, remainder-force/u² decreases from 0.00636307 at u=0.01 to 0.000636631 at u=0.001 and 0.0000636634 at u=0.0001, demonstrating the rounding rather than an asymptotic constant.

## 3. Capacity bridge investigated

Adding an orientational saturation free energy superficially supplies a logarithmic barrier. It does not close the model in a common equilibrium ensemble: that classical entropic barrier needs T>0, while the exact gapless cubic needs T=0. A two-reservoir construction would need a new dynamical derivation. Even a formal hybrid consisting of this cubic and even analytic terms misses the target fifth-order term. No target-shaped barrier is inserted and presented as a microscopic result.

The two mechanisms therefore remain distinct open routes. Combining their successful fragments is not justified by the present calculations. Positivity, one capacity scale, or an occupancy count still selects no integer n.

## 4. Evidence and scope

The raw Hamiltonian, exact rates, affinities, limiting order, units and derivations are in raw_derivation.md. No external theorem or material-specific experimental claim is needed for the results here: all new formulas are derived directly from the specified finite chain, elementary matrix spectrum and one-dimensional integrals. source_provenance.json identifies the frozen local inputs. No novelty or literature-exhaustiveness claim is made.

The portable script check_medium_round2.py executed **132 checks**, all passing. The v2 runner record run_001/manifest.json validates with status completed. Controls cover 25 (N,h) distributions, three independent generator nullspace solves, three small-source and three zero-source controls, all 25 Clifford anticommutators, three eigenspectra, five sea quadratures, three cubic-expansion controls and twelve thermal integrals. The stationary family uses N up to 1000; exact floating-point checks do not replace the displayed uniform derivations. The Fano formula is a large-N expansion and is not asserted as a finite-N identity.

Reproduction from the repository root:

```bash
python3 core_open_problems_round2_2026_10_20/02_medium/check_medium_round2.py /tmp/medium-round2-reproduction
```

Requirements: Python 3, NumPy, SciPy. The audited run used Python 3.9.6, NumPy 1.26.2 and SciPy 1.11.4. No network, external data or repository imports are needed. The contract is contract.json; exact hashes and observed runtime metadata are in the manifest. A new reproduction directory keeps the original evidence intact.

## 5. Review and next obligation

Primary verdict: **incomplete, with the smallest missing implication being a physical gravitational source map for either microscopic model.** The chain's log-intensity affinity and the Hamiltonian's internal mass bilinear are explicit; neither equals the required gravitational coupling by derivation. The Hamiltonian also fails the target quartic sign and capacity, and neither route selects n.

Self-review checked matrix degeneracy, radial measure, energy subtraction, units, source versus observable, zero-source uniqueness, the j² self term, limiting-order dependence and common-temperature consistency. Parent independent review checked the sea integral, cubic and quartic signs. These are algebraic checks, not a certificate that an actual gravitational medium exists. Proofread-math self-review covered this report and raw derivation; no unresolved notation issue or mathematical-token correction remains.

The next experiments and their success conditions are in continuation.md. They require a specified coupling/reservoir or actual constrained quantum spectrum before further matching; repeating saturation fits is not the next step.
