#!/usr/bin/env python3
"""CFG655: NGC 1052 trail (DF2, DF4, DF9) and LEDA 4014647 as a cold-energy supply test.

Criteria: FROZEN_CRITERIA.md (committed alone, 0207b6abe). One process, seconds, no downloads.
MUTATE=1 cyclically shifts Rule P's labels; the headline must then FAIL (exit 1).
kappa = 1/2 fitted; cold energy mass required; not theory closed.
"""
import itertools, json, math, os, sys
import numpy as np
from scipy.optimize import brentq

MUTATE = os.environ.get("MUTATE", "0") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "_MUTATE" if MUTATE else ""

G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19
FOOTS = {"canonical": 9.3603e-11, "alt": 1.1312e-10}


# ---- the record's XC4 repaired kernel (copied from CFG5_common.nu_mono; checked against CFG626's grid form below)
def _h_rar(y):
    z = np.sqrt(y); return y / np.expm1(z)


_dh = lambda t: (2 * np.expm1(math.sqrt(t)) - math.sqrt(t) * (1 + np.expm1(math.sqrt(t)))) / (2 * np.expm1(math.sqrt(t)) ** 2)
_YP = brentq(_dh, 1.0, 5.0); _HP = _h_rar(_YP); _DELTA = 0.05
_YS = brentq(lambda t: _dh(t) - _DELTA * _HP / (t + _YP), 1.0, _YP)


def nu_mono(y):
    y = float(y)
    h = _h_rar(max(y, 1e-300)) if y <= _YS else _h_rar(_YS) + _DELTA * _HP * math.log((y + _YP) / (_YS + _YP))
    return 1.0 + h / y


# ---- inputs (FROZEN_CRITERIA.md; sources in README)
GAL = {
    "DF2":  dict(Ms=2.0e8, eMs=0.20, Re=2.0, Dref=20.0, Dprim=20.0, obs=(8.5, 2.3, 3.1), src="Danieli+19 KCWI stars"),
    "DF4":  dict(Ms=1.5e8, eMs=0.27, Re=1.6, Dref=20.0, Dprim=20.0, obs=(6.3, 2.5, 1.6), src="Shen+23 fiducial"),
    "DF9":  dict(Ms=1.4e8, eMs=0.23, Re=1.1, Dref=20.6, Dprim=20.6, obs=(6.5, 3.9, 4.3), src="Keim+26 KCWI"),
    "LEDA": dict(Ms=10 ** 7.98, eMs=10 ** 0.06 - 1, Re=0.601, Dref=17.7, Dprim=17.7, obs=(15.8, 2.0, 2.0), src="Vaz+26 KCWI"),
}
SECONDARY = [("DF2", "Emsellem+19 MUSE stars", (10.8, 3.2, 4.0)), ("DF2", "GC system, interloper removed (2503.03404)", (8.63, 2.88, 2.14)),
             ("DF2", "GC system, all 16 (2503.03404)", (14.86, 3.89, 2.83)), ("DF4", "Shen+23 KCWI stars", (8.0, 2.3, 1.9)),
             ("DF4", "vD+19 GCs", (4.2, 4.4, 2.2))]
RULE_P = {"DF2": "E", "DF4": "E", "DF9": "E", "LEDA": "T"}
AGES = {"DF2": (8.28, 2.07, 1.41), "DF4": (10.68, 1.38, 1.51), "DF9": (10.36, 1.61, 1.95), "LEDA": (11.54, 1.12, 1.69)}  # Tang+25b Table 2
T_COLL = 8.0
NAMES = list(GAL)


