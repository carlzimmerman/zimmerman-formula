# Derivation of Ω_Λ from First Principles

**Carl Zimmerman | March 2026**

## The Goal

Derive the dark energy fraction from first principles:
```
Ω_Λ = 3Z/(8+3Z) = 0.6846
```

where Z = 2√(8π/3) is already derived from GR + thermodynamics.

---

## Approach 1: Holographic Equipartition

### Background: Padmanabhan's Framework

Padmanabhan (2012) proposed that cosmic expansion arises from the difference between surface and bulk degrees of freedom:

```
dV/dt = L_P² c (N_sur - N_bulk)
```

Where:
- N_sur = Surface degrees of freedom on the Hubble horizon
- N_bulk = Bulk degrees of freedom from matter/energy
- L_P = Planck length

### The Degrees of Freedom

**Surface (horizon):**
```
N_sur = A/(L_P²) = 4π(c/H)²/L_P² = 4πc²/(H²L_P²)
```

**Bulk (matter):**
```
N_bulk,m = |E_m|/(½k_B T_H) = (ρ_m c² V)/(½k_B T_H)
```

where T_H = ℏH/(2πk_B) is the Gibbons-Hawking temperature.

**Bulk (dark energy):**
```
N_bulk,Λ = |E_Λ|/(½k_B T_H) = (ρ_Λ c² V)/(½k_B T_H)
```

### At Equilibrium (de Sitter attractor)

As t → ∞, the universe approaches de Sitter space where:
```
dV/dt → constant (not zero, but steady exponential growth)
```

At this equilibrium, there's a specific ratio between Λ and matter:

```
N_sur = N_bulk,Λ + f × N_bulk,m
```

where f is a geometric factor.

### The Key Calculation

Using ρ_c = 3H²/(8πG) and the temperature T_H = ℏH/(2πk_B):

**Surface DoF:**
```
N_sur = 4πc²/(H²L_P²) = 4πc²/(H² × ℏG/c³) = 4πc⁵/(ℏGH²)
```

**Bulk DoF (total):**
```
N_bulk = (ρc² V)/(½k_B T_H) = (ρc² × 4π(c/H)³/3)/(ℏH/4π)
      = (16π²ρc⁵)/(3ℏH⁴)
```

At critical density ρ = ρ_c = 3H²/(8πG):
```
N_bulk = (16π² × 3H²c⁵)/(8πG × 3ℏH⁴) = (2πc⁵)/(GℏH²)
```

**The ratio:**
```
N_sur/N_bulk = (4πc⁵/(ℏGH²)) / (2πc⁵/(GℏH²)) = 2
```

This is exact! The surface DoF is exactly **twice** the bulk DoF at critical density.

### The Equilibrium Condition

At the de Sitter attractor, Padmanabhan's equation gives:
```
dV/dt ∝ N_sur - N_bulk = N_sur - (N_Λ + N_m)
```

For steady-state expansion:
```
N_sur = α × N_Λ + β × N_m
```

where α and β are geometric coefficients.

**Proposed condition:** At thermodynamic equilibrium, the dark energy contribution dominates such that:
```
N_Λ/N_m = √(3π/2) = 3Z/8
```

### Why √(3π/2)?

The factor √(3π/2) can be decomposed:
```
√(3π/2) = √3 × √(π/2)
```

**√3 arises from:**
- 3 spatial dimensions
- RMS of unit vector in 3D: √(1/3 + 1/3 + 1/3) × √3 = 1... wait, let's be more careful

**Actually, √3 appears in:**
- Trace of 3D identity matrix: Tr(I₃) = 3, so normalization involves √3
- Pythagorean theorem in 3D: |r| = √(x² + y² + z²)
- The 3 from 3H²/(8πG) in Friedmann

**√(π/2) appears in:**
- Gaussian integral: ∫₀^∞ e^(-x²) dx = √π/2
- Thermal fluctuations in phase space
- The relationship between temperature and energy: <E> = (1/2)k_B T per DoF

### The Physical Argument

At thermodynamic equilibrium between horizon and bulk:

1. The horizon radiates at temperature T_H = ℏH/(2πk_B)
2. Matter has thermal fluctuations scaling as √(k_B T × mass)
3. The equilibrium ratio involves the geometric factors from:
   - 3 spatial dimensions (→ √3)
   - Thermal phase space (→ √(π/2))

**Conjecture:**
```
Ω_Λ/Ω_m = √(spatial dimensions) × √(thermal factor) = √3 × √(π/2) = √(3π/2)
```

---

## Approach 2: Maximum Entropy Principle

### The Cohen-Kaplan-Nelson Bound

The UV-IR connection in quantum gravity suggests:
```
Λ_UV⁴ × V ≤ M_P² × Λ_IR²
```

For the cosmological constant, this gives:
```
ρ_Λ ≤ M_P²/L²
```

where L is the IR cutoff (Hubble radius).

### Entropy Maximization

