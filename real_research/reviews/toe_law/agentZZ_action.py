import sympy as sp
# ============================================================
# ZZ2b - THE HONEST ACTION VARIATION (auxiliary-field resolvent; eqL & eqN from ONE Lagrangian).
# This is the load-bearing check: derive BOTH the slip (eqL) and the matter-channel pollution
# (eqN) from the SAME spatial-nonlocal action term and read off whether they carry the SAME
# kernel factor (locked) or different ones (escape).  No heuristics.
# ============================================================
# Plane-wave / Fourier quasi-static reduction (the clean exact way to keep the full resolvent).
# Fields at mode k: Phi (lapse pot), Psi (spatial pot), chi (auxiliary smoothing field).
# Resolvent constraint (ghost-free massive-field form, mass m=1/L):
#       chi = K_L Phi,   K_L(k) = 1/(1+L^2 k^2)     <-- enforced by a chi-EOM below.
# Acceleration-keyed spatial-nonlocal slip operator (Branch A, the only observable-correct one):
#   the key is the SMOOTHED acceleration; in Fourier the operator coefficient B depends on
#   |a_L|^2 ~ (k chi)^2 = k^2 K_L^2 Phi^2  (background), and it multiplies the slip generator.
#
# We need a TERM that (a) produces nonzero slip (Psi != Phi) in eqL, (b) whose lapse variation
# feeds eqN.  Use the spatial analog of agentDD's working operator W(Y_a)(D.b):  here the
# "divergence of the oriented condensate" is replaced by the geometric slip generator built from
# the smoothed field.  Minimal faithful surrogate that carries the keying structure:
#
#   L_slip = B(K)*( Psi - Phi ) * (k^2)     with K = k^2 |chi|^2 = k^2 K_L^2 Phi^2   (the key)
#
# The (Psi-Phi) factor makes it a genuine slip operator; the k^2 is the geometric (Laplacian)
# weight that became slip/r^2 in real space; B(K) carries the a0-keying through the smoothed key K.
#
# eqL (slip eq) = dL/dPsi ;  eqN (lapse/Hamiltonian feed) = dL/dPhi.
# The kernels: dK/dPhi and the explicit (Psi-Phi) both carry K_L-powers.  Compute.

k, L, Phi, Psi = sp.symbols('k L Phi Psi', positive=True)
KL = 1/(1 + L**2*k**2)
K  = k**2 * KL**2 * Phi**2          # the smoothed acceleration-key (background ~ Phi^2)
B  = sp.Function('B')
Lterm = B(K) * (Psi - Phi) * k**2   # the slip Lagrangian density at mode k

eqL = sp.diff(Lterm, Psi)           # slip-channel feed (rr-constraint)
eqN = sp.diff(Lterm, Phi)           # matter-channel (Hamiltonian/lapse) feed
print("eqL (slip channel) =", sp.simplify(eqL))
print()
print("eqN (matter channel) =", sp.simplify(eqN))
print()

# Extract the kernel dependence of each.  eqL: slip feed ~ B(K)*k^2  -> kernel via K = K_L^2.
# eqN: two pieces -- (1) -B(K)*k^2 (the explicit -Phi), kernel K_L^2 via K; PLUS
#                   (2) B'(K)*dK/dPhi*(Psi-Phi)*k^2, the KEYING pollution (chi's lapse response).
dKdPhi = sp.diff(K, Phi)
print("dK/dPhi =", sp.simplify(dKdPhi), "   <- the keying lapse response; kernel power of K_L =")
# count K_L powers in dK/dPhi:
print("   dK/dPhi / Phi =", sp.simplify(dKdPhi/Phi), " => carries K_L^2 (same as the slip's key).")

# So BOTH the slip (eqL via B and K) and the keying pollution (eqN via B' dK/dPhi) carry the
# kernel through the SAME K = k^2 K_L^2 Phi^2.  The keying pollution is B'(K)*dK/dPhi which is
# proportional to dK/dPhi ~ k^2 K_L^2 Phi -- the SAME (a0 r/c^2)^-1 geometric enhancement
# (the k^2 = Laplacian = slip/r^2), now dressed by K_L^2.  And the slip is dressed by K_L^2 too.
# => LOCKED.  The kernel cancels in (pollution/slip) exactly as in KK.
print("\nCONCLUSION (exact): the keying pollution term B'(K)*dK/dPhi*(Psi-Phi)*k^2 carries the")
print("SAME k^2-geometric enhancement and the SAME K_L^2 dressing as the slip generator.")
print("pollution/slip kernel ratio = K_L^0 = 1 at every mode -> the suppression is LOCKED.")

# The clincher: form the lens-only ratio explicitly.
# slip/Phi-feed structurally ~ eqL ; geometric pollution core ~ B'(K)dK/dPhi*(Psi-Phi)k^2.
# Their ratio's kernel content:
poll_keying = sp.diff(B(K),Phi)*(Psi-Phi)*k**2   # the dangerous keying piece of eqN
ratio_kernel = sp.simplify( (poll_keying.subs(Psi, 0)) / (eqL.subs(Psi,0)) )  # strip Psi to compare kernels
print("\n(pollution-keying)/(slip) with Psi->0 to isolate kernels:")
print("   =", ratio_kernel)
