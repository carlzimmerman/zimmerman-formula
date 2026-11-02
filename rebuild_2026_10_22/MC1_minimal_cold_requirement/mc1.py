#!/usr/bin/env python3
"""MC1 (FROZEN_CRITERIA.md, AMENDMENT_A1.md): the a0 law held fixed, invert for a separate cold component; requirements only, reinstates nothing.
    OMP_NUM_THREADS=1 nice -n 15 python3 mc1.py            -> mc1.out, mc1_results.json
    MC1_MUTATE=1 ... python3 mc1.py                        -> a0 x 1.5, share x 0.5; K1, K2 must fail, exit 1
kappa = 1/2 FITTED; cold dark energy, never a particle; not theory closed."""
import json, math, os, sys, csv, glob
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
import numpy as np, warnings; warnings.simplefilter("ignore")
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
MUT = bool(os.environ.get("MC1_MUTATE")); TAG = "_MUTATE" if MUT else ""; OUT = []; RES = {}; CHK = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(n, ok, t): CHK.append((n, bool(ok))); P(f"{n} {'PASS' if ok else 'FAIL'}: {t}")
A0 = dict(canonical=9.3603e-11 * (1.5 if MUT else 1), alt=1.1312e-10 * (1.5 if MUT else 1)); SHARE = 5.35 * (0.5 if MUT else 1); FEET = ("canonical", "alt")
G, MS, PC, CK = 6.674e-11, 1.989e30, 3.0857e16, 299792.458; KPC = PC * 1e3; MPC = PC * 1e6; KMS2 = 1e6; H = 0.672
OMX = 0.1197 * (0.5 if MUT else 1); OMB = 0.0224; RHOC_H1 = 3 * (100e3 / MPC) ** 2 / (8 * math.pi * G); RHOC = RHOC_H1 * H * H; MSPC3 = MS / PC ** 3
RX0 = OMX * RHOC_H1; OMm = (OMX + OMB) / H ** 2; BINS = [(20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)]; FQ = 0.872; INP = os.path.join(RB, "CRG1_clean_room_regrade", "inputs")
SEED = 20261102; NB = 2000
def law(g, a): return 0.5 * g + np.sqrt(0.25 * g * g + a * g)
def lawinv(g, a): return g * g / (g + a)
# ---------------------------------------------------------- native shape, contraction
SJ = json.load(open(os.path.join(RB, "ZN2_native_profile_sparc_groups", "zn2_low_shapes.json"))); LX = np.log(np.array(SJ["x"]))
TAGS = sorted(((float(SJ[m]["0.00"]["lgM"]), np.array(SJ[m]["0.00"]["lnm"])) for m in ("1e10", "1e11", "1e12", "1e13", "1e14")), key=lambda t: t[0])
def lnm(lg):
    if lg <= TAGS[0][0]: return TAGS[0][1]
    if lg >= TAGS[-1][0]: return TAGS[-1][1]
    k = next(i for i in range(len(TAGS) - 1) if TAGS[i][0] <= lg <= TAGS[i + 1][0]); w = (lg - TAGS[k][0]) / (TAGS[k + 1][0] - TAGS[k][0]); return (1 - w) * TAGS[k][1] + w * TAGS[k + 1][1]
FC = 5.35 / 6.35
def r200(M200): return (3 * M200 * MS / (4 * math.pi * 200 * RHOC)) ** (1 / 3)
def Mc_native(M200, r):
    R = r200(M200); ln_ = lnm(math.log10(M200)); lx = np.log(np.maximum(np.minimum(np.asarray(r, float), R) / R, 1e-300)); return FC * M200 * np.exp(np.where(lx >= LX[0], np.interp(lx, LX, ln_), ln_[0] + 2 * (lx - LX[0])))
_x = open(os.path.join(RB, "X39_baryonic_contraction", "x39_contraction.py")).read(); SGN = 1; exec(_x[_x.index("def contract(r, Mb, M0, F, gnedin=None):"):_x.index('P("\\n=== checks")')])
def em1(lMb): return 10 ** (11.18 + 0.9 * (lMb - 10))
def share200(Mb): return 6.35 * Mb
# ---------------------------------------------------------- SPARC
T = {}
for l in open(os.path.join(INP, "sparc", "SPARC_Lelli2016c.mrt")):
    t = l.split()
    if len(t) == 19:
        try: T[t[0]] = dict(Inc=float(t[5]), L36=float(t[7]), MHI=float(t[13]), Vflat=float(t[15]), Q=float(t[17]))
        except ValueError: pass
GAL = []
for f_ in sorted(glob.glob(os.path.join(INP, "sparc", "rotmod", "*_rotmod.dat"))):
    n = os.path.basename(f_).replace("_rotmod.dat", ""); a = np.loadtxt(f_, comments="#", ndmin=2); m = T[n]
    if m["Q"] > 2 or m["Inc"] < 30 or len(a) < 3: continue
    GAL.append(dict(name=n, R=a[:, 0] * KPC, V=a[:, 1], eV=a[:, 2], Vg=a[:, 3], Vd=a[:, 4], Vb=a[:, 5], **m))
