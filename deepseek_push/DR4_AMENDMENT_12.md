# DR4 AMENDMENT 12 — THE LAW'S VERTICAL STRUCTURE

**Filed 2026-09-15, in the open before Gaia DR4 (Dec 2026). Lane G112.**
**Deliverable: this file (`deepseek_push/DR4_AMENDMENT_12.md`), committed and pushed.**

> **NUMBERING NOTE (honesty, filed with the text).** `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`
> already carries an **AMENDMENT 12** (2026-09-09, the L47 coherence-length correction, entered from
> `fable_independent_2026/L47_xi_collision.py`). That amendment is about the wide-binary Arm B and is
> **not touched by this text**. This document is the **VERTICAL-STRUCTURE amendment** (the task's
> "Amendment 12"), consolidating the funnel, the dark disk, and the double-map into the registration.
> When this block is appended into `PREREGISTRATION_DR4.md` it takes the **next free ordinal
> (AMENDMENT 13)** there, or any ordinal the owner assigns — nothing in this text depends on the number.
> The instruction "do not rewrite the existing text, append" is observed verbatim: this amendment
> **adds** vertical-structure rows to the registration and **changes no existing row** of Section 1
> (the wide-binary arms table, Amendments 1–12), Section 2 (s^TX), or the amendment protocol.

---

