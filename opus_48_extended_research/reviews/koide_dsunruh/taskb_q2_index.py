"""
TASK B — Q2: Is there an INDEX / TOPOLOGICAL / CHARACTER-VALUED partition function
(a la equivariant localization) natural to the dS horizon, where the MEASURE itself
IS a class function (per-irrep)?

This is the strongest YES candidate: equivariant index theorems and character-valued
partition functions ARE per-irrep by construction (the answer is a sum over irreps
weighted by characters chi_R, evaluated as class functions). The dS horizon DOES carry
a one-loop "horizon character" (Anninos-Denef-Law-Sun 2020) — a genuine character-valued
object. The question: would THIS make the framework's equilibrium measure per-irrep,
and does it FORCE r=sqrt2, or is it a hopeful re-skin?

Both-ways: a character-valued partition function is real physics. But we must check whether
it is the measure on the FLAVOR/family Hilbert space whose equipartition sets r — or a
character of the SPACETIME isometry (SO(d,1) of dS), unrelated to S3-family.
"""
import sympy as sp, mpmath as mp
mp.mp.dps = 40

print("="*78)
print("Q2: character-valued / equivariant-index partition function -> per-irrep measure?")
print("="*78)

# --- What an equivariant index actually computes ---
# Equivariant localization: Z(g) = Tr_H [ g * exp(-beta H) ] for a SYMMETRY g.
# This is the EQUIVARIANT character. It IS a class function OF g (the group element you insert).
# Decompose H = (+)_R n_R V_R.  Then Z(g) = sum_R n_R chi_R(g) exp(-beta E_R).
print("\n[1] Equivariant partition function: Z(g) = Tr[g exp(-beta H)] = sum_R n_R chi_R(g) e^{-beta E_R}.")
print("    It is a CLASS FUNCTION of the inserted group element g. Per-irrep info lives in chi_R(g).")

# THE CRUCIAL SMUGGLE: a class function of g is NOT a per-irrep MEASURE on physical states.
# To EXTRACT the irrep content you INTEGRATE against characters (Peter-Weyl / Frobenius):
#   n_R = integral_G dg conj(chi_R(g)) Z(g)   <- this RECOVERS multiplicities n_R, still per-STATE
#         because n_R counts STATE copies, and the physical probability is n_R d_R / dim.
# The 'measure' that is per-irrep is the HAAR measure dg on the GROUP, NOT a measure on the
# family Hilbert space. Equilibrium of the bath is still Z = Z(g=identity) = sum_R n_R d_R e^{-bE},
# and chi_R(identity) = d_R -> the dimension multiplicity RE-APPEARS at g=1.
g = sp.symbols('g')
print("\n[2] THE KILLER: at the physical point g = identity (no twist), chi_R(1) = d_R.")
print("    Z(1) = sum_R n_R d_R e^{-beta E_R}  -> the dim multiplicity d_R is BACK -> per-STATE.")
print("    Character-valuedness only survives if you keep a NONTRIVIAL twist g != 1 inserted")
print("    FOREVER. A thermal EQUILIBRIUM (the framework's bath) is the UNTWISTED g=1 trace.")
print("    The probability of being in the doublet = n_D d_D e^{-bE_D}/Z(1); the d_D=2 is present.")

# Verify: chi for S3 standard rep at identity = 2 (=dim), trivial = 1.
# S3 character table (classes: e, (12)[3 elts], (123)[2 elts]):
chars = {'trivial':[1,1,1], 'sign':[1,-1,1], 'standard':[2,0,-1]}
print("\n[3] S3 characters at identity (first column) = dimensions:")
for R,c in chars.items():
    print(f"    chi_{R}(e) = {c[0]}  (= d_R)")
print("    => any UNTWISTED (equilibrium, g=e) character evaluation returns the DIMENSION.")
print("    Per-irrep weighting needs evaluation AWAY from g=e (a permanent flavor twist),")
print("    which is NOT a thermal equilibrium and has no dS-horizon justification on the family index.")

# --- The dS horizon character (Anninos et al) is about SPACETIME isometry, not S3-family ---
print("\n[4] The genuine dS-horizon 'character' (Anninos-Denef-Law-Sun): it is the character of")
print("    the dS_{d+1} ISOMETRY group SO(d+1,1) / the quasinormal-mode spectrum — a property of")
print("    SPACETIME fields (spin, mass, SO(d,1) reps), NOT of an internal S3 FAMILY symmetry.")
print("    To make IT set r you must IDENTIFY the S3 family rep with an SO(d,1) spacetime rep.")
print("    No such identification is forced (family S3 commutes with spacetime by Coleman-Mandula);")
print("    inserting it is exactly the re-labeling. The horizon character does NOT see the 3 families.")

# --- Equivariant LOCALIZATION fixed points: do they weight per-irrep? ---
# Duistermaat-Heckman / Atiyah-Bott localize an integral to FIXED POINTS of g, weighting each
# fixed point by 1/det(1-g) (the equivariant Euler class). The WEIGHTS are 1/(weights of the
# tangent rep) — a per-WEIGHT (=per-STATE in the tangent space) product, NOT a flat per-irrep sum.
print("\n[5] Localization weights = product over TANGENT WEIGHTS 1/(1-g^{w}) (per-WEIGHT = per-state")
print("    in the tangent rep), not a flat per-irrep weight. Even localization is per-state-structured.")

print("\n" + "="*78)
print("Q2 VERDICT: NO FORCING (cleanest re-skin). Character-valued/equivariant partition functions")
print("ARE class functions of an INSERTED twist g, but (a) at the physical equilibrium point g=e the")
print("character returns chi_R(e)=d_R, restoring per-STATE; (b) the only genuine dS-horizon character")
print("is of the SPACETIME isometry SO(d,1), blind to the internal S3 family (Coleman-Mandula); (c)")
print("equivariant localization weights are per-tangent-weight, not flat per-irrep. To get per-irrep")
print("you must keep a permanent family twist g!=e with no dS justification = the re-labeling.")
