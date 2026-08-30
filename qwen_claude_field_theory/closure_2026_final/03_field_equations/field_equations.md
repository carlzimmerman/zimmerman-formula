# Phase VII — Complete Metric Field Equations + Conservation Check

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

We write the complete metric field equation and analyze the **conservation
constraint** `∇^μ E_{μν} = 0` — the crux identified in Phase II.

---

## 1. The field equation

Varying
```
S = (c^3/16πG) ∫ √(-g) [ R - 2Λ - (a_0^2/c^4) M[g] ] + S_m[g, ψ]
```
with respect to `g^{μν}` gives
```
G_{μν} - Λ g_{μν} - (a_0^2/c^4) E_{μν} = (8πG/c^4) T^{(m)}_{μν} ,   (FE)
```
where `E_{μν} = δM/δg^{μν}` is the **nonlocal M-stress tensor** (a causal
integral operator, Phase II/III).

**DERIVED:** `E_{μν}` is nonlocal (it involves retarded Green's functions via
δΦ, δZ and transport integrals via δM). It is a **causal** tensor (depends on
δg only in the past of x, Phase III). It is **not** a local differential
expression in the metric and its derivatives.

---

## 2. The conservation constraint (the crux)

Taking the covariant divergence of `(FE)` and using the contracted Bianchi
identity `∇^μ G_{μν} = 0` (and `∇^μ g_{μν} = 0`):
```
−(a_0^2/c^4) ∇^μ E_{μν} = (8πG/c^4) ∇^μ T^{(m)}_{μν} .
```
For **matter on-shell** (`∇^μ T^{(m)}_{μν} = 0`):
```
∇^μ E_{μν} = 0        (on the full on-shell solution).      (C)
```

### Does `(C)` hold?

**The key question:** is `M[g]` a **diffeomorphism-invariant** scalar
functional? If so, then `E_{μν} = δM/δg^{μν}` is automatically conserved on-shell
(standard Noether/Bianchi argument). If not, `(C)` fails.

**Analysis (DERIVED + UNKNOWN):**

1. The **PDE** defining M — the transport equation
   `∇_μ[√(-g) U^μ (M+F)] = 0` — is diffeomorphism-invariant (all ingredients
   `U, Φ, Z, F` are scalars/covectors built from the metric and T).

2. The **particular solution** of the transport equation (the forced response
   to the source, propagated with the retarded Green's function) is
   diffeomorphism-invariant.

3. The **homogeneous solution** (the integration constant, constant along flow
   lines) is **not automatically diffeomorphism-invariant**: it depends on the
   choice of Cauchy surface / flow labeling. The in-in prescription (Phase III)
   fixes this constant, but the fix is made relative to the CTP contour / a
   Cauchy surface, which is **not** diffeomorphism-invariant in general.

Therefore:
- **On the isolated stationary branch** (`M → -F(Z)` at past infinity, a
  diffeomorphism-invariant IC), `M` is diffeomorphism-invariant and
  **`(C)` holds**.
- **For general time-dependent configurations**, the in-in IC may break
  diffeomorphism invariance, in which case **`(C)` may fail**.

**Status: UNKNOWN in general; holds on the isolated branch.** This is the
crux: the conservation of the nonlocal tensor is **not automatic** and depends
on the diffeomorphism-invariance of the integration-constant prescription.

> **Caveat:** Even if `(C)` holds on the isolated branch, the **ghost** (Phase
> VI) means the theory is unstable regardless. The conservation check is
> necessary but not sufficient.

---

## 3. The full field equation with auxiliary fields

In the localized representation (Phase IV), the field equation becomes a system:
```
G_{μν} - Λ g_{μν} = (8πG/c^4) T^{(m)}_{μν} + (a_0^2/c^4) E_{μν}^{(aux)} ,
Box Φ = R_{μν} U^μ U^ν ,
∇_μ[√(-g) U^μ (M + F(Z))] = 0 ,
∇_μ T ∇^μ T = -1 ,
-κ - ∇_μ U^μ + (F-couplings) = 0   (M algebraic) ,
Box b = 2 R_{uu}   (ghost, Phase VI) .
```
The last line is the **ghost EOM** — the physical pathology.

---

## 4. Summary of Phase VII results

| # | Result | Status |
|---|--------|--------|
| 1 | Field equation: `G_{μν} - Λg_{μν} - (a_0²/c⁴)E_{μν} = (8πG/c⁴)T^{(m)}_{μν}`. | DERIVED |
| 2 | `E_{μν}` is a causal nonlocal (integral) tensor. | DERIVED |
| 3 | Conservation constraint `∇^μ E_{μν} = 0` (matter on-shell). | DERIVED |
| 4 | `(C)` holds on the isolated branch (diffeomorphism-invariant IC); **UNKNOWN for general configurations** (in-in IC may break diffeo invariance). | UNKNOWN (crux) |
| 5 | The ghost EOM `Box b = 2 R_{uu}` is part of the full system (Phase VI pathology). | DERIVED |

**Phase VII verdict:** The field equation is well-defined as a nonlocal system.
The conservation constraint holds on the isolated branch but is **not guaranteed**
in general. Regardless, the **ghost** (Phase VI) makes the theory unstable, so
the field equation describes an **unstable** system.
