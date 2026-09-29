#!/usr/bin/env python3
"""CFG94 -- independent re-derivation of the enclosed-mass-exchange headline numbers (CFG48 G4 / CFG70).
Spec: FROZEN.md + AMENDMENT0_prerun.md in this directory (written before any run). Modes: MUTATE=1 (u = 1*P instead of 3/2*P),
MUTATE=2 (probe raises M_enc of every shell, not only s > q). Exit 0 iff every control and reproduction gate passes."""
import os, sys, math, itertools, hashlib
import numpy as np
from scipy import integrate, optimize, special
import mpmath as mp

MODE = os.environ.get("MUTATE", "0")
OUT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cfg94_main.out" if MODE == "0" else f"cfg94_MUTATE{MODE}.out"), "w")
FAILS = []
GATES = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); OUT.write(s + "\n"); OUT.flush()


def check(name, ok, detail=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name} {detail}")
    if not ok:
        FAILS.append(name)


def gate(name, ok, detail=""):
    P(f"  [{'MATCH' if ok else 'NO-MATCH'}] {name} {detail}")
    GATES.append((name, ok))


for f in ("FROZEN.md", "AMENDMENT0_prerun.md"):
    P(f"sha256 {f}: {hashlib.sha256(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f), 'rb').read()).hexdigest()[:16]}")
P(f"MODE = {MODE}")

# ---------------------------------------------------------------------------------------------- constants
G = 6.6743e-11; MSUN = 1.98841e30; KPC = 3.0856776e19; MPC = 1e3 * KPC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
OM, HH, OCH2, OBH2 = 0.3153, 0.6736, 0.1200, 0.02237
OL = 1 - OM
H0 = 100 * HH * 1e3 / MPC
RHOC = 3 * H0 ** 2 / (8 * math.pi * G)
RHOM = OM * RHOC
OC_OB = OCH2 / OBH2
LAM_HEAD = {"0": 1.5, "1": 1.0, "2": 1.5}[MODE]          # internal-energy coefficient u = lambda P
P(f"H0 = {H0*MPC/1e3:.3f} km/s/Mpc; rho_m = {RHOM*MPC**3/MSUN:.4e} Msun/Mpc^3; Omega_c/Omega_b = {OC_OB:.4f}; lambda = {LAM_HEAD}")


# ---------------------------------------------------------------------------------------------- spherical collapse (turnaround today)
def delta_ta(Om, Ol=None):
    """1+delta at turnaround for a shell that turns around today: time from R=0 to R_ta equals the age of a flat LCDM universe."""
    Ol = 1 - Om if Ol is None else Ol
    t0 = 2 / (3 * math.sqrt(Ol)) * math.asinh(math.sqrt(Ol / Om)) if Ol > 0 else 2 / 3   # in 1/H0
    def tsh(D):
        A, B = Om * D, Ol
        f = lambda th: 2 * math.sin(th) ** 2 / math.sqrt(A - B * math.sin(th) ** 2 * (1 + math.sin(th) ** 2))
        return integrate.quad(f, 0, math.pi / 2, epsabs=1e-14, epsrel=1e-14)[0]
    lo = 2 * Ol / Om * 1.0000001 if Ol > 0 else 1.0
    D = optimize.brentq(lambda D: tsh(D) - t0, lo + 1e-6, 1e3, xtol=1e-14, rtol=1e-14)
    return D, tsh(D) - t0


D_EDS, _ = delta_ta(1.0, 0.0)
DTA_OWN, resid = delta_ta(OM)
DTA = {"own": DTA_OWN, "CFG48 11.81": 11.81, "EdS 5.552": (3 * math.pi / 4) ** 2, "r200c": 200 * RHOC / RHOM}
P(f"Delta_ta(EdS) = {D_EDS:.6f} (analytic {(3*math.pi/4)**2:.6f}); Delta_ta(Om={OM}) own = {DTA_OWN:.5f} (time residual {resid:.1e})")
check("C6a EdS turnaround (3pi/4)^2", abs(D_EDS / (3 * math.pi / 4) ** 2 - 1) < 1e-5, f"rel {D_EDS/(3*math.pi/4)**2-1:.2e}")
check("C6b time residual < 1e-8", abs(resid) < 1e-8, f"{resid:.1e}")


