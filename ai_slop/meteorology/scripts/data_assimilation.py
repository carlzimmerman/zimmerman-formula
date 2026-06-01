"""
DATA ASSIMILATION: First-Principles Physics
=============================================

Mathematical foundations of combining observations with models
to create optimal atmospheric state estimates.

Topics:
- Bayes' theorem foundation
- Optimal interpolation
- 3D-VAR and 4D-VAR
- Ensemble Kalman Filter
- Observation operators
- Error covariances

Author: Carl Zimmerman
Framework: Z² = 32π/3 hurricane intensity research
"""

import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("DATA ASSIMILATION: First-Principles Physics")
print("=" * 70)

# =============================================================================
# PART 1: THE ANALYSIS PROBLEM
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: THE ANALYSIS PROBLEM")
print("=" * 70)

print("""
HYPOTHESIS: The best estimate of atmospheric state combines model predictions
and observations, weighted by their respective uncertainties.

THE FUNDAMENTAL PROBLEM:

Given:
1. Background (prior forecast): x_b with error covariance B
2. Observations: y with error covariance R
3. Observation operator: H (maps state to observation space)

Find:
Analysis (posterior): x_a that minimizes expected error

BAYESIAN FRAMEWORK:

Bayes' theorem:
    P(x|y) ∝ P(y|x) × P(x)

    posterior ∝ likelihood × prior

For Gaussian errors:
    P(x) = exp[-½(x - x_b)ᵀ B⁻¹ (x - x_b)]          (prior)
    P(y|x) = exp[-½(y - Hx)ᵀ R⁻¹ (y - Hx)]          (likelihood)

The posterior is maximized when we minimize the COST FUNCTION:

    J(x) = ½(x - x_b)ᵀ B⁻¹ (x - x_b) + ½(y - Hx)ᵀ R⁻¹ (y - Hx)
           └─────────── J_b ──────────┘   └─────────── J_o ───────────┘
           background term                observation term

This is the fundamental equation of variational data assimilation.
""")

def cost_function_1d(x, x_b, y, H, sigma_b, sigma_o):
    """
    1D cost function for variational data assimilation.

    J = (x - x_b)²/(2σ_b²) + (y - Hx)²/(2σ_o²)
    """
    J_b = (x - x_b)**2 / (2 * sigma_b**2)
    J_o = (y - H * x)**2 / (2 * sigma_o**2)
    return J_b + J_o

# Demonstrate cost function
print("\nCost Function Example:")
print("-" * 50)
x_b = 20.0  # Background: 20°C
y = 22.0   # Observation: 22°C
H = 1.0    # Direct observation
sigma_b = 2.0  # Background error: 2°C
sigma_o = 1.0  # Observation error: 1°C

x_values = np.linspace(18, 24, 100)
J_values = [cost_function_1d(x, x_b, y, H, sigma_b, sigma_o) for x in x_values]

# Find minimum
x_a = x_values[np.argmin(J_values)]
print(f"Background: {x_b}°C (σ = {sigma_b}°C)")
print(f"Observation: {y}°C (σ = {sigma_o}°C)")
print(f"Analysis (minimum J): {x_a:.2f}°C")

# =============================================================================
# PART 2: OPTIMAL INTERPOLATION (OI)
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: OPTIMAL INTERPOLATION")
print("=" * 70)

print("""
HYPOTHESIS: For linear observation operators and Gaussian errors, the
analysis has an explicit analytical solution.

DERIVATION:

Setting ∂J/∂x = 0:
    B⁻¹(x - x_b) + Hᵀ R⁻¹(Hx - y) = 0

Solving for x:
    x_a = x_b + K(y - Hx_b)

Where K is the KALMAN GAIN MATRIX:
    K = BHᵀ(HBHᵀ + R)⁻¹

INTERPRETATION:
- (y - Hx_b) is the INNOVATION (observation minus background)
- K weights the innovation by relative errors
- If σ_b >> σ_o: K → H⁻¹, trust observations
- If σ_o >> σ_b: K → 0, trust background

ANALYSIS ERROR COVARIANCE:
    P_a = (I - KH)B

The analysis is ALWAYS better than the background (trace reduces).

1D SCALAR CASE:
    K = σ_b² / (σ_b² + σ_o²)
    x_a = x_b + K(y - x_b)
    σ_a² = (1 - K)σ_b²
""")

