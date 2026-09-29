import Mathlib

/-!
# MineM1-B: the tidal-tensor stress of CFG44/CFG50/CFG101 -- exact algebra of its spherical reduction

Source lanes (sympy checks and exact reductions in committed scripts):
  campaign_fresh_gravity/CFG101_tidal_closure_rederivation/cfg101_main.py  lines 62-121 (S1: d_j T_ij = 0, tr T = 2 lap Phi, T_rr = 2 g_N/r, T_perp = 4 pi G rho - g_N/r;
      S3: point mass a_f = 0, a_react = 4 pi G chi P'; P6/N1 line 233-237: chi_c = 3/(8 pi G rho_0) = 3 h^3/(G M) for the exponential sphere)
  campaign_fresh_gravity/CFG101_referee_ceiling.py  lines 1-14 (docstring: "Two exact reductions ... P_rr = a0 g_N/(8 pi G) ... |chi_c a_f|/g_tot = (r/4)|T_rr' + 2(1-beta)T_perp'|/lambda_max";
      lambda_max = G M/(3 h^3) reached as r -> 0; exponential-sphere derivative formulas dTrr, dTp, beta)

CERTIFIED (premises => conclusions; mathematics only):
* B1 `tidal_div_free`, `tidal_trace`: for a fully symmetric third-derivative array D (Clairaut symmetry is a HYPOTHESIS: the lemma is the index algebra,
  not the analysis of a C^3 potential), the divergence of T_ij = delta_ij lap Phi - d_i d_j Phi vanishes and tr T = 2 lap Phi.
* B2 `tidal_radial_conservation`: with g = Phi' (T_rr = 2g/r, T_perp = g' + g/r), T_rr' + 2(T_rr - T_perp)/r = 0 (the radial component of div T = 0);
  `tperp_poisson`: Poisson turns T_perp into 4 pi G rho - g/r.
* B3 `meanDens_bounds`: for ANY non-increasing spherical density rho(s) on [0,inf), rho(r) <= rhobar(r) <= rho(0) (rhobar = 3/r^3 int_0^r s^2 rho ds, proved by integral comparison);
  hence `tidal_lambda_max_le`: both eigenvalues T_rr = (8 pi/3) G rhobar and T_perp = 4 pi G (rho - rhobar/3) are <= the central value (8 pi/3) G rho_0 at every radius, and
  `meanDens_tendsto`, `tperp_tendsto`: they tend to it as r -> 0+ (rho continuous at 0), so lambda_max(T) = (8 pi/3) G rho_0 exactly and the ghost boundary is chi_c = 3/(8 pi G rho_0)
  (`chi_c_exponential`: = 3 h^3/(G M) for rho_0 = M/(8 pi h^3)).  [The lane checks the max numerically for the exponential sphere; the all-monotone-profile statement is a mathematical generalisation.]
* B4 point mass: `pointmass_trace_deriv` (T_rr + 2 T_perp = 0 outside, so an isotropic stress exerts no force on the fluid: a_f = 0) and `pointmass_react`
  (a_react = 8 pi G d/dr[chi P/2] = -chi G a0 M/r^3 for P = a0 M/(8 pi r^2)).
* B5 exponential sphere: M(x) = 1 - e^{-x}(1 + x + x^2/2) has M' = x^2 e^{-x}/2 (`Mexp_deriv`); `exp_Trr_deriv`, `exp_Tperp_deriv` give the exact T_rr', T_perp' used by the referee script;
  `exp_beta`: -(3/2) rho_b/rhobar_b = -x^3 e^{-x}/(4M);  `af_over_gtot`: the target's Jeans stress gives a_f/g_tot = (r/4)(T_rr' + 2(1-beta)T_perp'), rho_c and g_tot drop out.

NOT certified: the action and reciprocity theorem (a_react from the multiplier equation), the 3-D Noether/virtual-work numerics, the ghost-free ceiling value (0.50077 g_tot at 0.852 h, a numerical
maximum of an explicit function of x), the flip radius 1.7795 h, the mass-size relation h(M_b), and the FRW inertia numbers.  Nothing here says the tidal closure works: it is a scoped no-go in CFG50/101.
kappa = 1/2 is FITTED; nothing here says the theory is closed.
-/