# ---------------------------------------------------------------------------------------------- kernels
def nu_p2(y):
    return np.sqrt(1 + 1 / np.asarray(y, float))


def nu_rar(y):
    y = np.asarray(y, float)
    return 1 / (-np.expm1(-np.sqrt(y)))


def hrar(y):
    y = np.asarray(y, float)
    return y / np.expm1(np.minimum(np.sqrt(y), 600.0))


def dhrar(y):
    t = np.minimum(np.sqrt(np.asarray(y, float)), 600.0); e = np.expm1(t)
    return (e - t * (e + 1) / 2) / e ** 2


YP = optimize.brentq(lambda y: float(dhrar(y)), 1.0, 5.0, xtol=1e-14)
HP = float(hrar(YP))
LN = np.linspace(-32, 32, 400001)                       # ln y grid
YG = np.exp(LN)
DH = np.maximum(dhrar(YG), 0.05 * HP / (YG + YP))
dy_dl = YG                                              # d y = y d ln y
HM = float(hrar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] * YG[1:] + DH[:-1] * YG[:-1]) * np.diff(LN))])


def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-13)
    return 1 + np.interp(np.log(y), LN, HM) / y


P(f"y_p (h_RAR' = 0) = {YP:.5f}, h_p = {HP:.5f}")
ys = np.geomspace(1e-6, 1.0, 60)
dev1 = np.max(np.abs(nu_mono(ys) / nu_rar(ys) - 1))
ys2 = np.geomspace(1.0, YP, 40)
dev2 = np.max(np.abs(nu_mono(ys2) / nu_rar(ys2) - 1))
ys3 = np.geomspace(1e-3, 30, 100)
dev3 = np.max(np.abs(nu_mono(ys3) / nu_rar(ys3) - 1))
check("C7a nu_mono = nu_RAR for y<=1 (<=1e-3)", dev1 <= 1e-3, f"max rel dev {dev1:.2e}; (1,y_p] reported dev {dev2:.2e}")
check("C7b nu_mono/nu_RAR-1 <= 3% up to y=30", dev3 <= 0.03, f"{dev3:.3e}")
check("C7c h_mono nondecreasing", bool(np.all(np.diff(HM) >= -1e-15)))


# ---------------------------------------------------------------------------------------------- scales
def r_M(M, a0):                      # M in Msun
    return math.sqrt(G * M * MSUN / a0)


def rta_A(M, D):
    Mcol = M * (1 + OC_OB) * MSUN
    return (Mcol / (4 / 3 * math.pi * D * RHOM)) ** (1 / 3)


def rta_B(M, D, nu, a0):
    Mb = M * MSUN
    f = lambda lr: math.log(Mb * float(nu(G * Mb / (math.exp(lr) ** 2 * a0 ))) / (4 / 3 * math.pi * math.exp(lr) ** 3 * RHOM)) - math.log(D)
    return math.exp(optimize.brentq(f, math.log(1e-3 * KPC), math.log(1e3 * MPC), xtol=1e-13))


a0c = A0["canonical"]
check("C8a r_M(1e10) = 3.86 kpc", abs(r_M(1e10, a0c) / KPC - 3.86) < 0.02, f"{r_M(1e10, a0c)/KPC:.4f}")
check("C8b r_ta(A, 1e10) = 319 kpc within 1%", abs(rta_A(1e10, DTA_OWN) / KPC / 319 - 1) < 0.01, f"{rta_A(1e10, DTA_OWN)/KPC:.2f} kpc (Delta {DTA_OWN:.3f}); with 11.81: {rta_A(1e10, 11.81)/KPC:.2f}")

# ---------------------------------------------------------------------------------------------- target profile (C1, C2)
P("\n== C1/C2 target profile from C(r) = rho_c r^3 g_tot = (a0/4pi) M_b(<r), point mass ==")
M0 = 1e10 * MSUN; a0 = a0c; rM = math.sqrt(G * M0 / a0)


