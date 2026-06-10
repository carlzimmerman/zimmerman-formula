# The laboratory bridge: F4 and the kernel vs already-published experiments — one prescription laboratory-KILLED, one door genuinely open, the rest immune by 10¹²⁺

*agentG, 2026-06-10. Task: the honest laboratory/particle-physics confrontation of the kernel a₀ = c²√(Λ/32π) =
9.36×10⁻¹¹ m/s² and the F4 shape μ_std(x) = x/√(1+x²), x = |a_total|/s, s ∈ {9.36×10⁻¹¹ framework, 5.42×10⁻¹⁰
hostile = cH_Λ}, against real published data. Artifacts: `agentG_lab_bridge.py` + `.out` (all numbers below are from
the run; the P-D torsion-oscillator ODE is integrated exactly and VALIDATED against Gundlach's own Fig. 1 simulation:
537 s predicted vs ~530 s in their figure). The banked boundary is respected: coincidence bridges (meV ~ Λ^{1/4} ~ m_ν,
GUT ladders) were audited NOT FORCED (`FORCING_ROUTES_REWORKED.md`, `CKN_LAMBDA_VALUE_VERDICT_2026-06-06.md`) — cited,
not re-litigated. Both normalizations, both ways, throughout.*

## 0. The prescription map (without it, "what does F4 predict in the lab?" is ill-posed)
F4 is a worldline rule, m·μ(|a|/s)·a = F. Everything below hangs on what "|a|" means for a real apparatus — the same
prescription dependence Door IVa exposed (instantaneous vs orbit-averaged = 100% of the eccentricity signal). The lab
fork is a *different axis* of the same space:

| | reading | lab background | status in repo |
|---|---|---|---|
| **P-A** | instantaneous total **kinematic** \|a\| in the local quasi-inertial frame (gravity = force) | suspended body: Earth rotation 2.28×10⁻² m/s² (dominant) ⊕ solar orbit 5.9×10⁻³ ⊕ galactic 2.2×10⁻¹⁰; free-faller: 9.8 | **the banked reading** (SPARC, Saturn, WB-EFE, eccentric orbits all use it) |
| **P-B** | instantaneous total **proper** \|a\| (accelerometer reading) | suspended body: 9.8; **free-faller: ~0 → deep MOND in the lab** | the bath/UDW-**mechanism-natural** reading (Deser–Levin κ = √(a_proper²+H²)); but P-B *alone cannot be the galactic law* — orbiting stars are free-falling (x_proper = 0 → no MOND), so the banked phenomenology is P-A-class. Flagged at full weight. |
| **P-C** | linearized response **kernel about the background trajectory** | the Door-I λ² structure: every finite-order coefficient is A(κ)+a²B(κ), κ = *background* total — a small superposed oscillation responds **linearly**, inheriting μ(x_bg), never μ(x_osc) | the only mechanism-grade kernel computed in this repo (`agentB_door1_*`) |
| **P-D** | **mode/axis-amplitude** reading: μ evaluated on the small oscillatory acceleration itself | the only reading whose lab prediction scales with the *signal's* smallness | never used by the repo; it is, verbatim, Gundlach's Eq. (2) |

Milgrom's own nonlocal-MI argument (Ann. Phys. 229, 384 (1994), astro-ph/9303012; pedagogical review
astro-ph/0112069) adds the **center-of-mass anchor**: for a composite body the CoM acceleration is the relevant
argument, not element accelerations — a torsion pendulum's CoM is on-axis and static, so canonical nonlocal MI
predicts Newtonian twist dynamics *by construction*. P-D is also internally sick (a suspended mass has a_z = 0
per-axis → zero vertical inertia for any perturbation — everyday physics already refutes it); Gundlach makes the
kill *quantitative*.

