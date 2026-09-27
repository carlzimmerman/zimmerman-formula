# XR12 — "swirling down between the bands", the filament reading: does FK1's trigger fire in the web's streams?

Cross-thread review, 2026-09-26/27 (night). Read-only on every other file. Four scripts in this folder, each with controls
that reproduce committed numbers, and each with a MUTATE run that must fail and does (rc = 1). Both a₀ footings wherever
a₀ enters (canonical 9.3619e-11, alt 1.1279e-10 m s⁻²; here only through the flagship radius r_F and X-COP's two-sided
gate). κ = ½ stays a declared input. The dark mass is still required. The dark fluid is FL1/FK1's order parameter
(φ_H the cold carrier, φ_L the kicked products), not a new particle species.

**The idea, verbatim:** "the halos is like a fluid of dark energy swirling down between the bands". This lane takes the
bands to be the cosmic web's filaments: the dark fluid spirals into halos along filaments. (XR11, a parallel lane, tested
the edge-layer reading of the same sentence; the two do not overlap.)

**FK1's trigger, as used throughout.** The conversion φ_Hφ_H → φ_Lφ_L is Bose-stimulated, with an exponent ∝ n² in the
fluid's *own* density. The coupling is K-gated (λ ∝ K^(−2q), q = 1.75), so the trigger is a sharp density threshold,
ρ_t(z)/ρ̄(z) = δ_t0 E(z)⁴/(1+z)³ (FK1 N2). FK1's bracket is δ_t0 = 5–25. δ_t0 = 5.31 is exactly the linear cell's matter
reading (2/3)x_c0/Ω_m0 at x_c0 = 2.5; it reproduces XR4 R1's 5.3/4.6/4.8/6.8/16.5 at z = 0/0.25/0.5/1/2. Below, ζ = δ_t0/5.31.

## The answer

**(A) Yes — FK1's n² trigger fires in the streams before the fluid reaches halos.**
- **The threshold sits in the web.** At z = 2/2.5/3 the nominal threshold is 16.5/24.8/35.8 × the mean, inside the
  standard filament range (δ ~ 10–30). Every stream near r_vir (δ ~ 100) is above it for z ≤ 4.7. Every virialised halo
  (at its virial radius) is above it for z ≤ 6.0. At FK1's upper bracket (25: 78/117/169) the smooth filaments stay below;
  collapsed halos still cross for z ≤ 3.1.
- **On the record's own box.** On L388's z = 2 ΛCDM mesh (3 boxes), 12.5% of the carrier sits above the nominal
  threshold: 1/3 in T-web filament cells, 2/3 in knots. At 25 it is 2.9%.
- **The trigger is local, so it resolves the clumps the streams carry.** At each host's own density the gain length is
  0.1–2 pc (1e6 M☉ minihalo to 1e15 M☉ cluster). A cold stream at the bare threshold is an absolute amplifier over 20 kpc,
  with a gain length ≤ 8 kpc, ≤ 0.014 of the PM's 0.39 Mpc/h cell. So the PM runs' mesh-smoothed trigger cannot see this.
  It also answers L357 V1's open question ("the verdict hinges on whether the carrier's small halos fire"): FK1's rate
  says they do.
- **In the resolved shells, the streams convert upstream.** With streams (C_s = 10) at the nominal cell, 65–75% of the
  flagship host's conversions fall outside r_200, at 50 H and 10³ H. Smooth spherical infall converts only inside r_200.

**What that does, gate by gate:**

| Gate | Nominal cell (δ_t0 = 5.31) | FK1 upper (25) | Scripts |
|---|---|---|---|
| Lyman-α forest (DE11: ≤ 10%, k_∥ 0.2–2, z = 2–3), calibrated gas proxy | **at the line:** 11.3% ('cleared') / 8.0% ('cap'); ≤ 4.1% at k_∥ ≤ 0.5, where the proxy is validated | 5.6%: passes | forest_halo_model |
| Flagship, S ≤ 0.059 at r_F = 38.6/35.2 kpc (MS2) | passes with streams at any rate ≥ 50 H (0.014–0.022); smooth infall only at the cold rate | **fails** (canonical 0.115–0.16; alt 0.061–0.070) | stream_shells |
| X-COP, two-sided 0.286–0.768 | inside: L388's pooled ε × 0.90–1.05 → 0.34–0.63 | inside: × 0.99–1.18 → 0.37–0.71 | stream_shells |

