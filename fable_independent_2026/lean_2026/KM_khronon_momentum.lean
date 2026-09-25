import Mathlib

open Real

/-!
# KM — certificates for the khronon-momentum lanes (real_research/khronon_momentum_2026, KM1–KM2)

SCOPE: Lean certifies the exact ALGEBRA of the linear systems the KM lanes solve: that the stated
closed forms SOLVE the Fourier-space equations (by substitution), and the identities read off them.
The equations themselves are taken as hypotheses/definitions exactly as derived symbolically in the
Python lanes (KM1: the linearised khronometric action in unitary gauge; KM2: L340's scalar block,
copied verbatim). Lean does NOT certify that these actions describe nature, nor anything beyond
linear, frozen-coefficient, principal order. Zero `sorry`; axioms ⊆ {propext, Classical.choice,
Quot.sound}.

A moving source ∝ e^{i(kx − ωt)}: the shift is 90° out of phase, σ = i s (KM1) and β = i b (KM2),
which makes every equation real.

K1  (KM1 C3) the closed forms (φ, s, ψ) solve the three khronometric equations for λ = 1 + ε, α = rε.
K2  (KM1 C4) the potential matter feels, Φ_B = φ + ω s, has NO 1/ε term: its denominator is k⁴Δ.
K3  (KM1 C4) its ω → 0 value is the full (matter + phantom) Newtonian potential, G-renormalised by
    1/(1 − α/2): the moving-at-rest phantom gravitates fully.
K4  (KM1 C2) CONTROL at λ = 1, α = 0: the Hamiltonian and momentum constraints force ω ρ_ph = 0 — a
    phantom that moves without momentum cannot exist (L330's frozen phantom).
K5  (KM1 C7) the lapse DOES carry a 1/ε pole: ε φ → 8πG ω² ρ_ph/(k²(r ω² − k²)) as ε → 0 — the
    aether's own acceleration (the MOND sector's input in L297), the correction L333 found.
K6  (KM2) the closed forms solve L340's block (real form); its static response is (1+C)/(1 − α_c(1+C)/2);
    at α_c = 0 the exact response is R = 1 − 3u²/(C+1) + [C/(C+1)] u²/(c_s² − u²),
    c_s² = c₂/(C(2 + 3c₂)), and the mode (pole) sits exactly at u² = c_s².
-/

noncomputable section

namespace KM

/-! ## KM1 — the linearised khronometric system for a moving galaxy -/

/-- The common denominator Δ = ε k² r + 3 ε ω² r − 2 k² + 2 ω² r. -/
def Δ (ε k ω r : ℝ) : ℝ := ε * k ^ 2 * r + 3 * ε * ω ^ 2 * r - 2 * k ^ 2 + 2 * ω ^ 2 * r

def φsol (G ε k ω r ρm ρp : ℝ) : ℝ :=
  8 * π * G * (ε * k ^ 2 * ρm + ε * k ^ 2 * ρp + 3 * ε * ω ^ 2 * ρp + 2 * ω ^ 2 * ρp) /
    (ε * k ^ 2 * Δ ε k ω r)

def ssol (G ε k ω r ρm ρp : ℝ) : ℝ :=
  -4 * π * G * ω * (-9 * ε ^ 2 * ω ^ 2 * r * ρm + 2 * ε * k ^ 2 * r * ρm + 6 * ε * k ^ 2 * ρm
    + 6 * ε * k ^ 2 * ρp - 6 * ε * ω ^ 2 * r * ρm + 4 * k ^ 2 * ρp) / (ε * k ^ 4 * Δ ε k ω r)

def ψsol (G ε k ω r ρm ρp : ℝ) : ℝ :=
  -4 * π * G * (3 * ε * ω ^ 2 * r * ρm - 2 * k ^ 2 * ρm - 2 * k ^ 2 * ρp + 2 * ω ^ 2 * r * ρm) /
    (k ^ 2 * Δ ε k ω r)

/-- The three equations (Hamiltonian, momentum, trace), Fourier space, ×16πG, λ = 1 + ε, α = rε. -/
def eqH (G ε k r ρm ρp φ ψ : ℝ) : ℝ := -16 * π * G * (ρm + ρp) + 2 * (r * ε) * k ^ 2 * φ - 4 * k ^ 2 * ψ
def eqM (G ε k ω ρm s ψ : ℝ) : ℝ :=
  -16 * π * G * ρm * ω - 2 * (1 + ε) * (k ^ 4 * s + 3 * ω * k ^ 2 * ψ) + 2 * k ^ 4 * s + 2 * ω * k ^ 2 * ψ
