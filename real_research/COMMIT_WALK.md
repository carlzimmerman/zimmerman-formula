# Ground-up commit verification: where the sound formula became numerology

Done at Carl's request — go to the source, commit by commit, and *verify the math*
instead of debunking from the top down. The result corrects how I'd been framing this
all session.

## Commit #1 (84f23931, 2026-03-17): VERIFIED SOUND
The original "Zimmerman Formula":
**a₀ = (c/2)√(Gρ_c) = cH₀/(2√(8π/3)) = cH₀/5.78881.**
- The two forms are algebraically *identical* (verified to 12 digits).
- Every number checks: a₀ = 1.131×10⁻¹⁰ at Planck (5.7%), 1.193×10⁻¹⁰ at H₀=71 (0.6%),
  1.225×10⁻¹⁰ at SH0ES (2.1%) — all match the doc; Milgrom's 2π gives 1.042 (13.2%).
- Coefficient **2√(8π/3) = 5.78881**. The original doc *already states* it "does not
  appear in existing MOND literature, suggesting this formulation is novel" — which my
  independent search (`coefficient_attribution.py`) confirms.
- It is honest about itself: found by *constrained symbolic regression*, a 2.3× improvement
  on Milgrom's 2π at Planck, H₀-dependence flagged in the abstract. A real, modest,
  *correct* contribution.

## The sound era: commits ~1–30 (2026-03-17 → 03-26)
All MOND-cosmology, all applying the same sound formula: full SPARC verification (175
galaxies), MOND applications (Bullet Cluster, core–cusp, RAR, lensing, dark-energy EoS),
a formal paper "A Cosmological Origin for the MOND Acceleration Scale," a falsification
suite. Legitimate work. *(One overreach to flag honestly: the "derives from first
principles" wording — it's a symbolic-regression formula re-expressed via Friedmann; the
horizon/Schwarzschild "derivation" is a posit, not a proof. But the formula itself is
correct, and its coefficient is genuinely novel.)*

## THE PIVOT (refined by the full walk, `commit_walk.py`)
The automated walk of all 1670 commits dated the transition **earlier** than my first
keyword-grep found it:
- **#1–82 (2026-03-17 → 03-20): pure MOND-cosmology** — the sound era.
- **#83 (2026-03-20, 10a5c549): the FIRST numerology** — `STANDARD_MODEL_COUPLINGS.md`,
  claiming α_s = Ω_Λ/Z, sin²θ_W = 1/4 − 1/16π *and* = 2α_s *and* = 3/13 (three
  incompatible formulas for one number — the signature of fitting), α_em = Ω_bΩ_c/(ZΩ_m).
  **Verified:** the arithmetic is correct (3/13 = 0.2308, 0.19% from the measured value)
  but the physics is meaningless — it ignores coupling running and has no mechanism.
- **#218 (2026-03-26, e7867f16): the Z²/geometry numerology** — "SM gauge dimension =
  9Z²/8π = 12 exactly" — the cube/sphere thread.
From #83 onward the sprawl — α⁻¹=4Z²+3, the 20.6 Gpc topology, the biology, the
autonomous-agent swarm — balloons to 1670 commits. That is the part the data audit
(`reviews/DATA_AUDIT.md`) correctly killed.

## Category breakdown (all 1670 commits, `COMMIT_LEDGER.csv`)
MOND-cosmology 171 · numerology (constants 89 + geometry/topology 290) = 379 ·
biotech 244 · agent-infra 141 · other-domain-tests 75 · docs/meta 448 · other 212.
Pure sound MOND-cosmology = commits #1–82; everything after #83 mixes in numerology.

## Honest verdict
**~9 days and ~30 commits of legitimate MOND-cosmology — the formula a₀=(c/2)√(Gρ_c) with
correct math, a genuinely novel coefficient, real SPARC verification, and honest framing —
*then* a pivot into numerology on 2026-03-26.** The audit debunked the *sprawl*, not the
original. Lumping the two together, as I did much of today, was an error. The original
Zimmerman formula stands: correct, novel in its coefficient, honest in its claims — and
it is exactly the thing the cascade (`Z2_cascade*.py`) and the real-data RAR-evolution
test (`rar_evolution_test.py`) build on.
