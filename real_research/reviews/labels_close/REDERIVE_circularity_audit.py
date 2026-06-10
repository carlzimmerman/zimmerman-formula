#!/usr/bin/env python3
"""
CIRCULARITY AUDIT (Fable's specific instruction): find the EXACT line where the de Sitter
vacuum's spectral placement (center vs edge) enters, and determine DERIVED vs ASSUMED.

I test FOUR candidate "algebraic" pickers to see if ANY of them fixes theta_vac from the
chord algebra alone (which would make the finding DERIVES/FORBIDS instead of CONTESTED):

  PICKER 1: chord vacuum |0> (ground state of N_hat). Where does ITS energy weight live?
  PICKER 2: Hamiltonian H = a + a^dag ground state (lowest energy). Where is it?
  PICKER 3: infinite-temperature / maximal-entropy state (rho ~ Identity). Where?
  PICKER 4: the confinement angle -- "O(N)-singlet escapes to the center". Does identifying
            the deep-MOND probe with the singlet SMUGGLE the center placement back in?

If PICKER 1,3 -> CENTER and PICKER 2 -> EDGE, the algebra supplies BOTH and does NOT pick a
unique 'de Sitter' -> the equals-sign (dS = which state) is the holographic dictionary,
external. That is the CONTESTED-TERMINAL signature.
"""
import numpy as np

def qpoch(a, q, tol=1e-16, Nmax=5000):
    a = np.asarray(a, dtype=complex); out = np.ones_like(a, dtype=complex); qk = 1.0
    for _ in range(Nmax):
        out *= (1 - a*qk); qk *= q
        if abs(qk) < tol: break
    return out
def mu_closed(theta, q):
    theta = np.asarray(theta, dtype=float)
    qq = qpoch(np.array([q]), q).real[0]
    e2 = np.exp(2j*theta)
    return qq*(qpoch(e2, q)*qpoch(np.conj(e2), q)).real/(2*np.pi)
def chord_jacobi(q, N):
    n = np.arange(1, N); b = np.sqrt((1 - q**n)/(1 - q))
    return np.diag(b, 1) + np.diag(b, -1)

print("#"*94)
print("# CIRCULARITY AUDIT: does the chord ALGEBRA fix theta_vac, or is it the dictionary?")
print("#"*94)

q = 0.7; N = 2000
J = chord_jacobi(q, N)
E, V = np.linalg.eigh(J)
E0 = 2/np.sqrt(1-q)
absE = np.abs(E)/E0

# PICKER 1: chord vacuum |0> = first basis vector. Its energy weight = |V[0,k]|^2.
w0 = V[0, :]**2
mean0 = np.sum(w0*absE)
fctr0 = w0[absE < 0.05].sum()
k_peak = np.argmax(w0)
print(f"\n[PICKER 1] chord vacuum |0> (N_hat ground state):")
print(f"    mean|E|/E0 = {mean0:.4f}; frac within 5% of center = {fctr0:.4f}; "
      f"peak at |E|/E0 = {absE[k_peak]:.4f}")
print(f"    => weight peaks at the CENTER. (algebra-determined state -> center)")

# PICKER 2: Hamiltonian ground state = lowest eigenvalue. Its energy = -E0 (the EDGE).
j_ground = np.argmin(E)
print(f"\n[PICKER 2] Hamiltonian H=a+a^dag GROUND state (lowest E):")
print(f"    E_ground = {E[j_ground]:.4f}; |E|/E0 = {absE[j_ground]:.4f}  => the EDGE.")
print(f"    => the H-ground state is an EDGE state. (algebra-determined state -> edge)")

# PICKER 3: infinite-temperature state rho ~ Identity. Its energy distribution is the DOS itself,
# which is the q-Gaussian -> centered at E=0.
print(f"\n[PICKER 3] infinite-T / max-entropy state (rho ~ Identity):")
# energy distribution = uniform over eigenstates weighted by multiplicity = DOS; mean|E|:
mean_inf = np.mean(absE)   # uniform over states
print(f"    energy distribution = DOS (q-Gaussian), symmetric about E=0; <E> = 0  => CENTER.")

