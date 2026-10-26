#!/usr/bin/env python3
"""IJ1_isothermal_jeans_halos -- frozen criteria FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (46979ae8db).

Isothermal-Jeans cold dark energy halos: isothermal (sigma0) in the total potential inside r1, where rho s v t = 1 with
BU1's fixed s(v); EM1's NFW (Bullock c, M200(M_b)) outside; rho and M matched at r1. PRIMARY has no free parameter.
Machinery executed read-only: IC1's ic1b_lib (SC1 -> X38 -> EM1/X30, as OS1), EM1 up to its halo profiles (CLASS, cB),
GR1's group (P4 T3) and SLUGGS (CFG528b) sections, X40b's CFG922 BCG matching. One thread.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ij1_isothermal_jeans.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ij1_isothermal_jeans.py --mutate   -> baryons out of the Jeans potential
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ij1_isothermal_jeans.py --variant  -> REPORTED variant (A2: one child
                                                                       process per SPARC evaluation, --sparc-eval FOOT LOG10A)
"""
import os, sys, io, csv, json, math, time, signal, subprocess, contextlib, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
for _v in ("X30_MUTATE", "CFG528_MUTATE", "CFG528_POSTFREEZE", "CFG528B_MUTATE", "CFG331_MUTATE"): os.environ.pop(_v, None)
import numpy as np
from scipy.optimize import brentq

T0 = time.time()
MUTATE = "--mutate" in sys.argv
SPEVAL = "--sparc-eval" in sys.argv
VARIANT = "--variant" in sys.argv or SPEVAL
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
TAG = "_MUTATE" if MUTATE else ("_VARIANT" if VARIANT else "")
LAMF = 0.0 if MUTATE else 1.0
sys.path.insert(0, HERE)
import ij1_lib as IJ  # noqa: E402

