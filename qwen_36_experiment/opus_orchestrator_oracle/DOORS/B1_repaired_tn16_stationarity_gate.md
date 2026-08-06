# DOOR B1 — Repaired tn16 with a stationarity gate
STATUS: OPEN | RANK: 5 | COST: S | KILLS FAST: n/a (housekeeping that stops a false result recurring)

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
tn16's headline `rho_min = -6.736e43` recurs on every rerun and is an artefact. Five one-line repairs, all
identified and verified in review:
1. **sin, not cos** (`tn16:199`) — the integrand is exactly odd; the cos recipe equals 1/(pi^3 eps), which is
   why rho comes out flat at ~6.3e11.
2. **restore dtau** (`tn16:132`) — its own docstring at `:100` specifies it. Missing it inflates the kernel
   norm by 1/dtau = 40.94, so nominal q^2 = 3e-2 is physically 1.2282 = **61.6x the real threshold**.
   (`tn15:286` does carry it.)
3. **tau_min = 1e-4 >> eps** — with tau_min = eps = 1e-8, delta_m is dominated by the regulator.
4. **exact triangular solve, not 80 Picard steps** — the operator is unit lower triangular, so `det = 1` for
   every q^2 and the resolvent always exists. No iteration is needed.
5. **refuse non-converged rows** — the two MOND rows ARE the two "Did not converge" rows (residuals 0.582,
   1.59), and `tn16_rho_ness_results.json` banks them.
Then add a **stationarity gate**: reject any solution whose late-tau growth rate is positive.

## Why it works with the framework
Pure repair. It changes no physics and no constant. Its value is that it stops a wrong number propagating
into every future paper draft.

## Concrete first calculation
Apply all five repairs, re-run the q^2 scan, and print for each row: converged?, late-tau growth rate,
rho_min, delta_m, and the gate verdict. Include a refinement column (N = 2048/4096/8192).

## Settles if / refuted if
SETTLED: with repairs, delta_m > 0 at every stationary coupling and rho < 0 appears only where the growth
rate turns positive — review found onset of negativity IS loss of stationarity, agreeing to < 1%
(rho_min = +7.9e-3 at 0.99x threshold, -4.7e-2 at 1.01x).
REFUTED: a stationary solution with rho < 0 exists ⇒ that is a real result and goes straight to A5.

## Known walls — do not rediscover
`q^2_crit = 0.06248` is not a bifurcation: it is `1/||G_R||_2` of the wrong operator on an N=64 grid, and
`||K|| ∝ N` so it tends to 0 (0.0625 at N=64 → 0.0038 at N=1024). The equation's only real threshold is the
Laplace pole `q^2 = 2 eta / A = 0.0199254`. Also: `delta_m ∝ 1/omega_min` exactly, so no magnitude exists in
either sign until C4 is done.
