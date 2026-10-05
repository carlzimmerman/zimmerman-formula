#!/usr/bin/env python3
"""CFG345: does B's cold component clump like CDM down to CFG344's M_cool(z_f=8)?
Frozen: FROZEN_CRITERIA.md (b4bb12ef3). Standard formulas, PROVISIONAL where transcribed from memory.
MUTATE (CFG345_MUTATE=1): wave field at the record's most suppressive allowed m = 2e-20 eV, road S at M = 4.24 eV.
Run from the repository root: python3 campaign_fresh_gravity/CFG345_cold_component_small_scales/cfg345_small_scales.py"""
import hashlib, json, math, os, sys
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG345_MUTATE") == "1"
SUF = "_MUTATE" if MUTATE else ""
SHA = hashlib.sha256(open(os.path.join(HERE, "FROZEN_CRITERIA.md"), "rb").read()).hexdigest()
LOG, OUT = [], {"lane": "CFG345", "frozen": "b4bb12ef3", "sha256": SHA, "mutate": MUTATE, "checks": {}}
def P(s=""): print(s); LOG.append(s)
def check(name, detail, ok):
    OUT["checks"][name] = {"detail": detail, "pass": bool(ok)}; P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

P(f"CFG345 cold-component small scales  MUTATE={MUTATE}  frozen sha256 {SHA}")
# ---------------------------------------------------------------- constants, cosmology (Planck 2018)
G, hbar, c, eV, Mpc, Msun = 6.674e-11, 1.054572e-34, 2.99792458e8, 1.602177e-19, 3.08568e22, 1.98892e30
h, Om, wc = 0.674, 0.315, 0.120
H0 = 100 * h * 1e3 / Mpc
rho_c0 = 3 * H0**2 / (8 * math.pi * G)                     # kg/m^3
rho_m_Msun_Mpc3 = rho_c0 * Om * Mpc**3 / Msun             # comoving mean matter density
z_eq = 3400.0
def M_of_k(k_Mpc):                                         # k in 1/Mpc (comoving)
    return 4 * math.pi / 3 * rho_m_Msun_Mpc3 * (math.pi / k_Mpc) ** 3
P(f"rho_m = {rho_m_Msun_Mpc3:.4e} Msun/Mpc^3 (2.775e11 h^2 Om = {2.775e11*h*h*Om:.4e})")

# ---------------------------------------------------------------- M_need from CFG344
J344 = json.load(open(os.path.join(ROOT, "campaign_fresh_gravity/CFG344_postreion_cold_accretion/cfg344_accretion_results.json")))
M_need = J344["HIST"]["8.0"]["M_cool"]
M_z2 = J344["HIST"]["8.0"]["M"]["2.0"]
check("C5 M_need from CFG344 JSON = 3.83e7 to 1%", f"{M_need:.4e} Msun (grows to {M_z2:.3e} by z=2); sensitivity z_f=10: {J344['HIST']['10.0']['M_cool']:.3e}, z_f=6: {J344['HIST']['6.0']['M_cool']:.3e}", abs(M_need / 3.83e7 - 1) < 0.01)

# ---------------------------------------------------------------- wave field (CFG288 road W = FL1 order parameter)
P("\n== Wave field: HBG (2000) transfer T = cos(x^3)/(1+x^8), x = 1.61 m22^(1/18) k / (9 m22^(1/2) /Mpc)")
def T(k, m22): x = 1.61 * m22 ** (1 / 18) * k / (9 * m22 ** 0.5); return math.cos(x**3) / (1 + x**8)
def k_half(m22, target):                                    # target = T^2 value
    return brentq(lambda k: T(k, m22) ** 2 - target, 1e-6, 9 * m22**0.5 / (1.61 * m22 ** (1 / 18)) * 1.16)