open MeasureTheory Set Filter Topology Real

namespace MineM1

/-- B1. Cartesian algebra: with `D i j k` the third partials of the potential (fully symmetric by Clairaut, a HYPOTHESIS here),
    the tidal tensor T_ij = delta_ij lap Phi - d_i d_j Phi has d_k T_ij = delta_ij sum_l D l l k - D i j k, and its divergence vanishes. -/
theorem tidal_div_free (D : Fin 3 → Fin 3 → Fin 3 → ℝ)
    (hs1 : ∀ i j k, D i j k = D j i k) (hs2 : ∀ i j k, D i j k = D i k j) (i : Fin 3) :
    ∑ j : Fin 3, ((if i = j then ∑ l : Fin 3, D l l j else 0) - D i j j) = 0 := by
  rw [Finset.sum_sub_distrib]
  have h1 : ∑ j : Fin 3, (if i = j then ∑ l : Fin 3, D l l j else 0) = ∑ l : Fin 3, D l l i := by
    simp [Finset.sum_ite_eq]
  rw [h1]
  have h2 : ∀ l : Fin 3, D l l i = D i l l := fun l => by rw [hs2 l l i, hs1 l i l]
  simp only [h2]
  ring

/-- trace: tr T = 3 lap Phi - lap Phi = 2 lap Phi (= 8 pi G rho by Poisson) -/
theorem tidal_trace (Lap : ℝ) (H : Fin 3 → Fin 3 → ℝ) (hL : Lap = ∑ i : Fin 3, H i i) :
    ∑ i : Fin 3, ((if i = i then Lap else 0) - H i i) = 3 * Lap := by
  simp [Finset.sum_sub_distrib, ← hL]
  ring

/-- B2. spherical radial conservation: with g = Phi' (so T_rr = 2g/r, T_perp = g' + g/r), T_rr' + 2 (T_rr - T_perp)/r = 0 -/
theorem tidal_radial_conservation {g g' : ℝ → ℝ} {r : ℝ} (hr : 0 < r) (hg : HasDerivAt g (g' r) r) :
    HasDerivAt (fun x => 2 * g x / x) (2 * g' r / r - 2 * g r / r ^ 2) r ∧
    (2 * g' r / r - 2 * g r / r ^ 2) + 2 * ((2 * g r / r) - (g' r + g r / r)) / r = 0 := by
  constructor
  · have h := (hg.const_mul 2).div (hasDerivAt_id r) hr.ne'
    refine h.congr_deriv ?_
    simp; field_simp
  · field_simp; ring

/-- Poisson: g' + 2g/r = 4 pi G rho turns T_perp into 4 pi G rho - g/r -/
theorem tperp_poisson {g g' rho G r : ℝ} (hP : g' + 2 * g / r = 4 * Real.pi * G * rho) :
    g' + g / r = 4 * Real.pi * G * rho - g / r := by
  have : 2 * g / r = g / r + g / r := by ring
  linarith

/-- mean density inside radius r, 3/r^3 int_0^r s^2 rho(s) ds (= 3 M(<r)/(4 pi r^3)) -/
noncomputable def meanDens (ρ : ℝ → ℝ) (r : ℝ) : ℝ := 3 / r ^ 3 * ∫ s in (0:ℝ)..r, s ^ 2 * ρ s

