# CFG43 — Gap 3: the a₀–Λ tie written into a conserved fluid's stress cap, in one action

Scripts (each with two MUTATE controls, `MUTATE=1` and `MUTATE=2`, which must exit 1): `A1_action_field_equations_dof.py` (11 checks), `A2_frw_flat_a0_and_dust_limit.py` (5), `A3_cap_entry_form_and_obstruction.py` (11). Shared code: `A_common.py`. Outputs are next to them. Each runs in about a second. The scripts were written by a delegated agent and re-run here: the main runs pass, and all six controls fail as required. I also checked the obstruction's key scaling by hand (below). The sympy derivations were run, not re-derived.

## What was built

One action (c = 1, M_P² = 1/8πG, ε = κ²/8π, **κ = ½ FITTED**):

    S = ∫d⁴x { √−g [(M_P²/2)R − M_P²Λ] + M_P²Λ ∂ₘTᵐ − √−g ρ(n; Λ) + Jᵐ ∂ₘθ },   n = √(−g_mn JᵐJⁿ)/√−g

Λ is the Henneaux–Teitelboim field with multiplier Tᵐ. The fluid is a Schutz–Sorkin irrotational fluid with one conserved current, coupled to g only. The cap enters as

    ρ(n; Λ) = m n + P_cap x arctan x,   x = m n/(ν* M_P² Λ),   P_cap(Λ) = ε M_P² Λ = a₀²/8πG.

That gives P = P_cap x²/(1+x²) ≤ P_cap. With κ = ½, a₀ = √(8πG P_cap) = 9.3603 × 10⁻¹¹ m/s², the same α(Λ) that XR20 T1 wrote into the kernel term, so **the kernel and the fluid's cap read the same constant**.

## Status

| | items |
|---|---|
| **DERIVED** (by these scripts, from the action) | Λ is a global integration constant (∂ₘΛ = 0 whatever the matter Lagrangian; a perturbation δΛ has no wave operator); number conservation (n a³ = const); the fluid's Λ-dependence lands only in the unimodular clock; Friedmann = GR + Λ + fluid; the reparametrisation identity; the Dirac count on a lattice (fluid alone D = 2N; adding the HT sector D = 2N + 2 with 2N − 1 first-class constraints and no tertiary one, so local degrees of freedom are unchanged and there is one global pair); a₀(z) flat to 6 × 10⁻¹¹ for z ≤ 10; Ω_c is initial data; a column bound Σ ≤ a₀/2πG (106.9 / 129.2 M☉/pc²) |
| **POSTULATED** | the tie function P_cap = (κ²/8π) ρ_Λ c² (so "H-TIE" agrees with XR20 by construction); the saturating shape x²/(1+x²) and its argument; irrotational flow; a hard bound; minimal coupling to g |
| **FITTED** | κ = ½; **ν\*, a new dimensionless constant** (below); Ω_c (inherited) |
| **OPEN** | a cap that binds across the BTFR mass range; shell crossing; the galaxy law itself; the bound-only switch; T5's max rule; PPN; the four-form variant (not attempted) |

## The obstruction (scoped)

Hypotheses: a single conserved current, an EOS that is barotropic in the density ν = ρ/ρ_Λ, P ≤ P_cap, linear growth close to ΛCDM, and the cap reached at r_M (where g_N = a₀ for the P2 point-mass phantom).

1. **No entry without a new number.** At ν\* = 1 the sound speed today is c_s² = 6 × 10⁻³ and linear growth is 5–14% of ΛCDM. The DBI/tachyon entry has no second scale but P < 0 and fails too.
2. **ν\* is new.** Growth within 5% needs ν\* ≥ 2 × 10⁴ to 1 × 10⁷ at k = 0.5–30 /Mpc (ν_min ∝ k^1.5).
3. **A scale-free window.** The density at r_M in units of ρ_Λ scales as ν_M ∝ M_b^(−1/2) exactly, and the growth bound at the halo's own scale (k = π/R, R ∝ M^(1/3)) scales as ν_min ∝ k^1.5 ∝ M^(−1/2). The ratio g₀ = ν_M/ν_min is therefore a pure number, and one ν\* engages the cap over a mass window of g₀² whatever ν\* is. Direct re-solves at 10⁹ and 3 × 10¹¹ M☉ give g₀ = 1.08 and 1.04. Depending on conventions g₀ ranges over 0.08–3.3, so the window is at most about **11× in mass, against the 10⁴ the BTFR needs**. This is a screening estimate (two-fluid Newtonian growth).
4. CFG2's settled medium has P_d = y P_cap, which exceeds a hard cap for y > 1. This action realises the CFG5-type bound, not CFG2's stress law.
5. A single-stream fluid cannot survive shell crossing (N17/XR8, cited from the record).

**What the obstruction does not touch:** a fluid whose cap is not a barotropic function of its own density (for example a non-barotropic or phase-space-dependent stress, or an order-parameter fluid such as FL1).

## Independent referee (2026-09-28)

A hostile re-implementation with its own linear-growth solver reproduced the obstruction: ν_min(k) = 2.2e4, 1.8e5, 2.0e6, 1.0e7 at k = 0.5, 2, 10, 30 /Mpc (the lane's values differ by 5–12%, from its coarse log grid), the exponent 1.49–1.50, ν_M ∝ M_b^(−1/2) exactly, and g₀ = 0.36 / 0.355 at 10⁹ / 3 × 10¹¹ M☉ (5% criterion; 1.06 / 1.04 at 20%). The criterion's redshift and the barotropic Jeans treatment do not matter. If the k values are in h/Mpc, ν_min is a factor 0.55 lower. Caveats: **"at most about 11×" is too strong as a ceiling.** It holds only if suppression beyond 50% is disallowed and F ≥ ½ is kept; stacking the generous choices (30% suppression, F ≥ 0.01, f_h = 40, k = 1/R) reaches 10⁴–10⁵, but each is individually unmotivated and F ≥ 0.01 contradicts the hydrostatic requirement (the P2 phantom needs P/P_cap = g_N/a₀ ≥ 1 inside r_M, which needs F → 1, cutting g₀ by about 3 more). Other cap shapes were not tested. The obstruction survives as stated for the saturating barotropic EOS.

## Which gates it touches

Group 5 of `closure_map/GATES.md`: 5.01 partly (one action for tie plus fluid, still not V0), 5.05 for the dof count of fluid + HT, 5.10 (Friedmann = GR + Λ + dust, growth fine only for ν\* ≥ ν_min), 5.13 (the tie now covers the fluid's cap; tied, not derived), 3.10/3.11 (flat a₀(z) inherits the unimodular branch). It does not touch 5.03, 5.04, 5.07, 5.08, 5.11, 5.12, the bound-only switch, the max rule or PPN.

## Standing

**Gap 3 is partly filled and Gap 2 is untouched.** The tie can act on a conserved fluid in one action without adding local degrees of freedom. But the cap's entry cannot be derived, and the natural saturating form needs a new constant and covers about one decade in mass. It is an existence result and a scoped no-go, not a mechanism. Nothing here says the theory is closed.

## Referee corrections (2026-09-29, README audit relayed from the Opus/Fable chat; appended)

- The "about 11× in mass" ceiling in the obstruction's item 3 is contradicted by this README's own referee paragraph, where stacked convention choices reach 10⁴–10⁵. Read the window as convention-dependent, from about 11× up to 10⁴–10⁵, against the 10⁴ the BTFR needs; the body text and ledger row 52 were not amended (append-only).