> ### 🚨 AMENDMENT [12/next-free] — 2026-09-15, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **THE LAW'S VERTICAL STRUCTURE IS REGISTERED, CONSOLIDATED FROM THE COMMITTED PREDICTIONS:**
> **(a) the funnel** `z_c(R) = a0/(16πG rho_b(R))` with the exact `z_c(8.2) = 140.63 pc` and the
> `e^{+R/3}` flare; **(b) the two-scale vertical dark structure** at R0 — the phantom slab + the sech²
> dark disk — with the double-map's declared amplitudes; **(c) the falsifiers** (a flat/random `z_c(R)`
> kills the funnel; a single-scale z-profile kills the double-map); **(d) the decision rules**
> (tracer, |z| window, precision) that let a DR4 measurement decide each. It **adds**; it moves
> nothing. This is the addition the vertical structure required *before* DR4 (December); it stands on
> committed artifacts only.
>
> **SOURCES (all committed):** `deepseek_push/G076_sheet_funnel.py`/`.out` (4/4 PASS — the funnel),
> `deepseek_push/G085_vertical_disk.py`/`.out` (3/4 PASS, V2 FAIL registered as the finding — the dark
> disk), `deepseek_push/G092_dr4_verticalmap.py`/`.out` (9/9 PASS — the DR4 double-vertical map),
> on the registered ancestors `glm53_push/G024_slab_limit.py` (the phantom slab), `G042_wang_vertical_response.py`
> (the local vertical response and the R0 regime map), `G078` (the survey columns), `G03G` (the triad).
> Both a0 footings are carried wherever a0 enters (working-rule 4): canonical 9.3619e-11, alt 1.1279e-10.
>
> **(a) THE FUNNEL — the flaring phantom layer (G076, 4/4 PASS, numbers verbatim).**
>
> | quantity | registered value | source |
> |---|---|---|
> | layer width | **z_c(R) = a0/(16πG rho_b(R))**, inverse to the local baryon volume density | G076 P2 |
> | baryon density profile | **rho_b(R) = 0.095·e^(−(R−8.2)/3)** Msun/pc³ (G024's committed rho_b(R0) = 0.095; the 3 kpc disk scale) | G024 / G076 |
> | solar-circle value | **z_c(8.2) = 140.627 pc — "140.63 pc exact"** (|dev| = 0.0032 pc; alt footing 169.42 pc) | G076 V2 |
> | the fingerprint sequence | **z_c(4) = 34.7 pc \| z_c(8.2) = 140.6 pc \| z_c(15) = 1357 pc** | G076 V3 |
> | the flare | **z_c ∝ e^{+R/3}**: z_c(15)/z_c(8.2) = 9.6472 = e^{2.2667}; z_c(25)/z_c(2) = 2136 = e^{7.667} **exact** — one e-fold per 3 kpc | G076 V3 |
> | saturation surface | **z\*(R) = 4 z_c(R)** (the slab column cancels there) | G024 / G076 |
> | the kpc class | z_c(13) = 0.70 kpc, z_c(15) = 1.36 kpc — the (0.7, 1.6) kpc vertical band is the FUNNEL at R = 13–15.5 kpc, not a gas disk at R0 | G085 V4 |
>
> **(b) THE DARK DISK AND THE TWO-SCALE Z-PROFILE (G085 3/4 + G092 9/9, numbers verbatim).**
>
> The vertical dark structure at R0 is the **SUM of two components** (G092's registered map):
>
> | component | registered form | numbers | source |
> |---|---|---|---|
> | (i) the PHANTOM SLAB | rho_ph(z) = A|z|^{−1/2} − rho_b on 0 < |z| < z\*, **including the negative outer layer (z_c, z\*)**; 0 beyond z\* | z_c = 140.6 pc (can) / 169.4 pc (alt); z\* = 4 z_c = 562.5 / 677.7 pc; peak column a0/(8πG) = 26.72 / 32.19 Msun/pc², two-sided; rho_ph(z\*) = −rho_b/2; box-nu = 2√(z_c/z) cancels at z\* | G024 V7 (sympy+Lean-certified), G092 V0 |
> | (ii) the DARK DISK (sech²) | rho_dd(z) = rho0 sech²(z/h) | **h = 1.0 kpc, rho0 ∈ [0.008, 0.015] Msun/pc³, central 0.0115** — the double-map's declared component (G042-registered local phantom floor 0.0078/0.0086 sits at the band's low edge) | G092 (brief-given); G042 |
>
> The theory's own equilibrium reading of the same sech² (G085, from **sigma_dark = v_flat/√2 =
> 121.4 km/s**, the triad): **h_env = sigma²/(2πG Σ_b) = [10.9, 15.6] kpc** over Σ_b = 35–50
> Msun/pc² (mid 12.84 kpc) and **rho0 = A/R0² = 0.00811** in the measured 0.008–0.015 band (lower
> edge; alt 0.00891). **Registered as a FAIL, not a fix**: G085 V2 — the equilibrium envelope is
> ~13 kpc, NOT 1 kpc (a 1 kpc disk needs sigma ~ 36 km/s, 3.4–3.5× colder than the triad — no such
> component exists in the theory). The task's "h ~ 1 kpc" is carried as G092's **declared component
> under test**; the derived envelope is the ~13 kpc floor. The registered two-scale forecast is the
> SUM, and both disk readings sit inside its declared band (see (d)).
>
> The testable z-profile at R0 (G085's sum form; |z| units pc, Msun/pc³):
> rho_dark(z) = rho0 sech²(z/(2h)) + rho_b(2√(z_c/|z|) − 1), |z| < z\*:
> **0.3245 (30) \| 0.2318 (50) \| 0.1384 (100) \| 0.1031 (140.6) \| 0.0432 (300) \| 0.0081 (≥ 562.5, the envelope floor)**.
> box-nu(z): **4.45 / 3.48 / 2.49 / 2.12 / 1.49 / 1.11** at 30 / 50 / 100 / 140.6 / 300 / 562.5 pc —
> still falls **2.1× from 30 → 140 pc** with the disk added (disk lift < 0.1) (G092 V1b).
>
> **(c) THE FALSIFIERS (pre-declared; any one kills its structure).**
>
> 1. **F1 — the funnel.** A measured z_c(R) **without the flare — flat or random in R, or tracking an
>    NFW-class smooth width with no rho_b(R)^{-1} coupling** — kills the funnel. G076 V3's registered
>    kill: a smooth NFW vertical profile "kills it"; the flare ratio z_c(15)/z_c(8.2) = e^{2.27} is
>    the decision number.
> 2. **F2 — the double-map.** A **single-scale z-profile** — no slope break, dark density positive
>    everywhere, positive outer bin — kills the two-scale map. G092 D3's registered reading: NO
>    smooth single-component profile can produce a negative outer bin; the sign of the outer-bin dark
>    column is "the cleanest single number".
> 3. **F3 — the slab (carried from G024 V7, sharpened by G092).** **Positive dark mass measured at
>    |z| ~ 300–560 pc kills the slab component** — the two-scale map predicts rho_dark < 0 there
>    (negative on (z_down, z\*), z_down = 180.4 pc, 19% of the 5–2000 pc grid) with the disk
>    included; both NFW and single-sech² are everywhere positive.
>
> **(d) THE DECISION RULES — which tracer, which |z| window, what precision.**
>
> | front | measurement | |z| window | precision | decision |
> |---|---|---|---|---|
> | DOUBLE-MAP at R0 | vertical density (+ kinematics) of a Gaia DR4 tracer population, Bovy–Rix-2013-class vertical Jeans/Poisson inversion (the declared precision model; G092 V1) | inner |z| < 300 pc (D2); outer 300–2000 pc (D3); slope 30–140 pc (D1); box-nu curve 30–562.5 pc | column bins **sigma_col = ±6 Msun/pc²** (statistical ~2 + baryon-subtraction wall ~5.7), per-bin density **±0.10 dex** | D2: **col_dark(\|z\|<300) = 25.7–29.8, central 27.8 Msun/pc² (canonical)** / 33.3–37.4 (alt) vs **6.6 (NFW)** / 4.7–8.7 (single-sech²) → **3.5σ** each (degrades < 2σ only if sigma_col ≳ 10.5). D1: d ln rho/d ln z = **−1.95 at 100 pc** vs ~0 (NFW), −0.02 (sech²); 30→100 pc fall **4.2× vs 1.01× = 6.2σ**; divergence at z_down = 180.4 pc. D3: outer/inner ratio **NEGATIVE −0.40…−0.03 (central −0.20)** vs **+2.31 (sech²), +5.57 (NFW)** → sign separation ~5.6σ. |
> | FUNNEL | the layer width vs Galactocentric radius: vertical dark-density profile at **R = 4, 8.2, 15 kpc** (same tracer/Jeans machinery mapped in R) | |z| ~ [0.1, 1.5] kpc at the outer radii (the funnel is the kpc structure at R = 13–15.5); slab window |z| < 300 pc at R0 | per-radius log z_c precision ≲ 0.15–0.2 dex (baryon-subtraction limited, same wall model) | the sequence **34.7 / 140.6 / 1357 pc**: require z_c(15)/z_c(8.2) = e^{2.27} = 9.65 and z_c(8.2)/z_c(4) = e^{1.40} = 4.05 at ≲ 0.3 dex combined; **|d ln z_c/dR| off +1/3 kpc⁻¹ (flat or random) = F1 kill**. Alt footing z_c(8.2) = 169.4 pc must not be misread against the canonical 140.63. |
> | both | the baryon model is the shared systematic: rho_b(R)/Σ_b sets both the funnel's normalization and the subtraction wall; the SAME committed baryon profile (G024's) is the declared one — no new baryon freedom at scoring time | — | — | — |
>
> **(e) WHAT DR4 DECEMBER DECIDES ON THE VERTICAL STRUCTURE — THE HONEST STATEMENT (V3; G076 V4, G085 V4, G092 V3).**
>
> **CAN decide** (this is the registered content): (1) **funnel vs NFW** — a flaring layer width
> tracking rho_b(R)^{-1} with the e^{+R/3} sequence, vs a smooth flareless halo width; (2) **two-scale
> vs single-scale** z-profile at R0 — the slope break at 30–140 pc, the negative outer 300–2000 pc
> bin, and the ~27–30 Msun/pc² inner column vs 6.6–8.7 for every smooth single-component model;
> (3) the box-nu 1/√z fall 30→140 pc (2.1×, disk-lifted by < 0.1).
> **CANNOT decide**: (1) the **identity** of the ~1-kpc sech² component — phantom disk vs baryonic
> thick disk vs cored halo fit a vertical map alone; (2) the **a0 footing** (canonical vs alt inner
> columns differ by ~6 Msun/pc² ~ 1σ — non-diagnostic; canonical decides, alt reported); (3) the
> **R0 regime map** (G042 V1b): at R0 ~ r_M the vertical force is nu-amplified LINEAR and the
> sqrt-layer column is the LARGE-R channel — under the strict regime reading the R0 inner dark column
> would be (ν(y_sun)−1)·col_b ~ 33 Msun/pc² (canonical), LARGER still; the D1–D3 discrimination
> survives BOTH readings; (4) **publishability**: no DR4-era pipeline will publish a negative dark
> density — the registered trough (rho_dark < 0 on ~180–562 pc) will surface as an apparent
> "missing" dark matter / dip at 300–560 pc, and a pipeline force-fitting rho ≥ 0 will smear it into
> an underestimate there; (5) **scope**: the vertical map is a supplementary channel per G024's own
> registration — it is NOT one of the two frozen pipelines (Door 4A wide-binary gamma, Door 4B s^TX),
> whose verdicts are untouched by this amendment.
> **The vertical structure's scoreable outcomes**: measured **flare + two-scale + negative outer bin**
> → the three registered structures stand, scored frame-consistently with the honesty rules (no
> "validates/proves" language); **F1 or F2 or F3** → that structure is killed **exactly as
> pre-declared**, with no post-hoc rescue.
>
> **(f) DELTA vs existing — what this amendment adds and what it does not touch.**
> **ADDS** vertical-structure rows to the registration: the funnel (with its table), the two-scale
> z-profile and the dark-disk numbers, the falsifiers F1–F3, and the decision rules of (d) — this is
> the only permitted kind of pre-DR4 addition (registered before the data exist, numbers fixed from
> committed artifacts only). **DOES NOT TOUCH**: the Section 1 wide-binary arms (Amendment 10 band,
> Amendment 11 arms table, the existing Amendment 12 coherence corrections — Arm A untouched, all
> clauses stand), the Section 2 s^TX bands, the estimator, the cut table, the error model, the
> frozen N, the no-verdict edge 1.23, the a₀-degeneracy flag, κ = ½ fitted-not-derived. No
> measurement moves. The two G024-registered banked fronts remain the frozen pipelines; this lane is
> registered as the supplementary vertical channel with its own pre-declared verdicts.
>
> **(g) Honest limitations carried.** The funnel's exact 140.63 pc inherits G024's rho_b(R0) = 0.095
> (28.5 one-sided / 300 pc); a baryon-model revision at scoring time is a mechanical substitution
> recorded in the appendix, never a re-tune. The double-map's declared precision (sigma_col = ±6
> Msun/pc², Bovy–Rix-2013-class) is an assumption, stated as such; the amplitude channel degrades
> below 2σ only past sigma_col ~ 10.5, the shape and ratio channels are systematics-limited
> separations no smooth single-component profile can mimic. The registered negative layer is
> G024-V7-certified (sympy + Lean) and cannot be laundered into a positive reading.
>
> **VERDICTS ON THIS FILING.** **V1 PASS** — the amendment text is complete: every committed number
> (the funnel 140.63 pc exact and the 34.7/140.6/1357 pc sequence, the e^{+R/3} flare, the sech²
> disk with its band, the two-scale profile), the falsifiers F1–F3, and the decision rules (tracer,
> |z| windows, precisions) are in the text above, quoted from committed artifacts. **V2 PASS** — the
> append-only discipline is stated ((f) and the header note): rows are added, no existing text is
> rewritten, and the pre-existing AMENDMENT 12 is explicitly left untouched. **V3 PASS** — the honest
> statement ((e)) says what DR4 December decides on the vertical structure: the flare-vs-flat layer
> width, the two-scale-vs-single-scale profile, the negative outer bin and the ~27–30 Msun/pc² inner
> column are decidable; component identity, the a0 footing, the R0 regime map and the publishability
> of the negative trough are not. The vertical structure is registered before DR4 as required.