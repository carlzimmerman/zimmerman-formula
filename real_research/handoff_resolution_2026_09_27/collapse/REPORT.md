# HR01 collapse, equilibrium and the edge

Base checkpoint: `48905ae11213afcb9ff1b7726530bb5dd1933fe3`, working-tree input hashes in `source_inventory.json` and per-run `reads.json`. Only this directory is written. No source lane, registration or Git state was changed. This is a self-review, not an independent-agent proof certificate. Both acceleration footings are used: 9.3603e-11 and 1.1312e-10 m/s²; kappa=1/2 is fitted, Z=5.7888.

**Original target not reached.** None of CFG2, CFG3 or CFG5 derives a covariant, well-posed, sole-fit-kappa model with the CFG4 edge and all its gates. The strongest surviving construction is a family of finite positive-density P2 halos with the enclosed mass retained outside and a boundary-normalized hydrostatic pressure. Its edge is boundary/formation data. Selecting the required distribution of edge radii, the top-level host prescription, and the galaxy/cluster transition remain obligations.

Primary proof-audit verdict for the proposed implication “shell crossing/splashback supplies the CFG4 edge in [0.31,0.48] without additional input”: **incomplete, with the smallest missing implication being the selection of the collapse history and its boundary radius by the proposed dynamics.** The unrestricted claim that shell crossing alone fixes that interval is refuted by independent orbital histories below. That refutation does not assert failure of a specified cosmological growing-mode ensemble, which has not been derived or simulated here.

## 1. Dependency graph and run contract

The actual graph is: stress/occupation postulate -> interior acceleration or dark stress rule -> stable time-dependent action -> system membership and collapse history -> density edge -> exterior conserved mass and cold-budget accounting -> common observational likelihoods. Algebraic verification of the first arrow does not establish the later arrows. The scripts score different subsets and sometimes different statistics: CFG2 uses a weighted 175-galaxy SPARC statistic with globally fitted mass-to-light ratio; CFG5 uses an unweighted filtered 155-galaxy statistic at fixed mass-to-light ratio. Their RMS numbers cannot be ranked against a single 0.110 threshold without harmonizing the statistic.

`run_suite.py` preserves repository layout in a scratch mirror. All CFG2/3/5 Python sources are copied unchanged, other repository entries are symlinks; source outputs for those lanes are not linked into the mirror. `record_child.py` refuses writes outside this lane and records hashes at first read and after execution for repository files actually opened by Python. Each job has a 900 s wall bound; jobs are sequential. Conventional numerical-library thread caps are cooperative and source harnesses can raise them to two. Process exit status and scientific checks are recorded separately. Inputs opened natively by external libraries are not fully captured by this Python hook, and symlinked input repositories are not a full immutable filesystem snapshot. Before/after hash equality is checked at closeout.

The handoff inventory was stale for CFG5: all three existing CFG5 main outputs were already present at the base, with scientific failures. CFG2_B main and every CFG3 output were missing. No nonexistent CFG2_C/D or CFG5_4/5/6 implementation can be represented as a completed run.

## 2. What CFG2 establishes and what it assumes

With point baryons M_b, the **postulated** pressure law P=a0 M_b/(8 pi r²), weak-field hydrostatics P'=-rho_d G(M_b+M_d)/r² and M_d'=4 pi r² rho_d imply

    (M_b+M_d) dM_d/dr = a0 M_b r/G,
    (M_b+M_d)² = M_b² + a0 M_b r²/G,

when the central dark point mass is zero. This conditional theorem is correct. Its uniqueness includes that central boundary condition. The geometric-mean stress law is not derived from the core dimensional a0 relation; changing it changes the kernel. For extended baryons, the algebraic field-stress reading E is a further declared rule, not the same hydrostatic theorem.

A decisive domain restriction applies to reading F. If M_b(r) is proportional to r^n, then P' is proportional to n-2. For n>2 the requested pressure rises outwards while -rho_d g cannot be positive for nonnegative dark density. `CFG2_common.law_F` uses max(-g_b',0) and the common integrator clips negative dark-density growth. The displayed F solution in this region solves a clipped rule, not the original pressure law. The deep ratio M_F²/M_E²=(2-n)/(n+2) only supplies a nonnegative dark-dominated branch for 0<=n<2; n=2 is a degenerate limit, and n>2 cannot be continued as that physical fluid.

