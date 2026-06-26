# WEIRDNESS LEDGER — frontier-curiosity ranking (EXPLORATION mode)

**Date:** 2026-06-25
**Mode:** EXPLORATION (Carl's ask: stop high-priesting ΛCDM, hunt "that's weird" leads as *directions to chase*, not
verdicts to kill). The FDR/surprise score here is a **ranking label** (more surprising × simpler × more cross-domain =
more interesting), NOT a kill switch. Both-ways the whole time: surface generously, label honestly.

**Framework anchor:** a₀ = c²√(Λ/32π) = cH_Λ/Z, Z = √(32π/3) — a real dS-Unruh modified-inertia MOND result. The
gravity side is a provably one-parameter EFT; the SM bridge is corpus-walled. The hunt below is for *new attack axes*,
not new claims of derivation.

All numeric claims sympy/mpmath dps≥40, reproduced this session. Scripts in `/tmp/wl_*.py`.

---

## THE RANKED FRONTIER (by "hmm that's weird" = surprise × simplicity × cross-domain-reach)

| rank | lead | label | weirdness | coincidence-odds | one-line |
|---|---|---|---|---|---|
| **1** | **Koide r=√2 = irrep-CHANNEL equipartition** (not STATE) | structural-resonance | **HIGH** | reframing of a ~1-in-69,000 angle | The open knob "why r=√2" becomes the precise choice **per-irrep measure vs per-state measure**, and the framework's own documented overshoot (r=2→Q=1) is *exactly* the standard per-state answer. ONE factor (the doublet dim 2) separates them. |
| **2** | **a₀_norm⁴·π = δ_Maj² = sin²θ_W,tree = 3/8** | structural-resonance | MEDIUM | ~1-in-100 | Three nominally-disjoint constructions land on the identical rational 3/8; the only cross-sector gap is *exactly one Einstein-measure π* — the canonical shape of an algebra→horizon (Unruh T=a/2π) map. |
| **3** | **sin²θ_W,tree = 3/8 as a forced trace identity** | structural-resonance | MEDIUM | structural (odds N/A) | The gauge sector has its OWN pre-fit forced geometric rational, parallel to gravity's √(8π/3); but minimal-SM running misses the measured 0.231 (known near-miss, a re-find). |
| **4** | **Singh gauge-3/8 and EJA-mass-3/8 share J₃(O)** | structural-resonance | MEDIUM | ~1-in-2000 if separate | Two of the three 3/8's may be one octonionic trace appearing twice (inference, not stated by Singh). |
| **5** | **Z² = 32π/3 = 8·(4π/3) = 8·V_ball(d=3)** | near-miss / null | LOW | not surprising | The gravity constant is "8 × unit 3-ball"; the 3 and 8 recur across sectors but for *different* reasons each time. Direct exceptional-group hunt = EMPTY (no E6/E7/E8/F4 dim within 1% of Z²). |
| **6** | **g = √(2/Z) = (3/8π)^(1/4) lands in cos θ_W ≈ (3/2)g** | simple-coincidence | LOW | density-baked (~1-in-3) | Value-echo of g in EW observables; the depth-3 reachable set tiles [0.5,0.6] densely → expected ≥1 chance hit. |

**Why this ranking:** Lead 1 targets a genuinely rare angle (Koide Q=2/3 is a ~1-in-69,000 random-triple event,
*re-measured this session*) and reframes the unforced knob into a sharp, physical, **new** question the corpus's six
banked Koide attacks never isolated (state-vs-channel counting). Leads 2–4 are medium-surprise rational collisions
(3/8 has pool-density ~1.5%, so a 3-way same-rational hit is ~1-in-100 — real but not Koide-class). Leads 5–6 are
LOW/null: the small integers recur as dimension-counts (not group dynamics), and the value-echoes are density-baked
(EXHAUSTION_THEOREM: the flavor rationals densely tile [0.5,0.6], so a landing there carries ~zero surprise).

---

## DEEP-EXPLORE #1 (the top pick) — Koide as irrep-CHANNEL equipartition

