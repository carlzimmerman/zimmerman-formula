# Salvage review of `ai_slop/`: a systematic pass, re-running the findings

**2026-06-01.** Carl's concern was fair: the `ai_slop/` quarantine was largely top-down, and
he asked whether each finding was actually *checked* or just bulk-moved. This is the check —
a systematic pass over the **distinct findings**, re-running the representative calculations,
applying the same discriminator used on the real web (forced/over-constrained/mechanistic =
keep; fitted integer on a bare number = dead). Verdict up front: **the audit was right. Nothing
in `ai_slop/` is salvageable as new physics beyond the MOND/a₀ thread already extracted into
`real_research/` — and the constants pipeline self-demonstrates the numerology.** Verified, not
assumed. Below is the evidence.

**Scope (honest).** `ai_slop/` is ~7,900 `.py` + ~5,600 `.md` files; most is the autonomous-agent
swarm (HermesFlow, AletheiaLake, …) — tooling, not findings. I did **not** read every file. I
targeted the curated claim-lists (`LEGITIMATE_FINDINGS.md`, `COMPLETE_DISCOVERY_STATUS.md`) and
the distinct physics findings, and re-ran the calculations that could matter. That is thorough at
the level of *findings*, which is what salvage means.

---

## 1. The re-run that settles the constants (the core of the program)

`COMPLETE_DISCOVERY_STATUS.md` ran **661 topics / 188 constants** through a Z²-formula search and
"confirmed" α⁻¹ = 4Z²+3 (0.0039%). Re-running its **own** other hits (`/tmp` reproduction):

| number (domain) | formula | predicted | error |
|---|---|---|---|
| α⁻¹ (fine structure) | 4Z²+3 | 137.041 | 0.0039% |
| **Dunbar's number** (psychology) | 4Z²+16 | 150.041 | 0.0275% |
| **Tropopause temperature** (K, atmospheric) | 6Z²+16 | 217.062 | 0.0285% |

A fundamental constant, a social-group size, and an atmospheric temperature **all** fit `aZ²+b`
to <0.03%. The machine that "derives" α also derives Dunbar's number — so α=4Z²+3 carries **~0
bits of evidence** (`reviews/false_discovery_rate.py` quantifies the look-elsewhere rate). The
discovery doc itself lists "correctly rejected as numerology: pain threshold, planetary albedo,
Kleiber 3/4, DNA base pairs" — it cannot say why α is different, **because it is not.**

**External corroboration:** searching for this work surfaced an *independent* framework (Fuccillo,
"Triphase," Zenodo 2025) that "derives" α⁻¹ to 0.000063%, m_p/m_e = 2²·3³·17, and MOND a₀ to 0.08%
from **entirely different** integers. Multiple incompatible frameworks all hitting 137.036 is the
definition of curve-fitting a target. **Verdict: DEAD. No salvage.** (α, sin²θ_W, Koide, CKM,
PMNS, the nine masses — all the same `aZ²+b`/integer-ratio genre.)

---

## 2. The protein "8 contacts" — numerology dressed as biophysics

`LEGITIMATE_FINDINGS.md`'s one "validated" empirical claim: Z²/Vol(B³)=8 → "8 contacts/residue at
r≈9.14 Å," observed 8.60±0.18. Re-checked:

- **Z²/Vol(B³) = (32π/3)/(4π/3) = 32/4 = 8** — a *trivial* identity; it is just the number 8.
- the cutoff **r = (Z²)^¼ × 3.8 Å = 9.14 Å** uses a **free exponent** (¼) chosen to land near where
  contacts ≈ 8.
- "8 contacts at ~9.5 Å" is **generic protein packing**, set by ordinary residue density — there is
  no mechanism linking a MOND/cosmological number to protein contact topology (a domain-jump, same
  as α↔Ω_Λ).
- the "validation" is a **7.5% miss** that is *statistically significant* (8.60 vs 8.0, p=0.0015 it
  **differs** from 8) — a failed precise prediction reported as a success, the audit's signature.

