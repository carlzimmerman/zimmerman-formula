"""Verify bit cap across every serialized rational, beyond LDL instrumentation."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];f=p/'exact_dual_001/certificate.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hashes={str(v.relative_to(r)):sha(v) for v in [f,Path(__file__)]};d=json.loads(f.read_text())
def vals(x):
 if isinstance(x,str) and '/' in x:yield F(x)
 elif isinstance(x,list):
  for v in x:yield from vals(v)
lengths={k:max([max(q.numerator.bit_length(),q.denominator.bit_length()) for q in vals(v)] or [0]) for k,v in d.items()};checks=dict(all_serialized_rationals_within_cap=max(lengths.values())<=20000,inputs_stable=all(sha(r/f)==h for f,h in hashes.items()));out=dict(checks=checks,maximum_bits=max(lengths.values()),by_field=lengths,input_sha256=hashes,clarification='run max_rational_bits instrumentation covers LDL entries only; complete certificate maximum is separately verified here')
(p/'dual_bit_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(checks,max(lengths.values()));assert all(checks.values())
