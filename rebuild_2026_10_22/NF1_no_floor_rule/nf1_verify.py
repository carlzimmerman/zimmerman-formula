#!/usr/bin/env python3
"""NF1 POST-RESULT, reported only: is the no-floor pass real at low mass? rms at free Upsilon and at Upsilon 0.50, signed offset at 0.50, by V_flat and for gas-dominated galaxies, where Upsilon cannot compensate; FC1 with floor, N0, N1, N2, and the simple-nu law. Background A.
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
FHERE = os.path.dirname(os.path.abspath(__file__)); FRB = os.path.dirname(FHERE)
CE = json.load(open(os.path.join(FRB, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; ETAV = [CE[str(e)]["med"] for e in (12, 13, 14)]; FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2)
LSD = os.path.join(FRB, "LS1_lstar_analogs"); S = open(os.path.join(LSD, "ls1_analogs.py")).read(); __file__ = os.path.join(LSD, "ls1_analogs.py")
exec(compile(S[:S.index('P("LS1 SPARC')], "ls1_head", "exec")); HERE = FHERE
S1 = 1.25 * 0.5 * math.log10(8.05 / 5.72); S2 = 1.25 * math.log10(8.05 / 5.92); A0 = dict(canonical=9.3603e-11, alt=1.1312e-10)
def Srule(M, s, floor=None):
    Mt = M / FC; c = FC * float(np.interp(math.log10(Mt), [12, 13, 14], ETAV)) * 10 ** (s * max(0.0, 12 - math.log10(Mt))) * sigma_coll(TAG, Mt)[0] * MSUNE / PC2
    return c if floor is None else max(floor, c)
def gh(q, s, floor=None):
    bg = BGS[TAG]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); M = 10 ** (bg["a"] + bg["b"] * (q["lMb"] - 10)); R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); c = Srule(M, s, floor); r0 = solve_r0(M * MSUNE, R200, c); return GE * math.pi * c * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
RULES = {"FC1 floor can": (lambda q: gh(q, 0.0, SIG["canonical"])), "FC1 floor alt": (lambda q: gh(q, 0.0, SIG["alt"])), "N0": (lambda q: gh(q, 0.0)), "N1": (lambda q: gh(q, S1)), "N2": (lambda q: gh(q, S2))}
def pred_law(q, f):
    g = np.maximum(q["GB"], 1e-300); y = g / A0[f]; return np.log10(g * (0.5 + np.sqrt(0.25 + 1.0 / y)))
OUTL = []
def Pn(s): print(s, flush=True); OUTL.append(s)
Pn("NF1 verify: rms in dex (free Upsilon / Upsilon 0.50), signed offset log(obs/pred) at 0.50, median Upsilon, fraction at the grid top; background A; kappa = 1/2 FITTED; not theory closed")
ALL = [q for q in GALS]; vf = {q["name"]: TAB.get(q["name"], {}).get("vf", float("nan")) for q in ALL}
fg = {q["name"]: 1.33 * q["meta"]["MHI"] / max(0.5 * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"], 1e-30) for q in ALL}
GROUPS = {"all 175": ALL, "V 20-60": [q for q in ALL if 20 <= vf[q["name"]] < 60], "V 60-100": [q for q in ALL if 60 <= vf[q["name"]] < 100], "V 100-150": [q for q in ALL if 100 <= vf[q["name"]] < 150], "V 150-200": [q for q in ALL if 150 <= vf[q["name"]] < 200], "V 200-250": [q for q in ALL if 200 <= vf[q["name"]] < 250], "V 250-400": [q for q in ALL if 250 <= vf[q["name"]] < 400], "gas-dominated": [q for q in ALL if fg[q["name"]] >= 0.5], "gas >= 0.7": [q for q in ALL if fg[q["name"]] >= 0.7]}
def stats(qs, pred):
    A, Bb, C, Dd, U = 0.0, 0.0, 0.0, 0.0, []
    for q in qs:
        lgp = pred(q); wr2, ws, iu = fit_one(q, lgp); A += float(wr2); Bb += float(ws); U.append(UPS[int(iu)])
        ok, w = q["OK"][:, I05], q["W"]; r = (np.log10(q["GO"]) - lgp[:, I05])[ok]; ww = w[ok]; C += float((ww * r * r).sum()); Dd += float((ww * r).sum())
    return math.sqrt(A / Bb), math.sqrt(C / Bb), Dd / Bb, float(np.median(U)), float(np.mean(np.array(U) >= 1.19)), float(np.mean(np.array(U) <= 0.31))
R = {}
PRED = {k: (lambda q, fn=fn: np.log10(np.maximum(q["GB"] + fn(q)[:, None], 1e-300))) for k, fn in RULES.items()}; PRED["law can"] = lambda q: pred_law(q, "canonical"); PRED["law alt"] = lambda q: pred_law(q, "alt")
for gname, qs in GROUPS.items():
    Pn(f"  {gname} (n {len(qs)})"); R[gname] = {}
    for k, pr in PRED.items():
        a, b, c, u, ft, fb = stats(qs, pr); R[gname][k] = dict(rms_free=a, rms_05=b, off_05=c, U=u, f_top=ft, f_bot=fb); Pn(f"     {k:14s} rms {a:.4f} / {b:.4f}; offset at 0.50 {c:+.3f}; U {u:.2f}; at top {ft:.2f}, at bottom {fb:.2f}")
json.dump(R, open(os.path.join(HERE, "nf1_verify.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "nf1_verify.out"), "w").write("\n".join(OUTL) + "\n")
