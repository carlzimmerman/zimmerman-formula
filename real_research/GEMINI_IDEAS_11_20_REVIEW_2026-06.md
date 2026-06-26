# Gemini ideas #11–20 vs the Zimmerman framework's established walls (2026-06-26)

*Both-ways triage of an external (Gemini) batch of TOE/derivation ideas against the framework's sympy-confirmed
no-go walls. Discipline: a genuine bypass = a real new door (credit + state the TEST + the next step); a re-route
into a named wall is stated decisively with the sign/regime/number where it bites. No reflexive dismissal, no
manufactured win. Numbers verified firsthand (see `/tmp`-style one-liners reproduced inline).*

Framework: **a₀ = c²√(Λ/32π) = cH_Λ/Z**, Z = √(32π/3) = 5.789, a₀ = 9.36×10⁻¹¹ m/s²; dS-Unruh **modified-inertia**
MOND; a₀ a **FORCED SCALE**, the MOND **sign + Z postulated**; theory side comprehensively closed.

## The established walls (sympy-confirmed, banked)

- **PASSIVITY → anti-MOND SIGN THEOREM.** Any causal + ghost-free + unitary cosmological source gives
  δm = 2∫ρ(ω)/ω² dω ≥ 0 (inertia RAISED = **anti-MOND**). MOND needs an **ACTIVE / gain** source (a band with ρ<0,
  i.e. T_b<0 / J_eff<0 / unsaturated-tachyon) that the **passive dS vacuum is not**
  (`NONEQUILIBRIUM_PASSIVITY_ESCAPE 2026-06-15`, `DOORA_REAL_NONEQUILIBRIUM_KERNEL 2026-06-26`,
  `ACTIVE_KERNEL_SIGNTHEOREM_2026-06`).
- **COVARIANT-MI TRICHOTOMY.** local = Ostrogradsky ghost / field = modified-gravity fails Cassini / nonlocal =
  passivity. No fourth box (`COVARIANT_MI_COMPLETION_2026-06`).
- **κ=½ UNFORCEABLE by continuous/dynamical probes** (ghost-freedom, unitarity, holography all κ-invariant;
  `KAPPA_FORCING_DOOR_CLOSED 2026-06-17`). **Left explicitly OPEN & out of scope:** a UV-complete embedding that fixes
  the overall action normalization by a **non-consistency principle** (microscopic dof count / **fixed-point boundary
  condition / index**). The closure is NOT topological/index — that door is un-closed.
- **SM MASS KERNEL-FREE** (gravity forces √(8π/3); the Yukawa sector has no forced kernel; `PARTICLE_BRIDGE_FRESH_EYES`).
- **MANNHEIM/WEYL conformal ALREADY KILLED** (mirages-killed list, `TOE_LITERATURE_MAP 2026-06-15`).
- **E8 has the DISTLER-GARIBALDI no-go** (0905.2658 Thm 1.3: no ToE subgroup in any real form of E8; 3 chiral
  generations + gravity cannot fit). Evaded for ONE family by a non-compact coset ≠ derived.
- **SME preferred-frame bridge INDUCES s_μν but is FLAVOR-BLIND** (the s^TX dipole is universal by the equivalence
  principle, gravity-sector; Koide r=√2 not derivable; `SM_BRIDGE_SME_LORENTZ`).
- **CLUSTER residual = shared-MOND gap with a DENSITY-VETO** (the AeST ghost-condensate dark sector HAS the mass but
  cannot be galaxy-safe AND cluster-clumpy at once; `project_ghost_condensate_dark_sector`).
- **U(N) matrix-model Path-6 did NOT select (3,2,1)** by anomaly/free-energy.

---

## (1) PER-IDEA TABLE

