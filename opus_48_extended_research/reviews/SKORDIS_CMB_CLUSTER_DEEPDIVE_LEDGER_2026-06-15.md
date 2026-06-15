# Skordis geometric framework + the CMB third peak + the cluster residual + the "fishy" data check (2026-06-15)

*Carl's ask: review Skordis's work for a geometric angle; solve/explain the two remaining genuinely-independent
losses (cluster residual η≈2.33, CMB third peak); deep-dive the data provenance because "this seems fishy since
everything else checks out." 11-agent ultrathink workflow, CAMB 1.6.6 recomputes (real Boltzmann code), primary
AeST literature, eROSITA + Planck provenance. Both ways, anti-motivated-reasoning. Source memos:
`SKORDIS_GEOMETRIC_FRAMEWORK_REVIEW`, `ROUTE2_CMB_THROUGH_AEST`, `ROUTE3_CLUSTER_RESIDUAL_SOLUTION_OR_EXPLANATION`,
`ROUTE4_DATA_PROVENANCE_CLUSTERS_CMB_FISHY_CHECK`, `ROUTE5_UNIFICATION_COST` (all `_2026-06-15`).*

---

## The headline (both ways)

**Skordis's AeST is a real, covariant, ghost-free geometric host that genuinely FITS the Planck CMB (third peak
included) and survives GW170817 — the machinery for the dark-matter-illusion thesis exists and works. But it works at
a NAMED price (a second early-universe Ω, a free cluster mass μ, an underived Z), the unification is galactic-only,
and the data is NOT fishy: the CMB is rock-solid (the loss is a parameter cost, not a data error) and the cluster ~2×
is real-but-soft and systematic-limited.** "Everything checks out, so the data is fishy" is itself the overstatement.

## Skordis's geometric framework

AeST (Skordis-Złošnik 2021, PRL 127 161302 = arXiv:2007.00082): ONE metric + ONE unit-timelike vector A_μ (the
"aether," A·A=−1, ∇·A=3H on FRW) + ONE shift-symmetric scalar φ. Matter couples only to g (EP holds); A_μ picks the
cosmic rest frame — exactly the structure the de Sitter-Unruh inertia needs. **Lineage:** TeVeS (Bekenstein-Sanders)
introduced the unit-vector for correct lensing but was bimetric and **killed by GW170817** (c_T≠c); AeST keeps the
{φ,A_μ} content on ONE metric with c_T=c in all backgrounds — it **survived GW170817 where TeVeS died.** Two
structural wins fall out free: **(1) no-slip lensing** (A⁰∼√(−g⁰⁰) ⇒ Ψ=Φ ⇒ lensing mass = dynamical mass — the
structural reason the lensing front reframed); **(2) a₀-CMB-safety** (the spatial-gradient sector Y=0 on FRW ⇒ a₀
provably absent from linear perturbation theory).

**The load-bearing decoupling:** a₀ lives ONLY in the spatial-gradient Y-sector (a forced Y^{3/2} term — the √-law,
n=3/2, matching the framework). The cosmological **dark-matter-mimic lives in the ORTHOGONAL K(Q) sector**
(shift-symmetric k-essence, a minimum at Q₀≠0 gives a^{−3} dust + a cosmological constant). a₀ and the dust density
are independent slots of the same free function.

