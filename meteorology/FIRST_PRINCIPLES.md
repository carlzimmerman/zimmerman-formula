# Weather Prediction from First Principles

## The Scientific Method Applied

### 1. OBSERVATION: What Is the System?

The atmosphere is a **thin compressible fluid shell** (~100 km thick) surrounding a
**rotating sphere** (radius R = 6,371 km, angular velocity Ω = 7.292×10⁻⁵ rad/s).

Key observational facts:
- Thickness/Radius ratio: ~1.5% (thin shell approximation valid)
- Rotation period: 24 hours (Coriolis force dominates at large scales)
- Temperature range: ~180K to ~330K (phase transitions matter)
- Pressure range: ~1000 hPa (surface) to ~0.1 hPa (mesosphere)
- Reynolds number: Re ~ 10¹² (highly turbulent)
- Rossby number: Ro ~ 0.1 for synoptic scales (rotation-dominated)

### 2. QUESTION: What Are We Predicting?

**The Forecasting Problem:**
Given the atmospheric state X_t at time t, predict the state X_{t+Δt}.

State vector (at each spatial point):
```
X = {
    T(x,y,z,t)  : Temperature [K]
    u(x,y,z,t)  : Eastward wind [m/s]
    v(x,y,z,t)  : Northward wind [m/s]
    w(x,y,z,t)  : Vertical wind [m/s]
    q(x,y,z,t)  : Specific humidity [kg/kg]
    p(x,y,z,t)  : Pressure [Pa]
    ρ(x,y,z,t)  : Density [kg/m³]
    Φ(x,y,z,t) : Geopotential [m²/s²]
}
```

The evolution operator F:
```
X_{t+Δt} = F(X_t, X_{t-Δt}, boundary_conditions, forcing)
```

**Our task:** Learn F from data while respecting physical constraints.

---

## 3. HYPOTHESIS: The Governing Equations

### 3.1 Fundamental Conservation Laws

These are **non-negotiable** - any valid model must conserve:

**Mass Conservation (Continuity):**
```
∂ρ/∂t + ∇·(ρv) = 0
```

**Momentum Conservation (Navier-Stokes in rotating frame):**
```
∂v/∂t + (v·∇)v = -∇p/ρ - 2Ω×v - g∇z + ν∇²v + F_external
```

Where:
- (v·∇)v : Advection (nonlinear transport)
- -∇p/ρ  : Pressure gradient force
- -2Ω×v  : Coriolis acceleration
- -g∇z   : Gravitational acceleration
- ν∇²v   : Viscous diffusion
- F      : External forcing (radiation, friction)

**Energy Conservation (First Law of Thermodynamics):**
```
ρc_p(∂T/∂t + v·∇T) = -p∇·v + ∇·(k∇T) + Q_radiation + Q_latent
```

**Equation of State (Ideal Gas):**
```
p = ρRT
```

### 3.2 The Primitive Equations (Large-Scale Approximation)

For scales > 10 km, we can make simplifying assumptions:

**Hydrostatic Balance** (vertical momentum):
```
∂p/∂z = -ρg
```
Valid because: vertical accelerations << g for large-scale motions

**Horizontal Momentum:**
```
Du/Dt = -∂Φ/∂x + fv + F_x
Dv/Dt = -∂Φ/∂y - fu + F_y
```
Where f = 2Ω sin(φ) is the Coriolis parameter, φ is latitude.

**Continuity (using pressure coordinates):**
```
∂u/∂x + ∂v/∂y + ∂ω/∂p = 0
```
Where ω = Dp/Dt is the pressure vertical velocity.

**Thermodynamic Equation:**
```
∂T/∂t + v·∇T + ωσ = Q/(c_p)
```
Where σ = -T∂ln(θ)/∂p is the static stability parameter.

### 3.3 Why the Problem is Chaotic

The nonlinear advection term (v·∇)v creates:
1. **Sensitive dependence on initial conditions** (butterfly effect)
2. **Energy cascade** across scales (turbulence)
3. **Limited predictability horizon** (~2 weeks for synoptic scales)

Lorenz (1963) showed even 3-equation truncations exhibit chaos.

---

## 4. THE GEOMETRY PROBLEM: Discretizing a Sphere

### 4.1 Why Latitude-Longitude Fails

A regular lat-lon grid has:
```
dx = R·cos(φ)·dλ  (zonal spacing)
dy = R·dφ         (meridional spacing)
```

