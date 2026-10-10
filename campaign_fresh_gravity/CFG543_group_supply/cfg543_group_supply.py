#!/usr/bin/env python3
"""CFG543: the group supply gap (FROZEN_CRITERIA.md, committed alone in 4db846853).

Data re-check (D1 NGC 4936 hot gas vs Tian M_bar; KT2017 crude match, descriptive), the law for the Tian+2026 groups with
(a) hot gas (H1 census-internal, H2 NGC 4936 anchor) and (b) Re-definition brackets, and the derived supply mechanisms
(P2 progenitor containment, max-concentration bound, catchment growth, f_ret check).
kappa = 1/2 FITTED; footings 9.36e-11 / 1.13e-10 never pooled; nu_mono; round rule; no EFE; class-A edge (CFG541).
Cold energy mass required. Not "theory closed". No downloads; CFG540 / CFG515 imported read-only.
Run: OMP_NUM_THREADS=2 nice -n 10 python3 cfg543_group_supply.py ; CFG543_MUTATE=1 for the MUTATE outputs.
"""
import os, sys, json, math
os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "CFG540_vizier2026_bfjr_mhongoose"))
sys.path.insert(0, os.path.join(HERE, "..", "CFG515_census_edge_resolution"))
import cfg540_bfjr as C                                     # noqa: E402  (read-only import)
from cfg515_lib import fret_census, fret_of, COLD_PER_B, FB16, H16   # noqa: E402

if not hasattr(np, "trapezoid"): np.trapezoid = np.trapz
MUT = os.environ.get("CFG543_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
G, MSUN, KPC = C.G, C.MSUN, C.KPC
FOOT = C.FOOT
HERN_RE = C.HERN_RE
X, LX = C.X, C.LX
RHO_T = 1.0 / (2 * np.pi * X * (1 + X) ** 3)                # Hernquist tracer, GM = a = 1
M_T = X ** 2 / (1 + X) ** 2
OUT = []


def log(s=""):
    print(s); OUT.append(s)


# ------------------------------------------------------------------ data
def lovisari():
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv"))
            if not l.startswith("#") and l.strip()]
    h, rows = rows[0], rows[1:]
    g = lambda r, k: float(r[h.index(k)])
    return [dict(name=r[0], R500=g(r, "R500_kpc"), Mg500=g(r, "Mgas500_1e12") * 1e12, R2500=g(r, "R2500_kpc"),
                 Mg2500=g(r, "Mgas2500_1e12") * 1e12, M500=g(r, "M500_1e13") * 1e13) for r in rows]


def kt_match(groups):
    def rd(f):
        rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", f))
                if not l.startswith("#") and l.strip()]
        h = rows[0]
        return [x for x in rows[3:] if len(x) == len(h)]
    gal = rd("kt2017_galaxies.tsv"); grp = {x[0].strip(): x for x in rd("kt2017_groups_full.tsv")}
    ra = np.array([float(x[1]) for x in gal]); de = np.array([float(x[2]) for x in gal])
    K = np.array([float(x[4]) if x[4].strip() else 99.0 for x in gal]); p1 = [x[5].strip() for x in gal]
    out = []
    for o in groups:
        d = np.hypot((ra - o["ra"]) * math.cos(math.radians(o["de"])), de - o["de"]) * 60
        k = np.where(d < 30)[0]
        if not len(k): continue
        k = k[np.argmin(K[k])]; x = grp.get(p1[k])
        if x is None or int(x[1]) < 4 or not x[2].strip() or not x[6].strip(): continue
        out.append(dict(id=o["id"], N=int(x[1]), logK=float(x[2]), sig=float(x[4]), Rg=float(x[6]) * 1e3,
                        virgo=(x[0].strip() == "41220")))
    return out


def read_groups():
    rows = []
    for l in open(os.path.join(C.DATA, "J_A_A_710_L39.tsv")):
        if l.startswith("#"): continue
        r = l.rstrip("\n").split("\t")
        if len(r) < 13 or not r[0].strip().isdigit() or r[1].strip() != "Galaxy group": continue
        rows.append(dict(id=r[2].strip(), ra=float(r[3]), de=float(r[4]), ls=float(r[5]), els=float(r[6]), lM=float(r[7]),
                         elM=float(r[8]), Re=float(r[10])))
    return rows


