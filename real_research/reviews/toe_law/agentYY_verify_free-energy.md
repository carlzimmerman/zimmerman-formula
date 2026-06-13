# agentYY VERIFY — adversarial referee of ROUTE 1 (crossed-product free energy F(a))

*Hostile referee, 2026-06-13. CENTRAL MISSION: is the claimed a~cH feature a GENUINE
thermodynamic EXTREMUM/transition (would DERIVE the scale, DERIVATIONAL), or the smooth
algebraic CROSSOVER of √(a²+H²) relabelled (STRUCTURAL, reproduces what we already knew)?
Independent re-derivation in `agentYY_verify_free-energy.py` (sympy+mpmath). I did NOT reuse
the route's algebra — I rebuilt T(a), the blueshift, the cancellation, F(a), and ran hostile
constructions the route did not try. Units ħ=c=k_B=1, cH=H.*

---

## REGRADE: **CONFIRMED** → verdict stays **STRUCTURAL-CEILING-CONFIRMED**.

The route's claim reproduces independently on every load-bearing number and structure. F(a) is
monotone; the a~H feature is the algebraic crossover of the temperature's two terms, NOT a
thermodynamic extremum or transition. The scale stays EXTERNAL. No genuine forced extremum at
a~cH was shown, so the default holds — and now from a harder push than the route applied.

---

## (1) Independent re-derivation of F(a) and dF/da

Rebuilt from the Killing norm, not copied:
- |ξ| = H/√(a²+H²); Tolman T(a)=T_GH/|ξ| = **√(a²+H²)/2π** — matches banked WW identity (Δ=0).
- **dT/da = a/(2π√(a²+H²)) > 0 for all a>0, zero ONLY at a=0.** T is strictly monotone; the
  a~H "crossover" (where the Unruh term a and the GH term H are comparable) is a feature of T's
  ALGEBRA, not a stationary point of T.
- **The load-bearing cancellation [Part 1]:** ⟨h_obs⟩/T = (q₀·B)/(T_GH·B) = **2πq₀/H, exactly
  a-independent.** Confirmed symbolically (sympy reports a ∉ free_symbols). This is *kinematically
  forced*, not an assumption: the observer (clock) energy and the temperature are both ~1/time,
  so both blueshift by the identical Tolman factor B=1/|ξ|; the ratio is a dimensionless,
  a-free pure number.
- **Literal Witten free energy [Part 2]:** S_gen = ⟨h_obs⟩/T + S₀ = S₀ + 2πq₀/H (a-independent),
  so **F(a) = E − T·S_gen = −T(a)·S₀ = −S₀√(a²+H²)/2π**, **dF/da = −S₀a/(2π√(a²+H²))**. sympy
  solve gives the interior zero set in a>0 = **∅** (only a=0). CONFIRMED.

## (2) Real stationary point with competing a-dependence — or crossover/inflection mistaken?

**It is NOT an extremum; the route did NOT mistake a crossover/inflection for one.** The route
correctly claims F is monotone (it does NOT claim DERIVATIONAL-SCALE-FORCED), and that claim is
right. Numeric scan [Part 5], H=S₀=1:

| a/H | F | F′ | F″ |
|-----|------|------|------|
|0.50|−0.1779|−7.12e−2|−0.1139|
|0.99|−0.2240|−1.120e−1|−0.05712|
|1.00|−0.2251|−1.125e−1|−0.05627|
|1.01|−0.2262|−1.131e−1|−0.05543|
|2.00|−0.3559|−1.424e−1|−0.01424|

F′(a)<0 strictly for all a>0 — **never zero at interior a**; F″ smooth and continuous across
a=H — **no kink, no jump, no latent heat, no transition**. The a~H crossover is descriptive
(reproduces the algebra of T), not a thermodynamic extremum. The central trap is correctly
avoided.