OUT = []
RES = dict(frozen="46979ae8db", mutate=MUTATE, footings={}, checks={}, reported={})
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
def dump(tag=TAG):
    open(os.path.join(HERE, f"ij1_isothermal_jeans{tag}.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(RES, open(os.path.join(HERE, f"ij1_isothermal_jeans_results{tag}.json"), "w"), indent=1, default=float)
def _term(signum, frame):
    if SPEVAL: sys.exit(2)
    P(f"SIGTERM at {time.time() - T0:.0f} s: partial outputs written with _PARTIAL; rerun to resume (SPARC variant cache kept)")
    dump(TAG + "_PARTIAL"); sys.exit(2)
signal.signal(signal.SIGTERM, _term)

# ------------------------------------------------------------------ machinery (read-only)
LIBSRC = os.path.join(REB, "IC1_inner_cluster_band", "ic1b_lib.py"); src = open(LIBSRC).read()
assert src.count('"ic1b_x30_machinery.log"') == 1
src = src.replace('"ic1b_x30_machinery.log"', repr(os.path.join(HERE, f"ij1_x30_machinery{TAG}.log")))
NS = {"__file__": LIBSRC, "__name__": "ic1b_ro"}; argv0 = sys.argv
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, LIBSRC, "exec"), NS)
sys.argv = argv0
(BGS, line, FEET, HK, SREF, SIG, prep, PREP, RM, N, ALLI, I, T3M, GALS, fit_one, pooled, GE, MSUNE, MPCE, dvecN, cells_from,
 NX) = (NS[k] for k in ("BGS", "line", "FEET", "HK", "SREF", "SIG", "prep", "PREP", "RM", "N", "ALLI", "I", "T3M", "GALS",
                        "fit_one", "pooled", "GE", "MSUNE", "MPCE", "dvecN", "cells_from", "NX"))
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(TE[:TE.index("# ---------------- halo profiles")], EM1SRC, "exec"), NE)
sys.argv = argv0
EBG, UPS = NE["BGS"], NE["UPS"]
assert len(UPS) == GALS[0]["GB"].shape[1] == 91
OS1J = json.load(open(os.path.join(REB, "OS1_core_law_out_of_sample", "os1_out_of_sample_results.json")))
GR1J = json.load(open(os.path.join(REB, "GR1_core_law_groups_ellipticals", "gr1_groups_ellipticals_results.json")))
BU1J = json.load(open(os.path.join(REB, "BU1_bullet_cross_section", "bu1_cross_section_results.json")))
X38J = json.load(open(os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos_results.json")))
X40J = json.load(open(os.path.join(REB, "X40b_core_surface_density_scaling", "x40b_sd_scaling_results.json")))
QF = {f: float(OS1J["footings"][f]["q_f"]) for f in FEET}
P(f"IJ1_isothermal_jeans_halos {'MUTATE (baryons removed from the Jeans potential)' if MUTATE else 'normal run'}  (frozen 46979ae8db)")
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy, not matter; route E outside r1; not theory closed")
P(f"machinery loaded (ic1b_lib -> SC1 -> X38 -> EM1/X30; EM1 CLASS backgrounds)  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
checks = []

# ------------------------------------------------------------------ units, s(v)
KPCm, MSUN = 3.0857e19, 1.98847e30
YR = 3.156e7; T_AGE = 13.8e9 * YR; TK = T_AGE / (KPCm / 1e3)            # t in kpc / (km/s)
CONV = 0.1 * MSUN / KPCm ** 2                                            # 1 cm^2/g in kpc^2/Msun
VFAC = 4 / math.sqrt(math.pi)
NSL = {f: float(BU1J["footings"][f]["n"]) for f in FEET}
SVK = {f: float(BU1J["footings"][f]["K_SI"]) * 1e3 ** (1 - NSL[f]) * (MSUN / KPCm ** 2) * 1e-3 for f in FEET}   # s v = SVK sigma^(1-n)
def s_cm2g(f, v, A=1.0):
    sig = v / VFAC; return A * SVK[f] * sig ** (1 - NSL[f]) / v / CONV
k2 = max(abs(s_cm2g(f, float(v)) / BU1J["footings"][f]["s_cm2g"][v] - 1) for f in FEET for v in BU1J["footings"][f]["s_cm2g"])
P(f"K2 s(v) vs BU1 JSON (10-4700 km/s): max rel {k2:.1e}; s(159.1) = " + " / ".join(f"{s_cm2g(f, VFAC * SREF):.4f}" for f in FEET)
  + f" cm^2/g; n = " + " / ".join(f"{NSL[f]:.3f}" for f in FEET) + f": {'PASS' if k2 < 1e-9 else 'FAIL'}")
checks.append(("K2", k2 < 1e-9))

# ------------------------------------------------------------------ K0: Lane-Emden vs IC1's table
mu_ic1, xi_ic1 = NS["_MU"], NS["_XI"]
k0b = float(np.max(np.abs(IJ.XI ** 2 * IJ.DPSI / mu_ic1 - 1))) if len(mu_ic1) == len(IJ.XI) else 1.0
s0_, rho0_ = 100.0, 1e8; rc_ = s0_ / math.sqrt(4 * math.pi * IJ.GK * rho0_)
LGd = np.linspace(math.log(1e-5), math.log(1e4), 50)
Ld = IJ.Lanes([1e3 * rc_], [4 * rho0_ * 1e-6], [1e30], [1.0], [0.0], [1.0], LGd, np.zeros((1, 50)), np.zeros((1, 50)), [0], [0.0])
Ld.svK = np.array([1 / (s0_ * Ld.T[0] * rho0_ * 1e-6)])                     # rho1 = 1e-6 rho0, r1 = rs = 1e3 r_c
_, _, TMd, _ = IJ.integrate(Ld, np.array([math.log(s0_)]), np.array([math.log(rho0_)]), 0.0, keep=True)
r1d = float(Ld.bc(np.array([math.log(s0_)]))[0][0]); ud = IJ.UMIN + np.arange(IJ.NU + 1) * (-IJ.UMIN / IJ.NU)
xid = r1d * np.exp(ud) / rc_; sel = (xid >= 1e-2) & (xid <= 1e3)
mu_mine = TMd[0][sel] / (4 * math.pi * rho0_ * rc_ ** 3)
mu_tab = np.exp(np.interp(np.log(xid[sel]), np.log(xi_ic1), np.log(mu_ic1)))
k0a = float(np.max(np.abs(mu_mine / mu_tab - 1)))
k0 = k0a < 1e-6 and k0b < 1e-9
P(f"K0 isothermal solver (M_b = 0) vs IC1 Lane-Emden table: RK4 M(r) max rel {k0a:.1e} over xi 1e-2..1e3 (r1/r_c {r1d / rc_:.0f}); "
  f"own (psi, psi') table vs IC1 xi^2 psi' {k0b:.1e}: {'PASS' if k0 else 'FAIL'}")
checks.append(("K0", k0))

# ------------------------------------------------------------------ K4a: EM1 cB
cBA, cBB = (float(EBG[t]["cB"](12.0)[0]) for t in ("A_c2b_refit", "B_cfg886_bg"))
k4a = abs(cBA - 11.81) < 0.005 and abs(cBB - 11.51) < 0.005
P(f"K4a EM1 Bullock c(1e12) A / B = {cBA:.3f} / {cBB:.3f} (11.81 / 11.51): {'PASS' if k4a else 'FAIL'}")
checks.append(("K4a", k4a))

LG = np.linspace(math.log(1e-5), math.log(1e4), 3000); RRG = np.exp(LG)       # baryon-table grid, kpc
def rhoc_kpc(h): return 3 * (100 * h * 1e3 / MPCE) ** 2 / (8 * math.pi * GE) * KPCm ** 3 / MSUNE
def nfw_par(lM200, c, rc):
    M200 = 10 ** lM200; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3); rs = R200 / c
    return rs, M200 / (4 * math.pi * rs ** 3 * IJ.mN(c)), R200
def hern_tab(M, a): return M * RRG ** 2 / (RRG + a) ** 2
def stats_diag(L, x, conv, nr, r1):
    ok = conv & np.isfinite(r1)
    return dict(n=int(L.size), unconverged=int((~conv).sum()), frac_unconverged=float(np.mean(~conv)), multi_root=int((nr > 1).sum()),
                no_root=int((nr == 0).sum()), r1_gt_Rtr=int(np.sum(ok & (r1 > L.Rtr))),
                sigma0_med=float(np.median(np.exp(x[ok, 0]))) if ok.any() else None, r1_med_kpc=float(np.median(r1[ok])) if ok.any() else None,
                rho0_med_Msun_pc3=float(np.median(np.exp(x[ok, 1]))) / 1e9 if ok.any() else None)
K1 = {"max": 0.0, "n": 0}
def k1_check(L, x, conv, idx):
    for j in idx:
        if not conv[j]: continue
        a, b = IJ.check_lane(L, int(j), x[j], LAMF); K1["max"] = max(K1["max"], abs(a), abs(b)); K1["n"] += 1
RNG = np.random.default_rng(20261026)

# ------------------------------------------------------------------ SPARC
def sparc_tables():
    TG, TS = np.zeros((len(GALS), len(LG))), np.zeros((len(GALS), len(LG)))
    for j, g in enumerate(GALS):
        R = g["R"]; o = np.argsort(R); R = R[o]
        for T_, V2 in ((TG, (np.sign(g["Vgas"]) * g["Vgas"] ** 2)[o]), (TS, (g["Vdisk"] ** 2 + 1.4 * g["Vbul"] ** 2)[o])):
            v2 = np.interp(RRG, R, V2); v2 = np.where(RRG < R[0], V2[0] * (RRG / R[0]) ** 2, v2)
            m = RRG * v2 / IJ.GK; T_[j] = np.where(RRG > R[-1], R[-1] * V2[-1] / IJ.GK, m)
    return TG, TS
SPG, SPS = sparc_tables()
K1SP = {f: set(map(tuple, np.c_[RNG.choice(len(GALS), 20, replace=False), RNG.integers(0, 91, 20)])) for f in FEET}
def sparc_ij(f, tag, A=1.0, pure=False, k1=False, chunk=5):
    bg = BGS[tag]; cB = EBG[tag]["cB"]; rc = rhoc_kpc(bg["h"]); rows = []; D = dict(lanes=[])
    agg = dict(x=[], conv=[], nr=[], r1=[], Rtr=[])
    for j0 in range(0, len(GALS), chunk):
        js = list(range(j0, min(j0 + chunk, len(GALS))))
        lM = np.array([bg["a"] + bg["b"] * (GALS[j]["lMb"] - 10) for j in js]); cc = cB(lM)
        par = [nfw_par(lM[k], cc[k], rc) for k in range(len(js))]
        rs = np.repeat([p[0] for p in par], 91); rhos = np.repeat([p[1] for p in par], 91); Rtr = np.repeat([p[2] for p in par], 91)
        rowi = np.repeat(js, 91); ups = np.tile(UPS, len(js)); nl = len(rs)
        L = IJ.Lanes(rs, rhos, Rtr, np.full(nl, A * SVK[f]), np.full(nl, NSL[f]), np.full(nl, TK), LG, SPG, SPS, rowi, ups)
        if pure: x, conv, nr = np.zeros((nl, 2)), np.zeros(nl, bool), np.zeros(nl, int)
        else: x, conv, nr = IJ.solve(L, LAMF)
        if k1: k1_check(L, x, conv, [k * 91 + u for k, j in enumerate(js) for (jj, u) in K1SP[f] if jj == j])
        for k, j in enumerate(js):
            g = GALS[j]; sl = slice(k * 91, (k + 1) * 91); Ls = L.sub(np.arange(sl.start, sl.stop))
            Mh, r1 = IJ.halo_mass(Ls, x[sl], conv[sl], np.broadcast_to(g["R"], (91, len(g["R"]))), LAMF)
            gh = GE * Mh * MSUNE / (g["R"][None, :] * KPCm) ** 2                     # (91, npts) m/s^2
            w = fit_one(g, np.log10(np.maximum(g["GB"] + gh.T, 1e-300))); rows.append(w)
            iu = int(w[2]); agg["x"].append(x[sl][iu]); agg["conv"].append(conv[sl][iu]); agg["nr"].append(nr[sl][iu])
            agg["r1"].append(r1[iu]); agg["Rtr"].append(Rtr[sl][iu])
            D["frac_unconv_all_ups"] = D.get("frac_unconv_all_ups", 0) + int((~conv[sl]).sum())
    st = pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows])
    Lb = IJ.Lanes(np.ones(len(GALS)), np.ones(len(GALS)), np.array(agg["Rtr"]), np.ones(len(GALS)), np.zeros(len(GALS)), np.ones(len(GALS)),
                  LG, SPG, SPS, np.arange(len(GALS)), np.ones(len(GALS)))
    st["diag_at_best_U"] = stats_diag(Lb, np.array(agg["x"]), np.array(agg["conv"]), np.array(agg["nr"]), np.array(agg["r1"]))
    st["unconverged_all_lanes"] = int(D.get("frac_unconv_all_ups", 0)); st["frac_unconverged_all_lanes"] = st["unconverged_all_lanes"] / (91 * len(GALS))
    st["line"] = line(st); return st
