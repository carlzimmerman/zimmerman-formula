# Mechanism review, 22 October 2026

**The dynamical mechanism is still open. A concrete constraint-algebra counterexample is the strongest result of this pass.** A second result is a conditional response-scale calculation, not a galaxy/cluster explanation. Review provenance: self-review, not independent certification.

## Scope and checkpoint

Base commit: `05a3bfdb73fd9194954dbcdb90602d2c2f979b83`. Tracked worktree initially clean; many pre-existing untracked artifacts. This review read the current README, status board, canonical v4 draft, recent commit history, DSF-21 THEORY, A54/A68/A69 and selected A83 source, the round-2 relativity report, and the latest doors-push map and D6 criteria. It is a cross-branch synthesis with a focused calculation, **not a claim to have read or rerun every file**. The precise date of the prior credit interruption was not available.

The record's current hierarchy matters:

| Piece | Surviving achievement | Missing implication |
|---|---|---|
| Galaxy law | Recorded rotation-curve fits and static constitutive construction | A conservative formation mechanism selecting the state |
| Scale | a0 proportional to sqrt(rho_DE); adopted kappa=1/2 | Numerical coefficient is still fitted; thermal alternative is postulated |
| Cosmology/shear | Recorded theory-v2 matches its comparison criteria | Transfer to an actual conserved parent action |
| Pressure-supported systems | Residual family identified | A selector covering dwarfs and clusters without breaking rotators |
| DSF-21 action | Explicit action and useful restricted quadratic calculations | Nonlinear constraints, actual polarized low-frequency response, cold-sector bridge |
| Lean | Algebraic identities for specified definitions | Proof that those definitions describe the complete physical action |

These empirical summaries are inherited, not independently remeasured here. A54/A68's constraint assertion is audited below. No adopted document or preregistration was modified.

## R1: exact counterexample to eight first-class constraints

**Claim audited:** A54 §2 and A68 §2 assert that the displayed unitary-gauge action has 26 phase-space dimensions, eight first-class constraints, no second-class constraints and hence five modes.

**Verdict: refuted as written for the eight-first-class assertion.** This does not establish the final mode count or an instability. The claim that there are five linear modes on the special vacuum is a distinct claim.

Use their conventions K=4piG, c=1, canonical pairs (P_i,pi_P^i) and (h_ij,pi^ij). On a flat three-torus with unit transverse area, take x of period 2pi and

```
h_ij = delta_ij, P_i = 0, pi_P^i = (J,0,0), pi^ij = q delta^ij,
pi_N = pi_shift = 0,
q^2 = (2+3 beta)/(12K) [J^2/(2 eta) + Lambda/(2K)],
K, eta, beta, Lambda > 0; J != 0.
```

All four primaries and all four of the claimed secondaries vanish pointwise. The momentum constraints vanish because all fields and momenta are spatially constant. The lapse constraint reduces exactly to

```
H_perp = -12K q^2/(2+3 beta) + J^2/(2 eta) + Lambda/(2K) = 0.
```

W(0)=0 and its first derivative is zero. Gradient energies vanish. These data are within the action's domain u<a0. They need not survive additional constraints discovered by the Dirac algorithm: that is precisely the issue with asserting the algorithm has already terminated.

The clock term in the Lagrangian is sqrt(h) P^i partial_i N. Integrating by parts on the torus gives **+sqrt(h) D_i P^i in H_perp**, with the sign used in A54. Thus at these data

```
dH[N]/dP_i = -partial_i N,
dH[N]/dpi_P^i = N J_i/eta.
```

Consequently the P contribution to the bracket is

```
{H[N],H[M]} = integral (J^i/eta) (N partial_i M - M partial_i N).
```

All other contributions vanish here: the gravity curvature/kinetic bracket has constant momentum coefficients and integrates to zero by periodic integration by parts; potential/kinetic metric terms are ultralocal and antisymmetrize to zero; the clock's metric variation is zero at P=0; quadratic P gradient terms and W have zero first P variation. The magnetic F^2 term, omitted in A54's displayed Hamiltonian, also has zero first variation here and cannot cancel the witness.

Choose N=sin(x), M=cos(x). Then

```
{H[sin x],H[cos x]} = -2pi J/eta != 0.
```

Constraint smearings can have either sign; they are not physical lapse histories. If desired positive smearings 2+sin(x), 2+cos(x) give the same integrated result. Therefore the asserted set is not first class. This obstruction persists even at beta=0. It is independent of a0, both numerical footings, gamma, and the detailed nonlinear form of W provided W'(0)=0.

The crucial error is stronger than the already acknowledged beta deformation: A54 says the P-sector pieces bracket with each other into zero. The clock-charge/kinetic cross bracket above does not. A68 C4 tests dH_perp/dN=0; that implies nothing about {H_perp,H_perp}. A vanishing bracket with an invented pi_P constraint cannot certify the real constraint algebra.

### What the missing preservation equation does on this witness

For constant J, integrating against an arbitrary test function yields

```
dot H_perp = (2J/eta) partial_x N = 0.
```

Thus preservation restricts the spatial lapse along J on this family. It does not allow arbitrary local lapse gauge transformations. Constant positive lapse is permitted, so the witness alone does not prove inconsistency or a ghost. A proper continuation must derive the full preservation operator with metric and P terms and classify its kernel under stated boundary conditions. It must not guess a new DOF count by subtracting one constraint.

### Verification

Exact symbolic constraint residual and integral; independent canonical central-difference discretization of H[N] with {P_j,pi_l}=delta_jl/dx. At n=32,64,128,256, the discrete bracket is exactly -n sin(2pi/n) for J=eta=1 and converges to -2pi. Deleting the clock term sets the bracket to zero and causes the witness check to fail. No quantum or statistical assumption enters.

## R2: a finite response scale, conditional on the vacuum calculation

Take A68's supplied flat-vacuum dispersion (not re-derived from the full nonlinear constrained system here):

```
omega^2 = c^2 gamma k^4/[B + eta k^2],
B = K(2+3 beta)/beta, gamma = K L_*^2/2.
```

For eta>0, define D=c L_* sqrt[beta/(2(2+3beta))]. Then omega <= D k^2, so the inverse angular frequency obeys

```
t_response = 1/omega >= R^2/D, R=1/k.
```

This is an eta-independent lower bound within that dispersion, with equality approached as eta tends to zero at fixed beta, gamma. In the IR, reducing eta cannot arbitrarily speed up the mode. The coefficient beta is still free; smaller beta makes this mode slower. The calculation uses beta=0.02798, the record's upper-bound input, hence the fastest beta choice. L_*=24,30,90 pc are illustrative branch choices, not a universal allowed interval (the D8 erratum already rejects that reading).