| # | Idea (short) | Wall it meets | Verdict | One-line reason | How to test with the framework |
|---|---|---|---|---|---|
| 11 | dS / Galileon-Vainshtein screening sets the MOND transition (a₀ as the Vainshtein scale) | COVARIANT-MI TRICHOTOMY (field-route = modified-gravity) | **HITS-WALL** | Vainshtein is modified-**gravity** (a fifth force screened at small r) — the **opposite topology** of the framework's modified-**inertia**, and the field route fails Cassini (the very box the trichotomy rules out); it also gives the wrong radial profile (screening turns MOND OFF inside r_V, MOND needs it ON below a₀). | Compute r_V = (r_s/m²)^{1/3} for the Galileon tuned so the crossover = a₀; check (a) Cassini quadrupole / s^TX bound on the residual fifth force in the solar system, (b) that the un-screened force has the wrong sign vs deep-MOND. Both already adverse in `CASSINI_QUADRUPOLE_CONSTRAINT` + the MG box of `COVARIANT_MI_COMPLETION`. |
| 12 | **dS-Schwinger pair-creation supplies the ACTIVE, MOND-signed kernel** | PASSIVITY → anti-MOND SIGN THEOREM (+ wrong-regime / threshold-direction) | **HITS-WALL** | Standout, deserved deep engagement, **re-routes** not evades: dS-Schwinger IS dS particle creation, pinned passive 3 ways. All three legs fail — wrong **scale** (threshold a_crit = 2πcH_Λ = **36.4 a₀**, and a₀ is **209× below** it), wrong **sign** (Bogoliubov noise 1+2\|β\|²≥1>0 ⇒ ρ≥0 ⇒ δm>0 = anti-MOND drag), wrong **regime** (Schwinger ∝ exp(−πa_crit/a) is an **above-threshold high-a** effect; MOND modifies **below** a₀). | (1) Read the threshold a_crit = 2πc·mc²/ħ for a dark quantum m=ħH/c²: = 36.4 a₀, never a₀ unless m hand-tuned. (2) Form the orbiting probe's retarded self-energy coupled to the pair-creation bath; its symmetric weight 1+2n_k>0 ⇒ δm = 2∫ρ/ω²>0. Run a Schwinger-rate spectral density through the `doorA_sign.py` kernel and confirm δm>0; the MOND sign appears ONLY if a ρ<0 band is inserted by hand. Falsifier-of-the-wall: a peer-reviewed acceleration-dependent vacuum response with a **negative-residue pole at ω<ω_orb and threshold exactly a₀** — none exists. |
| 13 | **Asymptotic-safety fixed-point exponents fix κ / a₀** (κ as an IR critical exponent of the Reuter FP) | κ=½ UNFORCEABLE — but via the **OPEN index/fixed-point-boundary route**, NOT the closed continuous/dynamical one | **NEW-DOOR** | The one in the batch not already closed. The κ-closure explicitly left the **fixed-point-boundary-condition** avenue open and out of scope; "a different κ-forcing than the ruled-out continuous" is correct and load-bearing. Two caveats (both ways): the naive **running-G → MOND** instantiation is DEAD (Donoghue 1911.02967: Euclidean RG-G ≠ real G(x); the one AS-MOND paper was withdrawn); and computability is unproven (critical exponents are scheme-dependent, numerical in truncations, no exponent shown = ½ or Z⁻¹=0.1727). | (1) Compute the critical-exponent spectrum {θᵢ} in EH + (curv)² truncation (Codello–Percacci–Rahmede tables); check any dimensionless θᵢ = κ=½ or Z⁻¹=√(3/32π)=**0.1727** to ~10% across truncations — none ⇒ door doesn't deliver the NUMBER. (2) Anti-circularity gate: keep κ symbolic; the FP boundary condition must force the normalization WITHOUT inputting Z by hand. (3) Decisive: run the linearized flow about the FP and read whether a₀ is RG-**relevant** (a prediction) or **irrelevant** (a free IR initial condition — then the FP says nothing). (4) Confirm you are NOT reproducing the withdrawn running-G construction. |
| 14 | A flavor/sector-specific Lorentz-violation (SME) term derives Koide / a fermion mass | SME bridge is FLAVOR-BLIND (equivalence principle) | **ADDRESSED** | The induced s_μν is **universal** — the s^TX boost dipole is the same for every species by the EP (gravity-sector s_bar). A flavor-dependent c_μν matter coefficient was the verified "15-order kill" MIS-MAP (universal-coupling differential cancellation). No flavor handle ⇒ cannot select r=√2 / a generation pattern. | Re-derive the induced coefficient: it is s_bar (gravity), trace-free, with NO O(1) un-β-suppressed anisotropic flavor channel (SO(3)-irrep + trajectory-independence). Confirm the matter-c_μν route cancels differentially (banked `S_TENSOR_SME_COMPONENT_LEDGER`). The bound it would have to beat (LLR/INPOP-Cassini) tests only universal projections. |
| 15 | Mannheim/Weyl conformal gravity hosts the framework / a₀ = conformal-symmetry-breaking VEV | MANNHEIM/WEYL ALREADY KILLED | **ADDRESSED** | Dead 3 ways: Hobson-Lasenby 2103.13451 ("conformal gravity does NOT predict flat rotation curves" — the flat-curve claim is an artifact); the γr linear term has the **WRONG SIGN** (repulsive where attraction is needed; fails cluster lensing); and the 4-derivative theory carries a massive spin-2 **ghost**. As an a₀-mechanism: deep-MOND scale invariance is broken **EXPLICITLY** (a₀ multiplies a non-invariant operator) ⇒ **no Goldstone**, a₀ cannot be a symmetry-breaking VEV (Milgrom 0810.4065). | No new test — closed. Re-verification seals: (a) sign of γ for SPARC outer curves vs cluster lensing conflict; (b) negative-residue spin-2 pole in the Weyl propagator; (c) a₀ multiplies a dimensionful (non-scale-invariant) coupling ⇒ no shift symmetry. |
| 16 | A scale-dependent / environment-dependent dark sector closes the **cluster** residual (clumpy in clusters, smooth in galaxies) | CLUSTER residual = shared-MOND gap **with the DENSITY-VETO** | **NEW-DOOR (partial, ranked #2)** | Genuinely the right target — the cluster gap is real and shared-MOND. A scale/density-selective clustering is exactly what would evade the AeST density-veto IF it can be galaxy-safe AND cluster-clumpy at once. The veto says one knob can't do both; a **two-regime k⁴-Jeans / environment-triggered condensation** is a distinct, un-closed mechanism (the existing `routeD_scale_selective_clustering.py` / `routeB_k4_jeans` probes are the seed, not a closure). Caveat: the framework's density-a₀ reading already lands Tian-2020's 17× to order with **zero params** and flattens the deficit to ±30% — so any new dark-sector cure must beat "understand-not-solve," not a blank slate. | (1) Demand the dark sector's Jeans/condensation scale λ_J(ρ) sit **above** galaxy scales (smooth, CDM-degenerate, no S8 cost) AND **below** cluster cores (clumpy) — solve λ_J(ρ_gal) vs λ_J(ρ_cluster) and check the window exists without a 3rd tuned parameter. (2) Hard veto test: does the same parameter that makes it cluster-clumpy spoil galaxy rotation curves (the AeST density-veto)? Run the BVP shooting in `CLUSTER_AEST_MASSTERM` with the environment trigger. (3) Cross-check vs the density-a₀ ±30% baseline — a real cure must do strictly better, not merely re-land the same order. |
| 17 | a₀ = the acceleration to change the dS horizon **area by one LQG/Planck-area quantum** | No named theory-wall — fails on its OWN NUMBERS (wrong magnitude) | **HITS-WALL** | New idea (LQG area-spectrum not previously banked), dies on arithmetic. N = A_H/ℓ_P² = **1.32×10¹²³** (= S_dS). Every "one-quantum" reading misses a₀ by 60–122 orders: cH_Λ/N = 4.1×10⁻¹³³ (**122 low**), cH_Λ/√N = 1.5×10⁻⁷¹ (**61 low**). The framework relates cH_Λ to a₀ by the **O(1) geometric Z=5.79** (Friedmann-3, Einstein-8π, free-fall-½), NOT by the entropy 10⁻¹²³. Wrong magnitude by construction. | Pure arithmetic, reproducible: N = 4π(c/H_Λ)²/(ħG/c³) = 1.3×10¹²³; test cH_Λ/N, cH_Λ/√N, cH_Λ·√(ℓ_P²/A_H) — none within 60 orders of a₀. To EVADE: derive Z=√(32π/3)=5.79 (an O(1)) from the area eigenvalue 8πγ√(j(j+1)) — but that sets the AREA unit, not a dimensionless O(1); no path to 5.79. Falsifier-of-the-idea: the required factor is the **inverse entropy 10⁻¹²³**, not an O(1). |
| 18 | E8 (or E6/SO(3,11) graviGUT) unifies gravity + SM and the framework's structure fixes the generations | E8 DISTLER-GARIBALDI no-go | **ADDRESSED** | Distler-Garibaldi (0905.2658, Thm 1.3, the 180>128 chirality-dimension kill, read verbatim) forbids 3 chiral generations + gravity in any real form of E8. The graviGUT is a **NATURAL-SETTING / anomaly-free HOME** for ONE chiral family (Coleman-Mandula + D-G **threaded/evaded** for one family by the non-compact coset) — but **evasion ≠ derivation**; the SM content is **FITTED**, the 3-generation structure is not produced. | Read off whether the proposal claims >1 chiral generation in a real E8 form (then D-G kills it) or only embeds one family (then it's a home, not a derivation). Check the coset is non-compact/antilinear (the only evasion route) and that NO observable beyond "anomaly-free home" is predicted (`PARTICLE_PHYSICS_FROM_DESITTER_GAUGE`). |
| 19 | Holographic anyon / FQHE-on-the-dS-screen: a₀ = the anyonic (fractional) excitation gap on the horizon | No named theory-wall — fails on magnitude + the cH₀-vs-cH_Λ footing fork + no derivation of the gap | **HITS-WALL** | New framing, weakest of the batch. Same magnitude problem as #17 (a "fractional quantum" on a 10¹²³-mode screen is 10⁻¹²³-ish off a₀), the fractional filling ν is a **free O(1)** with no principle fixing it to give Z, and it inherits the unresolved cH₀-vs-cH_Λ footing fork (ρ_total/cH₀ → 1.13×10⁻¹⁰ vs ρ_DE/cH_Λ → 9.36×10⁻¹¹) without deriving which. Re-labels ρ_DE, derives nothing. | Demand the anyon gap Δ produce a₀ = (something)·Δ with the "something" forced (not a fitted ν). It can't: ν is free and the gap on N=10¹²³ modes is the wrong scale. Confirm it doesn't smuggle the cH₀-footing (run both footings; the idea is non-diagnostic of either). No falsifiable handle beyond the already-tested a₀(z) branch. |
| 20 | **Frustrated domain-wall network (w=−2/3) sources dark energy** and sets a₀ / the a₀(z) branch | No theory-wall — but moot (re-labels ρ_DE) + the a₀(z) branch is already the live empirical test | **HITS-WALL (soft / non-diagnostic)** | A frustrated wall network has w=−2/3, so ρ_DE redshifts as (1+z)^{3(1+w)} = **(1+z)¹** (a gentle DECLINE into the past, NOT constant). It is a legitimate DE candidate, but for the framework it only **re-labels** the ρ_DE that a₀=c²√(Λ/32π) already uses — it does NOT derive Z (the O(1) is still Friedmann-3/Einstein-8π) and does NOT supply the MOND sign. Its one genuine consequence (a specific a₀(z) ∝ √ρ_DE(z) with w=−2/3) is **already the framework's live hostage front** and is currently non-diagnostic / ΛCDM-degenerate. | Compute a₀(z) for w=−2/3 vs the canonical w=−1: ρ ∝ (1+z) gives a **shallower** decline than √ρ_DE^{Λ}. Feed both into the existing a0(z) hostage pipeline (`a0z_unified_pipeline.py`) and the DESI w(z) branch; the DR3 gate (2026-27) + ELT (early-mid 2030s) discriminate w=−2/3 vs w=−1 vs the rival rising cH(z). Until then non-diagnostic — say so. |