def gbar(g, U): return (np.abs(g["Vg"]) * g["Vg"] + U * np.abs(g["Vd"]) * g["Vd"] + 1.4 * U * np.abs(g["Vb"]) * g["Vb"]) * KMS2 / g["R"]
def Mbtot(g, U): return (U * g["L36"] + 1.33 * g["MHI"]) * 1e9
def coldg(g, U, mass, f):
    """Newtonian cold acceleration on g's radii. mass: em1 or share. f: response."""
    R = g["R"]; Mb = Mbtot(g, U); M200 = em1(math.log10(Mbtot(g, 0.5))) if mass == "em1" else share200(Mbtot(g, 0.5)); Rv = r200(M200)
    if f == 0: return G * Mc_native(M200, R) * MS / R ** 2
    rg = np.geomspace(R[0] * 0.05, Rv * 1.2, 300); M0 = Mc_native(M200, rg); Mbk = np.maximum.accumulate(np.maximum(gbar(g, U) * R ** 2 / G / MS, 0)); Mt = max(Mbk[-1], Mb)
    Mg = np.where(rg < R[0], Mbk[0] * (rg / R[0]) ** 2, np.interp(np.log(rg), np.log(R), Mbk)); o = rg > R[-1]; t = np.clip(np.log(rg[o] / R[-1]) / math.log(3), 0, 1); Mg[o] = np.exp(np.log(max(Mbk[-1], 1e-30)) * (1 - t) + np.log(Mt) * t); Mg = np.maximum.accumulate(Mg)
    Mf = contract(rg, Mg, M0, Mt / float(M0[-1]))[0]; return G * np.interp(np.log(R), np.log(rg), M0 + f * (Mf - M0)) * MS / R ** 2
def outer(g): return (g["R"] >= g["R"].max() * 2 / 3) & (g["V"] > 0)
def resid(g, U, a0, gc, reading):
    gb = np.maximum(gbar(g, U), 1e-20); gO = g["V"] ** 2 * KMS2 / g["R"]; p = law(gb, a0) + gc if reading == "N" else law(gb + gc, a0); return np.log10(gO / p), gO, gb
def binof(g):
    for i, (a, b) in enumerate(BINS):
        if a <= g["Vflat"] < b: return i
    return -1
BY = [[g for g in GAL if binof(g) == i] for i in range(6)]
def boot(v):
    v = np.asarray(v); r = np.random.default_rng(SEED); i = r.integers(0, len(v), (NB, len(v))); return float(np.median(v)), float(np.median(v[i], axis=1).std())
def inv_disc(a0, U):
    O = {}
    for i, gs in enumerate(BY):
        GN, GS, D = [], [], []
        for g in gs:
            d, gO, gb = resid(g, U, a0, 0.0, "N"); m = outer(g); GN.append(float(np.mean(((gO - law(gb, a0)) / gb)[m]))); GS.append(float(np.mean((lawinv(gO, a0) / gb - 1)[m]))); D.append(float(np.mean(d[m])))
        O[f"{BINS[i][0]}-{BINS[i][1]}"] = dict(n=len(gs), GN=boot(GN), GS=boot(GS), d=boot(D))
    return O
def dbin(gs, U, a0, mass, f, psi, rd, cache=None):
    D = []
    for g in gs:
        k = (g["name"], U, mass, f); gc = cache.get(k) if cache is not None else None
        if gc is None:
            gc = coldg(g, U, mass, f)
            if cache is not None: cache[k] = gc
        m = outer(g); D.append(float(np.mean(resid(g, U, a0, psi * gc, rd)[0][m])))
    return float(np.median(D))
def room(gs, U, a0, mass, f, rd, cache):
    D0 = [float(np.mean(resid(g, U, a0, 0.0, rd)[0][outer(g)])) for g in gs]; d0, s = boot(D0); fl = min(d0, 0.0) - 2 * s; psi = 0.0; lo, hi = 0.0, 1.0
    if dbin(gs, U, a0, mass, f, 1.0, rd, cache) >= fl: return dict(psi=1.0, floor=fl, d0=d0, s=s, capped=True)
    for _ in range(14):
        c = 0.5 * (lo + hi)
        if dbin(gs, U, a0, mass, f, c, rd, cache) >= fl: lo = c
        else: hi = c
    return dict(psi=lo, floor=fl, d0=d0, s=s, capped=False)
def rms_all(U, a0, mass, f, psi, rd, cache):
    r = []
    for g in GAL:
        k = (g["name"], U, mass, f); gc = cache.setdefault(k, coldg(g, U, mass, f)) if psi else 0.0; d = resid(g, U, a0, psi * gc if psi else 0.0, rd)[0]; r.append(d[(g["V"] > 0) & np.isfinite(d)])
    r = np.concatenate(r); return float(np.sqrt(np.mean(r * r)))
# ---------------------------------------------------------- LITTLE THINGS
LT = []
for r in csv.DictReader(open(os.path.join(INP, "little_things", "oh2015_table2.csv"))):
    if all(r[k].strip() != "" for k in ("Rmax_kpc", "V_kms", "Mgas_1e7Msun", "MSED_1e7Msun")): LT.append((float(r["Rmax_kpc"]) * KPC, float(r["V_kms"]), float(r["Mgas_1e7Msun"]) * 1e7, float(r["MSED_1e7Msun"]) * 1e7))
LT = np.array(LT)
def inv_lt(a0):
    R, V, g_, s = LT.T; gb = G * (g_ + s) * MS / R ** 2; gO = V ** 2 * KMS2 / R; E = np.log10(gO / law(gb, a0)); GN = (gO - law(gb, a0)) / gb; GS = lawinv(gO, a0) / gb - 1; gc = np.array([G * float(Mc_native(em1(math.log10(mb)), r_)) * MS / r_ ** 2 for r_, mb in zip(R, g_ + s)]); Ep = np.log10(gO / (law(gb, a0) + gc)); e0, se = boot(E); fl = min(e0, 0) - 2 * se; lo, hi = 0, 1
    for _ in range(14):
        c = (lo + hi) / 2; (lo, hi) = (c, hi) if np.median(np.log10(gO / (law(gb, a0) + c * gc))) >= fl else (lo, c)
    return dict(n=len(R), E=(e0, se), GN=boot(GN), GS=boot(GS), E_full=float(np.median(Ep)), psi=lo)
