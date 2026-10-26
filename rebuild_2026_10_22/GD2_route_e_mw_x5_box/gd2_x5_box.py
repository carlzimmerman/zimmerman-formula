#!/usr/bin/env python3
"""GD2_route_e_mw_x5_box: route E (Newtonian + OS1-cored cold dark energy halo) on X5's frozen published-prior baryon box.

Criteria FROZEN_CRITERIA.md (78f30f7368, committed alone).  X5's family and grid and P4's machinery are used READ-ONLY
(x5_lib imported; P4's Problem.solve_newton).  Burkert closed form and compact root copied from X38 (A1).
Run:  OMP_NUM_THREADS=1 nice -n 15 python3 gd2_x5_box.py [--mutate]
kappa = 1/2 FITTED; footings never pooled; cold dark energy, not matter; not theory closed.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, time, itertools
import numpy as np
from scipy.optimize import brentq, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REB, "X5_mw_joint_baryons"))
import x5_lib as L  # noqa: E402

MUTATE = "--mutate" in sys.argv
TAG = "_MUTATE" if MUTATE else ""
T0 = time.time(); OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

G = 4.30091e-6; KZU = 2 * math.pi * G * 1e6                       # kpc (km/s)^2/Msun; K_z/(2 pi G) in Msun/pc^2
FEET = ("canonical", "alt")
SIG_A0 = {"canonical": 106.879e6, "alt": 129.165e6}                # Msun/kpc^2 (X38)
QF = {"canonical": 0.0 if MUTATE else 0.892, "alt": 0.0 if MUTATE else 0.748}
SREF = 70.50
VLAST = {"PRIMARY": 172.98, "VARIANT": 229.05}
EM1 = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
BGS = {t: dict(a=EM1["rows"][t]["R1"]["a"], b=EM1["rows"][t]["R1"]["b"], h=F3[t]["params"]["h"]) for t in ("A_c2b_refit", "B_cfg886_bg")}
KZ_BR, KZ_BR_E = 66.4, 2.2
LINE_KZ, LINE_OU = L.LINE_CHI2, 59.89250004508689

def B(x):
    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def solve_r0(Mtot, Rout, Sig):                                     # X38 A1 compact root
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    if lm(pk.x) < math.log(Mtot):
        return math.exp(pk.x), True
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), pk.x, xtol=1e-14)), False

ns = L.load_p4(); F = L.Family(ns); PS = ns["S"]
vE, eE = L.eilers_target(ns)
R0 = ns["R0_MW"]; BR_R = ns["BR_R"]; BR_K = ns["BR_K"]; BR_E5 = ns["BR_E5"]
ou = np.loadtxt(os.path.join(L.DATA, "mw_rc_ou2024_table1.tsv"), comments="#", skiprows=14)
OR, OV = ou[:, 0], ou[:, 1]; OE = np.hypot(0.5 * (ou[:, 2] + ou[:, 3]), np.where(OR <= 22.0, 0.03, 0.15) * OV)
A0C = L.A0_SI["canonical"]                                         # Newton is a0-free; solve once in canonical units
P(f"GD2_route_e_mw_x5_box {'MUTATE (q = 0, X38 core)' if MUTATE else 'normal run'}  (frozen 78f30f7368)")
P("route E: Newtonian baryons + OS1 Burkert halo; kappa = 1/2 FITTED; footings never pooled; not theory closed")
P(f"lines: L1 |vc-229.1|<=9.2 & |vc-{vE:.3f}|<={2*eE:.3f}; L2a chi2_Kz<={LINE_KZ:.3f}; L2b |Kz(R0)-66.4|<=4.4; L3 chi2_Ou<={LINE_OU:.3f}")

def newton(rhof):
    Mu = PS.mass_unit(A0C); g = ns["mw_grid"](6.6e10 / Mu)
    rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); Mt = 2 * float(np.sum(rho1 * g.vol))
    pr = PS.Problem(g, rho1, Mt, 0.0, Lam=0.0); Phi = pr.solve_newton()
    o = ns["mw_obs"](g, Phi, A0C)
    vou = L.vc_plane(ns, g, Phi, A0C, OR)
    return dict(Mb=Mt * Mu, K=np.array(o["K"]), K_R0=o["K_R0"], vc_R0=o["vc_R0"], vou=vou)

def grade(bar, foot, vlast, bg):
    Sig = SIG_A0[foot] * (vlast / math.sqrt(2) / SREF) ** QF[foot]
    lM = bg["a"] + bg["b"] * (math.log10(bar["Mb"]) - 10); M200 = 10 ** lM
    rc = 3 * (100 * bg["h"] / 1e3) ** 2 / (8 * math.pi * G); R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
    r0, sat = solve_r0(M200, R200, Sig)
    gh = lambda r: G * math.pi * Sig * r0 ** 2 * B(np.asarray(r, float) / r0) / np.asarray(r, float) ** 2
    rk = np.hypot(BR_R, 1.1); K = bar["K"] + gh(rk) * 1.1 / rk / KZU
    r00 = math.hypot(R0, 1.1); K0 = bar["K_R0"] + float(gh(r00)) * 1.1 / r00 / KZU
    vc = math.sqrt(bar["vc_R0"] ** 2 + R0 * float(gh(R0)))
    vo = np.sqrt(bar["vou"] ** 2 + OR * gh(OR))
    cK = float(np.sum(((K - BR_K) / BR_E5) ** 2)); cO = float(np.sum(((vo - OV) / OE) ** 2))
    l1 = abs(vc - L.VC_BRIEF) <= L.VC_BRIEF_LINE and abs(vc - vE) <= 2 * eE
    l2a, l2b, l3 = cK <= LINE_KZ, abs(K0 - KZ_BR) <= 2 * KZ_BR_E, cO <= LINE_OU
    D = max(cK / LINE_KZ, abs(vc - vE) / (2 * eE), cO / LINE_OU, abs(K0 - KZ_BR) / (2 * KZ_BR_E))
    return dict(Sig_ratio=Sig / SIG_A0[foot], lgM200=lM, r0=r0, sat=sat, vc_R0=vc, K_R0=K0, chi2_Kz=cK, chi2_Ou=cO,
                L1=bool(l1), L2a=bool(l2a), L2b=bool(l2b), L3=bool(l3), D=D, dvc=vc - bar["vc_R0"], dK=K0 - bar["K_R0"])

checks = []
# K0: McMillan on this Newtonian path vs GD1/S3 baryon-only
m0 = newton(ns["rho_mcm"])
k0 = abs(m0["vc_R0"] / 177.234 - 1) < 0.01 and abs(m0["K_R0"] / 62.024 - 1) < 0.01
P(f"K0 McMillan Newtonian: V_b(R0) {m0['vc_R0']:.3f} (GD1 177.234), K_z,b {m0['K_R0']:.3f} (62.024), M_b {m0['Mb']:.4e}: {'PASS' if k0 else 'FAIL'}")
checks.append(("K0", k0))
RES = dict(frozen="78f30f7368", mutate=MUTATE, K0=dict(vb=m0["vc_R0"], kzb=m0["K_R0"]), cells=[])
Mgas = F.gas_mass(); k1 = True; k3 = True
P(f"\n{'Sig_b':>5} {'M_bb':>5} {'R_d':>5} {'M*':>6} RdIN M*IN | {'Vb':>6} {'Kb':>5} || per footing/V_last (bg A): vc  Kz  chi2Kz chi2Ou  L1 L2a L2b L3")
for sb, mbb, rd in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID):
    rhof, p = F.rho(sb, mbb, rd)
    bar = newton(rhof)
    Mana = p["M_thin"] + p["M_thick"] + p["M_bb"] + Mgas; rel = bar["Mb"] / Mana - 1
    k1 = k1 and abs(rel) < 2e-3
    c = dict(sig_b=sb, M_bb=mbb, R_d=rd, Mstar=p["Mstar"], tag_Rd_IN=bool(L.RD_TAG[0] <= rd <= L.RD_TAG[1]),
             tag_Mstar_IN=bool(L.MSTAR_TAG[0] <= p["Mstar"] <= L.MSTAR_TAG[1]), Mb=bar["Mb"], mass_rel_err=rel,
             Vb_R0=bar["vc_R0"], Kb_R0=bar["K_R0"], rows={})
    line = f"{sb:5.1f} {mbb/1e10:5.2f} {rd:5.3f} {p['Mstar']/1e10:6.3f} {'Y' if c['tag_Rd_IN'] else 'n':>4} {'Y' if c['tag_Mstar_IN'] else 'n':>4} | {bar['vc_R0']:6.1f} {bar['K_R0']:5.1f} ||"
    for foot in FEET:
        for vk, vl in VLAST.items():
            for t, bg in BGS.items():
                r = grade(bar, foot, vl, bg); c["rows"][f"{foot}|{vk}|{t}"] = r
                k3 = k3 and r["dvc"] > 0 and r["dK"] > 0
            r = c["rows"][f"{foot}|{vk}|A_c2b_refit"]
            line += f" {foot[:3]}/{vk[0]} {r['vc_R0']:5.1f} {r['K_R0']:5.1f} {r['chi2_Kz']:6.1f} {r['chi2_Ou']:6.0f} {'Y' if r['L1'] else '-'}{'Y' if r['L2a'] else '-'}{'Y' if r['L2b'] else '-'}{'Y' if r['L3'] else '-'} |"
    RES["cells"].append(c); P(line)

# ------------------------------------------------------------------ classes
def classify(key):
    cs = RES["cells"]; allp = [c for c in cs if all(c["rows"][key][l] for l in ("L1", "L2a", "L2b", "L3"))]
    vk = [c for c in cs if all(c["rows"][key][l] for l in ("L1", "L2a", "L2b"))]
    if any(c["tag_Rd_IN"] and c["tag_Mstar_IN"] for c in allp): cls = "FEASIBLE IN PRIORS"
    elif allp: cls = "FEASIBLE (WIDE PRIORS ONLY)"
    elif vk: cls = "V+K ONLY"
    else: cls = "INFEASIBLE"
    best = min(cs, key=lambda c: c["rows"][key]["D"]); b = best["rows"][key]
    n = {l: sum(c["rows"][key][l] for c in cs) for l in ("L1", "L2a", "L2b", "L3")}
    n["L1&L2a&L2b"] = len(vk); n["all"] = len(allp); n["L1&L2b"] = sum(c["rows"][key]["L1"] and c["rows"][key]["L2b"] for c in cs)
    vmax = max(cs, key=lambda c: c["rows"][key]["vc_R0"])
    return dict(cls=cls, counts=n, best=dict(sig_b=best["sig_b"], M_bb=best["M_bb"], R_d=best["R_d"], Mstar=best["Mstar"], **{k: b[k] for k in ("vc_R0", "K_R0", "chi2_Kz", "chi2_Ou", "D", "L1", "L2a", "L2b", "L3")}),
                max_vc=dict(vc=vmax["rows"][key]["vc_R0"], K_R0=vmax["rows"][key]["K_R0"], chi2_Kz=vmax["rows"][key]["chi2_Kz"], sig_b=vmax["sig_b"], M_bb=vmax["M_bb"], R_d=vmax["R_d"]),
                short_disc_best_vc=max(c["rows"][key]["vc_R0"] for c in cs if c["R_d"] <= 2.27))
RES["classes"] = {}
P("")
for foot in FEET:
    for vk in VLAST:
        for t in BGS:
            key = f"{foot}|{vk}|{t}"; cl = classify(key); RES["classes"][key] = cl
            b = cl["best"]; mv = cl["max_vc"]
            P(f"[{key}] {'GRADED' if t == 'A_c2b_refit' else 'reported'}: CLASS {cl['cls']}; counts {cl['counts']}")
            P(f"     best D {b['D']:.2f} at Sig_b {b['sig_b']}, M_bb {b['M_bb']:.3g}, R_d {b['R_d']:.3f}: vc {b['vc_R0']:.1f}, Kz {b['K_R0']:.1f}, chi2_Kz {b['chi2_Kz']:.1f}, chi2_Ou {b['chi2_Ou']:.0f}")
            P(f"     max vc in box {mv['vc']:.1f} (Sig_b {mv['sig_b']}, M_bb {mv['M_bb']:.3g}, R_d {mv['R_d']:.3f}; Kz {mv['K_R0']:.1f}, chi2_Kz {mv['chi2_Kz']:.1f}); short-disc max vc {cl['short_disc_best_vc']:.1f}")
r0p = RES["cells"][0]["rows"]
k2 = (abs(r0p["canonical|PRIMARY|A_c2b_refit"]["Sig_ratio"] - 1.635) < 1e-3 and abs(r0p["alt|PRIMARY|A_c2b_refit"]["Sig_ratio"] - 1.510) < 1e-3
      and abs(r0p["canonical|VARIANT|A_c2b_refit"]["Sig_ratio"] - 2.100) < 1e-3 and abs(r0p["alt|VARIANT|A_c2b_refit"]["Sig_ratio"] - 1.863) < 1e-3)
import resource
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
checks += [("K1_masses", k1), ("K2_OS1_factor", k2), ("K3_halo_raises", k3), ("K4_rss", rss < 1.0)]
P("")
for k, v in checks:
    P(f"{k}: {'PASS' if v else 'FAIL'}"); RES.setdefault("checks", {})[k] = bool(v)
P(f"VERDICT (PRIMARY, bg A): canonical {RES['classes']['canonical|PRIMARY|A_c2b_refit']['cls']}; alt {RES['classes']['alt|PRIMARY|A_c2b_refit']['cls']}")
P(f"runtime {time.time() - T0:.0f} s, peak RSS {rss:.2f} GB")
json.dump(RES, open(os.path.join(HERE, f"gd2_x5_box_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"gd2_x5_box{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(v for _, v in checks) else 1)
