# ZT11_zstar_cherenkov: frozen criteria (written before any script or number of this lane)

Test frozen in `rebuild_2026_10_22/Z1_successor_design/TEST_PLAN.md` (0d1959a4f5), "Z-T11 (Cherenkov)":
emission of the khronon/dust pair by a mass moving at v > c_pair. **PASS**: energy-loss time > 10 Hubble times for the
Sun and for MW disc stars at L★ = 24 and 90 pc. Design: Z★ = v3s-OC (`Z1_successor_design/DESIGN.md`).
κ = ½ FITTED. Footings a₀ = 9.3603e-11 / 1.1312e-10 m/s², scored separately, never pooled. No dark-matter particle (the
cold sector is one pressureless medium, a field). Not "theory closed".

## 1. Physics implementation (choices fixed here)

**I1. The pair is the held medium's sound mode (derived, not assumed).** Use the record's PN Lagrangian of v3/v3s
(`X3_switched_stiffness/x3_switched_stiffness.py`, block B2-S, "L1"), generalised to 3D, with μ_K = 0 because Z★ removes
K(Q) (DESIGN §3):

    L = −|∇φ|²/(2K) − ρ_m φ + P·∇Ξ − W(K|P|) − (γ_L/2)[max(∇·P, 0)]²,   Ξ = φ − σ̇ + |∇σ|²/2,   K = 4πG.

Matter enters only through φ (S_m[g, matter], minimal coupling; V3_FULL_PICTURE eq. at line 23). By parts P·∇Ξ = −ρ_τΞ
with ρ_τ = ∇·P (= D·P). The script derives with sympy, on the stiff side (D·P > 0, where the held medium sits):
- the linear dispersion about a uniform held density ρ₀ with longitudinal W-stiffness M (M_θ in X3):
  ω² = Kρ₀(M − 1) + γ_Lρ₀k² (self-gravity included). Sound speed c_s² = γ_Lρ₀, gap ω_g² = Kρ₀(M − 1).
- the forced equation for a moving point mass M★: δρ̈ − c_s²∇²δρ + ω_g²δρ = Kρ₀M★δ³(x − vt) (source through φ only).
- P3's decoupled pair (G = D·P, Z = k²/(K M_L + γ_L k²) at μ_K = 0) is the same mode without self-gravity:
  G k²/Z − ω²(I1) = Kρ₀ exactly.
- the static response of the medium (linearised statics) gives the effective coupling of a point mass to the medium at
  wavenumber k: G_eff(k)/G = (M + L★²k²/2)/(M − 1 + L★²k²/2). At M = 1 this must equal X15's U_N = KM(L★²k²+2)/(L★²k⁴).
  So inside the screening length (kL★ ≫ 1) the coupling is exactly Newtonian; beyond it the enhancement is bounded by
  M/(M − 1).

**I2. Cherenkov loss (independent derivation, Ostriker-type linear response).** From the retarded solution of I1's forced
equation, the drag force on the source is derived with sympy (angular δ-integral done analytically):

    F = (K² M★² ρ₀ / (4π v²)) ∫_{k_min}^{k_max} (dk/k) g(k)²,   K²/(4π) = 4πG²,

for v > c_s, with k_min = ω_g/√(v² − c_s²) (Cherenkov condition ω_k < kv), and g(k) the coupling factor.
dE/dt = F v; t_loss = (½M★v²)/(F v) = v³ / (8π G² M★ ρ₀ ln Λ_eff), ln Λ_eff = ∫(dk/k) g².
- **Verdict envelope (conservative):** g(k)² = [G_eff(k)/G]² with M = M_T = 1 + x (the smallest W-stiffness, which
  gives the largest coupling and the smallest gap), and k_max = 1/R★ (stellar radius: the largest log).
- Also reported (no verdict weight): g = 1 (pure screened coupling), k_max = 1/r_acc (r_acc = 2GM★/v²) and
  k_max = 1/r_nl (where the star's screened hedgehog density M★/(2πL★²r) equals ρ₀, the nonlinear core).
- If v ≤ c_s: no Cherenkov emission (t_loss = ∞).

**I3. The medium.** ρ₀ = local held density = the law's phantom density in the MW owner (Z★: held dust = phantom where
supply ≥ demand, DESIGN §4). Computed as ρ_dyn − ρ_b at the star's (R, z = 0) from S3's cached isolated AQUAL solve of
the McMillan17 baryons (S3 `s3_mw.py` key "main|<foot>|s1.000000|eN0.000000|", read-only from
`S3_v3_mw_seals/_cache_final`, via `Grid.lap_density`). If the cached file is absent the script STOPS (it never solves
or writes into S3). x = g/a₀ at the star from the same solve's in-plane v_c (v_c²/R).
Sensitivity (reported): ρ₀ × 10 (a free-dust surplus or a denser held column).

