import Mathlib
import ChainCert.PointMass

/-!
# ChainC -- the EXTENDED-PROFILE identities of CFG44 (script B1, checks S2 and S3(S))

Setting (units of the script): G > 0, a0 > 0, r > 0, spherical static Newtonian.  Data, all functions of r:
* `Mb`  enclosed baryonic mass,  `Mb' = 4 pi r^2 rho_b`,  `rho_b >= 0`;
* `Sig` the outer baryonic column `Sigma_out`, taken as a DIFFERENTIABLE function with `Sig' = - rho_b`
        (the decay `Sig -> 0` at infinity, which is what makes `Sig = Int_r^inf rho_b`, is a SEPARATE hypothesis and is
        used only where it is needed: `pressure_unique`, `pressure_nonneg`, `pressure_pos`);
* `Mc`  enclosed cold mass, `Mc' = 4 pi r^2 rho_c`;
* the TARGET (CFG10 (ii), a declared law): `rho_c * g_tot = a0 Mb/(4 pi r^3)`,  `g_tot = G (Mb + Mc)/r^2`.

Every derivative statement is a `HasDerivAt` at a point `r > 0` (never `deriv` of a function used at a junk point).

What is certified (exact real-analysis identities, premises => conclusion):
* (1) `identity_P`      : `P = a0 g_N/(8 pi G) + (a0/2) Sig`  has  `P' = - a0 Mb/(4 pi r^3)`  (no target, no positivity needed);
* (2) `hydrostatic_general`: under the target, `P' = - rho_c g_tot`;   `pressure_unique`: with `P -> 0` at infinity, ANY
        solution of `Q' = - rho_c g_tot` that decays at infinity IS `P`;   `pressure_nonneg`, `pressure_pos`: `P >= 0` (`> 0`);
        `dispersion_ratio`: `sigma^2/(V_c^2/2) = 1 + 4 pi r^2 Sig/Mb` (script (S));
* (3) `target_iff_ode`, `ode_hasDerivAt`: the target is equivalent to `w' = a0 r u_N/u`, `u = G (Mb + Mc)`, `u_N = G Mb`, `w = u - u_N`;
* (4) point mass: `pointMass_*` (Mb constant): the `ChainB` cold mass satisfies the target, `P` reduces to `ChainB.Pfun`,
        the general ODE reproduces `ChainB.target_ODE`, and an `ExtConfig` witness is built from the ChainB data.