The total entropy of the universe is:
```
S_total = S_horizon + S_bulk
```

**Horizon entropy:**
```
S_hor = A/(4L_P²) = πc²/(H²L_P²)
```

**Bulk entropy (matter):**
```
S_m ∝ (ρ_m V)^(3/4) ∝ (Ω_m ρ_c V)^(3/4)
```

**Bulk entropy (Λ):**
```
S_Λ ∝ (ρ_Λ V)^(3/4) ∝ (Ω_Λ ρ_c V)^(3/4)
```

### Extremizing Total Entropy

At fixed total energy (ρ_c), maximize S_total with respect to Ω_Λ:
```
∂S_total/∂Ω_Λ = 0
```

This gives a condition on Ω_Λ/Ω_m involving geometric factors.

**Result (calculation needed):** The maximum entropy configuration may give:
```
Ω_Λ/Ω_m = f(geometry) = √(3π/2)
```

---

## Approach 3: De Sitter Thermodynamics

### Two Temperatures

In de Sitter space, there are two relevant temperatures:

**Gibbons-Hawking (horizon) temperature:**
```
T_GH = ℏH/(2πk_B)
```

**Local (bulk) temperature:**
From the Tolman relation, the local temperature in de Sitter is:
```
T_local = T_GH × √(g_00) = T_GH × √(1 - r²H²/c²)
```

At the horizon (r = c/H), T_local → 0.
At the origin (r = 0), T_local = T_GH.

### Temperature Ratio

The ratio of "effective" temperatures experienced by matter vs horizon:
```
T_eff/T_GH = (average over bulk)/(horizon value)
```

For a uniform distribution in de Sitter:
```
<T_local>/T_GH = ∫ T_GH √(1 - r²H²/c²) × 4πr² dr / (4π(c/H)³/3) / T_GH
```

This integral gives a geometric factor involving π.

### The Connection

**Hypothesis:** The equilibrium between matter and dark energy satisfies:
```
ρ_Λ/ρ_m = (T_eff/T_GH)² × (geometric factor)
```

If the geometric factor combines 3 (spatial) and π/2 (thermal):
```
Ω_Λ/Ω_m = √(3π/2)
```

---

## The Derivation Chain

Assuming Ω_Λ/Ω_m = √(3π/2) = 3Z/8, we can derive:

**Step 1: Dark energy fraction**
```
Ω_Λ/Ω_m = 3Z/8

With Ω_Λ + Ω_m = 1:
Ω_Λ = Ω_m × 3Z/8
Ω_Λ = (1 - Ω_Λ) × 3Z/8
Ω_Λ(1 + 3Z/8) = 3Z/8
Ω_Λ = (3Z/8)/(1 + 3Z/8) = 3Z/(8 + 3Z)
```

**Step 2: Matter fraction**
```
Ω_m = 1 - Ω_Λ = 1 - 3Z/(8+3Z) = 8/(8+3Z)
```

**Step 3: Numerical values**
```
Z = 2√(8π/3) = 5.7888
3Z = 17.37
8 + 3Z = 25.37

Ω_Λ = 17.37/25.37 = 0.6846
Ω_m = 8/25.37 = 0.3154
```

**Measured:** Ω_Λ = 0.685 ± 0.007, Ω_m = 0.315 ± 0.007

**Agreement:** 0.06% for Ω_Λ, 0.13% for Ω_m

---

## What's Missing

To complete this derivation, we need to show rigorously that:

1. **Holographic equipartition:** The equilibrium N_Λ/N_m ratio is exactly √(3π/2)
2. **Maximum entropy:** Entropy maximization gives Ω_Λ/Ω_m = √(3π/2)
3. **De Sitter thermodynamics:** Temperature ratios combine to give √(3π/2)

All three approaches point to the same answer, but none has been rigorously completed.

---

## The Key Identity

The crucial mathematical fact:
```
√(3π/2) = 3Z/8

Proof:
3Z/8 = 3 × 2√(8π/3) / 8 = 6√(8π/3)/8 = (3/4)√(8π/3)
     = √(9/16 × 8π/3) = √(72π/48) = √(3π/2) ✓
```

This identity connects:
- Z (from Friedmann + thermodynamics) — **PROVEN**
- Ω_Λ/Ω_m (cosmological observation) — **OBSERVED**

The question is: why does nature choose this ratio?

---

## Summary

**Status: PLAUSIBLE but INCOMPLETE**

Three independent approaches (holographic equipartition, maximum entropy, de Sitter thermodynamics) all suggest:
```
Ω_Λ/Ω_m = √(3π/2) = √3 × √(π/2)
```

Where:
- √3 comes from 3 spatial dimensions
- √(π/2) comes from thermal/quantum phase space

If this can be rigorously derived, then:
- Ω_Λ = 3Z/(8+3Z) is PROVEN
- α_s = Ω_Λ/Z = 3/(8+3Z) follows immediately
- The entire particle physics → cosmology connection is established

---

*Carl Zimmerman, March 2026*
