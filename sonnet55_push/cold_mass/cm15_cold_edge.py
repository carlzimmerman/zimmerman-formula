"""cm15: cold edge of the cooling window -- does native T_vir < 1e4 K (not luminosity class) decide which dwarfs need extra mass?
Frozen: cm15_FROZEN_CRITERIA.md.  Law sigma as CFG341/CFG335.  Run from anywhere; MUTATE=1 shuffles sigma_obs (separate outputs).
"""
import os, csv, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data", "dsph")
MUTATE = os.environ.get("MUTATE") == "1"; SLUG = "cm15_cold_edge" + ("_MUTATE" if MUTATE else "")
G, MSUN, PC, MP, KB = 6.674e-11, 1.989e30, 3.0857e16, 1.6726e-27, 1.380649e-23
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LOG, OUT, res = [], {"lane": "cm15", "mutate": MUTATE}, []
rng = np.random.default_rng(15)


def P(s=""):
    print(s); LOG.append(s)


def check(n, ok):
    res.append(bool(ok)); P(("PASS  " if ok else "FAIL  ") + n)


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def nu(y):
    y = max(y, 1e-14); return 1.0 / (1.0 - math.exp(-math.sqrt(y)))


def sig_law(Mb, rh, a0):
    r = (4 / 3) * rh * PC; gN = G * 0.5 * Mb * MSUN / r**2
    return math.sqrt(gN * nu(gN / a0) * r / 3.0) / 1e3


def Tnat(Mb, a0):
    V = (G * Mb * MSUN * a0) ** 0.25; return 0.6 * MP * V**2 / (2 * KB)


rows = []
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(DATA, fn))):
        MV, sig, ul = fnum(r.get("M_V")), fnum(r.get("vlos_sigma")), fnum(r.get("vlos_sigma_ul"))
        rh = fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
        if MV is None or rh is None or sig is None or ul is not None or sig <= 0:
            continue
        hi = fnum(r.get("mass_HI")); Mb = 2.0 * 10 ** (0.4 * (4.83 - MV)) + 1.33 * (10**hi if hi is not None else 0.0)
        rows.append(dict(name=r["name"], MV=MV, Mb=Mb, rh=rh, sig=sig))
if MUTATE:
    for d, s in zip(rows, rng.permutation([d["sig"] for d in rows])):
        d["sig"] = float(s)
P(f"cm15{' MUTATE' if MUTATE else ''}: {len(rows)} resolved dwarfs")
check("C1 sig_law reduces to the deep-MOND (4/81 G M a0)^(1/4)-type scaling: sigma^4 ratio for M x16 = 16 at y << 1 (to 2%)",
      abs((sig_law(1.6e3, 300, A0["canonical"]) / sig_law(1e2, 300, A0["canonical"]))**4 / 16 - 1) < 0.02)


def med_err(x):
    if len(x) == 0:
        return float("nan"), float("nan")
    bs = [np.median(rng.choice(x, len(x))) for _ in range(4000)]
    return float(np.median(x)), float(np.std(bs))


def diff_err(x, y):
    bs = [np.median(rng.choice(x, len(x))) - np.median(rng.choice(y, len(y))) for _ in range(4000)]
    return float(np.median(x) - np.median(y)), float(np.std(bs))


for foot, a0 in A0.items():
    D = np.array([math.log10(d["sig"] / sig_law(d["Mb"], d["rh"], a0)) for d in rows])
    T = np.array([Tnat(d["Mb"], a0) for d in rows]); cls = np.array([d["MV"] <= -7.7 for d in rows])
    cold = T < 1e4
    d1, e1 = diff_err(D[cold], D[~cold]); mc, ec = med_err(D[cold & cls]); mu, eu = med_err(D[cold & ~cls]); mm, em = med_err(D[~cold])
    dcu, ecu = diff_err(D[cold & cls], D[cold & ~cls]) if (cold & cls).sum() and (cold & ~cls).sum() else (float("nan"),) * 2
    OUT[foot] = dict(N=len(D), N_cold=int(cold.sum()), N_cold_cls=int((cold & cls).sum()), N_cold_ufd=int((cold & ~cls).sum()), N_mid=int((~cold).sum()),
                     D1=d1, D1_err=e1, cold_cls=mc, cold_cls_err=ec, cold_ufd=mu, cold_ufd_err=eu, mid=mm, mid_err=em, cls_minus_ufd=dcu, cls_minus_ufd_err=ecu,
                     cold_classicals=[d["name"] for d, c in zip(rows, cold & cls) if c], mid_names=[d["name"] for d, c in zip(rows, ~cold) if c])
    P(f"\n  {foot}: N {len(D)}; COLD {cold.sum()} (classicals {(cold & cls).sum()}, UFDs {(cold & ~cls).sum()}), MID {(~cold).sum()}")
    P(f"    D1 = COLD - MID = {d1:+.3f} +- {e1:.3f} ({d1/e1:+.2f} sigma)")
    P(f"    median offset: COLD classicals {mc:+.3f} +- {ec:.3f} ({mc/ec:+.2f} s); COLD UFDs {mu:+.3f} +- {eu:.3f} ({mu/eu:+.2f} s); MID {mm:+.3f} +- {em:.3f}")
    P(f"    COLD classicals - COLD UFDs = {dcu:+.3f} +- {ecu:.3f} ({dcu/ecu:+.2f} sigma)")
    P(f"    COLD classicals: {', '.join(OUT[foot]['cold_classicals'])}")
    P(f"    MID: {', '.join(OUT[foot]['mid_names'])}")
F = [OUT[f] for f in A0]
sup = all(o["D1"] > 2 * o["D1_err"] and o["cold_cls"] > 2 * o["cold_cls_err"] for o in F)
con = all(o["cold_ufd"] > 2 * o["cold_ufd_err"] and abs(o["cold_cls"]) < 2 * o["cold_cls_err"] and o["cls_minus_ufd"] < -2 * o["cls_minus_ufd_err"] for o in F)
verdict = "SUPPORTED" if sup else ("CONTRADICTED" if con else "INCONCLUSIVE")
OUT["verdict"] = verdict
P(f"\n{'MUTATE ' if MUTATE else ''}VERDICT: {verdict}")
if MUTATE:
    real = json.load(open(os.path.join(HERE, "cm15_cold_edge_results.json")))
    a, b = real["canonical"]["cold_cls"], OUT["canonical"]["cold_cls"]
    check(f"MUTATE: COLD-classical median moves > 0.05 dex ({a:+.3f} -> {b:+.3f})", abs(a - b) > 0.05)
P(f"\n{sum(res)}/{len(res)} pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
raise SystemExit(0 if all(res) else 1)
