#!/usr/bin/env python3
"""
SKEPTIC/VERIFIER re-run of door S_seraille_coefficient -- INDEPENDENT check.

Re-derive C_S from the two Seraille relations (verified by WebFetch of
arXiv:2502.14686v2 this session):
   Eq.(13):  Lambda ~ 1/alpha^2     ('~' proportionality, NO prefactor, NO 8piG)
   Eq.(61):  a0 ~= c^2/alpha        (simplest normalization; Eq.60 O(1) 'we do not
                                      control these numerical factors')
Generalize the two undetermined O(1)'s (K_S in Lambda, b_S in a0), eliminate alpha,
cast into the framework form a0 = c^2 sqrt(Lambda/C_S), read off C_S, and test
whether C_S is a DEFINITE number or a ratio of free O(1)'s.  Both ways.
"""
import sympy as sp
import numpy as np

print("="*78)
print("INDEPENDENT VERIFY: Seraille coefficient C_S vs framework 32pi")
print("="*78)

c, Lambda, alpha, a0 = sp.symbols('c Lambda alpha a0', positive=True)
K_S, b_S, C_S = sp.symbols('K_S b_S C_S', positive=True)

# Seraille (generalized): a0 = b_S c^2/alpha  ;  Lambda = K_S/alpha^2
alpha_sol = sp.solve(sp.Eq(a0, b_S*c**2/alpha), alpha)[0]
Lam_of_a0 = (K_S/alpha**2).subs(alpha, alpha_sol)
a0_of_Lam = sp.solve(sp.Eq(Lambda, Lam_of_a0), a0)
a0_of_Lam = [s for s in a0_of_Lam if s.is_positive][0]
a0_of_Lam = sp.simplify(a0_of_Lam)
print("\n  alpha(a0)      =", alpha_sol)
print("  a0(Lambda)     =", a0_of_Lam)

# match to a0 = c^2 sqrt(Lambda/C_S)
CS = sp.solve(sp.Eq(a0_of_Lam, c**2*sp.sqrt(Lambda/C_S)), C_S)[0]
CS = sp.simplify(CS)
print("\n  C_S (sympy)    =", CS, "   <-- expect K_S/b_S^2")
assert sp.simplify(CS - K_S/b_S**2) == 0, "C_S != K_S/b_S^2"
print("  CHECK C_S = K_S/b_S^2 ............ PASS (sympy-exact)")

# FORM check: a0/(c^2 sqrt(Lambda)) free of Lambda,c  => form reproduced
form = sp.simplify(a0_of_Lam/(c**2*sp.sqrt(Lambda)))
print("\n  a0/(c^2 sqrt(Lambda)) =", form,
      " -> free of {Lambda,c}:", form.free_symbols.isdisjoint({Lambda, c}))

# numeric: framework vs most-natural Seraille (K_S=b_S=1)
c_val = 2.99792458e8
val32 = float(32*sp.pi)
print("\n  32pi =", round(val32,4), "  sqrt(32pi) =", round(np.sqrt(val32),4))
for Lam in [1.090e-52, 1.1056e-52]:
    a0_fw  = c_val**2*np.sqrt(Lam/val32)            # framework
    a0_ser = c_val**2*np.sqrt(Lam/1.0)              # Seraille K_S=b_S=1
    print(f"  Lambda={Lam:.4e}:  a0_fw={a0_fw:.4e}  a0_ser(1,1)={a0_ser:.4e}"
          f"  ratio={a0_ser/a0_fw:.4f}")

# what K_S forces C_S=32pi at b_S=1 ?
print("\n  To force C_S=32pi with b_S=1 (Eq.61):  K_S = 32pi =", round(val32,2))
print("  natural O(1) band ~[0.1,10];  32pi ~", round(val32/10,1),
      "x above band top -> tuned landing, NOT natural.")

# BOTH-WAYS escape test: could b_S carry the 32pi naturally so K_S=1?
#   C_S=32pi with K_S=1 => b_S = 1/sqrt(32pi) = 0.0997  (b_S~0.1, edge of band)
b_for = 1/np.sqrt(val32)
print(f"\n  ALT escape: with K_S=1, forcing C_S=32pi needs b_S=1/sqrt(32pi)={b_for:.4f}")
print("  (b_S~0.1 is at the LOW edge of O(1); but Eq.61 sets b_S~=1, and Eq.60 O(1)")
print("   is IC-dependent/uncontrolled -> b_S NOT pinned to 0.1 either => still free.)")

print("\n" + "="*78)
print("RESULT: C_S = K_S/b_S^2, a RATIO of two UNDETERMINED O(1)'s (Eq.13 '~' no")
print("prefactor; Eq.60 O(1) 'we do not control these numerical factors').")
print("FORM a0~c^2 sqrt(Lambda) reproduced; COEFFICIENT 32pi NOT transmitted.")
print("Verdict = DISAGREE (coefficient mechanism-dependent/undetermined). CONFIRMED.")
print("="*78)