if SPEVAL:                                   # A2: one SPARC evaluation in a child process
    _f, _la = sys.argv[sys.argv.index("--sparc-eval") + 1], float(sys.argv[sys.argv.index("--sparc-eval") + 2])
    _st = sparc_ij(_f, "A_c2b_refit", 10 ** _la)
    print("SPARC_EVAL " + json.dumps(dict(rms=_st["rms"], U=_st["U_median"], rss=rss())), flush=True); sys.exit(0)

# ------------------------------------------------------------------ clusters (X30 cells, BCG as X39 / X40b)
P687 = np.load(os.path.join(REPO, "campaign_fresh_gravity", "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
CEN = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG922_cluster_core_baryon_recheck", "cfg922_census_A1.json")))["eRASS1"]
MY = NX["MY"]; J9 = np.full(N, -1)
for i in range(N):
    dd = np.hypot((P687["ra"] - MY["ra"][i]) * np.cos(np.radians(MY["dec"][i])), P687["dec"] - MY["dec"][i]) * 3600; j = int(np.argmin(dd))
    if dd[j] < 5 and abs(P687["z"][j] - MY["z"][i]) < 1e-3: J9[i] = j
meas = np.array([j >= 0 and not CEN[j].get("not_measured", False) for j in J9])
bcg = np.array([float(CEN[j]["bcg_med"]) if j >= 0 else np.nan for j in J9])
BCG = np.where(meas & (bcg > 0), bcg, np.nan); nbcg = int(np.isfinite(BCG).sum()); FILL = BCG.copy()
for t in range(3):
    m = T3M == t; FILL[m & ~np.isfinite(BCG)] = float(np.nanmedian(BCG[m]))
P(f"CFG922 BCG matched {nbcg} (X39 / X40b: 190); filled {int((~np.isfinite(BCG)).sum())} by MGAS500-tercile median")
CLZ = np.array([float(NX["CL"][i]["z"]) for i in range(N)])
EA = EBG["A_c2b_refit"]; BGA = BGS["A_c2b_refit"]
RHOCZ = {}
def cluster_ij(f, A=1.0, pure=False, bcg=True, fair=False, k1=False):
    out = {}; diag = {}; Mh_all = {}
    for hk in HK:
        idx = [int(i) for i in ALLI]; nl = len(idx)
        TG = np.zeros((nl, len(LG))); rs = np.zeros(nl); rhos = np.zeros(nl); Rtr = np.zeros(nl)
        for k, i in enumerate(idx):
            pp = prep(i, f, hk); lr = np.log(RM / KPCm); Mb = pp["Mb"] / MSUNE
            if bcg: Mb = Mb + FILL[i] * (RM / KPCm) ** 2 / (RM / KPCm + 10.0) ** 2
            lm = np.log(np.maximum(Mb, 1e-300)); p0 = (lm[1] - lm[0]) / (lr[1] - lr[0])
            TG[k] = np.exp(np.where(LG < lr[0], lm[0] + p0 * (LG - lr[0]), np.interp(LG, lr, lm)))
            z = CLZ[i]
            if z not in RHOCZ: RHOCZ[z] = EA["rhoc"](z) * KPCm ** 3 / MSUNE
            Mt = pp["Mfair"] / MSUNE if fair else 10 ** (BGA["a"] + BGA["b"] * (math.log10(float(pp["Mb"][-1]) / MSUNE) - 10))
            c = float(EA["cB"](math.log10(Mt), z)[0]); rs[k], rhos[k], _ = nfw_par(math.log10(Mt), c, RHOCZ[z]); Rtr[k] = pp["rta"] / KPCm
        L = IJ.Lanes(rs, rhos, Rtr, np.full(nl, A * SVK[f]), np.full(nl, NSL[f]), np.full(nl, TK), LG, TG, np.zeros_like(TG), np.arange(nl), np.ones(nl))
        if pure: x, conv, nr = np.zeros((nl, 2)), np.zeros(nl, bool), np.zeros(nl, int)
        else: x, conv, nr = IJ.solve(L, LAMF)
        if k1 and hk == "h0672": k1_check(L, x, conv, RNG.choice(nl, 20, replace=False))
        Mh, r1 = IJ.halo_mass(L, x, conv, np.broadcast_to(RM / KPCm, (nl, len(RM))), LAMF)
        V = np.zeros((N, 8))
        for k, i in enumerate(idx):
            V[i] = dvecN(i, f, hk, prep(i, f, hk)["Mb"] + Mh[k] * MSUNE)
        PREP.clear()
        out[hk] = cells_from(f, hk, V)[0]; diag[hk] = stats_diag(L, x, conv, nr, r1)
        if hk == "h0672":
            diag["sigma0_by_KT_tercile"] = {f"T{t+1}": float(np.median(np.exp(x[np.isin(idx, np.asarray(I)[NS['TID'] == t]) & conv, 0])))
                                           for t in range(3)} if not pure else None
            diag["r1_kpc_by_KT_tercile"] = {f"T{t+1}": float(np.nanmedian(r1[np.isin(idx, np.asarray(I)[NS['TID'] == t])])) for t in range(3)} if not pure else None
    ok = {k: all(abs(out[hk][k]["Z"]) <= 2 for hk in HK) for k in out["h0672"]}
    return out, ok, diag

# ------------------------------------------------------------------ groups + SLUGGS: GR1's sections (read-only)
GR1SRC = os.path.join(REB, "GR1_core_law_groups_ellipticals", "gr1_groups_ellipticals.py"); TG1 = open(GR1SRC).read()
seg = TG1[TG1.index("# ------------------------------------------------------------------ groups (P4 T3"):
          TG1.index("# ------------------------------------------------------------------ graded runs")]
GNS = dict(np=np, math=math, json=json, os=os, sys=sys, io=io, contextlib=contextlib, brentq=brentq, time=time, T0=T0, rss=rss,
           P=lambda *a: None, checks=[], REB=REB, REPO=REPO, bgA=BGA, SIG=SIG, SREF=SREF, solve_r0=NS["NS"]["solve_r0"], BURK=NS["NS"]["B"],
           SAT=NS["NS"]["SAT"], GE=GE, MSUNE=MSUNE, MPCE=MPCE, FEET=FEET, X40J=X40J, X38J=X38J, OS1J=OS1J, QF=QF, MUTATE=False)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(seg, GR1SRC, "exec"), GNS)
k4c = all(ok for _, ok in GNS["checks"])
P(f"GR1 sections executed: its K0d / K0b / K0c " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in GNS["checks"]))
GROUPS, NSG, BIN, CEN5, RGs, LRs, Gs, KPCs, score, off_pops, POPS, MS528 = (GNS[k] for k in (
    "GROUPS", "NSG", "BIN", "CEN", "RG", "LR", "Gs", "KPC", "score", "off_pops", "POPS", "MSUN"))
