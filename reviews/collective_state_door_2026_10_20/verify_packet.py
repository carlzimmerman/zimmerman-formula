"""Check provenance, version reconciliation and preservation, not physics."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


old = ROOT / 'reviews/polarization_link_2026_10_20'
old_record = read(old / 'VERIFICATION.json')
prior = []
for entry in old_record['earlier_packets']:
    folder = ROOT / 'reviews' / entry['packet']
    inventory = folder / 'PACKET_SHA256.json'
    items = read(inventory)['files']
    bad = [p for p, expected in items.items()
           if digest(folder / p) != expected]
    prior.append(dict(packet=entry['packet'], files_checked=len(items),
                      inventory_matches_previous_pin=
                      digest(inventory) == entry['inventory_sha256'],
                      mismatches=bad))
items = read(old / 'PACKET_SHA256.json')['files']
prior.append(dict(packet=old.name, files_checked=len(items),
                  inventory_matches_previous_pin=digest(old / 'PACKET_SHA256.json') ==
                  '61ea8ac28f9b3c8a3c9792866021178a85d9eba374c0f9dd67b2009778d43553',
                  mismatches=[p for p, expected in items.items()
                              if digest(old / p) != expected]))

pins = []
historical_index = None
for file, key in [('finite_host/source_hashes.json', 'sources'),
                  ('topology/source_hashes.json', 'inputs'),
                  ('ROOT_SOURCE_PINS.json', 'sources'),
                  ('recent/update_source_hashes.json', 'sources')]:
    for row in read(PACKET / file)[key]:
        expected = row.get('sha256', row.get('sha256_actual'))
        actual = digest(ROOT / row['path'])
        pin = dict(record=file, path=row['path'], expected=expected,
                   actual=actual, valid=actual == expected)
        # A later owner edit to a campaign index does not alter an exact
        # historical observation. Verify that index against its committed
        # assessment bytes; do not refresh the old hash to silence staleness.
        if file == 'recent/update_source_hashes.json' and row['path'] == 'campaign_fresh_gravity/LEDGER.md':
            assessment = row['new_assessment']
            raw = subprocess.check_output(['git','show',
                  assessment['head'] + ':' + row['path']], cwd=ROOT)
            pinned = hashlib.sha256(raw).hexdigest()
            pin.update(valid=pinned == expected,
                       verification_mode='exact committed historical index',
                       pinned_revision=assessment['head'],
                       pinned_revision_sha256=pinned,
                       current_later_bytes_differ=actual != expected)
            historical_index = pin
        pins.append(pin)

new_rows = {row['path']: row for row in
            read(PACKET / 'recent/update_source_hashes.json')['sources']}
reconciled = []
for row in read(PACKET / 'recent/source_hashes.json')['sources']:
    actual = digest(ROOT / row['path'])
    expected = row['sha256_actual']
    if actual == expected:
        pins.append(dict(record='recent/source_hashes.json', path=row['path'],
                         expected=expected, actual=actual))
    else:
        new = new_rows.get(row['path'], {})
        valid = (new.get('classification') == 'new_version_since_old_pin'
                 and (actual == new.get('sha256_actual') or
                      (row['path'] == 'campaign_fresh_gravity/LEDGER.md'
                       and historical_index is not None and historical_index['valid'])))
        reconciled.append(dict(path=row['path'], old_pin=expected,
                               current=actual, new_pin=new.get('sha256_actual'),
                               documented_version_change=valid))

finite = read(PACKET / 'audit_finite/provenance.json')
spectral = read(PACKET / 'audit_spectral/provenance.json')
profile = read(PACKET / 'audit_finite/profile_gate_provenance.json')
proofs = [finite['reviewed_proof']] + spectral['reviewed_proofs']
# The profile review uses the same path/hash convention, independently of
# whether it is serialized as one object or a one-element list.
if 'reviewed_proof' in profile:
    proofs.append(profile['reviewed_proof'])
else:
    proofs.extend(profile['reviewed_files'])
review_bad = [row['path'] for row in proofs
              if digest(ROOT / row['path']) != row['sha256']]
required = {str(PACKET.relative_to(ROOT) / p) for p in
            ('finite_host/RESULT.md', 'topology/RESULT.md',
             'SPECTRAL_RECEIPT.md', 'PROFILE_GATE.md')}
checks = dict(
    five_prior_packets_preserved=all(not x['mismatches'] and
                                    x['inventory_matches_previous_pin'] for x in prior),
    relied_on_sources_fresh_or_verified_at_exact_historical_index=all(
        x.get('valid', x['expected'] == x['actual']) for x in pins),
    historical_source_changes_explicitly_reconciled=all(
        x['documented_version_change'] for x in reconciled),
    four_required_analytic_notes_reviewed=required.issubset({x['path'] for x in proofs}),
    reviewed_proof_bytes_fresh=not review_bad,
    finite_audit_report_hash_matches=digest(ROOT / finite['audit_report']['path']) ==
                                    finite['audit_report']['sha256'],
    spectral_audit_report_hash_matches=digest(ROOT / spectral['output']['path']) ==
                                      spectral['output']['sha256'],
    profile_gate_review_hash_matches=digest(ROOT / profile['audit_report']['path']) ==
                                    profile['audit_report']['sha256'],
    root_records_present=all((PACKET / p).is_file() for p in
                            ('TARGET.md', 'README.md', 'NEXT.md', 'NOVELTY_DELTA.md')))
record = dict(checkpoint='collective-state-door-2026-10-20',
              recorded_utc=datetime.now(timezone.utc).isoformat(),
              assessment_base='cc07e00a3ba0f2917f16d834b6ca54bcd93a4dcf',
              latest_scientific_review_cutoff='177591c05a384bc07c819e3fe0d5517aa8798cb4',
              observed_head=subprocess.check_output(['git','rev-parse','HEAD'],
                                                   cwd=ROOT,text=True).strip(),
              purpose='Source/proof freshness and immutable-history preservation; not a mathematical or empirical certificate',
              checks=checks, earlier_packets=prior,
              earlier_packet_file_count=sum(x['files_checked'] for x in prior),
              pins=pins, reconciled_historical_versions=reconciled,
              reviewed_proofs=proofs, review_mismatches=review_bad,
              audit_artifact_hashes={str(p.relative_to(PACKET)):digest(p)
                                    for folder in ('audit_finite','audit_spectral')
                                    for p in sorted((PACKET/folder).glob('*')) if p.is_file()},
              scientific_runs=0, symbolic_package_runs=0, parameter_scans=0,
              target_reached=False, empirical_profile_inversion_executed=False,
              new_fitted_parameters=0)
(PACKET / 'VERIFICATION.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(dict(checks=checks,
                      prior_files=record['earlier_packet_file_count'],
                      source_pin_checks=len(pins),
                      documented_source_versions=len(reconciled)),indent=2))
if not all(checks.values()):
    raise SystemExit(1)
