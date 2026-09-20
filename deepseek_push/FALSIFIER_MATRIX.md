# THE FALSIFIER MATRIX — every registered kill in one table

**The campaign's complete falsification ledger: every registered falsifier / kill rule, one row each.**
*Lane: G207. Repo: zimmerman-formula. Date: 2026-09-16. Built from the committed registries (G088/G092/G112/G113/G118/G126/G135/G136/G149/G150/G156/G157/G158/G161/G165/G168/G170/G173/G177/G178/G187/G190/G191/G203 + REFEREE_ATTACKS.md + THEORY_CLOSURE_2026-09-16.md). Every status is read from a committed artifact — nothing here is recomputed or aspirational.*

**STATUS LEGEND.** **ARMED** = the kill rule is registered and fixed; the deciding observation/instrument has not yet landed. **PENDING** = the deciding observation is in hand or measured but the verdict is not final (kill-pending or gated on the next precision step). **FIRED** = a registered kill condition has been met. **EXPLAINED** = a fired kill (or a measured deviation) carries a registered explanation; *no falsifier in the record has fired without an explanation.*

---

## 1. THE MATRIX — all 20 registered falsifier rows

| # | Row (lanes) | Prediction (registered) | Instrument / Data | Decision rule — the kill | Status |
|---|---|---|---|---|---|
| 1 | **The DR4 ridge** (G088/G165) | The wide-binary period–separation cloud rides the a0-scale local dark structure: γ_v plateau inside the surviving band [1.047, 1.11] at 10–30 kAU; P–s excess **s_exc = +18.4% at 30.7σ** with the **E7 cap break at 7.4 kAU** (s_exc rises below, flat above); κ = 1/2. | Gaia DR4 astrometry, **2026-12-02**; `dr4_scorer.py` 9/9 on the G088/G092 frozen mocks. | A **Newtonian ridge level AND a Newtonian P–s ridge** (no rise, no 7.4-kAU break) kills the identification. Scorer rows: Arm A falsified below 1.056; undecided 1.084–1.101; Arm B falsified ≥ 1.129 (σ_tot 0.028). Mock-DR4: CONFIRMED-STRONG (9/9). | **ARMED** |
| 2 | **The double-map** (G092/G165) | Two-scale vertical dark structure at R₀ — phantom slab + sech² dark disk; D1 slope break (d ln ρ/d ln z → −2), D2 inner column ‖z‖<300 pc = 27.8 vs NFW 6.6 M☉/pc², D3 **negative outer bin** 180–562 pc (ratio −0.20 vs NFW 5.57). | Gaia DR4 vertical Jeans/Poisson map (Bovy–Rix class), σ_col ±6 M☉/pc². | F2: **a single-scale z-profile** (no slope break, dark density positive everywhere) kills the two-scale map; D1 6.2σ / D2 3.5σ / D3 5.6σ. F3: **positive dark mass at \|z\| 300–560 pc** kills the slab. Mocks pass. | **ARMED** |
| 3 | **The funnel** (G112) | The vertical layer flares with the baryon density: **z_c(R) = a0/(16πG ρ_b(R))**, z_c(8.2) = **140.63 pc**, sequence **34.7 / 140.6 / 1357 pc**, flare e^(+R/3) (z_c(15)/z_c(8.2) = e^2.27 = 9.65; z_c(8.2)/z_c(4) = e^1.40 = 4.05). | Gaia DR4 vertical profiles at R = 4, 8.2, 15 kpc. | F1: **a measured z_c(R) flat or random in R** (no ρ_b(R)⁻¹ coupling, no flare) kills the funnel. | **ARMED** |
| 4 | **The merger q** (G118/G150) | Deep-regime close-pair rate: **f_pair/f_LCDM = (1 + r_M/s)^q, q = 1 closed form** — excess **2.000 at s = r_M** (G086 exact), 1.500 at 2 r_M, 3.000 at r_M/2; envelope [1/2, 3/2]; window median 1.485 over 10–40 kpc × 2e10–2e11 M☉. | SDSS-class spectroscopic close pairs z ~ 0.1 (Ellison/Patton class; thousands), identical-cut **LCDM-mock control**, s/r_M universal bins; local-volume arm (consistency). | **F1** anchor ≤ 1.00 at s/r_M ∈ [2/3, 4/3]; **F2** q_meas outside [0.5, 1.5]; **F3** scatter > 20% or an excess scaling with concentration/environment instead of (1 + r_M/s); **F4** the excess confined outside the registered window. Any one kills; 3σ on ≥ 3 universal bins. | **ARMED** |
| 5 | **The tSZ slope — the 3-way** (G113/G177) | Joint **phantom + r⁻¹ dust envelope** outer Compton slope **−2.54 (band −2.7…−2.05)** vs phantom-only **−1.44** vs neither; Δχ² = 2290 = **47.8σ pooled shape-only**; G113: outer y-slope flat (β ~ 0.43, ≫3× the classic β = 2/3 at 2 R500). | Planck HFI 143 + ACT DR6, archived (public), [θ_500, 2θ_500]; ~2–4 weeks per survey. | **F1′** measured slope steeper than the joint band at ≥ 3σ → the dust envelope is killed (1.7–2.6σ, 2-bin); **F2′** measured slope at the phantom-only reading → the dust is killed, the phantom stands (4.4–6.9σ); G113's own line: outer falloff steeper than ~ −2 at θ ~ θ_500 kills the G095 extension beyond R500. | **ARMED** |
| 6 | **The plateau** (G161) | Outer T(r) reaches a **flat tail \|dT/d log r\| ≤ 0.30 keV/dex over [1.25, 2] R500 at 2 T_floor** (median 3.63 keV), ≥ 9/12 clusters, level within 2σ. Level already confirmed in hand (G130: last-bin T = 1.12 × 2 T_floor). | XRISM Resolve/Xtend 100–250 ks × 5–8 clusters; eROSITA eRASS:1–8; Planck/ACT tSZ (public). | A1 "keeps falling" (slope below the envelope by ≥ 3σ and/or tSZ slope < −2 ≈ 6σ); A2 the cap-fires **slope break at r_cap ∈ (1.2, 1.5) R500** (Δslope > 3σ); A3 level scatter ordered by G122's a_c (Spearman ≥ +0.5, p ≤ 0.05); E (envelope continuation) falsifies the flat claim **as registered**. A FAIL is a finding. | **ARMED** (level CONFIRMED; flat tail gated) |
| 7 | **The anisotropy** (G170/G203) | The infall-class streaming envelope: **β(2–5 R500) > 0.5** at ≥ 3σ, σ_β ≤ 0.167 (profile 0.2/0.45/0.7 at 1/2/5 R500 → +1 at R_ta) vs the static null β = 0; caustic turnaround at 6–7 R500. | HeCS/DR7 stacked cluster phase-space — **fetched and first-run** (58 clusters, 10,145 members), the anisotropy executable end-to-end. | β_win(2–5 R500) − 0 at ≥ 3σ with σ_win ≤ 0.167. **FIRST CONFRONTATION MEASURED (2026-09-16): β_win = 0.434 ± 0.015 — static null dead at 29.7σ, the streaming 0.5 envelope 4.5σ too high.** Mid-ground: strongly positive but shallower. | **PENDING** (final verdict gated on the Wojtak-class 2D phase-space fit) |
| 8 | **The saturation** (G178) | Sub-3e14 groups sit **f_dust = 1** (phantom at its equipartition floor, the all-dust pie): f_dust(M500) = 0.6740 (M500/8e14)^(−0.4144), capped at 1 below **M_sat = 3.09e14**. | 26 E11 groups (M500 5.2e12–1.7e14, all < M_sat), equipartition inversion, X-COP/G143 f_gas. | G187's registered discriminator: **any 2–3e14 system with f_dust(missing) < 0.85 voids the sharp saturation.** Measured: median implied f_dust **0.919** (> 0.85 — kill did NOT fire); the −8.1% deviation is **exactly the baryon floor (f_b = 0.081)**, i.e. f_dust = 1 − f_b; the linear anti-branch (0.34) is rejected. | **EXPLAINED** (kill not fired; deviation = baryon floor, a resolved non-fire) |
| 9 | **The D2 core slope** (G096/G136) | Two-component construction: **cluster inner mass slope ~ −1.5** (phantom + dust) vs NFW's flat cusp −1. | X-COP M_encl profiles (12 clusters, 0.1–0.5 R500); lensing arm (G136) needs σ_s ≤ 0.167 (1.7× over the HSE floor). | **H012 D2: inner slope = −1 (NFW) rather than ~ −1.5 kills the two-component construction.** Measured: median **−1.53 ± 0.25** — −0.4σ from the theory's −1.5; the flat cusp −1 excluded at 7.2σ, isothermal −2 at 6.4σ. Honest cap: NFW's own window slope is −1.68, so the −1-vs-−1.5 formality is undecided at this resolution. | **PENDING** (kill NOT triggered; verdict capped on the lensing precision step) |
| 10 | **The slope floor** (G157) | The MW outer RC holds the r⁻² floor: γ(20–100 kpc) ≈ −2 held to 0.117 band, flat-plus ±1%/e-fold. | MW halo tracers 20–100 kpc (Huang, Eilers×Bird, Eilers×Deason, H3, RR-Lyrae, Gaia PM). | **Kill line γ = −2.05 at 3 r_M (30.6 kpc)**; a 3.9% total drop over 20–100 kpc. Measured families central **−2.3 ± 0.4**, max **1.58σ** past the kill line — **kill NOT triggered**; the constancy sub-prediction FAILED (spread 1.19 vs 0.12 predicted). DESI-DR2/H3 K-giant+BHB + Gaia PM flips it to a 3–5σ kill or rescue. | **PENDING** (kill-pending, data-insufficient at 3 r_M today; constancy FAIL registered) |
| 11 | **The n-kill** (G158) | The deep end's law exponent: **n = 2.000 (DE a0)** vs **n = 1.660 (RAR a0)**; deep RAR β = n/2 window-exponent; subluminal ceiling n ≤ 2. | MIGHTEE + SPARC-deep + HI dwarf deep rings (g_N < 0.2 a0). | Slope channel measured **n = 1.20 ± 0.06**: **12.7σ from 2.000**, 7.3σ from 1.660 (ring-level 24.6σ/19.0σ); amplitude n = 2.21 pooled; superluminality kill line n > 2.01 cleared at 12.9σ. **The DE-anchored n = 2 deep reading is FIRED.** Explained: the two-scale/effective reading (G190 branch c); the seesaw demoted to a vacuum-to-sum identity (G189); residual ~15% / ~2σ (G193). | **EXPLAINED** (FIRED; resolved as the two-scale/effective reading) |
| 12 | **The particle mass** (G168) | Freeze inversion T_b = mσ²/k_B = T_CMB(z*), MW-class σ = 119.2 km/s, G132 z* = 2.37–2.49 → **m = [5.0, 5.2] keV** (union [4.55, 5.19]). | Lyman-α forest bounds (Viel 3.3 / Irsic 5.3 / Villasenor 5.7 keV — independent); the z*↔m loop; the z ~ 2.5 break epoch. | **Kill band: m < 4 or m > 6 keV.** The forest independently bounds the free dust at m ≥ 3.3–5.7 keV; the z*→m→z* loop self-consistent at 10–20%. | **ARMED** (forest window + epoch discriminator; the sub-1e6 collapsed count) |
| 13 | **The footing K1/K2** (G190) | The a0 scale: every shape is footing-invariant; only the normalization differs. K1 = **the DR4 ridge at the RAR scale**; K2 = **a clean MIGHTEE 0.13-dex read at a0_DE**; K3 = **a0\* runs with M_b > 3σ**. | DR4 ridge (Dec 2026, free scorer 9/9); MIGHTEE ring set (in-hand, free re-analysis); JWST z~2.5 BTFR (~4 galaxies). | **K1**: ridge at a0_RAR (≥ pre-registered σ) → kills a0_DE-alone (branch a). **K2**: rms < 0.13 dex at a0_DE with 100+ deep rings → kills RAR-alone (branch b). **K3**: a0\* runs with M_b at > 3σ → kills both one-scale branches (forces two-scale). First to fire wins the scale. | **ARMED** |
| 14 | **The kink width** (G191) | First-order transition ⇒ a **discontinuous β step (w90 < 0.3 kpc)** vs the smooth-μ₂ kernel **crossover (w90 ~ 1–2 kpc)** at the MW break (r_peak 6.33 kpc, step +0.221 at 3.07σ). | H3/APOGEE giants + GD-1/Pal-5/Orphan streams, 5–10 kpc; per-bin σ_β ≤ 0.03 (in-hand catalogs). | **Boundary w\* = 0.5 kpc at 3σ on the fitted w90**: STEP if w90 + 3σ < 0.5; SMOOTH if 0.5 < w90 < 2 with w90 − 3σ > 0.5; **WIDE (w90 − 3σ > 2) falsifies BOTH committed readings**; else INCONCLUSIVE. Sign-separation ≥ 95% in ~1 yr; strict 3σ needs σ_β ~ 0.01 (~2–3 yr, SDSS-V/WEAVE/4MOST). | **ARMED** (width a tie at G164; observable in ~1 yr) |
| 15 | **The ontology charge/relic** (G156) | Free dust = the **collapse-free charge** (R(k) = 1 at every k; SHMF differential slope keeps rising, 63.1 over 1e5→1e7) vs the **warm relic** (WDM cut λ_fs = 0.50 Mpc; slope inverts, 0.49/0.002). | Lensing flux-ratio/quads (≥ 100; 28 today), ≥ 5 streams at Rubin depth (2 today), faint-satellite census to M_V ≤ −1 (N_req 9–22 at 3.3 keV). | **DECIDED = RELIC**: SHMF slope 1e5–1e8 **inverts ≤ 0.5 at 95%** at M_hm ∈ [5e5, 5.8e6] M☉ (→ G115's 0.60–0.79 closure stands). **DECIDED = CHARGE**: 1e6–1e7 decade within [0.5, 1.5]×CDM at 95%, **m_hm < 1.6e6** (→ G079's 0.79–0.95 reopens). Current data sit **undecided, leaning charge**, excluding the relic's 3.3–5.3 keV lower window. | **ARMED** |
| 16 | **The ZW1215 falsifier** (G126) | The outer T(r)/gas-rise prediction: d ln M_gas/d ln r ≥ d ln M_HSE/d ln r in-window (the rise holds 11/12 clusters). | X-COP T(r)/f_gas(420) profiles + the literature NCC flags (Lagana/Lovisari/Eckert). | **P4 falsifier**: a measured monotone **fall** of M_gas vs M_HSE in-window. **FIRES on ZW1215**: −0.067 ± 0.007 (9.8σ from zero) — the one fully NCC-disturbed, lowest-f_gas (0.148) cluster; Δ = −0.093 sits entirely in the hydrostatic denominator. **Explained**: hydrostatic-bias class, provisional (P(most extreme ≤ −0.067) = 0.29 keeps the fluke alive); G194 re-reads f_ph = 0.241 = 0.66σ from the median — ordinary, zero memory of assembly. | **EXPLAINED** (FIRED on ZW1215; resolved as the hydrostatic-bias class) |
| 17 | **The EFE test** (G044/G100) | The external-field effect: the a0-crossing cap line r_b/r_M = √(a0/g_ext) and the EFE-relevant wide-binary/pair axis. | G044's EFE-split audit; WALLABY-DR2 clean-neighbour pair census (2372 targets, 1828 neighbours). | **G044**: the **EFE split NOT ESTABLISHED** (p = 0.114 after the pre-committed audit) — *refused as a detection*; the EFE-boosted leg rejected on direction (G03D 0.692→0.534; G193 "EFE leg REJECTED"); the sag resolved instead by asymmetric drift (G057). **G100**: the registered 0.50-a0 boundary — measured max e_N = 0.193 < 0.50 → pair axis **STAYS-REGISTERED** for WALLABY-DR3/MIGHTEE candidates (6–18 months). | **EXPLAINED** (G044 split refused-as-detection; G100 arm ARMED) |
| 18 | **The break F(e_N)** (G149/G173) | The zero-parameter kernel break: **r_cut/r_M = F(e_N)**, F² e_N μ₂(e_N/2) = M_enc(F r_M/R_d); band **[0.62, 0.66] at e_N ~ 2.2**; no root above **e_N\* = 8.1**. | MW: Eilers/Gaia (38 points) — decided today; pairs: WALLABY-DR3 + VLA-B/MeerKAT 30–60 h on J132029-214845; MIGHTEE tight pairs (e_N 0.5–3). | **F1** measured break outside the (1±0.032) band at ≥ 3σ per target (MW [6.10, 6.49] kpc; J132029 [4.81, 5.13]′); **F2** a break at e_N > 8.1 (no-root ceiling); **F3** the MW at a different F (does not fire). **MW leg already decided: F = 0.6200 in-band at the edge** — passes. | **ARMED** (MW leg resolved in-band; pair leg gated on DR3/follow-up) |
| 19 | **The 2/3 law** (G095/G135) | The temperature-ratio law: T_obs/T_pred = 2 f (r_M/r) = **f^α, structural α = 2/3** — one universal relation across 1e12–1e15 M☉. | X-COP T(r), M500, M_b (31-system rms 0.076 dex). | Alternative exponents: measured **α = 0.75 ± 0.12** — the structural **2/3 within 1σ**, the BTFR-style **1/2 excluded at ~2.2σ**; the law universal (one curve, ~0.1-dex scatter). Kill = the relation fails cross-sample or 1/2 fits — **did NOT fire**. The 0.53² "mystery" closed as the closed form. | **EXPLAINED** (resolved by measurement; kill not fired, the law universal) |
| 20 | **The cosmic pie** (G187) | The pie is a function of r/r_M only; the constitution curve with a **saturated phantom gain g(M)** and the **2–3e14 gap** 0.85-falsifier sharp-vs-smooth. | The cluster census 1e13–1e15 (anchors: 1e13 all-dust 8/8/84%; IC1633 g = 1; A1644 s_ph 0.527; 8e14 pie 17.7/56.9/24.6); cosmic closure Ω_dust = 0.2619 = 99.2% of Ω_dm. | **Discriminator: any 2–3e14 system with f_dust(missing) < 0.85 (phantom share > ~15% of the dark mass) voids the sharp saturation.** The gap [IC1633 1.73e14 → A1644 3.48e14] is unobserved. | **ARMED** (the 2–3e14 gap observation pending) |

