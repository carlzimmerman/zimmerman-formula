#!/usr/bin/env python3
r"""THE UNIFYING THEOREM: why all six architectures died, via Hojman-Kuchar-Teitelboim.
And the exact minimal sacrifice that opens a viable theory."""
import sympy as sp
P=print
P("="*80); P("HKT UNIQUENESS AND THE MOND WALL"); P("="*80)
P(r"""
HOJMAN-KUCHAR-TEITELBOIM (1976). If the Hamiltonian constraint H_perp
  (a) closes the Dirac algebra  {H_perp(x),H_perp(y)} = H^i(x) d_i delta - (x<->y),
  (b) is ULTRALOCAL in h_ij (no spatial derivatives of momenta), and
  (c) is at most quadratic in momenta,
then H_perp IS the GR Hamiltonian constraint, uniquely (up to G, Lambda).

COROLLARY (the MOND wall). Exact MOND requires a nonlinear mu(|DPsi|/a0) in the static
constraint => H_perp must be DEFORMED. By HKT, any deformation must break (a), (b), or (c).
Every architecture we tested breaks exactly one -- and the observable that fails is
DETERMINED by which one:""")

rows=[("(a) algebra closure","MMG: replace H_perp by C_M => (pi_N,C_M) 2nd class, refoliation lost",
       "gamma_PPN = 0 (no spatial potential); alpha_3 = -1/-3",
       "audit 8c53d66a, repair 2542182b"),
      ("(a) closure, variant","MMG_REPAIR_A: S2'=D^2(q+lnN) restores Phi=Psi",
       "gamma=1 OK but alpha_3=-3, deep-MOND source sign flips (BTFR dies)","2542182b"),
      ("(b) ultralocality","CGD nonlocal: E_i = D_i Delta^-1 (3)R",
       "(3)R^(1)|_TT = 0 => no tensor gradient => c_T = 0","6f603c50"),
      ("(b) ultralocality","DW nonlocal: U = Box_ret^-1(R_uu)",
       "localization ghost 2T+2S; Cassini Q2 10-14 sigma","DOI 22132648"),
      ("(c) momentum structure","F(A^2) kinetic carrier: nonlinear in lapse-acceleration",
       "khronon scalar propagates (2+1), Z_perp=2(1-mu)>0","sf40/sf41"),
      ("source routing","YCG: MOND on conformal q",
       "sourced by T^i_i ~ rho v^2/c^2 ~ 5e-7 rho => MOND inert","5b7efd3d"),
      ("source routing","CMYG: composite metric g~=e^{2aq}g",
       "conformal => light blind to q (no lensing); disformal => cone split","this run")]
P(f"\n  {'BREAKS':<22}{'ARCHITECTURE':<44}{'FAILS AS'}")
for br,arch,fail,ev in rows: P(f"  {br:<22}{arch[:42]:<44}{fail}")

P("\n"+"="*80); P("THE THEOREM"); P("="*80)
P(r"""
  Exact MOND + minimal coupling + 2 tensor DOF + gamma_PPN=1 + c_T=1 is OVERDETERMINED.
  HKT says GR is the unique solution of (a)+(b)+(c); MOND requires leaving that point; and
  each exit door has now been walked and lands on a specific, measured contradiction.

  This is not "MOND is impossible" -- it is: NO 2-DOF LOCAL DEFORMATION OF H_perp DELIVERS
  MOND WITH GR'S LENSING. The wall is HKT, not any one construction.""")

P("\n"+"="*80); P("THE MINIMAL SACRIFICE (what one shot at PASS actually costs)"); P("="*80)
P(r"""
  Four requirements can each be dropped. Cost of each, priced from committed evidence:

  1. DROP "2 DOF" -> accept 2+1 with a SCREENED scalar (k-mouflage/Vainshtein).
     Every gate above becomes passable: gamma_PPN=1 (scalar screened in solar system),
     lensing OK (scalar couples conformally to BOTH potentials via a single Phi=Psi source),
     c_T=1 (scalar doesn't touch TT), exact mu retained.
     COST: a third propagating DOF. This is AeST/TeVeS/RelMOND territory (AeST = 6 DOF).
     STATUS in repo: Vainshtein/k-mouflage listed as "never tried, ranked #4" (RESUME_HERE).
     >>> THIS IS THE ONLY DOOR WITH NO COMMITTED KILL. <<<

  2. DROP "minimal coupling" -> forbidden by spec (and by honesty: it is fitting, not deriving).
  3. DROP "exact mu=1-e^{-y}" -> mu_n clears Cassini but does NOT repair gamma_PPN/alpha_3.
  4. DROP "gamma_PPN=1 / lensing" -> the theory stops describing the universe.

  VERDICT ON THE ONE SHOT: within {2 DOF, local, minimal coupling, exact MOND, GR lensing}
  there is NO PASS -- that set is closed by HKT plus six committed kills. The honest
  best-shot theory is 2+1 with a screened scalar, which is a DIFFERENT (and already-populated)
  class, and whose open gate is whether screening can be made compatible with the
  wide-binary/EFE data the DR4 registration will test.""")
P("="*80); P("FRIED CHICKEN: not on this menu. The kitchen is closed by HKT.")
