# A56 — mutations

Each mutation is a `--mutate=<name>` flag in `a56_checks.py`. Every one changes **one** premise of the
argument and must break at least one check (exit code 1). Captured output: `a56_MUTATE_<name>.out`.
Clean run: `25/25 PASS`, exit 0, 17 s.

```bash
python3 a56_checks.py                       # 25/25 PASS, exit 0
python3 a56_checks.py --mutate=compton       # exit 1
python3 a56_checks.py --mutate=density_gamma # exit 1
python3 a56_checks.py --mutate=window        # exit 1
python3 a56_checks.py --mutate=alt_a0        # exit 1
python3 a56_checks.py --mutate=notherm       # exit 1
```

| # | mutation | what it changes | checks broken |
|---|---|---|---|
| M1 | `compton` | identifies `L*` with the P Compton length (`L_P := L*`, the √2 dropped) | K3, K4, K7, K14 |
| M2 | `density_gamma` | pretends a density-dependent stiffness is harmless (`extra := 0`) | K8 |
| M3 | `window` | widens A20's measured floor from 24 pc to 10 pc | K4, K13, K14 |
| M4 | `alt_a0` | uses the alt footing everywhere but reports the canonical `sigma_c` | K22 |
| M5 | `notherm` | uses `mu = 1.00` for the 10⁴ K thermal width | K23 |

## M1 `compton` — "L\* is the Compton length"

Sets `L_P = LSTAR`, i.e. `m_P = hbar/(c L*)` instead of `hbar/(c L*/sqrt2)`. Four checks break, which is
the point: the Compton reading is not a harmless relabelling.

```
K3   FAIL residual 0 ; m_P=4.7451e-61 kg ; m_P/H0=1.8514e+08 exactly 0 ; 2.62e8 +- 1%%
K4   FAIL hbar/(m_P c) = 24.0250 pc ; -0.10% below the 24 pc floor < 24 pc by > 25%
K7   FAIL spread over 4 spellings = 4.14e-01       < 1e-6
K14  FAIL 34 lengths, 1 in window ; Compton = 24.025 pc 0 in window
```

`m_P` moves by √2 (4.745e-61 vs 6.711e-61 kg), `m_P/H_0` by √2 (1.851e8 vs 2.618e8), and the four spellings
of (1) no longer agree (spread 0.414 = √2−1). K4 inverts: the mutated "Compton length" is now *above* the
floor, which is exactly the statement that the real Compton length is 29.2 % *below* it.

## M2 `density_gamma` — "gamma may depend on the medium's density"

Forces the extra coefficient in the P equation to zero. This is the mutation that matters for the guard:
if it survived, R2a (density-set `L*`) would be a legitimate reading.

```
K8   FAIL coefficient of p' : gamma_0 + (0)        nonzero for m != 0
```

The true coefficient of `p''` is `gamma_0 + 3 gamma_0 m q/rho_0` for `gamma = gamma_0(1+p'/rho_0)^m` (K8,
sympy). With `m = 0` it is `gamma_0` and the exact first integral `g = g_N + u` follows; with `m != 0` the
stiffness is field-dependent and the first integral is not the same equation. Setting the term to zero is
the only way to keep R2a alive — which is why R2a is a *different action*, not a reading of this one.

## M3 `window` — "the measured window is wider than it is"

Moves the floor from 24 pc to 10 pc, which would admit the Compton length (16.99 pc).

```
K4   FAIL hbar/(m_P c) = 16.9882 pc ; -69.88% below the 10 pc floor < 10 pc by > 25%
K13  FAIL in window: sqrt(gamma/G)=60.22 pc ; gamma normalisations 16.99/24.03/60.22 pc 1 census entry ; 3 of 3 normalisations in window
K14  FAIL 34 lengths, 1 in window ; Compton = 16.988 pc 0 in window
```

Two independent checks catch it: the Compton-length test (K4) and the census tiers (K13, K14). K13's
message also shows the real content of the window: with a 10 pc floor *all three* O(1) normalisations of
`gamma` (16.99 / 24.03 / 60.22 pc) are inside, i.e. the window's width, not its position, is what carries
information — and at 3.75× it carries none about the coefficient (K15b).

## M4 `alt_a0` — "the footing does not matter"

Reports the alt-footing `sigma_c` (9.153 km/s) where the canonical one is required.

```
K22  FAIL sigma_c = 8.330 (can) / 9.153 (alt) km/s ; /8.23 = 1.112 / 1.112   1.012 +- 0.02 ; 1.112 +- 0.02
```

The identity `sigma_c = sqrt(a_0 L*)` is footing-dependent at 20 % (`(1.13/9.36)^{1/2} = 1.099`), and K22 is
the check that the canonical footing lands on the μ = 1.22 thermal width (1.012) while the alt footing lands
on the μ = 1.00 one (1.007, reported separately). Pooling the two footings erases exactly the agreement the
lane claims, so the check has teeth.

## M5 `notherm` — "the thermal width is pure hydrogen on the canonical footing"

Uses `mu = 1.00` at 10⁴ K, i.e. 9.085 km/s instead of 8.226 km/s.

```
K23  FAIL sigma(1e4K,mu=1.00)=9.085 km/s ; L*=28.58 pc (alt 23.67) ; R_core=63.5 pc  8.23 +- 1%% ; L* in [21.6,90] pc
```

`L*` moves from 23.43 to 28.58 pc (+22 %), `R_core` from 52.0 to 63.5 pc. Both are still inside A20's
`[24, 90] pc` window, which is the honest lesson of this mutation: **the window cannot tell μ = 1.00 from
μ = 1.22.** Only the 1.2 % match at fixed μ does, and that is what K23 tests.

## What the mutations collectively show

1. **Every check has a distinct failure mode.** No two mutations break the same set (M2 and M4/M5 break
   exactly one check each; M1 breaks four; M3 breaks three). There is no single knob that turns the whole
   suite red, which is what a suite of independent claims should look like.
2. **The two load-bearing claims are the two most fragile.** K8 (constant `gamma`) and K22/K23 (`sigma_c` from
   the 10⁴ K width) are each broken by a one-line change. That is the correct place for the fragility: they
   are the only two places where the lane says something the action does not already contain.
3. **Nothing in the suite can be repaired by tuning a number.** Every mutation changes a *premise* (a √2, an
   exponent, a floor, a footing, a mass fraction), not a value; no mutation is a rescaling of `L*`.