def g_law(r):
    gN = G * M0 / r ** 2
    return math.sqrt(gN ** 2 + a0 * gN)


def rho_c(r):
    return a0 * M0 / (4 * math.pi * r ** 3 * g_law(r))


okC1 = True
for x in (0.3, 1, 3, 30):
    Mc = integrate.quad(lambda lr: 4 * math.pi * math.exp(lr) ** 3 * rho_c(math.exp(lr)), math.log(1e-9 * rM), math.log(x * rM), epsabs=0, epsrel=1e-13, limit=400)[0]
    ex = M0 * (math.sqrt(1 + x * x) - 1)
    rel = Mc / ex - 1
    okC1 &= abs(rel) < 1e-7
    P(f"    x={x:5g}: M_c(<r)/[M(sqrt(1+x^2)-1)] - 1 = {rel:.2e}")
check("C1 M_c closed form", okC1)
okC2 = True
for x in (0.3, 1, 3, 30):
    r = x * rM
    Pf = lambda rr: a0 * M0 / (8 * math.pi * rr ** 2)
    h = r * 1e-4
    dP = (Pf(r + h) - Pf(r - h)) / (2 * h)
    Mc = M0 * (math.sqrt(1 + x * x) - 1)
    lhs = -dP; rhs = rho_c(r) * G * (M0 + Mc) / r ** 2
    s2 = Pf(r) / rho_c(r); vc2 = r * g_law(r)
    okC2 &= abs(lhs / rhs - 1) < 1e-6 and abs(s2 / (vc2 / 2) - 1) < 1e-12
    P(f"    x={x:5g}: hydrostatic {lhs/rhs-1:.2e}; sigma^2/(V_c^2/2)-1 = {s2/(vc2/2)-1:.2e}")
check("C2 hydrostatics + sigma^2=V_c^2/2", okC2)


# ---------------------------------------------------------------------------------------------- the exchange functional (numerical)
def erfstep(t):
    return 0.5 * (1 + special.erf(t))


def u_P(s, Menc, lam):            # energy density, pressure-slaved
    return lam * a0 * Menc / (8 * math.pi * s ** 2)


def eps_sigma(s, Menc, lam):      # energy per unit mass, sigma-slaved, u = lam*P -> lam*sigma^2 (P = rho sigma^2)
    gN = G * Menc / s ** 2
    return lam * (s / 2) * math.sqrt(gN ** 2 + a0 * gN) / 1.0 * 0.5 * 2      # lam * sigma^2, sigma^2 = (s/2) g


def dE_dq(reading, q, w, h, m, lam):
    """-(1/m) [E(q+h)-E(q-h)]/(2h): the difference of the two total energies is integrated as one integrand (their common part cancels
    identically); symmetrised in +-m. Positive = outward."""
    def Mnc(s, qq, mm):
        if MODE == "2":
            return M0 + mm                                  # MUTATE 2: every shell sees the probe
        return M0 + mm * erfstep((s - qq) / w)

    def integrand(s, mm):
        if reading == "P":
            wt = 4 * math.pi * s ** 2
            return wt * (u_P(s, Mnc(s, q + h, mm), lam) - u_P(s, Mnc(s, q - h, mm), lam))
        wt = 4 * math.pi * s ** 2 * rho_c(s)
        return wt * (eps_sigma(s, Mnc(s, q + h, mm), lam) - eps_sigma(s, Mnc(s, q - h, mm), lam))
    lo, hi = q - 14 * w, q + 14 * w + h
    res = []
    for mm in (m, -m):
        v = integrate.quad(integrand, lo, hi, args=(mm,), epsabs=0, epsrel=1e-12, limit=500, points=[q - 3 * w, q, q + 3 * w])[0]
        res.append(-(v / (2 * h)) / mm)
    return 0.5 * (res[0] + res[1])


