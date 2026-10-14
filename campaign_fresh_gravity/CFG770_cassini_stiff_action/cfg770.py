"""CFG770 -- Cassini Q2 for the framework's one-field action with stiffness and NO basin rule.

Criteria: FROZEN_CRITERIA.md (committed alone first, 4d35ef158).
Action: L = -|grad Phi - K P|^2/(2K) - rho Phi - W_rem(u) - (gamma/2)|grad P|^2, K = 4 pi G, u = K|P|,
        K dW_rem/du = R(u) = u^2/(a0 - u);  Lambda^2 = gamma/K;  CFG691's L*^2 = 2 Lambda^2 (checked, K1).
Linear response of p = P - P_e about the Galaxy's uniform background P_e:
        m_i(k) = (A_i + L^2 k^2)/(A_i + 1 + L^2 k^2),  dPhi(k) = -4 pi G M/(k^2 sum_i khat_i^2 m_i),
        Q2 = (G M/pi) int k^2 dk int dc P2(c)/(m_perp + c^2 (m_par - m_perp))   [Park/Hees convention].
Run: python3 cfg770.py   (CFG770_MUTATE=1 for the teeth; separate outputs).  One process, seconds, < 100 MB.
"""
import json
import math
import os
import sys

import numpy as np
import sympy as sp
from scipy import integrate

