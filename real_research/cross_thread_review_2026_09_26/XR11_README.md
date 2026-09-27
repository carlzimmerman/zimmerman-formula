# XR11 — "a fluid of dark energy swirling down between the bands": the edge layers

Cross-thread review, 2026-09-26 (night). Read-only on every other file. Four new files of code in this folder (three lanes
and one shared module); every lane has controls that reproduce committed numbers exactly, and the two physics lanes have a
MUTATE run that must fail. Both a0 footings wherever a0 enters (canonical 9.36e-11, alt 1.13e-10 m s⁻²). κ = ½ stays a
declared input. The dark mass is still required. The dark fluid is FL1/FK1's order parameter (φ_H the cold carrier, φ_L the
kicked products), not a new particle species.

**The idea, and the two readings tested.** The author's idea, verbatim: "the halos is like a fluid of dark energy swirling
down between the bands". The author confirmed that the bands are the edge (transition) layers of the MOND regions. The
trigger is DE12 (7f84b3546): once the converged model's MOND-sector gate is varied as an action term, it acts as a
negative bulk modulus on the layer's gas. The phantom's response squared, A², with A ~ 50–100, amplifies it:
c_gate = 1500–3700 km/s against 37–117 km/s gas. DE13 (6daea932c) found no gradient repair that works at an acceptable
cost.
- **(A) The dark fluid carries the layer's stiffness.** The gate reads a dark-fluid variable, so its second variation lands
  on the fluid (A = 1) instead of the gas. The price is MS1's edge force on the fluid. Could that force itself be the
  clearing mechanism?
- **(B) Swirl or flow through the layer** stabilises DE12's gradient instability.

## Answer

