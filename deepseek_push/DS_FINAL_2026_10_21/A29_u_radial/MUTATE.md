# A29 — mutations

Three mutations, each a plausible slip in a *different* part of the chain, each breaking a
different check group. Run with `python3 a29_checks.py --mutate[2|3]`; each writes its own
`a29_MUTATE*.out` / `a29_results_MUTATE*.json` and exits 1.

## M1 — the inversion offset (`--mutate`)

`u = P_l/(D − P_N)` instead of `u = (P_l − P_N)/(D − P_N)`: the patient forgets that `P_l` already
contains the baryons, so the baryonic share is counted as phantom. This is the natural reading of
"the law's share of the signal" and it is wrong by the baryon term, which is 10–25% of `P_l`.

```
K2 FAIL u IN=0.4408 MID=0.5806 OUT=1.1462 0.3348+-0.056 / 0.4716+-0.036 / 0.9865+-0.098
K3 FAIL <w> IN=-0.1864 MID=-0.1398 OUT=+0.0487 -0.2217 / -0.1761 / -0.0045, ordered
K6 FAIL max rel resid 1.9e-01 <1e-10
K7 FAIL w(1/2)=-1/6 exact; MID +2.23s from -1/6; OUT +1.49s from 0 exact; |Z|<1.5 and |Z|<1
A29 COMPLETE: 21/25 checks PASS.
```

Note the failure mode: the offset *raises* u in every band, flips the MID value from 0.79σ to
+1.8σ from 1/2, and pushes OUTER to 1.15 — i.e. it manufactures a spurious "1/2 inside, >1
outside" structure. K6 (the round trip to the measured amplitude) catches it without any theory
input.

## M2 — the factor of 3 (`--mutate2`)

`⟨w⟩ = u − 1` instead of `(u−1)/3`: the trace of the stress is read as `ρ+3p = ρ(1+w)` rather than
`ρ(1+3w)`, i.e. the `3` in `T^i_i = 3p` is dropped.

```
K3 FAIL <w> IN=-0.6652 MID=-0.5284 OUT=-0.0135 -0.2217 / -0.1761 / -0.0045, ordered
K6 FAIL max rel resid 2.2e+00 <1e-10
K7 FAIL w(1/2)=-1/6 exact; MID -30.06s from -1/6; OUT -0.41s from 0 exact; |Z|<1.5 and |Z|<1
A29 COMPLETE: 22/25 checks PASS.
```

This is the mutation that matters physically: with `w = u−1` the inner medium would be at
w = −0.665, i.e. `w ≈ −2/3` — a *domain-wall* equation of state, and a very different claim. The
`u = 1/2 ⇔ w = −1/6` correspondence (K7) is what forbids it, and K7 breaks at 30σ.

## M3 — the wrong boundary (`--mutate3`)

`r_splash = R500` (0.7845 Mpc) instead of `1.15 r200c` (1.189 Mpc): the X-ray boundary identified
with the splashback radius. This is the most tempting error in the lane, because R500 is the number
the input catalogue actually supplies.

```
K18 FAIL r_sp=0.78 Mpc vs the MID/OUTER boundary 1.42 (ratio 0.553)
K20 FAIL |R_caustic(1.42) - r_sp(0.78)| = 0.63 Mpc (3.17 sigma); r_sp in (1.18,1.71) = False
A29 COMPLETE: 23/25 checks PASS.
```

Both boundary checks break: the significance of mechanism (iii) rests on r_sp landing on the
measured transition (caustic 1.4186 Mpc, u-step interval 1.176–1.711 Mpc), and R500 misses it by
3.2σ. The mutation also shows why the coefficient in §6 matters — the first version of this lane
used r200m/r200c = 1.39 instead of the correct 1.647, which put r_sp at 1.19 Mpc and would have
left mechanism (iii) surviving for the wrong reason.