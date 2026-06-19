# The non-adiabatic relational sigma-spread: a falsifiable MI-vs-MG cluster test (2026-06-19)

*9-agent both-ways workflow; 4 verified scripts in sigma_spread/. Develops + CORRECTS Fable's
GENUINE_MI_CLUSTER_DISTINCTIVE (which over-claimed a clean "MG=0, CDM=0" discriminator).*

**HEADLINE: a GENUINE but CONFOUND-LIMITED test of modified inertia — not the advertised clean
discriminator.** Two parts are SOLID and kernel-independent: (i) **MG = 0 is a structural theorem**
(elliptic no-history field theory, momentary-a_ex EFE, any a0); (ii) the **MI plunger-hotter SIGN and
EXISTENCE are theorems** (guaranteed by theta(0)>theta(1), which Milgrom forces; constant theta = the
adiabatic/MG limit = 0). BUT the adversarial pass overturned the "CDM=0" half: **tidal-shock heating
FAKES a same-signed, comparable-amplitude (~2-5% at y~1) sigma-vs-infall-phase correlation** — the
confound I flagged is real. The MI content survives as the DIFFERENCE: MI is ~2x hotter AND has the
decisively OPPOSITE RADIAL TREND, so the test is DEGRADED ~4-5x over the mimic, not dead — deployable
only as the JOINT (amplitude + radial-trend) test. Amplitude 4.5-9.7% (sigma) is KERNEL-HOSTAGE (rides
the unknown theta(y); factor-2; the MI-kernel workflow is trying to pin it). Carriers are UDGs ONLY
(~0-45 usable per rich cluster; dSph marginal, ellipticals adiabatic-dead). Test path: proof-of-concept
upper limit NOW (recast LEWIS Hydra + Coma KCWI/MUSE UDG sigma vs the kr infall proxy, ~2026-27);
marginal ~3sigma dedicated MUSE/KCWI campaign ~2028-32 (N~100-200, IF purity~0.7); definitive 3-5sigma
ELT-HARMONI/MOSAIC resolved-star era ~2032+. Load-bearing caveats: (a) the kr infall proxy works where
the signal is WEAK (inner-shell tension, needs non-kinematic tidal/quenching tags for purity~0.4);
(b) amplitude unverified until theta(y) is pinned. No manufactured win; Fable's over-claim corrected.

---

# The non-adiabatic relational σ-spread: a concrete falsifiable test of modified inertia at clusters

A synthesis of the four verified scripts in `/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/sigma_spread/` (`mi_sigma_spread_amplitude.py`, `population_nonadiabatic.py`, `discriminator_robustness.py`, `feasibility.py`), the banked verdict `opus_48_extended_research/reviews/GENUINE_MI_CLUSTER_DISTINCTIVE_2026-06-15.md`, and the Milgrom-2022 (arXiv:2208.07073 = PRD 106 064060) A(ω)/θ(y) functional reused from `cluster_closure/mi_dynamic_route.py` and `real_research/reviews/member_MI_nonadiabatic_plunge.py`. All four scripts run clean and the numbers below reproduce on re-execution.

---

## 1. The SIGNAL — MI σ-spread amplitude vs non-adiabaticity y

The framework's inertia is a time-nonlocal functional of the acceleration history (Milgrom-2022 Eq. 3/5). A cluster member feels the cluster's external field a_ex, which oscillates at ω_ex as the member orbits; its internal stars orbit at ω_in. The EFE on the member enters through the two-frequency relation A(ω_in) = a_in + a_ex·θ(y), y ≡ ω_ex/ω_in (Eq. 34). Because θ is a **function** of y, two members at the **same momentary cluster-centric radius** (same |a_ex|) but different infall phase get **different effective inertia**, hence different internal σ.

**R(y) = σ_MI(infall phase)/σ_QS at matched a_ex** (fiducial deep-MOND member, θ = 2/(1+y²)):

| y = ω_ex/ω_in | R(y) | deviation |
|---|---|---|
| 0.01 (adiabatic) | 1.0000 | +0.0% |
| 0.10 | 1.0005 | +0.1% |
| 0.50 | 1.0127 | +1.3% |
| 1.00 (plunging) | 1.0416 | +4.2% |
| 2.00 (deep radial) | 1.0964 | +9.6% |

