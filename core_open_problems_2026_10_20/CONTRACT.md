# Four independent investigations of the core theory

Date: 2026-10-20 (America/New_York). Requested deliverable: independent research
on the four specified questions, checked and pushed to the repository. This is
a research checkpoint, not a claim that four open problems can be solved on demand.

Base checkpoint: `431f22bd6fe998759b843d13113762d73356aec6`.
The shared checkout contains substantial pre-existing untracked work. Each lane
owns only its numbered subdirectory; the coordinator owns this index and the
integration records. Existing theory statements and sealed predictions are read-only.
Input hashes pin working-tree sources that may differ from the base commit.

## Mathematical target

Use the canonical S2 action from
`campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md` and the subsequent
law adjudication `argon_push/AG4_law_from_action/`:

\[
\mathcal L=-\frac{|\nabla\Phi-K\mathbf P|^2}{2K}-\rho_b\Phi
-W_{\rm rem}(u)-\frac\gamma2|\nabla\mathbf P|^2,
\quad K=4\pi G,\quad u=K|\mathbf P|,
\quad K W'_{\rm rem}(u)=\frac{u^2}{a_0-u},
\quad \gamma=\frac{K L_*^2}{2}.
\]

The full polarization potential is
\(W_{\rm full}=W_{\rm rem}+u^2/(2K)\). Confusing these potentials
double-counts or removes the critical quadratic term.

In the aligned, unscreened static branch the capacity family is
\(u^2+n\bar g u=a_0\bar g\), \(g=\bar g+u\), with capacity
\(u<a_0/n\). Here \(n\) is a capacity coefficient, not a critical exponent.
For \(n=1\), \(\bar g=g^2/(g+a_0)\); for \(n=2\),
\(g^2-\bar g^2=a_0\bar g\). These are distinct laws.

The fitted scale is \(a_0=\kappa c\sqrt{G\rho_{\rm DE}}\),
\(\kappa=1/2\), where \(\rho_{\rm DE}\) is mass density.
The horizon surface gravity, a detector's background acceleration, the physical
acceleration, and the baryonic acceleration must be separately defined before
quoting any factor of two.

## Success and useful partial results

1. **Horizon normalization.** Success means a specified state, coupling and
   mechanism fix the dimensionless coefficient without importing the target
   value. A matching scale, a rescaled temperature, or an adjustable response is
   only conditional progress. Test curved-spacetime detector, information and
   saturation routes against their actual assumptions.
2. **Microscopic medium.** Success means a microscopic action or partition
   function produces the required potential and fixes the capacity coefficient.
   Reconstructed potentials remain conditional models. Give an observable
   distinguishing the two laws on the same footing.
3. **Relativity.** Success requires field-derived equality of lensing and
   dynamical potentials, luminal tensor propagation, an acceptable Solar-System
   limit, and physical stability including the endpoints of acceleration.
   A static Hessian or a schematic covariant action is insufficient.
4. **Stiffness.** Success means a physical mechanism fixes \(L_*\) with no
   constants selected to fit its window. Check the stated window against its
   actual provenance: CFG820 gives a conditional lower limit near 24 pc;
   1 kpc was CFG691's scan edge, and CFG832 estimates a soft upper edge near
   2.04/2.14 kpc under a point-source screening approximation. CFG821's
   incompatible dwarf limit is not a clean stiffness measurement.

Every lane must separate derivations under explicit hypotheses, bounded numerical
checks, analogies, empirical inputs, and unresolved obligations. A failed route
does not refute all possible mechanisms. Prior negative results must be checked
before repeating them. Finite scripts cannot certify an all-background theory.

## Independent work and integration

| Lane | Owner | Write scope |
|---|---|---|
| Horizon normalization | `horizon_normalization` | `01_horizon/` |
| Medium and law selection | `saturating_medium` | `02_medium/` |
| Covariant completion | `relativistic_completion` | `03_relativity/` |
| Origin of stiffness | `stiffness_origin` | `04_stiffness/` |

Workers start in isolated contexts and do not read each other's candidate
conclusions. The coordinator supplies source locations and reconciles conventions.
The runtime permits three concurrent workers in addition to the coordinator.
Reports must include exact input locators/hashes, reproducible commands, decisive
calculations, checked primary sources, and the smallest unresolved implication.
The coordinator re-runs computations and audits critical arguments before release.
After the initial independent investigations, the horizon worker was reused for
a separate raw-action review of the relativity calculation in
`05_independent_review/`, before seeing that worker's reduction.