# ---------------------------------------------------------- X-COP
def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
XS = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0); XC = []
DX = os.path.join(REPO, "real_research", "data", "xcop")
for n in sorted(os.listdir(DX)):
    p_ = os.path.join(DX, n)
    if not (os.path.isdir(p_) and os.path.exists(os.path.join(p_, f"{n}_mstar.fits"))): continue
    with fits.open(os.path.join(p_, f"{n}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{n}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg5 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{n}_mstar.fits")) as h: st = h[2].data.copy()
    row = {x: (x * r5, li(hm["RADIUS"], hm["M_FORW"], x * r5), li(ga["RADIUS"] * rg5, ga["MGAS"], x * r5), li(st["RADIUS"], st["MSTAR"], x * r5)) for x in XS}; XC.append(dict(name=n, rows={x: v for x, v in row.items() if np.all(np.isfinite(v))}))
def xcop(a0, shift=0.0):
    O = {}; rho = {}
    for c in XC:
        prev = None
        for x in XS:
            if x not in c["rows"]: continue
            r, mh, mg, ms = c["rows"][x]; mh = mh * 10 ** shift; Rm = r * KPC; gb = G * (mg + ms) * MS / Rm ** 2; gO = G * mh * MS / Rm ** 2; L = law(gb, a0) * Rm ** 2 / G / MS; dMN = mh - L; dMS = lawinv(gO, a0) * Rm ** 2 / G / MS - (mg + ms); O.setdefault(x, []).append(dict(ratio=mh / L, dM=dMN, dMg=dMN / mg, GN=dMN / (mg + ms), GS=dMS / (mg + ms), dMS=dMS, r=r, mh=mh, mb=mg + ms))
            if prev is not None and x > prev[0]:
                for rd_, dm_, pm in (("N", dMN, prev[1]), ("S", dMS, prev[2])):
                    vol = 4 * math.pi / 3 * (r ** 3 - prev[3] ** 3) * 1e9; rho.setdefault((rd_, x), []).append(dict(rho=(dm_ - pm) / vol, r=math.sqrt(r * prev[3]), mh=mh))
            prev = (x, dMN, dMS, r)
    T_ = {}
    for x in XS:
        A = O[x]; f = lambda k: float(np.median([q[k] for q in A])); T_[x] = dict(n=len(A), r=f("r"), ratio=f("ratio"), dM=f("dM"), dMg=f("dMg"), GN=f("GN"), GN_s=float(np.std([q["GN"] for q in A], ddof=1) / math.sqrt(len(A))), GS=f("GS"), dMS=f("dMS"), mb=f("mb"), mh=f("mh"))
    Rt = {}
    for rd_ in "NS":
        xs_ = [x for x in XS[1:]]; r_ = [float(np.median([q["r"] for q in rho[(rd_, x)]])) for x in xs_]; v_ = [float(np.median([q["rho"] for q in rho[(rd_, x)]])) for x in xs_]; mh_ = [float(np.median([q["mh"] for q in rho[(rd_, x)]])) for x in xs_]; pos = [i for i, a in enumerate(v_) if a > 0]; sl = np.full(len(v_), np.nan); sl[pos] = np.gradient(np.log(np.array(v_)[pos]), np.log(np.array(r_)[pos])) if len(pos) > 1 else np.nan; cs = [math.sqrt(G * m * MS / (r * KPC) / (-s)) / 1e3 if (np.isfinite(s) and s < 0) else float("nan") for m, r, s in zip(mh_, r_, sl)]; shells = [q["rho"] for q in rho[(rd_, 1.0)]]
        Rt[rd_] = dict(x=xs_, r_kpc=r_, rho_Mspc3=list(v_), slope=sl.tolist(), c_implied=cs, last_shell_n_neg=int(sum(a < 0 for a in shells)), last_shell_mean=float(np.mean(shells)), last_shell_se=float(np.std(shells, ddof=1) / math.sqrt(len(shells))))
    return dict(table=T_, rho=Rt)
