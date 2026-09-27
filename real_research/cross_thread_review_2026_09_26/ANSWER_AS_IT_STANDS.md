# The answer as it stands: ASSEMBLING

2026-09-26/27. This page is assembled from the parallel threads' results. Every row cites a lane and a commit, or
says it is pending. The owners' own rows are in [ANSWER_ROWS_RECEIVED.md](ANSWER_ROWS_RECEIVED.md). **The closure
target is OPEN.** κ = ½ is a declared input. The dark mass is required.

**Consistency gate.** `XR10_answer_validator.py` traces every scorecard row's model from source. **No scorecard row
is yet computed on M\* itself.** Each is off on a stated axis, listed in §3. The same-model runs that close those gaps
are queued (§6).

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
  - **V0 is not yet a complete action.** Its region gate is an open obstruction once varied (DE12 7f84b3546,
    DE13 6daea932c). The data passes use the gate as a prescribed mask.
- **MOND.**
  - The kernel is ν_mono, declared; it equals ν_RAR for y ≤ 2.337, with a largest gap of 0.0104 dex.
  - It is heat-filtered and region-local (L361, σ = 1; σ is negligible for KiDS and Harvey).
  - a₀ = κc√(Gρ_Λ) with κ = ½ declared, so a₀ is flat in time.
- **The switch.**
  - It reads the MOND sector only, in CV3's constrained form C[∇²(u−v) + ∇·((ν−1)∇Sw)]. That is carrier-blind
    (MS1) and has a gate-independent constraint determinant (CV3).
  - The vacuum gate is x_c,eff(z) = x_c0[Ω_Λ0/Ω_Λ(z)]^p, with p = 1, x_c0 = 2.5 and w ≤ 0.25 (DE2/DE9).
  - MS5's κ-form cap, U_cap = C·m(∇²Φ_X, v_cap² κ_X²), ends every region at v_cap/(H√x_c): 1.75 Mpc at z = 0.5,
    2.99 Mpc at z ≈ 0. v_cap = 325 km/s is declared. The κ form has not yet been rebuilt on the constrained fields
    (XR10's flag).
- **The dark mass** is a new field (FL1 40c6ae144, FL2 e96b71eb0, FK1 c2e1fa119; XR8).
  - **What it is:** a superfluid order parameter Φ, one complex scalar. It feels Newtonian gravity only (reciprocity
    holds). Its phase is not the khronon (CV4: the leaves are CMC; the phase winds at nodes).
  - **XR8:** the only continuum that passes shell crossing is a nearly free, coherent complex wave field. Every
    single-velocity fluid fails.
  - **"Not particles"** here means a classical coherent field at occupation ~1e76–1e88 per de Broglie cell. Its quanta
    would still be bosons of mass m ≳ 1.9–5.2e-19 eV. The amount is set by initial data, not derived.
  - **The kick (FK1/FL2):** a U(1)-breaking mass term ε Re(Φ²) splits Φ in two, and λ(K)(Im Φ²)² converts
    φ_Hφ_H → φ_Lφ_L into back-to-back waves at v_k.
    - ε/m² = 1.84–2.35e-6 is FITTED to the kick window 575–650 km/s.
    - The trigger is the fluid's own n², sharp by Bose stimulation.
    - The coupling is vacuum-gated through K with q = 1.75, force-free on CMC leaves. The leaves do not fold.

## 2. Field content and constants (V0 writer's list)

| Content | Status |
|---|---|
| g_μν: 2 tensor modes | derived |
| khronon τ: 1 propagating scalar | declared |
| constrained auxiliaries (U, W, L, λ₀; Y = w, Ψ, V = v, Λ_d) | no propagating DOF; the full Dirac count is XR3 calc 2, still open |
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
| c₂ | declared, in tension across the record (L340's window 7.3e-3–0.067 against Planck's ≤ 0.6–2.9e-3; KM1 needs ≫ 1e-4) |
| ν_mono (δ = 0.05) | declared |
| the gate W | declared; obstructed when varied |
| m_d ≥ 2–5e-19 eV | declared |
| ε | FITTED |
| λ₀, q = 1.75 | declared |
| the dark amount and its misalignment (within ~14° of φ_H) | declared |

## 3. Scorecard (every row nearby-M*; the axis that keeps it off M* is named)

| Gate | Verdict | Numbers | Lane | Off M* on |
|---|---|---|---|---|
| Flat-a₀ flagship, z = 2.5 | **not established** | passes only if the carrier is fully cleared at r_F (S ≤ 0.059). L388's measured z = 2 residue, S = 0.063–0.075, gives +0.106 to +0.126 dex | MS2; flag from the advancement thread | carrier: S set to 0 by hand; the r_F residue is unmeasured |
| KiDS-1000, carrier lensing included | pass | −37.0/−34.0 (hard), −32.3/−29.3 (w 0.25) | DE10 dabce1b73 | carrier: L375's shell model, not L388's |
| Cosmic shear, halo model, κ cap | pass | 1.049/1.124 (w 0.25). Uncapped fails at 2.7/3.2 | MS3/MS4/MS5 | epoch: retention taken at z = 0/2, scored at z = 0.5 |
| Lyman-α forest | pass (conservative argument) | worst 0.0041 | DE11 aa6588d56 | cap and carrier absent; the operator over-states the phantom |
| RAR, RC100 | pass | carrier shift ≤ 1.24e-4 dex | L391 441d811e2 | switch absent; L376's carrier |
| S₈, clearing, X-COP | pending | — | L396 (κ cap, 575/600/650) | canonical footing only |
| Harvey | knife-edge | S2 passes only at 575 km/s (provisional) | L389 → L397 | L370's absolute matter mask |
| EFE, cluster-infall BTFR | **fails** | 2.2–6.3σ (κ-form re-score, XR9) | XR9 | (none) |
| EFE, LV dwarfs | **fails** | 3.9–4.5σ | XR6/XR9 | (none) |
| Local Group zero-velocity radius | **fails** | +0.18 to +0.24 dex | XR9 | (none) |
| Coma UDGs | **fails** | 4.2–4.3σ | XR9 | (none) |

## 4. Doors closed today (tried, failed, recorded)

- **Switch readings.**
  - Matter-only fails KiDS everywhere (DE8, L392).
  - Curvature leaks onto the carrier and makes lensing differ from dynamics (MS1, DE7).
  - A K-only gate is blind (CV4).
- **Action-level repairs of the MOND-sector gate** (DE13).
  - A gradient stiffness on f destabilises longer scales.
  - A gradient stiffness on U costs 32 v_f² at r_F and 2e8 v_f² at the Sun.
  - An acceleration-reading gate breaks ν_mono's monotonicity.
- **Region sizes.**
  - The small-region door (XR9): KiDS needs ~1.5 Mpc regions around L* galaxies, while the Local Group needs
    ~0.8–1.1 Mpc. The two passing sets are disjoint.
  - Shrinking regions leaves the EFE worse.
- **Caps and carriers.**
  - The withdrawn cap form fails shear (MS5). "One number sets the cap and the kick" is false (XR7).
  - GP4's window is withdrawn (PAPER34 v3). The acceleration-triggered carrier fails shear (AT4). L373 at p = 2 has
    no window. Astra's w = 1 gate has no window (DE9).
- **Fluids.**
  - Every single-velocity continuum fails shell crossing (XR8), and L374's runaway is not the kick.
  - Mock-based cosmic-shear passes are not established (MS3, DE5b).

## 5. Data gates ahead

- Gaia DR4, 2026-12-02 (frozen pre-registration).
- The z ≈ 2.5 deep-MOND Tully–Fisher zero point: needs JWST and ALMA.
- Euclid DR1, 2027.

## 6. Pending, and who owns it

**Same-model confirmation**, which moves §3's rows onto M*:
- L396: the κ cap at 575/600/650 km/s, three boxes. It supplies z = 0.4 retention, which fixes the shear epoch.
- L397: Harvey at its own epoch.
- KiDS re-scored with M*'s carrier at galaxy scale: the DE thread and the advancement thread.
- The flagship's r_F residue: FK2 (the fluid's own conversion) or AT5 (an added acceleration channel).

