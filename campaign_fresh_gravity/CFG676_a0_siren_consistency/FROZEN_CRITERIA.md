# CFG676 FROZEN CRITERIA: the a0–siren consistency relation (a two-messenger prediction)

Date: 2026-10-12. Block CFG670–679. Committed ALONE before any CFG676 code or number. κ = ½ FITTED; footings separate; cold
energy mass required; not "theory closed"; nothing says the data favour the framework.

## 0. The relation
The record's law ties a0 to dark energy: a0(z) = κ c √(G ρ_DE(z)) (owner rule, 10-06). Hence, with no free constant,
  **a0(z)/a0(0) = √(ρ_DE(z)/ρ_DE,0) = exp[(3/2) ∫₀^z (1 + w(z′)) dz′/(1 + z′)]**,
CPL w = w0 + wa z/(1+z): ρ_DE(z)/ρ_DE,0 = (1+z)^{3(1+w0+wa)} exp(−3 wa z/(1+z)).
Standard sirens measure the expansion history from gravitational waves alone (no distance ladder, no EM calibration); galaxy
dynamics at the same z measure a0(z). The framework says the two must agree through this relation. The record's rival law
a0 ∝ H(z) and the flat law a0 = const are the comparison curves (the record's standing a0(z) contest).

## 1. Computation
- DESI DR2 w0wa posteriors (BAO+CMB with each SN sample), **read from the DESI DR2 paper text** (arXiv 2503.14738) before use;
  if not verifiable, labelled recalled and given no weight.
- Table: Δlog10 a0(z) at z = 0.5, 1, 2, 3 for each combination, plus the a0 ∝ H(z) rival (with the same w0wa) and flat (= 0).
- Required precision: the siren (w0, wa) uncertainty (uncorrelated, equal fractional) at which the predicted Δlog10 a0 at z = 1
  and z = 2 is a 2σ departure from flat. Reported, no verdict.
- Context only: the record's measured a0(z) constraints (CFG213–229 high-z calibration-limited; CFG258/301 MIGHTEE local) are
  cited, not re-scored.

## 2. Output
Sealed `cfg676_predictions.json` (sha256 committed). This is a prediction + requirement lane: no data verdict. MUTATE
(`CFG676_MUTATE=1`): w0 = −1, wa = 0 must give Δlog a0 = 0 at all z (exit 1 iff it bites).
