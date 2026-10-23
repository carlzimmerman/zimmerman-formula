# v3s soft side: is the D·P < 0 region strongly coupled? — RESULT

Criteria `FROZEN_CRITERIA.md`, committed `a7649df81b` before any script. Owner's standing instruction: "keep swinging on
the hardest problems". This is the open item X3 named for the adopted theory v3s (`591ec436be`). κ = ½ FITTED; both
footings, never pooled. No dark-matter particle. Not theory closed.

## Verdict: BENIGN — the soft side is weakly coupled on every astrophysical scale; "Λ = 0" was a scaling artifact

1. **What the soft side is (N1, sympy, residuals 0).**
   - With γ_L switched off, P is eliminated algebraically. Its Legendre transform is BS's −(J_x − Λ)/(2K) (C4 K3,
     re-derived).
   - For v = −∇σ, the identity ∇Ξ = v̇ + (v·∇)v holds exactly. So the soft-side khronon is a fluid whose Lagrangian is
     its **squared material acceleration relative to gravity**: (1/2K)(Dv/Dt + ∇φ)·M⁻¹·(Dv/Dt + ∇φ) − ρ_τΞ + ….
   - The expansion gives the quadratic (1/2KM)|v̇|² and the convective cubic (1/KM) v̇·(v·∇)v.
   - The linear mode is dispersionless, ω² = Kρ_τ(M_θ − 1) (H4's bounded branch). It has no k² term (X3's "c_π = 0"),
     but its frequency is not zero.
2. **Power counting for a z = 0 field (N2).**
   - Canonical v_c = v/√(KM), vertex √(KM) v̇_c·(v_c·∇)v_c, fluctuation v_c² ~ k³/ω. This gives the dimensionless loop
     parameter **ε = KMk⁵/ω³** (ħ = c = 1, K = 4πl_P²).
   - **P3's own formula gives exactly ¼ of this** when it is fed the soft side's k-dependent c_π(k) = √(G/Z) = ω/k, with
     Z = k²/(KM); the ¼ is P3's V1 convention c_zz/2, squared. P3's hashed `scales()` reproduces KMk⁵/(4ω³) to 1e-9
     at a dispersionless test point.
   - X3's "Λ = 0" came from inserting the k → ∞ limit c_π = 0 into the relativistic scaling Λ² = Z^(3/2)c^(7/2)/λ. That
     formula is not meant for a flat dispersion. MUTATE, which does exactly that, gives Λ = 0 and ℓ = ∞ everywhere.
3. **H4's regions, both footings (N3).** Over all 320 region values (f0/f3, base/fine, box/near, median and max |ρ_τ|),
   with the conservative rate Γ = √(K|ρ_τ|(M_θ − 1)) and M_θ = 1 + x:
   - the strong-coupling length is **ℓ_sc = 57 m to 54 km** (canonical 57 m–54 km, alt 57 m–49 km);
   - the worst case is the cluster-pair lobes at |ρ_τ| = 7e-32 kg/m³;
   - the decoupled bracket gives ≤ 13.5 km, and with ω ≥ H₀ ≤ 0.46 km;
   - the benign line was 1 pc (3.1e16 m). The soft side's EFT holds on all scales above ~10–10⁴ m, so it covers
     every galactic and cosmological process in the saddles and lobes.
4. **Approach to the null and to the interface (N4, reported).** At the median region (|ρ_τ| 6e-27 kg/m³, x 0.01),
   ℓ_sc = 1.8 km. ℓ_sc ∝ (|ρ_τ| x)^(−3/10) grows only slowly. It stays below 1 pc for every x ≥ 1e-40 and every
   |ρ_τ| ≥ 5e-71 kg/m³ (the bisection floors; 1 kpc is never reached in the scanned range). At 1e-9 of the region depth,
   ℓ_sc = 910 km, the same kind of thin layer as X3's stiff-side interface layer (7 m–1.1 km).
   - *Estimate, not gated:* near a non-degenerate field null, x grows linearly with the distance r. The EFT then fails
     only where ℓ_sc(x(r)) > r, which for a region gradient scale of 100 kpc is r ≲ 10⁴ km. The strongly coupled cores
     are planet-sized points inside Mpc-sized lobes.
5. **The convective vertex sets the scale (N5).** At k_sc in every region, the 𝒥‴ cubic (from J_x's third derivative)
   is ≤ 4e-43 of the convective ε, and the K(Q) dust cubic (P3's V5) ≤ 6e-71.

**So X3's qualifier 4 resolves in v3s's favour.** The switch removes the Hadamard instability. The price is not loss
of EFT control in saddles. It is a soft-side fluid that is weakly coupled down to ~km scales, with ≤ 10⁴ km cores at field
nulls and thin layers at the interface. X3's other qualifiers are unchanged: dust ≥ −D·P on the stiff side, the knife
edge at zero dust (sign-consistent numerics), and H4's bounded growth (≤ 0.20 e-folds median).

## Checks

| run | result |
|---|---|
| run 1 (`soft_side_sc_RUN1_crash.out`) | N1–N3 printed and PASS, then N4 crashed. Cause: M − 1 computed as (1 + x) − 1 underflows at x = 1e-40 in the bisection. Fixed by using x directly; N3's values (x ≥ 1e-3) are unchanged to 1e-13 |
| run 2 (`soft_side_sc.out`, `soft_side_sc_results.json`) | **5/5 PASS** |
| MUTATE (`soft_side_sc_MUTATE.out`) | X3's reading, c_π ≡ 0: ℓ = ∞, N3 FAIL, exit 1, as required |

Under 1 s, one thread, nice 15.

## What this does not do

- It does not test classical large-amplitude nonlinearity of actual khronon flows in saddles; that needs the khronon
  velocity field, and ε_cl = k|v|/ω could be O(1) for bulk flows at Mpc scales. It is a separate, open question.
- It does not cover 3D evolution, the moving interface, the DBI K, or anything beyond one-loop power counting with
  O(1) factors (P3's convention).
- The null-core size in item 4 is an estimate.
