"""
TASK B — Q1: Does the dS-Unruh bath equilibrate CONSERVED CHARGES / CASIMIRS
(per-irrep) rather than ENERGY (per-state)?

The claim that would FORCE per-irrep: if the equilibrium measure of the dS bath
were the MICROCANONICAL/CANONICAL measure of a CONSERVED CHARGE (a Casimir of S3,
constant on each irrep) instead of the energy (which counts states), then equal
weighting would be per-irrep -> r=sqrt2.

Both-ways test: a thermal bath equilibrates whatever is CONSERVED and ADDITIVE
(extensive). We check (i) whether energy is per-state (it is, by construction:
Z = sum_states exp(-beta E)), and (ii) whether a CASIMIR can play the role of
energy in a Gibbs measure, and what measure that actually induces.
"""
import sympy as sp, mpmath as mp
mp.mp.dps = 40

print("="*78)
print("Q1: does the bath weight by a CASIMIR (per-irrep) instead of ENERGY (per-state)?")
print("="*78)

# --- The canonical partition function is INTRINSICALLY per-state ---
# Z = Tr exp(-beta H) = sum over a BASIS of the Hilbert space = sum over STATES.
# For a rep V = V_singlet (+) V_doublet of S3, Tr_V(1) = dim V = 1 + 2 = 3 (per-STATE).
# A class function / per-irrep sum would be Tr restricted to ONE copy per irrep = sum over
# IRREPS = 2 (singlet + doublet counted once each), NOT 3.
print("\n[1] The trace is per-STATE by definition:")
print("    Z = Tr exp(-beta H) = sum_{basis states}.  dim(V) = 1 + 2 = 3 states.")
print("    Equal Boltzmann weight (high-T) -> each of 3 STATES weight 1 -> doublet:singlet = 2:1")
print("    -> per-STATE equipartition -> r=2 -> Q=1 (OVERSHOOT). This is the DEFAULT and it is forced")
print("    by the trace being a sum over a basis (states), not over irreps.")

# --- Can a CASIMIR be the 'energy' in a Gibbs measure? ---
# S3 has irreps: trivial(1), sign(1), standard(2). The 'Casimir' (sum of squared
# generators of the regular rep / the class-sum operator) is CONSTANT on each irrep.
# A Gibbs measure exp(-beta * Casimir) would weight by IRREP LABEL. Test what it gives.
print("\n[2] Gibbs measure with a CASIMIR as 'energy':  p(irrep) ~ d_irrep * exp(-beta*C_irrep)")
print("    Even here the STATE COUNT d_irrep reappears as the multiplicity in the trace:")
# For ANY operator that is a class function (constant c_R on irrep R), the trace is
#   Tr exp(-beta C) = sum_R d_R * exp(-beta c_R)   <-- d_R (per-STATE multiplicity) is STILL there.
dS, dD = 1, 2  # dims of singlet, doublet
C_S, C_D = sp.symbols('C_S C_D', real=True)  # Casimir eigenvalues
beta = sp.symbols('beta', positive=True)
Z_cas = dS*sp.exp(-beta*C_S) + dD*sp.exp(-beta*C_D)
print("    Z = 1*exp(-beta C_S) + 2*exp(-beta C_D).  The '2' (doublet dim) is UNAVOIDABLE in the trace.")
print("    The probability the system is in the DOUBLET = 2 exp(-beta C_D)/Z.")
print("    For this to give EQUAL per-irrep weight (P_singlet = P_doublet) we need")
print("    1*exp(-beta C_S) = 2*exp(-beta C_D), i.e. exp(-beta(C_S - C_D)) = 2  -> a TUNED beta.")
beta_eq = sp.solve(sp.Eq(sp.exp(-beta*(C_S-C_D)), 2), beta)
print("    Required beta =", beta_eq, "  (TUNED to log2/(C_D - C_S); NOT high-T, NOT forced).")

print("\n[3] THE SMUGGLE CHECK: to get per-irrep you must CANCEL the d_R multiplicity.")
print("    'Equilibrate the Casimir' does NOT do this — the trace STILL carries d_R=dim.")
print("    The ONLY measure that is genuinely per-irrep is the PLANCHEREL-DUAL / character")
print("    measure that weights each irrep by 1 (or by d_R^0), which is NOT any Gibbs/thermal")
print("    measure of a Hamiltonian. A conserved charge that is a class function still enters")
print("    a TRACE (sum over states) -> the dim multiplicity survives -> per-STATE.")

# --- Is there a CONSERVED additive charge whose equipartition is per-irrep? ---
# Equipartition theorem: <x dH/dx> = kT per QUADRATIC dof -> per-STATE (per mode). A conserved
# charge Q_cons that is ADDITIVE over states also distributes per-state in equilibrium
# (grand-canonical: <n_state> set per state via mu). No additive conserved charge is per-irrep:
# 'being in irrep R' is NOT additive (you cannot have 1.5 doublets); irrep label is a
# SUPERSELECTION/topological datum, not an extensive charge.
print("\n[4] Equipartition / grand-canonical: additive conserved charges distribute PER-STATE")
print("    (per mode / per dof). The irrep LABEL is not additive/extensive -> it is NOT the")
print("    kind of charge a bath equilibrates. 'How many doublets' is superselection, not a")
print("    thermodynamic occupation. => no additive conserved charge yields per-irrep weighting.")

print("\n" + "="*78)
print("Q1 VERDICT: NO FORCING. A bath weights by a TRACE (sum over states); even a Casimir/")
print("class-function 'energy' keeps the dim multiplicity d_R inside the trace -> per-STATE.")
print("Per-irrep requires CANCELLING d_R (a Plancherel-dual/character measure), which is NOT")
print("a Gibbs measure of any Hamiltonian. Getting P_singlet=P_doublet needs a TUNED beta=log2/dC,")
print("not high-T and not forced. => per-irrep is a re-skin; default stays per-STATE (overshoot).")
