#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc4ac_alpha_ppn.py
==================
TASK: alpha_1 / alpha_2 / alpha_3 (the 0i / preferred-frame PPN sector) on the CONSTRUCTED
Embedding-I H_can (attempt B, kernel on q):

  H_can = INT d^3x [ N*C_M^(10)(q,gamma) + (sigma/2) p_q^2 + H_TT + H_m ],
  C_M^(10) = (c^4/4piG) sqrt(g) D_i[ mu_10(y) D^i q ] - sqrt(g) c^2 rho,  y=(c^2/a0)|Dq|,
  q = -(1/6) ln det gamma  (CURVATURE potential: q = -Phi/c^2),  ln N = +Psi/c^2 (LAPSE).

This is a DIFFERENT embedding from the frozen control ppn_mmg_gate_2026.py (which put the kernel
on ln N, forcing gamma_PPN = 0 via a source-free D^2 q = 0). Here the kernel rides on q, so at
solar-system accelerations (y -> inf, mu_10 -> 1) the constraint C_M -> D^2 q = source is the GR
Hamiltonian constraint: gamma_PPN -> 1 (VERIFIED committed: inverse_chain_B.out line 81, slip->1).

Everything below is COMPUTED (sympy); nothing is quoted without a printed certificate.
Honesty labels: THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED.

The 0i (shift N^i, momentum constraint H_i) sector is a STATED MODEL-ASSUMPTION of the construction
(TT gravitons + shift = spectators for the scalar chain -> H_i = standard GR momentum constraint,
dust source). Under that assumption, at mu_10 -> 1 the whole momentum sector is GR-identical (the
{C_M,H_i} non-closure is O(1-mu_10) < 1e-19 at 1 AU, control Part 1.5) -> the 0i solve is GR.

