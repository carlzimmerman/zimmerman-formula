# PRE-REGISTRATION (D2): The Cluster y_c Kink as an EXACT NULL — Statement of Record for Euclid-Era Cluster Lensing

**Filed:** 2026-07-16 (prep_2026, Door 2 of the four-door synthesis; second named pre-December action)
**Status:** NULL-STATEMENT pre-registration. This is **not a detection promise.** The kink was
honestly **RETIRED as a detection target** on 2026-07-16 (see `TARGET_SPEC.md` in this
directory): on realistic cluster baryon profiles it sits at r ≈ 8–23 kpc, inside the BCG,
10–50× below any usable weak-lensing radius, with an amplitude 2.3–3.5× below the banked
0.06 dex systematics floor. What survives — and what this document pins in advance — is the
**sharp, pre-declared null/detection fork**: the framework's falsifiable statement of record
for stacked cluster lensing in the Euclid era.

Nothing here uses "proves" or "validates." Every load-bearing number below is printed by the
committed, exit-0 scripts hashed in §8. Both a₀ footings are carried throughout.

---

## 1. The three doors and what each one predicts

| Door | Mechanism | Kink at g_bar = y_c·a₀? | Why |
|---|---|---|---|
| **Branch B** (elastic dark-energy medium WITH the entropy-budget throttle) | Verlinde-class elastic response, cutoff y_c = Z/2 | **YES** — slope discontinuity in the lensing RAR at g_bar = y_c·a₀, i.e. at r_kink ≈ 8–23 kpc; bipolar ±2–3 % feature in Σ(R) confined to R < r_kink; **exactly zero** signal at R > r_kink | The medium's response is depleted as (y_c/y)ⁿ above the budget crossover; below it, throttled = uncut exactly (T = 1) |
| **Pure MI** (Branch A, modified inertia, no medium) | dS-Unruh inertia modification only; g_obs = g_bar·ν(y), ν = √(1+1/y) | **NO — EXACTLY no kink, anywhere, at any radius or acceleration.** There is no y_c scale in pure MI at all | y_c = Z/2 exists only as a property of the medium's entropy budget; with no medium there is nothing to throttle. This is the EXACT NULL of record |
| **ΛCDM** | NFW halo + baryons | **NO kink — but for a different reason** | NFW+BCG profiles are smooth in g_bar; ΛCDM has no fixed-acceleration scale at 2.7×10⁻¹⁰ m/s². Its no-kink prediction is generic smoothness, not an exact cancellation |

**Honest degeneracy, stated up front: a null on the kink does NOT distinguish pure MI from
ΛCDM.** Both predict no kink. The kink observable discriminates **Branch B against everything
else** — that is all it does, and that is what is pre-registered.

A second honesty rail: pure MI passing the no-kink test does **not** vindicate pure MI's
cluster story overall. Pure MI under-predicts cluster lensing on a single metric and concedes
a genuine dark component (Branch A's standing concession; central deficit η(R500) ~ 1.0–1.3,
shared with all MOND-class laws). The exact null is a statement about the *absence of a
y_c feature*, not about cluster mass budgets.

---

## 2. The observable (pre-declared, exactly)

**Primary observable:** the logarithmic derivative of the stacked cluster lensing profile,

  O(R) ≡ d ln Σ(R) / d ln R  (strong-lensing convergence maps, κ = Σ/Σ_cr)
  O'(R) ≡ d ln ΔΣ(R) / d ln R  (stacked weak-lensing excess surface density)

binned at ≤ 0.1 dex in R, stacked in bins of cluster mass proxy (richness/M500) and lens
redshift. A "kink" = a discontinuity in O(R) localized at the radius where the *baryonic*
acceleration crosses g_bar = y_c·a₀, coherent across mass bins **in acceleration, not in
radius** (the acceleration locus is the primary pin; the radius is baryon-model dependent).

**Equivalent RAR-space observable:** the slope d log g_obs / d log g_bar of the cluster
lensing RAR across g_bar = y_c·a₀.