XG, LXG, RHO_H, M_H, HERN_RE, G540, MS540, KP540 = (NSG[k] for k in ("XG", "LXG", "RHO_H", "M_H", "HERN_RE", "G540", "MSUN540", "KPC540"))
RCA = rhoc_kpc(BGA["h"])
def groups_ij(f, A=1.0, pure=False, k1=False):
    lanes = [(o, d) for o in GROUPS for d in (0.0, 0.01, -0.01)]; nl = len(lanes)
    TG = np.zeros((nl, len(LG))); rs = np.zeros(nl); rhos = np.zeros(nl); Rtr = np.zeros(nl); aa = np.zeros(nl); Mbs = np.zeros(nl)
    for k, (o, d) in enumerate(lanes):
        lMb = o["lM"] + d; Mbs[k] = 10 ** lMb; aa[k] = o["Re"] / HERN_RE; TG[k] = hern_tab(Mbs[k], aa[k])
        lM200 = BGA["a"] + BGA["b"] * (lMb - 10); rs[k], rhos[k], Rtr[k] = nfw_par(lM200, float(EA["cB"](lM200)[0]), RCA)
    L = IJ.Lanes(rs, rhos, Rtr, np.full(nl, A * SVK[f]), np.full(nl, NSL[f]), np.full(nl, TK), LG, TG, np.zeros_like(TG), np.arange(nl), np.ones(nl))
    if pure: x, conv, nr = np.zeros((nl, 2)), np.zeros(nl, bool), np.zeros(nl, int)
    else: x, conv, nr = IJ.solve(L, LAMF)
    if k1: k1_check(L, x, conv, 3 * RNG.choice(len(GROUPS), 10, replace=False))
    Mh, r1 = IJ.halo_mass(L, x, conv, XG[None, :] * aa[:, None], LAMF)
    ls = np.zeros(nl)
    for k in range(nl):
        gN = M_H / XG ** 2 + Mh[k] / Mbs[k] / XG ** 2
        s2 = float(np.trapz(4 * np.pi * XG ** 2 * RHO_H * XG * gN * XG, LXG) / 3.0) * G540 * Mbs[k] * MS540 / (aa[k] * KP540)
        ls[k] = 0.5 * math.log10(s2) - 3.0
    ls = ls.reshape(len(GROUPS), 3); d = [o["ls"] - ls[j, 0] for j, o in enumerate(GROUPS)]; sl = list((ls[:, 1] - ls[:, 2]) / 0.02)
    st = NSG["class_stats"](d, sl); st["diag"] = stats_diag(L, x, conv, nr, r1); return st
