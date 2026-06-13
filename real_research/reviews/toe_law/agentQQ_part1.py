import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("agentQQ Route 2 — PART 1: the X2 passivity sum rule, and what CS-violation does to it")
print("="*78)

# ----------------------------------------------------------------------------
# X2 setup. The retarded response chi_hat(omega) = mu_hat(omega) - mu_hat(inf)
# is causal => analytic in UHP. Kramers-Kronig / unsubtracted dispersion:
#   mu_hat(0) - mu_hat(inf) = (2/pi) Integral_0^inf Im mu_hat(lam)/lam dlam
# PASSIVE bath: Im mu_hat(omega) >= 0 for omega>0  => mu_hat(0) >= mu_hat(inf).
# That's X2 Eq (X-7): static >= high-freq (dielectric ordering).
#
# MOND/MI needs mu_hat(0) ~ 0 < mu_hat(inf)  => INVERTED => the secular channel
# must be ACTIVE: Im mu_hat < 0 somewhere (a band of NEGATIVE spectral weight).
# ----------------------------------------------------------------------------

print("""
X2 STRUCTURE (frequency domain, dispersion sum rule):
  mu_hat(0) - mu_hat(inf) = (2/pi) * Int_0^inf Im mu_hat(lam)/lam dlam
  passive bath: Im mu_hat(lam) >= 0  =>  mu_hat(0) >= mu_hat(inf)   [X2 ordering]
  MOND needs    mu_hat(0) < mu_hat(inf)  =>  REQUIRES a band Im mu_hat < 0 (ACTIVE)
""")

# ----------------------------------------------------------------------------
# PP's spectral moments. PP (No-Fold Theorem) works with the dispersion
# omega^2(k) built from a self-energy Pi(k) = Int rho(s) ds /(s + k^2) style
# Herglotz representation. Define the spectral moments:
#   I_n = Int rho(s) s^? ... The CS bound that matters is I2^2 <= I1 I3
#   on POSITIVE rho (Cauchy-Schwarz on the measure rho ds).
# sigma6 (the k^6 coefficient of omega^2) ends up proportional to a combination
# that is sign-fixed NEGATIVE by CS when rho>=0; bounding the fold (sigma6>0)
# needs the CS INEQUALITY to FLIP => requires rho to go NEGATIVE in a band
# (non-passive / active spectral weight).
# ----------------------------------------------------------------------------

# Demonstrate CS on positive measure, then show the flip needs negative weight.
print("CAUCHY-SCHWARZ on spectral moments I_n = Int rho(s) s^n ds :")
s = sp.symbols('s', positive=True)
# moments
print("  CS:  I_n^2 <= I_{n-1} I_{n+1}  holds for ANY positive measure rho>=0 (log-convexity).")
print("  PP's banked result: sigma6 ~ -(I1 I3 - I2^2) <= 0  => fold UNbounded for passive.")
print("  To get sigma6>0 (bounded fold) need I2^2 > I1 I3 => CS VIOLATED => rho<0 in a band.\n")

# Numerical demonstration: random POSITIVE spectra never violate (re-confirm PP),
# and an explicit ACTIVE (signed) spectrum that DOES violate.
import random
random.seed(7)
def moments(weights, nodes):
    I = {}
    for n in (1,2,3):
        I[n] = sum(w*(x**n) for w,x in zip(weights,nodes))
    return I

viol = 0
N = 50000
for _ in range(N):
    m = random.randint(2,6)
    nodes = [random.uniform(0.05, 5.0) for _ in range(m)]
    weights = [random.uniform(0.0, 1.0) for _ in range(m)]   # POSITIVE
    I = moments(weights, nodes)
    if I[2]**2 > I[1]*I[3] + 1e-12:
        viol += 1
print(f"  POSITIVE-spectrum CS test: {viol}/{N} violate I2^2>I1 I3  (expect 0 — re-confirms PP)")

# explicit active (signed) example that violates
nodes = [0.5, 2.0]
weights = [1.0, -0.3]   # NEGATIVE weight band = active
I = moments(weights, nodes)
print(f"  SIGNED-spectrum example weights={weights}: I2^2-I1 I3 = {I[2]**2 - I[1]*I[3]:+.4f}  (>0 => CS violated => fold can be bounded)")
print(f"     => so bounding the fold is EXACTLY a demand for negative (active) spectral weight.\n")