**The sympy-exact reframing** (`/tmp/wl_lead2_equipartition.py`). Brannen circulant √m_k = M(1 + r·cos(φ+2πk/3))
gives Q = 1/3 + r²/6 (φ cancels). Decompose the √-mass 3-vector under the Z₃/S₃ structure into the **singlet** (the
(1,1,1) democratic direction) and the **2-dim doublet**:

```
|singlet|² = 3M²            |doublet|² = 3M²·r²/2
|singlet|² = |doublet|²   ⟺   r = √2   ⟺   Q = 2/3   (EXACT, Koide)
```

So **Koide is exactly "equal power in the singlet CHANNEL and the doublet CHANNEL."** Contrast the two natural measures
(`/tmp/wl_lead2_pushhard.py`, `/tmp/wl_hiT_check.py`):

- **STATE / dimension equipartition** (equal power per real dimension — the standard equipartition-theorem / Plancherel
  measure, which weights an irrep by its dimension): |sing|² = ½|doublet|² ⟹ **r = 2 ⟹ Q = 1**. This is the framework's
  *documented overshoot wall*, now identified as the physically-standard answer.
- **CHANNEL equipartition** (one unit per irrep, the character / class-function measure): ⟹ **r = √2 ⟹ Q = 2/3** (Koide).

**The whole gap is one forced integer:** r²_state/r²_channel = 2 = dim(doublet); Q_state − Q_channel = 1/3 = the
democratic floor. The framework's thermal bath counts the wrong thing by **one structural step** (3 dimensions vs 2
channels), NOT by 36 orders of magnitude.

**Is there a thread? — YES, but it is a sharper wall, not an opening (both-ways, decisive).**
1. **The framework's OWN dS-Unruh bath gives the OVERSHOOT.** A thermal bath sums over Bose *states*; the equipartition
   theorem allots (½)kT per quadratic DOF = **per state = per dimension = Plancherel = r=2 = Q=1**. Used honestly, the
   framework's natural home reproduces the banked overshoot, not Koide.
2. **The "high-T = channel limit" shortcut is a SMUGGLE** (caught this session, `/tmp/wl_hiT_check.py`). High temperature
   equalizes per-state Boltzmann weights — exp(−C₂/T)→1 for every mode — which gives doublet:singlet = 2:1 = the r=2
   overshoot, NOT the channel limit. Channel-equipartition has to be imposed at the level of *what is summed* (irreps vs
   states); nothing thermal forces it. So there is no free thermal route to Koide.
3. **Cross-fermion wall STANDS** (re-measured: Q_lep=0.6667, Q_up=0.849, Q_down=0.731). Quarks share the S₃ permutation
   rep, so any channel-equipartition principle forces Q=2/3 for them too — they aren't. A channel measure must
   *additionally* be lepton-selective, and **uniform color (N_c=3) cancels in Q** (corpus, re-confirmed) → color is not
   the selector. The selector remains unidentified.

**Honest verdict on the thread:** This is a genuinely NEW, sympy-exact *formulation* of the open knob — outside the six
declared-exhausted Koide axes — that pins the wall to **one un-smuggled question**: *is the equilibrated/conserved object
a class function (character, per-irrep) or an extensive energy (per-state)?* Standard physics says per-state (overshoot);
Koide needs per-irrep. It does NOT knock the wall down, and the cross-fermion lepton-selector problem is untouched. But it
converts a vague "why this irrational r=√2" into a crisp measure-theory dichotomy with a single integer at stake.

**NEXT CONCRETE STEP (a direction, not a verdict):** Search for a *forced* reason the flavor sector's equilibrium measure
is a class function (per-irrep / character) rather than per-state — and one that is intrinsically lepton-selective. Two
specific, tractable probes:
- **(a)** Does the Sumino family-gauge-boson loop (the one known mechanism that protects Koide against QED running)
  weight by **character** (a class function over the family group) rather than by state? If the family-symmetry gauge
  coupling enters as Tr over irreps, channel-counting could be *induced* rather than postulated. Check the Sumino
  effective potential's measure explicitly.
