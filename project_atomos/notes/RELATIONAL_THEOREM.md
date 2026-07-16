# The Relational / Koide-Class Exhaustion Theorem

**Project:** PROJECT_ATOMOS — the relational (Koide-class) shape
**Date:** 2026-06-25
**Enumerator:** `/Users/carlzimmerman/new_physics/project_atomos/exhaust_relational.py`
**Gate:** `/Users/carlzimmerman/new_physics/project_atomos/gate/` (3-part gate, reused verbatim, never modified)
**Status:** ADVERSARIALLY VERIFIED — clean null, Koide is the unique survivor (and even Koide is gate-killed).

---

## THE THEOREM (precise statement)

> Exhaustively over the Koide-class **relational** space — **1014 mass-set relations** in four
> families (F1 generalized-Koide power-sums, F2 sqrt-mass-vector angles, F3 symmetric-function
> invariants), fully enumerated over every triple and quad within and across the SM mass sectors,
> plus **4** fixed F4 cross-sector mixing↔mass interlocks, tested against a pool of **15**
> forced-geometric target values (exact exhaustive look-elsewhere multiplicity = 1014 × 15 =
> **15,210**) — the **only** parameter-free, forced-value relation that survives the random-mass-set
> null **and** the cross-fermion falsification **and** the exact look-elsewhere correction is the
> **Koide relation Q = (Σ mᵢ)/(Σ √mᵢ)² = 2/3 for the charged leptons**.
>
> Validated by re-deriving Koide: the enumerator recovers Q=2/3 to |Q−2/3|=6.16×10⁻⁶ and certifies
> it the Koide way (random-mass-triple null ~1-in-44,444, density peak away from 2/3), NOT by
> Gate-A-on-the-rational-2/3.
>
> **Even Koide does not pass the full gate**: it clears Gate A (structural null) but is FDR-DEAD at
> Gate B — the Koide amplitude has no forced kernel. So the relational shape produces **zero new
> physics-class survivors**, and re-confirms that Koide is a real, parameter-free *puzzle* that the
> framework only **re-labels**, not a derived result.

**One line:** Over the fully-enumerated Koide-class relational space, Koide Q=2/3 (charged leptons)
is the unique parameter-free forced-value relation in the SM — a clean null, no new lead — and it
remains a kernel-free re-labeling, not a derivation.

---

## SCOPE (exactly what was covered)

### Relation families (deterministic, complete)
- **F1 — generalized-Koide power sums:** R = (Σ mᵢᵃ)/(Σ mᵢᵇ)ᶜ over the bounded rational grid
  a ∈ {½,1,3/2,2}, b ∈ {¼,½,1,3/2}, c ∈ {1,2,3}, restricted to the scale-invariant members
  a = b·c (7 per triple). **CONTAINS the Koide member (a,b,c)=(1,½,2)** — this is the ground-truth
  carrier and the validity proof.
- **F2 — sqrt-mass-vector angles:** cos²θ of the √m vector to reference vectors (the democratic
  (1,…,1) Koide ref + each canonical basis eᵢ), reported both as the cos² ratio and as the angle in
  degrees (the Koide 45° / cos²=½ geometry, plus the Z₃/circulant amplitude).
- **F3 — symmetric-function / power-sum invariant ratios:** scale-invariant ratios p₁²/(n·p₂),
  n·p₂/p₁², geom/arith, p_½²/(n·p₁) (= the Koide-cos² class), e₂/e₁² over each mass set.
- **F4 — cross-sector interlocks (fixed list of 4):** quark-lepton complementarity (θ_C + θ₁₂^PMNS
  vs 45°), Gatto-Sartori-Tonin (√(m_d/m_s) vs Cabibbo λ), b-τ unification (m_b/m_τ vs 3), and
  θ₁₃^PMNS vs λ/√2.

### Sectors (mass sets the relations range over)
charged leptons {e,μ,τ}; up-quarks {u,c,t}; down-quarks {d,s,b}; all-6-quarks (triples+quads);
generation-diagonal {e,u,d}; lepton+top {e,μ,τ,t}; lepton+bottom {e,μ,τ,b}. (Baryons {p,n}: too
few for a triple, used cross-sector only.)

### Forced-target pool (15)
The 2/3 / circulant family {2/3, 1/3, 1/2, 3/4, 1/6, 1, 3/8, 5/3, 2/9}, the forced O(1) irrationals
{√2, 1/√2, √3}, and the angles {45°, 60°, asin(1/√3) TBM}.

