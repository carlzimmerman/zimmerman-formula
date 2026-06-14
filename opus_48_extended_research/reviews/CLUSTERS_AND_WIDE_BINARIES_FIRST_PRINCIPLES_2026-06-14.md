# First-principles attack on the framework's two hardest fronts: clusters + wide binaries (2026-06-14)

*An 11-agent derive-then-hostile-refute workflow (5 routes × derive+refute + synthesis), every load-bearing
number independently re-derived (and cross-checked by hand). Carl asked for solutions DERIVED from the
framework. The honest verdict, both ways, no manufactured cure: **neither front is SOLVED from first
principles; both SURVIVE; both have genuine intrinsic structure and a sharp testable prediction.** Supporting
derivations: `CLUSTER_AEST_MASSTERM_2026-06-14.md`, `CLUSTER_DSUNRUH_BARYONS_2026-06-14.md`,
`WB_EFE_DERIVATION_2026-06-14.md` + the `.py` scripts in this folder.*

---

## CLUSTERS — CANDIDATE-UNPROVEN (one real right-scale mechanism; no first-principles closure)

**The genuine win (ruled IN, keep it):** the framework's covariant realization (AeST) carries an **intrinsic
scalar/aether mass term μ²Φ that ordinary MOND/QUMOND lacks.** It switches **ON at the cluster scale** (1/μ ~ 1
Mpc, CMB-pinned) and **OFF in galaxies** (10 kpc ≪ 1/μ — verified: AeST/MOND = 0.998 at 30 kpc), with the
**right sign at onset** — exactly where MOND misses ~2×. This is independently published (Durakovic–Skordis
2024) and verified here with two independent integrators. It moves clusters from *"MOND just fails"* to *"AeST
has a candidate at the right scale."*

**Why it does NOT close the 2× (the honest core):**
- With the **CMB-pinned 1/μ = 1 Mpc and the natural inner boundary condition**, the mass term gives a *deficit*
  — g_AeST/g_MOND at R500 = **0.21×**, not a 2× boost; the helpful 3.79× peak lands at **~6 Mpc (the wrong
  radius)**.
- Pushing the one rescue knob (the boundary shift χ_∞) to the **true physical condition Φ(∞)→0** *still* gives a
  deficit (~0.46×). η = 2.15 only comes from a **per-cluster tune** that pulls *away* from the physical
  asymptotics — "fitted, not predicted."
- **Scale tension (hard):** one μ cannot serve both — Mistele's bounds (verified) need 1/μ < 0.63 Mpc for
  clusters but 1/μ > 1 Mpc for galaxies. And **μ is a free *third* AeST constant, NOT welded to
  a₀ = c²√(Λ/32π)** — so any fix is *accommodated*, like every MOND cluster patch, not derived from the
  framework's law.
- **The lower a₀ costs you here:** η_framework/η_MOND = √(1.20/0.936) = **1.132 — clusters are +13% *harder*
  than regular MOND** (exact, baryon-independent, recomputed three ways on real eRASS1). Reported, not buried.
- The dS-Unruh-interpolation + baryon route is **PARTIAL** (a correct *diagnosis*, not a cure): honest baryon
  accounting leaves η ~ 2.15; even a contested 2× IGIMF doubling leaves η ~ 1.28.
- **Overclaims caught + dropped:** the aether-stress "~80% of the deficit" headline is a tuned κ knob (sweeps
  0.11–0.88 with an arbitrary zero-point) on a *broken* (μR)² expansion at μR=1.68; and "dS-Unruh is the weakest
  interpolation / sharpest failure" is false (the standard ν is weaker at every y — the route's own table prints
  it).

**The sharp testable prediction (this is real and falsifiable):** AeST predicts the cluster mass-excess is **not
a constant factor** but a **PEAK-then-DIP / phantom-negative-mass RAR** — extra g above MOND in a band, then
*below* MOND in the outskirts — with **peak radius ∝ √M500**. A monotone, constant-factor excess, or one
growing in the *outskirts* (as some 2024 hydrostatic analyses find), **kills** the AeST route. Plus the exact
parameter-free lock: the framework's ν fixes **η = 1.132 × (regular-MOND η) on every cluster.**

---

## WIDE BINARIES — SHARP-PREDICTION-PENDING-DATA (survives all data; does not yet decide)

**The clean derivation (verified, hand-checked):** a solar-neighborhood binary sits in the Milky Way's external
field **g_ext = V_c²/R₀ = 2.15×10⁻¹⁰ = 2.30 a₀** (framework), so it is **EFE-dominated**, not deep-MOND. Through
the textbook AQUAL anisotropic G_eff tensor (G_⊥/G = 1/μ, G_∥ stiffer along g_ext; matches
Bekenstein–Milgrom/Banik–Zhao), the orbit-averaged capped boost is **γ_cap = 1.324 (framework) vs 1.421
(standard MOND)**, with the transition at ~6 kau. **Because g_ext is fixed by the Galaxy, the framework's lower
a₀ (e = 2.30 vs 1.79) FORCES a *smaller* boost — derived analytically, not asserted.**