---

## 3. The exact predicted signature (Branch B), per footing

Provenance of the cutoff: **y_c = Z/2 = 2.894405** (Z = √(32π/3) = 5.788810; dimensionless,
**footing-free**), derived from Verlinde's own entropy budget taken *verbatim from the
published version of record* — **SciPost Phys. 2, 016 (2017), eqs. (28)–(34)**: matter
entropy displacement S_M = −2πMcr/ħ (eq. 28), dark-energy volume-law entropy
S_DE = (r/L)A/4Għ (eq. 29), strain–budget identification ε_M = (8πG/a_0V)Σ_M
(eqs. 32–34), giving ε_M = 2 g_bar/a_0V exactly, so the crossover sits at g_bar = a_0V/2,
i.e. y_c = Z/2 on the program's horizon reading a_0V = cH_Λ = Z·a₀. The competing O(1)
reading y_c = Z/3 is excluded by Verlinde's own eq. (41). Full derivation + three-rendering
source verification: `zimmerman-formula/real_research/papers/ELASTIC_MEDIUM_YC_Z2_2026.md`
(committed, DOI-backed; repo frozen — cited read-only).

| Quantity | Canonical footing (a₀ = 9.36×10⁻¹¹ = cH_Λ/Z, pure-Λ) | Alt footing (a₀ = 1.13×10⁻¹⁰, ρ_total/cH₀) |
|---|---|---|
| Kink locus in acceleration | **g_bar = 2.7092×10⁻¹⁰ m/s²** | **g_bar = 3.2707×10⁻¹⁰ m/s²** |
| r_kink, fiducial clusters (M500 = 1–15×10¹⁴ M☉) | 9.5–11.2 kpc | 8.0–9.2 kpc |
| r_kink, all variants (cool-core, 2×BCG) | **9.5–22.7 kpc** | **8.0–19.1 kpc** |

The footing fork moves r_kink by only ~15 %; **both footings land the kink inside the BCG**
(96–100 % of M_bar at r_kink is BCG stars). The fork is carried but is not decision-relevant
for this observable.

**Footing-independent amplitude** (throttle index n = 1 minimal / n = 2 bracket):

- Peak RAR deviation: **0.0170 dex at y = 6.13** (n=1); **0.0260 dex at y = 5.24** (n=2).
- RAR slope discontinuity at y_c: d log g_obs/d log g_bar drops from 0.8715 to
  **0.7341 (n=1) / 0.5968 (n=2)** — a break of **−0.138 / −0.275**.
- Projected signature in Σ(R) (full Abel projection, fiducial clusters): **bipolar**,
  +2.6–2.9 % Σ deficit inside R ≈ 5–6 kpc, −1.4–3.1 % Σ excess just inside r_kink,
  **exactly zero at R > r_kink** (< 0.001 % at 2 r_kink — mass redistribution, net zero).
- **ΔΣ(R) at R > r_kink carries NO signal at all.** This is exact, not approximate: the
  throttled and uncut laws share the same effective enclosed mass at r_kink and are
  identical outside it.

Everything above y_c exists **only inside r_kink**; outside, Branch B throttled = uncut
framework law exactly (T = 1). All numbers re-verified by independent machinery
(`adversarial_recheck_d2.py`, scipy quad/brentq + closed forms, exit 0).

---

## 4. Pre-declared decision rules

**Rule D (detection).** A slope discontinuity in O(R) detected at ≥5σ, localized at
g_bar = y_c·a₀ within either footing's locus (±15 %, the footing spread), with break
magnitude in the band −0.10 to −0.30 and the bipolar Σ signature (interior deficit + excess
lobe, zero exterior signal), coherent in *acceleration* across ≥2 independent mass bins:
→ **Branch B supported at the detected significance; pure MI's exact null VIOLATED**
(the no-medium branch is then wrong about cluster lensing structure, independent of its
galaxy-scale standing); **ΛCDM strained** (NFW has no fixed-acceleration feature; an NFW
mimic would have to conspire in radius differently at every mass to hold one acceleration).
Detection does not "prove" the medium — it supports the throttle signature specifically.

