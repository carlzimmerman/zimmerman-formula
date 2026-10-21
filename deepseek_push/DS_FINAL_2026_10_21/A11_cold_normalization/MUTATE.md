# A11 — MUTATE

Seven mutations, each a plausible mis-statement of one premise. `python3 a11_checks.py --mutate <Mu>` applies
the mutation, prints `# MUTATION: ...` in the header, writes the mutated JSON to `a11_results_MUTATE.json`, and
exits 1 whenever a check fails (by design).

| id | mutation | checks that break | score |
|---|---|---|---|
| Mu1 | replace the canonical law by the n=2 "a₀-line" law `g² = g_N² + a0 g_N` | K9a, K17 | 2 break, 32/34 |
| Mu2 | `Δ_ta = 1` (no turnaround): `r_ta` becomes the mean-density radius | K10b | 1 breaks, 33/34 |
| Mu3 | `f_b = 0.5`, so `(1−f_b)/f_b` becomes 1.0 instead of 5.364 | K4b, K4c, K6a, K7a, K7b, K7c, K10b, K18a, K20 | 9 break, 25/34 |
| Mu4 | linear edge `r_e = N r_M` instead of the exact `r_M√(N(N+1))` | K9a, K7c, K17 | 3 break, 31/34 |
| Mu5 | `c_s² = 4πG L*²ρ` instead of `2πG L*²ρ` | K11a, K11b | 2 break, 32/34 |
| Mu6 | `λ_J = 2πL*` instead of `√2πL*` | K13a | 1 breaks, 33/34 |
| Mu7 | `M_ph/M_b = (√(1+2/y)−1)/2` (kernel coefficient 1 instead of 4) | K2, K3a, K3b, K4a, K4c, K6a, K18a, K19 | 8 break, 26/34 |

Measured values, clean → mutated:

- **Mu1**: K9a `1.1e-16 → 5.51e-2`; K17 `40 → 0`. The exact edge root is a property of the canonical kernel,
  not of any interpolation with the same deep limit. K1 and K2 stay PASS because they are symbolic statements
  about the canonical law and are not re-evaluated under the mutation — stated so the immunity is not mistaken
  for teeth.
- **Mu2**: K10b `1.399 → 0.620`. The condensed variant's R5 violation disappears if `r_ta` is inflated to the
  mean-density radius, i.e. the exclusion of `N = 53.6` is a statement about `Δ_ta`, exactly as §13 says.
- **Mu3**: K7a `8.296 → 1.546`; K4b `5.843 → 1.414`. Changing `f_b` moves the cosmic ratio and the census `N`
  together, which is the point of §9–§10.
- **Mu4**: K9a `1.1e-16 → 5.85e-2`; K7c `5.4e-4 → 5.91e-2`. The record's log form differs from `N r_M` by
  6% at `N = 8.3` and from the exact root by 0.05% — this is the mutation that separates the two.
- **Mu5**: K11a `0.5191 → 1.0382`; K11b `33.311 → 23.555`. Doubling the prefactor moves the causal crossing
  by `√2`.
- **Mu6**: K13a `106.63 → 150.80`.
- **Mu7**: K2 `0 → 0.479`. A wrong kernel coefficient is caught by the symbolic identity plus its numeric
  tie-in, and propagates to every check that consumes `F`.

## Recorded output — `--mutate Mu4` (the subtlest mutation; complete stdout, exit 1)

