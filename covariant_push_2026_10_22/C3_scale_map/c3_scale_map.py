#!/usr/bin/env python3
"""C3_scale_map -- AeST's own scales vs the screened theory's stiffness length L*.

Criteria: FROZEN_CRITERIA.md (committed alone first).  Run:
    OMP_NUM_THREADS=1 nice -n 10 python3 c3_scale_map.py [--mutate]
Deterministic, no network, single thread.  kappa = 1/2 is FITTED.  Not theory closed.

External inputs (record transcriptions of arXiv LaTeX sources; NO copy is on disk -> "not verified on disk"):
  SZ21 = Skordis & Zlosnik, PRL 127, 161302 (2021), arXiv:2007.00082:
    Eq. (5) action; Eq. (6) quasi-static action S = -int{ A[|grad Phi|^2 - 2 grad Phi.grad phi + |grad phi|^2
    - mu^2 Phi^2 + J(Y)] + Phi rho },  A = (2-K_B)/(16 pi Gt);  mu^2 = 2 K_2 Q_0^2/(2-K_B);  mu^-1 >~ 1 Mpc;
    r_C ~ (r_M mu^-2)^(1/3)  [real_research/bridge1_aest_equations.md; real_research/reviews/typeII_known_limits_2026.py F7;
    real_research/reviews/ppn_verify_transcription_2026.py].
  arXiv:2109.13287 Eq. (30): c_s^2 = (2-K_B)(1 + K_B lambda_s/2)/(K_2 K_B)  [ppn_verify_transcription_2026.py:349].
  AeST's Einstein-aether map c1 = K_B, c2 = 0, c3 = -K_B, c4 = 0  [ppn_verify_transcription_2026.py:67].
Local inputs: exactly D7d's (a0 footings, GM_sun, E0-E3 from D7b json, Hees/Park bands, planet bounds) and E4's
globular estimator (copied verbatim, nu_L, no EFE recipe).
"""
import json, math, os, sys, time, resource
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
def rel(*p): return os.path.join(ROOT, *p)
sys.path.insert(0, rel("doors_push_2026_10_22", "D7d_screened_q2"))
import d7d_solver as D7D                     # read-only import (functions only)

MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
RES = {"lane": "C3_scale_map", "mutate": MUT, "checks": {}}
CHK = []
def check(name, ok, value, thr, label):
    CHK.append(bool(ok)); RES["checks"][name] = dict(ok=bool(ok), value=str(value), threshold=str(thr), label=label)
    P(f"{name} {'PASS' if ok else 'FAIL'} {value} {thr}  -- {label}")
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
t0 = time.time()

# ------------------------------------------------------------------ inputs (labelled; D7d's)
GM = 1.32712440018e20; AU = 1.495978707e11; PC = 3.0857e16; MPC = 1e6 * PC
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
BAND_H = (-3.0e-27, 9.0e-27); BAND_P = (-2.0e-27, 5.2e-27)
LSTARS = [24.0, 50.0, 90.0]
PLANETS = {"Earth": (1.0 * AU, 8.7e-15), "Mars": (1.524 * AU, 1.4e-15), "Saturn": (9.58 * AU, 7.0e-15)}
MU_INV = 1.0 * MPC                            # SZ21 requirement mu^-1 >~ 1 Mpc, taken AT the boundary (most favourable)
MU = 1.0 / MU_INV
d7b = json.load(open(rel("doors_push_2026_10_22", "D7b_cassini_Q2", "d7b_cassini_q2_results.json")))
EV = {f: {E: v["ge_total"] for E, v in d7b["grid"][f]["none"].items()} for f in A0}
d7d = json.load(open(rel("doors_push_2026_10_22", "D7d_screened_q2", "d7d_screened_q2_results.json")))
e4 = json.load(open(rel("doors_push_2026_10_22", "E4_fitted_three", "e4_fitted_three_results.json")))
RES["inputs"] = dict(GM=GM, a0=A0, mu_inv_Mpc=1.0, Hees_2sigma=BAND_H, Park_2sigma=BAND_P, Lstar_pc=LSTARS,
                     E_ge_total=EV, planet_bounds=PLANETS,
                     sources_status="SZ21 / arXiv:2109.13287 equations: record transcriptions, not verified on disk")

