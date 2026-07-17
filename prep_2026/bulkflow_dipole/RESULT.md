# Bulk flow + quasar dipole vs Sarkar's dark-energy critique

Framework under test: Carl Zimmerman's **de Sitter-Unruh MODIFIED-INERTIA** theory.
`a0 = cH_Lambda/Z = 9.36e-11` (canonical) / `1.13e-10` (alt total-rho footing);
`nu(y) = sqrt(1 + 1/y)`, `y = g_bar/a0`; inertia referred to the passive CMB/dS-Unruh frame.

Scripts (exit 0, both footings): `bulkflow.py`, `quasar_dipole.py`. Figure: `bulkflow_fig.png`.

---

## LANE A -- BULK FLOW (Qin et al. 2021, ApJ 922:59)

**Sarkar's anomaly:** CMB-frame convergence is not seen to >=200 h^-1 Mpc; measured bulk
flows sit **above** the LCDM linear-theory curve (data/LCDM ~ 1.6-2.9 over R=30-180 h^-1 Mpc).

**Pipeline.** (1) `V_LCDM(R)` from a BBKS-CDM P(k) (Sugiyama Gamma=0.166), sigma8=0.80
normalized, 3D bulk-flow variance `sigma_v^2(R)=(H0 f)^2/(2pi^2) INT P(k) W_th^2(kR) dk`.
Reproduces the Qin pink curve to ~20-30% (241 km/s @ R=30 -> 64 @ R=300).
(2) RMS **coherent** peculiar acceleration on the same P(k)/window via the field-level
Newtonian relation `g = (3 H0 Om / 2f) sigma_v` (g and v share the delta(k)/k weight).
(3) MI boost `B(R)=nu(g_pec(R)/a0)`, both footings. (4) Overlay on the labelled Qin points.

### Result -- the literal prescription OVERSHOOTS badly
On tens-of-Mpc scales the **coherent** peculiar field is tiny:
`g_pec(R) ~ 1.3e-13 .. 4.8e-13 m/s^2`, i.e. `g/a0 ~ 0.0014 .. 0.005` -- **deep-MOND**.
The framework `nu` there is **14-27** (both footings within ~10%), so
`V_MI = 1700-3400 km/s`, overshooting the CF4TF/W09 data by a **median ~10x (6-13x)**.
Higher-a0 alt footing makes the overshoot slightly worse (nu 15-30).

**This is a gross overshoot, and we report it as such.** Feeding the framework's *local*
inertia kernel the *coherent, R-smoothed* acceleration is the wrong quantity: a galaxy's
total acceleration (what MI actually modifies) is dominated by its local/virial
environment (>= a0 at halo outskirts, >> a0 inside), not by the ~a0/100 large-scale field.
The naive coherent-field boost therefore mis-scales the effect by an order of magnitude.

### What the data actually need
The mean `data/LCDM ~ 1.9`. A boost `nu ~ 1.9` corresponds to `g_bar ~ 0.4 a0 ~ 3.6e-11`
-- an **environmental/a0-scale** acceleration, NOT the coherent field. The
"environmental-a0 reading" band `nu(g ~ 0.5-2 a0) ~ 1.2-1.7` (orange band in the figure)
sits in the **right direction and right rough magnitude** to lift LCDM toward the data,
but slightly undershoots the ~1.9 the highest points want. So MI **plausibly helps** in
the sense Sarkar's anomaly requires (extra large-scale flow above LCDM) -- but only under
the environmental reading, and the effect is modest, not the 10x the literal estimator gives.

### HONEST QUASI-LINEAR FLAG
This is a `nu`-boost bracket, **not** a first-principles P(k)-of-MI. The framework's full
**linear cosmology is UNBUILT (an open door)**: there is no MI transfer function, no MI
growth `f`, and no self-consistent field-level `nu`-weighting. The two readings
(coherent-field 10x overshoot vs environmental modest lift) **bracket** the truth; only the
framework's own linear theory can pick the number. We do NOT claim MI explains the bulk flow.

### CREDIT
The "MOND/modified-dynamics enhances large-scale flows / growth" idea is **not novel**:
Nusser 2002 (astro-ph/0109016) on MOND peculiar velocities and growth; and the MOND
structure-formation / bulk-flow literature (Llinares, Angus, Katz N-body). The only
framework-specific content here is whether *its* `a0 + nu` gives the right **magnitude** --
and the literal quasi-linear estimator does not (overshoots), while the environmental
reading is in the right ballpark but under-specified.

---

## LANE B -- QUASAR DIPOLE (Secrest et al. 2021, ApJL 908:L51)

CatWISE 1.36M QSO: `D_obs ~ 1.54e-2`, direction CMB-consistent, amplitude ~2x
Ellis-Baldwin `D_EB = [2+x(1+alpha)]beta_cmb ~ 6.7e-3`. **Excess ~ 8.7e-3.**

Framework apex signature = a dynamical RAR/lensing anisotropy of fractional size
`(1/2) beta_cmb = 6.2e-4` (0.062%). It is **a0-INDEPENDENT** -> identical both footings.

- `D_frame / D_excess = 0.071` -> framework is **~14x too small**.
- Even if this anisotropy fed directly into a count-aberration dipole (it does **not** --
  different observable), it supplies only ~7% of the excess.

**VERDICT: framework-NEGLIGIBLE for the amplitude.** The genuine shared datum is the
**DIRECTION**: framework apex == CMB apex == QSO-dipole direction. The Secrest amplitude
excess is not a framework prediction, and the framework offers no count-anisotropy
mechanism that adds meaningfully to `D`.

---

## VERDICTS (straight, both footings)

- **LANE A: NEEDS-LINEAR-THEORY** (with a **MI-WRONG-SCALE** flag on the literal
  coherent-field boost, which overshoots ~10x). MI *helps* in the direction Sarkar's
  anomaly wants under the environmental-a0 reading (modest nu~1.2-1.7 lift), but the
  first-principles number is unavailable until the framework's linear cosmology is built.
  Both footings agree to ~10%.
- **LANE B: NEGLIGIBLE.** Apex dipole (1/2)beta_cmb = 6.2e-4 is ~14x below the ~8.7e-3
  quasar excess; a0-independent, identical both footings. Shared direction is the real
  (and only) framework-relevant datum.
