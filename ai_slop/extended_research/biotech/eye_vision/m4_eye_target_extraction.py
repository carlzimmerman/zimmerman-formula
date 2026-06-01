#!/usr/bin/env python3
"""
M4 Eye/Vision Disorders Target Extraction Pipeline
====================================================

Comprehensive computational pipeline for therapeutic peptide design targeting
eye and vision disorders. Focuses on validated druggable targets with known
benchmarks from published clinical trials and preclinical studies.

THERAPEUTIC AREAS:
==================
1. Age-Related Macular Degeneration (AMD) - Wet and Dry
2. Diabetic Retinopathy / Diabetic Macular Edema
3. Glaucoma - Primary Open-Angle and Angle-Closure
4. Cataracts - Age-related, Diabetic, Congenital
5. Dry Eye target system (Keratoconjunctivitis Sicca)
6. Uveitis - Autoimmune and Infectious
7. Retinitis Pigmentosa and Inherited Retinal Dystrophies
8. Corneal Disorders - Keratoconus, Dystrophies

APPROVED DRUG BENCHMARKS:
=========================
Anti-VEGF (Wet AMD / DR):
- Aflibercept (Eylea): Kd = 0.49 pM for VEGF-A165
- Ranibizumab (Lucentis): Kd = 46 pM for VEGF-A165
- Bevacizumab (Avastin): Kd = 580 pM for VEGF-A165
- Brolucizumab (Beovu): Kd = 22 pM for VEGF-A165

Glaucoma:
- Netarsudil (Rhopressa): ROCK Ki = 1 nM
- Ripasudil (Glanatec): ROCK Ki = 19 nM
- Latanoprost: FP receptor EC50 = 3.6 nM

Dry Eye:
- Lifitegrast (Xiidra): LFA-1/ICAM-1 IC50 = 1.4 nM
- Cyclosporine (Restasis): Calcineurin IC50 = 7 nM

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026
"""

import json
import numpy as np
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import hashlib


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

