#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L342 -- THE BOUND-REGION SWITCH: MOND acts where the preferred leaves curve faster than they expand.  One geometric
scalar of C-H/K's own foliation repairs its FRW failure (L341), leaves galaxies, the Solar System and wide binaries
untouched, and IMPROVES the KiDS-1000 lensing fit.

THE SWITCH.  L341 showed C-H/K needs a variable that knows whether matter has decoupled from the Hubble flow, and
that its foliation is CMC-stiff (K = 3H everywhere, delta K = 0 for static sources).  The stiffness is what makes
the following work: the ratio of the leaves' intrinsic curvature to their extrinsic curvature squared,
        x = 9 R3 / (4 K^2),
is built from the clock alone.  On the flat FRW background R3 = 0, so x = 0 (MOND off in the early universe); at
linear order the Hamiltonian constraint gives x = (3/2) Omega_m(z) delta (off in the linear web); in a static bound
system R3 = 16 pi G rho_dyn/c^2 with rho_dyn the phantom-inclusive density and K = 3H, so x = 4 pi G rho_dyn/H^2
(>> 1 in galaxies).  C-H/K's MOND term 2 alpha^2 q(...) is multiplied by f(x): f = 0 for x < x_c, f = 1 for x > x_c.

WHAT THIS LANE CHECKS (reuses L340's kernel nu_mono, L341's growth machinery, f21's SPARC bins, B21 KiDS data)
  B1 THE GEOMETRY (symbolic): flat FRW has R3 = 0; with delta K = 0 (L341 F5) the linearised Hamiltonian constraint
     gives x = (3/2) Omega_m delta; a static weak field gives x = 4 pi G rho_dyn/H^2.
  B2 LINEAR COSMOLOGY IS REPAIRED: with the switch, sigma_8 returns to LCDM (0.81); L341's unswitched value 18-27 is
     reproduced as the control.
  B3 GALAXIES AND THE SOLAR SYSTEM ARE UNTOUCHED: at every SPARC point x >= 1e2 x_c; in the Solar neighbourhood
     x ~ 1e6; wide binaries likewise.
  B4 KiDS-1000 SELECTS THE THRESHOLD: the lensing rotation curves of four stellar-mass bins (full covariance, M_b free
     per bin) prefer x_c ~ 4-7 over no switch by Delta chi^2 ~ -11..-19 (both footings; best x_c = 5), and exclude x_c >= 15
     (+41..+112).  x_c ~ 4-7 is the turnaround scale of spherical collapse, not a tuned number.
  B5 HEALTH: inside bound regions f = 1 and f' = 0, so L340's block is unchanged; in the switching shell the induced
     K^2 coefficient ~ 2 alpha^2 q x^2 f''/K^2 is ~1e-14, far below c_2 = 7.3e-3.
  B6 THE PREDICTION: every galaxy's lensing phantom ends at r_t = v_flat/(sqrt(x_c) H(z)) -- ~1 Mpc for the Milky
     Way today, proportional to M_b^(1/4) and shrinking as 1/H(z) at high redshift (still >> galaxy discs, so the
     flat-a0(z) Tully-Fisher prediction is untouched).
  MUTATE=1 removes the switch (x_c = 0): B2 must FAIL (sigma_8 back to ~20, rc = 1).

SCOPE AND WHAT IS STILL MISSING.  The switch is a construction (one new number, x_c), not a derivation.  The KiDS
improvement sits on a poor base fit (chi^2 ~ 118/60; point-mass baryons, no 2-halo, no external field) -- a lead.
The switch uses the dynamical density, so the outskirts are bistable (MOND-on and MOND-off are both self-consistent
where only the phantom exceeds the threshold); which branch forms is a dynamical question for the lambda-channel.
The dark sector is NOT solved: the CMB still needs a cold fluid, and any cold fluid left inside galaxies is
amplified by MOND there (L321).

Run from the repository root:  python3 real_research/g03_audit_2026/L342_bound_region_switch.py
"""
import os, sys, json, math, time, warnings
warnings.filterwarnings("ignore", message=".*encountered in matmul.*"); warnings.filterwarnings("ignore", category=DeprecationWarning)
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L342_bound_region_switch"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L342", "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()
def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok
def banner(t): P("\n" + "=" * 104); P(t); P("=" * 104)
P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: no switch (x_c = 0); B2 must FAIL ***")
XC = 0.0 if MUTATE else 5.0            # the working threshold (inside KiDS's preferred 4-7)

# ---------------------------------------------------------------------------------------- constants, kernel
c = 2.99792458e8; Mpc = 3.0856775814913673e22; G = 6.67430e-11
h = 0.6736; om_b, om_c = 0.02237, 0.1200; T_CMB = 2.7255; N_eff = 3.046; ns = 0.965
H0 = 100*h*1e3/Mpc; rho_crit0 = 3*H0**2/(8*math.pi*G)
Og = (4*5.670374419e-8*T_CMB**4/c**3)/rho_crit0; Or = Og*(1 + N_eff*(7/8)*(4/11)**(4/3))
Ob, Oc = om_b/h**2, om_c/h**2; Om = Ob + Oc; OL = 1 - Om - Or
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}; SIG8 = 0.811
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"): return np.where(y < 1e4, y/np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6): return (h_rar(y*(1 + e)) - h_rar(y*(1 - e)))/(2*y*e)
YP = brentq(lambda y: float(dh_rar(y)), 1, 5); HP = float(h_rar(YP))
LYG = np.linspace(-14, 14, 280001); YG = 10**LYG; DH = np.maximum(dh_rar(YG), 0.05*HP/(YG + YP))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5*(DH[1:] + DH[:-1])*np.diff(YG))])
def nu_mono(y): y = max(float(y), 1e-14); return 1.0 + float(np.interp(math.log10(y), LYG, HM))/y
nu_arr = np.vectorize(nu_mono)

# ============================================================================================ B1 geometry
banner("B1  THE SWITCH VARIABLE x = 9 R3/(4 K^2): FRW, linear, static (symbolic)")
Hs, rhob, dl, Gs, cs_, dK = sp.symbols('H rho_bar delta G c deltaK', positive=True)
Kbar = 3*Hs/cs_
# linearised Hamiltonian constraint on flat FRW:  dR3 + (4/3) Kbar dK = 16 pi G drho / c^2  (R3bar = 0, Kbar^2 = 24 pi G rho_bar / c^2)
fried = sp.Eq(Kbar**2, 24*sp.pi*Gs*rhob/cs_**2)
dR3 = 16*sp.pi*Gs*rhob*dl/cs_**2 - sp.Rational(4, 3)*Kbar*dK
x_lin = sp.simplify((9*dR3/(4*Kbar**2)).subs(dK, 0))
Omega_m = sp.symbols('Omega_m', positive=True)
x_lin_Om = sp.simplify(x_lin.subs(rhob, Omega_m*3*Hs**2/(8*sp.pi*Gs)))
rhod = sp.symbols('rho_dyn', positive=True)
x_static = sp.simplify(9*(16*sp.pi*Gs*rhod/cs_**2)/(4*Kbar**2))
P(f"    flat FRW background: R3 = 0 -> x = 0;  Friedmann (Hamiltonian constraint): {fried}")
P(f"    linear, delta K = 0 (L341 F5): x = {x_lin} = {x_lin_Om}")
P(f"    static weak field (R3 = 16 pi G rho_dyn / c^2, K = 3H/c): x = {x_static}")
check("B1 x = 0 on the FRW background, x = (3/2) Omega_m delta at linear order, x = 4 pi G rho_dyn / H^2 in a static system",
      f"linear {x_lin_Om}; static {x_static}", sp.simplify(x_lin_Om - sp.Rational(3, 2)*Omega_m*dl) == 0 and
      sp.simplify(x_static - 4*sp.pi*Gs*rhod/Hs**2) == 0)

# ============================================================================================ B2 linear cosmology
banner("B2  LINEAR COSMOLOGY WITH THE SWITCH (L341's growth machinery, the CMB's cold fluid present)")
def T_EH98(k):
    th = T_CMB/2.7; s = 44.5*math.log(9.83/(Om*h*h))/math.sqrt(1 + 10*om_b**0.75)
    ag = 1 - 0.328*math.log(431*Om*h*h)*(Ob/Om) + 0.38*math.log(22.3*Om*h*h)*(Ob/Om)**2
    ge = Om*h*(ag + (1 - ag)/(1 + (0.43*k*s/h)**4)); q = k*th*th/ge
    L = math.log(2*math.e + 1.8*q); Cc = 14.2 + 731.0/(1 + 62.5*q); return L/(L + Cc*q*q)
def P_un(kh): k = kh*h; return k**ns*T_EH98(k)**2
def Wth(x): return 3*(math.sin(x) - x*math.cos(x))/x**3
PN = (SIG8/math.sqrt(quad(lambda kh: kh**2*P_un(kh)*Wth(8*kh)**2/(2*math.pi**2), 1e-4, 60, limit=600)[0]))**2
def Delta_lin0(kh): return math.sqrt(kh**3*PN*P_un(kh)/(2*math.pi**2))
KH = np.logspace(math.log10(0.02), math.log10(20.0), 48); DREF = np.array([Delta_lin0(k) for k in KH])
def sigma8_of(D0): return math.sqrt(np.trapz([D0[i]**2*Wth(8*KH[i])**2 for i in range(len(KH))], np.log(KH)))
def growth(xc, foot="canonical", mode="rms", z_i=1000.0):
    om = Om; ol = 1 - om - Or; a_i = 1/(1 + z_i); a0 = A0[foot]
    Ez = lambda a: math.sqrt(Or/a**4 + om/a**3 + ol); dlnH = lambda a: 0.5*(-4*Or/a**4 - 3*om/a**3)/Ez(a)**2
    r0 = solve_ivp(lambda N, Y: [Y[1], 1.5*(om/math.exp(3*N)/Ez(math.exp(N))**2)*Y[0] - (2 + dlnH(math.exp(N)))*Y[1]],
                   (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14).y[0][-1]
    Di = DREF/r0
    def boost(y, a, dlt):
        Omz = om/a**3/Ez(a)**2
        return nu_mono(y) if 1.5*Omz*abs(dlt) >= xc else 1.0         # the switch: x = (3/2) Omega_m(z) |delta|
    if mode == "rms":
        def rhs(N, Y):
            a = math.exp(N); D, Dp = Y; rho = om*rho_crit0/a**3
            gk = 4*math.pi*G*rho*np.abs(Di*D)/(KH*h/(a*Mpc)); grms = math.sqrt(np.trapz(gk**2/KH, KH)/np.trapz(1/KH, KH))
            drms = math.sqrt(np.trapz((Di*D)**2/KH, KH)/np.trapz(1/KH, KH))
            return [Dp, 1.5*(om/a**3/Ez(a)**2)*boost(grms/a0, a, drms)*D - (2 + dlnH(a))*Dp]
        return Di*solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-7, atol=1e-12).y[0][-1]
    out = []
    for i, kh in enumerate(KH):
        def rhs(N, Y, kh=kh):
            a = math.exp(N); d, dp = Y; gN = 4*math.pi*G*om*rho_crit0/a**3*abs(d)/(kh*h/(a*Mpc))
            return [dp, 1.5*(om/a**3/Ez(a)**2)*boost(gN/a0, a, d)*d - (2 + dlnH(a))*dp]
        out.append(solve_ivp(rhs, (math.log(a_i), 0.0), [Di[i], Di[i]], method="LSODA", rtol=1e-7, atol=1e-22).y[0][-1])
    return np.array(out)
B2 = {}
for foot in ("canonical", "alt"):
    for mode in ("rms", "permode"):
        B2[(foot, mode, "switch")] = sigma8_of(growth(XC, foot, mode))
        B2[(foot, mode, "none")] = sigma8_of(growth(0.0, foot, mode))
        P(f"    {foot:9s} {mode:7s}: sigma_8 with the switch (x_c = {XC}) = {B2[(foot, mode, 'switch')]:.4f};  without (L341) = {B2[(foot, mode, 'none')]:.2f}")
sw = [v for k_, v in B2.items() if k_[2] == "switch"]; nsw = [v for k_, v in B2.items() if k_[2] == "none"]
check("B2 with the switch linear growth returns to LCDM (sigma_8 within 2% of 0.811, both footings, both field arguments); "
      "without it the L341 overshoot (> 10x) is reproduced", f"switched {min(sw):.3f}-{max(sw):.3f}; unswitched {min(nsw):.1f}-{max(nsw):.1f}",
      all(abs(v/SIG8 - 1) < 0.02 for v in sw) and min(nsw) > 10*SIG8,
      "the per-mode switch here keys on the mode's own linear delta; the rms run keys on the rms delta")

# ============================================================================================ B3 galaxies, Solar System
banner("B3  GALAXIES, THE SOLAR SYSTEM AND WIDE BINARIES ARE UNTOUCHED (x >> x_c)")
sys.path.insert(0, os.path.join(REPO, "hunt_2026")); cwd = os.getcwd(); os.chdir(os.path.join(REPO, "hunt_2026"))
from hunt_lib import load_sparc
gals = load_sparc(); os.chdir(cwd)
KPC = 3.0857e19; xs = []
for g_ in gals:
    r = np.asarray(g_["r"])*KPC; go = np.asarray(g_["gobs"])
    if len(r) < 3: continue
    rho = np.gradient(r**2*go, r)/(4*math.pi*G*r**2)                  # dynamical density from the observed field
    rho = np.maximum(rho, go/(4*math.pi*G*r)*0.5)                        # guard noisy outer derivatives (isothermal floor)
    xs.append(float((4*math.pi*G*rho/H0**2)[-1]))
MSUNPC3 = 1.98892e30/(3.0857e16)**3
x_sun = 4*math.pi*G*0.1*MSUNPC3/H0**2
P(f"    SPARC outermost points: min x = {min(xs):.3g}, median {np.median(xs):.3g} (x_c = {XC});  Solar neighbourhood (0.1 Msun/pc^3): x = {x_sun:.2e}")
OUT["numbers"]["B3"] = {"sparc_min_x": min(xs), "sparc_median_x": float(np.median(xs)), "x_sun": x_sun}
check("B3 every SPARC galaxy's outermost measured point, the Solar neighbourhood and hence wide binaries sit at x >= 100 x_c: "
      "the switch is saturated (f = 1, f' = 0) wherever the record's galaxy and local gates live",
      f"SPARC min x = {min(xs):.0f}; Solar nbhd {x_sun:.1e}", min(xs) > 100*max(XC, 5.0) and x_sun > 1e5)

# ============================================================================================ B4 KiDS
banner("B4  KiDS-1000 (Brouwer+2021 lensing rotation curves) SELECTS THE THRESHOLD")
B = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
MS, PCm = 1.98892e30, 3.0857e16; MPCm = PCm*1e6
Rd, Ed, Sd = [], [], []
for b in (1, 2, 3, 4):
    d = np.genfromtxt(os.path.join(B, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt"), comments="#")
    Rd.append(d[:, 0]); Ed.append(d[:, 1]/d[:, 4]); Sd.append(d[:, 3]/d[:, 4])
cv = np.genfromtxt(os.path.join(B, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"), comments="#")
vv = cv[:, 4]/cv[:, 6]; npb = len(Rd[0]); Cf = vv.reshape(4, 4, npb, npb).transpose(0, 2, 1, 3).reshape(4*npb, 4*npb)
Ci = np.linalg.inv((Cf + Cf.T)/2)
rr = np.geomspace(1e-3, 30, 4000)*MPCm; Rp = np.geomspace(0.02, 4, 240)*MPCm
Hlens = H0*math.sqrt(Om*1.25**3 + OL)                                   # lens redshift ~0.25
def esd(Mb, a0, xc):
    M = Mb*nu_arr(G*Mb/rr**2/a0)
    if xc:
        rho_dyn = np.gradient(M, rr)/(4*math.pi*rr**2); on = 4*math.pi*G*rho_dyn/Hlens**2 >= xc
        it = int(np.where(on)[0].max()) if on.any() else 0
        M = np.where(np.arange(len(rr)) > it, M[it], M)
    rho = np.gradient(M - Mb, rr)/(4*math.pi*rr**2); Sig = np.zeros_like(Rp)
    for i, Rv in enumerate(Rp):
        m = rr > Rv*1.0000001; r_ = rr[m]; Sig[i] = 2*np.trapz(rho[m]*r_/np.sqrt(r_**2 - Rv**2), r_)
    Mc = np.concatenate([[0], np.cumsum(0.5*(Sig[1:]*Rp[1:] + Sig[:-1]*Rp[:-1])*np.diff(Rp))])*2*math.pi + math.pi*Rp[0]**2*Sig[0]
    return Rp/MPCm, (Mc/(math.pi*Rp**2) - Sig + Mb/(math.pi*Rp**2))*PCm**2/MS
LM = np.linspace(9.8, 11.8, 21)
B4 = {}
for foot in ("canonical", "alt"):
    a0 = A0[foot]
    for xc in (0.0, 2.0, 4.0, 5.0, 7.0, 15.0, 30.0):
        mods = []
        for b in range(4):
            best = None
            for lm in LM:
                Rq, dS = esd(10**lm*MS, a0, xc); mk = np.interp(Rd[b], Rq, dS); c_ = float(np.sum(((Ed[b] - mk)/Sd[b])**2))
                if best is None or c_ < best[0]: best = (c_, mk)
            mods.append(best[1])
        dv = np.concatenate(Ed) - np.concatenate(mods); B4[(foot, xc)] = float(dv @ Ci @ dv)
    P(f"    {foot:9s}: chi^2 no switch {B4[(foot, 0.0)]:.1f};  Delta chi^2 at x_c = 2/4/5/7/15/30: " +
      ", ".join(f"{B4[(foot, xc)] - B4[(foot, 0.0)]:+.1f}" for xc in (2.0, 4.0, 5.0, 7.0, 15.0, 30.0)))
OUT["numbers"]["B4"] = {f"{k_[0]}/{k_[1]}": v for k_, v in B4.items()}
d47 = [min(B4[(f_, 4.0)], B4[(f_, 7.0)]) - B4[(f_, 0.0)] for f_ in ("canonical", "alt")]
d15 = [B4[(f_, 15.0)] - B4[(f_, 0.0)] for f_ in ("canonical", "alt")]
check("B4 KiDS prefers a switch at x_c ~ 4-7 over no switch (Delta chi^2 < -8, both footings) and excludes x_c >= 15 (> +25)",
      f"best of 4/7: {d47[0]:+.1f} / {d47[1]:+.1f}; x_c = 15: {d15[0]:+.1f} / {d15[1]:+.1f}",
      all(v < -8 for v in d47) and all(v > 25 for v in d15),
      "a lead: poor base fit (~118/60), point-mass baryons, no 2-halo or external-field term; a full comparison needs "
      "the LCDM NFW + 2-halo model on the same data", load_bearing=False)

# ============================================================================================ B5 health
banner("B5  HEALTH OF THE SWITCH")
a0c = A0["canonical"]; alpha = a0c/c**2; Kb = 3*H0/c
s_shell = 1e-4                                                          # deep-MOND field ratio at ~1 Mpc
q_shell = (2.0/3.0)*s_shell**3                                          # q(s^2) ~ (2/3) s^3 in deep MOND (q' = nu - 1 ~ s^-1)
coef = 2*alpha**2*q_shell*XC**2*1.0/Kb**2 if XC else 0.0                # |f''| ~ 1 across the shell, x ~ x_c
P(f"    switching shell (s ~ {s_shell:g}): induced K^2 coefficient ~ 2 alpha^2 q x^2 f''/K^2 = {coef:.1e}  vs c_2 = 7.3e-3")
check("B5 inside bound regions the switch is saturated (L340's block unchanged); in the switching shell the induced K^2 "
      "coefficient is orders of magnitude below c_2", f"{coef:.1e} << 7.3e-3", coef < 1e-6)

# ============================================================================================ B6 prediction
banner("B6  THE PREDICTION: a mass- and redshift-dependent lensing truncation r_t = v_flat / (sqrt(x_c) H(z))")
rows = []
for Mb in (1e9, 1e10, 6e10, 3e11):
    vf = (G*Mb*MS*a0c)**0.25
    for z_ in (0.0, 0.25, 2.5):
        Hz = H0*math.sqrt(Or*(1+z_)**4 + Om*(1+z_)**3 + OL); rows.append((Mb, z_, vf/1e3, vf/(math.sqrt(max(XC, 5.0))*Hz)/MPCm))
for r_ in rows:
    if r_[1] in (0.0, 2.5): P(f"    M_b = {r_[0]:.0e} Msun, z = {r_[1]}: v_flat = {r_[2]:.0f} km/s, r_t = {r_[3]*1e3:.0f} kpc")
OUT["numbers"]["B6"] = rows
check("B6 (a prediction, not a test) r_t ~ 1 Mpc for the Milky Way today, scaling as M_b^(1/4) and 1/H(z); at z = 2.5 it is "
      "still >> 100 kpc, so the flat-a0(z) Tully-Fisher test is untouched",
      f"MW (6e10) today {[r_[3] for r_ in rows if r_[0] == 6e10 and r_[1] == 0.0][0]*1e3:.0f} kpc; at z = 2.5 "
      f"{[r_[3] for r_ in rows if r_[0] == 6e10 and r_[1] == 2.5][0]*1e3:.0f} kpc",
      [r_[3] for r_ in rows if r_[0] == 6e10 and r_[1] == 2.5][0] > 0.1, load_bearing=False)

banner("VERDICT")
P(f"""  One scalar of C-H/K's own foliation, x = 9 R3/(4 K^2), switches the MOND sector on only where the leaves curve faster
  than they expand.  It is zero on FRW and (3/2) Omega_m delta in the linear web, so linear growth returns to LCDM
  (B2: sigma_8 {min(sw):.3f}-{max(sw):.3f} against L341's {min(nsw):.0f}-{max(nsw):.0f}); it is saturated in every galaxy and in the Solar System
  (B3); KiDS-1000 prefers it at x_c ~ 4-7 -- the turnaround scale -- over no switch (B4, a lead); it is healthy (B5); and
  it predicts a lensing truncation at r_t = v_flat/(sqrt(x_c) H) (B6).  It does not solve the dark sector: the CMB's cold
  fluid must still stay out of galaxies.  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
