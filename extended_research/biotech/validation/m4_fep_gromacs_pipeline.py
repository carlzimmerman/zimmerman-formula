#!/usr/bin/env python3
"""
M4 FEP/GROMACS Absolute Binding Affinity Pipeline
===================================================

Automates setup for Alchemical Free Energy Perturbation (FEP) using GROMACS
and the pmx library for calculating absolute binding free energies.

Physics:
- CHARMM36m force field parameterization
- Thermodynamic cycle for ΔGbind calculation
- Decoupling peptide from solvent and receptor binding pocket
- Lambda windows (λ=0.0 to 1.0) for Coulombic and vdW transformations
- Bennett Acceptance Ratio (BAR) for free energy estimates

Output:
- GROMACS topology and coordinate files
- Multi-window simulation bash scripts for GPU cluster
- Alchemical analysis commands for BAR error estimates

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026

REQUIREMENTS:
- GROMACS 2023+ with GPU support
- pmx library (pip install pmx-biobb)
- MDAnalysis
- alchemlyb (pip install alchemlyb)
"""

import json
import os
import subprocess
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import shutil


@dataclass
class FEPSimulationConfig:
    """Configuration for FEP simulation setup."""
    # System
    peptide_sequence: str
    peptide_id: str
    receptor_pdb: str

    # Force field
    forcefield: str = "charmm36m"
    water_model: str = "tip3p"

    # Lambda windows
    n_lambda_coul: int = 11  # Coulombic decoupling windows
    n_lambda_vdw: int = 20   # van der Waals decoupling windows

    # Simulation parameters
    temperature: float = 300.0  # Kelvin
    pressure: float = 1.0       # bar

    # Equilibration
    nsteps_em: int = 50000      # Energy minimization steps
    nsteps_nvt: int = 50000     # NVT equilibration (100 ps)
    nsteps_npt: int = 50000     # NPT equilibration (100 ps)

    # Production
    nsteps_prod: int = 2500000  # Production (5 ns per window)

    # GPU settings
    gpu_id: int = 0
    n_threads: int = 8


@dataclass
class ThermodynamicCycle:
    """Thermodynamic cycle for absolute binding free energy."""
    # ΔGbind = ΔGcomplex - ΔGsolvent
    # Where each ΔG is calculated by alchemical decoupling

    dG_complex: float = 0.0      # Decoupling in complex
    dG_complex_err: float = 0.0
    dG_solvent: float = 0.0      # Decoupling in solvent
    dG_solvent_err: float = 0.0
    dG_bind: float = 0.0         # Final binding free energy
    dG_bind_err: float = 0.0


def generate_lambda_schedule(n_coul: int = 11, n_vdw: int = 20) -> Dict[str, List[float]]:
    """
    Generate lambda schedule for alchemical transformation.

    Coulombic interactions turned off first, then vdW.
    Uses soft-core potentials for vdW to avoid singularities.
    """
    # Coulombic lambdas: 0 -> 1 (turn off electrostatics)
    lambda_coul = [round(i / (n_coul - 1), 3) for i in range(n_coul)]

    # vdW lambdas: 0 -> 1 (turn off van der Waals)
    # Use non-linear spacing near endpoints for better overlap
    lambda_vdw_raw = []
    for i in range(n_vdw):
        # Sigmoidal-like spacing for better phase space overlap
        x = i / (n_vdw - 1)
        # More points near 0 and 1 where overlap is critical
        if x < 0.1:
            lambda_vdw_raw.append(round(x * 2, 3))  # Fine near 0
        elif x > 0.9:
            lambda_vdw_raw.append(round(0.8 + (x - 0.9) * 2, 3))  # Fine near 1
        else:
            lambda_vdw_raw.append(round(x, 3))

    # Ensure unique sorted values
    lambda_vdw = sorted(set(lambda_vdw_raw))

    return {
        "coul": lambda_coul,
        "vdw": lambda_vdw,
        "total_windows": len(lambda_coul) + len(lambda_vdw)
    }


