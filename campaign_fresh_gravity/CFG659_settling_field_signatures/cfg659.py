"""CFG659: does the settling field P leave any signature in ordinary matter or light?

Criteria: FROZEN_CRITERIA.md (committed alone, 75e95fe06). Reading lane on CFG694 (action), CFG695 (saturating W), CFG696
(radiative attractor); no CFG690-699 file is edited or imported.
  L = -|grad Phi - 4 pi G lam P|^2 / 8 pi G - rho_b Phi - W(P) - (gamma/2)|grad P|^2 + (I/2)|P_t|^2      (lam = 1 is the action)
  gamma = 2 pi G L*^2  (CFG691: l_gamma = L*^2 / 2 r_M);  c_P = sqrt(gamma / I) unfixed (CFG696).
  W: CFG695 saturating vacuum minus the critical quadratic; in u = 4 pi G P:  4 pi G W = w(u) = -a0 u - a0^2 ln(1 - u/a0) - u^2/2,
     w'(u) = u^2/(a0 - u),  w''(u) = u(2 a0 - u)/(a0 - u)^2.   Local gap for P perturbations: m^2 = 4 pi G w''/gamma = 2 w''/L*^2.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy mass required; no particle species; not
"theory closed"; no LCDM or standard-MOND yardstick in any verdict.

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg659.py        (CFG659_MUTATE=1: lam = 0; exit 1 iff any channel is non-zero)
"""
import os, sys, json, math
import numpy as np
from scipy.integrate import solve_bvp, quad

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG659_MUTATE", "0") == "1"
LAM = 0.0 if MUT else 1.0
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg659{TAG}.out"), "w")
RES = {"lane": "CFG659", "criteria": "75e95fe06", "mutate": MUT, "lam": LAM, "checks": {}, "numbers": {}}


def P_(s=""):
    print(s, flush=True)
    OUT.write(s + "\n")


def check(key, ok, detail):
    RES["checks"][key] = dict(ok=bool(ok), detail=detail)
    P_(f"  [{'PASS' if ok else 'FAIL'}] {key}: {detail}")
    return bool(ok)


P_(__doc__.strip())

G, C, MSUN, PC, YR = 6.6743e-11, 2.99792458e8, 1.98847e30, 3.0856775814913673e16, 3.15576e7
KPC, MPC, GYR, MP = 1e3 * PC, 1e6 * PC, 1e9 * YR, 1.67262192e-27
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LSTAR = [5.75, 100.0, 1000.0]                        # pc
CPS = [5e-3, 1.5e-2, 0.1, 1.0]                       # units of c
SIGNALS = {}                                          # channel -> worst signal (for the MUTATE control)


def w2(u, a0):                                        # w''(u), saturating vacuum minus quadratic
    return u * (2 * a0 - u) / (a0 - u) ** 2


def u_law(gN, a0):                                    # static unscreened polarization, u = a0 g/(a0+g), g_N = g^2/(g+a0)
    g = 0.5 * (gN + np.sqrt(gN ** 2 + 4 * gN * a0))
    return a0 * g / (a0 + g)


def gap_m(gN, a0, Ls):                                # local gap wavenumber (1/m) for P perturbations, law background
    u = LAM * u_law(gN, a0)
    return np.sqrt(2 * w2(u, a0)) / Ls


# =============================================================== D1: coupling (3-D spectral check)
P_("\nD1  coupling: Phi equation div(grad Phi - 4 pi G lam P) = 4 pi G rho_b  =>  g = g_N - 4 pi G lam P_L;  P_T never enters Phi")
rng = np.random.default_rng(659)
n = 32
k1 = 2 * np.pi * np.fft.fftfreq(n)
KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
K2 = KX ** 2 + KY ** 2 + KZ ** 2; K2[0, 0, 0] = 1.0
Gs = 1.0 / (4 * np.pi)                                # G = 1/4pi units for the check
rho = rng.normal(size=(n, n, n)); rho -= rho.mean()
Pv = [rng.normal(size=(n, n, n)) for _ in range(3)]
Pk = [np.fft.fftn(p) for p in Pv]
divPk = 1j * (KX * Pk[0] + KY * Pk[1] + KZ * Pk[2])
PLk = [Ki * (KX * Pk[0] + KY * Pk[1] + KZ * Pk[2]) / K2 for Ki in (KX, KY, KZ)]
PTk = [Pk[i] - PLk[i] for i in range(3)]


