# L319–L320 — the Λ-triggered kicked-decay carrier, and the pincer it exposes

## L319 — the one dark-sector door the record left untested

`L319_lambda_triggered_kicked_decay.py` reuses the validated exact linear-response solver from L168, copied rather than edited, with CLASS initial conditions. Its controls:

- The ΛCDM growth matches CLASS to 1.1%.
- With v_k = 0 the model reproduces ΛCDM. The residual is first-order discretisation: 1.56e-3, 1.11e-3 and 7.7e-4 at N_A = 300, 420 and 600 (`L319_c2_convergence.py`).
- It reproduces L168's universal-lifetime cell: S8 = 0.7865, with the forest failing.

`MUTATE=1` replaces the trigger with a universal lifetime of the same f_d(0); the forest then fails and rc = 1. A resolution re-run is recorded in `_NA600.out`.

**Model.** X → Y + light, with an isotropic kick v_k given to the daughter. The decay rate is Γ ∝ [Ω_Λ(a)/Ω_Λ,0]^p. The record closed kicked decay only for a *universal* lifetime (the forest needs τ ≥ 41 Gyr, galaxies need τ ≤ 20 Gyr). A rate triggered by vacuum domination avoids that pincer by construction.

| Cell | f_d at z = 3 / 2 / 1 | Power at k = 5 h/Mpc (z = 3, z = 2) | S8 |
|---|---|---|---|
| p = 2, f_d(0) = 0.8, v_k = 600 | 0.0004 / 0.0031 / 0.048 | 0.9996, 0.9965: **strict forest pass** (≥ the 5.3 keV relic) | **0.826** |
| p = 2, f_d(0) = 0.8, v_k = 1000 | same | 0.9995, 0.9957: strict pass | **0.803** |

For comparison, KiDS-Legacy measures 0.815 ± 0.016 and Planck 0.834. **This is the first carrier on the record to pass both the forest and S8** while depleting 80% of the cold component by today, which is what galaxies need.

## L320 — the price at high redshift, and a framework result

`L320_carrier_highz_price_rc100.py` (4/4; `MUTATE=1` sets the retained fraction to zero, and the rise and overshoot findings fail, rc = 1). Each of RC100's galaxies (z = 0.6–2.5) is predicted under three models and pushed through the data's own closed-form inversion. The systematic grid covers disc geometry, gas fraction and a₀ footing.

| Model | d log a₀/dz | Median f_DM inside R_e |
|---|---|---|
| **RC100 data** | −0.112 ± 0.062 | 0.29 |
| Framework alone | 0 (flat, exactly) | **0.23–0.31** |
| Framework + L319 carrier | +0.07 to +0.10 (**3.0–3.4σ against the data**) | 0.48–0.59 |
| ΛCDM alone (Moster+13 halo masses, Dutton–Macciò concentrations, no contraction) | +0.13 to +0.15 | 0.38–0.49 |

**Two results:**

1. ~~On RC100 the framework alone beats ΛCDM on both the level and the trend.~~ **Corrected by L323: the LEVEL is a tie.** Given its fair systematic range (NFW, a −0.2 dex lighter halo, or −0.1 dex lower concentration), ΛCDM also matches RC100's median f_DM. **The TREND is robust:** every ΛCDM variant, including a maximal feedback core and the combination most favourable to ΛCDM, predicts a₀ rising at +0.13 to +0.16 dex/z, 3.7–4.1σ above RC100's trend, while the framework is flat (1.6σ). RC100's caveats apply: its f_DM is model-dependent and its selection is uncontrolled.
2. **The forest–RC100 pincer applies to any carrier.** The forest needs a cold component clustered in the intergalactic medium on 0.1–1 Mpc scales at z = 2–3. RC100 says galaxies at that same epoch carry no cold halo. Kicks remove matter from shallow wells first, so they deplete the intergalactic medium before galaxy halos, which is the wrong order. A carrier would have to be absent from galaxy halos while present in the intergalactic medium at z ≈ 2, and also present in clusters today: a switch that is non-monotonic in potential depth. The record has found no such switch (f22).

**Standing:** the Λ-triggered carrier passes the forest and S8 but is disfavoured at about 3σ by RC100. The structural conflict between closing the dark sector and the framework's flat-a₀(z) galaxies is now explicit.

## L321 — the z = 0 gates on the real X-COP sample, with both couplings

