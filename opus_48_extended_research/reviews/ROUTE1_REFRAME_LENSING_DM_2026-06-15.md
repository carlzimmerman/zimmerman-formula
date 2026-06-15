# Route 1 — Is lensing an INDEPENDENT dark-matter proof? The framework's own relativistic-lensing law (2026-06-15)

Framework a0 = c² √(Λ/32π) = (c/2)√(G ρ_DE) = **9.355e-11** (verified to 7 figs). dS-Unruh interpolation
g_obs = √(g_N² + g_N·a0), ν(y)=√(1+1/y). Covariant completion = AeST (Skordis–Zlosnik 2021). Quarantine: a0/Z
never asserted derived. Both-ways rule applied to every "reduces to cluster problem" AND every "genuinely independent."

---

## HEADLINE (the load-bearing reframe, VERIFIED from the AeST/TeVeS field equations)

**In AeST and TeVeS the two metric potentials are EQUAL (no gravitational slip): Φ = Ψ, and BOTH equal
Φ̂ + φ (Newtonian-baryonic + scalar). Light deflection integrates Φ+Ψ = 2Φ; dynamics feels Φ. Same Φ. So the
lensing mass and the dynamical mass reconstructed with the GR kernel are IDENTICAL — by construction.**

Verified two ways:
- **Literature (direct quotes).** TeVeS (Bekenstein 2004): ds² = −(1+2Φ/c²)dt² + (1−2Φ/c²)dx², single Φ in
  both terms, "light bending measures the same potential as dynamics" (Bekenstein/Sanders; reviewed in the
  TeVeS-lensing papers astro-ph/0106100, 1205.4880). AeST (arXiv:2301.03499, Mistele–McGaugh–Verlinde weak-lensing
  confrontation): "In the weak-field limit, this metric has the same form as in GR, just with the Newtonian
  potential replaced by Φ = Φ̂ + φ" — **no slip; one potential governs dynamics AND lensing.** This is the
  CONSTRUCTED fix for original non-relativistic MOND, which under-lensed because the scalar did not source Ψ.
- **Python (`/tmp/lensing_reframe.py`).** For the framework's own dS-Unruh g_obs at a0=9.355e-11, the ratio
  M_lens(<r)/M_dyn(<r) = 1.0000 for every g_bar bin (1e-9 … 1e-13) and every ν() — because no-slip makes both
  the convergence integral and the kinematic mass reconstruct the SAME g_obs(r).

**CONSEQUENCE (the reframe): "lensing proves dark matter" largely REDUCES to "clusters need a residual" — the
known shared-MOND cluster problem — NOT a separate, independent proof.** Confirmed by the dedicated MOND-lensing
paper (arXiv:2410.02612, "the view from gravitational lensing"): *"observations of the galactic velocity field
or the X-ray profile … will yield a dynamical mass EQUIVALENT to the lensing mass BY CONSTRUCTION, in MONDian
gravity."* The lensing residual IS the dynamical residual.

---

## THE SIX "lensing = DM" ARGUMENTS — both ways (reduces vs genuinely independent)

| # | Argument | How it's presented as DM proof | Through the framework's AeST lensing law | Verdict |
|---|---|---|---|---|
| (a) | **Bullet Cluster offset** | Lensing peak offset from X-ray gas, tracks galaxies → collisionless DM | No-slip → lensing tracks the TOTAL (baryon+residual) potential; residual is galaxy-centred & collisionless | **REDUCES to cluster residual** (conceded loss) |
| (b) | **Cluster SL+WL mass ~2× baryons** | Lensing mass ≫ baryonic → DM halo | M_lens = M_dyn by construction; the η residual is the SAME object kinematics see | **REDUCES to cluster residual** (the known η problem) |
| (c) | **Galaxy-galaxy lensing RAR + morphology split** | Lensing g_obs follows the RAR; early-types lens +0.26 dex high | Bulk RAR PASSES (no-slip enhancement at a0=9.355e-11, soft); split is a0-INDEPENDENT type-dependence | **bulk REDUCES/PASSES; split is the #1 INDEPENDENT loss** |
| (d) | **Cosmic shear + CMB lensing match ΛCDM P(k)** | Matter power spectrum / 3rd peak needs CDM clustering | NOT a lensing-vs-dynamics issue — it is whether the framework supplies CDM-like clustering at recombination | **GENUINELY INDEPENDENT — framework LOSES (3rd peak)** |
| (e) | **Strong-lens Einstein radii + time delays** | Deflection/H0 from total mass | No-slip → Φ+Ψ deflection enhanced by same MOND factor; Einstein radii fit on baryons+phantom | **REDUCES to dynamics** (TeVeS fits galaxy SL, 1205.4880) |
| (f) | **Flux-ratio anomalies / substructure in lensed quasars** | Perturbations need ~10⁷–10⁹ M⊙ subhalos | About the ABUNDANCE OF SMALL CLUMPS, not the smooth lens potential — orthogonal to no-slip | **GENUINELY INDEPENDENT — open, not yet a framework kill** |

