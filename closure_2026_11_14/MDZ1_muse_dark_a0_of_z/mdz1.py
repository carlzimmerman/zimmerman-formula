"""MDZ1: the law's a0(z) = (c/2) sqrt(G rho_DE(z)) against MUSE-DARK III's measured a0(z) (arXiv:2604.22613v1)
and Escala's BTFR reading (arXiv:2608.10073). TEST lane; adopts nothing. Criteria: FROZEN_CRITERIA.md (committed alone).

usage: python3 -I -B mdz1.py <lane_dir> <inputs_csv> <mode>     mode in {canonical, alt, MUT, NULL}
"""
import csv, hashlib, itertools, json, math, os, sys

import numpy as np
from scipy import optimize, stats
from scipy.special import ndtri_exp

CSV_SHA = "3e6f0bb072985e0eecd81105f12730d5ff25e4719dc256700aa20c668ca26a3a"
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
C_SI, MPC_M = 299792458.0, 3.0856775814913673e22
LN10 = math.log(10.0)

lane, csv_path, MODE = sys.argv[1], sys.argv[2], sys.argv[3]
assert MODE in ("canonical", "alt", "MUT", "NULL"), MODE
raw = open(csv_path, "rb").read()
sha = hashlib.sha256(raw).hexdigest()
if sha != CSV_SHA:
    sys.exit(f"inputs CSV sha256 {sha} != frozen {CSV_SHA}")
IN = {r["key"]: r["value"] for r in csv.DictReader(open(csv_path, newline=""))}
num = lambda k: float(IN[k])
vec = lambda k: [float(x) for x in IN[k].split("|")]

# ------------------------------------------------------------------ inputs
Z = np.array([num(f"mud_bin{i}_z") for i in range(1, 5)])
A = np.array([num(f"mud_bin{i}_a0") for i in range(1, 5)])
ERR = np.array([num(f"mud_bin{i}_err") for i in range(1, 5)])
TRANS = np.array([0.0, 0.005e-10, 0.005e-10, 0.0])           # pixel-read middle bins
FIG6 = {0.0: np.zeros(4), 0.2: np.log10(np.array(vec("mud_fig6_p020")) / np.array(vec("mud_fig6_fid"))),
        0.45: np.log10(np.array(vec("mud_fig6_p045")) / np.array(vec("mud_fig6_fid")))}
G_a00, G_a00_s = num("mud_G_a00"), num("mud_G_a00_95") / 1.96
G_a1, G_a1_s = num("mud_G_a1"), num("mud_G_a1_95") / 1.96
GLOBALS = {"Eq4_DC14": (num("mud_G_a00"), num("mud_G_a00_95") / 1.96, num("mud_G_a1"), num("mud_G_a1_95") / 1.96),
           "Eq9_best_profile": (num("mud_GD_a00"), num("mud_GD_a00_95") / 1.96, num("mud_GD_a1"), num("mud_GD_a1_95") / 1.96),
           "Eq14_MOND": (num("mud_GM_a00"), num("mud_GM_a00_95") / 1.96, num("mud_GM_a1"), num("mud_GM_a1_95") / 1.96),
           "AppE_MOND_regression_1sig": (num("mud_GMreg_a00"), 0.45e-10, num("mud_GMreg_a1"), num("mud_GMreg_a1_err"))}
ESC_Z = np.array([num("esc_z1"), num("esc_z2"), num("esc_z3")])
ESC_D = np.array([num("esc_dZP1"), num("esc_dZP2"), num("esc_dZP3")])
ESC_S = np.array([num("esc_dZP1_err"), num("esc_dZP2_err"), num("esc_dZP3_err")])
CPL = {"Pan": tuple(vec("rec_CPL_Pan")), "DES5": tuple(vec("rec_CPL_DES5")), "Uni": tuple(vec("rec_CPL_Uni"))}

# ------------------------------------------------------------------ law
def f_of(case, z):
    z = np.asarray(z, float)
    if case == "L":
        return np.ones_like(z)
    if case == "H":
        return np.sqrt(0.315 * (1 + z) ** 3 + 0.685)
    w0, wa = CPL[case[2:]]
    F = (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))
    if case[0] == "D":
        return np.sqrt(F)
    return np.sqrt((w0 + wa * z / (1 + z)) * F / w0)


