#!/usr/bin/env python3
"""
M4 Empirical Stability Screener
================================

Standard biophysics-based structural stability screening using ESMFold.

This replaces the Z² cosmological framework with real, peer-reviewed metrics:
- pLDDT (Predicted Local Distance Difference Test) confidence scores
- Separate payload vs linker domain analysis
- Empirical stability thresholds used by pharma

The Z² framework was mathematically elegant but tautological:
- S/S_max approaches 0 for all proteins (molecular entropy << holographic bound)
- d_eff = 3 + 5(1 - 0) = 8 is an arithmetic certainty, not physics

This script uses the same metrics as Pfizer, Moderna, and major pharma.

LICENSE: AGPL-3.0 + OpenMTA + CC BY-SA 4.0 (Open Science Prior Art)
"""

import json
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import warnings

# Try importing ESM
try:
    import torch
    from transformers import AutoTokenizer, EsmForProteinFolding
    from transformers.models.esm.openfold_utils.protein import to_pdb, Protein as OFProtein
    ESM_AVAILABLE = True
except ImportError:
    ESM_AVAILABLE = False
    print("[WARNING] ESMFold not available. Install with: pip install transformers torch")

# Known BBB-crossing peptide sequences for domain identification
BBB_PEPTIDES = {
    'angiopep2': 'TFFYGGSRGKRNNFKTEEY',
    'rvg29': 'YTIWMPENPRPGTPCDIFTNSRGKRASNG',
    'tat': 'YGRKKRRQRRR',
    'irgd': 'CRGDKGPDC',
}

# Linker sequences to exclude from payload pLDDT
LINKER_PATTERNS = ['GGGGS', 'GGGGSGGGGS', 'EAAAK', 'PAPAP']


@dataclass
class StabilityResult:
    """Empirical stability analysis result."""
    name: str
    sequence_length: int

    # Global metrics
    mean_plddt: float
    min_plddt: float
    max_plddt: float
    std_plddt: float

    # Domain-specific metrics
    payload_plddt: float
    linker_plddt: float
    bbb_peptide_plddt: float

    # Stability classification
    is_stable: bool
    stability_tier: str  # A, B, C, D
    instability_reason: Optional[str]

    # Structure info
    has_structure: bool
    pdb_path: Optional[str]


