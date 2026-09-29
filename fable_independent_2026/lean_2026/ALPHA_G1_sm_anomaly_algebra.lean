import Mathlib

/-!
# M2_01 -- Lean certificate for the anomaly-cancellation algebra of lane G1
Source lane: real_research/alpha_principle_2026/G_topological_anomaly/g1_anomaly_charges.py
(checks A1a-A1d, A2a-A2b, A3a, A4a-A4e, A5a-A5b).  Nothing in the repo's Lean corpus certifies this
(`git grep -i anomaly -- '*.lean'` returns only unrelated hits: I01_bhstar_wave.lean "anomaly window", AS045).

CERTIFIED (pure mathematics, real numbers, one generation of left-handed Weyl fermions
Q(Nc,2) U(Nc,1) D(Nc,1) L(1,2) E(1,1) with hypercharges yQ yU yD yL yE and Nc colours):
* `lin_consequences`: the SU(Nc)^2 U(1), SU(2)^2 U(1) and grav^2 U(1) equations force
  yL = -Nc yQ, yD = -2 yQ - yU, yE = 2 Nc yQ  (no hypothesis on Nc).
* `cubic_factorisation`: on that linear solution the cubic U(1)^3 anomaly equals
  6 Nc yQ (Nc^2 yQ^2 - (yQ + yU)^2).
* `anomaly_solution_set` (Nc /= 0): the four equations hold IFF the linear relations hold and
  (yQ = 0  or  yU = (Nc-1) yQ  or  yU = -(Nc+1) yQ) -- exactly the three families sympy printed.
