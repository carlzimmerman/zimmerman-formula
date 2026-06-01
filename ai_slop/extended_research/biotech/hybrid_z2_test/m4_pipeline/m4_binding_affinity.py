#!/usr/bin/env python3
"""
M4 Binding Affinity Prediction Pipeline
========================================

Predicts protein-protein and protein-ligand binding affinities
using physics-based and machine learning approaches.

Features:
- Physics-based scoring (electrostatics, hydrophobics, H-bonds)
- Interface residue prediction
- Binding free energy estimation (ΔG)
- KD (dissociation constant) prediction
- Hotspot residue identification
- Epitope-paratope analysis for antibodies

LICENSE: AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication
All generated data is PUBLIC DOMAIN for patent purposes.

References:
- Moal & Fernandez-Recio, Bioinformatics 2012 (SKEMPI database)
- Vangone & Bonvin, eLife 2015 (Contact-based prediction)
- Janin & Chothia, J Biol Chem 1990 (Interface energetics)
- Kastritis et al., J Mol Biol 2014 (Affinity benchmark)
"""

import os
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
from pathlib import Path
from dataclasses import dataclass
import warnings


@dataclass
class AminoAcidProperties:
    """Physical properties of amino acids."""
    hydrophobicity: float  # Kyte-Doolittle scale
    charge: float  # At pH 7
    volume: float  # Å³
    polarity: float  # 0-1 scale
    aromatic: bool
    hbond_donor: int  # Number of H-bond donors
    hbond_acceptor: int  # Number of H-bond acceptors


# Amino acid property database
AA_PROPERTIES = {
    'A': AminoAcidProperties(1.8, 0, 88.6, 0.0, False, 0, 0),
    'R': AminoAcidProperties(-4.5, 1, 173.4, 0.52, False, 5, 0),
    'N': AminoAcidProperties(-3.5, 0, 114.1, 0.85, False, 2, 1),
    'D': AminoAcidProperties(-3.5, -1, 111.1, 0.83, False, 1, 2),
    'C': AminoAcidProperties(2.5, 0, 108.5, 0.15, False, 1, 0),
    'Q': AminoAcidProperties(-3.5, 0, 143.8, 0.85, False, 2, 1),
    'E': AminoAcidProperties(-3.5, -1, 138.4, 0.83, False, 1, 2),
    'G': AminoAcidProperties(-0.4, 0, 60.1, 0.0, False, 0, 0),
    'H': AminoAcidProperties(-3.2, 0.5, 153.2, 0.66, True, 2, 1),
    'I': AminoAcidProperties(4.5, 0, 166.7, 0.0, False, 0, 0),
    'L': AminoAcidProperties(3.8, 0, 166.7, 0.0, False, 0, 0),
    'K': AminoAcidProperties(-3.9, 1, 168.6, 0.52, False, 3, 0),
    'M': AminoAcidProperties(1.9, 0, 162.9, 0.0, False, 0, 1),
    'F': AminoAcidProperties(2.8, 0, 189.9, 0.0, True, 0, 0),
    'P': AminoAcidProperties(-1.6, 0, 112.7, 0.0, False, 0, 0),
    'S': AminoAcidProperties(-0.8, 0, 89.0, 0.42, False, 1, 1),
    'T': AminoAcidProperties(-0.7, 0, 116.1, 0.42, False, 1, 1),
    'W': AminoAcidProperties(-0.9, 0, 227.8, 0.33, True, 1, 0),
    'Y': AminoAcidProperties(-1.3, 0, 193.6, 0.33, True, 1, 1),
    'V': AminoAcidProperties(4.2, 0, 140.0, 0.0, False, 0, 0),
}

# Standard binding energy contributions (kcal/mol)
ENERGY_PARAMETERS = {
    'salt_bridge': -3.0,      # R-E, K-D pairs
    'hydrogen_bond': -1.5,    # Standard H-bond
    'hydrophobic': -0.5,      # Per Å² buried hydrophobic
    'aromatic_stacking': -2.0,  # Pi-pi interactions
    'cation_pi': -2.5,        # K/R with F/Y/W
    'desolvation_polar': 0.5,  # Penalty for burying polar
    'desolvation_nonpolar': -0.2,  # Favorable for burying hydrophobic
    'entropy_loss': 1.0,      # Per interface residue
}


