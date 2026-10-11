"""CFG631 shared builders: per-galaxy PROPERTY tables (SPARC, WALLABY, KiDS f30 early types). No law residual is computed here.
Residual machinery is borrowed at run time from CFG537 (discs) and CFG531/585 (KiDS) by executing their heads unedited.
"""
import os, io, csv, json, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
DATA = os.path.join(REPO, "real_research", "data")
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
os.environ.setdefault("OMP_NUM_THREADS", "1")


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return float("nan")


def unit(a, d):
    a, d = np.radians(np.asarray(a, float)), np.radians(np.asarray(d, float))
    return np.stack([np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)], axis=-1)


def nearest(u, U):
    with np.errstate(all="ignore"):
        s = np.degrees(np.arccos(np.clip(U @ u, -1, 1))) * 3600
    i = int(np.nanargmin(s)); return i, float(s[i])


def run_head(path, cut, env_drop=()):
    for v in env_drop:
        os.environ.pop(v, None)
    src = open(path).read(); assert src.count(cut) >= 1
    ns = {"__file__": path, "__name__": "head"}
    with contextlib.redirect_stdout(io.StringIO()), np.errstate(all="ignore"):
        exec(compile(src.split(cut)[0], path, "exec"), ns)
    return ns


def load_rc3():
    rc = []
    for line in open(os.path.join(DATA, "rc3_devaucouleurs1991_colors.tsv")):
        p = line.rstrip("\n").split("\t")
        if len(p) < 14:
            continue
        a, d = fnum(p[0]), fnum(p[1])
        if np.isfinite(a) and np.isfinite(d):
            rc.append(dict(ra=a, dec=d, BT=fnum(p[6]), BVo=fnum(p[10]), Ai=fnum(p[12]), Ag=fnum(p[13])))
    return rc, unit([r["ra"] for r in rc], [r["dec"] for r in rc])


# ------------------------------------------------------------------ discs: CFG537 head (data build + residual functions)
def cfg537_head():
    return run_head(os.path.join(LANES, "CFG537_outer_excess_independent", "cfg537_wallaby.py"),
                    "# ================================================================== power forecast", ("CFG537_MUTATE",))


def sparc_props(ns):
    """Per-galaxy properties for CFG537's SPARC sample SAMP (same order as ns['sparc_rows'] output)."""
    rc, U3 = load_rc3()
    pos = json.load(open(os.path.join(DATA, "sparc_positions_merged.json")))
    env = {}
    rows = open(os.path.join(DATA, "sparc_a0_environment_table.csv")).read().splitlines()
    hdr = rows[0].split(",")
    for r in rows[1:]:
        v = dict(zip(hdr, r.split(","))); env[v["name"]] = fnum(v["onepd_2mpp"])
    out = []
    for g in ns["SAMP"]:
        m = g["m"]; nm = g["name"]
        a = np.loadtxt(os.path.join(DATA, "sparc_data", f"{nm}_rotmod.dat"), comments="#")
        R, SBb = a[:, 0], a[:, 7]
        Lb = 2 * math.pi * np.trapz(SBb * (R * 1e3), R * 1e3) / 1e9 if np.any(SBb > 0) else 0.0   # 1e9 Lsun (as L36)
        Ld = max(m["L36"] - Lb, 0.0)
        Ms, Mg = 0.5 * m["L36"], 1.33 * m["MHI"]                       # CFG537's M_b definition (1e9 Msun)
        Rd = m["Rdisk"]
        col = np.nan
        p = pos.get(nm)
        if p and p.get("ra") is not None:
            i, s = nearest(unit(p["ra"], p["dec"]), U3)
            if s <= 30 and np.isfinite(rc[i]["BT"]):
                B0 = rc[i]["BT"] - (rc[i]["Ag"] if np.isfinite(rc[i]["Ag"]) else 0.0) - (rc[i]["Ai"] if np.isfinite(rc[i]["Ai"]) else 0.0)
                m36 = 3.24 - 2.5 * math.log10(m["L36"] * 1e9) + 5 * math.log10(m["D"] * 1e6 / 10)
                col = B0 - m36
        e = env.get(nm, np.nan)
        out.append(dict(name=nm, lMb=math.log10((Ms + Mg) * 1e9), fgas=Mg / (Ms + Mg),
                        fbul=(0.7 * Lb / (0.5 * Ld + 0.7 * Lb)) if (0.5 * Ld + 0.7 * Lb) > 0 else 0.0,
                        bul=float(((0.7 * Lb / (0.5 * Ld + 0.7 * Lb)) if (0.5 * Ld + 0.7 * Lb) > 0 else 0.0) > 0.05),
                        lSig=math.log10(Ms * 1e9 / (2 * math.pi * (Rd * 1e3) ** 2)) if Rd > 0 else np.nan,
                        T=float(m["T"]), inc=float(m["Inc"]), HF=float(int(m["fD"]) == 1),
                        colour=col, env=math.log10(e) if np.isfinite(e) and e > 0 else np.nan,
                        nout=int((g["R"] >= 3 * Rd).sum())))
    return out