| inverse wavenumber R | 1/omega at L*=24 pc | at L*=90 pc |
|---|---:|---:|
| 1 kpc | 0.00166 Gyr | 0.000442 Gyr |
| 10 kpc | 0.166 Gyr | 0.0442 Gyr |
| 30 kpc | 1.49 Gyr | 0.398 Gyr |
| 100 kpc | 16.6 Gyr | 4.42 Gyr |
| 1 Mpc | 1659 Gyr | 442 Gyr |

Numerics use eta=gamma. The radius where the IR inverse frequency is 10 Gyr is 77.65, 86.81, 150.36 kpc at L*=24,30,90 pc. At fixed L* and beta a0 cancels, so both footings give the same table. If an externally justified relation L*=sigma_c^2/a0 is imposed instead, L* changes between footings and these radii change as a0^(-1/2); that extra relation is not assumed here.

**Interpretation limit:** R is inverse wavenumber, not wavelength. This is an oscillation response time, not a relaxation time, signal front, halo edge or age measurement. Finite domains, forcing, initial conditions and dissipation matter. Hubble curvature changes the vacuum equation; the round-2 report already contains an H-dependent term. Polarized backgrounds alter the potential Hessian and constraint reduction. A69 already observes that this vacuum k^4 operator alone supplies the wrong static force profile. Hence the tempting statement 'galaxies settle but clusters do not' is an unverified hypothesis, not a result.

A useful next question is whether a **repaired** parent retains a similar radius/age scaling on actual nonlinear galaxy solutions. It would then supply a falsifiable history dependence instead of another fitted equilibrium coefficient. The constraint audit comes first.

## R3: why an inward fraction near one-half is not yet a mechanism

For any even radial velocity distribution f(v_r)=f(-v_r), the inward mass fraction is exactly one-half. The Gaussian check is an example, not the proof: change variable v_r -> -v_r in the negative-half integral. Total density and radial stress count both signs equally. Minimal gravitational coupling does not discard the outgoing half.

Therefore phase mixing can explain a population-count identity but cannot by itself select the law-sourcing population u. The missing step is an interaction/current equation that distinguishes the populations while conserving total stress-energy. This is not a no-go against every stream-dependent coupling. D6 already has an unexecuted inflow hypothesis; no claim is made to have completed its self-similar infall or observational tests.

## Literature and novelty

The literature-check skill and SciSpace semantic search were used on 22 October 2026. Search question: 'Can a conservative gravitational polarization medium with a preferred foliation and quartic low-frequency dispersion dynamically reproduce MOND in galaxies while leaving cold matter unrelaxed in clusters, and what Hamiltonian constraint consistency obstructions are known?'

SciSpace returned Blanchet–Le Tiec, Khoury and the user's own deposits. The user's deposits are not independent corroboration. Several indexed arXiv records carry ingestion dates in place of original publication years; primary arXiv records must control dating.

Primary records inspected:
- Bellorin–Restuccia, **On the consistency of the Horava Theory**, arXiv:1004.0055v3 (2012 revision), https://arxiv.org/abs/1004.0055v3. Its abstract explicitly identifies a second-class constraint in a pure-gravity lambda-R setting. Adjacent result only; no theorem imported for the present P-coupled theory.
- Arkani-Hamed, Cheng, Luty, Mukohyama, **Ghost Condensation and a Consistent Infrared Modification of Gravity**, hep-th/0312099v1 (2003), https://arxiv.org/abs/hep-th/0312099v1. The abstract explicitly states k^4 dispersion and time-dependent modification of gravity. A slow quartic mode is not itself novel.
- Blanchet, **Gravitational polarization and the phenomenology of MOND**, astro-ph/0605637v4 (2007 revision), https://arxiv.org/abs/astro-ph/0605637v4. Gravitational polarization as a MOND mechanism is prior art.

Authentication was at primary metadata/abstract level; no external theorem is needed for R1. This is a bounded discovery search, not a comprehensive novelty certification. The exact R1 witness was not located in the inspected local reports. No global novelty claim is made.

## Audit matrix and continuation

| Obligation | Status |
|---|---|
| Initial data satisfy all asserted eight constraints | Passed analytically and symbolically |
| Full bracket at those data vanishes | Failed: -2pi J/eta |
| Eight first-class constraints | Refuted for the displayed action |
| Full nonlinear mode count / well-posedness | Not addressed; requires preservation and boundary analysis |
| Vacuum response arithmetic | Verified in stated 15 cases; bound proved conditionally |
| Response law on a galaxy background | Open |
| A causal conserved cold-sector selector | Open |
| kappa=1/2 derived | Not achieved |
| Novel, observationally validated completion | Not achieved |

Next executable obligation: derive the full lapse-preservation operator from A33, retaining the clock-charge/kinetic bracket and the gravitational beta deformation; determine whether constraints/lapse fixation leave an admissible evolving branch. Then compute finite-wavelength perturbations of an actual polarized solution. A new action repair must be tested against the static law before any inherited shear pass is transferred to it. The old successful simulation cannot certify a changed parent.

The target remains open. R1 is a substantive checkpoint, not completion of the research objective.

## Reproduction and record limits

The validated manifest is `run2/manifest.json` (status `completed`); results are `run2/results.json`, log `run2/stdout.txt`: **27/27 checks pass**. `run/` preserves the initial 26/27 run and its too-strict approximation check. The post-result amendment explains the correction. The first manifest's script/contract hashes no longer match current files; it is historical evidence, not the current reproducible run.

Quick verification:

```
python3 sol61_push/mechanism_reassessment_2026_10_22/checks.py /tmp/mechanism_reassessment_results.json
python3 sol61_push/mechanism_reassessment_2026_10_22/checks.py /tmp/mechanism_reassessment_mutation.json --mutate
```

The second command is expected to exit 1: clock deletion removes the nonzero bracket and its continuum convergence target (25/27). The mutation outputs in this directory are a diagnostic outside the bounded runner, not a second validated manifest. The bounded runner records the exact successful command and input/output hashes. Numerical-library threads were limited to one; no heavyweight simulations or data downloads were run. The attempted nice priority change was refused by the environment; the small calculation still ran. No dependency installation, commits, pushes or manuscript changes were made.

Self-proofreading covered this report's definitions, signs, units, cross-references and claim scope. No inherited source was copyedited. Mathematical review remains self-review; independent review is still desirable before promoting the counterexample into the canonical record.

## Continuation checkpoint: lapse preservation derived

See `PRESERVATION_RESULT.md` for the subsequent calculation. The missing bracket has now been derived including the metric variation of D.P and checked in a nonconstant plane-dependent sector. Preservation requires a weighted-divergence equation. An exact rotating-current witness on a torus admits no positive periodic lapse despite satisfying the old constraint list. Conversely, the flat quadratic scalar model retains one positive-energy mode after a correct four-second-class-constraint reduction. A regular spherical no-flux branch has a derived radial momentum relation and is the next constructive route. These results supersede the earlier statement that preservation had not yet been calculated; they do not close the full nonlinear theory.

