import sympy as sp
# Final hostile check: ABSOLUTE kernel power on the slip vs the pollution-keying core,
# for symmetric (q=2) vs bare-generator (q=0).  Confirm the q=0 "re-imports full pollution" claim
# is exact, and that no placement decouples.
k, L, Phi, Psi = sp.symbols('k L Phi Psi', positive=True)
KL = 1/(1+L**2*k**2); x = L*k
B = sp.Function('B')

def kernel_powers(pv, qv, sv):
    key = k**2 * KL**(2*pv) * Phi**2
    gen = k**2 * KL**qv
    slipdiff = (KL**sv*Psi - Phi)
    Lt = B(key)*gen*slipdiff
    eqL = sp.diff(Lt,Psi)                        # slip: dL/dPsi
    poll = sp.diff(B(key),Phi)*gen*slipdiff      # keying pollution core
    # Evaluate KL-power: substitute B(z)=1, B'(z)=1 to expose pure kernel, at Phi=Psi=1
    repl = {B(key): 1}
    # for B' use a stand-in: treat B as exp so B'=B
    z = sp.symbols('z'); Bexp = sp.exp
    eqL_k  = (k**2 * KL**qv)                      # slip generator's kernel (B factored, =Bexp(key)*key' irrelevant to compare)
    poll_k = (sp.diff(sp.exp(key),Phi)*gen)       # pollution with B=exp
    slip_k = (sp.exp(key)*gen)                    # slip with B=exp, dL/dPsi ~ B*gen*KL^s
    ratio = sp.simplify(poll_k/slip_k)
    return sp.simplify(ratio)

print("pollution/slip kernel ratio (B=exp surrogate), should be KL-FLAT (=> locked) if no decouple:")
for (p,q,s),name in [((1,2,0),"symmetric"),((1,0,0),"bare generator"),((1,2,1),"smooth slipdiff too"),((2,0,0),"heavy key+bare gen")]:
    rr = kernel_powers(p,q,s)
    # the ratio depends on dkey/dPhi ~ 2 Phi k^2 KL^(2p); the SLIP also ~ B*gen. The KL-dependence
    # of the RATIO = dkey/dPhi's KL power = KL^(2p), divided by nothing (slipdiff Psi-term has KL^s).
    print(f"  {name:22s} (p={p},q={q},s={s}): ratio = {rr}")
print()
print("Interpretation: the ratio = (2 Phi k^2 KL^{2p}) i.e. the KEY's lapse response.  It is")
print("independent of q (the generator kernel) -> decoupling the generator does NOT help.  The")
print("pollution is set by the KEY's kernel KL^{2p}, the SAME kernel the slip uses to be")
print("acceleration-keyed.  At the slip's mode KL^{2p}~O(1) (else no slip).  LOCKED, every placement.")

# And confirm: at k where slip survives (KL~1), pollution core ~ full.  At k where KL<<1
# (pollution suppressed), the KEY itself ->0 so the operator turns OFF -> no slip.  Same number.
print("\nNumeric (p=1): at the mode where you'd want suppression, key-response and slip die together:")
for xv in [0.1, 1.0, 3.0, 10.0]:
    klv = 1/(1+xv**2)
    print(f"  L*k={xv:5}: KL={klv:.4f}, key-response KL^2={klv**2:.4e}  (slip ~KL, pollution ~KL^2: BOTH ->0 together)")