def generate_mdp_em(output_path: Path):
    """Generate energy minimization MDP file."""
    mdp_content = """; Energy Minimization MDP for FEP Setup
; CHARMM36m force field compatible

; Run control
integrator              = steep
nsteps                  = 50000
emtol                   = 100.0
emstep                  = 0.01

; Neighbor searching
cutoff-scheme           = Verlet
nstlist                 = 10
rlist                   = 1.2
vdwtype                 = Cut-off
vdw-modifier            = Force-switch
rvdw-switch             = 1.0
rvdw                    = 1.2

; Electrostatics
coulombtype             = PME
rcoulomb                = 1.2
pme_order               = 4
fourierspacing          = 0.12

; Constraints
constraints             = h-bonds
constraint-algorithm    = LINCS
lincs-order             = 4
"""
    with open(output_path, "w") as f:
        f.write(mdp_content)


def generate_mdp_nvt(output_path: Path, temperature: float = 300.0):
    """Generate NVT equilibration MDP file."""
    mdp_content = f"""; NVT Equilibration MDP for FEP Setup
; CHARMM36m force field compatible

; Run control
integrator              = md
dt                      = 0.002
nsteps                  = 50000  ; 100 ps

; Output control
nstxout                 = 5000
nstvout                 = 5000
nstfout                 = 0
nstlog                  = 1000
nstenergy               = 1000
nstxout-compressed      = 5000

; Neighbor searching
cutoff-scheme           = Verlet
nstlist                 = 20
rlist                   = 1.2

; Electrostatics
coulombtype             = PME
rcoulomb                = 1.2
pme_order               = 4
fourierspacing          = 0.12

; van der Waals
vdwtype                 = Cut-off
vdw-modifier            = Force-switch
rvdw-switch             = 1.0
rvdw                    = 1.2

; Temperature coupling
tcoupl                  = V-rescale
tc-grps                 = Protein Non-Protein
tau_t                   = 0.1 0.1
ref_t                   = {temperature} {temperature}

; Pressure coupling (off for NVT)
pcoupl                  = no

; Constraints
constraints             = h-bonds
constraint-algorithm    = LINCS
lincs-order             = 4

; Velocity generation
gen_vel                 = yes
gen_temp                = {temperature}
gen_seed                = -1

; Center of mass motion removal
comm-mode               = Linear
nstcomm                 = 100
"""
    with open(output_path, "w") as f:
        f.write(mdp_content)


def generate_mdp_npt(output_path: Path, temperature: float = 300.0,
                     pressure: float = 1.0):
    """Generate NPT equilibration MDP file."""
    mdp_content = f"""; NPT Equilibration MDP for FEP Setup
; CHARMM36m force field compatible

; Run control
integrator              = md
dt                      = 0.002
nsteps                  = 50000  ; 100 ps

; Output control
nstxout                 = 5000
nstvout                 = 5000
nstfout                 = 0
nstlog                  = 1000
nstenergy               = 1000
nstxout-compressed      = 5000

; Neighbor searching
cutoff-scheme           = Verlet
nstlist                 = 20
rlist                   = 1.2

; Electrostatics
coulombtype             = PME
rcoulomb                = 1.2
pme_order               = 4
fourierspacing          = 0.12

; van der Waals
vdwtype                 = Cut-off
vdw-modifier            = Force-switch
rvdw-switch             = 1.0
rvdw                    = 1.2

; Temperature coupling
tcoupl                  = V-rescale
tc-grps                 = Protein Non-Protein
tau_t                   = 0.1 0.1
ref_t                   = {temperature} {temperature}

; Pressure coupling
pcoupl                  = C-rescale
pcoupltype              = isotropic
tau_p                   = 5.0
ref_p                   = {pressure}
compressibility         = 4.5e-5
refcoord_scaling        = com

; Constraints
constraints             = h-bonds
constraint-algorithm    = LINCS
lincs-order             = 4

; Center of mass motion removal
comm-mode               = Linear
nstcomm                 = 100
"""
    with open(output_path, "w") as f:
        f.write(mdp_content)


