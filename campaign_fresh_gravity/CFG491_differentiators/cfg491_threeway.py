#!/usr/bin/env python3
"""CFG491 -- the on-disk three-way test: framework (candidate B, no EFE) vs DMO-LCDM vs standard MOND (with EFE)
on SPARC + Chae+2021 environmental fields.  Frozen: FROZEN_CRITERIA.md (committed alone first, 788eeec2c).
Statistics: S1 = EFE slope beta (partial on mean log x), S2 = RAR tightness (CFG476's statistic).
Run from anywhere:  python3 cfg491_threeway.py      MUTATE:  CFG491_MUTATE=1 python3 cfg491_threeway.py
kappa = 1/2 is FITTED; both footings, never pooled; the cold mass is still required; no particle is added."""
import os, sys, io, csv, json, math, time, hashlib, contextlib
import numpy as np
from scipy.optimize import minimize_scalar, brentq

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
MUT = os.environ.get("CFG491_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
SLUG = "cfg491_threeway" + TAG
ENV = os.path.join(C.REPO, "real_research", "reviews", "directional_efe_2026", "laneB_data", "chae21_env.csv")
FROZEN = os.path.join(HERE, "FROZEN_CRITERIA.md")
G, MSUN, KPC, H = 6.674e-11, 1.989e30, 3.0857e19, 0.7
RHOC = 3 * (H * 100 * 1e3 / 3.0857e22) ** 2 / (8 * math.pi * G)
GDAG = 1.2e-10
AF = {"canonical": C.A0["canonical"], "alt": C.A0["alt"]}
NMOCK = 300
OUT, LOG = {"lane": "CFG491", "mutate": MUT, "checks": {}, "footings": {}}, []
t0 = time.time()


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, ok, msg, load_bearing=True):
    OUT["checks"][name] = dict(ok=bool(ok), msg=str(msg), load_bearing=load_bearing)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


P(f"CFG491 three-way test{' -- MUTATE (data := one standard-MOND realisation, seed 4910)' if MUT else ''}")
P(f"  FROZEN_CRITERIA.md sha256 {hashlib.sha256(open(FROZEN, 'rb').read()).hexdigest()}")


# ------------------------------------------------------------------------------------------------ kernels + 1-D AQUAL EFE
def nu_rar(z):
    z = np.maximum(np.asarray(z, float), 1e-300); return 1.0 / (-np.expm1(-np.sqrt(z)))


def nu_mono(z):
    return np.asarray(C.nu_mono(np.maximum(np.asarray(z, float), 1e-300)), float)


KER = {"mono": nu_mono, "rar": nu_rar}
_LZ = np.linspace(-16.0, 6.0, 44001)
_FT = {k: np.log10(KER[k](10 ** _LZ) * 10 ** _LZ) for k in KER}


def Ff(k, z):
    return KER[k](z) * np.asarray(z, float)


def Finv(k, e):
    ea = np.maximum(np.abs(np.asarray(e, float)), 1e-14)
    return 10 ** np.interp(np.log10(ea), _FT[k], _LZ)


def nu_e(k, z, e):
    z = np.maximum(np.asarray(z, float), 1e-300); ze = Finv(k, e)
    return (Ff(k, z + ze) - e) / z


# ------------------------------------------------------------------------------------------------ data
env = {r["galaxy"].strip(): r for r in csv.DictReader(open(ENV))}


def prep(g):
    R = g["R"] * KPC
    gb = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2) * 1e6 / R
    ok = (gb > 0) & (g["Vobs"] > 0)
    m = g["meta"]
    L = m["L36"] * 1e9
    vb2 = g["Vbul"][-1] ** 2; vd2 = g["Vdisk"][-1] ** 2; fb = vb2 / max(vb2 + vd2, 1e-9)
    Ms = L * (0.5 * (1 - fb) + 0.7 * fb)
    return dict(name=g["name"], R=R[ok], gb=gb[ok], V=g["Vobs"][ok], eV=np.clip(g["eV"][ok], 1, None),
                Vg=g["Vgas"][ok], Vd=g["Vdisk"][ok], Vb=g["Vbul"][ok], lMs=math.log10(max(Ms, 1e6)),
                D=m["D"], eD=(m["eD"] if m["eD"] > 0 else 0.1 * m["D"]), inc=m["Inc"], einc=max(m["eInc"], 0.5))


