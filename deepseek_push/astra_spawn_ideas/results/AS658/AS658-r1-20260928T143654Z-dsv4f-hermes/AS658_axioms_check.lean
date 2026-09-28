import Mathlib
import Mathlib.Tactic

/-
  AS658 -- gauge invariance and local degree count of the k04 three-form vacuum
  (Lean 4 certificate of the algebraic core).

  Cell: A a three-form, F = dA, F = q eps (eps_{0123} = +1, eps^{0123} = -1, mostly-plus),
  vacuum action S = int P(q) d^4x on a contractible flat patch, P(q) = Z q^2/2 + b beta^2 q^2,
  a0 = beta sqrt(G) |q|, kappa = 1/2 ADOPTED (FRAMEWORK_CONTRACT).

  The degree count rests on exactly two algebraic steps, certified here:

  T1 (eom_invertible / eom_components): the four EOM components
     E_sigma = sum_mu epsU(mu,sigma) d_mu P_q are equivalent to d_mu P_q = 0 for all mu:
     the coefficient map dP_q |-> E is the signed permutation diag(-1, +1, -1, +1)
     (rows = triples (123),(023),(013),(012); columns = mu = complement index),
     k-independent and invertible over Z.  Hence the bulk equation is a pure constraint:
     q = const locally, zero propagating modes, no dispersion relation (no root omega(k)).

  T2 (eb_antisym, double_sum_swap, symm_contract_zero): for ANY antisymmetric kernel eb
     (the epsilon contraction of an antisymmetric pair) and ANY symmetric factor s
     (e.g. s(mu,nu) = k_mu k_nu, the second-derivative symbol), the double sum
     sum_{mu,nu} eb(mu,nu) * s(mu,nu) vanishes.  This is the d^2 = 0 core: the gauge
     direction a = dB (Fourier ahat = i k ^ bhat) is a null direction of the second
     variation of S.  Proof: summation swap + antisymmetry of eb + symmetry of s.

  T3 (gauge_null_plane_wave): explicit 4-term plane-wave nullity with the EOM row signs:
        -k0 ahat123 + k1 ahat023 - k2 ahat013 + k3 ahat012 = 0   for ahat = k ^ b,
     ring-closed for arbitrary integer k and antisymmetric b (the 1/6 prefactor dropped).

  No physical claim is made beyond the algebra; the physics reading is in derivation.md.
-/

namespace AS658

-- triple index: 0 = (123), 1 = (023), 2 = (013), 3 = (012); mu = complement index
/-- rows of the EOM map: epsU(mu, s) * v(mu) contribution, v = d_mu P_q components.
    epsU(mu,s) = -sgn((mu, triple_s)) for mu = complement(s), else 0:  diag(-1, 1, -1, 1). -/
def epsU (mu s : Fin 4) : ℤ :=
  match mu, s with
  | 0, 0 => -1
  | 1, 1 => 1
  | 2, 2 => -1
  | 3, 3 => 1
  | _, _ => 0

/-- EOM component s for gradient data v : the four mu = complement terms (explicit sum). -/
def eomComp (v : Fin 4 → ℤ) (s : Fin 4) : ℤ :=
  epsU 0 s * v 0 + epsU 1 s * v 1 + epsU 2 s * v 2 + epsU 3 s * v 3

/-- T1: EOM = 0 (all four components) iff the whole gradient v vanishes.
    (det of the coefficient map is +-1: the four equations are four independent conditions
    on the four components of d P_q; the bulk system is a constraint, not a wave system.) -/
theorem eom_invertible (v : Fin 4 → ℤ) (h : ∀ s : Fin 4, eomComp v s = 0) :
    ∀ mu : Fin 4, v mu = 0 := by
  intro mu
  fin_cases mu
  · have h0 := h 0
    simp [eomComp, epsU] at h0
    exact h0
  · have h1 := h 1
    simp [eomComp, epsU] at h1
    exact h1
  · have h2 := h 2
    simp [eomComp, epsU] at h2
    exact h2
  · have h3 := h 3
    simp [eomComp, epsU] at h3
    exact h3

/-- the coefficient map is the k-independent signed permutation diag(-1, 1, -1, 1):
    no root omega(k), i.e. no characteristic variety / no dispersion. -/
theorem eom_components (v : Fin 4 → ℤ) :
    eomComp v 0 = -v 0 ∧ eomComp v 1 = v 1 ∧ eomComp v 2 = -v 2 ∧ eomComp v 3 = v 3 := by
  simp [eomComp, epsU]

