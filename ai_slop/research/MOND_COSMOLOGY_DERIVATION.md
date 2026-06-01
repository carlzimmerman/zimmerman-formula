# The MOND-Cosmology Connection

**What Can Actually Be Derived**

**Carl Zimmerman | April 2026**

---

## The Central Mystery

The MOND acceleration scale:
```
a₀ ≈ 1.2 × 10⁻¹⁰ m/s²
```

is numerically close to the cosmic acceleration scale:
```
cH₀ ≈ 6.9 × 10⁻¹⁰ m/s²
```

The ratio:
```
cH₀/a₀ ≈ 5.75
```

This "cosmic coincidence" has been noted by Milgrom (1983) and many others. It's one of the deepest mysteries in physics IF MOND is real.

---

## 1. Verlinde's Approach (2016)

### 1.1 The Idea

Erik Verlinde proposed that gravity is an emergent phenomenon from entropy:
```
F = T × (∂S/∂x)
```

In regions where the entropy is "screened" by dark energy, the effective gravity is modified.

### 1.2 The Derivation

Verlinde derives a MOND-like regime when:
```
a < a_D where a_D = cH₀/C

and C is a constant of order unity
```

His analysis suggests C ≈ 6 based on horizon geometry, giving:
```
a₀ = cH₀/6 ≈ 1.15 × 10⁻¹⁰ m/s²
```

**This matches the observed a₀!**

### 1.3 Where Does the "6" Come From?

In Verlinde's framework:
- The factor involves the "dark energy" equation of state w = -1
- Combined with geometric factors from the horizon
- He gets something like 6 from the holographic analysis

**But the exact derivation of "6" is not universally agreed upon.**

---

## 2. My Attempt at Rigorous Derivation

### 2.1 Setup

Consider a cosmological horizon at distance r_H = c/H.

The entropy within the horizon:
```
S = πr_H²/l_Pl² = πc²/(H²l_Pl²) = πM_Pl²c²/H²
```

The mass-energy within:
```
M = ρ × V = (3H²c²/(8πG)) × (4πr_H³/3)
  = (3H²c²/(8πG)) × (4πc³/(3H³))
  = c⁵/(2GH)
  = M_Pl²c²/(2H)
```

### 2.2 Temperature and Acceleration

The Unruh temperature for an accelerating observer:
```
T_U = ℏa/(2πck_B)
```

The Hawking temperature of the cosmological horizon:
```
T_H = ℏH/(2πk_B) = ℏcH/(2πck_B)
```

**Question:** At what acceleration does T_U = T_H?
```
ℏa/(2πck_B) = ℏH/(2πk_B)
a = cH
```

So a = cH is the acceleration at which Unruh and Hawking temperatures match.

### 2.3 The Factor

But a₀ ≈ cH/6, not cH. Where does the factor of 6 come from?

**Attempt 1: Geometric Factor**

The horizon is a 2-sphere. The ratio of surface area to enclosed volume:
```
A/V = 4πr²/(4πr³/3) = 3/r
```

For the horizon:
```
A/V = 3H/c
```

This gives a factor of 3, not 6.

**Attempt 2: Degrees of Freedom**

If the MOND transition involves matter degrees of freedom:
```
DoF_matter = 3 generations × 2 chiralities = 6
```

Then:
```
a₀ = cH/(DoF_matter) = cH/6
```

**This gives the right factor!**

But this is NUMEROLOGY unless we can show WHY matter DoF enter the formula.

### 2.4 Verlinde-Style Argument

In Verlinde's emergent gravity, the entropy of matter is "diluted" by dark energy:
```
a_effective = a_Newton × (1 - S_DE/S_total)
```

Near the MOND transition, the screening effect kicks in when:
```
a ≈ cH × (entropy factors)
```

The entropy of dark energy vs matter involves their relative DoF:
```
DoF_DE/DoF_matter = 13/6 (from our earlier analysis)
```

This could explain why the transition happens at a ≈ cH/6 rather than cH.

**But this argument is hand-wavy and needs rigorous derivation.**

---

## 3. What Can Be Rigorously Derived?

### 3.1 The Equality a = cH

**DERIVABLE:** The scale a = cH emerges from:
```
Unruh temperature = Hawking temperature of horizon
```

This is legitimate physics. At a = cH, quantum effects from acceleration match quantum effects from the cosmological horizon.

### 3.2 The Factor of ~6

**NOT RIGOROUSLY DERIVED.** Attempts include:
- Verlinde's entropy screening (factor comes from geometry)
- DoF counting (factor = matter DoF = 6)
- Holographic arguments

But none of these are rigorous derivations. They're plausibility arguments.

### 3.3 Why Z² = 32π/3?

If a₀ = cH/Z with Z² = 32π/3, then:
```
Z² = 32π/3 = (32/3)π

Z = √(32π/3) = √(32/3) × √π = (4√2/√3) × √π
  = 4√(2π/3)
```

Alternatively:
```
Z² = 32π/3 = (8π/3) × 4 = (8π/3) × BEKENSTEIN
```

Where does 8π/3 come from?

