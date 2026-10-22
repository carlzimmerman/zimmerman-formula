"""D8b -- is the per-galaxy HI dispersion a universal floor, or driven by SF / mass? Stilp+2013 (arXiv:1301.1989v2),
23 dwarfs, 200 pc beam. Criteria: FROZEN_CRITERIA.md (97ec7892fa), committed before this script.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -I d8b_sigma_universality.py   (D8B_MUTATE=1: sigma_m2 -> planted driven
sigma; K2 fails). sigma is footing-free; L* = sigma^2/a0 on both footings, never pooled. kappa = 1/2 FITTED."""
import os, sys, re, json, math, hashlib
import numpy as np
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__))
D8 = os.path.join(HERE, "..", "D8_Lstar_value")
MUT = os.environ.get("D8B_MUTATE") == "1"
SEED = 20261022
NPERM, NBOOT, NMC = 100_000, 10_000, 100_000
PC = 3.0856775814913673e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
A_PRIM, A_SEC = 0.05 / 4, 0.05 / 16
B_DRV = 1.0 / 3.0
SHA = {"stilp2013_table-derived-properties.tex": "4673d84985696d64a9786ffefed907ce4c85f7b7e7233ca04bf2bcd8b3e5bc54",
       "stilp2013_table-sample.tex": "835fef56f5d4018e997857f3b251874fd431ff9df9b1f24d58b54c1451e9be23",
       "stilp2013_table-correlations.tex": "01c95604dc5cf6762f611c01ebd43bd29c91d925c7eb02548cddbb34a9174046"}
SHA_SIG = "155d780cf9064d904529b04924d431519b065933b6844fdc34fce220dfdd5ac1"
OUT, CH = [], []
RES = {"lane": "D8b_sigma_universality", "mutate": MUT, "criteria_commit": "97ec7892fa", "seed": SEED}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(i, ok, v, t, w): CH.append(dict(id=i, ok=bool(ok), value=v, threshold=t, what=w)); P(f"{i} {'PASS' if ok else 'FAIL'} {v} {t}   # {w}")
def norm(n): return re.sub(r"\s+", " ", re.sub(r"[~$]|\\,", " ", n)).strip().lower()
def rows_of(fn):
    raw = open(fn, "rb").read(); txt = raw.decode()
    body = txt.split("\\startdata")[1].split("\\enddata")[0]
    out = []
    for l in body.split("\\\\"):
        l = re.sub(r"\\tablenotemark\{[^}]*\}", "", l).strip()
        if l: out.append([x.strip() for x in l.split("&")])
    return hashlib.sha256(raw).hexdigest(), out
def num(s):
    s = s.strip()
    if s in ("", "\\nodata", "...", "--") or "<" in s: return np.nan
    return float(re.findall(r"-?[\d.]+", s)[0])

# ---------- data ----------
h_sig, rs = rows_of(os.path.join(D8, "stilp2013_table-measurements.tex"))
sig = {norm(r[0]): dict(m2=float(r[1]), cen=float(re.findall(r"[\d.]+", r[2])[0]), ecen=float(re.findall(r"[\d.]+", r[2])[1])) for r in rs}
h_der, rd = rows_of(os.path.join(HERE, "stilp2013_table-derived-properties.tex"))
h_smp, rsm = rows_of(os.path.join(HERE, "stilp2013_table-sample.tex"))
h_cor, rc = rows_of(os.path.join(HERE, "stilp2013_table-correlations.tex"))
shas = {"stilp2013_table-derived-properties.tex": h_der, "stilp2013_table-sample.tex": h_smp, "stilp2013_table-correlations.tex": h_cor}
ok1 = h_sig == SHA_SIG and all(shas[k] == SHA[k] for k in SHA)
check("K1", ok1, f"sigma {h_sig[:10]}, der {h_der[:10]}, smp {h_smp[:10]}, cor {h_cor[:10]}", "all sha256 match", "table integrity")
names = list(sig)
der = {norm(r[0]): dict(Mb=num(r[1]), MHI=num(r[2]), Mst=num(r[3]), SFR=num(r[4]), SFR_MHI=num(r[5]), SSFR=num(r[6]), SHI=num(r[7])) for r in rd}
smp = {norm(r[0]): dict(w20=num(r[9])) for r in rsm}
# X in log10 (masses already log10; others logged); w20 logged
X = {"SSFR": lambda n: math.log10(der[n]["SSFR"]), "Mb": lambda n: der[n]["Mb"],
     "SFR": lambda n: math.log10(der[n]["SFR"]), "SFR_MHI": lambda n: math.log10(der[n]["SFR_MHI"]),
     "MHI": lambda n: der[n]["MHI"], "Mst": lambda n: der[n]["Mst"], "SHI": lambda n: math.log10(der[n]["SHI"]),
     "w20": lambda n: math.log10(smp[n]["w20"])}