def react_numeric(reading, x, lam):
    q = x * rM
    out = []
    for wr in (1e-3, 5e-4):
        w = wr * q
        out.append(dE_dq(reading, q, w, w / 50, 1e-4 * M0, lam))
    return 2 * out[1] - out[0]                                # Richardson in w


def react_closed(reading, x, lam):                            # derived: a/g_law with u = lam*P
    s = math.sqrt(1 + x * x)
    if reading == "P":
        return (lam / 2) * x * x / s                          # (lam/2) a0 / g_law
    return (lam / 4) * (2 + x * x) / (1 + x * x) * x * x / s


# symbolic derivation (own): a = 4 pi q^2 d(u)/dM_enc (P) ; 4 pi q^2 rho_c d(eps)/dM_enc (sigma)
import sympy as sp
q_, M_, a0_, G_, lam_, X = sp.symbols("q M a0 G lam X", positive=True)
Me = sp.Symbol("Me", positive=True)
uP = lam_ * a0_ * Me / (8 * sp.pi * q_ ** 2)
gN = G_ * Me / q_ ** 2
sig2 = (q_ / 2) * sp.sqrt(gN ** 2 + a0_ * gN)
gl = sp.sqrt((G_ * M_ / q_ ** 2) ** 2 + a0_ * G_ * M_ / q_ ** 2)
rhoc_ = a0_ * M_ / (4 * sp.pi * q_ ** 3 * gl)
aP = (4 * sp.pi * q_ ** 2 * sp.diff(uP, Me)).subs(Me, M_)
aS = (4 * sp.pi * q_ ** 2 * rhoc_ * lam_ * sp.diff(sig2, Me)).subs(Me, M_)
rM_ = sp.sqrt(G_ * M_ / a0_)
subx = {q_: X * rM_}
rP = sp.simplify((aP / gl).subs(subx)); rS = sp.simplify((aS / gl).subs(subx))
P(f"\nsympy: a_P/g_law = {rP};   a_sigma/g_law = {rS}")
for xx in (0.3, 1.0, 3.0, 10.0, 30.0):
    vP = float(rP.subs({X: xx, lam_: 1.5})); vS = float(rS.subs({X: xx, lam_: 1.5}))
    assert abs(vP / react_closed("P", xx, 1.5) - 1) < 1e-12 and abs(vS / react_closed("S", xx, 1.5) - 1) < 1e-12, "sympy vs closed form"
P("  sympy result equals the closed forms used below to 1e-12 (lam = 3/2) at the five x")

# ---------------------------------------------------------------------------------------------- reaction table
P("\n== Reaction on the baryons, a/g_law, lambda = %.3g (point mass, canonical a0) ==" % LAM_HEAD)
XS = (0.3, 1.0, 3.0, 10.0, 30.0)
TP = dict(zip(XS, (0.065, 0.53, 2.13, 7.46, 22.5)))
TS = dict(zip(XS, (0.062, 0.398, 1.17, 3.77, 11.3)))
num = {}
P("   x      P numeric   P closed    P printed | S numeric   S closed    S printed")
okC3 = True
for x in XS:
    nP = react_numeric("P", x, LAM_HEAD); nS = react_numeric("S", x, LAM_HEAD)
    gl_x = g_law(x * rM)
    nPr, nSr = nP / gl_x, nS / gl_x
    cP, cS = react_closed("P", x, LAM_HEAD), react_closed("S", x, LAM_HEAD)
    num[x] = (nPr, nSr)
    okC3 &= abs(nPr / cP - 1) < 1e-3 and abs(nSr / cS - 1) < 1e-3
    P(f"  {x:5g}  {nPr:10.5f}  {cP:10.5f}  {TP[x]:8g}   | {nSr:10.5f}  {cS:10.5f}  {TS[x]:8g}   (num/closed-1: {nPr/cP-1:+.1e}, {nSr/cS-1:+.1e})")
