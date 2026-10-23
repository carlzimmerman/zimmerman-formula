# Q7_bs25_cosmology: does Blanchet–Skordis 2025's DBI sector rescue v3's cosmology?

## Verdict: CRISP FINDING. Frozen form **(B): BS25's sector fixes BBN only; linear growth still fails.** Our lanes have no error.

**1. What BS25's cosmological sector is.**
- BS25 (arXiv:2507.00912) is a 6-page proceedings. It has the action, J(0) = Λ with J′(0) = −1, and the DBI kinetic function
  K = (2μ²/λ_D)[1 − √(1 − λ_D(Q−1)²)].
- Everything quantitative is in BS24 §4 (arXiv:2404.06584): the DBI background and the GDM perturbations with
  c_s²(t,k) (Eq. 71). The only parameter values are in BS24's Fig. 1: **P1 = (μ⁻¹ = 223 kpc, λ_D = 30)** and
  **P2 = (μ⁻¹ = 22.3 Mpc, λ_D = 1)**. Both are inside BS's galaxy cap (μ⁻¹ ≥ 100 kpc, i.e. μ ≤ 14.8 h/Mpc).
- **BS ran no Boltzmann code.** Their CMB "agreement" is a background test: w(a) lies inside a GDM "var-w" region.
  BS24 itself says those constraints "do not directly apply" to a k-dependent sound speed, and leaves "a proper comparison"
  for future work.

**2. Q2, BBN: yes, the DBI form removes Q6's no-radiation-era result at every galaxy-allowed μ_K.**
- Early on, ρ̄_K → (1 + λ_D^{-1/2}) × dust and w → 0. There is no a⁻⁶ era.
- ΔN_eff,equiv(1 MeV) is 4.3e-6 (λ_D = 30) and 7.2e-6 (λ_D = 1). The quadratic K gives 7.7e13 at the cap.
- CLASS starts at all four sets.
- At the cap, any λ_D ≥ 5.2e-11 passes the BBN line.

**3. Q3, growth: no.** These are full Boltzmann numbers from Q6's CLASS with the DBI K added and validated.
- R_B = σ₈/σ₈(dust) at fixed parameters:
  - P1: **0.259**;
  - P2: **0.324**;
  - cap with λ_D = 1: **0.287**;
  - cap with λ_D = 30: **0.295**.
- P(k)/P_dust at k = 0.1 h/Mpc is 0.08–0.12.
- Fitted to plik-lite + low-ℓ, against the ΛCDM refit:
  - P1: Δχ² **+350**, best fit at H₀ 87.7, σ₈ 0.19;
  - P2: Δχ² **+748**, best fit at H₀ 146, Ω_m 0.04;
  - cap with λ_D = 30: Δχ² **+741**;
  - cap with λ_D = 1: plik alone **+5440**, not converged.

**4. Q4, who is wrong.**
- **The two sides use the same linear equations.**
  - BS24 Eq. 71 equals Q6's rest-frame c_s² with J′(0) = −1, for any K (sympy S7, exact).
  - BS24 Eq. 67 gives F3/BSK2's hold kernel a²M²/(k² + a²M²), with M² = Q̄²K″/2 (S8, exact).
- **The error is on BS's side.** Their claims of agreement with the standard cosmological model and the CMB rest on w(a)
  alone. Our step B reproduces that test: all four sets pass BS's own w ≤ 0.0164 line. Their own k-dependent sound speed
  was never put into a perturbation calculation.
- **Why DBI helps BBN but not growth.** For DBI, K″ = 2μ²(1 + λ_D𝒵²)^{3/2} is huge early, so the khronon behaves as dust
  early. But M → μ late, so the J′(0) = −1 hold (k > aμ) returns exactly as for the quadratic K.