## 1. Gundlach et al. (torsion balance) — the amplitude prescription is LABORATORY-DEAD; everything banked is immune
**Pinned:** Gundlach, Schlamminger, Spitzer, Choi, Woodahl, Coy, Fischbach, *Laboratory Test of Newton's Second Law
for Small Accelerations*, **PRL 98, 150801 (2007)** (read in full). Torsion pendulum: κ = 2.36×10⁻⁹ N·m/rad, τ₀ =
795 s, r_e = 0.023 m, amplitudes 13 nrad–19 μrad ⇒ accelerations 1.9×10⁻¹⁴ – 2.7×10⁻¹¹ m/s². **F ∝ a confirmed down
to 5×10⁻¹⁴ m/s²**; Fig.-2 residual envelope ±2×10⁻¹⁴ m/s² (0.07–0.2% over the top decade, O(40%) at the floor); their
MOND-simulation recovery spans a₀ = 10⁻¹⁶–10⁻⁹. Predecessor: Abramovici & Vager, PRD 34, 3240 (1986), F = ma down to
3×10⁻¹¹ m/s². Gundlach et al. say it themselves, both ways: the result "does not invalidate MOND directly, since MOND
requires that the measurement must be carried out in the absence of any other larger accelerations," but it
"constrain[s] any theoretical formalism seeking to derive MOND from fundamental principles… by requiring that
formalism to reproduce F = ma under laboratory conditions."

**F4 predictions (computed):**
- **P-A** (banked): x_bg = 2.4×10⁸ (fw) / 4.2×10⁷ (hostile) → deviation 1/(2x²) = **8.4×10⁻¹⁸ / 2.8×10⁻¹⁶** vs the
  0.2% demonstrated bound → **safe by 2×10¹⁴ / 7×10¹²**.
- **P-B** (proper, 9.8): deviation **4.6×10⁻²³ / 1.5×10⁻²¹** → safe by 10¹⁸⁺.
- **P-C** (kernel): a linear kernel about the background cannot see the oscillation amplitude at all; additionally the
  bath memory time at a = 9.8 is τ_c = 2πc/a = 1.9×10⁸ s, so the 795-s pendulum sits at ωτ_c ≈ 1.5×10⁶ — deep-UV for
  the kernel, which returns the *bare* inertia. Safer than the static estimate. **The instantaneous-vs-orbit-averaged
  fork of Door IVa is lab-degenerate** (the background |a| is constant to ~10⁻¹² fractionally): Gundlach cannot decide
  IVa; it decides the amplitude-vs-background axis instead —
- **P-D** (amplitude; their own Eq. 2, our exact ODE): at the 5×10⁻¹⁴ floor, Y = a_N/s = 5.3×10⁻⁴ (fw) / 9.2×10⁻⁵
  (hostile) → predicted acceleration excess **ν = ×43 (fw) / ×104 (hostile)**, period collapse 795 s → **115 s / 74 s**
  — against a measured proportionality good to ~40% there and 0.2% in the mid-decade. Effect-size kill **×10² – ×3×10³**;
  in kernel-scale terms the data cap s ≲ 6.3×10⁻¹³–8.4×10⁻¹⁴, i.e. **the framework normalization is excluded ×148–×1116
  and the hostile one ×855–×6464 under P-D**. *That is a real laboratory kill of the amplitude prescription at two-to-
  three orders of magnitude, at both normalizations.* It retro-kills nothing banked (the repo never used P-D), but it
  adds a wall to the spec sheet: **any future F4 mechanism whose linearized lab response is amplitude-keyed (AC-coupled
  /static-projecting kernels) is pre-killed by Gundlach** — the Door-I λ² census (background-κ coefficients) passes this
  wall automatically; that is now a *required* feature, not a convenience.
- **The one P-A lab loophole, named and bounded:** kinematic cancellation of rotation⊕orbit⊕galactic terms (Ignatiev,
  PRL 98, 101101 (2007), gr-qc/0612159; PRD 77, 102001 (2008)) — windows of 2s/(ω_E a_rot) ≈ **0.11 ms (fw) / 0.65 ms
  (hostile)**, twice a year, at ~80° latitude spots. Never attempted; P-A is lab-untested, not lab-untestable.

**Hostility inversion, recorded:** in the lab the *hostile* (larger) normalization is the MORE exposed one everywhere
below — deeper x at fixed signal. Same pattern as the lensing battery (worst exposure hardens).

