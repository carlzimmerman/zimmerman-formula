# agentGG — JWST-era high-z kinematics vs the a₀(z) branches (the inline confrontation)

*C. Zimmerman + Claude, 2026-06-11. The watch-entry-6 pre-registered response, executed on what
JWST/ALMA have actually published as of 2026-06. Run: `agentGG_jwst_highz.py` → `.out`. Provenance
note: the multi-agent harvest (workflow `jwst-kinematics-confrontation`) was killed mid-flight by the
monthly spend limit after one sweep angle returned 8 candidates; triage, extraction, and computation
were completed inline. Footing rule applied throughout: both footings (a₀ = 9.36×10⁻¹¹ fw /
1.2×10⁻¹⁰ canon), the framework's declining √ρ_DE branch with the repo's two locked CPL sets, the
rival rising E(z), the constant baseline. C3 fence honored: every statement below is keyed to the
z > 4 data here, none to z = 0.*

## VERDICT: **REGIME-INSUFFICIENT** — and the named fork that opens it

Published JWST-era high-z kinematics **cannot discriminate the a₀(z) branches — not because the
errors are large, but because of where the points sit**: every extracted object lives at
g_obs = 5.7–24 a₀, above the MOND onset on both footings. Specifically (all computed, section 2 of
the `.out`):

- **Constant and both declining branches are Newtonian-degenerate at the measured radii** (<4%
  apart in predicted velocity — the fork lives at r > r_MOND ≈ 3–14 kpc, beyond every last
  measured point). Blocked by RADIUS.
- **The rising rival is NOT Newtonian there** — at z = 7.31 its a₀_eff = 13.5 a₀ puts REBELS-25 at
  2 kpc inside its own MOND regime (boost ×1.5–2) — but its prediction still overlaps the
  observation because the baryonic mass is only known to ×7. Blocked by the MASS BUDGET.

Any high-z "BTFR offset" built from these velocities tests the mass budget (gas fraction, IMF,
M_dyn estimator) — not a₀(z).

## The harvest (8 sweep candidates → 3 extracted, 5 logged)

| Object | z | Data | What was extracted | Status |
|---|---|---|---|---|
| REBELS-25 (2405.06025) | 7.31 | ALMA [CII] | V_rot,max = 372⁺⁸²₋₆₆ km/s at 2 kpc (i = 25°±6°, corrected); σ = 33±9; M* = 8⁺⁴₋₂×10⁹; L_[CII] = 1.7±0.2×10⁹ L⊙; r_e = 2.1±0.2 kpc | FIT (Mbar bracketed) |
| DLA0817g1 (2512.05213) | 4.26 | NIRSpec Hα + ALMA [CII] | v_rot(R_e) = 206±14 (Hα) / 235±16 ([CII]); M* = 10^10.6±0.2 and M_gas,[CII] = 10^10.24±0.05 — **both dynamics-independent**; R_e = 2.0 kpc | FIT (the clean point) |
| de Graaff+ 6 JADES (2308.09742) | 5.5–7.4 | NIRSpec MOS | v(r_e) = 5–148 (not i-corrected), σ₀ = 37–60, log M_dyn = 9.2–10.2; per-galaxy M* in Appendix B (not retrievable); gas SFR-inferred only | DIRECTIONAL bin |
| GN20, 15 quiescent z~2, 16 sub-L*, 272 grism emitters, 2 outflow dwarfs | — | — | non-circular / stellar-Jeans / dispersion / population-level / outflow-contaminated | logged, unprocessed |

**Circularity catches (the working rule earning its keep):** REBELS-25's published
M_gas = 1.1×10¹¹ is M_dyn − M* — and its α_[CII] = 62 is likewise M_dyn-derived. Both ILLEGAL for
any baryonic test; the independent bracket used instead is α_[CII] ∈ [7, 30] (DSFG-like to
Zanella+19 median) → M_bar ∈ [8×10⁹ stars-only, 5.9×10¹⁰]. That ×7 bracket is the co-blocker named
in the verdict. The de Graaff M_dyn/M* = 10–40 excess sits at g_dyn ≈ 8–100 a₀ — a
high-acceleration mass-budget statement (their own reading: large gas masses or M* systematics),
non-diagnostic for a₀(z) and for the a★ floor. No sweep object reaches g < 5×10⁻¹² m/s²: nothing
enters the agentCC a★ window either.

## The fork that IS within reach (section 3 of the `.out`)

One deep ALMA [CII] rotation curve of a REBELS-class disc reaching ~3–4 R_e (r ≳ 6–10 kpc — i.e.
past r_MOND) splits the branches at fixed M_bar by **×2.3–2.4 in asymptotic velocity** — an order
of magnitude above the ~20% velocity errors:

| Branch (canon footing, M_bar bracket) | V(r ≫ r_MOND) |
|---|---|
| declining √ρ_DE (both CPL sets) | 86–143 km/s |
| constant | 106–175 km/s |
| **rising E(z) [rival]** | **204–335 km/s** |

The co-requirement: an independent M_bar to ×2 (JWST IMF/SED + a non-dynamical gas tracer).
**Registered as watch entry 12.** Until then: REGIME-INSUFFICIENT, no branch favored, no branch
wounded — and recorded with equal weight: nothing in this data hurts the declining branch, and
nothing helps it.

## Discipline notes
- Predicted-V table uses point-mass g_bar = an upper bound; only branch DIFFERENCES at fixed M_bar
  are read as the test (absolutes are consistent within the enclosed-fraction ×0.5 mass model).
- ν(y) = √(1+1/y) — the framework's own baseline shape (agentCC's locked convention).
- CPL parameter sets exactly as locked in-repo: (w₀, w_a) = (−0.83, −0.75)
  [`project_a0_tracks_dark_energy.py`] and (−0.752, −0.86) [`efe_vs_z_recompute.py`]; both run, <2%
  apart at these redshifts.
- The spend-limit kill of the verification stage means this memo has NOT had an independent hostile
  extraction audit; the five most load-bearing numbers were however each quoted with table/section
  provenance at fetch time, and the two flagged misreads (de Graaff M* ~ 10^7.4; "α_[CII] = 62 is
  independent") were caught and excluded inline.
