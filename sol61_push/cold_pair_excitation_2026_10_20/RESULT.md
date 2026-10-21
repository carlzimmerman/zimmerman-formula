# Actual fragment collisions: concentration, outward transport, and a mode-acceptance gap

The prepared in-phase pair produces a central concentration and exports energy and conserved cold charge through large control surfaces. The opposite-phase pair separates again. This is an actual same-action field-evolution result, beyond a stationary binding-energy gap or an imposed cooling coefficient. It does **not** establish a weak-mode cooling law for the nonlinear remnant, a physical dwarf capture rate, or a successful four-dwarf mass budget.

This packet tests an explicit alternative charged-matter action, not an adopted completion of the canonical polarization framework. Its physical mass/time normalization and population bridge remain open. Frozen publications, Claude's criteria and `cold_final_mile_2026_10_13/CURRENT.txt` are unchanged.

## 1. Action and finite experiment

Use canonical complex kinetic terms for charge-one Psi and charge-two X, and a half-normalized real kinetic term for chi. In dimensionless units,

    V = |Psi|^2 + 4.0016 |X|^2
        + g (X* Psi^2 + X Psi*^2)
        + lambda |Psi|^4 + 200 chi |Psi|^2 + U(chi),
    g = .002168,
    lambda = 1.99 + g^2/4.0016,
    U(chi) = 10000 chi^2/2 - 100 chi^3/8 + chi^4/4.

The full five-real-field equations evolve without damping, an imposed target profile, a fitted collision efficiency, or a receiver. The common U(1) current is

    Q = integral [2 Im(Psi* Psi_t) + 4 Im(X* X_t)] dV.

The model's binding mechanism is explicit. Eliminating the neutral field locally at fixed I=|Psi|^2 and eliminating static X gives the low-density configuration-potential expansion

    V_local(I) = I - .01 I^2 + .0001 I^3 + 2.875e-8 I^4 + ... .

The attractive quartic term competes with stabilizing higher terms; gradients supply an additional finite-size cost. Exact local minimization at I50 gives V/I=.7535292070<1. `EFFECTIVE_BINDING_MECHANISM.md` audits this15-check derivation. It explains how self-binding is possible in this specified action, not why nature chooses this matter/action. A rotating stationary reduction instead has the X denominator MX^2-4omega^2 in E-omega Q. Local elimination omits gradients and retardation and is not a replacement full dynamical action or proof of a stable continuum fragment family. The full fields, including the neutral field, are evolved in every experiment here.

Stationary seeds come from the previously pinned true-origin Q80000 branch. The new solver uses conservative cylindrical finite volumes, a regular axis, zero Dirichlet outer faces, and kick-drift-kick time stepping. Lorentz-contracted fields, carrier phases and advective velocities are all included in the boosted seeds. Finite-overlap superposition and cell sampling change actual initial E/Q; the logged values, rather than nominal 2×80000, are used throughout.

Eight field runs were declared: the in-phase pair, half timestep, finer spatial grid, opposite phase, larger separation, faster pair, static isolated fragment and translating isolated fragment. Primary geometry is Nr=188, Nz=480, dx=.75, dt=.005, T=240; the finer grid uses dx=.5 at the same box size. The pair has initial centres z=±12 and individual speeds ±.1. The separation control uses centres ±16, and the faster control speeds ±.2. These are fast dimensionless head-on tests with zero orbital angular momentum. They are not dwarf-velocity experiments. The stated finite interval and domain do not establish long-time escape or a continuum limit.

## 2. Concentration and charge retention

| Case | Actual initial Q | Q within r15 at t240 | Q within r20 at t240 | Q15 / initial Q |
|---|---:|---:|---:|---:|
| in phase | 160485.927 | 137157.352 | 139093.659 | .854638 |
| half timestep | 160485.927 | 137157.237 | 139093.574 | .854637 |
| finer space grid | 160310.804 | 136264.560 | 138373.508 | .850002 |
| opposite phase | 160143.294 | 2007.261 | 50014.212 | .012534 |
| larger separation | 160318.019 | 138256.977 | 140104.035 | .862392 |
| faster pair | 160295.734 | 127662.396 | 129048.221 | .796418 |