def g_simple(gb, a0):
    return 0.5 * (gb + np.sqrt(gb * gb + 4 * a0 * gb))


def g_mcg(gb, a0):
    return gb / (-np.expm1(-np.sqrt(gb / a0)))


_cif = {}
def C_IF(lo, hi, a0):
    key = (round(lo, 6), round(hi, 6), a0)
    if key not in _cif:
        gb = 10 ** np.linspace(lo, hi, 201)
        y = np.log10(g_simple(gb, a0))
        res = optimize.minimize_scalar(lambda la: float(np.sum((np.log10(g_mcg(gb, 10 ** la)) - y) ** 2)),
                                       bounds=(math.log10(a0) - 1, math.log10(a0) + 1), method="bounded",
                                       options={"xatol": 1e-10})
        _cif[key] = 10 ** res.x / a0
    return _cif[key]


# ------------------------------------------------------------------ Tacconi 2020 molecular gas (main sequence)
def t_c(z):
    L = math.log10(1 + z)
    return 10 ** (1.143 - 1.026 * L - 0.599 * L ** 2 + 0.528 * L ** 3)


def mu_mol(z, logm):
    tc = t_c(z)
    lssfr = (-0.16 - 0.026 * tc) * (logm + 0.025) - (6.51 - 0.11 * tc) + 9.0
    return 1.6 / (1 + z) * 10 ** lssfr


# ------------------------------------------------------------------ response of the fitted a0 to a mass offset (Fig. 6)
def resp(i, d):
    if d <= 0.2:
        return FIG6[0.2][i] * d / 0.2
    if d <= 0.45:
        return FIG6[0.2][i] + (FIG6[0.45][i] - FIG6[0.2][i]) * (d - 0.2) / 0.25
    return FIG6[0.45][i] + (FIG6[0.45][i] - FIG6[0.2][i]) * (d - 0.45) / 0.25


# ------------------------------------------------------------------ statistics
def sig_from_chi2(chi2, dof):
    if chi2 <= 0:
        return 0.0
    logp = stats.chi2.logsf(chi2, dof)
    return float(-ndtri_exp(logp - math.log(2.0)))


def wslope(z, y, s):
    w = 1 / s ** 2
    S, Sx, Sy, Sxx, Sxy = w.sum(), (w * z).sum(), (w * y).sum(), (w * z * z).sum(), (w * z * y).sum()
    D = S * Sxx - Sx * Sx
    b = (S * Sxy - Sx * Sy) / D
    a = (Sxx * Sy - Sx * Sxy) / D
    chi = float(np.sum(w * (y - a - b * z) ** 2))
    return b, math.sqrt(S / D), chi


def word(P0, Pmin, Pmax):
    if P0 <= 2:
        return "AGREES" + (", FRAGILE" if Pmax > 3 else "")
    if P0 > 3 and Pmin > 3:
        return "EXCLUDES"
    if P0 > 3 and Pmin > 2:
        return "EXCLUDES, FRAGILE"
    return "NO VERDICT"


B1 = [None, 9.0, 9.5, 10.0]
B2 = [0.0, 0.2, 0.45]
B3 = [-0.10, 0.0, 0.10]
WIN = [(-12.0, -10.5), (-11.5, -10.0), (-11.0, -9.5)]
DRIFT = [-0.5, 0.0, 0.5]
EREAD = ["E1", "E2"]
ASPUB = (None, 0.0, 0.0, (-11.5, -10.0), 0.0, "E1")
RAMP = (Z - Z[0]) / (Z[-1] - Z[0])


def corrected(Abins, b1, b2, b3):
    """ln a0 per bin after the mass (B1, B2) and inner-cut (B3) corrections; returns ln a0 and max mass offset."""
    lnA = np.log(Abins).copy()
    dmax = 0.0
    for i in range(4):
        mu = 0.0 if b1 is None else mu_mol(Z[i], b1)
        d = math.log10(10 ** b2 + mu)
        dmax = max(dmax, d)
        lnA[i] += LN10 * resp(i, d)
    lnA += np.log(1 + b3 * RAMP)
    return lnA, dmax