# ---------------------------------------------------------- main
RES["footings"] = {}
for ft in FEET:
    a0 = A0[ft]; R = {}; cache = {}; P(f"\n{'=' * 20} {ft} a0 {a0:.4e}; share {SHARE}")
    P("-- Part 1, SPARC, Gamma = M_x/M_b at outer third; median +- boot; N, S; d = law residual")
    R["disc"] = {}
    for U in (0.5, 0.35, 0.25):
        R["disc"][str(U)] = inv_disc(a0, U); P(f" U {U}:")
        for b, q in R["disc"][str(U)].items(): P(f"   {b:8s} n {q['n']:3d} d {q['d'][0]:+.3f}+-{q['d'][1]:.3f} Gamma_N {q['GN'][0]:+.3f}+-{q['GN'][1]:.3f} Gamma_S {q['GS'][0]:+.3f}+-{q['GS'][1]:.3f}")
    R["lt"] = inv_lt(a0); q = R["lt"]; P(f"-- LITTLE THINGS n {q['n']} E {q['E'][0]:+.3f}+-{q['E'][1]:.3f} Gamma_N {q['GN'][0]:+.3f}+-{q['GN'][1]:.3f} Gamma_S {q['GS'][0]:+.3f}+-{q['GS'][1]:.3f} E with EM1 native {q['E_full']:+.3f} psi room {q['psi']:.3f}")
    R["xcop"] = xcop(a0); R["xcop_m12"] = xcop(a0, -0.12)
    for lab, X_ in (("HSE", R["xcop"]), ("HSE-0.12", R["xcop_m12"])):
        P(f"-- X-COP {lab}: x r_kpc M/Mlaw dM(1e14) dM/Mg Gamma_N(+-) Gamma_S Gamma_N/share dM_S(1e14) phi_sys_N phi_sys_S (over share x M_b(<R500))")
        for x, q in X_["table"].items(): P(f"   {x:.1f} {q['r']:6.0f} {q['ratio']:.2f} {q['dM'] / 1e14:.2f} {q['dMg']:.2f} {q['GN']:.2f}+-{q['GN_s']:.2f} {q['GS']:.2f} {q['GN'] / SHARE:.2f} {q['dMS'] / 1e14:.2f} {q['dM'] / (SHARE * X_['table'][1.0]['mb']):.2f} {q['dMS'] / (SHARE * X_['table'][1.0]['mb']):.2f}")
        for rd in "NS":
            q = X_["rho"][rd]; P(f"   rho_x[{rd}] Msun/pc^3 " + " ".join(f"{a:.2e}" for a in q["rho_Mspc3"]) + " | slope " + " ".join(f"{a:+.2f}" for a in q["slope"]) + " | c_implied km/s " + " ".join(f"{a:.0f}" for a in q["c_implied"]) + f" | shell x 0.7-1: {q['last_shell_n_neg']} of 7 negative, mean {q['last_shell_mean']:.2e} +- {q['last_shell_se']:.2e}")
    LMr = json.load(open(os.path.join(RB, "LM1_law_missing_mass_map", "lm1_results.json")))[ft]; R["shear"] = {k: LMr[k] for k in ("Q_all", "Q_all_s", "Q_M1", "Q_M2", "Q_M3", "dDS_all", "dDS_all_s", "M2Dmin", "M2Dmin_s")}; R["groups"] = LMr["groups"]
    P("-- Shear stacks (LM1, read): R 0.18 0.26 0.38 0.56 0.81 1.18 1.71 2.49"); P("   Q all " + " ".join(f"{a:.1f}" for a in LMr["Q_all"])); P("   Q all / (share*1.034) " + " ".join(f"{a / (SHARE * 1.034):.2f}" for a in LMr["Q_all"]))
    for k in ("Q_M1", "Q_M2", "Q_M3"): P(f"   {k} " + " ".join(f"{a:.1f}" for a in LMr[k]))
    RC = np.array([0.18, 0.26, 0.38, 0.56, 0.81, 1.18, 1.71, 2.49]); iM = int(np.argmax(LMr["M2Dmin"])); Mi = LMr["M2Dmin"][iM]; RCl = [0.181, 0.263, 0.381, 0.556, 0.807, 1.176, 1.711, 2.491]; sh = [Mi / (math.pi * (RCl[j] * 1e6) ** 2) - LMr["dDS_all"][j] for j in (6, 7)]; R["sheet"] = dict(M2Dmax=Mi, R_at=RCl[iM], S_req=sh, s=[LMr["dDS_all_s"][6], LMr["dDS_all_s"][7]]); P(f"   Continuity: M2D_min peaks {Mi:.2e} at {RCl[iM]} Mpc; a mass that stopped there gives dDS {Mi / (math.pi * (RCl[6] * 1e6) ** 2):.1f}, {Mi / (math.pi * (RCl[7] * 1e6) ** 2):.1f} at 1.71, 2.49; measured {LMr['dDS_all'][6]:.1f}+-{LMr['dDS_all_s'][6]:.1f}, {LMr['dDS_all'][7]:.1f}+-{LMr['dDS_all_s'][7]:.1f}; so Sigma_x there at least {sh[0]:.1f}, {sh[1]:.1f} Msun/pc^2 (positive mass only; X57 A1: not a bound on shear alone)")
    q = R["groups"]; P(f"-- Groups (LM1, read): n {q['n']} d mean {q['d_mean']:+.3f} median {q['d_median']:+.3f}; dM/M_law {q['dMoverL_med']:.3f}; Gamma_N {q['dMoverB_med']:.2f}; lg M_b {q['lgMb_median']:.2f}, Re {q['Re_med']:.0f} kpc. Reading S (A^2-1 deep): {(1 + q['dMoverL_med']) ** 2 - 1:.2f}")
    Blr = json.load(open(os.path.join(RB, "BL1_blue_lens_halo_mass", "bl1_results.json")))["k"]["law"][ft]; gm = 10 ** -12.6; gl = float(law(gm, a0)); R["lens"] = {}
    for c_ in ("blue", "red", "all"):
        A, s = Blr[c_]["A"], Blr[c_]["sA"]; g2 = lambda aa: (aa - 1) * gl / gm; S2 = lambda aa: float(lawinv(aa * gl, a0)) / gm - 1; R["lens"][c_] = dict(A=A, s=s, GN=g2(A), GN_up=g2(A + 2 * s), GS=S2(A), GS_up=S2(A + 2 * s)); P(f"-- Lens {c_}: A {A:.3f}+-{s:.3f}; at window mid g_bar 10^-12.6: Gamma_N {g2(A):+.2f} (2s up {g2(A + 2 * s):+.2f}), Gamma_S {S2(A):+.2f} (2s up {S2(A + 2 * s):+.2f})")
    Bu = json.load(open(os.path.join(RB, "UX6_gas_term_bullet", "ux6_results.json")))["rows"][f"LAW|{ft}"]["M300"]; O3 = (3.5e14, 2.3e14); R["bullet"] = dict(law=Bu, need=[O3[i] - Bu[i] for i in (0, 1)]); P(f"-- Bullet M300 law {Bu[0]:.3e}, {Bu[1]:.3e}; required cold on the galaxies {O3[0] - Bu[0]:.3e}, {O3[1] - Bu[1]:.3e}; +-15 % of observed (X32's PROVISIONAL)")
    # T2, T3, T4
    P("-- T2/T3 room psi: share of native at EM1 mass fitting the floor; rows f_Q 0, 0.872; U 0.5, 0.25; N and S"); R["room"] = {}
    for U in (0.5, 0.25):
        for f in (0.0, FQ):
            for rd in "NS":
                k = f"U{U}|f{f}|{rd}"; R["room"][k] = {}; s_ = []
                for i, gs in enumerate(BY):
                    q = room(gs, U, a0, "em1", f, rd, cache); R["room"][k][f"{BINS[i][0]}-{BINS[i][1]}"] = q; s_.append(f"{q['psi']:.3f}" + ("+" if q["capped"] else ""))
                P(f"   {k:18s} " + " ".join(s_))
    P("-- T4 double count at psi 1: excess in dex against law, dV km/s at R_last, Upsilon that restores d = 0 (common in bin; <0.05 if none)"); R["T4"] = {}
    for mass in ("em1", "share"):
        for f in (0.0, FQ):
            for rd in "NS":
                k = f"{mass}|f{f}|{rd}"; R["T4"][k] = {}; s_ = []
                for i, gs in enumerate(BY):
                    d0 = dbin(gs, 0.5, a0, mass, f, 0.0, rd); d1 = dbin(gs, 0.5, a0, mass, f, 1.0, rd, cache); V = float(np.median([np.mean(g["V"][outer(g)]) for g in gs])); dV = V * (10 ** (-(d1 - d0) / 2) - 1); Us = 0.0
                    for U in np.round(np.arange(0.5, 0.0499, -0.05), 2):
                        if dbin(gs, float(U), a0, mass, f, 1.0, rd, cache) >= 0: Us = float(U); break
                    R["T4"][k][f"{BINS[i][0]}-{BINS[i][1]}"] = dict(d0=d0, d1=d1, dV=dV, U=Us); s_.append(f"{d1 - d0:+.3f}/{dV:+.0f}/{Us if Us else '<.05'}")
                P(f"   {k:16s} " + "  ".join(s_))
    R["rms"] = dict(law_U5=rms_all(0.5, a0, "em1", 0.0, 0.0, "N", cache));
    for mass in ("em1", "share"):
        for f in (0.0, FQ):
            for rd in "NS": R["rms"][f"{mass}|f{f}|{rd}"] = rms_all(0.5, a0, mass, f, 1.0, rd, cache)
    P("-- Pooled unweighted rms at U 0.50/0.70, every point: " + json.dumps({k: round(v, 4) for k, v in R["rms"].items()}))
    # FG1-style path: per-galaxy Upsilon, weighted rms, median U, tilt
    UPS = np.round(np.arange(.30, 1.2000001, .01), 2); ULO = np.round(np.arange(.05, 1.2000001, .01), 2)
    def path(mass, f, rd, psi, grid):
        wr2, ws, Yb, Vf = [], [], [], []
        for g in GAL + []:
            gO = g["V"] ** 2 * KMS2 / g["R"]; gc = (coldg(g, 0.5, mass, f) if psi else 0.0) * psi; W = 1 / (np.maximum(g["eV"], 1) / np.maximum(g["V"], 1)) ** 2; A = []; B = []
            for U in grid:
                gb = gbar(g, float(U)); ok = (gb > 0) & (gO > 0) & (g["V"] > 0); p = (law(np.maximum(gb, 1e-30), a0) + gc) if rd == "N" else law(np.maximum(gb, 1e-30) + gc, a0); r = np.where(ok, np.log10(np.where(gO > 0, gO, 1.) / p), 0.); A.append(float((W * r * r * ok).sum())); B.append(float((W * ok).sum()))
            A = np.array(A); B = np.array(B); q = np.where(B > 0, A / np.where(B > 0, B, 1), np.inf)
            if not np.isfinite(q).any(): continue
            i = int(np.argmin(q)); wr2.append(A[i]); ws.append(B[i]); Yb.append(grid[i]); Vf.append(g["Vflat"])
        Yb = np.array(Yb); Vf = np.array(Vf); lo = (Vf > 0) & (Vf < 100); hi = Vf > 150; return dict(rms=math.sqrt(sum(wr2) / sum(ws)), U=float(np.median(Yb)), tilt=float(np.median(Yb[lo]) - np.median(Yb[hi])), byV=[float(np.median(Yb[(Vf >= a) & (Vf < b)])) for a, b in BINS], at_floor=float(np.mean(Yb <= grid[0])))
    def fixedU(mass, f, rd, psi):
        wr2, ws = 0.0, 0.0
        for g in GAL:
            gO = g["V"] ** 2 * KMS2 / g["R"]; W = 1 / (np.maximum(g["eV"], 1) / np.maximum(g["V"], 1)) ** 2; gb = gbar(g, .5); ok = (gb > 0) & (g["V"] > 0); gc = (coldg(g, .5, mass, f) if psi else 0.0) * psi; p = (law(np.maximum(gb, 1e-30), a0) + gc) if rd == "N" else law(np.maximum(gb, 1e-30) + gc, a0); r = np.where(ok, np.log10(np.where(gO > 0, gO, 1.) / p), 0.); wr2 += float((W * r * r * ok).sum()); ws += float((W * ok).sum())
        return math.sqrt(wr2 / ws)
    R["path"] = {}; P("-- Per-galaxy Upsilon path (Q<=2 only, contraction held at U 0.5): rms, median U, tilt lo-hi, fixed-U 0.5/0.7 weighted rms; U by V_flat bin; grid floor 0.30, then 0.05")
    for k, (mass, f, rd, psi) in {"law": ("em1", 0.0, "N", 0.0), "em1|f0|N": ("em1", 0.0, "N", 1.0), "em1|fQ|N": ("em1", FQ, "N", 1.0), "em1|f0|S": ("em1", 0.0, "S", 1.0), "em1|fQ|S": ("em1", FQ, "S", 1.0), "share|f0|N": ("share", 0.0, "N", 1.0), "share|fQ|N": ("share", FQ, "N", 1.0), "share|f0|S": ("share", 0.0, "S", 1.0), "share|fQ|S": ("share", FQ, "S", 1.0)}.items():
        a_ = path(mass, f, rd, psi, UPS); b_ = path(mass, f, rd, psi, ULO); fx = fixedU(mass, f, rd, psi); R["path"][k] = dict(g30=a_, g05=b_, fixedU=fx); P(f"   {k:12s} .30: rms {a_['rms']:.4f} U {a_['U']:.2f} tilt {a_['tilt']:+.2f} floor {a_['at_floor']:.2f} | .05: rms {b_['rms']:.4f} U {b_['U']:.2f} tilt {b_['tilt']:+.2f} byV " + " ".join(f"{u:.2f}" for u in b_['byV']) + f" | fixed-U rms {fx:.4f}")
    # P1 sound speed
    P("-- P1: isothermal c in the galaxy's log potential, bg rho_x, R_out 1 Mpc. c_min so M_x(<R_last)/M_b <= room; room = median + 2 sigma Gamma_N at U 0.5, at least 0.02"); R["P1"] = {}
    rbar = RX0 * MPC ** 3 / MS  # Msun/Mpc^3
    def Mx(V, c, Rl_kpc):
        n = V ** 2 / c ** 2; rr = np.geomspace(Rl_kpc * 1e-2, Rl_kpc, 200) / 1e3; rho = rbar * np.exp(np.minimum(n * np.log(1.0 / rr), 600)); return float(np.trapz(4 * np.pi * rr ** 3 * rho, np.log(rr)))
    for i, gs in enumerate(BY):
        q = R["disc"]["0.5"][f"{BINS[i][0]}-{BINS[i][1]}"]; rm = max(q["GN"][0] + 2 * q["GN"][1], 0.02); C = []
        for g in gs:
            Rl = g["R"].max() / KPC; Mb_ = max(float(gbar(g, 0.5)[-1] * g["R"][-1] ** 2 / G / MS), 1e5); lo, hi = 1.0, 5000.0
            for _ in range(40):
                c = math.sqrt(lo * hi); (lo, hi) = (lo, c) if Mx(g["Vflat"], c, Rl) <= rm * Mb_ else (c, hi)
            C.append(hi)
        C = np.array(C); V_ = np.array([g["Vflat"] for g in gs]); R["P1"][f"{BINS[i][0]}-{BINS[i][1]}"] = dict(room=rm, c=float(np.median(C)), cmax=float(C.max()), c_over_V=float(np.median(C / V_))); P(f"   {BINS[i]} room {rm:.3f} c_min median {np.median(C):.0f} max {C.max():.0f} km/s; c/V {np.median(C / V_):.2f}")
    top = R["P1"]["250-400"]["cmax"]; med = R["P1"]["150-200"]["c"]; ci = [a for a in R["xcop"]["rho"]["N"]["c_implied"] if np.isfinite(a)]; P(f"   Window: discs need c >= {top:.0f} (top bin max), {R['P1']['250-400']['c']:.0f} (top median), {med:.0f} (150-200 median), X22 asks 190/201; X-COP's required profile implies {min(ci):.0f}-{max(ci):.0f} km/s; ratio over x {max(ci) / min(ci):.2f}")
    R["P1w"] = dict(top=top, topmed=R["P1"]["250-400"]["c"], med=med, ci=ci)
    # P4 energy
    P("-- P4: energy to lift the EM1 native share out of R_last and out of R200, log potential at V_flat, per E_SN = 1e49 erg/Msun star, perfect delivery"); R["P4"] = {}
    for i, gs in enumerate(BY):
        E1, E2 = [], []
        for g in gs:
            M200 = em1(math.log10(Mbtot(g, .5))); Rv = r200(M200); Rl = g["R"].max(); rr = np.geomspace(Rl * 1e-3, Rl, 200); Mc = Mc_native(M200, rr); Mst = max(.5 * g["L36"] * 1e9, 1e4); V2 = g["Vflat"] ** 2 * KMS2; dm = np.gradient(Mc); e1 = float(np.sum(dm * V2 * np.log(Rl / rr))) * MS * 1e7; ES = 1e49 * Mst; Mo = Mc[-1]; e2 = e1 + Mo * V2 * math.log(max(Rv / Rl, 1)) * MS * 1e7; E1.append(e1 / ES); E2.append(e2 / ES)
        R["P4"][f"{BINS[i][0]}-{BINS[i][1]}"] = dict(eps_Rlast=float(np.median(E1)), eps_R200=float(np.median(E2))); P(f"   {BINS[i]} eps(out of R_last) {np.median(E1):.3f} eps(out of R200) {np.median(E2):.3f}")
    # P3 cap
    rhoc = max(R["xcop"]["rho"]["N"]["rho_Mspc3"]); P(f"-- P3: density cap at X-COP's largest required rho_x {rhoc:.2e} Msun/pc^3; psi-equivalent M_x,cap/M_x,native at R_last, and residual shift"); R["P3"] = dict(rho_cap=rhoc, bins={})
    for i, gs in enumerate(BY):
        fr, dd = [], []
        for g in gs:
            M200 = em1(math.log10(Mbtot(g, .5))); Rs = g["R"]; rg = np.geomspace(Rs[0] * .02, Rs[-1], 400); Mc = Mc_native(M200, rg); rho = np.gradient(Mc, rg) / (4 * math.pi * rg ** 2) * MS / MS * (PC ** 3); rc2 = np.minimum(rho, rhoc); Mcap = np.cumsum(4 * math.pi * rg ** 2 * rc2 / PC ** 3 * np.gradient(rg)); gc = G * np.interp(Rs, rg, Mcap) * MS / Rs ** 2; fr.append(float(Mcap[-1] / Mc[-1])); m = outer(g); dd.append(float(np.mean(resid(g, .5, a0, gc, "N")[0][m])))
        R["P3"]["bins"][f"{BINS[i][0]}-{BINS[i][1]}"] = dict(frac=float(np.median(fr)), d=float(np.median(dd))); P(f"   {BINS[i]} M_cap/M_native {np.median(fr):.3f}; d {np.median(dd):+.3f} (law {R['disc']['0.5'][f'{BINS[i][0]}-{BINS[i][1]}']['d'][0]:+.3f})")
    # P2 density
    dens = {}
    for i, gs in enumerate(BY):
        v = []
        for g in gs:
            M200 = em1(math.log10(Mbtot(g, .5))); Rl = g["R"].max(); rr = np.array([Rl * .9, Rl * 1.1]); v.append((Mc_native(M200, rr)[1] - Mc_native(M200, rr)[0]) * PC ** 3 / (4 * math.pi / 3 * (rr[1] ** 3 - rr[0] ** 3)))
        dens[f"{BINS[i][0]}-{BINS[i][1]}"] = float(np.median(v))
    R["P2"] = dict(disc_rho_Rlast=dens); P("-- P2: native rho_x at R_last, Msun/pc^3, by bin: " + " ".join(f"{v:.2e}" for v in dens.values()))
    RES["footings"][ft] = R
