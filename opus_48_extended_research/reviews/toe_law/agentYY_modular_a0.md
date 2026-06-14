# agentYY — the modular FREE-ENERGY / a0-SCALE verdict (banking memo)

*agentYY, 2026-06-13. WW (commit 4549c61b) proved the framework's QM foundation is the type II_1
dS observer algebra (Witten crossed product arXiv:2112.12828; CLPW 2206.10780) and that the
Deser–Levin temperature T_DL=(ħ/2π)√(a²+(cH)²) IS the boost-KMS modular temperature (machine-
verified, STRUCTURAL). WW graded it STRUCTURAL not DERIVATIONAL and named the ONLY known route to
a derivational upgrade: does the dressed observer's crossed-product FREE ENERGY F(a)=E−T·S_gen (or
the relative/generalized entropy S(a)) along a boost orbit of acceleration a have a genuine
thermodynamic EXTREMUM (dF/da=0 / a transition) at a~cH — FORCING the inertial transition scale
from the type II_1 modular thermodynamics WITHOUT φ — or is it monotone so the scale stays
external? Two routes computed (free-energy, relative-entropy), each with a hostile verifier.
Units ħ=c=k_B=1 ⇒ cH=H. Coefficient quarantine (q=1/4, Z) held throughout; φ never invoked.*

---

## OVERALL VERDICT: **STRUCTURAL-CEILING-CONFIRMED**

The type II_1 modular thermodynamics **REPRODUCES** the a0 scale but does **NOT DERIVE** it. Both
named thermodynamic objects — the crossed-product free energy F(a) and the relative entropy
S_rel(a) — are **strictly monotone in a with no interior extremum and no transition at a~cH**. The
a~H feature is the *algebraic crossover* of √(a²+H²) (where the Unruh term a and the GH term H are
comparable inside the modular temperature), reproduced descriptively by the structural identity —
NOT a thermodynamic extremum (derived). WW's structural/derivational boundary is **confirmed
SHARPER from both the free-energy and the entropy side.** The a0 scale stays an EXTERNAL input
(modular offset H + worldline acceleration a). No quarantined coefficient (q=1/4, Z) enters,
because no extremum lands at a~cH — there is nothing to probe.

**Plain answer to the mandatory question:** The type II_1 QM foundation **CANNOT DERIVE** the a0
scale. It only **REPRODUCES** it. The crossover at a~cH sits inside √(a²+H²) *by construction* (H
is the modular offset, supplied ONCE); the thermodynamics contains no stationary condition,
extremum, or transition that singles out a=H, so the scale is not forced — it remains an input.

---

## ROUTE LEDGER (counted at VERIFIED grade only)

Both routes computed, both independently verified by a hostile checker, both regraded CONFIRMED.

### Route 1 — crossed-product FREE ENERGY F(a) — VERIFIED: STRUCTURAL-CEILING-CONFIRMED
- **Object:** F(a)=E−T·S_gen along a boost orbit, T(a)=√(a²+H²)/2π the WW-banked modular (Tolman-
  blueshifted GH/boost-KMS) temperature, Witten/CLPW type II_1 dressed generator ĥ=H_mod+q,
  S_gen=⟨ĥ⟩/T+S_out.
- **Computed:** F(a) is MONOTONE — no extremum, no transition at a~H. The load-bearing structural
  fact: the Witten observer-energy term ⟨ĥ⟩/T = E/T is **a-INVARIANT** because proper energy
  E(a)=q₀·B(a) and temperature T(a)=T_GH·B(a) blueshift by the IDENTICAL Tolman factor
  B=1/|ξ|=√(a²+H²)/H, so it cancels — leaving **F(a)=−T(a)·S₀=−S₀√(a²+H²)/2π** with
  **dF/da=−S₀·a/(2π√(a²+H²))**, zero only at a=0, never at a~H. Tested across 3 physically-
  distinct energy/entropy assignments (literal Witten S_gen; frame-invariant entropy; hostile
  a-dependent conformal bath F_gas=−K·Tⁿ⁺¹, any n>0 ⇒ bracket >0 ⇒ monotone for EVERY n).
