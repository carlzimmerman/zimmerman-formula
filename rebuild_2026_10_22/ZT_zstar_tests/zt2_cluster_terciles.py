#!/usr/bin/env python3
"""ZT_zstar_tests / Z-T2: the capacity-truncated law of design Z* (v3s-OC) on X2's eRASS1 x KiDS cluster terciles.

Frozen line: Z1_successor_design/TEST_PLAN.md section 2 (0d1959a4f5); implementation choices: FROZEN_CRITERIA.md section 3.
Model per cluster (X2's rescaled gas, M_b = 1.2 M_gas): the AQUAL law inside r_s, M_b(<r) + f_s M_b,own beyond; where
R_own < r_s the law stops at R_own and the free excess f_s M_b,own - M_ph(R_own) follows CFG930's native debris profile.
R_own at 200 rho_c(z) and at 18 pi^2 rho_m(z); r_s by capacity (M_ph(<r_s) = S) and by the closed form r_M sqrt(f_s(f_s+1)).
Data, statistics, systematics (e), terciles, projector, gas shapes and reduced shear are X2's, exec'd read-only from X2's and
F1's source text (as X2 did with F1).  Nothing is edited; nothing is downloaded.

Run:  OMP_NUM_THREADS=1 nice -n 15 python3 zt2_cluster_terciles.py [--mutate]
      --mutate: cross shear as the data, and the held dust added on top of the untruncated law; K0 and K3 must FAIL.
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import os, sys, json, math, time, hashlib, resource, csv
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import PchipInterpolator

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
LANES = os.path.join(REPO, "campaign_fresh_gravity")
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []
RES = {"lane": "ZT_zstar_tests", "test": "Z-T2", "plan": "Z1_successor_design/TEST_PLAN.md @ 0d1959a4f5", "mutate": MUT}
CHECKS = []


def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(name, ok, val, thr, what=""):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}  -- {what}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr), what=what)


def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)


def guard(tag):
    if rss() > 0.95:
        say(f"RSS GUARD {rss():.3f} GB at {tag} -> abort"); sys.exit(3)


say(f"Z-T2 cluster terciles under the capacity-truncated law (Z* v3s-OC) {'MUTATE' if MUT else 'normal run'}")
say("kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. Cold energy, no particle. Not 'theory closed'.")
say("Nothing here says the data favour the framework.\n")

# ============================================================== F1's functions (exactly as X2 exec'd them, from F1's source text)
F1SRC = os.path.join(REB, "F1_cluster_cores", "f1_cluster_cores.py"); TXT = open(F1SRC).read(); RES["f1_source_sha256"] = sha(F1SRC)
def cut(t, a, b): i = t.index(a); j = t.index(b, i); return t[i:j]
NS = {"np": np, "os": os, "sys": sys, "REPO": REPO, "_trap": np.trapz, "PchipInterpolator": PchipInterpolator}
exec(cut(TXT, "G = 6.674e-11", "# ---------------------------------------------------------------- sources"), NS)
exec(cut(TXT, "EDGES = np.logspace", "def gather("), NS)
exec(cut(TXT, "RG = np.logspace(-3", "# SIS self-test (K4)"), NS)
exec(cut(TXT, "def gas_mass(", "# ---------------------------------------------------------------- K5"), NS)
G, MSUN, MPC, KG_PC2, A0 = NS["G"], NS["MSUN"], NS["MPC"], NS["KG_PC2"], NS["A0"]
RG, RC = NS["RG"], NS["RC"]; RM = RG * MPC
FEET = ("canonical", "alt"); HK = ("h0672", "h0686"); HV = {"h0672": 0.672, "h0686": 0.686}; HI = {"h070": 0, "h0672": 1, "h0686": 2}
CELLS = [(f, h) for f in FEET for h in HK]
NS.update(math=math, json=json, csv=csv, brentq=brentq, cumulative_trapezoid=cumulative_trapezoid, MUT=False, RM=RM, FEET=FEET, HK=HK,
          HV=HV, HI=HI, CELLS=CELLS, LANES=LANES, RES=RES, sha=sha, say=say, MSUN=MSUN)

# ============================================================== data: X2's replay npz (lines copied from X2, MUTATE = cross shear)
X2DIR = os.path.join(REB, "X2_cluster_outskirts"); X2SRC = open(os.path.join(X2DIR, "x2_cluster_outskirts.py")).read()
RES["x2_source_sha256"] = sha(os.path.join(X2DIR, "x2_cluster_outskirts.py"))
NPZ = os.path.join(X2DIR, "x2_replay_percluster.npz"); RES["replay_npz_sha256"] = sha(NPZ); X = np.load(NPZ)
N = len(X["z"]); CL = [dict(name=str(X["name"][i]), ra=float(X["ra"][i]), dec=float(X["dec"][i]), z=float(X["z"][i]), Mgas500=float(X["Mgas500"][i]),
                         MgL=float(X["MgL"][i]), MgH=float(X["MgH"][i]), R500=float(X["R500"][i]), off_deg=float(X["off_deg"][i])) for i in range(N)]
order = np.argsort(X["ra"]); PATCH = np.empty(N, int); PATCH[order] = np.arange(N) * 30 // N
ALL = np.ones(N, bool)
_q = np.quantile(X["Mgas500"], [1 / 3, 2 / 3]); TID = np.digitize(X["Mgas500"], _q); TERC = {f"T{t + 1}": TID == t for t in range(3)}
RES["tercile_median_Mgas500"] = {k: float(np.median(X["Mgas500"][v])) for k, v in TERC.items()}
DAT = {}
for hk in HK:
    i = HI[hk]; Dt = X["D"][:, i]; Et = X["E"][:, i]; Dx = X["Dx"][:, i]; Ex = X["Ex"][:, i]
    if MUT: Dt, Et = Dx, Ex
    W = np.where(Et < 1e8, 1 / Et ** 2, 0); Wx = np.where(Ex < 1e8, 1 / Ex ** 2, 0)
    B = X["den"][:, i].sum(0) / X["den_r"][:, i].sum(0)
    DAT[hk] = dict(D=Dt, W=W, B=B, Dx=Dx, Wx=Wx, DRR=X["DRR"][:, i], m2=X["den"][:, i], m=X["m3to8"][:, i])
NS.update(X=X, N=N, CL=CL, PATCH=PATCH, ALL=ALL, TERC=TERC, DAT=DAT)
say(f"replay npz {RES['replay_npz_sha256'][:16]}..., clusters {N}; tercile Mgas500 medians "
    + " ".join(f"{k} {v:.2e}" for k, v in RES["tercile_median_Mgas500"].items()))

# ============================================================== X2's statistics, projector, gas, EFE table, debris, model (exec'd)
exec(cut(X2SRC, "PB = [3, 4, 5, 6, 7]", "# ============================================================== projector"), NS)
exec(cut(X2SRC, "def project_floor(", "# ============================================================== EFE"), NS)
sys.path.insert(0, os.path.join(REB, "F2_outer_lensing")); import f2_aqual as AQ  # noqa: E402  (read-only)
NS["AQ"] = AQ
exec(cut(X2SRC, "CH = list(csv.DictReader", "CTAB = {}"), NS)
NS["CTAB"] = {}
exec(cut(X2SRC, "def ctable(", "for f in FEET:"), NS)
exec(cut(X2SRC, "C949 = os.path.join", "# ============================================================== the model"), NS)
exec(cut(X2SRC, "def model(", "PRED = {}"), NS)
stats, gas, project_floor, offset_floor, sig_bins = (NS[k] for k in ("stats", "gas", "project_floor", "offset_floor", "sig_bins"))
model_x2, redfac, debris = NS["model"], NS["redfac"], NS["debris"]
DM, DA_lcdm, g_aqual_sph, dsig_from_sig, at_bins = (NS[k] for k in ("DM", "DA_lcdm", "g_aqual_sph", "dsig_from_sig", "at_bins"))
BANDS = NS["BANDS"]
t1 = time.time()
for f in FEET:
    NS["CTAB"][(f, "noclu")] = NS["ctable"](AQ.solve_efe(NS["YE"][f]["noclu"], maxit=3000))
say(f"  F2 EFE noclu tables (K0 reproduction of X2's C* only) [{time.time() - t1:.0f} s]")

# ============================================================== Z* constants (Z1's record inputs)
F_S = 5.364; OM = 0.2976


def rho_c(h, z):
    H0 = h * 1e5 / MPC                                      # s^-1 (MPC in m, as F1)
    return 3 * H0 ** 2 / (8 * math.pi * G) * (OM * (1 + z) ** 3 + 1 - OM)


def drho(h, z, conv):
    if conv == "200c":
        return 200 * rho_c(h, z)
    return 18 * math.pi ** 2 * OM * (3 * (h * 1e5 / MPC) ** 2 / (8 * math.pi * G)) * (1 + z) ** 3      # 18 pi^2 rho_m(z), EdS convention


def first_cross(r, y):
    """first r where y changes sign from + to - (linear interpolation); None if never."""
    s = np.where((y[:-1] > 0) & (y[1:] <= 0))[0]
    if not s.size:
        return None
    j = s[0]; return float(r[j] + (r[j + 1] - r[j]) * y[j] / (y[j] - y[j + 1]))


def r_supply(Mph, S, Mb_own, a0, rsdef):
    if rsdef == "lit":
        return math.sqrt(G * Mb_own / a0) * math.sqrt(F_S * (F_S + 1)) / MPC if S > 0 else float("inf")
    rr = first_cross(RG, S - Mph)
    return rr if rr is not None else float("inf")


DEB = {}


def zstar_mass(i, cl, foot, hk, gasshape, rconv, rsdef, fs=F_S, inactive=False):
    """returns (M_tot(<r) kg on RG, M_b, M_law, meta)."""
    h = HV[hk]; a0 = A0[foot]; z = cl["z"]; q = (float(DM(z, h)) / (1 + z)) / DA_lcdm(z)
    Mg500 = cl["Mgas500"] * q ** 2.5; R500 = cl["R500"] * q
    Mg, _ = gas(Mg500, R500, gasshape); Mb = Mg * 1.2
    gl = g_aqual_sph(G * Mb / RM ** 2, a0); Mlaw = gl * RM ** 2 / G; Mph = Mlaw - Mb
    Ro = first_cross(RG, (1 + fs) * Mb - 4 * math.pi / 3 * drho(h, z, rconv) * RM ** 3)
    Ro = Ro if Ro is not None else float("inf")
    Mb_own = float(np.interp(Ro, RG, Mb)) if math.isfinite(Ro) else float(Mb[-1])
    S = fs * Mb_own
    rs = r_supply(Mph, S, Mb_own, a0, rsdef)
    if inactive:                                            # K1 (A1): capacity and owner boundary both removed
        Ro, rs, S, Mb_own = float("inf"), float("inf"), float("inf"), float(Mb[-1])
    rich = Ro < rs
    meta = dict(R_own=Ro, r_s=rs, rich=bool(rich), Mb_own=Mb_own / MSUN, S=S / MSUN)
    if MUT:
        return Mb + Mph + S, Mb, Mlaw, meta                                        # MUTATE: held dust on top of the law
    if not rich:
        Mh = np.where(RG <= rs, Mph, S); Mf = 0.0
        meta["step_at_rs"] = float((S - np.interp(rs, RG, Mph)) / MSUN) if math.isfinite(rs) else 0.0
    else:
        MphR = float(np.interp(Ro, RG, Mph)); Mh = np.where(RG <= Ro, Mph, MphR); Ef = S - MphR
        key = (i, hk, gasshape)
        if key not in DEB:
            Mc, dm = debris(float(Mg[-1] / MSUN), Mg500, z); DEB[key] = (Mc / Mc[-1], dm)
        shape, dm = DEB[key]; Mf = Ef * shape
        meta.update(E_free=Ef / MSUN, deb_rb=float(dm["rb"]))
    return Mb + Mh + Mf, Mb, Mlaw, meta


def project(i, cl, foot, hk, Mtot, red):
    """X2 model()'s code path from M(<r) on: density, floored projection, miscentring, Delta Sigma at bins, reduced shear."""
    h = HV[hk]
    rho = np.gradient(Mtot, RM) / (4 * np.pi * RM ** 2)
    Sig = project_floor(rho); d = np.radians(cl["off_deg"]) * float(DM(cl["z"], h)) / (1 + cl["z"])
    So = offset_floor(Sig, d); P = at_bins(dsig_from_sig(So)) / KG_PC2; Sb = sig_bins(So)
    fac = np.ones(8); kap = np.zeros(8)
    if red:
        fac, kap = redfac(hk, i, Sb); P = P * fac
    return P, float(np.mean(rho < 0)), fac, kap


