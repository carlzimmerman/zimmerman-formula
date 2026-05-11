# Z² Framework Constants for xdiag Simulations
# =============================================
# Author: Zimmerman Formula Research
# xdiag Library Credit: Alexander Wietek (Apache 2.0)

module Z2Constants

export Z2, Z, BEKENSTEIN, GAUGE, N_GEN, ALPHA_INV
export PARITY_SUPPRESSION, SHEAR_ANGLE, VACUUM_RATIO

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================

"""
    Z2 = 32π/3 ≈ 33.5103216383

The fundamental geometric constant from cube/sphere geometry.
Emerges from Friedmann equation + Bekenstein-Hawking entropy.
"""
const Z2 = 32 * π / 3  # = 33.5103216383

"""
    Z = √(32π/3) ≈ 5.7888311871

Square root of Z², appears in many derived quantities.
"""
const Z = sqrt(Z2)  # = 5.7888311871

# =============================================================================
# CUBE STRUCTURE CONSTANTS
# =============================================================================

"""BEKENSTEIN = 4: Body diagonals of cube, appears in S = A/(4ℓ_P²)"""
const BEKENSTEIN = 4

"""GAUGE = 12: Edges of cube, dimension of SU(3)×SU(2)×U(1)"""
const GAUGE = 12

"""N_GEN = 3: Face pairs of cube, number of fermion generations"""
const N_GEN = 3

# =============================================================================
# DERIVED CONSTANTS
# =============================================================================

"""α⁻¹ = 4Z² + 3 = 137.04: Inverse fine structure constant"""
const ALPHA_INV = 4 * Z2 + 3  # = 137.0412865532

"""S = 3/110: Parity suppression factor for tensor modes"""
const PARITY_SUPPRESSION = 3 / 110  # = 0.02727...

"""θ = arctan(1/√2) ≈ 35.26°: Topological shear angle"""
const SHEAR_ANGLE = atan(1 / sqrt(2))  # radians
const SHEAR_ANGLE_DEG = rad2deg(SHEAR_ANGLE)  # = 35.264...°

"""13:19 vacuum partition ratio"""
const VACUUM_RATIO = 13 / 19  # = 0.6842... (Ω_Λ)
const MATTER_RATIO = 6 / 19   # = 0.3158... (Ω_m)

# =============================================================================
# LATTICE PARAMETERS FOR M4 64GB
# =============================================================================

"""Maximum lattice size for 40GB memory limit"""
const MAX_SITES_1D = 30
const MAX_SITES_2D = 25  # 5×5 = 25 sites
const MAX_SITES_3D = 27  # 3×3×3 = 27 sites

"""
Hilbert space dimension estimates:
- 24 sites: 2^24 = 16.7M states, ~130 MB per vector
- 28 sites: 2^28 = 268M states, ~2 GB per vector
- 30 sites: 2^30 = 1.07B states, ~8 GB per vector
Lanczos needs ~3-5 vectors, so 30 sites ≈ 24-40 GB
"""

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

"""Print all Z² constants"""
function print_constants()
    println("=" ^ 50)
    println("Z² FRAMEWORK CONSTANTS")
    println("=" ^ 50)
    println("Z² = 32π/3 = $(Z2)")
    println("Z  = √(Z²) = $(Z)")
    println()
    println("Cube Structure:")
    println("  BEKENSTEIN = $(BEKENSTEIN)")
    println("  GAUGE      = $(GAUGE)")
    println("  N_GEN      = $(N_GEN)")
    println()
    println("Derived:")
    println("  α⁻¹ = 4Z² + 3 = $(ALPHA_INV)")
    println("  Parity suppression = 3/110 = $(PARITY_SUPPRESSION)")
    println("  Shear angle = $(SHEAR_ANGLE_DEG)°")
    println("  Ω_Λ = 13/19 = $(VACUUM_RATIO)")
    println("=" ^ 50)
end

end # module