---

## (2) THE SCHWINGER VERDICT (idea #12 — the standout), decisively

**dS-Schwinger pair-creation does NOT supply the active, MOND-signed, low-acceleration kernel. It is high-field
anti-MOND drag that re-routes straight into the passivity + wrong-regime wall.** All three legs fail, with the
sign and regime stated:

- **SIGN — anti-MOND (the wall).** The in-in symmetric (noise) weight of Bogoliubov pair-creation is
  **1 + 2|β|² = 1 + 2n_k ≥ 1 > 0**, forced by unitarity |α|²−|β|²=1. Positive symmetric weight ⇒ ρ(ω) ≥ 0 ⇒
  **δm = 2∫ρ/ω² dω > 0 ⇒ inertia RAISED ⇒ anti-MOND.** dS particle creation ADDS positive noise and **positive
  dissipation** (drag), the wrong sign — verified by the cosmological-dissipation primaries (gr-qc/9403054:
  dissipative + noise + positive entropy production; 2202.08218: FLRW condensate dissipation = decay/friction).
  This is the **same passive side** the bank pinned three independent ways.
- **REGIME — high-a, not low-a (backwards).** The Schwinger rate ∝ exp(−π a_crit/a) is an **above-threshold**
  effect: suppressed at low a, active at high a. **MOND modifies inertia BELOW a₀.** The regime is inverted, and
  the dS horizon does not flip it (the horizon makes the super-horizon IR band special, ~110–295× below the
  orbital band per DOOR A — not the high-a band).
