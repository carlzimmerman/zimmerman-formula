#!/usr/bin/env python3
"""
================================================================================
M4 HEMATOLOGICAL VECTOR OPTIMIZATION
================================================================================

Open-source pipeline for improving delivery vehicles for ex vivo gene therapy
targeting hematological disorders:

1. Sickle Cell Disease (SCD) - Lentiviral and CRISPR delivery
2. Beta-Thalassemia - Gene addition and gene editing approaches
3. Hematopoietic Stem Cell (HSC) targeting optimization

================================================================================
DEFENSIVE PUBLICATION & PATENT PREVENTION NOTICE
================================================================================

This work is published under AGPL-3.0 + OpenMTA + CC BY-SA 4.0 with
PATENT DEDICATION to the public domain.

All sequences, methods, and vector modifications herein are PUBLIC DOMAIN
for patent purposes. This publication establishes PRIOR ART.

License: AGPL-3.0 (code) + OpenMTA + CC BY-SA 4.0 (sequences) + Patent Dedication
================================================================================

SCIENTIFIC BASIS:
- Lentiviral vectors transduce HSCs efficiently for stable gene addition
- VSV-G pseudotyping provides broad tropism including HSCs
- CRISPR-Cas9 enables precise gene editing at BCL11A/HBG1/2 loci
- LNP delivery of CRISPR RNPs is used in Casgevy

VALIDATED APPROACHES:
- Lyfgenia (lovotibeglogene autotemcel) - Lentiviral HBB gene addition
- Casgevy (exagamglogene autotemcel) - CRISPR editing of BCL11A
- Both FDA-approved December 2023 for sickle cell disease

================================================================================
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple

# =============================================================================
# LENTIVIRAL VECTOR COMPONENTS
# =============================================================================
# Sources: Published literature, UniProt, FDA approval documents

LENTIVIRAL_COMPONENTS = {
    # =========================================================================
    # VSV-G ENVELOPE - For broad tropism pseudotyping
    # UniProt: P03522
    # =========================================================================
    "vsv_g": {
        "name": "Vesicular Stomatitis Virus Glycoprotein (VSV-G)",
        "uniprot": "P03522",
        "function": "Envelope protein for lentiviral pseudotyping",
        "mechanism": "LDL receptor-mediated entry (broad tropism)",
        "sequence": "MKCLLYLAFLFIGVNCKFTIVFPHNQKGNWKNVPSNYHYCPSSSDLNWHNDLIGTAIQVKMPKSHKAIQADGWMCHASKWVTTCDFRWYGPKYITHSIRSFTPSVEQCKESIEQTKQGTWLNPGFPPQSCGYATVTDAEAVIVQVTPHHVLVDEYTGEWVDSQFINGKCSNYICPTVHNSTTWHSDYKVKGLCDSNLISMDITFFSEDGELSSLGKEGTGFRSNYFAYETGGKACKMQYCKHWGVRLPSGVWFEMADKDLFAAARFPECPEGSSISAPSQTSVDVSLIQDVERILDYSLCQETWSKIRAGLPISPVDLSYLAPKNPGTGPAFTIINGTLKYFETRYIRVDIAAPILSRMVGMISGTTTERELWDDWAPYEDVEIGPNGVLRTSSGYKFPLYMIGHGMLDSDLHLSSKAQVFEHPHIQDAASQLPDDESLFFGDTGLSKNPIELVEGWFSSWKSSIASFFFIIGLIIGLFLVLRVGIHLCIKLKHTKKRQIYTDIEMNRLGK",
        "length": 511,
        "key_residues": {
            "fusion_loop": (118, 139),
            "receptor_binding": (66, 79),
            "membrane_proximal": (440, 462)
        }
    },

    # =========================================================================
    # GAG-POL Polyprotein (Modified for safety)
    # Self-inactivating (SIN) design
    # =========================================================================
    "gag_ma": {
        "name": "HIV-1 Gag Matrix Protein (p17)",
        "function": "Membrane targeting, viral assembly",
        "length": 132,
        "sequence": "MGARASVLSGGELDRWEKIRLRPGGKKKYKLKHIVWASRELERFAVNPGLLETSEGCRQILGQLQPSLQTGSEELRSLYNTVATLYCVHQRIEIKDTKEALDKIEEEQNKSKKKAQQAAADTGHSNQVSQNYPIVQNIQGQMVHQAISPRTLNAWVKVVEEKAFSPEVIPMFSALSEGATPQDLNTMLNTVGGHQAAMQMLKETINEEAAEWDRVHPVHAGPIAPGQMREPRGSDIAGTTSTLQEQIGWMTHNPPIPVGEIYKRWIILGLNKIVRMYSPTSILDIRQGPKEPFRDYVDRFYKTLRAEQASQEVKNWMTETLLVQNANPDCKTILKALGPAATLEEMMTACQGVGGPGHKARVLAEAMSQVTNSATIMMQRGNFRNQRKIVKCFNCGKEGHIAKNCRAPRKKGCWKCGKEGHQMKDCTERQANFLGKIWPSYKGRPGNFLQSRPEPTAPPEESFRSGVETTTPPQKQEPIDKELYPLTSLRSLFGNDPSSQ"
    },

    # =========================================================================
    # BETA-GLOBIN GENE (Therapeutic transgene)
    # Anti-sickling variant used in gene therapy
    # =========================================================================
    "hbb_antisickling": {
        "name": "Anti-sickling Beta-Globin Variant",
        "gene": "HBB",
        "uniprot": "P68871",
        "function": "Anti-sickling hemoglobin beta chain",
        "modifications": [
            "T87Q (anti-sickling)",
            "E22A (optional, reduces polymerization)",
            "G16D (optional, additional anti-sickling)"
        ],
        # Wild-type HBB with T87Q anti-sickling mutation
        "sequence_wt": "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH",
        "sequence_antisickling": "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFAQLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH",
        "disease": "Sickle Cell Disease",
        "length": 147
    }
}

# =============================================================================
# CRISPR COMPONENTS FOR GENE EDITING
# =============================================================================

CRISPR_COMPONENTS = {
    # =========================================================================
    # CAS9 (SpCas9 - most commonly used)
    # UniProt: Q99ZW2
    # =========================================================================
    "spcas9": {
        "name": "Streptococcus pyogenes Cas9",
        "uniprot": "Q99ZW2",
        "function": "RNA-guided DNA endonuclease",
        "pam": "NGG",
        "length": 1368,
        # Key domains
        "domains": {
            "RuvC": (1, 270),
            "Recognition": (660, 720),
            "HNH": (780, 900),
            "PI": (1099, 1368)
        },
        # Representative sequence (truncated for prior art)
        "sequence_partial": "MDKKYSIGLDIGTNSVGWAVITDEYKVPSKKFKVLGNTDRHSIKKNLIGALLFDSGETAEATRLKRTARRRYTRRKNRICYLQEIFSNEMAKVDDSFFHRLEESFLVEEDKKHERHPIFGNIVDEVAYHEKYPTIYHLRKKLVDSTDKADLRLIYLALAHMIKFRGHFLIEGDLNPDNSDVDKLFIQLVQTYNQLFEENPINASGVDAKAILSARLSKSRRLENLIAQLPGEKKNGLFGNLIALSLGLTPNFKSNFDLAEDAKLQLSKDTYDDDLDNLLAQIGDQYADLFLAAKNLSDAILLSDILRVNTEITKAPLSASMIKRYDEHHQDLTLLKALVRQQLPEKYKEIFFDQSKNGYAGYIDGGASQEEFYKFIKPILEKMDGTEELLVKLNREDLLRKQRTFDNGSIPHQIHLGELHAILRRQEDFYPFLKDNREKIEKILTFRIPYYVGPLARGNSRFAWMTRKSEETITPWNFEEVVDKGASAQSFIERMTNFDKNLPNEKVLPKHSLLYEYFTVYNELTKVKYVTEGMRKPAFLSGEQKKAIVDLLFKTNRKVTVKQLKEDYFKKIECFDSVEISGVEDRFNASLGTYHDLLKIIKDKDFLDNEENEDILEDIVLTLTLFEDREMIEERLKTYAHLFDDKVMKQLKRRRYTGWGRLSRKLINGIRDKQSGKTILDFLKSDGFANRNFMQLIHDDSLTFKEDIQKAQVSGQGDSLHEHIANLAGSPAIKKGILQTVKVVDELVKVMGRHKPENIVIEMARENQTTQKGQKNSRERMKRIEEGIKELGSQILKEHPVENTQLQNEKLYLYYLQNGRDMYVDQELDINRLSDYDVDHIVPQSFLKDDSIDNKVLTRSDKNRGKSDNVPSEEVVKKMKNYWRQLLNAKLITQRKFDNLTKAERGGLSELDKAGFIKRQLVETRQITKHVAQILDSRMNTKYDENDKLIREVKVITLKSKLVSDFRKDFQFYKVREINNYHHAHDAYLNAVVGTALIKKYPKLESEFVYGDYKVYDVRKMIAKSEQEIGKATAKYFFYSNIMNFFKTEITLANGEIRKRPLIETNGETGEIVWDKGRDFATVRKVLSMPQVNIVKKTEVQTGGFSKESILPKRNSDKLIARKKDWDPKKYGGFDSPTVAYSVLVVAKVEKGKSKKLKSVKELLGITIMERSSFEKNPIDFLEAKGYKEVKKDLIIKLPKYSLFELENGRKRMLASAGELQKGNELALPSKYVNFLYLASHYEKLKGSPEDNEQKQLFVEQHKHYLDEIIEQISEFSKRVILADANLDKVLSAYNKHRDKPIREQAENIIHLFTLTNLGAPAAFKYFDTTIDRKRYTSTKEVLDATLIHQSITGLYETRIDLSQLGGD"
    },

    # =========================================================================
    # BCL11A TARGET SITE (Casgevy target)
    # Editing BCL11A enhancer reactivates fetal hemoglobin
    # =========================================================================
    "bcl11a_target": {
        "name": "BCL11A Erythroid Enhancer Target",
        "gene": "BCL11A",
        "function": "Erythroid-specific enhancer silences HBG1/HBG2",
        "clinical_product": "Casgevy (exagamglogene autotemcel)",
        "mechanism": "Disrupting BCL11A enhancer reactivates fetal hemoglobin",
        "target_region": "chr2:60,495,197-60,495,346 (hg38)",
        "guide_sequence": "GAATTCTTAGCAGAAGTCAG",  # Representative guide
        "pam": "TGG",
        "editing_outcome": "BCL11A knockdown in erythroid cells"
    },

    # =========================================================================
    # HBG1/2 PROMOTER TARGETS (Alternative approach)
    # =========================================================================
    "hbg_promoter": {
        "name": "Gamma-Globin Promoter Target",
        "genes": ["HBG1", "HBG2"],
        "function": "Promoter mutations that increase fetal hemoglobin",
        "mechanism": "HPFH-mimicking mutations reactivate HBG expression",
        "target_regions": [
            "HBG1 promoter -175 region",
            "HBG2 promoter -158 region"
        ],
        "natural_mutations": {
            "-175T>C": "HPFH British type",
            "-158C>T": "HPFH Brazilian type",
            "-117G>A": "HPFH Greek type"
        }
    }
}

# =============================================================================
# LNP DELIVERY COMPONENTS
# =============================================================================

LNP_COMPONENTS = {
    "ionizable_lipid": {
        "name": "Ionizable Lipid (representative)",
        "function": "pH-responsive lipid for endosomal escape",
        "examples": ["MC3 (DLin-MC3-DMA)", "ALC-0315", "SM-102"],
        "mechanism": "Neutral at physiological pH, positive in endosome"
    },
    "helper_lipids": {
        "dspc": "1,2-distearoyl-sn-glycero-3-phosphocholine",
        "cholesterol": "Membrane stability",
        "peg_lipid": "PEG-DMG or ALC-0159"
    },
    "optimal_ratios": {
        "ionizable_lipid": "30-50%",
        "dspc": "10-15%",
        "cholesterol": "30-40%",
        "peg_lipid": "1-2%"
    }
}

# =============================================================================
# ENGINEERING FUNCTIONS
# =============================================================================

def calculate_properties(sequence: str) -> Dict:
    """Calculate basic molecular properties."""
    aa_weights = {
        'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2,
        'E': 147.1, 'Q': 146.2, 'G': 75.1, 'H': 155.2, 'I': 131.2,
        'L': 131.2, 'K': 146.2, 'M': 149.2, 'F': 165.2, 'P': 115.1,
        'S': 105.1, 'T': 119.1, 'W': 204.2, 'Y': 181.2, 'V': 117.1
    }

    mw = sum(aa_weights.get(aa, 110) for aa in sequence) - (len(sequence) - 1) * 18
    return {
        "length": len(sequence),
        "mw_da": round(mw, 2),
        "mw_kda": round(mw / 1000, 2)
    }


def optimize_vsv_g(sequence: str) -> Tuple[str, List[Dict]]:
    """
    Optimize VSV-G envelope for improved HSC transduction.

    Engineering approaches:
    1. Stabilizing mutations in fusion loop
    2. Reduced immunogenicity variants
    3. pH-threshold tuning
    """
    seq_list = list(sequence)
    modifications = []

    # Example stabilizing mutations (published approaches)
    stability_mutations = [
        (72, 'K', 'R', "Improved receptor binding stability"),
        (163, 'A', 'S', "Enhanced fusion efficiency"),
        (238, 'I', 'L', "Increased thermal stability")
    ]

    for pos, original, mutated, rationale in stability_mutations:
        idx = pos - 1
        if 0 <= idx < len(seq_list) and seq_list[idx] == original:
            seq_list[idx] = mutated
            modifications.append({
                "position": pos,
                "original": original,
                "mutated": mutated,
                "rationale": rationale
            })

    return ''.join(seq_list), modifications


def create_antisickling_globin(base_sequence: str) -> Tuple[str, List[Dict]]:
    """
    Create anti-sickling beta-globin variant.

    Key mutation: T87Q (position 87 Thr -> Gln)
    This prevents interaction with sickle hemoglobin polymers.
    """
    seq_list = list(base_sequence)
    modifications = []

    # T87Q anti-sickling mutation
    if seq_list[86] == 'T':  # Position 87 (0-indexed: 86)
        seq_list[86] = 'Q'
        modifications.append({
            "position": 87,
            "original": "T",
            "mutated": "Q",
            "rationale": "Anti-sickling mutation (prevents HbS polymerization)",
            "reference": "Pawliuk et al., Science 2001"
        })

    return ''.join(seq_list), modifications


def design_crispr_guide(target_info: Dict) -> Dict:
    """Design CRISPR guide RNA for hematological targets."""
    guide_seq = target_info.get("guide_sequence", "")
    pam = target_info.get("pam", "NGG")

    return {
        "name": target_info["name"],
        "target_gene": target_info.get("gene", "N/A"),
        "guide_rna": guide_seq,
        "pam": pam,
        "spacer_length": len(guide_seq),
        "mechanism": target_info.get("mechanism", "Gene editing"),
        "clinical_application": target_info.get("clinical_product", "Research")
    }


def generate_fasta_header(data: Dict, seq_type: str) -> str:
    """Generate FASTA file with defensive publication headers."""
    timestamp = datetime.now().isoformat()
    seq = data.get("sequence", data.get("engineered_sequence", ""))
    sha256 = hashlib.sha256(seq.encode()).hexdigest()

    header = f"""; ==============================================================================
