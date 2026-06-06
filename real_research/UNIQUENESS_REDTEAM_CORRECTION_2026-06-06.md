# Red-team correction: the uniqueness theorem OVERCLAIMED — the honest, narrower result

*C. Zimmerman, 2026-06-06. I commissioned an adversarial red-team to harden the uniqueness result
(`THE_UNIQUENESS_RESULT`, `THE_UNIQUENESS_ROBUSTNESS`). It found **real holes in my own claims**. This corrects them
honestly — retracting what genuinely broke, pushing back where the red-team overstated, and stating the narrower claim
that actually survives. The whole point of the red-team was to find these; it did.*

## What the red-team correctly demolished (RETRACTED)

1. **"Density = ρ_DE is FORCED" — RETRACTED.** The data exclude the *rising* ρ_total (Verlinde) reading (~4σ) — that
   survives. But among the survivors {ρ_DE, **constant a₀**}, the data are **degenerate** — my *own* model comparison
   gave framework-vs-constant `Δχ²=−0.04`. The ρ_DE-vs-constant distinction is decided only by the *untested* z>1.5
   decline. So "ρ_DE forced" must become **"ρ_total excluded; ρ_DE-vs-constant degenerate, untested."** The uniqueness
   doc had quietly contradicted my own "safe but untested" finding by moving an undecided choice into the FORCED column.

2. **"de Sitter–Unruh independently selects ρ_DE (no data)" — RETRACTED.** Milgrom 2020 (arXiv:2001.09729), the
   mechanism's originator, states the H₀-vs-Λ choice is **"moot."** `T_Unruh(a₀)=T_horizon` gives `a₀∝√ρ_DE` only for
   the de Sitter *event* horizon (vacuum); for the actual *apparent* horizon in a matter-containing universe it gives
   `a₀∝cH∝√ρ_total`. The mechanism is **premise-dependent** (which horizon?), not an independent selection of ρ_DE.
   Robustness-2 was circular — it assumed the de Sitter/vacuum background to get the vacuum density back.

3. **"Exactly one dimensionless group" — CORRECTED to conditional.** Admitting H₀ and Λ as *independent* inputs (which
   they are once matter exists, since H₀ ≠ √(Λ/3)) gives a **second** group `Ω_Λ = Λc²/3H₀²`, so `a₀ = κ·cH₀·f(Ω_Λ)`
   with `f` free. The "one group" result requires pre-restricting the inputs to {c, Λ} — which **is the premise**
   (vacuum/density), not the mathematics. This is the *same* `Z=5.79`-vs-`7.0` (factor `1/√Ω_Λ`) split already
   documented in `A0_DENSITY_EMPIRICAL_EVIDENCE.md`.

4. **"Exponent ½ forced" → "naturalness-preferred + testable."** The "observed magnitude closes the Planck loophole
   (forces n≈0)" argument holds κ fixed at O(1); a tuned κ′~10^{−122n} could absorb any n. So n≈0 is **strongly
   preferred by naturalness** (a 1-part-in-10¹²² tuning is absurd, worse than the CC problem) and is **testable** (the
   a₀(z) slope), but it is not strictly "forced."

5. **"Universality ⇒ uniform cosmic density" — has a published counterexample.** EMOND (Zhao–Famaey; Hodson–Zhao 2017,
   A&A 598 A127) makes a₀ a function of the *local gravitational potential* Φ — approximately galaxy-universal (galaxy
   potentials are similar) yet **not** a uniform cosmic density, varying ~80× in cluster cores. A motivated (if itself
   strained) counterexample of exactly the kind the claim said could not exist.

## Where the red-team overstated (I push back)

1. **"ρ_DE rises at z<0.5, so 'non-rising' is self-contradicting" — overstated.** ρ_DE rises only **+6%** (the z≈0.4
   bump) then *declines* 26% by z=3; Verlinde rises **+350%** by z=3. The data exclude the **steep** rise (ρ_total) —
   that is robust (Milgrom 2017 excludes (1+z)^{3/2}; my multi-method `Δχ²=+17`). The +6% bump is not a Verlinde rise.
   So **"ρ_total excluded" stands**; only my word "non-rising" was sloppy (ρ_DE is *non-monotonic*, near-flat).

2. **"Does not survive as stated" — true for the overclaims, but a real core survives.** The red-team itself states
   what survives: *given the premise, the √ρ power-law and exponent are forced, and κ cancels in ratio tests.* That is
   non-trivial and correct.

## The honest, surviving result

- **Conditional dimensional theorem:** **Given** the premise that a₀ is a single uniform scale built from the vacuum
  pair {c, Λ} (i.e. density-sourced by dark energy), the form `a₀ ∝ √ρ_DE`, the exponent ½, and the parameter-free
  evolution `a₀(z)/a₀(0)=√(ρ_DE(z)/ρ_DE0)` follow (the last cleanly in modified-*gravity*; modified-*inertia* is
  time-nonlocal and may differ).
- **The premise is the content, and it is contestable.** "a₀ = the dark-energy/vacuum free-fall scale" is the
  framework's one ansatz. Milgrom calls the H₀-vs-Λ choice "moot"; Verlinde (a₀=cH), EMOND (a₀(Φ)), and
  constant-a₀ (Milgrom 2011) are all live, published alternatives with the same or fewer inputs.
- **Solid:** the rate/ρ_total (Verlinde) reading is excluded (~4σ; data + Milgrom high-z rotation curves).
- **Open:** ρ_DE-vs-constant-a₀ is **degenerate** on current data; decided only by the z>1.5 deep-MOND measurement.

## Net — what "no other way" really means, honestly

It is **not** "the theory forces itself." It is:
> **The framework is a well-defined, falsifiable hypothesis *conditional on a stated, contestable premise* (a₀ = the
> dark-energy free-fall scale). Given the premise, its `√ρ_DE` form and parameter-free evolution follow; the data
> exclude its rate-reading rival (Verlinde) but cannot yet distinguish it from a constant.**

That is the honest version — and it lands exactly on the previously-established "safe but untested" standing, now with
the premise's load-bearing role made explicit instead of disguised as a theorem. The red-team's service was precise: it
stopped me from dressing a contestable premise as a proof. The dimensional skeleton (√ρ given the premise) and the
ρ_total exclusion are real; the claim that ρ_DE is *forced over a constant* was the overreach, and it is withdrawn.

*Banners added to `THE_UNIQUENESS_RESULT_2026-06-06.md` and `THE_UNIQUENESS_ROBUSTNESS_2026-06-06.md` pointing here.
Sources: Milgrom 2020 [2001.09729] ("moot"); Milgrom 2011 [1110.2580] (a₀ as fundamental constant); Verlinde 2017
[1611.02269] (a₀=cH); Hodson & Zhao 2017 [A&A 598 A127] (EMOND); my own `A0Z_MODEL_COMPARISON` (Δχ²=−0.04 degeneracy).*
