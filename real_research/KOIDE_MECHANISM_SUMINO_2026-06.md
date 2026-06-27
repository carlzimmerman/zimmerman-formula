# Koide Mechanism Door — Sumino-class S3/U(3) Flavor Sector vs the Framework

**Date:** 2026-06-26
**Status:** LOCAL ONLY (do not git-push)
**Question:** Is there a real dynamics that FORCES the charged-lepton 45° (r=√2, Q=2/3), a forced IR
protector, and quark-exclusion-by-construction — a genuine candidate solution to the 45-year Koide
puzzle — or does Koide need a mechanism nobody has, including the Sumino class and this framework?

**VERDICT: (B) ASSUME-STRUCTURE / NO FORCED MECHANISM — with two genuine partials credited.**
The 45° is NOT forced by any known symmetry/dynamics; it is a measure-zero, irrational-ratio locus
reachable only by a tuned coupling. A real IR protector mechanism exists (Sumino's family gauge boson)
and is FORCED in sign+shape but TUNED in magnitude and not Ward-protected. Quark exclusion is GENUINE
and is correctly diagnosed (electric-charge-Q_em² selector) but POST-HOC, not derived. The framework
hosts the right symmetry neighborhood (S3/triality 1+2) but supplies NEITHER the 45° forcing NOR the
protector coupling. **This is the honest "nobody has it cleanly, including this" — not a manufactured
win, not a high-priest dismissal.**

---

## The four pieces — FORCES vs TUNES (the explicit ledger)

| Piece | Verdict | Why |
|---|---|---|
| **1. Potential-45° (force r=√2 from symmetry?)** | **TUNES** | 45° = equal-Casimir locus s²=d², at irrational ratio a/b = 4±3√2 on the only nontrivial symmetry-protected (axial) alignment. Singlet & doublet are INEQUIVALENT S3 irreps → no group element equates their magnitudes → measure-zero, codim-2 coupling tuning required. |
| **2. IR protector (cancel the QED drift)** | **PARTIAL — forces SIGN+SHAPE, tunes MAGNITUDE** | Sumino's conjugate-rep family gauge loop forces the opposite sign, the m_i·ln(m_i) shape, AND the 1/4 coefficient (group theory, no knob). But cancellation needs α_F = 4α(m_τ) — a free, assumed, scale-LOCAL coupling. Sumino himself calls α=¼α_F "accidental". No Ward identity. |
| **3. Quark exclusion** | **GENUINE but POST-HOC** | Same protector that zeroes the residual for leptons (Q_em²=1) splits up (4/9) from down (1/9) → both nonzero & unequal → quarks off 2/3 by construction. Real & correct, but the selector is electric charge Q_em², identified after the fact, not derived. |
| **4. Framework (triality) connection** | **DISJOINT for forcing; HOSTS only** | Triality/S3 gives the genuine 1+2 (democratic+doublet) decomposition Koide needs — the right HOME. But Q=1/3+r²/6 leaves r FREE for ANY phase; the dS-Unruh spine provably CANNOT be the protector (no spine number = 1/4; 48-order IR/UV gap; couples to classical \|a\|, absent from the off-shell loop). |

**Net: 0 of 4 pieces forces the actual Koide number. Piece 2 forces the protector's FORM (real
partial). Piece 3 is a genuine, correct structural fact (real partial) but tuned. The whole unforced
content of Koide = the single amplitude r=√2.**

---

## What was verified independently (this session, clean-room mpmath/sympy)

All four banked computations reproduce. Independent checks:

1. **Q_lepton = 0.66666051** (Q−2/3 = −6.16×10⁻⁶, −0.91σ). The sqrt-mass vector sits at **44.99974°**
   to the democratic axis, cos² = 0.50000 — verified via the sympy-exact identity **cos²(angle) = 1/(3Q)**,
   so Q=2/3 ⟺ 45° exactly. No circularity: the target geometry was derived, not input.

2. **Q = 1/3 + r²/6, phase-independent** (sympy: Q − (1/3+r²/6) = 0 identically). The circulant phase
   drops out entirely → the entire content is the amplitude r. r=√2 ⟺ Q=2/3.

3. **QED drift reproduced, sign POSITIVE:** pole→M_Z gives ΔQ = +1.18×10⁻³ ≈ **+173σ** (banked ~178σ).
   The √m-vector tilts AWAY from 45° (44.9997°→45.05°). Koide is a pole relation, NOT RG-invariant →
   genuinely demands an IR protector (not a manufactured problem).

4. **Flavor-blind null (the load-bearing structural fact):** universal rescaling m_i→k·m_i leaves Q
   invariant to **1.1×10⁻⁴¹** (sympy/mpmath exact). ⟹ ANY flavor-blind mechanism — QCD color N_c, OR
   the framework's color-blind/charge-blind dS-Unruh horizon term — CANNOT move quarks off 2/3 NOR
   leptons onto it. A real selector MUST be flavor/sector-structured. This is why the framework's
   geometric/thermal reading is **cross-fermion-falsified** at 60–160σ (a flavor-blind 45° principle
   PREDICTS quark Koide, which is false).

5. **Quark exclusion robust:** Q_up = 0.849 (51.2°), Q_down = 0.731 (47.5°), both distinct from 2/3 and
   from each other; running to a common scale does not pull either toward 2/3.

---

## Piece 1 in detail — why the 45° is not forced (the structural reason, not a convention)