ALL = [g for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2]
K476 = [d for d in (prep(g) for g in ALL) if len(d["R"]) >= 3]
SAMPLE = []
for g in ALL:
    if g["meta"]["Inc"] < 30 or g["name"] not in env:
        continue
    d = prep(g)
    if len(d["R"]) < 5:
        continue
    r = env[g["name"]]
    a, b = float(r["log_eN_maxclu"]), float(r["log_eN_noclu"])
    ea, eb = float(r["e_log_eN_maxclu"]), float(r["e_log_eN_noclu"])
    d["lN"] = 0.5 * (a + b); d["slN"] = math.sqrt(0.5 * (ea ** 2 + eb ** 2) + (0.5 * (a - b)) ** 2)
    SAMPLE.append(d)
P(f"  sample: {len(SAMPLE)} SPARC galaxies (Q <= 2, Inc >= 30, in Chae+2021 env, >= 5 points); CFG476 sample {len(K476)}")


def concat(gals):
    idx = np.concatenate([np.full(len(d["R"]), i) for i, d in enumerate(gals)])
    cat = {k: np.concatenate([d[k] for d in gals]) for k in ("R", "gb", "V", "eV", "Vg", "Vd", "Vb")}
    cat["idx"] = idx
    for k in ("lMs", "D", "eD", "inc", "einc"):
        cat["g_" + k] = np.array([d[k] for d in gals])
    if "lN" in gals[0]:
        cat["g_lN"] = np.array([d["lN"] for d in gals]); cat["g_slN"] = np.array([d["slN"] for d in gals])
    return cat


CS, C476 = concat(SAMPLE), concat(K476)


# ------------------------------------------------------------------------------------------------ LCDM pieces (CFG476's recipe)
def moster(lMh):
    Mh = 10 ** lMh; M1 = 10 ** 11.590
    return math.log10(2 * 0.0351 * Mh / ((Mh / M1) ** -1.376 + (Mh / M1) ** 0.608))


def inv_moster(lMs):
    return brentq(lambda x: moster(x) - lMs, 9.0, 15.5)


def halo_base(cat):
    l0, sl = [], []
    for lMs in cat["g_lMs"]:
        h = inv_moster(lMs); e = 1e-3
        l0.append(h); sl.append((moster(h + e) - moster(h - e)) / (2 * e))
    return np.array(l0), np.array(sl)


for cat in (CS, C476):
    cat["g_lMh0"], cat["g_slope"] = halo_base(cat)


def nfw_g(Mh, r, c):
    R200 = (3 * Mh * MSUN / (4 * math.pi * 200 * RHOC)) ** (1 / 3); rs = R200 / c
    m = lambda x: np.log(1 + x) - x / (1 + x)
    return G * Mh * MSUN * m(r / rs) / m(c) / r ** 2


def c_dm(Mh):
    return 10 ** (0.905 - 0.101 * np.log10(Mh * H / 1e12))


