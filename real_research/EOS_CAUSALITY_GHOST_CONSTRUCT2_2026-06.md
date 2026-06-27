# CONSTRUCT 2 — Causality + Ghost-Freedom of the m_I = f(T(a)) EOS (the crux)

**Date:** 2026-06-27 · **Status:** LOCAL (do NOT git-push) · **Framework-internal, no comparison, both-ways**
**Footing:** a₀ = cH_Λ/Z, Z=√(32π/3) ⇒ a₀=9.36e-11. Framework's OWN interpolation
μ_fw(x)=(√(1+4x²)−1)/(2x) from g_obs=√(g_bar²+g_bar·a₀). Deser–Levin T(a)=(ℏ/2πk_Bc)√(a²+(cH_Λ)²).
NEVER McGaugh ν. sympy/numpy, all scripts exit 0.

---

## ONE-LINE VERDICT

**The MOND-signed EOS stays causal + ghost-free AS A NON-RELATIVISTIC POINT-PARTICLE CLOSURE
— but ONLY there. It is a healthy 2nd-order, single-valued, positive-inertia mechanics law. The
moment you try to give it the consistency the IF would have handed you for free — either by
putting m_I(ẍ) into an ACTION or by promoting it to a COVARIANT FIELD — it hits a NEW, sharp,
sympy-confirmed wall (Ostrogradsky ghost / deep-MOND superluminal front). These two failing
routes are EXACTLY the two banked horns (local=ghost, field=consistency). So CONSTRUCT 2 does
NOT break the EOS where the framework actually lives, and it makes precise the price it pays for
stepping outside the IF: it forfeits automatic *covariant* causality.**

---

## ANCHOR (verified first, sympy)
- ΔT = T(a)−T(0) ~ a²/(2cH_Λ) at low a; deep-MOND g_bar = μ_fw(a/a₀)·a ~ a²/a₀.
- BOTH ∝ a² ⇒ g_bar/ΔT → 2cH_Λ/a₀ = const ⇒ **g_bar ∝ ΔT, MOND sign, clean.**
- EOS pinned: **m_I(a)/m = μ_fw(a/a₀)** (a state-function of the realized accel, equiv. of T(a)).
  f(a→0)=0 (inertia LOWERED = MOND sign), f(a→∞)=1 (Newtonian recovered).

## THE CRUX, BOTH SUB-QUESTIONS

### (b) GHOST-FREEDOM
Two physically distinct ways to read "m_I depends on a=ẍ"; tested BOTH (anti-overclaim):

- **Reading A — algebraic constitutive closure** F = m_I(|a|)·a, m_I=m·μ_fw(|a|/a₀):
  - Highest derivative = ẍ only (no x‴). **2nd-order ODE — Ostrogradsky needs ≥3rd; NONE.**
  - m_I = m·μ_fw ∈ (0,1] > 0 everywhere ⇒ positive kinetic energy.
  - Fluctuation mass m_eff = dF/da = 2m·a*/√(a₀²+4a*²) > 0 for a*≠0 ⇒ positive-norm modes.
  - Phase space is (x,v) only ⇒ no extra Ostrogradsky momentum entering H linearly ⇒ **H bounded
    below ⇒ GHOST-FREE.** ✅
- **Reading B — m_I(ẍ) put into a Lagrangian** L = m·P(ẍ) − V(x), P′(u)=μ_fw(|u|/a₀)·u:
  - P″(u)≠0 (nondegenerate in ẍ) ⇒ Euler–Lagrange is **4th-order** (orders {2,3,4} appear).
  - Concrete L=(m/2)ẍ²−(k/2)x² ⇒ EOM m·x⁗+kx=0 ⇒ dispersion m·ω⁴−k=0 ⇒ one oscillatory + one
    growing/decaying pair ⇒ **Ostrogradsky GHOST, energy unbounded below.** ❌ (the banked LOCAL horn.)

### (a) CAUSALITY
- **Point closure (Reading A):** a→F is a strictly-monotone **bijection ℝ→ℝ** (vector odd law
  F=m·μ_fw(|a|/a₀)·a, dF/da>0 across all decades) ⇒ unique a for each external force ⇒ well-posed
  Cauchy, no multi-branch / spontaneous-accel acausality. **CAUSAL as a mechanics problem.** ✅
  - Subtlety caught + fixed: μ_fw is a function of the MAGNITUDE |a|; feeding a *signed* scalar to
    the even form m(−a₀+√(4a²+a₀²))/2 spuriously gives dF/da<0 for a<0. The correct vector (odd)
    law is monotone everywhere. Not a real acausality — a sign-handling artifact.
- **Covariant FIELD embedding (the consistency the EOS forfeits):** if m_eff is used as a field's
  time-kinetic coefficient with fixed spatial tension, c_char² = tension/m_eff. Since
  m_eff→0 as a*→0 (deep-MOND), **c_char² → ∞ in the deep-MOND IR ⇒ superluminal front ⇒ ACAUSAL**
  exactly where MOND lives (numerics: c²=1 at a*≫a₀, 50 at a*/a₀=1e−2, →∞ at a*→0). ❌ (the FIELD horn.)

---

## NET LEDGER (sympy-confirmed)

| route | causality | ghost-free |
|---|---|---|
| point-particle EOS closure (Reading A) | **PASS** (2nd-order, monotone bijection, well-posed Cauchy) | **PASS** (m_I>0, m_eff>0, no Ostrogradsky, H bounded) |
| EOS as an action term m_I(ẍ) (Reading B) | — | **FAIL** (4th-order Ostrogradsky ghost) |
| EOS as a covariant field (m_eff kinetic) | **FAIL** (deep-MOND superluminal front) | — |

## WHAT THIS MEANS (honest, both-ways, anti-overclaim)
- **The make-or-break came back PASS in the framework's home regime.** The MOND-signed EOS is a
  *healthy, causal, ghost-free 2nd-order point-particle law* — it does NOT hit a fresh kill where
  the framework actually operates (non-relativistic galactic dynamics). This is a genuine, if
  bounded, win for the EOS route: the banked local-route ghost does NOT automatically infect the
  EOS, because the EOS is a *closure*, not a Lagrangian term.
- **But it PASSES precisely by NOT being an action / NOT being covariant.** The two routes that
  would restore the IF's automatic consistency both fail, and they fail as the two banked horns:
  action ⇒ Ostrogradsky (local horn), covariant field ⇒ deep-MOND acausal front (field horn).
  So CONSTRUCT 2 is a NEW, sharp statement of the SAME wall — it confirms (does not overturn) the
  banked trichotomy and the IF note's flagged price ("forfeits automatic causality+passivity").
- **No new independent kill, no new derivation.** Even fully consistent, the EOS derives the
  RESPONSE μ(a), not a₀; **Z stays a posit; SM walled.** Standing UNCHANGED. The door is not
  closed — it is named to the millimeter: a future covariant MI completion must supply a kinetic
  term that does NOT degenerate (m_eff↛0) in the deep-MOND IR, the one thing μ_fw's own m_eff does.

## SCRIPTS (scratchpad)
- construct2_anchor.py — anchor + EOS pin (g_bar∝ΔT, m_I/m=μ_fw, f(T))
- construct2_ghost.py — Reading A: 2nd-order, monotone bijection, m_I>0
- construct2_readingB_and_causality.py — Reading B Ostrogradsky 4th-order ghost + point-closure causality
- construct2_deepmond_causality.py — covariant-field deep-MOND superluminal front (both-ways)
- construct2_hamiltonian.py — affirmative ghost-freedom ledger