# =================================================================== Q1: AeST's mass term on a point mass
P("=== Q1  AeST's mass term (SZ21 Eq. 6: lap Psi + mu^2 Psi = 4 pi Ghat rho + lap varphi) on a point mass")
r, m, G_M, a0s, r0, x = sp.symbols("r mu GM a_0 r_0 x", positive=True)
SGN = -1 if MUT else +1                       # mutate: Yukawa sign (lap - mu^2)
Phi = -G_M * sp.cos(m * r) / r
lap = lambda f: sp.diff(r ** 2 * sp.diff(f, r), r) / r ** 2
res_eq = sp.simplify(lap(Phi) + SGN * m ** 2 * Phi)
lim0 = sp.limit(Phi * r / (-G_M), r, 0)
g_pull = sp.simplify(sp.diff(Phi, r))         # inward pull magnitude (dPhi/dr > 0 means attraction)
g_form = sp.simplify(g_pull - G_M * (sp.cos(m * r) + m * r * sp.sin(m * r)) / r ** 2)
ser = sp.series(g_pull, r, 0, 2).removeO()
ser_ok = sp.simplify(ser - (G_M / r ** 2 + G_M * m ** 2 / 2)) == 0
k1 = (res_eq == 0) and lim0 == 1 and g_form == 0 and ser_ok
check("K1", k1, f"residual={res_eq}; r->0 norm={lim0}; series={sp.simplify(ser)}", "all exact",
      "Newtonian regime: Phi = -GM cos(mu r)/r; pull = GM/r^2 + GM mu^2/2 + O(mu^4 r^2) -> constant hedgehog, L_eq = sqrt(2)/mu")
L_eq = math.sqrt(2) / MU
RES["Q1"] = dict(newtonian_pull="GM(cos mu r + mu r sin mu r)/r^2", hedgehog="GM mu^2/2 (sunward, ADDED to MOND, does not replace it)",
                 L_eq_pc=L_eq / PC, sun_hedgehog_m_s2=GM * MU ** 2 / 2)
P(f"  hedgehog GM mu^2/2 at mu^-1 = 1 Mpc: Sun {GM * MU ** 2 / 2:.3e} m/s^2; L_eq = sqrt(2)/mu = {L_eq / PC / 1e6:.3f} Mpc "
  f"(= {L_eq / (90 * PC):.3e} x the window top 90 pc)")
# deep-MOND regime: extra enclosed source -mu^2 int Phi r^2 dr with Phi = sqrt(GM a0) ln(r/r0)
PhiM = sp.sqrt(G_M * a0s) * sp.log(r / r0)
rr = sp.symbols("rr", positive=True)
extra = -m ** 2 * sp.integrate((PhiM * r ** 2).subs(r, rr), (rr, 0, r))
frac = sp.simplify(extra / G_M)                # fractional change of r^2 g_E relative to GM
rM = sp.sqrt(G_M / a0s)
frac_form = sp.simplify(frac + (m ** 2 * r ** 3 / rM) * (sp.log(r / r0) / 3 - sp.Rational(1, 9)))
rC = sp.solve(sp.Eq(m ** 2 * r ** 3 / rM, 1), r)[0]
k2 = frac_form == 0 and sp.simplify(rC - (rM / m ** 2) ** sp.Rational(1, 3)) == 0
check("K2", k2, f"r_C = {rC}", "(r_M mu^-2)^(1/3) exact",
      "deep-MOND: fractional term -(mu^2 r^3/r_M)(ln(r/r0)/3 - 1/9): grows OUTWARD; depends on Phi's zero point r0 (cosmological gauge)")
P("  => the mass term acts at LARGE r (r >~ r_C, mu^-1) and is oscillatory (Helmholtz sign), not a Newtonian switch-off;")
P("     the task's premise 'Newtonian-like beyond a length' is corrected by the record's SZ21 transcription (typeII F7).")

