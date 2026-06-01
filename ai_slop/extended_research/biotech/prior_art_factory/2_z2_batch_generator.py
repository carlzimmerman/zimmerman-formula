import json
import os

# Z^2 Theoretical Ligand Library
# 10-mers utilizing heavy aromatic anchors flanked by rigid stabilizing residues
Z2_LIGANDS = [
    {"suffix": "Z2_ARO_W1", "seq": "PWLPTQWLLP"},
    {"suffix": "Z2_ARO_Y1", "seq": "YWPLQLWTPP"},
    {"suffix": "Z2_RIG_P1", "seq": "PPLWYWPPLQ"},
    {"suffix": "Z2_SEL_R1", "seq": "RWPKWGELTK"}
]

def generate_alphafold_batches():
    if not os.path.exists("z2_batches"):
        os.makedirs("z2_batches")

    try:
        with open("sanitized_targets.json", "r") as f:
            targets = json.load(f)
    except FileNotFoundError:
        print("[!] Error: sanitized_targets.json not found. Run 1_pdb_symmetry_miner.py first.")
        return

    for target in targets:
        batch_jobs = []
        
        target_name = target["target_id"]
        sequence = target["sequence"]
        sym_count = target["symmetry_count"]

        # Generate a job for each theoretical ligand
        for ligand in Z2_LIGANDS:
            job_name = f"{target_name}_{ligand['suffix']}"
            
            job = {
                "name": job_name,
                "sequences": [
                    {
                        "proteinChain": {
                            "sequence": sequence,
                            "count": sym_count
                        }
                    },
                    {
                        "proteinChain": {
                            "sequence": ligand["seq"],
                            "count": 1
                        }
                    }
                ]
            }
            batch_jobs.append(job)

        # Write the server-ready batch file
        filename = f"z2_batches/{target_name}_batch.json"
        with open(filename, "w") as f:
            json.dump(batch_jobs, f, indent=2)
            
        print(f"[+] Generated spatial mapping batch: {filename}")

if __name__ == "__main__":
    print("[*] Initializing Z^2 Geometric Batch Generator...")
    generate_alphafold_batches()
    print("[*] All batches compiled and ready for topological simulation.")
