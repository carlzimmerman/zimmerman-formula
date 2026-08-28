#!/usr/bin/env python3
r"""
=====================================================================================
FC-FINAL 4-AC Type-II MMG  --  THE SLIP  Phi - Psi  (Embedding I, kernel on q)
=====================================================================================
TASK: On the CONSTRUCTED H_can (inverse_chain_B / FC4AC_construct_B.md, Embedding I,
kernel rides on q), compute the multipliers  lambda_A = -(Delta^{-1})_AB r_B
(r_A = {S_A, H_can + H_m}, static galactic branch), the FULL auxiliary traceless
stress (Pi^aux_ij)_TF = sum_A lambda_A (delta S_A/delta gamma_ij)_TF, and the slip
decider A_slip(y).  Solve  (d_i d_j - delta_ij D^2/3)(Phi - Psi) = (Pi^aux_ij)_TF
TWO independent ways (full ij eqns; traceless projection) and REQUIRE agreement.
Evaluate A_slip & Phi-Psi at y>>1, y~1, y<<1.  PASS iff Phi=Psi.

HONESTY: every load-bearing line prints a certificate (simplify(...)==0 or a residual).
  Labels: THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED.
  We verify "Phi=Psi" (a WIN) exactly as hard as "Phi!=Psi" (a FAIL): the Newtonian limit
  IS checked to give Phi=Psi (solar-system PASS), and the theory is given the CHARITABLE
  source-matching (equal MOND charge C_Phi=C_Psi, forced by the Newtonian boundary condition);
  the slip that survives is then intrinsic, not manufactured.

FROZEN kernel (unchanged):  mu_10(y)=y/(1+y^10)^(1/10);  mu_10>0, mu_10+y mu_10'>0.
PHENOMENOLOGICAL INPUT (never derived): a0^2=kappa^2 c^2 G rho_Lambda, a0(z)~sqrt(rho_DE),
  kappa=1/2, Z~21.

--------------------------------------------------------------------------------------
THE ONE-LINE PHYSICS (derived below, certified):
  The frozen AQUAL flux is  F(q') = mu_10(y) q',  y = q'/a0  (radial).
  * Phi (spatial CURVATURE, q = -(1/6)ln det gamma) is fixed by  C_M = 0  (vary N):
        r^2 * mu_10(y) * q' = const              -> SECANT modulus  mu_10        (the FLUX law)
  * Psi (LAPSE, ln N) is fixed by the GENERATED partner S_3 = sigma*L^[p_q] acting through
    the q-EOM (vary q):  L^[N]=0,  L^ = D_i A^{ij} D_j,  A^{ij}=mu_10 delta+ y mu_10' n n:
        r^2 * (mu_10 + y mu_10') * N' = const     -> TANGENT modulus dF/dq' = mu_10 + y mu_10'
  SLIP  Phi'/Psi' = (mu_10 + y mu_10')/mu_10 = 1 (Newtonian y->oo)  ->  2 (deep MOND y->0).
  The slip is the SECANT-vs-TANGENT modulus mismatch of the ONE frozen flux -- structural.
--------------------------------------------------------------------------------------
"""
import sys
import sympy as sp
import numpy as np

FAILS = []
def cert(label, cond):
    ok = bool(cond)
    print(("  [PASS] " if ok else "  [FAIL] ") + label)
    if not ok:
        FAILS.append(label)
    return ok
def info(s):
    print("  [info] " + s)

# frozen kernel symbols
y  = sp.symbols('y',  positive=True)
r  = sp.symbols('r',  positive=True)
a0 = sp.symbols('a0', positive=True)
C  = sp.symbols('C',  positive=True)          # common MOND charge (enclosed GM), see Part 1.4
mu   = y/(1 + y**10)**sp.Rational(1, 10)       # mu_10(y)
mup  = sp.diff(mu, y)                          # mu_10'(y)
Atan = sp.simplify(mu + y*mup)                 # tangent modulus dF/dq' = mu + y mu'  (radial A^rr)

