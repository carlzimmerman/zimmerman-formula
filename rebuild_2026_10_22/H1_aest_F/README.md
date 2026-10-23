# H1_aest_F: is there an AeST free function F(Y, Q) that is healthy at Y = 0, grows structure, gives the law, keeps Cassini and passes BBN?

## Verdict: NONE IN THE FAMILY

**No family member passes.** No member of SZ's own family, and no member of the record's capped interpolants, passes
all five conditions. Two conflicts decide it.

**Conflict 1: (i) health at Y = 0 against (iii) the MOND limit.**
- Health at Y = 0 sees F only through one number, λ₀ = F_Y(0, Q₀)/(2−K_B). K3 shows why: Y is O(ε²) on the Y = 0
  background, so every term beyond linear in Y is cubic.
- SZ's condition λ_s > 0 needs λ₀ > 0.
- The MOND limit (SZ eq. `Jcal_MOND`; VSZ eq. `def_f_general`, f → x/(1+β₀)) sets λ₀ = 0 for every member. That
  includes SZ's own CMB "MOND models", and SZ say so themselves: ∂F/∂Y "is zero in the MOND limit".
- So C5's negative-energy defect is not specific to C1's capped F. **Every MOND-limit F in AeST's class has it.**

**Conflict 2: (iii) against (v) for SZ's own interpolants.**
- BBN needs λ_s ≥ 24.7. At that value, SZ's simple, exponential and sharp functions are f ≈ x across the whole SPARC range.
  That is the slow transition ν ≈ 1 + y^−½.
- They lose to the canonical law:
  - canonical footing: z = −2.37 to −2.74, S1 = +318 to +413;
  - alt footing: z = −2.78 to −3.64, S1 = +697 to +806.
- Only the capped boundary (λ_s = ∞ with a cap) gives the law:
  - cap-n1 is the canonical law exactly;
  - cap-n2 is the n = 2 law.
- Both caps pass (ii), (iii), (iv) and (v). They fail only (i).

**The structural result: the negative-energy mode is the growth mode (theorem T1, COMPUTED by sympy, K2).**
- In a Jeans-swindle background of AeST dust, the ω = 0 Jordan-mode energy and the dust growth rate obey
  E_J/Γ² = −8k²D²/(I Q̄³ N²) < 0 exactly, with and without γ_L. So E_J < 0 exactly where the dust grows.
- Hence "no negative-energy mode at any k" means "the dust grows at no k". **(i)-strict and (ii) are incompatible for
  every F in AeST's class.**
- What SZ's λ_s > 0 actually does is end the band at k_c = μ√(1+1/λ₀). SZ call the band "Jeans-type".
- The γ_L term ends it too. For the screened theory (cap-n1 + γ_L) the band ends at k_c = 242 Mpc⁻¹ ≈ 1/(4.1 kpc)
  (μ⁻¹ = 1 Mpc, L★ = 24 pc). Without γ_L it never ends.

**A door outside the family, at the cost of one POSTULATED constant.**
- The door is a floor, f = λ₀ + x/(1−x). It passes all five at every declared λ₀ ∈ {1e-3, 1e-2, 1e-1}.
- No λ₀ was fitted. Its only job is to satisfy SZ's literal λ_s > 0.
- It does not remove the band. It moves k_c to 31.6, 10 and 3.3 Mpc⁻¹.
- It changes the far field. Beyond r = r_M/λ₀ the law turns Newtonian with G×(1+1/λ₀), so it falls as 1/r² and no
  longer flattens. For 10¹¹ M☉ that radius is 12 Mpc, 1.2 Mpc and 120 kpc (canonical).
  - At λ₀ = 0.1 this would cut the outer lensing that lane F2 already finds short. That is the direction only; it was
    not computed against lensing data.

κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework.

## Scorecard (graded lines from FROZEN_CRITERIA §2; both footings)

