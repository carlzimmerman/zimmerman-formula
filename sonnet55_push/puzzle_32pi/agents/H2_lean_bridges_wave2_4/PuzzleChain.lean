import Mathlib
import P3_record_iff
import P7_offset_family
import P8_omega_lambda

open Real

/-!
# PuzzleChain: every reading of the puzzle is ONE premise, and that premise is NOT a theorem of the definitions

WHAT LEAN CERTIFIES HERE (premises => conclusions only).  NOTHING here proves kappa = 1/2, a0 = sqrt(G rho)/2 or Lambda = 32 pi a0^2 as physics, and nothing shows
that any route DERIVES them.  The "chain" shows exactly this: under the stated DEFINITIONS, sixteen different-looking statements are logically equivalent to the single
hypothesis `OpenPremise` (Lambda = 32 pi a0^2), and the definitions alone do not imply it (explicit witness models where all definitions hold and every form fails,
and a family of models with an arbitrary Z).  So every reading of the puzzle reduces to ONE open premise; none of them is a theorem.

Conventions (c = G = 1).  A `Setup` is (a0, L, H0, Omega_Lambda) with a0, L, H0, Omega_Lambda > 0 and the flatness/definition relation 3 H0^2 Omega_Lambda = 3/L^2 (Lambda = 3 H0^2 Omega_Lambda = 3/L^2).
Definitions: Lambda = 3/L^2, rho = Lambda/(8 pi), H = 1/L, Z = H/a0, kappa = a0/sqrt(rho), R* = t_Lambda = 1/sqrt(rho), the Schwarzschild horizon of surface gravity a0 has r_s = 1/(2 a0)
(kappa = 1/(4M), r_s = 2M) and area A = 4 pi r_s^2 = pi/a0^2, the Rindler length is 1/a0, the memory moment M1 = (2/3)/a0 (record; = (2/3) R_c for the sharp kernel, P3 `Rc_iff`, so R_c = (3/2) M1),
the channel count N = sqrt(rho)/a0 (= 1/kappa, P3 `N_two_iff`), U_v = Lambda/a0^2 (Poisson units), W_v = rho/a0^2 (a0^2/G units), the Sciama integral I(R) = 2 pi rho R^2 (P3), the offset
coefficient c_off = 8 pi rho/a0^2 (P7), the pure-tension wall tension sigma_0 = a0/(2 pi) (P1: proper acceleration 2 pi sigma = a0), the sheet densities Sigma_Lambda = rho R*, Sigma_M = a0/(2 pi).

THE TFAE (`chain_tfae`, one theorem `iff_premise` per form):
 1 Lambda = 32 pi a0^2 (`OpenPremise`)   2 G rho = 4 a0^2   3 kappa = 1/2   4 A Lambda = 32 pi^2   5 Rindler length = 2 R*   6 U_v = 32 pi   7 W_v = 4   8 M1 = (4/3) t_Lambda
 9 R_c = 2 R* (R_c = (3/2) M1)   10 N = 2   11 Z^2 = 32 pi/3 (a0 = H/Z)   12 Omega_Lambda = 32 pi a0^2/(3 H0^2)   13 Sciama I(R_c) = 8 pi   14 c_off = 32 pi
 15 rho = 16 pi^2 sigma_0^2   16 Sigma_Lambda = 4 pi Sigma_M.
