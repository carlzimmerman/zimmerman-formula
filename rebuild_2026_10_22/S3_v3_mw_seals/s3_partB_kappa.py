#!/usr/bin/env python3
"""S3_v3_mw_seals Part B: kappa re-fit under v3's AQUAL disc law (tile 47).

Criteria FROZEN_CRITERIA.md §3 (8f6c6587e1) + A1, A2.  CFG493's code executed read-only up to its per-route budget section
(loaders, point masks, levers, error terms, GLS machinery); my nu1 fits with a per-point AQUAL correction C(R; a0).
Steps: K (kernel nu_mono -> nu1) -> A (AQUAL disc, isolated; the verdict) -> E (EFE along the disc axis, reported).
Per-galaxy AQUAL solves run in short-lived child processes (s3_kappa_lib.py).
Run: OMP_NUM_THREADS=1 nice -n 15 python3 s3_partB_kappa.py [--mutate]
kappa = 1/2 FITTED (here MEASURED, never derived); footings never pooled; no dark-matter particle; not theory closed.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, io, csv, json, math, time, contextlib, hashlib, resource
import numpy as np
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s3_aqual as S

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFGD = os.path.join(REPO, "campaign_fresh_gravity")
TAG = S.TAG
OUT, CHECKS = [], []
T0 = time.time()
CACHE = S.CACHE


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.append(s)


def check(name, ok, detail=""):
    CHECKS.append(dict(name=name, ok=bool(ok), detail=detail))
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")
    return bool(ok)


P("=" * 112)
P(f"S3 Part B: kappa under v3's AQUAL disc law {'*** MUTATE: mu == 1 ***' if S.MUTATE else ''}")
P("kappa = 1/2 FITTED (measured here, never derived); footings never pooled; not theory closed")
P("=" * 112)

# ------------------------------------------------------------------ CFG493 executed read-only (up to its budget section)
src = open(os.path.join(CFGD, "CFG493_kappa_combined", "cfg493_kappa_combined.py")).read()
head = src.split("# ------------------------------------------------------------------ I2 and per-route budgets")[0]
ns = {"__file__": os.path.join(CFGD, "CFG493_kappa_combined", "cfg493_kappa_combined.py"), "__name__": "cfg493_import"}
argv0 = sys.argv; sys.argv = [argv0[0]]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(head, "cfg493_head", "exec"), ns)
sys.argv = argv0
J493 = json.load(open(os.path.join(CFGD, "CFG493_kappa_combined", "cfg493_kappa_combined_results.json")))
cb0 = ns["combine"](ns["PRIM"])
dL = max(abs(ns["L1"] - J493["routes"]["P1 SPARC gas points (ladder)"]["L"]), abs(ns["L2"] - J493["routes"]["P2 MeerKAT MIGHTEE-HI widths"]["L"]),
         abs(ns["L3"] - J493["routes"]["P3 WALLABY DR2 gas points"]["L"]))
comb_ref = J493.get("combined", {})
Lc_ref = comb_ref.get("L", None); sc_ref = comb_ref.get("sigma", None)
P(f"  CFG493 read-only: L1 {ns['L1']:+.6f} L2 {ns['L2']:+.6f} L3 {ns['L3']:+.6f}; combined {cb0['L']:+.6f} +- {cb0['sigma']:.6f} (JSON {Lc_ref} +- {sc_ref})")
okc = (Lc_ref is None) or (abs(cb0["L"] - Lc_ref) < 1e-6 and abs(cb0["sigma"] - sc_ref) < 1e-6)
check("B1", dL < 1e-6 and okc, f"CFG493 reproduced with nu_mono: max |dL_route| {dL:.1e}, combined {cb0['L']:+.6f} +- {cb0['sigma']:.6f} (tol 1e-6)")
combine, cov, verdict, kap, route, CAND, SH = (ns[k] for k in ("combine", "cov", "verdict", "kap", "route", "CAND", "SH"))
arrays, sel_points, rescale, P1g, TIE1, RC_RED = (ns[k] for k in ("arrays", "sel_points", "rescale", "P1g", "TIE1", "RC_RED"))
build, gas_points, AG, GX = (ns[k] for k in ("build", "gas_points", "AG", "GX"))
U2_0, L2_0 = dict(ns["U2"]), ns["L2"]
lev2 = dict(S_gas=ns["lev2_gas"], S_star=ns["lev2_star"], S_HF=ns["lev2_HF"])
A0G = np.array([4.0e-11, 6.5e-11, 10.5e-11, 17.0e-11])
LA0G = np.log10(A0G)


def Cint(tab, la):
    """tab (4, n) at A0G -> C at log10 a0 = la (linear in log a0, clamped)."""
    la = min(max(la, LA0G[0]), LA0G[-1])
    j = int(np.clip(np.searchsorted(LA0G, la) - 1, 0, 2))
    t = (la - LA0G[j]) / (LA0G[j + 1] - LA0G[j])
    return (1 - t) * tab[j] + t * tab[j + 1]


# ------------------------------------------------------------------ fits with nu1 and C (my versions of CFG493's fit1/fit3)
def fit1C(parts, nu=S.nu1):
    """parts: (gb, go, w, Ctab|None) per galaxy.  CFG493's objective with g_model = C nu(gb/a0) gb."""
    def f(la):
        tot = 0.0
        for gb, go, w, Ct in parts:
            C = 1.0 if Ct is None else Cint(Ct, la)
            tot += np.sum(w * (np.log10(go) - np.log10(C) - np.log10(gb) - np.log10(nu(gb / 10 ** la))) ** 2)
        return tot
    return minimize_scalar(f, bounds=(-10.8, -9.3), method="bounded", options={"xatol": 1e-5}).x


