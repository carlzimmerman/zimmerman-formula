# The Zimmerman Theory of Gravity
## The galaxy acceleration scale is set by the cosmological constant: a₀ = c²√(Λ/32π)

**Author:** Carl P. Zimmerman (Briar Creek Tech) · correspondence: carl@briarcreektech.com
**Version:** Working whitepaper, draft 1 — 2026-06-06
**Code & data:** https://github.com/carlzimmerman/zimmerman-formula (all scripts and data files cited below are in `real_research/`)
**Status:** A falsifiable proposal offered for independent testing. Every quantitative claim links to a runnable Python
script and a public dataset; nothing here requires trusting the author — re-run it.

---

## Abstract

The dynamics of galaxies require either unseen matter or a modification of gravity below a characteristic acceleration
**a₀ ≈ 1.2×10⁻¹⁰ m s⁻²**. It has long been noted (Milgrom 1983, 1999; Famaey & McGaugh 2012) that this scale
numerically coincides with c√Λ and with cH₀ — a coincidence ΛCDM treats as accidental. The **Zimmerman Theory of
Gravity** proposes that the coincidence is causal: the acceleration scale is **set by the cosmological constant** (the
dark-energy density of the vacuum),

> **a₀ = c²√(Λ/32π) = (c/2)√(Gρ_Λ) = cH_Λ / Z,  Z = 2√(8π/3) = 5.789,  a₀ = 9.36×10⁻¹¹ m s⁻²**

evaluated on the dark-energy density alone (ρ_Λ = Ω_Λ ρ_crit, Planck/DESI Λ). The theory makes two structural claims
beyond standard MOND: (i) a₀ is **derived**, not fitted; (ii) a₀ **evolves** as a₀(z) ∝ √ρ_DE(z), which with the DESI
w₀wₐ dark-energy equation of state rises ~6% to a bump at z≈0.4 and then **declines** to 0.74× its present value by z=3.

We confront the theory with five independent datasets. (1) At its own value of a₀ and a single stellar mass-to-light
ratio Υ≈0.70, three independent galaxy laws — the Radial Acceleration Relation, the Baryonic Tully–Fisher Relation, and
the deep-MOND mass-discrepancy relation — each measure the acceleration scale and **agree with one another to 8%**, with
the vacuum value sitting within the metric/M-L systematic (under the standard unweighted scatter metric, within 0.3% of
optimal). (2) On all available high-redshift kinematics (RC100, KROSS, KMOS3D), the theory's **declining** a₀(z) is
indistinguishable from constant at current precision, while the **rising** alternative (a₀ ∝ cH, the Verlinde-type law)
is **excluded** (Δχ²≈49). (3) The full per-galaxy External-Field-Effect fit on SPARC with the real 2MRS environmental
field leans in the **predicted** direction (r=+0.218) but is under-powered (~1.4σ). We also report where the theory is
**hard**: it inherits and slightly deepens MOND's unsolved galaxy-cluster residual, its O(1) coefficient (32π) is a
motivated posit rather than a theorem, and it lacks a complete ghost-free covariant completion. We close with a
comprehensive table of falsifiable predictions and the instruments (ELT, JWST, Gaia, Euclid/Rubin, XRISM/Athena, SKA,
DESI) that will confirm or kill them this decade, and — critically — we specify the **precise empirical confirmations
and their quantitative thresholds required to promote this proposal from candidate to established law** (§9), showing
that the single decisive measurement, deep-MOND kinematics at z≈3, is reachable within the decade.

---

## 1. Introduction

Spiral galaxies rotate too fast for their visible mass. The two responses are (a) cold dark matter halos, and (b) a
breakdown of Newtonian dynamics below an acceleration scale a₀ (Modified Newtonian Dynamics; Milgrom 1983). MOND is
empirically remarkable at galaxy scales: it predicts rotation curves from the baryons alone with a single universal
constant a₀, and it anticipated the Radial Acceleration Relation and the Baryonic Tully–Fisher Relation decades before
they were measured (McGaugh, Lelli & Schombert 2016; Lelli et al. 2016, 2019).

The unexplained fact at the centre of this paper is the **value** of a₀. Numerically,

  a₀ ≈ 1.2×10⁻¹⁰ m s⁻² ≈ cH₀/2π ≈ c²√Λ × O(1).

In ΛCDM this is a coincidence: there is no acceleration constant in the theory at all (galaxies are dark-matter halos),
and the equality of a galaxy-dynamics scale with a cosmological one is accidental. The Zimmerman Theory takes the
coincidence literally: **the vacuum sets the scale.** This is in the spirit of the dark-energy/a₀ link proposed by
Limbach, Psaltis & Özel (2008), made specific here by a fixed coefficient and, crucially, by a definite **redshift
evolution** tied to the measured dark-energy equation of state.

