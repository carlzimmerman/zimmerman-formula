# Koide per-irrep-vs-per-state MEASURE — decisive both-ways VERDICT

**Date:** 2026-06-25
**Question:** Does the family-gauge / dS-Unruh structure FORCE a per-irrep / class-function
measure → r=√2 → Koide Q=2/3 *derived* (a genuine OPENING — the first non-circular 2/3 in the
corpus)? Or is the measure per-STATE → overshoot r=2 → Koide stays a re-labeling (WALL)? Or
genuinely OPEN with a sharper probe?
**Tooling:** sympy 1.13.1 + mpmath dps≥50 (clean-room re-derivation, not just re-running the
task scripts); primary source WebFetch of Sumino arXiv:0903.3640 (ar5iv full text).
**Quarantine held:** 2/3, √2, r enter ONLY as the empirical PDG target to be matched — never as input.

---

## VERDICT: (B) WALL — per-STATE confirmed. Koide stays a re-labeling (the 171st).

The dS-Unruh / family-gauge structure does **NOT** force a per-irrep measure. Every covariant
measure (Plancherel, regular-rep, Gibbs over any S3-invariant Casimir, equivariant character at
the physical equilibrium point g=e) carries the irrep **dimension** d_R → per-STATE → **r=2 →
Q=1**, the documented overshoot. Landing on Koide (r=√2) requires the **non-covariant** "count
irreps, ignore their dimension" measure — the p=0 endpoint of a one-parameter family — which is
selected *because* it hits 2/3. And the **lepton-selector is absent**: quarks share the same S3
3-generation structure but Q≠2/3, so any fermion-blind measure (which the dS bath is, by the
equivalence principle) is falsified by the quarks. This is not a crack; it is a clean wall, and
its location is named precisely below.

---

## The single decisive identity (smoking gun, sympy-exact, clean-room reproduced)

Split the √-mass energy budget between the S3 singlet (dim 1) and doublet (dim 2) with weight
∝ dim^p:

| p | measure name | covariant? | r | Koide Q |
|---|--------------|-----------|---|---------|
| **0** | **flat-over-irreps (ignore dim)** | **NO** | **√2** | **2/3 ← the target** |
| 1 | Plancherel / per-state / thermal | YES (canonical) | 2 | 1 (overshoot) |
| 2 | regular representation | YES | 2√2 | 5/3 |

**r = √(2^{p+1})**, sympy-exact. Koide is the **p=0 endpoint — the only non-covariant member**.
The canonical group-theoretic base measure is Plancherel (weight = dim), which is p=1, which
**overshoots to exactly the framework's known r=2 = Q=1**. Choosing p=0 is choosing the answer.
That is the whole forcing question in one line, and the answer is NO.

Independently re-derived via Shannon maxent over channel probabilities {w_s, w_d}: maxent
relative to the **dimension** base measure (Plancherel) → w_s=1/3, w_d=2/3 → r=2 → Q=1; maxent
relative to a **flat-over-labels** base → w_s=w_d=1/2 → r=√2 → Q=2/3. The flat-over-labels base
treats a 1-dim and a 2-dim irrep as equiprobable a priori — no thermal/covariant principle does
this; it must be input by hand.

---

## Why no covariant measure forces per-irrep — the d_R smuggle (decisive)

A thermal bath weights by a **trace** = sum over a basis = sum over STATES. The verified, clean-
room-reproduced facts:

- **Gibbs with a Casimir as "energy":** Z = 1·e^{−βC_S} + 2·e^{−βC_D}. The doublet's factor **2**
  (= d_D) is *inside the trace and unavoidable*. To get P_singlet = P_doublet you need a **tuned**
  β = log2/(C_D−C_S) — not high-T, not forced. The irrep label is a superselection datum, not an
  additive extensive charge, so it is not the kind of quantity a bath equilibrates.
