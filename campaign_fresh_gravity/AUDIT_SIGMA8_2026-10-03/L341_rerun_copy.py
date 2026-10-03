#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L341 -- THE FRW GATE FOR C-H/K: the candidate of L340 FAILS linear cosmology, no floor built from its own fields
rescues it, and KiDS says where the missing switch may sit.

THE GATE.  L340 left "cosmological perturbations" as the first open item.  C-H/K's MOND kernel acts on the
filtered Newtonian field of ALL matter (C-H: Delta u = 4 pi G rho_total).  The CMB needs a cold fluid at Omega_c
(L295), so the live configuration is baryons + a cold component with the MOND sector switched on.  The record's
L142 found that an unfloored MOND boost on linear perturbations overshoots sigma_8 by ~17x (P2-b), and that the
framework's derived dS-Unruh Hubble floor, X = Z^2 (H/H_Lambda)^2 + y^2, removes the boost -- but that floor was
derived in the modified-INERTIA arm (prep_2026/mi_covariant_pt), which is lensing-dead.  C-H/K is modified gravity.
Does it have a floor of its own?

WHAT THIS LANE SHOWS (L142's growth machinery re-implemented: EH98 transfer, growing-mode ICs fixed off the
integrator's own unboosted run, per-mode and self-consistent rms field arguments; both a0 footings)
  F1 CONTROL: the LCDM spectrum and sigma_8 = 0.811 are reproduced.
  F2 THE GATE FAILS: C-H/K with the CMB's cold fluid gives sigma_8 = 18-27 at every c_2 in L340's window
     (7.3e-3 .. 0.067), per-mode and rms, both footings; P(k) is 250-1.5e5 x LCDM.
  F3 FINITE TRACKING DOES NOT RESCUE IT: the phantom's response weight 1/(1 + (H/c_s k)^2) with
     c_s^2 = c_2 c^2/(C(2 + 3 c_2)) leaves sigma_8 >= 1.3 even at c_2 = 1e-6 (c_s ~ 40 km/s, which would already
     break the galaxy tracking of L340 T1) -- the phantom follows the growing modes far faster than H.
  F4 THE NATURAL COVARIANT FLOOR, AND ITS HEALTH: C-H/K has one cosmological scalar of its own, the clock's
     expansion K (= 3H on FRW).  kappa = K/(3 alpha) = cH/a0 is EXACTLY the record's dS-Unruh floor.
       * as a quadratic floor, q(s^2 + kappa^2), it induces a K^2 term (2/9)(nu - 1) of the WRONG sign against
         -c_2 K^2: in deep MOND (nu - 1 >> 4.5 c_2) the khronon becomes a ghost/tachyon -- unhealthy;
       * as a quartic floor, q(sqrt(s^4 + kappa^4)), there is no K^2 term at K = 0 (L340's static block untouched)
         and on FRW the induced coefficient is (2/9) C_L(kappa) = (2/9) h'(kappa) << c_2 (healthy); the linear
         MOND response is (nu(s_eff) - 1)(s/s_eff)^2 -> 0 and sigma_8 returns to 0.81.
  F5 BUT THE FOLIATION IS CMC-STIFF (symbolic, the L340 block): the perturbation of K is ZERO for every static
     source (any C, any alpha_c) and ZERO for every source where C = 0; only time-dependent MOND sources move it,
     delta K = -i C omega rho/(2 c_2 k^2) at small omega.  A static galaxy therefore sits in K = 3 H_0.
  F6 SO THE K-FLOOR SWITCHES MOND OFF IN GALAXIES TODAY: kappa_0 = cH_0/a0 = 7.0 (canonical) / 5.8 (alt); on
     SPARC's binned RAR (f21's statistic) the floored law is excluded by Delta chi^2 >> 1e3.
  F7 WHAT THE MISSING SWITCH MUST DO (KiDS-1000, Brouwer+2021 lensing rotation curves, 4 stellar-mass bins, full
     covariance, M_b free per bin): a switch that turns MOND off where matter has not decoupled from the Hubble flow
     cannot truncate the phantom inside ~1 Mpc -- Delta chi^2 = +256 at 0.3 Mpc (the virial scale), +105 at 0.5 Mpc
     -- while a truncation at ~1 Mpc (the turnaround scale) is mildly PREFERRED (Delta chi^2 ~ -11 on a poor base
     fit, chi^2 = 118/60; 2-halo and external-field terms not modelled -- a lead, not a result).
  MUTATE=1 sets the MOND sector off (nu = 1): F2 must FAIL (rc = 1).

VERDICT IN ONE LINE.  C-H/K is not cosmologically viable as built; the only floor made of its own fields (K) is
healthy in quartic form but CMC-stiff, so it kills galaxies; a complete theory needs a variable that knows whether
matter has decoupled from the Hubble flow, switching at >~ 1 Mpc around galaxies -- which C-H/K does not contain.

Run from the repository root:  python3 real_research/g03_audit_2026/L341_chk_frw_gate.py
"""
import os, sys, json, math, time, warnings
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")   # spurious macOS-Accelerate BLAS flags; results finite (checked)
warnings.filterwarnings("ignore", category=DeprecationWarning)
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L341_chk_frw_gate"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L341", "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()
def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok
def banner(t): P("\n" + "=" * 104); P(t); P("=" * 104)
P(__doc__.split("WHAT THIS LANE SHOWS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the MOND sector is switched off (nu = 1); F2 must FAIL ***")

# ---------------------------------------------------------------------------------------- cosmology (L142 machinery)
c = 2.99792458e8; Mpc = 3.0856775814913673e22; G = 6.67430e-11
h = 0.6736; om_b, om_c = 0.02237, 0.1200; T_CMB = 2.7255; N_eff = 3.046; ns = 0.965
H0 = 100*h*1e3/Mpc; rho_crit0 = 3*H0**2/(8*math.pi*G)
Og = (4*5.670374419e-8*T_CMB**4/c**3)/rho_crit0; Or = Og*(1 + N_eff*(7/8)*(4/11)**(4/3))
Ob, Oc = om_b/h**2, om_c/h**2; Om = Ob + Oc; OL = 1 - Om - Or
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}; SIG8 = 0.811
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
# ---------------------------------------------------------------------------------------- L340's monotone kernel
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"): return np.where(y < 1e4, y/np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6): return (h_rar(y*(1 + e)) - h_rar(y*(1 - e)))/(2*y*e)
YP = brentq(lambda y: float(dh_rar(y)), 1, 5); HP = float(h_rar(YP))
LYG = np.linspace(-14, 14, 280001); YG = 10**LYG; DH = np.maximum(dh_rar(YG), 0.05*HP/(YG + YP))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5*(DH[1:] + DH[:-1])*np.diff(YG))])
def nu_mono(y):
    if MUTATE: return 1.0
    y = max(float(y), 1e-14); return 1.0 + float(np.interp(math.log10(y), LYG, HM))/y
def hprime(y): return float(np.interp(math.log10(max(y, 1e-14)), LYG, DH))
def nu_eff(y, kap):                      # the quartic floor q(sqrt(s^4 + kappa^4)): (nu - 1)_eff = (nu(s_eff) - 1)(s/s_eff)^2
    if kap == 0: return nu_mono(y)
    se = (y**4 + kap**4)**0.25; return 1.0 + (nu_mono(se) - 1.0)*(y/se)**2
def growth(sector, floor, c2, foot="canonical", mode="rms", z_i=1000.0):
    om = {"lcdm": Om, "both": Om}[sector]; ol = 1 - om - Or; a_i = 1/(1 + z_i); a0 = A0[foot]
    Ez = lambda a: math.sqrt(Or/a**4 + om/a**3 + ol); dlnH = lambda a: 0.5*(-4*Or/a**4 - 3*om/a**3)/Ez(a)**2
    r0 = solve_ivp(lambda N, Y: [Y[1], 1.5*(om/math.exp(3*N)/Ez(math.exp(N))**2)*Y[0] - (2 + dlnH(math.exp(N)))*Y[1]],
                   (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14).y[0][-1]
    Di = DREF/r0
    def boost(y, a, kh):
        if sector == "lcdm": return 1.0
        kap = c*H0*Ez(a)/a0 if floor else 0.0
        nu = nu_eff(y, kap); Cc = nu - 1.0
        if c2 is None or Cc <= 0: return nu
        cs = c*math.sqrt(c2/(Cc*(2 + 3*c2))); kphys = kh*h/(a*Mpc)
        return 1.0 + (nu - 1.0)/(1.0 + (H0*Ez(a)/(cs*kphys))**2)
    if mode == "rms":
        def rhs(N, Y):
            a = math.exp(N); D, Dp = Y; rho = om*rho_crit0/a**3
            gk = 4*math.pi*G*rho*np.abs(Di*D)/(KH*h/(a*Mpc)); grms = math.sqrt(np.trapz(gk**2/KH, KH)/np.trapz(1/KH, KH))
            return [Dp, 1.5*(om/a**3/Ez(a)**2)*boost(grms/a0, a, 1.0)*D - (2 + dlnH(a))*Dp]
        return Di*solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-7, atol=1e-12).y[0][-1]
    out = []
    for i, kh in enumerate(KH):
        def rhs(N, Y, kh=kh):
            a = math.exp(N); d, dp = Y; gN = 4*math.pi*G*om*rho_crit0/a**3*abs(d)/(kh*h/(a*Mpc))
            return [dp, 1.5*(om/a**3/Ez(a)**2)*boost(gN/a0, a, kh)*d - (2 + dlnH(a))*dp]
        out.append(solve_ivp(rhs, (math.log(a_i), 0.0), [Di[i], Di[i]], method="LSODA", rtol=1e-7, atol=1e-22).y[0][-1])
    return np.array(out)

banner("F1  CONTROL: the LCDM spectrum")
s_ctl = sigma8_of(growth("lcdm", False, None)); s_ref = sigma8_of(DREF)
check("F1 the integrator's LCDM run and the reference spectrum give sigma_8 = 0.811 to 1%", f"{s_ctl:.4f} / {s_ref:.4f}",
      abs(s_ctl/SIG8 - 1) < 0.01 and abs(s_ref/SIG8 - 1) < 0.01)

banner("F2-F3  C-H/K WITH THE CMB'S COLD FLUID: the linear boost, with and without finite tracking")
F2 = {}
for foot in ("canonical", "alt"):
    for c2 in (7.3e-3, 0.067):
        for mode in ("rms", "permode"):
            D0 = growth("both", False, c2, foot, mode); F2[(foot, c2, mode)] = (sigma8_of(D0), float(((D0/DREF)**2).min()), float(((D0/DREF)**2).max()))
            P(f"    {foot:9s} c_2 = {c2:<6g} {mode:7s}: sigma_8 = {F2[(foot, c2, mode)][0]:8.3f};  P/P_LCDM in [{F2[(foot, c2, mode)][1]:.3g}, {F2[(foot, c2, mode)][2]:.3g}]")
s2min = min(v[0] for v in F2.values())
check("F2 THE GATE: in L340's whole c_2 window, both footings and both field arguments, C-H/K with the CMB's cold fluid "
      "overshoots sigma_8 by more than 10x", f"min sigma_8 = {s2min:.3g} (observed 0.811)", s2min > 10 * SIG8,
      "C-H/K is not cosmologically viable as built: the MOND sector acts on the linear field and double-counts the cold fluid")
F3 = {}
for c2 in (1e-6, 1e-5, 1e-4):
    for mode in ("rms", "permode"):
        F3[(c2, mode)] = sigma8_of(growth("both", False, c2, "canonical", mode))
P("    slow tracking: " + "; ".join(f"c_2 = {k_[0]:.0e} {k_[1]}: {v:.3g}" for k_, v in F3.items()))
check("F3 finite tracking does not rescue it: even c_2 = 1e-6 (c_s ~ 40 km/s at C = 30, below galaxy tracking) leaves "
      "sigma_8 > 1.3", f"min sigma_8 over c_2 in 1e-6..1e-4 = {min(F3.values()):.3g}", min(F3.values()) > 1.3)

banner("F4  THE K-FLOOR: quadratic is unhealthy, quartic is healthy and fixes linear growth")
C2W = 7.3e-3
kap0 = {f: c*H0/A0[f] for f in A0}
quad_bad = [(y, (2/9)*(nu_mono(y) - 1)) for y in (0.01, 0.1, 1.0)]
qrt_frw = [(z_, (2/9)*hprime(c*H0*math.sqrt(Or*(1+z_)**4 + Om*(1+z_)**3 + OL)/A0["canonical"])) for z_ in (0.0, 1.0, 10.0)]
P(f"    kappa_0 = cH_0/a0 = {kap0['canonical']:.2f} (canonical) / {kap0['alt']:.2f} (alt) -- the record's floor Z H_0/H_Lambda")
P("    quadratic floor, induced K^2 coefficient (2/9)(nu-1) at y = 0.01/0.1/1 (vs c_2 = 7.3e-3): " + ", ".join(f"{v:.3g}" for _, v in quad_bad))
P("    quartic floor on FRW, induced coefficient (2/9) h'(kappa) at z = 0/1/10: " + ", ".join(f"{v:.2e}" for _, v in qrt_frw))
F4 = {mode: sigma8_of(growth("both", True, C2W, "canonical", mode)) for mode in ("rms", "permode")}
P(f"    quartic K-floor, c_2 = {C2W}: sigma_8 = {F4['rms']:.4f} (rms) / {F4['permode']:.4f} (per mode)")
check("F4 the quadratic K-floor makes the khronon unhealthy in deep MOND ((2/9)(nu-1) > c_2); the quartic floor is healthy "
      "on FRW ((2/9) h' << c_2) and returns linear growth to LCDM within 5%",
      f"quadratic {quad_bad[0][1]:.2g} > {C2W}; quartic {max(v for _, v in qrt_frw):.1e} < {C2W}; sigma_8 {F4['rms']:.3f}",
      quad_bad[0][1] > C2W and max(v for _, v in qrt_frw) < C2W and all(abs(v/SIG8 - 1) < 0.05 for v in F4.values()))

banner("F5  THE FOLIATION IS CMC-STIFF: the response of K in L340's scalar block (symbolic)")
k, Cs, c2s, acs, ws = sp.symbols('k C c_2 alpha_c omega', real=True)
psi, phi, beta, U, R = sp.symbols('psi phi beta U R')
def K_of(Cv, acv, wv):
    Dd = -sp.I*wv; eps = -c2s
    E = [4*k**2*psi - 4*k**2*phi - Dd*(-12*Dd*psi + 4*k**2*beta + 6*eps*(3*Dd*psi - k**2*beta)),
         -4*k**2*psi - 4*k**2*(U - phi) + 2*acv*k**2*phi - R,
         4*k**2*Dd*psi - 2*eps*k**2*(3*Dd*psi - k**2*beta) + Dd*R,
         4*k**2*(U - phi) + 4*k**2*Cv*U]
    s = sp.solve(E, [psi, phi, beta, U], dict=True)[0]
    return sp.cancel(3*Dd*s[psi] - k**2*s[beta])
K_static = K_of(Cs, acs, 0); K_newton = K_of(0, 0, ws); K_gen = sp.factor(sp.cancel(K_of(Cs, 0, ws)/R))
K_lead = sp.factor(sp.series(K_gen, ws, 0, 2).removeO())
P(f"    delta K, static source, any C and alpha_c: {K_static};  delta K where C = 0 (alpha_c -> 0), any omega: {K_newton}")
P(f"    delta K / rho, alpha_c -> 0: {K_gen};  small omega: {K_lead}")
check("F5 delta K vanishes for every static source and wherever C = 0; only time-dependent MOND sources move it (proportional "
      "to C omega rho / c_2 k^2): a static galaxy keeps the cosmological K = 3H", f"static {K_static}; C=0 {K_newton}; lead {K_lead}",
      K_static == 0 and K_newton == 0 and K_lead != 0,
      "at linear order around FRW; a nonlinear relaxation of the khronon inside bound systems is not excluded here")

banner("F6  THE K-FLOOR IN GALAXIES TODAY (kappa = cH_0/a0): SPARC")
sys.path.insert(0, os.path.join(REPO, "hunt_2026")); cwd = os.getcwd(); os.chdir(os.path.join(REPO, "hunt_2026"))
from hunt_lib import load_sparc, A0 as A0H
gals = load_sparc(); os.chdir(cwd)
gb = np.concatenate([g_["gbar"] for g_ in gals]); go = np.concatenate([g_["gobs"] for g_ in gals])
gid = np.concatenate([np.full(len(g_["r"]), i) for i, g_ in enumerate(gals)]); mm = (gb > 0) & (go > 0)
gb, go, gid = gb[mm], go[mm], gid[mm]; lo = np.log10(go)
F6 = {}
for foot, a0 in A0H.items():
    lyy = np.log10(gb/a0); edges = np.linspace(-2.6, 1.6, 22); cen = 0.5*(edges[1:] + edges[:-1]); ch = {"free": 0.0, "floor": 0.0}
    for i in range(len(cen)):
        kb = (lyy >= edges[i]) & (lyy < edges[i + 1])
        if kb.sum() < 15: continue
        rng = np.random.default_rng(i); gl = np.unique(gid[kb]); bs = []
        for _ in range(200):
            pick = rng.choice(gl, len(gl), replace=True); idx = np.concatenate([np.where(kb & (gid == g_))[0] for g_ in pick]); bs.append(np.median(lo[idx]))
        se = float(np.std(bs)); ob = float(np.median(lo[kb])); mg = float(np.median(np.log10(gb[kb])))
        ch["free"] += ((ob - (math.log10(nu_eff(10**cen[i], 0.0)) + mg))/se)**2
        ch["floor"] += ((ob - (math.log10(nu_eff(10**cen[i], c*H0/a0)) + mg))/se)**2
    F6[foot] = ch
    P(f"    {foot:9s}: chi^2 without floor {ch['free']:.1f}, with the K-floor at kappa_0 = {c*H0/a0:.2f}: {ch['floor']:.1f}")
check("F6 with K = 3H_0 inside galaxies the quartic K-floor removes MOND from the RAR: excluded on SPARC by Delta chi^2 > 1e3",
      "; ".join(f"{f_}: {v['floor'] - v['free']:+.0f}" for f_, v in F6.items()),
      all(v["floor"] - v["free"] > 1e3 for v in F6.values()))

banner("F7  WHERE A BOUND-vs-EXPANDING SWITCH MAY SIT: KiDS-1000 lensing rotation curves")
B = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
G6, MS, PCm = 6.6743e-11, 1.98892e30, 3.0857e16; MPCm = PCm*1e6; a0c = A0["canonical"]
Rd, Ed, Sd = [], [], []
for b in (1, 2, 3, 4):
    d = np.genfromtxt(os.path.join(B, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt"), comments="#")
    Rd.append(d[:, 0]); Ed.append(d[:, 1]/d[:, 4]); Sd.append(d[:, 3]/d[:, 4])
cv = np.genfromtxt(os.path.join(B, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"), comments="#")
vv = cv[:, 4]/cv[:, 6]; npb = len(Rd[0]); Cf = vv.reshape(4, 4, npb, npb).transpose(0, 2, 1, 3).reshape(4*npb, 4*npb)
Ci = np.linalg.inv((Cf + Cf.T)/2)
rr = np.geomspace(1e-3, 30, 4000)*MPCm; Rp = np.geomspace(0.02, 4, 240)*MPCm
nu_arr = np.vectorize(lambda x: 1.0 + float(np.interp(math.log10(max(x, 1e-14)), LYG, HM))/max(x, 1e-14))
def esd(Mb, rt):
    M = Mb*nu_arr(G6*Mb/rr**2/a0c)
    if rt is not None: M = np.where(rr > rt*MPCm, M[np.searchsorted(rr, rt*MPCm)], M)
    rho = np.gradient(M - Mb, rr)/(4*math.pi*rr**2); Sig = np.zeros_like(Rp)
    for i, Rv in enumerate(Rp):
        m = rr > Rv*1.0000001; r_ = rr[m]; Sig[i] = 2*np.trapz(rho[m]*r_/np.sqrt(r_**2 - Rv**2), r_)
    Mc = np.concatenate([[0], np.cumsum(0.5*(Sig[1:]*Rp[1:] + Sig[:-1]*Rp[:-1])*np.diff(Rp))])*2*math.pi + math.pi*Rp[0]**2*Sig[0]
    return Rp/MPCm, (Mc/(math.pi*Rp**2) - Sig + Mb/(math.pi*Rp**2))*PCm**2/MS
LM = np.linspace(9.8, 11.8, 21)
cache = {lm: esd(10**lm*MS, None) for lm in LM}
F7 = {}
for rt in (None, 2.0, 1.0, 0.5, 0.3):
    mods = []
    for b in range(4):
        best = None
        for lm in LM:
            Rq, dS = cache[lm] if rt is None else esd(10**lm*MS, rt)
            mk = np.interp(Rd[b], Rq, dS); c_ = float(np.sum(((Ed[b] - mk)/Sd[b])**2))
            if best is None or c_ < best[0]: best = (c_, mk)
        mods.append(best[1])
    dv = np.concatenate(Ed) - np.concatenate(mods); F7[rt] = float(dv @ Ci @ dv)
    P(f"    truncation radius {str(rt):5s} Mpc: full-covariance chi^2 = {F7[rt]:.1f} (60 points)")
dch = {rt: F7[rt] - F7[None] for rt in (2.0, 1.0, 0.5, 0.3)}
OUT["numbers"].update({"F2": {str(k_): v for k_, v in F2.items()}, "F3": {str(k_): v for k_, v in F3.items()}, "F4": F4,
                       "F5": {"static": str(K_static), "C0": str(K_newton), "lead": str(K_lead)}, "F6": F6, "F7": {str(k_): v for k_, v in F7.items()}})
check("F7 a switch that truncates the MOND phantom inside ~0.5 Mpc is excluded by KiDS (Delta chi^2 > +50); at ~1 Mpc it is "
      "allowed and mildly preferred", "; ".join(f"{k_} Mpc: {v:+.1f}" for k_, v in dch.items()),
      dch[0.3] > 50 and dch[0.5] > 50 and dch[1.0] < 0,
      "a lead, not a result: the untruncated base fit is poor (chi^2 ~ 118/60) and 2-halo / external-field terms are not modelled",
      load_bearing=False)

banner("VERDICT")
P(f"""  C-H/K fails the FRW gate as built: with the cold fluid the CMB requires, its MOND sector boosts the linear field
  and sigma_8 comes out {s2min:.0f}-{max(v[0] for v in F2.values()):.0f} (F2); finite tracking cannot fix it (F3).  The one floor made of its own fields, the
  clock's expansion K, reproduces the record's dS-Unruh floor on FRW and is healthy in quartic form (F4), but the
  foliation is CMC-stiff (F5): a static galaxy keeps K = 3H_0, and the floor then removes MOND from galaxies (F6).
  What a complete theory still needs is a variable that knows whether matter has decoupled from the Hubble flow;
  KiDS says such a switch cannot sit inside ~0.5 Mpc of a galaxy and is allowed near ~1 Mpc (F7).  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
