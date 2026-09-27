# XR16 — the FK2 lane: the dark fluid's own conversion surface, the flagship at z = 2.5, and the forest

FK1 (c2e1fa119) builds the kick inside the dark fluid's order parameter:
- a U(1)-breaking splitting, ε/m² = 1.84–2.35 × 10⁻⁶;
- the conversion φ_Hφ_H → φ_Lφ_L at v_k = 575–650 km/s;
- a pure cross quartic λ(K)(Im Φ²)², gated through K with q = 1.75;
- Bose stimulation.

Its trigger is the fluid's own density. FL2 (e96b71eb0) puts it in V0's dark slot.

This lane asks two things of that trigger:
- **Part A.** Does its conversion surface clear the flat-a₀ flagship radius r_F by z = 2.5? MS2/DE4 allow a retained
  carrier S ≤ 0.059 at r_F. L388's particle-mesh residue (S = 0.063–0.075) fails, so the row is "not established".
- **Part B.** Is its early conversion budget safe for the Lyman-α forest?

The design was supplied by the session that built FK1 and is implemented here, not re-derived: the depth criterion, the
reuse of AT1, the progenitor gate and the brackets. It is a construction. The carrier is a state of the framework's own
field, and its **mass is still required**.

Script: `XR16_fluid_conversion_surface.py` (+ `.out`, `_MUTATE.out`, `_results[_MUTATE].json`). It execs parts of AT1
and reads committed JSON and source text (AT1, AT2, L365). Nothing outside this folder was edited, and no particle-mesh
run was made.

## Verdicts

### Part A — the flagship at z = 2.5: passes on the record's grid (M_b = 10¹⁰–10¹¹ M☉)

**The flagship radius is inside the surface.** At z = 2.5 the fluid's stimulated front sits at 0.92–1.00 r200 in every
flagship host. The flagship radius r_F sits at 0.16–0.36 r200, so it is inside even the spontaneous-ignition region
(0.44–0.75 r200 for C = 0.3–3).

**The in-place population left early.**
- In the main progenitor the front passed r_F at z = 3.8–6.9.
- At that moment the intact progenitor's v_esc(r_F) was 107–421 km/s, below every kick in 575–650 km/s. That holds in
  540/540 cells at 575–600 km/s and in all cells at 650.
- The gate holds for any dlnM/dz magnitude ≥ 0.21. The bracket tested is 0.6–1.0.

**What is left at r_F.** With that population gone, and over every bracket, S at r_F ≤ 7 × 10⁻⁵ and the zero-point shift
is ≤ 1 × 10⁻⁴ dex. The brackets are:
- K = C·E_need = 18–540;
- α = 0.6–1.0;
- v_k = 575–600 km/s;
- both footings, the gas range, and both kernels;
- both readings of the potential's response.

The per-particle refinement G2 gives ≤ 0.0042. What the flagship's 0.059 then has to cover is FK1's declared cold φ_L
misalignment share, which is not scored here.

### The in-place trap the design warned about bites only if the well is held fixed

"In place" means AT1's rule at the fluid's surface with no early escape. This is the MUTATE, and the pre-declared H-A2
(check T1).

| M_b (M☉) | in place: AT1's self-consistent reading | in place: intact well held fixed | the fluid's history (G1), both readings |
|---|---|---|---|
| 10¹⁰ | 0 | 0.0007–0.0037 | 0 |
| 10¹⁰·⁵ | 0.0004–0.0009 | 0.015–0.041 | 0 |
| 10¹¹ | 0.006–0.010 | **0.12–0.21** | 0 (self-consistent); ≤ 7 × 10⁻⁵ (intact) |
| 10¹¹·⁵ | 0.09–0.58 | 0.43–0.72 | see below |

- **AT1's own reading.** The potential drops as the converted carrier leaves, and the daughters born in place escape. S
  is ≤ 0.010 and the shift ≤ 0.020 dex on the record's grid. **The pre-declared H-A2 (in place fails) is falsified in
  this reading** (T1 FAIL, reported).
- **The intact well held fixed.** The in-place S reaches 0.21 at M_b = 10¹¹ (shift 0.35 dex). That is the designer's
  L388-like number.
- A front that sweeps out over Gyr lies between the two readings. The early escape is what makes the pass independent of
  that unresolved response.

### M_b = 10¹¹·⁵ (outside MS2's grid): mostly fails

