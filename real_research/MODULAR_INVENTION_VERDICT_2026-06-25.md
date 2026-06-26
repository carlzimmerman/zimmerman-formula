# Modular flavor (Attack A) + invented lepton-selective Koide protector (4 constructions) — both-ways VERDICT

**Date:** 2026-06-25
**Question (two attacks, one discipline):** Does genuinely-NEW machinery — (A) Feruglio modular
flavor as a bridge from the framework's de Sitter / `Z=√(32π/3)` geometry to a fixed modulus `τ`,
or (B) an *invented* lepton-selective Koide protector (4 candidate constructions) — crack the lone
open Koide question: derive the amplitude `r=√2` (⟺ `Q=2/3`) **non-circularly**, without inputting
the masses / `2/3` / `√2`?
**Bar for a WIN (high, both-ways):** (A) `τ` fixed by dS/Z geometry via a relation derived WITHOUT
the masses/Koide, that THEN reproduces the data. (B) a protector that is lepton-selective BY
CONSTRUCTION AND forces `r=√2` without assuming `2/3` AND is not falsified by the quarks.
**Tooling reproduced this session:** `sympy 1.13` + `mpmath dps≥40`; every numeric and structural
claim below was re-run clean-room, not merely re-read. Quarantine held: `2/3`, `√2`, `r`, the masses
enter ONLY as the empirical target.

---

## VERDICTS

- **(A) Modular flavor → `τ`-fixing: PARTIAL-HOOK** (one real structural resonance — shared `Z3`
  generation symmetry — but no forced `τ`, no fixed point reproduces `2/3`; the amplitude stays free).
- **(B) Invented lepton-selective protector (4 constructions): FAILS** (every construction either
  does not force `r=√2`, or forces it only by a tuned coupling that IS the operator vanishing at
  `2/3` = smuggling the answer, or supplies no natural lepton-selector).

Both land where the honest prior expected. The combined meta-result is the load-bearing one: **even
invention + new external frameworks do not crack it**, which CONFIRMS — does not weaken — the deep
standing: the SM mass sector needs genuinely-new lepton-selective IR dynamics not yet in hand. That
is honest progress (a sharpened wall with its location named), not a failure to report.

---

## Anti-circularity spine (verified first, sympy-exact — the whole game)

`Q = 1/3 + r²/6`, phase-independent (re-derived dps=40):
- `r=√2 ⟹ Q = 1/3 + 2/6 = 2/3` **exactly**;  `r=2 ⟹ Q=1`;  `r=0 ⟹ Q=1/3`.

Therefore **"force any mechanism to give `r=√2`" ≡ "force `|singlet|²=|doublet|²`" ≡ "assume
`Q=2/3`"** — UNLESS the forcing relation never references `2/3` or `√2`. This identity is the knife
every candidate below is held to. (Verified: the `r=√(2^{p+1})` measure-family gives `p=0→r=√2→Q=2/3`,
`p=1→r=2→Q=1`, `p=2→r=2√2→Q=5/3`; Koide is the lone non-covariant `p=0` endpoint.)

---

## ATTACK A — Modular flavor ↔ dS geometry: **PARTIAL-HOOK**

Script: `opus_48_extended_research/reviews/koide_dsunruh/attackA_modular_dS_bridge.py` (re-run clean
this session; all arithmetic reproduced). Four concrete bridge proposals, each flagged for
circularity / surface-analogy:

- **[A2] Does `Z` or the kernel equal a fixed-point coordinate? NO.** `Z=5.789`,
  `kernel=(3/8π)^(1/4)=0.5878` vs the universal fixed-point coordinates `Im(ω)=√3/2=0.866`,
  `Im(i)=1`, `Re(ω)=−1/2`. Zero clean matches (rel_eps `1e-6`). Fixed points are **SL(2,Z)-universal**
  — a fixed point of `SL(2,Z)` for ANY theory — carrying no `32π/3` or `3/8π` information. No
  framework→`τ` map.
- **[A3] Does the dS scale set the nome `|q|=e^{−2π Im τ}`? Drives `τ` the WRONG way.** The ONLY
  genuine dS dimensionless number is `1/S_dS = GℏH²/c⁵ ~ 10⁻¹²²` (de Sitter entropy). Setting
  `|q|=10⁻¹²²` gives **`Im(τ)≈44.7`** — deep in the **`i·∞` CUSP** (residual `Z_N^T` shift →
  hierarchical/diagonal texture), the OPPOSITE of the democratic-`Z3` circulant Koide needs. And
  `10⁻¹²²` is the **measured** Λ — an input, not a derivation.
