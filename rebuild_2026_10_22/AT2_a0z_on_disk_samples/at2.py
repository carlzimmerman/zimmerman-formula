"""AT2: grade every high-z kinematic sample on disk with AT1's a0(z) tracking rule, unchanged.

Frozen criteria: FROZEN_CRITERIA.md (e453a3ad83). Reads CFG689's primary quantiles (BAO+SN.P1) exactly as AT1 does, counts
each registry sample per z* bin, applies the reference match (R1-R5) and gates G1-G4, and computes y-bar only for a cell that
passes all of them. Checks K1-K8. Small: stdlib only, one thread, well under 1 GB.
kappa = 1/2 FITTED; not theory closed.

Run from the repo root:  python3 rebuild_2026_10_22/AT2_a0z_on_disk_samples/at2.py      (MUTATE=1 for the twin)
"""
import ast, csv, hashlib, json, math, os, random, re, statistics, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE") == "1"
OUTDIR = os.environ.get("AT2_OUTDIR", HERE)
INNER = os.environ.get("AT2_INNER") == "1"
SUFFIX = "_MUTATE" if MUTATE else ""
ZS = ["1.0", "1.2", "1.5", "2.33"]
BINS = {"1.0": (0.90, 1.10), "1.2": (1.10, 1.35), "1.5": (1.35, 1.915), "2.33": (1.915, 2.75)}
GRID = [0.01 + k * 0.99 / 999 for k in range(1000)]   # AT1 / CFG683 grid
S_GAL = 0.14            # per-galaxy scatter, dex (AT1 / CFG685 budget)
NDRAW = 2000
SEED = 20261104
checks = []
opened = []


def check(name, ok, detail):
    checks.append((name, bool(ok), detail))


def P(rel):
    return os.path.join(ROOT, rel)


def rows(rel):
    opened.append(rel)
    with open(P(rel), newline="") as f:
        return list(csv.DictReader(f))


def fl(x):
    try:
        v = float(str(x).strip())
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def zbin(z):
    if z is None:
        return None
    for k, (lo, hi) in BINS.items():
        if lo <= z < hi or (k == "2.33" and z == hi):
            return k
    return None


# ---- K1: AT1's numbers from cfg689.json, same lines as at1.py ------------------------------------------------------
CFG = "campaign_fresh_gravity/CFG689_native_ruler_bao/cfg689.json"
opened.append(CFG)
p1 = json.load(open(P(CFG)))["BAO+SN"]["P1"]
at1 = json.load(open(P("rebuild_2026_10_22/AT1_a0z_tracking_decision/at1.json")))
Q = {}
for z in ZS:
    X = p1[z]["sqrtX_q"]; E = p1[z]["E_q"]
    gap = math.log10(E[1]) - math.log10(X[3])
    sE = math.log10(E[2]) - math.log10(E[1])
    sX = math.log10(X[3]) - math.log10(X[2])
    S = lambda e: gap / math.sqrt(e * e + sE * sE + sX * sX)
    e3 = max(e for e in GRID if S(e) >= 3)
    a = at1["rows"][z]
    ok = all(abs(u - v) < 1e-12 for u, v in [(gap, a["gap"]), (sE, a["sE"]), (sX, a["sX"]), (e3, a["e3"])])
    check(f"K1 z {z} matches at1.json (1e-12) and CFG689 e_3sigma (0.001)", ok and abs(e3 - p1[z]["e_3sigma"]) <= 0.001,
          f"e_3sigma {e3:.4f} (AT1 {a['e3']:.4f}, CFG689 {p1[z]['e_3sigma']:.4f})")
    Q[z] = dict(e3=e3, gap=gap, T=math.log10(X[2]), X16=math.log10(X[1]), X84=math.log10(X[3]),
                R=math.log10(E[2]), E16=math.log10(E[1]), E84=math.log10(E[3]))


