#!/usr/bin/env python3
"""Independent identifier/header fixtures and a separate false-evidence mutation."""
import json
from pathlib import Path
import audit_inputs as A
checks=[]
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
for original,expected in [('J0008-0004','J0008-0004'),('002907.80-005550.0','J0029-0055'),('SDSS J0037-0942','J0037-0942'),('NGC4486',None),('name',None)]:
 check('identifier_'+original,A.lens_id(original)==expected)
text='# a catalogue\nrecno\tSDSS\tsigma\tMType\n1\tJ0008-0004\t200\tE\n'
i,header=A.table_header(text);check('independent_fixture_header',i==1 and header==['recno','SDSS','sigma','MType'])
check('dispersion_morphology_not_rotation',A.rotation_columns(header)==[])
check('photometric_V_not_rotation',A.rotation_columns(['name','V','Vmag','sigma','e_sigma','MType'])==[])
check('explicit_rotation_fields_recognized',A.rotation_columns(['name','V/sigma','lambda_R','rotation_class'])==['V/sigma','lambda_R','rotation_class'])
# The independently specified required observable is a measured velocity ratio.
allowed={'V/sigma','lambda_R','rotation_class'}
main_claim=A.rotation_columns(header);mutated_claim=['sigma']
main_acceptable=all(name in allowed for name in main_claim)
mutant_acceptable=all(name in allowed for name in mutated_claim)
check('main_does_not_fabricate_evidence',main_acceptable)
check('dispersion_as_rotation_mutation_rejected',not mutant_acceptable)
obj=dict(checks=checks,passed=sum(x['passed'] for x in checks),total=len(checks),source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),Path(A.__file__).resolve()]},scope='Parser and evidence-type controls only; no observed lens class or physical grade')
A.atomic(A.HERE/'audit_checks.json',obj)
A.atomic(A.HERE/'mutate/false_rotation_evidence.json',dict(header=header,claimed_rotation_fields=mutated_claim,accepted=mutant_acceptable,required_observable='Measured rotation evidence, not dispersion alone',source_hashes=obj['source_hashes']))
print(json.dumps(dict(passed=obj['passed'],total=obj['total']),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
