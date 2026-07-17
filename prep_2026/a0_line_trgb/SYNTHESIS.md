# The TRGB Lever on the a0-Line — SYNTHESIS

**Question fired:** does restricting the gas-dominated SPARC a0-line to galaxies with
high-quality (TRGB/Cepheid) distances cut the biggest systematic budget line hard
enough to discriminate the dark-energy footing of a0 — canonical **9.355e-11**
(a0 = cH_Λ/Z = c²·√(Λ/32π), pure-Λ) vs alt **1.1305e-10** (= cH_0/Z)?

**Framework note (its own terms):** modified-INERTIA with a horizon-derived
a0 and its own dS-Unruh interpolation g_obs = √(g_bar² + g_bar·a0). Squaring gives the
exact through-origin identity **E ≡ g_obs² − g_bar² = a0·g_bar**. The gas-dominated
subsample kills ~71% of the M/L degeneracy; the distance flag fD in
`sparc_master_clean.csv` lets us cut σ_lnD 5× (0.25 Hubble-flow → 0.05 TRGB).
Kernel credit: ν = √(1+1/y) is Milgrom 1999 PLA 253:273 Eq. 9; the distinctive content
is the cH_Λ/Z coefficient + the MI completion. SPARC = Lelli-McGaugh-Schombert 2016;
comparison scale g† = 1.2e-10 = McGaugh+2016.

---

## HEADLINE

**The TRGB lever WORKS mechanically but is NON-DIAGNOSTIC of the footing.** It genuinely
tightens the a0-line — the estimator-choice systematic COLLAPSES (median↔GLS agree to
~0.2σ on the clean set) and the distance systematic is cut ~2–3.5× — but the total error
is then floored by the global M/L (Υ) + gas-calibration + ν-shape systematics ABOVE the
2-ban footing-separation target. The clean-distance central **moves UP** to
~1.27–1.35e-10 (Ud=0.7), landing above both anchors, so it leans **mildly against
canonical** rather than detecting it. **Neither footing is confirmed.** Honest verdict:
**TIGHTENS-BUT-NON-DIAGNOSTIC (both footings), UPHELD under adversarial verification.**

---

## OUTCOME

### Does it discriminate the footing? NO.
Footing separation is **≤ 1.3 bans** (log-flat prior) and **< 1 ban** under the
adversarial 15% informed-prior floor — below the 2-ban decisive line on **every** prior
convention. The wall is not the galaxy count: the global floor
√(sysU² + sysG²) = 1.46e-11 (Ud=0.7) **already exceeds** the σ_tot ≤ |Δ|/2 = 9.75e-12
required to split the 20.9%-apart anchors. So **no finite number of TRGB gas dwarfs alone
reaches 2σ** — UNDERPOWERED-BY-FLOOR, not by count (N=18–20 is already ~half the banked
gas sample, point-balanced against Hubble-flow).

### Where does the TRGB-anchored a0 land? (both footings, both Ud)
| Set | Ud | N gal/pts | GLS | median | tot err |
|---|---|---|---|---|---|
| TRGB (fD∈{2,3}) | 0.7 | 18/147 | **1.333e-10** | 1.273e-10 | 12.8% |
| TRGB (fD∈{2,3}) | 0.5 | 20/191 | **1.490e-10** | 1.426e-10 | 12.4% |
| Full gas (banked) | 0.7 | 49/310 | 1.181e-10 | 0.973e-10 | 16.1% |
| Hubble-flow (fD=1) | 0.7 | — | 0.954e-10 | 0.805e-10 | — |

The clean-distance central **does not stay at the banked ~0.97–1.18e-10** — it moves UP
~13% coherently across median + GLS + bootstrap (jackknife max one-galaxy shift <10%;
not one-galaxy-driven; NGC2915 leverage inside the bootstrap band). The banked low
full-gas median (0.973) was largely a **Hubble-flow-distance artifact** (HF median 0.805).

### Occam bans (realized on the ACTUAL reduced-sysD subsample)
Ud=0.7 TRGB: **canonical −0.49 ban** (2.75σ low, mildly disfavored) /
**alt +0.80 ban** (1.28σ low, weakly favored). Separation +1.29 ban → alt.
Ud=0.5 TRGB: canonical −1.88 / alt +0.10. The 1σ band [1.16, 1.50]e-10 sits **above
both anchors**. Realizes-and-CORRECTS the banked "σ/3 → canonical −2.45 ban" forecast:
that arithmetic reproduces exactly but its premise (a 3× TOTAL-error cut) is **not
delivered by distances alone** — distance is not the binding systematic once
gas-dominated.

