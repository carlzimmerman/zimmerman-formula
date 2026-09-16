# G202 — THE MNRAS RESULTS-SECTION SKELETON
**The paper's results, section by section, assembled from the closed lanes — with the numbers, the lane citations, the falsifiers, and the pending observations.**

*Lane: G202. Repo: zimmerman-formula. Date: 2026-09-16.*
*Sources (all committed, nothing recomputed): G070 G071 G072 G073 G074 G075 G076 G078 G079 G080 G084 G088 G090 G091 G092 G093 G095 G098 G109 G114 G115 G119 G122 G129 G131 G132 G133 G135 G137 G139 G140 G141 G143 G149 G154 G156 G159 G161 G162 G165 G167 G168 G176 G177 G178 G179 G180 G182 G183 G184 G185 G186 G187 G188 G189 G190 G191 G192 G193 G194 G196 G198; H027; G03_SPEC §3; GRAVITY_EVERYWHERE (G120). Companion artifact: G202_results.json.*
*Relationship to the draft: PAPER_SKELETON.md (2026-09-14) is the overall paper skeleton (abstract/intro/derivations). This document is the RESULTS section's blueprint — §4 of that draft — rebuilt from the lanes that have since closed (G162/G176/G178/G179/G182/G184/G186/G187/G188/G192/G193/G194/G196/G198), with every number, its error, and its provenance. Drafting the results = rewriting the numbered statements below in prose + figures.*

---

## THE RESULTS SECTION — one line per section

| § | Section | The claim in one line | Closed by |
|---|---|---|---|
| 4.1 | The equipartition law | One zero-parameter law across 12 decades: M_dark/M_b = r/r_M. | G131/G162/G070/G071/G074/G078/G114 |
| 4.2 | The one boundary | Exactly one radius: r_M = sqrt(G M_b/a0), the baryonic a0-crossing, a first-order phase switch. | G196/G119/G176/G182/G186/G132/G188 |
| 4.3 | The cluster sector | M_dyn = M_b + M_ph + M_dust, closed form; one open number q. | G192/G143/G179/G135/G184 |
| 4.4 | The dark sector | One charge, two phases; m = 5.0–5.2 keV; the cosmic density closes. | G168/G093/G198/G180/G194 |
| 4.5 | The force-face | PPN = GR; no fifth force; the Cassini null is architectural. | G120/H027/G03_SPEC §3 |
| 4.6 | Open items | q, the sliver, the gap, the pending verdicts — the referee box. | G192/G196/G190 |

---

## §4.1 THE EQUIPARTITION LAW

**The paper's sentence.** The dark sector equilibrates at the virial temperature set by the vacuum scale; the equilibrated density is exactly the phantom, ρ = sqrt(G M_b a0)/(4πG r²), and the fully-predicted, zero-parameter relation

> **M_dark(<r) / M_b = r / r_M**,  r_M = sqrt(G M_b / a0),  σ² = v_flat²/2 = κ = c_s² = 1/2,  Σ_ph(<r_M) = a0/(πG),

holds across 12 decades of baryonic mass with a single slope-1 line.

**The headline numbers (5).**

