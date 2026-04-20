#!/usr/bin/env python3
"""
M4 Overnight Intensive Pipeline Controller
===========================================

Master controller for computationally intensive overnight analysis:
1. Structure prediction (ESMFold or fallback)
2. Molecular dynamics simulations
3. Binding affinity predictions
4. Cross-analysis and ranking

This script is designed to run overnight on an M4 Mac, utilizing
all available compute resources for comprehensive analysis.

Estimated runtime: 4-8 hours depending on sequence count

LICENSE: AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication
All generated data is PUBLIC DOMAIN for patent purposes.
"""

import os
import sys
import json
import time
import hashlib
import subprocess
import multiprocessing as mp
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import traceback
import signal

# Configuration
CONFIG = {
    'max_workers': max(1, mp.cpu_count() - 1),  # Leave 1 core free
    'structure_prediction_timeout': 3600,  # 1 hour per structure max
    'md_steps': 10000,  # Steps per sequence
    'checkpoint_interval': 300,  # Save checkpoint every 5 min
    'gpu_memory_fraction': 0.8,  # Use 80% of available GPU
}


class ProgressTracker:
    """Track and save progress for resume capability."""

    def __init__(self, checkpoint_file: str = "overnight_checkpoint.json"):
        self.checkpoint_file = Path(checkpoint_file)
        self.progress = {
            'started': None,
            'phase': 'init',
            'completed_structures': [],
            'completed_md': [],
            'completed_affinity': [],
            'failed': [],
            'current_sequence': None,
        }
        self._load_checkpoint()

    def _load_checkpoint(self):
        """Load previous checkpoint if exists."""
        if self.checkpoint_file.exists():
            try:
                with open(self.checkpoint_file, 'r') as f:
                    self.progress = json.load(f)
                print(f"[RESUME] Loaded checkpoint from {self.checkpoint_file}")
                print(f"  Phase: {self.progress.get('phase')}")
                print(f"  Completed structures: {len(self.progress.get('completed_structures', []))}")
            except Exception as e:
                print(f"[WARNING] Could not load checkpoint: {e}")

    def save_checkpoint(self):
        """Save current progress."""
        self.progress['last_checkpoint'] = datetime.now().isoformat()
        with open(self.checkpoint_file, 'w') as f:
            json.dump(self.progress, f, indent=2)

    def is_completed(self, sequence_name: str, phase: str) -> bool:
        """Check if sequence already completed for phase."""
        completed_key = f'completed_{phase}'
        return sequence_name in self.progress.get(completed_key, [])

    def mark_completed(self, sequence_name: str, phase: str):
        """Mark sequence as completed for phase."""
        completed_key = f'completed_{phase}'
        if completed_key not in self.progress:
            self.progress[completed_key] = []
        if sequence_name not in self.progress[completed_key]:
            self.progress[completed_key].append(sequence_name)
        self.save_checkpoint()

    def mark_failed(self, sequence_name: str, error: str):
        """Mark sequence as failed."""
        self.progress['failed'].append({
            'name': sequence_name,
            'error': error,
            'time': datetime.now().isoformat()
        })
        self.save_checkpoint()