STK = {}


def stack_Z(foot, hk, gasshape, red, rconv, rsdef, fs=F_S, inactive=False):
    key = (foot, hk, gasshape, red, rconv, rsdef, fs, inactive)
    if key in STK: return STK[key]
    P = np.empty((N, 8)); META = []; negs = []; k3 = 0.0
    for i, cl in enumerate(CL):
        Mt, Mb, Ml, meta = zstar_mass(i, cl, foot, hk, gasshape, rconv, rsdef, fs, inactive)
        p, ng, _, _ = project(i, cl, foot, hk, Mt, red); P[i] = p; negs.append(ng)
        meta["design_over_law_1Mpc"] = float(np.interp(1.0, RG, Mt) / np.interp(1.0, RG, Ml))
        meta["design_over_law_2Mpc"] = float(np.interp(2.0, RG, Mt) / np.interp(2.0, RG, Ml))
        if math.isfinite(meta["S"]):
            k3 = max(k3, abs(Mt[-1] / (Mb[-1] + meta["S"] * MSUN) - 1))
        META.append(meta)
    STK[key] = (P, META, float(max(negs)), k3); guard("stack_Z"); return STK[key]


def stack_law(foot, hk, **kw):
    P = np.empty((N, 8)); FAC = np.ones((N, 8)); KAP = np.zeros((N, 8))
    red = kw.pop("red", False)
    for i, cl in enumerate(CL):
        p, sb, _, _ = model_x2(cl, foot, hk, **kw)
        if red: f_, k_ = redfac(hk, i, sb); p = p * f_; FAC[i] = f_; KAP[i] = k_
        P[i] = p
    return P, FAC, KAP


