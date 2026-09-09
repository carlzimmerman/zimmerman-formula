# L41 — the cluster source, as a specification any proposal can be run against

`L41_cluster_specification.py` + `.out` — **21 checks, 10 controls PASS, 11 FAIL; the FAILs are the finding.**
Runs in 2 s. Both a₀ footings (9.3619e-11 canonical, 1.1279e-10 alt) throughout.

Seven lanes closed every mechanism this programme owns for the cluster residual, and each reported a
*negative*. This lane assembles them into the one thing they collectively determine — a **positive
specification** — and then asks the question no single lane could ask: **is that specification satisfiable
by any object at all?**

---

## 0. The controls, first

The risk in a synthesis lane is quoting rather than verifying. Every number the argument leans on is
recomputed here from its own data, with independent code.

| control | reproduced | published | source lane |
|---|---|---|---|
| **K0** cluster cosmic ratio | M_dark/M_bar = **5.73 ± 0.68** (12% scatter), f_bar = **0.149** | 5.73 ± 0.68, 0.149 | L7 |
| **K1** required boost | Δ_req = **5.47 s^(0.811 ± 0.071)**, rms 0.094 dex; cluster/galaxy ratio **2.3–5.3** | 5.47 s^0.811, 2.2–5.1 | L2 |
| **K2** pair ratio | N = **1900**, A_Newton = **5.645 ± 0.136**, M_dark/M_bar = **30.9 ± 1.5** | 1900, 5.645, 30.9 ± 1.6 | L21 |
| **K3** projection machinery | analytic NFW ΔΣ to **2.1e-3** | — | new here |
| **P0** positive control | an NFW dark component gives shear slope **−0.820** vs measured **−0.851 ± 0.040** (0.5σ) | — | new here |
| **P1** L24's new constraint | framework phantom slope **−0.309** vs measured **−0.851**, difference **+0.542 at 9σ** | +0.53 ± 0.06, 9σ | L24 C11 |
| **D1/D2** source slope | ρ_X ~ r^**(−1.42)** over 40–750 kpc | −1.53 | g04a |

P1 matters: L24's shape constraint is the newest and least-tested ingredient, and it is here **reproduced
with different code, a different baryon build and a different projection method**. It enters the
specification verified, not quoted.

K1's worst |z| is 27 with pooled standard errors, which brackets L2's cluster-bootstrapped 13 and L6's
pooled 25. **Carry L2's 13**; it is the conservative one.

---

## 1. THE SPECIFICATION — ten numbered requirements

Any completion that claims to supply the cluster residual must meet **all** of these **simultaneously**.
Each carries a number, a tolerance and the script that established it.