What is NOT certified: that the target is the right law (CFG10's declared law); that the ODE has a solution for a given
baryon profile, its uniqueness, or `Mc(0+) = 0`; `rho_c >= 0` on real profiles (only the conditional `rhoC_nonneg`);
`Sig -> 0`/`g_N -> 0` for a given profile (hypotheses); the Jeans/anisotropy identity (B); Eddington positivity;
the barotropic no-go; any GR, relativistic or empirical fact.
-/

open Filter Topology

set_option linter.unusedVariables false

noncomputable section

namespace ChainC

/-- Newtonian field of the baryons: `g_N = G Mb / r^2`. -/
def gN (G : ℝ) (Mb : ℝ → ℝ) (r : ℝ) : ℝ := G * Mb r / r ^ 2

/-- total field felt by the fluid: `g_tot = G (Mb + Mc)/r^2` (`= u/r^2`). -/
def gtot (G : ℝ) (Mb Mc : ℝ → ℝ) (r : ℝ) : ℝ := G * (Mb r + Mc r) / r ^ 2

/-- the target charge `a0 Mb(<r)/(4 pi r^3)`. -/
def charge (a0 : ℝ) (Mb : ℝ → ℝ) (r : ℝ) : ℝ := a0 * Mb r / (4 * Real.pi * r ^ 3)

/-- the hydrostatic pressure of the script's (P): `a0 g_N/(8 pi G) + (a0/2) Sigma_out`. -/
def Pext (G a0 : ℝ) (Mb Sig : ℝ → ℝ) (r : ℝ) : ℝ := a0 * gN G Mb r / (8 * Real.pi * G) + a0 / 2 * Sig r

/-- Pointwise (r > 0) hypotheses of the extended-profile problem, all in one `Prop` so that satisfiability can be
witnessed.  It contains NO decay hypothesis and NO positivity of `rho_c`. -/
structure ExtConfig (G a0 : ℝ) (Mb Mc Sig rhoB rhoC : ℝ → ℝ) : Prop where
  hG : 0 < G
  ha : 0 < a0
  Mb_deriv : ∀ r, 0 < r → HasDerivAt Mb (4 * Real.pi * r ^ 2 * rhoB r) r
  rhoB_nonneg : ∀ r, 0 < r → 0 ≤ rhoB r
  Mb_nonneg : ∀ r, 0 < r → 0 ≤ Mb r
  Sig_deriv : ∀ r, 0 < r → HasDerivAt Sig (-rhoB r) r
  Mc_deriv : ∀ r, 0 < r → HasDerivAt Mc (4 * Real.pi * r ^ 2 * rhoC r) r
  total_pos : ∀ r, 0 < r → 0 < Mb r + Mc r
  target : ∀ r, 0 < r → rhoC r * gtot G Mb Mc r = charge a0 Mb r

/-! ## (1) the identity (P) -/

/-- (1) IDENTITY (P) for an arbitrary profile: `d/dr [a0 g_N/(8 pi G) + (a0/2) Sig] = - a0 Mb/(4 pi r^3)`.
    Hypotheses: `G > 0`, `r > 0`, `Mb' = 4 pi r^2 rho_b`, `Sig' = -rho_b` at `r`.  Nothing else. -/
theorem identity_P {G a0 : ℝ} (hG : 0 < G) {Mb Sig : ℝ → ℝ} {rhoB r : ℝ} (hr : 0 < r)
    (hMb : HasDerivAt Mb (4 * Real.pi * r ^ 2 * rhoB) r) (hS : HasDerivAt Sig (-rhoB) r) :
    HasDerivAt (Pext G a0 Mb Sig) (-(charge a0 Mb r)) r := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have hr2 : r ^ 2 ≠ 0 := by positivity
  have h1 : HasDerivAt (fun r => G * Mb r / r ^ 2)
      ((G * (4 * Real.pi * r ^ 2 * rhoB) * r ^ 2 - G * Mb r * (↑2 * r ^ (2 - 1))) / (r ^ 2) ^ 2) r :=
    (hMb.const_mul G).div (hasDerivAt_pow 2 r) hr2
  have h2 := ((h1.const_mul a0).div_const (8 * Real.pi * G)).add (hS.const_mul (a0 / 2))
  refine h2.congr_deriv ?_
  unfold charge
  field_simp
  ring

/-! ## (2) hydrostatic equilibrium, uniqueness and positivity of the pressure -/

/-- (2) HYDROSTATIC EQUILIBRIUM for every profile: given the target at `r`, `dP/dr = - rho_c g_tot`. -/
theorem hydrostatic_general {G a0 : ℝ} (hG : 0 < G) {Mb Mc Sig : ℝ → ℝ} {rhoB rhoC r : ℝ} (hr : 0 < r)
    (hMb : HasDerivAt Mb (4 * Real.pi * r ^ 2 * rhoB) r) (hS : HasDerivAt Sig (-rhoB) r)
    (hT : rhoC * gtot G Mb Mc r = charge a0 Mb r) :
    HasDerivAt (Pext G a0 Mb Sig) (-(rhoC * gtot G Mb Mc r)) r := by
  rw [hT]; exact identity_P hG hr hMb hS

/-- `charge >= 0` whenever `Mb(r) >= 0` (with `a0, r > 0`). With `identity_P` (`dP/dr = -charge`) this gives the
    derivative sign `dP/dr <= 0`; that combination is not this theorem. -/
theorem charge_nonneg {a0 : ℝ} (ha : 0 < a0) {Mb : ℝ → ℝ} {r : ℝ} (hr : 0 < r) (hM : 0 ≤ Mb r) :
    0 ≤ charge a0 Mb r := by
  unfold charge; positivity

/-- Under the target, positive total mass and `Mb >= 0`, the cold density is nonnegative:
    `rho_c = a0 Mb/(4 pi G r (Mb + Mc))`.  (This is the only positivity of `rho_c` that is certified.) -/
theorem rhoC_nonneg {G a0 : ℝ} (hG : 0 < G) (ha : 0 < a0) {Mb Mc : ℝ → ℝ} {rhoC r : ℝ} (hr : 0 < r)
    (hM : 0 ≤ Mb r) (htot : 0 < Mb r + Mc r) (hT : rhoC * gtot G Mb Mc r = charge a0 Mb r) :
    0 ≤ rhoC := by
  have hg : 0 < gtot G Mb Mc r := by unfold gtot; positivity
  have hc := charge_nonneg ha hr hM
  rw [← hT] at hc
  exact nonneg_of_mul_nonneg_left hc hg

section decay
variable {G a0 : ℝ} {Mb Mc Sig rhoB rhoC : ℝ → ℝ}

/-- `P -> 0` at infinity, from `Sig -> 0` and `g_N -> 0` (the latter holds e.g. for bounded `Mb`; here a hypothesis). -/
theorem Pext_tendsto_zero (hG : 0 < G) (hSig : Tendsto Sig atTop (𝓝 0))
    (hgN : Tendsto (gN G Mb) atTop (𝓝 0)) : Tendsto (Pext G a0 Mb Sig) atTop (𝓝 0) := by
  have h1 := (hgN.const_mul a0).div_const (8 * Real.pi * G)
  have h2 := hSig.const_mul (a0 / 2)
  have h3 := h1.add h2
  simp only [mul_zero, zero_div, add_zero] at h3
  exact h3

/-- (2) UNIQUENESS: any `Q` on `r > 0` with `Q' = - rho_c g_tot` and `Q -> 0` at infinity equals `P` there.
    So, under the decay hypotheses, `P(r) = Int_r^inf rho_c g_tot` is forced to be the script's (P). -/
theorem pressure_unique (C : ExtConfig G a0 Mb Mc Sig rhoB rhoC)
    (hSig : Tendsto Sig atTop (𝓝 0)) (hgN : Tendsto (gN G Mb) atTop (𝓝 0))
    {Q : ℝ → ℝ} (hQ : ∀ r, 0 < r → HasDerivAt Q (-(rhoC r * gtot G Mb Mc r)) r)
    (hQ0 : Tendsto Q atTop (𝓝 0)) : ∀ r, 0 < r → Q r = Pext G a0 Mb Sig r := by
  have hDd : ∀ r, 0 < r → HasDerivAt (fun r => Q r - Pext G a0 Mb Sig r) 0 r := by
    intro r hr
    have := (hQ r hr).sub (hydrostatic_general C.hG hr (C.Mb_deriv r hr) (C.Sig_deriv r hr) (C.target r hr))
    exact this.congr_deriv (by ring)
  set D : ℝ → ℝ := fun r => Q r - Pext G a0 Mb Sig r with hD
  have hconst : ∀ a, 0 < a → ∀ b, 0 < b → D a = D b := by
    intro a ha b hb
    refine (isOpen_Ioi (a := (0:ℝ))).is_const_of_deriv_eq_zero (isPreconnected_Ioi) ?_ ?_ ha hb
    · intro x hx
      exact (hDd x hx).differentiableAt.differentiableWithinAt
    · intro x hx
      simp only [Pi.zero_apply]
      exact (hDd x hx).deriv
  have hlim : Tendsto D atTop (𝓝 0) := by
    have := hQ0.sub (Pext_tendsto_zero (a0 := a0) C.hG hSig hgN)
    simpa using this
  intro r hr
  have hc : Tendsto D atTop (𝓝 (D r)) := by
    refine tendsto_const_nhds.congr' ?_
    filter_upwards [eventually_gt_atTop 0] with s hs
    exact hconst r hr s hs
  have := tendsto_nhds_unique hc hlim
  simp only [hD] at this
  linarith

/-- (2) POSITIVITY of the pressure (the script's H4 / N4 for the pressure, proved): under the target, `Mb >= 0` and the
    decay hypotheses, `P(r) >= 0` for every `r > 0` (`P` is antitone and tends to 0). -/
theorem pressure_nonneg (C : ExtConfig G a0 Mb Mc Sig rhoB rhoC)
    (hSig : Tendsto Sig atTop (𝓝 0)) (hgN : Tendsto (gN G Mb) atTop (𝓝 0)) :
    ∀ r, 0 < r → 0 ≤ Pext G a0 Mb Sig r := by
  have hd : ∀ r, 0 < r → HasDerivAt (Pext G a0 Mb Sig) (-(charge a0 Mb r)) r :=
    fun r hr => identity_P C.hG hr (C.Mb_deriv r hr) (C.Sig_deriv r hr)
  have hanti : AntitoneOn (Pext G a0 Mb Sig) (Set.Ioi 0) := by
    refine antitoneOn_of_deriv_nonpos (convex_Ioi 0) ?_ ?_ ?_
    · intro x hx
      exact (hd x hx).continuousAt.continuousWithinAt
    · rw [interior_Ioi]
      intro x hx
      exact (hd x hx).differentiableAt.differentiableWithinAt
    · rw [interior_Ioi]
      intro x hx
      rw [(hd x hx).deriv]
      have := charge_nonneg C.ha hx (C.Mb_nonneg x hx)
      linarith
  intro r hr
  have h0 := Pext_tendsto_zero (a0 := a0) C.hG hSig hgN
  refine le_of_tendsto h0 ?_
  filter_upwards [eventually_ge_atTop r] with s hs
  exact hanti (Set.mem_Ioi.mpr hr) (Set.mem_Ioi.mpr (lt_of_lt_of_le hr hs)) hs

/-- (2) STRICT positivity: if moreover `Mb > 0` on `r > 0`, then `P(r) > 0`. -/
theorem pressure_pos (C : ExtConfig G a0 Mb Mc Sig rhoB rhoC)
    (hSig : Tendsto Sig atTop (𝓝 0)) (hgN : Tendsto (gN G Mb) atTop (𝓝 0))
    (hMpos : ∀ r, 0 < r → 0 < Mb r) : ∀ r, 0 < r → 0 < Pext G a0 Mb Sig r := by
  have hd : ∀ r, 0 < r → HasDerivAt (Pext G a0 Mb Sig) (-(charge a0 Mb r)) r :=
    fun r hr => identity_P C.hG hr (C.Mb_deriv r hr) (C.Sig_deriv r hr)
  have hanti : StrictAntiOn (Pext G a0 Mb Sig) (Set.Ioi 0) := by
    refine strictAntiOn_of_deriv_neg (convex_Ioi 0) ?_ ?_
    · intro x hx
      exact (hd x hx).continuousAt.continuousWithinAt
    · rw [interior_Ioi]
      intro x hx
      rw [(hd x hx).deriv]
      have hx' : 0 < x := hx
      have : 0 < charge a0 Mb x := by
        unfold charge
        have := hMpos x hx'
        have := C.ha
        positivity
      linarith
  intro r hr
  have h1 := pressure_nonneg C hSig hgN (r + 1) (by linarith)
  have h2 := hanti (Set.mem_Ioi.mpr hr) (Set.mem_Ioi.mpr (by linarith : (0:ℝ) < r + 1)) (by linarith)
  linarith

end decay

/-- (2) the script's (S): `sigma^2/(V_c^2/2) = 1 + 4 pi r^2 Sig/Mb`, with `sigma^2 = P/rho_c`, `V_c^2 = r g_tot`.
    Needs the target at `r` and `Mb(r) != 0`. -/
theorem dispersion_ratio {G a0 : ℝ} (hG : 0 < G) (ha : 0 < a0) {Mb Mc Sig : ℝ → ℝ} {rhoC r : ℝ} (hr : 0 < r)
    (hM : Mb r ≠ 0) (hT : rhoC * gtot G Mb Mc r = charge a0 Mb r) :
    Pext G a0 Mb Sig r / rhoC / (r * gtot G Mb Mc r / 2) = 1 + 4 * Real.pi * r ^ 2 * Sig r / Mb r := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have e : Pext G a0 Mb Sig r / rhoC / (r * gtot G Mb Mc r / 2) = 2 * Pext G a0 Mb Sig r / (r * (rhoC * gtot G Mb Mc r)) := by
    simp only [div_eq_mul_inv, mul_inv]; ring
  rw [e, hT]
  unfold Pext charge gN
  field_simp
  ring

/-! ## (3) the ODE form (T) -/

/-- (3) the target is EQUIVALENT to the ODE `G Mc' = a0 r u_N/u` (`u = G (Mb + Mc)`, `u_N = G Mb`), pointwise, given
    `Mc' = 4 pi r^2 rho_c` and nonzero total mass. -/
theorem target_iff_ode {G a0 : ℝ} (hG : 0 < G) {Mb Mc : ℝ → ℝ} {rhoC r : ℝ} (hr : 0 < r)
    (htot : Mb r + Mc r ≠ 0) :
    rhoC * gtot G Mb Mc r = charge a0 Mb r ↔
      G * (4 * Real.pi * r ^ 2 * rhoC) = a0 * r * (G * Mb r) / (G * (Mb r + Mc r)) := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have hG' : G ≠ 0 := hG.ne'
  unfold gtot charge
  constructor
  · intro h
    field_simp at h ⊢
    nlinarith [h]
  · intro h
    field_simp at h ⊢
    nlinarith [h]

/-- (3) w' = a0 r u_N / u :  with `u = G (Mb + Mc)`, `u_N = G Mb`, `w = u - u_N`, under the target and the derivative
    hypotheses at `r > 0`, `w` has derivative `a0 r u_N(r)/u(r)`. -/
theorem ode_hasDerivAt {G a0 : ℝ} (hG : 0 < G) {Mb Mc : ℝ → ℝ} {rhoB rhoC r : ℝ} (hr : 0 < r)
    (hMb : HasDerivAt Mb (4 * Real.pi * r ^ 2 * rhoB) r) (hMc : HasDerivAt Mc (4 * Real.pi * r ^ 2 * rhoC) r)
    (htot : Mb r + Mc r ≠ 0) (hT : rhoC * gtot G Mb Mc r = charge a0 Mb r) :
    HasDerivAt (fun r => G * (Mb r + Mc r) - G * Mb r)
      (a0 * r * (G * Mb r) / (G * (Mb r + Mc r))) r := by
  have h := ((hMb.add hMc).const_mul G).sub (hMb.const_mul G)
  refine h.congr_deriv ?_
  rw [← (target_iff_ode (a0 := a0) hG hr htot).mp hT]
  ring

/-- `w = u - u_N` is `G Mc` (so the ODE is an ODE for the cold mass). -/
theorem w_eq {G : ℝ} {Mb Mc : ℝ → ℝ} :
    (fun r => G * (Mb r + Mc r) - G * Mb r) = fun r => G * Mc r := by
  funext r; ring

/-! ## (4) the point mass: reduction to `ChainB` -/

section pointmass
variable {G a0 M : ℝ}

/-- the constant enclosed baryonic mass is `Mb = fun _ => M`. -/
abbrev constM (M : ℝ) : ℝ → ℝ := fun _ => M

/-- (4) with `Mb` constant, `gtot` is `ChainB.gtot`. -/
theorem gtot_pointMass (r : ℝ) : gtot G (constM M) (ChainB.Mc G a0 M) r = ChainB.gtot G a0 M r := rfl

/-- (4) THE ChainB COLD MASS SATISFIES THE TARGET for constant `Mb`: `rho_c g_tot = a0 M/(4 pi r^3)`. -/
theorem pointMass_target (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    ChainB.rhoC G a0 M r * gtot G (constM M) (ChainB.Mc G a0 M) r = charge a0 (constM M) r :=
  ChainB.charge_identity hG ha hM hr

/-- (4) `P` of the extended-profile identity reduces to `ChainB.Pfun` when `Mb = M`, `Sig = 0`
    (`Sig = 0` IS `Int_r^inf rho_b` for a point mass: `rho_b = 0` for `r > 0`). -/
theorem Pext_pointMass (hG : 0 < G) (r : ℝ) :
    Pext G a0 (constM M) (fun _ => 0) r = ChainB.Pfun G a0 M r := by
  unfold Pext gN ChainB.Pfun
  by_cases hr : r = 0
  · subst hr; simp
  · have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
    have hG' : G ≠ 0 := hG.ne'
    field_simp
    ring

/-- (4) the general theorems apply to the point mass: an `ExtConfig` with `rho_b = 0`, `Sig = 0`,
    `Mc = ChainB.Mc`, `rho_c = ChainB.rhoC`.  This is also the satisfiability witness with the decay hypotheses. -/
theorem pointMass_config (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) :
    ExtConfig G a0 (constM M) (ChainB.Mc G a0 M) (fun _ => 0) (fun _ => 0) (ChainB.rhoC G a0 M) where
  hG := hG
  ha := ha
  Mb_deriv := fun r hr => by simpa using hasDerivAt_const r M
  rhoB_nonneg := fun r hr => le_rfl
  Mb_nonneg := fun r hr => hM.le
  Sig_deriv := fun r hr => by simpa using hasDerivAt_const r (0:ℝ)
  Mc_deriv := fun r hr => ChainB.Mc_hasDerivAt hG ha hM hr
  total_pos := fun r hr => by
    have := ChainB.sx_pos (r := r) hG ha hM
    unfold ChainB.Mc
    nlinarith
  target := fun r hr => pointMass_target hG ha hM hr

/-- (4) decay hypotheses hold for the point mass. -/
theorem pointMass_decay (hG : 0 < G) :
    Tendsto (fun _ : ℝ => (0:ℝ)) atTop (𝓝 0) ∧ Tendsto (gN G (constM M)) atTop (𝓝 0) := by
  refine ⟨tendsto_const_nhds, ?_⟩
  have h : Tendsto (fun r : ℝ => r ^ 2) atTop atTop := tendsto_pow_atTop (by norm_num)
  show Tendsto (fun r : ℝ => G * M / r ^ 2) atTop (𝓝 0)
  exact tendsto_const_nhds.div_atTop h

/-- (4) the general pressure theorems specialised: for the point mass `P = ChainB.Pfun = a0 M/(8 pi r^2)` is positive
    (from `pressure_pos`, via the general theory) -- a cross-check, not a new claim. -/
theorem pointMass_pressure_pos (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    0 < ChainB.Pfun G a0 M r := by
  have h := pressure_pos (pointMass_config hG ha hM) (pointMass_decay (M := M) hG).1
    (pointMass_decay (M := M) hG).2 (fun r _ => hM) r hr
  rwa [Pext_pointMass hG] at h

/-- (4) the general hydrostatic theorem, specialised to the point mass, gives `ChainB.hydrostatic`. -/
theorem pointMass_hydrostatic (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    HasDerivAt (ChainB.Pfun G a0 M) (-(ChainB.rhoC G a0 M r * ChainB.gtot G a0 M r)) r := by
  have C := pointMass_config hG ha hM
  have h := hydrostatic_general hG hr (C.Mb_deriv r hr) (C.Sig_deriv r hr) (C.target r hr)
  have hf : Pext G a0 (constM M) (fun _ => 0) = ChainB.Pfun G a0 M := by
    funext y; exact Pext_pointMass hG y
  rw [hf] at h
  exact h

/-- (4) the general ODE, specialised to the point mass, reproduces `ChainB.target_ODE`
    (`G dMc/dr = a0 r u_N/u`), through the general `target_iff_ode`/`ode_hasDerivAt` chain. -/
theorem pointMass_ode (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    G * deriv (ChainB.Mc G a0 M) r = a0 * r * (G * M) / (G * (M + ChainB.Mc G a0 M r)) := by
  have C := pointMass_config hG ha hM
  have htot := (C.total_pos r hr).ne'
  have h := ode_hasDerivAt hG hr (C.Mb_deriv r hr) (C.Mc_deriv r hr) htot (C.target r hr)
  rw [w_eq] at h
  have hd := h.deriv
  have hMcd := (C.Mc_deriv r hr).differentiableAt
  rw [deriv_const_mul _ hMcd] at hd
  exact hd

end pointmass

/-! ## Satisfiability witnesses for the pointwise hypotheses -/

section witness

/-- WITNESS 2 (extended, non-degenerate, `Mb` not constant, `rho_b > 0`): the isothermal pair
    `Mb = Mc = (a0/(4G)) r^2`, `rho_b = rho_c = a0/(8 pi G r)`, `Sig = -(a0/(8 pi G)) log r`.
    All pointwise hypotheses of `ExtConfig` hold with the target.  It does NOT satisfy `Sig -> 0`
    (`Sig -> -inf`), so it witnesses `identity_P`, `hydrostatic_general`, `target_iff_ode`, `ode_hasDerivAt`,
    `dispersion_ratio` but not the decay-dependent theorems (the point mass, `pointMass_config`, witnesses those). -/
theorem isothermal_config {G a0 : ℝ} (hG : 0 < G) (ha : 0 < a0) :
    ExtConfig G a0 (fun r => a0 / (4 * G) * r ^ 2) (fun r => a0 / (4 * G) * r ^ 2)
      (fun r => -(a0 / (8 * Real.pi * G)) * Real.log r)
      (fun r => a0 / (8 * Real.pi * G * r)) (fun r => a0 / (8 * Real.pi * G * r)) where
  hG := hG
  ha := ha
  Mb_deriv := fun r hr => by
    have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
    have h := (hasDerivAt_pow 2 r).const_mul (a0 / (4 * G))
    refine h.congr_deriv ?_
    field_simp
    ring
  rhoB_nonneg := fun r hr => by positivity
  Mb_nonneg := fun r hr => by positivity
  Sig_deriv := fun r hr => by
    have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
    have h := (Real.hasDerivAt_log hr.ne').const_mul (-(a0 / (8 * Real.pi * G)))
    refine h.congr_deriv ?_
    field_simp
  Mc_deriv := fun r hr => by
    have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
    have h := (hasDerivAt_pow 2 r).const_mul (a0 / (4 * G))
    refine h.congr_deriv ?_
    field_simp
    ring
  total_pos := fun r hr => by positivity
  target := fun r hr => by
    have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
    have hG' : G ≠ 0 := hG.ne'
    unfold gtot charge
    field_simp
    ring

/-- WITNESS 3 (decaying outer column, `Sig -> 0`, `Mb` bounded): the exponential profile
    `rho_b = e^{-r}`, `Sig = e^{-r}`, `Mb = 4 pi (2 - e^{-r}(r^2 + 2 r + 2))` satisfies the hypotheses of `identity_P`
    at every `r > 0`, with `Sig -> 0`. (No cold fluid is attached: hypotheses of (1) only.) -/
theorem exp_profile_identity_P {G a0 : ℝ} (hG : 0 < G) {r : ℝ} (hr : 0 < r) :
    HasDerivAt (Pext G a0 (fun r => 4 * Real.pi * (2 - Real.exp (-r) * (r ^ 2 + 2 * r + 2)))
        (fun r => Real.exp (-r))) (-(charge a0 (fun r => 4 * Real.pi * (2 - Real.exp (-r) * (r ^ 2 + 2 * r + 2))) r)) r := by
  refine identity_P (rhoB := Real.exp (-r)) hG hr ?_ ?_
  · have h1 : HasDerivAt (fun r : ℝ => Real.exp (-r)) (-Real.exp (-r)) r := by
      simpa using (hasDerivAt_neg r).exp
    have h2 : HasDerivAt (fun r : ℝ => r ^ 2 + 2 * r + 2) (2 * r + 2) r := by
      have := ((hasDerivAt_pow 2 r).add ((hasDerivAt_id r).const_mul 2)).add_const 2
      simpa using this
    have h3 := (((h1.mul h2).const_sub 2).const_mul (4 * Real.pi))
    refine h3.congr_deriv ?_
    ring
  · simpa using (hasDerivAt_neg r).exp

theorem exp_profile_decay : Tendsto (fun r : ℝ => Real.exp (-r)) atTop (𝓝 0) := by
  simpa using Real.tendsto_exp_neg_atTop_nhds_zero

end witness

end ChainC