- **Equivariant / character-valued partition function (the cleanest YES candidate):** Z(g) =
  Σ_R n_R χ_R(g) e^{−βE_R} IS a class function of an *inserted twist g*. But at the physical
  equilibrium g = identity, χ_R(e) = d_R (S3: trivial 1, sign 1, standard 2) → per-STATE returns.
  Character-valuedness survives only under a permanent flavor twist g≠e, which is not a thermal
  equilibrium and has no dS justification. The genuine dS-horizon character (Anninos–Denef–Law–Sun)
  is of the SPACETIME isometry SO(d+1,1)/quasinormal modes — blind to internal S3 family by
  Coleman–Mandula. Localization weights are per-tangent-weight products 1/(1−g^w), not a flat
  per-irrep sum.
- **Native dS-Unruh bath:** a mode sum over the 1+2 = 3-state Hilbert space → per-STATE → r=2.

**Per-irrep requires CANCELLING d_R** (a Plancherel-dual / character measure), which is no Gibbs
measure of any Hamiltonian. None of Q1/Q2/Q3 supplies it.

---

## Sumino is NOT a per-irrep measure — verified against the primary source

The setup's hope was: "Sumino DERIVES Koide 2/3, so he must encode an effectively-per-irrep
structure — find it and let dS-Unruh inherit it." **WebFetch of arXiv:0903.3640 (ar5iv full text)
falsifies the premise in Sumino's own words.**

1. **2/3 is IMPOSED, not derived.** Sumino: *"By deliberately choosing a specific form of the
   potential, the VEV is made to satisfy the relation"*; *"We need some symmetry enhancement in
   order to realize this relation without fine tuning"*; *"every model requires either absence or
   strong suppression of some of the terms in the potential … without justification."* The 45°
   equal-amplitude split (Φ⁰)²=ΦᵃΦᵃ is the **selected potential minimum** (engineered via the
   field X + SU(9)×U(1)), with required parameter hierarchies of order 10⁻³–10⁻⁴.
2. **The protection is a per-FLAVOR radiative lock, not a per-irrep weight.** The U(3) gauge-boson
   1-loop has the SAME per-flavor log shape as QED, opposite sign; cancellation for arbitrary μ
   requires **α = (1/4)α_F** — which Sumino concedes is an *"accidental factor (or parameter
   tuning)"*. It needs α_F=α AND the family-boson masses locked to v_i ∝ √m_i — a dynamical lock,
   not a thermal measure. There is no bath, no Plancherel-vs-class-function choice anywhere.
3. **The steelman ("condition (19) IS an equal-channel split") is a CONSTRAINT, not a measure,
   and on the wrong space.** Its "2 channels" = U(1) vs SU(3)-adjoint of the 9-dim gauge/scalar
   T^α space — *not* the S3 singlet/doublet of the 3 generations that carries the 45°. It is an
   imposed VEV minimum, not a forced thermal/Plancherel weight. The high bar (a forced measure
   that *lands* 2/3) is not met.
4. **Lepton-selectivity is dynamical, not measure-borne.** Sumino: *"Quarks and neutrinos are not
   included … anomalies induced by the family gauge interactions do not cancel."* No Koide for
   quarks emerges. Selectivity rides on the conjugate-rep operator O₁ (ψ_L in (3,1), e_R in
   (3̄,−1)) + the α=(1/4)α_F tuning — charge-sector physics the flavor-blind dS bath cannot carry.

**Net: even the one genuine Koide-deriving mechanism in the literature does NOT derive 2/3** — it
imposes it (potential minimum) and protects it (per-flavor radiative lock). There is no per-irrep
kernel for the dS-Unruh spine to inherit. The banked NO is sharpened, not weakened.

---

## Lepton-selector test (REQUIRED for any OPENING) — ABSENT

PDG masses, mpmath dps=50:

| sector | Q (Koide) | vs 2/3 | ±30%-mass band |
|--------|-----------|--------|----------------|
| charged leptons (e,μ,τ) | 0.6666605 | −6.2e-6 (≈−0.9σ, τ-mass-limited) | — |
| up quarks (u,c,t) | 0.848981 | +0.182 | [0.806, 0.884] |
| down quarks (d,s,b) | 0.731428 | +0.0648 | [0.669, 0.787] |
| neutrinos (NO, m₁ free) | 0.585 (m₁=0) … 0.336 (m₁=0.05 eV) | free fn of m₁ | — |