`L321_carrier_z0_retention_gate.py` (4/4; `MUTATE` v_k = 0 fails G1, rc = 1). Retention is computed by exact phase-mixing in the framework's gravity (ν_RAR plus the SW01 magnitude-based external-field rule), relative to a no-decay control drawn with identical random numbers. C2 reproduces the record's 0.576 by an independent route: the additive median over 12 X-COP clusters is 0.476.

- **Universal coupling** (the carrier sources the MOND field) is **dead at z = 0 on clusters**. Retained daughters are MOND-boosted, and X-COP overshoots by 1.56–1.84× at every kick S8 allows. ⚠️ Correction from L322's mutation run: the *galaxy* failure (+0.08–0.10 dex) holds at f_d(0) = 0.8 only; at f_d = 0.9 universal galaxies pass (+0.042 dex).
- **Additive coupling** (a metric-coupled carrier) passes every galaxy host. X-COP overshoots by 1.34 at the kicks S8 allows.
- ⇒ **A dark carrier in this framework must not source the MOND field.** The binding reason is the clusters, not the galaxies.

## L322 — the additive window, RC100, and a coincidence test

`L322_additive_window_and_coincidence_test.py`. All thresholds were declared before the scan.

| Threshold set | Window |
|---|---|
| Strict: S8 ≥ 0.767 (KiDS-Legacy 3σ); X-COP within 20% | **none** |
| Alternative: S8 ≥ 0.748 (DES × KiDS 3σ); X-COP corrected for the measured 6% non-thermal support | v_k 1400–1700 (f_d 0.8), 1300–1400 (f_d 0.9) |

- RC100 under additive coupling is **3.5–3.7σ against the carrier**, with f_DM 0.49–0.56 against 0.29.
- **Coincidence test, with pre-declared candidates and a look-elsewhere count:**
  - For the decay rate, Γ₀ = 5.5–8.4 H₀ and none of the 28 framework-rate candidates falls in it (chance of at least one: 0.93).
  - For the kick, 1 of 27 candidates falls in the window: √(a₀ × 1 Mpc), which uses an arbitrary length, with a chance rate of 0.84.
  - **No coincidence.**

**Standing of the carrier:**
- It passes the forest and S8.
- It must be metric-coupled.
- It survives z = 0 only in a threshold-dependent sliver.
- It is disfavoured at about 3.5σ by RC100.
- Its rate has no natural scale.

The dark-sector door is now stated as precisely as the record allows: cold in the intergalactic medium at z = 2–3, absent from galaxy halos at z ≲ 2.5, about half-present in clusters at z = 0, and not sourcing the MOND field.

## L323 — stress test of the RC100 comparison, with ΛCDM given every fair chance

`L323_rc100_framework_vs_lcdm_stress.py` (6/6; `MUTATE` +0.25 in f_DM breaks the level tie, rc = 1). ΛCDM variants tried: NFW (Moster+13 halo masses, Dutton–Macciò concentrations), a halo 0.2 dex lighter, concentration 0.1 dex lower, a maximal Read+2016 core (n = 1, r_c = 1.75 R_e), Blumenthal contraction, and all of the favourable ones together.

- **Level (median f_DM inside R_e): tie.** The framework's best cell and the NFW, lighter-halo and lower-concentration cells all contain zero offset at 68%. **The L320 level claim is withdrawn.**
- **Trend (inverted a₀ against z): every ΛCDM variant rises by +0.13 to +0.16 dex/z, 3.7–4.1σ above RC100.** The framework is flat at 1.6σ. No halo knob removes the rise, because it comes from how ΛCDM halos evolve with redshift.
- **Framework residuals** show no trend with g_bar (Spearman p = 0.29), so there is no sign of a wrong kernel at z ~ 1–2.

## L332 — the independent replication on KMOS3D: it did not happen, and L323's trend becomes conditional

`L332_kmos3d_trend_replication.py` (4/5; the fifth is the pre-declared T1, shown as FAIL; `MUTATE` replaces v_obs with the ΛCDM-NFW prediction, K1 and K2 fail, rc = 1). The data are Übler+2017 v_circ,max for 117 galaxies, cross-matched uniquely to the KMOS3D catalogue's H-band R_e. 93 of them are not in RC100.

