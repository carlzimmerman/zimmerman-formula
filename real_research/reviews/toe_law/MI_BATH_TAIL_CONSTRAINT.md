# The missing object's first kill-test: the bath-inertia kernel's high-a tail vs planetary ephemerides

*C. Zimmerman, 2026-06-10. Trilemma calculation #1 (`TOE_TRILEMMA.md`), pushed analytically. This is the first time the
repo's two threads — the Γ_th/Deser-Levin bath kernel and solar-system data — meet. Result, both ways: the bath gives
the deep-MOND LIMIT for free (the original attraction, confirmed), but its natural subtraction scheme predicts a
constant ~cH anomalous acceleration at high a, excluded by planetary ephemerides by ~3.5–4.5 orders; and its deep-MOND
COEFFICIENT is a₀ = 2cH, which overshoots the SPARC-fitting framework value by 2Z ≈ 11.6. Scope: this kills the SPECIFIC
ansatz (gapless response-excess with global-T_dS subtraction), not the modified-inertia class — and in doing so it
converts the "missing object" from an aspiration into a spec sheet. Arithmetic by hand below; sympy/numpy verification
staged (`mi_bath_tail_check.py`) [VERIFY-ON-UNBLOCK]. C1/C2 only.*

## The construction (nothing new assumed — repo pieces only)
1. **Γ_th blind run (banked):** gapless UDW response in dS, Γ = λ²H/2π², τ_c = 1/H.
2. **Deser–Levin (banked, used in the state-existence work):** a detector with proper acceleration a in dS sees
   T_eff = (ħ/2πck_B)·√(a² + (cH)²) — the Unruh and Gibbons–Hawking temperatures add in quadrature.
3. **Milgrom-99 bath-inertia ansatz (the natural one):** inertia ∝ the response EXCESS over the dS floor,
   m_eff/m = [T_eff(a) − T_eff(0)] / T_U(a) ⇒ **μ(x) = [√(x²+1) − 1]/x, x ≡ a/(cH).**
   (The gapless-rate version Γ(a) = λ²√(a²+(cH)²)/2π² gives the same μ — rates ∝ temperatures here.)

## Limit 1 — deep MOND (a ≪ cH): the shape is free, the coefficient is not
√(a²+(cH)²) − cH ≈ a²/(2cH) ⇒ μ ≈ a/(2cH) ⇒ F = m a²/(2cH): the deep-MOND form **emerges**, with
**a₀(bath) = 2cH**. Numbers: cH_Λ = Z·a₀(framework) = 5.789 × 9.36×10⁻¹¹ = 5.42×10⁻¹⁰ m/s² (ρ_DE footing);
cH₀ = 6.55×10⁻¹⁰ (ρ_total footing). So a₀(bath) = 1.08–1.31×10⁻⁹ — **11.6× (= 2Z) to 14× above the SPARC-fitting
9.36×10⁻¹¹.** Consistent with the banked verdict (Z data-selected, not derived); now the bath's OWN coefficient is on
record, and it does not fit galaxies either. *Both-ways note: the often-quoted "a₀ ≈ cH₀/2π ≈ 1.04×10⁻¹⁰" coincidence
uses a 2π the bath construction does not produce; the bath produces 2, not 1/2π.*

## Limit 2 — high a (the NEW constraint): a constant cH anomaly, ephemeris-dead
√(a²+(cH)²) − cH ≈ a − cH + (cH)²/(2a) ⇒ μ ≈ 1 − cH/a ⇒ the EOM μ(a)·a = g_N gives
**a = g_N + cH** — a constant anomalous acceleration of magnitude cH on every solar-system body (Pioneer-sized; the
Pioneer anomaly was thermal recoil, and planets never showed it).
- Saturn: g_N = GM☉/r² = 1.327×10²⁰/(1.433×10¹²)² = **6.46×10⁻⁵ m/s²**; predicted δa = cH = **5.4–6.6×10⁻¹⁰ m/s²**
  (both footings — the kill is footing-robust, checked both ways per the #1 rule).
- Ephemeris bound (PINNED 2026-06-10): **Folkner's Cassini radiometric bound — anomalous radial acceleration at Saturn
  < 10⁻¹⁴ m/s²** (via the Pioneer review, arXiv:1001.3686 §VI); planet-wide, INPOP08 excludes any constant acceleration
  > ~¼ Pioneer ≈ 2.2×10⁻¹⁰ m/s² (Fienga et al., arXiv:0906.3962). The conclusion survives even the soft planet-wide
  bound (cH exceeds it ×2.5); against the Saturn-specific bound it is not close.
- **Excess: ×54,000 ≈ 4.7 orders (ρ_DE footing); ×65,000 ≈ 4.8 orders (ρ_total). The natural bath kernel is dead in the
  solar system.** (`mi_bath_tail_check.py` verified: deep series x/2 ✓, tail 1−u+u²/2 ✓, 2Z = 11.58 ✓, quadratic tail
  2.3×10⁻¹⁵ SAFE ✓.)
- Contrast with the class-evasion (unchanged): modified inertia evades the Desmond/Hees EFE **quadrupole** by class —
  Saturn's proper acceleration is solar-dominated (g_gal/g_N ~ 3×10⁻⁶), so no Q₂ analogue arises. The kill here is a
  DIFFERENT, sharper channel: the radial 1/x tail of this μ. "Evades Cassini by class" never licensed a fat tail.

## The viability line (what the missing object must do — the spec sheet)
- A tail closing one order faster, μ ≈ 1 − (cH)²/(2a²) (the T_eff-quadratic residue), gives
  δa(Saturn) = (cH)²/(2g_N) = (5.42×10⁻¹⁰)²/(1.292×10⁻⁴) = **2.3×10⁻¹⁵ m/s² — SAFE** even against the tightest bound.
  ⇒ **the ephemeris line falls cleanly BETWEEN the linear and quadratic tails: viable kernels must have
  μ − 1 = o(cH/a), e.g. O((cH/a)²) or exponential (a gapped detector's e^{−E/k_BT} response gives the latter naturally).**
- The deep-MOND coefficient must come out ≈ cH/5.8, not 2cH ⇒ the response→inertia coupling must supply ≈1/11.6.
- **Both requirements pinch the SAME unknown the Γ_th run flagged as its conditionality: the Step-4 coupling** (how the
  bath response maps to inertia). One unknown, two quantitative constraints from opposite regimes — that is a spec
  sheet, not a free function: any candidate coupling is now testable on day one against (i) SPARC normalization,
  (ii) the Saturn tail, before any covariance work begins.
- Day-one liability ledger (unchanged, rides along): the type-dependent lensing split (a clock-based law is as
  type-blind as a force-based one), clusters ~2×, a₀(z) at z≈3.

## Honest scope (locked)
- This kills **one ansatz** (gapless response-excess, global-floor subtraction), not modified inertia, not the bath
  idea, and not the kernel a₀(z) ∝ √ρ_DE (which never needed this host). The deep-MOND emergence is the encouraging
  half and it stands.
- Nothing here derives Z = 5.789; the boundary in `TOE_TRILEMMA.md` is unchanged. What changed: the missing object now
  has **numbers it must beat** — the difference between a research direction and a wish.
- [VERIFY-ON-UNBLOCK]: `mi_bath_tail_check.py` (sympy limits + the Saturn arithmetic + both footings); pin the exact
  INPOP/EPM Saturn bound; then commit both with this note.