def wallaby_props(ns):
    w12 = {}
    for r in csv.DictReader(open(os.path.join(EXT, "wallaby_dr2", "allwise_wallaby_dr2.csv"))):
        w12[r["wallaby_name"]] = fnum(r.get("w1mpro")) - fnum(r.get("w2mpro"))
    out = []
    for g in ns["GALS"]:
        r = ns["best"][g["name"]]
        out.append(dict(name=g["name"], lMb=g["lMb"], fgas=g["Mg"] / (g["Ms"] + g["Mg"]),
                        lSig=math.log10(g["Ms"] / (2 * math.pi * (g["Rd"] * 1e3) ** 2)) if g["Rd"] > 0 else np.nan,
                        T=float(g["T"]), inc=fnum(r["Inc_model"]), W12=w12.get(g["name"], np.nan), nout=g["nout"]))
    return out


# ------------------------------------------------------------------ KiDS: CFG585 head (CFG531 estimator) + CFG509 counts head
KPROPS = ("ur", "rK", "lssfr", "z", "env")


def kids_heads():
    A = run_head(os.path.join(LANES, "CFG585_age_settling", "cfg585_age.py"), 'P("=" * 100)', ("CFG585_MUTATE", "CFG531_MUTATE"))
    B = run_head(os.path.join(LANES, "CFG509_split_satellite_leakage", "cfg509_counts.py"), "NAMES = [")
    return A, B


def kids_props(A, B):
    """Raw per-lens properties for all lenses (CFG531 order) and the partial residual of each property within f30 early
    types: OLS on [log M* quintile dummies, log M*, all OTHER properties]. Returns (raw, partial, valid mask E2)."""
    Lp, o, ix = A["Lp"], A["o"], A["ix"]
    j = o[ix]
    rK = np.asarray(Lp["MAG_ABS_r"], float)[j] - np.asarray(Lp["MAG_ABS_Ks"], float)[j]
    sfr = np.asarray(Lp["SFR_BEST"], float)[j]
    lm = A["LMSL"]
    raw = dict(ur=A["U"], rK=rK, lssfr=np.where(sfr > -90, sfr - lm, np.nan), z=np.asarray(A["lens"]["z"], float), env=B["meas"])
    E = A["E"]
    E2 = E.copy()
    for k in KPROPS:
        E2 &= np.isfinite(raw[k])
    E2 &= np.abs(rK) < 10
    qb = np.quantile(lm[E2], np.linspace(0, 1, 6)); qid = np.clip(np.searchsorted(qb, lm, side="right") - 1, 0, 4)
    Dm = [(qid[E2] == q).astype(float) for q in range(5)] + [lm[E2]]
    part = {}
    for k in KPROPS:
        X = np.column_stack(Dm + [raw[kk][E2] for kk in KPROPS if kk != k])
        y = raw[k][E2]; b = np.linalg.lstsq(X, y, rcond=None)[0]
        v = np.full(len(lm), np.nan); v[E2] = y - X @ b; part[k] = v
    return raw, part, E2, qid
