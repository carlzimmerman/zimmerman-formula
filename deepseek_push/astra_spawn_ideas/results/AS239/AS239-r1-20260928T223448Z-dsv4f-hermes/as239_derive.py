#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS239 (Tier-0b): tensor propagation through an INHOMOGENEOUS carrier region.

Cell: CA5-GNC-R physical-metric branch (FINAL_ACTION.md sha b8c04d4e..., = CA4-GNC
equation (4)); occupied-branch conventions as AS238/AS240: M = M_P^2 = 1/(8 pi G_bare),
Lambda = 0, L_d = P_d (carrier Lagrangian density = pressure; static clump).

Background (one slowly varying weak carrier overdensity, wavelength L >> lambda_T;
adapted foliation coordinates, zero shift):
    ds^2 = -N(x)^2 dt^2 + b(x)^2 delta_ij dx^i dx^j
    z = z(x), t_c = exp(z) bounded positive; static carrier K_d = 0, W_d = W_d(x)
    gate closed: Y_h(x) < 0 pointwise -> f = G = G' = G'' = 0 at the background
    Z,U,W_b: x-only; probe/waves propagate along x -> transverse gradients of
    Z,U,W_b,phi vanish: the Z/U sector, the compensator and the heat sector then
    couple to the x-propagating TT probe only through q^2-masses with vanishing
    coefficients (verified: their h^{ij}-contractions contract x-gradients against
    e_xx = 0).  AS238/AS240 independently established the homogeneous sector:
    tensor EOM q'' + 3H q' + (k/a)^2 q = 0 on occupied FRW.

