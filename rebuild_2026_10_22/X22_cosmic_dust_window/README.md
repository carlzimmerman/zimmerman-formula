# X22_cosmic_dust_window: is there a scale, time or environment where a cold component clusters for the forest and σ₈, yet is absent from isolated galaxies?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (a2b532e3c6, committed alone first). Amendments A1–A3
(`AMENDMENTS.md`) are implementation or reported-only and change no line. κ = ½ FITTED. Footings 9.3603e-11 /
1.1312e-10 m/s², never pooled. The cold component is gravitating field mass, never a particle. No knob fitted. Not
"theory closed". Nothing here says the data favour the framework. Every number is from `x22_cosmic_dust_window.out` /
`_results.json`.

## Verdict: WINDOW ONLY WITH A NON-GRAVITATIONAL EXCLUSION (both footings)

**Gravity alone: NO WINDOW.** Any cold component that passes the forest falls into galaxies. That holds for a frozen
comoving cut and for a Jeans scale ∝ a^p at every p ≤ 0.5.

A window opens only if something other than gravity removes the cold component from galaxies. Two kinds pass the frozen
gates:
1. **Universal late heating.** The component must be cold through the forest epoch and hot today: c_s ≤ 6–13 km/s at
   z = 2–3, rising to c_s,need = **190 km/s (canonical) / 201 km/s (alt)** by z = 0, about twice V_last. That is
   Jeans power p ≥ 3 (c_s ∝ a^{2.5} or steeper).
2. **A collapse key.** An expulsion that switches on only where baryons are far above the cosmic mean of their epoch.
   The key is δ_b = ρ_b/ρ̄_b(z) with a threshold between 100 and 3.4e4, or equivalently the number of internal dynamical
   times N_orb. Its strength must be the same c_s,need.

**The record has no action for either.** X6 shows the khronon family has no free dust coupling, and a separate dust
double-counts. X19 step 2 finds no action-level selector. CFG944 Theorem G shows that local θ-keyed terms (the natural
collapse clock) carry a ghost or cannot be off in the linear universe.

## The numbers

**λ_forest (Step 1).** The cut family is L319's T² = [1 + (αk)^{2ν}]^{−10/ν}, ν = 1.12, graded with X4's forest rule.

| cut | k_c⁻¹ = α (Mpc/h) | k_hm (h/Mpc) | λ_hm (Mpc/h) | Lagrangian R_hm | M_hm (M☉) | class |
|---|---|---|---|---|---|---|
| α_PASS (strict line; = 5.3 keV WDM) | 0.00753 | 59.9 | 0.105 | 52.5 kpc/h | 7.81e7 | PASS |
| α_NF (largest not FAIL; verdict-bearing) | 0.02991 | 15.08 | **0.417** | 208 kpc/h | **4.89e9** | UNDECIDED at the edge |

- The lines bound α at: strict ≤ 0.00753; L346 band top ≤ 0.0545; loose (T²(k5) ≥ 0.9) ≤ 0.0299; worst bin 0.5 ≤ 0.0914
  Mpc/h. The pincer's loose yardstick alone allows ≤ 0.0325.
- The line itself asks for dust-like power down to λ_line = 2π/k5 = 1.36 Mpc/h.

**R_gal and the galaxy tolerance (Step 2).**

SPARC R_last (min / 16 / 50 / 84 / max) is 0.71 / 4.96 / 11.27 / 35.57 / 108.31 kpc.

| | canonical | alt |
|---|---|---|
| f_max: largest fraction of the D-F fair share that passes X6's d2 line on this footing | **0.196** | **0.0269** |
| f_max from the rms line alone | 1.0 | 1.0 |
| tolerated M_c(<R_last)/M_b, median (16–84 %) | 0.035 (0.024–0.052) | 0.0049 (0.0033–0.0074) |
| Lagrangian M_L = (Ω_m/Ω_b)M_b, min / 50 % / max | 3.0e8 / 4.67e10 / 3.8e12 M☉ | 2.9e8 / 4.67e10 / 3.4e12 M☉ |
| Lagrangian R_L, min / 50 % / max (Mpc/h) | 0.082 / 0.442 / 1.91 | 0.082 / 0.442 / 1.85 |
| hydrostatic c_s,need (isothermal, flat well) | 190.0 km/s (median 1.91 V_last) | 201.3 km/s (2.02 V_last) |
| content left by gravitational virial heating (c_s = V/√2), as a fraction of the fair share inside R_last (median) | 0.541 | 0.541 |