**Does it derive Z or the scalar density? NO to both.** The geometry forces a₀∼√Λ at the level of FORM and SCALE
(Gibbons-Hawking horizon) but: Z (≈5.79) is un-pinned (six horizon-entropy routes give a₀=κ·c√(Gρ_Λ) with κ free:
κ=½⇒Z=5.79, Verlinde⇒6, thermal⇒2π); the dust density is the free integration constant I₀ ("the density ρ̄ is not
(classically) predicted" — the authors' words). **Form+scale yes; coefficient+CMB-unification no.**

## The CMB third peak — AeST FITS it, at a unification cost; NOT fishy

**AeST fits the full Planck CMB + matter power spectrum** (Skordis-Złošnik 2021, first-of-its-kind for relativistic
MOND). Mechanism: the k-essence scalar's energy density redshifts as a^{−3} (pressureless dust), mimicking CDM.
**CAMB 1.6.6 recompute (this session, real Boltzmann code):** P3/P2 rises monotonically with Ω_c h²: **0.527
(baryon-only) → 0.673 → 0.793 → 0.894 → 0.980 (ΛCDM).** A pure modified-inertia / baryon-only universe (a₀ adds 0 to
the linear transfer functions) **fails the third peak by ANY tuning (best ≈0.54).** The third peak directly measures
the clustering pressureless density; a₀ cannot supply it.

**THE COST (the honest distinctive finding):** AeST supplies the clustering field — but its amplitude is the FREE
integration constant I₀ (~Ω_cdm≈0.26), **provably orthogonal to a₀=c²√(Λ/32π).** ρ_DE/ρ_CDM≈2.6 today and the two
sectors z-scale differently (const vs (1+z)³, diverging ~10⁸-10⁹ by recombination) — **one number provably cannot set
both.** "Two dark sectors, one number" holds at z=0 galaxies (a₀↔Λ does RAR/BTFR) but **FAILS at the CMB** (needs a
second, independently-tuned Ω). This is the AeST authors' own admission.

**Is it fishy? NO — firm, not a reflex.** The third peak (ℓ≈800) sits **deep in the cosmic-variance-limited band**
(Planck TT is CV-limited below ℓ≈1800) — cannot be removed by a better instrument or foreground re-analysis;
independently confirmed by **ACT DR6 and SPT-3G** (Ω_c h²=0.118±0.001, <1%, different sky/beams/systematics); the
known Planck anomalies (A_L 2.8σ, low-ℓ deficit) live at LOW ℓ, not the third peak. **The correct rebuttal is "AeST
fits Planck at +1 parameter," NEVER "Planck is wrong."**

## The cluster residual — SOFTENED, NOT CURED (and any AeST cure is fit-at-a-cost)

Four sub-routes, each honestly closed or open-at-a-cost:
- **AeST μ²Φ mass term (Durakovic-Skordis 2024):** RIGHT-signed peak (corrects the banked "wrong-signed" — gas
  "more compressed than MOND... more apparent dark matter") **but non-monotone** (peak-then-deficit "as if negative
  mass density"), double-bound by the **Mistele 2023 squeeze** (galaxy-WL needs m²/f_G<1 Mpc⁻², clusters need ≳1 —
  same free mass pulled opposite ways), per-cluster-tuned, μ FREE (not a₀=Λ). Candidate, NOT a demonstrated cure (no
  fit to eRASS1; authors say "remains to be seen," "future work").
- **Neutrinos: DEAD** — needs Σmν~6 eV; DESI 2024 Σmν<0.072 eV excludes by ~80×.
- **Baryons: a ~⅓ reducer, not a closer** — η 2.82→2.33→~1.7 floor; the missing gas is expelled BEYOND R500 (wrong
  radius); undiminished (~2.0-2.2) in gas-complete clusters. The "budget incomplete" premise VINDICATED; the
  "therefore no deficit" conclusion REFUTED.
- **The AeST dark-fluid does BOTH** (same a^{−3} dust mode that fits the CMB, clustering at cluster scales): the most
  promising, **genuinely literature-OPEN** ("whether the MOND missing mass in clusters could be addressed without an
  additional DM component beyond the k-essence scalar" — unresolved) — but **fit-at-a-cost** (a separate
  ghost-condensate density m~6500 H₀, not from a₀=Λ; breaks the unification like the CMB).

**The systematic softening (the honest, decisive lever):** eRASS1 M500 is a WL-calibrated count-rate proxy. Li+2024:
**WL runs ~110% above hydrostatic AND kinematic** (which agree with each other) — collaboration-flagged, brackets η
across **[~1.0, 2.33]**. Like-for-like same-radius gap ~76% (110% partly R500-aperture inflation). XRISM measures
non-thermal pressure DIRECTLY at 2-13% (A2029 ≤2%) — NOT the 52% the hydrostatic-bias defense needs, so the gap is
NOT non-thermal pressure; WL independently biased high 20-50% by projection/triaxiality. **Convergent TRUE η(R500) ≈
1.3-1.9.** Crucially the framework's OWN lower a₀ **inflates η by +13%** (√(1.2/0.936)=1.133) — the OPPOSITE of a
footing rescue. Significance 1.9-3.7σ vs the 0.10-0.20 dex floor.

**Verdict:** REAL, MOND-SHARED, SOFT, central, lensing-confirmed (no-slip ⇒ the cluster lensing 2× is the SAME
residual, not a second DM proof), softened to ~1.3-1.9 but NOT erased (lower end >1, undiminished in gas-complete
clusters), and UNCURED as a unification win.

## The "fishy" verdict — both ways, no conspiracy, no dismissal

- **Clusters — the instinct has GENUINE MERIT (partially vindicated):** the eRASS1 mass is a WL-calibrated proxy, and
  the collaboration ITSELF flags WL running ~110% above hydrostatic+kinematic. The cluster mass scale IS ~2×
  systematic-limited and the raw 2.33 overstates the equilibrium truth (true ~1.3-1.9). **This is a known, sourced,
  collaboration-flagged systematic — NOT fishiness, NOT a conspiracy — and it softens but does NOT erase the loss.**
- **CMB — the instinct is WRONG (no merit), but the right rebuttal:** the third peak is CV-limited, three-experiment-
  confirmed, anomalies at low-ℓ. NO artifact to find. **The honest line is "AeST fits it at +1 parameter," not
  "Planck is wrong."** Refusing to call it fishy is the honest physics, not high-priest dismissal.

## The honest corrected standing

**"Everything else checks out" is itself an overstatement** — several "else" items do NOT cleanly check out:
- **Genuinely checks out:** galaxy RAR/BTFR via a₀=9.355e-11; a₀↔Λ as a real unification of the dark-ENERGY face
  (Ω_DE=0.685); the AeST host is real, ghost-free, c_T=c (survived GW170817), no-slip lensing, fits the CMB.
- **Contested / non-diagnostic (does NOT cleanly check out):** morphology split (contested), a₀(z) (MUSE measures it
  RISING, non-diagnostic), wide binaries (MOND-degenerate), cluster lensing (reframed = same residual, not a new win).
- **Two real losses:** CMB third peak (FIT-BY-AeST-AT-A-COST, one extra Ω = I₀, unification galactic-only); cluster
  η≈2.33 (SOFT/systematic-limited ~1.3-1.9/UNCURED).

**The cost of the Skordis machinery (named, not hidden):** beyond a₀=Λ, the DM-illusion thesis on the AeST host needs
(1) a second early-universe Ω~0.26 (I₀, the CMB/clustering dust); (2) a free double-bound cluster mass μ; (3) an
underived Z; (4) the K(Q) function shape. **Standing UNCHANGED: live + partly favorable, zero referee-proof kills, no
fishy data, two real MOND-shared costs.** Quarantine held: a₀/Z never asserted derived.

## One line

AeST genuinely FITS the CMB third peak and is Skordis's honest geometric host for the dark-matter-illusion thesis —
but at a real, named price (a second early-universe Ω, a free double-bound cluster mass, an underived Z); the CMB is
rock-solid-not-fishy (the loss is unification economy, not a data error) and the cluster ~2× is real-but-soft and
systematic-limited (~1.3-1.9, collaboration-flagged WL, +13% worse on the framework's own a₀) — so "everything checks
out, the data is fishy" is itself the overstatement.

*Both ways, no exception: the AeST CMB fit + the GW170817 survival + the cluster systematic softening + the
right-signed mass term are credited at full weight; the unification cost, the underived Z, the dead neutrinos, the
uncured cluster residual, and the rock-solid CMB are conceded at full weight; the "fishy" framing is corrected in
both directions (clusters partly right, CMB wrong). Quarantine held.*
