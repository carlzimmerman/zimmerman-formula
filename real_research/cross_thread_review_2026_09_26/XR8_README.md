# XR8 — What is the fluid? (2026-09-26)

The author's direction: *"we need to find out what the 'Fluid' is.. which is not particles"*. The framework needs a dark
**mass** (the CMB and clusters require it) that is not a new particle species. XR8 asks what that mass can be as a
continuum, and whether it can be a state of the framework's own fields while the khronon stays a global time function
(criterion B).

Everything here is read-only on the rest of the repository. Every number comes from a script in this folder with
controls and a MUTATE run that must fail. κ = ½ and both a₀ footings play no role: the carrier is kernel-invisible
(A3), so the shell-crossing test is Newtonian self-gravity only. **No a₀ and no κ enters any number below, and both
footings give identical results.**

## The answer, in brief

- **No single-velocity fluid passes shell crossing, whatever its equation of state or dispersion order.** L374's
  ghost-condensate dust and every completion tried here fail on L374's own test and rule: the cubic P‴ (γ = 3) index,
  the X-dependent k⁴ coefficient, a k⁶ term added or replacing k⁴, and the Madelung (polar) form of the wave field.
  Each either leaves its own domain (ρ < 0, below the minimum, then runs away), becomes singular at a node, or replaces
  crossing by pressure. The leading Galileon-type cubic, (∇²π)(∇π)², is a total derivative in one dimension, so this
  1-D test cannot see it.
- **What passes is a field that multistreams by interference:** a complex order parameter Φ = √n e^{iθ} in its full
  (Cartesian) form, with a *light* radial mode — in practice a nearly free complex field. Its incoherent (mixed) state
  carries velocity dispersion. The collisionless phase-space continuum f(x, v) passes too, as the reference: it is
  the collisionless equation itself.
- **The passing field's phase cannot be the khronon.** Where streams cross the field has nodes, and its phase winds by
  ±2π around each one. In every tracking run the first node comes at 1.03–1.09 t_sc, and there are hundreds to ~10⁵
  node events per run. A phase with space-time windings is not a single-valued time function. θ must belong to a
  different field, locked to the khronon's rate at most in the background, as DF1 proposes.
- **This is new field content.** It is a complex scalar, one canonical pair in its non-relativistic limit and two real
  fields relativistically, that V0 does not contain: its added fields are leafwise auxiliaries (CV2), and its one
  propagating scalar is the khronon (FL1 F1, uncommitted). "Not particles" can honestly mean only this: a classical
  coherent field at occupation ~10⁷⁶–10⁸⁸ per de Broglie cell at L383's floor, m ≳ 1.9–5.2 × 10⁻¹⁹ eV
  with the framework's clearing. Its quanta, if quantised, would be bosons of mass m. The dark mass is its conserved
  U(1) charge, and the amount is initial data, not derived.

## Part A — the inverse specification

Each row's snippet is checked at its path by [`XR8_spec_table.py`](XR8_spec_table.py) (14/14; MUTATE, one tampered
number, fails A4, rc = 1). Every cited file is committed; CV3 and CV4 were committed by their owner (`ab6f31b61`) while
XR8 ran. Only DF1's FL1 (`real_research/dark_fluid_2026/`), cited in Part C, was still uncommitted.

