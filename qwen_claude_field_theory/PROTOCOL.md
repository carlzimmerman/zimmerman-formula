# PROTOCOL — read this, then do ONE idea, then STOP

You are a local worker running one idea per session. **Fresh context every time.** The
ledger is your only memory. Do not try to hold the project in your head.

## The framework, in the six lines you actually need

1. `a0 = kappa * c * sqrt(G * rho_Lambda) = 9.3619e-11 m/s^2` (canonical) or `1.1279e-10`
   (alt footing). **Report both** for any dimensional number. `kappa = 1/2` is **FITTED,
   never derived** (measured 0.529 +/- 0.034).
2. `y = g_bar / a0`. The anomalous acceleration is `u = (nu(y) - 1) * g_bar`; write
   `U(y) = u/a0`.
3. The **a0-line** (Carl's signature relation) is `g_obs^2 = g_bar^2 + a0*g_bar`, i.e.
   `nu = sqrt(1 + 1/y)`, i.e. `U = sqrt(y^2+y) - y`, saturating at `U -> 1/2`.
4. The **legal class** (ghost-free in AeST) is any `U(y)` strictly increasing with
   `U -> sqrt(y)` as `y -> 0`. Closed-form family: `J_Y = v/(1 - v/s)`, `v = sqrt(Y)/a0`,
   which saturates at `U -> s`. `s = 1/2` is the a0-line. `s = 1` is the standard "simple"
   kernel.
5. **Route A**, `nu = 1/(1 - exp(-sqrt y))`, is **ILLEGAL** in AeST: its `U` peaks at
   0.6476 at `y = 2.540` then falls, so no single-valued free function reproduces it.
6. The promotion `a0^2(Q) = kappa^2 G (-K(Q))` makes **a0 a field, not a constant**:
   `a0(nu)/a0(0) = [(1+nu0^2)/(1+nu^2)]^(1/4)` with `nu = nu0 * rho/rho_0`, and
   `nu0 <= 2.36e-6`.

**THE OPEN PROBLEM most of these ideas attack:** ephemerides need the saturation
`s <= 2.4e-3`; the RAR needs `s >= 0.558`. **Incompatible by 233x.**

## Rules

- **R1. ONE idea per session.** Get it from `next_idea.py`. Do it. Ledger it. Stop.
- **R2. Write a script.** Put it in `runs/` named after the idea id, e.g.
  `runs/i017_something.py`. It must print numbered `[ok]`/`[FAIL]` checks and exit 0 only
  if all pass. No script, no claim.
- **R3. Honest grading, both ways.** A result that hurts the framework is as valuable as
  one that helps. Never soften an adverse number; never inflate a favourable one. If you
  find the framework wins, say so plainly too.
- **R4. TIME BOX: 20 minutes.** If the idea is not producing a number by then, write what
  you have, grade it `NOT COMPUTED`, ledger it, and STOP. **A stalled session is the only
  real failure mode here.** Partial results with a clear statement of what blocked you are
  worth more than nothing.
- **R5. Never invent** an equation number, a citation, a DOI, or a data value. If you did
  not read it, mark it `UNVERIFIED`.
- **R6. Do not modify** anything in `prep_2026/gaia_dr4_prep/` (frozen pre-registration),
  any `*_HASH.txt`, or any file outside `qwen_claude_field_theory/`. Read them freely.
- **R7. Write a FULL RESULT FILE** to `results/I###_<shortname>.md`, using
  `RESULT_TEMPLATE.md`. This is the thing Carl reviews later, so it must stand alone: the
  math written out, the numbers in a table, why the verdict fired, and — mandatory — a
  section arguing against your own conclusion. A ledger row without a result file does not
  count as done.
- **R8. Append exactly one LEDGER.md row** at the end, then end the session.

## Ledger row format

```
| I017 | one-line what you did | the decisive number | PASS / KILL / PARTIAL / NOT COMPUTED |
```

`PASS` = the hypothesis survived its own pre-registered test.
`KILL` = it failed; say which condition.
`PARTIAL` = you got a number but it does not decide.
`NOT COMPUTED` = you ran out of time or hit a wall; say which.

## Data you can use (real paths, verified to exist)

| what | path |
|---|---|
| SPARC master table (175 galaxies) | `real_research/data/SPARC_Lelli2016c.mrt` |
| SPARC secondary table | `real_research/data/SPARC_table.txt` |
| RAR points, 3389, log10 g_bar / log10 g_obs (m/s^2) | `ai_slop/website/public/data/rar_real_sparc.json` |
| same, in a0 units | `qwen_38_experiment/data/rar_sparc_a0units.json` |
| committed RAR fitter (gives 0.108 dex) | `real_research/rar_framework_a0_mlfit.py` |
| a0(z) tabulated | `real_research/data/a0_of_z.csv` |
| 2MRS galaxy catalogue (environments) | `real_research/data/2mrs_catalog.csv` |
| KiDS weak-lensing RAR | `prep_2026/kids_rar/kids_rar_lambda.py` |
| the closed-theory construction | `nbody_2026/stage75_the_closed_theory_2026.py` |
| the nu0 pin, with CLASS | `nbody_2026/stage76_nu0_recombination_pin_2026.py` |
| local-a0 / ephemeris | `real_research/reviews/a0_local_ephemeris_2026.py` |
| legality + the legal family | `real_research/reviews/typeII_*_2026.py` |

CLASS is installed (`from classy import Class`). numpy, scipy, sympy are available.

**If a path in an idea does not exist, do not hunt for it.** Grade `NOT COMPUTED`, say the
path was missing, and stop. That is a useful result — it tells us the idea needs data we do
not have.
