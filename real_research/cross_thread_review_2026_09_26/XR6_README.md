# XR6 — the converged candidate against the three galaxy-environment liabilities

Cross-thread review, 2026-09-26 (late evening). Read-only on every other file: two new scripts in this folder, each with
controls that reproduce the committed numbers exactly and a MUTATE run that must fail. Both a0 footings throughout
(canonical 9.36e-11, alt 1.13e-10 m s⁻²). κ = ½ stays a declared input; the dark mass is still required; no new
particle species.

**Question.** The candidate the threads converged on is the C-H/K branch with ν_mono and L361's region kernel, the
MOND-sector switch, the linear gate (p = 1, x_c0 = 2.5), MS3's local cap (v_cap = 325 km/s) and a density-triggered
carrier. Does it change any of three liabilities that no thread owns?
1. The 09-03 external-field (EFE) samples.
2. The Local Group zero-velocity radius.
3. The Coma ultra-diffuse galaxies (UDGs).

**Answer.** None flips. Two get worse and two stay (the EFE samples are counted separately):

| Liability | Before (XR4 / L23) | Under the candidate | Verdict |
|---|---|---|---|
| EFE, cluster-infall BTFR slope (N = 314) | 2.4–2.9σ scalar-sum form, 3.5–4.1σ subtract form | 2.2–3.4σ scalar, **4.6–6.6σ subtract** | **worse** (subtract +0.9 to +2.3σ; scalar within −0.05…+0.4σ) |
| EFE, members − field zero point | 2.8–3.1σ | 0.0–2.2σ | weakened (below 2.2σ) |
| EFE, Local Volume dwarfs (N = 92) | 3.87–4.48σ | 3.87–4.48σ, identical | **stays** |
| EFE, both samples in quadrature | 4.5–6.6σ | 4.4–8.0σ | worse at the top end |
| LG zero-velocity radius (candidate cell) | +0.143…+0.219 dex | **+0.168…+0.245 dex** (1.41–1.69 Mpc vs 0.96) | **worse** by +0.025 dex |
| Coma UDGs (11) | +1.159 / +1.112 dex = 4.9 / 4.7σ | +0.982 / +0.949 dex = **4.35 / 4.20σ** | **stays** (weakened, but not by the cap) |

No new failure was found. Every cluster member beyond the cap keeps its own MOND region out to ≥ 3.9 R_HI, so none is
left Newtonian with its carrier cleared.

## The candidate as scored (every definition read from code)

- **Kernel.** ν_mono (`L340_filtered_khronon_completion.py:103-117`), equal to ν_RAR for y ≤ 2.337. It is region-local
  per `L361_bound_region_kernel.py:16-32`: w is sourced by f ρ_b and screened across the inactive web, 1/m ≤ 0.5 Mpc
  (L361 R4). Inside a region the EFE is QUMOND sourced by the in-region **baryons**, e_N = G M_b(<r)/r².
- **Switch.** L395's `msc` cell (`real_research/dark_sector_2026/L395_two_switch_branches.py:123-127`, uncommitted,
  read at 20:16):
  - x = 1.5 Ω_m(z)(ρ_b + max(ρ_ph,all, 0))/ρ̄_m (absolute, untruncated phantom of all baryons);
  - on where x ≥ x_c0 E^{2p} max(1, v_loc²/v_cap²), with v_loc² = |g_ms|²/(−∇·g_ms).
- **Equivalent form** (checked on 20000 random draws, K0):

  on ⟺ 4πGρ_ms ≥ max(x_c,eff H², √x_c,eff · H · |g_ms|/v_cap).

  In deep MOND v_loc² = v_f(r)²/(1 + s/2), where s = d ln M_b/d ln r. So every host above v_cap is capped at the **same**
  radius, r_cap = (1 + s/2) v_cap/(H √x_c,eff). That is MS3's 1.75 Mpc at z = 0.5 (reproduced, K5), and 3.5–3.7 Mpc for
  every PSZ2 cluster at z = 0.02–0.06 (`XR6_efe_udg_under_candidate.out:51,53`).

## 1. EFE — cluster-infall BTFR: the cap makes the slope worse

**Geometry** (`XR6_efe_udg_under_candidate.out:51-54`).
- The capped edge is 3.53–3.73 Mpc for all 21 clusters; v_loc at the edge is 822–1273 km/s.
- Of the 314 members, 188 sit inside their cluster's region, 14 have their own region merged with it, and **112 have
  their own region beyond it** (committed r = R_proj).
- With r = 1.3 R_proj, 189–190 are beyond; with the cluster's baryons truncated at r200, 176–239.

