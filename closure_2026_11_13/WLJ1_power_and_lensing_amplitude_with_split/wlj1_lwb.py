#!/usr/bin/env python3
"""WLJ1 (FROZEN_CRITERIA.md, 03f9823de7) part 5: gates G-LWB1 and G-LWB1R (DESI DR1 Lensing Without Borders, Delta Sigma + wp, J label)
for REF, ADOPT and SPLIT.
  lwb1:  LWB1's lwb1.py executed UNCHANGED from its own folder up to its "primary and brackets" marker (data, model, transforms, fit,
         label); its global HM (CO1's stored R_tot) is replaced by each case's z = 0 R_tot. Primary (five vectors) and pi_max 80 / 100
         (gating) for every case; LWB1's other brackets (pi_max 300, point mass, R_min 5 / 12, no magnification column, wp correlation
         0.5, N = 1) for REF, ADOPT and SPLIT f = 2. The CAMB halofit bracket is left out.
  lwb1r: LWB1R's lwb1r.py executed UNCHANGED from its own folder as a module without its main() call; its global CO1 is replaced by
         each case's; main()'s inner proj_set / tmpl / fit_all are COPIED (cited). NPROC is set to 1 (one worker; the projection
         code is LWB1R's). Primary (five vectors) and pi_max 80 / 100 for every case; point mass and R_min 5 / 12 for REF, ADOPT, S2.
  nice -n 10 python3 -I -B wlj1_lwb.py <lwb1|lwb1r>  -> wlj1_lwb_<which>.json / .out  (twins under "twins")
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, types
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
import multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WHICH = sys.argv[1]; assert WHICH in ("lwb1", "lwb1r")
OUT = []; T0 = time.time()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
HM = json.load(open(os.path.join(HERE, "wlj1_hm.json"))); MU = json.load(open(os.path.join(HERE, "wlj1_hm_MUTATE.json")))
FOOTS = ("canonical", "alt")
def rtot(cs, ft):
    if cs == "REF": return HM["cases"][f"ADOPT|{ft}|0.0"]["R_bar"]
    if cs == "TWL":
        a = HM["cases"][f"S2|{ft}|0.0"]; return (np.array(a["R_bar"]) * (1 + 2 * (np.array(a["R_cold"]) - 1))).tolist()
    if cs == "TWB": return MU["TWB"][f"TWB|{ft}|0.0"]["R_tot"]
    return HM["cases"][f"{cs}|{ft}|0.0"]["R_tot"]
def fake_co1(cs): return dict(k=HM["k"], primary={ft: dict(R_tot=rtot(cs, ft)) for ft in FOOTS})
CASES = ["REF", "ADOPT", "S1.25", "S2", "S3", "Sinf", "TWB", "TWL"]; FULLBR = ("REF", "ADOPT", "S2")
RES = dict(lane="WLJ1", part=f"G-{WHICH.upper()}", criteria="03f9823de7", rows={}, KA={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")

if WHICH == "lwb1":
    SRC = os.path.join(REPO, "closure_2026_11_12", "LWB1_lensing_amplitude_crosscheck", "lwb1.py"); code = open(SRC).read()
    cut = code.index("# ------------------------------------------------------------------ primary and brackets")
    os.environ.pop("LWB1_MUTATE", None)
    NS = {"__file__": SRC, "__name__": "lwb1_lib"}; exec(compile(code[:cut], SRC, "exec"), NS)
    os.environ.update({v: "1" for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS")})
    vector, templates, scan, label, VEC, TGT = (NS[k] for k in ("vector", "templates", "scan", "label", "VEC", "TGT"))
    STORED = json.load(open(os.path.join(os.path.dirname(SRC), "lwb1.json")))
    assert np.allclose(NS["KH"], HM["k"])
    VV = {nm: vector(sv) for nm, sv in VEC.items()}
    for cs in CASES:
        NS["HM"] = fake_co1(cs)
        for ft in FOOTS:
            T40 = templates(ft, "pair", 40.0); row = dict(primary={}, brackets={})
            for nm, V in VV.items():
                r = scan(V, T40, TGT[ft]); r["label"] = label(r); row["primary"][nm] = r
            for pm_ in ((80.0, 100.0, 300.0) if cs in FULLBR else (80.0, 100.0)):
                T = templates(ft, "pair", pm_); r = scan(VV["J"], T, TGT[ft]); r["label"] = label(r); row["brackets"][f"pimax_{int(pm_)}"] = {"J": r}
            if cs in FULLBR:
                br = row["brackets"]
                br["point_mass"] = {"J": scan(VV["J"], T40, TGT[ft], pm=True)}
                for rm in (5.0, 12.0): br[f"rmin_{int(rm)}"] = {"J": scan(vector(VEC["J"], rmin=rm), T40, TGT[ft])}
                br["no_magnification_column"] = {"J": scan(vector(VEC["J"], use_mb=False), T40, TGT[ft])}
                br["wp_corr_0p5"] = {"J": scan(vector(VEC["J"], wpcorr=0.5), T40, TGT[ft])}
                Tl = templates(ft, "linear", 40.0); br["N_equals_1"] = {"J": scan(VV["J"], Tl, TGT[ft])}
                for v_ in br.values():
                    for r in v_.values(): r["label"] = label(r)
            RES["rows"][f"{cs}|{ft}"] = row
            j = row["primary"]["J"]
            P(f"  [{ft}] {cs:6s} J {j['best_sigma8']:.4f} +- {j['width']:.4f} gap {j['gap']:+.3f} p {j['p']:.3f} -> {j['label']}; " + "; ".join(f"{nm} {r['gap']:+.2f}" for nm, r in row["primary"].items() if nm != "J")
              + "; brackets J " + " ".join(f"{b}:{v['J']['gap']:+.2f}" for b, v in row["brackets"].items()) + f"   [{time.time() - T0:.0f} s]")
    for ft in FOOTS:
        a = RES["rows"][f"ADOPT|{ft}"]; s = STORED
        dd = [abs(a["primary"][nm]["best_sigma8"] - s["primary"][ft][nm]["best_sigma8"]) for nm in VEC] + [abs(a["brackets"][f"pimax_{p}"]["J"]["best_sigma8"] - s["brackets"][ft][f"pimax_{p}"]["J"]["best_sigma8"]) for p in (80, 100)]
        dg = [abs(a["primary"][nm]["gap"] - s["primary"][ft][nm]["gap"]) for nm in VEC]
        RES["KA"][f"KA_G7_{ft}"] = dict(max_d_sigma8=max(dd), max_d_gap=max(dg), pass_=bool(max(dd) <= 0.0005 and max(dg) <= 0.01))
        P(f"KA-G7 [{ft}] ADOPT against LWB1's stored rows: {RES['KA'][f'KA_G7_{ft}']}")
else:
    mp.set_start_method("fork", force=True)
    SRC = os.path.join(REPO, "closure_2026_11_12", "LWB1R_blind_lensing_regrade", "lwb1r.py"); code = open(SRC).read()
    mod = types.ModuleType("lwb1r_lib"); mod.__file__ = SRC; sys.modules["lwb1r_lib"] = mod
    exec(compile(code, SRC, "exec"), mod.__dict__)                 # __name__ is "lwb1r_lib": main() is not called
    NS = mod.__dict__; NS["NPROC"] = 1
    STORED = json.load(open(os.path.join(os.path.dirname(SRC), "lwb1r.json")))
    build_points, load_wp, cov_for, Proj, xi_of, Fit, label, growth_fns, P_formB, LENS, VECTORS, RG, FOOT, KK, RHO_CRIT = (NS[k] for k in (
        "build_points", "load_wp", "cov_for", "Proj", "xi_of", "Fit", "label", "growth_fns", "P_formB", "LENS", "VECTORS", "RG", "FOOT", "KK", "RHO_CRIT"))
    pts = build_points(); wps = load_wp()
    zL = {li: float(np.mean([p['zl'] for p in pts if p['lens'] == li])) for li in range(len(LENS))}
    C_all = cov_for(pts)
    # ---- copied from lwb1r.py main(): proj_set, tmpl, fit_all
    def proj_set(Pf, rho):
        return {li: Proj(RG, xi_of(Pf(zL[li]), RG), rho) for li in range(len(LENS))}
    def tmpl(projs, plist, wl, pimax, rpcol=False):
        tds = [projs[p['lens']].ds_at(p['rp']) if rpcol else projs[p['lens']].ds_bin(p['r1'], p['r2']) for p in plist]
        twp = [projs[w['lens']].wp_parts(w['rp'], pimax) for w in wl]
        return tds, twp
    def fit_all(projs, s8t, fz, plist=None, wl=None, C=None, pimax=40.0, rpcol=False, vecs=None, **kw):
        plist = pts if plist is None else plist; wl = wps if wl is None else wl; C = C_all if C is None else C
        tds, twp = tmpl(projs, plist, wl, pimax, rpcol)
        res = {}
        for v, sv in VECTORS.items():
            if vecs is not None and v not in vecs: continue
            ii = [i for i, p in enumerate(plist) if p['surv'] in sv]
            lens_in = sorted(set(plist[i]['lens'] for i in ii))
            wi = [j for j, w in enumerate(wl) if w['lens'] in lens_in]
            F = Fit([plist[i] for i in ii], C[np.ix_(ii, ii)], [wl[j] for j in wi], [tds[i] for i in ii], [twp[j] for j in wi], fz, s8t, **kw)
            r = F.run(); r['gap'], r['label'] = label(r, s8t); res[v] = r
        return res
    for cs in CASES:
        NS["CO1"] = fake_co1(cs)
        for ft in FOOTS:
            s8t, Om = FOOT[ft]['s8'], FOOT[ft]['Om']; rho = Om * RHO_CRIT
            D, f = growth_fns(Om); fz = {li: f(zL[li]) for li in range(len(LENS))}
            projs = proj_set(lambda z: P_formB(z, ft), rho)
            row = dict(primary=fit_all(projs, s8t, fz), brackets={})
            for pm in (80.0, 100.0): row["brackets"][f"pimax_{int(pm)}"] = fit_all(projs, s8t, fz, pimax=pm, vecs=("J",))
            if cs in FULLBR:
                row["brackets"]["pointmass"] = fit_all(projs, s8t, fz, pm=True, vecs=("J",))
                for rmin in (5.0, 12.0):
                    pl = build_points(rmin=rmin); row["brackets"][f"Rmin_{int(rmin)}"] = fit_all(projs, s8t, fz, plist=pl, C=cov_for(pl), vecs=("J",))
            RES["rows"][f"{cs}|{ft}"] = row
            j = row["primary"]["J"]
            P(f"  [{ft}] {cs:6s} J {j['best']:.4f} +- {j['width']:.4f} gap {j['gap']:+.3f} p {j['p']:.3f} -> {j['label']}; " + "; ".join(f"{nm} {r['gap']:+.2f}" for nm, r in row["primary"].items() if nm != "J")
              + "; brackets J " + " ".join(f"{b}:{v['J']['gap']:+.2f}" for b, v in row["brackets"].items()) + f"   [{time.time() - T0:.0f} s]")
    for ft in FOOTS:
        a = RES["rows"][f"ADOPT|{ft}"]; s = STORED["foot"][ft]
        dd = [abs(a["primary"][v]["best"] - s["primary"][v]["best"]) for v in VECTORS] + [abs(a["brackets"][f"pimax_{p}"]["J"]["best"] - s[f"pimax_{p}"]["J"]["best"]) for p in (80, 100)]
        dg = [abs(a["primary"][v]["gap"] - s["primary"][v]["gap"]) for v in VECTORS]
        RES["KA"][f"KA_G8_{ft}"] = dict(max_d_sigma8=max(dd), max_d_gap=max(dg), pass_=bool(max(dd) <= 0.0005 and max(dg) <= 0.01))
        P(f"KA-G8 [{ft}] ADOPT against LWB1R's stored rows: {RES['KA'][f'KA_G8_{ft}']}")
RES["KA_ok"] = bool(all(v["pass_"] for v in RES["KA"].values()))
P(f"Known answers pass: {RES['KA_ok']}   ({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, f"wlj1_lwb_{WHICH}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"wlj1_lwb_{WHICH}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