def phi_k(rhok, divk):
    ph = -4 * np.pi * Gs * (rhok + LAM * divk) / K2
    ph[0, 0, 0] = 0
    return ph


rk = np.fft.fftn(rho)
ph_full, ph_N = phi_k(rk, divPk), phi_k(rk, 0 * divPk)
divPTk = 1j * (KX * PTk[0] + KY * PTk[1] + KZ * PTk[2])
ph_T = phi_k(rk, divPTk)
err_L = max(np.max(np.abs(np.fft.ifftn(-1j * Ki * ph_full) - (np.fft.ifftn(-1j * Ki * ph_N) - 4 * np.pi * Gs * LAM * np.fft.ifftn(PLi))))
            for Ki, PLi in zip((KX, KY, KZ), PLk))
err_T = float(np.max(np.abs(ph_T - ph_N)))
check("D1 g = g_N - 4piG lam P_L exactly; a purely transverse P leaves Phi unchanged", err_L < 1e-10 and err_T < 1e-10,
      f"max|g - (g_N - 4piG lam P_L)| = {err_L:.1e}; max|Phi[P_T] - Phi_N| = {err_T:.1e}")
P_("    Matter feels P ONLY through Phi (universal, composition-blind): a passing longitudinal wave gives delta a = -4 pi G lam delta P_L.")
P_("    Electromagnetism: the action has NO term containing A_mu or F_munu. Any direct P-light coupling would be a NEW TERM (a knob);")
P_("    none is added. Light sees P only through the metric potentials (Phi; Psi = Phi is the open relativistic completion).")
SIGNALS["D1_force_per_unit_P"] = 4 * np.pi * G * LAM

# =============================================================== D2/D3: wave spectrum and flux
P_("\nD2  linear waves about a background u0 (a0 = footing):")
P_("    longitudinal:  I w^2 = gamma (k^2 + m^2),  m^2 = 2 w''(u0)/L*^2   (the |grad Phi - 4piG P|^2 term is P_L-independent: no mass)")
P_("    transverse:    I w^2 = gamma k^2 + 4 pi G lam^2 + gamma m_T^2         (massive, and decoupled from matter by D1)")
P_("    speed c_P = sqrt(gamma/I) (unfixed, CFG696). These are NOT GR gravitational waves: longitudinal, speed c_P, gapped where u0 != 0.")
P_("    regimes: deep (u0 << a0) m^2 = 4 u0/(a0 L*^2);  saturated (g >> a0) m ~ sqrt2 g/(a0 L*);  screened core of a star: u0 ~ GM/L*^2 ~ 0.")
P_("D3  traveling longitudinal wave: e = I Pdot^2, flux F = c_P e;  delta u0 = 4 pi G lam delta P0 = lam sqrt(16 pi G c_P F)/(w L*)")

# =============================================================== K1 + E_code (CFG696 functional, cubic W, CFG691 units)
P_("\nK1  static field energy of CFG696's functional (cubic W): E_code(S) = -int_0^S [v'^2/2 + v^2/s^2 + |v|^3/(3s) - v/s] ds")


def f_bvp(t, y):
    s = np.exp(t)
    return np.vstack([y[1], -y[1] + 2.0 * y[0] + s ** 2 * y[0] * np.abs(y[0]) - LAM])


tt = np.linspace(math.log(1e-4), math.log(1e4), 4001)
ss = np.exp(tt)
if LAM > 0:
    SOL = solve_bvp(f_bvp, lambda ya, yb: np.array([ya[1] - (ya[0] - 0.5), yb[0] - (1e-4 - 1e-8)]), tt,
                    np.vstack([1 / (ss + 2), -ss / (ss + 2) ** 2]), tol=1e-8, max_nodes=200000)
    qf = lambda s: float(SOL.sol(math.log(s))[0])
    dqf = lambda s: float(SOL.sol(math.log(s))[1]) / s
else:
    qf = lambda s: 0.0
    dqf = lambda s: 0.0


def e_code(s):
    q, dq = qf(s), dqf(s)
    v, dv = s * q, q + s * dq
    return 0.5 * dv ** 2 + v ** 2 / s ** 2 + abs(v) ** 3 / (3 * s) - LAM * v / s