**The band — what works.**
- The forest bounds the normalisation from below: ζ ≥ 1.42, or ≥ 2.77 with FK1's own √σ modulation.
- The flagship bounds it from above: ζ ≤ 2.54–2.76 (canonical), 4.09–4.29 (alt), with streams at FK1's rate.
- So FK1's trigger works in a band δ_t0 ≈ 7.5–13.5 (canonical, plain proxy): 1.4–2.6× the linear cell's matter reading,
  near the low end of FK1's own bracket.
- With the √σ modulation the canonical band closes (2.77 against 2.54–2.76); the alt band stays open (2.77–4.1).
- The filament geometry is what keeps the flagship's end open: converting in the streams, upstream, keeps the carrier
  from arriving at r_F.

**(B) Spin — no, not at any level a gate can see.** At λ′ ≤ 0.05:
- the rotation carries ≤ 3.7% of the support; the density at r_F drops 5.8% and the conversion edge moves 1.8%;
- the vortex lattice is 22–320 pc apart, with core filling ≤ 5e-7;
- back-to-back pairs cancel the prograde/retrograde asymmetry: retention moves ≤ 0.0064 against X-COP's 0.088 margin,
  and ≤ 0.0019 at r_F.

## Part A1 — the trigger in the web (`XR12_filament_trigger.py`, 8/8; MUTATE q = 0 fails B1, rc = 1)

| Quantity | Result |
|---|---|
| **C0** FK1 N1–N3 reproduced from FK1's formulas vs its JSON | z_convert 0.8574/1.4829/2.6934/4.0119; peak z = 0.298, 1.3479×; E_need 178.05; G_t/mc² 1.806e-9 (0 deviation) |
| **B1** background under the gate | peak 0.048 of the trigger's exponent at z = 0.30 (δ_t0 = 5.31). MUTATE (q = 0) crosses for z ≥ 0.90, FK1 N2's range |
| **A1** ρ_t/ρ̄ at z = 0/0.5/1/2/2.5/3/4/6 | 5.3/4.8/6.8/16.5/24.8/35.8/67.7/182 (5.31); 25/22.6/31.9/78/117/169/319/855 (25). Virial: 328/230/202/185/182/181/179/178 |
| **A2** L388's z = 2 LCDM mesh, 3 boxes | above the nominal threshold 0.125 of the carrier (filament 0.33, knot 0.66 of it); above 25: 0.029 (knots 0.95). CONTROL: above the PM's own trigger 0.299 vs L366's decayed 0.275 |
| **A3** gain length at the host's own density | minihalo 0.12 pc, dwarf 0.22 pc, flagship 2.1 pc, cluster 0.18 pc (≤ 9e-4 r_s). Cold streams at the bare threshold: 0.18–7.9 kpc (σ = 5–60 km/s), ΓL/v_k = 2.5–114 over 20 kpc |
| **S1** sympy | K4 = πG²/(4Hδ); a sweep that vanishes to first order gives C4 G^(3/2)/α^(1/2), C4 = 1.7480; counter-propagating kinetic amplification turns absolute at ΓL/v = 1 |
| **E** (estimate, O(1)) the effective threshold by environment | cold filaments at z = 2.5 (zero-strain cone): 0.21–0.26 n_t; sheets at z = 0.3: 0.13; converging streams at r_vir: 0.77; minihalos σ = 2–20 km/s: 0.07–0.72; galaxy halos σ = 150: 0.63–1.98; clusters: 1.6–5.1 |
| **E2** conversion rate at 2 n_t, z = 2.5 | 1456 H (σ → 0), 676/299/76/25/10 H at σ = 2/5/20/60/150 km/s; ×2.5–6 at 5 n_t |

**Reading.** FK1 normalises its coupling on the Hubble-swept background (K4). The streams are exactly where the sweep is
weakest and the pump coldest, so every cold environment they contain converts at or below n_t. The E numbers are
estimates; nothing downstream rests on them. The forest lane scans the threshold instead.

## Part A2 — the forest (`XR12_forest_halo_model.py`, 5/6; K is a recorded estimate failure; MUTATE fails H1 and H2, rc = 1)

**Method.** L357's halo model is re-implemented line for line: CLASS, Sheth–Tormen with bias, Dutton–Macciò NFW, the
kicked daughters' escape table, and a running maximum in time. It is fed into L319's validated linear solver. The one
change is FK1's threshold in a halo, ρ/ρ_crit(z) > ζ δ_t0 Ω_m0 E²; the carrier fraction cancels.

**The two proxies, and which one the forest sees.**
- **C1 (control):** L357's V1 cell is reproduced **exactly**: F_b(z = 2, 3) = 0.458335/0.429317, T²(k=5) =
  0.301392/0.367012.
