# Superfluid route — standing, 2026-08-18

Stopped early for credit budget. What is banked, what is owed.

## BANKED (committed, 19/19, `sf01_ansatz_closure_2026.py`)

1. **The a₀-line's AQUAL free function, in closed form:**
   f(z) = ½√z·√(1+4z) + ¼·asinh(2√z) − √z,  z = (g_obs/a₀)².
   Deep-MOND limit **exactly (2/3)z^(3/2)** — the same 3/2 power and 2/3 coefficient AeST's own
   MOND term carries, with **no free constant in the chain**. Recovered, not fitted.
2. **Carl's DBI kernel supplies exponents 2,4,6,… at its minimum (every odd coefficient verified
   zero) and 1/2 at the wall. The MOND job needs 3/2 — available at NEITHER place.**
3. **But the two jobs never share a point of the domain**: background at X = Q−Q₀ > 0,
   quasi-static at X = −𝒴/2m ≤ 0. A two-sided function is admissible. **GRADE: OPEN.**
4. **m is not a new free parameter** — it is fixed by a₀, which is already fixed.

## THE ONE NEW RESULT FROM THE STOPPED RUN (prior-art line, MIXED verdict)

The repo's own verbatim AeST transcription (`real_research/bridge1_aest_equations.md`) records
that **in the quasi-static limit 𝒬 = (1−Ψ)𝒬₀**. Therefore under the ansatz

    X = (𝒬 − 𝒬₀) − 𝒴/(2m) = −Ψ·𝒬₀ − 𝒴/(2m)

— **X contains the Newtonian potential Ψ directly.** That is exactly what R1 demands (the free
function must eat the total potential, not the scalar's own gradient), and it arrives from a
relation already in the corpus rather than from a new assumption. **This has never been
computed.** It is the single most promising item on the route and the obvious next step.

Also confirmed by that line: the superfluid has been graded in this corpus **only as a rival
theory** (Berezhiani–Khoury as an object to beat), **never as Carl's own condensate**. The
F(X) ansatz inside AeST is genuinely new here.

## OWED — and these are the deciding items, none of them run

| # | item | why it decides |
|---|---|---|
| O1 | **The vector sector under the X-ansatz** | whether R2 is actually evaded. sf01 settles only that the SCALAR jobs can coexist. C_V untouched. |
| O2 | **The phonon–baryon coupling vs γ_PPN = 1** | AeST's matter couples to g alone; a direct coupling risks the 0.601σ lensing result. Is a universal (trace/disformal) coupling available? |
| O3 | **Is the two-sided F one natural function or a splice?** | a splice is not a theory |
| O4 | **The dust problem (2d)** | does phonon pressure evade the ρ+3p / ρ+p obstruction, or is it another equation of state the theorem already forbids? |
| O5 | **Clusters** | BK's own known weak front |

**Cheapest next step, and it is O1+the X = −Ψ𝒬₀ result together:** one script, mostly sympy,
asking whether X's Ψ-dependence gives R1 for free AND what it does to C_V. That is the whole
verdict in one file.

## STANDING CONSTRAINT (Carl, 2026-08-18, emphatic)

**No dark-matter PARTICLE, in any framing.** The dark sector here is a **field** — a
shift-symmetric condensate with a conserved charge. Phonons are excitations of that field, not
of a gas of particles. Never present this route as Khoury-style particle dark matter.
Equally: **never claim the dark sector is absent** — Ω_dm is full, it is what the CMB pass and
w = −1 both rest on, and saying otherwise re-opens the 2026-06 retraction.