theorem meanDens_bounds {ρ : ℝ → ℝ} (hanti : AntitoneOn ρ (Ici 0)) {r : ℝ} (hr : 0 < r) :
    ρ r ≤ meanDens ρ r ∧ meanDens ρ r ≤ ρ 0 := by
  have hint : IntervalIntegrable (fun s => ρ s * s ^ 2) volume 0 r := by
    apply IntervalIntegrable.mul_continuousOn
    · exact AntitoneOn.intervalIntegrable (hanti.mono (by
        intro x hx; rw [uIcc_of_le hr.le] at hx; exact hx.1))
    · exact (continuous_pow 2).continuousOn
  have hint' : IntervalIntegrable (fun s => s ^ 2 * ρ s) volume 0 r := by
    simpa [mul_comm] using hint
  have hr3 : 0 < r ^ 3 := by positivity
  have hcs : ∫ s in (0:ℝ)..r, s ^ 2 = r ^ 3 / 3 := by
    simp [integral_pow]; norm_num
  unfold meanDens
  constructor
  · have h1 : ∫ s in (0:ℝ)..r, s ^ 2 * ρ r ≤ ∫ s in (0:ℝ)..r, s ^ 2 * ρ s := by
      apply intervalIntegral.integral_mono_on hr.le
      · exact (continuous_pow 2).intervalIntegrable _ _ |>.mul_const _
      · exact hint'
      · intro s hs
        exact mul_le_mul_of_nonneg_left (hanti (show (0:ℝ) ≤ s from hs.1) (show (0:ℝ) ≤ r from hr.le) hs.2)
          (sq_nonneg s)
    rw [intervalIntegral.integral_mul_const, hcs] at h1
    have : ρ r = 3 / r ^ 3 * (r ^ 3 / 3 * ρ r) := by field_simp
    calc ρ r = 3 / r ^ 3 * (r ^ 3 / 3 * ρ r) := this
      _ ≤ _ := mul_le_mul_of_nonneg_left h1 (by positivity)
  · have h1 : ∫ s in (0:ℝ)..r, s ^ 2 * ρ s ≤ ∫ s in (0:ℝ)..r, s ^ 2 * ρ 0 := by
      apply intervalIntegral.integral_mono_on hr.le
      · exact hint'
      · exact (continuous_pow 2).intervalIntegrable _ _ |>.mul_const _
      · intro s hs
        exact mul_le_mul_of_nonneg_left (hanti (show (0:ℝ) ≤ 0 from le_refl _) (show (0:ℝ) ≤ s from hs.1) hs.1)
          (sq_nonneg s)
    rw [intervalIntegral.integral_mul_const, hcs] at h1
    calc 3 / r ^ 3 * ∫ s in (0:ℝ)..r, s ^ 2 * ρ s ≤ 3 / r ^ 3 * (r ^ 3 / 3 * ρ 0) :=
          mul_le_mul_of_nonneg_left h1 (by positivity)
      _ = ρ 0 := by field_simp

/-- eigenvalues of the tidal tensor of a spherical baryon distribution: T_rr = (8 pi/3) G rhobar, T_perp = 4 pi G (rho - rhobar/3);
    both are bounded by the central value (8 pi/3) G rho_0 when rho <= rhobar <= rho_0. -/
theorem tidal_eigs_le {G ρ0 ρ mb : ℝ} (hG : 0 < G) (h1 : ρ ≤ mb) (h2 : mb ≤ ρ0) :
    (8 * Real.pi / 3) * G * mb ≤ (8 * Real.pi / 3) * G * ρ0 ∧
    4 * Real.pi * G * (ρ - mb / 3) ≤ (8 * Real.pi / 3) * G * ρ0 := by
  have hp := Real.pi_pos
  have hpG : 0 < Real.pi * G := mul_pos hp hG
  constructor
  · nlinarith
  · nlinarith

/-- for ANY non-increasing spherical density both eigenvalues lie below the central value at every radius -/
theorem tidal_lambda_max_le {G : ℝ} (hG : 0 < G) {ρ : ℝ → ℝ} (hanti : AntitoneOn ρ (Ici 0)) {r : ℝ} (hr : 0 < r) :
    (8 * Real.pi / 3) * G * meanDens ρ r ≤ (8 * Real.pi / 3) * G * ρ 0 ∧
    4 * Real.pi * G * (ρ r - meanDens ρ r / 3) ≤ (8 * Real.pi / 3) * G * ρ 0 :=
  tidal_eigs_le hG (meanDens_bounds hanti hr).1 (meanDens_bounds hanti hr).2

