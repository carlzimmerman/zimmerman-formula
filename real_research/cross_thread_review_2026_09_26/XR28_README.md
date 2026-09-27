# XR28 — can the outskirts of galaxy clusters measure the chain's band-pass length L?

Cross-thread review, 2026-09-27. Three scripts and a shared module in this folder, read-only on every other file. Each script
has pre-declared checks, a MUTATE run that must fail (and does: rc = 1), and outputs `<name>.out` / `<name>_results.json`
(`_MUTATE` versions for the control). Both a0 footings are carried: canonical 9.3603 × 10⁻¹¹ and alt 1.1312 × 10⁻¹⁰ m s⁻².
κ = ½ is FITTED and does not enter beyond a0; no constant is added. The dark mass is still required, and it is the chain's own
fluid (FK1/FP10), not a particle species.

## The answer

**Yes, and they cut L from above.** The chain's band-pass makes every isolated system Gauss-compensated (FP6 G6e): the
phantom's enclosed mass rises inside ~L and is paid back just outside. At cluster mass this leaves a **compensation trough** in
the lensing density:
- It sits at 1.7–2.9 L(z) for L0 = L(z = 0) ≥ 1 Mpc, i.e. at 1.1–1.6 r200m at H_Y's length, just outside the splashback radius.
- It often drives the 3D lensing density (Newton + phantom) **negative** in a thin shell (ACT-DR5 mass, H_Y: at 1.36–1.45 r200m).
- Its position tracks L(z), not the cluster mass: at H_Y it is 2.06–2.79 L(z) in four samples whose r200m spans 0.34 dex
  (0.13 dex in units of L(z); read from the recorded JSON, not a pre-declared check -- see O3 below).
- The phantom is a large part of the lensing mass: at matched lensing M200m, the lensing M200m exceeds the Newtonian M200m
  (each at its own r200m) by 32–34% at 4.8 × 10¹⁴ h⁻¹ and 87–97% at 1.8 × 10¹⁴ h⁻¹ (H_Y, canonical / alt).

