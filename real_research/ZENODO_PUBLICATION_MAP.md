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
| **Z² = 32π/3 "derived from η(T³/Z₂)=8×(4π/3)"** | **RETRACT the derivation [SCRIPT-PROVEN]** (keep Z as a *posit*) | `eta_local_bruning_seeley.py`: η density = **0 at every momentum** (±\|p\| cancel); 4π/3 is the unit-ball volume from D→\|D\|; **scale-invariance kill** (η is scale-free, a volume scales as c³). `twisted_heat_trace_check.py`: honest trace = integer **8** |
| **α⁻¹ = 4Z² + 3** | **RETRACT [SCRIPT-PROVEN]** | `false_discovery_rate.py`: the 34,073-formula search hits an **arbitrary** target in [100,150] to ≤0.004% **19.9%** of the time → ~0 bits; same family fits Dunbar's # & tropopause T <0.03% |
| Koide, CKM, PMNS, 9 fermion masses, GAUGE=12 | **RETRACT [SCRIPT-PROVEN]** | `is_Z_special.py`: **52 of 64** "derivations" contain **no Z** — integer arithmetic on {3,4,8,12} that reproduces for *any* base value |
| **sin²θ_W = 2·Ω_m/Ω_Λ** | **SOFTEN — coincidence, not evidence (keep, not proof)** | `omega_weinberg_relation_test.py`: *consistent* within the 3.4% cosmological window in every scheme, mechanism-free, "not yet tested" — **not cleanly dead.** My blanket "retract" was too harsh |
| genetic code (4=Bekenstein, 20=gauge+cube) | **RETRACT [ARGUED — no script]** | exact-integer relabeling (4=4, 20=12+8): no fit error to compute, unfalsifiable; argument only |
| "physics, mathematics, biology, **consciousness, and time** from first principles" | **RETRACT [ARGUED — no content]** | nothing to compute |
| M-theory 11D / M2+M5 branes | **already retracted by you** (correct) | your `ERRATA` Corrections 1–4 |
| T³/Z₂ 20.6 Gpc cosmic topology | **RETRACT [SCRIPT-PROVEN]** | `matched_circle_planck_verification.py`: R_i=0.74·χ_rec excluded by a wide margin vs Planck (α_min~15°, R_i>0.97χ_rec) |
| cosmic dipole R=19/6 | **RETRACT [ARGUED + data]** | fitted ratio; observed R fell to ~1.5–2 (arXiv:2511.00822) — argument + external data, no repo confirmation script |
| therapeutics (c-Myc, NaV1.7, PETase, CFTR, D2R, AMPs; Kd, "cures") | **PRIOR-ART ONLY, no efficacy** | your own `LEGITIMATE_FINDINGS.md` concedes this |

---

## Evidence grades — what I actually *showed* (don't dismiss without showing)

Fair challenge: a "RETRACT" next to a script name is still a dismissal until the script is run.
Running them rather than citing them tightened the map in three ways:

- **SCRIPT-PROVEN dead** — the script *demonstrates* the failure, it is not asserted:
  - **α=4Z²+3** → 19.9% look-elsewhere in α's range (the hit is the *expected* output of a 34k search).
  - **η(T³/Z₂)=32π/3** → η density is **0 everywhere**; the 4π/3 is an inserted unit-ball volume; a
    scale-free invariant *cannot* equal a c³-scaling volume (extension-independent kill shot).
  - **Koide/CKM/PMNS/masses** → 52/64 "derivations" have **no Z** — they hold for any base value.
  - **20.6 Gpc topology** → excluded by a wide margin against the real Planck matched-circle bound.
- **I had one too harsh — corrected:** **sin²θ_W = 2Ω_m/Ω_Λ** is, per its own script, a *consistent*
  coincidence inside the 3.4% cosmological window (mechanism-free, not yet testable) — **not cleanly
  dead.** It is "keep as a not-yet-evidence coincidence," not "retract." Softened above.
- **Argued, not script-proven (stated honestly):** the genetic code (exact-integer relabeling),
  "consciousness/time" (no content), and the dipole 19/6 (fitted ratio + the observed value falling)
  rest on *argument* and external data, not a repo confirmation script — a weaker basis, flagged as such.

So: I did not dismiss without showing — and showing it both *hardened* the core retractions (α, the
eta-derivation, the constants, the topology are provably dead) and *caught my own overreach* on the
Weinberg relation. That asymmetry — provable where it's dead, honest where it's only argued — is the
whole point.

## Harshness re-audit (Carl: "make sure you weren't harsh elsewhere / more legit science in there")

Re-ran the strongest pro-framework candidates fresh (not trusting the devil's-advocate files):

- **MORE legit than I credited — the *evolution* is DERIVED, not posited.** `horizon_a0_derivation.py`:
  tying a₀ to the instantaneous horizon **forces a₀(z)∝H(z)∝E(z), route-independently, and it
  needs no Z.** I had been calling the whole thing "posited"; that under-sold it. The falsifiable
  prediction has a *derivation*; only the O(1) coefficient is fit. **Elevate this.**
- **The "unique geometry" argument, tested** (`coefficient_uniqueness_test.py`): 32π/3 is a
  *legitimate* value (its √(8π/3) is the real Friedmann factor — not arbitrary), **but not
  uniquely selected** — Z=cH₀/a₀ is degenerate with H₀ (Planck+SPARC→√(32π/3), TRGB→6=Verlinde,
  SH0ES→2π=Milgrom), a ±17% band holds many simple constants, and the web is *Z-independent* (Z
  cancels in every edge), so it cannot confirm the value. So "only this geometry works and the
  web follows" does not hold — but the number is not arbitrary numerology either. Fair middle.
- **Ω_Λ≈13/19, Ω_m≈6/19, sin²θ_W=2Ω** — softened correctly, with the right reason now:
  `cosmic_weinberg_relation.py` shows these are **why-now coincidences** (a time-varying ratio
  equal to a near-constant only at the present epoch) — real ~1% matches worth *recording*, but
  *not testable as laws* (DESI confirms the value, not the relation). **Record, don't bank** —
  and do not tier them with the falsifiable a₀(z) trend. (Note: the *interlocking* claim that
  13/19 explains *both* Ω_Λ *and* μ_n/μ_p is still dead — μ_n/μ_p is the quark model's −2/3.)
- **No other major over-harshness found.** α=4Z²+3, the eta-derivation, the constants census, and
  the 20.6 Gpc topology are **script-proven dead** (shown above), not devil's advocacy.

Net: the one thing I under-credited is real and important — **the evolving prediction is derived,
not assumed.** That strengthens the surviving paper; it does not revive the constants.

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

- 2026-09-05 — PAPER4 The Filtered MOND Action (central tidal identity, comparable-mass forces, first covariant clock action, the screening operator): DOI 10.5281/zenodo.22347632 (concept 10.5281/zenodo.22347631); files qwen_claude_field_theory/papers_2026/PAPER4_filtered_action_2026.{tex,pdf,zenodo.json}
- 2026-09-06 — PAPER5 A Ceiling Dark Matter Cannot Impose (the bounded-boost theorem for MOND-class kernels; the SPARC ladder, the kernel discrimination against the exponential carrier, and the X-COP cluster violation with both escapes closed): DOI 10.5281/zenodo.22544565 (concept 10.5281/zenodo.22544564)
