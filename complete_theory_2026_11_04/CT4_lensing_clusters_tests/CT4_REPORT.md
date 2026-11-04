# CT4: lensing, clusters and the data-test programme (review lane)

Opened under `complete_theory_2026_11_04/README.md`. A review lane: nothing was computed, no grader was run, no download was made, no frozen file was edited. Every number below is read from the record, with its source. Web reading is PROVISIONAL (search snippets only, no PDFs). kappa = 1/2 FITTED. Footings (canonical 9.3603e-11, alt 1.1312e-10) are reported apart, never pooled. The cold sector stays retired. No particle. Not theory closed. Nothing here says the data favour the framework.

The object under review is the plain law, g_obs = (g_b + sqrt(g_b^2 + 4 g_b a0))/2 with a0 = kappa c sqrt(G rho_DE). Rows built for route E (PAPER54, CFG801/803/804/903, SP1, SP2) are listed only so they are not mistaken for law results.

## 1. The record

### 1a. Galaxy-galaxy lensing (KiDS-1000, Brouwer et al. 2021 isolated lenses)

| Lane | What it tested | Result | Status for the plain law |
|---|---|---|---|
| CFG801 / PAPER54 v1.0 (10-16) | route E's settled halo with an edge at 5.84 r_M | edge EXCLUDED, dchi2 +197 (R <= 0.31 Mpc), +753 (all radii) canonical; +234 / +813 alt | Route E only. The no-edge continuation is the law's own profile, and it fits poorly in absolute terms: chi2 84 on 28 dof (inner), about 160 on 52 for every model, worst in the massive bins |
| CFG885 | B21's LCDM distances swapped for the native background | SHIFTED, SAME CLASS; T 0.968-1.062, set by unknown H0 | Distances don't move any class |
| CFG903, PAPER54 (4) | catalogue two-halo term for route E | PARTIAL, about 58 % of the outer shortfall | Route E only |
| X53 / SP1 K2 | the law alone on B21 Fig-3 | chi2 160.70 canonical / 127.60 alt | Law baseline |
| LE1 (11-03) | the law under every lensing estimator on record | ESTIMATORS DISAGREE, NO DEFECT. A30 Z +9.27 / +6.52; data above the law at R <= 0.3 Mpc by **+0.089 dex** (A1) to **+0.116 dex** (G3); no single swap brings A30 within abs(Z) 2 | **The law is short, about 0.09-0.12 dex, at 35-300 kpc** |
| CX1 (11-03) | leaf-space collisions | the only line-level collision is lensing against SPARC, -0.223 +- 0.073 (3.0 sigma), one innermost radius | Lensing and SPARC disagree under the same leaves |
| REQUIREMENTS row 8 / KN1, BL1 | amplitude by colour | law: blue 0.878, red 1.313 | Red lenses need about 31 % more than the law |
| CW6 (11-04) | measured kSZ hot gas on the lenses | GAP UNCHANGED both footings. B21c red 1.313 +- 0.063 (+4.96 sigma) canonical, 1.200 +- 0.058 (+3.46) alt; blue 0.878 +- 0.074 (-1.65), 0.802 +- 0.067 (-2.94). One gas rule can't lift red within 2 sigma without pushing blue over. Inner 250 kpc gas shape assumed; no colour-split gas measurement exists | Gas doesn't close it on present data |
| NV1 / NV2 (11-04) | a non-local variable (external field E1) for the lenses | lens rebuild FAILED (486,584 vs 259,383 lenses); lenses NOT COMPUTABLE | Open; needs a deeper neighbour catalogue (download) |
| STANDING (07-11 door 3) | what the required phantom is | lensing RAR follows the dynamical RAR to about 1 Mpc (B21, Mistele et al. 2024); no particle patch supplies it | The law's shape is right in outline; the amplitude is the problem, mostly in red/massive lenses |

**Lensing requirement, in numbers.** The plain law must gain about +0.09 to +0.12 dex (23-31 %) inside 0.3 Mpc on the stack, and the gain must be colour-dependent: red lenses about x1.31 (canonical) / x1.20 (alt), blue lenses not at all (they sit at 0.88 / 0.80, i.e. already at or below the law). Whatever does this must leave SPARC rotation curves alone (CX1: -0.22 dex lensing-vs-SPARC tension at matched leaves).