The completed CFG2_B main verifies the phenomenological E fit at weighted RMS 0.1083/0.1035 dex, versus F 0.1445/0.1389. The global stellar mass-to-light normalization is profiled. The proposed settled-capacity scope rule gives 0.1740/0.1734 dex at Upsilon=0.42/0.45, against its own <=0.120 criterion. The source labels this failure “reported,” so rc=0 does not establish the proposed construction including its scope. Replacing that scope is an outstanding design task, not a successful parameter elimination.

## 3. A constructive finite density edge

Let r_M²=G M_b/a0 and choose any r_e>0. On 0<r<r_e define

    M_t(r)=M_b sqrt(1+r²/r_M²),
    rho_d(r)=a0 M_b/(4 pi G r M_t(r)),
    P_e(r)=a0 M_b/(8 pi) [1/r² - 1/r_e²] + P_ext.

The density is positive. Direct differentiation gives

    P_e'=-a0 M_b/(4 pi r³)=-rho_d G M_t/r².

At r_e, P_e=P_ext. Outside, set rho_d=0 and retain M_d(r_e); the exterior acceleration is G[M_b+M_d(r_e)]/r². Thus the pressure-matching and Gauss-law requirements can be satisfied simultaneously. For vacuum P_ext=0, the interior pressure is positive and decreases to zero. This is a static spherical weak-field fluid solution away from the singular baryon point; it is not a proof of an admissible collisionless distribution function, a regular center, dynamical stability, a causal equation of state, or a covariant action.

The original unshifted CFG2 pressure has P(r_e)>0 and cannot be abruptly matched to vacuum without exterior pressure or an additional surface stress. The pressure offset above changes its absolute constitutive law, though it preserves the derivative, density and interior force. It introduces r_e as boundary data. Hydrostatics therefore supplies a viable matching construction but no selection of x_e.

For point baryons P_original/P_cap=y=g_b/a0, and P_e/P_cap=y-y_e when P_ext=0. The CFG2 equilibrium is consequently not subject to CFG5's universal final-state stress cap wherever y>1+y_e. A pressure ceiling alone allows rho_d=P_d=0 in a baryonic well, whereas the RAR requires g/g_b=sqrt(2) at y=1. It cannot imply the RAR without additional equalities and formation selection.

`edge_audit.py` independently checks the analytic hydrostatic residual against pressure quadrature on both footings, five chosen edge fractions, and retained exterior mass. Main: 10/10 checks. MUTATE changes the exterior to the baryonic mass only and fails exactly `density_edge_Gauss_retention`, while the interior checks continue to pass. Version-2 runner manifests are in `edge_main/` and `edge_mutation/`; both validate, including the intentionally unsuccessful mutation record.

### Boundary-selection discriminator

Matching the original absolute pressure P_original=a0 M_b/(8 pi r²) to the positive vacuum stress scale P_ext=P_cap=a0²/(8 pi G) gives **g_b(r_e)=a0 and r_e=r_M**. For M_b=10^10 solar masses, r_M is 3.859/3.511 kpc on the two footings. In contrast, x_e=.31–.48 with the illustrative r_ta=500 kpc requires 155–240 kpc. It needs P_ext/P_cap=(r_M/r_e)², approximately 2.1e-4–6.2e-4 for that mass. The value depends on mass and formation boundary. With P_ext=0 and the original fixed pressure zero, P_original(r)>0 at every finite r, so no finite pressure-matched edge exists.

The positive vacuum stress scale used in that test is not the negative equation-of-state pressure of a cosmological constant. Treating it as exterior confining pressure is itself a hypothesis. The more general pressure offset provides an equilibrium matching family but does not derive its selected edge. A constant offset leaves Newtonian hydrostatic gradients unchanged; in a covariant theory an absolute matter-Lagrangian shift contributes to vacuum stress. It cannot be treated as a free pressure gauge without auditing the actual action and matching conditions. No such action fixing the offset is supplied by these lanes.

`boundary_selection.py` verifies this discriminator for 10^9, 10^10 and 10^11 solar masses on both footings. Its MUTATE substitutes 0.4 r_ta as the supposed vacuum-pressure-selected edge and fails the named pressure-matching check. The surviving design requirement is concrete: derive an environment/formation pressure or a boundary action that sets the required small pressure and edge jointly, while retaining exterior mass.