| F | in family | (i) λ₀ > 0 | (ii) growth | (iii) z vs canonical (can / alt) | (iv) max Q₂/Park | (v) λ_s ≥ 24.7 |
|---|---|---|---|---|---|---|
| SZ-simple, λ_s = 24.7 | yes | F | P | F (−2.74 / −3.22) | 1.0e-8 P | P |
| SZ-exp, λ_s = 24.7 | yes | F | P | F (−2.37 / −3.41) | 1.0e-8 P | P |
| SZ-sharp, λ_s = 24.7 | yes | F | P | F (−2.46 / −2.78) | 1.1e-8 P | P |
| SZ-∞ (f = x) | yes | F | P | F (−2.74 / −3.64) | 1.1e-8 P | P |
| cap-n1 (C1, μ = x/(1+x)) | boundary | F | P | P (0 / 0, identical) | 3.6e-8 P | P |
| cap-n2 (n = 2) | boundary | F | P | P (+0.24 / +2.52) | 7.0e-8 P | P |
| door λ₀ = 1e-3 | **outside, +1** | P | P | P (+1.47 / +3.36) | 3.6e-8 P | P |
| door λ₀ = 1e-2 | **outside, +1** | P | P | P (+1.20 / +2.61) | 3.6e-8 P | P |
| door λ₀ = 1e-1 | **outside, +1** | P | P | P (−0.72 / +1.31) | 3.5e-8 P | P |

**SPARC numbers, as asked.** S1 is Σ Δχ²_min; per-galaxy MAP Υ; AG4b pipeline.

| F | canonical footing: vs canonical z, S1 | canonical footing: vs ν_RAR z, S1 | alt footing: vs canonical z, S1 | alt footing: vs ν_RAR z, S1 |
|---|---|---|---|---|
| canonical law itself (yardstick) | — | −3.31, +70.0 | — | −4.77, +54.3 |
| SZ-simple | −2.74, +366 | −3.74, +436 | −3.22, +752 | −4.38, +806 |
| SZ-exp | −2.37, +342 | −3.52, +412 | −3.41, +724 | −4.18, +778 |
| SZ-sharp | −2.46, +319 | −3.34, +389 | −2.78, +697 | −4.14, +751 |
| SZ-∞ | −2.74, +413 | −3.64, +483 | −3.64, +806 | −4.34, +860 |
| cap-n1 | 0, 0 | −3.31, +70.0 | 0, 0 | −4.77, +54.3 |
| cap-n2 | +0.24, +711 | +0.21, +781 | +2.52, +120 | +2.01, +174 |
| door 1e-3 | +1.47, −4.8 | −1.80, +65.2 | +3.36, −14.0 | +0.13, +40.3 |
| door 1e-2 | +1.20, −40.5 | +0.57, +29.5 | +2.61, −130 | +1.99, −76.1 |
| door 1e-1 | −0.72, +233 | −0.93, +303 | +1.31, −383 | +0.92, −329 |

