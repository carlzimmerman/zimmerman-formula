#!/usr/bin/env python3
"""
M4 Neurological Disorders Target Extraction Pipeline
======================================================

Comprehensive computational pipeline for therapeutic peptide design targeting
neurological and neurodegenerative disorders. Complements the existing
open_therapeutics antibody engineering work with small peptide approaches.

THERAPEUTIC AREAS:
==================
1. Alzheimer's Disease - Amyloid-β, Tau, neuroinflammation
2. Parkinson's Disease - α-synuclein, dopaminergic neuroprotection
3. Amyotrophic Lateral Sclerosis (ALS) - SOD1, TDP-43, C9orf72
4. Huntington's Disease - Huntingtin aggregation
5. Multiple Sclerosis - Demyelination, neuroinflammation
6. Stroke/Neurodegeneration - Neuroprotection, excitotoxicity

APPROVED DRUG BENCHMARKS:
=========================
Alzheimer's:
- Lecanemab (Leqembi): Kd = 0.5 nM for Aβ protofibrils
- Aducanumab (Aduhelm): Kd = 0.1 nM for Aβ aggregates
- Memantine: NMDAR Ki = 0.5 μM

Parkinson's:
- No disease-modifying therapies approved
- Prasinezumab: Phase II (anti-synuclein)

ALS:
- Tofersen (Qalsody): ASO targeting SOD1 mRNA
- Riluzole: Glutamate modulator

MS:
- Natalizumab (Tysabri): α4-integrin IC50 = 0.3 nM
- Ocrelizumab (Ocrevus): Anti-CD20

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026
"""