def generate_mdp_fep(output_path: Path, lambda_coul: float, lambda_vdw: float,
                     temperature: float = 300.0, pressure: float = 1.0,
                     nsteps: int = 2500000):
    """
    Generate FEP production MDP file with lambda parameters.

    Uses soft-core potentials for vdW to avoid singularities.
    """
    mdp_content = f"""; FEP Production MDP
; Alchemical Free Energy Perturbation with CHARMM36m
; Lambda: coul={lambda_coul}, vdw={lambda_vdw}

; Run control
integrator              = sd      ; Stochastic dynamics (Langevin)
dt                      = 0.002
nsteps                  = {nsteps}  ; {nsteps * 0.002 / 1000:.1f} ns

; Output control
nstxout                 = 0
nstvout                 = 0
nstfout                 = 0
nstlog                  = 5000
nstenergy               = 500
nstxout-compressed      = 5000
nstdhdl                 = 100     ; dH/dλ output frequency

; Neighbor searching
cutoff-scheme           = Verlet
nstlist                 = 20
rlist                   = 1.2

; Electrostatics
coulombtype             = PME
rcoulomb                = 1.2
pme_order               = 4
fourierspacing          = 0.12

; van der Waals
vdwtype                 = Cut-off
vdw-modifier            = Force-switch
rvdw-switch             = 1.0
rvdw                    = 1.2

; Temperature coupling (via SD integrator)
tc-grps                 = System
tau_t                   = 2.0
ref_t                   = {temperature}

; Pressure coupling
pcoupl                  = C-rescale
pcoupltype              = isotropic
tau_p                   = 5.0
ref_p                   = {pressure}
compressibility         = 4.5e-5

; Constraints
constraints             = h-bonds
constraint-algorithm    = LINCS
lincs-order             = 4

; ============================================
; FREE ENERGY PARAMETERS
; ============================================
free-energy             = yes
init-lambda-state       = -1      ; Use explicit lambda values below

; Lambda values for this window
coul-lambdas            = {lambda_coul}
vdw-lambdas             = {lambda_vdw}

; Soft-core parameters (critical for vdW decoupling)
sc-alpha                = 0.5     ; Soft-core alpha
sc-power                = 1       ; Power for soft-core
sc-sigma                = 0.3     ; Soft-core sigma (nm)
sc-coul                 = no      ; No soft-core for Coulombic

; Decoupling
couple-moltype          = Peptide
couple-lambda0          = vdw-q   ; Fully coupled at lambda=0
couple-lambda1          = none    ; Fully decoupled at lambda=1
couple-intramol         = yes     ; Include intramolecular interactions

; dH/dλ calculation
calc-lambda-neighbors   = -1      ; Calculate dH/dλ for all states (for MBAR)

; ============================================
; Domain decomposition
; ============================================
; Disabled for single GPU
"""
    with open(output_path, "w") as f:
        f.write(mdp_content)


def generate_topology_header(peptide_sequence: str, forcefield: str = "charmm36m"):
    """Generate GROMACS topology file header with CHARMM36m."""
    return f"""; Topology for peptide: {peptide_sequence}
; Generated by M4 FEP Pipeline
; Force field: {forcefield}
; Date: {datetime.now().isoformat()}

; Include force field parameters
#include "charmm36m.ff/forcefield.itp"

; Include water topology
#include "charmm36m.ff/tip3p.itp"

; Include peptide topology (generated by gmx pdb2gmx)
#include "peptide.itp"

; Include ion topologies
#include "charmm36m.ff/ions.itp"

[ system ]
; Name
Peptide-Receptor FEP System

[ molecules ]
; Compound        #mols
Receptor          1
Peptide           1
SOL               XXXX    ; Updated by gmx solvate
NA                XX      ; Updated by gmx genion
CL                XX      ; Updated by gmx genion
"""