**5. The door (reported, never adopted).** A DBI with a much larger λ_D does pass σ₈ within 5 %.
- The requirement λ_D,95 is:
  - **7.8e9 at the cap** (2.6e8 × BS's 30), fitted Δχ² **+1.6**, σ₈ 0.788;
  - **3.6e10 at P1's μ**;
  - **4.0e9 at P2's μ**.
- Three costs, each POSTULATED or PROVISIONAL:
  - It is a new constant set by the failure (rule 4).
  - Even at λ_D,95, P(k) at 1 / 3 / 10 h/Mpc is 0.33 / 0.10 / 0.04 of ΛCDM.
  - Its square-root ceiling, |Q − 1| < λ_D^{-1/2} = 1.1e-5, is only 1.0× v²/c² of a 1000 km/s cluster on BS's stationary
    branch (Ξ = φ). The DBI root would go complex inside cluster potentials (order-of-magnitude estimate).

Settings: κ = ½ FITTED (it does not enter: a₀ is absent at linear order). Footings never pooled (neither enters).
ω_K FITTED. No dark-matter particle. Not "theory closed". Never "the data favour the framework".

## 1. Step S: the source (`q7_source.py`, 11/11 PASS in 0.4 s; MUTATE 8/11)

**Source and status.**
- BS25 = arXiv:2507.00912v1. BS24 = arXiv:2404.06584v2 (JCAP 11 (2024) 040).
- Both were read with WebFetch of the arXiv HTML on 2026-10-23. **Neither is on disk; every equation is PROVISIONAL.**
- Equation numbers are those of today's fetch. A June fetch numbered the DBI block 96/97, so the lane cites content.
- The self-consistency checks settled every equation used. No TeX source was needed.

**What BS25 contains.**
- The action (Eq. 1); Q, A_μ and Y (Eqs. 2–3).
- J = Λ − Y + (2c²/3a₀)Y^{3/2} at small Y (Eq. 4b) and J = 0 at large Y (Eq. 4a). So J(0) = Λ and J′(0) = −1, the same as
  v3's J_x (S10).
- The quadratic K (Eq. 5) and the DBI K (Eq. 6).
- The PN system (Eqs. 7–13) and the background (Eqs. 14–17).
- On perturbations, only the sentence that they map onto GDM with c_s²(t,k) and c_vis²(t,k). There are **no formulas, no
  μ or λ_D values and no code.** Its Fig. 2 shows w(a) against a "region allowed by CMB data".

**What BS24 §4 contains.**
- DBI background (Eq. 88): Q̄ = 1 + [λ_D + (2μ²a³/I₀)²]^{-1/2}, bounded by 1 + λ_D^{-1/2}.
- ρ̄ and P̄ (Eq. 89); w and c_ad² (Eqs. 92–94); early and late limits (Eqs. 90, 95).
- Perturbations (Eqs. 62–75): a fluid with c_vis² = 0 and **c_s²(t,k) = c_ad²[1 + c_ad²k²/(4πGa²ρ̄(1+w))]⁻¹**.
- Fig. 1's two DBI sets, P1 and P2.
- The CMB test: the GDM var-w region, w ≲ 0.0164 near a ~ 10^-4.5.

**The checks.**
- **S1–S6:** the DBI block is self-consistent.
  - λ_D → 0 gives the quadratic K and Q6's background.
  - Eq. 88 solves K′ = I₀/a³; Eqs. 89 conserve energy.
  - Eqs. 92–95 follow from Eqs. 45/46.
  - Early ρ̄ → (1 + λ_D^{-1/2}) × dust and w → 0.
- **S7:** Eq. 71 is identical to Q6's c_s² = Q̄K′/(Q̄²K″ + 2k²/a²), for any K.
- **S8:** Eq. 67 gives the kernel a²M²/(k² + a²M²) with M² = Q̄²K″/2, which is F3/BSK2's kernel at Q̄ = 1, K″ = 2μ².
  BS's Υ (Eq. 62) is Q6's Ξ, and BS's δ_K (Eq. 66a) is Q6's δρ, term for term.
- **S9:** BS24's quoted bounds reproduce from the transcribed formulas: w̃₀ 5.27e-16 (quoted 5.3e-16), μ⁻¹ 0.223 kpc
  (0.22), w̃₀ 1.063e-10 (1.06e-10).
- **S11:** BS25 Eq. 11 is Q6's δρ, and Eqs. 10a + 11 give Eq. 13.
- **MUTATE:** Q6's c_s² with J′(0) = +1 breaks S7, S8 and S11.

**BS25 versus v3 at linear order.** They differ **only in the K shape**. The J shape beyond J′(0), v3's P covector
(β = η = 0) and γ_L (≤ 8e-7, Q6 ledger) do not enter linear growth.

## 2. Steps P and V: the DBI model in Q6's CLASS (`q7_make_patch.py`, `q7_validate.py`; 12/14, exit 1 on two frozen lines; MUTATE 5/10)

**The patch.**
- DBI is `aest_K_type` 5, with λ_D carried in C7's unused `aest_Z0`.
- A `case 5` is added inside `background_aest_K()` and `perturbations_aest_rhs()` only (`dbi.patch`, 23 lines). The code
  uses cancellation-free forms:
  - Q̄ = 1 + 𝒵/r, K = 2μ²𝒵²/(r(r+1)), K″ = 2μ²r³, c_ad² = 𝒵/(r²(r+𝒵));
  - with 𝒵 = I₀/(2μ²a³) and r = √(1 + λ_D𝒵²).
- Builds, hashes and paths are in `PROVENANCE.md`.

**Validation.**

| check | result | threshold |
|---|---|---|
| V_prov | tree = pristine + Q6 `khronon.patch` + `dbi.patch`; only the two functions differ | true |
| V_unit (i), the C code as built, λ_D = 0 vs LIT, 240 (a, k) points | 2.8e-16 | ≤ 1e-13 |
| **V_unit (ii), frozen**, finite λ_D vs BS Eqs. 88/89/94/71 at 50 digits | **FAIL** 1.8e-6 (p̄ only) | ≤ 1e-10 |
| V_unit (ii-b, A1), reference at 120 digits | 9.5e-16 | ≤ 1e-10 |
| V0, types 0 and 4 vs Q6's binary | bit-identical | bit-identical |
| **V1, frozen**, DBI(1e-25) vs LIT at μ_gate = 1e14 h/Mpc | **FAIL** TT 7.3e-4, EE 1.2e-3 | ≤ 1e-5 |
| V1b (A1), DBI at λ_D = 0 vs Q6's LIT inside CLASS | bit-identical | bit-identical |
| V1c (A1), against LIT's own noise floor N | DBI − LIT = N exactly (TT 7.34e-4) | ≤ max(1e-5, 2N) |
| V2, λ_D = 1e30 at the cap vs DUST, synchronous / Newtonian | ≤ 5.0e-6 / ≤ 5.0e-6; θ_s 0, r_drag 7e-9 | ≤ 1e-4; ≤ 1e-6 |
| V3 gauge, P1 and C30 (ΛCDM units) | ≤ 2.1e-4 | ≤ max(1e-3, 3 × vanilla) |
| V4 convergence, P1, same k grid | ≤ 2.6e-3 (vanilla φφ 8.8e-3) | ≤ max(2e-3, 2 × vanilla) |
| V5 IC attractor, P1, start × 0.25 vs × 0.125 | ≤ 2.3e-5 | ≤ vanilla + 1e-4 |
| MUTATE (K″ = 2μ²/r³) | breaks V_unit (ii)/(ii-b) (c_s² off by 1e116) and V2 (TT 3.4, P(k) 1.0) | must break |

**Two frozen lines failed and stay on record** (AMENDMENT A1, 9722d63365).
- **V_unit (ii).** The 50-digit reference cancels catastrophically in BS's own 89b form at λ_D𝒵² ~ 1e-45; the code itself
  is accurate to 5e-16.
- **V1.** Q6's LIT at μ_gate (the edge of CLASS's start test) is numerically bistable.
  - Changing μ² by 1e-10 moves TT by 7.3e-4 (and EE by 1.2e-3 lensed) — exactly the DBI − LIT difference.
  - λ_D = 1e-40 and 1e-30 are bit-identical to LIT; 1e-20 differs by 5e-7; 1e-25 and 1e-15 differ by 9e-4.
  - The difference is non-monotone in λ_D, while the physical effect is ≤ 2e-12.