E200 = -sum(quad(e_code, a, b, limit=400)[0] for a, b in ((1e-4, 1), (1, 20), (20, 200)))
E1e4 = E200 - sum(quad(e_code, a, b, limit=400)[0] for a, b in ((200, 2000), (2000, 1e4 * 0.999)))
slope = (E1e4 - E200) / math.log(1e4 * 0.999 / 200)
RES["numbers"]["E_code"] = dict(S200=E200, S1e4=E1e4, log_slope=slope)
if LAM > 0:
    check("K1 E_code(200) = CFG696 released energy for the zero start (2.99995) within 2%", abs(E200 - 2.99995) / 2.99995 < 0.02,
          f"E_code(200) = {E200:.5f}; E_code(1e4) = {E1e4:.4f}; d E/d ln S = {slope:.4f} (deep-regime analytic 2/3)")
else:
    P_(f"    lam = 0: E_code(200) = {E200:.3e}")
SIGNALS["E_code"] = E200

# =============================================================== settling energy per halo (saturating W, unscreened)
P_("\nS1  energy released by settling, saturating W (framework-native): E = M_b V_f^2 * eps(R/r_M),  V_f^4 = G M_b a0, r_M = sqrt(G M_b/a0)")


def eps_release(X):                                  # -int_0^X x^2 [w~(u~) - u~/x^2] dx, w~ = w/a0^2, u~ = u/a0, g~_N = 1/x^2
    def integ(x):
        gn = 1.0 / x ** 2
        u = LAM * float(u_law(np.array(gn), 1.0))
        w = -u - math.log1p(-u) - u * u / 2 if u > 1e-6 else u ** 3 / 3 + u ** 4 / 4
        return x * x * w - u
    return -sum(quad(integ, a, b, limit=400)[0] for a, b in ((1e-8, 1e-3), (1e-3, 1), (1, X)) if b > a)


HALOS = {"galaxy": (6e10, 100 * KPC, 1 * MPC), "group": (1e12, 500 * KPC, 1 * MPC), "cluster": (1e14, 2 * MPC, 5 * MPC)}
SETTLE = {}
for foot, a0 in FOOT.items():
    for h, (Mb, R, rout) in HALOS.items():
        M = Mb * MSUN
        Vf = (G * M * a0) ** 0.25
        rM = math.sqrt(G * M / a0)
        eps = eps_release(R / rM)
        E = eps * M * Vf ** 2
        t_rel, t_mer = 10 * GYR, R / Vf
        SETTLE[(foot, h)] = dict(Vf=Vf, rM=rM, eps=eps, E=E, L_relaxed=E / t_rel, L_merging=E / t_mer, t_mer=t_mer)
        P_(f"    {foot:9s} {h:7s}: V_f {Vf / 1e3:6.0f} km/s, r_M {rM / KPC:6.1f} kpc, R/r_M {R / rM:5.1f}, eps {eps:.3f}, "
           f"E {E:.2e} J; no-trap ceiling L: relaxed (10 Gyr) {E / t_rel:.1e} W, merging (R/V_f = {t_mer / GYR:.2f} Gyr) {E / t_mer:.1e} W")
RES["numbers"]["settle"] = {f"{k[0]}|{k[1]}": v for k, v in SETTLE.items()}
SIGNALS["settle_E"] = max(v["E"] for v in SETTLE.values())

c630 = json.load(open(os.path.join(LANES, "CFG630_settling_feeds_dark_energy", "cfg630_results.json")))
u_cos = c630["checks"]["K4_ceiling"]["max_drho"] * c630["inputs"]["rho_DE0"] * C ** 2 * LAM
P_(f"    cosmic ceiling (CFG630 K4 max d rho_DE/rho_DE0 = {c630['checks']['K4_ceiling']['max_drho']:.2e}): all settling energy ever, "
   f"as P waves: u_P <= {u_cos:.2e} J/m^3")
RES["numbers"]["u_cosmic_ceiling"] = u_cos

