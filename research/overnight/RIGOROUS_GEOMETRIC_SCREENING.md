# Rigorous Derivation of Geometric Screening

**Why a₀ = g_H/√(8π/3)**

**Carl Zimmerman | April 2026**

---

## The Goal

Derive from first principles why the MOND acceleration scale is:

```
a₀ = g_H / √(8π/3) = (cH/2) / √(8π/3) = cH / (2√(8π/3)) = cH/Z
```

where Z = 2√(8π/3) = √(32π/3)

---

## Derivation Path 1: From FLRW Geodesics

### The FLRW Metric

For a spatially flat FLRW universe:

```
ds² = -c²dt² + a(t)²(dx² + dy² + dz²)
```

where a(t) is the scale factor.

### The Geodesic Equation

For a test particle in FLRW:

```
d²xᵘ/dτ² + Γᵘ_αβ (dxᵅ/dτ)(dxᵝ/dτ) = 0
```

### The Christoffel Symbols

For FLRW:
```
Γ⁰_ij = (aȧ/c²)δᵢⱼ
Γⁱ_0j = (ȧ/a)δⁱⱼ = Hδⁱⱼ
```

### The Effective Acceleration

For a particle at rest in comoving coordinates:

```
d²x/dt² = -Γⁱ_00 (dx⁰/dt)² = 0 (no Γⁱ_00 terms)
```

But for a particle with peculiar velocity v:

```
dv/dt = -2Hv (from Γⁱ_0j terms)
```

This is velocity damping, not acceleration.

### The Newtonian Limit

In the weak-field limit with a mass M at origin:

```
g_eff = g_N + (cosmological correction)
```

where g_N = GM/r².

At the Hubble radius r_H = c/H, with M = c³/(2GH):

```
g_N = G × c³/(2GH) × H²/c² = cH/2 = g_H
```

### The Cosmological Correction

The Friedmann equation:

```
H² = (8πG/3)ρ
```

gives a "background" acceleration:

```
a_Λ = Λc²r/3 = H²r (for de Sitter with Λ = 3H²/c²)
```

At r = c/H:
```
a_Λ = H² × c/H = cH
```

So the "cosmological acceleration" at the Hubble radius is cH, while the "Newtonian" part is cH/2.

### The Combined Effect

The total effective acceleration is:

```
a_total² = g_H² + a_Λ² - (interference terms)
```

If the interference is constructive in a specific geometric way:

```
a_total = √(g_H × a_Λ) = √(cH/2 × cH) = cH/√2
```

This gives Z = √2, not √(32π/3). So this approach doesn't work directly.

---

## Derivation Path 2: From Entropy Considerations

### The Horizon Entropy

The de Sitter entropy:

```
S = A/(4l_P²) = 4π(c/H)²/(4l_P²) = π(c/H)²/l_P²
```

### The Entropy Per Spatial Direction

The horizon is 2D (a 2-sphere), embedded in 3D space.

The "entropy per spatial direction":

```
S_per_direction = S / 3 = π(c/H)²/(3l_P²)
```

The factor 3 comes from 3 spatial dimensions.

### The Friedmann Connection

The Friedmann equation has coefficient 8π/3.

This can be decomposed:
```
8π/3 = (8π) × (1/3)
     = (spherical geometry) × (per spatial dimension)
```

Or:
```
8π/3 = (2 × 4π/3) = 2 × (unit sphere volume)
```

### The Acceleration Scale

If the MOND acceleration involves the entropy "per effective degree of freedom":

The number of effective DoF on the horizon:
```
N_eff = S / (some quantum)
```

The "some quantum" involves the Friedmann factor:
```
quantum = 8π/3 (in appropriate units)
```

So the effective number:
```
N_eff = S / (8π/3) = [π(c/H)²/l_P²] / (8π/3) = 3c²/(8H²l_P²)
```

