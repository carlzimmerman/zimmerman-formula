#!/usr/bin/env python3
"""
M4 Z² Validation Experiments
=============================

Rigorous experimental validation framework to test whether Z² corrections
improve predictions compared to classical methods.

HYPOTHESIS:
    Z² = 32π/3 geometric corrections improve molecular property predictions

NULL HYPOTHESIS:
    Z² corrections provide no improvement over classical methods

VALIDATION APPROACH:
    1. Use proteins with KNOWN experimental values (ground truth)
    2. Make blind predictions (classical and Z²-corrected)
    3. Compare both to experimental data
    4. Statistical tests for significance

METRICS:
    - Pearson correlation (r)
    - Root Mean Square Error (RMSE)
    - Mean Absolute Error (MAE)
    - Paired t-test (p-value)

If Z² corrections are real physics, they should:
    - Improve correlation with experimental values
    - Reduce prediction errors
    - Show statistically significant improvement (p < 0.05)

LICENSE: AGPL-3.0 + OpenMTA + CC-BY-SA-4.0
"""

import numpy as np
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import urllib.request
import warnings

# Z² constants
Z = 2 * np.sqrt(8 * np.pi / 3)  # Z = 2√(8π/3) ≈ 5.7735
Z_SQUARED = 32 * np.pi / 3       # Z² = 32π/3 ≈ 33.51

# =============================================================================
# EXPERIMENTAL GROUND TRUTH DATABASES
# =============================================================================

# Protein-protein binding affinities with EXPERIMENTAL Kd values
# Sources: PDBbind, BindingDB, literature
BINDING_VALIDATION_SET = [
    # Antibody-antigen interactions (well-characterized)
    {
        'name': 'Trastuzumab-HER2',
        'type': 'antibody-antigen',
        'kd_nM': 0.1,  # 100 pM - experimental
        'delta_g_kcal': -13.6,  # from Kd
        'interface_area_A2': 1800,
        'source': 'Cho et al. Nature 2003',
        'pdb': '1N8Z',
    },
    {
        'name': 'Bevacizumab-VEGF',
        'type': 'antibody-antigen',
        'kd_nM': 0.5,
        'delta_g_kcal': -12.7,
        'interface_area_A2': 1650,
        'source': 'Muller et al. Structure 1998',
        'pdb': '1BJ1',
    },
    {
        'name': 'Adalimumab-TNFα',
        'type': 'antibody-antigen',
        'kd_nM': 0.1,
        'delta_g_kcal': -13.6,
        'interface_area_A2': 1750,
        'source': 'Hu et al. JBC 2013',
        'pdb': '3WD5',
    },
    {
        'name': 'Rituximab-CD20',
        'type': 'antibody-antigen',
        'kd_nM': 8.0,
        'delta_g_kcal': -11.0,
        'interface_area_A2': 1400,
        'source': 'Du et al. JBC 2008',
        'pdb': '2OSL',
    },
    {
        'name': 'Cetuximab-EGFR',
        'type': 'antibody-antigen',
        'kd_nM': 0.39,
        'delta_g_kcal': -12.8,
        'interface_area_A2': 1600,
        'source': 'Li et al. Cancer Cell 2005',
        'pdb': '1YY9',
    },
    # Enzyme-inhibitor interactions
    {
        'name': 'Barnase-Barstar',
        'type': 'enzyme-inhibitor',
        'kd_nM': 0.00001,  # 10 fM - one of tightest known
        'delta_g_kcal': -19.0,
        'interface_area_A2': 1500,
        'source': 'Schreiber & Fersht JMB 1995',
        'pdb': '1BRS',
    },
    {
        'name': 'TEM1-BLIP',
        'type': 'enzyme-inhibitor',
        'kd_nM': 0.5,
        'delta_g_kcal': -12.7,
        'interface_area_A2': 1200,
        'source': 'Strynadka et al. Nature 1994',
        'pdb': '1JTG',
    },
    {
        'name': 'Trypsin-BPTI',
        'type': 'enzyme-inhibitor',
        'kd_nM': 0.06,
        'delta_g_kcal': -13.9,
        'interface_area_A2': 1400,
        'source': 'Castro & Anderson Biochemistry 1996',
        'pdb': '2PTC',
    },
    # Protein-protein interactions (general)
    {
        'name': 'p53-MDM2',
        'type': 'protein-protein',
        'kd_nM': 600,
        'delta_g_kcal': -8.5,
        'interface_area_A2': 700,
        'source': 'Schon et al. JMB 2002',
        'pdb': '1YCR',
    },
    {
        'name': 'IL2-IL2Rα',
        'type': 'protein-protein',
        'kd_nM': 10,
        'delta_g_kcal': -10.9,
        'interface_area_A2': 1100,
        'source': 'Wang et al. Science 2005',
        'pdb': '1Z92',
    },
    {
        'name': 'Ras-Raf',
        'type': 'protein-protein',
        'kd_nM': 20,
        'delta_g_kcal': -10.5,
        'interface_area_A2': 1300,
        'source': 'Nassar et al. Nature 1995',
        'pdb': '1GUA',
    },
    {
        'name': 'Insulin-InsR',
        'type': 'protein-protein',
        'kd_nM': 0.2,
        'delta_g_kcal': -13.2,
        'interface_area_A2': 1900,
        'source': 'Menting et al. Nature 2013',
        'pdb': '3W14',
    },
]

