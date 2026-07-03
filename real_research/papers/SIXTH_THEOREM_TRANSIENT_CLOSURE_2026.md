# Scale Yes, Shape Yes, Sign No: A Sixth Theorem Closing the Finite-Time/Non-Stationary Corner of Covariant Modified Inertia

**Carl P. Zimmerman** (Briar Creek Tech)
*2026-07-03. Companion computations: 13 scripts, all exit 0, adversarially re-run, at* `real_research/reviews/nonstationary_2026_07/` *in the supplementary repository.*

---

## Abstract

A five-theorem chain (Zenodo 10.5281/zenodo.21016309, 21139029, 21148494, 21152331) closes covariant modified inertia (MI) as a realization of MOND — under one standing assumption: **stationarity** of the environment's state. The uncovered corner is the natural next question, and it is also the mechanism class of a concurrent proposal (M.J. Luo, arXiv:2602.14515, Feb 2026): can a **non-stationary** bath state, or a **finite-time/transient** response, produce a persistent inertia *reduction* (δm < 0, the MOND sign) in the galactic band without unexplained power? We close it in three legs, each adversarially verified. **(i)** For linear coupling to a free field, the response kernel is the field commutator — a state-independent c-number at *all finite times*, for *all* states (including non-Gaussian; verified exactly in Fock and cat states) and all non-stationary linear dynamics (time-dependent couplings and parametric/FRW-type frequency drive); in-band parametric kernel-engineering is separately dead by a ×30–36 pump-rate deficit. **(ii)** For structured (nonlinear) baths, transient gain is *real* — we exhibit it two independent ways — but it persists only for min(T₁, 1/Γ₂, 1/detuning); in the deep-MOND band both its one-shot preparation (×~3×10¹¹ occupancy shortfall) and its regeneration (coherence discount over population inversion is exactly ≤ ×2, and the redshift-drift dephasing floor makes coherence ~5× *worse*) exceed the universe's non-stationarity budget by ~10 orders, while resonant band coverage forces a ~400-channel comb whose phase-random component over-heats disks ×342–788. **(iii)** Finite-time spectral broadening of the vacuum — Luo's effect — is real and we reconstruct it: the windowed de Sitter–Unruh response obeys an exact quadrature a_eff² ≈ a² + H² + κ²c²/T², κ = 1.746, whose ΔT-mapping shape is *exactly* this framework's interpolation ν(y) = √(1+1/y) (sympy identity, a₀ = 2a_Λ). But Wightman positivity locks the sign for **every** window and **every** trajectory: F(ω) ≥ 0 with F(−ω) − F(ω) = (ω/2π)∫χ², so no transient protocol inverts populations (adversarial maximum p_e/p_g = 0.54 for acceleration bursts with parametric pumping), the dynamical dressing stays δm ≥ 0, and the effective scale is *floored* at cH = Z·a₀ — the framework's a₀ = cH_Λ/Z sits a factor Z = 5.79 below the floor, unreachable from the transient side. The genuinely non-stationary scale the mechanism does produce is window-locked to the orbit, a_T = κcv/R — velocity-dependent (κc/v ≈ 1,700–17,000), 2–5 orders above a₀ throughout disks — which yields a mechanism-level discriminator: a window-generated interpolation scale would migrate the radial-acceleration-relation transition with c/v across galaxy populations, and SPARC shows it does not. Conclusion: finite-time de Sitter–Unruh physics supplies the *scale window* and the exact interpolation *shape*, and cannot supply the *sign*. The pentad is a hexad. One residual door is quantified, not closed: one-shot transients contribute ~1.6% per 10 orbits in dynamically *unsettled* systems — nothing for the RAR, but landing exactly on the framework's live non-adiabatic σ-spread front.

---

## 1. The question, and why it is the last theory corner

Theorems I–V close covariant MI from three sides: locality (Ostrogradsky), field-mediation (Cassini/slip), and the environment route — where the **sign/state clause** (Theorem III) proved that passive/KMS baths only *add* inertia, the **frequency law** (Theorem IV) proved in-band softening from a stationary ghost-free bath requires a sub-drive pole, and the **gas clamp** (Theorem V) destroyed the one four-theorem-compliant construction. Every one of those proofs assumes the bath state (or kernel) is **stationary**.