**I4. The bodies and speeds (owner frame = MW free-fall frame, non-rotating).**
- Sun: M★ = 1 M☉, R★ = R☉, at R₀ = 8.122 kpc, v ∈ {230, 250} km/s.
- Disc stars: R ∈ {4, 6, 8.122, 12, 16} kpc, v = v_c(R) from the same solve per footing, M★ ∈ {1, 20} M☉ with
  R★ = R☉ (M★/M☉)^0.8 (POSITED main-sequence scaling; enters only the log).
- L★ ∈ {24, 90} pc; γ_L = K L★²/2.

**I5. The pair speed reported.** c_s (galactic held medium) per row; plus the Sun's own screened neighbourhood:
v3s (no cap) c_π(r) = √(GM☉/r) (P3's hedgehog, μ_K dropped), and Z★ with R1's cap D·P ≤ ρ_d (ρ_d = ρ₀):
c_π = √(γ_L ρ₀) beyond r_nl.

**Hubble time.** t_H = 1/H₀ with H₀ = 67.4 km/s/Mpc (EXTERNALLY CALIBRATED; the native refits 67.2–68.6 move it < 2 %).

## 2. Verdict rule (from TEST_PLAN, made operational)

- **PASS**: t_loss(envelope) > 10 t_H in every row (Sun at 230 and 250 km/s; all disc-star rows), both L★, both footings.
- **FAIL**: t_loss(envelope) < 10 t_H in any row in which t_loss(g = 1, k_max = 1/r_acc) is also < 10 t_H.
- **UNDECIDED**: otherwise (envelope fails only through the conservative choices), or if a needed ingredient is underived.

## 3. Checks (`K*`, exit 0 iff all pass)

- **K1** P3 reproduction: c_π = √(G/Z) with μ_K terms dropped reproduces P3's JSON `E4` c_pi for "planets (1 AU)" and
  "Eot-Wash (38.6 um)", both footings, L★ 24 and 90 pc, within 1e-3 relative (≈1e-4 c).
- **K2** sympy: I1's linear dispersion from the 3D PN Lagrangian equals X3's B1-S `omega2_P` (its JSON string) at μ_K = 0,
  θ = 0 (longitudinal, M_θ = M_L): residual 0.
- **K3** sympy: P3's decoupled G k²/Z (μ_K = 0) minus I1's ω² = Kρ₀ (residual 0).
- **K4** sympy: the angular Cherenkov integral equals 1/(k²v²) for ω_k < kv, and the prefactor reduces to 4πG²M★²ρ₀/v²
  (residual 0); plus a numeric check of the δ-integral with a narrow Gaussian (rel. error < 1e-3).
- **K5** sympy: G_eff(k)/G from the linear statics; at M = 1 equals X15's U_N/(KM/k²) (residual 0); limits 1 (kL★→∞) and
  M/(M − 1) (k → 0).
- **K6** dimensional check: t_loss in SI units, via sympy.physics.units (result has dimension of time).
- **K7** MW input: the cached solve's v_c(R₀) within 1 % of the record (X5 step 0, P4 B1 F0 L★ 24 pc: 215.170 / 220.377
  km/s), and the phantom density at (R₀, 0) is > 0.
- **K8** Ostriker cross-check: in the massless limit (ω_g → 0) and M = 1 (g = 1), the numerical k-integral of I2
  reproduces 4πG²M²ρ₀ lnΛ/v² with lnΛ = ln(k_max/k_min) to 1e-6.

**`--mutate`** (env `ZT11_MUTATE=1` or flag): the sound speed is set to c_s² = 2γ_Lρ₀ and P3's G to 2 D·P (a factor-2
normalisation error). K1 and K3 must FAIL. Outputs `zt11_cherenkov_MUTATE.out`, `zt11_cherenkov_results_MUTATE.json`.

## 4. Compute and style

`OMP_NUM_THREADS=1 nice -n 15 python3`, one process, < 1 GB RSS, minutes; no solves, no downloads; reads S3's cache
read-only. Post-result changes go in a dated AMENDMENT file. No personal names or home paths in committed files.
