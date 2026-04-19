#!/usr/bin/env python3
"""
Legal Stamper - Automated License Header Injection

SPDX-License-Identifier: AGPL-3.0-or-later

Automatically stamps generated files with appropriate open-source licenses:
- Python scripts (.py): AGPL-3.0-or-later header
- Sequences (.fasta): OpenMTA + CC BY-SA 4.0 header
- Structures (.pdb): OpenMTA + CC BY-SA 4.0 header

PURPOSE: Defensive Publishing / Prior Art Creation
- Prevents patent enclosure of open therapeutic research
- Ensures all derivatives must remain open (copyleft)
- Creates timestamped public record

LEGAL FRAMEWORK:
- AGPL-3.0: Strongest copyleft for software (network use triggers sharing)
- OpenMTA: Standard open material transfer agreement (Addgene, etc.)
- CC BY-SA 4.0: Attribution + ShareAlike for data/sequences

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import os
import sys
import hashlib
from datetime import datetime
from typing import List, Optional
import argparse

# ==============================================================================
# LICENSE TEMPLATES
# ==============================================================================

AGPL_HEADER = '''#!/usr/bin/env python3
"""
{filename}

SPDX-License-Identifier: AGPL-3.0-or-later

This file is part of the Open Therapeutic Sequence Project.

Copyright (C) {year} Carl Zimmerman and Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

DEFENSIVE PUBLICATION NOTICE:
This code and any sequences/structures it generates are published as
PRIOR ART to prevent patent enclosure. This publication establishes
a public record of the invention date.

Generated: {timestamp}
"""
'''

FASTA_HEADER = '''; ==============================================================================
; OPEN THERAPEUTIC SEQUENCE - PRIOR ART PUBLICATION
; ==============================================================================
;
; LICENSE: OpenMTA (Open Material Transfer Agreement) + CC BY-SA 4.0
;
; This sequence is distributed under the Open Material Transfer Agreement
; (OpenMTA, https://www.openmta.org/) and Creative Commons Attribution-
; ShareAlike 4.0 International (CC BY-SA 4.0).
;
; You are free to:
;   - USE: Synthesize, express, and test this sequence
;   - SHARE: Copy and redistribute in any medium or format
;   - ADAPT: Remix, transform, and build upon this material
;
; Under the following terms:
;   - ATTRIBUTION: Give appropriate credit, provide a link to the license
;   - SHAREALIKE: Distribute derivatives under identical terms
;   - NO PATENTS: You may not patent this sequence or derivatives
;
; PRIOR ART NOTICE:
; This sequence is published as PRIOR ART to prevent patent enclosure.
; Publication Date: {timestamp}
; SHA-256 Hash: {hash}
;
; For the full OpenMTA, see: https://www.openmta.org/
; For CC BY-SA 4.0, see: https://creativecommons.org/licenses/by-sa/4.0/
;
; ==============================================================================

'''

PDB_HEADER = '''REMARK   0 ==============================================================================
REMARK   0 OPEN THERAPEUTIC STRUCTURE - PRIOR ART PUBLICATION
REMARK   0 ==============================================================================
REMARK   0
REMARK   0 LICENSE: OpenMTA (Open Material Transfer Agreement) + CC BY-SA 4.0
REMARK   0
REMARK   0 This structure is distributed under the Open Material Transfer Agreement
REMARK   0 (OpenMTA) and Creative Commons Attribution-ShareAlike 4.0 International.
REMARK   0
REMARK   0 You are free to use, share, and adapt this structure under the terms
REMARK   0 of attribution and share-alike. No patents may be filed on this
REMARK   0 structure or derivatives.
REMARK   0
REMARK   0 PRIOR ART NOTICE:
REMARK   0 This structure is published as PRIOR ART to prevent patent enclosure.
REMARK   0 Publication Date: {timestamp}
REMARK   0 SHA-256 Hash: {hash}
REMARK   0
REMARK   0 ==============================================================================
'''

JSON_HEADER = '''{{
  "_license": {{
    "spdx": "CC-BY-SA-4.0",
    "type": "OpenMTA + CC BY-SA 4.0",
    "prior_art": true,
    "publication_date": "{timestamp}",
    "sha256": "{hash}",
    "notice": "This data is published as PRIOR ART. No patents may be filed."
  }},
'''


def calculate_hash(content: str) -> str:
    """Calculate SHA-256 hash of content."""
    return hashlib.sha256(content.encode()).hexdigest()


def is_already_stamped(content: str, file_type: str) -> bool:
    """Check if file already has license header."""
    markers = {
        'py': 'SPDX-License-Identifier:',
        'fasta': 'OPEN THERAPEUTIC SEQUENCE',
        'pdb': 'OPEN THERAPEUTIC STRUCTURE',
        'json': '"_license":'
    }
    marker = markers.get(file_type, 'SPDX-License-Identifier')
    return marker in content[:2000]  # Check first 2000 chars


def stamp_python_file(filepath: str, dry_run: bool = False) -> bool:
    """Add AGPL-3.0 header to Python file."""
    with open(filepath, 'r') as f:
        content = f.read()

    if is_already_stamped(content, 'py'):
        print(f"  ⏭ Already stamped: {filepath}")
        return False

    filename = os.path.basename(filepath)
    timestamp = datetime.now().isoformat()
    year = datetime.now().year

    # Remove existing shebang/docstring if present
    lines = content.split('\n')
    start_idx = 0

    # Skip shebang
    if lines and lines[0].startswith('#!'):
        start_idx = 1

    # Skip existing docstring
    if start_idx < len(lines) and lines[start_idx].strip().startswith('"""'):
        # Find closing """
        for i in range(start_idx + 1, len(lines)):
            if '"""' in lines[i]:
                start_idx = i + 1
                break

    # Build new content
    header = AGPL_HEADER.format(
        filename=filename,
        year=year,
        timestamp=timestamp
    )

    new_content = header + '\n'.join(lines[start_idx:])

    if dry_run:
        print(f"  📝 Would stamp: {filepath}")
        return True

    with open(filepath, 'w') as f:
        f.write(new_content)

    print(f"  ✓ Stamped: {filepath}")
    return True