def outcome(y, e, q):
    """AT1 section 3, unchanged. Takes only the ratio y and its error e."""
    tX = (q["X84"] - q["T"]) if y > q["T"] else (q["T"] - q["X16"])
    tE = (q["R"] - q["E16"]) if y < q["R"] else (q["E84"] - q["R"])
    dT = (y - q["T"]) / math.sqrt(e * e + tX * tX)
    dR = (q["R"] - y) / math.sqrt(e * e + tE * tE)
    if abs(dT) <= 2 and dR >= 3:
        return "DECIDES-law"
    if abs(dR) <= 2 and dT >= 3:
        return "DECIDES-rival"
    if abs(dT) > 3 and abs(dR) > 3:
        return "NEITHER"
    return "INCONCLUSIVE"


def graded(y, e_stat, c, q, gate=True):
    e = math.sqrt(e_stat * e_stat + c * c)
    if gate and e > q["e3"]:
        return "BLOCKED"
    return outcome(y, e, q)


# ---- registry loaders: each returns a list of (z, v_over_sigma or None) ---------------------------------------------
def ratio(a, b):
    a, b = fl(a), fl(b)
    return a / b if (a is not None and b not in (None, 0.0)) else None


def L_kurvs():
    integ = {r["kurvs_id"]: r for r in rows("data_assembly/arxiv_tables/kurvs2023_integrated.csv")}
    kin = {r["kurvs_id"]: r for r in rows("data_assembly/arxiv_tables/kurvs2023_kinematics.csv")}
    ids = [r["kurvs_id"] for r in rows("data_assembly/arxiv_tables/kurvs2023_fdm.csv")]
    return [(fl(integ[i]["z_halpha"]), fl(kin.get(i, {}).get("vrot_over_sigma0"))) for i in ids]


def L_genzel():
    rel = "campaign_fresh_gravity/CFG401_genzel17_gas_shape/cfg401_gas_shape.py"
    opened.append(rel)
    src = open(P(rel)).read()
    m = re.search(r"^T1 = (\{.*?\})\n", src, re.S | re.M)
    t1 = ast.literal_eval(m.group(1))
    return [(v[0], v[6] / v[4]) for v in t1.values()]          # z, V_c / sigma0


def L_rc41():
    return [(fl(r["z"]), None) for r in rows("data_assembly/price2021_rc41/price2021_rc41.csv")]


def L_ubler17():
    return [(fl(r["z"]), ratio(r["vcirc_max_kms"], r["sigma0_kms"])) for r in rows("data_assembly/high_z_tf_tables/ubler2017.csv")]


def L_k3dcubes():
    return [(fl(r["Z"]), ratio(r["V22"], r["sig0"])) for r in rows("data_assembly/kmos3d_cubes/k3d_fits_main_final.csv")
            if r["status"] == "ok"]


def L_sinsao():
    t6 = {r["source"]: r for r in rows("data_assembly/highz_literature_tables/sins_ao/sins_ao_table6_kinematics.csv")}
    return [(fl(r["z_Halpha"]), fl(t6.get(r["source"], {}).get("Vrot_over_sigma0")))
            for r in rows("data_assembly/highz_literature_tables/sins_ao/sins_ao_table1_sample.csv")]


def L_sins09():
    return [(fl(r["z_halpha"]), fl(r["vrot_over_sig"])) for r in rows("data_assembly/high_z_tf_tables/sins2009_dynamics.csv")]


def L_rc100():
    return [(fl(r["z"]), ratio(r["Vc_Re_kms"], r["sigma0_kms"]))
            for r in rows("real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv")]


def L_msa3d():
    vs = {r["ID"]: fl(r["vsig"]) for r in rows("real_research/data/msa3d_2026_rotation_curves.csv")}
    return [(fl(r["z"]), vs.get(r["id"])) for r in rows("data_assembly/arxiv_tables/msa3d_galaxies.csv")]


def L_noema3d():
    return [(fl(r["z"]), fl(r["Vc_over_sigma0"])) for r in rows("data_assembly/noema3d/noema3d_per_galaxy.csv")]


