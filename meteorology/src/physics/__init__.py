# Physics modules for weather prediction
from .conservation import (
    mass_conservation_loss,
    energy_conservation_loss,
    divergence_penalty,
    physical_bounds_loss,
)
from .atmospheric import (
    compute_geopotential_height,
    compute_potential_temperature,
    compute_virtual_temperature,
    compute_saturation_vapor_pressure,
)
