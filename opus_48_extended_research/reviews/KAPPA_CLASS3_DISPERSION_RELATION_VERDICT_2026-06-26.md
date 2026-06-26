# The κ-forcing door, CLASS 3 — modified dispersion relations / deformed mass-shells: CLOSED, gives the TEMPERATURE root and leaves κ free (2026-06-26)

*Gated action-brute-force, Class 3: can a deformed dispersion ω²=k²+m²+f(k;a₀) (rainbow / DSR / κ-Poincaré / dS
Klein-Gordon) reproduce the dS-Unruh inertia AND select the DENSITY root (a₀=cH_Λ/Z) over the TEMPERATURE root
(a₀=2cH_Λ) AND pin its outside coefficient to κ=½, from its own structure, non-circularly? This directly tests the
F1 root-selection. Scripts: /tmp/class3_dispersion_kappa.py + /tmp/class3_steelman.py (all sympy-exact, reproduce
the banked Z=4√6√π/3=5.78881, a₀_temp/a₀_dens=11.578, κ_eff=Z). Honest prior: uncertain → resolves NO.*

---

## Verdict: NO SURVIVOR. A dispersion relation gives the TEMPERATURE root and leaves κ a free amplitude.

Class 3 fails the gate on exactly the two axes the F1 clue predicts. A momentum-space deformation that reproduces
the dS-Unruh inertia lands on a₀=2cH_Λ (the **temperature** root), and the deformation's outside amplitude IS the
free κ. Both failures are sympy-exact, not asserted.

## Why — the two structural facts (sympy-verified, both reproduce banked numbers)

**(1) A dispersion supplies only the kinematic cH scale → it picks the TEMPERATURE root.**
The dS-Unruh inertia depends only on the dimensionless ratio a/cH (banked F1: W(a)=√(a²+(cH)²) is a function of
a/cH alone). A momentum-space deformation can introduce exactly ONE new scale — the crossover momentum/energy —
which is degenerate with cH (the de Sitter horizon scale). Reading the implied a₀ off the leading IR term gives
a₀ = 1/(2·lead) = **2cH_Λ** (Candidate 3A, sympy: g_eff = a²/(2cH) − …, a₀ = 2cH_Λ). The DENSITY root requires
ρ_Λ = Λc²/(8πG) — the **Einstein 8πG** normalization, a property of how the same Λ *gravitates*, NOT of a
free-particle mass-shell. The two roots are separated by exactly a₀_temp/a₀_dens(½) = 8√6√π/3 = **11.578**, a
factor built from 8π (Einstein) and 3 (Friedmann) that a momentum-shell has no access to. To reach the density
root a dispersion must be multiplied by 1/Z by hand = **inserting the answer** (G-CIRCULAR).

**(2) The deformation AMPLITUDE is the free κ — formally degenerate with the scale.**
Write the most general IR-deformed shell ω² = c²k² + (mc²/ℏ)² + A·(a₀/c)²·F(k). Every observable (inertia, group
velocity) depends on A and a₀ ONLY through the product **A·a₀²** — they are degenerate, only the combination is
observable. So "A=½" is a CHOICE of how to split the product, not a derivation. The rescaling κ→λκ gives
a₀→λa₀ strictly linearly (a₀(2κ)/a₀(κ)=2, sympy), and every dispersion consistency condition — ω²≥0, group
velocity v_g≤c, no-ghost — is amplitude-HOMOGENEOUS: an OPEN inequality / a RANGE of A, never a unique value, and
blind to whether the single scale equals 2cH or cH/Z (both give causal, positive shells). This is the **same
N-homogeneity wall** that closed ghost-freedom, restated in momentum space.

## The steelman (strongest non-homogeneous hope) — also fails, in the predicted direction

The one place a dispersion-like object is FORCED by the framework's own geometry is the **de Sitter Klein-Gordon
shell**: (□ − m² − ξR)φ=0 with R(dS₄)=12H²=4Λc² (sympy) and conformal ξ=1/6 → m_eff² = m² + 2H². This DOES force
a coefficient — but it is the **curvature/conformal** coefficient (ξ=1/6, ξR=2H²) of an INSIDE-shell mass shift
scaling as H², on the **cH/temperature** root, NOT the outside density-root ½. Its implied acceleration scale is
~Hc = cH again. The κ-Poincaré Casimir (Candidate 3D) likewise gives the sinh-expansion coefficients 1/4, 1/12,
1/24 on a length scale (inside-root), never an isolated outside ½. Rainbow/Magueijo-Smolin uses an ℏ-laden energy
scale E_dS=ℏH_Λ → cancels classically (holography barrier).

## Gate ledger (Class 3)

| Gate | Result | One-line reason (sympy) |
|---|---|---|
| **G-FORCED** | **FAIL** | deformation amplitude A is the outside κ; ω²≥0 / v_g≤c / no-ghost are A-homogeneous (open inequalities) → amplitude free; only A·a₀² observable |
| **G-FDR** | **FAIL** | ½ is the universal Taylor half (temperature root); deformation classes give 1/4, 1/12, 1/24, 1/6, 2, … — ½ not singled out for the density root, which needs Z=5.789 |
| **G-ROOT** | **FAIL** | every dispersion reproducing dS-Unruh inertia gives a₀=2cH_Λ (TEMPERATURE root); density root needs Einstein 8πG a mass-shell can't supply |
| **G-CIRCULAR** | would-be FAIL | reaching the density root from a dispersion = multiplying by 1/Z by hand = inserting the answer |
| **G-SCALEFRACTION** | **FAIL** | κ is the OUTSIDE amplitude; a dispersion fixes only the INSIDE k-dependence and the single crossover SCALE (degenerate with cH/Z), never the outside multiplier |

## Both ways (full weight each)

- **PRIZE not won (concede):** no dispersion relation forces κ=½ on the density root. It reproduces the F1 outcome
  exactly — selects the TEMPERATURE root (a₀=2cH_Λ, ~12× too big) and leaves κ a free amplitude. a₀'s value stays
  un-derived; the framework remains a provably one-parameter EFT.
- **CLOSURE is the value (credit):** Class 3 was the direct momentum-space test of the F1 root-selection, and it
  resolves it cleanly: a mass-shell deformation is **structurally a temperature-root object** (it sees only the
  kinematic cH scale, never the Einstein-8πG density), and its amplitude is **formally degenerate with the scale**
  (A·a₀² is the only observable), so positivity/causality/no-ghost — the conditions that constrained ratios
  elsewhere — are blind to the outside κ. The deepest new content: the dS Klein-Gordon shell, the one geometry-
  forced dispersion, gives the conformal coefficient 1/6 (curvature, inside-shell, cH root), categorically the
  wrong ½. Consistent with and completing the ~18-route map (ghost-freedom, unitarity, holography, CKN-dof,
  topological-η, five-way Hail-Mary, the 8-family sweep) — same scale-fraction wall, hit again.

## One line

**CLOSED, temperature-root + free-amplitude:** a deformed mass-shell reproducing the dS-Unruh inertia sees only the
kinematic cH scale → it lands on the TEMPERATURE root a₀=2cH_Λ (the Einstein-8πG density root, separated by exactly
Z=5.789, is invisible to a momentum-shell), and its deformation amplitude is formally degenerate with the scale
(only A·a₀² is observable) so ω²≥0/v_g≤c/no-ghost leave κ free; the one geometry-forced dispersion (dS
Klein-Gordon) gives the conformal ξ=1/6 curvature coefficient on the cH root, not the outside density-root ½ — so
Class 3 forces neither the root nor the coefficient, and the κ-door stays closed. Quarantine held (κ symbolic throughout).