- **[A4] Steelman: FORCE `τ=ω` (its residual `Z3^ST` = the generation `Z3`) — does `ω` give `Q=2/3`?
  NO.** Verified the Koide `Q` from the actual modular-form values:
  - `τ=i` (wt-2 A4 triplet `Y=(1,1−√3,−2+√3)`) → `Q = 0.4019` (`r=0.642`);
  - `τ=ω` pure `Z3` eigenvector `(1,ω,ω²)` → `|·|=(1,1,1)` democratic → `Q = 1/3` (`r=0`);
  - `τ=ω` Feruglio triplet `(1,ω,−ω²/2)` → `|·|=(1,1,½)` → `Q = 0.360` (`r=0.40`);
  - cusp → `Q=1`. **NONE equals `2/3=0.6667`.** Different reps/weights at the SAME `ω` give
    `Q ∈ {1/3, 0.36, 0.5, 0.375}`, so landing on `2/3` requires **hand-picking the rep = inputting
    the answer.**
- **[A5] Is `H ↔ dS` a forced identification or a surface analogy? SURFACE ANALOGY.** `H=SL(2,R)/SO(2)`
  is Euclidean, negative-curvature, 2D moduli space; `dS₄` is Lorentzian, positive-curvature, 4D
  spacetime. The framework has NO `τ`, NO holomorphic Yukawa, NO `q`-expansion, NO modular weight;
  the flavor `τ` is a dynamical SUGRA/string modulus VEV — not the cosmological constant and not the
  fixed pure number `Z`. "Both hyperbolic" supplies no functor sending `Z` to a point of `H`.

**Why PARTIAL-HOOK and not pure NULL:** there is ONE genuine structural resonance — the residual
symmetry at `τ=ω` is the order-3 `Z3^ST`, which **is the same generation-`Z3`** the framework's
Spin8-triality `1+2` decomposition already uses to build the Koide circulant SHAPE. Modular flavor
and the framework independently land on the same `Z3` — non-trivial corroboration of the SHAPE.
**But (the honest both-ways truth)** this is exactly the `1+2` shape the framework already possessed,
and it leaves the AMPLITUDE `r=√2` FREE in BOTH pictures: the actual modular form value at `ω` gives
`Q=1/3` or `0.36`, never `2/3`. The hook re-expresses the known shape; it derives no amplitude. The
circularity theorem still bites. This is a hosting/corroboration hook on the SHAPE, not a derivation.

---

## ATTACK B — Invented lepton-selective Koide protector (4 constructions): **FAILS**

All four fail, each by a distinct, verified mechanism. (sympy 1.13 + mpmath dps=40; quarantine held.)

- **C1 — Color-singlet-weighted protector. TWO independent kills.**
  - *(1a) Does not force `r=√2` at all.* The singlet/doublet split lives on the **generation (`S3`)**
    factor; a color-singlet projector acts only on the orthogonal **color** tensor factor, commutes
    with everything on generation space → imposes ZERO constraint on `r`.
  - *(1b) Does not exclude quarks.* `q̄q` is **itself a color singlet**, so the color-singlet channel
    is populated by quark bilinears. Excluding quarks needs forbidding `q̄q` by hand. The color
    channel delivers neither the forcing nor the selectivity.
