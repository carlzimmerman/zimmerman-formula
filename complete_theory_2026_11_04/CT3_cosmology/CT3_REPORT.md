# CT3 cosmology: what the CMB and growth demand of a no-particle theory, and what the record has already excluded

This is a review lane under `complete_theory_2026_11_04/README.md`. It adopts nothing and reinstates nothing. The cold sector retired on 2026-11-01 stays retired, and only the owner can reinstate it. There is no dark matter particle. v3s is not reopened. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework.

The lane re-ran nothing that already exists. One new small check, `ct3_cmb_checks.py` → `ct3_cmb_checks.out`, used vanilla CLASS 3.3.4 and the raw Planck PR3 TT file already on disk. It took about 1 minute on one thread at 0.37 GB. It has no frozen gate, so it gives numbers only and no verdict. Nothing was downloaded.

## 1. The record: every cosmology attempt

| Attempt | Number hit or missed | Reason |
|---|---|---|
| Baryons only (L129, L165 CAMB, L295) | Fails. H3/H2 is 0.527 at the true peaks, against 0.979 ± 0.010 raw (CT3). σ8 is 0.077 | No non-oscillating potential well at recombination |
| MOND kernel in CLASS, no CDM (L183, L184) | H3/H2 0.56 against 0.99. Low ℓ is boosted 5-300× | x ≈ 11-14 at z 1100, so the law is Newtonian there. Any boost of baryon gravity oscillates with the plasma |
| a₀ ∝ H(z), no dark field (STANDING §3-4) | Fails growth (tilted ×300) and the forest | Same as above |
| a₀ ∝ √ρ_DE on FRW (C2 K1) | Y = 0 at order ε⁰ and ε¹, so a₀ is absent from linear FRW | The law cannot act on the linear CMB or P(k) |
| Smooth dust a⁻³ (commit 517201dd50, L165) | Third peak fails | It does not cluster |
| Release at recombination (X34) | EXCLUDED. σ8 is 0.05 of the dust case. The release must happen by z ≳ 5e4 | The cold component must already exist |
| Native turn-on, raw χ² (RF5) | A window exists only at z_on 3e4-1e6, about 9 z_eq and above | This is ordinary early dust |
| P(X) covariant closure (BOLTZ1) | Dust limit passes. No turn-on in P(X) | It folds at the first caustic |
| AeST (C2, UX2, H1, H2, AN1, AN2) | CMB passes only at g = 1, with a fitted ω_x 0.1206. K_B < 0.078. Fails clusters (H2). AN1 and AN2 give NO VERDICT (folds, no settling) | Its dust is the retired sector at linear order (UX2). ∂ρ_dust/∂a₀ = 0 |
| Khronon dust / BSK / v3s (X4, F3, L1) | σ8/σ8,dust 0.003-0.005 at the native cap | Radiation-like until z ≈ 35-78 |
| β completion (X17) | Overshoots at k ≳ 1-3 h/Mpc | |
| Barotropes / density key (DF2, DF3) | Passes gate 1 at 5 of 10 cells. Forest not graded | Requirement 4 is untouched |
| Conversion of cold into dark energy: Route C (commit 840d6ccfea), X37 | Route C: CMB lensing forces the clustering to survive to z < 0.30. X37 FAILS clusters (cores empty first) | Route C rested on Planck ΛCDM parameter values, from before the 10-25 rule |
| Neutrinos (NU1, CT3) | 3 × 0.45 eV: H3/H2 0.538, σ8 0.036. 3 × 1 eV: 0.570 | Too little, and still semi-relativistic at z 1100 |
| Seed-free / misalignment origin (X1, CFG362, CFG507) | Amount is an input. Isocurvature fails by 2e8-6e8 (X1) | The origin is relocated, not derived |
| Settling growth (PAPER45 → CFG555, CFG596) | EXCLUDED on raw KiDS, Δχ² +68.7 | This is on the gravitating field. It passed only on particles |
| Law on the web, no cold term (WG2) | CMB lensing r is 0.08-0.31 with the law off and 560-660 with QUMOND on (both with baryons-only expansion) | The measured value lies between. WG3 (bound-only switch) is frozen, with no result yet |

**Two record notes, reported here and not edited:**
- **L295's "1.192, peaks too high" is a fixed-ℓ artefact.** It reads D(816)/D(537) at ΛCDM's peak positions. The baryons-only peaks sit at ℓ 297, 778 and 1223. At the true peaks, H3/H2 = 0.527: the third peak is too low, by about half. The failure stands, but its direction and size are wrong in L295.
- **CFG689's a₀(z) band rests on the retired sector.** Its native ruler is r_d = 147.1 Mpc, which comes from ω_c 0.1202. With baryons only, r_d = 201.4 Mpc (CT3). The band is therefore conditional on a component the owner has retired.

## 2. The requirement in numbers

**Measured from the raw spectrum, without ΛCDM.** The ratio is a local fit to Planck PR3 TT with diagonal errors. It has no foreground model and is not a likelihood. Raw TT gives H3/H2 = 0.979 ± 0.010 and H2/H1 = 0.451. The ratio does not depend on geometry: at h 0.67 and at h 0.45 it is 0.527 against 0.526. It is tied to how much the potential is driven at recombination. Across the dust family (w = 0, c_s = 0, geodesic):

