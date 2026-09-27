# XR13 — the per-object door

Cross-thread review, 2026-09-26/27. Read-only on every other file. Four new scripts live in this folder. Each has
controls that reproduce committed numbers exactly and a MUTATE run that must fail. Both a0 footings are in every gate
(canonical 9.36e-11, alt 1.13e-10 m s⁻²). κ = ½ stays a declared input, the dark mass is still required, and no new
particle species is added.

**The door.** XR6 and XR9 found that the converged model M\* fails four environment tests: the cluster-infall BTFR, the
Local Volume dwarfs, the Coma UDGs and the Local Group's R₀. The data behave as if galaxies were isolated from their
environment. The door is a phenomenological rule; no action is attempted.
- **(1) Per-object regions.** Each bound baryonic object at galaxy scale is its own MOND region, partitioned from its
  neighbours at the watershed of the MOND-sector density. Its kernel reads only its own baryons (L361's screening).
- **(2) No region above v_cap.** A system with v_f = (G M_b a₀)^¼ > 325 km s⁻¹ has no MOND region. That means
  M_b > M_cap = 8.98e11 / 7.45e11 M☉ (canonical/alt): clusters and massive groups.

**The object rule, declared before scoring.**
- **R1.** An object is its own region iff its watershed basin reaches at least l_obj = 1 kpc toward its host. That extent
  is s\*, the distance from the object to the MOND-sector density saddle on the host axis. Both profiles are isolated
  baryons plus their own ν_mono phantom: a Hernquist host (MW 6e10, a = 3 kpc; M31 1.2e11, a = 6 kpc) and a Plummer object.
- **R2 (reported).** Star clusters are never objects.
- **R3 (stress test).** An object must also have r_h ≥ l_obj.

## Answer: two liabilities flip, one improves, one moves partway, and the door breaks five things M\* passed

| Gate | M\* | The door | Verdict |
|---|---|---|---|
| (a) EFE, cluster-infall BTFR slope (N = 314) | 2.2–6.3σ | **0.07–0.10σ**; zero point 1.31σ | **FLIPS** |
| (b) EFE, LV dwarfs C (N = 92; +0.080 ± 0.047) | 3.9–4.5σ | **1.41–1.42σ** at l_obj ≤ 1.5 kpc | **FLIPS**, but only for l_obj ≤ 1.5 kpc |
| (c) Coma UDGs | 4.2–4.3σ | 2.25 / 2.03σ (+0.40 / +0.36 dex) | improves; **does not flip** |
| (d) Local Group R₀ (decay history) | +0.18 to +0.24 dex | +0.14 to +0.20 dex | **partway; still fails** |
| MW–M31 timing at 0.78 Mpc (−110 km s⁻¹) | −142 to −200 km s⁻¹ (over-predicts; past-flyby escape) | −7 to +49 km s⁻¹ | **NEW FAILURE** |
| (e) KiDS-1000 | −32.2 / −29.3 | unchanged in the committed model | **unchanged; at risk for real lenses** |
| (f) Cosmic shear, halo model (0.8 ≤ R ≤ 1.2) | 0.90–1.12 | 0.66–0.98 | **BREAKS** (lower side; one-sided R ≤ 1.2 passes) |
| (g) X-COP (L388 retention, 575–650 km s⁻¹) | window at all four kicks | **no window** | **BREAKS** |
| (h) El Gordo | Δχ −0.58 to −0.12 | Δχ −0.07 to +0.11 | **ease lost** (back to ΛCDM's tension) |
| (h) Harvey | knife-edge | intact carrier β = 0.000; core-decayed up to +0.78 | depends on the carrier's shape |
| (i) Groups at 2e13 (hunt item 7) | pass at 575–650 | **fail at every kick**; a ×9–17 step at M_cap | **BREAKS** |
| RAR, RC100 | pass | SPARC max 2.7e11 < M_cap | unchanged |
| Gaia DR4 wide binaries | untouched | s\*(Sun) = 0.12 kpc < l_obj | unchanged |
| Hunt item 93, outer-halo globulars | M/L_V 0.76 needed | 0.68 under R1 (unchanged under R2) | worse under R1 |

Net (`XR13_gate_table.out`): **2 flips against 5 gates broken or newly failed**, plus a new declared constant that has a
window of a factor 2.

## Gate by gate

**(a) Cluster-infall BTFR (`XR13_door_environment.out`).**
- All 21 PSZ2 hosts hold ≥ 1.1e13 M☉ of baryons inside R500 (≥ 12 M_cap). Part (2) leaves none a region.
- Every member reads only its own baryons, so e = 0 and the scalar-sum and subtract forms coincide.
- Predicted slope +0.0003 against the observed +0.0033 ± 0.0304 (R_proj) and +0.0023 ± 0.0289 (1.3 R_proj): 0.07–0.10σ.
- Members minus field: +0.0001 predicted against −0.0119 ± 0.0092 observed, 1.31σ.
- No member's basin toward its nearest member neighbour is smaller than its R_HI (0/310; median s\*/R_HI = 14, from
  projected separations, a lower bound).

**(b) LV dwarfs.**
- Under R1 at 1 kpc all 92 are their own regions (smallest s\* 1.21 kpc: Segue 1).
- Predicted C = +0.014 against +0.080 ± 0.047: 1.41σ (x1/x1.5/x2 host baryons, both footings).
- **The result is set by l_obj.** C stays below 2σ only for l_obj ≤ 1.5 kpc. It reaches 2.2σ at 2 kpc, 2.8–2.95σ at 3 kpc
  and 4.2–5.5σ at 10 kpc, where the nearby ultra-faints fall back into their host's region and the EFE becomes a step
  again.
- The size rule R3 fails at every scale (2.2–4.6σ). The host scale lengths (×0.5, ×2) change nothing.

**(c) Coma UDGs.**
- Coma is 98 M_cap, so it has no region and every UDG is isolated MOND.
- The offset is +0.397 / +0.358 dex. The floor, recomputed on this arm, falls to 0.165 dex because the Coma mass-model and
  f_b entries vanish. That gives **2.25 / 2.03σ**.
- The Newtonian pull of Coma's smooth carrier inside r½, at the ret = 1 X-COP would then need, moves this to
  2.23 / 2.01σ.
- The discrepancy that remains is the isolated-MOND one: the UDGs need 2.5× more mass than their baryons' MOND gives.

**(d) The Local Group (`XR13_door_local_group.out`).**
- The model is XR6/XR9's shell model generalised to the MW and M31 as two point masses, MW:M31 = 1:2, cut at their
  watershed. The saddle is 0.47 d from the MW; the MW's basin is a nearly planar half-space, 43% of the sky.
- Reading T is the task's specification: each tracer feels one galaxy's phantom plus both galaxies' baryons and carriers.
- The pair history is the kinematic timing orbit: timing mass 4.83e12 M☉, maximum separation 1.04 Mpc.
- Each ray gets a solid-angle-mean R₀ over the 90% of the sky with |cos θ| ≤ 0.9.
- Result on the decay history: **+0.136 / +0.183 dex canonical, +0.156 / +0.202 alt** (M_b 1.145e11 / 1.72e11). XR9's M\*
  gives +0.176 / +0.221 and +0.196 / +0.241.

| Variant (decay) | dex from 0.96 |
|---|---|
| M\* as two points in one region | +0.171 to +0.237 (the geometry alone moves R₀ by −0.005) |
| Door, reading T, 1:2 | +0.136 to +0.202 |
| Door, reading T, 1:1 | +0.131 to +0.198 |
| Door, the door's own d(t) | +0.138 to +0.201 |
| Tracers in holes, D_f = 0.85 / 2/3 | +0.115 to +0.183 / +0.081 to +0.152 |
| Tracers fully screened (D_f = 0) | median 0.50–0.66 Mpc, below the band |

- The partition cuts each basin's MOND pull to √(M_i/M). But the galaxies sit 0.26 and 0.52 Mpc off the barycentre, and
  the tracers on each side are closer to their own galaxy. That restores most of the pull.
- **Reading P** is L361/L370's exact curl-free projection of f V, computed numerically. Its Gauss control holds to 0.5%.
  Across the bounded watershed it leaks about 0.36 of the MW's phantom onto M31 and 0.47 of M31's onto the MW at today's
  region sizes. It also makes each region lopsided: the negative-mass Gauss layer on the cut face repels its own galaxy.
- At the tracers today, P/T = 0.88–1.22 by direction. **Pre-declared P1 (P ≥ T everywhere) failed.** Its solid-angle
  effect on R₀ is +0.002 dex, so R₀ is the same under both readings.

**The MW–M31 timing (a failure M\* does not have in this form).**
- Two separate regions attract as real masses (L370's rule). Reading T gives Newtonian baryons plus carrier, and the pair
  at 0.78 Mpc recedes or barely falls: **−7 to +49 km s⁻¹**. That is ≥ 23σ from −109.3 ± 4.4.
- Reading P gives +5 to +17 km s⁻¹. The leak (attractive) and the self-push (repulsive) nearly cancel.
- Keeping only the attractive leak gives −70 to −99 km s⁻¹. That selection violates momentum conservation and is not a
  reading of the door.
- M\* over-predicts instead: −142 to −200 km s⁻¹ in the same scheme; item 13 gives −223 / −241. Its published escape is a
  past close encounter, which the door's weakly bound pair cannot have had.

**(e) KiDS (`XR13_door_cosmology.out`).**
- Every fitted lens bin is at or below 10^11.1 M☉, below M_cap, and the lenses are isolated. The door changes no input of
  XR9's −32.24 / −29.27 (DE10: −32.3 / −29.3).
- **The risk the committed model has no room for.** Rule (1)'s watershed gives every satellite a basin: a cone behind it,
  60° half-angle for the LMC and 4–29° for the dSphs.
- For the Milky Way's 67 catalogued satellites, the union over their real Galactocentric directions covers 0.21 / 0.35 /
  0.34 / 0.27 of the host's sky at 50 / 100 / 200 / 500 kpc. Without the Magellanic Clouds it covers 0.10–0.19.
- A lens's phantom flux through a sphere drops by that fraction. "KiDS unchanged" holds only for lenses without
  satellites; a satellite-population re-score is needed.

**(f) Cosmic shear.**
- Halos lose their phantom above M = 10^13.19 / 10^13.13 M☉.
- R(k) falls from 0.90–1.12 (M\*) to 0.66–0.98. The upper side passes. The kicked carrier's small-scale deficit, which the
  cluster phantoms masked, now shows: R = 0.66 at k = 1 h/Mpc.
- Giving those halos their central galaxy's own phantom lifts the minimum only to 0.68–0.70.

**(g) X-COP.**
- Without the phantom, the two-sided 20% rule needs a retained carrier of 0.868–1.405. M\* needs 0.286–0.768. The C2
  control reproduces L354's rows and bounds exactly.
- Every X-COP cluster has M(<1 Mpc/h) = 5.0–8.7e14, so all fall in L388's top bin.
- L388 retains 0.37–0.61 (pooled, ≥ 1e14) and 0.79–0.85 (top bin) at 575–650 km s⁻¹. **No kick passes.**
- The top bin would reach 0.868 near 546 km s⁻¹. That is a linear extrapolation below L388's range, not a run.

**(h) Mergers.** L370's kernel-off run (ν = 1, real mass = lensing mass) is exactly the door's cluster physics.
- El Gordo: Δχ goes from −0.58…−0.12 to −0.07…+0.11. The phantom's ease is gone and ΛCDM's tension is back.
- Harvey: β_excess = 0.000 with an intact carrier, +0.001–0.018 depleted uniformly to 0.55.
- A core-decayed carrier fails harder than with the phantom: up to +0.78 at 100 kpc apertures.

**(i) Groups (item 7's 20 Lovisari groups).**
- Every group is above M_cap. The door supplies 0.09–0.34 of M500 without the carrier; M\* supplies 0.66–0.79.
- The carrier needed is 0.78–1.08 of the ΛCDM-like halo. M\* needs 0.24–0.40, and L388's lowest bin holds 0.17–0.34.
- With L388's retention the door's median group reaches 0.40–0.66 of M_HSE. **It fails at every kick**, while M\* passes
  at every kick.
- Part (2) also puts a step at M_cap. A system just above M_cap keeps its baryons only, while one just below keeps full
  MOND: a factor ν = 9–17 in non-carrier mass at 300–500 kpc. Hunt item 55 found η flat from 5e12 to 1.6e15.
- Dropping part (2) would not save the clusters. Under rule (1) alone, members' basins carve 0.99 of a rich cluster's sky
  and 0.86 of a group's.

## The object rule costs a window, a type rule and a constant

- **Window.** l_obj must exceed the s\* of solar-neighbourhood structure: Sun 0.12, wide binary 0.14, open cluster 0.54 kpc.
  These are upper bounds, since a spherical Milky Way under-states the disc's gradient. It must stay below the dwarfs'
  smallest s\* (1.08–1.21 kpc) for (b). **So 0.55 < l_obj < 1.1 kpc, a factor of 2.**
- **Globulars.** At l_obj = 1 kpc, R1 also separates **52 of Baumgardt's 157 Milky Way globulars**, 29 of them inside
  R_GC = 20 kpc (ω Cen, M13, M92, M56, NGC 362 at s\* ≈ 1.0–1.1 kpc; upper bounds).
- It separates all four item-93 outer-halo clusters. Losing the Milky Way's EFE takes their joint M/L_V from 0.76 to 0.68
  (0.71 to 0.64 alt), further below the stellar-population floor of 1.3.
- Keeping every globular in the Galaxy needs l_obj > 12.8 kpc, where (b) fails at 4.5–5.0σ.
- **A pure scale therefore cannot separate dwarf galaxies from globular clusters.** The door needs the type rule R2: it
  has to be told what a galaxy is.

## The door's cost, plainly

- **Two new declared inputs.** The object scale l_obj, with a working window of a factor 2, and a type rule (R2). v_cap
  becomes an existence threshold for regions, with a step at M_cap that the group data do not show.
- **No action.** The partition, the "object" and part (2) are declared. The door has three gaps:
  - Its w must not cross a watershed, which L361's single screened field cannot do between adjacent active regions.
  - Its prescribed partition does not conserve momentum. Each region's projected field pushes the pair's centre of mass.
  - The partition geometry decides between readings T and P, which differ for the timing.
- **It breaks** X-COP, the groups, cosmic shear's lower side and the MW–M31 timing, and it loses El Gordo's ease. The
  cluster costs come from rule (1)'s watershed itself, not only from part (2).
- **It leaves open** the Coma UDGs (2.0–2.25σ) and the Local Group (+0.14 to +0.20 dex), and it puts KiDS at risk for
  lenses with satellites.

## Controls and mutations

| Script | Controls (all exact unless stated) | MUTATE (regions merged) |
|---|---|---|
| `XR13_door_environment.py` (~10 s) | C1: XR9's full κ-form cluster table at the cell. C2: dwarf rows. C3: UDG rows, floor, edges (all 0e+00). C4: item 93's joint M/L 0.756 ± 0.154 / 0.705 ± 0.143 | D1–D3 fail, rc = 1; the scored numbers are XR9's (2.23–6.28σ, 3.87–4.48σ, 4.20–4.35σ) |
| `XR13_door_local_group.py` (~3.5 min) | C1: XR9's merged R₀ (0e+00). C2: two-region integrator in merged mode (6.7e-16). C2b: two-region root-finder (1e-12). C3: item 13's −222.5 / −241.5. W1: 0/200 basin mismatches against direct ascent. C5: Gauss 4.6e-3 | D4 fails, rc = 1 |
| `XR13_door_cosmology.py` (~12 s) | C1: MS4's 1.049101 / 1.124278 (0e+00). C2: L354's X-COP rows and L366's bounds 0.2863 / 0.7679 (0e+00). C3: item 7's η 1.80–2.11 / 1.54–1.81 | D5, D6 fail, rc = 1 |
| `XR13_gate_table.py` | bookkeeping over the three results files | T1 fails, rc = 1 |

## Recorded, not hidden

- **The first Local Group runs used XR6's `run_cells`.** It picks the last velocity sign change on a 24-point grid of
  starting radii. With two galaxies, tracers that start inside the pair's early extent have chaotic radial histories, and
  the grid locked onto inner crossings on several rays (R₀ down to 0.002 Mpc). This biased the first solid-angle means low,
  for example +0.107 against the final +0.136 dex on the canonical 1.145e11 decay cell; they are not used. The replacement
  is C2b's root-finder, checked against XR6 in the merged case.
- **Pre-declared P1 failed.** Reading T is not uniformly the door's best case for R₀ (P/T = 0.88–1.22). The net effect is
  +0.002 dex.
- **A development printout wrongly said the Magellanic Clouds were not in the dwarf census.** They are (LMC 3.5e9, SMC
  1.5e9 M☉ at Υ_V = 2). The committed output uses them and reports the union with and without them.
- **The pre-declared gate expectations are reported as they fell.** G3 (UDGs flip), G4 (LG flips), G5 (shear), G6
  (X-COP), G7 (groups) and T1P all failed.

## Scope

- Spherical or axisymmetric, 1-D shell dynamics along fixed rays, as XR6/XR9. Reading P's tables are built at today's
  separation and scaled with d. d(t) is prescribed.
- The member and UDG regions ignore neighbours that are not in the HI sample, for example the BCG.
- L388's retention was measured in boxes with the cluster phantoms on. The carrier feels only Newtonian φ, so the effect of
  removing them is second order and was not re-run.
- The group stellar masses come from an SHMR, and the BGG share (0.3–0.6) is declared.
- The satellite-basin estimate uses the Milky Way as its template lens.

## Files (only these)

| Stem | Script | Output | Results | MUTATE output | MUTATE results |
|---|---|---|---|---|---|
| `XR13_door_environment` | `.py` | `.out` | `_results.json` | `_MUTATE.out` | `_results_MUTATE.json` |
| `XR13_door_local_group` | `.py` | `.out` | `_results.json` | `_MUTATE.out` | `_results_MUTATE.json` |
| `XR13_door_cosmology` | `.py` | `.out` | `_results.json` | `_MUTATE.out` | `_results_MUTATE.json` |
| `XR13_gate_table` | `.py` | `.out` | `_results.json` | `_MUTATE.out` | `_results_MUTATE.json` |

Plus this `XR13_README.md`. Run from the repository root: the three lanes (any order), then `XR13_gate_table.py`. Add
`MUTATE=1` for the controls.