def boot1C(parts, nu=S.nu1):
    rng = np.random.default_rng(7)
    return float(np.std([fit1C([parts[i] for i in rng.integers(0, len(parts), len(parts))], nu) for _ in range(500)]))


def fit3C(Pp, nu=S.nu1, sint=0.11):
    """Pp: (name, gb, go, sg, Ctab|None).  CFG493's fit3 with nu1 and C."""
    ch = np.zeros_like(AG)
    for _, gb, go, sg, Ct in Pp:
        for i, a in enumerate(AG):
            C = 1.0 if Ct is None else Cint(Ct, math.log10(a))
            pred = C * gb * nu(gb / a)
            ch[i] += np.sum((np.log10(go) - np.log10(pred)) ** 2 / (sg ** 2 + sint ** 2))
    i = int(np.argmin(ch)); lo, hi = max(0, i - 6), min(len(AG), i + 7)
    p = np.polyfit(np.log(AG[lo:hi]) - math.log(AG[i]), ch[lo:hi], 2)
    return math.exp(math.log(AG[i]) - p[1] / (2 * p[0]))


def boot3C(Pp, nu=S.nu1):
    rng = np.random.default_rng(43)
    B = [fit3C([Pp[i] for i in rng.integers(0, len(Pp), len(Pp))], nu) for _ in range(200)]
    lo, hi = np.percentile(B, [16, 84]); return (math.log10(hi) - math.log10(lo)) / 2


# reproduction of fit1/fit3 with nu_mono through my versions (sanity, part of B1's spirit; printed)
parts_nom = [(b, o, w, None) for (b, o, w) in arrays(P1g, 0.5, 10 ** TIE1)]
P(f"  my fit1C(nu_mono) on CFG493's P1 parts: {fit1C(parts_nom, S.nu_mono):+.6f} vs CFG493 {ns['L1']:+.6f}")

# ------------------------------------------------------------------ point radii (CFG493's masks replicated to get R)
def p1_points(gs, U=0.5, gscale=1.0):
    out = []
    for g in gs:
        m = sel_points(g); R = g["R"][m]
        vg = g["Vgas"][m]
        KPC = 3.0857e19
        b = (gscale * np.sign(vg) * vg ** 2 + U * g["Vdisk"][m] ** 2 + 1.4 * U * g["Vbul"][m] ** 2) * 1e6 / (R * KPC)
        o = (g["Vobs"][m] * 1e3) ** 2 / (R * KPC)
        ok = (b > 0) & (o > 0)
        out.append((g["name"], R[ok], float(g["R"][-1])))
    return out


def p3_points(gals, ups_scale=1.0, gas_scale=1.0, fcut=0.8):
    out = []
    for g in gals:
        vb2 = g["vg2"] + g["vs2"]
        fg = np.where(vb2 > 0, g["vg2"] / np.where(vb2 > 0, vb2, 1), 0)
        m = (fg > fcut) & (g["vg2"] > 0)
        if m.sum() >= 2:
            out.append((g["name"], g["R"][m], float(g["R"][-1])))
    return out


# ------------------------------------------------------------------ P1 inputs: rotmod SB columns (by name), rescaled as P1g
SPD = os.path.join(REPO, "real_research", "data", "sparc_data")
meta = {g["name"]: g["meta"] for g in ns["SP"]}
J449 = ns["J449"]; srD = ns["srD"]
p1_jobs = []
for g in P1g:
    nm = g["name"]
    d = np.genfromtxt(os.path.join(SPD, f"{nm}_rotmod.dat"), comments="#")
    f = (srD[nm][1] / srD[nm][0]) if nm in srD else 1.0
    assert np.allclose(d[:, 0] * f, g["R"]), nm
    p1_jobs.append(dict(name=nm, R=(d[:, 0] * f).tolist(), Vgas=(d[:, 3] * math.sqrt(f)).tolist(), SBdisk=d[:, 6].tolist(),
                        Vbul=(d[:, 5] * math.sqrt(f)).tolist(), Rdisk=float(meta[nm]["Rdisk"]) * f,
                        Mgas_target=1.33 * float(meta[nm]["MHI"]) * 1e9 * f ** 2))          # AMENDMENT A7

