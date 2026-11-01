# TP02: weak-coupling threshold/RG matching and microscopic matter coupling

Owner authorization, 1 November 2026: continue TP01 by matching quantum
thresholds and RG flow, deriving the matter coupling, and testing whether
the pressure obstruction survives higher-order corrections. Base revision:
`40d43dbb8a9f1517e214302380f7659df7626e6a`. The shared checkout is active and
dirty. TP01 artifacts are immutable inputs; their hashes identify versions.

## Exact targets

1. Derive a consistent renormalization-scale dictionary for the specified
   canonical-K rigid SU(5) action and its full one-loop thresholds. Check
   Callan–Symanzik cancellation before improving the potential. Include
   coupling, dimensional parameter and wavefunction running at the order
   claimed. Distinguish RG-resummed logarithms from a complete finite
   two-loop threshold calculation.
2. Start with genuinely weak couplings and test the pressure boundary under
   justified higher-order improvements, scale variation and independent
   differentiation. Unselected coupling boundary values are explicit trial
   inputs. Do not choose them to fit a0 or a desired pressure outcome.
3. Derive the occupied-state coupling from actual microscopic modes where
   possible. Retain field-dependent rest energies, kinetic terms, state and
   number assumptions, gauge charges, phase/light modes and induced forces.
   The former W=K exp(-2s)+U portal is a comparator until derived. A changed
   matter coupling defines a different pressure problem and must be labelled.

Proof or controlled continuation would establish a precise small-coupling
statement with its uncertainty/order. Finite numerical persistence is only
evidence in the sampled schemes/parameters. A missing cosmological state,
new stable species, portal, gauge/IR matching or gravity input remains a
named open dependency. No fully matched theory or universal no-go is
presupposed.

## Portfolio and ownership

- `rg_threshold/`: RG-improved full-threshold calculation, assigned to the
  spectrum researcher; no changes to TP01 source files.
- `matter_coupling/`: microscopic occupied-state action and pressure, assigned
  to the matter researcher. Starts from the raw SU(5) action and spectrum.
- `rg_derivation/`: independent beta/anomalous-dimension, scale-invariance
  and truncation audit, assigned to the algebra researcher.
- Coordinator: contract, source checks, interface reconciliation, combined
  verification, current status and continuation.

Each researcher writes only its directory. Pin exact inputs; freeze a
finite contract before execution. Mathematical derivations and experiments
must disclose hypotheses, field/scale conventions, counts, excluded regimes,
controls, software and hashes. Use bounded v2 evidence records and fresh
output directories. Preserve failed attempts and source versions.

Use one numerical thread, minutes per individual experiment, low memory
(below 1 GB where feasible); no new production simulations, downloads,
package installation, queue modification or Git staging/commit/push. Read
primary sources through authorized tools as needed. macOS affinity and
address-space limits are unavailable: use supported wall/CPU/thread caps and
report observed RSS, never claim an unenforced cap. No pre-existing paper,
seal, solver, theorem, TP01 artifact or scientific input is changed.

At each substantive result pursue the cheapest unresolved implication within
these resources, rather than stopping at an unexecuted proposal. Cross-review
the critical matching and pressure derivations before physical interpretation.