- **THEOREM (the structural ceiling):** the crossed product fixes ONE generator (β=2π/H, boost),
  and the worldline enters ONLY through T(a), so **F(a)=Φ(T(a))**. Since dT/da>0 strictly (zero
  only at a=0), an interior extremum requires Φ′(T)=0; but T(a=H)=√2·H/2π is an ordinary interior
  temperature, and H is supplied only ONCE (the modular offset), so it cannot ALSO place Φ′=0 at
  a~H. Forcing a~H would require H to appear a SECOND time in Φ — absent from the type II_1
  crossed product. Opposite-sign turnover loophole (Φ=A·Tᵖ−C·Tʳ): the stationary T* is set by
  FREE coefficients; pinning T*=T(a=H) is by-hand tuning, not algebra-forced, and no such term
  arises from E≥0, S≥0.
- **Transition test:** F and all derivatives smooth/analytic in a²; F″ at a/H=0.50/0.99/1.00/1.01/
  2.00 = −0.114/−0.0571/−0.0563/−0.0554/−0.0142 — no kink, jump, or latent heat. Full Deser–Levin
  √(a²+(c_χH)²) identical structure; crossover merely relabels to a~c_χH (still input).
- **Verifier (hostile, CONFIRMED):** independently re-derived F(a)=−S₀√(a²+H²)/2π; strictly
  monotone, F″ smooth at a=H; the Tolman cancellation ⟨h_obs⟩/T=2πq₀/H is exactly a-independent
  (sympy confirms a∉free_symbols). Added harder pushes — a-dependent observer entropy via a 1-mode
  thermal clock, a rest-frame non-blueshift-locked bath (the only escape from the Tolman
  cancellation), E(a) itself, bath heat capacity, reparametrization traps — ALL confirm no
  interior extremum, because in F=E−TS every physical piece is positive and monotone in T. Did NOT
  mistake the crossover/inflection for an extremum.
- **Artifacts:** `agentYY_routeFreeEnergy.py`, `agentYY_routeFreeEnergy.md`.

### Route 2 — relative / generalized ENTROPY S_rel(a) — VERIFIED: STRUCTURAL-CEILING-CONFIRMED
- **Object:** Araki relative entropy S_rel(ρ_a‖ρ_GH) of the accelerated boost-orbit state vs the
  Gibbons–Hawking state, using WW's identity that T_DL IS the boost-KMS modular temperature, so
  ρ_a and ρ_GH are two KMS states of the SAME boost generator at β_a=2π/√(a²+H²), β_GH=2π/H.
  Explicit spectral models: M1 (single boost-frequency oscillator / Unruh-Planck) and M2 (the
  genuine type II_1 / DSSYK dS QNM ladder E_n=λ(Δ+n), agentS-banked). Plus algebra-level Jacobson
  dQ=T_mod dS_gen with Witten's crossed-product generalized entropy.
- **Computed:** S_rel(a) is **strictly MONOTONE increasing** (dS_rel/da>0 at every scanned
  a∈[1e-4,5000]H, all models); single global minimum at a=0 (the GH state, S_rel=0); no turnover.
  The ONLY feature is the inflection d²S_rel/da²=0 (peak of the modular response), and it **SLIDES
  with the probe knob Ω/H** (a*/H = 2.08…225 for Ω/H=0.05…5, tracking where T_DL~Ω — a probe
  scale, not cosmological). In the cold/heavy-probe limit (M2 QNM ladder) it FREEZES at
  **a*/H=1/√2=0.7071**, which sympy confirms is EXACTLY the inflection of the bare blueshift map
  β=2π/√(a²+H²) [d²β/d(a/H)²∝(2(a/H)²−1)] — the algebraic crossover of √(a²+H²), NOT a derived
  extremum, and a factor ~8 from a~cH (Z=5.789). Algebra-level Clausius reduces to the factor
  (1−T_mod·β_GH)=1−√(a²+H²)/H=1−1/|ξ| — the pure Tolman blueshift, the SAME object agentQ found, so
  the algebra **INHERITS agentQ's worldline no-go rather than evading it** (no independent dT_DL/da
  inertia-side channel appears).