def cached_batch(func, jobs, tagname, batch):
    key = hashlib.sha1((tagname + TAG + json.dumps(jobs, sort_keys=True)).encode()).hexdigest()[:16]
    fn = os.path.join(CACHE, f"kappa_{tagname}_{key}.json")
    if os.path.exists(fn):
        d = json.load(open(fn)); return d["res"], d["peak"]
    res, peak = S.run_batch("s3_kappa_lib", func, jobs, batch=batch)
    json.dump(dict(res=res, peak=peak), open(fn, "w"))
    return res, peak



# ------------------------------------------------------------------ P3 inputs (AMENDMENT A6): Sigma per build variant, my V_gas^2
best, srcW, wise, flt, arr = ns["best"], ns["src"], ns["wise"], ns["flt"], ns["arr"]
VARS = {"nom": dict(H0w=67.4), "h70": dict(H0w=70.0), "cmb": dict(H0w=67.4, dist="cmb"), "ad8": dict(H0w=67.4, sig_ad=8.0),
        "rd05": dict(H0w=67.4, rdfac=0.5), "rd2": dict(H0w=67.4, rdfac=2.0), "nofc": dict(H0w=67.4, fluxcorr=False)}
BUILDS = {k: build(**v) for k, v in VARS.items()}


def sigma_for(nm, H0w=67.4, dist="hubble", fluxcorr=True, **kw):
    r = best[nm]; s_ = srcW[nm]
    D = flt(s_["dist_h"]) * 70.0 / H0w
    gx_ = GX.get(nm)
    if dist == "cmb" and gx_ is not None:
        D = flt(gx_["D_mpc"]) * 73.0 / H0w
    fc = 10 ** (flt(s_["log_m_hi_corr"]) - flt(s_["log_m_hi"])) if (fluxcorr and np.isfinite(flt(s_.get("log_m_hi_corr", "nan")))) else 1.0
    kpc_as = D * 1e3 / 206264.806
    return arr(r["Rad_SD"]) * kpc_as, arr(r["SD_FO_model"]) * 1e6 * 1.33 * fc


rep = 0.0
for vk in ("nom", "h70", "cmb", "nofc"):
    for gg in BUILDS[vk][:40]:
        rS, Sg = sigma_for(gg["name"], **VARS[vk])
        rep = max(rep, float(np.max(np.abs(ns["v2_disc"](gg["R"], rS, Sg) - gg["vg2"]) / np.maximum(np.abs(gg["vg2"]), 1e-9))))
P(f"  P3: Sigma replication of CFG493's build (4 variants, 40 galaxies each): max rel {rep:.1e}")
VG2, VG2T = {}, {}
for vk in ("nom", "h70", "cmb", "nofc"):
    jobs = []
    for gg in BUILDS[vk]:
        rS, Sg = sigma_for(gg["name"], **VARS[vk])
        jobs.append(dict(name=gg["name"], R=gg["R"].tolist(), rS=rS.tolist(), Sig=Sg.tolist()))
    res_, pk = cached_batch("job_wallaby_vg2", jobs, f"vg2_{vk}", 25)
    VG2[vk] = {r["name"]: np.array(r["vg2"]) for r in res_}; VG2T[vk] = {r["name"]: np.array(r["vg2_thin"]) for r in res_}
for vk in ("ad8", "rd05", "rd2"):
    VG2[vk] = VG2["nom"]; VG2T[vk] = VG2T["nom"]
MY = {vk: [dict(gg, vg2=VG2[vk][gg["name"]]) for gg in BUILDS[vk]] for vk in VARS}
G67 = MY["nom"]
G67d = {g["name"]: g for g in G67}
P3pts = p3_points(G67)
P3names = [n for n, _, _ in P3pts]
P3rec = [n for n, _, _ in p3_points(BUILDS["nom"])]
p3_in = {}
for nm in P3names:
    rS, Sg = sigma_for(nm, **VARS["nom"])
    s_, w_ = srcW[nm], wise[nm]
    D = flt(s_["dist_h"]) * 70.0 / 67.4; kpc_as = D * 1e3 / 206264.806
    m1 = flt(w_["w1gmag"]) if np.isfinite(flt(w_["w1gmag"])) else flt(w_["w1mpro"])
    Mstar = 0.6 * 10 ** (-0.4 * (m1 - 5 * math.log10(D * 1e6) + 5 - 3.24))
    r2 = flt(w_["r_2mass"])
    Rd = (r2 * kpc_as / 3.5) if (np.isfinite(r2) and r2 > 0) else 10 ** (0.33 * (math.log10(Mstar) - 10) + 0.45)
    p3_in[nm] = dict(name=nm, R=G67d[nm]["R"].tolist(), rS=rS.tolist(), Sig=Sg.tolist(), Mstar=Mstar, Rd=Rd)