- **The pre-declared replication failed.** Every model's residuals fall with z, the framework included: −0.070 to −0.084 dex/z (5σ), against ΛCDM's −0.094 to −0.106.
- **The cause is common-mode (K1).** Newtonian baryons alone fall at −0.11 dex/z. At z ≈ 2.3, 27–54% of galaxies (depending on geometry) rotate *slower than their own Newtonian baryons*; at z ≈ 0.9 the figure is 2–11% (Fisher p ≤ 3×10⁻⁴). Übler's gas-to-star ratio comes from scaling relations and rises from 0.46 to 1.19. No model that adds gravity can fit those galaxies.
- **KMOS3D cannot decide the question (K2).** The framework and ΛCDM predicted trends differ by ≤ 0.031 dex/z, while the data sit ≥ 0.068 dex/z off both. L323's inverted-a₀ statistic does "replicate" at 4.4σ, but it drops 50% of the z > 1.9 galaxies and only 10% at z < 1.2, so it is conditioned on the outcome and is **not** quoted.
- **R1: L323's trend is calibration-conditional.** A z-tilt of β = −0.05 dex/z in the baryonic masses, a factor 1.25 end to end over z = 0.6–2.5, brings ΛCDM's least-rising cell within 2σ of RC100. At β = −0.10 the framework is 2.7σ off. One galaxy sitting exactly at the inversion's f_DM = 0.02 edge moves RC100's slope by 0.41σ. KMOS3D shows the high-z inputs can carry a z-dependent baryon error, and its sign (baryons over-estimated at high z) moves RC100's data *toward* ΛCDM, if RC100's fitted masses share it.

**Standing:** L323's result survives every halo knob but not a baryon-calibration tilt of ~0.05–0.1 dex/z. It should be quoted as *conditional on the high-z baryonic-mass calibration*. What would decide it is high-z dark fractions from kinematics with per-galaxy gas masses (CO or dust), not scaling relations.

**Lean certificate for L332:** `fable_independent_2026/lean_2026/I23_rar_inversion_below_baryons.lean` (exit 0, zero `sorry`, standard axioms). It proves:
- the RAR kernel never weakens gravity (ν ≥ 1);
- a galaxy measured below its own Newtonian baryons cannot be fitted by any model that adds gravity, framework or halo (the logic of K1);
- the closed-form a₀ inversion of L320/L323 is exact;
- the inversion is defined only for g_b < g_obs, which is the selection that conditions T2 on its outcome.

## L345 — the two live fronts tested together: C-H/K cannot host the Λ-triggered carrier

`L345_chk_universal_carrier_pincer.py` (2/2; `MUTATE` switches to L321's additive coupling, L322's window reappears, rc = 1). Lean certificate `fable_independent_2026/lean_2026/I25_chk_universal_coupling.lean` (exit 0, zero `sorry`).

**Why it is universal.** C-H/K's MOND sector reads the total lapse, so a minimally coupled carrier is MOND-boosted exactly like baryons. This follows from L340's own scalar block, checked symbolically (U0) and in Lean (I25). L321's "additive" coupling therefore has no realisation in C-H/K. The only internal escape is a direct coupling of the carrier to C-H's auxiliary U with g_U = C. That coupling would have to track the field-dependent kernel.

**The scan.**
- X-COP overshoots 1.78–1.92× at 1000 km/s.
- It comes within 20% (after the non-thermal correction) only at v_k ≈ 2500–3000 km/s, where S₈ = 0.52–0.65.
- The scan used the monotone kernel, both footings, f_d(0) = 0.8–0.99 and v_k = 1000–3000 km/s.
- The S₈ floors are 0.767 (strict) and 0.748 (alternative).

**No cell passes under either pre-declared threshold set.** The parallel L341 (`g03_audit_2026/L341_chk_frw_gate`) had already found that C-H/K fails linear cosmology with the cold fluid the CMB needs (σ₈ = 18–27). This lane adds that its only live carrier cannot fix that at z = 0 either: clusters and S₈ pull the carrier's kick in opposite directions.

**What would save the pair (none is on the record):**
- a carrier coupled directly to U;
- a kernel that does not read the carrier's field (not C-H/K);
- a carrier absent from clusters at z = 0 but present at z = 2–3.

## L365 — the virialization-triggered carrier: a narrow window, decided by clusters

`L365_virialization_triggered_carrier.py` (4/4; `MUTATE`, in which the trigger never fires, fails T1 and T2, rc = 1). This lane builds spec item (3) of the 09-25 synthesis: a carrier that is cold in the web and the forest and leaves halos as they virialize.

**The setup.** A two-species particle-mesh cosmology (baryons plus the carrier, Newtonian gravity, as the kernel-invisible spec requires). A cold carrier particle decays at Γ = 10H once the bound-region variable x̃ ≥ (3/2)Ω_m δ (Lean I26) exceeds x_c, and receives an isotropic kick v_k.