| # | requirement | value | tolerance | established by |
|---|---|---|---|---|
| **R1** | **amount, cluster** | M_X/M_bar = **5.73 ± 0.68** at 0.80 R500 (1000 kpc), universal to 12% across twelve X-COP clusters; 1.06× the cosmic Ω_dm/Ω_b | ±0.68 (12%) | `L7_cosmic_ratio.py`, re-derived as K0 |
| **R2** | **amount under the hydrostatic bias** | the same ratio runs **5.73 → 9.04** over the measured b ∈ [0, 0.33]. Every rescue needs **b < 0**, i.e. σ² < 0 in twelve of twelve clusters | b ∈ [0.00, 0.42] measured | `L18_hse_bias.py` |
| **R3** | **3-D shape, cluster** | ρ_X ~ **r^(−1.5)** over 40–750 kpc, not flat; equivalently a required boost Δ_req = **5.5 s^0.81**, whose log-slope is **4.4σ above the 1/2** that caps every kernel with a deep-MOND limit | 0.09 dex rms about the power law | `g04a` (D2 here) + `L2_cluster_inverse.py` (K1 here) |
| **R4** | **projected shear shape** ⭐new | d ln ΔΣ / d ln R = **−0.851 ± 0.040** over 0.5–2 Mpc. The framework's phantom gives **−0.309**: short by **+0.542, 9σ**, because it is a near-uniform sheet. A source whose density *rises* outward gives ΔΣ < 0 — shear of the **wrong sign** | ±0.06 (9σ) | `L24_lensing_vs_dynamics.py` C11, reproduced as P1 |
| **R5** | **lensing ≡ dynamics** | S_lens − S_dyn = **+0.37 ± 0.24 (1.55σ)**. The source must gravitate identically in both probes, so **no lensing sector can repair a dynamical shortfall** | 1.55σ agreement | `L24` C8 |
| **R6** | **mass-scale, NON-monotone** ⭐new | M_X/M_bar = **30.9 ± 1.5** within 132 kpc of a 1.6e11 M⊙ pair against **5.73** at 1000 kpc of a 6.4e13 M⊙ cluster — a factor **5.4 at 15σ**. Held at *fixed radius* the clusters give **9.20 ± 1.30** at 132 kpc, so the gap is still **3.4× at 11σ** and is not a radius artefact | ±1.6 (16σ) | `L21_binary_galaxies.py` S1, re-derived as K2 and A1 |
| **R7** | **galaxy-scale non-overshoot** | ≤ **0.408 M_b** inside 10 kpc at L\* (M_b = 8e10) and ≤ **0.589 M_b** at a dwarf (M_b = 2e9), from the RAR's own 0.11 dex scatter. An NFW cosmic share gives 0.34 (admissible) and 1.90 (3.2× over) | 0.11 dex RAR scatter | `L21` S6 + `g04k`/`L1` |
| **R8** | **phase-space floor** | Tremaine–Gunn **m ≥ 4.67 eV** at σ = 886 km/s. A relic *at* its floor is cored and fails R3; escaping needs m ≳ 8.3 eV, at which the species carries most of Ω_dm | hard bound | `g04a` R3/R4b |
| **R9** | **cosmological abundance** | Ω_X/Ω_b = 5.43 at cluster scale. If supplied by a *force* rather than mass, BBN caps G_cosmo/G_local at 1.2, against the **9.2** a fixed-strength finite-range force needs (**41×**) and the **1.82** monotone screening forces (**4×**) | \|G/G₀ − 1\| < 0.2 | `L5_long_range_G.py`, `L6_screened_force.py` |
| **R10** | **not a kernel** | no single-valued Δ(s) serves both populations: at the *same* accelerations clusters need **2.2–5.1×** the boost galaxies measure, worst \|z\| = 13. The solenoidal field cannot rescue this: div a_S = 0 makes it **exactly** invisible to the enclosed-mass inversion | 3σ per bin | `L2` (K1 here) + `L22_curl_field.py` |

---

## 2. IS THE SPECIFICATION SELF-CONSISTENT? — **No. V1 FAILS.**

### 2.1 Three ways to serve both anchors, all closed

| check | proposition | result |
|---|---|---|
| **A1** | one radial law R(r) in **absolute radius** serves both | **FAIL.** At the pair's own 132 kpc the clusters measure R = 9.20 ± 1.30; the pairs need 30.9 ± 1.5 — factor **3.4 at 11σ**. The cluster's own R(r) is itself **non-monotone**: 3.9 at 30 kpc → 9.5 at 200 kpc → 5.73 at 1000 kpc |
| **A2** | one law in **scaled radius** r/R200 serves both | **FAIL.** The pair R200 is scanned 250–600 kpc rather than assumed; the gap is **3.8–5.4×** across the whole range, and scaling mostly makes it *worse* |
| **A3** | a component **tracing the baryons** at one universal ratio | **FAIL** at **15σ**. This is the sharpest single consequence of L7 + L21 together: **the cosmic share is a cluster-scale coincidence, not a universal component** |

### 2.2 The search: does *any* single profile serve both scales?

To make "no profile exists" a search result and not a straw man, take the most general **host-blind** rule
mapping a system's baryons to the source,

```
M_X( < r )  =  C · M_bar( < r )^a · (r / 100 kpc)^b
```

