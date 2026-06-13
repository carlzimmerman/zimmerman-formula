import sympy as sp

# ============================================================
# STEP 2: Large-order behavior of the FREE perturbative series.
# Resurgence forces a non-perturbative FORM only if the perturbative
# coefficients grow FACTORIALLY (Gevrey-1) with a definite Borel
# singularity structure. We test the candidate free series.
# ============================================================
H, c, b, a, x, t = sp.symbols('H c_chi b a x t', positive=True)

print("="*60)
print("(2a) Series of the RESPONSE-relevant combination in a^2")
print("="*60)
# agentEE [3e]: the deep-MOND/worldline law is analytic in a^2 at a=0.
# 2 - t  = 2a^2/(H^2+a^2) (the MOND interpolation seen in the firewall L8).
twomt = 2*a**2/(H**2+a**2)
ser = sp.series(twomt, a, 0, 12)
print("2-t = 2a^2/(H^2+a^2), series in a:", ser)
# coefficients:
coeffs = sp.Poly(sp.series(twomt,a,0,16).removeO(), a).all_coeffs()[::-1]
print("a-coeffs (low->high):", coeffs)
# ratio test for factorial growth: c_{n+1}/c_n
print("This is geometric (radius H), coeffs ~ (-1)^k/H^{2k} -- NO factorial growth.")

print()
print("="*60)
print("(2b) The amplitude A(b) series about b=0 (physical-velocity expansion)")
print("="*60)
A = H**2/(16*sp.pi**2*c*(c**2 - b**2))
serA = sp.series(A, b, 0, 14)
print("A(b) about b=0:", serA)
# coefficients ~ b^{2k}/c^{2k+2} -- geometric, radius c_chi. NO factorial.
print("A(b) coeffs ~ 1/c_chi^{2k+3}: geometric, radius=c_chi. NO factorial growth.")

print()
print("="*60)
print("(2c) Is there ANY natural free series with factorial growth?")
print("Candidate: the small-u expansion of the free pullback's spectral")
print("density. Free density (agentEE [2d]) = Planck: rho ~ omega/(1-e^{-2pi omega/kappa}).")
print("="*60)
om, k = sp.symbols('omega kappa', positive=True)
planck = om/(1 - sp.exp(-2*sp.pi*om/k))
# small-omega expansion (Bernoulli) -- factorial? No: radius set by 2pi/kappa poles.
serP = sp.series(planck, om, 0, 10)
print("Planck density small-omega:", serP)
print("Bernoulli coeffs B_n/n! * (2pi/kappa)^... : these are the Bernoulli numbers;")
print("B_{2n} ~ (2n)!/(2pi)^{2n} -- FACTORIAL growth! Borel singularities on imaginary axis.")