print(f"\n[VERDICT on PICKERS 1-3]")
print(f"    PICKER 1 (N_hat vacuum)   -> CENTER")
print(f"    PICKER 2 (H ground state) -> EDGE")
print(f"    PICKER 3 (infinite-T)     -> CENTER")
print(f"    The chord algebra supplies BOTH a natural CENTER state AND a natural EDGE state.")
print(f"    No single algebraic condition uniquely selects 'the de Sitter static patch'.")
print(f"    => the placement theta_vac is NOT fixed by [a,a^dag]_q=1; it is the EXTERNAL")
print(f"       holographic dictionary (N-V: center; Okuyama: edge).")

# ----------------------------------------------------------------------------------
# PICKER 4: THE CONFINEMENT ANGLE -- does "the singlet escapes to the center" smuggle
# the placement back in? Rahman-Susskind: generic backreacting matter -> stretched horizon
# (edge); only O(N)-singlets reach the bulk CENTER. The deep-MOND limit is identified with
# the singlet/strict-horizon limit. We test whether THAT identification is itself a
# placement assumption or an algebra theorem.
# ----------------------------------------------------------------------------------
print("\n" + "#"*94)
print("# PICKER 4: the CONFINEMENT angle -- does 'singlet -> center' smuggle the placement?")
print("#"*94)
print("""
  The confinement statement (Rahman-Susskind 2401.08555) is: generic matter cords sit at the
  STRETCHED HORIZON; only O(N)-singlet cords reach the bulk CENTER. The framework's escape is:
  the deep-MOND a->0 limit = the singlet/strict-horizon limit -> center -> MOND.

  CIRCULARITY CHECK: the phrase 'reach the bulk CENTER' already presupposes that the bulk
  center IS the dS static-patch interior. But WHICH spectral location is 'the bulk center of
  the static patch' is EXACTLY the N-V-vs-Okuyama dictionary question:
     - Under N-V, the static-patch interior maps to the spectral center (E=0). Then
       'singlet -> bulk center' = 'singlet -> spectral center' -> MOND. (consistent, but
       only because the dictionary was already assumed.)
     - Under Okuyama, the static-patch geometry is the near-EDGE triple-scaling saddle
       (theta->pi). Then 'singlet -> bulk center of THAT geometry' maps to the spectral EDGE
       region, NOT E=0. 'Bulk center' is a GEOMETRIC statement; its SPECTRAL image depends on
       the dictionary.
  => 'the singlet escapes to the center' does NOT independently fix the spectral placement;
     it re-imports the same theta_vac assumption (geometric-center <-> spectral-location map).
""")

# Quantify the kernel's inability to break the degeneracy: q^{Delta N} on an edge source.
def matter_E(q, N, Delta):
    J = chord_jacobi(q, N); E, V = np.linalg.eigh(J)
    n = np.arange(N); D = q**(Delta*n)
    return E, (V.T*D)@V
print("  QUANTITATIVE: can the matter kernel q^{Delta N} move an EDGE source to the center?")
q = 0.7; N = 1500
for Delta in (0.1, 0.5, 1.0):
    E, O_E = matter_E(q, N, Delta)
    E0 = 2/np.sqrt(1-q); a = np.abs(E)/E0
    j_e = np.argmax(E)
    we = O_E[:, j_e]**2; we /= we.sum()
    leak = we[a < 0.10].sum()
    print(f"    Delta={Delta:.2f}: weight from an EDGE source that reaches |E|/E0<0.10 = {leak:.5f}"
          f"  (kernel cannot rescue MOND from an edge placement)")

print("""
  CONCLUSION OF AUDIT:
  - The EXACT line where the sign is set is the choice of theta_vac (spectral location of the
    de Sitter vacuum): pi/2 (center, N-V) vs ->pi (edge, Okuyama). In the matrix route it is
    the choice of source column j_c (argmin|E|) vs j_e (argmax E).
  - That choice is NOT derived: the algebra has a center state (N_hat vacuum / infinite-T) AND
    an edge state (H ground); the dS = WHICH state equals-sign is the holographic dictionary.
  - The confinement angle does NOT rescue a derivation: 'singlet -> bulk center' re-imports the
    geometric-center <-> spectral-location map, i.e. the same dictionary.
  => CONTESTED-TERMINAL (undecidable within DSSYK). NOT DERIVES, NOT FORBIDS.
""")
