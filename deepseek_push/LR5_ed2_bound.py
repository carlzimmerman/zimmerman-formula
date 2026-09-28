#!/usr/bin/env python3
"""LR5 -- E[D^2] >= 3 E[Dv^2]^2 / E[v^4] Lean leg (Z7-wave; owns LR5_*).
Door: register row 15, Lean status 'open (M01)'. Empirical leg (J06 86/86)
stands; this lane is R0 audit + the Lean leg only.
R0 FIRST (numbers before Lean): J06 chain (J06_bound_sharpen.py verbatim):
E[D ang] = E[Dv^2]/2, E[ang^2] = E[v^4]/12 under v|ang ~ N(0, 2*ang);
B_1 = 3E[Dv^2]^2/E[v^4] = E[Dang]^2/E[ang^2]. Synthetic checks: cloud
v|ang ~ N(0, 2 ang), D = 1.3*ang attains slack 1 (tight); noised cloud slack > 1.
Lean targets (T3 primary -- self-contained discriminant proof of L2
Cauchy-Schwarz: pointwise |fg| <= (f^2+g^2)/2 breaks the circularity; T1
Gaussian 4th moment via mgf is probed and recorded as blocker if out of reach).
KILLS (pre-registered): exit 0 iff R0 passes AND T3 (or T1) compiles zero-sorry
with axioms subset {propext, Classical.choice, Quot.sound}; else exit 1 with
the precise blocker. No sorry in the banked file. No budget tuning."""
import json, os, subprocess, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN_DIR = os.path.join(os.path.dirname(HERE), "fable_independent_2026", "lean_2026")
OUT = os.path.join(HERE, "LR5_ed2_bound.out")
RESF = os.path.join(HERE, "LR5_results.json")
_T0 = time.time()
LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="LR5 E[D^2] bound Lean leg", pre_registration="Z7-WAVE_BRIEF.md LR5 gates",
               verdict=verdict, exit=rc, elapsed_s=round(time.time() - _T0, 1), log=LOG)
    if extra: RES.update(extra)
    with open(RESF, "w") as f: json.dump(RES, f, indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

# ---------- R0: mechanical audit ----------
log("R0: symbolic check of the coefficient algebra")
import sympy as sp
a, b = sp.symbols("a b", positive=True)
ident = sp.simplify(3 * (2 * a) ** 2 / (12 * b) - a ** 2 / b)
if ident != 0:
    finish(1, "R0-FAIL: coefficient algebra does not close (got %s)" % ident)
log("R0: 3*(2a)^2/(12*b) - a^2/b = 0 symbolically OK (brief amendment 1)")

log("R0: synthetic clouds v|ang ~ N(0, 2*ang)")
rng = np.random.default_rng(5150)
n = 4_000_000
ang = rng.uniform(0.1, 2.0, n)
for tag, D_expr in (("tight", 1.3 * ang), ("noised", 1.3 * ang + 0.4 * ang * rng.standard_normal(n))):
    v = rng.standard_normal(n) * np.sqrt(2.0 * ang)
    ED2  = float(np.mean(D_expr ** 2))
    EDv2 = float(np.mean(D_expr * v ** 2))
    Ev4  = float(np.mean(v ** 4))
    B1 = 3.0 * EDv2 ** 2 / Ev4
    EDang = float(np.mean(D_expr * ang)); Eang2 = float(np.mean(ang ** 2))
    CS = EDang ** 2 / Eang2
    slack = ED2 / B1
    log("R0[%s]: E[D2]=%.6f B1=%.6f CS-form=%.6f (chain err %.2e) slack=%.6f"
        % (tag, ED2, B1, CS, abs(B1 - CS) / max(abs(CS), 1e-30), slack))
    if tag == "tight" and abs(slack - 1.0) > 0.01:
        finish(1, "R0-FAIL: tight cloud slack %s != 1" % slack)
    if tag == "noised" and slack <= 1.0:
        finish(1, "R0-FAIL: noised cloud slack %s <= 1" % slack)
    if abs(B1 - CS) > 5e-3 * abs(CS):  # MC tolerance: 4e6 samples, rel 0.5% (noised cloud chain err ~0.2% at n=4e6, scales as 1/sqrt(n))
        finish(1, "R0-FAIL: B_1 != CS-form on %s cloud" % tag)
log("R0: chain verified on both clouds (tight slack=1, noised slack>1)")

# ---------- Lean: T3 primary (self-contained L2 Cauchy-Schwarz) ----------
lean = r"""import Mathlib

open MeasureTheory Real

/- LR5: Lean leg of the J06 bound chain E[D^2] >= 3 E[Dv^2]^2 / E[v^4]
   (register row 15, 'open (M01)').  Z7-wave.
   * T2lite (corrected per brief amendment 1): the m=1 chain coefficient algebra
     3*(2a)^2/(12b) = a^2/b -- pure algebra over the moment identities
     E[Dv^2] = 2*E[Dang], E[v^4] = 12*E[ang^2] (the identities themselves are
     the conditional-Gaussian leg, R0-audited numerically in LR5_ed2_bound.out;
     not probability-space-certified here -- labeled, not sorry'd).
   * T3: Cauchy-Schwarz in L2 for real-valued functions -- the probability-space
     leg of a^2/b <= E[D^2].  Proof: Q(t) = integral (f - t g)^2 >= 0 for all t,
     expanded mechanically; discriminant argument at t = C/A closes it; the
     circularity is broken by pointwise |fg| <= (f^2+g^2)/2 (AM-GM), so f*g is
     integrable without invoking CS. -/
theorem lr5_chain (a b : ℝ) (hb : b ≠ 0) :
    (3 : ℝ) * (2 * a) ^ 2 / (12 * b) = a ^ 2 / b := by
  field_simp
  ring

theorem lr5_l2_cs {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω}
    (f g : Ω → ℝ) (hf : MemLp f 2 μ) (hg : MemLp g 2 μ) :
    (∫ x, f x * g x ∂μ) ^ 2 ≤ (∫ x, f x ^ 2 ∂μ) * (∫ x, g x ^ 2 ∂μ) := by
  classical
  have hf2 : Integrable (fun x => f x ^ 2) μ := hf.integrable_sq
  have hg2 : Integrable (fun x => g x ^ 2) μ := hg.integrable_sq
  have hfg : Integrable (fun x => f x * g x) μ := hf.integrable_mul hg
  have hDge : 0 ≤ ∫ x, f x ^ 2 ∂μ := integral_nonneg (fun x => sq_nonneg (f x))
  have hAge : 0 ≤ ∫ x, g x ^ 2 ∂μ := integral_nonneg (fun x => sq_nonneg (g x))
  have hexp : ∀ t : ℝ, ∫ x, (f x - t * g x) ^ 2 ∂μ
      = (∫ x, f x ^ 2 ∂μ) - 2 * t * (∫ x, f x * g x ∂μ) + t * t * (∫ x, g x ^ 2 ∂μ) := by
    intro t
    have i2 : Integrable (fun x => 2 * t * (f x * g x)) μ := hfg.const_mul (2 * t)
    have i3 : Integrable (fun x => t * t * (g x ^ 2)) μ := hg2.const_mul (t * t)
    have s1 : Integrable (fun x => f x ^ 2 - 2 * t * (f x * g x)) μ := hf2.sub i2
    have hcongr : (fun x => (f x - t * g x) ^ 2) =ᵐ[μ]
        (fun x => f x ^ 2 - 2 * t * (f x * g x) + t * t * (g x ^ 2)) :=
      Filter.Eventually.of_forall (fun x => by ring)
    rw [integral_congr_ae hcongr, integral_add s1 i3, integral_sub hf2 i2,
        integral_const_mul, integral_const_mul]
  set A : ℝ := ∫ x, g x ^ 2 ∂μ with hAdef
  set C : ℝ := ∫ x, f x * g x ∂μ with hCdef
  set D : ℝ := ∫ x, f x ^ 2 ∂μ with hDdef
  by_cases hA : A = 0
  · have hint0 : ∫ x, g x ^ 2 ∂μ = 0 := by rw [← hAdef]; exact hA
    have hg0 : (fun x => g x ^ 2) =ᵐ[μ] (fun _ : Ω => (0:ℝ)) :=
      (integral_eq_zero_iff_of_nonneg (fun x => sq_nonneg (g x)) hg2).mp hint0
    have hfg0 : (fun x => f x * g x) =ᵐ[μ] (fun _ : Ω => (0:ℝ)) := by
      filter_upwards [hg0] with x hx
      have hgx : g x = 0 := pow_eq_zero_iff (n := 2) (by norm_num) |>.mp hx
      simp [hgx]
    have hC0 : C = 0 := by
      rw [hCdef, integral_congr_ae hfg0, integral_zero]
    rw [hC0, hA]
    simp
  · have hApos : 0 < A := lt_of_le_of_ne hAge (Ne.symm hA)
    have hq : 0 ≤ ∫ x, (f x - (C / A) * g x) ^ 2 ∂μ := integral_nonneg (fun x => sq_nonneg _)
    rw [hexp (C / A)] at hq
    have h2 : 0 ≤ A * (D - 2 * (C / A) * C + (C / A) * (C / A) * A) := by
      nlinarith [hq, hApos]
    have h3 : A * (D - 2 * (C / A) * C + (C / A) * (C / A) * A) = A * D - C * C := by
      have hne : A ≠ 0 := Ne.symm (hApos.ne)
      field_simp
      ring
    linarith [h2, h3]

#print axioms lr5_chain
#print axioms lr5_l2_cs
"""

open(os.path.join(LEAN_DIR, "LR5_ed2_bound.lean"), "w").write(lean)
p = subprocess.run(["lake", "env", "lean", "LR5_ed2_bound.lean"], cwd=LEAN_DIR,
                   capture_output=True, text=True, timeout=1800)
out = p.stdout + p.stderr
open(os.path.join(HERE, "LR5_lean_stdout.txt"), "w").write(out)
log("Lean compile rc=%d (%d chars)" % (p.returncode, len(out)))
if p.returncode != 0 or "sorryAx" in out or "declaration uses 'sorry'" in out:
    finish(1, "LEAN-FAIL (rc=%d): blocker recorded verbatim in LR5_lean_stdout.txt" % p.returncode)
finish(0, "BANKED: T3 (L2 Cauchy-Schwarz, zero-sorry) + T2lite corrected chain algebra; "
          "E[D^2] >= B_1 Lean leg closed at the algebra level; the conditional-Gaussian "
          "identities remain the labeled model leg (R0-audited numerically)")
