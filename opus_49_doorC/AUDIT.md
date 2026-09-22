# AUDIT — the deepseek lane's lattice strong-coupling claims (YM05, YM07, I15)

Auditor: opus_49_doorC (independent). Scope: correctness of the constants against the
lane's own derivations and the physics literature, and against the certified I15 formula.
Gate: SU(2) gap at g²=2 should be 1, SU(3) should be 7/3, thresholds sqrt(8/3) and 3/2.

**Machinery used.** (i) Re-ran `YM05_lattice_gap.py` and `YM07_uniform_gap.py` from copies
in /tmp (lane tree untouched): **YM05 16/16 PASS, YM07 15/15 PASS** — the recorded counts
reproduce. (ii) Compiled the Lean certificates against the repo's Mathlib build
(v4.34.0-rc2, `fable_independent_2026/lean_2026`): `I15_suN_lattice_gap.lean` **exit 0**,
`YM05_lattice_gap.lean` **exit 0**, `YM07_uniform_gap.lean` **exit 0** — all theorems carry
only the standard axioms (propext, Classical.choice, Quot.sound; no sorry). (iii) Re-derived
every constant symbolically and numerically (see `verify_doorC.py`; run here: 15/15 PASS).

## 1. Verdict on the gate constants: PASS (all eight)

| Item | Lane value | Literature / certified | Verdict |
|---|---|---|---|
| C_F(SU(2)) | 3/4 | (N²−1)/2N = 3/4 (standard; Lane Part A1 constructs sum t_a²=¾I from σ_a/2) | ✓ |
| C_F(SU(3)) | 4/3 | (N²−1)/2N = 4/3 (Lane A2 constructs sum t_a²=(4/3)I from λ_a/2) | ✓ |
| E_loop | (g²/2)·4·C_F = 2xC_F | single plaquette: four links, each (x/2)C₂; E₁(H_E)=2xC_F (PROOF.md §3); SU(2)=3x/2, SU(3)=8x/3 | ✓ |
| |tr U| ≤ N, |Re tr U| ≤ N | unit-circle spectrum + triangle inequality (standard) | ✓ |
| Δ_SU2(2) | 1 | 3·2/2 − 4/2 = 1 = (N²−2)/N\|_{N=2} (I15 `gap_at_two`) | ✓ |
| Δ_SU3(2) | 7/3 | 8·2/3 − 6/2 = 7/3 = (N²−2)/N\|_{N=3} | ✓ |
| x*_SU2 | sqrt(8/3) ≈ 1.633 | 3x/2 = 4/x ⇔ x² = 8/3 | ✓ |
| x*_SU3 | 3/2 | 8x/3 = 6/x ⇔ x² = 9/4 | ✓ |

All eight gate values are reproduced symbolically, and they agree with the certified
general-N formula `gap_N(x) = x(N²−1)/N − 2N/x`, `gap_N(2)=(N²−2)/N` (I15). The lane's
application of the Casimir (fundamental of SU(N)), the 4-link plaquette loop energy, and the
unitary trace bound — the three literature inputs the task names — are correct and standard.

## 2. Finding A — a normalization mismatch in the lane text (minor; not a numerical error)

The lane's displayed Hamiltonian (YM05.py header, YM05.lean scope note) has magnetic
coefficient **2/g²** (i.e. β=b_N=2 in `H_B=(β/x)(1−T)`), but the gap polynomials use the
bound **2N/x** (4/x for SU(2), 6/x for SU(3)):

- For SU(2) both readings coincide at the norm level: ‖H_B‖ ≤ (2/x)·2 = 4/x = 2N/x, so the
  mismatch is **masked**.
- For SU(3) they differ: with β=2 the correct bound is 8x/3 − 4/x (threshold sqrt(3/2)≈1.225,
  value at x=2: 10/3), whereas the lane's and gate's 8x/3 − 6/x requires β=3, i.e. the
  coefficient **N/g²**. So the gate constants 7/3 and 3/2 match the convention "magnetic
  bound 2N/x (β=N)", not the display "β=2".

This is *exactly what the I15 operator proof already registered*: PROOF.md §1/§5 notes that
for the displayed b_N=2 the sharper bound is `2x C_F − b_N/x`, giving 2 (SU(2)) and 13/3
(SU(3)) at x=2, and states plainly that **the values 1 and 7/3 are lower bounds, not exact
gaps, and are not the sharpest statement for the displayed normalization**. The correct
reading: the certified constants are valid lower bounds under the 2N/x (b_N=N) convention;
the lane notebook's β=2 display is inconsistent with that convention. **Audit: arithmetic
PASS; notation/convention mismatch in the lane text (already flagged on the corrected
record). No number in the certified set is wrong.**

