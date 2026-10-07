#!/usr/bin/env python3
"""CFG391 -- satellite-plane members vs non-members under the law (MW VPOS, M31 GPoA).

Frozen criteria: FROZEN_CRITERIA.md (committed before this script).  kappa = 1/2 fitted; both footings.
Offset = log10(sigma_obs / sigma_law), AUDIT_UFD isolated estimator (Upsilon_V = 2, r = 4/3 r_half, half the
mass inside, nu = 1/(1 - exp(-sqrt y))).

Run:   python3 cfg391_plane_membership.py            -> cfg391_plane_membership.out / _results.json
       python3 cfg391_plane_membership.py --mutate   -> *_MUTATE.out / *_MUTATE_results.json (exit 1 = planted signal seen)
"""
import os, sys, csv, json, math, warnings
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord, Galactocentric

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "dsph")
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
OUT = []


def P(s=""):
    print(s); OUT.append(str(s))


G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0_S06 = 9.36e-11          # session-06 value, control C2 only


def nu(y):
    y = max(y, 1e-12); return 1.0 / (1.0 - math.exp(-math.sqrt(y)))


def fnum(v):
    try:
        x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def unit(l, b):
    l, b = math.radians(l), math.radians(b)
    return np.array([math.cos(b) * math.cos(l), math.cos(b) * math.sin(l), math.sin(b)])


# published normals (FROZEN_CRITERIA inputs); S06 = recalled, control C2 only
NORMALS = {"VPOSnew": (164.0, -6.9), "VPOSclass": (157.3, -12.7), "DoS_PPK12": (156.4, -2.2),
           "PK20_pole_k7": (179.5, -9.0), "S06_recalled": (169.3, -2.8)}
PK20_MEM = {"Draco", "Ursa Minor", "Carina", "Fornax", "Leo II", "Sculptor"}
PK20_NON = {"Sextans", "Leo I", "Sagittarius"}
PK20_POLES = {"Sagittarius": (275.2, -8.0, 0.8), "Draco": (169.9, -19.3, 1.2), "Ursa Minor": (195.5, -8.0, 4.3),
              "Sculptor": (349.3, -2.2, 2.0), "Sextans": (232.7, -49.4, 3.4), "Carina": (160.5, -11.9, 6.5),
              "Fornax": (176.5, 15.8, 6.7), "Leo II": (186.3, -21.2, 23.2), "Leo I": (251.1, -38.6, 17.9)}
IBATA15 = {"Andromeda I", "Andromeda III", "Andromeda IX", "Andromeda XI", "Andromeda XII", "Andromeda XIV",
           "Andromeda XVI", "Andromeda XVII", "Andromeda XXV", "Andromeda XXVI", "Cassiopeia II", "NGC 147",
           "NGC 185", "Andromeda XIII", "Andromeda XXVII"}
IBATA_NONCOROT = {"Andromeda XIII", "Andromeda XXVII"}
IBATA_PLAUS = {"NGC 205", "LGS 3", "IC 1613"}

# ------------------------------------------------------------------ MW objects + MC orbital poles (session-06 code path)
mw = []
for r in csv.DictReader(open(os.path.join(DATA, "lvd_dwarf_mw.csv"))):
    MV, sig, ul = fnum(r["M_V"]), fnum(r["vlos_sigma"]), fnum(r["vlos_sigma_ul"])
    rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"]); Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
    if None in (MV, sig, rh) or ul is not None or r["name"] in ("Large Magellanic Cloud", "Small Magellanic Cloud", "LMC", "SMC"):
        continue
    if MV > -7.7 and Dh is None:
        continue
    ph = [fnum(r[k]) for k in ("ra", "dec", "distance", "vlos_systemic", "pmra", "pmdec")]
    if None in ph:
        continue
    mw.append(dict(name=r["name"], host="MW", pop="UFD" if MV > -7.7 else "classical", LV=10 ** (0.4 * (4.83 - MV)), rh=rh, sig=sig,
                   MHI=(10 ** fnum(r["mass_HI"]) if fnum(r["mass_HI"]) is not None else 0.0), ph=ph,
                   e=[fnum(r["distance_em"]) or 0.05 * ph[2], fnum(r["vlos_systemic_em"]) or 1.0, fnum(r["pmra_em"]) or 0.05, fnum(r["pmdec_em"]) or 0.05]))
