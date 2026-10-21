# CFG935 AMENDMENT A1: the S2 thin-shell discretisation (implementation fix; before any S2 result)

Date: 2026-10-20. Committed alone, after FROZEN_CRITERIA.md (38f4b6f18) and AMENDMENT A0 (e9a824153), and before any valid
R-a(ii) (S2) number exists. FROZEN_CRITERIA.md is not edited.

## What failed

FROZEN_CRITERIA §2 discretised the S2 tether energy with m(<r) piecewise constant between sorted shells, so the force on a
shell is the exact step derivative (r²/G)[w(G(k+1)μ/r²) − w(Gkμ/r²)], w(u) = −u²/2 − a₀u − a₀² ln(1 − u/a₀). Because w diverges
only logarithmically at u = a₀, this force grows only like −ln(a₀ − u) and its work is finite. **In the frozen rule a shell of
finite mass can therefore reach u = a₀, where the action is undefined.** The continuum barrier is infinite: the push per unit
mass, K W_rem′(u) = u²/(a₀ − u), diverges as 1/(a₀ − u), and its work diverges logarithmically. The frozen rule was a
discretisation artefact, and its first runs broke down:
- MUTATE M3 (S2, IC-I, t_end 100) and the first Ra2_I run reached u ≥ a₀ at t = 1.80 and returned NaN energies;
- the first Ra2_S run, with a step limit added (an inward shell may cover at most 10% of the gap to its own barrier per step),
  still reached the barrier at t = 17.93 and returned NaN;
- Ra2_L (the cold static law) ran correctly (energy exact to 1e-14); it is rerun with A1 anyway.

Seen in those failed runs (disclosed): progress lines with escaped fractions 0.12–0.25 and enclosed masses m(<2, 5, 8) ≈
0.8–1.3, 2.5–3.1, 3.8–4.4 at t ≈ 550–750. Those runs had NaN energies (at least one shell had left the domain of the action), so
no number from them is used.

## The fix: midpoint-in-mass thin shells (the rule the gravity already uses)

A shell of rank k (k shells strictly inside) feels the push μ h(u_k), h(u) = u²/(a₀ − u), u_k = G(k + ½)μ/r². This is the exact
gradient of

  V_tether,mid = Σ_k μ φ_k(r_(k)),  φ_k(r) = ∫_r^∞ h(A_k/r′²) dr′ = (A_k/r)[atanh(√x)/√x − 1],  A_k = G(k + ½)μ, x = A_k/(a₀r²),

which is continuous when shells cross (the sum over ranks at a common radius is symmetric). It is the midpoint rule in mass of
the same continuum functional, (1/G)∫r² w(G m/r²) dr = ∫dr ∫_0^{m(r)} h(G m′/r²) dm′, so it converges to the same S2 energy as
μ → 0. Its barrier at u_k = a₀ is infinite (φ_k diverges logarithmically, its force as 1/gap). Its discrete static state is
exactly the law's quantiles, M_ph(<r_k) = (k + ½)μ, because h(u_law) = g_N. The baryon pull −μ g_b and the energy Σ μΦ_b are
unchanged. No physics changes; only the discretisation of the S2 term does.

**Step limit (kept):** an inward-moving shell may cover at most 10% of the gap to its own barrier r_b,k = √(G(k + ½)μ/a₀) per
step (a floor of 1e-10 is flagged if hit).

## Other implementation notes (disclosed)

- `brentq` rejected rtol = 4e-16 (minimum 4·eps) in the first ETH part, which therefore wrote nothing. With A1 the static
  positions come from Newton-refined quantiles instead.
- The runner logged "rc 0" for that crash, because `$(date)` in the same echo resets `$?`. Part success is judged by the part
  JSON, not by the logged rc.
- Before any scored run the reflecting inner boundary was moved from r_min = 0.05 to 1e-3. At 0.05 it pumped energy (K2 test
  ε_E 8.9e-3 at t = 200). At 1e-3 no shell reaches it, and K2 gives 1.5e-4 at t = 200 (2.1e-4 at t = 650).
- Rerun order after the runner finishes the N-type parts (which A1 does not touch): ETH, Ra2_L, Ra2_I, Ra2_S, MUTATE, summary.