# =================================================================== Q2: can AeST's class stiffen the longitudinal mode?
P("")
P("=== Q2  Static AeST-class action, Fourier space (k along z): fields Phi, phi, alpha (A_L = grad alpha), a_T (transverse A)")
k, Q0, lam, c1, c123, mu2, rho, bL = sp.symbols("k Q_0 lambda_s c_1 c_123 mu2 rho beta_L", positive=True)
Ph, ph, al, aT = sp.symbols("Phi phi alpha a_T")
chi_ = ph + Q0 * al                            # V_L = k chi ; V_T = Q0 a_T
def Lag(extra_terms):
    return ((k * Ph - k * chi_) ** 2 + (Q0 * aT) ** 2 + lam * (k ** 2 * chi_ ** 2 + Q0 ** 2 * aT ** 2) - mu2 * Ph ** 2
            + c1 * k ** 2 * aT ** 2 + c123 * k ** 4 * al ** 2 + extra_terms - 2 * rho * Ph)
sol = sp.solve([sp.diff(Lag(0), v) for v in (Ph, ph, al, aT)], [Ph, ph, al, aT], dict=True)[0]
Phi_sol = sp.simplify(sol[Ph])
indep = all(sp.simplify(sp.diff(Phi_sol, c)) == 0 for c in (c123, c1))
k3 = indep and sp.simplify(sol[al]) == 0 and sp.simplify(sol[aT]) == 0
check("K3", k3, f"Phi = {Phi_sol}; alpha = {sp.simplify(sol[al])}; a_T = {sp.simplify(sol[aT])}",
      "dPhi/dc123 = dPhi/dc1 = 0, alpha = 0",
      "DECOUPLING: the aether's longitudinal stiffness c123 = c1+c2+c3 (0 in AeST) and its curl stiffness c1 = K_B never reach Phi "
      "for a longitudinal source; phi's shift symmetry absorbs grad alpha")
# the named term: beta (div V)^2 = beta k^4 chi^2  (in Eq.-6 units beta = beta_L/(2-K_B))
sol_b = sp.solve([sp.diff(Lag(bL * k ** 4 * chi_ ** 2), v) for v in (Ph, ph, al, aT)], [Ph, ph, al, aT], dict=True)[0]
Phi_b = sp.simplify(sol_b[Ph])
P(f"  with the named term beta k^4 chi^2: Phi = {Phi_b}   (depends on beta: {sp.simplify(sp.diff(Phi_b, bL)) != 0})")
RES["Q2"] = dict(decoupling=bool(k3), Phi_AeST=str(Phi_sol), Phi_named=str(Phi_b),
                 nonlinear_argument="phi enters only via V = grad phi + Q0 A; delta phi gives div(dL/dV) = 0, delta alpha then gives "
                                    "c123 lap^2 alpha = 0 -> alpha = 0 (decaying BCs), for ANY F(Y,Q); exact, not linearised")
# K4: radial field, (div V)^2 operator == radial vector Laplacian (D7d's (P)); coefficient map
v = sp.Function("v")(r); bet = sp.symbols("beta", positive=True)
divV = sp.diff(r ** 2 * v, r) / r ** 2
dens_named = 0 if MUT else bet / 2 * divV ** 2          # mutate: curl-only stiffness (radial field has no curl)
dens_full = bet / 2 * (sp.diff(v, r) ** 2 + 2 * v ** 2 / r ** 2)   # (beta/2)|grad V|^2 for V = v(r) rhat
def EL(dens):
    Lr = r ** 2 * dens
    return sp.simplify((sp.diff(Lr, v) - sp.diff(sp.diff(Lr, sp.diff(v, r)), r)) / r ** 2)
