# Honest Review: The h_× = 0 Derivation

**Carl Zimmerman | May 2026**

---

## The User's Question

> "How did we get h_× from the geometry?"

This is a crucial question that prompted a careful review of the derivation.

---

## The Existing Derivation (from GW_POLARIZATION_DERIVATION.md)

The document claims h_× = 0 from the following argument:

### Step 1: Z₂ Action on Extra Dimensions
```
The Z₂ orbifold action:
σ: y^i → -y^i    for i = 4, 5, 6 (extra dimensions)
```

### Step 2: Mode Expansion
```
Functions on T³ expand in Fourier modes.
Z₂ projection keeps only even modes (cosine).
```

### Step 3: Polarization Parity (THE KEY CLAIM)
```
h_+ = (h_xx - h_yy)/2  →  "symmetric under π/2 rotation"  →  Z₂-even
h_× = h_xy             →  "antisymmetric under π/2 rotation"  →  Z₂-odd
```

### Step 4: Conclusion
```
Z₂-odd → projected out → h_× = 0
```

---

## Critical Analysis: Where Is The Gap?

### The Problem

The derivation conflates THREE DIFFERENT THINGS:

1. **Z₂ acting on extra dimensions** (y^4, y^5, y^6 → -y^4, -y^5, -y^6)
2. **Parity in 4D spacetime** (x, y, z → -x, -y, -z)
3. **Rotation in the x-y plane** of GW propagation

These are **not the same transformation**.

### The Gap in Logic

The Z₂ orbifold acts on the **extra dimensions**:
```
(y^4, y^5, y^6) → (-y^4, -y^5, -y^6)
```

But the GW polarizations h_+ and h_× are defined in the **4D spacetime** plane perpendicular to propagation:
```
For GW in z-direction:
h_+ defined in x-y plane of 4D spacetime
h_× defined in x-y plane of 4D spacetime
```

**How does a Z₂ acting on (y^4, y^5, y^6) affect the x-y plane of 4D?**

The derivation does not clearly establish this connection.

### What Would Be Needed

To properly derive h_× = 0, we would need:

1. **Full Kaluza-Klein reduction** of 7D graviton to 4D
2. **Identification of how 4D polarizations arise** from 7D components
3. **Analysis of Z₂ action** on each 7D component
4. **Verification that h_×** (specifically the x-y component) is projected out

### The Handwave

The statement:
> "Under rotation by π/2: h_× → -h_×"

Is TRUE for a rotation, but:
- The Z₂ is NOT a rotation in the 4D spacetime
- The Z₂ acts on extra dimensions, not the x-y plane
- The connection between extra-dimensional Z₂ and 4D rotation is not established

---

## Possible Valid Derivations

### Option 1: The Z₂ IS Related to 4D Parity

If the orbifold structure induces a parity transformation in 4D:
```
x → -x (in 4D)
```

Then:
- e^+ (plus tensor) is even under 4D parity
- e^× (cross tensor) is even under 4D parity

**BOTH are even!** (as I showed in my analysis)

So this doesn't give h_× = 0.

### Option 2: Helicity and Orbifold Twist

The two helicity states h = ±2 are related to h_+ and h_×:
```
h_R = (h_+ + i h_×)/√2    (helicity +2)
h_L = (h_+ - i h_×)/√2    (helicity -2)
```

If the orbifold projects out one helicity:
```
Suppose only h = +2 survives.
Then h_R = h_+ + i h_× exists
     h_L = h_+ - i h_× = 0

This gives h_+ = i h_×, not h_× = 0.
```

**This doesn't work either.**

### Option 3: Specific Orbifold Action

Perhaps the specific T³/Z₂ action includes a phase:
```
Z₂: (y) → (-y) with h_× → -h_×
```

This would require the Z₂ to act DIFFERENTLY on the two polarizations.

But the graviton is a single field h_MN. The Z₂ acts on ALL components the same way.

---

## Honest Assessment

### What I Can Say With Confidence

1. **On T³/Z₂ topology**, mode functions are constrained:
   - Even modes (cos) survive
   - Odd modes (sin) are projected for zero mode only

2. **The h_× zero mode is forbidden** (constant h_× field)

3. **Propagating GW with k ≠ 0** can have both polarizations

### What I Cannot Justify

1. **h_× = 0 for all gravitational waves**
2. **The connection between extra-dimensional Z₂ and 4D polarization parity**

### The Status of This Prediction

| Statement | Status |
|-----------|--------|
| h_× zero mode = 0 | VALID |
| h_× = 0 for propagating GW | UNCERTAIN |
| h_× = 0 is exact | NOT ESTABLISHED |

---

## What This Means for Z²

### If h_× = 0 IS Valid (with proper derivation)

- It's a dramatic prediction
- GW170817 would be strong evidence against Z²
- LIGO data could falsify the framework

### If h_× = 0 IS NOT Valid

- Remove this from testable predictions
- GW170817 is no longer relevant
- One major "falsification" is removed

### What Needs to Be Done

1. **Careful Kaluza-Klein reduction** of 7D gravity on T³/Z₂
2. **Analysis of 4D graviton polarization content**
3. **Either establish h_× = 0 rigorously or remove the prediction**

---

## Conclusion

**The user's question exposed a gap in the derivation.**

The existing argument for h_× = 0 conflates:
- Z₂ action on extra dimensions
- Parity in 4D spacetime
- Rotation in the GW propagation plane

A rigorous derivation would need to carefully trace how the extra-dimensional Z₂ action affects the 4D graviton polarizations.

**Until this is done, h_× = 0 should be considered an UNCERTAIN prediction, not a confirmed consequence of the framework.**

---

*This is how science works: when a derivation is questioned, we must either strengthen it or acknowledge its weakness.*
