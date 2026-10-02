#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG288 STAGE B -- THE BEST HONEST ONE-FIELD CONSTRUCTIONS, SCORED AGAINST EVERY GATE.

Frozen in FROZEN_CRITERIA.md sections 3, 5, 7.4 (committed before this script; its sha256 is printed below).  In one line each:
  ROAD W (wave field)    S = int sqrt(-g)[Mbar^2 R/2 - |dPhi|^2 - m^2 |Phi|^2 - rho_Lambda] + S_m[g]; Phi complex (FL1's order parameter in
                         V0's dark slot), lambda = 0, m declared.  The vacuum value rho_Lambda is the dark energy; the oscillation is the cold
                         component: a classical field whose quanta would be light bosons of mass m.
  ROAD S (shift charge)  S = int sqrt(-g)[Mbar^2 R/2 + P(X)] + S_m[g], P = -rho_Lambda + (M^4/2)(X/X0 - 1)^2 (the record's K(Q) class),
                         plus a seeding term -J(t) phi; the dust is the conserved charge (stage A, A2).
  DERIVED                W1 NR limit -> Schrodinger-Poisson (sympy); W2 background, misalignment amplitude, averaged w (exact radiation-era
                         solution); W3 dispersion omega^2 = (hbar k^2/2m)^2 - 4 pi G rho (sympy), c_vis^2 = 0 (sympy); W4 HBG transfer;
                         W5 the 1-D stream test (exact FFT Schrodinger vs exact collisionless vs the single-valued sticky fluid); W6 merger;
                         W7 tensor equation h'' + 3H h' - h_zz/a^2 = 0 with the field present (sympy, c_T = 1), Hamiltonian positivity;
                         road S: (box phi)^2 adds no hdot^2 / h_z^2 term (sympy).
  GATES                  G-BG, G-DUST, G-ONSET, G-AMOUNT, G-STREAM, G-PK, G-MERGER, G-STAB/GW, per road, thresholds as frozen.
MODES: MUTATE=0 main; MUTATE=1 the wave field's hbar/m raised to nu = 0.02: the wave-vs-collisionless match must FAIL (rc 1).
kappa = 1/2 FITTED.  No dark-matter particle species is added: the cold component is the dark-energy field doing a second job; its quanta
would be light bosons; the cold MASS is still required.  Nothing here says the theory is closed or that the data favour the framework.
Run: python3 campaign_fresh_gravity/CFG288_one_field_dark_sector/cfg288_construction_gates.py   (MUTATE=1 for the control)
"""
import sys
sys.dont_write_bytecode = True
import os, math, json, time, hashlib
import numpy as np
import sympy as sp
from scipy.special import jv, gamma as Gam
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C

MODE = int(os.environ.get("MUTATE", "0"))
SLUG = "cfg288_construction_gates" + (f"_MUTATE{MODE}" if MODE else "")
R = C.Report(SLUG, False)
P, check, num = R.P, R.check, R.num
T0 = time.time()
P(__doc__.split("Run: python3")[0].strip())
FROZEN = os.path.join(HERE, "FROZEN_CRITERIA.md")
P(f"\n  FROZEN_CRITERIA.md sha256 {hashlib.sha256(open(FROZEN, 'rb').read()).hexdigest()}")
if MODE == 1:
    P("\n  *** MUTATE=1: nu = hbar/m = 0.02 in the stream test -- the wave-vs-collisionless match must FAIL ***")
LB0 = MODE == 0

# ================================================================================================ constants (frozen ledger)
c = 2.99792458e8; G = 6.67430e-11; hbar = 1.054571817e-34; eV = 1.602176634e-19; kB = 1.380649e-23
MPC = 3.0856775814913673e22; KPC = MPC / 1e3; AU = 1.495978707e11; MSUN = 1.98847e30
HC_EVM = hbar * c / eV
h = 0.6736; H0 = 100 * h * 1e3 / MPC
ob, oc, onu_m = 0.02237, 0.1200, 0.06 / 93.14
TCMB, NEFF = 2.7255, 3.046
rho_crit = 3 * H0 ** 2 / (8 * math.pi * G)
og = (math.pi ** 2 / 15) * (kB * TCMB) ** 4 / (hbar * c) ** 3 / c ** 2 / (rho_crit / h ** 2)
o_r = og * (1 + NEFF * 7 / 8 * (4 / 11) ** (4 / 3))
Om = (ob + oc + onu_m) / h ** 2
Orad0 = og * (1 + (NEFF - 1.0153) * 7 / 8 * (4 / 11) ** (4 / 3)) / h ** 2
OL = 1 - Om - Orad0
Oc, Or_h = oc / h ** 2, o_r / h ** 2
RATIO = Oc / OL
rhoL = OL * rho_crit
def to_eV4(rho):
    return rho * c ** 2 / eV * HC_EVM ** 3
rhoL_eV4 = to_eV4(rhoL)
MPL = math.sqrt(hbar * c / (8 * math.pi * G)) * c ** 2 / eV
H0_eV = hbar * H0 / eV
def H_si(z):
    return H0 * math.sqrt(Or_h * (1 + z) ** 4 + (ob + oc) / h ** 2 * (1 + z) ** 3 + OL)
def H_eV(z):
    return hbar * H_si(z) / eV
def rho_d(z):        # cold density (kg/m^3) at z
    return Oc * rho_crit * (1 + z) ** 3
KAPPA = 0.5
M_MIN, M_L383 = 2e-20, 2e-19
CS2_CMB, CS_FOREST, W_TOL = 1e-5, 5.0, 1e-5
NU = 0.02 if MODE == 1 else 5e-5

# z_req from the seeding run (frozen section 3 / 7.3)
SEED_JSON = os.path.join(HERE, "cfg288_seeding_camb_results.json")
if os.path.exists(SEED_JSON):
    sj = json.load(open(SEED_JSON))["numbers"]
    ZREQ = sj.get("z_req")
    SEED_TABLE = sj.get("seeding_table", [])
    P(f"\n  z_req read from cfg288_seeding_camb_results.json: {ZREQ}  (None = undefined under the frozen rule)")
else:
    ZREQ, SEED_TABLE = 1e7, []
    P("\n  cfg288_seeding_camb_results.json absent: z_req = 1e7 (frozen fallback)")
PH_JSON = os.path.join(HERE, "cfg288_seeding_posthoc_instrument_POSTHOC_results.json")
ZREQ_POSTHOC = json.load(open(PH_JSON))["numbers"].get("posthoc_zreq") if os.path.exists(PH_JSON) else "n/a"
ZREQ_MAX = 1e7       # the largest value the frozen definition can return

GATES = {"W": {}, "S": {}}
def gate(road, name, verdict, ok, detail):
    GATES[road][name] = dict(verdict=verdict, ok=bool(ok), detail=detail)
    check(f"{'ROAD W' if road == 'W' else 'ROAD S'} {name}: {verdict}", detail, ok, load_bearing=LB0)

# ================================================================================================ W1
R.banner("W1  NON-RELATIVISTIC LIMIT OF THE KLEIN-GORDON FIELD IN A WEAK STATIC POTENTIAL (sympy)")
t, x, eps = sp.symbols("t x epsilon", positive=True)
m = sp.symbols("m", positive=True)
U = sp.Function("U")(x)
psi = sp.Function("psi")(t, x)
gtt, gxx = -(1 + 2 * U), (1 - 2 * U)
sqrtg = sp.sqrt((1 + 2 * U) * (1 - 2 * U) ** 3)
Phi = sp.exp(-sp.I * m * t) * psi
box = (1 / gtt) * sp.diff(Phi, t, 2) + (1 / sqrtg) * sp.diff(sqrtg * (1 / gxx) * sp.diff(Phi, x), x)
KG = sp.expand(sp.simplify((box - m ** 2 * Phi) * sp.exp(sp.I * m * t)))
# scalings: d/dt ~ eps, d/dx ~ sqrt(eps), U ~ eps (and U' ~ eps^(3/2))
pt, ptt, px, pxx, ptx, p0 = sp.symbols("psi_T psi_TT psi_X psi_XX psi_TX psi0")
u0, u1 = sp.symbols("U0 U1")
rep = {sp.Derivative(psi, (t, 2)): eps ** 2 * ptt, sp.Derivative(psi, t, x): eps ** sp.Rational(3, 2) * ptx,
       sp.Derivative(psi, (x, 2)): eps * pxx, sp.Derivative(psi, t): eps * pt, sp.Derivative(psi, x): sp.sqrt(eps) * px}
KGs = KG.subs(rep)
KGs = KGs.subs(sp.Derivative(U, x), eps ** sp.Rational(3, 2) * u1).subs(U, eps * u0).subs(psi, p0)
ser = sp.series(KGs, eps, 0, 2).removeO()
o0 = sp.simplify(ser.coeff(eps, 0)); o1 = sp.simplify(sp.expand(ser).coeff(eps, 1))
target = 2 * m * (sp.I * pt + pxx / (2 * m) - m * u0 * p0)
okW1 = o0 == 0 and sp.simplify(o1 - target) == 0
P(f"    O(eps^0): {o0};  O(eps^1): {sp.factor(o1)}  ->  i psi_t = -psi_xx/(2m) + m U psi  (hbar = c = 1)")
check("W1 [sympy] the NR limit of the Klein-Gordon field is Schrodinger-Poisson: the O(eps) equation is 2m (i psi_t + psi_xx/2m - m U psi) = 0",
      f"O(eps^0) = {o0}; O(eps^1) matches: {okW1}", okW1, load_bearing=LB0)

# ================================================================================================ W2
R.banner("W2  BACKGROUND: the vacuum value is the dark energy; the oscillation is the cold component")
a0_can = KAPPA * c * math.sqrt(G * rhoL); a0_alt = KAPPA * c * math.sqrt(G * rho_crit)
d_can = a0_can / C.A0_SI["canonical"] - 1; d_alt = a0_alt / C.A0_SI["alt"] - 1
W_PL, SW_PL = -1.028, 0.031
P(f"    a0 = kappa c sqrt(G rho): canonical (rho_Lambda) {a0_can:.5e} vs record {C.A0_SI['canonical']:.5e} ({d_can:+.2e}); "
  f"alt (rho_crit) {a0_alt:.5e} vs record {C.A0_SI['alt']:.5e} ({d_alt:+.2e})")
P(f"    w_DE = -1 exactly (V_min constant: T_mn = -rho_Lambda g_mn); Planck 2018 + SNe + BAO constant w = {W_PL} +- {SW_PL}: |dw| = {abs(-1 - W_PL) / SW_PL:.2f} sigma")
rL_s, m2_s, ph_s = sp.symbols("rho_Lambda m2 phi", positive=True)
Vpot = rL_s + m2_s * ph_s ** 2 / 2
indepV = sp.diff(sp.diff(Vpot, ph_s), rL_s) == 0
z_on = brentq(lambda z: H_eV(z) - M_MIN, 10.0, 1e12)
frac_L_on = rhoL / (3 * H_si(z_on) ** 2 / (8 * math.pi * G))
P(f"    the field equation contains rho_Lambda only through H: dV'/d rho_Lambda = 0 ({indepV}); rho_Lambda/rho_total at onset (m = {M_MIN:.0e}, "
  f"z_on = {z_on:.3e}) = {frac_L_on:.2e} -> the dust amount and rho_Lambda are dynamically independent")
# averaged w: exact identity from the equation of motion, 2(K - V) = d(phi phidot)/dt + 3 H phi phidot, then the adiabatic cycle average
# with <phi^2> ~ a^-3: <w> = (3/2)(H/m)^2 in radiation domination (Hdot = -2H^2) and (9/8)(H/m)^2 in matter domination (Hdot = -3H^2/2)
ts_ = sp.symbols("t"); Hs_ = sp.Function("H")(ts_); fs_ = sp.Function("f")(ts_); ms_ = sp.symbols("m", positive=True)
eom_ = {sp.Derivative(fs_, (ts_, 2)): -3 * Hs_ * sp.diff(fs_, ts_) - ms_ ** 2 * fs_}
ident = sp.simplify((sp.diff(fs_ * sp.diff(fs_, ts_), ts_) + 3 * Hs_ * fs_ * sp.diff(fs_, ts_)).subs(eom_) - (sp.diff(fs_, ts_) ** 2 - ms_ ** 2 * fs_ ** 2))
Q, Hh, Hd = sp.symbols("Q H Hdot")          # Q = <phi^2>, d<phi^2>/dt = -3 H Q
avg_phiphid = -sp.Rational(3, 2) * Hh * Q                     # <phi phidot> = (1/2) d<phi^2>/dt
d_avg = -sp.Rational(3, 2) * (Hd * Q + Hh * (-3 * Hh * Q))    # d/dt <phi phidot>
twoKV = d_avg + 3 * Hh * avg_phiphid                          # 2 <K - V>
w_RD = sp.simplify((twoKV / 2).subs(Hd, -2 * Hh ** 2) / (ms_ ** 2 * Q))
w_MD = sp.simplify((twoKV / 2).subs(Hd, -sp.Rational(3, 2) * Hh ** 2) / (ms_ ** 2 * Q))
P(f"    identity 2(K - V) - [d(phi phidot)/dt + 3H phi phidot] = {ident} (on the EOM);  adiabatic average: <w>_RD = {w_RD}, <w>_MD = {w_MD}")
# numerical control (can fail): the secular part of (K - V) x^(3/2) in the exact radiation-era Bessel solution is (3/8) C_inf / x^2
Cinf_ = Gam(1.25) ** 2 * math.sqrt(2) / math.pi
xx = np.linspace(200.0, 400.0, 40001)
ph = Gam(1.25) * (xx / 2) ** (-0.25) * jv(0.25, xx); dph = -Gam(1.25) * (xx / 2) ** (-0.25) * jv(1.25, xx)
yv = 0.5 * (dph ** 2 - ph ** 2) * xx ** 1.5
basis = [np.cos(2 * xx), np.sin(2 * xx), np.cos(2 * xx) / xx, np.sin(2 * xx) / xx, np.cos(2 * xx) / xx ** 2, np.sin(2 * xx) / xx ** 2,
         np.cos(2 * xx) / xx ** 3, np.sin(2 * xx) / xx ** 3, 1 / xx ** 2, 1 / xx ** 3, 1 / xx ** 4]
coef, *_ = np.linalg.lstsq(np.array(basis).T, yv, rcond=None)
gam_fit = float(coef[8]); gam_th = 3 / 8 * Cinf_
okw = abs(gam_fit / gam_th - 1) < 0.05 and sp.simplify(ident) == 0 and w_RD == sp.Rational(3, 2) * Hh ** 2 / ms_ ** 2
P(f"    exact Bessel solution, least-squares secular coefficient of (K - V) x^1.5 on x in [200, 400]: {gam_fit:.5f} vs (3/8) C_inf = {gam_th:.5f}")
check("W2-CTRL [sympy + numerical; can fail] <w> = (3/2)(H/m)^2 in radiation domination: the EOM identity holds exactly and the exact Bessel "
      "solution's secular (K - V) coefficient equals (3/8) C_inf to 5%",
      f"identity residual {ident}; <w>_RD = {w_RD}; fitted/theory = {gam_fit / gam_th:.4f}", okw, load_bearing=LB0)
def w_at_z(mm, z):
    return 1.5 * (H_eV(z) / mm) ** 2          # the larger (radiation-era) coefficient, at either epoch
wx = dict(gamma_fit=gam_fit, gamma_theory=gam_th, w_RD=str(w_RD), w_MD=str(w_MD))
w3400, w1100 = w_at_z(M_MIN, 3400.0), w_at_z(M_MIN, 1100.0)
P(f"    |<w>| <= (3/2)(H/m)^2: z = 3400: {w3400:.2e}; z = 1100: {w1100:.2e} (m = {M_MIN:.0e} eV)")
# misalignment amplitude needed (exact radiation-era Bessel solution, constant g*: declared approximation)
Cinf = Gam(1.25) ** 2 * math.sqrt(2) / math.pi
MLIST = [("m_min (Lyman-alpha)", M_MIN), ("L383 floor", M_L383), ("q=3/4", MPL ** 0.25 * (H0_eV * math.sqrt(OL)) ** 0.75),
         ("q=2/3", MPL ** (1 / 3) * (H0_eV * math.sqrt(OL)) ** (2 / 3)), ("q=1/2", MPL ** 0.5 * (H0_eV * math.sqrt(OL)) ** 0.5),
         ("rho_Lambda^(1/4)", rhoL_eV4 ** 0.25)]
MIS = {}
for lab, mm in MLIST:
    phi_over = math.sqrt(3 * Oc * (H0_eV / mm) ** 0.5 / (Cinf * 2 ** 1.5 * Or_h ** 0.75))
    dV = 0.5 * mm ** 2 * (phi_over * MPL) ** 2
    zo = 10 ** brentq(lambda lz: H_eV(10 ** lz) - mm, 1.0, 40.0) 
    MIS[lab] = dict(m_eV=mm, phi_i_over_MPl=phi_over, phi_i_GeV=phi_over * MPL / 1e9, dV_eV4=dV, dV_over_rhoL=dV / rhoL_eV4,
                    dV_quarter_eV=dV ** 0.25, z_on=zo)
    P(f"    {lab:20s} m = {mm:.3e} eV: phi_i = {phi_over:.3e} Mbar_Pl = {phi_over * MPL / 1e9:.3e} GeV; Delta V = m^2 phi_i^2/2 = {dV / rhoL_eV4:.3e} rho_Lambda "
      f"(Delta V^(1/4) = {dV ** 0.25:.3e} eV); z_on = {zo:.3e}")
num("W2", dict(a0_canonical=a0_can, a0_alt=a0_alt, d_can=d_can, d_alt=d_alt, rhoL_frac_at_onset=frac_L_on, w_avg=wx, w3400=w3400, w1100=w1100,
               misalignment=MIS))

okBG = abs(d_can) <= 0.01 and abs(d_alt) <= 0.01 and abs(-1 - W_PL) <= 2 * SW_PL
gate("W", "G-BG", "PASS" if okBG else "FAIL", okBG,
     f"w = -1 exactly ({abs(-1 - W_PL) / SW_PL:.1f} sigma from Planck+SNe+BAO); a0 tie canonical {d_can:+.1e}, alt {d_alt:+.1e} (<= 1%). The tie is the "
     f"vacuum term's: the dust's dynamics never read rho_Lambda (dV'/d rho_Lambda = 0)")

# ================================================================================================ W3
R.banner("W3  PERTURBATIONS: Schrodinger-Poisson dispersion, sound speed, anisotropic stress (sympy)")
hb, mm_, k_, w_, Gs, rb = sp.symbols("hbar m k omega G rhobar", positive=True)
al, ga = sp.symbols("alpha gamma")
Ek = hb ** 2 * k_ ** 2 / (2 * mm_); gg = 4 * sp.pi * Gs * mm_ * rb / k_ ** 2
Msys = sp.Matrix([[hb * w_ - Ek + gg, gg], [gg, -hb * w_ - Ek + gg]])
disp = sp.solve(sp.Eq(Msys.det(), 0), w_ ** 2)
target_disp = (hb * k_ ** 2 / (2 * mm_)) ** 2 - 4 * sp.pi * Gs * rb
okdisp = len(disp) == 1 and sp.simplify(disp[0] - target_disp) == 0
P(f"    linearised SP: omega^2 = {sp.simplify(disp[0]) if disp else None}")
check("W3 [sympy] linearised Schrodinger-Poisson gives omega^2 = (hbar k^2/2m)^2 - 4 pi G rho, i.e. c_s^2 = (hbar k/2m)^2 >= 0 for every k",
      f"matches: {okdisp}", okdisp, load_bearing=LB0)
# anisotropic stress at linear order
e_ = sp.symbols("e"); xs_ = sp.symbols("x1:4"); tt_ = sp.symbols("tau")
phib = sp.Function("phib")(tt_); dphi = sp.Function("dphi")(tt_, *xs_)
phif = phib + e_ * dphi
Tij = sp.Matrix(3, 3, lambda i, j: sp.diff(phif, xs_[i]) * sp.diff(phif, xs_[j]))
trace = sum(Tij[i, i] for i in range(3))
aniso = (Tij - trace / 3 * sp.eye(3)).applyfunc(lambda q: sp.expand(q).coeff(e_, 1))
okvis = aniso == sp.zeros(3, 3)
check("W3 [sympy] c_vis^2 = 0: the traceless stress of a scalar is second order in the perturbation (zero at linear order)",
      f"linear traceless stress = 0: {okvis}", okvis, load_bearing=LB0)
def cs2_wave(mm, kcom_Mpc, z):         # (hbar k_phys / 2 m c)^2, dimensionless
    kphys = kcom_Mpc * (1 + z) / MPC
    return (hbar * kphys * c / (2 * mm * eV)) ** 2
cs2_rec = cs2_wave(M_MIN, 0.3, 1100.0)
cs_forest = math.sqrt(cs2_wave(M_MIN, 10 * h, 3.0)) * c / 1e3
P(f"    m = {M_MIN:.0e} eV: c_s^2(z = 1100, k = 0.3/Mpc) = {cs2_rec:.2e} (<= 1e-5); c_s(z = 3, k = 10 h/Mpc) = {cs_forest:.2e} km/s (<= 5); "
  f"|w(1100)| <= {w1100:.1e}; c_vis^2 = 0")
num("W3", dict(cs2_rec=cs2_rec, cs_forest_kms=cs_forest))
okDUST = cs2_rec <= CS2_CMB and cs_forest <= CS_FOREST and w1100 <= W_TOL and okvis
gate("W", "G-DUST", "PASS-CONDITIONAL (m >= 2e-20 eV declared)" if okDUST else "FAIL", okDUST,
     f"(w, c_s^2, c_vis^2) at z = 1100 = (<= {w1100:.1e}, {cs2_rec:.1e}, 0); forest c_s {cs_forest:.1e} km/s")

# ================================================================================================ G-ONSET (road W)
ok_on_i = w3400 <= W_TOL
ok_on_ii = z_on >= ZREQ_MAX
gate("W", "G-ONSET", "PASS (timing); amount -> G-AMOUNT" if (ok_on_i and ok_on_ii) else "FAIL", ok_on_i and ok_on_ii,
     f"(i) |w(3400)| <= {w3400:.1e}; (ii) z_on = {z_on:.2e} >= {ZREQ_MAX:.0e}, the largest value the frozen z_req can take (frozen z_req = {ZREQ}: "
     f"undefined because the frozen lensed controls failed; post-hoc analogue {ZREQ_POSTHOC}); (iii) Omega_c h^2 = 0.120 only by the declared "
     f"phi_i -> G-AMOUNT")

# ================================================================================================ G-AMOUNT (road W)
mis0 = MIS["m_min (Lyman-alpha)"]
gate("W", "G-AMOUNT", f"AMOUNT FREE (needs phi_i = {mis0['phi_i_over_MPl']:.2e} Mbar_Pl at m = 2e-20 eV, plus m itself)", False,
     f"omega_c = 0.120 needs phi_i = {mis0['phi_i_GeV']:.2e} GeV (Delta V = {mis0['dV_over_rhoL']:.1e} rho_Lambda, a second scale "
     f"{mis0['dV_quarter_eV']:.0f} eV); at the A3 candidate q = 3/4 (m = {MIS['q=3/4']['m_eV']:.1e} eV) phi_i = {MIS['q=3/4']['phi_i_over_MPl']:.2e} Mbar_Pl. "
     f"rho_c/rho_Lambda = {RATIO:.3f} (1+z)^3: no constant tie to rho_Lambda can give it without singling out today")

# ================================================================================================ W4
R.banner("W4  SMALL-SCALE POWER: Hu-Barkana-Gruzinov transfer at the declared mass")
def T_hbg(kMpc, mm):
    m22 = mm / 1e-22
    xx = 1.61 * m22 ** (1 / 18) * kMpc / (9 * m22 ** 0.5)
    return math.cos(xx ** 3) / (1 + xx ** 8)
sup02 = 1 - T_hbg(0.2 * h, M_MIN) ** 2; T2_10 = T_hbg(10 * h, M_MIN) ** 2
P(f"    m = {M_MIN:.0e} eV: 1 - T^2(0.2 h/Mpc) = {sup02:.2e} (<= 0.03); T^2(10 h/Mpc) = {T2_10:.6f} (>= 0.5)")
P("    the seeding correspondence: a wave field converts at H(z_on) = m, so the frozen seeding table's EXCLUDED z_seed <= 1e4 says m >~ "
  f"{H_eV(1e4):.1e} eV (z_seed = 1e4); m_min = {M_MIN:.0e} eV onsets at {z_on:.1e}, above every grid z_seed")
num("W4", dict(sup02=sup02, T2_10=T2_10, m_floor_from_seeding_1e4=H_eV(1e4)))
okPK = sup02 <= 0.03 and T2_10 >= 0.5
gate("W", "G-PK", "PASS-CONDITIONAL (m >= 2e-20 eV declared; L383 floor 2-5e-19 eV reported)" if okPK else "FAIL", okPK,
     f"HBG: 1 - T^2(0.2 h/Mpc) = {sup02:.1e}, T^2(10 h/Mpc) = {T2_10:.4f}; the mass is a declared constant (stage A, A3: not derived)")

# ================================================================================================ W5
R.banner(f"W5  STREAM TEST (1-D free streaming): exact FFT Schrodinger (nu = {NU:g}) vs exact collisionless vs the sticky single-valued fluid")
N, NQ, SIG, A = 2 ** 15, 2 ** 21, 0.01, 1 / (2 * math.pi)
dx = 1.0 / N
xg = np.arange(N) * dx
kk = 2 * np.pi * np.fft.fftfreq(N, d=dx)
S0 = lambda q: (A / (2 * math.pi)) * np.cos(2 * math.pi * q)
v0 = lambda q: -A * np.sin(2 * math.pi * q)
G_sm = np.exp(-0.5 * (kk * SIG) ** 2)
def smooth(rho):
    return np.real(np.fft.ifft(np.fft.fft(rho) * G_sm))
def cic(xpos):
    xp = np.mod(xpos, 1.0) / dx
    i0 = np.floor(xp).astype(np.int64); fr = xp - i0
    rho = np.bincount(i0 % N, weights=1 - fr, minlength=N) + np.bincount((i0 + 1) % N, weights=fr, minlength=N)
    return rho / (len(xpos) * dx)
qg = -0.5 + (np.arange(NQ) + 0.5) / NQ
psi0 = np.exp(1j * S0(xg) / NU)
def lower_hull(xs, ys):
    hull = []
    for i in range(len(xs)):
        while len(hull) >= 2:
            i1, i2 = hull[-2], hull[-1]
            if (xs[i2] - xs[i1]) * (ys[i] - ys[i1]) - (ys[i2] - ys[i1]) * (xs[i] - xs[i1]) <= 0:
                hull.pop()
            else:
                break
        hull.append(i)
    return np.array(hull)
L1 = {}
for tt in (2.0, 3.0):
    psi_t = np.fft.ifft(np.fft.fft(psi0) * np.exp(-0.5j * NU * kk ** 2 * tt))
    rw = smooth(np.abs(psi_t) ** 2)
    rc = smooth(cic(qg + tt * v0(qg)))
    phi_l = qg ** 2 / 2 + tt * S0(qg)
    hidx = lower_hull(qg, phi_l)
    seg = np.searchsorted(hidx, np.arange(NQ))
    on = np.zeros(NQ, bool); on[hidx] = True
    xs_ = qg + tt * v0(qg)
    sidx = np.clip(seg, 1, len(hidx) - 1)
    ia, ib = hidx[sidx - 1], hidx[sidx]
    slope = (phi_l[ib] - phi_l[ia]) / (qg[ib] - qg[ia])
    xstick = np.where(on, xs_, slope)
    rf = smooth(cic(xstick))
    nrm = np.sum(rc) * dx
    L1[tt] = dict(wave=float(np.sum(np.abs(rw - rc)) * dx / nrm), fluid=float(np.sum(np.abs(rf - rc)) * dx / nrm),
                  stuck_mass_fraction=float(1 - on.mean()) if False else float(np.mean(~on)))
    P(f"    t = {tt:g} t_sc: L1(wave, collisionless) = {L1[tt]['wave']:.4f}; L1(sticky fluid, collisionless) = {L1[tt]['fluid']:.4f}; "
      f"fluid mass in the shock {L1[tt]['stuck_mass_fraction']:.3f}   {R.el()}")
num("W5", {str(k): v for k, v in L1.items()} | dict(nu=NU, N=N, NQ=NQ, sigma=SIG))
okwave = all(L1[tt]["wave"] <= 0.02 for tt in L1)
power = all(L1[tt]["fluid"] > 0.02 for tt in L1)
check("W5 [the stream test] the wave field's coarse-grained density matches the exact collisionless answer (L1 <= 0.02 at t = 2 and 3 t_sc)"
      + (" [MUTATE: must FAIL]" if MODE == 1 else ""),
      f"L1 = {L1[2.0]['wave']:.4f} / {L1[3.0]['wave']:.4f}", okwave, load_bearing=True)
check("W5-POWER [control that can fail] the single-valued sticky fluid FAILS the same match (L1 > 0.02 at both times): the test has power",
      f"L1 = {L1[2.0]['fluid']:.4f} / {L1[3.0]['fluid']:.4f}", power, load_bearing=LB0)
gate("W", "G-STREAM", "PASS (self-gravitating version INHERITED from L374)" if (okwave and power) else ("VOID (no power)" if not power else "FAIL"),
     okwave and power, f"wave L1 {L1[2.0]['wave']:.4f}/{L1[3.0]['wave']:.4f} vs fluid control {L1[2.0]['fluid']:.3f}/{L1[3.0]['fluid']:.3f}")

# ================================================================================================ W6
R.banner("W6  MERGER (Bullet class)")
Lm = 200 * KPC
cq = hbar * (2 * math.pi / Lm) * c ** 2 / (2 * M_MIN * eV) / 1e3        # km/s
lam_db = 2 * math.pi * hbar * c ** 2 / (M_MIN * eV * 3e6) / KPC * 1e3   # pc at 3000 km/s
P(f"    quantum-pressure speed at L = 200 kpc: c_q = hbar k/2m = {cq:.2e} km/s (<= 30); de Broglie length at 3000 km/s = {lam_db:.3f} pc; "
  f"lambda = 0: no non-gravitational self-interaction; multistreaming from W5")
num("W6", dict(cq_kms=cq, lambda_dB_pc=lam_db))
okM = cq <= 30 and okwave and power
gate("W", "G-MERGER", "PASS" if okM else "FAIL", okM, f"c_q {cq:.1e} km/s; superposes (W5); sigma/m = 0 (lambda = 0)")

# ================================================================================================ W7
R.banner("W7  STABILITY AND GRAVITATIONAL WAVES (sympy)")
tt_s, zz = sp.symbols("t z", real=True)
ee = sp.symbols("e")
af = sp.Function("a", positive=True)(tt_s); hf = sp.Function("h")(tt_s, zz)
X4 = [tt_s, sp.Symbol("x"), sp.Symbol("y"), zz]
gm = sp.diag(-1, af ** 2 * (1 + ee * hf), af ** 2 * (1 - ee * hf), af ** 2)
gi = gm.inv()
def christ(g, gi, X):
    n = 4
    return [[[sp.simplify(sum(gi[a_, d_] * (sp.diff(g[d_, b_], X[c_]) + sp.diff(g[d_, c_], X[b_]) - sp.diff(g[b_, c_], X[d_])) for d_ in range(n)) / 2)
              for c_ in range(n)] for b_ in range(n)] for a_ in range(n)]
Gm = christ(gm, gi, X4)
def ricci(Gm, X):
    n = 4
    Rm = sp.zeros(n, n)
    for b_ in range(n):
        for d_ in range(n):
            Rm[b_, d_] = sum(sp.diff(Gm[a_][b_][d_], X[a_]) for a_ in range(n)) - sum(sp.diff(Gm[a_][b_][a_], X[d_]) for a_ in range(n)) \
                + sum(Gm[a_][a_][e2] * Gm[e2][b_][d_] for a_ in range(n) for e2 in range(n)) - sum(Gm[a_][d_][e2] * Gm[e2][b_][a_] for a_ in range(n) for e2 in range(n))
    return Rm
Rm = ricci(Gm, X4)
Rs = sum(gi[i, j] * Rm[i, j] for i in range(4) for j in range(4))
Gxx = sum(gi[1, cc] * Rm[cc, 1] for cc in range(4)) - Rs / 2
Gyy = sum(gi[2, cc] * Rm[cc, 2] for cc in range(4)) - Rs / 2
lin = sp.simplify(sp.diff(Gxx - Gyy, ee).subs(ee, 0))
wave_op = sp.diff(hf, tt_s, 2) + 3 * sp.diff(af, tt_s) / af * sp.diff(hf, tt_s) - sp.diff(hf, zz, 2) / af ** 2
ratio = sp.simplify(lin / wave_op)
okT = ratio.free_symbols == set() and ratio != 0
P(f"    d/de (G^x_x - G^y_y)|_(e=0) = ({ratio}) x (h_tt + 3 H h_t - h_zz/a^2);  T^x_x - T^y_y = 0 for any homogeneous scalar (its stress is isotropic)")
check("W7 [sympy] with the scalar present the tensor mode obeys h_tt + 3H h_t - h_zz/a^2 = 0: c_T = 1 exactly",
      f"(G^x_x - G^y_y) linear part / wave operator = {ratio}", okT, load_bearing=LB0)
# Hamiltonian positivity for the complex field (flat space)
p1, p2, g1, g2, f1, f2, msq, rL2 = sp.symbols("p1 p2 g1 g2 f1 f2 msq rho_L", real=True)
Lc = sp.Rational(1, 2) * (p1 ** 2 + p2 ** 2) - sp.Rational(1, 2) * (g1 ** 2 + g2 ** 2) - msq / 2 * (f1 ** 2 + f2 ** 2) - rL2
Hc = sp.expand(sum(sp.diff(Lc, q) * q for q in (p1, p2)) - Lc)
quad = sp.hessian(Hc, (p1, p2, g1, g2, f1, f2))
eigs = list(quad.eigenvals().keys())
okH = all(sp.simplify(e_v.subs(msq, sp.Symbol("M2", positive=True))).is_nonnegative for e_v in eigs)
P(f"    Hamiltonian density = {Hc}  (Phi = (f1 + i f2)/sqrt 2); Hessian eigenvalues {eigs}")
check("W7 [sympy] no ghost: the Hamiltonian density is a positive quadratic form (plus the constant rho_Lambda) for m^2 > 0; dispersion omega^2 = k^2 + m^2",
      f"eigenvalues {eigs}", okH, load_bearing=LB0)
# kernel invisibility: INHERITED (provenance of the record's committed lanes)
prov = {}
for lab, rel in (("L353", "real_research/g03_audit_2026/L353_kernel_invisible_dark_component_results.json"),
                 ("MS1", "real_research/mond_sector_gate_2026/MS1_gate_variation_reciprocity_results.json"),
                 ("FL1", "real_research/dark_fluid_2026/FL1_order_parameter_results.json")):
    try:
        jj = json.load(open(os.path.join(C.REPO, rel)))
        prov[lab] = dict(path=rel, n_checks=jj.get("n_checks"), n_fail_load_bearing=jj.get("n_fail_load_bearing"))
    except Exception as ex:
        prov[lab] = dict(path=rel, error=repr(ex))
fl2 = open(os.path.join(C.REPO, "real_research/dark_fluid_2026/FL2_dark_slot_with_the_kick.out")).read().strip().splitlines()[-1]
prov["FL2"] = dict(path="real_research/dark_fluid_2026/FL2_dark_slot_with_the_kick.out", last_line=fl2.strip())
P("    kernel invisibility INHERITED (not re-derived): " + "; ".join(f"{k}: {v.get('n_checks')} checks, {v.get('n_fail_load_bearing')} load-bearing failures"
                                                          if "n_checks" in v else f"{k}: {v.get('last_line', v.get('error'))}" for k, v in prov.items()))
okprov = all(v.get("n_fail_load_bearing") == 0 for k, v in prov.items() if "n_checks" in v) and "load-bearing failures: 0" in fl2
rho_loc = 0.4e9 * eV / c ** 2 / 1e-6           # 0.4 GeV/cm^3 in kg/m^3
Msolar = rho_loc * 4 / 3 * math.pi * (9.5 * AU) ** 3 / MSUN
P(f"    solar system: dark mass inside 9.5 AU at 0.4 GeV/cm^3 = {Msolar:.2e} Msun (<= 1.7e-10, Pitjeva & Pitjev 2013)")
num("W7", dict(tensor_ratio=str(ratio), hamiltonian_eigs=[str(e_v) for e_v in eigs], provenance=prov, M_dark_9p5AU_Msun=Msolar))
okSTAB = okT and okH and okdisp and okprov and Msolar <= 1.7e-10
gate("W", "G-STAB/GW", "PASS (kernel invisibility INHERITED)" if okSTAB else "FAIL", okSTAB,
     f"no ghost, c_s^2 >= 0, m^2 > 0, c_T = 1 (derived), metric coupling only; L353/MS1/FL1/FL2 provenance clean: {okprov}; solar {Msolar:.1e} Msun")

# ================================================================================================ ROAD S
R.banner("ROAD S  THE SEEDED SHIFT CHARGE (ghost-condensate P(X)), scored with stage A's A2 results")
Xs_, X0s, M4s, rLs = sp.symbols("X X0 M4 rho_Lambda", positive=True)
Ps = -rLs + M4s / 2 * (Xs_ / X0s - 1) ** 2
rho_at_X0 = sp.simplify((2 * Xs_ * sp.diff(Ps, Xs_) - Ps).subs(Xs_, X0s)); P_at_X0 = sp.simplify(Ps.subs(Xs_, X0s))
okSBG = sp.simplify(rho_at_X0 - rLs) == 0 and sp.simplify(P_at_X0 + rLs) == 0
gate("S", "G-BG", "PASS" if (okSBG and okBG) else "FAIL", okSBG and okBG,
     f"at X0: rho = {rho_at_X0}, P = {P_at_X0} -> w = -1; the same a0 tie as road W ({d_can:+.1e} / {d_alt:+.1e})")
def M_needed(z, tol):            # c_s^2 = rho_d / (4 M^4) <= tol  ->  M (eV)
    return (to_eV4(rho_d(z)) / (4 * tol)) ** 0.25
M_dust = M_needed(1100.0, CS2_CMB)
cs_f_S = math.sqrt(to_eV4(rho_d(3.0)) / (4 * M_dust ** 4)) * c / 1e3
M_single = (1e3 * rhoL_eV4) ** 0.25
cs2_single = to_eV4(rho_d(1100.0)) / (4 * M_single ** 4)
P(f"    G-DUST: c_s^2 = rho_d/(4 M^4) <= 1e-5 at z = 1100 needs M >= {M_dust:.3f} eV; forest c_s(z=3) there = {cs_f_S:.2e} km/s; "
  f"single scale (M^4 = 1e3 rho_Lambda, M = {M_single * 1e3:.2f} meV): c_s^2(1100) = {cs2_single:.2e}")
gate("S", "G-DUST", f"PASS-CONDITIONAL (needs M >= {M_dust:.2f} eV, a second scale; the single-scale tie FAILS, c_s^2(1100) = {cs2_single:.1e})", True,
     f"w = c_s^2/2, c_vis^2 = 0 (perfect fluid); forest {cs_f_S:.1e} km/s at M = {M_dust:.2f} eV")
M_on_i = (to_eV4(rho_d(3400.0)) / (8 * W_TOL)) ** 0.25          # |w| = rho_d / (8 M^4) <= 1e-5 at z_eq
M_on_ii = (to_eV4(rho_d(ZREQ_MAX)) / (8 * W_TOL)) ** 0.25
gate("S", "G-ONSET", f"PASS-CONDITIONAL (needs M >= {M_on_ii:.3g} eV to stay in the dust regime back to z = 1e7)", True,
     f"(i) |w(3400)| <= 1e-5 needs M >= {M_on_i:.2f} eV; (ii) the dust regime at z = {ZREQ_MAX:.0e} needs M >= {M_on_ii:.3g} eV; a SEEDED charge must be "
     f"created at a z_seed not excluded by the frozen table (z_seed <= 1e4 EXCLUDED)")
need_res = RATIO * (1 + 1e5) ** 3
gate("S", "G-AMOUNT", "AMOUNT FREE (needs the charge C = rho_c0/sqrt(2 X0), i.e. the amount itself)", False,
     f"C is an integration constant (A2.1-A2.3); a seeding event needs a reservoir >= rho_c(z_s) = {need_res:.1e} rho_Lambda at z_s = 1e5 (the earliest "
     f"grid z_seed not excluded); recombination's reservoirs fall short by x2.6 to x5e8 (A2.5)")
gate("S", "G-STREAM", "FAIL", False,
     f"the single-valued gradient flow (u ~ d phi) is this road's dust limit: the W5 sticky-fluid control misses the collisionless answer by L1 = "
     f"{L1[2.0]['fluid']:.3f}/{L1[3.0]['fluid']:.3f}; L374 (committed): the condensate EFT breaks at the first stream crossing")
# Jeans scale at M = M_dust, comoving, z = 1100 (k_J ~ a is smallest there over [0, 1100])
def kJ_com_hMpc(Mev, z):
    cs = math.sqrt(to_eV4(rho_d(z)) / (4 * Mev ** 4)) * c
    return math.sqrt(4 * math.pi * G * rho_d(z)) / cs / (1 + z) * MPC / h
kJ_d = kJ_com_hMpc(M_dust, 1100.0)
M_pk = M_dust * math.sqrt(2.0 / kJ_d)
P(f"    G-PK: comoving Jeans k_J(z = 1100) at M = {M_dust:.2f} eV = {kJ_d:.2e} h/Mpc (need >= 2); k_J ~ M^2 -> M >= {M_pk:.1f} eV "
  f"(k_J(z = 1100, M) = {kJ_com_hMpc(M_pk, 1100.0):.2f} h/Mpc)")
gate("S", "G-PK", f"PASS-CONDITIONAL (needs M >= {M_pk:.2f} eV; at the coldness-minimal M = {M_dust:.2f} eV, k_J(1100) = {kJ_d:.2f} h/Mpc: "
     f"{'passes' if kJ_d >= 2 else 'fails'} there; the binding condition is G-ONSET's M)", True,
     f"k_J = a sqrt(4 pi G rho_d)/c_s with c_s^2 = rho_d/(4 M^4); the v9 DBI chassis with M^4 pinned near rho_Lambda failed this (record: 18-300x)")
gate("S", "G-MERGER", "FAIL", False, "(i) a single-valued flow cannot pass through itself (G-STREAM FAIL); the record's merger gate")
# (box phi)^2 adds no hdot^2 / h_z^2 term
phs = sp.Function("phi")(tt_s)
sqrtg_t = sp.sqrt(-gm.det())
boxphi = (1 / sqrtg_t) * sp.diff(sqrtg_t * gi[0, 0] * sp.diff(phs, tt_s), tt_s)
Lbox = sp.series(sp.simplify(sqrtg_t * boxphi ** 2), ee, 0, 3).removeO()
ht_, hz_ = sp.symbols("h_t h_z")
L2 = sp.expand(Lbox.coeff(ee, 2)).subs({sp.Derivative(hf, tt_s): ht_, sp.Derivative(hf, zz): hz_})
c_ht2 = sp.simplify(sp.diff(L2, ht_, 2)); c_hz2 = sp.simplify(sp.diff(L2, hz_, 2))
P(f"    (box phi)^2 sqrt(-g) at O(h^2): d^2/d(h_t)^2 = {c_ht2}; d^2/d(h_z)^2 = {c_hz2}  (no kinetic or gradient term for h)")
okSc = c_ht2 == 0 and c_hz2 == 0
check("S-W7 [sympy] the ghost condensate's (box phi)^2 term adds no h_t^2 or h_z^2 term (P(X) has no metric derivatives): c_T = 1 on road S too",
      f"coefficients {c_ht2}, {c_hz2}", okSc, load_bearing=LB0)
gate("S", "G-STAB/GW", "PASS-CONDITIONAL (needs C > 0, the record's forced sign, and the declared k^4 term)" if (okSc and okT) else "FAIL", okSc and okT,
     "c_s^2 = P_X/(P_X + 2 X P_XX) > 0 iff P_X > 0 iff C > 0; P_X + 2 X P_XX > 0 near X0 (no ghost); c_T = 1")

# ================================================================================================ the gate table
R.banner("THE GATE TABLE")
for road, lab in (("W", "ROAD W -- linear complex wave field, V = rho_Lambda + m^2 |Phi|^2 (quanta would be light bosons)"),
                  ("S", "ROAD S -- seeded shift charge, ghost-condensate P(X) with P(X0) = -rho_Lambda")):
    P(f"  {lab}")
    for gname, gv in GATES[road].items():
        P(f"    {gname:10s} {gv['verdict']}")
num("GATES", GATES)
num("mode", MODE)
P(f"\n  run time {time.time() - T0:.0f} s.  kappa = 1/2 FITTED; the cold mass is still required; nothing here says the theory is closed.")
nf = R.write(here=HERE)
sys.exit(1 if nf else 0)
