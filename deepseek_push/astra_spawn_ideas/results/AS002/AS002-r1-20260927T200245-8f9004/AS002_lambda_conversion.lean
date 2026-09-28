import Mathlib

/-!
# AS002 -- lambda conversion without a hidden Einstein factor (certified algebraic core)

Formal content only. The physical reading, domains and footings are in the accompanying
derivation.md and result.json; nothing here is a physical claim by itself.

Premises (framework inputs, kappa = 1/2 ADOPTED, not derived):
  P1 (Einstein vacuum stress, 8-pi convention):
        rho = Lambda * c^2 / (8 * pi * G_E)
  P2 (framework scale):  a0^2 = G_N * c^2 * rho / 4

Certified statements:
  T1  AS002_lambda_conversion        :  Lambda = 32*pi*(G_E/G_N)*a0^2/c^4
  T2  AS002_lambda_sameG             :  G_E = G_N specialisation, Lambda = 32*pi*a0^2/c^4
  T1c AS002_lambda_converse_scale_sq :  a0^2 = G_N*Lambda*c^4/(32*pi*G_E)  (converse leg)
  K1a AS002_wrong_einstein_factor    :  dropping the 8*pi in P1 shifts the reconstructed
                                             scale by exactly sqrt(8*pi): a0'^2 = 8*pi*a0^2
  K1b AS002_wrong_lambda_factor      :  the same error reads Lambda_wrong = 4*a0^2/c^4
                                             ( = Lambda_correct/(8*pi) )
  T3  AS002_general_kappa_at_half    :  general-kappa form reduces to T1 at kappa^2 = 1/4

All variables real; division requires the cited non-zero hypotheses; positivity premises are
stated where a square root or a division is the physical reading. No sorry / admit.
-/

open Real

/-- T1: the two premises entail Lambda = 32*pi*(G_E/G_N)*a0^2/c^4 (asymmetric couplings). -/
theorem AS002_lambda_conversion (G_E G_N rho a0 Lambda c : ℝ)
    (hGE : G_E ≠ 0) (hGN : G_N ≠ 0) (hc : c ≠ 0)
    (h1 : rho = Lambda * c ^ 2 / (8 * Real.pi * G_E))
    (h2 : a0 ^ 2 = G_N * c ^ 2 * rho / 4) :
    Lambda = 32 * Real.pi * (G_E / G_N) * a0 ^ 2 / c ^ 4 := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  have ha0sq : a0 ^ 2 = G_N * Lambda * c ^ 4 / (32 * Real.pi * G_E) := by
    calc
      a0 ^ 2 = G_N * c ^ 2 * rho / 4 := h2
      _ = G_N * c ^ 2 * (Lambda * c ^ 2 / (8 * Real.pi * G_E)) / 4 := by
        rw [h1]
      _ = G_N * Lambda * c ^ 4 / (32 * Real.pi * G_E) := by
        field_simp [hpi, hGE, hc] <;> ring
  calc
    Lambda = 32 * Real.pi * (G_E / G_N) * a0 ^ 2 / c ^ 4 := by
      rw [ha0sq]
      field_simp [hpi, hGE, hGN, hc] <;> ring

/-- T2: same-G specialisation (the framework contract / README identity). -/
theorem AS002_lambda_sameG (GN rho a0 Lambda c : ℝ)
    (hGN : GN ≠ 0) (hc : c ≠ 0)
    (h1 : rho = Lambda * c ^ 2 / (8 * Real.pi * GN))
    (h2 : a0 ^ 2 = GN * c ^ 2 * rho / 4) :
    Lambda = 32 * Real.pi * a0 ^ 2 / c ^ 4 := by
  have h := AS002_lambda_conversion GN GN rho a0 Lambda c hGN hGN hc h1 h2
  calc
    Lambda = 32 * Real.pi * (GN / GN) * a0 ^ 2 / c ^ 4 := h
    _ = 32 * Real.pi * a0 ^ 2 / c ^ 4 := by
      field_simp [hGN, hc, Real.pi_ne_zero]

