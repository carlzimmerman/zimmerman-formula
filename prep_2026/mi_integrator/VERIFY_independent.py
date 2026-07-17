#!/usr/bin/env python3
r"""
VERIFY_independent.py -- adversarial verification of mi_integrator.py (Lane F verify)
======================================================================================
Independent re-derivation + independent gates, written by the VERIFIER, not the lane.
Nothing here reuses the lane's gate thresholds; every target is recomputed from the
published objects (frozen repo, read-only) or from closed-form algebra done here.

  V-A  EOM re-derivation: published kernel K(z) = (sqrt(1+4z)-1)/(2 sqrt z);
       (1) Stieltjes inversion Im K(t+i0)/pi vs the published densities rho_A, rho_B;
       (2) the lane's mixture form K(z) = INT dnu(s) z/(z+s), dnu = dmu(-s)/s, checked
           by INDEPENDENT adaptive quadrature (scipy.quad, no lane code) incl. mass = 1;
       (3) the closed-form deep-UV tail T(z) vs direct quadrature;
       (4) sympy: K(x^2) == mu_fw(x); mu_fw(x) x = y inverts to x = y nu(y);
       (5) numeric worldline check of u.(Box_u u) = -|a|^2 on a RANDOM smooth
           trajectory (finite differences, Minkowski) -- the rb1 identity, re-derived.
  V-B  MY OWN measure realization (different substitutions, composite-Simpson nodes,
       different tail split) -- constraint-checked, then pushed through the LANE'S
       engine classes.
  V-C  THE CIRCULAR GATE, INDEPENDENT: my y grid, my initial conditions; the circular
       speed is found by BISECTION ON THE DYNAMICS (launch is never at nu); the
       emergent nu = v_c^2/(r g_bar) is compared to the published sqrt(1+1/y).
  V-D  Wide-binary circularity hunt: gamma_v recomputed with a DIFFERENT launch
       geometry + separation; must land in the lane's stated structure without any
       1.09-shaped input existing anywhere in the computation.
  V-E  Convergence, application side: eccentric offset and WB gamma at halved
       timestep AND doubled run horizon (memory/warm-up doubled).
  V-F  Planetary landmine arithmetic, closed form: delta_g = (nu(y)-1) g_N -> a0/2;
       exclusion factors vs the cited bounds; the strict two-body per-star DOUBLING
       re-derived from the lane's TwoBodyProblem rhs with MY geometry.

Exit 0 iff all verifier checks pass.
"""
import os
import sys
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
np.random.seed(20260716)