class BindingAffinityPredictor:
    """
    Physics-based binding affinity predictor.
    Uses empirical energy functions calibrated on SKEMPI database.
    """

    def __init__(self):
        self.results = []

    def analyze_interface(self, seq1: str, seq2: str,
                         interface_residues1: Optional[List[int]] = None,
                         interface_residues2: Optional[List[int]] = None) -> Dict:
        """
        Predict interface residues based on sequence composition.
        """
        # If interface not specified, predict based on composition
        if interface_residues1 is None:
            interface_residues1 = self._predict_interface_residues(seq1)
        if interface_residues2 is None:
            interface_residues2 = self._predict_interface_residues(seq2)

        # Analyze interface composition
        interface_seq1 = ''.join([seq1[i] for i in interface_residues1 if i < len(seq1)])
        interface_seq2 = ''.join([seq2[i] for i in interface_residues2 if i < len(seq2)])

        return {
            'interface_residues_1': interface_residues1,
            'interface_residues_2': interface_residues2,
            'interface_size_1': len(interface_residues1),
            'interface_size_2': len(interface_residues2),
            'interface_composition_1': self._analyze_composition(interface_seq1),
            'interface_composition_2': self._analyze_composition(interface_seq2),
        }

    def _predict_interface_residues(self, sequence: str,
                                    window_size: int = 5) -> List[int]:
        """
        Predict likely interface residues based on sequence properties.
        Interface residues tend to be: aromatic, charged, or have mixed polarity.
        """
        scores = []

        for i, aa in enumerate(sequence):
            if aa not in AA_PROPERTIES:
                scores.append(0)
                continue

            props = AA_PROPERTIES[aa]
            score = 0

            # Aromatic residues often at interfaces
            if props.aromatic:
                score += 2

            # Charged residues can form salt bridges
            if abs(props.charge) > 0:
                score += 1.5

            # H-bond capable residues
            score += (props.hbond_donor + props.hbond_acceptor) * 0.5

            # Moderate hydrophobicity (not too buried, not too exposed)
            if -1 < props.hydrophobicity < 2:
                score += 1

            scores.append(score)

        # Smooth with window
        smoothed = np.convolve(scores, np.ones(window_size)/window_size, mode='same')

        # Return residues above threshold
        threshold = np.percentile(smoothed, 70)
        interface_residues = [i for i, s in enumerate(smoothed) if s >= threshold]

        return interface_residues

    def _analyze_composition(self, sequence: str) -> Dict:
        """Analyze amino acid composition."""
        if not sequence:
            return {}

        composition = {}
        for aa in sequence:
            composition[aa] = composition.get(aa, 0) + 1

        # Convert to percentages
        total = len(sequence)
        for aa in composition:
            composition[aa] = composition[aa] / total * 100

        # Categorize
        aromatic = sum(composition.get(aa, 0) for aa in 'FWY')
        charged = sum(composition.get(aa, 0) for aa in 'DEKR')
        polar = sum(composition.get(aa, 0) for aa in 'NQST')
        hydrophobic = sum(composition.get(aa, 0) for aa in 'AILMV')

        return {
            'aromatic_pct': aromatic,
            'charged_pct': charged,
            'polar_pct': polar,
            'hydrophobic_pct': hydrophobic,
        }

    def count_potential_interactions(self, seq1: str, seq2: str,
                                    interface1: List[int],
                                    interface2: List[int]) -> Dict:
        """Count potential favorable interactions."""
        interactions = {
            'salt_bridges': 0,
            'hydrogen_bonds': 0,
            'hydrophobic_contacts': 0,
            'aromatic_interactions': 0,
            'cation_pi': 0,
        }

        # Get interface residues
        res1 = [seq1[i] for i in interface1 if i < len(seq1)]
        res2 = [seq2[i] for i in interface2 if i < len(seq2)]

        # Positively charged in seq1
        pos1 = [aa for aa in res1 if aa in 'RK']
        neg1 = [aa for aa in res1 if aa in 'DE']
        aromatic1 = [aa for aa in res1 if aa in 'FWY']
        hbond1 = [aa for aa in res1 if aa in 'NQSTYW']
        hydrophobic1 = [aa for aa in res1 if aa in 'AILMVF']

        pos2 = [aa for aa in res2 if aa in 'RK']
        neg2 = [aa for aa in res2 if aa in 'DE']
        aromatic2 = [aa for aa in res2 if aa in 'FWY']
        hbond2 = [aa for aa in res2 if aa in 'NQSTYW']
        hydrophobic2 = [aa for aa in res2 if aa in 'AILMVF']

        # Estimate interactions
        interactions['salt_bridges'] = min(len(pos1) + len(neg1),
                                          len(pos2) + len(neg2))
        interactions['hydrogen_bonds'] = min(len(hbond1), len(hbond2)) * 2
        interactions['hydrophobic_contacts'] = min(len(hydrophobic1), len(hydrophobic2))
        interactions['aromatic_interactions'] = min(len(aromatic1), len(aromatic2))
        interactions['cation_pi'] = min(len(pos1) + len(pos2),
                                        len(aromatic1) + len(aromatic2))

        return interactions

    def estimate_binding_energy(self, seq1: str, seq2: str,
                               interface1: Optional[List[int]] = None,
                               interface2: Optional[List[int]] = None) -> Dict:
        """
        Estimate binding free energy (ΔG) in kcal/mol.
        Negative values indicate favorable binding.
        """
        # Get interface
        interface_info = self.analyze_interface(seq1, seq2, interface1, interface2)
        interface1 = interface_info['interface_residues_1']
        interface2 = interface_info['interface_residues_2']

        # Count interactions
        interactions = self.count_potential_interactions(seq1, seq2, interface1, interface2)

        # Calculate energy contributions
        energy_contributions = {}

        # Favorable interactions
        energy_contributions['salt_bridges'] = (
            interactions['salt_bridges'] * ENERGY_PARAMETERS['salt_bridge']
        )
        energy_contributions['hydrogen_bonds'] = (
            interactions['hydrogen_bonds'] * ENERGY_PARAMETERS['hydrogen_bond']
        )
        energy_contributions['hydrophobic'] = (
            interactions['hydrophobic_contacts'] * ENERGY_PARAMETERS['hydrophobic'] * 10
        )  # Scaled by estimated buried area
        energy_contributions['aromatic'] = (
            interactions['aromatic_interactions'] * ENERGY_PARAMETERS['aromatic_stacking']
        )
        energy_contributions['cation_pi'] = (
            interactions['cation_pi'] * ENERGY_PARAMETERS['cation_pi'] * 0.5
        )  # Probability factor

        # Penalties
        interface_size = len(interface1) + len(interface2)
        energy_contributions['entropy_loss'] = (
            interface_size * ENERGY_PARAMETERS['entropy_loss'] * 0.3
        )

        # Total
        delta_g = sum(energy_contributions.values())

        # Estimate KD from ΔG
        # ΔG = RT ln(KD)
        # KD = exp(ΔG / RT)
        RT = 0.592  # kcal/mol at 298K
        kd_M = np.exp(delta_g / RT)

        return {
            'delta_g_kcal_mol': delta_g,
            'kd_M': kd_M,
            'kd_nM': kd_M * 1e9,
            'pKd': -np.log10(kd_M),
            'energy_contributions': energy_contributions,
            'interaction_counts': interactions,
            'interface_info': interface_info,
            'affinity_class': self._classify_affinity(kd_M)
        }

    def _classify_affinity(self, kd_M: float) -> str:
        """Classify binding affinity."""
        if kd_M < 1e-12:
            return "Ultra-tight (sub-pM)"
        elif kd_M < 1e-9:
            return "Very tight (pM-nM)"
        elif kd_M < 1e-6:
            return "Tight (nM-μM)"
        elif kd_M < 1e-3:
            return "Moderate (μM-mM)"
        else:
            return "Weak (>mM)"

    def identify_hotspots(self, sequence: str,
                         interface_residues: List[int]) -> List[Dict]:
        """
        Identify binding hotspot residues.
        Hotspots are residues whose mutation significantly weakens binding.
        """
        hotspots = []

        for i in interface_residues:
            if i >= len(sequence):
                continue

            aa = sequence[i]
            if aa not in AA_PROPERTIES:
                continue

            props = AA_PROPERTIES[aa]
            hotspot_score = 0

            # Aromatic residues are often hotspots (Bogan & Thorn, 1998)
            if aa in 'WYF':
                hotspot_score += 3

            # Charged residues involved in salt bridges
            if aa in 'RKE':
                hotspot_score += 2

            # H-bonding residues
            if props.hbond_donor + props.hbond_acceptor >= 2:
                hotspot_score += 1

            if hotspot_score >= 2:
                hotspots.append({
                    'position': i + 1,  # 1-indexed
                    'residue': aa,
                    'hotspot_score': hotspot_score,
                    'predicted_ddG_ala': hotspot_score * 1.5  # Estimated ΔΔG for Ala mutation
                })

        # Sort by score
        hotspots.sort(key=lambda x: x['hotspot_score'], reverse=True)

        return hotspots


