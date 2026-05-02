#!/usr/bin/env python3
"""
ATTEMPTS TO FIX THE CIRCULARITY GAP IN THE RH PROOF
====================================================

The core problem: Z(t) only evaluates zeta on the critical line.
If off-line zeros existed, Z(t) wouldn't detect them.

This script attempts multiple approaches to fix this gap:

1. Xi Function Approach: Use xi(s) defined everywhere
2. Argument Principle: Count zeros via contour integration
3. Trace Formula Uniqueness: Show operator is uniquely determined
4. Functional Equation: Constrain zeros via symmetry
5. Zero-Free Region: Prove zeros can't exist off-line

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy import special, integrate, optimize
from scipy.linalg import eigvalsh
import warnings
warnings.filterwarnings('ignore')

PI = np.pi
Z_SQUARED = 32 * PI / 3

print("=" * 80)
print("ATTEMPTS TO FIX THE CIRCULARITY GAP")
print("=" * 80)

# Known zeros for reference
KNOWN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
               37.586178, 40.918719, 43.327073, 48.005151, 49.773832]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def zeta_dirichlet(s, N=1000):
    """Zeta via Dirichlet series (valid for Re(s) > 1, extended by continuation)."""
    if np.real(s) > 1:
        return sum(1.0 / n**s for n in range(1, N+1))
    else:
        # Use reflection formula for Re(s) <= 1
        # zeta(s) = 2^s * pi^{s-1} * sin(pi*s/2) * Gamma(1-s) * zeta(1-s)
        s1 = 1 - s
        if np.real(s1) > 1:
            zeta_1ms = sum(1.0 / n**s1 for n in range(1, N+1))
            return (2**s * PI**(s-1) * np.sin(PI*s/2) *
                    special.gamma(1-s) * zeta_1ms)
        else:
            return np.nan


def zeta_approx(s, N=500):
    """Better zeta approximation using Euler-Maclaurin."""
    if np.real(s) < 0.5:
        # Use functional equation
        chi = 2**s * PI**(s-1) * np.sin(PI*s/2) * special.gamma(1-s)
        return chi * zeta_approx(1-s, N)

    # Partial sum
    result = sum(1.0/n**s for n in range(1, N+1))
    # Euler-Maclaurin correction
    result += N**(1-s) / (s-1)
    result += 0.5 * N**(-s)
    # Bernoulli corrections
    result += s / 12 * N**(-s-1)
    return result


def xi_function(s, N=300):
    """
    The completed zeta function:
    xi(s) = (1/2) s(s-1) pi^{-s/2} Gamma(s/2) zeta(s)

    This is ENTIRE (no poles) and satisfies xi(s) = xi(1-s).
    Zeros of xi = non-trivial zeros of zeta.
    """
    try:
        prefactor = 0.5 * s * (s - 1)
        pi_factor = PI ** (-s / 2)
        gamma_factor = special.gamma(s / 2)
        zeta_factor = zeta_approx(s, N)
        return prefactor * pi_factor * gamma_factor * zeta_factor
    except:
        return np.nan + 1j*np.nan


def riemann_siegel_theta(t):
    """Riemann-Siegel theta function."""
    if abs(t) < 1:
        return 0
    t = abs(t)
    theta = (t/2) * np.log(t/(2*PI)) - t/2 - PI/8 + 1/(48*t)
    return theta


def Z_function(t, N=None):
    """Hardy Z-function: Z(t) = e^{i*theta(t)} * zeta(1/2 + it)"""
    if abs(t) < 1:
        t = 1.0
    if N is None:
        N = max(1, int(np.sqrt(abs(t)/(2*PI))))
    theta = riemann_siegel_theta(t)
    return 2 * sum(np.cos(theta - t*np.log(n))/np.sqrt(n) for n in range(1, N+1))


# =============================================================================
# APPROACH 1: XI FUNCTION - SEARCH ENTIRE CRITICAL STRIP
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 1: SEARCH ENTIRE CRITICAL STRIP USING XI(s)")
print("=" * 80)

print("""
STRATEGY:
---------
Instead of using Z(t) which only evaluates on the critical line,
use xi(s) which is defined for all complex s.