```
# MUTATION: Mu4 (use the linear edge r_e = N r_M instead of the exact r_e = r_M sqrt(N(N+1)))
# A11 cold-sector normalization checks  (G=6.67430e-11, a0=9.36e-11, c=2.99792458e8)
# f_b=0.157126  5.364 = (1-f_b)/f_b = 5.364327
K1 PASS 0.000000e+00 1.000000e-30
K2 PASS 0.000000e+00 1.000000e-13
K3a PASS 1.250062e-09 1.000000e-06
K3b PASS 1.000060e-06 1.000000e-05
K4a PASS 0.000000e+00 1.000000e-12
K4b PASS 5.842973e+00 5.842970e+00
K4c PASS 1.424511e+01 1.400000e+01
   # MW       M_b=6.00e+10 r_v=0.2455 Mpc  M_tot=1.563e+12  mu(<r_v)=0.968  M_ph/M_b(enc)=25.90  M_ph/M_b(tot)=25.04  y_v=0.00144  c=r_v/a=61.4
   # cluster  M_b=1.40e+14 r_v=1.6863 Mpc  M_tot=5.065e+14  mu(<r_v)=0.758  M_ph/M_b(enc)=3.77  M_ph/M_b(tot)=2.62  y_v=0.05560  c=r_v/a=6.7
K5 PASS 9.565951e+00 2.000000e+00
   # volume integral of rho_ph = 3.679069e+42 vs boundary 3.679069e+42  (min rho_ph 3.796e-25 > 0)
K22 PASS 1.332268e-15 1.000000e-06
   # a=    1 kpc  c= 247.0  mu=0.9920  M_ph/M_b(tot)=25.53  y_v=1.45e-03
   # a=    2 kpc  c= 123.2  mu=0.9840  M_ph/M_b(tot)=25.36  y_v=1.45e-03
   # a=    4 kpc  c=  61.4  mu=0.9682  M_ph/M_b(tot)=25.04  y_v=1.44e-03
   # a=    8 kpc  c=  30.4  mu=0.9374  M_ph/M_b(tot)=24.41  y_v=1.41e-03
   # a=   16 kpc  c=  15.0  mu=0.8787  M_ph/M_b(tot)=23.20  y_v=1.37e-03
   # a=   32 kpc  c=   7.2  mu=0.7722  M_ph/M_b(tot)=20.94  y_v=1.28e-03
K19 PASS 1.245004e-12 1.000000e-09
K6a PASS -1.675730e-01 -1.666667e-01
K6b PASS -5.000000e-01 -5.000000e-01
   # M_b=3.0e+10  f_ret=0.1000  log10 M_ta=12.110  N=53.6433
   # M_b=1.0e+11  f_ret=0.1216  log10 M_ta=12.548  N=44.1254
   # M_b=1.0e+12  f_ret=0.3596  log10 M_ta=13.077  N=14.9169
   # M_b=1.0e+13  f_ret=0.6466  log10 M_ta=13.822  N=8.2958
   # M_b=1.0e+14  f_ret=0.9000  log10 M_ta=14.679  N=5.9604
K7a PASS 8.295808e+00 8.296000e+00
K7b PASS 5.364327e+01 5.364300e+01
K8a PASS 2.435290e-02 1.000000e-02
K8b PASS 3.565749e-02 1.000000e-02
   # M_b=3.0e+10  N=53.643  law F(r200)=36.823  N/F=1.457  r200=0.249 Mpc
   # M_b=6.0e+10  N=53.643  law F(r200)=32.752  N/F=1.638  r200=0.314 Mpc
   # M_b=1.0e+11  N=44.125  law F(r200)=28.152  N/F=1.567  r200=0.350 Mpc
   # M_b=1.0e+12  N=14.917  law F(r200)=13.299  N/F=1.122  r200=0.532 Mpc
   # M_b=1.0e+13  N=8.296  law F(r200)=7.369  N/F=1.126  r200=0.958 Mpc
   # M_b=1.0e+14  N=5.960  law F(r200)=4.384  N/F=1.360  r200=1.875 Mpc
   # min N/F = 1.072 at log10 M_b = 12.60  (census never undersupplies the law)
K18a PASS 1.072276e+00 1.250000e+00
K18b PASS 1.260000e+01 1.300000e+01
K9a FAIL 5.845401e-02 1.000000e-12
K7c FAIL 5.912558e-02 2.000000e-03
K17 FAIL 0.000000e+00 4.000000e+01
K10a PASS 3.884017e-01 1.000000e+00
K10b PASS 1.399047e+00 1.000000e+00
K11a PASS 5.190809e-01 5.190800e-01
K11b PASS 3.331146e+01 3.331100e+01
K12 PASS 3.945375e+02 1.000000e+02
K13a PASS 1.066292e+02 1.066290e+02
K13b PASS 1.044966e-04 1.000000e-03
K14 PASS 7.723046e+02 1.000000e+02
   # M_b=6e10 galaxy: r_M=9.453 kpc  r_e(N=53.64)=507 kpc  r_e(N=8.30)=78 kpc
K20 PASS 6.466161e+00 5.000000e+00
   # window as velocities: sigma_lo=8.33 km/s (24 pc)  sigma_hi=55.08 km/s (1.050 kpc)
K21 PASS 1.050285e+00 1.000000e+00
K15a PASS -6.666667e-01 -6.666667e-01
K15b PASS 2.331468e-15 1.000000e-10
K16 PASS 1.302227e+01 1.000000e+01
#
# names: K1 law inversion | K2 phantom-ratio identity | K3 limits | K4 5.364 inverse
#        K5 non-universality | K6 scaling | K7 census N | K8 cube test | K9 edge root
#        K10 R5 bound | K11-K12 sound speed | K13-K14 cutoffs | K15 barotropic no-go
#        K16 cross-section no-go | K17 N not fixed by the law | K20 turnover
#        K18 census-vs-law gap | K19 concentration | K21 window-as-velocity
#        K22 volume integral of rho_ph equals the boundary term
A11 COMPLETE: 31/34 checks PASS.
```

Three checks fail, all three of them edge-geometry checks, and nothing else moves by more than the 6% the
mutation itself injects (K10a `0.393 → 0.388`, K10b `1.412 → 1.399`, K20 `6.165 → 6.466`). That localisation
is the evidence that K9a/K7c/K17 test the edge relation and not, say, the census table.

## Recorded output — `--mutate Mu7` (breaks the central identity)

```
K2 FAIL 4.790568e-01 1.000000e-13
K3a FAIL 2.929079e-01 1.000000e-06
K3b FAIL 5.000002e-01 1.000000e-05
K4a FAIL 3.173887e-01 1.000000e-12
K4c FAIL 1.334202e+01 1.400000e+01
K19 FAIL 3.013617e-01 1.000000e-09
K6a FAIL -1.679483e-01 -1.666667e-01
K18a FAIL 1.549332e+00 1.250000e+00
A11 COMPLETE: 26/34 checks PASS.
```

Exit code 1. K5, K7, K10, K11–K16, K20, K21 and K22 stay PASS, so the suite does not fail wholesale: the
mutation is caught by the checks that depend on the form of `F`, not by those that depend on
`(f_b, f_ret)`, `L*` or `σ/m`.
