# The Galaxy-Cluster Residual in de Sitter–MOND: the Dark Sector Has the Mass, but a Density-Ordering Veto Forbids It from Being Galaxy-Safe and Cluster-Clumpy at Once

**C. P. Zimmerman**
*Briar Creek Tech · Charlotte, NC · carl@briarcreektech.com*

*Version 2026-06-20 · Zenodo [10.5281/zenodo.20779562](https://doi.org/10.5281/zenodo.20779562).*

---

## Abstract

Modified Newtonian Dynamics (MOND) and its relativistic completions reproduce galaxy rotation curves with a single acceleration scale a₀ ≈ 1.2×10⁻¹⁰ m s⁻², yet they famously leave a residual missing-mass discrepancy of a factor ≈ 2 in the cores of galaxy clusters — a problem first quantified by Sanders (1999, 2003) and unchanged in modern data. We ask whether this residual can be explained *within* the de Sitter–MOND framework (a₀ = c²√(Λ/32π) = cH_Λ/Z, Z = √(32π/3) = 5.7888, giving a₀ = 9.36×10⁻¹¹ m s⁻²), whose dark sector is the Aether-Scalar-Tensor (AeST) ghost-condensate of Skordis & Złośnik (2021) — a cold, w = 0, ρ ∝ a⁻³ *mode of the gravity field*, not a new particle. We report a clean, two-sided result. **(i) The abundance is not the problem.** The AeST shift-symmetric Q-mode carries Ω_dm worth of cold density; deposited at the cosmic dark-to-baryon ratio it supplies (Ω_dm/Ω_b)·M_b ≈ 7.0×10¹⁴ M⊙ inside R₅₀₀ against the ≈ 4.79×10¹⁴ M⊙ a factor-2 cluster requires — **a ratio of 1.46, with zero mass tuning.** The framework's dark sector *has* the cluster mass. **(ii) But it cannot deploy that mass galaxy-safely.** The Q-mode is sound-speed-zero (c_s² → 0) sub-horizon — the very property that lets AeST match the *Planck* third acoustic peak — so its Jeans length vanishes and its growth is gated only by the field's mass term, ρ > μ²/4πG. Galaxy disks (≈10²² kg m⁻³) and cluster cores (≈10²³·⁵ kg m⁻³) both exceed this threshold by ~10¹³, **and the galaxy disk is ≈3.7× denser than the cluster core**: the density ordering runs *backwards*, so any field configuration that clumps in cluster cores clumps *more* in galaxies. Injecting the required cold density into a fiducial disk shifts the radial-acceleration relation (RAR) by +0.12 to +0.23 dex against an observed scatter floor of 0.11–0.14 dex — re-introducing exactly the cuspy-halo scatter MOND was constructed to remove. We prove this is not evaded by an acceleration-dependent gate: a₀ is absent from the AeST linear perturbation equations (Bridge-1), so the dust grows by pure gravitational instability, blind to a₀. **The conclusion is a no-go, stated symmetrically:** the cluster residual *is* the framework's own dark sector doing a cold-dark-matter job — that is the explanation — but in the two clean field limits the sector either over-fills clusters and breaks galaxies, or stays galaxy-safe and fills only ~17–20% of the cluster core. There is no limit in which it does both. Consequently the "pure MOND, no dark matter" reading is forfeited: the framework contains dark matter, of a non-particle (gravity-mode) kind. A galaxy-safe no-new-particle stack (the shift-symmetric Y–Q response +17–20%, intracluster-medium and intracluster-light baryons within the cosmic baryon ceiling, and budget-capped stellar remnants) closes ≈36% of the robust ~10¹⁴ M⊙ core gap, leaving ~64% open. We test the natural escape — a scale-selecting Jeans length from the ghost condensate's k⁴ dispersion, which would order clustering by *scale* (clusters yes, galaxies no) and sidestep the density argument — and find it closed at the linear level: the quadratic higher-derivative coefficient is **zero in the published AeST action** (Blanchet & Skordis 2024, §6.2, verbatim), so there is no k⁴ Jeans scale, and the one finite scale (the condensate mass μ⁻¹ ≳ 22 Mpc) sits *above* all clusters with the wrong topology. The single remaining theory lever is therefore the AeST *nonlinear* term's dependence on the gravitational-potential depth |Φ| — the enhancement that Durakovic & Skordis (2024) found "illustrates the potential of AeST to address the shortcomings of MOND in galaxy clusters" and explicitly deferred beyond the isothermal case. We perform that deferred non-isothermal calculation (the +μ²Φ Helmholtz mass term, solved numerically on real cluster baryon profiles) and find the lever genuinely real and large — ~10⁵× the naive potential coupling, reaching 28–100% of the core residual — and galaxy- and Cassini-safe at its natural footing (RAR shift 7×10⁻⁴ dex, Saturn anomaly 10⁻⁹ fractional), but **descriptive rather than predictive**: the closure is set by the Helmholtz oscillation *phase*, not the cosmological boundary value, so it requires a per-cluster tune (the natural untuned boundary gives a *deficit*), and the value imposed universally breaks the galaxy RAR by 0.275 dex. The framework's cluster sector therefore remains irreducibly phenomenological; the single un-closed branch is whether a full 3D cosmological AeST N-body calculation dynamically pins the oscillation phase that the static boundary-value problem leaves free. We also report two negative results that close common escape routes: the framework's history-dependent modified inertia is *wrong-signed* for a cluster surplus (d ln M_eff / d ln a₀ = −1 exactly), and the hot-dark-matter (neutrino) option is excluded by KATRIN (2024) and DESI DR2 (2025). All quantitative claims are reproduced by committed Python scripts (all exit 0). Quarantine note: a₀, Z, κ, and the dark-sector amplitude I₀ are never asserted to be derived.

---

## 1. The cluster residual, and the question

MOND (Milgrom 1983a,b,c) explains galaxy rotation curves and the baryonic Tully–Fisher relation with one acceleration scale; the radial-acceleration relation (RAR) of McGaugh, Lelli & Schombert (2016) and Lelli et al. (2017) is among the tightest scaling relations in extragalactic astronomy, with an intrinsic scatter of only 0.03–0.06 dex (Li et al. 2018; Stiskalek & Desmond 2023). Yet in the cores of galaxy clusters MOND under-predicts the gravitating mass by a factor ≈ 2 — the residual missing-mass problem of Sanders (1999, 2003), confirmed in modern lensing + X-ray data (Famaey & McGaugh 2012, §9; Famaey, Pizzuti & Saltas 2024; Famaey 2026 on the Bullet Cluster) and persisting at the cluster core (Kelleher & Lelli 2024 find a missing/visible ratio of 1–5 at 200–300 kpc, declining outward — a *core* phenomenon).

This residual is **shared across the entire relativistic-MOND family**: the framework studied here is a *modified-inertia* reading whose quasi-static cluster mass equals the modified-gravity prediction of AeST to machine precision, so the residual is identical and is not specific to any one theory. The question of this paper is sharp and constructive: *the residual is real, so something supplies the extra cluster mass — what, within the framework, is it, and at what cost?*

The de Sitter–MOND framework (Zimmerman 2026a, Zenodo 10.5281/zenodo.20721540) sets the MOND scale by the cosmological constant through a de Sitter–Unruh effective temperature (Deser & Levin 1997),

> a₀ = c²√(Λ/32π) = (c/2)√(Gρ_DE) = cH_Λ/Z,  Z = √(32π/3) = 5.7888,  a₀ = 9.36×10⁻¹¹ m s⁻²,

and adopts as its dark sector the AeST ghost-condensate of Skordis & Złośnik (2021): the shift-symmetric scalar's temporal "Q-mode," a w = 0, ρ ∝ a⁻³ cold component that is a *mode of the gravity field*, not a new particle. This is the authors' own identification — Verwayen, Skordis & Złośnik (2024) write the kinetic function K(Q) = μ²(Q−1)² (a ghost condensate in the sense of Arkani-Hamed, Cheng, Luty & Mukohyama 2004), and Blanchet & Skordis (2024) adopt the identical structure. The amplitude I₀ ~ Ω_dm is a free input. The crucial property — the one that lets AeST fit the full *Planck* CMB power spectrum including the third acoustic peak — is that the Q-mode is cold, c_s² → 0 sub-horizon, clustering like cold dark matter on linear scales.

We test whether that *same* cold sector supplies the cluster-core residual.

## 2. The abundance is not the problem (the 1.46× result)

For a rich cluster (M₅₀₀ = 10¹⁵ M⊙, R₅₀₀ ≈ 1.56 Mpc, baryon mass M_b ≈ 1.30×10¹⁴ M⊙ at the eROSITA-eRASS1 composition; Bulbul et al. 2024), a factor-η = 2 discrepancy inside R₅₀₀ requires extra gravitating mass M_extra ≈ 4.79×10¹⁴ M⊙. The AeST Q-mode, deposited at the cosmic cold-to-baryon ratio Ω_dm/Ω_b ≈ 5.4, supplies

> (Ω_dm/Ω_b)·M_b ≈ 7.0×10¹⁴ M⊙  ⟹  ratio = 1.46,

with **zero mass tuning** — the amplitude is fixed by the cosmic ratio, not fitted to the cluster. In core terms (inside 420 kpc) a cold-dark-matter-like Q-dust deposits ≈ 1.0×10¹⁴ M⊙, matching the core gap. *The framework's dark sector has the cluster mass.* This is precisely how AeST is designed to work: MOND on galaxy scales, plus a cold gravity-mode sector that clusters like CDM on larger scales. The reproduction is in `reviews/cluster_explain/route1_qmode_clustering_profile.py`.

## 3. The galaxy veto, and why it is a density-ordering no-go

The hoped-for resolution — a field that clumps in cluster cores but stays smooth in galaxies — has no realization, for a reason that is convention-independent.

**The growth threshold.** A c_s² → 0 field has vanishing Jeans length, so its growth is gated only by its mass term: collapse proceeds wherever the local density exceeds ρ_thr = μ²/4πG. With the AeST screening scale μ⁻¹ ~ 1 Mpc, ρ_thr ≈ 1.5×10⁻¹⁰ ρ_crit. **Both** a galaxy disk (≈ 10¹³·⁹ ρ_crit) and a cluster core (≈ 10¹³·⁴ ρ_crit) exceed this by ~13 orders of magnitude. The mass term screens the *static potential* on scales > μ⁻¹ but cannot prevent sub-Mpc collapse in either system.

**The ordering runs backwards.** The galaxy disk is **≈ 3.7× denser** than the cluster core (ρ_disk ≈ 1.2×10⁻²² vs ρ_core ≈ 3.3×10⁻²³ kg m⁻³). Gravitational clumping is monotonic in density, so any configuration cold enough to clump in cluster cores clumps *more* in galaxy disks. There is no single sound speed or mass scale that makes the field cluster in clusters but not in the (denser) galaxies; the would-be window is empty and inverted.

**The kill.** Injecting the cold density required for clusters into a fiducial galaxy disk shifts the RAR by

> +0.115 dex at 10% of the halo, +0.124 dex at 60%, +0.233 dex at 100%,

against the observed RAR scatter floor of 0.11–0.14 dex (McGaugh et al. 2016) — re-introducing exactly the galaxy-to-galaxy cuspy-halo scatter that MOND was constructed to remove. (`reviews/cluster_explain/qmode_clustering_and_timedomain_MI.py`.)

**No acceleration gate rescues it.** One might hope a₀ itself gates the growth so that clumping is acceleration-selective. It does not: in the AeST framework a₀ is provably absent from the linear perturbation equations (the "Bridge-1" result; Skordis & Złośnik 2021; reproduced in `reviews/`), so the dust grows by pure gravitational instability, knowing nothing about a₀. The growth is CDM-identical at linear order.

**The no-go.** In the two clean field limits the same sector either (a) behaves as a structureless cold fluid — closing clusters but breaking galaxies by +0.12 to +0.23 dex — or (b) is treated as the faithful shift-symmetric AeST response — galaxy-safe by shift symmetry, but filling only ~17–20% of the cluster core. *There is no limit in which it both closes clusters and preserves galaxies.* The residual is the field doing a cold-dark-matter job, but it is cold dark matter **relocated onto the gravity mode, not eliminated.**

**The scale-selection loophole, tested and closed.** The most natural escape from a density-ordering argument is a *scale* gate: a finite Jeans length λ_J that orders clustering by wavelength rather than density. A ghost condensate generically supplies one — its dispersion carries a higher-derivative ω² ~ k⁴/M² term (Arkani-Hamed et al. 2004) — and *if* λ_J sat between galaxy (~kpc) and cluster (~Mpc) scales, the field would clump at cluster scales (small k, unstable) while being smoothed at galaxy scales (large k, stabilized), galaxy-safe and cluster-clumpy at once, sidestepping the density argument entirely. The topology is correct, and we credit it at full weight. **But it has no realization in the published host.** (i) The quadratic k⁴ coefficient is *zero* in AeST: Blanchet & Skordis (2024, §6.2) state verbatim that "there are no higher derivative interaction terms in the action, which are also quadratic in the fields (and so contribute to the usual dispersion relation)"; the k⁴ tail belongs only to the *isolated* ghost condensate with interactions ignored, and the real AeST scalar dispersion is ω² = c_s²k² + M² (Skordis & Złośnik 2022, Eq. 29) — a plain k²+gap with no k⁴ Jeans scale. (ii) The one genuine finite scale, the condensate mass μ, has the *wrong* topology: AeST grows for k < μ and is stabilized for k > μ (Blanchet & Skordis 2024), so the field clumps on scales *larger* than μ⁻¹, the opposite of what is needed; and with μ⁻¹ ≳ 22 Mpc (fixed by galaxy MOND) every bound system — galaxy disks, cluster cores, and R₅₀₀ alike — lies on the stabilized k > μ side, with only superclusters and the CMB growing. (iii) Even granting a non-zero k⁴, the ghost-condensate/wave-dark-matter Jeans length scales as ρ⁻¹/⁴, so it is *shorter* in the denser galaxy (λ_J,gal / λ_J,clus ≈ 0.54) — it tracks density, and the galaxy clumps *more*, re-importing the no-go; and no single mass M can simultaneously match the CMB third peak (M ~ eV) and smooth galaxies (M ~ 10⁻³⁰ eV), ~28–30 orders apart. The scale-selection loophole is therefore closed at the linear level. (Computations: `reviews/evade_nogo/evade_k4_jeans_scale.py`, `evade_bestshot_invert.py`.)

## 4. Two closed escape routes

**History-dependent modified inertia is wrong-signed.** The framework's inertia is non-local in time (Milgrom 1994, 2022); the quasi-static limit gives modified-inertia ≡ modified-gravity exactly, and the full multi-frequency response gives a boost factor ≤ 1.000 (the root-mean-square acceleration exceeds the mean, *reducing* the inferred mass). The formation-epoch variant fares no better: d ln M_eff / d ln a₀ = −1 exactly, so a *higher* a₀ at cluster formation imprints *less* phantom mass — the wrong sign for a surplus. (`reviews/cluster_explain/qmode_clustering_and_timedomain_MI.py`, sympy-verified.)

**Hot dark matter (neutrinos) is excluded.** The classic MOND cluster fix — ~1.5–2 eV neutrinos that cluster on cluster but not galaxy scales (Sanders 2003; Angus, Famaey & Zhao 2006) — is now closed: KATRIN (2024) limits m_ν < 0.45 eV, and DESI DR2 (2025) bounds Σm_ν < 0.052–0.064 eV (95% CL), below the normal-ordering floor. No neutrino mass remains viable for the residual.

## 5. What a galaxy-safe, no-new-particle stack does close

The genuinely galaxy-safe ingredients sum to a partial closure of the robust ~10¹⁴ M⊙ core gap:

- the AeST shift-symmetric Y–Q response (an in-place, galaxy-safe boost) supplies +17–20% (~7×10¹² M⊙);
- intracluster-light and bottom-heavy-initial-mass-function stellar mass in cluster ellipticals — real baryons, galaxy-safe by selection (ellipticals, not the rotation-supported disks that define the RAR; Conroy & van Dokkum 2012) — and intracluster-medium baryons within the cosmic baryon ceiling f_b = Ω_b/Ω_m = 0.156 add ~2.7×10¹³ M⊙ in the core;

for a total closure of **≈ 36%**, leaving **~6.4×10¹³ M⊙ (~64%)** of the core gap open. We emphasize, against an earlier optimistic reading of our own, that this core gap is **robust**: the post-XRISM equilibrium bracket η(R₅₀₀) ∈ [1.0, 2.33] is an *outskirts* statement, whereas the resolved cluster *core* weak-lensing-to-X-ray mass ratio is already ≈ 1.03, so the core residual is not deflated by the weak-lensing-versus-hydrostatic mass-proxy question.

## 6. The AeST nonlinear potential-depth enhancement, computed: real and galaxy-safe, but descriptive, not predictive

The scale-selection loophole is closed at the *linear* level (§3). But the AeST MOND dynamics live in the theory's *nonlinear* term, and there a single galaxy-safe lever survives — the one candidate that, across an exhaustive door-by-door search, passes both the galaxy radial-acceleration-relation veto and the Solar-System (Cassini) bound while boosting clusters: an enhancement keyed not on density but on the **gravitational-potential depth**. The AeST authors' own cluster study, Durakovic & Skordis (2024, "Towards galaxy cluster models in AeST"), finds the cluster RAR enhancement set by "the AeST weak-field mass parameter, the mass of the system, **and the boundary value of the gravitational potential**," calls it "the potential of AeST to address the shortcomings of MOND in galaxy clusters," and explicitly defers the quantitative test ("will require going beyond the isothermal case"). We performed that deferred non-isothermal calculation.

The mechanism is the **+μ²Φ mass term** in the AeST weak-field equation (Durakovic & Skordis 2024, Eq. 2.40; Blanchet & Skordis 2024, Eq. 3.21): pure AQUAL is shift-invariant, but the mass term breaks that, so the absolute asymptotic level χ∞ becomes physical and feeds back as a phantom source ρ_eff = −μ²Φ/4πG. The operator is Helmholtz, so the homogeneous solutions are oscillatory. Solving it numerically (spherical, non-isothermal, real A2029-class baryons; solver validated against analytic MOND at μ→0 to one part in 10⁶) yields three results. **(i) The magnitude is reached:** the core (<420 kpc) phantom mass is +4.2×10¹³ M⊙ on the cosmological-dark-energy χ∞ branch (~28% of the residual) and up to +1.5×10¹⁴ M⊙ on the boost branches (~100%), i.e. **~10⁵× the naive O(1) potential coupling** (which closes 0.0002%) — a real Helmholtz-mass-term mechanism gap, not a denominator trick. **(ii) It is galaxy- and Cassini-safe at the natural footing:** the galaxy RAR shift is 6.85×10⁻⁴ dex (73× under the 0.05 dex veto), and the Saturn anomaly is 1.0×10⁻⁹ fractional (2.3×10⁴× under the PPN bound), the split being geometric — the correction scales as (μr)², and the CMB-pinned 1/μ ≈ 1 Mpc sits between galaxy (kpc) and cluster (Mpc) scales. **(iii) But the closure is multivalued and descriptive, not predictive — and this is the verdict:** χ∞ does not determine the boost; the Helmholtz oscillation *phase* does. The *same* cosmological χ∞ is hit at phases spanning η(R₅₀₀) from −3.12 to +3.97 (both large boosts and deficits), η swings from +2.08 to +7.37 with the matching-radius convention, and the *natural untuned* boundary gives η = −1.54 — a **deficit**, not a boost. Reaching closure requires a per-cluster tune of χ∞; no cosmologically-pinned value delivers it, and the value a cluster needs, imposed *universally*, leaks into the galaxy RAR as a 0.275 dex shift (5.5× over the veto). Moreover the framework's own dS-Unruh modified inertia is horizon-set and blind to local Φ, so no framework field even carries the required χ∞ coupling — the lever is AeST's, not the framework's. **The cluster boost is therefore a per-object fit, not a parameter-free prediction**: the framework's cluster lensing and dynamics remain irreducibly phenomenological (an AeST-class free function). The single un-closed branch the spherical-static solve cannot settle is whether a full 3D cosmological AeST N-body calculation — the cluster embedded in its real collapsing environment, evolved through turnaround — *dynamically* pins the oscillation phase that the static boundary-value problem leaves free; if it does, and to a boost phase universally, the door reopens, and that is the decisive open computation no AeST author has performed.

## 7. Two-sided summary

The result is symmetric and we state both halves at full weight. **In the framework's favor:** the dark sector it already possesses — required independently by the CMB — has, with zero tuning, 1.46× the mass a factor-2 cluster needs; the residual is therefore *explained*, not mysterious, and explained with no new fundamental particle. **Against the strong reading:** that same sector cannot deploy its mass while preserving the galaxy RAR, by a clean density-ordering argument (galaxies are denser than cluster cores; the CMB-required c_s² → 0 makes the field clump wherever density is highest). The "pure MOND, no dark matter at all" interpretation is therefore forfeited at clusters: the honest framework is **MOND in galaxies, plus a non-particle (gravity-mode) cold dark sector that clusters in clusters and on the CMB.** That is a coherent, internally consistent, and arguably expected position for an AeST-embedded theory — it is simply not "no dark matter." The remaining ~64% core gap is closeable galaxy-safely only if the AeST μ-scale threads the intermediate regime of §6.

## 8. Reproducibility

Every quantitative claim is reproduced by committed Python scripts (all exit 0), at <https://github.com/carlzimmerman/zimmerman-formula> under `opus_48_extended_research/reviews/cluster_explain/`:

- `route1_qmode_clustering_profile.py`, `route1_qmode_profile_jeans_filter.py` — the 1.46× abundance and the Jeans/growth-threshold filter (§2–3);
- `qmode_clustering_and_timedomain_MI.py` — the galaxy-RAR injection veto and the wrong-signed time-domain / formation-epoch inertia (§3–4);
- `route3_literature_sweep.py` — the 2024–2026 literature survey and the neutrino exclusion (§4);
- `route4_bruteforce_stack.py` — the galaxy-safe stack and the ~36% partial closure (§5);
- `evade_nogo/evade_k4_jeans_scale.py`, `evade_nogo/evade_bestshot_invert.py` — the k⁴ scale-selection loophole test, the B = 0 check against the AeST action, and the ρ⁻¹/⁴ Jeans-scale inversion (§3);
- `aest_phi_cluster/aest_phi_cluster_solve.py`, `aest_phi_galaxy_cassini_veto.py`, `aest_phi_cluster_ADVERSARIAL.py` — the deferred non-isothermal AeST +μ²Φ weak-field solve, the galaxy/Cassini veto, and the χ∞-multivaluedness scan (§6; solver validated against analytic MOND at μ→0).

Supporting cluster analyses (the weak-lensing-vs-hydrostatic mass proxy, the baryon census, the modified-inertia mass re-derivation) are in `reviews/` (`WL_VS_HYDRO_ETA_2026-06-20.md`, `CLUSTER_MEASUREMENT_SYSTEMATICS_2026-06-20.md`, `UNIFIED_LAW_MI_MASSES_2026-06-20.md`).

## 9. References

- Angus, G. W., Famaey, B. & Zhao, H. 2006, *MNRAS* **371**, 138 (astro-ph/0606216).
- Arkani-Hamed, N., Cheng, H.-C., Luty, M. A. & Mukohyama, S. 2004, *JHEP* **05**, 074 (hep-th/0312099).
- Blanchet, L. & Skordis, C. 2024, *JCAP* **11**, 040 (arXiv:2404.06584).
- Bulbul, E. et al. (eROSITA/eRASS1) 2024, *A&A* **685**, A106.
- Conroy, C. & van Dokkum, P. 2012, *ApJ* **760**, 71.
- Deser, S. & Levin, O. 1997, *Class. Quantum Grav.* **14**, L163 (gr-qc/9706018).
- DESI Collaboration 2025, DESI DR2 BAO cosmological constraints (arXiv:2503.14738).
- Durakovic, A. & Skordis, C. 2024, "Towards galaxy cluster models in the Aether-Scalar-Tensor theory" (arXiv:2312.00889, *JCAP*).
- Famaey, B. & McGaugh, S. S. 2012, *Living Rev. Relativity* **15**, 10 (arXiv:1112.3960).
- Famaey, B., Pizzuti, L. & Saltas, I. D. 2024, *Phys. Rev. D* **111**, 123042 (arXiv:2410.02612).
- Famaey, B. 2026, "On the residual missing mass of the Bullet Cluster" (arXiv:2605.10022).
- KATRIN Collaboration 2024, neutrino-mass bound m_ν < 0.45 eV (arXiv:2406.13516).
- Kelleher, R. & Lelli, F. 2024, *A&A* (arXiv:2405.08557).
- Lelli, F., McGaugh, S. S., Schombert, J. M. & Pawlowski, M. S. 2017, *ApJ* **836**, 152.
- Li, P., Lelli, F., McGaugh, S. & Schombert, J. 2018, *A&A* **615**, A3.
- McGaugh, S. S., Lelli, F. & Schombert, J. M. 2016, *Phys. Rev. Lett.* **117**, 201101.
- Milgrom, M. 1983a,b,c, *ApJ* **270**, 365/371/384.
- Milgrom, M. 1994, *Ann. Phys.* **229**, 384; 2022, *Phys. Rev. D* **106**, 084006 (arXiv:2208.07073).
- Mistele, T., McGaugh, S. & Hossenfelder, S. 2024, *A&A* **676**, A100.
- Sanders, R. H. 1999, *ApJ* **512**, L23; 2003, *MNRAS* **342**, 901 (astro-ph/0212293).
- Skordis, C. & Złośnik, T. 2021, *Phys. Rev. Lett.* **127**, 161302 (arXiv:2007.00082).
- Skordis, C. & Złośnik, T. 2022, *Phys. Rev. D* **106**, 104041 (arXiv:2109.13287).
- Stiskalek, R. & Desmond, H. 2023, *MNRAS* (arXiv:2305.19978).
- Verwayen, P., Skordis, C. & Boehm, C. 2024, *MNRAS* **531**, 272 (arXiv:2304.05134).
- Verwayen, P., Skordis, C. & Złośnik, T. 2024 (AeST ghost-condensate identification).
- Zimmerman, C. P. 2026a, framework record, Zenodo 10.5281/zenodo.20721540; 2026b, evolving-a₀(z) note, Zenodo 10.5281/zenodo.20737162.

*Quarantine note: a₀, Z, κ = ½, and the dark-sector amplitude I₀ are inputs and free parameters, never asserted to be derived. This is a both-sided consistency analysis of an existing theory's dark sector, not a discovery paper and not a claim of a theory of everything.*
