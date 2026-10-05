import Mathlib

/-! CFG333: decisive pass/fail inequalities, rational bounds rounded outward from cfg333_one_rule_results.json.
  m = offset (dex) | gamma_hat - gamma_pred | joint-Ups distance to [1.3, 2.2]; e = its 1-sigma error. Pass = |m| < 2e. -/

theorem cfg333_R0_WB_canonical_fail (m e : ℚ) (h1 : m ≤ (-581/1250 : ℚ)) (h2 : e ≤ (11/200 : ℚ)) :
    m ≤ -(2 * e) := by
  linarith

theorem cfg333_R0_GC_canonical_fail (m e : ℚ) (h1 : m ≤ (-3077/5000 : ℚ)) (h2 : e ≤ (1391/10000 : ℚ)) :
    m ≤ -(2 * e) := by
  linarith

theorem cfg333_R0_CL_canonical_pass (m e : ℚ) (h1 : (67/1000 : ℚ) ≤ m) (h2 : m ≤ (671/10000 : ℚ)) (h3 : (521/5000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R0_UFD_canonical_fail (m e : ℚ) (h1 : (649/2000 : ℚ) ≤ m) (h2 : e ≤ (43/500 : ℚ)) :
    2 * e ≤ m := by
  linarith

theorem cfg333_R0_WB_alt_fail (m e : ℚ) (h1 : m ≤ (-4623/10000 : ℚ)) (h2 : e ≤ (32/625 : ℚ)) :
    m ≤ -(2 * e) := by
  linarith

theorem cfg333_R0_GC_alt_fail (m e : ℚ) (h1 : m ≤ (-414/625 : ℚ)) (h2 : e ≤ (259/2000 : ℚ)) :
    m ≤ -(2 * e) := by
  linarith

theorem cfg333_R0_CL_alt_pass (m e : ℚ) (h1 : (47/1000 : ℚ) ≤ m) (h2 : m ≤ (471/10000 : ℚ)) (h3 : (1037/10000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R0_UFD_alt_fail (m e : ℚ) (h1 : (761/2500 : ℚ) ≤ m) (h2 : e ≤ (859/10000 : ℚ)) :
    2 * e ≤ m := by
  linarith

theorem cfg333_R1_WB_canonical_fail (m e : ℚ) (h1 : m ≤ (-581/1250 : ℚ)) (h2 : e ≤ (11/200 : ℚ)) :
    m ≤ -(2 * e) := by
  linarith

theorem cfg333_R1_GC_canonical_fail (m e : ℚ) (h1 : m ≤ (-3077/5000 : ℚ)) (h2 : e ≤ (1391/10000 : ℚ)) :
    m ≤ -(2 * e) := by
  linarith

theorem cfg333_R1_CL_canonical_pass (m e : ℚ) (h1 : (17/200 : ℚ) ≤ m) (h2 : m ≤ (851/10000 : ℚ)) (h3 : (1111/10000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R1_UFD_canonical_fail (m e : ℚ) (h1 : (649/2000 : ℚ) ≤ m) (h2 : e ≤ (43/500 : ℚ)) :
    2 * e ≤ m := by
  linarith

theorem cfg333_R1_WB_alt_fail (m e : ℚ) (h1 : m ≤ (-4623/10000 : ℚ)) (h2 : e ≤ (32/625 : ℚ)) :
    m ≤ -(2 * e) := by
  linarith

theorem cfg333_R1_GC_alt_fail (m e : ℚ) (h1 : m ≤ (-414/625 : ℚ)) (h2 : e ≤ (259/2000 : ℚ)) :
    m ≤ -(2 * e) := by
  linarith

theorem cfg333_R1_CL_alt_pass (m e : ℚ) (h1 : (47/625 : ℚ) ≤ m) (h2 : m ≤ (753/10000 : ℚ)) (h3 : (553/5000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R1_UFD_alt_fail (m e : ℚ) (h1 : (761/2500 : ℚ) ≤ m) (h2 : e ≤ (859/10000 : ℚ)) :
    2 * e ≤ m := by
  linarith

theorem cfg333_R2_WB_canonical_pass (m e : ℚ) (h1 : (749/10000 : ℚ) ≤ m) (h2 : m ≤ (3/40 : ℚ)) (h3 : (11/200 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R2_GC_canonical_pass (m e : ℚ) (h1 : (0 : ℚ) ≤ m) (h2 : m ≤ (0 : ℚ)) (h3 : (2177/5000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R2_CL_canonical_pass (m e : ℚ) (h1 : (67/1000 : ℚ) ≤ m) (h2 : m ≤ (671/10000 : ℚ)) (h3 : (521/5000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R2_UFD_canonical_fail (m e : ℚ) (h1 : (649/2000 : ℚ) ≤ m) (h2 : e ≤ (43/500 : ℚ)) :
    2 * e ≤ m := by
  linarith

theorem cfg333_R2_WB_alt_pass (m e : ℚ) (h1 : (387/5000 : ℚ) ≤ m) (h2 : m ≤ (31/400 : ℚ)) (h3 : (32/625 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R2_GC_alt_pass (m e : ℚ) (h1 : (0 : ℚ) ≤ m) (h2 : m ≤ (0 : ℚ)) (h3 : (2177/5000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R2_CL_alt_pass (m e : ℚ) (h1 : (47/1000 : ℚ) ≤ m) (h2 : m ≤ (471/10000 : ℚ)) (h3 : (1037/10000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R2_UFD_alt_fail (m e : ℚ) (h1 : (761/2500 : ℚ) ≤ m) (h2 : e ≤ (859/10000 : ℚ)) :
    2 * e ≤ m := by
  linarith

theorem cfg333_R3_WB_canonical_pass (m e : ℚ) (h1 : (749/10000 : ℚ) ≤ m) (h2 : m ≤ (3/40 : ℚ)) (h3 : (11/200 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R3_GC_canonical_fail (m e : ℚ) (h1 : m ≤ (-31/80 : ℚ)) (h2 : e ≤ (927/5000 : ℚ)) :
    m ≤ -(2 * e) := by
  linarith

theorem cfg333_R3_CL_canonical_pass (m e : ℚ) (h1 : (959/5000 : ℚ) ≤ m) (h2 : m ≤ (1919/10000 : ℚ)) (h3 : (349/2500 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R3_UFD_canonical_fail (m e : ℚ) (h1 : (1689/2500 : ℚ) ≤ m) (h2 : e ≤ (1593/10000 : ℚ)) :
    2 * e ≤ m := by
  linarith

theorem cfg333_R3_WB_alt_pass (m e : ℚ) (h1 : (387/5000 : ℚ) ≤ m) (h2 : m ≤ (31/400 : ℚ)) (h3 : (32/625 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R3_GC_alt_fail (m e : ℚ) (h1 : m ≤ (-4407/10000 : ℚ)) (h2 : e ≤ (349/2000 : ℚ)) :
    m ≤ -(2 * e) := by
  linarith

theorem cfg333_R3_CL_alt_pass (m e : ℚ) (h1 : (1723/10000 : ℚ) ≤ m) (h2 : m ≤ (431/2500 : ℚ)) (h3 : (1419/10000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg333_R3_UFD_alt_fail (m e : ℚ) (h1 : (1689/2500 : ℚ) ≤ m) (h2 : e ≤ (1593/10000 : ℚ)) :
    2 * e ≤ m := by
  linarith