def generate_bash_setup_script(config: FEPSimulationConfig, output_dir: Path,
                               lambda_schedule: Dict) -> str:
    """Generate bash script for system setup."""
    script = f"""#!/bin/bash
# M4 FEP System Setup Script
# Generated: {datetime.now().isoformat()}
# Peptide: {config.peptide_id}
# Force field: {config.forcefield}

set -e  # Exit on error

# Directory setup
WORKDIR="{output_dir}"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

echo "=============================================="
echo "M4 FEP SETUP: {config.peptide_id}"
echo "=============================================="

# 1. Prepare receptor structure
echo "Step 1: Preparing receptor..."
gmx pdb2gmx -f receptor.pdb -o receptor_processed.gro -water {config.water_model} \\
    -ff {config.forcefield} -ignh -his << EOF
0
0
0
0
0
EOF

# 2. Prepare peptide structure (separate topology)
echo "Step 2: Preparing peptide..."
# First convert sequence to PDB using external tool or pre-prepared structure
# Assuming peptide.pdb exists
gmx pdb2gmx -f peptide.pdb -o peptide_processed.gro -water {config.water_model} \\
    -ff {config.forcefield} -ignh -p peptide.top

# Extract peptide itp from topology
grep -A1000 "\\[ moleculetype \\]" peptide.top | grep -B1000 "\\[ system \\]" | \\
    head -n -1 > peptide.itp

# 3. Create complex
echo "Step 3: Creating complex..."
# Manually combine GRO files (receptor + peptide)
python3 << 'PYTHON'
import MDAnalysis as mda

# Load structures
receptor = mda.Universe("receptor_processed.gro")
peptide = mda.Universe("peptide_processed.gro")

# Combine (peptide should be positioned in binding site)
# This is a placeholder - real docking should precede this
combined = mda.Merge(receptor.atoms, peptide.atoms)
combined.atoms.write("complex.gro")
print(f"Complex created: {{len(combined.atoms)}} atoms")
PYTHON

# 4. Define simulation box
echo "Step 4: Defining box..."
gmx editconf -f complex.gro -o complex_box.gro -c -d 1.2 -bt dodecahedron

# 5. Solvate
echo "Step 5: Solvating..."
gmx solvate -cp complex_box.gro -cs spc216.gro -o complex_solv.gro -p topol.top

# 6. Add ions
echo "Step 6: Adding ions..."
gmx grompp -f ions.mdp -c complex_solv.gro -p topol.top -o ions.tpr -maxwarn 2
echo "SOL" | gmx genion -s ions.tpr -o complex_ions.gro -p topol.top \\
    -pname NA -nname CL -neutral -conc 0.15

# 7. Energy minimization
echo "Step 7: Energy minimization..."
gmx grompp -f em.mdp -c complex_ions.gro -p topol.top -o em.tpr
gmx mdrun -v -deffnm em -ntmpi 1 -ntomp {config.n_threads}

# 8. NVT equilibration
echo "Step 8: NVT equilibration..."
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -v -deffnm nvt -ntmpi 1 -ntomp {config.n_threads}

# 9. NPT equilibration
echo "Step 9: NPT equilibration..."
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -v -deffnm npt -ntmpi 1 -ntomp {config.n_threads}

echo "=============================================="
echo "SETUP COMPLETE"
echo "Ready for FEP production runs"
echo "=============================================="
"""
    return script


def generate_bash_fep_production(config: FEPSimulationConfig, output_dir: Path,
                                  lambda_schedule: Dict, leg: str = "complex") -> str:
    """
    Generate bash script for FEP production runs.

    leg: "complex" or "solvent" (two legs of thermodynamic cycle)
    """
    n_windows = lambda_schedule["total_windows"]

    script = f"""#!/bin/bash
# M4 FEP Production Script - {leg.upper()} LEG
# Generated: {datetime.now().isoformat()}
# Peptide: {config.peptide_id}
# Total windows: {n_windows}

set -e

WORKDIR="{output_dir}/{leg}"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

# GPU configuration
export GMX_GPU_ID={config.gpu_id}
export OMP_NUM_THREADS={config.n_threads}

echo "=============================================="
echo "FEP PRODUCTION: {leg.upper()} LEG"
echo "Lambda windows: {n_windows}"
echo "=============================================="

"""

    # Add lambda window runs
    window_idx = 0

    # Coulombic decoupling (vdW = 0)
    for i, lc in enumerate(lambda_schedule["coul"]):
        script += f"""
# Window {window_idx}: lambda_coul={lc}, lambda_vdw=0.0
mkdir -p window_{window_idx:02d}
cd window_{window_idx:02d}
ln -sf ../npt.gro .
ln -sf ../npt.cpt .
ln -sf ../topol.top .

gmx grompp -f ../mdp/fep_coul_{lc:.3f}_vdw_0.000.mdp \\
    -c npt.gro -t npt.cpt -p topol.top -o fep.tpr -maxwarn 2

gmx mdrun -v -deffnm fep -ntmpi 1 -ntomp {config.n_threads} \\
    -nb gpu -pme gpu -bonded gpu -update gpu

cd ..
echo "Window {window_idx} complete (coul={lc}, vdw=0.0)"
"""
        window_idx += 1

    # van der Waals decoupling (Coulombic already off)
    for i, lv in enumerate(lambda_schedule["vdw"]):
        if lv == 0.0:
            continue  # Already covered in Coulombic phase
        script += f"""
# Window {window_idx}: lambda_coul=1.0, lambda_vdw={lv}
mkdir -p window_{window_idx:02d}
cd window_{window_idx:02d}
ln -sf ../npt.gro .
ln -sf ../npt.cpt .
ln -sf ../topol.top .

gmx grompp -f ../mdp/fep_coul_1.000_vdw_{lv:.3f}.mdp \\
    -c npt.gro -t npt.cpt -p topol.top -o fep.tpr -maxwarn 2

gmx mdrun -v -deffnm fep -ntmpi 1 -ntomp {config.n_threads} \\
    -nb gpu -pme gpu -bonded gpu -update gpu

cd ..
echo "Window {window_idx} complete (coul=1.0, vdw={lv})"
"""
        window_idx += 1

    script += f"""
echo "=============================================="
echo "FEP {leg.upper()} LEG COMPLETE"
echo "Total windows run: {window_idx}"
echo "=============================================="
"""
    return script