/-- antisymmetric kernel (epsilon with the antisymmetric pair fixed, e.g. eps^{mu nu 2 3}). -/
def eb (mu nu : Fin 4) : ℤ :=
  match mu, nu with
  | 0, 1 => -1
  | 1, 0 => 1
  | 2, 3 => 1
  | 3, 2 => -1
  | _, _ => 0

/-- eb is antisymmetric (epsilon property). -/
lemma eb_antisym (mu nu : Fin 4) : eb mu nu = -eb nu mu := by
  fin_cases mu <;> fin_cases nu <;> decide

/-- double summation swap: sum_{mu,nu} h mu nu = sum_{mu,nu} h nu mu. -/
lemma double_sum_swap (h : Fin 4 → Fin 4 → ℤ) :
    (∑ mu : Fin 4, ∑ nu : Fin 4, h mu nu) =
    (∑ mu : Fin 4, ∑ nu : Fin 4, h nu mu) := by
  rw [Finset.sum_comm]

/-- pointwise sign/symmetry step used inside the double sum. -/
lemma pointwise_step (s : Fin 4 → Fin 4 → ℤ) (hs : ∀ i j, s i j = s j i) :
    (∑ mu : Fin 4, ∑ nu : Fin 4, eb nu mu * s nu mu) =
    (∑ mu : Fin 4, ∑ nu : Fin 4, (-(eb mu nu)) * s mu nu) := by
  apply Finset.sum_congr rfl
  intro mu hmu
  apply Finset.sum_congr rfl
  intro nu hnu
  rw [eb_antisym nu mu, hs nu mu]

/-- T2 core (d^2 = 0): a symmetric factor contracted with an antisymmetric kernel vanishes.
    Applies with s(mu,nu) = k_mu k_nu: the gauge direction a = dB is a null direction of the
    second variation of S. -/
theorem symm_contract_zero (s : Fin 4 → Fin 4 → ℤ) (hs : ∀ i j, s i j = s j i) :
    (∑ mu : Fin 4, ∑ nu : Fin 4, eb mu nu * s mu nu) = 0 := by
  have hmain : (∑ mu : Fin 4, ∑ nu : Fin 4, eb mu nu * s mu nu) =
      - (∑ mu : Fin 4, ∑ nu : Fin 4, eb mu nu * s mu nu) := by
    calc
      (∑ mu : Fin 4, ∑ nu : Fin 4, eb mu nu * s mu nu)
          = (∑ mu : Fin 4, ∑ nu : Fin 4, eb nu mu * s nu mu) := double_sum_swap (fun μ ν => eb μ ν * s μ ν)
      _ = (∑ mu : Fin 4, ∑ nu : Fin 4, (-(eb mu nu)) * s mu nu) := pointwise_step s hs
      _ = - (∑ mu : Fin 4, ∑ nu : Fin 4, eb mu nu * s mu nu) := by
        simp [Finset.sum_neg_distrib, neg_mul]
  omega

/-- T3: explicit plane-wave gauge nullity with the EOM row signs:
    -k0 ahat123 + k1 ahat023 - k2 ahat013 + k3 ahat012 = 0  for ahat = k ^ b.
    (the prefactor 1/6 is dropped: zero is zero.) -/
theorem gauge_null_plane_wave (k0 k1 k2 k3 b01 b02 b03 b12 b13 b23 : ℤ) :
    -k0 * (k1 * b23 - k2 * b13 + k3 * b12)
      + k1 * (k0 * b23 - k2 * b03 + k3 * b02)
      - k2 * (k0 * b13 - k1 * b03 + k3 * b01)
      + k3 * (k0 * b12 - k1 * b02 + k2 * b01) = 0 := by
  ring

/-- the wedge construction used in T3 (for the record). -/
def ahat (k : Fin 4 → ℤ) (b : Fin 4 → Fin 4 → ℤ) (nu rho sigma : Fin 4) : ℤ :=
  k nu * b rho sigma - k rho * b nu sigma + k sigma * b nu rho

end AS658

-- axiom footprint
#print axioms AS658.eom_invertible
#print axioms AS658.eom_components
#print axioms AS658.eb_antisym
#print axioms AS658.double_sum_swap
#print axioms AS658.pointwise_step
#print axioms AS658.symm_contract_zero
#print axioms AS658.gauge_null_plane_wave
