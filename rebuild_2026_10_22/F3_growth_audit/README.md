# F3_growth_audit: the growth and cosmic-shear failures, and the growth no-go, checked against the covariant screened theory

## Verdicts

| failure | verdict | the number |
|---|---|---|
| (a) gravitating-field growth 15–19 % too clumpy at 512³ (CFG555/556) | **BELONGS TO THE SETTLING RULES ONLY.** v3's own nonlinear growth is **UNDECIDABLE WITHOUT A NATIVE SIM** (spec below). | 86 % of the excess sits in the relocated source (R3 512³, k = 0.317: source auto-power 0.017 plus cross term 0.124, out of 0.163). The rest is the source's gravity acting on the particles. |
| (b) KiDS ξ± Δχ² +68.7 (CFG596) | **BELONGS TO THE SETTLING RULES ONLY.** Reproduced exactly: 144.26 / 212.99 / +68.73. v3's linear part is CONSISTENT. Its nonlinear part is UNDECIDABLE WITHOUT A NATIVE SIM. | Dust limit, linear P(k), k ≤ 0.3 h/Mpc, about 30 KiDS points: predicted S8 0.845 (A) / 0.814 (B); KiDS asks for 0.754 ± 0.063 / 0.761 ± 0.060 (1.5σ / 0.9σ). |
| (c) no-go "law + a¹ growth + no EFE" | **The no-EFE leg is evaded by paying for an EFE. The growth leg is INHERITED BY THE COVARIANT THEORY** in a new form: the K(Q) mass μ_K has no allowed window. | To keep σ8 within 5 % of the dust limit, μ_K must be ≥ 361–2542 h/Mpc. BS24 Eq. 39 caps it at 14.8 h/Mpc. The gap is **24–172×**. The EFE costs −0.30 dex on a satellite's boost (1D estimate). |

κ = ½ is FITTED. The footings are never pooled (no a₀ enters K0–K5). No dark-matter particle is used. Not "theory closed".
Nothing here says the data favour the framework. No PM simulation was run, and CFG960 was not touched.

## Files and commits

- `FROZEN_CRITERIA.md` contains the assumption ledger (§1) and was committed alone first (0bef684eea). AMENDMENT A1 is post-result and fixes a K1 algebra slip.
- `f3_growth_audit.py` → `.out`, `_results.json`. It passes 9/9, exits 0, and takes 38 s at 0.36 GB peak RSS on one thread.
- `F3_MUTATE=1` breaks K0 (F built from the particle field) and K1 (AeST-like J ∝ Y^{3/2}). It gives 7/9 and exits 1 (`*_MUTATE.*`).
- Run: `OMP_NUM_THREADS=1 nice -n 15 python3 f3_growth_audit.py`.

## 1. Assumption ledger (summary; full table in FROZEN_CRITERIA §1)

The PM engine (CFG527 lineage, the lean copy used in CFG596):
- **ICs:** EH no-wiggle spectrum, n_s 0.965, σ8 0.811, Planck-2018 ω_b and ω_c. ΛCDM-PROCESSED.
- **Background:** flat w = −1. ΛCDM-PROCESSED values on a GR form, which is native in the dust limit.
- **Cold-sector equation of motion:** the cold share rides on the same Newtonian collisionless particles as the baryons. There is no Jeans scale. POSITED; it is not BS dust.
- **The "gravitating field":** Newtonian gravity of all particles, **plus** an additive QUMOND phantom built from the baryons' Newtonian field with kernel ν_mono. This is STANDARD-MOND-MACHINERY, not AQUAL.
- **Settling:** tidal switch, turnaround catchments, census edge, f_ret table, a zero-sum shell draw and a cap. POSITED RULE; no action produces it (CFG941 (g), CFG947, CFG955).
- **Δ_ta:** from a ΛCDM shell ODE. ΛCDM-PROCESSED.

The KiDS likelihood (CFG592 library):
- The ξ± data are RAW.
- The covariance (with its ΛCDM fiducial), the SOM n(z) with its Δz prior, the shear bias and NLA IA are SURVEY-CALIBRATION.
- The projection background (Ω_m 0.3153) and D(z) are ΛCDM-PROCESSED.

The covariant theory:
- J_x, K = μ_K²(Q−1)² and γ_L are FRAMEWORK-NATIVE.
- The dust abundance is FITTED.
- **μ_K is missing from the v3 parameter table.** BS24 Eq. 39 sets μ_K⁻¹ ≫ 100 kpc, which is an external premise.

## 2. Is "settling" part of the covariant theory?

**No.** v3 has no switch, catchment, edge, f_ret or relocation. Its cold sector is a K(Q) fluid with pressure
c_s² = (Q̄−1)/Q̄ (C5), sourcing an AQUAL-type field. The engine's two load-bearing ingredients are both foreign to v3:
- the relocated source e − comp, a POSITED RULE;
- the additive QUMOND phantom, STANDARD-MOND-MACHINERY.