lapvec_r = sp.diff(v, r, 2) + 2 * sp.diff(v, r) / r - 2 * v / r ** 2
k4a = sp.simplify(EL(dens_named) + bet * lapvec_r) == 0
k4b = sp.simplify(EL(dens_full) + bet * lapvec_r) == 0
KB, Ls = sp.symbols("K_B L_star", positive=True)
# Eq.(6) units: S = -int A[|grad Phi - V|^2 + J + (beta_L/(2-K_B)) (div V)^2]; screened (x2): |grad Phi - p|^2 + ... + (L*^2/2)|grad p|^2
beta_L = sp.solve(sp.Eq(sp.Symbol("bL") / (2 - KB), Ls ** 2 / 2), sp.Symbol("bL"))[0]
check("K4", k4a and k4b, f"named-term EL = -beta*lap_vec_r: {k4a}; full gradient EL same: {k4b}; beta_L = {beta_L}",
      "exact", "the named term reproduces D7d's radial (P) operator, hence CFG691's ODE with l = L*^2/(2 r_M)")
RES["Q2"]["named_term"] = dict(action_term="-beta_L [nabla_mu (q^{mu nu} nabla_nu phi)]^2 in the SZ21 bracket",
                               beta_L=str(beta_L), linear_FRW="(div V)^2 -> k^4 chi^2/a^4: spatial derivatives only (no Ostrogradsky "
                               "time derivatives at linear order); full well-posedness OPEN")

# curl-stiffness length of AeST in screened-theory units
Q0s, K2s, cs, lams = sp.symbols("Q_0 K_2 c_s lambda_s", positive=True)
LF2 = 2 * KB / ((2 - KB) * Q0s ** 2)
LF2_mu = sp.simplify(LF2.subs(Q0s, sp.sqrt(m ** 2 * (2 - KB) / (2 * K2s))))
K2_of_cs = sp.solve(sp.Eq(cs ** 2, (2 - KB) * (1 + KB * lams / 2) / (K2s * KB)), K2s)[0]
LF2_cs = sp.simplify(LF2_mu.subs(K2s, K2_of_cs))
LF2_min = sp.simplify(LF2_cs - 2 / (cs ** 2 * m ** 2))
P(f"  AeST curl-stiffness length (screened units): L*_F^2 = {LF2} = {LF2_mu} = {LF2_cs}")
P(f"  L*_F^2 - 2/(c_s^2 mu^2) = {sp.factor(LF2_min)}  (> 0 for 0 < K_B < 2, lambda_s >= 0)  => L*_F >= sqrt(2)/(c_s mu)")
RES["Q2"]["curl_length"] = dict(LF2=str(LF2_cs), bound="L*_F >= sqrt(2)/(c_s mu) >= sqrt(2) mu^-1 if c_s <= c",
                                cs_needed_for_LF_90pc=math.sqrt(2) * MU_INV / (90 * PC),
                                cs_needed_for_LF_24pc=math.sqrt(2) * MU_INV / (24 * PC))
P(f"  for L*_F to sit in the window, c_s >= {math.sqrt(2) * MU_INV / (90 * PC):.3e} c (90 pc) / {math.sqrt(2) * MU_INV / (24 * PC):.3e} c (24 pc)")

# =================================================================== Q3: local predictions
P("")
P("=== Q3  local predictions.  V1 = AeST + named term (gamma_L = L*^2/2, gamma_F = L*_F^2/2 >= 1 Mpc^2 -> g = gamma_F/gamma_L -> inf)")
def chi_g(kap, c, xe, g):
    jp = 1 + xe; jl = (1 + xe) ** 2; b = jl - jp; s2 = 1 - c * c
    A11 = kap ** 2 / 2 + jp + b * c * c - 1; A22 = g * kap ** 2 / 2 + jp + b * s2; A12 = b * c * np.sqrt(s2)
    return A22 / (A11 * A22 - A12 ** 2)
def chi_inf(kap, c, xe):
    b = (1 + xe) ** 2 - (1 + xe)
    return 1.0 / (kap ** 2 / 2 + xe + b * c * c)
def I2(chif, xe, nk=4000, nc=64, kmin=1e-4, kmax=1e4):
    cg, cw = np.polynomial.legendre.leggauss(nc); P2 = 0.5 * (3 * cg ** 2 - 1)
    lk = np.linspace(np.log(kmin), np.log(kmax), nk); kk = np.exp(lk)
    c2 = 2.5 * (chif(kk[:, None], cg[None, :], xe) * P2 * cw).sum(1)
    b = (1 + xe) ** 2 - (1 + xe)
    return np.trapz(kk ** 3 * c2, lk) - (8.0 / 3.0) * b / kmax