- **(b)** Is the lepton-vs-quark asymmetry a **color-trace** effect after all — not as a uniform N_c factor (which
  cancels) but as a *per-channel* color weight that breaks the singlet/doublet balance differently for colored vs
  colorless families? The corpus killed the *uniform* color factor; the *channel-structured* color weight is untested.

---

## DEEP-EXPLORE #2 — a₀_norm⁴·π = δ_Maj² = sin²θ_W,tree = 3/8

**Sympy-exact** (`/tmp/wl_lead1_triple.py`):
```
a₀_norm = (3/8π)^(1/4) = √(2/Z) = 0.587787…      (framework Λ→a₀ normalization)
a₀_norm⁴·π = 3/8   (EXACT)        δ_Maj² = 3/8   (Singh J₃(O) lepton spread)        sin²θ_W,tree = 3/8 (SU5 trace)
a₀_kernel² = 8π/3 = π / sin²θ_W,tree  (EXACT)  →  (8π/3)(3/8) = π
```
Three independent constructions (Friedmann-3/Einstein-8π for gravity; the J₃(O) characteristic cubic for flavor; the
one-generation trace Tr(T₃²)/Tr(Q²) for the weak angle) land on the identical rational **3/8**, and the cross-sector
difference between the gravity quantity and the pure algebra is **exactly one bare factor of π** — precisely the
Einstein-8π measure the gravity object must carry and the pure algebra cannot. That single-π gap is the *canonical shape*
of a discrete-algebra → horizon-measure map (Unruh T = a/2π is the archetype).

**Is there a thread? — A real structural resonance, but value-equality not identity; ~1-in-100.**
- **Odds (re-quantified, `/tmp/wl_density_odds.py`):** in a pool of 137 simple rationals, ~1.5% sit within ±5% of 3/8;
  with ~10 favored candidates per construction, a 3-way same-rational hit is ~(1/10)² ≈ **1-in-100**. Medium, not
  Koide-class.
- **Both-ways caveat (decisive against over-claiming):** the three 3/8's have genuinely different origins
  (3 = spatial-d / rank-3-generations / SU(2)-from-cubic; 8 = Einstein-8π / octonion / trace) — a rational collision, not
  a proven shared invariant. **It does NOT make a₀ derive masses:** Singh's own 2026 paper (arXiv:2605.24866) confirms
  ZERO Λ/a₀/sin²θ_W content in his mass derivation, so the corpus "disjoint uses" verdict survives the newest literature.

**NEXT CONCRETE STEP:** Look for a *fourth, not-put-in-by-hand* appearance of 3/8 that the algebra→horizon map would
predict — and a derived reason the map forces *exactly* one bare π (no extra factors). Until a derived map predicts a
fresh 3/8, this stays a structural-resonance lead, not a bridge.

---

## DEEP-EXPLORE #3 — Z² = 8·(4π/3) and the exceptional-dimension hunt

**Sympy-exact** (`/tmp/wl_lead3_and_bath.py`): Z² = 32π/3 = 8·(4π/3) = 8 × unit-3-ball-volume. The gravity constant is
"8 × V_ball(d=3)", and 8 (= SU(3) adjoint = 2³ = octonion dim = D5 Coxeter) and 3 (= spatial d = Friedmann = triality)
are the same small integers that pervade the exceptional-algebra flavor structure.

**Is there a thread? — Mostly NULL / LOW.** The direct exceptional-group hunt came up **EMPTY**: no F4(52)/E6(78)/
E7(133)/E8(248)/G2(14) dimension lands within 1% of Z²=33.51 or any clean framework combination (248/Z²=7.40,
Z²/27=1.24 — no hits). Z lives in the measure/π world; exceptional dims live in the pure-integer world; they meet only at
the shared small integers, which are dimension-counts not group-dynamical appearances. Ubiquity ≠ unification. **Honest
label: near-miss/null; the 3-and-8 sharing is a weak structural resonance only.**

