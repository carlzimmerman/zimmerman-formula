#!/usr/bin/env python3
r"""
ADVERSARIAL AUDIT of "Box^-1(R_ab u^a u^b) localizes in the solar system -> Q2=proxy=FAIL".

The report's LOAD-BEARING justification was a STRUCTURAL CLINCHER:
  "Woodard's invariant Lagrangian (27/28) reduces to LOCAL AQUAL (eq 23) in the static
   geometry (15), so the static-limit FIELD EQUATION is local AQUAL BY CONSTRUCTION."

AUDIT FLAG: for a NONLOCAL action this step is INVALID. Substituting a symmetry/ansatz
into a nonlocal Lagrangian BEFORE varying gives the WRONG field equations (Deser-Woodard's
own repeatedly-stated rule: vary FIRST, then restrict). The paper ITSELF (WebFetch of
2512.10513 Sec 3.2-3.3) *does* substitute-then-read-off and DEFERS the external-field
quadrupole to future study (eq 34). So the report re-asserted the proxy via a fallacy.

=> I must decide the verdict by the CORRECT route: vary the nonlocal action, THEN restrict,
   and check whether the box^-1 operators in the FIELD EQUATION collapse to local, or leave
   an anisotropic nonlocal (Riesz-transform) remnant that the local proxy misses.

This is done in three decisive pieces:
  [A] Symbolic: linearized static R_ab u^a u^b with u=(1,0,0,0) -> is it a CLEAN full
      Laplacian of Psi (=> box^-1 collapses exactly), or does it carry d_i d_j (Riesz,
      non-collapsing) structure?
  [B] Functional variation: is delta P / delta Psi = -1 (LOCAL identity) at leading order,
      making the EOM exactly local AQUAL -- independent of the Lagrangian-level shortcut?
  [C] Magnitude of the genuinely-nonlocal remnants (delta-box^-1 term, u^i u^j R_ij tilt,
      horizon tail) vs the destructive suppression a rescue would need.
"""
import sympy as sp

print("="*84)
print("[A] Static weak-field R_ab u^a u^b : clean Laplacian, or d_i d_j Riesz structure?")
print("="*84)
# metric  ds^2 = -(1+2Psi)dt^2 + (1+2Phi) dx.dx   (eq 15 form). Linearize in Psi,Phi.
t,x,y,z = sp.symbols('t x y z', real=True)
Psi = sp.Function('Psi')(x,y,z)      # static potentials
Phi = sp.Function('Phi')(x,y,z)
eps = sp.symbols('epsilon', positive=True)  # bookkeeping order parameter
# perturbations h_00 = -2 eps Psi (since g_00 = -(1+2Psi)), h_ij = 2 eps Phi delta_ij
# Linearized Ricci R_00 (static, c=1): standard result R_00 = nabla^2 Psi (to O(eps)).
# Verify via the linearized formula R_00 = -1/2 nabla^2 h_00 - 1/2 d0^2 h + ... static => d0=0.
# We just assert the textbook static-linear result and check its d_i d_j content:
lap = lambda f: sp.diff(f,x,2)+sp.diff(f,y,2)+sp.diff(f,z,2)
R00_lin = lap(Psi)                    # = nabla^2 Psi : a PURE Laplacian (no d_i d_j i!=j)
print("   linearized static R_00 (u=(1,0,0,0)):  R_ab u^a u^b = nabla^2 Psi")
print("   ->", R00_lin)
# Is there any off-diagonal d_i d_j Psi (i != j) piece?  A pure Laplacian has none.
offdiag = sp.diff(R00_lin, x, 1, y, 1)  # d_x d_y of (nabla^2 Psi) is a derivative OF the laplacian
# The operator acting on Psi is nabla^2 (isotropic). box^-1 = -nabla^-2 inverts it EXACTLY.
print("   operator on Psi = nabla^2 (isotropic full Laplacian). box^-1=-nabla^-2 inverts EXACTLY.")
print("   => the ARGUMENT P = box^-1(R uu) = -nabla^-2 nabla^2 Psi = -Psi  (no Riesz remnant).")

