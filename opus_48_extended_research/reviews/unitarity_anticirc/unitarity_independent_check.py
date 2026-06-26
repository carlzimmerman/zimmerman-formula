"""
INDEPENDENT adversarial verification of the UNITARITY anti-circularity claim.
I do NOT reuse the claim's scripts. I rebuild each algebraic assertion from scratch
and try to BREAK it (find a path from a positivity/unitarity condition to a unique N).

Anti-circularity rule: kappa=1/2 / 8pi / density-route must NOT be smuggled in.
N (the MOND-scale normalization, the coefficient that maps to kappa) is kept a free
symbol throughout. We only reference the value 1/2 at the very end to LOCATE kappa,
never to manufacture a forcing.
"""
import sympy as sp

print("="*78)
print("SETUP: Keldysh / in-in doubled action with a FREE normalization N")
print("="*78)

# Free MOND-scale normalization (maps to kappa). lambda = an arbitrary rescaling.
N, lam = sp.symbols('N lambda', positive=True)
w, T = sp.symbols('omega T', positive=True)   # frequency, KMS temperature
qp, qm = sp.symbols('q_+ q_-', real=True)      # Keldysh average / difference
# rho(w): a spectral density shape (dimensionless after factoring N). Generic positive shape.
rho = sp.Function('rho')(w)
# coth thermal factor
coth = sp.coth(w/(2*T))

print("\nKeldysh variables: q_+ = (q1+q2)/2 [average/physical], q_- = q1-q2 [difference].")
print("Physical EOM = delta S / delta q_-  evaluated at q_- -> 0  => q_- - LINEAR.")
print("N enters every kernel as a homogeneous dimensionful magnitude.")

print("\n" + "="*78)
print("TEST 1 — SK REALITY (the explicit i): is it N-invariant?")
print("="*78)
# In SK/in-in, the q_- - quadratic 'noise' term carries an explicit i (the Feynman-Vernon
# influence phase): contribution ~ i * (noise) * q_-^2, with noise = N^2 * Nz_shape.
# The q_- - linear 'drift/dissipation' term is REAL: ~ (drift) * q_+ * q_-.
# SK reality is the statement: noise-term imaginary, drift-term real. Test N-scaling.
Nz_shape = rho*coth                  # noise spectral shape (>=0 demanded by positivity)
noise_term  = sp.I * N**2 * Nz_shape * qm**2       # imaginary by construction
drift_term  = N**2 * rho * qp * qm                 # real (here both at N^2; see Test 4)

# Under N -> lam*N:
noise_resc = noise_term.subs(N, lam*N)
drift_resc = drift_term.subs(N, lam*N)
# Reality is a property of the COEFFICIENT (is it i*real vs real). Rescaling by positive lam
# multiplies by a positive real -> cannot change "imaginary" into "real".
print("noise term  :", noise_term)
print("  is purely imaginary coefficient? ", sp.im(sp.I*N**2) != 0 and sp.re(sp.I*N**2)==0)
print("under N->lam*N:", noise_resc, " -> ratio =", sp.simplify(noise_resc/noise_term))
print("drift term  :", drift_term)
print("under N->lam*N: ratio =", sp.simplify(drift_resc/drift_term))
print(">>> Both rescale by lam^2 (positive). Reality/imaginariness UNCHANGED for any N.")
print(">>> SK reality is a PHASE/SIGN condition, N-INVARIANT. It cannot pin |N|.")

print("\n" + "="*78)
print("TEST 2 — POSITIVITY Nz(w) >= 0 (noise spectral density): N-invariant SIGN?")
print("="*78)
# Positivity of the influence-functional noise kernel: Nz(w) = N^2 * rho(w) * coth(w/2T) >= 0.
Nz = N**2 * rho * coth
Nz_resc = Nz.subs(N, lam*N)
print("Nz(w)      =", Nz)
print("Nz scaling under N->lam*N: factor =", sp.simplify(Nz_resc/Nz), " (positive prefactor)")
print(">>> The inequality Nz>=0 demands rho>=0 and coth>0 (it does for w,T>0);")
print(">>> it fixes the SIGN of N^2 (already +). It is INVARIANT under N->lam*N.")
# Is the inequality ever SATURATED at a finite interior N (which could pin a scale)?
dNz_dN = sp.diff(Nz, N)
print("d Nz/dN =", sp.simplify(dNz_dN), " -> stationary point in N at N=",
      sp.solve(sp.Eq(dNz_dN,0), N))
print(">>> Only stationary point is N=0 (the boundary). NO interior saturation =>")
print(">>> positivity is an OPEN inequality, cannot pin a finite scale by saturation.")

print("\n" + "="*78)
print("TEST 3 — KMS / FDT: noise/dissipation RATIO. Common N cancels?")
print("="*78)
# Fluctuation-dissipation: Nz(w) = coth(w/2T) * Im G_R(w).
# If BOTH kernels are same order in N (the integrated-out dS bath gives both at N^2):
ImGR_sameorder = N**2 * rho          # dissipation kernel, N^2
Nz_fdt         = N**2 * rho * coth   # noise kernel, N^2
ratio = sp.simplify(Nz_fdt / ImGR_sameorder)
print("Im G_R (N^2) =", ImGR_sameorder)
print("Nz     (N^2) =", Nz_fdt)
print("FDT ratio Nz/ImGR =", ratio, "  <-- N CANCELS; only fixes coth (the temperature T).")
print(">>> FDT fixes the noise/dissipation RATIO and T, NOT the common scale N.")

print("\n" + "="*78)
print("TEST 4 — THE STEELMANNED FAILURE MODE: MIXED-ORDER FDT (drift~N^1, noise~N^2)")
print("="*78)
# Could a mixed-order FDT pin N? Drift linear in N, noise quadratic in N.
Q = sp.symbols('Q', positive=True)   # a second, independent coupling/observable
drift_N1 = N * rho                    # hypothetical drift at order N^1
noise_N2 = N**2 * rho * coth          # noise at order N^2
# An FDT-like relation tying them with an external scale Q: noise = Q * drift * coth ?
eq_mixed = sp.Eq(noise_N2, Q * drift_N1 * coth)
solN = sp.solve(eq_mixed, N)
print("Mixed-order relation  noise(N^2) = Q * drift(N^1) * coth :")
print("  solve for N =>", solN)
print(">>> MIXED-ORDER FDT IS SOLVABLE for N (N = Q). So unitarity-class CAN pin N")
print("    ONLY IF the two kernels sit at DIFFERENT powers of N.")
print(">>> BUT: this requires a SECOND independent scale Q (here the external coupling).")
print("    It trades one free scale (N) for another (Q) -> derives NOTHING absolute.")

print("\n" + "="*78)
print("TEST 5 — THE ACTUAL ROUTE-E OBJECT: conservative EVEN kernel, Im G_R = 0")
print("="*78)
# Route-E uses a CONSERVATIVE even memory kernel: no dissipation => Im G_R = 0.
ImGR_conservative = sp.Integer(0)
print("Route-E dissipation kernel Im G_R =", ImGR_conservative, " (conservative even kernel)")
# FDT with zero dissipation:
print("FDT: Nz = coth * Im G_R =", sp.simplify(coth*ImGR_conservative))
print(">>> Im G_R = 0  => the dissipative spectral density is IDENTICALLY ZERO.")
print(">>> There is NO dissipative magnitude for positivity/FDT to constrain.")
print(">>> Unitarity is VACUOUS on the magnitude for the conservative kernel.")
print(">>> Only the N-homogeneous even/real structure + q_+ kinetic positivity survive,")
print("    and (Tests 1-3) those are all N-invariant.")
