# XR9 — the small-region door

Cross-thread review, 2026-09-26 (night). Read-only on every other file: five new scripts in this folder, each with controls
that reproduce committed numbers exactly and a MUTATE run that must fail. Both a0 footings in every gate (canonical
9.36e-11, alt 1.13e-10 m s⁻²). κ = ½ stays a declared input; the dark mass is still required; no new particle species.

**The door.** The converged model's MOND regions are large (an L\* edge of ~1.4–1.7 Mpc at z = 0) because the KiDS cap
was derived with the switch alone (DE2 3.867; 4.347 on the MOND-sector reading at w = 0.25, DE9). DE10 found that the
carrier's own lensing passes KiDS easily at p = 1, x_c0 = 2.5. The door: raise the threshold (r_e ∝ 1/√x_c,eff) and let the
carrier plus the correlated matter (the 2-halo term) carry the lensing at 0.5–3 Mpc.

**Pre-declared hypothesis (from the coordinating review, written into `XR9_kids_flagship.py` before any scan cell ran).**
Some threshold above the switch-only KiDS cap passes KiDS with the carrier. At that threshold, the LG's R₀ and the
cluster-infall EFE slope both move into their bands. The door fails if KiDS needs the private phantom out to ≳ 1.5 Mpc even
with the carrier.

**Answer: the door does not open.** No cell passes all seven gates. H fails at its first step:
- **The carrier barely moves the KiDS cap.** With the carrier's lensing it goes from 4.347 to **4.42** (x_c0 ≤ 3.40 at p = 1,
  ≤ 2.99 at p = 1.5).
- **KiDS still needs the phantom out to 1.5–1.6 Mpc** (the fitted lenses' f = 0 radius at the passing cells and at the cap), so
  the door's failure condition is met. The switch-only fit already needed about this reach; the carrier does not relax it.
- **What the door does fix.** The LG moves into its band, but only at x_c0 = 7–14 (p = 1) or 5–14 (p = 1.5), which is disjoint
  from KiDS.
- **What it cannot fix.** The two EFE samples and the Coma UDGs pass at no cell. Shrinking the regions turns the EFE into a
  step, and the dwarfs get worse as the regions shrink.

## Built in before scoring

- **The cap is MS5's κ form** (61a3a0858, the coordinating review's correction): U = C·min(∇²Φ_X, v_cap² κ_X²), with
  κ_X = 1/r for any spherical profile. Every spherical region therefore stops at ℓ_cap(z) = v_cap/(H√x_c,eff), which shrinks
  with the threshold.
  - The withdrawn local form (threshold × max(1, v_loc²/v_cap²)) appears **only** in the controls that reproduce DE10 and
    XR6, and is labelled there.
  - For a member galaxy beyond its host's cap, κ is read two ways, and a pass must hold under both:
    - **'galaxy'**: its own 1/s, out to ℓ_cap.
    - **'two-field'**: the exact curvature of its radial field plus the host's field (derivation in `galaxy_region_k`).
      Toward the host κ = g_g/(s|g_g − g_h|); across the host's field κ → g_g³/(s|F|³).