## Continuation checkpoint: radial lapse operator

`RADIAL_RESULT.md` now derives the next preservation step with both spherical metric variables retained before variation. At time symmetry the radial lapse equation has a nonzero highest-derivative coefficient for beta>0; its formal flat limit is a screened elliptic equation with a unique regular bounded lapse for prescribed asymptotic value. The six exact checks pass and the manifest validates. This does not establish positivity/invertibility on an actual galaxy background. The next load-bearing input is a self-consistent finite-stiffness polarized background with specified matter and boundary conditions, not another chosen field profile.

## Continuation checkpoint: polarized response changes the timescale argument

`NONLINEAR_WEAK_RESULT.md` retains the nonlinear potential in a formal leading weak-field energy. Its convexity and Hessian give a positive k² restoring term at nonzero polarization; oblique waves require transverse-mode mixing, included by a low-frequency Schur complement. The earlier vacuum response-radius arithmetic is unchanged, but its use as a galaxy/cluster separation mechanism is **not supported**. A fixed-source energy minimum is also not an attractor. Ten symbolic checks pass, with the full reduction's truncation error and actual galaxy background explicitly unverified. These limits should accompany any quotation of the earlier 78–150kpc vacuum radius.

## Continuation checkpoint: outgoing scalar radiation

`RADIATION_RESULT.md` identifies a gapless outgoing channel in the reduced mixed scalar, to which CFG760–762's different massive-wave exclusion does not directly apply. A planar interface conserves flux and transmits at every tested positive frequency, but its low-frequency transmission is suppressed as 4 sqrt(omega) in the stated normalization. A separate prescribed spherical mass-conserving source emits finite-size breathing radiation, with low-frequency power proportional to omega^(5/2) at fixed second-moment amplitude. Ten interface checks and six source checks pass; both current manifests validate. No self-consistent halo cooling rate, cold-sector selector, or observationally viable completion follows yet.

## Continuation checkpoint: spherical stationary backgrounds

`SPHERICAL_RESULT.md` solves the fixed-Plummer-source weak-field finite-stiffness radial vector equation for three stiffnesses, with tolerance and outer-boundary refinement. Five checks pass and the manifest validates. It identifies regular central q~r and finite polarization density, replacing the zero-stiffness central q~sqrt(r) cusp in this reduced setting. A source-dependent transition scaling is derived but not numerically fitted. These are now usable reduced-model backgrounds for a radial radiation calculation; they are not the missing exact metric/clock/cold solution.

## Continuation checkpoint: radial wave operator and long-range boundary

`RADIAL_WAVE_RESULT.md` derives the radial fourth-order operator and its positive spatial quadratic form in the same approximate model. The isolated background's 1/r stiffness produces an outgoing logarithmic phase and a frequency-dependent crossover radius. A naive free-vacuum boundary is therefore not uniformly valid for slow waves. Seven checks and the current manifest pass; a reversed-phase mutation fails. The slowest ray-time estimates fail their short-wavelength validity check and are not promoted to cooling predictions. The next global response calculation must retain the long-range exterior and both admissible fourth-order branches.

## Continuation checkpoint: global driven radial radiation

`FORCED_RADIAL_RESULT.md` solves the global forced radial problem on finite-stiffness Plummer backgrounds, retaining outgoing and decaying long-range branches. Six checks pass and the bounded manifest validates. Source work matches exterior power at approximately1e-6 relative; outer-radius refinement is below0.04%. For the same mass-conserving Gaussian drive, power relative to vacuum is0.0001749 at dimensionless frequency0.3 and1.974 at frequency1. These are source-response ratios, not transmission probabilities. Failed numerical probes and the origin-boundary repair are retained. No autonomous damping time is yet established. The concurrent unscreened Cassini/SPARC no-go in D7c remains a separate unresolved observational obligation.

## Continuation checkpoint: reciprocal backreaction and stability threshold

`BACKREACTION_RESULT.md` calculates static and outgoing susceptibilities for the same source/background. A diagnostic reciprocal mechanical coordinate damps at weak coupling only if its full restoring force remains viable; static energy requires k>lambda² chi0, with chi0 approximately0.00162990 in the chosen normalization. Eight checks and the current manifest pass; incoming-wave mutation reverses dissipation. The diagnostic coordinate is not a derived matter sector. A dimensional comparison also shows the two tested frequencies are too high to establish slow material relaxation; a low-frequency global response and an actual matter action remain necessary.

## Continuation checkpoint: slow radiation is too weak for the diagnostic weak-coupling route

`LOW_FREQUENCY_RESULT.md` extends the global response to0.003–0.03 and derives a formal omega^5 law from the long-range acoustic region. The coefficient computed from the static response predicts the numerical powers increasingly well toward lower frequency. Eight checks and the current bounded manifest pass; finite-domain and matching limitations are explicit. Combining this response with the diagnostic oscillator gives millions of periods or more for slow weak-coupling amplitude damping. The radiation channel is real in this reduced model but does not establish rapid material settling. A derived live matter/collective mode or a different lawful relaxation interaction is now the more important missing input.

## Continuation checkpoint: collisionless response has a speed mismatch

`KINETIC_RESULT.md` derives a local Maxwellian Vlasov/scalar determinant using minimal gravitational coupling. Seven checks pass and the manifest validates. Resonant field roots damp, while exceeding the enhanced Jeans threshold produces a growing mode. At the previously used beta0.02798, the x=1 field phase speed is about7223 times the quoted cold dispersion; effective resonance would require beta around5.15e-10, which is not derived. Relevant prior art was located through SciSpace and its primary abstract verified. This is a conditional kinetic route and diagnostic, not a new interaction or the missing cold/P sourcing mechanism.

## Continuation checkpoint: identified-medium inertia and pressure tradeoff

`MEDIUM_INERTIA_RESULT.md` reconciles CFG939's already-derived mass inertia with the preceding independent-field kinetic calculation. The theories have different degrees of freedom and different restoring forces; eta=1/rho cannot simply be imported into A33. In the identified branch, a local repulsive kinetic response can phase-mix efficiently, but the same velocity dispersion shifts equilibrium. The derived cold-profile relation A epsilon_warm=4/(kr)² identifies a possible short-scale compatible regime while leaving global energy transfer and the free-population selector open. Seven checks and the current manifest pass. No halo damping time is inferred from the invalid kr=1 local extrapolation.

## Continuation checkpoint: anisotropic warm equilibrium exists, but needs a boundary completion

`ANISOTROPIC_RESULT.md` constructs a positive stationary straight-trajectory distribution reproducing the full point-source gamma=0 identified-medium law density. Its anisotropic stress divergence vanishes despite nonzero dispersion, so the earlier isotropic pressure correction is not a universal obstruction. Ten checks and the current manifest pass; dropping tangential stress fails three checks. The exact family has infinite mass and a nonzero virial surface term, not a finite isolated halo. A finite confining transition, stability and formation remain unproved; the arbitrary speed distribution does not select a cold fraction or derive kappa.