- **C2 (calibration):** L366's own decay history (committed f_d = 0.1587 at z = 3 and 0.2754 at z = 2, lognormal-extended),
  weighted by the bias measured here on L388's field (2.24–2.40), was run through both proxies.
  - The **gas** proxy (the solver's cold component, projected to 1D) gives 4.73% at z = 2 against L366's **measured**
    4.18%, and 1.09% against 0.56% at z = 3.
  - The **total-matter** T²(k=5), L357's gate, reads **0.25** for that same *passing* construction.
  - So the total-matter proxy is not a forest proxy for a kicked carrier: the hot daughters' missing clustering is in the
    matter power, not in the absorbers.
- **For the record:** L357 V1's "destroys the forest" (T² = 0.30) rests on that proxy. On the gas proxy V1 reads 19% at
  z = 2: still over the 10% rule, by far less.
- **Caveat, recorded in the output.** The proxy tracks the PM at k_∥ ≤ 0.3–0.5. At k_∥ ≥ 1 the PM's flux power *rose* by
  3% where the linear proxy falls. The proxy is a magnitude calibration with a ~2× systematic.

**FK1's cell.**
- **H1.** Every halo above M_min converts **whole** for z ≤ 3. The bias-weighted converted fraction is F_b = 0.42 by z = 3
  and 0.35 by z = 4: 2.6× the PM trigger's at z = 4, so the conversion starts earlier. F_u(z = 0) = 0.40.
- **H2**, calibrated worst |ΔP1D| over k_∥ 0.2–2:

| Case | z = 3 | z = 2 | z = 2 curve at k_∥ = 0.2 / 0.5 / 1 / 2 | total-matter T²(k=5), z = 3/2 |
|---|---|---|---|---|
| nominal, M_min 1e8, 'cleared' | 0.052 | **0.113** | 0.024 / 0.041 / 0.073 / 0.113 | 0.40 / 0.34 |
| nominal, 'cap' (refilled) | 0.033 | **0.080** | 0.017 / 0.028 / 0.051 / 0.080 | 0.51 / 0.40 |
| nominal, M_min 1e6 (FDM floor at 2e-19 eV) | 0.073 | **0.149** | 0.033 / 0.056 / 0.098 / 0.149 | 0.30 / 0.27 |
| upper 25, M_min 1e8 | 0.021 | **0.056** | 0.012 / 0.020 / 0.035 / 0.056 | 0.61 / 0.44 |

The kick is a minor lever: 575–650 km/s moves the nominal cell by −0.2 to +0.5% (0.111–0.118). **The nominal cell sits at DE11's line.** On
the scales where the proxy is validated it passes (≤ 4.1%); the excess sits at k_∥ ≳ 1.4 h/Mpc. A linear proxy cannot
decide it. That needs a flux run with a sub-grid conversion.

**W, the window.** The ζ-scan gives the forest's lower bound: ζ ≥ 1.42 (plain), ≥ 2.77 (√σ). Two flagship bounds:
- **The trigger's reach**, ρ_NFW(r_F)/ρ_t, would allow ζ ≤ 12.7–44. That is not the binding bound.
- **The own-density cap** (worst case, ζ ≤ 0.059 ρ̄(<r_F)/ρ_t) gives 2.15–6.1 across hosts of 7e11–3e12 M☉ and both
  footings; 2.70/3.22 for the 1e12 host.

**K (estimate).** Cold sheets and filaments with the cone enhancement convert late (z ≲ 2.5). They add only +0.7% (nominal)
and +0.1% (upper) to the z = 2 forest, so the pre-declared "both brackets over 10%" failed (kept). But F_b(z = 2) jumps to
0.95 at the nominal cell. If that estimate holds, S₈ and cluster retention after z ~ 2 are at risk. Flagged, not scored.

## Part A3 — the flagship and clusters in the resolved shells (`XR12_stream_shells.py`, 7/8; R10 kept as run; MUTATE fails F2b, rc = 1)

**Method.** L376's halo2() (L375's shell model) is re-implemented with the trigger as a parameter.
- **C1 (control):** with the record's trigger (x̃ > 5, local total density, un-gated) it reproduces L376's committed RC100
  z = 2 numbers **exactly** (3.956624e-4, 0.453032). It is bit-identical to L376's halo2() on a fresh configuration.
- **FK1's trigger** reads the *cold* carrier's own shell density against ρ_t(z).
- **Streams:** outside r_200 the infall is concentrated by C_s = 10, a stream covering ~10% of the sphere.
- **Upstream:** a fraction F_u(z) of the accreted carrier arrives already converted, at w = 144–384 km/s (z = 0–2.5),
  taken from the forest lane's halo model.
- **Rates:** the record's 10 H, FK1's coherent limit 10³ H, and 50 H for a realistic stream (E2).

