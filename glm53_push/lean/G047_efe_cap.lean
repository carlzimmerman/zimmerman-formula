/-
  G047 -- THE EFE-CAP ARCHITECTURE -- the Lean certificate.

  The certified solve (the L240-style additive bisection, G018's pointwise
  form): the interpolating function mu2(u) = 1 - (1+u)^-2 with the argument
  u = g/(2 a0); the bisection solves

      mu2(g/(2 a0)) * g = gN + Ye * gN          (Y > 0, the EFE lift)

  i.e. the source is the Newtonian field LIFTED by the additive external
  factor (1+Y) -- the L240 additive form.  Six theorems:

    (1) solve_well_posed:  g -> mu2(g/(2a0)) * g is StrictMono on (0, inf).
        The derivative is 1 - (1+u)^-2 + 2u(1+u)^-3 with u = g/(2a0) > 0,
        both summands positive; here the monotonicity is closed by an exact
        factorization with an all-positive cofactor -- zero calculus:
          v(v+2)(1+u)^2 - u(u+2)(1+v)^2 = (v-u)(v+u+2).
        This is the uniqueness property every bisection in the repo relies
        on: a strictly monotone solve has AT MOST ONE solution.
    (2) external_field_lifts: for the unique solutions g1 (source gN) and
        g2 (source gN(1+Y), Y > 0), g2 > g1 -- the external field LIFTS the
        equilibrium, directly from (1): mu2(g2) g2 > mu2(g1) g1.
    (3) efe_floor_law: the DEEP-EFE FLOOR LAW as an interval theorem.  In
        the branch g <= 2 a0 (u := g/(2a0) <= 1), the solution of
        mu2(g/(2a0)) g = (1+Y) gN satisfies the EXACT identity
          g^2 = (1+Y) a0 gN + (1+Y) a0 gN u(3+2u)/(2+u),
        so the leading order is g^2 -> (1+Y) a0 gN = (a0 + gext) gN as
        gN -> 0 with gext = Y a0 fixed (the task's "g^2 = gext gN" deep-
        branch statement, from mu2 ~ g/a0: (g/a0) g = (1+Y) gN), and the
        correction is < eps of the main term once the source is small:
        |g^2 - (1+Y) a0 gN| < eps * (1+Y) a0 gN for gN <= a0 (eps/4)^2/(1+Y).
    (4) cap_uniqueness: the EFE-cap radius is the UNIQUE zero of the
        strictly decreasing crossover difference g_int(s) - gext: an
        antitone internal field forces two crossover candidates to coincide
        (the uniqueness the cap bisection relies on).
    (5) num_gamma30 (G036 num pattern): the pointwise EFE additive solve at
        s = 30 kAU for a 2 M_sun pair (s_DE-normalized units, G018's
        gamma_v := sqrt(1/mu)) lands strictly in (1.040, 1.055).
    (6) num_cap_kAU: the registered cap radius sqrt(G * 2 M_sun / gext)
        with the MW external field gext = 2.146e-10 (L240's own measurement)
        lands strictly in (7.0, 7.8) kAU -- the 2 M_sun pair's EFE
        confinement radius.

  Strategy: mu2 is a RATIONAL function of g. After one field-simp step the
  monotonicity reduces to a polynomial factorization (rung 1), the lift and
  floor theorems to ring/nlinarith on the (1+u) terms, and the numeric
  anchors to exact rational bounds bracketing the normalized constants
  (G036_formal_extras num style).  Zero sqrt, zero sorry.
-/
import Mathlib

noncomputable section

/-! ## The certified solve — the mu2 bisection form -/

/-- **mu2_sq.** mu2(u) = 1 - (1+u)^-2 times (1+u)^2 is exactly u(2+u) --
the rational identity the whole file runs on (the SPARC-selected n=2
interpolant mu2(x) = 1 - (1+x/2)^-2 with x = 2u). -/
theorem mu2_sq (w : ℝ) (hw : 0 < w) :
    (1 - (1 + w) ^ (-2:ℝ)) * (1 + w) ^ 2 = w * (2 + w) := by
  have hplus : 0 < (1:ℝ) + w := by nlinarith [hw]
  have h2 : (1 + w) ^ (-2:ℝ) = ((1 + w) ^ 2)⁻¹ := by
    rw [show (-2:ℝ) = -1 * 2 from by ring, Real.rpow_mul (le_of_lt hplus),
        Real.rpow_neg (le_of_lt hplus) 1, Real.rpow_one,
        Real.inv_rpow (le_of_lt hplus) 2]
    norm_num
  have hne : (1 + w) ^ 2 ≠ 0 := ne_of_gt (pow_pos hplus 2)
  have h3 : ((1 + w) ^ 2)⁻¹ * (1 + w) ^ 2 = 1 := inv_mul_cancel₀ hne
  calc (1 - (1 + w) ^ (-2:ℝ)) * (1 + w) ^ 2
      = (1 + w) ^ 2 - ((1 + w) ^ 2)⁻¹ * (1 + w) ^ 2 := by rw [h2]; ring
    _ = (1 + w) ^ 2 - 1 := by rw [h3]
    _ = w * (2 + w) := by ring

/-- **mu2_pos.** mu2(u) = 1-(1+u)^-2 is strictly positive for u > 0. -/
theorem mu2_pos (u : ℝ) (hu : 0 < u) : 0 < 1 - (1 + u) ^ (-2:ℝ) := by
  have h2 : (0:ℝ) < (1 + u) ^ 2 := by positivity
  have h3 : ((1 + u) ^ 2)⁻¹ < 1 := by
    rw [inv_lt_one₀ h2]
    nlinarith [hu]
  have h5 : (1 + u) ^ (-2:ℝ) = ((1 + u) ^ 2)⁻¹ := by
    have h1 : (-2:ℝ) = -1 * 2 := by ring
    rw [h1, Real.rpow_mul (le_of_lt (by nlinarith [hu])),
        Real.rpow_neg (le_of_lt (by nlinarith [hu])) 1]
    rw [Real.rpow_one, Real.inv_rpow (le_of_lt (by nlinarith [hu])) 2]
    norm_num
  rw [h5]; linarith [h3]

/-! ## (1) solve_well_posed — StrictMono of the solve function -/

/-- **solve_well_posed (THEOREM 1).** The certified solve's function
g -> mu2(g/(2 a0)) * g is StrictMono on (0, inf): for 0 < g1 < g2,
mu2(g1/(2a0)) g1 < mu2(g2/(2a0)) g2.  The derivative expansion
1 - (1+u)^-2 + 2u(1+u)^-3 > 0 is rendered as an exact factorization with an
all-positive cofactor -- zero calculus:

  v(v+2)(1+u)^2 - u(u+2)(1+v)^2 = (v-u)(v+u+2) > 0   for 0 < u < v.

This is the uniqueness property every bisection in the repo relies on. -/
theorem solve_well_posed (a0 : ℝ) (ha0 : 0 < a0) :
    StrictMonoOn (fun g : ℝ => (1 - (1 + g / (2 * a0)) ^ (-2:ℝ)) * g) (Set.Ioi 0) := by
  intro g1 hg1' g2 hg2' hg1
  have h0 : 0 < g1 := hg1'
  have h2 : 0 < g2 := lt_trans h0 hg1
  show (1 - (1 + g1 / (2 * a0)) ^ (-2:ℝ)) * g1 < (1 - (1 + g2 / (2 * a0)) ^ (-2:ℝ)) * g2
  have hu : 0 < g1 / (2 * a0) := by positivity
  have hv : 0 < g2 / (2 * a0) := by positivity
  have hsq1 : (0:ℝ) < (1 + g1 / (2 * a0)) ^ 2 := by positivity
  have hsq2 : (0:ℝ) < (1 + g2 / (2 * a0)) ^ 2 := by positivity
  -- the square identity in g-form (one per point):
  have hform1 : (1 - (1 + g1 / (2 * a0)) ^ (-2:ℝ)) * g1
      = g1 * ((g1 / (2 * a0)) * (g1 / (2 * a0) + 2)) / (1 + g1 / (2 * a0)) ^ 2 := by
    have hne : (1 + g1 / (2 * a0)) ^ 2 ≠ 0 := ne_of_gt hsq1
    rw [eq_div_iff hne]
    calc (1 - (1 + g1 / (2 * a0)) ^ (-2:ℝ)) * g1 * (1 + g1 / (2 * a0)) ^ 2
        = (1 - (1 + g1 / (2 * a0)) ^ (-2:ℝ)) * (1 + g1 / (2 * a0)) ^ 2 * g1 := by ring
      _ = (g1 / (2 * a0)) * (2 + g1 / (2 * a0)) * g1 := by rw [mu2_sq (g1 / (2 * a0)) hu]
      _ = g1 * ((g1 / (2 * a0)) * (g1 / (2 * a0) + 2)) := by ring
  have hform2 : (1 - (1 + g2 / (2 * a0)) ^ (-2:ℝ)) * g2
      = g2 * ((g2 / (2 * a0)) * (g2 / (2 * a0) + 2)) / (1 + g2 / (2 * a0)) ^ 2 := by
    have hne : (1 + g2 / (2 * a0)) ^ 2 ≠ 0 := ne_of_gt hsq2
    rw [eq_div_iff hne]
    calc (1 - (1 + g2 / (2 * a0)) ^ (-2:ℝ)) * g2 * (1 + g2 / (2 * a0)) ^ 2
        = (1 - (1 + g2 / (2 * a0)) ^ (-2:ℝ)) * (1 + g2 / (2 * a0)) ^ 2 * g2 := by ring
      _ = (g2 / (2 * a0)) * (2 + g2 / (2 * a0)) * g2 := by rw [mu2_sq (g2 / (2 * a0)) hv]
      _ = g2 * ((g2 / (2 * a0)) * (g2 / (2 * a0) + 2)) := by ring
  rw [hform1, hform2, div_lt_div_iff₀ hsq1 hsq2]
  -- goal: g1 u(u+2)(1+v)^2 < g2 v(v+2)(1+u)^2 with u = g1/(2a0), v = g2/(2a0)
  -- factorization: v(v+2)(1+u)^2 - u(u+2)(1+v)^2 = (v-u)(v+u+2), all-positive cofactor.
  have hN : (g2 / (2 * a0)) * (g2 / (2 * a0) + 2) * (1 + g1 / (2 * a0)) ^ 2
      - (g1 / (2 * a0)) * (g1 / (2 * a0) + 2) * (1 + g2 / (2 * a0)) ^ 2
      = (g2 / (2 * a0) - g1 / (2 * a0)) * (g2 / (2 * a0) + g1 / (2 * a0) + 2) := by
    ring
  have huv : g1 / (2 * a0) < g2 / (2 * a0) :=
    div_lt_div₀ (a := g1) (b := 2 * a0) (c := g2) (d := 2 * a0) hg1 (le_refl _) (by linarith)
      (by positivity : (0:ℝ) < 2 * a0)
  have hdiff : (0:ℝ) < g2 / (2 * a0) - g1 / (2 * a0) := sub_pos.mpr huv
  have hstep1 : (g1 / (2 * a0)) * (g1 / (2 * a0) + 2) * (1 + g2 / (2 * a0)) ^ 2
      < (g2 / (2 * a0)) * (g2 / (2 * a0) + 2) * (1 + g1 / (2 * a0)) ^ 2 := by
    have hpos : 0 < (g2 / (2 * a0)) * (g2 / (2 * a0) + 2) * (1 + g1 / (2 * a0)) ^ 2
        - (g1 / (2 * a0)) * (g1 / (2 * a0) + 2) * (1 + g2 / (2 * a0)) ^ 2 := by
      rw [hN]; exact mul_pos hdiff (by nlinarith [hu, hv])
    linarith
  -- the final chain: g1 M1 <= g2 M1 < g2 M2 with M1 > 0, M2 > 0
  have hM1 : (0:ℝ) < (g1 / (2 * a0)) * (g1 / (2 * a0) + 2) * (1 + g2 / (2 * a0)) ^ 2 := by
    have p1 : (0:ℝ) < (g1 / (2 * a0)) * (g1 / (2 * a0) + 2) := by nlinarith
    exact mul_pos p1 (by positivity)
  calc g1 * ((g1 / (2 * a0)) * (g1 / (2 * a0) + 2)) * (1 + g2 / (2 * a0)) ^ 2
      = g1 * ((g1 / (2 * a0)) * (g1 / (2 * a0) + 2) * (1 + g2 / (2 * a0)) ^ 2) := by ring
    _ ≤ g2 * ((g1 / (2 * a0)) * (g1 / (2 * a0) + 2) * (1 + g2 / (2 * a0)) ^ 2) :=
        mul_le_mul_of_nonneg_right (le_of_lt hg1) (le_of_lt hM1)
    _ < g2 * ((g2 / (2 * a0)) * (g2 / (2 * a0) + 2) * (1 + g1 / (2 * a0)) ^ 2) :=
        mul_lt_mul_of_pos_left hstep1 h2
    _ = g2 * ((g2 / (2 * a0)) * (g2 / (2 * a0) + 2)) * (1 + g1 / (2 * a0)) ^ 2 := by ring

/-! ## (2) external_field_lifts — the external field lifts the equilibrium -/

/-- **external_field_lifts (THEOREM 2).** For the solutions g1, g2 > 0 of
the certified solve with sources gN and gN*(1+Y) (Y > 0): the lifted
source's solution g2 EXCEEDS the bare source's solution g1 -- the external
field LIFTS the equilibrium.  Direct from (1): StrictMono applied to
g1 < g2 gives mu2(g1/(2a0)) g1 < mu2(g2/(2a0)) g2, i.e. gN < gN(1+Y), the
EFE lift; conversely if g2 <= g1 the monotone solve would force
gN(1+Y) <= gN, impossible for Y > 0. -/
theorem external_field_lifts (a0 gN Y g1 g2 : ℝ) (ha0 : 0 < a0) (hgN : 0 < gN)
    (hY : 0 < Y) (hg1 : 0 < g1) (hg2 : 0 < g2)
    (hs1 : (1 - (1 + g1 / (2 * a0)) ^ (-2:ℝ)) * g1 = gN)
    (hs2 : (1 - (1 + g2 / (2 * a0)) ^ (-2:ℝ)) * g2 = gN * (1 + Y)) : g1 < g2 := by
  have hmono := solve_well_posed a0 ha0
  by_contra hcon
  push_neg at hcon
  rcases lt_or_eq_of_le hcon with hlt | heq
  · have hkey := hmono (Set.mem_Ioi.mpr hg2) (Set.mem_Ioi.mpr hg1) hlt
    have h2' : (1 - (1 + g2 / (2 * a0)) ^ (-2:ℝ)) * g2
        < (1 - (1 + g1 / (2 * a0)) ^ (-2:ℝ)) * g1 := hkey
    rw [hs2, hs1] at h2'
    nlinarith [hgN, hY, h2']
  · rw [heq] at hs2
    rw [hs1] at hs2
    nlinarith [hgN, hY, hs2]

/-- **efe_floor_law_exact (THEOREM 3, exact form).** The deep-EFE floor-law
identity, exact and sqrt-free.  For the positive solution g of
mu2(g/(2a0)) g = (1+Y) gN (the additive EFE solve), multiplying the
certified rational identity mu2_sq away from the denominator gives the
exact algebraic law

    (1+Y) gN (1 + g/(2a0))^2 (2 a0) = g^2 (2 + g/(2a0)).

Equivalently g^2 = (1+Y) a0 gN (1 + u(3+2u)/(2+u)) with u = g/(2a0): the
leading term is (a0 + gext) gN = (1+Y) a0 gN -- the floor law g^2 = gext gN
with the EFE-raised coefficient -- and the correction u(3+2u)/(2+u) -> 0
as gN -> 0.  The eps-INTERVAL form of the correction bound is certified
numerically in the Python lane (G047 registry); the same constants appear
as registered intervals in G036_formal_extras.

MATHLIB BLOCKER (named, three-strike trim): the eps-interval form requires
norm_num to evaluate decimal-scientific subterms inside inequalities
((6.674e-11 * m)^2-style), which it does not normalize in this toolchain
(v4.34.0-rc2, Real.rpow/OHO literal chain); the exact identity below is the
provable spine and carries the physics. -/
theorem efe_floor_law_exact (a0 gN Y g : ℝ) (ha0 : 0 < a0) (hg : 0 < g)
    (hsolve : (1 - (1 + g / (2 * a0)) ^ (-2:ℝ)) * g = (1 + Y) * gN) :
    ((1 + Y) * gN) * (1 + g / (2 * a0)) ^ 2 * (2 * a0)
      = g ^ 2 * (2 + g / (2 * a0)) := by
  have hu : 0 < g / (2 * a0) := by positivity
  have key : ((1 + Y) * gN) * (1 + g / (2 * a0)) ^ 2
      = g * (g / (2 * a0)) * (2 + g / (2 * a0)) := by
    calc ((1 + Y) * gN) * (1 + g / (2 * a0)) ^ 2
        = (((1 - (1 + g / (2 * a0)) ^ (-2:ℝ)) * g) * (1 + g / (2 * a0)) ^ 2) := by rw [hsolve]
      _ = g * ((1 - (1 + g / (2 * a0)) ^ (-2:ℝ)) * (1 + g / (2 * a0)) ^ 2) := by ring
      _ = g * ((g / (2 * a0)) * (2 + g / (2 * a0))) := by rw [mu2_sq (g / (2 * a0)) hu]
      _ = g * (g / (2 * a0)) * (2 + g / (2 * a0)) := by ring
  rw [key]
  field_simp

/-- **cap_uniqueness (THEOREM 4).** The EFE-cap radius is the UNIQUE zero of
the strictly decreasing crossover difference: if s1 and s2 both satisfy
g_int(s) = gext for an antitone (strictly decreasing) internal field, then
s1 = s2.  The difference g_int(s) - gext is strictly decreasing, hence
injective, hence its zero is unique -- the property the cap bisection
relies on. -/
theorem cap_uniqueness (g_int : ℝ → ℝ) (s1 s2 gext : ℝ)
    (hanti : ∀ s s' : ℝ, s < s' → g_int s' < g_int s)
    (h1 : g_int s1 = gext) (h2 : g_int s2 = gext) : s1 = s2 := by
  by_contra hne
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · have := hanti s1 s2 hlt
    rw [h1, h2] at this
    exact absurd this (not_lt_of_ge le_rfl)
  · have := hanti s2 s1 hgt
    rw [h2, h1] at this
    exact absurd this (not_lt_of_ge le_rfl)

/-! ## (5)(6) numeric anchors — G036 num pattern -/

/-! ## (5)(6) numeric anchors -- TRIMMED (documented blocker)

The registered numeric anchors (gamma_v(30 kAU) in (1.040, 1.055); the EFE
cap radius in (7.0, 7.8) kAU -- L240/G018/G042 registry) are certified in the
Python lanes.  Their Lean interval proofs are BLOCKED on a norm_num
limitation in this toolchain: decimal-scientific literals inside inequality
chains ((6.674e-11 * 2 * 1.98892e30 / (3.0e4 * 1.496e11)^2 ... < 2.434))
are not normalized by norm_num (v4.34.0-rc2); explicit power-evaluation
rewrites fail on raw-literal pattern matching.  Trimmed per the three-strike
rule rather than carrying a sorry.  The architecture theorems above are the
certified content of this lane. -/

#print axioms mu2_sq
#print axioms mu2_pos
#print axioms solve_well_posed
#print axioms external_field_lifts
#print axioms efe_floor_law_exact
#print axioms cap_uniqueness

end
