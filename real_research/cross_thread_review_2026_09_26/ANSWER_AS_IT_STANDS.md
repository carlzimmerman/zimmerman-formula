# The answer as it stands: ASSEMBLING

2026-09-26/27. This page is assembled from the parallel threads' results. Every row cites a lane and a commit, or
says it is pending. The owners' own rows are in [ANSWER_ROWS_RECEIVED.md](ANSWER_ROWS_RECEIVED.md). **The closure
target is OPEN.** κ = ½ is a declared input. The dark mass is required.

**2026-09-27: the program changed direction.**
- The author stopped the triggered-carrier chain at 22:40 on 2026-09-26. Their reason: scanning switch branches, caps
  and kicks on a hand-posited carrier adds knobs instead of deriving them.
- The goal now is one action with no declared constants beyond κ = ½ (fitted), with the dark sector a state of the
  same field. The first-principles derivation chain leads it (`real_research/derivation_chain_2026/`,
  `CHAIN_STATUS.md`).
- §1–§6 record where the construction approach (the model M*) stands. §7 lists the review lanes that now serve the
  chain.

**Consistency gate.** `XR10_answer_validator.py` traces every scorecard row's model from source (re-run c64766ca8).
- **One scorecard row is now computed on M\* itself:** KiDS on M*'s carrier (XR14). It carries two stated
  approximations, both in the carrier trigger.
- Every other row is off M* on a stated axis, listed in §3.

Four compatible-approximation rules are enabled, each backed by an exact or computed check:
- Harvey operator C for A: XR5 H1, |Δβ| ≤ 5e-5.
- ν_RAR = ν_mono for y ≤ 2.337: XC4, exact.
- The cap does not bind on KiDS lenses: DE10 S1.
- The cap does not bind at the flagship radius: ℓ_cap(2.5) = 216 kpc against r_F ≤ 38.6 kpc.

The forest's conservative-argument rules stay off, because they are arguments, not controls.

## 1. The model M*

- **Gravity.**
  - GR plus the khronon: C-H/K, BPS with α_c > 0 and β = 0, and the leaf average. Causality is criterion B. c_T = c.
  - The one covariant action is V0 (`real_research/chk_v0_2026/`: CV1 cc2b55bbb, CV2 db21f7edf, CV3 a7abb4d4f (corrected), CV4 ab6f31b61).
  - **V0 is not a complete action.** Its region gate is obstructed once varied (DE12 7f84b3546, DE13 6daea932c).
    Neither repair door works (XR15). The data passes use the gate as a prescribed mask.
- **MOND.**
  - The kernel is ν_mono, declared; it equals ν_RAR for y ≤ 2.337, with a largest gap of 0.0104 dex.
  - It is heat-filtered and region-local (L361, σ = 1; σ is negligible for KiDS and Harvey).
  - a₀ = κc√(Gρ_Λ) with κ = ½ declared, so a₀ is flat in time.
- **The switch.**
  - It reads the MOND sector only, in CV3's constrained form C[∇²(u−v) + ∇·((ν−1)∇Sw)]. That is carrier-blind (MS1).
  - CV3 records a gate-independent constraint determinant. XR15 found that this holds only if U reads an ungated
    phantom; with V0 as written the determinant depends on the gate and is singular in every layer. CV3's owner
    decides which reading V0 uses.
  - The vacuum gate is x_c,eff(z) = x_c0[Ω_Λ0/Ω_Λ(z)]^p, with p = 1, x_c0 = 2.5 and w ≤ 0.25 (DE2/DE9).
  - MS5's κ-form cap, U_cap = C·m(∇²Φ_X, v_cap² κ_X²), ends every region at v_cap/(H√x_c): 1.75 Mpc at z = 0.5,
    2.99 Mpc at z ≈ 0. v_cap = 325 km/s is declared.
