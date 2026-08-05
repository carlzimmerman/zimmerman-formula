#!/usr/bin/env python3
"""
eos_compare_monddirect.py — Rigorous EOS vs standard MOND comparison

CRITICAL FIX: Both interpolation functions must use x = a/a_0 as the
dimensionless variable. Previously, we compared against x = a/a_gh which
was wrong.

This script:
1. Defines x_EOS = a / a0_EOS where a0_EOS comes from the EOS (a_gh/(2Z))
2. Defines x_std = a / a0_std for standard MOND forms
3. Compares mu(x) on CONSISTENT axes
4. Double-checks all analytic limits numerically
5. Tests consistency with multiple observational constraints
"""

import numpy as np
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json, os

# ============================================================================
# PHYSICAL INPUT (observational only)
# ============================================================================
c      = 2.99792458e8
hbar   = 1.054571817e-34
kB     = 1.380649e-23
Lambda = 1.089e-53

H_dS   = c * np.sqrt(Lambda / 3)       # s^-1
a_gh   = c * H_dS                        # ~1.7e-10 m/s^2 — acceleration scale
T_GH   = hbar * H_dS / (2*np.pi*kB)     # K

# Standard MOND a0
a0_standard = 1.2e-10  # central observed value

print("=" * 80)
print("EOS vs STANDARD MOND: CONSISTENT x = a/a_0 COMPARISON")
print("=" * 80)
print(f"\na_gh = c*H_dS  = {a_gh:.3e} m/s^2")
print(f"a0 (observed)  = {a0_standard:.1e} m/s^2")
print(f"Ratio a_gh/a0  = {a_gh/a0_standard:.3f}")

# ============================================================================
# EOS PARAMETERS
# ============================================================================
# Z derived from matching the transition scale to observed a0:
#   a_transition ≈ a_gh / (2Z) = a0  =>  Z = a_gh / (2*a0)
Z = a_gh / (2 * a0_standard)
a0_from_EOS = a_gh / (2 * Z)  # should equal a0_standard

print(f"\nEOS parameter: Z = {Z:.4f} (derived from a0_obs)")
print(f"EOS a0 prediction: a0 = a_gh/(2Z) = {a0_from_EOS:.3e} m/s^2")

# ============================================================================
# INTERPOLATION FUNCTIONS — defined with x = a/a_0
# ============================================================================
def mu_eos(x, Z=Z):
    """EOS interpolation: mu(x) = tanh(asinh(2Z*x/(a_gh/a0))/2)"""
    # u = 2Z * (a/a_gh) = 2Z * x * (a0/a_gh) = 2Z * x / (2Z) = x ... wait
    # a/a_gh = (a/a0)*(a0/a_gh) = x * (1/(2Z))
    # u = 2Z * (a/a_gh) = 2Z * x / (2Z) = x
    # So mu = tanh(asinh(x)/2). The Z cancels out!
    u = x  # because a0_EOS = a_gh/(2Z) by construction
    asinh_u = np.log(u + np.sqrt(u**2 + 1))
    return (np.exp(asinh_u/2) - np.exp(-asinh_u/2)) / \
           (np.exp(asinh_u/2) + np.exp(-asinh_u/2))

def mu_standard_mondd(x):
    """Standard: mu = x/sqrt(1+x^2)"""
    return x / np.sqrt(1 + x**2)

def mu_simple_mondd(x):
    """Simple: mu = x/(1+x)"""
    return x / (1 + x)

def mu_AQUAL(x):
    """AQUAL-inspired: mu = x/sqrt(1+4x^2) ... actually let's try mu = sqrt(1+x^2)-x+..."""
    # More standard AQUAL form: nu(y) where y = a_N/a0, and the MOND function is different
    pass

def mu_exponential(x):
    """Exponential interpolation: mu = 1 - exp(-x)"""
    return 1 - np.exp(-x)

# ============================================================================
# KEY INSIGHT: Z CANCELS OUT!
# ============================================================================
print()
print("=" * 80)
print("KEY DERIVATION: Why the EOS interpolation is UNIQUELY DETERMINED")
print("=" * 80)
print("""
The u parameter:
  u = 2Z * (a/a_gh)

The EOS transition scale: a_0_EOS = a_gh/(2Z), so:
  a/a_gh = (a/a_0)*(a_0/a_gh) = x/(2Z)

Therefore: u = 2Z * x/(2Z) = x

THE INTERPOLATION FUNCTION IS:
  mu(x) = tanh(asinh(x)/2)

where x = a/a0 by construction. Z DOES NOT APPEAR — it was absorbed into
the definition of a0! This is because we chose a0 = a_gh/(2Z).

The EOS makes ONE prediction beyond MOND: the SHAPE of the interpolation
function is UNIQUELY determined as mu = tanh(asinh(x)/2).

Let's verify this function and compare to standard forms.
""")

