# NET SIGN — Cluster-Member EFE σ-Spread, per Infall Zone

**Lane:** net-sign. **Script:** `net_sign.py` (exit 0, `net_sign.out`). **Both footings**
(a₀ = 9.36e-11 canonical cH_Λ/Z, 1.13e-10 alt cH₀/Z). Real framework kernel + real infall
orbit integrated in the dressed cluster field, framework MODE-II exponential memory operator
(mi_integrator SPEC form) at all three committed corners. **No "proves." s=−1 postulate flagged.**

---

## The contradiction we were asked to reconcile

- **GAP_STATEMENT.md E4/E7** (`prep_2026/sigma_spread/`): sign **NEGATIVE** ("plungers less
  boosted"); E7's kill-condition falsifies the framework on a **positive** sign.
- **predict.py** (`prep_2026/cluster_efe_channel/`): **POSITIVE** baseline ("plungers HOTTER")
  **plus** a dated pericentre **sign-flip** — first-infall DEFICIT / post-peri EXCESS (the D3
  pre-registration, DOI 10.5281/zenodo.21179352).

## Root cause (not a numeric clash — a field-vs-y labelling error + an imported timescale)

All banked calcs share the same boost B = 1/μ_fw(A/a₀), A = a_in + a_ex·θ(y), θ **decreasing**.
Run it and σ **rises** from settled to plunger: **more external loading → more Newtonian →
lower MOND boost → cooler; shedding loading → hotter.**

1. **GAP E4/E7's "NEGATIVE / plungers less boosted" is a TEXT-LABEL BUG.** Low θ (high y) =
   *less* external loading = *less* suppression = **more** boost. E7's kill-condition ("positive
   sign falsifies") is **backwards** and self-trips the framework's own correct prediction — this
   is exactly the verify lane's "weak-memory population self-trips E7." **Do not pre-register E7
   as written.**
2. **predict.py's BASELINE ("plungers HOTTER") is CORRECT** and is the banked calc that was right
   on sign.
3. **predict.py/D3's pericentre flip DIRECTION is INVERTED.** It encoded "cold isolated past" as
   y_hist ≈ 0.1 (**low** y) — but θ(y≈0) ≈ 2 is **MAXIMAL** loading. Isolation is **a_ex → 0**
   (zero loading for any θ), *not* low-y. Worked correctly in **field space**, first-infall
   (rising field, felt < now) is the **HOTTEST / largest-excess** zone; the just-past-pericentre
   member is the **cool** side — the exact inverse of predict/D3.

## Separation: shared boost vs the MG-impossible piece

- **Instantaneous θ(y_cur) boost = the banked 6–13%** (reproduced: **9.5%** fiducial both
  footings). This is the *current-configuration* EFE — **partly SHARED** (MG has an instantaneous
  EFE too). **Not** the discriminant.
- **MG-impossible piece = the HISTORY spread at FIXED current field a_ex(now).** Two members at
  the same a_ex(now) but different infall history differ **only in MI**, because MI's felt loading
  is a memory-weighted functional of the a_ex history; MG's is instantaneous. `sympy`:
  d(σ_MG)/d(history) ≡ 0 for any a₀, any interpolation. **This is the sole theorem-grade claim.**

## The per-zone net sign (real kernel + real orbit, at matched a_ex(now) = 0.5 a₀)

The per-zone sign is **reference-dependent** — the deep root of the banked disagreement. Reported
against **both** anchors.

| anchor | meaning |
|---|---|
| **THEOREM** | vs the MG prediction σ(a_now). Every under-loaded member (felt<a_now) is *hotter than MG*; the ~14–15% common offset is **UNOBSERVABLE** (degenerate with baryonic M/L) → the **spread** is the signal. |
| **OBSERVABLE** | vs the sample-mean felt (the FJ baseline an observer fits). first-infall = hot tail, long-settled = cool tail. |

**Deviation vs the observable sample mean (%), (felt/a₀), canonical footing:**

| memory corner | first-infall | recent post-peri | backsplash re-approach | ancient/settled |
|---|---|---|---|---|
| **E10 gap 2c/a₀ = 203 Gyr** *(committed)* | **+0.81** (0.032) | −0.04 (0.048) | −0.27 (0.052) | −0.47 (0.056) |
| H_Λ = 17.5 Gyr *(stable)* | **+5.97** (0.056) | −0.87 (0.222) | −1.61 (0.247) | −1.88 (0.256) |
| dwarf-v3 Lorentz = 0.45 Gyr *(predict.py; unstable band)* | **+3.15** (0.410) | −4.54 (1.003) | +2.66 (0.433) | +1.41 (0.500) |

(Alt footing is materially identical; see `net_sign.out`.)

**Robust across BOTH footings and ALL corners:** first-infall pre-peri is the **HOTTEST** zone
(largest excess) and sits **above** recent post-peri — inverting predict.py/D3's ordering at the
source. The signal is essentially **MONOTONE in accumulated loading (~ time-since-infall)**, not a
sharp dated pericentre flip. The *cool-tail identity is itself timescale-dependent*: long memory
(E10/H_Λ) → ancient/settled coolest; short memory → recent-post-peri coolest (it retains the
just-passed pericentre loading).

## Resolving the raw-loading(+) vs memory(−) "competition"

It is a **field-vs-y artifact, not a real competition.** In field space both branches agree:
a member whose felt field is below current is hotter (first-infall felt 0.12 a₀ < now 0.50 a₀ →
**+10.7%**, hotter). The spurious "memory(−)" branch comes from the y-space bug — encoding the cold
past as low-y (θ≈2, maximal loading) gives a false **−4.9%**. Fixing the encoding removes the
competition; the net sign is set unambiguously by sign(a_ex,felt − a_ex,now).

## Timescale pin (framework-first)

Two corpus memories disagree ~450×:
- **E10 covariant horizon memory τ_mem = 2c/a₀ = 2Z/H_Λ = 203 Gyr (can) / 168 Gyr (alt)**;
  footing-free τ·H_Λ = 2Z = 11.58. This is what the **19/19-verified MI integrator**
  (`prep_2026/mi_integrator/`) actually integrates, and one of its two **stable** corners; the
  integrator found the **orbital-band 0.45 Gyr corner SECULARLY UNSTABLE**. Framework-first ⇒ the
  committed memory is the **slow horizon memory**.
- **dwarf-v3 Lorentzian 0.45 Gyr** (predict.py/D3) — not anchored to E10, in the unstable band.

τ_mem(E10) ≫ crossing/residence (~1–6 Gyr) ⇒ **DEEP ADIABATIC**: felt loading is a ~200-Gyr
average dominated by the near-zero pre-infall past ⇒ the observable per-zone spread is
**RESIDENCE-limited (< ~1.5%, both footings)** and the sharp pericentre feature **FREEZES OUT**.
predict.py's 0.45 Gyr is the *only* thing making the flip a resolvable (~7–8%) sub-orbit transient
— exactly the correction `mi_spread.py` already made for the star-orbit observable (6–13% →
sub-%). **E13 |K|=1 pure-phase caveat:** a one-time ramp is felt with gain ~1 and a group delay
(not a hard freeze). The pure-delay test confirms the **sign is unchanged** (under-loaded = hotter,
first-infall +); only the **magnitude / transient-survival** is timescale-hostage.

## Magnitude vs the 6–13% shared boost

| | shared θ(y_cur) boost | MG-impossible history span (E10 / H_Λ / 0.45 Gyr) |
|---|---|---|
| canonical | 9.5% | **1.3% / 7.9% / 7.7%** |
| alt | 9.5% | **1.5% / 8.4% / 8.4%** |

The MG-impossible history span is comparable to the shared boost **only** for the short (unstable)
corner and **collapses to ~1–1.5%** for the committed E10 horizon memory.

## Which banked calc was right

- **predict.py baseline — CORRECT** on sign (under-loaded = hotter).
- **GAP E4/E7 — TEXT-LABEL BUG**, negative/kill-condition backwards; **must be fixed before
  pre-registration** (E7 currently self-trips the framework's own correct prediction).
- **predict.py/D3 pericentre flip — INVERTED** (y-space encoding of isolation); and, framework-first,
  **largely frozen out** by the committed E10 memory.

## Verdict — OUTCOME (B)

The sign is **ROBUST ONLY in the first-infall pre-pericentre zone** (POSITIVE / hotter / largest
excess). **Pin the pre-registration there**: the pre-registrable correlation is *σ-excess DECREASES
with accumulated loading / time-since-infall*. The full **dated pericentre sign-flip CANNOT be
pre-registered** as a clean prediction (timescale-hostage + was backwards in the banked calc). The
**existence** of the fixed-field history spread **is** pre-registrable (MG-impossible). **MG = 0 at
fixed true field is the sole theorem-grade claim, regardless of the sign.**

**Caveats:** the sign is **conditional on the s=−1 postulate** (s=+1 flips it). MI-class-generic
(MI-vs-MG), **not** this-framework-vs-Milgrom. a₀ value + s=−1 remain postulates. Magnitude is
kernel-hostage; only sign + existence + MG=0 are load-bearing.
*Credit: Milgrom 1983 (MOND) / 1999 PLA 253:273 (ν-kernel wellhead) / 2022 PRD 106 064060 (MI, EFE).*