def kalman_gain_1d(sigma_b, sigma_o):
    """1D Kalman gain K = σ_b² / (σ_b² + σ_o²)"""
    return sigma_b**2 / (sigma_b**2 + sigma_o**2)

def analysis_1d(x_b, y, sigma_b, sigma_o):
    """
    1D analysis using optimal interpolation.
    """
    K = kalman_gain_1d(sigma_b, sigma_o)
    x_a = x_b + K * (y - x_b)
    sigma_a = np.sqrt((1 - K) * sigma_b**2)
    return x_a, sigma_a, K

# Demonstration
print("\nOptimal Interpolation Results:")
print("-" * 50)
x_a, sigma_a, K = analysis_1d(x_b, y, sigma_b, sigma_o)
print(f"Kalman gain K = {K:.3f}")
print(f"Analysis: {x_a:.2f}°C")
print(f"Analysis error: {sigma_a:.2f}°C")
print(f"Error reduction: {(1 - sigma_a/sigma_b)*100:.1f}%")

# Show behavior for different error ratios
print("\nKalman Gain vs Error Ratio:")
print("-" * 50)
print(f"{'σ_b/σ_o':<12} {'K':<12} {'Weight on obs'}")
print("-" * 50)
for ratio in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
    K = kalman_gain_1d(ratio, 1.0)
    print(f"{ratio:<12.1f} {K:<12.3f} {K*100:.1f}%")

# =============================================================================
# PART 3: 3D-VAR (Three-Dimensional Variational)
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: 3D-VAR")
print("=" * 70)

print("""
HYPOTHESIS: For large systems (millions of variables), iterative minimization
of the cost function is more practical than direct matrix inversion.

3D-VAR ALGORITHM:

1. Start with x = x_b (background as first guess)
2. Compute cost function J(x) and gradient ∇J(x)
3. Use conjugate gradient or quasi-Newton to update x
4. Repeat until convergence

GRADIENT OF COST FUNCTION:
    ∇J = B⁻¹(x - x_b) + Hᵀ R⁻¹(Hx - y)

KEY MATRICES:

B (Background Error Covariance):
- Size: n × n where n ~ 10⁸ (state dimension)
- Cannot store explicitly!
- Model as correlation × variance: B = Σ C Σ
- Use recursive filters or spectral transforms

R (Observation Error Covariance):
- Size: m × m where m ~ 10⁶ (observation count)
- Often assumed diagonal (uncorrelated errors)
- Includes measurement + representativeness errors

H (Observation Operator):
- Maps model state to observation space
- Can be nonlinear (H → H(x))
- Examples: interpolation, radiative transfer, etc.

PRACTICAL IMPLEMENTATION:
- Use incremental formulation: δx = x - x_b
- Transform to uncorrelated variables: ξ = B^(-1/2) δx
- Multiple outer loops for nonlinearity
""")

def gradient_descent_3dvar(x_b, y, H, B_inv, R_inv, alpha=0.1, n_iter=100):
    """
    Simple gradient descent for 3D-VAR cost function.

    For demonstration - real systems use conjugate gradient.
    """
    x = x_b.copy()

    for i in range(n_iter):
        # Compute gradient
        grad_Jb = B_inv @ (x - x_b)
        grad_Jo = H.T @ R_inv @ (H @ x - y)
        grad = grad_Jb + grad_Jo

        # Update
        x = x - alpha * grad

        # Check convergence
        if np.linalg.norm(grad) < 1e-6:
            break

    return x

# 2D example
print("\n2D 3D-VAR Example:")
print("-" * 50)

n = 2  # State dimension
m = 2  # Observation dimension