# ------------------------------------------------------------------------------------------------ the generator
def mock(cat, model, aF, rng, nuisance=True):
    """returns the observer-inferred g_obs and V for one realisation of `model` (F, L, M, Msame)."""
    ng, ix = len(cat["g_D"]), cat["idx"]
    if nuisance:
        ud, ub, ug = (10 ** rng.normal(0, s, ng) for s in (0.10, 0.10, 0.04))
        Dt = np.maximum(cat["g_D"] * (1 + rng.normal(0, 1, ng) * cat["g_eD"] / cat["g_D"]), 0.3 * cat["g_D"])
        it = np.clip(cat["g_inc"] + rng.normal(0, 1, ng) * cat["g_einc"], 10, 89)
    else:
        ud = ub = ug = np.ones(ng); Dt = cat["g_D"].copy(); it = cat["g_inc"].copy()
    fD = (Dt / cat["g_D"])[ix]
    gbt = (ug[ix] * np.sign(cat["Vg"]) * cat["Vg"] ** 2 + ud[ix] * 0.5 * cat["Vd"] ** 2 + ub[ix] * 0.7 * cat["Vb"] ** 2) * 1e6 / cat["R"]
    gbt = np.maximum(gbt, 1e-16)
    Rt = cat["R"] * fD
    if model == "F":
        g = nu_mono(gbt / aF) * gbt
    elif model == "L":
        Mh = 10 ** (cat["g_lMh0"] + rng.normal(0, 0.15, ng) / cat["g_slope"])
        c = c_dm(Mh) * 10 ** rng.normal(0, 0.11, ng)
        g = gbt + nfw_g(Mh[ix], Rt, c[ix])
    else:
        lN = cat["g_lN"] + (rng.normal(0, 1, ng) * cat["g_slN"] if nuisance else 0)
        gNe = (10 ** lN * GDAG)[ix]
        if model == "M":
            e = Ff("rar", gNe / GDAG); g = nu_e("rar", gbt / GDAG, e) * gbt
        else:
            e = Ff("mono", gNe / aF); g = nu_e("mono", gbt / aF, e) * gbt
    Vt = np.sqrt(np.maximum(g, 0) * Rt) / 1e3
    Vo = Vt * np.sin(np.radians(it[ix])) / np.sin(np.radians(cat["g_inc"][ix])) + rng.normal(0, 1, len(Vt)) * cat["eV"]
    Vo = np.clip(Vo, 1, None)
    return (Vo * 1e3) ** 2 / cat["R"], Vo


# ------------------------------------------------------------------------------------------------ statistics
def S2(cat, go, V):
    lgo, lgb = np.log10(go), np.log10(cat["gb"]); w = 1 / (cat["eV"] / V) ** 2
    f = lambda la: np.sum(w * (lgo - lgb - np.log10(nu_mono(cat["gb"] / 10 ** la))) ** 2) / np.sum(w)
    r = minimize_scalar(f, bounds=(-11.5, -9.0), method="bounded", options={"xatol": 1e-5})
    return math.sqrt(r.fun), 10 ** r.x


def template(cat, aF):
    """per-galaxy D_i, X_i and the S1 membership (>= 3 points with x < 1)."""
    x = cat["gb"] / aF; ix = cat["idx"]; ng = len(cat["g_D"])
    e = Ff("mono", 10 ** cat["g_lN"] * GDAG / aF)[ix]
    d = np.log10(nu_e("mono", x, e)) - np.log10(nu_mono(x))
    sel = x < 1
    cnt = np.bincount(ix[sel], minlength=ng)
    keep = cnt >= 3
    Dm = np.bincount(ix[sel], weights=d[sel], minlength=ng) / np.maximum(cnt, 1)
    Xm = np.bincount(ix[sel], weights=np.log10(x[sel]), minlength=ng) / np.maximum(cnt, 1)
    return dict(sel=sel, cnt=cnt, keep=keep, D=Dm, X=Xm)


def beta(cat, go, aF, T, return_all=False, gal_idx=None):
    x = cat["gb"] / aF; ix = cat["idx"]; ng = len(cat["g_D"])
    r = np.log10(go) - np.log10(nu_mono(x) * cat["gb"])
    Rm = np.bincount(ix[T["sel"]], weights=r[T["sel"]], minlength=ng) / np.maximum(T["cnt"], 1)
    k = np.where(T["keep"])[0] if gal_idx is None else gal_idx
    A = np.vstack([np.ones(len(k)), T["D"][k], T["X"][k]]).T
    coef = np.linalg.lstsq(A, Rm[k], rcond=None)[0]
    return (float(coef[1]), Rm) if return_all else float(coef[1])


def pval(m, d):
    m = np.asarray(m); n = len(m)
    return max(2 * min(np.mean(m <= d), np.mean(m >= d)), 1.0 / n)


