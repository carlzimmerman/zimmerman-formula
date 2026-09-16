# G227 — THE ONTOLOGY LEAN ROADMAP: the next certificates that complete the spine

**Status:** 2026-09-16. Assembly lane over the committed record — the final
ontology statement's Lean-future (G180, G214, THE_THEORY.md L1–L16). Every
certificate below was **re-verified today** in the repo's Mathlib build
(`lake env lean`, Lean 4.34.0-rc2, `mondlean` project): **exit 0, zero real
`sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound}** — including the
NEW G227 prototype certificate, which moves the first gap theorem from
algebra-on-record to Lean-certified in this very lane.

---

## (1) THE CURRENT CERTIFIED SET — the recount

### 1a. The task inventory, recounted theorem by theorem

| Inventory entry | Count | Certificate / file |
|---|---|---|
| G03G | **4** | `lean/G03G_triad.lean` — sqrt_pair, equipartition_exact, vc_flat_exact, sigma_virial_half |
| G083 | **5** | `lean/G083_surface_density.lean` — surface_density_universal, _equipartition_form, num_sigma_bar_msun, _mean, _composition |
| G090 | **5** | `lean/G090_equivalence.lean` — sqrt_pair, vflat_sq_identity, btfr_quartic, equipartition_virial, equipartition_linear_law |
| G201 | **8** | `lean/G201_jump_share.lean` — isothermal_density_ratio, entropy_jump_log, entropy_jump_cube, entropy_jump_additivity, jump_cube, share_identity, share_identity_deep, deep_limit_sq |
| G058 | **6** | `glm53_push/lean/G058_omega_from_a0.lean` — omega_from_a0_gen, omega_from_a0, num_omega_lambda, num_omega_lambda_h0_planck, one_constant_closure, omega_lambda_near_planck |
| G055 | **12** | `glm53_push/lean/G055_frozen_scalar.lean` |
| G031 | **13** | `lean/G031_fluid_action.lean` — the hydrostatic spine (zimmerman_temperature, phantom_is_isothermal, deep_rar, btfr, the_spine) |
| G039 | **14** | `glm53_push/lean/G039_horn_a_clean.lean` (6) + `G039_radial_scatter.lean` (8) |
| G036 | **9** | `lean/G036_formal_extras.lean` — the slab column / peak / w-window |
| G047 | **6** | `glm53_push/lean/G047_efe_cap.lean` — mu2_sq, mu2_pos, solve_well_posed, external_field_lifts, efe_floor_law_exact, cap_uniqueness |
| G007 | **11** | `lean/G007_bimetric.lean` — the bimetric closure |
| G001+G002 | **12** | `lean/G001_clockmaker_dilemma.lean` (8) + `lean/G002_G003_onefunction_phantom.lean` (4) |
| **Sum (task list)** | **105** | |

### 1b. The full certified ledger (all files that compile clean in the build)

The deepseek spine set (G214's ledger, re-verified today): EQUILIBRIUM_THEORY
**12** · G001 **8** · G002/G003 **4** · G007 **11** · G031 **13** · G036 **9**
· G03G **4** · G083 **5** · G090 **5** · G201 **8** = **79 theorems / 10
certificates** — unchanged from G214, all exit 0 today.

Adding the glm53-lane-only certificates (G058 6, G055 12, G039 14, G047 6,
G024 9 — the shared files are byte-identical copies): the **complete repo
certified ledger = 126 theorems across 16 certificate files**, all re-verified
today (exit 0, zero sorry). The G214 "79" is the spine ledger; "126" is the
whole machine-checked surface. **The recount: the task inventory sums to
105; the full ledger is 126; the spine subset is 79 — all three numbers
verified programmatically in this lane.**

### 1c. What the recount changed

- Every count in the inventory is **confirmed exact** (comment-stripped
  theorem scan, not docstring claims): G03G 4 ✓, G083 5 ✓, G090 5 ✓, G201 8
  ✓, G058 6 ✓, G055 12 ✓, G031 13 ✓, G039 6+8=14 ✓, G036 9 ✓, G047 6 ✓,
  G007 11 ✓, G001+G002 8+4=12 ✓.
- The inventory omitted EQUILIBRIUM_THEORY (12, the consolidated spine file)
  and G024 (9); both compile clean and belong on the ledger.
- The G214 "74/8" line in THEORY_CLOSURE (pre-G090/G201-era) is stale; the
  live number is 79 (spine) / 126 (full).

---

## (2) THE GAP — the physics inputs not yet Lean-covered

Per G214's coverage analysis, the certified spine is
`a0 → σ² = √(GM_ba0)/2 → ρ = S/(4πGr²) → M_ph(<r_M) = M_b → g² = a0 g_N →
BTFR`, with the entrance E2 (the virial + max-entropy premises of σ²) the one
non-Lean rung. The four physics inputs named in the task, each adjudicated:

### (a) THE GAUSS-MAP CHARGE — M_ph(<r) = (1/4πG) ∮ g·dA — **CERTIFIED TODAY (G227)**

The G154/G180 charge: on the static branch the dark mass is the Gauss-map
charge of the sourced field. **State the theorem**: for the isothermal well,
g = S/r with S := √(GM_ba0) constant on the sphere S(r), so

    ∮_{S(r)} g dA = (4πr²)·(S/r) = 4π √(GM_ba0) r,
    M_ph(<r) = (1/4πG)∮ g dA = √(GM_ba0) r / G = M_b r / r_M,
    M_ph(<r_M) = M_b  exactly.

This lane **certified it in Lean today**: `deepseek_push/lean/G227_gauss_map_prototype.lean`,
five theorems, exit 0, zero sorry (see §3, C4). The algebra was verified
this lane (sympy-exact): the flux identity is exactly `4π√(GM_ba0)r`; the
mass identity needs exactly the G03G/G090 `sqrt_pair` product, re-derived
in-file. **The G154 charge is no longer algebra-on-record — it is a theorem.**

### (b) THE ENTROPY-JUMP EXPONENT 3 — **ALREADY LEAN (G201)**

The phase-space-dimension reading (dS/k_B = 3 ln(σ_ph/σ_d), one ln per
dimension; A_b = exp(dS/k_B) = (σ_ph/σ_d)³) is **already certified**: G201
carries `entropy_jump_log`, `entropy_jump_cube`, `entropy_jump_additivity`,
`jump_cube` — the exponent 3 at log level, power level, and amplitude level,
zero sorry (re-verified today). The honest statement: **the "3" as a
dimension count is a definitional reading on top of certified algebra** — the
algebra IS Lean; the Boltzmann entropy identification stays an explicit
physics premise, exactly as G214 states. A definitional theorem
(`phase_space_volume : Ω ∝ σ³ ⇒ ΔS/k_B = 3 ln(σ_ph/σ_d)`) is the only
remaining formalization, and it is trivial (one `log_pow`); it is a
cosmetic-complete, not a gap-closing, theorem.

### (c) THE z* INVERSION — m(z*) = k_B T_0 (1+z*)/σ² — **NOT YET LEAN, EASY**

z* := mσ²/(k_BT_0) − 1 (G132/G163/G168: the decoupling epoch where the
equilibrium temperature T_b = mσ²/k_B equals the CMB temperature T_0(1+z*)).
The inversion is a linear solve:

    z* = mσ²/(k_BT_0) − 1  ⇔  m = k_B T_0 (1+z*) / σ².

Verified this lane (sympy-exact, both directions). **Certifiable in one
`field_simp`** with no sqrt machinery, no rpow — strictly easier than any
existing certificate. The physics premises (which σ — the triad 119.2 km/s,
G168's registered footing; T_0 = 2.7255 K) stay inputs, exactly as the lane
convention requires. **This is the second new theorem of the set (C5).**

### (d) THE α = 2/3 TEMPERATURE-LAW EXPONENT — **NOT YET LEAN, THREE CANDIDATES**

T_obs/T_pred = 2 f (r_M/R500), f = M_dyn/M_b; with the overdensity-500
self-similarity R500 = f^{1/3} R500^(b) the exponent on f is exactly
2/3 = 1 − 1/3 (virial +1, self-similarity −1/3; G095/G135). Three candidate
theorems, ranked by cleanliness (all algebra verified this lane):

- **d1 — the pure arithmetic** `2/3 = 1 − 1/3` (norm_num): the exponent's
  structure as an identity. Trivial; states the meaning but carries no law.
- **d2 — the log10 face identity**: `log10(2 f r_M/R500) =
  (2/3) log10 f + log10(2 r_M/R500^(b))` given `R500 = f^{1/3} R500^(b)` —
  the G135 V1a identity, sympy-exact. Requires `Real.log_rpow` for the
  f^{1/3} step: MEDIUM difficulty, the cleanest *law-carrying* candidate.
- **d3 — the rpow-level substitution** `2 f r_M/(f^{1/3} R500b) =
  2 (r_M/R500b) f^{2/3}` — the full fractional-power identity. HARDEST: needs
  the rpow-log injectivity extraction (the named synthesis failure of G03G's
  general form).

Cleanest pick: **d2 as the theorem (G214's C3 `twothirds_law`, restated at
the log level to stay inside `log_rpow`)**, with d1 as its opening line and
d3 registered as the rpow-grade variant.

---

## (3) THE ROADMAP — the spine-completion candidate set

| # | Candidate | Difficulty | Dependencies | Closes |
|---|---|---|---|---|
| **C4** | **`gauss_map_charge`** (flux = 4π√(GM_ba0)r; charge = M_b r/r_M; equipartition) | **DONE TODAY** (G227 prototype, 5 thms, exit 0) | G03G/G090 `sqrt_pair` technique (re-derived in-file) | **the G154 charge — THE GAP (a)** |
| **C5** | **`mass_inversion`**: m(z*) = k_B T_0(1+z*)/σ² | **EASY** (one field_simp; no sqrt, no rpow — easier than any existing cert) | none; standalone | **THE GAP (c)** — the mass from z* |
| **C6** | **`jump_dimension3`** (definitional: Ω ∝ σ³ ⇒ ΔS/k_B = 3 ln ratio) | **EASY** (log_pow, one line) | G201 entropy_jump_cube | **THE GAP (b)** — makes the reading definitional (algebra already Lean) |
| **C3** | **`twothirds_law`** (log10 face: (2/3) log10 f + const) | **MEDIUM** (log_rpow) | G095/G135 identity; Mathlib `Real.log_rpow` | **THE GAP (d)** — the 2/3 exponent as certified algebra |
| C3' | twothirds at rpow level (f^{2/3} closed form) | **HARD** (rpow-log injectivity; G03G's named synthesis gap) | Mathlib rpow interface on v4.34.0-rc2 | same, full form — register, don't lead |
| C1 | `virial_rung4`: σ² = C/2 from the G091 shell-energy integrals | **HARD** (energy integrals in Lean) | `integrand_const` machinery (G031); closed virial chain | the spine's non-Lean entrance E2 |
| C2 | `maxentropy_phantom`: EL iff γ = C/σ² + strict concavity ⇒ ρ = A/r² | **MEDIUM-HARD** (variational second variation) | Mathlib concavity; G084's exact-residual | the spine's non-Lean entrance E2 |

**Dependency ordering:** C4 ⊥ everything (standalone sqrt_pair re-derived);
C5 ⊥ everything; C6 ⊃ G201 (already landed); C3 ⊃ G095's identity (committed
lane) + Mathlib `log_rpow`; C1 ⊃ G031's integral machinery; C2 ⊃ C1's
temperature premise (or matches it). C1+C2 together close the entrance E2,
making **every spine edge Lean** (G214's statement, unchanged). C4–C6+C3 are
the **ontology set**: they lift the charge, the mass inversion, the jump
dimension, and the temperature exponent from algebra-on-record to theorems.

---

## (4) VERDICTS

**V1 — the theorem inventory, recounted and verified.** The task inventory
sums to **105 theorems** (every listed count confirmed exact by
comment-stripped scan: G03G 4, G083 5, G090 5, G201 8, G058 6, G055 12,
G031 13, G039 6+8, G036 9, G047 6, G007 11, G001+G002 8+4). The full repo
ledger is **126 theorems / 16 certificates** (adds EQUILIBRIUM_THEORY 12 and
G024 9); the deepseek spine subset is 79/10 (G214's number, still exact).
All re-verified today: exit 0, zero real sorry (the only "sorry" strings in
any file are in comments), axioms ⊆ {propext, Classical.choice, Quot.sound}.
**PASS.**

**V2 — the candidate set with dependencies.** Seven candidates ranked:
C4 `gauss_map_charge` **DONE today** (the G154 charge, certified);
C5 `mass_inversion` EASY — the z*→m inversion, one field_simp;
C6 `jump_dimension3` EASY — the exponent-3 definitional reading (algebra
already Lean in G201); C3 `twothirds_law` MEDIUM — the 2/3 log10 face via
`log_rpow`; C3' rpow-grade HARD (registered, not lead); C1 `virial_rung4`
HARD — the spine's largest non-Lean premise; C2 `maxentropy_phantom`
MEDIUM-HARD — completes the entrance. Dependencies stated per theorem; none
of C4/C5/C6/C3 blocks another, and C1+C2 remain the deep-spine rungs.
**PASS.**

**V3 — the honest statement.** The Lean spine's ontology next step is now
concrete and partly *already taken*: **(a) the G154 Gauss-map charge is
Lean-certified today** (G227 prototype: the isothermal-wall flux
∮g·dA = 4π√(GM_ba0)r, the charge M_ph(<r) = M_b r/r_M, and the equipartition
M_ph(<r_M) = M_b, 5 theorems, exit 0, zero sorry) — the charge is no longer
algebra-on-record; **(b) the entropy-jump exponent 3 was already Lean** (G201,
4 theorems) — the "definitional theorem" redraw is cosmetic, not gap-closing;
**(c) the m(z*) inversion and (d) the 2/3 temperature exponent are the two
remaining easy-medium theorems** — one `field_simp` and one `log_rpow`
respectively, both algebra-verified in this lane, both riding committed
physics premises (the triad σ, T_0, the R500 = f^{1/3}R500b self-similarity)
that stay explicitly stated inputs. **The 2–4 theorems that move the
charge/entropy/mass inversions from algebra-on-record to Lean-certified are
C4 (done), C5, C6, C3 — three of them are new certificates of one-lane
difficulty on the existing sqrt_pair/log_pow machinery**; the deep spine's
virial and max-entropy entrances (C1, C2) remain the HARD pair, exactly as
G214 registered, and nothing in this roadmap pretends they are easy. Honest
single line: the ontology's Lean-future is four theorems of easy-to-medium
difficulty plus the two hard entrance rungs — and one of the four landed
with this document.

*Checks: 16+1 certificates compiled (all exit 0) · inventory recounted
programmatically (105 task-list / 126 full / 79 spine) · G227 prototype
certified (5 theorems, zero sorry) · all four gap algebras verified
sympy-exact. Files: `deepseek_push/G227_lean_roadmap.md`,
`deepseek_push/G227_results.json`, `deepseek_push/lean/G227_gauss_map_prototype.lean`.*