class AntibodyAffinityAnalyzer:
    """
    Specialized analyzer for antibody-antigen binding.
    Focuses on CDR regions and paratope-epitope interactions.
    """

    # Approximate CDR positions (Kabat numbering)
    CDR_POSITIONS = {
        'VH': {
            'CDR1': (31, 35),
            'CDR2': (50, 65),
            'CDR3': (95, 102)
        },
        'VL': {
            'CDR1': (24, 34),
            'CDR2': (50, 56),
            'CDR3': (89, 97)
        }
    }

    def __init__(self):
        self.predictor = BindingAffinityPredictor()

    def analyze_scfv(self, scfv_sequence: str, linker: str = "GGGGS" * 4) -> Dict:
        """
        Analyze scFv antibody binding potential.
        """
        # Try to find linker and split VH/VL
        linker_pos = scfv_sequence.find(linker)

        if linker_pos > 0:
            vh = scfv_sequence[:linker_pos]
            vl = scfv_sequence[linker_pos + len(linker):]
        else:
            # Estimate based on typical lengths
            vh = scfv_sequence[:120]
            vl = scfv_sequence[120:]

        # Identify CDR regions
        vh_cdrs = self._identify_cdrs(vh, 'VH')
        vl_cdrs = self._identify_cdrs(vl, 'VL')

        # Analyze CDR composition
        vh_cdr_analysis = self._analyze_cdrs(vh, vh_cdrs)
        vl_cdr_analysis = self._analyze_cdrs(vl, vl_cdrs)

        # Predict paratope (antigen-binding residues)
        paratope = self._predict_paratope(vh, vl, vh_cdrs, vl_cdrs)

        # Estimate overall affinity potential
        affinity_potential = self._estimate_affinity_potential(
            vh_cdr_analysis, vl_cdr_analysis
        )

        return {
            'vh_length': len(vh),
            'vl_length': len(vl),
            'vh_cdrs': vh_cdrs,
            'vl_cdrs': vl_cdrs,
            'vh_cdr_analysis': vh_cdr_analysis,
            'vl_cdr_analysis': vl_cdr_analysis,
            'predicted_paratope': paratope,
            'affinity_potential': affinity_potential,
            'developability_flags': self._check_developability(vh, vl)
        }

    def _identify_cdrs(self, sequence: str, chain_type: str) -> Dict:
        """Identify CDR regions in VH or VL."""
        cdrs = {}
        positions = self.CDR_POSITIONS.get(chain_type, {})

        for cdr_name, (start, end) in positions.items():
            if end <= len(sequence):
                cdrs[cdr_name] = {
                    'start': start,
                    'end': min(end, len(sequence)),
                    'sequence': sequence[start-1:end]
                }

        return cdrs

    def _analyze_cdrs(self, sequence: str, cdrs: Dict) -> Dict:
        """Analyze CDR composition and properties."""
        analysis = {}

        for cdr_name, cdr_info in cdrs.items():
            cdr_seq = cdr_info['sequence']

            # Count residue types
            aromatic = sum(1 for aa in cdr_seq if aa in 'FWY')
            charged = sum(1 for aa in cdr_seq if aa in 'DEKR')
            hydrophobic = sum(1 for aa in cdr_seq if aa in 'AILMV')

            analysis[cdr_name] = {
                'length': len(cdr_seq),
                'sequence': cdr_seq,
                'aromatic_count': aromatic,
                'charged_count': charged,
                'hydrophobic_count': hydrophobic,
                'aromatic_density': aromatic / len(cdr_seq) if cdr_seq else 0,
            }

        return analysis

    def _predict_paratope(self, vh: str, vl: str,
                         vh_cdrs: Dict, vl_cdrs: Dict) -> List[Dict]:
        """Predict key paratope residues."""
        paratope = []

        # VH CDR3 is usually most important
        if 'CDR3' in vh_cdrs:
            cdr3 = vh_cdrs['CDR3']
            for i, aa in enumerate(cdr3['sequence']):
                if aa in 'WYFRK':  # Common paratope residues
                    paratope.append({
                        'chain': 'VH',
                        'cdr': 'CDR3',
                        'position': cdr3['start'] + i,
                        'residue': aa,
                        'importance': 'high' if aa in 'WYF' else 'medium'
                    })

        # VL CDR3 also contributes
        if 'CDR3' in vl_cdrs:
            cdr3 = vl_cdrs['CDR3']
            for i, aa in enumerate(cdr3['sequence']):
                if aa in 'WYFRK':
                    paratope.append({
                        'chain': 'VL',
                        'cdr': 'CDR3',
                        'position': cdr3['start'] + i,
                        'residue': aa,
                        'importance': 'medium'
                    })

        return paratope

    def _estimate_affinity_potential(self, vh_analysis: Dict,
                                    vl_analysis: Dict) -> Dict:
        """Estimate binding affinity potential based on CDR composition."""
        score = 50  # Baseline

        # CDR3 length and composition are key
        if 'CDR3' in vh_analysis:
            vh_cdr3 = vh_analysis['CDR3']
            # Optimal CDR3 length is ~12-18 residues
            if 12 <= vh_cdr3['length'] <= 18:
                score += 10
            # Aromatic residues enhance binding
            score += vh_cdr3['aromatic_count'] * 5
            # Some charge helps
            score += min(vh_cdr3['charged_count'] * 2, 10)

        if 'CDR3' in vl_analysis:
            vl_cdr3 = vl_analysis['CDR3']
            score += vl_cdr3['aromatic_count'] * 3

        # Cap score
        score = min(score, 100)

        return {
            'score': score,
            'class': self._classify_potential(score),
            'predicted_kd_range': self._predict_kd_range(score)
        }

    def _classify_potential(self, score: float) -> str:
        """Classify affinity potential."""
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Moderate"
        else:
            return "Low"

    def _predict_kd_range(self, score: float) -> str:
        """Predict KD range based on score."""
        if score >= 80:
            return "pM - low nM"
        elif score >= 60:
            return "nM range"
        elif score >= 40:
            return "high nM - low μM"
        else:
            return "μM range or weaker"

    def _check_developability(self, vh: str, vl: str) -> List[str]:
        """Check for developability concerns."""
        flags = []

        # Check for aggregation-prone motifs
        agg_motifs = ['VVV', 'III', 'LLL', 'FFF']
        for motif in agg_motifs:
            if motif in vh or motif in vl:
                flags.append(f"Aggregation-prone motif: {motif}")

        # Check for deamidation sites (NG)
        ng_vh = vh.count('NG')
        ng_vl = vl.count('NG')
        if ng_vh + ng_vl > 2:
            flags.append(f"Multiple deamidation sites (NG): {ng_vh + ng_vl}")

        # Check for oxidation-prone Met
        met_count = vh.count('M') + vl.count('M')
        if met_count > 5:
            flags.append(f"Multiple oxidation-prone Met: {met_count}")

        # Check for unpaired Cys
        cys_vh = vh.count('C')
        cys_vl = vl.count('C')
        if cys_vh % 2 != 0:
            flags.append("Unpaired Cys in VH")
        if cys_vl % 2 != 0:
            flags.append("Unpaired Cys in VL")

        if not flags:
            flags.append("No developability concerns identified")

        return flags


