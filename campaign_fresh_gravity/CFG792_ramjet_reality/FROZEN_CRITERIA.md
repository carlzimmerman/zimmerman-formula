# CFG792 FROZEN CRITERIA: the hypothetical cold-energy ramjet, stress-tested (committed before any script)

HYPOTHETICAL. CFG791 showed that the kinematics close: α = (η ρ A c²/M) β/(1+β). This lane asks what else the design
must survive. Inputs: ρ_c = 0.01 M☉ pc⁻³, v₀ = 230 km/s, intake 1 g/m². All external numbers are provisional and quoted
from memory.

## Tests
- **F (fuel identity).** The record defines cold energy as "energy carried predominantly as rest mass"
  (MASTER_COLD_ENERGY_EQUATIONS.md line 22), so the available energy density is ρc². The rival field-stress reading
  (CFG660) gives only the field energy g²/8πG, at g = 2×10⁻¹⁰ m s⁻². Report the ratio, and CFG791's α Cen time under
  each reading.
- **N (natural matter).** If the portal is a bulk material property set so that a 1 g/m² column converts the design
  η, then Earth's air above about 100 km (about 3 g/m²) converts the ambient flux ρc²v. The light reaches the ground.
  Compare it with the moonless night-sky illuminance (10⁻³ lux, at 93 lm/W) and with Earth's heat flow (47 TW).
  Classes:
  - excess > 10: a MATERIAL PORTAL is EXCLUDED, and the required suppression in natural matter is reported;
  - otherwise: ALLOWED.
- **S (stimulation).** In-device conversion lifetime τ_dev = (d/v)/η, with d = 0.5 μm (1 g/m² at 2 g/cm³) and
  v = v₀. The stimulation factor over CFG789's spontaneous bound τ ≥ 4.4×10¹⁵ yr is S = τ/τ_dev. Report it.
- **T (thermal).** The waste fraction w (0.01, 0.1, 1) of the ship-frame intake power γ²ρc²vA is radiated from both
  faces (ε = 1). Report the sail temperature at β = 0.1, 0.5, 0.9 and 0.998. Classes: T < 2000 K is OK (carbon);
  above that it is a LIMIT. Also report the directional factor: Lambertian one-sided emission delivers 2/3 of the
  collimated thrust (an η-equivalent).
- **I (interstellar gas).** n = 1 cm⁻³ of protons. Below β_stop they stop in the sail and give drag ρ_ISM v²; above it
  they pass through, depositing Bethe dE/dx × 0.1 mg/cm². Report the ratios drag/thrust and heat_ISM/heat_cold(w=0.01)
  across β. Classes: < 1 everywhere is OK.
- **D (dark-energy conversion, analytic aside).** w = −1 is boost-invariant, so there is no ram effect: converting it
  gives a photon rocket with ambient fuel, thrust P/c, with power set by device volume, not speed.

## Controls
- K1: τ₀ = M/(ηρAc) = 57 d for 1 g/m² at η = 1 (CFG791).
- K2: Bethe formula for a 100 MeV proton in carbon lands within 20% of 6.4 MeV cm²/g (PSTAR, quoted from memory).
- MUTATE: ρ_c → 0 must zero the N excess and the cold heat (output written separately).

κ fitted; not theory closed.