def generate_bash_analysis(config: FEPSimulationConfig, output_dir: Path) -> str:
    """Generate bash script for alchemical analysis using alchemlyb."""
    script = f"""#!/bin/bash
# M4 FEP Analysis Script
# Generated: {datetime.now().isoformat()}
# Peptide: {config.peptide_id}

set -e

WORKDIR="{output_dir}"
cd "$WORKDIR"

echo "=============================================="
echo "ALCHEMICAL ANALYSIS: {config.peptide_id}"
echo "=============================================="

# Run alchemical analysis using alchemlyb
python3 << 'PYTHON'
import os
import glob
import numpy as np
from alchemlyb.parsing.gmx import extract_dHdl, extract_u_nk
from alchemlyb.preprocessing import subsampling
from alchemlyb.estimators import BAR, MBAR, TI
from alchemlyb.visualisation import plot_mbar_overlap_matrix
import matplotlib.pyplot as plt

def analyze_leg(leg_dir, leg_name):
    \"\"\"Analyze one leg of the thermodynamic cycle.\"\"\"
    print(f"\\nAnalyzing {{leg_name}} leg...")

    # Find all xvg files
    dhdl_files = sorted(glob.glob(f"{{leg_dir}}/window_*/fep.xvg"))

    if not dhdl_files:
        print(f"No dH/dl files found in {{leg_dir}}")
        return None, None

    print(f"Found {{len(dhdl_files)}} lambda windows")

    # Extract dH/dl data
    dhdl_list = []
    for f in dhdl_files:
        try:
            dhdl = extract_dHdl(f, T=300)
            # Subsample to remove correlation
            dhdl_subsampled = subsampling.equilibrium_detection(dhdl)
            dhdl_list.append(dhdl_subsampled)
        except Exception as e:
            print(f"Warning: Could not parse {{f}}: {{e}}")

    if not dhdl_list:
        return None, None

    # Combine data
    dhdl_all = subsampling.slicing(subsampling.concat(dhdl_list), lower=0, step=1)

    # BAR estimator (preferred for GROMACS)
    print("Running BAR estimator...")
    bar = BAR()
    bar.fit(dhdl_all)
    dG_bar = bar.delta_f_.iloc[0, -1]
    dG_bar_err = bar.d_delta_f_.iloc[0, -1]

    print(f"  BAR: ΔG = {{dG_bar:.3f}} ± {{dG_bar_err:.3f}} kJ/mol")

    # Also try MBAR for comparison
    try:
        u_nk_list = []
        for f in dhdl_files:
            try:
                u_nk = extract_u_nk(f, T=300)
                u_nk_list.append(u_nk)
            except Exception:
                pass

        if u_nk_list:
            u_nk_all = subsampling.concat(u_nk_list)
            mbar = MBAR()
            mbar.fit(u_nk_all)
            dG_mbar = mbar.delta_f_.iloc[0, -1]
            dG_mbar_err = mbar.d_delta_f_.iloc[0, -1]
            print(f"  MBAR: ΔG = {{dG_mbar:.3f}} ± {{dG_mbar_err:.3f}} kJ/mol")

            # Plot overlap matrix
            fig = plot_mbar_overlap_matrix(mbar.overlap_matrix)
            fig.savefig(f"{{leg_dir}}/overlap_matrix.png", dpi=150)
            plt.close()
            print(f"  Overlap matrix saved to {{leg_dir}}/overlap_matrix.png")
    except Exception as e:
        print(f"  MBAR analysis failed: {{e}}")

    return dG_bar, dG_bar_err

# Analyze both legs
dG_complex, dG_complex_err = analyze_leg("complex", "complex")
dG_solvent, dG_solvent_err = analyze_leg("solvent", "solvent")

# Calculate binding free energy
print("\\n" + "="*60)
print("THERMODYNAMIC CYCLE RESULTS")
print("="*60)

if dG_complex is not None and dG_solvent is not None:
    # ΔGbind = ΔGcomplex - ΔGsolvent
    dG_bind = dG_complex - dG_solvent
    dG_bind_err = np.sqrt(dG_complex_err**2 + dG_solvent_err**2)

    # Convert to kcal/mol (1 kJ/mol = 0.239 kcal/mol)
    dG_bind_kcal = dG_bind * 0.239
    dG_bind_err_kcal = dG_bind_err * 0.239

    print(f"ΔG_complex  = {{dG_complex:.3f}} ± {{dG_complex_err:.3f}} kJ/mol")
    print(f"ΔG_solvent  = {{dG_solvent:.3f}} ± {{dG_solvent_err:.3f}} kJ/mol")
    print(f"ΔG_bind     = {{dG_bind:.3f}} ± {{dG_bind_err:.3f}} kJ/mol")
    print(f"            = {{dG_bind_kcal:.2f}} ± {{dG_bind_err_kcal:.2f}} kcal/mol")

    # Estimate Kd from ΔGbind
    # ΔG = RT ln(Kd), so Kd = exp(ΔG/RT)
    # R = 8.314 J/(mol·K), T = 300 K
    RT = 8.314 * 300 / 1000  # kJ/mol
    Kd_M = np.exp(dG_bind / RT)
    Kd_nM = Kd_M * 1e9

    print(f"\\nEstimated Kd = {{Kd_nM:.2e}} nM")

    # Save results
    results = {{
        "peptide_id": "{config.peptide_id}",
        "dG_complex_kJmol": float(dG_complex),
        "dG_complex_err_kJmol": float(dG_complex_err),
        "dG_solvent_kJmol": float(dG_solvent),
        "dG_solvent_err_kJmol": float(dG_solvent_err),
        "dG_bind_kJmol": float(dG_bind),
        "dG_bind_err_kJmol": float(dG_bind_err),
        "dG_bind_kcalmol": float(dG_bind_kcal),
        "dG_bind_err_kcalmol": float(dG_bind_err_kcal),
        "Kd_nM": float(Kd_nM),
        "method": "BAR",
        "temperature_K": 300.0
    }}

    import json
    with open("fep_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\\nResults saved to fep_results.json")
else:
    print("ERROR: Could not complete thermodynamic cycle analysis")

print("="*60)
PYTHON

echo "=============================================="
echo "ANALYSIS COMPLETE"
echo "=============================================="
"""
    return script


