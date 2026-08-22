#!/usr/bin/env python3
r"""The INDIRECT k^4 channel: the precise quantity that decides Gen-2.

Carl: 'The important test is whether the reduction produces any residual k^4 gamma^2 term.'
Here is the mechanism by which it CAN, and the exact threshold it must clear.

THE CHANNEL.  Setting delta N = 0 by hand (what the earlier run did) hides this:
  X = (c^4/a0^2) h^ij a_i a_j  with a_i = d_i ln N a COVECTOR (gamma-independent at fixed N).
  So at linear order in a TT mode, at FIXED N,
        delta X = (c^4/a0^2) delta h^ij a^(0)_i a^(0)_j = -X0 (gamma^ij ahat_i ahat_j)
  -- a LINEAR TT SOURCE in the lapse constraint, with NO derivatives, nonzero whenever the
  wave has polarisation content along a^(0).  Hence delta N is sourced at O(gamma).
  But Y_a contains D_<i D_j> ln N, so its quadratic part contains (d_i d_j delta N)^2.
  With delta N = kappa gamma this is kappa^2 k^4 gamma^2 -- the Gen-1 killer, RESURRECTED
  through the constraint rather than through the operator.
"""
import numpy as np, sympy as sp
def head(t): print("\n"+"="*96+f"\n{t}\n"+"="*96)
c=2.99792458e8; a0=9.3619e-11; L=c**2/a0
head("A -- the linear TT source in the lapse constraint (symbolic)")
g11,g12,ax,az,X0=sp.symbols('gamma_11 gamma_12 a_x a_z X_0',real=True)
print("  delta X = -X0 gamma^ij ahat_i ahat_j .  For a wave along z with a^(0) along z:")
print("     ahat = (0,0,1), gamma_zz = 0 for TT with k||z  =>  delta X = 0.")
print("  For a^(0) along x (wave still along z):  ahat = (1,0,0), gamma_xx = h_+ =/= 0")
print("     =>  delta X = -X0 h_+   -- NONZERO, no derivatives, O(gamma).")
print("  So the source vanishes only in the aligned configuration; generically it is O(X0 gamma).")
head("B -- the threshold kappa = delta N/gamma must clear")
print("  Indirect contribution to the tensor action:")
print("     -(2 a0^2/c^4) eps A (c^8/a0^4) (d_i d_j delta N)^2  =  -2 eps A (c^4/a0^2) k^4 kappa^2 gamma^2")
print("  against the GR gradient term (1/4) k^2 gamma^2, giving a fractional dispersion")
print("     dv/v  ~  4 eps A kappa^2 (k c^2/a0)^2 .")
eps=1.1e-24; A=0.03; f=100.0
k=2*np.pi*f/c; enh=(k*L)**2
bound=1e-15
kap2=bound/(4*eps*A*enh); kap=np.sqrt(kap2)
print(f"\n  at f = {f:.0f} Hz:  (k c^2/a0)^2 = {enh:.3e}")
print(f"  eps = {eps:.1e}, A = {A}:   need kappa^2 < {kap2:.3e}")
print(f"  ==> |delta N / gamma|  <  {kap:.3e}   at LIGO wavelengths")
head("C -- what that means")
print(f"  c^2/a0 = {L:.3e} m.  The suppression the constraint must supply is 1/(k L) ~ {1/(k*L):.2e}")
print(f"  per power, so kappa < {kap:.1e} means the lapse response must be suppressed by")
print(f"  roughly {kap*enh**0.5:.1e} x (1/(kL)) -- i.e. delta N must inherit AT LEAST two")
print( "  powers of (a0/(k c^2)) from the constraint solve, not merely be 'small'.")
print("\n  THREE POSSIBLE OUTCOMES, and the running calculation must pick one:")
print("   (i)  the lapse equation is ELLIPTIC (~ nabla^2 delta N = source): then")
print("        kappa ~ X0 (a0/c^2)^2/k^2 x O(1) -- carries TWO powers of 1/(kL)^2, i.e.")
print("        parametrically FAR below the threshold.  Gen-2 survives.")
print("   (ii) the lapse equation is ALGEBRAIC in delta N at this order: kappa ~ O(X0),")
print("        no k-suppression at all -> dv/v ~ 4 eps A X0^2 (kL)^2 ~ 1e17.  Gen-2 DIES")
print("        exactly as Gen-1 did, and the repair is illusory.")
print("   (iii) the source cancels identically by a symmetry of the TT sector: Gen-2 survives")
print("        cleanly and the earlier delta N = 0 shortcut was accidentally right.")
head("D -- honest status")
for s in ["This is NOT a result. It is the identification of the single quantity that decides",
          "Gen-2, and its numerical threshold. I do not know which of (i)-(iii) holds; the",
          "answer requires the lapse constraint actually solved, which is what the running",
          "program is computing.",
          "It does show that the earlier 'Gen-2 passes by 4.4e9' figure is INCOMPLETE: it was",
          "computed with delta N = 0 imposed, and the indirect channel can exceed it by ~1e32",
          "if the lapse response is unsuppressed. Carl was right to refuse the shortcut.",
          "Note the aligned case (a^(0) parallel to k) has delta X = 0 identically, so any",
          "surviving effect is anisotropic in the wave direction -- a potential observable,",
          "and also a useful cross-check on whichever answer comes back."]:
    print("  [S]",s)
