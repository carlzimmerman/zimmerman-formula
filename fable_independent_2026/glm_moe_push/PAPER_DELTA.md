# PAPER_DELTA — dark_universe_bridge vs the record (2026-09-17)

**Identified:** `paper/dark_universe_bridge.tex` — "The MOND Acceleration Scale as the
Cosmological Constant: a Coefficient-Free Bridge Between Galaxy Dynamics and Dark-Energy
Evolution" (June 2026; five-channel version, commit bc58b49a57). **Discarded:** the 15:03
attachment (a DE-lane work order, not a paper), prep_2026 journal kits (submission packaging),
PAPER9/PAPER29/PAPER_ATOMOS (other tracks, already audited). If the intended document is
something else (e.g. an arXiv posting today), one line redirects this sweep.

**VERDICT: the paper maps onto the repo essentially 100% — it is the June snapshot of work the
repo has since moved past. Revelations FROM the paper that the repo lacks: none found. The
valuable output is the reverse delta: three maintenance flags on the published text, each backed
by the repo's own committed record.**

## Mapping (paper claim → paper § → repo pointer → status)

| claim | § | repo | status |
|---|---|---|---|
| a₀ = c²√(Λ/32π) = (c/2)√(Gρ_DE), ~30%, coefficient "traceable, not derived" | 1 | rung 1; `a0kit/a0kit.py` (both footings); KS01 (slot NOT LIVE) | RESTATE — the paper's honesty matches the record exactly |
| dark-sector unification, "not a theory of everything" | 2 | trilemma no-go (THE_IRREDUCIBLE "stop defending" list) | RESTATE — compliant wording |
| **coefficient-free bridge** a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)) | 3 | `real_research/THE_IRREDUCIBLE_FRAMEWORK_2026-06-05.md`, verbatim: "It is **coefficient-free** (the test below cancels both κ and the z=0 value)"; `a0kit` README (`a0_of_z`) | RESTATE — same document, same week |
| √ρ_DE vs cH(z)/Z; Limbach+08, Milgrom 17 "marginally prefer √ρ_DE" | 3 | rung 8; a0kit README (canonical vs alt footings); `citations/limbach/`; FRONT_A0Z_DESI_2026-06-20 ("not novel; the fresh pieces are the value...") | RESTATE |
| DESI DR2 CPL: {1.01, 0.86, 0.74} at z={1,2,3}; bump ~6% at z≈0.4 | 3 | a0kit computes the formula; **EB-E9: z_pk = 0.41, +6.3%** (the paper's number exactly); **RETRACTIONS.md: the June CPL-dressed prediction is WITHDRAWN** ("never self-consistent with w = −1"); PREDICTIONS_LEDGER A-3: R = 0.775 [0.68, 0.88] registered, UNDECIDED | RESTATE + **RETRACTED** (see F1) |
| AeST C(Q) realization + four checks (ghost, c_GW, CMB, universality) | 4 | THE_IRREDUCIBLE (June 5, same week): **"AeST as *the* realization. It fails the computed Cassini quadrupole (~15–25σ)"** — stop defending; WHAT_IS_AQUAL: AeST's 𝓕(𝒴) monotonicity "much stricter... fatal in AeST"; rung 3 "AeST PPN" DEAD; grok_push/K002 (screened-AeST action door closed) | **CONTRADICTION** (see F2) |
| five-channel table; Fisher 3σ/30 discs, 5σ/25+anchor | 5 | `prep_2026/a0z_crossscale/` (~35 scripts: a0z_model_comparison_forecast, forecast_rubin_a0z, desi_posterior_a0z, highz_systematics_floor, lensed_deepmond_floor...); PREDICTIONS_LEDGER A-3 (Rubin 3.3σ); TC5-07/S3-30 sharpen channel 4 into the early-rotator zero point (0.009% z≤5; deficits to z=30) | RESTATE — and sharpened since |
| decisive measurement: 30–80 galaxies, JWST+ALMA, 0.06 dex/galaxy, 0.033 dex signal, +0.16 dex cH rise | 6 | registered rung-1 test (±0.13 dex, ~2027); OBSERVING_CASE_A0Z_2026.md; highz_* scripts | RESTATE |
| Z ∈ [4.2, 6.0]; excludes 1, 2, 2.9; includes √(32π/3); ~8% open to 2π | honest ¶2 | KS01 D1/D2 (three candidates inside 2σ; separation needs σ_κ ~ 1.2%); `kappa_closure/k03_half_vs_two_pi_precision.py` is literally this comparison | RESTATE |
| precedents: Milgrom 99/09, Blanchet, CKN, **Singh 2026**, **Marongwe & Kauffman 2025** | 1, honest ¶1 | README ("prior art three times over: Blanchet & Le Tiec 2009, Blanchet & Seraille 2025, and Singh 2026"); `citations/singh/`, `citations/limbach/`; opus_48 ROUTE5_NULL_STEELMAN ("MATCHED"); highz_tfr_fork DATA_LEDGER (M&K "excluded as non-usable") | RESTATE — all four external papers already absorbed |

Hand spot-checks (no script needed — every formula has a committed home): CPL with the paper's
(w₀,w_a) = (−0.752, −0.86) at z = 3 gives ρ_DE/ρ_DE0 = 0.543 → √ = **0.737** ✓ paper's 0.74,
inside the registered A-3 band [0.68, 0.88]; V-shift 0.737^{1/4} → **−0.032 dex** ✓ paper's
0.033; cH rise → **+0.165 dex** ✓ paper's +0.16; Z-mapping κ = √(8π/3)/Z reproduces the paper's
κ=½ ↔ Z=5.79 and Milgrom κ=0.461 ↔ Z≈2π ✓ — KS01's table transposed. No SW03 script: every
number has a computed home (a0kit, PREDICTIONS_LEDGER, RETRACTIONS, stage17); re-running them
would be check(True)-theatre.

## The reverse delta — maintenance flags on the published text (ordered)

**F1 — the paper's central falsifiable prediction is retracted in the author's own record.**
RETRACTIONS.md: *"The DESI-CPL a₀(z) bump, '+6% at z≈0.4' — never self-consistent with w = −1.
This is the June 'falsifiable prediction' and it is withdrawn — wrong construction."* Superseded
by the stage-17 derived flat law (a₀ constant to <1% for z ≤ 5, from the action), which converts
the paper's one-sided decline forecast into a sharper two-sided null: *any* robust a₀ evolution
below z~5 falsifies (TC5-09/ET-C4). The paper presents the declining branch as live and decisive.

**F2 — the AeST realization (Sec 4) is on the repo's stop-defending list, same week as the paper.**
THE_IRREDUCIBLE (2026-06-05): *"AeST as *the* realization. It fails the computed Cassini
quadrupole (~15–25σ)."* The paper's four checks (ghost, c_GW, CMB-linear, universality) omit
Cassini/PPN/α₂ entirely — while its own channel-5 predicts an evolving external-field effect,
which is exactly the channel L243/L264 bind to the quadrupole. WHAT_IS_AQUAL adds an
AeST-specific kill (𝓕(𝒴) monotonicity → saturating anomaly → constant sunward pull).

**F3 — MUSE-DARK III omitted.** The paper: "consistent with the high-z Tully–Fisher data that
exclude the steep cH(z) rise." The repo's registered record: MUSE-DARK III (Ciocan,
arXiv:2604.22613) measures a₀ RISING at z~1 — contested, ΛCDM-assembly-degenerate, non-diagnostic
— with the standing rule (book audit, verbatim): *"Name it, classify it non-diagnostic, never
omit it."* The declining bridge (0.74 at z=3) is further from MUSE than the flat law is.

**F4 (minor, integrity) — the paper's data-availability statement promises the four AeST
verification scripts "available at github.com/carlzimmerman/zimmerman-formula."** Filename and
content searches (kappa_0, C(Q), ρ₀/ρ_DE, ghost-free, c_GW, *aest*) find no committed scripts for
the C(Q) construction. Either commit them or amend the statement.

## What the paper does NOT supply (checked, per the standing hunts)

No mechanism for S(η_⊙) ≈ 0.008 (the paper predates the environmental-suppression class and never
mentions Cassini or the Oort pincer); no covariant action for the Γ/η law (its AeST route is the
killed one); no ANSWER-B material. The one legitimately new object the paper could have
contributed — a mechanism-level η_c — is absent, so KILLS_SYNTHESIS's open lane stands.

## Score per the loop's own culture

Paper = June snapshot; RESTATE everywhere; zero NEW; three CONTRADICTION/STALENESS flags (F1–F3)
plus one integrity flag (F4). The words "derived", "closed", "breakthrough" appear nowhere above
as claims — the paper itself never uses them dishonestly (its honest-assessment section is the
record's own language), which is why the flags are about staleness, not theatre.
