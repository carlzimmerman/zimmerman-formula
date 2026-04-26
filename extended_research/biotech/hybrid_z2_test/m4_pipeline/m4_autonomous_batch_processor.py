#!/usr/bin/env python3
"""
================================================================================
M4 AUTONOMOUS BATCH PROCESSOR
================================================================================

Master controller script for high-throughput autonomous therapeutic sequence
generation. Runs all M4 pipeline scripts systematically and handles errors
gracefully.

This script can run unattended to process:
- Ophthalmic biologics (anti-VEGF, AAV for retinal target system)
- Neuromuscular gene therapy vectors (SMA, DMD)
- Hematological vectors (sickle cell, thalassemia)
- Lysosomal enzyme BBB fusions
- Expired patent antibody engineering
- Therapeutic antibody extraction

================================================================================
DEFENSIVE PUBLICATION & PATENT PREVENTION NOTICE
================================================================================

This work is published under AGPL-3.0 + OpenMTA + CC BY-SA 4.0 with
PATENT DEDICATION to the public domain.

All sequences, methods, and results are PUBLIC DOMAIN for patent purposes.
This publication establishes PRIOR ART via cryptographic hashing and timestamping.

License: AGPL-3.0 (code) + OpenMTA + CC BY-SA 4.0 (sequences) + Patent Dedication
================================================================================
"""

import os
import sys
import json
import hashlib
import subprocess
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

PIPELINE_SCRIPTS = [
    {
        "name": "Ophthalmic Biologics",
        "script": "m4_ophthalmic_biologics_upgrader.py",
        "description": "Anti-VEGF antibodies and AAV capsids for eye diseases",
        "output_dir": "ophthalmic_biologics",
        "diseases": ["Wet AMD", "Diabetic macular edema", "Inherited retinal disorders"]
    },
    {
        "name": "Genetic Capsid Engineering",
        "script": "m4_genetic_capsid_engineering.py",
        "description": "AAV capsids for neuromuscular gene therapy",
        "output_dir": "genetic_capsids",
        "diseases": ["SMA", "DMD", "Limb-girdle MD"]
    },
    {
        "name": "Hematological Vectors",
        "script": "m4_hematological_vector_optimization.py",
        "description": "Lentiviral and CRISPR delivery for blood disorders",
        "output_dir": "hematological_vectors",
        "diseases": ["Sickle Cell target system", "Beta-Thalassemia"]
    },
    {
        "name": "Lysosomal Enzyme BBB",
        "script": "m4_lysosomal_enzyme_bbb.py",
        "description": "Brain-penetrating enzyme fusions for storage disorders",
        "output_dir": "lysosomal_enzyme_bbb",
        "diseases": ["MPS I/II/III", "Tay-Sachs", "Krabbe", "Gaucher", "Fabry", "Pompe"]
    },
    {
        "name": "Expired Patent Antibodies",
        "script": "m4_expired_patent_antibodies.py",
        "description": "Engineering blockbuster antibodies from expired patents",
        "output_dir": "expired_patent_antibodies",
        "diseases": ["Cancer", "Autoimmune", "Inflammatory"]
    },
    {
        "name": "Therapeutic Sequence Extraction",
        "script": "m4_therapeutic_sequence_extraction.py",
        "description": "High-throughput antibody engineering",
        "output_dir": "therapeutic_sequences",
        "diseases": ["Alzheimer's", "Parkinson's", "ALS", "MS", "Migraine"]
    }
]

# =============================================================================
# BATCH PROCESSOR CLASS
# =============================================================================