def eqT (ε k ω φ s ψ : ℝ) : ℝ :=
  6 * (1 + ε) * (-3 * ω ^ 2 * ψ - ω * k ^ 2 * s) - 4 * k ^ 2 * φ + 4 * k ^ 2 * ψ + 6 * ω ^ 2 * ψ
    + 2 * ω * k ^ 2 * s

theorem K1_solves (G ε k ω r ρm ρp : ℝ) (hε : ε ≠ 0) (hk : k ≠ 0) (hΔ : Δ ε k ω r ≠ 0) :
    eqH G ε k r ρm ρp (φsol G ε k ω r ρm ρp) (ψsol G ε k ω r ρm ρp) = 0 ∧
    eqM G ε k ω ρm (ssol G ε k ω r ρm ρp) (ψsol G ε k ω r ρm ρp) = 0 ∧
    eqT ε k ω (φsol G ε k ω r ρm ρp) (ssol G ε k ω r ρm ρp) (ψsol G ε k ω r ρm ρp) = 0 := by
  refine ⟨?_, ?_, ?_⟩ <;>
  · simp only [eqH, eqM, eqT, φsol, ssol, ψsol]
    field_simp
    simp only [Δ]
    ring

/-- Φ_B = φ + ω s: no 1/ε term (denominator k⁴Δ only). -/
def ΦBform (G ε k ω r ρm ρp : ℝ) : ℝ :=
  -4 * π * G * (-9 * ε * ω ^ 4 * r * ρm - 2 * k ^ 4 * ρm - 2 * k ^ 4 * ρp + 2 * k ^ 2 * ω ^ 2 * r * ρm
    + 6 * k ^ 2 * ω ^ 2 * ρm - 6 * ω ^ 4 * r * ρm) / (k ^ 4 * Δ ε k ω r)

theorem K2_PhiB_regular (G ε k ω r ρm ρp : ℝ) (hε : ε ≠ 0) (hk : k ≠ 0) (hΔ : Δ ε k ω r ≠ 0) :
    φsol G ε k ω r ρm ρp + ω * ssol G ε k ω r ρm ρp = ΦBform G ε k ω r ρm ρp := by
  simp only [φsol, ssol, ΦBform]
  field_simp
  ring

theorem K3_static_full_phantom (G ε k r ρm ρp : ℝ) (hk : k ≠ 0) (h2 : ε * r - 2 ≠ 0) :
    ΦBform G ε k 0 r ρm ρp = -4 * π * G * (ρm + ρp) / (k ^ 2 * (1 - r * ε / 2)) := by
  have h2' : 1 - r * ε / 2 ≠ 0 := by
    intro h; apply h2; linarith
  have h2'' : 2 - ε * r ≠ 0 := by
    intro h; apply h2; linarith
  have hΔ0 : Δ ε k 0 r = k ^ 2 * (ε * r - 2) := by simp only [Δ]; ring
  have hΔ0' : Δ ε k 0 r ≠ 0 := by rw [hΔ0]; exact mul_ne_zero (pow_ne_zero 2 hk) h2
  simp only [ΦBform]
  rw [hΔ0]
  field_simp
  ring

/-- CONTROL (λ = 1, α = 0): the constraints force ω ρ_ph = 0. -/
theorem K4_control_frozen (G k ω ρm ρp φ s ψ : ℝ) (hG : 0 < G) (hk : k ≠ 0)
    (hH : eqH G 0 k 1 ρm ρp φ ψ = 0) (hM : eqM G 0 k ω ρm s ψ = 0) : ω * ρp = 0 := by
  simp only [eqH, eqM] at hH hM
  have hk2 : k ^ 2 ≠ 0 := pow_ne_zero 2 hk
  -- hH: ψ = −4πG(ρm+ρp)/k²;  hM: ω(−16πGρm − 4k²ψ) = 0
  have hψ : 4 * k ^ 2 * ψ = -16 * π * G * (ρm + ρp) := by linarith
  have hM' : ω * (-16 * π * G * ρm - 4 * k ^ 2 * ψ) = 0 := by linarith
  rw [hψ] at hM'
  have hπG : 16 * π * G ≠ 0 := by positivity
  have : ω * ρp * (16 * π * G) = 0 := by linarith
  rcases mul_eq_zero.mp this with h | h
  · exact h
  · exact absurd h hπG

