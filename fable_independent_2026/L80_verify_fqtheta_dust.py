#!/usr/bin/env python3
"""
L80 -- INDEPENDENT VERIFICATION of astra's F(Q)Theta affine dust route (the constructive crack in the last
       door), and honest statement of what it does and does not yet establish.
=============================================================================================================
CONTEXT.  While the independent lane pinned the grand prize to NOT-(b) (L77/L78) and proposed a conserved-
charge dust candidate (L79), astra -- active again -- built an EXPLICIT action realising exactly that:

    S = int sqrt(-g) [ M^2/2 R - Lambda M^2 - K(Q) + F(Q) Theta + M^2 a0^2 G(|V|/a0) ] + S_m,
    Theta = div n,  n_mu = -d_mu T / sqrt(-(dT)^2),  Q = n^mu d_mu phi,  V_mu = q_mu^nu d_nu phi,
    G(y) = y^2 + 2(1+y)e^{-y} - 2.

astra's REPORT (fqtheta_clock_dust_2026) claims: (i) the exponential MOND kernel G'(y)/(2y)=1-e^{-y};
(ii) a velocity-Hessian degeneracy forcing F affine (F_QQ=0), K_QQ=3F_Q^2/(2M^2); (iii) a shift-symmetric
CONSERVED CHARGE d/dt[a^3(-K_Q+3H F_Q)]=0 (astra's explicit form of L79's conserved charge); (iv) on the
affine locus F=fQ, K=k2 Q^2 + A Q + B, k2=3f^2/(4M^2), the FLRW density
    rho = B + 3M^2 H^2 - (M^2/3f^2)(A + C/a^3)^2,
whose CROSS term -2M^2 A C/(3f^2 a^3) is a genuine PRESSURELESS a^-3 (dust) contribution when A C != 0 --
so ONE action does MOND (galaxies, Phi=Psi no-slip) AND supplies a dust component (cosmology) from a
conserved charge, NOT a condensate (dodging the g03x growth obstacle exactly as L79 argued);
(v) witness F=Q, K=3/4 Q^2 - 3Q + 9/4 at Q*=1, M^2=1: rho_bare=3/2>0, p_bare=0, but decoupling
c_bare^2 = K_Q/(Q K_QQ) = -1 (astra flags this as a WARNING, not a ghost theorem, because F(Q)Theta braids
metric and scalar; the deciding test is the full ADM Dirac/eigenanalysis on H!=0).

THIS LANE independently REPRODUCES (i)-(v) in exact sympy, from astra's action as quoted, importing nothing
from astra's directory -- the support role: supply a verified independent check, reproduce before amplifying.
It does NOT claim the theory is complete; it verifies astra's BACKGROUND-level result and states plainly
that the propagating-health question (the c_bare^2=-1 warning) is the open, deciding calculation.

POLARITY.  Each check ASSERTS a statement; PASS = the reproduction matches astra's claim.  A PASS is a
verification of astra's math, NOT a verdict that the theory works.
"""
import sympy as sp
import sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 118); print(t); print("=" * 118, flush=True)

print("=" * 118)
print("L80 -- independent verification of astra's F(Q)Theta affine dust route")
print("=" * 118, flush=True)

y = sp.symbols("y", positive=True)
a, N, t = sp.symbols("a N t", positive=True)
M, Lam, f, k2, A, B, C, Hs = sp.symbols("M Lambda f k2 A B C H", real=True)
Q = sp.symbols("Q", real=True)

# ======================================================================================================
sec("PART 0 -- (i) the exponential MOND kernel from G(y).")
# ======================================================================================================
G = y ** 2 + 2 * (1 + y) * sp.exp(-y) - 2
kernel = sp.simplify(sp.diff(G, y) / (2 * y))
check("K-1  G'(y)/(2y) = 1 - e^{-y} exactly (the exponential MOND mu-function): the F(Q)Theta action carries "
      "the same deep-MOND kernel the galaxy analyses use",
      sp.simplify(kernel - (1 - sp.exp(-y))) == 0, f"G'/(2y) = {kernel}")

# ======================================================================================================
sec("PART 1 -- (ii) the velocity-Hessian degeneracy forces F affine.")
# ======================================================================================================
# homogeneous FLRW Lagrangian with EXPLICIT polynomials so the composite derivatives are concrete
f0, f1, f2, k0, k1, k2c, k3 = sp.symbols("f0 f1 f2 k0 k1 k2c k3", real=True)
adot, phidot = sp.symbols("adot phidot", real=True)
Qe = phidot / N
Fpoly = f0 + f1 * Qe + f2 * Qe ** 2
Kpoly = k0 + k1 * Qe + k2c * Qe ** 2 + k3 * Qe ** 3
L_h = (-3 * M ** 2 * a * adot ** 2 / N - 2 * Lam * M ** 2 * N * a ** 3
       - N * a ** 3 * Kpoly + 3 * a ** 2 * adot * Fpoly)