# ------------------------------------------------------------------------------------------------ controls
P("\nCONTROLS")
k1, _ = S2(C476, (C476["V"] * 1e3) ** 2 / C476["R"], C476["V"])
check("K1", abs(k1 - 0.0994) <= 0.0005, f"S2 on CFG476's sample = {k1:.4f} dex (CFG476 0.0994)")
zz = 10 ** np.linspace(-3, 1, 200)
k2 = max(float(np.max(np.abs(nu_e(k, zz, 1e-12) / KER[k](zz) - 1))) for k in KER)
check("K2", k2 < 1e-6, f"max |nu_e(z; 1e-12)/nu(z) - 1| = {k2:.2e}")
ee = 10 ** np.linspace(-4, 0, 200)
k3 = max(float(np.max(np.abs(Ff(k, Finv(k, ee)) / ee - 1))) for k in KER)
check("K3", k3 < 1e-6, f"max |F(Finv(e))/e - 1| = {k3:.2e}")
rk = np.random.default_rng(476)
k4 = float(np.median([S2(C476, *mock(C476, "L", AF["canonical"], rk, nuisance=False))[0] for _ in range(100)]))
check("K4", abs(k4 - 0.205) <= 0.02, f"L generator, V noise only, CFG476 sample: median rms {k4:.4f} (CFG476 0.205)")

