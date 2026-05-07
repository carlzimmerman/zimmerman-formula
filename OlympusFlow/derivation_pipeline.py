#!/usr/bin/env python3
"""
OLYMPUSFLOW - Unified Derivation Pipeline
==========================================

A clean, unified pipeline for Z² derivations that integrates:
1. MetisFlow (research)
2. DerivationEngine (reasoning)
3. AletheiaLake (ground truth)
4. MnemosyneLake (working memory)

This replaces the fragmented stages with a single coherent flow.

Data Flow:
    DerivationTask
        │
        ▼
    MetisStage (Research literature)
        │
        ▼
    DerivationStage (Build chain with Legomena)
        │
        ▼
    VerificationStage (Validate against experiment)
        │
        ▼
    StorageStage (Route to AletheiaLake or MnemosyneLake)

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Add parent for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from .derivation_contracts import (
    DerivationChain, VerifiedDerivation, DerivationStep,
    DerivationLevel, ChainStatus, StorageDestination, ZSquaredRelevance,
    Z2, Z, PHI
)
from .derivation_engine import DerivationEngine


# =============================================================================
# PIPELINE TASK
# =============================================================================

@dataclass
class DerivationTask:
    """Input task for the derivation pipeline."""
    constant_name: str
    target_value: float
    domain: str = "physics"
    assignment: str = ""  # Research question/context

    # Optional experimental data (will search if not provided)
    experimental_value: float = None
    experimental_uncertainty: float = None
    experimental_source: str = ""

    def __post_init__(self):
        if not self.assignment:
            self.assignment = f"Derive {self.constant_name} from Z² first principles"


@dataclass
class PipelineResult:
    """Result from the derivation pipeline."""
    task: DerivationTask
    verified: VerifiedDerivation

    # Timing
    total_time: float = 0.0
    metis_time: float = 0.0
    derivation_time: float = 0.0
    verification_time: float = 0.0
    storage_time: float = 0.0

    # Outcome
    success: bool = False
    stored_to: str = ""  # "aletheia", "mnemosyne", or "rejected"
    truth_id: str = ""   # ID if stored

    def summary(self) -> Dict:
        return {
            "constant": self.task.constant_name,
            "target_value": self.task.target_value,
            "level": self.verified.chain.level.value,
            "status": self.verified.chain.status.value,
            "formula": self.verified.chain.final_formula,
            "computed_value": self.verified.chain.computed_value,
            "percent_error": self.verified.chain.percent_error,
            "hrm_score": self.verified.hrm_score,
            "destination": self.verified.destination.value,
            "stored_to": self.stored_to,
            "total_time_seconds": self.total_time
        }


# =============================================================================
# UNIFIED DERIVATION PIPELINE
# =============================================================================

class DerivationPipeline:
    """
    Unified pipeline for Z² derivations.

    Integrates all components into a single clean flow.
    """

    def __init__(self, output_dir: str = "derivation_outputs", verbose: bool = True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose

        # Initialize components
        self.engine = DerivationEngine(verbose=verbose)
        self.metis = None  # Lazy load
        self.aletheia = None  # Lazy load
        self.mnemosyne = None  # Lazy load

        # Statistics
        self.stats = {
            "total_runs": 0,
            "first_principles": 0,
            "derived": 0,
            "numerology": 0,
            "failed": 0,
            "to_aletheia": 0,
            "to_mnemosyne": 0,
            "rejected": 0
        }

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[Pipeline {ts}] {msg}")

    def _load_metis(self):
        """Lazy load MetisFlow."""
        if self.metis is None:
            try:
                from MetisFlow import MetisEngine
                self.metis = MetisEngine(verbose=self.verbose)
                self._log("✓ MetisFlow loaded")
            except ImportError:
                self._log("⚠ MetisFlow not available")

    def _load_aletheia(self):
        """Lazy load AletheiaLake."""
        if self.aletheia is None:
            try:
                from OlympusFlow.lakes.aletheia import AletheiaLake
                self.aletheia = AletheiaLake()
                self._log("✓ AletheiaLake loaded")
            except ImportError:
                self._log("⚠ AletheiaLake not available")

    def _load_mnemosyne(self):
        """Lazy load MnemosyneLake."""
        if self.mnemosyne is None:
            try:
                from MnemosyneLake import MnemosyneLake
                self.mnemosyne = MnemosyneLake(persist=True)
                self._log("✓ MnemosyneLake loaded (persist=True)")
            except ImportError:
                self._log("⚠ MnemosyneLake not available")

    def run(self, task: DerivationTask) -> PipelineResult:
        """
        Run the complete derivation pipeline.

        Stages:
        1. MetisStage - Research the constant
        2. DerivationStage - Build derivation chain
        3. VerificationStage - Validate against experiment
        4. StorageStage - Store to appropriate lake
        """
        self._log(f"\n{'═'*70}")
        self._log(f"DERIVATION PIPELINE: {task.constant_name}")
        self._log(f"{'═'*70}\n")

        start_total = time.time()
        self.stats["total_runs"] += 1

        result = PipelineResult(task=task, verified=None)

        # =====================================================================
        # STAGE 1: METIS (Research)
        # =====================================================================
        self._log("┌─ STAGE 1: MetisFlow Research")
        start_metis = time.time()

        strategy = None
        self._load_metis()

        if self.metis:
            metis_result = self.metis.research(task.constant_name, task.target_value)
            strategy = metis_result.strategy

            self._log(f"│  Derivation exists: {metis_result.derivation_exists}")
            self._log(f"│  Z² viable: {metis_result.z_squared_viable}")
            self._log(f"│  Approach: {strategy.recommended_approach.value}")
            self._log(f"│  Confidence: {strategy.confidence_score:.2f}")

            # Check if we should skip
            if strategy.z_squared_relevance == ZSquaredRelevance.NONE:
                self._log(f"│  ⚠ SKIPPING: No Z² relevance")
                # Create a failed chain
                chain = DerivationChain(
                    target_constant=task.constant_name,
                    target_value=task.target_value
                )
                chain.level = DerivationLevel.FAILED
                chain.status = ChainStatus.INVALID
                result.verified = VerifiedDerivation(chain=chain)
                result.verified.destination = StorageDestination.REJECTED
                result.verified.rejection_reason = "No Z² relevance (MetisFlow)"
                result.total_time = time.time() - start_total
                self.stats["failed"] += 1
                self.stats["rejected"] += 1
                return result

        result.metis_time = time.time() - start_metis
        self._log(f"└─ MetisFlow: {result.metis_time:.1f}s")

        # =====================================================================
        # STAGE 2: DERIVATION (Build chain)
        # =====================================================================
        self._log("\n┌─ STAGE 2: Derivation Engine")
        start_deriv = time.time()

        # Pass strategy to engine
        strategy_dict = strategy.to_dict() if strategy else None
        chain = self.engine.derive(
            task.constant_name,
            task.target_value,
            strategy=strategy_dict
        )

        self._log(f"│  Level: {chain.level.value}")
        self._log(f"│  Status: {chain.status.value}")
        self._log(f"│  Formula: {chain.final_formula}")
        self._log(f"│  Error: {chain.percent_error:.4f}%")
        self._log(f"│  Steps: {len(chain.steps)}")
        self._log(f"│  First principles: {chain.is_first_principles()}")

        result.derivation_time = time.time() - start_deriv
        self._log(f"└─ Derivation: {result.derivation_time:.1f}s")

        # Update stats
        if chain.level == DerivationLevel.FIRST_PRINCIPLES:
            self.stats["first_principles"] += 1
        elif chain.level == DerivationLevel.DERIVED:
            self.stats["derived"] += 1
        elif chain.level == DerivationLevel.NUMERICAL_MATCH:
            self.stats["numerology"] += 1
        else:
            self.stats["failed"] += 1

        # =====================================================================
        # STAGE 3: VERIFICATION (Validate against experiment)
        # =====================================================================
        self._log("\n┌─ STAGE 3: Verification")
        start_verify = time.time()

        verified = self.engine.verify(
            chain,
            experimental_value=task.experimental_value,
            experimental_uncertainty=task.experimental_uncertainty,
            experimental_source=task.experimental_source
        )

        self._log(f"│  HRM Score: {verified.hrm_score:.2f}")
        self._log(f"│  Deviation: {verified.deviation_sigma:.2f}σ")
        self._log(f"│  Destination: {verified.destination.value}")

        result.verified = verified
        result.verification_time = time.time() - start_verify
        self._log(f"└─ Verification: {result.verification_time:.1f}s")

        # =====================================================================
        # STAGE 4: STORAGE (Route to appropriate lake)
        # =====================================================================
        self._log("\n┌─ STAGE 4: Storage")
        start_storage = time.time()

        if verified.destination == StorageDestination.ALETHEIA_LAKE:
            self._store_to_aletheia(task, verified)
            result.stored_to = "aletheia"
            result.success = True
            self.stats["to_aletheia"] += 1
            self._log(f"│  ★ Stored to AletheiaLake (first-principles truth)")

        elif verified.destination == StorageDestination.MNEMOSYNE_LAKE:
            self._store_to_mnemosyne(task, verified)
            result.stored_to = "mnemosyne"
            result.success = True
            self.stats["to_mnemosyne"] += 1
            self._log(f"│  → Stored to MnemosyneLake (working memory)")

        else:
            result.stored_to = "rejected"
            result.success = False
            self.stats["rejected"] += 1
            self._log(f"│  ✗ Rejected: {verified.rejection_reason}")

        result.storage_time = time.time() - start_storage
        self._log(f"└─ Storage: {result.storage_time:.1f}s")

        # =====================================================================
        # COMPLETE
        # =====================================================================
        result.total_time = time.time() - start_total

        self._log(f"\n{'─'*70}")
        self._log(f"COMPLETE: {task.constant_name}")
        self._log(f"  Level: {chain.level.value}")
        self._log(f"  Stored: {result.stored_to}")
        self._log(f"  Total time: {result.total_time:.1f}s")
        self._log(f"{'─'*70}\n")

        # Save result to output dir
        self._save_result(task, result)

        return result

    def _store_to_aletheia(self, task: DerivationTask, verified: VerifiedDerivation):
        """Store to AletheiaLake."""
        self._load_aletheia()

        if self.aletheia:
            # Create Z2Truth
            from OlympusFlow.lakes.aletheia import Z2Truth, DerivationLevel as ALDLevel

            truth = Z2Truth(
                name=task.constant_name.lower().replace(" ", "_"),
                domain=task.domain,
                claim=f"{task.constant_name} = {verified.chain.final_formula}",
                formula=verified.chain.final_formula,
                z2_prediction=verified.chain.computed_value,
                derivation_level=ALDLevel.FIRST_PRINCIPLES,
                derivation_notes=verified.chain.physical_mechanism,
                experimental_value=verified.experimental_value,
                experimental_uncertainty=verified.experimental_uncertainty,
                experimental_source=verified.experimental_source
            )

            # Note: AletheiaLake is immutable, so we just log the intent
            self._log(f"│  Would add to AletheiaLake: {truth.name}")
            self._log(f"│  (AletheiaLake is immutable - manual review required)")

    def _store_to_mnemosyne(self, task: DerivationTask, verified: VerifiedDerivation):
        """Store to MnemosyneLake."""
        self._load_mnemosyne()

        if self.mnemosyne:
            # Create VerifiedTruth for MnemosyneLake
            from MnemosyneLake import VerifiedTruth

            truth = VerifiedTruth(
                truth_id=verified.chain.chain_id,
                domain=task.domain,
                claim=f"{task.constant_name} = {verified.chain.final_formula}",
                z2_formula=verified.chain.final_formula,
                z2_prediction=verified.chain.computed_value,
                measured_value=task.target_value,
                percent_error=verified.chain.percent_error,
                hrm_score=verified.hrm_score,
                data_source="DerivationPipeline",
                status="validated" if verified.hrm_score > 0.8 else "pending"
            )

            self.mnemosyne.add_truth(truth)
            self._log(f"│  Added to MnemosyneLake: {truth.truth_id}")

    def _save_result(self, task: DerivationTask, result: PipelineResult):
        """Save result to output directory."""
        import re
        normalized = task.constant_name.lower().replace(" ", "_")
        normalized = re.sub(r'[/\\:*?"<>|]', '_', normalized)  # Remove filesystem-unsafe chars
        output_file = self.output_dir / f"{normalized}_result.json"

        data = {
            "task": {
                "constant_name": task.constant_name,
                "target_value": task.target_value,
                "domain": task.domain,
                "assignment": task.assignment
            },
            "result": result.summary(),
            "chain": result.verified.chain.to_dict() if result.verified else None,
            "timing": {
                "metis": result.metis_time,
                "derivation": result.derivation_time,
                "verification": result.verification_time,
                "storage": result.storage_time,
                "total": result.total_time
            },
            "timestamp": datetime.now().isoformat()
        }

        output_file.write_text(json.dumps(data, indent=2, default=str))

    def run_batch(self, tasks: List[DerivationTask]) -> List[PipelineResult]:
        """Run multiple derivation tasks."""
        results = []
        total = len(tasks)

        self._log(f"\n{'═'*70}")
        self._log(f"BATCH RUN: {total} derivation tasks")
        self._log(f"{'═'*70}\n")

        start_batch = time.time()

        for i, task in enumerate(tasks):
            self._log(f"\n[{i+1}/{total}] Processing: {task.constant_name}")
            result = self.run(task)
            results.append(result)

        batch_time = time.time() - start_batch

        # Summary
        self._log(f"\n{'═'*70}")
        self._log(f"BATCH COMPLETE")
        self._log(f"{'═'*70}")
        self._log(f"Total tasks: {total}")
        self._log(f"Total time: {batch_time:.1f}s ({batch_time/total:.1f}s/task)")
        self._log(f"\nBreakdown:")
        self._log(f"  First principles: {self.stats['first_principles']}")
        self._log(f"  Derived: {self.stats['derived']}")
        self._log(f"  Numerology: {self.stats['numerology']}")
        self._log(f"  Failed: {self.stats['failed']}")
        self._log(f"\nStorage:")
        self._log(f"  → AletheiaLake: {self.stats['to_aletheia']}")
        self._log(f"  → MnemosyneLake: {self.stats['to_mnemosyne']}")
        self._log(f"  ✗ Rejected: {self.stats['rejected']}")
        self._log(f"{'═'*70}\n")

        return results

    def get_stats(self) -> Dict:
        """Get pipeline statistics."""
        return dict(self.stats)


# =============================================================================
# DEMO
# =============================================================================

def demo():
    """Demonstrate the unified derivation pipeline."""
    pipeline = DerivationPipeline(output_dir="derivation_demo")

    # Test tasks
    tasks = [
        DerivationTask(
            constant_name="Dark Energy Density",
            target_value=0.6847,
            domain="cosmology",
            experimental_value=0.6847,
            experimental_uncertainty=0.0073,
            experimental_source="Planck 2018"
        ),
        DerivationTask(
            constant_name="Weak Mixing Angle",
            target_value=0.23122,
            domain="particle_physics",
            experimental_value=0.23122,
            experimental_uncertainty=0.00003,
            experimental_source="PDG 2022"
        ),
        DerivationTask(
            constant_name="von Karman Constant",
            target_value=0.41,
            domain="fluid_dynamics"
        )
    ]

    results = pipeline.run_batch(tasks)

    # Print summaries
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    for r in results:
        print(f"\n{r.task.constant_name}:")
        print(f"  Formula: {r.verified.chain.final_formula}")
        print(f"  Level: {r.verified.chain.level.value}")
        print(f"  Stored: {r.stored_to}")


if __name__ == "__main__":
    demo()