def L_alpaka():
    zs = {r["id"]: fl(r["z"]) for r in rows("data_assembly/arxiv_tables/alpaka1_sample.csv")}
    return [(zs.get(r["id"]), fl(r["vext_over_sigma_ext"])) for r in rows("data_assembly/arxiv_tables/alpaka1_kinematics.csv")]


def L_alpaka_jwst():
    return [(fl(r["z"]), None) for r in rows("data_assembly/arxiv_tables/alpaka_jwst2026_data.csv")]


def L_lelli():
    # the mass-model table has no z column; z from the data README (zC-488879 1.47, zC-400569 2.24)
    gal = sorted({r["galaxy"] for r in rows("data_assembly/arxiv_tables/lelli2023_massmodels.csv")})
    zmap = {"zC-488879": 1.47, "zC-400569": 2.24}
    return [(zmap.get(g), None) for g in gal]


def L_amvrosiadis():
    zs = {r["alessid"]: fl(r["z"]) for r in rows("data_assembly/arxiv_tables/amvrosiadis_parent.csv")}
    return [(zs.get(r["alessid"]), ratio(r["vmax_kms"], r["sigma_kms"]))
            for r in rows("data_assembly/arxiv_tables/amvrosiadis_bestfit.csv")]


def L_phibss():
    return [(fl(r["z_co"]), None) for r in rows("data_assembly/kmos3d_phibss/phibss13_joined.csv")]


def L_girard():
    out = []
    for r in rows("data_assembly/highz_literature_tables/girard2021/girard2021_table1_galaxy_properties.csv"):
        z = fl(r["z"])
        if z is None or z < 0.9:
            continue
        v = ratio(r["vrot_mol_kms"], r["sigma0_mol_kms"]) or ratio(r["vrot_ion_kms"], r["sigma0_ion_kms"])
        out.append((z, v))
    return out


def L_kross():
    return [(fl(r["z_halpha"]), ratio(r["vc_kms_intrinsic_at_2Rhalf"], r["sigma0_kms"]))
            for r in rows("data_assembly/high_z_tf_tables/kross_v2.csv")]


def L_sharma():
    return [(fl(r["Redshift"]), fl(r["Rot_Disp_ratio_int"])) for r in rows("data_assembly/arxiv_tables/sharma2024_gs21b.csv")]


def L_mancera():
    return [(fl(r["z"]), fl(r["v_over_sigma_halpha"])) for r in rows("data_assembly/arxiv_tables/manceraPina2026_sample.csv")]


def L_zfire():
    return [(fl(r["z"]), ratio(r["V22_kms"], r["sigma_g_kms"]))
            for r in rows("data_assembly/highz_literature_tables/zfire2018/zfire_table3_kinematics.csv")]


def L_sigma():
    return [(fl(r["z_spec"]), ratio(r["vrot_kms"], r["sigma_g_kms"])) for r in rows("data_assembly/high_z_tf_tables/simons2016_sigma.csv")]


def L_musedark():
    return [(fl(r["z"]), ratio(r["v22"], r["sigma_fit_kms"])) for r in rows("data_assembly/musedark_catalogues/musedark_numeric.csv")]