## 2. Atom interferometry — existing data are SILENT under every reading; the protocol door is genuinely open
**Pinned instruments:** Kasevich & Chu, PRL 67, 181 (1991) (first light-pulse AI); Peters, Chung & Chu, Nature 400,
849 (1999): absolute gravimetry **Δg/g ≈ 3×10⁻⁹** (2×10⁻⁸ per 1.3-s shot, 1×10⁻¹⁰ after 2 days); Asenbaum, Overstreet,
Kim, Curti, Kasevich, PRL 125, 191101 (2020), arXiv:2005.11624: dual-species ⁸⁵Rb/⁸⁷Rb, 2 s free fall in the 10-m
tower, **η = [1.6 ± 1.8(stat) ± 3.4(syst)]×10⁻¹²** → demonstrated differential-acceleration accuracy **1.8×10⁻¹¹
(stat) / 3.8×10⁻¹¹ (total) m/s²** — *below the kernel scale a₀ = 9.4×10⁻¹¹*. That is the load-bearing fact.

**What existing AI data imply (computed):**
- **P-A:** the falling atom has x = g/s ≈ 10¹¹ → δg/g = 4.6×10⁻²³ (fw) / 1.5×10⁻²¹ (hostile) → margin vs 3×10⁻⁹:
  **7×10¹³ / 2×10¹²**. Untestable.
- **P-B:** between pulses the atom is **force-free** — the worldline law reads 0 = 0 and the trajectory is the
  geodesic; photon kicks occur at ~10³ m/s² (x ≫ 1, Newtonian recoil); the mirror/laser reference is suspended
  (x ≫ 1, Newtonian). **F4-P-B predicts exactly the standard k_eff g T² phase.** A deep-x atom with *no applied force*
  produces no observable. EP-type AI comparisons (Asenbaum) are also blind: μ is composition-independent → η_F4 = 0.
- Residual systematics in published gravimeters (e.g. ~10⁻⁹-g-class magnetic-gradient forces) are too small for their
  F4-enhanced response to breach the 7×10⁻⁹-g comparison floors — existing budgets do not accidentally test F4.
- **Verdict: NO reading of F4 is tested by any published atom-interferometer dataset.** Honest both ways: AI data
  neither constrain nor support.

**THE DOOR (the bridge-to-quantum-experiments claim, stated precisely):** put the atom where only F4-P-B physics can
act — free fall (proper x ≈ 0) — and apply a **calibrated sub-a₀ force** (magnetic gradient on a field-sensitive
state, dual-state differential to common-mode-reject gravity). Observable: extra differential phase
Δφ = k_eff·(a − F/m)·T², with a = ν(y)·F/m, y = (F/m)/s, ν the exact μ_std inversion. Computed at A20-class
parameters (k_eff = 1.61×10⁷ m⁻¹, T = 0.955 s):

| normalization | optimal y | max Δa [m/s²] | Δφ [rad] | vs A20 accuracy (stat/total) |
|---|---|---|---|---|
| framework 9.36×10⁻¹¹ | 0.49 | **2.8×10⁻¹¹** | 4.1×10⁻⁴ | **1.6σ / 0.7σ** per campaign |
| hostile 5.42×10⁻¹⁰ | 0.49 | **1.6×10⁻¹⁰** | 2.4×10⁻³ | **9.2σ / 4.3σ** per campaign |

The deep-MOND signature is **shape, not scale**: a(F) ∝ √F below s (response enhancement ×3.2 at y = 0.1) — a
square-root response curve over a 2-decade F-scan is self-calibrating and does not require absolute force calibration
at the effect level. So: **the hostile normalization of P-B is testable at ~4–9σ with the existing instrument class;
the framework normalization needs ×3–5 (longer T — the tower already runs 2T ≈ 1.9 s — LMT, or integration).** Honest
weight: this door tests the *mechanism-natural* reading, which (i) cannot itself be the galactic law (free-fall
inconsistency above) and (ii) already lost its λ² bath mechanism (Door I). A null walls in the bath corner further; a
detection would out-rank everything else in this program. Caveats flagged: the worldline rule has no unique quantum
extension (the phase carries an O(1) action-prescription uncertainty on top of the trajectory term; quantum-stationary
systems like bouncing-neutron qBOUNCE states make μ(|a|) ill-posed altogether — AI's semiclassical trajectories are
exactly why it is the right instrument), and clean 10⁻¹¹-m/s² force application is a real systematics program.