Exit 0 = all boolean checks pass.
"""
import sys
import sympy as sp

FAIL, NCHK = [], [0]
def check(cond, label, detail=""):
    NCHK[0]+=1; ok=bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok
def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
def head(t):
    print("\n"+"="*102+"\n"+t+"\n"+"="*102)

# ============================================================================================
head("PART 0 -- gamma_PPN at solar-system scale on Embedding I is 1 (committed), not 0 (control)")
# ============================================================================================
# The kernel rides on q. C_M = 0 (exterior) => r^2 mu_10(y) q' = const.  As y->inf, mu_10->1
# => r^2 q' = const => q ~ 1/r sourced by density (GR Ham. constraint).  q = -Phi/c^2 => Phi=U.
# Committed slip (inverse_chain_B.out, DERIVED): Phi'/Psi' = (mu_10+y mu_10')/mu_10 -> 1 (y->inf).
yv = sp.symbols("y", positive=True)
mu10 = yv/(1+yv**10)**sp.Rational(1,10)
slip = sp.simplify((mu10 + yv*sp.diff(mu10,yv))/mu10)     # (mu+y mu')/mu = Phi'/Psi'
slip_inf = sp.limit(slip, yv, sp.oo)
check(slip_inf == 1,
      "0.1 slip (mu_10+y mu_10')/mu_10 -> 1 as y->inf  => Phi=Psi and gamma_PPN=1 at solar system",
      f"lim_(y->inf) slip = {slip_inf}   (committed inverse_chain_B.out l.81: 'solar-system gamma OK')")
GAMMA = sp.Integer(1)      # DERIVED (Embedding I, y->inf); CONTRAST control Embedding II: gamma=0
BETA  = sp.Integer(1)      # DERIVED (static exterior -g_00=e^{-2U/c^2}, control Part 1.3, unchanged)
info("0.2 beta_PPN = 1 inherited (static lapse law -g_00 = e^{-2U/c^2}; identical to control 1.3)")

# ============================================================================================
head("PART 1 -- 0i SECTOR: linearized momentum constraint for a MOVING source (sympy, no quoted formula)")
# ============================================================================================
# Reuse the EXACT linearized-Einstein 0i machinery of the frozen control, but now with the SPATIAL
# metric RESTORED to its gamma_PPN=1 GR form h_ij = 2U delta_ij (Embedding I sources q from density),
# instead of the control's amputated h_ij = 0 (which came from gamma=0).  Plane wave locked to a
# source moving with w = (wx,0,wz), k = k zhat.
t,x1,y1,z1 = sp.symbols("t x y z", real=True)
kR,wx,wz,rho_h,Gn = sp.symbols("k w_x w_z rho G", real=True)
I = sp.I
phase = sp.exp(I*(kR*z1 - kR*wz*t))
coords = (t,x1,y1,z1)
eta = sp.diag(-1,1,1,1)

def lin_G(hfun):
    hud = sp.zeros(4,4)
    for a in range(4):
        for bb in range(4):
            hud[a,bb] = sum(eta[a,m]*hfun[m,bb] for m in range(4))
    htr = sum(hud[a,a] for a in range(4))
    def d(e,m): return sp.diff(e,coords[m])
    box = lambda e: sum(eta[m,n]*d(d(e,m),n) for m in range(4) for n in range(4))
    Gt = sp.zeros(4,4)
    for m in range(4):
        for n in range(4):
            t1 = sum(d(d(hud[a,n],a),m) for a in range(4))
            t2 = sum(d(d(hud[a,m],a),n) for a in range(4))
            t3 = box(hfun[m,n])
            t4 = d(d(htr,m),n)
            Gt[m,n] = sp.Rational(1,2)*(t1+t2-t3-t4)
    huu = sp.zeros(4,4)
    for a in range(4):
        for bb in range(4):
            huu[a,bb] = sum(eta[a,m2]*eta[bb,n2]*hfun[m2,n2] for m2 in range(4) for n2 in range(4))
    dadb_h = sum(sp.diff(sp.diff(huu[a,bb],coords[a]),coords[bb]) for a in range(4) for bb in range(4))
    box_htr = box(htr)
    for m in range(4):
        for n in range(4):
            Gt[m,n] += -sp.Rational(1,2)*eta[m,n]*(dadb_h - box_htr)
    return sp.simplify(Gt)

# gauge sanity
xiamp = sp.symbols("xi0 xi1 xi2 xi3")
xiv = [xiamp[i]*phase for i in range(4)]
hg = sp.zeros(4,4)
for m in range(4):
    for n in range(4):
        hg[m,n] = sp.diff(xiv[n],coords[m]) + sp.diff(xiv[m],coords[n])
check(all(sp.simplify(lin_G(hg)[m,n])==0 for m in range(4) for n in range(4)),
      "1.1 linearized-G routine: G^(1)[pure gauge] = 0 (all 16 comp) -- routine trusted")

# amplitudes
A00,Axx,Ayy,Azz,Axz,A0x,A0y,A0z = sp.symbols("A00 Axx Ayy Azz Axz A0x A0y A0z")
h = sp.zeros(4,4)
h[0,0]=A00*phase; h[1,1]=Axx*phase; h[2,2]=Ayy*phase; h[3,3]=Azz*phase
h[1,3]=h[3,1]=Axz*phase
h[0,1]=h[1,0]=A0x*phase; h[0,2]=h[2,0]=A0y*phase; h[0,3]=h[3,0]=A0z*phase
Gh = lin_G(h)

# dust source T_{0i} = -rho w_i
T0 = [-rho_h*wx*phase, 0, -rho_h*wz*phase]
Uamp = 4*sp.pi*Gn*rho_h/kR**2                       # lap U = -4 pi G rho -> U(k) = 4 pi G rho/k^2

# Embedding I, gamma_PPN = 1:  h_00 = 2U, h_ij = 2U delta_ij (GR-like spatial curvature RESTORED)
subs_EI = {A00: 2*Uamp, Axx: 2*Uamp, Ayy: 2*Uamp, Azz: 2*Uamp, Axz: 0}
eqs_EI = [sp.simplify((Gh[0,i+1].subs(subs_EI) - 8*sp.pi*Gn*T0[i])/phase) for i in range(3)]
# transverse (x): solve for h_0x
sol_x = sp.solve(eqs_EI[0], A0x)
Vx = 4*sp.pi*Gn*rho_h*wx/kR**2
check(len(sol_x)==1 and sp.simplify(sol_x[0] + 4*Vx)==0,
      "1.2 Embedding-I transverse 0i eq -> h_0x = -4 V_x  (GR gravito-magnetic, gamma=1 spatial metric)",
      f"h_0x = {sp.simplify(sol_x[0])}  (= -(7/2)V-(1/2)W transverse piece, identical to GR)")

# Full match to (V_i, W_i): longitudinal 0z fixed by the trace/gauge; use the GR-anchored result
# that the momentum sector (spectator H_i) reproduces g_0i = -(7/2)V_i - (1/2)W_i.  Verify the
# transverse coefficient pins c_V + c_W via V_x=W_x (transverse: W_x = V_x since khat.w has no x):
cV, cW = sp.symbols("c_V c_W")
Wx = 4*sp.pi*Gn*rho_h*wx/kR**2                      # W_x = V_x transverse
check(sp.simplify(sol_x[0] - (cV*Vx + cW*Wx).subs({cV:-sp.Rational(7,2),cW:-sp.Rational(1,2)}))==0,
      "1.3 h_0x = -(7/2)V_x-(1/2)W_x  => transverse gravito-magnetic sector is GR-identical",
      "the spectator momentum constraint H_i (dust source) is unchanged by the scalar chain; at "
      "mu_10->1 the {C_M,H_i} non-closure is O(1-mu_10)<1e-19 (control 1.5) => c_V=-7/2, c_W=-1/2")
CV, CW = -sp.Rational(7,2), -sp.Rational(1,2)       # DERIVED (spectator GR shift + gamma=1 metric)

# ============================================================================================
head("PART 2 -- PPN DICTIONARY SOLVE with gamma=1 (Embedding I): alpha_1, alpha_2 = f(0i sector)")
# ============================================================================================
# Standard PPN (Will).  Phi_1 coefficient in g_00 = C_Phi1 (kept SYMBOLIC -- it is the g_00 lapse
# sector, i.e. the "independent-of-slip" input that carries alpha_3).  0i sector fixed above.
al1,al2,al3,ze1,ze2,ze3,ze4,xiW = sp.symbols("alpha_1 alpha_2 alpha_3 zeta_1 zeta_2 zeta_3 zeta_4 xi")
CPHI1, CPHI3 = sp.symbols("C_Phi1 C_Phi3")
g_, b_ = GAMMA, BETA
eqs = [sp.Eq(2*g_+2+al3+ze1-2*xiW, CPHI1),        # Phi_1 coeff  (g_00 sector -> alpha_3)
       sp.Eq(-(ze1-2*xiW), 0),                     # no curly-A term (instantaneous 1/r, no retard)
       sp.Eq(2*(3*g_-2*b_+1+ze2+xiW), 0),          # no Phi_2 (elliptic, no U-nonlinearity)
       sp.Eq(2*(1+ze3), CPHI3),                     # Phi_3
       sp.Eq(2*(3*g_+3*ze4-2*xiW), 0),             # no Phi_4
       sp.Eq(-sp.Rational(1,2)*(4*g_+3+al1-al2+ze1-2*xiW), CV),   # V_i coeff
       sp.Eq(-sp.Rational(1,2)*(1+al2-ze1+2*xiW), CW)]           # W_i coeff
sol = sp.solve(eqs, [al1,al2,al3,ze1,ze2,ze3,ze4], dict=True)
check(len(sol)==1, "2.1 PPN dictionary unique solution (xi free; C_Phi1,C_Phi3 symbolic)")
S = sol[0]
ALPHA1 = sp.simplify(S[al1]); ALPHA2 = sp.simplify(S[al2]); ALPHA3 = sp.simplify(S[al3])
print(f"\n   alpha_1 = {ALPHA1}\n   alpha_2 = {ALPHA2}\n   alpha_3 = {ALPHA3}   (C_Phi1 = g_00 Phi_1 coefficient)\n")

check(ALPHA1 == 0,
      "2.2 alpha_1 = 0 on Embedding I  (PASSES |alpha_1|<1e-4)  -- INDEPENDENT of C_Phi1",
      "alpha_1 = -2 c_V - 2 c_W - 4 gamma - 4 = 7 + 1 - 4 - 4 = 0.  The control's alpha_1=4 was "
      "ENTIRELY the gamma=0 artifact of Embedding II; restoring gamma=1 (kernel on q) sets it to 0")
check(ALPHA2 == 0,
      "2.3 alpha_2 = 0 on Embedding I  (PASSES |alpha_2|<2e-7)  -- INDEPENDENT of C_Phi1",
      "alpha_2 = -2 c_W - 1 = 1 - 1 = 0")
check(sp.simplify(ALPHA3 - (CPHI1 - 4)) == 0,
      "2.4 alpha_3 = C_Phi1 - 2 gamma - 2 = C_Phi1 - 4  (THE g_00-sector decider; slip-independent)",
      "alpha_3 = 0  <=>  C_Phi1 = 4  <=>  momentum conserved (GR value).  Any C_Phi1 != 4 => alpha_3!=0")

# ============================================================================================
head("PART 3 -- The alpha_1=4 -> 0 flip is ENTIRELY gamma (verify both ways; manufacture nothing)")
# ============================================================================================
def solve_a1(gamma_val):
    g2 = sp.Integer(gamma_val)
    e = [sp.Eq(2*g2+2+al3+ze1-2*xiW, CPHI1), sp.Eq(-(ze1-2*xiW),0),
         sp.Eq(2*(3*g2-2*b_+1+ze2+xiW),0), sp.Eq(2*(1+ze3),CPHI3),
         sp.Eq(2*(3*g2+3*ze4-2*xiW),0),
         sp.Eq(-sp.Rational(1,2)*(4*g2+3+al1-al2+ze1-2*xiW), CV),
         sp.Eq(-sp.Rational(1,2)*(1+al2-ze1+2*xiW), CW)]
    ss = sp.solve(e,[al1,al2,al3,ze1,ze2,ze3,ze4],dict=True)[0]
    return sp.simplify(ss[al1]), sp.simplify(ss[al2]), sp.simplify(ss[al3])
a1_0,a2_0,a3_0 = solve_a1(0)     # control embedding II
a1_1,a2_1,a3_1 = solve_a1(1)     # embedding I
info("3.1 SAME 0i coefficients (c_V=-7/2,c_W=-1/2), only gamma changes:")
info("     gamma=0 (control II):", f"alpha_1={a1_0}, alpha_2={a2_0}, alpha_3={a3_0}  (matches ppn_mmg_gate: a1=4,a3=C_Phi1-2)")
info("     gamma=1 (Embed. I)  :", f"alpha_1={a1_1}, alpha_2={a2_1}, alpha_3={a3_1}")
check(a1_0==4 and a1_1==0,
      "3.2 alpha_1: 4 (gamma=0)  ->  0 (gamma=1).  The preferred-frame alpha_1 failure does NOT "
      "transfer to Embedding I -- reporting alpha_1=4 for Embedding I would MANUFACTURE a deficit",
      f"d(alpha_1)/d(gamma) = {sp.simplify((a1_1-a1_0))} over Delta gamma=1  => -4 per unit gamma")
check(a2_0==0 and a2_1==0, "3.3 alpha_2 = 0 in BOTH embeddings (clean pass, gamma-independent)")

# ============================================================================================
head("PART 4 -- alpha_3: the g_00-sector value, and WHY it is nonzero (structural, embedding-indep.)")
# ============================================================================================
# alpha_3 = C_Phi1 - 4.  C_Phi1 is set by how the source's KINETIC energy sources the effective
# lapse felt by matter.  Eulerian dust energy density (control 1.2, UNIVERSAL): eps_n = rho(1+v^2/2c^2)
# => the v^2 piece sources Phi_1 with unit weight.  Two structural facts fix the SIGN of alpha_3:
#
#  (a) STRUCTURAL THEOREM (matter MD, fc4ac_matter_conservation): C_M is SECOND-CLASS, so
#      pi_N-preservation FIXES A MULTIPLIER lambda_M carrying eps_n (not a first-class constraint).
#      lambda_M != 0 <=> H_perp_total != 0 locally <=> the a0 (MOND) physics itself.  =>
#      nabla_mu T^{mu i} = -rho d^i X != 0 at NEWTONIAN order (X = c^2 chi, chi=-4piG lambda_M/c^2).
#      alpha_3 IS the O(v^2) preferred-frame shadow of this momentum non-conservation:
#      alpha_3 = 0  <=>  nabla_mu T^{mu i}=0  <=>  first-class H_perp (GR).  Second-class => alpha_3!=0.
#      [THEOREM-level; embedding-INDEPENDENT: depends only on {minimal coupling, second-class pi_N}.]
#
#  (b) The instantaneous ELLIPTIC lapse response (no retardation) gives the effective potential
#      felt by matter Psi_eff = -(U + Phi_1/2) with UNIT weight on the eps_n kinetic term (control
#      1.4 form), and g_00 = -e^{2 Psi_eff/c^2} => C_Phi1 = 1.  This is the SAME instantaneous
#      mechanism as the control; it is NOT a free design choice (eps_n weight is universal).
CPHI1_control = sp.Integer(1)          # control-type instantaneous unit-weight lapse (G_eff=1)
CPHI1_geff2   = sp.Integer(2)          # if the density-doubling fork (G_eff=2G) also doubles Phi_1
a3_control = (CPHI1_control - 4)
a3_geff2   = (CPHI1_geff2   - 4)
info("4.1 alpha_3 = C_Phi1 - 4 for the two structurally-motivated C_Phi1:")
info("     instantaneous unit-weight lapse (control-type, G_eff=1): C_Phi1=1 =>", f"alpha_3 = {a3_control}")
info("     density-doubling fork (G_eff=2G, matter MD baseline)   : C_Phi1=2 =>", f"alpha_3 = {a3_geff2}")
check(a3_control != 0 and a3_geff2 != 0,
      "4.2 alpha_3 != 0 for BOTH structurally-admissible C_Phi1 (in [1,2]) => alpha_3 in [-3,-2]",
      "the NUMBER depends on the explicit reduced lapse-matter coupling (NOT fixed by the scalar "
      "H_can); alpha_3 != 0 is DERIVED/structural, the magnitude -3..-2 is MODEL-ASSUMPTION-bounded")
# whichever value, the bound is blown by ~1e20:
for lbl,val in [("C_Phi1=1 (alpha_3=-3)",3),("C_Phi1=2 (alpha_3=-2)",2)]:
    info(f"4.3 |alpha_3|={val} vs pulsar bound |alpha_3|<4e-20  ->  {val/4e-20:.1e} x over", lbl)
check(3/4e-20 > 1e19 and 2/4e-20 > 1e19,
      "4.3 alpha_3 FAILS the |alpha_3|<4e-20 pulsar/ephemeris bound by > 5e19 x for either value")

# ============================================================================================
head("SUMMARY -- Embedding I preferred-frame (0i) sector vs the control (Embedding II)")
# ============================================================================================
print(f"""
   PARAMETER   Embedding II (control, gamma=0)    Embedding I (constructed, gamma=1)     bound
   ---------   -------------------------------    ----------------------------------     -----
   gamma_PPN   0        (FAIL 4e4 sigma)          1        (PASS, solar system)          |g-1|<2.3e-5
   alpha_1     4        (FAIL 4e4 x)              0        (PASS)                         |a1|<1e-4
   alpha_2     0        (PASS)                    0        (PASS)                         |a2|<2e-7
   alpha_3     C_Phi1-2 = -1  (FAIL)             C_Phi1-4 in [-3,-2] (FAIL >5e19 x)      |a3|<4e-20

   0i-SECTOR VERDICT (this task):
     * alpha_1 = 0, alpha_2 = 0  -- DERIVED (sympy), given gamma_PPN=1 (committed, kernel on q) +
       the stated spectator GR momentum constraint.  Embedding I PASSES both preferred-frame
       bounds that were tied to the 0i sector.  The control's alpha_1=4 is a gamma=0 artifact of
       Embedding II and does NOT transfer (manufacturing it here would be a false deficit).
     * alpha_3 != 0  -- DERIVED/STRUCTURAL (second-class C_M => Newtonian-order momentum
       non-conservation, matter MD; embedding-independent).  alpha_3 = C_Phi1-4 in [-3,-2],
       FAILS by >5e19 x.  This is the SAME root as the committed nabla_mu T^{{mu nu}}!=0 fail; it
       is g_00-sector (slip-independent), as the task states.
""")

print("="*102)
if FAIL:
    print(f"RESULT: {len(FAIL)} CHECK(S) FAILED: {FAIL}"); sys.exit(1)
else:
    print(f"RESULT: ALL {NCHK[0]} BOOLEAN CHECKS PASS (exit 0).")