NOREF = ("none on disk", "no z < 0.1 table with the same tracer, velocity definition, baryon recipe and method (R1-R5)")
SPARC = ("SPARC (CFG140 anchor)", "fails R2 (HI vs Halpha), R3 (measured HI gas vs none), R4 (no pressure term vs a large one), R5")
GIRARD = ("Girard+2021 DYNAMO rows", "fails R5 (z > 0.9 rows are a compilation of other papers and pipelines) and R2 (radius)")
TILEY = ("Tiley+2019 SAMI_matched", "R1, R2, R5 pass; fails R3 (no gas on either side, so no a0 estimator)")
# (id, name, loader, tracer, gas route, G2 pass, c_primary, src, c_optimistic, src, G4 note, reference)
REG = [
    (1, "KURVS-CDFS (rotation-supported)", L_kurvs, "Halpha KMOS, V at R'_3D/R'_6D", "none", False, 0.45, "CFG685 #1", 0.45, "-", "g_bar/a0 0.06-0.67 (CFG140): not all <= 0.5", SPARC),
    (2, "Genzel+2017 six curves", L_genzel, "Halpha SINS/KMOS curves", "scaling", False, 0.45, "CFG685 #3", 0.45, "-", "outer g ~1-3 a0 (CFG400)", NOREF),
    (3, "RC41 (Price+2021)", L_rc41, "Halpha fits at R_e", "scaling", False, 0.45, "CFG685 #3", 0.45, "-", "at R_e, near-Newtonian (CFG685)", NOREF),
    (4, "KMOS3D TF (Ubler+2017)", L_ubler17, "Halpha, max model V_c", "scaling", False, 0.45, "CFG685 #3", 0.45, "-", "massive, near-Newtonian (CFG685)", NOREF),
    (5, "KMOS3D raw-cube fits z >= 1.9", L_k3dcubes, "Halpha, own 3D fits", "none", False, 0.50, "CFG685 #7-11", 0.50, "-", "never inner and outer (CFG386)", NOREF),
    (6, "SINS/zC-SINF AO", L_sinsao, "Halpha AO, V_rot", "none", False, 0.50, "CFG685 #7-11", 0.50, "-", "one radius (CFG386)", NOREF),
    (7, "SINS 2009", L_sins09, "Halpha, mixed methods", "SFR inversion", False, 0.45, "CFG685 #3", 0.45, "-", "not shown", NOREF),
    (8, "RC100 (CORRECTED)", L_rc100, "V_c(R_e), author decompositions", "mixed (K 0.13)", False, 0.40, "CFG685 #4", 0.10, "CFG218", "lever 2.5-4.8 at R_e (CFG685)", NOREF),
    (9, "MSA-3D", L_msa3d, "NIRSpec ionised, V at R_e", "depletion-time scaling", False, 0.60, "CFG685 #5", 0.60, "-", "~2 R_e, lever ~2.5 (CFG685)", NOREF),
    (10, "NOEMA3D", L_noema3d, "CO, V_c at R_e,disk", "CO (+dust)", True, 0.40, "CFG685 #2", 0.043, "CFG218", "lever 2.5-4 at R_e (CFG685)", GIRARD),
    (11, "ALPAKA I", L_alpaka, "CO/[CI] 3D rings, V_ext", "CO/[CI] L'", True, 0.50, "CFG685 #7-11", 0.50, "-", "R_ext not tabulated: not shown", NOREF),
    (12, "ALPAKA-JWST", L_alpaka_jwst, "CO/[CI] + NIRCam", "CO/[CI]", True, 0.50, "CFG685 #7-11", 0.50, "-", "not shown", NOREF),
    (13, "Lelli+2023", L_lelli, "CO curves", "CO", True, 0.50, "CFG685 #7-11", 0.50, "-", "V^2/R > 3-4 a0 (paper)", NOREF),
    (14, "Amvrosiadis+2025", L_amvrosiadis, "CO, V_c at 2 r_e", "CO", True, 0.50, "CFG685 #7-11 class", 0.50, "-", "~10 a0 (data README)", NOREF),
    (15, "PHIBSS (Tacconi+2013)", L_phibss, "CO V_rot", "CO", True, 0.50, "CFG685 #7-11 class", 0.50, "-", "massive, near-Newtonian", NOREF),
    (16, "Girard+2021 compilation", L_girard, "mixed Halpha / CO", "mixed", False, 0.50, "CFG685 #7-11 class", 0.50, "-", "not shown", GIRARD),
    (17, "KROSS (Harrison+2017; Tiley+2019)", L_kross, "Halpha, V_2.2 / V_C at 2 R_1/2", "none", False, 0.45, "CFG685 #3 class", 0.45, "-", "no g_bar without gas", TILEY),
    (18, "KROSS GS21b (Sharma+2024)", L_sharma, "Halpha, V at R_out ~5 R_D", "scaling", False, 0.45, "CFG685 #3 class", 0.45, "-", "g_bar set by assumed gas", NOREF),
    (19, "Mancera Pina+2026", L_mancera, "Halpha, flat V_circ", "none", False, 0.45, "CFG685 #3 class", 0.45, "-", "not shown", NOREF),
    (20, "ZFIRE 2018", L_zfire, "MOSFIRE slit V_2.2", "none", False, 0.45, "CFG685 #3 class", 0.45, "-", "not shown", NOREF),
    (21, "SIGMA (Simons+2016)", L_sigma, "MOSFIRE slit V_rot", "none", False, 0.45, "CFG685 #3 class", 0.45, "-", "not shown", NOREF),
    (22, "MUSE-DARK", L_musedark, "MUSE [OII]", "modelled surface density", False, 0.30, "CFG218", 0.30, "-", "not shown", NOREF),
]
OOD = [("ALMA-CRISTAL", "data_assembly/arxiv_tables/cristal2025_sample.csv", "z_cii"),
       ("Roman-Oliveira+2023", "data_assembly/arxiv_tables/romanoliveira2023_sample.csv", "z"),
       ("Danhaive+2025", "data_assembly/arxiv_tables/danhaive2025_gold.csv", "z"),
       ("ALPINE (Jones+2021)", "data_assembly/highz_literature_tables/jones2021_alpine/jones2021_table1_sample_classes.csv", "z"),
       ("ALPINE corpus_z1", "data_assembly/highz_literature_tables/alpine_corpus_z1/corpus_z1_galaxies.csv", "redshift"),
       ("MIGHTEE-HI z > 0.25", "data_assembly/mightee_hi_highz/mightee_hi_highz.csv", "z"),
       ("BUDHIES", "data_assembly/high_z_tf_tables/budhies_hi.csv", "z_hi"),
       ("PHIBSS2 z 0.5-0.8", "data_assembly/phibss2_z05_08/phibss2_z05_08.csv", "z_optical")]

