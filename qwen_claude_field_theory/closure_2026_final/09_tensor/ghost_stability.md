# Phase VI — Ghost / Stability Analysis  (decisive)

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

Phase V found a ghost scalar `b = Φ − ξ` in the (Φ, ξ) bi-scalar sector. This
phase determines whether `b` is a **physical** ghost (couples to the metric,
back-reacts, and makes the theory unstable) or a **decoupled** artifact
(Veneziano-type, removable by boundary conditions).

---

## 1. The localized (Φ, ξ) sector and the ghost field

From the localized action (Phase IV), the (Φ, ξ) sector is
```
S_{Φξ} = ∫ d^4x √(-g)  ξ ( Box Φ - R_{μν} U^μ U^ν ) .
```
Diagonalize with `a = Φ + ξ` (healthy) and `b = Φ − ξ` (ghost):
```
Φ = (a+b)/2 ,   ξ = (a-b)/2 .
```
Substituting and integrating by parts (Box is self-adjoint):
```
S_{Φξ} = ∫ √(-g) [ (1/4) a Box a  −  (1/4) b Box b
                   − (1/2) a R_{uu}  +  (1/2) b R_{uu} ] .
```

### The ghost field `b`

The `b`-sector is
```
S_b = ∫ √(-g) [ − (1/4) b Box b  +  (1/2) b R_{uu} ] .
```
Three properties, all **DERIVED**:

1. **Negative energy (ghost).** The kinetic term is `−(1/4) b Box b =
   −(1/4) ∫ [ (∂_t b)² − (∇b)² ]`. The Hamiltonian (energy) is
   `H_b = −(1/4) ∫ [ (∂_t b)² + (∇b)² ] < 0`. The field `b` has the **wrong
   kinetic sign**: it is a **ghost**.

2. **Coupled to the metric.** The source term `+(1/2) b R_{uu}` means `b` is
   **sourced by the metric curvature** `R_{uu} = R_{μν} U^μ U^ν`. The ghost
   therefore **does not decouple** from the metric sector: it back-reacts on,
   and is sourced by, the gravitational field. This rules out the Veneziano
   (decoupled-ghost) escape.

3. **Massless.** The operator is `Box` (the massless d'Alembertian); there is
   no mass term `m² b`. In vacuum (`R_{uu} = 0`), the EOM is `Box b = 0`, so
   `b` is a **massless** ghost. A massless ghost is an **infrared (IR)
   instability**, not merely a UV one: it affects arbitrarily long distances
   and times, and cannot be removed by a high-energy cutoff.

### The ghost EOM

Varying `S_b` with respect to `b` (Box self-adjoint, boundary terms vanish):
```
−(1/4) Box b + (1/2) R_{uu} = 0     =>     Box b = 2 R_{uu} .
```
The ghost is **directly sourced by the metric curvature**. In vacuum,
`Box b = 0` (massless free ghost); in the presence of matter/curvature,
`b` is forced to respond to `R_{uu}`.

---

## 2. Why the in-in / CTP prescription does NOT remove the ghost

**DERIVED:** Phase III showed that the CTP/in-in prescription fixes the
**integration constant** (the homogeneous solution) of the transport equation
for δM. But the ghost `b` is **not** an integration constant — it is a
**propagating mode** of the (Φ, ξ) bi-scalar, with its own kinetic term and its
own EOM (`Box b = 2 R_{uu}`). The CTP prescription fixes the **initial data**
of `b` (the turning-point matching `b_Δ(t_max) = 0`), but it does **not**
remove the negative-energy mode from the propagator. The ghost remains a
physical, propagating, negative-energy DOF.

**The in-in prescription cures the integration-constant ambiguity (Phase II,
item 5); it does NOT cure the ghost (Phase V, item 5).** These are two distinct
defects, and only the first is fixed by the causal prescription.

---

## 3. Stability verdict

**DERIVED (decisive):** The candidate contains a **massless physical ghost
scalar** `b = Φ − ξ` that:
- has **negative energy** (wrong kinetic sign),
- is **sourced by the metric curvature** `R_{uu}` (does not decouple),
- is **massless** (IR instability, not removable by a UV cutoff).

Consequences:
1. **Vacuum instability.** The negative-energy mode can be excited with
   arbitrarily small energy cost, leading to a runaway (the vacuum decays by
   producing ghost-antighost pairs with net negative energy). The theory has
   **no stable vacuum**.
2. **Acausality / loss of unitarity.** A ghost violates the positivity of the
   Hilbert-space norm, so the theory is **non-unitary**. This is the
   Ostrogradski/ghost instability.
3. **Back-reaction on the metric.** Because `b` is sourced by `R_{uu}`, the
   ghost back-reacts on the metric, corrupting the MOND phenomenology that the
   candidate was designed to produce. The ghost is not a harmless auxiliary
   artifact; it is a **physical** pathology.

**Phase VI verdict: FAIL (physical ghost).** The candidate has a massless
physical ghost. This is a **fatal** instability, independent of the regulator
no-go (Phase I) and the T-gap (Phase II). The theory is **not stable** and
**not unitary**.

---

## 4. Could the ghost be removed? (recorded for completeness)

| Escape | Verdict |
|--------|---------|
| Veneziano decoupling (ghost decouples from matter) | **NO.** `b` is sourced by `R_{uu}` (the metric curvature); it does not decouple. |
| CTP / in-in boundary conditions | **NO.** The prescription fixes the IC, not the propagating negative-energy mode. |
| High-energy (UV) cutoff | **NO.** The ghost is massless (IR); a UV cutoff does not remove it. |
| Adding a mass term `m² b` | **NO.** A massive ghost is still a ghost (negative energy); it only moves the instability to a different scale. (Also not in the frozen candidate.) |
| Replacing `Box^{-1}` by a nonlocal function with a ghost-free kernel | **NOT IN FROZEN CANDIDATE.** This would change the frozen definition of `Φ = Box_ret^{-1} R_{uu}`. Some nonlocal gravity models (e.g. with a specific `f(Box)`) can be ghost-free, but the frozen candidate uses the bare retarded inverse, which is ghostful. |

**No escape within the frozen candidate removes the ghost.**

---

## 5. Summary of Phase VI results

| # | Result | Status |
|---|--------|--------|
| 1 | `b = Φ − ξ` has negative energy (wrong kinetic sign): it is a ghost. | DERIVED |
| 2 | `b` is sourced by the metric curvature `R_{uu}` (`Box b = 2 R_{uu}`): it does not decouple. | DERIVED |
| 3 | `b` is massless (`Box`, no mass term): IR instability, not removable by a UV cutoff. | DERIVED |
| 4 | The CTP/in-in prescription fixes the IC but NOT the propagating ghost mode. | DERIVED |
| 5 | No escape within the frozen candidate removes the ghost. | DERIVED |
| 6 | **The candidate has a massless physical ghost → no stable vacuum, non-unitary.** | DERIVED (decisive) |

**Phase VI verdict: FAIL.** The candidate is **unstable** (physical massless
ghost). This is a fatal defect, independent of all other findings.