**Problems:**
1. **Pole singularity:** As φ → ±90°, dx → 0 (infinite point density)
2. **Anisotropic resolution:** Equator has much coarser effective resolution
3. **CFL condition nightmare:** Tiny dx at poles requires tiny Δt everywhere
4. **Wasted computation:** Most grid points clustered at poles

### 4.2 The Icosahedral Solution

**Platonic Solids and Uniform Sphere Coverage:**

An icosahedron has:
- 12 vertices
- 20 equilateral triangular faces
- 30 edges

**Key property:** All vertices equidistant from center → projects to uniform points on sphere.

**Recursive Refinement:**
1. Start with icosahedron inscribed in unit sphere
2. Subdivide each triangle into 4 smaller triangles
3. Project new vertices onto sphere
4. Repeat n times

After n refinements:
- Nodes: N = 10·4ⁿ + 2
- Faces: F = 20·4ⁿ
- Resolution: ~2πR/(√(10·4ⁿ))

| Level | Nodes | Resolution (km) |
|-------|-------|-----------------|
| 0 | 12 | ~7,000 |
| 1 | 42 | ~3,500 |
| 2 | 162 | ~1,750 |
| 3 | 642 | ~875 |
| 4 | 2,562 | ~440 |
| 5 | 10,242 | ~220 |
| 6 | 40,962 | ~110 |

GraphCast uses level 6 (40,962 nodes) ≈ 0.25° resolution.

### 4.3 Why This Matches the Physics

**Physical Information Propagation:**
- Sound waves: ~340 m/s
- Gravity waves: ~100 m/s
- Rossby waves: ~10 m/s
- Jet stream: ~50 m/s

In Δt = 6 hours, information travels ~2000 km maximum.

**Graph Edges:**
Connect nodes within physical influence distance.
Long-range edges (from coarse mesh levels) allow fast propagation.

---

## 5. WHY GRAPH NEURAL NETWORKS?

### 5.1 PDEs as Message Passing

Consider a discretized Laplacian (heat diffusion):
```
∂T/∂t = α∇²T  →  T_i^{n+1} = T_i^n + α·Δt·Σⱼ (T_j^n - T_i^n)/d_ij²
```

This IS message passing:
- Each node i receives messages from neighbors j
- Messages are weighted by distance
- Node state updates based on aggregated messages

**Navier-Stokes discretization has the same structure.**

### 5.2 The Encode-Process-Decode Architecture

**Physical Interpretation:**

1. **Encoder (Grid → Mesh):**
   - Maps from observation coordinates to computational coordinates
   - Like transforming to characteristic variables in PDEs
   - Learns optimal representation for dynamics

2. **Processor (Mesh → Mesh, repeated):**
   - Simulates time evolution on the mesh
   - Multiple layers = multiple sub-timesteps
   - Long-range edges = implicit large-scale modes

3. **Decoder (Mesh → Grid):**
   - Maps back to observation space
   - Reconstructs physical fields from latent state

**This mirrors spectral methods:**
- Encoder = Forward transform (physical → spectral)
- Processor = Time-stepping in spectral space
- Decoder = Inverse transform (spectral → physical)

---

## 6. PHYSICAL CONSTRAINTS FOR THE LOSS FUNCTION

### 6.1 Latitude-Weighted MSE

The area element on a sphere:
```
dA = R² cos(φ) dφ dλ
```

Unweighted MSE would over-penalize polar errors (high point density).

**Correct loss:**
```
L = Σᵢ wᵢ (y_pred,i - y_true,i)²
where wᵢ = cos(φᵢ) / Σⱼ cos(φⱼ)
```

### 6.2 Conservation Law Penalties

**Mass Conservation Penalty:**
```
L_mass = ||∂ρ/∂t + ∇·(ρv)||²
```

**Energy Conservation Penalty:**
```
L_energy = ||∂E_total/∂t - Q_external||²
```

### 6.3 Physical Bounds

Enforce:
- T > 0 (absolute zero)
- q ≥ 0 (specific humidity non-negative)
- p > 0 (pressure positive)
- Relative humidity ≤ 100% (or allow supersaturation with penalty)

---

## 7. TESTABLE PREDICTIONS

Our model must satisfy:

