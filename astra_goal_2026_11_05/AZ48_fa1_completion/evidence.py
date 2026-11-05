#!/usr/bin/env python3
"""Authenticate local evidence before numerical aggregation; never run old drivers."""
import json,platform
from pathlib import Path
import numpy as np
import scipy
import audit_inputs as A

class EvidenceError(ValueError):pass

def source_hashes(hashes):
    if not hashes:raise EvidenceError('Missing source identities')
    for name,digest in hashes.items():
        relative=Path(name);path=(A.ROOT/relative).resolve()
        if relative.is_absolute() or A.ROOT.resolve() not in path.parents:raise EvidenceError('Source path outside repository')
        if not path.is_file() or A.sha(path)!=digest:raise EvidenceError('Stale source: '+name)

def versions(value):
    current=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__)
    if any(current.get(key)!=v for key,v in value.items()):raise EvidenceError('Numerical environment changed')

def check_report(path,total,expected_failures=()):
    obj=json.loads(path.read_text());source_hashes(obj['source_hashes'])
    if 'versions' in obj:versions(obj['versions'])
    checks=obj['checks'];names=[c['name'] for c in checks]
    if len(checks)!=total or len(set(names))!=total or obj['total']!=total:raise EvidenceError('Incomplete or duplicate check coverage')
    if any(type(c['passed']) is not bool for c in checks):raise EvidenceError('Nonboolean check')
    failed={c['name'] for c in checks if not c['passed']}
    if failed!=set(expected_failures) or obj['passed']!=total-len(failed):raise EvidenceError('Unexpected known-answer/control result')
    return dict(path=A.relative(path),sha256=A.sha(path),total=total,expected_failures=sorted(failed))

def authenticate_sample(field_dir,sample_dir):
    field_dir=Path(field_dir);sample_dir=Path(sample_dir)
    result=json.loads((field_dir/'result.json').read_text())
    with np.load(field_dir/'checkpoint.npz',allow_pickle=False) as saved:field_state=json.loads(str(saved['state']))
    if field_state['status']!='complete' or field_state['identity']!=result['identity']:raise EvidenceError('Incomplete field or mismatched identity')
    if set(field_state['outputs'])!={'field.npy','result.json'}:raise EvidenceError('Incomplete field artifact list')
    for name,digest in field_state['outputs'].items():
        if A.sha(field_dir/name)!=digest:raise EvidenceError('Changed field artifact: '+name)
    if result['field_sha256']!=field_state['outputs']['field.npy']:raise EvidenceError('Field hash mismatch')
    source_hashes(result['identity']['source_hashes']);versions(result['identity']['versions'])
    samples=json.loads((sample_dir/'samples.json').read_text());state=json.loads((sample_dir/'sampling_checkpoint.json').read_text())
    if state['status']!='complete' or state['result_sha256']!=A.sha(sample_dir/'samples.json'):raise EvidenceError('Incomplete or changed sampling output')
    source_hashes(samples['source_hashes'])
    if samples['field_identity']!=result['identity'] or samples['field_sha256']!=result['field_sha256'] or samples['field_result_sha256']!=A.sha(field_dir/'result.json'):raise EvidenceError('Samples do not belong to this field')
    expected=dict(field_result_sha256=samples['field_result_sha256'],field_sha256=samples['field_sha256'],mutate=samples['mutate'],source_hashes=samples['source_hashes'],versions=result['identity']['versions'])
    if state['identity']!=expected:raise EvidenceError('Sampling checkpoint identity mismatch')
    if samples['mutate'] and 'mutate' not in sample_dir.parts:raise EvidenceError('Mutation output outside mutate tree')
    provenance=dict(field_result=A.relative(field_dir/'result.json'),field_result_sha256=A.sha(field_dir/'result.json'),field_sha256=result['field_sha256'],samples=A.relative(sample_dir/'samples.json'),samples_sha256=A.sha(sample_dir/'samples.json'))
    return samples,provenance

def prerequisite_specs():
    return [
      ('bullet_source_checks.json',24,[]),('mutate/bullet_source_checks.json',24,['selector_isotropic','selector_deep_point']),
      ('grid3d_checks.json',21,[]),('mutate/grid3d_checks.json',21,['canonical_selector_8','alt_selector_8','canonical_selector_16','alt_selector_16','mixed_selector_independent']),
      ('spherical_boundary_checks.json',16,[]),('newton_checks.json',22,[]),('sampling_checks.json',42,[]),
      ('mutate/sampling_checks.json',42,['isotropic_sample_invariant','isotropic_disc_invariant_32','isotropic_disc_fraction_32','isotropic_disc_invariant_64','isotropic_disc_fraction_64','rotated_sample_invariant','rotated_disc_invariant_32','rotated_disc_fraction_32','rotated_disc_invariant_64','rotated_disc_fraction_64']),
      ('convergence_checks.json',58,[]),('mutate/convergence_checks.json',58,['canonical_point_resolution','canonical_point_box','alt_point_resolution','alt_point_box']),
      ('worker_verified/contract_e/checks.json',12,[]),('worker_verified/homotopy_b/checks.json',12,[]),
      ('sample_resume_verified/contract_c/checks.json',9,[]),('sample_resume_verified/mutation_b/mutate/checks.json',9,[]),
      ('sampling_verified/contract_c/checks.json',11,[])]

def prerequisites():
    records=[];errors=[]
    for name,total,failures in prerequisite_specs():
        try:records.append(check_report(A.HERE/name,total,failures))
        except (EvidenceError,OSError,KeyError,ValueError,TypeError) as exc:errors.append(dict(path=name,error=str(exc)))
    return dict(verified=not errors,records=records,errors=errors)
