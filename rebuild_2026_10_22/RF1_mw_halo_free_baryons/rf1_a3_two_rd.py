#!/usr/bin/env python3
"""RF1 A3: route E on a two-scale-length halo-free disc (thin R_t from LN16, thick R_T from BH&G16), M_bb Valenti+16, McKee gas.
Frozen in AMENDMENTS.md A3 before any number. Machinery copied from rf1_mw.py (60c9eae3d1) and X5's family, read-only.
Run: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I rf1_a3_two_rd.py   (RF1_MUTATE=1: q = 0, S x 0.5; K1 must fail, exit 1)
kappa = 1/2 FITTED; footings never pooled; cold dark energy, never a particle; not theory closed; nothing here says the data favour the framework.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, time, hashlib, resource
import numpy as np
from scipy.optimize import brentq, minimize_scalar
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REB, "X5_mw_joint_baryons"))
import x5_lib as L  # noqa: E402
MUT = os.environ.get("RF1_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = []; T0 = time.time()
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

G = 4.30091e-6; KZU = 2 * math.pi * G * 1e6
SIG_A0 = {"canonical": 106.879e6, "alt": 129.165e6}; SREF = 70.50
QF = {"canonical": 0.0 if MUT else 0.892, "alt": 0.0 if MUT else 0.748}
EM1 = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
TA, TB = "A_c2b_refit", "B_cfg886_bg"
BGS = {t: dict(a=EM1["rows"][t]["R1"]["a"], b=EM1["rows"][t]["R1"]["b"], h=F3[t]["params"]["h"]) for t in (TA, TB)}
KZ_BR, KZ_BR_E = 66.4, 2.2; LINE_KZ, LINE_OU = L.LINE_CHI2, 59.89250004508689
_T = json.load(open(os.path.join(HERE, "rf1_rule_table.json"))); _G = np.array(_T["lg"]); FC = _T["fc"]
_LT = {TA: np.log10(_T["A"]), TB: np.log10(_T["B"])}
def S_nat(M200, tag): return (0.5 if MUT else 1.0) * 10 ** float(np.interp(math.log10(M200), _G, _LT[tag]))
def B_burkert(x):
    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def B_smooth(x):
    x = np.asarray(x, float); return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
def solve_r0(Mtot, Rout, Sig, Bf):
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(Bf(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    if lm(pk.x) < math.log(Mtot): return math.exp(pk.x), True
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), pk.x, xtol=1e-14)), False

ns = L.load_p4(); F = L.Family(ns); PS = ns["S"]; vE, eE = L.eilers_target(ns)
R0 = ns["R0_MW"]; BR_R, BR_K, BR_E5 = ns["BR_R"], ns["BR_K"], ns["BR_E5"]
ou = np.loadtxt(os.path.join(L.DATA, "mw_rc_ou2024_table1.tsv"), comments="#", skiprows=14)
OR, OV = ou[:, 0], ou[:, 1]; OE = np.hypot(0.5 * (ou[:, 2] + ou[:, 3]), np.where(OR <= 22.0, 0.03, 0.15) * OV)
A0C = L.A0_SI["canonical"]  # as rf1_mw.py
GAS_MCM = F.sig_gas_R0 / 1e6; MGAS_MCM = F.gas_mass(); ZT, ZK = ns["ZD_THIN"], ns["ZD_THICK"]
P(f"RF1 A3 two-scale-length disc {'MUTATE (q = 0, S x 0.5)' if MUT else 'normal run'}  (frozen: AMENDMENTS.md A3; RF1 criteria 9468ee04b2)")
P(f"McMillan thin share of stellar surface density at R0 (held, labelled): f_thin {F.f_thin:.4f}; gas 13.7 McKee on McMillan forms; M_bb 2.0e10 Valenti+16")

def newton(rhof):
    Mu = PS.mass_unit(A0C); g = ns["mw_grid"](6.6e10 / Mu)
    rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); Mt = 2 * float(np.sum(rho1 * g.vol))
    pr = PS.Problem(g, rho1, Mt, 0.0, Lam=0.0); Phi = pr.solve_newton(); o = ns["mw_obs"](g, Phi, A0C)
    return dict(Mb=Mt * Mu, K=np.array(o["K"]), K_R0=o["K_R0"], vc_R0=o["vc_R0"], vou=L.vc_plane(ns, g, Phi, A0C, OR))
def gas_rho(R, z):
    zz = np.abs(z); Rs = np.maximum(R, 1e-6)
    return ((ns["S0_HI"] * np.exp(-4.0 / Rs - Rs / 7.0) / (4 * 0.085)) / np.cosh(np.minimum(zz / (2 * 0.085), 300)) ** 2
            + (ns["S0_H2"] * np.exp(-12.0 / Rs - Rs / 1.5) / (4 * 0.045)) / np.cosh(np.minimum(zz / (2 * 0.045), 300)) ** 2)

def cell2(sb, mbb, rt, rT, gas_col=13.7):
    """Two scale lengths. Same construction as X5 Family.rho / rf1_mw.cell, with thin R_t and thick R_T; share at R0 = McMillan's."""
    gs = gas_col / GAS_MCM
    sig_star = (sb - (gs - 1) * GAS_MCM) * 1e6 - F.sig_gas_R0
    st = F.f_thin * sig_star * math.exp(R0 / rt); sk = (1 - F.f_thin) * sig_star * math.exp(R0 / rT)
    fb = mbb / F.M_bulge_mcm
    RHO0_B, ALPHA_B, R0_B, RCUT_B, Q_B = ns["RHO0_B"], ns["ALPHA_B"], ns["R0_B"], ns["RCUT_B"], ns["Q_B"]
    def rhof(R, z):
        zz = np.abs(z)
        thin = (st / (2 * ZT)) * np.exp(-zz / ZT - R / rt); thick = (sk / (2 * ZK)) * np.exp(-zz / ZK - R / rT)
        rp = np.maximum(np.sqrt(R * R + (zz / Q_B) ** 2), 1e-7)
        bulge = fb * (RHO0_B / (1 + rp / R0_B) ** ALPHA_B * np.exp(-(rp / RCUT_B) ** 2))
        return thin + thick + bulge + gs * gas_rho(R, z)
    bar = newton(rhof); M_thin, M_thick = 2 * math.pi * st * rt * rt, 2 * math.pi * sk * rT * rT
    Mana = M_thin + M_thick + mbb + gs * MGAS_MCM
    return dict(sig_b=sb, M_bb=mbb, R_t=rt, R_T=rT, Mstar=M_thin + M_thick + mbb, M_thin=M_thin, M_thick=M_thick, bar=bar, mass_rel=bar["Mb"] / Mana - 1)

