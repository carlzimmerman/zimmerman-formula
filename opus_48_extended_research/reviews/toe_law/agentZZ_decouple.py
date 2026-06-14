import sympy as sp
# ============================================================
# ZZ2c - THE HOSTILE ESCAPE: can the kernel DECOUPLE slip from pollution?
# The only way the spatial class escapes the lock is if the slip carries a DIFFERENT kernel power
# than the geometric pollution core.  Enumerate the placements of K_L and test each against the
# wall-4 lens-only identity (r^0-class = alpha^6 slip/Phi', i.e. geometric eqN core IS the slip).
# ============================================================
k, L, Phi, Psi = sp.symbols('k L Phi Psi', positive=True)
KL = 1/(1+L**2*k**2)
B = sp.Function('B'); Bp = sp.Function('Bp')

# General operator: key smoothed with power p, slip-generator (geometric, Laplacian k^2) smoothed
# with power q, the explicit slip difference (Psi-Phi) smoothed with power s.
# L_term = B(key)*(D-generator)*(slip-diff),  key ~ k^2 KL^(2p) Phi^2, gen ~ k^2 KL^q,
#          slip-diff ~ (KL^s Psi - Phi) [if Psi smoothed but not Phi -> asymmetric]
p, q, s = sp.symbols('p q s', integer=True, nonnegative=True)
def run(pv, qv, sv, name):
    key = k**2 * KL**(2*pv) * Phi**2
    gen = k**2 * KL**qv
    # slip difference: smoothing Psi differently from Phi is the asymmetry attempt
    slipdiff = (KL**sv * Psi - Phi)
    Lt = B(key)*gen*slipdiff
    eqL = sp.diff(Lt, Psi)     # slip channel
    eqN = sp.diff(Lt, Phi)     # matter channel
    # geometric keying-pollution piece of eqN = the term with B'(key)*dkey/dPhi:
    poll = sp.diff(B(key),Phi)*gen*slipdiff
    # isolate kernel powers by ratio at fixed fields (strip B,B' by structure):
    # slip kernel: coeff of Psi in eqL:
    slip_k = sp.simplify(sp.diff(eqL, Psi))   # remove Psi -> the kernel * B
    print(f"\n[{name}] p={pv} q={qv} s={sv}")
    # The lens-only test: does poll/slip have nontrivial KL (escape) or KL^0 (locked)?
    # Compare the KL-power of the geometric pollution core vs the slip generator.
    poll_kpow = sp.simplify( (poll.subs(Psi,0)) )   # geometric core, Psi=0
    slipgen_kpow = sp.simplify( (eqL) )             # slip generator (dL/dPsi)
    ratio = sp.simplify(poll_kpow / slipgen_kpow)
    # extract pure KL-power dependence (set B=Bp=1 formally via series in KL):
    ratio = ratio.rewrite(sp.Pow)
    print("   poll/slip (kernel structure):", ratio)
    return ratio

# Symmetric (KK pattern): key & gen & slip-diff all smoothed equally
run(1,2,0,"symmetric acceleration-keyed (the observable-correct one)")
# Asymmetric attempt 1: smooth ONLY the key, leave geometric generator un-smoothed
run(1,0,0,"smooth key only, bare geometric generator")
# Asymmetric attempt 2: smooth the slip difference (Psi) but not the key
run(0,0,1,"smooth slip-difference only")
# Asymmetric attempt 3: heavy key smoothing, bare generator
run(2,0,0,"heavy key smoothing, bare generator")

print("\n--- Why the asymmetric placements FAIL the observable or the wall ---")
print("The geometric pollution core comes from delta(operator)/delta(Phi).  The operator's only")
print("Phi-dependence that produces nu(g_bar/a0) is THROUGH THE KEY (the acceleration magnitude).")
print("So the keying pollution ALWAYS carries the key's kernel power (2p).  The SLIP is generated")
print("by the SAME operator coefficient B(key) -> also carries the key's response.  Decoupling the")
print("geometric *generator* kernel (q,s) does NOT decouple the KEYING pollution from the slip,")
print("because BOTH ride the B(key) response.  An un-smoothed (bare) geometric generator just")
print("RE-IMPORTS the FULL un-suppressed (a0 r/c^2)^-1 pollution (q=0 -> KL^0 in the core).")
