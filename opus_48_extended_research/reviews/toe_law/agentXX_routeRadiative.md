# agentXX ROUTE 1 — dS-RADIATIVE / CURVATURE-INDUCED c_chi(H): does dS curvature LOCK the khronon sound speed to H?

*agentXX, 2026-06-13. Files: `agentXX_routeRadiative.py` → `.out` (part 1, the dS dispersion +
size of the curvature correction) and `agentXX_routeRadiative_part2.py` → `.out` (part 2, the
adversarial robustness: linear-K, symmetry protection, GH-thermal, scale separation). Read first
and ONLY: `agentU_khronon_m22.md` (the khronon EFT, c_1..c_4 conventions, the spin-0 sound speed,
the Cherenkov corner c_chi² ∈ [1.000, 1.033], the strong-coupling floor M_SC ≳ meV). All numbers
machine-generated. Coefficient quarantine held: q=1/4, Z, the coefficient never asserted. Maximum
hostility applied to the FRAMEWORK-FAVORABLE outcome (a lock) — I gave the lock its strongest shot
(linear-K enhancement, thermal route) and it failed on the merits. No git.*

---

## THE QUESTION (the recurring residual, stated)

Across the mechanism arc (agentSS, RR, TT, UU) the SAME residual blocks fold delivery: the edge
coincidence **R = G_sat** fails to be FORCED because **R is H-intrinsic** (set by the dS scale H /
the Gibbons-Hawking modular structure) while **G_sat is c_chi-intrinsic** (set by the khronon sound
speed c_chi), and the two are SCALE-DECOUPLED. The fix would be a **c_chi ↔ H SCALE-LOCK**: if the
khronon sound speed is dynamically fixed to a power of H, the two scales tie and the coincidence
becomes automatic.

ROUTE 1 tests the **dS-RADIATIVE / CURVATURE-INDUCED** lock: does the dS BACKGROUND (Ricci
R = 12H², foliation extrinsic curvature K = ∇·u = 3H) generate a correction δ(c_chi²) that drives
c_chi toward an H-determined value?

---

## VERDICT UP FRONT

**FREE-MUST-TUNE.** The dS curvature does NOT lock c_chi to H. The bare spin-0 sound speed is a
dimensionless **ratio of Lagrangian couplings** c_chi² = c₁₂₃(2−c₁₄)/[c₁₄(1−c₁₃)(2+c₁₃+3c₂)] — no
curvature scale appears in it. Every dS-curvature correction is suppressed by **(H/M)²** where M is
the khronon Lorentz-violating scale, bounded BELOW by the strong-coupling floor **M ≳ meV ≈ 10^29.8 H**.
The correction is therefore **10⁻⁶⁰ (at M = meV) to 10⁻¹²² (at M = M_Pl)** — negligible by 60–122
orders. A genuine O(1) lock would require **M ~ H**, which the EFT validity / strong-coupling floor
**forbids** by ≥ 30 decades. c_chi remains a **free PPN coupling that must be TUNED** to land the
edge coincidence. This is exactly the recurring residual, now QUANTIFIED: R (H-intrinsic) and
c_chi/G_sat (M-intrinsic, M ≥ meV) are decoupled by ≥ 30 decades, and dS curvature supplies only an
(H/M)² lever — far too weak to bridge the gap.

---

## THE COMPUTATION

### [1] The bare spin-0 sound speed is a scale-free coupling ratio
Einstein-aether / khronometric spin-0 (khronon) speed, standard Jacobson form (c₁..c₄,
1711.08845/1802.04303 convention):

> **c_chi² = c₁₂₃ (2 − c₁₄) / [ c₁₄ (1 − c₁₃)(2 + c₁₃ + 3c₂) ]**

with c₁₃ = c₁+c₃, c₁₄ = c₁+c₄, c₁₂₃ = c₁+c₂+c₃. This is **dimensionless and contains no H, no
curvature, no scale** — it is set entirely by the (free, marginal) c_i. **Bare c_chi is a free
Lagrangian coupling.** (agentU banked it FREE in the Cherenkov corner [1.000, 1.033].)

### [2]–[3] The dS dispersion: the H-correction rides (H/k)²
In dS (flat slicing, a = e^{Ht}, khronon T = t + χ, χ the spin-0 Goldstone), the background scalars
are ∇·u = 3H, u·∇u = 0, R = 12H². The Goldstone dispersion is

> **ω² + 3iHω = c_chi² k_phys² + ξ H²**   (Hubble friction 3H; curvature-induced mass ξH², ξ=O(1))

Reading off the effective sound speed at physical wavenumber: **c_eff²(k) = c_chi² + ξ(H/k_phys)²**.
The H-dependence is an **IR (long-wavelength) correction that VANISHES sub-horizon** (k→∞).

### [4] At the fold band the IR correction is ~10⁻¹⁰
The fold / edge coincidence lives at the banked fold band k_fold ~ 1.1×10⁵ k_H (agentRR/SS;
k_fold/k_H = 1.1e5). At that scale **(H/k_phys)² ≈ 8.3×10⁻¹¹** — the IR curvature correction is
~10⁻¹⁰ × O(1). NEGLIGIBLE.

### [5] The UV / radiative correction δ(c_chi²) ~ (H/M)² — dead by 60–122 orders
A k-independent curvature coupling (R/M²)(∇χ)² → δc_chi² = #·12H²/M². Sizing across M
(H₀ in energy = ℏH₀ = 1.45×10⁻⁴² GeV):

