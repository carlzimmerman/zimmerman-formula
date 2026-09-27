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
- FP12 (59e537955), the verdict is mixed:
  - the Local Group, M81 and IC 342 share a +0.20 dex R0 overshoot (p = 0.93);
  - the 14-group stack sits at +0.12 to +0.14 dex;
  - Cen A matches;
  - it predicts R0(M83) = 1.24/1.28 Mpc.
- FP18 (09990b398), a data-only test: is the KiDS vs local-flow R0 pincer in the data itself? **UNDECIDED.**
  - At face value, no single mass profile fits both, at 9.8σ. KiDS needs more than 5.9e12 M☉ inside 0.76 Mpc,
    while R0 = 0.93 Mpc allows at most 1.44e12.
  - Profiling the comparability systematics (galaxy type, isolation, stellar-mass scale and others) cuts it to 2.3σ.
  - **LCDM shares the pincer.** Its KiDS-fitted halos turn around at 1.85–1.94 Mpc, against 0.91–0.93 observed.
    So the R0 overshoot does not single out the chain.
  - The R0 errors used so far were too small: ±0.12 for the 14-group stack, not ±0.02. FP12's offsets stand, but
    its significances are overstated.
  - The decisive measurement is FP21: lensing around spectroscopically isolated spirals at 0.3–1.5 Mpc.
- **Bug found (FP18):** FP6's KiDS projection (esd_of_M) under-projects the lensing signal, by 59% at 35 kpc and
  5–14% at 0.3–2.6 Mpc.
  - It feeds the chain's KiDS scores (FP1, FP6, FP9, FP11–FP14), and also the record's L355 and AT3.
  - FP20 is fixing it and re-scoring. Until then the chain's KiDS passes are provisional.
  - M*'s KiDS path (DE8 → DE10 → XR9 → XR14) uses a different projection and is not affected.
- FP13 (27faacc84) replaces FP9's four constants with readouts of the state (the separator H_S).
  - What is still chosen by hand:
    - δ_c, which can sit anywhere in 1.3–2.6;
    - c_y = 1;
    - the form of the onset ramp. MOND's yield switches on when the cosmic expansion starts to accelerate, at z = 0.635.
  - Semi-analytic scores, with a standard ΛCDM nonlinear field (halofit) standing in:
    - σ₈ 1.018–1.023, forest 0, flagship ≤ 0.013 dex, SPARC 1.8e-3;
    - KiDS −6.2/−7.7. This includes z = 0.4, where FP9's cell fails at +20.6.
  - The pass holds only if the action reads the actual nonlinear matter field.
  - The Local Group still fails (R0 1.54 Mpc).
- FP14 (03db97f14) takes the gravity core down to one knob (ξ) plus one regulator (α_c).
- In flight on the chain lead's side:
  - FP12: other groups' R0.
  - FP15: the dark sector's constants.
  - FP16: re-accretion.
  - FP17: ξ.

Running here:
- **XR18 (53854a459): H_S is linearly ILL-POSED as written at z ≤ 0.635.** Its leaf-averaged state term feeds an
  O(1) local force into the lapse and φ equations. On FP13's own headline state that force flips the sign of the
  constraint on k = 0.12–1.62 h/Mpc. FP13's "adds no local term" does not hold at the action level.
  - H_Y is linearly healthy: criterion B holds, and there is no DE12-type term. But it fails KiDS at z = 0.4.
  - The chain lead is repairing H_S in FP19, testing both of XR18's directions: B fixed by stationarity, or a
    readout through <K>_h only. XR21's stage 2 waits for the repaired term's re-audit.
- **XR19:** does the fluid's own conversion run away through the cosmic web? XR12 and XR16 both flagged this, unscored.
- **XR20 (a075ad7f7): a₀ and Λ can be TIED through one field; κ stays fitted.**
  - **The tie that works:** in unimodular gravity (Henneaux–Teitelboim), dΛ = 0 is a field equation. So
    a₀ = κc√(Gρ_Λ) is exactly constant on every solution, with no new local mode and with FRW and PPN unchanged. This
    moves FP5's "a₀ POSTULATED" to "a₀ TIED". The tie is to the unimodular constant: a separate vacuum energy would
    shift the observed Λ but not a₀.
  - **Routes that fail or don't tie:**
    - A four-form: the kernel folds and becomes unstable (ω² < 0). The unstable band covers 7.6% of SPARC points and a
      561–3036 AU shell around every solar-mass star.
    - The khronon's K: a₀ tracks H(z), the rival law.
    - Sequestering: a₀ is constant but not tied.
  - **Evolving dark energy:** a field tie reads V = (ρ − p)/2, not ρ_DE.
    - A healthy thawing field makes a₀ rise into the past, by +0.07 to +0.16 dex at z = 2.5. That would erode the
      z ≈ 2.5 test.
    - The DESI fits cross w = −1, which only a ghost field can follow.
    - Under the unimodular tie with a true cosmological constant, a₀ stays flat.
  - **Correction to the κ-closure record, confirmed by XR31 (c1932dcf8):**
    - k04's four-form promotion is UNSTABLE for 2.39 < g_N/a₀ < 155. F6 cannot fail, so it never tested stability.
    - The unstable band covers 17% of SPARC points, a shell from 639 to 5154 AU around every solar-mass star, and
      wide binaries at 2–5 kAU.
    - A correction note now sits beside k04 (`kappa_closure/k04_F6_CORRECTION_2026-09-27.md`).
    - PAPER6 (DOI 10.5281/zenodo.22559892) carries the F6 claim, the "205 AU" figure (should be about 639 AU) and
      the 2 kAU wide-binary shift. The DR4 pre-registration's Amendment 11 records the same variant (without
      registering it). An erratum or amendment is the author's call.