# Protein stability with EXPERIMENTAL ΔG unfolding values
STABILITY_VALIDATION_SET = [
    {
        'name': 'Lysozyme (hen)',
        'length': 129,
        'delta_g_unfold_kcal': 9.0,  # Positive = stable
        'tm_celsius': 72,
        'source': 'Privalov & Khechinashvili JMB 1974',
        'pdb': '1LYZ',
    },
    {
        'name': 'RNase A',
        'length': 124,
        'delta_g_unfold_kcal': 8.7,
        'tm_celsius': 63,
        'source': 'Pace et al. FASEB 1996',
        'pdb': '7RSA',
    },
    {
        'name': 'Myoglobin',
        'length': 153,
        'delta_g_unfold_kcal': 10.5,
        'tm_celsius': 76,
        'source': 'Privalov Adv Protein Chem 1979',
        'pdb': '1MBN',
    },
    {
        'name': 'Cytochrome c',
        'length': 104,
        'delta_g_unfold_kcal': 8.0,
        'tm_celsius': 83,
        'source': 'Makhatadze & Privalov JMB 1992',
        'pdb': '1HRC',
    },
    {
        'name': 'Ubiquitin',
        'length': 76,
        'delta_g_unfold_kcal': 7.5,
        'tm_celsius': 87,
        'source': 'Wintrode et al. Proteins 1994',
        'pdb': '1UBQ',
    },
    {
        'name': 'SH3 domain (Src)',
        'length': 57,
        'delta_g_unfold_kcal': 3.5,
        'tm_celsius': 56,
        'source': 'Grantcharova & Baker Biochemistry 1997',
        'pdb': '1SRL',
    },
    {
        'name': 'Barnase',
        'length': 110,
        'delta_g_unfold_kcal': 10.2,
        'tm_celsius': 55,
        'source': 'Matouschek et al. Nature 1989',
        'pdb': '1BNR',
    },
    {
        'name': 'CI2',
        'length': 64,
        'delta_g_unfold_kcal': 7.0,
        'tm_celsius': 64,
        'source': 'Jackson & Fersht Biochemistry 1991',
        'pdb': '2CI2',
    },
]

