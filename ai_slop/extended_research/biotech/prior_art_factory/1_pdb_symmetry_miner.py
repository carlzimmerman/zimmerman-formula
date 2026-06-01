import requests
import json
import time

def fetch_symmetric_targets(max_results=50):
    print(f"[*] Initiating geometric query for {max_results} symmetric macromolecular targets...")
    
    # RCSB PDB Search API payload
    # Looking for: Resolution < 2.0A, Homo-oligomers, no membrane components
    search_payload = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entry_info.resolution_combined",
                        "operator": "less_or_equal",
                        "value": 2.0
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "struct_keywords.pdbx_keywords",
                        "operator": "contains_words",
                        "value": "de novo" # Sanitized search space
                    }
                }
            ]
        },
        "request_options": {
            "paginate": {
                "start": 0,
                "rows": max_results
            }
        },
        "return_type": "entry"
    }

    response = requests.post("https://search.rcsb.org/rcsbsearch/v2/query", json=search_payload)
    if response.status_code != 200:
        print(f"[!] API Error or no results found. Status: {response.status_code}")
        print(response.text)
        return []

    pdb_ids = [hit['identifier'] for hit in response.json().get('result_set', [])]
    
    sanitized_targets = []
    
    for idx, pdb_id in enumerate(pdb_ids):
        print(f"[*] Fetching sequence and symmetry data for spatial target: {pdb_id}")
        
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
            entry_data = gql_resp['data']['entry']
            
            # Extract sequence and symmetry
            seq = entry_data['polymer_entities'][0]['entity_poly']['pdbx_seq_one_letter_code_can'].replace('\n', '')
            sym = entry_data['assemblies'][0]['rcsb_struct_symmetry'][0]['symbol'] if (entry_data.get('assemblies') and entry_data['assemblies'][0].get('rcsb_struct_symmetry')) else "C2"
            
            # Map biological symmetry to our geometric target naming convention
            sym_count = 2 if "C2" in sym else (3 if "C3" in sym else (4 if "C4" in sym else 2))
            
            target_data = {
                "target_id": f"TARGET_{sym}_{str(idx+1).zfill(3)}",
                "source_pdb": pdb_id,
                "sequence": seq,
                "symmetry_count": sym_count
            }
            sanitized_targets.append(target_data)
            
        except Exception as e:
            continue
            
        time.sleep(0.2) # Polite API rate limiting

    # Save to local pipeline feed
    with open("sanitized_targets.json", "w") as f:
        json.dump(sanitized_targets, f, indent=4)
    
    print(f"[+] Successfully banked {len(sanitized_targets)} geometric targets to sanitized_targets.json")

if __name__ == "__main__":
    fetch_symmetric_targets(max_results=50)
