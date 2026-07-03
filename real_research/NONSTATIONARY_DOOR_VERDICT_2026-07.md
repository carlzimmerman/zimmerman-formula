# The Non-Stationary Door: Adjudicated (2026-07-03)

**Question.** The five-theorem chain (Ostrogradsky; Cassini/slip; the sign/state clause; the PT/frequency law; the gas clamp) closes covariant modified inertia under one standing assumption: **stationarity** of the bath state. The one uncovered corner — flagged as the live theory door, and independently the mechanism class of M.J. Luo, arXiv:2602.14515 (Feb 2026) — is: *can a **non-stationary** bath state, or a **finite-time/transient** response, produce a persistent δm < 0 (the MOND sign) in the galactic band without unexplained pump power?*

**Verdict: CLOSED — on all three sub-corners, adversarially verified, both a₀ footings.** The transient corner falls back inside Theorems III/IV. This extends the pentad to a **sixth theorem** (finite-time/non-stationary closure). One quantified residual door survives (§5).

Method: 3 compute lanes + 3 independent adversarial verifiers (each instructed to attack in *both* directions), 13 scripts, all exit 0, `real_research/reviews/nonstationary_2026_07/`. Workflow run `wf_b3d8ac83-a8c`.

---

## 1. Lane A — free fields are state-blind at ALL times (not just stationary ones)

**Claim proven (operator identity, then exact numerics):** for a worldline *linearly* coupled to a free (quadratic) bath, the response kernel — dissipation + mass renormalization — is the field **commutator**, a c-number at every finite time, for **every** bath state (Gaussian or not) and for **every non-stationary linear dynamics** (time-dependent couplings, time-dependent frequencies/parametric drive). The state enters only the noise kernel.

- Symbolic: sympy-exact Heisenberg/Duhamel solution; no stationarity used anywhere (`laneA_symbolic_state_blindness.py`).
- Numeric: N=200-mode ohmic bath; kick response identical across vacuum / thermal / squeezed / oscillating-squeezed / coherent to 2.4e-13 while noise kernels differ ×5 and oscillate (`laneA_numeric_finite_bath.py`).
- Verifier strengthening: exact Fock-space computation of ⟨[x(t),x(s)]⟩ in genuinely **non-Gaussian** states (Fock n=3, even cat): spread 9.8e-16, matches −i·sin(ωΔt)/ω. Parametric (FRW-like ω_k(t)) driving amplifies the kernel ×2.4 but stays state-blind (spread 2.6e-11); in-band kernel-engineering by cosmic parametric pumping needs pump rate 2Ω ≥ 6.5e-17 s⁻¹ vs available H → deficit **×35.9 (canonical H=1.807e-18 s⁻¹) / ×29.7 (alternate H=2.182e-18 s⁻¹)** (`verify_A_freefield_kernel_and_sign.py`).
- Honest transient kept: a sudden coupling quench mimics μ<1 enormously (μ(0⁺)=−62.5) but dies in ~1 drive period (~1/t tail, 11.4% residual of the *positive* asymptotic shift at 10 periods), is suppressed ×6e7 by adiabatic switch-on, is state-blind anyway, and the asymptote is μ_∞=1.116>1 — **anti-MOND**.

**⇒ The dS vacuum + free fields can never give a state-engineered MOND sign — stationary or not.** The door, if open at all, lives only in nonlinear/structured baths (confirmed boundary: anharmonic bath or nonlinear coupling makes the kernel state-dependent — spread 1.5e-1 vs 3e-16 harmonic control).

## 2. Lane B — transient gain is real; its power bill is the same wall

**Confirmed (two independent methods):** transient δm<0 **exists** — inverted TLS gives δm(0)=−0.36 (analytic −2g²ω₀|w|/(Ω²(ω₀²−Ω²)), re-derived symbolically and by dissipator-free RK4), dying at T₁; resonant phase-locked coherence gives δm<0 at *first* order in g, dying at min(1/Γ₂, 1/|ω₀−Ω|); 5% detuning flips the sign in ~10 periods. Theorem IV is confirmed *stationary-only*: the transient lives in the homogeneous sector, no sub-Ω pole needed — **the door is genuinely ajar for ~one decay time.**

Then the bill (galactic band Ω = v/R ∈ [3.2e-17, 1.9e-14] rad/s; 10-orbit persistence = up to 3.5 Hubble times):

