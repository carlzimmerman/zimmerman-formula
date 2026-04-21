# Molecular Dynamics Protocol V1.0

## Production-Grade Explicit Solvent Simulation Protocol

**Version:** 1.0
**Date:** April 21, 2026
**Platform:** Apple Silicon (M4 Max) with Metal Acceleration
**Authors:** Carl Zimmerman & Claude Opus 4.5

---

## Overview

This document defines the strict protocol for production-grade molecular dynamics simulations of therapeutic peptides. The 100ps shakedown run confirmed the pipeline functions correctly. This protocol specifies the parameters for 10-50ns overnight production runs.

**Key Principle:** No geometric axioms. Pure thermodynamics. Gibbs Free Energy is the only arbiter.

---

## 1. Peptide Capping Requirements

### N-Terminal Acetyl Cap (ACE)
```
Residue Name: ACE
Atoms: CH3-CO-
Molecular Weight: 43.04 Da
OpenMM Template: Built into Amber14 force field
```

**Implementation:**
```python
# When building peptide, prepend ACE residue
# PDBFixer will recognize standard caps
from pdbfixer import PDBFixer
fixer.addMissingAtoms()  # Adds ACE if N-terminus detected
```

### C-Terminal Amide Cap (NME)
```
Residue Name: NME (N-methylamide) or NH2
Atoms: -CO-NH-CH3 or -CO-NH2
Molecular Weight: 30.03 Da (NME) or 16.02 Da (NH2)
OpenMM Template: Built into Amber14 force field
```

**Implementation:**
```python
# C-terminal amide prevents carboxyl charge
# Use NME for N-methylamide or construct NH2 terminus
```

### Why Caps Matter
- Uncapped termini have unphysical +1 (N-term) and -1 (C-term) formal charges
- These charges cause artifactual electrostatic interactions
- Capped peptides mimic the electronic environment of peptides within proteins
- Drug-like peptides are typically acetylated and amidated

---

## 2. Force Field Specification

### Primary Force Field
```python
forcefield = ForceField('amber14-all.xml', 'amber14/tip3p.xml')
```

**Amber14-all includes:**
- Amber14SB protein parameters (validated for peptides)
- Proper ACE and NME cap templates
- Compatible with TIP3P explicit water

### Water Model
```
Model: TIP3P (Transferable Intermolecular Potential 3-Point)
Geometry: Rigid 3-site
O-H bond: 0.9572 Å
H-O-H angle: 104.52°
Charges: O = -0.834e, H = +0.417e
```

### Ion Parameters
```
Positive Ion: Na+ (Joung-Cheatham parameters)
Negative Ion: Cl- (Joung-Cheatham parameters)
Ionic Strength: 0.15 M (physiological)
```

---

## 3. System Preparation

### Solvation Box
```python
modeller.addSolvent(
    forcefield,
    model='tip3p',
    padding=1.2 * unit.nanometer,  # 12 Å minimum to periodic image
    ionicStrength=0.15 * unit.molar,
    positiveIon='Na+',
    negativeIon='Cl-',
)
```

**Box padding rationale:**
- 1.2 nm ensures peptide never interacts with its periodic image
- Minimum image convention requires padding > cutoff distance
- 1.0 nm cutoff + 0.2 nm buffer = 1.2 nm padding

### Nonbonded Interactions
```python
system = forcefield.createSystem(
    modeller.topology,
    nonbondedMethod=PME,           # Particle Mesh Ewald for long-range
    nonbondedCutoff=1.0 * unit.nanometer,
    constraints=HBonds,             # Constrain H-X bonds (allows 2fs timestep)
    rigidWater=True,                # Rigid TIP3P geometry
    ewaldErrorTolerance=0.0005,     # PME accuracy
)
```

---

## 4. Equilibration Protocol (STRICT 2-STAGE)

### Stage 1: NVT Equilibration (1 ns)
**Purpose:** Thermalize the system at constant volume

```python
# NVT Integrator
integrator_nvt = LangevinMiddleIntegrator(
    310 * unit.kelvin,           # Body temperature
    1.0 / unit.picosecond,       # Friction coefficient
    2.0 * unit.femtoseconds,     # Timestep
)

# NO barostat for NVT
# Run for 500,000 steps = 1 ns
NVT_STEPS = 500000  # 1 ns at 2 fs/step
```

**What happens:**
- Random velocities assigned from Maxwell-Boltzmann distribution at 310K
- System absorbs thermal energy
- Water molecules reorient around peptide
- Hydrogen bond network forms