# ============================================================== K0: X2's terciles at C0 and C* (law) reproduced
X2J = json.load(open(os.path.join(X2DIR, "x2_cluster_outskirts_results.json")))
dev = 0.0; LAW = {}
for lab, kw, sx in (("C0", {}, False), ("C*", dict(gasshape="P", efe="noclu", red=True), True)):
    for f, hk in CELLS:
        P = stack_law(f, hk, **dict(kw))[0]; LAW[(lab, f, hk)] = P
        for t, sel in TERC.items():
            s = stats(hk, P, "boost", sel, sx); ref = X2J["terciles"][lab][t]["boost"][f"{f}|{hk}"]
            for b in ("INNER", "MID", "OUTER"):
                dev = max(dev, abs(s[b]["A"] - ref[b]["A"]), abs(s[b]["s_jk"] - ref[b]["s_jk"]), abs(s[b]["s_tot"] - ref[b]["s_tot"]))
    guard("K0")
check("K0", dev <= 1e-6, f"max |A, s_jk, s_tot - X2 terciles (C0, C*; boost; 4 cells)| {dev:.1e}", "<= 1e-6",
      "X2's tercile statistics reproduced (same data, same code path)")

# ============================================================== K1 (A1): truncation inactive gives the C*_own law; K4 reduced shear
# A1 (post-RUN1, check only): RUN1's K1 used f_s = 1e6, which also moves R_own (1 + f_s) inside 30 Mpc for light clusters and makes
# them supply-rich with a huge free excess -- the model as frozen, not the law limit.  K1 now removes the capacity and the owner
# boundary together (S = R_own = r_s = infinity) and compares per cluster on the scale max|Delta Sigma| (RUN1 kept: *_RUN1.out).
k1 = 0.0
for f, hk in [("canonical", "h0672"), ("alt", "h0686")]:
    Plaw, FAC, KAP = stack_law(f, hk, gasshape="P", red=True)
    Pz = stack_Z(f, hk, "P", True, "200c", "cap", inactive=True)[0]
    k1 = max(k1, float(np.max(np.abs(Pz - Plaw).max(1) / np.abs(Plaw).max(1))))
    if f == "canonical": FAC0, KAP0 = FAC, KAP
