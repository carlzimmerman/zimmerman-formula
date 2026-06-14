# The cluster measurement playbook — how to test the framework's distinctive predictions, ranked (2026-06-14)

*Deeper 2023-2026 pull by observational modality (X-ray/microcalorimetry, lensing, SZ/baryon-census,
cluster-galaxy kinematics, high-z/a0(z)) + the concrete "how do we measure this" playbook. 11-agent workflow
(5 modality pulls → hostile probes → synthesis), every instrument/date/number web-verified, calcs reproduced on the
real eRASS1 FITS. Framework a0=9.36e-11, both ways. Source memos: `XRAY_MICROCAL_ETA_NONTHERMAL`,
`LENSING_MODALITY_LATEST_AND_MEASUREMENT`, `SZ_BARYON_CENSUS_VIRIAL_MEASUREMENT` (all `_2026-06-14`); the
density-a0 shape resolved in [[CLUSTER_DENSITY_A0_SHAPE_RECONCILED]].*

---

## The latest measured state (2023-2026)

- **η(R500) magnitude:** real eRASS1 (Bulbul+2024, N=9830, z_med=0.30) → **median η = 2.33** on the framework's own
  dS-Unruh interpolation (η-worst footing, +13% surcharge for the lower a0); canonical a0 → 2.07. The shared-MOND
  ~2× liability, reproduced bit-for-bit.
- **The WL-vs-hydrostatic resolution (the headline 2025-26 result):** XRISM/Resolve microcalorimetry now *directly*
  measures non-thermal pressure — A2029 (Xu+2025) NTP ≤2% to R2500; 9 cool cores (2510.06322) kinetic/total ~2.2%
  vs sims 5-6.5%; SPT+XMM (Aroca-Lobato 2025, 2504.00113) f_nt 15±11% at R500, 27±12% at R200. **NTP cannot supply
  the 52% needed to reach η~2** (15% → η~1.20, 35% → η~1.57). Li+2024: WL mass +110% over hydrostatic, and
  hydrostatic≈kinematic — so the WL/hydro gap is NOT non-thermal pressure. **Convergent true η(R500) ≈ 1.0-1.3.**
- **Baryon census to r_vir:** eROSITA outskirts (2509.25317, 680 clusters) gas ~70-80% universal at R200m after
  clumping; massive systems reach the universal fraction within r_vir; kSZ recovers baryons only at 2-3 r_vir. But
  **η at R500 floors at ~1.7-2.0** — the found baryons sit beyond R500 and can't act on g_bar(R500). IGIMF remnants
  (Zhang/Zonoozi/Kroupa 2026) reach ~88% in nearby cores (contested, model-dependent, MOND-shared).
- **η(r) shape:** central core (missing/gas ~10, ~400-450 kpc cutoff) dying to ~1 by 2-3 Mpc (CLASH
  Pizzuti/Famaey/Saltas; X-COP Kelleher-Lelli 2024; Bullet Cha 2025 lens model + Famaey 2026).

## The ranked playbook — tests of the framework's DISTINCTIVE content

| Rank | Test | Modality / instrument | Distinctive? | Timeline | Confirms / kills |
|---|---|---|---|---|---|
| **1** | **Cluster-member vs field dwarf σ, opposite-sign** | kinematics: MUSE/LEWIS now, 4MOST/WEAVE/DESI 2025-28, ELT/HARMONI ~2029 | **YES** (sign: framework σ↑ with ρ, MOND-EFE σ↓) | **~2027-28** | σ rises with ambient ρ → framework; σ falls / no dependence → EFE-MOND |
| 2 | Environment-split lensing-RAR slope d log a0/d log(1+δ) at fixed M*/morph | lensing: Euclid DR1 (Oct 2026)/DR2-3, Rubin Y3-10 | **YES** (cleanest density-axis isolation) | ~2028-30 | members above field at fixed g_bar → a0_local>a0_field; slope~0 → retreat to tuned-Mpc |
| 3 | NTP-corrected radial η(r) shape vs ρ^(1/4) boost | X-ray: XRISM now (R2500), eROSITA eRASS:4 stacks, Athena X-IFU | partly (sign now resolved: see below) | **Athena ~2037** for per-cluster | flattening tracks ρ^(1/4) → framework; degenerate w/ residual baryons |
| 4 | Density-binned baryon-census η stack (node vs field, fixed M_bar) | SZ/kSZ: Simons Obs (2025-34), CMB-S4 ~2032 | YES (rides underived scale) | ~2028-30 (plausible-target) | deep-MOND a0 rises with ρ_local → framework; no dependence / breaks SPARC → kill |
| 5 | η(R500) magnitude, M_WL/M_HSE, outskirt baryon convergence | X-ray/lensing/SZ (now-2028) | **NO — shared-MOND** | now-2028 | kills η~2 HSE-artifact branch; LCDM reads identically |
| 6 | Cluster-epoch η(z) for the declining a0(z) branch | high-z: eROSITA+Euclid+Rubin; NewAthena resolved cores | YES (by sign) | **non-diagnostic <z~1.5; ~2037+** | η rises with z → declining a0(z); existing MUSE-DARK III leans against |

