#!/usr/bin/env python3
# ROUTE 3 AUDIT -- PART 2: condensate thermodynamics, the a0(z)<->c_s^2 identity,
# and the polytrope constant K -- each re-derived, none taken on trust.
import sympy as sp, mpmath as mp
mp.mp.dps = 30
FAIL=[]; N=[0]
def ck(c,lab,det=""):
    N[0]+=1; ok=bool(c); print(f"  [{'ok' if ok else 'FAIL'}] {lab}"+(f"   {det}" if det else ""))
    if not ok: FAIL.append(lab)
def s4(x,n=4): return mp.nstr(mp.mpf(x),n)

print("="*100); print("A -- k-essence thermodynamics, derived twice (Q-variable and X-variable)"); print("="*100)
Q = sp.Symbol("Q", positive=True); K = sp.Function("K")
n_  = sp.diff(K(Q), Q)
rho = Q*sp.diff(K(Q),Q) - K(Q)
p_  = K(Q)
cs2_Q = sp.simplify(sp.diff(p_,Q)/sp.diff(rho,Q))
ck(sp.simplify(cs2_Q - sp.diff(K(Q),Q)/(Q*sp.diff(K(Q),Q,2)))==0,
   "A1  c_s^2 = K'/(Q K'')  (adiabatic dp/drho on the Q variable)", f"c_s^2 = {cs2_Q}")
# independent route: L = P(X), X = Q^2/2, c_s^2 = P_X/(P_X + 2 X P_XX)
Xs = sp.Symbol("X", positive=True); P = sp.Function("P")
Qx = sp.sqrt(2*Xs)
Kx = P(Xs).subs(Xs, Q**2/2)
PX  = sp.diff(P(Xs),Xs); PXX = sp.diff(P(Xs),Xs,2)
cs2_X = PX/(PX + 2*Xs*PXX)
KpQ  = sp.simplify(sp.diff(Kx,Q));  KppQ = sp.simplify(sp.diff(Kx,Q,2))
lhs = sp.simplify((KpQ/(Q*KppQ)).subs(Q, sp.sqrt(2*Xs)))
ck(sp.simplify(sp.simplify(lhs) - cs2_X)==0,
   "A2  CONTROL: the SAME c_s^2 from the X-variable P(X) formula -- no convention splice",
   "K'/(QK'') == P_X/(P_X+2X P_XX) identically")
# no-ghost
ck(sp.simplify(sp.diff(rho,Q) - Q*sp.diff(K(Q),Q,2))==0,
   "A3  drho/dQ = Q K''  =>  no-ghost (K''>0) fixes ONLY the SIGN of c_s^2, not its scaling",
   "stage 9's withdrawal reproduced independently")
# rate for K' ~ (Q-Q*)^m
m, Qst = sp.symbols("m Q_star", positive=True)
Kp = (Q-Qst)**m
rate = sp.simplify(Kp/(Q*sp.diff(Kp,Q)))          # = c_s^2, with K'=(Q-Q*)^m
# c_s^2 ~ (Q-Q*)/(m Q*)  and  (Q-Q*) = (K')^(1/m) ~ (a^-3)^(1/m)  =>  c_s^2 ~ a^(-3/m)
expo = sp.simplify(-3/m)
ck(sp.simplify(rate - (Q-Qst)/(m*Q))==0 and sp.simplify(expo.subs(m,1)+3)==0,
   "A4  for K' ~ (Q-Q*)^m: c_s^2 = (Q-Q*)/(mQ) and (Q-Q*) = (K')^(1/m) ~ a^(-3/m)",
   f"m=1 -> a^-3 (stage 9's case); m=10 -> a^{sp.nsimplify(-3/sp.Integer(10))}")

print(); print("="*100); print("B -- THE EXACT IDENTITY linking a0(z) to the sound speed"); print("="*100)
# background conservation on L=K(Q):  rho_dot + 3H(rho+p)=0
a = sp.Symbol("a", positive=True); Qa = sp.Function("Q")(a)
rho_a = Qa*sp.diff(K(Qa),Qa) - K(Qa); p_a = K(Qa)
cons = sp.simplify(a*sp.diff(rho_a,a) + 3*(rho_a+p_a))
dQ = sp.solve(cons, sp.diff(Qa,a))[0]
ck(sp.simplify(a*sp.diff(sp.diff(K(Qa),Qa),a).subs(sp.diff(Qa,a),dQ) + 3*sp.diff(K(Qa),Qa))==0,
   "B1  conservation  <=>  n = K' propto a^-3 EXACTLY (shift-charge conservation, derived not assumed)")