which contains every proposal this programme has made — (a,b) = (1,0) is "X traces the baryons",
a = 0 is a universal background halo, a = 1 with b < 0 is a kernel-like boost decaying outward. **The two
anchors fix one line:** `6.0240 a + 2.0227 b = 4.4272`, i.e. `b = 2.189 − 2.978 a`. 35 members were scanned
along it in steps of 0.10 in a, from a = −1.6 to +1.8.

| gate | check | admissible window |
|---|---|---|
| cluster's own measured ratio profile, ≤ 0.15 dex | **B1 PASS** | **a ∈ [+0.40, +0.50]** (best 0.132 dex at a = +0.50) |
| R4 shear log-slope, within 3σ | **B2 PASS** | **a ∈ [+0.60, +0.70]** (closest −0.802 at a = +0.60) |
| R7 galaxy non-overshoot at L\* **and** dwarf | **B3 PASS** | **a ∈ [−1.60, −0.80]** |
| **all three at once** | **B4 FAIL** | **EMPTY** |

**The three windows are pairwise disjoint.** And the galaxy window is worse than merely disjoint: every
member of it has ρ_X *rising* outward, which produces **ΔΣ < 0** — weak-lensing shear of the wrong **sign**,
not merely the wrong slope. The reason is structural and can be read straight off the anchors: to be
5.73 M_bar at 1000 kpc of a cluster and 30.9 M_bar at 132 kpc of a pair, the source must be far flatter
than the baryons at cluster scale (ρ_X ~ r^−0.8 at a = 0), and a flat source projects to a sheet.

### 2.3 THE INCOMPATIBLE PAIR (the theorem)

Along the anchor line the only surviving direction is a **host-mass abundance law**. That exponent is not
free — **the pair sample measures the whole rule internally**, in 3 × 3 cells of its own baryonic mass and
separation, with the same estimator:

```
measured inside the pairs :  alpha = +0.150 ± 0.123 ,  beta = +0.686 ± 0.065   =>   a = +1.150 , b = +0.686
the anchor line requires  :  6.0240 a + 2.0227 b = 4.4272 ;  this (a,b) gives 8.3152
residual                  :  +3.888 ± 0.711 in ln M_X   =>   over-predicts the cluster source by 49x, 5.5 sigma
```

**C2 FAIL, 5.5σ.** The pair population's own internal rule — more source per baryon in more massive hosts,
and more of it at larger radius — points in exactly the direction the cluster anchor forbids. Extrapolated
to a cluster it over-predicts the required source by a factor **49**.

*Honesty note.* The one-dimensional version (C1: mass exponent +0.298 ± 0.113 against the required
−0.280, "opposite sign at 5.1σ") is **partly an r_p–M_b correlation**; controlling for separation drops the
mass exponent to +0.150 ± 0.123, only 1.2σ from zero. **C2's joint residual is the load-bearing number and
it is driven by β**, the radial exponent, which is 10σ from zero. C1 should be read as indicative only.

### 2.4 The one escape the specification leaves open — **stated, not closed**

**B5 FAIL (door open).** For a component at the cosmic share to give the observed pair kinematics, the true
baryon mass inside 132 kpc must be **4.96×** the K-band stellar mass — 6.1e11 M⊙ undetected per pair. Does
the framework's own galaxy-scale gate close that? **It does not**: even spread uniformly inside 132 kpc
(the distribution most favourable to the escape) it puts only **0.0017 M_b inside 10 kpc** against a
tolerance of 0.41. This door is **open on this repository's data**. It is closed, if at all, by
circumgalactic-medium mass budgets — the requirement is roughly four stellar masses of gas inside 130 kpc
of an L\* pair — which is a literature question this lane does **not** settle and does not claim to.

---

## 3. The flagged cored-versus-cuspy disagreement: **NOT REAL** (D3 FAIL)

L24 flagged a genuine-looking internal conflict: Famaey, Pizzuti & Saltas 2024 find the lensing residual
**cored** inside ~1 Mpc, while this repository's `g04a` reports ρ ~ r^(−1.53) and **not** cored.

