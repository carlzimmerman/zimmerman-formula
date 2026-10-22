# C5_health: is the covariant screened theory healthy?

## Verdict: CONDITIONALLY HEALTHY — and only in C4's literal form

- **The Khronon + P parent survives, but only as C4 literally wrote it.** That form has BS's bare R (β = 0), no P kinetic
  term (η = 0) and BS's K(Q) dust.
  - It has no ghost and no gradient instability on any background tested where the frozen-coefficient (WKB) expansion
    is valid.
  - Only the 2 tensor modes propagate, at c.
  - P and the khronon scalar are instantaneous: they obey elliptic constraints.
  - The ω = 0 (linear-in-t) mode has **positive** energy at every k.
  - On FRW the dust has c_s² = 𝒦′/(Q𝒦″) = (Q̄−1)/Q̄. Growth is bounded by the Jeans rate.
- **The conditions it needs** (DERIVED or COMPUTED here):
  - γ_L > 0;
  - W convex, i.e. M_T, M_L ≥ 1 (equivalently 0 ≤ 1+J′ < 1 and 0 ≤ 1+J′+2YJ″ < 1). The record's W meets this at every
    field strength.
  - 𝒦″ > 0 and Q̄ ≥ 1, i.e. a positive dust charge I₀;
  - β = 0 and η = 0 **exactly**.
  - **Cost:** it is not subluminal in the cone sense. Its constraints propagate instantaneously. It passes criterion B
    (global time) and fails criterion A (v ≤ c).
- **A33 written covariantly (β > 0, η > 0) does not survive as a Khronon parent.**
  - **(i) η > 0 with BS's R (β = 0) is UNHEALTHY.** Wherever u ≠ 0, one scalar has
    ω² = −γ_L η u₀² cos²θ k⁴ (K = 1 units; matches the numerics to ratio 1.0). That is a gradient instability whose rate
    grows as k², so the initial-value problem is ill-posed (Hadamard).
    - u ≠ 0 means every galaxy, and the Solar System through the Galactic external field.
    - In the Solar System at k = 1/AU (L★ = 24 pc, η = γ) the rate is **83 /yr (canonical) and 95 /yr (alt)**.
    - Health needs the record's β > 2ηa₀²/K (round-2). It is confirmed as the exact boundary: the sign change sits at
      β = 1.48707e-19 = 2ηu₀² (rel 4e-18). That needs a (∇·n)² term, which BS's action lacks.
  - **(ii) β > 0 with BS's K(Q) dust is UNHEALTHY in an IR band.** For aH ≪ k ≪ μ_K, ω² = −β k²/(2+3β) (−0.1999 vs 0.2;
    −0.000499 vs 0.000499). This is the projectable-Hořava sign: the dust's lapse mass releases A68's lapse constraint.
    - At μ_K/H = 4.4e4 (μ⁻¹ = 100 kpc) the rate reaches 1.8e4 H (β = 1) and 900 H (β = 1e-3).
    - A rough window where both (i) and (ii) are tolerable is 2ηa₀²/K ≈ 6e-19 (η/γ) < β ≲ 1e-9. The upper end is an
      estimate from the rate ≈ 0.9 μ_K√(β/2) at two points, with rate ≤ H. It is not a check.
  - A33 with **no** K(Q) dust (μ_K = 0, its own Vlasov medium) stays the record's healthy EFT. H1, H2 and H7 reproduce
    A68 and round-2. But then the Khronon supplies nothing beyond A33.