# ------------------------------------------------------------------ hot-gas geometry (Lovisari-derived)
def beta_shape(r, rc):
    return r - rc * np.arctan(r / rc)


def gas_geometry(L):
    lM = np.log10([o["Mg500"] for o in L]); lR = np.log10([o["R500"] for o in L])
    B, A = np.polyfit(lM, lR, 1)
    xr = float(np.median([o["R2500"] / o["R500"] for o in L])); tg = float(np.median([o["Mg2500"] / o["Mg500"] for o in L]))
    f = lambda c: beta_shape(xr, c) / beta_shape(1.0, c) - tg
    c = brentq(f, 1e-4, 50.0, xtol=1e-14)
    k4 = abs(beta_shape(xr, c) / beta_shape(1.0, c) - tg)
    return dict(A=float(A), B=float(B), rc_over_R500=float(c), x2500=xr, mg_ratio=tg, K4=float(k4))


GEO = None


def R500_of(Mh500):
    return 10 ** (GEO["A"] + GEO["B"] * math.log10(Mh500))


# ------------------------------------------------------------------ chain: baryons, supply, sigma
def config_masses(lM, cfg):
    """returns (M_cat, M_hot, supply, f_ret_used) in Msun"""
    M = 10 ** lM
    kind = cfg["kind"]
    if kind == "C0":
        f = fret_census(M)[0]; return M, 0.0, COLD_PER_B * M / f, f
    if kind == "P1":
        fc = cfg.get("fcond", 0.10)
        Mta_h = M * H16 / (fc * FB16)
        f = max(fret_of(math.log10(Mta_h)), fc)
        Mhot = M * (f / fc - 1.0)
        return M, Mhot, COLD_PER_B * (M + Mhot) / f, f
    if kind == "P2":
        fc = cfg.get("fcond", 0.10)
        return M, 0.0, COLD_PER_B * M / fc, fc
    if kind == "P2h":
        fh = fret_census(0.5 * M)[0]
        return M, 0.0, COLD_PER_B * (0.5 * M / fh + 0.5 * M / 0.10), None
    if kind == "P3":
        Mhot = cfg["h2"] * M; f = fret_census(M + Mhot)[0]
        return M, Mhot, COLD_PER_B * (M + Mhot) / f, f
    raise ValueError(kind)


def sigma_log(o, a0, cfg, dlM=0.0, smult=1.0, newton=False, bound=False):
    lM = o["lM"] + dlM
    M, Mhot, Msup, _ = config_masses(lM, cfg)
    Msup *= smult
    Re = o["Re"] / cfg.get("k", 1.0)
    a = Re * KPC / HERN_RE
    r = X * a
    Mb = M * M_T
    if Mhot > 0:
        Rt_f = cfg.get("Rt", 1.0)
        # hot mass inside R500 fixes R500; G2 (Rt = 2 R500) keeps the total
        rc_f = GEO["rc_over_R500"]
        if Rt_f == 1.0:
            R5 = R500_of(Mhot)
        else:
            frac = beta_shape(1.0, rc_f) / beta_shape(Rt_f, rc_f)
            R5 = R500_of(Mhot * frac)
        rc = rc_f * R5 * KPC; Rt = Rt_f * R5 * KPC
        Mg = Mhot * beta_shape(np.minimum(r, Rt), rc) / beta_shape(Rt, rc)
        Mb = Mb + Mg
    gN = G * Mb * MSUN / r ** 2
    if newton:
        g = gN
    else:
        nu = C.nu(gN / a0)
        g = nu * gN
        if bound:
            g = G * (Mb + Msup) * MSUN / r ** 2 if Msup is not None else g
        elif cfg.get("edge", True):
            mph = (nu - 1.0) * Mb
            k = np.where(mph >= Msup)[0]
            if len(k):
                xe = k[0]
                g = np.where(np.arange(len(X)) > xe, G * (Mb + mph[xe]) * MSUN / r ** 2, g)
    s2 = np.trapezoid(4 * np.pi * X ** 2 * RHO_T * r * g * X, LX) / 3.0
    return 0.5 * math.log10(s2) - 3.0