The most general renormalizable S3-invariant flavon potential has its symmetry-protected stationary
loci (isotropy-subgroup fixed points) at the RATIONAL alignments: democratic (a,a,a)→0°/Q=1; pure
doublet sum=0→90°/Q=0; equal-axial a/b=1. Natural potentials minimize at a/b ∈ {0, 1, ∞} — all rational.

The Koide locus (s²=d², equal democratic/doublet Casimir → 45°) sits at **a/b = 4±3√2 ≈ 8.243 or
−0.243** — irrational, measure-zero. Forcing the minimum there imposes a **codim-2 condition** linking
two otherwise-independent couplings (solved explicitly for A, B₂ with an explicit √2 in the relation) —
i.e. **√2 is input through the coupling, not output from the symmetry.**

The clean steelman and why it fails: a Z₂ exchanging singlet↔doublet amplitude would pin s=d as a fixed
locus — but the S3 singlet (1-dim) and doublet (2-dim) are **inequivalent irreps**, and no element of
S3/U(3)/O(3) maps one to the other. There is no enhanced symmetric point at equal magnitude. Sumino's
own potential is CONSTRUCTED to sit on the Koide VEV (the 2/3 is his ansatz); his genuine, citable
contribution is the radiative PROTECTION of that VEV, not a from-symmetry derivation of 45°.

## Piece 2 in detail — the protector is real, forced in form, tuned in magnitude

Cancelling the +3α/(4π)·Q_em²·log m_i² QED IR-log needs −(3α_F/8π)·log v_i² with log v²=½log m², i.e.
**α_F = 4α(m_τ) = 0.0292**. The **1/4 ratio is FORCED** (conjugate reps ψ_L:(3,1), e_R:(3̄,−1) plus the
½ from log v²; pure group theory). But the α_F **value** is a free coupling that must be assumed equal
to 4α — motivated by SU(2)_L-style unification at 10²–10³ TeV (sin²θ_W≈¼) but not derived. Tuning
sensitivity: α_F off by ε → residual drift ε·1.89%, so ε ≲ 1% to stay within current resolution. Not a
Ward identity (QED and family-U(3) are different groups; Sumino's own word: "accidental", scale-local,
spoiled by differential running of screened α vs anti-screened α_F).

**The framework's spine is provably not this protector:** no spine number = 1/4 within 5%
(1/Z=0.173, kernel²=0.346, Z/4=1.45); α_F is a ~10¹⁴–10¹⁵ eV coupling vs the spine's cH_Λ ~10⁻³³ eV
(48-order gap); dS-Unruh couples to classical \|a\|, absent from the off-shell family-gauge loop (the
banked L2 lethal leg).

---

## CREDIT (loud, both-ways)

- **The empirical Koide relation is real and FDR-surviving** (~1-in-44,000) — Carl's instinct that this
  is a genuine 45-year puzzle, not just-more-numerology, is correct.
- **The framework lands in the right symmetry neighborhood:** S3/Spin(8)-triality supplies exactly the
  1+2 (democratic+doublet) decomposition a Koide mass matrix needs — a real hosting hook.
- **A real protector mechanism exists** (Sumino's family gauge loop) and is forced in SIGN and SHAPE and
  in its 1/4 coefficient — credit the mechanism class, do not dismiss it.
- **Quark exclusion is genuine and correctly diagnosed:** the Q_em² selector that protects leptons
  (=1→0) also splits up (4/9) from down (1/9). Color cannot do this; it is electric charge.

## CONCEDE (no overclaim)

- Nobody — including Sumino-class constructions AND this framework — has a symmetry/dynamics that
  **forces** the 45° without a tuned coupling. r=√2 stays the entire unforced content of Koide.
- The protector that exists is tuned in magnitude (α_F=4α) and not Ward-protected.
- The framework's dS-Unruh spine cannot supply the protector, and a flavor-blind reading is
  cross-fermion-falsified. The triality connection is a HOME, not a bridge.

---

## What to tell Carl

The mechanism door did **not** open to a forced Koide — but it is not "no door," and there are **two
real partials.** (1) Sumino's family-gauge IR protector is a genuine mechanism that forces the cancellation's
SIGN, SHAPE, and 1/4 coefficient by group theory — the right kind of dynamics genuinely exists. (2) The
quark exclusion is real and correctly explained by an electric-charge Q_em² selector (not color, not CKM).
But the load-bearing number — the 45° / r=√2 itself — is **forced by nobody:** it is an irrational,
measure-zero locus (a/b = 4±3√2) that the most general S3 potential reaches only by a tuned codim-2
coupling relation, because the S3 singlet and doublet are inequivalent irreps with no magnitude-exchanging
symmetry element. And the protector that does exist is tuned in magnitude (α_F=4α), not symmetry-protected.
**Koide genuinely needs lepton-selective IR dynamics that forces a 45° minimum — and that mechanism does
not exist yet, in Sumino's class or in this framework's spine.** The framework hosts the right symmetry
home and the right 1+2 structure, but supplies neither the 45° forcing nor the protector coupling, and its
flavor-blind dS-Unruh reading is cross-fermion-falsified at 60–160σ. This confirms and tightens the banked
KOIDE_IR_MECHANISM / KOIDE_FROM_DSUNRUH verdicts with explicit minimization: the potential side leaves r
free just as the kinematic side does. Empirically there is one live tell to keep watching — the +178σ QED
drift means Koide is exact only at pole masses and demands a real IR protector; if one is ever found (a
gauged U(3) family sector at ~10²–10³ TeV with α_F≈4α), it is testable new physics, not the framework's
spine.