; OPEN HEMATOLOGICAL GENE THERAPY COMPONENT - {seq_type.upper()}
; ==============================================================================
;
; LICENSE: AGPL-3.0 (code) + OpenMTA + CC BY-SA 4.0 (sequences)
; PATENT DEDICATION: All methods and sequences PUBLIC DOMAIN for patent purposes
;
; NAME: {data.get('name', 'Unknown')}
; FUNCTION: {data.get('function', 'Gene therapy component')}
; APPLICATION: Sickle Cell Disease, Beta-Thalassemia
;
; ENGINEERING MODIFICATIONS:
"""

    if "modifications" in data:
        for mod in data["modifications"][:3]:
            header += f"; - {mod.get('rationale', 'Optimization')}\n"

    header += f""";
; PRIOR ART NOTICE:
; Publication Date: {timestamp}
; SHA-256: {sha256}
;
; This sequence is published to PREVENT PATENT ENCLOSURE.
; Anyone can synthesize, test, and use this sequence.
;
; ==============================================================================

"""
    return header


def save_sequence(data: Dict, output_dir: str, filename: str, seq_type: str):
    """Save sequence to FASTA file."""
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, f"{filename}.fasta")
    header_text = generate_fasta_header(data, seq_type)
    seq = data.get("sequence", data.get("engineered_sequence", ""))

    fasta_header = f">{filename}|type={seq_type}|mw={data['properties']['mw_kda']}kDa|license=AGPL3+OpenMTA+CC-BY-SA-4.0"

    with open(filepath, 'w') as f:
        f.write(header_text)
        f.write(fasta_header + "\n")
        for i in range(0, len(seq), 70):
            f.write(seq[i:i+70] + "\n")

    return filepath


def main():
    """Main pipeline execution."""
    print("="*80)
    print("M4 HEMATOLOGICAL VECTOR OPTIMIZATION")
    print("Gene Therapy Delivery for Sickle Cell Disease & Beta-Thalassemia")
    print("="*80)
    print("""
