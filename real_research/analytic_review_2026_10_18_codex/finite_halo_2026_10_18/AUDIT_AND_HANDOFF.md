# Finite halo audit and continuation record

18 October 2026. Checkpoint ZAR-2026-10-18-02. Base Git revision `3c01aa2861bf576f4c2d942251eb9d2f89cae108`; parent analytic artifact `KINETIC_PARTITION.md`, SHA-256 `4fc5f73161d04197c5901fecfd97a2bdd2f3a9c33e685a487e22ca7eaf184758`. Parent files and shared research ledgers remain unchanged.

## Target contract and result

The user requested finite halo boundary matching and an analytic stability assessment for the kinetic extension, without scientific computation or interference with concurrent calculations.

The physical target is partially advanced. Finite equilibria and restricted radial stability are established for the same spherical energy. One exact-law annulus construction is a singular circular-orbit measure. A separate smooth isotropic family has a sufficient radial linear stability certificate in a dilute parameter regime. A finite smooth isotropic halo with substantial tether fraction, the galaxy-law profile and general dynamical stability remains open.

The model retains positive G and a0, separately conserved cold populations and fixed baryons. Its acceleration dictionary is the one in the parent note. No conversion, new pressure wall, damping, prescribed heat bath or uncounted force was added. Smooth extended baryons are explicitly introduced only in the regular isotropic core branch; the circular hollow branch keeps the point source. Neither branch implements finite stiffness or a relativistic completion.

## Claim cards and verdicts

| ID | Exact claim | Verdict |
|---|---|---|
| ZAR-F1 | Cutting the constant-f r^-2 isotropic density sharply at an attractive finite edge cannot yield a nonnegative compact isotropic DF merely by setting Jeans pressure to zero. | Refuted construction, with the local speed-support counterexample |
| ZAR-F2 | The displayed smooth M <= A r profile and constant-f circular measures form a finite self-consistent spherical equilibrium, exactly M = A r on an interior annulus. | Proved as written within the cubic effective model |
| ZAR-S1 | Its coherent spherical radial shell maps at fixed individual angular momenta have the displayed positive coupled quadratic and a coercive conserved linear energy. | Proved as written in that perturbation class |
| ZAR-F3 | The displayed positive linear-cutoff DFs have regular finite supports and no boundary wall in the stated baryonic-plateau regime. | Proved as written |
| ZAR-S2 | Compact isotropic equilibria with bounded central susceptibility and eta < 1 obey the stated supported radial linear energy estimate, assuming a well-posed linearized flow. | Conditional on that stated flow framework; sufficient bound attainable for F3 |
| ZAR-F4 | Lowered exponential finite seeds and small nonzero tether continuation approximate A r to any prescribed tolerance on a sufficiently distant annulus of any prescribed finite logarithmic width. | Analytic existence argument; stability not established for that branch |
| ZAR-M1 | The constant-f two-temperature leading isothermal asymptote has a positive spatial composition exponent for 0 < f < 1. | Proved as written; not a temporal-instability verdict |

All amplitude and fraction choices remain inputs. A circular-orbit family with positive energy variation is not an isotropic warm family. A dilute smooth stability certificate is not a stability certificate for the concentrated law-like branch.

## Dependencies and audit obligations

The new proofs use the parent energy and force dictionary, ordinary velocity integration, radial cumulative-mass variations, boundary conditions, Cauchy-Schwarz inequalities and ordinary differential equations. Their critical algebra is written in the proof files. No scientific computational leaf, empirical fit or borrowed single-species Vlasov stability theorem supports a new claim here.

| Obligation | Check performed | Status |
|---|---|---|
| Source dictionary unchanged | Differentiate the parent energy and keep tether response sourced by M_t alone | Passed |
| Boundary energy and force signs | Integrate each exterior acceleration to a potential with zero at infinity | Passed |
| Sharp isotropic cutoff | Compare Jeans edge ratio 1 with kinematic upper bound 2/3 | Passed obstruction |
| Core choice visible | Point source plus angular-momentum exclusion versus explicitly smooth fixed baryons | Passed |
| Circular positivity and normalization | M <= A r gives v_ct^2 > 0; integrate the velocity delta measure with its cylindrical Jacobian | Passed |
| No hidden shell or wall | Smooth filling and taper, zero cold radial pressure, continuous potential and force | Passed |
| Coupled radial quadratic | Reconstruct both mass variations; include angular kinetic energy; check density-term cancellations and surface terms | Passed |
| Coercive linear dynamics | Verify bounded weighted self-adjoint shell operator and lower frequency bound on finite hollow support | Passed for coherent shell maps |
| Isotropic finite radius | Integrate the explicit central bootstrap and simple-root bounds; prove no restart using the provisional empty exterior | Passed |
| Isotropic phase-space positivity | Direct velocity integration of the prescribed nonnegative energy DFs | Passed |
| Smooth stability criterion | Derive susceptibility bound and reciprocal quadratic conservation; include bounded central chi in upper norm estimate | Passed with stated hypotheses |
| Concentrated smooth stability | Eta may fail; exact radial form not proved positive for this branch | Not addressed |
| Nonspherical and nonlinear stability | Spherical energy does not supply a full angular action; linear norm does not control nonlinear crossing | Not addressed |