def slug_halo(n, f, A, Ms, k1=False):
    b = BIN[n]; lM200 = BGA["a"] + BGA["b"] * (math.log10(Ms) - 10)
    rs, rhos, R200 = nfw_par(lM200, float(EA["cB"](lM200)[0]), RCA)
    L = IJ.Lanes([rs], [rhos], [R200], [A * SVK[f]], [NSL[f]], [TK], LG, hern_tab(Ms, b["ah"])[None, :], np.zeros((1, len(LG))), [0], [1.0])
    x, conv, nr = IJ.solve(L, LAMF)
    if k1: k1_check(L, x, conv, [0])
    Mh, r1 = IJ.halo_mass(L, x, conv, RGs[None, :], LAMF)
    return Mh[0], dict(converged=bool(conv[0]), sigma0=float(math.exp(x[0, 0])), r1_kpc=float(r1[0]), n_roots=int(nr[0]))
def sluggs_ij(f, A=1.0, k1=False):
    per, info, nunc = {}, {}, 0
    for n in CEN5:
        b = BIN[n]; lr12 = math.log(b["r12"]); cache = {}
        def enc(lm):
            if lm not in cache: cache[lm] = slug_halo(n, f, A, 10 ** lm)
            return math.log10(0.5 * 10 ** lm + float(np.interp(lr12, LRs, cache[lm][0]))) - math.log10(0.5 * b["Mjam"])
        grid = np.linspace(math.log10(b["Mjam"]) - 3, math.log10(b["Mjam"]), 13); fv = [enc(float(v)) for v in grid]
        br = [k for k in range(12) if fv[k] * fv[k + 1] <= 0]
        if not br:
            per[n] = None; info[f"NGC{n}"] = "not computable (no JAM-analogue root)"; continue
        lm = brentq(enc, float(grid[br[0]]), float(grid[br[0] + 1]), xtol=1e-6)
        Mh, dg = slug_halo(n, f, A, 10 ** lm, k1=k1); nunc += not dg["converged"]; Ms = 10 ** lm
        g = Gs * (Ms * RGs ** 2 / (RGs + b["ah"]) ** 2 + Mh) * MS528 / (RGs * KPCs) ** 2
        per[n] = off_pops(n, g, POPS[n]); info[f"NGC{n}"] = dict(Mstar_over_Mjam=Ms / b["Mjam"], **dg)
    st = score(per, f); st["info"] = info; st["unconverged"] = nunc; return st
def gcls(st): return "PASS" if st["verdict"] == "CONSISTENT" else "FAILS"
def scls(st, os1):
    if st["closes"]: return "PASS"
    comp = all(v is not None for v in st["per"].values())
    if comp and st["n_reversed"] == 0 and np.isfinite(st["mean"]) and abs(st["mean"]) <= 0.5 * abs(os1): return "IMPROVES ON OS1"
    return "FAILS"

# ------------------------------------------------------------------ dwarfs (CD1 / OS1 rule)
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
G_, PC = 6.674e-11, 3.0857e16; CAP = 0.254484; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
def dwarf_rows(f):
    out = []
    for r in (r for r in X1 if r["footing"] == f):
        r12 = 4 / 3 * float(r["rh_pc"]) * PC; gN = G_ * (10 ** float(r["logMstar"]) * 1.989e30 / 2) / r12 ** 2
        D, sd = float(r["Delta[Newton]"]), float(r["sdMC[Newton]"]); out.append(dict(r=r, r12=r12, gN=gN, D=D, sd=sd, gobs=gN * 10 ** D))
    return out
def dwarf_grade(rows, gpred):
    res = []
    for o, gp in zip(rows, gpred):
        r = o["r"]
        if o["D"] <= 0: res.append(dict(name=r["name"], cls=r["cls"], S=0.0, z=-np.inf, graded=True)); continue
        ratio = 10 ** o["D"] - 1
        if ratio < 0.1: res.append(dict(name=r["name"], cls=r["cls"], S=np.nan, z=np.nan, graded=False)); continue
        gh = o["gobs"] - o["gN"]; sdh = o["sd"] * 10 ** o["D"] / ratio
        res.append(dict(name=r["name"], cls=r["cls"], S=gh / gp, z=(math.log10(gh) - math.log10(gp)) / sdh, graded=True, g_pred_over_a0=gp))
    g = [o for o in res if o["graded"]]; fin = [o for o in g if np.isfinite(o["z"])]
    fu = float(np.mean([o["z"] >= 2 for o in g])); medS = float(np.median([o["S"] for o in g])); fo = float(np.mean([o["z"] <= -2 for o in fin]))
    cd1 = "EXCLUDE" if fu >= 0.25 else ("CONSISTENT" if fu < 0.05 and medS <= 1 else "PARTIAL")
    return dict(frac_up=fu, medS=medS, frac_over=fo, cd1_label=cd1, n_graded=len(g), rows=res)
def dwarfs_os1(f, q):
    rows = dwarf_rows(f); gp = []
    for o in rows:
        sig = math.sqrt(o["gobs"] * o["r12"] / 3) / 1e3; gp.append(CAP * A0[f] * (sig / SREF) ** q)
    return dwarf_grade(rows, gp)
def dwarfs_ij(f, A=1.0, pure=False, k1=False):
    rows = dwarf_rows(f); nl = len(rows)
    TG = np.zeros((nl, len(LG))); rs = np.zeros(nl); rhos = np.zeros(nl); Rtr = np.zeros(nl)
    for k, o in enumerate(rows):
        Ms = 10 ** float(o["r"]["logMstar"]); a = float(o["r"]["rh_pc"]) / 1e3
        TG[k] = Ms * RRG ** 3 / (RRG ** 2 + a ** 2) ** 1.5
        lM200 = BGA["a"] + BGA["b"] * (math.log10(Ms) - 10); rs[k], rhos[k], Rtr[k] = nfw_par(lM200, float(EA["cB"](lM200)[0]), RCA)
    L = IJ.Lanes(rs, rhos, Rtr, np.full(nl, A * SVK[f]), np.full(nl, NSL[f]), np.full(nl, TK), LG, TG, np.zeros_like(TG), np.arange(nl), np.ones(nl))
    if pure: x, conv, nr = np.zeros((nl, 2)), np.zeros(nl, bool), np.zeros(nl, int)
    else: x, conv, nr = IJ.solve(L, LAMF)
    if k1: k1_check(L, x, conv, RNG.choice(nl, 10, replace=False))
    r12k = np.array([o["r12"] / KPCm for o in rows])
    Mh, r1 = IJ.halo_mass(L, x, conv, r12k[:, None], LAMF)
    gp = GE * Mh[:, 0] * MSUNE / (r12k * KPCm) ** 2
    st = dwarf_grade(rows, gp); st["diag"] = stats_diag(L, x, conv, nr, r1)
    st["r1_over_r12_med"] = float(np.nanmedian(r1 / r12k)); return st