P(f"  P1: {len(p1_jobs)} SPARC galaxies; P3 rebuilt: {len(P3names)} WALLABY galaxies with gas points under my V_gas^2 "
  f"(record's v2_disc selection: {len(P3rec)}; in both {len(set(P3names) & set(P3rec))})")

# ------------------------------------------------------------------ AQUAL corrections in child processes (cached JSON)
RSSB = {}
P("\n--- AQUAL corrections (child processes)")
a0l = A0G.tolist()
R1p, pk = cached_batch("job_sparc", [dict(j, a0_list=a0l, thin=False) for j in p1_jobs], "p1", 1); RSSB["p1"] = pk
R1t, pk = cached_batch("job_sparc", [dict(j, a0_list=a0l, thin=True) for j in p1_jobs], "p1thin", 1); RSSB["p1thin"] = pk
P(f"  P1 done ({time.time() - T0:.0f} s; child peak RSS {max(RSSB.values()):.0f} MB)")
p3_jobs = [dict(name=n, R=p3_in[n]["R"], rS=p3_in[n]["rS"], Sig=p3_in[n]["Sig"], Mstar=p3_in[n]["Mstar"], Rd=p3_in[n]["Rd"]) for n in P3names]
R3p, pk = cached_batch("job_wallaby", [dict(j, a0_list=a0l, thin=False) for j in p3_jobs], "p3", 2); RSSB["p3"] = pk
R3t, pk = cached_batch("job_wallaby", [dict(j, a0_list=a0l, thin=True) for j in p3_jobs], "p3thin", 2); RSSB["p3thin"] = pk
R1x, pk = cached_batch("job_sparc", [dict(j, a0_list=a0l, thin=False, tail=2.0) for j in p1_jobs], "p1tail2", 1); RSSB["p1tail2"] = pk
R3x, pk = cached_batch("job_wallaby", [dict(j, a0_list=a0l, thin=False, tail=2.0) for j in p3_jobs], "p3tail2", 2); RSSB["p3tail2"] = pk
P(f"  P3 and outer-gas-extent variants done ({time.time() - T0:.0f} s; child peak RSS {max(RSSB.values()):.0f} MB)")
for r in R1p:
    nm = r["name"]; f_ = (srD[nm][1] / srD[nm][0]) if nm in srD else 1.0
    r["Mgas_ratio_to_SPARC_MHI"] = r["Mgas"] / (1.33 * meta[nm]["MHI"] * 1e9 * f_ ** 2)
P("  P1 inversion gas mass / (1.33 M_HI,SPARC f^2): " + ", ".join(f"{r['name']} {r['Mgas_ratio_to_SPARC_MHI']:.2f}" for r in R1p))
maxres = max(c["residual"] for rr in (R1p, R1t, R3p, R3t, R1x, R3x) for r in rr for c in r["C"])
P(f"  max AQUAL residual over all galaxy solves {maxres:.1e}")


def ctab_from(res_list):
    return {r["name"]: (np.array(r["R"]), np.array([c["C"] for c in r["C"]])) for r in res_list}


C1p, C1t, C3p, C3t = ctab_from(R1p), ctab_from(R1t), ctab_from(R3p), ctab_from(R3t)
C1x, C3x = ctab_from(R1x), ctab_from(R3x)


def ctab_at(Ctabs, name, R, Rlast):
    """C table (4, len(R)) at point radii R by interpolation in x = R/R_last of the galaxy's own profile."""
    Rg, tab = Ctabs[name]
    x = np.asarray(R) / Rlast; xg = Rg / Rg[-1]
    return np.array([np.interp(x, xg, t) for t in tab])


# B2: gas inversion and Newtonian V_bar^2 at P1 points; B3: WALLABY V_gas^2
b2_rms, b2_med = 0.0, []
for r, g in zip(R1p, P1g):
    m = sel_points(g)
    vb2_sp = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    fit, tgt = np.array(r["gas_fit"]), np.array(r["gas_target"])
    b2_rms = max(b2_rms, float(np.sqrt(np.mean(((fit - tgt)[m] / vb2_sp[m]) ** 2))))
    b2_med += list(np.abs(np.array(r["vbar2_me"])[m] / vb2_sp[m] - 1))
b2_med = float(np.median(b2_med))
check("B2", b2_rms <= 0.03 and b2_med <= 0.05, f"P1 gas inversion rms (per galaxy, worst) {b2_rms:.4f} of V_bar^2 (tol 0.03); my Newtonian V_bar^2 vs rotmod median |d| {b2_med:.4f} (tol 0.05)")
b3, b3p = [], []
for gg in BUILDS["nom"]:
    if gg["name"] not in P3rec:
        continue
    vb2 = gg["vg2"] + gg["vs2"]; fg = np.where(vb2 > 0, gg["vg2"] / np.where(vb2 > 0, vb2, 1), 0)
    m = (fg > 0.8) & (gg["vg2"] > 0)
    b3 += list(np.abs(VG2["nom"][gg["name"]][m] / gg["vg2"][m] - 1))