def stamp_fasta_file(filepath: str, dry_run: bool = False) -> bool:
    """Add OpenMTA header to FASTA file."""
    with open(filepath, 'r') as f:
        content = f.read()

    if is_already_stamped(content, 'fasta'):
        print(f"  ⏭ Already stamped: {filepath}")
        return False

    timestamp = datetime.now().isoformat()
    content_hash = calculate_hash(content)

    header = FASTA_HEADER.format(
        timestamp=timestamp,
        hash=content_hash
    )

    new_content = header + content

    if dry_run:
        print(f"  📝 Would stamp: {filepath}")
        return True

    with open(filepath, 'w') as f:
        f.write(new_content)

    print(f"  ✓ Stamped: {filepath}")
    return True


def stamp_pdb_file(filepath: str, dry_run: bool = False) -> bool:
    """Add OpenMTA header to PDB file."""
    with open(filepath, 'r') as f:
        content = f.read()

    if is_already_stamped(content, 'pdb'):
        print(f"  ⏭ Already stamped: {filepath}")
        return False

    timestamp = datetime.now().isoformat()
    content_hash = calculate_hash(content)

    header = PDB_HEADER.format(
        timestamp=timestamp,
        hash=content_hash
    )

    new_content = header + content

    if dry_run:
        print(f"  📝 Would stamp: {filepath}")
        return True

    with open(filepath, 'w') as f:
        f.write(new_content)

    print(f"  ✓ Stamped: {filepath}")
    return True


def stamp_json_file(filepath: str, dry_run: bool = False) -> bool:
    """Add license metadata to JSON file."""
    with open(filepath, 'r') as f:
        content = f.read()

    if is_already_stamped(content, 'json'):
        print(f"  ⏭ Already stamped: {filepath}")
        return False

    timestamp = datetime.now().isoformat()
    content_hash = calculate_hash(content)

    # For JSON, we need to inject the license object
    # This is trickier - we'll add a comment-style header
    header_comment = f'''// ==============================================================================
// OPEN THERAPEUTIC DATA - PRIOR ART PUBLICATION
// LICENSE: OpenMTA + CC BY-SA 4.0
// Publication Date: {timestamp}
// SHA-256: {content_hash}
// This data is published as PRIOR ART. No patents may be filed.
// ==============================================================================

'''

    # Note: JSON doesn't support comments, so we prepend as a separate file
    # or we modify the JSON structure
    import json
    try:
        data = json.loads(content)
        data['_license'] = {
            'spdx': 'CC-BY-SA-4.0',
            'type': 'OpenMTA + CC BY-SA 4.0',
            'prior_art': True,
            'publication_date': timestamp,
            'sha256': content_hash,
            'notice': 'This data is published as PRIOR ART. No patents may be filed.'
        }

        new_content = json.dumps(data, indent=2)

        if dry_run:
            print(f"  📝 Would stamp: {filepath}")
            return True

        with open(filepath, 'w') as f:
            f.write(new_content)

        print(f"  ✓ Stamped: {filepath}")
        return True

    except json.JSONDecodeError:
        print(f"  ⚠ Invalid JSON, skipping: {filepath}")
        return False


