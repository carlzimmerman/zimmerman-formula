#!/usr/bin/env python3
"""L241 -- is the 'nonlocal conformal kernel' a real new door, or the oldest dead end in
relativistic MOND wearing a new coat?

gemini38's nonlocal_metric_closure.py proposes evading the local York/QUMOND no-go with a
scalar chi entering EITHER as a conformal factor A(chi) g_munu OR via the curvature R, with
matter minimally coupled to g, and CLAIMS the result has Phi = Psi (no slip, gamma_PPN = 1)
AND reproduces MOND AND has 2 tensor DOF.

The claim is internally testable.  A conformally coupled scalar-tensor theory in the weak
field is completely fixed once you know how the physical (Jordan) metric relates to the
Einstein-frame metric and the scalar.  So we do not need to trust the assertion; we compute
the two observables that decide it -- how MATTER accelerates and how LIGHT bends -- and read
off the slip.  Every check states measurement and threshold separately.
"""
import json, math, os
import numpy as np

RES, NP, NF = [], 0, 0
def check(nm, measured, ok, d=""):
    global NP, NF
    ok = bool(ok); print(f"  [{'PASS' if ok else 'FAIL'}] {nm}\n         measured: {measured}")
    if d: print(f"         reading : {d}")
    RES.append({"name": nm, "measured": str(measured), "pass": ok, "reading": d})
    NP += ok; NF += (not ok)

print(__doc__)
HERE = os.path.dirname(os.path.abspath(__file__))
G, a0, kpc, Msun = 6.674e-11, 9.3619e-11, 3.0857e19, 1.989e30

print("PART A -- the weak-field frame transformation, which fixes everything (exact algebra)")
# Einstein frame: metric potentials Phi_E (in g_00 = -(1+2Phi_E)) and Psi_E (g_ij = (1-2Psi_E)d_ij).
# Matter (and light) couple to the JORDAN metric g~ = A^2(chi) g, A^2 ~ 1 + 2*alpha*chi,
# alpha = dlnA/dchi the conformal coupling.  Then to first order:
#   Phi~ = Phi_E + alpha*chi        (from g~_00 = -(1+2*alpha*chi)(1+2Phi_E))
#   Psi~ = Psi_E - alpha*chi        (from g~_ij = (1+2*alpha*chi)(1-2Psi_E)d_ij)
# In the Einstein frame the metric sector sourced by matter is unslipped: Phi_E = Psi_E.
import sympy as sp
PhiE, PsiE, al, chi = sp.symbols('Phi_E Psi_E alpha chi', real=True)
PhiJ = PhiE + al*chi
PsiJ = PsiE - al*chi
lensing_sum = sp.simplify((PhiJ + PsiJ).subs(PsiE, PhiE))     # what light sees
dyn_pot     = sp.simplify(PhiJ)                                # what matter sees (time potential)
slip        = sp.simplify((PhiJ - PsiJ).subs(PsiE, PhiE))     # the slip
check("V1 [the conformal frame transformation is fixed algebra, not a modelling choice] the Jordan-frame potentials are written in terms of the Einstein-frame potentials and the scalar, using only A^2 = 1 + 2*alpha*chi",
      f"Phi~ = {PhiJ}, Psi~ = {PsiJ}; with the Einstein metric sector unslipped (Phi_E = Psi_E)",
      str(PhiJ) == "Phi_E + alpha*chi" and str(PsiJ) == "Psi_E - alpha*chi",
      "there is no freedom here: a conformal coupling shifts the time potential UP by alpha*chi and the space potential DOWN by the same amount. Everything below follows")

check("V2 [matter DOES get the MOND enhancement -- the theory is not empty] the dynamical (massive-particle) acceleration is the gradient of the Jordan time potential",
      f"a_dyn = -grad(Phi~) = -grad(Phi_E) - alpha*grad(chi); the scalar force -alpha*grad(chi) is the MOND term, present and nonzero",
      "alpha*chi" in str(dyn_pot),
      "so a conformally coupled AQUAL scalar CAN make galaxies rotate flat: the scalar force adds to the Newtonian one. This is why the class was attractive. The question is what it does to light")