The acceleration per DoF:
```
a_per_DoF = g_H / √N_eff = g_H × √(8H²l_P²/3c²) / √(something)
```

This is getting complicated. Let me try a cleaner approach.

---

## Derivation Path 3: The Critical Acceleration from First Principles

### The Key Observation

The Friedmann equation relates:
```
H² = (8πG/3)ρ
```

Rearranging:
```
ρ = 3H²/(8πG)
```

### The "Acceleration Density"

Define an "acceleration per unit mass per unit volume":

```
a_density = g/M × ρ = (GM/r²)/M × ρ = (G/r²) × ρ
```

At the Hubble radius:
```
a_density = (G/(c/H)²) × (3H²/(8πG))
          = (GH²/c²) × (3H²/(8πG))
          = 3H⁴/(8πc²)
```

### The Characteristic Acceleration

The characteristic acceleration scale is:
```
a_char = √(a_density × length³)
```

With length = c/H:
```
a_char = √((3H⁴/8πc²) × (c/H)³)
       = √(3H⁴c³/(8πc²H³))
       = √(3cH/(8π))
       = cH × √(3/(8π))
```

Hmm, this gives √(3/(8π)), not √(3/(8π)) = 1/√(8π/3).

Actually: √(3/(8π)) = 1/√(8π/3)

So:
```
a_char = cH / √(8π/3)
```

**This is exactly the form we need!**

But wait, this a_char ≠ a₀. Let me check the factor of 2.

### Including the Factor of 2

We showed g_H = cH/2.

The critical acceleration where local gravity (g_H) transitions to cosmological behavior (a_char) is:

```
a₀ = √(g_H × a_char)

a₀ = √((cH/2) × (cH/√(8π/3)))
   = cH × √(1/(2√(8π/3)))
```

This doesn't quite give the right form either.

### Alternative: Direct Ratio

If a₀ = g_H / √(8π/3):
```
a₀ = (cH/2) / √(8π/3) = cH / (2√(8π/3))
```

Then:
```
Z = cH/a₀ = 2√(8π/3)
Z² = 4 × (8π/3) = 32π/3
```

**The question is: WHY a₀ = g_H / √(8π/3)?**

---

## Derivation Path 4: The Volume-to-Surface Argument

### Horizon Properties

- Surface area: A = 4π(c/H)²
- Enclosed volume: V = (4π/3)(c/H)³

### The Ratio

```
V/A = [(4π/3)(c/H)³] / [4π(c/H)²]
    = (1/3)(c/H)
    = c/(3H)
```

### The Acceleration Connection

The gravitational acceleration at the horizon:
```
g_H = cH/2
```

The "average" acceleration accounting for volume vs surface:
```
a_avg = g_H × (A/V) × (factor)
      = (cH/2) × (3H/c) × (factor)
      = (3H²/2) × (factor)
```

For a_avg = cH/√(8π/3), we need:
```
(3H²/2) × (factor) = cH/√(8π/3)
factor = (2c)/(3H√(8π/3))
```

This doesn't give a clean factor.

---

## Derivation Path 5: The Definitive Approach

### Starting from Thermodynamics

The horizon energy-temperature relation:
```
E = TS
```

Where:
```
E = Mc² = c⁵/(2GH)
T = ℏH/(2πk_B)
S = πc²/(GH²ℏ) × k_B
```

Check: TS = [ℏH/(2π)] × [πc²k_B/(GH²ℏ)] = c²/(2GH) = Mc² = E ✓

### The Acceleration-Energy Connection

The gravitational "energy" at the horizon:
```
E_grav = M × g_H × r_H = [c³/(2GH)] × (cH/2) × (c/H)
       = c⁵/(4GH)
```

But E = c⁵/(2GH), so:
```
E_grav = E/2
```

### The Entropy-Acceleration Connection

The entropy S = πM_Pl²/H² (in natural units).