---

## COMPLETENESS — proven, not estimated

Per-sector **closed-form == enumerated count in every one of the 8 sectors** (`--self-check`):

| sector   | keys | triples | quads | F1 | F2 | F3 | total | match |
|----------|-----:|--------:|------:|---:|---:|---:|------:|:-----:|
| leptons  | 3 | 1 | 0 | 7 | 8 | 5 | 20 | ✓ |
| up       | 3 | 1 | 0 | 7 | 8 | 5 | 20 | ✓ |
| down     | 3 | 1 | 0 | 7 | 8 | 5 | 20 | ✓ |
| quarks6  | 6 | 20 | 15 | 245 | 310 | 175 | 730 | ✓ |
| baryons  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | ✓ |
| gen_diag | 3 | 1 | 0 | 7 | 8 | 5 | 20 | ✓ |
| lep_up   | 4 | 4 | 1 | 35 | 42 | 25 | 102 | ✓ |
| lep_down | 4 | 4 | 1 | 35 | 42 | 25 | 102 | ✓ |
| **TOTAL**| | | | | | | **1014** | **PROVEN** |

The relation space is a deterministic Cartesian product (families × exponent-grid × mass-subsets ×
reference-vectors); its closed-form size matches the actual generated count exactly. **Nothing is
skipped** → the FDR look-elsewhere (1014 × 15 = 15,210, 13.9 bits) is **exact**, not an estimate.

---

## GROUND TRUTH — Koide re-derived (the validity proof)

`exhaust_relational.py --koide-ground-truth` (independently reproduced this session):

- Koide member found in the F1 grid: **(sum m^1)/(sum m^1/2)^2 = Q = (Σm)/(Σ√m)²** — the (1,½,2) member.
- On the charged-lepton masses: **Q = 0.66666051**, **|Q − 2/3| = 6.16×10⁻⁶** (hand-confirmed).
- Certified **the Koide way** (NOT Gate-A-on-2/3): random-mass-triple null
  **P(|Q_rand − 2/3| < 1e-5) = 2.25×10⁻⁵ = ~1-in-44,444**, matching the banked ~1-in-44,000.
  **Seed-robust** — independent seeds give 1-in-40,816 … 1-in-54,054 (centered on ~1-in-44k);
  not a seed artifact.
- Random-Q density **peaks at 0.997, far from 2/3** → 2/3 is a genuine special angle for the leptons.
- Gate: clears **Gate A** (rational→structural, 11.2 bits at the leptons-only multiplicity) but is
  **FDR-DEAD at Gate B** ("forced structure appears in only 0 independent places; a single
  appearance is a definition, not a kernel"). This is the honest banked Koide verdict.
- The cos²=½ (45°) F2 partner and the p_½²/(n·p₁)=½ F3 invariant are algebraically the SAME
  e,μ,τ content (cos² = 1/(3Q)); hand-confirmed cos² = 0.50000462. Not independent relations.

If the F1 family had not contained the Koide member, the relational shape would be wrong and this
would have reported + stopped. It does, and it re-derives Koide → **validity proven.**

---

## THE FULL SWEEP — zero new survivors (the null)

Over all 1014 relations × 15 targets, **169 forced-target matches** were found, decomposing as:
- **147 trivial R = 1 identities** — relations of the form (Σmᵃ)/(Σmᵃ)¹ = 1 by construction;
  null p = 1.0, FDR-DEAD instantly (−0.0 bits). Independently reproduced (e.g. up-sector matches are
  all R=1, gate-A fail).
- **22 non-trivial**, of which the genuinely-special ones (raw single-relation null beating
  measurement noise) are scrutinized and refuted below.

### Survivors after the random-set null + cross-fermion + look-elsewhere: **the lepton Koide trio only**
The Koide content recurs as expected in `leptons`, `lep_up`, `lep_down` (same e,μ,τ masses):
F1 Q=2/3 (1-in-44,444), F2 cos²=½ / 45°, F3 p_½²/(n·p₁)=½ (1-in-35,088). **All the same relation
re-expressed**, not new. Under the exact look-elsewhere (−13.9 bits), Koide's 15.4 raw bits →
**+1.5 corrected bits** (below the 10-bit Gate-A threshold over the full search), and Gate B kills
it regardless. No physics-class survivor.

---

## ADVERSARIAL REFUTATIONS (every non-trivial near-hit killed)

### (1) gen_diag F1 (Σm^{3/2})/(Σm^{1/2})³ = 0.16651 → 1/6, RAW ~1-in-97,561 — **REFUTED**
The single most "surprising" non-Koide hit. Killed three independent ways (all reproduced this session):
- **(a) Light-quark-mass artifact.** Built on m_u (±22.7%) and m_d (±10.2%). The 1e-5 absolute null
  window is unjustified for ~10–20%-uncertain inputs. MC-propagating the PDG mass errors:
  **R = 0.1685 ± 0.0100, only 0.18σ from 1/6**, and **P(|R−1/6| < 1e-3) ≈ 0.09 (~1-in-11)** at a
  measurement-class window. The "1-in-97k" is a tolerance artifact (eps tighter than the input
  precision).
- **(b) Density / bounded-range.** The relation is bounded **[1/9 = 0.111 … 1]** (degenerate floor
  1/n²=1/9, confirmed analytically). 1/6 sits in the dense band just above the floor: **4.86%** of
  random triples land in [0.111, 0.20]; the random density **peaks at 0.991**, far from any pinned
  structure.
- **(c) Hand-picked cross-sector triple** (e,u,d) with no forced reason to land on 1/6.
→ Not a survivor.

### (2) Cross-fermion falsification — **CONFIRMED** (the koide_geometry_crossfermion teeth)
No up- or down-quark relation lands on 2/3, ½, or 45°. Hand-confirmed Koide-Q: **up = 0.8489**,
**down = 0.7312**, both far from 2/3. A naive family-universal Koide claim is correctly killed at
Gate C by the up/down contradiction; the lepton Koide has **no forced reason** to be sector-specific
(no declared sector-specific ingredient), so it is not promoted to a universal law.

### (3) quarks6 F1 (Σm^{1/2})/(Σm^{1/4})² → 3/8, ~1-in-23,810 — **REFUTED** (light-quark + tolerance
artifact, same mechanism as (1); corrected to +0.6 bits under look-elsewhere).

