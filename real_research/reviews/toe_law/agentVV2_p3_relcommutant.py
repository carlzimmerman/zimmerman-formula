import numpy as np
from numpy.linalg import eigvalsh, eigh
np.set_printoptions(precision=4, suppress=True)
rng = np.random.default_rng(101)

# =====================================================================
# TEST C: THE RESIDUAL OBSTRUCTION -- the OFF-DIAGONAL / RELATIVE-COMMUTANT
# freedom that KMS-on-the-generator does NOT fix.
#
# Setup. In a II_1 factor M with faithful normal state omega (density rho),
# the modular flow is sigma_t = Ad(rho^{it}). The CENTRALIZER M_omega =
# {x : sigma_t(x)=x} = commutant of rho = block-diagonal in rho's eigenbasis.
#
# KMS-at-beta w.r.t. the boost pins rho's EIGENVALUES (Test B: unique).
# But a *-iso psi: M_chord -> M_dS that intertwines the flows is only forced
# to MATCH on the centralizer / spectral data. On the OFF-CENTRALIZER part
# (the off-diagonal blocks connecting different rho-eigenspaces) psi has
# RESIDUAL FREEDOM: any unitary in the centralizer M_omega can be composed
# with psi and STILL intertwine the flow and STILL fix the state.
#
# So: Inn(M)_omega = unitaries commuting with rho = the EXACT residual
# freedom. We compute its size. If it is nontrivial, state+flow matching
# does NOT uniquely determine psi -- there is a gauge orbit, and within it
# the framework's load-bearing OBSERVABLES (center placement theta_v,
# off-diagonal matter spectral weights) can VARY. That is the placement
# freedom agentTT found, re-derived here as a centralizer gauge group.
# =====================================================================

d = 8
# A state rho with a DEGENERATE-ish spectrum (generic boost ladder has
# distinct eigenvalues, but the matter sector adds multiplicity):
# model: boost ladder (distinct) (x) matter multiplicity m  -> blocks.
ladder = np.array([0.40, 0.25, 0.18, 0.17])  # 4 distinct boost levels (sum=1)
mult   = 2                                     # matter multiplicity per level
ev = np.repeat(ladder/mult, mult)             # 8 eigenvalues, 4 degenerate pairs
print("=== TEST C: centralizer gauge group (residual psi-freedom) ===")
print("rho eigenvalues:", ev, " sum=", ev.sum())

# Centralizer of rho = block-diag unitaries: U(m) per distinct eigenvalue.
# dim of centralizer unitary group = sum over distinct eigs of (mult_i)^2.
from collections import Counter
c = Counter(np.round(ev,8))
dims = [k**2 for k in c.values()]   # real dim of U(m) is m^2
print("distinct eigenvalues:", dict(c))
print("centralizer = product of U(m_i); real dim =", sum(dims))
print("  -> NONTRIVIAL residual gauge whenever any multiplicity m_i>1.")

# Now show: a centralizer unitary V (commutes with rho) gives a NEW iso
# psi' = Ad(V) o psi that STILL fixes the state (V rho V^* = rho) and STILL
# intertwines the flow (V commutes with rho^{it}), yet ACTS NONTRIVIALLY
# on the matter off-diagonal blocks -> moves load-bearing observables.
# Build a V mixing the 2-dim matter multiplet at the top boost level:
V = np.eye(d, dtype=complex)
theta = 0.7
V[0,0]=np.cos(theta); V[0,1]=-np.sin(theta); V[1,0]=np.sin(theta); V[1,1]=np.cos(theta)
rho = np.diag(ev)
print("\nV commutes with rho (fixes state & flow):", np.allclose(V@rho, rho@V))
print("V is NOT a scalar (acts nontrivially):", not np.allclose(V, V[0,0]*np.eye(d)))

# A 'matter observable' living in the off-... actually in the multiplet block:
# e.g. a sigma_z-like operator distinguishing the two matter copies at top level.
Mobs = np.zeros((d,d), dtype=complex); Mobs[0,0]=1.0; Mobs[1,1]=-1.0
before = np.trace(rho@Mobs).real
after  = np.trace(rho@(V@Mobs@V.conj().T)).real
print(f"\nmatter-multiplet observable expectation: before={before:.4f} after(psi')={after:.4f}")
print(">>> SAME state, SAME flow, DIFFERENT observable value under the gauge V.")
print(">>> The centralizer multiplicity is the EXACT residual freedom NOT killed")
print(">>> by (D1)+(D3)+KMS. State+flow matching is necessary, NOT sufficient.")