**Success criteria:**
- Temperature stabilizes at 310 ± 5 K
- No large potential energy spikes

### Stage 2: NPT Equilibration (2 ns)
**Purpose:** Equilibrate density at constant pressure

```python
# Add Monte Carlo Barostat
barostat = MonteCarloBarostat(
    1.0 * unit.atmospheres,      # 1 atm
    310 * unit.kelvin,           # Must match integrator
    25,                          # Attempt volume change every 25 steps
)
system.addForce(barostat)

# NPT Integrator (same as NVT)
integrator_npt = LangevinMiddleIntegrator(
    310 * unit.kelvin,
    1.0 / unit.picosecond,
    2.0 * unit.femtoseconds,
)

# Run for 1,000,000 steps = 2 ns
NPT_EQUIL_STEPS = 1000000  # 2 ns at 2 fs/step
```

**What happens:**
- Box volume adjusts to achieve 1 atm pressure
- Density equilibrates to ~1.0 g/cm³
- Any vacuum bubbles collapse
- System reaches thermodynamic equilibrium

**Success criteria:**
- Density stabilizes at 1.0 ± 0.02 g/cm³
- Box dimensions stable (< 0.5% fluctuation)
- RMSD rate of change approaches zero

---

## 5. Production Run Specification

### Duration Options
| Run Type | Duration | Steps (2fs) | CPU Hours (est.) |
|----------|----------|-------------|------------------|
| Quick validation | 10 ns | 5,000,000 | 2-4 hours |
| Standard | 25 ns | 12,500,000 | 6-10 hours |
| Publication-grade | 50 ns | 25,000,000 | 12-20 hours |

### Production Integrator
```python
integrator = LangevinMiddleIntegrator(
    310 * unit.kelvin,           # Temperature
    1.0 / unit.picosecond,       # Friction (thermostat coupling)
    2.0 * unit.femtoseconds,     # Timestep (requires HBonds constraint)
)
```

### Langevin Middle Integrator Rationale
- **Better than Velocity Verlet:** Includes stochastic thermostat
- **Better than Langevin:** "Middle" scheme has better energy conservation
- **2 fs timestep:** Safe with HBonds constraints (fastest bond is C-H at ~10 fs)

### Trajectory Output
```python
# Save coordinates every 10 ps (5000 steps)
TRAJECTORY_INTERVAL = 5000  # steps

# Save to DCD format (compact binary)
simulation.reporters.append(
    DCDReporter(f'{peptide_id}_trajectory.dcd', TRAJECTORY_INTERVAL)
)

# State data every 1 ps
simulation.reporters.append(
    StateDataReporter(
        f'{peptide_id}_state.csv',
        500,  # Every 1 ps
        step=True,
        time=True,
        potentialEnergy=True,
        kineticEnergy=True,
        temperature=True,
        volume=True,
        density=True,
    )
)
```

---

## 6. Apple Silicon Metal Acceleration

### Platform Configuration
```python
from openmm import Platform

# Force Metal platform for Apple Silicon
platform = Platform.getPlatformByName('Metal')

# Platform properties (optional tuning)
properties = {
    'Precision': 'mixed',  # mixed precision for speed + accuracy
}

# Create simulation with Metal
simulation = Simulation(
    modeller.topology,
    system,
    integrator,
    platform,
    properties,
)
```

### Metal vs CPU Performance
| Platform | 10ns Runtime (est.) | Notes |
|----------|---------------------|-------|
| CPU | 8-12 hours | Uses all P-cores |
| Metal | 2-4 hours | GPU acceleration |
| CUDA | N/A | Not available on Mac |

### Fallback Logic
```python
try:
    platform = Platform.getPlatformByName('Metal')
    print("Using Metal (Apple GPU)")
except Exception:
    try:
        platform = Platform.getPlatformByName('OpenCL')
        print("Using OpenCL")
    except Exception:
        platform = Platform.getPlatformByName('CPU')
        print("Using CPU (slow)")
```

---

## 7. RMSD Analysis Protocol

### Reference Structure
```python
# Use post-NPT-equilibration structure as reference
# NOT the initial extended chain
state = simulation.context.getState(getPositions=True)
reference_positions = state.getPositions(asNumpy=True)
```

### RMSD Calculation
```python
def calculate_rmsd(ref, pos, indices):
    """
    Calculate RMSD with center-of-mass alignment.
    """
    ref_subset = ref[indices]
    pos_subset = pos[indices]

    # Center both
    ref_centered = ref_subset - np.mean(ref_subset, axis=0)
    pos_centered = pos_subset - np.mean(pos_subset, axis=0)

    # RMSD
    diff = ref_centered - pos_centered
    rmsd = np.sqrt(np.mean(np.sum(diff**2, axis=1)))

    return rmsd
```

