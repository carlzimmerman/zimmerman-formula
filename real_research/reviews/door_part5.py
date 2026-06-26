import numpy as np
print("="*100)
print("[D] The SHARP question: does X2's 'Im mu_hat < 0 (active)' survive as a real obstruction,")
print("    or is it the LINEAR-RESPONSE SEPARABILITY artifact Milgrom explicitly flags as N/A?")
print("="*100)
print()
print("X2 setup (agentX_sk_kernel.out): linearize mu_fw about a deep-MOND background, treat mu_hat(w)")
print("as a RESPONSE FUNCTION acting on the acceleration perturbation, demand causal (KK) completion,")
print("find Im mu_hat(w) < 0 => negative-residue => 'active'. This is a LINEAR-RESPONSE statement.")
print()
print("Milgrom 2208.07073, page 3 (the causality paragraph, VERBATIM paraphrase):")
print('  "In LINEAR-RESPONSE systems, where the cause (input) can be separated from the effect (output),')
print('   such causality is guaranteed by certain analyticity properties... the analog of I here.')
print('   ... But to avoid complications, I assume we are dealing with a CLOSED system, allowed to')
print('   evolve on its own; so the forces are determined as part of the solution, not dictated at will."')
print()
print("=> Milgrom himself states the linear-response causal-kernel framing (the X2 framing) is the")
print("   framing for an OPEN/driven system (input separable from output). The actual MI is a CLOSED")
print("   system where a(t) and F(t) are solved JOINTLY and are NOT separable. The passivity theorem")
print("   (Im chi >= 0 for passive) is a theorem ABOUT a linear response chi mapping an INDEPENDENT")
print("   input to an output. It does not constrain a closed nonlinear constitutive relation.")
print()

# Make the separability point concrete & quantitative: passivity bounds the linear susceptibility chi
# defined by  output = chi * input  with input EXTERNAL. For the MI, is mu_hat such a chi?
# In X2, the 'input' was taken as the acceleration perturbation and 'output' the force perturbation
# (or vice versa). But on a closed orbit a and F are NOT independent: F=-grad V(x), x=double-integral of a.
# So 'Im(F-vs-a response)<0' does NOT mean energy gain; it means the a<->F relation has a reactive part
# of a given sign -- which for a CONSERVATIVE nonlinear constitutive law is generic.

print("[D1] Concrete demonstration: a PASSIVE conservative NONLINEAR spring has the SAME 'inverted',")
print("     'active-looking' linearized response sign that X2 reads as activity -- yet stores zero net energy.")
print("     Take F(x) = x + b x^3 (b<0 softening) OR a saturable element; linearize about amplitude A:")
print("     d<F>/d<x> (secant stiffness) DECREASES with A -- the 'mu(0)>mu(inf)'-type inversion in stiffness.")
A=np.linspace(0.01,3,15); b=-0.05
# secant 'modulus' of a softening spring over an oscillation of amplitude A (averaged):
# F=x+b x^3 ; effective linear modulus k_eff(A) = <F x>/<x^2> over a cycle x=A cos
keff = 1 + b*0.75*A**2   # <(x+bx^3)x>/<x^2> with x=Acos: =1 + b*(3/4)A^2
print("     softening spring secant modulus k_eff(A):  k_eff(small A)=%.3f  k_eff(large A)=%.3f  (DROPS)"%(keff[0],keff[-1]))
print("     -> a textbook PASSIVE conservative element shows a 'modulus that drops with amplitude'.")
print("     Energy stored over a cycle = oint F dx = 0 EXACTLY (F=-dU/dx, U=x^2/2+b x^4/4). Passive+conservative.")
# verify
x=A[-1]*np.cos(np.linspace(0,2*np.pi,100000)); F=x+b*x**3
W=np.trapz(F,x)  # closed loop integral in x: returns ~0 for single-valued F(x)
print("     oint F dx over a cycle = %.2e (=0 => conservative). The 'inversion' alone is NOT activity."%W)
print()
print("[D2] WHY X2 still read 'active': it imposed a CAUSAL (one-sided, retarded) kernel completion on a")
print("     relation that, on the physical closed orbit, is NOT a causal input->output map. The minimal")
print("     causal completion of a NON-causal symmetric relation injects a spurious Im part whose sign is")
print("     then read as gain. That is a property of the FORCED causal-LTI EMBEDDING, not of the dynamics.")
print("     agentX itself flagged this: '~half acausal', 'fixed causal kernel phenomenologically DEAD,")
print("     only the ADAPTIVE (spectrum-resolving) construction survives' -- i.e. the LTI kernel is the wrong object.")
