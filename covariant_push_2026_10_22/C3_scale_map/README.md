# C3_scale_map: do AeST's own scales give L★?

## Verdict: SCOPED NO-GO

No term in AeST's class can produce L★-type small-scale screening. A covariant screened theory is therefore
**AeST plus one named term**, not AeST. With that term, the local predictions are the same as D7d/CFG740/E4 to within
3 %. L★ becomes a **new constant of the covariant theory**, and its value is **FITTED**. κ = ½ stays FITTED. Not theory closed.

- Criteria were frozen first (c16ef33ae5). AMENDMENT A1 (6dba29d773) is **post-result**.
- Script: `c3_scale_map.py` takes 3.4 s, peaks at 0.34 GB, runs single-threaded, and makes no downloads.
  - It scores **9/11 PASS and exits 1**. Two frozen checks fail, and both fails are kept (see "Two frozen fails").
- `--mutate` flips the mass-term sign and drops the named term. K1 and K4 then fail, along with the frozen K5, giving 7/11 (`*_MUTATE.*`).
- Run 1, before the amendment, is kept as `c3_scale_map_RUN1_preamend.out`.
- Every number below is in `c3_scale_map_results.json`.

**Source status.** The SZ21 equations used here come from the record's transcriptions of the arXiv LaTeX. The sources are:
- SZ21 = Skordis & Złośnik, arXiv:2007.00082: Eq. (5) action, Eq. (6) quasi-static action, μ, "μ⁻¹ ≳ 1 Mpc" and r_C;
- arXiv:2109.13287: Eq. (30) c_s² and the aether map c₁ = K_B, c₃ = −K_B.

The transcriptions are in `real_research/bridge1_aest_equations.md` and in `real_research/reviews/typeII_known_limits_2026.py` and
`ppn_verify_transcription_2026.py`. **No copy of either paper is on disk.** All of these equations are
"external input, not verified on disk".

## 1. AeST's scales, and which regime each one controls

| scale | what it controls | regime |
|---|---|---|
| a₀ (coefficient of the 𝒴^{3/2} term) | the acceleration switch to MOND | an acceleration, not a length |
| μ = √(2K₂/(2−K_B)) Q₀, with μ⁻¹ ≳ 1 Mpc | the mass term μ²Φ | **large r** |
| r_C = (r_M μ⁻²)^{1/3} | where μ²Φ overtakes the MOND field | **large r**: 3.3–3.4 kpc for the Sun, 17 kpc for a globular, 230 kpc for a 10¹¹ M☉ galaxy |
| curl length L★_F² = 2K_B/((2−K_B)Q₀²) | stiffness of the aether's transverse part | L★_F ≥ √2/(c_s μ) ≥ 1.41 Mpc if c_s ≤ c |
| λ_s (J → λ_s𝒴) | renormalises G in the Newtonian regime | no length |

**The mass term works at large scales, in the opposite direction to L★.** The record's SZ21 transcription gives
∇²Ψ + **μ²**Ψ = 4πĜρ + ∇²φ (typeII F7). That is a Helmholtz sign, so beyond r_C the field **oscillates**. It is not a
Newtonian switch-off. The question's premise ("Newtonian-like at large distances") is corrected by this.

On a point mass (K1, sympy, exact), the Newtonian regime gives:
- Φ = −GM cos(μr)/r;
- pull = GM(cos μr + μr sin μr)/r² = **GM/r² + GMμ²/2** + O(μ⁴r²).

So AeST already contains a constant sunward "hedgehog", like the screened theory's GM/L★². Its equivalent length is
L_eq = √2/μ ≥ **1.41 Mpc**, which is 1.6×10⁴ times the window top. It is **added to** MOND and does not replace it. For the
Sun it is 7.0e-26 m/s².

In the deep-MOND regime (K2), the fractional correction is −(μ²r³/r_M)(ln(r/r₀)/3 − 1/9).
- It grows **outward**.
- It depends on the zero point of Φ, which is a cosmological gauge.
- The onset radius is exactly SZ21's r_C.

## 2. Can AeST's class screen small systems? No. Here is the proof.