# ---- reference R1 re-check (counts of z < 0.1 rows in the named candidate tables) ---------------------------------
tiley = rows("data_assembly/high_z_tf_tables/tiley2019.csv")
n_sami = sum(r["survey"] == "SAMI_matched" for r in tiley)            # SAMI is z < 0.1 by survey definition (no z column)
n_dynamo = sum(1 for r in rows("data_assembly/highz_literature_tables/girard2021/girard2021_table1_galaxy_properties.csv")
               if fl(r["z"]) is not None and fl(r["z"]) < 0.1)

# ---- census and gates -----------------------------------------------------------------------------------------------
census = []
for (sid, name, loader, tracer, gas, g2, cp, cps, co, cos, g4, ref) in REG:
    data = loader()
    zs = [z for z, _ in data if z is not None]
    cells = {}
    for zk in ZS:
        sel = [(z, v) for z, v in data if zbin(z) == zk]
        if not sel:
            continue
        vs = [v for _, v in sel if v is not None]
        med = statistics.median(vs) if vs else None
        q = Q[zk]
        reasons = [f"no reference ({ref[0]}: {ref[1]})"]          # no registry sample has a qualifying reference (criteria 2)
        g1 = cp < q["e3"]
        if not g1:
            reasons.append(f"G1 c {cp:.2f} >= e_3sigma {q['e3']:.3f}")
        if not g2:
            reasons.append(f"G2 gas route '{gas}'")
        g3 = med is not None and med >= 6
        if not g3:
            reasons.append("G3 v/sigma " + (f"median {med:.1f} < 6" if med is not None else "not shown"))
        reasons.append(f"G4 {g4}")
        cells[zk] = dict(N=len(sel), n_vsig=len(vs), vsig_med=med, c_primary=cp, c_optimistic=co, e3=q["e3"],
                         G1=g1, G1_optimistic=co < q["e3"], G2=g2, G3=g3, G4=False, reference=False,
                         label="BLOCKED", reasons=reasons, ybar=None)
    census.append(dict(id=sid, name=name, tracer=tracer, gas=gas, N_file=len(data),
                       z_min=min(zs) if zs else None, z_max=max(zs) if zs else None,
                       N_in_domain=sum(c["N"] for c in cells.values()), c_primary=cp, c_primary_src=cps,
                       c_optimistic=co, c_optimistic_src=cos, reference=ref[0], reference_verdict=ref[1], cells=cells))
