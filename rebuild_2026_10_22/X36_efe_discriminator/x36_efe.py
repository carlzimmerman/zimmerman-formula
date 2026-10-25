#!/usr/bin/env python3
"""X36_efe_discriminator: is X33's large-SPARC residual-vs-log e_ext trend reproduced by (a) the law's exact AQUAL EFE (P4
machinery), by (b) route E's emergent cold-dark-energy halos (EM1's model, no EFE term), by neither, or by a confound?

Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (d8651cafc3, committed alone before any script or number).
kappa = 1/2 FITTED.  Footings never pooled.  No dark-matter particle.  Not "theory closed".

Run:   PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x36_efe.py                 -> x36_efe.out, x36_efe_results.json
       X36_MUTATE=1 (same command)  -> e_ext shuffled within T bins + EFE off in (a); K_repro and K_efe must FAIL (exit 1)
Step 0a needs the scratch EM1 rerun in step0_em1/ (see README).
"""
import os, sys, io, csv, json, math, time, contextlib, resource, warnings
sys.dont_write_bytecode = True                                   # never write __pycache__ into other lanes
import numpy as np
from scipy.stats import spearmanr, t as TDIST
from classy import Class

warnings.filterwarnings("ignore", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.dirname(HERE)
REPO = os.path.dirname(RB)
DATA = os.path.join(REPO, "real_research", "data")
MUT = os.environ.get("X36_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
T0_ = time.time()
OUTL = []
RES = dict(lane="X36_efe_discriminator", criteria="d8651cafc3", mutate=MUT, checks={}, step0={})
FOOTS = ("canonical", "alt")
FK = {"canonical": "can", "alt": "alt"}
LN10 = math.log(10.0)
G, MSUN, KPC_S, MPC = 6.67430e-11, 1.98847e30, 3.0857e19, 3.0857e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
GE_CHAE = 1.2e-10
B_BOOT = 2000
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
NODES = np.array([0.30, 0.40, 0.50, 0.60, 0.75, 0.90, 1.05, 1.20])
LM = np.round(np.arange(8.0, 14.0001, 0.02), 2)

with contextlib.redirect_stdout(io.StringIO()):
    sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
    import CFG4_common as C4  # noqa: E402  (read only: the footings)
assert all(abs(float(C4.A0[f]) - A0[f]) < 1e-15 for f in FOOTS)
sys.path.insert(0, os.path.join(RB, "P4_v3_galaxy_tiles"))
import p4_solver as S  # noqa: E402  (read only)


def P(s=""):
    print(s, flush=True); OUTL.append(str(s))


def check(key, ok, value, detail=""):
    RES["checks"][key] = dict(ok=bool(ok), value=value, detail=detail)
    P(f"{key} {'PASS' if ok else 'FAIL'}  {value}  {detail}")


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9


def nu1(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def jl(p):
    return json.load(open(p))


# ============================================================================ S0a: EM1 scratch rerun vs EM1's committed JSONs
P("=== STEP 0")
EMD = os.path.join(RB, "EM1_emergent_dust_law"); SCR = os.path.join(HERE, "step0_em1")
s0a = {}; oka = True
for tag_, fn in (("default", "em1_emergent_results.json"), ("ups05", "em1_emergent_results_UPS05.json")):
    ref = jl(os.path.join(EMD, fn)); mine = jl(os.path.join(SCR, fn))
    oka &= all(v["ok"] for v in mine["checks"].values())
    for bg in ("A_c2b_refit", "B_cfg886_bg"):
        r, m = ref["rows"][bg]["R1"], mine["rows"][bg]["R1"]
        d = dict(rms=(m["rms"], r["rms"]), U=(m["U_median"], r["U_median"]), a=(m["a"], r["a"]), b=(m["b"], r["b"]),
                 g_model=(10 ** mine["rows"][bg]["R3"]["model"]["lg"], 10 ** ref["rows"][bg]["R3"]["model"]["lg"]))
        oka &= abs(d["rms"][0] - d["rms"][1]) <= 1e-4 and d["U"][0] == d["U"][1] and d["a"][0] == d["a"][1] and d["b"][0] == d["b"][1]
        oka &= abs(d["g_model"][0] / d["g_model"][1] - 1) <= 1e-3
        s0a[f"{tag_}|{bg}"] = d
    for f in FOOTS:
        d = (mine["law"][f]["rms"], ref["law"][f]["rms"]); s0a[f"{tag_}|law|{f}"] = d
        oka &= abs(d[0] - d[1]) <= 1e-4
RES["step0"]["S0a"] = s0a
check("S0a", oka, "; ".join(f"{k}: " + (", ".join(f"{kk} {v[0]:.4g}/{v[1]:.4g}" for kk, v in d.items()) if isinstance(d, dict) else f"{d[0]:.5f}/{d[1]:.5f}")
                            for k, d in s0a.items()), "(mine / EM1 committed)")

# ============================================================================ atlas, X33 findings, S0b
ATL = list(csv.DictReader(open(os.path.join(RB, "X33_system_atlas", "x33_atlas.csv"))))
X33F = jl(os.path.join(RB, "X33_system_atlas", "x33_findings.json"))
SP = {r["id"]: r for r in ATL if r["class"] == "SPARC"}
fl = lambda s: float(s) if s not in ("", "NaN", "nan") else float("nan")
s0b = {}; okb = True
for f in FOOTS:
    for scope, sel in (("SPARC:large", lambda r: r["subclass"] == "large"), ("SPARC", lambda r: True)):
        rows = [r for r in SP.values() if sel(r) and np.isfinite(fl(r["e_ext"])) and np.isfinite(fl(r[f"resid_dex_{FK[f]}"]))]
        rho = spearmanr(np.log10([fl(r["e_ext"]) for r in rows]), [fl(r[f"resid_dex_{FK[f]}"]) for r in rows])[0]
        ref = X33F["footings"][f]["correlations"][f"{scope}|log e_ext"]
        s0b[f"{f}|{scope}"] = dict(n=len(rows), rho=float(rho), ref_n=ref["n"], ref_rho=ref["rho"])
        okb &= len(rows) == ref["n"] and abs(rho - ref["rho"]) <= 1e-9
RES["step0"]["S0b"] = s0b
check("S0b", okb, "; ".join(f"{k} N {v['n']} rho {v['rho']:+.4f} (X33 {v['ref_rho']:+.4f})" for k, v in s0b.items()))

# ============================================================================ SPARC (P4's loader, verbatim)
def load_sparc_own():
    d_ = os.path.join(DATA, "sparc_data"); gal = []
    for f in sorted(os.listdir(d_)):
        if not f.endswith("_rotmod.dat"):
            continue
        try:
            d = np.genfromtxt(os.path.join(d_, f), comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        gal.append(dict(name=f.replace("_rotmod.dat", ""), R=d[:, 0], Vobs=d[:, 1], eV=d[:, 2], Vgas=d[:, 3], Vdisk=d[:, 4], Vbul=d[:, 5]))
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
    tab = {}
    for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        tok = line.split()
        if len(tok) != 19:
            continue
        try:
            vals = [float(t) for t in tok[1:18]]
        except ValueError:
            continue
        row = dict(zip(keys, vals))
        for k in ("T", "fD", "Q"):
            row[k] = int(row[k])
        tab[tok[0]] = row
    for g_ in gal:
        g_["meta"] = tab.get(g_["name"])
    return gal


def gal_arrays(q, ups):
    R = q["R"] * KPC_S
    VB2 = np.sign(q["Vgas"])[:, None] * q["Vgas"][:, None] ** 2 + ups[None, :] * q["Vdisk"][:, None] ** 2 + 1.4 * ups[None, :] * q["Vbul"][:, None] ** 2
    GB = VB2 * 1e6 / R[:, None]
    GO = ((q["Vobs"] * 1e3) ** 2 / R)[:, None] * np.ones_like(GB)
    OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (q["Vobs"] > 0)[:, None]
    W = (1.0 / (np.clip(q["eV"], 1, None) / np.clip(q["Vobs"], 1, None)) ** 2)
    return GB, GO, OK, W


def chi2_offset(r, sig, s2):
    w = 1.0 / sig ** 2
    a = np.sum(w * r * r, axis=0); b = np.sum(w * r, axis=0); c = np.sum(w, axis=0)
    return a - s2 * b * b / (1.0 + s2 * c)


def sparc_mass_fun(q, ups, a0):
    R = q["R"]
    vb2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + ups * q["Vdisk"] ** 2 + 1.4 * ups * q["Vbul"] ** 2
    cfac = 1e6 / KPC_S / a0
    Mk = cfac * vb2 * R
    def M(r):
        r = np.asarray(r, float)
        v = np.interp(r, R, vb2)
        out = cfac * v * r
        out = np.where(r < R[0], Mk[0] * (r / R[0]) ** 3, out)
        out = np.where(r > R[-1], Mk[-1], out)
        return out
    return M, float(Mk[-1])


def ratio_solve(Mfun, Mt, ge, Lam_kpc, r_eval, rmax, r_in, nper=20, Nt=16, align=True):
    re_ = S.log_edges(r_in, S.r_out_for(Mt, ge, rmax), nper, align=float(np.min(r_eval)) if align else None)
    gA = S.Grid(re_, S.theta_edges(Nt if ge > 0 else 1, full=True))
    prA = S.Problem(gA, gA.rho_spherical(Mfun), Mt, ge, Lam=Lam_kpc); prA.solve()
    rf, mono, ring, gc = gA.radial_profiles(prA.Phi)
    gB = S.Grid(re_, S.theta_edges(1, full=True))
    prB = S.Problem(gB, gB.rho_spherical(Mfun), Mt, 0.0); prB.solve()
    rfB, monoB, _, _ = gB.radial_profiles(prB.Phi)
    base = gB.at_r(rfB, monoB, r_eval)
    return [gA.at_r(rf, p_, r_eval) / base for p_ in (mono, ring, gc)], (gA, prA, gB, prB)


def sparc_solve(q, ups, a0, ge, Lam_kpc, nper=20, Nt=16):
    M, Mtot = sparc_mass_fun(q, ups, a0)
    R = q["R"]
    rats, objs = ratio_solve(M, max(Mtot, 1e-8), ge, Lam_kpc, R, R[-1], R[0] / 30.0, nper=nper, Nt=Nt)
    gN = M(R) / R ** 2
    galg = np.where(gN > 0, S.g_from_gN(np.abs(gN)), 1e-300)
    return [np.log10(np.maximum(galg * rt, 1e-300) * a0) for rt in rats], objs


def interp_nodes(lg_nodes):
    x = np.log(NODES); xf = np.log(UPS)
    out = np.empty((lg_nodes.shape[1], len(UPS)))
    for k in range(lg_nodes.shape[1]):
        out[k] = np.interp(xf, x, lg_nodes[:, k])
    return out


def fit_sample(GALS, LGP):
    rows = []
    for q in GALS:
        GB, GO, OK, W = gal_arrays(q, UPS)
        lgp = LGP[q["name"]]
        r = np.where(OK, np.log10(np.where(OK, GO, 1.0)) - lgp, 0.0)
        Wm = np.where(OK, W[:, None], 0.0)
        mse = (Wm * r * r).sum(0) / np.maximum(Wm.sum(0), 1e-300)
        i_rms = int(np.argmin(mse))
        rows.append(dict(name=q["name"], U_rms=float(UPS[i_rms]), wsum=float(Wm[:, i_rms].sum()), wr2=float((Wm[:, i_rms] * r[:, i_rms] ** 2).sum())))
    return rows


def pooled(rows):
    return dict(N=len(rows), rms=math.sqrt(sum(x["wr2"] for x in rows) / sum(x["wsum"] for x in rows)),
                U_median=float(np.median([x["U_rms"] for x in rows])))


GALS = load_sparc_own()
NG = len(GALS)
GBYN = {q["name"]: q for q in GALS}
CFG695 = jl(os.path.join(REPO, "campaign_fresh_gravity", "CFG695_saturating_vacuum", "cfg695_results.json"))["numbers"]["S2"]
U0 = {f: float(CFG695[f]["U"]) for f in FOOTS}
ENV = {r["galaxy"].strip(): r for r in csv.DictReader(open(os.path.join(REPO, "real_research", "reviews", "directional_efe_2026", "laneB_data", "chae21_env.csv")))}
LNE = {k: dict(primary=0.5 * (float(r["log_eN_maxclu"]) + float(r["log_eN_noclu"])), maxclu=float(r["log_eN_maxclu"]), noclu=float(r["log_eN_noclu"])) for k, r in ENV.items()}


def ge_of(name, a0, which="primary"):
    if name not in LNE:
        return 0.0
    return float(S.g_from_gN(10 ** LNE[name][which] * GE_CHAE / a0))


def pts(q, ups, a0):
    """valid-point arrays at one Upsilon: g_bar, g_obs, mask, log g_iso."""
    GB, GO, OK, W = gal_arrays(q, np.array([ups]))
    gb, go, ok = GB[:, 0], GO[:, 0], OK[:, 0]
    lgi = np.log10(nu1(np.where(ok, gb, 1.0) / a0) * np.where(ok, gb, 1.0))
    return gb, go, ok, lgi


# ============================================================================ S0c residual identity
s0c = {}
for f in FOOTS:
    mx = 0.0; n = 0; nbad = 0
    for q in GALS:
        gb, go, ok, lgi = pts(q, U0[f], A0[f])
        ref = fl(SP[q["name"]][f"resid_dex_{FK[f]}"])
        if ok.any():
            d = abs(float(np.median(np.log10(go[ok]) - lgi[ok])) - ref); mx = max(mx, d); n += 1
            tol = 0.5 * 10 ** (math.floor(math.log10(abs(ref))) - 5) if ref != 0 else 5e-7   # A1: half a unit in the 6th significant digit
            nbad += int(d > tol)
    s0c[f] = dict(n=n, max_abs_diff=mx, n_outside_6digit_tol=nbad)
RES["step0"]["S0c"] = s0c
check("S0c", all(v["n_outside_6digit_tol"] == 0 and v["n"] == NG for v in s0c.values()), "; ".join(f"{f} N {v['n']} max|d| {v['max_abs_diff']:.1e}, outside 6-digit tol {v['n_outside_6digit_tol']}" for f, v in s0c.items()),
      f"(U0 {U0})")

# ============================================================================ S0d P4 L* = 0 EFE pooled rms
P4J = jl(os.path.join(RB, "P4_v3_galaxy_tiles", "p4_v3_galaxy_tiles_results.json"))["tiles"]   # A1: script bug fix (key path)
s0d = {}; tt = time.time()
for f in FOOTS:
    a0 = A0[f]; LG = {}
    for q in GALS:
        GB, GO, OK, W = gal_arrays(q, UPS)
        lgiso = np.log10(np.where(GB > 0, nu1(np.maximum(GB, 1e-300) / a0) * np.maximum(GB, 1e-300), 1e-300))
        ge = ge_of(q["name"], a0)
        if ge <= 0:
            LG[q["name"]] = lgiso; continue
        LG[q["name"]] = interp_nodes(np.array([sparc_solve(q, u, a0, ge, 0.0)[0][0] for u in NODES]))
    st = pooled(fit_sample(GALS, LG)); ref = P4J["T1"]["footings"][f]["L0"]
    s0d[f] = dict(rms=st["rms"], U=st["U_median"], P4_rms=ref["rms"], P4_U=ref["U_median"])
RES["step0"]["S0d"] = s0d
check("S0d", all(abs(v["rms"] - v["P4_rms"]) <= 1e-4 and v["U"] == v["P4_U"] for v in s0d.values()),
      "; ".join(f"{f} {v['rms']:.6f}@{v['U']:.2f} (P4 {v['P4_rms']:.6f}@{v['P4_U']:.2f})" for f, v in s0d.items()), f"({time.time() - tt:.0f} s)")

# ============================================================================ route E (EM1's machinery, copied)
F3 = jl(os.path.join(RB, "F3_growth_audit", "f3_growth_audit_results.json"))["K2"]
BGS = {}
for tag in ("A_c2b_refit", "B_cfg886_bg"):
    p = F3[tag]["params"]
    c = Class(); c.set({"omega_b": p["omega_b"], "omega_cdm": p["omega_cdm"], "h": p["h"], "ln10^{10}A_s": p["lnAs"], "n_s": p["n_s"],
                        "tau_reio": p["tau"], "N_ur": 3.044, "output": "mPk", "P_k_max_h/Mpc": 200.0, "z_max_pk": 10.0})
    c.compute()
    h = p["h"]; k = np.logspace(-4, math.log10(150.0), 3000)
    Pk = np.array([c.pk_lin(kk * h, 0.0) for kk in k]) * h ** 3
    Om = (p["omega_b"] + p["omega_cdm"]) / h ** 2 + c.Omega_nu
    rhom = Om * 2.775e11 * h ** 2
    def sigma(M, k=k, Pk=Pk, rhom=rhom, h=h):
        R = (3 * M / (4 * math.pi * rhom)) ** (1 / 3) * h
        x = np.outer(np.atleast_1d(R), k); W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
        return np.sqrt(np.trapz(k ** 3 * Pk * W ** 2 / (2 * math.pi ** 2), np.log(k), axis=1))
    zg = np.linspace(0, 30, 3001); Dg = np.array([c.scale_independent_growth_factor(z) for z in zg]); Dg /= Dg[0]
    H0 = 100 * h * 1e3 / MPC
    def cB(lM, z=0.0, sigma=sigma, zg=zg, Dg=Dg):
        s0 = sigma(0.01 * 10 ** np.atleast_1d(lM))
        Dt = np.clip(1.686 / s0, Dg[-1], 1.0)
        zc = np.interp(-Dt, -Dg, zg)
        return 4.0 * (1 + zc) / (1 + z)
    BGS[tag] = dict(rc0=3 * H0 ** 2 / (8 * math.pi * G), cgrid=cB(LM), fb=p["omega_b"] / (p["omega_b"] + p["omega_cdm"]))
    c.struct_cleanup()
mN = lambda x: np.log1p(x) - x / (1 + x)


def r200(lM, rc):
    return (3 * 10 ** lM * MSUN / (4 * math.pi * 200 * rc)) ** (1 / 3)


def g_nfw(lM, c_, r, rc):
    R2 = r200(np.asarray(lM), rc)[:, None]; rs = R2 / np.asarray(c_)[:, None]
    return G * 10 ** np.asarray(lM)[:, None] * MSUN * mN(r[None, :] / rs) / mN(np.asarray(c_))[:, None] / r[None, :] ** 2


LMB = np.array([math.log10((0.5 * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9) for q in GALS])


def em1_tables(q, bg, ups):
    """EM1's fit_one over the LM grid at the Upsilon vector ups: (nLM,) wr2, ws, iu."""
    GB, GO, OK, W = gal_arrays(q, ups)
    gh = g_nfw(LM, bg["cgrid"], q["R"] * KPC_S, bg["rc0"])
    lgp = np.log10(np.maximum(GB[None, :, :] + gh[:, :, None], 1e-300))
    r = np.where(OK, np.log10(GO)[:, :] - lgp, 0.0)
    Wm = np.where(OK, W[:, None], 0.0)
    wr2 = (Wm * r * r).sum(-2); ws = np.broadcast_to(Wm.sum(-2), wr2.shape)
    i = np.argmin(wr2 / np.maximum(ws, 1e-300), axis=-1)
    take = lambda a: np.take_along_axis(a, i[..., None], -1)[..., 0]
    return take(wr2), take(ws), i


AG = np.round(np.arange(10.0, 13.5001, 0.02), 2); BG_ = np.round(np.arange(0.0, 2.0001, 0.02), 2)


def fit_relation(WR2, WS):
    best = (np.inf, None, None); gidx = np.arange(NG)[:, None]
    for a in AG:
        lm = a + BG_[None, :] * (LMB[:, None] - 10.0)
        j = np.clip(np.rint((lm - LM[0]) / 0.02).astype(int), 0, len(LM) - 1)
        rms = np.sqrt(WR2[gidx, j].sum(0) / WS[gidx, j].sum(0))
        kk = int(np.argmin(rms))
        if rms[kk] < best[0]:
            best = (float(rms[kk]), (float(a), float(BG_[kk])), j[:, kk])
    return best


EM1REF = {"R1": jl(os.path.join(EMD, "em1_emergent_results.json"))["rows"], "UPS05": jl(os.path.join(EMD, "em1_emergent_results_UPS05.json"))["rows"]}
RTE = {}            # (bg, convention-key) -> dict(a, b, j (NG,), ups (NG,))
s0e = {}; oke = True; tt = time.time()
for bg_tag, bg in BGS.items():
    for ck, ups in (("R1", UPS), ("UPS05", np.array([0.50])), ("U0|canonical", np.array([U0["canonical"]])), ("U0|alt", np.array([U0["alt"]]))):
        TT = [em1_tables(q, bg, ups) for q in GALS]
        WR2 = np.array([t[0] for t in TT]); WS = np.array([t[1] for t in TT]); IU = np.array([t[2] for t in TT])
        rms, ab, j = fit_relation(WR2, WS)
        RTE[(bg_tag, ck)] = dict(a=ab[0], b=ab[1], rms=rms, j=j, ups=ups[IU[np.arange(NG), j]])
        if ck in EM1REF:
            ref = EM1REF[ck][bg_tag]["R1"]
            s0e[f"{bg_tag}|{ck}"] = dict(a=ab[0], b=ab[1], rms=rms, ref_a=ref["a"], ref_b=ref["b"], ref_rms=ref["rms"])
            oke &= ab[0] == ref["a"] and ab[1] == ref["b"] and abs(rms - ref["rms"]) <= 1e-4
RES["step0"]["S0e"] = s0e
RES["route_E_relations"] = {f"{k[0]}|{k[1]}": dict(a=v["a"], b=v["b"], rms=v["rms"]) for k, v in RTE.items()}
check("S0e", oke, "; ".join(f"{k} ({v['a']:.2f},{v['b']:.2f}) rms {v['rms']:.4f} (EM1 ({v['ref_a']:.2f},{v['ref_b']:.2f}) {v['ref_rms']:.4f})" for k, v in s0e.items()),
      f"({time.time() - tt:.0f} s)")
P("  route E relations at U0: " + "; ".join(f"{k}: lgM200 = {v['a']:.2f} + {v['b']:.2f}(lgMb-10), rms {v['rms']:.4f}" for k, v in RES["route_E_relations"].items() if "U0" in k))
s0_ok = all(RES["checks"][k]["ok"] for k in ("S0a", "S0b", "S0c", "S0d", "S0e"))
if not s0_ok:
    P("STOP RULE: a step-0 check failed; nothing further is computed (write a dated AMENDMENT first).")
    open(os.path.join(HERE, f"x36_efe{TAG}.out"), "w").write("\n".join(OUTL) + "\n")
    json.dump(RES, open(os.path.join(HERE, f"x36_efe_results{TAG}.json"), "w"), indent=1, default=float)
    sys.exit(1)

# ============================================================================ samples and the e_ext axis
SA = [q["name"] for q in GALS if np.isfinite(fl(SP[q["name"]]["e_ext"]))]
SL = [n for n in SA if SP[n]["subclass"] == "large"]
LOGE = {n: math.log10(fl(SP[n]["e_ext"])) for n in SA}
if MUT:   # shuffle log e_ext within morphology bins
    rng = np.random.default_rng(3602); Tbin = lambda T: 0 if T <= 3 else (1 if T <= 6 else (2 if T <= 8 else 3))
    for b_ in range(4):
        mem = [n for n in SA if Tbin(GBYN[n]["meta"]["T"]) == b_]
        vals = [LOGE[n] for n in mem]; perm = rng.permutation(len(mem))
        for n, k_ in zip(mem, perm):
            LOGE[n] = vals[k_]
P(f"\nsamples: S_L (large, with environment) N {len(SL)}; S_A (all with environment) N {len(SA)}; U0 {U0}; MUTATE {MUT}")

# ============================================================================ per-galaxy residuals per convention and footing
UPS_EM1 = {GALS[i]["name"]: float(RTE[("A_c2b_refit", "R1")]["ups"][i]) for i in range(NG)}
GIDX = {q["name"]: i for i, q in enumerate(GALS)}
CONV = ("C_U0", "C_05", "C_EM1")


def ups_of(conv, f, n):
    return U0[f] if conv == "C_U0" else (0.50 if conv == "C_05" else UPS_EM1[n])


def rte_key(conv, f):
    return {"C_U0": f"U0|{f}", "C_05": "UPS05", "C_EM1": "R1"}[conv]


PG = {}            # (f, conv) -> {name: dict}
tt = time.time()
for f in FOOTS:
    a0 = A0[f]
    for conv in CONV:
        d_ = {}
        for n in SA:
            q = GBYN[n]; u = ups_of(conv, f, n)
            gb, go, ok, lgi = pts(q, u, a0)
            lgo = np.log10(np.where(ok, go, 1.0))
            row = dict(ups=u, n_ok=int(ok.sum()), r_obs=float(np.median(lgo[ok] - lgi[ok])))
            # (a) law + exact AQUAL EFE (P4 sparc_solve), variants
            fac = 0.0 if MUT else 1.0
            sol = {}
            sol["a"] = sparc_solve(q, u, a0, fac * ge_of(n, a0, "primary"), 0.0)[0]
            sol["a_maxclu"] = sparc_solve(q, u, a0, fac * ge_of(n, a0, "maxclu"), 0.0)[0]
            sol["a_noclu"] = sparc_solve(q, u, a0, fac * ge_of(n, a0, "noclu"), 0.0)[0]
            sol["a_L24"] = sparc_solve(q, u, a0, fac * ge_of(n, a0, "primary"), 0.024)[0]
            lgm = {"a": sol["a"][0], "a_ring": sol["a"][1], "a_maxclu": sol["a_maxclu"][0], "a_noclu": sol["a_noclu"][0], "a_L24": sol["a_L24"][0]}
            # (b) route E: EM1's halo on its relation for this convention, no EFE term
            for bg_tag, bk in (("A_c2b_refit", "b"), ("B_cfg886_bg", "b_bgB")):
                rel = RTE[(bg_tag, rte_key(conv, f))]; j = int(rel["j"][GIDX[n]])
                gh = g_nfw(LM[j:j + 1], BGS[bg_tag]["cgrid"][j:j + 1], q["R"] * KPC_S, BGS[bg_tag]["rc0"])[0]
                lgm[bk] = np.log10(np.maximum(np.where(ok, gb, 1.0) + gh, 1e-300))
                if bk == "b":
                    row["lgM200_E"] = float(LM[j])
            for mk, lg in lgm.items():
                row[f"r_{mk}"] = float(np.median(lg[ok] - lgi[ok]))
                row[f"rem_{mk}"] = float(np.median(lgo[ok] - lg[ok]))
            d_[n] = row
        PG[(f, conv)] = d_
    P(f"  [{f}] per-galaxy predictions done ({time.time() - tt:.0f} s)")
MODELS = ("a", "a_ring", "a_maxclu", "a_noclu", "a_L24", "b", "b_bgB")

# ============================================================================ statistics
def boot_idx(N):
    return np.random.default_rng([3601, N]).integers(0, N, (B_BOOT, N))


def slope(x, y):
    xm = x.mean(-1, keepdims=True); ym = y.mean(-1, keepdims=True)
    return ((x - xm) * (y - ym)).sum(-1) / ((x - xm) ** 2).sum(-1)


def stats(names, f, conv, extra=None):
    x = np.array([LOGE[n] for n in names]); BI = boot_idx(len(names)); xb = x[BI]
    ro = np.array([PG[(f, conv)][n]["r_obs"] for n in names]) if extra is None else extra
    s_obs = float(slope(x, ro)); sb_obs = slope(xb, ro[BI]); sd_obs = float(np.std(sb_obs, ddof=1))
    rho, p = spearmanr(x, ro)
    out = dict(N=len(names), s_obs=s_obs, sd_obs=sd_obs, rho=float(rho), p=float(p), models={})
    for m in MODELS:
        rm = np.array([PG[(f, conv)][n][f"r_{m}"] for n in names]); rem = np.array([PG[(f, conv)][n][f"rem_{m}"] for n in names])
        s_m = float(slope(x, rm)); dlt = sb_obs - slope(xb, rm[BI]); sdd = float(np.std(dlt, ddof=1))
        out["models"][m] = dict(s=s_m, sd_s=float(np.std(slope(xb, rm[BI]), ddof=1)), delta=s_obs - s_m, sd_delta=sdd,
                                z=(s_obs - s_m) / sdd if sdd > 0 else float("inf"), rem_slope=float(slope(x, rem)),
                                rem_sd=float(np.std(slope(xb, rem[BI]), ddof=1)), rem_rho=float(spearmanr(x, rem)[0]),
                                median_r=float(np.median(rm)), max_abs_r=float(np.max(np.abs(rm))))
    out["P"] = abs(out["models"]["a"]["s"] - out["models"]["b"]["s"]) / sd_obs
    return out


ST = {}
P("\n=== SLOPES (dex in residual per dex in e_ext; paired bootstrap B 2000)")
for f in FOOTS:
    for conv in CONV:
        for sname, names in (("S_L", SL), ("S_A", SA)):
            st = stats(names, f, conv); ST[f"{f}|{conv}|{sname}"] = st
            ma, mb = st["models"]["a"], st["models"]["b"]
            P(f"[{f} {conv} {sname} N {st['N']}] measured s {st['s_obs']:+.4f} +- {st['sd_obs']:.4f} (rho {st['rho']:+.3f}, p {st['p']:.1e}) | "
              f"(a) law+EFE s {ma['s']:+.4f} (z {ma['z']:+.2f}; median r_a {ma['median_r']:+.4f}, max|r_a| {ma['max_abs_r']:.3f}) | "
              f"(b) route E s {mb['s']:+.4f} (z {mb['z']:+.2f}) | power P {st['P']:.2f}")
            P("      variants: " + ", ".join(f"{m} s {st['models'][m]['s']:+.4f} z {st['models'][m]['z']:+.2f}" for m in MODELS if m not in ("a", "b")) +
              f" | remaining slope vs (a) {ma['rem_slope']:+.4f} +- {ma['rem_sd']:.4f}, vs (b) {mb['rem_slope']:+.4f} +- {mb['rem_sd']:.4f}")
RES["slopes"] = ST

# ============================================================================ confounds (S_L, C_U0)
def ranks(v):
    from scipy.stats import rankdata
    return rankdata(v)


def partial(y, x, Z):
    ry, rx = ranks(y), ranks(x)
    if Z.shape[1] == 0:
        r = float(np.corrcoef(rx, ry)[0, 1]); k = 0
    else:
        A = np.column_stack([np.ones(len(y))] + [ranks(z) for z in Z.T])
        ey = ry - A @ np.linalg.lstsq(A, ry, rcond=None)[0]; ex = rx - A @ np.linalg.lstsq(A, rx, rcond=None)[0]
        r = float(np.corrcoef(ex, ey)[0, 1]); k = Z.shape[1]
    dof = len(y) - 2 - k; tt_ = r * math.sqrt(dof / max(1 - r * r, 1e-300))
    return r, float(2 * TDIST.sf(abs(tt_), dof))


def ctrl_vals(n):
    q = GBYN[n]; m = q["meta"]; a = SP[n]
    return dict(logD=math.log10(m["D"]), inc=m["Inc"], Q=m["Q"], T=m["T"], logSigma0=math.log10(fl(a["Sigma0"])), logL36=math.log10(m["L36"] * 1e9),
                logMb=math.log10(fl(a["M_b"])), fD_hubble=1.0 if m["fD"] == 1 else 0.0, uma=fl(a["uma_member"]),
                logRlast=math.log10(fl(a["R_last_kpc"])), logx=math.log10(fl(a["x_char"])))


GATED = ("logD", "inc", "Q", "T", "logSigma0", "logL36", "logMb", "fD_hubble", "uma")
REPORTED = ("logRlast", "logx")
CF = {}
P("\n=== CONFOUNDS (S_L, C_U0; partial Spearman by rank regression)")
for f in FOOTS:
    names = SL; y = np.array([PG[(f, "C_U0")][n]["r_obs"] for n in names]); x = np.array([LOGE[n] for n in names])
    CV = {k: np.array([ctrl_vals(n)[k] for n in names]) for k in GATED + REPORTED}
    raw, praw = partial(y, x, np.zeros((len(y), 0)))
    single = {}
    for k in GATED + REPORTED:
        if np.ptp(CV[k]) == 0:
            single[k] = dict(skipped="constant in sample"); continue
        r, p = partial(y, x, CV[k][:, None]); re_, pe = spearmanr(CV[k], x)
        single[k] = dict(rho_partial=r, p=p, rho_e_ctrl=float(re_), p_e_ctrl=float(pe), drop=abs(raw) - abs(r), gated=k in GATED)
    Zj = np.column_stack([CV[k] for k in GATED if np.ptp(CV[k]) > 0])
    rj, pj = partial(y, x, Zj)
    fires = (pj >= 0.05) and (abs(rj) <= 0.5 * abs(raw))
    cand = [(v["drop"], k) for k, v in single.items() if v.get("gated") and v["p_e_ctrl"] < 0.01]
    name = max(cand)[1] if cand else "joint (no single control)"
    # residual slope by distance method
    hub = np.array([ctrl_vals(n)["fD_hubble"] for n in names]) == 1
    byfd = {lab: dict(N=int(m_.sum()), s=float(slope(x[m_], y[m_])) if m_.sum() > 3 else float("nan"), rho=float(spearmanr(x[m_], y[m_])[0]) if m_.sum() > 3 else float("nan"))
            for lab, m_ in (("Hubble flow", hub), ("other methods", ~hub))}
    CF[f] = dict(raw=dict(rho=raw, p=praw), single=single, joint=dict(rho=rj, p=pj, controls=[k for k in GATED if np.ptp(CV[k]) > 0]),
                 gate_fires=bool(fires), named=name if fires else None, by_fD=byfd)
    P(f"[{f}] raw rho {raw:+.3f} (p {praw:.1e}); joint partial rho {rj:+.3f} (p {pj:.1e}) -> gate {'FIRES' if fires else 'does not fire'}")
    for k, v in single.items():
        if "skipped" in v:
            P(f"     | {k:10s} skipped ({v['skipped']})"); continue
        P(f"     | {k:10s} partial rho {v['rho_partial']:+.3f} (p {v['p']:.1e}); Spearman(e, {k}) {v['rho_e_ctrl']:+.3f} (p {v['p_e_ctrl']:.1e})" + ("" if v["gated"] else "  [reported, not gated]"))
    P(f"     | by distance method: " + "; ".join(f"{k} N {v['N']} s {v['s']:+.4f} rho {v['rho']:+.3f}" for k, v in byfd.items()))
RES["confounds"] = CF

# ============================================================================ verdict per footing
VF = {}
for f in FOOTS:
    st0 = ST[f"{f}|C_U0|S_L"]; za = st0["models"]["a"]["z"]; Pw = st0["P"]
    zb = {conv: ST[f"{f}|{conv}|S_L"]["models"]["b"]["z"] for conv in CONV}
    zb_best = min(abs(v) for v in zb.values())
    if CF[f]["gate_fires"]:
        v = f"CONFOUND-DRIVEN ({CF[f]['named']})"
    elif Pw < 2 or (abs(za) < 2 and zb_best < 2):
        v = "NOT DIAGNOSTIC" + (" (power P < 2)" if Pw < 2 else " (both reproduce)")
    elif abs(za) < 2 and all(abs(x_) >= 3 for x_ in zb.values()) and Pw >= 3:
        v = "EFE DISCRIMINATES: LAW"
    elif zb_best < 2 and abs(za) >= 3 and Pw >= 3:
        v = "EFE DISCRIMINATES: ROUTE E"
    else:
        v = "UNDECIDED (" + ("NEITHER" if abs(za) >= 3 and all(abs(x_) >= 3 for x_ in zb.values()) else "TENSION") + ")"
    VF[f] = dict(verdict=v, z_a=za, z_b=zb, P=Pw, reproduces_a=abs(za) < 2, reproduces_b_best=zb_best < 2)
base = lambda s_: s_.split(" (")[0] if not s_.startswith("UNDECIDED") else s_
V = VF["canonical"]["verdict"] if base(VF["canonical"]["verdict"]) == base(VF["alt"]["verdict"]) else "UNDECIDED (footing split)"
RES["verdict_per_footing"] = VF; RES["verdict"] = V

# ============================================================================ reported: tidal bound, DR4, directional record
TB = {}
for d_mpc in (1.0, 3.0):
    rat = []
    for n in SL:
        lM = PG[("canonical", "C_U0")][n]["lgM200_E"]; gext = 10 ** LOGE[n] * A0["canonical"]
        rt = (G * 10 ** lM * MSUN / (2 * gext / (d_mpc * MPC))) ** (1 / 3)
        rat.append(rt / (GBYN[n]["R"][-1] * KPC_S))
    TB[f"d={d_mpc:g}Mpc"] = dict(median=float(np.median(rat)), min=float(np.min(rat)))
RES["tidal_bound_rt_over_Rlast"] = TB

SEAL = jl(os.path.join(RB, "S3_v3_mw_seals", "SEALED_V3_MW_DR4.json")); C6 = jl(os.path.join(REPO, "covariant_push_2026_10_22", "C6_literal_cassini", "c6_literal_cassini_results.json"))
R0 = float(SEAL["inputs"]["R0_kpc"]); DR4 = {}
for f in FOOTS:
    vc = SEAL["v3"][f]["1.000000"]["P2_Vc_gamma0_exact"]
    lgR = np.log10([8.0, 9.0]); lgV = np.log10([vc["R8"], vc["R9"]])
    V0 = 10 ** (lgV[0] + (lgV[1] - lgV[0]) * (math.log10(R0) - lgR[0]) / (lgR[1] - lgR[0]))
    dlg_dlgR = 2 * (lgV[1] - lgV[0]) / (lgR[1] - lgR[0]) - 1
    e0 = (V0 * 1e3) ** 2 / (R0 * KPC_S) / A0[f]
    lever = abs(dlg_dlgR) * (math.log10(R0 + 0.2) - math.log10(R0 - 0.2))
    DR4[f] = dict(V_R0=V0, e_MW_R0=e0, dlog_e_over_400pc=lever,
                  screened_gamma_minus_1_20kAU={L: C6["R3_wide_binary"][f"{f}|{L}"]["gamma_minus_1"][0] for L in ("24", "50", "90")})
sl_x = np.array([LOGE[n] for n in SL]); DR4["SPARC_S_L_log_e_10_90"] = [float(v) for v in np.percentile(sl_x, [10, 90])]
RES["DR4_note"] = DR4
W = jl(os.path.join(REPO, "prep_2026", "wallaby_firing", "fire_wallaby_results.json"))["stacks"]["ALL | canonical a0=9.36e-11 | maxclu"]
N16 = jl(os.path.join(REPO, "prep_2026", "aligned_firing", "fire_aligned_n16_results.json"))["stacks"]["ALL | canonical a0=9.36e-11 | maxclu"]
RES["directional_efe_record"] = dict(n16=dict(n=N16["n"], Ahat=N16["Ahat"], Z=N16["Z"]), wallaby=dict(n=W["n"], Ahat=W["Ahat"], boot_std=W["boot_std"], Z=W["Z"]))

P("\n=== REPORTED")
P("tidal bound (route E halos, S_L, canonical U0 relation): " + "; ".join(f"{k}: r_t/R_last median {v['median']:.1f}, min {v['min']:.1f}" for k, v in TB.items()))
for f in FOOTS:
    d = DR4[f]
    P(f"DR4 [{f}]: MW field at R0 = {R0} kpc: V {d['V_R0']:.1f} km/s, e = g/a0 {d['e_MW_R0']:.2f}; lever arm over +-200 pc {d['dlog_e_over_400pc']:.4f} dex "
      f"(SPARC S_L log e 10-90%: {DR4['SPARC_S_L_log_e_10_90'][0]:+.2f} to {DR4['SPARC_S_L_log_e_10_90'][1]:+.2f}); v3s screened gamma_v-1 at 20 kAU (L* 24/50/90 pc) "
      + ", ".join(f"{v:.2e}" for v in d["screened_gamma_minus_1_20kAU"].values()) + "; route E: Newtonian by construction")
P(f"directional EFE record: n16 Ahat {N16['Ahat']:+.2f} (Z {N16['Z']:+.2f}) beside WALLABY n {W['n']} Ahat {W['Ahat']:+.2f} +- {W['boot_std']:.2f} (Z {W['Z']:+.2f}); AQUAL = +1 on that scale")

# ============================================================================ checks
P("\n=== CHECKS")
kefe = {}
for f in FOOTS:
    ra = np.array([PG[(f, "C_U0")][n]["r_a"] for n in SA]); kefe[f] = dict(max=float(ra.max()), max_abs=float(np.max(np.abs(ra))))
check("K_efe", all(v["max"] <= 1e-6 and v["max_abs"] > 1e-3 for v in kefe.values()), "; ".join(f"{f} max r_a {v['max']:+.2e}, max|r_a| {v['max_abs']:.4f}" for f, v in kefe.items()))
krep = {f: (ST[f"{f}|C_U0|S_L"]["rho"], s0b[f"{f}|SPARC:large"]["ref_rho"]) for f in FOOTS}
check("K_repro", all(abs(a - b) <= 1e-9 for a, b in krep.values()), "; ".join(f"{f} {a:+.6f} vs X33 {b:+.6f}" for f, (a, b) in krep.items()))
kpl = {}
for f in FOOTS:
    x = np.array([LOGE[n] for n in SL]); ro = np.array([PG[(f, "C_U0")][n]["r_obs"] for n in SL])
    stp = stats(SL, f, "C_U0", extra=ro - 0.10 * (x - x.mean())); st0 = ST[f"{f}|C_U0|S_L"]
    kpl[f] = dict(shift=stp["s_obs"] - st0["s_obs"], sd=st0["sd_obs"])
check("K_plant", all(abs(v["shift"] + 0.10) <= 2 * v["sd"] for v in kpl.values()), "; ".join(f"{f} shift {v['shift']:+.4f} (planted -0.10, 2 sd {2 * v['sd']:.4f})" for f, v in kpl.items()))
check("K_rss", rss_gb() < 1.0, f"{rss_gb():.2f} GB")

P(f"\nVERDICT per footing: canonical {VF['canonical']['verdict']}; alt {VF['alt']['verdict']}  ->  {V}")
RES["runtime_s"] = time.time() - T0_
allok = all(v["ok"] for v in RES["checks"].values())
P(f"checks: {'ALL PASS' if allok else 'SOME FAIL'}  ({RES['runtime_s']:.0f} s)")
with open(os.path.join(HERE, f"x36_per_galaxy{TAG}.csv"), "w", newline="") as fh:
    keys = ["ups", "n_ok", "r_obs"] + [f"r_{m}" for m in MODELS] + [f"rem_{m}" for m in MODELS] + ["lgM200_E"]
    w = csv.writer(fh); w.writerow(["footing", "convention", "galaxy", "sample", "log_e_ext"] + keys)
    for (f, conv), d_ in PG.items():
        for n, row in d_.items():
            w.writerow([f, conv, n, "S_L" if n in SL else "S_A_only", f"{LOGE[n]:.6f}"] + [f"{row[k]:.6g}" if isinstance(row[k], float) else row[k] for k in keys])
open(os.path.join(HERE, f"x36_efe{TAG}.out"), "w").write("\n".join(OUTL) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x36_efe_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if allok else 1)