MODE = os.environ.get("CFG770_MUTATE", "")            # "", "M1" (stiffness off) or "M2" (KP term dropped)
assert MODE in ("", "M1", "M2")
MUT = MODE == "M2"                                       # M2 zeroes the KP-term response
HERE = os.path.dirname(os.path.abspath(__file__))
SUF = f"_MUTATE_{MODE}" if MODE else ""
OUTF = open(os.path.join(HERE, f"cfg770{SUF}.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUTF.write(s + "\n")


G = 6.67430e-11
MSUN = 1.98847e30
GM = 1.32712440018e20
AU = 1.495978707e11
PC = 3.0856775814913673e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
GE = [2.00e-10, 2.32e-10, 2.64e-10]
Q2_CEIL, A_SUNWARD, M_SAT_BOUND, R_SAT = 5.2e-27, 3.66e-14, 6.7e-11, 9.54 * AU
LSTAR_MIN = 5.75 * PC
LSTAR_M1 = 1e-4 * PC
RES = {"lane": "CFG770", "mutate": MODE, "checks": {}, "numbers": {}}
FAILS = []


def check(name, ok, detail):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail)
    if not ok:
        FAILS.append(name)


R = lambda u, a0: u * u / (a0 - u)
dR = lambda u, a0: (2 * u * a0 - u * u) / (a0 - u) ** 2


def background(ge, a0):
    ue = a0 * ge / (a0 + ge)
    gNe = ge - ue
    return dict(ue=ue, gNe=gNe, Apar=dR(ue, a0), Aperp=R(ue, a0) / ue, R_ok=abs(R(ue, a0) / gNe - 1))


XC, WC = np.polynomial.legendre.leggauss(96)
P2C = 0.5 * (3 * XC ** 2 - 1)


def mfun(A, kap):
    if MUT:  # M2: drop the KP term -> m = 1
        return np.ones_like(np.asarray(kap, float) * 1.0)
    return (A + kap ** 2) / (A + 1 + kap ** 2)


def defic(kap, Apar, Aperp):
    """1 - S(c) computed without cancellation: 1 - m_i = 1/(A_i + 1 + kap^2).  (First run subtracted numerically: K2 roundoff.)"""
    if MUT:
        return np.zeros_like(XC)
    return XC ** 2 / (Apar + 1 + kap ** 2) + (1 - XC ** 2) / (Aperp + 1 + kap ** 2)


def J(kap, Apar, Aperp):
    d = defic(kap, Apar, Aperp)
    if MUT:
        return 0.0
    d0 = 1.0 / (Aperp + 1 + kap ** 2)                       # c = 0 value; int P2 dc = 0 so subtracting it is exact
    # (second run: without this subtraction K2 failed at 1e-9 from quadrature roundoff on the constant)
    return float(np.sum(WC * P2C * (d / (1 - d) - d0 / (1 - d0))))


def Fiso(kap, Apar, Aperp):
    """<1/S>_c - 1 (isotropic part of the anomaly)."""
    d = defic(kap, Apar, Aperp)
    return float(0.5 * np.sum(WC * d / (1 - d)))


def Q2(Lam, Apar, Aperp):
    f = lambda t: (math.exp(t) ** 3) * J(math.exp(t), Apar, Aperp)  # kap^2 dkap = kap^3 dt
    val = 0.0
    for lo, hi in [(-12, -4), (-4, 0), (0, 4), (4, 12)]:
        val += integrate.quad(f, lo, hi, limit=400, epsabs=0, epsrel=1e-11)[0]
    return GM / (math.pi * Lam ** 3) * val


def a_anom(r, Lam, Apar, Aperp):
    """anomalous radial acceleration (negative = sunward): -(2GM/pi) int dk k j1(kr) F(k).
    Split F = 1/(L k)^2 + rem: the first term gives exactly -GM/(2 L^2)."""
    if MUT:
        return 0.0
    lead = -GM / (2 * Lam ** 2)
    x0 = r / Lam

    def j1(x):
        return (math.sin(x) / x - math.cos(x)) / x if x > 1e-4 else x / 3 - x ** 3 / 30

    def g(t):
        kap = math.exp(t)
        d = defic(kap, Apar, Aperp)
        # F - 1/kap^2 with the leading term removed analytically: d/(1-d) - 1/kap^2
        rem = float(0.5 * np.sum(WC * (d / (1 - d) - 1 / kap ** 2)))
        return kap * kap * j1(kap * x0) * rem  # k dk = kap^2 dt / L^2 (L^2 restored below)

    val = 0.0
    for lo, hi in [(-14, -6), (-6, -2), (-2, 2), (2, 6), (6, 9)]:
        val += integrate.quad(g, lo, hi, limit=600, epsabs=1e-30, epsrel=1e-10)[0]
    return lead - (2 * GM / math.pi) * val / Lam ** 2


# ============================================================ K3 sympy linearization
P("CFG770  Cassini Q2 for the one-field stiffened action, no basin rule" + (f"  [MUTATE {MODE}]" if MODE else ""))
P("\nK3  sympy: Jacobian of F(P) = R(K|P|) P/|P| at P = (0,0,P0)")
px, py, pz, P0, Ks, a0s = sp.symbols("p_x p_y p_z P0 K a0", positive=True)
uu = Ks * sp.sqrt(px ** 2 + py ** 2 + pz ** 2)
Rs = uu ** 2 / (a0s - uu)
Fv = [Rs * c / sp.sqrt(px ** 2 + py ** 2 + pz ** 2) for c in (px, py, pz)]
Jm = sp.Matrix([[sp.diff(Fv[i], v) for v in (px, py, pz)] for i in range(3)]).subs({px: 0, py: 0, pz: P0})
u0 = Ks * P0
R0 = u0 ** 2 / (a0s - u0)
dR0 = sp.diff(sp.Symbol("w") ** 2 / (a0s - sp.Symbol("w")), sp.Symbol("w")).subs(sp.Symbol("w"), u0)
k3 = all(sp.simplify(Jm[i, j] - (Ks * (R0 / u0 if i < 2 else dR0) if i == j else 0)) == 0 for i in range(3) for j in range(3))
check("K3 linearization", k3, "dF/dP = K diag(R/u, R/u, R'(u)) exactly")

# ============================================================ K1 background-free limit
P("\nK1  no background (A -> 1e-9): anomalous pull at r << Lambda vs CFG691's GM/L*^2")
Lam_t = LSTAR_MIN / math.sqrt(2)
a_k1 = a_anom(1e-3 * Lam_t, Lam_t, 1e-9, 1e-9)
k1 = abs(abs(a_k1) / (GM / LSTAR_MIN ** 2) - 1) if not MUT else float("nan")
check("K1 L*^2 = 2 Lambda^2", (k1 <= 1e-3) if not MUT else True,
      f"|a| = {abs(a_k1):.4e} vs GM/L*^2 = {GM / LSTAR_MIN ** 2:.4e}, rel {k1:.1e}")

# ============================================================ backgrounds
P("\nBackgrounds (action's own static solution: g_e = g_Ne + u_e, R(u_e) = g_Ne)")
BG = {}
for f, a0 in A0.items():
    for ge in GE:
        b = background(ge, a0)
        BG[(f, ge)] = b
        P(f"  {f:9s} g_e {ge:.2e}: u_e/a0 {b['ue'] / a0:.4f}, A_par {b['Apar']:.4f}, A_perp {b['Aperp']:.4f}, "
          f"boost g_e/g_Ne {ge / b['gNe']:.4f}, lambda_e(L*min) {LSTAR_MIN / math.sqrt(2) / math.sqrt(min(b['Apar'], b['Aperp']) + 1) / PC:.3f} pc")
RES["numbers"]["backgrounds"] = {f"{f}_{ge:.2e}": b for (f, ge), b in BG.items()}

# ============================================================ K2 isotropic background
b0 = BG[("canonical", 2.32e-10)]
q_aniso = Q2(Lam_t, b0["Apar"], b0["Aperp"])
q_iso = Q2(Lam_t, b0["Aperp"], b0["Aperp"])
k2 = abs(q_iso) <= 1e-10 * abs(q_aniso) if not MUT else abs(q_iso) < 1e-40
check("K2 isotropic -> Q2 = 0", k2, f"Q2_iso {q_iso:.3e} vs Q2_aniso {q_aniso:.3e}")

# ============================================================ T1 / T2 / T3 / K4
LS = LSTAR_M1 if MODE == "M1" else LSTAR_MIN
Lam = LS / math.sqrt(2)
P(f"\nT1  Q2/ceiling at L* = {LS / PC:g} pc (ceiling {Q2_CEIL:.1e} s^-2, Park+2026 2 sigma)")
t1 = {}
for (f, ge), b in BG.items():
    q = Q2(Lam, b["Apar"], b["Aperp"])
    t1[f"{f}_{ge:.2e}"] = q
    P(f"  {f:9s} g_e {ge:.2e}: Q2 = {q:+.3e} s^-2 -> |Q2|/ceiling = {abs(q) / Q2_CEIL:.3e}")
worst1 = max(abs(v) for v in t1.values()) / Q2_CEIL
check("T1 Cassini Q2 (headline)", worst1 < 1, f"worst |Q2|/ceiling {worst1:.3e} over 3 g_e x 2 footings")
RES["numbers"]["T1_Q2"] = t1

P("\nT2  Q2 across the stiffness window (canonical, g_e 2.32e-10), reported")
t2 = {}
for Lpc in [5.75, 10, 30, 100, 300, 1000]:
    q = Q2(Lpc * PC / math.sqrt(2), b0["Apar"], b0["Aperp"])
    t2[Lpc] = q
    P(f"  L* {Lpc:7.2f} pc: |Q2|/ceiling {abs(q) / Q2_CEIL:.3e}")
RES["numbers"]["T2"] = t2

P(f"\nT3  planetary gates in the background at L* = {LS / PC:g} pc")
t3 = {}
for (f, ge), b in BG.items():
    a1 = a_anom(AU, Lam, b["Apar"], b["Aperp"])
    aS = a_anom(R_SAT, Lam, b["Apar"], b["Aperp"])
    Msat = abs(aS) * R_SAT ** 2 / G / MSUN
    t3[f"{f}_{ge:.2e}"] = dict(a1AU=a1, ratio1=abs(a1) / A_SUNWARD, Msat=Msat, ratioM=Msat / M_SAT_BOUND)
    P(f"  {f:9s} g_e {ge:.2e}: sunward 1 AU {a1:+.4e} (ratio {abs(a1) / A_SUNWARD:.4f}); "
      f"Saturn monopole {Msat:.4e} Msun (ratio {Msat / M_SAT_BOUND:.4f})")
w3 = max(max(v["ratio1"], v["ratioM"]) for v in t3.values())
check("T3 planetary gates", w3 < 1, f"worst ratio {w3:.4f}")
RES["numbers"]["T3"] = t3

P("\nK4  linear validity: max K|p| / u_e (isotropic Yukawa bound with A_min, r -> 0 is the maximum: GM/(2 Lambda^2))")
k4 = max(GM / (2 * Lam ** 2) / b["ue"] for b in BG.values())
check("K4 linear validity", (k4 <= 1e-3) if not MODE else True, f"max K|p|/u_e = {k4:.3e}" + (" (MUTATE: not required)" if MODE else ""))

# ============================================================ T4 / C0 reported
P("\nT4  Galactic boost at the Sun in this action (reported, no verdict)")
for (f, ge), b in BG.items():
    P(f"  {f:9s} g_e {ge:.2e}: g_e/g_Ne = {ge / b['gNe']:.4f}")
P("\nC0  no stiffness (gamma = 0): sunward tail at 1 AU = u(g) = a0 g/(a0+g), g from g_N = GM/AU^2")
c0 = {}
for f, a0 in A0.items():
    gN = GM / AU ** 2
    g = 0.5 * (gN + math.sqrt(gN ** 2 + 4 * gN * a0))
    u = g - gN
    c0[f] = u / A_SUNWARD
    P(f"  {f:9s}: tail {u:.4e} m/s^2 = {u / A_SUNWARD:.0f}x the bound  (FAIL as expected)")
RES["numbers"]["C0"] = c0

if MODE == "M1":
    P("\nM1 tooth: with the stiffness effectively off (L* = 1e-4 pc) T1 or T3 must FAIL")
    if not any(n.startswith(("T1", "T3")) for n in FAILS):
        P("  M1 tooth DID NOT BITE")
    else:
        P("  M1 tooth bites")
if MODE == "M2":
    P("\nM2 tooth: with the KP term dropped Q2 must vanish identically")
    bite = max(abs(v) for v in t1.values()) == 0.0
    P(f"  M2 tooth {'bites' if bite else 'DID NOT BITE'} (max |Q2| = {max(abs(v) for v in t1.values()):.1e})")
    if bite:
        FAILS.append("M2 tooth: Q2 = 0 identically (designed exit 1)")
RES["fails"] = FAILS
json.dump(RES, open(os.path.join(HERE, f"cfg770_results{SUF}.json"), "w"), indent=1, default=float)
P("\nFAILS:", FAILS if FAILS else "none")
OUTF.close()
sys.exit(1 if FAILS else 0)
