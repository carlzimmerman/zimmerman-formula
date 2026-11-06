/-
QX5 (closure_2026_11_06/QX5_cluster_terms, criteria e3badba22f): the sandwich lemma behind the
class labels. A monotone phantom multiplier F that is at most 1 + eps at a calibration key above k
cannot exceed 1 + eps at k; if a cluster at k needs F >= 1 + delta with delta > eps, no monotone
member of the class exists. Same for antitone keys (class d). kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace QX5

/-- Upper sandwich for a non-decreasing multiplier. -/
theorem mono_cap {F : ℝ → ℝ} (hF : Monotone F) {k khi ε : ℝ}
    (hk : k ≤ khi) (hcal : F khi ≤ 1 + ε) : F k ≤ 1 + ε :=
  le_trans (hF hk) hcal

/-- No monotone member: a cluster key below a calibrated galaxy key cannot get the boost. -/
theorem mono_dead {F : ℝ → ℝ} (hF : Monotone F) {kc kg ε δ : ℝ}
    (hk : kc ≤ kg) (hcal : F kg ≤ 1 + ε) (hneed : 1 + δ ≤ F kc) (hlt : ε < δ) : False := by
  have := mono_cap hF hk hcal
  linarith

/-- Antitone version (class d: boost must grow as the enclosed density falls). -/
theorem anti_dead {F : ℝ → ℝ} (hF : Antitone F) {kc kg ε δ : ℝ}
    (hk : kg ≤ kc) (hcal : F kg ≤ 1 + ε) (hneed : 1 + δ ≤ F kc) (hlt : ε < δ) : False := by
  have := hF hk
  linarith

/-- Group bracket: a monotone F evaluated between two calibrated keys stays between their values. -/
theorem mono_between {F : ℝ → ℝ} (hF : Monotone F) {a k b : ℝ} (h1 : a ≤ k) (h2 : k ≤ b) :
    F a ≤ F k ∧ F k ≤ F b :=
  ⟨hF h1, hF h2⟩

/-- Phantom-multiplier mass is monotone in F (phantom >= 0): more F, more model mass. -/
theorem model_mono {Mb Ml F₁ F₂ : ℝ} (hph : Mb ≤ Ml) (hF : F₁ ≤ F₂) :
    Mb + F₁ * (Ml - Mb) ≤ Mb + F₂ * (Ml - Mb) := by
  have : 0 ≤ Ml - Mb := by linarith
  nlinarith

end QX5

#print axioms QX5.mono_cap
#print axioms QX5.mono_dead
#print axioms QX5.anti_dead
#print axioms QX5.mono_between
#print axioms QX5.model_mono