**Theorem (K3, sympy, plus an exact nonlinear argument).**
- In the static weak-field limit, every AeST-class term reduces to the same pieces. These are:
  - the Einstein-aether gradient terms, c₁|∇×A|² + c₁₂₃(∇·A)²;
  - F(𝒴, 𝒬) and J·∇φ.
- The scalar enters only through V = ∇φ + Q₀A, which is the spatial projection q^{μν}∇_νφ.
- Varying φ gives ∇·(∂L/∂V) = 0.
- Varying the longitudinal aether α then gives c₁₂₃∇⁴α = 0, so α = 0. This holds for **any** F, not only at linear order.
- So the shift symmetry of φ absorbs any longitudinal aether stiffness. AeST itself has c₁₂₃ = 0 anyway.
- The curl stiffness c₁ = K_B acts only on ∇×V, and that vanishes for a spherical source.
- Result: the spherical static sector has **no length except μ**. K3 finds that Φ is independent of both c₁₂₃ and c₁, and that α = a_T = 0.

**The missing term (K4, sympy, exact).**
- L★ screening needs a stiffness on ∇·V. That is the term **−β_L [∇_μ(q^{μν}∇_νφ)]²** in the SZ21 bracket, with
  **β_L = (2 − K_B) L★²/2**.
- For a radial field, its Euler–Lagrange operator equals the radial vector Laplacian in D7d's equation (P). So the
  isolated sector reproduces CFG691's ODE exactly.