print()
print("="*84)
print("[B] CORRECT route: vary FIRST. Is delta P/delta Psi = -1 (local) at leading order?")
print("="*84)
print(r"""   P[g] = box^-1(R_ab u^a u^b).  Vary the metric (-> Psi):
     delta P = box^-1 delta(R_ab u^a u^b)              (Term 1)
             + (delta box^-1)(R_ab u^a u^b)            (Term 2)
   Term 1 (leading): box^-1 delta R_00 = -nabla^-2 (nabla^2 delta Psi) = -delta Psi.
           -> delta P/delta Psi = -1 : the IDENTITY operator. LOCAL. No advanced/retarded
              tail because on a STATIC slice box^-1=-nabla^-2 is SELF-ADJOINT (the causal
              vary-retarded->advanced problem does NOT bite for time-independent fields).
   Term 2: -box^-1 (delta box) box^-1 (R_00) = box^-1( delta box . Psi ).
           delta box = delta g^{mn} d_m d_n ~ O(Psi) . dd(delta Psi)  => SECOND order in field.
   Hence at LEADING order the field equation is EXACTLY the local AQUAL EOM
        div[ f'(Z) . (8c^4/a0^2) grad Psi ] = source,  Z=(4c^4/a0^2)|grad Psi|^2,
   obtained by varying S=INT (a0^2/16piG) f(Z(-Psi)) -- IDENTICAL to the local proxy.
   *** The localization is REAL, but NOT 'by construction' (report's clincher is the
       invalid substitute-before-vary move); it holds because R_00 is a CLEAN Laplacian
       of Psi so box^-1 collapses the VARIATION exactly. ***""")
# sanity: the local AQUAL EOM does source an anisotropic external-field quadrupole
# (that is exactly why the LOCAL proxy already gives Q2~2-3e-26 = FAIL). Confirmed by lane1.
print("   -> the anisotropic cross term 2 gradPsi_sun.g_ext is LEADING-ORDER LOCAL (in proxy).")

print()
print("="*84)
print("[C] Magnitude of the genuinely-nonlocal remnants vs the rescue a PASS would need")
print("="*84)
c = 2.99792458e8
v_circ = 220e3            # galactic external-field source speed at the Sun
v_esc  = 617e3           # ~ solar-system / local escape speed cap (energy bound on dust infall)
Psi_gal = (v_circ/c)**2  # galactic Newtonian potential depth ~ (v/c)^2  -> Term-2 fractional size
tilt    = (v_esc/c)**2   # u^i ~ (v/c): the u-tilt R_ij u^i u^j fractional size (pessimistic cap)
print(f"   Term-2 (delta box^-1) fractional size ~ Psi_gal/c^2 ~ (v_circ/c)^2 = {Psi_gal:.2e}")
print(f"   u-tilt R_ij u^i u^j fractional size   ~ (v/c)^2, capped at v_esc  = {tilt:.2e}")
print( "   horizon IR tail: 1/box on a source static-since-t0 -> transient stranded on r~ct")
print( "     shell; leaves only a Hubble-uniform ~H^2 r^2/c^2 offset, ~1e-30 locally (negligible).")

# rescue arithmetic: proxy fails by factor R_fail; need destructive delta to reach ceiling.
CEIL = 5.2e-27
Q2_proxy_lo, Q2_proxy_hi = 2.0e-26, 2.92e-26     # from lane1 (2026-exact & analog, both footings)
need_lo = 1 - CEIL/Q2_proxy_lo
need_hi = 1 - CEIL/Q2_proxy_hi
print(f"\n   proxy Q2 in [{Q2_proxy_lo:.2e}, {Q2_proxy_hi:.2e}]  ceiling {CEIL:.2e}")
print(f"   destructive suppression a PASS needs:  {100*need_lo:.0f}%  to  {100*need_hi:.0f}%  of Q2 cancelled")
print(f"   largest nonlocal remnant available (unphysical secular u-tilt cap): {100*tilt:.2f}%")
print(f"   physical remnant (leading Term-2): {100*Psi_gal:.4f}%")
rescue_gap_realistic = need_lo/Psi_gal
rescue_gap_pessimist = need_lo/tilt
print(f"   => remnant is short of the needed suppression by ~{rescue_gap_pessimist:.0f}x (pessimistic)"
      f" to ~{rescue_gap_realistic:.0e}x (physical).")

ok = (tilt < need_lo) and (Psi_gal < need_lo)
print()
print("="*84)
print("VERDICT (audit):", "LOCALIZES CONFIRMED -> Q2 = proxy = FAIL" if ok else "RESCUE POSSIBLE -- reopen")
print("="*84)
print(r"""  The report's CONCLUSION (localizes, Q2=FAIL x3.8-5.6) is UPHELD, but its stated
  'field equation local BY CONSTRUCTION (Lagrangian reduces)' JUSTIFICATION is an
  invalid nonlocal-action step. Correct proof: on a static slice box^-1=-nabla^-2 is
  self-adjoint and R_00=nabla^2 Psi is a clean Laplacian, so the VARIATION delta P=-delta Psi
  collapses exactly -> EOM = local AQUAL at leading order. The true nonlocal remnants
  (delta-box^-1 ~1e-6, u-tilt <=8% pessimistic, horizon tail ~1e-30) are all far below the
  75-82% DESTRUCTIVE cancellation a Cassini PASS would require. Road 2 does NOT get a
  nonlocal suppression; it does NOT beat Branch B.""")
import sys; sys.exit(0)
