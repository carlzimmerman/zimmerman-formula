# Special Relativity

Special relativity is the foundation of modern physics. It unifies space and time into spacetime, and its symmetries (Lorentz invariance) constrain everything from particle physics to string theory.

---

## 1. The Big Picture

### The Speed Limit of the Universe

**Key insight:** The speed of light c is the same for all observers.

This isn't just about light - it's about the structure of spacetime itself.

### Real-World Consequence

GPS satellites travel at ~14,000 km/hr. Without relativistic corrections:
- Clocks would drift by 38 microseconds/day
- Position errors would accumulate at ~10 km/day
- Your GPS would be useless within hours!

**Your phone's GPS IS a daily proof of special relativity.**

---

## 2. The Two Postulates

### Einstein's Postulates (1905)

1. **Relativity Principle:** The laws of physics are the same in all inertial reference frames.

2. **Constancy of Light Speed:** The speed of light c is the same for all observers, regardless of their motion.

### Why These Are Radical

**Everyday intuition:** If you're on a train moving at 50 mph and throw a ball forward at 20 mph, the ball moves at 70 mph relative to the ground.

**Light doesn't work this way:** If you're on a spaceship at 0.5c and shine a flashlight forward, the light STILL moves at c (not 1.5c) relative to the ground!

---

## 3. Time Dilation

### Moving Clocks Run Slow

A clock moving at speed v runs slower by factor γ:

```
Δt_moving = γ Δt_rest

where γ = 1/√(1 - v²/c²) ≥ 1
```

### The Light Clock Visualization

```
Rest frame:              Moving frame:

    ┃   mirror              ╱ mirror
    ┃     ↑               ╱   ↗
    ┃     │ light       ╱   ╱ light travels
    ┃     │ path      ╱   ╱  longer path!
    ┃     ↓         ╱   ╱
    ┃   detector  ╱   ↙
                ╱   detector
                ───────→ v

    Time: t            Time: t√(1 + v²/c²)
```

The light has to travel further → takes more time → moving clock runs slow.

### Real Example: Muons

Cosmic ray muons have a half-life of 1.5 μs. They're created 10 km up in the atmosphere.

**Without relativity:** They should decay before reaching ground.
**With relativity:** They're moving at 0.998c, so γ ≈ 15. Their "clock" runs 15× slower. They reach the ground!

**We detect them every day. Relativity is REAL.**

---

## 4. Length Contraction

### Moving Objects Shrink

An object moving at speed v is contracted in the direction of motion:

```
L_moving = L_rest / γ
```

### Visualization

```
At rest:         ██████████████████████
                 │←─────── L ────────→│

Moving fast:     ██████████
                 │←─ L/γ ─→│
```

### Reciprocity

This is symmetric:
- You see moving objects as contracted
- They see YOU as contracted

Both are right! There's no contradiction because of **relativity of simultaneity**.

---

## 5. Spacetime and 4-Vectors

### The Spacetime Interval

Instead of separate space and time, we have **spacetime**:

```
ds² = -c²dt² + dx² + dy² + dz²
```

This **interval** is the same for all observers!

### Why Minus Sign?

The time part has opposite sign from space parts.

This is what makes spacetime different from ordinary 4D space.

### 4-Vectors

Position: xᵘ = (ct, x, y, z)
Momentum: pᵘ = (E/c, pₓ, pᵧ, pᵤ)
Velocity: uᵘ = γ(c, vₓ, vᵧ, vᵤ)

The "length" of a 4-vector is Lorentz invariant.

---

## 6. Lorentz Transformations

### The Rotation of Spacetime

Just as rotations mix x and y, Lorentz transformations mix t and x:

```
t' = γ(t - vx/c²)
x' = γ(x - vt)
y' = y
z' = z
```

### Matrix Form

```
[ct']   [γ    -βγ   0   0] [ct]
[x' ] = [-βγ   γ    0   0] [x ]
[y' ]   [0     0    1   0] [y ]
[z' ]   [0     0    0   1] [z ]

where β = v/c
```

### Hyperbolic Trig

Define **rapidity** φ by tanh(φ) = v/c. Then:

```
γ = cosh(φ)
βγ = sinh(φ)
```

Lorentz transformations are **hyperbolic rotations** in spacetime!

---

## 7. Energy and Momentum

