# M09 — The finite-past initial-value problem
COST: M | KILLS FAST: YES | script: `mi_finite_past_ivp_2026.py`

## The task
At ω_c = a₀/c the memory time is **101.5 Gyr = 7.4× the age of the universe**, so only **12.7%** of the
kernel weight lies inside any real worldline's past, and the frozen homogeneous mode retains ~87% of its
initial value over cosmic time. Every steady-state transform in the corpus assumes an infinite past.
Nobody has solved it as an actual initial-value problem.

## Do
1. Integrate the localized system on a finite worldline: ẍ = −∇Φ + (memory terms) together with
   χ̇ᵢ + ωᵢχᵢ = ωᵢa, with χᵢ(−T) = 0 and T = 13.797 Gyr. Use a two-pole Prony kernel (the localization is
   exact — see `mi_auxfield_exact_circular_2026.py`).
2. Compare the resulting rotation curve to the steady-state prediction.
3. Test initial-data sensitivity: vary χᵢ(−T) and report how much the answer moves.

## Settles if / refuted if
KILLS the steady-state reading: if the answer is initial-data-dominated, every C and S number at
ω_c = a₀/c is inapplicable — the estimate is 1/|C| ≥ 3.4e3 with asymptote ω_c/Ω, i.e. **one** power of c/v,
not two.
CONFIRMS: insensitive to initial data ⇒ the steady-state transforms are legitimate.

## Known walls
The localization itself is verified exact (residual identically zero). What is unverified is the
steady-state *premise*, not the algebra. ω_c is a **free fifth constant** — committed window 1.78–2.21e-14,
where the suppression vanishes entirely.