- **Sign (kernel-independent theorem):** R > 1 and grows with y. A plunger (θ(~1)≈1) sheds the adiabatic θ(0)≈few external loading that a circular member carries → smaller inertia argument → deeper MOND → **larger** internal boost → **hotter** σ. This holds for **any** decreasing θ — it is not a kernel choice.
- **Existence (kernel-independent theorem):** the spread is nonzero whenever θ(0) > θ(1), which Milgrom forces (θ(1)=1, θ decreasing, θ(0)~few). A constant θ is exactly the adiabatic/MG limit (Eq. 35, a₀-degenerate) → spread 0. So **nonzero is guaranteed; zero is the MG/CDM prediction.**
- **|dR/dy| peaks at y ≈ 1** (1.02 rational, 1.06 e^{1−y}, 1.12 e^{(1−y)/2}) — the plunging band is exactly where the discriminating sensitivity lives.

**Peak amplitude** (cross-infall-phase σ-spread, plunging window y ≤ 1.5, deep-MOND member):
- Milgrom's 3 verbatim θ kernels [2/(1+y²) θ(0)=2; e^{1−y} θ(0)=e; e^{(1−y)/2} θ(0)=1.65]: **4.5%–8.6% in σ** (9.0%–17.3% in boost).
- With two extra brackets (Gaussian, Lorentzian θ(0)=3): up to 9.7%.
- Over the requested grid {0.01,0.1,0.5,1,2} including the y=2 tail: **9.4%**.
- Most-diffuse members (a_in=0.3a₀, a_ex=2a₀): **6.4–12.0%**, reproducing the banked 6.2–11.8%.

**Kernel-dependence (the load-bearing caveat):** amplitude scales with θ(0) and spans a factor ~2 (4.5%→9.7%) across reasonable forms. Only θ(1)=1, θ decreasing, θ(0)~few are fixed; Milgrom states plainly "we have no knowledge of the form of θ(y)." **The sign and existence are theorems; the magnitude is unverified.** Quote a range, never a point value.

---

## 2. The MEMBER POPULATION — which members cross y ~ 1, counts per cluster

y = ω_ex/ω_in = (cluster orbital frequency at pericenter)/(member internal stellar frequency). Crossing y~1 requires a **large, diffuse, low-σ member on a radial/plunging orbit** — internally slow (small ω_in) and externally fast (small pericenter, large ω_ex). From `population_nonadiabatic.py` in a Coma-like M₂₀₀=10¹⁵ M_⊙ NFW cluster (c=5, R₂₀₀=2 Mpc; orbit integrator measures a 3.35 Gyr radial period):

| member type | ω_in | y at pericenter | verdict |
|---|---|---|---|
| **UDG** (σ=20, R=3 kpc) | 6.8/Gyr | **1.17 @150 kpc, 1.53 @100 kpc** | **CROSSES y~1** |
| extreme low-σ UDG (σ=10) | — | 2.34 @peri, 0.91 @500 kpc | crosses out to ~0.9 Mpc |
| dSph (σ=8, R=0.3 kpc) | 27/Gyr | 0.18–0.38 | MARGINAL, never crosses |
| normal elliptical (σ=200) | 68/Gyr | 0.05–0.15 | DEEP ADIABATIC → ZERO signal (a₀-degenerate trap) |

**The carriers are UDGs only.** dSph are internally too fast (only the largest, deepest plungers graze y~0.4); normal ellipticals sit in the adiabatic a₀-degenerate trap and must be excluded.

**Counts per rich (M~10¹⁵) cluster:** UDG census ~200 (van der Burg+2016) to ~1000 (Yagi+2016 Coma); × radial/recent-infall fraction 0.3–0.6 (Coma UDGs ARE predominantly first-infall plungers, Yagi/Alabi MNRAS 479 3308) × near-pericenter duty cycle 0.10–0.25 (measured 8.5–21.9% over one radial period) → **~6–150 UDGs physically in the y>0.5 regime per snapshot**; × resolved-kinematics fraction 0.05–0.3 → **~0–45 USABLE per rich cluster today.** Stacking ~10 rich clusters (Coma/Perseus/Virgo/Fornax/Frontier-Fields/4MOST) gives tens-to-~hundred matched plungers. **A small, specific subset — not a generic cluster population.**

---

## 3. The OBSERVATIONAL TEST — precision, proxy, sample size, instruments, timeline

**Estimator:** at matched cluster-centric radius (matched |a_ex|), split members into a low-y "virialized/circular" bin and a high-y "plunge" bin by an infall-phase proxy; test whether mean internal σ differs. Null (MG/CDM-inertia): Δσ = 0. Signal (MI): Δσ = (dilution × f) × σ_obj.