check("K8 every registry sample has >= 1 row in some z* bin", all(s["N_in_domain"] > 0 for s in census),
      ", ".join(f"#{s['id']} {s['N_in_domain']}" for s in census))
ood = []
for name, rel, col in OOD:
    zz = [fl(r[col]) for r in rows(rel)]
    zz = [z for z in zz if z is not None]
    nin = sum(zbin(z) is not None for z in zz)
    ood.append(dict(name=name, N=len(zz), z_min=min(zz), z_max=max(zz), N_in_bins=nin))
check("K8 out-of-domain samples have 0 rows in any bin", all(o["N_in_bins"] == 0 for o in ood),
      ", ".join(f"{o['name']} {o['N_in_bins']}" for o in ood))
n_graded = sum(1 for s in census for c in s["cells"].values() if c["label"] != "BLOCKED")
check("G0 no y-bar is formed in any BLOCKED cell", all(c["ybar"] is None for s in census for c in s["cells"].values()),
      f"{n_graded} cells graded")

# ---- K2 planted recovery, K3 MUTATE, K5 scrambled z ---------------------------------------------------------------
TRUTH = {"law": "T", "rival": "R"}
if MUTATE:
    TRUTH = {"law": "R", "rival": "T"}           # K3: the law and rival labels swapped
WANT = {"law": "DECIDES-law", "rival": "DECIDES-rival"}


def recover(N, c, zk, truth, gate=True, zgen=None, rng=None):
    q = Q[zk]
    qg = q
    e_stat = S_GAL / math.sqrt(N)
    hit = blocked = 0
    for _ in range(NDRAW):
        if zgen == "scramble":                  # K5: truth generated at one of the other three bins
            qg = Q[rng.choice([k for k in ZS if k != zk])]
        y = rng.gauss(qg[TRUTH[truth]], e_stat)
        lab = graded(y, e_stat, c, q, gate)
        hit += lab == WANT[truth]
        blocked += lab == "BLOCKED"
    return hit / NDRAW, blocked / NDRAW


rng = random.Random(SEED)
k2a = {zk: {t: recover(1000, 0.0, zk, t, rng=rng)[0] for t in WANT} for zk in ZS}
check("K2a powered control (N 1000, c 0): both laws recovered >= 95 % in every bin",
      all(v >= 0.95 for d in k2a.values() for v in d.values()),
      "; ".join(f"z {zk} law {d['law']:.3f} rival {d['rival']:.3f}" for zk, d in k2a.items()))
k2b_ok = True
for s in census:
    for zk, c in s["cells"].items():
        b = {t: recover(c["N"], c["c_primary"], zk, t, rng=rng)[1] for t in WANT}
        c["K2b_blocked_fraction"] = b
        k2b_ok &= all(v == 1.0 for v in b.values())
        c["K2c_c0_recovery"] = {t: recover(c["N"], 0.0, zk, t, rng=rng)[0] for t in WANT}
        c["K2d_copt_nogate_recovery"] = {t: recover(c["N"], c["c_optimistic"], zk, t, gate=False, rng=rng)[0] for t in WANT}
