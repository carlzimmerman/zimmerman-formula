# G180 — THE ONTOLOGY AMENDMENT

**Correct the record in place: the dark mass / dark sector is NOT the shift-Noether charge.**

**Filed 2026-09-16. Lane G180.** Builds on G154 (`G154_static_charge.py/.out/.json`, the Gauss-map
derivation, 18/18) and the wave-13 ledger entries in `WAVEBOARD.md`. **Deliverable: this file +
`G180_results.json` (committed and pushed). The old files are NOT silently edited — the amendment
document is the deliverable; the hits are recorded below with their per-hit DELTA rows.**

> **THE ONE-SENTENCE AMENDMENT:** on the static branch the shift-Noether current is `J^mu = 0`
> (hy4's DOOR 3 is exact — G154), so the statement **"the dark matter / dark sector IS the Noether
> charge"** is empty there; the dark mass is instead the **GAUSS-MAP charge of the sourced scalar
> field** (the surface integral of the field), with the closed form
> **M_ph(<r) = (1/4πG) ∮ g·dA = M_b r/r_M**, equivalently the **charge of the dust fluid** whose
> density is the phantom **ρ = √(G M_b a₀)/(4πG r²)**. This is a WORDING-level amendment: every
> downstream claim (the Lean certificates G028/G090/G03G, the empirical record) survives unchanged.

---

## 0. THE EXACT PHYSICS (what the wording becomes; per G154, hy4-correct)

On the **static branch** the shift-symmetric scalar field is `φ = φ(x)` with `φ̇ = 0`, so the
shift-Noether current is identically zero pointwise:

    J^0 = f′(K) ∂⁰φ = f′(K)·0 = 0         (canonical momentum π = f′(K)φ̇ = 0 too)
    Q   = ∫ J^0 d³x = 0                   (no Noether charge to integrate)
    ∂ᵢJⁱ = −∂₀J⁰ = 0                      (spatial current divergenceless: zero flux through
                                          every closed surface — no Gauss-map charge in the
                                          Noether current; G154 R1–R4, C1)

The dark mass is therefore **not** a Noether boundary term. It is the **Gauss-map charge of the
SOURCED field** — the surface integral of the total acceleration field `g` that satisfies the
sourced equation `div[f′(K) grad φ] = 4πG ρ_b` (H008/H011's sourced form), i.e. of
`ρ_DM = (1/4πG) div(g − g_b)` (G154 C2):

    M_ph(<r) = (1/4πG) ∮_{S(r)} g·dA = r·√(G M_b a₀)/G = M_b (r/r_M),   r_M = √(GM_b/a₀).

This is the framework's registered universal linear law (G03E V2; G154 C3; Lean G03G #2).
At `r = r_M`: `M_ph(<r_M) = M_b` exactly (the equipartition; G154 C2, Lean G03G #1 / G090 #4).
EFE-capped at `√(a₀/g_ext)`: capped share 0.660 M_b (canonical) / 0.725 (alt) (G154 C4).
Equivalently (D1–D2), the dust-fluid current `J^μ_fluid = n u^μ` carries the same number:
`J⁰_fluid = n(x) ≠ 0` at rest, `M_dark(<r) = ∫ m n d³x = M_ph(<r)` — the fluid charge and the
Gauss-map charge are the same mass carried two ways. The phantom density:

    ρ_DM(r) = √(G M_b a₀)/(4πG r²).

**What stays true and is NOT amended:** G028's Lean certificate (L217 V3) proves a conserved
comoving Noether charge `Q = a³ P_X φ̇` on the **homogeneous FRW family** (density `a⁻³`, carries
Ω_dm, w-window) — that is the cosmological / time-dependent branch, **silent on static halos**
(G154 G1–G2); it is not a static-halo charge. The vendor-legal and empirical record (Cassini null,
RAR as hydrostatics, lensing = GR × real mass, the equipartition/virial algebra) is untouched.

**THE AMENDED STATEMENT (replaces every hit below):**

> "The dark mass is the **Gauss-map charge of the sourced scalar field** / the charge of the dust
> fluid, whose density is the phantom **ρ = √(G M_b a₀)/(4πG r²)**; on the static branch the
> shift-Noether current is empty (J^μ = 0)."

---

## 1. THE GREP (V1) — every committed place the wording appears

Case-insensitive `Noether` grep over the six named files
(`GRAVITY_EVERYWHERE.md`, `THE_THEORY.md`, `THEORY_STATUS_2026-09-16.md`, `LAW_VERIFIED.md`,
`WAVEBOARD.md`, `PREDICTIONS.md` — all in `deepseek_push/`). **17 raw hits** in 5 files; classified
below as (A) substantive wording-to-correct, (B) borderline label, (C) already-correct /
diagnostic. `PREDICTIONS.md`: **0 hits** (its only "dark sector" mention, L35, is an unrelated
falsification note: "the dark sector is not the phantom").

| File | Raw hits | (A) assert "dark mass/sector = Noether charge" | (B) label | (C) correct/diagnostic |
|---|---|---|---|---|
| GRAVITY_EVERYWHERE.md | 6 | L14, L41, L104, L300(+L302), L398–399 | L31 | — |
| THE_THEORY.md | 2 | L33, L86 | — | — |
| THEORY_STATUS_2026-09-16.md | 1 | — | — | L78 (records the emptiness) |
| LAW_VERIFIED.md | 1 | L37–38 | — | — |
| WAVEBOARD.md | 7 | L723 (+L645 borderline) | — | L626/631/633/635/696 (already the G154 amendment) |
| PREDICTIONS.md | 0 | — | — | — |

Note: `WAVEBOARD.md` L625–636 already carries the G154 settlement instructing exactly this
amendment ("the STATUS wording must amend 'dark matter is the conserved Noether charge' ->
'Gauss-map charge of the sourced field / charge of the dust fluid' (G180 dispatched)") — this
document is the execution of that instruction.

---

## 2. THE DELTA ROWS (per hit: old → new, impact)

**File: GRAVITY_EVERYWHERE.md** (this file is G082's assembly — its §5 "ten lines" L394–405 are the
object G082 named; the ontology wording lives there and in §1.1/§3.2/§3.3)

**D1 · L14 (epigraph).**
- OLD: `…the scalar's vacuum value is the dark energy; its Noether charge is the dark matter.`
- NEW: `…its dark sector is the sourced field's Gauss-map charge (M_ph(<r) = M_b r/r_M; the shift-Noether current J^μ = 0 on the static branch).`
- IMPACT: none — the substance of the epigraph (one constant; the sector makes the RAR/flat
  curves/clusters) unchanged; only the carrier is renamed.

**D2 · L31 (action, `S_fluid` label `/ the Noether-charge dust`).**
- OLD: `+ S_fluid[J, φ, β, α]  [the Noether-charge dust]`
- NEW: `+ S_fluid[J, φ, β, α]  [the charge dust — carrier of the Gauss-map / fluid charge]`
- IMPACT: none — the fluid does carry a charge (J⁰_fluid = n), so the label is not wrong; renamed
  only to avoid conflation with the (empty) shift-Noether current.

**D3 · L41.**
- OLD: `**The cold sector is a Noether charge, not a species.**`
- NEW: `**The cold sector is a charge, not a species** — on the static branch the dark mass is the
  Gauss-map charge of the sourced field, M_ph(<r) = (1/4πG)∮g·dA = M_b r/r_M, carried also by the
  fluid current J⁰_fluid = n(x); the shift-Noether current J⁰ = f′φ̇ = 0 there.`
- IMPACT: none — the "not a species" (no particle to detect) point survives; the adjacent claim
  (one conservation law, no independent particle number, G028/G031) is about the FRW charge and is
  unchanged.

**D4 · L104.**
- OLD: `Its Noether charge (1.1) is the mass.`
- NEW: `Its dark mass is the Gauss-map charge of the sourced field (M_ph(<r) = M_b r/r_M), not the
  shift-Noether charge (empty on the static branch).`
- IMPACT: none — rest of §1.1 (the MOND-looking force is the gravity of the equilibrated charge
  dust; the scalar never pulls) unchanged.

**D5 · L300–302 (section heading + lead).**
- OLD heading: `### 3.2 Dark matter — the Noether charge, in two phases`
- OLD lead: `The cold sector is not a particle species; it is the shift-symmetry charge (G028),…`
- NEW heading: `### 3.2 Dark matter — the Gauss-map charge of the sourced field, in two phases`
- NEW lead: `The cold sector is not a particle species; it is the charge of the sourced field / the
  dust fluid (G028's certified charge is the comoving FRW one; the shift-Noether current is empty
  on the static branch), and it has two acceleration-selected states (H032 D1):`
- IMPACT: none — §3.2's two phases (phantom / free dust), the particle census G093, and the
  Tremaine–Gunn bounds are unchanged; the density `ρ = √(GM_b a₀)/(4πGr²)` already quoted at L305 is
  exactly the amended phantom density.

**D6 · L398–399 (ten-lines, G082's assembly).**
- OLD: `3. The scalar modifies no force anywhere; it generates a sector of Noether charge.` /
  `4. That charge is the dark matter — a field configuration, not a species.`
- NEW: `3. The scalar modifies no force anywhere; it sources a field whose Gauss-map charge is the
  dark sector (the shift-Noether current J^μ = 0 on the static branch).` /
  `4. That charge is the dark matter — a field configuration / the dust-fluid charge, not a
  species: M_ph(<r) = (1/4πG)∮g·dA = M_b r/r_M.`
- IMPACT: none — the ten-lines' points 4–10 (mass relations, RAR as EOS, lensing, EFE cap, dark
  energy, open list) are untouched.

**File: THE_THEORY.md**

**D7 · L33 (Lemma 3).**
- OLD: `The cold sector (the Noether charge of the shift symmetry, w = 0) in a baryonic well
  equilibrates at the virial temperature…`
- NEW: `The cold sector (the dark sector = the Gauss-map charge of the sourced field; the fluid
  dust, w = 0) in a baryonic well equilibrates at the virial temperature…`
- IMPACT: none — the lemma's content (`σ² = √(GM_b a₀)/2`, `c_deep = 1`) is the equilibrium, derived
  three ways; carrier rename only.

**D8 · L86.**
- OLD: `gravity of the equilibrated Noether-charge dust (lemmas 3-4).`
- NEW: `gravity of the equilibrated charge dust (the Gauss-map / fluid charge; lemmas 3-4).`
- IMPACT: none — the 16-lemma chain and its Lean spine (66 theorems, zero sorry) untouched.

**File: LAW_VERIFIED.md**

**D9 · L37–38.**
- OLD: `Gravity everywhere: GR + one shift-symmetric scalar whose Noether charge is the cold
  sector; in the deep isolated regime the sector is the maximum-entropy equilibrium at the
  DE-set temperature (sigma^2 = v_flat^2/2), giving the r^-2 profile, the equipartition,…`
- NEW: `Gravity everywhere: GR + one shift-symmetric scalar whose sourced field carries the
  Gauss-map charge of the dark sector (M_ph(<r) = M_b r/r_M; the shift-Noether current is empty
  on the static branch); in the deep isolated regime the sector is the maximum-entropy equilibrium
  at the DE-set temperature (sigma^2 = v_flat^2/2), giving the r^-2 profile, the equipartition,…`
- IMPACT: none — LAW_VERIFIED is the "what survives every audit" statement; the vetted claims
  (r⁻², equipartition, RAR hydrostatics, universal surface density, Cassini null, lensing =
  GR×real mass) are all unchanged.

**File: WAVEBOARD.md**

**D10 · L723 (the standing-summary line; the board's live master sentence).**
- OLD: `GR + one shift-symmetric scalar; its Noether charge is the dark sector (the free dust:
  cold, m > 3.3 keV;…); its vacuum is the dark energy;…`
- NEW: `GR + one shift-symmetric scalar; the Gauss-map charge of its sourced field is the dark
  sector (M_ph(<r) = M_b r/r_M; the shift-Noether current is empty on the static branch) (the free
  dust: cold, m > 3.3 keV;…); its vacuum is the dark energy;…`
- IMPACT: none — all of the line's downstream physics (equipartition regime M_dark(<r) = M_b r/r_M,
  r⁻², RAR, Cassini null, lensing, EFE cap, DR4 face) unchanged.

**File: THEORY_STATUS_2026-09-16.md**

**D11 · L78 (diagnostic — NO CHANGE REQUIRED).**
- OLD (unchanged): `…VANISHES on the static branch: the dark mass as Noether charge EMPTY there,
  G154 attack, dispatched…`
- NEW: none — this line already records the emptiness and the G154 resolution; it is part of the
  correction's own record, not a wrong assertion. Listed for completeness.

**WAVEBOARD.md L626/631/633/635/696 & L645 (already-amended / borderline).**
- L626/631/633/696 are the G154 settlement text (the shift-Noether charge is empty; the dark mass
  is assigned via the Gauss-map charge) — correct as committed.
- L635 quotes the old wording inside the amendment instruction — correct as committed.
- L645 `phantom = Noether dust at the Zimmerman temperature` (G155's reading): **borderline** —
  "Noether dust" is a legacy label for the equilibrated charge dust; per this amendment prefer
  "charge dust (Gauss-map/fluid charge)" but the sentence is already a description of G031's
  equilibrium/EOS reading, so a rename is optional, not required.

**File: PREDICTIONS.md** — **no hits** (V1: 0 occurrences of the Noether-charge ontology wording).

---

## 3. IMPACT — does any downstream claim break? **No. The amendment is WORDING-level.**

| Claim | Verdict | Reason |
|---|---|---|
| **Lean G028** (certifies the FRW comoving charge, `Q = a³ P_X φ̇`, homogeneous family) | **UNCHANGED** | G028/L217 is the cosmological time-dependent branch (density `a⁻³`, carries Ω_dm); it is *silent* on static halos (G154 G1–G2) — the amendment does not touch it either way. |
| **Lean G090** (certifies the vflat / equipartition algebra: `M_ph(<r) = M_b r/r_M` ⇔ the RAR) | **UNCHANGED** | The certificate is pure algebra on the linear law; under the amendment that law *becomes* the Gauss-map charge. The algebra is identical; only the ontology label of `M_ph` changes. |
| **Lean G03G** (triad + equipartition: `M_ph(<r_M) = M_b`, flatness selection, virial half) | **UNCHANGED** | Same — `sqrt_pair` / `equipartition_exact` / `vc_flat_exact` / `sigma_virial_half` are algebra on `M_ph = M_b r/r_M`; no Noether-current premise anywhere. |
| **The empirical record** (Cassini null, RAR as hydrostatics, lensing = GR × real mass, BTFR, EFE cap, DR4 face, cluster prize) | **UNCHANGED** | Every measurement tests the *mass relations / equilibrium*, which are the same numbers under either label. The amendment changes the name of the carrier, not a number. |
| **The "no species" claim** (no particle to detect) | **UNCHANGED** | The field-configuration / dust-fluid reading still predicts the 40-year direct-detection nulls. |

---

## 4. VERDICTS

- **V1 — the grep is complete.** Case-insensitive `Noether` scan of the six named files: 17 raw
  hits in 5 files; `PREDICTIONS.md` clean (0). 10 substantive wording-to-correct hits
  (GRAVITY_EVERYWHERE L14/L41/L104/L300–302/L398–399, THE_THEORY L33/L86, LAW_VERIFIED L37–38,
  WAVEBOARD L723, + WAVEBOARD L645 borderline); 1 already-correct diagnostic (THEORY_STATUS L78);
  6 already-amended (WAVEBOARD L626/631/633/635/696). No committed occurrence of the ontology
  wording is missed.

- **V2 — the amendment document is complete.** This file + `G180_results.json`; the exact physics
  (§0), the grep (§1), the per-hit DELTA rows (old → new → impact, §2), and the downstream-impact
  audit of the Lean certificates G028/G090/G03G and the empirical record (§3) are all present.

- **V3 — honest statement.** The ontology is **corrected in wording, assigned in substance**: the
  dark mass is not the shift-Noether charge (J^μ = 0 on the static branch — hy4/G154 were right),
  it is the **Gauss-map charge of the sourced scalar field** with the closed form
  **M_ph(<r) = (1/4πG) ∮ g·dA = M_b r/r_M**, equivalently the charge of the dust fluid whose
  density is the phantom **ρ = √(G M_b a₀)/(4πG r²)**. hy4's DOOR-3 emptiness result is correct
  and preserved; the physics survives; the surplus is a word.
