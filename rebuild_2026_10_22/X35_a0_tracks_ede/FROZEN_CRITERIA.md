# X35_a0_tracks_ede — FROZEN CRITERIA (committed with ASSUMPTION_LEDGER.md, alone, before any script or number)

**The owner's idea.** a₀ tracks the dark-energy density, a₀(z) = κ c √(G ρ_DE(z)) (flat a₀ is only the w = −1 case). If
ρ_DE contains an early dark energy (EDE) component, a₀ at z ≈ 1100 could be 10²–10⁴ × today's, so the plasma at
recombination would sit deep in the law's regime. **Question:** can a₀ tracking an EDE component switch the law on at
recombination strongly enough to supply the steady (non-oscillating) potential wells the acoustic peaks (third peak) and
early growth need, without a separate cold component, and without breaking BBN, the damping tail, the sound horizon / H₀ or
the late-time galaxy results?

Settings. κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt a₀ = 1.1312e-10 m/s², each scaled by
√(ρ_DE(z)/ρ_DE(0)), reported separately, never pooled. No dark-matter particle. EDE parameters are transcribed from the
literature (PROVISIONAL, from memory of the papers, no download) and are never fitted here. Not "theory closed". Nothing
here says the data favour the framework. X34 (recombination release) runs in parallel; this lane does not touch a
turn-on of the cold sector and runs no CLASS.

Files. Script `x35_ede_tracking.py` (sympy + numpy/scipy, PYTHONHASHSEED=0, one thread, `nice -n 15`, < 1 GB, minutes).
Outputs `x35_results.json`, `x35_ede_tracking.out`; MUTATE twin `X35_MUTATE=1` → `x35_results_MUTATE.json`,
`x35_ede_tracking_MUTATE.out`.

## 0. Step 0 — stop rule (all must PASS, else the lane stops with UNDECIDED and nothing after it is graded)

| id | reproduction | line |
|---|---|---|
| S0-1 | The record's "x ≈ 11–14 at z ≈ 1100, a₀ inert" (MAP §1 L22; Z1 ledger: "RECORD (audit estimate)", no script). Estimator frozen here: x = k_phys \|Ψ(k, z = 1100)\| c² / a₀, Ψ = Newtonian-gauge potential per ln k from this lane's own fluid ODE (§2) in the record's ruler cosmology (ω_b 0.02236, ω_c 0.1202, h 0.677, CFG689), Λ only, at k = 0.05 Mpc⁻¹ | within a factor 2 of the record: canonical x ∈ [7, 28], alt x ∈ [5.5, 22] |
| S0-2 | The record's DESI curve M-DEC (CFG223 `R_dec`, w0 −0.838, wa −0.62): R(0, 1, 2, 3) = 1, 0.990, 0.874, 0.775 | ±0.002 each |
| S0-3 | CFG689's native a₀(z): the committed `cfg689.json` (primary) P1 `sqrtX_q` medians at z* = 2.33 are read back: 0.909 (BAO+SN) and 0.950 (BAO) | ±0.002 each |
| S0-4 | Sound-horizon integrator: r_d for the CFG689 ruler cosmology (ω_b 0.02236, ω_c 0.1202, N_eff 3.046, m_ν = 0) | within 1 % of CFG689's 147.07 Mpc |