check("C3 numerical bilocal-energy derivative = closed form (1e-3)", okC3)
# independent brute force with mpmath: total energies (no differencing of integrands) for sigma reading at x=1
mp.mp.dps = 30
if MODE != "2":
    x = 1.0; q = mp.mpf(x * rM); w = q * mp.mpf("1e-3"); m = mp.mpf(1e-4 * M0); h = w / 50
    Gm, a0m, M0m = mp.mpf(G), mp.mpf(a0), mp.mpf(M0)
    def Etot(qq):
        def f(s):
            Menc = M0m + m * (1 + mp.erf((s - qq) / w)) / 2
            gNm = Gm * Menc / s ** 2
            gl0 = mp.sqrt((Gm * M0m / s ** 2) ** 2 + a0m * Gm * M0m / s ** 2)
            rc = a0m * M0m / (4 * mp.pi * s ** 3 * gl0)
            return 4 * mp.pi * s ** 2 * rc * mp.mpf(LAM_HEAD) * (s / 2) * mp.sqrt(gNm ** 2 + a0m * gNm)
        pts = [mp.mpf(1e-6) * q, qq - 20 * w, qq - 5 * w, qq, qq + 5 * w, qq + 20 * w, 40 * q]
        return mp.quad(f, pts)
    Fmp = -(Etot(q + h) - Etot(q - h)) / (2 * h) / m
    Fq = float(Fmp) / g_law(x * rM)
    P(f"  brute-force mpmath total-energy difference (sigma, x=1, w=1e-3 q, m/M=1e-4, no Richardson): {Fq:.6f}; closed {react_closed('S', 1.0, LAM_HEAD):.6f}; (w-dependence O(1e-3))")
    check("C3b brute-force total-energy differencing within 2e-3", abs(Fq / react_closed("S", 1.0, LAM_HEAD) - 1) < 2e-3, f"{Fq/react_closed('S',1.0,LAM_HEAD)-1:+.2e}")

# asymptotics C4
xs_lo, xs_hi = 1e-3, 1e4
okC4 = True
for rd in ("P", "S"):
    lo = react_closed(rd, xs_lo, 1.5) / (0.75 * xs_lo ** 2)
    hi = react_closed(rd, xs_hi, 1.5) / ((0.75 if rd == "P" else 0.375) * xs_hi)
    okC4 &= abs(lo - 1) < 1e-2 and abs(hi - 1) < 1e-3
    P(f"  asymptotics {rd}: lo/(3/4 x^2) = {lo:.6f}, hi/(coefficient * x) = {hi:.6f}")
check("C4 x->0, x->inf asymptotics", okC4)
# also with the numerical operator at x = 1e-3 and 1e3 (not only closed forms)
if MODE == "0":
    xl = 1e-2
    nl = react_numeric("P", xl, LAM_HEAD) / g_law(xl * rM) / (0.75 * xl ** 2)
    xh = 1e3
    nh = react_numeric("S", xh, LAM_HEAD) / g_law(xh * rM) / (0.375 * xh)
    P(f"  numerical operator: P at x=1e-2 / (3/4 x^2) = {nl:.5f};  sigma at x=1e3 / (3/8 x) = {nh:.5f}")
    check("C4b numerical operator asymptotics (2e-2)", abs(nl - 1) < 2e-2 and abs(nh - 1) < 2e-2)

# crossing
cross = {rd: optimize.brentq(lambda x: react_closed(rd, x, LAM_HEAD) - 0.10, 0.05, 5) for rd in ("P", "S")}
P(f"  0.10 g_law crossing: pressure x = {cross['P']:.4f}, sigma x = {cross['S']:.4f}")

# gates R1
P("\n== R1 gates: numerical reaction vs printed (relative <= 0.5%) ==")
for x in XS:
    gate(f"R1 P x={x:g}", abs(num[x][0] / TP[x] - 1) <= 0.005, f"{num[x][0]:.4f} vs {TP[x]}")
for x in XS:
    if x == 30.0:
        gate("R1 sigma x=30 in [11.0,12.0)", 11.0 <= num[x][1] < 12.0, f"{num[x][1]:.4f} vs 11.x (CFG70 11.3)")
    else:
        gate(f"R1 sigma x={x:g}", abs(num[x][1] / TS[x] - 1) <= 0.005, f"{num[x][1]:.4f} vs {TS[x]}")