How to read the SPARC tables:
- The paired median-rms z magnifies tiny shifts. The door at 1e-3 moves the median by only about 1e-5 dex, yet scores
  z = +3.36 (D7c's caveat). Read it as "consistent", not "preferred".
- ν_RAR is a reference shape, not a law. The canonical law itself sits at z = −3.3 / −4.8 against it.

**Growth (ii).**
- **COMPUTED:** Γ²(k → 0) = 4πG̃ρ̄ for every λ₀ (K2). In AeST the Newtonian term survives in the IR for any F.
  - So the AeST counterpart of F3's J′(0) criterion is not λ₀ = 0.
  - F changes growth only at k ≳ μ/√λ₀.
- The door's shift at k ≤ 0.3 h/Mpc (μ⁻¹ = 1 Mpc) is 1.7e-6, 1.7e-5 and 1.6e-4 for λ₀ = 1e-3, 1e-2 and 1e-1.
  - At μ⁻¹ = 10 Mpc (reported only) the shift is 3.4e-3 at λ₀ = 1e-3 and 0.33 at λ₀ = 0.1.
- **Side result (F-independent, reported only).** AeST's own dust growth is suppressed above μ:
  Γ²/Γ²_GR = 1/(1 + 2k²/((2−K_B)μ²)).
  - At 0.3 h/Mpc this is 0.959 for μ⁻¹ = 1 Mpc and 0.190 for μ⁻¹ = 10 Mpc.
  - It has the same form as C7's small-scale P(k) suppression "set by K₂".
  - It sharpens SZ's μ⁻¹ ≳ 1 Mpc into a window bounded from both sides.

**Solar System (iv).**
- C6's Route F was rerun with each F's own response tensor at the Milky Way field.
- Q₂ is at most 7e-8 of Park's bound, and M_T, M_L ≥ 1.74.
- The planets' hedgehog GM/L★² does not depend on F, so C6's values carry over: Mars 0.173 of its bound at 24 pc.

## Checks: 6/6 PASS, exit 0 (8.6 s, 0.29 GB, one thread)

| check | what it shows |
|---|---|
| K1 | C5's AeST Jordan energies are reproduced from C5's own source, which was exec'd read-only (difference 0) |
| K2 | T1 holds: the ratio is −8 with and without γ_L. Γ²(0) = IQ̄/2 = 4πG̃ρ̄. The closed form has residual 0 |
| K3 | Y⁽⁰⁾ = Y⁽¹⁾ = 0 and Y⁽²⁾ = \|∇φ + Q̄A\|² |
| K4 | cap-n1 = ν₁ and cap-n2 = √(1+1/y) to 1e-15. The table matches the direct solve to 7.9e-10. The limits are right |
| K5 | AG4b is reproduced exactly (z +0.2402 / +2.5222) |
| K6 | C6's I₂ and Q₂ are reproduced exactly |

**History and files.**
- Criteria were frozen first (a4d76f492e).
- Run 1 (`*_RUN1.*`) scored 5/6. K4 failed on table round-off (1.8e-8). The same round-off gave cap-n1 a spurious
  z = −3.50 against itself, with d = 0.0000 dex.
- AMENDMENT A1 (post-result) made the table denser and scores exact-identity members with their closed form. No pass
  line changed.
- `H1_MUTATE=1` flips the dust term's sign and uses x/(1+x) for the cap. K2 and K4 then fail (4/6, exit 1; `*_MUTATE.*`).
- Run: `OMP_NUM_THREADS=1 nice -n 15 python3 h1_aest_f.py`.

## Constants counted

- SZ's family carries two F constants: a₀ (both footings, FITTED) and λ_s (declared at 24.7 and ∞ only).
- The caps carry a₀ only. K_B, K₂ and Q₀ (μ) belong to AeST and are not fixed by F.
- The door adds λ₀ (POSTULATED, +1).

## Errors found in the record (not edited)

- `covariant_push_2026_10_22/C5_health/README.md` L41 says the γ_L term "confines E < 0 to k ≲ μ (≥ Mpc)". In fact the
  band ends at k_c ≈ (2μ²/L★²)^¼: 242 Mpc⁻¹ ≈ 1/(4.1 kpc) at μ⁻¹ = 1 Mpc and L★ = 24 pc. That is far inside μ⁻¹.
- C5's defect (a) is read as a pathology of the capped F. It is the dust's Jeans growth mode (T1), and every
  MOND-limit F shares it.

## What this does not show

- **Growth is a Jeans swindle.** It uses Minkowski plus a dust density, with no Hubble friction and only k ≫ aH. The full
  λ₀ ≠ 0 FRW run would need C7's patched CLASS with λ_c ≠ 0 (C7 names the extra E-equation term).
- **Health is linear only.** It covers the Y = 0 background. It is not a Hamiltonian count.
- **The SPARC law is the algebraic per-point form.** That is exact for spherical AQUAL and approximate in discs; every
  law is treated the same way. The μ term is neglected at SPARC radii.
- **No new data.**