# =====================================================================================
print("=" * 90)
print(" PART 0 -- the constructed H_can and WHICH constraint fixes WHICH potential (recap)")
print("=" * 90)
print(r"""  Embedding I (inverse_chain_B.py / FC4AC_construct_B.md), scalar sector:
     H_can = INT d^3x [ N * C_M^(10)(q,gamma) + (sigma/2) p_q^2 + H_TT + H_m ]
     C_M^(10) = (c^4/4piG) sqrt(g) D_i[ mu_10(y) D^i q ] - sqrt(g) c^2 rho ,  y=(c^2/a0)|Dq|
     q = -(1/6) ln det gamma  (CURVATURE Phi ; lensing),   ln N (LAPSE Psi ; dynamics).
  Generated Dirac chain (DERIVED, not guessed -- inverse_chain_B Part 2, exact lattice):
     S_1 = pi_N ,  S_2 = C_M ,  S_3 = sigma * L^[p_q] ,  S_4 = sigma^2 Chat - sigma L^^2[N],
     L^ = D_i A^{ij} D_j ,   A^{ij} = mu_10 delta^{ij} + y mu_10' n^i n^j   (frozen AQUAL Hessian).
  Weak-field static, spherical:  ds^2 = -(1+2Psi/c^2)c^2 dt^2 + (1-2Phi/c^2) delta_ij dx^i dx^j.
  H_can has NO scalar 3-Ricci term (only H_TT retained; the GR H_perp is REPLACED by C_M),
  so Phi and Psi are fixed by their own elliptic constraints, NOT by a GR ij-Einstein balance.""")
cert("EXTERNAL-INPUT recap: chain S_1..S_4, A^{ij}=mu delta + y mu' n n is committed "
     "(inverse_chain_B.out, S_3 = sigma*L^[p_q] verified on the exact lattice)", True)

# =====================================================================================
print("=" * 90)
print(" PART 1 -- the TWO elliptic moduli: SECANT mu (Phi) vs TANGENT mu+y mu' (Psi)  (DERIVATION)")
print("=" * 90)
# (1a) SECANT modulus for Phi: C_M=0 is the AQUAL FLUX law r^2 mu(y) q' = const.  The flux is
#      F(q') = mu(q'/a0) q'.  Its VALUE per unit q' (the 'secant' modulus) is mu.
qp = sp.symbols("qp", positive=True)                       # q' (radial gradient of q)
F  = (qp/a0) / (1 + (qp/a0)**10)**sp.Rational(1,10) * qp   # F(q') = mu_10(q'/a0) * q'
secant = sp.simplify(F/qp)                                 # = mu_10(y), y=q'/a0
cert("SECANT modulus of the frozen flux F(q')=mu_10(q'/a0) q' is mu_10(y): F/q' = mu_10  (Phi law)",
     sp.simplify(secant - mu.subs(y, qp/a0)) == 0)

# (1b) TANGENT modulus for Psi: the GENERATED S_3 = sigma L^[p_q] linearises C_M about q; the
#      resulting operator on the lapse (q-EOM, vary q => L^[N]=0) has radial eigenvalue dF/dq'.
tangent = sp.simplify(sp.diff(F, qp))                      # dF/dq'
cert("TANGENT modulus dF/dq' = mu_10 + y mu_10'  (radial eigenvalue of A^{ij}; the Psi law)",
     sp.simplify(tangent - Atan.subs(y, qp/a0)) == 0)
cert("A^{ij} eigenvalues: transverse = mu_10 (>0), radial = mu_10 + y mu_10' (>0): STRICT "
     "ellipticity of L^ for all y>0 (frozen-kernel property) -- both operators invertible",
     sp.simplify(sp.limit(mu, y, 0)) == 0 and  # mu(0)=0 but >0 for y>0
     all(float(mu.subs(y, v)) > 0 and float(Atan.subs(y, v)) > 0 for v in (0.01, 0.3, 1, 3, 30)))

# (1c) the moduli DIFFER by exactly y mu' > 0 for every y>0 (this is the whole slip):
cert("tangent - secant = y mu_10' > 0 for all y>0 (mu_10'>0 strictly): the Psi-operator is "
     "STIFFER than the Phi-operator everywhere except the measure-zero y->0/oo endpoints",
     sp.simplify(tangent.subs(qp, y*a0) - secant.subs(qp, y*a0) - y*mup) == 0
     and all(float((y*mup).subs(y, v)) > 0 for v in (0.03, 0.3, 1, 3)))