**Result.** A window exists in S₈, the forest and halo clearing together. At x_c = 5 and v_k ≈ 700 km/s:
- S₈ is 0.928 of ΛCDM (strict floor 0.922);
- the flux power stays within 5.5%;
- dense cells keep 19% of ΛCDM's carrier at z = 2.

The window runs from about 560 to 720 km/s on the strict S₈ floor, or to about 800 km/s on the alternative:
- at 550 km/s the dense cells keep 0.31 (not cleared);
- at 850 km/s S₈ drops to 0.885.

Faster kicks clear halos but cost S₈ (0.65–0.87). Higher thresholds keep S₈ but do not clear halos. My pre-run hypothesis ("no window") was falsified by the widened grid.

**What decides it: clusters.** L354's cluster table scored the carrier decaying at z = 0 in the full-depth well, and needs v_k ≥ 1000–1200 km/s. For a local trigger that is a proxy of unknown sign: the carrier decays earlier in shallower progenitors, but the growing cluster (v_esc ≈ 2000–3000 km/s) can recapture daughters kicked at about 700 km/s. Cluster retention under the assembly history is the next computation.

**Limits.** 50 Mpc/h box on a 0.39 Mpc/h mesh; the MOND boost of baryons inside halos is not modelled; one realisation.

## L357 — the virialization-triggered carrier: the plain trigger fails once minihalos count; the vacuum-gated one opens a window

`L357_virialization_triggered_carrier.py` (8/8; `MUTATE` = the trigger never fires, V1 and D2 fail, rc = 1). Lean `fable_independent_2026/lean_2026/L357_L361_vacuum_gate_certificates.lean` (algebra only).

**The construction.** The carrier is kernel-invisible (L353) and decays where u = x̃ [Ω_Λ(z)/Ω_Λ,0]^p exceeds a threshold. Here x̃ is L351's shear-completed switch variable, and dropping the shear gives a lower bound on the triggered mass. The daughters are kicked.
- The decayed fraction that matters for large-scale power is bias-weighted. It is computed in a halo model: Sheth–Tormen, Dutton–Macciò NFW, a carrier cut-off of 10⁸ M☉, and escape of the daughters.
- Forest and S₈ use L319's solver. X-COP and the galaxy hosts use L321's phase-mixed retention with the decay confined to the triggered region. KiDS uses L355; RC100 and the flagship use L320.

**The plain trigger (p = 0) fails.**
- At its natural threshold, where every virialized halo decays, it takes 40–50% of the bias-weighted carrier out of the z = 2–3 forest. T²(k=5) = 0.30–0.64 at 700 and 3000 km/s, against a loose floor of 0.9.
- Where the forest does survive (x̃ ≳ 5000), cluster outskirts keep a full cold halo and X-COP overshoots (≥ 1.32).
- The parallel L365 triggers on the mesh-scale density. It finds a slow-kick window because halos below its resolution never fire. The two lanes bracket the plain trigger.

**The vacuum-gated trigger opens a window.** With p = 2 there are 3 strict cells and 17 alternative. The best cell decays where x̃ ≥ 2000 today, with v_k = 3000 km/s, and passes:
- the forest (T² ≥ 0.998);
- S₈ = 0.772;
- X-COP 1.08 / 1.13 (canonical / alt);
- the galaxy gate.

It works for two reasons. Rotation curves are measured at x̃ ~ 10⁴–10⁵ while cluster R500 sits at x̃ ~ 200–350. And a cluster that loses its core expands, so phase-mixed retention leaves ~0.55–0.6 of the carrier inside R500 at 3000 km/s.

**The price.** Galaxies at z ≈ 2.5 keep carrier outside their cleared cores:
- the deep-MOND Tully–Fisher zero point shifts +0.8 dex at z = 2.5 (framework alone 0.00, ΛCDM +0.33);
- RC100's inner dark fraction comes out at 0.43 against the data's 0.29 (RC100 is calibration-conditional).

**KiDS.** With the kernel reading the web's baryons it fails, as every carrier does. With the bound-region kernel (`g03_audit_2026/L361`) and the gated switch (`L359`), the assembled pair passes (`L360`, 70 of 96 pairs).


## L366 — cluster retention under the assembly history: a joint window at v_k ≈ 650 km/s