Read the way the observers read the sky (projection to ΔΣ and Σ_g, DK14 fit with Shin et al. 2021's priors), the chain moves
the splashback **inward** and makes the lensing slope **steeper**:

| sample (published) | probe | measured r_sp/r200m, γ(r_sp) | LCDM, same machinery | chain at H_Y (L0 = 1.688), canonical / alt |
|---|---|---|---|---|
| ACT-DR5 × DES-Y3, 4.8 × 10¹⁴ h⁻¹, z = 0.46 (Shin+2021, SZ) | WL | 1.16 +0.21/−0.29, −3.42 +0.54/−0.40 | 1.12, −3.22 | 0.89 / 0.87, −4.27 / −4.39 |
| | galaxies | 1.10 +0.06/−0.14, −3.40 +0.32/−0.17 | 0.94, −2.99 | 0.87 / 0.86, −2.84 / −2.86 |
| DES-Y1 redMaPPer, 1.8 × 10¹⁴ h⁻¹, z = 0.41 (Chang+2018, optical) | WL | 0.97 ± 0.15, −3.5 ± 0.4 | 1.06, −3.19 | 0.91 / 0.88, −4.48 / −4.64 |
| | galaxies | 0.82 ± 0.05, −3.6 ± 0.3 | 0.88, −2.93 | 0.62 / 0.61, −2.99 / −3.01 |

The two massive samples (CCCP, Contigiani+2019, WL 1.34 +0.45/−0.26; Planck SZ, Zürcher & More 2019, galaxies 0.92 +0.13/−0.15)
cannot be scored by the forward-fit: for the LCDM control itself the DK14 fit puts the steepest slope at the window's edge
(the model's feature is too weak there at the published precision; CCCP itself reports no significant steepening). They are
reported with the 3D read-out only (O1b).

## Can the data pin L?

Δχ² of the chain against the LCDM control, on the published r_sp/r200m and γ(r_sp) of DES-Y1 and ACT-DR5 (WL and galaxies,
8 numbers; pulls capped at |5|), both footings (canonical / alt):

| L0 [Mpc] | 0.5 | 0.75 | 1.0 | 1.3 | **1.688 (H_Y)** | ~1.99 (H_K1, interp.) | 2.2 | 2.9 | 5.0 | ∞ |
|---|---|---|---|---|---|---|---|---|---|---|
| all four probes | +19.5 / +19.7 | +5.8 / +5.7 | **+3.8 / +4.6** | +14.7 / +20.2 | **+26.9 / +32.8** | +29.5 / +36.7 | +31.1 / +39.2 | +43.2 / +51.3 | +52.7 / +37.9 | +42.1 / +26.0 |
| SZ sample only (ACT-DR5) | +0.9 / +1.1 | +0.7 / +0.6 | +1.7 / +1.6 | +2.1 / +2.4 | +8.2 / +9.7 | +12.1 / +14.7 | +14.4 / +17.7 | +20.7 / +23.2 | +30.3 / +16.0 | — |
| outer-ΔΣ shape proxy (reported) | 12.5 / 16.8 | 14 / 18 | 28 / 36 | 45 / 59 | 62 / 81 | — | 78 / 98 | 94 / 113 | 143 / 168 | 789 / 856 |

- **Excluded (Δχ² > 9 on both footings): L0 = 0.5 and every L0 ≥ 1.3 Mpc**, including H_Y (1.688), H_K1 (FP19, L0 = 2.9 Ω_L =
  1.99, window 1.82–3.16; interpolated) and H_S's band (1.87–3.25; grid points 2.2 and 2.9). L = ∞ (no band-pass) is excluded too.
- **Allowed (Δχ² ≤ 4 on both footings): nothing.** The least disfavoured is **L0 ≈ 0.75–1.0 Mpc** (+3.8 to +5.8).
- On the cleanest sample alone (SZ-selected ACT-DR5), L0 ≤ 1.3 Mpc passes (≤ +2.4), H_Y is marginal (+8.2 / +9.7), H_K1 and H_S
  are excluded (≥ +12). The optical sample's pull on L0 = 0.5 comes from a window-edge read-out and is soft.
- The shape proxy (R ≥ 0.8 h⁻¹ cMpc, free amplitude, Shin et al.'s 8.7% per-bin precision -- **not** their data vector) fails
  at every L0: at H_Y the ACT-mass ΔΣ is +16–24% at 1.2–2.4 h⁻¹ cMpc and −14–16% at 3.4–4.9 h⁻¹ cMpc against LCDM's shape.

So the outskirts put an **upper bound L0 ≲ 1–1.3 Mpc**, and every separator's window sits above it: H_Y (1.688; its KiDS floor
L(0.25) ≥ 1.2 Mpc means L0 ≥ 1.56), H_K1 (1.82–3.16) and H_S (1.87–3.25). Combined with the KiDS floor this is a **KiDS–cluster
pincer on the band-pass length**. Two cautions: the KiDS side was scored with FP6's projector (FP20 re-scored it: FP9's z = 0.25
pass stands); and the WL-slope part of the exclusion depends on the dark-sector reading by up to 0.55 (see below) -- under the
"front" and "turnaround" readings H_Y's SZ-only Δχ² falls to +3.4 / +6.4 and +4.2 / +5.8 (canonical / alt; computed from the
hot-phase JSON's read-outs against the outskirts LCDM control; the halo-only reading gives +10.3 / +13.0), so on the SZ sample
alone H_Y is not excluded under every reading; the optical sample and the shape proxy still exclude it.

## The recaptured hot phase (`XR28_hot_phase.py`)

At H_Y's L, five readings of the chain's own conversion rules (cold reference; halo escape only, the largest cold phase;
nominal with XR19's web epochs; conversion at turnaround, XR19 I1; conversion at the front, FP10 A6) and v_k = 575/600/650 km/s:

- **No distinctive signature.** The 3D dark-matter slope minimum moves by −1.31 to +0.19 against the cold reference
  (noise-level, either sign): HP1's pre-declared "≥ 0.5 shallower in every bracket" **fell**.
- **No second caustic** from the hot phase (1 of 32 runs has one, and it is the cold reference).
- **Without the phantom**, the hot phase alone moves the dark-matter splashback by ≤ +6% (ACT mass: 1.077 vs 1.012 r200m).
- Why: about half the fluid escaped sub-haloes at z ≈ 5–13 and is Hubble-cooled to ~100 km/s before cluster infall; the ~30%
  converted in the web at z ≈ 1–2 arrives at ~300–400 km/s; both are small against infall speeds of ~1500 km/s. The lensing
  signature is the phantom's, not the dark sector's.
- **The L-verdict's dependence on the dark reading:** WL r_sp/r200m moves by only −0.057 to +0.044 across readings, but the WL
  slope by −0.19 to +0.55 (turnaround and front readings shallower). HP2's pre-declared 0.5 bound **fell** by 0.05.
- The galaxy-to-lensing splashback ratio: ACT mass 0.91–0.99 (data 0.95); DES mass 0.60–0.72 (data 0.85): the phantom pulls
  baryonic tracers in much more than dark matter at low mass.

## Checks

**`XR28_outskirts_L.py`** (main 8/10, rc = 1; MUTATE rc = 1):

| Check | Result |
|---|---|
| O1 control | The LCDM model's read-outs of the scored SZ sample: pulls −0.13 (WL r_sp), +0.38 (WL γ), −1.11, +1.29 (galaxies). Pass. |
| O1b (reported) | 3D read-out vs every sample (LCDM / H_Y): CCCP −1.87 / −1.25, Planck +0.58 / +1.37, ACT WL −0.29 / −0.31, DES galaxies +4.21 / +3.07. |
| **O2 FELL** | "The trough at 1–3 L(z) for every finite L0": 64/64 runs have a trough, but for L0 = 0.5–0.75 (L(z) = 0.3–0.5 Mpc, below the clusters' baryon extent) it sits at up to 5.17 L. For L0 ≥ 1 it is at 1.66–2.90 L. |
| **O3 FELL** | "At H_Y the trough radius varies ≤ 0.15 dex across samples": 0.22 dex in physical radius (2.14–3.58 Mpc). The check compared samples at different z; in units of each sample's L(z) the spread is 0.13 dex (post-hoc reading, not a check). |
| O4 pass | The published r_sp/γ exclude L0 = 0.5 and every L0 ≥ 1.3 at Δχ² > 9 on both footings. |
| O5–O8 (reported) | The allowed range (none at ≤ 4 on both footings); the shape proxy (fails everywhere); ν_mono at H_Y (WL 0.86 / 0.84 vs P2 0.89 / 0.87: same verdict); L = ∞ (+42 / +26; shape 789 / 856). |
| H (reported) | H1 (H_Y excluded) held; H2 (L0 in [1, 3.25] fails the shape proxy) held; H3 (galaxies ≥ 10% inside LCDM at H_Y) **fell** (ACT 8%; DES 30%); H4 (footings agree) **fell** (L0 = 1.0: +3.8 vs +4.6 straddle the ≤ 4 line). |

MUTATE (band-pass removed, L = ∞ in every chain run): O2 and O3 fail with no trough at all (0 of 64). rc = 1.

**`XR28_hot_phase.py`** (main 3/5, rc = 1; MUTATE rc = 1): HP1 and HP2 fell as above; HP3–HP5 reported. MUTATE (every bracket
forced cold) makes HP1 fail with Δγ = 0 exactly. rc = 1.

**`XR28_controls.py`** (main 10/11 after the K5b re-run, rc = 0; MUTATE rc = 1):

| Check | Result |
|---|---|
| **K1** Bertschinger (1985) | Self-consistent self-similar collisionless solution (EdS, point-mass seed): caustics at 0.3656 / 0.2373 / 0.1800 r_ta against the published 0.364 / 0.236 / 0.179 (as quoted by Wang, Wang & Mo 2022, A&A 667, A99): 0.43 / 0.56 / 0.56%. |
| **K2** Adhikari, Dalal & Chamberlain (2014) | Their toy model with Λ against their eq. (3): ratios 0.904–1.093 over s = 1–3, Ω_M = 0.3–1; 1.005 / 0.995 / 0.980 at s = 1. |
| **K3** XR19 (committed b55775ce0) | A daughter's comoving reach from z_e = 1 at 600 km/s: 4.945567068731957 Mpc, bit-identical to XR19's committed R table (read with `git show`); quadrature agrees to 8e-8. |
| **K4** the phantom | Equals FP6's committed `phantom()` to 4.6e-8 (M_b 1e11–1e14 Msun, L 0.5–3 Mpc, both footings); L → ∞ gives the unfiltered P2 phantom to 3e-13. |
| **K5** projection | Uniform-shell ΔΣ vs Wright & Brainerd's NFW: 6.6e-4. The DK14 forward-fit recovers a known r_sp to 0.7%. |
| **K5b** FP20's test cases | See "The projection" below. |
| K6 (reported, as first written) | FELL and kept: the unsmoothed t = 0 member with an unwindowed read-out is not converged (an inner 1-D caustic read as splashback). |
| **K6b** production configuration | 1200 shells, ds = 0.0005 and 4 kick nodes move the DK14 WL and galaxy r_sp/r200m by ≤ 4.3% (LCDM), ≤ 3.3% (chain at H_Y), ≤ 0.2% (chain at L0 = 0.75). |
| K7 (reported) realism | LCDM model at Γ = 2.70: 3D r_sp/r200m 1.070 vs More, Diemer & Kravtsov (2015) eq. 5 1.104; DK14 WL 1.216 vs Shin et al.'s N-body 1.07. |
| K8 (reported) | The committed inputs (FP10's A6 budget, XR19's F_tot), with sha256. |

MUTATE (K1's mass profile frozen at the initial guess; K2's halo stops growing after entry): K1 (caustics up to 7% off) and K2
(ratios 0.31–0.66) fail. rc = 1.

## The projection (FP20's audit)

FP20 (7a8c25321) listed `XR28_common.py`, `XR28_controls.py` and `XR28_outskirts_L.py` as users of L352's `project_M2` /
DE8's `esd_from_mlens` (and `esd_of_M` in the controls). That listing matches the **names** `model_esd` and a docstring phrase
("not FP6's esd_of_M"), not the code. XR28 never calls those functions. Its projector (`shell_esd_kernel`) is FP20's own exact
uniform-density-shell formula, with the mass inside the first bin kept as a central point. K5b checks it on FP20's test cases
against an independent, singularity-free quadrature:
- truncated SIS, NFW, a cored and a hollow template, at 35 kpc and the 14 WL radii: ≤ 5.7e-4;
- a compact mass passed in as extended: kept exactly (2e-16);
- the model's own histogram profiles, the path the lane uses: exact to 1e-14.

No projector was switched. K5b was added after the recorded main runs, and `XR28_controls.py` was re-run (MUTATE first, main last).

## History and disclosures

1. **Scratch explorations came first** (session scratch, not committed): the point-mass phantom at L = 0.5–5 Mpc; a cold-DM
   chain run over L0 at the ACT mass; the DK14 forward-fit on single members; the self-similar and Adhikari prototypes; the
   projection and FP6-phantom comparisons. The checks and hypotheses were written after these and before the recorded runs.
2. **The controls' first run (MUTATE) showed K6 failing** in every mode (the LCDM DK14 fit read an inner 1-D caustic as
   splashback). Before any main run the production configuration was fixed and checked (K6b): a declared lognormal apocentre
   scatter of 0.12 in r on the matter profiles (the triaxiality a spherical model lacks; Adhikari et al. 2014, Fig. 3), the DK14
   read-out restricted to [0.5, 3] r200m, ds = 0.00075. K6 is kept, reported, as it fell.
3. **A smoke run of `XR28_outskirts_L.py`** (scratch copy, reduced grid, outputs not kept) showed the forward-fit degenerate for
   the two massive samples and the trough finder catching a negative phantom density in the model's cored centre (r/L = 0.02).
   Before the recorded runs the trough search was restricted to [0.5, 6] L(z) and the **scoring rule** was declared: a
   (sample, probe) is scored only where the LCDM control's read-out is interior with fit χ² ≤ 2 N_bins; pulls capped at |5|.
4. **The runner's first attempt logged the wrong exit code** (`$?` read `date`'s status). The runs were restarted from the
   controls MUTATE with correct capture; the outputs here come from the restarted runs; each `.out` ends with its `rc=`.
5. **Before the outskirts runs**, L0 = 4.0 was dropped from the grid and a secant (log-mass) update adopted for the lensing-mass
   matching, for the time budget on a loaded machine (load average 19–21 on 16 cores). The outskirts main still took 22 min.
6. **K5b** was added after the recorded main runs (FP20 relay); the controls were re-run. The MUTATE results files were renamed
   to the folder's `_results_MUTATE.json` convention (contents unchanged; `Report` fixed).
7. **The LCDM control's DK14 read-out is fragile** on weak-feature 1-D profiles: it sits at the window edge for CCCP and Planck,
   and in the hot-phase lane's no-phantom ACT run (0.500 against 1.123 in the outskirts run). Hence the scoring rule and the
   SZ-only numbers. The chain's read-outs are stable (K6b).
8. **H_K1** is not on the grid; its Δχ² is interpolated in ln L0 between 1.688 and 2.2.
9. **Hypotheses that fell are kept as run**: O2, O3, H3, H4, HP1, HP2.

## Limits

- A 1-D spherical shell model: baryons collisionless (no gas pressure or accretion shock), no dynamical friction, no
  substructure; triaxiality stands in as the declared 0.12 apocentre scatter.
- The phantom is that of an isolated spherical system: no external field from the web, and no projection effects of optical
  selection (redMaPPer's known bias toward small galaxy r_sp is not modelled).
- The dark sector's conversion is applied as the committed histories (FP10, XR19) and brackets, not simulated.
- The forward-fit is a MAP DK14 fit with fractional errors from the published S/N, not the covariance and not an MCMC. The shape
  proxy is not a likelihood of the data.
- The chain's clusters here keep the full cosmic dark share (FP16: X-COP is already too massive). A cluster light enough to
  pass X-COP would make the phantom relatively larger and the trough deeper, so the outskirts tension is, if anything,
  understated.

## Hand-offs (the owners' calls; nothing outside this folder was edited)

1. **Separator owners (FP19 / H_K1):** cluster outskirts bound L0 ≲ 1–1.3 Mpc against H_K1's window 1.82–3.16 (a KiDS–outskirts
   pincer). The compensation trough is a derived, mass-independent signature of the band-pass (FP6 G6e).
2. **The decisive data test** is a direct fit of the chain's ΔΣ to the stacked cluster-lensing data vectors with covariances
   (ACT-DR5 × DES-Y3, DES-Y3/HSC redMaPPer) out to 20 h⁻¹ Mpc. The data vectors are not in the repository; this lane's shape
   proxy stands in.
3. **FP20:** XR28's projector is exact (K5b); XR28 can come off the P2 list.
4. **The particle-mesh track (XR21):** the trough's 3D structure around non-spherical clusters fed by filaments.

## Files

- `XR28_common.py`: shared machinery (cosmology, phantom, shell model, dark phases, projection, DK14 fit, the data table).
- `XR28_controls.py`, `XR28_outskirts_L.py`, `XR28_hot_phase.py`, each with `.out`, `_MUTATE.out`, `_results.json`,
  `_results_MUTATE.json`.
- `XR28_README.md`: this file.

## Reproduction

Run from the repository root, at most 2 workers each (the controls use one process):

```
python3 real_research/cross_thread_review_2026_09_26/XR28_controls.py      # ~9 min
python3 real_research/cross_thread_review_2026_09_26/XR28_outskirts_L.py   # ~15-22 min
python3 real_research/cross_thread_review_2026_09_26/XR28_hot_phase.py     # ~6 min
```

Prefix any with `MUTATE=1` for its control. Data sources: Shin et al. (2021, MNRAS 507, 5758, Table 3 and sec. 4); Chang et al.
(2018, ApJ 864, 83); Contigiani, Hoekstra & Bahé (2019, MNRAS 485, 408); Zürcher & More (2019, ApJ 874, 184); DK14 priors from
Shin et al. (2021, Table 1).