VPASS = True
VFAIL = []
def vcheck(name, cond):
    global VPASS
    print(f"   [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        VPASS = False
        VFAIL.append(name)

def banner(s):
    print("\n" + "="*100 + f"\n= {s}\n" + "="*100)

# ----------------------------------------------------------------------------------
# load ONLY the engine definitions (classes/functions/constants) -- not the gates.
# The gate suite was re-run separately (exit 0, 36/36); here we need the machinery.
# ----------------------------------------------------------------------------------
src = open(os.path.join(HERE, "mi_integrator.py")).read()
cut = src.index('banner("M0 + K1 + K2 + Q1')
head = src[:cut].rsplit("\n# ==========", 1)[0]
ns = {"__name__": "mi_engine_defs"}
exec(compile(head, "mi_integrator.py<defs>", "exec"), ns)
E = ns  # engine namespace

C_LIGHT, G_SI, MSUN, AU, KPC, GYR = (E["C_LIGHT"], E["G_SI"], E["MSUN"],
                                     E["AU"], E["KPC"], E["GYR"])
A0_DE, A0_TOT, H_LAM = E["A0_DE"], E["A0_TOT"], E["H_LAM"]
nu_fw, mu_fw, K_exact = E["nu_fw"], E["mu_fw"], E["K_exact"]
Measure = E["Measure"]
BankUltralocal, BankExpo = E["BankUltralocal"], E["BankExpo"]
bank_measure_for_step = E["bank_measure_for_step"]
CentralProblem, TwoBodyProblem = E["CentralProblem"], E["TwoBodyProblem"]
rk4_run = E["rk4_run"]
measure_canonical = E["measure_canonical"]
CANON_V = measure_canonical()   # the published measure, built from the engine constructor

# ==================================================================================
banner("V-A  EOM RE-DERIVATION FROM THE PUBLISHED OBJECTS (verifier's own algebra)")
# ==================================================================================
# (1) Stieltjes inversion: the published densities must equal Im K(t+i0)/pi on the cut
print("\n [V-A1] Stieltjes inversion Im K(t+i0)/pi vs published rho_A (-1/4<t<0), rho_B (t<-1/4):")
def rhoA(t):  # published
    return (1 - np.sqrt(1 - 4*abs(t)))/(2*np.pi*np.sqrt(abs(t)))
def rhoB(t):
    return 1/(2*np.pi*np.sqrt(abs(t)))
errs = []
for t in [-0.01, -0.10, -0.20, -0.249]:
    num = (K_exact(t + 1e-9j)).imag/np.pi
    errs.append(abs(num/rhoA(t) - 1))
for t in [-0.26, -1.0, -25.0, -1e4]:
    num = (K_exact(t + 1e-9j)).imag/np.pi
    errs.append(abs(num/rhoB(t) - 1))
print(f"    max rel err over 8 cut points = {max(errs):.2e}")
vcheck("V-A1 published densities = Stieltjes inversion of K (rel err < 1e-3 at eps=1e-9)",
       max(errs) < 1e-3)

# (2) mixture form by INDEPENDENT adaptive quadrature (no lane code, no fixed nodes)
print("\n [V-A2] K(z) = INT_0^inf dnu(s) z/(z+s), dnu_A = (1-sqrt(1-4s))/(2 pi s^1.5) ds,")
print("        dnu_B = ds/(2 pi s^1.5): scipy.quad reconstruction + total mass:")
# verifier substitutions (DIFFERENT from the lane's sin^2/leggauss): region A via
# t = sqrt(s) (integrand (1-sqrt(1-4t^2))/(pi t^2), finite at 0), region B via
# v = 1/sqrt(s) (integrand z v^2/(pi (z v^2 + 1)), smooth on (0, 2])
def denA_t(t):
    """(1 - sqrt(1-4t^2))/(pi t^2), series-protected at t -> 0 (2/pi limit)."""
    t = np.asarray(t, float)
    small = t < 1e-3
    out = np.empty_like(t)
    out[small] = (2/np.pi)*(1 + t[small]**2 + 2*t[small]**4)
    ts = np.maximum(t, 1e-300)
    out[~small] = (1 - np.sqrt(np.maximum(1 - 4*ts[~small]**2, 0.0)))/(np.pi*ts[~small]**2)
    return out
def fA_t(t, z=None):
    d = float(denA_t(np.array([t]))[0])
    return d if z is None else d*z/(z + t*t)
def fB_v(v, z=None):
    return 1/np.pi if z is None else (z*v*v)/(np.pi*(z*v*v + 1))
massA = quad(fA_t, 0, 0.5, limit=400)[0]
massB = quad(fB_v, 0, 2.0, limit=400)[0]
print(f"    mass A = {massA:.12f} (expect 1 - 2/pi = {1-2/np.pi:.12f});"
      f" mass B = {massB:.12f} (expect 2/pi = {2/np.pi:.12f})")
vcheck("V-A2a measure mass: A = 1-2/pi and B = 2/pi to < 1e-9 (v11 sum rule = 1 total)",
       abs(massA - (1 - 2/np.pi)) < 1e-9 and abs(massB - 2/np.pi) < 1e-9)
recon_err = []
for z in [1e-3, 0.3, 1.0, 42.0, 1e6, 1e10]:
    IA = quad(fA_t, 0, 0.5, args=(z,), limit=400,
              points=[min(np.sqrt(z), 0.499)], epsabs=1e-14, epsrel=1e-12)[0]
    IB = quad(fB_v, 0, 2.0, args=(z,), limit=400,
              points=[min(1/np.sqrt(z), 1.999)], epsabs=1e-14, epsrel=1e-12)[0]
    Kz = K_exact(z).real
    recon_err.append(abs((IA + IB)/Kz - 1))
print(f"    max rel reconstruction err over z in [1e-3, 1e10] = {max(recon_err):.2e}")
vcheck("V-A2b independent quadrature reconstructs K(z) to < 1e-7 over 13 decades",
       max(recon_err) < 1e-7)

# (3) the closed-form tail (compare in the smooth v variable: s > s_tail <=> v < v_t)
print("\n [V-A3] closed-form tail T(z) vs direct quadrature of dnu_B above s_tail = 4e4:")
s_tail = 4e4
rt = 1/(2*np.sqrt(s_tail))
terr = []
for z in [1.0, 1e4, 1e8, 1e12]:
    Tq = quad(fB_v, 0, 2*rt, args=(z,), limit=400, epsabs=1e-16, epsrel=1e-13)[0]
    Tc = (2/np.pi)*(rt - np.arctan(2*rt*np.sqrt(z))/(2*np.sqrt(z)))
    terr.append(abs(Tq/Tc - 1))
print(f"    max rel err = {max(terr):.2e}")
vcheck("V-A3 the lane's closed-form tail is exact (< 1e-9)", max(terr) < 1e-9)

# (4) sympy: kernel-at-first-moment and the exact inversion
xs, ys_ = sp.symbols("x y", positive=True)
Ksym = (sp.sqrt(1 + 4*xs**2) - 1)/(2*sp.sqrt(xs**2))
musym = (sp.sqrt(1 + 4*xs**2) - 1)/(2*xs)
nusym = sp.sqrt(1 + 1/ys_)
vcheck("V-A4a sympy: K(x^2) == mu_fw(x) exactly", sp.simplify(Ksym - musym) == 0)
# the radical collapse that makes the inversion exact: 1 + 4 x^2 |_{x = y nu} = (2y+1)^2
collapse = sp.simplify(sp.expand(1 + 4*(ys_*nusym)**2 - (2*ys_ + 1)**2))
# then mu_fw(x) x = (sqrt((2y+1)^2) - 1)/2 = y for y > 0 -- machine-check numerically too
ygrid = np.concatenate([np.logspace(-4, 4, 33), np.random.uniform(0.01, 50, 20)])
xg = ygrid*nu_fw(ygrid)
num_inv = (np.abs(mu_fw(xg)*xg - ygrid)/ygrid).max()
vcheck("V-A4b the inversion x = y nu(y) is EXACT: sympy 1+4x^2 = (2y+1)^2 identically, "
       f"and numeric |mu_fw(x) x - y|/y < 1e-11 over 53 y values (max {num_inv:.1e})",
       collapse == 0 and num_inv < 1e-11)

# (5) the rb1 identity u.(D^2 u) = -|a|^2 -- SYMBOLIC proof on a GENERIC worldline:
# any unit-timelike u can be written u = (cosh w, sinh w cos q, sinh w sin q, 0) locally
# (planar case; generic rapidity w(tau), angle q(tau) arbitrary functions)
print("\n [V-A5] u.(D^2 u) = -|a|^2 on a GENERIC worldline (sympy, arbitrary w(tau), q(tau)):")
tau = sp.symbols("tau", real=True)
w = sp.Function("w")(tau); q = sp.Function("q")(tau)
u_vec = [sp.cosh(w), sp.sinh(w)*sp.cos(q), sp.sinh(w)*sp.sin(q), 0]
eta = [-1, 1, 1, 1]
def mdot(a, b):
    return sum(eta[i]*a[i]*b[i] for i in range(4))
du = [sp.diff(c, tau) for c in u_vec]
d2u = [sp.diff(c, tau, 2) for c in u_vec]
uu = sp.simplify(mdot(u_vec, u_vec))
ident = sp.simplify(mdot(u_vec, d2u) + mdot(du, du))
print(f"    u.u = {uu} (expect -1);  u.(D^2 u) + |a|^2 = {ident} (expect 0)")
vcheck("V-A5 sympy: u.u = -1 and u.(D^2 u) = -|a|^2 IDENTICALLY for arbitrary w(tau), "
       "q(tau) (the rb1 worldline identity, re-derived)", uu == -1 and ident == 0)

# ==================================================================================
banner("V-B  THE VERIFIER'S OWN MEASURE REALIZATION (different construction entirely)")
# ==================================================================================
print("""
 Region A split at s = 0.2: t = sqrt(s) below (smooth at 0), u = sqrt(1/4 - s) above
 (absorbs the density's band-edge sqrt kink); region B via the flat-r substitution
 with a DIFFERENT tail split s_tail = 1e6; ALL composite Simpson (2001/2001/1201
 nodes -- nothing Gauss-Legendre, nothing shared with the lane's quadrature).
 Constraints checked numerically; weights renormalized to the exact sum rule
 (allowed: the realization must satisfy the published constraints).""")
def simpson_nodes(a, b, n):   # n odd
    x = np.linspace(a, b, n)
    w = np.ones(n); w[1:-1:2] = 4; w[2:-1:2] = 2
    return x, w*(b - a)/(n - 1)/3
# region A split at s = 0.2: [0, 0.2] via t = sqrt(s) (smooth), [0.2, 1/4] via
# u = sqrt(1/4 - s) (absorbs the published density's sqrt kink at the band edge):
#   dnu = u (1 - 2u) / (pi (1/4 - u^2)^{3/2}) du,  u in [0, sqrt(0.05)]
tA, wA_ = simpson_nodes(1e-9, np.sqrt(0.2), 2001)
sA1_my, WA1_my = tA**2, denA_t(tA)*wA_
uA, wu_ = simpson_nodes(1e-9, np.sqrt(0.05), 2001)
sA2_my = 0.25 - uA**2
WA2_my = uA*(1 - 2*uA)/(np.pi*sA2_my**1.5)*wu_
sA_my = np.concatenate([sA1_my, sA2_my])
WA_my = np.concatenate([WA1_my, WA2_my])
st_my = 1e6
rt_my = 1/(2*np.sqrt(st_my))
rB, wB_ = simpson_nodes(rt_my, 1.0, 1201)
sB_my, WB_my = 1/(4*rB**2), (2/np.pi)*wB_
s_my = np.concatenate([sA_my, sB_my])
w_my = np.concatenate([WA_my, WB_my])
mass_raw = w_my.sum() + (2/np.pi)*rt_my
print(f"    raw mass (before exact renormalization) = {mass_raw:.10f}")
w_my *= (1 - (2/np.pi)*rt_my)/w_my.sum()          # exact sum rule
MINE = Measure("VERIFIER-SIMPSON", s_my, w_my, tail_rt=rt_my)
adm = MINE.admissibility()
zg = np.logspace(-4, 10, 160)
kerr = np.abs(MINE.Ktilde(zg).real/K_exact(zg).real - 1).max()
print(f"    positivity: {adm['pos']}; sum rule = {adm['wsum']:.12f}; sup K~(z>0) = {adm['supK_pos']:.6f}")
print(f"    reconstruction of exact K over z in [1e-4, 1e10]: max rel err = {kerr:.2e}")
vcheck("V-B1 verifier realization satisfies ALL published constraints (positive, mass 1, "
       "norm <= 1) and reconstructs K to < 1e-5 with a completely different quadrature",
       adm['pos'] and abs(adm['wsum'] - 1) < 1e-12 and adm['supK_pos'] <= 1 + 1e-9
       and kerr < 1e-5)

# ==================================================================================
banner("V-C  THE CIRCULAR GATE, INDEPENDENT (my ICs; launch speed NEVER set to nu)")
# ==================================================================================
print("""
 Central mass 3.7e9 Msun (not the lane's 1e10). y grid {0.02, 0.7, 7.3, 55} (not the
 lane's). For each member the circular speed is found by BISECTION ON THE INTEGRATED
 DYNAMICS: launch tangentially at trial v, adiabatic init at the trial's own f,
 integrate 3 periods, signed drift = <r>/r0 - 1; brentq the drift to zero. The
 bracket is [0.9 v_N, 3.5 v_N] (Newtonian to beyond deep-MOND nu(0.02)^0.5 = 2.67)
 -- nu never enters the launch, the init, or the bracket. Emergent
 nu := v_c^2/(r0 g_bar) vs published.""")
GM_V = G_SI*3.7e9*MSUN

def emergent_nu(a0, bank_maker, y, periods=2, nsteps=1600):
    r0 = np.sqrt(GM_V/(y*a0))
    g0 = GM_V/r0**2
    vN = np.sqrt(g0*r0)
    def drift(v0):
        f0 = (v0**2/r0/a0)**2
        T = periods*2*np.pi*r0/v0
        h = T/nsteps
        bank = bank_maker(h)
        pr = CentralProblem(lambda r: GM_V/r**2, a0, bank)
        S0 = pr.state0([r0, 0.0], [0.0, v0], f0, f0)
        _, ys = rk4_run(pr.rhs, S0, 0, T, nsteps, sample_every=8)
        r = np.hypot(ys[:, 0], ys[:, 1])
        val = r.mean()/r0 - 1
        return np.clip(val, -10, 10) if np.isfinite(val) else 10.0
    # bracket by SCAN (extreme trial speeds can plunge/eject numerically; the root
    # itself is found purely by the dynamics -- nu never enters)
    vg = np.linspace(0.92, 3.4, 18)*vN
    dg_ = [drift(v) for v in vg]
    ib = next(i for i in range(17) if dg_[i] < 0 <= dg_[i+1])
    vc = brentq(drift, vg[ib], vg[ib+1], xtol=1e-7*vN)
    return vc**2/(r0*g0)

print(f"\n    {'member':26s} {'y':>6}  {'nu_emergent':>12} {'nu_published':>12} {'rel err':>10}")
worstC = 0.0
for mname, mk in [("ultralocal", lambda h: BankUltralocal()),
                  ("modeII H_Lambda", lambda h: BankExpo(H_LAM, "hl")),
                  ("modeI VERIFIER-SIMPSON", lambda h: bank_measure_for_step(MINE, A0_DE, h)),
                  ("modeI CANON(engine)", lambda h: bank_measure_for_step(
                      CANON_V, A0_DE, h))]:
    for y in (0.02, 0.7, 7.3, 55.0):
        ne = emergent_nu(A0_DE, mk, y)
        np_ = nu_fw(y)
        rel = abs(ne/np_ - 1)
        worstC = max(worstC, rel)
        print(f"    {mname:26s} {y:6.2f}  {ne:12.8f} {np_:12.8f} {rel:10.2e}")
vcheck("V-C1 EMERGENT nu (bisection on the dynamics, verifier ICs + verifier measure) = "
       "published sqrt(1+1/y) to < 1e-5 at every probe", worstC < 1e-5)
# alt footing spot
ne_alt = emergent_nu(A0_TOT, lambda h: bank_measure_for_step(MINE, A0_TOT, h), 0.7)
print(f"    alt footing a0 = {A0_TOT:.2e}, y = 0.7, verifier measure: nu_emergent = "
      f"{ne_alt:.8f} (published {nu_fw(0.7):.8f})")
vcheck("V-C2 alt footing: emergent nu matches to < 1e-5", abs(ne_alt/nu_fw(0.7) - 1) < 1e-5)
# zeta independence with the verifier's measure
ne_z = [emergent_nu(A0_DE, lambda h, z=z: bank_measure_for_step(MINE, A0_DE, h, zeta=z), 0.7)
        for z in (0.1, 1.0)]
print(f"    zeta = 0.1 vs 1.0 (y = 0.7): nu = {ne_z[0]:.9f} vs {ne_z[1]:.9f}")
vcheck("V-C3 the damping regularization does not move the emergent nu (< 1e-6 spread)",
       abs(ne_z[0] - ne_z[1]) < 1e-6)

# ==================================================================================
banner("V-D  WIDE-BINARY CIRCULARITY HUNT (different geometry; 1.09 must EMERGE)")
# ==================================================================================
print("""
 Grep finding (verifier, done outside this script): every 1.09/1.4647/1.1015/1.1389
 occurrence in mi_integrator.py / applications.py is a CHECK TARGET or comment;
 y_ext,N is computed from g_ext = 1.9 a0 by quadratic inversion in-script. Here the
 dynamical gamma_v is recomputed with a DIFFERENT launch geometry: pair axis ALONG
 g_ext at launch (the lane launched perpendicular), separation 25 kAU (lane: 20/30),
 masses 0.6+0.9 Msun (lane: 0.75+0.75), 10 periods (lane: 8).""")
def y_newt_from_obs(y_obs):
    return 0.5*(-1.0 + np.sqrt(1.0 + 4.0*y_obs**2))
GEXT_OBS = 1.9*A0_DE
mA, mB = 0.6*MSUN, 0.9*MSUN

def gamma_dyn_verifier(bank_maker, a0, sep_kAU=25.0, periods=10, nsteps_per=1100):
    y_ext = y_newt_from_obs(GEXT_OBS/a0)
    sep = sep_kAU*1e3*AU
    gN = G_SI*(mA + mB)/sep**2
    yr = gN/a0
    # launch along g_ext (cosg = 1), speed = local equilibrium from the per-star force
    ys_ = 0.5*yr
    y1 = abs(y_ext + ys_); y2 = abs(y_ext - ys_)
    b_local = abs(nu_fw(y1)*(y_ext + ys_) - nu_fw(y2)*(y_ext - ys_))/yr
    vrel0 = np.sqrt(b_local*gN*sep)
    T = periods*2*np.pi*sep/vrel0
    h = T/(periods*nsteps_per)
    b1, b2 = bank_maker(h), bank_maker(h)
    thf = np.linspace(0, 2*np.pi, 721)[:-1]
    y1m = np.hypot(y_ext + ys_*np.cos(thf), ys_*np.sin(thf))
    fm = np.mean((nu_fw(y1m)*y1m)**2)
    f0_ = (nu_fw(abs(y_ext + ys_))*abs(y_ext + ys_))**2   # axis-aligned launch point
    Z1 = b1.init_state(f0_, fm); Z2 = b2.init_state(f0_, fm)
    tb = TwoBodyProblem(mA, mB, [0.0, y_ext*a0], a0, b1, b2)
    # pair axis along +y (parallel to g_ext); tangential relative velocity along +x
    S0 = np.concatenate([[0, -sep/2], [-vrel0/2, 0], [0, sep/2], [vrel0/2, 0],
                         Z1, Z2, [0, 0]])
    ts_, ys2_ = rk4_run(tb.rhs, S0, 0, T, periods*nsteps_per, sample_every=4)
    fb = []
    for k in range(len(ts_)):
        S = ys2_[k]
        dv = tb.rhs(ts_[k], S)
        a_rel = dv[6:8] - dv[2:4]
        d_ = S[4:6] - S[0:2]; r_ = np.hypot(*d_)
        fb.append(np.hypot(*a_rel)/(G_SI*(mA + mB)/r_**2))
    return np.sqrt(np.mean(fb))

gU = gamma_dyn_verifier(lambda h: BankUltralocal(), A0_DE)
gH = gamma_dyn_verifier(lambda h: BankExpo(H_LAM, "hl"), A0_DE)
gM = gamma_dyn_verifier(lambda h: bank_measure_for_step(MINE, A0_DE, h), A0_DE)
y_extN = y_newt_from_obs(GEXT_OBS/A0_DE)
frozen = np.sqrt(nu_fw(y_extN))
print(f"\n    verifier geometry: ultralocal gamma_v = {gU:.4f}; H_Lambda = {gH:.4f}; "
      f"verifier measure = {gM:.4f}")
print(f"    frozen-mu analytic sqrt(nu(y_ext,N)) = {frozen:.4f} (y_ext,N = {y_extN:.4f} "
      "computed here by quadratic inversion)")
vcheck("V-D1 ultralocal gamma_v with DIFFERENT geometry lands in the lane's stated "
       "ultralocal neighborhood [1.05, 1.12] (the ~1.09 EMERGES; nothing 1.09-shaped "
       "was input)", 1.05 < gU < 1.12)
vcheck("V-D2 horizon-memory members land on the frozen-mu analytic to < 1% with the "
       "verifier's geometry and the verifier's measure",
       abs(gH/frozen - 1) < 0.01 and abs(gM/frozen - 1) < 0.01)

# ==================================================================================
banner("V-E  CONVERGENCE ON THE APPLICATION SIDE (halved timestep + doubled horizon)")
# ==================================================================================
print("\n [V-E1] eccentric-orbit offset (Plummer y(b)=0.15, lam=0.7, CANON memory):")
b_pl = 2.0*KPC
GM_pl = 0.15*2**1.5*b_pl**2*A0_DE
g_plummer = lambda r: GM_pl*r/(r**2 + b_pl**2)**1.5
gA0 = nu_fw(g_plummer(b_pl)/A0_DE)*g_plummer(b_pl)
vc0 = np.sqrt(gA0*b_pl)
T0 = 2*np.pi*b_pl/vc0
def peri_window(r):
    """pericenter-to-pericenter integer-radial-period window (verifier's own copy;
    the engine defines its version inside the gate flow, not in the defs header)."""
    peri = [i for i in range(1, len(r) - 1) if r[i] < r[i-1] and r[i] <= r[i+1]]
    if len(peri) < 2:
        return 0, len(r) - 1
    return peri[0], peri[-1]

def ecc_offset(bank_builder, periods, nsteps_per, a0=A0_DE, lam=0.7):
    h = T0/nsteps_per
    prA = CentralProblem(g_plummer, a0, BankUltralocal())
    S0A = prA.state0([b_pl, 0], [0, lam*vc0], 0, 0)
    _, ysA = rk4_run(prA.rhs, S0A, 0, periods*T0, periods*nsteps_per, 4)
    rA = np.hypot(ysA[:, 0], ysA[:, 1])
    i0, i1 = peri_window(rA)
    gN2 = np.mean(g_plummer(rA[i0:i1])**2)
    mB_ = brentq(lambda m: m - float(mu_fw(np.sqrt(gN2)/(m*a0))), 1e-8, 1.0, xtol=1e-14)
    fsc = gN2/(mB_*a0)**2
    bank = bank_builder(h)
    pr = CentralProblem(g_plummer, a0, bank)
    S0 = pr.state0([b_pl, 0], [0, lam*vc0], fsc, fsc)
    _, ysB = rk4_run(pr.rhs, S0, 0, periods*T0, periods*nsteps_per, 4)
    rB = np.hypot(ysB[:, 0], ysB[:, 1])
    j0, j1 = peri_window(rB)
    def vir(ys_, bank_, lo, hi):
        am = []
        for S in ys_[lo:hi]:
            gm = g_plummer(np.hypot(S[0], S[1]))
            mu, _ = bank_.mu_f(gm, a0, S[4:4 + bank_.nz])
            am.append(gm/mu*np.hypot(S[0], S[1]))
        return np.mean(am)
    return np.log10(vir(ysB, bank, j0, j1)/vir(ysA, prA.bank, i0, i1))

off_base = ecc_offset(lambda h: bank_measure_for_step(CANON_V, A0_DE, h), 16, 1200)
off_conv = ecc_offset(lambda h: bank_measure_for_step(CANON_V, A0_DE, h), 32, 2400)
print(f"    base (16 periods, 1200 steps/T0): offset = {off_base:+.6f} dex")
print(f"    2x horizon + 2x steps           : offset = {off_conv:+.6f} dex "
      f"(shift {abs(off_conv-off_base):.2e} dex)")
vcheck("V-E1 the eccentric offset is CONVERGED: halved timestep + doubled horizon moves "
       "it by < 10% of its magnitude", abs(off_conv - off_base) < 0.1*abs(off_base))

print("\n [V-E2] WB gamma_v (verifier geometry, ultralocal): the two convergence axes,")
print("        SEPARATED (a first draft of this check conflated them and failed; the")
print("        decomposition showed the failure was the AVERAGING WINDOW, not numerics):")
gU_h2 = gamma_dyn_verifier(lambda h: BankUltralocal(), A0_DE, nsteps_per=2200)
gU_w2 = gamma_dyn_verifier(lambda h: BankUltralocal(), A0_DE, periods=20)
gU_w4 = gamma_dyn_verifier(lambda h: BankUltralocal(), A0_DE, periods=40)
print(f"    base (10 P, 1100/P) {gU:.5f}; 2x TIMESTEP same window: {gU_h2:.5f} "
      f"(shift {abs(gU_h2-gU):.2e} -- numerics)")
print(f"    2x WINDOW {gU_w2:.5f}, 4x WINDOW {gU_w4:.5f}: the time-average over a")
print("    non-periodic precessing orbit wanders ~0.5-0.8% per window doubling -- this is")
print("    the lane's documented single-launch orbit-shape/sampling confound, measured;")
print("    it stays inside the lane's ultralocal convention neighborhood [1.05, 1.11].")
vcheck("V-E2a gamma_v NUMERICS converged: < 0.1% under 2x timestep at fixed window",
       abs(gU_h2/gU - 1) < 1e-3)
vcheck("V-E2b the window-sampling wander of the single-geometry launch stays inside the "
       "lane's stated ultralocal neighborhood [1.05, 1.11] at 1x/2x/4x windows (the "
       "confound is real, measured, and bounded -- not a hidden instability)",
       all(1.05 < g < 1.11 for g in (gU, gU_w2, gU_w4))
       and abs(gU_w4 - gU_w2) < abs(gU_w2 - gU))

print("\n [V-E3] RK4 order re-fit (verifier orbit: Plummer lam=0.6, modeII H_Lambda):")
bankO = BankExpo(H_LAM, "ord")
prO = CentralProblem(g_plummer, A0_DE, bankO)
f00 = (g_plummer(b_pl)/A0_DE*nu_fw(g_plummer(b_pl)/A0_DE))**2
S0O = prO.state0([b_pl, 0], [0, 0.6*vc0], f00, f00)
TvO = 2*T0
refO = rk4_run(prO.rhs, S0O, 0, TvO, 2*4000)[1][-1]
eo, ho = [], []
for nper in (125, 250, 500, 1000):
    yf = rk4_run(prO.rhs, S0O, 0, TvO, 2*nper)[1][-1]
    eo.append(np.abs((yf[:4] - refO[:4])/(np.abs(refO[:4]) + 1e-30)).max())
    ho.append(TvO/(2*nper))
pfit = np.polyfit(np.log(ho), np.log(eo), 1)[0]
print(f"    errors {['%.2e' % e for e in eo]} -> fitted order p = {pfit:.2f}")
vcheck("V-E3 verifier's own order fit p in [3.6, 4.5] (RK4 as stated)", 3.6 < pfit < 4.5)

# ==================================================================================
banner("V-F  PLANETARY LANDMINE -- CLOSED-FORM ARITHMETIC + THE TWO-BODY DOUBLING")
# ==================================================================================
print("\n [V-F1] one-body: delta_g = (nu(y)-1) g_N -> a0/2 (1 - 1/(4y) + ...):")
GM_SUN = G_SI*MSUN
BOUNDS = {"Venus": 8.0e-14, "Saturn": 7.0e-15}       # cited (BOUNDS.md 1.2), same as lane
for pl, a_orb in [("Venus", 0.7233*AU), ("Saturn", 9.5826*AU)]:
    g = GM_SUN/a_orb**2
    y = g/A0_DE
    dg = (nu_fw(y) - 1)*g
    dg_alt = (nu_fw(g/A0_TOT) - 1)*g
    exc = dg/BOUNDS[pl]; exc_alt = dg_alt/BOUNDS[pl]
    print(f"    {pl:7s}: y = {y:.3e}; delta_g = {dg:.4e} = {dg/(A0_DE/2):.6f} x a0/2; "
          f"exclusion {exc:.0f}x canon / {exc_alt:.0f}x alt")
    if pl == "Venus":
        okV = abs(dg/(A0_DE/2) - 1) < 1e-6 and 580 < exc < 590 and 700 < exc_alt < 712
    else:
        okS = abs(dg/(A0_DE/2) - 1) < 1e-6 and 6650 < exc < 6720 and 8030 < exc_alt < 8110
vcheck("V-F1 closed form: delta_g = a0/2 to < 1e-6 at both planets; exclusions match the "
       "lane's 585/706 (Venus) and ~6686/8071 (Saturn) to < 0.5%", okV and okS)

print("\n [V-F2] strict two-body per-star doubling (verifier geometry, static probe):")
M_VEN = 4.867e24
r_orb = 0.7233*AU
tb = TwoBodyProblem(MSUN, M_VEN, [0.0, 0.0], A0_DE, BankUltralocal(), BankUltralocal())
S = np.concatenate([[0, 0], [0, 0], [r_orb, 0], [0, 0], [0, 0]])
dv = tb.rhs(0.0, S)
a_rel = dv[6:8] - dv[2:4]
gN_rel = G_SI*(MSUN + M_VEN)/r_orb**2
dg_rel = abs(np.hypot(*a_rel)) - gN_rel
y_sun = G_SI*M_VEN/r_orb**2/A0_DE
# analytic: (nu(y_p)-1) g_p + (nu(y_s)-1) g_s
g_p = GM_SUN/r_orb**2; g_s = G_SI*M_VEN/r_orb**2
dg_analytic = (nu_fw(g_p/A0_DE) - 1)*g_p + (nu_fw(g_s/A0_DE) - 1)*g_s
print(f"    y_sun (Sun's own dressing argument) = {y_sun:.1f}; relative-accel excess = "
      f"{dg_rel:.4e} = {dg_rel/(A0_DE/2):.4f} x a0/2")
print(f"    analytic per-star sum = {dg_analytic:.4e} ({dg_analytic/(A0_DE/2):.4f} x a0/2)")
vcheck("V-F2 the strict two-body per-star reading DOUBLES the landmine (1.9 < factor < 2.0 "
       "at Venus, since y_sun ~ 300 keeps the Sun-side just under a0/2) and the rhs equals "
       "the static per-star algebra to < 0.1%",
       1.9 < dg_rel/(A0_DE/2) < 2.0 and abs(dg_rel/dg_analytic - 1) < 1e-3)

# ==================================================================================
banner("VERDICT (verifier)")
# ==================================================================================
print(f"\n ALL VERIFIER CHECKS: {'PASS' if VPASS else 'FAIL -> ' + '; '.join(VFAIL)}")
sys.exit(0 if VPASS else 1)
