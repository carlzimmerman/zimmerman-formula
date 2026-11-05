# CQ4_unimodular_tie: TIE BY HAND (no gain over AX1)

κ = ½ FITTED; not theory closed. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. Not blind. No
particle, no cold sector, and nothing here reinstates the retired cold sector. Nothing here says the data favour the
framework. Literature is from memory and PROVISIONAL; there was no web search and nothing was downloaded. The script runs
in about 1 s on one thread.

**Question.** Gate G5 (AX1): does a₀ = κ c √(Gρ_Λ) come out of an action if the unimodular multiplier Λ, a constant of
integration, also sets the MOND sector's kinetic scale?

**Answer.** The tie can be written healthily, but the action does not fix it.

The action is v3s with its constant Λ promoted to the Henneaux–Teitelboim multiplier: add 2Λ∂_μB^μ and keep
J(Y; Λ) = Λ − 2α²Λ[u − ln(1+u)]. B^μ's equation gives ∂_μΛ = 0 exactly, with no feedback from galaxies (k04's flux tie
had feedback). On shell the theory is v3s with a₀ = α c² √Λ, and

    κ² = 8π α² (1 − ρ_v/ρ_Λ,obs).

Three things go wrong:

- **G5b FAIL.** α is a free normalisation, and promoting it to a field kills the MOND sector.
- **G5c FAIL.** a₀ is tied to the multiplier, not to the gravitating vacuum density.
- **C1 FAIL.** Any matter vacuum energy ρ_v shifts κ. Holding κ within ±0.099 dex needs −0.58 ≤ ρ_v/ρ_Λ ≤ 0.37. The
  electron's one-loop term alone is 2.6e31 (canonical) and 1.8e31 (alt) [PROVISIONAL formula]. The cosmological-constant
  problem moves into a₀.

## Gates

| gate | result | why |
|---|---|---|
| S scale relation | PASS | the parent's simple-μ law with a₀ = αc²√Λ; κ² = 8πα²Λ/Λ_obs; α² = 1/(32π), ρ_v = 0 gives ½ |
| G5a form | PASS, no gain | the only acceleration from G, c, Λ is (number)·c²√Λ; the record already lists the form as forced |
| G5b number | **FAIL** | α free; ∂J/∂α = −2αΛh(u) = 0 only at u = 0 |
| G5c observed vacuum | **FAIL** | ∂κ²/∂Λ_v = −8πα²/Λ_obs ≠ 0 |
| C1 renormalisation | **FAIL** | the tie breaks the unimodular shift symmetry Λ → Λ + δ, ρ_v → ρ_v − δ; window vs ~1e31 |
| C2 time dependence | reported | w = −1 exactly for the tied vacuum; a₀(z)/a₀(0) = 1 at every z, so a₀ cannot track an evolving ρ_DE; set against CFG689's "flat within about 1σ, mild decline preferred", not graded |
| H1 no ghost | PASS | (Λ, B) has a zero velocity Hessian, a first-order pair and a gauge symmetry, with no local mode; the khronon's health is inherited (V3W W4, V3X W4c), not re-run |
| H2 no fifth force | PASS | δΛ = 0 locally on shell |
| H3 c_T = c | PASS | the added terms are metric-free; the tensor sector is v3s's |

Known answers K0 (Henneaux–Teitelboim alone) and K1 (v3s's law, κ = ½) pass. In the MUTATE, tying to k04's flux shows
feedback (dq/dY = +0.030 at u = 1), and the multiplier tie shows none. Every sympy identity simplifies to 0. A rerun gives
byte-identical output.

**Remark, not a gain on G5.** Tying to the multiplier, the Legendre partner of k04's flux, removes k04's environmental a₀
(a₀_loc = a₀(1 − g_N/155a₀)) exactly. The coefficient stays free in both: Z/β² in k04, α here. Passing G5b would need KC1's
ξ = 1, or premise A. Passing G5c and C1 would need a₀ to couple to the summed √−g coefficient, which is not a field.

## Record check (before freezing)

k04 tied a₀ to the four-form flux. The volume-form study (sol61_push … volume_form §4) tied it to the unimodular volume,
and k02 ran the sequestering direction. KC1 and KF1 apply, and v3s's J already uses one constant with 32π by hand. None
tied a₀ to the multiplier itself, so this was not ALREADY ON RECORD. It nearly was: the outcome matches k04 F2's free
coefficient.

## Files and commits

- `FROZEN_CRITERIA.md`: 1118e49b50, committed and pushed alone, first.
- `derivation.md`: the derivation, with a check id on every equation.
- `cq4_unimodular_tie.py` and `cq4_unimodular_tie.out`: rc 0, sha256 of the output begins 13c8b745c1bbb0da.

Committed together after the criteria.