Only charged leptons hit 2/3. The mismatch is robust to ±30% quark-mass uncertainty (the down
band only *grazes* 2/3 at its extreme; the up band is far). A measure that acts on the S3
*generation* index — as the dS-Unruh bath does, flavor-blind by the equivalence principle —
would force 2/3 in **all** sectors → **falsified by the quarks**. No lepton-selector exists in
either the S3 structure or the dS bath. **LEPTON-SELECTOR: ABSENT (fatal to any OPENING claim).**

---

## Smuggles caught

1. **The MEASURE smuggle (decisive):** "flat over channels" = the p=0 / ignore-dimension weight,
   the unique non-covariant member of the dim^p family; every covariant measure (Plancherel,
   regular-rep, Gibbs-Casimir, character@g=e, localization) carries d_R → per-state → overshoot.
2. **The d_R-restoration smuggle:** any "per-irrep" measure must cancel the dimension multiplicity,
   but a thermal trace always carries d_R = χ_R(e); the doublet's factor 2 reappears.
3. **The "Sumino is per-irrep" smuggle:** Sumino imposes 2/3 (tuned potential minimum) + protects
   it (per-flavor radiative lock with an accidental α=¼α_F); no thermal/Plancherel measure exists
   anywhere — verified against the primary source.
4. **The wrong-decomposition smuggle:** the family-gauge irreps are U(3) 8+1; the 45° lives on the
   S3 1+2 of the 3 generations — different spaces.
5. **The selector smuggle:** the principle must be hand-switched-off for quarks; the S3/dS
   structure supplies no selector.

---

## Bottom line (both ways, no manufactured result)

- **Forced (real credit, full weight):** the decomposition *objects* {singlet=trivial,
  doublet=standard} of the √-mass vector under S3-natural-3 are genuine rep theory; and the
  framework correctly localizes the mechanism to IR/Sumino-class (Koide exact at pole masses,
  ~178σ-resolvable RG drift). Right symmetry neighborhood, right mechanism class.
- **NOT forced (the wall):** the *equipartition measure*. r=√2 is the p=0 non-covariant endpoint;
  every covariant/thermal measure gives r=2 (overshoot). The free parameter r is merely relabeled
  from "doublet/singlet ratio" to "measure exponent p," with p=0 chosen because it hits Koide.
- **Falsified (the selector):** quarks share the S3 but give Q≠2/3; the dS bath is flavor-blind;
  no lepton-selector exists.

This is the same wall as KOIDE_FROM_DSUNRUH (165th) and KOIDE_CHANNEL_COUNT_SMUGGLE_CHECK (170th),
now reached from the per-irrep-vs-per-state *measure* axis and confirmed against Sumino's primary
text. **The axis is closed cleanly.** The SM mass sector stays walled.

**The one un-smuggled question that would actually be open (the C-path, NOT supplied by any
re-labeling):** a *dynamical, lepton-specific* O(α/π) IR mechanism — a real gauged
U(3)/S₃-triality family sector whose scalar-potential minimum lands at r=√2 AND supplies the
opposite-sign family-boson loop (Sumino's own new physics). The framework offers a *symmetry home*
for that, but does not derive it from a₀/Z/κ. That is a search for new lepton-selective dynamics,
not a measure the dS-Unruh spine carries.

**Scripts (reproduced this session):**
`/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/koide_dsunruh/taskb_setup.py`,
`taskb_reconcile.py`, `taskb_q1_casimir.py`, `taskb_q2_index.py`, `taskb_q3_familygauge.py`,
`taskb_default_perstate.py`, `taskb_sumino_irrep_audit.py`.
Primary source: arXiv:0903.3640 (ar5iv full text, WebFetch'd this session).
Banked: `KOIDE_FROM_DSUNRUH_2026-06-20.md`, `KOIDE_IR_MECHANISM_2026-06-17.md`,
`KOIDE_CHANNEL_COUNT_SMUGGLE_CHECK_2026-06-25.md`.