That assumption is not innocent. Lasers exist: a *non-stationary* medium amplifies. The real universe is not stationary: H(t) drifts. And a particle on a galactic orbit is not probed for infinite time: its acceleration vector rotates at Ω = v/R, so the physically relevant response is a **finite-window** response — precisely the generalization Luo (arXiv:2602.14515) proposes, where short-time acceleration broadens spectra beyond the stationary Unruh result and the broadening is read as the MOND interpolation.

So the corner is sharp: **transient or non-stationary physics, in the galactic band (Ω ∈ [3.2×10⁻¹⁷, 1.9×10⁻¹⁴] rad/s; 10-orbit persistence = 10⁸–10¹⁰ yr, up to 3.5 Hubble times), with the universe's actual non-stationarity as the only free power source.** Throughout, both coefficient footings are carried: canonical a₀ = 9.36×10⁻¹¹ m/s² (cH_Λ/Z, ρ_DE) and alternate 1.13×10⁻¹⁰ (ρ_total/cH₀); every verdict below is footing-stable (spreads ≤ ×1.10 on budgets; 20.7% on H).

## 2. Theorem VI (statement)

> **Theorem VI (finite-time/non-stationary closure).** For a worldline coupled to any environment:
> **(i)** if the coupling is linear and the environment a free (quadratic) field, the response kernel (dissipation + mass renormalization) equals the field commutator — a state-independent c-number at all finite times, for all states and all non-stationary linear dynamics. No state preparation, transient probing, or parametric cosmic driving yields δm < 0; the in-band parametric escape fails by ×30–36 on both footings.
> **(ii)** if the environment is structured/nonlinear, transient δm < 0 exists but persists only for min(T₁, 1/Γ₂, 1/|ω₀−Ω|); in the deep-MOND band its one-shot preparation is short by ~3×10¹¹ in occupancy and its regeneration by ~10 orders in power (coherence discount ≤ ×2 exactly; redshift-drift dephasing floor Γ_φ ≈ 15 H₀ makes coherence ~5× worse than inversion), while resonant band coverage requires a ~405-channel comb whose phase-random component over-heats disks ×342–788.
> **(iii)** finite-time spectral broadening of the vacuum is real and Deser–Levin-shaped, but positivity-locked: for every window and every trajectory F(ω) ≥ 0 and F(−ω) − F(ω) = (ω/2π)∫χ², so populations never invert, the dressing stays δm ≥ 0, and every window's effective scale obeys a_eff ≥ cH = Z·a₀. The broadening supplies the interpolation *shape* (exactly ν(y) = √(1+1/y)) and a *scale window*, never the *sign*; and its genuinely non-stationary transition scale is velocity-dependent (κc/v), not universal.

**Scale yes, shape yes — sign, still no.**

## 3. Leg (i): free fields are state-blind at all times

The stationary state-blindness of free fields is an old friend; the finite-time, non-stationary version had to be checked, because "transient" is exactly where intuition expects loopholes.

**Operator identity (symbolic).** Solving the driven bath mode exactly (Heisenberg/Duhamel, sympy) for an *arbitrary* operator source and *time-dependent* couplings: the influence kernels split into a response part built solely from the commutator — a c-number for a free field, hence identical in every state — and a noise part where all state dependence (including genuinely non-stationary oscillating-squeezed covariances) lives. No stationarity is invoked anywhere. Because it is an operator identity, it covers non-Gaussian states too.

**Numerics.** An N=200-mode ohmic bath, evolved exactly: the kick response across vacuum / thermal (n̄=2) / squeezed (r=1) / oscillating-squeezed / coherent states agrees to 2.4×10⁻¹³ while the noise kernels differ by ×5 and oscillate in time. Adversarial verification replaced one numerically-tautological leg of this test with a direct Fock-space computation of ⟨[x(t),x(s)]⟩ in genuinely non-Gaussian states (Fock n=3, even cat): spread 9.8×10⁻¹⁶ against the analytic −i·sin(ωΔt)/ω.