## 3. MICROSCOPE — pass but BLIND on η; the only macroscopic system straddling x = 1, in an unpublished channel
**Pinned:** Touboul et al., *MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle*, **PRL 129,
121102 (2022)**, arXiv:2209.15487 (companion 2209.15488; instrument 2102.11087): **η(Ti,Pt) = [−1.5 ± 2.3(stat) ±
1.5(syst)]×10⁻¹⁵**; 710 km orbit → g = 7.95 m/s², differential-acceleration scale η·g ≈ 2.2×10⁻¹⁴ m/s².

- **The EP channel (the published 10⁻¹⁵): F4 predicts η = 0 exactly, under every prescription and both
  normalizations** — μ multiplies the inertia of both collocated masses identically (same trajectory, same x,
  composition-blind). Measured −1.5 ± 2.7×10⁻¹⁵: consistent at 0.5σ. **PASS, but zero bits**: universal modified
  inertia is structurally invisible to Eötvös ratios. The celebrated bound neither constrains nor supports F4. (The
  task's premise "does F4 predict an EP-violation-like signal?" — answer: **no**, and that is a theorem-grade feature
  of universal MI, not an escape; second-order leakage from slightly different per-mass offsets → Δμ sits at gradient
  frequencies (DC/2f_EP), frequency-separated from f_EP; not computed, flagged.)
- **P-A** (banked): x = g/s = 8.5×10¹⁰ / 1.5×10¹⁰ → common-mode deviation 6.9×10⁻²³ / 2.3×10⁻²¹. No channel exists at
  that level. Safe/untestable.
- **P-B** (proper): the masses' proper acceleration is the *applied electrostatic* acceleration — and it straddles the
  kernel scale (computed; offsets are tens-of-μm class per the in-flight characterization, gradient 2GM/r³ =
  2.25×10⁻⁶ s⁻²): gradient at 10–100 μm offset → a = 2.2×10⁻¹¹–2.2×10⁻¹⁰ m/s² → **x_fw = 0.24–2.4 (μ = 0.23–0.92),
  x_hostile = 0.04–0.41 (μ = 0.04–0.38)**; drag-free in-band residual class 10⁻¹² → x ≪ 1; V3-spin centrifugal at
  20 μm ≈ 6.8×10⁻⁹ → x ≫ 1; calibration stimuli ~10⁻⁷ class → x ≫ 1. **MICROSCOPE is the only flown macroscopic
  precision system whose test masses sit at and below x = 1 in proper acceleration.** But the F4-P-B observable is a
  **common-mode force↔acceleration scale factor 1/μ(x)** — degenerate with electrostatic gain calibration (performed
  at x ≫ 1) and with offset estimation. The published η is blind to it; the predicted few-% (fw) to ×2–×12 (hostile,
  deep rows) response anomalies live in the instrument-consistency/calibration channel, which would take a **dedicated
  reanalysis** (session-level force-model closure across acceleration amplitudes) to convert into a bound. Both ways:
  plausibly *killing* for P-B-hostile if the closure is at the few-% level; **no published bound exists today** and we
  do not manufacture one.

## 4. CKN / g-2 — one paragraph, the banked verdict, no re-litigation
The F4 shape itself is dead-silent in storage rings: a muon at BNL/FNAL has proper acceleration γ²v²/ρ ≈ 1.1×10¹⁹ m/s²
→ x ≈ 10²⁸–10²⁹ → inertia correction **~10⁻⁵⁹–10⁻⁵⁷** vs ~10⁻¹⁰ experimental precision: nothing, ever. The only
Λ→laboratory bridge on offer is the CKN-EFT one (Cohen–Kaplan–Nelson, PRL 82, 4971 (1999), hep-th/9803132), and the
banked audit already fixed its status: the framework's CKN content is the **saturated bound with a free O(1)**
(`CKN_LAMBDA_VALUE_VERDICT_2026-06-06.md` — saturation, L = c/H, and the dropped additive constant are all assumed;
the seesaw is an algebraic identity carrying zero new information), and **no forcing route exists** for the
coefficient or for any meV/Λ^{1/4} particle bridge (`FORCING_ROUTES_REWORKED.md`, four worked negatives + the
structural symmetry-breaking-scale argument). The g-2 literature confirms the generic channel is empty with existing
data: Blinov & Draper (PRD 104, 076024 (2021), arXiv:2107.03530; cf. Banks & Draper, PRD 101, 126010 (2020),
arXiv:1911.05778) find lepton g-2/Lamb-shift sensitivity reaches L_eff(m_e) ≳ 10 nm against the gravitationally
motivated ~10⁵ km — **~16 orders of magnitude short**: "far from being sensitive to the depletions motivated by
quantum gravity." Verdict: **the kernel's Λ connection makes NO forced laboratory prediction in the g-2/CKN channel —
the banked free-coefficient situation, unchanged.** No numerology was attempted; none is licensed.

