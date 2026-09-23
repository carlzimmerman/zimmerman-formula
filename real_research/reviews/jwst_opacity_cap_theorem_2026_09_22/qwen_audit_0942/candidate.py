import os
import json
import sys
from sympy import symbols, Rational, integrate, cos, sin, pi, sqrt, simplify, expand

# Get mode and inputs
mode = os.environ.get('ORCH_MODE', 'main')

# Define the Thomson kernel P(mu) = 3(1+mu^2)/8 on [-1,1]
# For the positive control, we use the SAME kernel but verify the integration explicitly.
# For the negative control, use isotropic P(mu) = 1/2 on [-1,1]

if mode == 'main' or mode == 'positive':
    # Thomson kernel: P(mu) = 3(1+mu^2)/8
    def P(mu):
        return Rational(3, 8) * (1 + mu**2)
    # Integration limits are standard [-1, 1]
    mu_lower, mu_upper = -1, 1
else:    # negative
    # Isotropic kernel: P(mu) = 1/2 on [-1,1]
    def P(mu):
        return Rational(1, 2)
    mu_lower, mu_upper = -1, 1

# Compute angular moments
mu, s, z, k, phi = symbols('mu s z k phi', real=True)

# E[mu^2] = integral_{-1}^{1} mu^2 * P(mu) dmu
E_mu2 = integrate(P(mu) * mu**2, (mu, mu_lower, mu_upper))

# E[1-mu^2] = integral_{-1}^{1} (1-mu^2) * P(mu) dmu
E_1mu2 = integrate(P(mu) * (1 - mu**2), (mu, mu_lower, mu_upper))

# Verify normalization: E[1] = 1
E_1 = integrate(P(mu), (mu, mu_lower, mu_upper))

# K[z^2] = E[z_new^2] where z_new = z*mu + sqrt(s-z^2)*sqrt(1-mu^2)*cos(phi)
# E[z_new^2] = z^2*E[mu^2] + (s-z^2)*E[1-mu^2]*E[cos^2(phi)]
# For uniform azimuth, E[cos^2(phi)] = 1/2
E_cos2_phi = Rational(1, 2)

K_z2 = z**2 * E_mu2 + (s - z**2) * E_1mu2 * E_cos2_phi
K_z2 = expand(K_z2)

# The jump bracket is E[(z_new - z)^2] = K[z^2] - 2z*E[z_new] + z^2
# E[z_new] = z*E[mu] + sqrt(s-z^2)*sqrt(1-mu^2)*E[cos(phi)] = 0 (since E[mu]=0 and E[cos]=0)
E_mu = 0
E_cos_phi = 0
E_z_new = z * E_mu + sqrt(s - z**2) * sqrt(1 - mu**2) * E_cos_phi

jump_bracket = K_z2 - 2*z*E_z_new + z**2
jump_bracket = expand(jump_bracket)

# For Thomson, we expect K[z^2] = 3s/10 + z^2/10 and jump_bracket = 3s/10 + 11z^2/10
# Check if the coefficients match
coeff_s_K = K_z2.coeff(s)
coeff_z2_K = K_z2.coeff(z**2)
coeff_s_bracket = jump_bracket.coeff(s)
coeff_z2_bracket = jump_bracket.coeff(z**2)

# For Thomson: coeff_s_K = 3/10, coeff_z2_K = 1/10, coeff_s_bracket = 3/10, coeff_z2_bracket = 11/10
# For isotropic: E[mu^2] = 1/3, E[1-mu^2] = 2/3
# K[z^2] = z^2*(1/3) + (s-z^2)*(2/3)*(1/2) = z^2/3 + s/3 - z^2/3 = s/3
# jump_bracket = s/3 - 0 + z^2 = s/3 + z^2

# Generator equation for z^2: L[z^2] = 2z + k*(K[z^2] - z^2)
# K[z^2] - z^2 = coeff_s_K*s + (coeff_z2_K - 1)*z^2
L_z2 = 2*z + k*(coeff_s_K*s + (coeff_z2_K - 1)*z**2)

