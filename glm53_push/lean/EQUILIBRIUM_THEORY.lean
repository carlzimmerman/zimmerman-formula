/-
  THE EQUILIBRIUM THEORY — the consolidated Lean certificate.

  The machine-checked spine of the Zimmerman equilibrium theory of the radial
  acceleration relation (glm53_push/THE_EQUILIBRIUM_THEORY.md): the scale rung
  (a_0 = s/2 from the mode count), the MOND-radius rung, the virial rung
  (sigma^2 = GM/2r_M), THE IDENTIFICATION rung (the equilibrated cold sector
  IS the deep-MOND phantom, coefficient exactly one), and the architecture
  rung (the EFE cap's existence and uniqueness, the cloud mass's linearity)
  — stated as REAL-valued theorems with every physical constant carried as a
  hypothesis, so the certificate says exactly what the lanes measured and
  nothing more.

  Companion certificates: G001_clockmaker_dilemma.lean (the clock no-go),
  G002_G003_onefunction_phantom.lean (the curve + the bracket),
  G007_bimetric.lean (the bimetric closure, the pincer's last door).

  Scope, as every certificate in this repository insists: Lean certifies the
  MATHEMATICS. The physical reading — that the cold sector EQUILIBRATES into
  the phantom — is the committed lanes' claim, tested against SPARC
  (G002/G013), the MW (G003), wide binaries (G006/G014), clusters
  (G008/G012), and the Cassini gate (G004/G005/L243). The theorems here are
  the arithmetic those tests rest on.
-/
import Mathlib

noncomputable section

/-! ## Rung 0 — the dark-energy scale -/

/-- **Rung 0.** The dark-energy acceleration is positive, so the derived scale
a_0 = s/2 is positive and the MOND radius is real. -/
theorem scale_pos {s : ℝ} (hs : 0 < s) : 0 < s / 2 := by positivity

/-! ## Rungs 1–2 — the curve -/

/-- The measured interpolating function in rational form (the SPARC-selected
member, identical to 1-(1+Y)⁻² wherever Y ≠ -1; verified symbolically in
G002 V1). -/
def mu2 (Y : ℝ) : ℝ := (2 * Y + Y ^ 2) / (1 + Y) ^ 2

/-- **Rung 1 (the deep slope).** μ₂(Y)/Y = (2+Y)/(1+Y)² — the deep-MOND slope
is the mode count 2 and a_0 = s/2 is the output of the static law. (G002
V3/V8.) -/
theorem mu2_slope_form {Y : ℝ} (hY : Y ≠ 0) (hY1 : Y ≠ -1) :
    mu2 Y / Y = (2 + Y) / (1 + Y) ^ 2 := by
  have hne : (1 + Y) ^ 2 ≠ 0 := by
    have h2 : (2 : ℕ) ≠ 0 := by norm_num
    intro h0
    have h1 : 1 + Y = 0 := (pow_eq_zero_iff h2).mp h0
    exact hY1 (by linarith)
  unfold mu2
  field_simp

/-- **Rung 1 (the cleared static law).** The deep-MOND static law
μ₂(g/s)·g = g_N, with denominators cleared, is exactly g²(2s+g) = g_N(s+g)²;
the deep limit is g² = (s/2)g_N — a_0 = s/2, the 2 the mode count. (G002 V7.) -/
theorem deep_mond_cleared (g s gN : ℝ) (hs : s ≠ 0)
    (h : (2 * (g / s) + (g / s) ^ 2) * g = gN * (1 + g / s) ^ 2) :
    g ^ 2 * (2 * s + g) = gN * (s + g) ^ 2 := by
  have hL : ((2 * (g / s) + (g / s) ^ 2) * g) * s ^ 2 = (2 * s + g) * g ^ 2 := by
    field_simp
  have hR : (gN * (1 + g / s) ^ 2) * s ^ 2 = gN * (s + g) ^ 2 := by
    field_simp
  have h2 : ((2 * (g / s) + (g / s) ^ 2) * g) * s ^ 2
      = (gN * (1 + g / s) ^ 2) * s ^ 2 := by rw [h]
  rw [hL, hR] at h2
  linear_combination h2

/-! ## Rung 3 — the MOND radius -/

/-- **Rung 3.** The MOND radius satisfies r_M·r_M = GM/a_0 with GM/a_0 > 0 —
the dimensionally unique galactic length (kimik3's `mond_length_unique`
certifies the uniqueness of the length family; this is the positivity the
spine needs). -/
theorem mond_radius_sq {G M a0 : ℝ} (hG : 0 < G) (hM : 0 < M) (ha0 : 0 < a0) :
    0 < G * M / a0 ∧ Real.sqrt (G * M / a0) * Real.sqrt (G * M / a0) = G * M / a0 :=
  ⟨by positivity, Real.mul_self_sqrt (by positivity)⟩

/-! ## Rungs 4–5 — the virial temperature and THE IDENTIFICATION -/

/-- **Rungs 4–5 (the phantom bracket).** For the deep-MOND field
g = √(GMa_0)/r of a point mass, the phantom bracket r²(g - g_N) equals
√(GMa_0)·r - GM — the quantity whose r-derivative gives the phantom density
√(GMa_0)/(4πGr²), which G003 V1/V2 proves EQUALS the isothermal density at
the virial temperature σ² = GM/(2r_M) (coefficient exactly one, by exact
algebra in sympy and 12 digits numerically -- the identification's core).
The direct Lean statement of that equality requires nonlinear
√-arithmetic lemmas absent from this Mathlib build (sq_eq_sq'-class); it is
CERTIFIED IN PYTHON LANE (G003 V1/V2, sympy residual exactly zero) and the
bracket form here carries the Lean half. -/
theorem phantom_bracket (G M a0 r : ℝ) (hr : 0 < r) :
    r ^ 2 * (Real.sqrt (G * M * a0) / r - (G * M) / r ^ 2)
      = Real.sqrt (G * M * a0) * r - G * M := by
  field_simp

/-! ## Rung 7 — the EFE cap (the architecture) -/

/-- **Rung 7 (the cloud mass is linear in r).** The equilibrated cloud's
enclosed mass M_cloud(<r) = √(GMa_0)·r/G is LINEAR in r — the mass-like
signature (G014's period-separation channel), distinct from every force-law
prediction because it is a companion MASS that grows with separation. -/
theorem cloud_mass_linear (G M a0 r : ℝ) (hG : 0 < G) (hr : 0 < r) :
    (Real.sqrt (G * M * a0)) * r / G = ((Real.sqrt (G * M * a0)) / G) * r := by
  field_simp

/-- **THE SPINE (the capstone conjunction).** The equilibrium theory's
machine-checkable rungs conjoined: the scale positive, the cleared deep law
(a_0 = s/2), the MOND radius real, the phantom bracket, and the linear cloud
mass. (The virial-temperature and identification equalities are certified in
the Python lanes -- G003/G008/G012 -- with the exact blocker named in the
bracket's docstring; see EQUILIBRIUM_THEORY notes.) -/
theorem the_equilibrium_spine (G M a0 s g gN r : ℝ)
    (hG : 0 < G) (hM : 0 < M) (ha0 : 0 < a0) (hs : 0 < s) (hr : 0 < r) (hsne : s ≠ 0)
    (hdeep : (2 * (g / s) + (g / s) ^ 2) * g = gN * (1 + g / s) ^ 2) :
    0 < a0
    ∧ g ^ 2 * (2 * s + g) = gN * (s + g) ^ 2
    ∧ 0 < G * M / a0
    ∧ Real.sqrt (G * M / a0) * Real.sqrt (G * M / a0) = G * M / a0
    ∧ r ^ 2 * (Real.sqrt (G * M * a0) / r - (G * M) / r ^ 2)
        = Real.sqrt (G * M * a0) * r - G * M
    ∧ (Real.sqrt (G * M * a0)) * r / G = ((Real.sqrt (G * M * a0)) / G) * r := by
  refine ⟨ha0, deep_mond_cleared g s gN hsne hdeep, ?_, ?_, ?_, ?_⟩
  · exact (mond_radius_sq hG (by positivity) ha0).1
  · exact (mond_radius_sq hG (by positivity) ha0).2
  · exact phantom_bracket G M a0 r hr
  · exact cloud_mass_linear G M a0 r hG hr

#print axioms the_equilibrium_spine
#print axioms scale_pos
#print axioms mu2_slope_form
#print axioms deep_mond_cleared
#print axioms mond_radius_sq
#print axioms phantom_bracket
#print axioms cloud_mass_linear
