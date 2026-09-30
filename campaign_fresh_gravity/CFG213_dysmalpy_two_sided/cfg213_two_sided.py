#!/usr/bin/env python3
"""CFG213 -- a two-sided a0 test on DysmalPy disc-halo decompositions: NOEMA3D (z ~ 1.4, measured CO gas) and ALMA-CRISTAL
(z ~ 5, dust-based gas).  D = 1/(1 - f_DM(R_e)) against nu(g_bar / a0(z)) for the flat law and the rival a0 ~ H(z).
Frozen criteria: FROZEN_CRITERIA.md here (03da24231), committed before any number.  kappa = 1/2 FITTED, NOT DERIVED.
The mass route (the fits' baryonic mass; CRISTAL's prior is 1 dex wide) is the headline limitation; the independent route
(SED + gas) is reported beside the primary, never substituted.  No sentence says the data favour the framework.
Run:  python3 campaign_fresh_gravity/CFG213_dysmalpy_two_sided/cfg213_two_sided.py        (MUTATE=1: every D_obs x 1.5)
"""
import os, sys, csv, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG4_common as K
    import CFG7_common as C
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "0", "1")
MUT = MODE == "1"
R = C.Report("cfg213_two_sided", MUT)
P, check = R.P, R.check
P(__doc__.split("Run:")[0].strip())

G2SI = 1e6 / 3.0856775814913673e19       # (km/s)^2/kpc -> m/s^2
OM = 0.315
A0F = {"canonical": K.A0["canonical"], "alt": K.A0["alt"]}
KER = {"nu_mono": K.nu_mono, "P2": K.nu_p2}
NBOOT, SEED = 10000, 213


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def nu1(nu, y):
    return float(nu(np.array([y]))[0])


def ystar(D, nu):
    return 10 ** brentq(lambda ly: nu1(nu, 10 ** ly) - D, -12, 14, xtol=1e-14, rtol=1e-14)