gate("R1 crossing x=0.38 (2 digits, pressure)", round(cross["P"], 2) == 0.38, f"{cross['P']:.4f}")

# ---------------------------------------------------------------------------------------------- energy
P("\n== Energy the exchange must supply, E_c(<r_e) / (1/2 M V_f^2), V_f^4 = G M a0, r_e = 0.4 r_ta ==")


def E_ratio_numeric(M, re, a0_, lam):
    Mb = M * MSUN; rMm = math.sqrt(G * Mb / a0_)
    # target profile for this mass
    def gl(r):
        gN = G * Mb / r ** 2
        return math.sqrt(gN ** 2 + a0_ * gN)
    def rc(r):
        return a0_ * Mb / (4 * math.pi * r ** 3 * gl(r))
    Ep = integrate.quad(lambda lr: math.exp(lr) ** 3 * 4 * math.pi * lam * a0_ * Mb / (8 * math.pi * math.exp(lr) ** 2),
                        math.log(1e-8 * rMm), math.log(re), epsabs=0, epsrel=1e-12)[0]      # int 4 pi s^2 u ds, ds = s dlns
    Es = integrate.quad(lambda lr: 4 * math.pi * math.exp(lr) ** 3 * rc(math.exp(lr)) * lam * (math.exp(lr) / 2) * gl(math.exp(lr)),
                        math.log(1e-8 * rMm), math.log(re), epsabs=0, epsrel=1e-12)[0]
    Vf2 = math.sqrt(G * Mb * a0_)
    return Ep / (0.5 * Mb * Vf2), Es / (0.5 * Mb * Vf2), re / rMm


TE_A = {1e9: 72.8, 1e10: 49.6, 1e12: 23.0}
TE_B = {1e9: 318, 1e10: 179, 1e12: 57}
P("  convention A (CFG48: collapse mass), Delta_ta = own / 11.81")
eA = {}
for M in (1e9, 1e10, 1e12):
    row = []
    for dn in ("own", "CFG48 11.81"):
        re = 0.4 * rta_A(M, DTA[dn]) if MODE != "x" else 0
        eP, eS, xe = E_ratio_numeric(M, re, a0c, LAM_HEAD)
        row.append((eP, eS, xe))
    eA[M] = row
    P(f"   M={M:.0e}: own: P {row[0][0]:.3f} sigma {row[0][1]:.3f} (x_e={row[0][2]:.2f}; 1.5 x_e/1.5*lam = {LAM_HEAD*row[0][2]:.3f});  Delta 11.81: {row[1][0]:.3f}   printed {TE_A[M]}")
    gate(f"R2 A M={M:.0e} (own Delta)", abs(row[0][0] / TE_A[M] - 1) <= 0.005, f"{row[0][0]:.3f} vs {TE_A[M]} ({row[0][0]/TE_A[M]-1:+.2%}); with 11.81: {row[1][0]:.3f} ({row[1][0]/TE_A[M]-1:+.2%})")
P("  convention B (committed: law's enclosed mass, phantom included), canonical a0")
eB = {}
for M in (1e9, 1e10, 1e12):
    rr = {}
    for kn, kf in (("nu_mono", nu_mono), ("P2", nu_p2), ("RAR", nu_rar)):
        for dn in ("own", "CFG48 11.81"):
            re = 0.4 * rta_B(M, DTA[dn], kf, a0c)
            rr[(kn, dn)] = E_ratio_numeric(M, re, a0c, LAM_HEAD)[0]
    eB[M] = rr
    P(f"   M={M:.0e}: nu_mono {rr[('nu_mono','own')]:.2f} (11.81: {rr[('nu_mono','CFG48 11.81')]:.2f}) | P2 {rr[('P2','own')]:.2f} | RAR {rr[('RAR','own')]:.2f}   printed {TE_B[M]}")
    v = rr[("nu_mono", "own")]
    gate(f"R2 B nu_mono M={M:.0e}", abs(v / TE_B[M] - 1) <= 0.005, f"{v:.2f} vs {TE_B[M]} ({v/TE_B[M]-1:+.2%}); with 11.81: {rr[('nu_mono','CFG48 11.81')]:.2f} ({rr[('nu_mono','CFG48 11.81')]/TE_B[M]-1:+.2%})")