- **XR21:** the chain's model in a particle-mesh box.
  - Stage 1 (build and code tests) is running. It now includes H_S with its readouts computed on the fly from the box's
    own matter field, plus a frozen-readout control.
  - Stage 2 (the separator's nonlinear cosmology) is on hold until FP19's repaired term passes a re-audit.
  - Stage 3 (conversion with re-accretion) waits on XR19.
- **FP10_FULL (df13605e0), done:** the dark-sector window hinges on re-accretion.
  - With conversion in place, 0 of 12 cells pass: X-COP fails at every kick, and cosmic shear fails.
  - In the optimistic (history) reading, 6 of 12 pass, at 575 and 600 km/s.
  - The flagship passes in the history reading, at ≤ 0.0005 dex.
  - FP16 (semi-analytic) and XR21's stage 3 (particle mesh) decide which reading holds.
- **XR19 (b55775ce0): the fluid's own conversion spreads through the web, but not everywhere.**
  - It spreads through collapsed and turned-around structure at z ≲ 1.5. It stays out of voids (exactly, in expanding
    flow) and out of z ≳ 3 (the vacuum gate).
  - 84–91% of the fluid is converted by z = 0. The rest streams at 200–400 km/s, leaving galaxies and groups, and
    clusters recapture it.
  - S8 comes out at 0.931 of LCDM, which passes.
  - Small-scale carrier power falls 2.5–3.5×, so weak lensing leans on the MOND phantom.
  - The forest is still not established.
  - A box run needs a web conversion channel.
- **The hardest open tests of the chain, launched 2026-09-27:**
  - **XR22, Gaia DR4 wide binaries.** It solves the chain's z = 0 law as a 3-D AQUAL two-body problem in the Galactic
    field, with the heat filter across ξ's window. It then computes the frozen pre-registration's own statistic
    (read-only), to see whether DR4 still tests the chain.
  - **XR23, the first massive halos.** Spherical collapse and the mass function in the chain's law at z = 6–20,
    against the knob-free baryon limit for JWST's earliest massive galaxies.
  - **XR24, the Local Group by numerical action.** A 3-D fit of the local Hubble flow, with the neighbouring groups'
    tides, to see whether R0's overshoot survives.
  - **XR25, strong fields.** Preferred-frame PPN, neutron-star sensitivities, and binary-pulsar dipole radiation on
    FP14's core. It also asks whether the constant-mean-curvature leaves exist around neutron stars and black holes,
    and what the GW170817 dipole bound gives.
  - **XR26, the CMB and BBN.** Do the chain's linear equations reduce exactly to GR + CDM at z ≳ 10? It computes the
    TT/TE/EE and lensing spectra against Planck, plus Y_p, D/H and ⁷Li. If gravity's cosmological strength differs
    from its local value, it also reports the implied H0 shift.
  - **XR27, the external-field systems.** M*'s three failures (cluster infall, the LV dwarfs, the Coma UDGs) and the
    systems that favour an external-field effect (Crater II, DF2/DF4, the M31 dwarfs, Chae's SPARC signal), all under
    the band-pass, as a function of L.
  - **XR28, cluster splashback.** Cluster outskirts with the two-phase dark sector and MOND cut beyond L: can the
    data pin L?
  - **XR29, the Milky Way's outer rotation curve.** The Gaia DR3 decline in the chain's law.
  - **XR30, one clock or two.** Can the khronon's constant-mean-curvature foliation and the unimodular clock be one
    structure?
  - **XR31, verifying the k04 correction.** An independent check of the claim that k04's four-form kernel folds.
  - **XR32, the S8 tension.** Does the conversion lower the S8 a weak-lensing survey would infer by the right amount,
    while keeping CMB lensing and cluster counts consistent?
  - **XR33, galaxy strong lensing.** SLACS lenses from baryons alone, and the IMF that requires.
