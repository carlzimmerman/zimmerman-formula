import sympy as sp

# ============================================================
# STEP 3: Borel-plane structure of the ONLY factorially-divergent
# free series -- the thermal (Planck / sinh^{-2}) worldline density.
# What non-perturbative form does resurgence force from it?
# ============================================================
om, k, n, s, z = sp.symbols('omega kappa n s z', positive=True)

# The free pullback worldline kernel is sinh^{-2}(kappa tau/2). Its small-tau
# (perturbative) expansion is the Laurent series 1/sinh^2(y) about y=0:
y = sp.symbols('y')
ser = sp.series(1/sp.sinh(y)**2, y, 0, 16)
print("1/sinh^2(y) about y=0:")
sp.pprint(ser)
# Coefficients are (rational) ~ Bernoulli; the asymptotic series in the
# DUAL (large-order) sense. Key fact: 1/sinh^2 has DOUBLE POLES at y = i pi m,
# m in Z\{0}. These are the Borel/Stokes singularities.
print()
print("Poles of 1/sinh^2(kappa tau/2) in complex tau: kappa tau/2 = i pi m")
print(" => tau_m = 2 pi i m / kappa, m = +-1, +-2, ...  (DOUBLE poles)")
print()
# Resurgence reading: the action (Borel singularity location) is the distance
# to the nearest singularity: |tau_1| = 2 pi / kappa = u  (the Deser-Levin u!).
# The non-perturbative scale is e^{-S} with S ~ (nearest singularity)*(omega).
print("Nearest singularity distance = 2 pi/kappa = u  ==> the instanton action.")
print("Stokes/non-perturbative weight ~ exp(- omega * 2pi/kappa) = exp(-2pi omega/kappa)")
print("  -- a SIMPLE EXPONENTIAL e^{-A omega}, A = 2pi/kappa.  NOT a stretched exp.")
print()

# ============================================================
# (3b) What ROOT/POWER does this Borel singularity carry?
# Double pole of 1/sinh^2 at tau_m  ==>  Borel transform has, near each
# singularity, what type? Map: a double pole in the function corresponds,
# in the large-order coefficients, to c_n ~ n / (tau_1)^n (n times geometric):
# that is a Borel singularity that is a DOUBLE POLE, not a branch point.
# A double pole in the Borel plane => the trans-series alien term is a pure
# exponential times a POLYNOMIAL prefactor (log-free), NO fractional power.
# ============================================================
# Confirm coefficient growth of 1/sinh^2 series ~ n (linear x geometric):
coeffs=[]
S = sp.series(1/sp.sinh(y)**2, y, 0, 40).removeO()
P = sp.Poly(S*y**2, y)  # multiply by y^2 to clear the leading 1/y^2
print("Leading small-y: 1/sinh^2 ~ 1/y^2 - 1/3 + y^2/15 - ...")
# Extract even coefficients a_{2j} of the regular part:
reg = sp.series(1/sp.sinh(y)**2 - 1/y**2, y, 0, 30).removeO()
terms = sp.Poly(reg, y).all_coeffs()[::-1]
print("regular-part coeffs (j: coeff of y^{2j}) and ratio to (2j+1)/pi^{2j}:")
import mpmath as mp
mp.mp.dps=30
for j in range(1, 12):
    cj = reg.coeff(y, 2*j)
    if cj==0: continue
    val = mp.mpf(sp.N(cj,30))
    # predicted large-order from m=1 double pole: a_{2j} ~ (2j+1)*2/pi^{2j+2}*(-1)^? 
    pred = (2*j+1)*2/mp.pi**(2*j+2)
    print(f" j={j:2d}  a_2j={float(val): .6e}  (2j+1)*2/pi^(2j+2)={float(pred): .6e}  ratio={float(val/pred): .6f}")