Tested directly. A cored profile with the outer slope Famaey et al. describe,
ρ(r) = ρ₀ / [1 + (r/r_c)²]^(3.5/2), passed through **g04a's own single-power-law fit over g04a's own
40–750 kpc range**, returns:

| r_c [kpc] | fitted slope over 40–750 kpc |
|---|---|
| **200** | **−1.573** |
| 300 | −1.082 |
| 400 | −0.780 |
| 600 | −0.450 |
| 1000 | −0.197 |

A core radius of **200 kpc reproduces the X-ray-required −1.42 to −1.53 exactly**. The two statements are
**not in conflict**: "ρ ~ r^−1.53 over 40–750 kpc" *is* the mean log-slope of the cored-with-steep-outskirts
shape Famaey et al. report, and g04a's "not cored" is a statement that the fit is not *flat* — which a core
radius comparable to the fitting range does not make it. The disagreement is a **parametrisation artefact**:
two groups fitting different functional forms over different radial ranges to the same shape.

**What survives as a real constraint, and both descriptions agree on it:** the core radius must be
**≲ 750 kpc**, comparable to or smaller than the fitting range. That is enough to exclude a relic sitting at
its Tremaine–Gunn floor, whose core is the whole system (R8 → R3).

---

## 4. Does this constrain ΛCDM? — **NO. E1 FAIL, and it was tested in the direction that would say no.**

A constraint on ΛCDM from this repository would be a major claim, so it was checked adversarially.
ΛCDM's own abundance-matching relation (Moster, Naab & White 2013), evaluated at the pair's measured
baryonic mass with **no fitted parameter**:

```
pair median M_b = 1.55e11 Msun  ->  M200 = 5.63e12 Msun per galaxy, R200 = 367 kpc
NFW puts 0.451 of that inside 132 kpc  ->  predicted M_dark/M_bar = 31.8
measured: 30.9 +/- 1.5      (0.6 sigma)
```

ΛCDM predicts the pair ratio to **0.6σ** with nothing fitted (L21's own forward model independently returns
A = 0.967 ± 0.024, 1.4σ from unity), and reproduces the clusters with nothing fitted either. **The ladder is
non-monotone in ΛCDM by construction:** galaxy-scale halos are baryon-*poor* (the stellar-to-halo-mass
relation), cluster-scale halos are baryon-complete. What L21 measured *is* the stellar-to-halo-mass
relation, which is an **input** to ΛCDM fixed by the galaxy stellar mass function — not a prediction this
measurement tests.

**Nothing in this lane constrains ΛCDM, and no such claim is made.** The non-monotone ladder is a problem
only for a completion that must supply the residual from a **universal component with a single cosmological
abundance** — which is the framework's situation and not ΛCDM's.

---

## 5. THE CHECKLIST — run any future proposal against this

In the spirit of L32's checklist for the coefficient. A proposal must state, for its cluster source:

1. **[R1]** its M_X/M_bar at 0.80 R500 — must be **5.73 ± 0.68**, and universal across clusters to **12%**.
   *Established by* `L7_cosmic_ratio.py` / L41 K0.
2. **[R2]** how it behaves under the hydrostatic bias — the requirement runs **5.73 → 9.04** over
   b ∈ [0, 0.33] and every escape needs b < 0. *Established by* `L18_hse_bias.py`.
3. **[R3]** its 3-D density log-slope over 40–750 kpc — must be **≈ −1.5 ± 0.15**, i.e. not flat, with any
   core radius **≲ 750 kpc**. *Established by* `g04a_cluster_source_phase_space.py` / L41 D2, D3.
4. **[R4]** its **projected** shear log-slope over 0.5–2 Mpc — must be **−0.85 ± 0.06**, and ΔΣ must be
   **positive**. A near-uniform phantom fails here at **9σ** even when its enclosed mass is right; a source
   rising outward fails by sign. *Established by* `L24_lensing_vs_dynamics.py` C11 / L41 P1.
5. **[R5]** that it gravitates identically in lensing and dynamics — the two shortfalls agree at **1.55σ**,
   so a lensing-sector fix is unavailable. *Established by* `L24` C8.