- The alt f_max is small because the law's own median Υ (0.44) already sits on the alt Υ edge.
- **The RAR rms alone tolerates the full fair share** (f_max = 1 on both footings). The exclusion rests on the
  stellar-population Υ window, as X6 found.

**Step 3A, frozen comoving cut (gravity only).**
- At α_NF the captured fraction T²(k_L) has median 0.76. X6's d2 line then fails on both footings (median Υ 0.43
  canonical, 0.37 alt).
- Reaching f_max needs k_excl = 16.3 / 24.5 h/Mpc, i.e. M_excl = 3.9e9 / 1.1e9 M☉. Only 13.7 % / 5.7 % of SPARC
  galaxies lie below that. The median galaxy is 12 / 41 times heavier.
- Those few suppressed galaxies, sitting inside an M_excl structure, would still collect 1.0–5.5 times their fair share
  inside R_last by infall (reported).
- At α_PASS no SPARC galaxy lies below M_excl; the median gap is 755 / 2570 in mass.
- **The gap (A3, reported).** SPARC M_L/M_hm has median 9.5 at α_NF and 598 at α_PASS. R_L/R_hm has median 2.1 and 8.4.
  So the forest demands dust-like clustering on the galaxies' own Lagrangian scales.

**Step 3B, Jeans scale λ_J ∝ a^p, with c_s(z = 0) = c_s,need.**

The table shows canonical values; alt is the same in class.

| p | c_s at z = 3 / 2 (km/s) | forest | R_σ₈ | T²(z = 0) at k = 1 / 10 h/Mpc | window |
|---|---|---|---|---|---|
| −0.5 (adiabatic) | 760 / 570 | FAIL | 0.031 | 0.000 / 0.000 | no |
| 0 (frozen comoving) | 380 / 329 | FAIL | 0.568 | 0.000 / 0.000 | no |
| 0.5 (constant c_s) | 190 / 190 | FAIL | 0.911 | 0.009 / 0.000 | no |
| 1 / 1.5 / 2 | 95 / 47.5 / 23.8 at z = 3 | FAIL | 0.966 / 0.983 / 0.990 | — | no |
| 3 | 5.94 / 12.2 | UNDECIDED (T²(k5) 0.998 / 0.989) | 0.995 | 0.822 / 0.050 | yes (late heating) |
| 4 / 6 / 8 | ≤ 1.48 / ≤ 4.06 | PASS | 0.997–0.999 | 0.897–0.974 / 0.005–0.031 | yes (late heating) |

- The 4 km/s pincer control gives T²(k = 10, z = 3) = 0.941 here (reported).

**Step 3C, environment keys.** C is the cosmic medium (the background for z ≤ 1100 plus forest absorbers); S is SPARC.

| key | C | S (16–84 %) | separates |
|---|---|---|---|
| ρ_b (M☉/pc³) | 6.1e-9 – 8.19 | 2.1e-4 – 3.8e-3 | **no**: the background passes through S at z = 31–85 |
| x = g_N/a₀ | 0 – 15.6 | 0.025 – 0.24 (canonical) | no |
| ρ_env | 3.9e-8 – 51.8 | 3.9e-8 | no |
| H (hosted) | 0 | 0 – 1 | no |
| e, kT | separate only by catalogue convention (no weight) | | see the note below |
| N_orb (computed for the cosmic medium) | 0.023 – 0.75 | 9.3 – 35 | **yes** |
| δ_b = ρ_b/ρ̄_b(z) | 0 – 100 (forest PROVISIONAL 0.1–10) | 3.4e4 – 6.2e5 | **yes**, gap ×339–345 |