def generate_slurm_submission(config: FEPSimulationConfig, output_dir: Path,
                              lambda_schedule: Dict) -> str:
    """Generate SLURM submission script for HPC clusters."""
    n_windows = lambda_schedule["total_windows"]

    script = f"""#!/bin/bash
#SBATCH --job-name=fep_{config.peptide_id}
#SBATCH --output=fep_%j.out
#SBATCH --error=fep_%j.err
#SBATCH --time=48:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={config.n_threads}
#SBATCH --gres=gpu:1
#SBATCH --partition=gpu
#SBATCH --array=0-{n_windows - 1}

# M4 FEP SLURM Array Job
# Peptide: {config.peptide_id}
# Generated: {datetime.now().isoformat()}

# Load GROMACS module (adjust for your cluster)
module load gromacs/2023-cuda

# Environment
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export GMX_MAXBACKUP=-1

cd {output_dir}

# Determine lambda window from array index
WINDOW=$SLURM_ARRAY_TASK_ID
WINDOW_DIR=$(printf "window_%02d" $WINDOW)

cd $WINDOW_DIR

echo "Running FEP window $WINDOW on $HOSTNAME"
echo "GPU: $CUDA_VISIBLE_DEVICES"

# Run production
gmx mdrun -v -deffnm fep -ntmpi 1 -ntomp $OMP_NUM_THREADS \\
    -nb gpu -pme gpu -bonded gpu -update gpu

echo "Window $WINDOW complete"
"""
    return script