def Q2_hees(chif, L, xe): return -2 * GM / (5 * np.pi * L ** 3) * I2(chif, xe)      # BN11/Hees convention (D7d's QF)
# K5
kk = np.geomspace(1e-3, 1e3, 301)[:, None]; cc = np.linspace(-0.999, 0.999, 41)[None, :]
worst = 0.0
for xe in (0.5, 1.3, 1.9, 2.5):
    worst = max(worst, float(np.max(np.abs(chi_g(kk, cc, xe, 1.0) / D7D.chi(kk, cc, xe) - 1))))
worst_inf = max(float(np.max(np.abs(chi_g(kk, cc, xe, 1e8) / chi_inf(kk, cc, xe) - 1))) for xe in (0.5, 1.3, 1.9, 2.5))
check("K5", worst < 1e-12 and worst_inf < 1e-6, f"g=1 vs D7d: {worst:.1e}; g=1e8 vs closed form: {worst_inf:.1e}", "<1e-12; <1e-6",
      "generalised Route F operator (kap^2/2)[khat khat + g(1 - khat khat)] + J - khat khat")
# K5b (AMENDMENT A1, post-result): the physical finite curl stiffness g_phys = (L*_F,min/L*)^2 = 2 mu^-2/L*^2
def g_phys(L): return 2.0 * MU_INV ** 2 / L ** 2
def chi_phys(L): return (lambda a, c_, xe: chi_g(a, c_, xe, g_phys(L)))
w5b = 0.0
for f, a0 in A0.items():
    for Lpc in LSTARS:
        for E, ge in EV[f].items():
            qa = Q2_hees(chi_phys(Lpc * PC), Lpc * PC, ge / a0); qb = Q2_hees(chi_inf, Lpc * PC, ge / a0)
            w5b = max(w5b, abs(qa / qb - 1))
check("K5b", w5b < 1e-3, f"max|Q2(g_phys)/Q2(chi_inf)-1| = {w5b:.2e}", "<1e-3",
      "[A1 post-result] finite physical curl stiffness g = 2 mu^-2/L*^2 vs g -> inf")
# K6 Cassini (primary numbers at g_phys, A1)
R6 = {}; allok = True
P("  Cassini Q2 (s^-2, Hees convention) at Saturn: V1 (g = g_phys, A1) vs D7d (g=1)")
for f, a0 in A0.items():
    for Lpc in LSTARS:
        row = []
        for E, ge in EV[f].items():
            xe = ge / a0
            q1 = Q2_hees(chi_phys(Lpc * PC), Lpc * PC, xe); qinf = Q2_hees(chi_inf, Lpc * PC, xe); qd = Q2_hees(lambda a, b_, c_: D7D.chi(a, b_, c_), Lpc * PC, xe)
            ok = BAND_H[0] <= q1 <= BAND_H[1] and BAND_P[0] <= q1 <= BAND_P[1]; allok &= ok
            dref = d7d["R1_physical"][f"{f}|{Lpc:g}|{E}"]["Q2"]
            R6[f"{f}|{Lpc:g}|{E}"] = dict(Q2_V1=q1, Q2_V1_chi_inf=qinf, Q2_D7d_recomputed=qd, Q2_D7d_json=dref, ratio_V1_D7d=q1 / qd,
                                          over_Hees_upper=q1 / BAND_H[1], over_Park_upper=q1 / BAND_P[1], ok=ok)
            row.append(q1)
        P(f"   {f:9s} L*={Lpc:3.0f} pc: V1 " + " ".join(f"{q:.3e}" for q in row) +
          f" | V1/D7d " + " ".join(f"{R6[f'{f}|{Lpc:g}|{E}']['ratio_V1_D7d']:.3f}" for E in EV[f]) +
          f" | max/Hees {max(row) / BAND_H[1]:.2e}")