FAC, KAP = FAC0, KAP0
check("K1", k1 <= 1e-9 or MUT, f"max_i max|P_Z(inactive) - P_law| / max|P_law| {k1:.1e} (2 cells)", "<= 1e-9 (skipped under MUTATE)",
      "with capacity and owner boundary removed the Z* code path reproduces the C*_own law")
kmid = float(np.median(KAP[:, 3:6][DAT["h0672"]["m2"][:, 3:6] > 0]))
check("K4", float(FAC.min()) >= 1.0 and kmid < 0.1, f"min factor {FAC.min():.5f}; median kappa_MID {kmid:.4f}", ">= 1; < 0.1",
      "reduced shear perturbative and >= 1 (C*_own law)")

# ============================================================== K2: point-mass baryons: capacity r_s = closed form
k2 = 0.0
for f in FEET:
    for Mpt in (3e12, 1e13, 3e13, 1e14):
        Mb = np.full(RG.size, Mpt * MSUN); Mph = g_aqual_sph(G * Mb / RM ** 2, A0[f]) * RM ** 2 / G - Mb
        S = F_S * Mpt * MSUN
        rc_ = r_supply(Mph, S, Mpt * MSUN, A0[f], "cap"); rl_ = r_supply(Mph, S, Mpt * MSUN, A0[f], "lit")
        k2 = max(k2, abs(rc_ / rl_ - 1))