for gg in G67:
    if gg["name"] not in P3names:
        continue
    vb2 = gg["vg2"] + gg["vs2"]; fg = np.where(vb2 > 0, gg["vg2"] / np.where(vb2 > 0, vb2, 1), 0)
    m = (fg > 0.8) & (gg["vg2"] > 0)
    b3p += list(np.abs(VG2["nom"][gg["name"]][m] / VG2T["nom"][gg["name"]][m] - 1))
b3, b3p = float(np.median(b3)), float(np.median(b3p))
check("B3", b3 <= 0.02, f"(frozen; AMENDMENT A6: the reference is noisy) P3 my grid V_gas^2 vs CFG493 v2_disc at CFG493's gas points: median |d| {b3:.4f} (tol 0.02)")
check("B3p", b3p <= 0.02, f"(AMENDMENT A6) my V_gas^2 (sech2 0.1 kpc) vs its razor-thin variant at the rebuilt gas points: median |d| {b3p:.4f} (tol 0.02)")

# ------------------------------------------------------------------ assemble parts per step
def p1_parts(Ctabs, U=0.5, gscale=1.0, gs=None):
    gs = P1g if gs is None else gs
    arrs = arrays(gs, U, gscale * 10 ** TIE1)
    pts = p1_points(gs, U, gscale * 10 ** TIE1)
    out = []
    for (b, o, w), (nm, R, Rl) in zip(arrs, pts):
        assert len(b) == len(R), nm
        Ct = None if Ctabs is None else ctab_at(Ctabs, nm, R, Rl)
        out.append((b, o, w, Ct))
    return out


def p3_parts(Ctabs, gals=None, **kw):
    gals = G67 if gals is None else gals
    Pp = gas_points(gals, **kw)
    pts = {n: (R, Rl) for n, R, Rl in p3_points(gals, **kw)}
    out = []
    for nm, gb, go, sg in Pp:
        R, Rl = pts[nm]
        Ct = None if (Ctabs is None or nm not in Ctabs) else ctab_at(Ctabs, nm, R, Rl)
        out.append((nm, gb, go, sg, Ct))
    return out


def p1_route(Ctabs, label):
    parts = p1_parts(Ctabs)
    L1 = float(fit1C(parts)); sd1 = boot1C(parts)
    nom = [(b, o, w, Ct) for (b, o, w, Ct), (bb, oo, ww) in zip(p1_parts(Ctabs, gscale=10 ** -TIE1), arrays(P1g, 0.5))]
    L1_nom = float(fit1C(nom))
    lev_gas = (fit1C(p1_parts(Ctabs, gscale=1.1)) - L1) / math.log10(1.1)
    lev_star = (fit1C(p1_parts(Ctabs, U=0.7)) - L1) / math.log10(1.4)
    lev_D = (fit1C(p1_parts(Ctabs, gs=[rescale(g, 10 ** 0.01) for g in P1g])) - L1) / 0.01
    U = {"statistics": sd1, "P1 RC reduction": RC_RED, "ladder zero point": abs(lev_D) * 0.01, "flux-tie transfer": abs(L1 - L1_nom) / 2}
    return dict(L=L1, U=U, lev=dict(S_gas=lev_gas, S_star=lev_star, S_HF=0.0))


def p3_route(Ctabs, src=None):
    """src: dict of variant builds (default MY = rebuilt P3, AMENDMENT A6; BUILDS = the record's v2_disc)."""
    src = MY if src is None else src
    Pp = p3_parts(Ctabs, gals=src["nom"])
    a3 = fit3C(Pp); L3 = math.log10(a3); sd3 = boot3C(Pp)
    lev_gas = (math.log10(fit3C(p3_parts(Ctabs, gals=src["nom"], gas_scale=1.1))) - L3) / math.log10(1.1)
    lev_star = (math.log10(fit3C(p3_parts(Ctabs, gals=src["nom"], ups_scale=1.4))) - L3) / math.log10(1.4)
    a3_70 = fit3C(p3_parts(Ctabs, gals=src["h70"])); lev_HF = (math.log10(a3_70) - L3) / math.log10(70 / 67.4)
    a3_cmb = fit3C(p3_parts(Ctabs, gals=src["cmb"])); a3_ad = fit3C(p3_parts(Ctabs, gals=src["ad8"]))
    a3_rd = [fit3C(p3_parts(Ctabs, gals=src[k])) for k in ("rd05", "rd2")]
    a3_nofc = fit3C(p3_parts(Ctabs, gals=src["nofc"]))
    U = {"statistics": sd3, "P3 distance frame": abs(math.log10(a3_cmb / a3)) / 2,
         "P3 AD/Rd/EFE": math.sqrt(math.log10(a3_ad / a3) ** 2 + max(abs(math.log10(x / a3)) for x in a3_rd) ** 2 + (0.5 * math.log10(1.085)) ** 2),
         "flux-tie transfer": abs(math.log10(a3 / a3_nofc)) / 2}
    return dict(L=L3, U=U, lev=dict(S_gas=lev_gas, S_star=lev_star, S_HF=lev_HF))


