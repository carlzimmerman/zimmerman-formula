# CFG633: read-and-map note on two Nature Astronomy items (tidal-torque memory; "ΛCDM in a courtroom")

**Type.** A READ-AND-MAP note. No script, no data download, no simulation, no verdict on the framework. It maps two published items onto the committed record. κ = ½ is fitted. The footings (9.36e-11 / 1.13e-10 m s⁻²) are never pooled. The cold energy's mass is still required. This is not "theory closed".

**Sources and how they were read.**

| item | version read | how |
|---|---|---|
| Sheng, Yu, Bao, ..., Pen, Wang, Yang, "A high-significance detection of primordial tidal torque imprints", Nature Astronomy (published 5 Aug 2026; DOI 10.1038/s41550-026-02948-w) | arXiv:2512.11383v2 (5 Aug 2026), full HTML | **VERBATIM**: the arXiv HTML was converted to text locally and every number below was read from that text |
| Kang, "Persistent primordial signature in present-day galaxies", Nature Astronomy News & Views (28 Sep 2026; DOI 10.1038/s41550-026-02979-3) | **NOT READ** | paywalled (nature.com redirects to login). Only a search-engine summary was seen: that the piece calls the result a more robust test of tidal-torque theory "while revealing an unexpected puzzle for galaxy formation". That summary is **PROVISIONAL**, and what the puzzle is has not been checked |
| Lahav & Shah, "ΛCDM in a courtroom", Nature Astronomy Perspective (accepted; October 2026 issue) | arXiv:2609.16097v1 (14 Sep 2026), full HTML | **VERBATIM**, as above |

---

## Part 1. The tidal-torque memory detection

### 1.1 What is measured

- **Observed spin, j_G.** This is the 2D projected spin (perpendicular to the line of sight) of 781 central ellipticals (ionized gas), 815 central spirals (gas), 635 ellipticals (stars) and 812 spirals (stars).
  - It comes from MaNGA DR17 kinematic position angles, fitted with PAFIT, with an Hα S/N ≥ 3 spaxel cut and a PA error ≤ 20°.
  - The sense of the spin is set by the receding and approaching sides.
  - Morphology comes from the MaNGA deep-learning VAC.
  - Only centrals in groups with M_h ≥ 10¹² M☉ inside the ELUCID volume are used.
- **Predicted spin, j_R.** This is a "spin reconstruction" proxy, j_α ∝ ε_αβγ T^r_βκ T^R_κγ. T^r and T^R are the initial tidal tensors of the reconstructed primordial potential, Gaussian-smoothed on two neighbouring scales with R → r⁺ and r ≈ 0.8 r_q.
  - r_q = (2 G M_h / Ω_m H₀²)^{1/3} is the halo's Lagrangian radius.
  - The proxy stands in for the unobservable protohalo inertia tensor in the classic TTT form J ∝ ε I T.
  - It is evaluated at the protohalo's Lagrangian position, then projected onto the sky.
- **Statistic.** μ is the weighted mean of cos θ between j_G and j_R, with weights β_TT^{1/2}. β_TT is the two-scale tidal-twist strength, and the ^{1/2} power is taken from simulations. The null mean is 0, since 2D random vectors give an arcsine distribution.
  - The null distribution comes from 40,000 shuffles of the observed spins within halo-mass bins.
  - Z = Σ(μ_i − μ_null,i) / (Σσ²_null,i)^{1/2} over the mass bins, with the lowest-mass bin excluded. The paper says this is approximate, because every bin shares one reconstructed field.

### 1.2 How the initial field is reconstructed, and what ΛCDM goes into it

Each step below is from the Methods (verbatim read).

1. **Present-day density.** It is built from the SDSS DR7 halo-based group catalogue (Yang et al.), NGC only, 0.01 ≤ z ≤ 0.12, groups ≥ 10¹² M☉.
   - Halo masses come from **abundance matching** of group luminosity or stellar mass, which needs a halo mass function. That mass function is ΛCDM's. The quoted mass error is a few tenths of a dex, from ΛCDM mocks.
   - Fingers of God are suppressed and the Kaiser effect is corrected (linear growth rate, ΛCDM).