## Review provenance and corrections

Three parallel analytic routes worked read-only from the parent checkpoint: finite isotropic matching, energy-Casimir stability, and boundary obstructions/circular construction. The root separately reconstructed the force variations, shell Hessian cancellations, susceptibility estimate and composition matrix.

A fresh reviewer was then given the raw definitions and proofs, without an inherited route history, and reconstructed the circular measure, exterior fields and coupled second variation. Its primary verdict was proved as written for the explicitly restricted finite circular/coherent radial theorem. The isotropic matching author reread its proof and also checked the circular profile and sharp-edge obstruction. The stability reviewer checked the written weighted operator and the isotropic susceptibility argument. These are same-team mathematical reviews, not a formal proof certificate or outside peer review.

The written review produced three clarifications, incorporated in the final files:

1. The no-restart proof freezes M_t(R_t) in a provisional empty continuation before identifying it as total tether mass; the total is not assumed in order to prove emptiness.
2. The lowered exponential continuation now states both species' DFs and holds H and its coefficient fixed while varying tether amplitude and central height.
3. The smooth-core upper stability norm explicitly assumes bounded central susceptibility, which the constructed cutoff equilibria satisfy.

An exterior wording qualification also restricts the positive critical-point statement to nonzero tether stock. The circular construction can be placed sufficiently far into the deep regime; it is not presented as a full-interpolation result.

Generic circular-orbit spheres, cutoff energy distributions and energy-Casimir estimates are established mathematical methods. Their explicit application to this response/mass dictionary and the displayed coefficient identities are the contribution of this continuation. Global novelty has not been investigated or claimed.

## Route status and next analytic work

| Route | Mechanism and decisive check | Current status | Continuation |
|---|---|---|---|
| Sharp isotropic truncation | Finite nonzero edge density versus compact isotropic velocity support | This construction closed by contradiction | Reopening requires a taper, anisotropy or a physically counted nonvacuum boundary |
| Finite circular annulus | Smooth cumulative taper and circular orbit measure; positive full radial shell quadratic | Finite equilibrium and restricted radial linear stability achieved | Introduce finite radial action width and test whether positivity persists; no unchecked transfer from the singular limit |
| Regular isotropic finite branch | Positive cutoff DF and finite-radius bootstrap; susceptibility certificate | Existence and a stable dilute subset achieved | Admit an actual galaxy-like susceptibility before claiming dark-dominated stability |
| Concentrated smooth annulus | Finite lowered exponential approximants with small tether stock | Existence argument retained; stability open | Apply the exact coupled radial energy form or a dynamically accessible mode analysis to this same branch |
| Arbitrary constant-f smooth matching | Outward composition system has a growing spatial mode | Generic matching ruled out; tuned trajectory unproved | Derive an admissible core-to-edge trajectory or allow a derived f(r); spatial growth alone does not settle temporal stability |

The cheapest next discriminator is analytic, not a numerical scan: choose an angular-momentum distribution with small nonzero radial width around the circular construction, derive its self-consistent density and finite transition layer, and test the actual kinetic quadratic. A finite-dimensional shell calculation must not be relabelled full Vlasov stability.

All uncompleted physical routes remain open. Three-dimensional dynamics first requires an actual angular extension of the spherical action. Formation and fraction/amplitude selection need counted currents and any receivers. Cosmological donor compensation and observational matching are not supplied by an isolated finite cold stock.

## Resource and verification record

Scientific scripts, numerical integrations, simulations, statistics and process operations: none. Existing job state was read only from the previously designated status file; it was not inferred from process inspection or changed. Verification used analytic rederivations, read-back, source-file hashes, local-link and math-delimiter checks. These document checks are not physical validation.

The exact source and final artifact hashes, proof-review revisions and verification outcomes are in [CHECKPOINT.json](CHECKPOINT.json). The parent checkpoint remains the ancestry anchor; arrival order of agent results does not supersede it.