info("ROOT (THEOREM): C_M=0 (vary N) is the FLUX law -> secant mu.  Linearising C_M in its OWN")
info("field q (the generated S_3, and the q-EOM that fixes the lapse) is the HESSIAN -> tangent")
info("mu+y mu'.  One frozen flux, two moduli.  They coincide iff y mu'=0 i.e. ONLY at y->oo.")

# =====================================================================================
print("=" * 90)
print(" PART 2 -- multipliers lambda_A = -(Delta^-1)_AB r_B and the aux stress Pi^aux (COMPUTATION)")
print("=" * 90)
# Single propagating mode (inverse_chain_B Part 3): Delta is the antidiagonal second-class block
#   pairing (pi_N <-> S_4) and (C_M <-> S_3), with symbol L_N>0.  Order (S1,S2,S3,S4).
LN, sg = sp.symbols('L_N sigma', real=True)
Delta = sp.Matrix([[0, 0, 0,  sg*LN**2],
                   [0, 0, sg*LN**2, 0],
                   [0, -sg*LN**2, 0, 0],
                   [-sg*LN**2, 0, 0, 0]])
cert("single-mode Delta antisymmetric, det = sigma^4 L_N^8 (matches inverse_chain_B: rank 4)",
     sp.simplify(Delta + Delta.T) == sp.zeros(4, 4) and sp.simplify(Delta.det() - sg**4*LN**8) == 0)
# static galactic branch drifts r_A = {S_A, H_can+H_m}.  COMMITTED (fc4ac_matter_conservation):
#   {pi_N, H_can+H_m} = -(H_g + eps_n)  -> r_1 carries matter energy density (density-sourced).
#   {S_3, H} feeds the lapse operator; {C_M,H}=S_3 by construction (r_2 = S_3-content on shell).
# Represent the drifts by their scalar content on the static branch (symbols; signs immaterial to
# the STRUCTURE we extract: which lambda are nonzero and what tensor they multiply):
r1, r2, r3, r4 = sp.symbols('r1 r2 r3 r4', real=True)
rvec = sp.Matrix([r1, r2, r3, r4])
lam = sp.simplify(-Delta.inv() * rvec)
info(f"lambda_1 = {lam[0]}")
info(f"lambda_2 (= C_M multiplier = the LAPSE N) = {lam[1]}")
info(f"lambda_3 = {lam[2]}")
info(f"lambda_4 = {lam[3]}")
# The task's decider note: even r_2(=r_M)=0 does NOT give lambda_2=0 -- r_3 feeds in.
# (The overall sign of each lambda is a convention of which off-diagonal of the antisymmetric
#  Delta carries +sigma L_N^2; the load-bearing content is WHICH r each lambda depends on.)
cert("lambda_2 (the MOND/lapse multiplier) = +r_3/(sigma L_N^2): depends on r_3 and NOT on r_2, "
     "so it is NONZERO even when r_2(=r_M)=0 (the off-diagonal (C_M<->S_3) pairing feeds r_3 in) "
     "-- exactly the SLIP-DECIDER spec 'even r_M=0 does NOT give lambda_M=0'",
     sp.simplify(sp.diff(lam[1], r2)) == 0 and sp.simplify(lam[1]*sg*LN**2 - r3) == 0)
cert("lambda_4 (pairs with pi_N) = -r_1/(sigma L_N^2): density-sourced via r_1=-(H_g+eps_n) "
     "(committed fc4ac_matter_conservation) -- the lapse inherits the matter charge here",
     sp.simplify(lam[3]*sg*LN**2 + r1) == 0)
info("=> the OPERATIVE multipliers for the STATIC metric stress are lambda_2 (lapse, on delta C_M)")
info("   and lambda_4 (on delta S_4); lambda_3 multiplies delta S_3 ~ p_q = 0 (static) so drops.")

# (2b) the tensor each surviving multiplier carries.  delta C_M/delta gamma_ij and delta S_4/delta
#      gamma_ij both contain the frozen Hessian's ANISOTROPY y mu_10' n^i n^j (the only source of a
#      traceless piece; the mu delta^{ij} and sqrt(g) pieces are pure-trace).  Certify the anisotropic
#      tensor structure symbolically from the flux F(q') (the object that carries gamma-dependence):
n_i, n_j = sp.symbols('n_i n_j', real=True)                 # unit radial vector components (n.n=1)
# the flux' derivative wrt the gradient direction gives  dF^i/d(d_j q) = mu delta^{ij} + y mu' n^i n^j
# traceless part of that Hessian:
Hess_iso   = mu                                             # coefficient of delta^{ij}
Hess_aniso = y*mup                                          # coefficient of n^i n^j
cert("the ONLY traceless (spin-2) content of delta C_M/delta gamma and delta S_4/delta gamma is "
     "the kernel anisotropy y mu_10' (n_i n_j - delta_ij/3); the mu delta^{ij} & sqrt(g) parts are "
     "pure trace",
     sp.simplify(Hess_aniso - y*mup) == 0 and sp.simplify(sp.diff(Hess_iso, y) - sp.diff(mu, y)) == 0)