| ω_x/ω_b | 0 | 1.8 | 3.6 | 4.5 | 4.9 | 5.4 | 6.3 |
|---|---|---|---|---|---|---|---|
| H3/H2 | 0.527 | 0.717 | 0.868 | 0.932 | 0.963 | 0.992 | 1.046 |

- **What H3/H2 requires.** Inside the dust family, ω_x/ω_b ≈ 4.9-5.4, with n_s anywhere from 0.93 to 1.0. ω_x/ω_b ≥ 4.5 holds robustly. This agrees with RF5's raw plik-lite value, 5.35.
- **Tilt cannot substitute.** At n_s = 1.3, baryons alone reach only 0.607.

**When the component must be there.** It must be dust by z ≥ 3e4 (RF5, X34), and it must cluster at c_s ≈ 0. Its density at z 1090 is about 43 M☉/pc³ (MC1).

**Later.**
- Growth needs σ8 near 0.8. KiDS and DES ξ+ allow a range, but not 0.08. On raw KiDS, S8 is about 0.77.
- CMB lensing needs an amplitude between the law off and the law on (WG2).

**How close this is to what was retired.** The retirement records the name "cold dark energy" with these words:

> it is w = 0, c_s = 0, geodesic at linear order

That is exactly the requirement above. UX2's finding is that nothing on record supplies the term without a component that is, at linear order, the one retired.

**How a field option differs.** The options are AeST's scalar in its dust phase, a P(X) dust limit, or a "gravitating field" rather than particles. None of them differs from the retired sector at linear order. They can differ only nonlinearly, in what the dust does inside wells. The retired items were these:

> route E, native rule N, N + response, the basin split, and every core rule built on them

Those are nonlinear rules. So a field-dust with different nonlinear behaviour is arguably a new answer to the same question. The retirement itself says:

> The retirement removes the proposed answer, not the question.

The owner should judge which way to read it. Note that requirement 4 (discs must be 66-82 % depleted, MC1) bites the nonlinear behaviour whatever the dust is made of.

## 3. Untried routes (at most 5, checked against the record)

1. **Field-dust whose nonlinear phase is the a₀ field's MOND regime.** This is one field with two regimes, as in AeST, but with the dust's amount tied to ρ_DE. The record lacks this tie: C2 found ∂ρ/∂a₀ = 0.
   - Prediction: H3/H2 and S8 as for dust (0.98-0.99, about 0.8).
   - First kill: depletion in discs below 66 % at 150-250 km/s (MC1 T2), in a 3D run with a baryonic disc. AN2's grid is not converged.
   - Relation to the retired sector: identical at linear order. Needs the owner's go.
2. **Homogeneous conversion of dust into dark energy after z ~ 1, re-graded on raw data.** Route C's kill used Planck ΛCDM parameters; X37 was orbit-keyed, not time-keyed.
   - Prediction: H3/H2 0.98. S8 falls roughly as D(z_c)/D(0), to about 0.4-0.6 at z_c 1-2, plus whatever the law adds.
   - First kill: CMB lensing r on raw PR4, using WG2's machinery, against the 1σ band. Route C expects the conversion must wait until z < 0.3.
   - Relation: this is the retired sector with an end date, so it needs the owner's go. Side effect: ρ_DE grows, so a₀(2.33)/a₀(0) ≈ 0.85.
3. **Enhancing baryon clustering with modified gravity alone.** Already tried (L183, X17, WG2), and dead.
   - Prediction: H3/H2 ≤ 0.56.
   - It does not open even with a₀(1100) raised through ρ_DE(z): the boost oscillates with the plasma.
4. **Primordial power: tilt or features.** Untried, but dead at the order-of-magnitude level.
   - n_s = 1.3 reaches H3/H2 0.61 against the required ≥ 0.95. Fixing each peak would need a feature per peak, which is tuning, not derivation.
   - The σ8 deficit stays at ×10.
5. **Known neutrinos.** Dead: H3/H2 is at most 0.57, and they fall short of the required mass by about 8×. The 11 eV sterile fermion is a particle (HF1 failed it).

**Honest read: the record suggests no no-particle route passes without a component that is, at linear order, the retired sector.**

## 4. Gated sequence

- **G0** (no compute): record notes on L295 and CFG689 go into PAPER67 v1.1's CMB section; "baryons-only third peak too low, 0.53".
- **G1** (owner): decide whether a linear-dust *field* with non-route-E nonlinear behaviour counts as reinstatement.
  - No: cosmology stays an open gap. Stop here.
  - Yes: go to G2.
- **G2:** CT1 supplies a ρ_DE-tied amount term in an action. Kill: ∂ρ_x/∂ρ_DE = 0 again.
- **G3:** frozen 3D disc-depletion run. Kill: below 66 % at 150-250 km/s.
- **G4:** after WG3 lands, test S8 and CMB lensing on raw KiDS and PR4. Route 2 is graded here only if the owner opens it.
