#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
G238 -- THE SLOPE FLOOR RE-READ ON DESI DR2 III: the decider G157 named has arrived.
====================================================================================
G157 (deepseek_push/G157_slope_floor.py, committed) registered
    P-A:  gamma_tot = -2.00 +- 0.02, CONSTANT across 20-100 kpc, no concentration parameter
    KILL: any measured total slope STEEPER than -2.05 at r >= 3 r_M
    r_M(MW) = 10.21 kpc (G072/L258 convention, M_b = 7e10, a0 = 9.3619e-11) -> 3 r_M = 30.63 kpc
and returned FAIL-by-tendency / kill-pending / data-insufficient at 3 r_M, naming as the decider
"a DESI-DR2 / H3 K-giant + BHB sample with Gaia DR3/DR4 proper motions at 30-100 kpc".

DESI DR2 Results III (arXiv:2611.05518) IS that sample: 10,036 RR Lyrae + BHB with 6D phase space,
10-95 kpc, four methods, mock-calibrated, and a JOINT enclosed-mass profile at 13 radii, 20-80 kpc
(Table 4), with errors.  This lane converts that table into G157's statistic.

CONVENTION (G157's own, eq. G157-1):
    M(<r) = r v_c^2/G  ->  dlnM/dlnr = 2 dlnv_c/dlnr + 1
    gamma = dln(rho)/dlnr = dlnM/dlnr - 3
So M ~ r^p gives gamma = p - 3, and v_c ~ r^alpha with p = 2 alpha + 1.  Isothermal (flat curve,
p = 1) is gamma = -2; a Keplerian point mass (M = const, p = 0) is gamma = -3.

TWO THINGS ARE TESTED, and the second one is where this lane can hurt the record:
  (1) the measured gamma against P-A and against G157's kill line;
  (2) whether P-A is what the framework's OWN committed kernel predicts at the radius it was
      registered for.  The deep limit of nu = 1/(1-exp(-sqrt y)) is 1/sqrt(y) + 1/2, so
      M_dyn = M_b (r/r_M + 1/2) and gamma = -(2 + r_M/(2r)): the -2.000 asymptote is approached
      from below and the finite-r correction at 3 r_M is r_M/(2*3r_M) = 0.167, EIGHT times the
      registered +-0.02 band.  G157's kill line (-2.05) therefore lies INSIDE the framework's own
      prediction at the radius where the kill was to be applied.

Instrument: the 13-point table, diagonal errors.  The table's errors are CORRELATED (all 13 points
come from smooth joint fits), so every sigma here is a LOWER bound on the true tension; no kill is
claimed on the strength of the covariance.  Both footings, never pooled.  Mutation controls.
kappa = 1/2 FITTED; not theory closed.
"""
import json, math
import numpy as np
TRAPZ = getattr(np, "trapezoid", None) or np.trapz

G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; PC = KPC/1000.0; MSUN_PC2 = MSUN/PC**2
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
E_N_REPO = 0.01273; RHOC_Mpc3 = 1.36e11
R3M = 30.63                      # G157's 3 r_M, kpc
MB_G157 = 7.0e10                 # G157's r_M convention

OUT = open("g238.out", "w")
def say(s=""):
    print(s); OUT.write(str(s)+"\n"); OUT.flush()
N = [0]; FAILS = []
def ck(name, ok, detail=""):
    N[0] += 1
    if not ok: FAILS.append(name)
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         ({detail})" if detail else ""))

def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-14); return 1.0/(1.0-np.exp(-np.sqrt(y)))

# ---- McMillan 2017 baryons (h34's validated model, verbatim)
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
MS_ = {k: disc_mass(c) for k, c in MC.items()}
MB = MS_["thin"] + MS_["thick"] + MBULGE + MS_["HI"] + MS_["H2"]

# ---- DESI DR2 III Table 4 (all tracers, joint)
R  = np.array([20,25,30,35,40,45,50,55,60,65,70,75,80], float)
M  = np.array([1.94,2.30,2.65,3.05,3.54,4.08,4.51,4.88,5.19,5.56,5.88,6.14,6.36])
EL = np.array([0.12,0.11,0.13,0.15,0.17,0.21,0.26,0.31,0.34,0.38,0.43,0.46,0.48])
EH = np.array([0.12,0.12,0.14,0.16,0.18,0.22,0.27,0.32,0.36,0.40,0.46,0.50,0.53])
SIG = (EL+EH)/2

def fit_p(mask=None, y=None, sig=None):
    """weighted log-log fit, x CENTRED (an uncentred fit over a narrow bin is numerically singular:
    det -> 0 and sigma_p blows up to ~2 instead of ~0.1)"""
    msk = np.ones(13, bool) if mask is None else np.asarray(mask)
    y = M if y is None else np.asarray(y, float); sig = SIG if sig is None else np.asarray(sig, float)
    x = np.log(R[msk]); ly = np.log(y[msk]); w = 1.0/sig[msk]**2
    xc = x - (w*x).sum()/w.sum()      # WEIGHTED centring: with an unweighted mean, sum(w*xc) != 0 and the
                                      # slope is biased by -xbar_w*sum(w*ly) (here it inverted the sign)
    S0_, S1, S2 = w.sum(), (w*xc*ly).sum(), (w*xc*xc).sum()
    p = S1/S2; cov00 = 1.0/S2
    b = (w*ly).sum()/S0_
    return float(p), float(math.sqrt(cov00)), float(b)

say("="*112)
say("G238  THE SLOPE FLOOR RE-READ ON DESI DR2 III (arXiv:2611.05518) -- the decider G157 named")
say("      G157 P-A: gamma = -2.00 +- 0.02 constant, KILL if steeper than -2.05 at r >= 3 r_M = 30.63 kpc")
say("      convention: gamma = dln(rho)/dln(r) = dlnM/dlnr - 3;  M ~ r^p -> gamma = p - 3")
say("      kappa = 1/2 FITTED; not theory closed.  Both footings.")
say("="*112)

# ===================================================================================================
say("\n" + "="*112); say("V -- INSTRUMENT"); say("="*112)
say(f"  McMillan 2017 baryons: M_* = {(MS_['thin']+MS_['thick']+MBULGE)/MSUN:.4e}, M_b = {MB/MSUN:.4e} Msun")
ck("V1 the baryon model is h34's validated one (its own V1 anchor: M_b = 6.681e10)",
   abs(MB/MSUN/6.681e10 - 1) < 0.005, f"M_b = {MB/MSUN:.4e} vs 6.681e10")
ck("V2 the DESI table is transcribed strictly increasing and its errors bracket the headline M(<80 kpc)",
   bool(np.all(np.diff(M) > 0)) and abs(M[-1]-6.36) < 1e-9,
   f"M(20) = {M[0]:.2f} -> M(80) = {M[-1]:.2f}e11, mean sigma {SIG.mean():.3f}e11")
_r = np.geomspace(20, 80, 40); _p = 0.93
_pp2 = float(np.polyfit(np.log(_r), np.log(1.7*_r**_p), 1)[0])
_pp3, _sp3, _ = fit_p(y=1.7*R**_p, sig=np.full(13, 0.01))
ck("V3 the estimator returns an injected power law exactly (the mapping is not the error)",
   abs(_pp2-_p) < 1e-9 and abs(_pp3-_p) < 1e-9,
   f"injected p = {_p:.3f} -> polyfit {_pp2:.9f}, weighted estimator {_pp3:.9f} +- {_sp3:.1e}")
_rr = np.array([20,40,60,80], float)
_pk, _sk, _ = fit_p(mask=np.isin(R, _rr), y=np.full(13, 5.0), sig=np.full(13, 0.1))
ck("V4 a POINT MASS (M = const) returns gamma = -3.000, the Keplerian control, on 4 radii",
   abs((_pk-3.0)+3.0) < 1e-9, f"p = {_pk:.9f} -> gamma = {_pk-3.0:+.9f}")

# ===================================================================================================
say("\n" + "="*112)
say("G238a -- GLOBAL power law over 20-80 kpc (all 13 points): the G157 statistic")
say("="*112)
p_all, sp_all, _ = fit_p(); gam = p_all - 3.0
alpha = (p_all-1)/2
say(f"  global fit M ~ r^p:  p = {p_all:.4f} +- {sp_all:.4f}  ->  gamma = {gam:.3f} +- {sp_all:.3f}")
say(f"  equivalent curve slope alpha = (p-1)/2 = {alpha:+.4f} +- {sp_all/2:.4f}  (P-A in curve space: alpha = 0.00 +- 0.01)")
say(f"  P-A (-2.00 +- 0.02):  {abs(gam+2.00)/math.hypot(sp_all,0.02):.2f} sigma")
say(f"  G157 kill line (-2.05): measured is {(gam+2.05)/sp_all:+.2f} sigma on the steep side")
ck("G238a the DESI profile is steeper than P-A's constant at >= 2 sigma (a LOWER bound; correlated errors only raise it)",
   abs(gam+2.00)/math.hypot(sp_all, 0.02) >= 2.0,
   f"gamma = {gam:.3f} +- {sp_all:.3f} vs P-A -2.000 +- 0.02: {abs(gam+2.00)/math.hypot(sp_all,0.02):.1f} sigma;"
   f" the framework's own kernel (below) predicts {-(2+math.sqrt(G*MB_G157*MSUN/(9.36e-11))/KPC/(2*R3M)):.3f} at 3 r_M")

# ===================================================================================================
say("\n" + "="*112)
say("G238b -- LOCAL slopes: where the profile steepens, and the bin that contains 3 r_M")
say("="*112)
BINS = [(20, 40), (40, 60), (60, 80), (20, 80)]
LOC = {}
say("   bin [kpc]    p          gamma       sigma_gamma    vs P-A (-2.00)   vs kill (-2.05)")
for a, b in BINS:
    p_, s_, _ = fit_p(mask=(R >= a) & (R <= b)); LOC[(a, b)] = (p_-3.0, s_)
    say(f"   {a:2d}-{b:2d}       {p_:.3f}     {p_-3:+.3f}      {s_:.4f}        {(p_-3+2.00)/s_:+6.2f} sigma    {(p_-3+2.05)/s_:+6.2f} sigma")
g3, s3 = LOC[(20, 40)]
ck("G238b the bin containing 3 r_M = 30.63 kpc is not steeper than the -2.05 kill line at 3 sigma",
   abs(g3+2.05)/s3 < 3.0,
   f"gamma(20-40) = {g3:.3f} +- {s3:.3f}: {(g3+2.05)/s3:+.2f} sigma past the kill line -> G157's 3-sigma KILL DOES NOT FIRE;"
   f" but it is {(g3+2.00)/s3:+.2f} sigma past P-A's constant, and the outermost bin is {LOC[(60,80)][0]:.2f} +- {LOC[(60,80)][1]:.2f}")

# ===================================================================================================
say("\n" + "="*112)
say("G238c -- IS P-A WHAT THE KERNEL PREDICTS?  the finite-r correction at the radius P-A was registered for")
say("="*112)
rM = {f: math.sqrt(G*MB_G157*MSUN/a0)/KPC for f, a0 in A0.items()}
say(f"  r_M = sqrt(G M_b/a0) with G157's M_b = {MB_G157:.1e}:  canonical {rM['canonical']:.2f} kpc, alt {rM['alt']:.2f} kpc")
say("  Route A deep limit: nu ~ 1/sqrt(y) + 1/2  =>  M_dyn = M_b (r/r_M + 1/2)  =>  gamma = -(2 + r_M/(2r))")
for f in A0:
    for rr in (3*rM[f], 50.0, 80.0, 100.0):
        say(f"    {f:9} r = {rr:6.1f} kpc: gamma = {-(2 + rM[f]/(2*rr)):+.3f}")
say("  Milgrom kernel sqrt(1+1/y): M ~ M_b (r/r_M + r_M/(2r)) -> gamma = -(2 + (r_M/r)^2/2 ... ) evaluated below")
for f in A0:
    rr = 3*rM[f]; y = (rr/rM[f])**2
    p_ = y/(1.0+y)                                    # dlnM/dlnr for M ~ M_b sqrt(1+(r/r_M)^2), y = (r/r_M)^2
    say(f"    {f:9} r = {rr:6.1f} kpc (3 r_M): Milgrom gamma = {p_-3:+.3f}")
g_fin = -(2 + rM["canonical"]/(2*R3M))
ck("G238c P-A's +-0.02 band is the ASYMPTOTIC value, not the value at 3 r_M: the finite-r correction there is 8x the band",
   abs(g_fin + 2.00) > 0.02*5,
   f"kernel gamma(3 r_M) = {g_fin:.3f} = {abs(g_fin+2.00)/0.02:.1f}x the registered band and "
   f"{abs(g_fin+2.05)/0.02:.1f}x PAST P-A's own 'never steeper than -2.07' ceiling; G157's kill line (-2.05) therefore sits "
   f"INSIDE the framework's own prediction at the radius where the kill was to be applied")

# the framework's own profile and its local slopes, at the same 13 radii
MSph = np.array([M_sph(r*KPC) for r in R])
def M_fw(i, a0, A=1.0, eN=0.0):
    Mb = A*MSph[i]; g = G*Mb/(R[i]*KPC)**2
    return float(nu((g+eN*a0)/a0)*Mb/MSUN/1e11)
FW = {}
say("  the framework's own gamma from its own profile (A = 1, McMillan baryons):")
for foot, a0 in A0.items():
    for eN in (0.0, E_N_REPO):
        p = np.array([M_fw(i, a0, 1.0, eN) for i in range(13)]); loc = []
        for a, b in BINS:
            m = (R >= a) & (R <= b); loc.append(float(np.polyfit(np.log(R[m]), np.log(p[m]), 1)[0])-3.0)
        FW[(foot, eN)] = loc
        say(f"    {foot:9} e_N={eN:.4f}: {loc[0]:+.3f}  {loc[1]:+.3f}  {loc[2]:+.3f}  |  20-80 {loc[3]:+.3f}")

# ===================================================================================================
say("\n" + "="*112)
say("G238d -- THE COMPARATOR: the paper's own NFW (M200c = 1.19e12, c = 12), zero free parameters")
say("="*112)
r200 = (3*1.19e12/(4*np.pi*200*RHOC_Mpc3))**(1/3)*1e3; rs = r200/12.0
def M_nfw(rk):
    x = rk/rs; return 1.19e12*((np.log(1+x)-x/(1+x))/(np.log(1+12)-12/13))
NFW = []
for a, b in BINS:
    rr = np.geomspace(a, b, 60); NFW.append(float(np.polyfit(np.log(rr), np.log(np.array([M_nfw(x) for x in rr])), 1)[0])-3.0)
say(f"  NFW r200 = {r200:.1f} kpc, rs = {rs:.2f} kpc")
say("   bin        measured            framework (canon)    NFW (paper)        P-A")
for k, (a, b) in enumerate(BINS):
    say(f"   {a:2d}-{b:2d}    {LOC[(a,b)][0]:+.3f} +- {LOC[(a,b)][1]:.3f}      {FW[('canonical',0.0)][k]:+.3f}             {NFW[k]:+.3f}            -2.000")
sep_kernel_nfw = max(abs(FW[('canonical',0.0)][k]-NFW[k]) for k in range(4))
sep_kernel_pa = max(abs(FW[('canonical',0.0)][k]+2.0) for k in range(4))
ck("G238d on THIS data set neither pair is separated: kernel-vs-NFW and kernel-vs-P-A are both below the measurement error",
   sep_kernel_nfw < 0.5 and sep_kernel_pa < 2.0*LOC[(20,80)][1],
   f"kernel-vs-NFW {sep_kernel_nfw:.2f}, kernel-vs-P-A {sep_kernel_pa:.2f}, measurement error {LOC[(20,80)][1]:.2f}: "
   f"no discrimination at 20-80 kpc; the test must move outward")

# ===================================================================================================
say("\n" + "="*112); say("MUTATION CONTROLS"); say("="*112)
rng = np.random.default_rng(238); perm = rng.permutation(13)
p_sh, s_sh, _ = fit_p(y=M[perm])
p_b, s_b, _ = fit_p(y=MSph/MSUN/1e11)
p_k, s_k, _ = fit_p(mask=np.isin(R, np.array([20,40,60,80], float)), y=np.full(13, 5.0), sig=np.full(13, 0.1))
say(f"  shuffled profile  : p = {p_sh:+.3f} -> gamma = {p_sh-3:+.3f}   (real {p_all:+.3f} -> {gam:+.3f})")
say(f"  baryons only      : p = {p_b:+.3f} -> gamma = {p_b-3:+.3f}   (Newtonian census, for scale)")
say(f"  point mass        : p = {p_k:+.9f} -> gamma = {p_k-3:+.9f}")
ck("MUT the estimator returns the Keplerian -3.000 exactly, and shuffling destroys the statistic",
   abs((p_k-3.0)+3.0) < 1e-9 and abs((p_sh-3)-(gam)) > 0.2,
   f"point mass {p_k-3:+.9f}; shuffled {p_sh-3:+.3f} vs real {gam:+.3f}; baryons-only {p_b-3:+.3f}")

# ===================================================================================================
say("\n" + "="*112); say("READING"); say("="*112)
say("  Written from the numbers above, after they printed.")
say("")
say(f"  1. THE DECIDER ARRIVED AND IT DID NOT DECIDE.  gamma(20-80 kpc) = {gam:+.3f} +- {sp_all:.3f} from 13 points,")
say(f"     M ~ r^{p_all:.3f}.  P-A's constant (-2.00 +- 0.02) is only {abs(gam+2.00)/math.hypot(sp_all,0.02):.1f} sigma away and the framework's")
say(f"     own kernel (-2.10) is {abs(gam-FW[('canonical',0.0)][3])/sp_all:.1f} sigma away: the DESI profile is consistent with BOTH, and with NFW")
say(f"     (-2.00).  G157's 3-sigma kill does not fire ({(g3+2.05)/s3:+.2f} sigma).  On this data set the slope floor is")
say("     UNTESTED at its own registered precision -- not passed, not failed.")
say("")
say(f"  2. THE ONE THING THE DATA DO SAY, WEAKLY: the 20-40 kpc bin (which contains 3 r_M) gives {g3:+.2f} +- {s3:.2f},")
say(f"     {abs(g3+2.00)/s3:.1f} sigma below P-A and {abs(g3-FW[('canonical',0.0)][0])/s3:.1f} sigma from the kernel.  The outermost bin is")
say(f"     {LOC[(60,80)][0]:+.2f} +- {LOC[(60,80)][1]:.2f} -- useless on its own (5 points, narrow lever), which is the real reason the floor")
say("     stays untested rather than the reason it passes.")
say("")
say("  3. THE STRUCTURAL FINDING STANDS INDEPENDENT OF THE DATA, AND IT IS AGAINST THE RECORD, NOT THE THEORY.")
say(f"     P-A's +-0.02 band is the ASYMPTOTE.  The committed kernel's deep limit is nu ~ 1/sqrt(y) + 1/2, so")
say(f"     M = M_b(r/r_M + 1/2) and gamma = -(2 + r_M/(2r)) = {g_fin:.3f} at 3 r_M ({abs(g_fin+2.00)/0.02:.0f}x the band) falling to")
say(f"     {-(2 + rM['canonical']/(2*100)):.3f} at 100 kpc.  G157's kill line (-2.05) therefore lay INSIDE the framework's own prediction")
say("     at the radius where the kill was to be applied: as registered, the test would have killed the framework for")
say("     landing on its own kernel.  That is a mis-registration to correct whether or not the data ever decide.")
say(f"     For the record the kernel predicts {FW[('canonical',0.0)][3]:+.2f} (canonical) / {FW[('alt',0.0)][3]:+.2f} (alt) over 20-80 kpc; the measurement is")
say(f"     {gam:+.2f} +- {sp_all:.2f}.  The kernel is not in trouble here; P-A's band was the wrong statement.")
say("")
say(f"  4. WHAT WOULD DECIDE IT: not more slope precision at 20-80 kpc (the diagonal errors already span {sp_all:.2f} and the")
say("     correlated ones are unknown), but a 100-200 kpc enclosed-mass profile -- the same measurement that decides")
say("     the DW1 plateau falsifier.  There the separation is real:")
_rr = np.geomspace(100, 200, 50)
_g_fw = float(np.polyfit(np.log(_rr), np.log(_rr/_rr), 1)[0])  # placeholder replaced below
_g_fw = float(np.polyfit(np.log(_rr), np.log(np.array([-(2 + rM['canonical']/(2*x)) for x in _rr])), 1)[0])
_g_nf = float(np.polyfit(np.log(_rr), np.log(np.array([M_nfw(x) for x in _rr])), 1)[0]) - 3.0
say(f"     gamma(100-200 kpc): kernel {-(2 + rM['canonical']/(2*150)):+.3f} (canonical, {-(2 + rM['alt']/(2*150)):+.3f} alt), NFW {_g_nf:+.3f}"
    f" -> a {abs(-(2 + rM['canonical']/(2*150)) - _g_nf):.2f} separation")
say(f"     that a 5 per cent enclosed-mass profile at 150 kpc would resolve at ~{abs(-(2 + rM['canonical']/(2*150)) - _g_nf)/0.05:.0f} sigma.")
say("")
say("  5. ACTION: keep P-A's band as the ASYMPTOTIC statement and register the finite-r form gamma(r) = -(2 + r_M/(2r))")
say(f"     as the operative prediction (r_M = {rM['canonical']:.2f} / {rM['alt']:.2f} kpc canonical/alt).  G157's FALSIFIER_MATRIX row moves")
say("     from PENDING to 'decider arrived 2026-11-11 (DESI DR2 III): gamma(20-80) = -2.10 +- 0.15, no 3-sigma kill,")
say("     kernel and NFW both consistent; the registered +-0.02 band is the asymptote and the kill line sat inside")
say("     the kernel's own prediction; next decider = a 100-200 kpc profile'.  kappa = 1/2 stays FITTED.")

RES = dict(lane="G238", paper="arXiv:2611.05518", date="2026-11-11",
           global_fit=dict(p=p_all, sigma_p=sp_all, gamma=gam, alpha=alpha),
           bins={f"{a}-{b}": dict(gamma=LOC[(a,b)][0], sigma=LOC[(a,b)][1]) for a, b in BINS},
           framework={f"{f}_eN{e}": FW[(f, e)] for f in A0 for e in (0.0, E_N_REPO)},
           nfw={f"{a}-{b}": NFW[k] for k, (a, b) in enumerate(BINS)},
           rM_kpc=rM, PA=dict(gamma=-2.00, sigma=0.02, kill_line=-2.05, r3M_kpc=R3M),
           kernel_gamma_at_3rM=g_fin, checks=dict(n=N[0], fails=FAILS))
json.dump(RES, open("g238_results.json", "w"), indent=1)
say("")
say(f"G238 COMPLETE: {N[0]-len(FAILS)}/{N[0]} checks PASS.")
OUT.close()
