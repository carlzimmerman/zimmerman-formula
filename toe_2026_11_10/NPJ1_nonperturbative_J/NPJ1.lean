/-
NPJ1 (non-perturbative origin of J): the algebraic identities that carry verdicts. TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.

1. The Bose-Einstein reading is the law's own Moebius map, and the same map is the Fermi-Dirac / Langmuir occupation:
   x = p/(1-p)  ->  x/(1+x) = p ;   x/(1+x) = 1/(1/x + 1).
2. C-loc: on the point mass, (m r)^2 with m = c_g x a0 and r^2 = G M (1+x)/(x^2 a0) is c_g^2 G M a0 (1+x).
3. Large-N Gross-Neveu (b1): at the broken-phase minimum sigma^2 = M^2 - q (q = g^2 A^2),
   -(M/pi) sigma^2 + (2/(3 pi)) M^3 = -M^3/(3 pi) + (M/pi) q   (analytic in A^2: no |A|^3 below gA = M).
4. BK point mass (a1): a_theta^2 / a_N = alpha^3 Lambda^2/(8 pi M_Pl) given theta'^2 = alpha M/(8 pi M_Pl r^2).
5. Leaf-pair amplitude (b2, c3): B = K nu g^3 a0/(4 pi c)  <->  nu g^3 = 4 pi B c/(K a0).
-/
import Mathlib

theorem npj1_be_moebius (p : ℝ) (hp : p ≠ 1) :
    (p / (1 - p)) / (1 + p / (1 - p)) = p := by
  have h : (1 - p) ≠ 0 := sub_ne_zero.mpr (Ne.symm hp)
  field_simp
  ring

theorem npj1_fd_reading (x : ℝ) (hx : 0 < x) : x / (1 + x) = 1 / (1 / x + 1) := by
  have h1 : x ≠ 0 := ne_of_gt hx
  have h2 : (1 + x) ≠ 0 := by linarith
  field_simp

theorem npj1_cloc (cg x a0 GM : ℝ) (hx : x ≠ 0) (ha : a0 ≠ 0) :
    (cg * x * a0) ^ 2 * (GM * (1 + x) / (x ^ 2 * a0)) = cg ^ 2 * (GM * a0 * (1 + x)) := by
  field_simp

theorem npj1_gn_min (M q : ℝ) :
    -(M / Real.pi) * (M ^ 2 - q) + (2 / (3 * Real.pi)) * M ^ 3
      = -(M ^ 3) / (3 * Real.pi) + (M / Real.pi) * q := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp
  ring

theorem npj1_bk (al L MP M r t2 : ℝ) (hMP : MP ≠ 0) (hM : M ≠ 0) (hr : r ≠ 0)
    (ht : t2 = al * M / (8 * Real.pi * MP * r ^ 2)) :
    ((al * L / MP) ^ 2 * t2) / (M / (MP ^ 2 * r ^ 2)) = al ^ 3 * L ^ 2 / (8 * Real.pi * MP) := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  subst ht
  field_simp

theorem npj1_leaf_amp (K nu g a0 c : ℝ) (hK : K ≠ 0) (ha : a0 ≠ 0) (hc : c ≠ 0) :
    nu * g ^ 3 = 4 * Real.pi * (K * nu * g ^ 3 * a0 / (4 * Real.pi * c)) * c / (K * a0) := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp
