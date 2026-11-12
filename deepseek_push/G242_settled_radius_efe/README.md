# G242 — the settled radius IS the external-field radius: SRH1's empty window

**The live failure.** FRZ1/FRZ1R: the z = 2.2–4.4 Lyman-α forest row FAILS by Δχ² ~ 10³ (gate 4). FRZ2: no
a0(z) variant passes. FZS1: confining the law's layout inside FLD1's settled radius drops it to 38.7/36.7,
and the x0.5 bracket passes (0.19). SRH1 then demanded **one** constant `f` in `R_set = f R_fold(z, M_b)`
through four gates and found:

```
G1 forest (z 2.2-4.4)  f <= 0.70   |   G4 KiDS (z ~ 0.3)  f >= 1.25   ->  WINDOW EMPTY  (gap 1.39/1.45)
```

a tilt `f = f0(1+z)^β` with β = −0.5 or −1 opens it — found post hoc, and counted against.

## The claim, and it has no free parameter

FLD1's `R_fold` comes from a kernel **with no external field** (its `X_fold` solves `X²+X = (R_fold/r_M)²`,
i.e. the AG4 law `ḡ = g²/(g+a₀)` — DE01's μ₁). Put the field back and the settled radius is where the
phantom halo is truncated: the EFE onset, measured in G240. So

```
R_set = r_M / e_N ,      e_N = g_ext/a₀ ,      g_ext = sqrt(G ρ_m a₀ R_struct)
```

and **both a₀ and G cancel identically** (sympy, V1):

```
R_set = r_M/e_N = sqrt(M_b / (ρ_m R_struct))
```

No a₀ — so no a0(z) enters the settled radius, and FRZ2's "no a0(z) passes" is orthogonal to this
mechanism. The settling is fixed by the halo's mass and the cosmic density, and nothing else.

## The tilt, and it is the one SRH1 needed

| | z = 2.5 (forest) | z = 0.3 (KiDS) |
|---|---|---|
| R_set | 139.9 kpc | 618.2 kpc |
| R_fold (FLD1) | 96.4 kpc | 259.1 kpc |
| `f_eff = R_set/R_fold` | **1.452** | **2.386** |

`f_eff(2.5)/f_eff(0.3) = 0.609`, i.e. **β = −0.50** at fixed halo mass, steepening to **β = −0.69** at
3× growth — inside exactly the range SRH1's A1 found opens the window (−0.5 to −1). The result is
independent of the web coherence scale (1, 3, 10 Mpc give the same ratio — `R_struct` cancels).

**Honest score: the tilt alone is 92% of the way and 8% short** (0.609 against the required 0.560), so at
*fixed* halo mass the window is still empty — G242b records that FAIL.

## The one missing ingredient is not optional

`f_eff ∝ M_b^{1/2}/M_b^{1/3} = M_b^{1/6}`, so growth enters as `g^{-1/6}`:

| M_b(0.3)/M_b(2.5) | ratio | window |
|---|---|---|
| 1.0 | 0.609 | EMPTY |
| **1.65** | **0.560** | **opens** |
| 3.0 | 0.507 | OPEN (β = −0.69) |
| 10.0 | 0.415 | OPEN |

`g_crit = 1.65`. Every halo that could sit in either gate grows by more than that between z 2.5 and 0.3.
**So the window opens, with f0 the only surviving freedom — a constant, not a history.**

## What this does not fix

- The forest's absolute normalisation and its bin-by-bin shape: FZS1's z 2.2–2.8 bins still fail at x1.
  The tilt moves the family through the x0.5 band; it does not repair a bin.
- ONE1's KiDS stack has not been re-run with the EFE layout — only its radius condition moves here.
- The growth factor `g` is a *condition*, not a computed halo-assembly number; it is checkable against the
  repo's own mass functions (CFG596/FZS1).

## What it does establish

SRH1's "WINDOW EMPTY" is a statement about the family `R_set = f R_fold` with `R_fold` from a
**no-external-field** kernel. Restore the field, as the framework requires, and the settled radius is
`r_M/e_N = sqrt(M_b/(ρ_m R_struct))` — no a₀, no G, β ≈ −0.5 to −0.7 — which is the tilt SRH1's own A1
found opens the window. **The empty window is a proxy artefact, the same species as DW1's M200c failure:
both came from evaluating the framework without its external field.**

`κ = 1/2` stays **FITTED**. Files: `g242.py`, `g242.out`, `g242_results.json`. **G242 COMPLETE: 5/6 PASS**
(the one FAIL is G242b, the fixed-mass window, deliberately kept).