rec_ok = max(abs(v["Q2_D7d_recomputed"] / v["Q2_D7d_json"] - 1) for v in R6.values())
mx = max(v["Q2_V1"] for v in R6.values()); mn = min(v["Q2_V1"] for v in R6.values())
check("K6", allok and rec_ok < 1e-6, f"V1 Q2 in [{mn:.2e}, {mx:.2e}]; D7d json reproduced to {rec_ok:.1e}",
      "inside Hees [-3e-27, 9e-27] and Park [-2e-27, 5.2e-27]", "V1 passes Cassini at L* = 24/50/90 pc, all E, both footings")
RES["K6_cassini"] = R6

def radial_g(GMx, L, xe, rr_, chif, nc=48, nk=200000, chunks=8):
    """orientation-averaged anomalous radial pull at rr_ (D7d's routeF_radial with a general chi; chunked for memory)."""
    from scipy.integrate import quad
    rho_ = rr_ / L; cg, cw = np.polynomial.legendre.leggauss(nc); K = 400.0 / rho_
    lk = np.linspace(np.log(1e-6), np.log(K), nk); kk_ = np.exp(lk); c0 = np.empty(nk)
    for sl in np.array_split(np.arange(nk), chunks):
        c0[sl] = 0.5 * (chif(kk_[sl, None], cg[None, :], xe) * cw).sum(1)
    z = kk_ * rho_
    j1 = np.where(z < 1e-3, z / 3 - z ** 3 / 30, np.sin(z) / z ** 2 - np.cos(z) / z)
    head = np.trapz(kk_ * kk_ * j1 * c0, lk)
    t1 = quad(lambda zz: 1 / zz ** 3, K * rho_, np.inf, weight="sin", wvar=1.0)[0]
    t2 = quad(lambda zz: 1 / zz ** 2, K * rho_, np.inf, weight="cos", wvar=1.0)[0]
    return 2 * GMx / (np.pi * L ** 2) * (head + 2 * (t1 - t2))
# K7 wide binary
s20 = 20e3 * AU; GMb = 1.5 * GM; R7 = {}; wmax = 0.0
P("  wide binary 1.5 Msun, 20 kAU: gamma_v - 1 (V1: monopole in the Galactic field + mass-term hedgehog)")
for f, a0 in A0.items():
    for Lpc in LSTARS:
        vals = []
        for E, ge in EV[f].items():
            a_an = radial_g(GMb, Lpc * PC, ge / a0, s20, chi_phys(Lpc * PC)) + GMb * MU ** 2 / 2
            vals.append(math.sqrt(1 + a_an / (GMb / s20 ** 2)) - 1)
        iso = 0.5 * (s20 / (Lpc * PC)) ** 2; wmax = max(wmax, max(vals))
        R7[f"{f}|{Lpc:g}"] = dict(gamma_minus_1=vals, CFG740_isolated=iso, D7d=d7d["C1_wide_binary"][f"{f}|{Lpc:g}"]["gamma_minus_1"],
                                  mass_term_part=0.5 * (GMb * MU ** 2 / 2) / (GMb / s20 ** 2))
        P(f"   {f:9s} L*={Lpc:3.0f} pc: " + " ".join(f"{q:.3e}" for q in vals) + f"  (isolated {iso:.3e}; D7d " +
          " ".join(f"{q:.3e}" for q in R7[f"{f}|{Lpc:g}"]["D7d"]) + ")")
P(f"   mass-term part of gamma_v - 1 at 20 kAU: {R7['canonical|24']['mass_term_part']:.2e}")
check("K7", wmax < 1e-3, f"max gamma_v-1 = {wmax:.3e}", "<1e-3", "V1 predicts no wide-binary boost visible to DR4 (D2 sigma_sys 0.020)")
RES["K7_wide_binary"] = R7
# planets under V1 (reported)
RP = {}
for f, a0 in A0.items():
    for Lpc in LSTARS:
        for name, (rp, bnd) in PLANETS.items():
            a = max(radial_g(GM, Lpc * PC, ge / a0, rp, chi_phys(Lpc * PC)) for ge in EV[f].values()) + GM * MU ** 2 / 2
            RP[f"{f}|{Lpc:g}|{name}"] = dict(a=a, bound=bnd, ratio=a / bnd, GM_over_L2=GM / (Lpc * PC) ** 2)
