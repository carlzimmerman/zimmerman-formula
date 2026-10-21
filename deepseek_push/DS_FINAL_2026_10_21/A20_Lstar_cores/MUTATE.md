# A20 — mutation record

`a20_checks.py` takes `--mutate=exp|k|dist`. Each mutation injects one plausible error into the
**analysis** code (never into the assertion), so a check that does not move is a check without teeth.
Captured outputs are in `a20_MUTATE_<name>.out` / `a20_results_MUTATE_<name>.json`.

Baseline: `A20 COMPLETE: 18/18 checks PASS.` (exit 0).

---

## 1. `--mutate=exp` — drop the `(3-n)` in the cusp mass

The cusp enclosed mass is `M(<r) = 4 pi rho r^3/(3-n)`; the mutation uses `4 pi rho r^3/3`, i.e. treats
every cusp as if it were isothermal (`n = 2`). This is *the* classic slip in this algebra, because the
result is only wrong for `n != 2`.

    17/18 checks PASS, exit 1
    K1   FAIL residual n=1,2 = ['L**2/(2*r**2)', '2*L**2/r**2'] exactly 0

The residual is `(3-n)/2 - 1`: `-1/2` for `n = 1` and `+1` for `n = 2`. K1 therefore tests the *whole*
`1 <= n <= 2` range, not just one point — a one-`n` check would have let this through.

---

## 2. `--mutate=k` — set `k = 1` in candidate 2 (`L* = V_f^2/(k a0)`)

`k = 1` is the degenerate reading `L* = r_M`, the MOND radius. It is the natural "simplification" and it
is what the record's own `sigma_c <= V_f/3` premise would give if the 3 were dropped.

    16/18 checks PASS, exit 1
    K15  FAIL cand2 outside window: 82.86%       30.29% +- 0.5%   below 24 pc: 0.00%, above 1 kpc: 82.86%
    K16  FAIL cand1 24pc 1.012 / 1kpc 6.530 ; cand2 20.073        1.012 / 6.530 / 6.691

Both C3 and C4 move, and in the direction that matters: `k` is not a knob that can be turned to rescue
candidate 2 — every `k` leaves the 2.637 dex spread (K14, which is scale-invariant) and every `k <= 9`
pushes more of the sample above 1 kpc. That is the structural statement, and K14 is deliberately written
on the *spread*, which no rescaling of candidate 2 can fix.

---

## 3. `--mutate=dist` — read the SPARC distance as kpc instead of Mpc

The `# Distance = ... Mpc` header is read as kpc, so every beam is `1e3` too large.

    17/18 checks PASS, exit 1
    K8   FAIL f(r_rel<24)=0.0000 <100=0.0000 <300=0.0000 <1k=0.0000   0 / 0 / 0.0114 / 0.2229

K8 fails on the two *non-zero* entries (`1.14 %` and `22.29 %` collapse to 0), which is exactly why the
check asserts those two numbers and not only the zeros. K9 (the 80 pc floor) does **not** move, and that is
correct: the floor is set by the tabulated `r_first = 80 pc`, which is distance-independent — the null for
a 24 pc core does not rest on the beam assumption at all.

---

## What the mutations establish

| mutation | check that catches it | what would have been wrong |
|---|---|---|
| `(3-n) -> 3` | K1 (both `n = 1` and `n = 2`) | the density-free ratio would hold only for the isothermal cusp |
| `k = 9 -> 1` | K15, K16 | candidate 2 would look like a different (also dead) formula |
| Mpc -> kpc | K8 (the non-zero fractions) | every "can SPARC resolve it" fraction would read 0 % |

None of the three can be absorbed by a tolerance: each moves a check by more than its stated band
(`0` vs `L^2/2r^2`; `82.86 %` vs `30.29 %`; `0.0000` vs `0.0114`).