PRIMARY = ("SSFR", "Mb")
m2 = np.array([sig[n]["m2"] for n in names]); cen = np.array([sig[n]["cen"] for n in names]); ecen = np.array([sig[n]["ecen"] for n in names])
em2 = m2 * ecen / cen   # frozen CONDITIONAL error transfer
logSSFR = np.array([X["SSFR"](n) for n in names])
if MUT:  # planted driven sigma replaces sigma_m2
    m2 = np.round(9.3 * (10 ** (logSSFR - np.median(logSSFR))) ** B_DRV, 1)
d8 = json.load(open(os.path.join(D8, "d8_stilp2013_results.json")))
d8m2 = {norm(r["name"]): r["s_m2"] for r in d8["rows"]}; d8cen = {norm(r["name"]): r["s_cen"] for r in d8["rows"]}
match = len(names) == 23 and all(n in der and n in smp for n in names) and len(der) == 23 and len(smp) == 23
same = all(abs(d8m2[n] - m2[i]) < 1e-9 and abs(d8cen[n] - cen[i]) < 1e-9 for i, n in enumerate(names))
check("K2", match and same, f"joined {sum(n in der and n in smp for n in names)}/23, sigma == D8 rows: {same}", "23/23 and identical", "frozen name join + D8 consistency")

rng = np.random.default_rng(SEED)
def rank(a): return stats.rankdata(a)
def spearman_perm(x, y, nperm, rng):
    rx, ry = rank(x), rank(y); rx = (rx - rx.mean()) / np.sqrt(((rx - rx.mean()) ** 2).sum()); ry = (ry - ry.mean()) / np.sqrt(((ry - ry.mean()) ** 2).sum())
    rho = float(rx @ ry); null = np.empty(nperm)
    for s in range(0, nperm, 10_000):
        k = min(10_000, nperm - s); idx = np.argsort(rng.random((k, len(ry))), axis=1)
        with np.errstate(all="ignore"): null[s:s + k] = (ry[idx] * rx).sum(1)
    assert np.all(np.isfinite(null))
    return rho, null
def crit_rho(null, a): return float(np.quantile(np.abs(null), 1 - a))
def rho80(n, a): return float(np.tanh((stats.norm.ppf(1 - a / 2) + stats.norm.ppf(0.8)) * math.sqrt(1.06 / (n - 3))))

def test(y, xname, a):
    x = np.array([X[xname](n) for n in names]); ok = np.isfinite(x); x, yy = x[ok], y[ok]; n = len(x)
    rho, null = spearman_perm(x, yy, NPERM, rng); p = float((np.sum(np.abs(null) >= abs(rho) - 1e-12) + 1) / (NPERM + 1))
    bi = rng.integers(0, n, (NBOOT, n)); br = np.array([stats.spearmanr(x[b], yy[b])[0] for b in bi])
    ly = np.log10(yy); sl = float(np.polyfit(x, ly, 1)[0]); bs = np.array([np.polyfit(x[b], ly[b], 1)[0] if np.ptp(x[b]) > 0 else np.nan for b in bi])
    ts = stats.theilslopes(ly, x)
    return dict(n=n, rho=rho, p_perm=p, rho_ci68=[float(np.nanpercentile(br, 16)), float(np.nanpercentile(br, 84))],
                rho_ci95=[float(np.nanpercentile(br, 2.5)), float(np.nanpercentile(br, 97.5))], slope_ols=sl,
                slope_ci95=[float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))], slope_theilsen=float(ts[0]),
                rho_crit=crit_rho(null, a), rho_80=rho80(n, a), alpha=a, significant=bool(p < a))