These are **aperture inventories**, not certified bound masses or physical dwarf core fractions. The in-phase remnant has one near-axis carrier-density peak late in the interval; its shape still oscillates. Opposite phase produces departing peaks near z=±21.4 at t240. The larger-separation time history is delayed by about40 time units, so comparisons should align collision stage rather than equate all t240 snapshots. A moving isolated fragment also crosses fixed apertures without thereby radiating its entire lost inventory.

Halving dt changes the in-phase final Q15 by .114 and Q20 by .085; spatial refinement changes the final central charge by about .65%. Primary maximum relative energy error is 3.48e-6 and falls to 8.32e-7 with half dt. Global Q is conserved to rounding precision. These controls are useful at the tested fast speeds; they do not provide the ~1e-12 relative energy accuracy needed to resolve a very small galactic orbital-energy difference directly against the rest energy.

The scientific figures are `analysis_run_001/pair_density.png` and `pair_diagnostics.png`. The latter deliberately labels |c|^2 as a conditional coordinate.

## 3. Actual outward currents

`FACE_FLUX.md` derives and independently tests the signed currents of the same finite-volume action. For an interior face i→j with symmetric conductance Cij,

    F_E(i→j) = sum_a fac_a Cij (q_ai-q_aj)(v_ai+v_aj),
    fac = (1,1,1,1,1/2),
    F_Q(i→j) = -2 Cij Im(Psi_i* Psi_j)
               -4 Cij Im(X_i* X_j).

For an aperture mask these currents exactly reproduce the continuous-time derivative of its positive-face-allocated energy and charge. Independent ODE differentiation gives normalized continuity residuals around1e-12. The audit has524 passing checks and does not evolve fields.

At r30 in the in-phase run, initial-minus-final E/Q inventories are18415.127/17473.249. Integrating the saved currents gives18118.764/17192.882, with E/Q=1.05385. The E inward/outward split is -31.150/+18149.914. At r40 the net integrals are E11489.212 and Q10711.476. There is real predominantly outward transport, rather than a conclusion based only on energy allocated outside a chosen aperture.

The saved20-time-unit current quadrature reproduces the in-phase aperture changes within roughly1–3%; half-dt results agree very closely, and spatial refinement changes net currents by roughly2–3.4%. Full accuracy and sign splits are retained in the audit. Opposite phase exports enormous bound-fragment inventory across r20 but very little across r40. Consequently aggregate E/Q, aperture loss and an outward sign do not alone classify the transport as free radiation. The finite reflecting box is globally closed; a surface crossing is not permanent escape from that box or a galaxy.

## 4. The collision excites a large coordinate; weak-mode acceptance fails

Using the depleted core's old Q160000 template would conceal a substantial reference error. New Q136000/Q140000 references were independently solved on N599/1199 grids, with exact discrete charge, localized unit-K ell2 candidates and residual controls. `MATCHED_REFERENCE_RESULT.md` preserves failed Newton-cap attempts and the byte-identical recovery provenance. The profiles are explicitly interpolated discrete references, not new continuum BVP solutions.

| Reference Q | carrier omega | localized Omega | weak Y20 gamma |
|---|---:|---:|---:|
| 136000 | .9120838357 | .0603874061 | 1.71359134e-5 |
| 140000 | .9116133427 | .0595870453 | 1.67189093e-5 |

The new radiation coefficients are recomputed on each fine reference, with positive outgoing flux, source-work balance and residual checks. They are not a freshly box/grid-converged nonlinear collision rate. The m0 source follows

    Y20^2 = Y00/sqrt(4pi) + sqrt(5) Y20/(7 sqrt(pi))
            + 3 Y40/(7 sqrt(pi)).

Only the Psi+ second-harmonic channel is open for these reference modes. Its weak-amplitude law is conditional on an accepted near-stationary linear mode:

    K = |c|^2,
    c = -i Omega/kappa integral Z* [v+(G+i Omega)q] dr,
    Kdot = -gamma K^2,
    Qdot_out = -Kdot/(2 Omega),
    Edot_out = [1+omega/(2 Omega)] (-Kdot).