/-- and the central value is the supremum: meanDens -> rho(0) as r -> 0+ (rho continuous at 0), so both eigenvalues tend to (8 pi/3) G rho_0 -/
theorem meanDens_tendsto {ρ : ℝ → ℝ} (hanti : AntitoneOn ρ (Ici 0)) (hc : ContinuousWithinAt ρ (Ici 0) 0) :
    Tendsto (meanDens ρ) (𝓝[>] 0) (𝓝 (ρ 0)) := by
  have hlow : Tendsto ρ (𝓝[>] 0) (𝓝 (ρ 0)) := hc.tendsto.mono_left (nhdsWithin_mono _ Ioi_subset_Ici_self)
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le' hlow tendsto_const_nhds ?_ ?_
  · filter_upwards [self_mem_nhdsWithin] with r hr using (meanDens_bounds hanti hr).1
  · filter_upwards [self_mem_nhdsWithin] with r hr using (meanDens_bounds hanti hr).2

theorem tperp_tendsto {G : ℝ} {ρ : ℝ → ℝ} (hanti : AntitoneOn ρ (Ici 0)) (hc : ContinuousWithinAt ρ (Ici 0) 0) :
    Tendsto (fun r => 4 * Real.pi * G * (ρ r - meanDens ρ r / 3)) (𝓝[>] 0) (𝓝 ((8 * Real.pi / 3) * G * ρ 0)) := by
  have hlow : Tendsto ρ (𝓝[>] 0) (𝓝 (ρ 0)) := hc.tendsto.mono_left (nhdsWithin_mono _ Ioi_subset_Ici_self)
  have := (hlow.sub ((meanDens_tendsto hanti hc).div_const 3)).const_mul (4 * Real.pi * G)
  convert this using 2
  ring

/-- ghost boundary chi_c = 1/lambda_max = 3/(8 pi G rho_0); for the exponential sphere rho_0 = M/(8 pi h^3) this is 3 h^3/(G M) -/
theorem chi_c_exponential {G M h : ℝ} (hG : 0 < G) (hM : 0 < M) (hh : 0 < h) :
    1 / ((8 * Real.pi / 3) * G * (M / (8 * Real.pi * h ^ 3))) = 3 * h ^ 3 / (G * M) := by
  have hp := Real.pi_pos
  field_simp

/-- point mass outside the baryons: T_rr = 2GM/r^3, T_perp = -GM/r^3 ; T_rr' + 2 T_perp' = 0 (tr T = 0), so an isotropic stress exerts no force -/
theorem pointmass_trace_deriv {GM r : ℝ} :
    HasDerivAt (fun x => 2 * GM / x ^ 3 + 2 * (-GM / x ^ 3)) 0 r := by
  have : (fun x : ℝ => 2 * GM / x ^ 3 + 2 * (-GM / x ^ 3)) = fun _ => 0 := by
    funext x; ring
  rw [this]; exact hasDerivAt_const r 0

/-- the reaction of an isotropic stress P on the baryons: a_react = 8 pi G F' with F = chi P/2, for P = a0 M/(8 pi r^2) equals -chi G a0 M / r^3 -/
theorem pointmass_react {G a0 M χ r : ℝ} (hr : 0 < r) :
    HasDerivAt (fun x => 8 * Real.pi * G * (χ * (a0 * M / (8 * Real.pi * x ^ 2)) / 2))
      (-(χ * G * a0 * M / r ^ 3)) r := by
  have hp := Real.pi_pos
  have h1 : HasDerivAt (fun x : ℝ => x ^ 2) (2 * r) r := by simpa using hasDerivAt_pow 2 r
  have h2 := (hasDerivAt_const r (a0 * M)).div (h1.const_mul (8 * Real.pi)) (by positivity)
  have h3 := ((h2.const_mul χ).div_const 2).const_mul (8 * Real.pi * G)
  refine h3.congr_deriv ?_
  field_simp
  ring

/-- the exponential sphere: M(x) = 1 - e^{-x}(1 + x + x^2/2) is the enclosed mass (units G = M_b = h = 1) and M' = x^2 e^{-x}/2 -/
noncomputable def Mexp (x : ℝ) : ℝ := 1 - Real.exp (-x) * (1 + x + x ^ 2 / 2)

