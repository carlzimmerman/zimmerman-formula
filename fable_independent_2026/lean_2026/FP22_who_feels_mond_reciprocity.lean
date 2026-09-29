import Mathlib

/-!
# M6-D -- FP22 checks A1, A2, A4: the static perfect square, and "who feels the MOND scalar" = "who sources it"

Source: `real_research/derivation_chain_2026/FP22_who_feels_mond.py`, part A (sympy):
  A1 (lines 424-433): the static reduction -2 a^2 + alpha_c a^2 + (2-alpha_c)(2a - D chi) D chi is the perfect square
      -(2-alpha_c)|a - D chi|^2, and a - D chi = D ln(N e^-chi) (Einstein-frame lapse N~ = N e^-chi);
  A2 (lines 435-470): two species with matter couplings -rho_b Phi - rho_d (Phi - beta phi): the scalar's source is
      rho_b + (1 - beta) rho_d and the dark component feels Phi_N + (1 - beta) phi: feel weights = source weights;
  A4 (lines 496-517): with phi's inertia the linear equation is  lambda chi_tt = -4 pi G (rho_b + (1-beta) rho_d),
      and the non-relativistic lapse of g~ is (1 + Phi) e^-chi -> 1 + Phi - chi at first order.
The script does these with sympy `euler_equations`; the lane's own text says "reciprocity: nothing can feel phi without
sourcing it".  Corpus check (2026-09-29): `git grep -n -i -e "Einstein-frame" -e "reciprocity" -e "perfect square"
-- '*.lean'` shows reciprocity only in the CFG44 B4/Exchange islands (a different construction: the phantom kernel /
tidal stress) and I22's unrelated Dobrushin perfect square.  The FP22 statements are not in the corpus.  New.

Setting: pointwise, in one space dimension, quantities are the real VALUES at a point x of the field derivatives.  The
static Lagrangian (per FP22's `static_L`) is
    L = [-(2 - a_c)(Phi' - phi')^2 - 2 a^2 J(phi'^2/a^2)]/(16 pi G) - sum_s rho_s (Phi - b_s phi),
so dL/dPhi = -sum rho_s, dL/dphi = sum b_s rho_s, and the momenta are
    p_Phi = -(2 - a_c)(Phi' - phi')/(8 pi G),   p_phi = [2(2 - a_c)(Phi' - phi') - 4 J'(..) phi']/(16 pi G).
The Euler-Lagrange equations d/dx p = dL/d(field) are taken as HYPOTHESES in expanded form (s := (Phi'-phi')',
Jd := d/dx(J' phi')), exactly the equations sympy prints.
CERTIFIED:
  * `perfect_square`   : -2 a^2 + a_c a^2 + (2-a_c)(2a - c) c = -(2-a_c)(a - c)^2  (ring identity);
  * `einstein_lapse`   : for N > 0, log(N e^-chi) = log N - chi, hence D ln(N e^-chi) = D ln N - D chi (HasDerivAt form);
  * `lapse_equation`   : from the Phi-equation, (2-a_c) s = 8 pi G sum rho_s   (so (Phi-phi)'' = 4 pi G_N sum rho_s,
                         G_N = G/(1 - a_c/2));
  * `scalar_source`    : from both equations, Jd = 4 pi G sum_s (1 - b_s) rho_s  (the scalar's source has weight
                         1 - b_s per species: beta = 0 -> all matter, beta = 1 -> the species is decoupled);
  * `felt_potential`   : the potential felt by species s, Phi - b_s phi, equals Phi_N + (1 - b_s) phi with Phi_N := Phi - phi;
  * `reciprocity`      : (felt weight of s) = (source weight of s) = 1 - b_s, identically -- a species that feels phi at
                         all sources it at exactly the same weight;
  * `dynamic_scalar`   : with the kinetic term 2 lambda chi_t^2/(16 pi G) added, the chi-equation reads
                         lambda chi_tt = -4 pi G sum_s (1 - b_s) rho_s;
  * `NR_lapse`         : d/d eps [(1 + eps Phi) exp(-eps chi)] at eps = 0 is Phi - chi.
NOT CERTIFIED: the Lagrangian itself (FP7's root), the identification of FK1 with beta = 0 (`S_Psi[g]`) or beta = 1
(the Einstein-frame metric), the L353 pair (A3, needs decay conditions), the cost A5 (WEP violation), any
sigma_8 / forest / KiDS number.  These are the lane's readings; here the mathematics of the stated static Lagrangian
only.  No empirical premise; kappa = 1/2 is unrelated.
-/

noncomputable section
namespace M6D

open Real

theorem perfect_square (ac a c : ℝ) :
    -2 * a ^ 2 + ac * a ^ 2 + (2 - ac) * (2 * a - c) * c = -(2 - ac) * (a - c) ^ 2 := by ring

theorem einstein_lapse (N chi : ℝ) (hN : 0 < N) :
    Real.log (N * Real.exp (-chi)) = Real.log N - chi := by
  rw [Real.log_mul hN.ne' (Real.exp_pos _).ne', Real.log_exp]
  ring

theorem einstein_lapse_deriv (N chi : ℝ → ℝ) {x : ℝ} {N' chi' : ℝ} (hN : 0 < N x)
    (hNd : HasDerivAt N N' x) (hcd : HasDerivAt chi chi' x) :
    HasDerivAt (fun y => Real.log (N y * Real.exp (-chi y))) (N' / N x - chi') x := by
  have h1 : HasDerivAt (fun y => Real.log (N y)) (N' / N x) x := hNd.log hN.ne'
  have h2 := h1.sub hcd
  refine h2.congr_of_eventuallyEq ?_
  have hcont : ContinuousAt N x := hNd.continuousAt
  have hev : ∀ᶠ y in nhds x, 0 < N y := hcont.eventually (lt_mem_nhds hN)
  filter_upwards [hev] with y hy
  exact einstein_lapse (N y) (chi y) hy

section species

variable {ι : Type*} (S : Finset ι) (rho b : ι → ℝ)

theorem lapse_equation (ac G s : ℝ) (hG : 0 < G)
    (hPhi : -(∑ i ∈ S, rho i) - (-(2 - ac) * s / (8 * π * G)) = 0) :
    (2 - ac) * s = 8 * π * G * ∑ i ∈ S, rho i := by
  have hp : 0 < 8 * π * G := by positivity
  field_simp at hPhi
  nlinarith [hPhi]

theorem scalar_source (ac G s Jd : ℝ) (hG : 0 < G)
    (hPhi : -(∑ i ∈ S, rho i) - (-(2 - ac) * s / (8 * π * G)) = 0)
    (hphi : (∑ i ∈ S, b i * rho i) - (2 * (2 - ac) * s - 4 * Jd) / (16 * π * G) = 0) :
    Jd = 4 * π * G * ∑ i ∈ S, (1 - b i) * rho i := by
  have hp : 0 < 16 * π * G := by positivity
  have h1 := lapse_equation S rho ac G s hG hPhi
  have hsum : ∑ i ∈ S, (1 - b i) * rho i = (∑ i ∈ S, rho i) - ∑ i ∈ S, b i * rho i := by
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [hsum]
  field_simp at hphi
  nlinarith [hphi, h1]

/-- the felt potential of species i: Phi - b_i phi = Phi_N + (1 - b_i) phi, Phi_N := Phi - phi -/
theorem felt_potential (Phi phi bi : ℝ) : Phi - bi * phi = (Phi - phi) + (1 - bi) * phi := by ring

/-- reciprocity: the coefficient of phi in the potential felt by species i is 1 - b_i, and 1 - b_i is also the weight with
which rho_i enters the scalar's source -/
theorem reciprocity (ac G s Jd : ℝ) (hG : 0 < G)
    (hPhi : -(∑ i ∈ S, rho i) - (-(2 - ac) * s / (8 * π * G)) = 0)
    (hphi : (∑ i ∈ S, b i * rho i) - (2 * (2 - ac) * s - 4 * Jd) / (16 * π * G) = 0) (Phi phi : ℝ) :
    Jd = 4 * π * G * ∑ i ∈ S, (1 - b i) * rho i ∧
    ∀ i, Phi - b i * phi = (Phi - phi) + (1 - b i) * phi := by
  exact ⟨scalar_source S rho b ac G s Jd hG hPhi hphi, fun i => felt_potential Phi phi (b i)⟩

/-- with phi's inertia: lambda chi_tt = -4 pi G sum (1 - b_i) rho_i -/
theorem dynamic_scalar (ac G s lam chitt : ℝ) (hG : 0 < G)
    (hPhi : -(∑ i ∈ S, rho i) - (-(2 - ac) * s / (8 * π * G)) = 0)
    (hchi : (∑ i ∈ S, b i * rho i) - (2 * (2 - ac) * s / (16 * π * G)) - (4 * lam * chitt / (16 * π * G)) = 0) :
    lam * chitt = -(4 * π * G) * ∑ i ∈ S, (1 - b i) * rho i := by
  have hp : 0 < 16 * π * G := by positivity
  have h1 := lapse_equation S rho ac G s hG hPhi
  have hsum : ∑ i ∈ S, (1 - b i) * rho i = (∑ i ∈ S, rho i) - ∑ i ∈ S, b i * rho i := by
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [hsum]
  field_simp at hchi
  nlinarith [hchi, h1]

end species

theorem NR_lapse (Phi chi : ℝ) :
    HasDerivAt (fun eps : ℝ => (1 + eps * Phi) * Real.exp (-(eps * chi))) (Phi - chi) 0 := by
  have h1 : HasDerivAt (fun eps : ℝ => 1 + eps * Phi) Phi 0 := by
    simpa using ((hasDerivAt_id (0:ℝ)).mul_const Phi).const_add 1
  have h2 : HasDerivAt (fun eps : ℝ => Real.exp (-(eps * chi))) (-chi) 0 := by
    have h3 : HasDerivAt (fun eps : ℝ => -(eps * chi)) (-chi) 0 := by
      have := ((hasDerivAt_id (0:ℝ)).mul_const chi).fun_neg
      simpa using this
    simpa using h3.exp
  have h4 := h1.mul h2
  refine h4.congr_deriv ?_
  simp
  ring

end M6D

end

#print axioms M6D.perfect_square
#print axioms M6D.einstein_lapse_deriv
#print axioms M6D.lapse_equation
#print axioms M6D.scalar_source
#print axioms M6D.reciprocity
#print axioms M6D.dynamic_scalar
#print axioms M6D.NR_lapse