- **SCALE — off by 36× on the wrong side.** The natural Unruh/Schwinger threshold for a horizon-scale quantum
  m_dS=ħH/c² is **a_crit = 2πc·H_Λ = 3.40×10⁻⁹ m/s² = 36.4 a₀** (verified), with a₀ = cH_Λ/5.79 sitting **209×
  BELOW** a_crit. a₀ is NOT the Schwinger threshold.

**Genuine credit (both ways):** the idea correctly identifies that an **ACTIVE source** is exactly what the MOND
kernel needs — the bank agrees (the active kernel requires a sustained inverted/gain reservoir: T_b<0 / J_eff<0 /
unsaturated tachyon). But dS-Schwinger is a **stable-Λ, NEC-respecting, cooling** source that produces
**positive-noise dissipation** — the passive side. A crack would require a band with **ρ(ω)<0 at ω_orb ≈ 2.4×10⁻¹⁶
rad/s** (population inversion / gain in-band); dS-Schwinger has none (its dissipation is positive and out-of-band).
**Re-routes into the wall, not a crack.**

---

## (3) RANK of the genuine new doors

**Only TWO ideas open something un-closed. Ranked:**

### #1 — Idea #13 (asymptotic-safety fixed-point exponents → κ): the one truly new theory door
- **Why it ranks first:** it targets the **lone explicitly-open avenue** the κ-closure flagged (fixed-point
  boundary condition / index — categorically different from the closed continuous/dynamical probes). If an exponent
  equals ½ or Z⁻¹=0.1727 it would FORCE the one free O(1) the framework cannot derive.