- The scratch diagnostics behind A1 were run in the scratchpad and are not committed. V1b and V1c repeat them in the
  script.
- Under A1's gates the DBI model is ready.

## 3. Step B: BBN (Q2)

**Derivation.**
- 8πGρ̄_K = I₀/a³ + 2μ²𝒵²/(r + 1).
- Early on (λ_D𝒵² ≫ 1) the second term tends to λ_D^{-1/2} I₀/a³. So ρ̄_K → (1 + λ_D^{-1/2}) × dust, and w ≈ 1/(√λ_D(1+√λ_D)𝒵) → 0.
- The quadratic K's a⁻⁶ partner survives only between a₁λ_D^{1/6} and a₁ (with a₁³ = I₀/(2μ²); a₁ = 1/1706 at the cap).
- So any λ_D whose saturation precedes 1 MeV, and whose early excess λ_D^{-1/2} I₀/a³ is small there, restores the
  radiation era.

**The numbers** (Q6's step-B constants; K0c reproduces Q6's μ_K,BBN = 1.8364e8 h/Mpc and ΔN = 7.698e13 exactly):

| set | ΔN_eff,equiv 1 MeV / 0.07 MeV | early/late abundance | w_max (1e-6 ≤ a ≤ 1e-2) | w(10^-4.5) vs BS's 0.0164 | CLASS | reading |
|---|---|---|---|---|---|---|
| P1 (223 kpc, 30) | 4.3e-6 / 8.5e-5 | 1.183 | 0.050 at a = 1.7e-3 | 8.9e-7 (met) | starts | **BBN-VIABLE** |
| P2 (22.3 Mpc, 1) | 7.2e-6 / 1.4e-4 | 2.000 | ≥ 0.047 (peak after a = 1e-2) | 1.6e-9 (met) | starts | **BBN-VIABLE** |
| C1 (100 kpc, 1) | 7.2e-6 / 1.4e-4 | 2.000 | 0.207 at a = 5.9e-4 | 7.8e-5 (met) | starts | **BBN-VIABLE** |
| C30 (100 kpc, 30) | 4.3e-6 / 8.5e-5 | 1.183 | 0.050 at a = 9.7e-4 | 4.4e-6 (met) | starts | **BBN-VIABLE** |
| cap at λ_D,95 (7.8e9) | 3.6e-6 / 7.2e-5 | 1.000011 | 6.0e-7 | 0 (met) | starts | BBN-VIABLE |