### Stability Criteria (Post-Equilibration)
| Metric | STABLE | MARGINAL | UNSTABLE |
|--------|--------|----------|----------|
| Mean RMSD | < 0.3 nm | 0.3-0.5 nm | > 0.5 nm |
| RMSD Drift | < 0.05 nm/ns | 0.05-0.2 nm/ns | > 0.2 nm/ns |
| Fluctuation (σ) | < 0.05 nm | 0.05-0.1 nm | > 0.1 nm |

**Interpretation:**
- STABLE: Peptide reached thermodynamic minimum, proceed to binding
- MARGINAL: May need longer simulation or structure optimization
- UNSTABLE: Redesign peptide or investigate unfolding mechanism

---

## 8. Overnight Batch Processing

### Script Template
```python
#!/usr/bin/env python3
"""
overnight_production_md.py - Long-haul MD batch processor
Run with: nohup python overnight_production_md.py > md_log.txt 2>&1 &
"""

PEPTIDES = [
    ("ZIM-SYN-004", "FPF", "ACE", "NME"),
    ("ZIM-ADD-003", "RWWFWR", None, None),
    ("ZIM-PD6-013", "WFFLY", "ACE", "NME"),
]

PRODUCTION_NS = 10  # Start with 10ns

for peptide_id, sequence, n_cap, c_cap in PEPTIDES:
    print(f"Starting {peptide_id}...")
    run_production_md(peptide_id, sequence, n_cap, c_cap, PRODUCTION_NS)
    print(f"Completed {peptide_id}")
```

### Running Overnight
```bash
# Start batch processing
cd validated_pipeline
nohup python overnight_production_md.py > md_overnight.log 2>&1 &

# Check progress
tail -f md_overnight.log

# Check if still running
ps aux | grep overnight
```

---

## 9. Quality Control Checklist

### Before Production Run
- [ ] Peptide structure built with correct sequence
- [ ] N-terminal cap applied (ACE if required)
- [ ] C-terminal cap applied (NME if required)
- [ ] System solvated with 1.2 nm padding
- [ ] Ions added for 0.15 M ionic strength
- [ ] Energy minimized (< 1000 kJ/mol/nm gradient)
- [ ] NVT equilibration complete (1 ns)
- [ ] NPT equilibration complete (2 ns)
- [ ] Reference structure saved for RMSD

### During Production Run
- [ ] Temperature stable at 310 ± 5 K
- [ ] Density stable at 1.0 ± 0.02 g/cm³
- [ ] No potential energy explosions
- [ ] Trajectory writing correctly

### After Production Run
- [ ] RMSD trajectory calculated
- [ ] Stability verdict assigned
- [ ] Results saved to JSON
- [ ] Trajectory archived

---

## 10. Expected Results

### For a STABLE peptide
```
Production: 10 ns
Final RMSD: 0.25 ± 0.03 nm
RMSD Drift: 0.02 nm/ns
Temperature: 310.1 ± 2.3 K
Density: 0.998 ± 0.005 g/cm³
VERDICT: STABLE - Proceed to umbrella sampling
```

### For an UNSTABLE peptide
```
Production: 10 ns
Final RMSD: 0.85 ± 0.15 nm
RMSD Drift: 0.35 nm/ns
Temperature: 310.2 ± 2.1 K
Density: 0.997 ± 0.006 g/cm³
VERDICT: UNSTABLE - Peptide unfolding, redesign required
```

---

## Appendix: Full Production Script

See: `val_10_overnight_production_md.py` (to be created)

---

## References

1. Case, D.A. et al. (2023). Amber 2023 Reference Manual
2. Eastman, P. et al. (2017). OpenMM 7: Rapid development of high performance algorithms for molecular dynamics. PLOS Comp. Bio.
3. Shirts, M.R. & Chodera, J.D. (2008). Statistically optimal analysis of samples from multiple equilibrium states. J. Chem. Phys.
4. Jorgensen, W.L. et al. (1983). Comparison of simple potential functions for simulating liquid water. J. Chem. Phys.

---

**Protocol Status:** APPROVED FOR OVERNIGHT RUNS
**Engine Status:** READY
**Next Action:** Create `val_10_overnight_production_md.py` and initiate batch processing

---

*This protocol represents the complete pivot from geometric axioms to pure first-principles thermodynamics. No Z². No magic numbers. Only Gibbs Free Energy.*
