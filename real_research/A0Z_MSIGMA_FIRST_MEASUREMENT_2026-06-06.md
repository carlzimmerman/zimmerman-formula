# The first a₀(z) from the density-selected M–σ method, on real data — a systematic-dominated null, with a sensible low-z half

*C. Zimmerman, 2026-06-06. Carl's idea (select deep-MOND galaxies by DENSITY, measure a₀ from the velocity dispersion)
built and run on 30 REAL published galaxies — the first time anyone has tried a₀(z) from the high-z pressure/rotation
M–σ relation. Honest outcome: the density selection works, the cleaner low-z half lands sensibly, but the a₀ extraction
is systematic-dominated by the 4th-power error amplification. A genuine first measurement and a clean null. Script:
`a0z_msigma_measurement.py`.*

## Method & data
- **Estimator:** deep-MOND `M_bar = V_e⁴/(G a₀)`, `V_e² = v_rot² + 3.4σ²` (KLASS asymmetric-drift form, unifies rotation
  + pressure) ⟹ `a₀ = V_e⁴/(G M_bar)`. `M_bar = M_*(1+f_gas)` (Tacconi gas, f_gas~0.8). **Density-select** `g_bar =
  G M_bar/R_e² < a₀_loc` to keep only genuinely deep-MOND systems.
- **Data (30 galaxies, real published kinematics):** de Graaff+2024 JADES (z~5.5–7.4, v_rot+σ+R_e measured); KLASS
  Girard/Mason 2020 (z~0.6–1.7, v_rot+σ; R_e from van der Wel size–mass); Saldana-Lopez+2025 (z~4–7.6, σ+R_e,
  dispersion-only). *(The agents corrected scrambled de Graaff values en route — now from the published PDF tables.)*

## Results

| subsample | N | a₀/a₀_loc (median) | reading |
|---|---|---|---|
| **z<2 (KLASS, AO-resolved)** | 9 | **0.9** | consistent with constant **and** framework; **disfavors** Verlinde (which needs ~2.4 at z=1.5) |
| z>3 (JADES/SL) | 3 | 14.9 | systematic-dominated (turbulence + thin-disk assumption + small N) |
| all deep-MOND | 12 | 1.4 (range **0.1–30**) | factor-~300 per-object scatter; trend p=+1.9 (spurious, ≈Verlinde) |

- **The density selection works** (Carl's reframe is sound): it correctly tags the deep-MOND low-mass tail (12 of 30) and
  rejects the high-acceleration massive disks (de Graaff's logM*~9 z>6 disks → g/a₀~2–4, Newtonian, correctly cut).
- **The dispersions are in the right ballpark** — `σ_obs/σ_deepMOND ≈ 0.8` for the selected objects, *not* a clean 10×
  turbulence offset. So the method is not dead on σ alone.
- **The cleaner low-z half lands sensibly:** at z~0.6–1.7 (KLASS, AO-resolved), the density-selected deep-MOND galaxies
  give **a₀ median 0.9× local** — the method *recovers roughly the right a₀ where the data are good*, and the value is
  consistent with flat/framework while inconsistent with a strong Verlinde rise. That is a genuine (if modest)
  validation of the method at z<2.

## The binding systematic (why it's a null overall)
The per-object a₀ scatters by a **factor ~300 (0.1 to 30× local)** — because `a₀ ∝ V_e⁴` amplifies *every* error to the
4th power:
- the **gas fraction** (M_bar ~ 5× M*, uncertain by ~2×) scales a₀ directly — the single largest term;
- the **rotation/pressure split** (V_e² = v_rot²+3.4σ²; the coefficient and the thin-disk assumption are uncertain at
  high z — de Graaff flag mergers inflating v_circ by ~0.15 dex);
- **turbulence** in σ (rises with z), which biases the z>3 points high and **fakes a rising trend** (p=+1.9 ≈ Verlinde)
  — the same artifact that contaminates every high-z kinematic a₀ test.

The median (1.4×) is consistent with **constant** within this scatter; the framework's 26% decline is far below the
noise. So the method **cannot yet decide framework-vs-flat** — but it *does* disfavor the steep Verlinde rise (the z<2
median is 0.9, not ~2), consistent with every other probe.

## Honest verdict
A real **first measurement** in a genuinely unoccupied niche, and a clean **systematic-dominated null**. Carl's
density-selection idea is the correct move (it works, and the low-z half validates), but the latch is the **4th-power
error amplification**: to turn this into a decisive a₀(z) test you need the V_e⁴ error budget controlled — **gas masses
to ≲0.1 dex, a clean rotation/pressure decomposition, and turbulence-subtracted σ** — none available now for logM*~8 at
z>2. The path is defined; the data precision is the wall.

**Net:** the new method joins the lensing-RAR door as a real, novel route that *sharpens the Verlinde exclusion now* (z<2
a₀~0.9, not rising) but *cannot reach the framework's distinctive decline* with present data. The framework remains
safe-but-untested; this is one more independent method confirming that standing — and the first to do it with
density-selected dispersions rather than resolved curves.

*Sources: de Graaff+2024 [2308.09742]; KLASS Girard/Mason 2020 [2006.14633]; Saldana-Lopez+2025 [2501.17145]; Tacconi
gas scaling [1702.01140]; van der Wel size–mass 2014; local deep-MOND M–σ coefficient [2605.26965].*