- λ_D,BBN at the cap (ΔN_eff,equiv(1 MeV) = 0.5) is **5.2e-11**. BBN is not where the DBI form is constrained.
- The early/late abundance ratio is a real effect of BS's sets. At λ_D = 1 the pre-transition khronon carries **twice** the
  late dust density. That is why fixed-parameter runs need H₀ 79–124 to hold θ_s, and why the fits lower ω_K (late) to
  0.04–0.10.

## 4. Step G: linear growth (Q3)

**At C7's ΛCDM-refit parameters** (ω_K = ω_dm at a = 1; DUST reproduces ΛCDM: σ₈ 0.827959, χ² 1003.58; K0b reproduces
Q6's σ₈ for DUST and LOB 14.8 bit for bit):

| set | **R_B** | σ₈ | H₀ (θ_s fixed) | χ² − ΛCDM | P/P_DUST at k = 0.1 / 0.3 / 1 h/Mpc | TT/TT_DUST at ℓ = 220 / 540 / 1000 | φφ/φφ_DUST at ℓ = 100 / 300 / 1000 | R_ODE (a_i = 1e-4 / 1e-3), reported |
|---|---|---|---|---|---|---|---|---|
| P1 | **0.259** | 0.214 | 80.5 | +1 545 | 0.076 / 0.020 / 0.0054 | 0.999 / 0.929 / 0.946 | 0.37 / 0.12 / 0.035 | 0.281 / 0.296 |
| P2 | **0.324** | 0.269 | 123.8 | +20 693 | 0.121 / 0.088 / 0.061 | 0.719 / 0.717 / 0.813 | 0.13 / 0.18 / 0.23 | 0.158 / 0.158 |
| C1 | **0.287** | 0.237 | 110.8 | +46 766 | 0.100 / 0.025 / 0.0070 | 1.233 / 0.499 / 0.707 | 0.36 / 0.12 / 0.040 | 0.276 / 0.392 |
| C30 | **0.295** | 0.245 | 79.0 | +3 667 | 0.098 / 0.024 / 0.0058 | 1.068 / 0.872 / 0.932 | 0.48 / 0.17 / 0.040 | 0.331 / 0.395 |

