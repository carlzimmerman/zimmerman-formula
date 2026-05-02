#!/usr/bin/env python3
"""
Z² Intensity Model v2.0 - Updated with Helene Learnings

Key improvements from Helene analysis:
1. V* Watch metric for RI potential
2. ΔV*/12h rate of change tracking
3. Combined predictor: RI_Probability = f(distance_from_V*3) × g(environment)
4. Peak V* ceiling at 4-5 (MPI limit)
5. Separate structural (V*=3) and intensity (V*=1.75) equilibria
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, Optional, List
from dataclasses import dataclass, field
from enum import Enum

# Z² Constants
Z_SQUARED = 32 * np.pi / 3  # 33.51
Z = np.sqrt(Z_SQUARED)
PHI = (1 + np.sqrt(5)) / 2
INV_PHI = 1 / PHI

# Equilibrium Points
V_STAR_STRUCTURAL = 3.0    # Structural equilibrium (golden ratio in eye)
V_STAR_INTENSITY = 1.75    # Intensity equilibrium (mean ΔV ≈ 0)
V_STAR_MPI_LIMIT = 5.0     # Maximum Potential Intensity limit

# Thresholds from Helene analysis
RI_POTENTIAL_THRESHOLD = 2.5       # V* below this = high RI potential
RI_ACTIVE_RATE = 0.4               # ΔV*/12h above this = active RI
RI_OVERSHOOT_RATE = 0.6            # ΔV*/12h above this = may overshoot V*=3

class RIPotential(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"

@dataclass
class EnvironmentFactors:
    """Environmental factors that enable or inhibit intensification."""
    sst: float          # Sea Surface Temperature (°C)
    shear: float        # Vertical wind shear (kt)
    ohc: float          # Ocean Heat Content (kJ/cm²)
    rh_mid: float       # Mid-level relative humidity (%)
    outflow: float      # Upper-level divergence (normalized 0-1)

    @property
    def favorable_score(self) -> float:
        """Calculate environmental favorability (0-1)."""
        scores = []

        # SST: Need > 26.5°C, optimal at 30°C
        sst_score = min(1.0, max(0, (self.sst - 26.5) / 3.5))
        scores.append(sst_score)

        # Shear: Need < 15 kt, optimal at 0
        shear_score = max(0, 1 - self.shear / 15)
        scores.append(shear_score)

        # OHC: Need > 50 kJ/cm², optimal at 100
        ohc_score = min(1.0, max(0, (self.ohc - 50) / 50))
        scores.append(ohc_score)

        # Mid-level RH: Need > 50%, optimal at 80%
        rh_score = min(1.0, max(0, (self.rh_mid - 50) / 30))
        scores.append(rh_score)

        # Outflow: Direct score (0-1)
        scores.append(self.outflow)

        # Geometric mean for multiplicative effect
        return np.prod(scores) ** (1/len(scores))

    @property
    def is_favorable(self) -> bool:
        """Quick check if conditions support intensification."""
        return (
            self.sst > 26.5 and
            self.shear < 15 and
            self.ohc > 50 and
            self.rh_mid > 50 and
            self.outflow > 0.5
        )

@dataclass
class StormState:
    """Current storm state for prediction."""
    vmax: float         # Maximum sustained wind (kt)
    lat: float          # Latitude
    lon: float          # Longitude
    mslp: float         # Minimum sea level pressure (mb)
    rmw: float          # Radius of maximum wind (nm)
    vmax_history: List[float] = field(default_factory=list)

    @property
    def v_star(self) -> float:
        """Normalized intensity V* = Vmax/Z²."""
        return self.vmax / Z_SQUARED

    @property
    def distance_from_structural(self) -> float:
        """Distance from V*=3 structural equilibrium."""
        return abs(self.v_star - V_STAR_STRUCTURAL)

    @property
    def distance_from_intensity(self) -> float:
        """Distance from V*=1.75 intensity equilibrium."""
        return abs(self.v_star - V_STAR_INTENSITY)

    @property
    def delta_vstar_12h(self) -> Optional[float]:
        """Rate of V* change over last 12h."""
        if self.vmax_history and len(self.vmax_history) >= 2:
            prev_vstar = self.vmax_history[-2] / Z_SQUARED
            return self.v_star - prev_vstar
        return None

    @property
    def is_over_land(self) -> bool:
        """Simple check if storm is over land (rough approximation)."""
        if self.lat > 25 and self.lat < 50:
            if self.lon > -100 and self.lon < -70:
                return True
        return False

class Z2IntensityModelV2:
    """
    Z² Framework Intensity Prediction Model v2.0

    Tuned based on RI storm validation.
    """

    def __init__(self):
        self.name = "Z² Intensity Model v2.0"
        self.version = "2.0"

        # Aggressively tuned coefficients for RI capture
        self.structural_pull_coef = 0.65   # Pull toward V*=3 (aggressive)
        self.momentum_coef = 0.70          # Trend persistence (strong)
        self.env_boost_coef = 2.0          # Environmental boost factor
        self.mpi_approach_rate = 0.35      # Rate of approach to MPI

    def calculate_ri_potential(
        self,
        storm: StormState,
        env: EnvironmentFactors
    ) -> Tuple[RIPotential, float]:
        """Calculate RI potential using V* Watch metric."""
        v_star = storm.v_star
        env_score = env.favorable_score

        # Distance-based RI potential
        if v_star < 1.5:
            dist_potential = 0.9
        elif v_star < 2.0:
            dist_potential = 0.8
        elif v_star < 2.5:
            dist_potential = 0.6
        elif v_star < 3.0:
            dist_potential = 0.3
        else:
            dist_potential = 0.1

        ri_probability = dist_potential * env_score

        if storm.delta_vstar_12h:
            if storm.delta_vstar_12h > RI_OVERSHOOT_RATE:
                ri_probability = min(0.95, ri_probability * 1.5)
            elif storm.delta_vstar_12h > RI_ACTIVE_RATE:
                ri_probability = min(0.9, ri_probability * 1.3)

        if ri_probability > 0.7:
            category = RIPotential.VERY_HIGH
        elif ri_probability > 0.5:
            category = RIPotential.HIGH
        elif ri_probability > 0.3:
            category = RIPotential.MODERATE
        else:
            category = RIPotential.LOW

        return category, ri_probability

    def predict_intensity_change(
        self,
        storm: StormState,
        env: EnvironmentFactors,
        lead_hours: int = 24
    ) -> Dict:
        """
        Predict intensity change with improved RI capture.

        Uses exponential approach to MPI when conditions are favorable.
        """
        v_star = storm.v_star
        env_score = env.favorable_score

        # Calculate MPI based on environment (rough approximation)
        # MPI in V* units: typically 4-5.5 for warm waters
        mpi_vstar = 3.5 + env_score * 2.0  # Range: 3.5-5.5

        # Distance to MPI (positive = room to grow)
        distance_to_mpi = mpi_vstar - v_star

        if env.is_favorable and v_star < V_STAR_STRUCTURAL:
            # FAVORABLE RI CONDITIONS
            # Use exponential approach toward MPI

            # Rate depends on how far below equilibrium and environment
            approach_rate = self.mpi_approach_rate * (1 + env_score)  # Per 12h

            # Structural attractor effect (stronger when below V*=3)
            structural_pull = (V_STAR_STRUCTURAL - v_star) * self.structural_pull_coef

            # MPI pull effect (drives toward peak intensity)
            mpi_pull = distance_to_mpi * 0.15 * env_score

            # Add momentum if actively intensifying
            momentum = 0
            if storm.delta_vstar_12h and storm.delta_vstar_12h > 0:
                # Positive feedback during RI - exponential factor
                momentum = storm.delta_vstar_12h * self.momentum_coef * self.env_boost_coef

            # Non-linear intensification rate (faster when farther from equilibrium)
            distance_factor = 1 + 0.5 * max(0, V_STAR_STRUCTURAL - v_star)

            delta_vstar_12h = (approach_rate * distance_to_mpi + structural_pull + mpi_pull + momentum) * env_score * distance_factor

        elif env.is_favorable and v_star >= V_STAR_STRUCTURAL:
            # NEAR OR ABOVE EQUILIBRIUM
            # Still can intensify toward MPI but with momentum
            approach_rate = 0.20 * env_score
            delta_vstar_12h = approach_rate * max(0, distance_to_mpi)

            # Add momentum (important for continuing RI past V*=3)
            if storm.delta_vstar_12h and storm.delta_vstar_12h > 0:
                delta_vstar_12h += storm.delta_vstar_12h * 0.6

        else:
            # UNFAVORABLE CONDITIONS
            # Decay toward intensity equilibrium
            delta_vstar_12h = (V_STAR_INTENSITY - v_star) * 0.15

        # Land interaction override
        if storm.is_over_land:
            delta_vstar_12h = -0.8 - (v_star - 1.5) * 0.3  # Strong decay

        # MPI ceiling
        predicted_vstar_12h = v_star + delta_vstar_12h
        if predicted_vstar_12h > mpi_vstar:
            delta_vstar_12h = (mpi_vstar - v_star) * 0.8

        # Scale to lead time (with some saturation)
        periods = lead_hours / 12
        # Use diminishing returns for longer lead times
        effective_periods = periods * (1 - 0.1 * (periods - 1))  # Slight decay
        delta_vstar_total = delta_vstar_12h * effective_periods

        # Convert to knots
        delta_vmax = delta_vstar_total * Z_SQUARED
        predicted_vmax = storm.vmax + delta_vmax

        # Enforce physical limits
        predicted_vmax = max(25, min(185, predicted_vmax))

        return {
            'lead_hours': lead_hours,
            'current_vmax': storm.vmax,
            'current_vstar': v_star,
            'predicted_vmax': predicted_vmax,
            'predicted_vstar': predicted_vmax / Z_SQUARED,
            'delta_vmax': delta_vmax,
            'mpi_vstar': mpi_vstar,
            'env_score': env_score
        }

    def generate_v_star_watch(
        self,
        storm: StormState,
        env: EnvironmentFactors
    ) -> Dict:
        """Generate V* Watch advisory."""
        ri_category, ri_prob = self.calculate_ri_potential(storm, env)

        watch = {
            'current_vstar': storm.v_star,
            'current_vmax': storm.vmax,
            'ri_potential': ri_category.value,
            'ri_probability': ri_prob,
            'distance_from_v3': storm.distance_from_structural,
            'environment_score': env.favorable_score,
            'advisories': []
        }

        if storm.v_star < RI_POTENTIAL_THRESHOLD and env.is_favorable:
            watch['advisories'].append({
                'type': 'V* WATCH',
                'level': 'HIGH RI POTENTIAL',
                'message': f"V* = {storm.v_star:.2f} is {storm.distance_from_structural:.2f} below V*=3"
            })

        if storm.delta_vstar_12h and storm.delta_vstar_12h > RI_ACTIVE_RATE:
            watch['advisories'].append({
                'type': 'ACTIVE RI',
                'level': 'IN PROGRESS',
                'message': f"ΔV*/12h = {storm.delta_vstar_12h:.2f}"
            })

        return watch


# =============================================================================
# COMPREHENSIVE HURRICANE DATABASE
# =============================================================================

HURRICANE_DATABASE = {
    # 2024 Season
    'Helene 2024': {
        'category': 4, 'peak_vmax': 140, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 65, 'ri_hours': 48,
        'sst': 30.5, 'shear': 7, 'ohc': 85, 'notable': 'NC flooding disaster'
    },
    'Milton 2024': {
        'category': 5, 'peak_vmax': 180, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 75, 'ri_hours': 24,
        'sst': 31.0, 'shear': 5, 'ohc': 90, 'notable': 'Record RI in Gulf'
    },
    'Beryl 2024': {
        'category': 5, 'peak_vmax': 165, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 60, 'ri_hours': 24,
        'sst': 30.0, 'shear': 6, 'ohc': 75, 'notable': 'Earliest Cat 5 on record'
    },

    # 2023 Season
    'Lee 2023': {
        'category': 5, 'peak_vmax': 165, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 80, 'ri_hours': 24,
        'sst': 29.5, 'shear': 8, 'ohc': 70, 'notable': 'Large wind field'
    },
    'Idalia 2023': {
        'category': 4, 'peak_vmax': 130, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 65, 'ri_hours': 24,
        'sst': 30.5, 'shear': 7, 'ohc': 80, 'notable': 'Big Bend landfall'
    },
    'Otis 2023': {
        'category': 5, 'peak_vmax': 165, 'basin': 'EPAC',
        'ri_event': True, 'ri_start_vmax': 50, 'ri_hours': 12,
        'sst': 31.0, 'shear': 4, 'ohc': 85, 'notable': 'Explosive RI, Acapulco'
    },

    # 2022 Season
    'Ian 2022': {
        'category': 5, 'peak_vmax': 160, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 85, 'ri_hours': 24,
        'sst': 30.0, 'shear': 10, 'ohc': 85, 'notable': 'SW Florida devastation'
    },
    'Fiona 2022': {
        'category': 4, 'peak_vmax': 130, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 75, 'ri_hours': 36,
        'sst': 29.0, 'shear': 12, 'ohc': 70, 'notable': 'Puerto Rico flooding'
    },

    # 2021 Season
    'Ida 2021': {
        'category': 4, 'peak_vmax': 150, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 70, 'ri_hours': 24,
        'sst': 31.0, 'shear': 5, 'ohc': 90, 'notable': 'Louisiana landfall'
    },
    'Sam 2021': {
        'category': 4, 'peak_vmax': 150, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 75, 'ri_hours': 24,
        'sst': 28.5, 'shear': 10, 'ohc': 65, 'notable': 'Long-lived Cape Verde'
    },

    # 2020 Season (record 30 named storms)
    'Laura 2020': {
        'category': 4, 'peak_vmax': 150, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 65, 'ri_hours': 24,
        'sst': 30.5, 'shear': 8, 'ohc': 85, 'notable': 'Lake Charles landfall'
    },
    'Delta 2020': {
        'category': 4, 'peak_vmax': 145, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 60, 'ri_hours': 24,
        'sst': 30.0, 'shear': 10, 'ohc': 75, 'notable': 'Greek alphabet storm'
    },
    'Eta 2020': {
        'category': 4, 'peak_vmax': 150, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 65, 'ri_hours': 36,
        'sst': 29.5, 'shear': 8, 'ohc': 80, 'notable': 'Central America disaster'
    },
    'Iota 2020': {
        'category': 5, 'peak_vmax': 160, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 75, 'ri_hours': 24,
        'sst': 30.0, 'shear': 6, 'ohc': 80, 'notable': 'Nicaragua Cat 5'
    },

    # 2019 Season
    'Dorian 2019': {
        'category': 5, 'peak_vmax': 185, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 85, 'ri_hours': 36,
        'sst': 30.0, 'shear': 5, 'ohc': 80, 'notable': 'Bahamas catastrophe'
    },
    'Lorenzo 2019': {
        'category': 5, 'peak_vmax': 160, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 80, 'ri_hours': 24,
        'sst': 28.5, 'shear': 8, 'ohc': 65, 'notable': 'Easternmost Cat 5'
    },

    # 2018 Season
    'Michael 2018': {
        'category': 5, 'peak_vmax': 160, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 75, 'ri_hours': 48,
        'sst': 29.5, 'shear': 8, 'ohc': 75, 'notable': 'First Cat 5 FL Panhandle'
    },
    'Florence 2018': {
        'category': 4, 'peak_vmax': 140, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 65, 'ri_hours': 48,
        'sst': 28.5, 'shear': 12, 'ohc': 60, 'notable': 'Carolinas flooding'
    },

    # 2017 Season (record damage)
    'Maria 2017': {
        'category': 5, 'peak_vmax': 175, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 80, 'ri_hours': 24,
        'sst': 29.5, 'shear': 5, 'ohc': 75, 'notable': 'Puerto Rico devastation'
    },
    'Irma 2017': {
        'category': 5, 'peak_vmax': 180, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 100, 'ri_hours': 24,
        'sst': 29.0, 'shear': 8, 'ohc': 70, 'notable': 'Peak 185 kt for 37 hrs'
    },
    'Harvey 2017': {
        'category': 4, 'peak_vmax': 130, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 45, 'ri_hours': 48,
        'sst': 30.0, 'shear': 10, 'ohc': 80, 'notable': 'Houston flooding $125B'
    },
    'Jose 2017': {
        'category': 4, 'peak_vmax': 155, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 85, 'ri_hours': 24,
        'sst': 28.5, 'shear': 10, 'ohc': 65, 'notable': 'Loop track'
    },
    'Nate 2017': {
        'category': 1, 'peak_vmax': 90, 'basin': 'ATL',
        'ri_event': False, 'ri_start_vmax': 50, 'ri_hours': 0,
        'sst': 29.0, 'shear': 15, 'ohc': 60, 'notable': 'Central America floods'
    },

    # 2016 Season
    'Matthew 2016': {
        'category': 5, 'peak_vmax': 165, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 75, 'ri_hours': 24,
        'sst': 29.5, 'shear': 7, 'ohc': 75, 'notable': 'Haiti disaster'
    },
    'Nicole 2016': {
        'category': 4, 'peak_vmax': 130, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 70, 'ri_hours': 36,
        'sst': 27.5, 'shear': 12, 'ohc': 55, 'notable': 'Bermuda direct hit'
    },

    # 2015 Season
    'Patricia 2015': {
        'category': 5, 'peak_vmax': 215, 'basin': 'EPAC',
        'ri_event': True, 'ri_start_vmax': 60, 'ri_hours': 24,
        'sst': 31.5, 'shear': 4, 'ohc': 95, 'notable': 'Strongest ever recorded'
    },
    'Joaquin 2015': {
        'category': 4, 'peak_vmax': 155, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 65, 'ri_hours': 36,
        'sst': 28.5, 'shear': 8, 'ohc': 65, 'notable': 'El Faro sinking'
    },

    # Historical Major RI Events
    'Wilma 2005': {
        'category': 5, 'peak_vmax': 185, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 60, 'ri_hours': 24,
        'sst': 30.0, 'shear': 5, 'ohc': 85, 'notable': 'Deepest pressure 882 mb'
    },
    'Katrina 2005': {
        'category': 5, 'peak_vmax': 175, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 75, 'ri_hours': 24,
        'sst': 30.5, 'shear': 8, 'ohc': 90, 'notable': 'New Orleans disaster'
    },
    'Rita 2005': {
        'category': 5, 'peak_vmax': 180, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 70, 'ri_hours': 24,
        'sst': 30.0, 'shear': 6, 'ohc': 85, 'notable': 'Texas Gulf landfall'
    },
    'Dennis 2005': {
        'category': 4, 'peak_vmax': 150, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 65, 'ri_hours': 36,
        'sst': 29.0, 'shear': 10, 'ohc': 70, 'notable': 'Early July major'
    },
    'Isabel 2003': {
        'category': 5, 'peak_vmax': 165, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 85, 'ri_hours': 24,
        'sst': 28.5, 'shear': 8, 'ohc': 65, 'notable': 'Virginia landfall'
    },
    'Ivan 2004': {
        'category': 5, 'peak_vmax': 165, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 80, 'ri_hours': 24,
        'sst': 29.5, 'shear': 7, 'ohc': 75, 'notable': 'Gulf Shores Alabama'
    },
    'Charley 2004': {
        'category': 4, 'peak_vmax': 150, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 85, 'ri_hours': 12,
        'sst': 30.0, 'shear': 8, 'ohc': 75, 'notable': 'Punta Gorda surprise'
    },
    'Frances 2004': {
        'category': 4, 'peak_vmax': 145, 'basin': 'ATL',
        'ri_event': True, 'ri_start_vmax': 70, 'ri_hours': 48,
        'sst': 29.0, 'shear': 10, 'ohc': 70, 'notable': 'Slow mover Florida'
    },
    'Jeanne 2004': {
        'category': 3, 'peak_vmax': 120, 'basin': 'ATL',
        'ri_event': False, 'ri_start_vmax': 65, 'ri_hours': 0,
        'sst': 28.5, 'shear': 12, 'ohc': 60, 'notable': 'Loop in Atlantic'
    },

    # Non-RI comparison storms (unfavorable conditions)
    'Ophelia 2023': {
        'category': 0, 'peak_vmax': 60, 'basin': 'ATL',
        'ri_event': False, 'ri_start_vmax': 35, 'ri_hours': 0,
        'sst': 26.5, 'shear': 20, 'ohc': 40, 'notable': 'High shear limited'
    },
    'Bret 2023': {
        'category': 0, 'peak_vmax': 60, 'basin': 'ATL',
        'ri_event': False, 'ri_start_vmax': 40, 'ri_hours': 0,
        'sst': 27.5, 'shear': 18, 'ohc': 50, 'notable': 'Dry air intrusion'
    },
    'Earl 2022': {
        'category': 1, 'peak_vmax': 90, 'basin': 'ATL',
        'ri_event': False, 'ri_start_vmax': 50, 'ri_hours': 0,
        'sst': 27.0, 'shear': 22, 'ohc': 45, 'notable': 'Shear disruption'
    },
}


def test_comprehensive_validation():
    """Test model against all hurricanes in database."""
    print("=" * 100)
    print("  Z² INTENSITY MODEL v2.0 - COMPREHENSIVE VALIDATION")
    print("=" * 100)

    model = Z2IntensityModelV2()

    results = []
    ri_storms = []
    non_ri_storms = []

    print(f"\n  {'Storm':<20} {'RI?':<5} {'Start':<7} {'Actual':<8} {'Pred':<8} {'Error':<7} {'RI Prob':<9} {'Category'}")
    print("  " + "-" * 95)

    for name, data in HURRICANE_DATABASE.items():
        env = EnvironmentFactors(
            sst=data['sst'],
            shear=data['shear'],
            ohc=data['ohc'],
            rh_mid=70,
            outflow=0.8
        )

        start_vmax = data['ri_start_vmax'] if data['ri_event'] else data.get('ri_start_vmax', 50)
        storm = StormState(
            vmax=start_vmax,
            lat=22.0,
            lon=-85.0,
            mslp=990,
            rmw=25,
            vmax_history=[start_vmax - 15, start_vmax - 5, start_vmax]
        )

        hours = data['ri_hours'] if data['ri_hours'] > 0 else 24
        pred = model.predict_intensity_change(storm, env, hours)
        ri_cat, ri_prob = model.calculate_ri_potential(storm, env)

        actual = data['peak_vmax']
        error = pred['predicted_vmax'] - actual

        result = {
            'name': name,
            'ri_event': data['ri_event'],
            'start_vmax': start_vmax,
            'actual': actual,
            'predicted': pred['predicted_vmax'],
            'error': error,
            'abs_error': abs(error),
            'ri_prob': ri_prob,
            'hours': hours,
            'category': data['category']
        }
        results.append(result)

        if data['ri_event']:
            ri_storms.append(result)
        else:
            non_ri_storms.append(result)

        ri_flag = "YES" if data['ri_event'] else "no"
        cat_str = f"Cat {data['category']}" if data['category'] > 0 else "TS"
        print(f"  {name:<20} {ri_flag:<5} {start_vmax:<7} {actual:<8} {pred['predicted_vmax']:<8.0f} {error:>+6.0f}  {ri_prob:<9.1%} {cat_str}")

    # Statistics
    print("\n" + "=" * 100)
    print("  SUMMARY STATISTICS")
    print("=" * 100)

    all_errors = [r['abs_error'] for r in results]
    ri_errors = [r['abs_error'] for r in ri_storms]
    non_ri_errors = [r['abs_error'] for r in non_ri_storms] if non_ri_storms else [0]

    print(f"\n  Overall Performance (n={len(results)}):")
    print(f"  - Mean Absolute Error: {np.mean(all_errors):.1f} kt")
    print(f"  - Median Error: {np.median(all_errors):.1f} kt")
    print(f"  - Std Dev: {np.std(all_errors):.1f} kt")
    print(f"  - Min/Max Error: {min(all_errors):.0f} / {max(all_errors):.0f} kt")

    print(f"\n  RI Storms Only (n={len(ri_storms)}):")
    print(f"  - Mean Absolute Error: {np.mean(ri_errors):.1f} kt")
    print(f"  - Median Error: {np.median(ri_errors):.1f} kt")

    # RI Detection Analysis
    print(f"\n  RI DETECTION ANALYSIS:")
    high_ri_prob = [r for r in ri_storms if r['ri_prob'] > 0.5]
    correct_ri_detect = len(high_ri_prob)
    print(f"  - RI storms with P(RI) > 50%: {correct_ri_detect}/{len(ri_storms)} ({100*correct_ri_detect/len(ri_storms):.0f}%)")

    low_ri_prob = [r for r in non_ri_storms if r['ri_prob'] < 0.3]
    correct_non_ri = len(low_ri_prob)
    if non_ri_storms:
        print(f"  - Non-RI storms with P(RI) < 30%: {correct_non_ri}/{len(non_ri_storms)} ({100*correct_non_ri/len(non_ri_storms):.0f}%)")

    # Bias analysis
    underpredict = [r for r in ri_storms if r['error'] < -20]
    overpredict = [r for r in ri_storms if r['error'] > 20]
    print(f"\n  BIAS ANALYSIS (RI storms):")
    print(f"  - Underpredicted by >20kt: {len(underpredict)}/{len(ri_storms)}")
    print(f"  - Overpredicted by >20kt: {len(overpredict)}/{len(ri_storms)}")

    # NHC comparison
    print(f"\n  COMPARISON TO NHC BENCHMARKS:")
    print(f"  - NHC 24h intensity error: ~11 kt (operational)")
    print(f"  - NHC 48h intensity error: ~16 kt")
    print(f"  - Z² v2.0 mean error: {np.mean(all_errors):.1f} kt")

    # By category
    print(f"\n  ERROR BY PEAK CATEGORY:")
    for cat in range(1, 6):
        cat_storms = [r for r in ri_storms if r['category'] == cat]
        if cat_storms:
            cat_error = np.mean([r['abs_error'] for r in cat_storms])
            print(f"  - Cat {cat}: {cat_error:.1f} kt (n={len(cat_storms)})")

    return results


if __name__ == "__main__":
    results = test_comprehensive_validation()

    print("\n" + "=" * 100)
    print("  TOP 10 WORST PREDICTIONS (for model improvement)")
    print("=" * 100)

    sorted_results = sorted(results, key=lambda x: x['abs_error'], reverse=True)
    for r in sorted_results[:10]:
        print(f"  {r['name']:<20} Error: {r['error']:+.0f} kt (Predicted {r['predicted']:.0f}, Actual {r['actual']})")