## 4. What shell crossing does and does not choose

An operational splashback definition requires a particle/shell trajectory and its first apocentre after its first pericentre; a current-turnaround surface concerns a different, later shell. Their ratio compares two epochs and two orbits. It cannot be calculated from a0 and kappa alone without the accretion and angular-momentum history.

A simple explicit history family makes the missing input visible. In a fixed spherical Kepler potential GM=1, take a tracer whose first turnaround radius is x and tangential velocity is ell/sqrt(x), with ell=0.2. Its semimajor axis is a=x/(2-ell²). Its radial period is 2 pi a^(3/2), and its first post-pericentre apocentre returns to x. Choose its earlier turnaround time to be minus that period, and choose a separate outer shell's first turnaround at time zero and radius 1. Then the current ratio is any chosen x; examples x=0.2, 0.4, 0.7 have identical gravitational laws and no a0-dependent force modification. Nearby tracers can be given a narrow spread of orbital energies and phases; the old stream and a subsequent infalling stream can intersect. This is a tracer-history counterexample to inference from shell crossing alone, **not** a self-consistent primordial growing-mode halo or a prediction for its density caustic. Imposing a common growing-mode history is precisely additional physical input that has to be supplied.

For a bounded sensitivity experiment, `edge_audit.py` evolves a tracer in the prescribed accreting spherical potential M(t)=M(1)t^p with

    r'' = -(pi²/8)t^p/r² + (pi²/8)ell²/r³,
    r(1)=1, r'(1)=0,
    r_ta(t)=t^((p+2)/3).

The last equation is a scale prescription (r_ta³ proportional M t²), not an output of a cosmological outer-shell solve. Thus this is explicitly a surrogate, not the full requested collapse calculation. The first new apocentre is measured by event integration. Static-potential controls conserve orbital energy and return to r=1; tightening the ODE tolerance verifies the reported ratio.

| mass-growth exponent p | x at ell=.1 | x at ell=.2 | x at ell=.4 |
|---|---:|---:|---:|
| 0 | .479144 | .474286 | .454236 |
| .5 | .338138 | .334405 | .319354 |
| 1 | .267897 | .265160 | .254295 |
| 2 | .195569 | .194045 | .188099 |
| 3 | .157578 | .156665 | .153128 |

The CFG4 interval occurs for part of the family, and fails in other admissible prescribed-growth cases. It is not a universal constant of an apocentre. The frequently quoted self-similar number 0.36 is not derived by these scripts and is not used as an external theorem here. A successful next calculation must predict the host population's history-dependent x distribution and propagate it into KiDS and the turned-around cold budget on both footings; replacing the distribution by a selected value 0.4 is an effective fit.

“Crossed in all three directions,” first radial shell crossing, and first post-pericentre apocentre are also different definitions. A one-dimensional spherical engine cannot by itself verify a three-direction crossing membership rule or identify nested top-level systems.

## 5. CFG3's different boundary and hidden assumptions

CFG3_principle explicitly sets the response to zero outside a gate. Gauss's theorem then requires a negative boundary contribution that cancels the interior phantom mass. This is a response edge. CFG4 requires an uncompensated finite density edge with retained enclosed mass. Changing the edge to splashback does not repair that mismatch: the differential operator and boundary conditions must change.

The occupation-factor algebra produces the RAR kernel once Bose enhancement, the selected free-fall mode, its time-ratio argument, and its coupling to the force are postulated. Dimensional a0 uniqueness does not supply those assumptions. The source itself leaves the baryons-only dark-field action open. Varying a field equation at fixed gate/frame does not establish an action for a dynamical gate and state-dependent free-fall region.

The heat-kernel uniqueness claim also needs restriction. Composition, isotropy and finite variance alone allow an isotropic compound-Poisson semigroup with characteristic function exp[t lambda(exp(-sigma²k²/2)-1)]. It composes, is positive and has finite variance, but is not Gaussian. A local continuous diffusion generator or appropriate scaling limit is additional input. Demonstrating that Gaussians compose does not prove uniqueness.

Tying the filter length to a field mass transfers the freedom to that mass; it does not derive the mass. The cold abundance, stellar/halo mapping and nonlinear population prescriptions remain inputs. A linear gate test gives the GR first-order limit at fixed background; it does not by itself bound a population of nonlinear regions.

## 6. CFG5 model and audit obligations