- **The dark mass** is a new field (FL1 40c6ae144, FL2 e96b71eb0, FK1 c2e1fa119; XR8).
  - **What it is:** a superfluid order parameter Φ, one complex scalar. It feels Newtonian gravity only (reciprocity
    holds). Its phase is not the khronon (CV4).
  - **"Not particles"** here means a classical coherent field at occupation ~1e76–1e88 per de Broglie cell. Its quanta
    would still be bosons of mass m ≳ 1.9–5.2e-19 eV. The amount is set by initial data, not derived.
  - **The kick (FK1/FL2):** ε Re(Φ²) splits Φ in two, and λ(K)(Im Φ²)² converts φ_Hφ_H → φ_Lφ_L into back-to-back
    waves at v_k. ε/m² = 1.84–2.35e-6 is FITTED to the kick window 575–650 km/s.

## 2. Field content and constants (V0 writer's list)

| Content | Status |
|---|---|
| g_μν: 2 tensor modes | derived |
| khronon τ: 1 propagating scalar | declared |
| constrained auxiliaries (U, W, L, λ₀; Y = w, Ψ, V = v, Λ_d) | no propagating DOF only where CV3's determinant is non-zero (XR15) |
| dark fluid Φ: 2 propagating real fields | declared, new content |
| **total** | **5 propagating, plus matter** |

| Constant | Status |
|---|---|
| κ = ½ | FITTED, underivable (Z ≡ κ = 5.7888) |
| a₀ | derived, given κ and Λ |
| Λ | declared (measured) |
| p = 1, x_c0 = 2.5, w ≤ 0.25 | declared, pinned to a window by the data |
| v_cap = 325 km/s | declared |
| ξ, m (web mass), σ = 1, α_c | declared |
| c₂ | declared, in tension across the record |
| ν_mono (δ = 0.05) | declared |
| the gate W | declared; obstructed when varied |
| m_d ≥ 2–5e-19 eV | declared |
| ε | FITTED |
| λ₀, q = 1.75 | declared |
| the dark amount and its misalignment | declared |

This list of declared constants is what the new direction is trying to eliminate.

## 3. Scorecard (the axis that keeps each row off M* is named)

| Gate | Verdict | Numbers | Lane | Off M* on |
|---|---|---|---|---|
| Flat-a₀ flagship, z = 2.5 | **not established** for M*'s carrier | L388's z = 2 residue S = 0.063–0.075 against S_crit = 0.059 gives +0.106 to +0.126 dex (XR17, a committed script). The fluid's own conversion does clear r_F on the record's grid (XR16: S ≤ 7e-5 via early escape at z = 3.8–6.9; M_b = 1e11.5 mostly fails) | MS2, XR17, XR16 | carrier: M*'s is L388's, not the fluid's own conversion |
| KiDS-1000, carrier lensing included | **pass, ON M\*** | M*'s carrier: −34.3 to −26.3 (worst −26.28) against +4; DE10's L375 carrier −37.0/−34.0 (hard), −32.3/−29.3 (w 0.25) | XR14 b667f56bb; DE10 dabce1b73 | (on M*, two stated trigger approximations) |
| Cosmic shear, halo model, κ cap | pass | 1.049/1.124 (w 0.25). Uncapped fails at 2.7/3.2 | MS3/MS4/MS5 | epoch: retention taken at z = 0/2, scored at z = 0.5 (L396 never ran) |
| Lyman-α forest, the switch | pass, converged | worst 0.0046 at three resolutions (DE11b) | DE11 aa6588d56, DE11b e35112739 | carrier and cap absent; phantom over-stated |
| Lyman-α forest with the fluid's own conversion | **not established** | 11.3% / 8.0% at the nominal cell against the 10% line (XR12); conversion not mass-selective, budget 4–6.5× AT1's (XR16) | XR12, XR16 | a different carrier; needs a flux run with sub-grid conversion |
| RAR, RC100 | pass | carrier shift ≤ 1.24e-4 dex | L391 441d811e2 | switch absent; L376's carrier |
| S₈, clearing, X-COP | **not run** | L396 was stopped before launch | — | — |
| Harvey | knife-edge, uncontrolled | S2 passes only at 575 km/s (+0.096 against +0.10); MUTATE never ran | L389 6dc375e88 (partial) | matter-only switch branch; L397 never ran |
| EFE, cluster-infall BTFR | **fails** | 2.2–6.3σ (κ-form re-score, XR9) | XR9 | (none) |
| EFE, LV dwarfs | **fails** | 3.9–4.5σ | XR6/XR9 | (none) |
| Local Group zero-velocity radius | **fails** | +0.18 to +0.24 dex | XR9 | (none) |
| Coma UDGs | **fails** | 4.2–4.3σ | XR9 | (none) |

