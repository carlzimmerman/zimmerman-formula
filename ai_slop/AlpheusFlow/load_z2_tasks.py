#!/usr/bin/env python3
"""
LOAD Z² DERIVATION TASKS - 50 Universal Constants
==================================================

Loads all 50 Z² constant derivation tasks across 6 categories:
1. Chaos Theory & Fluid Dynamics (5 tasks)
2. Condensed Matter & Lattice Physics (10 tasks)
3. Nuclear & Subatomic Geometries (10 tasks)
4. Astrophysics & Planetary Geometry (10 tasks)
5. Complex Systems, Network Theory & Biology (10 tasks)
6. Material Limits & Boundary Conditions (5 tasks)

Author: Carl Zimmerman
Date: May 5, 2026
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from AlpheusFlow.queue import ResearchQueue, ResearchTask, TaskPriority, create_derivation_task

# =============================================================================
# CATEGORY 1: CHAOS THEORY & FLUID DYNAMICS SCALING (5 tasks)
# =============================================================================

CHAOS_TASKS = [
    {
        "target": "von Karman Constant",
        "value": 0.41,
        "assignment": "In fluid dynamics, the logarithmic velocity profile of turbulent flow near a boundary is governed by the von Karman constant, empirically measured near 0.41. Using strictly the Z-Squared Framework's dimensional reduction from a 3D bulk to a 2D surface, geometrically derive why fluid turbulence hitting a physical boundary locks into this exact geometric scaling factor."
    },
    {
        "target": "Feigenbaum Delta",
        "value": 4.669,
        "assignment": "In chaos theory, the bifurcation of non-linear systems approaches chaos at a universal rate of 4.669. Using the Z-Squared cubic tessellation geometry, prove computationally why geometric folding in phase space mandates this exact chaotic boundary ratio."
    },
    {
        "target": "Feigenbaum Alpha",
        "value": 2.502,
        "assignment": "The ratio of the width of a pitchfork bifurcation is governed by the universal constant 2.502. Derive this scaling factor from first principles using the discrete topology of the S1/Z2 orbifold folding."
    },
    {
        "target": "Critical Rayleigh Number",
        "value": 1708,
        "assignment": "Fluids heated from below spontaneously form geometric convection cells (Benard cells) when the Rayleigh number crosses exactly 1708. Using the geometric constraints of a 3D volume transitioning to a 2D convective plane, mathematically derive this exact instability threshold."
    },
    {
        "target": "Critical Reynolds Number",
        "value": 2040,
        "assignment": "Laminar flow in a pipe transitions to turbulence at a Reynolds number of roughly 2040. Formulate a Z-Squared proof demonstrating why the topological limit of continuous flow breaks down into discrete geometric eddies at this exact macroscopic ratio."
    },
]

# =============================================================================
# CATEGORY 2: CONDENSED MATTER & LATTICE PHYSICS (10 tasks)
# =============================================================================

CONDENSED_MATTER_TASKS = [
    {
        "target": "Graphene Magic Angle",
        "value": 1.1,  # degrees
        "assignment": "Two 2D hexagonal lattices exhibit perfect superconductivity when twisted exactly 1.1 degrees (approx 0.019 radians). Derive this angle strictly from the interference patterns of two intersecting 2D holographic planes bounded by Z-Squared geometry."
    },
    {
        "target": "Quantum Hall 5/2 State",
        "value": 2.5,
        "assignment": "Electrons confined to 2D at near absolute zero form a resistance plateau exactly at the 5/2 fraction. Use the 12 edges of the Z-Squared cubic geometry (12=8+3+1) to derive why 5/2 is the only allowable even-denominator topological invariant."
    },
    {
        "target": "Graphene Opacity",
        "value": 0.023,  # pi*alpha
        "assignment": "A single layer of graphene absorbs exactly pi*alpha of incident light. Derive this exact fractional percentage limit using the Z-Squared geometric expression for the fine structure constant (alpha^-1=4Z2+3) interacting with a 2D plane."
    },
    {
        "target": "Landauer Limit ln(2)",
        "value": 0.693,
        "assignment": "The minimum absolute energy required to erase one bit of information is kB*T*ln(2). Derive the geometric origin of ln(2) using the Z2 orbifold symmetry, proving information erasure is just the geometric folding of a state space."
    },
    {
        "target": "3D Percolation Threshold",
        "value": 0.3116,
        "assignment": "In a simple 3D cubic lattice, global connectivity (percolation) occurs when exactly 31.16% of the nodes are filled. Derive this threshold from first principles using the unique tessellation properties of the Z-Squared cube."
    },
    {
        "target": "2D Percolation Threshold",
        "value": 0.5927,
        "assignment": "In a 2D square lattice, percolation occurs at ~59.27%. Relate this geometric phase transition to the Z-Squared spectral dimension flow as ds transitions from 3 to 2."
    },
    {
        "target": "Madelung Constant NaCl",
        "value": 1.747,
        "assignment": "The electrostatic binding energy of a cubic sodium chloride crystal is scaled by the Madelung constant. Derive 1.747 purely from the 12=8+3+1 edge/vertex charge distribution of the fundamental Z-Squared cube."
    },
    {
        "target": "Margolus-Levitin Quantum Speed Limit",
        "value": 1.571,  # pi/2
        "assignment": "A quantum system cannot evolve to an orthogonal state faster than pi*hbar/(2E). Derive this absolute speed limit strictly from the rotational geometry of the T3/Z2 internal manifold."
    },
    {
        "target": "Efimov Scaling Factor",
        "value": 22.7,
        "assignment": "Three interacting bosons will form an infinite nested series of bound states, each exactly 22.7 times larger than the last. Derive this discrete geometric scaling factor directly from the volume packing constraints of the Z-Squared spherical boundary."
    },
    {
        "target": "Kepler Sphere Packing",
        "value": 0.74048,
        "assignment": "The maximum density of packed spheres in 3D is exactly pi/(3*sqrt(2)). Prove that this geometric density limit is fundamentally linked to the Z-Squared identity (32*pi/3) mapping a sphere inside a cube."
    },
]

# =============================================================================
# CATEGORY 3: NUCLEAR & SUBATOMIC GEOMETRIES (10 tasks)
# =============================================================================

NUCLEAR_TASKS = [
    {
        "target": "Nuclear Magic Number 82",
        "value": 82,
        "assignment": "Atomic nuclei are exceptionally stable when they have 82 protons or neutrons. Prove computationally why the geometric shell structure of 82 nucleons represents a perfect topological closure in the Z-Squared 3D lattice space."
    },
    {
        "target": "Pion-to-Proton Mass Ratio",
        "value": 0.14,
        "assignment": "The mass of the pion is roughly 14% the mass of the proton. Derive this ratio strictly from the dimensional degrees of freedom allocated to the 8 vertices of the SU(3) strong force geometry."
    },
    {
        "target": "Deuteron Binding Energy",
        "value": 2.22,  # MeV
        "assignment": "The proton and neutron in a deuterium nucleus are bound by exactly 2.22 MeV. Derive this energy scale geometrically using the overlap of two adjoining cubic lattice unit cells."
    },
    {
        "target": "Neutron Skin Lead-208",
        "value": 0.28,  # femtometers
        "assignment": "Heavy nuclei form a 'skin' of excess neutrons. Derive the exact 0.28 femtometer thickness of the Lead-208 boundary using the volume-to-surface entropy partition function mu(x)=x/(1+x)."
    },
    {
        "target": "Hoyle State Carbon-12",
        "value": 7.65,  # MeV
        "assignment": "Carbon-12 possesses a highly specific resonance state at 7.65 MeV that allows stars to synthesize the elements of life. Prove that 7.65 MeV is the exact geometric eigenvalue required to fuse three alpha particles in the Z-Squared lattice."
    },
    {
        "target": "Muon Lifetime",
        "value": 2.196,  # microseconds
        "assignment": "The muon decays in exactly 2.196 microseconds. Derive this specific temporal decay rate using the dimensional scaling of the muon/electron mass ratio (64*pi+Z) crossing the electroweak boundary."
    },
    {
        "target": "Neutron Lifetime Anomaly",
        "value": 9,  # seconds difference
        "assignment": "Neutrons measured in a beam decay in 888 seconds; in a bottle, 879 seconds. Use the Z-Squared holographic boundary conditions to mathematically prove why the geometric confinement of the 'bottle' forces a 9-second discrepancy in the decay rate."
    },
    {
        "target": "Proton Gyromagnetic Ratio",
        "value": 42.57,  # MHz/T
        "assignment": "The proton's gyromagnetic ratio is 42.57 MHz/T. Since Z-Squared successfully derived the neutron/proton magnetic moment ratio, now derive the absolute proton spin coupling from the T3 cubic topology."
    },
    {
        "target": "Choptuik Scaling Exponent",
        "value": 0.374,
        "assignment": "In general relativity, the mass of a black hole formed at the threshold of critical collapse scales with an exponent of 0.374. Derive this non-linear exponent from the collapse of a 3D Z-Squared bulk into a holographic singularity."
    },
    {
        "target": "TOV Limit Neutron Star",
        "value": 2.1,  # solar masses
        "assignment": "Neutron stars collapse into black holes at roughly 2.1 solar masses. Calculate this exact geometric crush limit using the strong force boundary constraints derived from the Z-Squared 8-vertex geometry."
    },
]

# =============================================================================
# CATEGORY 4: ASTROPHYSICS & PLANETARY GEOMETRY (10 tasks)
# =============================================================================

ASTRO_TASKS = [
    {
        "target": "Chandrasekhar Limit",
        "value": 1.44,  # solar masses
        "assignment": "Electron degeneracy pressure fails at 1.44 solar masses. Derive the numerical coefficient (1.44) from first principles using the volume geometry of the Z-Squared sphere packing limit."
    },
    {
        "target": "Pioneer Anomaly Acceleration",
        "value": 8.74e-10,  # m/s^2
        "assignment": "The Pioneer spacecraft experienced an unexplained sunward acceleration of 8.74e-10 m/s^2. Notice that this is nearly identical to the Z-Squared derived MOND scale (a0~1.19e-10). Prove mathematically if the Pioneer anomaly is an artifact of the Z-Squared spectral dimension flow in the outer solar system."
    },
    {
        "target": "Solar Hale Cycle",
        "value": 22,  # years
        "assignment": "The Sun's magnetic field flips and resets exactly every 22 years (the Hale cycle). Derive this temporal period geometrically from the magnetohydrodynamic volume limits of a rotating spherical bulk."
    },
    {
        "target": "Chandler Wobble Period",
        "value": 433,  # days
        "assignment": "The Earth's axis of rotation wobbles with a primary period of 433 days. Model the Earth as a Z-Squared geometric sphere and derive this precise wobble frequency from its topological inertial moment."
    },
    {
        "target": "Cosmic Bulk Flow Velocity",
        "value": 300,  # km/s
        "assignment": "Galaxy clusters appear to be drifting together at a universal speed of ~300 km/s toward a specific point in the sky. Test if this bulk flow is a geometric consequence of the Z-Squared horizon boundary conditions."
    },
    {
        "target": "CMB Dipole Temperature",
        "value": 3.3,  # mK
        "assignment": "The Cosmic Microwave Background exhibits a 3.3 mK dipole due to Earth's motion. Determine if the absolute magnitude of this baseline velocity is constrained by the Z = sqrt(28*pi/3) expansion metric."
    },
    {
        "target": "ARCADE-2 Radio Excess",
        "value": 6,  # times louder
        "assignment": "The universe contains a background of radio waves 6 times louder than standard models predict. Prove whether this excess synchrotron radiation is generated by electrons interacting with the MOND (a0) boundary."
    },
    {
        "target": "Extragalactic Background Light",
        "value": 0,  # to derive
        "assignment": "Derive the absolute energy density limit of the cumulative starlight of the universe using the thermodynamic limits of the Z-Squared holographic screen."
    },
    {
        "target": "Observable Universe Ratio",
        "value": 3.29,  # 46/14 Gly
        "assignment": "The observable universe is ~46 billion light-years in radius, while the Hubble radius is ~14 billion. Derive this exact expansion ratio strictly using the geometric constant Z2=32*pi/3."
    },
    {
        "target": "QCD Beta Function Coefficient",
        "value": 11,
        "assignment": "The strong force gets weaker at high energies, dictated by the coefficient 11. Derive the integer 11 geometrically from the edges of the Z-Squared cube minus the global topology (12-1=11)."
    },
]

# =============================================================================
# CATEGORY 5: COMPLEX SYSTEMS, NETWORK THEORY & BIOLOGY (10 tasks)
# =============================================================================

COMPLEX_TASKS = [
    {
        "target": "Zipf's Law Exponent",
        "value": 1.0,
        "assignment": "In any complex system (languages, city populations), the rank-frequency distribution follows an inverse power law with an exponent of exactly 1. Prove that s=1 is the only allowable entropy partition for information sorted on a discrete geometric lattice."
    },
    {
        "target": "Benford's Law Distribution",
        "value": 0.301,  # log10(2)
        "assignment": "The leading digits in naturally occurring datasets follow a specific logarithmic curve. Derive this probability distribution as a pure geometric consequence of scale-invariance within the Z-Squared framework."
    },
    {
        "target": "DNA Helix Twist Angle",
        "value": 36,  # degrees
        "assignment": "The B-DNA double helix twists exactly 36 degrees per base pair, creating 10 pairs per turn. Derive this structural angle from the geometric constraints of stacking 2D chemical planes within a 3D cylindrical volume."
    },
    {
        "target": "Levinthal Paradox Exponent",
        "value": 300,  # 10^300 configurations
        "assignment": "A protein finds its correct 3D folded shape instantly, despite having 10^300 possible configurations. Prove that the folding pathway is a deterministic geometric collapse governed by the Z-Squared spectral dimension flow ds->2."
    },
    {
        "target": "Dunbar's Number",
        "value": 150,
        "assignment": "The cognitive limit to the number of stable social relationships a human can maintain is ~150. Treat cognitive network connections as edges on a complex lattice and derive the geometric hard-limit of stability."
    },
    {
        "target": "Golden Ratio Phyllotaxis",
        "value": 1.618,
        "assignment": "Leaves and seeds grow in spirals governed by the golden ratio. While numerically understood, derive why the universe defaults to this irrational number using the volume-packing constraints of the Z-Squared sphere."
    },
    {
        "target": "Kleiber's Law Coefficient",
        "value": 0,  # to derive Y0
        "assignment": "We already proved the 3/4 scaling exponent. Now, derive the absolute coefficient Y0 that anchors the metabolic equation, purely from the thermodynamic limits of carbon-based bonds."
    },
    {
        "target": "Lotka-Volterra Phase Shift",
        "value": 1.571,  # pi/2
        "assignment": "The populations of predators and prey oscillate out of phase by exactly 90 degrees (pi/2). Derive this phase shift dynamically from the conservation of topological volume in a closed system."
    },
    {
        "target": "Connectome Fractal Dimension",
        "value": 2.5,
        "assignment": "The human brain's neural network has a fractal dimension of roughly 2.5. Derive this exact fractional dimensionality by applying the Z-Squared spectral dimension formula ds(x)=2+mu(x) to a biological neural network."
    },
    {
        "target": "Heart Rate Scaling Exponent",
        "value": -0.25,  # -1/4 power
        "assignment": "Mammalian heart rates scale with mass to the -1/4 power. Derive this negative fractional exponent geometrically from the 32*pi/3 spatial boundaries of a pumping fluid volume."
    },
]

# =============================================================================
# CATEGORY 6: MATERIAL LIMITS & BOUNDARY CONDITIONS (5 tasks)
# =============================================================================

MATERIAL_TASKS = [
    {
        "target": "Graphene Tensile Strength",
        "value": 130,  # GPa
        "assignment": "Graphene breaks at 130 Gigapascals. Derive this exact mechanical breaking point from the topological limit of carbon-carbon bonds stretched across a 2D Z-Squared lattice."
    },
    {
        "target": "Silicon Bandgap Energy",
        "value": 1.11,  # eV
        "assignment": "Silicon at room temperature has a bandgap of 1.11 eV. Formulate a proof deriving this exact quantum energy gap strictly from the cubic geometry of the silicon diamond lattice."
    },
    {
        "target": "Universal Conductance Quantum",
        "value": 7.75e-5,  # 2e^2/h in Siemens
        "assignment": "Electrical conductance in 1D quantum wires happens in strict integer steps of 2e^2/h. Prove why the topological boundaries of a 1D wire mandate this exact mathematical step."
    },
    {
        "target": "Casimir Force Coefficient",
        "value": 0,  # to derive
        "assignment": "Two uncharged plates in a vacuum are pushed together by virtual particles. Derive the absolute force constant of the Casimir effect by mathematically mapping the Z-Squared boundary conditions of the restricted 3D space."
    },
    {
        "target": "von Klitzing Constant",
        "value": 25812,  # Ohms
        "assignment": "The von Klitzing constant defines exact plateaus of electrical resistance. Derive the absolute value 25,812 Ohms using purely the geometric constants of the Z-Squared M4xT3/Z2 framework."
    },
]


# =============================================================================
# LOAD ALL TASKS
# =============================================================================

ALL_CATEGORIES = {
    "chaos_fluid_dynamics": CHAOS_TASKS,
    "condensed_matter": CONDENSED_MATTER_TASKS,
    "nuclear_subatomic": NUCLEAR_TASKS,
    "astrophysics_planetary": ASTRO_TASKS,
    "complex_systems_biology": COMPLEX_TASKS,
    "material_limits": MATERIAL_TASKS,
}


def load_all_z2_tasks(queue: ResearchQueue = None) -> int:
    """Load all 50 Z² derivation tasks into the queue."""
    if queue is None:
        queue = ResearchQueue()

    total = 0
    for category, tasks in ALL_CATEGORIES.items():
        print(f"\nLoading category: {category}")
        for task_data in tasks:
            task = create_derivation_task(
                target=task_data["target"],
                target_value=task_data["value"],
                assignment=task_data["assignment"],
                category=category,
                domain="physics"
            )
            queue.add(task)
            total += 1
            print(f"  Added: {task.name}")

    print(f"\nTotal tasks loaded: {total}")
    return total


def get_task_summary() -> str:
    """Get summary of all tasks."""
    lines = ["Z² Derivation Tasks Summary", "=" * 50, ""]

    total = 0
    for category, tasks in ALL_CATEGORIES.items():
        lines.append(f"\n{category.upper()} ({len(tasks)} tasks)")
        lines.append("-" * 40)
        for task in tasks:
            lines.append(f"  - {task['target']}: {task['value']}")
            total += 1

    lines.append(f"\n{'=' * 50}")
    lines.append(f"TOTAL: {total} tasks")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load Z² Derivation Tasks")
    parser.add_argument("--load", action="store_true", help="Load all tasks to queue")
    parser.add_argument("--summary", action="store_true", help="Show task summary")
    parser.add_argument("--count", action="store_true", help="Show task count")

    args = parser.parse_args()

    if args.summary:
        print(get_task_summary())
    elif args.count:
        total = sum(len(tasks) for tasks in ALL_CATEGORIES.values())
        print(f"Total Z² derivation tasks: {total}")
    elif args.load:
        queue = ResearchQueue()
        count = load_all_z2_tasks(queue)
        print(f"\nLoaded {count} tasks. Queue has {len(queue)} total tasks.")
        print(f"Queue saved to: {queue.persistence_path}")
    else:
        parser.print_help()