## The sharpest near-term test (RANK 1)

**Stacked, equilibrium-controlled, environment-split internal kinematics:** cluster-member vs matched-field dwarfs
at FIXED internal g_N — does velocity dispersion **rise (framework: a0_local>a0_field as modified inertia tied to
ρ_total) or fall (standard-MOND EFE)** with ambient density? Why it wins:
- The **only** test of genuinely distinctive content on an instrument operating **today** (MUSE/LEWIS; 4MOST/WEAVE/
  DESI add statistics 2025-28) — no 2037-Athena gate.
- **Opposite-sign** against the key rival (framework σ↑, EFE σ↓), so it is non-degenerate against *generic*
  constant-a0 MOND — which the magnitude tests cannot achieve (LCDM and MOND read those identically). The field EFE
  sign is already measured at 8-11σ (Chae 2020/21), so its absence/reversal in clusters is a real anomaly to exploit.
- **Binding systematic (why it needs design, not just data):** the strongest current FOR datum (Coma UDGs on the RAR
  with no EFE suppression) is degenerate with non-equilibrium first-infall MOND (Nagesh/Freundlich/Famaey 2024). So
  it is **not** decisive on a single elevated σ — it needs phase-space/orbit selection or a stacked equilibrium-tagged
  sample (buildable ~2026-28). A correctly-signed signature-to-watch, NOT a banked win.

## The distinctive-vs-shared line (honest)

Every X-ray **magnitude** channel (η~2.33, M_WL/M_HSE, outskirt baryons) is **shared-MOND** — decisive against "the
η~2 is an HSE artifact" and "baryons explain clusters in any MOND," but LCDM reads them identically. The four
**distinctive** channels all reduce to one claim — **a0 scales with local density** — and each is currently
sign-resolved-but-tilted (X-ray shape, see [[CLUSTER_DENSITY_A0_SHAPE_RECONCILED]]: right sign, flattens to ±30%,
doesn't close), degenerate with non-equilibrium MOND / cold DM (kinematics), non-diagnostic at current precision
(a0(z)), or rides an underived smoothing scale the framework's own value (1/μ~1 Mpc breaks SPARC +34%) falsifies.
**The distinctive content is real and falsifiable but NOT delivered.**

## The gating theory deficit (the one calc that unlocks the rest)

RANKS 2/3/4 all ride the same wall: **no DERIVED inner smoothing scale simultaneously keeps SPARC tight (~0.13 dex,
field) AND supplies the cluster-core density-a0 boost.** The framework's own 1/μ~1 Mpc breaks the RAR +34% and
over-closes clusters to η~0.47; the clean tests only work at a tuned ~10 Mpc scale. **Until a smoothing scale is
*derived*, no distinctive cluster test can be a banked win** — this is the single most valuable theory calc to
advance before pursuing the observations.

## Next actions

1. **Build the equilibrium-controlled environment-split kinematics forecast** (RANK 1): predicted σ(ρ_local) at
   fixed internal g_N under framework (σ↑, deep-MOND amplitude on the framework's OWN dS-Unruh prefactor) vs MOND-EFE
   (σ↓), with the Nagesh-2024 first-infall σ-inflation as a nuisance term → the sample size + orbit-selection cut for
   a >3σ sign-split with MUSE+4MOST/WEAVE/DESI by 2027-28.
2. **Watch three measurements:** next XRISM cool-core NTP releases past R2500 (tighten the η~2 kill); Euclid DR1
   stacked cluster-member GGL (first environment-split RAR slope); SPT+XMM/ACT-DR5 follow-ups to Aroca-Lobato 2025.
3. **Resolve the smoothing-scale trap** — the gating theory calc above.

## Citation/precision fixes banked (web-verified)

KiDS morphology split is **6σ (Brouwer 2021)**, not 8.8σ; Bullet lens model is **Cha 2025 (ApJL 987 L15)**, not
"Rihtaršič 2026"; the g†=2e-9 cluster RAR is **Tian 2020 (ApJ 896 70, arXiv:2001.08340, 20 CLASH)**, scatter 0.06
dex; the distinctive η(r) boost is **ρ^(1/4)** (√ρ is the a0 scaling). See [[CLUSTER_DENSITY_A0_SHAPE_RECONCILED]].

## One line

Cluster X-ray magnitude tests are now decisive but **shared-MOND** (XRISM NTP kills the η~2 HSE-artifact branch →
true η(R500)~1.0-1.3); the framework's **distinctive a0_local>a0_field content** survives in four sign-/scale-
challenged channels, of which the **stacked equilibrium-controlled cluster-member-vs-field opposite-sign kinematics
test (σ↑ vs EFE σ↓) is the sharpest near-term probe (MUSE+4MOST/WEAVE ~2027-28)** — but every distinctive test is
gated by the one unbuilt piece: a *derived* (not tuned) density-smoothing scale.

*No manufactured cure (the distinctive content is flagged undelivered and gated), no high-priest dismissal (the
opposite-sign kinematics test, the zero-parameter flattening, and the XRISM η~2 kill are credited at full weight).
Quarantine held: a0/Z never asserted derived; the smoothing scale flagged tuned-not-derived.*