def predict(g, D, a0, law, fs=1.0):
    f = D / g["Dref"]; Mb = g["Ms"] * f * f; r = (4.0 / 3.0) * g["Re"] * f * KPC
    gN = G * 0.5 * Mb * MSUN / r ** 2
    nu = nu_mono(gN / a0) if law else 1.0
    nu = 1.0 + fs * (nu - 1.0)
    s = math.sqrt(nu * gN * r / 3.0) / 1e3
    # prediction error from M_* only: propagate by finite difference in Mb
    Mb2 = Mb * (1 + g["eMs"]); gN2 = G * 0.5 * Mb2 * MSUN / r ** 2
    nu2 = (1.0 + fs * (nu_mono(gN2 / a0) - 1.0)) if law else 1.0
    s2 = math.sqrt(nu2 * gN2 * r / 3.0) / 1e3
    return s, abs(s2 - s), gN / a0, (nu_mono(gN / a0) if law else 1.0)


def zscore(obs, sp, ep):
    s, up, lo = obs
    e = up if sp > s else lo
    return (s - sp) / math.sqrt(e * e + ep * ep)


def score(labels, foot, Doverride=None):
    a0 = FOOTS[foot]; out = {}
    for n in NAMES:
        g = GAL[n]; D = (Doverride or {}).get(n, g["Dprim"])
        sN, eN, y, _ = predict(g, D, a0, False); sL, eL, _, nu = predict(g, D, a0, True)
        sF, eF = (sN, eN) if labels[n] == "E" else (sL, eL)
        out[n] = dict(D=D, y=y, nu=nu, sig_N=sN, e_N=eN, sig_law=sL, e_law=eL, label=labels[n], sig_fw=sF,
                      Z_N=zscore(g["obs"], sN, eN), Z_law=zscore(g["obs"], sL, eL), Z_fw=zscore(g["obs"], sF, eF))
    return out


lines = []
def P(s=""):
    print(s); lines.append(s)


# ---- kernel check against the CFG626 grid form
def _nu_grid_check():
    LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
    dh = lambda y: (2 * np.expm1(np.sqrt(y)) - np.sqrt(y) * (1 + np.expm1(np.sqrt(y)))) / (2 * np.expm1(np.sqrt(y)) ** 2)
    with np.errstate(all="ignore"):
        DH = np.maximum(np.nan_to_num(dh(YG), nan=0.0), _DELTA * _HP / (YG + _YP))
    H = float(_h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])
    ys = [0.01, 0.05, 0.2, 1.0, 5.0]
    return max(abs(nu_mono(y) - (1 + np.interp(np.log10(y), LYG, H) / y)) / nu_mono(y) for y in ys)


kchk = _nu_grid_check()
P("CFG655  NGC 1052 trail + LEDA 4014647: cold-energy supply test" + ("   [MUTATE: Rule P labels cyclically shifted]" if MUTATE else ""))
P(f"kernel check nu_mono (CFG5 closed form) vs CFG626 grid form: max rel diff {kchk:.2e}")
P("")

labels = dict(RULE_P)
if MUTATE:
    vals = [RULE_P[n] for n in NAMES]; vals = vals[-1:] + vals[:-1]
    labels = dict(zip(NAMES, vals))
P("Rule P labels: " + ", ".join(f"{n}={labels[n]}" for n in NAMES))

RES = {"labels": labels, "kernel_check": kchk, "primary": {}, "dist": {}, "secondary": {}, "partial": {}, "rules": {}, "mutate16": {}}
for foot in FOOTS:
    P(""); P(f"=== {foot}  a0 = {FOOTS[foot]:.4e} m/s^2  (primary distances)")
    P(f"{'galaxy':6s} {'D':>5s} {'y=gN/a0':>8s} {'nu':>5s} | {'sig_obs':>15s} | {'Newton':>11s} {'Z_N':>6s} | {'law':>11s} {'Z_law':>6s} | label {'Z_fw':>6s}")
    sc = score(labels, foot); RES["primary"][foot] = sc
    for n in NAMES:
        v = sc[n]; o = GAL[n]["obs"]
        P(f"{n:6s} {v['D']:5.1f} {v['y']:8.4f} {v['nu']:5.2f} | {o[0]:5.1f} +{o[1]:.1f}/-{o[2]:.1f} | {v['sig_N']:5.2f}+-{v['e_N']:.2f} {v['Z_N']:+6.2f} | "
          f"{v['sig_law']:5.2f}+-{v['e_law']:.2f} {v['Z_law']:+6.2f} |   {v['label']}   {v['Z_fw']:+6.2f}")