kh_T2 = k_half(1.0, 0.5); kh_T = k_half(1.0, 0.25)
A_T2, A_T = M_of_k(kh_T2), M_of_k(kh_T)                      # M_1/2 at m22 = 1; scales as m22^(-4/3)
k200 = k_half(200.0, 0.5)
check("C1 T^2=1/2 k_1/2 vs Hu+00 4.5 m22^(4/9)/Mpc (PROVISIONAL) within 5%", f"{kh_T2:.3f} /Mpc; scaling check m22=200: {k200/200**(4/9):.3f}", abs(kh_T2 / 4.5 - 1) < 0.05 and abs(k200 / 200 ** (4 / 9) / kh_T2 - 1) < 1e-3)
check("C2 T=1/2 M_1/2 vs Schive+16 3.8e10 m22^(-4/3) Msun (PROVISIONAL) within 10%", f"{A_T:.3e} Msun (k {kh_T:.3f}/Mpc)", abs(A_T / 3.8e10 - 1) < 0.10)

def kJ_wave(z, m_eV):                                       # comoving, 1/Mpc
    a = 1 / (1 + z); rho = rho_c0 * Om * a**-3
    k_phys = (16 * math.pi * G * rho) ** 0.25 * (m_eV * eV / c**2 / hbar) ** 0.5
    return a * k_phys * Mpc
kJeq = kJ_wave(z_eq, 1e-22)
check("C3 Jeans formula at z_eq vs CFG288's k_J,eq = 9 m22^(1/2)/Mpc within 15%", f"{kJeq:.3f} /Mpc", abs(kJeq / 9 - 1) < 0.15)

m22_star = (A_T2 / M_need) ** 0.75
m_rows = [("record window floor (Ly-a, Rogers & Peiris 2021 as quoted)", 2e-20), ("L383 dwarf-heating floor low", 2e-19),
          ("L383 floor high", 5e-19), ("q=3/4 numerology", 1.4e-18), ("window top", 37.0)]
if MUTATE: m_rows = [("MUTATE: most suppressive allowed m", 2e-20)]
WAVE = {"A_T2": A_T2, "A_T": A_T, "m22_star": m22_star, "m_star_eV": m22_star * 1e-22, "rows": []}
P(f"  A (T^2=1/2) = {A_T2:.4e} Msun, A (T=1/2) = {A_T:.4e} Msun;  bound M_1/2 <= M_need  <=>  m >= {m22_star*1e-22:.3e} eV (m22 >= {m22_star:.1f})")
P(f"  {'row':55s} {'m (eV)':>9s} {'M1/2 T^2=.5':>12s} {'M1/2 T=.5':>11s} {'M_J z=6/8/10':>30s} {'dn/dM ratio @M_need*':>20s}  ok?")
for lab, m in m_rows:
    m22 = m / 1e-22
    Mh2, Mh = A_T2 * m22 ** (-4 / 3), A_T * m22 ** (-4 / 3)
    MJ = [M_of_k(kJ_wave(z, m)) for z in (6, 8, 10)]
    M0 = 1.6e10 * m22 ** (-4 / 3)                           # Schive+16 HMF fit, PROVISIONAL
    hmf = (1 + (M_need / M0) ** -1.1) ** -2.2
    ok = Mh2 <= M_need
    WAVE["rows"].append({"label": lab, "m_eV": m, "M_half_T2": Mh2, "M_half_T": Mh, "M_J_z6_8_10": MJ, "hmf_ratio_at_Mneed": hmf, "below_M_need": ok})
    P(f"  {lab:55s} {m:9.2e} {Mh2:12.3e} {Mh:11.3e} {MJ[0]:9.2e}/{MJ[1]:9.2e}/{MJ[2]:9.2e} {hmf:20.3f}  {'yes' if ok else 'NO -> FLAG'}")
P("  (* Schive+16 halo-mass-function suppression [1+(M/M0)^-1.1]^-2.2, M0 = 1.6e10 m22^-4/3: PROVISIONAL, context only)")
OUT["wave"] = WAVE

# ---------------------------------------------------------------- road S: ghost-condensate P(X) dust, c_s^2 = rho_d/(4 M^4)
P("\n== Road S (condensate dust): c_s^2 = rho_d/(4 M^4), k_J = a sqrt(4 pi G rho_d)/c_s")
rho_d0_eV4 = wc * 8.0966e-11                                # eV^4 (rho_crit/h^2 = 1.0537e-5 GeV/cm^3)
rho_d0 = wc / h**2 * rho_c0                                 # kg/m^3
def kJ_S(z, M_eV):
    a = 1 / (1 + z); cs2 = rho_d0_eV4 * (1 + z) ** 3 / (4 * M_eV**4)
    return a * math.sqrt(4 * math.pi * G * rho_d0 * (1 + z) ** 3) / (math.sqrt(cs2) * c) * Mpc