**Neither works.**
- **(A) moves the problem; it does not remove it.** Reading the dark fluid takes the whole second variation off the gas.
  This is exact: the gas block is zero, with no A² and no A. It also lowers the channel about 10×, to 0.09–0.12 of DE12's.
  But the dark fluid is softer than the gas where the layers sit:
  - φ_H has no pressure of its own (FK1's pure cross quartic).
  - Quantum pressure is metres per second at kpc scales.
  - At the z = 0.25 edges the fluid is a cold infall stream.
  So the dark channel is unstable there, and at z = 2.5 it beats even the generous phase-mixed (Jeans) dispersion.
  The edge force is too weak to clear anything where the layer is stable enough to exist. Where it is strong enough, the
  layer is violently unstable, and an exact inequality ties the two together (the pincer).
  A dark-fluid gate also puts the MOND regions in the wrong places: the kick clears φ_H exactly where MOND must be on.
- **(B) is ruled out on scale.** Swirl and shear add a k-independent frequency, while DE12's Γ = k·sqrt(c_gate² − c_s²)
  grows with k:
  - modes along the rotation axis never feel the rotation;
  - crossing a layer before it grows needs a flow of 26–96 v_f;
  - a swirl at v_f holds only wavelengths 75–260× longer than the layer.

## Reading (A): the gate reads the dark fluid — `XR11_dark_channel_gate.py` (12/13; H1 the recorded failure)

**The derivation (S1, sympy on CV1/MS1's Lagrangian with φ_H and φ_L separate; zero residuals).**
Write the gate as a function of the density it reads, V(ρ) = W(t(U(ρ))). Let B = dL/df, DE12's kernel term
a0²q/(8πG).
- **First variation.** The fluid feels V_H − u_N = −B V′(ρ_H). That is a **well** for a density reading and a **barrier**
  for a depletion reading.
  - φ_L feels nothing if U reads φ_H only.
  - The baryons and light feel nothing either: U reads no metric field and no baryon.
- **Second variation (its k⁰ part).** It is −½ B V″ (δρ_H)² on φ_H only, so c_gate,d² = ρ_H B V″(ρ_H), with A = 1.
  The gas block and the gas–dark cross term are exactly zero. Field responses are O(1/k) or O(1/k²).
- **Controls.** MS1's matter-door leak and its MOND-sector zero are reproduced.
- **The weighted door U = g·U_MS.** It leaks −(B/8πG) C W′ ∇²(Φ − v) g′(ρ_H) onto the fluid and keeps the gas's A²
  term, multiplied by g².

**The fluid's own stiffness (N0; `XR11_shell_model_velocities.py`).**
- **No self-pressure.** FK1's pure cross quartic gives φ_H g_HH = 0.
- **Quantum pressure.** ħk/2m is 4.8 m/s at k = 1/kpc for m = 2×10⁻¹⁹ eV, and less for heavier m.
- **What is left is the velocity distribution.** In the Vlasov/Penrose picture:
  - a phase-mixed, single-humped distribution is stable iff σ > c_gate,d along k;
  - a set of cold streams is unstable for any c_gate,d > 0.
- **L375's shell model.** The lane loads its halo() unedited except for the return line; its histograms are identical to
  L375's (C1). The cold carrier is multistream only out to 400–540 kpc ≈ 2–2.3 r200, with σ_r ≈ 90–170 km/s. Beyond that
  the model injects single-velocity cold shells. The kicked hosts are cleared of φ_H inside ~90–120 kpc.

**The dark channel on real layers (N1).** This is the φ_H density door at the vacuum gate's own threshold (p = 1,
x_c0 = 2.5, w = 0.25), with the carrier uncleared (S = 1), on DE12's hosts.

| z | M_b | edge, kpc (r/r200) | c_gate,d can/alt (km/s) | Jeans σ | the fluid there | Γ(1/kpc)/H, cold |
|---|---|---|---|---|---|---|
| 0.25 | 1e10 | 299 (2.6) | 148/155 | 38 | beyond the multistream zone | 1.9e3 |
| 0.25 | 1e11 | 671 (2.7) | 247/259 | 82 | beyond | 3.2e3 |
| 0.25 | 1e12 | 1512 (2.8) | 410/430 | 180 | beyond | 5.3e3 |
| 0.25 | 1e14 | 5056 (3.0) | 2102/2205 | 591 | beyond | 2.7e4 |
| 2.5 | 1e10 | 63 (1.2) | 127/133 | 73 | multistream | 5.0e2 |
| 2.5 | 1e11 | 142 (1.3) | 212/222 | 159 | multistream | 8.4e2 |
| 2.5 | 1e12 | 319 (1.3) | 351/369 | 349 | multistream | 1.4e3 |
| 4.0 | 1e12 | 154 (0.9) | 355/374 | 454 | inside r200 | 8.3e2 |

- **H1 (pre-declared; FAILED and kept).** The hypothesis was that c_gate,d < 300 km/s on every z = 0.25 galaxy layer.
  The 1e12 group host gives 410/430 km/s; the galaxies give 148–259 km/s.
- **H1b (added after the first run).** The dark channel is 0.09–0.12 of DE12's gas channel on the same host.
- **H2.** At z = 2.5, c_gate,d exceeds the Jeans σ on every galaxy layer. The thinnest margin is the 1e12 host, at a ratio
  of 1.006. At z = 4 that host's layer falls inside r200 and is Jeans-stable, 355 against 454 km/s: the one stable case,
  uncleared.
- **Verdict at z = 0.25.** The layers sit at 2.6–3.0 r200, outside the multistream zone. The fluid there is a cold stream,
  unstable for any c_gate,d, with Γ ≈ 2–5×10³ H at 1/kpc. For a cold wave field the fastest rate is m c_gate,d²/ħ. The
  Jeans σ loses on every z = 0.25 layer too. Only against the effective 100–300 km/s band quoted for 1–3 Mpc would the
  1e10–1e11 layers be marginal. That band is a pairwise/substructure dispersion, not a fine-grained stiffness of the stream.
- **N1c: placed where KiDS wants the regions.** Here the threshold is tuned so that the layer sits at the MOND-sector door's
  own edge (0.77–2.6 Mpc at z = 0.25).
  - c_gate,d is 276–541 km/s against a Jeans σ of 27–154 km/s.
  - The tuned threshold switches on every dark overdensity δ_d ≥ 0.30–1.3.

**The pincer (H4, exact; checked on 72 layer-readings).**
- **The bound.** A smooth gate that switches on or off in ρ has V′ = 0 at the layer's end. So over the rising half,
  max c_gate,d² ≥ (B_min/B_max)(ρ_min/Δρ)|δV|max. It holds on 72/72, with a minimum ratio of 3.1.
- **The depletion lock.** For a depletion power law, c_gate,d² = (1 + |n|)(ρ/ρ_c)|δV| exactly at the layer's centre, to
  3×10⁻¹⁴.
- **What follows.** A stable gate's edge potential stays below about σ² times the rising half's density span, which is
  1.2–2.2 at w = 0.25. A barrier strong enough to clear or confine, |δV| ~ v_esc²/2, would need a span of order
  v_esc²/2σ².

**Can the edge force clear galaxies and let clusters keep their fluid? (H5; `barrier_table` in the JSON).** No.

| host (M_b) | z = 0.25: edge; well / barrier (km/s, √(2\|δV\|)) | v_esc, carrier removed–kept | z = 2.5: well / barrier | v_esc |
|---|---|---|---|---|
| L\* (6.3e10) | 571 kpc; 107–112 / 98–103 | 251–514 | 100–105 / 98–103 | 367–745 |
| group (1e12) | 1512 kpc; 197–207 / 181–189 | 623–1270 | 184–193 / 180–189 | 918–1861 |
| rich group (1e13) | 2231 kpc; 615–645 / 564–591 | 1257–2024 | 563–593 / 552–581 | 1865–2987 |
| cluster (1e14) | 5056 kpc; 1010–1060 / 925–971 | 2701–4333 | 917–967 / 899–947 | 4023–6457 |

- **The outer layers.** The edge potential is at most 0.54 of every host's escape speed, even with the carrier removed. It
  can neither lift a galaxy's fluid out nor separate galaxies from clusters: the ratio is about the same at every mass.
- **Retention.** X-COP's retention is untouched. The cluster barriers are 0.9–1.06×10³ km/s against escape speeds of
  2.7–6.5×10³ km/s. The kick, not this force, decides retention (XR7).
- **Where the force is strong, the layer is not viable.**
  - At the inner boundary of a kicked host's cleared core (~90–120 kpc; N1b) the potential reaches 1.6–1.8×10³ km/s.
  - Next to the flagship's r_F it reaches 340–620 km/s.
  - In both places c_gate,d is 0.6–4×10³ km/s. A barrier strong enough to hold the fluid out sits on a layer that tears
    itself apart.

**What it costs (K1).**
- **Kernel invisibility is lost at every edge.** The edge force is 10–13× the carrier's own gravity at z = 0.25 L\* layers
  and 2.5–2.7× at z = 2.5. A phase-mixed carrier would respond by |δV|/σ_J² ≈ 1.0–1.3, piling 5–6% of its mass inside
  2 Mpc into the layer.
- **KiDS sees the placement first.**
  - The φ_H door's L\* edge sits at 571–747 kpc (S = 1 and the shell model's no-decay run).
  - That is where the MOND-sector door would sit at x_c,eff(0.25) ≈ 14–16. XR9's scan gives Δχ² ≈ +140 to +161 there,
    against its cap of 4.42.
  - A 1.5 Mpc edge would need the threshold × 0.06–0.10. That switches on every dark overdensity above δ_d ≈ 0.3–0.5.
