#!/usr/bin/env python3
"""CFG571: pre-registered required-baryon / required-gas predictions for three unreleased ALMA data sets (FROZEN_CRITERIA.md, 5f68a68c3).
Run: python3 cfg571_prereg.py [--mutate].  Record inputs only; nothing is fetched."""
import csv, os, sys, json, math
import numpy as np
from scipy.optimize import brentq
from scipy.special import i0, i1, k0, k1
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "campaign_fresh_gravity", "CFG44_fluid_target"))
from Bcommon import nu_mono
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
NU = (lambda y: np.ones_like(np.asarray(y, float))) if MUT else nu_mono
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
G = 4.30091e-6                      # kpc (km/s)^2 / Msun
U = 1e6 / 3.0857e19                 # 1 (km/s)^2/kpc in m/s^2
FOOT = {"canon 9.36e-11": 9.3603e-11, "alt 1.13e-10": 1.1312e-10}
W0, WA, OM = -0.838, -0.62, 0.315
def r_desi(z): a = 1 / (1 + z); return math.sqrt(a ** (-3 * (1 + W0 + WA)) * math.exp(-3 * WA * (1 - a)))
def r_H(z): return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)
def r_fb(z): return float(np.interp(z, [0, 1, 2, 2.5], [1.0, 1.20, 2.82, 4.88]))
MODELS = {"F-DESI": r_desi, "F-flat": lambda z: 1.0, "R-H": r_H, "L-fb(RAR-eq)": r_fb}
CHK = []
def check(name, ok, extra=""): CHK.append((name, bool(ok))); P(f"[{'PASS' if ok else 'FAIL'}] {name} {extra}")

def B(y): return y * y * (i0(y) * k0(y) - i1(y) * k1(y))
def v2_exp(M, Rd, R): return 2 * G * M / Rd * B(R / (2 * Rd))
def m_from_v2(v2, Rg, R): return v2 * Rg / (2 * G * B(R / (2 * Rg)))
def gbar_req(gobs, a0):           # g in (km/s)^2/kpc, a0 in m/s^2
    A = a0 / U; f = lambda gb: float(NU(gb / A)) * gb - gobs
    return brentq(f, gobs * 1e-8, gobs * (1 + 1e-12), xtol=gobs * 1e-12, rtol=1e-12)

def predict(R, Vc, z, Mstar, Rd):
    """required log M_bar (spherical-equivalent V^2 R/G of the required baryonic velocity) and total M_gas for both gas shapes, per model and footing."""
    gobs = Vc ** 2 / R; out = {}
    for fn, a00 in FOOT.items():
        for mn, rf in MODELS.items():
            vb2 = gbar_req(gobs, a00 * rf(z)) * R; vs2 = v2_exp(Mstar, Rd, R); vg2 = vb2 - vs2
            d = dict(logVbar2R_G=math.log10(vb2 * R / G), floor=vg2 <= 0)
            for gs, k in (("Rg=Rd", 1.0), ("Rg=1.5Rd", 1.5)):
                d["logMgas_" + gs] = math.log10(m_from_v2(vg2, k * Rd, R)) if vg2 > 0 else None
            out[(fn, mn)] = d
    return out
fmt = lambda x: "FLOOR" if x is None else f"{x:5.2f}"

# ---- controls ----
check("C1 DESI CPL a0 ratio at z = 2 is 0.87 +- 0.01", abs(r_desi(2.0) - 0.87) < 0.01, f"({r_desi(2.0):.3f})")
ys = np.linspace(0.3, 2.0, 20001); pk = (2 * B(ys)).max(); check("C3 Freeman peak V^2 = 0.387 +- 0.003 GM/Rd near R 2.15 Rd", abs(pk - 0.387) < 0.003 and abs(2 * ys[(2 * B(ys)).argmax()] - 2.15) < 0.05, f"({pk:.4f} at {2 * ys[(2 * B(ys)).argmax()]:.3f} Rd)")
save = NU; NU = lambda y: np.ones_like(np.asarray(y, float)); g = 150.0 ** 2 / 9.0
check("C4 Newtonian round trip: V_bar,req = V_c to < 1e-6 with nu = 1", abs(math.sqrt(gbar_req(g, 1.13e-10) * 9.0) / 150.0 - 1) < 1e-6); NU = save