# P2: kernel bound and the reference-disc AQUAL shift
y84 = 0.084
dK2 = -2 * math.log10(float(S.nu1(y84) / S.nu_mono(y84)))
P2K = dict(L=L2_0 + dK2 / 2, U=dict(U2_0, **{"P2 kernel (y <= 0.084 bound)": abs(dK2) / 2}), lev=lev2)
ref, pk = cached_batch("job_refdisc", [dict(a0_si=10 ** L2_0, thin=False), dict(a0_si=10 ** L2_0, thin=True)], "p2ref", 1); RSSB["p2ref"] = pk
dA2 = [-2 * math.log10(c) for c in ref[0]["C"]]
dA2t = [-2 * math.log10(c) for c in ref[1]["C"]]
shiftA2 = float(np.mean(dA2)); errA2 = float((max(dA2) - min(dA2)) / 2)
geomA2 = abs(float(np.mean(dA2t)) - shiftA2) / 2
P(f"  P2: kernel shift {dK2 / 2:+.5f} +- {abs(dK2) / 2:.5f} dex; reference deep disc (y at 3/4/5 R_d {np.round(ref[0]['y'], 4).tolist()}): C {np.round(ref[0]['C'], 5).tolist()} "
  f"-> AQUAL shift {shiftA2:+.5f} +- {errA2:.5f} dex (razor-thin {np.mean(dA2t):+.5f})")
P2A = dict(L=P2K["L"] + shiftA2, U=dict(P2K["U"], **{"P2 AQUAL reference disc": errA2, "AQUAL geometry": geomA2}), lev=lev2)

# ------------------------------------------------------------------ steps K and A
P("\n--- steps (per route: log a0 +- total; GLS combined; both footings)")
STEPS = {}
R_K1 = p1_route(None, "K"); R_K3 = p3_route(None)
R_K3rec = p3_route(None, src=BUILDS)                  # kernel only on the record's (v2_disc) P3: reported, never the verdict
R_A1 = p1_route(C1p, "A"); R_A3 = p3_route(C3p)
R_A1t = p1_route(C1t, "A thin"); R_A3t = p3_route(C3t)
R_A1x = p1_route(C1x, "A tail2"); R_A3x = p3_route(C3x)
R_A1["U"]["AQUAL geometry"] = abs(R_A1["L"] - R_A1t["L"]) / 2
R_A3["U"]["AQUAL geometry"] = abs(R_A3["L"] - R_A3t["L"]) / 2
R_A1["U"]["outer gas extent"] = abs(R_A1["L"] - R_A1x["L"]) / 2          # AMENDMENT A4
R_A3["U"]["outer gas extent"] = abs(R_A3["L"] - R_A3x["L"]) / 2
P(f"  P1 L: primary {R_A1['L']:+.4f}, razor-thin {R_A1t['L']:+.4f}, gas tail to 2 R_last {R_A1x['L']:+.4f}; "
  f"P3 L: primary {R_A3['L']:+.4f}, razor-thin {R_A3t['L']:+.4f}, tail 2 r_last {R_A3x['L']:+.4f}")

# B4: interpolated vs direct C at the fitted a0 (5 galaxies per route) -- direct solves in children
def b4(route_name, jobs_fn, Ctabs, La, names, ptsf):
    jobs = [dict(jobs_fn(n), a0_list=[10 ** La], thin=False) for n in names]
    res, pk = S.run_batch("s3_kappa_lib", "job_sparc" if route_name == "P1" else "job_wallaby", jobs, batch=1)
    worst = 0.0
    for r in res:
        Rg = np.array(r["R"]); Cd = np.array(r["C"][0]["C"])
        Ci = Cint(Ctabs[r["name"]][1], La)
        worst = max(worst, float(np.max(np.abs(Ci / Cd - 1))))
    return worst, pk


p1map = {j["name"]: j for j in p1_jobs}; p3map = {j["name"]: j for j in p3_jobs}
w1, pk1 = b4("P1", lambda n: {k: v for k, v in p1map[n].items()}, C1p, R_A1["L"], [j["name"] for j in p1_jobs[:5]], None)
w3, pk3 = b4("P3", lambda n: {k: v for k, v in p3map[n].items()}, C3p, R_A3["L"], P3names[:5], None)
RSSB["b4"] = max(pk1, pk3)
check("B4", max(w1, w3) <= 0.003, f"C interpolated in log a0 vs direct at the fitted a0: P1 {w1:.4f}, P3 {w3:.4f} (tol 0.003)")


