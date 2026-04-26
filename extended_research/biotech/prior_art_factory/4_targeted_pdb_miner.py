import requests
import json
import time

# A curated list of explicitly high-value therapeutic targets extracted from the pipelines.
# These PDB IDs represent multi-billion dollar markets (Autoimmune, Metabolic, Neurological).
TARGETED_PDBS = [
    "1TNF", # TNF-alpha (Humira target - Autoimmune)
    "1ALU", # IL-6 (Actemra target - Autoimmune)
    "6X18", # GLP-1R (Ozempic target - Metabolic)
    "6ORV", # GIPR (Mounjaro target - Metabolic)
    "1IYT", # Amyloid-beta (Neurological)
    "1XQ8", # Alpha-synuclein (Parkinson's - Neurological)
    "2SOD", # SOD1 (ALS - Neurological)
    "4Y6O", # TNF-alpha variant (Autoimmune)
    "1TNR", # TNFR1 (Autoimmune)
    "4HR9", # IL-17A (Cosentyx target - Autoimmune)
    "4QHU", # IL-23 (Skyrizi target - Autoimmune)
    "1F45", # IL-1beta (Autoimmune)
    "1ITB", # IL-2 (Autoimmune/Cancer)
    "6BBU", # JAK1 (Rinvoq target - Autoimmune)
    "1YVJ", # JAK3 (Autoimmune)
    "4GVJ", # TYK2 (Autoimmune)
    "5RV7", # SARS-CoV-2 Mpro (Viral/Protease - structurally symmetric)
    "1I8L", # IL-10 (Autoimmune)
    "3V4V", # IL-22 (Autoimmune)
    "3V2Y", # IL-13 (Autoimmune)
    "3CU7", # IL-4 (Autoimmune)
    "5O3T", # Tau protein (Alzheimer's - Neurological)
    "1FKN", # Huntingtin (Huntington's - Neurological)
    "6VNO", # LRRK2 (Parkinson's - Neurological)
    "2NT0", # PINK1 (Parkinson's - Neurological)
    "1AGQ", # Parkin (Parkinson's - Neurological)
]

def fetch_targeted_symmetries():
    print(f"[*] Initiating targeted 'Sniper' query for {len(TARGETED_PDBS)} high-value structural targets...")
    
    sanitized_targets = []
    
    for idx, pdb_id in enumerate(TARGETED_PDBS):
        print(f"[*] Fetching sequence and symmetry data for specific target: {pdb_id}")
        
        # Fetching sequence and stoichiometry data via GraphQL
        graphql_query = f"""
        {{
          entry(entry_id: "{pdb_id}") {{
            polymer_entities {{
              entity_poly {{
                pdbx_seq_one_letter_code_can
              }}
            }}
            assemblies {{
              rcsb_struct_symmetry {{
                symbol
              }}
            }}
          }}
        }}
        """
        try:
            gql_resp = requests.post("https://data.rcsb.org/graphql", json={"query": graphql_query}).json()
            if 'errors' in gql_resp:
                print(f"[!] Target {pdb_id} returned GraphQL error, skipping.")
                continue
                
            entry_data = gql_resp['data']['entry']
            if not entry_data:
                print(f"[!] Target {pdb_id} not found in PDB, skipping.")
                continue
            
            # Extract sequence and symmetry
            seq = entry_data['polymer_entities'][0]['entity_poly']['pdbx_seq_one_letter_code_can'].replace('\n', '')
            sym = "C1" # Default to monomer if no symmetry found
            
            if entry_data.get('assemblies') and len(entry_data['assemblies']) > 0:
                assembly = entry_data['assemblies'][0]
                if assembly.get('rcsb_struct_symmetry') and len(assembly['rcsb_struct_symmetry']) > 0:
                    sym = assembly['rcsb_struct_symmetry'][0]['symbol']
            
            # Map biological symmetry to our geometric target naming convention
            sym_count = 2 if "C2" in sym else (3 if "C3" in sym else (4 if "C4" in sym else (1 if "C1" in sym else 2)))
            
            target_data = {
                "target_id": f"TARGET_{pdb_id}_{sym}_{str(idx+1).zfill(3)}",
                "source_pdb": pdb_id,
                "sequence": seq,
                "symmetry_count": sym_count
            }
            sanitized_targets.append(target_data)
            
        except Exception as e:
            print(f"[!] Error processing {pdb_id}: {e}")
            continue
            
        time.sleep(0.2) # Polite API rate limiting

    # Save to local pipeline feed
    output_file = "sanitized_targets.json"
    with open(output_file, "w") as f:
        json.dump(sanitized_targets, f, indent=4)
    
    print(f"[+] Successfully banked {len(sanitized_targets)} high-value targets to {output_file}")

if __name__ == "__main__":
    fetch_targeted_symmetries()