check("K2b every cell's own N and c_primary: gate blocks 100 % of planted draws", k2b_ok, "")
k5 = {zk: {t: recover(1000, 0.0, zk, t, zgen="scramble", rng=rng)[0] for t in WANT} for zk in ZS}
base = statistics.mean(v for d in k2a.values() for v in d.values())
scr = statistics.mean(v for d in k5.values() for v in d.values())
check("K5 scrambled z: rival recovery < 50 % in every bin and overall drop >= 20 points",
      all(d["rival"] < 0.5 for d in k5.values()) and (base - scr) >= 0.20,
      f"overall {base:.3f} -> {scr:.3f}; " + "; ".join(f"z {zk} law {d['law']:.3f} rival {d['rival']:.3f}" for zk, d in k5.items()))

# ---- K6 footings: the ratio cancels the footing --------------------------------------------------------------------
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}      # used ONLY here, never as a0,ref of graded data
k6 = {}
for zk in ZS:
    ys = {f: math.log10((a * 10 ** Q[zk]["T"]) / a) for f, a in FOOT.items()}
    labs = {f: outcome(y, 0.01, Q[zk]) for f, y in ys.items()}
    k6[zk] = dict(y=ys, label=labs, diff=abs(ys["canonical"] - ys["alt"]))
check("K6 footings cancel: y-bar and label identical across footings", all(d["diff"] < 1e-12 and len(set(d["label"].values())) == 1
      for d in k6.values()), "; ".join(f"z {zk} dy {d['diff']:.1e} {d['label']['canonical']}" for zk, d in k6.items()))

# ---- K7 inputs ------------------------------------------------------------------------------------------------------
code = open(os.path.abspath(__file__)).read().split("BANNED = [")[0]
BANNED = ["5.364", "0.315", "67.4", "rc100_nestorshachar2023_table3.csv", "table3_PUBLISHED"]
hits = [b for b in BANNED if b in code]
miss = [r for r in opened if not os.path.exists(P(r))]
check("K7 inputs: files exist; RC100 only _CORRECTED; no Planck/LCDM literals", not hits and not miss
      and any("_CORRECTED" in r for r in opened) and not any(r.endswith("table3.csv") for r in opened), f"hits {hits} missing {miss}")

# ---- report ---------------------------------------------------------------------------------------------------------
out = [f"AT2 a0(z) on-disk samples graded with AT1's rule, MUTATE={MUTATE}. Source cfg689.json BAO+SN.P1 (CFG689 primary).",
       "kappa = 1/2 FITTED; not theory closed. Footings never pooled. Not blind.", "",
       "z*    bin            e_3sigma  log sqrtX50  log E50",
       *[f"{zk:<5} [{BINS[zk][0]:.3f},{BINS[zk][1]:.3f})  {Q[zk]['e3']:.4f}    {Q[zk]['T']:+.4f}      {Q[zk]['R']:+.4f}" for zk in ZS],
       "", f"Reference candidates (R1 recount): Tiley+2019 SAMI_matched rows {n_sami}; Girard+2021 rows at z < 0.1: {n_dynamo}", "",
       "Per sample (N in bins 1.0 / 1.2 / 1.5 / 2.33; c_primary vs the bin's e_3sigma; label):"]