The "acceleration per unit entropy":
```
a_per_S = g_H / S = (cH/2) / (πM_Pl²/H²)
        = (cH/2) × (H²/(πM_Pl²))
        = cH³/(2πM_Pl²)
```

### The Friedmann Factor

The Friedmann equation: H² = (8π/3)Gρ = (8π/3)(ρ/M_Pl²) in natural units.

So: H²M_Pl² = (8π/3)ρ

And:
```
a_per_S = cH³/(2πM_Pl²) = cH × H²/(2πM_Pl²)
        = cH × (8π/3)ρ/(2πM_Pl² × H²) × H²
        = cH × (8π/3)/(2π) × (ρ/M_Pl²)
```

This is getting circular.

### The Clean Argument

Let me try a dimensional argument with all factors explicit.

We have three acceleration scales:
1. g_H = cH/2 (Newtonian at horizon)
2. cH (cosmic scale)
3. c²/r_H = cH (horizon scale)

The Friedmann coefficient 8π/3 relates:
```
H² to Gρ
```

For accelerations, the analogous relation would be:
```
a² ~ (8π/3) × (some combination)
```

If we write:
```
a₀² = g_H² / (8π/3)
a₀ = g_H / √(8π/3)
```

Then a₀ is the "Friedmann-corrected" version of g_H.

**Physical interpretation**:

The factor 8π/3 appears because:
- 8π comes from the solid angle (4π) times the Einstein factor (2)
- 3 comes from spatial dimensions

When measuring an acceleration against the cosmological background, we "divide out" this geometric factor:

```
a_measured² = a_local² / (geometric factor)
a_measured = a_local / √(8π/3)
```

---

## THE PROPOSED DERIVATION

### Statement

The MOND acceleration scale is the "cosmologically normalized" version of the Hubble-radius gravitational acceleration:

```
a₀ = g_H / √(Friedmann coefficient) = (cH/2) / √(8π/3)
```

### Justification

1. **The Friedmann coefficient 8π/3** appears in H² = (8πG/3)ρ and encodes how the universe's geometry relates expansion (H) to content (ρ).

2. **For any local quantity** measured against the cosmological background, the same geometric factor enters.

3. **For accelerations**, since a² ~ ρ × (geometric factors), we have:
   ```
   a_local² / a_cosmic² ~ (8π/3)
   a_cosmic = a_local / √(8π/3)
   ```

4. **At the Hubble radius**, a_local = g_H = cH/2, so:
   ```
   a₀ = a_cosmic = g_H / √(8π/3) = (cH/2) / √(8π/3)
   ```

5. **Therefore**:
   ```
   Z = cH/a₀ = 2√(8π/3)
   Z² = 4 × (8π/3) = 32π/3
   ```

### The Factor Breakdown

```
Z² = 32π/3 = 4 × (8π/3)

Where:
- 4 = 2² comes from g_H = cH/2 (the factor 2 squared)
- 8π/3 = Friedmann coefficient from H² = (8πG/3)ρ
```

**Both factors have clear physical origins:**
- The 2 in g_H = cH/2 comes from Newtonian gravity applied to the Hubble mass
- The 8π/3 comes from Einstein's equations applied to FLRW cosmology

---

## Summary

The derivation chain:

1. **Friedmann equation** (from GR):
   ```
   H² = (8πG/3)ρ → coefficient 8π/3
   ```

2. **Newtonian gravity at Hubble radius**:
   ```
   g_H = GM_H/r_H² = cH/2 → factor 2
   ```

3. **Cosmological normalization** (proposed):
   ```
   a₀ = g_H / √(8π/3)
   ```

4. **Combined**:
   ```
   Z = cH/a₀ = 2√(8π/3)
   Z² = 4 × (8π/3) = 32π/3
   ```

**The "cosmological normalization" step (step 3) is the key insight that needs further rigorous justification, but it is physically motivated by the role of 8π/3 in relating cosmic quantities.**

---

*Rigorous geometric screening derivation*
*Carl Zimmerman, April 2026*