# ---- verdict per footing
def verdict(foot, labs):
    sc = score(labs, foot)
    zfw = max(abs(sc[n]["Z_fw"]) for n in NAMES)
    disc = abs(sc["DF2"]["Z_law"]) >= 3 and abs(sc["DF4"]["Z_law"]) >= 3
    dist_ok = all(max(abs(v["Z_fw"]) for v in score(labs, foot, {"DF2": d}).values()) <= 2 for d in (17.6, 21.7))
    if zfw > 3: v = "FAIL"
    elif zfw > 2: v = "TENSION"
    elif not disc: v = "NOT DIAGNOSTIC"
    elif not dist_ok: v = "TENSION (DF2 distance)"
    else: v = "PASS"
    return v, zfw, disc, dist_ok

P(""); P("=== VERDICT (Rule P)")
VER = {}
for foot in FOOTS:
    v, zfw, disc, dok = verdict(foot, labels); VER[foot] = v
    P(f"{foot}: {v}   max|Z_fw| = {zfw:.2f}; sigma_law fails DF2 and DF4 at >=3: {disc}; holds with DF2 at 17.6 and 21.7 Mpc: {dok}")
headline = all(v == "PASS" for v in VER.values())
RES["verdict"] = VER
P("HEADLINE: " + ("PASS CONDITIONAL ON THE FORMATION-CHANNEL LABEL" if headline else "not PASS: " + str(VER)))

# ---- distance bracket
P(""); P("=== Distance bracket (all models; Z_N / Z_law / Z_fw)")
for foot in FOOTS:
    for tag, Dov in (("all at 13 Mpc", {n: 13.0 for n in NAMES}), ("all at 20 Mpc", {n: 20.0 for n in NAMES}),
                     ("DF2 at 16.2", {"DF2": 16.2}), ("DF2 at 17.6", {"DF2": 17.6}), ("DF2 at 21.7", {"DF2": 21.7})):
        sc = score(labels, foot, Dov); RES["dist"][f"{foot}|{tag}"] = sc
        P(f"{foot:9s} {tag:14s} " + "  ".join(f"{n}: {sc[n]['Z_N']:+.2f}/{sc[n]['Z_law']:+.2f}/{sc[n]['Z_fw']:+.2f}" for n in NAMES))

# ---- R1 alternative rules
P(""); P("=== R1 alternative labelling rules (reported)")
from scipy.stats import norm
pA = {}
for n, (t, up, lo) in AGES.items():
    e = lo if t > T_COLL else up
    pA[n] = 1 - norm.cdf((T_COLL - t) / e)
ruleA = {n: ("AMBIG" if 0.4 <= pA[n] <= 0.6 else ("T" if pA[n] > 0.5 else "E")) for n in NAMES}
ruleM = {n: "E" for n in NAMES}
P("Rule A P(t_M > 8 Gyr): " + ", ".join(f"{n} {pA[n]:.2f} -> {ruleA[n]}" for n in NAMES))
for rname, rl in (("Rule M (membership only)", ruleM), ("Rule A (age only)", ruleA)):
    for foot in FOOTS:
        variants = [dict(rl)]
        amb = [n for n in NAMES if rl[n] == "AMBIG"]
        if amb:
            variants = []
            for combo in itertools.product("ET", repeat=len(amb)):
                d = dict(rl); d.update(zip(amb, combo)); variants.append(d)
        for vl in variants:
            sc = score(vl, foot)
            nin = sum(abs(sc[n]["Z_fw"]) <= 2 for n in NAMES)
            P(f"{rname:26s} {foot:9s} labels {''.join(vl[n] for n in NAMES)}: within 2 sigma {nin}/4  "
              + " ".join(f"{n} {sc[n]['Z_fw']:+.2f}" for n in NAMES))
            RES["rules"][f"{rname}|{foot}|{''.join(vl[n] for n in NAMES)}"] = {n: sc[n]["Z_fw"] for n in NAMES}