**Hostile pushes the route did NOT run (all confirm monotone, no a~H extremum):**
- [Part 3] **a-dependent OBSERVER entropy** — treat the q-clock as a 1-mode thermal oscillator at
  T(a) with full S_osc(ω/T). dF/da scanned over a∈(0,5]: **NO sign change** (monotone). This is
  a sharper hostile move than the route's bath (Model C) and still gives no extremum.
- **The one escape from the Tolman cancellation: a REST-frame bath whose energy does NOT
  blueshift** (E=q₀ const, S=S₀+K·Tⁿ). Even here dF/da = a·(−Kn(...)−K(...)−S₀(2π)ⁿ)/(...): the
  bracket is a SUM OF POSITIVE TERMS, so **no interior zero** (symbolic ∅; numeric no sign
  change). The deepest reason the ceiling holds: in F=E−TS every physical piece is **positive
  and monotone in T** (E≥0, S≥0), and a sum of −(positive monotone)·(a/√) cannot turn over.
- [Part B/C] E(a) itself, and the bath heat capacity C(T)=Kn(n+1)Tⁿ: **monotone / smooth, no
  singularity** at T(a~H). a~H is an ordinary interior temperature thermodynamically.
- [Part D] reparametrization traps (dF/d(ln a), F/T): no interior extremum; F/T=−S₀ constant.

**The theorem is sound [Part 4]:** since a enters F ONLY through T(a), dF/da = Φ′(T)·dT/da with
dT/da>0 (zero only at a=0); an interior extremum REQUIRES Φ′(T)=0. T(a=H)=√2·H/2π is an
ordinary interior temperature; H is supplied ONCE (the modular offset inside √(a²+H²)) and
cannot ALSO place Φ′=0 at exactly that T. The loophole (opposite-sign Φ=A·Tᵖ−C·Tʳ) needs free
coefficients tuned by hand to land T*=T(a=H) — an INPUT, not algebra-forced — and the crossed
product furnishes no such negative term (E,S≥0). All correct.

## (3) Respects agentQ's worldline no-go? Is the algebra-level evasion real?

**Respected; there is no real evasion that would force the scale [Part 6].** agentQ's no-go is
that the worldline DL-temperature route through horizon/Clausius thermodynamics does not reach
MOND derivationally (the (H/a)² piece is pure scheme / anti-MOND). The free-energy route does
NOT claim to evade it at the algebra level in a scale-forcing way: F(a) is parametrized by the
proper acceleration a OF a boost-orbit WORLDLINE, and a enters ONLY via |ξ|→T(a) — a worldline-
kinematic quantity. No second, non-worldline appearance of H is introduced. So the crossed
product supplies H exactly once, consistent with agentQ; the route's own theorem says the same.
No smuggled evasion.

## (4) c_χ / full Deser–Levin [Part 7]
T=√(a²+(c_χH)²)/2π has identical structure; dT/da>0 (zero only at a=0); the crossover merely
RELABELS to a~c_χH (still an INPUT scale set by H and c_χ). No zero of Φ′ created. Verdict
unchanged — and this is exactly the "crossover relabelled" structural signature, NOT a
derivation.

## QUARANTINE
q=1/4 / Z never asserted by the route or by me. No extremum lands at a~H, so the coefficient
question never arose. Reported both ways at full weight: the monotone prior was the likely
outcome, it survives every hostile alternative convention I could build, and I confirm it is the
convention-robust truth (literal Witten S_gen, invariant-entropy reading, hostile a-dependent
observer entropy, rest-frame non-blueshift-locked bath, full DL with c_χ) — not a default
artifact.

## BOTTOM LINE
extremum_or_crossover: **CROSSOVER (structural)** — the smooth algebraic crossover of √(a²+H²)
relabelled; F(a)=Φ(T(a)) is strictly monotone, F′≠0 at any interior a, F″ smooth at a=H, no
transition. recompute_agrees: **yes** (every load-bearing number and structure reproduced
independently, plus harder hostile pushes all confirm). regrade: **CONFIRMED**.
regraded_verdict: **STRUCTURAL-CEILING-CONFIRMED**. The a0 scale stays an EXTERNAL input.