## Continuation checkpoint: finite bound positive distributions, including stiffness

`FINITE_KINETIC_RESULT.md` constructs an anisotropic positive f(Q) family and solves its density and effective potential together. There are24/27 finite bound gamma0 cases and8/9 finite bound stiff cases, with all cap rejections retained. Each current manifest validates and its6 checks pass. The edge comes from a negative bound energy cutoff and an inward exterior force, not a reflecting wall. This advances the prior infinite family, but profiles generally lie below the cold law and retain chosen occupation/anisotropy parameters. No stability, formation, selector or observational success is established.

## Continuation checkpoint: conditional spherical stability

`ENERGY_CASIMIR_RESULT.md` derives an exact nonnegative conserved-functional gap for the finite linear-cutoff kinetic family in the identified-medium model. It bounds phase-space L2 distance, and density L2 for positive stiffness, during admissible invariant-preserving spherical evolution. Nine checks and the manifest pass; deleting the angular-momentum term fails anisotropic stationarity. This is conditional energy-distance stability, not a global well-posedness theorem, nonspherical stability or attraction. The distribution/parameter selection and force-law mismatch remain open. Related energy-Casimir prior art was found with SciSpace and authenticated at the publisher-abstract level.

## Continuation checkpoint: fixed-mass approach to the cold stiff branch

`COLD_LIMIT_RESULT.md` holds mass1 and stiffness0.01 fixed while increasing the kinetic occupation parameter. Four finite bound solutions move toward an independent cold free-boundary reference. At the highest tested occupation, total gravity differs by at most4.56% at four declared interior radii and0.392% at r=1; this is not a uniform or observational error bound. Six checks and the current manifest pass after tightening a failed mass-shooting probe. Collisionless transport does not automatically produce the increasingly concentrated distributions, and the stability bound is not uniform in the cold limit. Formation and parameter selection remain open.

## Continuation checkpoint: global phase-space feasibility and updated input audit

`PHASE_PACKING_RESULT.md` combines the classical occupation bound with the native finite-system virial identity, without isotropic or local-wave assumptions. Five checks and the manifest pass. The coldest tested density needs fmax>=40.33, versus1.224 in the warmest example; no collisionless rearrangement of that lower-ceiling closed population can produce the target stationary density, irrespective of anisotropy. No primordial fine-grained ceiling is known, so this is a necessary-input test, not a universal exclusion.

The newer E1 input audit reports D7c's old two-footing no-go becomes UNDECIDED under the native single footing and revises other empirical sensitivities. Earlier entries citing D7c as a standing no-go are superseded by that qualification. This synthesis inspected the new audit but has not independently rerun it; the analytical kinetic findings remain separate from those observational gates.

## Continuation checkpoint: first live conservative near-equilibrium evolution

`LIVE_RELAXATION_RESULT.md` evolves a5% canonical dilation of a finite equilibrium under a self-consistent radial particle-mesh Hamiltonian. Energy drift stays below4.02e-6 and the late bulk-radius response is smaller than the early response at two resolutions. Five analysis checks and its manifest pass. But controls drift and injected energy differs by42% across meshes, so no converged damping rate or asymptotic settling is claimed. An initial under-resolved central-cell cap failure is disclosed. The next numerical obligation is an equilibrium of the discrete energy itself, then matched-energy and longer-time tests. This is not primordial formation or a cold-fraction selector.

## Continuation checkpoint: discrete equilibrium and matched-energy response

`DISCRETE_EQUILIBRIUM_RESULT.md` solves the continuous stationary f(Q) in the exact interpolated particle-mesh mean field. Control drift improves by factors6–9, and injected dilation energy is matched across two resolutions. Six audit checks and the current manifest pass. The finite-time disturbance decreases at both resolutions, but late amplitudes remain resolution dependent; no damping rate or permanent settling is claimed. The tested warm A10 member is not the near-law cold branch.

The new D7d report states that the screened action passes its Cassini quadrupole gate at the record's stiffness lengths. This synthesis inspected its report, not independently reran the solver. It is a positive reported static-screening result, separate from the unresolved kinetic identification, full parent and formation/selector problems.

### Longer live response checkpoint

See LONG_RESPONSE_RESULT.md. Refined warm spherical runs extend to t=120 without a large revival, and the late radius response is mainly an offset (.01148) with smaller fluctuations (.00164 standard deviation). Coarse control hits the outer boundary at t=113.705; no extrapolation. Conservation is good but does not establish convergence. The bounded audit retains FAILED status because two strict perturbed-prefix comparisons fail (RMS-radius differences at most 2.47e-10, other observables up to 1.76e-7). The valid manifest records failures honestly. This advances finite-time redistribution evidence, not cold formation, a unique attractor, or a complete dynamical parent.

### Cold-branch dynamical checkpoint

COLD_DISCRETE_RESULT.md tests A10000 rather than extrapolating from warm A10. Four live runs finish t=40 and show substantial persistent radial oscillations: late/early window standard-deviation ratios .9365/.9393. Static spatial refinement approaches the continuum profile but remains imperfect (512-node acceleration deficit up to4.36% relative to continuum A10000 at sampled radii). The bounded v2 audit retains FAILED status for one force finite-difference threshold; a step-size diagnostic suggests cancellation without silently overriding it. Warm settling is not established for the near-law branch. A cold collective-mode analysis is now more informative than assuming universal phase mixing.

### Cold radial spectrum checkpoint

COLD_SPECTRUM_RESULT.md derives the zero-dispersion radial Sturm–Liouville problem and its positive conserved quadratic energy. Four grid resolutions give fundamental period7.59059, on the scale of finite-A live peaks7.1–8.3, without a fitted frequency. A dilation excites multiple modes; positivity supports oscillations, not dissipative settling. The bounded spectrum audit passes4 checks with valid provenance. Finite-A kinetic stability, damping, formation, novelty and the full parent are still open.

### Orbit-resonance checkpoint

ORBIT_RESONANCE_RESULT.md samples1024 continuum orbits per occupation parameter. A10000 median orbital frequency .22734 lies below cold collective .82776; third/fourth harmonic proximity remains common. No fundamental resonance exclusion or damping rate follows from the sample. A conditional scaling argument gives typical Omega_r proportional to A^(-1/5) for regular interior orbit families while cold collective frequencies remain finite, moving resonances to higher harmonics. This identifies a possible cold-settling obstacle; orbit-mode Fourier weights and full kinetic response are still needed.

### Orbit-coupling checkpoint

ORBIT_COUPLING_RESULT.md computes Fourier coupling to the finite-A dilation trial potential, avoiding an unjustified cold-eigenfunction boundary transplant. At A10000 only .0248% of the sampled n1–8 harmonic power lies in exploratory5% bands around the cold reference frequency. Third/fourth frequency matches exist but couple weakly to this trial. Five numerical gates pass with valid provenance, including a finite-dilation potential-derivative check. This is not a kinetic eigenmode, damping rate or formation mechanism.