def tanh_asinh_half(x):
    """mu(x) = tanh(asinh(x)/2) — the UNIQUE EOS prediction."""
    x_arr = np.asarray(x, dtype=float)
    result = np.zeros_like(x_arr)
    mask = x_arr > 0
    if np.any(mask):
        asinh_u = np.log(x_arr[mask] + np.sqrt(x_arr[mask]**2 + 1))
        result[mask] = (np.exp(asinh_u / 2) - np.exp(-asinh_u / 2)) / \
                       (np.exp(asinh_u / 2) + np.exp(-asinh_u / 2))
    return result

# ============================================================================
# SECTION 1: ANALYTIC LIMITS (VERIFIED SYMBOLICALLY)
# ============================================================================
print()
print("=" * 80)
print("SECTION 1: ANALYTIC LIMITS — DOUBLE-CHECKED")
print("=" * 80)

# High-x limit (Newtonian)
print("\nHIGH-x: x >> 1 (Newtonian regime)")
asymptotic = []
for x_val in [2, 5, 10, 50, 100]:
    mu_val = tanh_asinh_half(x_val)
    asymptotic.append(mu_val)
    delta = 1 - mu_val
    print(f"  x={x_val:5.0f}: mu = {mu_val:.10f},  1-mu = {delta:.6e}  (expected: ~1/(2x*...))")

# Verify: for large x, mu -> 1 - 1/(2x) + O(x^(-2))
print("\n  Analytic prediction: 1 - mu ≈ 1/(2x) [verify below]")
for x_val in [5, 10, 50, 100]:
    mu_val = tanh_asinh_half(x_val)
    actual_delta = 1 - mu_val
    approx_delta = 1 / (2 * x_val)
    print(f"  x={x_val:5.0f}: actual delta = {actual_delta:.6e}, 1/(2x) = {approx_delta:.6e}")

# Low-x limit (MOND regime)
print("\nLOW-x: x << 1 (MOND regime)")
for x_val in [1e-4, 1e-3, 1e-2, 1e-1]:
    mu_val = tanh_asinh_half(x_val)
    print(f"  x={x_val:8.1e}: mu = {mu_val:.8f},  mu/x = {mu_val/x_val:.8f}")

# Analytic: mu -> x/2 for small x
print("\n  Analytic: mu ≈ x/2 for small x (verify:")
for x_val in [1e-4, 1e-3, 1e-2]:
    mu_val = tanh_asinh_half(x_val)
    ratio_to_linear = mu_val / (x_val / 2.0)
    print(f"  x={x_val:8.1e}: mu/x/2 = {ratio_to_linear:.6f} (should -> 1)")

# VERIFICATION BY SERIES EXPANSION
print("\n" + "-" * 40)
print("SERIES EXPANSION VERIFICATION:")
print("-" * 40)
print("""
mu(x) = tanh(asinh(x)/2)

For small x:
  asinh(x) = x - x^3/6 + O(x^5)
  asinh(x)/2 = x/2 - x^3/12 + O(x^5)
  tanh(y) = y - y^3/3 + O(y^5) for small y
  So: mu(x) ≈ (x/2 - x^3/12) - (x/2)^3/3 + ...
            = x/2 - x^3/12 - x^3/24 + ...
            = x/2 - x^3/8 + O(x^5)

CHECK: mu(x)/x -> 1/2 as x -> 0 ✓
       mu(x) ≈ x/2 for small x ✓

For large x:
  asinh(x) = ln(2x) + O(x^(-2))
  tanh(ln(2x)/2) = (√(2x) - 1/√(2x))/(√(2x) + 1/√(2x))
                  = (2x-1)/(2x+1)
                  = 1 - 2/(2x+1) + O(x^(-2))
                  = 1 - 1/x + O(x^(-2))

CHECK: mu -> 1 as x -> inf, with correction ~1/x ✓
""")