The identity 8 pi G P=g² is an isothermal singular self-similar equilibrium identity, not a general identity of collapsing or baryon-dominated systems. Its transfer to a cosmological dark-stress cap is a postulate. Constant P_cap does not imply a constant BTFR normalization after a history-dependent halo population and baryon contraction.

The engine uses prescribed abundance matching and concentration/accretion relations, a uniform tangential-velocity coefficient in [0.15,0.35], a cooling radius fraction .02, a doubled stellar mass for the galaxy's gas prescription, a 600 km/s kick (575/650 brackets), 64 stochastic daughter directions, 24 radial neighbours, 0.2 kpc softening, a time-step coefficient .03, and a first-apocentre coherence cutoff. These are physical modeling choices, empirical inputs and numerical parameters; they are not consequences of kappa. Seed and finite-resolution choices must be separated from physical universality claims.

The engine's finite radial-neighbour velocity variance includes smooth single-stream velocity gradients. CFG5_1's plane test recognizes and refines away this term, but the engine uses a fixed 24-neighbour estimator without subtracting it. Increasing shell count changes the smoothing scale and which particles convert. Consequently the existing failure between 600 and 1000 shells (converted fraction .0457 vs .0904) must be resolved before treating its conversion budget or interpolated realized cap as a prediction. Checking both fixed neighbour count and fixed smoothing fraction is the discriminating next numerical control.

The daughter treatment replaces a distribution of bound energies/directions by one mean radial speed and one tangential moment, and removes positive instantaneous-energy daughters. It is a reduced shell surrogate, not a self-consistent phase-space solution. The engine does not currently return an operational splashback/turnaround surface or a covariant action. Its density or acceleration maxima do not define the CFG4 edge.

## 7. Recommendation dispositions

- Finish CFG2_A/B: executed in this mirror; interior E phenomenology survives, settled-capacity scope does not. Missing C/D must be implemented before cluster and cosmology claims are tested for that lane.
- Finish all five CFG3 scripts: scalar/SPARC/Solar main+mutation executed; CLASS/KiDS execution status is supplied by the run table appended below. Irrespective of scores, its compensated response edge requires redesign to target CFG4.
- Finish CFG5_1/2/3: runs reproduced where listed below; preserved failures are scientific results, not incomplete jobs. Missing 4/5/6 are absent code, not successfully executed analyses.
- Derive shell-crossing edge: a conditional hydrostatic matching construction and explicit history dependence are established; universal interval is not. A self-consistent growing-mode population and history-dependent observational propagation remain open, with the resolution control required first.
- Sole-fit-kappa construction: not achieved. Strongest usable reduced target retains interior P2, finite density support and conserved exterior mass; its host boundary and scope rule remain to be derived, and cold abundance/mass are retained inputs.

## 8. Additional structural controls

`structural_controls.py` verifies eight checks: the source-style neighbour estimator gives 6.02294e-6 artificial stress on an affine monokinetic flow at 600 samples; doubling samples with 24 neighbours changes it by .249891, while doubling neighbours to preserve the spatial fraction changes it by .969515. Removing the local affine velocity fit gives residual 2.26e-48; a symmetric two-stream case retains .0167037 stress. The mutation disables detrending and fails precisely the single-stream-cleanliness check. This is a synthetic diagnostic and candidate estimator repair, not a proof that this estimator cures the nonlinear shell code. The script also checks a nonzero clipped-F hydrostatic residual and the non-Gaussian finite-variance semigroup. The latter is explicitly positive: its characteristic function is the Poisson-weighted sum of n-fold Gaussian jump characteristic functions; per-coordinate variance is t, fourth cumulant is 3t. Its composition law therefore does not imply a Gaussian kernel.

## 9. Fresh CFG3 observational results

The exact-projector KiDS baseline reproduces FP20 to 5.7e-14 in chi-square. The fresh primary CFG3 lens model (compensated boundary, own free-fall frame and full residual tide) fails all six cells: delta chi-square +31.2, +37.8, +35.9, +41.6, +45.6, +48.1 against the +9 gate. Removing external tides altogether gives +8.4, -1.2, -2.3, +3.0, -4.4, +7.3 and passes, as an explicitly changed own-matter coupling rule. Half the tide still fails the alternate footing (+15.5 to +16.0). Gate radii range 1.64–7.52 Mpc across the reported baryon masses; those are not the CFG4 splashback density boundary.

