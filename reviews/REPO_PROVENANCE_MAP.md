# Repo Provenance Map — how the project actually progressed

**v12 · 2026-05-31 · a targeted git-history + calculation audit, so no one has to crawl 7,920 files**

This is the honest index of the repository: its timeline, what calculations exist, and which are
load-bearing. It was built from `git log` + a calculation inventory + spot-reads — *not* a
line-by-line crawl, because (as shown below) ~7,000 of the 7,920 Python files are not physics, and
the physics that exists follows two already-classified patterns. The map exists so the volume is
never mistaken for evidence.

---

## 1. Timeline — the single most important finding

**1,618 commits, 2026-03-17 → 2026-05-31 (~2.5 months; 440/480/698 per month).** The order in
which ideas entered is decisive:

| Day | Date | What first appeared |
|---:|---|---|
| **1** | 2026-03-17 | **MOND–cosmology relation: a₀ = cH₀/Z, SPARC data, high-z/JWST test** |
| 2 | 2026-03-18 | α⁻¹ "derivation" (the constants numerology begins) |
| 3 | 2026-03-20 | GUT scale M_Pl/Z⁴, proton mass, Yukawa, Weinberg, E6 |
| 4 | 2026-03-21 | Z² = 32π/3 formalized as the central constant |
| 7 | 2026-03-24 | cosmic topology / T³ torus / matched circles (v1.0.0, Zenodo) |
| 9 | 2026-03-26 | parity/4PCF/chirality **+ origin-of-life + Platonic-solids** derivations |
| 46 | 2026-05-02 | (Skordis/MOND-action only incidental until the v12 review session) |

**The repo began with the one idea that survived the entire audit.** The day-1 MOND–cosmology
relation (a₀ ∝ H, the evolving-a₀ prediction) is exactly the piece the v12 review found legitimate
and forward-testable. Everything else accreted *on top* within the first ~10 days. Volume grew
~7,900×; the load-bearing physics did not improve. The good idea was first.

## 2. Inventory — 7,920 `.py`, 5,632 `.md`, but the physics is a thin slice

| Area | Files | What it is | Status |
|---|---:|---|---|
| `HermesFlow/` + `TruthFlow/` `hermes_agent` | ~7,000 | agent-framework test suites, **duplicated 4×** (gateway/tools/CLI tests, conftest fixtures) | **not physics** |
| `meteorology/` | ~130 | a separate weather project | not physics |
| `research/foundations/` | 122 | **Z²-derives-everything** catalog (α, G, CKM, Born rule, CPT, baryogenesis, Λ, …) | **numerology** |
| `research/proof_attempt/` | 168 | **Riemann Hypothesis** proof attempts (Connes–Consani, Berry–Keating, Fargues–Fontaine, …) | separate over-reach; ~certainly invalid |
| `research/geometric_closure/` | 179 | the "all physics from Z²=8×(4π/3)" closure | numerology (audited: more knobs than data) |
| `research/offensive_campaign/` | — | cosmic-topology + BOSS parity-odd 4PCF "tests" | excluded / non-test (audited) |
| `research/` (other) + `reviews/` | ~250 | misc. analyses + **the v12 honest audit** | mixed; `reviews/` is load-bearing |

## 3. Classification verified by spot-read (not just filenames)

Three representative `research/foundations` scripts, read directly, all confirm the same pattern:
- **`Z2_ALPHA_DERIVATION.py`** — opens *"WHY α⁻¹ = 4Z² + 3 EXACTLY … Why coefficient 4? Why offset
  3?"* It starts **from** the fitted formula and rationalizes the chosen integers post-hoc.
- **`DERIVING_G_FROM_Z2.py`** — *"Strategy: find the dimensionless combination that equals a Z²
  expression."* A literal **search-to-match** for G.
- **`Z2_BORN_RULE.py`** — claims to derive P=|ψ|² "NO free parameters, NO assumptions," while
  defining CUBE=8, GAUGE=12, FACES=6, BEKENSTEIN=4, N_GEN=3 — a pile of **chosen integers**, and an
  overclaim against Gleason's theorem.

This is the `geometric_closure` audit's finding at scale: a continuous constant (Z²) plus many
freely-chosen small integers, one tunable formula per target. **No hidden legitimate gem was found.**

## 4. What is actually load-bearing (the survivors)

1. **Evolving-a₀ cosmology** (day-1 kernel) → built out in the v12 review into the **scaling-MOND
   program**: `v12_SCALING_MOND_ACTION.md`, `v12_UNIFICATION_PATH.md`, and the `reviews/` scripts
   (`horizon_a0_derivation`, `radion_mond_bridge`, `scaling_mond_action`, `gate2_cmb_scaling_a0`,
   `scaling_mond_btfr_evolution`). Falsifiable at z>10 on **low-acceleration** systems.
2. **The E₆ orbifold GUT** (`v12_E6_GUT_CONSTRUCTION.md`) — a legitimate but *inherited* SUSY
   orbifold GUT (DT splitting, proton decay); does **not** derive the constants.

Everything else — the constants numerology (`foundations`, `geometric_closure`), the cosmic
topology (`offensive_campaign`, excluded), the RH attempts (`proof_attempt`) — is either dead,
excluded, or a separate rabbit hole. The full audit lives in `reviews/` (FDR, parameter count,
matched-circle exclusion, parity null-test, topology/chirality audit, η-invariant critique).

## 5. Recommendation

**A first-to-last crawl is not worth doing.** ~7,000 files are duplicated agent boilerplate; the
physics is two large catalogs that follow patterns already verified here (constants numerology;
RH attempts). Expected yield of new legitimate physics ≈ zero, and re-reading 122 "Z² derives the
Born rule"-type scripts risks lending false weight to settled-dead material. **This map is the
index; the `reviews/` folder is the verdict.** If anything, the one nonzero-yield follow-on is a
skim of `research/proof_attempt/`'s own `RH_HONESTY_ASSESSMENT.py` checkpoints — to confirm that
effort, like this one, already self-rates as unproven.

*Method: `git rev-list`, `git log --grep`, `find`, and direct `sed`/`Read` spot-reads. Reproduce
with the commands recorded in the v12 review session.*