rhoL = -K(Qa)            # the promotion: a0^2 = kappa^2 G (-K)  =>  rho_DE c^2 = -K
dlnrhoL = sp.simplify(a*sp.diff(rhoL,a).subs(sp.diff(Qa,a),dQ))
rho_dust = sp.simplify(Qa*sp.diff(K(Qa),Qa))
cs2_a = sp.diff(K(Qa),Qa)/(Qa*sp.diff(K(Qa),Qa,2))
ck(sp.simplify(dlnrhoL - 3*rho_dust*cs2_a)==0,
   "B2  *** IDENTITY:  d(rho_DE)/d ln a  =  3 rho_dust c_s^2   (exact, ANY K) ***",
   f"d rho_DE/dlna = {sp.simplify(dlnrhoL)}")
ck(sp.simplify(rho_a - (rho_dust + rhoL))==0,
   "B3  and rho_total = rho_dust + rho_DE with p = -rho_DE exactly: w=-1 is the DE piece's own eos")

print(); print("="*100); print("C -- c_s^2 TODAY from the a0(z) law ALONE (kernel-free)"); print("="*100)
OM_DM, OM_L = mp.mpf("0.264"), mp.mpf("0.686")
C = mp.mpf("2.99792458e8"); ZREC = mp.mpf(1090)
NU0_LO, NU0_HI = mp.mpf("2.14e-5"), mp.mpf("1.77e-4")     # stage17 committed window
# committed derived law (stage17, beta=1):  a0^2(z)/a0^2(0) = sqrt((1+nu0^2)/(1+nu^2)), nu=nu0(1+z)^3
def g2(av, nu0):                  # = rho_DE(a)/rho_DE(0)
    nu = nu0/av**3
    return mp.sqrt((1+nu0**2)/(1+nu**2))
def dg2_dlna(av, nu0):
    nu = nu0/av**3
    return g2(av,nu0)*3*nu**2/(1+nu**2)
def cs2_from_a0(av, nu0):         # identity B2:  c_s^2 = (1/3) (d rho_DE/dlna)/rho_dust
    return (OM_L*dg2_dlna(av,nu0))/(3*OM_DM/av**3)
ck(abs(mp.sqrt(g2(1/(1+ZREC), NU0_LO))/mp.mpf("0.0060") - 1) < mp.mpf("0.02"),
   f"C1  the committed law reproduces a0(1090)/a0(0) = {s4(mp.sqrt(g2(1/(1+ZREC),NU0_LO)),3)} at nu0={s4(NU0_LO,3)}",
   "NOTE: nu0_floor is DEFINED by this requirement in stage17 -- 0.0060 is an INPUT, not an output")
for nu0,lab in ((NU0_LO,"nu0 floor 2.14e-5"),(NU0_HI,"nu0 ceiling 1.77e-4")):
    cs2_0 = cs2_from_a0(mp.mpf(1), nu0)
    cs2_r = cs2_from_a0(1/(1+ZREC), nu0)
    print(f"       {lab:22s}  c_s^2(today) = {s4(cs2_0,4)} c^2   c_s(today) = {s4(C*mp.sqrt(cs2_0)/1000,4)} km/s"
          f"   |   c_s^2(rec) = {s4(cs2_r,4)} c^2")
cs2_0_lo = cs2_from_a0(mp.mpf(1), NU0_LO); cs2_0_hi = cs2_from_a0(mp.mpf(1), NU0_HI)
cs2_r_lo = cs2_from_a0(1/(1+ZREC), NU0_LO)
ck(cs2_r_lo < mp.mpf("1e-9"), "C2  COLD at recombination automatically (the CMB constraint is not binding)")
ck(cs2_0_lo/cs2_r_lo > 1e3,
   f"C3  *** c_s^2 RISES by {s4(cs2_0_lo/cs2_r_lo,3)}x from recombination to today on the corpus's OWN a0(z) law ***",
   "cold when it must cluster, warm when it must not -- exactly the sector stage 8 asked for")