# ---- KURVS ----
D = os.path.join(ROOT, "data_assembly", "arxiv_tables")
rd = lambda f: {r["kurvs_id"]: r for r in csv.DictReader(open(os.path.join(D, f)))}
I, K, V, F = rd("kurvs2023_integrated.csv"), rd("kurvs2023_kinematics.csv"), rd("kurvs2023_velocities_at_radii.csv"), rd("kurvs2023_fdm.csv")
k15 = (float(V["15"]["v_at_last_point_kms"]), float(V["15"]["R_halpha_max_kpc"]), float(I["15"]["logMstar"]), float(I["15"]["reff_kpc"]), float(K["15"]["sigma0_kms"]))
check("C2 KURVS-15 inputs match CFG569 (112.2 at 9.2 kpc, logM* 10.07, reff 3.8, sigma0 68)", k15 == (112.2, 9.2, 10.07, 3.8, 68.0), str(k15))
IN = ["3", "4", "5", "6", "7", "9", "11", "12", "15", "16", "19", "20", "21", "22"]
res = {"KURVS": {}, "GS4_24110": {}, "U4_27928": {}}
for br in ("P-B", "P0"):
    P(f"\n=== KURVS discs in 2026.1.00363.S, pressure branch {br}: required total log M_gas (Rg=Rd) per model, footing canon / alt ===")
    P(f"{'id':>3} {'z':>5} {'v/s0':>4} {'R':>5} {'Vc':>6} {'logM*':>5} {'gobs/a0':>7} | " + " | ".join(f"{m:>15}" for m in MODELS) + " | KURVS fDM")
    for k in IN:
        z, lm, re, s0 = float(I[k]["z_halpha"]), float(I[k]["logMstar"]), float(I[k]["reff_kpc"]), float(K[k]["sigma0_kms"])
        R, v, vs = float(V[k]["R_halpha_max_kpc"]), float(V[k]["v_at_last_point_kms"]), float(K[k]["vrot_over_sigma0"])
        Rd = re / 1.678; Vc = math.sqrt(v * v + (2 * s0 * s0 * R / Rd if br == "P-B" else 0.0))
        pr = predict(R, Vc, z, 10 ** lm, Rd); prim = vs >= 1.5
        res["KURVS"].setdefault(k, dict(z=z, vs=vs, primary=prim, R=R, logMstar=lm, fDM=F.get(k, {}).get("fDM_within_reff", "")))[br] = dict(Vc=Vc, pred={f"{a}|{b}": c for (a, b), c in pr.items()})
        cell = lambda m: f"{fmt(pr[('canon 9.36e-11', m)]['logMgas_Rg=Rd'])}/{fmt(pr[('alt 1.13e-10', m)]['logMgas_Rg=Rd'])}"
        P(f"{k:>3} {z:5.3f} {vs:4.1f}{'*' if prim else ' '} {R:5.1f} {Vc:6.1f} {lm:5.2f} {Vc ** 2 / R * U / 1.1312e-10:7.2f} | " + " | ".join(f"{cell(m):>15}" for m in MODELS) + f" | {F.get(k, {}).get('fDM_within_reff', '')}")
P("  (* = primary sample, v/sigma0 >= 1.5; FLOOR = stars alone already exceed the required baryons; gobs/a0 on the alt footing)")

# ---- forecast ----
P("\n=== Pre-data forecast (KURVS primary sample) ===")
fc = {}
for br in ("P-B", "P0"):
    for fn in FOOT:
        prim = [v for v in res["KURVS"].values() if v["primary"]]
        sep = np.median([v[br]["pred"][f"{fn}|R-H"]["logVbar2R_G"] - v[br]["pred"][f"{fn}|F-DESI"]["logVbar2R_G"] for v in prim])
        sepL = np.median([v[br]["pred"][f"{fn}|L-fb(RAR-eq)"]["logVbar2R_G"] - v[br]["pred"][f"{fn}|F-DESI"]["logVbar2R_G"] for v in prim])
        sepF = np.median([v[br]["pred"][f"{fn}|F-flat"]["logVbar2R_G"] - v[br]["pred"][f"{fn}|F-DESI"]["logVbar2R_G"] for v in prim])
        floors = {m: sum(v[br]["pred"][f"{fn}|{m}"]["floor"] for v in prim) for m in MODELS}
        N = len(prim); line = []
        for s in (0.25, 0.40):
            st = math.sqrt(0.15 ** 2 + (1.253 * s / math.sqrt(N)) ** 2); line.append(f"s={s}: sigma_tot {st:.3f}, R-H {abs(sep) / st:.1f}sig, L-fb {abs(sepL) / st:.1f}sig, F-flat {abs(sepF) / st:.1f}sig")
        fc[f"{br}|{fn}"] = dict(N=N, sep_RH=sep, sep_Lfb=sepL, sep_flat=sepF, floors=floors)
        P(f"{br} {fn}: N {N}; median required-baryon shift vs F-DESI: R-H {sep:+.3f} dex, L-fb {sepL:+.3f}, F-flat {sepF:+.3f}; FLOOR discs {floors}")
        P("     " + " | ".join(line) + "   (s = assumed per-disc scatter of Delta, a forecast assumption)")