- **Concrete next step / framework test:** compute the EH+(curv)² critical-exponent spectrum {θᵢ} (Codello–Percacci–Rahmede),
  check across truncations for θ = ½ or **0.1727** at the ~10% level; **gate it anti-circularly** (κ symbolic, no
  Z input by hand — the same gate that sank holography); and decisively settle whether a₀ is RG-relevant
  (prediction) or RG-irrelevant (free IR datum, FP silent). **Honest prior:** speculative — exponents are
  scheme-dependent and none is shown to match; the naive running-G→MOND version is already DEAD (Donoghue), so
  this must be the **distinct exponent-as-κ** route. Likely returns "doesn't deliver the number" — a valid outcome
  that closes the last named κ-avenue for a new reason.

### #2 — Idea #16 (environment/scale-selective dark sector → cluster cure): the one new empirical door
- **Why it ranks second:** the cluster residual is a real, shared-MOND gap, and a two-regime
  condensation is the one mechanism that could thread the AeST **density-veto** (galaxy-safe AND cluster-clumpy).
- **Concrete next step / framework test:** solve the Jeans/condensation scale λ_J(ρ) and check a window exists with
  ρ_galaxy → smooth (CDM-degenerate, no S8 cost) and ρ_cluster → clumpy **without a third tuned parameter**; then
  run the density-veto hard test (does the cluster-clumpy knob spoil galaxy RCs? — BVP shooting in
  `CLUSTER_AEST_MASSTERM`). **Honest prior:** the framework's zero-param density-a₀ reading already lands Tian-2020's
  17× to order and flattens the deficit to ±30%, so a new cure must **beat understand-not-solve**, and the density-veto
  is a steep wall — partial at best.