### 7.1 Necessary Conditions (Must Pass)
1. **Conservation:** Total mass, energy approximately conserved over forecast
2. **Climatology:** Long rollouts should not drift from observed climate
3. **Physical bounds:** No negative temperatures, pressures, humidities
4. **Symmetry:** Forecasts invariant under rotation about Earth's axis

### 7.2 Skill Metrics
1. **RMSE vs ERA5:** Root mean square error against reanalysis
2. **ACC:** Anomaly correlation coefficient (pattern correlation)
3. **CRPS:** Continuous ranked probability score (for probabilistic forecasts)
4. **Extreme events:** Hurricane track error, heat wave detection

### 7.3 Falsification Criteria
The model is **wrong** if:
1. Mass changes by >1% over 10-day forecast
2. Global mean temperature drifts >1K over 10-day forecast
3. Predicts negative absolute humidity anywhere
4. Worse than climatology at any lead time

---

## 8. CONNECTION TO Z² FRAMEWORK

### 8.1 Geometric Constants

The Z² framework identifies fundamental geometric constants:
- Z² = 32π/3 ≈ 33.51 (from Friedmann + horizon thermodynamics)
- Cube × Sphere = 8 × 4π/3

**Atmospheric Analogs:**
- Sphere: Earth's geometry (obviously)
- Cube: 8 vertices ↔ 8 major circulation cells? (2 Hadley + 2 Ferrel + 2 Polar + 2 Walker)

### 8.2 Topological Invariants

Z² framework: Index theorems give N_gen = 3 generations

**Atmospheric analog:**
- 3 primary meridional cells per hemisphere (Hadley, Ferrel, Polar)
- Quantized from angular momentum constraints
- Could there be an "index theorem" for atmospheric circulation modes?

### 8.3 Scale Relationships

Z² framework: α⁻¹ = 4Z² + 3 = 137.04

**Question:** Are there fundamental dimensionless ratios in atmospheric dynamics?
- Rossby number: Ro = U/(fL) ~ 0.1 for synoptic scale
- Ekman number: Ek = ν/(fL²) ~ 10⁻⁶
- Froude number: Fr = U/√(gH) ~ 0.01

The ratios between these might have geometric significance.

### 8.4 Hypothesis to Test

**Conjecture:** The number of dominant EOF modes in atmospheric variability
may be constrained by topological invariants similar to the Z² framework.

If true, we should see:
- Discrete spectrum of variability patterns
- Mode count related to simple geometric numbers
- Cross-scale coupling with specific ratios

---

## 9. IMPLEMENTATION ROADMAP

### Phase 1: Geometry Foundation
1. Implement icosahedral mesh generation from first principles
2. Verify: uniform point distribution, consistent connectivity
3. Implement spherical distance calculations (haversine)
4. Build grid ↔ mesh interpolation

### Phase 2: Graph Structure
1. Define multi-resolution mesh hierarchy
2. Construct edge connections (spatial + multi-scale)
3. Implement efficient graph storage (sparse adjacency)
4. Verify: information can propagate globally in few hops

### Phase 3: Neural Architecture
1. Build encoder: lat-lon grid → mesh features
2. Build processor: message-passing GNN layers
3. Build decoder: mesh features → lat-lon grid
4. Verify: architecture preserves physical dimensions

### Phase 4: Physics Integration
1. Implement latitude-weighted loss
2. Add conservation law penalties
3. Include Coriolis parameter as node feature
4. Verify: trained model approximately conserves mass/energy

### Phase 5: Training & Validation
1. Set up ERA5 data pipeline (Zarr format)
2. Implement autoregressive training loop
3. Train on historical data (1979-2017)
4. Validate on held-out period (2018-2020)

### Phase 6: Analysis
1. Compare to ERA5 reanalysis
2. Analyze conservation properties
3. Study learned representations
4. Look for Z²-related structure in modes

---

## REFERENCES

1. Lorenz, E.N. (1963). Deterministic Nonperiodic Flow. J. Atmos. Sci.
2. Sadourny, R. et al. (1968). Numerical Integration of Primitive Equations on a Sphere.
3. Lam, R. et al. (2023). GraphCast: Learning skillful medium-range global weather forecasting. Science.
4. Bi, K. et al. (2023). Pangu-Weather: Accurate medium-range global weather forecasting. Nature.
5. Pathak, J. et al. (2022). FourCastNet: A Global Data-driven High-resolution Weather Model.

---

*Document created following the scientific method: observation → hypothesis → prediction → experiment*
*Applies first-principles physics to justify architectural choices*
