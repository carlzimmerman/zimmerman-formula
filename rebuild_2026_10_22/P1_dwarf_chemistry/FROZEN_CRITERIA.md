# P1_dwarf_chemistry — FROZEN CRITERIA (written before any script or number of this lane)

Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. κ = ½ FITTED. Footings canonical
a0 = 9.3603e-11, alt 1.1312e-10 m/s², never pooled. Cold energy, no particle. Not "theory closed". Nothing here says the data
favour the framework. Assumptions: `ASSUMPTION_LEDGER.md` (committed with this file).

## The question
E6 Part C (`doors_push_2026_10_22/E6_native_fret/`) found the satellites' cold supply sufficient by chemistry: the homogeneous
leaky box on mean [Fe/H] gives catchment baryons ≥ L_min × present baryons, median q_chem = L_req/L_min = 0.21 canonical / 0.19 alt
(F1, log y −0.5, W2). It is conditional on winds at ISM metallicity (ζ = 1) and no pre-enrichment. Six systems were short at
central values (Columba I, Segue 1, Tucana IV, UMa I, UMa II, Willman 1). This lane replaces the two assumptions by what the
satellites' own metallicity distributions (MDFs) and [Mg/Fe] say, and recomputes q on both footings.
Supply is not mechanism: even a confirmed supply leaves the binding mechanism open (G2 failed). The README must say so.

## Record checked before freezing
E6 (README, criteria, script L113–270 leaky-box functions, per-system CSV); E3 (CSV); CFG920 (leaky box, W1/W2, ζ escape);
CFG317 (yield bracket: log y_Fe/Z_Fe,⊙ = −0.2 nominal, [−0.5, +0.1], declared core-collapse-dominated: O yield ≈ 1–1.5 Z_O,⊙ and
the [α/Fe] ≈ +0.3–0.4 plateau); CFG852 (gas loss vs metallicity, correlation only); CFG51 (`reduce_walker.py`, Walker 2023
membership; not reused, cross-check only); CFG257 (Geha 2026 Paper II Table A1 transcription); G2 (binding fails); LVD
PROVENANCE. No lane in the record fits an MDF shape or uses [Mg/Fe].

## Analytic statements (stated before computing; K1/K3/K6 check them)
One-zone model: instantaneous recycling and mixing; outflow η·SFR at metallicity ζ·Z_ISM; start metallicity Z0; no inflow;
optional terminal strip of the gas left when star formation stops. Let t = ln(g0/g) (gas-consumption variable; stars per dt ∝ e^−t),
t ∈ [0, u]. Then dZ/dt = p0 − kZ with **p0 = y/(1+η)** and **k = (ζ−1)η/(1+η) ≥ 0**. Gas-free today: **L = (1+η)/(1−e^−u)**.
- **A1.** With Z0 = 0: Z/p0 = φ_k(t) = (1 − e^−kt)/k (→ t at k = 0), so **L = y / (p0 (1−e^−u)) = y · f(0+)**, where f is the stellar
  MDF density in linear Z at its metal-poor end. This holds for every ζ ≥ 1. The catchment is set by the MDF's metal-poor end, not
  by its mean. With ζ = 1 (k = 0) the shape is fixed and the mean suffices (E6).
- **A2 (width band).** k = 0, Z0 = 0: ln Z = ln p0 + ln t with t ~ Exp(1) truncated at u, so the intrinsic std of [Fe/H] lies in
  **[1/ln10, π/(√6 ln10)] = [0.4343, 0.5570] dex** for every η and u (gas-bearing W1 included). A narrower MDF needs k > 0 (ζ > 1),
  Z0 > 0 or inflow. A broader one needs inhomogeneous mixing or ζ < 1.