# BBB penetration with EXPERIMENTAL permeability data
BBB_VALIDATION_SET = [
    # Small molecule calibration (Papp values)
    {
        'name': 'Caffeine',
        'mw': 194,
        'psa': 58,
        'logP': -0.07,
        'bbb_penetrant': True,
        'papp_cm_s': 2.5e-5,  # High permeability
        'source': 'Summerfield et al. JPharmSci 2007',
    },
    {
        'name': 'Verapamil',
        'mw': 455,
        'psa': 64,
        'logP': 3.79,
        'bbb_penetrant': True,
        'papp_cm_s': 1.8e-5,
        'source': 'Di et al. DrugDiscovToday 2003',
    },
    {
        'name': 'Atenolol',
        'mw': 266,
        'psa': 85,
        'logP': 0.16,
        'bbb_penetrant': False,
        'papp_cm_s': 2.0e-7,  # Low permeability
        'source': 'Summerfield et al. JPharmSci 2007',
    },
    # Peptide/protein data
    {
        'name': 'Angiopep-2 (19aa)',
        'mw': 2300,
        'psa': 450,
        'logP': -2.5,
        'bbb_penetrant': True,  # LRP1-mediated
        'transcytosis_quotient': 0.85,
        'source': 'Demeule et al. JNeurochem 2008',
    },
    {
        'name': 'TAT peptide (11aa)',
        'mw': 1560,
        'psa': 380,
        'logP': -4.0,
        'bbb_penetrant': True,  # CPP
        'transcytosis_quotient': 0.45,
        'source': 'Schwarze et al. Science 1999',
    },
    {
        'name': 'Insulin (51aa)',
        'mw': 5800,
        'psa': 1200,
        'logP': -3.0,
        'bbb_penetrant': False,  # Too large
        'transcytosis_quotient': 0.02,
        'source': 'Pardridge WM NeuroRx 2005',
    },
    {
        'name': 'Transferrin (679aa)',
        'mw': 77000,
        'psa': 15000,
        'logP': -10.0,
        'bbb_penetrant': True,  # Receptor-mediated
        'transcytosis_quotient': 0.15,
        'source': 'Friden et al. PNAS 1991',
    },
]


# =============================================================================
# PREDICTION MODELS
# =============================================================================

class ClassicalPredictor:
    """
    Classical (non-Z²) binding and stability predictions.
    Based on standard computational biology approaches.
    """

    def predict_binding_energy(self, interface_area: float,
                               n_hbonds: int = None,
                               n_salt_bridges: int = None) -> float:
        """
        Classical binding energy prediction.

        Uses empirical relationship:
        ΔG ≈ -0.01 * interface_area (crude approximation)

        More sophisticated: include H-bonds, salt bridges
        """
        # Empirical: ~10-30 cal/mol per Å² of buried surface
        base_energy = -0.02 * interface_area

        # H-bond contribution (~1-2 kcal/mol each)
        if n_hbonds:
            base_energy -= 1.5 * n_hbonds

        # Salt bridge contribution (~1-4 kcal/mol each)
        if n_salt_bridges:
            base_energy -= 2.0 * n_salt_bridges

        return base_energy

    def predict_stability(self, length: int,
                         hydrophobic_fraction: float = 0.35) -> float:
        """
        Classical stability prediction.

        Empirical: ΔG_unfold ≈ 0.05-0.1 kcal/mol per residue for stable proteins
        """
        # Base stability from length
        base_stability = 0.07 * length

        # Hydrophobic contribution
        hydrophobic_bonus = hydrophobic_fraction * length * 0.03

        return base_stability + hydrophobic_bonus

    def predict_bbb_score(self, mw: float, psa: float,
                          logP: float = 0) -> float:
        """
        Classical BBB penetration score.

        Based on Lipinski-like rules and empirical models.
        """
        # MW penalty (sharp cutoff around 400-500)
        mw_score = np.exp(-mw / 400) if mw < 5000 else np.exp(-mw / 50000)

        # PSA penalty (cutoff around 90 Å²)
        psa_score = np.exp(-psa / 90)

        # LogP (optimal around 1-3)
        logp_score = np.exp(-(logP - 2)**2 / 4)

        # Combined score
        score = (mw_score * psa_score * logp_score) ** (1/3)

        return np.clip(score, 0, 1)


