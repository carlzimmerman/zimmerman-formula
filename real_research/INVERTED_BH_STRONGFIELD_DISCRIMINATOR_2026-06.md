# Strong-Field MI-vs-MG Discriminator: Quantifying the Inverted-BH Corollary

**Date:** 2026-06-26 · **Mode:** QUANTIFY a published corollary, both-ways, against the real literature
**Source claim:** `papers/INVERTED_BH_DUALITY_2026.md` §5 + `FRONTIER_CONSEQUENCES_INVERTED_BH_2026-06.md` Frontier 1 (DOI 10.5281/zenodo.20947913)
**Footing:** a₀ = cH_Λ/Z, Z = 2√(8π/3) = 5.78881; dual a₀_BH = c⁴/4GMZ; r_cross = √Z·r_s = 2.406 r_s; x_ISCO = Z/9 = 0.643.
**LOCAL ONLY — do not git-push (Carl's standing instruction).**

All shifts verified in sympy + mpmath (dps=40). Both GR limits checked (shadow b = 3√3 M = 5.196 M; ISCO = 6 M; ISCO at α=0 returns exactly 6.0). No manufactured win, no high-priesting.

---

## 0. The framework's prediction: a NULL (this is the anchor)

The modified-inertia (MI) reading forces **exactly-GR** strong-field observables — shadow, photon sphere, ISCO frequency, ringdown QNM spectrum, inspiral waveform — for every black hole. The dual a₀_BH = c⁴/4GMZ self-cancels by two structural facts: (i) mass-independence (r_cross = 2.406 r_s and x_ISCO = 0.643 depend only on r/r_s, already inside the GR metric → absorbed by covariance + EP), and (ii) the free-fall / Hartle–Hawking theorem (MI responds to *proper* acceleration; a geodesic detector sees no horizon bath; all clean BH observables are geodesic).

**So the framework predicts 0% deviation on shadow/ISCO/QNM.** Critical anti-overclaim: GR *also* predicts 0%. A clean GR-consistent measurement therefore **falsifies rivals that shift the metric; it never confirms the framework** (a null-vs-null with GR is at best a weak consistency point). The test's only discriminating axis is MI-vs-MG — the strong-field extension of the banked Cassini axis.

---

## 1. RIVAL 1 — MOG / STVG (Moffat): DISTINGUISHABLE

Metric (geometrized G_N = c = 1, gravitational charge Q² = α(1+α)M², enhanced G = G_N(1+α)):
> f(r) = 1 − 2(1+α)M/r + α(1+α)M²/r²

**Analytic laws (sympy series, small α — independently re-derived here):**
- Photon sphere: **r_ph = 3M + (7/3)M·α**
- Shadow, bare-M normalization (Moffat's own; shadow scales ~(1+α)): **δb/b = +(5/6)α**
- Shadow, ADM/measured-mass normalization (what EHT actually uses — Sgr A* mass from S-stars gives GM_ADM = (1+α)GM): **δb/b = −(1/6)α + (29/216)α²**

**Numeric table (verified mpmath, dps=40):**

| α | shadow (bare-M) | shadow (ADM) | ISCO radius | EHT/galaxy anchor |
|---|---|---|---|---|
| 0.01 | +0.83% | −0.17% | +0.75% | — |
| 0.05 | +4.16% | −0.80% | +3.74% | — |
| 0.10 | +8.30% | −1.54% | +7.46% | — |
| 0.30 | +24.8% | −4.04% | +22.2% | — |
| 1.0 | +81.3% | −9.36% | +72.2% | — |
| 1.13 | +91.7% | −10.0% | +81.4% | M87* shadow-fit (Moffat 2019, 1904.04142) |

QNM (eikonal real freq Ω_ph = √f(r_ph)/r_ph): **decreases** ≈ −8.3%/0.1α (−0.83·α to leading order).

**The load-bearing both-ways subtlety — mass normalization sets sign AND size.** At fixed *bare* M the shadow GROWS (+(5/6)α); at fixed *measured/ADM* mass it SHRINKS (−(1/6)α, saturating near −20% at α~8–10). EHT measures ADM mass, so the honest observational shift is the ADM branch — *smaller* than Moffat's headline (1+α) number. This matters: the bare-M "+83%/α" overstates what EHT would see.

**Honest α window.** Galaxy rotation needs α~8–10 (Moffat–Rahvar 2013), but horizon-scale α is NOT theory-pinned (running G is expected to make it smaller near the BH). Moffat's own M87* shadow fit gives α = 1.13 ± 0.30; Sgr A* gives α consistent with 0. So the honest horizon window is **α ∈ [0, ~1.13]**.

**Current bounds (literature):** EHT already constrains 0 < α < 0.044 (Sgr A*), 0.040 < α < 0.232 (M87*) [EPJC 82 (2022) 304, Schwarzschild-MOG shadows]. EHT shadow precision today ~±9–10% (Sgr A* δ = −0.08 ± 0.09, ~10% of Kerr).

**Resolvability (verified thresholds):**
- ngEHT (2030s, ~2% target shadow fidelity): resolves **α > 0.024** (bare-M) to **α > 0.12** (ADM). Even a modest horizon α~0.1 gives +8% (bare-M) / −1.5% (ADM) — ngEHT-resolvable in the bare-M reading, marginal in the ADM reading.
- LISA (2035+, ringdown spectroscopy ~0.1–1%): the −8.3%/0.1α QNM slope makes **α > ~0.006** LISA-detectable; EMRIs/MBH inspirals add inspiral-phase reach.

**VERDICT (MOG): DISTINGUISHABLE, REAL, DECADAL.** A confirmed pure-GR shadow/ringdown at ngEHT (2030s) / LISA (2035+) precision EXCLUDES horizon-scale MOG above α ~ 0.02–0.12, falsifying that rival while being consistent with (not confirming) the framework's GR null. Significance: a percent-level shadow detection would be exclusionary at ngEHT (2σ+ at the few-percent level); LISA ringdown is the cleaner channel. MOG is the rival the test actually bites.

---

## 2. RIVAL 2 — AeST / Aether-Scalar-Tensor (Skordis–Zlosnik, the framework's own host): NOT DISTINGUISHABLE (test null vs AeST)

This is the corollary's most important both-ways correction, and it goes AGAINST the paper's broad claim.

**Decisive reference: "Stealth black holes in Aether Scalar Tensor theory" (arXiv:2412.15395, Dec 2024).** AeST black holes are **STEALTH**: the background metric is *exactly* a GR vacuum/electrovac solution (Schwarzschild / Reissner–Nordström), carrying only **secondary hair** (non-trivial scalar/vector fields, but no new conserved charge, geometrically invisible). For the physical q=1 case the unique solution is the RN metric; one branch joins continuously onto the AeST cosmological solution.

**Two independent reasons AeST → GR in the strong field:**
1. **Stealth (2412.15395):** the metric is exactly GR, so *every geodesic observable* — shadow, photon sphere (1.5 r_s), ISCO frequency, lensing, GW inspiral — is identical to GR. Shadow shift = 0, ISCO shift = 0, inspiral shift = 0. The authors themselves state the only possible discriminators are NON-geodesic: "quasinormal modes... or thermodynamics."
2. **Scale separation (verified):** the AeST MOND scalar carries the MOND length L_M = c²/a₀ = 9.6×10²⁶ m. Versus Sgr A*'s r_s = 1.27×10¹⁰ m that is **L_M/r_s ≈ 7.6×10¹⁶ (~17 orders)**. The scalar is utterly negligible / screened at the horizon, so AeST BH solutions reduce to Schwarzschild/Kerr independent of the stealth argument.

The only AeST channel that could ever differ is a sub-percent, uncharacterized QNM/thermodynamic difference from the hair's perturbation sector on a GR background — deep below the ngEHT/LISA floor and not quantified in the literature. The c_T = c / GW170817 constraint is satisfied structurally (AeST tensor modes propagate at c by construction), which is *exactly* why AeST keeps MOND without a strong-field metric handle.

**VERDICT (AeST): NOT DISTINGUISHABLE — the test is null-vs-null vs AeST.** AeST predicts the SAME exactly-GR shadow/ISCO/inspiral as the framework. The shadow/ISCO test does NOT separate the framework's MI null from AeST. **The paper's §5 claim that "a metric-MOND completion (AeST, MOG)... predicts shifted strong-field observables" is OVERSTATED for AeST specifically** — AeST's published BHs are stealth = GR geometry.

**Genericity caveat (both-ways honesty):** 2412.15395 solves specific spherical static branches; it does not fully close whether *non-stealth* hairy AeST BHs exist in other parameter regimes. But the existence of an observationally-consistent stealth=GR branch is enough to break a *clean* falsification claim against AeST. Against AeST the test is non-diagnostic.

---

## 3. Residual framework strong-field signature? (would it be 3-way?)

**No.** The free-fall/Hartle–Hawking theorem + mass-independence force the framework to EXACTLY GR on all geodesic observables — that is the whole point of the null. The lone non-geodesic loophole (proper-accelerated accretion/jet plasma at r_cross = 2.406 r_s, where x = a/a₀_BH = O(1)) is swamped by MHD + radiation pressure (~10⁵ orders at Sgr A*), so it is not a clean test. There is no residual positive framework signature. The test is **2-way (MOG vs {framework = AeST = GR})**, not 3-way.

---

## 4. Is the strong-field MI-vs-MG test REAL?

| Rival | Distinguishable? | Shift | Resolvable? | Significance | When |
|---|---|---|---|---|---|
| **MOG/STVG** | **YES** | shadow ±(5/6)α bare / −(1/6)α ADM; ISCO +; QNM −8%/0.1α | ngEHT α>0.024–0.12; LISA α>0.006 | exclusionary at percent level; EHT already α<0.044 (SgrA*) | ngEHT 2030s, LISA 2035+ |
| **AeST** | **NO** (stealth = GR) | 0% geodesic; sub-% uncharacterized QNM only | below floor | null-vs-null | n/a |
| **Framework (MI)** | predicts NULL (=GR) | 0% | — | falsifies rivals, never confirms self | — |

**HONEST HEADLINE:** The strong-field MI-vs-MG test is **REAL vs MOG, NULL vs AeST — i.e. PARTIAL**. It is a **decadal extension of Cassini's MI-vs-MG axis to the strong field** — a genuine NEW discriminator the published paper introduced, now quantified. It bites one rival (MOG) and is non-diagnostic against the framework's own host theory (AeST), which is itself GR-in-the-strong-field. The framework predicts a NULL; a clean GR shadow/ringdown falsifies MOG (above α~0.02–0.12) but does not confirm the framework.

---

## 5. WHAT TO TELL CARL — both ways

**The honest YES.** The corollary is a real, new, rigorous consequence not among the banked six, and it IS a genuine discriminator — against MOG. MOG shifts the metric at O(α): shadow ±(5/6)α (bare-M) or −(1/6)α (ADM), ISCO +7.5%/0.1α, QNM −8%/0.1α. EHT already bounds α < 0.044 at Sgr A*; ngEHT (2030s) reaches α~0.02–0.12 and LISA (2035+) reaches α~0.006. A clean GR result excludes horizon-scale MOG and is consistent with (never confirms) the framework's null. The duality itself (a₀_BH = c⁴/4GMZ, r_cross = 2.406 r_s, x_ISCO = 0.643) is machine-exact and I reproduced all of it.

**The honest NO / correction.** The paper's §5 lumps AeST with MOG ("AeST, MOG... predicts shifted strong-field observables"). **For AeST that is OVERSTATED.** The framework's own host theory (Skordis–Zlosnik) has *published stealth black holes* with EXACT GR geometry (arXiv:2412.15395, RN/Schwarzschild + secondary hair), and the MOND scalar sits ~17 orders below the horizon scale (verified L_M/r_s ≈ 7.6×10¹⁶). So AeST ALSO predicts GR shadow/ISCO/inspiral — the test is **null-vs-null against AeST and does not separate the framework from it.** The honest asymmetry the prompt anticipated is confirmed against the literature: **MOG distinguishable, AeST not.**

**Three standing limits (do not let this inflate):** (1) it is a NULL, not a detection — only a falsification asymmetry, never a framework win; (2) its only axis is MI-vs-MG, the *same axis as banked Cassini* — it extends Cassini to strong field, it does not open an independent axis; (3) it is decadal+ (ngEHT 2030s, LISA 2035+), and the ADM-normalized MOG shift may sit near the ngEHT floor for modest α. The two banked near-term fronts (a₀(z) BTFR-sign, s^TX SME dipole) remain sharper.

**Recommendation:** narrow the paper's §5 AeST claim. Against AeST the strong-field test is null-vs-null (non-diagnostic, the AeST stealth branch matches GR); **MOG is the only rival in the ngEHT/LISA crosshairs.** Never "no doors" — this is a real, narrow, far, partial door that bites MOG.

---

## Reproducibility

MOG metric f(r) = 1 − 2(1+α)M/r + α(1+α)M²/r²; photon sphere outer root, ISCO from 3ff′ − 2rf′² + rff″ = 0, shadow b = r/√f at r_ph, all sympy-symbolic + mpmath dps=40. GR limits verified: shadow 3√3 M = 5.196 M, ISCO = 6 M (ISCO at α=0 → exactly 6.0). Framework dual Z = 5.78881, √Z = 2.40599, Z/9 = 0.64320. AeST scale L_M = c²/a₀ = 9.60×10²⁶ m, r_s(SgrA*) = 1.27×10¹⁰ m, ratio 7.56×10¹⁶.

**Sources:** arXiv:2412.15395 (AeST stealth BHs, Dec 2024); Moffat 2019 arXiv:1904.04142 (Schw-MOG shadow ~(1+α), α=1.13±0.30 M87*); EPJC 82 (2022) 304 (EHT α bounds); EHT Sgr A* I (arXiv:2311.08680, δ precision); ngEHT 2030s ~2% target. Skordis–Zlosnik 2021 (AeST, MOND scalar mass).
