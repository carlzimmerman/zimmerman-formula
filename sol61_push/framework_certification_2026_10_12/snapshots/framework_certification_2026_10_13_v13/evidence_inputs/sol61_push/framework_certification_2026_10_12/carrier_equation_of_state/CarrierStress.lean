import Mathlib

/-! Classical canonical own-framework charged carrier, natural units.
phi=(r1+i*r2)/sqrt(2), chi=(r3+i*r4)/sqrt(2).
K=sum v_i^2/2, S=(r1^2+r2^2+4*r3^2+4*r4^2)/2.
The source current j^0=i(phi* dotphi-phi dotphi*)+2i(chi* dotchi-chi dotchi*)
is q=r2*v1-r1*v2+2*r4*v3-2*r3*v4. No quantum rate is used.
Potential lower bound is derived from DECLARED actual positive-square structure;
u1,u2 denote real/imaginary parts of sqrt(Delta)*chi+g/sqrt(Delta)*phi^2.
No cosmological evolution, metric backreaction or observed EOS is inferred. -/
noncomputable section
namespace FrameworkCarrierStress

def kinetic (v1 v2 v3 v4 : ℝ) : ℝ := (v1 ^ 2 + v2 ^ 2 + v3 ^ 2 + v4 ^ 2) / 2
def amplitude (r1 r2 r3 r4 : ℝ) : ℝ := (r1 ^ 2 + r2 ^ 2 + 4 * r3 ^ 2 + 4 * r4 ^ 2) / 2
def charge (r1 r2 r3 r4 v1 v2 v3 v4 : ℝ) : ℝ :=
  r2 * v1 - r1 * v2 + 2 * r4 * v3 - 2 * r3 * v4
def potential (m S u1 u2 rep phiSq : ℝ) : ℝ := m ^ 2 * S + u1 ^ 2 + u2 ^ 2 + rep * phiSq ^ 2
/-- Exact real/imaginary components of the source positive square in sqrt2 coordinates. -/
def residualReal (Δ g r1 r2 r3 : ℝ) : ℝ :=
  Real.sqrt Δ * r3 / Real.sqrt 2 + g / Real.sqrt Δ * (r1 ^ 2 - r2 ^ 2) / 2
def residualImag (Δ g r1 r2 r4 : ℝ) : ℝ :=
  Real.sqrt Δ * r4 / Real.sqrt 2 + g / Real.sqrt Δ * r1 * r2
def actualPotential (m Δ g rep r1 r2 r3 r4 : ℝ) : ℝ :=
  potential m (amplitude r1 r2 r3 r4) (residualReal Δ g r1 r2 r3)
    (residualImag Δ g r1 r2 r4) rep ((r1 ^ 2 + r2 ^ 2) / 2)

def rho (K V : ℝ) : ℝ := K + V
def pressure (K V : ℝ) : ℝ := K - V
def gradientRho (K B V : ℝ) : ℝ := K + B + V
def isotropicPressure (K B V : ℝ) : ℝ := K - B / 3 - V

theorem four_coordinate_squares (a b c d v w x y : ℝ) :
    (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2) * (v ^ 2 + w ^ 2 + x ^ 2 + y ^ 2) -
      (a * v + b * w + c * x + d * y) ^ 2 =
    (a * w - b * v) ^ 2 + (a * x - c * v) ^ 2 + (a * y - d * v) ^ 2 +
      (b * x - c * w) ^ 2 + (b * y - d * w) ^ 2 + (c * y - d * x) ^ 2 := by ring

theorem four_coordinate_cauchy (a b c d v w x y : ℝ) :
    (a * v + b * w + c * x + d * y) ^ 2 ≤
      (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2) * (v ^ 2 + w ^ 2 + x ^ 2 + y ^ 2) := by
  have he := four_coordinate_squares a b c d v w x y
  have hp : 0 ≤ (a * w - b * v) ^ 2 + (a * x - c * v) ^ 2 + (a * y - d * v) ^ 2 +
      (b * x - c * w) ^ 2 + (b * y - d * w) ^ 2 + (c * y - d * x) ^ 2 := by positivity
  linarith

theorem charge_bound (r1 r2 r3 r4 v1 v2 v3 v4 : ℝ) :
    charge r1 r2 r3 r4 v1 v2 v3 v4 ^ 2 ≤
      4 * amplitude r1 r2 r3 r4 * kinetic v1 v2 v3 v4 := by
  have hc := four_coordinate_cauchy r2 (-r1) (2 * r4) (-2 * r3) v1 v2 v3 v4
  convert hc using 1 <;> dsimp [charge, amplitude, kinetic] <;> ring

theorem positive_square_potential (m S u1 u2 rep phiSq : ℝ) (hrep : 0 ≤ rep) :
    m ^ 2 * S ≤ potential m S u1 u2 rep phiSq := by
  unfold potential
  have hp : 0 ≤ u1 ^ 2 + u2 ^ 2 + rep * phiSq ^ 2 := by positivity
  linarith

/-- Generic stress restriction from proved coordinate charge bound and action floor. -/
theorem homogeneous_stress_bound (m S K V q : ℝ) (hK : 0 ≤ K)
    (hcharge : q ^ 2 ≤ 4 * S * K) (hV : m ^ 2 * S ≤ V) :
    m ^ 2 * q ^ 2 ≤ rho K V ^ 2 - pressure K V ^ 2 := by
  have hc := mul_le_mul_of_nonneg_left hcharge (sq_nonneg m)
  have hv := mul_le_mul_of_nonneg_left hV (by positivity : 0 ≤ 4 * K)
  unfold rho pressure
  nlinarith [hc, hv]

