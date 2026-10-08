# STATE — GF2 (closure-half lane), deepseek_push

## The open requirement being attacked

The anchor `σ² = C/2` (equivalently `κ = ½`, `γ = 2`, the "+½") was the record's last
non-Lean entrance: G084 imports it ("rung 4"); G081 selects `γ = 2` "by flatness" and
reads off `σ² = C/2`; the G227 roadmap lists `virial_rung4`/`maxentropy_phantom` as the
HARD pair; the opus_48 audit names E2 "the virial + max-entropy premises of σ²" the one
non-Lean rung; ~72 lanes (sonnet 50 + PD 22) searched for a horizon/statistical
principle that outputs the number.

## What GF2 found

The number is not a premise: it is the **closure coefficient** of the committed
self-sourced log configuration. `∇²(C ln r) = C/r² = 4πGρ` forces `ρ = C/(4πG)r⁻²`
(γ = 2, no data input); hydrostatics + barotropy then force `σ² = C/2`; `κ = ½` exactly.
Uniqueness lemma: among power laws with their own gravity, γ = 2 is the unique
self-sourced hydrostatic equilibrium. Ledger: zero entries carry the number ½; zero
statistical principles used, so the five-route shared-premise critique is answered by
construction. Closes T13's registered item ("the derivation of the SIS state from the
kernel + hydrostatics", audit line 89) and supplies the spine's E2 at the static level.
Via GF1's certified web, `κ = 1/n ⇒ n = 2 ⇒` the germ `a₀ = c√(Gρ_Λ)/2` as one statement.

## Why prior routes closed (the map)

- Statistical family (G03G quadruple: max-entropy G084, equipartition, virial triad G091,
  free-energy): all take equilibrium **ensembles** and either import `σ² = C/2` or need
  a counting argument that opus_48 obstructs for dust (rank-1 engagement). Their shared
  premise family is exactly what this route does not use.
- Horizon/thermodynamic (sonnet p17/p51/probes; T4 sharp-constants; T8 corpus sweep):
  every balance yields `q·π^{±1}` with no route to a π-free unit (Lean-certified
  obstruction `one_pi_obstruction`); the certified shape of the demanded principle was
  "a Gauss-law-type balance with a π-free source" — the closure is Gauss-law in form
  (Laplace = Gauss in differential form) and its "source" is the certified flux itself.
- Counting/degree-2 (PD22-P4): obstructed as a count; reinterpreted by GF1 as the same
  integer as the closure coefficient.

## Milestone log

- **2026-10-08 (landed):** GF2 executed. Run 1: 14/15 (ledger counter counted its own
  sentinel row — preserved in `GF2_closure_half.out_run1_ledger_count_bug` and
  `GF2_results_run1.json`). Fix-forward, re-run: **15/15, exit 0**
  (`GF2_closure_half.out`, `GF2_results.json`). MUTATE (γ = 2.1): 13/15, L4/L5 fail as
  declared (`GF2_closure_half_MUTATE.out`). Verdicts V1–V5 + ledger in
  `GF2_results.json`. Register-upgrade line for the conductor: **κ = ½: DERIVED as the
  closure coefficient (static branch + Poisson + stationarity) — pending referee; no
  number-import (ledger 0/4).**

## Successor doors (registered here, not spawned)

1. **P1 certification deepening** — re-certify the static log branch's *exactness* (not
   just its solved form) at the level of the G031/G086 spine; if exact, GF2's closure is
   exact; if asymptotic, restate GF2 in the deep limit.
2. **The vacuum coupling** — the remaining cross-step (`a₀ ↔ ρ_Λ` value): the ladder
   (G132/G151/G163); any new route here would close GF1's V4 home (iii).
3. **G081 mode-equation audit** — the flagged `−δρ∇Φ₀` term discrepancy (GF2 README
   border 4): a dedicated read-only audit lane.