def stats(D, s):
    D = np.asarray(D); n = len(D)
    m = float(D.mean()); se = float(D.std(ddof=1) / math.sqrt(n)); sys_ = float(np.mean(s) * 0.10)
    tot = math.hypot(se, sys_); Z = m / tot
    lab = "CLOSES" if abs(Z) < 2 else ("ABOVE" if Z >= 2 else "BELOW (over-corrects)")
    return dict(N=n, mean=m, se=se, sys=sys_, tot=tot, Z=Z, median=float(np.median(D)), rms=float(D.std(ddof=1)), label=lab)


def run(rows, a0, cfg, smult=1.0, newton=False, bound=False, need_s=True):
    lp = np.array([sigma_log(o, a0, cfg, 0.0, smult, newton, bound) for o in rows])
    if need_s:
        lp2 = np.array([sigma_log(o, a0, cfg, 0.01, smult, newton, bound) for o in rows])
        s = (lp2 - lp) / 0.01
    else:
        s = np.full(len(rows), 0.25)
    ls = np.array([o["ls"] for o in rows])
    D = ls - lp
    return D, s, stats(D, s)


# ------------------------------------------------------------------ checks
def k3_mc():
    rng = np.random.default_rng(543)
    vals = []
    for _ in range(4):
        N = 5000
        u = rng.random(N); su = np.sqrt(u); rr = su / (1 - su)
        ct = rng.uniform(-1, 1, N); ph = rng.uniform(0, 2 * np.pi, N); st = np.sqrt(1 - ct ** 2)
        x, y = rr * st * np.cos(ph), rr * st * np.sin(ph)
        acc = 0.0; npair = 0
        for i in range(0, N, 500):
            dx = x[i:i + 500, None] - x[None, :]; dy = y[i:i + 500, None] - y[None, :]
            R = np.hypot(dx, dy)
            ii = np.arange(i, min(i + 500, N))
            mask = ii[:, None] < np.arange(N)[None, :]
            acc += np.sum(1.0 / R[mask]); npair += mask.sum()
        vals.append(npair / acc)
    return float(np.mean(vals)) / HERN_RE, float(np.std(vals) / math.sqrt(len(vals))) / HERN_RE


