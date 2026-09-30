#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""CFG193_a_velocities -- R1 (sample), R2 (velocity chain), A1/A5 parts, the sigma_u table, the u table.
Own code.  Outputs: CFG193_a_velocities.out, CFG193_a_velocities_results.json, CFG193_utable.csv, CFG193_utable.npz.
Rerun: ZF_REPO=<repo> python3 CFG193_a_velocities.py   (< 1 min).  Exit 0 if all own checks pass, 2 otherwise."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG193_common import *

T = Tee(os.path.join(HERE, "CFG193_a_velocities.out"))
P = T.p
P("CFG193_a_velocities  (repo = <repo>)")
gal = load_sparc()
P("SPARC rotmod files with a master-table row:", len(gal))
raw = raw_count(gal)
c1 = clean_sample(gal, "U1")
c2 = clean_sample(gal, "U2")
def bymethod(lst):
    d = {}
    for g in lst:
        d[g["meta"]["fD"]] = d.get(g["meta"]["fD"], 0) + 1
    return dict(sorted(d.items()))
P("R1  raw (Q<=2 & Inc>=30, no point cut):", len(raw), bymethod(raw))
P("R1  clean U1 (>=5 finite points with R,V,eV>0):", len(c1), bymethod(c1))
P("R1  clean U2 (U1 and total baryonic V^2 > 0 at fiducial Upsilon):", len(c2), bymethod(c2))
removed = [g["name"] + "(fD=%d,n=%d)" % (g["meta"]["fD"], int(usable_mask(g).sum())) for g in raw if g not in c1]
P("R1  removed by the >=5-usable-points cut:", removed)
few = sorted([(int(usable_mask(g).sum()), g["name"], g["meta"]["fD"]) for g in raw])[:8]
P("R1  the 8 raw galaxies with the fewest usable points:", few)

pos = load_positions()
ned = load_ned()
cats = load_catalogues()
P("positions:", len(pos), " NED cz:", len(ned))
tab = build_table(gal, ned, pos, cats)
src = {}
for nm, t in tab.items():
    src[t["src"]] = src.get(t["src"], 0) + 1
P("velocity sources (all 175 with a position; first available):", dict(sorted(src.items(), key=lambda kv: str(kv[0]))))
nov = [g["name"] for g in gal if g["name"] not in tab or tab[g["name"]]["cz_hel"] is None]
P("no velocity (listed, dropped):", nov)
# overlaps
dv, big = [], []
for nm, t in tab.items():
    c = t["cand"]
    for j in range(1, len(c)):
        d = c[j][1] - c[0][1]
        dv.append(abs(d))
        if abs(d) > 50:
            big.append((nm, c[0][0], c[0][1], c[j][0], c[j][1], round(c[j][2], 2)))
P("source overlap: n pairs %d, median |dv| = %.1f km/s" % (len(dv), float(np.median(dv)) if dv else float("nan")))
P("|dv| > 50 km/s (flagged; the primary fit is rerun without them):", big)
# KT2017 group check
P("KT2017 groups whose members carry different HRV (check printed):", sum(1 for v in cats["KT2017"][4].values() if v), "of", len(cats["KT2017"][4]))

prim = [g for g in c1 if g["meta"]["fD"] in (2, 3, 4, 5) and g["name"] in tab and tab[g["name"]]["cz_hel"] is not None]
hf = [g for g in c1 if g["meta"]["fD"] == 1 and g["name"] in tab and tab[g["name"]]["cz_hel"] is not None]
P("PRIMARY (clean, f_D in 2..5, with a velocity):", len(prim), bymethod(prim))
P("Hubble-flow clean with a velocity (CIRCULAR rows only):", len(hf))
P("primary galaxies of the 68-set lacking a velocity:", [g["name"] for g in c1 if g["meta"]["fD"] in (2, 3, 4, 5) and g not in prim])

def uvals(g, h0=H0_PRIMARY, vsun=(V_SUN, SUN_L, SUN_B), **kw):
    t = tab[g["name"]]
    zc = cmb_convert(t["cz_hel"], t["l"], t["b"], *vsun)
    D = g["meta"]["D"]
    return float(u_los(zc, D, h0, **kw)), float(zc)