k1100 = kJ_S(1100, 4.24) / h
check("C4 road S k_J(1100) at M=4.24 eV vs CFG288's 2.2 h/Mpc within 10%", f"{k1100:.3f} h/Mpc", abs(k1100 / 2.2 - 1) < 0.10)
B_eq = M_of_k(kJ_S(z_eq, 1.0))                               # M_J(z_eq) at M = 1 eV; scales M^-6
B_8 = M_of_k(kJ_S(8, 1.0))
M_star = (B_eq / M_need) ** (1 / 6); M_star8 = (B_8 / M_need) ** (1 / 6)
S_rows = [("G-DUST minimum (record)", 4.24), ("G-DUST from z=3400 (record)", 9.9), ("G-ONSET requirement (record)", 3300.0)]
if MUTATE: S_rows = [("MUTATE: record minimum", 4.24)]
SR = {"B_eq": B_eq, "B_8": B_8, "M_star_eV_zeq": M_star, "M_star_eV_z8": M_star8, "rows": []}
P(f"  bound M_J(z_eq) <= M_need <=> M >= {M_star:.2f} eV (lenient, at z=8: M >= {M_star8:.3f} eV)")
for lab, M in S_rows:
    Meq, M8 = B_eq * M**-6, B_8 * M**-6
    ok = Meq <= M_need
    SR["rows"].append({"label": lab, "M_eV": M, "M_J_zeq": Meq, "M_J_z8": M8, "below_M_need": ok})
    P(f"  {lab:32s} M = {M:8.2f} eV: M_J(z_eq) = {Meq:.3e}, M_J(z=8) = {M8:.3e} Msun  {'ok' if ok else 'NO -> FLAG'}")
OUT["roadS"] = SR

# ---------------------------------------------------------------- forest reach (record criteria)
k10 = 10 * h
M_forest = M_of_k(k10)
T2_10_floor = T(k10, 200.0) ** 2
P(f"\n== Forest: k = 10 h/Mpc <-> M = {M_forest:.3e} Msun ({M_forest/M_need:.0f}x M_need); T^2(10 h/Mpc) at 2e-20 eV = {T2_10_floor:.4f}")
OUT["forest"] = {"M_k10": M_forest, "ratio_to_M_need": M_forest / M_need, "T2_k10_m2e-20": T2_10_floor}

# ---------------------------------------------------------------- verdict
allC = all(v["pass"] for v in OUT["checks"].values())
if MUTATE:
    flags = [r["label"] for r in WAVE["rows"] if not r["below_M_need"]] + ["road S " + r["label"] for r in SR["rows"] if not r["below_M_need"]]
    OUT["flags"] = flags
    P(f"\nMUTATE flags (suppress at the record's most suppressive allowed value): {flags if flags else 'none'}")
    verdict = "MUTATE: " + ("SUPPRESSES at the record's extreme -> FLAGGED" if flags else "no suppression")
else:
    wave_all = all(r["below_M_need"] for r in WAVE["rows"])
    S_all = all(r["below_M_need"] for r in SR["rows"])
    inside_wave = 2e-20 <= m22_star * 1e-22 <= 37
    inside_S = 4.24 <= M_star  # bound lies inside the record's allowed range (M >= 4.24 eV, no upper limit)
    if wave_all and S_all: verdict = "CDM-LIKE"
    elif inside_wave or inside_S: verdict = "CONDITIONAL"
    else: verdict = "SUPPRESSED"
    P(f"\nB as frozen (T5 identity, STANDING): no microphysics specified -> no cutoff.")
    P(f"Wave field: CDM-like at M_need iff m >= {m22_star*1e-22:.3e} eV (inside window: {inside_wave}); road S iff M >= {M_star:.1f} eV (record's onset gate already demands 3.3 keV).")
P(f"VERDICT: {verdict}   (all controls pass: {allC})")
OUT["verdict"] = verdict; OUT["controls_pass"] = allC
json.dump(OUT, open(os.path.join(HERE, f"cfg345_small_scales{SUF}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg345_small_scales{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if allC else 1)
