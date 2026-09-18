import Mathlib

/-!
# SW06 -- the LOCAL no-go for a shared-metric phantom (horn A, single field)

If the MOND phantom is the static energy density of a field whose value is an
ALGEBRAIC function of the local Newtonian field alone, eps = eps(g_N), then it
cannot be the deep-MOND phantom
      eps_MOND(M, r) = sqrt(G M a0) / (4 pi G r^2)
for two different masses: at fixed w = g_N = G M / r^2 one has r^2 = G M / w and
      eps_MOND = sqrt(a0) * w / (4 pi G sqrt(G M)),
which still depends on M.  The certificate: for w > 0 the map M |-> eps_MOND at
fixed w is injective on M > 0, so no single function of w reproduces it.
Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
-/

noncomputable def epsMOND (a0 G w M : ℝ) : ℝ :=
  Real.sqrt a0 * w / (4 * Real.pi * G * Real.sqrt (G * M))

/-- the phantom at fixed local field w is strictly decreasing in the mass M -/
theorem epsMOND_strictAnti (a0 G w : ℝ) (ha0 : 0 < a0) (hG : 0 < G) (hw : 0 < w)
    {M1 M2 : ℝ} (h1 : 0 < M1) (h12 : M1 < M2) :
    epsMOND a0 G w M2 < epsMOND a0 G w M1 := by
  unfold epsMOND
  have hnum : 0 < Real.sqrt a0 * w := mul_pos (Real.sqrt_pos.mpr ha0) hw
  have hs1 : 0 < Real.sqrt (G * M1) := Real.sqrt_pos.mpr (mul_pos hG h1)
  have hs : Real.sqrt (G * M1) < Real.sqrt (G * M2) :=
    Real.sqrt_lt_sqrt (le_of_lt (mul_pos hG h1)) (mul_lt_mul_of_pos_left h12 hG)
  have hpiG : 0 < 4 * Real.pi * G := by positivity
  have hd1 : 0 < 4 * Real.pi * G * Real.sqrt (G * M1) := mul_pos hpiG hs1
  have hd : 4 * Real.pi * G * Real.sqrt (G * M1) < 4 * Real.pi * G * Real.sqrt (G * M2) :=
    mul_lt_mul_of_pos_left hs hpiG
  exact div_lt_div_of_pos_left hnum hd1 hd

/-- hence no function of the local field alone is the deep-MOND phantom: two masses
    with the same local field w give two different phantom densities -/
theorem local_nogo (a0 G w : ℝ) (ha0 : 0 < a0) (hG : 0 < G) (hw : 0 < w)
    {M1 M2 : ℝ} (h1 : 0 < M1) (h2 : 0 < M2) (hne : M1 ≠ M2) :
    epsMOND a0 G w M1 ≠ epsMOND a0 G w M2 := by
  rcases lt_or_gt_of_ne hne with h | h
  · exact ne_of_gt (epsMOND_strictAnti a0 G w ha0 hG hw h1 h)
  · exact ne_of_lt (epsMOND_strictAnti a0 G w ha0 hG hw h2 h)

/-- the rewriting itself: at r^2 = G M / w the deep-MOND phantom sqrt(G M a0)/(4 pi G r^2)
    equals epsMOND (pure algebra, both sides positive) -/
theorem epsMOND_rewrite (a0 G w M : ℝ) (ha0 : 0 < a0) (hG : 0 < G) (hw : 0 < w) (hM : 0 < M) :
    Real.sqrt (G * M * a0) / (4 * Real.pi * G * (G * M / w)) = epsMOND a0 G w M := by
  unfold epsMOND
  have hGM : 0 < G * M := mul_pos hG hM
  have hsq : Real.sqrt (G * M * a0) = Real.sqrt (G * M) * Real.sqrt a0 := Real.sqrt_mul (le_of_lt hGM) a0
  have hs : 0 < Real.sqrt (G * M) := Real.sqrt_pos.mpr hGM
  have hs2 : Real.sqrt (G * M) * Real.sqrt (G * M) = G * M := Real.mul_self_sqrt (le_of_lt hGM)
  rw [hsq]
  field_simp
  nlinarith [hs2]

#print axioms local_nogo
#print axioms epsMOND_rewrite