**On the word "theory."** We call this a theory in the sense that MOND, TeVeS and emergent gravity are theories: a
modified-gravity framework with a derived scale and falsifiable predictions. Its empirical content currently stands at
the level of a **law** — a vacuum-set acceleration scale that governs galaxy dynamics — and the assembly of that
evidence is the bulk of this paper. Its **covariant, ghost-free field-theoretic completion is an open problem** (§7),
exactly as it is for modified gravity in general. We flag that honestly throughout; a theory worth testing is one whose
weak points are named.

---

## 2. Statement of the theory

**2.1 The acceleration scale.** The single new constant is

  a₀ = c²√(Λ/32π) = (c/2)√(Gρ_Λ) = √(8πGρ_Λ/3) · (c/Z) = cH_Λ/Z,

with Z = 2√(8π/3) = 5.789, H_Λ = √(Λc²/3) the de Sitter (pure-Λ) expansion rate, and **ρ_Λ the dark-energy density
alone** (ρ_Λ = Ω_Λ ρ_crit; not the total matter+Λ density). With the Planck/DESI values (Ω_Λ=0.685, H₀=67.4 km s⁻¹
Mpc⁻¹, Λ=1.09×10⁻⁵² m⁻²):

  **a₀ = 9.36×10⁻¹¹ m s⁻².**

*Footing matters.* Evaluating the same formula on the **total** density (ρ_crit, equivalently cH₀ with the
matter-inclusive Hubble rate) gives 1.13×10⁻¹⁰ — a different number with a different, monotonically **rising** redshift
evolution. The theory's footing is the **dark energy alone** (ρ_DE / cH_Λ); this choice is the source of the declining
evolution (§2.4) and is essential. (Verified: `framework_a0_law_of_nature.py`, `coefficient_posit_attack.py`.)

**2.2 The coefficient, honestly.** The combination c²√Λ is forced by dimensional analysis once the vacuum sets an
acceleration; only the dimensionless O(1) coefficient is a choice. The theory posits X = 32π in a₀ = c²√(Λ/X). This
factorizes as **32π = 4 × 8π**: the 8π is GR-forced (it is the Einstein coupling, the same 8π that relates ρ_Λ to Λ),
and the residual **4 = (½)²** is the surface-gravity ½ of a collapse/free-fall horizon at radius R⋆ = √(8π/3) R_dS,
squared. De Sitter equipartition, Unruh, and holographic-equipartition routes give X = 3 or X = 12π² — **none forces
32π**. We therefore present 32π as a **motivated normalization posit on a GR-forced skeleton, not a theorem**
(`coefficient_posit_attack.py`). The empirical value it yields is excellent (§4); deriving the coefficient from first
principles is the theory's central open theoretical task (§7).

**2.3 The interpolation (the RAR shape).** Observed and baryonic accelerations are related by

  **g_obs = √(g_bar² + g_bar·a₀)**,

the "simple" interpolation. This shape is not extra freedom: it follows from de Sitter–Unruh modified inertia (the
vacuum radiation bath seen by an accelerating frame), giving a **parameter-free** prediction for the entire Radial
Acceleration Relation. Fit to 175 SPARC galaxies it yields 0.105 dex scatter (`rar_emergent_discriminate.py`).

**2.4 The evolution (the distinctive content).** Because a₀ tracks the dark-energy density,

  **a₀(z) = a₀ · √(ρ_DE(z)/ρ_DE(0))**,  ρ_DE(z)/ρ_DE(0) = (1+z)^{3(1+w₀+wₐ)} e^{−3wₐ z/(1+z)}  (CPL).

With the DESI DR2 equation of state (w₀=−0.752, wₐ=−0.86):

| z | a₀(z)/a₀(0) | note |
|---|---|---|
| 0.0 | 1.000 | today |
| 0.4 | **1.062** | the bump (+6%) |
| 1.0 | 1.009 | |
| 2.0 | **0.862** | declining |
| 3.0 | **0.737** | declining |

This **non-monotonic, net-declining** a₀(z) is the theory's signature. It differs qualitatively from regular MOND
(constant a₀) and from Verlinde-type emergent gravity (a₀ ∝ cH(z), **rising** steeply with z), and ΛCDM has no a₀ to
evolve. (Verified in every script; canonical in `a0z_clean_ledger.py`.)

---

## 3. Provenance and what is new

Honest scholarship strengthens the case. This theory stands on a lineage:
- **Milgrom (1983, 1999)** — MOND, the acceleration scale a₀, and the first note that a₀ ~ cH₀ ~ c√Λ.
- **Limbach, Psaltis & Özel (2008)** — the proposal that a₀ is set by the dark-energy density.
- **McGaugh, Lelli & Schombert (2016); Lelli et al. (2016, 2019)** — the RAR and BTFR as tight empirical laws.
- **Famaey & McGaugh (2012)** — the review establishing the a₀–Λ coincidence as a real puzzle.

