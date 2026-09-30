import Mathlib
import ChainCert.Certificates

/-!
# ChainCert.Dimension -- why an acceleration scale must exist (the "ten doors" reading, as dimensional analysis on monomials)

SCOPE, stated plainly: this is DIMENSIONAL ANALYSIS ON MONOMIALS.  A quantity is a monomial in a few constants, and its
dimension is the exponent vector over (metre, second, kilogram), the convention of C1.  Nothing here is a statement about all
possible theories: a theory may use dimensionless functions of the constants, several extra constants, non-monomial
combinations, or a scale set by dynamics rather than by a constant, and none of that is covered.

The framework (`Dim`, `mono`) is the one of C1: `C1_in_framework` shows that C1's three unit equations are exactly the component
equations of `α • dc + β • dG + γ • dρ = dAcc`, reusing `C1_a0_form_iff`.

Certified here (premises ⇒ conclusions):
* `length_GMc_iff`, `length_GMc_mass_exp`: a length G^a M^b c^d has a = 1, b = 1, d = −2 (r* = G M/c²).  So
  `no_sqrtM_length_GMc`: no monomial in (G, M, c) alone is a length ∝ M^½.  Likewise `velocity_GMc_iff`: the only velocity is
  c, and `no_quarterM_velocity_GMc`: no velocity ∝ M^¼ (the BTFR scaling v⁴ ∝ M) comes from (G, M, c) alone.
* (G, M, c) is a basis of the dimension space (`basis_decomp`); `massExp x = x_L + x_T + x_M` is the mass exponent of x in that
  basis; x is dimensionally a monomial in G and c alone iff `massExp x = 0` (`GcSpan_iff`).
* ONE extra constant X: a length G^a M^½ c^d X^e exists iff `massExp X ≠ 0` (`sqrtM_length_iff`), iff (G, c, X) make an
  acceleration (`acc_from_GcX_iff`, `sqrtM_length_iff_acc`).  Every such length is r* = √(G M/A) EXACTLY as a monomial, with
  A = G^(1−2a) c^(−2d) X^(−2e) of the dimension of an acceleration (`sqrtM_length_acc`).  For the velocity:
  `quarterM_velocity_iff`, and v⁴ = G M A with A = G^(4a−1) c^(4d) X^(4e) an acceleration (`quarterM_velocity_acc`) -- the
  BTFR form of C2.