# ---- GS4_24110 ----
P("\n=== GS4_24110 (RC100 GS3 15675), z 1.997, R = Re 7.39 kpc, V_c 206 (RC100, pressure-corrected) ===")
for lm in (10.89, 10.76):
    pr = predict(7.39, 206.0, 1.997, 10 ** lm, 7.39 / 1.678); res["GS4_24110"][str(lm)] = {f"{a}|{b}": c for (a, b), c in pr.items()}
    for fn in FOOT:
        P(f"  logM* {lm} {fn}: " + "; ".join(f"{m} logMbar,req {pr[(fn, m)]['logVbar2R_G']:.2f} Mgas,req(<-total, Rd/1.5Rd) {fmt(pr[(fn, m)]['logMgas_Rg=Rd'])}/{fmt(pr[(fn, m)]['logMgas_Rg=1.5Rd'])}" for m in MODELS))
P("  ΛCDM reference: RC100 fDM(Re) 0.56 -> baryons within Re = 0.44 V^2 Re/G = 10^%.2f (their decomposition)" % math.log10(0.44 * 206.0 ** 2 * 7.39 / G))

# ---- U4_27928 ----
z = 1.41933  # D_A from flat LCDM H0 70, Om 0.3 (angular size only)
from scipy.integrate import quad
dc = 2.99792458e5 / 70.0 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, z)[0] * 1e3; da = dc / (1 + z); Re = 0.49 / 206264.806 * da
P(f"\n=== U4_27928 (z {z}), conditional on the CO-measured V_c at R = 2 Re = {2 * Re:.1f} kpc (Re 0.49\" = {Re:.2f} kpc, D_A {da / 1e3:.0f} Mpc); logM* 10.74 ===")
P(f"{'V_c':>5} | " + " | ".join(f"{m:>22}" for m in MODELS) + "   (required total log M_gas Rg=Rd, canon/alt)")
for Vc in (150, 175, 200, 225, 250, 275, 300):
    pr = predict(2 * Re, float(Vc), z, 10 ** 10.74, Re / 1.678); res["U4_27928"][str(Vc)] = {f"{a}|{b}": c for (a, b), c in pr.items()}
    P(f"{Vc:5d} | " + " | ".join(f"{fmt(pr[('canon 9.36e-11', m)]['logMgas_Rg=Rd']) + '/' + fmt(pr[('alt 1.13e-10', m)]['logMgas_Rg=Rd']):>22}" for m in MODELS))

ratios = {m: {str(zz): MODELS[m](zz) for zz in (1.4, 1.6, 2.0)} for m in MODELS}
P("\nmodel a0(z)/a0(0): " + "; ".join(f"{m} " + "/".join(f"{v:.2f}" for v in r.values()) for m, r in ratios.items()) + "  (z 1.4/1.6/2.0)")
json.dump(dict(controls=CHK, ratios=ratios, forecast=fc, results=res), open(os.path.join(HERE, f"cfg571_prereg{TAG}_results.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg571_prereg{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    col = all(abs(v["sep_RH"]) < 0.01 for v in fc.values()); P(f"MUTATE (nu = 1): F-DESI vs R-H separation collapses -> {'detected (exit 1)' if col else 'NOT detected'}")
    open(os.path.join(HERE, f"cfg571_prereg{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if col else 0)
sys.exit(0 if all(ok for _, ok in CHK) else 1)