6. **[R6]** its M_X/M_bar at galaxy-pair scale — must be **30.9 ± 1.6** within 132 kpc of a 1.6e11 M⊙ pair
   while remaining **5.73** at cluster scale, i.e. **a factor 5.4 with no universal abundance**, and
   **3.4× at fixed radius**. *Established by* `L21_binary_galaxies.py` S1 / L41 K2, A1.
7. **[R7]** what it puts inside 10 kpc of a galaxy — **≤ 0.408 M_b** at L\*, **≤ 0.589 M_b** at a
   2e9 M⊙ dwarf. *Established by* `L21` S6 / L41 (recomputed).
8. **[R8]** its phase-space density — **m ≥ 4.67 eV** if a fermionic relic, and not sitting at that floor
   (which would core it and fail R3). *Established by* `g04a` R3/R4b.
9. **[R9]** its cosmological abundance — Ω_X/Ω_b = 5.43; if it is a **force** instead of mass, G_cosmo/G_local
   ≤ 1.2 from BBN, against **9.2** for a fixed-strength finite-range force and **≥ 1.82** for any monotone
   screening. *Established by* `L5_long_range_G.py`, `L6_screened_force.py`.
10. **[R10]** that it is not a kernel — no single Δ(s) serves both populations (**2.2–5.1×**, \|z\| = 13),
    and the solenoidal field cannot help (div a_S = 0). *Established by* `L2_cluster_inverse.py`,
    `L22_curl_field.py`.
11. **[R11 — the joint requirement, this lane's own]** it must satisfy R1 **and** R6 with **one** host-blind
    rule. No member of the two-parameter family `M_X = C M_bar^a r^b` does: the three admissible windows are
    **disjoint** (B4), and the rule the pair sample measures internally over-predicts the cluster source by
    **49× at 5.5σ** (C2). A proposal that evades this must introduce a **new free function of host mass** —
    either a host-mass-dependent source abundance, or a host-mass-dependent baryon detection efficiency
    (the pair would need **4.96×** its K-band baryons inside 132 kpc). The second is the stellar-to-halo-mass
    relation under another name, and a completion adopting it **inherits ΛCDM's galaxy-formation sector
    wholesale** — a real cost that should be stated as one. *Established by* `L41_cluster_specification.py`.

**Fast rejection rule.** A proposal whose cluster source is a near-uniform sheet fails **R4** without further
computation. A proposal whose source has a single universal abundance per baryon fails **R6** without further
computation.

---

## 6. Three-sentence verdict

The specification the seven closed lanes collectively define is **not self-consistent**: R1 and R6 alone
demand 5.73 baryonic masses at 1000 kpc of a cluster and 30.9 inside 132 kpc of a pair, which is a factor
**3.4 at 11σ even at fixed radius**, and a 35-member search over the most general host-blind profile rule
closes with three **pairwise disjoint** admissible windows and an **empty** intersection.

**No single radial profile serves both scales**: the rule the pair sample measures internally,
(a, b) = (+1.15, +0.69), over-predicts the cluster source by **49× at 5.5σ**, and every family member that
keeps the source out of a dwarf produces weak-lensing shear of the wrong **sign**.

**This does not constrain ΛCDM** — its abundance-matching relation predicts the pair ratio to 0.6σ with
nothing fitted, because the non-monotone ladder *is* the stellar-to-halo-mass relation — and the one escape
that remains open is a **new free function of host mass**, which a completion may adopt but should
recognise as importing ΛCDM's galaxy-formation sector rather than replacing it.

---

*Two flagged items handed back, not edited here:* (i) L24's cored-versus-cuspy flag is **resolved as a
parametrisation artefact** (§3), not a physical conflict — FINDINGS' L24 entry can be softened by whoever
owns it. (ii) L21's mass-scale trend (M0, "+3.9σ") is **partly an r_p–M_b correlation**; controlled for
separation the mass exponent alone is +0.150 ± 0.123 (§2.3), and the robust internal statement is the
radial exponent β = +0.686 ± 0.065.
