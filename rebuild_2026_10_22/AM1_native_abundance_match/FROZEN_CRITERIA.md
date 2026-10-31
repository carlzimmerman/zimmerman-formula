# AM1_native_abundance_match: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** Every route E pass on SPARC takes each galaxy's halo mass from EM1's relation, lg M200 = 11.18 + 0.90 (lg M_b − 10) on background A. That relation is fitted. Does the native mass function, matched to measured baryons, give that relation? And does the SPARC line survive with the native relation in its place? This is Argon's AM1 and gate G13.

**Disclosed.** I expect the match to run high at the bright end, since abundance matching generally turns over near the knee, and EM1's single power law doesn't. I have no number on these samples. Argon's lines are on record in `../ARGON_REPLY_2026-10-31/PREDICTIONS_ON_RECORD.md`.

**Standing.** κ = ½ FITTED. Footings never pooled. Cold dark energy, never a particle. No ΛCDM input in a grade. Not "theory closed". Nothing here says the data favour the framework. No downloads.

## Inputs
- **Halos.** Press–Schechter on the native σ(M) (`EPS["A_c2b_refit"]`, the same table as Σ_coll), with X73's own δ_c, at z = 0: n(>M) on total mass. No fitted parameter. Sheth–Tormen (a 0.707, p 0.3, calibrated on ΛCDM N-body) is reported only, tagged [BORROWED FIT].
- **Baryons.** GAMA G3C with KiDS-bright M★, as P2: 1/V_max, r < 19.8, 0.02 < z < 0.30, the three equatorial boxes. M_b = M★ (1 + 10^(−0.69 lg M★ + 6.63)), P2's cold-gas relation without its extra hot term, on the native distance scale. M★ carries P2's ledger: ±0.2 dex systematic.
- **Which galaxies.** Host halos only, so the primary count is centrals: RankIterCen = 1 or ungrouped. All galaxies are reported beside it.

## The match
n_h(>M_t) = n_b(>M_b), no scatter, monotonic. The SPARC path's M200 is a cold mass under FC1, so the path takes M200 = f_c M_t. That f_c M_t is what's compared with EM1's relation; M_t is reported beside it. M_t is taken as Press–Schechter's mass, without a conversion to 200 ρ_c. ZN1's M₂₀₀/M nominal is reported beside it once it lands.

## Grade
**A. Match against EM1**, at lg M_b = 10: Δ = lg M200 − 11.18, and the slope of lg M200 on lg M_b over 9.5–10.5.
- **AM MATCHES EM1:** |Δ| ≤ 0.12 and slope 0.90 ± 0.10 (Argon's pass).
- **AM HIGH:** lg M200 at 10¹⁰ above 11.45 (Argon's fail).
- **AM LOW:** lg M200 at 10¹⁰ below 11.06.
- **AM INTERMEDIATE:** otherwise, naming what misses.
- **[MASS-CONVENTION-DEPENDENT]** appended if M_t in place of f_c M_t changes the class.

**B. The SPARC line with this relation**, in place of EM1's, through X74's grader with FC1's rule (F, both footings) and NF1's N1:
- **SPARC SURVIVES:** rms ≤ 0.110 and median Υ in [0.50, 0.80] on backgrounds A and B, for that rule.
- **SPARC BREAKS,** naming the direction.

The group path takes the same relation. Its Z is reported beside the line, and it's G13's "one rule" reading. Argon's line says a relation above 11.45 breaks SPARC at Υ below 0.42, and that's scored.

## Reported, not graded
1. All galaxies in place of centrals.
2. M★ ± 0.2 dex.
3. Sheth–Tormen [BORROWED FIT].
4. 0.02 < z < 0.15.
5. The relation at lg M_b 9, 10, 11, 11.5, against EM1's.
6. 0.15 dex of scatter in M_b at fixed M_t, applied by a Gaussian convolution of n_h before matching.

## Checks
- **K1:** Press–Schechter's integral of M n(M) over 10⁷–10¹⁶·⁵ against erfc(ν/√2) at 10⁷: |d| ≤ 2e-3 of ρ_m.
- **K2:** P2's own M_b formula and cuts reproduce its printed ρ_b,gal (lg M ≥ 8), 2.959e8: within 1e-3 relative.
- **K3:** EM1's linear relation through this path's `am1_lm` reproduces FC1's SPARC rms and median Υ and group Z exactly: |d| ≤ 1e-9.
- **MUTATE** (`--mutate`, separate outputs): n_b × 2 must move lg M200 at 10¹⁰ by more than 0.03.
- Any K failure: no verdict, exit 1.