class AutonomousBatchProcessor:
    """Autonomous batch processor for M4 therapeutic pipeline."""

    def __init__(self, output_base: str = "batch_results"):
        self.output_base = output_base
        self.start_time = datetime.now()
        self.results = []
        self.manifest = {
            "pipeline": "M4 Autonomous Batch Processor",
            "version": "1.0",
            "license": "AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication",
            "start_time": self.start_time.isoformat(),
            "scripts": [],
            "prior_art_hashes": []
        }

        # Create output directory
        os.makedirs(output_base, exist_ok=True)

        # Setup logging
        self.log_path = os.path.join(output_base, "batch_log.txt")
        self._log(f"M4 Autonomous Batch Processor initialized at {self.start_time}")

    def _log(self, message: str, level: str = "INFO"):
        """Log message to file and console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level}] {message}"
        print(log_line)

        with open(self.log_path, 'a') as f:
            f.write(log_line + "\n")

    def run_script(self, script_info: Dict) -> Dict:
        """Run a single pipeline script and capture results."""
        script_name = script_info["script"]
        pipeline_name = script_info["name"]

        self._log(f"Starting: {pipeline_name} ({script_name})")

        result = {
            "name": pipeline_name,
            "script": script_name,
            "start_time": datetime.now().isoformat(),
            "status": "pending",
            "output_files": [],
            "error": None
        }

        try:
            # Check if script exists
            if not os.path.exists(script_name):
                raise FileNotFoundError(f"Script not found: {script_name}")

            # Run script
            process = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout per script
            )

            # Check for success
            if process.returncode == 0:
                result["status"] = "success"
                result["stdout"] = process.stdout[-5000:]  # Last 5000 chars
                self._log(f"Completed: {pipeline_name}")

                # Collect output files
                output_dir = script_info.get("output_dir")
                if output_dir and os.path.exists(output_dir):
                    result["output_files"] = self._collect_output_files(output_dir)
                    self._log(f"  Generated {len(result['output_files'])} files")

            else:
                result["status"] = "error"
                result["error"] = process.stderr[-2000:]
                self._log(f"Error in {pipeline_name}: {process.stderr[:200]}", "ERROR")

        except subprocess.TimeoutExpired:
            result["status"] = "timeout"
            result["error"] = "Script execution timed out (10 min limit)"
            self._log(f"Timeout: {pipeline_name}", "ERROR")

        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            result["traceback"] = traceback.format_exc()
            self._log(f"Exception in {pipeline_name}: {str(e)}", "ERROR")

        result["end_time"] = datetime.now().isoformat()
        return result

    def _collect_output_files(self, output_dir: str) -> List[Dict]:
        """Collect all output files and compute hashes."""
        files = []

        for root, dirs, filenames in os.walk(output_dir):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, output_dir)

                # Compute SHA-256 hash
                with open(filepath, 'rb') as f:
                    content = f.read()
                    sha256 = hashlib.sha256(content).hexdigest()

                file_info = {
                    "path": rel_path,
                    "size": len(content),
                    "sha256": sha256,
                    "timestamp": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                }
                files.append(file_info)

                # Add to prior art manifest
                self.manifest["prior_art_hashes"].append({
                    "file": os.path.join(output_dir, rel_path),
                    "sha256": sha256,
                    "timestamp": file_info["timestamp"]
                })

        return files

    def run_all(self) -> Dict:
        """Run all pipeline scripts in sequence."""
        self._log("="*60)
        self._log("STARTING AUTONOMOUS BATCH PROCESSING")
        self._log("="*60)

        total_scripts = len(PIPELINE_SCRIPTS)
        successful = 0
        failed = 0

        for i, script_info in enumerate(PIPELINE_SCRIPTS, 1):
            self._log(f"\n[{i}/{total_scripts}] Processing: {script_info['name']}")
            self._log(f"  Description: {script_info['description']}")
            self._log(f"  Diseases: {', '.join(script_info['diseases'])}")

            result = self.run_script(script_info)
            self.results.append(result)
            self.manifest["scripts"].append({
                "name": script_info["name"],
                "script": script_info["script"],
                "status": result["status"],
                "output_count": len(result.get("output_files", []))
            })

            if result["status"] == "success":
                successful += 1
            else:
                failed += 1
                # Continue to next script on error (graceful handling)
                self._log(f"  Continuing to next script despite error...")

        # Generate final report
        self.manifest["end_time"] = datetime.now().isoformat()
        self.manifest["summary"] = {
            "total_scripts": total_scripts,
            "successful": successful,
            "failed": failed,
            "total_files_generated": sum(
                len(r.get("output_files", [])) for r in self.results
            )
        }

        # Save manifest
        manifest_path = os.path.join(self.output_base, "PRIOR_ART_MANIFEST.json")
        with open(manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)

        self._log(f"\nPrior Art Manifest saved: {manifest_path}")

        return self.manifest

    def print_summary(self):
        """Print final summary."""
        duration = datetime.now() - self.start_time

        print("\n" + "="*80)
        print("M4 AUTONOMOUS BATCH PROCESSING COMPLETE")
        print("="*80)
        print(f"""
Duration: {duration}

RESULTS:
  Total scripts: {self.manifest['summary']['total_scripts']}
  Successful: {self.manifest['summary']['successful']}
  Failed: {self.manifest['summary']['failed']}
  Total files generated: {self.manifest['summary']['total_files_generated']}

SCRIPT RESULTS:
""")

        for result in self.results:
            status_icon = "[OK]" if result["status"] == "success" else "[X]" if result["status"] == "error" else "[!]"
            print(f"  {status_icon} {result['name']}: {result['status']}")
            if result["status"] == "success":
                print(f"      Files: {len(result.get('output_files', []))}")
            elif result.get("error"):
                print(f"      Error: {result['error'][:100]}...")

        print(f"""
PRIOR ART ESTABLISHMENT:
  All generated sequences have been cryptographically hashed (SHA-256).
  Manifest saved to: {self.output_base}/PRIOR_ART_MANIFEST.json

  This establishes:
  1. Timestamped proof of creation
  2. Cryptographic verification of content
  3. Prior art against future patent claims

LICENSE: AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication

DISEASES ADDRESSED:
""")

        all_diseases = set()
        for script_info in PIPELINE_SCRIPTS:
            all_diseases.update(script_info["diseases"])

        for target system in sorted(all_diseases):
            print(f"  - {target system}")

        print("\n" + "="*80)


def main():
    """Main entry point."""
    print("="*80)
    print("M4 AUTONOMOUS BATCH PROCESSOR")
    print("Open-Source Therapeutic Sequence Factory")
    print("="*80)
    print("""
This script will autonomously run all M4 pipeline scripts to generate
therapeutic sequences for multiple target system areas.

The pipeline will:
1. Run each script in sequence
2. Handle errors gracefully (continue on failure)
3. Collect all output files
4. Generate SHA-256 hashes for prior art
5. Create a comprehensive manifest

LICENSE: AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication
All generated sequences are PUBLIC DOMAIN for patent purposes.
""")

    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Initialize and run processor
    processor = AutonomousBatchProcessor()
    processor.run_all()
    processor.print_summary()


if __name__ == "__main__":
    main()