The fresh web run has a strict reproduction failure K1: maximum amplitude discrepancy 4.4e-7, chi-square discrepancy 6.3e-5 and f-star discrepancy 2.0e-7, exceeding the source's 1e-9/1e-6/1e-9 tolerances. This is retained as a numerical reproducibility failure, not interpreted as an astrophysical exclusion. The local vanilla CLASS source build and extension hashes are in `class_provenance.json`; no source tolerances were relaxed. S1 gives the deliberately GR linear limit (amplitude 1), while the approximate compensated halo model gives 1.004–1.006. Its no-EFE shear proxy shifts S8 by +6.7/+7.7 percent; prescribed in-region fields .01/.03 a0 reduce it. Such prescribed fields and the halo-model approximation are conditional inputs.

CFG3 SPARC has a reported residual-trend failure (largest binned median .090/.058 dex against .05), despite its headline RMS pass. CFG3 Solar's 0.032-pc candidate has reported monopole failures, though the field-mass-tied Airy-length candidate passes its primary test. These passes do not derive the dark mass. CFG5 principle fails its alternate-footing plateau check: .710 versus .918, a .208 difference against .15; canonical .903 is within tolerance.

## 10. Obligation matrix and parameter accounting

| obligation | status | decisive evidence |
|---|---|---|
| Point-baryon P2 from specified pressure and central boundary | passed, conditional on those postulates | analytic reduction and CFG2_A |
| Same pressure law supplies extended-baryon RAR everywhere | failed | n>2 sign contradiction; clipped numerical branch is changed law |
| Field-stress reading E fits its registered SPARC statistic | computationally verified in this sample | CFG2_B main and zero-a0 mutation |
| CFG2 scope/capacity prescription preserves galaxy fit | failed | .1740/.1734 against .120 |
| Positive finite density edge with retained mass can match hydrostatics | passed in stated static weak-field family | edge main and Gauss mutation |
| Vacuum pressure alone selects the desired outer radius | failed for P_ext=P_cap or zero | r_M or no finite match |
| Shell-crossing condition alone selects [0.31,.48] | incomplete for target cosmological family; unrestricted implication refuted | history dependence and explicit tracer family |
| CFG3 boundary realizes CFG4's density edge | failed | compensated response cancels exterior phantom mass |
| CFG3 free-fall tidal model satisfies primary KiDS gate | failed in stated pipeline | +31 to +48, exact projector control passed |
| Gaussian uniqueness from declared semigroup assumptions | failed without stronger hypotheses | compound-Poisson counterexample |
| CFG5 stress cap entails RAR/flat BTFR | not established; simple cap-only implication refuted | empty-dark solution obeys cap; population model retains additional inputs |
| CFG5 continuum conversion budget | not established | original resolution failure, fresh run table, synthetic gradient contamination |
| Bound top-level membership and three-axis crossing from spherical engine | not addressed | no such output/object in source |
| One covariant action and well-posed dynamics for all required rules | not addressed | source leaves baryons-only action and matching selection unspecified |
| Simultaneous KiDS, cold-budget, clusters, Solar and galaxy gates | not established | individually fitted effective rules do not compose into one theory |

The primary fitted normalization remains kappa=1/2. CFG2 additionally profiles a global stellar mass-to-light normalization in its galaxy test; its dark-field mass and cosmological dark abundance are input quantities, and its E reading and scope are declared rules. CFG3's coherence length is tied to a dark-field mass, which remains an independent input; its occupation/coupling, region-frame prescription and baryon-only response are assumptions. The KiDS halo mapping and two-halo amplitude profiling are nuisance/model inputs, not derivations from kappa. CFG5 inherits the kick scale/splitting, dark-field mass/amount and coherent-conversion rule, plus empirical halo and cooling histories. Numerical regulator values are separately listed in section 6. Calling a constant “tied” does not remove the independent quantity to which it is tied, and calling an empirical population relation “fixed” does not derive it from the action.

The constant a0 prediction survives as a statement about the prescribed vacuum scale. It does not make every fitted halo-population BTFR coefficient constant. No accounting in this report promotes kappa to derived status.

## 11. Completed CFG5 runs and convergence discriminator