- **The KiDS owner's five rules:**
  1. The carrier amplitude fs = 1 in every gated score. Fitted amplitudes are labelled diagnostics.
  2. The 2-halo amplitude A ≤ 2 is gated, with A per bin reported. A ≤ 20 is shown beside it.
  3. The carrier halos are re-run with each cell's refitted lens masses. This is L390's recipe on the scored switch: 28
     shell-model halos, DE10's seeds.
  4. The flagship caps the threshold, and cells above it are marked failing.
  5. The forest passes by monotonicity from DE11 (worst 0.0041 at the converged cell; every scan cell's x_c,eff(z) is at or
     above that cell's at every z).

## The gate table (`XR9_gate_table.out`)

w = 0.25; both kicks (600/650 km s⁻¹) and both footings inside every entry. KiDS gives the worse Δχ² (≤ +4 passes); the
LG the dex range of the model's own 'decay' carrier history (band ±0.10); the EFE and UDG columns the σ range over all
variants; shear R_min–R_max with the cap.

| cell | x_c,eff(0.25) | KiDS | flagship | LG | EFE clusters | EFE dwarfs | UDGs | shear | RC |
|---|---|---|---|---|---|---|---|---|---|
| p1 x2.5 | 3.25 | **−29.0** | pass | +0.18…+0.24 | 2.2–6.3 | 3.9–4.5 | 4.2–4.3 | **0.90–1.12** | 17.2 |
| p1 x3.5 | 4.55 | +14.6 | pass | +0.14…+0.20 | 2.1–6.9, NF | 3.9–4.5 | 4.2–4.3 | **0.82–0.99** | 14.5 |
| p1 x5 | 6.50 | +60.4 | pass | +0.08…+0.15 | 1.9–6.5, NF | 3.9–4.5 | 3.6–4.6 | 0.74–0.98 | 12.1 |
| p1 x7 | 9.09 | +107 | pass | **+0.03…+0.09** | 1.7–6.5, NF | 3.9–4.5 | 3.7–5.2 | 0.67–0.98 | 10.2 |
| p1 x10 | 13.0 | +140 | pass | **−0.04…+0.02** | 1.4–6.8, NF | 3.9–4.5 | 2.7–5.2 | 0.64–0.98 | 8.5 |
| p1 x14 | 18.2 | +161 | fails (1e11.5) | **−0.10…−0.04** | 1.3–6.8, NF | 3.9–4.5 | 2.8–5.5 | 0.61–0.98 | 7.2 |
| p1 x20 | 26.0 | +211 | fails (1e11.5) | −0.17…−0.11 | 1.0–6.9, NF | 3.9–4.5 | 2.1–5.3 | 0.60–0.98 | 6.0 |
| p1.5 x2.5 | 3.70 | **−13.0** | pass | +0.16…+0.22 | 2.2–6.4 | 3.9–4.5 | 4.2–4.3 | **0.83–0.99** | 17.2 |
| p1.5 x5 | 7.40 | +88.9 | fails (1e11.5) | **+0.07…+0.13** | 1.9–6.5, NF | 3.9–4.5 | 3.6–4.6 | 0.68–0.98 | 12.1 |
| p1.5 x10 | 14.8 | +139 | fails (≥1e11) | **−0.04…+0.02** | 1.4–6.8, NF | 3.9–4.5 | 2.7–5.2 | 0.62–0.98 | 8.5 |
| p1.5 x20 | 29.6 | +233 | fails (all) | −0.17…−0.11 | 1.0–6.9, NF | 3.9–4.5 | 2.1–5.3 | 0.60–0.98 | 6.0 |

Bold marks a pass. NF means new failures under the two-field reading. The rows p1.5 x3.5, x7 and x14 are in the `.out`.
- RC (the last column) passes at every cell: min r_full/R_last ≥ 6.0 over all 175 SPARC galaxies.
- The forest passes at every cell by monotonicity.

**Passing sets.**

| Gate | Passes at |
|---|---|
| KiDS | p1 x2.5, p1.5 x2.5 |
| flagship | p1 x2.5–x10, p1.5 x2.5 |
| LG | p1 x7–x14, p1.5 x5–x14 |
| shear (two-sided) | p1 x2.5–x3.5, p1.5 x2.5 |
| RC, forest | every cell |
| EFE clusters, EFE dwarfs, UDGs | **none** |

Disjoint pairs: **KiDS × LG** and **shear × LG**.

## Gate by gate (`XR9_kids_flagship.out`, `XR9_cosmic_shear.out`, `XR9_environment.out`)

**KiDS: the carrier cannot replace the phantom beyond ~1 Mpc.** The rows below are p = 1, fs = 1, A ≤ 2, w = 0.25.

| x_c0 | x_c,eff(0.25) | With the carrier (canonical/alt) | Switch alone | Lens regions |
|---|---|---|---|---|
| 2.5 | 3.25 | −32.2/−29.3 (DE10: −32.3/−29.3, L390's masses) | −24.6/−20.7 | fully on to ≤ 1.28 Mpc, f = 0 at ≤ 1.62 |
| 3.5 | 4.55 | +9.6/+14.6 | +14.6/+16.4 | fully on to ≤ 1.21 Mpc |
| 5 | 6.50 | +57/+60 | +65/+70 | — |
| 20 | 26.0 | +210 | — | — |

- The carrier is worth 1.7–44 in Δχ² across the cells, not the ~100+ the missing phantom costs.
- The 2-halo amplitude stays bias-like: A ≤ 1.9 up to x_c,eff(0.25) = 6.5, and it saturates at 2.0 only from 7.4. Freeing it
  to A ≤ 20 changes no verdict.
- **Diagnostic, unphysical above 1:** with fs up to 3 (three times the halo's own carrier), x_c0 = 3.5 still fails on the alt
  footing (+0.3/+6.5), and x_c0 = 5 gives +52/+53.
- **The cap itself,** bisected with the carrier: x_c,eff(0.25) ≤ **4.4209** (4.4196 with the other cell's halos), against
  4.3473 switch-only.

**Flagship.** The smooth-gate cap with the κ cap in x_c,eff(2.5) is:

| M_b | canonical / alt | Largest x_c0, p = 1 | Largest x_c0, p = 1.5 |
|---|---|---|---|
| 1e10 | 1060 / 1403 | 75 | 19.9 |
| 1e10.5 | 591 / 783 | 42 | 11.1 |
| 1e11 | 329 / 436 | 23.3 | 6.19 |
| 1e11.5 | 184 / 244 | **13.0** | **3.46** |

The heaviest galaxies lose r_F first, as expected.

**LG.** R₀ with the model's carrier history (M_b = 1.145e11 and 1.72e11), canonical/alt, in Mpc:

| cell | R₀ (Mpc) | Band 0.76–1.21 |
|---|---|---|
| p1 x7 | 1.02/1.07 and 1.13/1.18 | in |
| p1 x10 | 0.88/0.92 and 0.97/1.02 | in |
| p1 x14 | 0.76/0.79 and 0.84/0.88 | in (the 1.72e11 mass only; 1.145e11 is −0.104 dex canonical) |
| p1 x20 | 0.65–0.75 | below |

- The κ cap does not bind on the LG: R₀ = 1.413/1.481 at the converged cell, identical to the withdrawn form.
- With a constant threshold (p = 0) the band is met only at x_c ≈ 10. From x_c = 40 on, R₀ = 0.60, the Newtonian
  baryons-plus-carrier floor.

**Cosmic shear: smaller regions help the upper side and uncover the lower side.**
- With the cap, the worst R falls from 1.12 to 0.98.
- Without any cap, shear passes from p1 x14 and p1.5 x10, where the cap is no longer needed.
- But **the minimum R(k) falls from 0.90 to 0.60**. The kicked carrier removes small-scale power, and at the converged cell
  the phantom masks it.
- Two readings of the gate:
  - **"Within 20%" (0.8 ≤ R ≤ 1.2).** This is how MS3 states it and how the table gates. It holds only at x_c0 ≤ 3.5 (p = 1)
    and 2.5 (p = 1.5).
  - **MS3/MS4's code checks only R ≤ 1.2.** On that rule every capped cell passes.

**EFE, cluster-infall BTFR (N = 314): the step.**
- **Members inside the host region** fall from 92% ('galaxy') / 51% ('two-field') at x_c0 = 2.5 to 19% / 7% at x_c0 = 20.
- **The slope does not reach 2σ at any cell:**
  - scalar-sum form: 1.0–3.46σ, and its worst variant stays at 3.36σ or more at every cell;
  - subtract form: 1.9–6.9σ.
- **The zero point** does improve, to ≤ 1.1σ at x_c0 = 20.
- **Members kept inside the host region keep the deficit and the rest lose it**, so the predicted slope stays steep.
- **The two-field reading adds new failures from x_c0 = 3.5 on**: 12 member-variants there, 232 at x_c0 = 20. These are members
  beyond their host's cap whose own region no longer covers R_HI across the host's field.
- **Even at x_c0 = 300** (1% inside) the slope is 0.46–3.37σ, with 452 new failures (diagnostic).
- **At the converged cell** the κ form gives edges of 2.88–3.01 Mpc and 2.2–6.3σ; XR6's withdrawn form gave 3.53–3.73 Mpc and
  2.18–6.63σ.

**EFE, Local Volume dwarfs (N = 92): not fixable by shrinking regions.**
- **Statistic C stays at 3.87–4.48σ at every cell.** The satellites that carry it sit within ~0.3 Mpc of the MW and M31 and
  stay inside their hosts' regions: 83–92 of the 92 are inside.
- **It worsens as the regions shrink:** 4.64σ at x_c,eff(0) = 200 (MW edge 173 kpc) and 6.21σ at 1000 (78 kpc), which is the
  step again.
- **The data point the other way:** the observed statistic is +0.080 ± 0.047, against the EFE's −0.10. Even no EFE at all would
  sit 1.7σ away.

**Coma UDGs.**
- **'Galaxy' reading:** the offset falls from +0.98 to +0.58 dex as Coma's edge shrinks from 2.99 to 1.06 Mpc (4.35σ → 2.13σ).
  Beyond x_c0 ≈ 40 every UDG sits outside Coma's region and scores as isolated: +0.40 dex, 1.6–2.1σ (diagnostic).
- **'Two-field' reading:** UDGs beyond the edge lose their own region at r_1/2 across Coma's strong field and turn
  Newtonian, up to 8 of 11 at x_c0 = 20, reaching +1.36 dex. A pass needs both readings, so the UDGs pass nowhere.

**Rotation curves.** Every SPARC galaxy's fully-on radius stays ≥ 6 R_last up to x_c0 = 20. The RAR is untouched throughout;
the tightest is UGC 9133 (R_last 108 kpc).

## The pinch, and what it says

The three "isolated-looking" liabilities do not share one fix. Each wants a different region size:

| Liability | Wants | Threshold |
|---|---|---|
| LG | L\* regions of ~0.8–1.1 Mpc at z ≈ 0 | x_c0 ≈ 7–14 at p = 1 |
| KiDS lenses (the same kind of galaxy, at z = 0.25) | regions to ~1.5 Mpc | x_c,eff(0.25) ≤ 4.42 |
| Cluster members and Coma UDGs | their hosts' regions below their own distances (≲ 0.5–0.75 Mpc) | x_c0 ≳ 40 |
| Dwarfs | no host EFE at all at 50–300 kpc | none: no region size delivers it |

- **No rising gate reconciles KiDS and the LG.** Within the power law, the threshold would have to FALL with redshift, p ≈ −0.5
  to −1.8 depending on the LG cell. That switches MOND on more and more at high z, against the forest and the flagship.
  This is arithmetic on the scanned numbers, not a scanned cell.
- **What does work in the scan:**
  - the LG's band (p1 x7–x14);
  - cosmic shear's upper side, uncapped from x_c0 = 14;
  - the flagship to x_c0 = 10 (p = 1);
  - the RAR and the forest.
- **Among the gates the door was meant to open, KiDS binds first, and not as a switch-only artefact.** The carrier's lensing
  raises its cap by only 1.7%. The EFE samples and the UDGs fail at every cell regardless.

## Controls and mutations

| Script | Controls (all exact unless stated) | MUTATE |
|---|---|---|
| `XR9_carrier_halos.py` | the refit masses; 28/28 halos with n within 1% of N (no MUTATE: it only produces inputs) | — |
| `XR9_kids_flagship.py` (~30 s) | C0: L352's baseline χ². C1: DE10's full table and preferred amplitudes (withdrawn cap, L390 masses; 0e+00). C2: the halo masses equal the κ-form refit at 14/14 cells. C3: κ = withdrawn form at the converged cell. C4: MS2's F1 rows. C5: DE9's smooth flagship cap, 329.3633/436.1862. C6: DE9's switch-only KiDS cap, passing at 4.3473 and failing at 4.3477. | fs = 0: M1 fails, rc = 1; the switch-only cap 4.3473 is recovered and every cell above it fails KiDS |
| `XR9_cosmic_shear.py` (~3 min) | MS4's committed 1.0491/1.1243 (cap) and 2.7191/3.1809 (none), 0e+00 | no cap: S1 fails, rc = 1 |
| `XR9_environment.py` (~4 min) | withdrawn-form controls: XR6's 36-cell LG table and numerical R₀; XR6's cluster table (24 × 6 × 8 numbers) and classification; XR6's dwarf rows; XR6's Coma edges, offsets, floor and σ | threshold frozen: E1 fails, rc = 1 |
| `XR9_gate_table.py` | bookkeeping over the three results files | KiDS column from the fs = 0 run: T1 fails, rc = 1 |

**Recorded, not hidden.** The first development run of the environment lane read the 'two-field' κ as a step at g_g = g_h. It
flagged 234 member-variants as new failures at the converged cell, which prompted re-deriving the curvature. The step was
wrong: the curvature near a satellite falls as (g_g/g_h)³/s across the field. It was replaced before any number was used
(noted in the docstring).

## Scope

- Spherical and 1-D throughout, and every other part of XR6's scope. The LG is one point mass at its barycentre; at the
  highest thresholds the MW and M31 regions need not merge, and this is not modelled.
- The member-galaxy κ uses a two-field approximation, not a 3-D solve.
- The carrier comes from one accretion history (L375's fiducial). The KiDS 2-halo term is linear.
- The shear verdict depends on the one- versus two-sided reading wherever R_min < 0.8.
- The cap and the trigger still have no complete action.

## Files (only these)

| Stem | Script | Output | Results | MUTATE output | MUTATE results |
|---|---|---|---|---|---|
| `XR9_carrier_halos` | `.py` | `.out` (five chunked calls) | `_results.json` (the halo cache) | — | — |
| `XR9_kids_flagship` | `.py` | `.out` | `_results.json` | `_MUTATE.out` | `_results_MUTATE.json` |
| `XR9_cosmic_shear` | `.py` | `.out` | `_results.json` | `_MUTATE.out` | `_results_MUTATE.json` |
| `XR9_environment` | `.py` | `.out` | `_results.json` | `_MUTATE.out` | `_results_MUTATE.json` |
| `XR9_gate_table` | `.py` | `.out` | `_results.json` | `_MUTATE.out` | `_results_MUTATE.json` |

Plus this `XR9_README.md`.

Run from the repository root, in order:
1. `XR9_carrier_halos.py`, repeated until it reports all halos present;
2. `XR9_kids_flagship.py`, `XR9_cosmic_shear.py` and `XR9_environment.py`;
3. `XR9_gate_table.py`.

Add `MUTATE=1` to run the controls.