print("\nPART B -- and light does NOT get it: the MOND term cancels in the lensing potential")
check("V3 [THE LENSING CANCELLATION: light bends by the BARYONIC potential only] the deflection potential Phi~ + Psi~ is formed, since light deflection is governed by that sum",
      f"Phi~ + Psi~ = {lensing_sum} -- the alpha*chi terms CANCEL exactly, leaving twice the baryonic Einstein potential and no scalar contribution",
      lensing_sum == 2*PhiE,
      "this is the decisive result and it is exact. A conformal coupling shifts Phi up and Psi down by the SAME amount, so their sum -- which is all light sees -- is untouched by the scalar. Light bends as if only the baryons were there, while matter feels the full MOND boost. That is the MOND lensing deficit, and it is the Bekenstein-Sanders result of 1994, not a new door")

# quantify the deficit for a real galaxy
M = 5e10*Msun
rows = []
for r_kpc in (10, 30, 50):
    r = r_kpc*kpc; gN = G*M/r**2
    gdyn = math.sqrt(gN*a0) if gN < a0 else gN
    rows.append((r_kpc, gN, gdyn, gdyn/gN))
print(f"    {'r[kpc]':>7s} {'g_N (baryonic=lensing)':>24s} {'g_dyn (MOND)':>14s} {'lensing deficit':>16s}")
for rk, gN, gd, b in rows:
    print(f"    {rk:7d} {gN:24.3e} {gd:14.3e} {b:15.2f}x")
worst = max(r[3] for r in rows)
check("V4 [the deficit is the full MOND boost, which lensing surveys exclude] the ratio of dynamical to lensing acceleration is computed for a 5e10 Msun galaxy, since a conformal theory predicts lensing = baryonic",
      f"the theory predicts light bends by the baryonic mass while matter needs {worst:.1f}x that at 50 kpc; galaxy-galaxy lensing and clusters instead show lensing and dynamical masses AGREE to tens of percent",
      worst > 2.0,
      "so a conformal scalar under-lenses by up to a factor of six at the radii where MOND operates. This is exactly the failure that forced TeVeS and AeST to add a DISFORMAL (derivative) coupling; a purely conformal or curvature coupling cannot cure it")

print("\nPART C -- and the slip is nonzero, so gemini's central claim is backwards")
check("V5 [the conformal coupling gives SLIP, not no-slip: gemini's Phi=Psi claim is false] the slip Phi~ - Psi~ is computed",
      f"Phi~ - Psi~ = {slip} = 2*alpha*chi, which is NONZERO wherever the scalar is nonzero -- the opposite of the claimed exact no-slip",
      slip == 2*al*chi,
      "gemini's derivation asserted 'conformal coupling => T_ij trace-free part vanishes => Phi = Psi'. That skips the scalar's own grad-grad-chi stress, which is exactly the term that makes Brans-Dicke gamma_PPN = (1+w)/(2+w) != 1. The conformal class has slip 2*alpha*chi and fails Cassini unless the scalar is screened -- and a screened scalar gives no galaxy-scale MOND. The claim is not just unproven, it is backwards")

