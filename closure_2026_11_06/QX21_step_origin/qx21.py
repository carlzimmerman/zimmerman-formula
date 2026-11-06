"""QX21: is QX20's hot/cold step physics (type-keyed) or a method artefact? Criteria: FROZEN_CRITERIA.md.
T1 KiDS early/late lensing log-ratio on CFG61's K1 bins; T2 dSph plain-law offsets vs SPARC anchor; T3 read LF1/RF3.
    python3 qx21.py            -> qx21.json / qx21.out
    python3 qx21.py --mutate   -> qx21_MUTATE.json / .out  (M2 Newton on T2; M1 is reported in both)
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, re, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
MUT = "--mutate" in sys.argv; TAG = "qx21_MUTATE" if MUT else "qx21"
OUT = []
def P(s=""): OUT.append(s); print(s)

# ---------------- T1 data (CFG61's loader, verbatim logic)
B21 = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
d = [np.loadtxt(os.path.join(B21, f"Fig-8_RAR-KiDS-isolated_Colorbin_{i}.txt")) for i in (1, 2)]
g = d[0][:, 0]
L = d[0][:, 1] / d[0][:, 4]; E = d[1][:, 1] / d[1][:, 4]
cv = np.loadtxt(os.path.join(B21, "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt"))
C30 = (cv[:, 4] / cv[:, 6]).reshape(2, 2, 15, 15).transpose(0, 2, 1, 3).reshape(30, 30)

# KA1: CFG61 C1 split chi2 on all 15 bins (u-r) = 119.9 +- 0.5
Cll, Cee, Cel, Cle = C30[:15, :15], C30[15:, 15:], C30[15:, :15], C30[:15, 15:]
Dall = E - L; chi_all = float(Dall @ np.linalg.solve(Cee + Cll - Cel - Cle, Dall))
KA1 = abs(chi_all - 119.9) <= 0.5

K1 = np.arange(8, 15)
def dstat(Lv, Ev, idx=K1):
    """GLS mean of d_i = log10(E_i/L_i) with linearised covariance."""
    x = np.concatenate([Lv, Ev]); n = len(idx)
    J = np.zeros((n, 30))
    for k, i in enumerate(idx):
        J[k, i] = -1.0 / Lv[i]; J[k, 15 + i] = 1.0 / Ev[i]
    Cd = J @ C30 @ J.T / np.log(10) ** 2
    dv = np.log10(Ev[idx] / Lv[idx]); w = np.linalg.solve(Cd, np.ones(n))
    Dm = float(w @ dv / w.sum()); s = float(1 / np.sqrt(w.sum()))
    return Dm, s, dv, Cd

D, s_stat, dv, Cd = dstat(L, E)
# D_law from CFG61's printed lens-by-lens law (L) columns on K1, canonical
txt = open(os.path.join(REPO, "campaign_fresh_gravity", "CFG61_kids_colour_split.out")).read()
rows = re.findall(r"K1 g_bar ([0-9.e+-]+): R_med late [0-9.]+ early [0-9.]+ Mpc \| late +([0-9.]+) \(L +([0-9.]+), S +[0-9.]+\) \| early +([0-9.]+) \(L +([0-9.]+), S", txt)
assert len(rows) == 7, len(rows)
Llaw = np.array([float(r[2]) for r in rows]); Elaw = np.array([float(r[4]) for r in rows])
d_law = np.log10(Elaw / Llaw); D_law = float(np.mean(d_law))
chk_data = max(abs(float(r[1]) / L[8 + k] - 1) for k, r in enumerate(rows)), max(abs(float(r[3]) / E[8 + k] - 1) for k, r in enumerate(rows))
s_sys = 0.05; s_tot = float(np.hypot(s_stat, s_sys)); S = 0.35
Dx = D - D_law
t1 = "STEP SEEN" if (Dx > 0 and Dx / s_tot >= 3) else ("NO STEP" if abs(Dx) / s_tot < 2 else "weak")
size = "same size" if abs(Dx - S) <= 2 * s_tot else ("smaller" if Dx < S - 2 * s_tot else "larger")
# M1: all 128 per-bin swaps
sw = []
for signs in itertools.product((1, -1), repeat=7):
    Ls, Es = L.copy(), E.copy()
    for k, sg in zip(K1, signs):
        if sg < 0: Ls[k], Es[k] = E[k], L[k]
    sw.append(dstat(Ls, Es)[0])
sw = np.array(sw); p95 = float(np.percentile(sw, 95)); M1 = D > p95
frac_ge = float(np.mean(sw >= D))

P("QX21 step origin. kappa = 1/2 FITTED; not theory closed." + ("  [MUTATE: M2 Newton on T2]" if MUT else ""))
P(f"KA1 CFG61 C1 u-r split chi2 (15 bins) {chi_all:.2f} vs 119.9 +- 0.5 -> {'PASS' if KA1 else 'FAIL'}; K1 data vs CFG61 print max rel {max(chk_data):.1e}")
P("T1 KiDS B21 early(u-r>=2.5)/late, K1 bins 8-14:")
for k, i in enumerate(K1):
    P(f"   g_bar {g[i]:.3e}: E {E[i]:7.2f} L {L[i]:7.2f}  d {dv[k]:+.3f} +- {np.sqrt(Cd[k,k]):.3f}   law d {d_law[k]:+.4f}")
P(f"   D = {D:+.3f} +- {s_stat:.3f} (stat) +- {s_sys:.2f} (sys) = +- {s_tot:.3f};  D_law {D_law:+.4f};  D - D_law = {Dx:+.3f} ({Dx/s_tot:+.2f} sigma)")
P(f"   -> T1 {t1}; size vs QX20 g_N step 0.35: {size} (diff {Dx - S:+.3f}, 2 sigma {2*s_tot:.3f})")
P(f"   M1 128 swaps: 95th pct {p95:+.3f}, frac >= D {frac_ge:.3f} -> {'BITES (T1 has power)' if M1 else 'NO POWER'}")

# ---------------- T2 dSphs
LW = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "LW1_law_scorecard", "lw1_dwarfs.json")))
Q20 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX20_failure_ladder", "qx20.json")))
rng = np.random.default_rng(21)
T2 = {}; KA2 = None; M2 = {}
import csv
X1 = {(r["footing"], r["name"]): float(r["Delta[Newton]"]) for r in
      csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount", "x1_per_system.csv")))}
for f in ("canonical", "alt"):
    ps = LW["footings"][f]["per_system"]; sparc = Q20[f]["sparc_mean"]
    T2[f] = {}
    for cls in ("MW classical", "bright M31", "MW ultra-faint", "M31 others", "LG field"):
        names = [n for n, x in ps.items() if x["cls"] == cls]
        v = np.array([ps[n]["plain"] for n in names])
        if MUT:   # M2 Newton: g_law -> g_N, offsets log g_obs/g_N from X1's per-system Newton column (same systems)
            vN = np.array([X1[(f, n)] for n in names])
            M2.setdefault(f, {})[cls] = float(np.median(vN) - np.median(v))
            v = vN
        b = np.array([np.median(rng.choice(v, len(v))) for _ in range(10000)])
        med = float(np.median(v)); lo, hi = float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
        present = (med - sparc >= 0.15) and (lo > sparc); absent = lo <= sparc <= hi
        T2[f][cls] = dict(N=int(len(v)), median=med, ci95=[lo, hi], minus_sparc=med - sparc,
                          label=("present" if present else ("absent" if absent else "weak")),
                          graded=cls in ("MW classical", "bright M31"))
    if f == "canonical": KA2 = abs(T2[f]["MW classical"]["median"] - 0.2445) <= 1e-4
for f in ("canonical", "alt"):
    P(f"T2 [{f}] dSph plain-law offsets vs SPARC anchor {Q20[f]['sparc_mean']:+.3f}:")
    for cls, r in T2[f].items():
        P(f"   {cls:15s} N {r['N']:3d} median {r['median']:+.3f} [{r['ci95'][0]:+.3f},{r['ci95'][1]:+.3f}] minus SPARC {r['minus_sparc']:+.3f} -> {r['label']}{'' if r['graded'] else ' (reported)'}")
P(f"KA2 LW1 MW-classical plain median canonical {T2['canonical']['MW classical']['median']:.4f} vs 0.2445 -> {'PASS' if KA2 else 'FAIL'}")
t2 = {f: ("present" if all(T2[f][c]["label"] == "present" for c in ("MW classical", "bright M31")) else
          ("absent" if all(T2[f][c]["label"] == "absent" for c in ("MW classical", "bright M31")) else "mixed")) for f in T2}
# dSph shuffle: relabel graded dSph + SPARC-anchor null (sign-flip of offsets about SPARC mean)
sh = {}
for f in ("canonical", "alt"):
    v = np.array([x["plain"] for x in LW["footings"][f]["per_system"].values() if x["cls"] in ("MW classical", "bright M31")])
    c = Q20[f]["sparc_mean"]; obs = np.median(v) - c
    null = [np.median(c + (v - c) * rng.choice((1, -1), len(v))) - c for _ in range(10000)]
    sh[f] = float(np.mean(np.array(null) >= obs))
P(f"T2 shuffle (sign-flip about SPARC anchor, graded dSphs): frac >= obs canonical {sh['canonical']:.4f}, alt {sh['alt']:.4f}")

# ---------------- T3 read
T3 = dict(LF1="KiDS shear on eRASS1 clusters gives ~0.12 dex MORE mass at fixed gas than X-COP hydrostatic (LF1 22272b3b32)",
          RF3="A2142 lensing agrees with hydrostatic", sign="lensing >= hydrostatic", label="METHOD-SIGN EXCLUDED")
P(f"T3 (read): {T3['LF1']}; {T3['RF3']} -> {T3['label']}")

if t1 == "STEP SEEN" and T3["label"] == "METHOD-SIGN EXCLUDED" and M1:
    lab = "STEP REAL (type-keyed)"
elif t1 == "NO STEP" and T3["label"] == "METHOD POSSIBLE":
    lab = "STEP METHOD"
else:
    lab = "NO VERDICT"
P(f"LABEL: {lab}; T2 key: canonical {t2['canonical']}, alt {t2['alt']} (pressure-supported cold dSphs)")
res = dict(tag=TAG, criteria="55374ee57a", KA1=dict(chi2=chi_all, ok=bool(KA1)), T1=dict(D=D, s_stat=s_stat, s_sys=s_sys, s_tot=s_tot,
           D_law=D_law, Dx=Dx, d=dv.tolist(), d_law=d_law.tolist(), label=t1, size=size, M1_p95=p95, M1_frac_ge=frac_ge, M1_bites=bool(M1)),
           T2=T2, T2_label=t2, T2_shuffle=sh, KA2=bool(KA2), T3=T3, label=lab)
json.dump(res, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