**Rule N (null).** No kink at per-bin Σ sensitivity p over the pre-declared window
(0.1–1.5 r_kink, 0.1-dex bins, 11 bins) with g_bar known to ≤0.01 dex:
→ **Branch B's throttle constrained at S/N_excl = √(Σᵢfᵢ²)/p**, where √(Σᵢfᵢ²) = 5.1–7.4 %
(template norms, M500 = 1–15×10¹⁴ M☉). Concretely: p ≤ 1.7–2.5 %/bin excludes the n=1
throttle at ≥3σ; p ≤ 1.0–1.5 %/bin at ≥5σ. **Pure MI passes** — trivially, since it
predicted nothing. **The null does NOT distinguish pure MI from ΛCDM** (both predicted no
kink); it only removes Branch B's throttle at the stated significance. Both conditions
(statistical p AND the 0.01-dex g_bar prior) must hold or the "null" is vacuous — see §6.

**Rule A (anomaly).** A sharp break detected at a g_bar locus *outside both footing bands*:
→ anomalous for **all three doors**; no door claims it; treated as a systematics candidate
first (M/L gradient, miscentering, selection), new physics second.

**Confounder pin (pre-declared):** a *constant* BCG M/L error shifts the apparent kink
radius by Δlog r = Δlog Υ/2 but cannot erase or create a slope discontinuity; only radial
M/L *gradients* (observed at 0.05–0.2 dex in massive ETG cores) can mimic or mask smooth
curvature. A claimed detection must therefore show the break survives marginalization over
an M/L gradient nuisance; a claimed null must show sensitivity to a break *after* that
marginalization.

---

## 5. Euclid data products this fork runs on

| Product | Content | Citation |
|---|---|---|
| Euclid Wide Survey | ~14 000 deg², WL source density requirement 30 arcmin⁻² | Euclid Collaboration: Scaramella et al. 2022, A&A 662, A112 (arXiv:2108.01201) |
| Cluster detections (AMICO + PZWav workflow) | Forecast ~2×10⁵ clusters to z = 2 (conservative threshold); Q1 demonstration: 426 joint high-S/N clusters in 63 deg², 0.2 ≤ z ≤ 1.5 | Sartoris et al. 2016, MNRAS 459, 1764; Euclid Collaboration: Adam et al. 2019, A&A 627, A23 (Euclid prep. III); Euclid Q1 XXXIV (A&A 2026, aa54937-25) |
| LensMC shear catalogue for cluster lensing | Q1: 75 arcmin⁻² raw (I_E < 27) / 26 arcmin⁻² (I_E < 24.5) over 63 deg²; cluster profiles constrained for 10¹⁴ M☉ to z ≈ 2 | Euclid Q1 LensMC cluster-lensing catalogue (arXiv:2606.20829) |
| COMB-CL WL cluster masses | Euclid will measure WL masses of ~13 000 (shot noise only) / ~3 000 (shape+LSS noise) clusters at S/N > 3 | Euclid Collaboration: Sereno et al. 2024, A&A (Euclid prep. XLII; arXiv:2404.08036) |
| WL mass accuracy/precision baseline | Shear-profile mass fits over **[0.4, 4.0] Mpc**; cluster core R < 100 kpc explicitly excluded; only ~3.7 % of M200c > 5×10¹³ M☉ clusters reach individual S/N_WL > 3 | Euclid Collaboration 2025, A&A (Euclid prep. LXV; aa52122-24); systematics-control baseline: Köhlinger, Hoekstra & Eriksen 2015, MNRAS 453, 3107 |
| Release timeline | DR1-Foundation ~1 900 deg² (Nov 2026); full DR1 higher-level WL products mid-2027 | ESA Cosmos Euclid DR1 timeline |