- **A3 (direction).** At a fixed observed (mean [Fe/H], σ), Z0 > 0 or pristine inflow give an L at least as large as the ζ-only
  (Z0 = 0, k > 0) reading. So the ζ reading is the conservative (lowest-L) one, and it is the one graded. In particular,
  **pre-enrichment raises E6's mean-only L_min at ζ = 1** (more of the mean is external, so less self-enrichment per unit gas and
  more loss). This is the opposite of E6 `FROZEN_CRITERIA.md` L59 and `README.md` L116 ("pre-enrichment lowers L").
- **A4 (untestable by any MDF).** Unmixed escape of fresh ejecta (a fraction f leaves before mixing) has exactly the MDF shape of
  ζ = 1 with a retained yield (1−f)·y. No MDF or [α/Fe] on disk tests it. It is named as a premise, and its price per system,
  f_break = 1 − q (the escape fraction at which the system's supply reaches its need), is reported.

## Inputs (all read-only; nothing downloaded)
- LVD `real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv`: `metallicity` (mean [Fe/H], as E6), `metallicity_spectroscopic_sigma`
  (+ep, −em, `_ul`, ref), `metallicity_photometric_sigma` (fallback only, flagged PHOT), kinematics/PM/structure for membership,
  `mass_HI` (× 1.33, as E6).
- Simon 2019 compilation `deepseek_push/data2/simon2019_dwarf_tab_ascii_14sep2018.dat`: σ_[Fe/H] (+, −, 90% UL flag) — alternate width.
- Geha 2026 Paper II Table A1 `campaign_fresh_gravity/CFG257_ufd_kinematics_scoping/geha2026_paperII_tableA1.csv`: N_stars, σ_[Fe/H] (inventory).
- Walker et al. 2023 per-star catalogue `real_research/data/walker2023/{hectocat,m2fshi,m2fsmed}.dat.gz`: per-star mean [Fe/H], [Mg/Fe]
  (APOGEE zero point, `*Avg` columns), velocities, logg, Gaia PM/parallax, flags.
- E6 `e6_per_system.csv`: L_req_F1, L_req_F2 per footing, Lmin_−0.5|W2, Lmin_+0.1|W1 (K2). E3 `e3_per_system.csv`: q_fret010_p2p5,
  M_dyn, logMstar (robust-shortfall line, Υ sensitivity).
- Yield bracket log y ∈ {−0.5, −0.2, +0.1} (CFG317). Supply factor 5.364 enters only through L_req (inherited).

## Step 1 — inventory (`p1_inventory.csv`)
For the 45 canonical systems (+ Andromeda XXVIII, alt only): LVD mean [Fe/H] and type; LVD σ (+/−/UL, ref); S19 σ (+/−/UL);
Geha N_stars and σ; Walker N_members, N_Fe, own σ, N_Mg, mean [Mg/Fe]; N_EMP. Names matched exactly (S19 '~' → space).

**Walker membership (declared, not tuned).** Per star (target, Gaia DR3 id), using the catalogue's quality-epoch means (`*Avg`);
a star in two files is combined by inverse variance. Required: goodNobs ≥ 1; Gaia id present; RRL = AGN = 0; f_Cany = 0 and
f_Chi2any = 0 (carbon or bad-fit spectra give unreliable [Fe/H]); loggAvg < 4.0; |v − v_sys,LVD| < 3·√(max(σ_LVD, 2)² + e_v²)
(σ_LVD = vlos_sigma, else its UL, else 5 km/s); PM χ² < 9.21 (2 dof, 99%) with s² = 0.05² + e_PM,LVD² + (σ_LVD/(4.74 d_kpc))² added
to each star's Gaia variance; parallax |ϖ − 1/d| < 3·√(e_ϖ² + 0.03²) where ϖ is given; elliptical radius ≤ 5 r_h (LVD rhalf,
ellipticity, position angle). [Fe/H] sample: members with finite FeHAvg and e > 0 (N_Fe). [Mg/Fe] sample: finite MgFeAvg (N_Mg).