def mk_routes(r1, p2, r3):
    return [route("P1 SPARC gas points (ladder)", r1["L"], r1["U"], r1["lev"]), route("P2 MeerKAT MIGHTEE-HI widths", p2["L"], p2["U"], p2["lev"]),
            route("P3 WALLABY DR2 gas points", r3["L"], r3["U"], r3["lev"])]


def report(label, routes):
    cb = combine(routes)
    out = dict(routes={}, combined=dict(L=cb["L"], sigma=cb["sigma"], w=cb["w"], chi2=cb["chi2"], p=cb["p"]))
    for r in routes:
        tot = math.sqrt(sum(v ** 2 for v in r["U"].values()) + sum((abs(r["lev"][k]) * SH[k]) ** 2 for k in SH))
        out["routes"][r["name"]] = dict(L=r["L"], total_sigma=tot, U=r["U"], lev=r["lev"])
    for foot in ("canonical", "alt"):
        v, pulls = verdict(cb["L"], cb["sigma"], foot)
        k = kap(cb["L"], foot); ks = k * cb["sigma"] * math.log(10)
        out[foot] = dict(kappa=k, kappa_err=ks, verdict=v, pulls=pulls)
    P(f"  [{label}] " + " | ".join(f"{n.split()[0]} {d['L']:+.4f}+-{d['total_sigma']:.4f}" for n, d in out["routes"].items())
      + f" || combined {cb['L']:+.4f} +- {cb['sigma']:.4f} (chi2 {cb['chi2']:.2f}, p {cb['p']:.2f}) || kappa_L {out['canonical']['kappa']:.3f} +- {out['canonical']['kappa_err']:.3f} "
        f"({out['canonical']['verdict']}; 1/2 at {out['canonical']['pulls']['1/2']:.2f} sig) | kappa_crit {out['alt']['kappa']:.3f} +- {out['alt']['kappa_err']:.3f} "
        f"({out['alt']['verdict']}; 1/2 at {out['alt']['pulls']['1/2']:.2f} sig)")
    return out


P2_0 = dict(L=L2_0, U=U2_0, lev=lev2)
STEPS["record_numono"] = report("record nu_mono (CFG493)", ns["PRIM"])
STEPS["K_kernel_nu1_recordP3"] = report("K kernel nu1, record P3 (reported)", mk_routes(R_K1, P2K, R_K3rec))
STEPS["K_kernel_nu1"] = report("K kernel nu1 (rebuilt P3)", mk_routes(R_K1, P2K, R_K3))
STEPS["A_aqual_disc"] = report("A AQUAL disc (v3)", mk_routes(R_A1, P2A, R_A3))
STEPS["A_thin_variant"] = report("A razor-thin variant", mk_routes(dict(R_A1t, U=R_A1["U"]), dict(P2A, L=P2K["L"] + float(np.mean(dA2t))), dict(R_A3t, U=R_A3["U"])))
P(f"  P1 C at its gas points (primary): median {np.median(np.concatenate([p[3][2] for p in p1_parts(C1p)])):.4f}; "
  f"P3: median {np.median(np.concatenate([p[4][2] for p in p3_parts(C3p) if p[4] is not None])):.4f} (at a0 = 1.05e-10)")

# ------------------------------------------------------------------ step E (EFE, gamma = 0; reported)
P("\n--- step E: EFE along the disc axis (reported only; SURVEY-CALIBRATION e_N; geometry gamma = 0)")
gx = {}
for row in csv.DictReader(open(os.path.join(REPO, "..", "gext_vectors_2026", "data", "gext_vectors.csv"))):
    gx[row["name"]] = row
GXW = {}
for row in csv.DictReader(l for l in open(os.path.join(REPO, "prep_2026", "wallaby_firing", "gext_wallaby_237.csv")) if not l.startswith("#")):
    GXW["WALLABY " + row["name"]] = row
