# XR19 — does the dark fluid's own conversion, once seeded in halos, run away through the cosmic web?

Cross-thread review, 2026-09-27. Read-only on every other file. Two scripts and a shared module in this folder. Each script
has controls that reproduce committed numbers exactly, and a MUTATE run that must fail and does (rc = 1). The dark fluid is
FL1/FK1's order parameter Φ: a classical field, not a particle species. Its quanta would be bosons of mass m ≳ 1.9–5.2 ×
10⁻¹⁹ eV, and **the dark mass is still required**. κ = ½ does not enter. a₀ enters only through the flagship's bound on the
conversion's normalisation. Both footings are carried there: canonical 9.3603 × 10⁻¹¹ and alt 1.1312 × 10⁻¹⁰ m s⁻².

Every rate is FK1's, FL2's or FP10's own:
- the pair coupling G(ρ, z) = G_t(z) ρ/ρ_t(z), with G_t = √(4HδE_need/π);
- the vacuum-gated threshold ρ_t/ρ̄ = δ_t0 E⁴/(1+z)³ (q = 1.75);
- the Hubble sweep πG²/(4Hδ) (FK1 K4);
- the second-order sweep C4 G^{3/2}/√α (XR12 S1);
- FP10 A5's Doppler-broadened rate γ = √π G²/(m v_k σ).

No constant was added. ε/m² (through v_k) is FITTED; λ₀ and q are DECLARED.

## The answer

**Partly yes.** The conversion runs through the collapsed and turned-around web at z ≲ 1.5 and percolates. It does not run
through the voids, and it does not run at z ≳ 3. It does not convert the whole dark mass.

Converted fraction of the WHOLE dark fluid, F_tot = F_halo + (1 − F_halo) f_web (running maximum):