### Kinetic derivative-weight checkpoint

KINETIC_WEIGHT_RESULT.md derives the prescribed-potential susceptibility with required1/Q weighting for f=FQ. The independent high-frequency spatial sum rule improves from6.87% to2.38% sampling discrepancy at1024/4096 orbits. A third-harmonic absorptive contribution remains visible across finite broadenings, so the earlier .0248% mass-weighted coupling statistic does not exclude kinetic absorption. No zero-width limit, self-consistent pole or decay rate has been established. Six bounded artifact-audit checks pass with valid provenance.

### Projected kinetic-feedback checkpoint

PROJECTED_FEEDBACK_RESULT.md includes feedback with S=<phi,K^-1phi>=.2513874. The finite sampled response is exactly equivalent to a positive rank-one update of orbital squared frequencies, preventing false damped-eigenvalue claims from finite rational samples. Its largest-weight frequency1.34–1.37 misses the .828 cold fundamental, so this single-shape approximation is not a mode/lifetime explanation. Five numerical checks pass. Multi-shape closure and continuum response remain open; passing the algebraic checks does not overcome the basis limitation.

### Multi-shape kinetic-feedback checkpoint

MULTISHAPE_RESULT.md expands the field space to1,2,4,8 shapes. Four/eight shapes recover a low response peak .810/.815 at1024/4096 orbits for both epsilon .03/.01, close to cold-fluid .827760 and live breathing. This resolves the large one-shape frequency mismatch at the level of a candidate finite-broadening response. Matrix sum-rule error improves7.00% to2.05%; no uniform error bound follows. Peak heights remain broadening-controlled, so damping and continuum convergence are unproved. Three bounded feedback-audit checks pass; the prior syntax-failed run is preserved. Formation, selection and complete parent remain open.

### Action-quadrature checkpoint

ACTION_QUADRATURE_RESULT.md replaces noisy1/Q phase-sample weighting with direct integration using dGamma=pi Tr d(L²)dE. The64x64 grid has mass error3.33ppm and matrix sum-rule error.00188%. The low peak is .823 on a.001 grid for32/64 orders,4/8 field shapes and epsilon.03/.01/.003, improving the candidate collective-mode frequency match. Peak heights remain broadening-controlled; no damping rate or formation mechanism follows. Three bounded response checks pass, with direct orbit constructions separately preserved.

### Linewidth-resolution checkpoint

LINEWIDTH_RESULT.md adds128x128 action quadrature and reduces broadening to1e-4. Frequency stays near.8228, but excess HWHM does not converge: at1e-4 it changes4.50e-5 to9.46e-5 between64/128 grids and becomes asymmetric. No damping rate or lifetime is inferred. Global sum-rule accuracy remains about.00187%, showing why it cannot certify narrow resonances. Two bounded operation checks pass; physical linewidth convergence remains unresolved. Direct resonant-curve integration is the next targeted remedy.

### Direct resonant-curve checkpoint

RESONANT_CURVES_RESULT.md computes the zero-broadening absorptive matrix along n Omega_r=.8228 with endpoint completion. An interpolation-only coefficient check failed and is preserved; direct orbit root/coefficient refinement repairs that approximation. Fixed-mode absorption .00618516/.00618524 agrees.00138% at64/128 grids; full matrices differ.134%. Third harmonic contributes98.52%. This establishes a numerically supported candidate kinetic transfer channel, not a free-mode damping rate or cold formation. Real principal-value response and basis/resonance-completeness checks remain. Three bounded checks pass with valid provenance.

### Principal-value and complex-mode checkpoint

PV_RESULT.md computes the pole-subtracted real matrix and combines it with the direct resonant absorptive matrix. Complex field phases reduce absorption relative to fixed real projections. A provisional real-axis decay indicator is stable across64/128 action grids but changes5.21e-4 to6.91e-5 between4/8 field shapes, so no physical lifetime is claimed. The candidate frequency remains near.8228. Three bounded checks pass; enlargement of the complex field space, continuation, formation and parent completion remain open.

### Sixteen-shape convergence checkpoint

BASIS16_RESULT.md extends the complex field space to8/12/16 nested shapes and reproduces the original eight-shape data exactly. The provisional decay indicator stabilizes near6.9e-5 within.33%, with frequency near.822797, across64/128 action grids. This is not a solved continued pole. The16-shape moment error is.676% at fixed16 harmonics, making harmonic refinement the next targeted uncertainty. Seven artifact-audit checks pass. Any inferred~1900-period decay time is strictly conditional, not a physical lifetime or formation result.

### Thirty-two-harmonic and frequency-dependence checkpoint

HARMONIC32_RESULT.md doubles orbital harmonics on the64 action grid. Full16-shape moment error improves.676% to.0000863%, while the selected fixed-B indicator changes only.00282%. Direct B(omega) at three frequencies yields a local Taylor-continuation estimate near .822797-i6.8e-5, stable across8/12/16 shapes and shifted about1.6% from fixed B. This is a conditional weak-damping approximation, not a directly solved continued pole or demonstrated formation rate. Conditional~1930 periods/e-fold indicates slow transfer, not rapid settling. Nine artifact-audit checks pass with valid provenance.

### Literature and continuation-route checkpoint

LITERATURE_CONTINUATION_RESULT.md authenticates primary versions of Fouvry–Prunet and Straub and limits the novelty claim: collisionless weak damping and radial oscillations are established neighboring phenomena. A project-specific variable change identifies the existing absorption matrix as pi times a resonance-frequency spectral density. This supplies a concrete route to causal analytic continuation, with sign and measure matched to the existing code. No continued pole was computed. Branch completeness, spectral regularity and representation convergence remain required; formation, occupation selection and parent completion remain open.

### Frequency-topology checkpoint

FREQUENCY_TOPOLOGY_RESULT.md finds substantial sampled energy-frequency minima on15/64 and30/128 angular-momentum rows. Two additional tiny reversal rows on the finer grid are not treated as physical folds. Interior PCHIP roots match direct brackets, but exact endpoints and unsampled regions remain unchecked. Fifth/sixth harmonics of the substantial minimum ranges straddle the candidate frequency, requiring branch splitting and turning-point integration before spectral continuation. Five bounded v2 checks pass with a valid manifest. This is a sampled topology diagnostic, not a new pole or damping result.

### Direct-fold and coordinate-swap checkpoint

DIRECT_FOLDS_RESULT.md directly locates fifth/sixth-harmonic energy minima resonant at.8228, across three orbit-quadrature orders. Their fixed-energy angular-momentum derivatives are nonzero and agree with derivatives along the minima within3.06e-6 relatively. Integrating the spectral density over angular-momentum roots therefore removes the energy-root Jacobian singularity locally. Six bounded v2 checks pass with valid provenance. This resolves a local numerical obstruction, not global spectral regularity, a continued pole or formation.