# C5
xe0 = 0.4 * rta_A(1e10, DTA_OWN) / r_M(1e10, a0c)
eP0, eS0, _ = E_ratio_numeric(1e10, 0.4 * rta_A(1e10, DTA_OWN), a0c, 1.5)
eP_z, eS_z, _ = E_ratio_numeric(1e10, 0.4 * rta_A(1e10, DTA_OWN), a0c, 0.0)
rz = react_closed("P", 3.0, 0.0)
check("C5a lambda->0: energy and reaction vanish", abs(eP_z) < 1e-30 * abs(eP0) and abs(eS_z) < 1e-30 * abs(eS0) and abs(rz) < 1e-30, f"E {eP_z:.1e}, {eS_z:.1e}; a {rz:.1e}")
Ere = 0.4 * rta_A(1e10, DTA_OWN)
aP_coef = react_closed("P", 100.0, 1.5) * g_law(100 * rM) / a0c            # -> 3/4 exactly
lockratio = eP0 * 0.5 * 1e10 * MSUN * math.sqrt(G * 1e10 * MSUN * a0c) / (aP_coef * a0c * 1e10 * MSUN * Ere) if True else 0
check("C5b E_c = a_react(P) M r_e (locked)", abs(lockratio - 1) < 1e-9, f"{lockratio-1:+.1e}; a/a0 = {aP_coef:.6f}; sigma/P E identical: {eS0/eP0-1:+.1e}")
check("C5c 1.5 x_e closed form", abs(eP0 / (1.5 * xe0) - 1) < 1e-9, f"{eP0:.4f} vs {1.5*xe0:.4f}")

# ---------------------------------------------------------------------------------------------- convention sweep
P("\n== Convention sweep and the pass-line test (declared S1-S10) ==")
RATA = {}
def edge_x(M, conv, dn, a0n, frac):
    a0v = A0[a0n]
    if conv == "A":
        r = rta_A(M, DTA[dn])
    else:
        kf = {"Bmono": nu_mono, "BP2": nu_p2, "BRAR": nu_rar}[conv]
        key = (M, conv, dn, a0n)
        if key not in RATA:
            RATA[key] = rta_B(M, DTA[dn], kf, a0v)
        r = RATA[key]
    return frac * r / r_M(M, a0v)


XGRID = np.geomspace(0.3, 30, 400)
def react_max(reading, lam, ref, xmax):
    xg = XGRID[XGRID <= xmax]
    if len(xg) == 0:
        return 0.0
    v = np.array([react_closed(reading, x, lam) for x in xg])
    if ref == "gN":
        v = v * np.sqrt(1 + xg ** 2)
    return float(v.max())


best = None; npass = 0; ncomb = 0
worst_tab = []
Ms = (1e8, 1e9, 1e10, 1e11, 1e12, 1e13, 1e14)
convs = ("A", "Bmono", "BP2", "BRAR")
combos = itertools.product(Ms, convs, DTA.keys(), ("canonical", "alt"), (0.31, 0.40, 0.48), ("P", "S"), (1.5, 1.0, 0.5, 3.0), ("gLaw", "gN"), ("full", "edge"), (1.0, math.sqrt(2), 2.0))
sweep_rows = {}
for M, conv, dn, a0n, frac, rd, lam, ref, rng, vm in combos:
    xe = edge_x(M, conv, dn, a0n, frac)
    xmax = 30.0 if rng == "full" else min(30.0, xe)
    R = react_max(rd, lam, ref, xmax)
    E = lam * xe / vm
    ncomb += 1
    ok = (R <= 0.10) and (E <= 1.0)
    npass += ok
    score = max(R / 0.10, E)
    if best is None or score < best[0]:
        best = (score, dict(M=M, conv=conv, Delta=dn, a0=a0n, frac=frac, reading=rd, lam=lam, ref=ref, range=rng, Vmult=vm), R, E, xe)
    if rng == "full" and ref == "gLaw" and rd == "P" and lam == 1.5 and vm == 1.0 and a0n == "canonical" and frac == 0.40 and dn == "own":
        sweep_rows[(M, conv)] = E