`L366_triggered_carrier_cluster_retention.py` (4/4; `MUTATE=2`, in which nothing escapes, fails R1, rc = 1). This is L365's construction in a 100 Mpc/h box (256³ mesh, 192³ particles per species), with the same trigger resolution and particle mass as L365 in 8× the volume. There are 22 halos with M(<1 Mpc/h) ≥ 10¹⁴ M☉/h. The carrier retention ε is measured within 1 Mpc/h at the same positions in every run.

**The cluster gate is two-sided**, as the record's X-COP criterion is (|M_dyn/M_HSE − 1| ≤ 0.2, non-thermal corrected, L354's table). It requires 0.286 ≤ ε ≤ 0.835 on the canonical footing and 0.220 ≤ ε ≤ 0.768 on the alternative.

| v_k (km/s) | S₈ / ΛCDM | forest | dense-cell carrier at z = 2 | cluster ε median (top 5) |
|---|---|---|---|---|
| 550 | 0.971 | 3.9% | 0.52 (not cleared) | 0.61 (0.75) |
| 600 | 0.963 | 4.2% | 0.33 (not cleared) | 0.50 (0.73) |
| **650** | **0.955** | **4.3%** | **0.22 (cleared)** | **0.32 (0.60)** |
| 700 | 0.945 | 4.4% | 0.17 | 0.21, undershoot (0.39) |
| 850 | 0.914 | 4.9% | 0.12 | 0.06, undershoot (0.16) |

**A joint window exists at v_k ≈ 650 km/s (roughly 620–690).** It passes S₈ strictly, the forest, halo clearing and both sides of the cluster gate, in one volume. The most massive halos (4–5×10¹⁴ M☉/h) keep 0.7–0.8.

**History, stated.** The first run of this script used a one-sided gate and the hypothesis that clusters recapture the carrier and close the window. That hypothesis was falsified: the median ε was 0.21 at 700 km/s. The gate was then made two-sided, as the record's criterion is, and the rerun hypothesis ("a joint window exists") was set before the rerun.

**Limits.**
- 0.39 Mpc/h mesh: galaxy-scale halos are not resolved.
- 1 Mpc/h aperture.
- L354's X-COP response is used as the map from retention to M_dyn/M_HSE.
- The MOND boost of baryons inside halos is not modelled.
- One realisation.

**Next, in order:**
- KiDS galaxy-scale retention at z ≈ 0.3 (L355 wants 20–30% of a ΛCDM halo);
- RC100's dark fractions at z ≈ 1–2.5;
- an action for the trigger, a decay rate tied to the foliation's bound-region scalar.

## L367 — cosmic shear for the triggered carrier: passes with the p = 2 kernel switch

`L367_triggered_carrier_cosmic_shear.py` (3/3; `MUTATE=1`, v_k = 0, fails S1, rc = 1). This reruns L366's box (same phases) to z = 0.5 and measures the carrier's **nonlinear** matter transfer T(k) = √(P_model/P_ΛCDM). T is compared with cosmic shear's bound T_max(k) from L364 (L363's region kernel on GP3's mock, R ≤ 1.2 on k = 0.1–1 h/Mpc, both footings).

| v_k (km/s) | T at k = 0.1 / 0.3 / 0.5 / 1.0 h/Mpc | p = 1 switch | p = 2 switch |
|---|---|---|---|
| 600 | 0.993 / 0.942 / 0.862 / 0.647 | fails | passes |
| **650** | **0.992 / 0.928 / 0.831 / 0.585** | **fails** (alt, +0.04) | **passes** (margin 0.10) |
| 700 | 0.990 / 0.913 / 0.796 / 0.527 | passes | passes |

The hypothesis was set before the run: at 650 km/s, p = 2 passes and p = 1 fails. It was confirmed. The ΛCDM twin gives T = 1 exactly.

**Informational.** Carrier retention at z = 0.3, within 0.5 Mpc/h of 10¹²–3×10¹³ M☉/h peaks, is 0.02–0.04. It is 0.26–0.44 for 3×10¹³–10¹⁴ peaks. Galaxy halos are sub-cell at this mesh.

## L368 — the full gate set: one cell passes everything

`L368_triggered_carrier_full_gate_set.py` (3/3; `MUTATE=1`, the no-kick limit, fails W1, rc = 1). Nothing is re-simulated. The script assembles the committed L366 and L367 numbers and adds KiDS with L360's machinery, loaded unedited: L352's switched phantom plus the carrier's halo, scaled by L367's measured galaxy-peak retention S. Every threshold is the record's.