- **The flagship (MS2).** A window exists: fully on at r_F needs S ≥ 0.018–0.051, while the zero point needs S ≤ 0.059.
  But the layer then sits at 21–46 kpc, just outside r_F.
  - Its c_gate,d is 644–1173 km/s.
  - Its well is 4.6–7.7 σ_J² deep, so a phase-mixed carrier would pile up by e⁵–e⁸ next to r_F.
  - MS2's carrier-blind door has neither problem.

**Where such a gate puts the MOND regions (H3, N2).**
- **The density door on the kicked carrier** (shell model, KiDS bins 1–2) is on only in the uncleared φ_H shell,
  ~100–300 kpc. It is off inside ~90–120 kpc, where rotation curves live.
- **Uncleared,** the L\* edges lie inside 1 Mpc, against KiDS's ~1.5 Mpc (XR9).
- **The depletion mirror** (vacuum reference) is on wherever δ_d ≤ 4.2 at z = 0.25 or δ_d ≤ 23 at z = 2.5: voids, sheets,
  most filaments and the forest's IGM.
  - On a kicked host it is on in the cleared core, off in the φ_H shell, and on again beyond.
  - To switch the flagship's r_F on it must switch on every δ_d ≤ 42–120 at z = 2.5.
- **The weighted MOND-sector door keeps the placement, but the gas keeps g²·A².** A uniform g is only a threshold rise, and
  none makes 1e6 K gas stable while a region survives beyond ~1.5 kpc. At z = 0.25 and 1e11, taking g from 1 to 10⁻⁴
  lowers c_gate from 2235 to 451 km/s while the edge shrinks from 1373 to 15 kpc. At z ≥ 2.5, c_gate even rises again as
  the layer reaches the Newtonian core.