theorem Mexp_deriv (x : ℝ) : HasDerivAt Mexp (x ^ 2 * Real.exp (-x) / 2) x := by
  have h1 : HasDerivAt (fun x : ℝ => Real.exp (-x)) (-Real.exp (-x)) x := by
    simpa using (hasDerivAt_neg x).exp
  have h2 : HasDerivAt (fun x : ℝ => 1 + x + x ^ 2 / 2) (1 + x) x := by
    have := ((hasDerivAt_id x).const_add 1).add ((hasDerivAt_pow 2 x).div_const 2)
    refine this.congr_deriv ?_
    simp
  have := (h1.mul h2).const_sub 1
  refine this.congr_deriv ?_
  ring

/-- T_rr = 2 M/x^3 and T_perp = e^{-x}/2 - M/x^3 (4 pi G rho_b = e^{-x}/2); derivatives used by CFG101/CFG50 -/
theorem exp_Trr_deriv {x : ℝ} (hx : 0 < x) :
    HasDerivAt (fun y => 2 * Mexp y / y ^ 3) (Real.exp (-x) / x - 6 * Mexp x / x ^ 4) x := by
  have h1 : HasDerivAt (fun y : ℝ => y ^ 3) (3 * x ^ 2) x := by simpa using hasDerivAt_pow 3 x
  have h := ((Mexp_deriv x).const_mul 2).div h1 (by positivity)
  refine h.congr_deriv ?_
  field_simp
  ring

theorem exp_Tperp_deriv {x : ℝ} (hx : 0 < x) :
    HasDerivAt (fun y => Real.exp (-y) / 2 - Mexp y / y ^ 3)
      (-Real.exp (-x) / 2 - Real.exp (-x) / (2 * x) + 3 * Mexp x / x ^ 4) x := by
  have h1 : HasDerivAt (fun y : ℝ => y ^ 3) (3 * x ^ 2) x := by simpa using hasDerivAt_pow 3 x
  have he : HasDerivAt (fun x : ℝ => Real.exp (-x)) (-Real.exp (-x)) x := by
    simpa using (hasDerivAt_neg x).exp
  have h := (he.div_const 2).sub ((Mexp_deriv x).div h1 (by positivity))
  refine h.congr_deriv ?_
  field_simp
  ring

/-- anisotropy of the target: beta = -(3/2) rho_b/rhobar_b = -x^3 e^{-x}/(4 M) with rho_b = e^{-x}/(8 pi), rhobar_b = 3 M/(4 pi x^3) -/
theorem exp_beta {x M : ℝ} (hx : 0 < x) (hM : 0 < M) :
    -(3 / 2) * (Real.exp (-x) / (8 * Real.pi)) / (3 * M / (4 * Real.pi * x ^ 3)) = -(x ^ 3 * Real.exp (-x)) / (4 * M) := by
  have hp := Real.pi_pos
  field_simp
  ring

/-- the exact reduction: with the target's Jeans stress P_rr = rho_c r g/2, P_perp = (1 - beta) P_rr and a_f = (1/2 rho_c)(T_rr' P_rr + 2 T_perp' P_perp),
    a_f/g_tot = (r/4)(T_rr' + 2 (1 - beta) T_perp'): rho_c and g_tot drop out, so with chi_c = 1/lambda_max the ceiling depends on x = r/h alone -/
theorem af_over_gtot {ρc g r β Trr' Tp' : ℝ} (hρ : ρc ≠ 0) (hg : g ≠ 0) :
    (1 / (2 * ρc)) * (Trr' * (ρc * (r * g / 2)) + 2 * Tp' * ((1 - β) * (ρc * (r * g / 2)))) / g
      = r / 4 * (Trr' + 2 * (1 - β) * Tp') := by
  field_simp
  ring


end MineM1

open MineM1 in
#print axioms tidal_div_free
open MineM1 in
#print axioms tidal_radial_conservation
open MineM1 in
#print axioms meanDens_bounds
open MineM1 in
#print axioms tidal_lambda_max_le
open MineM1 in
#print axioms tperp_tendsto
open MineM1 in
#print axioms chi_c_exponential
open MineM1 in
#print axioms pointmass_react
open MineM1 in
#print axioms Mexp_deriv
open MineM1 in
#print axioms exp_Tperp_deriv
open MineM1 in
#print axioms exp_beta
open MineM1 in
#print axioms af_over_gtot