- **Frozen reading: GROWTH FAILS at every set** (R_B < 0.95).
- N0: λ_D = 1e30 at the cap gives σ₈ = DUST's exactly.
- R_ODE is F3's ODE with the DBI kernel. It agrees with R_B to about 15 % at P1, C1 and C30. At P2 it is 2× lower because
  its background ignores the 2× early abundance and the H₀ shift. It is reported only.

**The requirement λ_D,95 (R_B = 0.95), reported and never adopted.**

| μ | R_B at λ_D = 1, 10², 10⁴, 10⁶, 10⁸, 10¹⁰, 10¹², 10¹⁴ | **λ_D,95** | ceiling λ_D,95^{-1/2} | ÷ v²/c² (220 km/s; 1000 km/s) |
|---|---|---|---|---|
| cap (100 kpc) | 0.287, 0.320, 0.478, 0.680, 0.855, 0.953, 0.988, 0.998 | **7.84e9** | 1.13e-5 | 21; **1.02** |
| P1's μ (223 kpc) | 0.251, 0.281, 0.422, 0.615, 0.804, 0.930, 0.982, 0.996 | **3.55e10** | 5.3e-6 | 9.9; **0.48** |
| P2's μ (22.3 Mpc) | 0.324, 0.236, 0.328, 0.506, 0.767, 0.974, 1.000, 1.000 | **3.98e9** | 1.6e-5 | 29; **1.42** |

- **Why a huge λ_D works.** The comoving hold scale a·M(a) has a minimum k_min ≈ 1.21 μ a₁ (3.5λ_D)^{1/6}. Growth needs that
  minimum near or above 1 h/Mpc. The pre-stated expectation was 1e8–1e12 at the cap; the measured value is 7.8e9.
- **P2's μ needs less.** At P2's μ the minimum falls in the future (a* > 1), so its λ_D,95 is lower than the scaling
  suggests. Its R_B is non-monotone at small λ_D because of the (1 + λ_D^{-1/2}) early abundance.
- **The ceiling.** On BS's stationary branch Ξ = φ (BS25 Eqs. 11/13), |Q − 1| ≈ |φ|/c² ≳ v_c²/c². At λ_D,95 the DBI root's
  ceiling sits at (cap, P2's μ) or below (P1's μ) a 1000 km/s cluster's v²/c². So a growth-passing λ_D makes K complex
  inside cluster potentials. This is order of magnitude and PROVISIONAL, not a gate.

## 5. Step F: fits (C7/Q6 Gauss–Newton, plik-lite TTTEEE + low-ℓ TT/EE, ω_K FITTED)