for s in census:
    ns = " / ".join(str(s["cells"][zk]["N"]) if zk in s["cells"] else "-" for zk in ZS)
    labs = sorted({c["label"] for c in s["cells"].values()})
    out.append(f"#{s['id']:<2} {s['name']:<36} z {s['z_min']:.2f}-{s['z_max']:.2f}  N_file {s['N_file']:<4} N_bins {ns:<18} "
               f"c {s['c_primary']:.2f} ({s['c_primary_src']}), c_opt {s['c_optimistic']:.3f}  -> {', '.join(labs)}")
    out.append(f"      reference: {s['reference']}: {s['reference_verdict']}")
    for zk, c in s["cells"].items():
        vm = f"{c['vsig_med']:.1f} (n {c['n_vsig']})" if c["vsig_med"] is not None else "not shown"
        out.append(f"      z* {zk:<4} N {c['N']:<4} v/sigma med {vm:<14} G1 {'pass' if c['G1'] else 'FAIL'}"
                   f" (opt {'pass' if c['G1_optimistic'] else 'FAIL'}) G2 {'pass' if c['G2'] else 'FAIL'}"
                   f" G3 {'pass' if c['G3'] else 'FAIL'} G4 FAIL  | K2c c=0 law {c['K2c_c0_recovery']['law']:.2f}"
                   f" rival {c['K2c_c0_recovery']['rival']:.2f} | K2d c_opt no-gate law {c['K2d_copt_nogate_recovery']['law']:.2f}"
                   f" rival {c['K2d_copt_nogate_recovery']['rival']:.2f}")
out += ["", "Out of domain (rows in any z* bin):"] + [f"  {o['name']}: N {o['N']}, z {o['z_min']:.2f}-{o['z_max']:.2f}, in bins {o['N_in_bins']}" for o in ood]
out += ["", "ONE DISC (AT1 does not apply): CFG970 Refsdal host; Ubler+2018; GS4_24110 (not on disk); U4_27928/U4_28473 (not on disk); Big Wheel (not in a file).", ""]
for n, ok, d in checks:
    out.append(f"[{'PASS' if ok else 'FAIL'}] {n}: {d}")
fail = [n for n, ok, _ in checks if not ok]
labels = {}
for s in census:
    for c in s["cells"].values():
        labels[c["label"]] = labels.get(c["label"], 0) + 1
out.append(f"CELLS: {sum(labels.values())} (sample, bin) cells; labels {labels}; samples {len(census)}")
out.append(f"RESULT: {len(checks) - len(fail)}/{len(checks)} checks pass" + (f"; FAIL {fail}" if fail else ""))
text = "\n".join(out) + "\n"
res = dict(mutate=MUTATE, bins=BINS, Q=Q, census=census, out_of_domain=ood, reference_recount=dict(sami_matched=n_sami, dynamo_lt_0p1=n_dynamo),
           K2a=k2a, K5=k5, K6=k6, checks=[dict(name=n, ok=ok, detail=d) for n, ok, d in checks])
jtext = json.dumps(res, indent=1, sort_keys=True, default=str) + "\n"

# ---- K4 byte-identical rerun (outer run only) ----------------------------------------------------------------------
if not INNER:
    tmp = tempfile.mkdtemp(prefix="at2_rerun_")
    env = dict(os.environ, AT2_INNER="1", AT2_OUTDIR=tmp)
    subprocess.run([sys.executable, os.path.abspath(__file__)], env=env, cwd=ROOT, capture_output=True, timeout=600)
    sha = lambda b: hashlib.sha256(b).hexdigest()
    try:
        o2 = open(os.path.join(tmp, f"at2{SUFFIX}.out"), "rb").read()
        j2 = open(os.path.join(tmp, f"at2{SUFFIX}.json"), "rb").read()
    except OSError:
        o2 = j2 = b""
    ok = o2 == text.encode() and j2 == jtext.encode()
    line = f"[{'PASS' if ok else 'FAIL'}] K4 byte-identical rerun: out sha256 {sha(text.encode())[:16]} vs {sha(o2)[:16]}, json {sha(jtext.encode())[:16]} vs {sha(j2)[:16]}\n"
    if not ok:
        fail.append("K4")
    text += line + f"FINAL: {len(checks) + 1 - len(fail)}/{len(checks) + 1} checks pass (K4 included)" + (f"; FAIL {fail}" if fail else "") + "\n"
open(os.path.join(OUTDIR, f"at2{SUFFIX}.out"), "w").write(text)
open(os.path.join(OUTDIR, f"at2{SUFFIX}.json"), "w").write(jtext)
print(text, end="")
sys.exit(1 if fail else 0)