class Z2Predictor:
    """
    Z²-corrected predictions using holographic framework.
    """

    def __init__(self):
        self.z = Z
        self.z2 = Z_SQUARED
        self.classical = ClassicalPredictor()

    def holographic_entropy(self, area: float) -> float:
        """Calculate holographic entropy for surface area."""
        # Effective molecular Planck length (~1 Å)
        l_eff = 1.0  # Ångstroms
        return area / (4 * l_eff**2)

    def predict_binding_energy(self, interface_area: float,
                               total_surface: float = None,
                               n_hbonds: int = None,
                               n_salt_bridges: int = None) -> float:
        """
        Z²-corrected binding energy.

        ΔG_Z² = ΔG_classical / [1 + (Z² - 1) * (S_interface/S_total) * f_proj]
        """
        # Classical prediction
        classical_dg = self.classical.predict_binding_energy(
            interface_area, n_hbonds, n_salt_bridges
        )

        # Holographic correction
        if total_surface is None:
            total_surface = interface_area * 5  # Estimate

        S_interface = self.holographic_entropy(interface_area)
        S_total = self.holographic_entropy(total_surface)

        info_ratio = S_interface / S_total if S_total > 0 else 0.2

        # Projection factor (simplified)
        f_proj = 0.5  # Assume half of manifold sampled

        # Z² correction factor
        z2_factor = 1 + (self.z2 - 1) * info_ratio * f_proj

        # Corrected energy
        z2_dg = classical_dg / z2_factor

        return z2_dg

    def predict_stability(self, length: int,
                         hydrophobic_fraction: float = 0.35) -> float:
        """
        Z²-corrected stability prediction.

        Uses manifold volume factor.
        """
        classical_stability = self.classical.predict_stability(
            length, hydrophobic_fraction
        )

        # Z² correction: stability enhanced by manifold constraint
        # Smaller proteins gain more from Z² (less entropy to lose)
        z2_factor = 1 + (self.z2 / 10) * (100 / length)

        return classical_stability * z2_factor

    def predict_bbb_score(self, mw: float, psa: float,
                          logP: float = 0) -> float:
        """
        Z²-corrected BBB score.

        Based on horizon thermodynamics.
        """
        classical_score = self.classical.predict_bbb_score(mw, psa, logP)

        # Z² enhancement for optimal geometry
        # Horizon crossing favors specific size ratios

        # Membrane "channel" cross-section
        channel_area = 400  # Å² (typical membrane protein pore)

        # Molecule cross-section
        radius = (3 * mw / (4 * np.pi * 1.35)) ** (1/3)  # Assume density 1.35
        molecule_area = np.pi * radius**2

        # Z² optimal ratio
        area_ratio = molecule_area / channel_area
        z2_optimal = 1 / self.z2  # ~0.12

        # Enhancement when close to Z² optimal
        z2_enhancement = np.exp(-(area_ratio - z2_optimal)**2 / 0.1)

        z2_score = classical_score * (1 + 0.5 * z2_enhancement)

        return np.clip(z2_score, 0, 1)


# =============================================================================
# VALIDATION FRAMEWORK
# =============================================================================

@dataclass
class ValidationResult:
    """Results from validation comparison."""
    metric: str
    n_samples: int
    classical_predictions: List[float]
    z2_predictions: List[float]
    experimental_values: List[float]

    # Statistics
    classical_correlation: float = 0.0
    z2_correlation: float = 0.0
    classical_rmse: float = 0.0
    z2_rmse: float = 0.0
    classical_mae: float = 0.0
    z2_mae: float = 0.0

    # Significance
    t_statistic: float = 0.0
    p_value: float = 1.0
    z2_significantly_better: bool = False