# ---------- T1 ----------
P("T1 tracking (Spearman, 1e5 permutations, 1e4 bootstrap; log10 X; slope = d log10 sigma / d log10 X)")
T1 = {}
for col, y in (("sigma_m2", m2), ("sigma_cen", cen)):
    T1[col] = {}
    for xn in list(X):
        a = A_PRIM if xn in PRIMARY else A_SEC; r = test(y, xn, a); T1[col][xn] = r
        P(f"  {col:9s} vs {xn:7s} [{'PRIMARY' if xn in PRIMARY else 'second.'}] n={r['n']} rho={r['rho']:+.3f} p={r['p_perm']:.4f} "
          f"(alpha {a:.4f}, |rho|crit {r['rho_crit']:.3f}, rho80 {r['rho_80']:.3f}) CI95 [{r['rho_ci95'][0]:+.2f},{r['rho_ci95'][1]:+.2f}] "
          f"slope {r['slope_ols']:+.3f} CI95 [{r['slope_ci95'][0]:+.3f},{r['slope_ci95'][1]:+.3f}] TS {r['slope_theilsen']:+.3f}{'  SIGNIFICANT' if r['significant'] else ''}")
RES["T1"] = T1
sig_prim = {(c, x): T1[c][x]["significant"] for c in T1 for x in PRIMARY}
b_hi = T1["sigma_m2"]["SSFR"]["slope_ci95"][1]
if any(sig_prim[("sigma_m2", x)] for x in PRIMARY):
    crisp = [x for x in PRIMARY if sig_prim[("sigma_m2", x)] and sig_prim[("sigma_cen", x)] and np.sign(T1["sigma_m2"][x]["rho"]) == np.sign(T1["sigma_cen"][x]["rho"])]
    v1 = "DRIVEN" + (" (CRISP: both columns, " + ",".join(crisp) + ")" if crisp else " (sigma_m2 only)")
elif b_hi < B_DRV: v1 = "FLOOR FAVOURED"
else: v1 = "UNDECIDED (low power)"
P(f"T1 VERDICT: {v1}   (slope sigma_m2 vs Sigma_SFR 95% upper {b_hi:+.3f} vs driven 1/3; any primary sigma_cen significant: "
  f"{any(sig_prim[('sigma_cen', x)] for x in PRIMARY)})")
RES["T1_verdict"] = v1
sec_sig = [f"{c} vs {x}" for c in T1 for x in X if x not in PRIMARY and T1[c][x]["significant"]]
sec_nom = [f"{c} vs {x} (p={T1[c][x]['p_perm']:.4f}, rho={T1[c][x]['rho']:+.3f})" for c in T1 for x in X if T1[c][x]["p_perm"] < 0.05]
P(f"secondary significant at Bonferroni-16: {sec_sig or 'none'}; nominal p<0.05 (any): {sec_nom or 'none'}")
RES["secondary_significant"] = sec_sig; RES["nominal_p05"] = sec_nom

# ---------- K3 planted controls ----------
x0 = logSSFR; xr = x0 - np.median(x0)
_, null_c = spearman_perm(x0, rng.random(23), 20_000, rng); rc = crit_rho(null_c, A_PRIM)
det = 0
for _ in range(200):
    yp = 9.3 * (10 ** xr) ** B_DRV + rng.normal(0, em2); det += abs(stats.spearmanr(x0, yp)[0]) > rc
fp = 0
for _ in range(2000):
    yn = 9.3 + rng.normal(0, em2); fp += abs(stats.spearmanr(x0, yn)[0]) > rc
pw, fpr = det / 200, fp / 2000
check("K3", pw >= 0.8 and abs(fpr - A_PRIM) <= 0.01, f"power(b=1/3) {pw:.3f}, false-pos {fpr:.4f}", ">= 0.80; 0.0125 +- 0.01", "planted driven / null controls (Sigma_SFR)")
RES["K3"] = dict(power_driven=pw, false_positive=fpr, rho_crit_planted=rc)

# ---------- K4 reproduce Stilp's own Spearman for sigma_central ----------
cmap = {"SFR / M": "SFR_MHI", "w_{20}": "w20", "baryon,tot": "Mb", "M$_\\star": "Mst", "M$_\\mathrm{HI}$": "MHI", "sfrsd": "SSFR", "Sigma_\\mathrm{HI}": "SHI"}
pub = {}
for r in rows_of(os.path.join(HERE, "stilp2013_table-correlations.tex"))[1]:
    lab = r[0]; key = None
    for k, v in cmap.items():
        if k in lab: key = v; break
    if key is None and lab.strip() == "SFR": key = "SFR"
    if key: pub[key] = float(re.sub(r"\\textbf\{|\}", "", r[1]))
dr = {k: round(T1["sigma_cen"][k]["rho"] - v, 4) for k, v in pub.items()}
check("K4", len(pub) == 8 and max(abs(v) for v in dr.values()) <= 0.05, f"{len(pub)} pairs, max |drho| {max(abs(v) for v in dr.values()):.4f}", "8 pairs, <= 0.05", "reproduce Stilp+13 Table sigma_central r_S")
RES["K4"] = dict(published=pub, delta=dr)