**Why it gets worse.** Under operator A, members beyond the cap are screened (L361 R1's Yukawa law, Dirichlet or
1/m = 0.2/0.5 Mpc), so they lose their EFE deficit. Members inside keep it. The EFE becomes a step at r_cap, so the
predicted contrast between low and high g_e grows while the mean offset shrinks.

**Numbers** (canonical, f_b(R500) = 0.13, committed geometry; `.out:61-64`):

| | scalar-sum slope | subtract slope | zero point |
|---|---|---|---|
| Uncapped (= XR4) | −0.0779 (2.66σ) | −0.1135 (3.83σ) | 2.94σ |
| Capped, Dirichlet | −0.0902 (3.07σ) | −0.1648 (5.52σ) | 1.66σ |
| Capped, 1/m = 0.5 | −0.0879 (3.00σ) | −0.1450 (4.87σ) | 2.04σ |

Observed slope: +0.0033 ± 0.0304.

**Over every operator-A variant** (f_b × form × gap × geometry × extent × footing; `.out:116-122`):
- Scalar-sum form: 2.18–3.37σ (uncapped 2.21–3.16).
- Subtract form: 4.56–6.63σ (uncapped 3.52–4.91).
- Zero point: 0.01–2.17σ (uncapped 0.65–3.08).
- **No variant moves toward the data by more than 0.05σ.**

Infalling groups beyond the cap would restore part of the EFE. That puts the truth between the uncapped and capped
rows, so the slope is no better in any case.

**Operator B** (the PM phantom L377/L395 actually runs; XR5 table row B) reads all baryons in ν's argument. It screens
nothing, so its EFE numbers are the uncapped ones. Beyond the cap, the action and the PM disagree on the EFE. L395's
scoring inherits B's EFE, not the action's.

## 1b. EFE — Local Volume dwarfs: unchanged

The cap cannot bind in the Local Group (`.out:136-139`):
- max v_loc in the MW/M31 deep-MOND zones is 287 km/s, even with host baryons ×2, against v_cap = 325;
- every dwarf is switched on (margin ≥ 1.35) inside its host's region (MW 1.57–1.96, M31 1.87–2.33 Mpc; none outside).

Statistic C is XR4's to 0e+00: 3.87 / 3.90σ with host baryons ×1, and 4.20–4.48σ with CGM.

## 2. Local Group zero-velocity radius: the reading moves the edge outward

Source: `XR6_lg_zero_velocity_mond_sector.out`.

**The cap.** v_f(LG) = 194–226 km/s < v_cap, so the cap does not bind in the LG's MOND zone (S1a: v_loc ≤ 264 km/s). It
acts only at z ≳ 6.7–7.0, inside the point mass's phantom-free Newtonian zone, and moves R₀ by 0 (S1b, `:39-41`).

**The reading.** XR4's edge subtracts the matter background (host in vacuum). The MOND-sector reading counts
baryons + phantom plus the ambient baryons: r_e = v_f/(H √(x_c,eff − 1.5 Ω_m f_b)) instead of v_f/(H √(x_c,eff + 1.5 Ω_m)).
- The edge is ×1.106 at z = 0 and ×1.005–1.118 over z = 0–5 (`:45`).
- At the candidate cell, M_b = 1.145e11, no carrier: R₀ = 1.413 / 1.480 Mpc (+0.168 / +0.188 dex), against XR4's
  1.334 / 1.398 (`:51,57`).
- Over M_b and carrier histories: +0.168 to +0.245 dex (`:64`). The shift is +0.025 dex everywhere (`:68`).
- MS2's contrast reading gives almost the same (1.402 Mpc).

**The pincer** (E1, `:73-76`). The uniform external Newtonian field in ν's argument that would bring R₀ to 0.96 is
1.98e-3 / 2.12e-3 a0. Compare it with what could supply it:

| Source | Field (a0) | R₀ (Mpc) |
|---|---|---|
| Most a KiDS-passing kernel transmits (L361 R3, 1/m = 0.5) | 1.0e-4 / 8.6e-5 | 1.29 / 1.34 |
| A merged neighbour group's baryons (k04's ≤ 1.03e11 M☉ at ≥ 3 Mpc) | ≤ 1.7e-5 | 1.38 / 1.45 |
| The web's baryonic field that operator B reads unscreened | 2.05e-3 / 1.70e-3 | **0.956 / 0.988** |

Only the third source is large enough, and that kernel fails KiDS by +233 (L361 R3). So the LG demands the very
external field that KiDS forbids, about 20× more than KiDS lets through.

## 3. Coma UDGs: inside the cap, still ~4.2–4.4σ

**Inside the cap.** Coma's capped edge is 3.71–4.37 Mpc across three mass models, three f_b and both footings. The
UDGs' farthest position is 2.34 Mpc (DF44, Einasto 3-D). All eleven feel the EFE (U1, `XR6_efe_udg_under_candidate.out:149-150`).