### Local fold-absorption checkpoint

FOLD_PATCH_RESULT.md implements the coordinate swap with actual dilation-trial Fourier coefficients on two fixed energy patches. Fifth/sixth patch absorptions are2.08867e-5 and4.03366e-8;32-to64 energy quadrature changes are below1.2e-7 relatively. Four bounded checks pass with valid provenance. These are local scalar integrals, not full harmonic contributions or self-consistent mode damping. Full curve coverage and the continued matrix calculation remain open.

### Formation-invariant checkpoint

ANGULAR_INVENTORY_RESULT.md returns to formation: closed spherical collisionless dynamics preserves every particle's angular momentum and hence its whole L² distribution. The A10/A10000 equilibrium mean L² ratio is13.269; three bounded moment checks pass with valid provenance. Canonical-dilation damping tests preserve this inventory and therefore cannot demonstrate warm-to-cold selection. This is additional to phase packing, conditional on the specified populations and closed central-force evolution. Initial cold inventory, nonspherical torques, interactions or boundary flux remain possible routes requiring explicit calculation.

### Selective-removal bound checkpoint

SELECTIVE_ESCAPE_RESULT.md optimally retains the lowest-L² particles to match the A10000 mean. Retained fractions are.12735,.27502,.57282 for A10,100,1000 respectively. Thus even ideal removal has a large mass cost and does not preserve the unit-mass target or overcome phase packing. Four bounded v2 checks pass with valid provenance; the original JSON-serialization failure is retained. This is a population-selection bound, not an escape simulation or full-distribution match.

### Cold assembly branch checkpoint

COLD_ASSEMBLY_RESULT.md constructs nine zero-dispersion unit-mass equilibria as prescribed baryonic strength varies.01–1, with positive refined radial spectra. All have L=0 and avoid the specific warm-inventory mismatch. The weak-field response is168 times slower, and the virial identity forbids a finite isolated equilibrium at exactly zero baryonic strength under these premises. Four bounded checks pass. This supplies a conditional branch for a live adiabatic-assembly test, not primordial formation or a completed mechanism.

### Live cold assembly checkpoint

COLD_LIVE_ASSEMBLY_RESULT.md evolves a prepared cold seed through a prescribed beta.1–1 baryonic ramp with a conservative shell Hamiltonian. T400 leaves about264 times less excitation than T100 at64/128 shells, with final position errors.16–.19% and accurate external-work accounting. Four bounded v3 checks pass with valid provenance. Failed initialization and fast-ramp domain-guard attempts are preserved; T20 remains unresolved. This is conditional live assembly without friction, not creation of cold occupation, reciprocal baryonic dynamics, global convergence or a complete formation mechanism.

### Assembly refinement and physical-time checkpoint

ASSEMBLY_REFINEMENT_RESULT.md isolates a64-shell time-step comparison (excitation change5.72e-8 relatively) and adds256 shells. Excitation remains about1.53e-5, but the innermost acceleration probe retains a2.85% continuum deficit, mainly static spatial error. Four checks pass with valid provenance. The established unit conversion maps T400 to25.42Gyr at final baryonic mass1e11 nominal solar masses on the canonical footing; this is a serious applicability limit, not a minimum-time theorem. Conditional numerical assembly is not yet a realistic formation mechanism.

### User-directed formation pivot

FORMATION_FOCUS_RESULT.md stops damping refinement. Existing ARGON fragmentation and charged-parent production both assume source preparation, so neither yet derives the cold seed. A new closed variational gas-cold model replaces prescribed baryonic growth with reciprocal contraction: early gas/cold infall agrees across step refinements, but explicit runs fail near the q barrier at about6.5. Failed manifests remain failed; this is numerical breakdown, not completed collapse. Next work is parent preparation and self-consistent stiff gas-cold evolution, with cosmological and thermodynamic inputs explicit.

### Vacuum-source and adaptive-collapse checkpoint

VACUUM_ORIGIN_AND_COLLAPSE_RESULT.md derives minimal-coupling vacuum mode equations from the existing carrier's quadratic action. A prescribed smooth expansion produces nonzero occupations without an occupied parent; four numerical checks pass. The expansion, curvature coupling, full abundance/coldness and carrier-to-medium map remain unproved. Adaptive reciprocal collapse reaches t13.71 with an inward half-mass region and outward outer shell, then fails at extreme q-barrier stiffness near time-step precision. No lasting bound object is certified; failed records are preserved and the final state is saved.


## Empty-state obstruction and event-based collapse checkpoint

EMPTY_STATE_OBSTRUCTION.md derives the unique classical vacuum by completing the square in X. The positive carrier action has no hidden nonzero homogeneous vacuum to supply the seed. Quantum gravitational production remains conditional on an unspecified cosmological state and curved-space completion. This is not a no-go for the distinct identified-medium theory.

REFLECTION_COLLAPSE_RESULT.md records six completed t=20 runs of an explicitly declared elastic hard-wall approximation to unresolved logarithmic turns. Both run manifests validate. Tight cutoff comparisons stabilize the outer ejection diagnostic; the interior remains tolerance- and resolution-sensitive. An analytic outer-shell comparison inequality supplies a sufficient escape criterion, satisfied with a large positive numerical margin. There is no certified permanent core or derived initial cold population. No damping work was resumed.


## Quantum spectrum and continuum localization checkpoint

PRODUCTION_SPECTRUM_RESULT.md records an integrated vacuum spectrum on a specified smooth inflation-to-radiation background, H_inf=m, xi=0. physical_spectrum_wkb2_v2_run completed and validates. For the existing MeV benchmark and thermalized radiation assumption, the asymptotic effective daughter yield is about 4.30e-36, roughly 1e-29 of the standard dark-matter target. Both charges are included. The free higher-inflation-scale source estimate enters the nonlinear/tachyonic regime of the existing cubic coupling; it is not a dilute-decay abundance prediction. production_scalings_run records the conversion and threshold diagnostics.

CORE_ENERGY_BOUND.md proves persistent localization in the specified closed model. The exact initial continuum energy has a positive convergent series with a geometric remainder bound. core_energy_exact_run verifies rational bounds: M(r<20)>0.03516 at every admissible time, and retained mass >0.06378 if an asymptotic decomposition exists. No fixed central numerical node is used in these continuum statements. Global existence, initial cold production and a settled profile remain unproved.

CORE_CONVERGENCE_RESULT.md records completed 32/64/128-shell t=30 runs with small energy drift but unconverged inner profiles. At this checkpoint the additional 256-shell and equivalent minimum-gap event-search runs are still executing; inspect their manifests before interpreting them. No damping work resumed.


### Source-state and solver continuation