**The honest transient, kept.** A sudden coupling quench *mimics* μ < 1 spectacularly — μ(0⁺) = −62.5 in our units — and this is exactly the class of effect a short-time argument gestures at. It dies in 1.02 drive periods, decays as ~1/t (11.4% of the *positive* asymptotic shift remains at 10 periods), is suppressed ×6×10⁷ by adiabatic switch-on, is state-blind anyway, and the asymptote is μ_∞ = 1.116 > 1: anti-MOND.

**The parametric escape, closed by budget.** One route evades state-engineering entirely: drive the bath *Hamiltonian* (FRW-like ω_k(t)) and engineer the kernel itself. Verified: the kernel is parametrically amplified (×2.4 achieved) while remaining a c-number — but in-band amplification needs pump rate 2Ω ≥ 6.5×10⁻¹⁷ s⁻¹, and the universe supplies H = 1.8–2.2×10⁻¹⁸ s⁻¹: deficit **×35.9 (canonical) / ×29.7 (alternate)**. Adiabatic kernel corrections are bounded at (H/Ω_min)² ≈ 3–5×10⁻³.

Free fields are therefore closed *unconditionally*: the dS vacuum plus free fields cannot give a state- or transient-engineered MOND sign. Any surviving door must live in structured/nonlinear environments — where the boundary was confirmed explicitly (anharmonic bath or nonlinear coupling makes the kernel state-dependent: spread 1.5×10⁻¹ vs 3×10⁻¹⁶ harmonic control).

## 4. Leg (ii): transient gain is real, and its bill is the same wall

We are not in the business of manufacturing deficits: **transient gain exists**, and we exhibit it two independent ways. An inverted two-level unit gives δm(0) = −2g²ω₀|w|/(Ω²(ω₀²−Ω²)) < 0 (confirmed symbolically via Kubo and by dissipator-free RK4 propagation: δm(ground) = +0.499, δm(inverted) = −0.499 against analytic 0.505); resonant phase-locked coherence gives δm < 0 at *first* order in the coupling. Theorem IV is genuinely stationary-only: the transient lives in the homogeneous sector and needs no sub-Ω pole. The door is ajar — for min(T₁, 1/Γ₂, 1/|ω₀−Ω|); a 5% detuning flips the sign within ~10 periods.

Then the accounting, in the only band that matters:

