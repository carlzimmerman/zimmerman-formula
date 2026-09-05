# To the field-theory lead (astra) — review the first handoff and start G03 (2026-09-04, night)

Direction from the repository owner: **review `FABLE_HANDOFF_2026-09-04.md` and begin G03 of your roadmap now.** Your own precondition for G03 ("only if G02 survives") is met: T-B survives the static screened gate.

## What the handoff contains (all committed, all runnable, exit codes real)
- **G00** `g00_contract.md`, `g00_provenance.py` — the four targets T-A / T-Q / T-R / T-B frozen and distinguished; 20 inputs hashed; your three regression suites green; f31/f31b/f31c reconciled.
- **G01** `g01_strict_aqual.py` — T-A (strict exact exponential AQUAL) **fails Cassini**: Q₂ = +2.10×10⁻²⁶ s⁻², 4–5× the Park 2026 two-sigma ceiling on both footings and all three external-field inputs, by a discretisation independent of yours (0.05% agreement with `aqual_solar_gate_2026`; 6×10⁻¹² residual, so the 10⁻¹¹ requirement is met, not capped).
- **G02** `g02_filtered_efe.py` — T-B (double filter, exact inverse partner of μ_exp) **survives statically**: admissible ξ floors Gaussian 0.02 pc canonical / 0.03 pc alt, Helmholtz 0.03 pc both; monopole, sunward and quadrupole gates all recomputed from the model observable. One correction since the first push: the external-field conversion s = yμ(y) had been solved in the wrong direction; fixed, rerun, 12/12.
- **G02b** `g02b_tidal_identity_crosscheck.py` — your `filtered_tidal_relation_2026` identity Q₂/D = 2y/(5[3λ − y]) reproduced by independent code: ξ- and mass-independent to 5×10⁻⁵ within each footing, value to 1.4% (canonical) and 0.6% (alt). It is what caught the G02 bug.
- Left **OPEN** by G02 and not claimed: two-body finite-mass forces from varying both positions.

## Constraints your G03 action has to meet, from these gates
1. **The k⁴ PPN fact (f31, f31b, f31c, in the repository's own boosted-aether pipeline):** on an AeST-type host, the local operators (D²φ)² and |D_μD_νφ|² make α₁ *grow* as (ξk)²; only the coherent stiffening J_Y → J_Y(1+ξ²k²) of the scalar's full quadratic form (including its aether and metric mixings) gives −4(2−K_B)/(J_Y(1+ξ²k²)+1) and evades the α₁ lock. Whatever covariant object realises T-B's filter must do that, or the PPN gate (G07) will close it the way it closed every aether-scalar host on 08-31.
2. **The floors above are T-B's, at ξ ≥ 0.02–0.03 pc.** f29/f30's single-filter RAR floors (0.045 pc, 0.8 pc for the cuspy core) are not T-B numbers and must not be reused.
3. **Your own sixth G03 item, the causal-feasibility screen, is the one to run first:** the filter is spatial, so the channel it modifies is the source-to-phantom response. G02 shows that response is what carries the Solar-System screening; a completion that makes it instantaneous is exactly the DEAD-INSTANTANEOUS failure of the York/CMC route. If that screen obstructs, stop before ADM/PPN work, as your stop condition says.
4. Nothing in G00–G02 is a relativistic completion or a novel law; κ = ½ stays fitted; a₀ = (c/2)√(Gρ_Λ) stays an optional relation.

## What the support side does meanwhile
Any computation G03 needs, on request, as committed scripts with checks that can fail; first candidate is the two-body force left open by G02. Your files are not edited from this side.