# Background and observations
x_b = np.array([20.0, 1010.0])  # Temperature, Pressure
y = np.array([22.0, 1008.0])   # Observations

# Error covariances (diagonal for simplicity)
B = np.diag([4.0, 16.0])  # σ_T = 2°C, σ_p = 4 hPa
R = np.diag([1.0, 4.0])   # σ_T = 1°C, σ_p = 2 hPa

B_inv = np.linalg.inv(B)
R_inv = np.linalg.inv(R)
H = np.eye(2)  # Direct observations

# Run 3D-VAR
x_a = gradient_descent_3dvar(x_b, y, H, B_inv, R_inv)

print(f"Background: T = {x_b[0]:.1f}°C, p = {x_b[1]:.1f} hPa")
print(f"Observation: T = {y[0]:.1f}°C, p = {y[1]:.1f} hPa")
print(f"Analysis: T = {x_a[0]:.1f}°C, p = {x_a[1]:.1f} hPa")

# =============================================================================
# PART 4: 4D-VAR (Four-Dimensional Variational)
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: 4D-VAR")
print("=" * 70)

print("""
HYPOTHESIS: Including time evolution in the cost function allows observations
at different times to constrain the analysis.

4D-VAR COST FUNCTION:

    J(x₀) = ½(x₀ - x_b)ᵀ B⁻¹ (x₀ - x_b)
          + ½ Σᵢ (yᵢ - Hᵢ xᵢ)ᵀ Rᵢ⁻¹ (yᵢ - Hᵢ xᵢ)

Where:
- x₀ = initial state at t = 0
- xᵢ = M₀→ᵢ(x₀) = state at time tᵢ from model propagation
- M = nonlinear model

GRADIENT COMPUTATION:

To find ∂J/∂x₀, we need the ADJOINT MODEL M*:

    ∇ₓ₀ J = B⁻¹(x₀ - x_b) + Σᵢ Mᵢ→₀* Hᵢᵀ Rᵢ⁻¹(Hᵢ xᵢ - yᵢ)

The adjoint integrates BACKWARD in time, propagating sensitivities.

ADVANTAGES OF 4D-VAR:
1. Uses observations at correct time (no need for time interpolation)
2. Implicitly accounts for flow-dependent error correlations
3. Produces dynamically consistent analysis
4. Can use all observations in assimilation window (typically 6-12 hours)

DISADVANTAGES:
1. Requires adjoint model (significant development effort)
2. Computationally expensive (~3-5× forward model)
3. Difficult to estimate flow-dependent B

OPERATIONAL USE:
ECMWF uses 4D-VAR with 12-hour windows
NCEP uses hybrid 4D-EnVar (ensemble-variational)
""")

def forward_model_simple(x, dt, n_steps):
    """
    Simple forward model: exponential decay toward equilibrium.
    x(t+dt) = x(t) + dt * k * (x_eq - x(t))
    """
    k = 0.1  # Relaxation rate
    x_eq = 15.0  # Equilibrium

    trajectory = [x]
    for i in range(n_steps):
        x = x + dt * k * (x_eq - x)
        trajectory.append(x)
    return np.array(trajectory)

def adjoint_model_simple(lambda_final, x_trajectory, dt):
    """
    Adjoint of simple forward model (integrates backward).
    """
    k = 0.1
    n_steps = len(x_trajectory) - 1

    lambda_traj = [lambda_final]
    lam = lambda_final

    for i in range(n_steps - 1, -1, -1):
        # Adjoint equation (backward)
        lam = lam * (1 - dt * k)
        lambda_traj.insert(0, lam)

    return np.array(lambda_traj)

# 4D-VAR demonstration
print("\n4D-VAR Schematic:")
print("-" * 50)
print("""
Time:      t₀=0        t₁=3h       t₂=6h       t₃=9h       t₄=12h
           |-----------|-----------|-----------|-----------|
State:     x₀ ───M───> x₁ ───M───> x₂ ───M───> x₃ ───M───> x₄
           ↑           ↓           ↓                       ↓
Obs:      x_b          y₁          y₂                      y₄

Forward pass: Integrate model, compute innovations
Backward pass: Adjoint propagates sensitivities to x₀
Update x₀ and repeat until converged
""")

