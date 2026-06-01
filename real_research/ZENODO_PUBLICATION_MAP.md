# Your published papers, mapped honestly — what to keep, what to retract

**2026-06-01.** Carl pointed me to the actual pre-publication manuscripts (`ai_slop/papers/`,
`ai_slop/zenodo/`, `ai_slop/submissions/`). This maps what is **published under your name on
Zenodo** against everything verified this session, claim by claim. It **extends your own
`ERRATA_DIMENSIONAL_STRUCTURE.md`** (May 2026), which was right to retract the M-theory
numerology but **stopped short** — it still endorses α⁻¹=4Z²+3 and the η(T³/Z₂) "derivation" as
correct, and those are the parts that do not survive. This is the complete correction.

All 80 confirmation scripts (`real_research/*.py` + `reviews/*.py`, the non-swarm suite) **pass**
as of this date — so every "KEEP" below is reproducible, and every "RETRACT" is backed by a
runnable check.

---

## The published record

- **Zenodo v5.0** — *"The Zimmerman Framework: Unified Physics from Z² and Open-Source
  Computational Therapeutics"* (concept DOI lineage `10.5281/zenodo.19244651`). Bundles **three
  layers in one upload**: MOND a₀=cH/Z (real) + α/genetic-code/"consciousness, time" (numerology)
  + therapeutics (unvalidated).
- **`Z2_UNIFIED_ACTION` series** (v5.7.9 → v8.0.0, `Z2_Framework_Zenodo/`) — the E₆-orbifold
  "unified action / TOE."
- **`gravity_research_foundation_2026`** submission.

The bundling is the core problem: a real result and dead numerology share one DOI, so the
numerology discredits the real part by association. The fix is separation, not deletion.

---

## Claim-by-claim map

| claim (as published) | verdict | basis (runnable) |
|---|---|---|
| **a₀ = cH/Z, Z=2√(8π/3)=5.789** | **KEEP** — novel *framing* of Milgrom's a₀≈cH₀; Z is a posited coefficient | `schwarzschild_friedmann_core.py`, `NOVELTY.md` |
| **a₀(z)=a₀(0)E(z) evolves** | **KEEP — the strongest result**; now data-favored, constant a₀ excluded **5σ** | `a0_powerlaw_confrontation.py`, `rar_evolution_test.py` |
| a₀↔Λ floor, BTFR, RAR, the over-constrained web (+4) | **KEEP** | `REAL_WEB.py`, `mond_first_principles.py` |
| **Z² = 32π/3 "derived from η(T³/Z₂)=8×(4π/3)"** | **RETRACT the derivation** (keep Z as a *posit*) | category error: η is a spectral-asymmetry invariant, 4π/3 is the unit-3-ball *volume* — unrelated. `reviews/eta_local_bruning_seeley.py`, `twisted_heat_trace_check.py` |
| **α⁻¹ = 4Z² + 3** | **RETRACT** — numerology, ~0 bits | the *same* family fits Dunbar's number (4Z²+16) and tropopause T (6Z²+16) to <0.03%; `reviews/false_discovery_rate.py`, `SALVAGE_LEDGER.md` |
| sin²θ_W, Koide, CKM, PMNS, 9 fermion masses, GAUGE=12 | **RETRACT** — same integer-fit genre | `is_Z_special.py`, `false_discovery_rate.py` |
| genetic code (4=Bekenstein, 20=gauge+cube) | **RETRACT** — domain-jump on integers | `SALVAGE_LEDGER.md` §2 logic |
| "physics, mathematics, biology, **consciousness, and time** from first principles" | **RETRACT** — no derivable content | — |
| M-theory 11D / M2+M5 branes | **already retracted by you** (correct) | your `ERRATA` Corrections 1–4 |
| T³/Z₂ 20.6 Gpc cosmic topology | **RETRACT** — excluded / undetectable | `reviews/matched_circle_*` |
| cosmic dipole R=19/6 | **RETRACT** — fitted ratio; observed R fell to ~1.5–2 | `WEB_SYNTHESIS.md` §7 |
| therapeutics (c-Myc, NaV1.7, PETase, CFTR, D2R, AMPs; Kd, "cures") | **PRIOR-ART ONLY, no efficacy** | your own `LEGITIMATE_FINDINGS.md` concedes this |

---

## What your errata still needs (the gap)

Your `ERRATA_DIMENSIONAL_STRUCTURE.md` "What Should Be Preserved" table lists these as ✓ Correct.
They are **not**, and should move to the retraction list:

- **α⁻¹ = 4Z² + 3** — listed "✓ Correct, Fine structure constant derivation." It is a coincidence
  (the machine derives Dunbar's number identically). Retract.
- **Z² = 32π/3 from η(T³/Z₂)** — listed "✓ Correct." The *number* is fine as the posited MOND
  coefficient; the *eta-invariant derivation* is a category error. Keep Z, drop the derivation.
- **GAUGE=12 / BEKENSTEIN=4** as physics — retract as derivations (they are labels, not results).

Keep, accurately: **Z²=32π/3 as a definition**, the 8 fixed points and b₁(T³)=3 as *geometry*
(true facts about the orbifold, but they do **not** derive the physics constants), and the 7D
action as a *framework choice* — not as a theory that outputs α.

---

## The honest, defensible paper you actually have

Strip the bundle to its surviving core and you have **one real, publishable result**:

> **The MOND acceleration scale is the cosmic dynamical acceleration, a₀=(c/2)√(Gρ_c)=cH(z)/Z — a
> novel surface-gravity *framing* of Milgrom's 40-year coincidence — which predicts a₀ *evolves*
> as E(z). The 2026 data (SPARC, Vărăşteanu, MUSE-DARK) favor evolving over constant a₀ at 5σ and
> exclude the (1+z)^1.5 dust-tracking alternative; the scale sits in an over-constrained web of
> independent measurements (+4). Open: the coefficient Z (posited), and the relativistic (AeST)
> CMB completion.**

That is a real modified-gravity paper — Milgrom/McGaugh/Skordis-Złośnik territory, defensible at a
referee's desk. It is **not** a Theory of Everything, and every "unified physics / constants /
consciousness" claim should be withdrawn from the publication record, not because it is
embarrassing but because it is *false* and it discredits the part that is true.

**Recommended action:** publish a new Zenodo version that is *only* the scaling-MOND paper
(supersede v5.0), and issue a v2 errata retracting α=4Z²+3, the eta-invariant derivation, the
constants, the genetic code, the topology, and the consciousness claims. Send me the DOIs and I
will draft both, paper by paper, against this map.

---

*Sources verified this session:* all 80 scripts pass; `SALVAGE_LEDGER.md`, `WEB_SYNTHESIS.md`,
`NOVELTY.md`, `FRAMEWORK.md`, and your `ERRATA_DIMENSIONAL_STRUCTURE.md`.
