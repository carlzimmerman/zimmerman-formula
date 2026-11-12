"""SRH1R grading (own code): stack, fit of the mass factor k, the statistic T of FROZEN_CRITERIA section 4, known answer
KA8, the MUTATE twins and the labels.
Usage: python3 -I srh1r_grade.py <work dir>
Outputs here: srh1r_grade.json / .out, srh1r_grade_MUTATE.json.
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from scipy.stats import chi2, f as fdist
from scipy.optimize import minimize_scalar
import srh1r_model as m

WORK = sys.argv[1]; OUT = []
def P(*a):
    s = " ".join(str(v) for v in a); print(s, flush=True); OUT.append(s)
L = np.load(os.path.join(WORK, "lens.npz")); zl, Mg, typ, patch, WGd, WW, ged = (L[k] for k in ("z", "Mgal", "typ", "patch", "WG", "WW", "ged"))
NU, NBIN, NP = len(zl), len(ged) - 1, 50; GB = np.arange(13); NG = len(GB); HART = (NP - NG - 2) / (NP - 1); PLINE = 0.05 / 3
R1 = np.sqrt(m.G_SI * Mg[:, None] * m.MSUN / ged[None, 1:]) / m.KPC; R2 = np.minimum(np.sqrt(m.G_SI * Mg[:, None] * m.MSUN / ged[None, :-1]) / m.KPC, 3000.0)
KF = 0.5 * 2.0 ** (np.arange(21) / 5); LKF = np.log(KF); KLO, KHI = 0.5, 8.0
lMg = np.log10(Mg)

def interp_k(nodes_k, arr):
    """arr[k_node, ...] -> on KF, (arr / k) linear in log k."""
    lk = np.log(nodes_k); out = np.empty((len(KF),) + arr.shape[1:])
    for a, k in enumerate(KF):
        i = int(np.clip(np.searchsorted(lk, math.log(k), side="right") - 1, 0, len(lk) - 2)); w = (math.log(k) - lk[i]) / (lk[i + 1] - lk[i])
        out[a] = k * ((1 - w) * arr[i] / nodes_k[i] + w * arr[i + 1] / nodes_k[i + 1])
    return out
_MOD = {}
def model(foot, case):
    """Per-lens cell models on KF: own halo, neighbours, permuted-position null (or None)."""
    key = (foot, case)
    if key not in _MOD:
        T = m.table(foot, case, cache=os.path.join(WORK, "tables"))
        own = np.stack([m.own_cells(T, lMg + math.log10(k), zl, R1, R2) for k in KF]) * m.DCONV
        N = np.load(os.path.join(WORK, f"nb_{foot}_{case}.npz")); nb = interp_k(N["k"], N["real"]); nul = interp_k(N["k"], N["null"]) if "null" in N.files else None
        _MOD[key] = (own, nb, nul, N)
    return _MOD[key]

def psum(mask, arr):
    """Patch sums of arr[lens, bin] over the masked lenses -> [patch, bin]."""
    return np.stack([np.bincount(patch[mask], arr[mask, b], NP) for b in range(arr.shape[1])], axis=1)
class Stack:
    def __init__(self, mask, MODk, WG=None):
        WG = WGd if WG is None else WG
        self.pg = psum(mask, WG); self.pw = psum(mask, WW); self.pm = np.stack([psum(mask, WW * MODk[a]) for a in range(len(KF))])   # [k, patch, bin]
        sw = self.pw.sum(0); self.D = 4 * m.G_SI * self.pg.sum(0) / sw; self.Dj = 4 * m.G_SI * (self.pg.sum(0) - self.pg) / (sw - self.pw)
        self.Mk = self.pm.sum(1) / sw; self.Mjk = (self.pm.sum(1)[:, None, :] - self.pm) / (sw - self.pw)[None]               # [k, bin], [k, patch, bin]
    def M(self, k):
        a = float(np.clip((math.log(k) - LKF[0]) / (LKF[1] - LKF[0]), 0, len(KF) - 1.000001)); i = int(a); w = a - i
        return k * ((1 - w) * self.Mk[i] / KF[i] + w * self.Mk[i + 1] / KF[i + 1]), k * ((1 - w) * self.Mjk[i] / KF[i] + w * self.Mjk[i + 1] / KF[i + 1])
def jcov(X): d = X - X.mean(0); return (NP - 1) / NP * d.T @ d
def kmin(fun):
    ks = np.exp(np.linspace(math.log(KLO), math.log(KHI), 241)); v = np.array([fun(k) for k in ks]); i = int(np.argmin(v))
    lo, hi = ks[max(i - 1, 0)], ks[min(i + 1, len(ks) - 1)]
    r = minimize_scalar(fun, bounds=(lo, hi), method="bounded", options=dict(xatol=1e-7)); return (r.x, r.fun) if r.fun <= v[i] else (ks[i], v[i])
def grade(S, Cinv_fixed=None):
    """The statistic of section 4 on the graded bins."""
    D, Dj = S.D[GB], S.Dj[:, GB]; CDi = np.linalg.inv(jcov(Dj))
    k0, _ = kmin(lambda k: float((D - S.M(k)[0][GB]) @ CDi @ (D - S.M(k)[0][GB])))
    if Cinv_fixed is None:
        C = jcov(Dj - S.M(k0)[1][:, GB]); Ci = HART * np.linalg.inv(C)
    else: C = None; Ci = Cinv_fixed
    kh, Tm = kmin(lambda k: float((D - S.M(k)[0][GB]) @ Ci @ (D - S.M(k)[0][GB])))
    onb = bool(kh < KLO * 1.005 or kh > KHI / 1.005); Mh = S.M(kh)[0]; r1 = D - S.M(1.0)[0][GB]
    Fst = (Tm / HART) * (NP - NG) / (NG * (NP - 1))
    return dict(T=float(Tm), p=float(chi2.sf(Tm, NG - 1)), k=float(kh), k0=float(k0), on_bound=onb, p_hotelling=float(fdist.sf(Fst, NG, NP - NG)),
                T_k1=float(r1 @ Ci @ r1), D=S.D.tolist(), M=Mh.tolist(), err=(np.sqrt(np.diag(jcov(S.Dj)))).tolist(), Cinv=Ci)
def line_status(g): return "NOT EVALUABLE" if g["on_bound"] else ("PASS" if g["p"] >= PLINE else "FAIL")
def gate(lines):
    st = [line_status(g) for g in lines.values()]
    return "NOT EVALUABLE" if "NOT EVALUABLE" in st else ("PASS" if all(s == "PASS" for s in st) else "FAIL")
SAMP = {"all": np.ones(NU, bool), "late": typ == 0, "early": typ == 1}
def run(foot, case, variant="F1.6_tieR", sub_null=False, own_only=False):
    own, nb, nul, _ = model(foot, case); MOD = own if own_only else (own + nb - (nul if sub_null else 0.0)); res = {}
    for sn, sm in SAMP.items():
        g = grade(Stack(L[variant] & sm, MOD)); g.pop("Cinv"); g["n"] = int((L[variant] & sm).sum()); g["status"] = line_status(g); res[sn] = g
    return dict(lines=res, gate=gate(res))
def brief(r): return "  ".join(f"{sn} T {g['T']:.2f} p {g['p']:.4f} k {g['k']:.3f} [{g['status']}]" for sn, g in r["lines"].items()) + f"  -> gate {r['gate']}"

RES = dict(lane="SRH1R", p_line=PLINE, T_line=float(chi2.isf(PLINE, NG - 1)), hartlap=HART, graded_bins=GB.tolist(), footings={})
MUT = dict(lane="SRH1R")
P(f"lenses carried {NU:,}; graded bins 0-12; line p >= {PLINE:.4f} (T <= {RES['T_line']:.2f}, 12 dof); Hartlap {HART:.4f}")
for v in ("F1.6_tieR", "F1.6_plain", "F1.3_tieR"):
    P(f"  set {v}: all {int(L[v].sum()):,}, late {int((L[v] & (typ == 0)).sum()):,}, early {int((L[v] & (typ == 1)).sum()):,}")
WIN = ("f0.40", "f0.50", "f0.60", "f0.70"); COMP = ("ref", "inf", "one1")
for foot in m.FOOTS:
    P(f"\n================ {foot} (a0 {m.A0[foot]:.4e})"); FR = {}; RES["footings"][foot] = FR
    # ---- KA8 plant
    own, nb, nul, N = model(foot, "f0.50"); MOD = own + nb; i2 = int(np.argmin(np.abs(KF - 2.0))); mask = L["F1.6_tieR"]
    g0 = grade(Stack(mask, MOD)); gp = grade(Stack(mask, MOD, WG=WW * MOD[i2] / (4 * m.G_SI)), Cinv_fixed=g0["Cinv"])
    FR["KA8"] = dict(pass_=bool(abs(gp["k"] - 2) < 1e-4 and gp["T"] < 1e-6), k=gp["k"], T=gp["T"])
    P(f"KA8 plant (f 0.5, k 2; the real sample's covariance): k {gp['k']:.6f}, T {gp['T']:.2e} -> {'PASS' if FR['KA8']['pass_'] else 'FAIL'}")
    # ---- neighbour k-interpolation check (reported): node k = 2 predicted from its two neighbours' nodes
    kn = N["k"]; pred = 2.0 * (0.5 * N["real"][2] / kn[2] + 0.5 * N["real"][4] / kn[4]); sw = psum(mask, WW).sum(0)
    a_, b_ = (psum(mask, WW * pred).sum(0) / sw)[GB], (psum(mask, WW * N["real"][3]).sum(0) / sw)[GB]; tot = (psum(mask, WW * MOD[i2]).sum(0) / sw)[GB]
    FR["nb_k_interp_check"] = float(np.max(np.abs(a_ - b_) / tot)); P(f"neighbour k-interpolation, double spacing, max error / total model: {FR['nb_k_interp_check']:.2e}")
    # ---- window, comparators
    FR["window"] = {}; FR["comparators"] = {}; FR["brackets"] = {}
    for c in WIN:
        r = run(foot, c); FR["window"][c] = r; P(f"{c}: {brief(r)}")
    for c in COMP:
        r = run(foot, c); FR["comparators"][c] = r; P(f"comparator {c}: {brief(r)}")
    # ---- brackets
    for c in WIN:
        b = dict(plain_tie=run(foot, c, variant="F1.6_plain"), veto_1p3=run(foot, c, variant="F1.3_tieR"), null_subtracted=run(foot, c, sub_null=True), own_only=run(foot, c, own_only=True))
        FR["brackets"][c] = b
        for bn, r in b.items(): P(f"  bracket {bn} {c}: {brief(r)}")
    # ---- per-bin table at f 0.5 (all), neighbour share, null
    r = FR["window"]["f0.50"]["lines"]["all"]; S = Stack(mask, nb); Sn = Stack(mask, nul)
    P("per bin, f 0.50, all (4 G DeltaSigma, 1e-12 m/s^2): bin | data +- err | model | neighbours | null")
    kh = r["k"]; nbk, nlk = S.M(kh)[0], Sn.M(kh)[0]; FR["per_bin_f0.50_all"] = dict(D=r["D"], err=r["err"], M=r["M"], nb=nbk.tolist(), null=nlk.tolist())
    for b in range(NBIN):
        P(f"  {b:2d}{'' if b < 13 else ' (not graded)'} | {r['D'][b] * 1e12:8.4f} +- {r['err'][b] * 1e12:.4f} | {r['M'][b] * 1e12:8.4f} | {nbk[b] * 1e12:8.4f} | {nlk[b] * 1e12:+.4f}")
    # ---- MUTATE
    ref_ = FR["window"]["f0.50"]; MU = {}
    r1 = run(foot, "mu1"); MU["MU1_share_x0.1"] = dict(run=r1, bites=bool(r1["gate"] == "FAIL"))
    r2 = run(foot, "mu2"); dT2 = r2["lines"]["all"]["T"] - ref_["lines"]["all"]["T"]; MU["MU2_no_reference_outside"] = dict(run=r2, dT_all=dT2, bites=bool(r2["gate"] == "FAIL" or abs(dT2) >= 4))
    r3 = run(foot, "mu3"); dT3 = r3["lines"]["all"]["T"] - ref_["lines"]["all"]["T"]; MU["MU3_f0.05"] = dict(run=r3, dT_all=dT3, bites=bool(r3["gate"] != ref_["gate"] or abs(dT3) >= 4))
    for mn, v in MU.items(): P(f"{mn}: {brief(v['run'])}" + (f"  dT(all) {v['dT_all']:+.2f}" if "dT_all" in v else "") + f"  -> {'bites' if v['bites'] else 'DOES NOT BITE'}")
    MUT[foot] = MU
    # ---- label
    gates = {c: FR["window"][c]["gate"] for c in WIN}; cg = {c: FR["comparators"][c]["gate"] for c in COMP}
    FR["all_lines_not_evaluable_everywhere"] = bool(all(g == "NOT EVALUABLE" for g in gates.values()))
    FR["gates"] = gates; FR["comparator_gates"] = cg; FR["mutate_bite"] = {mn: v["bites"] for mn, v in MU.items()}
    FR["does_not_separate"] = bool(len(set(gates.values()) | set(cg.values())) == 1)
    FR["fragile"] = bool(any(FR["brackets"][c][bn]["gate"] != gates[c] for c in WIN for bn in ("plain_tie", "veto_1p3", "null_subtracted")))
    P(f"gates: {gates}; comparators: {cg}; does not separate: {FR['does_not_separate']}; fragile: {FR['fragile']}")
json.dump(MUT, open(os.path.join(HERE, "srh1r_grade_MUTATE.json"), "w"), indent=1)

# ---------------------------------------------------------------- labels (known answers of the other scripts are read from their outputs)
KAm = json.load(open(os.path.join(HERE, "srh1r_model_ka.json")))["KA"]; KAd = json.load(open(os.path.join(HERE, "srh1r_data.json")))
ka_common = all(v["pass_"] for v in KAm.values()) and KAd["KA6"]["pass_"]
P(f"\nknown answers KA1-KA5, KA7 (model; KA2 as amended by A1): {[k + (' PASS' if v['pass_'] else ' FAIL') for k, v in KAm.items()]}; KA6 (data): {'PASS' if KAd['KA6']['pass_'] else 'FAIL'}")
for foot in m.FOOTS:
    FR = RES["footings"][foot]; ka = ka_common and FR["KA8"]["pass_"]; bite = all(FR["mutate_bite"].values()); g = FR["gates"]
    if not ka or not bite or FR["all_lines_not_evaluable_everywhere"]: lab = "NO VERDICT"
    elif any(v == "PASS" for v in g.values()): lab = "LENSING HOLDS IN THE WINDOW"
    elif all(v == "FAIL" for v in g.values()): lab = "LENSING FAILS IN THE WINDOW"
    else: lab = "NO VERDICT"
    FR["label"] = lab; FR["known_answers_pass"] = bool(ka); FR["mutate_all_bite"] = bool(bite)
    P(f"LABEL {foot}: {lab}" + (" [does not separate]" if FR["does_not_separate"] else "") + (" [fragile]" if FR["fragile"] else "")
      + f"   (known answers {'pass' if ka else 'FAIL'}; twins {'all bite' if bite else 'NOT ALL BITE'}; passing f: {[c for c, v in g.items() if v == 'PASS']})")
RES["note"] = "kappa = 1/2 FITTED; not theory closed; adopts nothing"
json.dump(RES, open(os.path.join(HERE, "srh1r_grade.json"), "w"), indent=1)
open(os.path.join(HERE, "srh1r_grade.out"), "w").write("\n".join(OUT) + "\n")
