#!/usr/bin/env python3
"""X20_hosted_dwarf_disequilibrium: is the hosted-dwarf extra over B_iso tidal disequilibrium or binary inflation?

Frozen criteria: FROZEN_CRITERIA.md (87b6832e84). Reads X1's per-system CSV, CFG257's Arroyo-Polonio table and LVD
ellipticities, all read-only. One process, one thread, seconds.

    python3 x20_hosted_dwarf_disequilibrium.py            -> .out, _results.json
    python3 x20_hosted_dwarf_disequilibrium.py --mutate   -> E from the AQUAL + EFE column (K0 must fail), _MUTATE outputs
"""
import csv, json, math, os, resource, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)

G, PC, KPC, MSUN = 6.674e-11, 3.0857e16, 3.0857e19, 1.989e30
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
HCLS = ("MW ultra-faint", "bright M31", "M31 others")
REP_CLS = ("MW classical", "indiv:Crater II", "indiv:Antlia II", "indiv:Canes Venatici I", "indiv:Sagittarius")
TAU_STAR, TAU_REP = 0.1, (0.03, 0.3)
NPERM, NBOOT, SEED = 20000, 10000, 20261024
K0_REF = {"canonical": (0.596, 0.220, 0.777), "alt": (0.539, 0.185, 0.697)}
ECOL = "Delta[AQUAL + EFE L*0 (exact MOND + EFE)]" if MUTATE else "Delta[iso AQUAL L*0]"
SCOL = "sdMC[" + ECOL[len("Delta["):]

def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None

# ------------------------------------------------------------------ data
X1 = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount", "x1_per_system.csv"))))
ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping",
                                            "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values())))
r_room = np.array([float(r["sig_f07"]) / float(r["sig_free"]) for r in ARR])
r_total = np.array([float(r["sig_f07"]) / float(r["sig_f0"]) for r in ARR])
ELL = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", fn))):
        e = fl(r.get("ellipticity"))
        if e is not None and not r.get("ellipticity_ul"):
            ELL[r["name"]] = e

def rows(foot, classes):
    out = []
    for r in X1:
        if r["footing"] != foot or r["cls"] not in classes:
            continue
        ms = 10 ** float(r["logMstar"]); rh = float(r["rh_pc"]) * PC; r12 = 4.0 / 3.0 * rh
        gN = G * (ms / 2) * MSUN / r12 ** 2
        dN, di = float(r["Delta[Newton]"]), float(r["Delta[iso AQUAL L*0]"])
        giso = gN * 10 ** (dN - di)
        d = float(r["d_host_kpc"]) * KPC; xe = float(r["x_e_mid"])
        mv = fl(r["M_V"]) if "M_V" in r else None
        out.append(dict(name=r["name"], host=r["host"], cls=r["cls"], E=float(r[ECOL]), s=float(r[SCOL]),
                        gN=gN, giso=giso, r12=r12, d=d, xe=xe, sigma=float(r["sigma"]), dN=dN, mv=mv))
    return out

def tau_of(R, a0, xe, d, fac=2.0):
    return fac * xe * a0 * np.array([q["r12"] for q in R]) / d / np.array([q["giso"] for q in R])

def rankdata(a):            # along last axis, no ties expected (continuous values)
    return np.argsort(np.argsort(a, axis=-1), axis=-1).astype(float)
def spearman(x, y):
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(axis=-1, keepdims=True); ry = ry - ry.mean(axis=-1, keepdims=True)
    return (rx * ry).sum(axis=-1) / np.sqrt((rx ** 2).sum(axis=-1) * (ry ** 2).sum(axis=-1))

def perm_test(R, E, a0, rng, nperm=NPERM):
    """T1: one-sided p of Spearman(E, log tau) against (d, x_e) pairs permuted within host."""
    xe = np.array([q["xe"] for q in R]); d = np.array([q["d"] for q in R])
    lt = np.log10(tau_of(R, a0, xe, d)); rho = float(spearman(lt, E))
    host = np.array([q["host"] for q in R])
    idx = np.tile(np.arange(len(R)), (nperm, 1))
    for h in np.unique(host):
        m = np.where(host == h)[0]
        idx[:, m] = m[np.argsort(rng.random((nperm, len(m))), axis=1)]
    ltp = np.log10(tau_of(R, a0, xe[idx], d[idx]))
    rp = spearman(ltp, np.broadcast_to(E, ltp.shape))
    return rho, float((np.sum(rp >= rho) + 1) / (nperm + 1))

def boot_median(E, s, rng, n=NBOOT):
    N = len(E)
    if N == 0:
        return float("nan"), float("nan")
    ix = rng.integers(0, N, (n, N))
    draws = E[ix] + s[ix] * rng.standard_normal((n, N))
    return float(np.median(E)), float(np.std(np.median(draws, axis=1)))