def sigmas(Abins, eread):
    e = ERR if eread == "E1" else ERR / 1.96
    return np.sqrt((e / Abins) ** 2 + (TRANS / Abins) ** 2)


def rows_for(case, a0, cfg, Abins=None):
    Abins = A if Abins is None else Abins
    b1, b2, b3, win, drift, er = cfg
    lnA, dmax = corrected(Abins, b1, b2, b3)
    s = sigmas(Abins, er)
    C = np.array([C_IF(win[0] + drift * RAMP[i], win[1] + drift * RAMP[i], a0) for i in range(4)])
    f = f_of(case, Z)
    y = lnA - np.log(C * f)
    b, sb, chi_lin = wslope(Z, y, s)
    PS = abs(b) / sb
    chiL = float(np.sum(((lnA - np.log(C * a0 * f)) / s) ** 2))
    PL = sig_from_chi2(chiL, 4)
    return {"slope": b, "sigma_slope": sb, "P_S": PS, "chi2_lin": chi_lin, "chi2_L": chiL, "P_L": PL,
            "dmax": dmax, "C_IF": C.tolist(), "lnA_corr": lnA.tolist()}


def scan(case, a0):
    out = []
    for b1, b2, b3, win, drift, er in itertools.product(B1, B2, B3, WIN, DRIFT, EREAD):
        cfg = (b1, b2, b3, win, drift, er)
        r = rows_for(case, a0, cfg)
        out.append((cfg, r))
    return out


def row_G(case, a0, a00, sa00, a1, sa1):
    zz = np.linspace(0.33, 1.44, 112)
    ff = f_of(case, zz)
    sl, ic = np.polyfit(zz, ff, 1)
    C = C_IF(-11.5, -10.0, a0)
    a1_law, a00_law = C * a0 * sl, C * a0 * ic
    return {"a1_law": a1_law, "a00_law": a00_law, "P_G": abs(a1 - a1_law) / sa1,
            "P_a00": abs(a00 - a00_law) / sa00}


def row_E(case):
    law = -np.log10(f_of(case, ESC_Z))
    res = {}
    for k in (1.0, 0.5, 0.0):
        chi = float(np.sum(((k * ESC_D - law) / ESC_S) ** 2))
        res[k] = {"chi2": chi, "P": sig_from_chi2(chi, 3), "law_dZP": law.tolist()}
    P0 = res[1.0]["P"]
    Ps = [res[k]["P"] for k in res]
    return res, word(P0, min(Ps), max(Ps))


def required_ramp(case, a0, target):
    """dex in a0, ramp 0 at bin 1 to -delta at bin 4 (on top of as-published), giving P_S = target."""
    base = rows_for(case, a0, ASPUB)
    def g(delta):
        Ab = A * 10 ** (-delta * RAMP)
        return rows_for(case, a0, ASPUB, Ab)["P_S"] - target if target > 0 else rows_for(case, a0, ASPUB, Ab)["slope"]
    try:
        return float(optimize.brentq(g, 0.0, 1.0))
    except ValueError:
        return float("nan")


# ------------------------------------------------------------------ known answers
lines, KA = [], {}
def say(s=""):
    lines.append(s)