/-- The lapse's 1/ε pole: ε φ at ε = 0 equals 8πG ω² ρ_ph/(k²(r ω² − k²)). -/
theorem K5_lapse_pole (G k ω r ρm ρp : ℝ) (hk : k ≠ 0) (hΔ0 : r * ω ^ 2 - k ^ 2 ≠ 0) :
    (8 * π * G * (0 * k ^ 2 * ρm + 0 * k ^ 2 * ρp + 3 * 0 * ω ^ 2 * ρp + 2 * ω ^ 2 * ρp) /
      (k ^ 2 * Δ 0 k ω r)) = 8 * π * G * ω ^ 2 * ρp / (k ^ 2 * (r * ω ^ 2 - k ^ 2)) := by
  have hD : Δ 0 k ω r = 2 * (r * ω ^ 2 - k ^ 2) := by simp only [Δ]; ring
  have hk2 : k ^ 2 ≠ 0 := pow_ne_zero 2 hk
  rw [hD, div_eq_div_iff (mul_ne_zero hk2 (mul_ne_zero two_ne_zero hΔ0)) (mul_ne_zero hk2 hΔ0)]
  ring

theorem K5_eps_phi (G ε k ω r ρm ρp : ℝ) (hε : ε ≠ 0) (hk : k ≠ 0) (hΔ : Δ ε k ω r ≠ 0) :
    ε * φsol G ε k ω r ρm ρp =
      8 * π * G * (ε * k ^ 2 * ρm + ε * k ^ 2 * ρp + 3 * ε * ω ^ 2 * ρp + 2 * ω ^ 2 * ρp) /
        (k ^ 2 * Δ ε k ω r) := by
  simp only [φsol]
  field_simp

/-! ## KM2 — L340's scalar block (real form, k = 1, ω = u, β = i b) -/

/-- The common denominator of L340's block solution. -/
def Dn (C c2 ac u : ℝ) : ℝ :=
  3 * C * ac * c2 * u ^ 2 + C * ac * c2 + 2 * C * ac * u ^ 2 + 6 * C * c2 * u ^ 2 + 4 * C * u ^ 2
    + 3 * ac * c2 * u ^ 2 + ac * c2 + 2 * ac * u ^ 2 - 2 * c2

def ψ2 (C c2 ac u R : ℝ) : ℝ :=
  -R * (3 * C * ac * c2 * u ^ 2 + 2 * C * ac * u ^ 2 + 6 * C * c2 * u ^ 2 - 2 * C * c2 + 4 * C * u ^ 2
    + 3 * ac * c2 * u ^ 2 + 2 * ac * u ^ 2 - 2 * c2) / (4 * Dn C c2 ac u)
def φ2 (C c2 ac u R : ℝ) : ℝ := R * c2 * (C + 1) / (2 * Dn C c2 ac u)
def b2 (C c2 ac u R : ℝ) : ℝ :=
  R * u * (9 * C * ac * c2 * u ^ 2 + 6 * C * ac * u ^ 2 - 2 * C * ac + 18 * C * c2 * u ^ 2 - 6 * C * c2
    + 12 * C * u ^ 2 - 4 * C + 9 * ac * c2 * u ^ 2 + 6 * ac * u ^ 2 - 2 * ac - 6 * c2) / (4 * Dn C c2 ac u)
def U2 (C c2 ac u R : ℝ) : ℝ := R * c2 / (2 * Dn C c2 ac u)

/-- L340's four rows (H1 block of L340_filtered_khronon_completion.py) in real form. -/
def row0 (c2 u ψ φ b : ℝ) : ℝ := -6 * b * c2 * u - 4 * b * u - 18 * c2 * ψ * u ^ 2 - 4 * φ - 12 * ψ * u ^ 2 + 4 * ψ
def row1 (ac R ψ φ U : ℝ) : ℝ := -R - 4 * U + 2 * ac * φ + 4 * φ - 4 * ψ
def row2 (c2 u R ψ b : ℝ) : ℝ := -R * u - 2 * b * c2 - 6 * c2 * ψ * u - 4 * ψ * u
def row3 (C φ U : ℝ) : ℝ := 4 * C * U + 4 * U - 4 * φ