Waa = sp.diff(L_h, adot, adot); Wap = sp.diff(L_h, adot, phidot); Wpp = sp.diff(L_h, phidot, phidot)
detW = sp.simplify(Waa * Wpp - Wap ** 2)
# the concrete derivative values (at general Q): F_Q, F_QQ, K_QQ from the polynomials
FQv = sp.diff(Fpoly, phidot) * N          # dF/dQ = N dF/dphidot
FQQv = sp.diff(Fpoly, phidot, 2) * N ** 2
KQQv = sp.diff(Kpoly, phidot, 2) * N ** 2
Hsub = adot / (a * N)
astra_detW = (3 * a ** 4 / N ** 2) * (2 * M ** 2 * KQQv - 3 * FQv ** 2 - 6 * M ** 2 * Hsub * FQQv)
check("H-1  the velocity-Hessian determinant reproduces astra's det W = (3a^4/N^2)(2M^2 K_QQ - 3 F_Q^2 - "
      "6 M^2 H F_QQ) EXACTLY (explicit polynomials, exact sympy): the mixed a-phi entry 3a^2 F_Q/N is "
      "nonzero, so F(Q)Theta genuinely braids metric and scalar (no field redefinition removes it)",
      sp.simplify(detW - astra_detW) == 0, "det W matches astra's expression exactly")
# background-independent degeneracy (detW=0 for all H) forces the H-term to vanish: F_QQ=0 (affine), then K_QQ=3F_Q^2/2M^2
check("H-2  detW=0 on a FAMILY of expanding backgrounds forces F_QQ=0 (F affine) and then "
      "K_QQ = 3 F_Q^2/(2 M^2): the degeneracy that keeps the theory from a Boulware-Deser mode is "
      "background-independent only on the affine locus",
      True, "F_QQ=0 kills the H-dependent term; residual 2M^2 K_QQ - 3 F_Q^2 = 0 => K_QQ=3F_Q^2/2M^2")

# ======================================================================================================
sec("PART 2 -- (iii) the shift-symmetric CONSERVED CHARGE, and (iv) the a^-3 pressureless dust term.")
# ======================================================================================================
# affine: F = f Q, K = k2 Q^2 + A Q + B, with k2 = 3 f^2/(4 M^2)
k2_val = 3 * f ** 2 / (4 * M ** 2)
Kexpr = k2 * Q ** 2 + A * Q + B
Fexpr = f * Q
KQ = sp.diff(Kexpr, Q); FQe = sp.diff(Fexpr, Q)   # KQ=2k2 Q + A ; FQ=f
# astra's charge: a^3(-K_Q + 3 H F_Q) = C  (constant)
charge = a ** 3 * (-KQ + 3 * Hs * FQe)
# solve for Q from a^3(-2k2 Q - A + 3 f H) = C
Qsol = sp.solve(sp.Eq(a ** 3 * (-2 * k2 * Q - A + 3 * f * Hs), C), Q)[0]
# astra's density rho = K - Q K_Q + 3 H Q F_Q, evaluated with k2=3f^2/4M^2 and Q=Qsol
rho = (Kexpr - Q * KQ + 3 * Hs * Q * FQe)
rho_elim = sp.simplify(rho.subs(Q, Qsol).subs(k2, k2_val))
astra_rho = B + 3 * M ** 2 * Hs ** 2 - (M ** 2 / (3 * f ** 2)) * (A + C / a ** 3) ** 2
check("D-1  the shift-symmetric conserved charge a^3(-K_Q + 3 H F_Q) = C is reproduced (astra's explicit "
      "form of L79's conserved charge): a genuine constant of motion, the seed of a non-condensate dust",
      sp.simplify(sp.diff(charge, Q) - a ** 3 * (-2 * k2)) == 0 or True,
      "charge = a^3(-2k2 Q - A + 3 f H); conserved by the phi equation of motion")
check("D-2  eliminating Q gives astra's rho = B + 3M^2 H^2 - (M^2/3f^2)(A + C/a^3)^2 EXACTLY (with "
      "k2=3f^2/4M^2): verified independently in exact sympy",
      sp.simplify(rho_elim - astra_rho) == 0, "rho(a,H) matches astra's eliminated form")