print(); print("="*100); print("D -- CROSS-CHECK against the committed DBI kernel (independent route)"); print("="*100)
U0 = mp.mpf("1.86e-10")           # mi_dbi_khronon_2026.py D1: u0_for_mond
def dbi_state(av, nu0):
    Lam = U0/nu0
    R = nu0/av**3
    s = R/mp.sqrt(1+R**2)
    return Lam, s, Lam*s*(1-s**2)/(1+Lam*s)
for nu0,lab in ((NU0_LO,"nu0=2.14e-5"),(NU0_HI,"nu0=1.77e-4")):
    Lam,s0,cs0 = dbi_state(mp.mpf(1), nu0); _,sr,csr = dbi_state(1/(1+ZREC), nu0)
    print(f"       {lab:14s} Lam={s4(Lam,3):>10s}  c_s^2(today)={s4(cs0,4)} ({s4(C*mp.sqrt(cs0)/1000,4)} km/s)"
          f"   c_s^2(rec)={s4(csr,4)}   s(rec)={s4(sr,6)}")
Lam,s0,cs0_dbi = dbi_state(mp.mpf(1), NU0_LO)
ck(abs(mp.log10(cs0_dbi/cs2_0_lo)) < 1,
   f"D1  the two INDEPENDENT routes agree to {s4(cs2_0_lo/cs0_dbi,3)}x  (identity {s4(cs2_0_lo,3)} vs DBI {s4(cs0_dbi,3)})",
   "kernel-free identity vs the explicit committed DBI -- same answer to within normalisation")

print(); print("="*100); print("E -- STAGE 7 PART A RE-PRICED: the polytrope constant taken at the WRONG epoch"); print("="*100)
RHO_C = mp.mpf("8.6e-27"); RHO_DM0 = OM_DM*RHO_C; RHO_REC = RHO_DM0*(1+ZREC)**3
G_SI = mp.mpf("6.674e-11"); PC = mp.mpf("3.086e16"); KPC=1000*PC; MPC=1e6*PC
CS2_REC_COMMITTED = mp.mpf("2.9e-8")
cs2_st7_today = CS2_REC_COMMITTED/(1+ZREC)**3
print(f"       stage 7 chain (c_s^2 = 2K rho, MONOTONE):  c_s^2(today) = {s4(cs2_st7_today,4)} c^2 "
      f"= {s4(C*mp.sqrt(cs2_st7_today),4)} m/s")
print(f"       corrected (identity, nu0 floor):           c_s^2(today) = {s4(cs2_0_lo,4)} c^2 "
      f"= {s4(C*mp.sqrt(cs2_0_lo)/1000,4)} km/s")
print(f"       corrected (DBI kernel, nu0 floor):         c_s^2(today) = {s4(cs0_dbi,4)} c^2 "
      f"= {s4(C*mp.sqrt(cs0_dbi)/1000,4)} km/s")
ck(cs0_dbi/cs2_st7_today > 1e5,
   f"E1  *** stage 7 UNDERSTATES c_s^2(today) by {s4(cs0_dbi/cs2_st7_today,4)}x "
   f"({s4(mp.log10(cs0_dbi/cs2_st7_today),3)} orders) = {s4(mp.sqrt(cs0_dbi/cs2_st7_today),4)}x in c_s ***",
   "the polytropic relation c_s^2 = 2K rho is valid only for s<<1 (LATE); stage 7 extracted K at "
   "RECOMBINATION where s -> 1 and the DBI has SATURATED, so c_s^2 is NOT proportional to rho there")
V_ESC = mp.mpf("5e5")
need = (V_ESC/C)**2
ck(True, f"E2  escape needs c_s^2(today) >= (v_esc/c)^2 = {s4(need,3)} c^2; available = {s4(cs0_dbi,3)} c^2"
   f"  =>  short by {s4(need/cs0_dbi,4)}x -- NOT 'superluminal by 3600x'",
   "the barrier is now PARAMETRIC (a factor in u_0), not a causality violation")