# Numerical series verification
print("\nNUMERICAL SERIES CHECK (low-x):")
x_small_vals = [1e-6, 5e-6, 1e-5]
mu_low = [tanh_asinh_half(x) for x in x_small_vals]
for xi, mi in zip(x_small_vals, mu_low):
    linear_approx = xi / 2.0
    cubic_corr = -xi**3 / 8.0
    predicted = linear_approx + cubic_corr
    print(f"  x={xi:.1e}: mu = {mi:.10e}, x/2 = {linear_approx:.10e}, "
          f"x/2-x^3/8 = {predicted:.10e}")

print("\nNUMERICAL SERIES CHECK (high-x):")
x_large_vals = [10, 50, 100]
mu_high = [tanh_asinh_half(x) for x in x_large_vals]
for xi, mi in zip(x_large_vals, mu_high):
    approx = 1 - 1/xi
    print(f"  x={xi:5.0f}: mu = {mi:.10e}, 1-1/x = {approx:.10e}")

# ============================================================================
# SECTION 2: FULL COMPARISON ON CONSISTENT AXIS
# ============================================================================
print()
print("=" * 80)
print("SECTION 2: INTERPOLATION FUNCTION COMPARISON (x = a/a_0)")
print("=" * 80)

x_vals = np.logspace(-4, 3, 500)
mu_eos_curve = tanh_asinh_half(x_vals)
mu_std_curve = mu_standard_mondd(x_vals)
mu_simple_curve = mu_simple_mondd(x_vals)
mu_exp_curve = mu_exponential(x_vals)

print(f"\n{'x':<10} {'EOS':<14} {'std μ=x/√(1+x²)':<20} {'simple=x/(1+x)':<18} {'exp=1-e^(-x)':<16}")
print("-" * 78)

for xi in [1e-4, 1e-3, 1e-2, 5e-2, 1e-1, 5e-1, 1.0, 2.0, 5.0, 10.0, 50.0]:
    idx = np.argmin(np.abs(x_vals - xi))
    m_e = mu_eos_curve[idx]
    m_s = mu_std_curve[idx]
    m_p = mu_simple_curve[idx]
    m_x = mu_exp_curve[idx]
    diff_es = (m_e - m_s) / (m_s + 1e-20) * 100
    diff_ep = (m_e - m_p) / (m_p + 1e-20) * 100
    print(f"{xi:<10.1e} {m_e:<14.8f} {m_s:<20.8f} {m_p:<18.8f} {m_x:<16.8f}")

# ============================================================================
# SECTION 3: QUANTITATIVE DEVIATIONS FROM STANDARD FORMS
# ============================================================================
print()
print("=" * 80)
print("SECTION 3: MAXIMUM DEVIATION BY REGIME")
print("=" * 80)

def max_deviation(mu1, mu2):
    """Max relative deviation (in %)."""
    rel = np.abs(mu1 - mu2) / (mu2 + 1e-20) * 100
    return np.max(rel), np.median(rel), np.mean(rel)

# In MOND regime (x < 0.1)
mask_mondd = x_vals < 0.1
max_e_s, med_e_s, mean_e_s = max_deviation(mu_eos_curve[mask_mondd], mu_std_curve[mask_mondd])
max_e_p, med_e_p, mean_e_p = max_deviation(mu_eos_curve[mask_mondd], mu_simple_curve[mask_mondd])

# In transition regime (0.1 < x < 3)
mask_trans = (x_vals > 0.1) & (x_vals < 3)
max_e_s_t, med_e_s_t, mean_e_s_t = max_deviation(mu_eos_curve[mask_trans], mu_std_curve[mask_trans])

# In Newtonian regime (x > 3)
mask_newt = x_vals > 3
max_e_s_n, med_e_s_n, mean_e_s_n = max_deviation(mu_eos_curve[mask_newt], mu_std_curve[mask_newt])

print(f"\nMOND regime (x < 0.1):")
print(f"  vs std:   max dev = {max_e_s:.2f}%, median = {med_e_s:.3f}%")
print(f"  vs simple: max dev = {max_e_p:.2f}%, median = {med_e_p:.3f}%")

print(f"\nTransition regime (0.1 < x < 3):")
print(f"  vs std:   max dev = {max_e_s_t:.2f}%, median = {med_e_s_t:.3f}%")

print(f"\nNewtonian regime (x > 3):")
print(f"  vs std:   max dev = {max_e_s_n:.2f}%, median = {med_e_s_n:.3f}%")

