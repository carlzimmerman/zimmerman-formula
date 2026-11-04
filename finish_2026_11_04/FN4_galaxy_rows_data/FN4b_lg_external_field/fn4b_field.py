#!/usr/bin/env python3
"""FN4b: the Local Group external field from a catalogue (UNGC + Milky Way + M31) at every X1 system; sign test and size.

Criteria: FROZEN_CRITERIA.md (committed alone before this script). Inputs on disk only:
  real_research/data/ungc_karachentsev2013.tsv (UNGC), real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv (LVD),
  rebuild_2026_10_22/X1_hosted_recount/x1_per_system.csv (residuals), rebuild_2026_10_22/LW1_law_scorecard/lw1_dwarfs.json (class sd),
  claude_goal_2026_11_03/CZ1_newtonian_external_field/cz1.json (K1). Constants and the UNGC parser follow CZ1's cz1.py.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -I fn4b_field.py   (FN4B_MUTATE=1 for the twin: UNGC distances x 0.5)
kappa = 1/2 FITTED; not theory closed.
"""
import csv, json, math, os, resource, sys, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from astropy.coordinates import SkyCoord, Galactocentric
import astropy.units as u

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
RB = os.path.join(REPO, "rebuild_2026_10_22")
MUT = os.environ.get("FN4B_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; Gk = 4.30091e-6; CONV = 3.0857e19 / 1e6     # CZ1's constants
M_MW = 7.0e10                                                                                    # KT15 / CZ1
nu_s = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))                                 # CZ1's nu
OUT = []; R = {"mutate": MUT}; T0 = time.time()


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


P(f"FN4b Local Group external field{' MUTATE (UNGC distances x 0.5)' if MUT else ''}. kappa = 1/2 FITTED; not theory closed.")
# ---------- UNGC (CZ1's parser)
U = []; hdr = None
for l in open(os.path.join(REPO, "real_research", "data", "ungc_karachentsev2013.tsv")):
    if l.startswith("#") or not l.strip(): continue
    p = [x.strip() for x in l.rstrip("\n").split("\t")]
    if hdr is None: hdr = p; continue
    if p[1] == "deg" or set(p[0]) <= {"-"}: continue
    U.append(dict(zip(hdr, p)))
def fnum(s):
    try: return float(s)
    except (TypeError, ValueError): return float("nan")
names = [r["Name"] for r in U]
raU = np.array([fnum(r["_RAJ2000"]) for r in U]); deU = np.array([fnum(r["_DEJ2000"]) for r in U]); DU = np.array([fnum(r["Dist"]) for r in U])
LK = np.array([fnum(r["KLum"]) for r in U]); MHI = np.array([fnum(r["MHI"]) for r in U])
def mb_ungc(ups=0.6):
    return np.where(np.isfinite(LK), ups * 10 ** np.nan_to_num(LK), 0.0) + np.where(np.isfinite(MHI), 1.33 * 10 ** np.nan_to_num(MHI), 0.0)
okU = np.isfinite(raU) & np.isfinite(deU) & np.isfinite(DU) & (DU > 0)
if MUT: DU = DU * 0.5
def gc(ra, dec, D_mpc):
    c = SkyCoord(ra=ra * u.deg, dec=dec * u.deg, distance=D_mpc * u.Mpc)
    g = c.transform_to(Galactocentric(galcen_distance=8.178 * u.kpc))
    return np.stack([g.x.to(u.kpc).value, g.y.to(u.kpc).value, g.z.to(u.kpc).value], axis=-1)
XU = np.full((len(U), 3), np.nan); XU[okU] = gc(raU[okU], deU[okU], DU[okU])
i31 = names.index("MESSIER031")
P(f"UNGC rows {len(U)}, with position and distance {int(okU.sum())}; M31 row {names[i31]}, M_b(0.6) {mb_ungc()[i31]:.3e} Msun; MW {M_MW:.1e} Msun at the centre")


