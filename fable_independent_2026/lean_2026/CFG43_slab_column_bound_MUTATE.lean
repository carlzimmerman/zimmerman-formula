import Mathlib

/-!
# MineM1-F: the slab first integral and the column bound Sigma <= a0/(2 pi G) of a hard stress cap (CFG43 A3, re-derived in CFG103 A3)

Source lanes: campaign_fresh_gravity/CFG43_fluid_tie/A3_cap_entry_form_and_obstruction.py (ledger row 5: "column bound Sigma <= a0/2piG (106.9 / 129.2 Msun/pc^2)")
  and campaign_fresh_gravity/CFG103_fluid_tie_rederivation/cfg103_A3.py lines 63-65 (sympy "a9 slab: d/dz [P + g^2/(8 pi G)] = 0 (hydrostatic + Poisson)" and
  "a10 slab column bound Sigma <= a0/(2 pi G)   [P0 = pi G Sigma^2/2 <= Pcap]").

CERTIFIED (premises => conclusions; pure calculus/algebra):
* `slab_first_integral`: if P' = -rho g and g' = 4 pi G rho for all z then P + g^2/(8 pi G) is constant.
* `slab_column_bound`: if additionally g(0) = 0 (midplane), P -> 0 and g -> g_inf far away, P(0) <= P_cap and a0^2 = 8 pi G P_cap (the cap's acceleration), then
  P(0) = g_inf^2/(8 pi G) (= pi G Sigma^2/2 when g_inf = 2 pi G Sigma), |g_inf| <= a0, and Sigma <= a0/(2 pi G).
* `cap_pressure_lt` and `slab_column_bound_strict`: the saturating arctan cap has P < P_cap strictly (P = P_cap x^2/(1+x^2)), so the bound is strict: Sigma < a0/(2 pi G).

NOT certified: that a real disk is a slab, or that the pressure obeys the cap (the entry FORM of the cap is the lane's POSTULATE, ledger row 4), the numerical values 106.9 and 129.2 Msun/pc^2
(they need the empirical a0 footings), and any statement about observed surface densities.  a0(z) flat is conditional on constant rho_Lambda (ChainCert.Chain).
kappa = 1/2 is FITTED; nothing here says the theory is closed.
-/

open Filter Topology Real

namespace MineM1

/-- slab first integral: hydrostatic P' = -rho g and Poisson g' = 4 pi G rho give d/dz [P + g^2/(8 pi G)] = 0 -/
theorem slab_first_integral {G : ℝ} (hG : 0 < G) {P g ρ : ℝ → ℝ}
    (hP : ∀ z, HasDerivAt P (-(ρ z * g z)) z) (hg : ∀ z, HasDerivAt g (4 * Real.pi * G * ρ z) z) :
    ∀ z, P z + g z ^ 2 / (8 * Real.pi * G) = P 0 + g 0 ^ 2 / (8 * Real.pi * G) := by
  have hp := Real.pi_pos
  have hd : ∀ z, HasDerivAt (fun z => P z + g z ^ 2 / (8 * Real.pi * G)) 0 z := by
    intro z
    have h2 : HasDerivAt (fun z => g z ^ 2) (2 * g z * (4 * Real.pi * G * ρ z)) z := by
      have := (hasDerivAt_pow 2 (g z)).comp z (hg z)
      refine this.congr_deriv ?_
      simp
    have := (hP z).add (h2.div_const (8 * Real.pi * G))
    refine this.congr_deriv ?_
    field_simp
    ring
  intro z
  exact is_const_of_deriv_eq_zero (fun x => (hd x).differentiableAt) (fun x => (hd x).deriv) z 0

/-- COLUMN BOUND: midplane field 0, pressure -> 0 and field -> g_inf far from the slab, midplane pressure below the cap P_cap = a0^2/(8 pi G):
    then g_inf^2/(8 pi G) = P(0) <= P_cap, so g_inf <= a0, and with Sigma = g_inf/(2 pi G) (Gauss), Sigma <= a0/(2 pi G). -/
theorem slab_column_bound {G a0 Pcap Sig ginf : ℝ} (hG : 0 < G) (ha : 0 < a0) {P g ρ : ℝ → ℝ}
    (hP : ∀ z, HasDerivAt P (-(ρ z * g z)) z) (hg : ∀ z, HasDerivAt g (4 * Real.pi * G * ρ z) z)
    (g0 : g 0 = 0) (hPinf : Tendsto P atTop (𝓝 0)) (hginf : Tendsto g atTop (𝓝 ginf))
    (hcap : P 0 ≤ Pcap) (hPc : a0 ^ 2 = 8 * Real.pi * G * Pcap) (hSig : ginf = 2 * Real.pi * G * Sig) :
    P 0 = ginf ^ 2 / (8 * Real.pi * G) ∧ |ginf| ≤ a0 ∧ Sig ≤ a0 / (4 * Real.pi * G) := by
  have hp := Real.pi_pos
  have key := slab_first_integral hG hP hg
  have hlim : Tendsto (fun z => P z + g z ^ 2 / (8 * Real.pi * G)) atTop (𝓝 (0 + ginf ^ 2 / (8 * Real.pi * G))) :=
    hPinf.add ((hginf.pow 2).div_const _)
  have hconst : Tendsto (fun z => P z + g z ^ 2 / (8 * Real.pi * G)) atTop (𝓝 (P 0 + g 0 ^ 2 / (8 * Real.pi * G))) :=
    tendsto_const_nhds.congr (fun z => (key z).symm)
  have heq := tendsto_nhds_unique hlim hconst
  rw [g0] at heq
  have h1 : P 0 = ginf ^ 2 / (8 * Real.pi * G) := by
    have : ginf ^ 2 / (8 * Real.pi * G) = P 0 + 0 ^ 2 / (8 * Real.pi * G) := by simpa using heq
    simpa using this.symm
  have hpos : 0 < 8 * Real.pi * G := by positivity
  have h2 : ginf ^ 2 ≤ a0 ^ 2 := by
    have : ginf ^ 2 / (8 * Real.pi * G) ≤ Pcap := h1 ▸ hcap
    rw [div_le_iff₀ hpos] at this
    nlinarith
  have h3 : |ginf| ≤ a0 := by
    have := abs_le_of_sq_le_sq' h2 ha.le
    exact abs_le.2 this
  refine ⟨h1, h3, ?_⟩
  have h4 : ginf ≤ a0 := (abs_le.1 h3).2
  rw [hSig] at h4
  rw [le_div_iff₀ (by positivity)]
  nlinarith


/-- the saturating cap never reaches P_cap: 0 <= P_cap x^2/(1+x^2) < P_cap for P_cap > 0 (so the bound is strict for the arctan cap) -/
theorem cap_pressure_lt {Pc x : ℝ} (hPc : 0 < Pc) : 0 ≤ Pc * (x ^ 2 / (1 + x ^ 2)) ∧ Pc * (x ^ 2 / (1 + x ^ 2)) < Pc := by
  have hd : 0 < 1 + x ^ 2 := by positivity
  refine ⟨mul_nonneg hPc.le (div_nonneg (sq_nonneg x) hd.le), ?_⟩
  have : x ^ 2 / (1 + x ^ 2) < 1 := by rw [div_lt_one hd]; linarith
  nlinarith

/-- strict version: if the midplane pressure is strictly below the cap then Sigma < a0/(2 pi G) -/
theorem slab_column_bound_strict {G a0 Pcap Sig ginf : ℝ} (hG : 0 < G) (ha : 0 < a0) {P g ρ : ℝ → ℝ}
    (hP : ∀ z, HasDerivAt P (-(ρ z * g z)) z) (hg : ∀ z, HasDerivAt g (4 * Real.pi * G * ρ z) z)
    (g0 : g 0 = 0) (hPinf : Tendsto P atTop (𝓝 0)) (hginf : Tendsto g atTop (𝓝 ginf))
    (hcap : P 0 < Pcap) (hPc : a0 ^ 2 = 8 * Real.pi * G * Pcap) (hSig : ginf = 2 * Real.pi * G * Sig) :
    Sig < a0 / (2 * Real.pi * G) := by
  have hp := Real.pi_pos
  obtain ⟨h1, h3, _⟩ := slab_column_bound hG ha hP hg g0 hPinf hginf hcap.le hPc hSig
  have hpos : 0 < 8 * Real.pi * G := by positivity
  have h2 : ginf ^ 2 < a0 ^ 2 := by
    have : ginf ^ 2 / (8 * Real.pi * G) < Pcap := h1 ▸ hcap
    rw [div_lt_iff₀ hpos] at this
    nlinarith
  have h4 : ginf < a0 := by
    by_contra hcon
    have hcon' := not_lt.mp hcon
    nlinarith
  rw [hSig] at h4
  rw [lt_div_iff₀ (by positivity)]
  nlinarith

end MineM1

open MineM1 in
#print axioms slab_first_integral
open MineM1 in
#print axioms slab_column_bound
open MineM1 in
#print axioms cap_pressure_lt
open MineM1 in
#print axioms slab_column_bound_strict