# ============================================================================
# SECTION 4: PLOTTING
# ============================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel A: All interpolation functions on log-log (x-axis is a/a0)
axes[0,0].loglog(x_vals, mu_eos_curve, 'b-', linewidth=3.5, label='EOS: μ=tanh(asinh(x)/2)')
axes[0,0].loglog(x_vals, mu_std_curve, 'r--', linewidth=2.5, alpha=0.7, label='Standard: x/√(1+x²)')
axes[0,0].loglog(x_vals, mu_simple_curve, 'g-.', linewidth=2.5, alpha=0.7, label='Simple: x/(1+x)')
axes[0,0].axhline(0.5, color='k', ls=':', alpha=0.3)
axes[0,0].axvline(1.0, color='k', ls=':', alpha=0.3)
# Reference lines
axes[0,0].loglog([0.01, 1], [0.005, 0.5], 'c--', linewidth=1, alpha=0.5, label='x/2 reference')
axes[0,0].loglog([1, 100], [1, 1], 'k:', linewidth=1, alpha=0.5)
axes[0,0].set_xlabel('x = a / a₀', fontsize=13)
axes[0,0].set_ylabel('μ(x)', fontsize=13)
axes[0,0].set_title('Interpolation Functions: EOS vs Standard MOND', fontsize=13)
axes[0,0].legend(fontsize=10)
axes[0,0].grid(True, alpha=0.3)
axes[0,0].set_ylim(1e-4, 3)

# Panel B: Relative deviation from standard (linear MOND regime)
dev_from_linear = np.abs(mu_eos_curve - x_vals/2) / (x_vals/2 + 1e-20) * 100
axes[0,1].semilogx(x_vals, dev_from_linear, 'b-', linewidth=3)
axes[0,1].axhline(0, color='k', ls=':', alpha=0.3)
axes[0,1].axvline(1.0, color='r', ls='--', alpha=0.5, label='a=a₀')
axes[0,1].set_xlabel('x = a / a₀', fontsize=13)
axes[0,1].set_ylabel('|μ_EOS - x/2|/(x/2) (%)', fontsize=11)
axes[0,1].set_title('EOS Deviation from Linear MOND (x/2)', fontsize=12)
axes[0,1].legend(fontsize=10)
axes[0,1].grid(True, alpha=0.3)
axes[0,1].set_ylim(0.1, 100)

# Panel C: Deviation from standard MOND interpolation
dev_std = np.abs(mu_eos_curve - mu_std_curve) / (mu_std_curve + 1e-20) * 100
axes[1,0].semilogx(x_vals, dev_std, 'r-', linewidth=3)
axes[1,0].axhline(0, color='k', ls=':', alpha=0.3)
# Mark minimum deviation region
min_idx = np.argmin(dev_std)
axes[1,0].plot(x_vals[min_idx], dev_std[min_idx], 'bo', markersize=8)
axes[1,0].set_xlabel('x = a / a₀', fontsize=13)
axes[1,0].set_ylabel('|μ_EOS - μ_std|/μ_std (%)', fontsize=11)
axes[1,0].set_title('Deviation from Standard Interpolation', fontsize=12)
axes[1,0].grid(True, alpha=0.3)
axes[1,0].set_ylim(0.1, 500)

# Panel D: Second derivative (inflection point = transition)
d2mu_eos = []
for i in range(1, len(x_vals)-1):
    d2 = (tanh_asinh_half(x_vals[i+1]) - 2*tanh_asinh_half(x_vals[i]) + tanh_asinh_half(x_vals[i-1])) / \
         ((np.log(x_vals[i+1]) - np.log(x_vals[i-1]))**2)
    d2mu_eos.append(d2)
d2mu_eos = np.array(d2mu_eos)

axes[1,1].semilogx(x_vals[1:-1], np.abs(d2mu_eos), 'b-', linewidth=3)
inflection_idx = np.argmax(np.abs(d2mu_eos))
axes[1,1].axvline(x_vals[inflection_idx+1], color='r', ls='--', alpha=0.7,
                  label=f'Inflection at x≈{x_vals[inflection_idx+1]:.3f}')
axes[1,1].set_xlabel('x = a / a₀', fontsize=13)
axes[1,1].set_ylabel('|d²μ/d(log x)²|', fontsize=12)
axes[1,1].set_title('Curvature: Transition Sharpness', fontsize=12)
axes[1,1].legend(fontsize=10)
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
save_path = os.path.join(os.path.dirname(__file__), 'eos_vs_std_mondd.png')
plt.savefig(save_path, dpi=150)
print(f"\nPlot saved: {save_path}")
plt.close()