def gvec(x, MB, excl=None):
    """Newtonian field [(km/s)^2/kpc] at galactocentric x from the MW point mass and UNGC rows (excl: bool mask of rows left out)."""
    g = -Gk * M_MW * x / np.linalg.norm(x) ** 3
    m = okU & (MB > 0)
    if excl is not None: m &= ~excl
    d = x[None, :] - XU[m]; r = np.linalg.norm(d, axis=1)
    return g - (Gk * MB[m][:, None] * d / r[:, None] ** 3).sum(0)


# ---------- K2 planted
def k2():
    x = np.array([0.0, 0.0, 0.0]); M = 1e11
    g1 = Gk * M / 1000.0 ** 2; d = np.array([1000.0, 0, 0]); gp = np.linalg.norm(-Gk * M * (x - d) / np.linalg.norm(x - d) ** 3)
    ang = np.linspace(0, 2 * np.pi, 13)[:-1]; pts = np.stack([1000 * np.cos(ang), 1000 * np.sin(ang), 0 * ang], 1)
    gr = np.linalg.norm((-Gk * M * (x - pts) / np.linalg.norm(x - pts, axis=1)[:, None] ** 3).sum(0))
    return abs(gp / g1 - 1) <= 1e-12 and gr <= 1e-12 * g1, float(gp / g1 - 1), float(gr / g1)
k2ok, k2a, k2b = k2(); R["K2"] = dict(point_rel=k2a, ring_rel=k2b, passed=bool(k2ok))
P(f"K2 planted: point mass rel dev {k2a:.1e}; ring of 12 net/one {k2b:.1e} -> {'PASS' if k2ok else 'FAIL'}")

# ---------- K1: CZ1 Part D reproduction (MW + M31 only, UNGC position of IC 1613)
cz = json.load(open(os.path.join(REPO, "claude_goal_2026_11_03", "CZ1_newtonian_external_field", "cz1.json")))
iic = names.index("IC1613"); MB06 = mb_ungc(0.6)
only31 = np.zeros(len(U), bool); only31[i31] = True
x_ic = XU[iic]
gtwo = gvec(x_ic, np.where(only31, MB06, 0.0))
k1 = {}
for foot, a0 in A0SI.items():
    y = np.linalg.norm(gtwo) / CONV / a0; ref = cz[f"ic1613|{foot}"]["yN_ext"]; k1[foot] = dict(y=y, cz1=ref, rel=y / ref - 1)
K1 = all(abs(v["rel"]) <= 1e-6 for v in k1.values())
R["K1"] = dict(detail=k1, passed=bool(K1))
P("K1 CZ1 Part D (IC 1613, MW + M31): " + ", ".join(f"{f} y_e {v['y']:.4e} vs {v['cz1']:.4e} (rel {v['rel']:+.1e})" for f, v in k1.items()) + f" -> {'PASS' if K1 else 'FAIL'}")

# ---------- systems: X1 rows, LVD positions
X1 = list(csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv"))))
LV = {}
for f in ("lvd_dwarf_mw", "lvd_dwarf_m31", "lvd_dwarf_local_field"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f"{f}.csv"))): LV.setdefault(r["name"], r)
sysn = sorted({r["name"] for r in X1}); miss = [n for n in sysn if n not in LV]
K4 = len(miss) <= 0.05 * len(sysn); R["K4"] = dict(n=len(sysn), unmatched=miss, passed=bool(K4))
P(f"K4 LVD match: {len(sysn) - len(miss)} of {len(sysn)} X1 systems; unmatched {miss or 'none'} -> {'PASS' if K4 else 'FAIL'}")
host_of = {r["name"]: r["host"] for r in X1}
S = {}
for n in sysn:
    if n in miss: continue
    r = LV[n]; ra, de = float(r["ra"]), float(r["dec"])
    D = float(r["distance"]) / 1000.0 if r.get("distance") else 10 ** (float(r["distance_modulus"]) / 5 + 1) / 1e6   # LVD distance in kpc
    x = gc(np.array([ra]), np.array([de]), np.array([D]))[0]
    sep = np.degrees(np.arccos(np.clip(np.sin(np.radians(de)) * np.sin(np.radians(deU)) + np.cos(np.radians(de)) * np.cos(np.radians(deU)) * np.cos(np.radians(raU - ra)), -1, 1)))
    excl = okU & (sep < 0.1) & (np.abs(DU / (0.5 if MUT else 1.0) - D) / D < 0.25)
    mhi = 10 ** float(r["mass_HI"]) if r.get("mass_HI") not in (None, "") else 0.0
    S[n] = dict(x=x, D=D, excl=excl, host=host_of[n], mhi=mhi)