For the actual in-phase remnant, the conditional coordinate is large: late |c|^2 is about378–644 at Q136000, versus at most .0113 in the evolved isolated Q80000 control. It is stable under timestep refinement, changes less than about2% under the Q/frame choices tested, and changes up to about9.5% under spatial refinement. A real non-spherical excitation is present.

However, the ell2 positive-state reconstruction residual fraction is typically .32–.53 late, and the full-field reference mismatch is about .45–.59 over the projection region. A seven-sample exploratory complex fit gives .0491 rather than the reference .06039/.05959. Its small fitted residual does not make that rate a nonlinear eigenfrequency: the finite window is only about one reference cycle, the fit has several coefficients, and the original per-snapshot phase choice need not define one consistent carrier frame. `REVIEW_PAIR_ANALYSIS.md` makes these limitations explicit. The robust conclusion is a large **conditional quadrupole coordinate in a mixed, nonstationary remnant**. It is not an accepted modal energy fraction or a measured gamma K^2 cooling law.

In particular, inserting the fitted coefficient near500 into the weak formula would replace the missing physical acceptance with an assumption. No such insertion is used to declare cooling, a retained charge, or a galaxy fit.

The separate152-check fixed-carrier audit then anchors the phase at t120 and propagates it with exactly omega_reference, consistently with the velocity transform. It gives fitted coordinate rates .04975–.05080 across reference/grid choices, still about14.7–17.6% below the corresponding linear modes. Coordinate squared changes by up to21–23% and fit residuals worsen to10–12%, so the earlier small frame-choice sensitivity applied only to the velocity-frequency choice, not this stronger phase-propagation test. Core-only r<12 field mismatch remains about .23–.41: outer waves alone do not explain it. `FIXED_CARRIER_RESULT.md` records the accepted finite sensitivity conclusion and its unaccepted physical implications.

For a genuine outgoing second-harmonic Psi+ wave, the channel kinematics are

    nu = omega + 2 Omega > 1,
    Omega_cut = (1-omega)/2,
    Q_out/K_out = 1/(2 Omega),
    free_Psi_kinetic/K_out = (nu-1)/(2 Omega).

At the two linear references, the cutoff is about .0440/.0442, the free-wave group speed is .250/.243c, and only .272/.258 of rotating excitation becomes free-Psi kinetic energy. The rest of that excitation pays the cost of unbinding charge; lab energy additionally carries its rest-energy contribution. If a real nonlinear mode softens toward the cutoff, its free-kinetic fraction tends to zero and its propagation channel closes there. The fitted coordinate rates are not physical frequencies to insert into this law. Radiation energy cannot all be reassigned as useful galaxy-centred wind energy while retaining the same charge stock.

## 5. Four-dwarf implication and Claude's new evidence

`FOUR_DWARF_GATES.md` pins the older CFG918 endpoints and their exact force, stock and aperture semantics. Under the still-unproved scalar-to-galaxy stock identification, the optimistic necessary products f_proc f_mode R eta_orb are3.67e-6 for Draco,2.32e-5 for Sextans,3.52e-5 for Fornax and3.96e-5 for LeoI. This is an energy-capacity condition, not an achieved transfer efficiency. Stellar heating, galaxy-centred angular-momentum export, wave-to-wind conversion, replenishment and survival are additional conditions.

Sextans' old endpoint leaves only1.146% of its available free stock for its reference wind. The field-pair experiment demonstrates charge transport; it does not justify ignoring that cost or identifying every crossing with that wind. Under the same old global-moment C-profile interpretation, even all available stock gives6.9358km/s rather than7.9km/s; within Re, the saved endpoint instead gives8.417km/s. That conditional profile/aperture obstruction must be resolved with an observationally matched endpoint and a new E/Q/J budget, rather than fixed by a cooling coefficient alone. Fornax/LeoI's old global guards also do not automatically guard a finite stellar aperture.