gc = Galactocentric(); rng = np.random.default_rng(41)
NV = {k: unit(*v) for k, v in NORMALS.items()}
for d in mw:
    n = 300; ra, dec, D, vl, pa, pd = d["ph"]
    c = SkyCoord(ra=np.full(n, ra) * u.deg, dec=np.full(n, dec) * u.deg, distance=np.clip(D + rng.normal(0, d["e"][0], n), 1, None) * u.kpc,
                 pm_ra_cosdec=(pa + rng.normal(0, d["e"][2], n)) * u.mas / u.yr, pm_dec=(pd + rng.normal(0, d["e"][3], n)) * u.mas / u.yr,
                 radial_velocity=(vl + rng.normal(0, d["e"][1], n)) * u.km / u.s).transform_to(gc)
    x = np.vstack([c.x.value, c.y.value, c.z.value]).T; v = np.vstack([c.v_x.value, c.v_y.value, c.v_z.value]).T
    L = np.cross(x, v); L /= np.linalg.norm(L, axis=1)[:, None]
    d["cos"] = {k: L @ nv for k, nv in NV.items()}
    m = L.mean(axis=0); m /= np.linalg.norm(m); d["pole"] = m


def mw_member(d, normal, cut, sense="any"):
    cs = d["cos"][normal]; ct = math.cos(math.radians(cut))
    f = (np.abs(cs) > ct).mean() if sense == "any" else (cs > ct).mean()
    return bool(f >= 0.5)


# ------------------------------------------------------------------ M31 objects
collins = {}
for line in open(os.path.join(DATA, "collins2013_m31_dsph.tsv")):
    if line.startswith("#") or not line.strip():
        continue
    p = line.rstrip("\n").split("\t")
    if len(p) < 20 or not p[0].strip().isdigit():
        continue
    nm = p[1].strip().replace("And ", "Andromeda ")
    if nm == "Andromeda XXX":
        nm = "Cassiopeia II"
    collins[nm] = fnum(p[18])


def load_m31(include_ul=False, collins_sigma=False):
    out = []
    for r in csv.DictReader(open(os.path.join(DATA, "lvd_dwarf_m31.csv"))):
        MV, sig, ul = fnum(r["M_V"]), fnum(r["vlos_sigma"]), fnum(r["vlos_sigma_ul"])
        rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"]); nm = r["name"]
        if nm == "M 32" or MV is None or rh is None:
            continue
        if collins_sigma and nm in collins:
            if collins[nm] and collins[nm] > 0:
                sig, ul = collins[nm], None
            else:
                continue
        if sig is None and ul is not None and include_ul:
            sig = ul
        elif sig is None or ul is not None:
            continue
        out.append(dict(name=nm, host="M31", pop="UFD" if MV > -7.7 else "classical", LV=10 ** (0.4 * (4.83 - MV)), rh=rh, sig=sig,
                        MHI=(10 ** fnum(r["mass_HI"]) if fnum(r["mass_HI"]) is not None else 0.0)))
    return out


def m31_member(d, scheme):
    n = d["name"]
    if scheme == "G1":
        return True if n in IBATA15 else (None if n in IBATA_PLAUS else False)
    if scheme == "G2":
        return None if (n in IBATA_NONCOROT or n in IBATA_PLAUS) else (n in IBATA15)
    if scheme == "G3":
        return (n in IBATA15) or (n in IBATA_PLAUS)
    raise ValueError(scheme)


# ------------------------------------------------------------------ offsets and the test
def add_offsets(objs, a0):
    for d in objs:
        Mb = 2 * d["LV"] + 1.33 * d["MHI"]; r = 4 / 3 * d["rh"] * PC; gN = G * 0.5 * Mb * MSUN / r ** 2
        d["nu"] = nu(gN / a0)
        d["off"] = math.log10(d["sig"] / (math.sqrt(d["nu"] * gN * r / 3) / 1e3))


def verdict(dl, sd):
    if dl < -0.2 and dl / sd < -3:
        return "TDG-ORIGIN SUPPORTED"
    if dl - 2 * sd > -0.2:
        return "DISFAVOURED"
    return "NON-DISCRIMINATING"