All twenty source-script executions (ten main, ten mutation) completed and produced scientific JSON. The complete scored table is `RUN_TABLE.md`, with machine detail in `run_table.json`. Every mutation has a named load-bearing scientific failure; none is counted merely for crashing. All Python-captured read inputs were unchanged during their runs. All inventoried original CFG2/3/5 files still match their initial hashes.

The fresh CFG5 collapse still fails C0b and H2a. At 10^12 solar masses, 600 versus 1000 shells gives h_max=.292606/.293076 but converted fraction .055659/.073718, beyond the source's 15% criterion. At 10^15 solar masses the dark pull is 1.226/1.169 a0, above its intended .918 cap. Cooling at 10^12 gives 1.27/1.66 a0. These reproduce the type of failure, not the old detailed numerical profiles.

The downstream CFG5 SPARC evaluation was run on the **fresh** main collapse JSON. Its primary fossil has RMS .1593/.1641 versus the same loader's .1453/.1421 reference. The alternate footing now exceeds its allowed .02 penalty (.0220) and H3a fails. The BTFR slopes 3.22/3.24 and normalization offsets +.219/+.153 dex fail H3d. Its z=2.5 zero-point shift is +.407/+.419 dex even though the cap's a0 is flat. Thus the source's old H3a pass is not robust to its own cap input regeneration.

`convergence_audit.py` executes six further canonical-footing, dark-only 10^12-solar-mass calls to the unchanged engine, with the actual imported source/module hashes and initial-array/power-spectrum hashes recorded in `convergence_results.json`. They took 14.0 s total, sequentially. The same-input repetition is bitwise identical in initial arrays, mass profiles and conversion budgets. This is direct evidence of repeatability in the present runtime.

| setting | h_max/a0 | converted / surviving dark mass inside own r200 |
|---|---:|---:|
| 600 shells, 24 neighbours | .292606 | .055659 |
| identical repeat | .292606 | .055659 |
| 1000 shells, 24 neighbours | .293076 | .073718 |
| 1000 shells, 40 neighbours (same neighbour fraction) | .361973 | .073664 |
| 600/24, time-step coefficient .015 instead of .03 | .311153 | .066451 |
| 600/24, input P(k) multiplied by 1+10^-7 | .318945 | .082501 |

Fixed smoothing fraction does **not** recover agreement: the peak acceleration moves +23.7%. Halving the time step moves the conversion mass +12.2%. A relative power-spectrum perturbation of only 10^-7 moves the conversion mass +33.95% and the peak pull +9.0%. These tests demonstrate strong finite-solver/input sensitivity and failure to establish convergence; they do not distinguish a rigorous dynamical instability from discontinuous shell ordering, conversion thresholds, time-step error and physical orbital chaos. A statistical population may need weaker converged observables, but those have not been supplied.

`source_history.json` verifies that the current engine, common module, driver and stored source output match HEAD. All first entered the record in incomplete handoff commit `1cbaea5db494f07216c2057aef96f6cc8630a212`; no later tracked source edit explains the discrepancy. The old files lack sufficient runtime and input-array provenance to reconstruct their exact generating environment. We therefore cannot uniquely identify the old discrepancy's cause. We can exclude changes made by this task, establish present-runtime determinism, and demonstrate an executable mechanism by which tiny upstream numerical differences become large profile/budget changes. The broad outer-NFW control remains passed, because it checks different radii and a 25% tolerance; it does not certify the inner acceleration or conversion budget.

`verify_convergence.py` independently checks the stored same-input repetition. Its mutation substitutes the genuinely perturbed-input run as if it were a repetition, and fails input fingerprints, output fingerprints and budget equality. This is an evidence-integrity mutation, not a second astrophysical simulation or a claim of physical falsification.

## 12. Current decision and executable continuation

Checkpoint HR01-COLLAPSE is complete as an audit/re-execution package, while the physical target remains unresolved. The present source lanes cannot supply the requested sole-fit-kappa construction or select the edge interval. The finite-density-edge equilibrium family is retained as the constructive matching target.

The smallest useful next implementation is a conservative phase-space or shell method with an explicitly defined stress smoothing/stream decomposition and convergence in shell count, time step and smoothing scale. It must output per-shell turnaround and first-apocentre events and a reproducible host-membership rule before an edge distribution can be scored. The existing fixed-neighbour and fixed-fraction variants have both been tested and neither supplies that convergence. A local gradient-subtraction estimator has passed affine one-stream and two-stream controls only; nonlinear and caustic controls are still required. That is a deferred implementation route, not an exhausted physical mechanism.