`CLAUDE_937_ARRIVAL.md` independently reconciles exact criteria73144fddb, seal a8792e8b4 and result d1b1b476f against raw artifacts. CFG937's hotter filtering floor can turn on Draco supply, but the primary result remains PARTIAL, corner-selectable and FRAGILE. All four target dwarfs get the same late-former label. Sextans' label is a group default; the own-evidence variant removes its filtering-floor assignment. Raising the common floor also raises Fornax/LeoI stock and can overboost UFDs. It supplies no derived cold concentration, transport, mass normalization or torque law. CFG937's assumed collisionless NFW-halo prescription is distinct from this packet's alternative matter action. CFG940 was criteria-only at that initial arrival checkpoint.

**Later finalized arrival:** `CLAUDE_940_ARRIVAL.md` reconciles CFG940 criteria798e98d78, amendment bda93d8db, results7c7fc125e and README ba794bf4f. The primary g_bar<1e-12 window has zero rotators and is NOT DIAGNOSTIC(DATA). Secondary all25 is below the law under total-baryon estimator A but on the law under enclosed-disc B; this bracket cannot be silently removed. The available matched dSph-minus-rotator contrast is about .32–.44 dex at g_bar>=1e-12, which narrows a pressure-supported/rotating population question without testing the missing lower-acceleration regime or the four individual dwarf budgets. Exact source/report qualifications, boolean-string handling and preserved failed K3 control are retained in that new audit. It supplies no microscopic capture, energy-export or spin-selection law.

No conclusion here says that Draco/Sextans are successfully concentrated while Fornax/LeoI are protected. The actual advances are a demonstrated finite collision/transport channel, an explicit phase dependence, and a stricter identification of the missing nonlinear cooling and population-selection calculations.

## 6. Prepared-state discriminator: large-amplitude relaxation is possible, weak loss remains unresolved

A new initial-state loader leaves the field equations and integrator unchanged. Its test-first old-binary attempt fails because the interface was unsupported; the new binary passes18 checks, including byte-identical existing static/moving evolutions and rejection of malformed initial states. The failed attempt remains failed.

The first clean linear-coordinate seed audit exposes a useful failed implication: nominal K50 has actual nonlinear Delta(E-omega Q)=549.09, and nominal K500 has50811.41, rather than50/500. It also changes Q. The huge excess comes from applying an undressed linear Cauchy perturbation at finite amplitude; an accurate linear-coordinate projection is not enough to define a clean finite-energy mode. Those raw seeds were not evolved or called energy-matched nonlinear modes.

The next controlled comparison explicitly prepares the massive mediator's quasistatic response on the same grid:

    -Lap h + U'(h) = -200 |Psi|^2,
    (-Lap+U''(h)) hdot = -200 d|Psi|^2/dt,
    U''(h) = 3(h-100/8)^2 + 61(100)^2/64 > 0.

At fixed charged arrays this has a unique discrete neutral configuration minimizer. The audit verifies its residuals, energy variation, exact charged-array/charge preservation and tangent. This is a construction of **different initial data**, not emitted energy or a demonstrated physical formation process. During subsequent evolution h is an ordinary dynamical field; it is not constrained to the static manifold. `CHI_DRESSED_PREPARATION.md` records56 passing initial-data controls.

Four conservative evolutions then completed8/8 checks each through T240, with snapshots every10. All use the same188×480 coarse geometry and dt=.005; no additional refinement of these four cases is claimed. `DRESSED_ANALYSIS_RESULT.md` and its552-check bounded analysis retain actual Q, full E, baseline-relative Delta(E-omega_ref Q), independent carrier conventions and train-only/held-out coordinate comparisons.

| Nominal coordinate squared | Actual initial Q | Initial Delta(E-omega_ref Q) from K0 | Final K0-subtracted coordinate squared | Dominant fitted coordinate rate | Held-out complex residual |
|---|---:|---:|---:|---:|---:|
| 1 | 136220.488 | .837048 | 1.000004 | .05955 | .00785 |
| 50 | 137537.669 | 48.909765 | 39.265050 | .05860 | .05385 |
| 500 | 149498.217 | 890.681279 | 102.916939 | .05325 | .17765 |