class BindingAffinityPipeline:
    """
    Complete binding affinity analysis pipeline.
    """

    def __init__(self, output_dir: str = "affinity_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.predictor = BindingAffinityPredictor()
        self.antibody_analyzer = AntibodyAffinityAnalyzer()
        self.results = []

    def analyze_antibody(self, name: str, sequence: str,
                        target_sequence: Optional[str] = None) -> Dict:
        """Analyze antibody binding properties."""
        print(f"  Analyzing antibody: {name}")

        # scFv analysis
        scfv_analysis = self.antibody_analyzer.analyze_scfv(sequence)

        result = {
            'name': name,
            'type': 'antibody',
            'sequence_length': len(sequence),
            'analysis': scfv_analysis
        }

        # If target provided, estimate binding
        if target_sequence:
            # Use CDR regions as interface
            interface_residues = []
            for cdr_name, cdr_info in scfv_analysis.get('vh_cdrs', {}).items():
                interface_residues.extend(range(cdr_info['start']-1, cdr_info['end']))

            binding = self.predictor.estimate_binding_energy(
                sequence, target_sequence, interface_residues
            )
            result['binding_prediction'] = binding

        self.results.append(result)
        return result

    def analyze_protein_pair(self, name: str,
                            seq1: str, seq2: str) -> Dict:
        """Analyze protein-protein binding."""
        print(f"  Analyzing interaction: {name}")

        binding = self.predictor.estimate_binding_energy(seq1, seq2)
        hotspots1 = self.predictor.identify_hotspots(
            seq1, binding['interface_info']['interface_residues_1']
        )
        hotspots2 = self.predictor.identify_hotspots(
            seq2, binding['interface_info']['interface_residues_2']
        )

        result = {
            'name': name,
            'type': 'protein_pair',
            'seq1_length': len(seq1),
            'seq2_length': len(seq2),
            'binding_prediction': binding,
            'hotspots_seq1': hotspots1[:5],  # Top 5
            'hotspots_seq2': hotspots2[:5],
        }

        self.results.append(result)
        return result

    def batch_analyze_antibodies(self, antibodies: Dict[str, str]) -> List[Dict]:
        """Analyze multiple antibodies."""
        results = []
        for name, sequence in antibodies.items():
            try:
                result = self.analyze_antibody(name, sequence)
                results.append(result)
            except Exception as e:
                print(f"    Error analyzing {name}: {e}")
                results.append({'name': name, 'error': str(e)})
        return results

    def save_results(self, filename: str = "affinity_analysis.json") -> str:
        """Save results to JSON."""
        output_file = self.output_dir / filename

        output_data = {
            'metadata': {
                'generator': 'M4 Binding Affinity Pipeline',
                'timestamp': datetime.now().isoformat(),
                'n_analyzed': len(self.results)
            },
            'results': self.results
        }

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)

        return str(output_file)

    def generate_report(self) -> str:
        """Generate human-readable report."""
        report = []
        report.append("=" * 70)
        report.append("M4 BINDING AFFINITY ANALYSIS REPORT")
        report.append("=" * 70)
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append(f"Sequences analyzed: {len(self.results)}")
        report.append("")

        # Sort by affinity
        antibodies = [r for r in self.results if r.get('type') == 'antibody']
        pairs = [r for r in self.results if r.get('type') == 'protein_pair']

        if antibodies:
            report.append("ANTIBODY ANALYSIS:")
            report.append("-" * 70)

            # Sort by affinity potential score
            antibodies_sorted = sorted(
                [a for a in antibodies if 'analysis' in a],
                key=lambda x: x['analysis'].get('affinity_potential', {}).get('score', 0),
                reverse=True
            )

            for ab in antibodies_sorted:
                analysis = ab.get('analysis', {})
                potential = analysis.get('affinity_potential', {})

                report.append(f"\n{ab['name']}:")
                report.append(f"  Length: {ab.get('sequence_length', 'N/A')} aa")
                report.append(f"  Affinity Potential: {potential.get('class', 'Unknown')} "
                             f"(score: {potential.get('score', 'N/A')})")
                report.append(f"  Predicted KD range: {potential.get('predicted_kd_range', 'Unknown')}")

                # CDR info
                vh_cdrs = analysis.get('vh_cdr_analysis', {})
                if 'CDR3' in vh_cdrs:
                    cdr3 = vh_cdrs['CDR3']
                    report.append(f"  VH CDR3: {cdr3.get('sequence', 'N/A')} "
                                 f"({cdr3.get('length', 0)} aa)")

                # Developability
                flags = analysis.get('developability_flags', [])
                if flags:
                    report.append(f"  Developability: {', '.join(flags[:3])}")

        if pairs:
            report.append("\n\nPROTEIN-PROTEIN INTERACTIONS:")
            report.append("-" * 70)

            for pair in pairs:
                binding = pair.get('binding_prediction', {})
                report.append(f"\n{pair['name']}:")
                report.append(f"  ΔG: {binding.get('delta_g_kcal_mol', 'N/A'):.2f} kcal/mol")
                report.append(f"  KD: {binding.get('kd_nM', 'N/A'):.2f} nM")
                report.append(f"  Affinity: {binding.get('affinity_class', 'Unknown')}")

                hotspots = pair.get('hotspots_seq1', [])
                if hotspots:
                    hs_str = ', '.join([f"{h['residue']}{h['position']}" for h in hotspots[:3]])
                    report.append(f"  Key hotspots: {hs_str}")

        report.append("")
        report.append("=" * 70)
        report.append("LICENSE: AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication")
        report.append("All data is PUBLIC DOMAIN for patent purposes.")
        report.append("=" * 70)

        return "\n".join(report)