def label(z):
    return "EXTRA" if z >= 2 else ("NONE" if z < 1 else "AMBIGUOUS")

# ------------------------------------------------------------------ run
P(f"X20_hosted_dwarf_disequilibrium  {'MUTATE run (E from the AQUAL + EFE column)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10 never pooled; not theory closed")
P(f"E column: {ECOL}")
RES = dict(frozen="87b6832e84", mutate=MUTATE, footings={}, checks={})
checks = []

for f in FOOTS:
    a0 = A0[f]; rng = np.random.default_rng(SEED)
    R = rows(f, HCLS); E = np.array([q["E"] for q in R]); S = np.array([q["s"] for q in R])
    xe = np.array([q["xe"] for q in R]); d = np.array([q["d"] for q in R])
    tau = tau_of(R, a0, xe, d); tau3 = tau_of(R, a0, xe, d, 3.0)
    for q, t in zip(R, tau):
        q["tau"] = float(t)
    FR = RES["footings"][f] = {}
    P(f"\n=== [{f}] set H: {len(R)} systems ({', '.join(f'{c} {sum(q[chr(99)+chr(108)+chr(115)] == c for q in R)}' for c in HCLS)})")

    # K0
    meds = [float(np.median([q["E"] for q in R if q["cls"] == c])) for c in HCLS]
    k0 = all(abs(m - r) <= 0.005 for m, r in zip(meds, K0_REF[f]))
    P(f"  K0 plain medians {[round(m, 3) for m in meds]} vs X19 {list(K0_REF[f])}: {'PASS' if k0 else 'FAIL'}")
    checks.append((f"K0[{f}]", k0))

    # K1
    k1d = []
    for q in R:
        b = arr_free.get(q["name"], med_free if (q["mv"] is not None and q["mv"] > -7.7) else 1.0)
        gobs_pt = 3 * (q["sigma"] * 1e3 * b) ** 2 / q["r12"]
        k1d.append(abs(math.log10(q["gN"] * 10 ** q["dN"]) - math.log10(gobs_pt)))
    k1 = float(np.median(k1d)) <= 0.05
    P(f"  K1 g_obs (CSV) vs 3(sigma b)^2/r12: median |d| {np.median(k1d):.4f} dex (max {max(k1d):.3f}): {'PASS' if k1 else 'FAIL'}")
    checks.append((f"K1[{f}]", k1))

    # T1
    rho, p = perm_test(R, E, a0, rng)
    rho3 = float(spearman(np.log10(tau3), E))
    P(f"  T1 Spearman(E, log tau) = {rho:+.3f}, one-sided permutation p = {p:.4g} (factor-3 tau: rho {rho3:+.3f}, same ranks)")
    per_cls_rho = {}
    for c in HCLS:
        m = np.array([q["cls"] == c for q in R])
        if m.sum() >= 5:
            per_cls_rho[c] = float(spearman(np.log10(tau[m]), E[m]))
    P("     per class rho (reported): " + ", ".join(f"{c} {v:+.2f}" for c, v in per_cls_rho.items()))
    FR["T1"] = dict(rho=rho, p=p, rho_factor3=rho3, per_class_rho=per_cls_rho)

    # T2
    FR["T2"] = {}
    for ts in (TAU_STAR,) + TAU_REP:
        m = tau <= ts
        med, sd = boot_median(E[m], S[m], rng)
        z = med / sd if m.sum() and sd > 0 else float("nan")
        lab = label(z) if m.sum() else "N/A"
        hi_med = float(np.median(E[~m])) if (~m).sum() else float("nan")
        tag = "PRIMARY" if ts == TAU_STAR else "reported"
        P(f"  T2 tau <= {ts:<4}: N {int(m.sum()):2d}  median E {med:+.3f} +- {sd:.3f}  Z {z:+.2f}  {lab:9s}  "
          f"(tau > {ts}: N {int((~m).sum())}, median {hi_med:+.3f})  [{tag}]")
        byc = {}
        for c in HCLS:
            mc = m & np.array([q["cls"] == c for q in R])
            if mc.sum():
                mm, ss = boot_median(E[mc], S[mc], rng)
                byc[c] = dict(N=int(mc.sum()), median=mm, sd=ss, Z=mm / ss if ss > 0 else float("nan"))
        if ts == TAU_STAR:
            P("     by class: " + "; ".join(f"{c} N {v['N']} {v['median']:+.3f} +- {v['sd']:.3f} (Z {v['Z']:+.2f})" for c, v in byc.items()))
        FR["T2"][str(ts)] = dict(N=int(m.sum()), median=med, sd=sd, Z=z, label=lab, N_above=int((~m).sum()),
                                 median_above=hi_med, by_class=byc)
    qt = np.percentile(tau, [0, 16, 50, 84, 100])
    P(f"  tau distribution: min {qt[0]:.3g}, 16% {qt[1]:.3g}, median {qt[2]:.3g}, 84% {qt[3]:.3g}, max {qt[4]:.3g}")

    # verdict
    t2 = FR["T2"][str(TAU_STAR)]
    c1 = p < 0.01; c2 = t2["label"] == "NONE" and t2["N"] >= 8
    if t2["N"] < 8:
        v = "UNDECIDED"
    elif c1 and c2:
        v = "DISEQUILIBRIUM SUPPORTED"
    elif c1 != c2:
        v = "PARTIAL"
    elif p >= 0.05 and t2["label"] == "EXTRA":
        v = "NOT SUPPORTED"
    else:
        v = "UNDECIDED"
    FR["verdict"] = v
    P(f"  VERDICT [{f}]: {v}")

    # B
    FR["B"] = {}
    for c in HCLS:
        Ec = float(np.median([q["E"] for q in R if q["cls"] == c])); qreq = 10 ** (-Ec / 2)
        mr, mn = float(np.median(r_room)), float(np.min(r_room))
        lab = "BINARIES CAN ERASE" if qreq >= mr else ("ONLY AT THE EXTREME" if qreq >= mn else "CANNOT")
        FR["B"][c] = dict(median_E=Ec, q_req=qreq, room_median=mr, room_min=mn, label=lab,
                          total_median=float(np.median(r_total)), total_min=float(np.min(r_total)))
        P(f"  B {c:15s}: needs sigma x {qreq:.3f}; room f07/free median {mr:.3f}, min {mn:.3f} -> {lab}"
          f"  (total f07/f0 median {np.median(r_total):.3f}, min {np.min(r_total):.3f})")

    # reported: ellipticity, reported classes, per-system table
    me = [(q["E"], ELL[q["name"]]) for q in R if q["name"] in ELL]
    if len(me) >= 5:
        a = np.array(me); re_ = float(spearman(a[:, 1], a[:, 0]))
        P(f"  reported: Spearman(E, ellipticity) {re_:+.3f} over {len(me)} systems")
        FR["ellipticity_rho"] = dict(rho=re_, N=len(me))
    RR = rows(f, REP_CLS)
    if RR:
        tr = tau_of(RR, a0, np.array([q["xe"] for q in RR]), np.array([q["d"] for q in RR]))
        P("  reported systems: " + "; ".join(f"{q['name']} E {q['E']:+.2f} tau {t:.3g}" for q, t in zip(RR, tr)))
        FR["reported_systems"] = {q["name"]: dict(cls=q["cls"], E=q["E"], tau=float(t)) for q, t in zip(RR, tr)}
    FR["per_system"] = [dict(name=q["name"], cls=q["cls"], E=q["E"], s=q["s"], tau=q["tau"]) for q in R]
    P("  per system (sorted by tau): " + "; ".join(f"{q['name']} {q['tau']:.2g}/{q['E']:+.2f}" for q in sorted(R, key=lambda q: q["tau"])))

    # K2 / K3 (canonical machinery, both footings)
    rngc = np.random.default_rng(SEED + 1)
    Esyn = 0.5 * np.log10(tau) + S * rngc.standard_normal(len(R))
    _, p2 = perm_test(R, Esyn, a0, rngc)
    k2 = p2 < 0.01
    P(f"  K2 positive control (E = 0.5 log tau + noise): p = {p2:.4g}: {'PASS' if k2 else 'FAIL'}")
    checks.append((f"K2[{f}]", k2))
    host = np.array([q["host"] for q in R]); ps = []
    for _ in range(200):
        Es = E.copy()
        for h in np.unique(host):
            mh = np.where(host == h)[0]; Es[mh] = Es[rngc.permutation(mh)]
        ps.append(perm_test(R, Es, a0, rngc, nperm=2000)[1])
    frac = float(np.mean(np.array(ps) > 0.01)); k3 = frac >= 0.9
    P(f"  K3 negative control (E shuffled within host, 200 x 2000 perms): fraction p > 0.01 = {frac:.3f}: {'PASS' if k3 else 'FAIL'}")
    checks.append((f"K3[{f}]", k3))

V = {f: RES["footings"][f]["verdict"] for f in FOOTS}
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else "UNDECIDED (footings disagree)"
P(f"\n=== VERDICT (both footings must agree): {RES['verdict']}   {V}")

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
checks.append(("K4", rss < 1.0))
P("\n=== CHECKS")
for k, ok in checks:
    P(f"  [{'PASS' if ok else 'FAIL'}] {k}")
RES["checks"] = {k: bool(ok) for k, ok in checks}
npass = sum(ok for _, ok in checks)
P(f"\nchecks {npass}/{len(checks)}; runtime {time.time() - T0:.1f} s; peak RSS {rss:.3f} GB")
open(os.path.join(HERE, f"x20_hosted_dwarf_disequilibrium{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x20_hosted_dwarf_disequilibrium_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if npass == len(checks) else 1)