The weak coordinate stays within .9716–1.0278 throughout. The strong coordinate changes substantially and is less coherently represented by the fitted basis. The fit uses20..180 for training,190..240 only for prediction, and both signed fundamental/second harmonics. Harmonic aliases are reported explicitly. None of these coordinate powers or fitted rates is an automatically accepted nonlinear modal energy/eigenfrequency. Even the weak evolved reference rate is1.39% below the fine radial reference, so attributing that whole discrepancy to physical amplitude softening would be incorrect. Between amplitudes, actual Q also changes: a frequency change cannot be assigned purely to amplitude at fixed charge.

The maximum baseline-difference drift of the conserved Delta(E-omega_ref Q) is1.23e-5, .0006063 and .0132634 for nominal1/50/500, respectively. These are about1.5e-5 of their actual initial baseline-relative values, much smaller than the strong exported signal. This conserved baseline difference is not the same as E-E_stat(Q_actual), which still requires an accepted actual-charge core reference.

The separate1004-check face-current audit reads all100 prepared-state snapshots, without advancing fields. At r30 the whole-interval endpoint inventory drops are:

| Nominal coordinate squared | E drop | Q drop | E drop minus K0 control | Q drop minus K0 control |
|---|---:|---:|---:|---:|
| 0 | 1.624102 | 1.272184 | 0 | 0 |
| 1 | 1.473241 | 1.141902 | -.150861 | -.130282 |
| 50 | 53.986694 | 50.076444 | 52.362592 | 48.804260 |
| 500 | 3585.009614 | 3144.400358 | 3583.385512 | 3143.128174 |

The strong case has real predominantly outward currents and retains roughly97.9% of its box charge inside r30 at T240. This demonstrates a finite relaxation/export capability for prepared finite-amplitude cold-core disturbances in the specified action. It does not classify all exported material as freely escaping waves, identify its spectrum with the one weak mode, or supply a dwarf capture efficiency. The small case's control-subtracted endpoint loss is negative: weak monotone radiative loss is **unresolved by this comparison**, despite numerical conservation passing.

There is a further important failed implication. In the strong case, integrating currents only every10 can substantially mis-estimate the early impulse. At r20 its whole-interval E-flux integral exceeds the endpoint drop by about314.94; control subtraction leaves312.78 of that discrepancy. A coarsely integrated rotating-current estimate can even appear to exceed the initially prepared baseline-relative excess. The endpoint E/Q budget does not do so. Keep the actual early/late windows and discrepancies in `DRESSED_FACE_FLUX_RESULT.md`; do not infer a physical efficiency or weak gamma from that undersampled integral. Higher-cadence currents and outgoing-state classification are the concrete next tests.

## 7. Interpretation and next action

The mechanistic chain now has actual finite evidence for self-binding in an explicit alternative action, phase-dependent pair concentration, quadrupole excitation, and conservative outward energy/charge transport. Preparing the heavy mediator correctly is essential; otherwise initial-data energy can masquerade as cooling. At finite amplitude the full state and charge budget matter, not just one linear coordinate.

The remaining central failure is the inference from those capabilities to a calibrated nonlinear cooling/capture kernel and then to four different dwarf outcomes. `NEXT_TEST.md` specifies the next radiator, boundary, spectral, nonzero-J and population/stock gates. No four individually adjusted efficiencies, universal late-former filling rule, unchanged-charge cooling assumption, or dimensionless-to-galaxy conversion is inserted to close the theory.

All prior frozen sources and publications remain untouched. Historical compiler-version declarations are corrected separately in `METADATA_CORRECTION.md/json` without rewriting frozen contracts/manifests: the directly observed build receipts identify clang21; the v2 build receipt does not contain its own compiler-version observation. Use pinned source/binary hashes and exact receipt scope. A software metadata correction is not a new physical result or a silently reconstructed historical observation.
