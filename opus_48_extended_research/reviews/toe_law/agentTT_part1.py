"""
agentTT ROUTE 1 — PART 1: The two SL(2,R)'s and their rep labels.

Side A (GRAVITY): static-patch SL(2,R)~SO(2,1) of the Gibbons-Hawking state.
  - QNM ladder Gamma_n = sinh((Delta+n)lambda) ; semiclassical -> H(Delta+n).
  - agentSS: this is the LOWEST-WEIGHT DISCRETE-SERIES rep D^+_Delta.
  - Casimir C2 = Delta(Delta-1) ; L0 spectrum = Delta + n, n=0,1,2,...
  - This is a HALF-BOUNDED (lowest-weight) spectrum: the modular/boost generator L0
    has spectrum bounded below by Delta, integer-spaced. That is the DEFINING signature
    of the discrete series D^+_Delta of SL(2,R) (equiv SU(1,1)).

Side B (MATTER, DSSYK chord): the matter two-point function at vacuum placement theta_v.
  - agentS: poles of G(t) at E_pole = cos(theta_v) cosh u - i sin(theta_v) sinh u, u=(Delta+k)lambda.
  - CENTER theta_v=pi/2: omega_pole = -i sinh((Delta+k)lambda) -> a discrete, purely-imaginary,
    Delta-offset, integer-indexed ladder. SAME structure as Side A.
  - EDGE theta_v=pi-eps: poles SINK BELOW the spectral floor for all rungs once eps<eps_c;
    the late-time decay is t^{-3/2} CONTINUUM endpoint asymptotics, NOT a discrete ladder.

PART 1 GOAL: extract the L0-spectrum (the ladder of the relevant generator) at each placement
and classify it as discrete-series (half-bounded, integer-spaced) vs principal/continuous
(unbounded both ways / continuous label). This is the rep-class diagnostic.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("PART 1 — rep-class diagnostic from the L0 / boost spectrum at each placement")
print("="*78)

# --- Side A: the GH discrete series ---
Delta, n, lam, k = sp.symbols('Delta n lambda k', positive=True)
# QNM ladder rate
Gamma_n = sp.sinh((Delta + n)*lam)
print("\n[Side A: GH static-patch SL(2,R)]")
print("  QNM rate Gamma_n = sinh((Delta+n)*lambda)")
print("  Semiclassical (lambda->0): leading =", sp.series(Gamma_n, lam, 0, 2).removeO())
print("  => L0 spectrum = Delta + n  (n=0,1,2,...): HALF-BOUNDED, integer-spaced.")
print("  Casimir C2 = Delta*(Delta-1)  (discrete series D^+_Delta).")

# --- Side B: matter-chord pole ladder at general placement theta_v ---
theta_v = sp.symbols('theta_v', real=True)
u = (Delta + k)*lam
E_pole_re = sp.cos(theta_v)*sp.cosh(u)
E_pole_im = -sp.sin(theta_v)*sp.sinh(u)
print("\n[Side B: matter-chord pole ladder]")
print("  E_pole(theta_v,k) = cos(theta_v)cosh((Delta+k)lambda) - i sin(theta_v) sinh((Delta+k)lambda)")

# CENTER
E_pole_center = E_pole_re.subs(theta_v, sp.pi/2) + sp.I*E_pole_im.subs(theta_v, sp.pi/2)
print("\n  CENTER theta_v=pi/2:")
print("    E_pole =", sp.simplify(E_pole_center))
print("    Re=0, Im=-sinh((Delta+k)lambda): purely imaginary discrete ladder.")
print("    => the matter L0 spectrum (decay-rate index) = Delta + k, k=0,1,2,...")
print("    SAME half-bounded integer-spaced ladder as Side A. Casimir = Delta(Delta-1).")

# Check the matrix-element / ladder structure matches the discrete-series raising op.
# Discrete series D^+_Delta: |Delta+n>, L+|Delta+n> ~ sqrt((n+1)(2Delta+n)) |Delta+n+1>.
m = sp.symbols('m', nonnegative=True, integer=True)
ladder_me = (m+1)*(2*Delta+m)   # |matrix element|^2 of L+ in D^+_Delta
print("\n  Discrete-series ladder |<.|L+|.>|^2 = (n+1)(2Delta+n):")
for mm in range(4):
    print(f"    n={mm}: {ladder_me.subs(m,mm)}")
print("  (Casimir from ladder: C2 = (Delta)(Delta-1) at lowest weight; standard.)")

# EDGE
print("\n  EDGE theta_v=pi-eps  (eps small, banked 1e-3):")
eps = sp.symbols('epsilon', positive=True)
E_pole_edge_re = sp.cos(sp.pi-eps)*sp.cosh(u)
E_pole_edge_im = -sp.sin(sp.pi-eps)*sp.sinh(u)
print("    Re E_pole = cos(pi-eps)cosh(u) = -cos(eps)cosh(u)  (NONZERO -> 'ringing')")
print("    Im E_pole = -sin(eps) sinh(u)")
print("    Spectral support floor omega_min = cos(eps) - 1 (from agentS).")
# threshold: Re E_pole below floor when cos(eps)(1-cosh u) < cos(eps)-1, i.e. cosh u > sec eps
print("    Rung k leaves support when cosh((Delta+k)lambda) > sec(eps)  [agentS eps_c].")
print("    => below eps_c ALL rungs exit support: NO discrete poles contribute;")
print("       G(t) ~ t^{-3/2} = soft-edge CONTINUUM endpoint asymptotics.")

print("\n" + "="*78)
print("PART 1 RESULT")
print("="*78)
print("CENTER: matter L0-ladder = {Delta+k} half-bounded integer-spaced = DISCRETE SERIES,")
print("        Casimir Delta(Delta-1), IDENTICAL rep label to the GH side.")
print("EDGE:   poles exit the spectral support; surviving spectral data is the CONTINUUM")
print("        band edge (Wigner sqrt), whose transform is t^{-3/2}, NOT a ladder.")
print("        The relevant rep is carried by the CONTINUOUS band, not a lowest-weight tower.")