In parallel, the boundary-action route must specify the exterior stress or surface dynamics and demonstrate why it selects a small environment-dependent pressure rather than P_cap or an arbitrary offset. A valid action may then determine the radius from initial data; it must predict those initial-data statistics and pass the cold-mass budget and KiDS jointly on both footings. Choosing x=.4 or removing tides after looking at a fit does not complete that derivation. No self-consistent 3-D collapse, covariant action, full nonlinear cosmological likelihood or missing CFG2_C/D and CFG5_4/5/6 program was invented and labeled completed.

Final self-review covered the equations and numerical values in this report and the three new analytic/control scripts. The alternate MOND radius was corrected from a hand-rounded 3.514 to the computed 3.511 kpc. Mathematical domain restrictions and unproved action/stability statements are explicit; this proofreading does not upgrade the substantive proof-audit verdict.

## 13. Higher resolution, matched initial spin, and a bounded numerical repair

The requested additional fixed-neighbour-fraction test is in `convergence_refinement.py` and `refinement_results.json` (17.9 s). At 1000/40 with eta=.015, h_max=.345550 and converted fraction=.076163. At 2000/80 with eta=.03 these are .352087/.046632; eta=.015 gives .419680/.050199. These do not establish a converged regulated budget. Holding the neighbour fraction fixed approximates a fixed initial Lagrangian smoothing fraction, **not** an exactly fixed Eulerian physical width after shell rearrangement.

The original resolution test also changes the angular-momentum realization: `rng.uniform(.15,.35,N)` assigns a random number by shell index, but the Lagrangian coordinate at an index changes with N. The same random seed therefore does not make the initial angular field identical between 600 and 1000 shells. Such comparisons confound numerical resolution and finite-population realization noise. They cannot alone diagnose a discretization error.

`matched_benchmark.py` addresses that ambiguity using lamj=.25 for all shells, explicitly a numerical benchmark, not a parameter-free physical proposal. It compares `engine_constant_j.py` with `engine_constant_j_force_refresh.py`; both are owned copies and the original engine is untouched. The latter makes one additional numerical change: recompute enclosed mass and acceleration after turnaround angular-momentum injection, baryon cooling and daughter-conversion impulses, before the next half kick. The original computes acceleration before those impulses and carries that stale acceleration into the next kick/drift. The refresh is a justified local update, but does not implement event-time interpolation.

| constant-spin benchmark | h_max/a0 | converted fraction |
|---|---:|---:|
| original event updates, 600/24 | .359666 | .042288 |
| original event updates, 1000/40 | .374064 | .026873 |
| original event updates, 2000/80 | .399479 | .032447 |
| refreshed forces, 600/24 | .344494 | .034020 |
| refreshed forces, 1000/40 | .371842 | .033263 |
| refreshed forces, 2000/80 | .413468 | .032192 |
| refreshed forces, 2000/80, half time step | .412541 | .041728 |

At 600/24, the same 10^-7 spectrum perturbation changes converted mass by -25.7% under the original event updates and -20.2% after force refresh. Thus unmatched initial spin is not the only sensitivity source. The refreshed 2000-shell peak acceleration is stable under step halving, but its conversion mass rises by 34.0% and its reported fraction rises by 29.6%. The repair has not established the intended stress-trigger dynamics or its numerical error.

The remaining implementation questions are specific: turnaround/pericentre/apocentre transitions are endpoint sign tests without within-step event location; threshold conversion is sampled at `nstep % 5 == 0`, so the physical trigger times depend on adaptive step history; stochastic daughter directions are drawn in firing-event order, so changed event order changes their assignment to shells; and the neighbour stress mixes stream dispersion and smooth spatial gradients. Daughter quadrature and shell-count changes remain finite-sampling differences even in the constant-spin benchmark. A converged event-consistent, statistically controlled evolution is the missing computational ingredient. These observations do not constitute a theorem of physical instability, and no new physical success is inferred from the partial numerical improvement.

All benchmark profiles, raw budgets, actual source hashes and runtimes are retained. The final recommendation is to retain the hydrostatic matching target and implement/test event-consistent dynamics before claiming a collapse-selected edge or transporting the realized cap into a precision galaxy fit.
