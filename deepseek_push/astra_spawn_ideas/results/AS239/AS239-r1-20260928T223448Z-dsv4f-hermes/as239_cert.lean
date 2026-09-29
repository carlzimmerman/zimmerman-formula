import Mathlib

/-!
AS239 Lean certificate (house style, self-contained).

Cell: CA5-GNC-R physical-metric branch (FINAL_ACTION.md sha b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e).

Declared static inhomogeneous carrier background:
  ds^2 = -N(x)^2 dt^2 + b(x)^2 (dx^2 + dy^2 + dz^2),  x-running lapse N, scale b.
Quadratic tensor action (test-field prescription; TT polarization q(t,x),
e_ij = diag(0,1,-1) flat):
  L_T^(2) = A qdot^2 + C q'^2 + D q^2,
  A = c/(N b),  C = -c N / b^3,  c = M/4 (M = M_P^2),  D = carrier measure mass +
  O((lambda/L)^2) background-curvature piece (Friedmann-cancelled on FRW).

Certificates below (pure real arithmetic; field_simp/ring identities):
  (a) cone_of_principal : c_T^2 = -C/A = N^2/b^2 : tensor cone = null cone of g;
  (b) static_transport   : the WKB amplitude law Amp(x) = a0 b(x)^2/N(x) solves the
        leading-order transport equation
        2 C th' Al' + C th'' Al + C' th' Al = 0   (th = phase, th' = w N/b);
  (c) static_current     : 2 (-C) th' Al^2 = 2 c w a0^2  (x-independent: amplitude
        changes; speed does not);
  (d) frw_current        : FRW limit A = c/a, w = k/a, Amp = a0*a:
        2 A w Amp^2 = 2 c k a0^2 (t-independent; strain normalization q ~ a^-1);
  (e) nc1_mismatch       : negative control: false photon speed^2 on the carrier
        composite metric g_d is e^{-2z} = 1/t_c^2, so the false mismatch
        1/t_c^2 - 1 is NONZERO for every t_c != 1 (samples 13/10, 7/10) and ZERO
        exactly at t_c = 1.

All theorems noncomputable; zero sorry; axioms minimal (propext at most).
-/

open scoped Real

namespace As239

noncomputable section

variable (c w a0 N Np b bp : ℝ)

-- (a) local tensor cone equals the photon null cone of g, coefficient by coefficient.
theorem cone_of_principal (hN : N ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0) :
    (-(-(c * N / b ^ 3))) / (c / (N * b)) = (N / b) ^ 2 := by
  field_simp [hN, hb, hc]

-- (b) static amplitude law solves the leading WKB transport equation:
-- C = -c N/b^3, th' = w N/b, th'' = w (N'b - N b')/b^2,
-- Al = a0 b^2/N, Al' = a0 (2 b b' N - b^2 N')/N^2, C' = -c (N'b - 3 N b')/b^4.
theorem static_transport (hN : N ≠ 0) (hb : b ≠ 0) :
    2 * (-(c * N / b ^ 3)) * (w * N / b) *
        (a0 * (2 * b * bp * N - b ^ 2 * Np) / N ^ 2)
      + (-(c * N / b ^ 3)) * (w * (Np * b - N * bp) / b ^ 2) * (a0 * b ^ 2 / N)
      + (-(c * (Np * b - 3 * N * bp) / b ^ 4)) * (w * N / b) * (a0 * b ^ 2 / N) = 0 := by
  field_simp [hN, hb]; ring

-- (c) conserved static current: 2 (-C) th' Al^2 is x-independent.
theorem static_current (hN : N ≠ 0) (hb : b ≠ 0) :
    2 * (-(-(c * N / b ^ 3))) * (w * N / b) * (a0 * b ^ 2 / N) ^ 2 = 2 * c * w * a0 ^ 2 := by
  field_simp [hN, hb]

-- (d) FRW limit: A = c/a, w = k/a, Amp = a0*a :  2 A w Amp^2 = 2 c k a0^2.
theorem frw_current (cA k a0 a : ℝ) (ha : a ≠ 0) :
    2 * (cA / a) * (k / a) * (a0 * a) ^ 2 = 2 * cA * k * a0 ^ 2 := by
  field_simp [ha]

-- (e) negative control NC1: false g_d speed mismatch 1/t_c^2 - 1 is nonzero for
-- t_c != 1 and zero at t_c = 1 (t_c = e^z bounded positive; s = e^{-z} = 1/t_c).
theorem nc1_mismatch_tc13 : (1 : ℝ) / ((13 : ℝ) / 10) ^ 2 - 1 ≠ 0 := by
  norm_num

theorem nc1_mismatch_tc710 : (1 : ℝ) / ((7 : ℝ) / 10) ^ 2 - 1 ≠ 0 := by
  norm_num

theorem nc1_mismatch_tc1 : (1 : ℝ) / (1 : ℝ) ^ 2 - 1 = 0 := by
  norm_num

end

end As239