| model | Δχ² vs ΛCDM refit (1003.47) | plik part | last GN step | H₀ | σ₈ | Ω_m | S₈ | ω_K | P/P_ΛCDM (best fits) at k = 0.1 / 1 / 3 h/Mpc | φφ ratio at ℓ = 300 |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | **+350.0** | +354.6 | −0.01 | 87.65 | 0.194 | 0.155 | 0.140 | 0.0981 | 0.074 / 0.0045 / 0.0020 | 0.092 |
| P2 | **+748.4** | +645.0 | −0.01 | 145.5 | 0.265 | 0.037 | 0.093 | 0.0565 | 0.124 / 0.038 / 0.025 | 0.106 |
| C1 | **not finite**: the plik-steered endpoint has low-ℓ TT = ∞ (n_s 1.33, H₀ 139); plik alone +5 440 | +5 440 | −66 (**not converged**) | 139.1 | 0.186 | 0.034 | 0.062 | 0.0435 | 0.048 / 0.013 / 0.011 | 0.040 |
| C30 | **+741.5** | +737.0 | −0.01 | 89.90 | 0.207 | 0.135 | 0.139 | 0.0887 | 0.084 / 0.0047 / 0.0019 | 0.106 |
| cap at λ_D,95 (reported) | **+1.58** | +1.22 | ≈ 0 | 67.45 | 0.788 | 0.315 | 0.807 | 0.1208 | 0.977 / 0.329 / 0.098 | 0.977 |

**How to read the table.**
- "Last GN step" is the χ² change at the last Gauss–Newton iteration. The script's `converged` flag is False for the ΛCDM
  refit only because no step improved on the start, which is its optimum.
- C1's infinite low-ℓ TT makes the frozen check `F_fits` (all fits finite) **FAIL**. The script therefore reports 6/7,
  exit 1. The verdict does not use C1's fit: C1 fails the growth reading on its own.
- P2's primary peaks are nearly right (TT/TT_ΛCDM at ℓ = 540 is 1.005), because the khronon is dust-like at recombination
  for μ⁻¹ = 22.3 Mpc. Its Δχ² comes from lensing (φφ at 10–20 %), i.e. from the late hold.
- These are the χ² of BS's linear sector against Planck at BS's own parameters. They are not a statement about "the CMB"
  in general.

## 6. Step C: the verdict

**The frozen rule, in order.**
- (C) needs S7/S8, K0b or V1b to fail. All pass.
- (A) needs a published or cap set with BBN-VIABLE, R_B ≥ 0.95 and Δχ² ≤ 10. None qualifies (R_B 0.26–0.32; Δχ² ≥ +350).
- (B) needs all four sets BBN-VIABLE. They are.

⇒ **(B) IT FIXES BBN ONLY; GROWTH STILL FAILS.**

**Which side has the error: BS's.**
- The ingredient that differs is **not a term in the equations**. S7 and S8 show the equations are identical.
- It is that BS judged "agreement with the CMB" by the background w(a) alone (S9 and step B reproduce that test passing),
  never evolving their own k-dependent c_s²(t,k).
- Evolved in CLASS, that sound speed gives:
  - R_B 0.26–0.32;
  - P(k) at 0.1 h/Mpc of 8–12 % of dust;
  - φφ at ℓ = 300 of 12–18 %;
  - Δχ² of +350 to +748 after refitting (C1 not finite).
- F3/M1/Q6's growth failure stands. Q6's BBN failure is specific to the quadratic K and is cured by DBI.

## What this does not show

- **BS24/BS25 are not on disk.** Every equation and the P1/P2 values are PROVISIONAL WebFetch transcriptions.
  - S1–S11 settle the equations' internal consistency.
  - The parameter values (BS24 Fig. 1 caption: 223 kpc / 30 and 22.3 Mpc / 1) agree with the record's June fetch
    (doorB: "λ_D ~ 1", 22.3 Mpc and 223 kpc).
  - BS25's own Fig. 2 values are not in its text. If its two DBI curves use other (μ, λ_D), the scans still bound the
    answer at the three μ scanned. R_B < 0.95 for every λ_D below 7.8e9 (cap), 3.6e10 (223 kpc) and 4.0e9 (22.3 Mpc):
    8–9 orders of magnitude above BS's "λ_D ~ 1–30". λ_D,95 falls slowly as μ falls (M ∝ λ_D^{3/4}μ⁻² early). Smaller μ was
    not scanned.