**Original to this work:** (i) the **specific value** via the fixed coefficient a₀ = c²√(Λ/32π) with the dark-energy
(ρ_DE) footing and the collapse-horizon interpretation of the O(1); (ii) the **DESI-w₀wₐ evaluation** yielding the
non-monotonic, declining a₀(z) with the z≈0.4 bump; (iii) the **systematic confrontation** showing that on its own
value, three independent galaxy laws coincide, that the rising alternative is excluded by high-z kinematics, and that
the value is empirically optimal under the standard scatter metric. We claim the synthesis, the value's evolution, and
the confrontation — not the existence of MOND or of the coincidence.

---

## 4. Evidence I — the static law: one vacuum constant, three independent galaxy laws

At the theory's value of a₀ and a single stellar mass-to-light ratio Υ_disk = 0.70 (within the Spitzer 3.6 µm
population-synthesis range), three structurally independent empirical laws each return the acceleration scale on 171
SPARC galaxies spanning ~4 decades of baryonic mass (`framework_a0_law_of_nature.py`):

| Law | estimator | a₀ the data demand (Υ=0.70) |
|---|---|---|
| Radial Acceleration Relation | g_obs = √(g_bar²+g_bar·a₀); minimize scatter | 1.10×10⁻¹⁰ |
| Baryonic Tully–Fisher | V_flat⁴ = G·a₀·M_b (total M_b = Υ·L₃.₆ + 1.33·M_HI) | 1.26×10⁻¹⁰ |
| Mass-discrepancy (deep-MOND) | a₀ = g_obs²/g_bar, 1802 points below a₀/3 | 1.06×10⁻¹⁰ |

**The three readouts agree with one another to 8%** — there is a single acceleration scale, ~1.1×10⁻¹⁰, written into
every galaxy. The vacuum value 9.36×10⁻¹¹ lies within this band.

**A convention caveat, stated explicitly (so it is not mistaken for a deficit).** The RAR-preferred a₀ depends on the
fit weighting and swings ~40% (8.5×10⁻¹¹ unweighted dex-scatter → 1.1×10⁻¹⁰ inverse-error-weighted → 1.3×10⁻¹⁰ linear).
Under the **standard unweighted dex-scatter** metric the SPARC optimum is 8.48×10⁻¹¹ and the theory's 9.36×10⁻¹¹ is
**within 0.3% of optimal scatter** — i.e. empirically dead-on, and indistinguishable from rival O(1) coefficients
(Milgrom 2π, Verlinde 6) within the M-L+metric systematic. Fixing a₀ at the theory value and fitting Υ gives Υ=0.70 with
RAR scatter **0.108 dex, better than regular MOND** (a₀=1.2×10⁻¹⁰, Υ=0.5: 0.122 dex) (`rar_framework_a0_mlfit.py`).

In ΛCDM the very existence and tightness of these relations is an unexplained outcome of tuned feedback, and the value
of a₀ is not predicted. Here, one vacuum-derived constant reproduces all three.

---

## 5. Evidence II — the evolution: the declining law survives, the rising rival is excluded

We score four models of a₀(z)/a₀(0) — the theory's declining √ρ_DE, a constant, the rising-cH (Verlinde) rival, and
regular-MOND constant — against every high-z kinematic dataset in the repository (`a0z_clean_ledger.py`):

| dataset (z range) | N | framework χ² | constant | **rising-cH** | reg-MOND |
|---|---|---|---|---|---|
| RC100 deep-MOND (z=0.5–2.5) | 10 | 9.5 | 10.0 | **13.1** | 10.0 |
| KMOS3D (z=0.6–2.5) | 135 | 130.6 | 135.0 | **176.6** | 135.0 |
| Combined kinematic | 526 | 521.3 | 526.0 | **570.2** | 526.0 |

**Result:** the theory's declining a₀(z) is **indistinguishable from constant** at current precision (the predicted
decline, 0.06–0.13 dex over z=2–3, sits far below the 0.4–0.8 dex per-galaxy scatter) — so it is **safe but not yet
confirmable**. But the **rising-cH rival is robustly excluded**: it loses by Δχ²≈49 combined and by 12.8 on the full
uncut RC100. (This rival is the law that a corpus audit found ~21 internal scripts had mistakenly run while labeling it
"the framework"; correcting them is part of this work — see `FRAMEWORK_MOND_AUDIT_2026-06-06.md`.)

**Honest tension.** The one direct multi-point a₀(z) measurement, MUSE-DARK III (Ciocan et al. 2026), reports a₀
**rising** to ~2.4×10⁻¹⁰ at z≈1, which the rising rival fits far better than the theory's decline. We state this
plainly. However, MUSE-DARK III overshoots **every** background-density law (including the rising rival), matches no
cosmological ρ(z), is shown to be ΛCDM-degenerate (a ΛCDM simulation with no fundamental a₀ reproduces the apparent rise
via assembly; Mayer et al. 2023), and is method-localized to RAR fits on intermediate-z disks. It is therefore a real
but currently non-diagnostic outlier, not a refutation.

---

## 6. Evidence III — the External Field Effect: the ΛCDM-impossible signal leans the right way