## 4. Doors closed (tried, failed, recorded)

- **Switch readings.**
  - Matter-only fails KiDS everywhere (DE8, L392).
  - Curvature leaks onto the carrier and makes lensing differ from dynamics (MS1, DE7).
  - A K-only gate is blind (CV4).
- **Action-level repairs of the MOND-sector gate.**
  - DE13: gradient stiffness on f or on U, and an acceleration-reading gate, all fail; no gradient energy of any
    strength rescues a layer (Lean, 8 theorems).
  - XR15: a smoothed gate leaves 16 of 24 layers growing at 1.1–2.8 H, and no single length works; a switched
    stiffness is unstable at every width.
  - XR11: letting the dark fluid carry the gate's stiffness moves it off the gas but leaves the fluid unstable on every
    z = 0.25 layer and puts the regions in the wrong places.
- **Region sizes and environment.**
  - The small-region door (XR9): KiDS needs ~1.5 Mpc regions around L* galaxies, the Local Group ~0.8–1.1 Mpc.
  - The per-object door (XR13): flips 2 of 4 environment liabilities but breaks the MW–M31 timing (≥ 23σ), X-COP,
    groups, two-sided cosmic shear and El Gordo's ease. It also needs a new constant and a galaxy-type rule.
- **Caps and carriers.**
  - The withdrawn cap form fails shear (MS5). "One number sets the cap and the kick" is false (XR7).
  - GP4's window is withdrawn (PAPER34 v3). AT4's carrier fails shear. L373 at p = 2 has no window. Astra's w = 1 gate
    has no window (DE9).
- **Fluids.**
  - Every single-velocity continuum fails shell crossing (XR8), and L374's runaway is not the kick.
  - Swirl does not help: rotation and shear stabilise no edge layer (XR11); spin moves retention by ≤ 0.0064 (XR12);
    vortices leave the clock undisturbed (FL3).
  - Mock-based cosmic-shear passes are not established (MS3, DE5b).

## 5. Data gates ahead

- Gaia DR4, 2026-12-02 (frozen pre-registration).
- The z ≈ 2.5 deep-MOND Tully–Fisher zero point: needs JWST and ALMA.
- Euclid DR1, 2027.

## 6. M*'s open items after the redirect

Stopped with no result: L393, L394, L395, L396, L397, AT5 (details in the rows page). CV6 (a dynamical gate field)
was not started. Nothing further is being launched on M*'s hand-set pieces. PAPER34 v3's source is ready; the upload
waits for the author's go.

## 7. The review lanes serving the derivation chain (2026-09-27)

Where the chain stands, from its own ledger (chain lead's commits; checked against `CHAIN_STATUS.md`):
- FP7's AQUAL-type root passes statics, the Solar System, stability, c_T and PPN.
- FP9's separator H_Y passes the linear gates with FOUR declared constants.
- FP10's dark sector clears galaxies before clusters, with ε FITTED.
- FP11: the MW–M31 timing works with baryons only, but R0 overshoots by +0.20 dex. The Local Group fails.
- In flight on the chain lead's side:
  - FP12: other groups' R0.
  - FP13: deriving the four separator constants.
  - FP14: the core's constants.
  - FP15: the dark sector's constants.
  - FP16: re-accretion.

Running here:
- **XR18:** an adversarial well-posedness audit of H_Y. It covers the yield surface, a DE12-type second variation,
  the leaf-average nonlocality, the degree-of-freedom count, and growth across the yield.
- **XR19:** does the fluid's own conversion run away through the cosmic web? XR12 and XR16 both flagged this, unscored.
- **XR20:** can a₀ and Λ come from one field? It tests unimodular Λ, a 4-form, K, sequestering, and evolving dark
  energy against the a₀(z) evidence.
- **XR21:** the chain's model in a particle-mesh box. Stage 1 (build and code tests) is running. Stage 2 (H_Y's
  nonlinear cosmology) waits on XR18 and FP13. Stage 3 (conversion with re-accretion) waits on XR19.
- **FP10_FULL:** the chain's full grid, launched here. The chain lead commits its outputs.