2. **Initial field.** It is inferred by Hamiltonian Monte Carlo with a 20-step particle-mesh forward model in a 500 Mpc/h box on a 500³ grid (1 Mpc/h cells). The forward model uses ΛCDM gravity and the **WMAP5 ΛCDM** parameters (Ω_m 0.258, Ω_Λ 0.742, h 0.72, σ₈ 0.796, n_s 0.963). Running the reconstructed field forward reproduces the observed structure down to about 2 Mpc/h (halos of about 10^12.5 M☉).
3. **Lagrangian remapping.** Each halo is mapped back to its protohalo position with the inverse displacement field of a **constrained ΛCDM N-body run** (CUBE2 P³M, 500³ particles, Zel'dovich start at z = 100).
4. **Calibrations taken from ΛCDM simulations.** The 0.8 r_q scale, the R → r⁺ choice, the β_TT^{1/2} weight, and the expected size of the signal all come from simulations. The paper's own numbers for the simulation chain are: protohalo vs late-time halo spin correlation about 0.7; TTT or proxy vs protohalo 0.5–0.6; baryonic galaxy spin 0.3–0.5. These exclude reconstruction, remapping, PA, projection and mass errors.

So the *initial tidal field* is ΛCDM-conditioned in its dynamics, its parameters, its halo masses and its remapping. The *observed spins* are raw IFU kinematics.

### 1.3 Results (verbatim)

| quantity | value |
|---|---|
| strongest population | gas in central ellipticals, μ = 0.13 at the optimal smoothing scale |
| significance, fiducial (scale optimised on the data; shuffles at that fixed scale) | 7.0σ |
| significance, fixed a-priori scale 0.8 r_q | Z = 6.3σ |
| significance, scale re-optimised in every shuffle (the fair look-elsewhere version) | Z = 5.9σ |
| mass dependence | optimal smoothing scale rises with M_h for M_h > 10^12.5 M☉, along 0.8 r_q; the lowest bin decorrelates (remapping and reconstruction errors) |
| spirals and stars | much weaker; spirals show a signal once low masses are cut; stars weaker than gas in both types |
| ellipticals vs spirals at fixed halo mass | ellipticals still stronger (Extended Data Fig. 3), so halo mass is not the only driver |
| earlier claim | spiral spins vs reconstructed field, about 3σ (their ref. 23) |

The defensible headline is the a-priori fixed-scale 6.3σ or the re-optimised-null 5.9σ, not 7.0σ.

### 1.4 What the framework predicts (reasoned from the axioms; no new calculation)

**Linear era: the same as CDM, by construction.** Tidal torquing acts on an expanding protohalo until turnaround. At that stage the region is not yet bound, so the switch (A5) is off and cold energy is ordinary cold matter with the cosmic amount Ω_c/Ω_b = 5.364 (A4). The initial tidal tensor, the protohalo shape and their misalignment are all built by Newtonian gravity on cold matter plus baryons. The framework inherits linear TTT whole. This is not a prediction distinctive of the framework. The record has never treated the linear era differently (CFG511: the CMB measures the cold energy's smooth mean density at z = 1100 to 1%; CFG624: that mass is required).

**After the switch turns on: no mechanism in the record that erases direction memory, and none that boosts it.**
- *Round settling (R6).* Settled cold energy is spherical and set by enclosed mass. A round halo exerts no torque on a disc, gas or stellar body inside it. So settling adds no torque, unlike a triaxial CDM halo that can realign a disc. If anything this would keep baryonic spin *closer* to its acquired direction. The record has no lane that quantifies this. The disc–halo torque in a triaxial CDM halo is one source of the 0.7 → 0.3–0.5 decorrelation in ΛCDM hydro simulations, and its size there is recalled, not checked.
- *Radial drift.* The class-A drift (CFG539) moves cold energy along −∇ψ. In a nearly round potential that is radial, so r × v keeps its direction and loses magnitude. That could change the halo's spin *magnitude* profile, never its direction. But no cold-energy EoM is viable on the record (CFG539 NO CLASS VIABLE; CFG544 kinetic consistency fails as is), so no magnitude prediction can be derived. The paper measures direction only.
- *No external-field effect (R7).* A system's internal dynamics do not depend on the field it sits in. Outside bound systems the law is off. So late tidal torques between neighbours are Newtonian on cold matter plus baryons, as in CDM. The framework gives **no dependence of alignment strength on a galaxy's internal acceleration regime (g_bar/a₀) at fixed halo mass**.
- *Mergers.* The merger lanes allow only α ≈ 0 (CFG623). Cold energy behaves collisionlessly through a merger, as CDM does. Merger-driven spin scrambling is therefore CDM-like.

**Bottom line for Part 1.** The framework predicts the **same** direction memory as CDM at the linear stage. It names one possible late-time difference: round settled halos add no realigning torque, which would leave the memory equal or slightly stronger. That difference is not quantified, and it would be swamped by the ΛCDM-calibrated noise budget (reconstruction, remapping, PA and mass errors). The measurement is **not discriminating** between the framework and CDM. It is consistent with the framework's linear-era axioms, but it is not evidence for the framework.

A framework-native caveat: the significance of the observed μ (Z ≈ 6) is raw against shuffles and does not depend on ΛCDM. The *predicted spins*, however, sit on a ΛCDM-dynamics reconstruction and ΛCDM abundance-matched masses (setting r_q). A framework-native re-reconstruction would need the framework's PM engine in the HMC forward model. That is not available, and the framework's own PM gravitating field is in tension at 512³ (CFG555). Since the framework is CDM-like on ≥ 2 Mpc/h linear-to-mildly-nonlinear scales outside bound systems, the reconstruction's *directions* should carry over to first order. Its halo masses would not: the framework's bound mass inside the supply edge is not the ΛCDM abundance-matched M_h (R2/R4; CFG594 calls the supply ΛCDM-borrowed). r_q, though, is a Lagrangian catchment scale, which R3 also defines by the turnaround sphere, so the mass–scale relation tested in Fig. 4a is not distinctive either.

### 1.5 Is there a distinctive, testable twist?

**(a) Acceleration regime: a null prediction, weakly discriminating.** At fixed M_h the framework predicts μ independent of the galaxy's internal g_bar/a₀ (R6 + R7). CDM predicts the same to first order. The null would only discriminate against theories with acceleration-dependent late torquing, and the owner rule bars using standard MOND as a yardstick. **Not worth a lane on its own.**

**(b) Age (u−r residual) at fixed halo mass: a diagnostic of the record's early-type age tension, not a framework-vs-rival test.**
- The record has an unexplained early-type age dependence. Older (redder at fixed M*) KiDS early types carry more inner lensing excess: raw ESD ratio ×1.46, Z +2.33 (CFG700); D +0.85 to +0.93, family-wise p 0.035 with colour, sSFR, photo-z and companions controlled (CFG585/586/631). The record's reading is "formation time, not composition", with no mechanism.
- Linear TTT, which the framework inherits, says an earlier-collapsing halo at fixed mass is a higher peak with a shorter torque phase and less late nonlinear accretion. So *if* the age signal is formation time, older early types should keep the primordial direction **at least as well** as younger ones: μ_old ≥ μ_young at fixed M_h.
- A clear reversal (young > old) would weaken the formation-time reading of CFG585/631. This sharpens an open tension. It does not test the framework against ΛCDM, because ΛCDM makes the same TTT statement.
- **Power is poor.** The per-galaxy σ of cos θ for 2D random vectors is 1/√2 ≈ 0.71. Splitting 781 ellipticals into thirds (about 260 each) gives σ(μ) ≥ 0.044 per third and σ(Δμ) ≥ 0.062 (unweighted lower bound; the β weights raise it). That is against a total μ of 0.13. Only a Δμ comparable to the whole signal would reach 2σ. Expect **NOT DIAGNOSTIC [LOW POWER]** unless the effect is large.

**Short spec (only if the owner approves the downloads in section 3; ID to be assigned from the free pool at the time):**
- Data: the authors' Zenodo release of per-galaxy j_G and j_R (gas, central ellipticals); MaNGA DR17 DRPall (NSA u−r, M*) and the Pipe3D VAC (light-weighted age, Dn4000) for the age proxy.
- Frozen first: (i) age proxy = u−r residual at fixed M* (the same construction as CFG585), with the Pipe3D age as secondary; (ii) OLD/YOUNG = top and bottom thirds within each halo-mass bin; (iii) statistic Δμ = μ_old − μ_young at the paper's fixed a-priori scale 0.8 r_q (no scale optimisation); (iv) null = 10,000 within-mass-bin age relabellings.
- Framework-native expectation (formation-time reading): Δμ ≥ 0. Decision: Δμ < 0 at 2σ weakens the formation-time reading. |Z| < 2 gives NOT DIAGNOSTIC.
- Controls: C1 reproduce the paper's fixed-scale μ per mass bin from the Zenodo files to ±0.005. C2 MUTATE = shuffle j_G within bins, which must give Δμ ≈ 0 and μ ≈ 0. C3 injection: rotate the YOUNG spins by a random angle drawn to halve their μ, and require that it is recovered at the forecast power.
- Footprint: one process, < 0.1 GB, nice -n 10, seconds. No simulation.
- Disclosure: this is not a framework-vs-ΛCDM discriminator. It probes the reading of the CFG585/631/700 age tension only.

---

## Part 2. "ΛCDM in a courtroom": the tensions it lists, mapped onto the record

**What the perspective is.** It is a case for and against a constant Λ versus dynamical dark energy (DDE, w₀w_a). The verdict is **"Not Proven"**. The authors warn against over-reading ~3σ frequentist results. It is mostly about dark energy, not dark matter.

**The tensions and arguments it lists (verbatim numbers), mapped onto the record.** Addresses = the record makes its own statement. Inherits = the framework takes the ΛCDM-side physics unchanged. Fails/open = a committed lane shows tension.

| # | item in the perspective | mapping | record |
|---|---|---|---|
| 1 | **DDE preference.** CMB+DESI DR2 BAO+DES-SN was 4.2σ. Newer SN (DES-Dovekie, Union3.1) bring it to 3.2–3.4σ; CMB+BAO alone 3.1σ. w₀ ≈ −0.72 to −0.80, w_a ≈ −0.72 to −0.95 | **Inherits ρ_DE(z) as an input; offers an independent measurement channel.** The framework does not predict ρ_DE(z). From its own ingredients it gives Λ plus an unobservable phantom-side settling trickle (about 1e-7 to 1e-6). Any real evolution is free (CFG549, CFG630). Its distinctive link is that a₀ tracks ρ_DE: a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)), with κ cancelling (CFG549). Galaxies at z ≈ 2–2.5 could measure that ratio independently of BAO, SN and CMB. DESI DR2 pins a₀(z)/a₀(0) to about ±0.04 dex (THEORY A3). The record's DESI-tracking curve is about 0.87 at z = 2 (chart_a0z_one.py M-DEC; DESI chain medians 0.78–0.83 at z = 2.5). No crisp test is on disk (CFG535). The sealed ALMA predictions (CFG571, 2026-11-06 / 11-28) carry both F-DESI and F-flat rows. | CFG549, CFG630, CFG535, CFG571, CFG452 |
| 2 | **Ω_m disagreement between CMB, BAO and SN** inside ΛCDM | **Inherits.** Cold energy is cold matter at cosmic scale, so Ω_m enters exactly as in ΛCDM. The record has no lane on the inter-probe Ω_m split. | (none) |
| 3 | **w ≈ −1 coincidence.** Constant-w fits give −0.971 ± 0.021 and −0.962; a DDE with mean w ≈ −1 must cross into phantom | **Partly addressed, partly open.** The framework's own channel is phantom-side by a negligible amount (1 + w ≈ −2e-7, no crossing; CFG630). The dissipative principle's canonical scalar partner cannot follow a w = −1 crossing and would need a non-canonical or multi-field partner (CFG542). If DESI's crossing is real, the framework's one principle needs an extension that is not on the record. | CFG542, CFG630, CFG549 |
| 4 | **Neutrinos.** ΛCDM CMB+BAO gives Σm_ν < 0.048 eV vs the oscillation floor 0.058 (NO); DDE relaxes this to < 0.129 | **Inherits.** The framework has no neutrino sector. One off-campaign numerology script (m₁ = ρ_Λ^{1/4}, Σ = 0.0613 eV) sits 0.06σ from minimal NO and fails the Feldman–Cousins 0.053 limit. It is not a framework prediction and is never cited as support. | real_research/neutrino_desi_2026_10_06 (commit 930394198), not a CFG lane |
| 5 | **Sound horizon.** BAO's DDE preference would drop if r_d were about 2% larger; no CMB evidence for early-universe changes | **Inherits.** The pre-recombination physics is ΛCDM's (cold energy = cold matter, switch off). | (none) |
| 6 | **CMB internal anomalies** (~2σ Planck lensing/curvature; ACT vs Planck Ω_m), and **τ.** τ > 0.07 would make ΛCDM preferable; SPT-only τ = 0.078 ± 0.013 | **Inherits.** The record does not model the CMB beyond the mean cold density (CFG511). | CFG511 |
| 7 | **SN systematics** (calibration, host-mass/dust, selection, evolution) | Not the framework's domain. The framework's a₀(z) channel is SN-independent (CFG549's stage-1 predictions used no DESI, DES or SN). | CFG549 |
| 8 | **H₀ tension** (distance ladder vs CMB+BAO+SN), not eased by DDE | **Inherits.** H₀ is an input. The record has no H₀-tension lane. a₀ = κc√(Gρ_DE) uses ρ_DE, which scales with H₀², so the two footings are partly an H₀/κ footing issue, but κ is fitted and this does not address the tension. | THEORY A2 |
| 9 | **S₈.** CMB+BAO S₈ still "moderately higher" than galaxy surveys; earlier >2σ lensing–CMB gaps reduced in DES Y6 / KiDS-Legacy | **Fails / open, in the wrong direction.** The framework's settled-halo matter power is *higher* than the data want. On its own PM gravitating field, growth fails at 512³ (0.15–0.19; σ₈ +3–5%; CFG555). The framework-native shear test leans against (KiDS Δχ² +24/+30, p 0.008/0.001) but is NOT DIAGNOSTIC as frozen (CFG592). The ΛCDM-calibrated context reading excludes the current settling rules (CFG590/591, context only). The framework does not ease S₈ and likely worsens it. | CFG555, CFG592, CFG590, CFG591, CFG593–595 |
| 10 | **DDE physics.** ρ_DE rising then falling (peak near z ≈ 0.4) is hard for quintessence | **Addressed as a consequence, not explained.** If ρ_DE has that shape, the framework's a₀ follows it: about +3.5% above today near z ≈ 0.05–0.9 for DESI medians (CFG452), and below today at z ≳ 1. That is a falsifiable corollary of A3, not an explanation of ρ_DE. | CFG452, CFG549 |
| 11 | **Dark energy–dark matter interaction** ("blending matter with dark energy"; may harm structure formation) | **Addressed, and found negligible or not preferred.** The framework has a derived energy hand-off from settling into the dark-energy partner, Q ≥ 0 (CFG542). Its size today is Δρ_DE/ρ_DE ≈ 1e-6, too small to make DESI's w(z) (CFG630). Generic cold ↔ vacuum flows are not DESI-preferred in any of four forms (CFG368; DESI-PREFERRED False everywhere; its single run check flag reads 0/1, so cite with care). A unified fluid with c_s² = 0.01 is excluded (CFG508 MUTATE). | CFG542, CFG630, CFG368, CFG508 |
| 12 | **Two dark energies** mistaken for one (Caldwell & Linder) | **Related, not the same.** The record finds dark energy and cold energy to be two components in every measured property (CFG508). That is a dark-energy / cold-component split, not two dark energies. The elastic-vacuum variant (CFG511) makes a₀ follow −p_DE rather than ρ_DE, a 0.09–0.17 dex difference at z = 2.5. | CFG508, CFG511 |
| 13 | **w₀w_a may be too crude**; structure growth and gravity tests are needed | The framework's growth sector is its main open tension (row 9). Its distinctive gravity-side prediction is the a₀(z) channel (row 1). | CFG555, CFG549 |
| 14 | **Future data.** DESI-Run2, LSST + 4MOST SN (5σ DDE "probable" if central values hold), LiteBIRD τ and σ(Σm_ν) ≈ 0.012 eV | The framework's dated tests are elsewhere: Gaia DR4 (2026-12-02; wide binaries, K_z, outer slope) and the sealed ALMA releases (2026-11-06, 11-28). A 5σ DDE result would turn the framework's a₀(z) into a firm forecast (the F-DESI rows). | THEORY §4, CFG571, CFG553 |

**Summary of the mapping (no advocacy).**
- *Addresses* (makes its own statement): a₀ tracks ρ_DE (rows 1, 10); its own DE channel is negligible and phantom-side (rows 3, 11); dark and cold energy are two components (row 12).
- *Open where the perspective's DDE is real*: the dissipative principle cannot cross w = −1 with a canonical partner (row 3).
- *Inherits unchanged*: Ω_m split, neutrinos, sound horizon, CMB anomalies and τ, SN systematics, H₀ (rows 2, 4–8).
- *Fails / open*: S₈ and growth. The framework's halos add clustering where the data want less (row 9).

The perspective's "Not Proven" is about Λ vs DDE. The framework takes no side on it: it measures, rather than predicts, ρ_DE(z).

---

## 3. Downloads that would need the owner's approval (none made)

| file | source | size | purpose |
|---|---|---|---|
| Per-galaxy observed and reconstructed spins + notebook (9 files: `jG_*`/`jR_*` for elliptical/spiral × gas/star, `TTT_main.ipynb`) | Zenodo 10.5281/zenodo.20263913 | 7.10 MB total (sizes from the Zenodo API metadata) | the age-split diagnostic in 1.5(b); whether the files carry MaNGA IDs and halo masses must be checked on arrival |
| `drpall-v3_1_1.fits` (MaNGA DR17 summary; NSA M*, colours) | data.sdss.org/sas/dr17/manga/spectro/redux/v3_1_1/ | 75.4 MB (HTTP HEAD) | age proxy (u−r residual at fixed M*) |
| `SDSS17Pipe3D_v3_1_1.fits` (Pipe3D VAC: stellar ages, Dn4000) | data.sdss.org/sas/dr17/manga/spectro/pipe3d/v3_1_1/3.1.1/ | 55.9 MB (HTTP HEAD) | secondary age proxy |

The ELUCID initial conditions are available only "upon reasonable request" from the corresponding author and are not needed for 1.5(b). The analysis code is public at github.com/Hiki1998/TTT-observation (not fetched).

## 4. Provisional items

- The News & Views content and its "unexpected puzzle" were not read. One candidate for the puzzle, *not checked*, is why merger-built ellipticals (and their ionized gas, often externally accreted per ATLAS3D-era results, which are recalled) keep the memory better than spirals at fixed halo mass. Do not cite any reading of the N&V until it is read verbatim.
- The decorrelation budget in ΛCDM hydro simulations (0.7 → 0.3–0.5) is quoted from the paper. Its split into causes (disc–halo torques, mergers, accretion) is recalled.
- Nothing here changes any verdict on the record.