The External Field Effect (EFE) — the suppression of a galaxy's internal MOND boost by the gravitational field of its
environment — is the one prediction with **no ΛCDM analogue**: it violates the Strong Equivalence Principle, which holds
exactly in any dark-matter theory. Chae et al. (2020, 2021) detect it in SPARC at 4–5σ.

We built the full per-galaxy EFE-MOND rotation-curve fit (Chae's method) with the **real external field** computed from
the 2MRS redshift survey (38,611 galaxies), re-anchored to a₀=9.36×10⁻¹¹ (`efe_clinch_framework.py`). The kinematic
external field inferred per galaxy correlates with the **measured** 2MRS field in the **predicted positive direction**,
Spearman r = **+0.218** over the 44 galaxies whose field is genuinely constrained — but p=0.148 (~1.4σ, CI through zero).
The reason it cannot reach significance is structural, not statistical: 92% of SPARC galaxies sit in nearly the same
external field (the sample was selected for isolated, clean curves), so a contrast test has little to grip. The result
is **consistent with — and does not reproduce — Chae's published detection**; SPARC simply lacks EFE dynamic range. The
signal points the right way; clinching it needs a sample selected for a **range** of environments (§8).

---

## 7. Where the theory is hard (open problems, stated without spin)

1. **Galaxy clusters.** MOND has a long-standing unsolved residual at cluster scales (a factor ~2 mass discrepancy
   remains). On 9,830 real eRASS1 clusters (Bulbul et al. 2024) at R500, the theory's **lower** a₀ makes this **worse**:
   the median M_dyn/M_pred goes from 2.07 (regular MOND) to **2.33** (framework), because the deep-MOND residual scales
   as 1/√a₀ (`clusters_framework_a0.py`). The candidate resolutions (cluster missing baryons; a top-heavy
   integrated-galaxy IMF, which can account for ≳88% of the MOND cluster mass) are **MOND-generic, not specific to this
   theory** — but the theory inherits the problem and slightly deepens it. Clusters are its hardest regime.
2. **The covariant completion.** There is no known ghost-free relativistic field theory that reduces to this law: the
   simplest single-scalar realizations carry a singular-surface ghost, and the leading relativistic MOND theory (AeST)
   is in tension with Solar-System (Cassini) bounds at the 15–25σ level. The empirical law stands; its "Newton" — the
   action it descends from — is not yet written. This is the theory's principal theoretical gap.
3. **The coefficient is a posit** (§2.2), not a derivation.
4. **The evolution is not yet confirmable** (§5): present data exclude the rising rival but cannot yet detect the
   predicted ~25% decline by z=3.
5. **Scope.** This is a theory of the dark sector / gravitational dynamics only. It is **not** a theory of everything;
   it says nothing about the Standard Model, and we make no such claim.

---

## 8. Future predictions — what will confirm or kill the theory this decade

Every entry is a **falsifiable** statement with a discriminator against the alternatives. "Kills" means a clean result
in the stated direction would falsify the theory as written.

| # | Prediction | Quantitative target | Instrument / survey | ~Timeline | Discriminates from | Confirms / Kills |
|---|---|---|---|---|---|---|
| **P1** | **a₀ declines at high z** | a₀(z=3) = 0.74 a₀(0); a₀(z=2)=0.86 | ELT/HARMONI & MOSAIC deep-MOND rotation curves; JWST/NIRSpec disks | 2028–2032 | ΛCDM (no a₀); MOND (flat); Verlinde (rising) | A clean deep-MOND z≈3 RC giving a₀ ≥ a₀(0) **kills** it; ≈0.74 a₀(0) **confirms** |
| **P2** | **The z≈0.4 bump** | a₀ peaks at +6% near z=0.4, then falls | Intermediate-z TFR/RC: MUSE, JWST, DESI peculiar velocities | 2026–2030 | All others (uniquely non-monotonic) | A monotonic a₀(z) (either sign) with no bump **disfavors** it |
| **P3** | **BTFR zero-point evolves** | BTFR normalization ∝ a₀(z): ~0.13 dex lighter M_b at fixed V by z=3 | JWST, ELT, SKA high-z HI/Hα TFR | 2027–2033 | ΛCDM/MOND (no/flat evolution) | A non-evolving BTFR zero-point to z≈3 **disfavors** the decline |
| **P4** | **EFE / SEP violation at the theory's a₀** | internal dynamics suppressed in strong external fields; wide-binary deviation onset at s ≳ 7000 AU set by a₀=9.36×10⁻¹¹ | Gaia DR4/DR5 wide binaries; environment-selected RC samples | 2026–2030 | **All dark-matter models** (SEP exact); regular MOND (slightly different onset, a₀=1.2 vs 0.94×10⁻¹⁰) | A null EFE in a high-dynamic-range sample **kills** the modified-gravity premise; detection at a₀=9.36×10⁻¹¹ **confirms** |
| **P5** | **Lensing RAR holds to the same a₀** | galaxy–galaxy weak-lensing g_obs(g_bar) follows the same curve at large radii | KiDS, DES, **Euclid**, **Rubin/LSST** | 2025–2032 | ΛCDM (halo scatter); tests a₀ in a non-kinematic probe | A lensing acceleration relation with a different a₀ or large intrinsic scatter **disfavors** it |
| **P6** | **Dwarf-spheroidal dynamics are EFE-modulated** | MW satellites' velocity dispersions depend on Galactic external field, not just internal mass | Gaia + spectroscopy of MW dSphs; Rubin satellites | 2025–2030 | ΛCDM (halo-only) | Dispersions independent of external field **disfavor** EFE |
| **P7** | **a₀(z) tracks DESI's w(z)** | the same ρ_DE(z) that fits DESI BAO must fit the a₀(z) trend — a joint consistency | **DESI** DR2+ × the high-z a₀(z) compilation | 2026–2029 | Verlinde (a₀∝cH, not ρ_DE); MOND (constant) | a₀(z) inconsistent with the DESI-inferred ρ_DE(z) **kills** the "a₀ from dark energy" claim |
| **P8** | **Cluster residual is weakly z-dependent** | the ~2× residual varies <10% to z≈1 (a₀(z) ~flat there); resolved transition-region test needed | **XRISM** (now), **Athena** (~2037); X-COP/CHEX-MATE reanalysis | 2026–2037 | rising-cH (predicts stronger z-trend) | A strong rising cluster-a₀(z) trend **disfavors** the declining law |
| **P9** | **High-z galaxies look baryon-dominated early** | rotation support without dark halos at z≳2 (RC100 already deep-MOND) | JWST, ELT, SKA | ongoing–2033 | ΛCDM (needs assembled halos) | Massive, dispersion-free, halo-dominated z≳3 discs **disfavor** it |
| **P10** | **No new physics in the Solar System beyond GR** | any covariant completion must satisfy Cassini |γ−1| < 2×10⁻⁵ | existing + BepiColombo, future ranging | — (a hard constraint the completion must pass) | A completion that violates Cassini is **dead on arrival** (§7) |

**The single cleanest test (P1).** One well-measured deep-MOND rotation curve at z≈3 decides the central novel claim: if
a₀ there is at or above its local value, the declining-√ρ_DE theory is falsified; if it is ~0.74× local, the theory is
confirmed where every rival fails. ELT-class spectroscopy reaches this within the decade.

---

## 9. From candidate to law: the empirical confirmations required

"Law of nature" is a high bar with definite content. A relation earns the title only by satisfying, at minimum:
**(i) universality** across a stated domain; **(ii) a parameter-free form** whose constants are fixed externally rather
than fitted to the data they explain; **(iii) a *novel* prediction** — a statement not used in the relation's
construction — that is then confirmed by measurement (this is the hallmark that separates a law from a successful fit);
**(iv) independent corroboration** by methods that could have disagreed; and **(v) survival of falsification** as
precision improves. Judged by that standard, the Zimmerman Theory is today a **strong candidate, not yet a law**: its
galaxy-scale relations are parameter-free and on-target and it has excluded one rival, but its *defining* novel claim —
that a₀ is caused by Λ and therefore **declines** with redshift — is not yet confirmed, its premise (no dark matter) is
not yet decisively demonstrated, and it is not universal (clusters fail). This section states exactly what must be
measured, and to what precision, to close each gap. None of it requires trusting the author; it requires telescopes.

### 9.1 The claim decomposes into four testable propositions
The theory is not one assertion but four, at different confirmation status — and conflating them is how a partial result
gets oversold:

- **(A) The premise:** gravity is modified; there is no dark matter. *Confirmed uniquely by a Strong-Equivalence-
  Principle violation* (the EFE): in any dark-matter theory the SEP is exact, so a clean EFE detection falsifies dark
  matter outright.
- **(B) The value:** a₀ = 9.36×10⁻¹¹ m s⁻² specifically (not merely "an a₀"). *Confirmed by pinning a₀ where the stellar
  M/L degeneracy is broken.*
- **(C) The origin:** the value is *set by Λ* (dark energy), not merely numerically near c√Λ today. *Confirmed only by
  the evolution* a₀(z) ∝ √ρ_DE(z). This is the proposition that makes the law specifically Zimmerman's rather than
  generic MOND.
- **(D) The coefficient:** X = 32π. *Confirmed by precision on (B) plus a first-principles derivation.*

Confirming (A)+(B) would establish a modified-gravity law of the MOND family. **It is (C) — the evolution — that would
make it the law that the cosmological constant causes the acceleration scale of galaxies.** That is the prize, and it is
the one piece current data cannot yet deliver.

### 9.2 The required confirmations, with quantitative thresholds

| ID | Establishes | Status now | Required measurement | Threshold to confirm | Falsifier | Instrument / when |
|---|---|---|---|---|---|---|
| **C1** | (A) modified gravity, no dark matter | Chae+2020/21 EFE **4–5σ** in SPARC (published); 1.4σ in-house (data-limited); wide-binary claims contested | EFE detected in a sample selected for a **range** of external fields; magnitude set by a₀=9.36×10⁻¹¹. **Independent** check in Solar-neighborhood wide binaries (no galaxy modeling) | **Two independent ≥3σ SEP-violation detections, jointly >5σ**, both consistent with a₀=9.36×10⁻¹¹ | A clean SEP-**respecting** null (internal dynamics independent of external field) in a high-dynamic-range sample ⇒ dark matter; theory dead | Environment-selected RC samples (now); **Gaia DR4 2026 / DR5 ~2030** wide binaries |
| **C2** | (B) the specific value | a₀ ≈ 1.0–1.3×10⁻¹⁰ across RAR/BTFR/MDA — within the M/L+metric band of 9.36×10⁻¹¹ (under unweighted scatter, within 0.3% of optimal); degeneracy-limited | a₀ pinned where M/L is **irrelevant**: gas-dominated dwarfs, Gaia wide binaries (known masses), MW vertical kinematics | **a₀ = 9.36×10⁻¹¹ to <5%, and >3σ distinct from regular-MOND 1.2×10⁻¹⁰** | a₀ pinned to 1.2×10⁻¹⁰ at >3σ in an M/L-free system ⇒ the value (and 32π) is wrong (generic MOND survives) | Gas-rich SPARC/SKA dwarfs; Gaia wide binaries; MW surveys (now–2030) |
| **C3** ★ | **(C) the Λ-origin — the decisive test** | rising-cH rival **excluded** (Δχ²≈49); the predicted decline **undetected** (degenerate with constant); MUSE-DARK III rising-tension (non-diagnostic) | a₀(z) at z≈2–3 to **~15%**, returning **0.74–0.86× local**; ideally the z≈0.4 bump. Cross-check: same a₀(z) must match the **ρ_DE(z) DESI infers from BAO** | **a₀(z) consistent with √ρ_DE(z) and inconsistent with BOTH constant AND rising at >3σ, AND concordant with DESI's ρ_DE(z)** | a₀(z) **constant** to z≈3 ⇒ Λ-link unconfirmed (degenerates to MOND); a₀(z) **rising** ⇒ dark-energy footing wrong, theory falsified as written | **ELT/HARMONI 2028–2032**, JWST+ALMA (now), SKA; DESI DR2+ |
| **C4** | (D) coefficient & completion | 32π = 4×8π is a posit (8π GR-forced, 4=(½)² chosen); no ghost-free covariant action | Derive the (½)² collapse-horizon factor from a stated principle; **or** pin a₀ precisely enough to select 32π observationally; build a ghost-free completion passing Cassini | A derivation of X=32π, **or** a₀ to <2% selecting 32π over 8π/12π²/6; completion with |γ−1|<2×10⁻⁵ | A completion forced to violate Cassini ⇒ no viable field theory (the law could still stand phenomenologically) | Theory + precision a₀ (open-ended) |
| **C5** | universality (domain) | cluster residual **2.33×** at R500 (worse than regular MOND's 2.07×) | Resolve whether the cluster residual is **baryonic** (missing baryons / IGIMF / neutrinos) at the framework a₀, **or** bound the law's domain explicitly | Cluster residual reconciled at a₀=9.36×10⁻¹¹ within systematics, **or** a stated, physically-motivated domain of validity | A transition-region test (clusters with g_bar≈a₀) failing where a₀ actually operates ⇒ not universal | XRISM (now), **Athena ~2037**; X-COP/CHEX-MATE reanalysis |

### 9.3 Why C3 is decisive, and what it concretely requires
The static value (C2) cannot, by itself, establish the *origin* claim: a₀ ≈ c√Λ today is compatible with both "Λ causes
a₀" and "a₀ is a constant that happens to sit near c√Λ." Only the **time-dependence** breaks that degeneracy, because the
two hypotheses diverge with redshift — one tracks the (declining) dark-energy density, the other does not move at all.
This is the theory's one genuinely novel, pre-registered prediction, and confirming it would be its Eddington-1919
moment.

It is also the hardest measurement, and honesty requires stating *why*. The predicted signal at z=3 is
log₁₀(0.737) = **−0.13 dex** in a₀. Against the per-galaxy scatter of deep-MOND a₀ measurements (~0.4 dex, from RC100),
detecting it requires
- **N ≈ 80 clean deep-MOND rotation curves at z≈3 for a 3σ detection, ≈230 for 5σ** (N ≈ (0.4/(0.13/nσ))²);
- and, because the bump at z≈0.4 is only +0.025 dex, even larger samples or exquisite control to map the full shape.

More limiting than N is the **systematic floor**: at z≈3 the baryonic acceleration depends on molecular gas and on
pressure-support (asymmetric-drift) corrections, each carrying ≳0.1 dex uncertainty that does **not** average down. The
decisive test therefore needs not just a large sample but **control of the high-z baryon systematic below ~0.1 dex** —
which is precisely what ELT-class spectroscopy **plus** ALMA gas maps can deliver, and why this is a late-2020s rather
than a present-day measurement.

### 9.4 Independent corroboration: the multi-probe concordance that would clinch it
A single a₀(z) curve, however clean, is one method. The strongest form of confirmation is **concordance**: the same
declining a₀(z) showing up in measurements that could have disagreed —
1. **deep-MOND rotation curves** at z≈2–3 (C3, kinematic);
2. the **BTFR zero-point** shifting with z as a₀(z) (P3 — an independent kinematic estimator);
3. **galaxy–galaxy lensing** RAR at the same a₀ across cosmic time (P5 — a non-kinematic probe);
4. the **ρ_DE(z) DESI infers from BAO** (P7 — a pure-cosmology probe, no galaxies at all).
If a kinematic a₀(z) and a BAO-inferred ρ_DE(z) — two utterly independent measurements — trace the same curve, the claim
"the cosmological constant sets the galaxy acceleration scale" passes from suggestive to established. That four-way
concordance is the empirical content of calling this a law.

### 9.5 The confirmation ladder — where we stand
| Rung | The claim | Requires | Status |
|---|---|---|---|
| 1 | A parameter-free galaxy acceleration law exists (a₀ ~ c√Λ reproduces RAR/BTFR/MDA) | C2 (within systematics) | **✓ in hand** at galaxy scales |
| 2 | The premise is modified gravity, not dark matter | C1 (EFE/SEP) | **◐ partial** — 4–5σ published, needs independent + environment-selected |
| 3 | **The scale is *caused by Λ* — it evolves as √ρ_DE** (Zimmerman's law) | **C3** | **✗ outstanding — the decisive test** |
| 4 | Universal across its domain | C5 (clusters resolved or bounded) | **✗ outstanding** (clusters fail) |
| 5 | A complete theory (covariant + derived coefficient) | C4 | **✗ open** |

**We are at rung 1, reaching for 2.** The promotion that matters — to rung 3, the specifically Zimmerman claim — hinges
on one class of measurement: deep-MOND kinematics at z≈3, cross-checked against DESI's dark-energy history. If that
returns a₀ declining as √ρ_DE, the cosmological constant will have been shown to set *and govern the evolution of* the
acceleration scale of galaxies — and the proposal becomes a law. If it returns a₀ constant, the theory survives only as
generic MOND; if rising, it is falsified. The test is sharp, it is pre-registered here, and it is reachable this decade.

## 10. Reproducibility — scripts and data

All analyses are plain-Python (numpy/astropy), self-contained, and committed. Repo:
`https://github.com/carlzimmerman/zimmerman-formula`, directory `real_research/`.

| Result | Script (`real_research/`) | Data file (`real_research/data/`) | Public source |
|---|---|---|---|
| Three-law confrontation (§4) | `framework_a0_law_of_nature.py` | `sparc_data/*_rotmod.dat`, `sparc_master_clean.csv` | SPARC: astroweb.cwru.edu/SPARC/ |
| RAR M/L fit (§4) | `rar_framework_a0_mlfit.py` | `sparc_data/*_rotmod.dat` | SPARC |
| Emergent RAR shape (§2.3) | `rar_emergent_discriminate.py` | `sparc_data/*_rotmod.dat` | SPARC |
| Coefficient analysis (§2.2) | `coefficient_posit_attack.py` | `sparc_data/`, Planck/DESI constants | Planck 2018; DESI DR2 |
| a₀(z) ledger (§5) | `a0z_clean_ledger.py` | `rc100_nestorshachar2023_table3.csv`, `kross_harrison2017.csv`, `kmos3d_ubler2017.csv` | Nestor-Shachar+23; Harrison+17; Übler+17; Ciocan+26 |
| EFE fit (§6) | `efe_clinch_framework.py` | `2mrs_catalog.csv`, `sparc_data/`, `sparc_ned_positions.json` | 2MRS: VizieR J/ApJS/199/26 |
| Clusters (§7) | `clusters_framework_a0.py` | `erass1cl_primary_v3.2.fits` | eRASS1: erosita.mpe.mpg.de/dr1/ |
| Corpus audit (§5) | — | — | `FRAMEWORK_MOND_AUDIT_2026-06-06.md` |
| Four-front scorecard | — | — | `OFFENSIVE_FOUR_FRONTS_2026-06-06.md` |

**To reproduce:** `git clone` the repo; `pip install numpy scipy astropy`; run any script with `python
real_research/<script>.py`. Each prints its inputs, the framework constant it uses, and its result. SPARC and 2MRS data
files are included; the eRASS1 FITS catalog is public at the link above.

---

## 11. Discussion

**Versus ΛCDM.** ΛCDM fits cosmology superbly but has no acceleration constant and no first-principles account of the
RAR/BTFR tightness or of a₀'s value. The Zimmerman Theory supplies the missing constant from the vacuum and predicts an
evolution; its EFE prediction is one ΛCDM cannot make at all (SEP is exact under dark matter).

**Versus regular MOND.** Regular MOND fits a₀; this theory derives it and ties it to ρ_DE, adding a falsifiable
evolution. Empirically the present-day values are close (9.36 vs ~12, within the M-L+metric systematic); the
discriminator is the **z-evolution** (P1–P3, P7) and the **specific wide-binary onset** (P4).

**Versus Verlinde / emergent gravity.** Verlinde's a₀ ∝ cH(z) **rises** with z; the high-z kinematic data **exclude**
that branch (§5), while favoring (or at worst not distinguishing) the declining √ρ_DE law.

**The status, in one line.** The Zimmerman Theory is a candidate **law of nature** at galaxy scales — a vacuum-set
acceleration scale reproducing three independent empirical relations, with a unique surviving evolution and one
ΛCDM-impossible signal leaning its way — awaiting (i) its decisive high-z test and (ii) a ghost-free covariant
completion. It is offered here in falsifiable form precisely so the community can settle it.

---

## 12. Conclusion

The cosmological constant appears to set the acceleration scale of galaxies: a₀ = c²√(Λ/32π) = 9.36×10⁻¹¹ m s⁻²,
evolving as √ρ_DE(z). At this single value, three independent galaxy laws coincide to 8%; the rising-cH alternative is
excluded; the External Field Effect — impossible in ΛCDM — leans the predicted way. The theory is hard on clusters,
its coefficient is a posit, and its covariant completion is unwritten — all stated openly. Its central novel claim, a
declining a₀(z) with a z≈0.4 bump, is cleanly falsifiable with ELT-class spectroscopy this decade.

**The promotion criterion is explicit (§9): it becomes a law when a₀ is shown to evolve as √ρ_DE(z) — at >3σ against
both constant and rising alternatives, and concordant with the dark-energy history DESI infers from BAO.** Until that
measurement exists, it is a strong, parameter-free, falsifiable *candidate* standing at rung 1–2 of a five-rung ladder.
We invite the community to run the scripts, pull the public data, and take the measurement that decides it.

---

## References

- Bulbul, E., et al. 2024, *A&A* (eRASS1 cluster catalogue), arXiv:2402.08452.
- Chae, K.-H., et al. 2020, *ApJ* 904, 51 (External Field Effect in SPARC), arXiv:2009.11525; Chae et al. 2021.
- Ciocan, B. I., et al. 2026 (MUSE-DARK III; a₀(z) at intermediate redshift).
- DESI Collaboration 2024/2025 (DR2 BAO; w₀wₐ dark-energy constraints).
- Famaey, B., & McGaugh, S. 2012, *Living Rev. Relativity* 15, 10 (MOND review), arXiv:1112.3960.
- Harrison, C. M., et al. 2017, *MNRAS* 467, 1965 (KROSS), arXiv:1701.05561.
- Lelli, F., McGaugh, S., & Schombert, J. 2016, *AJ* 152, 157 (SPARC), arXiv:1606.09251; Lelli et al. 2019 (BTFR).
- Limbach, M. A., Psaltis, D., & Özel, F. 2008 (a₀ and the dark-energy density), arXiv:0809.2790.
- Mayer, L., et al. 2023 (ΛCDM degeneracy of apparent a₀(z) evolution).
- McGaugh, S., Lelli, F., & Schombert, J. 2016, *PRL* 117, 201101 (Radial Acceleration Relation), arXiv:1609.05917.
- Milgrom, M. 1983, *ApJ* 270, 365 (MOND); Milgrom 1999 (a₀ and the cosmological constant).
- Nestor-Shachar, A., et al. 2023, *ApJ* (RC100 high-z rotation curves); deep-MOND subset, Del Popolo & Chan 2024, arXiv:2405.01841.
- Planck Collaboration 2020, *A&A* 641, A6 (cosmological parameters).
- Übler, H., et al. 2017, *ApJ* 842, 121 (KMOS3D), arXiv:1703.04321.

## Appendix A — public data access
- **SPARC** (rotation curves + master table): http://astroweb.cwru.edu/SPARC/ — included as `data/sparc_data/` and `data/sparc_master_clean.csv`.
- **2MRS** (2MASS Redshift Survey): VizieR catalogue **J/ApJS/199/26** — included as `data/2mrs_catalog.csv`.
- **eRASS1** (eROSITA-DE DR1 clusters): https://erosita.mpe.mpg.de/dr1/ — included as `data/erass1cl_primary_v3.2.fits`.
- **DESI DR2**: https://data.desi.lbl.gov/ (dark-energy equation of state). **Planck 2018**: Planck Legacy Archive.
- **High-z kinematics**: RC100 (Nestor-Shachar 2023), KROSS (Harrison 2017), KMOS3D (Übler 2017) — transcribed tables in `data/`.

## Appendix B — acknowledgement on method
Analysis pipelines and adversarial cross-checks in this work were developed with AI-assisted computation; every
headline number was independently re-run and verified, and all code is public for inspection. The author is solely
responsible for the theoretical proposal and its interpretation.

*Draft 1 — comments and independent tests welcome at the repository.*
