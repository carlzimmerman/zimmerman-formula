#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG6 (part 2) -- THE BRANCHES AGAINST THE RECORD'S a0(z) EVIDENCE: which branch the data prefer, how much an evolving dark
energy erodes or sharpens the z ~ 2.5 flat-a0 test, how many z ~ 1-2.5 objects would separate the branches, and what changes
elsewhere on the record's scorecard if a branch other than A (the unimodular tie, exactly flat) holds.

THE BRANCHES (part 1, CFG6_a0z_branches.py, whose main-run JSON this script reads):
  A  a0 reads the Henneaux-Teitelboim constant: flat for any dark-energy history.
  B  a0 ~ sqrt(rho_DE); C  a0 ~ sqrt(V); D  a0 ~ sqrt(-p).  Each FOLLOWING the DESI DR2 CPL fits (-CPL; needs a ghost or a
     braided dark energy past w = -1), or with a HEALTHY thawing field, w0-matched (-thaw(w0)) or conditioned on the posterior
     (-thaw(post)).  Uncertainties: the DESI DR2 public chains (L275's thinned copies).

THE EVIDENCE (the record's, not re-litigated; its readings inherited):
  - the a0(z) fork likelihood (prep_2026/a0z_crossscale/a0z_fork_likelihood_2026.py): 10 committed constraints (MSA-3D,
    MUSE-DARK III = Ciocan+26, Jeanneau+26, Ubler+17 KMOS3D z = 0.9 and 2.3, Amvrosiadis+25, Tiley+19 KROSS, the Big Wheel,
    McGaugh+24, Milgrom 2017), with the framework's own dilution lever and the LambdaCDM-degenerate apparent-drift nuisance
    marginalised over the record's four priors.  Its own head is executed read-only (as a0z_lcdm_native_hypothesis_2026.py
    does) so every model gets the identical treatment;
  - the RC100 closed-form inversion (hunt_2026/h16: d log a0/dz = -0.112 +/- 0.063, with its caveat);
  - the Jeanneau+26 deep-MOND refit (prep_2026/jeanneau_refit: Delta_b = +0.140 +/- 0.272 at z = 1.06, lever 0.76);
  - the 17-row high-z Tully-Fisher ledger (prep_2026/highz_tfr_fork/data_ledger.csv; L276's pulls);
  - MUSE-DARK III's apparent a0 at z ~ 1 (+0.377 dex; the record reads it as APPARENT, non-diagnostic);
  - the pre-registered z ~ 2.5 zero point (PAPER7: 0.00 vs LambdaCDM-native +0.334 (L274) at +/-0.13 dex), the JWST IFU
    forecast's per-object precision (prep_2026/a0z_crossscale/a0z_deepmond_ifu_forecast_2026) and M*'s flagship carrier
    residue (XR17: +0.106..+0.126 dex).

PRE-DECLARED (copied from the lane's hypothesis file, written 2026-09-27T16:03Z before any code of this lane ran):
  H8 controls: the fork likelihood's face chi^2 302.086/15.455/233.886 and marginalised log10 B under its four priors to 1e-6;
     h16's RC100 slope -0.1123 +/- 0.0625; the Jeanneau refit's 0.51 sigma; L276's max pulls; L274's +0.334.  EXPECT TRUE.
  H9 which branch: no branch beats A by |log10 B| > 0.5 on the drift-marginalised fork likelihood; at face value the rising
     branches win on Ciocan alone.  The RC100 slope prefers declining branches: B-CPL within 1 sigma, A at 1.8 sigma, healthy
     thawing at 2.5-3 sigma.  RC100 is the only datum separating branches at > 2 sigma, only against healthy thawing; with its
     caveat a lean, not a verdict.
  H10 erosion at sigma_obj = 0.13, z = 2.5: flat 2.57 sigma from LCDM-emergent; B-CPL 3.3, C-CPL 2.8, D-CPL 2.3, healthy
     thawing 1.4-2.0; healthy thawing + the flagship carrier residue (+0.106..+0.126, XR17) falls below 1 sigma.  EXPECT TRUE.
  H11 N objects (3 sigma, z = 2.5): A vs B-CPL ~16 at 0.13 (~170 at 0.43); A vs healthy thawing 6-31 at 0.13; each branch vs
     LCDM-emergent 2-6.  EXPECT within a factor 2.
  H12 elsewhere: gates at z <= 0.5 move by less than the committed canonical-vs-alt lever (0.0823 dex in a0); the forest stays
     >= 10x inside its line; the flagship is the one gate where a non-A branch matters (-0.10..+0.16 dex vs its +/-0.10
     tolerance).
  MUTATE: branch A reads rho_total: the fork-likelihood 'A = M-FLAT' control and the headline 'A inside +/-0.13 at 2.5' must
     FAIL, rc = 1.
"""
DOC_CHECKS = r"""
CHECKS
  C1 CONTROL the fork likelihood (its committed head executed read-only): face chi^2 of M-DEC/M-RISE/M-FLAT and the
     marginalised log10 B of its three pairs under its four priors equal its committed JSON (1e-6).
  C1b CONTROL branch A through the same machinery equals the committed M-FLAT (face chi^2 233.886; every prior) -- MUTATE fails it.
  C2 CONTROL h16's RC100 selection, closed-form inversion and bootstrap (its RNG replayed): -0.1123 +/- 0.0625 (N = 99).
  C3 CONTROL the Jeanneau refit's committed Delta_b, band, lever, z and the flat law's 0.51 sigma (re-derived).
  C4 CONTROL L276's bTFR pulls: 'max |pull| per law' for its five laws, re-derived from the ledger and L275's bands.
  C5 CONTROL the inputs this part quotes: L274's +0.334, XR17's residue range, the IFU forecast's per-object sigma(log a0).
  C6 CONTROL part 1's main-run results exist, are not the MUTATE file, and passed HEADLINE-FLAT with rc = 0.
  C7 CONTROL the environment null (A0_COSMICWEB_ENVIRONMENT_2026-06.md): the committed slopes and the rho_local fork's exclusion.
  E1 the branches on the fork likelihood: face and marginalised log10 Z relative to A, three subsets (all 10; without Ciocan;
     the clean near-a0 subset), both footings (the alt lever uses y_alt = y a0_can/a0_alt).  Dark-energy uncertainty
     marginalised: -CPL over 200 chain draws per combination, -thaw(w0) over 150, -thaw(post) over the part-1 node weights.
  E2 RC100: each branch's predicted d log a0/dz on the same 99 redshifts, and its pull.
  E3 the Jeanneau refit: each branch's Delta_b = -0.76 Delta log a0(1.06) and its pull.
  E4 the bTFR ledger rows (full systematics): each branch's chi^2 and max pull.
  E5 MUSE-DARK III: the gap left at z = 1 and the fraction closed.
  E6 the z ~ 2.5 zero point: separation from LambdaCDM-native (+0.334) and from H(z) (+0.576) at sigma_obj = 0.13, 0.215,
     0.257, 0.431; with M*'s flagship residue added; the erosion (or sharpening) relative to A.
  E7 the number of objects for a 3-sigma separation of each branch from A and from LambdaCDM-native at z = 1, 1.5, 2, 2.5,
     with and without a 0.05 dex coherent floor.
  E8 elsewhere: KiDS, cosmic shear, the forest, the flagship (prediction, edge margin, residue), clusters (eRASS1's eta
     trend), Harvey, the z ~ 0 gates, CMB lensing -- each branch's change against each gate's margin, sized by the committed
     canonical-vs-alt pair where one exists.
  E9 the environment null: each branch's predicted environmental slope against the measured ones.
  HEADLINE branch A's z = 2.5 prediction is 0.000, inside the pre-registered +/-0.13 -- MUTATE fails it.
  W  the ledger and the recommendation.
MUTATE=1: branch A reads rho_total (a0 ~ H(z)): C1b and HEADLINE must FAIL (rc = 1).

SCOPE.  Every datum and its reading are the record's; nothing is re-fitted.  The gate sizes in E8 are linear responses built
from committed canonical/alt pairs (a uniform +0.0823 dex shift in a0 at the gate's epoch); a redshift-dependent shift is
approximated by its value at the gate's epoch.  Harvey has no committed footing pair and is not sized.  The IFU per-object
precisions are the forecast's, at its design point y = 0.2.
"""
import os, sys, re, io, csv, json, math, time, copy, contextlib, warnings
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True                   # write nothing outside CFG6_* (no __pycache__)
import CFG6_common as C
import numpy as np

warnings.filterwarnings("ignore")
MUTATE = os.environ.get("MUTATE", "0") == "1"
NAME = "CFG6_a0z_evidence"
TXT = os.path.join(HERE, NAME + ("_MUTATE.out" if MUTATE else ".out"))
JSN = os.path.join(HERE, NAME + ("_results_MUTATE.json" if MUTATE else "_results.json"))
T_START = time.time()
TEE = C.Tee(TXT)
sys.stdout = TEE
OUT = {"lane": "CFG6", "part": "evidence, erosion, objects, elsewhere", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
R = C.Recorder(OUT)
P, banner, check = R.P, R.banner, R.check
dex = np.log10
P(__doc__.strip())
P(DOC_CHECKS.strip())
if MUTATE:
    P("\n  *** MUTATE=1: branch A reads the TOTAL density (a0 ~ H(z)); C1b and HEADLINE must FAIL ***")

# ================================================================================================ part 1's results
J1p = os.path.join(HERE, "CFG6_a0z_branches_results.json")
J1 = json.load(open(J1p))
G = J1["numbers"]["thaw_grid"]
GT = json.load(open(os.path.join(HERE, G["tracks_file"])))           # part 1's companion file (main run)
LAMS, OMS, ZG = np.array(GT["lams"]), np.array(GT["oms"]), np.array(GT["zg"])
W0G = np.array(GT["w0"])
TRK = {k: np.array(v) for k, v in GT["tracks"].items()}
PW = {k: np.array(v) for k, v in G["post_weights"].items()}
PRED1 = J1["numbers"]["P"]["pred"]
MAPKEY = {"B": "dens", "C": "V", "D": "press"}
CH_DATA = {k: C.load_chain(k) for k in C.DESI_ORDER}
rngD = np.random.default_rng(6)
DRAWS = {}
for k in C.DESI_ORDER:
    wt, w0s, was, oms = CH_DATA[k]
    idx = rngD.choice(len(wt), size=200, replace=True, p=wt / wt.sum())
    idx2 = rngD.choice(len(wt), size=150, replace=True, p=wt / wt.sum())
    DRAWS[k] = dict(cpl=np.stack([w0s[idx], was[idx], oms[idx]], 1), thaw=np.stack([w0s[idx2], was[idx2], oms[idx2]], 1))
ZF = np.round(np.linspace(0.0, 3.5, 141), 10)                     # fine grid for the thawing branch functions
R_A = (lambda z: np.sqrt(C.OM_M * (1 + np.asarray(z, float)) ** 3 + C.OM_L)) if MUTATE else (lambda z: np.ones_like(np.asarray(z, float)))


def thaw_w0_track(br, k, which):
    """the w0-matched thawing track (log10 ratio on ZF) for draws of combination k"""
    d = DRAWS[k]["thaw"]
    return C.thaw_interp_w0(LAMS, OMS, ZG, W0G, TRK[MAPKEY[br]], d[:, 0], d[:, 2], ZF)


THAW_W0 = {(br, k): thaw_w0_track(br, k, "thaw") for br in "BCD" for k in C.DESI_ORDER}
NODES = {br: C.thaw_nodes_at(ZG, TRK[MAPKEY[br]], ZF) for br in "BCD"}      # (nOm, nLam, nZF)


def branch_samples(br, z):
    """list of (weight, dlog a0(z)) samples for a branch realisation, per combination -> dict k -> (w, v)"""
    z = np.atleast_1d(np.asarray(z, float))
    out = {}
    for k in C.DESI_ORDER:
        if br == "A":
            out[k] = (np.array([1.0]), dex(R_A(z))[None, :])
        elif br.endswith("-CPL"):
            d = DRAWS[k]["cpl"]
            fn = C.CPL_MAPS[br[0]]
            out[k] = (np.ones(len(d)) / len(d), np.array([dex(fn(z, a, b)) for a, b, _ in d]))
        elif br.endswith("-thaw(w0)"):
            T = THAW_W0[(br[0], k)]
            out[k] = (np.ones(len(T)) / len(T), np.array([np.interp(z, ZF, t) for t in T]))
        elif br.endswith("-thaw(post)"):
            w = PW[k].ravel()
            N_ = NODES[br[0]].reshape(-1, len(ZF))
            keep = w > 1e-4 * w.max()
            out[k] = (w[keep] / w[keep].sum(), np.array([np.interp(z, ZF, t) for t in N_[keep]]))
        elif br == "rival H(z)":
            d = DRAWS[k]["cpl"]
            out[k] = (np.ones(len(d)) / len(d), np.array([dex(C.R_total(z, a, b, om)) for a, b, om in d]))
        elif br == "LCDM-emergent":
            out[k] = (np.array([1.0]), dex(C.lcdm_emergent(z))[None, :])
    return out


def wmed(w, v):
    i = np.argsort(v)
    c_ = np.cumsum(w[i]) / np.sum(w)
    return float(np.interp(0.5, c_, v[i])), float(np.interp(0.16, c_, v[i])), float(np.interp(0.84, c_, v[i]))


BRANCHES = ["A", "B-CPL", "C-CPL", "D-CPL", "B-thaw(w0)", "C-thaw(w0)", "D-thaw(w0)", "B-thaw(post)", "C-thaw(post)", "D-thaw(post)"]

# ================================================================================================ C controls
banner("C   CONTROLS")
PARENT = C.rpath("prep_2026", "a0z_crossscale", "a0z_fork_likelihood_2026.py")
src = open(PARENT).read()
cut = src.index("PAIRS = [")
ns = {"__file__": PARENT, "__name__": "cfg6_parent_loaded"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[:cut], ns)
POINTS, MODELS, ln_evidence = ns["POINTS"], ns["MODELS"], ns["ln_evidence"]
fork = json.load(open(C.rpath("prep_2026", "a0z_crossscale", "a0z_fork_likelihood_2026_results.json")))
PRIORS = [("face", 0.0), ("P-HALF  U[0,0.46]", 0.46), ("P-MAG   U[0,0.92]", 0.92), ("P-MSA   U[0,1.22]", 1.22), ("P-WIDE  U[0,1.50]", 1.50)]
L10 = math.log(10.0)
dmax1 = 0.0
lnZc = {pl: {m: ln_evidence(m, pm)[0] for m in ("M-DEC", "M-RISE", "M-FLAT")} for pl, pm in PRIORS}
for m in ("M-DEC", "M-RISE", "M-FLAT"):
    dmax1 = max(dmax1, abs(-2 * lnZc["face"][m] - fork["face_chi2"][m]))
for pl, pm in PRIORS[1:]:
    for a, b in (("M-DEC", "M-RISE"), ("M-DEC", "M-FLAT"), ("M-RISE", "M-FLAT")):
        dmax1 = max(dmax1, abs((lnZc[pl][a] - lnZc[pl][b]) / L10 - fork["marginalized"][pl]["log10B"][f"{a}_vs_{b}"]))
check("C1 CONTROL the fork likelihood's committed head, executed read-only: face chi^2 (M-DEC/M-RISE/M-FLAT) and the marginalised "
      "log10 B of its three pairs under the four drift priors equal its committed JSON",
      f"max |diff| {dmax1:.1e}; face chi^2 " + "/".join(f"{-2 * lnZc['face'][m]:.3f}" for m in ("M-DEC", "M-RISE", "M-FLAT")), dmax1 < 1e-6)
MODELS["CFG6-A"] = lambda z, w0=None, wa=None: R_A(z)
dA = max(abs(ln_evidence("CFG6-A", pm)[0] - lnZc[pl]["M-FLAT"]) for pl, pm in PRIORS)
check("C1b CONTROL branch A through the same machinery is the committed M-FLAT (the framework's flat law = its w -> -1 limit), "
      "face value and every prior", f"max |d ln Z| vs M-FLAT {dA:.1e}; A's face chi^2 {-2 * ln_evidence('CFG6-A', 0.0)[0]:.3f} "
      f"(committed M-FLAT {fork['face_chi2']['M-FLAT']:.3f})", dA < 1e-9)

rows_rc = list(csv.DictReader(open(C.rpath("real_research", "data", "rc100_nestorshachar2023_table3.csv"))))


def fnum(v):
    try:
        return float(v)
    except Exception:
        return float("nan")


gal = []
for r in rows_rc:
    z, lMb, Re, Vc, gRe = fnum(r["z"]), fnum(r["logMbar_Msun"]), fnum(r["Re_kpc"]), fnum(r["Vc_Re_kms"]), fnum(r["g_Re_ms2"])
    if not all(np.isfinite([z, lMb, Re, Vc, gRe])):
        continue
    gal.append(dict(z=z, Re=Re, gobs=gRe))
for r in rows_rc:
    zz, rr_ = fnum(r["z"]), fnum(r["Re_kpc"])
    for g in gal:
        if abs(g["z"] - zz) < 1e-9 and abs(g["Re"] - rr_) < 1e-9:
            g["fdm"] = fnum(r.get("fDM_within_Re", "nan"))
for g in gal:
    fdm = g.get("fdm", float("nan"))
    g["la"] = math.log10((1.0 - fdm) * g["gobs"] / (math.log(1.0 / fdm)) ** 2) if 0.02 < fdm < 0.98 else float("nan")
okg = [g for g in gal if np.isfinite(g["la"])]
zr, lar = np.array([g["z"] for g in okg]), np.array([g["la"] for g in okg])
rng16 = np.random.default_rng(1627)
sl16 = np.polyfit(zr, lar, 1)[0]
bs16 = np.array([np.polyfit(zr[i], lar[i], 1)[0] for i in (rng16.integers(0, len(zr), len(zr)) for _ in range(500))])
h16 = C.rd("hunt_2026/h16_h27_h97.out") or ""
s16 = f"[all] d log a_0/dz = {sl16:+.4f} +- {bs16.std():.4f} (N = {len(zr)})"
check("C2 CONTROL h16 (RC100 through the closed-form kernel inversion): this lane's replay of its selection, inversion and "
      "bootstrap (RNG 1627) prints the committed line", f"'{s16}' found in h16's .out: {s16 in h16}", s16 in h16)
SL_OBS, SL_SIG = float(sl16), float(bs16.std())

jr = C.rd("prep_2026/jeanneau_refit/deep_refit.rerun_2026-09-18.out") or ""
mj = {k: re.search(p_, jr) for k, p_ in (("db", r"Delta_b = ([+-][0-9.]+) dex"), ("band", r"HONEST BAND = .* = \+-([0-9.]+) dex"),
                                         ("lever", r"dilution: median ([0-9.]+) canonical"), ("z", r"z median ([0-9.]+)"),
                                         ("flat", r"sigma from canonical\(0\): ([0-9.]+)"))}
JE = {k: float(v.group(1)) for k, v in mj.items()} if all(mj.values()) else None
check("C3 CONTROL the Jeanneau+26 deep-MOND refit: Delta_b, the honest band, the median lever and z, and the flat law's committed "
      "0.51 sigma (re-derived as Delta_b/band)", f"{JE}; re-derived {JE['db'] / JE['band']:.2f} sigma" if JE else "NOT FOUND",
      JE is not None and abs(JE["db"] / JE["band"] - JE["flat"]) < 0.01)

l275 = json.load(open(C.rpath("fable_independent_2026", "L275_results.json")))
zg76 = np.linspace(0.0, 5.0, 101)
laws76 = {"framework, own law": np.zeros_like(zg76), "framework, DESI w(z) at face value": np.array(l275["bands"]["pressure"]["desy5sn"]["grid"]["med"]),
          "density mapping": np.array(l275["bands"]["density"]["desy5sn"]["grid"]["med"]), "H(z) law": np.array(l275["bands"]["hz"]["desy5sn"]["grid"]["med"]),
          "ΛCDM emergent scale": dex(C.lcdm_emergent(zg76))}
led = list(csv.DictReader(open(C.rpath("prep_2026", "highz_tfr_fork", "data_ledger.csv"))))
TFR = []
for r in led:
    z, db, st, sy, dil = fnum(r["z_eff"]), fnum(r["delta_b_dex_mass_axis"]), fnum(r["stat_err_dex"]), fnum(r["sys_est_dex"]), fnum(r["dilution_typ"])
    if np.isnan(db) or np.isnan(st):
        continue
    TFR.append(dict(study=r["study"], z=z, rel=r["relation"], db=db, st=st, sy=(0.0 if np.isnan(sy) else sy), dil=dil))
BT = [d for d in TFR if d["rel"].startswith("bTFR")]
mp76 = {nm: max(abs((d["db"] + d["dil"] * float(np.interp(d["z"], zg76, c))) / math.sqrt(d["st"] ** 2 + d["sy"] ** 2)) for d in BT)
        for nm, c in laws76.items()}
s76 = "max |pull| per law: " + ", ".join(f"{nm} {v:.1f}" for nm, v in mp76.items())
l276 = C.rd("fable_independent_2026/L276_data_vs_models_a0z.out") or ""
check("C4 CONTROL L276: the per-law maximum pull over the bTFR rows (full systematics, per-sample dilution) re-derived from the "
      "committed ledger and L275's bands", f"'{s76}' found in L276's .out: {s76 in l276}", s76 in l276)

l274 = C.rd("fable_independent_2026/L274_a0z_theories_chart.out") or ""
m274 = re.search(r"\(z = 2\.5: ([+-][0-9.]+) dex \(factor", l274)
LCDM25 = float(m274.group(1))
x17 = C.rd("real_research/cross_thread_review_2026_09_26/XR17_flagship_row_numbers.out") or ""
RES17 = [float(v) for v in re.findall(r"worst shift at z = 2\.5 \+([0-9.]+) dex", x17)]
ifu = json.load(open(C.rpath("prep_2026", "a0z_crossscale", "a0z_deepmond_ifu_forecast_2026_results.json")))
SIG_OBJ = {"PAPER7 requirement": 0.13}
for lab, key in (("JWST IFU + CO gas + incl.", "JWST IFU + gas 0.12 dex + inclination 4 deg, y = 0.2 (design point)"),
                 ("JWST IFU + CO gas", "JWST IFU + CO/dust gas 0.12 dex, y = 0.2 (design point)"),
                 ("JWST IFU only", "JWST IFU only (KS gas 0.30 dex), y = 0.2 (design point)")):
    SIG_OBJ[lab] = float(ifu["budgets"][key]["sigma_log_a0"])
check("C5 CONTROL the quoted inputs: L274's LambdaCDM-native +0.334 dex at z = 2.5; XR17's residue shifts at z = 2.5 for M*'s "
      "carrier (four kicks); the IFU forecast's per-object sigma(log a0) at its design point",
      f"LCDM +{LCDM25:.3f}; XR17 {RES17}; sigma_obj {SIG_OBJ}", abs(LCDM25 - 0.334) < 1e-9 and len(RES17) == 4
      and abs(min(RES17) - 0.1055) < 1e-9 and abs(max(RES17) - 0.1258) < 1e-9 and abs(SIG_OBJ["JWST IFU only"] - 0.431) < 1e-3)
hf1 = next((v["ok"] for k_, v in J1["checks"].items() if k_.startswith("HEADLINE-FLAT")), False)
c6 = (not J1["mutate"]) and hf1 and J1["verdict"]["n_fail_load_bearing"] == 0
check("C6 CONTROL part 1's main-run results: present, not the MUTATE file, HEADLINE-FLAT passed, no load-bearing failure",
      f"mutate {J1['mutate']}; HEADLINE-FLAT {hf1}; load-bearing failures {J1['verdict']['n_fail_load_bearing']}", c6)
env = C.rd("real_research/reviews/A0_COSMICWEB_ENVIRONMENT_2026-06.md") or ""
tofl = lambda s_: float(s_.replace("\u2212", "-"))
m2 = re.search(r"Slope d log a\u2080 / d log\(1\+\u03b4\) = \*\*([+\u2212-][0-9.]+) \u00b1 ([0-9.]+)\*\*", env)
m3 = re.search(r"slope \*\*([+\u2212-][0-9.]+) \u00b1 ([0-9.]+)\*\* \u2014 0\.6\u03c3 from 0", env)
mT = re.search(r"a\u2080 vs log M_halo: .*?slope ([+\u2212-][0-9.]+) \u00b1 ([0-9.]+)\.", env)
ENV = {k: (tofl(m.group(1)), float(m.group(2))) for k, m in (("2MRS", m2), ("2M++ (real space)", m3), ("Tully group mass", mT)) if m}
FORK = {k: (0.5 - v[0]) / v[1] for k, v in ENV.items() if k != "Tully group mass"}   # the +0.5 fork lives on log(1 + delta); Tully is log M_halo
check("C7 CONTROL the environment null (the BIG-SPARC-class fork on the public SPARC, A0_COSMICWEB_ENVIRONMENT_2026-06.md): the "
      "committed slopes d log a0/d log(1 + delta) and their distance from the rho_local fork (+0.5), re-derived (the writeup "
      "quotes 10.5 and 6.8 sigma)", f"{ENV}; +0.5 excluded at " + ", ".join(f"{k} {v:.2f} sigma" for k, v in FORK.items()),
      len(ENV) == 3 and abs(FORK["2MRS"] - 10.5) <= 0.1 and abs(FORK["2M++ (real space)"] - 6.8) <= 0.1
      and "10.5\u03c3 from +0.5" in env and "6.8\u03c3 from +0.5" in env,
      "a0 is set by a spatially uniform density (rho_Lambda), not by the local one: the design constraint every branch must meet")

# ================================================================================================ E1 the fork likelihood
banner("E1  THE BRANCHES ON THE FORK LIKELIHOOD (log10 Z relative to branch A; > 0 favours the branch)")
SUBSETS = {"all 10": [P_["tag"] for P_ in POINTS], "no Ciocan": [P_["tag"] for P_ in POINTS if not P_["tag"].startswith("[2]")],
           "clean near-a0": [P_["tag"] for P_ in POINTS if P_["tag"].startswith(("[3]", "[7]", "[8]", "[9]", "[10]"))]}
PTS_ALT = copy.deepcopy(POINTS)
for P_ in PTS_ALT:
    if P_["kind"] == "RATIO":
        P_["y_gbar"] = P_["y_gbar"] * C.A0["canonical"] / C.A0["alt"]
        P_["L"] = ns["lever"](P_["y_gbar"])
FOOTPTS = {"canonical": POINTS, "alt": PTS_ALT}
ns["MODELS"]["CFG6-LCDM"] = lambda z, w0=None, wa=None: np.asarray(C.lcdm_emergent(z), float)


def lnZ_models(names_weights, pmax, pts):
    """ln of the weight-averaged evidence over a list of (model name, kwargs, weight)"""
    v = np.array([ln_evidence(nm, pmax, pts=pts, **kw)[0] for nm, kw, _ in names_weights])
    w = np.array([ww for _, _, ww in names_weights])
    m = v.max()
    return float(m + math.log(np.sum(w * np.exp(v - m)) / np.sum(w)))


def register(br, k):
    """model names + kwargs + weights for a branch realisation on combination k"""
    if br == "A":
        return [("CFG6-A", {}, 1.0)]
    if br.endswith("-CPL"):
        MODELS[f"CFG6-{br}"] = (lambda fn: (lambda z, w0=None, wa=None: fn(np.asarray(z, float), w0, wa)))(C.CPL_MAPS[br[0]])
        return [(f"CFG6-{br}", dict(w0=float(a), wa=float(b)), 1.0) for a, b, _ in DRAWS[k]["cpl"]]
    if br.endswith("-thaw(w0)"):
        lst = []
        for s_, t in enumerate(THAW_W0[(br[0], k)]):
            nm = f"CFG6-{br}|{k}|{s_}"
            MODELS[nm] = (lambda tt: (lambda z, w0=None, wa=None: 10 ** np.interp(np.asarray(z, float), ZF, tt)))(t)
            lst.append((nm, {}, 1.0))
        return lst
    if br.endswith("-thaw(post)"):
        w = PW[k].ravel()
        N_ = NODES[br[0]].reshape(-1, len(ZF))
        lst = []
        for j in np.where(w > 1e-3 * w.max())[0]:
            nm = f"CFG6-{br}|{k}|{j}"
            MODELS[nm] = (lambda tt: (lambda z, w0=None, wa=None: 10 ** np.interp(np.asarray(z, float), ZF, tt)))(N_[j])
            lst.append((nm, {}, float(w[j])))
        return lst
    if br == "rival H(z)":
        return [("M-RISE", {}, 1.0)]
    if br == "LCDM-emergent":
        return [("CFG6-LCDM", {}, 1.0)]


E1 = {}
t_e1 = time.time()
for foot, pts_all in FOOTPTS.items():
    ns["_arr_cache"].clear()
    for sub, tags in SUBSETS.items():
        pts = [P_ for P_ in pts_all if P_["tag"] in tags]
        for br in BRANCHES + ["rival H(z)", "LCDM-emergent"]:
            for k in (C.DESI_ORDER if br not in ("A", "rival H(z)", "LCDM-emergent") else ["DESY5"]):
                nw = register(br, k)
                for pl, pm in PRIORS:
                    E1[(foot, sub, br, k, pl)] = lnZ_models(nw, pm, pts)
P(f"    evidences computed in {time.time() - t_e1:.0f} s")
TAB1 = {}
for foot in ("canonical", "alt"):
    P(f"\n    {foot} footing: log10 Z(branch) - log10 Z(A), DESY5 draws (Pantheon+ / Union3 in brackets for the dark-energy branches)")
    P(f"    {'branch':15s} {'subset':14s} " + "".join(f"{pl.split()[0]:>22s}" for pl, _ in PRIORS))
    for br in BRANCHES[1:] + ["rival H(z)", "LCDM-emergent"]:
        for sub in SUBSETS:
            cells = []
            for pl, _ in PRIORS:
                base = E1[(foot, sub, "A", "DESY5", pl)]
                if br in ("rival H(z)", "LCDM-emergent"):
                    v = (E1[(foot, sub, br, "DESY5", pl)] - base) / L10
                    cells.append(f"{v:+.2f}".rjust(22))
                    TAB1[(foot, br, sub, pl)] = [v]
                else:
                    vv = [(E1[(foot, sub, br, k, pl)] - base) / L10 for k in C.DESI_ORDER]
                    TAB1[(foot, br, sub, pl)] = vv
                    cells.append(f"{vv[0]:+.2f} [{vv[1]:+.2f}/{vv[2]:+.2f}]".rjust(22))
            P(f"    {br:15s} {sub:14s} " + "".join(cells))
OUT["numbers"]["E1"] = {"|".join(k): v for k, v in TAB1.items()}
SUMM = {}                                                           # max |log10 B| of any dark-energy branch vs A, per subset/prior
for sub in SUBSETS:
    for pl, _ in PRIORS:
        vals = [(v, br) for (foot, br, sb, p_), vv in TAB1.items() for v in vv if sb == sub and p_ == pl and br in BRANCHES]
        vmax, bmax = max(vals, key=lambda t: abs(t[0]))
        SUMM[(sub, pl)] = (vmax, bmax)
P("\n    largest |log10 B| of any dark-energy branch against A (any footing, any combination):")
for sub in SUBSETS:
    P(f"    {sub:14s} " + "".join(f"{pl.split()[0]:>8s} {SUMM[(sub, pl)][0]:+6.2f}" for pl, _ in PRIORS))
OUT["numbers"]["E1_summary"] = {f"{a}|{b}": v for (a, b), v in SUMM.items()}
marg_max = max(abs(v) for (foot, br, sub, pl), vv in TAB1.items() for v in vv
               if br in BRANCHES and pl.startswith(("P-MAG", "P-MSA")))
face_rise = [TAB1[("canonical", br, "all 10", "face")][0] for br in ("C-thaw(w0)", "D-CPL", "D-thaw(w0)")]
check("E1 = H9 (reported as it falls) no dark-energy branch beats or loses to A by more than |log10 B| = 0.5 on the drift-marginalised "
      "fork likelihood (P-MAG, P-MSA; every subset, footing and combination); at face value the rising branches are favoured "
      "(Ciocan alone)", f"max |log10 B| under P-MAG/P-MSA {marg_max:.2f}; face value, all 10, C-thaw(w0)/D-CPL/D-thaw(w0) vs A: " +
      "/".join(f"{v:+.2f}" for v in face_rise), marg_max <= 0.5 and all(v > 0 for v in face_rise), load_bearing=False)

# ================================================================================================ E2-E5 the individual data
banner("E2-E5  RC100's slope, the Jeanneau refit, the bTFR ledger, MUSE-DARK III -- per branch (DESY5 draws; P+/U3 medians)")
ROWS = {}
for br in BRANCHES + ["rival H(z)", "LCDM-emergent"]:
    sl = branch_samples(br, zr)
    j106 = branch_samples(br, [JE["z"]])
    m1 = branch_samples(br, [1.0])
    bt = branch_samples(br, [d["z"] for d in BT])
    row = {}
    for k in (C.DESI_ORDER if br not in ("A", "LCDM-emergent") else ["DESY5"]):
        w, V = sl[k]
        slopes = np.array([np.polyfit(zr, v, 1)[0] for v in V])
        s_med = wmed(w, slopes)[0]
        w2, V2 = j106[k]
        dbp = -JE["lever"] * wmed(w2, V2[:, 0])[0]
        w3, V3 = m1[k]
        d1 = wmed(w3, V3[:, 0])[0]
        w4, V4 = bt[k]
        vbt = np.array([wmed(w4, V4[:, i])[0] for i in range(len(BT))])
        pulls = np.array([(d["db"] + d["dil"] * vbt[i]) / math.sqrt(d["st"] ** 2 + d["sy"] ** 2) for i, d in enumerate(BT)])
        row[k] = dict(slope=s_med, rc100_pull=(SL_OBS - s_med) / SL_SIG, jeanneau_db=dbp, jeanneau_pull=(JE["db"] - dbp) / JE["band"],
                      bTFR_chi2=float(np.sum(pulls ** 2)), bTFR_maxpull=float(np.max(np.abs(pulls))), muse_z1=d1)
    ROWS[br] = row
MU = math.log10(2.38)                                               # L276's banked MUSE-DARK III a0|z~1 = 2.38 vs a0(0) = 1.0
for br in ROWS:
    for k in ROWS[br]:
        ROWS[br][k]["muse_gap"] = MU - ROWS[br][k]["muse_z1"]
        ROWS[br][k]["muse_frac"] = ROWS[br][k]["muse_z1"] / MU
P(f"    RC100 observed d log a0/dz = {SL_OBS:+.4f} +/- {SL_SIG:.4f}; Jeanneau Delta_b = {JE['db']:+.3f} +/- {JE['band']:.3f} at z = {JE['z']}; "
  f"MUSE +{MU:.3f} dex at z = 1; bTFR rows {len(BT)}")
P(f"    {'branch':15s} {'RC100 slope':>12s} {'pull':>6s} {'Jeanneau Db':>12s} {'pull':>6s} {'bTFR chi2':>10s} {'max':>5s} "
  f"{'z=1':>7s} {'MUSE gap':>9s} {'closed':>7s}")
for br, row in ROWS.items():
    r_ = row["DESY5"]
    alt = "" if len(row) == 1 else "   P+/U3 RC100 pull " + "/".join(f"{row[k]['rc100_pull']:+.2f}" for k in ("Pantheon+", "Union3"))
    P(f"    {br:15s} {r_['slope']:+12.4f} {r_['rc100_pull']:+6.2f} {r_['jeanneau_db']:+12.3f} {r_['jeanneau_pull']:+6.2f} "
      f"{r_['bTFR_chi2']:10.2f} {r_['bTFR_maxpull']:5.2f} {r_['muse_z1']:+7.3f} {r_['muse_gap']:+9.3f} {r_['muse_frac']:7.1%}" + alt)
OUT["numbers"]["E2_E5"] = ROWS
lcdm_lin = math.log10(2.13) / 2.5
P(f"    (h16's linear LambdaCDM-native slope log10(2.13)/2.5 = {lcdm_lin:+.4f}: pull {(SL_OBS - lcdm_lin) / SL_SIG:+.2f}; the exact DM14 "
  f"slope on the same redshifts is in the LCDM-emergent row)")
rp = {br: max(abs(ROWS[br][k]["rc100_pull"]) for k in ROWS[br]) for br in ROWS}
check("E2 = H9 (RC100, reported as it falls) the RC100 slope prefers declining branches: B-CPL within 1 sigma, A at 1.8 sigma, the "
      "healthy thawing branches at 2.5-3 sigma", ", ".join(f"{br} {ROWS[br]['DESY5']['rc100_pull']:+.2f}" for br in ROWS),
      abs(ROWS["B-CPL"]["DESY5"]["rc100_pull"]) < 1 and 1.6 < abs(ROWS["A"]["DESY5"]["rc100_pull"]) < 2.0
      and all(2.5 <= abs(ROWS[br]["DESY5"]["rc100_pull"]) <= 3.0 for br in ("B-thaw(w0)", "C-thaw(w0)", "D-thaw(w0)")), load_bearing=False)
others = {br: max(max(abs(ROWS[br][k]["jeanneau_pull"]), ROWS[br][k]["bTFR_maxpull"]) for k in ROWS[br]) for br in BRANCHES}
check("E3/E4 (reported) the Jeanneau refit and the bTFR ledger separate no branch: every branch within 1 sigma of the refit and "
      "within 2 sigma of every bTFR row", ", ".join(f"{br} {v:.2f}" for br, v in others.items()), max(others.values()) < 2.0,
      "the archival Tully-Fisher arm stays undecided (FORK_RESULTS, L276)", load_bearing=False)
check("E5 (reported) no branch reaches MUSE-DARK III's apparent +0.377 dex at z = 1: the smallest gap is > 0.2 dex, so MUSE stays "
      "non-diagnostic of the branch (the record reads it as an apparent, method-localised a0)",
      ", ".join(f"{br} {ROWS[br]['DESY5']['muse_gap']:+.3f}" for br in BRANCHES), min(ROWS[br][k]["muse_gap"] for br in BRANCHES for k in ROWS[br]) > 0.2,
      load_bearing=False)

# ================================================================================================ E6 the z = 2.5 test
banner("E6  THE z ~ 2.5 ZERO POINT: separation from LambdaCDM-native (+0.334) and H(z), per branch; the erosion relative to A")
Z25 = {br: {k: wmed(*[a[:, 0] if a.ndim == 2 else a for a in branch_samples(br, [2.5])[k]]) for k in (C.DESI_ORDER if br != "A" else ["DESY5"])}
       for br in BRANCHES}
HZ25 = 0.576
E6 = {}
P(f"    {'branch':15s} {'z=2.5 [68%]':>22s} " + "".join(f"{lab[:18]:>20s}" for lab in SIG_OBJ) + f"{'+XR17 res (0.13)':>20s} {'vs H(z) (0.13)':>16s}")
for br in BRANCHES:
    med, lo, hi = Z25[br]["DESY5"]
    sb = (hi - lo) / 2
    seps = {lab: (LCDM25 - med) / math.sqrt(s ** 2 + sb ** 2) for lab, s in SIG_OBJ.items()}
    cont = [(LCDM25 - med - r) / math.sqrt(0.13 ** 2 + sb ** 2) for r in (min(RES17), max(RES17))]
    E6[br] = dict(z25=med, band=[lo, hi], sep=seps, sep_with_residue=cont, sep_hz=(HZ25 - med) / 0.13,
                  other=[Z25[br][k][0] for k in Z25[br]])
    P(f"    {br:15s} {med:+.3f} [{lo:+.3f},{hi:+.3f}]    " + "".join(f"{v:20.2f}" for v in seps.values()) +
      f"{cont[1]:9.2f}..{cont[0]:.2f}{E6[br]['sep_hz']:16.2f}")
ero = {br: E6[br]["sep"]["PAPER7 requirement"] / E6["A"]["sep"]["PAPER7 requirement"] for br in BRANCHES}
P("    erosion (<1) or sharpening (>1) of the flat test's separation from LambdaCDM at 0.13: " + ", ".join(f"{br} {v:.2f}" for br, v in ero.items()))
OUT["numbers"]["E6"] = dict(rows=E6, erosion=ero)
pre = {"A": 2.57, "B-CPL": 3.3, "C-CPL": 2.8, "D-CPL": 2.3}
h10 = (all(abs(E6[b]["sep"]["PAPER7 requirement"] - v) <= 0.15 for b, v in pre.items())
       and all(1.4 <= E6[b]["sep"]["PAPER7 requirement"] <= 2.0 for b in ("C-thaw(w0)", "D-thaw(w0)"))
       and all(max(E6[b]["sep_with_residue"]) < 1.0 for b in ("C-thaw(w0)", "D-thaw(w0)")))
check("E6 = H10 (reported as it falls) at 0.13 dex per object: flat 2.57 sigma from LambdaCDM-native; B-CPL 3.3, C-CPL 2.8, D-CPL "
      "2.3; healthy thawing 1.4-2.0; healthy thawing plus M*'s flagship residue below 1 sigma",
      ", ".join(f"{b} {E6[b]['sep']['PAPER7 requirement']:.2f}" for b in BRANCHES) + "; with residue (thaw w0): " +
      ", ".join(f"{b} {min(E6[b]['sep_with_residue']):.2f}-{max(E6[b]['sep_with_residue']):.2f}" for b in ("C-thaw(w0)", "D-thaw(w0)", "C-thaw(post)")),
      h10, load_bearing=False)

# ================================================================================================ E7 the number of objects
banner("E7  HOW MANY OBJECTS: N for a 3-sigma separation (sigma_obj per object on log a0; coherent floor f)")


def n_obj(delta, s, f=0.0, k=3.0):
    t = (abs(delta) / k) ** 2 - f ** 2
    return float("inf") if t <= 0 else s ** 2 / t


ZN = [1.0, 1.5, 2.0, 2.5]
MEDZ = {br: {z: wmed(branch_samples(br, [z])["DESY5"][0], branch_samples(br, [z])["DESY5"][1][:, 0])[0] for z in ZN} for br in BRANCHES}
LCZ = {z: float(dex(C.lcdm_emergent(z))) for z in ZN}
E7 = {}
for lab_s, s in (("0.13", 0.13), ("0.257 (IFU + CO gas)", SIG_OBJ["JWST IFU + CO gas"]), ("0.431 (IFU only)", SIG_OBJ["JWST IFU only"])):
    for f in (0.0, 0.05):
        P(f"\n    sigma_obj {lab_s}, floor {f:.2f}:  {'':12s}" + "".join(f"{'z=' + str(z):>18s}" for z in ZN))
        for br in BRANCHES[1:]:
            vals = [n_obj(MEDZ[br][z] - MEDZ["A"][z], s, f) for z in ZN]
            vl = [n_obj(LCZ[z] - MEDZ[br][z], s, f) for z in ZN]
            E7[(lab_s, f, br)] = dict(vs_A=vals, vs_LCDM=vl)
            P(f"    {br:15s} vs A / vs LCDM: " + "".join((f"{v:7.0f}" if np.isfinite(v) else "    inf") + " /" + (f"{u:6.1f}" if np.isfinite(u) else "   inf") + "   " for v, u in zip(vals, vl)))
        vA = [n_obj(LCZ[z] - MEDZ["A"][z], s, f) for z in ZN]
        E7[(lab_s, f, "A")] = dict(vs_LCDM=vA)
        P(f"    {'A':15s}      vs LCDM:  " + "".join(f"{u:18.1f}" for u in vA))
OUT["numbers"]["E7"] = {f"{a}|{b}|{c}": v for (a, b, c), v in E7.items()}
nAB = E7[("0.13", 0.0, "B-CPL")]["vs_A"][3]
nAB43 = E7[("0.431 (IFU only)", 0.0, "B-CPL")]["vs_A"][3]
nth = [E7[("0.13", 0.0, b)]["vs_A"][3] for b in ("B-thaw(w0)", "C-thaw(w0)", "D-thaw(w0)")]
nL = [E7[("0.13", 0.0, b)]["vs_LCDM"][3] for b in BRANCHES[1:]] + E7[("0.13", 0.0, "A")]["vs_LCDM"][3:4]
check("E7 = H11 (reported as it falls, within a factor 2) at z = 2.5 and 3 sigma: A vs B-CPL ~16 objects at 0.13 (~170 at 0.43); "
      "A vs healthy thawing (w0-matched) 6-31 at 0.13; each branch vs LambdaCDM-native 2-6",
      f"A vs B-CPL {nAB:.0f} (0.13), {nAB43:.0f} (0.43); A vs thawing(w0) " + "/".join(f"{v:.0f}" for v in nth) +
      f"; vs LCDM {min(nL):.1f}-{max(nL):.1f}", 8 <= nAB <= 32 and 85 <= nAB43 <= 340 and all(3 <= v <= 62 for v in nth)
      and all(1 <= v <= 12 for v in nL), load_bearing=False)

# ================================================================================================ E8 elsewhere
banner("E8  WHAT CHANGES ELSEWHERE: each branch's shift at each gate's epoch against the gate's margin (DESY5 medians)")


def at(br, z):
    return wmed(branch_samples(br, [z])["DESY5"][0], branch_samples(br, [z])["DESY5"][1][:, 0])[0]


de10 = json.load(open(C.rpath("real_research", "dark_energy_2026", "DE10_kids_converged_model_results.json")))["numbers"]["table"]["v600/w0.02"]["kids"]
sK = (de10["alt"] - de10["canonical"]) / C.LEVER_FOOT
ans = C.rd("real_research/cross_thread_review_2026_09_26/ANSWER_AS_IT_STANDS.md") or ""
mk = re.search(r"worst [\u2212-]([0-9.]+)\) against \+([0-9.]+)", ans)
KIDS_WORST, KIDS_LINE = -float(mk.group(1)), float(mk.group(2))    # the answer page: M*'s carrier worst -26.28 against +4
m4 = re.search(r"w = 0\.25, x_c0 = 2\.5, cap  1\.75 Mpc: worst R canonical ([0-9.]+), alt ([0-9.]+)",
               C.rd("real_research/mond_sector_gate_2026/MS4_smooth_gate_shear.out") or "")
SH = (float(m4.group(1)), float(m4.group(2)))
sS = (SH[1] - SH[0]) / C.LEVER_FOOT
de11 = json.load(open(C.rpath("real_research", "dark_energy_2026", "DE11_forest_converged_model_results.json")))["numbers"]["F1"]["cells"]
fc, fa = de11["L25_canonical_w0.02/z2.0"], de11["L25_alt_w0.02/z2.0"]
sF = math.log(fa / fc) / C.LEVER_FOOT
de1 = json.load(open(C.rpath("real_research", "dark_energy_2026", "DE1_vacuum_gate_flagship_results.json")))["numbers"]["E1"]
edge = {f: [r for r in de1[f"1.0/2.5/{f}/11.0"] if abs(r["z"] - 2.5) < 1e-9][0]["ratio"] for f in ("canonical", "alt")}
fp22 = json.load(open(C.rpath("real_research", "derivation_chain_2026", "FP22_who_feels_mond_results.json")))["numbers"]
actc, acta = fp22["L0"]["control"]["canonical/lin"]["ACT"], fp22["L0"]["control"]["alt/lin"]["ACT"]
sL = (acta - actc) / C.LEVER_FOOT
feff = [r["lin"] for r in fp22["L2_verdict"]["f_eff_b_real"]]
kn = C.KernelNuMono()


def dlnnu_dlna0(y):                                                  # d ln nu/d ln a0 = -d ln nu/d ln y, nu = 1 + h/y
    y = C.mp.mpf(y)
    nu = 1 + kn.h(y) / y
    dnu = (kn.hp(y) * y - kn.h(y)) / y ** 2
    return float(-dnu * y / nu)


sNu = float(np.mean([dlnnu_dlna0(y) for y in (0.33, 0.45, 0.58)]))


def dlogE25(br):
    """the branch's own expansion history at z = 2.5 against LambdaCDM at the same Omega_m (the dark energy's effect only)"""
    lE = lambda om: float(dex(np.sqrt(om * 3.5 ** 3 + 1 - om)))
    if br == "A":
        return 0.0
    if br.endswith("-CPL"):
        d = DRAWS["DESY5"]["cpl"]
        return float(np.median([float(dex(C.R_total(2.5, a, b, om))) - lE(om) for a, b, om in d]))
    if br.endswith("-thaw(w0)"):
        d = DRAWS["DESY5"]["thaw"]
        v = C.thaw_interp_w0(LAMS, OMS, ZG, W0G, TRK["logE"], d[:, 0], d[:, 2], [2.5])[:, 0]
        return float(np.median(v - np.array([lE(om) for om in np.clip(d[:, 2], OMS[0], OMS[-1])])))
    w = PW["DESY5"]
    lEn = C.thaw_nodes_at(ZG, TRK["logE"], [2.5])[:, :, 0] - np.array([[lE(om)] * len(LAMS) for om in OMS])
    return float(np.sum(w * lEn) / np.sum(w))
E8 = {}
zc = np.linspace(0.0, 1.0, 11)
P(f"    levers: KiDS {sK:+.1f} chi^2/dex (DE10 {de10['canonical']:.2f} -> {de10['alt']:.2f}); shear {sS:+.3f} R/dex (MS4 {SH[0]}/{SH[1]} vs 1.2); "
  f"forest x{math.exp(sF):.2f}/dex (DE11 {fc:.5f} -> {fa:.5f} vs 0.10); flagship edge r_e/r_F {edge['canonical']:.2f}/{edge['alt']:.2f}; "
  f"CMB-lensing ACT (uncut, linear) {sL:+.3f}/dex x f_eff {min(feff):.2f}-{max(feff):.2f}; cluster d ln nu/d ln a0 at y = 0.33-0.58 = {sNu:.3f}")
P(f"    {'branch':15s} {'KiDS dchi2':>10s} {'shear can/alt':>15s} {'forest':>9s} {'flag. dpred':>11s} {'edge (HT/DE)':>14s} {'+res vs LCDM':>13s} "
  f"{'eta slope':>10s} {'Harvey z.3':>10s} {'z<=.03':>7s} {'CMBlens':>8s}")
for br in BRANCHES:
    d025, d05, d2, d25, d03, d003, d15 = (at(br, z) for z in (0.25, 0.5, 2.0, 2.5, 0.3, 0.023, 1.5))
    dens25 = 2 * at("B" + br[1:], 2.5) if br != "A" else 0.0
    dE25 = dlogE25(br)
    etaz = np.array([at(br, z) for z in zc])
    eta_slope = -sNu * float(np.polyfit(zc, etaz, 1)[0])
    row = dict(kids=sK * d025, shear=(SH[0] + sS * d05, SH[1] + sS * d05), forest=fa * math.exp(sF * d2), flag_pred=d25,
               edge_HT=(0.75 * d25 - 2 * dE25, math.log10(edge["canonical"])), edge_DE=0.75 * d25 - 2 * dE25 + 0.5 * dens25,
               res_vs_lcdm=(LCDM25 - d25 - max(RES17), LCDM25 - d25 - min(RES17)), eta_slope=eta_slope, harvey_dlog_a0=d03,
               z0=d003, cmb=(sL * d15 * min(feff), sL * d15 * max(feff)))
    E8[br] = row
    P(f"    {br:15s} {row['kids']:+10.2f} {row['shear'][0]:7.3f}/{row['shear'][1]:5.3f} {row['forest']:9.5f} {d25:+11.3f} "
      f"{row['edge_HT'][0]:+6.3f}/{row['edge_DE']:+6.3f} {row['res_vs_lcdm'][0]:+6.3f}..{row['res_vs_lcdm'][1]:+.3f} {eta_slope:+10.4f} "
      f"{d03:+10.3f} {d003:+7.4f} {row['cmb'][1]:+8.4f}")
P(f"    margins: KiDS {KIDS_LINE - KIDS_WORST:.1f} (M*'s worst {KIDS_WORST} vs +{KIDS_LINE}); shear 1.2 - R = {1.2 - SH[0]:.3f}/{1.2 - SH[1]:.3f}; "
  f"forest line 0.10; flagship tolerance 0.10 dex (S_crit); flagship edge log(r_e/r_F) = {math.log10(edge['canonical']):.2f}/{math.log10(edge['alt']):.2f}; "
  f"eRASS1 eta trend +0.187 +/- 0.013 per unit z (constant a0 requires 0); Harvey +0.096 vs +0.10 (not sized: no footing pair)")
OUT["numbers"]["E8"] = E8
cross_shear = [br for br in BRANCHES if E8[br]["shear"][1] > 1.2]
z05 = {br: abs(at(br, 0.5)) for br in BRANCHES}
low_ok = [br for br in BRANCHES if max(abs(at(br, z)) for z in (0.023, 0.25, 0.3, 0.5)) < C.LEVER_FOOT]
check("E8 = H12 (reported as it falls) gates at z <= 0.5 move by less than the committed canonical-vs-alt lever (|d log a0| < 0.0823 "
      "dex) for every branch; the forest stays >= 10x inside its line; the flagship prediction moves by -0.10..+0.16 dex",
      f"branches within the lever at z <= 0.5: {low_ok}; |d log a0(0.5)|: " + ", ".join(f"{b} {v:.3f}" for b, v in z05.items()) +
      f"; worst forest {max(E8[b]['forest'] for b in BRANCHES):.4f}; flagship d pred {min(E8[b]['flag_pred'] for b in BRANCHES):+.3f}.."
      f"{max(E8[b]['flag_pred'] for b in BRANCHES):+.3f}; shear crosses 1.2 on the alt footing for {cross_shear}",
      len(low_ok) == len(BRANCHES) and max(E8[b]["forest"] for b in BRANCHES) < 0.01
      and -0.11 <= min(E8[b]["flag_pred"] for b in BRANCHES) and max(E8[b]["flag_pred"] for b in BRANCHES) <= 0.17, load_bearing=False)

# ================================================================================================ E9 the environment null
banner("E9  THE ENVIRONMENT NULL: every branch reads a spatially uniform density")
xr20 = json.load(open(C.rpath("real_research", "cross_thread_review_2026_09_26", "XR20_evolving_de_a0z_results.json")))
dloc = max(abs(v) for v in xr20["numbers"]["E6"].values())            # the potential tie's local response (XR20 E6), cluster centre
S_BR = {"A": 0.0, "C (alpha(phi), local)": dloc / math.log(10) / 3.0, "B, D (leaf-averaged)": 0.0}
for k, v in S_BR.items():
    P(f"    {k:24s}: predicted |d log a0/d log(1 + delta)| <= {v:.1e}" + ("  (XR20 E6's 3.4e-11 at a 1e14 Msun centre over a 3-dex contrast)" if "local" in k else ""))
pulls_env = {k: max(abs((0.0 - v[0]) / v[1]) for v in ENV.values()) for k in S_BR}
check("E9 every branch meets the environment null: the dark energy is uniform on galaxy scales, so a0 carries no environmental "
      "slope (A exactly 0; the local potential tie <= 1e-11; the leaf-averaged ties 0 in space), within 2 sigma of every "
      "measured slope, while the rho_local reading stays excluded",
      "max |pull| of a zero slope: " + ", ".join(f"{k} {v:.2f}" for k, v in pulls_env.items()) + f"; rho_local excluded at >= {min(FORK.values()):.1f} sigma",
      all(v < 2 for v in pulls_env.values()) and all(v > 6 for v in FORK.values()),
      "the evolving-dark-energy branches change a0 in time, never in space: they inherit the null's support for rho_Lambda over rho_local")
OUT["numbers"]["E9"] = dict(measured=ENV, fork_sigma=FORK, predicted=S_BR)

# ================================================================================================ HEADLINE
banner("HEADLINE: branch A's z = 2.5 prediction" + ("  [MUTATE: A reads rho_total]" if MUTATE else ""))
a25 = float(dex(R_A(2.5)))
check("HEADLINE branch A predicts 0.000 dex at z = 2.5 -- the pre-registered framework value, inside +/-0.13 -- for every dark-energy "
      "history", f"A at z = 2.5: {a25:+.3f} dex; separation from LambdaCDM-native {(LCDM25 - a25) / 0.13:.2f} sigma at 0.13",
      abs(a25) < 1e-12, "MUTATE: the rho_total tie is the rival a0 ~ H(z), +0.576 dex" if MUTATE else "")

# ================================================================================================ W the ledger
banner("W   THE LEDGER AND THE RECOMMENDATION")
LED = [
    ("X-CFG6-1", "DATA PREFER", f"all 10 fork constraints: the rising branches are favoured only while the drift prior is below the "
     f"record's headline (P-MAG up to {SUMM[('all 10', 'P-MAG   U[0,0.92]')][0]:+.2f}, from MUSE-DARK III); headline P-MSA "
     f"{SUMM[('all 10', 'P-MSA   U[0,1.22]')][0]:+.2f} ({SUMM[('all 10', 'P-MSA   U[0,1.22]')][1]}); without Ciocan at most "
     f"{max(abs(SUMM[('no Ciocan', pl)][0]) for pl, _ in PRIORS):.2f}; clean near-a0 subset at most "
     f"{max(abs(SUMM[('clean near-a0', pl)][0]) for pl, _ in PRIORS):.2f}: undecided; RC100's slope pulls A {ROWS['A']['DESY5']['rc100_pull']:+.2f}, B-CPL {ROWS['B-CPL']['DESY5']['rc100_pull']:+.2f}, "
     f"C-thaw(w0) {ROWS['C-thaw(w0)']['DESY5']['rc100_pull']:+.2f}, C-thaw(post) {ROWS['C-thaw(post)']['DESY5']['rc100_pull']:+.2f} "
     "(a constraint on a rise, not a detection of a decline: h16's caveat)"),
    ("X-CFG6-2", "EROSION", f"at 0.13 dex: A {E6['A']['sep']['PAPER7 requirement']:.2f} sigma from LambdaCDM-native; B-CPL "
     f"{E6['B-CPL']['sep']['PAPER7 requirement']:.2f}; C-CPL {E6['C-CPL']['sep']['PAPER7 requirement']:.2f}; D-CPL "
     f"{E6['D-CPL']['sep']['PAPER7 requirement']:.2f}; healthy thawing: w0-matched {E6['C-thaw(w0)']['sep']['PAPER7 requirement']:.2f} (C), "
     f"posterior-conditioned {E6['C-thaw(post)']['sep']['PAPER7 requirement']:.2f} (C)"),
    ("X-CFG6-3", "OBJECTS", f"3 sigma at z = 2.5: A vs LambdaCDM {E7[('0.13', 0.0, 'A')]['vs_LCDM'][3]:.1f} objects at 0.13 "
     f"({E7[('0.431 (IFU only)', 0.0, 'A')]['vs_LCDM'][3]:.0f} at 0.43); A vs B-CPL {nAB:.0f} ({nAB43:.0f}); A vs C-thaw(post) "
     f"{E7[('0.13', 0.0, 'C-thaw(post)')]['vs_A'][3]:.0f}"),
    ("X-CFG6-4", "ELSEWHERE", f"z <= 0.5 gates: KiDS |dchi2| <= {max(abs(E8[b]['kids']) for b in BRANCHES):.1f} against a {KIDS_LINE - KIDS_WORST:.0f} "
     f"margin; cosmic shear's alt margin (0.076) is crossed by {cross_shear}; forest <= {max(E8[b]['forest'] for b in BRANCHES):.4f} vs 0.10; "
     f"flagship prediction {min(E8[b]['flag_pred'] for b in BRANCHES):+.3f}..{max(E8[b]['flag_pred'] for b in BRANCHES):+.3f} dex"),
    ("X-CFG6-5", "ENVIRONMENT", "every branch ties a0 to a spatially uniform density: predicted environmental slope <= 1e-11 against "
     + ", ".join(f"{k} {v[0]:+.3f} +/- {v[1]:.3f}" for k, v in ENV.items()) + f"; rho_local excluded at >= {min(FORK.values()):.1f} sigma"),
]
for k_, t_, v_ in LED:
    P(f"    {k_:9s} {t_:11s} {v_}")
OUT["ledger"] = [dict(link=a, what=b, value=c) for a, b, c in LED]
check("W (reported) the ledger", f"{len(LED)} links", True, load_bearing=False)

n_fail = sum(1 for _, ok, lb in R.CH if lb and not ok)
banner("VERDICT")
P(f"""  Against the record's a0(z) evidence the data do not pick a branch.  On all ten fork constraints the rising branches win only
  while the LambdaCDM-degenerate drift prior is below the record's headline (face value up to {SUMM[('all 10', 'face')][0]:+.1f}, P-MAG
  {SUMM[('all 10', 'P-MAG   U[0,0.92]')][0]:+.2f} in log10 B), and every bit of that comes from MUSE-DARK III, which sits above every branch;
  at the headline prior the largest is {SUMM[('all 10', 'P-MSA   U[0,1.22]')][0]:+.2f} ({SUMM[('all 10', 'P-MSA   U[0,1.22]')][1]}); without MUSE-DARK III every branch is within
  {max(abs(SUMM[('no Ciocan', pl)][0]) for pl, _ in PRIORS):.2f} of the flat law, and within {max(abs(SUMM[('clean near-a0', pl)][0]) for pl, _ in PRIORS):.2f} on the clean near-a0 subset.
  RC100's slope, the one datum with power, leans against a rise (A {ROWS['A']['DESY5']['rc100_pull']:+.2f} sigma,
  healthy w0-matched thawing {ROWS['C-thaw(w0)']['DESY5']['rc100_pull']:+.2f}, the declining density branch {ROWS['B-CPL']['DESY5']['rc100_pull']:+.2f}), with h16's caveat.
  At z = 2.5 and 0.13 dex per object the flat law sits {E6['A']['sep']['PAPER7 requirement']:.2f} sigma from LambdaCDM-native; following the DESI fits the
  density and potential ties sharpen it (B {E6['B-CPL']['sep']['PAPER7 requirement']:.2f}, C {E6['C-CPL']['sep']['PAPER7 requirement']:.2f}) and the pressure tie erodes it slightly
  (D {E6['D-CPL']['sep']['PAPER7 requirement']:.2f});
  a healthy thawing field erodes it ({E6['C-thaw(post)']['sep']['PAPER7 requirement']:.2f} conditioned on the posterior, {E6['C-thaw(w0)']['sep']['PAPER7 requirement']:.2f} w0-matched).
  kappa stays FITTED; nothing here derives it; the data do not favour the framework over LambdaCDM.""")
OUT["verdict"] = dict(n_checks=len(R.CH), n_fail_load_bearing=n_fail)
json.dump(OUT, open(JSN, "w"), indent=1, default=str)
rc = 0 if n_fail == 0 else 1
P(f"\n  {len(R.CH) - sum(1 for _, ok, _l in R.CH if not ok)}/{len(R.CH)} checks pass; load-bearing failures: {n_fail}; wrote "
  f"{os.path.basename(JSN)}  ({time.time() - T_START:.0f} s)")
P(f"rc = {rc}")
TEE.flush()
sys.stdout = sys.__stdout__
TEE.close()
sys.exit(rc)
