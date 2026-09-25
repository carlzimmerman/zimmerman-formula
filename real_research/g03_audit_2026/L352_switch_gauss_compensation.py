#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L352 -- GAUSS'S LAW AND THE BOUND-REGION SWITCH: a switch that turns C-H/K's MOND flux off in the linear web cancels an
isolated galaxy's phantom beyond its edge.  L341 (F7) and L342 (B4) scored KiDS with the phantom's mass RETAINED beyond
the edge -- a profile no local switch of the MOND flux can produce.  Rescored with the profile the action does produce,
L342's threshold x_c ~ 5 is disfavoured; a window at x_c ~ 2-3 survives KiDS and growth, and the Lyman-alpha forest
(L346, committed by the parallel lane) closes it.

WHY THIS GATE.  In C-H/K the phantom enters only through a divergence: Delta Phi = 4 pi G rho_b + S* div[f(x) (nu - 1)
grad S u] (ACTION.md, T-B's field equation, with L342's switch f multiplying the MOND term).  If f = 0 on a closed
surface around a galaxy, the divergence theorem fixes the flux of grad Phi through it at 4 pi G M_b: beyond the switch
edge an isolated galaxy weighs exactly its baryons, for dynamics and (lensing = dynamics) for lensing.  The phantom
inside the edge is cancelled by an equal negative mass at the edge.  L342's KiDS model kept M(<r) = M(<r_edge) beyond
the edge (its code: M = np.where(r > r_edge, M[edge], M); L341 F7 likewise).