STOCHASTIC_SOURCE_RESULT.md records a completed 4096-patch stochastic inflation calculation beginning at zero coarse field. It generates both X and Phi amplitudes using the existing potential and declared de Sitter noise approximation; it does not supply post-inflation momenta, charge or cold yield. NONLINEAR_SOURCE_GATE.md bounds the first fixed-source potential release and connects its residual coefficient to the already known chemical-cap/scattering-zero combination. Neither is advertised as a completed formation mechanism.

The compiled-force audit passes, and compiled 256-shell collapse now reaches t=30. Independent cutoff and time-tolerance variations satisfy the frozen 5% criterion for the two late-window enclosed-mass averages. A 512-shell attempt was externally killed; t_eval-only storage replaces retention of every internal-step interpolant, with an exact agreement test through the first N32 barrier event. The 512-shell streaming rerun remains in progress at this checkpoint. assess_core.py and its contract specify the final comparison before that result is read.


### Final finite-time formation checkpoint

The 512-shell streaming run completed through t=30; no numerical jobs remain running. assess_core_run completed and validates: late-window averaged M(r<3), M(r<5) change by 1.99%/0.292% under 256->512 refinement, 1.43%/0.457% under cutoff variation, and 4.00%/2.27% under time-tolerance variation. All satisfy the predeclared 5% per-comparison criterion. This establishes coarse finite-time numerical stability in the approximate barrier model, not a steady halo or the asymptotic bound fraction. CORE_CONVERGENCE_RESULT.md is the current report; CORE_ENERGY_BOUND.md supplies the independent exact continuum localization bound.

The quantum spectrum still underproduces the standard MeV target by roughly29 orders for H_inf=m. The higher-H stochastic ensemble generates both fields, and its full instantaneous potential Hessian is positive in all4096 sampled states despite the empty-Phi instability. Prior CFG362 stochastic misalignment and the conditional isocurvature gate are now explicitly linked in STOCHASTIC_SOURCE_RESULT.md. Nonlinear conversion, spatial perturbations/free streaming, and the scalar-carrier-to-identified-medium mapping remain open. No claim of a complete formation mechanism or novel breakthrough is made.


### Quantum conversion and neutral-stock survival continuation

QUANTUM_CONVERSION_RESULT.md adds the radial Phi quartic Floquet instability and the full-tree neutral 4-to-2 threshold amplitudes. The transverse growth exponent peaks at 0.1469914; conditional radiation matching puts twenty asymptotic growth e-folds well before X oscillation. phi_fragmentation_run has valid provenance but failed its overly strong all-patch H/M>1e6 assertion (actual minimum 3.77e5); its five numerical Floquet checks passed. No nonlinear fragmentation yield is claimed.

neutral_four_to_two_v2_run and audit_neutral_amplitude_run completed and validate. Recursive tree amplitudes agree with independent exact rational closed forms. The balanced-channel amplitude is a negative sum of squares and cannot cancel for the existing positive lambda_rep. The conditional forward loss coefficient is 1.0181e14 GeV^-8; inserting the target density gives a few-MeV survival-rate diagnostic, not a predicted source temperature or final abundance. Earlier serialization failure is preserved.

No cold population has been assumed or fed to the identified-medium solver: nonlinear source conversion, quantum spatial/momentum matching, isocurvature and the action-level carrier/medium bridge are still open. All new numerical jobs are terminal; no damping calculation was resumed.


### Coupled nonlinear early-field evolution

NONLINEAR_FRAGMENTATION_RESULT.md records five completed three-dimensional classical-statistical evolutions with all original potential terms retained. A fresh vacuum-built coarse stochastic source and finite-band de Sitter coordinate/momentum covariance are used, with their matching/IR/UV limitations explicit. No cold seed is supplied.

The original 32/64-cubed batch failed its all-case UV test; the coarse spectrum is not certified. The 96-cubed refinement completes with energy/work residual 2.85e-6, charge drift 3.06e-13, and UV gradient fraction 2.47e-5. Coarse observables agree with 64 cubed: late inhomogeneous Phi variance fraction .421916, pressure/energy .339848, quartic potential energy fraction .271034. Independent elliptic-solution, Hamiltonian-gradient and covariance controls pass.

The result is early nonlinear spatial structure with an order-one coherent component and virtually unchanged overdamped X, not a final particle distribution. H/M remains 2.67e7. Classical vertices do not replace complete late quantum number-changing collisions. The vacuum nonrelativistic C n^4 sink is inapplicable to this state and is not appended. The handoff assessment explicitly leaves cold_relic_yield and cold_mass_for_collapse null. Requested final cold survival remains unresolved; no numerical jobs remain running.


### Late conversion final pass

LATE_CONVERSION_RESULT.md derives a distribution-independent conditional screening bound, including Phi mass work: the no-transfer Phi conformal energy implies a Hessian Rayleigh upper bound 4m^2+S/a^2-2g|X|. For the saved high-H source and a free radial X continuation, it becomes negative near a=6.573e10, H=3.112e-12 GeV (visible T approximately1.49 TeV under the imposed thermal history). At twice that a, the negative-curvature scale is about46m. This is an instantaneous stability obstruction to the passive continuation, not a conversion efficiency or final relic yield.

The separate Hinf=m vacuum source has a completed leading late-decay/recoil calculation with inverse quantum formation: affected weighted fraction1.306e-7, leading Y=4.29965e-36, abundancefraction9.839e-30, rms speed3.76e-16c at visible0.8eV. Late number-loss and dilute-phase diagnostics are tiny, but the full early resonant collision network remains unintegrated; this is not an all-channel certified survival bound. The two source branches are not combined.

Current runs dilute_quantum_survival_v2_run, screening_exit_bound_v2_run and audit_late_kinetics_run completed. The original dilute serialization failure and earlier stronger screening-cap calculation are preserved. High-H nonlinear quantum survival remains open; no cold seed was assumed, no collapse mass supplied, and no jobs remain running.


## 2026-10-23: direct late-window test and pair-conversion gate

See `LATE_NONLINEAR_TRANSFER_RESULT.md`. A conditional 96^3 four-X-cycle
local evolution using the original couplings resolves the UV diagnostic and
finds final X energy loss 9.523e-5, with a cycle-average loss 3.447e-5.
Most positive Phi energy gain is offset by interaction energy; excitation
is not equivalent to reservoir depletion. The initial late warm Phi waves
are prescribed energy-constrained test data, not derived from the earlier
quantum history. A free-mode proxy gives 13.8% of Phi quadratic energy at
f<1; the classical run is not a controlled quantum survival calculation.

The same action's X+anti-X -> Phi+anti-Phi channel has vacuum threshold
sigma*v=4.75243e-8 GeV^-2. On a hypothetical surviving free high-H reservoir
at A=0.001 GeV, Gamma_ann/H=12180.3. In a quasiparticle regime it can remain
open for M/2<mPhi,eff<M when single-X decay is blocked. This identifies a
second conversion route, not a new interaction or verified final yield.
Forward-only yields and collisionless cooling are explicitly conditional;
inverse reactions, coherent effects and earlier hot number-changing losses
remain uncomputed. No seed or scalar-to-medium bridge has been assumed.

