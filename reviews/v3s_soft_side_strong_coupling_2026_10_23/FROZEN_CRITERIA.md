# v3s soft side: is the D·P < 0 region strongly coupled? — FROZEN CRITERIA (before any script or number)

Context: the owner adopted **v3s** (`591ec436be`): v3 with the switched stiffness −(γ_L/2)[max(D·P, 0)]². X3's
qualifier 4 says that on the D·P < 0 ("soft") side "the pair has no gradient term (c_π = 0), so P3's estimate gives
Λ = 0", and that "whether that matters needs a non-relativistic (dust-like) strong-coupling analysis, which is not done
here" (X3 README L28, L186–188). This lane does that analysis. Inputs read-only: X3 README, H4's committed
`h4_v3_saddle_stability_results.json` (regions), P3's hashed `scales()` (sha256 1aaf59ad…cb67bb6d). κ = ½ FITTED; both
footings, never pooled. No dark-matter particle. Not theory closed. Small, one thread, nice 15. Owner's standing
instruction: "keep swinging on the hardest problems".

## What I worked out by hand before freezing (stated so it cannot steer)

- On the soft side γ_L is off, so P is eliminated algebraically: P·∇Ξ − W → the Legendre dual 𝒥 of W. That is BS's
  J term (C4 K3). With v = −∇σ (curl-free) the identity ∇Ξ = v̇ + (v·∇)v + ∇φ holds, so the soft-side khronon is a
  fluid whose Lagrangian is the squared material acceleration relative to gravity,
  `L_soft = (1/2K)(Dv/Dt + ∇φ)·M⁻¹·(Dv/Dt + ∇φ) − ρ_τ Ξ + μ_K²Ξ²/(2K) + …`.
  Its linear mode is dispersionless: ω² = Kρ_τ(M_θ − 1), H4's bounded branch.
- **It has no k² term, but its frequency is not zero.** For a z = 0 field the power counting is: canonical
  v_c = v/√(KM); convective cubic √(KM) v̇_c·(v_c·∇)v_c; fluctuation v_c² ~ k³/ω. That gives the loop parameter
  **ε_NR(k) = K M k⁵/ω³** (ħ = c = 1, K = 4π l_P²). P3's own formula with the k-dependent c_π(k) = √(G/Z) = ω/k (Z =
  k²/(KM)) gives ε_P3 = KMk⁵/(4ω³), the same up to P3's V1 convention (c_zz/2). Expectation: X3's "Λ = 0" comes from
  inserting c_π = 0 (the k → ∞ limit) into a relativistic scaling formula, and the soft side has a finite strong-coupling
  length ℓ_sc = 2π (4ω³/KM)^(−1/5) ~ 10²–10³ m at H4's saddle depths. On astrophysical scales that is weakly coupled.

## Checks (`soft_side_sc.py`; `--mutate` = X3's reading, c_π ≡ 0 inserted into P3's formula)

- **N1 (structure, sympy).** (i) For v = −∇σ in 3D with generic functions: ∇(−σ̇ + ½|∇σ|²) − (v̇ + (v·∇)v) = 0. (ii) The
  Legendre transform of P·a − W(K|P|) at γ_L = 0 equals BS's −J_x(|a|²)/(2K) up to the sign convention C4 K3 uses
  (residual 0; C4's identity, re-derived). (iii) The expansion of (1/2K)(Dv/Dt)·M⁻¹·(Dv/Dt) to cubic order gives
  quadratic (1/2KM)|v̇|² and cubic (1/KM) v̇·(v·∇)v for isotropic M. PASS iff all residuals are 0.
- **N2 (power counting, sympy).** ε_NR = KMk⁵/ω³ is dimensionless in ħ = c = 1, and ε_P3(c_π = ω/k) / ε_NR = 1/4 exactly,
  with P3's V1 coefficient taken from P3's committed c_zz. PASS iff both hold.
- **N3 (H4's regions, both footings).** For every H4 region record (f0 and f3, base and fine, box and near; median and
  max |ρ_τ| with their x), with M_θ = M_T = 1 + x (conservative: smallest M − 1):
  - Γ = √(K|ρ_τ|(M_θ − 1)) (with self-gravity), and Γ_dec = √(K|ρ_τ|M_θ) as the bracket;
  - k_sc from ε_P3 = 1 (P3's convention) and from ε_NR = 1; ℓ_sc = 2π/k_sc;
  - a variant with ω = max(Γ, H₀).
  **PASS ("benign") iff ℓ_sc ≤ 1 pc in every region at the conservative Γ.** Readings: all ≤ 1 pc ⇒ "the soft side is
  weakly coupled on every astrophysical scale; X3's qualifier 4 is a scaling artifact"; any region ≥ 1 kpc ⇒ "galactic-
  scale strong coupling: v3s is not an EFT in saddles"; otherwise reported as INTERMEDIATE with the regions named.
- **N4 (approach to the null and to the interface).** ℓ_sc as a function of x at the region densities, and as a function
  of |ρ_τ| → 0 (the interface). Reported: the x and |ρ_τ| below which ℓ_sc exceeds 1 pc and 1 kpc, compared with X3's
  stiff-side interface layer (7 m–1.1 km at ρ_τ = 1e-9 × depth). No threshold.
- **N5 (other soft-side vertices).** The 𝒥‴ cubic (v̇³, coefficient from J_x's third derivative) and the K(Q) dust cubic
  (P3's V5), at the same (k, ω): reported as ratios to the convective vertex's ε. PASS iff both are ≤ ε_conv at k_sc in
  every N3 region (the convective vertex sets the scale).
- **MUTATE (X3's reading).** c_π ≡ 0 inserted into P3's relativistic formula: required Λ = 0 and ε = ∞ at every k (the
  check distinguishes the readings).

Not tested: classical (large-amplitude) nonlinearity of actual khronon flows in saddles (needs the khronon velocity
field), 3D evolution, the interface's moving-boundary problem, the DBI K, and anything beyond one-loop power counting.