* `sm_solution`: the Standard-Model values (x6: 1, -4, 2, -3, 6) at Nc = 3 solve all four equations.
* `no_singlet_no_solution`: with yE = 0 there is no solution with yQ /= 0 (the script's MUTATE control).
* homogeneity: the three linear equations scale like lambda, the cubic like lambda^3 (`anom_homogeneous`),
  and (y -> lambda y, g -> g/lambda) leaves every matter coupling g y invariant
  (`coupling_rescaling_invariant`): the overall coupling normalisation is NOT fixed by anomalies.
* charge lattice with Q_em = T3 + y/(2 Nc) at yQ = 1: q_u = 1/2 + 1/(2Nc), q_d = q_u - 1, the conjugates
  carry -q_u, -q_d, proton charge ((Nc+1)/2) q_u + ((Nc-1)/2) q_d = 1 for every Nc, and Nc = 3 gives 2/3, -1/3.
* `with_nuR_cubic`: adding a singlet nu_R (yN) at Nc = 3, on the 3-dimensional linear solution space the
  cubic equals 18 a0 (2 a0 - a2 - a5)(4 a0 + a2 - a5); `BL_Y_span_solves`: every combination
  a Y + b (B-L) solves all four equations (coupling ratio g_Y/g_{B-L} not fixed).
NOT CERTIFIED: that the SM content is the true content (empirical), that the u<->d swapped branch is excluded
(the lane says that is a Yukawa/Higgs statement, not an anomaly one), anything about the value of alpha.
This is a negative-result algebra: it shows the anomaly conditions fix RATIOS of hypercharges and leave one
overall scale (hence alpha) free.  kappa = 1/2 is not involved.
-/

namespace M2Anomaly

/-- the four anomaly equations for one generation, Nc colours -/
def e3 (yQ yU yD : ℝ) : ℝ := 2 * yQ + yU + yD
def e2 (Nc yQ yL : ℝ) : ℝ := Nc * yQ + yL
def eg (Nc yQ yU yD yL yE : ℝ) : ℝ := 2 * Nc * yQ + Nc * yU + Nc * yD + 2 * yL + yE
def ec (Nc yQ yU yD yL yE : ℝ) : ℝ :=
  2 * Nc * yQ ^ 3 + Nc * yU ^ 3 + Nc * yD ^ 3 + 2 * yL ^ 3 + yE ^ 3

theorem lin_consequences (Nc yQ yU yD yL yE : ℝ)
    (h3 : e3 yQ yU yD = 0) (h2 : e2 Nc yQ yL = 0) (hg : eg Nc yQ yU yD yL yE = 0) :
    yL = -Nc * yQ ∧ yD = -2 * yQ - yU ∧ yE = 2 * Nc * yQ := by
  unfold e3 e2 eg at *
  have hL : yL = -Nc * yQ := by linarith
  have hD : yD = -2 * yQ - yU := by linarith
  refine ⟨hL, hD, ?_⟩
  have : yE = -2 * yL - Nc * (2 * yQ + yU + yD) := by linarith
  rw [this, hL]
  have h3' : 2 * yQ + yU + yD = 0 := h3
  rw [h3']; ring

theorem cubic_factorisation (Nc yQ yU : ℝ) :
    ec Nc yQ yU (-2 * yQ - yU) (-Nc * yQ) (2 * Nc * yQ)
      = 6 * Nc * yQ * (Nc ^ 2 * yQ ^ 2 - (yQ + yU) ^ 2) := by
  unfold ec; ring

/-- complete solution set of the four anomaly equations (any Nc /= 0) -/
theorem anomaly_solution_set (Nc yQ yU yD yL yE : ℝ) (hNc : Nc ≠ 0) :
    (e3 yQ yU yD = 0 ∧ e2 Nc yQ yL = 0 ∧ eg Nc yQ yU yD yL yE = 0 ∧ ec Nc yQ yU yD yL yE = 0) ↔
    (yL = -Nc * yQ ∧ yD = -2 * yQ - yU ∧ yE = 2 * Nc * yQ ∧
      (yQ = 0 ∨ yU = (Nc - 1) * yQ ∨ yU = -(Nc + 1) * yQ)) := by
  constructor
  · rintro ⟨h3, h2, hg, hc⟩
    obtain ⟨hL, hD, hE⟩ := lin_consequences Nc yQ yU yD yL yE h3 h2 hg
    refine ⟨hL, hD, hE, ?_⟩
    have hc' := hc
    rw [hL, hD, hE, cubic_factorisation] at hc'
    have hprod : (6 * Nc) * (yQ * ((Nc * yQ - (yQ + yU)) * (Nc * yQ + (yQ + yU)))) = 0 := by
      nlinarith [hc']
    have h6 : (6 * Nc) ≠ 0 := mul_ne_zero (by norm_num) hNc
    have hp := (mul_eq_zero.mp hprod).resolve_left h6
    rcases mul_eq_zero.mp hp with h | h
    · exact Or.inl h
    · rcases mul_eq_zero.mp h with h | h
      · right; left; linarith
      · right; right; linarith
  · rintro ⟨hL, hD, hE, hcase⟩
    refine ⟨?_, ?_, ?_, ?_⟩
    · unfold e3; rw [hD]; ring
    · unfold e2; rw [hL]; ring
    · unfold eg; rw [hL, hD, hE]; ring
    · rw [hL, hD, hE, cubic_factorisation]
      rcases hcase with h | h | h
      · rw [h]; ring
      · rw [h]; ring
      · rw [h]; ring

/-- Standard Model hypercharges (x6) at Nc = 3 solve all four equations. -/
theorem sm_solution :
    e3 1 (-4) 2 = 0 ∧ e2 3 1 (-3) = 0 ∧ eg 3 1 (-4) 2 (-3) 6 = 0 ∧ ec 3 1 (-4) 2 (-3) 6 = 0 := by
  unfold e3 e2 eg ec; norm_num

/-- the u <-> d swapped branch also solves them (excluded only by Yukawa/Higgs structure) -/
theorem sm_swapped_solution :
    e3 1 2 (-4) = 0 ∧ e2 3 1 (-3) = 0 ∧ eg 3 1 2 (-4) (-3) 6 = 0 ∧ ec 3 1 2 (-4) (-3) 6 = 0 := by
  unfold e3 e2 eg ec; norm_num

/-- mutation control: with no electron singlet (yE = 0) there is no solution with yQ /= 0. -/
theorem no_singlet_no_solution (Nc yQ yU yD yL : ℝ)
    (h3 : e3 yQ yU yD = 0) (h2 : e2 Nc yQ yL = 0) (hg : eg Nc yQ yU yD yL 0 = 0)
    (hNc : Nc ≠ 0) : yQ = 0 := by
  obtain ⟨_, _, hE⟩ := lin_consequences Nc yQ yU yD yL 0 h3 h2 hg
  have : Nc * yQ = 0 := by linarith
  exact (mul_eq_zero.mp this).resolve_left hNc

/-- homogeneity: linear equations degree 1, cubic degree 3 -/
theorem anom_homogeneous (l Nc yQ yU yD yL yE : ℝ) :
    e3 (l * yQ) (l * yU) (l * yD) = l * e3 yQ yU yD ∧
    e2 Nc (l * yQ) (l * yL) = l * e2 Nc yQ yL ∧
    eg Nc (l * yQ) (l * yU) (l * yD) (l * yL) (l * yE) = l * eg Nc yQ yU yD yL yE ∧
    ec Nc (l * yQ) (l * yU) (l * yD) (l * yL) (l * yE) = l ^ 3 * ec Nc yQ yU yD yL yE := by
  unfold e3 e2 eg ec
  refine ⟨?_, ?_, ?_, ?_⟩ <;> ring

/-- (y -> l y, g -> g / l) leaves every matter coupling g * y invariant -/
theorem coupling_rescaling_invariant (g l y : ℝ) (hl : l ≠ 0) : (g / l) * (l * y) = g * y := by
  field_simp

/-- charge lattice with Q_em = T3 + y/(2 Nc), normalisation yQ = 1 (a choice of unit) -/
noncomputable def qem (Nc T3 y : ℝ) : ℝ := T3 + y / (2 * Nc)

theorem charge_lattice (Nc : ℝ) (hNc : Nc ≠ 0) :
    qem Nc (1 / 2) 1 = 1 / 2 + 1 / (2 * Nc) ∧
    qem Nc (-1 / 2) 1 = qem Nc (1 / 2) 1 - 1 ∧
    qem Nc 0 (-1 + Nc) = -qem Nc (-1 / 2) 1 ∧            -- d^c carries -q_d
    qem Nc 0 (-1 - Nc) = -qem Nc (1 / 2) 1 ∧              -- u^c carries -q_u
    qem Nc 0 (2 * Nc) = 1 ∧                               -- e^c has charge +1
    ((Nc + 1) / 2) * qem Nc (1 / 2) 1 + ((Nc - 1) / 2) * qem Nc (-1 / 2) 1 = 1 := by
  unfold qem
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> field_simp <;> ring

theorem charges_Nc3 :
    qem 3 (1 / 2) 1 = 2 / 3 ∧ qem 3 (-1 / 2) 1 = -1 / 3 ∧ qem 3 0 (-4) = -2 / 3 ∧ qem 3 0 2 = 1 / 3 := by
  unfold qem; norm_num

/-- Witten SU(2): the number of doublets (Nc + 1) Ng is even for Nc = 3, every Ng -/
theorem witten_even_Nc3 (Ng : ℕ) : Even ((3 + 1) * Ng) := by
  exact ⟨2 * Ng, by ring⟩

/-- with a singlet nu_R (Nc = 3): cubic on the 3-dim linear solution space -/
theorem with_nuR_cubic (a0 a2 a5 : ℝ) :
    6 * a0 ^ 3 + 3 * (-2 * a0 - a2) ^ 3 + 3 * a2 ^ 3 + 2 * (-3 * a0) ^ 3
        + (6 * a0 - a5) ^ 3 + a5 ^ 3
      = 18 * a0 * (2 * a0 - a2 - a5) * (4 * a0 + a2 - a5) := by
  ring

/-- span{Y, B-L} lies inside the solution variety (Nc = 3, with nu_R) -/
theorem BL_Y_span_solves (a b : ℝ) :
    let yQ := a * 1 + b * 1
    let yU := a * (-4) + b * (-1)
    let yD := a * 2 + b * (-1)
    let yL := a * (-3) + b * (-3)
    let yE := a * 6 + b * 3
    let yN := a * 0 + b * 3
    (2 * yQ + yU + yD = 0) ∧ (3 * yQ + yL = 0) ∧
    (6 * yQ + 3 * yU + 3 * yD + 2 * yL + yE + yN = 0) ∧
    (6 * yQ ^ 3 + 3 * yU ^ 3 + 3 * yD ^ 3 + 2 * yL ^ 3 + yE ^ 3 + yN ^ 3 = 0) := by
  intro yQ yU yD yL yE yN
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp only [yQ, yU, yD, yL, yE, yN] <;> ring

end M2Anomaly

#print axioms M2Anomaly.lin_consequences
#print axioms M2Anomaly.cubic_factorisation
#print axioms M2Anomaly.anomaly_solution_set
#print axioms M2Anomaly.sm_solution
#print axioms M2Anomaly.sm_swapped_solution
#print axioms M2Anomaly.no_singlet_no_solution
#print axioms M2Anomaly.anom_homogeneous
#print axioms M2Anomaly.coupling_rescaling_invariant
#print axioms M2Anomaly.charge_lattice
#print axioms M2Anomaly.charges_Nc3
#print axioms M2Anomaly.witten_even_Nc3
#print axioms M2Anomaly.with_nuR_cubic
#print axioms M2Anomaly.BL_Y_span_solves