/-- Full coordinate-level homogeneous statement, not an assumed Cauchy leaf. -/
theorem coordinate_stress_bound (m r1 r2 r3 r4 v1 v2 v3 v4 u1 u2 rep phiSq : ℝ)
    (hrep : 0 ≤ rep) :
    m ^ 2 * charge r1 r2 r3 r4 v1 v2 v3 v4 ^ 2 ≤
      rho (kinetic v1 v2 v3 v4) (potential m (amplitude r1 r2 r3 r4) u1 u2 rep phiSq) ^ 2 -
      pressure (kinetic v1 v2 v3 v4) (potential m (amplitude r1 r2 r3 r4) u1 u2 rep phiSq) ^ 2 := by
  apply homogeneous_stress_bound
  · unfold kinetic; positivity
  · exact charge_bound r1 r2 r3 r4 v1 v2 v3 v4
  · exact positive_square_potential m (amplitude r1 r2 r3 r4) u1 u2 rep phiSq hrep

/-- The coordinate inequality applied directly to the actual declared carrier potential. -/
theorem actual_carrier_stress_bound (m Δ g rep r1 r2 r3 r4 v1 v2 v3 v4 : ℝ)
    (hrep : 0 ≤ rep) :
    m ^ 2 * charge r1 r2 r3 r4 v1 v2 v3 v4 ^ 2 ≤
      rho (kinetic v1 v2 v3 v4) (actualPotential m Δ g rep r1 r2 r3 r4) ^ 2 -
      pressure (kinetic v1 v2 v3 v4) (actualPotential m Δ g rep r1 r2 r3 r4) ^ 2 :=
  coordinate_stress_bound m r1 r2 r3 r4 v1 v2 v3 v4
    (residualReal Δ g r1 r2 r3) (residualImag Δ g r1 r2 r4) rep
    ((r1 ^ 2 + r2 ^ 2) / 2) hrep

/-- Positive density with exact p/rho=-1 has no kinetic energy or charge. -/
theorem exact_negative_one (S K V q : ℝ) (hcharge : q ^ 2 ≤ 4 * S * K)
    (hrho : 0 < rho K V) (hw : pressure K V / rho K V = -1) : K = 0 ∧ q = 0 := by
  have hp := (div_eq_iff hrho.ne').mp hw
  unfold rho pressure at hp
  have hk : K = 0 := by linarith
  rw [hk] at hcharge
  refine ⟨hk, ?_⟩
  nlinarith [sq_nonneg q]

/-- Saturating the charge-mass floor forces vanishing homogeneous pressure. -/
theorem saturated_pressure_zero (m S K V q : ℝ) (hK : 0 ≤ K)
    (hcharge : q ^ 2 ≤ 4 * S * K) (hV : m ^ 2 * S ≤ V)
    (hsat : rho K V ^ 2 = m ^ 2 * q ^ 2) : pressure K V = 0 := by
  have hb := homogeneous_stress_bound m S K V q hK hcharge hV
  nlinarith [sq_nonneg (pressure K V)]

/-- Isotropically averaged gradient stress; no general anisotropic scalar p assumed. -/
theorem isotropic_stress_bound (m S K B V q : ℝ) (hS : 0 ≤ S) (hK : 0 ≤ K)
    (hB : 0 ≤ B) (hcharge : q ^ 2 ≤ 4 * S * K) (hV : m ^ 2 * S ≤ V) :
    m ^ 2 * q ^ 2 ≤ gradientRho K B V ^ 2 - isotropicPressure K B V ^ 2 := by
  have hv : 0 ≤ V := le_trans (by positivity) hV
  have hb := homogeneous_stress_bound m S K V q hK hcharge hV
  have he : gradientRho K B V ^ 2 - isotropicPressure K B V ^ 2 =
      rho K V ^ 2 - pressure K V ^ 2 + (8 / 3 : ℝ) * K * B +
        (4 / 3 : ℝ) * B * V + (8 / 9 : ℝ) * B ^ 2 := by
    unfold gradientRho isotropicPressure rho pressure
    ring
  have hp : 0 ≤ (8 / 3 : ℝ) * K * B + (4 / 3 : ℝ) * B * V + (8 / 9 : ℝ) * B ^ 2 := by positivity
  rw [he]
  linarith

theorem isotropic_exact_negative_one (S K B V q : ℝ) (hK : 0 ≤ K) (hB : 0 ≤ B)
    (hcharge : q ^ 2 ≤ 4 * S * K) (hrho : 0 < gradientRho K B V)
    (hw : isotropicPressure K B V / gradientRho K B V = -1) : K = 0 ∧ B = 0 ∧ q = 0 := by
  have hp := (div_eq_iff hrho.ne').mp hw
  unfold gradientRho isotropicPressure at hp
  have hk : K = 0 := by linarith
  have hzeroB : B = 0 := by linarith
  rw [hk] at hcharge
  exact ⟨hk, hzeroB, by nlinarith [sq_nonneg q]⟩

end FrameworkCarrierStress
#print axioms FrameworkCarrierStress.four_coordinate_squares
#print axioms FrameworkCarrierStress.four_coordinate_cauchy
#print axioms FrameworkCarrierStress.charge_bound
#print axioms FrameworkCarrierStress.positive_square_potential
#print axioms FrameworkCarrierStress.homogeneous_stress_bound
#print axioms FrameworkCarrierStress.coordinate_stress_bound
#print axioms FrameworkCarrierStress.exact_negative_one
#print axioms FrameworkCarrierStress.saturated_pressure_zero
#print axioms FrameworkCarrierStress.isotropic_stress_bound
#print axioms FrameworkCarrierStress.isotropic_exact_negative_one

#print axioms FrameworkCarrierStress.actual_carrier_stress_bound