# =============================================================================
# PART 5: ENSEMBLE KALMAN FILTER (EnKF)
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: ENSEMBLE KALMAN FILTER")
print("=" * 70)

print("""
HYPOTHESIS: Background error covariance can be estimated from an ensemble
of forecasts, avoiding the need for explicit B matrix specification.

EnKF ALGORITHM:

1. FORECAST STEP:
   For each ensemble member k = 1, ..., N_e:
       x_k^f = M(x_k^a)
   (Propagate previous analysis ensemble through model)

2. Estimate background mean and covariance:
       x̄^f = (1/N_e) Σ x_k^f
       P^f ≈ (1/(N_e-1)) Σ (x_k^f - x̄^f)(x_k^f - x̄^f)ᵀ

3. ANALYSIS STEP:
   Compute Kalman gain:
       K = P^f Hᵀ (H P^f Hᵀ + R)⁻¹

   Update each member with perturbed observations:
       x_k^a = x_k^f + K(y + ε_k - H x_k^f)

   Where ε_k ~ N(0, R) maintains correct variance.

ADVANTAGES:
1. Flow-dependent error covariances (automatically!)
2. No adjoint model needed
3. Naturally provides ensemble for probabilistic forecasting
4. Parallelizable (each member independent)

CHALLENGES:
1. Sampling error with finite ensemble (N_e ~ 50-100)
2. Need LOCALIZATION to reduce spurious correlations
3. INFLATION needed to prevent filter divergence

LOCALIZATION:
    K_local = ρ ∘ K     (element-wise product with correlation function)

    ρ(d) = Gaspari-Cohn function, zero beyond cutoff distance

OPERATIONAL USE:
NCEP GDAS uses EnKF for ensemble generation
Many centers use hybrid EnKF-VAR
""")

def enkf_analysis(X_f, y, H, R, localization=None):
    """
    Ensemble Kalman Filter analysis step.

    X_f: N_state × N_ens forecast ensemble
    y: observations
    H: observation operator (matrix)
    R: observation error covariance
    """
    N_state, N_ens = X_f.shape

    # Ensemble mean and perturbations
    x_mean = np.mean(X_f, axis=1)
    X_pert = X_f - x_mean[:, np.newaxis]

    # Sample covariance (in observation space)
    HX = H @ X_f
    HX_mean = np.mean(HX, axis=1)
    HX_pert = HX - HX_mean[:, np.newaxis]

    # P^f H^T and H P^f H^T
    PfHT = X_pert @ HX_pert.T / (N_ens - 1)
    HPfHT = HX_pert @ HX_pert.T / (N_ens - 1)

    # Kalman gain
    K = PfHT @ np.linalg.inv(HPfHT + R)

    # Perturbed observations (maintaining R variance)
    y_pert = y[:, np.newaxis] + np.random.multivariate_normal(
        np.zeros(len(y)), R, N_ens).T

    # Analysis ensemble
    X_a = X_f + K @ (y_pert - HX)

    return X_a

# EnKF demonstration
print("\nEnKF Example:")
print("-" * 50)

N_state = 3   # State dimension
N_ens = 50    # Ensemble size
N_obs = 2     # Observation count

# Generate forecast ensemble
x_truth = np.array([20.0, 1010.0, 50.0])  # T, p, RH
ensemble_spread = np.array([2.0, 4.0, 10.0])
X_f = x_truth[:, np.newaxis] + ensemble_spread[:, np.newaxis] * np.random.randn(N_state, N_ens)

# Observations (with error)
H = np.array([[1, 0, 0], [0, 1, 0]])  # Observe T and p only
R = np.diag([1.0, 4.0])
y_true = H @ x_truth
y = y_true + np.array([0.5, -1.0])  # Add some "error" simulating obs

# Run EnKF
X_a = enkf_analysis(X_f, y, H, R)

