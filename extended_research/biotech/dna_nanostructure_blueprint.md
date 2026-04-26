# Track 2: Polymeric Nanoscale Tetrahedron Blueprint

**Project:** Z² Delivery Matrix (DNA Geometry)  
**Scaffold:** M13mp18 (7249 bases)  
**Geometry:** Regular Tetrahedron (Edge length ≈ 30 nm)

## 1. Cadnano Strut Routing Strategy

To fold the 7249-base scaffold into a rigid tetrahedron, we utilize a multi-layer origami approach to ensure stability and precise volumetric containment.

### 1.1 Structural Struts
- **Edge Architecture:** Each of the 6 edges is designed as a 6-helix bundle (6HB) to maximize torsional rigidity.
- **Base Pairs per Edge:** A 30 nm edge corresponds to approximately 88 base pairs (assuming 0.34 nm per base pair).
- **Crossover Mapping:** Scaffold crossovers occur strictly every 21 base pairs (two full turns of the B-form double helix, ~10.5 bp/turn) to neutralize global twist and ensure edge linearity.

### 1.2 Hinge Region Design (Vertices)
To minimize steric strain at the four vertices where three 6HB struts converge:
- **Vertex Flexibility:** Single-stranded scaffold loops (2-4 bases) are intentionally left unpaired at the inner vertex joints. This relieves the extreme dihedral strain of forcing a sharp 60° internal angle (tetrahedral face angle).
- **Staple Exclusion:** No staple strands cross between adjacent edges at the absolute vertex point; instead, struts are interlocked by scaffold routing alone at the vertex, allowing rotational freedom before secondary locking.

### 1.3 The Toehold Displacement Trigger
To enable the conformational shape change (unzipping the cage):
- **Overhang Placement:** On Edge #4, we insert an extended staple strand that does not terminate flush with the helix end.
- **Toehold Specification:** A 15-base single-stranded overhang (Sequence: `5'-ACGTACGTACGTACG-3'` or sequence-optimized for minimal secondary structure) is extended from the 3' end of the staple. 
- **Trigger Mechanism:** This overhang remains exposed to the solvent. When the exact complementary single-stranded target sequence binds to this 15-base toehold, branch migration initiates, peeling the structural staple away from the scaffold and initiating catastrophic strut failure (cage opening).

---

## 2. oxDNA Simulation Parameters (Thermodynamic Testing)

To computationally prove the unzipping mechanism, we model the structure using the coarse-grained oxDNA2 framework.

### 2.1 Standard MD `input` File

```ini
# oxDNA2 Molecular Dynamics Configuration for Toehold Unzipping

backend = CUDA
backend_precision = mixed
interaction_type = DNA2

# Thermodynamic parameters
T = 300K
salt_concentration = 0.5    # 500 mM NaCl to screen electrostatic repulsion
dt = 0.005                  # Integration time step (approx 15 fs)
steps = 10000000            # 10 million steps for conformational sampling

# Thermostat
thermostat = john
newtonian_steps = 103

# Output configuration
trajectory_file = trajectory.dat
info_file = energy.dat
print_energy_every = 10000
print_conf_interval = 10000

# Input files (Assuming compiled topology and relaxed configuration)
topology = tetrahedron.top
conf_file = tetrahedron_relaxed.conf

# External Forces
external_forces = 1
external_forces_file = external_forces.conf
```

### 2.2 `external_forces.conf` (The Pulling Force)

To simulate the toehold-mediated strand displacement, we apply a harmonic spring force between the exposed 15-base overhang and the incoming complementary target sequence, dragging them together.

```json
{
    "type": "mutual_trap",
    "particle": 1450,       // Particle ID of the 5' end of the incoming complementary strand
    "ref_particle": 320,    // Particle ID of the 3' end of the 15-base toehold on the tetrahedron
    "stiff": 1.0,           // Spring stiffness (oxDNA simulation units)
    "r0": 0.5,              // Equilibrium distance (to force base pairing)
    "rate": 0.0001          // Steered MD pull rate (gradually increasing spring force)
}
```

### 2.3 Expected Simulation Outcome
1. **Initial State:** The harmonic trap forces the complementary strand into the immediate proximity of the 15-base toehold.
2. **Branch Migration:** As the simulation progresses, base pairs form along the 15-base toehold (random walk of branch migration).
3. **Displacement:** The structural staple holding Edge #4 together is stripped from the scaffold.
4. **Conformational Change:** The loss of the 6HB integrity on Edge #4 causes the tetrahedron to spring open, exposing the internal cavity.

---

## 3. LEGAL DISCLAIMER (BIOTECH/THERAPEUTICS)

**ALL THERAPEUTIC DESIGNS AND COMPUTATIONAL OUTPUTS ARE PROVIDED FOR THEORETICAL RESEARCH PURPOSES ONLY.**

1. **NOT MEDICAL ADVICE:** This repository and its outputs do not constitute medical advice, diagnosis, or treatment recommendations. No physician-patient relationship is created.
2. **NOT PEER REVIEWED:** Algorithms, designs, and predictions have not undergone formal peer review or regulatory validation (FDA, EMA, etc.).
3. **NO WARRANTY:** All content is provided "AS IS" without warranty of any kind, express or implied, including merchantability, fitness for a particular purpose, or accuracy.
4. **COMPUTATIONAL ONLY:** All therapeutic results are computational predictions. No claims are made regarding in vitro, in vivo, or clinical efficacy or safety. Actual biological behavior may differ substantially.
5. **REGULATORY COMPLIANCE:** Any use for actual drug development must comply with all applicable regulations (IND, GLP, GMP, IRB approval, clinical trial protocols).
6. **ASSUMPTION OF RISK:** Users assume all risks associated with use of this information and derivatives.
7. **INTELLECTUAL PROPERTY:** Users are responsible for ensuring use does not infringe existing patents or IP rights.

**Copyright (c) 2026 Carl Zimmerman. All rights reserved under AGPL-3.0-or-later.**
