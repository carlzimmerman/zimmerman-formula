#!/usr/bin/env python3
"""RF1_mw_halo_free_baryons: route E (OS1 and native N) on baryons with no halo in their normalisations, where any exist.
Criteria FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (9468ee04b2, committed alone). X5's family and P4's Newtonian solve READ-ONLY.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I rf1_mw.py     (RF1_MUTATE=1 twin: q = 0, S x 0.5; K2, K3 must fail)
kappa = 1/2 FITTED; footings never pooled; cold dark energy, never a particle; not theory closed; nothing here says the data favour the framework.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, time, itertools, hashlib, resource
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

# Candidate halo-free bulge rows: value and M/L must be read from the paper or its TeX on disk. Memory is never a source.
HALO_FREE_BULGE = []
BULGE_CANDIDATES = {"Kent 1992": "paper not on disk; value and M/L unread", "Dwek+95": "paper not on disk; value and M/L unread",
                    "pre-M2M clump-giant counts": "no paper on disk; value and M/L unread"}

G = 4.30091e-6; KZU = 2 * math.pi * G * 1e6
SIG_A0 = {"canonical": 106.879e6, "alt": 129.165e6}; SREF = 70.50
QF = {"canonical": 0.0 if MUT else 0.892, "alt": 0.0 if MUT else 0.748}
VLAST = {"PRIMARY": 172.98, "VARIANT": 229.05}
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
A0C = L.A0_SI["canonical"]
GAS_MCM = F.sig_gas_R0 / 1e6; ZT0, ZK0 = ns["ZD_THIN"], ns["ZD_THICK"]; MGAS_MCM = F.gas_mass()
P(f"RF1_mw_halo_free_baryons {'MUTATE (q = 0, S x 0.5)' if MUT else 'normal run'}  (criteria 9468ee04b2)")
P("route E: Newtonian baryons + OS1 or native-N halo; kappa = 1/2 FITTED; footings never pooled; not theory closed")
P(f"McMillan gas column at R0 {GAS_MCM:.3f} Msun/pc^2 (McKee 13.7 +- 1.6); Eilers target {vE:.3f} +- {eE:.3f}")

def newton(rhof):
    Mu = PS.mass_unit(A0C); g = ns["mw_grid"](6.6e10 / Mu)
    rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); Mt = 2 * float(np.sum(rho1 * g.vol))
    pr = PS.Problem(g, rho1, Mt, 0.0, Lam=0.0); Phi = pr.solve_newton(); o = ns["mw_obs"](g, Phi, A0C)
    return dict(Mb=Mt * Mu, K=np.array(o["K"]), K_R0=o["K_R0"], vc_R0=o["vc_R0"], vou=L.vc_plane(ns, g, Phi, A0C, OR))

def gas_rho(R, z):
    zz = np.abs(z); Rs = np.maximum(R, 1e-6)
    return ((ns["S0_HI"] * np.exp(-4.0 / Rs - Rs / 7.0) / (4 * 0.085)) / np.cosh(np.minimum(zz / (2 * 0.085), 300)) ** 2
            + (ns["S0_H2"] * np.exp(-12.0 / Rs - Rs / 1.5) / (4 * 0.045)) / np.cosh(np.minimum(zz / (2 * 0.045), 300)) ** 2)

def cell(sb, mbb, rd, gas_col=13.7, zs=1.0):
    """Sigma_b fixed at sb: stars = sb - gas_col. Gas = McMillan's radial forms x gas_col / McMillan's column."""
    gs = gas_col / GAS_MCM; ns["ZD_THIN"], ns["ZD_THICK"] = ZT0 * zs, ZK0 * zs
    base, p = F.rho(sb - (gs - 1) * GAS_MCM, mbb, rd); ns["ZD_THIN"], ns["ZD_THICK"] = ZT0, ZK0
    rhof = (lambda R, z: base(R, z) + (gs - 1) * gas_rho(R, z)) if gs != 1 else base
    bar = newton(rhof); Mana = p["M_thin"] + p["M_thick"] + p["M_bb"] + gs * MGAS_MCM
    return dict(sig_b=sb, M_bb=mbb, R_d=rd, Mstar=p["Mstar"], tag_Rd_IN=bool(L.RD_TAG[0] <= rd <= L.RD_TAG[1]),
                tag_Mstar_IN=bool(L.MSTAR_TAG[0] <= p["Mstar"] <= L.MSTAR_TAG[1]), bar=bar, mass_rel=bar["Mb"] / Mana - 1)

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
    return dict(S=Sig / 1e6, lgM200=lM, r0=r0, sat=sat, vc_R0=vc, K_R0=K0, chi2_Kz=cK, chi2_Ou=cO, L1=bool(l1), L2a=bool(cK <= LINE_KZ),
                L2b=bool(abs(K0 - KZ_BR) <= 2 * KZ_BR_E), L3=bool(cO <= LINE_OU), D=D, dvc=vc - bar["vc_R0"], dK=K0 - bar["K_R0"])
L4 = ("L1", "L2a", "L2b", "L3")
def classify(cs, rows):
    allp = [i for i, r in enumerate(rows) if all(r[l] for l in L4)]; vk = [i for i, r in enumerate(rows) if r["L1"] and r["L2a"] and r["L2b"]]
    intag = [i for i, c in enumerate(cs) if c["tag_Rd_IN"] and c["tag_Mstar_IN"]]
    cls = ("FEASIBLE IN PRIORS" if any(i in intag for i in allp) else "FEASIBLE (WIDE PRIORS ONLY)" if allp else "V+K ONLY" if vk else "INFEASIBLE")
    d = lambda i: dict(sig_b=cs[i]["sig_b"], M_bb=cs[i]["M_bb"], R_d=cs[i]["R_d"], Mstar=cs[i]["Mstar"], **{k: rows[i][k] for k in ("vc_R0", "K_R0", "chi2_Kz", "chi2_Ou", "D", "lgM200", "S", "r0")})
    ib = int(np.argmin([r["D"] for r in rows])); ip = min(intag, key=lambda i: rows[i]["D"]) if intag else None
    return dict(cls=cls, n_cells=len(cs), n_all=len(allp), frac_box=len(allp) / len(cs), n_in_tags=len(intag), n_all_in_tags=sum(i in intag for i in allp),
                frac_in_tags=(sum(i in intag for i in allp) / len(intag)) if intag else None, n_VK=len(vk), counts={l: sum(r[l] for r in rows) for l in L4},
                passing=[dict(sig_b=cs[i]["sig_b"], M_bb=cs[i]["M_bb"], R_d=cs[i]["R_d"]) for i in allp], best=d(ib), best_in_tags=d(ip) if ip is not None else None)
def grade_box(cs, tags=(TA, TB)):
    return {f"{n}|{t}": classify(cs, [grade(c["bar"], k, f, v, t) for c in cs]) for n, k, f, v in RULES for t in tags}

checks = {}
RES = dict(criteria="9468ee04b2", mutate=MUT, halo_free_bulge=HALO_FREE_BULGE, bulge_candidates=BULGE_CANDIDATES, gas_mcm=GAS_MCM, eilers=[vE, eE])
m0 = newton(ns["rho_mcm"]); checks["K0"] = abs(m0["vc_R0"] / 177.234 - 1) < 0.01 and abs(m0["K_R0"] / 62.024 - 1) < 0.01
P(f"K0 McMillan Newtonian: V_b(R0) {m0['vc_R0']:.3f}, K_z,b {m0['K_R0']:.3f}, M_b {m0['Mb']:.4e}: {'PASS' if checks['K0'] else 'FAIL'}")
GRID = list(itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID))
# K1: McMillan's gas on X5's family reproduces GD2
csK = [cell(s, m, r, gas_col=GAS_MCM) for s, m, r in GRID]; GD2 = json.load(open(os.path.join(REB, "GD2_route_e_mw_x5_box", "gd2_x5_box_results.json")))["classes"]
k1 = True
for f in ("canonical", "alt"):
    c = classify(csK, [grade(q["bar"], "os1", f, 172.98, TA) for q in csK]); g2 = GD2[f"{f}|PRIMARY|{TA}"]
    ok = c["cls"] == g2["cls"] and c["n_all"] == g2["counts"]["all"] and abs(c["best"]["D"] - g2["best"]["D"]) < 1e-9; k1 = k1 and ok
    P(f"K1 [{f}] X5 family + McMillan gas: {c['cls']}, n_all {c['n_all']}, best D {c['best']['D']:.6f} (GD2 {g2['cls']}, {g2['counts']['all']}, {g2['best']['D']:.6f}): {'PASS' if ok else 'FAIL'}")
checks["K1"] = k1
RES["mcmgas_box"] = grade_box(csK)
# K2, K3
r2 = lambda f, v: (v / math.sqrt(2) / SREF) ** QF[f]
checks["K2"] = all(abs(r2(f, v) - x) < 1e-3 for f, v, x in (("canonical", 172.98, 1.635), ("alt", 172.98, 1.510), ("canonical", 229.05, 2.100), ("alt", 229.05, 1.863)))
ref = {1e10: 51.8, 1e11: 78.4, 1e12: 149.0, 1e13: 236.0, 1e14: 380.0}; dev = {k: S_nat(k * FC, TA) / v - 1 for k, v in ref.items()}; s9 = S_nat(1e9, TA)
checks["K3"] = max(abs(v) for v in dev.values()) < 0.01 and abs(s9 / 29.4 - 1) < 0.01
P(f"K2 OS1 factors: {'PASS' if checks['K2'] else 'FAIL'}; K3 native table at M_t 1e10..1e14: {[round(S_nat(k * FC, TA), 1) for k in ref]}, lg M200 9: {s9:.1f}: {'PASS' if checks['K3'] else 'FAIL'}")

# ------------------------------------------------------------------ BRACKET: McKee gas, Portail M_bb (labelled, never graded)
cs = [cell(s, m, r) for s, m, r in GRID]
checks["K5"] = all(abs(c["mass_rel"]) < 2e-3 for c in cs) and all(abs(c["mass_rel"]) < 2e-3 for c in csK)
BR = grade_box(cs); RES["bracket"] = BR
k4 = True
for n, k, f, v in RULES:
    for t in BGS:
        k4 = k4 and all((lambda r: r["dvc"] > 0 and r["dK"] > 0)(grade(c["bar"], k, f, v, t)) for c in cs)
checks["K4"] = k4
checks["K6"] = all(json.dumps(BR[f"N|canonical|{t}"], sort_keys=True) == json.dumps(BR[f"N|alt|{t}"], sort_keys=True) for t in BGS)
P(f"\n=== BRACKET (M_bb = Portail+17: LCDM-PROCESSED, PROVISIONAL; never graded). McKee gas 13.7. 175 cells.")
for k, c in BR.items():
    b, ip = c["best"], c["best_in_tags"]
    P(f"[{k}] BRACKET class {c['cls']}; all-4 {c['n_all']}/175 = {c['frac_box']:.3f}; in both LN tags {c['n_all_in_tags']}/{c['n_in_tags']}; lines {c['counts']}")
    P(f"     best D {b['D']:.2f}: Sig_b {b['sig_b']}, M_bb {b['M_bb']:.3g}, R_d {b['R_d']:.3f}: vc {b['vc_R0']:.1f}, Kz {b['K_R0']:.1f}, chi2_Kz {b['chi2_Kz']:.1f}, chi2_Ou {b['chi2_Ou']:.1f}, S {b['S']:.1f}, lgM200 {b['lgM200']:.2f}")
    if ip: P(f"     best in tags D {ip['D']:.2f}: Sig_b {ip['sig_b']}, M_bb {ip['M_bb']:.3g}, R_d {ip['R_d']:.3f}: vc {ip['vc_R0']:.1f} (z {(ip['vc_R0'] - vE) / eE:+.1f}), Kz {ip['K_R0']:.1f}, chi2_Ou {ip['chi2_Ou']:.0f}")

# ------------------------------------------------------------------ LOOKUP (DIAGNOSTIC, not a prior)
MLK = [0.5e10, 0.8e10, 1.0e10, 1.3e10, 1.64e10, 1.88e10, 2.12e10, 2.5e10, 3.0e10]
LK = {}; bars = {(s, m, r): cell(s, m, r) for m in MLK for s in L.SIG_B_GRID for r in L.RD_GRID}
P("\n=== LOOKUP (DIAGNOSTIC, not a prior): number of the 5 Sigma_b passing all four lines; bg A; then best-Sigma_b v_c")
RD = L.RD_GRID
for n, k, f, v in RULES:
    if n == "N|alt": continue
    tab = {}
    P(f"[{n}]  R_d: " + " ".join(f"{r:5.2f}" for r in RD))
    for m in MLK:
        row = []; vcs = []
        for r in RD:
            gs = [grade(bars[(s, m, r)]["bar"], k, f, v, TA) for s in L.SIG_B_GRID]
            row.append(sum(all(g[l] for l in L4) for g in gs)); vcs.append(max(g["vc_R0"] for g in gs))
        tab[f"{m:.3g}"] = dict(n_pass=row, vc_max=vcs)
        P(f"   M_bb {m / 1e10:4.2f}e10: " + " ".join(f"{x:5d}" for x in row) + "   | vc_max " + " ".join(f"{x:5.1f}" for x in vcs))
    LK[n] = tab
RES["lookup"] = dict(R_d=RD, M_bb=MLK, rows=LK)

# ------------------------------------------------------------------ sensitivity on the bracket box
P("\n=== SENSITIVITY (bracket box; bg A)")
SENS = {}
for lab, kw in (("gas 10.5 (McKee -2 sigma)", dict(gas_col=10.5)), ("gas 16.9 (McKee +2 sigma)", dict(gas_col=16.9)), ("z_d x 0.8", dict(zs=0.8)), ("z_d x 1.2", dict(zs=1.2))):
    q = [cell(s, m, r, **kw) for s, m, r in GRID]; SENS[lab] = {}
    for n, k, f, v in RULES:
        if n == "N|alt" or n.endswith("VARIANT"): continue
        c = classify(q, [grade(z["bar"], k, f, v, TA) for z in q]); SENS[lab][n] = dict(cls=c["cls"], n_all=c["n_all"], in_tags=c["n_all_in_tags"], best_in_tags_vc=c["best_in_tags"]["vc_R0"], best_in_tags_D=c["best_in_tags"]["D"])
        P(f"  {lab:26s} [{n}] {c['cls']}; all-4 {c['n_all']}; in tags {c['n_all_in_tags']}; best in tags vc {c['best_in_tags']['vc_R0']:.1f}, D {c['best_in_tags']['D']:.2f}")
RES["sensitivity"] = SENS
P("  McMillan's gas column (K1 box):")
for n, k, f, v in RULES:
    if n == "N|alt" or n.endswith("VARIANT"): continue
    c = RES["mcmgas_box"][f"{n}|{TA}"]; P(f"  [{n}] {c['cls']}; all-4 {c['n_all']}; in tags {c['n_all_in_tags']}")

# ------------------------------------------------------------------ McMillan row, labelled
P("\n=== McMillan 2017 baryons (LCDM-PROCESSED, reported), bg A")
RES["mcmillan"] = {}
for n, k, f, v in RULES:
    r = grade(m0, k, f, v, TA); RES["mcmillan"][n] = r
    P(f"  [{n}] vc {r['vc_R0']:.1f} (z {(r['vc_R0'] - vE) / eE:+.1f}), Kz {r['K_R0']:.1f}, chi2_Kz {r['chi2_Kz']:.1f}, chi2_Ou {r['chi2_Ou']:.0f}, S {r['S']:.1f}, lgM200 {r['lgM200']:.2f}")

# ------------------------------------------------------------------ short disc against the priors
P("\n=== GD2's short disc against the priors (passing cells on the bracket box, PRIMARY or N; bg A)")
SD = {}
for key in (f"OS1|canonical|PRIMARY|{TA}", f"OS1|alt|PRIMARY|{TA}", f"N|canonical|{TA}"):
    ps = BR[key]["passing"]; rds = sorted({p["R_d"] for p in ps}); SD[key] = dict(R_d=rds)
    rows = [dict(R_d=r, z_BHG=(r - 2.6) / 0.5, in_BHG_2s=bool(abs(r - 2.6) <= 1.0 + 1e-9), z_LN16=(r - 2.64) / 0.13, in_LN16_2s=bool(L.RD_TAG[0] <= r <= L.RD_TAG[1])) for r in rds]
    SD[key]["rows"] = rows; P(f"  [{key}] R_d {[round(x, 3) for x in rds]}: " + "; ".join(f"{x['R_d']:.2f}: BH&G {x['z_BHG']:+.1f} sigma, LN16 {x['z_LN16']:+.1f} sigma" for x in rows))
RES["short_disc"] = SD

# ------------------------------------------------------------------ external field: tide only, reported
def lg200(Mb): return BGS[TA]["a"] + BGS[TA]["b"] * (math.log10(Mb) - 10)
EXT = {}
for nm, Mb, d in (("M31", 1.3e11, 770.0), ("LMC", 3e9, 49.9)):
    M = 10 ** lg200(Mb); gu = G * Mb / d ** 2
    dv2 = R0 * 2 * G * M * R0 / d ** 3; EXT[nm] = dict(Mb=Mb, d=d, lgM200=math.log10(M), g_uniform_baryon_kms2_kpc=gu, dV_at_229=229.05 * (math.sqrt(1 + dv2 / 229.05 ** 2) - 1), dV_baryon_only=229.05 * (math.sqrt(1 + (R0 * 2 * G * Mb * R0 / d ** 3) / 229.05 ** 2) - 1))
    P(f"tide [{nm}] lgM200 {math.log10(M):.2f}: largest |dV_c(R0)| {EXT[nm]['dV_at_229']:.3f} km/s using M200 at {d} kpc; {EXT[nm]['dV_baryon_only']:.4f} on baryons only")
RES["external"] = EXT

# ------------------------------------------------------------------ verdict
usable = [r for r in HALO_FREE_BULGE if r.get("read_from_disk")]
if not usable:
    VERD = {n: "UNDETERMINED: no halo-free bulge mass on disk" for n in ("OS1|canonical", "OS1|alt", "N")}
else:
    raise SystemExit("a usable halo-free row needs its grade wired in per FROZEN_CRITERIA section Verdict")
RES["verdict"] = VERD; checks["K7"] = rss() < 1.0; RES["checks"] = {k: bool(v) for k, v in checks.items()}
P(f"\n=== VERDICT: {VERD}")
P("candidates: " + "; ".join(f"{k}: {v}" for k, v in BULGE_CANDIDATES.items()))
P("checks " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in sorted(checks.items())))
fn = os.path.join(HERE, f"rf1_mw_results{TAG}.json")
def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items() if k != "bar"}
    if isinstance(o, (list, tuple)): return [clean(x) for x in o]
    return o
s = json.dumps(clean(RES), indent=1, default=float, sort_keys=True); open(fn, "w").write(s)
P(f"results sha256 {hashlib.sha256(s.encode()).hexdigest()}; peak RSS {rss():.2f} GB")
P("kappa = 1/2 FITTED; footings never pooled; not theory closed; nothing here says the data favour the framework.")
open(os.path.join(HERE, f"rf1_mw{TAG}.out"), "w").write("\n".join(OUT) + "\n")
print(f"runtime {time.time() - T0:.0f} s")
sys.exit(0 if all(checks.values()) else 1)