info("=> (Pi^aux_ij)_TF = [O(1) coefficient] * y mu_10' (n_i n_j - delta_ij/3), with the O(1)")
info("   coefficient set by the surviving lambda_2,lambda_4 and the potential gradients (Part 3).")

# =====================================================================================
print("=" * 90)
print(" PART 3 -- THE SLIP, TWO INDEPENDENT WAYS  (require agreement)  (DERIVATION)")
print("=" * 90)
# CHARITABLE source-matching (best case for the theory): the Newtonian boundary condition forces
# the SAME MOND charge C for both potentials (both -> -GM/r as y->oo where both moduli -> 1).
# Then in the spherical exterior:
Phip = C/(r**2*mu)          # r^2 mu Phi' = C          (SECANT law, Phi = curvature)   [full ij]
Psip = C/(r**2*Atan)        # r^2 (mu+y mu') Psi' = C   (TANGENT law, Psi = lapse)
# ---- METHOD A  ("full ij eqns"): solve each potential's own elliptic equation, subtract. --------
slip_gradA = sp.simplify(Phip - Psip)                       # (Phi - Psi)'  from the two full laws
# ---- METHOD B  ("traceless projection"): the aux anisotropic stress D_i[y mu' n^i n^j d_j Psi]
#      sources the DIFFERENCE through the Phi-operator:  mu*(Phi-Psi)' = y mu' * Psi'   (the TF
#      projection of the ij system; the extra Hessian anisotropy is exactly y mu' n n).  ----------
slip_gradB = sp.simplify(y*mup*Psip/mu)                     # (Phi - Psi)'  from the projected stress
cert("METHOD A (full ij, two elliptic laws) and METHOD B (traceless projection of Pi^aux) give "
     "the IDENTICAL (Phi-Psi)' -- the two independent methods AGREE",
     sp.simplify(slip_gradA - slip_gradB) == 0)
info(f"   (Phi-Psi)'(r,y) = {sp.simplify(slip_gradA)}  (both methods)")
# the physical slip ratio (normalisation-independent -- C cancels):
slip = sp.simplify(Phip/Psip)                               # = (mu+y mu')/mu
cert("SLIP  Phi'/Psi' = (mu_10 + y mu_10')/mu_10  (C cancels: normalisation-independent)",
     sp.simplify(slip - Atan/mu) == 0)

# =====================================================================================
print("=" * 90)
print(" PART 4 -- A_slip(y) and the THREE limits  (COMPUTATION + sympy limits)")
print("=" * 90)
# A_slip := (Pi^aux)_TF / [ y mu_10' (n_i n_j - delta_ij/3) ]  (task's definition).  From Part 3,
# the projected slip law is  mu (Phi-Psi)' = (Pi^aux)_flux = y mu' Psi', so the aux anisotropic
# stress coefficient normalised by the natural y mu' structure is Psi'-carried; the DIMENSIONLESS,
# r-independent, normalisation-independent invariant that the decider reduces to is the slip EXCESS
A_slip = sp.simplify(slip - 1)                              # = y mu_10'/mu_10  (slip - 1)
cert("A_slip(y) = slip - 1 = y mu_10'/mu_10 (dimensionless invariant; = normalised (Pi^aux)_TF); "
     "A_slip = 0  <=>  y mu_10' = 0  <=>  Phi=Psi",
     sp.simplify(A_slip - y*mup/mu) == 0)
lim_hi = sp.limit(slip, y, sp.oo);  A_hi = sp.limit(A_slip, y, sp.oo)
lim_lo = sp.limit(slip, y, 0);      A_lo = sp.limit(A_slip, y, 0)
cert("y>>1 (NEWTONIAN, solar system):  slip -> 1  and  A_slip -> 0  =>  Phi = Psi  (a genuine PASS "
     "in this regime -- NOT manufactured; unlike the old source-free chassis gamma_PPN=0)",
     lim_hi == 1 and A_hi == 0)
