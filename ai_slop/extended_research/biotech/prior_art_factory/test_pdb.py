import requests

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
                    "value": "de novo"
                }
            }
        ]
    },
    "request_options": {
        "paginate": {
            "start": 0,
            "rows": 10
        }
    },
    "return_type": "entry"
}

resp = requests.post("https://search.rcsb.org/rcsbsearch/v2/query", json=search_payload)
print(resp.status_code)
if resp.status_code == 200:
    print([hit['identifier'] for hit in resp.json().get('result_set', [])])
else:
    print(resp.text)
