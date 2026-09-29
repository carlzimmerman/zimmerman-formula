# CFG161 — a consistency check of CFG160's P4: the KURVS − KROSS differential under Kretschmer et al.'s pressure support

- **Criteria:** frozen in `CFG161_FROZEN_CRITERIA.md` (507725b7b), at the orchestrator's go.
- **Disclosure: the criteria are blind; the outcome is not.**
  - The file was written before, and committed unchanged after, the orchestrator's message that relayed CFG165's result for this question: under P4, KURVS − KROSS = +0.151 ± 0.045, 3.4σ from flat and 1.8σ from the rival.
  - Nothing in the question, the statistic, the predictions or the decision rule was set after that message.
- **Script:** `CFG161_kross_differential_p4.py`; seconds per run. It runs CFG141's and CFG140's pipelines read-only, with CFG160's P4 functions copied verbatim.
- **Runs:**
  - The main run passes both controls and H1 and exits 0.
  - The MUTATE run (KURVS velocities × 2) makes P4 manufacture evolution: D = +0.556, 11σ from flat and 9.6σ from the rival. H1 fails and the run exits 1, so the control is informative.

## Bottom line

**By the frozen rule the P4 differential lands on the rival: D = +0.148 ± 0.044, 3.3σ from flat's zero and 1.7σ from the rival's predicted +0.072. P4 does not manufacture evolution; P1, P2 and P3 do. This is a consistency statement about P4 at about 1.6σ power. It is not an a₀ verdict, and it does not validate P4.**

| prescription (μ = 0.67, δ = 0, canonical, unanchored) | D = Δ_flat(KURVS) − Δ_flat(KROSS) | the rival's prediction D_H | frozen rule |
|---|---|---|---|
| P0, no correction | +0.017 ± 0.058 | +0.069 | consistent with both |
| P1, σ₀ on KURVS (CFG140) | +0.273 ± 0.070 | +0.078 | manufactures evolution |
| P2, σ_out on KURVS (CFG141) | +0.265 ± 0.065 | +0.077 | manufactures evolution |
| P3, fixed height | +0.218 ± 0.070 | +0.074 | manufactures evolution |
| **P4, Kretschmer (primary)** | **+0.148 ± 0.044** | **+0.072** | **lands on the rival** |
| P4, α × 0.6 | +0.110 ± 0.045 | +0.071 | lands on the rival |
| P4, α × 1.4 | +0.175 ± 0.046 | +0.073 | manufactures evolution |
| P4, KURVS with σ₀ | +0.126 ± 0.050 | +0.074 | lands on the rival |