- **C2 — Anomaly-selective family gauge (Sumino-class). Color is a multiplicity factor, not a kind
  difference.** Careful Weyl `[SU(3)_F]³` count with the conjugate assignment `ψ_L:(3,1)`,
  `e_R:(3̄,−1)`: the LEPTON cubic anomaly is **nonzero** (=3), so Sumino cancels it by hand with
  spectator fermions; the QUARK anomaly is **12× larger** (color `N_c=3` × weak mult). Color enters
  only as anomaly SIZE, not KIND. So leptons are made anomaly-free by added spectators and quarks are
  excluded by simply **not gauging** their family symmetry — a field-content CHOICE, not a forced
  selector. And the QED cancellation needs the tuned `α=¼α_F` (Sumino's own *"accidental factor or
  parameter tuning"*).
- **C3 — Residual/exchange-symmetry equipartition protector. No symmetry can do it.** The natural
  non-circular way to force `|s|=|d|` is a symmetry exchanging the singlet (dim 1) and doublet (dim 2)
  sectors. But they have **different dimension**; no group element and no automorphism (`Out(S3)`
  trivial; `S3` is complete) can exchange irreps of unequal dimension. The general `S3`-invariant
  potential `V = a|s|²+b|d|²+c|s|⁴+d|d|⁴+e|s|²|d|²` has a minimum at `|s|=|d|` ONLY under the tuned
  `a=b ∧ c=d` (sympy-exact), which no symmetry enforces. Writing `V=λ(|s|²−|d|²)²` is the smuggle:
  `(|s|²−|d|²)` is precisely the operator that vanishes at `Q=2/3`.
- **C4 — Modular fixed-point protector (Feruglio-class; the strongest hope). Pins AWAY from
  democratic.** Verified the canonical `τ=i` A4 wt-2 multiplet `Y=(1, 1−√3, −2+√3)` is **ORTHOGONAL**
  to the democratic axis: `Σ Y = 0` exactly → angle `90°` (re-confirmed dps=40). That is the EXTREME
  OPPOSITE of Koide's `45°` (`cos=1/√2`), not equipartition (`Q` at `τ=i` `=0.4019`, not `2/3`).
  The residual symmetry pins a specific algebraic texture AWAY from democratic; reaching `45°`
  requires leaving the fixed point and tuning the departure `|ε|` chosen to hit `2/3` (circular).
  Modular symmetry also acts on all sectors → lepton-vs-quark selectivity again needs by-hand
  differential weight assignments.

**Forcing scorecard:** `forces_r_√2_non-circular = NO` (no construction does it without smuggling
`2/3` via the `(|s|²−|d|²)` operator or hand-tuning).
**Selectivity scorecard:** `lepton-selective = TUNED / hand-imposed in every construction` — color
weight is not a selector (`q̄q` is a singlet); anomaly cancellation is a field-content choice (both
lepton and quark `[SU(3)_F]³` anomalies are nonzero, color only changes size); modular acts on all
sectors. The one genuine selectivity in the literature (Sumino) is DYNAMICAL — conjugate
`(3,1)/(3̄,−1)` reps + tuned `α=¼α_F` — which the framework's spine does not carry.

---

## Framework connection — FRAMEWORK-FOREIGN dynamics, framework-HOSTED symmetry

None of the protector *dynamics* comes from the spine (`a₀/Z/κ/dS-Unruh`). The only protector that
could force `r=√2` — a gauged `U(3)/S3` family sector with a tuned scalar `X`-field + opposite-sign
family-boson loop (Sumino's own new physics at `10²–10³ TeV`) — requires a new gauge group, a new
scalar, and the `α=¼α_F` tuning, supplied by NONE of `Z, κ, a₀, dS-Unruh`. The framework offers only
a **symmetry HOME**: `S3`/Spin8-triality gives the `1`(democratic)`+2`(standard) decomposition the
Koide circulant needs — a hosting hook, not the dynamics.

Numerical coincidences, verified and correctly diagnosed as non-load-bearing:
- closest framework amplitude `√(2/Z)=(3/8π)^(1/4)=0.5878` is off `√2` by exactly `√Z=2.406` —
  **the wrong number** (re-confirmed dps=40);
- `κ=½ ⟹ 1/√κ=√2` **exactly** — but `κ` is the provably-unforceable gravity normalization, is
  fermion-blind, and is quark-Koide-falsified (a cross-sector coincidence between two FREE numbers);
- `kernel⁴ = 3/(8π)` **exactly** collides with Sumino's `3α_F/(8π)` prefactor — but that prefactor
  is **constructed to CANCEL** (it is on its way to zero by the `α=¼α_F` design) and the two `3/(8π)`
  have unrelated origins (Einstein-`8πG`+Friedmann-`3H²` vs a 1-loop gauge self-energy). Forcing it
  is circular.

---

## Honest both-ways credit and the wall

**Genuine credit at full weight:** the framework lands in the **right symmetry neighborhood**
(`S3`/triality `1+2`), correctly diagnoses the mechanism must be **IR/Sumino-class** (Koide exact at
pole masses, ~178σ-resolvable RG drift, UV group-count ruled out), the structural reduction
`3 components → 1 number r` is real, AND modular flavor independently corroborates the generation
`Z3` (the Attack-A hook). These are not nothing.

**The walls, named precisely:**
- A color/anomaly selector REDUCES nothing on `r` and does not naturally exclude quarks.
- No symmetry can exchange the dim-1 singlet and dim-2 doublet → no non-circular equipartition forcing.
- Every covariant/thermal measure gives `r=2` (overshoot); `r=√2` is the lone non-covariant `p=0`
  endpoint, chosen because it hits `2/3`.
- The lepton-selector is ABSENT: quarks share the `S3` but give `Q≠2/3` (`Q_up=0.849`, `Q_down=0.731`,
  robust to ±30% mass band), and the dS bath is flavor-blind by the equivalence principle.

**META (the honest deep result).** Both attacks were genuinely-new ground (an external framework,
and four invented constructions), not a re-run — and **both come back PARTIAL/FAIL**. That even
invention and a borrowed, more-predictive external framework (modular flavor, which CAN pin ratios
at fixed points) **cannot crack `r=√2` non-circularly** is the substantive finding: it CONFIRMS and
sharpens the banked standing that the SM mass sector is kernel-free and needs **genuinely-new
lepton-selective IR dynamics not yet in hand** (a real gauged `U(3)/S3` family sector whose potential
minimum lands at `r=√2` AND supplies the opposite-sign family-boson loop AND is charged-lepton-
specific by construction). The framework offers a symmetry home for exactly that; it does not derive
it. Quarantine held; `a₀/Z/κ` not derived; Koide stays RE-LABELED, not derived.

---

## The ONE concrete next step (for the Attack-A partial hook only)

The only hook with any forward life is the shared `Z3`. The concrete, falsifiable next step that
would either upgrade it or kill it cleanly:

**Compute the Koide `Q` from a modular form whose weight/level is FIXED by a framework quantum number
(not hand-picked) at `τ=ω` — and check whether ANY framework-forced weight `k` lands `Q=2/3`
non-circularly.** Concretely: is there a framework integer (e.g. from the Spin8-triality rep content,
or `Z`'s integer part, or the `1+2`/`3`-generation index) that selects a modular weight `k` such that
the weight-`k` level-3 A4 (or S4/A5) multiplet value at `ω` gives `|·|` at exactly `45°`? If a
framework-forced `k` exists and yields `Q=2/3` WITHOUT scanning weights to hit it, that is a genuine
opening to stress-test hard. **Honest prior: this is very likely NULL too** — the `Q(ω)` values
across weights/reps already span `{1/3, 0.36, 0.5, 0.375}` and none is `2/3`, so unless a framework
quantum number forces the weight *and* that weight happens to give `45°`, it reduces to hand-picking.
But it is the single un-run, non-circular test the `Z3` resonance actually licenses, and it is cheap
(sympy + the published A4/S4/A5 weight-`k` multiplets). Run it; report both ways.

---

**Scripts / sources (reproduced or read this session):**
`opus_48_extended_research/reviews/koide_dsunruh/attackA_modular_dS_bridge.py` (re-run, all arithmetic
reproduced); `real_research/KOIDE_CHANNEL_MEASURE_VERDICT_2026-06-25.md`,
`KOIDE_CHANNEL_COUNT_SMUGGLE_CHECK_2026-06-25.md`, `KOIDE_CPATH_FRAMEWORK_FIXES_SUMINO_2026-06-25.md`;
`opus_48_extended_research/reviews/KOIDE_FROM_DSUNRUH_2026-06-20.md`,
`KOIDE_IR_MECHANISM_2026-06-17.md`, `PARTICLE_BRIDGE_FRESH_EYES_2026-06-17.md`.
Primary literature: Feruglio arXiv:1706.08749 (modular flavor, fixed points `i`/`ω`/cusp, residual
`Z2^S`/`Z3^ST`/`Z_N^T`); Sumino arXiv:0903.3640 / 0812.2090 (the one genuine Koide-deriving mechanism
— imposes `2/3` via the `(−1,+1⁸)` X-signature, protects it via the tuned `α=¼α_F` per-flavor lock).