EFE = {}
for br in ("noclu", "maxclu"):
    a1 = 10 ** R_A1["L"]; a3 = 10 ** R_A3["L"]
    j1, n1 = [], []
    for j in p1_jobs:
        if j["name"] in gx:
            gNe = 10 ** float(gx[j["name"]][f"log_eN_{br}"]) * 1.2e-10
            j1.append(dict(j, a0_list=[a1], eN_list=[gNe / a1], thin=False)); n1.append(j["name"])
    j3, n3 = [], []
    for j in p3_jobs:
        if j["name"] in GXW:
            gNe = float(GXW[j["name"]][f"eN_{br}_can936"]) * 9.36e-11
            j3.append(dict(j, a0_list=[a3], eN_list=[gNe / a3], thin=False)); n3.append(j["name"])
    r1, pk = cached_batch("job_sparc", j1, f"p1efe_{br}", 1); RSSB[f"p1efe_{br}"] = pk
    r3, pk = cached_batch("job_wallaby", j3, f"p3efe_{br}", 2); RSSB[f"p3efe_{br}"] = pk
    # C tables with the EFE value replacing the isolated one at every a0 (fixed; declared approximation)
    C1e = dict(C1p); C3e = dict(C3p)
    for r in r1:
        C1e[r["name"]] = (np.array(r["R"]), np.repeat(np.array(r["C"][0]["C"])[None, :], 4, axis=0))
    for r in r3:
        C3e[r["name"]] = (np.array(r["R"]), np.repeat(np.array(r["C"][0]["C"])[None, :], 4, axis=0))
    pE1 = p1_parts(C1e); pE3 = p3_parts(C3e)
    L1e = float(fit1C(pE1)); L3e = math.log10(fit3C(pE3))
    # same with isolated C held fixed at the fitted a0 (to isolate the EFE shift from the C(a0) treatment)
    C1f = {k: (v[0], np.repeat(Cint(v[1], R_A1["L"])[None, :], 4, axis=0)) for k, v in C1p.items()}
    C3f = {k: (v[0], np.repeat(Cint(v[1], R_A3["L"])[None, :], 4, axis=0)) for k, v in C3p.items()}
    L1f = float(fit1C(p1_parts(C1f))); L3f = math.log10(fit3C(p3_parts(C3f)))
    eNs1 = [jj["eN_list"][0] for jj in j1]; eNs3 = [jj["eN_list"][0] for jj in j3]
    EFE[br] = dict(n_P1=len(n1), n_P3=len(n3), P3_without_eN=[n for n in P3names if n not in n3],
                   dL1=L1e - L1f, dL3=L3e - L3f, eN_P1_median=float(np.median(eNs1)) if eNs1 else None,
                   eN_P3_median=float(np.median(eNs3)) if eNs3 else None)
    routesE = mk_routes(dict(R_A1, L=R_A1["L"] + EFE[br]["dL1"]), P2A, dict(R_A3, L=R_A3["L"] + EFE[br]["dL3"]))
    STEPS[f"E_efe_{br}"] = report(f"E EFE {br} (P2 unchanged: no e_N on disk)", routesE)
    P(f"     {br}: P1 {len(n1)}/12 with e_N (median e_N {EFE[br]['eN_P1_median']}), dL1 {EFE[br]['dL1']:+.4f}; "
      f"P3 {len(n3)}/{len(P3names)} with e_N (median {EFE[br]['eN_P3_median']}), dL3 {EFE[br]['dL3']:+.4f}")

# ------------------------------------------------------------------ verdict
dKA = STEPS["A_aqual_disc"]["combined"]["L"] - STEPS["K_kernel_nu1"]["combined"]["L"]
dK = STEPS["K_kernel_nu1_recordP3"]["combined"]["L"] - STEPS["record_numono"]["combined"]["L"]
dP3 = STEPS["K_kernel_nu1"]["combined"]["L"] - STEPS["K_kernel_nu1_recordP3"]["combined"]["L"]
moves = "AQUAL moves kappa" if abs(dKA) >= 0.02 else "AQUAL does not move kappa materially"
P(f"\nVERDICT (step A, v3): kappa_Lambda {STEPS['A_aqual_disc']['canonical']['kappa']:.3f} +- {STEPS['A_aqual_disc']['canonical']['kappa_err']:.3f} "
  f"({STEPS['A_aqual_disc']['canonical']['verdict']}); kappa_crit {STEPS['A_aqual_disc']['alt']['kappa']:.3f} +- {STEPS['A_aqual_disc']['alt']['kappa_err']:.3f} "
  f"({STEPS['A_aqual_disc']['alt']['verdict']}); combined log a0 shifts: kernel (record P3) {dK:+.4f}, P3 rebuilt on a smooth V_gas^2 "
  f"(record error, A6) {dP3:+.4f}, AQUAL disc {dKA:+.4f} dex -> {moves}")
RES = dict(lane="S3_v3_mw_seals", part="B", mutate=S.MUTATE, criteria="8f6c6587e1", amendments=["A1 0501ac4248", "A2 938675e060"],
           a0_grid=A0G.tolist(), steps=STEPS, efe=EFE, p2=dict(kernel_shift=dK2 / 2, aqual_shift=shiftA2, aqual_err=errA2, ref=ref),
           aqual_vs_kernel_shift=dKA, kernel_shift_recordP3=dK, p3_rebuild_shift=dP3, label=moves, max_residual=maxres, checks=CHECKS)
npass = sum(c["ok"] for c in CHECKS)
RES["runtime_s"] = round(time.time() - T0, 1)
RES["peak_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 1)
RES["child_rss_MB"] = RSSB
json.dump(RES, open(os.path.join(HERE, f"s3_partB_kappa_results{TAG}.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
P(f"\nS3_PARTB COMPLETE: {npass}/{len(CHECKS)} checks PASS.  runtime {RES['runtime_s']} s, parent peak RSS {RES['peak_rss_MB']} MB, child peaks {RSSB}")
open(os.path.join(HERE, f"s3_partB_kappa{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHECKS) else 1)
