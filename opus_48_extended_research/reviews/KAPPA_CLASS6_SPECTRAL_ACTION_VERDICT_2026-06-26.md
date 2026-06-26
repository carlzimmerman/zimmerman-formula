# Class 6 (spectral / discrete action) κ-door: CLOSED — the heat-kernel f-moments are free cutoff data that set G and Λ_cosmo (inside the root), the one genuinely-fixed spectral number (the a₄ conformal anomaly) lands in the curvature² sector (wrong slot, same as η), and κ=½-density is reachable by NEITHER (2026-06-26)

*Gated action-brute-force, Class 6. Target: a₀=(c/2)√(Gρ_DE)=c²√(Λ/32π)=cH_Λ/Z, Z=2√(8π/3)=5.78881; √(8π/3) FORCED, lone free
number = the OUTSIDE coefficient κ=½ on the density root. Construct S=Tr f(D/Λ_cut) (Connes-Chamseddine spectral action),
Seeley-DeWitt/Gilkey heat-kernel expansion; also Benincasa-Dowker causal-set action. Honest prior: the f-moments are
notoriously free → likely FREE. Outcome: **FAILS-free-multiplier**, both ways. Scripts: /tmp/spectral_kappa.py,
/tmp/spectral_gate.py, /tmp/spectral_bothways.py (sympy, all identities verified).*

---

## Verdict: FAILS-free-multiplier. The spectral/discrete action does NOT force κ=½-density.

The Chamseddine-Connes spectral action `Tr f(D/Λ_cut) ~ Σ_k f_k Λ_cut^{d−k} a_k(D²)` produces, in d=4 (sympy-verified
identifications against the textbook readout, van Suijlekom 2015 Ch.8 / hep-th/9606001):
- **Newton constant** `G = 3π/(4 Λ_cut² f₂)` — a SCALE set by the cutoff and the moment `f₂=∫f(u)u du`.
- **Cosmological constant** `Λ_cosmo = 6 Λ_cut² f₄/f₂` — a SCALE set by the cutoff and the moment RATIO `f₄/f₂`.

Build the framework's a₀ from these: `a₀ = (1/2)c√(Gρ_DE) = (√3/4) c² Λ_cut √(f₄/f₂)/√π`. Sympy confirms this is
**identically equal** to `c²√(Λ_cosmo/32π)` for ALL `f₄/f₂` (difference = 0). That identity is the tell: the density route
is a **tautology** once you write the outside ½ — the spectral action imposes **no constraint that selects ½**, and any
`f₄/f₂` just rescales Λ_cosmo. The action produces what is INSIDE the root (G, ρ_DE) plus the overall cutoff scale; it
produces **nothing in front of the root**. κ=½ is the Komar/free-fall multiplier we put there by hand.

## The gate (each criterion, sympy-checked)

- **(G-SCALEFRACTION) — FAILS.** κ sits OUTSIDE the dimensionful root √(Gρ_DE). The moments f₀,f₂,f₄ set only what is
  INSIDE (G, Λ_cosmo) — they cannot reach the outside multiplier. This is the exact slot the ~18 prior routes proved
  unreachable.
- **(G-ROOT) — does not force the choice.** The spectral action produces (G, Λ_cosmo) = a vacuum-energy/DENSITY, with NO
  dS-Unruh TEMPERATURE object anywhere (it is a Euclidean heat-kernel trace). So it is silent about the
  density-vs-temperature root choice; adopting a₀=(c/2)√(Gρ) is the density route ASSUMED, not selected by structure.
- **(G-FORCED) — FREE INPUT.** The only numbers are f₀,f₂,f₄ (moments of a free cutoff profile f) and Λ_cut, none fixed by
  the spectral-action axioms; Chamseddine-Connes themselves fix f₂,f₄ by **matching G_Newton and Λ_cosmo to observation**.
  a₀'s coefficient is `√(3 f₄/(4π f₂))/2` — tuned via f₄/f₂ to data. κ=½ is the inserted Komar ½, the ratio is fit. Not an
  output.
- **(G-FDR) — continuum.** f₄/f₂ ranges over (0,∞) → the a₀ coefficient is a continuum; ½ is not a distinguished member of
  the family, it is tacked on outside. Look-elsewhere = the whole real line.
- **(G-CIRCULAR) — circular/inserted.** Getting a₀=9.36e-11 out needs fitting f₄/f₂ to the observed Λ AND multiplying by the
  hand-chosen ½. Both inserted; nothing in Tr f(D/Λ) forces either.

## Both ways — is there ANY structural fix of the f-moments? (steelman, full weight)

- **Steelman 1 — "spectral-action universality / Tauberian":** only the zeta-function POLES (the a_k heat-kernel
  coefficients) are universal; the MOMENTS f_{2k} are the VALUES of f at those poles and are explicitly free cutoff data
  (van Suijlekom). The standard almost-commutative SM construction FITS f₀,f₂,f₄ to {G_Newton, Λ_cosmo, gauge/Higgs
  couplings}. No universality fixes them.