# ---------------------------------------------------------- footing-free
P("\n" + "=" * 20 + " footing-free")
rho0 = RX0 / MSPC3; Z = lambda r: (r / rho0) ** (1 / 3) - 1; rho = lambda z: rho0 * (1 + z) ** 3; RES["rho0"] = rho0
P(f"rho_x0 {rho0:.3e} Msun/pc^3 = {RX0:.3e} kg/m^3; rho_x(1090) {RX0 * 1091 ** 3:.3e} kg/m^3 = {rho(1090):.2f} Msun/pc^3; rho_x(3e4) {rho(3e4):.2e} Msun/pc^3")
Xr = RES["footings"]["canonical"]["xcop"]["rho"]["N"]["rho_Mspc3"]; Dr = RES["footings"]["canonical"]["P2"]["disc_rho_Rlast"]
P("Crossing z of cosmic rho_x: X-COP required " + " ".join(f"{Z(a):.0f}" if a > 0 else "neg" for a in Xr) + "; native disc at R_last " + " ".join(f"{Z(a):.0f}" for a in Dr.values()))
def kJ(z, c, om=None): a = 1 / (1 + z); return a * math.sqrt(1.5 * OMm * (1 + z) ** 3) * 100 * H / c / H  # comoving h/Mpc
KL = 2 * math.pi / 1.36; RES["growth"] = {}
Cw = {ft: RES["footings"][ft]["P1w"] for ft in FEET}
for ft in FEET:
    c0 = Cw[ft]["topmed"]; rows = {}
    P(f"-- growth, {ft}, c at z 0 = {c0:.0f} km/s (top-bin median) and X22's 190/201. Forest line k {KL:.2f} h/Mpc (X22). Jeans k h/Mpc at z 3, 2, 0:")
    for nm, fn in (("constant", lambda z: c0), ("redshifting c~(1+z)", lambda z: c0 * (1 + z)), ("barotrope c^2~rho^0.5", lambda z: c0 * (1 + z) ** 0.75)):
        rows[nm] = [kJ(z, fn(z)) for z in (3, 2, 0)]; P(f"   {nm:24s} " + " ".join(f"{a:.3f}" for a in rows[nm]) + f"; short of the line at z 3 by x{KL / rows[nm][0]:.1f}")
    cz3 = kJ(3, 1.0) / KL; p = math.log(c0 / cz3) / math.log(4); rows["c_allowed_z3"] = cz3; rows["p_needed"] = p; rows["p_x22"] = math.log(c0 / 13) / math.log(4); P(f"   c allowed at z 3 by k_J >= line: {cz3:.0f} km/s (X22's stricter 6-13); needs dln c/dln a >= {p:.2f}, or {rows['p_x22']:.2f} on X22's 13 km/s. Sign: every thermal or barotropic row has it <= 0.")
    frac = 5.35 * 0.5 * (c0 / CK) ** 2; sn = 1e49 / (MS * 1e3 * (CK * 1e5) ** 2); rows["E_req"] = frac; rows["E_SN_full"] = sn; P(f"   Heating cost per baryon rest mass 5.35 c^2/2 = {frac:.2e}; E_SN if all baryons became stars {sn:.2e}, ratio {sn / frac:.2f}; at f_star 0.05 (PROVISIONAL) {0.05 * sn / frac:.3f}; times delivery 0.003 (CM1) {0.05 * .003 * sn / frac:.1e}")
    mj = lambda z, c: 4 * math.pi / 3 * (OMm * 2.775e11 * H * H) * (math.pi / (kJ(z, c) * H)) ** 3; rows["M_J_z0"] = mj(0, c0); rows["M_J_z0_x22"] = mj(0, 190.0); P(f"   Jeans mass at z 0, constant c: {mj(0, c0):.2e} Msun (c {c0:.0f}), {mj(0, 190.0):.2e} (c 190); LM1's M1 tercile needs cold at lg M_gas 12.5"); cr = {"redshifting": c0 * 1091, "barotrope": c0 * 1091 ** 0.75, "constant": c0}; rows["c2_1090"] = {k: (v / CK) ** 2 for k, v in cr.items()}; P("   (c/c_light)^2 at z 1090, against UX2's pointer 1e-6: " + " ".join(f"{k} {(v / CK) ** 2:.1e}" for k, v in cr.items())); rows["mach"] = 4700 / c0; P(f"   Bullet: Mach 4700/c = {4700 / c0:.1f} (4700 km/s PROVISIONAL); on-gas control Z -5.12 (UX6 K6): a fluid that shocks sits with the gas")
    RES["growth"][ft] = rows