def test(objs, labels, mutate=MUT, perm=False):
    """objs with 'off','nu','host','pop'; labels: list of True/False/None (None = excluded)."""
    keep = [(d, m) for d, m in zip(objs, labels) if m is not None]
    groups = {}
    for d, m in keep:
        groups.setdefault((d["host"], d["pop"]), []).append(d["off"])
    meds = {k: float(np.median(v)) for k, v in groups.items()}
    x = np.array([d["off"] - (0.5 * math.log10(d["nu"]) if (mutate and m) else 0.0) - meds[(d["host"], d["pop"])] for d, m in keep])
    mm = np.array([m for _, m in keep], bool)
    if not mm.any() or mm.all():
        return dict(delta=float("nan"), sd=float("nan"), n_mem=int(mm.sum()), n_non=int((~mm).sum()), verdict="EMPTY GROUP")
    dl = float(np.median(x[mm]) - np.median(x[~mm]))
    b = np.random.default_rng(43); bs = []
    for _ in range(2000):
        i = b.integers(0, len(x), len(x)); q = mm[i]
        if q.any() and (~q).any():
            bs.append(np.median(x[i][q]) - np.median(x[i][~q]))
    sd = float(np.std(bs))
    pred = -float(np.median([0.5 * math.log10(d["nu"]) for d, m in keep if m]))
    res = dict(delta=dl, sd=sd, n_mem=int(mm.sum()), n_non=int((~mm).sum()), verdict=verdict(dl, sd), delta_pred=pred,
               f_retained=(1 - dl / pred) if pred != 0 else float("nan"), underpowered=bool(abs(pred) < 0.2),
               members=sorted(d["name"] for d, m in keep if m))
    if perm:
        pr = np.random.default_rng(47); pd_ = []
        for _ in range(2000):
            s = pr.permutation(mm); pd_.append(np.median(x[s]) - np.median(x[~s]))
        pd_ = np.array(pd_)
        res["perm_median"] = float(np.median(pd_)); res["perm_p_le"] = float((pd_ <= dl).mean())
    return res


def line(lbl, r):
    if r["verdict"] == "EMPTY GROUP":
        return f"   {lbl:34s} members {r['n_mem']:2d} / non {r['n_non']:2d}: EMPTY GROUP"
    s = (f"   {lbl:34s} members {r['n_mem']:2d} / non {r['n_non']:2d}: Delta {r['delta']:+.3f} +- {r['sd']:.3f} "
         f"(pred {r['delta_pred']:+.3f}, retained {r['f_retained']:+.2f}{', UNDERPOWERED' if r['underpowered'] else ''}) -> {r['verdict']}")
    if "perm_p_le" in r:
        s += f"  [perm median {r['perm_median']:+.3f}, p(<=obs) {r['perm_p_le']:.3f}]"
    return s


RES = {}
P(f"CFG391 plane members vs non-members{'  [MUTATE: members made Newtonian]' if MUT else ''}")
P("=" * 110)
P(f"MW sample: {len(mw)} ({sum(d['pop']=='UFD' for d in mw)} UFD, {sum(d['pop']=='classical' for d in mw)} classical)")

# ---- C2 fidelity (session-06 configuration)
add_offsets(mw, A0_S06)
c2 = test(mw, [mw_member(d, "S06_recalled", 30) for d in mw], mutate=False)
c2ok = abs(c2["delta"] - 0.034) <= 0.005 and abs(c2["sd"] - 0.098) <= 0.01
RES["C2"] = dict(c2, passed=c2ok)
P(f"C2 session-06 reproduction: Delta {c2['delta']:+.4f} +- {c2['sd']:.4f} (target +0.034 +- 0.098) -> {'PASS' if c2ok else 'FAIL'}")

# ---- C3 pole check vs PK20 Table 3
c3 = {}
for d in mw:
    if d["name"] in PK20_POLES:
        lp, bp, dp = PK20_POLES[d["name"]]
        ang = math.degrees(math.acos(np.clip(d["pole"] @ unit(lp, bp), -1, 1)))
        lo = math.degrees(math.atan2(d["pole"][1], d["pole"][0])) % 360; la = math.degrees(math.asin(d["pole"][2]))
        tol = max(3 * dp, 10.0)
        c3[d["name"]] = dict(ours=(round(lo, 1), round(la, 1)), pk20=(lp, bp), angle=ang, tol=tol, ok=bool(ang <= tol))
npres = len(c3); nok = sum(v["ok"] for v in c3.values()); c3ok = nok >= npres - 2
RES["C3"] = dict(objects=c3, n_present=npres, n_ok=nok, passed=c3ok)
P(f"C3 poles vs PK20 Table 3: {nok}/{npres} within tolerance -> {'PASS' if c3ok else 'FAIL'}")
for k, v in c3.items():
    P(f"   {k:12s} ours (l,b)=({v['ours'][0]:6.1f},{v['ours'][1]:6.1f})  PK20 ({v['pk20'][0]:6.1f},{v['pk20'][1]:6.1f})  angle {v['angle']:5.1f} tol {v['tol']:5.1f} {'ok' if v['ok'] else 'MISS'}")

