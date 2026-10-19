"""CFG829 -- does KiDS isolated-galaxy lensing show the dwarfs' +0.44 dex excess at the dwarfs' own g_bar?
Criteria: FROZEN_CRITERIA.md (b941b73ce).  Data: Brouwer+21 (B21) public ESD files.  Run: python3 cfg829.py (CFG829_MUTATE=1).
kappa = 1/2 FITTED; not theory closed."""
import os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
B = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
MUT = os.environ.get("CFG829_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G_pc, PCm = 4.52e-30, 3.086e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; A_DW = 10 ** 0.44
nu_e = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
nu_s = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-15)))
def load(esd, cov, binmin=None):
    d = np.loadtxt(os.path.join(B, esd)); gb, esdt, bias = d[:, 0], d[:, 1], d[:, 4]
    go = 4 * G_pc * esdt / bias * PCm * (2.75 if MUT else 1.0)
    c = np.loadtxt(os.path.join(B, cov)); n = len(gb); C = np.zeros((n, n))
    sel = c if binmin is None else c[(np.isclose(c[:, 0], binmin)) & (np.isclose(c[:, 1], binmin))]
    def idx(x):                                            # ESD files print g_bar to 5 digits; covmatrix to full precision
        k = int(np.argmin(np.abs(gb / x - 1))); return k if abs(gb[k] / x - 1) < 1e-3 else None
    for row in sel:
        i, j = idx(row[2]), idx(row[3])
        if i is not None and j is not None: C[i, j] = row[4] / row[6]
    C *= (4 * G_pc * PCm) ** 2 * (2.75 ** 2 if MUT else 1.0)
    return gb, go, C
SETS = {"blue (u-r<2.5)": ("Fig-8_RAR-KiDS-isolated_Colorbin_1.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0),
        "red (u-r>2.5)": ("Fig-8_RAR-KiDS-isolated_Colorbin_2.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5),
        "all isolated": ("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt", "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", None),
        "isolated dwarfs": ("Fig-10_RAR-KiDS-isolated-dwarfs_Nobins.txt", "Fig-10_RAR-KiDS-isolated-dwarfs_covmatrix.txt", None)}
W = (10 ** -13.3, 10 ** -11.9); WC = (10 ** -11.9, 10 ** -10.9)
def amp(gb, go, C, gl, win):
    m = (gb >= win[0]) & (gb < win[1])
    if m.sum() < 2: return None
    Ci = np.linalg.inv(C[np.ix_(m, m)]); a = gl[m] @ Ci @ gl[m]
    A = float(gl[m] @ Ci @ go[m] / a); s = float(a ** -0.5)
    r = go[m] - A * gl[m]; chi2 = float(r @ Ci @ r)
    return dict(A=A, sA=s, n=int(m.sum()), chi2=chi2, gbar=gb[m].tolist(), ratio=(go[m] / gl[m]).tolist())
P("CFG829  KiDS isolated lensing at the dwarfs' g_bar (1e-13.3 .. 1e-11.9)" + ("  [MUTATE g_obs x2.75]" if MUT else ""))
RES = dict(lane="CFG829", mutate=MUT, window=W, calib=WC, A_dwarf=A_DW)
for foot in ("canonical", "alt"):
    for kn, nu in (("nu_e", nu_e), ("nu_simple", nu_s)):
        if foot == "alt" and kn == "nu_simple": continue
        P(f"\n  [{foot} | {kn}]")
        for name, (f, c, bm) in SETS.items():
            gb, go, C = load(f, c, bm); gl = gb * nu(gb / A0[foot])
            a, ac = amp(gb, go, C, gl, W), amp(gb, go, C, gl, WC)
            if a is None: P(f"    {name:16s} NOT DIAGNOSTIC (<2 points in window)"); continue
            if name.startswith("blue") and foot == "canonical" and kn == "nu_e":
                holds = abs(a["A"] - 1) < 2 * a["sA"] and (A_DW - a["A"]) >= 3 * a["sA"]
                shape = a["A"] >= 2.0 and (a["A"] - 1) >= 3 * a["sA"]
                RES["cls"] = "LAW HOLDS AT LOW g" if holds else ("LAW-SHAPE" if shape else "INTERMEDIATE")
                RES["k1"] = ac
            RES[f"{foot}|{kn}|{name}"] = dict(window=a, calib=ac)
            cal = f"calib A {ac['A']:.2f}+-{ac['sA']:.2f} ({ac['n']} pts)" if ac else "calib n/a"
            P(f"    {name:16s} A {a['A']:.3f} +- {a['sA']:.3f}  (dex {math.log10(max(a['A'], 1e-3)):+.3f}; {a['n']} pts, chi2 {a['chi2']:.1f})  "
              f"(A-1)/sA {(a['A'] - 1) / a['sA']:+.1f}  (2.75-A)/sA {(A_DW - a['A']) / a['sA']:+.1f}  | {cal}")
            if name.startswith("blue") and foot == "canonical" and kn == "nu_e":
                P("      per point g_bar: g_obs/g_law = " + ", ".join(f"{g:.1e}: {r:.2f}" for g, r in zip(a["gbar"], a["ratio"])))
k1 = RES.get("k1")
if k1 and not MUT:
    ok = abs(math.log10(max(k1["A"], 1e-3)) - 0.04) <= 3 * k1["sA"] / (k1["A"] * math.log(10))
    P(f"\n  K1 blue calibration window A {k1['A']:.2f} +- {k1['sA']:.2f} vs SPARC +0.04 dex -> {'PASS' if ok else 'FAIL'}")
P(f"\n  CLASS (blue lenses, nu_e, canonical): {RES.get('cls')}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg829_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg829{sfx}.out"), "w").write("\n".join(OUT) + "\n")