## THE TABLE
| experiment | published bound (pinned) | F4 prediction (per prescription × normalization) | margin | verdict |
|---|---|---|---|---|
| **Gundlach 2007** torsion balance, PRL 98, 150801 | F ∝ a down to 5×10⁻¹⁴ m/s²; ±2×10⁻¹⁴ residuals (0.2% mid-decade) | P-A: 8.4×10⁻¹⁸ (fw) / 2.8×10⁻¹⁶ (h); P-B: 4.6×10⁻²³ / 1.5×10⁻²¹; P-C: smaller still (UV of bath kernel, ωτ_c ~ 10⁶); **P-D: ×43 / ×104 acceleration excess, period 795→115/74 s** | P-A/B/C safe ×10¹²⁻¹⁹; **P-D excluded ×148–1116 (fw), ×855–6464 (h) in s** | **P-D laboratory-KILLED, both normalizations**; banked readings immune |
| Abramovici–Vager 1986, PRD 34, 3240 | F = ma down to 3×10⁻¹¹ m/s² | same structure, weaker | subsumed ×~10³ by Gundlach | corroborates the P-D kill |
| **Atom gravimeters** (Peters–Chung–Chu, Nature 400, 849) | Δg/g ≈ 3×10⁻⁹ absolute | P-A: δg/g = 4.6×10⁻²³ / 1.5×10⁻²¹; P-B: **exactly zero** (force-free geodesic); P-D: zero (signal is the 9.8) | ≥2×10¹² | **silent — no reading tested** |
| **AI applied-force protocol** (A20 instrument class, PRL 125, 191101) | demonstrated δ(Δa) = 1.8–3.8×10⁻¹¹ m/s² | P-B: Δa_max = s·max y(ν−1) = **2.8×10⁻¹¹ (fw) / 1.6×10⁻¹⁰ (h)**, √F response shape | fw: 0.7–1.6σ; **hostile: 4.3–9.2σ** per campaign | **THE OPEN DOOR** (designed experiment; no published data yet) |
| **MICROSCOPE final**, PRL 129, 121102 | η = [−1.5 ± 2.3 ± 1.5]×10⁻¹⁵ | η_F4 = **0 exactly** (all readings, both s) | consistent 0.5σ; zero discriminating power | **PASS but BLIND** (universal MI invisible to Eötvös ratios) |
| MICROSCOPE scale-factor channel (unpublished) | force-model closure, not a published bound | P-B: masses at x = 0.04–2.4 → response anomalies few-% (fw) to ×2–12 (h) | n/a — reanalysis-grade | the one *existing dataset* that could test P-B; flagged, not claimed |
| **Muon g-2** (BNL/FNAL) + CKN | a_μ to ~10⁻¹⁰; CKN-EFT: lab L_eff ≳ 10 nm vs needed 10⁵ km (BD21) | F4: 10⁻⁵⁹–10⁻⁵⁷; kernel→g-2: **no forced prediction** (free O(1), banked) | F4: ~10⁴⁸ below sensitivity; CKN channel ~10¹⁶ short | **empty by audit** — boundary respected |

## HEADLINE — which laboratory door is open with existing data
1. **A real kill, at full weight:** the **amplitude/per-axis prescription (P-D) of modified inertia is
   laboratory-dead** — Gundlach 2007 excludes it by **two to three orders of magnitude in the kernel scale at both
   normalizations** (×148–×1116 framework, ×855–×6464 hostile), with the predicted period collapse (795 → 115/74 s)
   integrator-verified against the paper's own simulation. This was never the banked reading, so F4-as-banked loses
   nothing — but the spec sheet gains the **Gundlach wall**: any future mechanism must deliver *background-anchored*
   (P-A/P-C-type) linear response in the lab. The Door-I λ² kernel structure passes it automatically; amplitude-keyed
   kernels need not apply.
