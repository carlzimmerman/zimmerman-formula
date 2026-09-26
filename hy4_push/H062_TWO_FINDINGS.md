# H062 — TWO FINDINGS: THE n-KAPPA IDENTITY COLLAPSE, AND I7

**Status:** both findings are *logical/interpretive*, established from the repo's own
banked results. Neither required a new physical computation, and neither is claimed
as one. Filed in `hy4_push` per the per-model separation convention.

**Amends:** `hy4_push/H061_RECIPE_AMENDMENT.md` (which withdrew a false kappa
derivation). This file says what survives and adds the one genuinely new rule.

---

## FINDING 1 — **kappa = 1/n is an IDENTITY, and that is why it looked like a derivation**

### The claim that is wrong
"`n = 2` is derived from `D = 4`; since `kappa = 1/n`, `kappa = 1/2` is derived."

### Why it is wrong — the collapse
Define everything in units of `s = c sqrt(G rho_Lambda)`:

```
a_0 = kappa * s                      (definition of kappa)
mu_n(Y) = 1 - (1+Y)^{-n},  Y = g/s   (the mode-count family)
deep limit:  mu_n -> n*Y
MOND:        mu_n * g = g_bar
   =>  n*(g/s)*g = g_bar
   =>  g^2 = (s/n) * g_bar
   =>  a_0 = s/n
   =>  kappa = 1/n                <-- IDENTITY, not a result
```

**So `kappa` and `n` are the same single dial, written two ways.** "n = 2" and
"kappa = 1/2" are the same statement. Nothing is gained by relabelling.

### What this does to the internal contradiction
The repo currently holds two claims that look incompatible:

- `README.md:66` — *"This is a DERIVATION of the value of n from the dimensionality
  of spacetime"* (H017)
- `README.md:126` — *"κ no-go / zero-mode theorem — this class of actions cannot
  derive the a₀–Λ coefficient"*

Given the identity above, **they are not in conflict.** H017's bridge
`D -> nPol(D) = D(D-3)/2 = n` would derive `kappa` only if `D = 4` were derived.
It is **input**. H017 says so itself: *"Closing that 'if' … is the remaining step."*
And `README.md:66` elsewhere: *"Deriving D = 4 from the action is not claimed."*

**So H017 derives a number whose relation to kappa is definitional, from a
dimension that is assumed. It does not touch the no-go.** The earlier "kappa is
derived" reading was an artefact of unit choice — exactly the zero mode the
no-go theorem names.

**Corollary (new):** the no-go's own hypothesis is *"for any FREE interpolating
function."* A kernel **fixed by mode counting is not free** — so the no-go does
not bind it. There is a genuine, named hole: **derive μ (don't fit it), and κ
arrives with it.** That hole is where the remaining work is.

---

## FINDING 2 — **I7, the log-log blindness rule (NEW)**

### Statement
`mu_n(Y) = 1 - (1+Y)^{-n}` is **linear at the origin**, hence

```
d ln mu_n / d ln Y  ->  1     for EVERY n
```

and the mode count sits in the **ordinary** (linear) coefficient:

```
mu_n(Y) = Y * sum_{k<n} q^(k+1),   q = (1+Y)^{-1}
   =>   mu_n'(0) = n
```

### Why it matters
**A log–log fit through the deep-MOND regime is structurally blind to n.** Fit
`ln mu` against `ln Y` and you recover ≈1 regardless of what the theory says. Any
gate that "measures the exponent" this way is a null measurement wearing a result's
clothes.

### Evidence it is not armchair
This lane's **C2 gate FAILED on its first pass for exactly this reason** — it asked
`d ln mu_n / d ln Y -> n`, and the run returned 1. The test was mis-specified, not the
theory. Fix: test the ordinary derivative. Certified at
`mu_eq_Y_mul_sum`, `sum_range_ones_eq_card`, `mu_coeff_n1/n2/n3`; the Python lane's C2
gate now fails correctly when it should.

### Standing instruction
> Write this into the register as a **measurement rule**, not a result. Whoever builds
> the deep-regime gate must test `mu'(0)`, never `d ln mu / d ln Y`.

---

## The door this opens — the exponent gap

Because κ = 1/n is one dial, the two closed fronts now bound the **same** integer:

| Gate | n required | Source |
|---|---|---|
| RAR, 155/175 SPARC curves, 2788 pts | **n = 2** (0.1502 dex) | `README.md:66`, L232 |
| Cassini EFE quadrupole | **n >= 5** (μ₃ fails both halves) | `route1B:240-242,251-255` |

**The intervals are disjoint. No single-kernel μ_n completion has κ = 1/2 and passes
Cassini.**

That is the sharpest currently-open statement in the register, and it is a
*consequence of noticing the identity collapse* — it does not exist anywhere in the
repo as written. The next computation is the joint (Cassini × RAR) exclusion region in
n. **Not yet run.**

---

*Supersedes the retracted kappa claim in `H061_RECIPE_AMENDMENT.md` §0. Does not
delete it.*