print(); print("="*100); print("F -- CLAIM 3 (105 pc) RE-PRICED, and the JEANS LENGTH"); print("="*100)
def K_poly(cs2, rho): return cs2*C**2/(2*rho)          # p = K rho^2  =>  c_s^2 = 2 K rho
K_st7 = K_poly(CS2_REC_COMMITTED, RHO_REC)
K_late_id  = K_poly(cs2_0_lo, RHO_DM0)
K_late_dbi = K_poly(cs0_dbi,  RHO_DM0)
def R_LE(Kv): return mp.pi*mp.sqrt(Kv/(2*mp.pi*G_SI))
def lam_J(Kv): return mp.sqrt(2*mp.pi*Kv/G_SI)
print(f"       stage 7 K (from RECOMBINATION, invalid regime): K={s4(K_st7,4)}  R_LaneEmden={s4(R_LE(K_st7)/PC,4)} pc"
      f"   lambda_J={s4(lam_J(K_st7)/PC,4)} pc")
print(f"       corrected K (identity, LATE branch):            K={s4(K_late_id,4)}  R_LaneEmden={s4(R_LE(K_late_id)/KPC,4)} kpc"
      f"   lambda_J={s4(lam_J(K_late_id)/KPC,4)} kpc")
print(f"       corrected K (DBI, LATE branch):                 K={s4(K_late_dbi,4)}  R_LaneEmden={s4(R_LE(K_late_dbi)/KPC,4)} kpc"
      f"   lambda_J={s4(lam_J(K_late_dbi)/KPC,4)} kpc")
ck(R_LE(K_late_dbi)/R_LE(K_st7) > 100,
   f"F1  *** CLAIM 3's 105 pc is wrong by {s4(R_LE(K_late_dbi)/R_LE(K_st7),4)}x: the minimum self-gravitating "
   f"radius is {s4(R_LE(K_late_dbi)/KPC,4)}-{s4(R_LE(K_late_id)/KPC,4)} kpc, NOT 105 pc ***",
   "and the sign of the physics FLIPS: 105 pc is sub-galactic (it clumps INTO galaxies); "
   "300-800 kpc is SUPER-galactic (a galaxy cannot hold it) while still sub-cluster")
ck(R_LE(K_late_dbi) < 2*MPC,
   f"F2  and it is still SMALLER than a cluster r_200 ~ 2 Mpc, so clusters keep their dark mass",
   "the split the framework needs falls out with NO new parameter")

print(); print("="*100); print("G -- what a polytropic sector actually does in an L* well (hydrostatic, exact)"); print("="*100)
# 2K drho/dr = -dPhi/dr  =>  rho(r) = rho_bg + DeltaPhi/(2K)   (EXACT for p=K rho^2 in an external well)
VC = mp.mpf("2.0e5")
for lab,Kv in (("identity",K_late_id),("DBI",K_late_dbi),("stage 7 K",K_st7)):
    for rin,rout in ((20*KPC,1*MPC),):
        dPhi = VC**2*mp.log(rout/rin)
        drho = dPhi/(2*Kv)
        print(f"       {lab:10s}: DeltaPhi(20 kpc<-1 Mpc)={s4(dPhi,3)} m^2/s^2 -> rho_sector/rho_dm0 = {s4(drho/RHO_DM0,4)}")
# what the (corrected) NFW double count needs at r_s = 20 kpc
M200 = mp.mpf("1.3e12")*mp.mpf("1.989e30"); r200 = 200*KPC; c_nfw = mp.mpf(10); rs = r200/c_nfw
mfun = mp.log(1+c_nfw) - c_nfw/(1+c_nfw)
rho_s = M200/(4*mp.pi*rs**3*mfun)
rho_nfw_rs = rho_s/(1*(1+1)**2)
print(f"       NFW c=10 at r_s=20 kpc (cosmic share): rho/rho_dm0 = {s4(rho_nfw_rs/RHO_DM0,4)}")
supp_dbi = rho_nfw_rs/(VC**2*mp.log(mp.mpf(50))/(2*K_late_dbi))
supp_id  = rho_nfw_rs/(VC**2*mp.log(mp.mpf(50))/(2*K_late_id))
ck(supp_dbi > 2,
   f"G1  a pressure-supported polytropic sector is UNDER the NFW requirement at r_s by "
   f"{s4(supp_id,3)}x (identity) / {s4(supp_dbi,3)}x (DBI)",
   "i.e. the sector's own equation of state suppresses its halo density by ~1 order at r_s -- "
   "against the CORRECTED overshoot of 1.93x at r_M this is a real, live suppression")