1. **The 12-decade line.** Pooled OLS slope **b = 1.004 ± 0.011 on n = 542** objects over log M_b = 2.63–14.35 (G131's 248-object 10-decade line, 0.988 ± 0.020, plus G162's three gap-filling channels — GEMS groups, 258 ATLAS3D ETGs at 0.083 dex median |r|, E11 groups); rms about the identity 0.180 dex; the 2.89-dex gap reduced to **0.63 dex (78% filled)**. (Lanes: G131, G162)
2. **The dSph floor.** The dispersion face of the same law at the bottom: median |log10(pred/obs)| = **0.222 over 34 dSphs** (bright dwarfs 0.163; the classical 7-dwarf floor median −0.00, all inside ±0.35 dex). The floor of galaxy dynamics is set by the same constant. (Lanes: G070, G03G)
3. **The deep end.** Gas-dominated HI dwarfs (n = 55): rms **0.150 dex**, mass-independent (Theil–Sen slope −0.00); SPARC 641 rings at the RAR benchmark 0.145 dex with zero parameters. The boundary from below: the globular-cluster crossing at **M_cross = 1.23e5 M_sun, r_M/r_h = η/2 = 3.39 exactly** (η = 7.0 ± 1.2). (Lanes: G114, G071, G074)
4. **The universal surface density.** The phantom sheet's mean column inside r_M is a pure constant: **Σ_ph(<r_M) = a0/(πG) = 213.74 M_sun/pc²** to machine precision over six decades of mass (M_b cancels; alt footing 257.52); the observed local column 141.3 is bracketed between a0/(2πG) and a0/(πG). Locally: ρ_dark(R0) = 0.0081 M_sun/pc³ (in the measured 0.008–0.015 band); the finite ±1.1 kpc column 17.7 M_sun/pc² (in 15–25). (Lanes: G078, G076)
5. **The amplitude — zero parameters, one open scale.** M_ph(<r_M) = M_b exactly (max |ratio−1| = 2.2e-16, Lean-certified G090 rung 1); the RAR g² = a0 g_N is the sector's equation of state, not a force law. The deep end sits at a0_eff = 1.08–1.10e-10 (the cross-convention re-run closed G133's 1.65× staircase: MIGHTEE at SPARC-class M/L reads 1.08e-10 onto the dwarf scale, ratio_matched 0.95; residual vs a0_DE = +15.4–17.5% = 2.18–2.46 sigma statistical, 1.78–2.01 with M/L conventions — marginal, down from the staircase's 5.2 sigma); the lane-convention MIGHTEE reading 1.8433e-10 is reproduced by the seesaw's own constant s_Lambda = 2 a0_DE = 1.87238e-10 at 0.12 sigma. The one surviving parameter is a0_eff, with the registered decision tree. (Lanes: G090, G03E, G167, G189, G193, G190)

**The falsifiers (named, per test).**

- The UFD end of the dSph floor: one-sided departure, obs σ ~2.5× pred, residual slope **+0.16 ± 0.02 per dex** (G070 V2-FAIL, carried honestly — binaries/disequilibrium).
- The high-z zero point: if the BTFR zero point drifts by the +0.33-dex class by z ~ 2.5, the amplitude is not M_b-scaled at high z and the equipartition is a local coincidence (G080).
- The DR4 vertical map: no 140.6-pc break, ν_layer ≠ 2, a flat/rising box-ν, or a positive outer-bin dark column kills the phantom-sheet identification (G076/G092 — 6 of the 9 DR4 rows).
- The sliver (log M 13.07–13.70) is a **data** gap, not a falsifier — stated as coverage, not claim (G162).

**The pending observations.**