- **Steelman 2 — "zeta-normalization / sharp cutoff so the moments are pure spectral numbers":** the one genuinely-FIXED
  spectral number on S⁴ is the **a₄ conformal-anomaly coefficient** (the 1/360-type Gilkey numbers) — but it is
  DIMENSIONLESS and multiplies **Weyl²/Gauss-Bonnet** (the curvature² sector), the **same WRONG SLOT** the topological-η
  door already closed. The moments that set G and Λ_cosmo (a₂~f₂, a₀~f₄) carry the FREE cutoff data. So the fixed spectral
  number cannot reach the outside Komar ½, and the free moments don't force it.

## Causal-set / lattice variant — same outcome

Benincasa-Dowker causal-set action: its normalization (the 4/√6 prefactor, the layer coefficients −1,9,−16,8) is FIXED by
demanding the continuum limit reproduce the R-term — i.e. fixed by MATCHING Einstein-Hilbert, not by an independent principle
— and the discreteness/mesoscale ℓ is a FREE parameter. It pins G_eff and the R-normalization (inside the root); a₀'s outside
Komar ½ is untouched. Same as Connes: FREE.

## Why this is consistent with the closed door (the deep wall, restated)

κ=½ is the bare classical ħ-free multiplier OUTSIDE the dimensionful density root; the √(8π) that fixes Z lives INSIDE
ρ_DE=Λc²/8πG. A heat-kernel expansion is, by construction, an expansion of an operator whose coefficients (the f-moments)
normalize the terms INSIDE the action (the G, Λ_cosmo, curvature² pieces). It has the same structural blindness as
ghost-freedom (an overall normalization), unitarity (signs/ratios), holography (the scale cH), and the topological η (an
integer anomaly in the wrong slot): none can reach an outside dimensionful Komar fraction. The spectral action is now the
**sixth** structurally-distinct barrier confirming κ is unforceable.

## What this closes / both ways

- **PRIZE not won (concede, full weight):** there is no non-circular spectral or discrete-action derivation of κ=½. a₀'s
  value stays un-derived; the framework remains a **provably one-parameter** EFT, not zero-parameter.
- **CLOSURE is the value (credit, full weight):** Class 6 was a named candidate class (the only one with an honest chance of
  fixing a normalization via heat-kernel moments). It closes for a sharp, reproduced reason: the f-moments are free cutoff
  data that set the INSIDE scales (G, Λ_cosmo), and the one genuinely-fixed spectral number (the a₄ conformal anomaly) is a
  dimensionless curvature² coefficient — the wrong slot — exactly as the η-door found. Quarantine held (κ kept symbolic;
  the value ½ and the 8π density route appear only in the post-hoc locating map; the honest FREE default emerged).

## What Carl CAN / MUST NOT say

- **CAN:** the spectral/discrete action (Connes-Chamseddine + Benincasa-Dowker causal sets) does NOT force κ=½; its
  heat-kernel f-moments are free cutoff integrals fixed by matching G_Newton and Λ_cosmo to observation, and the one fixed
  spectral number (the a₄ conformal anomaly) lands in the curvature² sector — the same wrong slot as the topological η.
  This is the sixth structurally-distinct barrier; κ=½ stays the framework's lone, exactly-characterized free input.
- **MUST NOT:** "the spectral action derives a₀ / fixes κ" (FREE — the moments are tuned to data); "the conformal-anomaly
  number gives ½" (it is dimensionless and multiplies curvature², not √(Gρ_DE)); any claim that Tr f(D/Λ) selects the
  density route over the temperature route (it has no temperature object — silent, not selecting). Quarantine: a₀/Z/κ never
  asserted derived.

## One line

**FAILS-free-multiplier:** the Connes-Chamseddine spectral action's heat-kernel moments f₀,f₂,f₄ are free cutoff data that
set only the INSIDE scales G=3π/(4Λ_cut²f₂) and Λ_cosmo=6Λ_cut²f₄/f₂ (sympy-verified, and a₀=(c/2)√(Gρ_DE) is then
identically c²√(Λ_cosmo/32π) for ALL f₄/f₂ — a tautology, no constraint selecting ½), while the one genuinely-fixed spectral
number (the a₄ conformal anomaly) is a dimensionless curvature² coefficient in the SAME wrong slot the η-door closed, and the
causal-set normalization is fixed by matching EH not by structure — so κ=½, the classical Komar multiplier OUTSIDE the
dimensionful density root, is reachable by neither, making the spectral/discrete action the sixth structurally-distinct
barrier and leaving κ the framework's lone free input. Quarantine held, both ways, no manufactured forcing.