- **AeST + γ_L (C1/C3) is CONDITIONALLY HEALTHY too, with two defects the Khronon form does not have.** It needs
  0 < K_B < 2, K₂ > 0 and λ_eff ≥ 0.
  - **(a) The ω = 0 mode has negative energy.** With the capped F, λ_eff = 𝒥′(0) = 0 at Y = 0 (vacuum and FRW). There
    the ω = 0 Jordan mode has energy
    E = −2k²(K₂Q₀² + k²)/(K₂Q₀⁴) < 0 at **every** k. SZ's own condition λ_s > 0 fails there.
    - The γ_L term confines E < 0 to k ≲ μ (≥ Mpc), as SZ describe.
  - **(b) The γ_L term gives an unbounded speed.** The scalar gets ω² ⊃ (2−K_B)L★²k⁴/(4K₂) with no k-dependent kinetic
    term, so the group speed is unbounded (no cone).
  - **Strong unscreened fields:** λ_L = (1+y)² − 1, so the scalar speed² grows as y² and the vector mass² as 1+y. Both
    diverge (C2's flag), but as heavy or fast modes, not ghosts. In screened systems λ_L = (1+x_e)² − 1 ≈ 4–12 and all
    is finite.
- **Which parent survives:** Khronon + P in C4's literal form. AeST + γ_L is second (ω = 0 negative-energy band, no cone).
  A33-as-Khronon (η > 0) does not survive with BS's R or with BS's dust.

## Item-by-item answers

1. **Linearisation (sympy, from scratch).**
   - The local quadratic matrix uses 10 fields (n, N_i, ζ, h₊, h×, δP_i) on frozen static backgrounds with u₀, g and
     angle θ.
     - It reproduces A68 exactly (H1): tensor ω² = k², transverse P ω² = (K+γ_Fk²)/η, scalar ω² = γ_Lk⁴/(K(2+3β)/β + ηk²).
   - FRW: scalar sector with K(Q). At μ_K = 0 it reproduces round-2's de Sitter action exactly (H2).
2. **DOF (H4; two routes agree on 12 rows).**

   | form | Minkowski | u₀ ≠ 0 |
   |---|---|---|
   | A33 | 5 (= A68) | 5 |
   | C4-literal (± BS dust) | 2 + ω = 0 pair | 2 + ω = 0 pair |
   | β = 0, η > 0 | 4 + ω = 0 pair | 5, one unstable |
   | β > 0, η = 0 | 3 | 3 |

3. **Kinetic and gradient conditions (A33 family).**
   - **No ghost:** β > 0 (on the 2+3β > 0 branch) and η > 0.
     - FRW kinetic matrix: diag[𝒦″(2+3β)a³/(2KN(2(2+3β)H²N² + β𝒦″)), aηk²/(2N)].
     - At β = 0: diag[𝒦″a³/(4H²KN³), aηk²/(2N)].
   - **No gradient instability or tachyon:** γ_L, γ_F ≥ 0 and M_T, M_L ≥ 1.
     - The closed form in the decoupling limit is Kin = diag(B/k² + η, η, η) and
       Pot = [[γ_Lk² + M_zz − 1, M_zx, 0], [M_zx, γ_Fk² + M_xx, 0], [0, 0, γ_Fk² + M_T]], with M = M_T I + (M_L − M_T)P̂P̂.
     - It matches the full roots to 2.2e-11 (H5).
   - **Principal (front) speeds:** tensor 1; scalar (γ_L/η)Δ; transverse γ_F/η. Subluminal iff η ≥ γ (round-2's Δ excess
     ≤ 3e-15 at η = γ).
4. **Strong fields.**
   - **J's growth outside BS's class gives no ghost and no gradient instability.**
     - Unscreened, it raises the P masses: M_T = 1+y, M_L = (1+y)². P becomes heavy and positive. Checked at y up to 1e8:
       312/312 WKB-valid points are healthy.
     - Screened (Solar System, NS), P sits at the Galactic value. Local g enters only through terms suppressed by g/k.
   - **The k⁴ mode exists only at β > 0, u₀ = 0, H = 0.**
     - ω²/k² = 1e-9 and 1e-7 at kL★ = 1e-4 and 1e-3.
     - It becomes a k² mode at u₀ ≠ 0 (0.536 at y = 1) and is gapped by 2BH² on de Sitter.
     - It is absent at β = 0.
   - **Strong coupling (W's cubic only):**
     - p_sc = K⁴/(9a₀²B^½α^{5/2}) = 7.5e-112 eV (IR regime);
     - p_sc = K²/(3a₀α^{3/2}) = 2.5e-68 eV (η regime; A69 has the same form with 8.485π);
     - H_native = 7.5e-34 eV. The mode is weakly coupled on all sub-Hubble scales (H8, both footings, 20/24/90 pc).
     - At γ_L → 0 the coupling diverges: the stiffness is what makes the theory perturbative.

## Checks: 7/10 PASS, exit 1 (three frozen FAILs kept)

- **Criteria were frozen first** (f002ce909a).
- **Execution history.** Execution 1 was aborted on a route-2 root-clustering bug. Execution 2 crashed on a key format
  error. Execution 3 was the first complete run (`*_RUN1.*`, 6/10). It had two code bugs, fixed afterwards:
  - H9's c_s² check was evaluated at β ≠ 0 after the Hd substitution;
  - H10's Krein signs were computed in double precision, which gave −6e-16 and −8e-9 at y ≥ 1e4.
  - No pass line was changed.
- **The three frozen FAILs:**
  - **H5 FAIL.** The closed form matches to 2.2e-11. But the frozen "dropped factor < 1e-6" line fails: g/k = 0.11 at
    the NS (weak-field expansion invalid at NS compactness), and 3.5e-6 at 90 pc, kL★ = 1e-3.
  - **H6 FAIL.** All 96 failing points have g/k ≥ 40.7: Solar System/NS backgrounds at kL★ ≤ 10³, where the frozen
    background is not local. All 312 points with g/k < 1 are healthy. This reading is post hoc.
  - **H9 FAIL (physics).**
    - β > 0 with dust gives a negative band squared speed.
    - At β = 0 the band value −4.8e-11 is the Jeans onset. There |ω²| ≤ 0.093 H² at Ω_K = 0.26, an illustrative
      background only.
- **Mutation.** `C5_MUTATE=1` sets ξ = 2 and flips SZ's K_B sign. It breaks H1, H2, H3 and H10 (3/10). Outputs are in
  `*_MUTATE.*`.
- **Run cost.** 204 s, 0.08 GB RSS, single thread, no downloads.

## Inputs

| input | class | source |
|---|---|---|
| SZ21 Minkowski action, dispersions, λ_s conditions | literature, **on disk** (outside the repo); transcription checked by H3 | `../_external_data/aest_papers_2026_10_22/src_2007.00082/newRMONDLett.tex` |
| BS action form, K(Q) = μ²(Q−1)², μ⁻¹ ≥ 100 kpc | literature via C4 (WebFetch, not on disk) | C4 README |
| A33 action, W, γ = KL★²/2 | FRAMEWORK-NATIVE | A33 `MASTER_ACTION.md` |
| x_e = 1.15–2.6 | FRAMEWORK-NATIVE | D7d json `R2_scan` |
| Ω_K = 0.26, H scale | illustrative background only (BS25's value); no verdict rests on it | — |
| a₀ footings | FITTED (κ = ½) | doors BRIEF |

## What this does not show

- It is linear (frozen-coefficient) analysis only. There is no nonlinear well-posedness and no full Hamiltonian count
  for C4-literal; the ω = 0 pair is read from det M.
- NS-compactness backgrounds are outside the weak-field expansion.
- The strong-coupling estimate uses W's cubic only. Gravity and clock vertices are not included.
- AeST strong-field values are frozen extrapolations in the aligned direction only.
- Whether C4-literal (γ_F = 0, η = 0) still passes Cassini/EFE is not computed. D7d used γ_F = γ_L. Adding γ_F at η = 0
  keeps P non-dynamical, so health is unchanged by structure.

κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the
framework.
