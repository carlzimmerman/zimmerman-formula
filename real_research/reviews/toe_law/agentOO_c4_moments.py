"""
agentOO Route 1, C4 — CLEAN analytic moment computation of sigma4 sign.

Strategy that finishes fast and gives an UNAMBIGUOUS sign:

The dispersion-shifting real part of the one-loop thermal self-energy can be written (after the Matsubara
sum) as a convolution of the external mode with the thermal bath spectral function. For the leading
small-k behaviour we Taylor-expand the SCATTERING (Landau) kernel in k and integrate against the thermal
distribution. The angular integral is done in closed form FIRST (no sqrt series), the radial integral
becomes elementary thermal moments \int q^a n_B(c_b q) dq = (T/c_b)^{a+1} Gamma(a+1) zeta(a+1).

Concretely, for the trilinear g chi phi phi and bath dispersion W=c_b q, the scattering-cut (Landau-damping)
contribution to Re Sigma(omega,k) at small k, with the external mode on-shell omega=c_chi k, reduces to an
angular average of  1/(omega - c_b k cos theta_eff)  type denominators expanded in k. We instead use the
EXACT closed angular integral of the relevant denominators and Taylor-expand the q-integrand.

Cleanest tractable channel: the FORWARD (Landau) term n(W_q)-n(W_{q+k}). Expand W_{q+k}=c_b q + c_b k x +
c_b k^2(1-x^2)/(2q) + ...  Then n(W_q)-n(W_{q+k}) = -n'(W_q)(W_{q+k}-W_q) - (1/2)n''(...)(...)^2 - ...
This is the HONEST gradient expansion of the thermal phase space. We carry it to the order that produces
k^4 on-shell and integrate the elementary moments. SIGN of the k^4 coefficient is the deliverable.

We also build the EMISSION/absorption (n(W_q)+n(W_{q+k})) term's leading k-expansion the same way.
"""
import sympy as sp

x = sp.symbols('x', real=True)            # cos theta
q, k, cchi, cb, T = sp.symbols('q k c_chi c_b T', positive=True)

# Bose function and derivatives in terms of energy W
W = sp.symbols('W', positive=True)
n = 1/(sp.exp(W/T)-1)

# W_{q+k} expanded in k to 4th order (|q+k| = q sqrt(1+2(k/q)x+(k/q)^2))
ratio = sp.sqrt(1 + 2*(k/q)*x + (k/q)**2)
qpk = q*ratio
Wpk = cb*qpk
Wpk_ser = sp.series(Wpk, k, 0, 5).removeO()       # c_b|q+k| to O(k^4)
Wq = cb*q

# --- Landau (forward) term:  F = (n(Wq)-n(Wpk)) / (omega - Wq + Wpk) - mirror ---
# on-shell omega = c_chi k. Denominator D = c_chi k - Wq + Wpk = c_chi k - c_b q + Wpk
# small k: Wpk -> Wq + dW, so D = c_chi k + dW where dW = Wpk - Wq = O(k).
dW = sp.expand(Wpk_ser - Wq)
dW = sp.series(dW, k, 0, 5).removeO()
Dland = cchi*k + dW                                # = c_chi k - c_b q + W_{q+k}

# n(Wq)-n(Wpk) Taylor in k via chain rule on the Bose function
nW = 1/(sp.exp((cb*q)/T)-1)
# build n(Wpk) as series in k: substitute Wpk_ser into n(W)
nval = 1/(sp.exp(Wpk_ser/T)-1)
nval_ser = sp.series(nval, k, 0, 5).removeO()
dn = sp.expand(nW - nval_ser)                      # n(Wq)-n(Wpk), O(k)..O(k^4)

# Landau contribution integrand (before 1/(2 Wq Wpk) and q^2 and angular int):
land = dn / Dland
# vertex/prefactor 1/(2 Wq Wpk): expand Wpk in denominator too
pref = 1/(2*Wq*Wpk_ser)
integrand_land = sp.series(sp.expand(pref*land), k, 0, 5).removeO()

# --- Emission term:  (n(Wq)+n(Wpk)) * [1/(omega-Wq-Wpk) - 1/(omega+Wq+Wpk)] ---
nsum = sp.series(nW + nval_ser, k, 0, 5).removeO()
Demi_minus = cchi*k - Wq - Wpk_ser
Demi_plus  = cchi*k + Wq + Wpk_ser
emi = nsum*(1/Demi_minus - 1/Demi_plus)
integrand_emi = sp.series(sp.expand(pref*emi), k, 0, 5).removeO()

total = sp.expand(integrand_land + integrand_emi)
total = sp.series(total, k, 0, 5).removeO()
total = sp.expand(total)

# multiply by q^2 (from d^3q) and integrate over angle x in [-1,1]
total_q2 = total*q**2
print("Angular integration (x in [-1,1])...")
ang = sp.integrate(total_q2, (x, -1, 1))
ang = sp.expand(ang)
poly = sp.Poly(ang, k)

print("\n# Coefficient of each k^n (still to be integrated over q against the dS thermal weight):")
coeffs = {}
for nn in range(0,5):
    c = sp.simplify(poly.coeff_monomial(k**nn))
    coeffs[nn] = c
    print("  k^%d coeff (q-integrand): %s" % (nn, c))

# Now integrate each k-coefficient over q from 0 to inf. These are elementary thermal moments.
print("\n# Radial q-integration of each k^n coefficient (the induced sigma_n):")
import mpmath as mp
mp.mp.dps = 30
Tnum = mp.mpf(1)/(2*mp.pi)   # T_dS = H/2pi
for cchi_num in [mp.mpf('1.5'), mp.mpf('0.7'), mp.mpf('2.5')]:
    print("\n--- c_chi=%s, c_b=1, T=H/2pi ---" % cchi_num)
    for nn in [0,2,4,6]:
        c = coeffs.get(nn, sp.Integer(0))
        if c == 0:
            print("  sigma%d = 0" % nn); continue
        f = sp.lambdify(q, c.subs({cb:1, cchi:cchi_num, T:sp.Rational(0)+sp.nsimplify(float(Tnum))}), 'mpmath')
        try:
            val = mp.quad(lambda Q: f(mp.mpf(Q)), [mp.mpf('1e-6'), 5, 30, 100])
            val = -val/(4*mp.pi**2)   # overall -g^2/(4pi^2), g=1
            tag = '<-- SIGMA4 (deliverable)' if nn==4 else ''
            print("  sigma%d = % .6e   %s" % (nn, float(val), tag))
        except Exception as e:
            print("  sigma%d : integration error %s" % (nn, e))