nex = {n: int(v["excl"].sum()) for n, v in S.items()}
# K3: a planted duplicate of IC 1613 at its UNGC position must be excluded
dup_sep = 0.0; K3 = bool(nex.get("IC 1613", 0) >= 1)
R["K3"] = dict(excluded_rows_total=int(sum(nex.values())), systems_with_self_in_UNGC=int(sum(v >= 1 for v in nex.values())), more_than_one=[n for n, v in nex.items() if v > 1], ic1613_self_excluded=K3, passed=K3)
P(f"K3 self-exclusion: {R['K3']['systems_with_self_in_UNGC']} systems have their own UNGC row excluded; more than one row excluded for {R['K3']['more_than_one'] or 'none'}; IC 1613 excluded {K3} -> {'PASS' if K3 else 'FAIL'}")

# ---------- fields
def fields(ups):
    MB = mb_ungc(ups); out = {}
    for n, v in S.items():
        g = gvec(v["x"], MB, v["excl"])
        if v["host"] == "MW": gh = -Gk * M_MW * v["x"] / np.linalg.norm(v["x"]) ** 3
        elif v["host"] == "M31": d = v["x"] - XU[i31]; gh = -Gk * MB[i31] * d / np.linalg.norm(d) ** 3
        else: gh = np.zeros(3)
        out[n] = dict(g=float(np.linalg.norm(g)), ghost=float(np.linalg.norm(gh)), gnonhost=float(np.linalg.norm(g - gh)))
    return out
F06 = fields(0.6); F03 = fields(0.3); F10 = fields(1.0)

lw1 = json.load(open(os.path.join(RB, "LW1_law_scorecard", "lw1_dwarfs.json")))
rng = np.random.default_rng(20261104)
def spearman(a, b):
    ra_ = np.argsort(np.argsort(a)); rb_ = np.argsort(np.argsort(b)); return float(np.corrcoef(ra_, rb_)[0, 1])
