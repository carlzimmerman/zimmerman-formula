#!/usr/bin/env python3
"""CFG537 Part B (FROZEN_CRITERIA.md, criteria commit 4d77eb8da): SPARC robustness, NOT a replication.
Does CFG534's early-type outer excess survive when the stellar M/L is free per galaxy within 3.6 micron bounds (Upsilon_d 0.30-0.80,
Upsilon_b = 1.4 Upsilon_d)?  B1 global fit; B2 inner-fit (R <= 1.5 Rd); B3 extreme early 0.8 / late 0.3 bound (reported).
CFG537_MUTATE=1 -> B-MU1 (T shuffled within bins, 200x), outputs *_MUTATE.*
Run: nice -n 10 python3 cfg537_sparc_ml.py > cfg537_sparc_ml.out ; CFG537_MUTATE=1 nice -n 10 python3 cfg537_sparc_ml.py > cfg537_sparc_ml_MUTATE.out
"""
import os, json, math
import numpy as np

os.environ.setdefault("OMP_NUM_THREADS", "2")
try:
    os.nice(10)
except OSError:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data")
MUT = os.environ.get("CFG537_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
LOG, CHK = [], {}
RES = {"lane": "CFG537", "part": "B (SPARC free-M/L robustness; not a replication)", "mutate": MUT, "criteria_commit": "4d77eb8da",
       "settings": "kappa = 1/2 FITTED; footings never pooled; nu(y)=1/(1-exp(-sqrt y)); cold energy mass still required; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
CONV = 3.0857e19 / 1e6
EDG = np.arange(7.0, 12.2 + 1e-9, 0.4)
GRID = np.round(np.arange(0.30, 0.80 + 1e-9, 0.01), 2)


def nu(y):
    y = np.maximum(y, 1e-300)
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def wmean(r, w, m):
    m = m & np.isfinite(r)
    return float((r[m] * w[m]).sum() / w[m].sum()) if m.sum() >= 2 else np.nan


def matched(rows, key, early):
    x = np.array([r[key] for r in rows]); lm = np.array([r["lMb"] for r in rows])
    num = den = 0.0; nb = ne = nl = 0
    for lo, hi in zip(EDG[:-1], EDG[1:]):
        m = (lm >= lo) & (lm < hi) & np.isfinite(x)
        a, b = x[m & early], x[m & ~early]
        if len(a) >= 2 and len(b) >= 2:
            v = a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)
            num += (a.mean() - b.mean()) / v; den += 1 / v; nb += 1; ne += len(a); nl += len(b)
    if den == 0:
        return dict(diff=np.nan, sig=np.nan, Z=np.nan, nbins=0)
    return dict(diff=num / den, sig=den ** -0.5, Z=num / den ** 0.5, nbins=nb, n_early=ne, n_late=nl)


keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
TAB = {}
for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    tok = line.split()
    if len(tok) != 19:
        continue
    try:
        TAB[tok[0]] = dict(zip(keys, [float(t) for t in tok[1:18]]))
    except ValueError:
        continue
SAMP = []
for f in sorted(os.listdir(os.path.join(DATA, "sparc_data"))):
    if not f.endswith("_rotmod.dat"):
        continue
    d = np.genfromtxt(os.path.join(DATA, "sparc_data", f), comments="#")
    nm = f.replace("_rotmod.dat", "")
    if d.ndim != 2 or d.shape[1] < 6 or nm not in TAB:
        continue
    g = dict(name=nm, R=d[:, 0], V=d[:, 1], eV=d[:, 2], Vg=d[:, 3], Vd=d[:, 4], Vb=d[:, 5], m=TAB[nm])
    if int(g["m"]["Q"]) <= 2 and g["m"]["Inc"] >= 30:
        SAMP.append(g)
P(f"SPARC Q<=2 & Inc>=30: {len(SAMP)}")


def resid(g, a0, ud):
    Vb2 = g["Vg"] * np.abs(g["Vg"]) + ud * g["Vd"] ** 2 + 1.4 * ud * g["Vb"] ** 2
    gb = Vb2 / g["R"]; gobs = g["V"] ** 2 / g["R"]; ok = (gb > 0) & (gobs > 0)
    r = np.full(len(g["R"]), np.nan); r[ok] = np.log10(gobs[ok] / (nu(gb[ok] / a0) * gb[ok]))
    w = 1.0 / ((2 * g["eV"] / np.maximum(g["V"], 1e-3) / math.log(10)) ** 2 + 0.05 ** 2)
    return r, ok, w


def fit_ups(g, a0, region):
    Rd = g["m"]["Rdisk"]
    best, bu = np.inf, np.nan
    for u in GRID:
        r, ok, w = resid(g, a0, u)
        m = ok & np.isfinite(r)
        if region == "inner":
            m = m & (g["R"] <= 1.5 * Rd)
        if m.sum() < 2:
            return np.nan
        c = float((w[m] * r[m] ** 2).sum())
        if c < best:
            best, bu = c, u
    return bu


def rows_for(a0, ups_of):
    rows = []
    for g in SAMP:
        u = ups_of(g)
        r, ok, w = resid(g, a0, u)
        Rd = g["m"]["Rdisk"]
        di, do = wmean(r, w, ok & (g["R"] <= 1.5 * Rd)), wmean(r, w, ok & (g["R"] >= 3 * Rd))
        Ms, Mg = 0.5 * g["m"]["L36"], 1.33 * g["m"]["MHI"]          # bin assignment at CFG534's fixed Upsilon (frozen)
        rows.append(dict(name=g["name"], T=int(g["m"]["T"]), lMb=math.log10((Ms + Mg) * 1e9), ups=float(u), d_in=di, d_out=do,
                         d_oi=do - di if np.isfinite(do) and np.isfinite(di) else np.nan))
    return rows


OUT = {}
for foot in FOOTS:
    a0 = A0SI[foot] * CONV
    early_of = {g["name"]: int(g["m"]["T"]) <= 3 for g in SAMP}
    U1 = {g["name"]: fit_ups(g, a0, "all") for g in SAMP}
    U2 = {}
    for g in SAMP:
        u = fit_ups(g, a0, "inner"); U2[g["name"]] = 0.5 if not np.isfinite(u) else u
    n_inner_fit = sum(np.isfinite(fit_ups(g, a0, "inner")) for g in SAMP)
    V = {"B0 fixed 0.5": rows_for(a0, lambda g: 0.5), "B1 global free": rows_for(a0, lambda g: U1[g["name"]]),
         "B2 inner-fit": rows_for(a0, lambda g: U2[g["name"]]), "B3 early 0.8 / late 0.3": rows_for(a0, lambda g: 0.8 if early_of[g["name"]] else 0.3)}
    o = {}
    if not MUT:
        P(f"\n[{foot}] (B2: {n_inner_fit} galaxies have >= 2 inner points and get an inner-fit Upsilon; others keep 0.5)")
    for nm, rows in V.items():
        T = np.array([r["T"] for r in rows]); early = T <= 3
        res = {k: matched(rows, k, early) for k in ("d_out", "d_in", "d_oi")}
        lu = np.log10([r["ups"] for r in rows]); lm = np.array([r["lMb"] for r in rows])
        ups_rows = [dict(lMb=r["lMb"], lu=math.log10(r["ups"])) for r in rows]
        res["dlogUps"] = matched(ups_rows, "lu", early)
        ua = np.array([r["ups"] for r in rows])
        res["frac_at_bounds"] = {c: dict(lo=float(np.mean(ua[sel] <= 0.30 + 1e-9)), hi=float(np.mean(ua[sel] >= 0.80 - 1e-9)),
                                         median=float(np.median(ua[sel])))
                                 for c, sel in (("early", early), ("late", ~early))}
        o[nm] = res; o[nm]["_rows"] = rows
        if not MUT:
            P(f"  {nm:24s}: d_out {res['d_out']['diff']:+.4f} +- {res['d_out']['sig']:.4f} (Z {res['d_out']['Z']:+.2f}); "
              f"d_in {res['d_in']['diff']:+.4f} (Z {res['d_in']['Z']:+.2f}); d_oi {res['d_oi']['diff']:+.4f} (Z {res['d_oi']['Z']:+.2f}); "
              f"dlogUps(E-L) {res['dlogUps']['diff']:+.3f} (Z {res['dlogUps']['Z']:+.2f}); Ups median E/L {res['frac_at_bounds']['early']['median']:.2f}/"
              f"{res['frac_at_bounds']['late']['median']:.2f}; at 0.8 E/L {res['frac_at_bounds']['early']['hi']:.2f}/{res['frac_at_bounds']['late']['hi']:.2f}; "
              f"at 0.3 E/L {res['frac_at_bounds']['early']['lo']:.2f}/{res['frac_at_bounds']['late']['lo']:.2f}")
    OUT[foot] = o

if not MUT:
    ref = {"canonical": 0.07125, "alt": 0.07215}
    check("B-C1 fixed Upsilon 0.5 reproduces CFG534 Delta_out to 1e-6 (JSON 0.0712.. / 0.07215..)",
          all(abs(OUT[f]["B0 fixed 0.5"]["d_out"]["diff"] - json.load(open(os.path.join(os.path.dirname(HERE), "CFG534_history_dependent_settling",
              "cfg534_sparc_sluggs_results.json")))["sparc"][f]["d_out"]["diff"]) < 1e-6 for f in FOOTS),
          f"{OUT['canonical']['B0 fixed 0.5']['d_out']['diff']:+.6f} / {OUT['alt']['B0 fixed 0.5']['d_out']['diff']:+.6f}")
    VER = {}
    for f in FOOTS:
        z1 = OUT[f]["B1 global free"]["d_out"]; z2 = OUT[f]["B2 inner-fit"]["d_out"]
        if z1["diff"] > 0 and z1["Z"] >= 2 and z2["diff"] > 0 and z2["Z"] >= 2:
            v = "EXCESS SURVIVES M/L"
        elif z1["Z"] < 1 or z2["Z"] < 1:
            v = "ABSORBED BY M/L"
        else:
            v = "PARTIAL"
        VER[f] = v
        P(f"\n[{f}] M/L VERDICT: {v}  (B1 Z {z1['Z']:+.2f}, B2 Z {z2['Z']:+.2f})")
    head = VER["canonical"] if VER["canonical"] == VER["alt"] else f"FOOTING-DEPENDENT (canonical {VER['canonical']} / alt {VER['alt']})"
    P(f"HEADLINE (Part B): {head}")
    RES["verdict"] = VER; RES["headline"] = head
else:
    MU = {}
    for foot in FOOTS:
        rows = OUT[foot]["B1 global free"]["_rows"]; T = np.array([r["T"] for r in rows]); lm = np.array([r["lMb"] for r in rows])
        rng = np.random.default_rng(5371); zs = []
        for _ in range(200):
            Tsh = T.copy()
            for lo, hi in zip(EDG[:-1], EDG[1:]):
                idx = np.where((lm >= lo) & (lm < hi))[0]
                Tsh[idx] = rng.permutation(Tsh[idx])
            zs.append(matched(rows, "d_out", Tsh <= 3)["Z"])
        zs = np.array(zs); zs = zs[np.isfinite(zs)]
        MU[foot] = dict(mean_Z=float(zs.mean()), sd_Z=float(zs.std()), frac_Z_ge_2=float((zs >= 2).mean()))
        check(f"B-MU1 [{foot}] T shuffled within bins kills B1 Delta_out: |mean Z| < 0.5", abs(zs.mean()) < 0.5,
              f"mean Z {zs.mean():+.3f} (sd {zs.std():.2f}; P(Z>=2) {(zs >= 2).mean():.3f})")
    RES["mutate"] = MU

for f in OUT:
    for nm in OUT[f]:
        rows = OUT[f][nm].pop("_rows")
        if nm == "B1 global free" and not MUT:
            OUT[f][nm]["per_galaxy_ups"] = {r["name"]: r["ups"] for r in rows}
RES["variants"] = OUT
RES["checks"] = CHK
P(f"\n{sum(c['ok'] for c in CHK.values())}/{len(CHK)} checks pass")
json.dump(RES, open(os.path.join(HERE, f"cfg537_sparc_ml_results{SUF}.json"), "w"), indent=1,
          default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