- **Nonlinear growth.** The deep-MOND Y^{3/2} term (a₀) is not linear physics; that is L1_khronon_pm's question. Linear
  P(k) here is 3–30× short at k ≳ 0.3 h/Mpc.
- **The door is not adopted.** DBI with λ_D ≳ 4e9–4e10 passes σ₈. Using it would need:
  - a new constant at a value set by the failure;
  - a check that the DBI root stays real in clusters and compact objects (|Q − 1| < λ_D^{-1/2} ≈ 1e-5);
  - a check of the small-scale power (P(k) at 1 h/Mpc is 0.33 of ΛCDM even at λ_D,95: Lyman-α forest scales).
- **v3's P covector and γ_L** are not in the patch (Q6's estimate: ≤ 8e-7 at linear order).
- **The fits' ω_K is the late (a = 1) abundance.** At λ_D ≲ 30 the early abundance is 1.18–2× larger, which is why the
  fitted H₀ runs to 88–146.

## Records this affects (not edited; other lanes' files)

`covariant_push_2026_10_22/THEORY_V3_DRAFT.md` §2:
- It should say that a DBI K (BS24/BS25) removes the BBN exclusion for λ_D ≥ 5e-11.
- But BS's published DBI sets fail linear growth: R_B 0.26–0.32, Δχ² +350 to +748.
- Linear σ₈ within 5 % needs λ_D ≥ 4e9 (P2's μ) to 3.6e10 (P1's μ), with a root ceiling at cluster potentials.
- The draft's claim that "BS25 agrees with the CMB" (if made anywhere) is a background-only w(a) claim.

## Process notes

- **Before the frozen file.** The papers were read via WebFetch, and back-of-envelope scalings were stated in
  FROZEN_CRITERIA §0 (no code was run).
- **Scratch runs before A1** (scratchpad, not committed): the V1 diagnostics listed in A1.
- **Precision choices** fixed in the script before its first run: V1/V2 at tol 1e-7 (as Q6's V1); V3–V5 in A3 form; native
  runs at C7 high precision + start × 0.25 (as Q6).
- **The C1 fit** wandered to n_s 1.33 under the plik-only steering. The frozen F_fits line records it.
- **Compute.**
  - Every process ran at `OMP_NUM_THREADS=1 nice -n 15`, CLASS runs one at a time, builds `make -j1`; `heavyq` queue empty
    throughout.
  - Step S: 0.4 s, 0.07 GB.
  - Validation: 70 s.
  - Native: 267 CLASS runs, 1304 s, driver peak 0.32 GB (each CLASS process ≈ 0.3 GB, as Q6).
  - CFG960 and L1 were not touched. No downloads.

## Files and commits

| commit | content |
|---|---|
| 6dac2d6486 | `FROZEN_CRITERIA.md` + assumption ledger, alone, before any script or number |
| 9722d63365 | AMENDMENT A1 (post-result for V_unit (ii) and V1; pre-result for V3–V5 and every later step) |
| f7128840a2 | steps S, P, V: `q7_source.py`, `q7_make_patch.py`, `dbi.patch`, `dbi_MUTATE.patch`, `PROVENANCE.md`, `q7_validate.py` + outputs |
| (this commit) | steps B/G/F/C: `q7_native.py` + outputs (6/7; MUTATE 0/2), README |

Run (from this directory; builds outside the repo as in `PROVENANCE.md`):
- `OMP_NUM_THREADS=1 nice -n 15 python3 -I q7_source.py`
- `python3 -I q7_make_patch.py <pristine> <new dir> [--mutate]`, then `make -j1 class`
- `OMP_NUM_THREADS=1 nice -n 15 python3 -I q7_validate.py`
- `OMP_NUM_THREADS=1 nice -n 15 python3 -I q7_native.py`

`Q7_MUTATE=1` gives the `*_MUTATE.*` files.