# =============================================================== S2: trapping below the gap
P_("\nS2  trapping: baryon-driven settling at w = 2 pi / t (t = 10 Gyr relaxed, R/V_f merging) below the local gap is evanescent;")
P_("    tau = int_R^r_out sqrt(m^2 - w^2/c_P^2) dr (point-mass law background); radiated fraction <= exp(-2 tau). Minimum over the window:")
TRAP = {}
for foot, a0 in FOOT.items():
    for h, (Mb, R, rout) in HALOS.items():
        M = Mb * MSUN
        r = np.geomspace(R, rout, 4000)
        gN = G * M / r ** 2
        best = None
        for mode, t in (("relaxed", 10 * GYR), ("merging", SETTLE[(foot, h)]["t_mer"])):
            w = 2 * np.pi / t
            for Ls in LSTAR:
                m = gap_m(gN, a0, Ls * PC)
                for cp in CPS:
                    kap = np.sqrt(np.clip(m ** 2 - (w / (cp * C)) ** 2, 0, None))
                    tau = float(np.trapz(kap, r))
                    row = dict(mode=mode, Lstar=Ls, cP=cp, tau=tau, log10_frac=-2 * tau / math.log(10))
                    TRAP[f"{foot}|{h}|{mode}|{Ls}|{cp}"] = row
                    if best is None or tau < best["tau"]:
                        best = row
        P_(f"    {foot:9s} {h:7s}: min tau {best['tau']:.3g} ({best['mode']}, L* {best['Lstar']} pc, c_P {best['cP']} c) "
           f"-> radiated fraction <= 10^{best['log10_frac']:.3g}")
RES["numbers"]["trap"] = TRAP
min_tau = min(v["tau"] for v in TRAP.values())
SIGNALS["trap_frac"] = math.exp(-2 * min_tau) if LAM > 0 else 0.0


def frac_rad(foot, h):                                 # worst (largest) radiated fraction for a halo
    return 0.0 if LAM == 0 else max(math.exp(-2 * v["tau"]) for k, v in TRAP.items() if k.startswith(f"{foot}|{h}|"))


# =============================================================== CFG696 PDE: ramp test (code units, cubic W)
P_("\nS3  CFG696 PDE, code units: start static, ramp the baryon source 1 -> 1.1 over T (smooth), run T + 600; radiated = flux out at S = 200")
S_MAX, DS, DT = 200.0, 0.02, 0.01
s = np.arange(0, S_MAX + DS / 2, DS)
si = s.copy(); si[0] = 1.0
v_st = np.where(s > 0, s * np.array([qf(max(x, 1e-4)) for x in s]), 0.0)


def run_ramp(T, amp=0.1):
    def src(t):
        if T == 0:
            x = 1.0 if t > 0 else 0.0
        else:
            x = 0.0 if t <= 0 else (1.0 if t >= T else 0.5 - 0.5 * math.cos(math.pi * t / T))
        return LAM * (1 + amp * x)

    def accel(v, t):
        a = np.zeros_like(v)
        a[1:-1] = (v[2:] - 2 * v[1:-1] + v[:-2]) / DS ** 2 - 2 * v[1:-1] / si[1:-1] ** 2 - v[1:-1] * np.abs(v[1:-1]) / si[1:-1] + src(t) / si[1:-1]
        return a
    v_old = v_st.copy()
    v = v_old + 0.5 * DT ** 2 * accel(v_old, 0.0); v[0] = 0.0; v[-1] = v_old[-1]
    flux, nsteps = 0.0, int(round((T + 600) / DT))
    for nn in range(1, nsteps):
        t = nn * DT
        v_new = 2 * v - v_old + DT ** 2 * accel(v, t)
        v_new[0] = 0.0
        v_new[-1] = v[-1] + DT * (-(v[-1] - v[-2]) / DS + src(t) / S_MAX ** 2)
        flux += -((v[-1] - v[-2]) / DS) * ((v_new[-1] - v_old[-1]) / (2 * DT)) * DT
        v_old, v = v, v_new
    return flux


RAMP = {}
for T in (0, 3, 10, 30, 100, 300):
    RAMP[T] = run_ramp(T)
    P_(f"    T = {T:4d}: radiated {RAMP[T]:+.4e}" + (f"  ({RAMP[T] / RAMP[0]:.2e} of the step)" if RAMP[0] else ""))
if LAM > 0 and RAMP[30] > 0 and RAMP[300] > 0:
    pexp = math.log(abs(RAMP[300]) / abs(RAMP[30])) / math.log(10)
    P_(f"    slope d ln E_rad / d ln T over T = 30..300: {pexp:.2f}  (step -> slow: adiabatic suppression)")
    RES["numbers"]["ramp_slope"] = pexp
    P_("    physical T in code units = t_phys c_P / l_gamma; a 0.6-10 Gyr settling at c_P >= 5e-3 c, l_gamma <= 0.1 pc gives T >= 1e9.")
RES["numbers"]["ramp"] = RAMP
SIGNALS["ramp"] = max(abs(x) for x in RAMP.values())