- **Coherence discount over inversion is ≤ ×2, exactly** (Liouvillian: Γ₂ = Γ₁/2 + Γ_φ; |ρ_ge| ≤ √(p_e p_g) — computed, not assumed). The ×2.9e10 inversion pump shortfall is reproduced (band-dependent 1.8e5 slow edge → 3.8e13 fast edge).
- **Redshift-drift dephasing** of horizon-tied in-band modes (Γ_φ ≈ 14.7 H₀ canonical / 16.1 H₀ alternate) makes the coherence route ~**4.9–5.4× worse**: S_coh ∈ [1.46e10 best case, 1.42e11–1.56e11 at the drift floor]; footing spread ×1.10. (Verifier softened one lane over-claim: drift kills ~99.9% of the deep-MOND grid, ×1.1-marginal at the fast corner, not literally 100%; the evading sliver is near the a₀ boundary and still budget-walled.)
- **Verifier's own open-direction attack, then closed:** a *free one-shot* prepared transient would survive 10 orbits in 85% of deep-MOND at the most generous Γ₂=H floor — but the **preparation** bill was implicit: dS-drift in-band occupancy |β|² = 3.2e-12 at band-mid → O(1) inversion is **~3e11 short even ONCE**; max coherence amplitude ≤ 1.8e-6 even granting full phase lock.
- **Universality kill (independent):** covering the band resonantly needs a ~405-channel comb with per-star phase locking (self-locking collapses into the stationary c-number kernel of Theorem III), and the phase-random remainder heats disks **×342–788** in σ_v (both footings). In-disk raw-energy headroom is only ×2.1.

**⇒ Transient/coherence gain cannot be prepared once, nor regenerated, in the deep-MOND band — it reduces to the same dS-drift delivery wall (~10 orders).**

## 3. Lane C — Luo's finite-time broadening: shape YES, sign NO, scale NO

Reconstructed from first principles (Gaussian-windowed Unruh–DeWitt response on Rindler/dS worldlines; Planck limit reproduced to 2e-4):

- **The broadening is real and Deser-Levin-like:** a_eff² = 1.003·a² + (H²) + κ²c²/T_win² with κ = 1.746 (max residual 0.1%). Luo's mechanism is a genuine finite-time generalization of dS-Unruh.
- **Shape — an honest WIN for the framework:** sympy-exact identity — the ΔT mapping μ = [√(a²+a_Λ²)−a_Λ]/a inverts **exactly** to the framework's g_obs = √(g_bar² + g_bar·a₀) with a₀ = 2a_Λ. The framework's ν(y)=√(1+1/y) *is* the unique dS-Unruh ΔT shape.
- **Sign — postulated, not derived:** Wightman positivity forces the windowed response F(ω) ≥ 0 for **any** window; the exact identity **F(−ω) − F(ω) = (ω/2π)∫χ²** (verified to 4e-16, and re-derived by the verifier from the universal Hadamard coincidence structure) is **trajectory-universal and window-universal** — no transient protocol produces population inversion from the vacuum. Tested adversarially on Luo's actual case (non-uniform acceleration bursts), sharp top-hat windows, and parametric/dynamical-Casimir pumps: max p_e/p_g = 0.540 < 1. Fed through the dynamical dressing, δm ≥ +0.65 on the whole (a, T_win) grid; windowed QBM confirms Pusz–Woronowicz passivity under arbitrary transient switching. **The MOND sign enters only via the μ~ΔT/T mapping — exactly as in Milgrom 1999.**
- **Scale — velocity-dependent, and floored:** the orbital stationarity window T=1/Ω gives a_T = κ·c·v/R, i.e. a_T/a_cent = κc/v ≈ 1,700–17,000 for v=30–300 km/s — **not universal**, and 2–5 orders above a₀ everywhere in disks (a_T/a₀ = 1.8e2–1.1e5 canonical; 1.5e2–9.0e4 alternate). The only window reproducing a₀ is T* = κc/a₀ ≈ 177 Gyr (canonical) / 147 Gyr (alternate) = **10.1/H on both footings** — the stationary limit Theorems III/IV already cover.
- **Verifier strengthening — the cH floor:** all quadrature coefficients are positive, so **a_eff ≥ cH for every window and every trajectory**. The forced Deser-Levin normalization is a₀_DL = 2cH = 2Z·a₀ = **11.58× the framework's canonical a₀** (both footings; 9.0× the empirical 1.2e-10). The framework's a₀ = cH_Λ/Z sits a factor Z = 5.79 **below the floor — unreachable from the transient side, period.** (Consistent with, and sharpening, the κ-closure: the coefficient remains underived; broadening can only overshoot it.)

**⇒ Luo's mechanism supplies the framework's exact interpolation *shape* and a clean *scale window*, but the sign is postulated by the mapping and the genuinely non-stationary scale is velocity-dependent — his corner falls back inside Theorems III/IV once made dynamical.**