for foot, a0 in A0.items():
    P(f"\n--- footing {foot} (a0 = {a0:.4e}) ---")
    add_offsets(mw, a0)
    R = RES.setdefault(foot, {})
    P(" MW D1 VPOSnew (164.0, -6.9):")
    for cut in (20, 30, 40):
        for sense in ("any", "co"):
            r = test(mw, [mw_member(d, "VPOSnew", cut, sense) for d in mw], perm=(sense == "any"))
            R[f"MW|D1|{cut}|{sense}"] = r; P(line(f"cut {cut} deg, {sense}", r))
    P(" MW D2 other published normals (30 deg, any sense):")
    for nk in ("VPOSclass", "DoS_PPK12", "PK20_pole_k7"):
        r = test(mw, [mw_member(d, nk, 30) for d in mw]); R[f"MW|D2|{nk}"] = r; P(line(f"{nk} {NORMALS[nk]}", r))
    P(" MW D3 PK20 published classical list (classicals only):")
    lab = [(True if d["name"] in PK20_MEM else False if d["name"] in PK20_NON else None) if d["pop"] == "classical" else None for d in mw]
    r = test(mw, lab); R["MW|D3"] = r; P(line("PK20 list", r))
    # M31
    m31 = load_m31(); add_offsets(m31, a0)
    P(f" M31 (LVD; {len(m31)} with measured sigma; M32 excluded):")
    for g in ("G1", "G2", "G3"):
        r = test(m31, [m31_member(d, g) for d in m31], perm=(g == "G1")); R[f"M31|{g}"] = r; P(line(g, r))
    m31u = load_m31(include_ul=True); add_offsets(m31u, a0)
    r = test(m31u, [m31_member(d, "G1") for d in m31u]); R["M31|G1|S3_UL"] = r; P(line("G1 + upper limits at limit (S3)", r))
    m31c = load_m31(collins_sigma=True); add_offsets(m31c, a0)
    r = test(m31c, [m31_member(d, "G1") for d in m31c]); R["M31|G1|S4_Collins"] = r; P(line("G1 Collins-2013 sigma (S4)", r))
    # COMBINED
    allobj = mw + m31
    lab = [mw_member(d, "VPOSnew", 30) for d in mw] + [m31_member(d, "G1") for d in m31]
    r = test(allobj, lab, perm=True); R["COMBINED"] = r; P(line("COMBINED (MW D1 30 + M31 G1)", r))
    P(" per-object offsets (population-median NOT subtracted):")
    for d in sorted(allobj, key=lambda q: (q["host"], q["pop"], q["name"])):
        mem = mw_member(d, "VPOSnew", 30) if d["host"] == "MW" else m31_member(d, "G1")
        P(f"   {d['host']:3s} {d['pop'][:4]:4s} {d['name']:22s} off {d['off']:+.3f}  0.5log nu {0.5*math.log10(d['nu']):.3f}  member {mem}")
    R["objects"] = [dict(host=d["host"], pop=d["pop"], name=d["name"], off=d["off"], half_log_nu=0.5 * math.log10(d["nu"])) for d in allobj]

prim = ["MW|D1|30|any", "M31|G1", "COMBINED"]
P("\nPRIMARY VERDICTS:")
for foot in A0:
    for k in prim:
        P(f"   {foot:9s} {k:14s} {RES[foot][k]['verdict']}")
    rob = len({RES[foot][f'MW|D1|{c}|any']['verdict'] for c in (20, 30, 40)}) == 1
    RES[foot]["MW_robust"] = rob
    P(f"   {foot:9s} MW verdict ROBUST across 20/30/40 deg: {rob}")
for foot in A0:
    for k in prim:
        r = RES[foot][k]
        P(f"   C1 {foot:9s} {k:14s} perm median {r['perm_median']:+.3f} ({'ok' if abs(r['perm_median']) <= 0.03 else 'FAIL'}), p {r['perm_p_le']:.3f}")

json.dump(RES, open(os.path.join(HERE, f"cfg391_plane_membership{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg391_plane_membership{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    seen = all(RES["canonical"][k]["verdict"] == "TDG-ORIGIN SUPPORTED" for k in prim)
    P(f"MUTATE planted signal seen on all three primaries (canonical): {seen}")
    open(os.path.join(HERE, f"cfg391_plane_membership{TAG}.out"), "a").write(f"MUTATE planted signal seen on all three primaries (canonical): {seen}\n")
    sys.exit(1 if seen else 0)
sys.exit(0)