### Which REDUCE to the cluster problem (NOT independent): (a), (b), (e), and the bulk of (c)
The no-slip identity Φ=Ψ collapses these into "is there a residual in the smooth total mass?" — which is the
SAME residual the dynamics/X-ray already require. The Bullet (Famaey 2026, arXiv:2605.10022): η≈8 within 300 kpc,
residual 3.4e14 M⊙ ~ the cluster's own baryonic mass, modeled as galaxy-centred collisionless Plummer spheres,
NOT neutrinos — i.e. the SAME central collisionless residual the cluster dynamics need. The cluster SL+WL ~2×
(b) and Tian-2024's tight cluster RAR (g‡=2e-9=21×a0_F) are the dynamical residual seen through lensing. **None
of these is an independent DM proof beyond the banked cluster η.**

### Which are GENUINELY INDEPENDENT (do NOT reduce):
- **(d) cosmic shear / CMB lensing / the matter power spectrum.** This is NOT a "lensing mass vs dynamical mass"
  statement — no-slip is irrelevant. It asks whether the theory grows CDM-like clustering (the odd/even peak ratio,
  σ8, P(k) shape). The framework already LOSES here on its own footing: banked `cmb_third_peak_dm_mimic.py` —
  baryon-only/modified-inertia gives P3/P2 = 0.42–0.54 vs Planck ~0.92, "cannot reach Planck by any tuning,"
  a0-IRRELEVANT linear theory (confirmed IF-robust in FRONT4 audit). AeST itself needs extra non-baryonic
  clustering (a massive field / dark fluid) to fit the CMB+P(k) — Skordis–Zlosnik's own construction adds it.
  **This is a real, independent loss, NOT cured by the no-slip reframe. Concede at full weight.**
- **(f) flux-ratio anomalies / lensed-quasar substructure.** Probes the ABUNDANCE of 10⁷–10⁹ M⊙ subhalos, a
  small-scale-power question (CDM vs SIDM vs FDM vs warm). Orthogonal to no-slip. The framework has no native
  cold-substructure population, so this is a potential FUTURE exposure — but baryonic structures (edge-on discs,
  1601.01671/1707.07680) also produce anomalies, so it is NOT currently a clean DM proof either. **Open;
  genuinely independent; not yet a kill in either direction.**

---

## FOOTING (rigorous, both ways)

**The cited lensing-DM measurements mostly use GR+DM (no a0 at all).** Cluster SL+WL masses, the Bullet, cosmic
shear, CMB lensing, Einstein radii — all reconstructed with the GR kernel and interpreted in ΛCDM. a0 enters ONLY
when one re-reads them through MOND. Footing audit of the framework's OWN scripts (banked
`LENSING_FOOTING_AUDIT_2026-06-14`, `lensing_a0_footing_HOSTILE_RECHECK`):
- **One cosmetic FALSE-WIN:** `door1_gravitational_lensing.py` displays the GGL-RAR boost table at the LOCAL
  1.2e-10 (and simple-mu), mislabeled "framework," landing the curve circularly on Brouwer's own adopted a0.
  Re-footed at 9.355e-11 with the framework's dS-Unruh ν, deep-MOND g_obs is **−0.054 dex LOWER** — still INSIDE
  Brouwer's 0.1–0.2 dex scatter, a SOFTER pass. Correcting it makes the number worse-looking, not better. Retract
  the polished wording; the pass survives.
- **ZERO false-deficits.** No script makes the framework "lens too weakly" via a wrong a0. The f4_lensing_wall
  40.5σ/12.5σ kills are at the CORRECT 9.36e-11 and target the pure-modified-inertia (baryon-only-metric)
  variant, which AeST's phantom-halo lensing does not use — framework-internal, not a footing artifact.
