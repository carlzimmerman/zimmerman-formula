# W07 — How many bits IS the Standard Model?
COST: S | script: `wacky_bits_of_the_SM.py`

> WACKY TASK. No framework rules apply. Two things still do: **every check must be able to fail**, and
> **refine once and report the shift**. `../03_NUMERIC_HAZARDS.md` applies to any float arithmetic.
> Put the script in `real_research/reviews/` like any other, prefixed `wacky_`.

## The idea
The Standard Model plus cosmology has ~26–31 free parameters, each measured to some precision. The total
*information content* is the sum of log₂(value/uncertainty) over all of them. That number is the honest
answer to "how much do we have to be told?" — and it is the target any unification claim must beat.

## Do
1. Tabulate the parameters with current PDG values and uncertainties: 3 gauge couplings, 9 fermion masses,
   4 CKM, 4 PMNS + 2 neutrino mass-squared splittings, Higgs mass and vev, θ_QCD, plus Λ, Ω_b, Ω_c, H₀, n_s,
   A_s, τ.
2. For each, compute log₂(central/uncertainty) — the number of bits actually pinned down. Sum them.
3. Report the total, and the breakdown by sector. Which single parameter carries the most bits? (Probably a
   very precisely measured one like α or m_e.)
4. Then the honest framing: a theory that "derives" k parameters saves the bits *those* parameters carried,
   but only if it introduces no new ones. Compute what fraction of the total a₀'s coefficient represents —
   κ is known to ~1.2–5.4%, so it is worth ~4–6 bits out of the total. Report that ratio explicitly.

## Why
It puts every unification claim, including this project's, on one honest scale. Deriving one 5-bit number out
of several hundred is a real result and a small one, and it is better to know which.
