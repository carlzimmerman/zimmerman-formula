# Work-Order H: The AbacusSummit N-Body Kinematic Audit

**Target:** Resolve the 3.8σ Q₄ Hexadecapole tension

**The Physics:** We need to prove that the Q₄ = -0.65 value is a natural consequence of the highly non-linear "Fingers of God" turbulent velocity field caused by our position 13.3° away from the repulsive Vertex #6.

---

## SYSTEM DIRECTIVE: STRICT SYMMETRIC BOUNDARY (NO HALLUCINATION)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  HARD STOP: DO NOT ALTER THE SYMMETRIC 20.6 Gpc BOX                         ║
║  HARD STOP: DO NOT TUNE PARAMETERS TO FIT THE DATA                          ║
║  HARD STOP: IF THE MODEL FAILS, REPORT THE FAILURE                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Locked Parameters (DO NOT MODIFY):**
- L_c = 20.6 Gpc (symmetric cube)
- v = 0.236 (vertex potential strength)
- η = 32π/3 = 33.510 (eta invariant)
- Observer-Vertex #6 angle = 13.3°

---

## Task

Execute an N-Body Kinematic Mock Observation: `research/abacus_audit/q4_vertex_kinematics.py`

---

## Technical Requirements

### 1. Data Ingestion

Load a baseline ΛCDM dark matter halo catalog from the **AbacusSummit** or **Quijote** public simulation suites.

- Box size: ≥ 2 Gpc/h (~2.9 Gpc with h=0.67)
- Use standard cosmology baseline (Planck 2018)
- Download from: https://abacussummit.readthedocs.io/

### 2. Topological Superposition

Mathematically superimpose the M⁴ = ℝ × (T³/Z₂) geometry.

**THE BOX IS STRICTLY SYMMETRIC:**
```python
L_x = 20.6  # Gpc - DO NOT CHANGE
L_y = 20.6  # Gpc - DO NOT CHANGE
L_z = 20.6  # Gpc - DO NOT CHANGE
```

### 3. Vertex Injection (Sub-Box Approach)

Since AbacusSummit boxes are ~2 Gpc, we inject the vertex potential as an external field:

1. Place mock "Earth" observer at box center
2. Inject vertex #6 repulsive potential at angular position θ = 13.3° from observer
3. Use analytical vertex potential:
   ```
   Φ_vertex(r) = v² × exp(-r²/(2σ²))
   where v = 0.236, σ = L_c/4 = 5.15 Gpc
   ```
4. Scale the potential gradient to match the equivalent effect at observer position

### 4. Velocity Evolution

Recalculate the peculiar velocities (RSD) of the halos under the vertex repulsion:

1. Compute gravitational acceleration from vertex potential gradient
2. Add to existing ΛCDM peculiar velocities
3. Evolve to z=0 (or appropriate redshift for comparison)

### 5. The Mock AP Test

Perform the Alcock-Paczyński BAO test from the perspective of the mock observer:

1. Compute 2-point correlation function ξ(s, μ)
2. Decompose into Legendre multipoles: ξ₀, ξ₂, ξ₄
3. Extract Q₄ = (ξ₄/ξ₀)_observed / (ξ₄/ξ₀)_isotropic - 1

---

## Falsification Protocol

Extract the Q₄ hexadecapole from the mock observation.

**SUCCESS CRITERION:**
```
Q₄_simulated = -0.65 ± 0.16 (matching DESI observation)
```

**IF the non-linear velocity shear naturally produces Q₄ ≈ -0.65:**
→ Tension is RESOLVED
→ The symmetric cube + vertex repulsion explains the observation

**IF it does NOT produce Q₄ ≈ -0.65:**
→ Report the FAILURE
→ Report the actual Q₄ value obtained
→ DO NOT invent a new geometry
→ DO NOT change v to force a fit
→ DO NOT propose asymmetric modifications

---

## Output Format

```json
{
  "work_order": "H",
  "target": "Q4_hexadecapole_tension",
  "parameters_locked": {
    "L_c": 20.6,
    "v": 0.236,
    "observer_vertex_angle": 13.3
  },
  "simulation": {
    "box_size_Gpc": "...",
    "n_halos": "...",
    "vertex_injection_method": "external_field"
  },
  "result": {
    "Q4_simulated": "...",
    "Q4_observed": -0.65,
    "Q4_error": 0.16,
    "tension_sigma": "...",
    "status": "RESOLVED | FAILED"
  },
  "verdict": "..."
}
```

---

## References

- AbacusSummit: https://abacussummit.readthedocs.io/
- Quijote Simulations: https://quijote-simulations.readthedocs.io/
- DESI BAO Analysis: https://data.desi.lbl.gov/