- The morphology split is a0-INDEPENDENT (g_obs = 4G·ESD at fixed g_bar; no a0/ν in the χ²) — no footing handle.
- The AeST weak-lensing confrontation (2301.03499) used the LITERATURE MOND a0≈1.2e-10, NOT 9.36e-11; its tension
  is the cluster-vs-galaxy m²/f_G tension (galaxies want m²/f_G < 0.001 Mpc⁻², clusters want ≳1) — i.e. the SAME
  cluster residual, NOT an a0-footing artifact against the framework.

---

## RESOLUTION STATUS — what's LIVE, what's CLOSED

**LIVE avenues (genuine, within the framework):**
1. **The reframe itself.** AeST no-slip is REAL and literature-confirmed: it demotes (a),(b),(e),bulk-(c) from
   "independent DM proofs" to restatements of the cluster η. This is the framework's strongest honest lensing
   move — it does NOT cure the cluster residual, but it correctly denies that lensing ADDS to it.
2. **Lensing as the cleanest cluster-η test (bypasses HSE bias).** TEST A/B/C in
   `LENSING_MODALITY_LATEST_AND_MEASUREMENT` — Euclid/Rubin stacked η(r), WL-vs-X-ray ratio, environment-split GGL
   — measurable 2026-2030. (Note: the density-a0 reading predicts the WRONG sign for the radial η(r) shape on the
   local reading; only the untuned-Mpc-smoothed reading lands Tian's magnitude.)

**CLOSED / conceded:**
- The morphology-split CGM-gas escape (eROSITA Zhang+2025 disfavors the differential M_gas≈M*; split hardens to
  8.6–9.2σ). **#1 independent lensing loss, a0-independent.**
- The density-a0 cluster cure (gating calc = CLOSED-FALSIFIER; per-galaxy density coupling excluded 10.5σ).
- The Bullet "non-equilibrium phantom-lag" resolution (BROKEN — uses dynamical time √(R/a0) as field-response
  time; field re-settles on R/c ≪ collision time, so phantom tracks the gas). The Bullet REDUCES to the cluster
  residual (collisionless, galaxy-centred) — a conceded shared-MOND loss, not resolved, not a clean kill.

---

## THE MORPHOLOGY SPLIT — is there a live avenue given eROSITA closure? (Q4)

**Checked the AeST no-slip angle explicitly: it does NOT open one.** The split is early-minus-late g_obs at fixed
g_bar — a difference of two MEASURED lensing profiles. A lens-vs-dynamical-potential difference would need Φ≠Ψ
(slip), but AeST has NO slip; and even if it did, the slip is type-BLIND (the law is universal), so it cancels
exactly in the early−late difference (verified: model line identical for both types, FRONT4 audit). Environment
(density-a0) is excluded as the lever — the field RAR measured d log a0/d log(1+δ) = +0.05±0.04, 6.8–10.5σ from
the +0.5 needed. No relativistic effect is type-dependent at fixed g_bar in a universal law. **The morphology
split is the genuine, hard, a0-INDEPENDENT, framework-UNFAVORABLE loss — no live avenue. Say so plainly.**

---

## NET (both ways)

- **YES — AeST genuinely ties lensing to dynamics (Φ=Ψ, no slip), verified from the field equations and the
  literature. This REFRAMES "lensing = DM": four of the six classic arguments (Bullet, cluster SL+WL ~2×, strong
  lensing/Einstein radii, the bulk GGL-RAR) REDUCE to the single cluster-residual problem — they are NOT
  independent proofs.** This is a legitimate, load-bearing win for the framework's *epistemics* (it shrinks the
  evidence base from "many independent lensing proofs" to "one shared cluster problem").
- **BUT two arguments are genuinely independent and do NOT reduce:** (d) the matter power spectrum / CMB-lensing /
  cosmic-shear clustering — where the framework LOSES on its own footing (3rd peak P3/P2, a0-irrelevant), and
  (f) lensed-quasar substructure — open. And the morphology split (independent within GGL) stays a hard loss.
- **Footing:** one cosmetic false-win (door1 GGL table at local a0) to retract; ZERO false-deficits. The reframe
  does not depend on any footing trick — it is a field-equation identity.

No manufactured cure (the cluster residual, the 3rd peak, and the morphology split stay UNRESOLVED). No
high-priest dismissal (the AeST no-slip reframe is real and credited at full weight; it correctly denies that
lensing is an independent DM proof beyond the cluster problem). Quarantine held.