NONE IS A THEOREM (`none_is_theorem`): witness `S_off` (a0 = H: Z = 1, kappa = sqrt(8 pi/3), A Lambda = 3 pi, ...) satisfies all definitions and fails every form (`all_fail_S_off`); witness `S_on`
satisfies every form (so the TFAE is not vacuous).  `Z_free`: for EVERY Z' > 0 there is a Setup with Z = Z' (`S_Z`), and the premise holds there iff Z'^2 = 32 pi/3 (the definitions leave Z free);
`family_values`/`family_targets_iff`: in that family the forms are DIFFERENT functions of Z' (A Lambda = 3 pi Z'^2, U_v = 3 Z'^2, W_v = 3 Z'^2/(8 pi), kappa^2 = 8 pi/(3 Z'^2), ...) that meet their
puzzle targets at the single point Z'^2 = 32 pi/3;
`Zkappa_relation`: Z^2 kappa^2 = 8 pi/3 in every Setup.
FALSE FRIENDS (`false_friends`): statements that hold in EVERY Setup (rho_Lambda A_dS = 6 F_max; A_dS Lambda = 12 pi; S_dS = pi L^2 with A_dS = 4 pi L^2) cannot be equivalent to the premise.
ARITHMETIC OF Z (P7/H7 style): `Z_sq_irrational`, `Z_irrational`: Z^2 = 32 pi/3 and Z, a0/H = sqrt(3/(32 pi)) are irrational (unconditional, irrational_pi); `Z_not_algebraic`, `aH_not_algebraic`:
NOT ALGEBRAIC, conditional on the explicit hypothesis `Transcendental Q pi` (Lindemann is not in Mathlib).  kappa = 1/2 is rational while Z is transcendental (`kappa_rational_Z_irrational`).
LINKS to the per-lane theorems (c = G = 1 instances): `link_P3_M1`, `link_P7_offset`, `link_P8_omega`.
-/

namespace PuzzleChain

/-- a model of the definitions: a0, L, H0, Omega_Lambda > 0 with Lambda = 3 H0^2 Omega_Lambda = 3/L^2 (c = G = 1) -/
structure Setup where
  a0 : ℝ
  L : ℝ
  H0 : ℝ
  Om : ℝ
  a0_pos : 0 < a0
  L_pos : 0 < L
  H0_pos : 0 < H0
  Om_pos : 0 < Om
  flat : 3 * H0 ^ 2 * Om = 3 / L ^ 2

namespace Setup

variable (S : Setup)

noncomputable def Lam : ℝ := 3 / S.L ^ 2
noncomputable def rho : ℝ := S.Lam / (8 * π)
noncomputable def H : ℝ := 1 / S.L
noncomputable def Z : ℝ := S.H / S.a0
noncomputable def kappa : ℝ := S.a0 / Real.sqrt S.rho
noncomputable def Rstar : ℝ := 1 / Real.sqrt S.rho
noncomputable def rs : ℝ := 1 / (2 * S.a0)
noncomputable def area : ℝ := 4 * π * S.rs ^ 2
noncomputable def rindler : ℝ := 1 / S.a0
noncomputable def M1 : ℝ := (2 / 3) / S.a0
noncomputable def Rc : ℝ := (3 / 2) * S.M1
noncomputable def Nchan : ℝ := Real.sqrt S.rho / S.a0
noncomputable def Uv : ℝ := S.Lam / S.a0 ^ 2
noncomputable def Wv : ℝ := S.rho / S.a0 ^ 2
noncomputable def sciama : ℝ := 2 * π * S.rho * S.Rc ^ 2
noncomputable def coff : ℝ := 8 * π * S.rho / S.a0 ^ 2
noncomputable def sigma0 : ℝ := S.a0 / (2 * π)
noncomputable def SigL : ℝ := S.rho * S.Rstar
noncomputable def SigM : ℝ := S.a0 / (2 * π)

theorem Lam_pos : 0 < S.Lam := by unfold Lam; have := S.L_pos; positivity
theorem rho_pos : 0 < S.rho := by
  unfold rho; have := S.Lam_pos; have := Real.pi_pos; positivity
theorem sqrt_rho_pos : 0 < Real.sqrt S.rho := Real.sqrt_pos.mpr S.rho_pos
theorem sqrt_rho_sq : Real.sqrt S.rho ^ 2 = S.rho := Real.sq_sqrt S.rho_pos.le
theorem Lam_flat : S.Lam = 3 * S.H0 ^ 2 * S.Om := by unfold Lam; rw [S.flat]

/-- key 1: rho = 4 a0^2 <=> Lambda = 32 pi a0^2 -/
theorem rho_iff : S.rho = 4 * S.a0 ^ 2 ↔ S.Lam = 32 * π * S.a0 ^ 2 := by
  have hp := Real.pi_pos
  unfold rho
  rw [div_eq_iff (by positivity)]
  constructor <;> intro h <;> linarith

/-- key 2: sqrt rho = 2 a0 <=> rho = 4 a0^2 -/
theorem sqrt_iff : Real.sqrt S.rho = 2 * S.a0 ↔ S.rho = 4 * S.a0 ^ 2 := by
  have h2 := S.sqrt_rho_sq
  have hs := S.sqrt_rho_pos
  have ha := S.a0_pos
  constructor
  · intro h; rw [← h2, h]; ring
  · intro h
    have : Real.sqrt S.rho ^ 2 = (2 * S.a0) ^ 2 := by rw [h2, h]; ring
    exact (sq_eq_sq₀ hs.le (by positivity)).mp this

end Setup

/-- THE single open premise: Lambda = 32 pi a0^2 -/
structure OpenPremise (S : Setup) : Prop where
  lam_eq : S.Lam = 32 * π * S.a0 ^ 2

/-- the sixteen forms -/
inductive Form
  | premise | grho | kappa | area | rindler | Uv | Wv | M1 | Rc | N | Zsq | omega | sciama | offset | wall | sheet
  deriving DecidableEq

def Form.holds (f : Form) (S : Setup) : Prop :=
  match f with
  | .premise => OpenPremise S
  | .grho => S.rho = 4 * S.a0 ^ 2
  | .kappa => S.kappa = 1 / 2
  | .area => S.area * S.Lam = 32 * π ^ 2
  | .rindler => S.rindler = 2 * S.Rstar
  | .Uv => S.Uv = 32 * π
  | .Wv => S.Wv = 4
  | .M1 => S.M1 = (4 / 3) * S.Rstar
  | .Rc => S.Rc = 2 * S.Rstar
  | .N => S.Nchan = 2
  | .Zsq => S.Z ^ 2 = 32 * π / 3
  | .omega => S.Om = 32 * π * S.a0 ^ 2 / (3 * S.H0 ^ 2)
  | .sciama => S.sciama = 8 * π
  | .offset => S.coff = 32 * π
  | .wall => S.rho = 16 * π ^ 2 * S.sigma0 ^ 2
  | .sheet => S.SigL = 4 * π * S.SigM

def allForms : List Form :=
  [.premise, .grho, .kappa, .area, .rindler, .Uv, .Wv, .M1, .Rc, .N, .Zsq, .omega, .sciama, .offset, .wall, .sheet]

/-- each form is equivalent to the premise -/
theorem iff_premise (f : Form) (S : Setup) : f.holds S ↔ OpenPremise S := by
  have hp := Real.pi_pos
  have ha := S.a0_pos
  have hL := S.L_pos
  have ha0 : S.a0 ≠ 0 := ha.ne'
  have hL0 : S.L ≠ 0 := hL.ne'
  have hs := S.sqrt_rho_pos
  have hs0 : Real.sqrt S.rho ≠ 0 := hs.ne'
  have hlam : OpenPremise S ↔ S.Lam = 32 * π * S.a0 ^ 2 := ⟨fun h => h.lam_eq, fun h => ⟨h⟩⟩
  have hkey := S.rho_iff
  have hsq := S.sqrt_iff
  rw [hlam]
  cases f with
  | premise => exact hlam
  | grho => exact hkey
  | kappa =>
    show S.a0 / Real.sqrt S.rho = 1 / 2 ↔ _
    rw [← hkey, ← hsq, div_eq_iff hs0]
    constructor <;> intro h <;> linarith
  | area =>
    show (4 * π * (1 / (2 * S.a0)) ^ 2) * S.Lam = 32 * π ^ 2 ↔ _
    have : (4 * π * (1 / (2 * S.a0)) ^ 2) * S.Lam = (π / S.a0 ^ 2) * S.Lam := by field_simp; norm_num
    rw [this]
    have h2 : S.a0 ^ 2 ≠ 0 := pow_ne_zero 2 ha0
    rw [div_mul_eq_mul_div, div_eq_iff h2]
    constructor <;> intro h <;> nlinarith [h, mul_pos hp hp]
  | rindler =>
    show 1 / S.a0 = 2 * (1 / Real.sqrt S.rho) ↔ _
    rw [← hkey, ← hsq]
    rw [div_eq_iff ha0]
    constructor
    · intro h
      field_simp at h
      linarith
    · intro h; rw [h]; field_simp
  | Uv =>
    show S.Lam / S.a0 ^ 2 = 32 * π ↔ _
    rw [div_eq_iff (pow_ne_zero 2 ha0)]
  | Wv =>
    show S.rho / S.a0 ^ 2 = 4 ↔ _
    rw [← hkey, div_eq_iff (pow_ne_zero 2 ha0)]
  | M1 =>
    show (2 / 3) / S.a0 = (4 / 3) * (1 / Real.sqrt S.rho) ↔ _
    rw [← hkey, ← hsq]
    constructor
    · intro h
      field_simp at h
      linarith
    · intro h; rw [h]; field_simp; ring
  | Rc =>
    show (3 / 2) * ((2 / 3) / S.a0) = 2 * (1 / Real.sqrt S.rho) ↔ _
    rw [← hkey, ← hsq]
    constructor
    · intro h
      field_simp at h
      linarith
    · intro h; rw [h]; field_simp
  | N =>
    show Real.sqrt S.rho / S.a0 = 2 ↔ _
    rw [← hkey, ← hsq, div_eq_iff ha0]
  | Zsq =>
    show (S.H / S.a0) ^ 2 = 32 * π / 3 ↔ _
    have hH : S.H = 1 / S.L := rfl
    have hLam : S.Lam = 3 / S.L ^ 2 := rfl
    rw [hH, hLam]
    have h2 : S.a0 ^ 2 * S.L ^ 2 ≠ 0 := by positivity
    have : (1 / S.L / S.a0) ^ 2 = 1 / (S.a0 ^ 2 * S.L ^ 2) := by field_simp
    rw [this, div_eq_div_iff h2 (by norm_num), div_eq_iff (pow_ne_zero 2 hL0)]
    constructor <;> intro h <;> nlinarith [h, mul_pos hp hp]
  | omega =>
    show S.Om = 32 * π * S.a0 ^ 2 / (3 * S.H0 ^ 2) ↔ _
    have hH0 : S.H0 ≠ 0 := S.H0_pos.ne'
    rw [eq_div_iff (by positivity), S.Lam_flat]
    constructor <;> intro h <;> nlinarith [h]
  | sciama =>
    show 2 * π * S.rho * ((3 / 2) * ((2 / 3) / S.a0)) ^ 2 = 8 * π ↔ _
    rw [← hkey]
    have : 2 * π * S.rho * ((3 / 2) * ((2 / 3) / S.a0)) ^ 2 = 2 * π * S.rho / S.a0 ^ 2 := by field_simp
    rw [this, div_eq_iff (pow_ne_zero 2 ha0)]
    constructor
    · intro h
      have : π * (S.rho - 4 * S.a0 ^ 2) = 0 := by nlinarith [h]
      rcases mul_eq_zero.mp this with h1 | h1
      · exact absurd h1 hp.ne'
      · linarith
    · intro h; rw [h]; ring
  | offset =>
    show 8 * π * S.rho / S.a0 ^ 2 = 32 * π ↔ _
    rw [← hkey, div_eq_iff (pow_ne_zero 2 ha0)]
    constructor
    · intro h
      have : π * (S.rho - 4 * S.a0 ^ 2) = 0 := by nlinarith [h]
      rcases mul_eq_zero.mp this with h1 | h1
      · exact absurd h1 hp.ne'
      · linarith
    · intro h; rw [h]; ring
  | wall =>
    show S.rho = 16 * π ^ 2 * (S.a0 / (2 * π)) ^ 2 ↔ _
    rw [← hkey]
    have : 16 * π ^ 2 * (S.a0 / (2 * π)) ^ 2 = 4 * S.a0 ^ 2 := by field_simp; ring
    rw [this]
  | sheet =>
    show S.rho * (1 / Real.sqrt S.rho) = 4 * π * (S.a0 / (2 * π)) ↔ _
    rw [← hkey, ← hsq]
    have hL' : S.rho * (1 / Real.sqrt S.rho) = Real.sqrt S.rho := by
      rw [mul_one_div, div_eq_iff hs0]; nlinarith [S.sqrt_rho_sq]
    have hR : 4 * π * (S.a0 / (2 * π)) = 2 * S.a0 := by field_simp; ring
    rw [hL', hR]

theorem allForms_length : allForms.length = 16 := rfl

/-- the sixteen forms are sixteen distinct statements (distinct constructors) -/
theorem allForms_nodup : allForms.Nodup := by decide

/-- the chain: all sixteen forms are equivalent (TFAE) -/
theorem chain_tfae (S : Setup) : List.TFAE (allForms.map (fun f => f.holds S)) := by
  apply List.tfae_of_forall (b := OpenPremise S)
  intro a ha
  simp only [List.mem_map] at ha
  obtain ⟨f, _, rfl⟩ := ha
  exact iff_premise f S

/-- any two forms are equivalent -/
theorem forms_equiv (f g : Form) (S : Setup) : f.holds S ↔ g.holds S := (iff_premise f S).trans (iff_premise g S).symm

/-! the witnesses -/

/-- a model with a0 = H (Z = 1): every definition holds, every form fails -/
noncomputable def S_off : Setup where
  a0 := 1
  L := 1
  H0 := 1
  Om := 1
  a0_pos := one_pos
  L_pos := one_pos
  H0_pos := one_pos
  Om_pos := one_pos
  flat := by norm_num

theorem S_off_not_premise : ¬ OpenPremise S_off := by
  intro h
  have hp := Real.pi_gt_three
  have := h.lam_eq
  unfold Setup.Lam S_off at this
  norm_num at this
  nlinarith

theorem all_fail_S_off (f : Form) : ¬ f.holds S_off := fun h => S_off_not_premise ((iff_premise f S_off).mp h)

/-- a model with a0 = H/Z, Z^2 = 32 pi/3 (L = 1, a0 = 1/Z, H0 = 1, Omega = 1): every form holds -/
noncomputable def S_on : Setup where
  a0 := 1 / Real.sqrt (32 * π / 3)
  L := 1
  H0 := 1
  Om := 1
  a0_pos := by
    have hp := Real.pi_pos
    exact one_div_pos.mpr (Real.sqrt_pos.mpr (by positivity))
  L_pos := one_pos
  H0_pos := one_pos
  Om_pos := one_pos
  flat := by norm_num

theorem S_on_premise : OpenPremise S_on := by
  have hp := Real.pi_pos
  have h2 := Real.sq_sqrt (show 0 ≤ 32 * π / 3 by positivity)
  refine ⟨?_⟩
  unfold Setup.Lam S_on
  simp only
  rw [div_pow, one_pow, h2]
  field_simp

theorem all_hold_S_on (f : Form) : f.holds S_on := (iff_premise f S_on).mpr S_on_premise

/-- NONE of the forms is a theorem of the definitions alone -/
theorem none_is_theorem (f : Form) : ¬ (∀ S : Setup, f.holds S) := fun h => all_fail_S_off f (h S_off)

/-- ... yet each is satisfiable, so the equivalences are not vacuous -/
theorem each_satisfiable (f : Form) : ∃ S : Setup, f.holds S := ⟨S_on, all_hold_S_on f⟩

theorem each_can_fail (f : Form) : ∃ S : Setup, ¬ f.holds S := ⟨S_off, all_fail_S_off f⟩

/-- in the witness S_off (a0 = H): Z = 1, kappa^2 = 8 pi/3 (= the value kappa = sqrt(8 pi/3) = 2.894, Z = 1), A Lambda = 3 pi != 32 pi^2, U_v = 3, W_v = 3/(8 pi), N^2 = 3/(8 pi) -/
theorem S_off_values :
    S_off.Z = 1 ∧ S_off.kappa ^ 2 = 8 * π / 3 ∧ S_off.area * S_off.Lam = 3 * π ∧ S_off.Uv = 3 ∧ S_off.Wv = 3 / (8 * π) ∧
    S_off.Nchan ^ 2 = 3 / (8 * π) := by
  have hp := Real.pi_pos
  have hs2 : Real.sqrt S_off.rho ^ 2 = S_off.rho := Setup.sqrt_rho_sq S_off
  have hrho : S_off.rho = 3 / (8 * π) := by
    unfold Setup.rho Setup.Lam S_off; simp
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold Setup.Z Setup.H S_off; simp
  · unfold Setup.kappa
    rw [div_pow, hs2, hrho]
    unfold S_off; simp
  · unfold Setup.area Setup.rs Setup.Lam S_off; simp; ring
  · unfold Setup.Uv Setup.Lam S_off; simp
  · unfold Setup.Wv; rw [hrho]; unfold S_off; simp
  · unfold Setup.Nchan
    rw [div_pow, hs2, hrho]
    unfold S_off; simp

/-- the one-parameter family of models with arbitrary Z' > 0: a0 = 1/Z', L = H0 = Omega_Lambda = 1 (so H = 1, Lambda = 3, rho = 3/(8 pi)) -/
noncomputable def S_Z (Z' : ℝ) (hZ : 0 < Z') : Setup where
  a0 := 1 / Z'
  L := 1
  H0 := 1
  Om := 1
  a0_pos := one_div_pos.mpr hZ
  L_pos := one_pos
  H0_pos := one_pos
  Om_pos := one_pos
  flat := by norm_num

theorem S_Z_Z {Z' : ℝ} (hZ : 0 < Z') : (S_Z Z' hZ).Z = Z' := by
  show (1 / (1:ℝ)) / (1 / Z') = Z'
  field_simp

/-- the definitions leave Z free: for every Z' > 0 there is a Setup with Z = Z', and the premise holds there iff Z'^2 = 32 pi/3 -/
theorem Z_free {Z' : ℝ} (hZ : 0 < Z') :
    ∃ S : Setup, S.Z = Z' ∧ (OpenPremise S ↔ Z' ^ 2 = 32 * π / 3) := by
  refine ⟨S_Z Z' hZ, S_Z_Z hZ, ?_⟩
  have := iff_premise .Zsq (S_Z Z' hZ)
  unfold Form.holds at this
  rw [S_Z_Z hZ] at this
  exact this.symm

/-- the forms as FUNCTIONS of Z' in the family S_Z: A Lambda = 3 pi Z'^2, U_v = 3 Z'^2, W_v = 3 Z'^2/(8 pi), N^2 = 3 Z'^2/(8 pi), kappa^2 = 8 pi/(3 Z'^2), Sciama I(R_c) = 3 Z'^2/4,
    c_off = 3 Z'^2 -- distinct functions that meet their puzzle targets (32 pi^2, 32 pi, 4, 4, 1/4, 8 pi, 32 pi) at the SAME point Z'^2 = 32 pi/3 and nowhere else -/
theorem family_values {Z' : ℝ} (hZ : 0 < Z') :
    (S_Z Z' hZ).area * (S_Z Z' hZ).Lam = 3 * π * Z' ^ 2 ∧ (S_Z Z' hZ).Uv = 3 * Z' ^ 2 ∧ (S_Z Z' hZ).Wv = 3 * Z' ^ 2 / (8 * π) ∧
    (S_Z Z' hZ).Nchan ^ 2 = 3 * Z' ^ 2 / (8 * π) ∧ (S_Z Z' hZ).kappa ^ 2 = 8 * π / (3 * Z' ^ 2) ∧
    (S_Z Z' hZ).sciama = 3 * Z' ^ 2 / 4 ∧ (S_Z Z' hZ).coff = 3 * Z' ^ 2 := by
  have hp := Real.pi_pos
  have hZ0 : Z' ≠ 0 := hZ.ne'
  set S := S_Z Z' hZ with hS
  have hLam : S.Lam = 3 := by rw [hS]; unfold Setup.Lam S_Z; simp
  have hrho : S.rho = 3 / (8 * π) := by unfold Setup.rho; rw [hLam]
  have ha : S.a0 = 1 / Z' := rfl
  have hs2 := S.sqrt_rho_sq
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold Setup.area Setup.rs; rw [hLam, ha]; field_simp; ring
  · unfold Setup.Uv; rw [hLam, ha]; field_simp
  · unfold Setup.Wv; rw [hrho, ha]; field_simp
  · unfold Setup.Nchan; rw [div_pow, hs2, hrho, ha]; field_simp
  · unfold Setup.kappa; rw [div_pow, hs2, hrho, ha]; field_simp
  · unfold Setup.sciama Setup.Rc Setup.M1; rw [hrho, ha]; field_simp; ring
  · unfold Setup.coff; rw [hrho, ha]; field_simp

/-- each of those functions hits its target exactly when Z'^2 = 32 pi/3 -/
theorem family_targets_iff {Z' : ℝ} (hZ : 0 < Z') :
    (3 * π * Z' ^ 2 = 32 * π ^ 2 ↔ Z' ^ 2 = 32 * π / 3) ∧ (3 * Z' ^ 2 = 32 * π ↔ Z' ^ 2 = 32 * π / 3) ∧
    (3 * Z' ^ 2 / (8 * π) = 4 ↔ Z' ^ 2 = 32 * π / 3) ∧ (8 * π / (3 * Z' ^ 2) = 1 / 4 ↔ Z' ^ 2 = 32 * π / 3) ∧
    (3 * Z' ^ 2 / 4 = 8 * π ↔ Z' ^ 2 = 32 * π / 3) := by
  have hp := Real.pi_pos
  have hZ2 : 0 < Z' ^ 2 := by positivity
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · constructor <;> intro h <;> nlinarith [h, mul_pos hp hp]
  · constructor <;> intro h <;> linarith
  · rw [div_eq_iff (by positivity)]; constructor <;> intro h <;> linarith
  · rw [div_eq_div_iff (by positivity) (by norm_num)]; constructor <;> intro h <;> linarith
  · rw [div_eq_iff (by norm_num)]; constructor <;> intro h <;> linarith

/-- Z^2 kappa^2 = 8 pi/3 in every Setup -/
theorem Zkappa_relation (S : Setup) : S.Z ^ 2 * S.kappa ^ 2 = 8 * π / 3 := by
  have hp := Real.pi_pos
  have hL := S.L_pos
  have ha := S.a0_pos
  have hs2 := S.sqrt_rho_sq
  have hk : (S.a0 / Real.sqrt S.rho) ^ 2 = S.a0 ^ 2 / S.rho := by rw [div_pow, hs2]
  have hz : ((1 / S.L) / S.a0) ^ 2 = 1 / (S.L ^ 2 * S.a0 ^ 2) := by field_simp
  have hrho : S.rho = 3 / (8 * π * S.L ^ 2) := by unfold Setup.rho Setup.Lam; field_simp
  unfold Setup.Z Setup.kappa Setup.H
  rw [hk, hz, hrho]
  field_simp

/-! false friends: identities that hold in EVERY Setup, hence not equivalent to the premise -/

theorem false_friends (S : Setup) :
    S.rho * (4 * π * S.L ^ 2) = 6 * (1 / 4) ∧ (4 * π * S.L ^ 2) * S.Lam = 12 * π := by
  have hp := Real.pi_pos
  have hL := S.L_pos
  have hL0 : S.L ≠ 0 := hL.ne'
  unfold Setup.rho Setup.Lam
  constructor <;> field_simp <;> ring

theorem false_friend_not_premise : ¬ (∀ S : Setup, OpenPremise S) ∧ ∀ S : Setup, S.rho * (4 * π * S.L ^ 2) = 6 * (1 / 4) :=
  ⟨none_is_theorem .premise, fun S => (false_friends S).1⟩

/-! irrationality / transcendence of Z -/

theorem Z_sq_irrational : Irrational (32 * π / 3) := by
  have h1 : Irrational (32 * π) := by
    have := irrational_pi.ratCast_mul (q := 32) (by norm_num)
    simpa using this
  have := h1.div_ratCast (q := 3) (by norm_num)
  simpa using this

/-- Z = sqrt(32 pi/3) is irrational (if it were rational its square would be) -/
theorem Z_irrational : Irrational (Real.sqrt (32 * π / 3)) := by
  intro ⟨q, hq⟩
  apply Z_sq_irrational
  refine ⟨q ^ 2, ?_⟩
  have h2 := Real.sq_sqrt (show 0 ≤ 32 * π / 3 by positivity)
  rw [← h2, ← hq]; push_cast; ring

/-- a0/H = sqrt(3/(32 pi)) is irrational -/
theorem aH_irrational : Irrational (Real.sqrt (3 / (32 * π))) := by
  intro ⟨q, hq⟩
  have hp := Real.pi_pos
  have hq0 : (q : ℝ) ≠ 0 := by
    intro h0
    rw [h0] at hq
    have : Real.sqrt (3 / (32 * π)) > 0 := Real.sqrt_pos.mpr (by positivity)
    rw [← hq] at this; simp at this
  have h2 := Real.sq_sqrt (show 0 ≤ 3 / (32 * π) by positivity)
  have h3 : (q : ℝ) ^ 2 = 3 / (32 * π) := by rw [hq]; exact h2
  apply Z_sq_irrational
  refine ⟨1 / q ^ 2, ?_⟩
  push_cast
  rw [h3]; field_simp

/-- CONDITIONAL on `Transcendental Q pi` (explicit hypothesis): Z is not algebraic -/
theorem Z_not_algebraic (hπ : Transcendental ℚ π) : ¬ IsAlgebraic ℚ (Real.sqrt (32 * π / 3)) := by
  intro h
  have hp := Real.pi_pos
  have h2 := Real.sq_sqrt (show 0 ≤ 32 * π / 3 by positivity)
  have hmem : Real.sqrt (32 * π / 3) ∈ algebraicClosure ℚ ℝ := (mem_algebraicClosure_iff).mpr h
  have hsq : Real.sqrt (32 * π / 3) ^ 2 ∈ algebraicClosure ℚ ℝ := (algebraicClosure ℚ ℝ).pow_mem hmem 2
  rw [h2] at hsq
  have h3 : ((3 / 32 : ℚ) : ℝ) ∈ algebraicClosure ℚ ℝ := (algebraicClosure ℚ ℝ).algebraMap_mem _
  have h4 := (algebraicClosure ℚ ℝ).mul_mem h3 hsq
  have e : ((3 / 32 : ℚ) : ℝ) * (32 * π / 3) = π := by push_cast; ring
  rw [e] at h4
  exact hπ ((mem_algebraicClosure_iff).mp h4)

/-- CONDITIONAL: a0/H = sqrt(3/(32 pi)) is not algebraic -/
theorem aH_not_algebraic (hπ : Transcendental ℚ π) : ¬ IsAlgebraic ℚ (Real.sqrt (3 / (32 * π))) := by
  intro h
  have hp := Real.pi_pos
  have h2 := Real.sq_sqrt (show 0 ≤ 3 / (32 * π) by positivity)
  have hmem : Real.sqrt (3 / (32 * π)) ∈ algebraicClosure ℚ ℝ := (mem_algebraicClosure_iff).mpr h
  have hsq : Real.sqrt (3 / (32 * π)) ^ 2 ∈ algebraicClosure ℚ ℝ := (algebraicClosure ℚ ℝ).pow_mem hmem 2
  rw [h2] at hsq
  have hinv : (3 / (32 * π))⁻¹ ∈ algebraicClosure ℚ ℝ := (algebraicClosure ℚ ℝ).inv_mem hsq
  have h3 : ((3 / 32 : ℚ) : ℝ) ∈ algebraicClosure ℚ ℝ := (algebraicClosure ℚ ℝ).algebraMap_mem _
  have h4 := (algebraicClosure ℚ ℝ).mul_mem h3 hinv
  have e : ((3 / 32 : ℚ) : ℝ) * (3 / (32 * π))⁻¹ = π := by push_cast; field_simp
  rw [e] at h4
  exact hπ ((mem_algebraicClosure_iff).mp h4)

/-- kappa = 1/2 is rational, but Z^2 = 8 pi/(3 kappa^2) is then irrational: for any RATIONAL kappa the corresponding Z^2 is irrational (unconditional) -/
theorem kappa_rational_Z_irrational (q : ℚ) (hq : q ≠ 0) : Irrational (8 * π / (3 * (q : ℝ) ^ 2)) := by
  have hq' : (q : ℝ) ≠ 0 := by exact_mod_cast hq
  have h1 : Irrational (8 * π) := by
    have := irrational_pi.ratCast_mul (q := 8) (by norm_num)
    simpa using this
  have h2 := h1.div_ratCast (q := 3 * q ^ 2) (by positivity)
  simpa using h2

/-! links to the lane theorems (c = G = 1) -/

/-- P3: the chain's M1-form is the record's iff `RecordIff.kappa_half_iff_M1` (kappa := a0/sqrt(rho)) -/
theorem link_P3_M1 (S : Setup) :
    RecordIff.M1of 1 S.a0 = (4 / 3) * RecordIff.tLam 1 S.rho ↔ S.kappa = 1 / 2 := by
  have hs := S.sqrt_rho_pos
  have hk : 0 < S.kappa := by unfold Setup.kappa; have := S.a0_pos; positivity
  have h := RecordIff.kappa_half_iff_M1 (κ := S.kappa) (c := 1) (G := 1) (ρ := S.rho) hk one_pos one_pos S.rho_pos
  have ha : RecordIff.a0of S.kappa 1 1 S.rho = S.a0 := by
    unfold RecordIff.a0of Setup.kappa
    have : Real.sqrt (1 * S.rho) = Real.sqrt S.rho := by rw [one_mul]
    rw [this]; field_simp
  rw [ha] at h
  exact h

/-- P7: the chain's offset coefficient satisfies G rho/a0^2 = c/(8 pi), so G rho = 4 a0^2 iff c = 32 pi (P7 `offset_iff`) -/
theorem link_P7_offset (S : Setup) : S.rho = 4 * S.a0 ^ 2 ↔ S.coff = 32 * π := by
  have hp := Real.pi_pos
  have h : 1 * S.rho / S.a0 ^ 2 = S.coff / (8 * π) := by
    unfold Setup.coff; field_simp
  have := OffsetFamily.offset_iff (G := 1) (ρ := S.rho) (a0 := S.a0) (c := S.coff) S.a0_pos.ne' h
  simpa using this

/-- P8: the chain's Omega-form is the lock `OmegaLambda.omega_iff` at c = 1 -/
theorem link_P8_omega (S : Setup) : S.Lam = 32 * π * S.a0 ^ 2 ↔ S.Om = 32 * π * S.a0 ^ 2 / (3 * S.H0 ^ 2) := by
  have h := OmegaLambda.omega_iff (c := 1) (H0 := S.H0) (Ω := S.Om) (a0 := S.a0) (Λ := S.Lam) one_pos S.H0_pos
    (by rw [S.Lam_flat]; ring)
  simpa using h

end PuzzleChain

#print axioms PuzzleChain.iff_premise
#print axioms PuzzleChain.allForms_nodup
#print axioms PuzzleChain.chain_tfae
#print axioms PuzzleChain.forms_equiv
#print axioms PuzzleChain.S_off_not_premise
#print axioms PuzzleChain.all_fail_S_off
#print axioms PuzzleChain.S_on_premise
#print axioms PuzzleChain.all_hold_S_on
#print axioms PuzzleChain.none_is_theorem
#print axioms PuzzleChain.each_satisfiable
#print axioms PuzzleChain.S_off_values
#print axioms PuzzleChain.Z_free
#print axioms PuzzleChain.family_values
#print axioms PuzzleChain.family_targets_iff
#print axioms PuzzleChain.Zkappa_relation
#print axioms PuzzleChain.false_friends
#print axioms PuzzleChain.Z_sq_irrational
#print axioms PuzzleChain.Z_irrational
#print axioms PuzzleChain.aH_irrational
#print axioms PuzzleChain.Z_not_algebraic
#print axioms PuzzleChain.aH_not_algebraic
#print axioms PuzzleChain.kappa_rational_Z_irrational
#print axioms PuzzleChain.link_P3_M1
#print axioms PuzzleChain.link_P7_offset
#print axioms PuzzleChain.link_P8_omega