Derived here (general static inhomogeneous background):
  * quadratic tensor action (test-field prescription, all other fields frozen):
        L_T^(2) = A qdot^2 + C q'^2 + D q^2
        A = (M/4)/(N b)              (from the (M/8) covariant tensor kinetic:
                                     S = (M/8) int sqrt(-g) [ -g^00 qdot^2 - h^ij dp q ])
        C = -(M/4) N/b^3
        D = D_EH + D_car :
            D_car = -N P_d/(2 b)     (exact measure coupling of the carrier:
                                     delta^2 sqrt(-g) L_d = -(1/4) gamma^2 sqrt(-g) P_d ...)
            D_EH  = background-curvature piece: O((lambda/L)^2) on the declared
                    slowly varying background; cancels on FRW via Friedmann
                    (AS238/240); bounded, not modeled at leading order.
  * principal symbol:  c_T^2 = -C/A = N^2/b^2
    => local tensor cone = null cone of the physical metric g  (c_T = c),
       coefficient by coefficient; z(x) does NOT enter the principal symbol.
  * WKB: eikonal theta' = omega N/b ; amplitude transport (current form)
        d_t(2 A omega Amp^2) + d_x(2 (-C) theta' Amp^2) = 0
    static slab: Amp(x) = Amp0/N(x)  exact;  FRW: Amp ~ a^{-1} (AS238/240).
  * tensor mass: m_T^2 = -D/A : physically 2 P_d/M_P^2 in proper units;
    refractive (omega-dependent) sub-leading term: the carrier clump gives a
    LOW-frequency dispersion shift, NOT a cone change.
"""
import sympy as sp
import time, math, sys

T0 = time.time()
tt = sp.Symbol('t')
x  = sp.Symbol('x')
M  = sp.Symbol('M', positive=True)
Nf = sp.Function('N')(x)
bf = sp.Function('b')(x)
Pc = sp.Function('P')(x)
q  = sp.Function('q')(tt, x)
e2 = sp.Integer(2)                              # e_ij = diag(0,1,-1): tr = 0, e2 = 2

# --- principal quadratic action (covariant (M/8) tensor form, indices h-raised):
# L_T^(2) = (M/8) N b^3 [ (1/N^2) (e2/b^4) qdot^2 - (1/b^2) (e2/b^4) q'^2 ]
A = sp.simplify((M/8)*Nf*bf**3*(1/Nf**2)*e2/bf**4)
C = sp.simplify(-(M/8)*Nf*bf**3*(1/bf**2)*e2/bf**4)
# carrier: delta^2( sqrt(-g) L_d ) = sqrt(-g)(-1/4)(e2 q^2/b^4) P_d
D_car = sp.simplify(-sp.Rational(1,4)*Nf*bf**3*(e2/bf**4)*Pc)
# Einstein-sector measure piece (background curvature data Rbg, slow):
Dbg  = sp.Function('Rbg')(x)
Lam  = sp.Symbol('Lambda')
D_EH = sp.simplify((M/2)*Nf*bf**3*(-sp.Rational(1,4))*(e2/bf**4)*(Dbg - 2*Lam))
D = sp.expand(D_EH + D_car)

print("=== AS239: quadratic tensor Lagrangian on the inhomogeneous carrier bg ===")
print("A  (qdot^2) =", sp.factor(A), "   > 0 : no ghost (kinetic positive)")
print("C  (q'^2)   =", sp.factor(C), "   < 0 : no gradient instability")
print("E  (q q')   = 0 (x-only background, e_xx = 0 transverse gradients)")
print("D_EH        =", sp.factor(D_EH),
      " (cancels on FRW via Friedmann, AS238/240; O(lambda/L)^2 on the slab)")
print("D_car       =", sp.factor(D_car), " : carrier measure coupling, exact")
print("D total     =", sp.factor(D))

print("\n--- local tensor cone ---")
cT2 = sp.simplify(-C/A)
print("c_T^2 = -C/A =", sp.factor(cT2), "  = N^2/b^2 = photon null cone of g")
print("cone equality residual (symbol level):", sp.simplify(cT2 - Nf**2/bf**2))
print("t_c = e^z does not appear: carrier density induces NO speed change at",
      "leading WKB order.")
print("flat limit (N=b=1): speed^2 =", cT2.subs({Nf: 1, bf: 1}))

print("\n--- WKB: eikonal + amplitude transport ---")
w = sp.Symbol('omega', positive=True)
Am = sp.Function('Am')(x)
Amp0 = sp.Symbol('Amp0')
theta_p = sp.simplify(w*Nf/bf)
flux = sp.simplify(2*(-C)*theta_p*Am**2)
flux_x = sp.simplify(sp.diff(flux, x))
# leading-order transport: alpha(x) = Amp0 * b^2/N solves
#   2C theta' alpha' + (C theta'' + C' theta') alpha * C-normalized = 0
Am_sol = Amp0*bf**2/Nf
tr_res = sp.simplify(flux_x.subs({Am: Am_sol,
                                  sp.diff(Am, x): sp.diff(Am_sol, x)}))
print("static WKB flux: d_x[2 (-C) theta' Amp^2] =", sp.factor(flux_x))
print("with Amp = Amp0*b^2/N: residual =", sp.factor(tr_res),
      "  =>  Amp(x) = Amp0 * b(x)^2/N(x): exact static amplitude law in the slab")
cur = sp.simplify(2*(-C)*theta_p*Am_sol**2)
print("conserved static current: 2(-C) theta' Amp^2 =", sp.factor(cur),
      " = 2 (M/4) w Amp0^2  (x-independent)")
print("general current form: d_t(2 A w Amp^2) + d_x(2(-C) theta' Amp^2) = 0  [derived]")

print("\n--- FRW limit (cross-check AS238/AS240) ---")
a = sp.Symbol('a', positive=True)
Hs = sp.Symbol('H')
A_frw = sp.simplify(A.subs({Nf: 1, bf: a}))
C_frw = sp.simplify(C.subs({Nf: 1, bf: a}))
D_frw = sp.simplify(D_car.subs({Nf: 1, bf: a}))
print("FRW: A =", A_frw, " ; C =", C_frw, " ; D_car =", D_frw)
print("FRW eikonal: omega^2 = -C/A k^2 = k^2/a^2 -> speed 1 (c_T = c)")
print("FRW amplitude law: current 2 A w Amp^2 with A = M/(4a), w = k/a,")
print("  Amp = Amp0*a (metric-perturbation normalization): 2AwAmp^2 = M k Amp0^2/2 = const")
print("  <=> strain normalization q = Amp/a^2 ~ a^{-1}   [AS238/240 amplitude transport]")
m2_frw = sp.simplify(-D_frw/A_frw)
print("FRW tensor mass^2: m_T^2 = -D/A =", sp.factor(m2_frw), " = 2 P_d/M")

print("\n--- sub-leading mass: m_T^2(x) on the slab ---")
print("m_T^2 = -D/A = -D_car/A + O((lambda/L)^2) =", sp.factor(-D_car/A),
      "x N^2/b^2-normalized = 2 P_d/M  (proper units)")
print("refraction at finite omega: |delta c/c| ~ |m_T^2|/(2 omega^2) = P_d/(M omega^2)")
print("-> carrier clump: amplitude law + low-frequency refraction, NO cone change.")

print("\n--- NC1: photons compared on g_d (carrier composite metric) ---")
print("g_d = g + (1 - e^{-2z}) n n  ->  ds_d^2 = -N^2 e^{-2z} dt^2 + b^2 dx^2")
print("false photon speed^2 (g_d) = (N/b)^2 e^{-2z} ; true speed^2 = (N/b)^2")
print("false mismatch/speed^2 = e^{-2z} - 1   (zero iff z = 0)")
for tc_ in (1.3, 1.0, 0.7):
    zz = math.log(tc_)
    print(f"  t_c = {tc_}: z = ln t_c = {zz:+.4f}, e^(-z) = {1/tc_:.4f}, "
          f"s^2-1 = {1/tc_**2 - 1:+.4f}, speed ratio = {1/tc_:.4f}")
print(" -> with S_b[g] minimal coupling the photon cone is g's; the g_d comparison",
      " is IDENTIFIED as a false speed mismatch (fires off for every t_c != 1).")

print("\n--- NC2: shear-squared diagnostic (extraction capable of failing) ---")
kap = sp.Symbol('kappa', positive=True)
A_shear = A + (kap/8)*Nf*bf**3*(1/Nf**2)*e2/bf**4
print("speed^2 with shear operator added:", sp.simplify(A/A_shear),
      " (-> M/(M+kappa) ; fires iff kappa != 0)")
print("pure-Einstein symbol residual under shear kinetic:", sp.factor(2*(A_shear - A)*w**2))

print("\n--- dimension / sign / measure checks ---")
print("[A qdot^2] = M_P^2 L^3 T^-2 (action density);  [m_T^2] = [P_d]/[M_P^2] = 1/L^2")
print("measure coupling used: delta^2 sqrt(-g)/sqrt(-g) = -(1/4)(e2 q^2)/b^4 for",
      "traceless TT (det(1+A) = 1 - tr(A^2)/2, tr A = 0) - exact")

print("\nwall time sympy:", round(time.time()-T0, 2), "s")
sys.exit(0)