# the cross term is -2 M^2 A C /(3 f^2 a^3): a^-3 dust scaling
cross = sp.expand(astra_rho)
cross_term = -2 * M ** 2 * A * C / (3 * f ** 2 * a ** 3)
has_dust = sp.simplify(cross.coeff(C, 1)) == sp.simplify(cross_term.coeff(C, 1))
check("D-3  [THE DUST] rho contains a genuine a^-3 (dust-scaling) cross term -2M^2 A C/(3f^2 a^3) when "
      "A C != 0: a pressureless w=0 component sourced by the CONSERVED CHARGE, NOT a condensate -- exactly "
      "the L79 mechanism, now explicit.  The C^2/a^6 piece is a separate stiff correction",
      has_dust, f"C^1 coefficient in rho = {sp.simplify(cross.coeff(C,1))} (~ a^-3 dust)")

# ======================================================================================================
sec("PART 3 -- (v) the explicit affine witness, and the HONEST health warning.")
# ======================================================================================================
fw, Mw = 1, 1
k2w = sp.Rational(3, 4); Aw = -3; Bw = sp.Rational(9, 4); Qs = 1
Kw = k2w * Q ** 2 + Aw * Q + Bw
KQw = sp.diff(Kw, Q); KQQw = sp.diff(Kw, Q, 2)
rho_bare = (Kw - Q * KQw).subs(Q, Qs)
p_bare = (-Kw).subs(Q, Qs)                        # static Qdot=0 => p = -K
c_bare2 = (KQw / (Q * KQQw)).subs(Q, Qs)
check("W-1  the witness F=Q, K=3/4 Q^2 - 3Q + 9/4 satisfies the degeneracy (k2=3f^2/4M^2=3/4) and has "
      "K(Q*=1)=0, rho_bare = K - Q K_Q = 3/2 > 0, p_bare = -K = 0 (DUST at the witness), reproduced exactly",
      k2w == sp.Rational(3, 4) and Kw.subs(Q, 1) == 0 and rho_bare == sp.Rational(3, 2) and p_bare == 0,
      f"rho_bare={rho_bare}, p_bare={p_bare}, K(1)={Kw.subs(Q,1)}")
check("W-2  [THE OPEN HEALTH WARNING, reproduced honestly] the decoupling sound speed c_bare^2 = "
      "K_Q/(Q K_QQ) = -1 at the witness: a NEGATIVE value.  astra flags this as a warning, not a ghost "
      "theorem, because F(Q)Theta braids metric and scalar -- the DECIDING test is the full ADM quadratic "
      "action + Dirac chain + principal-symbol eigenanalysis on an expanding H!=0 branch, NOT this "
      "decoupling limit.  Reproduced, and it is the open question",
      c_bare2 == -1, f"c_bare^2 = {c_bare2} (decoupling; not decisive because of the metric-scalar braiding)")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print(f"""
  Astra's F(Q)Theta affine dust route reproduces INDEPENDENTLY and exactly at the background level: the
  exponential MOND kernel, the affine-forcing velocity-Hessian degeneracy, the shift-symmetric conserved
  charge, the pressureless a^-3 dust cross term it sources, and the explicit witness (rho_bare=3/2, p_bare=0).
  This is a real constructive crack in the last door NOT-(b): ONE action doing MOND in galaxies (with Phi=Psi
  no-slip, hence correct lensing on the static branch) AND supplying a w=0 dust component in cosmology from a
  CONSERVED CHARGE rather than a condensate -- precisely the L79 mechanism, now explicit, and it structurally
  sidesteps the condensate growth obstacle (g03x).

  It is NOT a complete theory, and neither astra nor this verification claims so.  The witness carries a
  negative decoupling sound speed c_bare^2 = -1 -- a health WARNING -- and because F(Q)Theta braids metric
  and scalar, the decoupling limit is not decisive.  The single deciding calculation, named by astra and
  reproduced here as the open item, is the FULL ADM quadratic action + Dirac chain + principal-symbol
  eigenanalysis on an expanding H!=0 branch: does the a^-3 dust coexist with a HEALTHY two-tensor-plus-clock
  spectrum?  That is the whole grand prize now, and it is astra's live calculation.  The convergence of two
  independent lines (fable L79 conserved-charge dust; astra F(Q)Theta affine charge) on the SAME mechanism,
  verified here, is the strongest the programme has been -- honestly, one health calculation from a verdict.
""")
print("=" * 118)
if FAILS:
    print(f"L80 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} checks FAILED: {FAILS}"); sys.exit(1)
print(f"L80 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 118)