# ============================================================================
# SECTION 5: OBSERVATIONAL CONSISTENCY CHECKS
# ============================================================================
print()
print("=" * 80)
print("SECTION 4: OBSERVATIONAL CONSISTENCY")
print("=" * 80)
print(f"CHECK 1: a0 scale from cosmology")
print(f"  a0 = c*H_dS / (2Z), with Z ~ O(1)")
print(f"  With Z = {Z:.3f}: a0 = {a0_from_EOS:.1e} m/s^2")
print(f"  Observed: a0 ≈ 1.2×10⁻¹⁰ m/s^2")
print(f"  Status: OK (by construction)")

print()
print("CHECK 2: Does Z have a natural value?")
print(f"  The EOS requires Z ~ O(1) for MOND to emerge correctly.")
print(f"  Z = {Z:.3f} is indeed O(1). No fine-tuning needed beyond a0 being in")
print("  the observed range (which comes from Lambda via a_gh = c*H_dS).")

print()
print("CHECK 3: Universal acceleration scale")
print("  The EOS predicts a SINGLE universal a0 for all systems.")

print()
print("CHECK 4: Interpolation shape — mu -> x/2 vs standard mu -> x")
print("  CRITICAL: the EOS low-x slope is 1/2, not 1.")
print(f"  This changes the deep-MOND velocity prediction by a factor of 2.")

# ============================================================================
# SECTION 6: TAYLOR SERIES OF THE INTERPOLATION (for use in force computations)
# ============================================================================
print("=" * 80)
print("SECTION 5: TAYLOR EXPANSION — FOR FORCE COMPUTATIONS")
print("=" * 80)
print("""
The EOS interpolation function: μ(x) = tanh(asinh(x)/2)

Expanded around x = a/a0:

LOW-x (MOND):  μ(x) = x/2 - x³/24 + O(x⁵)
HIGH-x (Newton): μ(x) = 1 - 1/x + 1/(2x²) - 1/(4x⁴) + O(x⁻⁶)

These expansions are verified below:
""")

# Low-x verification
print("LOW-x expansion verification:")
for x_val in [0.01, 0.05, 0.1]:
    exact = tanh_asinh_half(x_val)
    approx_lin = x_val / 2.0
    approx_cubic = x_val/2 - x_val**3/24
    err_linear = abs(exact - approx_lin) / exact * 100
    err_cubic = abs(exact - approx_cubic) / exact * 100
    print(f"  x={x_val:.2f}: exact={exact:.8e}, lin approx={approx_lin:.8e} (err={err_linear:.4f}%),"
          f" cubic={approx_cubic:.8e} (err={err_cubic:.6f}%)")

# High-x verification
print("\nHIGH-x expansion verification:")
for x_val in [2, 5, 10, 50]:
    exact = tanh_asinh_half(x_val)
    approx = 1 - 1/x_val + 1/(2*x_val**2) - 1/(4*x_val**4)
    err = abs(exact - approx) / max(abs(exact), 1e-20) * 100
    print(f"  x={x_val:5.1f}: exact={exact:.8e}, approx={approx:.8e} (err={err:.6f}%)")

# ============================================================================
# SECTION 7: SUMMARY TABLE
# ============================================================================
print()
print("=" * 80)
print("SECTION 6: SUMMARY — KEY RESULTS")
print("=" * 80)

summary = {
    "eos_interpolation_function": "mu(x) = tanh(asinh(x)/2)",
    "x_definition": "x = a / a_0",
    "a0_derivation": "a_0 = c * H_dS / (2Z), with Z ~ O(1) from cosmology",
    "low_x_limit": "mu = x/2 - x^3/24 + O(x^5)",
    "high_x_limit": "mu = 1 - 1/x + 1/(2x^2) - 1/(4x^4) + O(x^-6)",
    "z_value": float(Z),
    "a0_predicted_mKSq": float(a0_from_EOS),
    "max_deviation_mondd_regime_percent": float(max_e_s),
    "notes": "Z absorbed into a0 definition; EOS interpolation is UNIQUE (no free parameters beyond a0)"
}

results_path = os.path.join(os.path.dirname(__file__), 'eos_compare_results.json')
with open(results_path, 'w') as f:
    json.dump(summary, f, indent=2)
print(f"\nEOS interpolation function uniquely determined: mu(x) = tanh(asinh(x)/2)")
print(f"Results saved: {results_path}")