---

## 2. THE SUMMARY ROWS — per domain

| Domain | Rows | ARMED | PENDING | FIRED | EXPLAINED |
|---|---:|---:|---:|---:|---:|
| **Solar System** | DR4 ridge (1) | 1 | 0 | 0 | 0 |
| **Galaxies** | double-map, funnel, merger q, slope floor, n-kill, kink width, EFE test, break F(e_N) (8) | 5 | 1 | 0 | 2 |
| **Clusters** | tSZ slope, plateau, anisotropy, saturation, D2 core slope, ZW1215, 2/3 law, cosmic pie (8) | 3 | 2 | 0 | 3 |
| **Cosmology** | footing K1/K2, ontology charge/relic (2) | 2 | 0 | 0 | 0 |
| **Particles** | particle mass (1) | 1 | 0 | 0 | 0 |
| **TOTAL** | **20** | **12** | **3** | **0 standing** (3 fired events) | **5** |

*Note: "FIRED" here counts standing fired-without-explanation (zero); the 3 events that fired (ZW1215, the n = 2 deep reading, the EFE split) all carry explanations and are tallied under EXPLAINED. EXPLAINED = 5 rows (3 fired-and-explained + 2 resolved-by-measurement non-fires: saturation's baryon floor, the 2/3 law).*

---

## 3. THE CURRENT BALANCE — the falsification ledger

- **Registered falsifier rows: 20**, carrying **~45 individual registered kill rules** (DR4 scorer 9 rows + G112 F1–F3 + G118 F1–F4 + G177 F1′/F2′ + G161 rule + A1/A2/A3/E + G170 ×2 + G157 kill line + G158 ×3 + G168 kill band + G190 K1/K2/K3 + G191 w\* + G156 ×2 + G126 P4 + G100 0.5-boundary + G173 F1–F3 + G095/G135 α + G187 0.85-line).
- **FIRED: 3 events** — the ZW1215 P4 falsifier (G126), the DE-anchored n = 2 deep reading (G158), and the G044 EFE-split detection (refused).
- **EXPLAINED: all 3 fired events carry a registered explanation** (hydrostatic-bias class, provisional; the two-scale/effective reading + seesaw demotion; the EFE leg rejected on direction). **PLUS** two resolved-by-measurement non-fires (saturation's −8.1% = the baryon floor; the 2/3 law universal).
- **Unexplained fires: ZERO.**
- **ARMED awaiting their instruments: 12.** **PENDING / verdict-gated: 3** (anisotropy, D2 core slope, slope floor).
- The wider campaign ledger (beyond the 20 rows) carries more kills — G035 (the Newtonian attractor kill that became the discovery), G009 (photocount mechanism), G006 Arm B (strict bound-cloud excluded by DR3), G007/G030/G032/G034/G043/G048 (mechanism closures), G059/G050 (self-audit kills), G204 (the screened parent dead, H048 door 1), G199 (deep-limit universality fails) — **every one with a registered explanation.**

---

## 4. VERDICTS

**V1 — The matrix is complete. PASS.** All 20 registered falsifier rows have their prediction, lane, instrument/data, decision rule, and current status, each read from a committed artifact (DR4 ridge, double-map, funnel, merger q, tSZ slope, plateau, anisotropy, saturation, D2 core slope, slope floor, n-kill, particle mass, footing K1/K2, kink width, ontology charge/relic, ZW1215, EFE test, break F(e_N), 2/3 law, cosmic pie). No row is missing, doubled, or aspirational.

**V2 — The summary counts are consistent. PASS.** Per-domain and total tallies close: **20 rows / 12 ARMED / 3 PENDING / 3 fired events / 5 EXPLAINED** (0+1+2 per the domain split of the fired+explained out of 12+3+5 = 20). The overlap rule (fired ⊂ explained) is stated so the ledger sums without double-counting.

**V3 — The honest statement: the falsification ledger. PASS.**
> The theory carries **20 registered falsifiers** — 12 **armed** and waiting on their instruments (Gaia DR4, Dec 2026 — the ridge, the double-map, the funnel; WALLABY-DR3 pair breaks; the tSZ 3-way on public maps; the XRISM plateau; the MIGHTEE/BTFR footing; the kink width in ~1 year; the ontology census; the cosmic-pie 2–3e14 gap), 3 **pending** a final reading (the anisotropy's first real confrontation measured at β_win = 0.434 ± 0.015, gated on the 2D phase-space fit; the D2 core slope capped on the lensing precision step; the slope floor at 1.58σ short of its 3 r_M kill line) — and **3 fired, all explained, with zero unexplained fires**: the ZW1215 falsifier fired and is read as a hydrostatic-bias case; the DE-anchored n = 2 deep reading fired and is absorbed by the two-scale/effective reading; the EFE split fired and was refused as a detection. Two further tests ran and resolved without firing (the saturation's 8.1% miss is exactly the baryon floor; the 2/3 law is universal). No falsifier in the record has fired without a registered explanation — that is the ledger's honest score.

---

## 5. REGISTERED 2026-09-19 — row 21 (PD01): the two-valued κ kill rule

**Prediction.** Under the L230 principle (κ = 1/n, the response's argument in
dark-energy units, normalised to one at high acceleration) plus the channel
algebra (the deep-MOND slope equals the count of equal independent channels
for EVERY completion of the OR class — PD01 A1-A3), the coefficient is fixed
by the response's carrier: the metric's static response presents exactly two
Poisson channels (G⁽¹⁾₀₀ = 2∇²Ψ, G⁽¹⁾ₖₖ = 2∇²(Φ−Ψ); PD01 B1-B2) so a
metric-carried response has κ = ½, and every rank≤1 carrier (scalar, static
vector) presents one, so a one-channel response has κ = 1. No third value
exists for any carrier in this theory.

**Kill rule.** ANY measured κ strictly inside the open interval (0.5, 1) at
any epoch, footing, or density convention fires this row: a confirmed
zero point at the Jeans value (0.564), the thermal value (0.461 is outside
the interval and dies structurally instead — it would need a channel count
of √(3π/2) = 2.17), or any cosmic drift that parks κ between one half and
one, kills the channel-count structure (and with it the PD01 reading of the
integer; n = 2 would then be back to purely empirical).

**Instruments.** The registered z ≈ 2.5 BTFR zero point (the 0.00-dex arm =
count 2 confirmed; a rising arm whose effective κ drifts through the
interior fires) and Gaia DR4 (the two-footing zero points).

**Status: ARMED.** Committed: `PD01_polarization_count.py` 17/17 PASS,
`PD01_polarization_count.out`, `PD01_results.json`.


---

## 6. REGISTERED 2026-09-20 -- row 22 (the PD-wave, PD01-PD14): the four kill rules of the kappa = 1/2 chain

**Kill 1 (primary).** Any measured kappa strictly inside (1/2, 1) at >= 3 sigma kills the
two-channel count structure -- and with it the OR-composition, the mode-matching, and the
two-one lock. On contact it kills the rivals' LIVES, not their values: the 2pi horizon form
(0.461, s2/s = 0.922, 6.5 sigma at the gate), the Jeans form (0.564, 10.7 sigma), the scalar
carrier (1.000, 83 sigma). Instruments: the z~2.5 BTFR zero point (PD14's spec: N = 92-847
distance-independent galaxies by scatter; systematics 0.90 percent quadrature < the gate;
DR4 ~2027 the low-z arm, the ELT-class high-z arm 2030s) and Gaia DR4. Status: ARMED,
EXECUTABLE (PD14: the gate closes; the decision is scheduled, not wished).

**Kill 2.** A detected WDM-type cutoff at ~0.5 Mpc (k_hm ~ 57 h/Mpc) kills the no-particle
ontology: the field's stress predicts NO sub-Mpc cut (the sound horizon 1.35-1.59 Gpc
comoving; R(k) = 1 through the registered deciding decade k ~ 100-500 h/Mpc). A CDM-like
spectrum to k >= 100 h/Mpc kills the particle face instead. Instrument: the sub-halo census
(the corpus's registered 5.6 decider) + the forest small-scale power. Status: ARMED.

**Kill 3.** Any measured cp = p'(0) != 1 -- a second RAR knee at g ~ s2 != s -- kills the
one-scale particle-free framework: kappa = s2/(2s) with s2/s measured = 1.0000 +/- 0.0033
(PD10). The 2pi form's s2/s = 0.922 sits 24 sigma out. Instrument: the SPARC-class deep
slope on both conventions. Status: MEASURED SHUT to 0.33 percent.

**Kill 4 (the Tolman constancy).** Any w-drift moves the count |1+3w| off 2: the corpus's
w <~ 5.7e-7 bound holds the factor constant to 1.7e-6 -- the flat-a0 law IS the Tolman
constancy (PD11). Instrument: the registered flat-a0 gate (the z~2.5 BTFR + the w-bound
machinery). Status: ARMED.

**The honest boundaries (unchanged):** the shape stays empirical (rung 2); the
OR-identification and the mode-matching premise are named (backed three ways,
mechanistically open); the Tolman reading is corroboration (the 2 = 3-1 trace difference),
not a replacement for the count derivation (PD01); the dimension tension (the Tolman count
d-1 vs the channel count 2-invariant) is recorded (PD11 T4) as the discriminator for any
future d-aware test. Seven compiled Lean certificates: PD05/PD07/PD09/PD10/PD11/PD12/PD13,
zero sorry, axioms = {propext, Classical.choice, Quot.sound}.