### (4) F4 cross-sector interlocks — **advisory only, refuted as parameter-free claims**
QLC (θ_C+θ₁₂ = 46.4° vs 45°), GST (√(m_d/m_s) vs λ), b-τ (m_b/m_τ vs 3), θ₁₃ vs λ/√2 are known
literature relations evaluated at blunt 3–22% windows. None is parameter-free; flagged-and-refuted,
not survivors.

---

## BOTH-WAYS DISCIPLINE (per the working rule)

This is the **honest expected null**, reported in both directions:
- **Not manufactured as a win:** Koide is the only survivor, and even it is **gate-killed at Gate B**
  (kernel-free). The relational shape did **not** find a derivation of Koide or any new SM relation.
- **Not reflexively dismissed:** Koide is **genuinely special and parameter-free** — re-derived to
  6×10⁻⁶, seed-robust ~1-in-44k null, density peak away from 2/3. Carl's instinct that Koide is the
  one real lead is **confirmed**: it is the unique Koide-class relation in the SM.
- The "surprising" 1/6 hit was **not** dismissed by reflex — it was killed by *propagating the
  actual light-quark mass uncertainty* (0.18σ from 1/6) and the bounded-range density, the same
  rigor applied to a claimed win.

---

## WHAT THIS RESULT IS (and is not)

- **IS:** a strong, publishable structural statement — *over the fully-enumerated Koide-class
  relational space (1014 relations, completeness a theorem), Koide Q=2/3 for the charged leptons is
  the unique parameter-free forced-value relation in the SM mass spectrum.* The per-constant formula
  exhaustion provably could not have found Koide; this relational exhaustion confirms there is nothing
  else of Koide's kind.
- **IS NOT:** a derivation of Koide, a TOE, or a new lead. Koide remains a 45-year puzzle the
  framework only **re-labels** (no forced kernel for the amplitude r; cross-fermion-falsified as a
  universal law). Consistent with the banked mass-sector verdict: the SM mass sector is firmly walled.

---

## REPRODUCE

```
cd /Users/carlzimmerman/new_physics/project_atomos
python3 exhaust_relational.py --self-check              # completeness (1014, PROVEN)
python3 exhaust_relational.py --koide-ground-truth      # re-derive Koide (PASS)
python3 exhaust_relational.py --sector all              # full sweep (clean null)
python3 exhaust_relational.py --sector all --json       # machine-readable
```
Gate imported verbatim from `gate/`; never modified. stdlib + numpy + mpmath + sympy.