Coarse runs fail UV checks and are preserved. The final 96^3 run and
independent corrected summation audit have dedicated provenance records.
No cold population has been fed into collapse.

Final verification: all seven new manifests validate; current 96^3,
homogeneous-control, pair-channel and corrected independent-audit runs are
completed. Coarse failures remain recorded. All jobs from this turn finished.

## 2026-10-23: evolving-bath recycling and conditional cold yield

See `EVOLVING_BATH_RECYCLING_RESULT.md`. The new kinetic calculation includes
rapid X <-> Phi Phi chemical equilibrium, pair conversion and its inverse,
finite-temperature direct quartic 4-to-2 and inverse 2-to-4, with conserved
energy and reaction heating. Real X formation plus pair conversion produces
a sustained effective 4-to-2 recycling cycle; it cannot be represented by
the previous constant zero-velocity loss coefficient alone.

For the explicitly conditional thermal matching of the hypothetical free
high-H reservoir at |X|=0.001 GeV, Yfinal=7.40907e-8 (16.95% of target),
60.80% of the kinetic-start weighted number. About 78.57% of the integrated
post-start loss is through pair recycling. A collisionless late continuation
gives rms v~1.03e-7 c at visible T=0.8 eV. These are not unique source-derived
predictions: matching the same free-envelope continuation at other amplitudes
in the tested set gives 5.96%-27.85% of target. These alternative histories
are sensitivity tests, not a physical allowed range or uncertainty interval.

No independently normalized cold Phi seed is added. The unproven input is
instead thermalization of a surviving quantum-produced reservoir at the
chosen epoch. The model uses an MB closure and a partial kinetic network;
full Bose collision terms, nonresonant cubic-containing/RIS-complete higher
reactions, coherent-to-particle matching and realistic gstar are still open.
Do not report this conditional relic as the high-H final abundance or feed
it into the separate collapse model.

Finite-temperature rate checks, tolerance refinement, independent integrated
energy/entropy, exact Bose detailed-balance identities and finite-decay
approach to the fast constraint pass. All ten new manifests validate; eight
current evidence runs completed. Two initial assessment/audit failures are
preserved and corrected in version-2 evidence. All jobs from this turn ended.


## Bath-formation continuation: omitted 3-to-2 absorption

See [BATH_FORMATION_REACTION_RESULT.md](BATH_FORMATION_REACTION_RESULT.md). The full vacuum tree channel X+Phi+antiPhi <-> Phi+Phi and its conjugate are nonzero and free of physical real-intermediate-state poles in this channel. The zero-velocity W-loss coefficient is 1767.5782 GeV^-5. It adds 41.93% to the starting chemical-relaxation prefactor of the previous conditional thermal calculation; insertion along the unchanged old trajectory corresponds to a missing loss of 20.75% of its final yield, not a corrected yield. Two new bounded runs completed with amplitude, conservation, detailed-balance, sampling, stoichiometry and phase-transfer checks. No bath matching time or cold seed was selected. A seed-free surviving abundance remains unresolved because the quantum correlators have not been evolved continuously from production through bath formation; other RIS-subtracted crossed channels are also missing.


## Quantum correlation continuation

See [QUANTUM_CORRELATION_CONTINUATION.md](QUANTUM_CORRELATION_CONTINUATION.md). Added and executed a quantum initial-covariance audit, nonzero-mode Hankel covariance completion, actual early linear quantum correlation propagation, and exact selected Wick-diagram inventory. The linear source reaches a declared 10% backreaction diagnostic at sampled z=3 (a=8.506), consistently across tested steps and grids; this is not thermalization. Nonlinear quantum scattering, absorption/inverse integration and the surviving cold abundance remain uncomputed. No bath time or cold seed was assumed, and no new conditional relic yield was produced.


## Nonlinear quantum Hamiltonian implementation

See [NONLINEAR_QUANTUM_SOLVER_RESULT.md](NONLINEAR_QUANTUM_SOLVER_RESULT.md). Implemented a finite-mode original-action quantum Hamiltonian and unitary, non-Gaussian evolution. Its virtual-state sums reproduce both absorption amplitude components (g lambda and g cubed), leading pair conversion, and both contact 4-to-2 channels to numerical precision; inverse evolution follows from the same Hamiltonian. Two-time connected quantum correlations and time/cutoff checks were run. The high-H source does not fit the benchmark occupation space, and the momentum continuum is not converged. Bath formation and surviving cold abundance remain uncomputed; no cold seed, bath epoch or replacement cosmological source was assumed. Failed initial audits are retained and explained in the report.


## Source-adapted basis and momentum continuation

See [MOVING_SOURCE_BASIS_RESULT.md](MOVING_SOURCE_BASIS_RESULT.md). The supplied source Gaussian covariance and large mean displacements admit an exact canonical basis change, removing the initial small-occupation constraint. Implemented an exact non-Gaussian potential-only substep and audited its reference-occupation identity. Cartesian fixed-band momentum sums were not converged (11–12% last changes); independent radial and direct triangle integration agree on the cubic kernel to 1.18e-6 relative. These are initial residual kernels and one operator substep, not thermalization or cold-particle production. Kinetic propagation of the resulting non-Gaussian state, full UV/IR treatment, late reaction evolution and surviving abundance remain unresolved.

### 2026-10-23 — Persistent wavefunction and high-H kinetic-overlap test

See `PERSISTENT_STATE_AND_OVERLAP_RESULT.md`. Added a full non-Gaussian, four-coordinate single-cell quantum propagator carrying the complex state through kinetic and interaction steps, with both original interactions and no separate rates. Tested time/grid refinement, inverse propagation, analytic free evolution, energy, and independent charge conservation. This is a reduced quench benchmark, **not propagation of the high-H quantum source** and not physical momentum convergence.

Separately continued the actual saved high-H classical realization from z=200 to 220 with absolute-time restart. Across dt=.01/.005 and 96/128 spatial grids, about 77.44–77.48% of the nonzero-mode Hartree energy proxy lies in shells with lambda*f>=1, and the mean homogeneous energy-proxy fraction is about 49.2%. Common-band spectrum changes are 2.16e-6 (time) and 5.58e-4 (restart-window spatial refinement). These diagnostics do not establish a weak-collision bath handoff; they do not prove that all resummed kinetic descriptions fail. Classical statistics still omit quantum Moyal terms. The 128 run starts from an interpolated 96 state.

Completed, validated records: `quantum_wavefunction_run`, `persistent_state_charge_run`, `kinetic_overlap_run`. No assumed cold seed or arbitrary thermal matching was added. **Bath formation and surviving cold abundance remain uncomputed.** Single-cell numerical success is not a new formation mechanism.