| v_k | switch | S₈ | forest | cleared | X-COP ε | shear | KiDS Δχ² (can/alt) | all |
|---|---|---|---|---|---|---|---|---|
| 600 | p = 2 | 0.963 | 4.2% | 0.33 ✗ | 0.50 | ✓ | −6.0/−2.0 | no |
| **650** | **p = 2** | **0.955** | **4.3%** | **0.22** | **0.32** | **✓** | **−5.5/−2.2** | **yes** |
| 650 | p = 1 | 0.955 | 4.3% | 0.22 | 0.32 | ✗ | −19.5/−12.5 | no |
| 700 | p = 2 | 0.945 | 4.4% | 0.17 | 0.21 ✗ (undershoot) | ✓ | −5.1/−2.2 | no |

**v_k = 650 km/s with the p = 2 switch passes every gate on both footings:** S₈ (strict), the forest, halo clearing, the two-sided X-COP gate, cosmic shear with the phantom, and KiDS.

**How narrow the window is.**
- It is one grid cell. 600 fails clearing and 700 undershoots X-COP. The kick grid is 50 km/s.
- KiDS is **not monotone in S** for p = 2: +2.4/+5.4 at S = 0.2 (fails on the alternative footing), −8.5/−4.9 at S = 0.1.
- The pass therefore needs galaxy-scale retention ≲ 0.1. That is sub-cell here: S = 0.029 is measured at 0.39 Mpc/h mesh.

**Not established.**
- An action for the trigger (the decay rate is posited, not derived).
- RC100 beyond the z = 2 clearing proxy.
- Resolved galaxy retention.
- The MOND boost of baryons in halos.
- More than one realisation of one 100 Mpc/h box.

This is a candidate window at PM resolution, not a solved dark sector.

## L375 — the carrier around KiDS lenses, resolved: KiDS passes with the carrier's own profile

`L375_triggered_carrier_galaxy_retention.py` (4/4; `MUTATE=1`, v_k = 0, fails K1, rc = 1). L368's KiDS pass rested on a galaxy-scale retention (S = 0.029) measured on a 0.39 Mpc/h mesh, which is sub-cell for these halos. This lane resolves each KiDS host halo (L360's Moster+13 M₂₀₀ = 4.2×10¹¹ – 5.6×10¹² M☉) with a spherical shell model:
- self-consistent Newtonian gravity: the carrier is kernel-invisible, so by L353's reciprocity theorem it feels no phantom;
- secondary infall on a Wechsler-form mass-accretion history (α = 0.75, bracketed by 0.5 and 1.2);
- the bin's fitted baryons plus a CGM;
- L365's trigger, unchanged: decay at Γ = 10H where the local x̃ > 5, then an isotropic kick.

The carrier's **own** z = 0.25 profile is projected with L352's projector and scored with L360's machinery.

| variant | S (<0.5 Mpc/h), bins 1–4 | undecayed part | KiDS p = 2 (can/alt) |
|---|---|---|---|
| fiducial, 650 km/s | 0.26 / 0.25 / 0.23 / 0.35 | 0.18 / 0.17 / 0.16 / 0.23 | **−11.5 / −8.4** |
| α = 0.5 | 0.20 / 0.19 / 0.18 / 0.27 | | −10.4 / −6.9 |
| α = 1.2 | 0.32 / 0.31 / 0.30 / 0.47 | | −13.8 / −9.4 |
| baryons static | 0.26 / 0.25 / 0.23 / 0.36 | | −11.5 / −7.2 |
| 600 / 700 km/s | ≈ fiducial | | −11.5 / −8.3, −11.4 / −8.5 |

**Two findings.**
- **Retention is ~8× higher than the mesh measured**, and it is mostly *undecayed* infalling carrier. The trigger reads the local total density, so once a halo's carrier has left, the outskirts fall below x̃ = 5 and newly accreted carrier stops decaying. The trigger limits itself. That is also why S barely depends on v_k.
- **KiDS passes anyway, in every variant, on both footings.** The retained carrier sits at r ≳ r₂₀₀, not in an NFW cusp. L368's non-monotone S-scan, which failed on the alternative footing at S = 0.2, scaled a full NFW profile. That was the wrong shape for this construction.

Controls:
- C1: the same halo with the decay off is rejected by KiDS (+144/+147), so the pipeline sees a retained halo.
- C2: a static NFW in Jeans equilibrium holds M(<r_s) to within 6% over 5 Gyr.
- MUTATE (v_k = 0): +150/+153.

**Limits.**
- Spherical symmetry: no mergers, no triaxial orbits.
- A smooth accretion history.
- One lens redshift.
- The trigger is still posited, with no action.