## Step 2 — premise tests
- **P-W (width), per system and source.** σ_c with errors (em, ep). NARROW if σ_c + 2ep < 0.4343 (or a UL < 0.4343); BROAD if
  σ_c − 2em > 0.5570; else CONSISTENT. A σ without errors is classed on its central value and flagged; UL ≥ 0.4343 → UNDETERMINED.
  Sources: LVD (primary), S19, Walker per-star (N_Fe ≥ 10; Gaussian MLE with per-star errors, profile Δ(−2lnℒ) = 1 interval).
  A system that is NARROW fails the joint premise "ζ = 1 ∧ Z0 = 0 ∧ no inflow" as a description of its MDF.
- **P-S (shape), Walker, N_Fe ≥ 10.** Best fit of the ζ = 1, Z0 = 0 family (MLE over p0 and u, model convolved with each star's
  error); probability-integral transform per star; Anderson–Darling against U(0,1); p-value by parametric bootstrap (200 refits,
  seeded). FAIL if p < 0.05.
- **P-A ([α/Fe]), Walker, N_Mg ≥ 5.** Weighted mean and weighted slope of [Mg/Fe] vs [Fe/H] (errors inflated by √max(1, χ²_ν)).
  DECLINE if slope + 2σ < 0 (SN Ia iron during star formation: total Fe yield applies, above the CC bracket; the IRA is broken for
  that iron); else PLATEAU if mean − 2σ ≥ +0.15 (core-collapse iron: CFG317's CC bracket is the right one); LOW if mean + 2σ < +0.15;
  else UNDETERMINED. α-anchored yield log y_Fe = log y_α − ⟨[Mg/Fe]⟩ with log y_α ∈ [0.00, 0.18] (CFG317's O-yield statement applied to
  α; EXTERNAL textbook): BELOW if its 2σ interval lies wholly below −0.5, ABOVE if wholly above +0.1, else IN. Reported; it does not
  move the graded corner.
- **P-0 (pre-enrichment).** A3 checked numerically (K3). N_EMP = members with [Fe/H] + 2e < −3.0 (reported).

## Step 3 — supply recomputed from the MDF
Grid: k ∈ {0} ∪ logspace(−3, 3, 241); u ∈ logspace(−4, 2, 241) ∪ {∞}. g(k,u) = ⟨ln φ_k(t)⟩, s²(k,u) = Var ln φ_k(t), σ_model = s/ln10.
Gas-free system with Z_g = 10^[Fe/H] (LVD mean, as E6): p0 = Z_g e^−g, **L = (y/p0)/(1−e^−u)**, allowed only if p0 ≤ y (η ≥ 0; strict
for k > 0). Gas-bearing (M_g > 0): u = ln(1 + (1+η)M_*/M_g), L = ((1+η)M_* + M_g)/(M_* + M_g), solved per k.
**L_MDF(I, y)** = min of L over allowed grid points with σ_model ∈ I. Intervals: I0 = [σ_c − 0.005, σ_c + 0.005] (central),
I2 = [σ_c − 2em, σ_c + 2ep] (floored at 0). If I lies wholly above the family maximum: L at (k = 0, u = ∞), flagged ABOVE. If I reaches
below the grid's smallest σ: NO BOUND (L := 1). No allowed point (chemistry under-produces [Fe/H]): L := 1, flagged UNDER (favours
shortfall, as E6). No σ: NOT TESTED. Reported at the L-minimising point of I0: η, ζ_MDF = 1 + k(1+η)/η, u, and f_break.
**q = L_req / L_MDF** with L_req from E6's CSV (F1 and F2, each footing).

