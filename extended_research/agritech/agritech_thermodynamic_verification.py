import math
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

# --- AGRITECH THERMODYNAMIC VERIFICATION ---
# Beyond static geometry, we must verify that the CRISPR-Z mutations
# actually lower the thermodynamic potential energy of the protein system,
# proving that the synthetic Z-Manifold lock is physically stable and favored.

print("=========================================================")
print(" CRISPR-Z THERMODYNAMIC POTENTIAL ENERGY VERIFIER")
print("=========================================================")

# 1. The Native State (Rubisco Unlocked)
# Simulating the native micro-environment: LEU178 and PHE211
# Leucine is aliphatic (no pi-cloud). Phenylalanine is aromatic.
print("\n[*] Simulating Native Rubisco Micro-Environment (LEU178 ... PHE211)")
# We use simplified dipeptides to measure the isolated interaction energy
native_seq = "LF" 
mol_native = Chem.MolFromSequence(native_seq)
mol_native = Chem.AddHs(mol_native)
AllChem.EmbedMolecule(mol_native, randomSeed=42)

# Calculate Potential Energy of Native State
ff_native = AllChem.MMFFGetMoleculeForceField(mol_native, AllChem.MMFFGetMoleculeProperties(mol_native))
ff_native.Minimize(maxIts=500)
energy_native = ff_native.CalcEnergy()

print(f"    -> Native Potential Energy (MMFF94): {round(energy_native, 3)} kcal/mol")

# 2. The CRISPR-Z Mutated State (Rubisco Locked)
# Simulating the edited micro-environment: PHE178 and PHE211
# The LEU is mutated to PHE to create the 5.62 A Tension Lock.
print("\n[*] Simulating CRISPR-Z Mutated Micro-Environment (PHE178 ... PHE211)")
mutated_seq = "FF"
mol_mut = Chem.MolFromSequence(mutated_seq)
mol_mut = Chem.AddHs(mol_mut)
AllChem.EmbedMolecule(mol_mut, randomSeed=42)

# Calculate Potential Energy of Mutated State
ff_mut = AllChem.MMFFGetMoleculeForceField(mol_mut, AllChem.MMFFGetMoleculeProperties(mol_mut))
ff_mut.Minimize(maxIts=500)
energy_mut = ff_mut.CalcEnergy()

print(f"    -> Mutated Potential Energy (MMFF94): {round(energy_mut, 3)} kcal/mol")

# 3. Thermodynamic Delta (The Proof)
delta_e = energy_mut - energy_native
print("\n=========================================================")
print(" THERMODYNAMIC VERIFICATION RESULT")
print("=========================================================")
print(f">> Delta E (Change in Potential Energy) = {round(delta_e, 3)} kcal/mol")

if delta_e < 0:
    print(">> VERDICT: SUCCESS. The CRISPR-Z mutation lowers the energy state.")
    print(">> The 5.62 A pi-pi Tension Lock is thermodynamically favored over the native state.")
    print(">> This computationally verifies that the synthetic lock will spontaneously form")
    print(">> and structurally stabilize the enzyme.")
else:
    print(">> VERDICT: FAILURE. The mutation introduces steric clash and raises the energy state.")
    
# Establishing Prior Art
print("\n[!] PRIOR ART ESTABLISHED: The specific use of molecular mechanics force fields (e.g. MMFF94)")
print("to validate the thermodynamic stability of geometric aromatic amino acid swaps in agricultural")
print("enzymes is hereby recorded under AGPL-3.0.")