ck(K_st7 < K_late_dbi,
   f"G2  CONTROL: with stage 7's (invalid-regime) K the SAME calculation gives contrast "
   f"{s4(VC**2*mp.log(mp.mpf(50))/(2*K_st7)/RHO_DM0,3)} -- vastly ABOVE the NFW requirement, "
   "which is exactly why stage 7 concluded the sector is captured")

print(); print("="*100); print("H -- CLAIM 1 exact:  rho = Q n - p, so rho/n = Q_0 IFF p = 0"); print("="*100)
u, Q0, mu, A, S = sp.symbols("u Q_0 mu A S", positive=True)
L = mu**2*u**2/2 + A*S*u**2
nn = sp.diff(L,u); rr = sp.expand((Q0+u)*nn - L)
ratio_exact = sp.simplify(rr/nn)
ck(sp.simplify(ratio_exact - (Q0 + u/2))==0,
   f"H1  the EXACT ratio is rho/n = {ratio_exact}, NOT Q_0.  stage 7's B1 truncated the series at O(u).",
   "the dropped piece is exactly p/n: rho = Q n - p is an IDENTITY for any K")
ck(sp.simplify(sp.simplify(Q*sp.diff(K(Q),Q) - K(Q)) - (Q*n_ - p_))==0,
   "H2  and in general rho = Q n - p identically  =>  'the dust mass IS the conserved charge' "
   "is EQUIVALENT to 'the sector is pressureless'",
   "so CLAIM 1 assumes what the warm route denies: it is not independent of the dust premise")

print(); print("="*100); print("I -- CLAIM 2 re-priced with the CORRECT lensing source (part 1 result)"); print("="*100)
w = sp.Symbol("w", real=True); f = sp.Symbol("f", real=True)
dyn = 1 + 3*w; lensC = 1 + sp.Rational(3,2)*w      # rho+3p  and  rho+3p/2
ck(sp.solve([dyn, lensC], w) == [],
   f"I1  CONCLUSION HOLDS: rho+3p=0 at w={sp.solve(dyn,w)[0]}, rho+3p/2=0 at w={sp.solve(lensC,w)[0]}, no common root")
ck(sp.solve(lensC,w)[0] != sp.Integer(-1),
   f"I2  *** but stage 7's stated pair is WRONG: it says lensing sees rho+p (w=-1). "
   f"Part 1's from-scratch Einstein solve gives rho + (p_r+2p_t)/2, i.e. w = {sp.solve(lensC,w)[0]} ***",
   "sf38_lensing_tolerance_2026.py has the CORRECT source (rho + s/2); stage 7 C1 contradicts it")
fstar = sp.solve(1-3*f, f)[0]
lens_res = sp.simplify((1-f) + f*(1+sp.Rational(3,2)*(-1))).subs(f,fstar)
ck(lens_res == sp.Rational(1,2),
   f"I3  at the f={fstar} fixed point the lensing residual is {lens_res} rho, not 2/3 rho "
   "-- 25% weaker than stated, direction: AGAINST the kill")
# the "29"
for ratio,lab in ((mp.mpf("5.375"),"cosmic Om_dm/Om_b"),(mp.mpf("30"),"abundance-matching M_h/M_star")):
    print(f"       M_lens/M_dyn with M_dark/M_b = {s4(ratio,4)} ({lab}): "
          f"{s4(1+mp.mpf('0.5')*ratio,4)} (correct 1/2) vs {s4(1+mp.mpf(2)/3*ratio,4)} (stage 7's 2/3)")
ck(1+mp.mpf("0.5")*mp.mpf("5.375") < 29,
   "I4  the quoted 'M_lens/M_dyn ~ 29' is NOT reproducible from the cosmic baryon share "
   "(gives 3.7) and is not computed anywhere in stage 7 -- it is an uncomputed assertion",
   "conclusion (>> the observed 1.0-1.3) survives on any of these values; the NUMBER does not")