### The Famous Equation

```
E = mc²
```

More completely:
```
E² = (pc)² + (mc²)²
```

### Rest Mass vs Relativistic Mass

**Rest mass m** is invariant - the same in all frames.

**Energy E = γmc²** includes kinetic energy.

For v << c: E ≈ mc² + ½mv² (rest energy + kinetic energy)

### Massless Particles

For photons (m = 0):
```
E = pc
```

This is why light moves at c - it has no rest mass!

---

## 8. The Light Cone

### Causality Structure

```
                Future
                  △
                 /│\
                / │ \
               /  │  \
              /   │   \  Light cone
             /    │    \
    ────────/─────┼─────\────────
            \     │     /   Elsewhere
             \    │    /   (spacelike)
              \   │   /
               \  │  /
                \ │ /
                 \│/
                  ▽
                Past
```

### Three Regions

1. **Inside the cone (timelike):** Events that can causally influence each other
2. **On the cone (lightlike):** Events connected by light signals
3. **Outside the cone (spacelike):** Events that CANNOT influence each other

### Why This Matters

No information can travel faster than light → cause must precede effect → physics makes sense!

---

## 9. Relativistic Symmetry: The Lorentz Group

### The Group Structure

The **Lorentz group** SO(3,1) consists of:
- Rotations in 3D space (3 generators)
- Boosts (Lorentz transformations) in 3 directions (3 generators)

Total: 6 generators → 6-dimensional group

### Extended: The Poincaré Group

Add spacetime translations → Poincaré group

This is the symmetry group of flat spacetime!

### Why This Matters for Physics

**Every physical law must be Lorentz invariant.**

This constrains:
- The form of Lagrangians
- Allowed particle interactions
- The structure of quantum field theory

---

## 10. Connection to the Z² Framework

### Lorentz Invariance is Essential

The Standard Model is a **Lorentz-invariant quantum field theory**.

The Z² framework:
- Uses Lorentz-invariant actions
- Derives constants that must be frame-independent
- Compactifies extra dimensions while preserving 4D Lorentz symmetry

### The Metric Signature

The Minkowski metric η_μν = diag(-1, +1, +1, +1) appears in:
- The spacetime interval
- The propagator structure
- The ADM decomposition

### Natural Units

In particle physics, we set c = 1:
- Energy and mass have same units (GeV)
- Length and time have same units (GeV⁻¹)

This simplifies everything while keeping Lorentz invariance manifest.

---

## Visualization: The Twins Paradox

### Setup

Twin A stays on Earth.
Twin B travels to a star 4 light-years away at 0.8c, then returns.

### Earth Frame

```
        B travels
        ←───────→
Time:   5 years there + 5 years back = 10 years

Distance: 4 ly each way

Conclusion: A ages 10 years
```

### Traveler Frame

```
γ = 1/√(1 - 0.64) = 1/0.6 = 5/3

Time experienced by B: 10 years × (3/5) = 6 years

Conclusion: B ages only 6 years!
```

### Resolution

When they reunite:
- Twin A (stayed home): aged 10 years
- Twin B (traveled): aged 6 years

**B is genuinely younger!**

The asymmetry comes from B's acceleration (turning around). The situation is NOT symmetric.

---

## Exercises

1. **Time dilation:** An astronaut travels at 0.9c. If 10 years pass on Earth, how much does the astronaut age?

2. **Length contraction:** A 100m spaceship passes Earth at 0.8c. How long does it appear to Earth observers?

3. **Energy:** An electron (m = 0.511 MeV/c²) has kinetic energy 1 MeV. What is its speed?

4. **Light cone:** Event A is at (t=0, x=0). Event B is at (t=1s, x=2×10⁸m). Are they causally connected?

5. **Lorentz boost:** Apply a boost with v=0.6c to the 4-vector (5, 3, 0, 0). What's the result?

---

## Connection to Z² Framework

| SR Concept | Z² Application |
|-----------|----------------|
| Lorentz invariance | All physics must respect this |
| Minkowski metric | Background for field theory |
| 4-momentum | Particle states are 4-vectors |
| Light cone | Causality structure |
| Natural units (c=1) | Simplifies all formulas |
| E = mc² | Mass scales, Planck mass |

---

**Next:** `02_quantum_mechanics.md` - The quantum world.