**The flagship, S(r_F), canonical/alt** (the record's x̃ trigger: 0.030/0.016):

| Variant | 10³ H (cold limit) | 50 H | 10 H (the record's) |
|---|---|---|---|
| 5.31 smooth | 0.052 / 0.039 | **0.067** / 0.040 | 0.182 / 0.047 |
| 5.31 streams | **0.019 / 0.017** | **0.022 / 0.020** | 0.085 / 0.036 |
| 5.31 streams + upstream | **0.017 / 0.014** | **0.021 / 0.019** | 0.075 / 0.036 |
| 25 smooth | 0.137 / 0.070 | — | 0.301 / 0.188 |
| 25 streams | 0.126 / 0.067 | 0.160 / 0.061 | 0.232 / 0.098 |
| 25 streams + upstream | 0.115 / 0.065 | — | 0.203 / 0.076 |

**Mechanism (F2a).** A trigger reading the fluid's own density stops below n_t, since re-seeding from vacuum needs n_t
again.
- So the cold carrier inside r_F is capped at ρ_t. At FK1's rate it sits at 5–27% of that cap.
- What r_F retains is mostly the **daughters of conversions near it** (≤ 0.08).
- A higher threshold moves the conversion inward, from a median 1.2–1.4 r_200 with streams at 5.31 to 0.40 r_200 at 25.
  More of both then stays inside r_F.
- That is why the flagship bounds FK1's normalisation from above, and why streams help it.

**The band (W2).** Log-interpolating S between the two brackets, the flagship allows ζ ≤ 2.54 (streams) / 2.76 (+upstream)
canonical, and 4.09/4.29 alt. Against the forest's 1.42 (plain) the band is open. Against 2.77 (√σ) it is closed on the
canonical footing and open on the alt.

**Clusters** (8e14 M☉, z = 0).
- The shell model's shift against the record's trigger, applied to L388's pooled ε (0.374–0.607 over 575–650 km/s), gives
  ×0.90–1.18 at FK1's rate (0.34–0.71) and ×0.98–1.08 at 10 H. **Inside 0.286–0.768 in every variant.**
- Streams lower retention (×0.90–0.93: daughters born on wider orbits). A high threshold with smooth infall raises it
  (×1.18).
- The upstream daughters, cooled to 144–320 km/s by z = 0–1, are recaptured.
- This is a shift estimate on a spherical, smooth model.

## Part B — spin (`XR12_spin_retention.py`, 5/5; MUTATE η = 1 fails B1, B3, B4, rc = 1)

| | Result |
|---|---|
| **B0** control | XR7's committed static-model 50% retention v_200 reproduced **exactly** (8 cells, 0 km/s) |
| η(λ′) for v_φ = η v_c sinθ | 0.129–0.235 over λ′ = 0.03–0.05, c = 4–10; rotational share of support 1.1–3.7% |
| **B1** centrifugal support | density at r_F −5.8%, n² rate −11%, conversion edge −1.8%. FK1 is sharp to 6%; r_F sits 12.7–44× above threshold. At 0.1 r_200: −16% (reported; no gate there) |
| **B2** vortex lattice (n_v = mΩ/πħ, an upper bound) | spacing 155/98/22 pc (flagship r_F) and 318/201/45 pc (cluster R_500) for m = 2e-19/5e-19/1e-17 eV; 2e5–1.6e9 vortices; core filling ≤ 5e-7; ≤ 6e-6 of the random node tangle multistreaming already carries |
| **B3** escape from a rotating pump | single daughters split prograde − retrograde by up to +0.11, but each pair has one of each. Pair-averaged retention moves ≤ 0.0064 (< 0.0088, a tenth of X-COP's margin); the 50% transition ≤ 0.4% in v_200; the 8e14 host 0.9946 → 0.9940/0.9949 |
| **B4** the flagship | escape of daughters born at r_F changes ≤ 0.0019, even in the full ΛCDM potential (both footings, every kick) |

## Checks and controls

| Script | Main | MUTATE (must fail) | Runtime |
|---|---|---|---|
| `XR12_filament_trigger.py` | 8/8, rc = 0 | q = 0 (no K-gate): B1 fails, the background crosses at z ≥ 0.90; rc = 1 | 4 s |
| `XR12_forest_halo_model.py` | 5/6, rc = 0 (K, an estimate, failed as pre-declared, kept) | trigger reads a mesh-smoothed density (M_min = 1e11): H1, H2 fail; rc = 1 | ~3.2 min |
| `XR12_stream_shells.py` | 7/8, rc = 0 (R10 = the first run's falsified F1/F2, kept) | v_k = 0: F2b fails; rc = 1 | ~3.6 min |
| `XR12_spin_retention.py` | 5/5, rc = 0 | η = 1 (rotation at v_c): B1, B3, B4 fail; rc = 1 | 15 s |

Every script is single-threaded (BLAS threads pinned to 1). `XR12_forest_halo_model.py` peaks near 1 GB (CLASS plus the
L388 fields); the others are far smaller.

## History and disclosures

1. **Scratch explorations came first.** In every script they preceded the checks' wording: the V1 reproduction, the
   nominal cell's F_b and both proxies, the PM calibration, and η(λ′). The H2 band (8–20%) and B1's scope (r_F and the
   edge, not 0.1 r_200) were set after them.
2. **The stream_shells first run falsified its own pre-declarations.** It ran at the record's 10 H only, with the same
   seeds. It failed F1 (0.47/0.40 of conversions outside r_200 at 25) and F2 (S(r_F) = 0.075–0.30 canonical). Both are
   kept as R10. FK1's coherent rate (10³ H) was then added, and F1′, F2a and F2b were declared before the rerun. I50
   (50 H) and E2 were added after the rerun, as reported rows.
3. **My first diagnosis of that failure was wrong.** I read it as "the own-density trigger leaves the refilled carrier at
   n_t" (a floor). The rerun shows the inequality runs the other way: at FK1's rate the cold carrier sits well below
   ρ_t/ρ̄(<r_F), and S is mostly daughters. The scripts call it a cap (an upper bound on the cold part), and the readings
   say what S is made of.
4. **The forest lane's W was amended.** It gained the cap bound after the shells' first run, and reports it as a worst
   case. H2 gained the 'cap' picture at the same time. No threshold, proxy or calibration changed.
5. **K's pre-declared expectation was wrong.** It expected both brackets over 10%; it is kept as run.

## Limits

- **Forest.** A linear gas proxy with a magnitude calibration: ~2× systematic, and the opposite sign to the PM at
  k_∥ ≥ 1. Halos only; the smooth web is the K estimate. No back-reaction of the conversion on halo formation. CDM P(k)
  down to 1e6 M☉.
- **Shells.** Spherical and smooth. Streams enter only through C_s = 10. One seed per run; static baryons. The rate is
  bracketed, not resolved.
- **The environment physics (E).** Order-of-magnitude, with O(1) factors.
- **Spin.** Static halos and a smooth rotation law.
- **FK1's constants.** ε, λ₀ and q stay declared; nothing here derives them. The trigger remains posited at action level
  as FK1 states it.

## Hand-offs (the owners' calls; nothing outside this folder was edited)

1. **The particle-mesh track (L395/L396).**
   - FK1's trigger reads the carrier's own density on sub-kpc scales. The mesh trigger (x̃ > 5 on 0.39 Mpc/h) misses the
     collapsed substructure, which converts from z ~ 6.
   - A same-model run needs a sub-grid conversion (this lane's F_u(z) is a starting point) and a flux computation. The
     nominal cell's forest verdict turns on k_∥ ≳ 1 h/Mpc.
2. **FK1's owner.**
   - The working normalisation is the band δ_t0 ≈ 7.5–13.5 (canonical), not FK1's bracket 5–25.
   - FK1's own √σ halo-regime modulation closes that band on the canonical footing. That rate needs pinning down.
   - The stream geometry (conversion upstream) is what keeps the flagship's end of the band open.
3. **L357's owner.** V1's forest verdict used the total-matter T². C2 shows that proxy fails the PM's own passing
   construction. On the calibrated gas proxy V1 reads 19% at z = 2, still a fail.
4. **S₈ and X-COP.** If the smooth web's second-order-sweep enhancement holds (E, K), F_b reaches ~0.95 by z = 2 at the
   nominal cell. That needs scoring before the band is trusted.

## Files

- `XR12_filament_trigger.py` (+ `.out`, `_MUTATE.out`, `_results.json`, `_results_MUTATE.json`)
- `XR12_forest_halo_model.py` (+ the same set). It reads FK1/L357/L366 JSON and L388's z = 2 fields, and executes L319's
  definitions exactly as L357 does.
- `XR12_stream_shells.py` (+ the same set). It imports L375/L376's helpers (their main is guarded), and reads
  `XR12_forest_halo_model_results.json`. **Run it after the forest lane.**
- `XR12_spin_retention.py` (+ the same set). It reads XR7's JSON.

Run from the repository root, e.g. `python3 real_research/cross_thread_review_2026_09_26/XR12_forest_halo_model.py`; add
`MUTATE=1` for the control.
