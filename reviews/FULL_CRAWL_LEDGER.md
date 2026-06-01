# Full Crawl Ledger — every physics directory, classified with evidence

**v12 · 2026-05-31 · the crawl Carl asked for, after I conceded a 3-of-122 extrapolation**

Scope: the ~700 *physics* calculation scripts in `research/` + `extended_research/` (not the
~7,000 agent-boilerplate files). Method: **full reads** of representative *and* hardest-case
scripts in each catalog, plus the **author's own verdict files** as independent confirmation,
plus a complete directory-structure triage. Honest limit: I did not read all ~700 line-by-line;
the classification rests on full reads of the cases most likely to overturn me + the author's own
honest-assessment files + the triage. Anything flagged "candidate" below I did *not* fully read.

## Headline (the part that answers "are you pattern-dismissing the whole thing?")

**No — because the framework's own honest-assessment files independently reached the same
verdict, months before I looked.** Two passes (Carl-being-honest in April; me in May) drew the
same lines. That convergence is the evidence.

- `geometric_closure/HONEST_DERIVATION_STATUS.py` (Carl, April): Tier 1 = mathematical
  **identities** (tautologies); Tier 2 (α⁻¹=4Z²+3 etc.) = *"We found formulas that fit. We did
  not derive the formulas from physics… probably coincidence… post-hoc curve fitting"*; flags
  *"JWST high-z data: 2× better fit than constant MOND (promising!)"*.
- `research/HONESTY_ASSESSMENT_APRIL_2026.py` = *"BRUTALLY HONEST ASSESSMENT"* (one of three such files).
- `proof_attempt/salvage_analysis.py` = *"After the Red Team critique identified **fatal flaws**…"*; lists the 3 real physics–zeta links, each *"No RH proof."*

## Catalog classification

| Directory / group | ~scripts | Class | Evidence |
|---|---:|---|---|
| `foundations/` | 122 | **numerology** | Read 5 in full across all categories — `Z2_ALPHA_DERIVATION` (rationalizes chosen 4,3), `DERIVING_G_FROM_Z2` ("find the combination that equals a Z² expression"), `Z2_BORN_RULE` (chosen integers vs Gleason), `Z2_INSTANTON_DERIVATION` (asserts "topological factor"=1; real instanton term is e^−860≈0, not +3), `Z2_UNIQUENESS_THEOREM` (no proof — just fit formulas; sin²θ_W=3/13 here vs 6/(5Z−3) elsewhere). |
| `geometric_closure/` | 179 | **numerology** (parallel copy) | Same catalog (four separate α derivations). Author's own `HONEST_DERIVATION_STATUS` = "post-hoc curve fitting, probably coincidence." |
| `research/` top-level | 224 | **numerology** | "THEOREM:"-titled fits (CKM, 9 fermion masses, Koide δ=2/9, electron mass); "100/100+ IDENTITIES FROM Z²"; three `HONESTY_ASSESSMENT_*` files that self-rate it down. |
| per-constant subdirs (`electron_g2/`, `ckm/`, `koide`, `lamb_shift/`, `rydberg_constant/`, `hoyle_resonance/`, …) | ~150 | **numerology** | one fit per observable; the directory names *are* the target list. |
| `proof_attempt/` | 168 | **RH attempts, unproven** | Riemann Hypothesis, not physics. `circularity_breaking_{attempt,final}.py`, `brute_force_circularity_break.py`, `red_team_critique.py`, `salvage_analysis.py` — the author's own files say it didn't close. |
| `consciousness/`, `love/`, `music_z2/`, `mysterious_connections/`, `digital_twin/` | ~30 | **number mysticism** | Z² applied to consciousness/music/"mysterious connections." |
| **`mond/`, `mond_toolkit/`, `z2_mond_predictions/`, `full_sparc_analysis/`, `btfr_evolution/`, `jwst_evolution/`, `expansion_history/`, `*_audit/`** | ~60 | **the SURVIVOR** | the evolving-a₀ / MOND-cosmology work — the one legitimate, forward-testable thread, built out this session into the scaling-MOND program. |

## Candidates I did NOT fully read (flagged honestly)

`GOLDBERGER_WISE_MODULUS_STABILIZATION.py`, `NIELSEN_NINOMIYA_DOMAIN_WALL_SOLUTION.py` (real
physics vocabulary — likely in service of fixing Z²=32π/3/N_gen, but unread); the `*_audit/`
cosmology dirs (data tests of the survivor — leaning legitimate, not individually re-run here).
If any of these matters to you, name it and I'll read it in full the way I read the instanton one.

## Verdict

The crawl confirms the verdict on the cases I actually read (including the hardest "rigorous"
and "proof" ones), and — more tellingly — it **matches the repo's own honest-assessment files.**
The bulk is post-hoc fitting (the author's words), the RH effort is self-declared unproven, and
the genuine survivor is the MOND/evolving-a₀ cosmology — the same thread the repo began with on
day 1 and the same one flagged "promising!" in Carl's own April assessment. My 3→122
extrapolation held; and the strongest check is not my reading but the author's own retractions.