- **Honesty catch (self-reported, does not change verdict):** a naive hand-factorization of
  dS_rel/db was caught not matching the direct symbolic derivative; recomputed to the verified full
  form Ω(Ω(b−bG)e^{Ωb}−2e^{Ωb}+2)/(1−e^{Ωb})² (negative for b<bG ⇒ positive dS_rel/da). Strict
  monotonicity now rests on the verified closed form + numeric scan.
- **Verifier (hostile, CONFIRMED; recompute_agrees: partial → regrade CONFIRMED):** independently
  re-derived S_rel from the trace definition (explicit Fock-space sum, matching the standard Gibbs
  form to 1e-40); strictly monotone, single global minimum at a=0; the lone cold-limit inflection
  at a/H=1/√2 confirmed EXACTLY the inflection of the kinematic blueshift map (descriptive
  crossover, factor 8.19 from a~cH); bare T_DL convex everywhere. The "partial" reflects the
  verifier independently re-deriving from the trace definition rather than reusing the prober's
  closed form — both agree on every load-bearing conclusion; NO forced extremum at a~cH shown.
- **Artifacts:** `agentYY_routeEntropy.py`, `agentYY_routeEntropy.out`, `agentYY_routeEntropy.md`.

---

## CONVERGENCE (the two verified routes agree)

Both objects that could have upgraded WW from STRUCTURAL to DERIVATIONAL — the free energy F(a) and
the relative entropy S_rel(a) — are **monotone with no extremum/transition at a~cH**. Both reduce
the entire worldline a-dependence to the single Tolman blueshift factor 1/|ξ|=√(a²+H²)/H entering
through T(a); H is therefore supplied ONCE (the modular offset), and a one-time offset cannot also
place a stationary condition at a~H. The route's only intrinsic feature is the algebraic crossover
of √(a²+H²) (parked at a~H/√2, scheme-dependent in the warm regime, ~8× from a~cH=H/5.789) — the
**central trap named in the brief, explicitly identified as a descriptive crossover and NOT
mistaken for a derived extremum.** Route 2 additionally shows the algebra-level Jacobson INHERITS
(does not evade) agentQ's worldline no-go.

## QUARANTINE — HELD
q=1/4, Z, the coefficient: NEVER asserted. The probe "does a coefficient enter at the extremum?" was
vacuous in both routes because **there is no extremum** — no feature lands at a~cH, so the
coefficient question never even arose. a*/H=1/√2 was checked against Z=5.789 and is nowhere near it.

## CHAIN UPDATE (one sentence)
The type II_1 dS observer-algebra QM foundation (WW) **REPRODUCES but cannot DERIVE the a0 scale**:
the crossed-product free energy F(a) and the relative entropy S_rel(a) are both strictly monotone
with no extremum or transition at a~cH, so WW's STRUCTURAL ceiling stands — confirmed sharper from
both thermodynamic sides — and the a0 scale remains an external input (modular offset H + worldline
a), with the only remaining candidate for a derivational upgrade being the modular RESPONSE /
dissipation kernel (the MI/Langevin lane), NOT any entropy or δQ=TδS object.

## STATUS: BANKED — STRUCTURAL-CEILING-CONFIRMED (both routes VERIFIED, convergent). The QM
foundation is a FOUNDATION that reproduces the framework algebraically; it does not derive a0's
SCALE. Quarantine intact; φ never invoked; crossover-vs-extremum boundary held sharp.