**Graded statistic:** median q over tested systems (LVD central σ), bootstrap over systems (4000, seeded), **F2** (E6's own
consistent accounting, CFG424) graded, F1 reported; each footing separately.
- Per system: SHORT if q(I0, −0.5) > 1. Robust supply if q(I2, −0.5) ≤ 1. Robust shortfall if L_req,F1,2.5% / L_MDF([σ_c+2ep ± 0.005], +0.1) > 1
  (E3's 2.5% need; F1 only, as E6).

## Outcome lines (frozen)
- **SUPPLY CONFIRMED:** at (I0, log y −0.5) median q ≤ 1 and its bootstrap 84th percentile ≤ 1, F2, on both footings. The SHORT systems
  are listed. (This means the supply survives with ζ and pre-enrichment taken from the MDF, whatever P-W says about ζ = 1.)
- **SUPPLY FAILS:** at (I0, log y +0.1) median q > 1 and its bootstrap 16th percentile > 1, F2, on both footings. The failing premise
  is named (ζ = 1, by P-W, in N systems).
- **UNDECIDABLE ON DISK:** otherwise; and also if the class changes under either robustness substitution: **R1** S19's measured σ in
  place of LVD's where S19 has one; **R2** the Walker per-star σ in place of LVD's where N_Fe ≥ 10. The exact data needed are named
  from the trigger.
Reported, not graded: all three yield corners, I2, F1, P-W counts per source, ζ_MDF, f_break, Υ_V ∈ {1.5, 2.5} on F2 L_req
((M_dyn − f M_*/2)/(5.364 f M_*)), E6's six systems one by one.

## Checks (`p1_dwarf_chemistry.py`, one line each; exit 0 iff all pass)
- **K1** quadrature vs exact: k = 0 rows vs E6/CFG920 `elnx` and the closed-form variance; u = ∞ rows vs Beta(1, 1/k):
  ⟨ln z⟩ = ψ(1) − ψ(1+1/k), Var = ψ₁(1) − ψ₁(1+1/k), for k ∈ {0.1, 1, 10, 100}. Max abs error ≤ 1e-6 in g and s².
- **K2** E6 reproduced by independent code: the k = 0 slice gives E6 CSV Lmin_−0.5|W2 and Lmin_+0.1|W1 within 1e-3 rel for every
  canonical system E6 tested.
- **K3** direction (A3): (i) E6's mean-only ζ = 1 L_min rises when Z0 = 0.3·Z_g is added, at [Fe/H] ∈ {−2.0, −2.5, −3.0}, log y −0.5
  (all 3); (ii) for 9 synthetic pre-enriched ζ = 1 MDFs (Z0/p ∈ {1, 3, 10} × u ∈ {0.1, 1, ∞}), the ζ-reading L_MDF from their
  (mean ln Z, σ) is ≤ their true L (all 9).
- **K4** Gaussian MLE of σ_int recovers the family's std: for grid points with σ_model ≈ 0.25 and 0.45 dex, N = 30 stars, errors
  0.3 dex, 300 seeded reps: |median σ_MLE / σ_model − 1| ≤ 0.15.
- **K5** Walker membership sanity: every system with N_members ≥ 10 has |median member v − v_sys,LVD| ≤ 3 km/s.
- **K6** band: the k = 0 grid's min and max σ_model equal 0.4343 and 0.5570 dex within 2e-3.
- **--mutate:** k ≡ 0 inside the quadrature (ζ = 1 imposed everywhere: E6's premise). K1 must FAIL on the k > 0 rows. Outputs
  `*_MUTATE.out`, `p1_dwarf_chemistry_results_MUTATE.json`, `p1_per_system_MUTATE.csv`.

## Not blind (disclosed)
Before freezing, the author listed the LVD σ_[Fe/H] column for all 46 systems (many 0.17–0.30 dex, from Geha 2026; Segue 1 0.59,
Columba I 0.71; Tucana IV, Grus I, Pictor II upper limits), read ~35 S19 σ values (often 0.4–0.95, e.g. UMa I 0.62 vs LVD 0.24),
the first rows of Geha's table, and the Walker row counts per target. A back-of-envelope gave, for UMa I at σ = 0.24, an L about
2.8× below E6's (about 8× at its 2σ-low width). No threshold above was moved after that; the band edges are analytic.

Compute: one thread, nice 15, < 1 GB, minutes. Nothing downloaded. Writes only inside this lane.