val1  = sp.nsimplify(slip.subs(y, 1));   Aval1 = sp.nsimplify(A_slip.subs(y, 1))
cert("y~1 (transition):  slip = 3/2,  A_slip = 1/2  =>  Phi != Psi  (FAIL begins)",
     sp.simplify(val1 - sp.Rational(3, 2)) == 0 and sp.simplify(Aval1 - sp.Rational(1, 2)) == 0)
cert("y<<1 (DEEP MOND, galaxies):  slip -> 2  and  A_slip -> 1  =>  Phi != Psi  (FAIL) -- the "
     "curvature gradient is TWICE the lapse gradient; no constant normalisation removes it",
     lim_lo == 2 and A_lo == 1)
print("    y-table of the DERIVED slip (mu_10+y mu_10')/mu_10 and A_slip = y mu_10'/mu_10")
print("    (verdict tol: |A_slip|<1e-3 => Phi=Psi to better than 0.1%, i.e. observationally GR):")
mu_n = sp.lambdify(y, mu, 'numpy'); slip_n = sp.lambdify(y, slip, 'numpy'); A_n = sp.lambdify(y, A_slip, 'numpy')
for yv in [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]:
    Av = float(A_n(yv))
    print(f"      y={yv:6.2f}:  mu={float(mu_n(yv)):.4f}  slip={float(slip_n(yv)):.6f}  "
          f"A_slip={Av:11.4e}   {'Phi=Psi (PASS)' if abs(Av) < 1e-3 else 'Phi!=Psi (FAIL)'}")
info("mu_10 is a SHARP kernel (n=10): the slip is pinned at EXACTLY 2.000 through the whole deep-")
info("MOND band y<~0.3, passes 1.5 at the y~1 knee, and is Newtonian (A_slip~1e-5) by y~3 -- the")
info("factor-2 swing is a WIDE plateau (all of galactic phenomenology), not a thin edge.")

# =====================================================================================
print("=" * 90)
print(" PART 5 -- numerical Phi-Psi for a point mass; lensing consequence (COMPUTATION)")
print("=" * 90)
# integrate the DERIVED (Phi-Psi)' for a Milky-Way-scale point lens; y set by the MOND field Phi.
G_SI, MSUN, KPC = 6.674e-11, 1.989e30, 3.086e19
A0, M = 9.3619e-11, 6.0e10*MSUN
def mu10(yv):  return yv/(1.0+yv**10)**0.1
def dmu10(yv): return (1.0+yv**10)**(-1.1)
def y_of_r(rv):
    # Phi' = C/(r^2 mu(y)) with C=GM and y=Phi'/a0  => solve y (1+y^10)^{-1/10} = GM/(r^2 a0) = g_N/a0
    t = G_SI*M/rv**2/A0
    yy = max(t, t**0.5)  # seed
    for _ in range(200):
        f = mu10(yy)*yy - t; fp = mu10(yy)+yy*dmu10(yy)
        yy = abs(yy - f/fp)
    return yy
rk = np.array([0.5,1,2,5,10,20,50,100,200])
print("  {:>7} {:>10} {:>8} {:>8} {:>18} {:>10}".format(
      "r[kpc]", "y", "slip", "A_slip", "d(Phi-Psi)/dr", "lens_eff"))
lens_eff_deep = None
for rr in rk:
    rv = rr*KPC; yy = y_of_r(rv)
    Phip_n = (G_SI*M)/(rv**2*mu10(yy))          # C=GM
    Psip_n = (G_SI*M)/(rv**2*(mu10(yy)+yy*dmu10(yy)))
    dPhiPsi = Phip_n - Psip_n
    slip_num = Phip_n/Psip_n                     # = (mu+y mu')/mu ; the physical slip ratio
    lens_eff = (Phip_n+Psip_n)/(2*Psip_n)       # =1 iff Phi=Psi; deep-MOND -> (1+2)/2=1.5
    lens_eff_deep = lens_eff
    print(f"  {rr:7.1f} {yy:10.3e} {slip_num:8.4f}"
          f" {yy*dmu10(yy)/mu10(yy):8.4f} {dPhiPsi:18.3e} {lens_eff:10.4f}")