labels = {}; R["footings"] = {}
for foot, a0 in A0SI.items():
    rows = [r for r in X1 if r["footing"] == foot and r["name"] in S]
    T = {}
    for r in rows:
        n = r["name"]; v = S[n]; f = F06[n]
        ms = 10 ** float(r["logMstar"]); mb = ms + 1.33 * v["mhi"]; r12 = 4 / 3 * float(r["rh_pc"]) / 1000.0
        yN = Gk * (mb / 2) / r12 ** 2 / CONV / a0; ye = f["g"] / CONV / a0; yh = f["ghost"] / CONV / a0
        dE = float(np.log10(nu_s(math.hypot(yN, yh))) - np.log10(nu_s(math.hypot(yN, ye))))
        cls = r["cls"] if not r["cls"].startswith("indiv") else f"{r['host']} individual"
        T.setdefault(cls, []).append(dict(name=n, Delta=float(r["Delta[iso AQUAL L*0]"]), log_ye=math.log10(ye), log_yh=math.log10(yh) if yh > 0 else None,
                                          nonhost_frac=f["gnonhost"] / f["g"], yN=yN, dE=dE,
                                          log_ye_ups03=math.log10(F03[n]["g"] / CONV / a0), log_ye_ups10=math.log10(F10[n]["g"] / CONV / a0)))
    res = {}
    for cls, L in sorted(T.items()):
        d = np.array([q["Delta"] for q in L]); le = np.array([q["log_ye"] for q in L]); de = np.array([q["dE"] for q in L])
        o = dict(n=len(L), median_Delta=float(np.median(d)), median_log_ye=float(np.median(le)), median_nonhost_frac=float(np.median([q["nonhost_frac"] for q in L])),
                 median_dE=float(np.median(de)), max_dE=float(np.max(de)), median_Delta_after=float(np.median(d + de)))
        if len(L) >= 5:
            rho = spearman(d, le); perm = np.array([spearman(rng.permutation(d), le) for _ in range(10000)])
            pval = float((np.sum(np.abs(perm) >= abs(rho)) + 1) / (len(perm) + 1)); o.update(rho=rho, p=pval)
            o["T1"] = "EFE-SIGNED TREND" if (rho < 0 and pval < 0.01) else ("OPPOSITE TREND" if (rho > 0 and pval < 0.01) else "NO TREND")
        else:
            o["T1"] = "TOO FEW (n < 5)"
        lw = lw1["footings"][foot]["rows"]["plain"].get(cls)
        sc = lw["sd"] if lw else 1.2533 * float(np.std(d, ddof=1)) / math.sqrt(len(d)) if len(d) > 1 else float("nan")
        o["sigma_c"] = sc; o["Z_before"] = o["median_Delta"] / sc; o["Z_after"] = o["median_Delta_after"] / sc
        o["moves"] = bool(abs(o["median_Delta_after"] - o["median_Delta"]) >= sc or ((abs(o["Z_before"]) > 2) != (abs(o["Z_after"]) > 2)))
        res[cls] = o
    R["footings"][foot] = dict(classes=res, systems=T)
    t2 = "FIELD MOVES A ROW" if any(o["moves"] for o in res.values()) else "FIELD MOVES NOTHING"
    labels[foot] = dict(T2=t2, T1={c: o["T1"] for c, o in res.items()})
    P(f"\n[{foot}] class: n, median Delta (iso law), median log y_e, non-host share, median dE, sigma_c, Z before -> after; T1 rho, p, label")
    for c, o in res.items():
        t1 = f"rho {o['rho']:+.2f}, p {o['p']:.3f}, {o['T1']}" if "rho" in o else o["T1"]
        P(f"  {c:<16s} n {o['n']:>2d}  {o['median_Delta']:+.3f}  {o['median_log_ye']:+.2f}  {o['median_nonhost_frac']:.3f}  {o['median_dE']:+.5f} (max {o['max_dE']:+.4f})  "
          f"{o['sigma_c']:.3f}  {o['Z_before']:+.2f} -> {o['Z_after']:+.2f}  {t1}")
    P(f"  T2 [{foot}]: {t2}")

checks = dict(K1=bool(K1), K2=bool(k2ok), K3=bool(K3), K4=bool(K4))
R["checks"] = checks; ok = all(checks.values())
R["labels"] = labels if ok else "NOT EVALUABLE"
fd = R["footings"]["canonical"]["systems"].get("LG field", [])
P("\nLG field dwarfs, canonical (log y_e, non-host share, dE, Delta):")
for q in sorted(fd, key=lambda q: q["log_ye"]):
    P(f"  {q['name']:<22s} {q['log_ye']:+.2f}  {q['nonhost_frac']:.2f}  {q['dE']:+.5f}  {q['Delta']:+.3f}")
P(f"\nChecks {checks}. Labels: " + ("NOT EVALUABLE" if not ok else "; ".join(f"{f}: T2 {v['T2']}" for f, v in labels.items())))
if MUT:
    R["mutate_bites"] = bool(not K1)
    P(f"MUTATE {'BITES: K1 fails' if not K1 else 'DID NOT BITE: K1 still passes (failed check)'}.")
P(f"done [{time.time() - T0:.0f} s, max RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB]")
json.dump(R, open(os.path.join(HERE, f"fn4b_field{TAG}.json"), "w"), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, f"fn4b_field{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if ok and not MUT else (1 if MUT and not K1 else (0 if MUT else 1)))
