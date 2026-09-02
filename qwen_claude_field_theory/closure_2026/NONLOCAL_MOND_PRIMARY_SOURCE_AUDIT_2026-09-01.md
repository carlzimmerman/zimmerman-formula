# Primary-source audit: what nonlocal metric MOND actually establishes

Date: 2026-09-01
Scope: action provenance, lensing, causality, degrees of freedom, PPN, stability, and cosmology relevant to the strict fried-chicken target.

## Source question

Do the primary nonlocal metric MOND papers provide one ordinary varied action which simultaneously gives a causal retarded theory, exact preferred interpolation
`mu(y)=1-exp(-y)`, no slip, two gravitational degrees of freedom, acceptable full PPN, ordinary matter conservation, stable FLRW, and no hidden auxiliary mode?

## Search record

Searches used SciSpace semantic search and direct primary-source verification on arXiv. The relevant primary papers are:

1. M. E. Soussa and R. P. Woodard, [A Nonlocal Metric Formulation of MOND](https://arxiv.org/abs/astro-ph/0302030), Class. Quant. Grav. 20 (2003) 2737.
2. C. Deffayet, G. Esposito-Farese, and R. P. Woodard, [Nonlocal metric formulations of MOND with sufficient lensing](https://arxiv.org/abs/1106.4984), Phys. Rev. D 84 (2011) 124054.
3. R. P. Woodard, [Nonlocal Metric Realizations of MOND](https://arxiv.org/abs/1403.6763), Can. J. Phys. 93 (2015) 242.
4. C. Deffayet and R. P. Woodard, [A Nonlocal Realization of MOND that Interpolates from Cosmology to Gravitationally Bound Systems](https://arxiv.org/abs/2512.10513), JCAP 04 (2026) 081.

## Verified content

### Soussa--Woodard 2003

The paper constructs causal, covariant, conserved nonlocal metric field equations and reports no extra weak-field graviton solutions in the analyzed sector. It reproduces MOND forces but explicitly finds insufficient lensing. It therefore fails the strict lensing gate and is not a completion of the target.

### Deffayet--Esposito-Farese--Woodard 2011

The paper constructs pure-metric nonlocal invariants which reproduce deep-MOND force scaling and sufficient lensing. Its weak-field MOND action is an ultra-weak expansion; the paper does not select the exact exponential interpolation required here. The construction is a decisive counterexample to any claim that covariance plus a single metric automatically forces the old scalar-curvature slip, but it does not supply a full Dirac count, full PPN parameters, or a stability proof satisfying the present target.

### Woodard 2014/2015

The paper supplies full nonlocal field equations for a model class and specializes them to cosmology. It presents cosmological reconstruction as further work and discusses auxiliary localizations as calculation devices. It does not prove that retarded history conditions are Dirac constraints, nor does it close the strict two-DOF/no-hidden-mode target.

### Deffayet--Woodard 2026

The paper combines a cosmological dust-like nonlocal functional with a bound-system MOND functional. Its equations distinguish the CDM-like density `rho` from baryonic density `varrho`. The local mimetic Lagrangian has independent fields `phi` and `rho`; the nonlocal model instead fixes their histories as functionals of the metric. The paper itself describes the cosmological sector as dark matter expressed as a nonlocal metric functional. It does not derive the exact preferred exponential kernel, the five PPN parameters, or a nonlinear two-tensor Dirac certificate.

The shared-current relation used in the repo is conditional. If two scalars obey

    D rho + theta rho = 0,
    D Q   + theta Q   = 0,

then `D(Q/rho)=0`. If the second equation has a source `S`, the executable result is `D(Q/rho)=S/rho`. This is a property of that common transport structure, not a theorem about every nonlocal MOND memory and not a lock to baryonic density.

## Dependency classification

| Claim | Source status | Strict-target status |
|---|---|---|
| Pure metric nonlocality can give sufficient MOND lensing | Directly established by 2011 construction | Useful surviving direction |
| The exact preferred `mu=1-exp(-y)` is derived | Not established by these sources | Open |
| Strictly retarded equations follow as the Euler--Lagrange equations of an ordinary one-copy nonlocal action | Not established | Open/obstructed by reciprocity |
| `N_grav=2` with no hidden auxiliary data | Not established nonlinearly | Open |
| Full `beta,gamma,alpha_1,alpha_2,alpha_3` | Not established | Open |
| Stable expanding FLRW with the same exact galaxy kernel | Not established | Open |
| All nonlocal MOND necessarily contains a baryon-tracking dark field | Not established; 2026 ratio lock is model-conditional | Withdrawn |

## Mathematical consequence for this repository

The papers keep nonlinear pure-metric nonlocal MOND scientifically open, but they do not satisfy the repo's strict victory conditions. The defensible new obstruction is narrower: a strictly retarded integral kernel is nonsymmetric, whereas the second functional derivative of an ordinary one-copy action is symmetric. A retarded solution may of course be selected for a local differential Euler--Lagrange equation by initial data; what fails is treating the retarded inverse itself as the Hessian kernel of an ordinary one-copy nonlocal action. Standard localization restores a local action but yields a regular indefinite response/multiplier pair unless an additional genuine constraint removes it.

Executable evidence: `nonlocal_door_2026/nonlocal_universal_claim_audit_2026.py` and its regression test.

## Result

No source found closes the fried-chicken target. The 2026 universal dark-field theorem is not supported by the primary literature and is refuted by the local AQUAL boundary-flux counterexample. The global theory question remains **OPEN**. The standard one-copy retarded-`Box^-1` realization is **DEAD under the stated variational assumptions**; a genuinely doubled in-in construction or a new elliptic constrained action must be analyzed separately.