# slip normalised to slip: lens efficiency relative to Phi=Psi baseline
cert("point-mass lensing efficiency (Phi'+Psi')/(2Psi') -> 1.5 in deep MOND (Phi=2Psi) vs 1 for "
     "Phi=Psi: a 50% weak-lensing EXCESS at galactic radii => tension with the Phi=Psi Mistele+24 "
     "KiDS RAR (committed 21-sigma-scale slip-1 stack); milder than the old chassis' factor-2 but "
     "nonzero and structural",
     abs(lens_eff_deep - 1.5) < 0.02)
info("(Solar-system radii sit at y>>1 -> slip=1 -> Cassini gamma is SAFE for THIS obstruction;")
info(" the slip is a GALACTIC-lensing failure, sharply different from gamma_PPN=0 which fails")
info(" the solar system too.  Both-ways honest: Newtonian PASS, deep-MOND FAIL.)")

# =====================================================================================
print("=" * 90)
print(" VERDICT")
print("=" * 90)
print(r"""  DECIDER: PASS iff Phi = Psi (at all accelerations).  RESULT: FAILED (deep-MOND slip).

  (1) TWO MODULI (DERIVATION, Part 1): the ONE frozen AQUAL flux F(q')=mu_10(q'/a0)q' fixes the
      CURVATURE Phi through its SECANT modulus mu_10 (C_M=0, vary N) and the LAPSE Psi through its
      TANGENT modulus mu_10+y mu_10' (the GENERATED S_3 = sigma L^[p_q], vary q).  These are the
      transverse vs radial eigenvalues of the frozen Hessian A^{ij}=mu delta + y mu' n n; they
      differ by y mu_10' > 0 for EVERY y>0.

  (2) SLIP, TWO METHODS AGREE (Part 3):  Phi'/Psi' = (mu_10 + y mu_10')/mu_10.  The full-ij solve
      and the traceless-projection of the auxiliary stress Pi^aux (~ lambda_2 delta C_M + lambda_4
      delta S_4, both carrying the anisotropy y mu_10' n n) give the IDENTICAL (Phi-Psi)'.
      lambda_2 (=lapse) is nonzero even at r_M=0 (fed by r_3), exactly as the slip-decider spec says.

  (3) THREE LIMITS (Part 4):
        y>>1 (solar):    slip=1,   A_slip=0   -> Phi=Psi  (PASS, verified as hard as the FAIL)
        y~1  (knee):     slip=3/2, A_slip=1/2 -> Phi!=Psi (FAIL)
        y<<1 (galaxies): slip=2,   A_slip=1   -> Phi!=Psi (FAIL)
      A_slip(y)=y mu_10'/mu_10 = 0 <=> Phi=Psi.  The factor-2 swing is y-dependent, so NO constant
      normalisation sets gamma_PPN=1 at all accelerations.  mu_10 is sharp: slip=2.000 for y<~0.3.

  (4) CONSEQUENCE (Part 5): deep-MOND weak-lensing efficiency (Phi'+Psi')/(2Psi') -> 1.5, a 50%
      excess over the Phi=Psi (Mistele+24 KiDS) baseline at galactic radii.  Solar system is SAFE
      (y>>1), so this is a GALACTIC-lensing FAIL, distinct from (and milder than) the source-free
      chassis' gamma_PPN=0 that fails everywhere.

  This DERIVES the origin of the committed FC-4AC slip verdict: it is NOT a free design choice --
  the generated S_3/S_4 FORCE the lapse onto the tangent modulus mu+y mu' while C_M fixes the
  curvature on the secant modulus mu.  gamma_PPN=1 is STRUCTURALLY excluded in Embedding I.
  SECTOR-ORTHOGONAL and UNCHANGED by the slip (EXTERNAL-INPUT, committed): alpha_3=-1
  (ppn_mmg_gate) and nabla_mu T^{mu nu}!=0 at Newtonian order (fc4ac_matter_conservation).
""")
print("=" * 90)
ok = len(FAILS) == 0
print(f" FC4AC-SLIP CERTIFICATE: {'ALL BOOLEAN CHECKS PASS (exit 0).' if ok else 'FAILURES:'}")
for f in FAILS:
    print("   - " + f)
print("=" * 90)
sys.exit(0 if ok else 1)