class OvernightController:
    """
    Main controller for overnight intensive analysis.
    """

    def __init__(self, input_dir: str = "batch_results",
                 output_dir: str = "overnight_results"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.tracker = ProgressTracker(
            str(self.output_dir / "checkpoint.json")
        )

        self.sequences = {}
        self.results = {
            'structures': {},
            'md': {},
            'affinity': {},
        }

        self.start_time = None
        self.log_file = self.output_dir / f"overnight_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    def log(self, message: str, level: str = "INFO"):
        """Log message to file and console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level}] {message}"
        print(log_line)

        with open(self.log_file, 'a') as f:
            f.write(log_line + "\n")

    def load_sequences(self) -> int:
        """Load all sequences from multiple directories."""
        self.log("Loading sequences from all result directories...")

        # Search multiple directories where FASTA files may be located
        search_dirs = [
            Path("batch_results"),
            Path("expired_patent_antibodies"),
            Path("lysosomal_enzyme_bbb"),
            Path("therapeutic_sequences"),
            Path("genetic_capsids"),
            Path("hematological_vectors"),
            Path("ophthalmic_biologics"),
            Path("open_therapeutics"),
            Path("bbb_fusion"),
            Path("."),
        ]

        fasta_files = []
        for search_dir in search_dirs:
            if search_dir.exists():
                found = list(search_dir.glob("**/*.fasta"))
                fasta_files.extend(found)
                if found:
                    self.log(f"  Found {len(found)} files in {search_dir}")

        # Deduplicate by path
        fasta_files = list(set(fasta_files))
        self.log(f"Total: {len(fasta_files)} FASTA files")

        for fasta_file in fasta_files:
            sequences = self._load_fasta(fasta_file)
            for name, seq in sequences.items():
                # Deduplicate by sequence hash
                seq_hash = hashlib.md5(seq.encode()).hexdigest()[:8]
                unique_name = f"{name}_{seq_hash}"
                self.sequences[unique_name] = {
                    'name': name,
                    'sequence': seq,
                    'source': str(fasta_file),
                    'length': len(seq)
                }

        self.log(f"Loaded {len(self.sequences)} unique sequences")
        return len(self.sequences)

    def _load_fasta(self, fasta_file: Path) -> Dict[str, str]:
        """Load sequences from a FASTA file."""
        sequences = {}
        current_name = None
        current_seq = []

        with open(fasta_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    if current_name:
                        sequences[current_name] = ''.join(current_seq)
                    current_name = line[1:].split()[0]
                    current_seq = []
                elif line and not line.startswith(';'):
                    current_seq.append(line)

        if current_name:
            sequences[current_name] = ''.join(current_seq)

        return sequences

    def run_structure_prediction(self):
        """Run structure prediction on all sequences."""
        self.log("=" * 60)
        self.log("PHASE 1: STRUCTURE PREDICTION")
        self.log("=" * 60)
        self.tracker.progress['phase'] = 'structures'

        # Import structure prediction module
        try:
            from m4_structure_prediction import StructurePipeline
            pipeline = StructurePipeline(str(self.output_dir / "structures"))
        except ImportError:
            self.log("Structure prediction module not found, using subprocess", "WARNING")
            pipeline = None

        completed = 0
        total = len(self.sequences)

        for seq_id, seq_data in self.sequences.items():
            if self.tracker.is_completed(seq_id, 'structures'):
                self.log(f"  [SKIP] {seq_data['name']} (already completed)")
                completed += 1
                continue

            self.log(f"  [{completed+1}/{total}] Predicting structure: {seq_data['name']}")
            self.tracker.progress['current_sequence'] = seq_id

            try:
                if pipeline:
                    result = pipeline.predict_structure(
                        seq_data['name'],
                        seq_data['sequence']
                    )
                    self.results['structures'][seq_id] = result
                else:
                    # Fallback to subprocess
                    result = self._run_structure_subprocess(seq_data)
                    self.results['structures'][seq_id] = result

                self.tracker.mark_completed(seq_id, 'structures')
                completed += 1

            except Exception as e:
                self.log(f"    ERROR: {e}", "ERROR")
                self.tracker.mark_failed(seq_id, str(e))

            # Progress update
            if completed % 10 == 0:
                elapsed = datetime.now() - self.start_time
                rate = completed / (elapsed.total_seconds() / 60) if elapsed.total_seconds() > 0 else 0
                remaining = (total - completed) / rate if rate > 0 else 0
                self.log(f"  Progress: {completed}/{total} "
                        f"({rate:.1f}/min, ~{remaining:.0f} min remaining)")

        self.log(f"Structure prediction complete: {completed}/{total}")

    def _run_structure_subprocess(self, seq_data: Dict) -> Dict:
        """Run structure prediction via subprocess."""
        # Create temp input file
        temp_fasta = self.output_dir / "temp_input.fasta"
        with open(temp_fasta, 'w') as f:
            f.write(f">{seq_data['name']}\n{seq_data['sequence']}\n")

        # Run prediction script
        cmd = [sys.executable, "m4_structure_prediction.py", str(temp_fasta)]
        result = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=CONFIG['structure_prediction_timeout'])

        # Cleanup
        temp_fasta.unlink(missing_ok=True)

        return {
            'status': 'completed' if result.returncode == 0 else 'failed',
            'output': result.stdout[:1000],
            'error': result.stderr[:500] if result.stderr else None
        }

    def run_molecular_dynamics(self):
        """Run MD simulations on all sequences using GPU acceleration."""
        self.log("=" * 60)
        self.log("PHASE 2: MOLECULAR DYNAMICS (GPU-ACCELERATED)")
        self.log("=" * 60)
        self.tracker.progress['phase'] = 'md'

        # Try GPU-accelerated MD first, fall back to CPU
        try:
            from m4_gpu_molecular_dynamics import GPUMolecularDynamics, DEVICE, MPS_AVAILABLE
            self.log(f"  Using GPU MD on device: {DEVICE}")
            if MPS_AVAILABLE:
                self.log(f"  Apple Silicon MPS: ENABLED")
            use_gpu_md = True
        except ImportError:
            self.log("GPU MD not available, falling back to CPU", "WARNING")
            try:
                from m4_molecular_dynamics import MDPipeline
                pipeline = MDPipeline(str(self.output_dir / "md"))
                use_gpu_md = False
            except ImportError:
                self.log("MD module not found, skipping", "WARNING")
                return

        completed = 0
        total = len(self.sequences)
        start_phase = datetime.now()

        for seq_id, seq_data in self.sequences.items():
            if self.tracker.is_completed(seq_id, 'md'):
                self.log(f"  [SKIP] {seq_data['name']} (already completed)")
                completed += 1
                continue

            self.log(f"  [{completed+1}/{total}] Running MD: {seq_data['name']} ({len(seq_data['sequence'])} aa)")

            try:
                if use_gpu_md:
                    # GPU-accelerated MD
                    md = GPUMolecularDynamics(seq_data['sequence'])
                    md_result = md.run_dynamics(n_steps=CONFIG['md_steps'], report_interval=100)

                    # Compute metrics
                    rmsf = md.compute_rmsf(md_result['trajectory'])
                    rmsd = md.compute_rmsd(md_result['trajectory'])

                    result = {
                        'name': seq_data['name'],
                        'sequence_length': len(seq_data['sequence']),
                        'n_steps': md_result['n_steps'],
                        'device': md_result['device'],
                        'elapsed_seconds': md_result['elapsed_seconds'],
                        'steps_per_second': md_result['steps_per_second'],
                        'mean_rmsf': float(rmsf.mean()),
                        'max_rmsf': float(rmsf.max()),
                        'final_rmsd': float(rmsd[-1]) if len(rmsd) > 0 else 0,
                        'stability_score': max(0, 100 - float(rmsf.mean()) * 5),
                    }
                    self.log(f"    Done in {md_result['elapsed_seconds']:.1f}s | "
                            f"RMSF={result['mean_rmsf']:.2f}Å | "
                            f"Speed={md_result['steps_per_second']:.0f} steps/s")
                else:
                    # CPU fallback
                    result = pipeline.analyze_sequence(
                        seq_data['name'],
                        seq_data['sequence'],
                        n_steps=CONFIG['md_steps']
                    )

                self.results['md'][seq_id] = result
                self.tracker.mark_completed(seq_id, 'md')
                completed += 1

            except Exception as e:
                self.log(f"    ERROR: {e}", "ERROR")
                self.tracker.mark_failed(seq_id, f"MD: {str(e)}")

            # Progress update every 10
            if completed % 10 == 0 and completed > 0:
                elapsed = (datetime.now() - start_phase).total_seconds()
                rate = completed / elapsed * 60  # per minute
                remaining = (total - completed) / rate if rate > 0 else 0
                self.log(f"  Progress: {completed}/{total} ({rate:.1f}/min, ~{remaining:.0f} min remaining)")

        self.log(f"MD simulations complete: {completed}/{total}")

    def run_binding_affinity(self):
        """Run binding affinity predictions."""
        self.log("=" * 60)
        self.log("PHASE 3: BINDING AFFINITY")
        self.log("=" * 60)
        self.tracker.progress['phase'] = 'affinity'

        try:
            from m4_binding_affinity import BindingAffinityPipeline
            pipeline = BindingAffinityPipeline(str(self.output_dir / "affinity"))
        except ImportError:
            self.log("Binding affinity module not found, skipping", "WARNING")
            return

        completed = 0
        total = len(self.sequences)

        for seq_id, seq_data in self.sequences.items():
            if self.tracker.is_completed(seq_id, 'affinity'):
                self.log(f"  [SKIP] {seq_data['name']} (already completed)")
                completed += 1
                continue

            self.log(f"  [{completed+1}/{total}] Analyzing affinity: {seq_data['name']}")

            try:
                result = pipeline.analyze_antibody(
                    seq_data['name'],
                    seq_data['sequence']
                )
                self.results['affinity'][seq_id] = result
                self.tracker.mark_completed(seq_id, 'affinity')
                completed += 1

            except Exception as e:
                self.log(f"    ERROR: {e}", "ERROR")
                self.tracker.mark_failed(seq_id, f"Affinity: {str(e)}")

        self.log(f"Affinity analysis complete: {completed}/{total}")

    def generate_integrated_report(self):
        """Generate integrated analysis report."""
        self.log("=" * 60)
        self.log("GENERATING INTEGRATED REPORT")
        self.log("=" * 60)

        report = []
        report.append("=" * 70)
        report.append("M4 OVERNIGHT INTENSIVE ANALYSIS - INTEGRATED REPORT")
        report.append("=" * 70)
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append(f"Total runtime: {datetime.now() - self.start_time}")
        report.append(f"Sequences analyzed: {len(self.sequences)}")
        report.append("")

        # Summary statistics
        n_structures = len(self.tracker.progress.get('completed_structures', []))
        n_md = len(self.tracker.progress.get('completed_md', []))
        n_affinity = len(self.tracker.progress.get('completed_affinity', []))
        n_failed = len(self.tracker.progress.get('failed', []))

        report.append("COMPLETION SUMMARY:")
        report.append(f"  Structure predictions: {n_structures}/{len(self.sequences)}")
        report.append(f"  MD simulations: {n_md}/{len(self.sequences)}")
        report.append(f"  Affinity analyses: {n_affinity}/{len(self.sequences)}")
        report.append(f"  Failed: {n_failed}")
        report.append("")

        # Top candidates (combining all metrics)
        report.append("TOP THERAPEUTIC CANDIDATES:")
        report.append("-" * 70)

        # Score each sequence
        scores = []
        for seq_id, seq_data in self.sequences.items():
            score = 0
            details = []

            # Structure confidence
            if seq_id in self.results.get('structures', {}):
                struct = self.results['structures'][seq_id]
                if 'plddt_mean' in struct:
                    plddt = struct['plddt_mean']
                    score += plddt / 100 * 30  # Max 30 points
                    details.append(f"pLDDT={plddt:.1f}")

            # MD stability
            if seq_id in self.results.get('md', {}):
                md = self.results['md'][seq_id]
                if 'stability_score' in md:
                    stability = md['stability_score']
                    score += stability / 100 * 30  # Max 30 points
                    details.append(f"Stability={stability:.1f}")

            # Binding affinity
            if seq_id in self.results.get('affinity', {}):
                aff = self.results['affinity'][seq_id]
                if 'analysis' in aff and 'affinity_potential' in aff['analysis']:
                    aff_score = aff['analysis']['affinity_potential'].get('score', 0)
                    score += aff_score / 100 * 40  # Max 40 points
                    details.append(f"Affinity={aff_score:.1f}")

            if score > 0:
                scores.append({
                    'seq_id': seq_id,
                    'name': seq_data['name'],
                    'score': score,
                    'details': details
                })

        # Sort and report top 20
        scores.sort(key=lambda x: x['score'], reverse=True)

        for i, entry in enumerate(scores[:20], 1):
            report.append(f"  {i:2d}. {entry['name'][:45]:<45}")
            report.append(f"      Score: {entry['score']:.1f}/100 | {', '.join(entry['details'])}")

        # Failed sequences
        if self.tracker.progress.get('failed'):
            report.append("\n\nFAILED SEQUENCES:")
            report.append("-" * 70)
            for fail in self.tracker.progress['failed'][:10]:
                report.append(f"  {fail['name']}: {fail['error'][:50]}")

        report.append("")
        report.append("=" * 70)
        report.append("LICENSE: AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication")
        report.append("All data is PUBLIC DOMAIN for patent purposes.")
        report.append("=" * 70)

        report_text = "\n".join(report)

        # Save report
        report_file = self.output_dir / "OVERNIGHT_ANALYSIS_REPORT.txt"
        with open(report_file, 'w') as f:
            f.write(report_text)

        # Save full results JSON
        results_file = self.output_dir / "overnight_full_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                'metadata': {
                    'start_time': self.start_time.isoformat() if self.start_time else None,
                    'end_time': datetime.now().isoformat(),
                    'n_sequences': len(self.sequences),
                    'config': CONFIG,
                },
                'results': {
                    'structures': {k: str(v) for k, v in self.results['structures'].items()},
                    'md': {k: str(v)[:500] for k, v in self.results['md'].items()},
                    'affinity': {k: str(v)[:500] for k, v in self.results['affinity'].items()},
                },
                'rankings': scores[:50],
            }, f, indent=2, default=str)

        self.log(f"Report saved: {report_file}")
        self.log(f"Full results: {results_file}")

        print("\n" + report_text)

    def run(self):
        """Run complete overnight analysis."""
        self.start_time = datetime.now()
        self.tracker.progress['started'] = self.start_time.isoformat()

        self.log("=" * 70)
        self.log("M4 OVERNIGHT INTENSIVE ANALYSIS")
        self.log("Starting comprehensive analysis pipeline")
        self.log("=" * 70)
        self.log(f"Start time: {self.start_time}")
        self.log(f"CPU cores available: {CONFIG['max_workers']}")
        self.log(f"Output directory: {self.output_dir}")
        self.log("")

        # Load sequences
        n_sequences = self.load_sequences()
        if n_sequences == 0:
            self.log("No sequences found! Please run batch processor first.", "ERROR")
            return

        # Estimate runtime
        estimated_hours = n_sequences * 0.5 / 60  # ~30 sec per sequence per phase
        self.log(f"Estimated runtime: {estimated_hours:.1f} hours for {n_sequences} sequences")
        self.log("")

        try:
            # Phase 1: Structure prediction
            self.run_structure_prediction()

            # Phase 2: Molecular dynamics
            self.run_molecular_dynamics()

            # Phase 3: Binding affinity
            self.run_binding_affinity()

            # Generate integrated report
            self.generate_integrated_report()

        except KeyboardInterrupt:
            self.log("\n[INTERRUPTED] Saving checkpoint...", "WARNING")
            self.tracker.save_checkpoint()
            self.log("Checkpoint saved. Resume by running script again.")
            raise

        except Exception as e:
            self.log(f"\n[CRITICAL ERROR] {e}", "ERROR")
            self.log(traceback.format_exc(), "ERROR")
            self.tracker.save_checkpoint()
            raise

        finally:
            end_time = datetime.now()
            runtime = end_time - self.start_time
            self.log("")
            self.log("=" * 70)
            self.log("OVERNIGHT ANALYSIS COMPLETE")
            self.log(f"Total runtime: {runtime}")
            self.log("=" * 70)


def signal_handler(signum, frame):
    """Handle interrupt signals gracefully."""
    print("\n[SIGNAL] Received interrupt, saving checkpoint...")
    raise KeyboardInterrupt


def main():
    """Main entry point."""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("=" * 70)
    print("M4 OVERNIGHT INTENSIVE PIPELINE")
    print("Comprehensive Therapeutic Analysis")
    print("=" * 70)
    print()
    print("This script will run computationally intensive analysis:")
    print("  1. Structure prediction (ESMFold)")
    print("  2. Molecular dynamics simulations")
    print("  3. Binding affinity predictions")
    print()
    print(f"Configuration:")
    print(f"  CPU cores: {CONFIG['max_workers']}")
    print(f"  MD steps: {CONFIG['md_steps']}")
    print()
    print("Press Ctrl+C at any time to save progress and exit.")
    print("Run the script again to resume from checkpoint.")
    print()

    # Check for existing batch results
    batch_dir = Path("batch_results")
    if not batch_dir.exists():
        print("[WARNING] No batch_results directory found!")
        print("Please run m4_autonomous_batch_processor.py first.")
        print()

        # Offer to create demo data
        print("Creating demo sequences for testing...")

        batch_dir.mkdir(exist_ok=True)
        demo_fasta = batch_dir / "demo_sequences.fasta"
        with open(demo_fasta, 'w') as f:
            f.write(">Demo_Anti_VEGF_scFv\n")
            f.write("EVQLVESGGGLVQPGGSLRLSCAASGFTFSSYWMSWVRQAPGKGLEWVANIKQDGSEKY\n")
            f.write("YVDSVKGRFTISRDNAKNSLYLQMNSLRAEDTAVYYCARWGYRFFDYWGQGTLVTVSS\n")
            f.write("GGGGSGGGGSGGGGSGGGGS\n")
            f.write("DIQMTQSPSSLSASVGDRVTITCRASQDVNTAVAWYQQKPGKAPKLLIYSASFLYSGVP\n")
            f.write("SRFSGSRSGTDFTLTISSLQPEDFATYYCQQHYTTPPTFGQGTKVEIK\n")
            f.write("\n>Demo_Angiopep2_Fusion\n")
            f.write("TFFYGGSRGKRNNFKTEEYGGGGSGGGGSEVQLVESGGGLVQPGGSLRLSCAASGFTFS\n")
            f.write("SYAMSWVRQAPGKGLEWVAVISYDGSNKYYADSVKGRFTISRDNAKNSLYLQMNSLRAE\n")
            f.write("DTAVYYCARGYYYYYYYYGMDVWGQGTLVTVSS\n")

        print(f"Created demo sequences at {demo_fasta}")

    # Run controller
    controller = OvernightController()
    controller.run()


if __name__ == "__main__":
    main()
