"""CFG887 -- is CFG880's 'clump sigma not universal' driven by sigma systematics?  Criteria: FROZEN_CRITERIA.md (1ff227ac7).
Inter-catalogue extra scatter (LVD vs McConnachie 2012, Collins 2013) as an empirical per-dwarf floor; then CFG880's fit, exec'd unchanged.
Run: python3 cfg887.py  (CFG887_MUTATE=1: inter-catalogue differences doubled).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, re, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG887_MUTATE") == "1"; SUF = "_MUTATE" if MUT else ""; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
DD = os.path.join(REPO, "real_research", "data", "dsph")
def fl(x):
    try:
        v = float(x); return None if math.isnan(v) else v
    except (TypeError, ValueError): return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(DD, f))):
        s = fl(r.get("vlos_sigma"))
        if s is None or fl(r.get("vlos_sigma_ul")) is not None: continue
        em, ep = fl(r.get("vlos_sigma_em")), fl(r.get("vlos_sigma_ep"))
        if not em or not ep: continue
        LVD[r["name"]] = (s, 0.5 * (em + ep))
def norm(n):
    n = n.strip()
    n = re.sub(r"\s*\((Local Group Suspect 3|Wolf-Lundmark-Melotte)\)", "", n)
    n = n.replace("(I)", "I").replace("Segue I", "Segue 1").replace("Segue II", "Segue 2").replace("Segue 1I", "Segue 2")
    n = re.sub(r"^And ", "Andromeda ", n); n = n.replace("M32", "M 32").replace("Sagittarius dSph", "Sagittarius")
    return re.sub(r"\s+", " ", n).strip().lower()
LN = {norm(k): k for k in LVD}
def pairs_m12():
    out, un = [], []
    for r in csv.DictReader(open(os.path.join(DD, "mcconnachie2012_dsph.csv"))):
        s, e = fl(r["sigma*"]), fl(r["e_sigma*"])
        if not s or not e: continue
        k = LN.get(norm(r["Name"]))
        (out.append((k, s, e)) if k else un.append(r["Name"]))
    return out, un
def pairs_c13():
    out, un = [], []
    lines = [l.rstrip("\n") for l in open(os.path.join(DD, "collins2013_m31_dsph.tsv")) if l.strip() and not l.startswith("#")]
    hdr = lines[0].split("\t"); idx = {h.strip(): i for i, h in enumerate(hdr)}
    for l in lines[3:]:
        v = l.split("\t")
        if len(v) < len(hdr): continue
        s = fl(v[idx["sigV"]]); E, e = fl(v[idx["E_sigV"]]), fl(v[idx["e_sigV"]])
        if not s or s == 0 or E is None or e is None: continue
        k = LN.get(norm(v[idx["Gal"]]))
        (out.append((k, s, 0.5 * (E + e))) if k else un.append(v[idx["Gal"]].strip()))
    return out, un
def ml_extra(d, e):
    best = None; grid = np.concatenate([[0.0], np.geomspace(1e-3, 2.0, 2000)])
    LL = []
    for sx in grid:
        w = 1 / (e ** 2 + sx ** 2); mu = np.sum(w * d) / np.sum(w)
        LL.append(-0.5 * np.sum(w * (d - mu) ** 2 - np.log(w)))
    LL = np.array(LL); j = int(np.argmax(LL)); prof = 2 * (LL[j] - LL)
    def iv(th):
        ok = grid[prof <= th]; return float(ok.min()), float(ok.max())
    w = 1 / (e ** 2 + grid[j] ** 2); mu = float(np.sum(w * d) / np.sum(w))
    return dict(s_x=float(grid[j]), mu=mu, s68=iv(1.0), s95=iv(3.84), N=len(d))
P("CFG887  empirical sigma systematic floor from independent catalogues" + ("  [MUTATE: differences doubled]" if MUT else ""))
RES = dict(lane="CFG887", mutate=MUT)
sets = {}
for tag, (pr, un) in (("LVD-M12", pairs_m12()), ("LVD-C13", pairs_c13())):
    d = np.array([math.log(LVD[k][0] / s) for k, s, e in pr]) * (2 if MUT else 1)
    ee = np.array([math.hypot(LVD[k][1] / LVD[k][0], e / s) for k, s, e in pr])
    sets[tag] = (d, ee, [k for k, s, e in pr]); R = ml_extra(d, ee); RES[tag] = dict(R, unmatched=un)
    P(f"  {tag}: N {R['N']}  mean ln ratio {R['mu']:+.3f}  extra scatter s_x {R['s_x']:.3f} [68% {R['s68'][0]:.3f}-{R['s68'][1]:.3f}; 95% {R['s95'][0]:.3f}-{R['s95'][1]:.3f}]  unmatched: {', '.join(un) or 'none'}")
    big = sorted(zip(sets[tag][2], d, ee), key=lambda t: -abs(t[1]))[:5]
    P("      largest |d|: " + "; ".join(f"{k} {x:+.2f} (err {y:.2f})" for k, x, y in big))
dp = np.concatenate([sets[t][0] for t in sets]); ep_ = np.concatenate([sets[t][1] for t in sets]); Rp = ml_extra(dp, ep_); RES["pooled"] = Rp
rng = np.random.default_rng(887); bs = []
for _ in range(2000):
    i = rng.integers(0, len(dp), len(dp)); bs.append(ml_extra(dp[i], ep_[i])["s_x"])
RES["pooled"]["boot_s68"] = [float(np.percentile(bs, 16)), float(np.percentile(bs, 84))]
f_p, f_c, f_u = Rp["s_x"] / math.sqrt(2), Rp["s_x"], Rp["s95"][1] / math.sqrt(2)
P(f"  pooled: N {Rp['N']}  s_x {Rp['s_x']:.3f} [95% {Rp['s95'][0]:.3f}-{Rp['s95'][1]:.3f}; bootstrap 68% {RES['pooled']['boot_s68'][0]:.3f}-{RES['pooled']['boot_s68'][1]:.3f}]")
P(f"  floors: primary f = s_x/sqrt2 = {f_p:.3f};  conservative f_c = s_x = {f_c:.3f};  pessimistic (95% upper)/sqrt2 = {f_u:.3f}")
RES["floors"] = dict(primary=f_p, conservative=f_c, pessimistic=f_u)
# ---- CFG880's fit, exec'd unchanged up to its post-hoc block
src_path = os.path.join(LANES, "CFG880_clump_sigma_universality", "cfg880.py"); src = open(src_path).read()
cut = src.index('POST = os.environ.get("CFG880_POSTHOC"'); ns = dict(__file__=src_path, __name__="cfg880_lib")
os.environ.pop("CFG880_MUTATE", None); exec(compile(src[:cut], src_path, "exec"), ns)
R880 = json.load(open(os.path.join(LANES, "CFG880_clump_sigma_universality", "cfg880_results.json")))
RES["fits"] = {}
for foot, a0 in ns["A0"].items():
    A = ns["arrays"](ns["SAMP"], a0); RES["fits"][foot] = {}
    for tag, flo in (("floor 0 (K1)", 0.0), ("primary f", f_p), ("conservative f_c", f_c), ("pessimistic", f_u)):
        AF = dict(A); AF["em"] = np.sqrt(A["em"] ** 2 + (flo * A["s"]) ** 2); AF["ep"] = np.sqrt(A["ep"] ** 2 + (flo * A["s"]) ** 2)
        RF = ns["fit"](AF, a0); RES["fits"][foot][tag] = dict(floor=flo, s_hat=RF["s_hat"], s95=RF["s95"], cls=RF["cls"])
        P(f"  [{foot}] {tag:17s} floor {flo:.3f}: {ns['fmt'](RF)}")
    k1 = abs(RES["fits"][foot]["floor 0 (K1)"]["s_hat"] - R880[foot]["primary"]["s_hat"]) + sum(abs(a - b) for a, b in zip(RES["fits"][foot]["floor 0 (K1)"]["s95"], R880[foot]["primary"]["s95"]))
    RES["fits"][foot]["K1"] = k1; P(f"  [{foot}] K1 floor-0 vs CFG880 committed: |diff| {k1:.1e} -> {'PASS' if k1 < 1e-9 else 'FAIL'}")
def cls_of(foot):
    a, c = RES["fits"][foot]["primary f"]["cls"], RES["fits"][foot]["conservative f_c"]["cls"]
    return "CFG880 STANDS" if a == "NOT UNIVERSAL" and c == "NOT UNIVERSAL" else ("CFG880 FRAGILE" if a == "NOT UNIVERSAL" else "SYSTEMATICS-LIMITED")
order = ["CFG880 STANDS", "CFG880 FRAGILE", "SYSTEMATICS-LIMITED"]
cc, ca = cls_of("canonical"), cls_of("alt"); overall = cc if cc == ca else order[max(order.index(cc), order.index(ca))]
P(f"\n  CLASS (canonical {cc}; alt {ca}): {overall}")
if MUT:
    ok = (overall != "CFG880 STANDS") or (f_p < 0.15); RES["mutate_ok"] = ok; P(f"  MUTATE: s_x {Rp['s_x']:.3f} -> {'responds' if ok else 'FAILED'}")
RES["cls"] = overall
json.dump(RES, open(os.path.join(HERE, f"cfg887_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg887{SUF}.out"), "w").write("\n".join(OUT) + "\n")

# ---- POST-HOC diagnostic (added after the first run; not graded): catalogues often cite the same measurement, which makes d = 0 by
# construction and hides systematics. Count identical values and re-estimate s_x on the pairs that differ.
if not MUT:
    P("\n  POST-HOC diagnostic (disclosed): identical-value pairs")
    for tag in list(sets) + ["pooled"]:
        d, ee = (dp, ep_) if tag == "pooled" else sets[tag][:2]
        same = np.abs(d) < 1e-9; Rd = ml_extra(d[~same], ee[~same]) if (~same).sum() > 2 else None
        P(f"   {tag}: {int(same.sum())} of {len(d)} pairs identical; on the {int((~same).sum())} differing pairs s_x {Rd['s_x']:.3f} [95% {Rd['s95'][0]:.3f}-{Rd['s95'][1]:.3f}] -> floor/sqrt2 {Rd['s_x']/math.sqrt(2):.3f}, 95% upper/sqrt2 {Rd['s95'][1]/math.sqrt(2):.3f}")
        RES.setdefault("posthoc_identical", {})[tag] = dict(n_same=int(same.sum()), n=len(d), s_x_diff=Rd["s_x"], s95_diff=Rd["s95"])
    json.dump(RES, open(os.path.join(HERE, f"cfg887_results{SUF}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"cfg887{SUF}.out"), "w").write("\n".join(OUT) + "\n")