# =============================================================== channels
P_("\n=== CHANNELS (worst corner of L* x c_P, each footing; verdict on the worst)")
VERD = {}


def verdict(sig, thr):
    r = sig / thr
    return ("OBSERVABLE" if r >= 1 else "NEAR THRESHOLD" if r >= 0.1 else "BELOW THRESHOLD"), r


def heat_per_mass(F, w, cp):                          # D5: absorption per length alpha = (w_J^2 W_I^2 / w^4) k; per unit mass F alpha/rho
    WI2 = 4 * np.pi * G * LAM ** 2 / ((2 * np.pi * G * (Ls_ * PC) ** 2) / (cp * C) ** 2)
    return 4 * np.pi * G * WI2 * F * LAM ** 2 / (w ** 3 * cp * C) if F > 0 else 0.0


# ---- C1 gas heating
P_("\nC1  gas heating. D5: I w^2 = gamma(k^2+m^2) - (4piG lam)^2 rho_b / w^2 (responsive baryons); absorbed fraction per radian")
P_("    <= w_J^2 W_I^2 / w^4 (W_I^2 = 4 pi G/I); heating per unit mass h = 4 pi G W_I^2 F / (w^3 c_P), taken at the lowest propagating w = c_P m.")
GASES = {"cluster ICM": ("cluster", 1e-3, 5e7, 500 * KPC), "galactic hot halo": ("galaxy", 1e-4, 2e6, 50 * KPC)}
C1 = {}
for gname, (h, ne, T, rr) in GASES.items():
    rho_g = 1.17 * MP * ne * 1e6
    cool = 2.4e-40 * math.sqrt(T) * (ne * 1e6) * (ne * 1e6 / 1.2) / rho_g
    worst = None
    for foot, a0 in FOOT.items():
        Mb = HALOS[h][0] * MSUN
        gN = G * Mb / rr ** 2
        for mode in ("L_relaxed", "L_merging"):
            Lc = SETTLE[(foot, h)][mode]
            F_ceil = Lc / (4 * np.pi * rr ** 2) * LAM
            for Ls_ in LSTAR:
                m = float(gap_m(np.array(gN), a0, Ls_ * PC))
                for cp in CPS:
                    w = cp * C * m if m > 0 else 1.0
                    hc = heat_per_mass(F_ceil, w, cp)
                    ha = hc * frac_rad(foot, h)
                    row = dict(foot=foot, mode=mode, Lstar=Ls_, cP=cp, h_ceiling=hc, h_actual=ha, cool=cool)
                    if worst is None or hc > worst["h_ceiling"]:
                        worst = row
    v_a, r_a = verdict(worst["h_actual"], 0.1 * cool)
    v_c, r_c = verdict(worst["h_ceiling"], 0.1 * cool)
    C1[gname] = dict(worst, verdict=v_a, ratio_actual=r_a, ratio_ceiling=r_c)
    P_(f"    {gname:17s}: cooling {cool:.2e} W/kg; worst corner ({worst['foot']}, {worst['mode']}, L* {worst['Lstar']} pc, c_P {worst['cP']} c): "
       f"no-trap ceiling h {worst['h_ceiling']:.2e} W/kg ({r_c:.1e} of 0.1 x cooling); with trapping {worst['h_actual']:.1e} -> {v_a}")
VERD["C1 gas heating"] = C1
SIGNALS["C1"] = max(max(v["h_ceiling"], v["h_actual"]) for v in C1.values())

# ---- C2 disc heating
P_("\nC2  disc heating, solar neighbourhood (R0 = 8 kpc, galaxy halo of S1). Stars are collisionless and w >= c_P m >> orbital frequencies,")
P_("    so the linear secular heating is zero (adiabatic); the number below is the D5 full-dissipation ceiling.")
thr2 = 0.1 * (20e3) ** 2 / (10 * GYR)
worst = None
for foot, a0 in FOOT.items():
    Mb = HALOS["galaxy"][0] * MSUN
    gN = G * Mb / (8 * KPC) ** 2
    for mode in ("L_relaxed", "L_merging"):
        F_ceil = SETTLE[(foot, "galaxy")][mode] / (4 * np.pi * (8 * KPC) ** 2) * LAM
        for Ls_ in LSTAR:
            m = float(gap_m(np.array(gN), a0, Ls_ * PC))
            for cp in CPS:
                w = cp * C * m if m > 0 else 1.0
                hc = heat_per_mass(F_ceil, w, cp)
                du = LAM * math.sqrt(16 * np.pi * G * cp * C * F_ceil) / (w * Ls_ * PC) if F_ceil > 0 else 0.0
                row = dict(foot=foot, mode=mode, Lstar=Ls_, cP=cp, h_ceiling=hc, h_actual=hc * frac_rad(foot, "galaxy"),
                           delta_u=du, delta_v=du / w)
                if worst is None or hc > worst["h_ceiling"]:
                    worst = row