| gas | M_h at z = 2.5 | rows passing | progenitor v_esc(r_F) at the passage |
|---|---|---|---|
| ×0.67 | 6.1 × 10¹³ | 0/120 | 607–1170 km/s |
| ×1.0 | 1.9 × 10¹³ | 42/120 | 481–803 km/s |
| ×1.5 | 7.8 × 10¹² | 112/120 | 407–612 km/s |

- These are group-mass halos. At z = 2.5 their stars are 1.0–1.6 × 10¹¹ M☉ (Moster, with L356's gas range).
- The progenitor gate escapes in 77 of 180 cells, and there the early escape clears r_F (S ≤ 0.0025; check A2).
- Elsewhere the daughters stay bound (S up to 0.58 in the self-consistent reading and 0.72 in the intact one).

### Part B — the forest: the budget leaves AT2's regime, so the forest is not established

**The trigger is not mass-selective.**
- The gate's threshold in units of ρ_crit(z) is (5/3)E²: 15, 35 and 66 at z = 2, 3 and 4. That is below every halo's
  mean density (200 ρ_crit) for z ≲ 6.
- So at z ≲ 4 every halo above the fluid's own scale converts almost whole, and the budget tracks the collapsed fraction:
  0.433 of 0.437 at z = 2.
- Of the converted carrier, only 0.21, 0.31 and 0.45 sits in hosts ≥ 10¹⁰·⁵ M☉ at z = 4, 3 and 2 (fiducial). AT1's
  acceleration trigger put ≥ 0.98 there.

Converted fraction of the carrier F (unweighted; running maximum in time):

| case | F(z = 4) | F(3) | F(2) | bias-weighted escaped F_b(3 / 2) |
|---|---|---|---|---|
| fluid, m = 2e-19 eV, K = 60 (fiducial) | 0.255 | 0.342 | 0.433 | 0.471 / 0.497 |
| most favourable: K = 18, the record's M_min = 10⁸ M☉ | 0.153 | 0.245 | 0.352 | 0.372 / 0.431 |
| heavier m (grid floor 1.5 × 10⁵ M☉), K = 540 | 0.312 | 0.382 | 0.460 | 0.511 / 0.520 |
| **AT1's A2 cell: what AT2 scored** | 0.032 | 0.052 | 0.083 | 0.100 / 0.107 |

**AT2's result does not carry over.**
- Even at the most favourable corner the budget is 4.7× (z = 3) and 4.2× (z = 2) AT1's cell. The fiducial is 6.5× and 5.2×.
- AT2's "≤ 0.33% at z = 3, ≤ 1.7% at z = 2" was measured in that smaller regime.

**The projection straddles the gate.**
- The committed particle-mesh responses give L365's rule per unit F(2) as 0.06–0.09 for sparsest-first removal and
  0.11–0.31 for densest-first.
- That projects an L365-rule deviation at z = 2 of 0.022–0.110 (most favourable) and 0.027–0.135 (fiducial), against
  the 10% gate.
- This is an extrapolation past the largest committed budget, F(2) = 0.28.
- The densest-first reading crosses the gate; the sparsest-first one does not. The fluid's pattern is every halo down to
  ~10⁶ M☉, spread through the web, and which reading it follows is not decidable here.

**Verdict: the forest is not established for the fluid's own trigger.** Deciding it needs a particle-mesh run with this
budget, which is the owner's call. The history is in the results JSON under `numbers.B.history`.

### Flag (B3, not scored): the design's stimulated criterion reaches the web

In the Hubble flow the gain at density ρ is (ρ/ρ_bg)²·E_need e-folds per sweep. A gain of ≥ 1 e-fold, the design's
stimulated criterion, is met:
- above δ = 0.2–1.1 at z = 2, 1.7–3.6 at z = 3 and 4.0–7.7 at z = 4;
- at the mean density itself below z ≈ 1.2–1.8.

This lane does not compute whether seeds from converted halos drive a front through filaments. That would take
ln(pump/seed) e-folds, not 1. If they do, the F(z) above is a lower bound, and a low-z conversion of the background would
be a problem well beyond the forest.

## Checks

| Check | Main run | MUTATE (in-place population kept) |
|---|---|---|
| C1 AT1's committed A2 rows at z = 2.5, v_A = 600, through this lane's copy (36 rows) | PASS, max dev 0 | PASS |
| C2 the copy without the gate is bit-identical to AT1's `retained_acc` | PASS, 0 | PASS |
| C3 the depth integral: closed form (isothermal) and adaptive quadrature with D | PASS, 9e-5 | PASS |
| C4 v_esc from L321's potential against the closed form | PASS, 6e-6 | PASS |
| C5 AT2's own functions reproduce its committed F4 table and cell rules | PASS, 0 | PASS |
| F1 r_F inside the fluid's surface at z = 2.5 (all hosts, K, v_k) | PASS | PASS |
| F2 (reported) passage epochs and escape speeds; fronts monotone; cusps ignite | PASS | PASS |
| **A1 = H-A1 (strict)** S ≤ 0.059 and shift ≤ 0.10 on the record's grid, both readings | **PASS**: S ≤ 7e-5 | **FAIL**: S 0.21, shift 0.35 dex (intact reading; self-consistent 0.010) |
| **A2** the early-escape step clears every escaped cell, including M_b = 10¹¹·⁵ | **PASS**: S ≤ 0.0025 | **FAIL**: S 0.59, shift 1.11 dex (M_b = 10¹¹·⁵) |
| T1 = H-A2 (pre-declared, reported) in place fails in AT1's own reading | **FAIL**: 0.010 | FAIL (the same computation) |
| A3 / A4 (reported) G2; the 10¹¹·⁵ extension | reported | reported |
| **B1 = H-B** the budget exceeds AT2's scored budget at the most favourable corner | **PASS**: 4.7× / 4.2× | PASS (the budget does not depend on the step) |
| B2 / B3 (reported) forest projection; the web flag | reported | reported |

**Main run: 14/15, no load-bearing failure, rc = 0.** T1 is the pre-declared expectation that fell, and is reported.

**MUTATE: 12/15, load-bearing failures A1 and A2, rc = 1, as designed.** The MUTATE keeps the in-place population.
- In AT1's self-consistent reading alone it would still clear the record's grid (S ≤ 0.010).
- It fails through the intact-potential reading (S = 0.21 at M_b = 10¹¹) and through the 10¹¹·⁵ hosts.
- So the early escape is load-bearing exactly where the retained carrier depends on how the well responds.

**Pre-declaration.** The three hypotheses (H-A1, H-A2, H-B, in the script's docstring) were written in the session's
scratch notes before any XR16 number was computed. An exploratory run of the components then followed, not committed:
- the fronts at z = 2.5 and the passages;
- ~75 retention calls on the M_b = 10¹¹ and 10¹¹·⁵ hosts: in place, surface-only, the intact-potential reading and G2,
  at v_k = 575–600.

At M_b = 10¹¹ it showed the in-place S at 0.006–0.010 in AT1's reading and 0.12–0.21 with the well held fixed. H-A2
was kept as declared and is reported as it fell. The one change afterwards made A1 stricter: it must now hold in both
potential readings, not only AT1's.

## How it is computed

**AT1's machinery, as designed.** `AT1_acceleration_trigger_highz.py` is exec'd from its committed text:
- up to "NFW loss cone + escape (added)": L357's head, L320's top, BK1's kernel and the baryons of a halo;
- then from "retention with decay on entry (added)" through `flagship_rows`.

AT1's main, its Monte Carlo tables and its checks are not run. The retention is a line-for-line copy of AT1's
`retained_acc`, bit-identical without the gate (C2). It adds two things:
- per-particle weights on the in-place decays;
- the potential-response reading.

**The conversion depth** is the design's
S_c(r) = (2CH/π) ∫_r^∞ (ρ_c/ρ_bg)² D dr′/σ(r′), with:
- ρ_bg = δ_t ρ̄_carrier and δ_t = 2.5E²/(1.5 Ω_m(z));
- D = exp(−½(Δv/σ)²), where Δv = v_k − √(v_k² − 2ΔΦ).

Spontaneous ignition is where S_c ≥ 1, and the stimulated front is where S_c ≥ 1/E_need. The front depends only on
K = C·E_need, so the design's six corners (C = 0.3–3, E_need = 60–180) are K = 18, 54, 60, 180 and 540. Each choice below
is the conservative side for the verdict it feeds:
- **The carrier is AT1's truncated NFW**, with no infall region. So S_c(r200) = 0 and the front lies inside r200. That is
  a smaller front, so r_F is passed later, in a bigger progenitor.
- **σ is the untruncated isotropic Jeans dispersion**, which is larger than the truncated one. That again gives a smaller
  front.

**The progenitor gate (G1, the design's).**
- The main progenitor follows M(z) = M(2.5)·e^(−α(z−2.5)), with α = 0.8 (0.6–1.0).
- Its fronts are computed on z = 2.5–20 in steps of 0.1. Concentrations are AT1's Dutton–Maccio values with a floor at
  c ≥ 3, where the fit's extrapolation collapses. The floor moves v_esc(r_F) by ≤ 0.6 km/s.
- z_pass is the first epoch at which the front reaches r_F.
- If the intact progenitor's v_esc(r_F) at z_pass is below v_k, the in-place population left then and is dropped. Only
  the daughters converting on entry at the z = 2.5 surface are kept.
- Otherwise AT1's in-place rule stands.

**G2 (reported).**
- Each in-place particle converted when the front reached its pericentre.
- It is kept with weight 1 − P_esc, taken from L357's escape table at that epoch's v_esc and σ.
- Kept daughters are then treated in place at z = 2.5, which is pessimistic because the well is deeper then.

**Two readings of the potential's response.**
- AT1's self-consistent iteration (iters = 2).
- The intact halo held fixed (iters = 0).

**Part B.**
- L357's halo model: CLASS linear P(k), Sheth–Tormen mass function and bias, Dutton–Maccio concentrations (c ≥ 3).
- Every halo gets the same depth criterion and its converted fraction M_c(< r_s)/M_c(< r200).
- The fluid's own cut-off is Schive+16's FDM suppression at m = 2e-19 and 1e-18 eV. The grid floor, 1.5 × 10⁵ M☉,
  stands for heavier m. L357's M_min = 10⁸ M☉ is kept as the most favourable case: it removes more small halos than any
  allowed fluid mass.
- Ignition is checked at the soliton core (Schive+14) with C = 0.3. It fails in 36 halo evaluations, all at z = 10–15 and
  M_h = 1.5 × 10⁵–1.9 × 10⁶ M☉; they are counted as unconverted.
- The budget is the running (irreversible) maximum in time.
- The forest is not re-simulated. The bound uses AT2's own functions (C5) and the committed responses: AT2's
  densest-first cells, its sparsest-first MUTATE cells, and L365's mesh-trigger runs at v ≤ 700 km/s.

## Said plainly

- **This is a halo-model construction.**
  - The conversion rule, its brackets and the progenitor gate are the design's.
  - Only the main progenitor is followed, on a single exponential accretion history. Mergers are not modelled.
  - Accreted carrier converts at the surface on arrival. For the record's hosts that surface sits at ~r200, where v_esc
    is below the kick.
- **The pass is for the record's grid.** It covers M_b = 10¹⁰–10¹¹ at z = 2.5, on AT1's (GP5/L320) flagship definition
  and on MS2's S ≤ 0.059. The group-mass 10¹¹·⁵ hosts mostly fail.
- **The forest is open, not failed.** The budget is 4–7× what AT2 scored, and the committed responses straddle the 10%
  gate at that budget. The B3 flag is not scored.
- **Unchanged.** The carrier's mass is still required. The cold φ_L misalignment share adds to S directly and is not
  scored here.

## Hand-offs (the owners' calls; nothing outside this folder was touched)

1. **The particle-mesh track:** a forest run with the fluid's budget F(z) from `numbers.B.history`, removing carrier from
   all halos down to the fluid's scale rather than densest-first.
2. **The FK1/FL owner:**
   - the trigger's non-selectivity (B1);
   - the stimulated criterion in the Hubble flow (B3): whether seeded fronts cross filaments at z = 2–4 and the mean
     background below z ≈ 1.2–1.8.
3. **The flagship row:** for the fluid's own trigger, it is now "passes on the halo model in both potential readings,
   M_b = 10¹⁰–10¹¹". The caveats above apply. The 10¹¹·⁵ hosts mostly fail: 154 of 360 rows pass, only where the
   progenitor gate escapes.

## Reproduction

`python3 real_research/cross_thread_review_2026_09_26/XR16_fluid_conversion_surface.py` from the repository root.
- The main run takes ~50 min, single-threaded, at ~3 GB peak.
- `MUTATE=1` runs its control.
- `XR16_SMOKE=1 XR16_OUTDIR=<dir>` is a reduced code test, never for the record.
