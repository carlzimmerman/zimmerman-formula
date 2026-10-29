# CS28 verification and self-review

## Computation audit

Two successful bounded runs, with contracts established before execution:

* `run_verified/`: 15 named checks, including nine trajectories from all
  h,lambda in {0.3,0.6,1}. Each has 101 samples and stops at the first squared
  coupling reaching 4. Monotonic v, decreasing w/v, the integrated comparison
  inequality and finite exit before the analytic upper bound are checked.
* `run_hierarchy/`: 10 named checks, including all 12 combinations of
  L in {100,300,1000} and alpha in {0.01,1/30,0.1,1}. Direct evaluation of
  the original stiffness agrees with the hierarchy formula within 2e-15
  relative tolerance. This finite tolerance is not a numerical proof.

The underlying algebraic identities use exact rational SymPy expressions.
The ODE and numerical comparisons are float64. No random sampling, hidden
filters, early successful truncation, or fitted parameters are used.
The universal flow statements use the explicit algebra and inequalities
in DERIVATION.md; their universality does not come from nine trajectories.
SU(6) normalization is checked by Tr(H^2)=1 and a block trace, independently
of the beta-function derivation. The original stiffness and its eliminated
form are evaluated separately for the numerical comparisons.

Both successful version-2 manifests were validated with validate_manifest.py
and the repository root, checking input and output hashes. The first failed
run is historical only, as explained in README.md. Its checker used the
wrong type of expression equality; no physical equation was changed to pass.

## Focused proof audit

Reviewed every new equation in DERIVATION.md and HIERARCHY.md:

* Equation (3): forward invariance follows because at and beyond the initial
  boundary v_t is positive while w_t is negative. Integrating d(1/v)/dt
  gives the bound up to existence of the one-loop solution. Perturbation
  theory generally fails first; no exact high-energy pole is inferred.
* Equation (4): all three independent linear R constraints are included.
  The unitarity contradiction requires X to survive as a nontrivial
  gauge-invariant chiral primary and both couplings to be interacting.
  Solving R constraints does not exclude boundary fixed points or enlarged
  theories. Accidental free X does not retain the interacting-X hypothesis.
* Equations (5), (9): the block restriction is algebra, not a consistent
  truncation or an exhibited SU(6) vacuum. The additional multiplet fields
  and matching cannot be ignored in a physical completion.
* Equation (6): eliminate the gauge coupling using beta_h=0 and then impose
  gamma_B=gamma_X. The extra-gamma condition is necessary only. A change
  in the gauge beta coefficient alone does not change this equation.
* Equations (7)-(10): Lambda_5 is the SU(5) one-loop integration constant.
  Gauge thresholds, a physical low-energy confinement scale, and the
  field-to-renormalization-scale map are not identified with it. The
  nonzero alpha drift prevents treating a high-scale group relation as
  vacuum-scale matching without calculation.
* Equation (11): this minimizes only the stated parameter-dependent energy.
  Promoting parameters to chiral fields adds F terms and a kinetic sector;
  the calculation is not a theorem excluding stabilization in such a model.

The external SCFT facts were checked in the exact primary source identified
in SOURCES.md. No novelty claim or complete SCFT classification is made.
This is a self-audit, not independent review by another researcher.

## Mathematical proofreading

Scope: all new CS28 prose and displayed equations. All symbols, logarithms,
positive-domain restrictions and conditional equalities were checked in
context. Mathematical-token corrections during proofreading: none.
The initial checker equality fix was an implementation repair, not a
mathematical edit. Whitespace validation is included in the commit check.

## Unresolved physical obligations

No selected numerical ratio, full SU(6) model, stabilized coupling moduli,
complete gauged spectrum, threshold control, transverse quantum stability,
full gravitating energy, or derived halo portal has been established.