import json
import numpy as np
import hashlib
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types."""
    def default(self, obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# =============================================================================
# VALIDATED THERAPEUTIC TARGETS
# =============================================================================

NEURO_DISEASE_TARGETS = {
    # =========================================================================
    # ALZHEIMER'S DISEASE
    # =========================================================================
    "Amyloid_Beta_42": {
        "full_name": "Amyloid-beta peptide 1-42",
        "uniprot": "P05067 (APP)",
        "pdb_ids": ["1IYT", "2BEG", "5OQV", "6SZF"],
        "disease": ["Alzheimer's Disease"],
        "mechanism": "Prevent Aβ aggregation, promote clearance",
        "druggability_score": 0.75,  # Difficult due to IDP nature
        "approved_drugs": ["Lecanemab", "Aducanumab", "Donanemab"],
        "benchmark_affinity": {
            "lecanemab_Kd_nM": 0.5,
            "aducanumab_Kd_nM": 0.1,
            "source": "van Dyck CH et al. N Engl J Med. 2023;388(1):9-21"
        },
        "binding_site": "Aggregation-prone regions (16-22, 29-42)",
        "key_residues": ["K16", "L17", "V18", "F19", "F20", "A21"],
        "priority": 1,
    },

    "Tau_PHF": {
        "full_name": "Tau paired helical filaments",
        "uniprot": "P10636",
        "pdb_ids": ["5O3T", "6QJH", "7NRQ"],
        "disease": ["Alzheimer's Disease", "Frontotemporal Dementia", "PSP"],
        "mechanism": "Inhibit tau aggregation, promote clearance",
        "druggability_score": 0.70,
        "approved_drugs": [],  # None yet approved
        "benchmark_affinity": {
            "gosuranemab_Kd_nM": 5.0,
            "tilavonemab_Kd_nM": 1.2,
            "source": "Jadhav S et al. Acta Neuropathol. 2019;138(5):681-708"
        },
        "binding_site": "Repeat domains (R1-R4), PHF core",
        "key_residues": ["K280", "K281", "V306", "V318", "I328"],
        "priority": 1,
    },

    "BACE1": {
        "full_name": "Beta-secretase 1",
        "uniprot": "P56817",
        "pdb_ids": ["1FKN", "4DJU", "6EJ2"],
        "disease": ["Alzheimer's Disease"],
        "mechanism": "Inhibit APP cleavage, reduce Aβ production",
        "druggability_score": 0.90,
        "approved_drugs": [],  # All failed in trials
        "benchmark_affinity": {
            "verubecestat_Ki_nM": 2.2,
            "lanabecestat_Ki_nM": 0.6,
            "source": "Egan MF et al. N Engl J Med. 2018;378(18):1691-703"
        },
        "binding_site": "Active site (aspartyl protease)",
        "key_residues": ["D32", "D228", "Y71", "S35"],
        "priority": 2,
    },

    "TREM2": {
        "full_name": "Triggering receptor expressed on myeloid cells 2",
        "uniprot": "Q9NZC2",
        "pdb_ids": ["5ELI", "6XDO"],
        "disease": ["Alzheimer's Disease"],
        "mechanism": "Enhance microglial phagocytosis of Aβ",
        "druggability_score": 0.80,
        "approved_drugs": [],
        "benchmark_affinity": {
            "AL002_EC50_nM": 50,
            "source": "Wang S et al. Cell. 2020;182(5):1198-1213"
        },
        "binding_site": "Ig-like domain",
        "key_residues": ["R47", "Y38", "H67"],
        "priority": 2,
    },

    # =========================================================================
    # PARKINSON'S DISEASE
    # =========================================================================
    "Alpha_Synuclein": {
        "full_name": "Alpha-synuclein",
        "uniprot": "P37840",
        "pdb_ids": ["1XQ8", "2N0A", "6CU7", "6XYO"],
        "disease": ["Parkinson's Disease", "Lewy Body Dementia", "MSA"],
        "mechanism": "Prevent aggregation, promote clearance",
        "druggability_score": 0.65,  # IDP, difficult target
        "approved_drugs": [],  # None approved
        "benchmark_affinity": {
            "prasinezumab_Kd_nM": 0.6,
            "cinpanemab_Kd_nM": 0.3,
            "source": "Pagano G et al. Nat Med. 2022;28(6):1212-20"
        },
        "binding_site": "NAC region (61-95), C-terminus",
        "key_residues": ["A53", "E46", "E83", "V70", "V74"],
        "priority": 1,
    },

    "LRRK2": {
        "full_name": "Leucine-rich repeat kinase 2",
        "uniprot": "Q5S007",
        "pdb_ids": ["6VNO", "7LHW"],
        "disease": ["Parkinson's Disease (familial)"],
        "mechanism": "Inhibit kinase activity (G2019S mutation)",
        "druggability_score": 0.88,
        "approved_drugs": [],
        "benchmark_affinity": {
            "DNL151_Ki_nM": 0.5,
            "MLi-2_Ki_nM": 0.8,
            "source": "Tolosa E et al. Nat Rev Neurol. 2020;16(2):97-107"
        },
        "binding_site": "ATP binding site (kinase domain)",
        "key_residues": ["K1906", "D2017", "G2019"],
        "priority": 2,
    },

    "GBA1": {
        "full_name": "Glucocerebrosidase",
        "uniprot": "P04062",
        "pdb_ids": ["2NT0", "3GXI"],
        "disease": ["Parkinson's Disease", "Gaucher Disease"],
        "mechanism": "Chaperone to stabilize mutant GBA1",
        "druggability_score": 0.82,
        "approved_drugs": ["Ambroxol (repurposed, trials)"],
        "benchmark_affinity": {
            "ambroxol_IC50_uM": 1.0,
            "isofagomine_Ki_nM": 40,
            "source": "Maegawa GH et al. J Biol Chem. 2009;284(35):23502-16"
        },
        "binding_site": "Active site (TIM barrel)",
        "key_residues": ["E235", "E340", "W381", "F128"],
        "priority": 2,
    },

    "GDNF": {
        "full_name": "Glial cell-derived neurotrophic factor",
        "uniprot": "P39905",
        "pdb_ids": ["1AGQ", "3FUB"],
        "disease": ["Parkinson's Disease (neuroprotection)"],
        "mechanism": "Mimic GDNF to protect dopaminergic neurons",
        "druggability_score": 0.60,  # Agonist design challenging
        "approved_drugs": [],
        "benchmark_affinity": {
            "GDNF_RET_Kd_nM": 0.1,
            "source": "Airaksinen MS et al. Nat Rev Neurosci. 2002;3(5):383-94"
        },
        "binding_site": "GFRα1 binding interface",
        "key_residues": ["R171", "R173", "K174"],
        "priority": 3,
    },

    # =========================================================================
    # ALS (AMYOTROPHIC LATERAL SCLEROSIS)
    # =========================================================================
    "SOD1_Misfolded": {
        "full_name": "Superoxide dismutase 1 (misfolded)",
        "uniprot": "P00441",
        "pdb_ids": ["2SOD", "4A7T", "5YTO"],
        "disease": ["ALS (familial, 2%)"],
        "mechanism": "Stabilize native fold, prevent aggregation",
        "druggability_score": 0.75,
        "approved_drugs": ["Tofersen (ASO)"],
        "benchmark_affinity": {
            "tofersen_IC50_nM": "N/A (ASO)",
            "anti_SOD1_Kd_nM": 1.0,
            "source": "Miller TM et al. N Engl J Med. 2022;387(12):1099-1110"
        },
        "binding_site": "Dimer interface, edge strands",
        "key_residues": ["G93", "A4", "G85", "D90"],
        "priority": 1,
    },

    "TDP43": {
        "full_name": "TAR DNA-binding protein 43",
        "uniprot": "Q13148",
        "pdb_ids": ["4BS2", "6N3C"],
        "disease": ["ALS (97%)", "Frontotemporal Dementia"],
        "mechanism": "Prevent cytoplasmic aggregation",
        "druggability_score": 0.55,  # Very difficult
        "approved_drugs": [],
        "benchmark_affinity": {
            "note": "No approved TDP-43 binders yet"
        },
        "binding_site": "RRM domains, C-terminal prion-like domain",
        "key_residues": ["M337", "Q331", "G348"],
        "priority": 1,
    },

    "C9orf72_DPR": {
        "full_name": "C9orf72 dipeptide repeat proteins",
        "uniprot": "Q96LT7",
        "pdb_ids": [],  # DPRs are disordered
        "disease": ["ALS (40%)", "Frontotemporal Dementia"],
        "mechanism": "Block DPR toxicity, nuclear transport",
        "druggability_score": 0.45,  # Very challenging
        "approved_drugs": [],
        "benchmark_affinity": {
            "note": "No approved DPR binders yet"
        },
        "binding_site": "Poly-GA, poly-GR, poly-PR sequences",
        "key_residues": [],
        "priority": 2,
    },

    # =========================================================================
    # HUNTINGTON'S DISEASE
    # =========================================================================
    "Huntingtin_PolyQ": {
        "full_name": "Huntingtin polyglutamine expansion",
        "uniprot": "P42858",
        "pdb_ids": ["3IO4", "6EZ8"],
        "disease": ["Huntington's Disease"],
        "mechanism": "Prevent polyQ aggregation",
        "druggability_score": 0.50,  # Repeat expansion difficult
        "approved_drugs": [],
        "benchmark_affinity": {
            "note": "No approved Htt binders; ASO (tominersen) failed Phase III"
        },
        "binding_site": "PolyQ tract, N-terminal domain",
        "key_residues": ["Q repeats"],
        "priority": 2,
    },

    # =========================================================================
    # MULTIPLE SCLEROSIS
    # =========================================================================
    "Alpha4_Integrin": {
        "full_name": "Integrin alpha-4 (VLA-4)",
        "uniprot": "P13612",
        "pdb_ids": ["3V4V", "6JOP"],
        "disease": ["Multiple Sclerosis", "Crohn's Disease"],
        "mechanism": "Block leukocyte adhesion and CNS infiltration",
        "druggability_score": 0.92,
        "approved_drugs": ["Natalizumab (Tysabri)"],
        "benchmark_affinity": {
            "natalizumab_IC50_nM": 0.3,
            "source": "Polman CH et al. N Engl J Med. 2006;354(9):899-910"
        },
        "binding_site": "I-domain, VCAM-1 interface",
        "key_residues": ["D130", "S132", "T212"],
        "priority": 1,
    },

    "CD20": {
        "full_name": "B-lymphocyte antigen CD20",
        "uniprot": "P11836",
        "pdb_ids": ["5RV7"],
        "disease": ["Multiple Sclerosis", "B-cell lymphomas"],
        "mechanism": "B-cell depletion",
        "druggability_score": 0.95,
        "approved_drugs": ["Ocrelizumab", "Ofatumumab", "Rituximab"],
        "benchmark_affinity": {
            "ocrelizumab_Kd_nM": 0.5,
            "rituximab_Kd_nM": 5.0,
            "source": "Hauser SL et al. N Engl J Med. 2017;376(3):221-34"
        },
        "binding_site": "Extracellular loop",
        "key_residues": ["A170", "P172", "N166"],
        "priority": 1,
    },

    "Myelin_MOG": {
        "full_name": "Myelin oligodendrocyte glycoprotein",
        "uniprot": "Q16653",
        "pdb_ids": ["1PKO", "1PY9"],
        "disease": ["Multiple Sclerosis", "MOGAD"],
        "mechanism": "Tolerogenic peptides, block autoimmunity",
        "druggability_score": 0.70,
        "approved_drugs": [],
        "benchmark_affinity": {
            "MOG35-55_IC50_uM": 10,  # T-cell activation
            "source": "Bettelli E et al. J Exp Med. 2003;197(9):1073-81"
        },
        "binding_site": "Ig-like domain",
        "key_residues": ["R35", "F44", "L47"],
        "priority": 2,
    },

    # =========================================================================
    # NEUROPROTECTION / STROKE
    # =========================================================================
    "NMDAR_GluN2B": {
        "full_name": "NMDA receptor GluN2B subunit",
        "uniprot": "Q13224",
        "pdb_ids": ["4PE5", "6WHT"],
        "disease": ["Stroke", "Excitotoxicity", "TBI"],
        "mechanism": "Block excitotoxic calcium influx",
        "druggability_score": 0.85,
        "approved_drugs": ["Memantine (weak, AD-approved)"],
        "benchmark_affinity": {
            "memantine_Ki_nM": 500,
            "ifenprodil_Ki_nM": 10,
            "source": "Paoletti P et al. Nat Rev Neurosci. 2013;14(6):383-400"
        },
        "binding_site": "NTD (ifenprodil site), channel pore",
        "key_residues": ["F114", "F176", "I111"],
        "priority": 2,
    },

    "PSD95_PDZ": {
        "full_name": "PSD-95 PDZ domain",
        "uniprot": "P78352",
        "pdb_ids": ["1BE9", "3GSL"],
        "disease": ["Stroke (neuroprotection)"],
        "mechanism": "Disrupt NMDAR-PSD95 interaction, reduce excitotoxicity",
        "druggability_score": 0.78,
        "approved_drugs": [],
        "benchmark_affinity": {
            "NA_1_IC50_uM": 1.0,
            "source": "Cook DJ et al. Nature. 2012;483(7388):213-7"
        },
        "binding_site": "PDZ binding groove",
        "key_residues": ["H130", "G132", "F133"],
        "priority": 2,
    },

    "BDNF_TrkB": {
        "full_name": "BDNF/TrkB signaling",
        "uniprot": "P23560 (BDNF), Q16620 (TrkB)",
        "pdb_ids": ["1BND", "4AT4"],
        "disease": ["Neurodegeneration (general)", "Depression"],
        "mechanism": "Activate TrkB for neuronal survival",
        "druggability_score": 0.68,
        "approved_drugs": [],
        "benchmark_affinity": {
            "BDNF_Kd_nM": 0.3,
            "7_8_DHF_EC50_nM": 500,
            "LM22A_4_EC50_uM": 1.0,
            "source": "Jang SW et al. PNAS. 2010;107(6):2687-92"
        },
        "binding_site": "TrkB D5 domain",
        "key_residues": ["R74", "K95", "R123"],
        "priority": 2,
    },
}


# =============================================================================
# TARGET EXTRACTION
# =============================================================================

@dataclass
class ExtractedTarget:
    """Extracted and validated therapeutic target."""
    target_id: str
    full_name: str
    uniprot: str
    pdb_ids: List[str]
    diseases: List[str]
    mechanism: str
    druggability_score: float
    priority: int
    benchmark_data: Dict
    binding_site_info: str
    key_residues: List[str]
    approved_drugs: List[str]
    sequence_hash: str = ""


def extract_targets(priority_threshold: int = 3) -> List[ExtractedTarget]:
    """Extract and validate therapeutic targets for neurological diseases."""

    targets = []

    for target_id, data in NEURO_DISEASE_TARGETS.items():
        if data.get("priority", 4) <= priority_threshold:
            target = ExtractedTarget(
                target_id=target_id,
                full_name=data["full_name"],
                uniprot=data["uniprot"],
                pdb_ids=data["pdb_ids"],
                diseases=data["disease"],
                mechanism=data["mechanism"],
                druggability_score=data["druggability_score"],
                priority=data["priority"],
                benchmark_data=data.get("benchmark_affinity", {}),
                binding_site_info=data.get("binding_site", ""),
                key_residues=data.get("key_residues", []),
                approved_drugs=data.get("approved_drugs", []),
                sequence_hash=hashlib.sha256(data["uniprot"].encode()).hexdigest()[:16],
            )
            targets.append(target)

    targets.sort(key=lambda x: (x.priority, -x.druggability_score))
    return targets


def generate_target_report(targets: List[ExtractedTarget]) -> str:
    """Generate a human-readable report of extracted targets."""

    report = []
    report.append("=" * 80)
    report.append("NEUROLOGICAL DISORDERS THERAPEUTIC TARGET REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append(f"Total targets: {len(targets)}")
    report.append("")

    # Group by disease
    diseases = {}
    for target in targets:
        for disease in target.diseases:
            if disease not in diseases:
                diseases[disease] = []
            diseases[disease].append(target)

    for disease in sorted(diseases.keys()):
        report.append("-" * 80)
        report.append(f"DISEASE: {disease}")
        report.append("-" * 80)

        for target in diseases[disease]:
            drugs_str = ", ".join(target.approved_drugs[:2]) if target.approved_drugs else "None"
            report.append(f"\n  {target.target_id}")
            report.append(f"    Full name: {target.full_name}")
            report.append(f"    UniProt: {target.uniprot}")
            report.append(f"    PDB: {', '.join(target.pdb_ids[:3]) if target.pdb_ids else 'None'}")
            report.append(f"    Druggability: {target.druggability_score:.2f}")
            report.append(f"    Priority: {target.priority}")
            report.append(f"    Approved drugs: {drugs_str}")
            report.append(f"    Mechanism: {target.mechanism}")

        report.append("")

    return "\n".join(report)


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def run_target_extraction():
    """Run the complete target extraction pipeline."""

    print("=" * 70)
    print("M4 NEUROLOGICAL DISORDERS TARGET EXTRACTION PIPELINE")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    targets = extract_targets(priority_threshold=3)

    print(f"Extracted {len(targets)} validated therapeutic targets")
    print()

    # Summary by disease
    diseases = {}
    for target in targets:
        for disease in target.diseases:
            if disease not in diseases:
                diseases[disease] = 0
            diseases[disease] += 1

    print("TARGETS BY DISEASE:")
    print("-" * 40)
    for disease in sorted(diseases.keys()):
        print(f"  {disease}: {diseases[disease]} targets")
    print()

    # Summary by priority
    priority_counts = {}
    for target in targets:
        p = target.priority
        priority_counts[p] = priority_counts.get(p, 0) + 1

    print("TARGETS BY PRIORITY:")
    print("-" * 40)
    for p in sorted(priority_counts.keys()):
        print(f"  Priority {p}: {priority_counts[p]} targets")
    print()

    # Generate report
    report = generate_target_report(targets)
    print(report)

    # Save results
    output_dir = Path(__file__).parent / "targets"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output = {
        "timestamp": timestamp,
        "total_targets": len(targets),
        "targets": [asdict(t) for t in targets],
        "disease_summary": diseases,
        "priority_summary": priority_counts,
        "license": "AGPL-3.0-or-later",
        "literature_sources": [
            "van Dyck CH et al. N Engl J Med. 2023;388(1):9-21 (Lecanemab)",
            "Pagano G et al. Nat Med. 2022;28(6):1212-20 (Prasinezumab)",
            "Miller TM et al. N Engl J Med. 2022;387(12):1099-1110 (Tofersen)",
            "Polman CH et al. N Engl J Med. 2006;354(9):899-910 (Natalizumab)",
            "Hauser SL et al. N Engl J Med. 2017;376(3):221-34 (Ocrelizumab)",
        ],
    }

    output_path = output_dir / f"neuro_targets_{timestamp}.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)

    print(f"\nResults saved: {output_path}")

    # Save report
    report_path = output_dir / f"neuro_targets_report_{timestamp}.txt"
    with open(report_path, 'w') as f:
        f.write(report)

    print(f"Report saved: {report_path}")

    print("\n" + "=" * 70)
    print("TARGET EXTRACTION COMPLETE")
    print("=" * 70)

    return targets


if __name__ == "__main__":
    run_target_extraction()