rows = []
allg = prim + hf
names = [g["name"] for g in allg]
arr = {k: [] for k in ("u", "u73", "u70", "ulum", "ulin", "uplanck", "sig_u", "zcmb", "cz", "l", "b", "D", "eD", "fD", "ucosz2")}
for g in allg:
    t = tab[g["name"]]
    u, zc = uvals(g)
    D, eD = g["meta"]["D"], g["meta"]["eD"]
    uhi = float(u_los(zc, D + eD)); ulo = float(u_los(zc, max(D - eD, 0.3 * D)))
    arr["u"].append(u); arr["u73"].append(uvals(g, 73.0)[0]); arr["u70"].append(uvals(g, 70.0)[0])
    arr["ulum"].append(uvals(g, dist="luminosity")[0]); arr["ulin"].append(uvals(g, linear=True)[0])
    arr["uplanck"].append(uvals(g, vsun=V_SUN_ALT)[0])
    arr["sig_u"].append(0.5 * abs(ulo - uhi))
    arr["zcmb"].append(zc); arr["cz"].append(t["cz_hel"]); arr["l"].append(t["l"]); arr["b"].append(t["b"])
    arr["D"].append(D); arr["eD"].append(eD); arr["fD"].append(g["meta"]["fD"])
A = {k: np.array(v, float) for k, v in arr.items() if k != "ucosz2"}
np.savez(os.path.join(HERE, "CFG193_utable.npz"), names=np.array(names), **A)
with builtins.open(os.path.join(HERE, "CFG193_utable.csv"), "w") as f:
    f.write("name,fD,D_Mpc,eD_Mpc,source,cz_hel,l_deg,b_deg,zcmb,u_67.66,u_70,u_73,u_lumdist,u_linear,u_planckvsun,sigma_u,z_W1,sample\n")
    for i, g in enumerate(allg):
        f.write("%s,%d,%.3f,%.3f,%s,%.1f,%.3f,%.3f,%.6f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.4f,%s\n" % (
            g["name"], A["fD"][i], A["D"][i], A["eD"][i], tab[g["name"]]["src"], A["cz"][i], A["l"][i], A["b"][i], A["zcmb"][i], A["u"][i],
            A["u70"][i], A["u73"][i], A["ulum"][i], A["ulin"][i], A["uplanck"][i], A["sig_u"][i], (A["u"][i] / W_REF) ** 2,
            "primary" if g in prim else "HF"))
n = len(prim)
u = A["u"][:n]
P("--- u for the primary galaxies (H0 = 67.66, comoving D, relativistic) ---")
P("|u| min/median/max: %.1f / %.1f / %.1f km/s;  z = (u/600)^2 min/median/max: %.4f / %.4f / %.4f" % (
    np.min(np.abs(u)), np.median(np.abs(u)), np.max(np.abs(u)), np.min((u / 600) ** 2), np.median((u / 600) ** 2), np.max((u / 600) ** 2)))
z = (u / W_REF) ** 2
P("rms(z - mean z) = %.4f  (R6 target window [0.22, 0.33])" % float(np.std(z)))
for k, lab in ((2, "TRGB"), (3, "Cepheid"), (4, "UMa"), (5, "SNIa")):
    m = A["fD"][:n] == k
    if m.any():
        P("  %-8s N=%2d  median sigma_u = %.1f km/s   median |u| = %.1f   D range %.1f-%.1f Mpc" % (lab, m.sum(), np.median(A["sig_u"][:n][m]), np.median(np.abs(u[m])), A["D"][:n][m].min(), A["D"][:n][m].max()))
P("--- A1: how far each velocity-construction variant moves u (primary 68) ---")
variants = {}
for key, lab in (("u73", "H0 = 73"), ("u70", "H0 = 70"), ("ulum", "D as luminosity distance"), ("ulin", "linear cz = H0 D"), ("uplanck", "Planck v_sun (369.82, 264.021, 48.253)")):
    d = A[key][:n] - u
    variants[key] = dict(max_abs=float(np.max(np.abs(d))), median=float(np.median(d)), rms=float(np.sqrt(np.mean(d ** 2))))
    P("  %-42s max|du| = %6.1f  median du = %6.1f  rms = %6.1f km/s" % (lab, np.max(np.abs(d)), np.median(d), np.sqrt(np.mean(d ** 2))))