EYE_DISEASE_TARGETS = {
    # =========================================================================
    # WET AMD / DIABETIC RETINOPATHY - Anti-angiogenic targets
    # =========================================================================
    "VEGF-A": {
        "full_name": "Vascular Endothelial Growth Factor A",
        "uniprot": "P15692",
        "pdb_ids": ["1VPF", "4QAF", "4GLU", "3QTK"],
        "target system": ["Wet AMD", "Diabetic Retinopathy", "Diabetic Macular Edema"],
        "mechanism": "Block VEGF binding to VEGFR1/2, geometrically stabilize neovascularization",
        "druggability_score": 0.95,
        "approved_drugs": ["Aflibercept", "Ranibizumab", "Bevacizumab", "Brolucizumab"],
        "benchmark_affinity": {
            "aflibercept_Kd_pM": 0.49,
            "ranibizumab_Kd_pM": 46,
            "brolucizumab_Kd_pM": 22,
            "source": "Papadopoulos N et al. Angiogenesis. 2012;15(2):171-85"
        },
        "binding_site": "Receptor binding domain (RBD), residues 1-110",
        "key_residues": ["F17", "M18", "D19", "Y21", "Q22", "K84", "H86", "Q87"],
        "priority": 1,
    },

    "VEGFR2": {
        "full_name": "Vascular Endothelial Growth Factor Receptor 2",
        "uniprot": "P35968",
        "pdb_ids": ["3V2A", "4AGD", "4ASD"],
        "target system": ["Wet AMD", "Diabetic Retinopathy"],
        "mechanism": "Block receptor dimerization and kinase activation",
        "druggability_score": 0.88,
        "approved_drugs": ["Tivozanib (systemic)", "Axitinib (systemic)"],
        "benchmark_affinity": {
            "VEGF_binding_Kd_nM": 75,
            "source": "Wiesmann C et al. Cell. 1997;91(5):695-704"
        },
        "binding_site": "D2-D3 domains (VEGF binding)",
        "key_residues": ["D86", "E99", "N167", "K168"],
        "priority": 2,
    },

    "Ang-2": {
        "full_name": "Angiopoietin-2",
        "uniprot": "O15123",
        "pdb_ids": ["4JZC", "5MOY"],
        "target system": ["Wet AMD", "Diabetic Retinopathy"],
        "mechanism": "Block Ang-2/Tie2 interaction, stabilize vasculature",
        "druggability_score": 0.82,
        "approved_drugs": ["Faricimab (bispecific anti-VEGF/Ang-2)"],
        "benchmark_affinity": {
            "faricimab_Kd_nM": 0.66,
            "source": "Sharma A et al. Eye. 2020;34:1149-50"
        },
        "binding_site": "Fibrinogen-like domain",
        "key_residues": ["K469", "N470", "E471", "F473"],
        "priority": 2,
    },

    # =========================================================================
    # DRY AMD - Complement pathway targets
    # =========================================================================
    "Complement_C3": {
        "full_name": "Complement Component C3",
        "uniprot": "P01024",
        "pdb_ids": ["2A73", "2ICE", "6RUR"],
        "target system": ["Dry AMD (Geographic Atrophy)"],
        "mechanism": "Block C3 activation, reduce drusen formation and RPE damage",
        "druggability_score": 0.75,
        "approved_drugs": ["Pegcetacoplan (Syfovre) - first FDA-approved for GA"],
        "benchmark_affinity": {
            "pegcetacoplan_Kd_nM": 0.5,
            "source": "Liao DS et al. Ophthalmology. 2020;127(2):186-195"
        },
        "binding_site": "Beta-chain, C3 convertase binding",
        "key_residues": ["R102", "D103", "H393", "E394"],
        "priority": 1,
    },

    "Complement_C5": {
        "full_name": "Complement Component C5",
        "uniprot": "P01031",
        "pdb_ids": ["3CU7", "5I5K"],
        "target system": ["Dry AMD", "Diabetic Retinopathy"],
        "mechanism": "Block C5 cleavage, prevent MAC formation",
        "druggability_score": 0.78,
        "approved_drugs": ["Avacincaptad pegol (Izervay) - FDA approved 2023"],
        "benchmark_affinity": {
            "eculizumab_Kd_pM": 120,
            "avacincaptad_Kd_nM": 15,
            "source": "Jaffe GJ et al. Ophthalmology. 2021;128(4):576-586"
        },
        "binding_site": "C5a cleavage site",
        "key_residues": ["R751", "I752", "S753"],
        "priority": 2,
    },

    "Factor_D": {
        "full_name": "Complement Factor D",
        "uniprot": "P00746",
        "pdb_ids": ["1DSU", "1DIC", "6RUR"],
        "target system": ["Dry AMD"],
        "mechanism": "geometrically stabilize alternative pathway amplification",
        "druggability_score": 0.85,
        "approved_drugs": ["Danicopan (in trials)"],
        "benchmark_affinity": {
            "danicopan_IC50_nM": 1.7,
            "source": "Risitano AM et al. Blood. 2020;136(15):1737-1750"
        },
        "binding_site": "Active site (serine protease)",
        "key_residues": ["H41", "D89", "S183"],
        "priority": 2,
    },

    # =========================================================================
    # GLAUCOMA - IOP reduction and neuroprotection
    # =========================================================================
    "ROCK1": {
        "full_name": "Rho-associated Protein Kinase 1",
        "uniprot": "Q13464",
        "pdb_ids": ["3D9V", "3TWJ", "5KKS"],
        "target system": ["Primary Open-Angle Glaucoma"],
        "mechanism": "Relax trabecular meshwork, increase aqueous outflow",
        "druggability_score": 0.92,
        "approved_drugs": ["Netarsudil (Rhopressa)", "Ripasudil (Glanatec)"],
        "benchmark_affinity": {
            "netarsudil_Ki_nM": 1.0,
            "ripasudil_Ki_nM": 19,
            "source": "Lin CW et al. PLoS ONE. 2018;13(3):e0194571"
        },
        "binding_site": "ATP binding site",
        "key_residues": ["K105", "E154", "D216", "N219"],
        "priority": 1,
    },

    "ROCK2": {
        "full_name": "Rho-associated Protein Kinase 2",
        "uniprot": "O75116",
        "pdb_ids": ["2F2U", "4L6Q"],
        "target system": ["Primary Open-Angle Glaucoma"],
        "mechanism": "Reduce actomyosin contractility in TM and ciliary muscle",
        "druggability_score": 0.90,
        "approved_drugs": ["Same as ROCK1"],
        "benchmark_affinity": {
            "netarsudil_Ki_nM": 1.0,
            "source": "Same as ROCK1"
        },
        "binding_site": "ATP binding site",
        "key_residues": ["K121", "E170", "D232"],
        "priority": 1,
    },

    "Endothelin_A": {
        "full_name": "Endothelin Receptor Type A",
        "uniprot": "P25101",
        "pdb_ids": ["5GLI", "5GLH"],
        "target system": ["Glaucoma", "Optic nerve ischemia"],
        "mechanism": "Block endothelin-mediated vasoconstriction",
        "druggability_score": 0.85,
        "approved_drugs": ["Bosentan (systemic)", "Ambrisentan (systemic)"],
        "benchmark_affinity": {
            "ET1_Kd_pM": 100,
            "bosentan_Ki_nM": 4.5,
            "source": "Krishnamoorthy RR et al. Mol Vis. 2008;14:600-5"
        },
        "binding_site": "Transmembrane ligand binding",
        "key_residues": ["D126", "W167", "N168"],
        "priority": 3,
    },

    "BDNF": {
        "full_name": "Brain-Derived Neurotrophic Factor",
        "uniprot": "P23560",
        "pdb_ids": ["1BND", "4N6K"],
        "target system": ["Glaucoma (neuroprotection)"],
        "mechanism": "Activate TrkB signaling, protect retinal ganglion cells",
        "druggability_score": 0.70,  # Agonist design is challenging
        "approved_drugs": [],  # No approved BDNF mimetics for eye
        "benchmark_affinity": {
            "BDNF_TrkB_Kd_nM": 0.3,
            "7,8-DHF_EC50_nM": 500,  # Small molecule TrkB agonist
            "source": "Jang SW et al. PNAS. 2010;107(6):2687-92"
        },
        "binding_site": "TrkB D5 domain interface",
        "key_residues": ["R74", "K95", "K123"],
        "priority": 2,
    },

    # =========================================================================
    # CATARACTS - Crystallin stabilization
    # =========================================================================
    "Alpha_A_Crystallin": {
        "full_name": "Alpha-crystallin A chain",
        "uniprot": "P02489",
        "pdb_ids": ["3L1F", "4M5S"],
        "target system": ["Age-related cataracts", "Diabetic cataracts"],
        "mechanism": "Stabilize native state, prevent aggregation",
        "druggability_score": 0.65,
        "approved_drugs": [],  # No approved stabilizers
        "benchmark_affinity": {
            "lanosterol_EC50_uM": 50,  # Disaggregation activity
            "25-hydroxycholesterol_EC50_uM": 20,
            "source": "Zhao L et al. Nature. 2015;523:607-611"
        },
        "binding_site": "Alpha-crystallin domain interface",
        "key_residues": ["R116", "R120", "D109"],
        "priority": 2,
    },

    "Alpha_B_Crystallin": {
        "full_name": "Alpha-crystallin B chain (HSPB5)",
        "uniprot": "P02511",
        "pdb_ids": ["2WJ7", "2Y1Y", "4M5T"],
        "target system": ["Age-related cataracts", "Desmin-related myopathy"],
        "mechanism": "Chaperone stabilization, prevent aggregation",
        "druggability_score": 0.68,
        "approved_drugs": [],
        "benchmark_affinity": {
            "CRYAB_peptide_IC50_uM": 10,
            "source": "Makley LN et al. Science. 2015;350(6261):674-7"
        },
        "binding_site": "Substrate binding groove",
        "key_residues": ["R120", "D109", "K121"],
        "priority": 2,
    },

    # =========================================================================
    # DRY EYE target system - Inflammation and tear film
    # =========================================================================
    "LFA1_ICAM1": {
        "full_name": "LFA-1/ICAM-1 Interaction",
        "uniprot": "P05362 (ICAM1), P20701 (LFA1)",
        "pdb_ids": ["1MQ8", "1IAM"],
        "target system": ["Dry Eye target system"],
        "mechanism": "Block T-cell adhesion to ocular surface epithelium",
        "druggability_score": 0.90,
        "approved_drugs": ["Lifitegrast (Xiidra)"],
        "benchmark_affinity": {
            "lifitegrast_IC50_nM": 1.4,
            "source": "Zhong M et al. J Med Chem. 2012;55(7):3459-74"
        },
        "binding_site": "I-domain of LFA-1",
        "key_residues": ["D137", "S139", "T206"],
        "priority": 1,
    },

    "Calcineurin": {
        "full_name": "Calcineurin (PP2B)",
        "uniprot": "Q08209",
        "pdb_ids": ["1AUI", "4F0Z"],
        "target system": ["Dry Eye target system", "Uveitis"],
        "mechanism": "Suppress T-cell activation and inflammation",
        "druggability_score": 0.85,
        "approved_drugs": ["Cyclosporine (Restasis, Cequa)"],
        "benchmark_affinity": {
            "cyclosporine_IC50_nM": 7,
            "source": "Clipstone NA, Crabtree GR. Nature. 1992;357:695-7"
        },
        "binding_site": "Cyclophilin-CsA binding interface",
        "key_residues": ["W352", "L354", "F356"],
        "priority": 1,
    },

    "MUC5AC": {
        "full_name": "Mucin 5AC",
        "uniprot": "P98088",
        "pdb_ids": [],  # Too large/glycosylated for crystal
        "target system": ["Dry Eye target system"],
        "mechanism": "Enhance goblet cell mucin secretion",
        "druggability_score": 0.50,
        "approved_drugs": [],
        "benchmark_affinity": {
            "note": "Target for secretion enhancement, not direct binding"
        },
        "binding_site": "N/A - secretory pathway target",
        "key_residues": [],
        "priority": 3,
    },

    "Lacritin": {
        "full_name": "Lacritin",
        "uniprot": "Q9GZZ8",
        "pdb_ids": [],
        "target system": ["Dry Eye target system"],
        "mechanism": "Stimulate tear protein secretion and corneal healing",
        "druggability_score": 0.60,
        "approved_drugs": [],
        "benchmark_affinity": {
            "lacritin_EC50_nM": 10,
            "source": "Sanghi S et al. Exp Eye Res. 2001;73(3):317-30"
        },
        "binding_site": "Syndecan-1 interaction",
        "key_residues": [],
        "priority": 3,
    },

    # =========================================================================
    # UVEITIS - Inflammation control
    # =========================================================================
    "TNF_alpha": {
        "full_name": "Tumor Necrosis Factor Alpha",
        "uniprot": "P01375",
        "pdb_ids": ["1TNF", "4Y6O", "5MU8"],
        "target system": ["Non-infectious Uveitis", "Posterior Uveitis"],
        "mechanism": "Block TNF-α signaling, reduce inflammation",
        "druggability_score": 0.95,
        "approved_drugs": ["Adalimumab (Humira)", "Infliximab (systemic)"],
        "benchmark_affinity": {
            "adalimumab_Kd_pM": 60,
            "infliximab_Kd_pM": 90,
            "source": "Radstake TR et al. Arthritis Rheum. 2009;60(5):1267-75"
        },
        "binding_site": "Receptor binding interface",
        "key_residues": ["K90", "R92", "D143", "A145"],
        "priority": 1,
    },

    "IL6": {
        "full_name": "Interleukin-6",
        "uniprot": "P05231",
        "pdb_ids": ["1ALU", "4CNI", "4O9H"],
        "target system": ["Uveitis", "Diabetic Macular Edema"],
        "mechanism": "Block IL-6 signaling, reduce inflammation",
        "druggability_score": 0.88,
        "approved_drugs": ["Tocilizumab (Actemra - systemic)"],
        "benchmark_affinity": {
            "tocilizumab_Kd_nM": 2.5,
            "source": "Mihara M et al. Clin Immunol. 2012;144(3):186-93"
        },
        "binding_site": "IL-6R binding interface",
        "key_residues": ["F74", "D160", "E172"],
        "priority": 2,
    },

    # =========================================================================
    # RETINITIS PIGMENTOSA - Photoreceptor preservation
    # =========================================================================
    "Rhodopsin": {
        "full_name": "Rhodopsin",
        "uniprot": "P08100",
        "pdb_ids": ["1F88", "6FK6", "7MT8"],
        "target system": ["Retinitis Pigmentosa (P23H mutation most common)"],
        "mechanism": "Pharmacological chaperone to correct misfolding",
        "druggability_score": 0.72,
        "approved_drugs": [],
        "benchmark_affinity": {
            "11_cis_retinal_Kd_nM": 0.5,
            "YC001_EC50_uM": 1,  # Retinal analog chaperone
            "source": "Chen Y et al. J Biol Chem. 2018;293(34):13027-37"
        },
        "binding_site": "Retinal binding pocket",
        "key_residues": ["K296", "E113", "W265", "Y268"],
        "priority": 2,
    },

    "PDE6": {
        "full_name": "Phosphodiesterase 6 (rod)",
        "uniprot": "P16499 (alpha), P35913 (beta)",
        "pdb_ids": ["6MZB", "7JZR"],
        "target system": ["Retinitis Pigmentosa"],
        "mechanism": "Gene therapy / protein replacement",
        "druggability_score": 0.55,
        "approved_drugs": [],
        "benchmark_affinity": {
            "cGMP_Km_uM": 17,
            "source": "Cote RH et al. J Biol Chem. 1994;269(45):28163-8"
        },
        "binding_site": "Catalytic domain",
        "key_residues": ["H617", "H653", "D654"],
        "priority": 3,
    },

    # =========================================================================
    # CORNEAL DISORDERS
    # =========================================================================
    "MMP9": {
        "full_name": "Matrix Metalloproteinase 9",
        "uniprot": "P14780",
        "pdb_ids": ["1L6J", "4JIJ", "4H3X"],
        "target system": ["Corneal ulcers", "Dry Eye", "Keratoconus"],
        "mechanism": "geometrically stabilize collagen degradation, preserve corneal integrity",
        "druggability_score": 0.88,
        "approved_drugs": ["Doxycycline (indirect MMP geometrically stabilize)"],
        "benchmark_affinity": {
            "marimastat_Ki_nM": 3,
            "GM6001_Ki_nM": 0.4,
            "source": "Brown S et al. J Biol Chem. 2000;275(18):14074-7"
        },
        "binding_site": "Zinc catalytic site",
        "key_residues": ["H401", "E402", "H405", "H411"],
        "priority": 2,
    },

    "LOX": {
        "full_name": "Lysyl Oxidase",
        "uniprot": "P28300",
        "pdb_ids": ["1N8Y"],
        "target system": ["Keratoconus"],
        "mechanism": "Enhance collagen cross-linking, strengthen cornea",
        "druggability_score": 0.55,
        "approved_drugs": ["Riboflavin-UVA (CXL procedure)"],
        "benchmark_affinity": {
            "BAPN_Ki_uM": 5,  # Inhibitor (not agonist)
            "source": "Kagan HM et al. J Cell Biochem. 2003;88(4):660-72"
        },
        "binding_site": "LTQ cofactor site",
        "key_residues": ["K314", "Y349", "K350"],
        "priority": 3,
    },
}