## 3. Finding B — YM07: arithmetic perfect, operator premise superseded

YM07's uniform-gap diverges from YM05 only in the *window* (x ≥ 8 instead of x ≥ 2) and the
*bound shape* (κ = 2N·n_inf instead of 2N): it claims a volume-independent strong-coupling
gap at x ≥ 8 via per-loop **localization** of the magnetic deficit (n_inf = 1 + 4(2d−3) = 13
counted; worst-case ceiling 18) with the extensive vacuum magnetic shift **cancelling**.

Audited arithmetic: all reproduces. Worst-case Lean window: 3x/2 − 72/x > 0 on x ≥ 8
(anchor 3), 8x/3 − 108/x > 0 on x ≥ 8 (anchor 47/6); counted κ=52: 3x/2 − 52/x (anchor 11/2
at x=8); counted thresholds sqrt(104/3)≈5.89, sqrt(117/4)≈5.41 — all below 8. The polynomials
are increasing on x>0; the window statement is true and conservative. `verify_doorC.py` §B.

The *operator status*, however: the repo's corrected R4 (2026-09-22) and PROOF.md §5 state
that YM07's route — comparison against the bare electric vacuum with per-loop localization
and exact cancellation of the extensive shift — **"requires a new argument for the dressed
vacuum; it is not used here."** The corrected many-plaquette theorem is instead the
Yarotsky application (gap ≥ 3x/16 for x ≥ X_d, X_d unvalued). Consequently:

> **YM07's explicit x ≥ 8 uniform window is arithmetic that is certified (Lean exit 0) but
> whose operator premise is registered-not-endorsed on the corrected record.** Treat YM07's
> numbers as scalar constants (all correct); do not cite its x ≥ 8 thermodynamic-limit gap
> as a certified operator theorem. The certified many-plaquette statement is PROOF.md §4
> (Yarotsky, gap ≥ 3x/16, x ≥ X_d, X_d not numerically evaluated).

(Note: the lone "FAIL" string in YM07's output is inside a check *reading* describing the
extensive-norm objection; the check itself passes — 15/15.)

## 4. Finding C — "1 and 7/3 are bounds, not the gaps": now quantified

With the exact Jacobi representation (LEMMA_doorC.md L1) the true single-plaquette SU(2)
gap is computable: at x=2, β=2 the exact gap is **3.114**, and numerically min over all
x>0 is 2.196 at x≈0.99. So the certified 1 (2N/x convention) and 2 (min–max β/x convention)
are both strictly conservative. This is consistent with (not a correction of) PROOF.md's
statement that the certified numbers are lower bounds; the audit adds the honest magnitude.

## 5. Literature cross-check (the three named inputs)

- **Casimir of the fundamental of SU(N):** C_F = (N²−1)/(2N) — standard (tr(t_a t_b) =
  δ_ab/2 normalization), verified by the lane's explicit matrix construction for SU(2)/SU(3)
  and by the all-N minimization in PROOF.md §2. ✓
- **4-link plaquette loop energy:** four fundamental links × (x/2)C₂ = 2xC_F — standard
  single-loop reduction (cf. PROOF.md §3; Ligterink–Walet–Bishop hep-lat/0001028). ✓
- **Unitary trace bound |tr U| ≤ N:** unit-modulus spectrum + triangle inequality,
  standard. ✓

## 6. Bottom line

- **All gate constants: correct** (machine-verified: scripts rerun 16/16 and 15/15; three
  Lean certificates compile exit 0 with only the standard axioms; 15/15 symbolic rechecks).
  SU(2)=1, SU(3)=7/3 at g²=2, thresholds sqrt(8/3) and 3/2 — all reproduced and all
  consistent with the certified general-N formula.
- **Two registrations for the record:** (A) the lane's β display vs the 2N/x bound used is a
  convention mismatch (masked for SU(2), visible for SU(3)); the correct sharpest single-
  plaquette line for b_N=2 is 3x/2 − 2/x (SU2), 8x/3 − 2/x (SU3), as PROOF.md already records.
  (B) YM07's operator premise (localization + shift cancellation vs the bare electric vacuum)
  is superseded on the corrected record; its arithmetic is correct but its x ≥ 8 uniform
  window is not the certified many-plaquette theorem.
- **No fake constants found; no incorrect certified number found.** The certified R4 numbers
  are lower bounds on a single-plaquette model, exactly as R4 now claims.