---

## (4) BOTH-WAYS BOTTOM LINE

**Genuinely opens something (test it):**
- **#13 (asymptotic-safety exponents → κ)** — the lone un-closed theory door; test = the FP critical-exponent
  spectrum vs ½ / 0.1727 with the anti-circularity gate.
- **#16 (environment-selective dark sector → clusters)** — the one new empirical door; test = the λ_J(ρ) window vs
  the AeST density-veto, beating the ±30% density-a₀ baseline.

**Re-routes into a proven wall (decline, with the sign/number where it bites):**
- **#12 (dS-Schwinger)** — passivity/wrong-regime wall: **high-field anti-MOND drag** (1+2n_k>0 ⇒ δm>0; threshold
  36.4 a₀; high-a not low-a). The standout that does not crack.
- **#11 (Galileon-Vainshtein)** — COVARIANT-MI trichotomy (field=MG fails Cassini; wrong screening topology).
- **#17 (LQG area-quantum)** — wrong magnitude by **122 orders** (needs 10⁻¹²³, not the O(1) Z).
- **#19 (holographic anyon/FQHE)** — magnitude + free filling ν + cH₀-vs-cH_Λ footing fork; re-labels ρ_DE.
- **#20 (frustrated w=−2/3 domain walls)** — moot DE re-labeling; its one consequence (a₀(z)) IS the live hostage
  front, currently non-diagnostic.

**Already addressed / closed (no re-opening):**
- **#15 (Mannheim/Weyl)** — killed 3 ways (flat-curve artifact, wrong-sign γr, spin-2 ghost) + explicit-not-spontaneous
  breaking ⇒ no Goldstone, a₀≠VEV.
- **#18 (E8 unification)** — Distler-Garibaldi no-go (180>128); a home, not a derivation; content fitted.
- **#14 (flavor-specific SME term)** — the bridge is flavor-blind by the equivalence principle (gravity-sector
  s_bar); no handle on Koide / generations.

**Net:** of #11–20, **2 genuine new doors (#13, #16)**, **5 re-routes into proven walls (#11, #12, #17, #19, #20)**,
**3 already-closed (#14, #15, #18)**. The standout (#12 dS-Schwinger) is **anti-MOND drag, not a crack**.
Quarantine held; nothing flips on the empirical fronts (s^TX, a₀(z)). No manufactured win, no high-priesting.

**Numbers reproduced (verified firsthand):**
`Z=√(32π/3)=5.7888`, `cH_Λ=Zₐ₀=5.418×10⁻¹⁰`, `a_crit=2πcH_Λ=3.404×10⁻⁹=36.4 a₀`;
`N=A_H/ℓ_P²=4π(c/H_Λ)²/(ħG/c³)=1.324×10¹²³`, `cH_Λ/N=4.1×10⁻¹³³ (−122 orders)`, `cH_Λ/√N=1.5×10⁻⁷¹ (−61 orders)`;
`Z⁻¹=√(3/32π)=0.17275`; `w=−2/3 ⇒ ρ_DE∝(1+z)¹`.
**Builds on:** `reviews/NONEQUILIBRIUM_PASSIVITY_ESCAPE_2026-06-15.md`,
`reviews/DOORA_REAL_NONEQUILIBRIUM_KERNEL_VERDICT_2026-06-26.md`, `reviews/KAPPA_FORCING_DOOR_CLOSED_2026-06-17.md`,
`reviews/PARTICLE_PHYSICS_FROM_DESITTER_GAUGE_2026-06-15.md`, `real_research/ACTIVE_KERNEL_SIGNTHEOREM_2026-06.md`,
`real_research/COVARIANT_MI_COMPLETION_2026-06.md`.