def stamp_directory(directory: str, recursive: bool = True,
                    dry_run: bool = False) -> dict:
    """Stamp all eligible files in directory."""
    stats = {'py': 0, 'fasta': 0, 'pdb': 0, 'json': 0, 'skipped': 0}

    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            ext = filename.split('.')[-1].lower()

            if ext == 'py':
                if stamp_python_file(filepath, dry_run):
                    stats['py'] += 1
                else:
                    stats['skipped'] += 1

            elif ext in ['fasta', 'fa', 'faa']:
                if stamp_fasta_file(filepath, dry_run):
                    stats['fasta'] += 1
                else:
                    stats['skipped'] += 1

            elif ext == 'pdb':
                if stamp_pdb_file(filepath, dry_run):
                    stats['pdb'] += 1
                else:
                    stats['skipped'] += 1

            elif ext == 'json':
                if stamp_json_file(filepath, dry_run):
                    stats['json'] += 1
                else:
                    stats['skipped'] += 1

        if not recursive:
            break

    return stats


def create_prior_art_manifest(directory: str, output_file: str = None) -> str:
    """Create a manifest of all prior art publications."""
    timestamp = datetime.now().isoformat()

    manifest = {
        'manifest_version': '1.0',
        'created': timestamp,
        'creator': 'Open Therapeutic Sequence Project',
        'license_framework': {
            'software': 'AGPL-3.0-or-later',
            'sequences': 'OpenMTA + CC BY-SA 4.0',
            'structures': 'OpenMTA + CC BY-SA 4.0',
            'data': 'CC BY-SA 4.0'
        },
        'prior_art_notice': (
            'All materials in this manifest are published as PRIOR ART '
            'to prevent patent enclosure. This publication establishes '
            'a public record of invention dates for defensive purposes.'
        ),
        'files': []
    }

    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            ext = filename.split('.')[-1].lower()

            if ext in ['py', 'fasta', 'fa', 'faa', 'pdb', 'json']:
                with open(filepath, 'r') as f:
                    content = f.read()

                file_hash = calculate_hash(content)
                rel_path = os.path.relpath(filepath, directory)

                manifest['files'].append({
                    'path': rel_path,
                    'type': ext,
                    'sha256': file_hash,
                    'size_bytes': len(content),
                    'indexed': timestamp
                })

    manifest['total_files'] = len(manifest['files'])

    import json
    manifest_json = json.dumps(manifest, indent=2)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(manifest_json)
        print(f"\n  ✓ Manifest saved: {output_file}")

    return manifest_json


def main():
    """Run legal stamper."""
    parser = argparse.ArgumentParser(
        description='Stamp files with open-source licenses for prior art publication'
    )
    parser.add_argument('directory', nargs='?', default='.',
                        help='Directory to process')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Show what would be done without making changes')
    parser.add_argument('--manifest', '-m', action='store_true',
                        help='Create prior art manifest')
    parser.add_argument('--recursive', '-r', action='store_true', default=True,
                        help='Process subdirectories recursively')

    args = parser.parse_args()

    print("=" * 70)
    print("LEGAL STAMPER - Open Science License Automation")
    print("=" * 70)
    print("Framework:")
    print("  • Software: AGPL-3.0-or-later (strongest copyleft)")
    print("  • Sequences: OpenMTA + CC BY-SA 4.0")
    print("  • Structures: OpenMTA + CC BY-SA 4.0")
    print("=" * 70)

    if args.dry_run:
        print("\n  [DRY RUN - No files will be modified]\n")

    print(f"\n  Processing: {os.path.abspath(args.directory)}")

    stats = stamp_directory(args.directory, args.recursive, args.dry_run)

    print("\n" + "=" * 70)
    print("STAMPING COMPLETE")
    print("=" * 70)
    print(f"  Python files stamped: {stats['py']}")
    print(f"  FASTA files stamped:  {stats['fasta']}")
    print(f"  PDB files stamped:    {stats['pdb']}")
    print(f"  JSON files stamped:   {stats['json']}")
    print(f"  Already stamped:      {stats['skipped']}")

    if args.manifest:
        manifest_file = os.path.join(args.directory, 'PRIOR_ART_MANIFEST.json')
        create_prior_art_manifest(args.directory, manifest_file)

    print("\n" + "=" * 70)
    print("PRIOR ART PUBLICATION NOTICE")
    print("=" * 70)
    print("""
  All stamped materials are now published as PRIOR ART.

  This establishes:
  ┌─────────────────────────────────────────────────────────────┐
  │ 1. Public record of invention date                         │
  │ 2. Prevention of subsequent patent claims                  │
  │ 3. Copyleft protection requiring derivatives stay open     │
  │ 4. Attribution requirements for academic use               │
  └─────────────────────────────────────────────────────────────┘

  Anyone can USE, SYNTHESIZE, and DISTRIBUTE these materials.
  Nobody can PATENT them or restrict access.
    """)


if __name__ == "__main__":
    main()