/-- T1c: converse leg -- P1 and P2 fix a0^2 uniquely from Lambda, G_E, G_N. -/
theorem AS002_lambda_converse_scale_sq (G_E G_N rho a0 Lambda c : ℝ)
    (hGE : G_E ≠ 0) (hGN : G_N ≠ 0) (hc : c ≠ 0)
    (h1 : rho = Lambda * c ^ 2 / (8 * Real.pi * G_E))
    (h2 : a0 ^ 2 = G_N * c ^ 2 * rho / 4) :
    a0 ^ 2 = G_N * Lambda * c ^ 4 / (32 * Real.pi * G_E) := by
  calc
    a0 ^ 2 = G_N * c ^ 2 * rho / 4 := h2
    _ = G_N * c ^ 2 * (Lambda * c ^ 2 / (8 * Real.pi * G_E)) / 4 := by
      rw [h1]
    _ = G_N * Lambda * c ^ 4 / (32 * Real.pi * G_E) := by
      field_simp [Real.pi_ne_zero, hGE, hc] <;> ring

/-- K1a: the negative control -- removing the 8*pi from the density definition changes the
reconstructed same-G scale by exactly sqrt(8*pi):  a0'^2 = 8*pi*a0^2. -/
theorem AS002_wrong_einstein_factor (GN a0 a0' Lambda c : ℝ)
    (hGN : GN ≠ 0) (hc : c ≠ 0)
    (hbad : a0' ^ 2 = GN * c ^ 2 * (Lambda * c ^ 2 / GN) / 4)
    (hgood : a0 ^ 2 = Lambda * c ^ 4 / (32 * Real.pi)) :
    a0' ^ 2 = 8 * Real.pi * a0 ^ 2 := by
  rw [hbad, hgood]
  field_simp [Real.pi_ne_zero, hGN, hc] <;> ring

/-- K1b: the same hidden-factor error expressed on the Lambda side:
Lam_wrong = 4*a0^2/c^4  ( = Lambda_correct / (8*pi) ). -/
theorem AS002_wrong_lambda_factor (GN a0 rho Lambda_wrong c : ℝ)
    (hGN : GN ≠ 0) (hc : c ≠ 0)
    (hrho : rho = 4 * a0 ^ 2 / (GN * c ^ 2))
    (hbad : rho = Lambda_wrong * c ^ 2 / GN) :
    Lambda_wrong = 4 * a0 ^ 2 / c ^ 4 := by
  rw [hrho] at hbad
  field_simp [hGN, hc] at hbad
  have hbadsymm : Lambda_wrong * c ^ 4 = 4 * a0 ^ 2 := by
    calc
      Lambda_wrong * c ^ 4 = c ^ 4 * Lambda_wrong := by ring
      _ = 4 * a0 ^ 2 := hbad.symm
  calc
    Lambda_wrong = Lambda_wrong * c ^ 4 / c ^ 4 := by
      field_simp [hc] <;> ring
    _ = 4 * a0 ^ 2 / c ^ 4 := by
      rw [hbadsymm]

/-- T3: the general-kappa form Lambda = 8*pi*(G_E/G_N)*a0^2/(kappa^2*c^4) reduces to T1
when kappa^2 = 1/4 (the adopted kappa = 1/2). -/
theorem AS002_general_kappa_at_half (G_E G_N kappa a0 Lambda c : ℝ)
    (hGE : G_E ≠ 0) (hGN : G_N ≠ 0) (hc : c ≠ 0)
    (hk2 : kappa ^ 2 = 1 / 4)
    (hgen : Lambda = 8 * Real.pi * (G_E / G_N) * a0 ^ 2 / (kappa ^ 2 * c ^ 4)) :
    Lambda = 32 * Real.pi * (G_E / G_N) * a0 ^ 2 / c ^ 4 := by
  calc
    Lambda = 8 * Real.pi * (G_E / G_N) * a0 ^ 2 / (kappa ^ 2 * c ^ 4) := hgen
    _ = 8 * Real.pi * (G_E / G_N) * a0 ^ 2 / ((1 / 4) * c ^ 4) := by
      rw [hk2]
    _ = 32 * Real.pi * (G_E / G_N) * a0 ^ 2 / c ^ 4 := by
      field_simp [Real.pi_ne_zero, hGN, hc] <;> ring

#check AS002_lambda_conversion
#check AS002_lambda_sameG
#check AS002_lambda_converse_scale_sq
#check AS002_wrong_einstein_factor
#check AS002_wrong_lambda_factor
#check AS002_general_kappa_at_half

#print axioms AS002_lambda_conversion
#print axioms AS002_lambda_sameG
#print axioms AS002_lambda_converse_scale_sq
#print axioms AS002_wrong_einstein_factor
#print axioms AS002_wrong_lambda_factor
#print axioms AS002_general_kappa_at_half