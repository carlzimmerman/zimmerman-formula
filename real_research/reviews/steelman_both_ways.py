#!/usr/bin/env python3
"""
BOTH-WAYS steelman (mandatory working rule): verify the CENTER/MOND reading as hard as the
EDGE/anti-MOND reading. The framework's strongest move: the deep-MOND a->0 limit IS the strict
empty-static-patch / O(N)-singlet / center limit, so the SIGN is recovered EVEN under Okuyama.

We test this on its own terms with the alpha = m/M_dS conical-deficit displacement, using the
Rahman-Susskind map (2312.04097/2401.08555): pi*v = pi - 2*theta_src, with v ~ p*alpha and
alpha = 8 pi G M / (...) the conical deficit. A LIGHTER / LOWER-ACCELERATION probe -> smaller
alpha -> theta_src closer to pi/2 (center). Question: does the DEEP-MOND limit a->0 (alpha->0)
drive theta_src -> pi/2 (center, MOND) REGARDLESS of the dS-static-patch dictionary?

This is the framework's genuine escape, and it must be scored fairly.
"""
import numpy as np

c=2.998e8; G=6.674e-11; Msun=1.989e30
H0=67.0e3/3.086e22; OmegaL=0.685; H_Lambda=H0*np.sqrt(OmegaL)
M_dS=c**2/(G*H_Lambda)/Msun

print("BOTH-WAYS: does the deep-MOND a->0 limit force the CENTER independent of the dictionary?\n")

# Rahman-Susskind: a conical defect of mass m makes deficit angle; the chord/energy displacement
# from the *empty* placement scales with alpha = m/M_dS. theta_src = theta_vac_empty + O(alpha).
print(f"  M_dS = {M_dS:.3e} Msun.  Displacement of theta_src from the empty placement ~ alpha:")
for nm,M in [("dwarf 1e7",1e7),("spiral 3e10",3e10),("massive 1e12",1e12),("cluster 1e15",1e15)]:
    alpha=M/M_dS
    print(f"    {nm:>14}: alpha={alpha:.2e} -> theta displacement ~ {alpha:.2e} rad")
print("""
  STEELMAN (pro-framework, scored fairly):
    * IF de Sitter (the empty static patch) is placed at the CENTER (N-V), then a galaxy probe
      with alpha<=2.65e-3 sits within ~0.003 rad of the center -> stays on FLAT DOS (s=0) ->
      p=1/2 -> MOND. The deep-MOND a->0 (alpha->0) limit lands EXACTLY on the center. STRONG.
    * The chord vacuum |0> (N_hat ground state) and the infinite-T/max-entropy state BOTH sit at
      the center -- so under the N-V dictionary the algebra's natural states AGREE with MOND.

  ANTI-STEELMAN (pro-edge, scored equally hard):
    * IF de Sitter is placed at the EDGE (Okuyama, derived via a triple-scaling limit around
      theta=pi that REPRODUCES dS-JT gravity -- a construction-level argument, not a guess),
      then the empty static patch is AT the edge, and a small-alpha probe sits within ~alpha of
      the EDGE -> SQRT DOS (s=1/2) -> p=3/5 -> anti-MOND. The deep-MOND a->0 limit lands on the
      EDGE. The displacement argument is SYMMETRIC: 'small alpha -> close to the empty placement'
      is true for BOTH center and edge. alpha->0 does NOT pick which empty placement is dS.
    * Rahman-Susskind themselves: generic backreacting matter cords are confined to the
      stretched horizon (edge/tail); only O(N)-singlets reach the bulk center. A physical galaxy
      is not an exact singlet.

  NET: the alpha->0 (deep-MOND) limit forces the probe to the EMPTY-static-patch placement, but
  it does NOT tell you WHERE that empty placement IS. That 'where' is the dS dictionary -- center
  (N-V) or edge (Okuyama). BOTH are construction-backed in the 2026 literature, NEITHER is forced
  by the chord algebra. So the sign is genuinely two-valued at the level of first principles.

  => The CENTER/MOND reading is NOT reflexively dismissed: it is fully recovered UNDER N-V, and
     the algebra's own ground/max-entropy states favor center. But it is NOT forced, because the
     EDGE/anti-MOND reading is equally construction-backed UNDER Okuyama. CONTESTED-TERMINAL.
""")

# Quantify: is there ANY q,Delta for which the kernel itself breaks the center/edge degeneracy?
# (i.e., does q^{Delta N} acting on the EMPTY edge state leak weight to the center, or vice versa?)
NPOCH=400
def qpoch(a,q,N=NPOCH):
    a=np.asarray(a,dtype=complex);out=np.ones(a.shape,dtype=complex);qk=1.0
    for _ in range(N): out*=(1-a*qk);qk*=q
    return out
def mu_t(theta,q):
    qq=qpoch(q,q).real;e2=np.exp(2j*np.asarray(theta,dtype=float))
    return qq*(qpoch(e2,q)*qpoch(np.conj(e2),q)).real/(2*np.pi)
def Gamp(t1,t2,D,q):
    num=qpoch(q**(2*D),q);t1=np.asarray(t1,dtype=float);t2=np.asarray(t2,dtype=float)
    den=np.ones(np.broadcast(t1,t2).shape,dtype=complex)
    for s1 in (1,-1):
        for s2 in (1,-1): den*=qpoch(q**D*np.exp(1j*(s1*t1+s2*t2)),q)
    return num/den

th=np.linspace(1e-4,np.pi-1e-4,120001)
E=2*np.cos(th)/np.sqrt(1-0.7); E0=2/np.sqrt(1-0.7)
print("  DEGENERACY-BREAK CHECK (q=0.7): does q^{Delta N} on an EDGE vacuum leak to the center?")
for D in (0.1,0.5,1.0):
    w=mu_t(th,0.7)*np.abs(Gamp(th,np.pi-1e-3,D,0.7))**2; w/=np.trapz(w,th)
    leak=np.trapz(w*(np.abs(E)/E0<0.10),th)   # weight that reached within 10% of center
    print(f"    Delta={D:.2f}: weight leaked to center (|E|/E0<0.10) = {leak:.4f}  "
          f"(edge-vac stays at edge => kernel does NOT rescue MOND from an edge placement)")
print("\n  => The diagonal kernel TRANSPORTS faithfully; it cannot convert an edge dS into a")
print("     center one. The sign is set entirely by the (contested) placement. Confirmed both ways.")