P("  V1 planets (max over E): " + "; ".join(f"{kk_}: {v['ratio']:.3f} of bound" for kk_, v in RP.items() if "|24|" in kk_ and "canonical" in kk_))
RES["V1_planets"] = RP

# K8 globulars: E4's native estimator, copied verbatim (nu_L, no EFE recipe; Upsilon_V = 1.6 SURVEY-CALIBRATION)
Gc, Msun, kpc, PCm = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16
UPS_V, WID = 1.6, 0.15
A0_E4 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
GCs = [g for g in json.load(open(rel("campaign_fresh_gravity", "CFG332_globulars_three_routes", "cfg332_globulars_results.json")))["clusters"]
       if g["name"] != "Pal 3"]
ST_s = np.array([0.01, 0.1, 0.3, 1, 3, 10, 100, 1000]); ST_S = np.array([0.0050, 0.048, 0.134, 0.358, 0.663, 0.894, 0.990, 0.998999])
def Sfun(s):
    if s <= 0.01: return s / 2
    if s >= 1000: return 1 - 1 / s
    return float(np.interp(math.log(s), np.log(ST_s), ST_S))
def nu_L(y): return 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / max(y, 1e-300)))
def wolf(M, rhl): return math.sqrt(Gc * M * Msun / (6.0 * (4.0 / 3.0) * rhl * PCm)) / 1e3
def gc_pred(g, a0, L):
    M = UPS_V * g["LV"]; sN = wolf(M, g["rhl"]); B = nu_L(Gc * (M * Msun / 2) / ((4.0 / 3.0) * g["rhl"] * PCm) ** 2 / a0)
    if L is None: return sN
    rMg = math.sqrt(Gc * M * Msun / a0) / PCm; lg = L ** 2 / (2 * rMg); s = (4.0 / 3.0) * g["rhl"] / lg
    return sN * math.sqrt(1 + Sfun(s) * (B - 1))
vU = (math.log(10) * WID / 2) ** 2
def chi2(a0, L): return sum((math.log(g["so"]) - math.log(gc_pred(g, a0, L))) ** 2 / ((g["eso"] / g["so"]) ** 2 + vU) for g in GCs)
GRID = np.geomspace(5.75, 3000, 6000); R8 = {}; k8 = True
for f, a0 in A0_E4.items():
    c = np.array([chi2(a0, L) for L in GRID]); cmin = min(c.min(), chi2(a0, None))
    i = np.where(c - cmin <= 3.84)[0][0]
    L95 = brentq(lambda L: chi2(a0, L) - cmin - 3.84, GRID[i - 1], GRID[i], xtol=1e-6)
    ref = e4["Lstar"]["CFG820"][f]["N1_native"]; k8 &= abs(L95 - ref) < 0.01
    dchi_V0 = chi2(a0, 1e-6) - cmin                                     # V0: unscreened (L* -> 0), isolated
    rh = max(g["rhl"] for g in GCs)
    R8[f] = dict(L95_V1=L95, E4_N1=ref, dchi2_V0_unscreened=dchi_V0, mass_term_frac_at_rh=(MU * (4 / 3) * rh * PCm) ** 2 / 2)
    P(f"  globulars [{f}]: V1 isolated floor L*_95 = {L95:.3f} pc (E4 N1 {ref:.3f}); V0 (L*->0) Delta chi2 = {dchi_V0:.2f}; "
      f"mass-term fraction at r_h {R8[f]['mass_term_frac_at_rh']:.1e}")
check("K8", k8, f"{R8['canonical']['L95_V1']:.3f}/{R8['alt']['L95_V1']:.3f}", "E4 N1 28.853/29.123 +-0.01",
      "V1's isolated spherical sector = the screened theory's (K3+K4); EFE floor OPEN for both")
RES["K8_globulars"] = R8

