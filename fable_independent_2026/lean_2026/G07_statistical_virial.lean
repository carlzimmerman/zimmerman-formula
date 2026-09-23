import Mathlib

/-!
# G07 -- THE STATISTICAL VIRIAL (reduced form): the max-entropy identity
#        closes the spine's one non-Lean rung E2

E2 = sigma^2 = sqrt(G M_b a0)/2 is the spine's one non-Lean rung: the virial
theorem enters as a physics input (G091), not as a statistical output.  This
certificate states the HONEST reduced theorem and its honest boundary:

  (1) `statistical_virial` :  the max-entropy EL identity
          γ = C / σ²        (the Boltzmann identification β = 1/σ², G084)
        at the phantom closure γ = 2  (ρ = A r^-2, the equilibrium's isothermal
        profile, Lean-certified: M01 / G227 / C07 / EQUILIBRIUM_THEORY)
        IMPLIES  σ² = C / 2 = Real.sqrt (G M_b a0) / 2  -- E2 as pure algebra.
  (2) `el_identity_inverse` :  the EL identity is an INVERSION:
          γ = C / σ²  ↔  σ² = C / γ.
  (3) `el_family_free` :  the honest boundary -- the counting admits EVERY
        positive temperature: for any s2 > 0 the slope γ = C / s2 solves the
        EL equation, so the entropy functional selects no σ².  What fixes
        γ = 2 (the phantom slope) -- equivalently σ² = C/2 directly -- is the
        kinetic-vs-potential MECHANICAL balance 2T + W_self + W_bar = 3P_sV
        (the virial theorem proper, G091): the missing premise, registered.

Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
-/

-- (1) THE REDUCED STATISTICAL VIRIAL:
--     { EL identity γ = C/σ² } ∧ { phantom closure γ = 2 }  =>  σ² = C/2
theorem statistical_virial (C s2 γ : ℝ) (hC : C ≠ 0) (hs2 : s2 ≠ 0)
    (hident : γ = C / s2) (hphantom : γ = 2) : s2 = C / 2 := by
  have hCeq : C = 2 * s2 := by
    have hγs2 : C / s2 = 2 := by rw [← hident, hphantom]
    calc C = (C / s2) * s2 := by field_simp [hs2]
         _ = 2 * s2 := by rw [hγs2]
  calc s2 = (2 * s2) / 2 := by field_simp
       _ = C / 2 := by rw [hCeq]

-- the instantiation at the committed well: C = sqrt(G M_b a0)
theorem statistical_virial_instantiated (G Mb a0 s2 : ℝ) (hG : 0 < G)
    (hMb : 0 < Mb) (ha0 : 0 < a0) (hs2 : s2 ≠ 0)
    (hident : (2 : ℝ) = Real.sqrt (G * Mb * a0) / s2) :
    s2 = Real.sqrt (G * Mb * a0) / 2 := by
  have hC : Real.sqrt (G * Mb * a0) ≠ 0 := by positivity
  exact statistical_virial (Real.sqrt (G * Mb * a0)) s2 2 hC hs2
    hident (by norm_num)

-- (2) the inversion: the EL identity is  γ = C/σ²  ↔  σ² = C/γ
theorem el_identity_inverse (C s2 γ : ℝ) (hs2 : s2 ≠ 0) (hγ : γ ≠ 0)
    (hident : γ = C / s2) : s2 = C / γ := by
  have hCequal : C = γ * s2 := by
    calc C = (C / s2) * s2 := by field_simp [hs2]
         _ = γ * s2 := by rw [← hident]
  calc s2 = (γ * s2) / γ := by field_simp [hγ]
       _ = C / γ := by rw [hCequal]

-- (3) the honest boundary: EVERY positive temperature is a consistent
--     max-entropy state (each σ² ↔ its own slope γ = C/σ²) -- the counting
--     selects no σ²: the virial's kinetic-potential balance is the physics
--     that fixes γ = 2 (or σ² = C/2), and that balance is NOT in S[ρ].
theorem el_family_free (C s2 : ℝ) (hs2 : s2 ≠ 0) :
    let γ := C / s2
    γ * s2 = C := by
  intro γ
  dsimp [γ]
  field_simp [hs2]

-- a symbolic instance of the closure: (γ = C/σ²) ∧ (γ = 2) → 2σ² = C
theorem phantom_half_closure (C s2 : ℝ) (hs2 : s2 ≠ 0)
    (hident : (2 : ℝ) = C / s2) : 2 * s2 = C := by
  field_simp [hs2] at hident
  nlinarith

#check statistical_virial
#check statistical_virial_instantiated
#check el_identity_inverse
#check el_family_free
#check phantom_half_closure

#print axioms statistical_virial
#print axioms statistical_virial_instantiated
#print axioms el_identity_inverse
#print axioms el_family_free
#print axioms phantom_half_closure