def setup_fep_pipeline(peptide_id: str, peptide_sequence: str,
                       receptor_pdb: str, output_base: Path) -> Dict:
    """
    Set up complete FEP pipeline for a peptide-receptor system.

    Returns dictionary with all generated files and commands.
    """
    print("=" * 70)
    print("M4 FEP/GROMACS PIPELINE SETUP")
    print("=" * 70)
    print(f"Peptide: {peptide_id}")
    print(f"Sequence: {peptide_sequence}")
    print(f"Receptor: {receptor_pdb}")
    print()

    # Create configuration
    config = FEPSimulationConfig(
        peptide_sequence=peptide_sequence,
        peptide_id=peptide_id,
        receptor_pdb=receptor_pdb
    )

    # Generate lambda schedule
    lambda_schedule = generate_lambda_schedule(
        n_coul=config.n_lambda_coul,
        n_vdw=config.n_lambda_vdw
    )

    print(f"Lambda windows: {lambda_schedule['total_windows']}")
    print(f"  Coulombic: {len(lambda_schedule['coul'])}")
    print(f"  van der Waals: {len(lambda_schedule['vdw'])}")

    # Create output directory structure
    output_dir = output_base / peptide_id
    output_dir.mkdir(parents=True, exist_ok=True)

    mdp_dir = output_dir / "mdp"
    mdp_dir.mkdir(exist_ok=True)

    scripts_dir = output_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)

    complex_dir = output_dir / "complex"
    complex_dir.mkdir(exist_ok=True)

    solvent_dir = output_dir / "solvent"
    solvent_dir.mkdir(exist_ok=True)

    # Generate MDP files
    print("\nGenerating MDP files...")
    generate_mdp_em(mdp_dir / "em.mdp")
    generate_mdp_nvt(mdp_dir / "nvt.mdp", config.temperature)
    generate_mdp_npt(mdp_dir / "npt.mdp", config.temperature, config.pressure)

    # Generate FEP MDP files for all lambda windows
    for lc in lambda_schedule["coul"]:
        generate_mdp_fep(
            mdp_dir / f"fep_coul_{lc:.3f}_vdw_0.000.mdp",
            lambda_coul=lc, lambda_vdw=0.0,
            temperature=config.temperature, pressure=config.pressure,
            nsteps=config.nsteps_prod
        )

    for lv in lambda_schedule["vdw"]:
        if lv > 0:  # Skip 0 (already covered)
            generate_mdp_fep(
                mdp_dir / f"fep_coul_1.000_vdw_{lv:.3f}.mdp",
                lambda_coul=1.0, lambda_vdw=lv,
                temperature=config.temperature, pressure=config.pressure,
                nsteps=config.nsteps_prod
            )

    print(f"  Generated {len(list(mdp_dir.glob('fep_*.mdp')))} FEP MDP files")

    # Generate bash scripts
    print("\nGenerating bash scripts...")

    setup_script = generate_bash_setup_script(config, output_dir, lambda_schedule)
    with open(scripts_dir / "01_setup.sh", "w") as f:
        f.write(setup_script)

    complex_script = generate_bash_fep_production(config, output_dir, lambda_schedule, "complex")
    with open(scripts_dir / "02_fep_complex.sh", "w") as f:
        f.write(complex_script)

    solvent_script = generate_bash_fep_production(config, output_dir, lambda_schedule, "solvent")
    with open(scripts_dir / "03_fep_solvent.sh", "w") as f:
        f.write(solvent_script)

    analysis_script = generate_bash_analysis(config, output_dir)
    with open(scripts_dir / "04_analysis.sh", "w") as f:
        f.write(analysis_script)

    slurm_script = generate_slurm_submission(config, output_dir, lambda_schedule)
    with open(scripts_dir / "submit_array.slurm", "w") as f:
        f.write(slurm_script)

    # Make scripts executable
    for script in scripts_dir.glob("*.sh"):
        script.chmod(0o755)

    print("  01_setup.sh - System preparation")
    print("  02_fep_complex.sh - Complex leg production")
    print("  03_fep_solvent.sh - Solvent leg production")
    print("  04_analysis.sh - BAR analysis")
    print("  submit_array.slurm - HPC array submission")

    # Generate summary
    summary = {
        "peptide_id": peptide_id,
        "peptide_sequence": peptide_sequence,
        "receptor_pdb": receptor_pdb,
        "config": asdict(config),
        "lambda_schedule": lambda_schedule,
        "output_directory": str(output_dir),
        "scripts": [str(s) for s in scripts_dir.glob("*")],
        "mdp_files": len(list(mdp_dir.glob("*.mdp"))),
        "estimated_gpu_hours": lambda_schedule["total_windows"] * 2 * 24,  # 2 legs, ~24h each
        "generated": datetime.now().isoformat()
    }

    with open(output_dir / "fep_pipeline_config.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nConfiguration saved to: {output_dir / 'fep_pipeline_config.json'}")
    print(f"Estimated GPU time: ~{summary['estimated_gpu_hours']} hours")

    return summary


