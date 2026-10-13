#!/usr/bin/env python3
"""CFG658 G-CL (FROZEN_CRITERIA.md, 12c5ab6b3): clusters and groups under the one-action construction's law
nu_s = 1/2 + sqrt(1/4 + 1/y) (g_N = g^2/(g + a0)).  Harnesses exec'd read-only; the only change is the kernel.
  CL1  CFG686: raw KiDS-1000 shear around 8 ACCEPT clusters (stored stacks) vs law_dsigma from Chandra gas (all 18 brackets + Newton,
       same bootstrap seed and key order); CFG686's own verdict rule.
  CL2  X-COP: CFG4 cluster_table (eta at 1000 kpc) and CFG634 T3 cells (B = all baryons, HCB = condensed; R0 / RI / RNc4; headline
       and inner band 200-420 kpc), CFG634 t3_label.
  CL3  CFG652: eFEDS groups x raw KiDS-1000, models from cfg658_cl3_models.py (x1), CFG652's score code and frozen rule.
MUTATE (M-K) in the same pass: the harness kernel reproduces each recorded table.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg658_clusters.py  -> cfg658_clusters.out, cfg658_clusters_results.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys, io, json, math, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import warnings
warnings.filterwarnings("ignore")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
EXTD = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
T0 = time.time(); OUT, RES, CHK = [], {"lane": "CFG658", "gate": "CL", "criteria": "12c5ab6b3"}, {}
try:
    os.nice(10)
except OSError:
    pass


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}"); return bool(ok)


def nu_s(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def slice_src(src, a, b):
    i = src.index(a) if a else 0
    j = src.index(b, i) if b else len(src)
    return src[i:j]


sys.path.insert(0, LANES)
import CFG4_common as C4                                                       # noqa: E402  (read-only)
P(__doc__.split("Run:")[0].strip())

# ============================================================================ CL1 CFG686
P("\n== CL1  CFG686: raw KiDS-1000 shear around 8 ACCEPT clusters vs the law on each cluster's own Chandra gas ==")
P686 = os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_shear.py")
s686 = open(P686).read()
N6 = {"__file__": P686, "__name__": "cfg686_ro"}
argv0 = sys.argv; sys.argv = [P686, "unused"]; os.environ.pop("MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(slice_src(s686, None, "# ---- sources ----"), P686, "exec"), N6)
    exec(compile(slice_src(s686, "# ---- the law's prediction from ACCEPT gas ----", "# ---- self-test"), P686, "exec"), N6)
    _ln = [l for l in s686.splitlines() if l.startswith("EDGES = np.logspace(")]
    assert len(_ln) == 1
    exec(compile(_ln[0], P686, "exec"), N6)                                        # the source block's bin definition only
sys.argv = argv0
J686 = json.load(open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_results.json")))
cls = J686["clusters"]; byname = {c["name"]: c for c in N6["CL"]}
KEYS = list(cls[0]["pred"].keys())
BANDS6 = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
D_ = np.nan_to_num(np.array([x["dsig"] for x in cls])); E_ = np.array([x["err"] for x in cls])
W_ = np.where(np.isfinite(E_) & (E_ > 0), 1 / E_ ** 2, 0)


def preds_for(kernel):
    N6["nu_mono"] = kernel
    out = []
    for x in cls:
        cl = byname[x["name"]]; pr = {}
        for foot, a0 in N6["A0"].items():
            for bs in (-0.5, 0.0, 0.5):
                for fs in (0.10, 0.20, 0.30):
                    pr[f"{foot}|b{bs:+.1f}|f{fs:.2f}"] = N6["law_dsigma"](cl, a0, bs, fs)[0]
        pr["newton"] = N6["law_dsigma"](cl, 0.0)[0]
        out.append(pr)
    return out


def summary_of(pr):
    def A_of(sel, key):
        P_ = np.array([pr[i][key] for i in sel]); o = {}
        for b, j in BANDS6.items():
            num = (W_[sel][:, j] * D_[sel][:, j]).sum(); den = (W_[sel][:, j] * P_[:, j]).sum(); o[b] = num / den if den != 0 else np.nan
        return o
    allsel = np.arange(len(cls)); rb = np.random.default_rng(1); sm = {}
    for key in KEYS + ["newton"]:
        A = A_of(allsel, key); boots = [A_of(rb.integers(0, len(cls), len(cls)), key) for _ in range(1000)]
        sm[key] = {b: [float(A[b]), float(np.nanstd([bb[b] for bb in boots]))] for b in BANDS6}
    return sm


def verdict6(s):                                                                # CFG686's rule, copied verbatim in logic
    z = {b: (v[0] - 1) / v[1] if v[1] > 0 else 0 for b, v in s.items()}
    if any(z[b] <= -2 for b in z): return "LAW OVERPREDICTS"
    if z["OUTER"] >= 2: return "EXTENDED EXCESS"
    if z["INNER"] >= 2 or z["MID"] >= 2: return "CORE EXCESS"
    if all(abs(z[b]) < 2 for b in z): return "LAW SUFFICES"
    return "MIXED"


prm = preds_for(C4.nu_mono)
dp = max(float(np.max(np.abs(np.array(prm[i][k]) - np.array(cls[i]["pred"][k] if k != "newton" else cls[i]["newton"])) /
                      np.maximum(np.abs(np.array(cls[i]["pred"][k] if k != "newton" else cls[i]["newton"])), 1e-30)))
         for i in range(len(cls)) for k in KEYS + ["newton"])
smm = summary_of(prm)
ds = max(abs(smm[k][b][j] - J686["A"][k][b][j]) for k in smm for b in BANDS6 for j in (0, 1))
check("M-K CFG686: nu_mono reproduces the stored predictions (1e-9 rel) and the A table incl. bootstrap sigma (1e-9)",
      dp < 1e-9 and ds < 1e-9, f"pred max rel {dp:.1e}; A max |d| {ds:.1e}")
prs = preds_for(nu_s)
sms = summary_of(prs)
CL1 = {}
for foot in ("canonical", "alt"):
    k = f"{foot}|b+0.0|f0.20"
    CL1[foot] = dict(A=sms[k], label=verdict6(sms[k]), A_mono=smm[k], label_mono=verdict6(smm[k]))
    P(f"  {foot:9s} nu_s : " + "  ".join(f"{b} {v[0]:.2f}+-{v[1]:.2f}" for b, v in sms[k].items()) + f"  -> {CL1[foot]['label']}"
      f"   (nu_mono: " + "  ".join(f"{b} {v[0]:.2f}" for b, v in smm[k].items()) + f" -> {CL1[foot]['label_mono']})")
brs = {k: verdict6(sms[k]) for k in KEYS}
CL1["brackets"] = {x: list(brs.values()).count(x) for x in set(brs.values())}
P(f"  newton: " + "  ".join(f"{b} {v[0]:.2f}+-{v[1]:.2f}" for b, v in sms["newton"].items()) + f";  nu_s across 18 brackets: {CL1['brackets']}")
RES["CL1"] = CL1

# ============================================================================ CL2 X-COP
P("\n== CL2  X-COP (record's corrected audit rows): CFG4 cluster_table and CFG634 T3 cells ==")
P4 = os.path.join(LANES, "CFG4_clusters.py"); s4 = open(P4).read()
N4 = dict(C=C4, np=np, math=math, json=json, os=os, NEWT_ONLY=False, COSMIC=0.1200 / 0.02237, A0=C4.A0)
exec(compile(slice_src(s4, "AUD = json.load(", "def delta_l7("), P4, "exec"), N4)
exec(compile(slice_src(s4, "def cluster_table(", "TAB = {}"), P4, "exec"), N4)
J4 = json.load(open(os.path.join(LANES, "CFG4_clusters_results.json")))["numbers"]["H2"]
CL2 = {"CFG4": {}}
d4 = 0.0
for foot in C4.FOOTS:
    for kn, kf in (("nu_mono", C4.nu_mono), ("nu_s", nu_s)):
        rows = N4["cluster_table"](kf, foot, 0.0)
        e, r_, idr = (float(np.median([x[k] for x in rows])) for k in ("eta", "resid", "id_ratio"))
        CL2["CFG4"][f"{foot}|{kn}"] = dict(eta=e, resid=r_, id_ratio=idr, phantom=float(np.median([x["phantom_over_Mb"] for x in rows])))
        if kn == "nu_mono":
            d4 = max(d4, abs(e - J4[f"{foot}|nu_mono"]["eta"]))
        P(f"  CFG4 {foot:9s} {kn:7s}: eta(1000 kpc) {e:.3f}; residual beyond the law {r_:.2f} M_b; law's phantom "
          f"{CL2['CFG4'][f'{foot}|{kn}']['phantom']:.2f} M_b; identity/measured {idr:.3f}")
check("M-K CFG4: nu_mono reproduces eta 1.820 / 1.679 (1e-6)", d4 < 1e-6, f"max |d| {d4:.1e}")

P634 = os.path.join(LANES, "CFG634_condensed_baryon_source", "cfg634_static.py"); s634 = open(P634).read()
for d in (os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "cluster_measurement_audit_2026"),):
    sys.path.insert(0, d)
N34 = dict(os=os, sys=sys, io=io, math=math, json=json, contextlib=contextlib, np=np, C4=C4, REPO=REPO, LANES=LANES,
           FOOTS=("canonical", "alt"), COLD_X=0.1200 / 0.02237, P=lambda *a: None, check=lambda *a: None, NU_=None)
exec(compile(slice_src(s634, "def m_nfw(x):", "def sigma_hcb("), P634, "exec"), N34)
t3src = slice_src(s634, "# ===================================================================================================== T3 X-COP",
                  "T3 = {}").replace("C4.nu_mono(", "NU_(")
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(t3src, P634, "exec"), N34)
J634 = json.load(open(os.path.join(LANES, "CFG634_condensed_baryon_source", "cfg634_static_results.json")))["T3"]["rows"]
CELLS = [("B|R0", "all", "R0", 4.0), ("HCB|R0", "cond", "R0", 4.0), ("B|RI", "all", "RI", 4.0), ("HCB|RI", "cond", "RI", 4.0),
         ("B|RNc4", "all", "RN", 4.0), ("HCB|RNc4", "cond", "RN", 4.0)]
T3 = {}
d34 = 0.0
for kn, kf in (("nu_mono", C4.nu_mono), ("nu_s", nu_s)):
    N34["NU_"] = kf
    for nm, srcm, res, conc in CELLS:
        head = {f: N34["t3_cell"](f, srcm, res, conc) for f in N34["FOOTS"]}
        inner = {f: N34["t3_cell"](f, srcm, res, conc, band=(200, 420)) for f in N34["FOOTS"]}
        T3[f"{kn}|{nm}"] = dict(headline=head, label=N34["t3_label"](list(head.values())), inner=inner,
                                inner_label=N34["t3_label"](list(inner.values())))
        if kn == "nu_mono":
            for f in N34["FOOTS"]:
                d34 = max(d34, abs(head[f]["eta_median"] - J634[nm]["headline"][f]["eta_median"]),
                          abs(inner[f]["eta_median"] - J634[nm]["inner_200_420"][f]["eta_median"]))
        P(f"  CFG634 T3 {kn:7s} {nm:9s}: eta headline " + " / ".join(f"{head[f]['eta_median']:.3f}+-{head[f]['sigma']:.3f}" for f in N34["FOOTS"])
          + f" -> {T3[f'{kn}|{nm}']['label']:8s} | inner 200-420 " + " / ".join(f"{inner[f]['eta_median']:.3f}" for f in N34["FOOTS"])
          + f" -> {T3[f'{kn}|{nm}']['inner_label']}")
check("M-K CFG634 T3: nu_mono reproduces the recorded headline and inner-band eta for all six cells (1e-6)", d34 < 1e-6, f"max |d| {d34:.1e}")
CL2["T3"] = T3
cstar = "PASS" if (T3["nu_s|B|R0"]["label"] == "PASS" and T3["nu_s|B|R0"]["inner_label"] == "PASS") else \
    ("FAIL" if (T3["nu_s|B|R0"]["label"] == "FAIL" or T3["nu_s|B|R0"]["inner_label"] == "FAIL") else "TENSION")
CL2["Cstar_verdict"] = cstar
P(f"  C* as built (law on all baryons, pure field, no reservoir = B|R0): headline {T3['nu_s|B|R0']['label']}, inner {T3['nu_s|B|R0']['inner_label']} -> {cstar}")
RES["CL2"] = CL2

# ============================================================================ CL3 CFG652
P("\n== CL3  CFG652: 131 eFEDS groups x raw KiDS-1000 (x1 primary; (a) condensed source, (b) all baryons) ==")
W652 = os.path.join(EXTD, "cfg652_work"); W658 = os.path.join(EXTD, "cfg658_work")
I0 = np.load(os.path.join(W652, "cfg652_inputs.npz")); D0 = np.load(os.path.join(W652, "cfg652_esd.npz"))
MD = np.load(os.path.join(W652, "cfg652_models.npz")); MS = np.load(os.path.join(W658, "cfg658_cl3_models.npz"))
cl3m = json.load(open(os.path.join(HERE, "cfg658_cl3_models.json")))
check("M-K CFG652 model recompute with the stored kernel equals the stored models (5 groups, 1e-9; cfg658_cl3_models.py)", cl3m["ok"],
      f"max rel {cl3m['mutate_control_maxrel']:.1e}")
P652 = os.path.join(LANES, "CFG652_hot_group_discriminator", "cfg652_test.py"); s652 = open(P652).read()
RB = np.geomspace(30, 3000, 13); RC = np.sqrt(RB[1:] * RB[:-1])
USE = (RC >= 50) & (RC <= 1000); BAND = (RC >= 250) & (RC <= 1000); NPATCH = 30
keep = I0["Mcond"] > 0
D = {k: (D0[k][keep] if k in ("WG", "WX", "WW", "NN", "pg") else D0[k]) for k in D0.files}
N52 = dict(D=D, np=np)
exec(compile(slice_src(s652, "    def esd(sel_g, sel_r, comp=\"t\"):", "    allg = np.ones(").replace("\n    ", "\n").lstrip(), P652, "exec"), N52)
esd, model_stack = N52["esd"], N52["model_stack"]
n = int(keep.sum()); allg = np.ones(n, bool); allr = np.ones(len(D["rz"]), bool)
obs, boost = esd(allg, allr)
vals = np.array([esd(D["pg"] != p, D["pr"] != p)[0][USE] for p in range(NPATCH)]); m_ = vals.mean(0)
Cj = (NPATCH - 1) / NPATCH * (vals - m_).T @ (vals - m_)
nb = int(USE.sum()); hart = (NPATCH - nb - 2) / (NPATCH - 1); Ci = np.linalg.inv(Cj) * hart
from scipy.stats import chi2 as CHI2   # noqa: E402


def aout(o, m):
    return float(np.log10(np.sum(o[BAND]) / np.sum(m[BAND])))


def score(arrs):
    st = {}
    for model in "ab":
        ms = model_stack(arrs[model], allg); d = obs[USE] - ms[USE]
        ch = float(d @ Ci @ d); p = float(CHI2.sf(ch, nb)); A = aout(obs, ms)
        Aj = np.array([aout(esd(D["pg"] != q, D["pr"] != q)[0], model_stack(arrs[model], D["pg"] != q)) for q in range(NPATCH)])
        sA = float(math.sqrt((NPATCH - 1) / NPATCH * np.sum((Aj - Aj.mean()) ** 2)))
        st[model] = dict(model=ms[USE].tolist(), chi2=ch, p=p, A_out=A, sA=sA)
    dchi = st["b"]["chi2"] - st["a"]["chi2"]
    if st["a"]["p"] < 0.01 and st["b"]["p"] < 0.01: lab = "BOTH EXCLUDED"
    elif dchi >= 9 and st["a"]["p"] >= 0.01: lab = "(a) FAVOURED"
    elif dchi <= -9 and st["b"]["p"] >= 0.01: lab = "(b) FAVOURED"
    else: lab = "NOT DIAGNOSTIC"
    st["dchi2_b_minus_a"] = dchi; st["label"] = lab
    return st


J652 = json.load(open(os.path.join(LANES, "CFG652_hot_group_discriminator", "cfg652_test_results.json")))["verdicts"]
CL3, d52 = {}, 0.0
P("  R (kpc)   " + " ".join(f"{x:7.0f}" for x in RC[USE])); P("  obs       " + " ".join(f"{x:7.1f}" for x in obs[USE]))
for foot in ("canonical", "alt"):
    sm = score({m: MD[f"{foot}__x1__{m}"][keep] for m in "ab"})
    d52 = max(d52, abs(sm["a"]["chi2"] - J652[foot]["x1"]["a"]["chi2"]), abs(sm["b"]["chi2"] - J652[foot]["x1"]["b"]["chi2"]))
    ss = score({m: MS[f"{foot}__x1__{m}"][keep] for m in "ab"})
    CL3[foot] = dict(nu_s=ss, stored=dict(a_chi2=sm["a"]["chi2"], b_chi2=sm["b"]["chi2"], label=sm["label"]))
    for m in "ab":
        P(f"  {foot:9s} nu_s ({m}): chi2 {ss[m]['chi2']:.1f}/{nb} p {ss[m]['p']:.3g}  A_out {ss[m]['A_out']:+.3f} +- {ss[m]['sA']:.3f}   model "
          + " ".join(f"{x:6.1f}" for x in ss[m]["model"]) + f"   (stored kernel chi2 {sm[m]['chi2']:.1f})")
    P(f"  {foot:9s} nu_s: dchi2(b-a) {ss['dchi2_b_minus_a']:+.1f} -> {ss['label']}")
check("M-K CFG652: the stored models reproduce the recorded x1 chi2 (a, b; both footings) to 0.01", d52 < 0.01, f"max |d| {d52:.1e}")
RES["CL3"] = CL3

RES["checks"] = CHK; RES["elapsed_s"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, "cfg658_clusters_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg658_clusters.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(v["ok"] for v in CHK.values()) else 1)