- **Persistence.** Deep-MOND (55%/59% of the band, canonical/alternate footing) needs ≥10 orbits — up to 3.5 Hubble times. No one-shot transient survives that at physical dephasing floors; ~99.9% of the on-grid deep-MOND volume is killed by redshift-drift dephasing alone (Γ_φ = 14.7/16.1 H₀), margin ×1.1 at the fast corner.
- **Preparation (the verifier's own open-direction attack, then closed).** Even granting a *free* one-shot: the dS-drift in-band occupancy is |β|² = 3.2×10⁻¹² at band-mid, so O(1) inversion is **~3×10¹¹ short even once**; maximal coherence amplitude √|β|² ≤ 1.8×10⁻⁶ even with perfect phase lock.
- **Regeneration.** The inversion pump shortfall S_inv = 2.9×10¹⁰ is reproduced (band-dependent 1.8×10⁵–3.8×10¹³). The hoped-for coherence discount is **exactly ≤ ×2** (Liouvillian: Γ₂ = Γ₁/2 + Γ_φ; |ρ_ge| ≤ √(p_e p_g) — computed, not assumed), and the drift floor makes coherence ~4.9–5.4× *worse*: S_coh ∈ [1.5×10¹⁰, 1.6×10¹¹]. Footing spread ×1.10.
- **Universality.** Covering the band resonantly needs ~405 tuned channels with per-star phase locking; self-locking collapses into the stationary c-number kernel of Theorem III, a single shared phase nets 1/√N* ~ 3×10⁻⁶ with a 50% anti-MOND sign, and the phase-random remainder heats disks **×342–788** in σ_v. In-disk raw-energy headroom: ×2.1.

The transient corner of structured baths thus reduces to the same dS-drift delivery wall the pumped steady state died on — now with the one-shot loophole explicitly priced.

## 5. Leg (iii): Luo's broadening — reconstruction, one honest win, two locks

We reconstructed the finite-time mechanism from first principles (Gaussian-windowed Unruh–DeWitt response on Rindler and de Sitter worldlines; the Planck spectrum recovered to 2×10⁻⁴ in the long-window limit).

**The effect is real.** The windowed response obeys an exact quadrature, a_eff² = 1.003·a² + H-floor + κ²c²/T_win², κ = 1.746 (max residual 0.1%): short-time acceleration genuinely broadens the spectrum in Deser–Levin form. On this point Luo is right, and it matters.

**The honest win.** Feeding a_eff through the ΔT mapping μ = [√(a²+a_Λ²) − a_Λ]/a and inverting yields — *exactly*, as a sympy identity — g_obs = √(g_bar² + g_bar·a₀) with a₀ = 2a_Λ. The interpolation this framework postulated in 2025 is the *unique* dS-Unruh ΔT shape. Two groups now arrive at the same functional form from the same physics independently; the shape is no longer a choice.

**Lock one: the sign is postulated, not derived.** Wightman positivity forces F(ω) ≥ 0 for any window, and the exact identity F(−ω) − F(ω) = (ω/2π)∫χ² — verified to 4×10⁻¹⁶, then re-derived adversarially from the universal Hadamard coincidence structure — is **trajectory-universal and window-universal**. Tested on Luo's actual case (non-uniform acceleration bursts), on sharp top-hat windows, and on parametric/dynamical-Casimir pumps: the maximum achievable p_e/p_g is 0.54 — no inversion, ever, from the vacuum. Fed through the dynamical dressing rather than the mapping, δm ≥ +0.65 across the whole (a, T_win) grid; windowed quantum-Brownian-motion checks confirm Pusz–Woronowicz passivity under arbitrary transient switching. The MOND sign in this construction enters where it entered in Milgrom (1999): in the postulated μ ~ ΔT/T map. The broadening dresses the *populations*; it never crosses them.

**Lock two: the scale is floored and velocity-dependent.** All quadrature coefficients are positive, so **a_eff ≥ cH for every window and every trajectory**. The forced Deser–Levin normalization is a₀_DL = 2cH = 2Z·a₀ = 11.58× the framework's canonical a₀ (both footings; 9.0× the empirical 1.2×10⁻¹⁰) — and since broadening only *adds* in quadrature, cH is a floor: the framework's a₀ = cH_Λ/Z sits a factor Z = 5.79 *below* it, unreachable from the transient side. This sharpens the κ-closure (10.5281/zenodo.20965016): the coefficient is not merely underived by this route — it is *excluded* by it. Meanwhile the genuinely non-stationary scale the window does produce is a_T = κ·c·v/R: a_T/a_centripetal = κc/v ≈ 1,700–17,000 for v = 30–300 km/s, putting a_T 2–5 orders above a₀ everywhere in disks. The only window that lands on a₀ is T* = κc/a₀ ≈ 177/147 Gyr (canonical/alternate) = 10.1/H on both footings — the stationary limit Theorems III/IV already govern.

**A mechanism-level discriminator falls out.** If the interpolation scale were window-generated, the RAR transition would migrate with c/v across galaxy populations — dwarfs (v≈30 km/s) and massive spirals (v≈300 km/s) would transition at accelerations an order of magnitude apart. SPARC's single, population-stable transition (the framework's own hierarchical fits, e.g. 0.108 dex at Υ=0.70) already rules this out. Any future finite-window MI proposal must explain why its scale does not carry the c/v fingerprint.

## 6. What this implies for arXiv:2602.14515

Luo's finite-time broadening is a real effect, and it independently lands on the same de Sitter–Unruh quadrature this framework postulates — indeed the ΔT-mapping shape is exactly ν(y) = √(1+1/y) with a₀ = 2a_Λ, which we regard as convergent support for the *shape*. But (a) the reduced-inertia sign enters through the Milgrom-1999-type mapping, not dynamics: for any window and any trajectory the windowed vacuum response obeys F(ω) ≥ 0 and F(−ω) − F(ω) = (ω/2π)∫χ², so no transient protocol inverts populations and the dynamical dressing stays δm ≥ 0 (vacuum passivity); (b) the genuinely non-stationary scale the mechanism produces is window-locked to the orbit and velocity-dependent (a_T = κcv/R, 2–5 orders above a₀ in disks), while every window's effective scale is floored at cH — the only a₀-reproducing window being ~10/H, the stationary limit. The mechanism therefore supplies scale-window and shape, not sign; and it inherits a falsifiable c/v fingerprint that SPARC already disfavors. We would be genuinely interested to be shown wrong on either lock — the named mind-changers are an *interacting-field* windowed calculation exhibiting inversion without violating passivity, or a dynamical (not chosen) lock of the window to ~10/H.