RULES = [("OS1|canonical|PRIMARY", "os1", "canonical", 172.98), ("OS1|canonical|VARIANT", "os1", "canonical", 229.05),
         ("OS1|alt|PRIMARY", "os1", "alt", 172.98), ("OS1|alt|VARIANT", "os1", "alt", 229.05),
         ("N|canonical", "nat", "canonical", 0.0), ("N|alt", "nat", "alt", 0.0)]
def grade(bar, kind, foot, vlast, tag):
    bg = BGS[tag]; lM = bg["a"] + bg["b"] * (math.log10(bar["Mb"]) - 10); M200 = 10 ** lM
    if kind == "os1": Sig, Bf = SIG_A0[foot] * (vlast / math.sqrt(2) / SREF) ** QF[foot], B_burkert
    else: Sig, Bf = S_nat(M200, tag) * 1e6, B_smooth
    rc = 3 * (100 * bg["h"] / 1e3) ** 2 / (8 * math.pi * G); R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
    r0, sat = solve_r0(M200, R200, Sig, Bf)
    gh = lambda r: G * math.pi * Sig * r0 ** 2 * Bf(np.asarray(r, float) / r0) / np.asarray(r, float) ** 2
    rk = np.hypot(BR_R, 1.1); K = bar["K"] + gh(rk) * 1.1 / rk / KZU
    r00 = math.hypot(R0, 1.1); K0 = bar["K_R0"] + float(gh(r00)) * 1.1 / r00 / KZU
    vc = math.sqrt(bar["vc_R0"] ** 2 + R0 * float(gh(R0))); vo = np.sqrt(bar["vou"] ** 2 + OR * gh(OR))
    cK = float(np.sum(((K - BR_K) / BR_E5) ** 2)); cO = float(np.sum(((vo - OV) / OE) ** 2))
    l1 = abs(vc - L.VC_BRIEF) <= L.VC_BRIEF_LINE and abs(vc - vE) <= 2 * eE
    D = max(cK / LINE_KZ, abs(vc - vE) / (2 * eE), cO / LINE_OU, abs(K0 - KZ_BR) / (2 * KZ_BR_E))
    return dict(S=Sig / 1e6, lgM200=lM, r0=r0, vc_R0=vc, K_R0=K0, chi2_Kz=cK, chi2_Ou=cO, L1=bool(l1), L2a=bool(cK <= LINE_KZ),
                L2b=bool(abs(K0 - KZ_BR) <= 2 * KZ_BR_E), L3=bool(cO <= LINE_OU), D=D)
L4 = ("L1", "L2a", "L2b", "L3")

checks = {}
# K1: single-R_d limit reproduces A1's graded cell (values from rf1_mw_results.json, A1 run ac81e1c324)
REF = {"N|canonical": (232.0662339084003, 68.53649338303407), "OS1|canonical|PRIMARY": (228.90290368882424, 67.63556402087326)}
c0 = cell2(47.1, 2.0e10, 1.9333333333333336, 1.9333333333333336); k1 = True
for n, k, f, v in RULES:
    if n in REF:
        g = grade(c0["bar"], k, f, v, TA); ok = abs(g["vc_R0"] / REF[n][0] - 1) < 1e-9 and abs(g["K_R0"] / REF[n][1] - 1) < 1e-9; k1 = k1 and ok
        P(f"K1 [{n}] R_t = R_T = 1.9333, Sig_b 47.1: vc {g['vc_R0']:.10f} (A1 {REF[n][0]:.10f}), Kz {g['K_R0']:.10f} (A1 {REF[n][1]:.10f}): {'PASS' if ok else 'FAIL'}")