**NEXT STEP (if pursued):** would require a *forced* derivation in which a specific exceptional group's dimension (not
"3" and "8" generically) enters the gravity normalization — none found, low prior.

---

## THE SINGLE BEST LEAD TO CHASE NEXT SESSION

**Lead #1 — Koide r=√2 as irrep-CHANNEL (not STATE) equipartition.**

**Why this one:**
1. **Highest weirdness × simplicity × cross-domain.** It targets a genuinely rare angle (Koide Q=2/3 re-measured at
   ~1-in-69,000, vs the ~1-in-100 rational-collision of the 3/8 leads), and the entire open knob collapses to **one
   forced integer** — the doublet dimension 2 — separating two named measures. That is maximal simplicity on a maximally
   surprising target.
2. **It is a genuinely NEW attack axis.** The corpus ran six distinct Koide derivation attacks (formula-exhaustion,
   relational-exhaustion, dS-Unruh mechanism, Dirac-normalization bridge, variational/fixed-point, sector-QN-law) — none
   separated **per-channel from per-state counting**. This reframing is outside all six.
3. **The framework's own thermal bath is the natural home**, and the reframing turns its *documented failure mode* (the
   r=2 → Q=1 overshoot) into a *diagnosis*: the overshoot IS the standard per-state/Plancherel answer, so the question is
   no longer "why does the bath fail" but the precise "what measure replaces per-state with per-irrep, and why is it
   lepton-selective."
4. **Both-ways honest.** I chased it hard and caught my own "high-T = channel" shortcut as a smuggle — so I am NOT
   over-selling it. The wall STANDS (no thermal route forces channel-counting; the cross-fermion lepton-selector is
   unidentified). But it is the lead most likely to either (a) produce a real forced kernel if the Sumino family-gauge
   measure turns out to be a character/class-function sum, or (b) close the Koide question cleanly by *proving* the
   measure must be per-state. Either outcome is progress; that asymmetry is what makes it the one to chase.

**The concrete first move next session:** open the Sumino family-gauge-boson effective potential and check, explicitly,
whether its equilibrium measure sums over family-group **irreps (character / class function → channel → r=√2 → Koide)**
or over **states (→ r=2 → overshoot)** — and whether that measure is intrinsically lepton-selective (colored families
breaking the singlet/doublet balance via a *channel-structured* color weight, the one color route the corpus's
uniform-N_c cancellation did NOT test).

---

## BOTH-WAYS META-NOTE (no high-priesting, no manufacturing)

- **No manufactured win:** every value-echo (3/8 triple, g in EW, Z²=8·ball) is labeled at its true density-baked odds;
  none is dressed as a derivation. The 3/8 triple is ~1-in-100, not a bridge — and Singh's own newest paper confirms zero
  cosmology content in his mass derivation.
- **No high-priesting:** the Koide channel-equipartition reframing is surfaced and chased generously as a *new* axis even
  though the corpus declared Koide "exhausted" — because it is genuinely outside the six prior attacks, and the
  exploration produced a sharper, un-smuggled formulation of the wall plus two concrete forward probes (Sumino measure,
  channel-structured color).
- **The honest middle, per lead:** weird because X (a rare angle reduces to one integer / three sectors share one
  rational with a single-π gap); might mean Y (a per-irrep equilibrium measure / an algebra→horizon map); caveat Z (the
  bath gives per-state by default and the lepton-selector is unidentified / it's a ~1-in-100 rational collision, not a
  proven shared invariant).

**Files:** verification scripts `/tmp/wl_lead1_triple.py`, `/tmp/wl_lead2_equipartition.py`, `/tmp/wl_lead2_pushhard.py`,
`/tmp/wl_density_odds.py`, `/tmp/wl_lead3_and_bath.py`, `/tmp/wl_hiT_check.py`. Corpus grounding:
`project_atomos/notes/{KOIDE_DIRAC_BRIDGE,KOIDE_SECTOR_VERDICT,EXHAUSTION_THEOREM,GEOMETRIC_WEB}.md`.
