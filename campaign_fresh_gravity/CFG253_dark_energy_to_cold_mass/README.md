# CFG253 — dark energy converted into the cold mass: an interacting vacuum

Research direction: this lane was directed by the owner (the repository's author), who proposed the idea and asked for it to be tested.

**The idea, recorded as a hypothesis, not as evidence.** It is an owner's idea: the cold dark mass the CMB needs (Ω_c h² ≈ 0.12) is dark energy "compacted" into a cold fluid rather than a particle.

**Status and files.**
- **Criteria:** `../CFG253_FROZEN_CRITERIA.md`, sha256 08cebfaf…. The hash was recorded in `CFG253_FROZEN_CRITERIA_SHA256.txt` before the script existed, and each `.out` re-checks it.
- **Script:** `CFG253_background.py` (about 4 s). It contains sympy checks and numerical background ODEs for readings (A) and (B), plus the budget for (C). It reads only the criteria and hash files, downloads nothing, and writes only inside this directory.
- **Runs:**
  - main: exit 0, 26/26 checks pass;
  - `MUTATE=1` (Q ≡ 0): exit 1. H-A1 and H-B1 fail as required, and M1 confirms that ρ_DE stays constant and a₀ flat (deviation 0.0);
  - `MUTATE=2` (the tie replaced by a₀ ∝ H): exit 1. H-A2 fails as required.
  - A second main run was byte-identical to the first.
- **Nothing is committed.** κ = ½ stays FITTED. The mass is still required. Nothing here says the theory is closed, and no sentence says any data favour it.

## Bottom line

- **A w = −1 vacuum cannot be compressed** (CFG176 S2). "Compacting" dark energy into a cold fluid can only mean an energy **exchange** Q from the vacuum to the fluid. That exchange breaks the separate conservation CFG195 flagged as premise P1, and it breaks the HT shift symmetry (CFG131 D2), so no committed action realises it.
- **(A) Continuous transfer, ongoing to today: it cannot be the cold mass.**
  - Identity (sympy S4): d(ρ_c a³)/d ln a = (Q/H) a³. So matching ΛCDM's a⁻³ history exactly means Q = 0.
  - At the declared G1 tolerance (3% of today's cold mass made after recombination), ≥ 97% of the cold mass must already exist at z = 1090.
  - At that tolerance a₀ rises by only 2–6% by z = 5 (≤ 0.025 dex). That is FLAT-LIKE against tonight's data band, but it fails CFG131's 1% line.
  - CFG131's 1% line allows only 0.5–1.6% of the cold mass to be made after recombination.
- **The expectation "making the cold mass from DE turns a₀ into roughly the rival" does NOT hold. Label: PARTIAL-SHAPE.**
  - a₀ does rise with z, the same sign as the rival.
  - Even when the transfer makes all of today's cold mass after recombination (a G1 catastrophe), a₀ goes only about 0.3–0.5 of the way to a₀ ∝ H(z) in dex at z ≤ 5:
    - a₀(2.5)/a₀(0) is 1.68–1.71, against the rival's 3.77;
    - a₀(5)/a₀(0) is 1.96–2.85, against the rival's 8.30.
  - Only the Q ∝ ρ_c form tends toward H(z) at high z (φ = 0.70 at z = 1090).
  - No G1-passing case gets anywhere near the rival.
- **(B) Early transfer, completed before recombination: it works only as CDM with a vacuum origin story.**
  - After z_t, ρ_DE = ρ_Λ0 exactly, so a₀ is exactly flat. The cold mass is the pre-transfer vacuum's excess, one-for-one with Ω_c.
  - Both G1 and G2 are therefore PASS-AS-RESTATEMENT.
  - It costs:
    - one new constant (z_t or Γ);
    - either a second, separate vacuum constant or a tuned endpoint ρ_Λ0/ρ_DE(z_t) = 1.9e-9 (z_t = 1100) down to 2.6e-24 (z_t = 1e8);
    - an early-dark-energy fraction that fails the (UNVERIFIED) EDE line for z_t ≲ 1e4 to 3e4.
  - Above z_t ≈ 1e6 it is NON-DIAGNOSTIC in linear cosmology (the GDM theorem), and it adds nothing testable.
  - Its only testable window, z_t ≈ 7e4–1e5, passes the background gates. But there most of the cold mass appears after the smallest Planck scales entered the horizon, and that mode-level CMB effect is not computed.
  - Coldness is allowed (c_s² = 0) by assumption, not derived.
- **(C) Clusters: FAIL under the premise.**
  - For a Lorentz-invariant vacuum, Q cannot be localised: the vacuum is uniform on the fluid's slices (CFG131 D1), and Q = 0 in a stationary halo (CFG131 A5).
  - The vacuum energy inside R500 is 636× short of the cluster's cold mass.
  - Inflow needs a non-Λ flowing medium, which is door 11's scoped no-go (CFG176/CFG195).
  - Under (B), the cluster's cold mass is simply the cosmic cold fluid that fell in, as in CDM.

## Reading (A): continuous transfer (today's Ω_c, Ω_Λ fixed; F_made = fraction of today's cold mass made after z = 1090)

φ(z) = log[a₀(z)/a₀(0)] / log E_ΛCDM(z), where 0 means flat and 1 means the rival.

| form | F_made | ξ | a₀(z)/a₀(0) at z = 1 / 2.5 / 5 | max dex (z ≤ 5) | φ(2.5) / φ(5) / φ(1090) | G1 | G2a (1%) / G2b (band) |
|---|---|---|---|---|---|---|---|
| A1: Q = ξHρ_DE | 0.03 | 0.0344 | 1.012 / 1.022 / 1.031 | 0.013 | 0.016 / 0.015 / 0.012 | PASS | FAIL / FLAT-LIKE |
| A1 | 0.10 | 0.112 | 1.040 / 1.073 / 1.105 | 0.044 | 0.053 / 0.047 / 0.039 | sens. only | FAIL / FLAT-LIKE |
| A1 | 1.00 (all) | 0.837 | 1.337 / 1.689 / 2.116 | 0.326 | 0.395 / 0.354 / 0.291 | FAIL | FAIL / BETWEEN |
| A2: Q = ξHρ_c | 0.03 | 0.00435 | 1.002 / 1.012 / 1.058 | 0.025 | 0.009 / 0.027 / 0.670 | PASS | FAIL / FLAT-LIKE |
| A2 | 0.10 | 0.0151 | 1.007 / 1.039 / 1.187 | 0.074 | 0.029 / 0.081 / 0.728 | sens. only | FAIL / BETWEEN |
| A2 | 0.99 | 0.658 | 1.201 / 1.713 / 2.848 | 0.455 | 0.406 / 0.495 / 0.704 | FAIL | FAIL / BETWEEN |
| A3: Q = ξH_Lρ_DE (CFG131) | 0.03 | 0.0515 | 1.012 / 1.017 / 1.019 | 0.008 | 0.013 / 0.009 / 0.002 | PASS | FAIL / FLAT-LIKE |
| A3 | 0.10 | 0.166 | 1.039 / 1.057 / 1.065 | 0.027 | 0.042 / 0.030 / 0.007 | sens. only | FAIL / FLAT-LIKE |
| A3 | 1.00 (all) | 1.065 | 1.349 / 1.675 / 1.961 | 0.293 | 0.389 / 0.318 / 0.085 | FAIL | FAIL / BETWEEN |

- **CFG131's 1% line, per form:**
  - ξ = 0.0111 / 0.00073 / 0.0274 for A1 / A2 / A3;
  - the transfer can then make only 0.96% / 0.51% / 1.59% of the cold mass.
  - A3's 0.0274 reproduces CFG131's 0.0275, a control.
- **Data band (G2b), by placement, not a re-scoring.**
  - FLAT-LIKE rows inherit the flat law's committed statements:
    - RC100 is −1.57σ from its own expectation;
    - CRISTAL's R_e fit route is DISFAVOURED-over, not robustly;
    - R_out and the independent route are CONSISTENT (CFG213/220/222).
  - Every statement carries its gas-route caveat.
  - BETWEEN rows are bracketed by committed laws but not scored by any committed row: NON-DIAGNOSTIC.
- **Reported, not gated:**
  - **Effective w.** At the G1 tolerance: A1 w₀ = −0.989 (wa −0.010), A3 −0.986 (wa −0.019), A2 −0.9994 (wa +0.004). A2's wa > 0 has the opposite sign from every committed DESI chain (CFG176/195).
  - **Background.** Making all of the cold mass lowers H(2.5) by 41% (A1) and moves D_M(1090) by +80%; at the G1 tolerance these shifts are about 1%.
  - **Early-universe limits.** EDE and BBN are negligible at the G1 tolerance (f_DE at recombination ≤ 9e-4), so G5 passes.
- **G3:** PASS. ρ ≥ 0 throughout, and the vacuum stress saturates the NEC.
- **G4:** +1 constant (ξ) per form, and Ω_c is not replaced.

## Reading (B): early transfer, completed before z_t

**B-inst: the minimum-cost bound.** All the cold mass is made at z_t, so the pre-transfer vacuum must be ρ_Λ0 + Ω_c(1+z_t)³. A sharp numerical transfer reproduces this to 0.15% (K5).

| z_t | f_EDE(z_t) | DE / radiation | remnant ρ_Λ0/ρ_DE(z_t) | ln(1/remnant) | G5 EDE (≤ 0.10, unverified) |
|---|---|---|---|---|---|
| 1100 | 0.638 | 2.6 | 1.9e-9 | 20.1 | FAIL |
| 3423 (z_eq) | 0.423 | 0.85 | 6.4e-11 | 23.5 | FAIL |
| 1e4 | 0.216 | 0.29 | 2.6e-12 | 26.7 | FAIL |
| 7e4 | 0.040 | 0.042 | 7.5e-15 | 32.5 | PASS |
| 1e5 | 0.028 | 0.029 | 2.6e-15 | 33.6 | PASS |
| 1e6 | 2.9e-3 | 2.9e-3 | 2.6e-18 | 40.5 | PASS |
| 1e8 | 2.9e-5 | 2.9e-5 | 2.6e-24 | 54.3 | PASS |
| 4.3e8 (BBN) | 6.8e-6 | 6.8e-6 | 3.3e-26 | 58.7 | PASS |
| 1e10 | 2.9e-7 | 2.9e-7 | 2.6e-30 | 68.1 | PASS |

- BBN is never binding for B-inst: at z_BBN the vacuum is at most 8.5e-8 of the radiation, against the 0.040 line.

**B-exp: an extra vacuum decaying at a constant rate Γ = H_ΛCDM(z_Γ), beside a separate ρ_Λ0.**
- The pre-transfer vacuum is 0.27–0.35 × ρ_c(z_Γ). f_EDE peaks at 0.27 (z_Γ = 1100), 0.19 (3423), 0.11 (1e4), 0.022 (7e4), 0.016 (1e5) and 1.7e-3 (1e6).
- The smallest z_Γ in the grid that passes both G1 and the EDE line is 7e4.
- At z_Γ = 7e4 and 1e5, however, 99% and 95% of the cold mass is made after z_k = 9.3e4, the horizon entry of k = 0.2/Mpc. So Planck's smallest scales entered with little cold matter. That mode-level effect is the only thing that could tell (B) from CDM in its passing window, and it is not computed here.
- For z_Γ ≥ 1e6 nothing is made after z_k.

**B-pow: one vacuum with Q = ξHρ_DE (ξ < 3) that switches off at z_t.**
- Because ρ_DE is continuous and equals ρ_Λ0 at z_t, the transfer creates only ρ_c(z_t) = ξρ_Λ0/(3 − ξ) (sympy S5).
- That is ≤ 5.6e-8 of the mass needed. A power-law transfer cannot make the mass; only a decay much faster than H can.

**Gates for (B):**
- **G1 and G2:** PASS-AS-RESTATEMENT (CDM's amount; the framework's constant ρ_Λ).
- **G3:** PASS.
- **G4:** +1 constant (z_t or Γ), plus a separate remnant vacuum or the tuned endpoint above.
- **G5:** FAIL for z_t ≲ 1e4, PASS above (conditional on the unverified bounds).
- **Coldness:** PASS BY ASSUMPTION. With Q^μ ∥ u_c and Q independent of ρ_c, CFG131 D1 gives c_s² = 0, which allows the fluid to be cold; it does not force it.
- **Adiabaticity:** argued, not computed. A decay running on local proper time from a uniform vacuum is adiabatic by the separate-universe argument. A trigger on a different clock would seed CDM isocurvature, whose Planck bound is known here only from memory (UNVERIFIED).
- **Overall:** REDUCES-TO CDM with a vacuum origin story. It is NON-DIAGNOSTIC for z_t ≳ 1e6, because linear cosmology sees only (w, c_s², c_vis²) and the amount (the GDM theorem; `real_research/dark_fluid_2026/README.md`).
- Before z_t, a₀ ∝ √ρ_DE would be 2.3e4× (z_t = 1100) to 6e11× (1e8) larger. No galaxies exist then, and a₀ enters no linear coefficient (CFG4_cosmology.out header), so this is not scored.

## Reading (C): clusters

- **Local budget.** The vacuum energy inside R500 is Ω_Λ/500 = 1.37e-3 of the mean density there. Converting all of it gives 1.6e-3 of the cold mass needed (0.872 of the total, from 6.8× baryons): **636× short**.
- **Inflow.** To supply the mass through the R500 sphere at c, a flow must carry ε = 0.069–0.194 of the vacuum flux ρ_Λ c (R = 1.0–1.4 Mpc, over 5–10 Gyr).
  - A w = −1 vacuum carries exactly zero flux (CFG176).
  - For a NEC-respecting non-Λ medium, CFG176/CFG195's 0.078 (0.090 NEC-only) is a cosmic-mean, perfect-fluid, integrated column. It is not a per-cluster bound, so the comparison is indicative only.
  - That route is door 11, a scoped no-go (CFG176, CFG195), and the compaction there needs 1 + w of order 1 (CFG195 A7).
- **Covariant constraint.** For a Lorentz-invariant vacuum, ∂_μρ_Λ = Q u_μ (CFG131 D1), so the vacuum stays uniform on the fluid's slices and Q cannot be localised. In a stationary halo Q = 0 (CFG131 A5).

## Hand predictions (frozen §5)

All eight were right within their stated ranges (P1–P8 PASS as reported checks). P7's "z_t ≳ 3e4" came out as 7e4, the grid's first passing point above 1e4.

## Disclosures

- **A scratch probe was run before the full script.** It was a copy of the A3 solver, in the scratchpad and outside this directory. It showed a backward finite-time blow-up of ρ_DE for ξ ≳ 1.12, and it printed F_made for ξ = 0.5–1.4. The A3 search bracket was set from it.
- **The first two full runs were killed without completing.** LSODA hung in the B-step solver.
  - The B-step was changed from a constant K = Γ/H to Γ = K·H_ΛCDM(z_t), integrated with DOP853 from z_t, and B-exp was switched to DOP853.
  - The A-section numbers seen in the partial first output are identical to the final ones.
- **Changes after seeing output:**
  - a G1 label used a strict ≤ 0.03, which rendered root-finder noise (F_made = 0.03 + 1e-9) as "sens. only". A tolerance of 1e-6 was added;
  - B-exp's EDE maximum was first taken over z ≥ 3.2, which picked up today's Λ era. It is now taken over z ≥ 50;
  - the column heading "made>7e4" was relabelled "made<z_k" (z_k = 9.33e4, which is what the code computes).
  - No verdict changed.
- **Normalisation.** This lane fixes today's Ω_c and Ω_Λ; CFG131 anchors ρ_c a³ at z = 999. The D_M shifts are normalisation-dependent and reported only.
- **From memory, UNVERIFIED:**
  - the EDE line (≤ 0.10 in 1e3–1e5);
  - ΔN_eff ≤ 0.3 and z_BBN ≈ 4.3e8;
  - the typical R500 of 1.0–1.4 Mpc;
  - the CDM-isocurvature bound, not scored.
- **Committed inputs used:**
  - Planck ω_c = 0.1200 ± 0.0012 (CFG4_cosmology.out);
  - z_rec = 1090 and z_eq = 3423 (L121 via CFG251);
  - Ω's from CFG131's Dcommon;
  - CFG222's proxy values 2.16 / 4.52 / 6.20.
- **Not blind.** The criteria were written after reading the committed results they cite.
- **Not computed:** a Boltzmann-code CMB run for any reading, including B's 7e4–1e5 window; a likelihood; perturbations during the transfer (A2 inherits CFG131's dust theorem while Q_ρ ≠ 0); an action.

## What would be testable

- **(A):** a transfer at the ≤ 1–3% level shows up in a₀ first. a₀(5)/a₀(0) = 1.02–1.06 is invisible to tonight's band but beyond CFG131's 1% line. A2's wa > 0 is also the opposite sign from DESI. The owner's idea in this reading makes only that sliver of the mass.
- **(B):** only a transfer epoch of z_t ≈ 7e4–1e5 could leave a signature, in Planck's damping tail. That needs a Boltzmann run, not done here. Above 1e6, (B) is observationally CDM.

## Reproduce (from the repository root)

```
python3 campaign_fresh_gravity/CFG253_dark_energy_to_cold_mass/CFG253_background.py            # rc 0
MUTATE=1 python3 campaign_fresh_gravity/CFG253_dark_energy_to_cold_mass/CFG253_background.py   # rc 1 (H-A1, H-B1 fail)
MUTATE=2 python3 campaign_fresh_gravity/CFG253_dark_energy_to_cold_mass/CFG253_background.py   # rc 1 (H-A2 fails)
```
