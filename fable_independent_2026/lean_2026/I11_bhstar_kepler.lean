import Mathlib

/-!
# I11 — Wave T: the Kepler-grade law KP1

SCOPE (per lean-math-certification): Lean certifies the zero-free-parameter law from
the transition condition. Definitions (the certified chain): the transition
g_B = a0(rho_B) with g_B = G M / r_B^2 and a0 = (c/2) sqrt(G mu m p n_H).
CONCLUSION (pure field algebra after one certified sqrt-elimination):

    r_B^4 * n_H * (c^2 * mu * mp) = 4 * G * M^2

— the product of the fourth power of the layer radius and the layer density equals a
number set by the mass ALONE and the fundamental constants. One law, every object,
one constant (5.01e68 m at M = 1e4 Msun; Python `bhstar_t1_kepler_predictions.py`
4/4). Falsifier: any LRD off by > x2 in r_B (x16 in the product). Zero `sorry`;
axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

/-- **T (KP1).** The transition condition in its zero-free-parameter polynomial form:
r_B^4 n_H c^2 mu mp = 4 G M^2. -/
theorem kepler_law {G M c rB n_H mu mp : ℝ}
    (hG : 0 < G) (hM : 0 < M) (hc : 0 < c) (hrB : 0 < rB) (hn : 0 < n_H)
    (hmu : 0 < mu) (hmp : 0 < mp)
    (htrans : G * M / rB ^ 2 = (c / 2) * Real.sqrt (G * mu * mp * n_H)) :
    rB ^ 4 * n_H * (c ^ 2 * mu * mp) = 4 * G * M ^ 2 := by
  set s := Real.sqrt (G * mu * mp * n_H) with hs_def
  have hs : s ^ 2 = G * mu * mp * n_H := by
    rw [hs_def, Real.sq_sqrt (by positivity : (0:ℝ) ≤ G * mu * mp * n_H)]
  have hsq : (G * M / rB ^ 2) ^ 2 = ((c / 2) * s) ^ 2 := by rw [htrans]
  rw [div_pow] at hsq
  have hexp : ((c / 2) * s) ^ 2 = (c / 2) ^ 2 * s ^ 2 := by ring
  rw [hexp, hs] at hsq
  have h3 : 4 * (G * M) ^ 2 = rB ^ 4 * (c ^ 2 * (G * mu * mp * n_H)) := by
    calc 4 * (G * M) ^ 2 = 4 * rB ^ 4 * ((c / 2) ^ 2 * (G * mu * mp * n_H)) := by
            rw [← hsq]; field_simp
      _ = rB ^ 4 * (c ^ 2 * (G * mu * mp * n_H)) := by ring
  have h4 : 4 * G * M ^ 2 = rB ^ 4 * (c ^ 2 * mu * mp * n_H) := by
    apply mul_left_cancel₀ hG.ne'
    calc G * (4 * G * M ^ 2) = 4 * (G * M) ^ 2 := by ring
      _ = rB ^ 4 * (c ^ 2 * (G * mu * mp * n_H)) := h3
      _ = G * (rB ^ 4 * (c ^ 2 * mu * mp * n_H)) := by ring
  rw [h4]
  ring

end

#print axioms kepler_law