print(f"Truth: T={x_truth[0]:.1f}°C, p={x_truth[1]:.1f} hPa, RH={x_truth[2]:.1f}%")
print(f"Observations: T={y[0]:.1f}°C, p={y[1]:.1f} hPa")
print(f"Forecast mean: T={np.mean(X_f[0]):.1f}±{np.std(X_f[0]):.1f}°C")
print(f"Analysis mean: T={np.mean(X_a[0]):.1f}±{np.std(X_a[0]):.1f}°C")
print(f"(RH unobserved): Forecast={np.mean(X_f[2]):.1f}±{np.std(X_f[2]):.1f}%")
print(f"(RH unobserved): Analysis={np.mean(X_a[2]):.1f}±{np.std(X_a[2]):.1f}%")

# =============================================================================
# PART 6: OBSERVATION OPERATORS
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: OBSERVATION OPERATORS")
print("=" * 70)

print("""
HYPOTHESIS: Observations measure quantities related to, but not identical to,
model state variables. The observation operator H(x) maps state to observables.

TYPES OF OBSERVATION OPERATORS:

1. DIRECT OBSERVATIONS:
   H(x) = interpolation from model grid
   Example: Surface temperature from synoptic stations

2. INTEGRATED OBSERVATIONS:
   H(x) = ∫ K(z) × x(z) dz
   Example: Satellite radiances (integrate through atmosphere)

3. DERIVED QUANTITIES:
   H(x) = f(x₁, x₂, ...)
   Example: Wind speed from u, v components

SATELLITE RADIANCE OBSERVATIONS:

The forward model for infrared radiance:
    R(ν) = ∫₀^∞ B(ν, T(z)) × ∂τ(ν,z)/∂z dz + τ_sfc × B(ν, T_sfc)

Where:
- B(ν, T) = Planck function
- τ(ν, z) = transmittance from z to satellite
- Depends on T(z), q(z), O₃(z), etc.

This is HIGHLY NONLINEAR!
- Use tangent linear approximation: δR = ∂R/∂x × δx
- Jacobians computed by finite difference or adjoint

GPS RADIO OCCULTATION:

Observes bending angle α as function of impact parameter:
    α(a) = -2a ∫_a^∞ (dn/dr) / √(n²r² - a²) dr

Related to refractivity N = (n-1) × 10⁶ ≈ 77.6 p/T + 3.73×10⁵ e/T²

Very valuable because:
- All-weather (not affected by clouds)
- High vertical resolution
- No instrument drift
""")

def interpolate_bilinear(field, x_frac, y_frac, i, j):
    """
    Bilinear interpolation observation operator.
    """
    val = (1-x_frac) * (1-y_frac) * field[i, j] + \
          x_frac * (1-y_frac) * field[i+1, j] + \
          (1-x_frac) * y_frac * field[i, j+1] + \
          x_frac * y_frac * field[i+1, j+1]
    return val

def radiative_transfer_simple(T_profile, p_profile, absorber_profile):
    """
    Simplified radiative transfer for demonstration.
    Compute upwelling radiance at TOA.
    """
    n_levels = len(T_profile)
    tau = np.zeros(n_levels)  # Optical depth

    # Simple Beer-Lambert absorption
    for k in range(1, n_levels):
        dp = p_profile[k-1] - p_profile[k]
        tau[k] = tau[k-1] + 0.001 * absorber_profile[k] * dp

    # Transmittance
    transmittance = np.exp(-tau)

    # Planck function (simplified)
    B = 5.67e-8 * T_profile**4 / np.pi

    # Integrate upward
    radiance = 0
    for k in range(n_levels - 1):
        dT_dz = transmittance[k] - transmittance[k+1]
        radiance += B[k] * dT_dz

    return radiance