| M (khronon LV scale) | (H/M)² |
|---|---|
| M_Pl (2.4×10¹⁸ GeV) | 3.5×10⁻¹²¹ |
| GUT (10¹⁶ GeV) | 2.1×10⁻¹¹⁶ |
| TeV | 2.1×10⁻⁹⁰ |
| GeV | 2.1×10⁻⁸⁴ |
| eV | 2.1×10⁻⁶⁶ |
| **meV (strong-coupling floor)** | **2.1×10⁻⁶⁰** |

Even at the LOWEST physically allowed LV scale (M_SC ≳ meV, agentU/1711.08845 Eq.15), δ(c_chi²) is
~10⁻⁶⁰. **c_chi is UNMOVED.**

### [6] / [E] Inversion — a lock needs M ~ H, which the EFT floor forbids
For δ(c_chi²) ~ O(c_chi²) ~ O(1) one needs **M ~ √12 H ~ 3.5 H**, i.e. the LV scale must sit AT THE
HUBBLE SCALE. But M ≥ M_SC ≳ meV ≈ **10^29.8 H** — the controlling scale is **≥ 30 decades above
H**. The two scales are decoupled by ≥ 30 decades; an (H/M)² lever cannot bridge it. **NO RADIATIVE
LOCK.**

---

## ADVERSARIAL ROBUSTNESS (part 2 — giving the lock its strongest shot)

- **(A) Linear-in-K enhancement — SYMMETRY-FORBIDDEN.** K = ∇·u = 3H is O(H¹); an operator
  (K/M)(∇χ)² would give δc_chi² ~ 3H/M (ONE power — much larger). But **K is T-ODD** (flips under
  u → −u / time reversal) while (∇χ)² is T-EVEN, so (K/M)(∇χ)² is T-odd and **forbidden** in the
  T-invariant khronon action (built from T-even quadratics (u·∇u)², (∇u)², (∇·u)²). The leading
  ALLOWED curvature shift is quadratic K²/M² ~ (H/M)². (And even the forbidden linear term is
  10⁻³⁰..10⁻⁶⁰ — still dead.)
- **(B) c_chi is a free, self-renormalizing coupling.** It runs logarithmically by O(c_i²/16π²),
  a SELF-correction set by the c_i — NOT an H-dependent one. No symmetry pins a specific value; dS
  enters only via (curvature/M²) insertions, already (H/M)².
- **(C) No SYMMETRY pins c_chi — and a symmetry lock wouldn't help anyway.** dS does not restore
  boost invariance for the khronon (it EXISTS to break boosts). c_T² = 1/(1−β) = 1 is forced by
  GW170817 but that fixes the SPIN-2 speed (via β); the SPIN-0 c_chi is a separate combination, NOT
  fixed by c_T (agentU banked it free in [1.000, 1.033]). Crucially: even IF a symmetry pinned
  c_chi, it would give a CONSTANT, **not c_chi = f(H)** — R(H) would still slide against G_sat(const)
  and the coincidence would still fail. A symmetry lock is the wrong KIND of lock for this residual.
- **(D) Gibbons-Hawking thermal shift.** T_dS = H/2π; the finite-T correction to a sound speed is
  ~(T_dS/M)² = (H/M)² — same dead suppression (10⁻⁶² at meV, 10⁻¹²³ at M_Pl). The thermal route
  gives no lock either.

---

## HONEST SCOPE / WHAT WOULD CHANGE THIS

- The verdict is **convention-robust** in M: across the entire allowed range of the khronon LV scale
  (meV → M_Pl) the correction is ≤ 10⁻⁶⁰. There is no choice of M (consistent with the EFT) that
  produces a lock.
- The verdict **hinges structurally on M ≫ H** (the strong-coupling floor M_SC ≳ meV from
  1711.08845 Eq.15). This is not a tunable convention — it is EFT validity. If a future construction
  put a NEW dynamical field at the Hubble scale (M ~ H) coupling to (∇χ)², that would be **new
  physics** (a Hubble-scale sector), not a dS-radiative effect on the existing khronon — and it is
  out of scope for ROUTE 1 (it belongs to a symmetry/dynamical route, not the curvature-correction
  route tested here).
- **The lock this route would need does not exist in this route.** δ(c_chi²) ~ (H/M)² with M ≥ meV
  is the entire story; it is negligible. ROUTE 1 returns NEEDS-NEW-INPUT, exactly the honest prior.

---

## VERDICT (structured)

- **route:** dS-radiative / curvature-induced correction δ(c_chi²) ~ (H/M)² to the khronon spin-0
  sound speed in a de Sitter background.
- **computed:** bare c_chi² = ratio of c_i (scale-free, free); dS dispersion ω²+3iHω = c_chi²k²+ξH²
  → c_eff² = c_chi² + ξ(H/k)², IR-only (~8.3×10⁻¹¹ at the fold band); UV/radiative δc_chi² ~ (H/M)²
  = 10⁻⁶⁰ (meV) to 10⁻¹²² (M_Pl); linear-K enhancement T-odd → forbidden; GH-thermal (H/M)²; a lock
  needs M~H, forbidden by M_SC ≳ meV ≈ 10^29.8 H.
- **lock_status:** FREE-MUST-TUNE.
- **c_chi(H):** none forced. c_chi is protected as a free Lagrangian coupling ratio; the only
  H-dependence dS supplies is δ(c_chi²) ~ (H/M)² with M ≥ meV ≫ H, so c_chi(H) ≈ c_chi^bare ×
  [1 + O(10⁻⁶⁰)] — i.e. c_chi stays at its free bare value to 60+ decimal places. To land the edge
  coincidence R = G_sat, c_chi must be TUNED by hand (the Cherenkov-corner value), not set by H.
- **verdict:** FREE-PARAMETER.