**The decisive geometry:** Euclid's own cluster WL fits start at **R = 0.4 Mpc** (prep. LXV),
with the core inside 100 kpc excluded even in idealized tests. r_kink = 8–23 kpc sits
**17–50× below the Euclid fit floor** and 4–12× below even the most aggressive stacked-WL
inner radii used in any survey (~100–200 kpc; miscentering, BCG light, member contamination,
blending). And Branch B's signal at R > r_kink is **identically zero** (§3).

---

## 6. Is the decision live at Euclid depth? Straight answer: NO — and not by lack of stacking

**No stacking depth makes the Euclid WL channel live.** This is not the usual "underpowered,
collect more clusters" situation: the Branch-B signal in ΔΣ at every radius Euclid measures
(R ≥ 0.4 Mpc, and even a hypothetical 0.1 Mpc floor) is **exactly zero**, so the
discriminating power is 0σ at N_cl = 426 (Q1), at 2×10⁵ (full Wide forecast), and at any N.
At those radii the throttled and uncut framework laws agree identically (y ≤ 0.3 ≪ y_c at
200 kpc across all models — clusters never reach the y_c locus outside their BCGs), and both
are smooth. **Stacked Euclid WL cluster profiles test nothing about the throttle, in either
direction, at any depth.** What Euclid WL *will* provide is the consistency-null side of the
record: smooth stacked profiles with no feature at any fixed g_bar locus, which all three
doors co-predict.

**Illustrative fantasy bound (pre-computed, assumptions stated):** even granting a WL survey
that could measure shear in 0.1-dex bins at R = 10 kpc with Euclid's 30 arcmin⁻² source
density (z_l = 0.3, D_A = 919 Mpc → 267 kpc/arcmin; 0.002 arcmin²/bin → 0.06 usable
galaxies per cluster per bin; σ_ε = 0.26; κ ≈ 0.3 there), the 5σ statistical bar
(p = 1.0–1.5 %/bin) would need **~5×10⁴–1.2×10⁵ stacked clusters** — a quarter to over half
of the entire conservative Euclid catalogue — *before* confronting the fact that at 10 kpc
the regime is strong lensing, the BCG's own light dominates the pixels, and shear
measurement is not possible there at all. The WL route is closed structurally, not
statistically.

**The only live-able channel** (carried from `TARGET_SPEC.md`, unchanged): strong lensing +
BCG kinematics at 1–15 kpc (HST/JWST-resolved; angular scale 0.25–3″ at z = 0.2–0.4 — 
resolution is not the obstacle). The statistical bar is modest — **~12–24 well-modeled
clusters at 5 %/bin Σ precision reach 5σ** on the template. The blocker is the g_bar prior:
at r_kink the mass is 96–100 % BCG stars, and the stellar-M/L (IMF) systematic in massive
early-type cores is ~0.1 dex — **4–6× the entire signal** (and the banked 0.06 dex known
systematics floor is itself 2.3–3.5× the signal). Existing cluster-RAR data never reaches
the regime at all: the banked Tian+2020 CLASH stack tops out at g_bar = 2.1×10⁻¹⁰, i.e.
y_max = 2.24 < y_c (innermost radius 14 kpc ≳ r_kink).

**Liveness condition (pre-declared):** the fork becomes decidable if and only if
(i) Σ(R) maps at 1–15 kpc on ≥12–24 well-modeled clusters at ≤5 %/bin, **and**
(ii) external, spatially resolved, IMF-sensitive BCG M/L priors at **0.005–0.01 dex** at
r < 15 kpc. Condition (ii) is beyond any current or funded program. Until both hold, a
reported "null" is vacuous under Rule N and must not be claimed as a Branch-B kill; a
reported "detection" fails the confounder pin of §4.

---

## 7. What this pre-registration retires, and what it keeps

