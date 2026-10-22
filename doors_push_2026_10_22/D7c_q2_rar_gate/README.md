# D7c_q2_rar_gate — does any law in the record's family pass both Cassini Q₂ and SPARC?

**Scope: UNSCREENED law forms only.** That means a point-mass Sun in a uniform external field, with no L★ stiffness
screening. The screened case is lane `D7d_screened_q2`. Nothing here says "the framework fails Cassini". It says what the
**unscreened law family** does.

## Verdict: SCOPED NO-GO, with one near-miss

- **No candidate passes both tests on both footings.** The frozen outcome rule therefore gives "no law passes both".
  The weakest tension in the whole family is **+2.6 σ** (Hees). It sits in one cell of the β family.
- **The action's own capacity family is a clean no-go.** This is u² + n g_N u = a₀g_N (n = 1 is the canonical law,
  n = 2 is the quadratic line).
  - SPARC passes on both footings only at **n = 2**. Its Q₂ fails at all four external fields: **+2.9 to +8.2 σ**.
  - Q₂ passes at all four fields only at **n = 8**. SPARC disfavours n = 8 at **z = −6.3** (canonical) and **−5.2** (alt).
  - n = 4–6 pass Q₂ at some fields and fail at others, and they fail SPARC (z −4.7 to −6.0 canonical).
- **All five named record laws fail unscreened Q₂ at every external field, on both footings.**

  | law | Q₂ / Hees 2σ line, canonical | Q₂ / Hees 2σ line, alt |
  |---|---|---|
  | n = 1 canonical | 1.69–3.68× | 1.90–4.01× |
  | n = 2 (also the quadrature P2 and α = 1) | 1.30–2.68× | 1.50–3.08× |
  | ν_mono | 1.70–3.64× | 1.92–4.05× |
  | standard μ (α = 2) | 1.18–1.62× | 1.41–2.14× |
  | ν_RAR (reference) | 1.72–3.77× | 1.93–4.15× |

  Every law also fails Park 2026.
- **The near-miss is the β family**, CFG4's ν_β = (1+y^−β)^{1/2β}. The record calls it an effective description only.
  - For β ≥ 2.5, Q₂ passes at all four fields on the canonical footing.
  - These members also pass the graded SPARC statistic on both footings (worst z −1.5 to −1.9).
  - They fail only one cell: the alt footing at E0, the framework's Milky Way model. The excess there is 1.19–1.23×,
    which is +2.6 σ.
  - That cell has a floor. Beyond the grid, β = 10, 20 and 40 give 1.22×, 1.23× and 1.23×. No β passes it.
  - AG4b's secondary statistic, the summed Δχ², disfavours the same members at **z −5.5 to −5.8** (canonical) and
    −4.8 to −5.2 (alt). On the canonical footing alone, whether the β family passes therefore depends on which SPARC
    statistic you use. The primary statistic says yes and S1 says no.
- **How the canonical law depends on the external field.** Q₂ rises monotonically with the total field g_e.
  - Hees 2σ passes only for **g_e ≤ 8.20e-11 m/s²** (canonical a₀) or **8.13e-11** (alt).
  - Park passes only for g_e ≤ 5.64e-11 or 5.68e-11.
  - Both limits are 2.2–3.0× below the kinematic field at the Sun (1.78–2.43e-10).
  - They are also below the framework's own Milky Way field (total 1.22e-10).

## Method

- **Q₂.** D7b's validated Route-M solver, exec'd read-only.
  - It uses no turn-off, the four external fields E0–E3 and D7b's a₀ values.
  - PASS means −3e-27 ≤ Q₂ ≤ 9e-27 s⁻² at all four fields.
- **SPARC.** AG4b's pipeline, reproduced verbatim (K2 reproduces AG4b exactly).
  - 170 galaxies.
  - Υ_disk is fitted per galaxy under a stellar-population prior.
  - The graded statistic is the paired median-rms z against each of the five named laws. A law FAILS if any of them
    beats it at z ≤ −2.
- **Families.** Capacity n ∈ [0.5, 8] (AG4 Lean T7, n real) and β ∈ [0.5, 6] (CFG4), both on the frozen grids.

## Checks

The script passes 5 of 6 checks and exits 1.
- **K1** reproduces D7b to 3.4e-7.
- **K2** reproduces AG4b exactly.
- **K3**: n = 1 is the canonical law; n = 2, β = 1, P2 and the α = 1 kernel are all one function, to 7e-16.
- **K5** (convergence) and **K6** (analytic limit) pass.
- **K4 FAILS as frozen.** CFG4's tabulated ν_mono and A25's closed-form splice differ by 3.3e-9 (tolerance 1e-10).
  This is numerical only.
- The first run's K3 failure was check-side round-off. It was fixed post-result (Amendment A1), and the first-run output
  is kept.
- `--mutate` applies the record's /√D bug. K1 and K6 then FAIL (3/6), so the mutation bites.
- Runtime is about 40 s, single thread, 150 MB.

Files: `d7c_q2_rar_gate.py`, `.out`, `_results.json`, `_MUTATE.*`, `_firstrun.*`.

## Things in the record this bears on

- **n = 2, quadrature P2 and α = 1 are one law.** It has four names in the record: A25 "Q", CFG4 `nu_p2`, AG4 n = 2 and the
  DESITTER α = 1 kernel. Its unscreened Q₂ is 1.30–3.08× the Hees line.
- **A25's "SPARC does not disfavour L" depends on the statistic.**
  - A25 used fixed Υ and binned Δχ², and got R and L tied.
  - With per-galaxy Υ and AG4b's paired median rms, ν_RAR beats L at z −3.3 (canonical) and −4.8 (alt).
  - The size of that preference is only 1e-4 dex. A z this large on a tiny shift is a property of the paired statistic.
    Read it as "consistent but tiny", not "excluded".
- **This lane does not touch the DHF24 class conflict.** That conflict is reproduced here inside the record's own families.

## What this does not show

- **The screened law.** See D7d_screened_q2.
- **AQUAL.** It would raise Q₂ by about 1/0.74 (D7b K5).
- **An ephemeris refit.**
- **Power for SPARC.** This lane does not re-measure it. It inherits AG4b's n = 1 vs n = 2 power only.
- **Any law outside the record.**

κ = ½ is fitted; footings are never pooled; the theory is not closed.