S0-1 reproduces a statement that has no committed script; it can only confirm the order of magnitude. It is labelled so.
The Λ-only x at z = 1100 for the DESI M-DEC curve is also reported (it must be ≥ the Λ value, the record's "equal or
lower a₀" statement).

## 1. Step 1 — magnitude

**EDE family (fluid form, Poulin+18 / Smith+20):** ρ_EDE(a) = 2 ρ_EDE(a_c) / (1 + (a/a_c)^{3(1+w_n)}), w_n = (n−1)/(n+1).
n = 3 gives w = ½ and dilution ∝ a^{−4.5}; the brief's "∝ a⁻⁶" is the n → ∞ (w = 1) case. **Both are run**, labelled.
f_EDE ≡ ρ_EDE(z_c) / ρ_tot(z_c), with ρ_tot from the ruler cosmology (+ EDE).

**Literature points (PROVISIONAL, transcribed, never fitted):**
- L1 Smith, Poulin & Amin 2020 (n = 3, Planck + BAO + SN + SH0ES): f = 0.122, log₁₀ z_c = 3.562.
- L2 Poulin, Smith, Karwal & Kamionkowski 2019 (n = 3, "Hubble tension" fit): f ≈ 0.08, z_c ≈ 5000 (approximate).
- L3 Hill+ 2020 bound without SH0ES: f < 0.087 (95 %), taken at z_c = 3500.
- L4 the brief's generic f = 0.10 at z_c = 3000 and at z_c = 5000.
A grid f ∈ {0.05, 0.087, 0.122}, z_c ∈ {3000, 3650, 5000} is also tabulated for context (not graded).

**Fields.** Ψ(k, z) from a small Newtonian-gauge fluid ODE (§2) in two background/perturbation models:
- **M-LCDM**: ruler cosmology with its cold component (ω_c 0.1202) — the "record's linear-era fields" estimator.
- **M-NATIVE**: no cold component (ω_c = 0; baryons + photons + neutrinos), the question's own premise.
EDE enters the background only (its perturbations are dropped; ASSUMPTION A6).

**Graded quantities at z = 1100, per footing, per model, per literature point:** x_max = max over k ∈ [0.01, 0.3] Mpc⁻¹
of x(k); x_rms = √∫ x(k)² d ln k over k ∈ [0.001, 1] Mpc⁻¹ (the total field a mode is linearised about).
**MAG_OK** ⟺ for at least one literature point L1–L4, x_max < 1 AND x_rms < 1 on both footings in both models.
Also reported: the z-window where x_max < 1 (z from 10⁵ to 300), and a₀(z)/a₀(0) at z = 0, 2.33, 1100, z_c, 10⁹.

**Late-time consistency (checks, §4):** |a₀(0)_EDE / a₀(0)_noEDE − 1| < 1e-4 and the direct EDE shift of a₀ at z = 2.33
< 1e-3 for every literature point. The **indirect** effect on CFG689 through its sound-horizon ruler is reported separately
(an ESTIMATE in flat Λ at CFG689's ω_m), never folded into the check.

## 2. Step 2 — the decisive physics (sympy + small numerics)

Equations: v3s field equations as written in `covariant_push_2026_10_22/V3_FULL_PICTURE.md` §2 and
`rebuild_2026_10_22/L1_khronon_pm/FROZEN_CRITERIA.md` §1 (BS24 PN system): Ξ the lapse perturbation, hold equation
4πGρ_τ = −[∇·(J_Y∇Ξ) + μ_K²Ξ] with J_Y = μ(x) − 1 = −1/(1+x), x = |∇Ξ|/a₀; Poisson ∇²φ = 4πG(ρ_b + ρ_γ-sector + ρ_τ);
khronon continuity ∂_tρ_τ + ∇·(ρ_τ v_τ) = 0, Dv_τ/Dt = −∇φ + ∇Ξ. Static limit: AQUAL ∇·[μ(|∇ψ|/a₀)∇ψ] + μ_K²ψ = 4πGρ.
Tight-coupled baryon–photon fluid: δ_γ'' + (R'/(1+R))δ_γ' + k²c_s²δ_γ = −(4/3)k²Ψ (sub-horizon, Φ = Ψ, Φ'' dropped).

Derivations (each a scored check):
- **D1 (covariant, no background charge).** ρ_τ ≡ 0 is an exact solution of the khronon continuity equation (homogeneous
  in ρ_τ). With ρ_τ ≡ 0 the hold equation is ∇·(J_Y∇Ξ) + μ_K²Ξ = 0, and, integrating by parts on a periodic domain,
  ∫Ξ·[∇·(J_Y∇Ξ) + μ_K²Ξ] = ∫[|∇Ξ|²/(1+x) + μ_K²Ξ²] = 0 ⇒ ∇Ξ ≡ 0 (Ξ ≡ 0 for μ_K > 0). Then φ is the GR potential of the baryon–photon–neutrino fluid at every
  a₀. Verified symbolically on a periodic 1-D Fourier test field.
- **D2 (covariant, with background charge ρ̄_τ = the Blanchet–Skordis dust, i.e. a separate cold component).** Linearised
  hold with mean-field f = μ(x̄): Ξ_k = −4πG a² δρ_τ / ((1 − f)k² + a²μ_K²) ⇒ dust self-gravity kernel
  s(k; f) = (a²μ_K² − f k²)/((1 − f)k² + a²μ_K²). In the EDE regime (x̄ → 0): s → a²μ_K²/(k² + a²μ_K²), a₀-free
  (L1's LIN kernel). a₀ enters only through f = x/(1+x); the deep limit removes it.
- **D3 (static-limit reading, the "naive" phantom).** Exact 1-D plane-wave AQUAL: μ(|g|/a₀) g = g_N ⇒ g = g_N ν(|g_N|/a₀),
  odd in g_N. With ψ an instantaneous functional of the plasma's own δ, the mode equation is an autonomous oscillator with an
  odd restoring term; its potential is even.
- **Effective Φ driving and phase.** For CDM the driving −(4/3)k²Φ_c is (nearly) constant over an acoustic period; for the
  law it is an odd function of δ_γ(t), i.e. in phase (or antiphase) with the wave. Graded statistic, the **steady
  fraction** F = |⟨Φ_extra⟩_T| / max|Φ_extra| over the oscillation (CDM control: F = 1), and the compression/rarefaction
  asymmetry A = |δ_max⁺| / |δ_max⁻| (odd/even peak proxy; CDM control > 1). Computed numerically on a non-expanding
  single-mode oscillator with (a) the deep plane-wave law (exact 1-D) and (b) a constant external Φ_c (control), both
  started from rest at the same amplitude.
- **Effective Jeans scale (static reading).** Linearising AQUAL about the total rms field x_rms (deep: x_true solves
  x²/(1+x) = x_N), G_eff/G ∈ [1/(μ(1+L)), 1/μ], L = dln μ/dln x. The plasma mode is non-oscillating (Jeans unstable) for
  k < k_J,eff, k_J,eff² = 16πG a² ρ_γ (1+R)² (G_eff/G) / c² (comoving). Reported at z = 1100 per literature point.

**Classification.** STEADY ⟺ (covariant) a non-oscillating extra potential exists with ρ̄_τ = 0, OR (static reading)
F ≥ 0.5 with the plasma still oscillating (k_J,eff < 0.02 Mpc⁻¹). OSCILLATING ⟺ not STEADY and the static-reading extra
potential has F < 0.5. If D1 gives an identically zero extra potential, the covariant sub-case is reported as "NULL" under
the OSCILLATING verdict's consequence (cannot replace CDM in the CMB).

## 3. Step 3 — peak proxy (only if Step 2 is STEADY)

Semi-analytic: zero-point offset −(1+R)Φ_extra,steady at z = 1100 vs the CDM case's offset; odd/even ratio A vs the CDM
control; third-peak driver = the steady Φ at k ≈ 0.09 Mpc⁻¹ relative to M-LCDM. Pass ⟺ within 30 % of the M-LCDM value.
Not run if Step 2 is not STEADY (stated).

## 4. Step 4 — reported (not graded by a threshold unless stated)

- BBN: ρ_EDE/ρ_r at T = 1 MeV (z ≈ 4.3e9); ΔN_eff-equivalent (late-time conversion, labelled); a₀ at that epoch. Q6's
  literal K(Q) stiff partner is independent of a₀ and is unchanged (stated, not recomputed).
- Damping tail: whether k_J,eff (static reading) reaches the damping range (k ≳ 0.1 Mpc⁻¹).
- Sound horizon: r_d for M-LCDM, M-LCDM + EDE, M-NATIVE, M-NATIVE + EDE (literature points); rough H₀ scaling
  H₀ ∝ 1/r_d at fixed θ* (labelled rough).
- The record's early-universe lanes (Q6 radiation era, X18 flux cap): whether a huge early a₀ changes them.

## 5. Frozen verdicts

1. If any S0 fails → **UNDECIDED** (stop).
2. Else if not MAG_OK → **MAGNITUDE INSUFFICIENT**.
3. Else if STEADY and Step 3 passes and Step 4 shows no break → **EDE-TRACKING LAW SUPPLIES STEADY WELLS** (state window).
4. Else if OSCILLATING → **LAW ACTIVE BUT OSCILLATES WITH BARYONS** (cannot replace CDM in the CMB); the covariant D1
   sub-case is named.
5. Else → **UNDECIDED**.

## 6. Checks (normal run: all PASS) and MUTATE (named checks must FAIL, exit 1)

Normal: S0-1…S0-4; K1 sympy D1 identity residual 0; K2 sympy D2 limits (x → 0 gives a²μ²/(k²+a²μ²); x → ∞ gives
(a²μ² − k²)/(a²μ²)); K3 sympy D3 identity μ(gν)·gν = g with ν = (1+√(1+4/y))/2, residual 0, and oddness; K4 F_law < 0.05
and F_CDM > 0.95; A_CDM > 1.05 and |A_law − 1| < 0.02; K5 late-time a₀ shifts (§1); K6 ODE super-horizon sanity: Ψ at
k = 0.001 Mpc⁻¹, z = 1100, M-LCDM, divided by its initial value lies in [0.80, 1.0].

`X35_MUTATE=1`: (i) EDE switched off (f = 0 at every point) → **M-A** "MAG_OK" must FAIL; **M-B** "a₀(1100)/a₀(0) > 10
for some literature point" must FAIL; (ii) the law's Φ is replaced by a constant Φ_c of equal amplitude → **M-C**
"F_law < 0.05" must FAIL; (iii) a non-zero initial khronon charge is planted in D1 → **M-D** "Ξ ≡ 0" must FAIL.
