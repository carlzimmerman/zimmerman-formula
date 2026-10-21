# A9 mutation — the check has teeth

Run: `python3 a9_checks.py --mutate` (exit code 1; normal run exits 0).

## The mutation

`rar_points()` applies the distance factor `f` to the **radius** (which sets both `g_obs`
and `g_bar` through `r`) but, under `--mutate`, drops it from the baryonic side:

```python
r  = g["rad"][m] * s
go = g["vobs"][m] ** 2 / r * KMS2_KPC
gb = vb2 / (g["rad"][m] * (1.0 if MUTATE else s)) * KMS2_KPC   # <-- s missing here
```

This is the most likely real bug in this calculation: `g_obs = V²/r` and `g_bar = V_bar²/r`
share one radius, and forgetting that on one side is exactly how a distance experiment gets
a wrong answer. It does not change the baseline fit (where `s = 1`), so it is a clean
single-cause mutation.

## What it breaks

```
K2  is the RAR's a0 prior-free?  Uniform D -> f*D must give a0 -> a0/f EXACTLY
        f=1.050   a0=9.702842e-11   a0*f/a0_0=0.923445808192   drms=2.81e-04
        f=1.083   a0=8.938395e-11   a0*f/a0_0=0.877427256506   drms=6.27e-04
        f=1.200   a0=6.785279e-11   a0*f/a0_0=0.738026750900   drms=2.82e-03
  K2 FAIL max|a0*f/a0_0 - 1| = 2.620e-01 ; max|drms| = 2.82e-03 dex
        threshold: < 1e-6 and < 1e-9 (the fit is exactly self-similar: a0 carries no absolute scale)

K3  the H0 lever: move only the 97 Hubble-flow distances from H0=73 to 67.4
        fiducial (SPARC H0=73 everywhere)  a0=1.103257e-10  rms=0.14190
        Hubble-flow set to H0=67.4         a0=9.809828e-11  (-11.083%)  rms=0.14170
  K3 FAIL d a0/a0 = -0.1108 for H0 73->67.4 on the Hubble-flow half
        threshold: -0.08 < d < -0.01 (predicted: -0.55 x 8.3% = -4.2%; the sign is fixed because D ~ 1/H0)
```

- **K2** goes from `1.3e-7` to `2.6e-1`: the fitted `a0` now scales as `1/f²` instead of
  `1/f`, so the invariance statement is destroyed by six orders of magnitude.
- **K3** goes from `−4.25%` to `−11.08%`: the H0 lever is over-reported by a factor 2.6,
  which is the difference between "κ moves by 2%" and "κ moves by 6%".

Summary line: `A9 COMPLETE: 8/10 checks PASS.` (normal run: `10/10`).

## What the mutation does NOT break

K1, K4–K10 are untouched, as they should be: they do not use `rar_points` with a distance
factor. A mutation that broke everything would be a bad mutation — it would mean the checks
share one code path rather than testing independent claims. K10 in particular still passes
because it is a literature bracket, not a fit; that is a known weakness of K10 and is
declared in `report.md` §"What this does not do".