* THE FAMILY, PRECISELY: X is admissible iff its dimension is not that of a monomial in G and c.  X = a₀ gives the unique
  r* = √(G M/a₀) (`acc_unique`); X = (acceleration)·c^k gives the unique r* = √(G M c^k/X) (`acc_c_family`).  But the family is
  STRICTLY LARGER than "an acceleration times a power of c": ħ is admissible (r* = G^¾ M^½ c^(−7/4) ħ^¼, the geometric mean of
  G M/c² and the Planck length, `hbar_admissible`) and is no acceleration-power times a c-power (`hbar_not_acc_c`,
  `not_only_accelerations`); a Hubble rate, Λ, a density (the chain's ρ_Λ: `rho_length`), any mass, length or time are
  admissible too; a velocity, G, or the Planck force c⁴/G are not (`force_not_admissible`).

So the correct reading of the "ten doors" is: an M^½ length (or an M^¼ velocity) needs a constant that, with G and c, supplies
an ACCELERATION SCALE A, and then r* = √(G M/A), v⁴ = G M A.  The theorem does NOT say that the extra constant must itself be an
acceleration, and it says nothing about which acceleration nature uses: that A is a₀, and that a₀ = κ c √(G ρ_Λ), are premises
elsewhere in the chain (C1 is conditional on the (c, G, ρ) monomial family; κ = ½ is FITTED).
-/

namespace Dimension

/-- a dimension m^l s^t kg^k, recorded by its exponent vector (l, t, k) over (metre, second, kilogram), as in C1 -/
abbrev Dim := ℚ × ℚ × ℚ

/-- G: m^3 s^-2 kg^-1 -/
def dG : Dim := (3, -2, -1)
/-- a mass: kg -/
def dM : Dim := (0, 0, 1)
/-- a speed (c): m s^-1 -/
def dc : Dim := (1, -1, 0)
/-- a mass density: kg m^-3 -/
def dρ : Dim := (-3, 0, 1)
/-- a length: m -/
def dLen : Dim := (1, 0, 0)
/-- an acceleration: m s^-2 -/
def dAcc : Dim := (1, -2, 0)
/-- an action (Planck's ħ): m^2 s^-1 kg -/
def dHbar : Dim := (2, -1, 1)
/-- a force (e.g. the Planck force c^4/G): m s^-2 kg -/
def dForce : Dim := (1, -2, 1)

/-- the dimension of the monomial G^a M^b c^d -/
def mono (a b d : ℚ) : Dim := a • dG + b • dM + d • dc

/-- the mass exponent of a dimension in the (G, M, c) basis: x_L + x_T + x_M -/
def massExp (x : Dim) : ℚ := x.1 + x.2.1 + x.2.2

/-- C1 read in this framework: c^α G^β ρ^γ is an acceleration iff (α, β, γ) = (1, ½, ½) (reuses `C1_a0_form_iff`) -/
theorem C1_in_framework (α β γ : ℚ) :
    α • dc + β • dG + γ • dρ = dAcc ↔ (α = 1 ∧ β = 1 / 2 ∧ γ = 1 / 2) := by
  rw [← C1_a0_form_iff]
  simp only [dc, dG, dρ, dAcc, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq]
  constructor
  · rintro ⟨h1, h2, h3⟩
    exact ⟨by linarith, by linarith, by linarith⟩
  · rintro ⟨h1, h2, h3⟩
    exact ⟨by linarith, by linarith, by linarith⟩

/-- a length G^a M^b c^d: (a, b, d) = (1, 1, −2), i.e. r* = G M/c² -/
theorem length_GMc_iff (a b d : ℚ) : mono a b d = dLen ↔ (a = 1 ∧ b = 1 ∧ d = -2) := by
  simp only [mono, dG, dM, dc, dLen, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq]
  constructor
  · rintro ⟨h1, h2, h3⟩
    refine ⟨by linarith, by linarith, by linarith⟩
  · rintro ⟨rfl, rfl, rfl⟩
    norm_num

/-- the mass exponent of any length built from (G, M, c) is 1 -/
theorem length_GMc_mass_exp {a b d : ℚ} (h : mono a b d = dLen) : b = 1 :=
  ((length_GMc_iff a b d).mp h).2.1

/-- NO monomial in (G, M, c) alone is a length ∝ M^½ -/
theorem no_sqrtM_length_GMc : ¬ ∃ a d : ℚ, mono a (1 / 2) d = dLen := by
  rintro ⟨a, d, h⟩
  have := length_GMc_mass_exp h
  norm_num at this

/-- a velocity G^a M^b c^d: (a, b, d) = (0, 0, 1), i.e. only c -/
theorem velocity_GMc_iff (a b d : ℚ) : mono a b d = dc ↔ (a = 0 ∧ b = 0 ∧ d = 1) := by
  simp only [mono, dG, dM, dc, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq]
  constructor
  · rintro ⟨h1, h2, h3⟩
    refine ⟨by linarith, by linarith, by linarith⟩
  · rintro ⟨rfl, rfl, rfl⟩
    norm_num

/-- NO monomial in (G, M, c) alone is a velocity ∝ M^¼ (the BTFR scaling) -/
theorem no_quarterM_velocity_GMc : ¬ ∃ a d : ℚ, mono a (1 / 4) d = dc := by
  rintro ⟨a, d, h⟩
  have := ((velocity_GMc_iff a (1 / 4) d).mp h).2.1
  norm_num at this

/-- the mass exponent of G^a M^b c^d X^e is b + e · massExp X -/
theorem massExp_mono (a b d e : ℚ) (x : Dim) : massExp (mono a b d + e • x) = b + e * massExp x := by
  obtain ⟨l, t, k⟩ := x
  simp only [massExp, mono, dG, dM, dc, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul]
  ring

/-- (G, M, c) is a basis: every dimension is G^p M^q c^s with p = x_L + x_T, q = massExp x, s = −2x_L − 3x_T -/
theorem basis_decomp (x : Dim) : x = (x.1 + x.2.1) • dG + massExp x • dM + (-2 * x.1 - 3 * x.2.1) • dc := by
  obtain ⟨l, t, k⟩ := x
  simp only [massExp, dG, dM, dc, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq]
  refine ⟨by ring, by ring, by ring⟩

/-- x is dimensionally a monomial in G and c alone iff its mass exponent vanishes -/
theorem GcSpan_iff (x : Dim) : (∃ p s : ℚ, x = p • dG + s • dc) ↔ massExp x = 0 := by
  constructor
  · rintro ⟨p, s, rfl⟩
    simp only [massExp, dG, dc, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul]
    ring
  · intro h
    refine ⟨x.1 + x.2.1, -2 * x.1 - 3 * x.2.1, ?_⟩
    have := basis_decomp x
    rw [h, zero_smul, add_zero] at this
    exact this

/-- ONE EXTRA CONSTANT X: a length G^a M^½ c^d X^e exists iff X is not dimensionally a monomial in G and c
    (massExp X ≠ 0); then e = 1/(2 massExp X) -/
theorem sqrtM_length_iff (x : Dim) :
    (∃ a d e : ℚ, mono a (1 / 2) d + e • x = dLen) ↔ massExp x ≠ 0 := by
  constructor
  · rintro ⟨a, d, e, h⟩ hq
    have h1 := congrArg massExp h
    rw [massExp_mono, hq] at h1
    norm_num [massExp, dLen] at h1
  · intro hq
    obtain ⟨l, t, k⟩ := x
    simp only [massExp] at hq
    refine ⟨1 / 2 + k / (2 * (l + t + k)), -1 + (t - 2 * k) / (2 * (l + t + k)), 1 / (2 * (l + t + k)), ?_⟩
    simp only [mono, dG, dM, dc, dLen, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq]
    refine ⟨?_, ?_, ?_⟩ <;> field_simp <;> ring

/-- (G, c, X) make an acceleration X^u G^v c^w iff massExp X ≠ 0; then u = −1/massExp X -/
theorem acc_from_GcX_iff (x : Dim) :
    (∃ u v w : ℚ, u • x + v • dG + w • dc = dAcc) ↔ massExp x ≠ 0 := by
  constructor
  · rintro ⟨u, v, w, h⟩ hq
    obtain ⟨l, t, k⟩ := x
    simp only [massExp] at hq
    simp only [dG, dc, dAcc, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq] at h
    obtain ⟨h1, h2, h3⟩ := h
    have : u * (l + t + k) = -1 := by linear_combination h1 + h2 + h3
    rw [hq, mul_zero] at this
    norm_num at this
  · intro hq
    obtain ⟨l, t, k⟩ := x
    simp only [massExp] at hq
    refine ⟨-1 / (l + t + k), -k / (l + t + k), 1 + (l + 3 * k) / (l + t + k), ?_⟩
    simp only [dG, dc, dAcc, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq]
    refine ⟨?_, ?_, ?_⟩ <;> field_simp <;> ring

/-- the length ∝ M^½ exists iff (G, c, X) supply an acceleration scale -/
theorem sqrtM_length_iff_acc (x : Dim) :
    (∃ a d e : ℚ, mono a (1 / 2) d + e • x = dLen) ↔ (∃ u v w : ℚ, u • x + v • dG + w • dc = dAcc) := by
  rw [sqrtM_length_iff, acc_from_GcX_iff]

/-- EVERY length r* = G^a M^½ c^d X^e is r* = √(G M/A) exactly as a monomial, where A = G^(1−2a) c^(−2d) X^(−2e) has the
    dimension of an acceleration (2(a, ½, d, e) = (1, 1, 0, 0) − (1−2a, 0, −2d, −2e) holds identically) -/
theorem sqrtM_length_acc {a d e : ℚ} {x : Dim} (h : mono a (1 / 2) d + e • x = dLen) :
    (1 - 2 * a) • dG + (-2 * d) • dc + (-2 * e) • x = dAcc := by
  obtain ⟨l, t, k⟩ := x
  simp only [mono, dG, dM, dc, dLen, dAcc, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq] at h ⊢
  obtain ⟨h1, h2, h3⟩ := h
  refine ⟨by linear_combination -2 * h1, by linear_combination -2 * h2, by linear_combination -2 * h3⟩

/-- X = a₀ an acceleration: the unique length ∝ M^½ is r* = √(G M/a₀) -/
theorem acc_unique (a d e : ℚ) : mono a (1 / 2) d + e • dAcc = dLen ↔ (a = 1 / 2 ∧ d = 0 ∧ e = -1 / 2) := by
  simp only [mono, dG, dM, dc, dLen, dAcc, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq]
  constructor
  · rintro ⟨h1, h2, h3⟩
    refine ⟨by linarith, by linarith, by linarith⟩
  · rintro ⟨rfl, rfl, rfl⟩
    norm_num

/-- X = (an acceleration) · c^k: the unique length ∝ M^½ is r* = √(G M c^k/X) (a = ½, d = k/2, e = −½) -/
theorem acc_c_family (k a d e : ℚ) :
    mono a (1 / 2) d + e • (dAcc + k • dc) = dLen ↔ (a = 1 / 2 ∧ d = k / 2 ∧ e = -1 / 2) := by
  simp only [mono, dG, dM, dc, dLen, dAcc, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq]
  constructor
  · rintro ⟨h1, h2, h3⟩
    have ha : a = 1 / 2 := by linarith
    have he : e = -1 / 2 := by linear_combination ha - h1 - h2
    subst ha he
    refine ⟨rfl, by linarith, rfl⟩
  · rintro ⟨rfl, rfl, rfl⟩
    refine ⟨by ring, by ring, by ring⟩

/-- ħ IS admissible: r* = G^¾ M^½ c^(−7/4) ħ^¼ is a length ∝ M^½ (the geometric mean of G M/c² and the Planck length) -/
theorem hbar_admissible : mono (3 / 4) (1 / 2) (-7 / 4) + (1 / 4 : ℚ) • dHbar = dLen := by
  simp only [mono, dG, dM, dc, dLen, dHbar, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq]
  norm_num

/-- ... and ħ is not (an acceleration)^j · c^k for any j, k (its mass exponent is 1, theirs 0) -/
theorem hbar_not_acc_c : ¬ ∃ j k : ℚ, dHbar = j • dAcc + k • dc := by
  rintro ⟨j, k, h⟩
  simp only [dHbar, dAcc, dc, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq] at h
  obtain ⟨_, _, h3⟩ := h
  norm_num at h3

/-- so "X must be an acceleration times a power of c" is FALSE as a statement about the monomial family: the admissible
    family is exactly massExp X ≠ 0 (`sqrtM_length_iff`), and it contains constants that are not of that form -/
theorem not_only_accelerations :
    ∃ x : Dim, (∃ a d e : ℚ, mono a (1 / 2) d + e • x = dLen) ∧ ¬ ∃ j k : ℚ, x = j • dAcc + k • dc :=
  ⟨dHbar, ⟨3 / 4, -7 / 4, 1 / 4, hbar_admissible⟩, hbar_not_acc_c⟩

/-- a force (e.g. the Planck force c⁴/G) is NOT admissible: it is dimensionally a G-c monomial -/
theorem force_not_admissible : ¬ ∃ a d e : ℚ, mono a (1 / 2) d + e • dForce = dLen := by
  rw [sqrtM_length_iff]
  simp [massExp, dForce]
  norm_num

/-- the chain's own extra constant ρ_Λ is admissible (massExp ρ = −2): r* = G^¼ M^½ c^(−½) ρ^(−¼) = √(G M/(c √(G ρ))), whose
    acceleration c √(G ρ) is C1's form (`C1_in_framework`) -/
theorem rho_length : mono (1 / 4) (1 / 2) (-1 / 2) + (-1 / 4 : ℚ) • dρ = dLen := by
  simp only [mono, dG, dM, dc, dLen, dρ, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq]
  norm_num

/-- the velocity form: a velocity G^a M^¼ c^d X^e exists iff massExp X ≠ 0 -/
theorem quarterM_velocity_iff (x : Dim) :
    (∃ a d e : ℚ, mono a (1 / 4) d + e • x = dc) ↔ massExp x ≠ 0 := by
  constructor
  · rintro ⟨a, d, e, h⟩ hq
    have h1 := congrArg massExp h
    rw [massExp_mono, hq] at h1
    norm_num [massExp, dc] at h1
  · intro hq
    obtain ⟨l, t, k⟩ := x
    simp only [massExp] at hq
    refine ⟨1 / 4 - k / (4 * (l + t + k)), 1 / 4 + (3 * k + l) / (4 * (l + t + k)), -1 / (4 * (l + t + k)), ?_⟩
    simp only [mono, dG, dM, dc, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq]
    refine ⟨?_, ?_, ?_⟩ <;> field_simp <;> ring

/-- EVERY velocity v = G^a M^¼ c^d X^e satisfies v⁴ = G M A exactly as a monomial, with A = G^(4a−1) c^(4d) X^(4e) of the
    dimension of an acceleration: the BTFR form v⁴ = G M a₀ of C2 -/
theorem quarterM_velocity_acc {a d e : ℚ} {x : Dim} (h : mono a (1 / 4) d + e • x = dc) :
    (4 * a - 1) • dG + (4 * d) • dc + (4 * e) • x = dAcc := by
  obtain ⟨l, t, k⟩ := x
  simp only [mono, dG, dM, dc, dAcc, Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul, Prod.mk.injEq] at h ⊢
  obtain ⟨h1, h2, h3⟩ := h
  refine ⟨by linear_combination 4 * h1, by linear_combination 4 * h2, by linear_combination 4 * h3⟩

end Dimension
