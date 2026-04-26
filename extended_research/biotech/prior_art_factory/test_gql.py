import requests

pdb_id = "1BYZ"
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
gql_resp = requests.post("https://data.rcsb.org/graphql", json={"query": graphql_query}).json()
print(gql_resp)