## 4. The sixth theorem (statement)

> **Theorem VI (finite-time/non-stationary closure).** For a worldline coupled to any bath: (i) if the coupling is linear and the bath free, the response kernel is a state-independent c-number at all finite times, under all states and all non-stationary linear dynamics — no state engineering, transient probing, or parametric cosmic driving (in-band deficit ×30–36 on both footings) yields δm<0; (ii) if the bath is structured/nonlinear, transient δm<0 exists but persists only for min(T₁, 1/Γ₂, 1/detuning), and both its one-shot preparation (×~3e11) and its regeneration (S_coh ~ 1.5e10–1.6e11, coherence discount ≤×2, drift floor ×5 penalty) in the deep-MOND band exceed the universe's non-stationarity budget by ~10 orders, while band coverage forces a resonant comb whose phase-random component over-heats disks ×342–788; (iii) finite-time spectral broadening of the vacuum is real and Deser-Levin-shaped but positivity-locked (F(ω)≥0, F(−ω)−F(ω)=(ω/2π)∫χ² for all windows and trajectories) with effective scale floored at cH = Z·a₀ — it supplies shape and scale-window, never the sign, and its non-stationary transition scale is velocity-dependent (κc/v), not universal.

**Scale yes, shape yes — sign, still no.** The pentad is now a hexad.

## 5. The doors that remain open (per standing rule: there are always doors)

1. **Dynamically unsettled systems (the Luo-type residual, now quantified):** one-shot transients contribute ~**1.6% per 10 orbits** — nothing for the RAR (settled disks), but potentially *distinctive* in recently-perturbed populations. This lands exactly on the framework's live **non-adiabatic relational σ-spread** front (MI 6–13%, MG exactly 0): a MOND-amplitude–vs–dynamical-settledness correlation is the observable. Underpowered today; not closed.
2. **Interacting-field windowed response** (both verifiers' named mind-changer): the positivity identity was proven for free fields pulled back to worldlines; a genuinely interacting-field windowed calculation exhibiting inversion without violating Pusz–Woronowicz would reopen (iii). No candidate exists; the burden is now a specific calculation.
3. **The data doors are untouched by all of this:** s̄^TX (Gaia-independent, dedicated-fit floor σ_A~4.3e-11), Gaia DR4 wide binaries (~Dec 2026), DESI DR3 w(z), a₀(z)/BTFR-sign at high z, BIG-SPARC population split.

## 6. What this means for arXiv:2602.14515 (one citable paragraph)

Luo's finite-time broadening is a real effect and independently lands on the same de Sitter–Unruh quadrature this framework postulates — the ΔT-mapping shape is *exactly* ν(y)=√(1+1/y) with a₀=2a_Λ. But (a) the reduced-inertia **sign** in that construction enters through the Milgrom-1999-type mapping, not dynamics: for any window and any trajectory the windowed vacuum response obeys F(ω)≥0 and F(−ω)−F(ω)=(ω/2π)∫χ², so no transient protocol inverts populations, and the dynamical dressing stays δm≥0 (vacuum passivity); (b) the genuinely non-stationary scale the mechanism *does* produce is window-locked to the orbit, a_T = κcv/R — velocity-dependent, 2–5 orders above a₀ in disks — while every window's effective scale is floored at cH = Z·a₀ ≈ 11.6×(a₀/2); the only a₀-reproducing window is ~10/H, the stationary limit. A mechanism-level discriminator follows: if the interpolation scale were window-generated, the RAR transition would migrate with c/v across galaxy populations; SPARC shows it does not.

---

## Scripts (all exit 0, adversarially re-run)

| Lane | Scripts |
|---|---|
| A | `laneA_symbolic_state_blindness.py`, `laneA_numeric_finite_bath.py`, `laneA_nonlinear_boundary.py`, `verify_A_freefield_kernel_and_sign.py` |
| B | `laneB_transient_gain_model.py`, `laneB_band_persistence.py`, `laneB_phase_conspiracy.py`, `laneB_regen_budget.py`, `verify_B_structured_adversarial.py` |
| C | `laneC_finite_time_response.py`, `laneC_sign_audit.py`, `laneC_scale_audit.py`, `verify_C_luo_adversarial.py` |

Footing fork carried throughout: canonical a₀ = 9.36e-11 (cH_Λ/Z, ρ_DE) vs alternate 1.13e-10 (ρ_total/cH₀); every verdict above is footing-stable (spreads printed in-script, ≤×1.10 on budgets, 20.7% on H).

*C.P.Z. + Fable 5 fleet, 2026-07-03.*