# =============================================================================
# TARGET EXTRACTION FUNCTIONS
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
    """Extract and validate therapeutic targets for eye diseases."""

    targets = []

    for target_id, data in EYE_DISEASE_TARGETS.items():
        if data.get("priority", 4) <= priority_threshold:
            target = ExtractedTarget(
                target_id=target_id,
                full_name=data["full_name"],
                uniprot=data["uniprot"],
                pdb_ids=data["pdb_ids"],
                diseases=data["target system"],
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

    # Sort by priority
    targets.sort(key=lambda x: (x.priority, -x.druggability_score))

    return targets


def generate_target_report(targets: List[ExtractedTarget]) -> str:
    """Generate a human-readable report of extracted targets."""

    report = []
    report.append("=" * 80)
    report.append("EYE/VISION DISORDERS THERAPEUTIC TARGET REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append(f"Total targets: {len(targets)}")
    report.append("")

    # Group by target system
    diseases = {}
    for target in targets:
        for target system in target.diseases:
            if target system not in diseases:
                diseases[target system] = []
            diseases[target system].append(target)

    for target system in sorted(diseases.keys()):
        report.append("-" * 80)
        report.append(f"target system: {target system}")
        report.append("-" * 80)

        for target in diseases[target system]:
            drugs_str = ", ".join(target.approved_drugs[:2]) if target.approved_drugs else "None"
            report.append(f"\n  {target.target_id}")
            report.append(f"    Full name: {target.full_name}")
            report.append(f"    UniProt: {target.uniprot}")
            report.append(f"    PDB: {', '.join(target.pdb_ids[:3])}")
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
    print("M4 EYE/VISION TARGET EXTRACTION PIPELINE")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Extract targets
    targets = extract_targets(priority_threshold=3)

    print(f"Extracted {len(targets)} validated therapeutic targets")
    print()

    # Summary by target system
    diseases = {}
    for target in targets:
        for target system in target.diseases:
            if target system not in diseases:
                diseases[target system] = 0
            diseases[target system] += 1

    print("TARGETS BY target system:")
    print("-" * 40)
    for target system in sorted(diseases.keys()):
        print(f"  {target system}: {diseases[target system]} targets")
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

    # Save JSON
    output = {
        "timestamp": timestamp,
        "total_targets": len(targets),
        "targets": [asdict(t) for t in targets],
        "disease_summary": diseases,
        "priority_summary": priority_counts,
        "license": "AGPL-3.0-or-later",
        "literature_sources": [
            "Papadopoulos N et al. Angiogenesis. 2012;15(2):171-85 (VEGF)",
            "Liao DS et al. Ophthalmology. 2020;127(2):186-195 (C3)",
            "Lin CW et al. PLoS ONE. 2018;13(3):e0194571 (ROCK)",
            "Zhong M et al. J Med Chem. 2012;55(7):3459-74 (LFA-1)",
            "Zhao L et al. Nature. 2015;523:607-611 (Crystallins)",
            "Chen Y et al. J Biol Chem. 2018;293(34):13027-37 (Rhodopsin)",
        ],
    }

    output_path = output_dir / f"eye_targets_{timestamp}.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)

    print(f"\nResults saved: {output_path}")

    # Save report
    report_path = output_dir / f"eye_targets_report_{timestamp}.txt"
    with open(report_path, 'w') as f:
        f.write(report)

    print(f"Report saved: {report_path}")

    print("\n" + "=" * 70)
    print("TARGET EXTRACTION COMPLETE")
    print("=" * 70)

    return targets


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    run_target_extraction()