- **The ρ_b key, graded.** c_s,need switched on while the background is above S's lower edge (z ≥ 31.5) makes the
  forest FAIL: T²(k5, z = 3) = 0.001 (canonical) / 0.0004 (alt), with R_σ₈ = 0.994. This is Part F of the pincer,
  carried over to baryon density.
- **The e convention is not physical.** The record-method rms linear peculiar gravity at z = 2–3 is 0.041–0.055 a₀. That
  lies inside SPARC's e range of 0.034–0.060, so at the forest epoch the cosmic medium sits in the same external field
  as SPARC galaxies today.
- **Side effects of a δ_b key (reported).** Every separating threshold also empties the hosted dwarf classes that need
  extra mass (MW ultra-faints, bright M31, M31 others). Clusters T1–T3 (δ_b 254–6e3) and groups depend on where the
  threshold sits.

## Checks

- **Main run: 10/10 PASS, exit 0** (S0-1…S0-5, C1–C5). 10 s, 0.10 GB, one thread.
  - Step 0 reproduces exactly: L346 bands (0 deviation), L319 T²_5.3keV = 0.9951884883, X6's law rms 0.054087 /
    0.053718 and U 0.52 / 0.44, f_d,max 0.0269184113, NGC 3198 0.145239 / 0.142154 dex, and X19's background band.
  - C2: the ODE equals the ΛCDM growth integral to 1.3e-8.
- **MUTATE (`X22_MUTATE=1`): exit 1.** Exactly the required checks fail: S0-1, S0-2, S0-3, S0-4, S0-5, C2 and C4. C1, C3
  and C5 pass. Its verdict line (UNDECIDED) is the control's output.

## Physical reading

**The galaxies are made of the forest's scales.** The forest needs dust-like growth to a half-mode no larger than
0.42 Mpc/h (5e9 M☉ Lagrangian). The median SPARC galaxy assembled from a region 0.44 Mpc/h in Lagrangian radius,
about 2 times R_hm. A cut that spares the forest leaves most galaxies' own collapse scale untouched.

**Gravity offers no escape.** A component cold enough for the forest has velocities far below V. It falls into any well
it collapsed with, and suppressed dwarfs re-acquire it by infall. Gravitational shock heating (c_s ≈ V/√2) still leaves
about 54 % of the fair share inside R_last.

**What an exclusion mechanism would need:**
- energy put into the cold component after z ≈ 2, to c_s ≈ 2V (about 190–200 km/s);
- either everywhere (late heating, p ≥ 3), or only where δ_b ≳ 10²–10⁴ (a collapse key);
- not keyed on density, acceleration or environment, which the early or linear universe also reaches;
- and it would have to come with an action. The record has none, and CFG944 blocks the local θ-clock route.

Late heating would leave power suppression at low z that is not graded here: T²(z = 0, k = 1) = 0.80–0.97 (both footings). Its
c_s,need also lies below the cluster dispersions in X19's table (450–630 km/s), so the hot component would stay bound in
clusters, T1 included.

The galaxy side itself rests on the Υ window: the RAR rms alone would tolerate the full fair share.

## What this does not show

- It is linear only: no N-body, no flux power. The forest gate is the record's linear proxy (X4).
- The captured fraction T²(k_L) and the hydrostatic profile are estimators, both chosen in the window-favourable
  direction.
- The forest δ_b range is PROVISIONAL (from memory). The verdict uses the loose bound 100.
- No exclusion action is written or tested. Clusters, hosted dwarfs and low-z lensing under late heating are not graded.

## Files and commits

| commit | content |
|---|---|
| a2b532e3c6 | `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md` (alone, before any script or number) |
| 5c7114f508 | `x22_cosmic_dust_window.py`, `.out` / `_results.json` (main and MUTATE), `AMENDMENTS.md` |
| (this commit) | README |

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X22_cosmic_dust_window/x22_cosmic_dust_window.py               # exit 0
PYTHONHASHSEED=0 X22_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X22_cosmic_dust_window/x22_cosmic_dust_window.py  # exit 1 by design
```