v_a, r_a = verdict(worst["h_actual"], thr2)
_, r_c = verdict(worst["h_ceiling"], thr2)
VERD["C2 disc heating"] = dict(worst, threshold=thr2, verdict=v_a, ratio_actual=r_a, ratio_ceiling=r_c)
P_(f"    threshold 0.1 x sigma_z^2/10 Gyr = {thr2:.2e} W/kg; worst ({worst['foot']}, {worst['mode']}, L* {worst['Lstar']}, c_P {worst['cP']} c): "
   f"ceiling {worst['h_ceiling']:.2e} W/kg ({r_c:.1e}); forced oscillation dv {worst['delta_v']:.2e} m/s; with trapping {worst['h_actual']:.1e} -> {v_a}")
SIGNALS["C2"] = max(worst["h_ceiling"], worst["delta_v"])

# ---- C3 binary orbital decay
P_("\nC3  quadrupole P radiation from a binary in its screened core (sigma = 2 r_M^2/L*^2 << 1: linear; local gap from the Galaxy's u0):")
P_("    chi = div P obeys chi_tt/c_P^2 - lap chi = 4 pi G lam rho_b/gamma; flux c_P gamma chi^2 =>  Pow = G lam^2 (Idd_ii^2 + 2 Idd:Idd)/(30 L*^2 c_P^3)")
P_("    circular orbit: Pow/Pow_GR = lam^2 (1/12) (c/c_P)^3 (c/(w_orb L*))^2.  Double pulsar: P_b = 2.4545 h (e = 0.088 neglected).")
w_orb = 2 * np.pi / (2.4545 * 3600)
M_dp = (1.338 + 1.249) * MSUN
v_orb = (G * M_dp * w_orb) ** (1 / 3)
sig_dp = 2 * (G * M_dp / FOOT["canonical"]) / (5.75 * PC) ** 2
gN_sun = 1.3e-10
C3 = {}
for Ls in LSTAR:
    for cp in CPS:
        ratio = LAM ** 2 / 12 * (1 / cp) ** 3 * (C / (w_orb * Ls * PC)) ** 2
        mgap = max(float(gap_m(np.array(gN_sun), a0, Ls * PC)) for a0 in FOOT.values())
        C3[f"{Ls}|{cp}"] = dict(ratio=ratio, propagates=bool(2 * w_orb > cp * C * mgap), v_over_cP=v_orb / (cp * C))
worst3 = max(C3.values(), key=lambda r: r["ratio"])
v3, r3 = verdict(worst3["ratio"], 9e-5)
excl = {Ls: (LAM ** 2 / 12 * (C / (w_orb * Ls * PC)) ** 2 / 9e-5) ** (1 / 3) for Ls in LSTAR}
VERD["C3 binary decay"] = dict(worst=worst3, verdict=v3, ratio_to_room=r3, cP_excluded_below=excl, sigma_binary=sig_dp)
for Ls in LSTAR:
    P_(f"    L* {Ls:7.2f} pc: ratio " + ", ".join(f"c_P {cp}c: {C3[f'{Ls}|{cp}']['ratio']:.1e}" for cp in CPS)
       + f"   | room 9e-5 excludes c_P < {excl[Ls]:.1e} c")
P_(f"    binary sigma = {sig_dp:.1e} (screened, linear); v_orb/c_P at the floor = {v_orb / (5e-3 * C):.2f} (slow-motion OK);"
   f" all corners propagate (2w >> c_P m_gap): {all(r['propagates'] for r in C3.values())}")
P_(f"    worst corner {worst3['ratio']:.1e} vs room 9e-5 -> {v3} ({r3:.1e})")
SIGNALS["C3"] = worst3["ratio"]