2. **No open door on the banked prescription (P-A/P-C):** every published lab test — torsion balances, atom
   gravimeters, MICROSCOPE — sits 10¹²–10¹⁹ above F4's predicted deviations, because every lab background trajectory
   has x ≫ 1 under those readings. The only in-principle P-A window is Ignatiev's ~0.1–0.7 ms kinematic-cancellation
   spots (80° latitude, equinoxes) — named, never attempted, not oversold. **The lab cannot presently kill or confirm
   F4-as-banked; its fate stays with Saturn/IVb, the lensing wall, and the DR4 fork.**
3. **One genuinely open door, with existing instruments and no existing data: atom interferometry at sub-a₀ proper
   acceleration (P-B).** Free-falling atoms are the first laboratory objects at x ≈ 0; the Asenbaum-class
   differential accuracy (1.8–3.8×10⁻¹¹ m/s²) is *already below a₀*. A calibrated sub-a₀ applied-force protocol with a
   √F-shaped response signature tests the **hostile normalization at 4–9σ now** and the framework normalization at
   ~1.6σ/campaign (×3–5 from decisive). Precision: this tests the *mechanism-natural proper-acceleration reading*,
   which cannot itself be the galactic law and whose λ² bath mechanism Door I already refuted — a null adds a lab wall
   to an already-walled corner; a detection would be the discovery of the decade. That asymmetry is stated, not hidden.
4. **MICROSCOPE's 10⁻¹⁵ is a non-event for F4 in both directions** — universal modified inertia predicts η = 0
   structurally; the real (hostile-normalization-sensitive) content sits in the unpublished common-mode
   calibration-closure channel, reanalysis-grade only.
5. **Particle physics stays empty by audit, not by assertion:** F4 at storage-ring accelerations is ~10⁻⁵⁸; the
   CKN/g-2 channel is ~16 orders short of gravitational motivation (Blinov–Draper) and the framework's free-O(1)
   status there is banked. No numerology entered.

## Honest scope (locked)
- The P-D kill is a kill of a *prescription corner*, not of F4-as-banked; conversely nothing in the lab record
  *supports* F4 — the honest summary is "immune, not endorsed."
- P-B's free-fall-inconsistency with galactic phenomenology is itself an argument that the AI door tests the
  mechanism corner, not the law; if Door II's hybrid (trajectory-nonlocal MI + metric partner) is the real object,
  its lab limit may differ from both P-A and P-B — the protocol's value is that it measures *whatever* the matter
  sector does at x < 1.
- MICROSCOPE offsets/spin rates are instrument-paper-class pins (tens-of-μm offsets, mHz-class spin); the P-B
  x-bracket [0.04, 2.4] is robust to factor-few changes in those inputs (checked across the 10–100 μm bracket).
- Gundlach precision inputs are read from the published Letter (residual envelope, amplitude range); the s_kill
  bracket spans the ultra-conservative (40% at floor) to nominal (0.2% mid-decade) readings — the kill survives the
  spread by ≥×148 at its weakest.
- No claim of priority for the AI protocol idea is made (lab-MOND proposals exist: Ignatiev 2007/2008, the Gundlach
  paper's own program); what is new here is only the F4-specific, normalization-resolved forecast against the
  demonstrated A20 sensitivity.

*Artifacts: `agentG_lab_bridge.py` (constants, all four prescriptions × both normalizations, exact ν-inversion,
RK4 P-D oscillator with Fig.-1 validation, protocol forecast, MICROSCOPE x-table, μ-ring/CKN numbers) +
`agentG_lab_bridge.out` (the run). Companions: `TOE_STATUS_AND_DOORS.md` (swarm section), `MI_COUPLING_FAMILY.md`,
`agentB_door1_mechanism_notes.md` (P-C structure), `FORCING_ROUTES_REWORKED.md` + `CKN_LAMBDA_VALUE_VERDICT_2026-06-06.md`
(the banked no-numerology boundary).*