def main():
    global GEO
    rows = read_groups()
    L = lovisari()
    GEO = gas_geometry(L)
    res = dict(lane="CFG543", mutate=MUT, N=len(rows), geometry=GEO, footings={})
    log(f"CFG543 {'MUTATE' if MUT else 'PRIMARY'}: Tian+2026 groups N = {len(rows)}; kappa = 1/2 FITTED; footings never pooled")

    # ---------------- D: data re-check
    n4936 = [o for o in rows if o["id"] == "NGC4936"][0]; l4936 = [o for o in L if o["name"] == "NGC4936"][0]
    h2 = l4936["Mg500"] / 10 ** n4936["lM"]
    D1 = "HOT GAS EXCLUDED" if 10 ** n4936["lM"] < l4936["Mg500"] else "NOT EXCLUDED"
    log(f"D1(i) NGC4936: Tian M_bar {10 ** n4936['lM']:.3e} vs Lovisari Mgas,500 {l4936['Mg500']:.3e} (h70; M500 {l4936['M500']:.2e}) "
        f"-> ratio {h2:.3f} -> {D1}")
    km = kt_match(rows)
    nv = [m for m in km if not m["virgo"]]
    dk = np.array([[o["lM"] for o in rows if o["id"] == m["id"]][0] - m["logK"] for m in nv])
    rg = np.array([[o["Re"] for o in rows if o["id"] == m["id"]][0] / m["Rg"] for m in nv])
    sg = np.array([10 ** [o["ls"] for o in rows if o["id"] == m["id"]][0] / m["sig"] for m in nv])
    log(f"D1(ii) crude KT2017 match (non-Virgo, N_mem >= 4): {len(nv)} groups; logMbar - log L_K median {np.median(dk):+.2f} "
        f"(16-84%: {np.percentile(dk, 16):+.2f}..{np.percentile(dk, 84):+.2f}) -> M_bar/L_K {10 ** np.median(dk):.2f}")
    log(f"D2 Re / KT Rg (projected virial radius) median {np.median(rg):.2f} (16-84%: {np.percentile(rg, 16):.2f}..{np.percentile(rg, 84):.2f}); "
        f"D3 sigma_Tian / sigma_KT median {np.median(sg):.2f}")
    res["D"] = dict(D1=D1, NGC4936_ratio=h2, NGC4936_Mbar=10 ** n4936["lM"], NGC4936_Mgas500=l4936["Mg500"], kt_N=len(nv),
                    kt_dlogMK_median=float(np.median(dk)), kt_ML_K=float(10 ** np.median(dk)), Re_over_Rg_median=float(np.median(rg)),
                    sig_ratio_median=float(np.median(sg)))
    log(f"geometry: log R500 = {GEO['A']:.3f} + {GEO['B']:.3f} log Mgas500; r_c/R500 = {GEO['rc_over_R500']:.4f} "
        f"(median R2500/R500 {GEO['x2500']:.3f}, Mgas2500/Mgas500 {GEO['mg_ratio']:.3f}); K4 {GEO['K4']:.1e} -> "
        f"{'PASS' if GEO['K4'] < 1e-6 else 'FAIL'}")
    k3, k3e = k3_mc()
    log(f"K3 MC Hernquist projected pairwise harmonic radius / R_e = {k3:.4f} +- {k3e:.4f} (analytic 6/pi/1.8153 = {6 / math.pi / HERN_RE:.4f}) -> "
        f"{'PASS' if abs(k3 - 1.052) < 0.01 else 'FAIL'}")
    res.update(K3=k3, K3_err=k3e)

    # ---------------- f_ret check (iii)
    f540 = np.array([fret_census(10 ** o["lM"])[0] for o in rows])
    f1 = np.array([config_masses(o["lM"], dict(kind="P1"))[3] for o in rows])
    hot1 = np.array([config_masses(o["lM"], dict(kind="P1"))[1] / 10 ** o["lM"] for o in rows])
    ratio = (COLD_PER_B / 0.10) / (COLD_PER_B / f540)
    log(f"(iii) CFG540 f_ret (fret_census of M_cat): median {np.median(f540):.3f} ({f540.min():.3f}-{f540.max():.3f}); "
        f"H1 f_ret(M_ta): median {np.median(f1):.3f} ({f1.min():.3f}-{f1.max():.3f}); H1 M_hot/M_cat median {np.median(hot1):.2f} "
        f"({hot1.min():.2f}-{hot1.max():.2f})")
    log(f"    containment: CFG540's M_ta below the galaxy-floor progenitor sum M_cat h/(0.10 f_b16) in {int(np.sum(f540 > 0.10 + 1e-12))}/{len(rows)} groups; "
        f"supply ratio (P2 or P1)/(CFG540) median {np.median(ratio):.2f} ({ratio.min():.2f}-{ratio.max():.2f})")
    res["fret_check"] = dict(f540_median=float(np.median(f540)), f540_min=float(f540.min()), f540_max=float(f540.max()),
                             fH1_median=float(np.median(f1)), Mhot_over_Mcat_H1_median=float(np.median(hot1)),
                             Mhot_over_Mcat_H1_min=float(hot1.min()), Mhot_over_Mcat_H1_max=float(hot1.max()),
                             n_containment_violations=int(np.sum(f540 > 0.10 + 1e-12)), supply_ratio_median=float(np.median(ratio)),
                             supply_ratio_min=float(ratio.min()), supply_ratio_max=float(ratio.max()))
    # (ii) catchment growth
    res["catchment_growth"] = {"z1": 0.5, "z2": 1.0 / 3.0, "bound": 1.0}
    log("(ii) catchment growth (EdS self-similar, M_ta ~ t^(2/3)): z = 1 / 2 catchment holds 0.50 / 0.33 of z = 0; "
        "the z = 0 catchment is the maximum to date -> supply factor <= 1.00 (cannot raise it)")

    CF = {"C0": dict(kind="C0"), "C0_noedge": dict(kind="C0", edge=False),
          "P1": dict(kind="P1"), "P1_f07": dict(kind="P1", fcond=0.07), "P1_f13": dict(kind="P1", fcond=0.13),
          "P1_G2": dict(kind="P1", Rt=2.0), "P1_noedge": dict(kind="P1", edge=False),
          "P2": dict(kind="P2"), "P2_f07": dict(kind="P2", fcond=0.07), "P2_f13": dict(kind="P2", fcond=0.13),
          "P2h": dict(kind="P2h"), "P3": dict(kind="P3", h2=h2), "P3_G2": dict(kind="P3", h2=h2, Rt=2.0)}
    for kk, k in (("R2", 1.052), ("R3", 2.104), ("R4", 3.305)):
        for b in ("C0", "P1", "P2"):
            CF[f"{b}_{kk}"] = dict(CF[b], k=k)
    if MUT:
        CF = {"C0": dict(kind="C0"), "P1": dict(kind="P1"), "P2": dict(kind="P2")}
    for fk, a0 in FOOT.items():
        log(f"\n=== footing {fk}: a0 = {a0:.3e} ===")
        # K2 deep-MOND point-mass-like check: very extended group, no edge
        o = dict(rows[0]); o["Re"] = 1e6
        lp = sigma_log(o, a0, dict(kind="C0", edge=False))
        k2 = abs(lp - (0.25 * math.log10(4 / 81 * G * 10 ** o["lM"] * MSUN * a0) - 3))
        log(f"K2 deep-MOND (4/81 G M a0)^(1/4): |diff| {k2:.4f} dex -> {'PASS' if k2 < 0.01 else 'FAIL'}")
        fr = dict(K2=k2, configs={})
        for nm, cfg in CF.items():
            D, s, st = run(rows, a0, cfg)
            fr["configs"][nm] = dict(st, Delta=[float(v) for v in D], s_mean=float(np.mean(s)))
            log(f"  {nm:12s} mean {st['mean']:+.3f}  SE {st['se']:.3f}  sys {st['sys']:.3f}  Z {st['Z']:+.2f}  med {st['median']:+.3f}  "
                f"rms {st['rms']:.3f} -> {st['label']}")
        if not MUT:
            ref = json.load(open(os.path.join(HERE, "..", "CFG540_vizier2026_bfjr_mhongoose", "cfg540_postfreeze_results.json")))[fk]
            k1a = abs(fr["configs"]["C0"]["mean"] - ref["cap_variant"]["mean"]); k1b = abs(fr["configs"]["C0_noedge"]["mean"] - ref["noedge"])
            log(f"K1 C0 vs CFG540 cap {ref['cap_variant']['mean']:+.4f}: |diff| {k1a:.4f}; no edge vs {ref['noedge']:+.4f}: |diff| {k1b:.4f} -> "
                f"{'PASS' if max(k1a, k1b) < 0.003 else 'FAIL'}")
            fr.update(K1_cap=k1a, K1_noedge=k1b)
            # max-concentration bound
            for b in ("C0", "P2", "P1"):
                D, s, st = run(rows, a0, CF[b], bound=True)
                fr["configs"][f"{b}_maxconc"] = dict(st, s_mean=float(np.mean(s)))
                log(f"  {b + '_maxconc':12s} mean {st['mean']:+.3f}  Z {st['Z']:+.2f} -> {st['label']}  (all supply at the centre: bound)")
            # supply scan (information only)
            for b in ("C0", "P1", "P2"):
                sc = {}
                tot = fr["configs"][b]["tot"]
                for mlt in (1.5, 2, 3, 5, 10, 20, 50):
                    D, _, _ = run(rows, a0, CF[b], smult=mlt, need_s=False)
                    sc[str(mlt)] = float(D.mean())
                need = next((m for m in sc if abs(sc[m]) < 2 * tot), None)
                fr["configs"][b]["supply_scan"] = sc; fr["configs"][b]["supply_factor_to_close"] = need
                log(f"  scan {b}: " + ", ".join(f"x{m} {v:+.3f}" for m, v in sc.items()) + f"  -> |mean| < 2 sigma_tot at x{need} (information only)")
        else:
            mu = {}
            for b in ("P1", "P2"):
                D0 = fr["configs"][b]["mean"]
                D, s, st = run(rows, a0, CF[b], smult=0.3)
                mu[f"M1_{b}"] = dict(mean=st["mean"], rise=st["mean"] - D0, bites=bool(st["mean"] - D0 >= 0.02))
                log(f"  M1 supply x0.3 {b}: mean {st['mean']:+.3f} (rise {st['mean'] - D0:+.3f}) -> {'BITES' if st['mean'] - D0 >= 0.02 else 'DOES NOT BITE'}")
                D, s, st = run(rows, a0, CF[b], newton=True)
                mu[f"M3_{b}"] = dict(mean=st["mean"], Z=st["Z"], label=st["label"], bites=st["label"] != "CLOSES")
                log(f"  M3 Newtonian {b}: mean {st['mean']:+.3f} Z {st['Z']:+.2f} -> {st['label']} -> {'BITES' if st['label'] != 'CLOSES' else 'DOES NOT BITE'}")
            Dt = np.array(fr["configs"]["P2"]["Delta"]); ls = np.array([o["ls"] for o in rows]); lp = ls - Dt
            rng = np.random.default_rng(543); n_gt = 0
            for _ in range(200):
                lsh = rng.permutation(ls)
                n_gt += (lsh - lp).std(ddof=1) > Dt.std(ddof=1)
            mu["M2_P2"] = dict(frac=float(n_gt) / 200, bites=bool(n_gt / 200 >= 0.95), true_rms=float(Dt.std(ddof=1)))
            log(f"  M2 sigma shuffle P2: rms grows in {n_gt}/200 -> {'BITES' if n_gt >= 190 else 'per-group tracking NOT DEMONSTRATED'}")
            fr["mutate"] = mu
        res["footings"][fk] = fr

    if not MUT:
        # verdict per footing
        V = {}
        for fk in FOOT:
            c = res["footings"][fk]["configs"]
            labs = []
            p1, p2 = c["P1"]["label"], c["P2"]["label"]
            if D1 == "HOT GAS EXCLUDED" and p1 == "CLOSES": labs.append("DATA-ISSUE (stars-only M_bar fed to the gas+stars census)")
            if p2 == "CLOSES": labs.append("MECHANISM FOUND (progenitor containment)")
            if p1 != "CLOSES" and p2 != "CLOSES" and c["P2_maxconc"]["Z"] >= 2:
                labs.append(f"GENUINE TENSION (Z P1 {c['P1']['Z']:+.2f}, P2 {c['P2']['Z']:+.2f})")
            nd = []
            if p1.startswith("BELOW") and p2 == "ABOVE": nd.append("P1 over-corrects while P2 is ABOVE")
            for b in ("P1", "P2"):
                if c[b]["label"] != "CLOSES" and any(c[k]["label"] == "CLOSES" for k in c if k.startswith(b + "_f") or k == b + "_G2"):
                    nd.append(f"{b} closes only inside a bracket")
            redep = [k for k in c if k.split("_")[-1] in ("R2", "R3", "R4") and k.split("_")[0] in ("P1", "P2")
                     and c[k]["label"] != c[k.split("_")[0]]["label"]]
            V[fk] = dict(labels=labs, nd_reasons=nd, re_dependent=redep)
        same = V["can"]["labels"] == V["alt"]["labels"]
        res["verdict"] = dict(per_footing=V, footings_agree=same)
        log("\n=== VERDICT (frozen rule) ===")
        for fk in FOOT:
            log(f"  {fk}: labels {V[fk]['labels'] or ['(none)']}; NOT DIAGNOSTIC triggers {V[fk]['nd_reasons'] or ['none']}; "
                f"Re-dependent variants {V[fk]['re_dependent'] or ['none']}")
        log(f"  footings agree: {same}")
    json.dump(res, open(os.path.join(HERE, f"cfg543_results{TAG}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg543_group_supply{TAG}.out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
