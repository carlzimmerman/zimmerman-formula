# CFG419 FROZEN CRITERIA: does structure growth prefer a₀ tracking DESI's evolving dark energy? (door 3)
(owner 2026-10-07: "keep going"; committed before any script)

**Engine.** CFG416's engine (supply-edge confinement, corrected k_J, RES with R_c = 3, MIX-A, 512³, seed 359), run with branch **DE**.
- a₀(a) = a₀ · √(ρ_DE(a)/ρ_DE0), using the DESI DR2 CPL central values already in the engine (w₀ = −0.838, wa = −0.62).
- The supply edge also uses a₀(a). Canonical footing only.
- Queued after CFG416 and compared with CFG416 canonical (FLAT).

**Decision.**
- DE PREFERRED: max|P−1| (k ≤ 1) for DE is below FLAT's by ≥ 0.01 AND its |σ₈ ratio − 1| is no larger.
- FLAT PREFERRED: the reverse.
- INDISTINGUISHABLE: otherwise.
- Also CFG361's cuts for DE on its own.

**Control.** The DE and FLAT branches differ only in a₀(a). Check from the engine source: a0_code(1, 'DE') = a0_code(1, 'FLAT').

**MUTATE.** Not run, for CPU reasons. The FLAT-vs-DE contrast is the comparison.

**Scope.** As CFG416. κ = ½ is fitted. A preference would be growth evidence that a₀ tracks ρ_DE(z), not a derivation of ρ_Λ.