### 1b. Cluster cores, mergers, groups

| Lane | What it tested | Result |
|---|---|---|
| LW1 (the law's own scorecard) | X-COP, keys, groups | X-COP **FAIL +0.467 / +0.434 dex**, M_HSE/M_law **2.93 / 2.72**; keys **10 of 15**, G-OUT-M3 +4.76; groups (Tian) PASS Z +0.31 / -0.31; Lovisari B2 FAIL +3.71 / +3.32 |
| Board warning | FG1/PAPER67's X-COP -0.151 | CS2's Burkert row, **not the plain law**. DR1 plain is +0.467 (rms 0.476) |
| DR1 | a density term in the law | closes 16 % of the X-COP deficit in dex (+0.467 to +0.393); the S needed is median 34 against a ceiling of 3; breaks SPARC |
| LM1 | map of the law's deficit (eRASS1 x KiDS) | missing mass about **8 x gas at 0.2-0.5 R500, 5 x at 0.5-1 R500**; lensing/law 1.9-2.6 at 0.18-0.8 Mpc, falling to about 1.0 by 1.7 Mpc |
| GM1 | is the deficit tied to gas? | NOT: stable inside KiDS and reaches X-COP's HSE masses, but HSC lensing reads it about 1.7 x higher; "tracks gas" can't be told from "tracks M500" |
| HX1 | one boost B(sigma) of the law's phantom | NO LADDER both footings. B needed: X-COP **4.09 / 3.66**, MaNGA Q4 ellipticals 4.22 / 3.73, Lovisari groups 1.5-2.5, Tian groups 1.18 / 1.08; X-COP need falls as x^-0.33 (Z -12.8) |
| MB1 | member galaxies' bound law halos | no hit. Tidal (F) short by 16.1 / 13.3 x; external-field (E) short 114 / 90 x; N (unscreened to 300 kpc) passes Bullet but over-masses outer keys; K needs about 50 x M_star, fitted |
| DB1 | Milgrom's cluster baryonic dark matter, ordinary mass | every arm FAILS. Needs M_cb/M_gas about 5 at 300 kpc; the requirement arm gets 14/15 keys and still fails the Bullet (main M300 4.84e14, over). Cold clouds have no window (factor 3.7); only 1e2-1e7 Msun black holes survive the order-of-magnitude gates, with no origin |
| Bullet, the law alone (DB1/MB1 K4) | | FAIL: M300 1.11e14 / 0.73e14, dkappa -0.068 / -0.111 (lensing peak on the gas, wrong sign) |
| REQUIREMENTS rows 9, 10 | | add mass in cores, A 1.91 +- 0.12 at 0.5-1.2 Mpc; outer shear slope on M_gas 0.47 against 0.90 +- 0.21 |
| CX1 / NP1 / NP2 | is the cluster need a data contradiction? | No: X-COP has no neighbour in leaf space (d_L >= 8.3). A smooth leaf rule can carry it (NP1), but every such rule fails elsewhere (IC 1613, A5-A7, lensing A30, dwarfs) and RQ3 rejects it |
| AN1 (AeST-class dust, reduced system) | does an AeST-like dust settle in cluster wells? | NO VERDICT; the two non-folding rows hold about 3 % of the law's phantom inside R500, far from X-COP's window |

**Cluster requirement, in numbers.** Inside R500 the plain law needs its gravity raised by a factor about 3-4 (X-COP: M_HSE/M_law 2.93 geometric; B 3.7-4.1 on the phantom), equivalently extra mass about 5-8 times the gas at 0.2-1 R500, falling outward to nothing measurable by about 1.7 Mpc. In the Bullet the extra mass must ride with the galaxies, not the gas. Groups need little (B 1.1-1.5), massive ellipticals as much as clusters (B 3-4): the need is not ordered by sigma, by gas, or by any single leaf on record.

### 1c. Data tests on record

| Test | Decides | Record | Status |
|---|---|---|---|
| ALMA MOUS uid://A001/X3788/Xbfd2, U4_28473 CO(3-2), PAPER66 v1.4 (DOI 10.5281/zenodo.23958256) | the mass budget of one z 2.52 disc; **not a0(z)** | FN2: date confirmed 2026-11-06 02:42:31 UTC, scorer ENV IDENTICAL, known answers 7/7; row A's MUTATE hollow on spw23 | **Download approved by the owner 11-04** (34.7 + 38.6 GB streamed, cutouts kept); run scheduled 22:15 ET Nov 5. One disc excludes no model |
| GS4_24110 [CI](2-1) | CFG809 scoring of one disc | release 2026-11-28 18:25:24 UTC; frozen MUTATE can't run on the window | **Approved** (7.0 GB + 14.8 MB); the owner triggers the run |
| Gaia DR4 wide binaries | the law's external-field-effect boost at 2-30 kAU | release 2 Dec 2026 (ESA page, PROVISIONAL). Bare-law rule exists (D2 note + A1-A3): law-first excluded iff Arm A floor - gamma_hat >= 3 sigma, i.e. gamma_hat <= 1.079 canonical / 1.109 alt; CW1's plain QUMOND through the frozen pipeline gives **1.149 +- 0.027 / 1.208 +- 0.007**, Newton 1.002 / 1.010; separable. s^TX bands VOID under alpha = 2 (Amendment 5). Amendment 7: sigma_sys 0.02 is irreducible | Frozen. The anchor is Arm A's floor (1.1614 / 1.1917), not the bare law's own number; optional owner clarification before 2 Dec (FN2 owner item 3). **Catalogue download needs the owner's go** |
| a0 tracking rho_DE vs H(z) (AT1, CFG689) | sqrt(X(z)) (flat within about 1 sigma: 0.91 / 0.94 / 0.91 at z 1.0 / 1.5 / 2.33) vs H/H0 (1.76 / 2.35 / 3.49) | AT1 Lean-certified rule: decisive only if the non-cancelling common mode < **0.055 / 0.072 / 0.074 / 0.084 dex** at z 1.0 / 1.2 / 1.5 / 2.33; then N_min 41 / 8 / 7 / 5 at 0.14 dex per galaxy. At c 0.075 only z 2.33 is open. C3 fails: a powered sample can still land INCONCLUSIVE | No public sample passes (CFG685 best 0.4-0.5 dex). KURVS (CFG160) is a conditional lean to H(z), flips with unmeasured gas (break-even mu 2.1 flat / 0.65 rival). KURVS-15 archival CO(2-1) would measure that gas: **imaging needs the owner's go** |
| kappa 1/2 vs 0.461 (KC1) | the coefficient | needs sigma(a0)/a0 <= **2.8 %**; galaxy floor 9.3-9.5 % (gas scale, shared, N-independent), best case 3.5 %; rho_DE native +-3.7 %; combined best about 5 %, under 2 sigma | Needs new observations: single-dish HI recalibration of gas-rich dwarfs to about 3 %, measured CO-dark H2, TRGB distances for WALLABY discs, a Planck-free rho_DE to <= 2 % on a0 |
| Directional EFE (STANDING 07-11 to 09-02) | aligned outer-disc asymmetry, QUMOND +1-4 % | WALLABY-25: A_hat -1.70 +- 2.12 (an amplitude, Z -0.57); n = 16: +2.95. Detection vs null needs N about 560; R3 deep null N about 1,160 | Open, underpowered; WALLABY / MaNGA scale needed |
| Cluster lensing outer slope (COS1) | law's ESD slope past R500 | 3 sigma needs about 4.3e3 cluster lenses; nothing on disk reaches 1.4 R500 | Open; Euclid/eRASS-class data |
| Euclid D2 exact-null prereg (07-16) | Branch B kink | written for the retired Branch B | **Not a plain-law test**; do not score it as one |
| SP1, SP2 sealed lensing | route E's halo switch and basin step | sealed | **Moot for the plain law**: the law branch predicts no step (ratio 1.00 at all radii) |

## 2. Requirements and the literature (provisional)

### (a) Lensing
The gap is +0.09-0.12 dex at R <= 0.3 Mpc on the stack, carried by red lenses (x1.31 / x1.20), with blue lenses at or under the law. Not an estimator artefact (LE1), not distances (CFG885), not the measured kSZ gas as profiled (CW6). Two readings are still open on the record, both data-limited: (i) more hot or cool gas concentrated inside 100 kpc in quiescent L* galaxies (no measurement exists there, CW6 caveat 2); (ii) an environment (external-field) dependence that the isolated-lens rebuild could not compute (NV2). Mistele, McGaugh and Hossenfelder (arXiv:2301.03499, provisional) confronted AeST with KiDS lensing at small accelerations; their result constrains AeST's mass term, it does not close a colour-dependent amplitude gap.

### (b) Clusters
The missing factor is about 3-4 in gravity inside R500 (5-8 x gas in mass), falling outward. This matches the literature's long-standing MOND cluster residual: Kelleher and Lelli 2024 (A&A 688, A78, five X-COP clusters, provisional from the abstract) find missing-to-visible about 1-5 at 200-300 kpc falling to 0.4-1.1 at 2-3 Mpc in relaxed clusters, and the MOND review literature (Famaey and McGaugh 2012; arXiv:2501.17006) records central dynamical-to-baryonic ratios up to about 10 under the MOND recipe. Cluster baryonic dark matter (Milgrom 2008) is DB1's arm and fails on the record.

**Do the action classes CT1 is likely to propose close it?** Not on any published result I could find:
- **AeST / khronon-type.** Durakovic and Skordis (arXiv:2312.00889, JCAP; provisional) solve isothermal spheres. They find an oscillatory regime past the MOND regime and a possible RAR peak above MOND, and say this "illustrates the potential", with a full quantitative comparison still to come. No published AeST fit to X-COP or the Bullet exists that I found. The record's own AeST-like dust (AN1) holds about 3 % of the needed phantom. AeST's cosmological dust-like component is the obvious carrier, but at that point the cluster mass is a cold component, which the owner retired on 11-01. If CT1 proposes AeST, the cluster question becomes whether its dust settles in cluster wells without settling in disc galaxies. The record's whole 09-10 history (BSK3, L341-L364, the dark-sector no-go) says this is where every such construction has broken.
- **k-essence (P(X) scalar, RAQUAL-like) and Einstein-aether MOND-like theories.** In the quasi-static limit they reproduce a MOND/QUMOND force law, and the plain law already fails clusters by a factor of 3-4. None adds cluster mass without an extra component or an extra scale. HX1 shows that no single extra scale on record orders the need, and DR1 shows that a density term can't reach it.
- **Honest summary.** The cluster gap has resisted every MOND-type theory for about 25 years (TeVeS, EMOND, sterile-neutrino MOND, superfluid DM, which needs a particle, and CBDM). The record adds about 30 failed rules of its own. No action class on record or in the literature reads closes it without matter that is not ordinary baryons, and that is excluded here by the no-particle rule and the 11-01 retirement. CT1 should treat clusters as a requirement any candidate action must be graded against, not one it can expect to pass.

## 3. Prioritised, dated test plan

Downloads flagged **[DL]** need the owner's go, unless already approved.

| P | Test | Decides | Sample / precision needed | Source, date | DL |
|---|---|---|---|---|---|
| 1 | Gaia DR4 wide binaries, frozen D2 rule | the law's boost at 2-30 kAU: plain QUMOND 1.149 / 1.208 vs Newton 1.00; law-first excluded at gamma_hat <= 1.079 / 1.109 | frozen pipeline; sigma_sys 0.02 irreducible (best about 1.55 sigma on a 0.03 signal, Amdt 7, but 5.7-8.2 sigma_tot plain-vs-Newton per CW1); report raw gamma_hat plus both distances | ESA, **2 Dec 2026** (provisional) | **[DL] needed** (owner go; size to be stated) |
| 2 | ALMA U4_28473 | one disc's mass budget; one disc excludes no model | as frozen (PAPER66 v1.4) | **6 Nov 2026** 02:42 UTC | approved |
| 3 | GS4_24110 | one disc, CFG809 | as frozen | **28 Nov 2026** | approved |
| 4 | KiDS lensing by colour and environment | is the +0.09-0.12 dex gap red-only and external-field-dependent? Lensing at large radii: the law predicts no edge to the EFE radius | rebuild the B21 isolated sample (NV2 failed: 486,584 vs 259,383 lenses), a deeper neighbour catalogue for E1, a colour-split hot-gas profile inside 100 kpc | KiDS-1000 public now; KiDS-Legacy public; Euclid DR1-Foundation about Nov 2026, full DR1 about mid-2027 (ESA 15 Jun 2026 revision, provisional; the older 21 Oct 2026 date is superseded) | **[DL]** |
| 5 | a0 tracking rho_DE vs H(z) | sqrt(X) vs E(z) | AT1: common mode < 0.055-0.084 dex; N 5-41 deep-MOND discs at z 1-2.33; measured gas is the binding term (KURVS flips with mu) | KURVS-15 archival CO(2-1) now; new JWST NIRSpec + ALMA CO(3-2) programmes (z 2.3-2.9 funnel, DOI 10.5281/zenodo.22563139); years | **[DL]** for KURVS-15 imaging |
| 6 | Directional EFE | QUMOND's aligned +1-4 % asymmetry vs null | N >= 560 detection-vs-null; about 1,160 deep null | WALLABY kinematic releases, MaNGA DAP (public) | **[DL]** |
| 7 | Cluster lensing past R500 | the law's outer slope and the falling need (LM1) | about 4.3e3 cluster lenses for 3 sigma (COS1) | eRASS1 x KiDS now (in record); Euclid clusters 2027+ | **[DL]** for new |
| 8 | kappa 1/2 vs 0.461 | the coefficient | sigma(a0)/a0 <= 2.8 % (now best about 5 %) | single-dish HI recalibration, CO-dark gas, TRGB for WALLABY discs, Planck-free rho_DE (DESI DR2+ BAO + SN); new observations, years, not archive | new observations |

## 4. Gated sequence

1. **Now to 2 Dec (no new lanes needed).** Run the approved ALMA (Nov 6) and GS4 (Nov 28) scorers as frozen. Before 2 Dec, the owner decides FN2 item 3: whether to file a dated clarification of the D2 law-first anchor (Arm A floor, A1's AQUAL value, or CW1's bare-law 1.149 / 1.208). Gate: no anchor change after any DR4 byte is seen.
2. **2 Dec onward.** On the owner's [DL] go, score DR4 with the frozen pipeline. Report raw gamma_hat and both distances, never one verdict word. Gate: Amendment 7's label rule; s^TX not scored (VOID).
3. **Lensing (parallel, gated on a [DL] go).** Freeze criteria for a colour-by-environment split of B21 lenses: the red gap must shrink with external field if the law's EFE is the cause, and stay if it is not. Prerequisites: the lens rebuild must reproduce 259,383 lenses (NV2's failed check), and the expected sign must be stated before any number. A colour-split inner gas profile, if one exists in the literature, is read before freezing.
4. **Clusters.** No new rule lanes: about 30 rules on record fail, and HX1/GM1 show no ordering variable. Use clusters only as a grading row for any CT1 action. A candidate must state its X-COP factor (3-4 needed), its Bullet sign and its group value before it is run.
5. **a0(z) and kappa.** No archive test can decide either (AT1, KC1). Gate: reopen only when a sample with measured gas reaches AT1's common-mode line, or one of KC1's new observations exists. The KURVS-15 CO imaging is the one archive step that would move the KURVS lean; it needs the owner's [DL] go.

Sources (web, provisional): Durakovic and Skordis, arXiv:2312.00889 (https://ar5iv.labs.arxiv.org/html/2312.00889); Kelleher and Lelli 2024, A&A 688, A78 (https://www.aanda.org/articles/aa/full_html/2024/08/aa49968-24/aa49968-24.html, arXiv:2405.08557); MOND review arXiv:2501.17006; Mistele, McGaugh and Hossenfelder, arXiv:2301.03499; ESA Euclid DR1 timeline (https://www.cosmos.esa.int/web/euclid/dr1-timeline) and the 2026-06-16 revision note (https://telescoper.blog/2026/06/16/euclid-update-revised-timeline/).