f3 = {c: float(f_of(c, 3.0)) for c in ("D-Pan", "D-DES5", "D-Uni", "Q-Pan", "Q-DES5", "Q-Uni")}
exp3 = {"D-Pan": 0.775, "D-DES5": 0.737, "D-Uni": 0.706, "Q-Pan": 0.966, "Q-DES5": 1.005, "Q-Uni": 1.054}
KA["KA1"] = all(abs(f3[c] - exp3[c]) <= 0.0005 for c in exp3)
ka1b = (abs(1.320 * FOOT["canonical"] - 1.235e-10) <= 0.001e-10, abs(1.322 * FOOT["alt"] - 1.495e-10) <= 0.001e-10)
KA["KA1b"] = all(ka1b)
H0 = 67.4e3 / MPC_M
a0_can = C_SI * H0 / 2 * math.sqrt(3 * 0.685 / (8 * math.pi))
KA["KA2"] = abs(a0_can / FOOT["canonical"] - 1) <= 5e-4
fid6 = np.array(vec("mud_fig6_fid")) * 1e-10
KA["KA3"] = bool(np.all(np.abs(fid6 - A) <= 0.02e-10))
cdeep = {k: C_IF(-13.0, -12.0, FOOT[k]) for k in FOOT}
KA["KA4"] = all(abs(v - 1) <= 0.01 for v in cdeep.values())
ka5 = G_a1 / G_a1_s
KA["KA5"] = 25 <= ka5 <= 35
c1 = A[0] * 10 ** resp(0, 0.2); c4 = A[3] * 10 ** resp(3, 0.45)
KA["KA6"] = (1.0e-10 <= c1 <= 1.4e-10) and (1.0e-10 <= c4 <= 1.4e-10)
tc0, mu1 = t_c(0.0), mu_mol(1.0, 9.5)
KA["KA7"] = (13.5 <= tc0 <= 14.2) and (0.3 <= mu1 <= 1.2)

say(f"MDZ1 mode {MODE}; inputs CSV sha256 {sha}")
say(f"KA1 f(3) {', '.join(f'{c} {f3[c]:.4f}' for c in f3)} -> {'PASS' if KA['KA1'] else 'FAIL'}")
say(f"KA1b AZ2 a0(2.33) {1.320 * FOOT['canonical']:.4e} / {1.322 * FOOT['alt']:.4e} -> {'PASS' if KA['KA1b'] else 'FAIL'}")
say(f"KA2 canonical a0 from H0 67.4, Om_L 0.685: {a0_can:.5e} (rel {a0_can / FOOT['canonical'] - 1:+.2e}) -> {'PASS' if KA['KA2'] else 'FAIL'}")
say(f"KA3 Fig.6 fiducial vs Fig.3 bins: max |diff| {np.max(np.abs(fid6 - A)):.3e} -> {'PASS' if KA['KA3'] else 'FAIL'}")
say(f"KA4 C_IF deep window: {', '.join(f'{k} {v:.5f}' for k, v in cdeep.items())} -> {'PASS' if KA['KA4'] else 'FAIL'}")
say(f"KA5 a1/sigma = {ka5:.1f} -> {'PASS' if KA['KA5'] else 'FAIL'}")
say(f"KA6 bin1 at +0.2 dex {c1:.3e}, bin4 at +0.45 dex {c4:.3e} -> {'PASS' if KA['KA6'] else 'FAIL'}")
say(f"KA7 t_c(0) {tc0:.2f} Gyr, mu_mol(z1, logM 9.5) {mu1:.3f} -> {'PASS' if KA['KA7'] else 'FAIL'}")
J = {"mode": MODE, "csv_sha256": sha, "KA": KA}
if not all(KA.values()):
    say("A KNOWN ANSWER FAILED: no word.")
    J["word"] = None
    open(os.path.join(lane, f"mdz1_{MODE}.out"), "w").write("\n".join(lines) + "\n")
    json.dump(J, open(os.path.join(lane, f"mdz1_{MODE}.json"), "w"), indent=1)
    sys.exit(1)
say("ALL KNOWN ANSWERS PASS")
say()

GRADED = ["L", "D-Pan", "D-DES5", "D-Uni"]

# ------------------------------------------------------------------ mutation / null twin
if MODE in ("MUT", "NULL"):
    a0 = FOOT["canonical"]
    J["twin"] = {}
    ok = True
    cases = ["L"] if MODE == "MUT" else GRADED
    for case in cases:
        if MODE == "MUT":
            Ab = 2.0e-10 * f_of("H", Z) / f_of("H", Z[0])
        else:
            Ab = 2.0e-10 * f_of(case, Z)
        r = rows_for(case, a0, ASPUB, Ab)
        bite = r["P_S"] > 3
        J["twin"][case] = {"bins": Ab.tolist(), "P_S": r["P_S"], "slope": r["slope"], "sigma": r["sigma_slope"]}
        say(f"{MODE} case {case}: bins {', '.join(f'{x:.3e}' for x in Ab)}; P_S {r['P_S']:.3f} -> {'bites' if bite else 'does not bite'}")
        ok &= bite if MODE == "MUT" else (r["P_S"] < 1)
    say(f"{MODE} {'PASS' if ok else 'FAIL'} (MUT must bite, NULL must not)")
    J["pass"] = bool(ok)
    open(os.path.join(lane, f"mdz1_{MODE}.out"), "w").write("\n".join(lines) + "\n")
    json.dump(J, open(os.path.join(lane, f"mdz1_{MODE}.json"), "w"), indent=1)
    sys.exit(0 if ok else 1)