# K9 V0 planets: spherical first integral u f(u) = g_N, f(u) = u/(a0-u) -> u = (sqrt(gN^2 + 4 a0 gN) - gN)/2 -> a0
R9 = {}; worst9 = 0.0; mars_fail = True
for f, a0 in A0.items():
    for name, (rp, bnd) in PLANETS.items():
        gN = GM / rp ** 2; u = (math.sqrt(gN ** 2 + 4 * a0 * gN) - gN) / 2 + GM * MU ** 2 / 2
        ref = d7d["C2_planets"][f"{f}|unscreened|{name}"]["no_turnoff"]
        worst9 = max(worst9, abs(u / ref - 1)); R9[f"{f}|{name}"] = dict(u=u, bound=bnd, ratio=u / bnd, D7d=ref)
    mars_fail &= R9[f"{f}|Mars"]["ratio"] > 1
check("K9", worst9 < 1e-6 and mars_fail, f"D7d match {worst9:.1e}; Mars ratio {R9['canonical|Mars']['ratio']:.2e}/{R9['alt|Mars']['ratio']:.2e}",
      "<1e-6; >1", "V0 (pure AeST with the screened law) FAILS the planetary monopole: u -> a0 near the Sun")
P("  V0 planets: " + "; ".join(f"{kk_} {v['ratio']:.2e}x bound" for kk_, v in R9.items()))
RES["K9_V0_planets"] = R9

# K10 scale map
def rM_of(Mkg_GM, a0): return math.sqrt(Mkg_GM / a0)
lens = {"mu^-1": MU_INV, "L_eq = sqrt2/mu": L_eq, "L*_F floor sqrt2/mu (c_s<=c)": math.sqrt(2) * MU_INV}
for f, a0 in A0.items():
    lens[f"r_C Sun ({f})"] = (rM_of(GM, a0) * MU_INV ** 2) ** (1 / 3)
    Mg = min(UPS_V * g["LV"] for g in GCs) * GM
    lens[f"r_C smallest globular ({f})"] = (rM_of(Mg, a0) * MU_INV ** 2) ** (1 / 3)
    lens[f"r_C 1e11 Msun galaxy ({f})"] = (rM_of(1e11 * GM, a0) * MU_INV ** 2) ** (1 / 3)
ratios = {kk_: vv / (90 * PC) for kk_, vv in lens.items()}
for kk_, vv in lens.items(): P(f"  {kk_:34s} {vv / PC:.4e} pc  = {ratios[kk_]:.3e} x 90 pc")
check("K10", min(ratios.values()) > 1e3, f"min ratio {min(ratios.values()):.3e} ({min(ratios, key=ratios.get)})", ">1e3",
      "no AeST length reaches the L* window")
RES["K10_scales"] = dict(lengths_pc={kk_: vv / PC for kk_, vv in lens.items()}, ratio_to_90pc=ratios)

# =================================================================== outcome
n = len(CHK); npass = sum(CHK)
RES["lines"] = dict(
    Q1="AeST's mass term is a LARGE-scale term (r >~ r_C, mu^-1), oscillatory, opposite in direction to L*'s small-scale screening"
    if (CHK[0] and CHK[1]) else "UNDECIDED",
    Q2="L* is OUTSIDE AeST's class; the covariant screened theory is AeST + one named term (beta_L)" if CHK[2] else "L* INSIDE AeST",
    Q4="L* = new constant of the covariant theory (beta_L = (2-K_B) L*^2/2), value FITTED (globular floor, calibration-dominated)")
RES["verdict"] = "SCOPED NO-GO" if CHK[2] else "CRISP FINDING"
RES["n_checks"], RES["n_pass"] = n, npass
RES["runtime_s"], RES["peak_rss_GB"] = time.time() - t0, rss()
P("")
for kk_, vv in RES["lines"].items(): P(f"{kk_}: {vv}")
P(f"verdict: {RES['verdict']}   (kappa = 1/2 FITTED; not theory closed)")
P(f"runtime {RES['runtime_s']:.1f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")
P(f"C3_SCALE_MAP COMPLETE: {npass}/{n} checks PASS.")
json.dump(RES, open(os.path.join(HERE, f"c3_scale_map_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"c3_scale_map{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == n else 1)