### Λ-inversion (Λ = 3Z²·a0²/c⁴, Z=5.789, Planck 1.089e-52)
Banked full-gas 1.59× Planck (+1.45σ). Tightened TRGB central 2.03× (GLS) / 1.85×
(median), +2.76σ — **overshoots**, sits FURTHER above Planck, not onto it. Dwarf rotation
still inverts to Λ within a factor ~2 across ~52 a-priori orders — a striking reframing,
but the clean subset pulls above Planck, not toward it. (Canonical a0 inverts to exactly
1.00× by construction; the measured lean is above.)

### Underpowered — honestly, yes, by floor
To become diagnostic you must beat the **global M/L (sysU) + gas-cal (sysG)** systematics
(external Υ priors, deep φ→0 gas-only points) AND grow clean-distance N with points
reaching y~1 — i.e. the **CCHP/EDD TRGB program or BIG-SPARC**. The fD flag alone is a
~2–3.5× sysD win, not the discriminator.

---

## VERIFIER CORRECTIONS APPLIED (all toward more caution, none overturning)

1. **Weight-noise fake-deficit trap** (the one that manufactured a0~3.3e-11 from
   observed-error weights): confirmed present — observed-error weighting collapses a0 to
   0.45–0.63e-10 on every subset — and **correctly avoided**: the pipeline uses
   model-based weights (biased=False, depending on g_bar not on the g_obs noise). Guard holds.
2. **The "central moves up to 1.33" is estimator-weighting-dependent.** A weight-free
   g_bar²-OLS gives **0.89e-10** (near canonical) at Ud=0.7 because per-point a0 = E/g_bar
   **declines with g_bar** (deep tercile ~1.6 → high tercile ~0.6e-10) — ν-SHAPE curvature
   leaking into the magnitude. So the honest central **straddles both footings
   0.89–1.49e-10**; "1.33" is a deep-regime-weighted slope, not a clean single a0, and
   **not a canonical detection either** (g_bar²-weighting is wrong for heteroskedastic E).
3. **TRGB-vs-Hubble-flow gap is distance-scale, NOT a g_bar-segment selection artifact**
   (the two subsamples already share the same g_bar window; range-matching removes zero
   points; y-medians 0.037 vs 0.041 essentially identical). N=18 cannot resolve whether HF
   distances are biased low or nearby-dwarf selection lifts TRGB.
4. **Occam ban signs are prior-convention-fragile** (log-flat −0.49 canon flips to +0.19
   under linear-flat); the robust reported number is the σ-tension (canon −2.75σ, alt
   −1.28σ) and the non-decisive separation (<1.3 bans every convention).
5. Both footings loaded from `anchor_values.json` throughout; frozen `real_research/`
   confirmed READ-ONLY/untouched.

---

## THESIS STATEMENT — "a0-from-rotation = the dark-energy density scale" after this run

The a0-line remains the sharpest single-number route from galaxy rotation to the
dark-energy density scale, and the TRGB lever **strengthens the METHOD** — it collapses
the estimator-choice systematic and cuts the distance budget — without yet strengthening
the **claim**. The clean-distance central sits at ~1.0–1.5e-10 depending on estimator
weighting and M/L (honest box straddling both footings), inverting to Λ within a factor
~2 of Planck across ~52 a-priori orders: a genuine, striking numerical coincidence that a
modified-inertia horizon a0 = cH_Λ/Z would produce, but **not a discrimination** of the
canonical pure-Λ footing from the cH_0/Z alternative. The lever leans mildly AWAY from
canonical, not onto it. The a0 VALUE and the s = −1 sign remain **postulates**; nothing
here derives them. No detection of either footing was manufactured, and no deficit was
manufactured.

---

## NEXT

Diagnosing the footing needs to beat the now-binding **global M/L + gas-cal floor**, not
just distances: (a) external per-galaxy Υ_disk priors (colour-based M/L, or resolved
stellar-pop fits) to shrink sysU; (b) deep φ→0 gas-only points and any TRGB dwarfs
reaching y~1 to break the magnitude/ν-shape degeneracy the verifier exposed; (c) the
**CCHP/EDD TRGB program** and **BIG-SPARC** to grow clean-distance N. The distance flag
has been spent — it is a ~2–3.5× sysD win, confirmed, and no longer the limiting line.
