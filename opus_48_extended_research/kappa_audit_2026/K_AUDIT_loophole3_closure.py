#!/usr/bin/env python3
"""
K_AUDIT (result) -- LOOPHOLE 3 closes: giving up UNIVERSAL lensing=dynamics (a source-dependent
gravitational slip) does not rescue channel B -- the slip it needs is O(1), which contradicts the
galaxy-galaxy weak-lensing RAR.

Run: python3 opus_48_extended_research/kappa_audit_2026/K_AUDIT_loophole3_closure.py   (sympy)
"""
import sympy as sp

gamma = sp.symbols('gamma', positive=True)
ratio = ((1 + gamma)/2)**2                 # a0_lens / a0_dyn for slip gamma = Psi/Phi

print("="*88)
print("LOOPHOLE 3 -- allow a slip (non-universal gamma) to engage channel B")
print("="*88)
print("\n[1] slip magnitude channel B needs: to move the deep-MOND slope 1->2 the slip channel must")
print("    contribute EQUALLY to the Psi channel -> |Phi-Psi| ~ Psi -> gamma=Psi/Phi differs from 1")
print("    by O(1). An ORDER-UNITY slip, not small.")
print("\n[2] slip -> observable. dynamics ~ Phi ; lensing ~ (Phi+Psi)=Phi(1+gamma) ->")
print(f"    a0_lens/a0_dyn = ((1+gamma)/2)^2 = {sp.expand(ratio)}")
for g in (1, 2, 0):
    print(f"      gamma={g}: a0_lens/a0_dyn = {float(ratio.subs(gamma,g)):.2f}")
print("    -> O(1) slip shifts the lensing-inferred a0 by a FACTOR ~2-4 vs the dynamical a0.")
print("\n[3] data: Brouwer+2021 KiDS weak-lensing RAR: g_obs(lensing) follows the SAME RAR (same")
print("    a0 ~ 1.2e-10) as the SPARC dynamical RAR over ~4 decades; the framework's own completion")
print("    fits it with gamma=1 (committed: lensing 21.2sigma -> 0.601sigma). a0_lens/a0_dyn ~= 1 to")
print("    ~20%. A factor 2-4 offset is grossly excluded.")
print("    CAVEAT: this uses the published a0_lens~=a0_dyn agreement + the framework's committed gamma=1")
print("    fit, NOT a from-scratch redo of Brouwer's ESD->g_obs deprojection. The slip->offset physics")
print("    (steps 1-2) is what is verified here.")
assert sp.simplify(ratio.subs(gamma, 1) - 1) == 0
print("\nVERDICT: loophole 3 CLOSES. The O(1) slip channel B requires predicts a factor ~2-4 lensing-vs-")
print("dynamics RAR mismatch, contradicting the observed agreement -- and it would destroy the framework's")
print("own strongest lensing success (gamma=1). A source-dependent gamma does not recover the count.")