| case | z = 3 | 2 | 1.5 | 1 | 0.5 | 0 |
|---|---|---|---|---|---|---|
| halo budget only (XR16's machinery, run to z = 0) | 0.342 | 0.433 | 0.480 | 0.529 | 0.580 | 0.629 |
| **nominal cell** (δ_t0 = 5.31) | 0.363 | **0.554** | 0.690 | **0.811** | 0.880 | **0.912** |
| nominal, every O(1) choice at its conservative end | 0.347 | 0.473 | 0.558 | 0.667 | 0.775 | 0.838 |
| nominal, pump = full cell density | 0.385 | 0.666 | 0.801 | 0.888 | 0.923 | 0.935 |
| nominal, no seeding (spontaneous only) | 0.356 | 0.505 | 0.597 | 0.692 | 0.779 | 0.833 |

**The band, both footings.** The forest's lower bound sets δ_t0 ≥ 7.54. The flagship's upper bound (XR12 W2) is 14.6 on the
canonical footing and 22.8 on the alt.

| band edge | F_tot(0 / 1 / 2) | every O(1) choice at its conservative end, F_tot(0 / 1) |
|---|---|---|
| δ_t0 = 7.54 (both footings) | 0.895 / 0.754 / 0.502 | 0.782 / 0.614 |
| δ_t0 = 14.6 (canonical top) | 0.812 / 0.631 / 0.443 | 0.690 / 0.556 |
| δ_t0 = 22.8 (alt top) | 0.743 / 0.578 / 0.404 | 0.656 / 0.534 |
| δ_t0 = 25 (FK1's upper bracket) | 0.730 / 0.569 / 0.395 | 0.651 / 0.530 |

**What drives it.** Three mechanisms, each computed in XR19_front_physics.

1. **Halo seeds, momentum-matched through the infall.** Bose stimulation needs |v − u_pump| = v_k against the LOCAL pump. At
   r200 the infalling pump blue-shifts 86–87% of the daughters, including tangential ones through the converging infall.
   They re-cross the resonance near 5 r200, close to the turnaround radius.
   - With the full-density pump, at z ≤ 1, the median gain there is 11–32 e-folds, which converts the zone (Y ≥ 1) for every
     tested halo, 10¹¹–10¹³ M☉.
   - With the smooth pump (1 − F_halo), it converts only for M ≥ 10¹² M☉.
2. **The zero-strain cone.** A turned-around single-stream sheet has directions along which the detuning's first derivative
   vanishes. The narrow resonance (G/δ ~ 10⁻³) then holds a mode for √(G/α), not G/(Hδ).
   - Exact ray integration gives 15–41× the Hubble sweep's gain; the local formula is confirmed to 0.70–0.89.
   - Pancakes therefore ignite from vacuum below the trigger, at ρ/ρ_t down to 0.20 at z = 2.
3. **Re-resonance in contracting flow.** Daughters born inside a turned-around pancake are blue-shifted along its collapse
   axis, then red-shifted outside, so they cross the resonance again.
   - This holds for 2–7% of (birth point, direction) pairs just past turnaround (d = 0.6), 14–19% at d = 0.75 and 21–26% at
     d = 0.85.
   - The median gains there are 40–220 e-folds at z ≤ 1.

On the web census (nominal cell) the conversion enters by these channels, as fractions of all cells:

| channel | spontaneous | seeded |
|---|---|---|
| turned-around sheets | 0.164 | 0.344 |
| multistream (kinetic) | 0.031 | 0.099 |
| expanding cells | 0.003 | 0.121 |

The converted set is one connected cluster: ≥ 0.99 of the converted cells at z ≤ 1.5.

**What stops it.**

1. **Expanding flow — a theorem.** For a pressureless pump and a free daughter in the same gravity, w = v − u obeys
   dw/dt = −(w·∇)u exactly (S1). So |w| only falls wherever the strain is positive definite.
   - A daughter born on the resonance there never returns, and a seed enters at most once (H1: zero re-crossings in every
     direction).
   - The voids' pump gains less than a few e-folds per passage.
   - Result: expanding cells are 7.8% converted at z = 0, and 93% of the unconverted cells are expanding.
2. **The gate at high z.** ρ_t/ρ̄ = 36 and 68 at z = 3 and 4, so f_web(z = 3) ≤ 0.066 in every bracket and at every
   normalisation from 5.31 to 25 (W2). Without the gate (MUTATE) everything converts by z = 6, and the mean background
   self-ignites for z ≥ 0.91.
3. **The smooth pump is dilute.** Only 1 − F_halo of a cell's density pumps; with the full density, F_tot(1) would be 0.888.
4. **The normalisation.** At the band's top, f_web(0) falls to 0.31–0.50.

**Robustness across (m, K, v_k, ε)** — f_web(z = 0 / 1) of the smooth carrier at the nominal cell:

| bracket | f_web(0 / 1) | nominal |
|---|---|---|
| v_k = 575–650 km/s (ε/m² = 1.84–2.35 × 10⁻⁶) | 0.761–0.764 / 0.597–0.606 | 0.762 / 0.598 |
| m = 10⁻¹⁷ eV (E_need 162) | 0.759 / 0.591 | |
| m = 10⁻⁶ eV (E_need 61) | 0.700 / 0.461 | |
| pump roughness σ_r = 0–30 km/s | 0.761–0.769 / 0.594–0.643 | |
| cone calibration 0.2–0.70 | 0.760 / 0.591 at 0.2 | |
| compression cap 3–∞ | 0.759–0.762 | |
| kinetic rate × ½ | 0.751 / 0.575 | |
| t_av 0.3/H | 0.758 / 0.590 | |
| g_need 1–10 | 0.716–0.798 / 0.477–0.717 | |
| reach 1–4 cells | 0.751–0.762 | |
| isotropic strain | 0.740 / 0.565 | |
| second realisation | 0.758 / 0.592 | |
| R_s = 1 Mpc/h | 0.704 / 0.517 | |
| every conservative choice at once | 0.562 / 0.292 (R_s 0.5); 0.496 / 0.201 (R_s 1) | |

K (the halo front's depth, 18–540) enters only F_halo and moves XR16's F(z ≤ 2) by ≤ 0.013. δ_t0 is the dominant lever.

## What it costs, if F_tot ~ 0.8–0.9 by z ~ 0.5–1

L319's linear solver is exec'd via L357's head. It is run with S(a) = 1 − F_esc, where F_esc is XR16's bias-weighted escaped
halo fraction plus the web part, because web daughters leave shallow structures.

| history | F_esc(0) | S8 ratio | carrier T²(k = 0.3 / 1 / 3 h/Mpc), z = 0.5 | C_L^φφ ratio, L = 100 / 300 / 1000 |
|---|---|---|---|---|
| halo only | 0.497 | 0.956 | 0.855 / 0.295 / 0.214 | 0.998 / 0.985 / 0.919 |
| **nominal** | 0.797 | **0.931** | 0.800 / **0.118** / 0.063 | 0.996 / 0.980 / **0.904** |
| every conservative choice | 0.706 | 0.942 | 0.830 / 0.201 / 0.112 | 0.997 / 0.983 / 0.912 |
| pump = full density | 0.856 | 0.924 | 0.776 / 0.073 / 0.042 | 0.996 / 0.978 / 0.896 |
| δ_t0 = 14.6 / 22.8 | 0.662 / 0.579 | 0.943 / 0.949 | 0.839–0.854 / 0.231–0.280 / 0.149–0.206 | ≥ 0.997 / ≥ 0.984 / 0.922–0.931 |

- **S8.** The ratio is 0.931 at nominal (absolute 0.783). That passes FP10 B6's strict gate (0.922), its alt gate (0.899) and
  PAPER34's floors (0.752/0.748). The pipeline reproduces FP10 A8's maximal "whole carrier converts at z_web" bracket to
  0.5–1%: 0.912 / 0.924 / 0.938 against FP10's 0.918 / 0.929 / 0.948. S8 moves by percents because the daughters' streaming
  scale is near σ8's.
- **Free streaming.** Web daughters converted at z = 2 / 1 / 0.5 move at 200 / 300 / 400 km/s today. That is k_fs = 0.34 /
  0.23 / 0.17 h/Mpc (λ 18–37 Mpc/h), after travelling 4.3 / 3.3 / 2.2 Mpc/h. They stream out of every galaxy and group
  potential, cluster only above ~20–40 Mpc/h, and are recaptured by clusters once Hubble-cooled.
- **Small-scale carrier power and KiDS.** At k ≳ 1 h/Mpc, z ≈ 0.5, the carrier's clustering falls a further 2.5–3.5× below the
  halo-only budget. Galaxy- and group-scale lensing would then rest on the MOND sector's phantom. Only the record's full
  lensing machinery (L360's switched fit, MS3's resolution-free cosmic-shear bound) can score that. **Not re-scored here.**
- **CMB lensing.** The web adds about 0.5% at L = 300 and 1.5% at L = 1000 (linear, Limber). Planck measures the lensing
  amplitude to about 2.5%, so this is at the error, not decisive alone.
- **Lyman-α forest.** F_tot(2) = 0.554 at nominal. XR16 B2's committed response range projects an L365-rule deviation of
  0.034–0.173, against the 0.10 gate (halo only: 0.027–0.135). The forest is strained further, and it stays "not established".
  This is an extrapolation past the committed F(2) ≤ 0.28.
- **X-COP** (order of magnitude only). A cluster's carrier accreted after z_web ≈ 1–1.5 that arrives already converted is
  24–38% of it, for dlnM/dz magnitude 0.6–1.0. Those daughters are Hubble-cooled to ~300–400 km/s, far below a cluster's
  ~2000 km/s escape speed, so they are recaptured on hotter orbits, as XR12's upstream daughters were. The retained fraction
  moves by less than this share. **Not re-scored.**

## What this means for a particle-mesh run of this dark sector

A halo-only sub-grid rule (XR16's F(z)) misses 0.12 of the carrier at z = 2 and 0.28 at z = 1 (nominal). It also puts the
removal in the wrong place: sheets, filaments and groups' surroundings, not only halos.

The web conversion is **not a knock-out** at the linear or order-of-magnitude level for S8, CMB lensing or X-COP. It worsens
the forest projection. It removes most of the carrier's remaining small-scale clustering at z < 1.

So a particle-mesh run is worth doing **only with the web channel in its sub-grid conversion**. The rule, from the census:
- a turned-around single-stream cell ignites on the zero-strain cone;
- the smooth pump is (1 − F_halo) ρ;
- a cell within ~1 Mpc/h of a converted converging or halo-hosting cell converts when its per-passage gain reaches ≳ 3
  e-folds;
- expanding cells get one passage only.

Its decisive outputs would be the forest at z = 2–3 and cosmic shear/KiDS (carrier removal against the phantom). S8 and X-COP
are not expected to decide.

## Part 1 — the front's physics (`XR19_front_physics.py`: main 12/12, rc = 0; MUTATE rc = 1)

| Check | Result |
|---|---|
| **C0** control | FK1 N1–N3 from FK1's formulas: z_convert 0.8574/1.4829/2.6934/4.0119; peak z = 0.298 at 1.3479×; E_need 178.05; G_t/mc² 1.806e-9. Deviation 0. |
| **C1** control | XR16 B3's and FP10 A8's committed "mean density stimulable below z" (1.152/1.762 and 1.165/1.760) reproduced exactly from the per-passage gain E_need (ρ/ρ_t)². |
| **G** (reported) | The gain map by z and density, gain lengths (coherent ~0.01–0.1 kpc at 10ρ̄; kinetic σ = 20: 0.3–11 kpc), and the seeded-conversion density for ln(pump/seed) = 1/3/10, over δ_t0 = 5.31–25 and E_need 61–178. |
| **G2** | The gate keeps the mean background's spontaneous exponent ≤ 0.048 E_need (z ≤ 10). A resonant seed gains up to 2.9–8.5 e-folds per passage there (z = 0.30), ≥ 1 below z = 1.16–1.76. |
| **S1** [sympy] | dw/dt = −(w·∇)u (with the chain rule on a generic field); d\|w\|²/dt = −2w·T·w (vorticity drops out); D'' = 2δ(2\|Tn\|² − n·Ṫ·n); on the cone \|Tn\|² = −e₁e₂; I(0) = C4, βI → π/2; the Doppler area is 2× the coherent one in FP10's convention (a factor-2 bracket downstream). |
| **H1** | Hubble flow, 21 directions at z = 0.5/1/2: gain = K4 to ≤ 8.6e-4; D(t) strictly falling after birth; 0 re-crossings. |
| **Z1** | Six turned-around pancakes (z = 0.5–2, d = 0.7–0.85): the exact max over directions is 0.697–0.887 of the local cone formula; the transverse direction matches K4 to 0.1%. |
| **Z2** | The cone beats the Hubble sweep 15–41×. All four sub-trigger pancakes ignite: 2686 e-folds at ρ/ρ_t 0.70, 1616 at 0.49, 295 at 0.20, 472 at 0.40 (E_need 178). |
| **Z3** (reported) | The 1D ignition compression by z, δ_t0, pump fraction and roughness (e.g. nominal, smooth pump, σ_r 10: 2.9/4.6/7.2/19.9/47.8 at z = 0/0.5/1/2/3; turnaround is 2.0–2.9). |
| **B1** | Re-crossing fraction 0.02/0.06/0.07 (d = 0.6), 0.14/0.18/0.19 (0.75), 0.21/0.26/0.26 (0.85) at z = 0.5/1/2. Median gains 222/98/10, 60/40/5, 95/53/7 e-folds. Hubble control 0. |
| **I1** | LCDM spherical shells (δ_c(M/M200)^(−0.6)); daughters from r200. Fast fraction 0.86–0.87 in every case; crossings at 4.9–5.3 r200 (1+δ 1.9–2.6). With s = 1 at z_e ≤ 1: gains 11–32, Y = 9e2–3e12. |
| **I2** (reported) | Smooth pump: Y = 0.28 (10¹¹, z = 1), 1.1–20 (10¹²–10¹³). z_e = 2: Y 0.14–0.86. δ_t0 = 13.5: Y 0.04–8. ε = 0.4/1.0: Y 32 / 0.17. |
| **R** (reported) | A daughter's comoving travel to z = 0 is 3.2–6.9 Mpc. The resonance reach Δ/H is 0.4–5 comoving Mpc for an excess Δ = 30–300 km/s. |
| **H** (reported) | The pre-declared hypotheses: H-S, H-H and H-Z held. **H-B fell** at its pre-declared configuration (d = 0.6: 2–7% < 20%). **H-I fell** on its smooth-pump clause (10¹¹ at z = 1: Y = 0.28). Kept as run. |

**MUTATE** (Bose stimulation removed): G2, H1, Z1, Z2, B1 and I1 fail; the controls and identities pass. 6 load-bearing
failures, rc = 1.

## Part 2 — the web (`XR19_web_runaway.py`: main 12/13, rc = 1 — H-W1 fell in its stacked conservative corner; MUTATE rc = 1)

The web is a Gaussian field with the record's CLASS P(k), on 128³ Lagrangian cells (R_s = 0.5 Mpc/h). A second realisation
and R_s = 1 Mpc/h are brackets. Zel'dovich gives densities and strains for single streams. Multistream cells take the
Zel'dovich particles' CIC density and 1D dispersion. The census is time-tracked over 17 epochs from z = 6 to 0, and
conversion is irreversible. The seeded front is causally limited to v_k dt per step. Percolation is the largest
6-connected cluster.

Why not the record's lognormal PDF (XR12's σ_ln): momentum matching needs each element's strain, and a one-point density
PDF carries none. The Zel'dovich field is the same Gaussian field the lognormal model exponentiates, with its deformation
tensor kept. The halo model enters through F_halo, from XR16's own machinery.

| Check | Result |
|---|---|
| **C1** control | XR16's committed F(z) history, 260 rows (20 budgets × 13 epochs), reproduced exactly by its own Part B, exec'd from its committed text. |
| **C2** control | L319's committed universal-decay cell (5 Gyr, 600 km/s) exactly: S8 0.7865422693234108, T²(k=5, z=3) 0.46813357143746914. |
| **C3** control | The grid's T-web fractions at threshold 0 are 0.0794/0.4193/0.4225/0.0789, against Doroshkevich's 0.0798/0.4202/0.4202/0.0798. σ(δ_lin) = 2.465 against CLASS's 2.415. |
| **B** (reported) | XR16's halo budget to z = 0 and across the band: F_halo(0) = 0.627–0.629; F_b,esc(0) = 0.460–0.497. |
| **G0** | The gate: the mean background's spontaneous exponent ≤ 0.048 E_need. MUTATE: it self-ignites for z ≥ 0.91. |
| **W1 = H-W1** | **FAIL as pre-declared ("in every O(1) bracket").** Every single-choice bracket passes: f_web(0) ≥ 0.70, f_web(1) ≥ 0.46, percolation ≥ 0.92 at z ≤ 1.5. The stacked "every conservative choice at once" corners fail: f_web(1) = 0.288–0.292 (R_s 0.5, two realisations) and 0.201 (R_s 1); f_web(0) = 0.496 (R_s 1); percolation 0.14–0.65 at z = 1.5. Kept as run. |
| **W2 = H-W2** | f_web(z = 3) ≤ 0.066 in every bracket and at every δ_t0 in 5.31–25. |
| **W3 = H-W3** | 93.3% of the cells unconverted at z = 0 are expanding; expanding cells are 7.8% converted. |
| **F1 = H-F** | Min F_tot(0) = 0.743 and min F_tot(1) = 0.578 over the four band edges (≥ 0.7 / 0.55). |
| **X1 = H-X** | S8 ratio 0.931 ≥ 0.899, and ≥ 0.922 as well. |
| X2–X5 (reported) | Free streaming, carrier T²(k), CMB lensing, the forest projection, X-COP's order of magnitude (above). |

**MUTATE** (the gate removed, q = 0, in the census and in XR16's budget; C1 still reproduces the committed, gated history):
G0 and W2 fail. W3 also fails, because nothing is left unconverted. rc = 1.

## History and disclosures

1. **Scratch explorations came first** (session scratch, not committed): the gain map, the pancake's local cone formula
   and exact rays, four census prototypes (Zel'dovich without and then with CIC, time tracking, halo sources, caps), and
   the spherical-shell infall model. Both scripts' hypotheses were written after these and before the scripts ran.
2. **Smoke runs.** Each script was run once as a code test before its recorded runs. The first was a copy writing to
   scratch; the second a documented `XR19_SMOKE=1` mode on 48³ grids. The first found three code bugs in
   `XR19_front_physics.py`, fixed before the recorded runs:
   - C1 took the wrong end of the stimulable range;
   - Z2 required every tested pancake to be sub-trigger instead of testing those that are;
   - I1's filter compared a rounded δ_t0 with the unrounded one and passed vacuously.
3. **Two thresholds were relaxed after the smoke run.** The smoke run showed B's pre-declared configuration (d = 0.6) re-crossing
   for only 2–7%, so depths 0.75 and 0.85 were added after it. B1's and I1's load-bearing thresholds were then relaxed to
   existence claims. H keeps the original thresholds, and both fell.
4. **H-W1 was not changed** after the 48³ smoke run showed its conservative corner failing, and it fell again at 128³.
5. **The main run of XR19_web_runaway exits 1** because of H-W1. The MUTATE runs exit 1 by design, on G0/W2 and on
   G2/H1/Z1/Z2/B1/I1 respectively.
6. **The census's spontaneous ignition is caustic-driven.** In the prototype, turned-around ignition happened mostly near
   the Zel'dovich caustic, at a median compression of ~34×. So a compression cap (3, 10) is a bracket. It moves f_web(0) by
   ≤ 0.003, because seeding carries the conversion once anything ignites, and the halos (the design's own conversion)
   always do.
7. **A factor-2 convention.** FP10's golden-rule rate is an occupation rate normalised with FK1's amplitude convention (S1:
   the kinetic area is 2× the coherent). It is carried as "kinetic × ½", which moves f_web(0) by 0.011.

## Limits

- **The web.** Zel'dovich on 64–128 Mpc/h boxes: exact for single streams and CIC-smoothed after shell crossing. There is no
  back-reaction of the conversion on structure growth. Sub-cell halos enter only through F_halo and the smooth fraction.
  It is a sub-grid model with brackets, not a simulation.
- **The pump's coherence.** The coherent cone formula needs the pump smooth to ~0.1–0.3 km/s over ~50–200 kpc. Roughness is
  a bracket (σ_r = 0–30 km/s), not derived.
- **Halo zones.** Spherical shells, one power-law profile (ε = 0.6; 0.4–1.0 reported), a static halo during the crossing,
  and the first crossing only.
- **Consequences.** Linear (L319) for S8, T² and CMB lensing. The forest projection is XR16's extrapolation. X-COP is an order
  of magnitude. KiDS and cosmic shear are **not scored**.
- **The flagship band.** It is XR12 W2's (committed). Whether the web conversion moves the flagship's own bound was not
  re-derived.

## Hand-offs (the owners' calls; nothing outside this folder was edited)

1. **The particle-mesh track:** the web channel's sub-grid rule above, and the forest at z = 2–3 and cosmic shear/KiDS as
   the decisive outputs.
2. **FK1/FL owner:** the trigger is not a density threshold outside the Hubble flow. The zero-strain cone lowers it in every
   turned-around sheet, and the normalisation δ_t0 is the lever that controls the web runaway.
3. **The lensing owners (L360/MS3):** the carrier's small-scale clustering at z < 1 falls a further 2.5–3.5× with the web
   conversion.

## Files

- `XR19_common.py`: shared formulas.
- `XR19_front_physics.py`, with `.out`, `_MUTATE.out`, `_results.json`, `_results_MUTATE.json`.
- `XR19_web_runaway.py`, with the same four output files. It execs XR16's head and Part B, and through them AT1's machinery,
  L357's head and L319's solver.
- `XR19_README.md`: this file.

## Reproduction

Run from the repository root, `XR19_front_physics.py` first because `XR19_web_runaway.py` reads its Z1 calibration:

```
python3 real_research/cross_thread_review_2026_09_26/XR19_front_physics.py      # ~5 min
python3 real_research/cross_thread_review_2026_09_26/XR19_web_runaway.py        # ~9 min, ~3 GB
```

Prefix either with `MUTATE=1` for its control. `XR19_SMOKE=1 XR19_OUTDIR=<dir>` is a reduced code test for the second
script, never for the record. BLAS is pinned to one thread; at most two workers.