lad = 5.3 * A["D"][:n]
P("  ladder scale (u shift of the H0=67.66 vs a 73-scale ladder = +5.3 D km/s):  max %.1f  median %.1f km/s" % (lad.max(), np.median(lad)))
# A3/A4 parts: LG projection
n_hat = np.array([unit(l, b) for l, b in zip(A["l"], A["b"])])
vlg = V_LG * unit(LG_L, LG_B)
proj = n_hat @ vlg if False else np.einsum("ij,j->i", n_hat, vlg)
r_all = float(np.corrcoef(u, proj[:n])[0, 1])
P("--- A3/A4 (velocity part): r(u, V_LG.n) over the primary 68 = %.3f  (README 0.76; window 0.71-0.81)" % r_all)
P("  v_sun,CMB - v_sun,LG check is not repeated (values from memory, S5).  |V_LG.n| median %.0f km/s" % np.median(np.abs(proj[:n])))
lv = A["D"][:n] < 8.0
P("  Local Volume (D < 8 Mpc): %d of %d;  r(u, V_LG.n) there = %.3f; rms(u - V_LG.n) there = %.1f km/s" % (
    lv.sum(), n, float(np.corrcoef(u[lv], proj[:n][lv])[0, 1]) if lv.sum() > 3 else float("nan"), float(np.sqrt(np.mean((u[lv] - proj[:n][lv]) ** 2)))))
P("  Ursa Major (f_D=4) median u = %.1f km/s, spread %.1f km/s (std)" % (np.median(u[A['fD'][:n] == 4]), np.std(u[A['fD'][:n] == 4])))
# A5: dv>50 galaxies inside the primary
bign = set(b[0] for b in big)
P("A5  flagged velocity-source disagreements inside the primary:", sorted(bign & set(names[:n])))
P("A5  the gross-mismatch galaxy UGC01281: candidates", tab.get("UGC01281", {}).get("cand"))
# checks
T.check("R1 velocity tables read; 175 SPARC galaxies", len(gal) == 175, "n=%d" % len(gal))
T.check("finite u for every primary galaxy", np.all(np.isfinite(u)), "")
_zz, _dc = __import__("CFG193_common")._comoving_table(H0_PRIMARY, OM)
T.check("z_cos inversion consistent (D_C(z_cos(D)) = D to 1e-3 Mpc)", abs(float(np.interp(float(z_cos(20.0)), _zz, _dc)) - 20.0) < 1e-3, "")
res = dict(raw=len(raw), raw_by_method=bymethod(raw), clean_U1=len(c1), clean_U1_by_method=bymethod(c1), clean_U2=len(c2), clean_U2_by_method=bymethod(c2),
           removed_by_point_cut=removed, sources=src, no_velocity=nov, n_overlap=len(dv), median_overlap_dv=float(np.median(dv)) if dv else None,
           big_dv=big, primary=len(prim), primary_by_method=bymethod(prim), hubble_flow_with_velocity=len(hf),
           rms_z=float(np.std(z)), abs_u_min_med_max=[float(np.min(np.abs(u))), float(np.median(np.abs(u))), float(np.max(np.abs(u)))],
           sigma_u_median={lab: float(np.median(A["sig_u"][:n][A["fD"][:n] == k])) for k, lab in ((2, "TRGB"), (3, "Cepheid"), (4, "UMa"), (5, "SNIa")) if (A["fD"][:n] == k).any()},
           variants=variants, r_u_VLGn=r_all, local_volume_count=int(lv.sum()))
jdump(res, os.path.join(HERE, "CFG193_a_velocities_results.json"))
bad = T.failed_load()
P("verdict: %d/%d checks pass; load-bearing failures: %d" % (sum(1 for c in T.checks if c[1]), len(T.checks), len(bad)))
sys.exit(2 if bad else 0)