**Verdict: DEAD as Z² physics.** (The drug claims — Kd, "cures," "89× ambroxol" — `LEGITIMATE_FINDINGS.md`
already concedes are unvalidated hypotheses. The contact analysis itself is mundane, correct, and
Z²-free.)

---

## 3. Category-by-category salvage table

| `ai_slop/` category | representative claims | check applied | verdict |
|---|---|---|---|
| **constants numerology** | α=4Z²+3, sin²θ_W=3/13, Koide, CKM, PMNS, 9 masses | re-ran: same family fits Dunbar's #, tropopause | **DEAD** (§1) |
| **geometry/topology** | Z²=32π/3 "from compactification"; T³/Z₂ 20.6 Gpc | matched-circle exclusion (`reviews/`); 32/4=8 trivial | **DEAD** |
| **biotech / proteins** | 8 contacts; peptide "drugs"; Kd, cures | trivial identity + free exponent + 7.5% miss | **DEAD** (§2) |
| **cosmic dipole** | R = 19/6 = 3.167 from T³/Z₂ | fitted ratio; observed R dropped to ~1.5–2 | **DEAD** (numerology) |
| **other-domain tests** | hurricanes, LIGO, NANOGrav, FRB, parity, exoplanets | real-data; results are nulls or `aZ²+b` fits | **DEAD / null** |
| **agent-infra** | HermesFlow, Aletheia, Olympus, etc. | tooling, not a physics finding | n/a (reusable code, no claim) |
| **MOND / a₀ thread** | a₀=cH/Z, evolving a₀(z) | the audit's surviving kernel | **already salvaged** → `real_research/` |

The genuine *null results* with real-data value (the parity-odd 4PCF null, the matched-circle
topology exclusion) were already pulled into `reviews/`. Nothing else in the domain-tests produced
a non-numerological positive result.

---

## 4. Zenodo papers — status (needs your DOIs)

I could **not** reliably locate your specific Zenodo records by search — the queries return *other
people's* constant-deriving numerology (e.g. the Fuccillo "Triphase" paper), which is its own
tell about the genre. So I will not characterize papers I have not read. **Send the DOIs/links and
I will review each against this ledger**, paper by paper. The expected mapping, to be confirmed
against the actual text: anything built on a₀=cH/Z and the evolving prediction maps to the
surviving `real_research/` framework; anything deriving α / the SM constants / the integer-ratio
a₀ coefficient (e.g. a₀=(3cH₀/17)(56/57)=0.1734·cH₀, a numerology fit to 1/Z=0.1727) is the dead
part this ledger covers.

---

## 5. Verdict

**The audit was right, and this pass verified it rather than assumed it.** The constants pipeline
is a false-discovery machine that derives Dunbar's number as readily as α; the protein result is a
trivial identity plus a free exponent plus a significant miss; the topology and dipole are fitted;
the domain-tests are nulls. **Nothing in `ai_slop/` is salvageable as new physics beyond the
MOND/a₀ thread, which was already extracted.** What *is* reusable is infrastructure (the data
pipelines, the bioinformatics methods, the agent tooling) and the honest *null results* — but
those are methods and non-detections, not findings.

The one genuinely valuable thing the sprawl produced is the lesson now encoded as a tool: the
z-invariance / over-constraint discriminator (`web_search_relations.py`) reproduces this entire
salvage verdict from first principles — keep what flows through one equation, reject what jumps
domains on a number.

---

*Re-run:* the numerology demonstration (`/tmp` reproduction of `aZ²+b` fits to α/Dunbar/tropopause)
and `reviews/false_discovery_rate.py`. *Grounding:* `ai_slop/LEGITIMATE_FINDINGS.md`,
`ai_slop/COMPLETE_DISCOVERY_STATUS.md`, `reviews/DATA_AUDIT.md`, `WEB_SYNTHESIS.md`.