**(a) σ precision.** Per-object resolution of a 6–13% spread on σ~10–20 km/s needs **~0.6–2.6 km/s** per-member σ error. Reached only by resolved-star spectroscopy of nearby (D≲20 Mpc) Fornax/Virgo dSph (100–300 stars/object; ELT-HARMONI decisively). At Coma/Hydra distances individual stars are unresolved → integrated-light σ at **15–40% per object** (KCWI Coma UDG Y358: 19±3 km/s = 16%; LEWIS Hydra UDG11: 20±8 = 40%) → the spread is a **population statistic only**. JWST-NIRSpec floor ~30–50 km/s is **out** for this σ regime.

**(b) Infall-phase proxy — the dominant degradation.** Projected phase-space kr = (|Δv|/σ_cl)(R_proj/r₂₀₀): low kr → virialized, high kr → recent radial infall. Two projection problems (R_proj≠R_3D, v_los≠v_3D) scramble both axes. The Monte-Carlo in `feasibility.py` finds the kr proxy has **near-zero or negative** true-infall contrast in the **inner shell where a_ex and the signal are strongest** (virialized-dominated; high |Δv_los| at small R_proj selects high-random-velocity virialized members, not infallers). kr develops useful contrast only at larger radius (0.6–0.8 r₂₀₀) where a_ex — and the signal — is smaller. **A genuine tension: the proxy works where the signal is weak.** Non-kinematic tags (tidal morphology = recent infall, first-passage star-formation quenching, backsplash) are **required** to push the effective contrast to ~0.4 (the fiducial dilution); kr alone gives ~0.1×.

**(c) Sample size** (two-bin, σ_obj=12 km/s, dilution 0.40):

| f | err/member | N (3σ) | N (5σ) |
|---|---|---|---|
| 0.10 | 1.0 km/s (ELT stars) | 156 | 434 |
| 0.10 | 2–3 km/s | 625–1406 | 1736–3906 |
| 0.13 | 1.0 km/s | 92 | 257 |
| 0.06 | 2.0 km/s | 1736 | 4823 |

Worst plausible corner (f=6%, purity 0.6) → **thousands**, effectively out of reach. Best (f=13%, ELT err~1, purity~0.8) → **~100–200** for 3σ. The test lives or dies on (i) which θ(y) nature picked (sets f in 6–13%) and (ii) infall-phase tagging purity.

**(d) Instruments, targets, timeline:**
- **Now (~free, proof-of-concept / upper limit):** recast existing LEWIS Hydra-I MUSE σ (18 UDGs) + Coma KCWI/MUSE UDG σ against the kr proxy at matched R_proj. N~20–50, err 15–40% → low power, establishes the method + a first weak amplitude constraint. ~1 paper, 2026–27.
- **~2028–2032 (marginal ~3σ):** dedicated MUSE+KCWI campaign on Coma/Hydra/Fornax UDGs+dSph, ~100–200 members spanning infall phase at matched radius, σ err pushed to ~2–3 km/s, IF purity ~0.7 holds.
- **~2032+ (ELT era, definitive 3–5σ):** HARMONI resolved-star σ to ~1–2 km/s on Fornax/Virgo dSph + MOSAIC multiplexed cluster-member σ; N~few hundred at matched radius — conditional on controlling the projection dilution (forward-model kr→phase) and on θ(y) putting f in the upper band.

---

## 4. The DISCRIMINATOR — MG = 0 (verified), CDM ≠ 0 (the tidal confound)

