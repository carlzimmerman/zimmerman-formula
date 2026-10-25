# X34_recombination_release: is recombination a release boundary for the cold sector?

**The owner's idea.** "Think of a black hole as the singularity. What if recombination is the opposite of that?" The working
reading is hypothesis RRB. The missing cold sector (gravitating field mass, never a particle) is released, frozen out
or decoupled at recombination (z ≈ 1100), and clumps like dust afterwards.

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (6c5d581400, committed alone first). κ = ½ FITTED. Footings
9.3603e-11 / 1.1312e-10 m/s², never pooled. No knob is fitted. Not "theory closed". Nothing here says the data favour
the framework. Every number below comes from `x34_recombination_release.out` / `_results.json`.

## Verdict: RRB REDUCES TO ORDINARY CDM

| question | class | the number |
|---|---|---|
| Q1 timing, R1 (density turn-on; graded) | **EXCLUDED** | latest allowed z_on = **50 000** (grid). Δχ² crosses 25 at z ≈ 3.9e4 and 4 at z ≈ 4.9e4. At z_on = 1100 / 1500, σ₈ falls to **0.050 / 0.047** of ΛCDM. |
| Q1 timing, R2 (kinetic release from photons; reported) | UNDECIDED by the frozen rule (CLASS refuses z_d ≤ 1500) | Every computable z_d ≤ 5e4 is EXCLUDED: 2500 → σ₈ ratio 0.083, Δχ² +7.8e4. 5e4 fails on σ₈ alone (0.942, Δχ² +3.3). Only 1e5 passes. |
| Q2 relic speed | **PASS** on both footings, at z_d = 1100 / 1500 | Window σ₀ ≈ 0.025–0.095 km/s (canonical) / 0.021–0.086 (alt). It closes or nearly closes at the epochs the CMB allows. |
| Q3 scale link | **UNDECIDED (NUMEROLOGY ONLY)** | 54 trials per footing, 1 match, ≈ 1.0 expected by chance. The match is √(kT_*/m_p) = 4.95 km/s vs c₀ and contains no a₀. |

**Reading.**
- A cold component that is born at recombination, or released from the photons there, is ruled out by the acoustic
  peaks and by σ₈, by orders of magnitude.
- It must already exist and cluster by z ≈ 5e4 (R1). In the photon-coupled reading it must decouple by z ≈ 1e5 (R2).
  Both are above z_eq = 3417 by more than a factor 10.
- So for the CMB the component has to be ordinary cold dust long before recombination. Recombination is not where the
  cold sector is released. Black hole / recombination is not a mirror pair here.
- The relic-speed window in Q2 is real arithmetic, but it only holds for z_d near recombination, and Q1 forbids that
  history.

## Q1 — timing (CLASS v3.3.4; no semi-analytic proxy was needed for R1)

**The two readings.**
- **R1** (`x34_turnon.patch`, built by `x34_make_patch.py` from the pristine source on disk).
  - ρ_c = ρ_c0 a⁻³ S(a): a tanh step in ln a of width 0.05.
  - The step is fed by a w = −1 reservoir, so energy is conserved. K1 measures the identity violation at 4.6e-5.
  - Released matter is born homogeneous on synchronous slices.
- **R2** uses stock CLASS idm–photon coupling (n = 0). u_idm_g is set so that CLASS's own DM-side drag rate equals a′/a
  at z_d (K4: 1.0000).

**Method.** Each grid point is graded with C2's plik-lite + low-ℓ likelihood against C7's ΛCDM refit (χ² 1003.475,
reproduced exactly). Every point is refitted unless it already passed at the start values.

| z_on | R1 Δχ² start → refit | R1 σ₈/σ₈,ΛCDM | R1 D3/D1 | R1 class | R2 Δχ² start → refit | R2 σ₈ ratio | R2 class |
|---|---|---|---|---|---|---|---|
| 100 000 | +0.44 (no refit) | 0.990 | 4.887 | PASS | +1.35 (no refit) | 0.982 | PASS |
| 50 000 | +6.28 → **+2.81** | 0.966 | 4.877 | PASS | +10.6 → +3.32 | **0.942** | EXCLUDED (σ₈ only) |
| 20 000 | +499 → +89.0 | 0.837 | 4.810 | EXCLUDED | +312 → +48.3 | 0.797 | EXCLUDED |
| 12 000 | +5771 → +545 | 0.678 | 4.709 | EXCLUDED | +2606 → +317 | 0.663 | EXCLUDED |
| 7 000 | +4.1e4 → +2052 | 0.446 | 4.819 | EXCLUDED | +2.0e4 → ∞* | 0.503 | EXCLUDED |
| 4 000 | +3.8e5 → +9200 | 0.221 | 5.370 | EXCLUDED | +9.8e4 → ∞* | 0.349 | EXCLUDED |
| 2 500 | +2.7e5 → ∞* | 0.082 | 5.353 | EXCLUDED | +2.3e5 → +7.8e4 | 0.083 | EXCLUDED |
| 1 500 | +4.4e5 → ∞* | 0.047 | 4.402 | EXCLUDED | CLASS refuses | — | UNDECIDED |
| 1 100 | +4.7e5 → ∞* | 0.050 | 5.041 | EXCLUDED | CLASS refuses | — | UNDECIDED |