The Friedmann equation has:
```
H² = 8πGρ/3
```

So:
```
Z² = (8π/3) × 4 = coefficient of Friedmann × 4
```

**This is interesting!** The Z² involves the Friedmann coefficient 8π/3.

### 3.4 The "4" Factor

If Z² = (8π/3) × 4, where does the 4 come from?

Possibilities:
- 4 = number of spacetime dimensions
- 4 = factor from Bekenstein-Hawking (A/4G)
- 4 = geometric factor

**The most natural interpretation:**
```
Z² = (8π/3) × 4 = (Friedmann coefficient) × (BH entropy factor)

Z² = (8πG/3) × (1/4G) × M_Pl⁴/... hmm, units don't work
```

Let me try again:
```
Friedmann: H² = (8πG/3)ρ

Define: ρ_crit = 3H²/(8πG)

Then: ρ = ρ_crit exactly (for flat universe)

The factor 8π/3 relates H to ρ through G.

Z² = 32π/3 = 4 × (8π/3)

The extra factor of 4 connects to... the Bekenstein bound?
```

---

## 4. Attempting a Clean Derivation

### 4.1 Starting Point

Take the Friedmann equation for a flat universe:
```
H² = 8πGρ/3
```

And the Bekenstein entropy of the horizon:
```
S = A/(4G) = 4πr_H²/(4G) = πr_H²/G = πc²/(GH²)
```

### 4.2 A Key Ratio

Compute:
```
S × H²/c² = π/G = πM_Pl²

This is just the Planck entropy scale.
```

Now, what if we ask: at what acceleration does the entropy per unit area equal the Planck scale?

The "entropy per unit acceleration" from Unruh:
```
For acceleration a, the Unruh temperature is T = ℏa/(2πk_Bc)
The entropy scales with T², so S_Unruh ~ a²
```

This is getting complicated. Let me try a different approach.

### 4.3 Dimensional Analysis

We have:
- c (speed of light)
- H (Hubble parameter)
- G (Newton's constant)
- ℏ (Planck's constant)

From these we can form:
```
Acceleration: cH (the only combination with units of acceleration using just c and H)
Length: c/H
Time: 1/H
Mass: c³/(GH) = M_H (Hubble mass)
Energy: c⁵/(GH)
```

The question: Why is a₀ = cH/6 and not cH?

**The factor of 6 must come from counting something.**

### 4.4 What Could "6" Count?

Options:
1. **Spatial dimensions:** 6 = 2 × 3 (three spatial dimensions, two polarizations?)
2. **Faces of cube:** 6 (but why a cube?)
3. **Matter degrees of freedom:** 6 = 3 generations × 2 chiralities
4. **Something geometric:** related to solid angle, 4π steradians?

None of these is a DERIVATION.

---

## 5. The Honest Conclusion

### What Is Actually Derived:

1. **The scale a ~ cH is natural** from Unruh-Hawking temperature matching

2. **Z² = 32π/3 fits the data** when Z = cH/a₀

3. **Z² = 4 × (8π/3) = 4 × (Friedmann coefficient)** is a nice factorization

### What Is NOT Derived:

1. **Why a₀ = cH/Z instead of a₀ = cH**

2. **Why Z ≈ 6 (or more precisely √(32π/3))**

3. **The physical meaning of the factor 4 in Z² = 4 × (8π/3)**

### The Real Derivation Task:

To make this real physics, we need to show:
```
Starting from:
- General Relativity (Friedmann equation)
- Quantum mechanics (Unruh/Hawking effects)
- Statistical mechanics (entropy)

Derive WITHOUT fitting:
- a₀ = cH₀/Z
- Z² = 32π/3 exactly
```

**This has not been done.**

---

## 6. What We Can Honestly Claim

### Strong Claim:
```
The MOND acceleration scale a₀ ≈ cH₀ is not a coincidence.
The scales are related through fundamental physics.
```

Evidence: Both scales involve the cosmological horizon.

### Weaker Claim:
```
The precise numerical factor Z = √(32π/3) ≈ 5.79
connecting a₀ = cH₀/Z may have deep significance.
```

Evidence: Z² = 32π/3 = 4 × (8π/3) involves the Friedmann coefficient.

### Speculation:
```
If Z determines a₀, maybe Z determines other constants too.
```

Status: Numerological patterns exist but are not derived.

---

## 7. Summary

| Statement | Status |
|-----------|--------|
| a₀ ∝ cH₀ | OBSERVED (Milgrom 1983) |
| a ∼ cH from Unruh-Hawking | DERIVABLE |
| Z² = 32π/3 exactly | FIT to observations |
| Z² = 4 × (Friedmann coefficient) | INTERESTING PATTERN |
| Why a₀ = cH/Z (not cH) | NOT DERIVED |
| Connections to α, masses, etc. | NUMEROLOGY |

**The framework has ONE legitimate derivation (a ∼ cH from temperature matching) and ONE interesting numerical pattern (Z² = 4 × 8π/3). Everything else is fitting.**

---

*MOND-Cosmology derivation assessment*
*Carl Zimmerman, April 2026*