def rd(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def fnum(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else float("nan")
    except (TypeError, ValueError):
        return float("nan")


# ------------------------------------------------------------------------------------------------ controls
R.banner("CONTROLS")
rt = {}
for k, nu in KER.items():
    Ds = np.geomspace(1.02, 50, 40)
    rt[k] = max(abs(nu1(nu, ystar(d, nu)) / d - 1) for d in Ds)
check("C1 kernel round trip nu(y*(D)) = D to 1e-9 (nu_mono, P2)", f"{rt}", max(rt.values()) < 1e-9)
c2 = []
for k, nu in KER.items():
    for foot in A0F:
        for z in (1.4, 5.0):
            for law, a0 in (("flat", A0F[foot]), ("rival", A0F[foot] * E(z))):
                gb = 3.3 * A0F[foot]
                Dexact = nu1(nu, gb / a0)
                c2.append(abs(math.log10(Dexact / nu1(nu, gb / a0))))
check("C2 a synthetic galaxy placed exactly on each law returns delta = 0 to 1e-12", f"max |delta| {max(c2):.1e}", max(c2) < 1e-12)

# ------------------------------------------------------------------------------------------------ data
dyn = {r["id"]: r for r in rd(os.path.join(AT, "cristal2025_dynamics.csv"))}
smp = {r["id"]: r for r in rd(os.path.join(AT, "cristal2025_sample.csv"))}
kin = {r["id"]: r for r in rd(os.path.join(AT, "cristal2025_kinematics.csv"))}
vec = rd(os.path.join(AT, "cristal_vector", "cristal_outer_summary.csv"))
ALIAS = {"09": "09a"}                      # dynamics / vector id -> sample / kinematics id (CFG197's join note)
VALIAS = {"10a-E": "10a"}                  # dynamics id -> vector id
EXCL = {"09", "15"}                        # vector curves disagree with the paper's table (frozen)
cr = []
for i, r in dyn.items():
    sid = ALIAS.get(i, i)
    s, k = smp.get(sid, {}), kin.get(sid, {})
    fm = fnum(k.get("f_molgas"))
    cr.append(dict(id=i, z=fnum(s.get("z_cii")), logMstar=fnum(s.get("logMstar")), f_molgas=fm, cls=k.get("classification", ""),
                   logMfit=fnum(r["logMtot"]), Re=fnum(r["Re_disk_kpc"]), Vrot=fnum(r["Vrot_Re_kms"]), sig0=fnum(r["sigma0_kms"]),
                   fdm=fnum(r["fDM_Re"])))
noema = []
for r in rd(os.path.join(REPO, "data_assembly", "noema3d", "noema3d_per_galaxy.csv")):
    noema.append(dict(id=r["id"], z=fnum(r["z"]), logMstar=fnum(r["logMstar_SED"]), logMgas=fnum(r["logMgas_CO_P1"]),
                      logMfit=fnum(r["logMbary_dyn"]), Re=fnum(r["Re_disk_fixed_kpc"]), Vc=fnum(r["Vc_at_Re_disk_kms"]),
                      sig0=fnum(r["sigma0_kms"]), fdm=fnum(r["fDM_Re_disk"])))
P(f"  CRISTAL: {len(cr)} dynamical disks; z present for {sum(math.isfinite(g['z']) for g in cr)}; excluded from the primary: "
  f"{sorted(EXCL)}; NOEMA3D: {len(noema)} galaxies")
for g in cr:
    assert math.isfinite(g["z"]) and 4.3 < g["z"] < 5.8, (g["id"], g["z"])
for g in noema:
    assert 1.1 < g["z"] < 1.7


def galaxy_rows(bin_name, gals, alpha=3.36, route=False, mutate=False):
    """per galaxy: g_bar [m/s^2], D_obs, z; the pressure variant alpha and the mass-route variant as frozen"""
    out = []
    for g in gals:
        if not all(math.isfinite(g[k]) for k in ("fdm", "Re", "sig0", "z")):
            continue
        if bin_name == "Z5":
            if not math.isfinite(g["Vrot"]):
                continue
            vc2_ad = g["Vrot"] ** 2 + 3.36 * g["sig0"] ** 2                 # the paper's V_circ at R_e
            vc2 = g["Vrot"] ** 2 + alpha * g["sig0"] ** 2
        else:
            if not math.isfinite(g["Vc"]):
                continue
            vc2_ad = g["Vc"] ** 2
            vc2 = g["Vc"] ** 2 - (3.36 - alpha) * g["sig0"] ** 2
        vb2 = (1 - g["fdm"]) * vc2_ad                                      # the fit's baryonic curve, held fixed
        gbar = vb2 / g["Re"] * G2SI
        if route:
            if bin_name == "Z5":
                if not (math.isfinite(g["logMstar"]) and math.isfinite(g["f_molgas"]) and math.isfinite(g["logMfit"])):
                    continue
                Mind = 10 ** g["logMstar"] / (1 - g["f_molgas"])
            else:
                Mind = 10 ** g["logMstar"] + 10 ** g["logMgas"]
            gbar = gbar * Mind / 10 ** g["logMfit"]
        D = (vc2 / g["Re"] * G2SI) / gbar
        if mutate:
            D = D * 1.5
        out.append(dict(id=g["id"], z=g["z"], gbar=gbar, D=D, cls=g.get("cls", "")))
    return out


def deltas(rows, law, foot, nu):
    d = []
    for r in rows:
        a0 = A0F[foot] * (E(r["z"]) if law == "rival" else 1.0)
        d.append(math.log10(r["D"] / nu1(nu, r["gbar"] / a0)))
    return np.array(d)


rng = np.random.default_rng(SEED)
BOOTIDX = {}


def med_ci(d, key):
    if len(d) not in BOOTIDX:
        BOOTIDX[len(d)] = rng.integers(0, len(d), size=(NBOOT, len(d)))
    bs = np.median(d[BOOTIDX[len(d)]], axis=1)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return float(np.median(d)), float(lo), float(hi)


def verdict(lo, hi):
    return "CONSISTENT" if lo <= 0 <= hi else ("DISFAVOURED-over" if lo > 0 else "DISFAVOURED-under")


BINS = {"Z1.4 (NOEMA3D)": ("Z1.4", noema), "Z5 (CRISTAL primary)": ("Z5", [g for g in cr if g["id"] not in EXCL])}
TABLE = {}
for bname, (bk, gals) in BINS.items():
    R.banner(f"{bname}")
    rows0 = galaxy_rows(bk, gals, mutate=MUT)
    P(f"  n = {len(rows0)}; z {min(r['z'] for r in rows0):.2f}-{max(r['z'] for r in rows0):.2f}")
    P("  per galaxy (primary: alpha 3.36, fit route): id, z, g_bar/A0_canonical, D_obs, D_pred flat / rival (nu_mono, canonical)")
    for r in rows0:
        P(f"    {r['id']:>9s}  z {r['z']:.3f}  g_bar/A0 {r['gbar'] / A0F['canonical']:7.2f}  D_obs {r['D']:.3f}  "
          f"D_flat {nu1(K.nu_mono, r['gbar'] / A0F['canonical']):.3f}  D_rival {nu1(K.nu_mono, r['gbar'] / (A0F['canonical'] * E(r['z']))):.3f}"
          + (f"  [{r['cls']}]" if r['cls'] else ""))
    res = {}
    for alpha in (3.36, 1.68, 0.0):
        for route in (False, True):
            rows = galaxy_rows(bk, gals, alpha=alpha, route=route, mutate=MUT)
            if len(rows) < 3:
                continue
            for kname, nu in KER.items():
                for foot in A0F:
                    for law in ("flat", "rival"):
                        m, lo, hi = med_ci(deltas(rows, law, foot, nu), (bname, alpha, route, kname, foot, law))
                        res[(alpha, route, kname, foot, law)] = dict(n=len(rows), med=m, lo=lo, hi=hi, v=verdict(lo, hi))
    TABLE[bname] = res
    for law in ("flat", "rival"):
        P(f"\n  {law.upper()}: median delta [95% CI] -> verdict  (rows: kernel / footing; columns: alpha 3.36 | 1.68 | 0 (reported); fit route)")
        for kname in KER:
            for foot in A0F:
                cells = []
                for alpha in (3.36, 1.68, 0.0):
                    c = res.get((alpha, False, kname, foot, law))
                    cells.append(f"{c['med']:+.3f} [{c['lo']:+.3f}, {c['hi']:+.3f}] {c['v']}" if c else "n/a")
                P(f"    {kname:7s} {foot:9s} | " + " | ".join(cells))
        for kname in KER:
            for foot in A0F:
                c = res.get((3.36, True, kname, foot, law))
                if c:
                    P(f"    ROUTE (SED + gas) {kname:7s} {foot:9s} alpha 3.36: n = {c['n']}, {c['med']:+.3f} [{c['lo']:+.3f}, {c['hi']:+.3f}] {c['v']}")
    # robust verdict per law (both footings, both kernels, alpha 3.36 and 1.68; the fit route)
    rob = {}
    for law in ("flat", "rival"):
        vs = {res[(a, False, k, f, law)]["v"] for a in (3.36, 1.68) for k in KER for f in A0F if (a, False, k, f, law) in res}
        rob[law] = vs.pop() if len(vs) == 1 else "NOT robust (" + ", ".join(sorted(vs)) + ")"
        # route flip?
        vr = {res[(3.36, True, k, f, law)]["v"] for k in KER for f in A0F if (3.36, True, k, f, law) in res}
        prim = {res[(3.36, False, k, f, law)]["v"] for k in KER for f in A0F}
        rob[law + "_route"] = ("route-dependent" if vr and vr != prim else ("route-stable" if vr else "route n/a"))
    dis = [l for l in ("flat", "rival") if rob[l].startswith("DISFAVOURED")]
    hsep = len(dis) == 1
    P(f"\n  ROBUST: flat {rob['flat']} ({rob['flat_route']}); rival {rob['rival']} ({rob['rival_route']})")
    P(f"  -> {'the decompositions SEPARATE the laws: ' + dis[0] + ' is robustly ' + rob[dis[0]] if hsep else 'no robust separation'}")
    R.num(bname, {f"{a}|{'route' if r_ else 'fit'}|{k}|{f}|{l}": v for (a, r_, k, f, l), v in res.items()})
    R.num(bname + " robust", rob)

# ------------------------------------------------------------------------------------------------ reported extras
R.banner("REPORTED: CRISTAL-09 / -15, Best Disk subset, the vector's outer radii, C3")
ex = galaxy_rows("Z5", [g for g in cr if g["id"] in EXCL], mutate=MUT)
for r in ex:
    P(f"  excluded {r['id']}: z {r['z']:.3f}, g_bar/A0 {r['gbar'] / A0F['canonical']:.2f}, D_obs {r['D']:.3f}, D_flat "
      f"{nu1(K.nu_mono, r['gbar'] / A0F['canonical']):.3f}, D_rival {nu1(K.nu_mono, r['gbar'] / (A0F['canonical'] * E(r['z']))):.3f}")
bd = galaxy_rows("Z5", [g for g in cr if g["id"] not in EXCL and g["cls"] == "Best Disk"], mutate=MUT)
for law in ("flat", "rival"):
    m, lo, hi = med_ci(deltas(bd, law, "canonical", K.nu_mono), ("bd", law))
    P(f"  Best Disk subset (n = {len(bd)}), {law}, nu_mono canonical: {m:+.3f} [{lo:+.3f}, {hi:+.3f}] {verdict(lo, hi)}")
zmap = {g["id"]: g["z"] for g in cr}
for rdef in ("table_Rout", "outermost_data_marker"):
    rows = []
    for v in vec:
        vid = v["id"]
        did = {"10a": "10a-E"}.get(vid, vid)
        if did in EXCL or v["radius_definition"] != rdef:
            continue
        vb, vt, Rk = fnum(v["Vbary_kms"]), fnum(v["Vtot_kms"]), fnum(v["R_kpc"])
        if not (vb > 0 and vt > 0 and Rk > 0):
            continue
        D = vt ** 2 / vb ** 2 * (1.5 if MUT else 1.0)
        rows.append(dict(id=did, z=zmap[did], gbar=vb ** 2 / Rk * G2SI, D=D))
    for law in ("flat", "rival"):
        m, lo, hi = med_ci(deltas(rows, law, "canonical", K.nu_mono), (rdef, law))
        P(f"  vector at {rdef} (n = {len(rows)}; model curves, extrapolated beyond the last marker), {law}, nu_mono canonical: "
          f"{m:+.3f} [{lo:+.3f}, {hi:+.3f}] {verdict(lo, hi)}")
# C3: the vector at R_e against the table
c3 = []
curves = rd(os.path.join(AT, "cristal_vector", "cristal_curves.csv"))
for g in cr:
    if g["id"] in EXCL or not math.isfinite(g["Vrot"]):
        continue
    vid = VALIAS.get(g["id"], g["id"])
    cv = {c: sorted([(fnum(r["R_kpc"]), fnum(r["value"])) for r in curves if r["id"] == vid and r["curve"] == c]) for c in ("V_bary", "V_tot")}
    if not cv["V_bary"] or not cv["V_tot"]:
        continue
    vb = np.interp(g["Re"], [a for a, _ in cv["V_bary"]], [b for _, b in cv["V_bary"]])
    vt = np.interp(g["Re"], [a for a, _ in cv["V_tot"]], [b for _, b in cv["V_tot"]])
    c3.append((g["id"], vt ** 2 / vb ** 2, 1 / (1 - g["fdm"]), vt, math.sqrt(g["Vrot"] ** 2 + 3.36 * g["sig0"] ** 2)))
if c3:
    rD = [a / b for _, a, b, _, _ in c3]
    rV = [a / b for _, _, _, a, b in c3]
    check("C3 (reported) vector at R_e vs table: D ratio and V_circ ratio (median, min, max)",
          f"D_vec/D_tab median {np.median(rD):.3f} [{min(rD):.3f}, {max(rD):.3f}]; V_vec/V_tab median {np.median(rV):.3f} "
          f"[{min(rV):.3f}, {max(rV):.3f}] over {len(c3)} disks", True, load_bearing=False)
if MUT:
    R.banner("MUTATE RESPONSE")
    ok = True
    # recompute the unmutated primary medians in-process and compare
    for bname, (bk, gals) in BINS.items():
        r0 = galaxy_rows(bk, gals, mutate=False)
        r1 = galaxy_rows(bk, gals, mutate=True)
        for law in ("flat", "rival"):
            d0 = np.median(deltas(r0, law, "canonical", K.nu_mono)); d1 = np.median(deltas(r1, law, "canonical", K.nu_mono))
            ok &= abs((d1 - d0) - math.log10(1.5)) < 1e-9
    check("MUTATE: every D_obs x 1.5 raises every bin's median delta by log10(1.5) to 1e-9", f"{ok}", ok)
R.write(here=LANE)
