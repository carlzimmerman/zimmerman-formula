#!/usr/bin/env python3
"""Preserve first-run source provenance; fix NumPy scalar JSON serialization."""
import argparse,json
from pathlib import Path
from audit import source_audit,benchmark
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
result=dict(source=source_audit(),benchmark=benchmark())
result['benchmark']['independent_control_SE_caveat']='Reported independent-control delta SE treats sampled normalized weights as fixed; it does not fully propagate their random normalization. Use the independent-control point comparison as a diagnostic, not a rigorous confidence bound.'
encoded=json.dumps(result,indent=2,default=lambda v:v.item())+'\n'
Path(a.output).write_text(encoded)
print(encoded)