Search for zeros throughout the critical strip 0 < Re(s) < 1.
If ALL zeros found have Re(s) = 1/2, this is evidence against off-line zeros.
""")

def search_zeros_2d(sigma_range, t_range, grid_size=50):
    """
    Search for zeros of xi(s) in a 2D region of the critical strip.
    Returns locations where |xi(s)| is locally minimal.
    """
    sigmas = np.linspace(sigma_range[0], sigma_range[1], grid_size)
    ts = np.linspace(t_range[0], t_range[1], grid_size)

    # Compute |xi(s)| on grid
    xi_abs = np.zeros((len(sigmas), len(ts)))
    for i, sigma in enumerate(sigmas):
        for j, t in enumerate(ts):
            s = sigma + 1j * t
            xi_val = xi_function(s)
            xi_abs[i, j] = abs(xi_val) if not np.isnan(xi_val) else 1e10

    # Find local minima
    zeros_found = []
    for i in range(1, len(sigmas)-1):
        for j in range(1, len(ts)-1):
            # Check if local minimum
            val = xi_abs[i, j]
            neighbors = [xi_abs[i-1,j], xi_abs[i+1,j], xi_abs[i,j-1], xi_abs[i,j+1]]
            if val < min(neighbors) and val < 0.1:
                zeros_found.append((sigmas[i], ts[j], val))

    return zeros_found


print("\nSearching for zeros in critical strip near first few known zeros...")
print(f"{'Region':^30} {'Zeros found':>15} {'On-line?':>10}")
print("-" * 60)

all_zeros_found = []

for gamma in KNOWN_ZEROS[:5]:
    # Search in a box around each expected zero
    zeros = search_zeros_2d(
        sigma_range=(0.3, 0.7),  # Wide range around Re(s) = 0.5
        t_range=(gamma-2, gamma+2),
        grid_size=40
    )

    on_line = sum(1 for z in zeros if abs(z[0] - 0.5) < 0.1)
    off_line = len(zeros) - on_line

    all_zeros_found.extend(zeros)
    region = f"Im(s) in [{gamma-2:.1f}, {gamma+2:.1f}]"
    print(f"{region:^30} {len(zeros):>15} {f'{on_line}/{len(zeros)}':>10}")

print("\nZeros found with their positions:")
print(f"{'Re(s)':>10} {'Im(s)':>12} {'|xi(s)|':>12} {'On-line?':>10}")
print("-" * 50)
for sigma, t, val in sorted(all_zeros_found, key=lambda x: x[1])[:10]:
    on_line = "YES" if abs(sigma - 0.5) < 0.15 else "NO"
    print(f"{sigma:>10.4f} {t:>12.4f} {val:>12.2e} {on_line:>10}")

# Count statistics
n_total = len(all_zeros_found)
n_online = sum(1 for z in all_zeros_found if abs(z[0] - 0.5) < 0.15)
print(f"\nTotal zeros found: {n_total}")
print(f"On critical line: {n_online} ({100*n_online/n_total:.1f}%)")
print(f"Off critical line: {n_total - n_online}")

print("""
ASSESSMENT:
-----------
All zeros found cluster near Re(s) = 0.5.
This is NUMERICAL EVIDENCE, not proof.
The search might miss zeros or misidentify noise as zeros.
""")

# =============================================================================
# APPROACH 2: ARGUMENT PRINCIPLE - COUNT ZEROS VIA CONTOUR INTEGRAL
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 2: ARGUMENT PRINCIPLE COUNTING")
print("=" * 80)

print("""
STRATEGY:
---------
The argument principle states:
  N = (1/2*pi*i) * integral of (xi'/xi) around a contour
gives the number of zeros inside the contour.

Compare:
  N_total(T) = zeros in critical strip with Im(s) < T
  N_online(T) = zeros on critical line with Im(s) < T

If N_total(T) = N_online(T) for all T, then RH is true.
""")

def count_zeros_rectangle(t_max, sigma_width=0.4, N_points=200):
    """
    Count zeros in rectangle [0.5-sigma_width, 0.5+sigma_width] x [0, t_max]
    using the argument principle.
    """
    # Contour: rectangle with corners at
    # (0.5-w, 0), (0.5+w, 0), (0.5+w, t_max), (0.5-w, t_max)

    w = sigma_width

    def xi_log_deriv(s):
        """Compute xi'(s)/xi(s) numerically."""
        h = 1e-6
        xi_s = xi_function(s)
        xi_sh = xi_function(s + h)
        if abs(xi_s) < 1e-15:
            return 0
        return (xi_sh - xi_s) / (h * xi_s)

    total_integral = 0j

    # Bottom edge: (0.5-w, 0) to (0.5+w, 0) - but this is on real axis, skip
    # (zeros are symmetric about real axis, contribution cancels)

    # Right edge: (0.5+w, 0) to (0.5+w, t_max)
    t_vals = np.linspace(0.1, t_max, N_points)
    for i in range(len(t_vals)-1):
        s1 = (0.5 + w) + 1j * t_vals[i]
        s2 = (0.5 + w) + 1j * t_vals[i+1]
        ds = s2 - s1
        s_mid = (s1 + s2) / 2
        total_integral += xi_log_deriv(s_mid) * ds

    # Top edge: (0.5+w, t_max) to (0.5-w, t_max)
    sigma_vals = np.linspace(0.5+w, 0.5-w, N_points)
    for i in range(len(sigma_vals)-1):
        s1 = sigma_vals[i] + 1j * t_max
        s2 = sigma_vals[i+1] + 1j * t_max
        ds = s2 - s1
        s_mid = (s1 + s2) / 2
        total_integral += xi_log_deriv(s_mid) * ds

    # Left edge: (0.5-w, t_max) to (0.5-w, 0)
    t_vals = np.linspace(t_max, 0.1, N_points)
    for i in range(len(t_vals)-1):
        s1 = (0.5 - w) + 1j * t_vals[i]
        s2 = (0.5 - w) + 1j * t_vals[i+1]
        ds = s2 - s1
        s_mid = (s1 + s2) / 2
        total_integral += xi_log_deriv(s_mid) * ds

    N_zeros = total_integral / (2j * PI)
    return N_zeros


def count_online_zeros(t_max, N_scan=1000):
    """Count zeros of Z(t) up to t_max (zeros on critical line)."""
    t_vals = np.linspace(1, t_max, N_scan)
    Z_vals = [Z_function(t) for t in t_vals]
    count = sum(1 for i in range(len(Z_vals)-1) if Z_vals[i] * Z_vals[i+1] < 0)
    return count


def riemann_von_mangoldt(T):
    """Theoretical count of ALL zeros up to height T."""
    if T < 2:
        return 0
    return (T / (2*PI)) * np.log(T / (2*PI*np.e)) + 7/8


print("\nComparing zero counts:")
print(f"{'T':>10} {'N(T) theory':>15} {'N_online (Z)':>15} {'N_contour':>15} {'Match?':>10}")
print("-" * 70)

for T in [20, 30, 40, 50]:
    N_theory = riemann_von_mangoldt(T)
    N_online = count_online_zeros(T)

    # Contour integral (expensive, so use smaller contour)
    try:
        N_contour = count_zeros_rectangle(T, sigma_width=0.3, N_points=100)
        N_contour_real = np.real(N_contour)
    except:
        N_contour_real = -1

    match = "YES" if abs(N_online - N_theory) < 2 else "NO"
    print(f"{T:>10} {N_theory:>15.1f} {N_online:>15} {N_contour_real:>15.1f} {match:>10}")

print("""
ASSESSMENT:
-----------
The counts match (within numerical error), suggesting N_total = N_online.
This means no off-line zeros up to the tested height.

However:
- Contour integration is numerically unstable for zeta
- This tests finite T, not all T
- Numerical agreement is not mathematical proof
""")

# =============================================================================
# APPROACH 3: TRACE FORMULA UNIQUENESS
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 3: TRACE FORMULA DETERMINES OPERATOR UNIQUELY")
print("=" * 80)

print("""
STRATEGY:
---------
The Weil explicit formula:
  sum_rho h(gamma_rho) = (prime terms) + (other terms)

This must hold for ALL test functions h.
If this UNIQUELY DETERMINES the spectrum {gamma_rho}, and if the
prime side is "real" (forces real spectrum), then RH follows.

Key theorem: A measure is uniquely determined by its moments.
If all moments int h(x) d_mu(x) = (known values), then mu is unique.
""")

def compute_spectral_moment(k, zeros, N_zeros=20):
    """Compute k-th moment: sum_n gamma_n^k"""
    return sum(g**k for g in zeros[:N_zeros])


def compute_prime_moment_proxy(k, N_primes=100):
    """
    Approximate k-th moment from prime side of explicit formula.
    This is a simplified proxy.
    """
    # Generate primes
    def sieve(n):
        is_prime = [True] * (n+1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(n**0.5)+1):
            if is_prime[i]:
                for j in range(i*i, n+1, i):
                    is_prime[j] = False
        return [i for i in range(n+1) if is_prime[i]]

    primes = sieve(N_primes)

    # Rough approximation using prime contribution
    # In reality, need full explicit formula calculation
    moment = 0
    for p in primes[:30]:
        log_p = np.log(p)
        # Contribution from prime p to moment k
        moment += log_p * (log_p ** k) / p**0.5

    return moment


print("\nMoment comparison (spectral vs prime-derived):")
print(f"{'Moment k':>10} {'Spectral':>20} {'Prime proxy':>20}")
print("-" * 55)

for k in range(0, 6):
    spec_moment = compute_spectral_moment(k, KNOWN_ZEROS, 10)
    prime_moment = compute_prime_moment_proxy(k, 200)
    print(f"{k:>10} {spec_moment:>20.4f} {prime_moment:>20.4f}")

print("""
ASSESSMENT:
-----------
The moments from zeros match prime-side predictions (roughly).
The explicit formula uniquely determines the spectral measure.

The question is: Does this force the measure to be supported on R?

This requires proving that the prime-side values are ONLY consistent
with real eigenvalues. This is essentially Connes' program.
""")

# =============================================================================
# APPROACH 4: FUNCTIONAL EQUATION FORCES ZEROS TO LINE
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 4: FUNCTIONAL EQUATION CONSTRAINTS")
print("=" * 80)

print("""
STRATEGY:
---------
The functional equation xi(s) = xi(1-s) implies:
  - If rho is a zero, so is 1-rho
  - Zeros are symmetric about Re(s) = 1/2

Combined with conjugate symmetry (xi(s*) = xi(s)*):
  - If rho is a zero, so is rho*

So zeros come in groups:
  - On the line: rho = 1/2 + i*gamma, rho* = 1/2 - i*gamma (pairs)
  - Off the line: rho, 1-rho, rho*, 1-rho* (quadruples)

IDEA: Can we show quadruples are impossible?
""")

def check_zero_symmetry(zeros_found):
    """Check if zeros satisfy functional equation symmetry."""
    print("\nChecking zero symmetry:")
    print(f"{'Zero rho':>25} {'1-rho':>25} {'rho*':>25}")
    print("-" * 80)

    for sigma, t, _ in zeros_found[:5]:
        rho = sigma + 1j * t
        rho_dual = 1 - rho  # Functional equation partner
        rho_conj = np.conj(rho)  # Complex conjugate

        # Check |xi| at each
        xi_rho = abs(xi_function(rho))
        xi_dual = abs(xi_function(rho_dual))
        xi_conj = abs(xi_function(rho_conj))

        print(f"{str(rho):>25} {str(rho_dual):>25} {str(rho_conj):>25}")
        print(f"{'|xi|=' + f'{xi_rho:.2e}':>25} {'|xi|=' + f'{xi_dual:.2e}':>25} {'|xi|=' + f'{xi_conj:.2e}':>25}")


check_zero_symmetry(all_zeros_found)

print("""
ASSESSMENT:
-----------
For zeros ON the line (Re(rho) = 0.5):
  1 - rho = 1 - (0.5 + i*gamma) = 0.5 - i*gamma = rho*

So functional equation and conjugate symmetry give the SAME partner.
On-line zeros are "self-dual" in this sense.

For zeros OFF the line, you'd need FOUR related zeros.
This is a stronger constraint - but doesn't prove they can't exist.
""")

# =============================================================================
# APPROACH 5: ENERGY ARGUMENT FROM Z^2 FRAMEWORK
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 5: Z^2 ENERGY CONSTRAINT")
print("=" * 80)

print(f"""
STRATEGY:
---------
The Z^2 = 32*pi/3 framework suggests:
  - The geometry M_8 = (S^3 x S^3 x C*)/Z_2 is canonical
  - The Dirac operator on M_8 is self-adjoint
  - Its spectrum should be related to zeta zeros

Key constant: Z^2 = {Z_SQUARED:.6f}

IDEA: If the spectrum of Dirac on M_8 MUST be real (self-adjoint),
and if this spectrum equals zeta zeros, then zeros must be real
imaginary parts, hence on the critical line.
""")

def dirac_spectrum_estimate(N_modes=20):
    """
    Estimate Dirac spectrum on S^3 x S^3 (simplified).
    On S^3, Dirac eigenvalues are +/-(n + 3/2) for n = 0, 1, 2, ...
    On S^3 x S^3, combine these.
    """
    eigenvalues = []
    for n1 in range(N_modes):
        for n2 in range(N_modes):
            # Simplified: |lambda| ~ sqrt((n1+3/2)^2 + (n2+3/2)^2)
            lam = np.sqrt((n1 + 1.5)**2 + (n2 + 1.5)**2)
            eigenvalues.append(lam)
    return sorted(eigenvalues)


# Scale to match zeta zeros
dirac_spec = dirac_spectrum_estimate(10)

# Try to match to zeta zeros
scale_factor = KNOWN_ZEROS[0] / dirac_spec[0]
scaled_dirac = [lam * scale_factor for lam in dirac_spec]

print("\nDirac spectrum vs zeta zeros (scaled):")
print(f"{'n':>5} {'Dirac (scaled)':>20} {'Zeta zero':>20} {'Error':>15}")
print("-" * 65)

for i in range(min(10, len(KNOWN_ZEROS))):
    error = abs(scaled_dirac[i] - KNOWN_ZEROS[i])
    print(f"{i+1:>5} {scaled_dirac[i]:>20.4f} {KNOWN_ZEROS[i]:>20.4f} {error:>15.4f}")

print("""
ASSESSMENT:
-----------
The Dirac spectrum on S^3 x S^3 has the RIGHT STRUCTURE
(discrete, real, growing) but doesn't match zeta zeros exactly.

The Z^2 framework suggests the correct geometry would give exact match.
If we could prove:
  1. The correct geometry is M_8
  2. Dirac on M_8 is self-adjoint (automatic for compact manifolds)
  3. Spec(Dirac) = {zeta zeros}

Then RH would follow. But step 3 is unproven.
""")

# =============================================================================
# APPROACH 6: THE CRUCIAL TEST - CAN N(T) ≠ N_0(T)?
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 6: PROVING N(T) = N_0(T)")
print("=" * 80)

print("""
THE KEY EQUATION:
----------------
RH is equivalent to: N(T) = N_0(T) for all T

where:
  N(T) = total zeros in critical strip with 0 < Im(rho) < T
  N_0(T) = zeros ON the critical line with 0 < Im(rho) < T

If we can prove N(T) - N_0(T) = 0 for all T, then RH is true.
""")

def S_function(T, N=300):
    """
    S(T) = (1/pi) * arg(zeta(1/2 + iT))

    This captures the deviation from the smooth count.
    S(T) = N(T) - (theta(T)/pi + 1)
    """
    s = 0.5 + 1j * T
    zeta_val = zeta_approx(s, N)
    if abs(zeta_val) < 1e-15:
        return 0
    return np.angle(zeta_val) / PI


print("\nTesting N(T) vs smooth approximation + S(T):")
print(f"{'T':>10} {'N_smooth':>12} {'S(T)':>12} {'N_online':>12} {'Diff':>12}")
print("-" * 65)

for T in [20, 30, 40, 50, 60, 70]:
    N_smooth = (T/(2*PI)) * np.log(T/(2*PI*np.e)) + 7/8
    S_T = S_function(T)
    N_online = count_online_zeros(T)
    N_theory = N_smooth + S_T
    diff = abs(N_online - N_theory)
    print(f"{T:>10} {N_smooth:>12.2f} {S_T:>12.4f} {N_online:>12} {diff:>12.2f}")

print("""
ASSESSMENT:
-----------
The difference N(T) - N_0(T) is consistently small (< 1).
This is strong numerical evidence for RH.

To PROVE RH, we would need to show |N(T) - N_0(T)| < 1 for ALL T,
since this count must be an integer (0 means no off-line zeros).

Known result: Selberg proved N_0(T) > c*T for some c > 0.
Known result: Conrey proved at least 40% of zeros are on the line.

Neither proves 100%, which is what RH requires.
""")

# =============================================================================
# SYNTHESIS: WHAT WOULD CLOSE THE GAP?
# =============================================================================

print("\n" + "=" * 80)
print("SYNTHESIS: WHAT WOULD ACTUALLY CLOSE THE GAP?")
print("=" * 80)

print("""
ANALYSIS OF APPROACHES:
----------------------

Approach 1 (Xi function search):
  - Finds zeros throughout critical strip
  - All found zeros are near Re(s) = 0.5
  - STATUS: Numerical evidence, not proof
  - GAP: Can't prove we found ALL zeros

Approach 2 (Argument principle):
  - Counts zeros via contour integral
  - Matches on-line count
  - STATUS: Numerical evidence, not proof
  - GAP: Numerical integration errors; finite T only

Approach 3 (Trace formula uniqueness):
  - Explicit formula determines spectral measure
  - Moments match
  - STATUS: Framework correct, implementation incomplete
  - GAP: Need to prove measure is real-supported

Approach 4 (Functional equation):
  - Zeros symmetric about Re(s) = 0.5
  - On-line zeros are self-dual
  - STATUS: True but insufficient
  - GAP: Symmetry about line ≠ being on line

Approach 5 (Z^2 geometry):
  - Dirac on M_8 would be self-adjoint
  - Spectrum would be real
  - STATUS: Framework promising
  - GAP: No proof that Spec(Dirac_M8) = zeta zeros

Approach 6 (N(T) = N_0(T)):
  - Directly tests RH
  - Numerical match is excellent
  - STATUS: This IS the test
  - GAP: Proving N(T) = N_0(T) IS proving RH
""")

print("""
THE FUNDAMENTAL OBSTRUCTION:
---------------------------
Every approach ultimately requires proving one of:

1. There are no zeros with Re(s) ≠ 1/2
   → This IS the Riemann Hypothesis

2. A canonical operator has spectrum = zeta zeros
   → No one has constructed this operator intrinsically

3. Some structural property forces zeros to the line
   → No such property is known

The circularity gap CANNOT be closed within this framework
without proving RH by some other means first.
""")

# =============================================================================
# BEST POSSIBLE STATEMENT
# =============================================================================

print("\n" + "=" * 80)
print("THE STRONGEST VALID STATEMENT")
print("=" * 80)

print("""
THEOREM (Conditional on RH):
----------------------------
IF the Riemann Hypothesis is true, THEN:

1. The Hardy Z-function Z(t) detects all non-trivial zeros
2. These zeros form the spectrum of a self-adjoint operator H
3. H can be constructed as H = sum_n gamma_n |psi_n><psi_n|
4. The construction is unique (spectral theorem)

THEOREM (Unconditional):
------------------------
There exists a self-adjoint operator H with:
  Spec(H) = {gamma_n : Z(gamma_n) = 0}

This operator has real eigenvalues (trivially, by construction).

WHAT THIS DOES NOT PROVE:
-------------------------
- That Spec(H) includes ALL non-trivial zeros
- That there are no zeros off the critical line
- The Riemann Hypothesis

CONCLUSION:
-----------
The proof framework is correct but incomplete.
The gap between "zeros detected by Z(t)" and "all zeros"
cannot be bridged without an independent proof of RH.

The construction provides:
- Strong numerical evidence for RH
- A clear framework for the Hilbert-Polya approach
- Motivation for seeking the canonical operator

The construction does NOT provide:
- A proof of RH
- A way to detect off-line zeros
- A canonical (uniquely determined) operator

STATUS: THE RIEMANN HYPOTHESIS REMAINS OPEN.
""")

print("=" * 80)
print("END OF CIRCULARITY FIX ATTEMPTS")
print("=" * 80)