- **z ~ 2.5 BTFR (JWST):** the epoch discriminator — flat 0.00 dex vs rising +0.33 dex; ±0.13-dex floor; 1 clean point = 20:1, 4 objects = 5 sigma (G080).
- **DR4 (Dec 2 2026):** the 9 pre-registered rows scored by dr4_scorer.py (9/9 on the mocks): RIDGE R-LEVEL band [1.047, 1.11], R-RIDGE +18.4% at 30.7 sigma, R-BREAK 7.43 kAU; DOUBLE-MAP D1 4.2× at 6.2 sigma, D2 27.8 vs 6.6 M_sun/pc², D3 negative outer bin at 5.6-sigma sign; FUNNEL F1a 34.7/140.6/1357 pc, F1b e^{+R/3} flare (G165).
- **The sliver:** massive-fossil-group / cluster-baryon-foot data through log M 13.7 (G162).
- The kink-width contract (the MW break's character) is §4.2's pending item, ~1 year on in-hand catalogs (G191).

---

## §4.2 THE ONE BOUNDARY

**The paper's sentence.** The theory has exactly one physical radius, the baryonic a0-crossing **r_M = sqrt(G M_b / a0)** (the identity G M_b/r_M = sqrt(G M_b a0) is Lean-certified). The crossing is a first-order phase switch between the strong-field dust phase and the deep-field phantom phase; every phase change in the dark sector sits on the single projected line **r_b = r_M sqrt(a0/g_ext)**, and the radial acceleration relation is that boundary's phase diagram.

**The headline numbers (5).**

1. **The break.** The Milky Way's rotation-curve break at **6.13 kpc = 0.623 r_M** (full-kernel solve, G119/G149; EFE-cap deep form 6.50–6.74 kpc = 0.66 r_M); the projection identity r_efe/r_M = sqrt(a0/g_ext) holds to 1e-16 (M_b cancels). (Lanes: G119, G149)
2. **The seam.** The pooled cluster dust density is ONE law with a seam at **r_t = 387 kpc = 0.96 × median r_M (402 kpc)** [1-sigma band 269–543 kpc]: the shape breaks p1 = 1.50 ± 0.04 → p2 = 2.94 ± 0.04 (d_BIC = −351 vs the single index; BIC winner over every rival). The cluster environment sits at the a0 floor (sqrt(a0/g_ext) = 0.963 → g_ext = 1.08 a0) — the seam is the un-projected, "bare" r_M boundary. (Lane: G176)
3. **The jump.** The phantom/dust amplitude is DERIVED from the collisionless infall: v_ff(r_b) = 2σ_ph = 242.9 km/s → caustic-broadened σ_d = v_ff/√3 = 140.2 km/s → **A_b = (σ_ph/σ_d)³ = 0.650** vs the measured boundary ratio 0.484 (within 1.34×, the 2-bar); per-cluster agreement R = 1.09, **12/12 inside the derived band [0.125, 0.5]**; the seam's integrated imprint A_integral = 0.364 agrees with the universal A = 0.273 within 1.34× — the seam and the jump are the same event at 0.96 r_M. The jump pins the dust law's c0-combination. (Lanes: G182, G185, G186, G159)
4. **The phase diagram.** The pie is the two-regime map at every scale: inside r_M the field is strong (g > a0) and un-equilibrated free dust carries the missing mass (cluster dust **81.6% of M_dyn at 50 kpc = 97.6% of the missing mass**; g_tot(R500)/a0 = 0.554 < 1 on 12/12); outside, sub-a0, the phantom equilibrates and dominates (**56.9% at R500**). The composition saturates: **M_sat = 3.09e14 M_sun** — phantom phase above (share 0.16–0.48 on 12 clusters), all-dust phase below (26 groups, f_dust = 0.919 = 1 − f_b with f_b = 0.081). The boundary rests inside a 0.30-dex data gap (IC1633 1.73e14 → A1644 3.48e14). (Lanes: G140, G178, G179, G188)
5. **The first-order character.** The phantom→free-dust crossing carries a finite entropy step **dS = 10.8–23.7 k_B/particle** (cosmic-ref 10.8, in-cluster 21.5, matched-density 23.7) — L/(N k_B T) = 10.8–23.7, water-class (13.1) — at boundary temperature **T_b = 9.52 K = the CMB at z = 2.49**. Same switch in two more observables: the temperature law's pivot (T_obs/T_pred = 2 (M_dyn/M_b)(r_M/r), structural exponent 2/3) and the pie's pivot u = r_M/R500. (Lanes: G132, G095, G188)

**The falsifiers (named).**

- **Smooth steepening:** a smooth log-quadratic p(r) lies within d_BIC = **16** of the sharp seam — the transition must be reported as "a resolved transition" until the BIC gap widens; the one-boundary claim rests on the sharp-seam model winning (G176, carried).
- **The kink-width contract:** the SIGN of the break's width decides step-vs-kernel at ≥95% in ~1 year (prediction w90 < 0.3 step / 1–2 smooth, boundary w* = 0.5; 3-sigma boundary at the deep s_beta ~ 0.01; Eilers-resolution reproduces PENDING) (G191).
- **The cap-firing mechanism is un-derived:** G138's cH0 firing rule fails 4/4 (never observable); the environmental PLACEMENT is derived, the TRIGGER is not — the paper must register this (G196).
- **The any-mass break:** |break| = r_M sqrt(a0/g_ext) for ANY system; the zero-parameter F(e_N) kernel solves the position and the MW is the one in-band object (passes); a measured pair-break off the F(e_N) curve (3-sigma band violation) is a shape kill (G190, WALLABY row).
- **The phase boundary's location is derived, not measured** — the [1.73, 3.48]e14 gap; any sub-3.48e14 system with f_dust < 0.85 voids the all-dust phase (G178).

**The pending observations.**

- **WALLABY DR3 pair-breaks:** e.g. break at 1 r_M requires e_N ≥ 1.39, pair d ≤ 4.4 kpc — the prediction is to find the break in low-field pairs and dwarfs (30–60 h VLA-B/MeerKAT; the decisive turn set e_N 0.5–3 has 0 committed pairs, catalog-limited 6–18 months) (G196/G190).
- **DR4 (Dec 2 2026):** the 6.1-kpc break's vertical realization (funnel/double-map rows F1–F3, D1–D3) plus the wide-binary break-shape (R-BREAK 7.4 kAU) (G165).
- **The phase-boundary gap:** eROSITA/SZ systems at 2–3e14 discriminate sharp-vs-smooth saturation (sharp: s_ph 8/10/12%, f_dust 0.91/0.89/0.86; smooth: s_ph 13/26/40%, f_dust 0.85/0.71/0.55) (G187).
- **The kink-width measurement** (~1 year, H3/APOGEE giants + GD-1/Pal-5/Orphan streams, in-hand catalogs) (G191).

---

## §4.3 THE CLUSTER SECTOR

**The paper's sentence.** The cluster dark sector composes in closed form:

> **M_dyn(<r) = M_b(<r) + M_ph(<r) + M_dust(<r)**,  M_ph = M_b(r)(r/r_M) (derived, Gauss-map charge),  M_dust = 0.72 (M500/8e14)^(−0.414 ± 0.157) (r/R500)^(−0.990 ± 0.035) (measured, two parameters),

with the closure SUM/M500 = 1 an identity; the amplitude is pinned by the derived infall jump; the sector's remaining freedom is the single number q.

**The headline numbers (5).**

1. **The closed form.** The phantom is the Gauss-map charge: M_ph(<r) = (1/4πG)∮g·dA = **M_b(r)(r/r_M)** (equipartition; the static-branch shift-Noether current J^μ = 0 is empty, the dark mass is ASSIGNED as the surface-integral charge — G154/G180). The dust: c_dust(M500, r) = 0.72 (M500/8e14)^(−0.414 ± 0.157) (r/R500)^(−0.990 ± 0.035) [c0 = −0.145, q = −0.414, p = +0.990; rms 0.119 → 0.097 dex; ONE envelope across M500 ~ 1e13–9e14, 38 systems]; enclosed M_dust(<r) = M_b(<r)(c_dust − 1)(r/r_M). (Lanes: G192, G143, G179, G154, G180)
2. **The power law and its freedom.** Two parameters (c0, q) + the 0.1-dex floor; c0's combination is PINNED by the derived jump (A_b = 0.650, R = 1.09, 12/12 — the sector's last freedom is **the single number q**, measured −0.414 ± 0.157, consistent with the jump's own mass run q_jump = −0.34 ± 0.27, not independently derived). The group scale discriminates: the 26-group dust rise **+0.536 ± 0.069 vs +0.235 on clusters (2.3× steeper, 20/26 above at t = 4.3)** rides this amplitude run. (Lanes: G143, G140, G185, G182)
3. **The pie.** At R500: **baryons 17.7% (15.1–21.5) / phantom 56.9% (54.0–60.7) / dust 24.6% (18.1–31.3)**; the data pie closes exactly, the LAW pie closes to −0.18 ± 0.06 dex (the 50–600 kpc fit-window extrapolation, stated not hidden). Inside: dust 81.6% at 50 kpc (= 97.6% of the missing mass) → 24.6% at R500. Cosmically: mass-function-weighted 〈s_d〉 = 0.805, 〈s_ph〉 = 0.111 — the equilibrium phase is NOT new cosmic mass. (Lanes: G179, G188, G187)
4. **The temperature law.** **log10(T_obs/T_pred) = (2/3) log10 f + log10(2 r_M/R500)** with structural alpha = 2/3 (virial +1, −1/3 from Δ500 self-similarity): pooled 31-system rms **0.076 dex** (clusters 0.067 = the HSE scatter, groups 0.081); cluster closed form 3.51 vs measured 3.57; T_pie = T_vir(M500) at 0.057 dex (the data-pie face = HSE); the virial 1/2 is excluded at ~2.2 sigma. (Lanes: G095, G135)
5. **The outer slope.** The dark-density envelope falls as **r^−2.404 ± 0.078** between R500 and 2R500 — three instruments consistent (X-ray dark residual −2.17 ± 0.32, X-ray gas beta-tail −2.624 ± 0.176, tSZ joint −2.37 ± 0.09; mutual chi2 = 2.29/2, p = 0.32): **7.7 sigma from NFW's −3**, inside the theory band [−2.4, −2.0] (the X-ray dark residual alone: 2.6 sigma). (Lane: G184)

**The falsifiers (named).**

- **The all-dust phase:** any system below 3.48e14 with f_dust(missing) < 0.85 voids the sharp saturation (G178).
- **The tSZ 3-way:** the sample-median 2-bin slope over [R500, 2R500] — (−2.94, −2.14) JOINT (center −2.54 ± 0.4) / phantom-only −1.44-class / steeper-than-joint neither; Delta chi2 = 2290 = **47.8 sigma pooled shape-only** (G177).
- **The position-inside-R500 degeneracy:** the knee at r_b/rs = 0.54 coincides with NFW's OWN transition (slope −1.70 at the knee) — unresolvable inside R500; only the outer slope discriminates, and the tSZ pooled slope error 0.09 resolves −2.4 vs −3 at ~7 sigma (G160/G129).
- **The constant-temperature face:** f_ph must NOT track the disturbance flags (the dark-ages constancy test, §4.4) — kill condition = f_ph trending with disturbance (G194).
- Carried honest caveats: A2319's pie has s_d = −2.7% (c < 1 at R500, the registered uncapped overshoot); the EFE-capped alternative reading collapses the pie to dust 82.3% + baryons 17.7% (G057 V2).

**The pending observations.**

- **tSZ (the 3-way verdict, ~2–4 weeks per survey):** all inputs public today (Planck MILCA/NILC + ACT maps; G126 pipeline committed); the falsifiers are asymmetric — F2' (dust-kill) at 4.4–6.9 sigma, F1' (steeper/neither) at 1.7–2.6 sigma: the measurement separates JOINT from PHANTOM-ONLY confidently, can only point at a different envelope slope (G177/G129).
- **XRISM (GO/AO cycles):** the plateau flat-tail certification — |dT/dlog r| ≤ 0.30 keV/dex over [1.25, 2] R500 at the level 2 T_floor (slope 0 at 3 sigma AND level at 2 sigma, ≥ 9/12); 5–8 clusters × 100–250 ks, per-cluster sigma_slope ≤ 0.2 keV/dex; the A1-vs-A2 slope break at r_cap in (1.2, 1.5) R500 is the XRISM bins' job. In hand: the LEVEL is confirmed (median last-bin T = 1.12 × 2 T_floor, envelope residual g = 0.90, 12/12 within 0.3 dex; flat tail NOT yet covered, 2/12 flat) (G161/G130).
- **eROSITA / SZ in the 2–3e14 gap:** sharp-vs-smooth saturation discrimination (G187); the within-R500 closure's measured phase boundary (G178).
- **XRISM-class HSE deprojection** for the lensing-core decision D2 at r < 0.1 R500 (NFW −1 vs the theory's core ~−1.5; slope ≤ −1.2 → NFW wins, ≤ −1.7 → the theory's core) (G136).

---

## §4.4 THE DARK SECTOR

**The paper's sentence.** The cold sector is not a species but the shift-symmetry charge of the scalar field — one charge, two acceleration-selected phases (equilibrated phantom / free dust). Inverting the freeze temperature against the CMB dates the equilibrium's formation to cosmic noon and predicts the carrier's mass, **m = 5.0–5.2 keV**; the sector's cosmic bookkeeping (equilibrium + envelope-inclusive free dust) closes the observed Omega_dm to 1.000; and the ontology is pre-registered as a charge-vs-relic test.

**The headline numbers (5).**

1. **The particle mass.** T_b = m σ²/k_B = T_CMB(z*): with the MW-class triad σ = 119.2 km/s and the committed G132 band z* = 2.37–2.49, **m = [5.00, 5.19] keV (canonical; union over footings [4.55, 5.19] keV)** — upper half of the forest window, 1.5× above the 2-sigma floor; the sharpest number m(z* = 2.4) = 5.05 keV; sensitivity dm/dz* = 1.49 keV per unit z. **Kill band m < 4 or m > 6 keV.** (Lanes: G168, G132)
2. **The independent window.** The Lyman-alpha forest bounds the free dust at **m ≥ 3.3–5.7 keV** (Viel 2013 2-sigma 3.3, Irsic 2017 5.3, Villasenor 2024 95% CL 5.7; streaming bound 4.7) — a different observable, no framework input; the loop z*→m→z* is self-consistent at ~10–20% (m = 5.7 keV maps back to z* = 2.84). The cluster-class converse decouples at z = 155–265 (dark ages), so the MW-class sigma is the only equilibrium that survives both directions. (Lanes: G093, G168)
3. **The density-closed cosmology.** **Omega_dust(envelope-inclusive) = 0.2619 = 99.2% of the observed Omega_dm = 0.264** (within-R500 halo slice 0.0879 = 33.3%; envelope + ambient infall + sub-1e12 + field 0.1740 = 65.9%); the equilibrium carries 0.79–1.28%; **equilibrium + dust = 0.2640 = 1.000 of Omega_dm — DENSITY-CLOSED** (mass conservation, G079's decomposition, 4e-6 register rounding). The halo-INTEGRAL keeps G115's warm-floor gap: 0.60–0.79 collapsed count (the envelope restores the local abundance — reservoir 2.0–6.2×, feed 8.28e12 M_sun/Gyr — but not the sub-1e6 count). The vacuum side: a0 alone gives **Omega_Lambda = 0.6857 (+0.07% of Planck 0.6847)**. (Lanes: G198, G187, G079, G115, G052)
4. **The ontology, assigned.** The dark mass is the Gauss-map charge of the sourced field, M_ph = (1/4πG)∮g·dA (G180, wording-level amendment; the old "Noether charge" wording is empty on the static branch, J^μ = 0, G154). It is a field configuration, not a particle: direct detection has nothing to find (40 years of nulls are the prediction); phase-space never caps the equilibrium (m > 23.25 eV needed, 4.01× BELOW the killed relic window); the free dust is the coldest species in the inventory (v_therm < 0.055 km/s, λ_fs < 0.5–0.8 Mpc vs the registered 0.6 Mpc). (Lanes: G180, G154, G028, G084, G093)
5. **The dark-ages freeze (the relic prediction).** The galaxy phantom froze at z* = 2.37–2.49 (T_b = 9.2–9.5 K, the CMB at cosmic noon); the cluster-class equilibrium froze at z = 155–265 (T_b = 232–635 K, 5.7 keV class; z*(841 km/s, 5 keV) = 166.5 reproduced) and stayed frozen (G093 collisionless, G103 static): **the phantom carries no memory of assembly** — the constancy test passes 3/3 conventions on n = 12 (f_ph flat across the disturbed/relaxed split, MW p = 0.39/0.59/0.49, Spearman rho = −0.203/−0.175, split explains < 20% of the variance; the one fully-flagged NCC case ZW1215 at f_ph = 0.241, 0.66 sigma from the median). (Lane: G194)

**The falsifiers (named).**

- **Direct detection** of a particle (there is no species; a detection claim would contradict the charge ontology) or LIGO/EHT non-GR signatures (G093/H027).
- **The mass measurement:** m outside [4.6, 5.2] keV (forest/sterile) kills the cosmic-noon coincidence — the forward band, not the loose window-wide converse, is the commitment (G168).
- **The epoch:** a BTFR zero-point break NOT in [2.37, 2.5] falsifies the freeze-epoch identity z_break = z* (G168/G011).
- **The charge/relic discriminator:** the G115 collapsed-count gap — charge (R(k) = 1, λ_fs = 0, subhalos continue below 1e6, N(>1e5) = 32076) closes 0.79–0.95; the warm-truncated relic (5.7 keV, λ_fs = 0.50 Mpc, M_hm = 5e5–5.8e6) leaves 0.60–0.79: a measurement of the deep-low-mass collapsed count picks the ontology (G156/G198).
- **The constancy test:** f_ph trending with the disturbance flags at cluster scale kills the frozen-relix prediction (G194).

**The pending observations.**

- **The mass m (the deciding number):** forest/sterile searches — m in [4.6, 5.2] keV confirms both the equilibrium and the z*-inversion; below ~4 or above ~6 keV kills them (G168).
- **z_break:** the BTFR zero-point break epoch at z ~ 2.4–2.5 — flat below z*, evolving at/above z* — the independent z* measurement (G080/G168; the same z ~ 2.5 discriminator as §4.1).
- **The charge/relic test:** sub-halo / Lyman-alpha counts below 1e6 M_sun (DESI, Euclid, next-gen forest) resolving 0.60–0.79 vs 0.79–0.95 (G156/G115).

---

## §4.5 THE FORCE-FACE

**The paper's sentence.** The theory modifies no force in any regime: the metric sector is exactly Einstein–Hilbert, so **PPN = GR** at the tested level; the scalar enters only as a sector generator, and its Solar-System prediction — no phantom, no transition shell, **the Cassini null** — is architectural, not fitted.

**The headline numbers (5).**

1. **c_T = c identically.** The scalar enters through K = −(1/2)(∂φ)²/Λ⁴ only algebraically — no derivative coupling, no disformal term — so the tensor quadratic action is exactly Einstein–Hilbert and **c_T = c, PPN(gamma, beta) = GR** with nothing to arrange; GW170817 is satisfied structurally (contrast AeST). (Lane: H027 T1, assembled in G120)
2. **The Cassini null — proven, not assumed.** The Solar-System-adjacent sector is absent: the local cloud is unbound and EFE-capped at 7.4 kAU, so the Sun's field is Newtonian plus local dust — no quadrupole, trivially under the Park 2026 ceiling. The pincer is complete: (a) every force-law completion fails Cassini — the bare μ₂ kernel exceeds the ceiling by **6.44×/7.63×** (both footings, S0-calibrated), a 44-solve scan of every surviving modification class never drops below **6.18×** (ξ = 0 best case), and the smooth-shell lemma (an isotropic local screen preserves the l = 2 moment) closes the class with proof; (b) the equilibrium reading predicts Newton there by construction. (Lanes: G03_SPEC §3, L243, G120)
3. **No fifth force anywhere.** MOND-looking dynamics is not a force law: it is the gravity of the equilibrated charge dust — the RAR is the sector's equation of state (hydrostatics), μ₂ the interpolant of the equilibrium's own law. The scalar itself never pulls. (Lanes: G031, G120)
4. **Lensing = GR with real mass.** The phantom is real mass in Einstein's equation — no conformal slip, no lensing-dead scalar (the L241 kill applies to conformal-only force laws, which this is not). (Lane: G03E V4)
5. **Black holes carry no independent scalar hair.** The sourced equation div[f'(K)∇φ] = 4πGρ has no integration constant independent of the metric's mass: EHT/LIGO see GR (ringdowns, shadows); compact objects carry the same phantom-halo law, M_ph/M = r/r_M (10 M_sun: 0.12 pc; 1e9 M_sun: 1.2 kpc). (Lanes: H027 T2/T3, G120)

**The falsifiers (named).**

- A non-GR ringdown or shadow deviation (EHT/LIGO) — no scalar hair permits none.
- A fifth-force signal at any scale — the scalar couples to nothing but its own charge's stress-energy, through GR.
- A lensing slip (light not seeing the full real mass).
- The DR4 wide-binary verdict is the live Solar-System-adjacent test: the Newton + cloud reading predicts the period–separation ridge (γ_v rising 1.002 → 1.047 at 10–30 kAU, +18.4% in separation, breaking at 7.43 kAU); a Newtonian or flat/breakless s-excess kills the cloud identification (G088).

**The pending observations.**

- **DR4 (Dec 2 2026):** the 9-row scorer — the RIDGE at 30.7 sigma (N = 2500 bright pairs, 30 uas), the R-BREAK at 7.4 kAU, the DOUBLE-MAP and FUNNEL rows; the γ_v LEVEL alone is triple-confounded (+2–10% mimics) and the strict plateau 1.2886 is already B-falsified on DR3 — the ridge, not the level, is the zero-parameter statement (G088/G165).
- **Next-generation Cassini-class / LIGO–Virgo–KAGRA & EHT upgrades,** and the WALLABY pair-break shape test (F(e_N), footing-invariant; MW anchor F(2.29) = 0.6232–0.6273) (G190).
- (The force-face is otherwise CLOSED-by-construction: no fitted parameter, no free normalization.)

---

## §4.6 THE OPEN-ITEMS BOX (the referee box)

The structure a referee expects: everything pending, named, bounded, and falsifier-armed — nothing closed that a gate did not close, nothing open that decides the story but is not named.

**The four named open items.**

1. **q — the single cluster number.** The dust law's mass slope, measured −0.414 ± 0.157 (12-point power; predictor se 0.27 > law se 0.16), consistent with the derived jump's run q_jump = −0.34 ± 0.27 but not independently derived. Discriminating test: the group-scale amplitude (the 26-group rise +0.536 ± 0.069 rides this run; G140's registered prediction). (G143/G185)
2. **The sliver.** The 12-decade line's unfilled 0.63 dex (5.4% of span) at log M 13.07–13.70 between the most massive groups and the least massive cluster — open by data, not by law; the seam residual rises gently (+0.115 groups → +0.273 clusters), no step. (G162)
3. **The gap.** The phase-boundary data gap [1.73, 3.48]e14 M_sun (IC1633 → A1644): the two-phase diagram is measured at its endpoints, the boundary DERIVED not measured; sharp-vs-smooth saturation discriminated at 2–3e14 (falsifier: f_dust < 0.85 below 3.48e14). (G178/G187)
4. **The pending verdicts.** DR4 (Dec 2 2026, 9 pre-registered rows, scorer 9/9 on mocks); tSZ 3-way (all inputs public, ~2–4 weeks per survey; asymmetric falsifiers F2' 4.4–6.9 sigma / F1' 1.7–2.6 sigma); z ~ 2.5 BTFR (JWST, 20:1 per clean point, 4 = 5 sigma; z_break = z*); XRISM plateau (GO cycles, per-cluster sigma_slope ≤ 0.2 keV/dex, the A1/A2 slope break). (G165/G177/G080/G161)

**The carried caveats (registered, verbatim).**

- The seam's sharpness is provisional: d_BIC = 16 to smooth steepening; the seam is ONE r_M-class radius, not per-cluster (d_BIC = −110.8) (G176).
- The cap's firing mechanism is not derived (G138's cH0 rule fails 4/4); the environmental placement is (G196).
- The 0.62 saturation share (the MW's phantom cap) lacks a closed-form derivation from the constants (G119).
- The relaxation/stability rung is open: does the sector actually relax to σ² = sqrt(G M_b a0)/2? (G081; K001 no attractor found — the honesty edge).
- The BTFR register correction is pending (G117); the -0.18-dex R500 closure offset is a fit-window statement; the m/z* inversion's circularity is guarded (z* is defined at the 5-keV anchor; the prediction becomes real only with independent z_break + a measured m) (G168); the UFD and cluster-amplitude end departures of the 12-decade line are carried as registered FAILs, not hidden (G070/G075).

---

## VERDICTS

### V1 — THE SKELETON IS COMPLETE WITH ALL NUMBERS. PASS.
Every one of the five results sections carries its 5 headline numbers with errors, units, and lane citations (542/1.004 ± 0.011; 0.623 r_M/0.96 r_M/0.650; 17.7-56.9-24.6/-2.404 ± 0.078/0.076 dex; 5.0–5.2 keV/0.2619 = 99.2%/1.000; 6.44×–6.18×/c_T = c), the open-items box names all four open items with their tests, and every pending instrument is mapped to the sections it decides (DR4 → 4.1/4.2/4.5, tSZ → 4.3, z~2.5 → 4.1/4.4, XRISM → 4.3). Nothing in the skeleton exceeds the committed lanes.

### V2 — THE FALSIFIER COVERAGE PER SECTION. PASS.
§4.1: 4 falsifiers + 1 stated data gap (UFD departure, high-z drift, DR4 map, sliver). §4.2: 5 falsifiers (smooth steepening, kink sign, cap mechanism, any-mass break, phase boundary). §4.3: 5 falsifiers (all-dust phase, tSZ 3-way, inside-R500 degeneracy, constancy test, overshoot caveats). §4.4: 5 falsifiers (direct detection, m band, epoch identity, charge/relic gap, constancy trend). §4.5: 4 falsifiers (ringdown/shadow, fifth force, lensing slip, DR4 ridge). Every section has a named kill condition with the number that fires it; the asymmetric tSZ falsifiers and the m/z* circularity guard are stated as such, not papered over.

### V3 — THE HONEST STATEMENT: READY TO DRAFT. PASS.
The MNRAS results structure is assembled and referee-checkable: what the paper says, section by section — 4.1 one zero-parameter law across 12 decades (542 objects, b = 1.004 ± 0.011) with the universal surface density and the dSph floor; 4.2 one physical radius r_M = sqrt(G M_b/a0) marked at every scale (break 0.62, seam 0.96, jump 0.650, first-order latent heat, phase diagram); 4.3 the cluster sector in closed form M_dyn = M_b + M_ph + M_dust with the derived amplitude, the 17.7/56.9/24.6 pie, the 2/3 temperature law and the three-instrument outer slope at 7.7 sigma from NFW; 4.4 the dark sector with the 5.0–5.2 keV mass prediction, the density-closed cosmology (0.2619 = 99.2% of Omega_dm, sum = 1.000) and the pre-registered charge/relic ontology; 4.5 the force-face with PPN = GR and the architectural Cassini null; 4.6 the open box (q, the sliver, the gap, the four pending verdicts). The paper's results are fully drafted-in-structure: every number committed, every falsifier armed, every pending observation named with its decision rule. The results TEXT (prose + figures) remains to be written from this skeleton; no new calculation is required to do so.

---

*Deliverable complete. Pass: 3/3 verdicts. G202_results.json written alongside.*