ΛCDM third-to-first peak ratio: D3/D1 = 4.886.

\* **Disclosed artefact.**
- The Gauss–Newton steering uses plik + priors only, as Q6 does. Low-ℓ TT is not steered.
- Far from ΛCDM, the refit wanders out of low-ℓ TT's spline range, and χ² becomes ∞. The plik part alone at those refits
  is still +1.6e4 to +2.1e4 (R1, z ≤ 2500).
- Every such point is EXCLUDED on σ₈ alone (ratio ≤ 0.35), so no class depends on the ∞.

**Margin.**
- R1 z_on,allowed = 5e4, which is **45× the recombination redshift** and 14.6× z_eq.
- At z_on = 1500 the start Δχ² is +4.4e5 and σ₈ is 4.7 % of ΛCDM, against lines of 25 and 5 %.
- The third peak is reshaped by a late turn-on. D3/D1 moves 4.886 → 4.40–5.37 for z_on ≤ 4000, and the peak heights
  themselves change by factors of 1.5–2.7 at fixed θ_s (K5: TT(810) × 1.50 at z_on = 1100).

**R2 near recombination.**
- CLASS's idm_g tight-coupling refuses whenever the DM opacity exceeds 1 % of Thomson.
- A reported-only rerun with that trigger raised (outside CLASS's validated regime) gives σ₈ 0.135 / 0.152 and
  D3/D1 0.14 / 0.28 at z_d = 1100 / 1500. The acoustic peaks are erased.
- The monotone trend from 1e5 down to 2500 points the same way. The frozen rule still reads UNDECIDED for R2's own class.

## Q2 — relic speed (both footings)

**Setup.**
- Relic: kinetic decoupling at T_d = T_cmb(1 + z_d); σ₀ = σ_d/(1 + z_d); e_d = (3/2)σ_d².
- μc² ≡ kT_d c²/σ_d² is a field-energy parameter, never a particle.
- Free streaming: Gilbert's equation (K2: matches the growth ODE to 3.5e-6; K3 Jeans limit passes), graded with
  X4/X22's forest rule verbatim.
- Floor: the phase-space (Tremaine–Gunn-type) bound σ_min = σ₀(ρ/ρ̄_c0)^{1/3}. It uses the 13 LG field dwarfs:
  Δ = ρ₁/₂/ρ̄_c0 = 1.6e5 / 1.7e6 / 4.3e6 (min / median / max).

**Forest bounds on σ₀ (footing-independent).**

| z_d | σ₀,PASS (strict) | σ₀,NF (verdict line) | σ₀ at λ_hm = 0.417 Mpc/h | σ₀,loose |
|---|---|---|---|---|
| 1100 | 0.0232 | **0.109** | 0.128 | 0.390 |
| 1500 | 0.0201 | 0.094 | 0.110 | 0.338 |
| 3417 (z_eq) | 0.0140 | 0.065 | 0.077 | 0.235 |
| 1e5 (R2's earliest pass) | 0.0047 | 0.022 | 0.026 | 0.080 |

At σ₀,NF the derived transfer has λ_hm = 0.355 Mpc/h. That is shorter than X22's 0.417 because this shape differs from
the L319 family.

**Floor window and intersection, at z_d = 1100.**

| | floor-compatible σ₀ (c₀ 68 % band) | ∩ forest NF | ∩ strict line | σ_d | e_d | μc² |
|---|---|---|---|---|---|---|
| canonical | 0.0248–0.0953 | **0.0248–0.0953** | empty | 27–105 km/s | 1.1e3–1.6e4 km²/s² | 2.1–31 MeV |
| alt | 0.0210–0.0862 | **0.0210–0.0862** | 0.0210–0.0232 | 23–95 km/s | 8.0e2–1.4e4 km²/s² | 2.6–43 MeV |

**Reading.**
- At z_d = 1100–1500 there is a non-empty window, so **Q2 is PASS**. A relic decoupling at recombination with
  σ_d ≈ 25–140 km/s would leave a 4–5 km/s phase-space floor in the field dwarfs and would still not fail the forest.
  It passes the strict forest line only on alt, in a sliver.
- At the epochs the CMB allows (z_d ≥ 1e5), the window is **empty on canonical** and a sliver on alt (0.0210–0.0222).
  At z_eq it is still open (0.025–0.065).
- The floor is ∝ ρ^{1/3}, not constant. At the central σ₀ the MW ultra-faints (median Δ 6.9e6) get **7.4 / 6.5 km/s**,
  against their binary-corrected σ of about 3.2 km/s. That is a worse ultra-faint overshoot than X24's constant floor.

## Q3 — scale link (dimensional enumeration, 54 trials per footing)

**Base quantities** (CLASS ΛCDM): z_* = 1088.9, H_* = 5.06e-14 s⁻¹, r_s = 144.4 Mpc comoving (132.5 kpc physical),
R_* = 0.621, c_s = 1.36e5 km/s, v_p = √(kT_*/m_p) = 4.95 km/s, v_e = 212 km/s.

| footing | trials | matches (≤ 0.1 dex) | expected by chance | nearest a₀-containing combinations |
|---|---|---|---|---|
| canonical | 54 | 1: v_p vs c₀ (+0.033 dex) | 0.99 | a₀/H_* vs c₀ −0.40 dex; v_p²/a₀ vs L★ −0.41 dex; v_p·H_* vs a₀ +0.43 dex |
| alt | 54 | 1: v_p vs c₀ (+0.087 dex) | 1.01 | a₀/H_* vs c₀ −0.26 dex; v_p·H_* vs a₀ +0.35 dex |

- The one match, the proton thermal speed at recombination ≈ c₀, contains no a₀. It is exactly the rate expected by
  chance. It is **numerology**: no action in the record derives it.
- No a₀-containing combination comes within 0.25 dex of any target.

## Checks and MUTATE

**Normal run: 12/12 with their required outcome.**
- S0-1: χ² reproduced exactly (1003.475). S0-2: σ₈ 0.827959. S0-3: the patched binary with the turn-on off equals
  vanilla (0.0). S0-4: X22's gate reproduced. S0-5: X24's c₀ re-derived, N = 13.
- K1 energy 4.6e-5. K2 growth 3.5e-6. K3 Jeans. K4 idm rate 1.0000. K5 TT(810) × 1.498. K6 TG identity. K7 a₀,canonical
  vs c²√(Λ/32π) = 0.996 (alt 1.204, reported).

**`X34_MUTATE=1`: 12/12 with their required outcome.**
- K1 fails (4.37, reservoir dropped), K2 fails (gravity sign flipped), K5 fails (vanilla binary in place of the patch,
  ratio 1.0000) and K7 fails (16π).
- Step 0, K3, K4 and K6 pass. The MUTATE run exits 0 with no Q1 refits.

**Run.**
- `python3 -I x34_make_patch.py`, then `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I x34_recombination_release.py`.
- 254 CLASS runs, 8 refused (among them the R2 starts at z_d = 1100 and 1500; the rest are refit steps), 1262 s.
- Peak RSS 0.29 GB, one thread. Builds and run files go outside the repository (`$X34_BUILD`). No downloads, and
  `compute_queue/` was not touched.

## Amendments and disclosures (post-freeze; no frozen line changed)

- **R2's u_idm_g.** It is solved at the start parameters and held fixed during the refit, so z_d is defined at the
  start point.
- **R2 sensitivity runs** (TCA trigger raised) were added after an uncommitted development run (3-point grid, no refits) had shown CLASS refusing R2 near recombination. They are reported only.
- **Development run.** That same run also printed the Q2/Q3 numbers before the final run. The code paths and the frozen lines were unchanged afterwards, apart from replacing one matmul with an explicit sum to silence spurious floating-point warnings.
- **The ∞ artefact** in the refits is disclosed above. Those classes rest on σ₈.
- **The overall label.** RRB REDUCES TO ORDINARY CDM applies because R1's allowed z_on (5e4) and R2's (1e5) both exceed
  z_eq (3417). R2's own class is UNDECIDED only because CLASS refuses z_d ≤ 1500.