# ---------- T2 noise-only ----------
P("T2 noise-only spread (H0: one true sigma + measurement error)")
T2 = {}
for col, y, e, lab in (("sigma_cen", cen, ecen, "table errors"), ("sigma_m2", m2, em2, "CONDITIONAL: fractional error transfer")):
    w = 1 / e ** 2; mu = float((w * y).sum() / w.sum()); chi2 = float((((y - mu) / e) ** 2).sum()); dof = len(y) - 1
    p_chi = float(stats.chi2.sf(chi2, dof))
    L = (y / np.median(y)) ** 2; ratio = float(np.percentile(L, 84) / np.percentile(L, 16))
    sims = mu + rng.normal(0, 1, (NMC, len(y))) * e
    Ls = sims ** 2; rsim = np.percentile(Ls, 84, axis=1) / np.percentile(Ls, 16, axis=1)
    p_mc = float(np.mean(rsim >= ratio)); chisim = (((sims - (sims * w).sum(1, keepdims=True) / w.sum()) / e) ** 2).sum(1)
    # ML intrinsic scatter
    def nll(s): v = e ** 2 + s ** 2; m = (y / v).sum() / (1 / v).sum(); return 0.5 * ((y - m) ** 2 / v + np.log(v)).sum()
    sg = np.linspace(0, 4, 4001); si = float(sg[np.argmin([nll(s) for s in sg])])
    nc = p_mc >= 0.05 and p_chi >= 0.05
    T2[col] = dict(errors=lab, mean_w=mu, chi2=chi2, dof=dof, p_chi2=p_chi, ratio_84_16=ratio, mc_ratio_median=float(np.median(rsim)),
                   mc_ratio_p95=float(np.percentile(rsim, 95)), p_mc=p_mc, sigma_int_kms=si, sigma_int_frac=si / mu,
                   mc_chi2_mean=float(chisim.mean()), verdict="NOISE-CONSISTENT" if nc else "INTRINSIC SCATTER")
    P(f"  {col:9s} [{lab}] weighted mean {mu:.2f} km/s; chi2 {chi2:.1f}/{dof} (p {p_chi:.2e}); L 84/16 obs {ratio:.3f} vs noise-only median "
      f"{np.median(rsim):.3f}, 95% {np.percentile(rsim, 95):.3f} (p {p_mc:.4f}); sigma_int {si:.2f} km/s ({si / mu * 100:.1f}%) -> {T2[col]['verdict']}")
RES["T2"] = T2
check("K5", abs(T2["sigma_cen"]["mc_chi2_mean"] / 22 - 1) <= 0.02, f"{T2['sigma_cen']['mc_chi2_mean']:.3f}", "22 +- 2%", "noise MC reproduces chi2 mean n-1")

# ---------- envelope L* on both footings ----------
floor = {f: json.load(open(os.path.join(D8, "d8_lstar_value_results.json")))["part2"][f]["L95_fine_pc"] for f in A0}
def Lpc(s, a0): return (s * 1e3) ** 2 / a0 / PC
ENV = {}
for col, y, e in (("sigma_m2", m2, em2), ("sigma_cen", cen, ecen)):
    ENV[col] = {}
    for lab, s in (("median", float(np.median(y))), ("p05", float(np.percentile(y, 5))), ("min", float(y.min())), ("min_minus_2err", float((y - 2 * e).min()))):
        ENV[col][lab] = dict(sigma_kms=s, **{f: Lpc(s, a0) for f, a0 in A0.items()})
    P(f"  envelope {col:9s}: " + "; ".join(f"{k} {v['sigma_kms']:.2f} km/s -> L* {v['canonical']:.1f}/{v['alt']:.1f} pc" for k, v in ENV[col].items())
      + f"   (CFG820 floor {floor['canonical']:.2f}/{floor['alt']:.2f} pc; canonical/alt)")
RES["envelope"] = ENV; RES["cfg820_floor_pc"] = floor
RES["checks"] = CH; n = sum(c["ok"] for c in CH)
P(f"\nD8B_SIGMA_UNIVERSALITY COMPLETE: {n}/{len(CH)} checks PASS.")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"d8b_sigma_universality_results{sfx}.json"), "w"), indent=1)
open(os.path.join(HERE, f"d8b_sigma_universality{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n == len(CH) else 1)
