# WT-08 FROZEN CRITERIA: a repaired parent CFG938′ (intrinsic leaf Laplacian + explicit mean density)

Lane WT-08 of `what_is_time/` (owner, 2026-10-21: "what is time in my framework?", then "figure it out from first principles").
Written 2026-10-21, before any script or number of this lane. κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s²
(CFG4_common) are scored separately and never pooled. Z = 5.7888. Cold energy is real gravitating mass; no particle species is
added. Framework-native quantities only. Not "theory closed". Nothing here says the data favour the framework. Anything true by
construction is flagged and carries no verdict weight. Parallel lanes: WT-07 (forced time structure), WT-09 (stiffness terms
with c_T = c); this lane does not edit, run or stage their files, nor CFG960/CFG961/WT-06.

## 0. Question

WT-02 found that CFG938's parent is Hadamard ill-posed off static backgrounds: its constraint uses
D²χ ≡ h^{μν}∇_μ∇_νχ = ³Δχ − θ u·∂χ, and the θ term (θ = 3H on FRW), which CFG938's S1d uses to absorb ρ̄, makes (χ, λ) a
forward/backward heat pair (Re σ = c²k²/3H). Build the repaired parent whose constraint uses only the intrinsic leaf Laplacian
(no derivative along u) with an explicit mean-density treatment, and run one battery on it: is it well posed, and does it still
give the law?

## 1. Inputs (read only)

| input | file | commit |
|---|---|---|
| parent action, S1d, S3a/S3b, S4 slip, S5a dispersion, S5c inertia, S6 | `campaign_fresh_gravity/CFG938_medium_continuum_eft/` | 92606e049b (criteria 7a0d41e8b) |
| the defect, FRW machinery, MU3, D1–D3, E1 (c_T), A1.2 observable bounds | `what_is_time/WT-02_preferred_time/` | 9b3d77382a (criteria b85749d1c) |
| orchestrator's independent check (read only; its expected clock term in c_T) | `campaign_fresh_gravity/CFG961_wt02_verification/FROZEN_CRITERIA.md` | 83b04219e2 |
| theorem D-T; the χ̄-boost correction, growth exponents 0.69433 / 0.60954 (EdS, Ω_c/Ω_b = 5.364) | `campaign_fresh_gravity/CFG941_self_gravity_repair/` | c85e14a0d2 |
| repairs already tried (gated tether, hover, option 2, option 3) | `campaign_fresh_gravity/CFG944_…`, `CFG945_…`, `CFG946_…`, `CFG947_…` | bebfe0471e; …; 59da0f0166 |
| metric variation of the intrinsic Laplacian, δΔ_h u = −k^{ij}D_iD_ju − (D_ik^{ij} − ½D^j tr k)D_ju (astra; read, cited, not edited) | `deepseek_push/astra_spawn_ideas/results/AS206/AS206-r1-20260928T170619Z-dsv4f-hermes/derivation.md` | e6d9add5cd |
| record precedent for leaf-mean subtraction (−c₂(K − ⟨K⟩)², ⟨θ⟩; khronon charge Q ≡ 0 rule) | `campaign_fresh_gravity/CFG172D_FROZEN_CRITERIA.md` lines 52–102 | b7c979e151 |
| L* window [24 pc, ≳ 1 kpc] | `campaign_fresh_gravity/CFG820_stiffness_from_globulars/README.md` | a57fe156ef |
| slip systems and bound (largest 1.9e-5) | `campaign_fresh_gravity/CFG847_lensing_slip_bound/` | 15c0894c1f |
| footings | `campaign_fresh_gravity/CFG4_common.py` | 3409d12da0 |
| NGC 3198 (Υ = 0.61, 43 radii) | `real_research/data/sparc_data/NGC3198_rotmod.dat` | 999f94dfee |
| KiDS √-tail end bounds 1.67 / 2.07 / 3.44 / 2.77 Mpc (M_b 1.50e10 / 3.66e10 / 6.01e10 / 9.13e10 M☉) | `hunt_2026/h72_where_the_boost_ends.out` | f9bfc283a0 |
| Solar-System backgrounds; 1-AU sunward-pull bound 3.66e-14 m/s² | `campaign_fresh_gravity/CFG770_cassini_stiff_action/cfg770.out` | 5554648db0 |