def dcls(st, os1_fu):
    if st["frac_up"] < 0.05 and st["medS"] <= 1 and st["frac_over"] < 0.25: return "PASS"
    if st["frac_up"] <= 0.5 * os1_fu and st["frac_over"] < 0.25: return "IMPROVES ON OS1"
    return "FAILS"

# ------------------------------------------------------------------ K4: record reproduction
if not MUTATE and not VARIANT:
    k4 = {}
    for f in FEET:
        c, _, _ = NS["grade"](f, QF[f]); oc = OS1J["footings"][f]["clusters"]["cells"]
        k4[f"OS1 cells {f}"] = max(abs(c[h][k]["pred"] - oc[h][k]["pred"]) for h in HK for k in c[h]) < 1e-6
        k4[f"GR1 groups {f}"] = abs(GNS["grade_groups"](f, QF[f])["mean"] - GR1J["footings"][f]["groups"]["st"]["mean"]) < 1e-6
        k4[f"GR1 SLUGGS {f}"] = abs(GNS["sluggs"](f, QF[f])["mean"] - GR1J["footings"][f]["sluggs"]["st"]["mean"]) < 1e-6
        d0 = dwarfs_os1(f, QF[f]); od = OS1J["footings"][f]["dwarfs"]
        k4[f"OS1 dwarfs {f}"] = abs(d0["frac_up"] - od["frac"]) < 1e-9 and abs(d0["medS"] - od["medS"]) < 1e-9
    k4["GR1 K0 sections"] = k4c
    P("K4 record reproduction: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in k4.items()) + f"   [{time.time() - T0:.0f} s]")
    checks.append(("K4", all(k4.values()) and k4a))
OS1REF = {f: dict(sumZ=float(OS1J["footings"][f]["clusters"]["sumZ"]), dw_fu=float(OS1J["footings"][f]["dwarfs"]["frac"]),
                  slug_mean=float(GR1J["footings"][f]["sluggs"]["st"]["mean"])) for f in FEET}

# ------------------------------------------------------------------ PRIMARY grades
def ccls(ok, cells, f):
    if all(ok.values()): return "PASS"
    bad = [k for k in ok if not ok[k]]
    sZ = sum(max(abs(cells[h][k]["Z"]) for h in HK) for k in bad)
    return "IMPROVES ON OS1" if len(bad) <= 1 and sZ < OS1REF[f]["sumZ"] else "FAILS"
def grade_all(f, A=1.0, k1=False, label="PRIMARY"):
    R = {}
    sA = sparc_ij(f, "A_c2b_refit", A, k1=k1); sB = sparc_ij(f, "B_cfg886_bg", A)
    R["sparc"] = dict(A=sA, B=sB, cls="PASS" if (sA["line"] and sB["line"]) else "FAILS")
    P(f"  [{f}|{label}] SPARC A rms {sA['rms']:.4f} @ U {sA['U_median']:.2f}, B {sB['rms']:.4f} @ {sB['U_median']:.2f} -> {R['sparc']['cls']}"
      f"; at best U: sigma0 med {sA['diag_at_best_U']['sigma0_med']:.1f} km/s, r1 med {sA['diag_at_best_U']['r1_med_kpc']:.2f} kpc; "
      f"unconverged {sA['unconverged_all_lanes']}/{91 * len(GALS)} lanes   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    cells, ok, cd = cluster_ij(f, A, k1=k1); cc = ccls(ok, cells, f)
    R["clusters"] = dict(cells=cells, ok=ok, diag=cd, cls=cc, fails=[k for k in ok if not ok[k]])
    for k in cells["h0672"]:
        a, b = cells["h0672"][k], cells["h0686"][k]
        P(f"     {k:10s} meas {a['meas']:+.3f}+-{a['s']:.3f} pred {a['pred']:+.3f} Z {a['Z']:+.2f} | h0.686 Z {b['Z']:+.2f}" + ("" if ok[k] else "  FAIL"))
    P(f"  [{f}|{label}] clusters -> {cc}; fails {R['clusters']['fails'] or 'none'}; sigma0 by KT tercile {cd.get('sigma0_by_KT_tercile')}; "
      f"r1 (kpc) {cd.get('r1_kpc_by_KT_tercile')}; unconverged {cd['h0672']['unconverged']}/{cd['h0672']['n']}   [{time.time() - T0:.0f} s]")
    g = groups_ij(f, A, k1=k1); R["groups"] = dict(st=g, cls=gcls(g))
    P(f"  [{f}|{label}] groups mean {g['mean']:+.4f} Z {g['Z']:+.2f} tot {g['tot']:.4f} -> {g['verdict']} -> {R['groups']['cls']}"
      f" (OS1/GR1 {GR1J['footings'][f]['groups']['st']['mean']:+.4f}, Z {GR1J['footings'][f]['groups']['st']['Z']:+.2f}); "
      f"sigma0 med {g['diag']['sigma0_med']:.0f} km/s; unconverged {g['diag']['unconverged']}")
    s = sluggs_ij(f, A, k1=k1); R["sluggs"] = dict(st=s, cls=scls(s, OS1REF[f]["slug_mean"]))
    P(f"  [{f}|{label}] SLUGGS " + " ".join(f"NGC{n} {(s['per'][f'NGC{n}'] if s['per'][f'NGC{n}'] is not None else float('nan')):+.3f}({s['Z'][f'NGC{n}']:+.1f})" for n in CEN5)
      + f" | mean {s['mean']:+.3f} (OS1 {OS1REF[f]['slug_mean']:+.3f}) cleared {s['n_cleared']}/4 rev {s['n_reversed']} -> {R['sluggs']['cls']}   [{time.time() - T0:.0f} s]")
    d = dwarfs_ij(f, A, k1=k1); R["dwarfs"] = dict(st=d, cls=dcls(d, OS1REF[f]["dw_fu"]))
    P(f"  [{f}|{label}] dwarfs frac_up {d['frac_up']:.3f} (OS1 {OS1REF[f]['dw_fu']:.3f}), median S {d['medS']:.2f}, frac_over {d['frac_over']:.3f}, "
      f"CD1 label {d['cd1_label']} -> {R['dwarfs']['cls']}; r1/r12 med {d['r1_over_r12_med']:.2f}; sigma0 med {d['diag']['sigma0_med']:.1f} km/s")
    t_ic = R["clusters"]["ok"]["G-IN-Mall"]; t_gr = R["sluggs"]["cls"] != "FAILS"; t_dw = R["dwarfs"]["cls"] != "FAILS"
    R["targets"] = dict(T_IC=t_ic, T_GR=t_gr, T_DW=t_dw)
    allc = [R[k]["cls"] for k in ("sparc", "clusters", "groups", "sluggs", "dwarfs")]
    if all(c == "PASS" for c in allc): lc = "IJ PASSES"
    elif t_ic and t_gr and t_dw and R["sparc"]["cls"] == "PASS" and R["groups"]["cls"] == "PASS" and R["clusters"]["cls"] != "FAILS": lc = "IJ HITS TARGETS"
    elif t_ic or t_gr or t_dw: lc = "IJ PARTIAL"
    else: lc = "IJ FAILS"
    R["lane_class"] = lc
    P(f"  [{f}|{label}] targets T-IC {t_ic}, T-GR {t_gr}, T-DW {t_dw}; classes SPARC {allc[0]}, clusters {allc[1]}, groups {allc[2]}, "
      f"SLUGGS {allc[3]}, dwarfs {allc[4]} -> LANE CLASS {lc}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    return R

if not VARIANT:
    for f in FEET:
        P(f"\n=== [{f}] PRIMARY: s(159 km/s) = {s_cm2g(f, VFAC * SREF):.4f} cm^2/g, n = {NSL[f]:.3f}" + ("  (MUTATE: lambda = 0)" if MUTATE else ""))
        RES["footings"][f] = dict(primary=grade_all(f, k1=not MUTATE)); dump(TAG + "_PARTIAL")

    if MUTATE:
        real = json.load(open(os.path.join(HERE, "ij1_isothermal_jeans_results.json")))
        bite = True
        for f in FEET:
            rp, mp = real["footings"][f]["primary"], RES["footings"][f]["primary"]
            ds = abs(mp["sluggs"]["st"]["mean"] - rp["sluggs"]["st"]["mean"])
            pr, pm = rp["clusters"]["cells"]["h0672"]["G-IN-Mall"]["pred"], mp["clusters"]["cells"]["h0672"]["G-IN-Mall"]["pred"]
            dc = abs(pm / pr - 1); b_ = ds >= 0.02 and dc >= 0.02; bite &= b_
            P(f"[{f}] MUTATE: SLUGGS mean moves {ds:.4f} dex (>= 0.02), G-IN-Mall pred moves {dc * 100:.2f} % (>= 2 %): {'bites' if b_ else 'does NOT bite'}")
            RES["footings"][f]["mutate"] = dict(d_sluggs=ds, d_inner_rel=dc, bites=b_)
        checks.append(("MUT", bite))
    else:
        V = {f: RES["footings"][f]["primary"]["lane_class"] for f in FEET}
        RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"UNDECIDED (footings disagree: {V})"
        per_cls = {}
        for c in ("sparc", "clusters", "groups", "sluggs", "dwarfs"):
            cs = {f: RES["footings"][f]["primary"][c]["cls"] for f in FEET}
            per_cls[c] = cs["canonical"] if cs["canonical"] == cs["alt"] else f"UNDECIDED {cs}"
        RES["verdict_per_class"] = per_cls
        P(f"\n=== PRIMARY VERDICT: {RES['verdict']}; per class {per_cls}")
        k1ok = K1["n"] > 0 and K1["max"] < 1e-4
        P(f"K1 matching (independent LSODA from the centre, {K1['n']} lanes over all classes and footings): max |rel| {K1['max']:.1e}: {'PASS' if k1ok else 'FAIL'}")
        checks.append(("K1", k1ok))
        k3 = {}
        for f in FEET:
            p = RES["footings"][f]["primary"]
            k3[f] = dict(sparc=p["sparc"]["A"]["frac_unconverged_all_lanes"], clusters=max(p["clusters"]["diag"][h]["frac_unconverged"] for h in HK),
                         groups=p["groups"]["st"]["diag"]["frac_unconverged"], sluggs=p["sluggs"]["st"]["unconverged"] / 4, dwarfs=p["dwarfs"]["st"]["diag"]["frac_unconverged"])
        k3ok = all(v <= 0.01 for d in k3.values() for v in d.values())
        P(f"K3 unconverged fractions {k3}: {'PASS' if k3ok else 'FAIL'}"); checks.append(("K3", k3ok)); RES["K3"] = k3
        dump(TAG + "_PARTIAL")

        # ---------------------------------------------------------- reported only
        P("\n=== REPORTED ONLY (no class weight)")
        for f in FEET:
            rep = RES["reported"].setdefault(f, {})
            sp = sparc_ij(f, "A_c2b_refit", pure=True); cpure, okp, _ = cluster_ij(f, pure=True); gp = groups_ij(f, pure=True); dp = dwarfs_ij(f, pure=True)
            rep["pure_NFW"] = dict(sparc=dict(rms=sp["rms"], U=sp["U_median"], line=sp["line"]), cluster_fails=[k for k in okp if not okp[k]],
                                   G_IN_Mall_Z=cpure["h0672"]["G-IN-Mall"]["Z"], groups=dict(mean=gp["mean"], Z=gp["Z"], verdict=gp["verdict"]),
                                   dwarfs=dict(frac_up=dp["frac_up"], medS=dp["medS"], frac_over=dp["frac_over"]))
            P(f"  [{f}] pure NFW (no core): SPARC A {sp['rms']:.4f} @ U {sp['U_median']:.2f}; cluster fails {rep['pure_NFW']['cluster_fails'] or 'none'} "
              f"(G-IN-Mall Z {rep['pure_NFW']['G_IN_Mall_Z']:+.2f}); groups {gp['mean']:+.4f} Z {gp['Z']:+.2f}; dwarfs frac_up {dp['frac_up']:.3f} "
              f"medS {dp['medS']:.2f} frac_over {dp['frac_over']:.3f}   [{time.time() - T0:.0f} s]")
            cf, okf, _ = cluster_ij(f, fair=True); rep["clusters_fair_share_5364"] = dict(fails=[k for k in okf if not okf[k]], cells=cf)
            P(f"  [{f}] clusters with OS1's fair-share mass (5.364, LCDM-derived; comparator only): fails {rep['clusters_fair_share_5364']['fails'] or 'none'}; "
              f"G-IN-Mall Z {cf['h0672']['G-IN-Mall']['Z']:+.2f}")
            cn, okn, _ = cluster_ij(f, bcg=False); rep["clusters_no_BCG"] = dict(fails=[k for k in okn if not okn[k]], G_IN_Mall_pred=cn["h0672"]["G-IN-Mall"]["pred"])
            P(f"  [{f}] clusters without the BCG: fails {rep['clusters_no_BCG']['fails'] or 'none'}; G-IN-Mall pred {cn['h0672']['G-IN-Mall']['pred']:.4f} "
              f"(with BCG {RES['footings'][f]['primary']['clusters']['cells']['h0672']['G-IN-Mall']['pred']:.4f})")
            bycls = {}
            for o in RES["footings"][f]["primary"]["dwarfs"]["st"]["rows"]:
                if o["graded"]: bycls.setdefault(o["cls"], []).append(o)
            rep["dwarfs_by_class"] = {k: dict(n=len(v), frac_up=float(np.mean([o["z"] >= 2 for o in v])), medS=float(np.median([o["S"] for o in v])))
                                      for k, v in sorted(bycls.items())}
            for k, v in rep["dwarfs_by_class"].items(): P(f"     dwarfs {k:24s} n {v['n']:3d} frac_up {v['frac_up']:.2f} median S {v['medS']:.2f}")
            dump(TAG + "_PARTIAL")
else:
    CHILD_RSS = {"max": 0.0}
    # ---------------------------------------------------------- variant: amplitude once on SPARC
    CACHE = os.path.join(HERE, "ij1_variant_sparc_cache.json")
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    for f in FEET:
        cf = cache.setdefault(f, {})
        def rmsA(la):
            kk = f"{la:+.2f}"
            if kk not in cf:
                pr = subprocess.run([sys.executable, os.path.abspath(__file__), "--sparc-eval", f, kk], capture_output=True, text=True)
                ln_ = [l for l in pr.stdout.splitlines() if l.startswith("SPARC_EVAL ")]
                if pr.returncode != 0 or not ln_: raise RuntimeError(f"child failed at {f} {kk}: {pr.stderr[-2000:]}")
                o_ = json.loads(ln_[0][11:]); cf[kk] = dict(rms=o_["rms"], U=o_["U"]); CHILD_RSS["max"] = max(CHILD_RSS["max"], o_["rss"])
                json.dump(cache, open(CACHE, "w"), indent=1)
            return cf[kk]["rms"]
        coarse = [round(-2 + 0.1 * i, 2) for i in range(41)]
        lc_ = min(coarse, key=rmsA)
        fine = sorted({round(lc_ + 0.02 * j, 2) for j in range(-5, 6)})
        laf = min(fine, key=rmsA); Af = 10 ** laf
        P(f"\n=== [{f}] VARIANT (REPORTED): log10 A_f = {laf:+.2f} (coarse {lc_:+.1f}); SPARC A rms {cf[f'{laf:+.2f}']['rms']:.4f} @ U {cf[f'{laf:+.2f}']['U']:.2f} "
          f"(A = 1: {cf['+0.00']['rms']:.4f})   [{time.time() - T0:.0f} s]")
        bnd = dict(s3000=s_cm2g(f, 3000, Af), s1000=s_cm2g(f, 1000, Af), s1900=s_cm2g(f, 1900, Af))
        P(f"  [{f}] variant bound margins: Bullet s(3000) {bnd['s3000']:.4f} vs 1.25 (x{1.25 / bnd['s3000']:.2f}); Harvey s(1000) {bnd['s1000']:.4f} vs 0.47 "
          f"(x{0.47 / bnd['s1000']:.2f}); Sagunski s(1900) {bnd['s1900']:.4f} vs 0.35 (x{0.35 / bnd['s1900']:.2f}); s(159) {s_cm2g(f, VFAC * SREF, Af):.3f} cm^2/g")
        RES["footings"].setdefault(f, {})["variant"] = dict(log10A=laf, A=Af, curve={k: v for k, v in cf.items()}, bounds=bnd, grades=grade_all(f, Af, label="VARIANT"))
        dump(TAG + "_PARTIAL")
    P(f"child SPARC evaluations: peak RSS {CHILD_RSS['max']:.2f} GB")
checks.append(("K5", rss() < 1.0))
n = sum(v for _, v in checks)
P(f"\nchecks {n}/{len(checks)}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks) + f"; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
RES["checks"] = {k: bool(v) for k, v in checks}
dump()
for t in ("_PARTIAL",):
    p_ = os.path.join(HERE, f"ij1_isothermal_jeans{TAG}{t}.out"); q_ = os.path.join(HERE, f"ij1_isothermal_jeans_results{TAG}{t}.json")
    for p in (p_, q_):
        if os.path.exists(p): os.remove(p)
if MUTATE: sys.exit(1 if n == len(checks) else 0)
sys.exit(0 if n == len(checks) else 1)
