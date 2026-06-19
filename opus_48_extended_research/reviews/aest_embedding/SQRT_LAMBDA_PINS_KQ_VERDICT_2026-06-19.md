# Does sqrt(Lambda) pin the AeST K(Q) amplitude? — the embedding's zero-vs-one-free-number crux (2026-06-19)

*Topic `sqrt_lambda_pins_KQ`. Tests whether the framework's de Sitter/Unruh/holographic
structure PINS the AeST dark-matter-mimic amplitude (I0 / Omega_dust) or mass (mu^2/K2), or
whether they are genuinely free. Primary source verified vs ar5iv full text this session;
calc in `sqrt_lambda_pins_KQ.py`. Quarantine held (a0/Z/kappa not asserted derived). Both-ways:
a "sqrt(Lambda) pins K(Q)" claim tested as hard as a "it stays free" claim. No manufactured unification.*

## ONE-LINE VERDICT

**NO — sqrt(Lambda) does NOT pin the K(Q) amplitude. The embedding gives a COMPLETE relativistic-MOND
host with the MOND scale a0 founded on Lambda, but the dark-matter-mimic AMPLITUDE (I0 -> Omega_dust ~ 0.26)
stays a FREE integration constant, and the mass mu^2/K2 stays a free empirically-pinned coupling. So the
honest prize is "ONE free number" (really 2+ in the dark sector), NOT "zero." Crediting Omega_dust ~ Omega_dm
as a unification would be manufactured (it's an O(1) why-now coincidence a0=sqrt(Lambda) provably does not set).**

## THE PRIMARY-SOURCE STRUCTURE (Skordis-Zlosnik 2021, arXiv:2007.00082, verified verbatim this session)

FLRW reduction: `S = (1/8piGtilde) int d^4x N a^3 [-3H^2/N^2 + K(Qbar)] + S_m[g]`, with
`K = -2Lambda + K2(Qbar - Q0)^2 + ...`. The shift-symmetric scalar integrates once to
**`dK/dQ = I0/a^3`** => **`rho-bar = rho-bar0/a^3`** (pressureless dust, the CDM-mimic the 3rd peak needs).
Dust amplitude: **`8 pi Gtilde rho_dust0 = Q0 * I0`**.

Authors' verbatim, load-bearing:
- **"As the solution depends on the initial condition I0, the density rho-bar is not (classically) predicted."**
- **"The CC in this model remains a freely specifiable parameter, just as in the LambdaCDM model."**
- extra free params vs LCDM: **"lambda_s, K_B, K2 (or equivalently w0) and Q0"** (+ the dust I0).
- a0 enters a DIFFERENT (orthogonal) sector: **`J -> (2 lambda_s/[3(1+lambda_s) a0]) Y^(3/2)`** — the
  spatial-gradient Y-sector, the sqrt-law n=3/2 (matches the framework). Y=0 on FRW => a0 is provably
  ABSENT from linear perturbations (Bridge-1).
- the mass mu (Verwayen-Skordis-Zlosnik 2024, MNRAS 531 272): **"for our purposes we treat it as a free
  parameter in this work"**; empirically pinned by flat-rotation-curve extent; NO stated `mu = f(Lambda)`.

## THE THREE TESTS (both-ways; none manufactures a relation)

**Test 1 — can a dS/holographic identity hit Omega_dust ~ 0.26?** Target why-now ratio
`Omega_dust/Omega_DE ~ 0.39`. Enumerated the candidate dimensionless dS/holographic combinations of
{Lambda, a0, Z, Omega_DE}: `Omega_DE` (0.685, off 2.6x), `1-Omega_DE` (=Omega_M by definition, includes
baryons, circular), `Omega_DE/Z` (0.118, off), `Omega_DE^(3/2)` (0.567, off). **NONE lands on 0.26 without
a hand-tuned O(1).** Any "holographic dust entropy" route is circular — a dust entropy already contains I0.

**Test 2 — can sqrt(Lambda) fix mu^2/K2?** Empirical `mu^-1 ~ 50 kpc - 1 Mpc`. Framework lengths: dS horizon
`c/H_Lambda ~ 5350 Mpc` (~10^3 x too big); the a0-crossover `sqrt(GM/a0) ~ 12 kpc` (galaxy-scale, RIGHT
ballpark). The galaxy-scale coincidence is the a0-crossover = a RESTATEMENT of a0, not a pin of the dark
sector. The Mistele/cluster SQUEEZE (galaxy-WL wants `m^2/f_G < 1 Mpc^-2`, clusters want `> 1`) shows mu is
pulled OPPOSITE ways by data — the signature of a FREE constant, not `mu = f(Lambda)`.

**Test 3 — THE DECISIVE STRUCTURAL SEPARATION (the real reason, not a numerology miss):**
`a0, Lambda, Z` are **action couplings** (Lagrangian constants: the Y^(3/2) coefficient = a0, the -2Lambda
term = Lambda). `I0 -> Omega_dust` is an **INTEGRATION CONSTANT** of the shift-symmetric phi-bar equation —
fixed by an INITIAL DATUM (the displacement of Q from Q0 at early times), NOT by the action's couplings.
`Q0` (expansion point) and `mu^2 ~ K2` (curvature at Q0) are further free K-constants. **A boundary/initial
constant is orthogonal to the bulk couplings by construction.** No de Sitter/Unruh/holographic thermodynamics
acting on couplings can set an initial datum. To claim sqrt(Lambda) pins I0 you must MANUFACTURE an O(1).
This is WHY Bridge-1 (a0 absent from linear theory) is not an accident: the dust amplitude that feeds the
linear transfer functions lives in a slot a0 cannot reach.

## BOTH-WAYS LEDGER

| claim | grade |
|---|---|
| a0 <-> Lambda is a real unification of the dark-ENERGY face (Omega_DE=0.685) | TRUE — credit fully |
| AeST fits full Planck CMB incl. 3rd peak via the a^-3 K(Q) dust | TRUE — genuine first for rel. MOND |
| The framework's dS-Unruh aether is a natural microphysical origin for AeST's A_mu | TRUE (embedding holds at {a0=MOND scale, A_mu=cosmic rest frame}) |
| sqrt(Lambda) / a0 / Z PINS the K(Q) dust amplitude I0 (=> Omega_dust) | **FALSE — I0 is a free integration constant ("rho-bar not classically predicted")** |
| sqrt(Lambda) PINS the K(Q) mass mu^2 / K2 | **FALSE — free, empirically pinned, squeeze-free; no mu=f(Lambda)** |
| Omega_dust ~ 0.26 ~ Omega_dm is a unification | **FALSE — O(1) why-now coincidence of ABUNDANCE; a0 absent from linear theory (Bridge-1) cannot set it** |
| The embedded framework has ZERO free numbers | **FALSE** |
| The embedded framework has ONE free number (honest prize) | TRUE in spirit; literally 2+ ({I0, Q0, K2/mu, lambda_s, K_B}), the load-bearing one = the amplitude I0 |

## NET

The embedding hypothesis (a) holds for the MOND scale: a0 = c^2 sqrt(Lambda/32pi) is a natural AeST MOND
scale tied to Lambda; (b) holds for the aether: dS-Unruh supplies a microphysical reading of A_mu = cosmic
rest frame; **(c) FAILS: sqrt(Lambda) does NOT pin the K(Q) amplitude — the dark-sector amplitude stays
free.** The framework becomes a COMPLETE relativistic MOND (galaxies+clusters+CMB+lensing+Cassini) FOUNDED
on de Sitter-Unruh with the MOND scale tied to Lambda, but the dark-MATTER-mimic density (~Omega_dm, the
load-bearing I0) is an independent number it does not derive and cannot avoid. **One free number, not zero.**
The dark sector is relocated (particle DM -> field condensate amplitude), not eliminated. Concede this loudly;
the honesty is what keeps the a0<->Lambda (dark-energy) unification credible.

## SOURCES
- Skordis & Zlosnik 2021, PRL 127 161302 = arXiv:2007.00082 (ar5iv full text, verified verbatim this session).
- Verwayen, Skordis & Zlosnik 2024, MNRAS 531 272 = arXiv:2304.05134 (mu "treated as a free parameter").
- Durakovic & Skordis 2024, JCAP = arXiv:2312.00889 (Q=Q0+I0(1+z)^3; Omega_AeST set by I0).
- Banked corpus: ROUTE2_CMB_THROUGH_AEST_2026-06-15, SKORDIS_CMB_CLUSTER_DEEPDIVE_LEDGER_2026-06-15,
  DARK_SECTOR_CMB_CLUSTERS_2026-06-19, dark_sector_cmb/{ONE_OR_TWO_VERDICT, aest_kq_alternative.py}.
- Calc: `aest_embedding/sqrt_lambda_pins_KQ.py` (this session).