L368's KiDS verdict stands, and it no longer rests on a sub-cell number.

## L376 — inside galaxies, resolved: the carrier is gone (RAR and RC100 gates pass)

`L376_triggered_carrier_inner_galaxies.py` (5/5; `MUTATE=1`, v_k = 0, fails R1 and R2, rc = 1). L375's shell model is generalised to any host and observing redshift. C1: it reproduces L375's committed S exactly (0.246533). In the construction the phantom supplies rotation-curve "dark matter", so any carrier left inside adds on top and moves galaxies off the RAR.

- **RAR, z = 0** (gate: carrier shift of log g_obs ≤ 0.057 dex, the RAR's intrinsic-scatter bound, at 2/4/8 R_d, both footings). Hosts: dwarf 10¹¹ / 3×10⁹, Milky Way 10¹² / 6×10¹⁰, massive 5×10¹² / 2×10¹¹ M☉.
  - At 650 km/s the worst shift is ≤ 1.2×10⁻⁴ dex.
  - With the decay off it is 0.17–0.26 dex (C2: the gate has teeth).
- **RC100, z = 1 and 2** (10¹² host, M_b = 10¹¹, R_e = 5.4 kpc).
  - The carrier inside R_e is 0.000 of ΛCDM's (gate 0.30). This replaces L365's z = 2 dense-cell proxy with a resolved number.
  - f_DM(<R_e) = 0.23 (canonical) / 0.26 (alt), all phantom, against 0.42–0.45 for a ΛCDM carrier.

**Why the interiors are empty.** Inside a galaxy the baryons alone keep x̃ > 5, so every carrier element there decays. A 650 km/s daughter far exceeds the post-decay escape speed (~230 km/s at 10 kpc for the Milky-Way host).

**The trigger used here is the least-trigger estimate.** Its x̃ is matter only; the geometric x̃ also contains the phantom and the shear (L342, L357), which only add decays. So these interior results can only strengthen. The same point runs the other way for clusters, noted below.

**Open, and named.** The phantom-inclusive trigger lowers cluster retention. The window's X-COP margin is thin (0.32 against 0.286, L366), so the next computation is the full construction in the particle-mesh runs: the switched phantom sourced by the baryons, felt by the baryons, and read by the trigger.

## L369 — the window does NOT survive other realisations (both hypotheses falsified)

`L369_triggered_carrier_window_realisations.py` (2/4, **rc = 1: both pre-declared hypotheses falsified**). L366/L367's construction, unchanged, in three 100 Mpc/h realisations: seeds (7, 11), which are L366's own, plus (17, 21) and (29, 33). Kicks run over 600–700 km/s in 25 km/s steps. Every gate is computed per box and on the pooled sample (3×10⁶ (Mpc/h)³, 71 halos ≥ 10¹⁴ M☉/h).

C1: the (7, 11) reruns reproduce L366's and L367's committed numbers **exactly** (zero deviation over 32 numbers).

| v_k | pooled S₈ | pooled forest | pooled cleared (≤ 0.30) | pooled X-COP ε (0.286–0.768) | shear p = 2 |
|---|---|---|---|---|---|
| 600 | 0.960 | 4.0% | 0.51 ✗ | 0.51 | ✓ |
| 625 | 0.955 | 4.1% | 0.44 ✗ | 0.44 | ✓ |
| 650 | 0.951 | 4.2% | 0.39 ✗ | 0.34 | ✓ |
| 675 | 0.946 | 4.3% | 0.34 ✗ | 0.27 ✗ | ✓ |
| 700 | 0.940 | 4.3% | 0.31 ✗ | 0.23 ✗ | ✓ |

- **The full window exists only in the original box** (7, 11), at 625 and 650 km/s. Box (17, 21) has none: clearing is 0.57–0.72. Box (29, 33) has none: clearing passes only where X-COP undershoots.
- **The pooled sample has no window, so L368's "one cell passes everything" was a one-realisation artefact.**
- **Box-to-box scatter is large in both gates that close the window.** The dense-cell clearing at z = 2 is 0.22 / 0.66 / 0.28 at 650 km/s. The cluster median is 0.25–0.59 at 650.
- **Pooled, the gates pinch from both sides.** Clearing needs kicks above 700 km/s; X-COP needs kicks below ~660 km/s.

**Two readings, stated separately.**
1. **As gated, the window is closed.** These are the record's gates, unchanged.
2. **The gate that fails at every kick is G3, a mesh proxy.** It is the carrier in cells with 1 + δ > 50 at z = 2, on a 0.39 Mpc/h mesh. Its stated purposes were RC100's dark fractions inside R_e and KiDS's 20–30% of a ΛCDM halo (L365). Both have since been resolved and pass: L376 finds 0.000 inside R_e at z = 1–2, and L375 finds KiDS −11.5/−8.4. If G3 were retired in favour of those resolved gates, the pooled sample would pass S₈, the forest, X-COP and shear at 600–650 km/s. **That retirement is a judgement made after seeing G3 fail, not a result.** It needs its own pre-declared test before anyone may claim a window.

MUTATE was not run. The main run's hypotheses were already falsified (rc = 1), so a control that forces the window closed has nothing to discriminate. The C1 reproduction is the control that matters here, and it is exact.

## L377 — the full construction on the mesh: the phantom RAISES cluster retention (hypothesis falsified, in sign)

`L377_full_construction_pm.py` (4/5, **rc = 1: the pre-declared hypothesis is falsified**; `MUTATE=1`, phantom off, reproduces L369 exactly, shift ×1.000, and fails R1 as designed). This is the first run of the whole construction on the mesh, on L366's box and seeds:
- L359's p = 2 vacuum-gated switch, on the matter-only branch;
- L340's ν_mono, rebuilt identically (C2: zero deviation from L352's table);
- a switched QUMOND phantom sourced by the baryons' Newtonian field and **felt by the baryons**;
- a carrier that feels Newtonian gravity only (L353);
- a trigger reading the **phantom-inclusive** x̃ (L342/L357).