Declared cosmology (CFG938's): Ω_b 0.0493, Ω_c/Ω_b 5.364, H₀ 67.4 km/s/Mpc, flat, Ω_Λ = 1 − Ω_m, radiation neglected (z ≤ 10).
GW170817: −3e-15 < c_T/c − 1 < 7e-16, D = 40 Mpc (WT-02's declared path model).

## 2. The variants (declared now; signature −+++, K = 4πG)

Common to all: S_c = ∫√−g [c⁴R/16πG − mc²n − W_full(u) − (3γ/4K²) τ_μν τ^μν] + S_b, comoving labels φ^I, n = √det B,
u² = h^{μν}∂_μχ∂_νχ, W_full(u) = [−a₀u − a₀² ln(1 − u/a₀)]/K, γ = KL*²/2, τ_μν = h_μ^α h_ν^β∇_α∇_βχ − ⅓h_μν h^{αβ}∇_α∇_βχ
(CFG938's τ, kept as instructed).

Definitions:
- **Intrinsic leaf Laplacian:** ³Δχ ≡ D^aD_aχ ≡ h^{μν}∇_μ∇_νχ + θ u^μ∂_μχ (= ∇_μ(h^{μν}∂_νχ) − a^ν∂_νχ, a the medium's
  acceleration). For irrotational flow it is the Laplacian of the induced metric on the medium's leaves. It contains no derivative
  along u. With vorticity it is still defined, as the projected 1+3 operator, but no leaves exist.
- **Leaf mean:** n̄_leaf(x) ≡ lim_{R→∞} ∫_{Σ_x∩B_R} n dV / ∫_{Σ_x∩B_R} dV. Here Σ_x is the medium leaf through x (the hypersurface
  orthogonal to u), B_R is the leaf-geodesic ball, and dV is the induced volume. The limit is assumed to exist and to be
  independent of the centre (statistical homogeneity). It gives 0 on an asymptotically flat leaf (isolated system), n̄(t) on FRW,
  and n̄(T(x)) at linear order about FRW, where T is the leaf time: u_μ = −N∂_μT, so ∂_iδT = −δu_i (longitudinal part).
- **N0 (zero mode of χ):** χ is normalised by ⟨χ⟩_leaf = 0, so χ̄ ≡ 0 on FRW. V1/V2's equations leave the leaf constant of χ free,
  which is why N0 is needed. It is part of the "explicit mean-density treatment".

The variants:
- **V3 (control):** + λ(h^{μν}∇_μ∇_νχ − Kmn). This is CFG938 as written, with χ̄ from S1d.
- **V1 (leaf mean):** + λ(³Δχ − Km(n − n̄_leaf)), with N0. It is defined only where leaves exist (ω = 0). For vortical flow at
  linear order, δT is taken from the Helmholtz-longitudinal part of δu; this is a diagnostic extension, not part of V1.
- **V2 (global variable):** + λ(³Δχ − Km(n − ν)) + μ^μ h_μ^ν ∂_νν, with N0. Here ν is a scalar field and μ^μ a vector multiplier
  (only hμ enters). The action is local except that ν is constant on leaves:
  - δμ gives D_aν = 0. Where ∂ν ≠ 0 this forces u_μ ∝ ∂_μν, i.e. irrotational flow with leaves = ν level sets.
  - δν gives Kmλ = ∇_μ(h^μ_ν μ^ν).
  - δλ gives ³Δχ = Km(n − ν). With bounded, statistically homogeneous D_aχ, ν = n̄_leaf on shell.
- **V1i, V2i (declared sub-variants):** V1, V2 with τ built from the intrinsic tidal tensor D_aD_bχ = h h∇∇χ + K_ab u·∂χ
  (K_ab = h h∇u; traceless part taken with h). They differ from V1/V2 only by σ_ab u·∂χ. With χ̄ = 0 this is second order, so the
  linear battery coincides (checked, Z1). They exist only because of the zero-mode test Z below. They are scored with the same
  battery and reported with equal prominence.

## 3. Test battery (each variant; sympy + numpy/scipy, one script `wt08.py`)

Linearisation follows WT-02's machinery:
- plane-symmetric labels φ¹ = x − εξ, φ² = y − εη, χ = χ̄ + εδχ, λ = εδλ, plus each variant's extra fields (V1: δT and a multiplier
  β for ∂_xδT = −δu_x; V2: δν, μ^x, μ^y);
- expand to O(ε²) and take Euler–Lagrange equations;
- plane waves e^{σx⁰ + ikx} on FRW (a = e^{hx⁰}, frozen Kρ_c = 1.5Ω_c(z)H², c = 1, lengths in c/H) and e^{−iωt + ikx} on static
  Minkowski (WT-02's A-i with uniform gradient u₀ ∥ k, ⊥ k, or 0; W expanded with D(u₀), D′(u₀)).
- Primary runs keep the metric unperturbed. Secondary runs add a quasi-static Newtonian Φ (−a|∂Φ|²/2 − Φ a³Km δn, K-units).

| test | what is computed | PASS iff |
|---|---|---|
| **T1** static law | each variant's reduced static functional E[M_c] (spherical; W_full; γ → 0) with n̄_leaf = 0 / ν = 0 (isolated leaf); Euler–Lagrange solved at NGC 3198's 43 radii | max\|g/g_law − 1\| ≤ 1e-12 on both footings. (V1/V2 reduce to V3 there: BY CONSTRUCTION, flagged.) Diagnostic, no weight: the same embedded in the cosmic mean ρ̄(z = 0), max\|Δg/g\| |
| **T2** ∇_μT^{μν} = 0 | (a) static stress of the new terms by metric variation (V1: Km n̄(λ − ⟨λ⟩)h_ij from √h and from n̄'s volume dependence; V2: Kmν λ h_ij and the μ term) and the identity ∂_jT_ij(total) = ∂_iχ E_λ + ∂_iλ E_χ + Km n ∂_iλ for generic 3-D fields (CFG938 S3b extended); (b) the FRW background continuity equation; (c) general case: diffeomorphism invariance (Noether) | (a), (b) are sympy-exact (residual ≡ 0) and the action is diffeomorphism invariant. (c) is BY CONSTRUCTION |
| **T3** FRW background | minisuperspace (N(t), a(t), χ̄, λ̄, ν̄): ρ = −a⁻³∂L/∂N, p = (3a²N)⁻¹∂L/∂a on the variant's background solution | w = 0 exactly; ρ − Km a⁻³ ≡ 0 (no new background energy); a₀ untouched (W unchanged: BY CONSTRUCTION). Report whether the background χ̄ is fixed by an equation |
| **T4** Hadamard / linear IVP | roots of det M on (i) static Minkowski (u₀/a₀ ∈ {0, 0.5, 0.9}, ∥/⊥, kL* ∈ [1e-2, 1e4]); (ii) expanding FRW (z = 0, 10; L* = 24 pc, 1 kpc; kℓ_H ∈ {1e2, …, 1e6}); (iii) contracting FRW (H → −H). Also the own-time-derivative class (ELLIPTIC / PARABOLIC) of the χ and λ equations | WELL-POSED on all three. FRW: max Re σ ≤ 10\|H\| over the grid. Static: every ω² real and ≥ 0 (max growth ≤ 1e-9√(Kρ₀)). ILL-POSED iff max Re σ/\|H\| > 1e3 at the top k with slope ≥ 0.5 (WT-02's rule is the slope 1.9–2.1 case). Otherwise UNRESOLVED. Primary and secondary (with Φ) classes must agree |
| **T5** kinetic signs | (a) no ghost: effective inertia A(k) of the longitudinal medium mode after eliminating every auxiliary field (Schur complement of M, σ² coefficient), on FRW z = 0, 10, ±H, kℓ_H ∈ {10, …, 1e6}, and on static backgrounds (CFG938's ρc² > D u/K, margins on CFG847's systems); (b) no gradient instability: static ω²/k² → γρ > 0, FRW oscillatory roots with Re σ bounded | A(k) > 0 everywhere on the grid and (b) holds. A(k)/A_dust at kℓ_H = 1, 3 is reported (no weight: metric perturbations omitted) |
| **T6** vorticity | (a) transverse (η) roots on FRW ±H and static; (b) the vortical inertia (σ² coefficient) and whether a free function enters it; (c) is the action defined for vortical medium flow, or does the variant exclude it by a constraint the evolution preserves? | (a) a σ = 0 root and no root with Re σ > 10\|H\| (FRW) or Im ω ≠ 0 (static); (b) positive and fixed by the variant's own equations; (c) yes. Label: **GLOBAL NOW** (vorticity excluded on FRW; leaves = level sets of a field) or **NOW = MEDIUM LEAVES FOR IRROTATIONAL FLOW ONLY** |
| **T7** slip | s_∇ = 4πG r\|p_r\|/(c²g) (W-only, CFG938's definition) plus the new isotropic stress's upper bound Δs = 4πG r ρ̄_c ∫_r^{10 Mpc} g dr′/(c²g) (ρ̄_c at z = 0; declared outer reference 10 Mpc) on CFG847's five systems, both footings | worst (s_∇ + Δs) ≤ 1.9e-5 |
| **T8** growth (D-T) | leading order in aH ≪ k ≪ a/L* (L* → 0, then k → ∞ with the constraint fields scaled as 1/k, 1/k²); EdS matter era, Ω_c/Ω_b = 5.364, baryons free dust, quasi-static Φ; from each variant's own quadratic action with a(t) general; power law ξ ∝ t^α ⇒ n = 1.5α_max (δ_c ∝ aⁿ) | reported per variant. **D-T CHANGED** iff n ≥ 0.98 (linear self-gravity of the tethered medium restored); **UNCHANGED** iff n ≤ 0.90; otherwise PARTIALLY CHANGED. Footing dependence: n is footing-independent iff a₀ does not enter the quadratic action (symbolic check) |
| **T9** frame size | D1 (α₂_eff = f_c, WT-02); D2 at R☉ and 1 AU in observable form (solar surface δΦ/U vs 1e-7(370 km/s/c)² = 1.52e-13; 1-AU pull vs 3.66e-14 m/s²); D3: u_v(v) for V3 = γvΩ_cH₀/2, and for V1/V2 from the leaf-tilt term (mode level at k = 1/r), with h72 crossovers r_× for w = 370, 1000 km/s | reported, no class weight. Per row: NOT VISIBLE (< 0.1 of bound, or r_× > 10 r_end), UNDERDETERMINED (inside the 10× band), EXCLUDED (≥ 10×) |
| **T10** c_T | WT-02's E1 TT computation extended by a timelike gradient V₀ = ∂₀χ̄: δ(c_T²/c²) = [C_s u² + C_t V₀²]L*²/c⁴. Path average: V3 with V₀ = Ω_cH₀c/2 over D = 40 Mpc plus WT-02's two-galaxy path; V1/V2 with V₀ = 0 (N0) plus the same galaxy path | reported, no class weight (WT-09 owns c_T). L*_max per variant from 7e-16 |
| **Z** zero mode | Z1: on FRW and static backgrounds with χ = F(x⁰) + εδχ, substitute δχ = δχ′ + F′δT (∂_xδT = −δu_x: the shift by a function of leaf time) into the O(ε²) Lagrangian; check whether it is independent of F (∂/∂F′, ∂/∂F″ ≡ 0, sympy). Z2: for the static-Minkowski standing medium sound wave with χ̄ = 0, the leaf mean of the χ-shift current's u-component (∝ ⟨τ₁:σ₁⟩) as a function of time | **GAUGE ZERO MODE** (PASS) iff Z1 is F-independent. Otherwise **ZERO-MODE DEFECT** if the variant's background equations leave F free (the linear dynamics then depend on an undetermined background, and, by Z2, holding F = 0 overdetermines the λ equation's leaf mean), or **FIXED BY BACKGROUND** if an equation fixes F (V3: S1d) |

## 4. Verdict classes (per variant)

- **REPAIRED** iff T1–T7 all PASS, T4 is WELL-POSED on all three backgrounds, and the primary and secondary runs agree.
- **FAILS** iff T1, T2 or T3 fails, or T4 is ILL-POSED on the static background.
- **PARTIAL** otherwise; the failing tests are named.

The Z label is reported beside the class with equal prominence. The "exact repaired action" quoted in the README is a variant
that is REPAIRED **and** Z PASS. If none is, none is quoted.

Separately, per variant: **D-T CHANGED / PARTIALLY CHANGED / UNCHANGED** (T8). Overall line: list every variant's class, Z
label and D-T label. No headline merges them.

## 5. Controls (all must pass for the main run to be read)

- **K1.** V3 through this lane's machinery reproduces two things:
  - CFG938's static law, max\|g/g_law − 1\| ≤ 1e-12 (CFG938 2.2e-16);
  - WT-02's FRW leading root Re σ = k²/3 (units H, c/H) to ≤ 1e-6 at kℓ_H = 1e6, with the Hadamard test firing.
- **K2.** V1 and V2 on static Minkowski (n̄_leaf = ν̄ = n₀ constant) give the same longitudinal and transverse dispersion
  determinant as V3 (CFG938 S5a, symbolic, up to a nonzero constant factor). Their static functional at n̄ = 0 equals V3's.
- **K3.** V1 with the leaf tilt switched off (n̄ evaluated at coordinate time) reproduces WT-02 MU3's FRW determinant
  symbolically (up to a nonzero factor).
- **K4.** The T8 machinery gives, for V3:
  - n = 0.69433 ± 5e-4 (CFG941 D6);
  - n = 0.60954 ± 5e-4 with the χ̄ boost removed from u² (CFG938 S6 / CFG941 K3);
  - n = 1 ± 1e-6 with the tether off (dust).
- **K5.** TT linearised Ricci = −½□h (WT-02 K5). C_s = 1.5 for a spatial gradient (WT-02 E1). L* = 0 gives c_T = c exactly.
- **K6.** CFG938's worst W-only s_∇ = 5.8e-6 is reproduced within 2%.
- **K7.** AS206 cross-check: λ√h δ(Δ_hχ) + ½tr(k)√h λΔ_hχ, built with AS206's identity, equals ½√h k^{ij}T^λ_ij up to a total
  divergence, where T^λ_ij = 2∂_(iλ∂_j)χ − δ_ij∇λ·∇χ is CFG938's S3a stress. The test is that the Euler operator of the difference
  with respect to k_ij vanishes. Negative control: dropping AS206's volume term must make it fail.

## 6. MUTATE (`WT08_MUTATE=1`; separate outputs `wt08_MUTATE.out`, `wt08_results_MUTATE.json`; exit 1 iff every tooth bites, else 2)

- **MU1 (required).** V1 with ³Δ → h^{μν}∇_μ∇_ν, i.e. the θ u·∂χ term restored and the mean subtraction kept. Bites iff T4 reads
  ILL-POSED on expanding AND contracting FRW.
- **MU2.** V2 without the μ term: ν becomes a plain multiplier, which forces λ ≡ 0. Bites iff T1 then fails (deviation ≥ 0.1, the
  law lost).
- **MU3.** V1 with the tether sector off (W → 0, λ term removed). Bites iff T8 reads D-T CHANGED (n ≥ 0.98).
- **MU4.** V2i with the sign of the K_ab u·∂χ correction flipped. Bites iff Z1 then reads F-dependent.
- **MU5.** V2 on FRW with ν̄ held constant (ν̄̇ = 0). Bites iff the T6 label flips to IRROTATIONAL FLOW ONLY (η̇ unconstrained).

## 7. Compute and hygiene

- One process: `OMP_NUM_THREADS=1 nice -n 10 python3 wt08.py`, timed with `/usr/bin/time -l`.
- In-script RSS guard: exit 75 above 0.9 GB.
- Watchdog at every guard: exit 75 if swap used has grown > 1 GB since start (`sysctl -n vm.swapusage`) or free + inactive
  (`vm_stat`) is below 8 GB.
- Before each run: check `ps -axo command=` for a live 1024³ PM job and for running wt0*.py processes (wait if two others run), and
  require free + inactive ≥ 12 GB.
- No downloads. No home paths or personal names in files.
- Outputs (`DERIVATION.md`, `wt08.py`, `wt08.out`, `wt08_results.json`, the `_MUTATE` pair, `README.md`) are left uncommitted for
  orchestrator review. Post-freeze changes go only in appended amendments; this text is not edited.

## 8. Blindness disclosure

I was told WT-02's MU3 hint (intrinsic ³Δ plus mean subtraction removes the ill-posedness) and read WT-02's README, criteria,
script and outputs, including MU3's determinant and Hadamard result. I also read:
- CFG938's README and DERIVATION, and its S3a/S3b and S4 code;
- CFG941's README, §1.4 and growth code (n = 0.69433 / 0.60954);
- CFG961's criteria, including its expectation that the ττ term with the timelike FRW gradient gives a c_T term near 7e-16 at
  L* = 1 kpc;
- AS206's derivation;
- the CFG944–947, CFG820 and CFG847 READMEs, and CFG172D's leaf-mean lines.

No number of this lane has been computed. By hand, before freezing, I expect:
1. V1/V2 remove the parabolic terms, so T4 is WELL-POSED on all three backgrounds at large k (contracting FRW keeps bounded
   O(|H|) growth).
2. At leading subhorizon order the leaf-tilt and ν/μ terms drop out (O(aH/k)²) and the χ̄ boost is absent. V1/V2 then give
   n ≈ 0.6095 and V3 0.694, so D-T is UNCHANGED for every variant (the tether's quadratic coefficient c₂ = 1 is untouched).
3. V2's constraint forbids medium vorticity wherever ν̇ ≠ 0 (GLOBAL NOW on FRW). V1 is undefined for vortical flow, so I expect T6
   to fail for V1.
4. Z: CFG938's τ carries a nonzero leaf charge (∝ τ:σ). That would make χ's leaf constant a physical but undetermined zero mode in
   V1/V2, and V1i/V2i would remove it. If so, only V2i can be both REPAIRED and Z PASS.
5. The cosmic-clock field u_v is suppressed in V1/V2 by about 9(Hr/c)².
6. c_T: V3 carries a clock term near the 7e-16 line at L* = 1 kpc (CFG961's expectation, read before freezing). V1/V2 do not.
7. Horizon-scale inertia corrections from the tilt are of order (aH/k)⁴, of unknown sign.

The rules above are written to decide either way. Expectation 4 is tested by Z1 and MU4; expectation 2 by K4 and MU3.
