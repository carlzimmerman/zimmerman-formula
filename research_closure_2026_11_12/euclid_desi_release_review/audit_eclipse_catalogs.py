#!/usr/bin/env python3
"""Reproduce the blinded ECLIPSE metadata audit from two local ZIP files.

No network access or theory calculation. These are quality cuts for this
metadata audit, specified before any formula scoring, not a preregistered
or sealed prospective experiment. Only metadata validity and published
quality flags are used; no acceleration or model-agreement residual is read.
"""

import argparse
import csv
import hashlib
import io
import json
import math
from collections import Counter
from pathlib import Path
from zipfile import ZipFile


DEFAULT_DATA_DIR = Path('/private/tmp/euclid_dr1_review_20261112')
FILES = {
    'object': (
        'ECLIPSE_object_catalogue.zip',
        '56433fecbdc459046ffe9eca44bb4dcf',
        'ECLIPSE_object_catalogue/ECLIPSE_object_catalogue.csv',
    ),
    'physical': (
        'ECLIPSE_D_dr1_redshifts_and_physical_properties.zip',
        'cb31dbd65a3586ab13f52cff2df67f6b',
        'eclipse_dr1_catalogue_key_v20261103.csv',
    ),
}
LIGHT_FIELDS = (
    'eclipse_effective_radius',
    'eclipse_sersic_index',
    'eclipse_luminosity_rband_med',
    'eclipse_mass_to_light_rband_med',
)


def positive(value):
    """Reject missing strings, non-finite values and the -99 sentinel."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and number > 0


def yes(value):
    # The released CSVs use the literal strings True and False.
    return value == 'True'


def read_table(data_dir, spec):
    name, expected_md5, member = spec
    path = data_dir / name
    raw = path.read_bytes()
    md5 = hashlib.md5(raw).hexdigest()
    if md5 != expected_md5:
        raise ValueError(f'{name}: MD5 mismatch; expected {expected_md5}, got {md5}')
    with ZipFile(io.BytesIO(raw)) as archive:
        reader = csv.DictReader(io.StringIO(archive.read(member).decode('utf-8-sig')))
        columns = reader.fieldnames
        rows = list(reader)
    return rows, {
        'filename': name,
        'member': member,
        'bytes': len(raw),
        'md5': md5,
        'sha256': hashlib.sha256(raw).hexdigest(),
        'rows': len(rows),
        'columns': len(columns),
    }


def audit(data_dir):
    objects, object_info = read_table(data_dir, FILES['object'])
    physical, physical_info = read_table(data_dir, FILES['physical'])
    by_id = {row['Unique_Identifier']: row for row in objects}
    if len(by_id) != len(objects):
        raise ValueError('Object identifiers are not unique')
    if len({row['unique_identifier'] for row in physical}) != len(physical):
        raise ValueError('Physical-property identifiers are not unique')
    pairs = [(by_id[row['unique_identifier']], row) for row in physical]
    mismatches = sum(a['Expert_Grade'] != b['lens_grade'] for a, b in pairs)
    if mismatches:
        raise ValueError(f'{mismatches} grade mismatches across the identifier join')

    stages = (
        ('all_AB', lambda a, b: True),
        ('grade_A', lambda a, b: a['Expert_Grade'] == 'A'),
        ('consensus_success', lambda a, b: yes(b['lens_model_success'])
         and b['lens_model_consensus_75'] == 'Success'),
        ('paper_final_sample', lambda a, b: yes(b['final_sample'])),
        ('valid_mass_and_light', lambda a, b:
         positive(b['eclipse_log_survived_mass_med'])
         and all(positive(b[field]) for field in LIGHT_FIELDS)),
        ('no_large_system_warning', lambda a, b: not yes(a['large_system_warning'])),
        ('positive_vetted_deflector_specz', lambda a, b: positive(a['desi_deflector_specz'])),
    )
    remaining = pairs
    funnel = []
    for name, keep in stages:
        remaining = [(a, b) for a, b in remaining if keep(a, b)]
        funnel.append({'stage': name, 'n': len(remaining)})

    # Source spectroscopic redshifts are absent, so this cannot count a
    # source-and-deflector spectroscopic gold sample.
    return {
        'scope': 'Metadata quality audit before any formula scoring; no preregistration claimed.',
        'archives': [object_info, physical_info],
        'join': {
            'object_key': 'Unique_Identifier',
            'physical_key': 'unique_identifier',
            'matched_rows': len(pairs),
            'grade_mismatches': mismatches,
        },
        'object_grades': dict(Counter(row['Expert_Grade'] for row in objects)),
        'funnel': funnel,
        'valid_light_fields': list(LIGHT_FIELDS),
        'clean_deflector_specz_candidate_ids': [
            {'unique_identifier': a['Unique_Identifier'], 'name': a['euclj_name']}
            for a, b in remaining
        ],
        'both_specz_gold_sample_count': None,
        'both_specz_limitation': 'No source spectroscopic redshift or paired-source linkage in the two CSVs.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument('--reference', type=Path,
                        help='Compare all funnel stages and candidate IDs with an existing audit JSON')
    parser.add_argument('--output', type=Path, help='Write JSON here instead of stdout')
    args = parser.parse_args()
    result = audit(args.data_dir)
    if args.reference:
        reference = json.loads(args.reference.read_text())
        expected = [(row['stage'], row['n']) for row in reference['funnel']]
        actual = [(row['stage'], row['n']) for row in result['funnel']]
        if actual != expected:
            raise ValueError(f'Funnel differs from reference: {actual!r} versus {expected!r}')
        if result['clean_deflector_specz_candidate_ids'] != reference['clean_deflector_specz_candidate_ids']:
            raise ValueError('Candidate identifiers or names differ from reference')
        result['reference_verification'] = {
            'path': str(args.reference),
            'all_funnel_stages_match': True,
            'all_candidate_identifiers_and_names_match_in_order': True,
            'candidate_count': len(result['clean_deflector_specz_candidate_ids']),
        }
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