P(f"  combinations scanned: {ncomb}; combinations passing BOTH lines: {npass}")
P(f"  best (smallest max(R/0.10, E)) = {best[0]:.3f}  ->  {best[1]}  R={best[2]:.4f} g, E={best[3]:.3f}, x_e={best[4]:.3f}")
P("  headline-convention energy ratio E_c/(1/2 M V_f^2) (P, lambda=3/2, canonical, own Delta, 0.40) by mass and r_ta convention:")
for M in Ms:
    P(f"     M={M:.0e}: " + "  ".join(f"{c}: {sweep_rows[(M,c)]:8.2f}" for c in convs))
# restricted sweeps that vary one thing from the headline (sensitivity)
P("  one-at-a-time sensitivity of the energy ratio at M=1e10 (headline A, own Delta, canonical, 0.40, lambda 3/2 = %.2f):" % (1.5 * edge_x(1e10, "A", "own", "canonical", 0.40)))
for label, kw in (("edge 0.31", dict(frac=0.31)), ("edge 0.48", dict(frac=0.48)), ("Delta 11.81", dict(dn="CFG48 11.81")), ("Delta EdS 5.552", dict(dn="EdS 5.552")),
                  ("Delta r200c", dict(dn="r200c")), ("a0 alt", dict(a0n="alt")), ("B nu_mono", dict(conv="Bmono")), ("B P2", dict(conv="BP2"))):
    args = dict(conv="A", dn="own", a0n="canonical", frac=0.40); args.update(kw)
    P(f"     {label:16s}: {1.5*edge_x(1e10, args['conv'], args['dn'], args['a0n'], args['frac']):9.3f}")
P("  lambda thresholds (u = lambda P): ")
lam_R = {}
for rd in ("P", "S"):
    for ref in ("gLaw", "gN"):
        base = react_max(rd, 1.0, ref, 30.0)
        lam_R[(rd, ref)] = 0.10 / base
        P(f"     reaction pass over x in [0.3,30] ({rd}, ref {ref}): lambda <= {lam_R[(rd, ref)]:.4f}  (thermal 3/2 is {1.5/lam_R[(rd, ref)]:.0f}x too large)")
P(f"     energy pass: lambda <= V_mult/x_e; at x_e(A, 1e10) = {xe0:.2f}: {1/xe0:.4f}; at the smallest x_e in the scan: {min(edge_x(M,c,d,a,f) for M in Ms for c in convs for d in DTA for a in A0 for f in (0.31,0.40,0.48)):.3f}")
xe_both = 2 / 3
xe_cross = cross["P"]
P(f"     what edge would pass both lines at lambda=3/2: energy needs x_e <= {xe_both:.3f}; reaction (P) needs x_e <= {xe_cross:.3f}; (sigma) {cross['S']:.3f}")
xe_A_1e10 = edge_x(1e10, "A", "own", "canonical", 0.40)
Mreq = 1e10 * (xe_A_1e10 / xe_cross) ** 6
P(f"     x_e scales as M^(-1/6): from x_e = {xe_A_1e10:.1f} at 1e10, x_e = {xe_cross:.3f} needs M ~ {Mreq:.1e} Msun (CFG48 r_ta convention)")
check("SW no combination passes both (result, not a control)", npass == 0, f"npass = {npass}")

# ---------------------------------------------------------------------------------------------- summary
P("\n== SUMMARY ==")
failed_gates = [n for n, ok in GATES if not ok]
P(f"controls failed: {FAILS if FAILS else 'none'}")
P(f"reproduction gates: {len(GATES) - len(failed_gates)}/{len(GATES)} match; non-matching: {failed_gates if failed_gates else 'none'}")
rc = 0 if (not FAILS and not failed_gates) else 1
P(f"exit code {rc}")
sys.exit(rc)