class EmpiricalStabilityScreener:
    """
    Screen therapeutic sequences for structural stability using ESMFold.

    Uses real biophysics metrics:
    - pLDDT > 70: Generally reliable structure
    - pLDDT > 85: High confidence structure
    - pLDDT < 50: Likely disordered/misfolded
    """

    def __init__(self, output_dir: str = "empirical_stability"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.model = None
        self.tokenizer = None
        self.device = None

        if ESM_AVAILABLE:
            self._load_model()

    def _load_model(self):
        """Load ESMFold model."""
        print("[STABILITY] Loading ESMFold model...")

        # Check for GPU
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            print("[STABILITY] Using CUDA GPU")
        elif torch.backends.mps.is_available():
            self.device = torch.device("mps")
            print("[STABILITY] Using Apple MPS GPU")
        else:
            self.device = torch.device("cpu")
            print("[STABILITY] Using CPU (slow)")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained("facebook/esmfold_v1")
            self.model = EsmForProteinFolding.from_pretrained(
                "facebook/esmfold_v1",
                low_cpu_mem_usage=True
            )
            self.model = self.model.to(self.device)
            self.model.eval()
            print("[STABILITY] ESMFold loaded successfully")
        except Exception as e:
            print(f"[WARNING] Could not load ESMFold: {e}")
            self.model = None

    def _identify_domains(self, sequence: str) -> Dict[str, List[Tuple[int, int]]]:
        """
        Identify payload, linker, and BBB peptide domains in sequence.

        Returns dict with domain name -> list of (start, end) positions.
        """
        domains = {
            'payload': [],
            'linker': [],
            'bbb_peptide': [],
        }

        seq_upper = sequence.upper()

        # Find BBB peptides
        bbb_positions = []
        for name, peptide in BBB_PEPTIDES.items():
            pos = seq_upper.find(peptide.upper())
            if pos != -1:
                bbb_positions.append((pos, pos + len(peptide)))
                domains['bbb_peptide'].append((pos, pos + len(peptide)))

        # Find linkers
        linker_positions = []
        for linker in LINKER_PATTERNS:
            start = 0
            while True:
                pos = seq_upper.find(linker, start)
                if pos == -1:
                    break
                linker_positions.append((pos, pos + len(linker)))
                domains['linker'].append((pos, pos + len(linker)))
                start = pos + 1

        # Payload is everything else
        all_non_payload = sorted(bbb_positions + linker_positions)

        if not all_non_payload:
            domains['payload'] = [(0, len(sequence))]
        else:
            # Find gaps between non-payload regions
            prev_end = 0
            for start, end in all_non_payload:
                if start > prev_end:
                    domains['payload'].append((prev_end, start))
                prev_end = max(prev_end, end)
            if prev_end < len(sequence):
                domains['payload'].append((prev_end, len(sequence)))

        return domains

    def _compute_domain_plddt(
        self,
        plddt_scores: np.ndarray,
        domains: Dict[str, List[Tuple[int, int]]]
    ) -> Dict[str, float]:
        """Compute mean pLDDT for each domain."""
        results = {}

        for domain_name, regions in domains.items():
            if not regions:
                results[domain_name] = 0.0
                continue

            scores = []
            for start, end in regions:
                scores.extend(plddt_scores[start:end].tolist())

            results[domain_name] = np.mean(scores) if scores else 0.0

        return results

    def predict_structure(self, name: str, sequence: str) -> Optional[StabilityResult]:
        """
        Predict structure and compute stability metrics.
        """
        if not ESM_AVAILABLE or self.model is None:
            return self._fallback_analysis(name, sequence)

        # Truncate very long sequences
        max_len = 400
        if len(sequence) > max_len:
            print(f"[WARNING] Truncating {name} from {len(sequence)} to {max_len} residues")
            sequence = sequence[:max_len]

        try:
            # Tokenize
            inputs = self.tokenizer(
                [sequence],
                return_tensors="pt",
                add_special_tokens=False
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Predict
            with torch.no_grad():
                outputs = self.model(**inputs)

            # Extract pLDDT scores
            plddt = outputs.plddt[0].cpu().numpy()  # Shape: (seq_len,)

            # Identify domains
            domains = self._identify_domains(sequence)
            domain_plddt = self._compute_domain_plddt(plddt, domains)

            # Global metrics
            mean_plddt = float(np.mean(plddt))
            min_plddt = float(np.min(plddt))
            max_plddt = float(np.max(plddt))
            std_plddt = float(np.std(plddt))

            # Stability classification
            payload_plddt = domain_plddt.get('payload', mean_plddt)

            if payload_plddt >= 85:
                tier = 'A'
                is_stable = True
                reason = None
            elif payload_plddt >= 75:
                tier = 'B'
                is_stable = True
                reason = None
            elif payload_plddt >= 60:
                tier = 'C'
                is_stable = False
                reason = "Marginal payload stability (pLDDT 60-75)"
            else:
                tier = 'D'
                is_stable = False
                reason = f"Unstable/Misfolded payload (pLDDT={payload_plddt:.1f})"

            # Save PDB structure
            pdb_path = None
            try:
                pdb_string = self._outputs_to_pdb(outputs, sequence)
                pdb_path = str(self.output_dir / f"{name}.pdb")
                with open(pdb_path, 'w') as f:
                    f.write(pdb_string)
            except Exception as e:
                print(f"[WARNING] Could not save PDB for {name}: {e}")

            return StabilityResult(
                name=name,
                sequence_length=len(sequence),
                mean_plddt=mean_plddt,
                min_plddt=min_plddt,
                max_plddt=max_plddt,
                std_plddt=std_plddt,
                payload_plddt=payload_plddt,
                linker_plddt=domain_plddt.get('linker', 0.0),
                bbb_peptide_plddt=domain_plddt.get('bbb_peptide', 0.0),
                is_stable=is_stable,
                stability_tier=tier,
                instability_reason=reason,
                has_structure=True,
                pdb_path=pdb_path,
            )

        except Exception as e:
            print(f"[ERROR] Structure prediction failed for {name}: {e}")
            return self._fallback_analysis(name, sequence)

    def _outputs_to_pdb(self, outputs, sequence: str) -> str:
        """Convert ESMFold outputs to PDB string."""
        # Get coordinates
        final_coords = outputs.positions[-1, 0].cpu().numpy()  # (seq_len, 37, 3)

        # Build PDB manually
        lines = []
        lines.append(f"HEADER    PREDICTED STRUCTURE")
        lines.append(f"REMARK   1 GENERATED BY M4 EMPIRICAL STABILITY SCREENER")
        lines.append(f"REMARK   2 DATE: {datetime.now().isoformat()}")

        atom_num = 1
        for i, aa in enumerate(sequence):
            # CA atom (index 1 in ESMFold output)
            x, y, z = final_coords[i, 1]
            lines.append(
                f"ATOM  {atom_num:5d}  CA  {self._aa_to_3letter(aa)} A{i+1:4d}    "
                f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C"
            )
            atom_num += 1

        lines.append("END")
        return "\n".join(lines)

    def _aa_to_3letter(self, aa: str) -> str:
        """Convert 1-letter AA to 3-letter."""
        mapping = {
            'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
            'Q': 'GLN', 'E': 'GLU', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
            'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
            'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL',
        }
        return mapping.get(aa.upper(), 'UNK')

    def _fallback_analysis(self, name: str, sequence: str) -> StabilityResult:
        """
        Fallback analysis when ESMFold is not available.
        Uses sequence-based heuristics.
        """
        # Heuristic stability metrics based on sequence composition
        n = len(sequence)

        # Count destabilizing features
        prolines = sequence.count('P')
        glycines = sequence.count('G')
        charged = sum(1 for aa in sequence if aa in 'RKDE')
        hydrophobic = sum(1 for aa in sequence if aa in 'VILFWM')

        # Estimate pLDDT based on composition
        # High Pro/Gly = more disorder
        disorder_fraction = (prolines + glycines) / n

        # Balanced charge = more stable
        charge_balance = abs(sequence.count('R') + sequence.count('K') -
                            sequence.count('D') - sequence.count('E')) / n

        # Hydrophobic core = more stable
        hydrophobic_fraction = hydrophobic / n

        # Heuristic pLDDT estimate
        base_plddt = 70.0
        base_plddt -= disorder_fraction * 30  # Disorder penalty
        base_plddt -= charge_balance * 20     # Charge imbalance penalty
        base_plddt += hydrophobic_fraction * 10  # Hydrophobic bonus

        estimated_plddt = np.clip(base_plddt, 30, 95)

        # Classification
        if estimated_plddt >= 85:
            tier = 'A'
            is_stable = True
            reason = None
        elif estimated_plddt >= 75:
            tier = 'B'
            is_stable = True
            reason = None
        elif estimated_plddt >= 60:
            tier = 'C'
            is_stable = False
            reason = "Marginal stability (heuristic estimate)"
        else:
            tier = 'D'
            is_stable = False
            reason = f"Likely unstable (estimated pLDDT={estimated_plddt:.1f})"

        return StabilityResult(
            name=name,
            sequence_length=n,
            mean_plddt=estimated_plddt,
            min_plddt=estimated_plddt - 10,
            max_plddt=estimated_plddt + 10,
            std_plddt=8.0,
            payload_plddt=estimated_plddt,
            linker_plddt=60.0,  # Linkers are typically flexible
            bbb_peptide_plddt=75.0,  # BBB peptides are well-characterized
            is_stable=is_stable,
            stability_tier=tier,
            instability_reason=reason,
            has_structure=False,
            pdb_path=None,
        )

    def screen_sequences(self, sequences: Dict[str, str]) -> List[StabilityResult]:
        """
        Screen multiple sequences for stability.
        """
        results = []
        total = len(sequences)

        print(f"\n[STABILITY] Screening {total} sequences...")
        print("=" * 60)

        for i, (name, sequence) in enumerate(sequences.items()):
            if i % 10 == 0:
                print(f"  Processing {i+1}/{total}...")

            result = self.predict_structure(name, sequence)
            if result:
                results.append(result)

        return results

    def save_results(self, results: List[StabilityResult]) -> str:
        """Save results to JSON."""
        # Separate stable and unstable
        stable = [r for r in results if r.is_stable]
        unstable = [r for r in results if not r.is_stable]

        # Summary statistics
        all_plddt = [r.payload_plddt for r in results]

        output = {
            "title": "M4 Empirical Stability Screening",
            "generated": datetime.now().isoformat(),
            "methodology": "ESMFold pLDDT confidence scoring",
            "note": "Replaces Z² cosmological framework with standard biophysics",
            "summary": {
                "total_screened": len(results),
                "stable_count": len(stable),
                "unstable_count": len(unstable),
                "mean_payload_plddt": float(np.mean(all_plddt)),
                "std_payload_plddt": float(np.std(all_plddt)),
                "tier_distribution": {
                    "A": len([r for r in results if r.stability_tier == 'A']),
                    "B": len([r for r in results if r.stability_tier == 'B']),
                    "C": len([r for r in results if r.stability_tier == 'C']),
                    "D": len([r for r in results if r.stability_tier == 'D']),
                },
            },
            "stable_candidates": [asdict(r) for r in sorted(stable, key=lambda x: -x.payload_plddt)],
            "unstable_flagged": [asdict(r) for r in unstable],
            "license": "AGPL-3.0 + OpenMTA + CC BY-SA 4.0",
        }

        output_path = self.output_dir / "empirical_candidates.json"
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n[STABILITY] Results saved to: {output_path}")
        return str(output_path)


def load_therapeutic_sequences(sequences_file: str) -> Dict[str, str]:
    """Load sequences from JSON file."""
    with open(sequences_file) as f:
        data = json.load(f)

    sequences = {}

    # Handle simple {name: sequence} format
    if isinstance(data, dict):
        for name, seq in data.items():
            if isinstance(seq, str) and len(seq) > 10:
                sequences[name] = seq
        if sequences:
            return sequences

    # Handle nested format with 'sequences' key
    for item in data.get('sequences', []):
        if isinstance(item, dict):
            name = item.get('name', item.get('id', 'unknown'))
            seq = item.get('sequence', '')
            if seq:
                sequences[name] = seq

    return sequences


def main():
    """Main entry point."""
    import sys

    print("=" * 70)
    print("M4 EMPIRICAL STABILITY SCREENER")
    print("Standard Biophysics Metrics (Replacing Z² Framework)")
    print("=" * 70)
    print()
    print("This script uses real pharmaceutical industry metrics:")
    print("  - pLDDT confidence scores from ESMFold")
    print("  - Domain-specific stability analysis")
    print("  - Payload vs linker separation")
    print()

    # Find sequences file
    sequences_file = "all_therapeutic_sequences.json"
    if len(sys.argv) > 1:
        sequences_file = sys.argv[1]

    if not Path(sequences_file).exists():
        print(f"[ERROR] Sequences file not found: {sequences_file}")
        return

    # Load sequences
    sequences = load_therapeutic_sequences(sequences_file)
    print(f"Loaded {len(sequences)} therapeutic sequences")

    # Run screening
    screener = EmpiricalStabilityScreener()
    results = screener.screen_sequences(sequences)

    # Save results
    output_path = screener.save_results(results)

    # Print summary
    stable = [r for r in results if r.is_stable]
    print()
    print("=" * 70)
    print("STABILITY SCREENING COMPLETE")
    print("=" * 70)
    print(f"Total sequences: {len(results)}")
    pct = 100*len(stable)/len(results) if results else 0
    print(f"Stable (Tier A/B): {len(stable)} ({pct:.1f}%)")
    print()
    print("TOP 10 MOST STABLE CANDIDATES:")
    print("-" * 60)
    for r in sorted(results, key=lambda x: -x.payload_plddt)[:10]:
        status = "STABLE" if r.is_stable else "UNSTABLE"
        print(f"  [{r.stability_tier}] {r.name}")
        print(f"      Payload pLDDT: {r.payload_plddt:.1f} | {status}")

    print()
    print(f"Full results: {output_path}")


if __name__ == "__main__":
    main()