C3 checks the mesh QUMOND on a spherical blob inside a switched sphere: it returns ν·g_N to within 4.5 / 2.5 / 1.2% at 1 / 2 / 3 Mpc/h. C1 reproduces L366's ΛCDM exactly.

**History.** The first design asked whether the seed-(7, 11) window survives the phantom. L369 then showed that window is a one-realisation artefact. The main run was stopped 80 s in, before any result, and the lane was redesigned. It now measures each gate's shift against L369's matched Newtonian runs. The hypothesis, set before the rerun, was that the phantom lowers cluster retention at every kick.

| v_k | X-COP ε: Newtonian → full | cleared (z = 2) | S₈ | pooled estimate (shifts applied to L369's pooled gates) |
|---|---|---|---|---|
| 600 | 0.495 → 0.527 (×1.06) | 0.335 → 0.335 | 0.963 → 0.969 | cleared 0.51 ✗, ε 0.54 |
| 625 | 0.401 → 0.446 (×1.11) | 0.264 → 0.264 | 0.959 → 0.965 | cleared 0.44 ✗, ε 0.49 |
| 650 | 0.318 → 0.358 (×1.12) | 0.223 → 0.223 | 0.955 → 0.961 | cleared 0.39 ✗, ε 0.38 |
| 675 | 0.239 → 0.288 (×1.20) | 0.195 → 0.195 | 0.950 → 0.956 | cleared 0.34 ✗, ε 0.32 |
| 700 | 0.212 → 0.258 (×1.22) | 0.171 → 0.171 | 0.945 → 0.951 | cleared 0.31 ✗, ε 0.28 ✗ (both within 0.01) |

- **The hypothesis is falsified in sign: the phantom *raises* cluster retention by 6–22%.**
  - The phantom in the trigger alone does almost nothing: the trigger-only run at 650 gives ε = 0.32 against 0.318. Cluster cores are already far above x̃ = 5.
  - The rise comes from the **baryons feeling the phantom**. They settle deeper into cluster wells, and that deepens the Newtonian potential the carrier feels.
  - L376's worry that the phantom-inclusive trigger lowers cluster retention was wrong in effect. I27's theorem (more cells fire) is still true; it just doesn't matter in cluster cores.
- **Clearing at z = 2 is untouched**, identical to four digits: the p = 2 gate keeps the phantom off at z = 2.
- **S₈ rises by 0.6%.** With no decay, the phantom alone gives S₈ ×1.009 and fails cosmic shear, as expected.
- **Single-box (7, 11) window: 625–675 km/s on both footings.** L369 shows single-box windows do not survive pooling.
- **The pooled estimate with the shifts applied is still no window.** Clearing, the G3 mesh proxy, stays the blocker. At 700 km/s both clearing (0.31) and X-COP (0.28) miss by under 0.01, so the construction pushes the pinch toward closing without opening it.