# Integrate L[z^2] over [0,T] and take expectations
# E[Z^2] = 2*E[integral_0^T z dt] + E[integral_0^T k*(K[z^2] - z^2) dt]
# Pathwise: integral_0^T 2z dt = s_T - s_0 = 1, so E[integral_0^T z dt] = 1/2
# E[Z^2] = 1 + E[integral_0^T k*(K[z^2] - z^2) dt]
# = 1 + E[integral_0^T k*(coeff_s_K*s + (coeff_z2_K - 1)*z^2) dt]
# = 1 + coeff_s_K*Qs + (coeff_z2_K - 1)*Qz

Qs, Qz, EZ2, ED2 = symbols('Qs Qz E_Z2 E_D2')

# E[Z^2] = 1 + coeff_s_K*Qs + (coeff_z2_K - 1)*Qz
EZ2_eq = 1 + coeff_s_K*Qs + (coeff_z2_K - 1)*Qz

# From the martingale M_t = t + F(s_t) - z_t, terminal value D
# [M]_T = integral_0^T k*jump_bracket dt
# E[D^2] = E[integral_0^T k*jump_bracket dt] = coeff_s_bracket*Qs + coeff_z2_bracket*Qz
ED2_eq = coeff_s_bracket*Qs + coeff_z2_bracket*Qz

# Eliminate Qz from the two equations
# From EZ2_eq: Qz = (EZ2 - 1 - coeff_s_K*Qs) / (coeff_z2_K - 1)
# Substitute into ED2_eq
Qz_expr = (EZ2 - 1 - coeff_s_K*Qs) / (coeff_z2_K - 1)
ED2_eliminated = coeff_s_bracket*Qs + coeff_z2_bracket*Qz_expr
ED2_eliminated = expand(ED2_eliminated)

# Collect terms in Qs and EZ2
coeff_Qs = ED2_eliminated.coeff(Qs)
coeff_EZ2 = ED2_eliminated.coeff(EZ2)
const_term = ED2_eliminated.subs({Qs: 0, EZ2: 0})

# The target identity is E[D^2] = (2/3)*Qs + (11/9)*(1 - E[Z^2])
# = (2/3)*Qs + 11/9 - (11/9)*E[Z^2]
# So coeff_Qs should be 2/3, coeff_EZ2 should be -11/9, const_term should be 11/9

# Check the coefficients
check_coeff_Qs = bool(coeff_Qs == Rational(2, 3))
check_coeff_EZ2 = bool(coeff_EZ2 == Rational(-11, 9))
check_const_term = bool(const_term == Rational(11, 9))

# The full check is that all three coefficients match
bracket_certificate = check_coeff_Qs and check_coeff_EZ2 and check_const_term

# For the negative control (isotropic), the coefficients should be different
# E[mu^2] = 1/3, E[1-mu^2] = 2/3
# K[z^2] = z^2*(1/3) + (s-z^2)*(2/3)*(1/2) = z^2/3 + s/3 - z^2/3 = s/3
# So coeff_s_K = 1/3, coeff_z2_K = 0
# jump_bracket = s/3 + z^2
# So coeff_s_bracket = 1/3, coeff_z2_bracket = 1
# The elimination should give different coefficients

# Output the results
results = {
    'E_mu2': str(E_mu2),
    'E_1mu2': str(E_1mu2),
    'E_1': str(E_1),
    'K_z2': str(K_z2),
    'jump_bracket': str(jump_bracket),
    'coeff_s_K': str(coeff_s_K),
    'coeff_z2_K': str(coeff_z2_K),
    'coeff_s_bracket': str(coeff_s_bracket),
    'coeff_z2_bracket': str(coeff_z2_bracket),
    'ED2_eliminated': str(ED2_eliminated),
    'coeff_Qs': str(coeff_Qs),
    'coeff_EZ2': str(coeff_EZ2),
    'const_term': str(const_term),
    'check_coeff_Qs': check_coeff_Qs,
    'check_coeff_EZ2': check_coeff_EZ2,
    'check_const_term': check_const_term,
    'bracket_certificate': bracket_certificate
}

# Print to stderr for diagnostics
for key, value in results.items():
    print(f'{key}: {value}', file=sys.stderr)

# Output the JSON result
output = {
    'protocol': 2,
    'complete': True,
    'checks': {
        'bracket_certificate': bracket_certificate
    },
    'measurements': results
}

print(json.dumps(output))