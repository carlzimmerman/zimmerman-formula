#!/usr/bin/env python3
"""NF1 POST-RESULT, reported only: RT1's recipe on LITTLE THINGS with route E: E = log(V^2/R) - log(g_N + G M_h(<R)/R^2), M200 from EM1's relation, floor vs no floor. IC 1613, WLM, DDO 210, DDO 216, and all galaxies with an SED mass. Z uses RT1's sE. Negative E means over-predicted.
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
FHERE = os.path.dirname(os.path.abspath(__file__)); FRB = os.path.dirname(FHERE)
CE = json.load(open(os.path.join(FRB, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; ETAV = [CE[str(e)]["med"] for e in (12, 13, 14)]; FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2)
LSD = os.path.join(FRB, "LS1_lstar_analogs"); S = open(os.path.join(LSD, "ls1_analogs.py")).read(); __file__ = os.path.join(LSD, "ls1_analogs.py")
exec(compile(S[:S.index('P("LS1 SPARC')], "ls1_head", "exec")); HERE = FHERE
S1 = 1.25 * 0.5 * math.log10(8.05 / 5.72); S2 = 1.25 * math.log10(8.05 / 5.92)
def Srule(M, s, floor=None):
    Mt = M / FC; c = FC * float(np.interp(math.log10(Mt), [12, 13, 14], ETAV)) * 10 ** (s * max(0.0, 12 - math.log10(Mt))) * sigma_coll(TAG, Mt)[0] * MSUNE / PC2
    return c if floor is None else max(floor, c)
def Ei(lMb, R_kpc, V, s, floor=None):
    bg = BGS[TAG]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); M = 10 ** (bg["a"] + bg["b"] * (lMb - 10)); R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); c = Srule(M, s, floor); r0 = solve_r0(M * MSUNE, R200, c)
    R = R_kpc * KPC; gN = GE * 10 ** lMb * MSUNE / R ** 2; gh = GE * math.pi * c * r0 ** 2 * B(R / r0) / R ** 2; gobs = (V * 1e3) ** 2 / R; return math.log10(gobs) - math.log10(gN + gh), c / (MSUNE / PC2), r0 / KPC, math.log10(M)
J = json.load(open(os.path.join(FRB, "RT1_lt_rotation_regrade", "rt1_lt_rotation_regrade_results.json"))); LG = J["lg"]["canonical"]; ALL = J["all26"]
OUTL = []
def Pn(s): print(s, flush=True); OUTL.append(s)
RULES = {"law can (RT1)": None, "floor can": (0.0, SIG["canonical"]), "floor alt": (0.0, SIG["alt"]), "N0": (0.0, None), "N1": (S1, None), "N2": (S2, None)}; R_ = {}
Pn("NF1 on RT1's LITTLE THINGS recipe: E (Z) by rule; negative is over-predicted; kappa = 1/2 FITTED; not theory closed")
for nm, g in LG.items():
    m = g["MSED"]; R_[nm] = {}; row = []
    for rk, rv in RULES.items():
        if rv is None: e = m["E"]; R_[nm][rk] = dict(E=e, Z=m["Z"]); row.append(f"{rk} {e:+.3f} ({m['Z']:+.1f})")
        else:
            e, c, r0, lM = Ei(m["logMb"], m["R"], m["V"], rv[0], rv[1]); z = e / m["sE"]; R_[nm][rk] = dict(E=e, Z=z, S=c, r0=r0, lgM200=lM); row.append(f"{rk} {e:+.3f} ({z:+.1f}, S {c:.0f})")
    Pn(f"  {nm} (R {m['R']} kpc, V {m['V']}, lg Mb {m['logMb']:.2f}): " + "; ".join(row))
res = dict(lg=R_)
RTF = os.path.join(FRB, "RT1_lt_rotation_regrade", "rt1_lt_rotation_regrade.py"); RTT = open(RTF).read(); cutrt = 'RES = dict(criteria="ac267e8bf1"'; assert RTT.count(cutrt) == 1; RTN = {"__file__": RTF, "__name__": "rt1_ro"}; exec(compile(RTT[:RTT.index(cutrt)], RTF, "exec"), RTN)
tab = {k: [] for k in RULES}; A0C = RTN["A0"]["canonical"]; rowsE = {}
for nm in RTN["NAMES"]:
    d = RTN["E_rot"](RTN["rec"](nm)[0], A0C, "MSED")
    if not d: continue
    tab["law can (RT1)"].append(d["E"]); rowsE[nm] = {"law can (RT1)": d["E"], "lgMb": d["logMb"], "R": d["R"], "V": d["V"], "sE": d["sE"]}
    for rk, rv in RULES.items():
        if rv is not None: e = Ei(d["logMb"], d["R"], d["V"], rv[0], rv[1])[0]; tab[rk].append(e); rowsE[nm][rk] = e
res["all"] = {}; res["rows"] = rowsE
for rk, v in tab.items():
    a_ = np.array(v); res["all"][rk] = dict(n=len(a_), median=float(np.median(a_)), p16=float(np.percentile(a_, 16)), p84=float(np.percentile(a_, 84)), rms=float(np.sqrt(np.mean(a_ ** 2)))); Pn(f"  all LITTLE THINGS with SED mass, {rk}: n {len(a_)}, median E {np.median(a_):+.3f} [{np.percentile(a_, 16):+.3f}, {np.percentile(a_, 84):+.3f}], rms {np.sqrt(np.mean(a_ ** 2)):.3f}")
json.dump(res, open(os.path.join(HERE, "nf1_lt.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "nf1_lt.out"), "w").write("\n".join(OUTL) + "\n")
