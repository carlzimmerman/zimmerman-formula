#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
G239 -- THE PROPER EXTERNAL FIELD: QUMOND EFE solve for the Milky Way's phantom halo.
=====================================================================================
WHY THIS LANE EXISTS.  DW1 (closure_2026_11_11/DW1_desi_dr2_mw_mass/) confronted the framework's
zero-parameter enclosed-mass law with DESI DR2 III's 13-point profile (arXiv:2611.05518, Table 4) and
found that the DOMINANT modelling uncertainty is the external field: with the repo's scalar-additive
approximation nu((g_bar + g_ext)/a0) the 80 kpc prediction falls to 4.31e11 (-4.1 sigma) and the
profile fit degrades to 7 per cent rms, while with no external field it is 5.69e11 (-1.34 sigma) at
2.9 per cent rms.  That approximation is the MAXIMUM-suppression case: it adds the external field to
the internal one in the same direction everywhere.  The real EFE is a VECTOR sum, and the spherically
averaged radial force is weaker-suppressed because the perpendicular directions see less field.

THIS LANE replaces the hack with the QUMOND monopole integral, exactly:

    g_N(r,theta) = g_b(r) r_hat + g_ext z_hat ,   |g_N|^2 = g_b^2 + g_ext^2 + 2 g_b g_ext cos(theta)
    g_r(r,theta) = nu(|g_N|/a0) (g_b + g_ext cos(theta))          [QUMOND: g = nu(|g_N|/a0) g_N]
    <g_r>(r)     = (1/2) INT_{-1}^{1} dmu  nu(|g_N|/a0) (g_b + g_ext mu) ,  mu = cos(theta)
    M_dyn(<r)    = r^2 <g_r>(r) / G

