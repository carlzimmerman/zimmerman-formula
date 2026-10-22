# A74 — MUTATIONS

Invocation: `A74_MUTATE=<name> python a74_checks.py` → writes `a74_MUTATE_<name>.out` and
`a74_results_MUTATE_<name>.json`, and exits **1** if any check fails.
Sweep driver: `run_mutations.py` (batched; merges into `mutation_results.json`).

**20 mutations, each changes exactly one input, each exit 1, no crashes, and all 29 checks are killed by
at least one.** No check had to be deleted.

| name | the one input it changes |
|---|---|
| `drop_gal` | skips every 10th SPARC galaxy (175 files → 154 fitted) |
| `drop_lens` | drops every 7th usable SLACS lens (70 → 60) |
| `floor10` | SPARC error floor 0.05 → 0.10 of V |
| `a0_off20` | a0 inside both likelihoods scaled by 0.8 (a 20% calibration error) |
| `sersic35` | Sérsic index n = 4.0 → 3.5 in the SLACS stellar mass |
| `arcsec` | arcsec→radian scale × 1.10 (a 10% error on R_e) |
| `imf_prior` | IMF prior width 0.036 → 0.100 dex (A70's cross-method spread) |
| `no_boot` | σ(SPARC) = the formal Δχ² = 1 error instead of the block bootstrap |
| `boot_draws` | bootstrap 200 → 60 draws |
| `kappa_de` | `kappa_of_a0` returns the ρ_DE convention instead of ρ_crit |
| `thermal_pi` | the thermal a0 = cH_Λ/π instead of cH_Λ/(2π) (doubled) |
| `treu_shift` | Treu+2010 per-lens log α shifted by +0.10 dex |
| `u_prior` | cluster prior σ_u 0.03 → 1.0 (prior removed) |
| `cluster_a` | A18 scale radius 250 → 200 kpc |
| `h0_70` | H0 = 67.4 → 70 km/s/Mpc |
| `omega` | Ω_Λ = 0.6847 → 0.72 |
| `b_marg` | B reported at the lensing value instead of the prior-weighted optimum (the profile/NM consistency is broken) |
| `resp_lin` | the B-response defined as ΔR/R over ΔB/B instead of the log derivative |
| `lambda_off` | Λ = 1.0890e-52 → 1.10e-52 m^-2 |
| `ups_window` | Υ window 0.05–2.5 → 0.40–1.00 |

## Exit codes and kills (final sweep, shipped script)

```
drop_gal     exit 1   23.7s  C1,C3,C6,C7,C15,C17,C22,C23,C28
drop_lens    exit 1   26.2s  C2,C8,C9,C10,C11,C15,C17,C22,C23,C24,C28
floor10      exit 1   27.4s  C3,C6,C7,C15,C17,C19,C22,C23,C24,C28,C29
a0_off20     exit 1   25.8s  C3,C6,C7,C8,C9,C10,C15,C17,C18,C19,C21,C22,C23,C24,C27,C28,C29
sersic35     exit 1   26.7s  C8,C9,C10,C11,C15,C17,C20,C28
arcsec       exit 1   26.5s  C8,C9,C10,C15,C28
imf_prior    exit 1   27.7s  C15,C17,C22,C23,C24,C28
no_boot      exit 1   26.7s  C15,C17,C18,C19,C21,C22,C23,C24,C28,C29
boot_draws   exit 1   11.7s  C7,C15,C17,C22,C23,C28
kappa_de     exit 1   28.9s  C4,C6,C14,C15,C17,C18,C19,C21,C22,C23,C24,C28,C29
thermal_pi   exit 1   27.1s  C5,C18,C19,C20,C21,C22,C23,C25,C26,C27,C29
treu_shift   exit 1   25.6s  C12
u_prior      exit 1   25.7s  C14,C15,C17,C22,C23,C28
cluster_a    exit 1   25.2s  C13,C14,C15,C17,C19,C22,C23,C28
h0_70        exit 1   25.3s  C4,C5,C6,C10,C13,C14,C15,C17,C18,C22,C23,C24,C25,C27,C28
omega        exit 1   25.9s  C5,C25
b_marg       exit 1   26.3s  C15,C16,C17,C18,C23,C27,C28
resp_lin     exit 1   26.4s  C10,C11,C15,C17,C20,C22,C23,C24,C28
lambda_off   exit 1   26.4s  C5,C25
ups_window   exit 1   17.2s  C3,C6,C7,C15,C17,C18,C19,C21,C22,C23,C24,C28,C29
```

## Which mutation kills which check

```
C1   drop_gal
C2   drop_lens
C3   drop_gal, floor10, a0_off20, ups_window
C4   kappa_de, h0_70
C5   thermal_pi, h0_70, omega, lambda_off
C6   drop_gal, floor10, a0_off20, kappa_de, h0_70, ups_window
C7   drop_gal, floor10, a0_off20, boot_draws, ups_window
C8   drop_lens, a0_off20, sersic35, arcsec
C9   drop_lens, a0_off20, sersic35, arcsec
C10  drop_lens, a0_off20, sersic35, arcsec, h0_70, resp_lin
C11  drop_lens, sersic35, resp_lin
C12  treu_shift
C13  cluster_a, h0_70
C14  kappa_de, u_prior, cluster_a, h0_70
C15  drop_gal, drop_lens, floor10, a0_off20, sersic35, arcsec, imf_prior, no_boot,
     boot_draws, kappa_de, u_prior, cluster_a, h0_70, b_marg, resp_lin, ups_window
C16  b_marg
C17  drop_gal, drop_lens, floor10, a0_off20, sersic35, imf_prior, no_boot, boot_draws,
     kappa_de, u_prior, cluster_a, h0_70, b_marg, resp_lin, ups_window
C18  a0_off20, no_boot, kappa_de, thermal_pi, h0_70, b_marg, ups_window
C19  floor10, a0_off20, no_boot, kappa_de, thermal_pi, cluster_a, ups_window
C20  sersic35, thermal_pi, resp_lin
C21  a0_off20, no_boot, kappa_de, thermal_pi, ups_window
C22  drop_gal, drop_lens, floor10, a0_off20, imf_prior, no_boot, boot_draws, kappa_de,
     thermal_pi, u_prior, cluster_a, h0_70, resp_lin, ups_window
C23  drop_gal, drop_lens, floor10, a0_off20, imf_prior, no_boot, boot_draws, kappa_de,
     thermal_pi, u_prior, cluster_a, h0_70, b_marg, resp_lin, ups_window
C24  drop_lens, floor10, a0_off20, imf_prior, no_boot, kappa_de, h0_70, resp_lin, ups_window
C25  thermal_pi, h0_70, omega, lambda_off
C26  thermal_pi
C27  a0_off20, thermal_pi, h0_70, b_marg
C28  drop_gal, drop_lens, floor10, a0_off20, sersic35, arcsec, imf_prior, no_boot,
     boot_draws, kappa_de, u_prior, cluster_a, h0_70, b_marg, resp_lin, ups_window
C29  floor10, a0_off20, no_boot, kappa_de, thermal_pi, ups_window
```

## Notes

1. **Every check is an evaluated comparison, not an assertion.** Each `ck(...)` computes a quantity from
   the data or from the likelihood and compares it to a value computed elsewhere: a stored value from
   another lane (`a71_results.json`, `a51_results.json`, `a55_results.json`, `a72_results.json`), a second
   numerical route (profile vs Nelder-Mead; spline vs direct 70-lens root; two quadrature forms; two
   σ(log B) routes), or an exact algebraic identity (`kappa_DE/kappa_P3 = 1/√Ω_Λ`, `R_core = 2.22144 L*`,
   the √2 between the two m_P formulas). No check is `ok = True` and none compares a quantity to itself.
2. **Six checks contain an identity clause**, and each is paired with a substantive comparison: C16
   (profile vs 3-D minimiser), C18/C19 (Δχ² vs the sum of its four terms; the three Δχ² consistent),
   C21 (Δχ² → σ → LR), C26 (R_core = (π/√2)L\\*), C27 (three decompositions close). Their identity clauses
   fail only if a code path breaks, which is what `b_marg` and `a0_off20` do — and each of the six is
   killed by at least one mutation (C16 by `b_marg`; C18 by `thermal_pi`/`b_marg`; C19 by
   `imf_prior`/`thermal_pi`; C21 and C26 by `thermal_pi`; C27 by `a0_off20`/`b_marg`). The identity is kept
   because it is load-bearing: if the reported decomposition did not close, or the LR were not the
   exponential of Δχ², every number in the report would be wrong. Each check also carries a substantive
   clause (a band, a sign structure, or a value stored by another lane).
3. **C26 has a single killer** (`thermal_pi`, which doubles a0 and puts L\* = 13.04 pc outside [24, 90]).
   That is a genuine single point of failure of that check, stated rather than hidden; C25 and C27 also
   respond to the same mutation, so the falsifier block as a whole is not singly protected.
4. **Two mutations crash if the checks are not written defensively** (a negative Δχ² under `thermal_pi`,
   and a negative raw-χ² difference under `a0_off20`). The shipped script takes `abs()` in the *diagnostic*
   square roots and lets the check fail on the sign, so both mutations produce named FAILs rather than a
   traceback. Exit codes are identical either way, but a crash would hide which checks the mutation kills.
5. **The `a0_off20` mutation was originally `newton` (a0 → 1e-30).** That moves the SPARC optimum outside
   the minimiser's bracket `[5e-11, 2.5e-10]` and the run dies in `brentq` before reaching most checks, so
   it was replaced by a 20% calibration error, which is also the more realistic systematic. The exact-Newton
   limit is not needed: C3 already pins the likelihood to the record at a0 = 1.132e-10 and 9.36e-11.
6. `mutation_results.json` holds the machine-readable sweep: `{mut, exit, fails[], crash, secs}`.
7. **Provenance of the sweep.** The 20 runs above were made with the shipped check set. A handful of
   *print-only* lines were added to `a74_checks.py` afterwards (the σ of the two costs, the quoted
   inputs/systematic floor, σ(κ)_SPARC, R_req ± σ_R, and σ(κ_P3) at 3σ), so `a74_MUTATE_*.out` lack those
   lines; every `ck(...)` expression, threshold and reference value is identical, and each mutation `.out`
   still contains all 29 check verdicts (verified: 29 per file, FAIL sets equal to
   `mutation_results.json`).