theorem K6_solves (C c2 ac u R : ℝ) (hD : Dn C c2 ac u ≠ 0) :
    row0 c2 u (ψ2 C c2 ac u R) (φ2 C c2 ac u R) (b2 C c2 ac u R) = 0 ∧
    row1 ac R (ψ2 C c2 ac u R) (φ2 C c2 ac u R) (U2 C c2 ac u R) = 0 ∧
    row2 c2 u R (ψ2 C c2 ac u R) (b2 C c2 ac u R) = 0 ∧
    row3 C (φ2 C c2 ac u R) (U2 C c2 ac u R) = 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;>
  · simp only [row0, row1, row2, row3, ψ2, φ2, b2, U2]
    field_simp
    simp only [Dn]
    ring

/-- Static response (at u = 0, Φ_B = φ): φ(0)/ψ_N = (1 + C)/(1 − α_c(1 + C)/2), ψ_N = −R/4. -/
theorem K6_static (C c2 ac R : ℝ) (hc2 : c2 ≠ 0) (hR : R ≠ 0) (hC : ac * (C + 1) - 2 ≠ 0) :
    φ2 C c2 ac 0 R / (-R / 4) = (1 + C) / (1 - ac * (1 + C) / 2) := by
  have hD : Dn C c2 ac 0 = c2 * (ac * (C + 1) - 2) := by simp only [Dn]; ring
  have h7 : (C + 1) * ac - 2 ≠ 0 := by intro h; apply hC; linarith
  have h8 : 2 - ac * (1 + C) ≠ 0 := by intro h; apply hC; linarith
  have hden : 1 - ac * (1 + C) / 2 ≠ 0 := by intro h; apply hC; linarith
  simp only [φ2]
  rw [hD]
  field_simp
  ring

/-- At α_c = 0: the exact lag law R − 1 = −3u²/(C+1) + [C/(C+1)] u²/(c_s² − u²), with
    c_s² = c₂/(C(2 + 3c₂)); equivalently the normalised response below. -/
theorem K6_lag_law (C c2 u : ℝ) (hC : 0 < C) (hc2 : 0 < c2)
    (hu : u ^ 2 ≠ c2 / (C * (2 + 3 * c2))) :
    ((φ2 C c2 0 u 1 + u * b2 C c2 0 u 1) / (-1 / 4)) / ((1 + C) / (1 - 0 * (1 + C) / 2)) =
      1 - 3 * u ^ 2 / (C + 1) + C / (C + 1) * (u ^ 2 / (c2 / (C * (2 + 3 * c2)) - u ^ 2)) := by
  have hC0 : C ≠ 0 := ne_of_gt hC
  have h3 : 2 + 3 * c2 ≠ 0 := by linarith
  have hC1 : C + 1 ≠ 0 := by linarith
  have hK : C * (2 + 3 * c2) ≠ 0 := mul_ne_zero hC0 h3
  obtain ⟨d, hd⟩ : ∃ d, d = C * (2 + 3 * c2) * u ^ 2 - c2 := ⟨_, rfl⟩
  have hd0 : d ≠ 0 := by
    rw [hd]; intro h; apply hu; field_simp; linarith
  have hDn : Dn C c2 0 u = 2 * d := by rw [hd]; simp only [Dn]; ring
  have key : c2 / (C * (2 + 3 * c2)) - u ^ 2 = -d / (C * (2 + 3 * c2)) := by
    rw [hd]; field_simp; ring
  rw [key]
  simp only [φ2, b2]
  rw [hDn]
  field_simp
  rw [hd]
  ring

/-- The mode: at α_c = 0 the block's denominator vanishes exactly at u² = c_s². -/
theorem K6_mode_speed (C c2 u : ℝ) (hC : 0 < C) (hc2 : 0 < c2) :
    Dn C c2 0 u = 0 ↔ u ^ 2 = c2 / (C * (2 + 3 * c2)) := by
  have h23 : (0:ℝ) < C * (2 + 3 * c2) := by positivity
  simp only [Dn]
  constructor
  · intro h; field_simp; linarith
  · intro h; rw [h]; field_simp; ring

end KM

end

#print axioms KM.K1_solves
#print axioms KM.K2_PhiB_regular
#print axioms KM.K3_static_full_phantom
#print axioms KM.K4_control_frozen
#print axioms KM.K5_lapse_pole
#print axioms KM.K5_eps_phi
#print axioms KM.K6_solves
#print axioms KM.K6_static
#print axioms KM.K6_lag_law
#print axioms KM.K6_mode_speed