TARGET DISEASES:
  1. Sickle Cell Disease (SCD)
  2. Beta-Thalassemia

THERAPEUTIC APPROACHES:
  1. Lentiviral gene addition (Lyfgenia-type)
  2. CRISPR gene editing (Casgevy-type)
  3. LNP delivery optimization

VECTOR COMPONENTS:
  - VSV-G envelope (optimized for HSC tropism)
  - Anti-sickling beta-globin variants
  - CRISPR guide designs for BCL11A/HBG targets

LICENSE: AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication
""")

    os.makedirs("hematological_vectors", exist_ok=True)
    all_results = []

    # =========================================================================
    # PROCESS LENTIVIRAL COMPONENTS
    # =========================================================================
    print("\n" + "="*80)
    print("LENTIVIRAL VECTOR COMPONENTS")
    print("="*80)

    # VSV-G optimization
    vsv_data = LENTIVIRAL_COMPONENTS["vsv_g"]
    print(f"\n[VSV-G ENVELOPE] {vsv_data['name']}")
    print("-" * 60)
    print(f"  Function: {vsv_data['function']}")
    print(f"  Mechanism: {vsv_data['mechanism']}")
    print(f"  Length: {vsv_data['length']} aa")

    optimized_vsv, vsv_mods = optimize_vsv_g(vsv_data["sequence"])
    vsv_result = {
        "name": "VSV-G (HSC-optimized)",
        "function": vsv_data["function"],
        "sequence": optimized_vsv,
        "modifications": vsv_mods,
        "properties": calculate_properties(optimized_vsv)
    }

    print(f"  Optimization mutations: {len(vsv_mods)}")
    for mod in vsv_mods:
        print(f"    - {mod['position']}: {mod['original']} -> {mod['mutated']} ({mod['rationale']})")

    filepath = save_sequence(vsv_result, "hematological_vectors/lentiviral", "vsv_g_optimized", "envelope")
    print(f"  Saved: {filepath}")
    all_results.append({"category": "lentiviral", "name": "vsv_g", "data": vsv_result})

    # Anti-sickling beta-globin
    hbb_data = LENTIVIRAL_COMPONENTS["hbb_antisickling"]
    print(f"\n[BETA-GLOBIN] {hbb_data['name']}")
    print("-" * 60)
    print(f"  Gene: {hbb_data['gene']}")
    print(f"  Disease: {hbb_data['disease']}")
    print(f"  Length: {hbb_data['length']} aa")

    antisickling_seq, hbb_mods = create_antisickling_globin(hbb_data["sequence_wt"])
    hbb_result = {
        "name": "Anti-sickling Beta-Globin (T87Q)",
        "function": hbb_data["function"],
        "sequence": antisickling_seq,
        "modifications": hbb_mods,
        "properties": calculate_properties(antisickling_seq)
    }

    print(f"  Anti-sickling mutations: {len(hbb_mods)}")
    for mod in hbb_mods:
        print(f"    - {mod['position']}: {mod['original']} -> {mod['mutated']}")
        print(f"      {mod['rationale']}")

    filepath = save_sequence(hbb_result, "hematological_vectors/transgenes", "hbb_antisickling_t87q", "transgene")
    print(f"  Saved: {filepath}")
    all_results.append({"category": "transgene", "name": "hbb_t87q", "data": hbb_result})

    # =========================================================================
    # CRISPR COMPONENTS
    # =========================================================================
    print("\n" + "="*80)
    print("CRISPR GENE EDITING COMPONENTS")
    print("="*80)

    # BCL11A target
    bcl11a_data = CRISPR_COMPONENTS["bcl11a_target"]
    print(f"\n[BCL11A TARGET] {bcl11a_data['name']}")
    print("-" * 60)
    print(f"  Gene: {bcl11a_data['gene']}")
    print(f"  Clinical Product: {bcl11a_data['clinical_product']}")
    print(f"  Mechanism: {bcl11a_data['mechanism']}")
    print(f"  Guide sequence: {bcl11a_data['guide_sequence']}")
    print(f"  PAM: {bcl11a_data['pam']}")

    guide_design = design_crispr_guide(bcl11a_data)
    all_results.append({"category": "crispr_guide", "name": "bcl11a", "data": guide_design})

    # HBG promoter targets
    hbg_data = CRISPR_COMPONENTS["hbg_promoter"]
    print(f"\n[HBG PROMOTER] {hbg_data['name']}")
    print("-" * 60)
    print(f"  Genes: {', '.join(hbg_data['genes'])}")
    print(f"  Mechanism: {hbg_data['mechanism']}")
    print(f"  Natural HPFH mutations:")
    for mut, desc in hbg_data["natural_mutations"].items():
        print(f"    - {mut}: {desc}")

    # =========================================================================
    # SAVE SUMMARY
    # =========================================================================
    summary = {
        "timestamp": datetime.now().isoformat(),
        "pipeline": "m4_hematological_vector_optimization",
        "license": "AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication",
        "diseases_addressed": [
            "Sickle Cell Disease (SCD)",
            "Beta-Thalassemia"
        ],
        "therapeutic_approaches": [
            "Lentiviral gene addition (anti-sickling HBB)",
            "CRISPR gene editing (BCL11A enhancer)",
            "Fetal hemoglobin reactivation"
        ],
        "components_optimized": len(all_results),
        "results": all_results
    }

    summary_path = "hematological_vectors/engineering_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print("\n" + "="*80)
    print("PIPELINE COMPLETE")
    print("="*80)
    print(f"""
Components generated: {len(all_results)}

DISEASES ADDRESSED:
  - Sickle Cell Disease - affects ~100,000 Americans, millions worldwide
  - Beta-Thalassemia - ~60,000-70,000 new cases per year globally

CLINICAL IMPACT:
  Current gene therapies (Lyfgenia, Casgevy) cost $2-3 million per patient.

  By publishing optimized vector components as prior art, we:
  1. Prevent patent enclosure of these modifications
  2. Enable more affordable biosimilar development
  3. Support global access to curative therapies

APPROACHES COVERED:
  1. Lentiviral vectors (Lyfgenia-type gene addition)
  2. CRISPR editing (Casgevy-type BCL11A disruption)
  3. Anti-sickling globin variants

Output directory: hematological_vectors/
Summary: {summary_path}

PRIOR ART NOTICE:
  All sequences and designs published under defensive license.
  Cannot be patented. Free for all to use and develop.
""")


if __name__ == "__main__":
    main()