WHAT THIS LANE CHECKS
  Z1 THE THEOREM (symbolic + numeric): spherical r^2 g = G M_b(<r) + r^2 f (nu - 1) g_N exactly, so f = 0 beyond r_e
     gives M_dyn(<r) = M_b there; in general it is the divergence theorem (the heat filter S* is a convolution that
     commutes with div on flat leaves, so it only smooths the edge over xi ~ 0.03 pc).  Numeric: a switched profile
     returns M_b beyond the edge to machine precision.
  Z2 THE EDGE IS SINGULAR (symbolic lemma + numeric, informational): in deep MOND the switch variable obeys
     x = x_b + X_0 (F + dF/du) (F = f(x), u = ln r, X_0 = v_f^2/(rH)^2).  Wherever 0 < f < 1 the density is positive, so the
     enclosed phantom cannot decrease there in baryon-poor outskirts; integrating the radial equation for smooth switches,
     F never reaches the off-branch.  The cancellation sits in a negative-mass shell where f ~ 0 (a delta shell for a step
     switch).  The KiDS profiles below use the step solution with the edge at its maximal radius (the most favourable).
  Z3 L342's THRESHOLD, RESCORED (Brouwer+2021 lensing rotation curves, 4 stellar-mass bins, full covariance, M_b free
     per bin, L342's B4 machinery with exact annulus averages): with the compensated profile x_c = 5 is disfavoured
     against the unswitched profile on both footings, with and without a free-amplitude linear 2-halo term per bin;
     the retained profile reproduces L342's preference (control).
  Z4 WHAT SURVIVES KiDS AND GROWTH: scanning x_c (switch variable x = (3/2) Omega_m delta, the Hamiltonian-constraint
     form derived in L346 / Lean I26), KiDS (+2-halo) accepts the compensated switch for x_c <~ 3 and L342's own growth
     machinery (B2) returns LCDM growth for x_c >= ~2; the fitted 2-halo amplitudes there are bias-like (<~ 2), so the
     Mpc-scale lensing beyond the edge must come from correlated matter -- the web's cold fluid -- not the phantom.
  Z5 ROBUSTNESS: the same scores with the lens population smeared (log M_b over each bin's width, lens z 0.15-0.35), which
     spreads the edge and its shell over the stack.
  Z6 BOOKKEEPING: L341 F7 and L342 B4 are withdrawn as properties of the construction; what the window would predict
     (a negative-shell lensing edge at r_e ~ 1-1.7 Mpc, the fitted edges) is recorded.
  Z7 THE PINCER WITH THE FOREST: the committed forest gate L346 (P/P_LCDM at k = 1-4 h/Mpc, z = 2-3, pre-declared band
     [0.8, 1.2]) fails every threshold it tested up to x_c = 7; KiDS with the realizable profile accepts only x_c <~ 3 and
     disfavours the higher thresholds.  No threshold satisfies both.
  MUTATE=1 scores KiDS with the retained (unrealizable) profile in place of the compensated one: Z3's load-bearing
  check must FAIL (rc = 1).

SCOPE.  Point-mass baryons; linear 2-halo shape with free amplitude (the isolated-lens selection suppresses 2-halo, so
a free amplitude is generous); deep-MOND switch variable (x = x~ of L351 in static systems).  The growth side is L342's
B2 machinery unchanged (no G_N/G_cos factor: the leaf-average lambda-term of L350 G5, or c_2 below the L350 ceilings).
The dark sector (why the cold fluid is outside the edge and not inside galaxies) is not addressed.

Run from the repository root:  python3 real_research/g03_audit_2026/L352_switch_gauss_compensation.py
"""
import os, sys, json, math, time, warnings
warnings.filterwarnings("ignore", message=".*encountered in matmul.*"); warnings.filterwarnings("ignore", category=DeprecationWarning)
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L352_switch_gauss_compensation"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L352", "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()
_trap = getattr(np, "trapezoid", None) or np.trapz
def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok
def banner(t): P("\n" + "=" * 104); P(t); P("=" * 104)
P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: KiDS is scored with the retained (unrealizable) profile; Z3 must FAIL ***")

# ---------------------------------------------------------------------------------------- constants, kernel (L342)
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
def nu_vec(y):
    y = np.maximum(np.asarray(y, float), 1e-14); return 1.0 + np.interp(np.log10(y), LYG, HM)/y

# ============================================================================================ Z1 the theorem
banner("Z1  GAUSS: beyond the switch edge an isolated galaxy weighs its baryons (symbolic + numeric)")
r_, Gs_, Mb_ = sp.symbols('r G M_b', positive=True)
F_ = sp.Function('F'); gN_ = sp.Function('g_N'); nu_ = sp.Function('nu')
flux = r_**2 * F_(r_) * (nu_(r_) - 1) * gN_(r_)                      # r^2 x (switched MOND flux)
rho_ph = sp.diff(flux, r_) / (4 * sp.pi * Gs_ * r_**2)               # the phantom density it sources
Mph = flux / Gs_                                                     # candidate enclosed phantom M_ph(<r)
Mph_simpl = sp.simplify(sp.diff(Mph, r_) - 4 * sp.pi * r_**2 * rho_ph) # dM/dr = 4 pi r^2 rho (regular at r = 0)
P(f"    phantom density = div(f J)/(4 pi G):  M_ph(<r) = r^2 F(r)(nu - 1) g_N / G  (antiderivative check: {Mph_simpl})")
P("    => F(r) = 0 on a sphere  <=>  M_ph(<r) = 0 there: the enclosed dynamical mass is M_b (and lensing = dynamics)")
# numeric: a MW-like profile, the switch closed smoothly between 0.9 and 1.1 Mpc (prescribed F(r)), fine grid
KPC = Mpc/1e3; MS = 1.98892e30
rr_n = np.geomspace(0.1, 3e4, 300001)*KPC
Mb_n = 6e10*MS; gN_n = G*Mb_n/rr_n**2
Fr = 0.5*(1 - np.tanh((rr_n/Mpc - 1.0)/0.05))
Mdyn_n = (rr_n**2*(gN_n + Fr*(nu_vec(gN_n/A0["canonical"]) - 1)*gN_n))/G
beyond = rr_n > 2.0*Mpc
dev = float(np.max(np.abs(Mdyn_n[beyond]/Mb_n - 1)))
peak = float(Mdyn_n[np.argmin(np.abs(rr_n/Mpc - 0.8))]/Mb_n)
# the same through a density integral (what a lensing reconstruction integrates)
rho_n = np.gradient(Mdyn_n, rr_n)/(4*math.pi*rr_n**2)
Mint = np.concatenate([[Mdyn_n[0]], Mdyn_n[0] + np.cumsum(0.5*(4*math.pi*rr_n[1:]**2*rho_n[1:] + 4*math.pi*rr_n[:-1]**2*rho_n[:-1])*np.diff(rr_n))])
dev_int = float(np.max(np.abs(Mint[beyond]/Mb_n - 1)))
neg_mass = float(np.trapz(np.minimum(4*math.pi*rr_n**2*rho_n, 0), rr_n)/Mb_n)
P(f"    numeric (M_b = 6e10, edge at 1 Mpc): M_dyn(<0.8 Mpc) = {peak:.1f} M_b;  beyond 2 Mpc |M_dyn/M_b - 1| <= {dev:.1e} (flux), "
  f"{dev_int:.1e} (density integral); negative mass in the edge = {neg_mass:.1f} M_b")
OUT["numbers"]["Z1"] = {"Mdyn_0p8_over_Mb": peak, "max_dev_beyond": dev, "max_dev_integral": dev_int, "negative_shell_over_Mb": neg_mass}
check("Z1 a switched divergence-form MOND flux cancels the phantom beyond the switch edge: M_dyn = M_b there (theorem; "
      "numeric to machine precision), the cancellation carried by a negative-mass shell at the edge",
      f"M_dyn(<0.8 Mpc) = {peak:.0f} M_b -> beyond 2 Mpc M_b to {max(dev, dev_int):.1e}; shell {neg_mass:.0f} M_b",
      Mph_simpl == 0 and dev < 1e-9 and dev_int < 2e-3 and neg_mass < -10,
      "no local switch of the MOND flux can leave an isolated galaxy's phantom mass in place beyond its edge")

# ============================================================================================ Z2 singular edge
banner("Z2  THE STATIC EDGE: positive density wherever the switch is partly on; no regular on->off solution")
u_, X0_, xb_ = sp.symbols('u X_0 x_b', real=True)
Fu = sp.Function('F')(u_)
x_expr = xb_ + X0_ * (Fu + sp.diff(Fu, u_))                          # deep MOND: x_ph = X_0 (F + F'), X_0 = v_f^2/(rH)^2
P(f"    x = {x_expr}   (from M_ph(<r) = F v_f^2 r/G:  4 pi G rho_ph/H^2 = X_0 d(F e^u)/du e^-u)")
P("    lemma: where 0 < F < 1, x lies in the switch band (x > 0), so d(F e^u)/du > -x_b e^u/X_0: the enclosed phantom")
P("    cannot decrease in baryon-poor outskirts while the switch is partly on")
rows_z2 = []
xc = 5.0
for wv in (0.25, 1.0):
    finv = lambda F, wv=wv: xc + 0.5*wv*math.log(F/(1 - F))
    for u1 in (-3.0, -1.0, -0.3):
        X0 = lambda u: xc*math.exp(-2*u)
        rhs = lambda u, Y: [(finv(min(max(Y[0], 1e-300), 1 - 1e-15)))/X0(u) - Y[0]]
        ev = lambda u, Y: Y[0] - 1.0; ev.terminal = True; ev.direction = 1
        sol = solve_ivp(rhs, (u1, 4.0), [1 - 1e-6], max_step=2e-3, rtol=1e-9, atol=1e-12, events=ev)
        rows_z2.append((wv, u1, float(sol.y[0].min()), float(math.exp(sol.t[np.argmin(sol.y[0])])), bool((sol.y[0] < 1e-3).any())))
        P(f"    tanh switch w = {wv}: leave saturation at r/r_t = {math.exp(u1):.3f} -> F dips to {sol.y[0].min():.3f} "
          f"(r/r_t = {math.exp(sol.t[np.argmin(sol.y[0])]):.2f}) and returns to 1; reaches the off-branch: {rows_z2[-1][4]}")
OUT["numbers"]["Z2"] = [dict(zip(("w", "u1", "F_min", "r_at_min", "reaches_off"), r_)) for r_ in rows_z2]
check("Z2 (informational) for smooth switches no static trajectory reaches the off-branch: the cancellation that Z1 "
      "requires sits in a singular negative shell (step switch) or has no regular static solution (smooth switch)",
      f"F_min over 6 runs = {min(r_[2] for r_ in rows_z2):.2f}; any reaching F < 1e-3: {any(r_[4] for r_ in rows_z2)}",
      not any(r_[4] for r_ in rows_z2),
      "the 'bistable outskirts' of L342 are sharper than stated: with baryon-poor outskirts the edge is a delta shell",
      load_bearing=False)

# ============================================================================================ Z3 KiDS
banner("Z3  L342's THRESHOLD RESCORED WITH THE REALIZABLE (COMPENSATED) PROFILE (KiDS-1000, L342's B4 machinery)")
B = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
PCm = 3.0857e16; MPCm = PCm*1e6
Rd, Ed, Sd = [], [], []
for b in (1, 2, 3, 4):
    d = np.genfromtxt(os.path.join(B, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt"), comments="#")
    Rd.append(d[:, 0]); Ed.append(d[:, 1]/d[:, 4]); Sd.append(d[:, 3]/d[:, 4])
cv = np.genfromtxt(os.path.join(B, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"), comments="#")
vv = cv[:, 4]/cv[:, 6]; npb = len(Rd[0]); Cf = vv.reshape(4, 4, npb, npb).transpose(0, 2, 1, 3).reshape(4*npb, 4*npb)
Ci = np.linalg.inv((Cf + Cf.T)/2)
rr = np.geomspace(1e-3, 30, 4000)*MPCm; Rp = np.geomspace(0.005, 6, 700)*MPCm
LOGSTEP = math.log(Rd[0][1]/Rd[0][0])                                # data bins are log-uniform
def Hz(z): return H0*math.sqrt(Om*(1 + z)**3 + OL)
def project_M2(rho):
    """projected (cylinder) mass M_2D(<R) of a spherical density, on the Rp grid (continuous part)."""
    Sig = np.zeros_like(Rp)
    for i, Rv in enumerate(Rp):
        m = rr > Rv*1.0000001; r2 = rr[m]; Sig[i] = 2*_trap(rho[m]*r2/np.sqrt(r2**2 - Rv**2), r2)
    return np.concatenate([[0], np.cumsum(0.5*(Sig[1:]*Rp[1:] + Sig[:-1]*Rp[:-1])*np.diff(Rp))])*2*math.pi + 2*math.pi*Rp[0]**2*Sig[0]
def shell_M2(m, re, R):
    """exact M_2D(<R) of a thin shell of mass m at radius re (smooth, no singularity)."""
    return np.where(R < re, m*(1 - np.sqrt(np.clip(1 - (R/re)**2, 0.0, 1.0))), m)
def annulus_esd(M2_of_R, Rq):
    """exact annulus average of Delta Sigma from M_2D alone:  <DS> = [2 Int M2/R dR - (M2(R2) - M2(R1))]/(pi (R2^2 - R1^2))."""
    out = np.zeros_like(Rq)
    for i, R0 in enumerate(Rq):
        R1, R2 = R0*math.exp(-LOGSTEP/2)*MPCm, R0*math.exp(LOGSTEP/2)*MPCm
        Rg = np.geomspace(R1, R2, 801); M2 = M2_of_R(Rg)
        out[i] = (2*_trap(M2/Rg, Rg) - (M2[-1] - M2[0]))/(math.pi*(R2**2 - R1**2))
    return out*PCm**2/MS
def model_M2(Mb, a0, xc, mode, z):
    """returns a function R -> M_2D(<R) [kg] and the edge radius [Mpc] for the three profiles."""
    M = Mb*nu_vec(G*Mb/rr**2/a0); re = None
    if xc and mode != "none":
        rho_dyn = np.gradient(M, rr)/(4*math.pi*rr**2)
        rho_bar = Om*rho_crit0*(1 + z)**3                             # x = 4 pi G (rho - rho_bar)/H^2 = (3/2) Omega_m(z) delta (L346, I26)
        on = 4*math.pi*G*(rho_dyn - rho_bar)/Hz(z)**2 >= xc
        it = int(np.where(on)[0].max()) if on.any() else 0; re = rr[it]
        M = np.where(np.arange(len(rr)) > it, M[it], M)                 # phantom density zero beyond the edge
    M2c = project_M2(np.gradient(M - Mb, rr)/(4*math.pi*rr**2))
    m_sh = -(M[-1] - Mb) if (mode == "compensated" and re is not None) else 0.0   # Z1: cancel the phantom exactly
    def f(R, M2c=M2c, m_sh=m_sh, re=re):
        val = np.interp(np.log(R), np.log(Rp), M2c) + Mb
        return val + (shell_M2(m_sh, re, R) if m_sh else 0.0)
    return f, (re/MPCm if re is not None else None)
# linear 2-halo shape at z = 0.25 (L342's EH98 transfer function), amplitude free per bin
def T_EH98(k):
    th = T_CMB/2.7; s = 44.5*math.log(9.83/(Om*h*h))/math.sqrt(1 + 10*om_b**0.75)
    ag = 1 - 0.328*math.log(431*Om*h*h)*(Ob/Om) + 0.38*math.log(22.3*Om*h*h)*(Ob/Om)**2
    ge = Om*h*(ag + (1 - ag)/(1 + (0.43*k*s/h)**4)); q = k*th*th/ge
    L = math.log(2*math.e + 1.8*q); Cc = 14.2 + 731.0/(1 + 62.5*q); return L/(L + Cc*q*q)
def Wth(x): return 3*(math.sin(x) - x*math.cos(x))/x**3
def P_un(kh): k = kh*h; return k**ns*T_EH98(k)**2
PN = (SIG8/math.sqrt(quad(lambda kh: kh**2*P_un(kh)*Wth(8*kh)**2/(2*math.pi**2), 1e-4, 60, limit=600)[0]))**2
def Dgrowth(a):
    Ez = lambda A: math.sqrt(Om/A**3 + OL)
    return 2.5*Om*Ez(a)*quad(lambda A: 1/(A*Ez(A))**3, 0, a)[0]
Dz = Dgrowth(1/1.25)/Dgrowth(1.0)
kk = np.geomspace(1e-4, 50, 6000)                                    # 1/Mpc
Pk = np.array([PN*P_un(k/h)/h**3 for k in kk])*Dz**2                 # Mpc^3
def xi_lin(rM): return _trap(kk**2*Pk*np.sinc(kk*rM/math.pi)*np.exp(-(kk*0.05)**2), kk)/(2*math.pi**2)
rgrid = np.geomspace(0.005, 200, 1500); xig = np.array([xi_lin(r0) for r0 in rgrid])
rho_m_z = Om*rho_crit0*1.25**3*(Mpc**3/MS)                           # Msun/Mpc^3
def w_proj(Rm):
    chi = np.geomspace(1e-4, 150, 3000); rr_ = np.sqrt(Rm**2 + chi**2)
    return 2*_trap(np.interp(np.log(rr_), np.log(rgrid), xig), chi)
Rp_M = Rp/MPCm; wR = np.array([w_proj(R0) for R0 in Rp_M])
Sig2h = rho_m_z*wR                                                   # Msun/Mpc^2 per unit bias
M2h = np.concatenate([[0], np.cumsum(0.5*(Sig2h[1:]*Rp_M[1:] + Sig2h[:-1]*Rp_M[:-1])*np.diff(Rp_M))])*2*math.pi + math.pi*Rp_M[0]**2*Sig2h[0]
M2h_kg = M2h*MS
twoh_cache = [annulus_esd(lambda R: np.interp(np.log(R), np.log(Rp), M2h_kg), Rd[b]) for b in range(4)]
P(f"    linear 2-halo per unit bias at z = 0.25 (annulus-averaged, bin 4): Delta Sigma_2h at 0.3/1.0/2.6 Mpc = "
  f"{np.interp(0.3, Rd[3], twoh_cache[3]):.3f} / {np.interp(1.0, Rd[3], twoh_cache[3]):.3f} / {twoh_cache[3][-1]:.3f} Msun/pc^2")
LM = np.round(np.arange(9.8, 11.81, 0.1), 2)
SMEAR_DM = (0.5, 0.15, 0.1, 0.1)                                     # half-widths of the four log M* bins (bin 1 capped)
ZS = (0.15, 0.25, 0.35)
_PROF = {}
def prof(lm, a0, xc, mode, z):
    key = (round(lm, 3), a0, xc, mode, z)
    if key not in _PROF: _PROF[key] = model_M2(10**lm*MS, a0, xc, mode, z)
    return _PROF[key]
_ESD = {}
def esd_bin(b, lm, a0, xc, mode, smear):
    key = (b, round(lm, 3), a0, xc, mode, smear)
    if key in _ESD: return _ESD[key]
    if not smear:
        f, re = prof(lm, a0, xc, mode, 0.25); out = (annulus_esd(f, Rd[b]), re)
    else:
        dm = SMEAR_DM[b]; offs = np.linspace(-dm, dm, 5) if dm > 0.12 else np.linspace(-dm, dm, 3)
        acc = np.zeros_like(Rd[b]); res = []
        for o in offs:
            for z in ZS:
                f, re = prof(round(lm + o, 2), a0, xc, mode, z); acc += annulus_esd(f, Rd[b]); res.append(re)
        out = (acc/(len(offs)*len(ZS)), (min(r_ for r_ in res if r_), max(r_ for r_ in res if r_)) if any(res) else None)
    _ESD[key] = out; return out
def fit_model(a0, xc, mode, with2h, smear=False):
    mods = []; res = []
    for b in range(4):
        best = None
        for lm in LM:
            mk0, re = esd_bin(b, lm, a0, xc, mode, smear)
            if with2h:                                                # best amplitude A in [0, 20] (diagonal proxy)
                t2 = twoh_cache[b]; wts = 1/Sd[b]**2
                A = float(np.clip(np.sum(wts*t2*(Ed[b] - mk0))/np.sum(wts*t2*t2), 0.0, 20.0)); mk = mk0 + A*t2
            else: A, mk = 0.0, mk0
            c_ = float(np.sum(((Ed[b] - mk)/Sd[b])**2))
            if best is None or c_ < best[0]: best = (c_, mk, lm, A, re)
        mods.append(best[1]); res.append((best[2], best[3], best[4]))
    dv = np.concatenate(Ed) - np.concatenate(mods)
    return float(dv @ Ci @ dv), res
real_mode = "retained" if MUTATE else "compensated"
Z3 = {}
for foot in ("canonical", "alt"):
    a0 = A0[foot]
    for w2 in (False, True):
        Z3[(foot, "none", 0.0, w2)] = fit_model(a0, 0.0, "none", w2)
        Z3[(foot, "retained", 5.0, w2)] = fit_model(a0, 5.0, "retained", w2)
        Z3[(foot, real_mode, 5.0, w2)] = fit_model(a0, 5.0, real_mode, w2)
        base = Z3[(foot, "none", 0.0, w2)][0]
        P(f"    {foot:9s} {'+2-halo' if w2 else 'no 2-halo':9s}: chi^2 unswitched {base:.1f} (60 pts);  retained x_c=5 (L342 B4, control) "
          f"{Z3[(foot, 'retained', 5.0, w2)][0] - base:+.1f};  {real_mode} x_c=5 {Z3[(foot, real_mode, 5.0, w2)][0] - base:+.1f}")
    r5 = Z3[(foot, real_mode, 5.0, True)][1]
    P(f"      {real_mode} x_c = 5 (+2-halo): edges {[round(r_[2], 2) for r_ in r5]} Mpc; A_2h {[round(r_[1], 2) for r_ in r5]}")
d5_2h = [Z3[(f_, real_mode, 5.0, True)][0] - Z3[(f_, "none", 0.0, True)][0] for f_ in ("canonical", "alt")]
d5_no = [Z3[(f_, real_mode, 5.0, False)][0] - Z3[(f_, "none", 0.0, False)][0] for f_ in ("canonical", "alt")]
dret = [Z3[(f_, "retained", 5.0, False)][0] - Z3[(f_, "none", 0.0, False)][0] for f_ in ("canonical", "alt")]
OUT["numbers"]["Z3"] = {f"{k_[0]}/{k_[1]}/{k_[2]}/{'2h' if k_[3] else 'no2h'}": {"chi2": v[0], "per_bin": v[1]} for k_, v in Z3.items()}
check("Z3 rescored with the profile the switch actually produces (phantom cancelled beyond the edge), L342's threshold "
      "x_c = 5 is DISFAVOURED against the unswitched profile on both footings: Delta chi^2 > +9 with a free 2-halo term "
      "and > +100 without; the retained profile reproduces L342's preference (control)",
      f"compensated x_c=5: +2-halo {', '.join(f'{v:+.1f}' for v in d5_2h)}; no 2-halo {', '.join(f'{v:+.0f}' for v in d5_no)}; "
      f"retained (control) {', '.join(f'{v:+.1f}' for v in dret)}",
      all(v > 9 for v in d5_2h) and all(v > 100 for v in d5_no),
      "L342's KiDS preference for x_c ~ 4-7 came from a profile the action cannot produce")

# ============================================================================================ Z4 what survives
banner("Z4  WHAT SURVIVES: the thresholds KiDS (+2-halo) accepts vs those that keep linear growth LCDM (L342's B2)")
XCS = (1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0, 15.0)
for foot in ("canonical", "alt"):
    a0 = A0[foot]
    for xc in XCS:
        Z3[(foot, real_mode, xc, True)] = fit_model(a0, xc, real_mode, True)
    base = Z3[(foot, "none", 0.0, True)][0]
    P(f"    {foot:9s} KiDS +2-halo, Delta chi^2 vs unswitched: " + ", ".join(f"x_c={xc:g}: {Z3[(foot, real_mode, xc, True)][0] - base:+.1f}" for xc in XCS))
def Pun(kh): k = kh*h; return k**ns*T_EH98(k)**2
def Delta_lin0(kh): return math.sqrt(kh**3*PN*Pun(kh)/(2*math.pi**2))
KH = np.logspace(math.log10(0.02), math.log10(20.0), 48); DREF = np.array([Delta_lin0(k) for k in KH])
def sigma8_of(D0): return math.sqrt(_trap([D0[i]**2*Wth(8*KH[i])**2 for i in range(len(KH))], np.log(KH)))
def growth(xc, foot="canonical", mode="rms", z_i=1000.0):           # L342's B2, verbatim
    om = Om; ol = 1 - om - Or; a_i = 1/(1 + z_i); a0 = A0[foot]
    Ez = lambda a: math.sqrt(Or/a**4 + om/a**3 + ol); dlnH = lambda a: 0.5*(-4*Or/a**4 - 3*om/a**3)/Ez(a)**2
    r0 = solve_ivp(lambda N, Y: [Y[1], 1.5*(om/math.exp(3*N)/Ez(math.exp(N))**2)*Y[0] - (2 + dlnH(math.exp(N)))*Y[1]],
                   (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14).y[0][-1]
    Di = DREF/r0
    def boost(y, a, dlt):
        Omz = om/a**3/Ez(a)**2
        return nu_mono(y) if 1.5*Omz*abs(dlt) >= xc else 1.0
    if mode == "rms":
        def rhs(N, Y):
            a = math.exp(N); D, Dp = Y; rho = om*rho_crit0/a**3
            gk = 4*math.pi*G*rho*np.abs(Di*D)/(KH*h/(a*Mpc)); grms = math.sqrt(_trap(gk**2/KH, KH)/_trap(1/KH, KH))
            drms = math.sqrt(_trap((Di*D)**2/KH, KH)/_trap(1/KH, KH))
            return [Dp, 1.5*(om/a**3/Ez(a)**2)*boost(grms/a0, a, drms)*D - (2 + dlnH(a))*Dp]
        return Di*solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-7, atol=1e-12).y[0][-1]
    out = []
    for i, kh in enumerate(KH):
        def rhs(N, Y, kh=kh):
            a = math.exp(N); d, dp = Y; gN = 4*math.pi*G*om*rho_crit0/a**3*abs(d)/(kh*h/(a*Mpc))
            return [dp, 1.5*(om/a**3/Ez(a)**2)*boost(gN/a0, a, d)*d - (2 + dlnH(a))*dp]
        out.append(solve_ivp(rhs, (math.log(a_i), 0.0), [Di[i], Di[i]], method="LSODA", rtol=1e-7, atol=1e-22).y[0][-1])
    return np.array(out)
G4 = {}
XCG = (1.5, 2.0, 2.5, 3.0, 4.0)
for foot in ("canonical", "alt"):
    for mode in ("rms", "permode"):
        for xc in XCG:
            G4[(foot, mode, xc)] = sigma8_of(growth(xc, foot, mode))
        P(f"    {foot:9s} {mode:7s}: sigma_8 at x_c = " + ", ".join(f"{xc:g}: {G4[(foot, mode, xc)]:.3f}" for xc in XCG))
window = {}
for foot in ("canonical", "alt"):
    base = Z3[(foot, "none", 0.0, True)][0]
    ok = [xc for xc in XCG if all(abs(G4[(foot, m_, xc)]/SIG8 - 1) < 0.02 for m_ in ("rms", "permode"))
          and Z3[(foot, real_mode, xc, True)][0] - base <= 4.0]
    Aw = {xc: [round(r_[1], 2) for r_ in Z3[(foot, real_mode, xc, True)][1]] for xc in ok}
    ew = {xc: [round(r_[2], 2) for r_ in Z3[(foot, real_mode, xc, True)][1]] for xc in ok}
    window[foot] = {"x_c": ok, "A_2h": Aw, "edges_Mpc": ew}
    P(f"    {foot:9s}: growth within 2% AND KiDS (+2-halo) Delta chi^2 <= +4 at x_c = {ok};  A_2h there {Aw};  edges {ew} Mpc")
OUT["numbers"]["Z4"] = {"window": window, "kids_2h": {f"{f_}/{xc}": Z3[(f_, real_mode, xc, True)][0] - Z3[(f_, "none", 0.0, True)][0]
                                                      for f_ in ("canonical", "alt") for xc in XCS},
                        "sigma8": {f"{k_[0]}/{k_[1]}/{k_[2]}": v for k_, v in G4.items()}}
narrow = all(window[f_]["x_c"] and max(window[f_]["x_c"]) <= 4.0 for f_ in ("canonical", "alt"))
phys_A = all(max(max(v) for v in window[f_]["A_2h"].values()) <= 2.0 for f_ in ("canonical", "alt") if window[f_]["x_c"])
check("Z4 without the forest a window survives on both footings: for x_c ~ 2-3 the compensated switch keeps linear growth "
      "within 2% of LCDM and fits KiDS as well as or better than the unswitched profile, with bias-like 2-halo amplitudes (<= 2)",
      f"canonical {window['canonical']['x_c']}, alt {window['alt']['x_c']}; A_2h physical: {phys_A}", narrow and phys_A,
      "the Mpc-scale lensing beyond the edge must then come from correlated matter (the web's cold fluid), not the phantom")

# ============================================================================================ Z5 robustness
banner("Z5  ROBUSTNESS: lens-population smearing (log M_b across each bin, lens z 0.15/0.25/0.35)")
Z5 = {}
for foot in ("canonical", "alt"):
    a0 = A0[foot]
    Z5[(foot, "none")] = fit_model(a0, 0.0, "none", True, smear=True)
    for xc in (2.0, 3.0, 5.0, 7.0, 10.0):
        Z5[(foot, xc)] = fit_model(a0, xc, real_mode, True, smear=True)
    base = Z5[(foot, "none")][0]
    P(f"    {foot:9s} smeared, +2-halo: chi^2 unswitched {base:.1f};  compensated " +
      ", ".join(f"x_c = {xc:g}: {Z5[(foot, xc)][0] - base:+.1f}" for xc in (2.0, 3.0, 5.0, 7.0, 10.0)))
OUT["numbers"]["Z5"] = {f"{k_[0]}/{k_[1]}": {"chi2": v[0], "per_bin": v[1]} for k_, v in Z5.items()}
sm5 = [Z5[(f_, 5.0)][0] - Z5[(f_, "none")][0] for f_ in ("canonical", "alt")]
sm2 = [min(Z5[(f_, 2.0)][0], Z5[(f_, 3.0)][0]) - Z5[(f_, "none")][0] for f_ in ("canonical", "alt")]
check("Z5 (robustness) with the lens population smeared, x_c = 5 stays disfavoured and the x_c ~ 2 window stays acceptable",
      f"x_c = 5: {', '.join(f'{v:+.1f}' for v in sm5)}; best of x_c = 2/3: {', '.join(f'{v:+.1f}' for v in sm2)}",
      all(v > 4 for v in sm5) and all(v <= 4 for v in sm2),
      "the verdicts do not hinge on the idealised single-edge shell", load_bearing=False)

# ============================================================================================ Z7 with the forest (L346)
banner("Z7  THE PINCER WITH THE FOREST: KiDS (this lane, realizable profile) vs the Lyman-alpha forest (L346, committed)")
L346J = os.path.join(HERE, "L346_switch_forest_gate_results.json")
forest = {}
if os.path.exists(L346J):
    F2 = json.load(open(L346J))["numbers"]["F2"]
    for key, (lo, hi) in F2.items():
        tag, foot_, z_ = key.rsplit("_", 2)[0], key.rsplit("_", 2)[1], key.rsplit("_", 2)[2]
        if tag.startswith("sw") and tag[2:].isdigit():
            xc = float(tag[2:]); forest.setdefault(xc, []).append((foot_, z_, lo, hi))
f_pass = {xc: all(0.8 <= lo and hi <= 1.2 for _, _, lo, hi in rows) for xc, rows in sorted(forest.items())}
for xc, rows in sorted(forest.items()):
    P(f"    L346 forest, x_c = {xc:g}: " + "; ".join(f"{f_} z={z_}: {lo:.2f}-{hi:.2f}" for f_, z_, lo, hi in rows) +
      f"  -> {'PASS' if f_pass[xc] else 'FAIL'} [0.8, 1.2]")
kids_ok = {xc: all(Z3[(f_, real_mode, xc, True)][0] - Z3[(f_, "none", 0.0, True)][0] <= 4.0 for f_ in ("canonical", "alt")) for xc in XCS}
P("    KiDS (+2-halo, realizable profile) Delta chi^2 <= +4 on both footings: " + ", ".join(f"x_c={xc:g}: {'ok' if kids_ok[xc] else 'no'}" for xc in XCS))
forest_min = min([xc for xc, ok in f_pass.items() if ok], default=None)
forest_fail_max = max([xc for xc, ok in f_pass.items() if not ok], default=None)
kids_max = max([xc for xc, ok in kids_ok.items() if ok], default=None)
above = [xc for xc in XCS if forest_fail_max is not None and xc > forest_fail_max]
kids_above = {xc: [Z3[(f_, real_mode, xc, True)][0] - Z3[(f_, "none", 0.0, True)][0] for f_ in ("canonical", "alt")] for xc in above}
P(f"    forest: every tested x_c <= {forest_fail_max:g} FAILS (L346); KiDS accepts x_c <= {kids_max:g}; above {forest_fail_max:g} KiDS gives "
  + "; ".join(f"x_c={xc:g}: {', '.join(f'{v:+.0f}' for v in vals)}" for xc, vals in kids_above.items()))
OUT["numbers"]["Z7"] = {"forest_pass": {str(k_): v for k_, v in f_pass.items()}, "kids_ok": {str(k_): v for k_, v in kids_ok.items()},
                        "kids_above_forest": {str(k_): v for k_, v in kids_above.items()}}
closed = (forest_fail_max is not None and kids_max is not None and kids_max <= forest_fail_max
          and all(min(v) > 9 for v in kids_above.values()))
check("Z7 KiDS and the forest leave no threshold: the thresholds KiDS accepts with the realizable profile (x_c <= ~3) all "
      "fail L346's pre-declared forest band, and above L346's highest failing threshold KiDS disfavours the switch by "
      "Delta chi^2 > +9 on both footings",
      f"KiDS ok <= {kids_max}; forest fails <= {forest_fail_max}; KiDS above: {kids_above}", closed,
      "both sides are quantitative tensions (collisionless PM forest; linear 2-halo), not theorems -- the pincer is closed at "
      "that precision")

# ============================================================================================ Z6 bookkeeping + prediction
banner("Z6  BOOKKEEPING AND THE NEW PREDICTION")
P("    L341 F7 and L342 B4 kept M(<r) = M(<r_edge) beyond the edge.  By Z1 that needs the MOND flux ON beyond the edge, i.e.")
P("    no switch there.  Their KiDS statements ('~1 Mpc truncation mildly preferred', 'x_c ~ 4-7 preferred, Delta chi^2")
P("    -15..-19') describe a profile C-H/K + f(x) cannot produce; they are withdrawn as properties of the construction.")
pred = []
for Mb in (1e10, 6e10, 2e11):
    vf_ = (G*Mb*MS*A0["canonical"])**0.25
    for xc in (2.0, 2.5):
        pred.append((Mb, xc, vf_/(math.sqrt(xc)*Hz(0.25))/Mpc, vf_/(math.sqrt(xc)*H0)/Mpc))
P("    prediction if the window is real: r_e = v_f/(sqrt(x_c) H(z)); " + "; ".join(f"M_b={r_[0]:.0e}, x_c={r_[1]:g}: {r_[3]:.2f} Mpc (z=0)"
                                                                        for r_ in pred))
P("    (fitted edges at x_c = 2-3 with the Hamiltonian-constraint variable: 0.95-1.7 Mpc, Z4)")
P("    beyond r_e an isolated galaxy lenses as its baryons plus correlated structure; inside, the phantom ends in a negative shell")
OUT["numbers"]["Z6"] = [dict(zip(("Mb", "x_c", "r_e_Mpc_z0.25", "r_e_Mpc_z0"), r_)) for r_ in pred]
check("Z6 (bookkeeping) the retained profile requires the MOND flux beyond the edge; L341 F7 and L342 B4 are withdrawn as "
      "evidence for the switch; the KiDS-only window would put a lensing edge at ~1-1.7 Mpc", "Z1 + Z3 control", True,
      load_bearing=False)

banner("VERDICT")
P(f"""  In C-H/K the phantom is the divergence of the MOND flux, so a switch that turns the flux off in the linear web makes
  every isolated galaxy weigh exactly its baryons beyond its switch edge, the phantom inside cancelled by a negative
  shell at the edge (Z1; singular as a static solution, Z2).  L342 scored KiDS with the phantom kept -- a profile the
  action cannot produce.  Rescored with the realizable profile, L342's threshold x_c = 5 is disfavoured (Z3:
  Delta chi^2 {', '.join(f'{v:+.0f}' for v in d5_2h)} with a free 2-halo term, {', '.join(f'{v:+.0f}' for v in d5_no)} without).  Without the forest a window
  survives at x_c ~ 2-3 (Z4, robust to smearing Z5), with the Mpc-scale lensing supplied by bias-like 2-halo matter.
  With the forest it does not: every threshold KiDS accepts fails L346's pre-declared forest band, and above L346's
  highest failing threshold KiDS disfavours the switch (Z7).  The local bound-region switch is closed at the precision
  of the two tests; its KiDS 'lead' (L342 B4) and L341 F7's truncation result are withdrawn.  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