- **The power row** was printed before D: σ_D = 0.044 and D_H = +0.072 (CFG140's deep-regime approximation is +0.083), so |D_H|/σ_D = 1.6. The frozen estimate of about 1.2 was made with CFG140's larger P0/P1 errors.
- **The absolute levels tell a different story** (post hoc and labelled; computed after reading the relay, with the same code). Anchor-corrected, under P4, at the same μ = 0.67:

  | sample | Δ′_flat | Δ′_H |
  |---|---|---|
  | KURVS (z ≈ 1.5) | +0.144 ± 0.044 (+3.3σ) | −0.006 (−0.1σ) |
  | KROSS (z ≈ 0.85) | −0.004 ± 0.020 (−0.2σ) | −0.082 (−4.1σ) |

  - So at one assumed gas fraction, flat fits KROSS and the rival fits KURVS. Neither law fits both.
  - The differential lands on the rival's predicted change, but the rival's absolute level fails at z ≈ 0.85.
- **Why the gas matters here.** Both samples are scored at the same μ = 0.67 (CFG140's R3 definition). Real molecular gas fractions rise from z ≈ 0.85 to 1.5.
  - More gas in KURVS than in KROSS would lower D, toward flat's zero.
  - The frozen check does not model this; it was declared untested.

## Controls

- **C1:** CFG140's committed R3 differentials reproduce exactly (P0 +0.017 ± 0.058, P1 +0.273 ± 0.070). The MUTATE run compares against CFG140's MUTATE output.
- **C2:** the copied P4 functions reproduce CFG160's committed decision cell (Δ′_flat +0.1441, Δ′_H −0.0060).

## Readings (as frozen)

- **The differential lands on the rival at about 1.6σ power.** It is reported as that, and it is not an a₀ verdict.
- **P4 passes the consistency check in the weak sense:** it does not manufacture an evolution neither law predicts, where P1, P2 and P3 all do. That is not a validation of P4.
- **Taken with the post-hoc absolute rows,** P4 at a common gas fraction leaves the two samples on opposite sides: flat at z ≈ 0.85, the rival at z ≈ 1.5. That points at the gas evolution, or at the P4 calibration, as the next thing to pin, not at either law.

## Disclosures

- **The outcome was known before the run,** from the orchestrator's relay of CFG165; the criteria were not.
- **The post-hoc absolute rows are not in the frozen file.** They were computed after the relay, with the same functions, to report the tension CFG165 raised.
- **An exploratory probe re-ran the main script once.** It rewrote the main outputs identically (the run is deterministic); this was verified line by line.

## Untested (declared)

- KROSS's own outer σ profile;
- the gas of either sample, and its evolution;
- the samples' different radii on Kretschmer's α curve (KROSS at x = 1; KURVS at x = 1.0–3.5);
- VELA's applicability to either sample.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## After CFG167's independent re-derivation (appended 2026-09-29; the text above is unchanged)

- **Wording: "lands on the rival" is fragile, and the differential does not choose between the laws. The KURVS lean rests on a calibration and gas region the data cannot fix; it is not a detection either way.**
- **What reproduces.** CFG167 (7738a1749) is the Opus chat's independent re-derivation. It reproduces every row to 7 × 10⁻⁶ in D, with equal class labels: D = +0.1483 ± 0.0445, D_H = +0.0722, 3.33σ from flat and 1.71σ from the rival.
- **The label is a sliver.** The observed D is 0.013 (0.29 σ_D) below the "manufactures evolution" edge.
- **The 3.3σ from flat holds only if the calibration errors are common to the two samples:**
  - common calibration errors: total z_flat = 2.52;
  - independent calibration errors: z_flat = 0.83;
  - the KROSS sub-sample selection alone: 2.05.
- **KROSS sub-samples.** Over 13 variants, D ranges from +0.025 to +0.213.
  - Seven variants, including leaving out KURVS-7, leave the ±0.05 window or change class. Dropping KURVS-7 flips the class to "manufactures".
  - KROSS's RT and RT+ sub-samples differ by 4.2σ: the sample is heterogeneous beyond its statistical error.
- **Power.** With gas and calibration free (independent errors), the rule labels "lands on the rival" in 11% of flat-truth and 22% of rival-truth trials. It cannot identify the rival at this power.
- **Absolute levels.** At the common μ = 0.67, the joint χ² of the two anchored levels is 16.5 for the rival and 0.06 for flat.
  - Flat fits both samples at μ_KROSS ≈ 0.5–0.7 with μ_KURVS ≈ 2.
  - The rival needs μ_KROSS ≲ 0.3 and μ_KURVS ≈ 0.7–0.75.
  - With gas free, both laws fit. CFG170 (fdbdcf323) finds the same through the gas ratio.
- **Label and provenance items (mine):**
  - The README and the MUTATE text say "velocities × 2", but the code multiplies by 10^0.3. That is 0.5% in V, with no effect.
  - The script prints "P4 manufactures evolution" on the P0–P3 rows too. The table above labels them correctly.
  - The sentence "P4 does not manufacture evolution; P1, P2 and P3 do" omits α × 1.4, which manufactures in this README's own table.
  - The anchor-corrected absolute rows (KURVS +0.144 / −0.006; KROSS −0.004 ± 0.020 / −0.082) were not printed by this lane's committed script. They came from an uncommitted probe. CFG167 reproduces them independently, and CFG170's C2 now prints the KROSS row from a committed script.
  - This lane's frozen expectation that D "rises by about 0.6 dex" under MUTATE was wrong: the rise is 0.41.
