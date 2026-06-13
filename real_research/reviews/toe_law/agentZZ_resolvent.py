import sympy as sp
# ============================================================
# ZZ1b - THE DECISIVE STRUCTURAL TEST (real variation, not Fourier heuristic)
# ============================================================
# Quasi-static, weak field.  Metric potentials Phi (lapse: N=1+Phi), Psi (spatial).  a_i = d_i Phi.
# A spatial-nonlocal slip operator reads a SMOOTHED field via the resolvent
#       (1 - L^2 nabla^2) Phi_L = Phi          i.e. Phi_L = K_L * Phi.
# We implement the resolvent as an AUXILIARY FIELD chi with its own constraint, the standard
# *local* way to make a finite-range nonlocal operator (this is the ONLY ghost-free way -- a
# resolvent with the RIGHT sign; a Yukawa Green function is the propagator of a massive field
# of mass m = 1/L).  This auxiliary-field form is what lets us check ghosts honestly (ZZ3).
#
# Lagrangian sketch for the slip sector (the spatial analog of agentDD's W(Y_a)(D.b)):
#   S_slip = Int d^3x sqrt(g) [ chi (Phi - chi)/L^2  - (something)(grad chi)^2  + B(chi) * (slip generator) ]
# but to test the KEYING we do not need the full action -- we need the LAPSE RESPONSE of the
# key.  The key is now chi = K_L * Phi (the smoothed lapse potential).  Two sub-questions:
#
#   Q1 (the KK question, spatial version): on a static background, does the operator collapse to
#       a local theory?   NO for a spatial kernel (chi != Phi pointwise).  Good -- KK-1 does not
#       transfer mechanically.
#
#   Q2 (the keying question, the real kill): the pollution = the lapse response of the key in
#       the Hamiltonian constraint.  delta(key)/delta(Phi) for the LOCAL key was (a0 r/c^2)^-1
#       enhanced because Y_a ~ (d Phi)^2 -> the variation lands TWO derivatives -> geometric
#       slip/r^2.  For the SMOOTHED key chi = K_L Phi:
#            delta(chi)/delta(Phi) = K_L          (the kernel itself, a SMOOTHING, |Khat|<=1)
#       So IF the key is LINEAR in the smoothed potential, the lapse response is just K_L --
#       a BOUNDED smoothing operator, NOT a derivative.  The (a0 r/c^2)^-1 enhancement came from
#       the key being QUADRATIC in the ACCELERATION (two derivatives).  Spatial smoothing of the
#       POTENTIAL (not the acceleration) replaces "two derivatives" by "two derivatives times K_L".
#
# THE FORK that decides everything:
#   (A) If the spatial key still keys on the ACCELERATION-magnitude (a.a) -- needed to reproduce
#       MOND's a0-keying / nu(g_bar/a0) -- then even smoothed, delta(key)/delta(Phi) carries the
#       SAME two derivatives (now dressed by K_L): the enhancement survives, suppressed only at
#       k >> 1/L.  At the halo scale (k ~ 1/r, and we need L <~ r to keep the slip) K_L ~ 1.
#   (B) If the spatial key keys on the POTENTIAL VALUE Phi_L (not its gradient), it is NOT
#       acceleration-keyed -> it does NOT produce nu(g_bar/a0) (the wrong observable; constant
#       or potential-keyed slip, a dead branch in agentY/W).
#
# Test BOTH branches explicitly on the quasi-static rr-constraint slip and the eqN feed.

r, L, alpha, G, pi_ = sp.symbols('r L alpha G pi', positive=True)
# weak-field radial profiles (functions of r); use agentY/DD conventions
Phi = sp.Function('Phi')(r)        # lapse potential, N = 1+Phi
Psi = sp.Function('Psi')(r)        # spatial potential
rho = sp.Function('rhob')(r)
# acceleration magnitude squared key  y^2 ~ (Phi')^2 / alpha^2  (a0 = eps*alpha grading)
Phip = sp.diff(Phi, r)
Phipp= sp.diff(Phi, r, 2)

# ---- BRANCH A: acceleration-keyed but SMOOTHED gradient ----
# smoothed acceleration a_L = K_L * Phi'.  Resolvent: (1 - L^2 Lap) a_L = Phi'.
# In radial form, to leading (long-wavelength) order a_L = Phi' - L^2 Phi''' + O(L^4).
# delta(key)/delta(Phi):  key_A = a_L^2/alpha^2; lapse response = 2 a_L/alpha^2 * delta(a_L).
# delta(a_L) under Phi->Phi+eta is K_L * eta' = eta' - L^2 eta''' + ...
# The IBP-enhanced geometric piece in eqN comes from the SECOND derivative on eta surviving IBP.
# Expand the kernel as a derivative series to see whether L^2 terms CANCEL the leading enhancement
# or merely ADD higher-derivative dressings.
eta = sp.Function('eta')(r)
KL = lambda f: f - L**2*sp.diff(f, r, 2)   # leading resolvent expansion 1/(1-L^2 Lap) ~ 1 - L^2 Lap (sign!)
da_L = KL(sp.diff(eta, r))                  # delta(a_L)
print("delta(a_L) [branch A, leading kernel] =", sp.expand(da_L))
# The lapse-response density that IBPs into the enhanced geometric eqN feed:
# ~ a_L * delta(a_L); the dangerous term is the one with eta'' (the second-derivative-on-test-fn
# that IBPs to slip/r^2).  Isolate the eta'' coefficient and the eta'''' (kernel) coefficient.
abar = Phip  # background smoothed accel ~ Phi' (leading)
resp = sp.expand(abar*da_L)
print("\na_L*delta(a_L) leading:", resp)