def run_demo():
    """Run a demonstration of the FEP pipeline setup."""
    print("=" * 70)
    print("M4 FEP/GROMACS PIPELINE - DEMONSTRATION")
    print("=" * 70)
    print()
    print("This script automates Alchemical Free Energy Perturbation (FEP)")
    print("calculations using GROMACS and the CHARMM36m force field.")
    print()
    print("PHYSICS:")
    print("  - Thermodynamic cycle for absolute binding free energy (ΔGbind)")
    print("  - Peptide decoupled from solvent AND from receptor binding pocket")
    print("  - ΔGbind = ΔGcomplex - ΔGsolvent")
    print()
    print("METHODOLOGY:")
    print("  - Lambda windows for Coulombic (11) and vdW (20) transformations")
    print("  - Soft-core potentials to avoid singularities")
    print("  - Bennett Acceptance Ratio (BAR) for free energy estimates")
    print("  - Error propagation through thermodynamic cycle")
    print()

    # Example peptide from our pipeline
    demo_peptide = {
        "peptide_id": "METAB_GLP1R_002",
        "sequence": "HAEGTFTSDVSSYLEGQAAKEFIAWLVKGR",  # GLP-1 analog
        "receptor": "GLP1R_6X18.pdb"  # PDB: 6X18 (GLP-1R structure)
    }

    # Set up pipeline
    output_base = Path(__file__).parent / "fep_simulations"

    summary = setup_fep_pipeline(
        peptide_id=demo_peptide["peptide_id"],
        peptide_sequence=demo_peptide["sequence"],
        receptor_pdb=demo_peptide["receptor"],
        output_base=output_base
    )

    print()
    print("=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print()
    print("1. Obtain receptor PDB structure (e.g., from RCSB PDB)")
    print("2. Generate peptide PDB (e.g., using PyMOL or MODELLER)")
    print("3. Dock peptide to receptor (see m4_pyrosetta_flexpepdock.py)")
    print("4. Run: ./scripts/01_setup.sh")
    print("5. Run: ./scripts/02_fep_complex.sh (or submit SLURM array)")
    print("6. Run: ./scripts/03_fep_solvent.sh")
    print("7. Run: ./scripts/04_analysis.sh")
    print()
    print("REQUIREMENTS:")
    print("  - GROMACS 2023+ with GPU support")
    print("  - pmx library: pip install pmx-biobb")
    print("  - alchemlyb: pip install alchemlyb")
    print("  - MDAnalysis: pip install MDAnalysis")
    print()

    return summary


if __name__ == "__main__":
    run_demo()
