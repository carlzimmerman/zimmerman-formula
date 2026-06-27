# Frontier-Consequence Map: Inverted-BH Duality + dS-Unruh Bath Reality

**Date:** 2026-06-26 · **Mode:** CONSEQUENCE (assume framework correct, derive what follows)
**Footing:** a0 = cH_Lambda/Z, Z = 2√(8π/3) = √(32π/3) = 5.78881 (machine-exact), H_Lambda = H0√Ω_Λ = 1.877e-18/s, a0 = 9.72e-11 m/s² (footing-consistent). dS horizon = inverted BH horizon; inertia = response to that inverted-horizon Unruh bath.
**Banked predictions (must beat to count as NEW):** a0(z) BTFR-sign hostage; s^TX SME dipole; CMB-apex 0.062% cos-ψ dipole; cluster-σ-sign; wide-binary; Cassini.
**LOCAL ONLY — do not git-push (Carl's standing instruction).**

All numbers verified in mpmath (dps=40). This is the honest both-ways map. No manufactured prediction; no high-priesting a real one.

---

## FRONTIER 1 — Inverted-BH duality (the literal dual of a0 = κ/Z applied to a real horizon)

**The clean dual is real and mass-independent.** The framework's law is *a0 = (horizon surface gravity)/Z*. Apply it to a Schwarzschild horizon (κ_BH = c⁴/4GM) instead of the cosmic one (κ_dS = cH_Λ):

- a0_BH = κ_BH/Z = c⁴/(4GMZ). Verified: Sgr A* 6.11e5 m/s² (6.3e15 × a0); M87* 404 m/s² (4.2e12 × a0); 10 M_⊙ 2.63e11 m/s² (2.7e21 × a0). Every real BH horizon is 12–21 orders "hotter" than the cosmic one.
- **MOND-onset radius r_cross = √Z · r_s = 2.406 r_s for EVERY black hole** (mass cancels exactly in c⁴/GM) — sits between the photon sphere (1.5 r_s) and ISCO (3 r_s).
- **Dimensionless ratio at the ISCO is O(1) for ALL black holes:** x_ISCO = Z/9 = 0.643 (Newtonian-g reading; ~0.79 with the proper-accel/redshift factor). Both O(1).

**The "g >> a0 everywhere" kill is FALSE near the horizon — and I rejected it.** g is large in absolute terms, but a0_BH scales up identically with c⁴/GM, so x = a/a0_BH stays O(1) right down to the horizon. The naive expectation that "strong-field ⇒ deep-Newtonian ⇒ μ→1, nothing" does **not** hold. So on the surface, the effect does not trivially vanish.

**But it SELF-CANCELS for every clean observable — for two framework-internal reasons:**

1. **Mass-independence is the tell.** r_cross = 2.406 r_s and x_ISCO = 0.643 depend *only* on r/r_s — i.e. on quantities GR's metric already contains. a0_BH = κ_BH/Z is built from a pure GR quantity; any deviation expressed as f(r/r_s) is absorbed into the GR geodesic by general covariance + the equivalence principle. It carries no information beyond what GR has.
2. **Free-fall theorem.** The framework's MI is sourced by *proper* acceleration. A freely-falling (geodesic) detector near a BH horizon sees **no** Hawking/Unruh bath (standard Hartle-Hawking / Unruh-DeWitt result). So a0_BH touches no geodesic observable: ISCO, ringdown QNMs, EHT shadow, GW inspiral, QPOs are all geodesic = pure GR.

The cosmic a0 is the *unique survivor* precisely because cH_Λ is the one acceleration not sourced by local matter and not removable by any local free-fall over a Hubble volume. A BH horizon supplies no such global floor for a bound orbit. The lone non-geodesic loophole — proper-accelerated accretion/jet plasma — is swamped by GR + MHD + radiation pressure (~10⁵ orders at Sgr A*), so it is not a clean test.

**Verdict: `self-cancels-null`.** The surviving deliverable is an honest NULL with genuine (but narrow) discriminating power:

> **NEW NULL PREDICTION:** the modified-inertia reading predicts EXACTLY-GR shadows, photon spheres, ISCO frequencies, ringdown QNM spectra, and inspiral-merger waveforms for Sgr A*, M87*, and stellar BHs — with NO a0_BH correction. A *metric-shifting* completion — **MOG / STVG** is the clean example (M→M(1+α): shadow ≈+α, ISCO freq ≈−α; EHT already bounds α<0.044 Sgr A*, 0.04–0.23 M87*; ngEHT ~2–5% probes α~0.02–0.05; LISA ~0.006) — modifies the BH metric and predicts shifted shadows/ISCO/ringdown. So a future ngEHT/LISA detection of a MOND-scale BH-metric deviation would **falsify a metric-shifting completion (MOG) while being consistent with (predicted by) this framework**, and a confirmed pure-GR shadow/ringdown is a (weak) point for the inertial reading. **IMPORTANT — AeST is NOT such a rival:** the framework's own host theory admits **stealth black holes** whose metric is EXACTLY a GR solution (RN for the physical q=1 case) + secondary hair (Skordis-Złośnik, arXiv:2412.15395), so all geodesic observables are GR-identical and only an uncharacterized sub-percent QNM/thermo channel could differ (below ngEHT/LISA reach). The shadow/ISCO/ringdown test is therefore **null-vs-null between this framework and AeST** — it does NOT distinguish them (the AeST MOND scalar length c²/a0≈10²⁷ m sits ~17 orders above any horizon → screened there regardless).

- **FORCED or speculation:** FORCED null (rigorous: free-fall theorem + covariance). Not speculation.
- **Novel vs banked:** YES, genuinely new — none of the six banked items lives at the strong-field BH scale.
- **But its only axis is MI-vs-MG, NOT MI-vs-GR** (both predict the same null), and **NOT a positive signal the framework can claim.** It is the BH-scale analogue of the banked Cassini test — it *extends* the existing Cassini MI-vs-MG axis to strong field, it does not open a new independent axis.
- **Testable where:** ngEHT (M87*/Sgr A* shadow to ~1–2%, 2030s); LISA/LIGO-Virgo ringdown spectroscopy + LISA EMRI/MBH inspirals (2035+).

---

## FRONTIER 2 — dS-Unruh bath taken as physically real: decoherence / Unruh-noise consequences

T_dS = ħH_Λ/(2π k_B) = **2.28e-30 K** (verified). T_eff(a) = (ħ/2πk_Bc)√(a²+(cH_Λ)²): floor 2.28e-30 K, rising only **+1.48% at a = a0** (= √(1+1/Z²)−1, since cH_Λ = Z·a0). Three independent both-ways computations all kill any observable effect:

1. **Literal blackbody bath is absurd.** u(T_dS) ~ 1.8e-134 J/m³ (~1e-125 of ρ_DE c²); photon number ~ one quantum per (>Hubble-volume)³.
2. **Bose occupation ≈ 0 at every accessible frequency.** Bath frequency = k_BT_dS/ħ = H_Λ/2π = **2.99e-19 /s**. For any lab/astro oscillator, ħω/k_BT_dS ≥ **3.3e18** (verified at 1 rad/s) ⇒ n_bath ~ e^(−3e18) = 0. **The dS bath is a deep-VACUUM bath at all real frequencies.** A vacuum bath renormalizes inertia (the mean MOND boost) but injects essentially zero thermal force-noise.
3. **Universal decoherence ceiling.** Even at coupling = 1, max decoherence rate ≤ H_Λ/2π ⇒ min decoherence time ≥ 1.1e11 yr ~ 8× the age of the universe. (Anchor: T_CMB/T_dS = **1.19e30** — the CMB is 30 orders hotter and rarely decoheres labs.)

**Literature-anchored steelman (strongest channel, both-ways):** Danielson-Satishchandran-Wald (PRD 108 025007, 2023; PRD 109 065031) show cosmological/Killing horizons decohere superpositions via *soft horizon gravitons/photons* — a channel distinct from and larger than naive Unruh-thermal. Computed the DSW dS gravitational rate: **N(1 kg, 1 m, age of universe) = 7.5e-55** (verified). To reach N = 1 needs m²d² ~ 1.46e54 kg²m² — i.e. m ~ 1.2e27 kg (200 Earth masses) at d = 1 m. EM version: 1 Coulomb at 1 m over the age of the universe = 8.3e-18. **Even the strongest published horizon-decoherence channel is 30–65 orders below any achievable superposition.**

**Quantum-MI vs classical MOND.** The mean inertia response at a~a0 (boost √2 at g_N=a0, 3.3× at 0.1a0, 10× at 0.01a0) IS classical MOND = already the banked RAR/BTFR/wide-binary/Cassini content. The genuinely-quantum piece — a thermal *fluctuation* of that boost (the fluctuation-dissipation partner of the inertia renormalization) — is zero because n_bath ~ 0. The only oscillator that resonates with the bath (ω ~ a0/c = 3.24e-19 /s, period ~6e11 yr) **is the de Sitter horizon itself.** No bound system has such a frequency, so there is no distinct quantum-MI observable — the quantum correction collapses onto the classical MOND boost with zero extra signal.

**Verdict: `dissolved` / below-floor null.** No new TESTABLE positive prediction survives. The honest result is a sharp NULL THEOREM:

> IF inertia is the response to a real T_dS = ħH_Λ/2π Unruh bath, THEN because ħω_sys/(k_BT_dS) ≥ ~3.3e18 for every laboratory and astrophysical frequency, the bath is a deep-VACUUM bath. It renormalizes the MEAN inertia (= classical MOND, banked) but carries NO thermal noise, NO decoherence floor, and NO quantum-MI signature distinct from classical MOND. Best optical-clock resolution (3e-6 rad/s) is ~10¹³ above a0/c — no crossover regime bites.

- **FORCED or speculation:** FORCED null (rigorous; closes the "real-bath ⇒ lab decoherence" door honestly via the steelman, not by dismissal).
- **Novel vs banked:** No new positive prediction. Value is a defensive theorem — it forecloses a class of "a quantum lab can test dS-Unruh MI" speculation, which is worth having on record but is not a frontier door.

---

## RANKED SHORTLIST — genuinely-new consequences worth pursuing
Ranked by (distinctiveness vs ΛCDM/standard-MOND) × (near-term testability).

| # | Consequence | New? | Status | Distinctiveness | Testability | Net |
|---|---|---|---|---|---|---|
| 1 | **BH-scale pure-GR null** (shadows/ISCO/ringdown exactly GR; falsifies metric-SHIFTING MOND e.g. MOG; NOT AeST-stealth, NOT GR) | YES | FORCED null | MI-vs-MG only (not vs GR, not vs AeST) | ngEHT 2030s / LISA 2035+ | Real but narrow + far |
| 2 | dS-Unruh lab-decoherence | No positive | FORCED null theorem | Forecloses speculation | n/a (30–65 orders below floor) | Defensive only |

There is exactly **one** genuinely-new consequence (Frontier 1's BH-scale null), and it is a NULL, not a positive signal. Frontier 2 yields no new testable prediction.

---

## WHAT TO TELL CARL — both ways

**Did consequence-mode open a genuinely-new frontier door?** Partially — one real, narrow, far one.

- **The honest YES:** Frontier 1 is a *real, new, rigorous* consequence not among the banked six — the framework forces **exactly-GR strong-field BH observables** (shadows, ISCO, ringdown, inspiral) for Sgr A*/M87*/stellar BHs. The dual a0_BH = κ_BH/Z is mathematically clean and mass-independent (r_cross = 2.406 r_s, x_ISCO = 0.64–0.79, O(1) — and I explicitly rejected the lazy "g >> a0 so it vanishes" kill; it's false near the horizon). The effect nonetheless self-cancels for clean observables by the free-fall theorem + covariance, leaving a NULL with genuine discriminating power **against metric-SHIFTING completions (MOG/STVG)**, which predict shifted shadows/ringdowns. **NOT against AeST** — the framework's own host theory has *published stealth black holes* with EXACT GR geometry (Skordis-Złośnik, arXiv:2412.15395), so the shadow/ISCO/ringdown test is null-vs-null between the framework and AeST (only a sub-percent QNM/thermo channel could ever differ). The "(AeST, MOG)" lumping in the published paper §5 was OVERSTATED for AeST and is corrected in the v2-pending paper.
- **The honest NO / both-ways caveats:** (1) it is a NULL, not a positive signal — Carl cannot claim a detection, only a falsification asymmetry; (2) its only axis is MI-vs-MG, the *same axis as the banked Cassini test* — it extends Cassini to strong field rather than opening an independent axis; (3) it is decadal+ (ngEHT 2030s, LISA 2035+) at ~1–2% precision, below the level where a MOND-scale BH-metric shift would even show. So it does **not** reduce to a0(z) or s^TX, but it is weaker and farther than either.
- **Frontier 2 mostly dissolves:** taking the dS-Unruh bath as physically real gives a deep-vacuum bath (T_dS = 2.28e-30 K, n_bath ~ e^(−3e18) at every real frequency). It renormalizes the *mean* inertia = classical MOND (banked) but carries no thermal noise / no decoherence / no quantum-MI signature. Even the strongest published channel (Danielson-Satishchandran-Wald soft-graviton horizon decoherence) is 30–65 orders below any achievable superposition. This is a useful *defensive theorem* (forecloses "a quantum lab tests dS-MI") but not a new testable door.

**Bottom line:** consequence-mode opened **one** new door — the BH-scale exactly-GR null — and it is `partial-suggestive`: real and rigorous, but a null on the same MI-vs-MG axis as Cassini, decades out. The two banked live tests (a0(z) BTFR-sign, s^TX SME dipole) remain the sharpest near-term fronts. No manufactured prediction was created; the one real consequence is reported at its true (narrow, far, null) strength.