check("K2", k2 <= 1e-3, f"max |r_s(cap) / r_s(closed form) - 1| {k2:.1e} (point masses 3e12-1e14 Msun, both footings)", "<= 1e-3",
      "capacity definition equals the plan's closed form r_M sqrt(f_s(f_s+1)) for point-mass baryons (K5)")

# ============================================================== the Z* runs
BASE = {"C*_own": dict(gasshape="P", red=True), "C0+e": dict(gasshape="G0", red=False)}
RCONV = ("200c", "18pi2m"); RSDEF = ("cap", "lit")
RUNS = {}; K3 = 0.0; NEG = 0.0
say("\n=== Z* on the terciles (A = data / model; +- s_tot with systematics (e); boost convention) ===")
for bl, bkw in BASE.items():
    for rc in RCONV:
        for rd in RSDEF:
            for f, hk in CELLS:
                P, META, ng, k3 = stack_Z(f, hk, bkw["gasshape"], bkw["red"], rc, rd); K3 = max(K3, k3); NEG = max(NEG, ng)
                row = {}
                for t, sel in TERC.items():
                    s = stats(hk, P, "boost", sel, True); sc = stats(hk, P, "clip", sel, True)
                    m = [META[j] for j in np.where(sel)[0]]
                    row[t] = dict(MID=s["MID"], OUTER=s["OUTER"], INNER=s["INNER"], chi2=s["chi2"], Z_MID=s["Z_MID"], Z_OUT=s["Z_OUT"],
                                  pass_MID=abs(s["MID"]["A"] - 1) <= 2 * s["MID"]["s_tot"], pass_OUT=abs(s["OUTER"]["A"] - 1) <= 2 * s["OUTER"]["s_tot"],
                                  clip=dict(A_MID=sc["MID"]["A"], A_OUT=sc["OUTER"]["A"],
                                            pass_MID=abs(sc["MID"]["A"] - 1) <= 2 * sc["MID"]["s_tot"], pass_OUT=abs(sc["OUTER"]["A"] - 1) <= 2 * sc["OUTER"]["s_tot"]),
                                  med_R_own=float(np.median([x["R_own"] for x in m])), med_r_s=float(np.median([x["r_s"] for x in m])),
                                  frac_rich=float(np.mean([x["rich"] for x in m])), med_Mb_own=float(np.median([x["Mb_own"] for x in m])),
                                  med_dl_1Mpc=float(np.median([x["design_over_law_1Mpc"] for x in m])),
                                  med_dl_2Mpc=float(np.median([x["design_over_law_2Mpc"] for x in m])))
                tp = [row[t] for t in TERC]
                if all(x["pass_MID"] and x["pass_OUT"] for x in tp): cls = "PASS"
                elif all(x["pass_OUT"] for x in tp): cls = "PARTIAL"
                else: cls = "FAIL"
                row["class"] = cls; row["neg_rho_frac_max"] = ng
                RUNS[f"{bl}|{rc}|{rd}|{f}|{hk}"] = row
                say(f"{bl:6s} R_own {rc:6s} r_s {rd} {f[:3]} {hk}: " + "  ".join(
                    f"{t} MID {row[t]['MID']['A']:.2f}+-{row[t]['MID']['s_tot']:.2f}{'' if row[t]['pass_MID'] else '*'} "
                    f"OUT {row[t]['OUTER']['A']:.2f}+-{row[t]['OUTER']['s_tot']:.2f}{'' if row[t]['pass_OUT'] else '*'} "
                    f"[R {row[t]['med_R_own']:.2f} r_s {row[t]['med_r_s']:.2f} rich {row[t]['frac_rich']:.2f}]" for t in TERC) + f"  neg {ng:.3f}  -> {cls}")
            STK.clear(); guard("runs")
