# TP02 continuation: what is known and the next missing operator

Authorized target: start weak, match quantum thresholds/RG, derive the
matter coupling, and test persistence of the pressure obstruction. Base
revision `40d43dbb8a9f1517e214302380f7659df7626e6a`; actual versions and
commands are pinned by the route manifests. Read README.md first.

## Reached at this checkpoint

- Complete one-/two-loop rigid-model running and full one-loop CS identity;
  reference-X, canonical-T and heavy-valley transport dictionary.
- RG/finite-one-loop thresholds and required scale logs at e=.01,.03,.05,.1;
  all 28 old-comparator scheme cases retain the pressure obstruction.
- A genuine calculable finite next-order heavy-relaxation subset, tested on
  all four weak points; it also retains that comparator failure.
- Derived phase-current coupling and actual mode rest/kinetic coupling,
  their reciprocal work and pressure laws. Complete known occupied heavy
  relaxation includes its quartic-charge term. The phase is pressure-rich;
  an explicit cold massive-mode window lacks a protected population/lifetime.
- Independent tensor contractions, field/CS reconstruction, pressure and
  Legendre audits; numerical domains and all current hashes verified.

## Exact uncomputed implications

1. **Finite two-loop matching.** The full reduced finite U2 at a chosen
   reference scale includes genuine diagrams plus the already computed
   heavy displacement. Construct the missing diagrams in the same
   Landau-gauge supersymmetric subtraction convention; count the heavy
   term once. Scale logs and beta functions cannot fix this finite function.
   Preserve the existing partial prescriptions as comparators, not as
   substitutes for those graphs.
2. **Finite occupied kinetic/current matching.** Construct the low-momentum
   component two-point/current vertices about the actual supersymmetry-
   broken background, including gauge/Goldstone mixing and light sectors.
   Compute the angular coefficient and any same-order higher-current terms.
   A small-F Kähler approximation was not established. The mass spectrum
   alone supplies neither all vertices nor the required derivative action.
   Then combine that action with U2 and rerun the native response. The
   existing positive radial tree gap does not replace this calculation.
3. **State and long-time dynamics.** For the phase route, derive/limit
   anomalous-charge evolution and select a state without fitting the
   pressure endpoint. For the massive-mode window, derive a physical
   gauge/IR occupation and collision/decay lifetime, rather than impose a
   conserved particle number. Production/cosmological halo work remains
   deferred until these material inputs are actually supplied.

These continuations are untried larger matching constructions, not exhausted
routes or proof of impossibility. The first two require the missing
gauge-consistent finite vertex/derivative calculation; another run of the
current RG-only interface does not address that step. Current evidence
does not establish a full physical no-go, a viable cold sector, gravity
completion, selected abundance or numerical kappa.

## Resume conditions and controls

Use the immutable TP01 spectrum and TP02 coefficient/pressure records.
For a new matching term, state its background, gauge, subtraction scale,
field chart, perturbative order, occupied-state assumptions and which
existing terms it replaces or adds. Verify CS and Legendre consistency,
positive admissible branches and independent derivative convergence before
interpreting a new root. Derive an actual finite remainder bound if making
a finite-coupling robustness claim. Do not treat residual scale variation
as that bound.

All TP02 deliverables are local. No commits, pushes, external jobs or queued
background work were started. Other work may advance HEAD; compare exact
hashes and preserve distinct source versions rather than refreshing pins.