**(a) and (b) are carried by those two ingredients:**
- 86 % of CFG555's 512³ excess is the relocated source (above).
- CFG596's F arm minus its S0 arm is exactly those two ingredients.
- A side result from MUTATE, reported only: scoring CFG596's RES run on its **particle** field alone still gives Δχ² +10.4 against S0. The settled mass pulls the particles too.

## 3. Applying the changes one at a time (brief rule 3)

| change | effect on the failure statistic |
|---|---|
| QUMOND → AQUAL | The F arm has no AQUAL analogue without a native run. With settling and the phantom removed, F ≡ S0 and Δχ² = 0 by construction. That is not a pass, it is an absence. |
| screening (L★ ≥ 21.7 pc) | None. The scale is 4,500× below the PM cell (98 kpc/h). |
| BS dust in place of Newtonian dust | Decisive (K4/K5 below). At BS's allowed μ_K, linear σ8 falls by 3–30×. |
| native H₀ / Ω_m (A → B) | S8,pred 0.845 → 0.814. KiDS amplitude Â 0.80 → 0.87. |
| E1/E4 flags (SPS masses, h = 0.70, r200c) | They do not enter the shear chain. Only the F arm's f_ret census table (mixed provenance, CFG886) does, and it leaves with the settling rules. |

## 4. The covariant theory's own numbers

**K1 (sympy, exact).**
- (i) For v3's J_x: J′(0) = −1, so 1 + J′ = y/(1+y) → 0 on FRW.
  - The Newtonian lapse-gradient term vanishes at linear order about FRW.
  - Linear growth is therefore GR growth only where the K(Q) dust term dominates (k < aμ_K).
  - **C2's γ = 0.555, f(0) = 0.510 is AeST's result (J ∝ Y^{3/2}, J′(0) = 0). It is not v3's general result.** It is v3's result only in the dust limit μ_K → ∞.
- (ii) The dust's Jeans wavenumber is k_J² = μ_K²Q̄(Q̄+1)/2, which → μ_K² as Q̄ → 1. So the Jeans scale and the static μ²ψ mass are the same scale.

**K0c.** C2's f(0) = 0.5105 is reproduced, by this lane's solver and by CLASS.

**K2, dust-limit linear prediction (CLASS):**
- (A) the record's own plik-lite refit (C2 c2b, g = 1): σ8 0.827, Ω_m 0.313, S8 0.845;
- (B) the CFG886 native background (Ω_m 0.2976, h 0.686) with (A)'s A_s and n_s: σ8 0.817, S8 0.814;
- the PM ICs, for reference: S8 0.829.

**K3, linear model vs raw KiDS-1000 ξ±.** Points are kept only if ≥ 90 % of their integrand is at k ≤ k_lin. The background is the model's own; the nuisances are the library's.