**This resolves the Chae-vs-Banik contradiction (the logic survives):** Banik's 16–19σ Newtonian null rejects
the *large* standard-MOND boost (γ ~ 1.5); the framework's smaller γ = 1.32 is consistent with that null AND
with the Saad–Ting baseline γ = 1.12 AND with Chae's 1.49 ± 0.2 band (0.85σ low). **The framework is consistent
with every reading — it survives wide binaries.**

**But it does NOT win them, and here is the honesty (both ways):**
- **No new physics:** γ_cap is a 1:1 re-encoding of a₀ — there is no z=0 framework-distinctive term. Wide
  binaries are a **shared MOND prediction**; the entire framework-vs-standard signal *is* the 20%-lower a₀
  already tested on SPARC/RAR.
- **The measurables are insensitive:** the framework's own banked program (`wb_a0_insensitivity.out`) shows the
  observed estimators barely move between a₀ = 9.36e-11 and 1.20e-10; the 7% lives only in the *un-measured*
  γ_cap, and eDR3 is degeneracy-limited (boost vs triple-contamination).
- **Direction is mildly *against*:** the field leans Newtonian (Banik 19σ), and γ = 1.32 is *farther* from
  Chae's 1.49 than standard MOND's 1.42 — if a detection sharpens, the lower a₀ is the disfavored side.
- **Overclaim caught:** the "γ(s) rises to 1.04–1.30" band splices two inconsistent estimators; the real
  *per-separation* curve for the framework's own (sharp/DSSYK) interpolation is **~Newtonian (+0–3.7%),
  undetectable in the current sample.** The band width *is* the unpinned interpolation choice, not a prediction.

**The exact curve to test:** report the **per-separation** γ(s) from one estimator — the framework's sharp
interp gives γ → 1.037 reached only at s ≫ 150 kau (≈ Newtonian across the eDR3/DR4 range); the angle-averaged
ceiling is γ_cap = 1.324. **Gaia DR4 (Dec 2026)**, with line-of-sight velocities → full 3D deprojection, decides.

---

## The honest bottom line (what to say, what not to say)

**Carl CAN say:**
- *Clusters:* "AeST carries an intrinsic mass term ordinary MOND lacks; it switches on at exactly the cluster
  scale with the right sign, is independently published, and predicts a falsifiable peak-then-dip cluster RAR
  with peak radius ∝ √M500 — a real channel, ruled in."
- *Wide binaries:* "A clean first-principles EFE application: g_ext = 2.30 a₀ gives a capped boost γ = 1.32, and
  because my a₀ is lower the framework *forces* a smaller boost than standard MOND — consistent with Banik's
  null AND Saad–Ting, reconciling the apparent Chae-vs-Banik contradiction."

**Carl must NOT say:** "first principles close the 2× cluster deficit," "the aether term covers ~80%," "the
framework solves wide binaries / they validate my a₀," or "γ(s) rises to 1.30." Each was tested and fails the
honesty bar. And the two real costs of the lower a₀ — **clusters +13% harder, and γ = 1.32 < 1.42** — are stated,
not hidden.

**Net:** the framework **survives both** (falsifiable, not falsified) and **closes neither** from first
principles. Clusters = a genuine right-scale candidate with a hard unsolved scale tension. Wide binaries = a
clean derived prediction that the current data cannot decide. No manufactured cure; the #1 rule held in both
directions.

## The next calculation (candidate → closed)

- **Clusters:** fit the *actual non-isothermal* AeST model (full μ²Φ, not the isothermal toy or the leading
  (μR)² expansion) to the eRASS1 η-vs-M500 relation, with **χ_∞ pinned by Φ(∞)→0 per cluster** (shot to ≥20
  Mpc) and **one CMB-pinned 1/μ held across SPARC *and* eRASS1 simultaneously.** If one physical μ + the natural
  BC reproduce η(M500) and the peak-then-dip shape → UPGRADE to CLOSES; if the galaxy-safe μ gives the verified
  0.21× deficit → FALSIFIED as a closure, banked as a prediction.
- **Wide binaries:** *derive which interpolation function the AeST covariant realization actually produces*
  (sharp/DSSYK → ~Newtonian +3.7%; soft → +30%) — that single unpinned knob turns the band into one line — then
  run the per-separation γ(s) through a realistic Gaia DR4 forward model (deprojection + triple contamination at
  the measured q², not q²=1) for the predicted detection σ.

*Independent hand cross-checks (this session, matching the agents): g_ext/a₀ = 2.29–2.30; EFE cap ν = 1.33;
η ≈ 1.84 at R500; the +13% lower-a₀ penalty = √1.282 = 1.132. Framework footing + both-ways honesty held;
quarantine held (Z/a₀ never asserted as derived; μ flagged as a free third constant).*