## Reading (B): swirl and flow — `XR11_swirl_flow.py` (5/5)

- **X1 (sympy, exact).** The rotating layer's dispersion relation is
  ω⁴ − ω²(c_eff²k² + 4Ω²) + 4Ω²c_eff²k² cos²θ = 0, with c_eff² = c_s² − c_gate².
  - With c_eff² < 0 the product of the ω² roots is negative for every θ ≠ 90°. A mode grows at every rotation rate.
  - Along the axis, rotation drops out entirely.
  - Only θ = 90° (and the axisymmetric shearing sheet, ω² = κ² + c_eff²k²) is held, and only for k < κ/|c_eff|.
- **X2 (shearing waves, numeric).**
  - While κ < |c_eff|k, which holds on every real layer, no wave is stabilised. Every perturbation grows by more than e³ in
    10 growth times.
  - Shear can delay a leading wave; the slowest grew ×58 instead of ×1.1×10⁴. It stops none.
  - The axis mode is unchanged.
  - Only the long-wave case κ > |c_eff|k, reported and not gated, holds the nearly axisymmetric waves.
- **X3 (DE12's layers, both footings, 1e6 K gas).**
  - Crossing the layer within 1/Γ at the longest mode that fits needs 3.5×10³–2.3×10⁴ km/s, which is 26–96 v_f. At
    k = 1/kpc it needs up to 2.5×10⁶ km/s.
  - At v_f the gas grows 26–96 e-folds per crossing.
  - A swirl at v_f holds only wavelengths ≥ 0.7–123 Mpc, which is ≥ 75× the layer. Γ(2π/L)/κ = 75–262.
- **X4 (reading A's dark channel).**
  - The cold stream needs 0.8–2.7×10³ km/s to cross, against v_f = 106–334 km/s.
  - A swirl at v_f holds only wavelengths ≥ 0.17–8 Mpc; at FL3's spin, ≥ 2.4–117 Mpc.
  - Below FL3's vortex spacing at the layer (0.35–1.4 kpc) the superfluid is irrotational and has no Coriolis force at
    all.
  - A flow of order v_f could beat the growth only on the massive z ≥ 2.5 layers where c_gate,d ≈ σ_J, and those are
    already marginal or stable.

## Controls and mutations

| Script | Controls | MUTATE |
|---|---|---|
| `XR11_shell_model_velocities.py` (~60 s) | C1: its halo() returns L375's histograms exactly (0 counts). C2: retention inside 0.5 Mpc/h is 0.245/0.230, against L375's 0.247/0.232. | none: it only produces inputs (as XR9_carrier_halos) |
| `XR11_dark_channel_gate.py` (~6 s) | C1: DE12's c_gate_max and edge on all 24 layers and its A = 1 control (18.39/93.38 km/s), 0e+00. S1: MS1's matter leak and MOND-sector zero. | A put back on the dark channel: H1b fails (ratio 5.0–8.3), and H5 fails too (5.0× v_esc); rc = 1 |
| `XR11_swirl_flow.py` (~3 s) | C1: DE12's c_gate_max, 0e+00 | the anti-pressure removed (c_eff² = +c_s²): X1, X2 and X3 fail; rc = 1 |

**Recorded, not hidden.**
- **H1 failed as declared** in the first run and fails in every run: 430 km/s at the 1e12 group host, so the main run's
  rc = 1 (12/13).
- **The first run scored 8/11.** Two of its failures were this lane's own evaluation bugs. Both were fixed before the
  second run and are noted in the script's docstring.
  - S1's weighted-door comparison simplified the expression before comparing it; sympy rewrote a log. Compared
    unsimplified, the difference is exactly 0.
  - H4's lock was evaluated at a layer centre found on an interpolated profile. That gave 5.8×10⁻⁶ against the 1×10⁻⁶
    tolerance. Solved on the analytic NFW it is 3×10⁻¹⁴; the tolerance is unchanged.
- **H1b was added after the first run** as the MUTATE's target. Its threshold, ratio < 1, is not tuned; the first run
  gave 0.09–0.12.
- **The shell-model lane's first development marker was wrong.** It took the outermost bin with outgoing cold elements as
  the splashback. That picked up the initial Jeans-Gaussian tail escaping, at ≲1e-2 of the mean density. It was replaced
  before any number was used, by the outermost bin where inflow and outflow coexist.
- **The shared code was moved to `XR11_common.py`** after the second run. The results JSON did not change (0 differences).

## Scope

- Frozen background and local WKB (k ≫ 1/layer), with spherical isolated hosts. The k⁰ part of the second variation is
  kept; field responses are O(1/k) and O(1/k²).
- The Vlasov criterion is used in its Penrose (static) form. The Jeans σ is the isotropic, untruncated-NFW value: generous
  at the edges.
- The shell model's limits apply: one accretion history, and no cold carrier beyond ~2 r200 at z = 0.25.
- The flagship is taken on DE12's host convention (point-mass baryons), not DE4's galaxy.
- Nothing here simulates the instabilities' nonlinear outcome.
- Other dark-fluid variables were not scanned, for example the φ_L products' density or ratio readings. The pincer (H4)
  applies to any smooth gate on any dark density.

## Files (only these, all `XR11_`)

| Stem | Script | Output | Results | MUTATE output | MUTATE results |
|---|---|---|---|---|---|
| `XR11_common` | `.py` (the shared reimplementation of L352/DE12's machinery; imported, not run) | — | — | — | — |
| `XR11_shell_model_velocities` | `.py` | `.out` | `_results.json` | — | — |
| `XR11_dark_channel_gate` | `.py` | `.out` | `_results.json` | `_MUTATE.out` | `_results_MUTATE.json` |
| `XR11_swirl_flow` | `.py` | `.out` | `_results.json` | `_MUTATE.out` | `_results_MUTATE.json` |

Plus this `XR11_README.md`.

Run from the repository root, in this order. Add `MUTATE=1` to the last two to run their controls.
1. `python3 real_research/cross_thread_review_2026_09_26/XR11_shell_model_velocities.py`
2. `python3 real_research/cross_thread_review_2026_09_26/XR11_dark_channel_gate.py`
3. `python3 real_research/cross_thread_review_2026_09_26/XR11_swirl_flow.py`