check("K3", K3 <= 1e-6, f"max |M(r_max) / (M_b(r_max) + S) - 1| {K3:.1e}", "<= 1e-6", "mass bookkeeping: total = baryons + supply")
RES["runs"] = RUNS; RES["neg_rho_frac_max"] = NEG
say(f"   (* = outside 2 s_tot; max fraction of floored negative-density cells over all runs {NEG:.3f})")

# law reference at C*_own (no EFE), per tercile
say("\n   reference: the untruncated law at C*_own (no EFE)")
LAWREF = {}
for f, hk in CELLS:
    P = stack_law(f, hk, gasshape="P", red=True)[0]
    LAWREF[f"{f}|{hk}"] = {t: {b: stats(hk, P, "boost", sel, True)[b] for b in ("MID", "OUTER")} for t, sel in TERC.items()}
    say(f"   law {f[:3]} {hk}: " + "  ".join(f"{t} MID {LAWREF[f'{f}|{hk}'][t]['MID']['A']:.2f}+-{LAWREF[f'{f}|{hk}'][t]['MID']['s_tot']:.2f} "
                                         f"OUT {LAWREF[f'{f}|{hk}'][t]['OUTER']['A']:.2f}+-{LAWREF[f'{f}|{hk}'][t]['OUTER']['s_tot']:.2f}" for t in TERC))
RES["law_reference_Cstar_own"] = LAWREF

# ============================================================== frozen class per footing and R_own convention
say("\n=== FROZEN CLASS (per footing, per R_own convention; stands only if both h cells and both r_s definitions agree) ===")
VERD = {}
for bl in BASE:
    for f in FEET:
        for rc in RCONV:
            cl_ = {f"{rd}|{hk}": RUNS[f"{bl}|{rc}|{rd}|{f}|{hk}"]["class"] for rd in RSDEF for hk in HK}
            u = set(cl_.values()); v = u.pop() if len(u) == 1 else "SPLIT " + json.dumps(cl_)
            VERD[f"{bl}|{f}|{rc}"] = v
            fails = sorted({f"{t}:{b}" for rd in RSDEF for hk in HK for t in TERC for b, k in (("MID", "pass_MID"), ("OUTER", "pass_OUT"))
                            if not RUNS[f"{bl}|{rc}|{rd}|{f}|{hk}"][t][k]})
            say(f"   {bl:6s} {f:9s} R_own {rc:6s}: {v}   bands outside 2 sigma in any cell: {', '.join(fails) or 'none'}")
RES["verdict"] = VERD
pk = rss(); check("K5", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB", "memory")
npass = sum(ok for _, ok in CHECKS)
RES.update(runtime_s=time.time() - T0, peak_rss_GB=pk)
say(f"\nZT2 COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time() - T0:.0f} s]")
open(os.path.join(HERE, f"zt2_cluster_terciles{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"zt2_cluster_terciles_results{TAG}.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer, np.bool_)) else str(o)))
sys.exit(0 if npass == len(CHECKS) else 1)