- **Retired:** the kink as a detection target for wide-survey lensing. The committed
  Gemini mock (`zimmerman-formula/real_research/reviews/open_doors_2026_07/
  cluster_throttle_lensing_mock.py`, read-only, repo frozen) placed r_kink ≈ 150 kpc by
  compressing 10¹⁴ M☉ of baryons into a 50 kpc Hernquist — the entire baryon budget of an
  M500 ≈ 10¹⁵ cluster at BCG scales — and used a₀ = 1.2×10⁻¹⁰ (neither footing) with the
  standard-MOND simple ν, not the framework's ν = √(1+1/y). The realistic re-computation
  (this directory) moves the kink to 8–23 kpc and its committed script reproduces the
  mock's 150.3 kpc exactly as a contrast case. The mock's closing claim ("the exact spatial
  signature that Euclid … should target") is **withdrawn** by this pre-registration.
- **Kept:** the fork itself, sharpened. Branch B's kink is now a *located, pinned,
  pre-registered* signature (acceleration locus, amplitude band, slope break, bipolar
  Σ template, exterior exact zero — per footing), and pure MI's **exact no-kink null** is
  the framework's falsifiable statement of record for Euclid-era cluster lensing. If anyone
  ever reports a cluster-lensing break at g_bar ≈ 2.7–3.3×10⁻¹⁰ m/s², the ledger of what
  each door predicted — written before any such data existed — is this document.

---

## 8. Reproducibility and integrity

Committed, runnable, exit-0 scripts (this directory; re-run 2026-07-16 before filing):

```
SHA-256 (kink_target_spec.py)      = 71cafc17a0a4eb5a4f18855670dc7d6ef743e2b8d7165cd380c3ecc1a67ed338
SHA-256 (adversarial_recheck_d2.py) = e682cd612b49a30404c40aebc6954d12cd8acb4135b89111f80b1c9085366bd4
SHA-256 (run_output.txt)            = 013541778a17ab126ae48d2a40e82657f53cfe932c4d01bcc43308f851d764a7
SHA-256 (TARGET_SPEC.md)            = 96f19c52410cc391412d587a518add82a231a4806dd0e6ae336ecee16af445d8
```

- `kink_target_spec.py` — gates re-verify y_c = Z/2, both kink accelerations, the banked
  0.017 dex @ y≈6 fingerprint, the n=2 bracket, the Gemini-mock reproduction, finiteness +
  interiority of every r_kink, and the bipolar projection with exterior agreement; **no
  detectability is asserted anywhere in the script.**
- `adversarial_recheck_d2.py` — independent machinery (quad/brentq/closed forms) re-derives
  r_kink, the amplitude, the slope break, the Σ lobes, and the Tian y_max < y_c
  confrontation.
- Banked upstream inputs (frozen repo, read-only): `real_research/papers/
  ELASTIC_MEDIUM_YC_Z2_2026.md` (y_c = Z/2 from SciPost Phys. 2, 016 (2017) eqs. (28)–(34);
  eq. (41) closes the Z/3 alternative), `real_research/reviews/cluster_rar_throttle_2026/
  lane1_predict.py` (throttle + fingerprint), `real_research/reviews/open_doors_2026_07/
  cluster_throttle_lensing_mock.py` (the corrected mock).

*Frozen-repo rule honored: nothing inside `zimmerman-formula/` was modified. The Gaia DR4
freeze (first pre-December action) lives in `prep_2026/gaia_dr4_prep/` and was not touched.*

---

## 9. Honesty rails (standing, restated)

1. Both a₀ footings carried at every step; the footing fork (~15 % in r_kink) is shown and
   is not decision-relevant here.
2. No "proves/validates" anywhere; Rule D says *supported*, Rule N says *constrained/killed
   at stated significance*.
3. The ΛCDM degeneracy of the null is stated in §1 and inside Rule N itself: a null does
   not distinguish pure MI from ΛCDM.
4. The detection framing is retired in plain language (§7); this is a null-statement
   pre-registration, not a detection promise.
5. Pure MI's exact null passing does not resolve Branch A's standing cluster-lensing
   concession (η(R500) ~ 1.0–1.3, MOND-shared).
6. y_c = Z/2 is derived from Verlinde's published coefficients; the throttle *form*
   T = min(1,(y_c/y)ⁿ) is the program's own construction; Branch B is priced, not adopted.
