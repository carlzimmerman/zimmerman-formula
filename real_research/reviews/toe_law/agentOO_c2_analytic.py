"""
agentOO Route 1, C2 — ANALYTIC k-expansion of the thermal self-energy.

The crude PV in C1 is noisy. Here we do the angular integral ANALYTICALLY and Taylor-expand the
integrand in k BEFORE the radial thermal integral, so the k^4 coefficient is a clean convergent
thermal moment integral whose SIGN we can read off exactly.

We use the standard finite-T scalar self-energy. The dispersion-shifting (real) part of the retarded
self-energy for the external mode chi(omega,k) coupling g chi phi phi /2 to a thermal bath of phi
(dispersion W_q = c_b q, occupation n(W_q)) is, after the Matsubara sum / standard reduction
(Le Bellac, Thermal Field Theory, ch. 6; Kapusta-Gale ch. 3):

  Re Sigma_T(omega,k) = (g^2/(4 pi^2)) * P \int_0^inf dq  q^2/W_q  n(W_q) * K(omega,k,q)

with the angular kernel (PV over cos theta = x, q+k line energy W_{q+k}=c_b sqrt(q^2+k^2+2qkx)):

  K = \int_{-1}^{1} dx (1/W_{q+k}) *
        [ 1/(omega - W_q - W_{q+k}) - 1/(omega + W_q + W_{q+k})
        + 1/(omega - W_q + W_{q+k}) - 1/(omega + W_q - W_{q+k}) ] / 2   (symmetrized, the n(W_q) factor pulled out by q<->q+k symmetry)

We do NOT need the exact closed K. Instead we Taylor-expand the ENTIRE on-shell integrand
Re Sigma(omega=c_chi k, k) in powers of k using sympy, integrate term-by-term against the thermal
weight, and read s4.

To make the expansion well-defined we keep the external line slightly off the bath cone (c_chi != c_b)
so there is no collinear divergence; then we study the sign of s4 as a function of (c_chi/c_b).
"""
import sympy as sp

# symbols
q, k, x, cchi, cb, w, T = sp.symbols('q k x c_chi c_b w T', positive=True)
# energies
Wq = cb*q
qpk = sp.sqrt(q**2 + k**2 + 2*q*k*x)
Wpk = cb*qpk
omega = cchi*k     # on-shell external

# the four energy denominators (retarded real part, PV understood); keep the standard combination
D1 = 1/(omega - Wq - Wpk)
D2 = 1/(omega + Wq + Wpk)
D3 = 1/(omega - Wq + Wpk)
D4 = 1/(omega + Wq - Wpk)

# kernel before thermal weight; 1/(W_q W_{q+k}) prefactor from 1/(4 W W) (the 4 absorbed in normalization)
kernel = (1/Wpk)*( (D1 - D2) + (D3 - D4) )

# Taylor-expand kernel in k to order k^7 (so on-shell, with omega = c_chi k, even powers up to k^6 survive)
print("Taylor expanding kernel in k (this is the heart of the calc)...")
ser = sp.series(kernel, k, 0, 8).removeO()
ser = sp.expand(ser)

# integrate over angle x in [-1,1] term by term
print("Angular integration...")
ser_ang = sp.integrate(ser, (x, -1, 1))
ser_ang = sp.simplify(ser_ang)

# collect powers of k
poly = sp.Poly(sp.expand(ser_ang), k)
print("\nAngular-integrated kernel, coefficients of k^n (each multiplies q^2/W_q * n(W_q) and integrates over q):")
for n in range(0,8):
    c = poly.coeff_monomial(k**n)
    c = sp.simplify(c)
    if c != 0:
        print("  k^%d : %s" % (n, c))