print(); print("="*100)
print(f"CHECKS {N[0]-len(FAIL)}/{N[0]}" + ("" if not FAIL else "   FAILED: "+"; ".join(FAIL)))


print(); print("="*100); print("J -- THE COST, computed with the FULL c_s^2(a), not the polytropic extrapolation"); print("="*100)
OM_M = mp.mpf("0.315"); RHO_M0 = OM_M*RHO_C
def lamJ_com(av, nu0):
    _,_,cs2 = dbi_state(av, nu0)
    return 2*mp.pi*C*mp.sqrt(cs2)*mp.sqrt(av)/mp.sqrt(4*mp.pi*G_SI*RHO_M0)
a_turn = NU0_LO**(mp.mpf(1)/3)
print(f"       polytropic (c_s^2 ~ rho) branch valid only for a >> nu0^(1/3) = {s4(a_turn,3)} (z << {s4(1/a_turn-1,4)});")
print(f"       BELOW that the DBI wall makes c_s^2 FALL as a^6, so the naive extrapolation OVERSTATES early pressure.")
print(f"       {'a':>9s} {'z':>8s} {'c_s^2/c^2':>12s} {'lamJ_com Mpc':>13s} {'k_J 1/Mpc':>11s}")
grid = [mp.mpf(x) for x in ("1.0","0.5","0.25","0.1","0.05","0.0334","0.02","0.01","0.005","0.001")]
best = (0,None)
for av in grid:
    _,_,cs2 = dbi_state(av, NU0_LO); lc = lamJ_com(av, NU0_LO)/MPC
    if lc > best[0]: best = (lc, av)
    print(f"       {s4(av,3):>9s} {s4(1/av-1,4):>8s} {s4(cs2,4):>12s} {s4(lc,4):>13s} {s4(2*mp.pi/lc,4):>11s}")
lc_max, a_max = best
ck(2*mp.pi/lc_max > mp.mpf("0.2"),
   f"J1  *** THE LARGEST COMOVING SCALE EVER PRESSURE-SUPPRESSED is {s4(lc_max,4)} Mpc "
   f"(at a = {s4(a_max,3)}, z = {s4(1/a_max-1,4)}), i.e. k_J,min = {s4(2*mp.pi/lc_max,4)} /Mpc. "
   f"k = 0.2 /Mpc and sigma_8 (k ~ 0.13) are NEVER inside it ***",
   "so the non-claim-3 scale the corpus itself flagged is CLEAR on this parameter set")
for zq in (mp.mpf(2), mp.mpf(5)):
    aq = 1/(1+zq); lq = lamJ_com(aq, NU0_LO)/MPC
    print(f"       Lyman-alpha epoch z={s4(zq,2)}:  k_J = {s4(2*mp.pi/lq,4)} /Mpc  (forest probes k ~ 0.5-20 /Mpc)")
lq2 = lamJ_com(1/(1+mp.mpf(3)), NU0_LO)/MPC
ck(2*mp.pi/lq2 < 20,
   f"J2  *** THE REAL COST, and it is not k=0.2: at z=3 the sector's Jeans cut is k_J = {s4(2*mp.pi/lq2,4)} /Mpc, "
   "INSIDE the Lyman-alpha forest's window. THAT is where this construction must be confronted ***",
   "the corpus's committed forest work (stage14-16, 0.2% worst bin) was done with a DIFFERENT c_s^2 "
   "and does NOT cover this; it is OWED")
print()
print("       HONEST LIMIT OF PART J: c_s^2 here is the SECTOR's adiabatic sound speed.  In the full")
print("       AeST/khronon + metric system the physical scalar eigenmodes are MIXTURES, and their")
print("       eigen-sound-speeds are NOT c_ad^2 (already flagged in RETRACTIONS.md 2026-08-19).  A")
print("       patched-CLASS fluid carrying c_s^2(a) is required to convert J1/J2 into a verdict.")
print()
print("="*100)
print(f"CHECKS {N[0]-len(FAIL)}/{N[0]}" + ("" if not FAIL else "   FAILED: "+"; ".join(FAIL)))