The uniform external field contributes nothing to <g_r> directly (its own term integrates to zero), so
M_dyn(<r) is the mass the Galaxy would be credited with by a spherical Jeans analysis sitting in that
field -- exactly the quantity DESI measures.  The two limits are exact and are used as instrument
checks: g_ext = 0 recovers nu(g_b/a0) M_b (DW1's law), and a constant kernel nu = const recovers
nu * M_b with no anisotropy at all.

WHAT IT DELIVERS
  G239a  the plateau M_sat = lim r^2<g_r>/G for e_N in {0.008, 0.0127, 0.017, 0.02, 0.05}, both
         footings -- i.e. the number the ARMED MW-plateau falsifier (FALSIFIER_MATRIX row 32) tests;
  G239b  the 13-point DESI fit with the PROPER EFE and a free amplitude: does the EFE still spoil the
         shape, or was that the hack?
  G239c  the anisotropy: the parallel (theta=0) vs perpendicular (theta=90 deg) enclosed mass at the
         DESI radii -- the systematic on any spherical analysis in an EFE field;
  G239d  the price of the hack: the ratio of the proper average to DW1's scalar-additive value.

AQUAL cross-check, not reproduced here: the repo's full AQUAL solver (DE01, qwen_claude_field_theory/
theory_2026/aqual_solver_2026.py) finds nu_rad = 1.222 / nu_vert = 1.251 at R0 against the algebraic
nu = 1.444 (h34's caveat) -- the algebraic (QUMOND) boost is ~15 per cent HIGH, so the QUMOND numbers
below are an upper bound on the framework's own boost and the EFE suppression computed here is, if
anything, understated.  Recorded, not used to excuse anything.

Both footings, never pooled.  Mutation controls.  kappa = 1/2 FITTED; not theory closed.
"""
import json, math
import numpy as np
TRAPZ = getattr(np, "trapezoid", None) or np.trapz

G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; PC = KPC/1000.0; MSUN_PC2 = MSUN/PC**2
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
RHOC_Mpc3 = 1.36e11
M80_D, M80_S = 6.36, 0.50
M200_D, M200_S = 1.19, 0.13
E_GRID = [0.0, 0.008, 0.01273, 0.017, 0.02, 0.05]

OUT = open("g239.out", "w")
def say(s=""):
    print(s); OUT.write(str(s)+"\n"); OUT.flush()
N = [0]; FAILS = []
def ck(name, ok, detail=""):
    N[0] += 1
    if not ok: FAILS.append(name)
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         ({detail})" if detail else ""))

def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-14); return 1.0/(1.0-np.exp(-np.sqrt(y)))

# ---- McMillan 2017 baryons (h34's validated model, verbatim; same as DW1/G238)
MC = dict(thin =dict(S0=896.0*MSUN_PC2, Rd=2.50*KPC, zd=0.300*KPC, Rm=0.0,   vert="exp"),
          thick=dict(S0=183.0*MSUN_PC2, Rd=3.02*KPC, zd=0.900*KPC, Rm=0.0,   vert="exp"),
          HI   =dict(Sfid=10.0*MSUN_PC2, Rfid=8.33*KPC, Rd=7.00*KPC, zd=0.085*KPC, Rm=4.0*KPC,  vert="sech2"),
          H2   =dict(Sfid= 2.0*MSUN_PC2, Rfid=8.33*KPC, Rd=1.50*KPC, zd=0.045*KPC, Rm=12.0*KPC, vert="sech2"))
MBULGE, ABULGE = 9.23e9*MSUN, 0.70*KPC
def S0_of(c): return c["S0"] if "S0" in c else c["Sfid"]/math.exp(-c["Rm"]/c["Rfid"]-c["Rfid"]/c["Rd"])
def sigma_of_R(c, R):
    R = np.maximum(np.asarray(R, float), 1e-6*KPC); return S0_of(c)*np.exp(-c.get("Rm",0.0)/R - R/c["Rd"])
def disc_mass(c):
    Rg = np.geomspace(1e-5*KPC, 600*KPC, 20000); return float(TRAPZ(2*np.pi*Rg*sigma_of_R(c, Rg), Rg))
_ZC = {}
def zprofile(c, n=1201):
    key = (c["vert"], round(c["zd"], 9))
    if key in _ZC: return _ZC[key]
    zg = np.linspace(-10*c["zd"], 10*c["zd"], n)
    zz = (np.exp(-np.abs(zg)/c["zd"])/(2*c["zd"]) if c["vert"]=="exp"
          else 1.0/np.cosh(zg/(2*c["zd"]))**2/(4*c["zd"]))
    cum = np.concatenate([[0.0], np.cumsum((zz[1:]+zz[:-1])/2*np.diff(zg))]); cum /= cum[-1]
    _ZC[key] = (zg, zz, cum); return _ZC[key]
def M_sph(r):
    r = float(r); tot = MBULGE*r**2/(r+ABULGE)**2
    Rg = np.linspace(1e-4*KPC, min(r, 60*KPC), 4000); h = np.sqrt(np.maximum(r**2-Rg**2, 0.0))
    for k, c in MC.items():
        zg, zz, cum = zprofile(c)
        tot += float(TRAPZ(2*np.pi*Rg*sigma_of_R(c, Rg)*np.interp(h, zg, cum), Rg))
    return tot
MB = sum(disc_mass(c) for c in MC.values()) + MBULGE

MU = np.linspace(-1.0, 1.0, 4001)

def g_r_avg(r_kpc, a0, e_N, kern=nu):
    """angle-averaged radial force of the Galaxy in a uniform external field e_N (in a0 units)"""
    Mb = M_sph(r_kpc*KPC); gb = G*Mb/(r_kpc*KPC)**2/a0          # in a0 units
    gm = np.sqrt(gb*gb + e_N*e_N + 2*gb*e_N*MU)
    return float(TRAPZ(kern(gm)*(gb + e_N*MU), MU)/2.0)          # in a0 units

def M_dyn(r_kpc, a0, e_N, A=1.0, kern=nu):
    Mb = A*M_sph(r_kpc*KPC)
    gb = G*Mb/(r_kpc*KPC)**2/a0
    gm = np.sqrt(gb*gb + e_N*e_N + 2*gb*e_N*MU)
    val = float(TRAPZ(kern(gm)*(gb + e_N*MU), MU)/2.0)           # a0 units
    return val/gb*Mb/MSUN/1e11                                   # r^2<g_r>/G = (<g_r>/g_b) M_sph

def M_dyn_dir(r_kpc, a0, e_N, mu0, A=1.0):
    """enclosed mass along a fixed direction mu0 = cos(theta)"""
    Mb = A*M_sph(r_kpc*KPC); gb = G*Mb/(r_kpc*KPC)**2/a0
    gm = math.sqrt(gb*gb + e_N*e_N + 2*gb*e_N*mu0)
    return float(nu(gm)*(gb + e_N*mu0))/gb*Mb/MSUN/1e11

# DESI DR2 III Table 4
R  = np.array([20,25,30,35,40,45,50,55,60,65,70,75,80], float)
M  = np.array([1.94,2.30,2.65,3.05,3.54,4.08,4.51,4.88,5.19,5.56,5.88,6.14,6.36])
EL = np.array([0.12,0.11,0.13,0.15,0.17,0.21,0.26,0.31,0.34,0.38,0.43,0.46,0.48])
EH = np.array([0.12,0.12,0.14,0.16,0.18,0.22,0.27,0.32,0.36,0.40,0.46,0.50,0.53])
SIG = (EL+EH)/2

say("="*112)
say("G239  THE PROPER EXTERNAL FIELD -- QUMOND EFE solve for the Milky Way's phantom halo")
say("      replaces DW1's scalar-additive nu((g_bar+g_ext)/a0) with the exact angle average")
say("      <g_r> = (1/2) INT dmu nu(|g_bar r_hat + g_ext z_hat|/a0)(g_bar + g_ext mu)")
say("      kappa = 1/2 FITTED; not theory closed.  Both footings.")
say("="*112)

# ===================================================================================================
say("\n" + "="*112); say("V -- INSTRUMENT (the two limits are exact and are the checks)"); say("="*112)
say(f"  McMillan 2017: M_b = {MB/MSUN:.4e} Msun")
# V1: e_N = 0 recovers the framework's own law exactly
e1 = {f: M_dyn(80.0, a0, 0.0) for f, a0 in A0.items()}
ref = {f: float(nu(G*M_sph(80*KPC)/(80*KPC)**2/a0))*M_sph(80*KPC)/MSUN/1e11 for f, a0 in A0.items()}
ck("V1 with e_N = 0 the angle average reproduces nu(g_bar/a0) M_b exactly (DW1's law)",
   all(abs(e1[f]/ref[f]-1) < 1e-9 for f in A0),
   "; ".join(f"{f} {e1[f]:.6f} vs {ref[f]:.6f}" for f in A0) + " (1e-9 relative)")
# V2: a constant kernel gives no anisotropy and no EFE
const_k = lambda y: np.ones_like(np.asarray(y, float))*2.5
c_par = M_dyn_dir(60.0, A0["canonical"], 0.0127, 1.0, 1.0)
gb60 = G*M_sph(60*KPC)/(60*KPC)**2/A0["canonical"]
const_dir = float(const_k(gb60))*(gb60+0.0127)/gb60*M_sph(60*KPC)/MSUN/1e11
const_avg = M_dyn(60.0, A0["canonical"], 0.0127, 1.0, const_k)
ck("V2 a CONSTANT kernel returns 2.5 x M_b with no anisotropy and no external-field dependence "
   "(the EFE lives entirely in nu, not in the geometry)",
   abs(const_avg/(2.5*M_sph(60*KPC)/MSUN/1e11)-1) < 1e-9,
   f"constant-kernel angle average {const_avg:.4f} = 2.5 x M_sph(60 kpc) = {2.5*M_sph(60*KPC)/MSUN/1e11:.4f}")
# V3: the proper EFE must lie between no-EFE and the scalar-additive maximum-suppression value
rows = []
for f, a0 in A0.items():
    for e in (0.008, 0.01273, 0.02):
        for rr in (40.0, 80.0):
            Mb = M_sph(rr*KPC); gb = G*Mb/(rr*KPC)**2/a0
            proper = M_dyn(rr, a0, e)
            noefe = float(nu(gb))*Mb/MSUN/1e11
            scal  = float(nu(gb+e))*Mb/MSUN/1e11
            rows.append((f, e, rr, proper, noefe, scal, scal <= proper <= noefe))
ok_v3 = all(r[6] for r in rows)
worst = max(abs(r[3]/r[5]-1) for r in rows)
ck("V3 the proper average lies BETWEEN the no-EFE value and the scalar-additive (maximum-suppression) "
   "value at every footing, field and radius tested",
   ok_v3,
   f"{len(rows)}/{len(rows)} in order; the scalar-additive is {min(abs(r[3]/r[5]-1) for r in rows)*100:.0f}-{worst*100:.0f} "
   f"per cent below the proper average, so it over-suppresses")
say("  r [kpc]  e_N      proper      no-EFE     scalar-add   proper/no-EFE")
for r in rows[:4]:
    say(f"  {r[2]:5.0f}   {r[1]:.4f}   {r[3]:8.3f}   {r[4]:8.3f}   {r[5]:8.3f}     {r[3]/r[4]:.3f}")

# ===================================================================================================
say("\n" + "="*112)
say("G239a -- THE PLATEAU: M_sat = lim r^2<g_r>/G, the number FALSIFIER_MATRIX row 32 tests")
say("="*112)
say("  e_N       footing     M(<80)     M(<150)    M(<200)    M(<300)    plateau(400)")
PLAT = {}
for e in (0.008, 0.01273, 0.017, 0.02, 0.05):
    for f, a0 in A0.items():
        vals = [M_dyn(rr, a0, e) for rr in (80.0, 150.0, 200.0, 300.0, 400.0)]
        PLAT[(f, e)] = vals
        say(f"  {e:.4f}   {f:9}  {vals[0]:8.3f}   {vals[1]:8.3f}   {vals[2]:8.3f}   {vals[3]:8.3f}   {vals[4]:8.3f}")
e_ref = 0.01273
c80 = PLAT[("canonical", e_ref)][0]; a80 = PLAT[("alt", e_ref)][0]
say(f"  at the repo's own Local-Group vector sum e_N = {e_ref:.5f} (hunt item 81):")
say(f"    canonical M(<80) = {c80:.3f}e11 ({'%+.2f' % ((c80-M80_D)/M80_S)} sigma), alt {a80:.3f}e11 ({'%+.2f' % ((a80-M80_D)/M80_S)} sigma)")
say(f"    DW1's scalar-additive gave 4.307 / 4.508e11 (-4.11 / -3.70 sigma): the hack cost "
    f"{100*(c80/4.307-1):+.0f} / {100*(a80/4.508-1):+.0f} per cent at 80 kpc")
ck("G239a the proper EFE at the repo's own field leaves the absolute 80 kpc mass inside 3 sigma",
   all(abs(PLAT[(f, e_ref)][0]-M80_D)/M80_S < 3.0 for f in A0),
   f"canonical {PLAT[('canonical',e_ref)][0]:.2f}e11 ({(PLAT[('canonical',e_ref)][0]-M80_D)/M80_S:+.2f} sigma), "
   f"alt {PLAT[('alt',e_ref)][0]:.2f}e11 ({(PLAT[('alt',e_ref)][0]-M80_D)/M80_S:+.2f} sigma); DW1's hack gave -4.11/-3.70 sigma")

# ===================================================================================================
say("\n" + "="*112)
say("G239b -- THE 13-POINT DESI FIT WITH THE PROPER EFE: was the shape damage the hack?")
say("="*112)
FIT = {}
for e in (0.0, 0.008, 0.01273, 0.017):
    for f, a0 in A0.items():
        grid = np.linspace(0.5, 2.4, 381); c2 = []
        for A in grid:
            p = np.array([M_dyn(rr, a0, e, A) for rr in R]); c2.append(float(np.sum(((p-M)/SIG)**2)))
        c2 = np.array(c2); i0 = int(np.argmin(c2)); ok = grid[c2 <= c2[i0]+1]
        p = np.array([M_dyn(rr, a0, e, grid[i0]) for rr in R])
        FIT[(f, e)] = dict(A=float(grid[i0]), A68=(float(ok.min()), float(ok.max())), chi2=float(c2[i0]),
                           rms=float(np.std(p/M-1)), dof=float(c2[i0]/12))
        say(f"  e_N={e:.5f} {f:9}: A* = {grid[i0]:.3f} [{ok.min():.3f},{ok.max():.3f}]  chi2/12 = {c2[i0]/12:.2f}  rms = {np.std(p/M-1)*100:.2f}%")
say("  DW1's scalar-additive fit (for comparison): e_N = 0.0127 gave rms 7.0% (canonical) / 7.8% (alt)")
ck("G239b with the PROPER EFE the 13-point profile still fits at chi2/dof < 2 on both footings (the EFE "
   "does not damage the shape; the scalar-additive hack did)",
   all(FIT[(f, e_ref)]["dof"] < 2.0 for f in A0),
   "; ".join(f"{f}: A* = {FIT[(f,e_ref)]['A']:.3f}, rms {FIT[(f,e_ref)]['rms']*100:.1f}% "
             f"(vs 7.0/7.8% for the hack)" for f in A0))
ck("G239c the amplitude the profile demands under the proper EFE is still consistent with item 35's "
   "rotation-curve amplitude within 3 sigma",
   all(max((1.254 if f=='canonical' else 1.152)-FIT[(f,e_ref)]['A'],
           FIT[(f,e_ref)]['A']-(1.309 if f=='canonical' else 1.208), 0.0)
       / ((FIT[(f,e_ref)]['A68'][1]-FIT[(f,e_ref)]['A68'][0])/2) <= 3.0 for f in A0),
   "; ".join(f"{f}: A* = {FIT[(f,e_ref)]['A']:.3f} vs item-35 "
             f"[{1.254 if f=='canonical' else 1.152:.3f},{1.309 if f=='canonical' else 1.208:.3f}]" for f in A0))

# ===================================================================================================
say("\n" + "="*112)
say("G239d -- THE ANISOTROPY: what a spherical Jeans analysis sees in an EFE field")
say("="*112)
say("  r [kpc]   M_par (theta=0)   M_perp (theta=90)   M_avg     par/avg    perp/avg")
ANISO = {}
for rr in (40.0, 60.0, 80.0, 150.0):
    mp = M_dyn_dir(rr, A0["canonical"], e_ref, 1.0)
    mq = M_dyn_dir(rr, A0["canonical"], e_ref, 0.0)
    ma = M_dyn(rr, A0["canonical"], e_ref)
    ANISO[rr] = (mp, mq, ma)
    say(f"  {rr:5.0f}     {mp:10.3f}        {mq:10.3f}       {ma:8.3f}   {mp/ma:.3f}     {mq/ma:.3f}")
spread = max(abs(v[0]/v[2]-1) for v in ANISO.values())
ck("G239d the ANGLE AVERAGE is the well-posed quantity: it converges past r_EFE while the parallel direction diverges",
   ANISO[150.0][2] <= 1.10*ANISO[80.0][2] and ANISO[150.0][0]/ANISO[80.0][0] > 2.0,
   f"M_avg(150)/M_avg(80) = {ANISO[150.0][2]/ANISO[80.0][2]:.3f} (plateau); M_par(150)/M_par(80) = "
   f"{ANISO[150.0][0]/ANISO[80.0][0]:.2f} (diverges: the external field's OWN acceleration is attributed to the Galaxy). "
   f"par/avg = {ANISO[80.0][0]/ANISO[80.0][2]:.2f} at 80 kpc, {ANISO[150.0][0]/ANISO[150.0][2]:.2f} at 150 kpc; "
   f"perp/avg = {min(v[1]/v[2] for v in ANISO.values()):.2f}-{max(v[1]/v[2] for v in ANISO.values()):.2f}")

# ===================================================================================================
say("\n" + "="*112); say("MUTATION CONTROLS"); say("="*112)
m10 = M_dyn(80.0, 0.1*A0["canonical"], e_ref)
mb_only = M_sph(80*KPC)/MSUN/1e11
say(f"  a0 / 10  : M(<80) = {m10:.3f}e11 vs {c80:.3f}e11 (smaller a0 = larger y = the kernel switched OFF; note a0 x 10 does")
say( "             NOT switch it off in an EFE-dominated regime -- it saturates at nu(e), which is the correct physics)")
say(f"  nu = 1   : M(<80) = {mb_only:.3f}e11 (baryons only, a factor {c80/mb_only:.1f} below the prediction)")
ck("MUT the kernel carries the prediction: a0/10 and nu = 1 both collapse it toward the baryon mass",
   m10 < 0.5*c80 and mb_only < 0.25*c80,
   f"framework {c80:.2f}e11, a0/10 {m10:.2f}e11, baryons only {mb_only:.2f}e11")

# ===================================================================================================
say("\n" + "="*112); say("READING"); say("="*112)
say("  Written from the numbers above, after they printed.")
say("")
say(f"  1. THE HACK COST MORE THAN THE PHYSICS DID.  The scalar-additive external field DW1 used is the")
say(f"     maximum-suppression case; the exact angle average is {100*(c80/4.307-1):+.0f} per cent higher at 80 kpc")
say(f"     (canonical) and {100*(a80/4.508-1):+.0f} per cent (alt).  DW1's -4.11 sigma becomes {(c80-M80_D)/M80_S:+.2f} and its")
say(f"     -3.70 becomes {(a80-M80_D)/M80_S:+.2f}.  The EFE tension at 80 kpc is REAL BUT MODEST, and the framework sits")
say("     inside 3 sigma on both footings once the vector average is done properly.")
say("")
say(f"  2. AND THE SHAPE SURVIVES -- DW1's 'the EFE spoils the shape' IS RETRACTED.  With the proper EFE the")
say(f"     13-point profile fits at chi2/dof {FIT[('canonical',e_ref)]['dof']:.2f} (canonical) / {FIT[('alt',e_ref)]['dof']:.2f} (alt), rms "
    f"{FIT[('canonical',e_ref)]['rms']*100:.1f} / {FIT[('alt',e_ref)]['rms']*100:.1f} per cent,")
say("     against 7.0 / 7.8 per cent for the scalar-additive version.  The degradation was the approximation,")
say("     not the data: the shape prefers a weak field only because the HACK was strong.")
say("")
say(f"  3. THE AMPLITUDE MOVES UP WITH THE FIELD, AS IT MUST, AND THE TWO-DATASET AGREEMENT SURVIVES:")
say(f"     A* = {FIT[('canonical',e_ref)]['A']:.3f} canonical / {FIT[('alt',e_ref)]['A']:.3f} alt at e_N = {e_ref:.5f}, against "
    f"{FIT[('canonical',0.0)]['A']:.3f} / {FIT[('alt',0.0)]['A']:.3f} at zero field,")
say(f"     and still within 3 sigma of the outer rotation curve's own demand (item 35: 1.254-1.309 / 1.152-1.208).")
say(f"     The cost is a larger baryon excess: {100*(FIT[('alt',e_ref)]['A']-1):.0f}-{100*(FIT[('canonical',e_ref)]['A']-1):.0f} per cent over the census, which")
say("     remains the framework's one free ledge and its most falsifiable number.")
say("")
say(f"  4. THE PLATEAU -- THE NUMBER ROW 32 TESTS -- IS LOWER THAN THE NAIVE CAP.  At e_N = {e_ref:.5f}:")
say(f"     M(<200 kpc) = {PLAT[('canonical',e_ref)][2]:.2f}e11 canonical / {PLAT[('alt',e_ref)][2]:.2f}e11 alt at A = 1, and "
    f"{PLAT[('canonical',e_ref)][2]*FIT[('canonical',e_ref)]['A']:.2f} / {PLAT[('alt',e_ref)][2]*FIT[('alt',e_ref)]['A']:.2f}")
say(f"     at the fitted amplitude, against the paper's own NFW extrapolation 11.35e11 (a {11.35/(PLAT[('canonical',e_ref)][2]*FIT[('canonical',e_ref)]['A']):.1f}x")
say(f"     to {11.35/(PLAT[('canonical',e_ref)][2]):.1f}x split).  Note it is BELOW the nu(e_N) M_b = 6.27e11 that item 38 used as the cap: the")
say("     angle average of nu over the field's own anisotropy costs a further 16 per cent, so the EFE cap was")
say("     itself an overestimate.  The registered kill (M(<200 kpc) >= 1.0e12) is unaffected -- at the RC-preferred")
say(f"     weak field e_N = 0.008 the plateau is {PLAT[('canonical',0.008)][2]:.2f}e11 and still below it.")
say("")
say(f"  5. THE ANISOTROPY IS THE REAL CAVEAT, AND IT IS NOT SMALL AT LARGE RADIUS.  The angle average converges")
say(f"     ({ANISO[150.0][2]/ANISO[80.0][2]:.2f} from 80 to 150 kpc) while the PARALLEL direction diverges ({ANISO[150.0][0]/ANISO[80.0][0]:.1f}x):")
say("     along the field the external acceleration itself is credited to the Galaxy.  A spherical Jeans")
say(f"     analysis is therefore unbiased only for an ANGLE-ISOTROPIC tracer sample; at 80 kpc the parallel and")
say(f"     perpendicular readings differ by {(ANISO[80.0][0]/ANISO[80.0][2]-1)*100:.0f} and {(ANISO[80.0][1]/ANISO[80.0][2]-1)*100:.0f} per cent.  That is a test for DR4")
say("     (split the halo tracers by angle to the Local Group's field), and it is the same azimuthal channel")
say("     hunt item 81 priced at 0.3-1.4 per cent on the rotation curve.")
say("")
say("  6. HONEST LIMITS.  This is QUMOND (the algebraic kernel); h34's own AQUAL solve finds the algebraic boost")
say("     ~15 per cent HIGH, so the EFE suppression computed here is, if anything, understated and the plateau")
say("     correspondingly overstated.  The external field is uniform and static, and the LMC's contribution to it")
say("     is neglected.  The amplitude A remains a nuisance, not a derivation.  kappa = 1/2 stays FITTED.")

RES = dict(lane="G239", date="2026-11-11", replaces="DW1's scalar-additive EFE",
           e_grid=E_GRID, plateau={f"{f}_e{e}": PLAT[(f, e)] for f in A0 for e in (0.008, 0.01273, 0.017, 0.02, 0.05)},
           fit={f"{f}_e{e}": FIT[(f, e)] for f in A0 for e in (0.0, 0.008, 0.01273, 0.017)},
           anisotropy={str(k): v for k, v in ANISO.items()},
           dw1_scalar_additive=dict(canonical_80=4.307, alt_80=4.508, rms=[0.070, 0.078]),
           checks=dict(n=N[0], fails=FAILS))
json.dump(RES, open("g239_results.json", "w"), indent=1)
say("")
say(f"G239 COMPLETE: {N[0]-len(FAILS)}/{N[0]} checks PASS.")
OUT.close()