print("\nObservation Types in Modern DA:")
print("-" * 60)
print(f"{'Type':<25} {'Count/day':<15} {'Coverage'}")
print("-" * 60)
print(f"{'Surface synop':<25} {'~20,000':<15} {'Land, limited ocean'}")
print(f"{'Radiosondes':<25} {'~1,500':<15} {'Land, 00/12Z'}")
print(f"{'Aircraft (AMDAR)':<25} {'~300,000':<15} {'Flight corridors'}")
print(f"{'Satellite radiances':<25} {'~10,000,000':<15} {'Global'}")
print(f"{'Atmospheric Motion Vec':<25} {'~500,000':<15} {'Tropics + clouds'}")
print(f"{'GPS-RO':<25} {'~30,000':<15} {'Global, all-weather'}")
print(f"{'Scatterometer winds':<25} {'~1,000,000':<15} {'Ocean surface'}")

# =============================================================================
# PART 7: ERROR COVARIANCE MODELING
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: ERROR COVARIANCE MODELING")
print("=" * 70)

print("""
HYPOTHESIS: Background error covariances have physically-based structure
that can be modeled efficiently without storing full matrices.

BACKGROUND ERROR COVARIANCE B:

For n ~ 10⁸ state variables, B is 10⁸ × 10⁸ ≈ 10¹⁶ elements!
Cannot store explicitly. Must model structure.

STRUCTURE OF B:

B = Σ C Σ

Where:
- Σ = diagonal standard deviation matrix
- C = correlation matrix (spatial/multivariate)

CORRELATION MODELING:

Horizontal correlations: Gaussian or Gaspari-Cohn
    ρ(r) = exp(-r²/2L²)

Vertical correlations: Depend on variable
- Temperature: Strong vertical correlation
- Wind: Weaker vertical correlation

BALANCE CONSTRAINTS:

Physical relationships reduce effective B:
- Geostrophic balance: ψ ↔ (u, v)
- Hydrostatic balance: T ↔ Φ
- Equation of state: T, p, ρ

B = K × B_u × Kᵀ

Where K is a balance operator and B_u is for unbalanced variables.

IMPLEMENTATION:

1. NMC Method: B from forecast differences at different lead times
   B ≈ E[(x_48h - x_24h)(x_48h - x_24h)ᵀ]

2. Ensemble Method: B from ensemble spread
   B ≈ (1/(N-1)) Σ (x_k - x̄)(x_k - x̄)ᵀ

3. Hybrid: Combine static and ensemble-based B
   B = α B_static + (1-α) B_ensemble
""")

def gaspari_cohn(r, L):
    """
    Gaspari-Cohn correlation function (compact support).
    Goes to zero at r = 2L.
    """
    c = L / np.sqrt(0.3)
    r_norm = np.abs(r) / c

    rho = np.zeros_like(r)

    # 0 ≤ r/c ≤ 1
    mask1 = r_norm <= 1
    z = r_norm[mask1]
    rho[mask1] = 1 - 5/3*z**2 + 5/8*z**3 + 1/2*z**4 - 1/4*z**5

    # 1 < r/c ≤ 2
    mask2 = (r_norm > 1) & (r_norm <= 2)
    z = r_norm[mask2]
    rho[mask2] = 4 - 5*z + 5/3*z**2 + 5/8*z**3 - 1/2*z**4 + 1/12*z**5 - 2/(3*z)

    return rho

# Demonstrate correlation functions
print("\nCorrelation Functions:")
print("-" * 50)
print(f"{'Distance (km)':<18} {'Gaussian':<15} {'Gaspari-Cohn'}")
print("-" * 50)

L = 500  # Correlation length scale (km)
distances = np.array([0, 100, 250, 500, 750, 1000, 1500])

for d in distances:
    gauss = np.exp(-d**2 / (2 * L**2))
    gc = gaspari_cohn(np.array([d]), L)[0]
    print(f"{d:<18} {gauss:<15.3f} {gc:<.3f}")

# =============================================================================
# PART 8: DATA ASSIMILATION FOR HURRICANES
# =============================================================================
print("\n" + "=" * 70)
print("PART 8: DATA ASSIMILATION FOR HURRICANES")
print("=" * 70)