checks["K1"] = k1

RT = [2.38, 2.51, 2.64, 2.77, 2.90]; RTH = [1.6, 1.8, 2.0, 2.2, 2.4]
cells = [cell2(s, 2.0e10, rt, rT) for s in L.SIG_B_GRID for rt in RT for rT in RTH]
checks["K2"] = all(abs(c["mass_rel"]) < 2e-3 for c in cells) and abs(c0["mass_rel"]) < 2e-3
P(f"K2 grid-vs-analytic mass, 125 cells: max |rel| {max(abs(c['mass_rel']) for c in cells):.2e}: {'PASS' if checks['K2'] else 'FAIL'}")
RES = dict(amendment="A3", mutate=MUT, f_thin=F.f_thin, R_t=RT, R_T=RTH, sig_b=L.SIG_B_GRID, M_bb=2.0e10, gas=13.7, boxes={}, verdict={})
P("\n=== A3 GRID: 125 cells, M_bb 2.0e10, McKee gas; per rule and background: cells passing all four lines; per-line counts; best D; max v_c(R0)")
for n, k, f, v in RULES:
    for t in (TA, TB):
        rows = [grade(c["bar"], k, f, v, t) for c in cells]
        allp = [i for i, r in enumerate(rows) if all(r[l] for l in L4)]
        ib = int(np.argmin([r["D"] for r in rows])); iv = int(np.argmax([r["vc_R0"] for r in rows]))
        box = dict(n_all=len(allp), counts={l: sum(r[l] for r in rows) for l in L4},
                   passing=[dict(sig_b=cells[i]["sig_b"], R_t=cells[i]["R_t"], R_T=cells[i]["R_T"]) for i in allp],
                   best=dict(sig_b=cells[ib]["sig_b"], R_t=cells[ib]["R_t"], R_T=cells[ib]["R_T"], **{x: rows[ib][x] for x in ("vc_R0", "K_R0", "chi2_Kz", "chi2_Ou", "D", "S", "lgM200")}),
                   max_vc=dict(sig_b=cells[iv]["sig_b"], R_t=cells[iv]["R_t"], R_T=cells[iv]["R_T"], vc_R0=rows[iv]["vc_R0"], K_R0=rows[iv]["K_R0"], chi2_Ou=rows[iv]["chi2_Ou"]))
        RES["boxes"][f"{n}|{t}"] = box; b = box["best"]; m = box["max_vc"]
        P(f"  [{n}|{t}] all-4 {box['n_all']}/125; lines {box['counts']}; best D {b['D']:.2f} (Sig_b {b['sig_b']}, R_t {b['R_t']}, R_T {b['R_T']}: vc {b['vc_R0']:.1f}, Kz {b['K_R0']:.1f}, chi2_Kz {b['chi2_Kz']:.1f}, chi2_Ou {b['chi2_Ou']:.0f}); max vc {m['vc_R0']:.1f} at (Sig_b {m['sig_b']}, R_t {m['R_t']}, R_T {m['R_T']}; Kz {m['K_R0']:.1f}, chi2_Ou {m['chi2_Ou']:.0f})")
        if box["passing"]: P(f"       passing: {box['passing']}")
for name, key in (("OS1|canonical", f"OS1|canonical|PRIMARY|{TA}"), ("OS1|alt", f"OS1|alt|PRIMARY|{TA}"), ("N", f"N|canonical|{TA}")):
    RES["verdict"][name] = ("PASS on halo-free baryons (two-scale-length disc)" if RES["boxes"][key]["n_all"] > 0 else "FAIL on halo-free baryons (two-scale-length disc)")
checks["K3"] = rss() < 1.0
P(f"\n=== VERDICT (A3, frozen; bg A, PRIMARY): {RES['verdict']}")
P("checks " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in sorted(checks.items())))
RES["checks"] = {k: bool(v) for k, v in checks.items()}
s = json.dumps(RES, indent=1, default=float, sort_keys=True); fn = os.path.join(HERE, f"rf1_a3_two_rd_results{TAG}.json"); open(fn, "w").write(s)
P(f"results sha256 {hashlib.sha256(s.encode()).hexdigest()}; peak RSS {rss():.2f} GB; runtime {time.time() - T0:.0f} s")
P("kappa = 1/2 FITTED; footings never pooled; not theory closed; nothing here says the data favour the framework.")
open(os.path.join(HERE, f"rf1_a3_two_rd{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(checks.values()) else 1)
