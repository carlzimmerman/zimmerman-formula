#!/usr/bin/env python3
"""
M4 Therapeutic Batch Controller
================================

Master execution script for autonomous therapeutic pipeline processing.
Orchestrates all M4 structural biology pipelines for overnight batch runs.

Pipelines executed:
1. Senolytic peptide engineering (BCL-xL inhibitors)
2. Autophagy flux enhancement (mTORC1 modulators)
3. AAV9 immune evasion (glycan shielding)
4. Ophthalmic biologics (anti-VEGF optimization)

Features:
- Sequential execution with error handling
- SHA-256 cryptographic hashing for prior art
- Comprehensive logging and metadata
- Auto-retry on API failures
- Prior art manifest generation

License: AGPL-3.0 + OpenMTA + CC-BY-SA-4.0 (Open Science Prior Art)
"""

import os
import sys
import json
import hashlib
import traceback
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import importlib.util


class TherapeuticBatchController:
    """
    Master controller for M4 therapeutic pipeline execution.

    Manages sequential execution of all therapeutic engineering pipelines,
    generates cryptographic prior art manifests, and handles error recovery.
    """

    def __init__(self, output_dir: str = "batch_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.log_file = self.output_dir / f"batch_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.manifest_file = self.output_dir / "PRIOR_ART_MANIFEST.json"

        self.start_time = None
        self.pipelines_run = []
        self.assets_generated = []
        self.errors = []

        # Pipeline definitions
        self.pipelines = {
            'senolytic': {
                'module': 'm4_senolytic_peptide_engineer',
                'description': 'BCL-xL competitive inhibitor peptides for senescent cell clearance',
                'therapeutic_area': 'Aging / Senescence',
                'output_dir': 'senolytic_peptides',
            },
            'autophagy': {
                'module': 'm4_autophagy_flux_enhancer',
                'description': 'mTORC1 RAPTOR modulators for enhanced autophagic flux',
                'therapeutic_area': 'Proteostasis / Neurodegeneration',
                'output_dir': 'autophagy_enhancers',
            },
            'aav9': {
                'module': 'm4_aav9_immune_evasion',
                'description': 'AAV9 capsid variants with glycan shielding for reduced immunogenicity',
                'therapeutic_area': 'Gene Therapy Delivery',
                'output_dir': 'aav9_engineered',
            },
            'ophthalmic': {
                'module': 'm4_ophthalmic_biologics_upgrader',
                'description': 'Anti-VEGF scFv optimization for macular degeneration',
                'therapeutic_area': 'Ophthalmology',
                'output_dir': 'ophthalmic_biologics',
            },
        }

    def log(self, message: str, level: str = "INFO"):
        """Log message to file and stdout."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level}] {message}"
        print(log_line)

        with open(self.log_file, 'a') as f:
            f.write(log_line + '\n')

    def calculate_sha256(self, content: str) -> str:
        """Calculate SHA-256 hash for prior art verification."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def load_module(self, module_name: str):
        """Dynamically load a pipeline module."""
        module_path = Path(__file__).parent / f"{module_name}.py"

        if not module_path.exists():
            raise FileNotFoundError(f"Pipeline module not found: {module_path}")

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        return module

    def run_pipeline(self, pipeline_name: str, max_retries: int = 3) -> Dict:
        """
        Execute a single pipeline with retry logic.

        Returns pipeline result with generated assets.
        """
        pipeline_info = self.pipelines.get(pipeline_name)
        if not pipeline_info:
            raise ValueError(f"Unknown pipeline: {pipeline_name}")

        self.log(f"Starting pipeline: {pipeline_name}")
        self.log(f"  Description: {pipeline_info['description']}")
        self.log(f"  Therapeutic area: {pipeline_info['therapeutic_area']}")

        result = {
            'pipeline': pipeline_name,
            'module': pipeline_info['module'],
            'status': 'pending',
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'assets': [],
            'errors': [],
            'retries': 0,
        }

        for attempt in range(max_retries):
            try:
                self.log(f"  Attempt {attempt + 1}/{max_retries}")

                # Load and run module
                module = self.load_module(pipeline_info['module'])

                if hasattr(module, 'main'):
                    pipeline_results = module.main()
                else:
                    raise AttributeError(f"Module {pipeline_info['module']} has no main() function")

                # Process results
                if isinstance(pipeline_results, list):
                    for asset in pipeline_results:
                        asset_record = self.process_asset(asset, pipeline_name)
                        result['assets'].append(asset_record)
                        self.assets_generated.append(asset_record)

                result['status'] = 'completed'
                result['end_time'] = datetime.now().isoformat()
                result['retries'] = attempt

                self.log(f"  Pipeline completed: {len(result['assets'])} assets generated")
                break

            except Exception as e:
                error_msg = f"{type(e).__name__}: {str(e)}"
                result['errors'].append({
                    'attempt': attempt + 1,
                    'error': error_msg,
                    'traceback': traceback.format_exc(),
                })
                self.log(f"  Error (attempt {attempt + 1}): {error_msg}", "ERROR")

                if attempt < max_retries - 1:
                    wait_time = 60 * (attempt + 1)  # Exponential backoff
                    self.log(f"  Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    result['status'] = 'failed'
                    result['end_time'] = datetime.now().isoformat()
                    self.errors.append({
                        'pipeline': pipeline_name,
                        'error': error_msg,
                    })

        self.pipelines_run.append(result)
        return result

    def process_asset(self, asset: Dict, pipeline_name: str) -> Dict:
        """Process a generated asset and create prior art record."""
        sequence = asset.get('sequence', '')

        asset_record = {
            'name': asset.get('name', 'unknown'),
            'pipeline': pipeline_name,
            'sequence_length': len(sequence),
            'sha256': self.calculate_sha256(sequence),
            'therapeutic_class': asset.get('therapeutic_class', 'unknown'),
            'target': asset.get('target', 'unknown'),
            'mechanism': asset.get('mechanism', 'unknown'),
            'indication': asset.get('indication', 'unknown'),
            'fasta_path': asset.get('fasta_path', ''),
            'timestamp': datetime.now().isoformat(),
            'license': 'AGPL-3.0 + OpenMTA + CC-BY-SA-4.0',
            'prior_art': True,
        }

        return asset_record

    def generate_prior_art_manifest(self) -> Dict:
        """Generate comprehensive prior art manifest for all assets."""
        manifest = {
            'manifest_version': '1.0.0',
            'generator': 'M4_Therapeutic_Batch_Controller',
            'generation_date': datetime.now().isoformat(),
            'prior_art_declaration': {
                'statement': (
                    "All sequences, methods, and designs contained herein are "
                    "published as PRIOR ART under defensive publication principles. "
                    "This publication establishes prior art to PREVENT PATENT ENCLOSURE "
                    "of these therapeutic designs."
                ),
                'legal_effect': (
                    "Publication of this manifest establishes a dated record of "
                    "invention disclosure, precluding subsequent patent claims on "
                    "the disclosed sequences and methods."
                ),
            },
            'license': {
                'code': 'AGPL-3.0',
                'sequences': 'OpenMTA + CC-BY-SA-4.0',
                'patents': 'Dedicated to Public Domain',
            },
            'batch_run': {
                'start_time': self.start_time.isoformat() if self.start_time else None,
                'end_time': datetime.now().isoformat(),
                'pipelines_executed': len(self.pipelines_run),
                'total_assets': len(self.assets_generated),
                'errors': len(self.errors),
            },
            'pipelines': [
                {
                    'name': p['pipeline'],
                    'status': p['status'],
                    'assets_count': len(p['assets']),
                    'retries': p['retries'],
                }
                for p in self.pipelines_run
            ],
            'assets': self.assets_generated,
            'integrity': {
                'manifest_sha256': None,  # Will be filled after serialization
                'asset_count': len(self.assets_generated),
            },
        }

        # Calculate manifest hash (excluding the hash field itself)
        manifest_copy = manifest.copy()
        manifest_copy['integrity']['manifest_sha256'] = 'PENDING'
        manifest_json = json.dumps(manifest_copy, indent=2, sort_keys=True)
        manifest['integrity']['manifest_sha256'] = self.calculate_sha256(manifest_json)

        return manifest

    def save_manifest(self, manifest: Dict):
        """Save prior art manifest to file."""
        # Load existing manifest if present
        existing_assets = []
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, 'r') as f:
                    existing = json.load(f)
                    existing_assets = existing.get('assets', [])
                    self.log(f"Loaded {len(existing_assets)} existing assets from manifest")
            except (json.JSONDecodeError, KeyError):
                pass

        # Merge assets (avoid duplicates by SHA256)
        existing_hashes = {a['sha256'] for a in existing_assets}
        new_assets = [a for a in manifest['assets'] if a['sha256'] not in existing_hashes]

        manifest['assets'] = existing_assets + new_assets
        manifest['integrity']['asset_count'] = len(manifest['assets'])

        # Recalculate manifest hash
        manifest_copy = manifest.copy()
        manifest_copy['integrity']['manifest_sha256'] = 'PENDING'
        manifest_json = json.dumps(manifest_copy, indent=2, sort_keys=True)
        manifest['integrity']['manifest_sha256'] = self.calculate_sha256(manifest_json)

        # Save
        with open(self.manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)

        self.log(f"Prior art manifest saved: {self.manifest_file}")
        self.log(f"  Total assets in manifest: {len(manifest['assets'])}")
        self.log(f"  New assets added: {len(new_assets)}")

    def run_all_pipelines(self, pipelines: Optional[List[str]] = None):
        """
        Execute all therapeutic pipelines in sequence.

        Args:
            pipelines: Optional list of pipeline names to run.
                       If None, runs all pipelines.
        """
        self.start_time = datetime.now()

        self.log("=" * 70)
        self.log("M4 THERAPEUTIC BATCH CONTROLLER")
        self.log("Autonomous Multi-Pipeline Therapeutic Engineering")
        self.log("=" * 70)
        self.log("")
        self.log(f"Start time: {self.start_time.isoformat()}")
        self.log(f"Output directory: {self.output_dir}")
        self.log(f"Log file: {self.log_file}")
        self.log("")

        # Determine which pipelines to run
        pipeline_names = pipelines or list(self.pipelines.keys())

        self.log(f"Pipelines to execute: {', '.join(pipeline_names)}")
        self.log("")

        # Execute pipelines sequentially
        for i, pipeline_name in enumerate(pipeline_names, 1):
            self.log("=" * 70)
            self.log(f"PIPELINE {i}/{len(pipeline_names)}: {pipeline_name.upper()}")
            self.log("=" * 70)

            try:
                result = self.run_pipeline(pipeline_name)
                status = "SUCCESS" if result['status'] == 'completed' else "FAILED"
                self.log(f"Pipeline {pipeline_name}: {status}")
            except Exception as e:
                self.log(f"Pipeline {pipeline_name} CRITICAL ERROR: {e}", "ERROR")
                self.errors.append({
                    'pipeline': pipeline_name,
                    'error': str(e),
                    'critical': True,
                })

            self.log("")

        # Generate and save manifest
        self.log("=" * 70)
        self.log("GENERATING PRIOR ART MANIFEST")
        self.log("=" * 70)

        manifest = self.generate_prior_art_manifest()
        self.save_manifest(manifest)

        # Final summary
        end_time = datetime.now()
        duration = end_time - self.start_time

        self.log("")
        self.log("=" * 70)
        self.log("BATCH RUN COMPLETE")
        self.log("=" * 70)
        self.log(f"End time: {end_time.isoformat()}")
        self.log(f"Duration: {duration}")
        self.log("")
        self.log("SUMMARY:")
        self.log(f"  Pipelines executed: {len(self.pipelines_run)}")
        self.log(f"  Pipelines successful: {sum(1 for p in self.pipelines_run if p['status'] == 'completed')}")
        self.log(f"  Pipelines failed: {sum(1 for p in self.pipelines_run if p['status'] == 'failed')}")
        self.log(f"  Total assets generated: {len(self.assets_generated)}")
        self.log(f"  Errors encountered: {len(self.errors)}")
        self.log("")
        self.log("OUTPUT FILES:")
        self.log(f"  Log: {self.log_file}")
        self.log(f"  Prior Art Manifest: {self.manifest_file}")
        self.log("")

        if self.errors:
            self.log("ERRORS:", "WARNING")
            for err in self.errors:
                self.log(f"  - {err['pipeline']}: {err['error']}", "WARNING")

        self.log("")
        self.log("THERAPEUTIC AREAS ADDRESSED:")
        for name, info in self.pipelines.items():
            if name in pipeline_names:
                self.log(f"  - {info['therapeutic_area']}: {info['description']}")

        self.log("")
        self.log("PRIOR ART NOTICE:")
        self.log("  All generated sequences are published as prior art.")
        self.log("  License: AGPL-3.0 + OpenMTA + CC-BY-SA-4.0")
        self.log("  Patent status: Dedicated to Public Domain")
        self.log("")

        return manifest


def main():
    """Main entry point for batch controller."""
    controller = TherapeuticBatchController(output_dir="batch_results")

    # Run all pipelines
    manifest = controller.run_all_pipelines()

    return manifest


if __name__ == "__main__":
    main()
