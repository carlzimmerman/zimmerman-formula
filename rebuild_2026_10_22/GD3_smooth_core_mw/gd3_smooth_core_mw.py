#!/usr/bin/env python3
"""GD3_smooth_core_mw: the flagship's Milky Way with the smooth core rho0/(1+x^2)^(3/2) and q re-calibrated on SPARC.

Criteria FROZEN_CRITERIA.md (d5dafa534e, committed alone).
Stage S: OS1's SPARC calibration (SC1 -> X38 -> X30 machinery exec'd read-only, as OS1 does), halo B(x) swapped.
Stage M: GD2's X5-box Milky Way grade (x5_lib + P4 Newtonian, read-only), halo B(x) swapped, q = q_fS.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gd3_smooth_core_mw.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gd3_smooth_core_mw.py --mutate   -> q = 0 (K5 must fail)
kappa = 1/2 FITTED; footings never pooled; cold dark energy, not matter; not theory closed.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, io, json, math, time, itertools, contextlib, resource
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

T0 = time.time()
MUTATE = "--mutate" in sys.argv
TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

def B_burkert(x):
    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def B_smooth(x):                                                   # M(<r) = pi Sigma r0^2 B_S(r/r0), Sigma = rho0 r0
    x = np.asarray(x, float); return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
SHAPES = {"burkert": B_burkert, "smooth": B_smooth}
FEET = ("canonical", "alt")
QF_OS1 = {"canonical": 0.892, "alt": 0.748}
checks = []
P(f"GD3_smooth_core_mw {'MUTATE (q = 0)' if MUTATE else 'normal run'}  (frozen d5dafa534e)")
P("route E: Newtonian + OS1 core law with the smooth core; kappa = 1/2 FITTED; footings never pooled; not theory closed")

# ---- K1: smooth mass function vs quadrature
k1 = all(abs(float(B_smooth(x)) / (4 * quad(lambda t: t * t * (1 + t * t) ** -1.5, 0, x, epsabs=0, epsrel=1e-13)[0]) - 1) < 1e-10
         for x in (0.3, 1.0, 3.0, 10.0)) and abs(float(B_smooth(1.0)) - 0.69707) < 1e-5
P(f"K1 B_S vs quadrature, B_S(1) = {float(B_smooth(1.0)):.5f}: {'PASS' if k1 else 'FAIL'}"); checks.append(("K1", k1))

# ================================================================== stage S (OS1's machinery, read-only)
RES = dict(frozen="d5dafa534e", mutate=MUTATE, stageS={}, stageM={})
SC1SRC = os.path.join(REB, "SC1_self_coupled_core_law", "sc1_core_law.py"); TS = open(SC1SRC).read()
code = TS[:TS.index('checks = [("K1", k1)]')]
code = code.replace('os.path.join(HERE, "sc1_x30_machinery.log")', repr(os.path.join(HERE, "gd3_x30_machinery.log")))
NS = {"__file__": SC1SRC, "__name__": "sc1_ro"}; argv0 = sys.argv; sys.argv = [SC1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code, SC1SRC, "exec"), NS)
sys.argv = argv0
sparc, BGS_S, line = NS["sparc"], NS["BGS"], NS["line"]
def set_shape(name):                                               # SC1's sparc uses its own B; solve_r0 uses X38's
    NS["B"] = SHAPES[name]; NS["NS"]["B"] = SHAPES[name]
OS1J = json.load(open(os.path.join(REB, "OS1_core_law_out_of_sample", "os1_out_of_sample_results.json")))
P(f"stage S machinery loaded [{time.time() - T0:.0f} s]; sigma_ref {NS['SREF']:.2f} km/s")

def calibrate(foot):
    bg = BGS_S["A_c2b_refit"]; cache = {}
    def rms(q):
        if q not in cache: cache[q] = sparc(foot, bg["a"], bg["b"], bg["h"], q)
        return cache[q]["rms"]
    coarse = [round(0.02 * i, 3) for i in range(61)]; qc = min(coarse, key=rms)
    fine = sorted({round(qc + 0.002 * j, 4) for j in range(-10, 11) if 0 <= qc + 0.002 * j <= 1.2}); qf = min(fine, key=rms)
    return qf, cache[qf], cache[0.0]

QS = {}; GATE = {}
for foot in FEET:
    set_shape("burkert"); qb, sb, _ = calibrate(foot)
    k0 = abs(qb - OS1J["footings"][foot]["q_f"]) < 1e-9 and abs(sb["rms"] - OS1J["footings"][foot]["sparc_A"]["rms"]) < 1e-9
    P(f"K0[{foot}] Burkert recalibration q_f {qb:.3f} rms {sb['rms']:.6f} (OS1 {OS1J['footings'][foot]['q_f']:.3f} / "
      f"{OS1J['footings'][foot]['sparc_A']['rms']:.6f}): {'PASS' if k0 else 'FAIL'}"); checks.append((f"K0[{foot}]", k0))
    set_shape("smooth"); qs, ss, s0 = calibrate(foot)
    bgB = BGS_S["B_cfg886_bg"]; sB = sparc(foot, bgB["a"], bgB["b"], bgB["h"], qs)
    GATE[foot] = bool(line(ss)); QS[foot] = qs
    P(f"[{foot}] smooth calibration: q_fS = {qs:.3f}; SPARC A rms {ss['rms']:.4f} @ U {ss['U_median']:.2f} (q=0: "
      f"{s0['rms']:.4f} @ U {s0['U_median']:.2f}); line {'PASS' if GATE[foot] else 'FAIL'}; bg B (reported) rms "
      f"{sB['rms']:.4f} @ U {sB['U_median']:.2f}   [{time.time() - T0:.0f} s]")
    RES["stageS"][foot] = dict(q_fS=qs, rms=ss["rms"], U=ss["U_median"], line=GATE[foot], q0_rms=s0["rms"], q0_U=s0["U_median"],
                               bgB=dict(rms=sB["rms"], U=sB["U_median"]))

# ================================================================== stage M (GD2's grade, read-only machinery)
sys.path.insert(0, os.path.join(REB, "X5_mw_joint_baryons"))
import x5_lib as L  # noqa: E402
G = 4.30091e-6; KZU = 2 * math.pi * G * 1e6
SIG_A0 = {"canonical": 106.879e6, "alt": 129.165e6}; SREF = 70.50
VLAST = {"PRIMARY": 172.98, "VARIANT": 229.05}
EM1 = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
BGS = {t: dict(a=EM1["rows"][t]["R1"]["a"], b=EM1["rows"][t]["R1"]["b"], h=F3[t]["params"]["h"]) for t in ("A_c2b_refit", "B_cfg886_bg")}
KZ_BR, KZ_BR_E = 66.4, 2.2
LINE_KZ, LINE_OU = L.LINE_CHI2, 59.89250004508689

def solve_r0(Mtot, Rout, Sig, Bf):                                 # X38 A1 compact root
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(Bf(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    if lm(pk.x) < math.log(Mtot):
        return math.exp(pk.x), True
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), pk.x, xtol=1e-14)), False

ns = L.load_p4(); F = L.Family(ns); PS = ns["S"]
vE, eE = L.eilers_target(ns)
R0 = ns["R0_MW"]; BR_R = ns["BR_R"]; BR_K = ns["BR_K"]; BR_E5 = ns["BR_E5"]
ou = np.loadtxt(os.path.join(L.DATA, "mw_rc_ou2024_table1.tsv"), comments="#", skiprows=14)
OR, OV = ou[:, 0], ou[:, 1]; OE = np.hypot(0.5 * (ou[:, 2] + ou[:, 3]), np.where(OR <= 22.0, 0.03, 0.15) * OV)
A0C = L.A0_SI["canonical"]

def newton(rhof):
    Mu = PS.mass_unit(A0C); g = ns["mw_grid"](6.6e10 / Mu)
    rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); Mt = 2 * float(np.sum(rho1 * g.vol))
    pr = PS.Problem(g, rho1, Mt, 0.0, Lam=0.0); Phi = pr.solve_newton()
    o = ns["mw_obs"](g, Phi, A0C)
    return dict(Mb=Mt * Mu, K=np.array(o["K"]), K_R0=o["K_R0"], vc_R0=o["vc_R0"], vou=L.vc_plane(ns, g, Phi, A0C, OR))

def grade(bar, foot, vlast, bg, q, Bf):
    Sig = SIG_A0[foot] * (vlast / math.sqrt(2) / SREF) ** q
    lM = bg["a"] + bg["b"] * (math.log10(bar["Mb"]) - 10); M200 = 10 ** lM
    rc = 3 * (100 * bg["h"] / 1e3) ** 2 / (8 * math.pi * G); R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
    r0, sat = solve_r0(M200, R200, Sig, Bf)
    gh = lambda r: G * math.pi * Sig * r0 ** 2 * Bf(np.asarray(r, float) / r0) / np.asarray(r, float) ** 2
    rk = np.hypot(BR_R, 1.1); K = bar["K"] + gh(rk) * 1.1 / rk / KZU
    r00 = math.hypot(R0, 1.1); K0 = bar["K_R0"] + float(gh(r00)) * 1.1 / r00 / KZU
    vc = math.sqrt(bar["vc_R0"] ** 2 + R0 * float(gh(R0))); vo = np.sqrt(bar["vou"] ** 2 + OR * gh(OR))
    cK = float(np.sum(((K - BR_K) / BR_E5) ** 2)); cO = float(np.sum(((vo - OV) / OE) ** 2))
    l1 = abs(vc - L.VC_BRIEF) <= L.VC_BRIEF_LINE and abs(vc - vE) <= 2 * eE
    D = max(cK / LINE_KZ, abs(vc - vE) / (2 * eE), cO / LINE_OU, abs(K0 - KZ_BR) / (2 * KZ_BR_E))
    return dict(Sig_ratio=Sig / SIG_A0[foot], lgM200=lM, r0=r0, sat=sat, vc_R0=vc, K_R0=K0, chi2_Kz=cK, chi2_Ou=cO,
                L1=bool(l1), L2a=bool(cK <= LINE_KZ), L2b=bool(abs(K0 - KZ_BR) <= 2 * KZ_BR_E), L3=bool(cO <= LINE_OU), D=D,
                dvc=vc - bar["vc_R0"], dK=K0 - bar["K_R0"])

CELLS = []; Mgas = F.gas_mass()
for sb, mbb, rd in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID):
    rhof, p = F.rho(sb, mbb, rd); bar = newton(rhof)
    CELLS.append(dict(sig_b=sb, M_bb=mbb, R_d=rd, Mstar=p["Mstar"], tag_Rd_IN=bool(L.RD_TAG[0] <= rd <= L.RD_TAG[1]),
                      tag_Mstar_IN=bool(L.MSTAR_TAG[0] <= p["Mstar"] <= L.MSTAR_TAG[1]), bar=bar))
MCM = newton(ns["rho_mcm"])
P(f"stage M: {len(CELLS)} X5 cells solved; McMillan V_b(R0) {MCM['vc_R0']:.3f}, K_z,b {MCM['K_R0']:.3f}   [{time.time() - T0:.0f} s]")

def classify(rows):
    allp = [i for i, r in enumerate(rows) if all(r[l] for l in ("L1", "L2a", "L2b", "L3"))]
    vk = [i for i, r in enumerate(rows) if all(r[l] for l in ("L1", "L2a", "L2b"))]
    if any(CELLS[i]["tag_Rd_IN"] and CELLS[i]["tag_Mstar_IN"] for i in allp): cls = "FEASIBLE IN PRIORS"
    elif allp: cls = "FEASIBLE (WIDE PRIORS ONLY)"
    elif vk: cls = "V+K ONLY"
    else: cls = "INFEASIBLE"
    ib = int(np.argmin([r["D"] for r in rows]))
    inpri = [i for i in range(len(rows)) if CELLS[i]["tag_Rd_IN"] and CELLS[i]["tag_Mstar_IN"]]
    ip = min(inpri, key=lambda i: rows[i]["D"]) if inpri else None
    cdesc = lambda i: dict(sig_b=CELLS[i]["sig_b"], M_bb=CELLS[i]["M_bb"], R_d=CELLS[i]["R_d"], Mstar=CELLS[i]["Mstar"],
                           **{k: rows[i][k] for k in ("vc_R0", "K_R0", "chi2_Kz", "chi2_Ou", "D", "L1", "L2a", "L2b", "L3")})
    return dict(cls=cls, n_all=len(allp), n_VK=len(vk), passing_Rd=sorted({CELLS[i]["R_d"] for i in allp}),
                best=cdesc(ib), best_in_prior=cdesc(ip) if ip is not None else None)

def run_box(shape, qd, label):
    out = {}; k3 = True
    for foot in FEET:
        for vk, vl in VLAST.items():
            for t, bg in BGS.items():
                rows = [grade(c["bar"], foot, vl, bg, qd[foot], SHAPES[shape]) for c in CELLS]
                k3 = k3 and all(r["dvc"] > 0 and r["dK"] > 0 for r in rows)
                out[f"{foot}|{vk}|{t}"] = dict(classify(rows), Sig_ratio=rows[0]["Sig_ratio"])
    return out, k3

# K2: Burkert + OS1 q_f reproduces GD2
GD2J = json.load(open(os.path.join(REB, "GD2_route_e_mw_x5_box", "gd2_x5_box_results.json")))
bk, _ = run_box("burkert", QF_OS1, "K2")
k2 = all(bk[k]["cls"] == GD2J["classes"][k]["cls"] and abs(bk[k]["best"]["D"] - GD2J["classes"][k]["best"]["D"]) < 1e-9
         for k in (f"{f}|{v}|A_c2b_refit" for f in FEET for v in VLAST))
P(f"K2 Burkert + OS1 q_f reproduces GD2 classes and best D (4 graded keys): {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))

QM = {f: 0.0 for f in FEET} if MUTATE else QS
main, k3 = run_box("smooth", QM, "main"); checks.append(("K3_halo_raises", k3))
rep_bq, _ = run_box("smooth", QF_OS1, "reported")
RES["stageM"] = dict(q_used=QM, graded=main, reported_smooth_at_burkert_q=rep_bq)
P(f"\n=== stage M: smooth core at q = {QM['canonical']:.3f} / {QM['alt']:.3f}")
for k, c in main.items():
    b = c["best"]; ip = c["best_in_prior"]
    P(f"[{k}] {'GRADED' if k.endswith('A_c2b_refit') else 'reported'}: CLASS {c['cls']}; Sig/Sig_a0 {c['Sig_ratio']:.3f}; "
      f"cells all-4 {c['n_all']} (R_d {c['passing_Rd']}), V+K {c['n_VK']}")
    P(f"     best D {b['D']:.2f} at Sig_b {b['sig_b']}, M_bb {b['M_bb']:.3g}, R_d {b['R_d']:.3f}: vc {b['vc_R0']:.1f}, Kz {b['K_R0']:.1f}, "
      f"chi2_Kz {b['chi2_Kz']:.1f}, chi2_Ou {b['chi2_Ou']:.0f}")
    if ip: P(f"     best in-prior D {ip['D']:.2f} at R_d {ip['R_d']:.3f}, M* {ip['Mstar']:.3g}: vc {ip['vc_R0']:.1f}, Kz {ip['K_R0']:.1f}, "
             f"chi2_Kz {ip['chi2_Kz']:.1f}, chi2_Ou {ip['chi2_Ou']:.0f}")
P("\n(reported) smooth core at OS1's Burkert q_f, bg A:")
for k, c in rep_bq.items():
    if k.endswith("A_c2b_refit"):
        P(f"  [{k}] {c['cls']}; best D {c['best']['D']:.2f} (R_d {c['best']['R_d']:.3f}); best in-prior D {c['best_in_prior']['D']:.2f}")
P("\n(reported) McMillan 2017 baryons, smooth core, bg A:")
RES["stageM"]["mcmillan"] = {}
for foot in FEET:
    for vk, vl in VLAST.items():
        r = grade(MCM, foot, vl, BGS["A_c2b_refit"], QM[foot], B_smooth); RES["stageM"]["mcmillan"][f"{foot}|{vk}"] = r
        P(f"  [{foot}|{vk}] vc {r['vc_R0']:.1f} (Eilers {vE:.1f} +- {eE:.1f}), Kz {r['K_R0']:.1f}, chi2_Kz {r['chi2_Kz']:.1f}, chi2_Ou {r['chi2_Ou']:.0f}")

# ---- classes and verdict
CLS = {}
for foot in FEET:
    c = main[f"{foot}|PRIMARY|A_c2b_refit"]["cls"]
    CLS[foot] = c if GATE[foot] else f"SPARC LINE FAILS (MW reported: {c})"
RES["classes"] = CLS
RES["verdict"] = CLS["canonical"] if CLS["canonical"] == CLS["alt"] else f"UNDECIDED (footings disagree: {CLS})"
P(f"\nVARIANT (V_last 229, reported beside): canonical {main['canonical|VARIANT|A_c2b_refit']['cls']}; alt {main['alt|VARIANT|A_c2b_refit']['cls']}")
P(f"=== VERDICT (PRIMARY, bg A): {RES['verdict']}")
k5 = main["canonical|VARIANT|A_c2b_refit"]["Sig_ratio"] > 1 and main["alt|VARIANT|A_c2b_refit"]["Sig_ratio"] > 1
checks += [("K4_rss", rss() < 1.0), ("K5_sigma_factor", k5)]
n = sum(v for _, v in checks)
P(f"\nchecks {n}/{len(checks)}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks)
  + f"; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
P("kappa = 1/2 FITTED; not theory closed.")
RES["checks"] = {k: bool(v) for k, v in checks}
for c in CELLS: c.pop("bar")
open(os.path.join(HERE, f"gd3_smooth_core_mw{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"gd3_smooth_core_mw_results{TAG}.json"), "w"), indent=1, default=float)
if MUTATE: sys.exit(1 if n == len(checks) else 0)
sys.exit(0 if n == len(checks) else 1)