**The author's "fluid of dark energy swirling down between the bands", all four readings:**
- XR11: the edge layers. Can the dark fluid carry the gate's stiffness, and does the MS1 edge force clear galaxies?
- XR12: filaments. Conversion in infall streams; spin.
- FK2: the two energy levels. Where the drop happens, and whether r_F is cleared.
- FL3, the clock's slices: **done** (ba60f163f). The dark fluid swirls through quantised vortices (spacing
  ~150–190 pc at 2e-19 eV) without disturbing the clock: δK/K ≤ 1.1e-3, no vorticity reaches τ, and criterion B
  holds.

**Repairs of V0's gate obstruction.** DE13's completion (a7abb4d4f, e9a9978f9) proves no gradient energy of any
strength works (E3; Lean 8 theorems). What remains:
- XR15 (running here): door (c), a smoothed gate variable.
- CV6 (queued here): a dynamical gate field χ with a spring. Its price is edge-layer gas with a fast sound speed of
  0.4–8c on times < 100 Myr, plus a new gravity-sector field of ~1e-30 eV. Its decisive test is whether the WHIM
  and accretion shocks tolerate that.
- Flag: massive galaxies (1e12) at z ≳ 4 may lose MOND at r_F (DE12's profile). This limits the flagship's scope;
  the JWST regime (z ≲ 2.5, low mass) is unaffected.

**Open doors from DE13, not yet sized (superseded by the list above):**
- (b) h(U)|∇U|², switching off inside collapsed regions.
- (c) a smoothed gate variable, (1−ℓ²∇²)χ = U.

**Also pending:**
- L394: M*'s switch and cap with L372's two-mode carrier, a labelled variant.
- L393: the curvature comparison.
- AT5: a labelled alternative carrier.
- DE11b: the forest's convergence check.
- PAPER34 v3: the source is ready; the upload waits for the author's go.
