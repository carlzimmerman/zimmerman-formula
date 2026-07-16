# ONE-LOOP FINITE PARTS — VERIFICATION LEDGER
All scripts in this directory. Rerun: `for f in finite_D1_selfenergy finite_D2_quasistatic_dnu
finite_protection_theorem finite_checks_sumrule_positivity finite_scheme_independence; do
python3 $f.py; echo "EXIT=$?"; done`. All exit 0. **37 PASS / 0 FAIL.**

## Scripts and what each proves-by-moving-the-number
| script | exit | checks | load-bearing verifications |
|---|---|---|---|
| `finite_D1_selfenergy.py` | 0 | 8 | a₁=2H², a₂=29/15 H⁴ on dS; flat H→0 limit = CW route (m²/16π²)(ln−1); H-part O(H²/m²); D1 shape-uniform; δν≡0 all y*; both footings |
| `finite_D2_quasistatic_dnu.py` | 0 | 8 | μ-indep piece (m⁴/64π²)(1+sW)²ln(1+sW); linear coeff=1 absorbed, residual (3/2)W²; Fork P ~2.8e38 (proxy), Fork C ~1e-86; anchor+footing spread ≤1e-96 |
| `finite_protection_theorem.py` | 0 | 8 | (a) mult-op dV/dp=0 vs disformal dV/dp≠0; (b) dS-const ⇒ z-indep; (c) K(0)=0 + geodesy ⇒ linear vertex zero; theorem holds; breakage (ii) (q0/m)²~5e-86 |
| `finite_checks_sumrule_positivity.py` | 0 | 8 | sum rule=1 (+ control breaks it); Im L≥0 (+ control drives negative); KMS balance=0 both footings (+ pump control fires) |
| `finite_scheme_independence.py` | 0 | 5 | d³V/d(M²)³=1/(32π²M²) in dim-reg AND proper-time cutoff (all M², all Λ); nonanalytic coeff = m⁴(1+sW)²/64π²; scheme diff analytic |

## Non-vacuity: the three live negative controls (item-4 requirement)
Each invariant check is paired with a perturbed input that MUST fail — verified it does:
1. **Sum rule** ∫dμ/|t|: real = 1.000000 (PASS); ρ×1.1 → 1.100000 (**control fires**).
2. **KL positivity** Im L(A<0): real all ≥0 (PASS); sign-flip measure on |t|∈(1,10) →
   Im L(−10) = −1.5550 < 0 (**control fires**).
3. **KMS detailed balance** Gp(−w)/Gp(w)·e^{βw}: real |ratio−1| = 0 (PASS); pumped leg →
   |ratio−1| ~ 1.5e+08 (**control fires**), both footings.
A hard-coded pass could not distinguish real from perturbed; these can, so the checks are real.

## Base facts re-verified against the frozen repo (READ-ONLY, not trusted)
- Measure additive constant a = 0.65411134, sum rule ∫dμ/|t| = 1, K(0)=0 —
  `oneloop_laneA_divergences.py` (banked; SETUP.md re-run log).
- Frame self-energy Γ₁ = (1/2)Tr ln[−□+m²(1+sW)], W local multiplication operator; linear
  vertex zero (geodesy); counterterm list {O_vac, O_W, O_WW, O_RW}, no a0 counterterm —
  same file.
- CW boundedness / dS IR floor 3H/2 / finite form factor — `twoloop_laneA_finite.py`
  (the misnamed ONE-loop finite lane); this workflow extends it to the δν extraction it
  explicitly left open (its lines 348-349).

## HONESTY FLAG (independently confirmed by direct read)
`open_doors_2026_07/mi_oneloop_tt_vertex_all_n.py` (commit e37c7144) lines 56 and 66 are
literally `check("delta(u_0)=0 for TT", True)` and
`check("V^(1)=0 for all n (TT decoupling theorem)", True)` — **hard-coded True**. The
"TT-vertex-zero at ALL orders n" is therefore a printed argument, **CAS-verified only n=1,2**
(in laneB). Any claim leaning on all-n TT decoupling (graviton-loop protection leg iv) is
downgraded accordingly and left out of scope.

## Scope honesty
- ρ_m = m²φ² is a proxy; Fork P's catastrophe is about the proxy, Fork C is the physical read.
- W(y)=1/(1+y) in the δν(y) plot is a labeled illustration; the observability verdict is
  map-independent (prefactor-set).
- Not closed: disformal ρ_m variant, finite two-loop parts, all-n TT graviton protection,
  T_μν metric variation. s, a0, Z remain inputs.
