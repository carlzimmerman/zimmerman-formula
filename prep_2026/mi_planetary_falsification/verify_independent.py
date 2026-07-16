#!/usr/bin/env python3
r"""
INDEPENDENT adversarial re-derivation of the MI planetary-falsification window.
Nothing imported from the lane scripts; every number rebuilt from first principles here.
Checks:
  (1) per-planet delta_g from Fienga-Minazzoli 2024 Table 10 perihelion sigmas via the Gauss
      secular equation, DERIVED here (not copied), for Mercury/Mars/Saturn -> exclusion factors honest?
  (2) the a0/2 CONSTANT sunward accel -> its per-planet observable (precession rate) GROWS with a;
      and the omega_c reactive-suppression conversion Re G=(wc/omega)^2 is right.
  (3) the secular-drift upper edge d ln r/dt = a0 wc/g_N re-derived from da/dt=2T/n independently.
  (4) both footings; window intersection; and a stress test of the lower edge and the gate order.
NO hard-coded verdict booleans; PASS is accumulated from computed comparisons only.
"""
import numpy as np, sys
PASS = True
def check(name, cond):
    global PASS
    ok = bool(cond); print(f"   [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok: PASS = False

C   = 2.99792458e8
YR  = 3.15576e7
MYR = YR*1e6
GYR = YR*1e9
MAS = 4.84813681e-9        # rad per milli-arcsec
GMsun   = 1.32712440018e20
GMearth = 3.986004418e14
A0 = {"canon": 9.36e-11, "alt": 1.13e-10}

# ------------------------------------------------------------------------------------------------
# (1) INDEPENDENT Gauss secular derivation of per-planet delta_g from a perihelion-rate sigma.
#     For a CONSTANT radial (sunward) perturbing accel A_r, Gauss: dw/dt = -(A_r/e) sqrt(p/GM) cos f.
#     Time-average <cos f>_t = -e  (derived below numerically as a check), so <dw/dt> = A_r sqrt(p/GM).
#     => A_r = |wdot| * sqrt(GM/p),  p=a(1-e^2).   Invert a measured sigma(wdot) [rad/s] into delta_g.
# planet: (a[m], e, T[days], sigma_perihelion[mas/yr])  sigma from FM24 Table 10 (EPM/INPOP best col)
PLAN = {
 "Mercury":(5.7909e10, 0.2056, 87.969,   0.006),
 "Venus"  :(1.08209e11,0.0068, 224.701,  0.015),
 "Earth"  :(1.49598e11,0.0167, 365.256,  0.0019),
 "Mars"   :(2.27939e11,0.0934, 686.980,  0.00037),
 "Jupiter":(7.78570e11,0.0489, 4332.59,  0.28),
 "Saturn" :(1.43353e12,0.0565, 10759.22, 0.0047),
}
# numeric check that time-averaged <cos f> = -e for an eccentric orbit (Kepler), e.g. Mars e=0.0934
def avg_cosf(e, N=2_000_000):
    f = np.linspace(0, 2*np.pi, N, endpoint=False)
    w = 1.0/(1+e*np.cos(f))**2                # dt propto r^2 df propto 1/(1+e cos f)^2
    return np.sum(np.cos(f)*w)/np.sum(w)
for e_test in (0.0934, 0.2056):
    check(f"time-avg <cos f> = -e  (e={e_test}: numeric {avg_cosf(e_test):+.5f} vs -e={-e_test:+.5f})",
          abs(avg_cosf(e_test) + e_test) < 1e-3)

FM24_TABLE = {"Mercury":4.6e-14,"Venus":8.0e-14,"Earth":8.7e-15,"Mars":1.4e-15,"Jupiter":5.6e-13,"Saturn":7.0e-15}
print("\n(1) per-planet delta_g via INDEPENDENT Gauss secular equation:")
dg = {}
for nm,(a,e,Td,sig_mas) in PLAN.items():
    p   = a*(1-e**2)
    wdot = sig_mas*MAS/YR                     # rad/s (1-sigma perihelion-rate uncertainty)
    A_r = wdot*np.sqrt(GMsun/p)               # = |wdot| sqrt(GM/p)   (constant radial accel bound)
    dg[nm] = A_r
    ratio = A_r/FM24_TABLE[nm]
    print(f"   {nm:8s}: sigma={sig_mas:7.4f} mas/yr  -> delta_g={A_r:.3e} m/s^2   (banked {FM24_TABLE[nm]:.1e}, ratio {ratio:.2f})")
    check(f"{nm} delta_g reproduces banked FM24 value within 15%", abs(ratio-1) < 0.15)

# exclusion factor of the a0/2 constant tail, per planet, both footings
print("\n    exclusion of the a0/2 constant sunward tail:")
for lab,a0 in A0.items():
    ex = {nm: (a0/2)/dg[nm] for nm in PLAN}
    binder = max(ex, key=ex.get)
    print(f"    [{lab}] a0/2={a0/2:.2e}:  " + ", ".join(f"{nm} {ex[nm]:.0f}x" for nm in PLAN))
    print(f"           -> tightest = {binder} ({ex[binder]:.0f}x)")
    # honesty band: kill must be >= ~600x (Venus) and Mars/Saturn ~ 6e3-3e4 x
    check(f"[{lab}] Mars excludes a0/2 by 3e4-4e4x and Saturn by ~6e3-8e3x (matches banked, not inflated)",
          2.8e4 < ex["Mars"] < 4.5e4 and 6e3 < ex["Saturn"] < 9e3)

# ------------------------------------------------------------------------------------------------
# (2) the a0/2 tail's observable is a PRECESSION rate that GROWS with a (so Mars/Saturn dominate).
#     From <dw/dt> = A_r sqrt(p/GM) = A_r sqrt(a(1-e^2)/GM) ~ A_r sqrt(a/GM) -> propto sqrt(a).
print("\n(2) a0/2 constant tail: precession rate vs semimajor axis (should GROW ~ sqrt(a)):")
a0 = A0["canon"]
wdots = []
for nm,(a,e,Td,sig) in PLAN.items():
    wd = (a0/2)*np.sqrt(a*(1-e**2)/GMsun)     # rad/s precession from the constant a0/2 tail
    wd_masyr = wd/MAS*YR
    wdots.append((a,wd))
    print(f"   {nm:8s}: a={a:.3e} m  precession from a0/2 = {wd_masyr:8.2f} mas/yr")
# monotonic in a (ignoring e), and Saturn >> Mercury
aa = np.array([x[0] for x in wdots]); ww=np.array([x[1] for x in wdots])
order = np.argsort(aa)
check("precession from a0/2 grows monotonically with semimajor axis (outer planets dominate)",
      np.all(np.diff(ww[order]) > 0))
# scaling check: ratio Saturn/Mercury precession should ~ sqrt(a_Sat/a_Merc)
rat_pred = np.sqrt(PLAN["Saturn"][0]/PLAN["Mercury"][0])
rat_act  = ( (a0/2)*np.sqrt(PLAN["Saturn"][0]*(1-PLAN["Saturn"][1]**2)/GMsun) ) / \
           ( (a0/2)*np.sqrt(PLAN["Mercury"][0]*(1-PLAN["Mercury"][1]**2)/GMsun) )
check(f"precession scales as sqrt(a): Saturn/Mercury ratio {rat_act:.2f} ~ sqrt(a_S/a_M)={rat_pred:.2f}",
      abs(rat_act/rat_pred-1) < 0.05)

# omega_c reactive suppression: gate Re G=1/(1+(w/wc)^2); for w>>wc, Re G=(wc/w)^2. Verify the edge
# wc <= omega_p sqrt(2 delta_g/a0) is the solution of (a0/2)(wc/w)^2 = delta_g.
def omega_of(Td): return 2*np.pi/(Td*86400.0)
print("\n    reactive per-planet omega_c edge (a0/2)(wc/w)^2 = delta_g  ->  wc = w sqrt(2 dg/a0):")
for lab,a0f in A0.items():
    edges = {nm: omega_of(PLAN[nm][2])*np.sqrt(2*dg[nm]/a0f) for nm in PLAN}
    b = min(edges, key=edges.get)
    print(f"    [{lab}] binding reactive edge = {b}  wc<= {edges[b]:.2e} rad/s  "
          f"(3-4 dex LOOSER than the drift edge below)")
    # closed-form must equal the direct root of the gate equation
    w = omega_of(PLAN[b][2]); root = w*np.sqrt(2*dg[b]/a0f)
    resid = (a0f/2)*(root/w)**2 - dg[b]
    check(f"[{lab}] reactive edge is the exact root of (a0/2)(wc/w)^2=delta_g at {b}", abs(resid) < 1e-30)

# ------------------------------------------------------------------------------------------------
# (3) secular-drift upper edge, re-derived INDEPENDENTLY from da/dt = 2 T/n (circular orbit).
#     Gate: G=1/(1+i w/wc). Dissipative accel f_t=(a0/2)|Im G|, Im G=-(w/wc)/(1+(w/wc)^2).
#     w>>wc: |Im G| = wc/w. da/dt=2 f_t/n=2 f_t/w ; d ln r/dt=2 f_t/(w a)=a0 wc/(w^2 a)=a0 wc/g_N.
print("\n(3) secular-drift edge d ln r/dt = a0 wc/g_N  (re-derived; LLR Gdot/G binds):")
# independent numeric: pick the Moon, a random wc in-window, compare closed form vs 2 f_t/(w a)
def ImG(w,wc): return -(w/wc)/(1+(w/wc)**2)
a_moon, T_moon = 3.844e8, 27.3217
w_moon = omega_of(T_moon)
gN_moon_dyn  = w_moon**2*a_moon        # DYNAMICAL g_N = omega^2 r (what the closed form actually uses)
gN_moon_kepl = GMearth/a_moon**2       # kinematic GM/r^2 (lane origin script's 2.70e-3 input)
print(f"    g_N,moon dynamical omega^2 r = {gN_moon_dyn:.4e} vs GMearth/r^2 = {gN_moon_kepl:.4e} "
      f"(differ {abs(gN_moon_dyn/gN_moon_kepl-1)*100:.2f}% from a/T rounding; immaterial to a x2.5 window)")
for wc in (1e-14, 2e-14):
    a0 = A0["canon"]
    f_t = (a0/2)*abs(ImG(w_moon,wc)); direct = 2*f_t/(w_moon*a_moon); closed = a0*wc/gN_moon_dyn
    check(f"Moon d ln r/dt: direct 2f_t/(wa)={direct:.3e} = a0 wc/(omega^2 r)={closed:.3e} (wc={wc:.0e}, "
          f"asymptote exact to (wc/w)^2~1e-17)", abs(direct/closed-1) < 1e-6)
gN_moon = gN_moon_kepl                 # keep the lane's kinematic value for the window edge (0.9% conservative)
# LLR bound: Biskupek & Mueller 2021 Gdot/G=(-5.0+/-9.6)e-15/yr; 2-sigma ceiling |cen|+2sig.
LLR_cen, LLR_sig = 5.0e-15, 9.6e-15
LLR_2sig = LLR_cen + 2*LLR_sig
print(f"    LLR Gdot/G=(-5.0+/-9.6)e-15/yr -> 2sigma ceiling |cen|+2sig = {LLR_2sig:.3e}/yr")
print("\n(4) JOINT WINDOW both footings (independent intersection):")
Y_DEEP, V_DWARF, GATE = 0.8, 25e3, 0.90
k = np.sqrt(GATE/(1-GATE))
win = {}
for lab,a0 in A0.items():
    om_gal = Y_DEEP*a0/V_DWARF
    lo = k*om_gal
    hi = (LLR_2sig/YR)*gN_moon/a0                 # a0 wc/g_N <= bound/s  -> wc <= bound*gN/a0
    win[lab] = (lo,hi)
    print(f"   [{lab}] lower(RAR)= {lo:.3e}  upper(LLR)= {hi:.3e} rad/s  "
          f"[{1/hi/MYR:.2f},{1/lo/MYR:.2f}] Myr  width x{hi/lo:.2f}  -> {'OPEN' if hi>lo else 'EMPTY'}")
    check(f"[{lab}] independent window NON-EMPTY", hi > lo)
    # forced action corner a0/2c must be FAR below the window (FREE, not forced)
    wc_act = a0/(2*C)
    check(f"[{lab}] action-forced corner a0/2c={wc_act:.2e} is >=4 dex below window bottom (corner is FREE)",
          np.log10(lo/wc_act) >= 4)

# ------------------------------------------------------------------------------------------------
# STRESS TESTS (hunt a manufactured save AND a manufactured deficit):
print("\n(5) STRESS TESTS:")
# (5a) manufactured-save check on the gate order: a SHARPER gate (order n) has drift ~ (wc/w)^n at the
#      Moon -> LOOSER drift edge -> WIDER window. So the single-pole (n=1) is the WORST case for drift:
#      choosing it does NOT manufacture a save. Verify n=2 gives a wider window.
def hi_edge_order(a0, n):
    # order-n low-pass |Im G| ~ (wc/w)^n at w>>wc ; drift ~ (a0/2)*2/(w a)*(wc/w)^n. Solve for wc at LLR.
    # d ln r/dt = a0 (wc/w)^n * (1/(w a)) ... set = bound. wc = w*( bound*w*a/a0 )^(1/n). Larger for n>1.
    bound = LLR_2sig/YR
    return w_moon*(bound*w_moon*a_moon/a0)**(1.0/n)
for lab,a0 in A0.items():
    h1, h2 = hi_edge_order(a0,1), hi_edge_order(a0,2)
    check(f"[{lab}] single-pole (n=1) drift edge {h1:.2e} is TIGHTER than n=2 {h2:.2e} "
          f"-> n=1 is conservative, NOT a manufactured save", h2 > h1)
# (5b) manufactured-deficit check: does the window survive a reasonably TIGHTER RAR lower edge and a
#      1-sigma (not 2-sigma) LLR?  Report where it closes -- honest fragility, neither hidden nor inflated.
print("    fragility scan (canon): where does the window close?")
a0 = A0["canon"]
for (yv,vv,nsig,tag) in [(0.8,25e3,2,"baseline"),(1.0,20e3,2,"harsher RAR (y=1,v=20)"),
                          (0.8,25e3,1,"1-sigma LLR"),(1.0,15e3,2,"aggressive RAR (y=1,v=15)")]:
    lo = k*(yv*a0/vv)
    bnd = (LLR_cen+nsig*LLR_sig)/YR
    hi = bnd*gN_moon/a0
    print(f"      {tag:28s}: lo={lo:.2e} hi={hi:.2e} -> {'OPEN x%.2f'%(hi/lo) if hi>lo else 'CLOSED'}")
# (5c) at what a0 does the window pinch shut? lo(a0)=hi(a0).
a0_close = np.sqrt( (LLR_2sig/YR)*gN_moon / (k*Y_DEEP/V_DWARF) )
print(f"    window pinches shut at a0 = {a0_close:.3e} m/s^2 (both footings {A0['canon']:.2e},{A0['alt']:.2e} are below it)")
check("both footings sit below the a0 at which the window closes (survival is not knife-edge in a0)",
      A0["alt"] < a0_close and A0["canon"] < a0_close)

print("\n"+"="*90)
print(f" verify_independent: {'ALL CHECKS PASS' if PASS else 'A CHECK FAILED'}")
print("="*90)
sys.exit(0 if PASS else 1)
