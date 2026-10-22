# A59 — mutation record

Two mutations, each altering one load-bearing ingredient of the lane's argument.
Both exit 1. Run:

```
python3 a59_checks.py                 # 22/22 PASS, exit 0
python3 a59_checks.py --mutate freeze  > a59_MUTATE_freeze.out   # 15/22, exit 1
python3 a59_checks.py --mutate nolstar > a59_MUTATE_nolstar.out  # 20/22, exit 1
```

---

## 1. `--mutate freeze` — alpha_1 frozen at its galactic value

**What it does.** Replaces `alpha_1(g, r_s)` by the single number `alpha_1(8 kpc) = 0.9277`
in every environment. This is *exactly A36's implicit assumption*: one coefficient, compared
once with one bound.

**What breaks** (7 checks, exit 1):

| check | normal | frozen | why it breaks |
|---|---|---|---|
| K10 (LLR) | `delta r = 6.4e-11 m`, 8.9 dex inside | `delta r = 543 m` vs a 5.3 cm bound | a constant 0.93 at `(w/c)^2` gives a 543 m lunar-range distortion — 4.0 decades *outside* the bound |
| K11 (pulsars) | +18.6 dex | **-4.4 dex** | 0.93 vs 3.5e-5 |
| K12 (wide binary) | `8(r/L*)^2/alpha_1 = 1.000` | 0.000 | the deep-MOND law no longer holds |
| K13 (outer SS) | `alpha_1 = 1.6e-5` | 0.93 | the outer solar system becomes an O(1) environment |
| K16 (the scan) | count = 0 | **count = 4**, min margin -4.65 dex | four environments now have a "test" that excludes the theory |
| K20 (verdict) | True/True/True | True/**False**/False | the verdict flips to EXCLUDED |
| K21 (`eta_N`) | 8.8 dex inside | outside | 0.93 vs 7.2e-5 |

**What it demonstrates.** Under a constant `alpha_1` the theory *is* excluded — by LLR, at
4 decades. So A36's verdict is not a statement about the theory; it is a statement about the
assumption that `alpha_1` is constant. The exclusion lives entirely in the freeze. Since the
theory's own formula makes `alpha_1` a function of `(g, r_s)` (A36 eq. 2.5, verified in K1/K2),
the freeze is not available and the exclusion does not transfer.

---

## 2. `--mutate nolstar` — the coherence screen dropped

**What it does.** Sets `D = 1` in `alpha_1 = 4u'/(D-u')`, i.e. drops the `(k L*)^2 u'/2`
term — the factor that suppresses `alpha_1` for a source smaller than `L*`.

**What breaks** (2 checks, exit 1):

| check | normal | mutated | why |
|---|---|---|---|
| K12 | `alpha_1(20 kAU) = 1.31e-4 = 8(r/L*)^2` | `alpha_1 = 11.9` | without the coherence screen a wide binary is an O(1) environment |
| K13 | `alpha_1(7000 AU) = 1.6e-5` | `alpha_1 = 0.939` | the outer solar system becomes O(1) |

**What it demonstrates.** The `8(r_s/L*)^2` law and the "no test at 7000 AU" statement both
require the coherence factor; it is load-bearing for every small-source environment. Note what
does *not* break: K10 (LLR stays at ~1e-15), because at 1 AU the acceleration screen `u' =
(a0/g)^2 = 2.5e-16` alone is enough. That is why the LLR pass is robust — and why K22
(`alpha_1(1 AU) <= 8/(kL*)^2 = 3.3e-13` for *any* `u'`) is the right way to state it.

---

## 3. What is *not* mutated, and why

- **The bilinearity of the `alpha_1` Lagrangian** (K7). There is no parameter to turn off: it is
  the structure of the PPN `alpha_1` operator. Mutating it would mean replacing the theory's
  `alpha_1` with something that is not `alpha_1`.
- **The published bounds.** They are inputs, verified on disk (`DOOR11_LITERATURE`, `BOUNDS.md`)
  and reproduced by K17 (LLR's 9e-5 ↔ a 5.3 cm lunar range, factor 2.6 from the 2 cm ranging
  precision).
- **A36's numbers.** Reproduced, not varied (K1, K2). The disagreement is about scope, and a
  mutation of A36's arithmetic would test nothing.