# ---- C4 PTA
P_("\nC4  nHz band. Settling at w ~ 1/t_dyn is ~7 decades below the band and trapped (S2): no settling signal in band.")
P_("    SMBH binary (1e9 Msun, f_GW 1e-8 Hz): free ratio as C3; the binary sits where g_N ~ 1e9 a0, sigma = 2 r_M^2/L*^2 > 2,")
P_("    so the saturated vacuum (u -> a0) is NOT screened (stiffness shifts the source by 1 - 2/sigma); gap m = sqrt(2 w''(u))/L*.")
Mbh = 1e9 * MSUN
wo = np.pi * 1e-8
a_bin = (G * Mbh / wo ** 2) ** (1 / 3)
C4 = {}
for foot, a0 in FOOT.items():
    rMb = math.sqrt(G * Mbh / a0)
    for Ls in LSTAR:
        sig = 2 * rMb ** 2 / (Ls * PC) ** 2
        fac = max(1 - 2 / sig, 0.0)
        r = np.geomspace(a_bin, 1 * KPC, 6000)
        m = gap_m(fac * G * Mbh / r ** 2, a0, Ls * PC)
        for cp in CPS:
            free = LAM ** 2 / 12 * (1 / cp) ** 3 * (C / (wo * Ls * PC)) ** 2
            kap = np.sqrt(np.clip(m ** 2 - (2 * wo / (cp * C)) ** 2, 0, None))
            tau = float(np.trapz(kap, r))
            esc = free * math.exp(-2 * tau) if free > 0 else 0.0
            C4[f"{foot}|{Ls}|{cp}"] = dict(sigma=sig, free_ratio=free, tau=tau, escaped_ratio=esc,
                                           gap_over_w_at_source=float(cp * C * m[0] / (2 * wo)))
worst4 = max(C4.items(), key=lambda kv: kv[1]["escaped_ratio"])
maxfree = max(C4.items(), key=lambda kv: kv[1]["free_ratio"])
v4, r4 = verdict(worst4[1]["escaped_ratio"], 0.1)
VERD["C4 PTA"] = dict(worst_escaped=worst4, verdict=v4, ratio=r4)
P_(f"    a_bin = {a_bin / PC:.3f} pc; largest FREE ratio {maxfree[1]['free_ratio']:.1e} at {maxfree[0]} (gap/w at source {maxfree[1]['gap_over_w_at_source']:.1e}, tau {maxfree[1]['tau']:.2e})")
P_(f"    min tau over window {min(v['tau'] for v in C4.values()):.2e}; worst ESCAPED ratio {worst4[1]['escaped_ratio']:.1e} ({worst4[0]}) -> {v4}")
P_(f"    local propagation at the Sun needs w > c_P m(u0): band edge 2pi x 2 nHz vs gap {max(CPS) * C * float(gap_m(np.array(gN_sun), FOOT['alt'], 5.75 * PC)):.1e} s^-1 (c_P = c, L* 5.75)")
SIGNALS["C4"] = worst4[1]["escaped_ratio"]

# ---- C5 lensing
P_("\nC5  merging cluster (Bullet-like: M_b 1e14, v 4500 km/s, R 500 kpc). Below the gap the response is in phase (no dissipation but")
P_("    trapped radiation): fractional profile change (w/w_m)^2 with w = v/R; even-in-v, so no centroid shift. Ceiling if fully damped: v/w_m.")
vB, RB, MB = 4.5e6, 500 * KPC, 1e14 * MSUN
worst5 = None
for foot, a0 in FOOT.items():
    m = float(gap_m(np.array(G * MB / RB ** 2), a0, 1.0))
    for Ls in LSTAR:
        for cp in CPS:
            wm = cp * C * m / (Ls * PC) if m > 0 else 0.0
            frac = LAM * (vB / RB / wm) ** 2 if wm > 0 else 0.0
            off_ceiling = LAM * vB / wm if wm > 0 else 0.0
            off_actual = off_ceiling * frac_rad(foot, "cluster")
            row = dict(foot=foot, Lstar=Ls, cP=cp, frac=frac, offset_ceiling_kpc=off_ceiling / KPC, offset_actual_kpc=off_actual / KPC,
                       superluminal_bulk=bool(vB > cp * C))
            if worst5 is None or frac > worst5["frac"]:
                worst5 = row