**What changes the amplitude is not the cap.** Under L361, ν reads Coma's **baryons** (e_N = f_b(r) g_true). L23 used
the closure-inverted total field, and the baryonic field is only 0.25–0.50 of it (`.out:151`). The results:
- **+0.982 / +0.949 dex = 4.35 / 4.20σ**, with the systematic floor recomputed on this arm (0.218 dex).
- Over f_b = 0.10–0.157 and both footings: 4.05–4.45σ.
- DF44 alone: +0.820 ± 0.139.
- The EFE term alone: +0.586 dex, 5.0σ (L23: +0.763, 6.0σ; `.out:157-166`).

**First infall.** A UDG at 9 Mpc lies beyond the cap and would be isolated: +0.396 dex, 1.8σ (L23's first-infall arm:
2.7σ). But falling from Coma's edge to the UDGs' radii takes ≥ 3.5–17.9 internal dynamical times at ≤ 3000 km/s
(`.out:172`), so they should have re-equilibrated. That is a hypothesis about the sample, not a repair.

**The carrier.** Coma's retained carrier (L388: up to 0.85) inside r_1/2 shifts the offset by 0.020 dex. That fails my
pre-declared 0.01 bound; it is 2% of the offset.

## Controls and mutations

| Script | Controls | Main run | MUTATE run |
|---|---|---|---|
| `XR6_efe_udg_under_candidate.py` (~9 s) | XR4's cluster and dwarf numbers reproduced to 0e+00 (C1, C2); L23's Coma numbers (+1.1595 / +1.1121, floor 0.2271, 4.93 / 4.73σ, DF44 +0.9377 ± 0.1389, 9 Mpc +0.6350; C3); ν_mono to 4.9e-9 and 0.01037 dex (K0); MS3's cap (K5) | 14/18; 0 load-bearing failures | no cap: every member back inside, the numbers equal XR4's, K1 and U3 fail, rc = 1 |
| `XR6_lg_zero_velocity_mond_sector.py` (~30 s) | All 204 XR4 cells and 19 mutation cells reproduced to 0e+00 (C2); k02's 1.929 / 2.021 and 1.176 (C1) | 9/11 | XR4's reading, no cap: reproduces XR4's +0.143…+0.219 dex, S2 fails, rc = 1 |

In the main runs, the failed checks are pre-declared hypotheses that are **reported, not hidden**:
- **V1:** the cap rescues the slope (it does not).
- **V2:** every variant gets worse (one is flat, ±0.05σ; V2b is written post-hoc and labelled so).
- **U2:** the UDGs flip (they do not).
- **U4:** the carrier shift stays under 0.01 dex (it is 0.020 dex).
- **S1c:** the closed form matches the numerical edge to 1% (it is 1.15% off at z = 5).
- **Z2:** the LG flips (it does not).

LG check S1, as first written, required the capped and uncapped edge tables to agree at all 97 epochs, and it failed.
The disagreement is the Newtonian-zone sliver at z ≳ 7. S1 was split into S1a–S1c, and the original is kept in the
docstring.

## Scope, and what would settle it

**Scope.**
- Spherical and 1-D throughout.
- The scalar-sum vs subtract ambiguity grows under the cap, because the subtract form's √e_N deficit at small e_N is
  exactly what the cap removes. A 3-D QUMOND disc-in-a-field factor would settle it (`hunt_2026/f16_curl_field_fork_on_discs.py:185`).
- Member 3-D radii use projected radii (lower bound) and 1.3 R_proj.
- XR4's f_b template beyond R500, extended or truncated at r200.
- A galaxy's own region comes from the scalar-sum 1-D form. It drops the 3-D positive EFE lobes, so it underestimates
  the region, which is conservative for the no-new-failure check.
- The switch uses GP0's cosmology, while the cluster geometry uses KC's H0 = 70.
- The cap and the trigger still have no action (MS3).

**What would settle it.**
- Clusters: the 3-D disc factor, per-cluster f_gas(r), caustic-based 3-D radii, and resolved HI kinematics.
- LG: a two-body or particle-mesh check with the MOND-sector switch.
- UDGs: the M/L and aperture systematics that dominate L23's floor.

## Files (only these)

- `XR6_efe_udg_under_candidate.py`, `.out`, `_MUTATE.out`, `_results.json`, `_results_MUTATE.json`
- `XR6_lg_zero_velocity_mond_sector.py`, `.out`, `_MUTATE.out`, `_results.json`, `_results_MUTATE.json`
- `XR6_README.md`

Run from the repository root with `python3 real_research/cross_thread_review_2026_09_26/XR6_<lane>.py`. Add `MUTATE=1`
for the control.
