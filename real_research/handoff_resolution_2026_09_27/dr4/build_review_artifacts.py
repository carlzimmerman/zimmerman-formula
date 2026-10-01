#!/usr/bin/env python3
from pathlib import Path
import hashlib, json
O=Path(__file__).resolve().parent; R=O.parents[2]
def sha(b): return hashlib.sha256(b).hexdigest()
f=R/'prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md'
before=f.read_bytes(); addition=(O/'AMENDMENT13_DRAFT_NOT_FILED.md').read_bytes()
after=before+b'\n\n'+addition
(O/'PREREGISTRATION_DR4_PROSPECTIVE.md').write_bytes(after)
assert after[:len(before)]==before
receipt=f'''NOT FILED — LOCAL PROSPECTIVE RECEIPT, following AMENDMENT12_HASH.txt's format.
AMENDMENT 13 -- correction of recorded four-form variant B-prime's stability;
  conditional double-filtered P2 wide-binary law H and seven-bin xi protocol.
date: 2026-09-27 (draft; actual filing date must be recorded on filing)
sha256(PREREGISTRATION_DR4.md) before proposed Amendment 13: {sha(before)}
sha256(PREREGISTRATION_DR4_PROSPECTIVE.md) after exact local append: {sha(after)}
sha256(AMENDMENT13_DRAFT_NOT_FILED.md): {sha(addition)}
added: F6 secant/tangent correction, negative longitudinal band, physical-kappa versus
  estimator-kappa distinction; conditional H ceilings and xi statistics; explicit
  uncompleted covariance/contamination/orbit/coverage gates and no-inference fallback.
unchanged: every byte of the existing registration; live pipeline files and HASH receipts.
  KAPPA = 1/2 FITTED, NOT DERIVED. Both a0 footings reported.
against interest: B-prime's 2-kAU shifts cannot be scored; xi remains a free length;
  XR22 Fisher precision is conditional and is not promised DR4 precision.
source: XR31 independent full control/main reruns; XR22 exact reruns tracked in
  full_records.json; forecast_audit_results.json; AUDIT.md and amendment draft.
status: review artifact only. This file is not AMENDMENT13_HASH.txt, and neither the
  frozen registration nor a live hash receipt was changed. Any draft revision requires
  recomputing this prospective receipt. Outstanding scientific gates remain explicit.
'''
(O/'PROSPECTIVE_HASH_RECEIPT.txt').write_text(receipt)
inputs=[]
for rel in ['prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md','prep_2026/gaia_dr4_prep/AMENDMENT12_HASH.txt','kappa_closure/k04_F6_CORRECTION_2026-09-27.md']:
 p=R/rel;inputs.append(dict(path=rel,sha256=sha(p.read_bytes())))
for p in (R/'real_research/cross_thread_review_2026_09_26').glob('XR2[2]*'):
 if p.is_file():inputs.append(dict(path=str(p.relative_to(R)),sha256=sha(p.read_bytes())))
for p in (R/'real_research/cross_thread_review_2026_09_26').glob('XR31*'):
 if p.is_file():inputs.append(dict(path=str(p.relative_to(R)),sha256=sha(p.read_bytes())))
(O/'source_hashes.json').write_text(json.dumps(inputs,indent=2))
print('append-only prefix verified; source registration',sha(before));print('prospective',sha(after))