# ---- R2 partial supply (Theory v2 eq. 2-3; CFG634 static form)
P(""); P("=== R2 partial supply: largest supply fraction f_s of the law target allowed at Z = +2 (E galaxies)")
for foot in FOOTS:
    a0 = FOOTS[foot]; row = []
    for n in ("DF2", "DF4", "DF9"):
        g = GAL[n]
        fz = lambda fs: zscore(g["obs"], *predict(g, g["Dprim"], a0, True, fs)[:2]) + 2.0
        if fz(1.0) > 0: fmax = 1.0
        elif fz(0.0) < 0: fmax = 0.0
        else: fmax = brentq(fz, 0.0, 1.0)
        RES["partial"][f"{foot}|{n}"] = fmax; row.append(f"{n} f_s <= {fmax:.3f}")
    P(f"{foot:9s} " + "; ".join(row))

# ---- R3 LEDA 4014647
P(""); P("=== R3 LEDA 4014647: measured Mdyn/M_* (<r_1/2) = 3 +- 1 (Vaz+26) vs the law's nu at r_1/2")
for foot in FOOTS:
    v = RES["primary"][foot]["LEDA"]; P(f"{foot:9s} nu(y={v['y']:.3f}) = {v['nu']:.2f}; a progenitor-remnant surplus would push sigma ABOVE sigma_law = {v['sig_law']:.2f}")

# ---- R4 secondary dispersions under Rule P
P(""); P("=== R4 secondary dispersions (Z_N / Z_law / Z_fw), primary distances")
for foot in FOOTS:
    a0 = FOOTS[foot]
    for n, lab, obs in SECONDARY:
        g = GAL[n]; sN, eN, _, _ = predict(g, g["Dprim"], a0, False); sL, eL, _, _ = predict(g, g["Dprim"], a0, True)
        zN, zL = zscore(obs, sN, eN), zscore(obs, sL, eL); zF = zN if labels[n] == "E" else zL
        RES["secondary"][f"{foot}|{n}|{lab}"] = (zN, zL, zF)
        P(f"{foot:9s} {n:4s} {lab:42s} {obs[0]:5.2f}: {zN:+.2f} / {zL:+.2f} / {zF:+.2f}")

# ---- M1: all 16 label assignments
P(""); P("=== M1 all 16 E/T assignments (pass = every galaxy |Z| <= 2 on both footings, primary distances)")
npass = 0; passing = []
for combo in itertools.product("ET", repeat=4):
    lab = dict(zip(NAMES, combo))
    ok = all(all(abs(score(lab, f)[n]["Z_fw"]) <= 2 for n in NAMES) for f in FOOTS)
    RES["mutate16"]["".join(combo)] = ok
    if ok: npass += 1; passing.append("".join(combo))
P(f"N_pass = {npass}/16 ({', '.join(passing) or 'none'}; order {'/'.join(NAMES)}); random-label pass rate {npass / 16:.3f}; "
  f"SPECIFIC (N_pass <= 2): {npass <= 2}")
RES["N_pass"] = npass

P(""); P("kappa = 1/2 fitted; cold energy mass required; not theory closed.")
with open(os.path.join(HERE, f"cfg655_trail_supply{TAG}_results.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=float)
with open(os.path.join(HERE, f"cfg655_trail_supply{TAG}.out"), "w") as fh:
    fh.write("\n".join(lines) + "\n")
sys.exit(0 if headline else 1)