| # | Requirement | What it forces on the fluid | Source (path:line) |
|---|---|---|---|
| A1 | Background and CMB: w = 0, cold | Linear cosmology sees only the GDM triple (w, c_s², c_vis²) plus an amount: a cold a⁻³ **fluid**, not a particle. A khronon Q-mode carrying both MOND and the dust has the w₀ squeeze: CMB w₀ ≤ 2.0e-14 against galaxy-MOND ≥ 1.4e-8, 5.85 orders. | `real_research/reviews/mi_particle_vs_mode_2026.py`:15, 103–105 |
| A2 | Lyman-α forest, z = 2–3 | Cold at z = 3: c_s(z=3) < 5 km/s (the pincer's check threshold) and ≤ 9.5 km/s (L185 via L289). A wave field needs m ≳ 2e-21 eV (Iršič) or 2e-20 eV (Rogers & Peiris). | `qwen_claude_field_theory/closure_2026/condensate_pincer_2026/condensate_mu_pincer_2026.out`:110; `…/dark_solid_first_gates_2026.out`:17; `real_research/clock_2026/L289_carrier_requirements.out`:23; `real_research/condensate_dust_2026/README.md`:70 |
| A3 | Kernel-invisible | Reciprocity: a component the kernel cannot see feels **Newtonian gravity only**, both its self-gravity and its response to baryons. In V0 the dark component feels u. | `real_research/g03_audit_2026/L353_kernel_invisible_dark_component.out`:44; `real_research/chk_v0_2026/CV1_nr_assembly.out`:34 |
| A4 | Collisionless in mergers, no pressure support | A supported medium lags ≥ 11× the Bullet offset. Harvey's β = −0.04 ± 0.07, bound +0.10. | `…/condensate_pincer_2026/merger_gate_supported_media_2026.out`:17; `real_research/merger_infall_2026/README.md`:29, 152 |
| A5 | Passes through shell crossing | The minimal condensate breaks at the first crossing. A wave field passes above a boson-mass floor of 1.9–5.2e-19 eV with clearing, 4.9e-19–1.25e-18 without. | `real_research/condensate_dust_2026/README.md`:50, 114, 116 |
| A6 | Cleared from galaxy halos by z ≈ 2–2.5, about half retained in clusters | X-COP two-sided gate 0.286 ≤ ε ≤ 0.835 (canonical) / 0.220–0.768 (alt). L388 pooled ε = 0.37–0.61. Clearing ≤ 0.30. | `real_research/dark_sector_2026/README.md`:82, 181; `…/L388_linear_gate_pooled.out`:46 |
| A7 | Small-scale power suppressed by z ≈ 0.5 (cosmic shear) | MOND regions capped near 1.75 Mpc with L388's retention: R = 1.05/1.12 against 1.2. Uncapped, 2.47–4.32. | `real_research/mond_sector_gate_2026/README.md`:33, 40, 60 |
| A8 | S8 / KiDS | σ₈ ratio ≥ 0.922. | `real_research/dark_sector_2026/L365_virialization_triggered_carrier.out`:24 |
| A9 | Criterion B: not the khronon's own dust | Stream crossing of the clock's own flow is a caustic of the foliation. The khronon's leaves are CMC in bound regions, with \|K/3H − 1\| ≤ 4.8e-3. | `XR3_obligations.md`:183; `real_research/chk_v0_2026/CV4_khronon_K_profile.out`:19, 43 |
| A10 | V0's multiplier rule (CV3) | A varied quantity reads only constrained fields. The fluid must live in a constrained field or a **new dynamical field**, never a multiplier. | `real_research/chk_v0_2026/README.md`:174 |
| A11 | The MOND-sector switch is carrier-blind (MS1) | The fluid must not enter what the switch reads. | `real_research/mond_sector_gate_2026/README.md`:28 |
| A12 | No new particle species; the mass is required | — | `XR3_obligations.md`:22–23 |

Two notes. The "c_s(z=3) ≲ 5 km/s" figure is a check threshold in the pincer and the dark-solid gates; the record's
stated forest requirement is ≤ 9.5 km/s (L185/L289). "30–60% retained" is the committed 0.37–0.61 (L388) inside a
0.286–0.768 gate.

## Part B — which non-particle continua pass through shell crossing

**The test is L374's, unchanged.** A cold converging flow v₀ sin(2πx/L) is run free-streaming and self-gravitating,
coarse-grained on L/50, and scored by the misplaced mass M against an exact collisionless sheet answer. The pass rule
is L374's (lines 41–44):

- M ≤ max(0.05, 2 × SP's M) at every post-crossing checkpoint in **both** tests;
- min ρ ≥ −0.01 ρ̄;
- energy conserved to 1%;
- no breakdown.

L374's pure functions (Grid, v_init, S_init, condensate, schrodinger) are imported, never its main. The two
re-implementations are checked against the imports:

- XR8's generalised fluid solver reproduces L374's `condensate()` exactly (C0: identical times, densities to 4e-16).
- XR8's wave solver reproduces `schrodinger()` exactly (M between them 0).

At nx = 4096, L374's committed first-negative times are reproduced to 1e-13 and its breakdown times to ≤ 8.4e-4. Its
21.5% at W = 0.1 is reproduced to four digits (C1). The completions run at nx = 2048.

| Candidate | Multistreams? | At the caustic | Afterwards | Verdict |
|---|---|---|---|---|
| (i) L374 condensate: γ = 2, k⁴ from (□φ)² | no | goes below its minimum at 0.81–1.05 t_sc (c_s² < 0) and breaks down at 0.98–1.37 t_sc (L374, reproduced) | W = 0.1 survives free streaming as a fluid, 21.5% misplaced | **fails** (control reproduced) |
| (ii-a) spatial cubic (∇²π)(∇π)² | — | Euler–Lagrange ≡ 0 in 1-D; in 2-D it is −4(π_xx π_yy − π_xy²) | — | **not testable in 1-D** |
| (ii-b) cubic P‴: γ = 3 (P ∝ X^{3/2} index), same k⁴ | no | below the minimum at 0.79–1.04 t_sc; breaks at 0.80–1.07 t_sc, earlier than γ = 2 (its k⁴ coefficient ∝ ρ flips sign below the minimum) | — | **fails** |
| (ii-c) α(X): δ(∇²π)² | no | ill-posed where \|b ∂ₓv\| > ε/D: at W = 1e-3 on the initial flow, breaking at 0.006 t_sc and earlier on a finer grid; at W = 1e-2 it breaks at 0.62–0.94 t_sc | — | **fails** (ill-posed) |
| (iii-a) k⁴ + k⁶ | no | below the minimum at 0.81–1.04 t_sc; breakdown delayed to 1.07–1.50 t_sc | — | **fails** |
| (iii-b) k⁶ replacing k⁴ | no | below the minimum at 0.89–1.05 t_sc; breaks at 1.09–1.60 t_sc (W = 1e-2 misplaces 10% at 1.5 t_sc first) | — | **fails** |
| (iv) Madelung form of the wave field (polar variables) | no | identical to its wave form until the first node (≤ 2.2e-6), then departs (22–33× within 0.03 t_sc) and goes singular at 1.12–1.22 t_sc (1.21 on 2× grid) | — | **fails** (pre-declared) |
| The order parameter, full (Cartesian) form, γ = 2, light radial mode | **yes**, by interference | passes; nodes appear from 1.03–1.09 t_sc | coarse-grains like cold dust; self-interaction pressure ∝ W | **passes** for W ≤ 5e-3 (free) and ≤ 1e-2 (gravity) |
| The same with a \|ψ\|⁶ (γ = 3) self-interaction | yes, if W is tiny | — | — | fails at W = 1e-3 (pre-declared R2 **falsified**); passes post hoc only at W ≤ 1e-4 (free) and 1e-5 (gravity) |
| (v) Vlasov f(x, v) on an Eulerian grid | **yes**, by phase-space folding | the grid coarse-grains the filaments (numerical warmth; Gibbs undershoot 10% of peak f) | warmth σ = 0.02 v₀ | **passes**, M ≤ 0.9% (control / ceiling) |
| Mixed-state wave field (21 incoherent wavefunctions) | **yes** | no single coherent phase | carries the velocity dispersion | **passes** against the warm answer, M ≤ 0.3% |
| Adhesion / sticky dust (ν → 0 Burgers) | no, sticks | shocks; mass condenses (5 of 20 000 sheets left with gravity) | keeps 12% (free) / 0.2% (gravity) of its kinetic energy | **fails**, well-posed but wrong (18–70% misplaced) |

### The order parameter's radial mode ([`XR8_order_parameter_scan.py`](XR8_order_parameter_scan.py))

For a complex scalar about its rotating state (the lead track's covariant clock, RESULT.md §3), the radial mode's mass
is μ² = V″(R₀) − Ω². The soft branch's non-relativistic limit is Bogoliubov's ω² = c_s²k² + D²k⁴, with D = ħ/2m and
**c_s = μD**; S1 checks this symbolically. So at fixed de Broglie length, L374's warmth W = c_s²/v₀² = (m_r D/v₀)² *is*
the radial mass m_r = 1/ξ, where ξ is the healing length.

- **Heavy radial mode:** the amplitude is slaved (Thomas–Fermi) and the field is a phase-only, pressure-supported fluid.
  At W = 0.1 the full field and the condensate misplace an identical 21.5%.
- **Light radial mode:** the amplitude is free to pass through zero.

| λ | tracks at | fails at | passing edge in L374 units |
|---|---|---|---|
| L/100, free | W ≤ 5e-3 | W ≥ 1e-2 | m_r ≤ 89/L (ξ ≥ L/89); m_r v₀ t_sc ≤ 14; ω_h t_sc ≤ 1.0 |
| L/100, gravity | W ≤ 1e-2 | W ≥ 3e-2 | m_r ≤ 126/L; m_r v₀ t_sc ≤ 20 |
| L/200, free | W ≤ 5e-3 | W ≥ 1e-2 | m_r ≤ 178/L (ξ ≥ L/178); m_r v₀ t_sc ≤ 28; ω_h t_sc ≤ 2.0 |
| L/200, gravity | W ≤ 1e-2 | W ≥ 3e-2 | m_r ≤ 251/L; m_r v₀ t_sc ≤ 40 |

The invariant is W, i.e. ξ/λ = 1/(4π√W), not m_r t_sc. The same W edges hold at both λ: free streaming passes at
5e-3 and fails at 1e-2; with gravity it passes at 1e-2 and fails at 3e-2. Halving λ doubles the passing m_r v₀ t_sc
(14 → 28) and ω_h t_sc (1 → 2). So the healing length must exceed about one de Broglie wavelength of the streams:
ξ ≥ 1.1 λ passes and ξ ≤ 0.8 λ fails, in free streaming. The self-interaction energy has to be small against the
streams' kinetic energy where they cross. In physical units (XR8_spec_table N3, W_c = 5e-3) that is a radial mass
m_r ≤ 2√W_c (v/c) m ≈ 6e-25 eV (a Segue-1-like dwarf) to 2e-22 eV (a cluster core), and a quartic self-coupling
λ₄ ≲ 4e-84 to 3e-74 (2e-78 in a Milky-Way halo). **The field must be nearly free.**

The pre-declared R2 ("the γ = 3 index is irrelevant when the radial mode is light") is falsified. At equal W the |ψ|⁶
interaction, which grows as ρ² where streams pile up, stops the crossing: it needs W about 100× smaller (post hoc:
tracks at ≤ 1e-4 free and ≤ 1e-5 with gravity). In free streaming both indices change verdict near an interaction
energy at the caustic peak of 0.2–0.6 of v₀²/2. With gravity they share no single threshold.

### Nodes, and why the phase cannot be the clock ([`XR8_nodes_and_polar_form.py`](XR8_nodes_and_polar_form.py))

Every tracking wave run has no node before the first crossing. Its first node falls at 1.03–1.09 t_sc, and its
node-event count by the end is 778–3112 (free) and 28 000–111 000 (self-gravitating). The census is resolution-converged:
by 3 t_sc the count is 796 at L/100 and 3112 at L/200, identical on 2× the grid, and at L/100 also at 4× coarser
sampling. The windings are ±1. The count grows 3.9× when λ halves, a fixed number per de Broglie space-time cell
(λ × λ/v₀).

The Madelung (polar) form of the same field is the order parameter with its density slaved to one velocity. It matches
the wave form to ≤ 2.2e-6 until the first node, departs 22–33× within 0.03 t_sc after it, and becomes singular
(ρ → 0) at 1.12–1.22 t_sc (1.21 on twice the grid). This is booked against the polar variables, not the field.

### The index question and the warm continuum ([`XR8_phase_space_continua.py`](XR8_phase_space_continua.py))

A warm water-bag with the sound speed of L374's warmest cell (W = 0.1) sits 12–17% from the cold answer in free
streaming (3–14% with gravity). That is the part of L374's 21.5% that is warmth. Scored against that warm answer, no
single-velocity form tracks it:

- the γ = 2 condensate misplaces 12–13% free and breaks at 1.56 t_sc with gravity;
- the coherent γ = 2 field misplaces 12–13% free and 11–15% with gravity;
- the γ = 3 condensate breaks at 1.07 t_sc in both tests;
- the coherent γ = 3 field misplaces up to 19% free and 57% with gravity.

The index is not the obstruction. The mixed-state wave field tracks the warm answer to ≤ 0.3%. The Vlasov continuum
tracks the cold answer to ≤ 0.9%.

## Part C — what the fluid can be (scoped: no V0 mapping; the V0 writer's DF1 owns that)

| Passing continuum | Completion of the order parameter Φ = √n e^{iθ}? | Framework's own field? | Cost |
|---|---|---|---|
| Coherent field, γ = 2, W ≤ 5e-3 (free) / 1e-2 (gravity) | **Yes**: the full (Cartesian) order parameter with a light radial mode (m_r ≤ 89/L, m_r v₀ t_sc ≤ 14 at L/100; ≤ 178/L, ≤ 28 at L/200; invariant: ξ ≳ 1.1 λ) | **No.** V0's added fields are all leafwise auxiliaries (CV2, `chk_v0_2026/README.md`), and its only propagating scalar is the khronon (FL1 F1, uncommitted). The lead track's charged clock has exactly this content, but it identifies T with the clock, and that fails at the first node. | one new complex field; m ≳ 1.9–5.2e-19 eV (L383); nearly free (λ₄ ≲ 2e-78 in a Milky-Way halo); the amount (U(1) charge) is initial data; kernel-invisible via L353's pair (FL1 F2); clearing and retention still need an action (A6, A7) |
| Coherent field, γ = 3 (\|ψ\|⁶) | Yes, but only at W ≲ 1e-5–1e-4 | No | as above, ~100× stricter on the self-coupling. **Flag:** in Berezhiani–Khoury the superfluid *is* the MOND mediator, which conflicts with A3 (L353: Newtonian only) and A11 (MS1: the switch must not read the carrier) |
| Mixed-state (incoherent) wave field | **Flag:** not a single coherent order parameter. It is an incoherent ensemble of the same field, a normal rather than condensed state, with no global θ to lock to the khronon | No (same field as above) | same field, no new content beyond it; granule heating (L383's floor) applies |
| Vlasov f(x, v) | **Flag:** fits no order-parameter reading. f is the collisionless equation itself, the particle continuum | — | "not particles" only as the Wigner function of the two field states above |

Failing continua and their readings:

- The condensate and its completions are the order parameter's phase-only (Thomas–Fermi) limit plus EFT operators.
- The Madelung fluid is the order parameter in polar variables.
- Adhesion has no order-parameter reading.

Excluded by the spec without a run:

- the khronon's own dust (A9);
- the aether: one velocity per point;
- V0's auxiliaries: leafwise fields with no independent initial data (CV2); the multipliers among them (Φ, Ψ, λ) are
  excluded outright (A10).

**For the V0 writer's constraint-Hessian and fold check, hand over:**

- the coherent order parameter with θ ≠ τ (its NR limit as tested here);
- its mixed state.

As a negative control, add the charged clock with T = τ: it should fail the fold condition at the first node.

## Checks and controls

| Script | Main | MUTATE (must fail) |
|---|---|---|
| `XR8_spec_table.py` | 14/14, rc = 0 (4 s) | tampered Bullet ratio: A4 fails, rc = 1 |
| `XR8_condensate_completions.py` | 11/11, rc = 0 (4m19s wall, 2m36s CPU) | γ = 2/3 cells at W ≤ 1e-3 replaced by their wave form: L374's cells at W = 1e-3 and 1e-4 then track in both tests; R1 fails, rc = 1 |
| `XR8_order_parameter_scan.py` | 6/7, **rc = 1: the pre-declared R2 (γ = 3 irrelevant when the radial mode is light) is falsified** (1m35s) | heavy radial mode (every W × 100): nothing tracks; R1 and R2 fail, rc = 1 |
| `XR8_nodes_and_polar_form.py` | 6/6, rc = 0 (1m34s) | polar form replaced by the wave form it rewrites: no breakdown; R4 fails, rc = 1 |
| `XR8_phase_space_continua.py` | 7/7, rc = 0 (3m04s) | mass-conserving BGK collisions (ν t_sc = 50) in the Vlasov continuum: M 7–37%; R5 fails, rc = 1 |

Wall times were taken on a shared machine at load average 30–50 on 16 cores. Every script is single-threaded and
under 5 minutes.

## Disclosure: code tests before the pre-declarations, and changes after first test runs

Scratch prototypes (not committed) preceded the scripts. They showed:

- first nodes at 1.03–1.08 t_sc;
- Vlasov M ≤ 0.8%;
- the Madelung departure at the first node;
- warmth 12–17%;
- sticky dust 18–70%;
- the mixed state ≤ 0.1% free;
- a completions survey at nx = 2048;
- a k⁶ step diagnosis: spurious 0.29 t_sc breakdowns at L374's step, converged at half and quarter step.

The scripts' docstrings disclose every change made after a script's own first test run:

- XR8 1/4: the k⁶ completions run at half L374's step, with a new check C5c.
- XR8 2/4: post-hoc γ = 3 cells, labelled as such; R2 kept as falsified.
- XR8 3/4: the γ = 3 cell removed from R3's claim; R4's pre-node agreement 1e-6 → 1e-5 with a departure clause; C1
  changed to a resolution-convergence test.
- XR8 4/4: C2's sampling tolerance 2e-3 → 5e-3 (measured 2.1e-3); Vlasov filters strengthened, cutting the Gibbs
  undershoot from 39% to ~10% of the peak f.

## Limits

- One dimension, a static background, non-relativistic, weak field, L374's single initial condition.
- The Galileon-type cubic needs a 2-D/3-D test.
- Collapse and the relativistic complex field are not run.
- The tested λ/L = 1e-2–5e-3 is conservative for Milky-Way halos and clusters (physical λ/R ≤ 4e-5) but not for
  ultra-faint dwarfs (λ/r_h ≈ 0.1–0.3). There L383's heating floor, not this test, binds.
- The mixed state is 21 discrete velocities, checked against the uniform water-bag.
- Vlasov is a ceiling: its grid warmth is σ = 0.02 v₀ plus filter coarse-graining.
- Clearing, retention and the ~600 km/s kick (A6, A7) are not addressed. The passing field still needs an action for
  them.

## Files

- `XR8_common.py`: shared pure solvers (imports L374's pure functions).
- `XR8_spec_table.py` + `.out`, `_MUTATE.out`, results JSON.
- `XR8_condensate_completions.py` + `.out`, `_MUTATE.out`, results JSON.
- `XR8_order_parameter_scan.py` + `.out`, `_MUTATE.out`, results JSON.
- `XR8_nodes_and_polar_form.py` + `.out`, `_MUTATE.out`, results JSON.
- `XR8_phase_space_continua.py` + `.out`, `_MUTATE.out`, results JSON.

Run any of them from the repository root with `python3 real_research/cross_thread_review_2026_09_26/<script>.py`. Add
`MUTATE=1` for the control.