| model | k_lin | N_kept | χ² at prediction (p) | Â (data's amplitude on P) | S8 the data ask for | class |
|---|---|---|---|---|---|---|
| A | 0.2 | 3 | — | — | — | NOT DIAGNOSTIC |
| A | 0.3 | 29 | 50.7 (0.008) | 0.80 ± 0.13 | 0.754 ± 0.063 | CONSISTENT (1.5σ) |
| B | 0.2 | 5 | — | — | — | NOT DIAGNOSTIC |
| B | 0.3 | 30 | 49.1 (0.016) | 0.87 ± 0.14 | 0.761 ± 0.060 | CONSISTENT (0.9σ) |

- The data's χ² is marginal even at the best amplitude (48.3 / 48.2 on about 30 points). S0 shows the same on its 104 points (p 0.014).
- Up to 10 % of each kept point's integrand lies at k > k_lin and is modelled linearly. That underestimates power there and biases Â *upward*.
- So the linear S8 gap is if anything larger than shown. It is a hint, not a tension, at this power.
- **The 104-point nonlinear KiDS set needs a native simulation.** Linear theory cannot score it.

**K4, BS dust at finite μ_K (background A).** The table gives σ8 ratio to the dust limit and the resulting σ8, under two kernels and two start times.

| μ_K | Jeans (C5), from 1e-3 | Jeans, from 1e-4 | BSK2 kernel, from 1e-3 | BSK2 kernel, from 1e-4 |
|---|---|---|---|---|
| 14.8 h/Mpc (μ⁻¹ = 100 kpc, BS24 Eq. 39 edge) | 0.121 → σ8 0.100 | 0.036 → 0.030 | 0.391 → 0.323 | 0.203 → 0.168 |
| 1100 h/Mpc (BSK2 floor) | 0.992 | 0.736 | 0.993 | 0.861 |
| 0.0232 h/Mpc (BS24 scale) | — | — | 0.075 | 0.041 |

- The K0b cross-check reproduces BSK2: 0.0405 vs its 0.037 at the BS24 scale, and 0.86 vs its 0.80 gate edge at 1.1e3. The difference is CLASS P(k) vs BSK2's own shape.
- Both kernels share BSK2's premise that the baryons feel Newtonian gravity at every k. Both omit radiation-era growth before a_i, so the a_i = 1e-3 column is an upper bound.

**K5: the μ_K window is EMPTY.**
- σ8 within 5 % of the dust limit needs μ_K ≥ 411 (Jeans), 361 (BSK2, from 1e-3) or 2542 h/Mpc (BSK2, from 1e-4).
- That is μ_K⁻¹ ≤ 3.6 / 4.1 / 0.6 kpc, which is 28× / 24× / 172× above BS24 Eq. 39's ceiling of 14.8 h/Mpc.
- With μ_K this large, the dust Jeans-clusters into galaxy halos above a few kpc. That is CFG946's O2a-3 "MOND + cold dust", where the BTFR is off by ×6.56 at r_ta: double counting.
- With μ_K below the ceiling, linear growth is 3–30× short.

## 5. The no-go (c), re-derived

**The premises** (CFG941 D-T, CFG946 T-O2):
1. a local theory;
2. the deep law;
3. a¹ growth of the cold sector;
4. no EFE, read from CFG925 R3.

T-O2 says a local field that supplies the deep law has an EFE. D-T says that if the cold energy is the phantom, its linear self-gravity cancels.

**How v3 meets them:**
- v3 is local and gives the law (AQUAL).
- Its cold energy is **not** the phantom; it is separate BS dust (CFG946's "option 2"). So D-T does not bite.
- It **has an EFE**, so it evades T-O2 by giving up premise 4.
  - **Price (K6):** a dwarf with g_N = 0.01 a₀ at the Milky Way's 100 kpc (g_ext = 0.11 a₀) gets a boost of 5.3 instead of 10.5. That is −0.30 dex in a 1D AQUAL estimate; 3D direction averages differ by O(1).
  - The satellites already sit +0.89 dex above the screened prediction (E3). The EFE pushes the prediction the wrong way.
- **The growth leg comes back** through μ_K (K4/K5):
  - a¹ growth holds only for k < aμ_K;
  - μ_K large enough for σ8 makes the dust double-count in galaxies;
  - μ_K small enough for galaxies starves linear growth.

So for v3 as written (quadratic BS K), "law + a¹ growth" is **INHERITED** as a failure with an empty window of 24–172×. The EFE is real, and it is the price of evading the no-EFE premise.

**Caveat.** For μ_K inside BS's window, growth on k > aμ_K comes only from the cubic deep-MOND term Y^{3/2}/a₀. That term is nonlinear from the first step (CFG946 N-L), and it adds growth that linear theory cannot see. Whether it restores σ8 without overshooting is **UNDECIDABLE WITHOUT A NATIVE SIM**.

## 6. The native simulation that decides what remains

A Khronon-native PM. It is not CFG960, which runs the old engine family.
- **Field equation:** ∇·[μ(|∇ψ|/a₀)∇ψ] + μ_K²ψ = 4πG(ρ_b + δρ_K), with μ = x/(1+x). This is AQUAL, with no QUMOND phantom and no settling, switch or catchment.
- **Species:**
  - baryons as particles;
  - BS dust as a K(Q) fluid (pressure c_s² = (Q̄−1)/Q̄), or as particles with the BSK1 hold force.
- **Parameters:** μ_K at the BS24 Eq. 39 edge (14.8 h/Mpc) and at 400 h/Mpc. Both footings. L★ is irrelevant at cell scale.
- **ICs:** linear spectra from a Khronon variant of C7's patched CLASS, not EH.
- **Box and statistic:** L100, N ≥ 512, against an S0 control on the same ICs. Scored with the CFG592/596 KiDS scorer on the native background (model B).
- **What it decides:** whether deep-MOND growth on k > aμ_K repairs the 3–30× linear deficit, and what σ8 and the KiDS Δχ² are.

## 7. Errors found in the record (not edited)

- `covariant_push_2026_10_22/THEORY_V3_DRAFT.md` §2 does not list μ_K. §3 ("CMB / linear P(k): a₀ absent at linear order") is true, but it hides that J_x′(0) = −1 removes the linear Newtonian term (K1).
- The brief's and C2 K7's "linear growth is GR growth on dust (γ = 0.555)" is AeST's result. For v3 it holds only as μ_K → ∞. BSK2 (2026-09-25) already registered the σ8/μ tension (C4 README L150).
- This lane's own frozen K1(ii) had an algebra slip, fixed in AMENDMENT A1 (post-result). The frozen line still prints `K1-orig FAIL`.

## What this does not show

- It does not score v3's nonlinear shear; that needs the sim in §6.
- It does not re-score CFG596; its frozen verdict stands.
- It does not test the alt footing (no a₀ enters the linear sector).
- It does not show that BS dust can or cannot be rescued by a non-quadratic K. With a K whose K″ is larger at early Q̄, the early Jeans scale shrinks while today's static μ stays small. That is an open door, and it would add a POSTULATED K shape.
