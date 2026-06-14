import numpy as np
from numpy.linalg import eigvalsh, eigh
np.set_printoptions(precision=5, suppress=True)

# =====================================================================
# FINITE-DIM MODEL OF A II_1 FACTOR (matrix algebra M_d with normalized
# trace tau = (1/d) Tr). Faithful normal states <-> density matrices rho
# with tau-expectation: omega_rho(x) = Tr(rho x), rho>0, Tr rho = 1.
# This is the standard finite-dim stand-in: the modular theory of (M, omega_rho)
# is sigma_t(x) = rho^{it} x rho^{-it}, EXACTLY the type-I shadow of the
# II_1 modular flow. We use it to test the *structural* reduction claims.
# =====================================================================

d = 6
rng = np.random.default_rng(20260613)

def rand_state(d, rng):
    A = rng.standard_normal((d,d)) + 1j*rng.standard_normal((d,d))
    H = A@A.conj().T
    rho = H/np.trace(H)
    return rho

# --- CLAIM under test: "two states with the SAME modular SPECTRUM are
#     related by a unitary" (the brief's tentative reduction). ---
# Modular operator Delta_omega in GNS has spectrum {lambda_i/lambda_j}
# (ratios of eigenvalues of rho). "Same modular spectrum" -> same multiset
# of eigenvalue-ratios -> (generically) same eigenvalues of rho.

rho1 = rand_state(d, rng)
ev1 = np.sort(eigvalsh(rho1))[::-1]

# Build rho2 with the SAME eigenvalues (same modular spectrum) but a
# DIFFERENT eigenbasis (a different state, NOT a scalar multiple).
U = np.linalg.qr(rng.standard_normal((d,d))+1j*rng.standard_normal((d,d)))[0]
rho2 = U @ np.diag(ev1) @ U.conj().T
ev2 = np.sort(eigvalsh(rho2))[::-1]

print("=== TEST A: same modular spectrum => unitarily related? ===")
print("eigs(rho1):", ev1)
print("eigs(rho2):", ev2)
print("spectra equal:", np.allclose(ev1, ev2))
# rho2 = U rho1' U^* where rho1' = V diag V^* ... they ARE unitarily conjugate
# as OPERATORS (same spectrum => unitarily equivalent). Confirm the unitary:
ev1b, V1 = eigh(rho1)
ev2b, V2 = eigh(rho2)
# order both ascending (eigh returns ascending)
W = V2 @ V1.conj().T
print("rho2 = W rho1 W^* :", np.allclose(rho2, W@rho1@W.conj().T))
print("W unitary       :", np.allclose(W@W.conj().T, np.eye(d)))
print()
print(">>> So 'same modular spectrum' DOES give a unitary W with W rho1 W^* = rho2.")
print(">>> BUT: is W an INNER automorphism that fixes the FACTOR structure AND")
print(">>>      lands inside the algebra's own unitary group with the RIGHT center/")
print(">>>      relative-commutant placement? That is the residual question. Test B.")