# ------------------------------------------------------------------------------------------------ main
MODELS = ("F", "L", "M", "Msame")
VERD = {}
for foot in ("canonical", "alt"):
    aF = AF[foot]; T = template(CS, aF)
    P(f"\n================ footing {foot}: a_F = {aF:.4e} m/s^2 ================")
    P(f"  S1 galaxies (>= 3 points at x < 1): {int(T['keep'].sum())} of {len(SAMPLE)}; template D_i median {np.median(T['D'][T['keep']]):+.4f} dex, "
      f"range [{T['D'][T['keep']].min():+.4f}, {T['D'][T['keep']].max():+.4f}]")
    if MUT:
        go_d, V_d = mock(CS, "M", aF, np.random.default_rng(4910))
    else:
        go_d, V_d = (CS["V"] * 1e3) ** 2 / CS["R"], CS["V"]
    b_d, Rm_d = beta(CS, go_d, aF, T, return_all=True); s_d, a_d = S2(CS, go_d, V_d)
    k = np.where(T["keep"])[0]; rb = np.random.default_rng(91)
    bb = [beta(CS, go_d, aF, T, gal_idx=rb.choice(k, len(k))) for _ in range(2000)]
    P(f"  DATA{' (MUTATE)' if MUT else ''}: beta = {b_d:+.3f} (galaxy bootstrap sigma {np.std(bb):.3f}); S2 = {s_d:.4f} dex at best a = {a_d:.3e}")
    MK = {}
    for mi, m in enumerate(MODELS):
        rng = np.random.default_rng(49100 + 10 * mi + (0 if foot == "canonical" else 1))
        st = []
        for _ in range(NMOCK):
            go, V = mock(CS, m, aF, rng)
            st.append((beta(CS, go, aF, T), S2(CS, go, V)[0]))
        st = np.array(st); MK[m] = st
        pb, ps = pval(st[:, 0], b_d), pval(st[:, 1], s_d)
        cons = pb >= 0.05 and ps >= 0.05
        P(f"  {m:5s}: beta median {np.median(st[:,0]):+.3f} [16-84 {np.percentile(st[:,0],16):+.3f}, {np.percentile(st[:,0],84):+.3f}]  p_beta {pb:.3f} | "
          f"S2 median {np.median(st[:,1]):.4f} [{np.percentile(st[:,1],16):.4f}, {np.percentile(st[:,1],84):.4f}]  p_S2 {ps:.3f}  -> "
          f"{'CONSISTENT' if cons else 'INCONSISTENT'}{'  (reported only)' if m == 'Msame' else ''}")
    def decide(bd, sd, excl=None):
        res = {}
        for m in ("F", "L", "M"):
            st = MK[m] if not (excl is not None and m == "F") else np.delete(MK["F"], excl, axis=0)
            pb, ps = pval(st[:, 0], bd), pval(st[:, 1], sd)
            res[m] = dict(p_beta=pb, p_S2=ps, consistent=bool(pb >= 0.05 and ps >= 0.05))
        if res["F"]["consistent"] and not res["L"]["consistent"] and not res["M"]["consistent"]:
            v = "FRAMEWORK SINGLED OUT"
        elif not res["F"]["consistent"]:
            v = "FRAMEWORK EXCLUDED"
        else:
            v = "NOT SINGLED OUT"
        return v, res
    v, res = decide(b_d, s_d)
    Psing = float(np.mean([decide(MK["F"][j, 0], MK["F"][j, 1], excl=j)[0] == "FRAMEWORK SINGLED OUT" for j in range(NMOCK)]))
    # reported power splits: how often F-pseudo-data rejects L, and rejects M
    rejL = float(np.mean([not decide(MK["F"][j, 0], MK["F"][j, 1], excl=j)[1]["L"]["consistent"] for j in range(NMOCK)]))
    rejM = float(np.mean([not decide(MK["F"][j, 0], MK["F"][j, 1], excl=j)[1]["M"]["consistent"] for j in range(NMOCK)]))
    label = v + (" (LOW POWER)" if Psing < 0.5 else "")
    why = [f"{m}: p_beta {res[m]['p_beta']:.3f}, p_S2 {res[m]['p_S2']:.3f}" for m in res]
    P(f"  POWER: P_single = {Psing:.3f} (F pseudo-data rejects L {rejL:.3f}, rejects M {rejM:.3f})")
    P(f"  VERDICT [{foot}]: {label}   ({'; '.join(why)})")
    sep = (np.median(MK['M'][:, 0]) - np.median(MK['F'][:, 0])) / np.std(MK['F'][:, 0])
    P(f"  reported: F-vs-M separation in beta = {sep:.2f} F-mock sigma; data beta sits at "
      f"{(b_d - np.median(MK['F'][:,0]))/np.std(MK['F'][:,0]):+.2f} sigma from F's median and "
      f"{(b_d - np.median(MK['M'][:,0]))/np.std(MK['M'][:,0]):+.2f} sigma from M's")
    VERD[foot] = label
    OUT["footings"][foot] = dict(a_F=aF, n_S1=int(T["keep"].sum()), n=len(SAMPLE), data=dict(beta=b_d, beta_boot_sigma=float(np.std(bb)), S2=s_d, a_best=a_d),
                                 mocks={m: dict(beta_med=float(np.median(MK[m][:, 0])), beta_16=float(np.percentile(MK[m][:, 0], 16)),
                                                beta_84=float(np.percentile(MK[m][:, 0], 84)), S2_med=float(np.median(MK[m][:, 1])),
                                                S2_16=float(np.percentile(MK[m][:, 1], 16)), S2_84=float(np.percentile(MK[m][:, 1], 84)),
                                                p_beta=pval(MK[m][:, 0], b_d), p_S2=pval(MK[m][:, 1], s_d)) for m in MODELS},
                                 decision=res, verdict=v, label=label, P_single=Psing, rejL=rejL, rejM=rejM, sep_beta_sigma=float(sep))

P("\nSUMMARY")
for f in VERD:
    P(f"  {f}: {VERD[f]}")
P("  kappa = 1/2 FITTED; footings never pooled; LCDM column = dark-matter-only abundance matching (feedback LCDM NOT tested);"
  " the cold mass is still required.")
P(f"  run time {time.time() - t0:.0f} s")
OUT["verdicts"] = VERD
ctrl_ok = all(c["ok"] for c in OUT["checks"].values())
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(l for l in LOG if not l.startswith("  run time")) + "\n")
if MUT:
    det = all(OUT["footings"][f]["decision"]["F"]["p_beta"] < 0.05 for f in OUT["footings"])
    P(f"MUTATE: F judged inconsistent through beta on both footings: {det} -> {'DETECTED (exit 1)' if det else 'NOT DETECTED: the test lacks teeth (exit 0)'}")
    with open(os.path.join(HERE, SLUG + ".out"), "a") as fh:
        fh.write(f"MUTATE: F judged inconsistent through beta on both footings: {det} -> {'DETECTED (exit 1)' if det else 'NOT DETECTED (exit 0)'}\n")
    sys.exit(1 if det else 0)
sys.exit(0 if ctrl_ok else 2)