# ------------------------------------------------------------------ grading, one footing
a0 = FOOT[MODE]
say(f"FOOTING {MODE}: a0 = {a0:.5e} m/s^2; C_IF(W0) = {C_IF(-11.5, -10.0, a0):.4f} "
    f"-> law a0 in McGaugh's convention {C_IF(-11.5, -10.0, a0) * a0:.4e}")
say(f"C_IF windows: " + ", ".join(f"[{w[0]},{w[1]}] {C_IF(w[0], w[1], a0):.4f}" for w in WIN))
mus = {lm: [mu_mol(z, lm) for z in Z] for lm in (9.0, 9.5, 10.0)}
say("Tacconi mu_mol per bin: " + "; ".join(f"logM {lm}: " + ", ".join(f"{m:.3f}" for m in mus[lm]) for lm in mus))
say("Fig.6 response dlog a0 at +0.2 / +0.45 dex: " + ", ".join(f"{FIG6[0.2][i]:+.3f}/{FIG6[0.45][i]:+.3f}" for i in range(4)))
say()
J["footing_a0"] = a0
J["cases"] = {}
headline = {}
for case in GRADED + ["Q-Pan", "Q-DES5", "Q-Uni", "H"]:
    f = f_of(case, Z)
    rec = {"f_bins": f.tolist(), "max_abs_f_minus_1": float(np.max(np.abs(f - 1)))}
    ap = rows_for(case, a0, ASPUB)
    rec["as_published"] = ap
    G = row_G(case, a0, G_a00, G_a00_s, G_a1, G_a1_s)
    rec["G"] = G
    rec["G_other"] = {k: row_G(case, a0, *v) for k, v in GLOBALS.items() if k != "Eq4_DC14"}
    if case in GRADED:
        sc = scan(case, a0)
        PS = [r["P_S"] for _, r in sc]; PL = [r["P_L"] for _, r in sc]
        iSmin = int(np.argmin(PS)); iLmin = int(np.argmin(PL))
        wS = word(ap["P_S"], min(PS), max(PS)); wL = word(ap["P_L"], min(PL), max(PL))
        # single-bracket edges for S (others at as-published)
        singles = {}
        for name, idx, vals in (("B1", 0, B1), ("B2", 1, B2), ("B3", 2, B3), ("B4win", 3, WIN), ("B4drift", 4, DRIFT), ("B5", 5, EREAD)):
            for v in vals:
                cfg = list(ASPUB); cfg[idx] = v
                r = rows_for(case, a0, tuple(cfg))
                singles[f"{name}={v}"] = (r["P_S"], r["P_L"])
        if wS.startswith("EXCLUDES") and G["P_G"] > 3:
            hw = "MEASURED RISE EXCLUDES THE LAW [" + MODE + "]" + (", FRAGILE" if "FRAGILE" in wS else "")
            hw += " (level also excluded)" if wL.startswith("EXCLUDES") else " (level not excluded: " + wL + ")"
        elif wS.startswith("AGREES") and wL.startswith("AGREES"):
            hw = "a0(z) AGREES" + (", FRAGILE" if ("FRAGILE" in wS or "FRAGILE" in wL) else "")
        else:
            hw = "NO VERDICT"
        headline[case] = hw
        rec.update({"S_word": wS, "L_word": wL, "P_S_min": min(PS), "P_S_max": max(PS), "P_L_min": min(PL),
                    "P_L_max": max(PL), "cfg_S_min": str(sc[iSmin][0]), "cfg_L_min": str(sc[iLmin][0]),
                    "dmax_S_min": sc[iSmin][1]["dmax"], "dmax_overall": max(r["dmax"] for _, r in sc),
                    "singles": singles, "headline": hw,
                    "required_ramp_dex_PS2": required_ramp(case, a0, 2.0),
                    "required_ramp_dex_flat": required_ramp(case, a0, 0.0)})
        E, wE = row_E(case)
        rec["E"] = {str(k): v for k, v in E.items()}; rec["E_word"] = wE
        say(f"=== case {case} (graded) f(bins) " + ", ".join(f"{x:.4f}" for x in f) + f"; max|f-1| {rec['max_abs_f_minus_1']:.4f}")
        say(f"  S as published: slope {ap['slope']:+.4f} +- {ap['sigma_slope']:.4f} per unit z, P_S {ap['P_S']:.2f}, chi2 lin {ap['chi2_lin']:.2f}/2")
        say(f"  S grid: P_S min {min(PS):.2f} at {sc[iSmin][0]} (largest mass offset {sc[iSmin][1]['dmax']:.3f} dex), max {max(PS):.2f} -> {wS}")
        say(f"  L as published: chi2 {ap['chi2_L']:.1f}/4, P_L {ap['P_L']:.2f}; grid min {min(PL):.2f} at {sc[iLmin][0]}, max {max(PL):.2f} -> {wL}")
        say("  S singles (P_S / P_L): " + "; ".join(f"{k} {v[0]:.2f}/{v[1]:.2f}" for k, v in singles.items()))
        say(f"  G (Eq. 4) a1 law {G['a1_law']:.4e} vs 1.59e-10: P_G {G['P_G']:.1f}; intercept law {G['a00_law']:.4e} vs 1.00e-10: {G['P_a00']:.1f} sigma")
        for k, v in rec["G_other"].items():
            say(f"    reported {k}: a1 law {v['a1_law']:.3e}, P {v['P_G']:.1f}; intercept law {v['a00_law']:.3e}, P {v['P_a00']:.1f}")
        say(f"  required differential (unsourced brackets: pressure support, M/L evolution, selection): "
            f"{rec['required_ramp_dex_PS2']:.3f} dex lower a0 at bin 4 than bin 1 for P_S 2; {rec['required_ramp_dex_flat']:.3f} dex for slope 0")
        say(f"  E (Escala BTFR): law dZP " + ", ".join(f"{x:+.3f}" for x in E[1.0]['law_dZP']) +
            f"; P_E k1 {E[1.0]['P']:.2f}, k0.5 {E[0.5]['P']:.2f}, k0 {E[0.0]['P']:.2f} -> {wE}")
        say(f"  HEADLINE {case}: {hw}")
    else:
        say(f"--- case {case} (reported) f(bins) " + ", ".join(f"{x:.4f}" for x in f) +
            f"; P_S {ap['P_S']:.2f}, P_L {ap['P_L']:.2f}; P_G {G['P_G']:.1f} (a1 law {G['a1_law']:.3e})")
    J["cases"][case] = rec
say()
sep_sig = float(np.min(sigmas(A, "E1")))
sep = max(J["cases"][c]["max_abs_f_minus_1"] for c in GRADED)
say(f"SEPARATION: max |f - 1| over the bins and graded cases {sep:.4f}; smallest bin sigma (ln, E1) {sep_sig:.4f} -> "
    + ("does NOT separate the law from constant-a0 MOND" if sep < sep_sig else "could separate from constant-a0 MOND"))
J["separation"] = {"max_abs_f_minus_1": sep, "min_sigma_ln": sep_sig, "separates_from_MOND": bool(sep >= sep_sig)}
J["headline"] = headline
say("HEADLINE " + MODE + ": " + "; ".join(f"{c}: {w}" for c, w in headline.items()))
open(os.path.join(lane, f"mdz1_{MODE}.out"), "w").write("\n".join(lines) + "\n")
json.dump(J, open(os.path.join(lane, f"mdz1_{MODE}.json"), "w"), indent=1, default=str)
