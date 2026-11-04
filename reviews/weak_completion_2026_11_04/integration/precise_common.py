"""Common vector-aware gas with the frozen tightened action-energy inversion."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'energy'))
from precise_orbit import GenericOrbit as PreciseCore
from common import CommonOrbit
class PreciseCommonOrbit(CommonOrbit):
 orbit=PreciseCore.orbit