print("""
HYPOTHESIS: Hurricane prediction benefits from specialized data assimilation
that accounts for the unique structure of tropical cyclones.

CHALLENGES:

1. SPARSE OBSERVATIONS:
   - Reconnaissance aircraft limited
   - Satellite has cloud contamination
   - Few surface observations over ocean

2. NONLINEAR DYNAMICS:
   - Rapid intensification
   - Eye wall replacement cycles
   - Interaction with environment

3. SCALE INTERACTIONS:
   - Vortex scale: ~100 km
   - Convective scale: ~10 km
   - Need to resolve both

SPECIALIZED TECHNIQUES:

1. VORTEX INITIALIZATION:
   - Bogus vortex insertion
   - Vortex relocation to observed position
   - Blend observed wind profile with environment

2. ADAPTIVE OBSERVATIONS:
   - Target sensitive regions (upstream trough)
   - Reconnaissance missions
   - Dropsondes at strategic locations

3. SATELLITE DATA:
   - Microwave sounders (see through clouds)
   - Scatterometer (surface winds, rain contamination)
   - ADT (Advanced Dvorak Technique for intensity)

4. ENSEMBLE SENSITIVITY:
   - Identify regions where observation impact is large
   - Guide reconnaissance patterns

IMPROVEMENT:
Track forecasts: ~15% improvement from DA per decade
Intensity forecasts: ~5% improvement (harder!)

The Z² = 32π/3 framework suggests intensity is controlled by
thermodynamic efficiency - need better SST, outflow observations.
""")

def relocate_vortex(field_2d, old_center, new_center, vortex_radius):
    """
    Simple vortex relocation demonstration.
    Shift vortex from old_center to new_center.
    """
    # In practice, this involves:
    # 1. Extract vortex from background
    # 2. Interpolate environment without vortex
    # 3. Add vortex at observed location
    pass

print("\nHurricane Observation Sources:")
print("-" * 60)
print(f"{'Source':<25} {'Frequency':<20} {'Variables'}")
print("-" * 60)
print(f"{'Recon aircraft':<25} {'2-3× daily (if avail)':<20} {'p, T, wind profile'}")
print(f"{'Dropsondes':<25} {'~20 per mission':<20} {'Full sounding'}")
print(f"{'Satellite IR':<25} {'15 min':<20} {'Cloud top T'}")
print(f"{'Satellite MW':<25} {'~3-4× daily':<20} {'T profile, rain'}")
print(f"{'Scatterometer':<25} {'~2× daily':<20} {'Surface wind'}")
print(f"{'Buoys/ships':<25} {'Hourly':<20} {'p, T, wind, SST'}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("DATA ASSIMILATION: SUMMARY")
print("=" * 70)

print("""
FUNDAMENTAL RESULTS:

1. BAYESIAN FOUNDATION:
   posterior ∝ likelihood × prior
   Leads to minimization of cost function J(x)

2. OPTIMAL INTERPOLATION:
   x_a = x_b + K(y - Hx_b)
   K = BHᵀ(HBHᵀ + R)⁻¹
   Weights by inverse error variance

3. 3D-VAR:
   Minimizes J(x) iteratively
   Practical for large systems
   Uses modeled B matrix

4. 4D-VAR:
   Includes time evolution
   Requires adjoint model
   Used by ECMWF (gold standard)

5. ENSEMBLE KALMAN FILTER:
   Flow-dependent B from ensemble spread
   No adjoint needed
   Sampling error requires localization

6. OBSERVATION OPERATORS:
   Map model state to observable quantities
   Range from simple interpolation to complex RT

7. ERROR COVARIANCES:
   Cannot store full B matrix
   Model as correlations × variances
   Physical balance constraints

8. HURRICANE DA:
   Sparse observations over ocean
   Vortex initialization critical
   Adaptive observations help

Z² = 32π/3 CONNECTION:
Data assimilation provides the initial conditions for hurricane
intensity prediction. Better DA of thermodynamic structure
(temperature, moisture) and air-sea fluxes directly improves
intensity forecasts through the Z² efficiency relationship.
""")

print("\nScript completed successfully.")