**MG = exactly 0 — VERIFIED, and it is structural.** QUMOND/AQUAL/AeST are elliptic (no-history) field theories; the EFE is solved at the instant t from the instantaneous source → it depends **only on the momentary a_ex** (Milgrom-2022 verbatim, lines 690–693). Sweeping y at fixed a_ex, the MG boost is flat to machine precision for **any** a₀ and any interpolation function (a₀ only rigidly rescales the single shared value — it cannot manufacture a spread MG structurally lacks). A best-fit MG-a₀ leaves the entire MI spread as an irreducible residual. **The signal is non-a₀-degenerate by construction — relationally** (cross-member at fixed a_ex; a single member's single orbit is still a₀-absorbable, stated not hidden). This is the genuine, clean half of the test.

**CDM ≠ 0 — the make-or-break confound (the adversarial finding, confirmed).** The claim "CDM gives exactly zero" is **FALSE** and was an overclaim in the original framing. CDM has no inertia channel, but CDM members suffer **tidal-shock heating** at pericenter (Gnedin-Ostriker 1999) governed by the **same** adiabatic parameter: χ_ad(y) = (1+1/y²)^(−γ), γ~2.5. So tidal heating **also** correlates internal σ with infall phase, with the **same sign** (plungers hotter) and a **comparable amplitude**:

| y | CDM tidal Δσ/σ (eps_imp=25%) | MI Δσ/σ |
|---|---|---|
| 0.50 | 0.2% | 1.3% |
| 1.00 | 2.2% | 5.1% |
| 1.50 | 4.9% | 10.8% |

The **bare** "σ correlates with infall phase" is therefore a **mush** — pure CDM fakes it.

**Is it separable? YES — by the OPPOSITE RADIAL TREND (separator S1, the single most robust handle):**

| a_ex/a₀ | MI spread (y:0.05→1) | tidal strength | trend |
|---|---|---|---|
| 0.3 | 12.0% | 0.3 | MI active, tidal weak |
| 1.0 | 8.3% | 1.0 | both moderate |
| 3.0 | 3.6% | 3.0 | MI falling, tidal rising |
| 30 | 0.4% | 30 | MI≈0, tidal PEAKS |

**MI peaks in the MOND-transition zone (a_ex~a₀, cluster outskirts R₅₀₀–R₂₀₀) and collapses to ~0 in the deep core (μ→1, EFE off); tidal heating does the opposite — it peaks in the core.** They are **radially anti-correlated**, cleanly separable by binning the σ-vs-infall-phase correlation across cluster radius. Two further separators reinforce it: **S2** — MI is reversible/current-phase (no accumulation) while tidal heating is cumulative (older infallers hotter at fixed current phase, a hysteresis residual); **S3** — tidal heating co-occurs with mass loss/tidal tails, so restricting to undisrupted members (intact King profile) removes the heaviest contaminants. **The discriminator is the JOINT relational signature, not the bare correlation.**

---

## 5. Honest verdict — both ways, quarantine held

**Is it a genuine, MG-impossible test of modified inertia? Yes — as the joint relational signature, not the bare correlation.** Three things are robust theorems: (i) MG gives **exactly zero** infall-phase σ-spread at matched radius for any a₀ (structural, elliptic-PDE, verified verbatim); (ii) the MI plunger-hotter **sign** holds for any decreasing θ; (iii) the spread is **non-a₀-degenerate** relationally. The arithmetic reproduces on all four scripts (MI 4.5–9.7% across kernels; diffuse 6.4–12.0% confirmed).

**What it is NOT:** it is **not** the advertised clean "MG=0, CDM=0" discriminator. **CDM is not zero** — tidal-shock heating produces a same-signed, same-y, comparable-amplitude (~2–5% at y~1) σ-vs-infall-phase correlation in pure CDM. The MI-specific content is the **difference after subtracting the confound** (MI runs ~2× hotter than CDM tidal at matched plunge and, decisively, has the **opposite radial trend**). The MI residual exceeds the mimic by ~4–5× — so the test is **degraded, not dead**, but it must be deployed as the joint radial+hysteresis+undisrupted signature, never the bare correlation.

**What it needs, and by when:** (1) the unknown θ(y) to put f in the upper 6–13% band; (2) infall-phase tagging purity pushed to ~0.75–0.85 via non-kinematic tags (the dominant systematic — kr alone fails in the signal-strong inner shell); (3) ~100–300 resolved-internal-σ UDG/dSph members at matched radius spanning infall phase. **Timeline:** proof-of-concept upper limit **now** (existing LEWIS Hydra-I + Coma KCWI/MUSE); marginal ~3σ **~2028–2032** (dedicated VLT/Keck); definitive 3–5σ in the **ELT era (~2032+)**.

**The load-bearing caveat:** the entire amplitude rides on the **A(ω)/θ(y) kernel, which is unknown** (Milgrom: "we have no knowledge of the form of θ(y)"). The sign (plunger hotter) and existence (MI nonzero vs MG structural zero) are kernel-independent theorems; the magnitude spans a factor ~2 and is unverified. A near-constant θ would shrink it toward zero, though Milgrom's "θ(0)~few" excludes the pathological limit.

**This is a TEST, not a closure** of the cluster residual: the cycle-averaged mean dynamical mass is **not** raised (`mi_dynamic_route.py`: A(ω) moves the mean the wrong way; deep-MOND scale invariance pins M·G·a₀ = η·σ⁴ shared by MI and MG). Quarantine held — a₀/Z/κ not asserted derived. The refuted "MI-tangential-vs-MG-radial ellipsoid sign" claim is not used. Both ways, no exception: the confound and the demanding subset are conceded at full weight; the MG-structural-zero, the plunger-hotter sign theorem, the non-a₀-degeneracy, and the separable opposite radial trend are credited at full weight.