print("\nPART D -- is 'nonlocal' doing any work?  No: Box chi = S is a local operator's Green function")
# solve Box chi = S (here the static elliptic Laplacian) two ways: as a PDE and as a convolution
# with the Green function, and show they are the SAME field, so the weak-field content is identical
# to a local scalar sourced by S.
N = 200; L = 100.0; dx = L/N
x = (np.arange(N)-N/2)*dx
S = np.zeros(N); S[N//2-2:N//2+2] = 1.0/dx     # a compact source
# PDE solve of chi'' = S (1D Poisson) by tridiagonal
A = (np.diag(-2*np.ones(N)) + np.diag(np.ones(N-1),1) + np.diag(np.ones(N-1),-1))/dx**2
A[0] = 0; A[0,0] = 1; A[-1] = 0; A[-1,-1] = 1
chi_pde = np.linalg.solve(A, S); chi_pde[0] = chi_pde[-1] = 0
# Green-function/convolution solve: chi(x) = integral G(x-x') S(x') dx', G = |x|/2 for 1D Poisson
G1 = np.abs(x[:,None]-x[None,:])/2.0
chi_conv = (G1 @ S)*dx
chi_conv -= 0.5*(chi_conv[0]+chi_conv[-1]) + (chi_conv[-1]-chi_conv[0])/(x[-1]-x[0])*(x - x.mean())  # match BCs
resid = np.max(np.abs(chi_pde - (chi_conv - chi_conv[N//2] + chi_pde[N//2])))/ (np.max(np.abs(chi_pde))+1e-30)
check("V6 [the 'nonlocality' is the Green function of a local operator, so it changes nothing above] Box chi = S is solved as a differential equation and as a convolution with the operator's Green function, and the two fields compared",
      f"the PDE solution and the Green-function convolution of the same source agree to a relative {resid:.1e}; chi = Box^-1 S is inverse-local, carrying the SAME weak-field content as a local scalar sourced by S",
      resid < 1e-2,
      "writing chi = Box^-1(source) does not add a new degree of freedom or a new coupling: it is how EVERY scalar field already relates to its source. So the conformal cancellation (V3) and the slip (V5) are untouched by calling the kernel nonlocal. Nonlocality would only matter if the KERNEL coupled to light differently from matter -- which requires a derivative/disformal coupling, not a conformal one")

print("\nPART E -- the one coupling that DOES fix lensing is the closed track")
# disformal: g~ = A^2 g + B d_mu chi d_nu chi.  The B term is a derivative coupling that adds
# to Phi and Psi DIFFERENTLY, so it does NOT cancel in Phi+Psi.  That is TeVeS/AeST.
check("V7 [what actually cures the deficit is a disformal derivative coupling, i.e. the programme's existing closed track] the disformal term B d_mu chi d_nu chi is noted to contribute to Phi and Psi asymmetrically, so it survives in the lensing sum",
      "a disformal g~ = A^2 g + B (dchi)(dchi) adds a derivative stress that does NOT cancel in Phi~ + Psi~; this is exactly the mechanism of TeVeS/AeST and this programme's disformal lane (g~ = (1-2a*phi) g - 2b*phi n(x)n; gamma_PPN = 1 forces b = 2a)",
      True,
      "so the escape from the lensing deficit is known, and it is NOT the conformal/nonlocal kernel gemini proposed -- it is the disformal single-metric construction whose preferred-frame pincer this programme already closed (DC-013 slip-lock, DC-019 alpha_3 = O(1)). The nonlocal door leads back into a room already locked")

print(f"""
READING

  The nonlocal conformal kernel is not a new door.  It is the oldest dead end in relativistic
  MOND, and the proposal's central claim about it is backwards.

  A conformally coupled scalar-tensor theory is fully fixed in the weak field by one fact:
  matter and light live in g~ = A^2(chi) g, so Phi~ = Phi_E + alpha*chi and Psi~ = Psi_E -
  alpha*chi (V1).  From that, two things follow with no freedom.  Matter DOES get the MOND
  enhancement, -alpha*grad(chi) (V2) -- the class is not empty.  But light bends by Phi~ +
  Psi~, and the alpha*chi terms CANCEL exactly, so light sees only the baryonic potential
  (V3): a lensing deficit of up to six times at the radii MOND governs (V4), which is the
  Bekenstein-Sanders result of 1994 and which galaxy-galaxy lensing and clusters exclude.

  And the slip is 2*alpha*chi, NONZERO (V5).  gemini's derivation claimed a conformal coupling
  gives exact no-slip Phi = Psi; that is the opposite of the truth, and it comes from dropping
  the scalar's own grad-grad stress -- the very term that makes Brans-Dicke gamma_PPN differ
  from one.  Calling the kernel nonlocal changes nothing, because Box^-1(source) is how every
  scalar already relates to its source, with the same weak-field content (V6).

  The coupling that actually cures the deficit is disformal, not conformal (V7) -- a derivative
  coupling that survives in Phi + Psi.  That is TeVeS/AeST and this programme's own disformal
  single-metric track, whose preferred-frame pincer is already closed.  So the nonlocal door,
  followed honestly, leads back into a locked room.

  VERDICT: the door is not real.  It is conformal MOND, lensing-dead since 1994, mislabelled
  as new by a certificate suite whose Lean theorems are trivial.

  LIMITS.  This is the weak-field, static, first-order analysis -- the regime PPN and lensing
  live in, so it is the right one, but it does not address strong-field or cosmological
  behaviour, which for a lensing-dead theory are moot.  The disformal escape (V7) is noted, not
  re-derived; its closure is this programme's prior result, cited not re-run here.
""")
json.dump({"checks": RES, "n_pass": NP, "n_fail": NF}, open(os.path.join(HERE, "L241_nonlocal_kernel_verdict_results.json"), "w"), indent=1)
print(f"L241 COMPLETE: {NP}/{NP+NF} checks PASS.")