## 7. What remains open

Per this program's standing rule, closures are maps, and maps have edges:

1. **Dynamically unsettled systems (the quantified residual).** One-shot transients contribute ~1.6% per 10 orbits. That is nothing for the RAR — settled disks — but it is *distinctive* where relaxation is recent: the prediction is a MOND-amplitude–vs–dynamical-settledness correlation, landing exactly on this framework's live non-adiabatic relational σ-spread front (MI 6–13%, MG exactly 0). Underpowered today; open.
2. **Interacting-field windows.** The positivity locks were proven for free fields pulled back to worldlines (the verifiers' named boundary). A windowed *interacting*-field calculation showing inversion without violating Pusz–Woronowicz would reopen leg (iii). No candidate exists; the burden is now one specific calculation.
3. **The empirical fronts are untouched:** the fixed-direction s̄^TX ephemeris test (10.5281/zenodo.21137568), Gaia DR4 wide binaries (~Dec 2026), DESI DR3 w(z) (the a₀(z) hostage), high-z BTFR offset sign, and the BIG-SPARC population split (10.5281/zenodo.21140507).

## 8. Verification and scope

Every quantitative claim above is backed by a committed, runnable script (numpy/sympy, no network), all exit 0, each lane re-run and attacked by an independent adversarial verifier instructed to refute in *both* directions. Verifier corrections are printed beside the results they amend, per this program's practice: one numerically-tautological state-blindness test replaced with an exact Fock-space computation; one "100% of deep-MOND" claim softened to "~99.9% on-grid, ×1.1-marginal at the fast corner"; one verifier's own threshold bug acknowledged and fixed; and two strengthenings added (the parametric-drive extension of leg (i); the cH-floor form of lock two).

Scope: this note closes the finite-time/non-stationary corner of covariant modified inertia. It does **not** claim "modified inertia is impossible" beyond the mapped territory (the interacting-field window of §7.2 is the precise surviving edge), and it does **not** touch the a₀ = c²√(Λ/32π) reframing or its live empirical tests, which stand or fall on the data fronts of §7.3. The author retracted all earlier "theory of everything" claims (2026-06-23); this note claims a closure and two locks, not a completion.

## Script index

| Leg | Scripts (all `real_research/reviews/nonstationary_2026_07/`, all exit 0) |
|---|---|
| (i) | `laneA_symbolic_state_blindness.py`, `laneA_numeric_finite_bath.py`, `laneA_nonlinear_boundary.py`, `verify_A_freefield_kernel_and_sign.py` |
| (ii) | `laneB_transient_gain_model.py`, `laneB_band_persistence.py`, `laneB_phase_conspiracy.py`, `laneB_regen_budget.py`, `verify_B_structured_adversarial.py` |
| (iii) | `laneC_finite_time_response.py`, `laneC_sign_audit.py`, `laneC_scale_audit.py`, `verify_C_luo_adversarial.py` |

## References (chain)

- Zimmerman, C.P., *Scale Without Law*, 10.5281/zenodo.21016309 (Theorems I–II context)
- Zimmerman, C.P., *The Sign Premise Is a State Clause*, 10.5281/zenodo.21139029 (Theorem III)
- Zimmerman, C.P., *The Fourth Horn*, 10.5281/zenodo.21148494 (Theorem IV)
- Zimmerman, C.P., *The Kernel That Builds Its Own Laser*, 10.5281/zenodo.21152331 (Theorem V)
- Zimmerman, C.P., *κ-closure*, 10.5281/zenodo.20965016 (coefficient non-forcing)
- Luo, M.J., arXiv:2602.14515 (2026); and arXiv:2311.03397 (2023)
- Milgrom, M., Phys. Lett. A 253, 273 (1999) (the ΔT mapping)
- Deser, S. & Levin, O., Class. Quantum Grav. 14, L163 (1997)
- Pusz, W. & Woronowicz, S.L., Commun. Math. Phys. 58, 273 (1978)