- It is a second-derivative scalar term, so it lies **outside** AeST's first-derivative class F(𝒴, 𝒬).
- On FRW at linear order it gives k⁴χ² (χ is SZ21's mixing variable). That term has spatial derivatives only, so it
  brings no Ostrogradsky time derivatives. Its relative size at k = 0.1 Mpc⁻¹ is about 1e-11.
- Full well-posedness is OPEN.
- Under rule 1 this counts as **+1 posited term and +1 constant (β_L)**.

**The two halves of the stiffness differ.** In D7d, γ_F = γ_L. In the AeST embedding (V1), the curl half comes from
K_B and is fixed by AeST's scales: L★_F ≥ √2/(c_s μ). For L★_F to fall inside the window, c_s would have to be at least
**1.6×10⁴ c** (90 pc) or **5.9×10⁴ c** (24 pc). So V1 has γ_F/γ_L ≥ 2.5×10⁸ at L★ = 90 pc. V1 is a **different static
theory** from D7d in the non-spherical (EFE) sector.

## 3. Local predictions on both footings (V1 = AeST + β_L term, at the minimal physical curl stiffness; V0 = pure AeST)

| test | V1 at L★ = 24 / 50 / 90 pc | V0 (pure AeST, screened law) |
|---|---|---|
| Cassini Q₂ (s⁻², E0–E3) | canonical 1.18–2.35e-34 / 1.31–2.59e-35 / 2.25–4.45e-36; alt 1.05–1.94e-34 / 1.16–2.14e-35 / 1.99–3.67e-36. **PASS** Hees and Park by 2.6e-8 down to 4e-10 of the line. V1/D7d = 1.021–1.027 (K6). | not solved. The case is decided by the monopole (next row). |
| inner-planet monopole | GM/L★² + GMμ²/2. Mars is 0.17 / 0.04 / 0.012 of its bound. | **FAIL**: u → a₀ near the Sun (spherical first integral). That is 6.7e4× (canonical) or 8.1e4× (alt) the Mars bound, and 1.1–1.6e4× at Earth and Saturn (K9; matches D7d to 4e-9). |
| wide binary 1.5 M☉, 20 kAU, γ_v − 1 | 8.09–8.12e-6 / 1.87e-6 / 5.79e-7 on both footings (K7). The mass-term part is 2.4e-15. **No DR4-visible boost.** | the unscreened law-first value (D2: 1.175 / 1.21) |
| outer globulars (E4 native estimator, isolated) | the spherical sector is identical, so L★_95 ≥ **28.853 / 29.123 pc** (K8 = E4 N1). The mass-term fraction at r_h is 7e-10. | L★ → 0: Δχ² = 25.4 / 28.0, so **excluded** |

## 4. L★ after this lane

L★ is **not derived**:
- Every AeST length is at least 36× the window top. The smallest is r_C(Sun), an outward onset.
- The relevant lengths (μ⁻¹, L_eq, L★_F) are at least 1.1–1.6×10⁴× the window top.
- No AeST constant fixes β_L.

In a covariant version, L★ is the coefficient of the one added term, β_L = (2 − K_B)L★²/2. That makes it a **new constant
of the covariant theory**. Its value is **FITTED**: the floor is 28.9 / 29.1 pc isolated, and per E1/E4 it is dominated by
Υ_V, spanning 20–42 pc.

## Two frozen fails (kept)

- **K5(b)** compared g = 1e8 with g → ∞ down to κ = 1e-3. There gκ²/2 = 50 is not asymptotic, so the clause was mis-specified.
  - A1 adds K5b, which uses the physical g. It agrees with χ∞ to 2.6e-10. K6 and K7 are scored at that g.
- **K10.** The smallest AeST length is 36.4× the window top, not the frozen 10³×.
  - No AeST length sits in the window, so the classification stands.
  - The threshold is unchanged.

## Input ledger

| input | class | source |
|---|---|---|
| SZ21 Eq. (5)/(6), μ, μ⁻¹ ≳ 1 Mpc, r_C | external theory input; record transcription, not on disk | `real_research/bridge1_aest_equations.md`; `typeII_known_limits_2026.py` |
| c_s² (arXiv:2109.13287 Eq. 30) | external theory input; used only for the L★_F bound, conditional on c_s ≤ c | `ppn_verify_transcription_2026.py:349` |
| a₀ footings | canonical FRAMEWORK-NATIVE (E1: clean to 3 %); alt ΛCDM-PROCESSED | D7d inputs |
| E0–E3 Galactic fields | as in D7b (survey-calibrated MW models) | D7b json |
| Hees 2014 / Park 2026 Q₂ | RAW parametrised-anomaly bounds | D7d / BOUNDS.md |
| globular σ, L_V, r_h | RAW; Υ_V = 1.6 is SURVEY-CALIBRATION (dominant, E1/E4) | CFG332 via E4 |
| law g_N = g²/(g + a₀), S(s) | FRAMEWORK-NATIVE | D7d, CFG691 |

No ΛCDM or standard-MOND machinery is used in any V1 or V0 verdict. The EFE recipe is not used.

## Found in the record (read-only)

- `real_research/AEST_MASS_SCALE_two_doors.md:59,74` and `THE_NEXT_CALCULATION_aest_quasistatic.md:22` say AeST's
  Solar-System limit is "QUMOND". The record's own SZ21 transcription (typeII F1, scalar_AQUAL_action) says it is the
  **two-field AQUAL-type** system Φ = Φ_N + φ, ∇·(J_Y∇φ) = ∇²Φ_N. That is not QUMOND.
- `AEST_MASS_SCALE_two_doors.md:11` names the authors of arXiv:2304.05134 as "Verwayen, Skordis, Złošnik".
  `typeII_known_limits_2026.py:31-32`, which was read from the source, says "Verwayen, Skordis & Boehm".
- The question's premise that μ gives "Newtonian-like behaviour at large distances" does not match the record's
  transcription, which says the behaviour is oscillatory (typeII F7).

## What this does not show

- No covariant well-posedness, stability or PPN check of V1 beyond linear order on FRW. The record's "AeST v9 PPN kill"
  (α₁ = −2(K_B + 2), CFG172 row N7) is untested here and also applies to V1. That belongs to C1/C2.
- No CMB, and no claim about what sets Q₀ or K₂.
- No nonlinear Cassini solve of V0. V0 has a finite-λ_s alternative (G renormalisation instead of the cap), but that
  changes the galactic law, and the law question is D7c's.
- V1's Cassini result is Route F (linear about the Galactic field). The globular floor is isolated. The EFE-aware floor
  is OPEN for both V1 and D7d, and the two now differ there through γ_F ≠ γ_L.