# band barotrope
Dmin, Dmax = min(Dr.values()), max(Dr.values()); zb = Z(Dmax), Z(Dmin); Xm = max(Xr); dln = math.log((1 + zb[0]) / (1 + zb[1])); ck = Cw["canonical"]["med"]; kb = kJ(0.5 * (zb[0] + zb[1]), ck); P(f"Band rule: pressure only for rho in native disc range {Dmin:.2e}-{Dmax:.2e}; X-COP's top {Xm:.2e}: X-COP required at x 0.15-0.25 is {Xr[0]:.2e}, {Xr[1]:.2e}; band {'overlaps' if Dmin < Xm else 'clear of'} cluster need. Cosmic mean crosses it z {zb[1]:.0f}-{zb[0]:.0f}, dln a {dln:.2f}, growth lost x{math.exp(dln):.2f} at k > k_J = {kb:.2f} h/Mpc (c {ck:.0f}); forest line asks k {KL:.2f}, T^2 >= 0.9 means amplitude within 5 %.")
RES["band"] = dict(Dmin=Dmin, Dmax=Dmax, Xmax=Xm, z=zb, growth_lost=math.exp(dln), kJ=kb)
# ---------------------------------------------------------- checks
P("\n=== checks")
Tc = xcop(9.3603e-11)["table"] if MUT else RES["footings"]["canonical"]["xcop"]["table"]; Tu = RES["footings"]["canonical"]["xcop"]["table"]; rec = {0.1: (3.51, 8.5), 0.2: (3.39, 8.0), 0.3: (3.18, 6.7), 0.5: (2.66, 5.2), 0.7: (2.16, 3.9), 1.0: (1.62, 2.3)}; e = max(max(abs(Tu[x]["ratio"] / rec[x][0] - 1), abs(Tu[x]["dMg"] / rec[x][1] - 1)) for x in rec)
LMX = json.load(open(os.path.join(RB, "LM1_law_missing_mass_map", "lm1_results.json")))["canonical"]["xcop"]; ee = max(abs(Tu[float(k)]["dMg"] / LMX[k]["ratio"] - 1) for k in LMX if float(k) in Tu); check("K1", max(ee, 0) <= 0.01, f"X-COP dM/Mg against LM1's JSON max rel {ee:.2e} (printed-table rounding {e:.3f}, not graded)")
r1090 = RX0 * 1091 ** 3; check("K2", abs(r1090 / 2.92e-18 - 1) <= 3.5e-3 and abs(RX0 / 2.249e-27 - 1) < 1e-3, f"rho_x(1090) {r1090:.4e} vs UX2 2.92e-18; rho_x0 {RX0:.4e} vs 2.249e-27")
sys.path.insert(0, os.path.join(RB, "UX3_cluster_gas_term")); import ux3_common as UC; S0 = UC.sparc(); rr = {ft: float(np.sqrt(np.mean(np.log10(S0[0][:, 1] / UC.law(S0[0][:, 0], 9.3603e-11 if ft == "canonical" else 1.1312e-10)) ** 2))) for ft in FEET}; check("K3", abs(rr["canonical"] - .186) < .002 and abs(rr["alt"] - .187) < .002, f"UX3's law even rms {rr}; this lane's own galaxy selection is Q<=2; LT E canonical {RES['footings']['canonical']['lt']['E'][0]:+.3f} vs record -0.025")
Bk = json.load(open(os.path.join(RB, "UX6_gas_term_bullet", "ux6_results.json")))["rows"]["LAW|canonical"]["M300"]; check("K4", abs(Bk[0] / 1.11e14 - 1) < .01 and abs(Bk[1] / .73e14 - 1) < .01, f"Bullet law row {Bk}")
rS = np.geomspace(10, 1000, 50); sig = 500.0; Mt = 2 * (sig * 1e3) ** 2 * rS * KPC / G / MS; sl = -2.0; cS = np.sqrt(G * Mt * MS / (rS * KPC) / 2) / 1e3; check("K5", abs(cS[10] / sig - 1) < .01, f"SIS sigma {sig} returns {cS[10]:.1f} by the Jeans form used")
M0 = Mc_native(1e13, np.array([0.1, 1.0]) * r200(1e13)); check("K6", abs(M0[1] / (FC * 1e13) - math.exp(lnm(13.0)[np.searchsorted(LX, 0.0)])) < .05, f"native reader M_c(R200)/(fc M200) {M0[1] / (FC * 1e13):.3f}, M_c(0.1R200)/M_c(R200) {M0[0] / M0[1]:.3f}")
kk = kJ(0, 100.0); hand = math.sqrt(1.5 * OMm) * 100 * H / 100 / H; check("K7", abs(kk / hand - 1) < 1e-9, f"k_J(z 0, c 100) {kk:.4f} h/Mpc; hand {hand:.4f}")
rg = np.geomspace(1e19, 1e23, 300); M0_ = Mc_native(1e12, rg); Mfz = contract(rg, 0 * rg, M0_, 0.0)[0]; check("K8", np.max(np.abs(Mfz / M0_ - 1)[5:-5]) < 1e-3, f"contract zero baryons max rel {np.max(np.abs(Mfz / M0_ - 1)[5:-5]):.2e}")
RES["checks"] = CHK; json.dump(RES, open(os.path.join(HERE, f"mc1_results{TAG}.json"), "w"), indent=1, default=float, sort_keys=True); open(os.path.join(HERE, f"mc1{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(c[1] for c in CHK) else 1)
