import Mathlib

/-!
# I07 — Wave P: the regime coincidence as an exact conditional identity

SCOPE (per lean-math-certification): Lean certifies the ALGEBRA connecting the K1
coincidence ratio to the layer radius — the exact statement that turns the coincidence
into a falsifiable prediction:

  DEFINITIONS (the certified chain): g_B = G M / r_B^2 (Newtonian layer gravity);
  a0(rho_B) = (c/2) sqrt(G rho_B) (the density-form); r*^2 = G M / a0 (the transition
  radius, i.e. the radius where g_B = a0).

  THE IDENTITY (ratio_identity):  r*^2 / r_B^2 = g_B / a0  — EXACT, pure algebra.
  So the coincidence ratio = (r*/r_B)^2: it equals 1 iff the layer sits at r*,
  and the K1 "discovery" is EXACTLY the prediction r_B = r* = 100 au at the fiducial
  (M = 1e4, n = 1e10) — which is NOT yet measured (Wave P audit: the CLOUDY fits pin
  the thickness N_H/n_H, not the radius; the spherical U-route DISFAVORS by 2-4 dex).

  THE TOLERANCE (tol_upper/tol_lower): ratio in [1/2, 2] iff r_B^2 in [r*^2/2, 2 r*^2].

Numbers Python-verified in `bhstar_p1_empirical_rigor.py` (8/8). Zero `sorry`;
axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

/-- **P (the exact identity).** (r*/r_B)^2 = g_B/a0 given the definitions — the
coincidence ratio IS the squared radius ratio. -/
theorem ratio_identity {G M rB rstar a0 gB : ℝ}
    (hG : 0 < G) (hM : 0 < M) (hrB : 0 < rB) (ha0 : 0 < a0)
    (hrstar2 : rstar ^ 2 = G * M / a0)      -- the transition-radius definition
    (hgB : gB = G * M / rB ^ 2) :           -- the layer gravity
    rstar ^ 2 / rB ^ 2 = gB / a0 := by
  rw [hrstar2, hgB]
  field_simp

/-- **P (tolerance, upper).** ratio <= 2 iff r*^2 <= 2 r_B^2. -/
theorem tol_upper {rB rstar x : ℝ} (hp : 0 < rB) (h : x = rstar ^ 2 / rB ^ 2) :
    x ≤ 2 ↔ rstar ^ 2 ≤ 2 * rB ^ 2 := by
  rw [h, div_le_iff₀ (by positivity)]

/-- **P (tolerance, lower).** ratio >= 1/2 iff r_B^2 <= 2 r*^2. -/
theorem tol_lower {rB rstar x : ℝ} (hp : 0 < rB) (hq : 0 < rstar) (h : x = rstar ^ 2 / rB ^ 2) :
    (1:ℝ) / 2 ≤ x ↔ rB ^ 2 ≤ 2 * rstar ^ 2 := by
  rw [h, le_div_iff₀ (by positivity)]
  constructor
  · intro h1
    have h2 : (1 / 2) * rB ^ 2 ≤ rstar ^ 2 := h1
    linarith [(by nlinarith [sq_nonneg rB] : (0:ℝ) ≤ rB ^ 2), h2]
  · intro h1
    have h2 : (1 / 2) * rB ^ 2 ≤ rstar ^ 2 := by
      have h3 : 0 ≤ rB ^ 2 := sq_nonneg rB
      nlinarith [h1, h3]
    exact h2

end

#print axioms ratio_identity
#print axioms tol_upper
#print axioms tol_lower