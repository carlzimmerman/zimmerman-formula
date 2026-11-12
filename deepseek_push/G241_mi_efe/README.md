# G241 — which EFE is the framework's? Modified inertia derived

**The question the chain left open.** DW1 → G239 → G240 ended with the Milky Way's virial mass at 5.3×10¹¹
(QUMOND's EFE) or 1.33×10¹² (AQUAL's) and no principle for choosing. This lane derives the EFE of the
completion the framework *claims* — modified inertia (`a0kit/a0kit.py`: "a modified-inertia (not
modified-gravity) completion") — and then asks whether the framework can actually be MI.

## The derivation, and it is one line

MI's equation of motion puts the interpolating function on the **acceleration of the body**, not on the field:

```
μ(|a|/a₀) a = F/m = g_N            (Milgrom 1994)
```

A star in the Galaxy's field plus a uniform external field sees `g_N = g_b + g_ext`, so
`a = ν(|g_b + g_ext|/a₀)(g_b + g_ext)` with `ν(y) = x/μ(x)`, `y = xμ(x)`. **That is identically QUMOND's
prescription** — sympy: `1/μ(x) − x/y` at `y = xμ(x)` is `0` for an *abstract* μ, and the a0-line kernel
reproduces it to 4×10⁻¹⁶ (V1, V1b). So **G239's angle average, its plateau and its −2.8σ M200c are the
modified-inertia numbers**, not a QUMOND curiosity (V2: identical to machine precision).

## But the framework is not modified inertia

| at 200 kpc | M_lens | M_dyn |
|---|---|---|
| MI (darkness is inertia) | 6.7×10¹⁰ (the baryons) | 5.3×10¹¹ |
| scalar (darkness is T^φ) | = M_dyn | 5.3×10¹¹ (MI-EFE) / 1.33×10¹² (field-EFE) |

Pure MI predicts a **lensing mass equal to the baryonic mass at every radius** — 8× below the dynamical
mass at 200 kpc. The lensing RAR (the repository's own zero-parameter test) shows the same boost as the
rotation curves. So pure MI is **excluded**, the framework's dark sector must be a **field**, and its own
stated ontology ("the dark mass IS the scalar's stress-energy") says the same thing.

## Which decides the EFE, and closes the chain

| prediction | M(<80 kpc) | M(<200 kpc) |
|---|---|---|
| MI / algebraic EFE | 4.98 (−2.8σ) / 5.11 (−2.5σ) | 0.53×10¹² (−5.1σ) |
| **field / AQUAL-like EFE** | **5.83 (−1.1σ) / 6.15 (−0.4σ)** | **1.33×10¹² (+1.0σ) / 1.48 (+2.2σ)** |
| DESI DR2 III | 6.36 ± 0.50 | 1.19 ± 0.13 |

**DESI's M200c chooses between the two completions at 2.5× separation: 5.1σ from MI, 1.1σ from the field
reading.** And even the 80 kpc amplitude leans the same way (−1.1σ vs −2.8σ). The chain resolves:

> DW1 found the completion ambiguity, G239 made it quantitative, G240 measured it, G241 says which side the
> framework is on. **M200c = 1.33×10¹² (+1.0σ) is the framework's prediction; the "failure" was the wrong
> completion's EFE.**

## The cost, stated as plainly as the gain

With the field EFE the MW mass does not plateau inside the virial radius (G240: it keeps rising to
~1.4×10¹² at 200–400 kpc), so **"the mass stops at ~6×10¹¹" — the framework's most distinctive MW
signature — is gone.** FALSIFIER_MATRIX row 32 stands on the shape test only:
`γ(100–200 kpc) = −2.03` against NFW `−2.39`, kill if a measured γ ≤ −2.25.

What the framework now passes, with nothing fitted except the one amplitude: M(<80 kpc) at −1.1/−0.4σ, the
13-point 20–80 kpc shape at χ²/dof 0.26 (rms 2.9%), the amplitude `A* = 1.33 ± 0.04` agreeing with item 35's
outer rotation curve at 0.45σ, and M200c at +1.0/+2.2σ.

## The honest residue is a library relabelling, not new physics

`a0kit` calls the completion "modified inertia" and derives its kernels that way. That **language** is now
excluded by lensing and by the framework's own scalar ontology. The kernels remain correct *as algebra*
(ν, the a0-line, the a0 value); what must be re-labelled is the completion — a scalar-tensor with a
nonlinear Poisson limit, whose EFE is the field's. Recorded here; the relabelling is bookkeeping.

`κ = 1/2` stays **FITTED**. Files: `g241.py`, `g241.out`, `g241_results.json`. `G241 COMPLETE: 6/6 checks PASS.`