def load_sequences_from_fasta(fasta_file: str) -> Dict[str, str]:
    """Load sequences from FASTA file."""
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


def main():
    """Main execution for overnight binding affinity analysis."""
    print("=" * 70)
    print("M4 BINDING AFFINITY PREDICTION PIPELINE")
    print("Physics-Based Interaction Analysis")
    print("=" * 70)
    print()

    # Setup
    output_dir = Path("affinity_results")
    output_dir.mkdir(exist_ok=True)

    pipeline = BindingAffinityPipeline(str(output_dir))

    # Look for scFv sequences from M4 pipeline
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
            fasta_files.extend(list(search_dir.glob("**/*.fasta")))

    # Deduplicate
    fasta_files = list(set(fasta_files))

    if fasta_files:
        print(f"Found {len(fasta_files)} FASTA files to analyze")

        for fasta_file in fasta_files:
            # Analyze all protein sequences (antibodies get special treatment)
            print(f"\nLoading: {fasta_file.name}")
            sequences = load_sequences_from_fasta(str(fasta_file))

            if sequences:
                print(f"  Found {len(sequences)} sequences")
                pipeline.batch_analyze_antibodies(sequences)

    if not fasta_files:
        # Demo sequences
        print("No FASTA files found, running demo analysis...")

        demo_antibodies = {
            "Demo_Anti_VEGF_scFv": (
                "EVQLVESGGGLVQPGGSLRLSCAASGFTFSSYWMSWVRQAPGKGLEWVANIKQDGSEKY"
                "YVDSVKGRFTISRDNAKNSLYLQMNSLRAEDTAVYYCARWGYRFFDYWGQGTLVTVSS"
                "GGGGSGGGGSGGGGSGGGGS"
                "DIQMTQSPSSLSASVGDRVTITCRASQDVNTAVAWYQQKPGKAPKLLIYSASFLYSGVP"
                "SRFSGSRSGTDFTLTISSLQPEDFATYYCQQHYTTPPTFGQGTKVEIK"
            ),
            "Demo_Angiopep2_scFv": (
                "TFFYGGSRGKRNNFKTEEY"  # Angiopep-2
                "GGGGS" * 4 +  # Linker
                "EVQLVESGGGLVQPGGSLRLSCAASGFTFSDYYMSWVRQAPGKGLEWVAYISSSGST"
                "IYYADSVKGRFTISRDNAKNSLYLQMNSLRAEDTAVYYCARWGQDGFMDYWGQGTLVTVSS"
                "GGGGSGGGGSGGGGSGGGGS"
                "DIQMTQSPSSLSASVGDRVTITCRASQDVNTAVAWYQQKPGKAPKLLIYSASFLYSGVP"
                "SRFSGSRSGTDFTLTISSLQPEDFATYYCQQHYTTPPTFGQGTKVEIK"
            )
        }

        pipeline.batch_analyze_antibodies(demo_antibodies)

    # Save results
    json_file = pipeline.save_results()
    print(f"\nResults saved to: {json_file}")

    # Generate report
    report = pipeline.generate_report()
    report_file = output_dir / "affinity_analysis_report.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"Report saved to: {report_file}")

    # Print summary
    print("\n" + report)

    return pipeline.results


if __name__ == "__main__":
    results = main()