class Z2ValidationFramework:
    """
    Rigorous validation of Z² corrections against experimental data.
    """

    def __init__(self, output_dir: str = "validation_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.classical = ClassicalPredictor()
        self.z2 = Z2Predictor()

        self.results = {}

    def calculate_statistics(self,
                            predictions: List[float],
                            experimental: List[float]) -> Dict:
        """Calculate correlation and error metrics."""
        pred = np.array(predictions)
        exp = np.array(experimental)

        # Pearson correlation
        if len(pred) > 2:
            correlation = np.corrcoef(pred, exp)[0, 1]
        else:
            correlation = 0.0

        # RMSE
        rmse = np.sqrt(np.mean((pred - exp)**2))

        # MAE
        mae = np.mean(np.abs(pred - exp))

        return {
            'correlation': correlation,
            'rmse': rmse,
            'mae': mae,
        }

    def paired_t_test(self,
                      errors1: List[float],
                      errors2: List[float]) -> Tuple[float, float]:
        """
        Paired t-test to determine if Z² errors are significantly smaller.

        H0: mean(errors_z2) >= mean(errors_classical)
        H1: mean(errors_z2) < mean(errors_classical)
        """
        e1 = np.array(errors1)
        e2 = np.array(errors2)

        n = len(e1)
        if n < 3:
            return 0.0, 1.0

        # Difference in absolute errors
        diff = np.abs(e1) - np.abs(e2)  # Positive if Z² is better

        mean_diff = np.mean(diff)
        std_diff = np.std(diff, ddof=1)

        if std_diff == 0:
            return 0.0, 1.0

        t_stat = mean_diff / (std_diff / np.sqrt(n))

        # One-tailed p-value (is Z² better?)
        # Using approximation for t-distribution
        from math import erf, sqrt
        p_value = 0.5 * (1 - erf(t_stat / sqrt(2)))

        return t_stat, p_value

    def validate_binding(self) -> ValidationResult:
        """
        Validate binding energy predictions against experimental Kd values.
        """
        print("\n" + "="*60)
        print("BINDING ENERGY VALIDATION")
        print("="*60)

        classical_pred = []
        z2_pred = []
        experimental = []
        names = []

        for entry in BINDING_VALIDATION_SET:
            name = entry['name']
            interface_area = entry['interface_area_A2']
            exp_dg = entry['delta_g_kcal']

            # Estimate total surface from interface (rough)
            total_surface = interface_area * 4

            # Classical prediction
            classical_dg = self.classical.predict_binding_energy(interface_area)

            # Z² prediction
            z2_dg = self.z2.predict_binding_energy(interface_area, total_surface)

            classical_pred.append(classical_dg)
            z2_pred.append(z2_dg)
            experimental.append(exp_dg)
            names.append(name)

            print(f"\n{name}:")
            print(f"  Experimental ΔG:  {exp_dg:.1f} kcal/mol")
            print(f"  Classical pred:   {classical_dg:.1f} kcal/mol (error: {abs(classical_dg - exp_dg):.1f})")
            print(f"  Z² pred:          {z2_dg:.1f} kcal/mol (error: {abs(z2_dg - exp_dg):.1f})")

        # Statistics
        classical_stats = self.calculate_statistics(classical_pred, experimental)
        z2_stats = self.calculate_statistics(z2_pred, experimental)

        # Errors for t-test
        classical_errors = [p - e for p, e in zip(classical_pred, experimental)]
        z2_errors = [p - e for p, e in zip(z2_pred, experimental)]

        t_stat, p_value = self.paired_t_test(classical_errors, z2_errors)

        result = ValidationResult(
            metric='binding_energy',
            n_samples=len(experimental),
            classical_predictions=classical_pred,
            z2_predictions=z2_pred,
            experimental_values=experimental,
            classical_correlation=classical_stats['correlation'],
            z2_correlation=z2_stats['correlation'],
            classical_rmse=classical_stats['rmse'],
            z2_rmse=z2_stats['rmse'],
            classical_mae=classical_stats['mae'],
            z2_mae=z2_stats['mae'],
            t_statistic=t_stat,
            p_value=p_value,
            z2_significantly_better=(p_value < 0.05 and z2_stats['rmse'] < classical_stats['rmse']),
        )

        print("\n" + "-"*40)
        print("BINDING VALIDATION SUMMARY:")
        print(f"  N samples: {result.n_samples}")
        print(f"  Classical: r={result.classical_correlation:.3f}, RMSE={result.classical_rmse:.2f}")
        print(f"  Z²:        r={result.z2_correlation:.3f}, RMSE={result.z2_rmse:.2f}")
        print(f"  t-test:    t={result.t_statistic:.2f}, p={result.p_value:.4f}")
        print(f"  Z² significantly better: {result.z2_significantly_better}")

        self.results['binding'] = result
        return result

    def validate_stability(self) -> ValidationResult:
        """
        Validate stability predictions against experimental ΔG unfolding.
        """
        print("\n" + "="*60)
        print("PROTEIN STABILITY VALIDATION")
        print("="*60)

        classical_pred = []
        z2_pred = []
        experimental = []

        for entry in STABILITY_VALIDATION_SET:
            name = entry['name']
            length = entry['length']
            exp_dg = entry['delta_g_unfold_kcal']

            # Classical prediction
            classical_dg = self.classical.predict_stability(length)

            # Z² prediction
            z2_dg = self.z2.predict_stability(length)

            classical_pred.append(classical_dg)
            z2_pred.append(z2_dg)
            experimental.append(exp_dg)

            print(f"\n{name} ({length} aa):")
            print(f"  Experimental ΔG:  {exp_dg:.1f} kcal/mol")
            print(f"  Classical pred:   {classical_dg:.1f} kcal/mol (error: {abs(classical_dg - exp_dg):.1f})")
            print(f"  Z² pred:          {z2_dg:.1f} kcal/mol (error: {abs(z2_dg - exp_dg):.1f})")

        # Statistics
        classical_stats = self.calculate_statistics(classical_pred, experimental)
        z2_stats = self.calculate_statistics(z2_pred, experimental)

        classical_errors = [p - e for p, e in zip(classical_pred, experimental)]
        z2_errors = [p - e for p, e in zip(z2_pred, experimental)]
        t_stat, p_value = self.paired_t_test(classical_errors, z2_errors)

        result = ValidationResult(
            metric='stability',
            n_samples=len(experimental),
            classical_predictions=classical_pred,
            z2_predictions=z2_pred,
            experimental_values=experimental,
            classical_correlation=classical_stats['correlation'],
            z2_correlation=z2_stats['correlation'],
            classical_rmse=classical_stats['rmse'],
            z2_rmse=z2_stats['rmse'],
            classical_mae=classical_stats['mae'],
            z2_mae=z2_stats['mae'],
            t_statistic=t_stat,
            p_value=p_value,
            z2_significantly_better=(p_value < 0.05 and z2_stats['rmse'] < classical_stats['rmse']),
        )

        print("\n" + "-"*40)
        print("STABILITY VALIDATION SUMMARY:")
        print(f"  N samples: {result.n_samples}")
        print(f"  Classical: r={result.classical_correlation:.3f}, RMSE={result.classical_rmse:.2f}")
        print(f"  Z²:        r={result.z2_correlation:.3f}, RMSE={result.z2_rmse:.2f}")
        print(f"  t-test:    t={result.t_statistic:.2f}, p={result.p_value:.4f}")
        print(f"  Z² significantly better: {result.z2_significantly_better}")

        self.results['stability'] = result
        return result

    def validate_bbb(self) -> ValidationResult:
        """
        Validate BBB penetration predictions.
        """
        print("\n" + "="*60)
        print("BBB PENETRATION VALIDATION")
        print("="*60)

        classical_pred = []
        z2_pred = []
        experimental = []

        for entry in BBB_VALIDATION_SET:
            name = entry['name']
            mw = entry['mw']
            psa = entry['psa']
            logP = entry.get('logP', 0)

            # Experimental: use transcytosis quotient if available, else binary
            if 'transcytosis_quotient' in entry:
                exp_score = entry['transcytosis_quotient']
            else:
                exp_score = 1.0 if entry['bbb_penetrant'] else 0.0

            # Predictions
            classical_score = self.classical.predict_bbb_score(mw, psa, logP)
            z2_score = self.z2.predict_bbb_score(mw, psa, logP)

            classical_pred.append(classical_score)
            z2_pred.append(z2_score)
            experimental.append(exp_score)

            print(f"\n{name}:")
            print(f"  Experimental:   {exp_score:.2f}")
            print(f"  Classical pred: {classical_score:.2f} (error: {abs(classical_score - exp_score):.2f})")
            print(f"  Z² pred:        {z2_score:.2f} (error: {abs(z2_score - exp_score):.2f})")

        # Statistics
        classical_stats = self.calculate_statistics(classical_pred, experimental)
        z2_stats = self.calculate_statistics(z2_pred, experimental)

        classical_errors = [p - e for p, e in zip(classical_pred, experimental)]
        z2_errors = [p - e for p, e in zip(z2_pred, experimental)]
        t_stat, p_value = self.paired_t_test(classical_errors, z2_errors)

        result = ValidationResult(
            metric='bbb_penetration',
            n_samples=len(experimental),
            classical_predictions=classical_pred,
            z2_predictions=z2_pred,
            experimental_values=experimental,
            classical_correlation=classical_stats['correlation'],
            z2_correlation=z2_stats['correlation'],
            classical_rmse=classical_stats['rmse'],
            z2_rmse=z2_stats['rmse'],
            classical_mae=classical_stats['mae'],
            z2_mae=z2_stats['mae'],
            t_statistic=t_stat,
            p_value=p_value,
            z2_significantly_better=(p_value < 0.05 and z2_stats['rmse'] < classical_stats['rmse']),
        )

        print("\n" + "-"*40)
        print("BBB VALIDATION SUMMARY:")
        print(f"  N samples: {result.n_samples}")
        print(f"  Classical: r={result.classical_correlation:.3f}, RMSE={result.classical_rmse:.2f}")
        print(f"  Z²:        r={result.z2_correlation:.3f}, RMSE={result.z2_rmse:.2f}")
        print(f"  t-test:    t={result.t_statistic:.2f}, p={result.p_value:.4f}")
        print(f"  Z² significantly better: {result.z2_significantly_better}")

        self.results['bbb'] = result
        return result

    def run_full_validation(self) -> Dict:
        """
        Run complete validation suite.
        """
        print("="*70)
        print("Z² VALIDATION EXPERIMENTS")
        print("Testing whether Z² corrections improve predictions")
        print("="*70)
        print()
        print(f"Z = 2√(8π/3) = {Z:.6f}")
        print(f"Z² = 8π/3 = {Z_SQUARED:.6f}")
        print()
        print("NULL HYPOTHESIS: Z² corrections provide no improvement")
        print("ALTERNATIVE: Z² corrections improve predictions (p < 0.05)")

        # Run validations
        binding_result = self.validate_binding()
        stability_result = self.validate_stability()
        bbb_result = self.validate_bbb()

        # Overall assessment
        print("\n" + "="*70)
        print("FINAL ASSESSMENT")
        print("="*70)

        improvements = 0
        significant = 0

        for name, result in self.results.items():
            rmse_improvement = (result.classical_rmse - result.z2_rmse) / result.classical_rmse * 100

            if result.z2_rmse < result.classical_rmse:
                improvements += 1
            if result.z2_significantly_better:
                significant += 1

            status = "✓ SIGNIFICANT" if result.z2_significantly_better else "✗ Not significant"

            print(f"\n{name.upper()}:")
            print(f"  RMSE improvement: {rmse_improvement:+.1f}%")
            print(f"  Correlation change: {result.z2_correlation - result.classical_correlation:+.3f}")
            print(f"  p-value: {result.p_value:.4f}")
            print(f"  Status: {status}")

        # Verdict
        print("\n" + "="*70)
        print("VERDICT")
        print("="*70)

        if significant == 3:
            verdict = "STRONG SUPPORT for Z² corrections"
            recommendation = "Z² framework appears valid - proceed with confidence"
        elif significant >= 1:
            verdict = "PARTIAL SUPPORT for Z² corrections"
            recommendation = "Z² shows promise but needs more validation"
        else:
            verdict = "NO SUPPORT for Z² corrections"
            recommendation = "Z² framework not validated - treat as hypothesis only"

        print(f"\n{verdict}")
        print(f"\nSignificant improvements: {significant}/3 metrics")
        print(f"RMSE reductions: {improvements}/3 metrics")
        print(f"\nRecommendation: {recommendation}")

        # Save results
        report = {
            'timestamp': datetime.now().isoformat(),
            'z_factor': Z,
            'z_squared': Z_SQUARED,
            'validation_results': {
                name: {
                    'n_samples': r.n_samples,
                    'classical_correlation': r.classical_correlation,
                    'z2_correlation': r.z2_correlation,
                    'classical_rmse': r.classical_rmse,
                    'z2_rmse': r.z2_rmse,
                    'p_value': r.p_value,
                    'significant': r.z2_significantly_better,
                }
                for name, r in self.results.items()
            },
            'verdict': verdict,
            'recommendation': recommendation,
        }

        report_path = self.output_dir / "z2_validation_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\nFull report: {report_path}")

        return report


def main():
    """Run Z² validation experiments."""
    validator = Z2ValidationFramework(output_dir="validation_results")
    report = validator.run_full_validation()
    return report


if __name__ == "__main__":
    main()