v5a, r5a = verdict(worst5["frac"], 0.05)
v5b, r5b = verdict(worst5["offset_actual_kpc"], 10.0)
_, r5c = verdict(worst5["offset_ceiling_kpc"], 10.0)
VERD["C5 lensing"] = dict(worst5, verdict_frac=v5a, ratio_frac=r5a, verdict_offset=v5b, ratio_offset=r5b, ratio_offset_ceiling=r5c)
P_(f"    worst ({worst5['foot']}, L* {worst5['Lstar']} pc, c_P {worst5['cP']} c): profile change {worst5['frac']:.1e} (vs 0.05: {v5a}, {r5a:.1e});"
   f" offset {worst5['offset_actual_kpc']:.1e} kpc ({v5b}); fully-damped ceiling {worst5['offset_ceiling_kpc']:.2f} kpc ({r5c:.2f} of 10 kpc)")
P_(f"    NOTE: v_bulk 4500 km/s > c_P at the 5e-3 c floor: {worst5['superluminal_bulk']} -> the c_P floor must sit above bulk speeds (Cherenkov),"
   " a consistency bound, not a signature.")
SIGNALS["C5"] = max(worst5["frac"], worst5["offset_ceiling_kpc"])

# ---- C6 light
P_("\nC6  light: no P-photon term in the action -> REQUIRES NEW COUPLING (not added). Via gravity (if Psi = Phi), the cosmic ceiling")
worst6 = 0.0
for foot, a0 in FOOT.items():
    for Ls in LSTAR:
        m_edge = float(gap_m(np.array(G * 1e14 * MSUN / (2 * MPC) ** 2), a0, Ls * PC))
        for cp in CPS:
            w = cp * C * m_edge if m_edge > 0 else 1.0
            du = LAM * 4 * cp * C * math.sqrt(np.pi * G * u_cos) / (w * Ls * PC) if u_cos > 0 else 0.0
            dphi = du / (w / (cp * C)) / C ** 2
            worst6 = max(worst6, dphi)
v6, r6 = verdict(worst6, 1e-5)
VERD["C6 light"] = dict(direct="REQUIRES NEW COUPLING", via_gravity_dPhi_over_c2=worst6, verdict_via_gravity=v6, ratio=r6)
P_(f"    P-wave energy (u_P {u_cos:.1e} J/m^3, at the lowest propagating w) gives dPhi/c^2 <= {worst6:.1e} (time-varying; vs 1e-5 CMB-level "
   f"anisotropy: {v6}, {r6:.1e}); trapping removes even this.")
SIGNALS["C6"] = worst6

# =============================================================== verdict
P_("\n=== VERDICT (frozen rule; worst corner)")
table = [("C1 gas heating (cluster ICM)", C1["cluster ICM"]["verdict"], f"{C1['cluster ICM']['ratio_actual']:.0e} (no-trap ceiling {C1['cluster ICM']['ratio_ceiling']:.0e})"),
         ("C1 gas heating (hot halo)", C1["galactic hot halo"]["verdict"], f"{C1['galactic hot halo']['ratio_actual']:.0e} (ceiling {C1['galactic hot halo']['ratio_ceiling']:.0e})"),
         ("C2 disc heating", VERD["C2 disc heating"]["verdict"], f"{VERD['C2 disc heating']['ratio_actual']:.0e} (ceiling {VERD['C2 disc heating']['ratio_ceiling']:.0e})"),
         ("C3 binary decay", v3, f"{r3:.1e} of room; excludes c_P < {excl[5.75]:.1e} c at L* 5.75 pc"),
         ("C4 PTA", v4, f"{r4:.0e}"),
         ("C5 lensing (profile / offset)", f"{v5a} / {v5b}", f"{r5a:.0e} / {r5b:.0e} (fully-damped ceiling {r5c:.2f})"),
         ("C6 light", "REQUIRES NEW COUPLING", f"via gravity {r6:.0e}")]
for name, v, r in table:
    P_(f"    {name:32s} {v:28s} {r}")
RES["verdict_table"] = table
RES["signals"] = SIGNALS

if MUT:
    nonzero = {k: v for k, v in SIGNALS.items() if abs(v) > 0}
    RES["control"] = dict(all_zero=not nonzero, nonzero=nonzero)
    P_(f"\nMUTATE (lam = 0): every channel zero: {not nonzero}" + (f"; non-zero: {nonzero}" if nonzero else ""))
    rc = 1 if nonzero else 0
else:
    rc = 0 if RES["checks"]["K1 E_code(200) = CFG696 released energy for the zero start (2.99995) within 2%"]["ok"] else 1
json.dump(RES, open(os.path.join(HERE, f"cfg659_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(rc)
