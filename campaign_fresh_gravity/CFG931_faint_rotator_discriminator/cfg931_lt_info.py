"""CFG931 POST-HOC INFO (AMENDMENT_A2.md, f2fe987af; no class weight): LITTLE THINGS faint rotators, single point at R_max.
Oh+2015 table2 (CFG442/data, read only): g_obs = V(R_max)^2/R_max (asymmetric-drift corrected), g_bar = G (M_gas + M*_SED)/R_max^2
(all tabulated baryons inside R_max, spherical).  Compared, per 0.5-dex cell, with LITTLE THINGS M* >= split and with CFG880 dSphs
M* < split (CFG880 input slice exec'd read-only).  LITTLE THINGS is never pooled with SPARC (CFG442/449 overlap offsets).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg931_lt_info.py  -> cfg931_lt_info.out / cfg931_lt_info.json.
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import io, json, math, glob, contextlib, builtins, warnings
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
for _e in ("CFG880_MUTATE", "MUTATE"): os.environ.pop(_e, None)
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOTS = ("canonical", "alt"); LN10 = math.log(10.0)
G, MSUN, PC, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19
GRID = np.arange(-20.0, 10.0001, 0.5); CELLS = (15, 16, 17); SPLITS = (1e7, 3e7, 1e8); FLOOR = 0.05; NBOOT = 4000
nu_e15 = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
RES = dict(lane="CFG931", part="POST-HOC INFO (AMENDMENT A2)", criteria="cad92ca1c", amendment_A2="f2fe987af", checks={})
P("CFG931 POST-HOC INFO (A2; no class weight): LITTLE THINGS single point at R_max vs LT M*>=split vs CFG880 dSphs, matched 0.5-dex cells")

# ---------------------------------------------------------------- LITTLE THINGS (Oh+2015)
D442 = os.path.join(LANES, "CFG442_a0_rung_expansion", "data")
DIST = {}
for l in builtins.open(os.path.join(D442, "oh15_table1.dat")):
    if l.strip():
        f = l.split("|"); DIST[f[0].strip().replace("_", "")] = float(f[2])
LT = []
for l in builtins.open(os.path.join(D442, "oh15_table2.dat")):
    if not l.strip(): continue
    f = l.split("|"); assert len(f) == 29, (len(f), l[:20])
    num = lambda s: float(s) if s.strip() else None
    nm = f[0].strip().replace("_", ""); Rmax, V = float(f[1]), float(f[3]); Mgas, MK, MSED = num(f[-5]), num(f[-4]), num(f[-3])
    LT.append(dict(name=nm, Rmax=Rmax, V=V, Mgas=Mgas * 1e7, MSED=None if MSED is None else MSED * 1e7, D=DIST[nm]))
ok_parse = (next(r for r in LT if r["name"] == "CVnIdwA")["Mgas"] == 2.91e7 and abs(next(r for r in LT if r["name"] == "CVnIdwA")["MSED"] - 4.9e6) < 1
            and next(r for r in LT if r["name"] == "DDO43")["MSED"] is None)
RES["checks"]["parse"] = ok_parse; P(f"  [{'PASS' if ok_parse else 'FAIL'}] Oh+2015 table2 parse (CVn I dwA M_gas 2.91e7, M*_SED 4.9e6; DDO 43 no M*_SED); {len(LT)} galaxies")
LTU = [r for r in LT if r["MSED"] is not None]
for r in LTU:
    Rm = r["Rmax"] * KPC; r["gb"] = G * (r["Mgas"] + r["MSED"]) * MSUN / Rm ** 2; r["go"] = (r["V"] * 1e3) ** 2 / Rm; r["lg"] = math.log10(r["gb"])
    r["cell"] = int(np.digitize(r["lg"], GRID) - 1)
    for f_ in FOOTS: r[f"D_{f_}"] = math.log10(r["go"] / (r["gb"] * float(nu_e15(r["gb"] / A0[f_]))))
P(f"  usable (with M*_SED): {len(LTU)}; left out (no M*_SED): {sorted(r['name'] for r in LT if r['MSED'] is None)}")

# ---------------------------------------------------------------- CFG880 dSphs (read-only slice), K-check vs the main run
F880 = os.path.join(LANES, "CFG880_clump_sigma_universality", "cfg880.py")
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"): raise PermissionError(f"refusing to write {file!r}")
    return builtins.open(file, mode, *a, **k)
N880 = {"__file__": F880, "__name__": "cfg880_inputs_ro", "open": _ro_open}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(builtins.open(F880).read().split("# ---------------- hierarchical likelihood ----------------", 1)[0], F880, "exec"), N880)
DW = {}
for f_ in FOOTS:
    A = N880["arrays"](N880["SAMP"], A0[f_]); law = np.sqrt(A["sl2"]); s = A["s"]; e = np.where(s > law, A["em"], A["ep"]); rows = []
    for j, (nm, r12pc) in enumerate(zip(A["names"], A["r12"])):
        L = N880["LVD"][nm]; Ms = 2.0 * 10 ** (0.4 * (4.83 - N880["fnum"](L["M_V"])))
        Mg = N880["gas_in"](N880["fnum"](L.get("mass_HI")), r12pc); gN = N880["G"] * (Ms / 2 + Mg) * N880["Msun"] / (r12pc * N880["PC"]) ** 2
        rows.append(dict(name=nm, Ms=Ms, lg=math.log10(gN), cell=int(np.digitize(math.log10(gN), GRID) - 1), D=2 * math.log10(s[j] / law[j]), sD=2 * e[j] / (s[j] * LN10)))
    DW[f_] = rows
kc = [float(np.mean([d["D"] for d in DW["canonical"] if d["Ms"] < 1e7 and d["cell"] == c])) for c in (15, 16)]
okk = abs(kc[0] - 0.318) <= 1e-3 and abs(kc[1] - 0.216) <= 1e-3
RES["checks"]["K_dsph_cells"] = dict(ok=okk, values=kc)
P(f"  [{'PASS' if okk else 'FAIL'}] K: CFG880 dSph cell means at split 1e7 (canonical) {kc[0]:+.3f} / {kc[1]:+.3f} vs main run +0.318 / +0.216")
if not (ok_parse and okk):
    P("  a check failed: no INFO numbers reported"); json.dump(RES, builtins.open(os.path.join(HERE, "cfg931_lt_info.json"), "w"), indent=1)
    builtins.open(os.path.join(HERE, "cfg931_lt_info.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(2)

# ---------------------------------------------------------------- per-galaxy list
P("\n  LITTLE THINGS galaxies (Oh+2015; single point at R_max): name, M*_SED, M_gas, R_max kpc, V(R_max), log g_bar, Delta canonical / alt")
for r in sorted(LTU, key=lambda r: r["MSED"]):
    P(f"    {r['name']:9s} {r['MSED']:.1e} {r['Mgas']:.1e} {r['Rmax']:5.2f} {r['V']:6.1f}  {r['lg']:6.2f}  {r['D_canonical']:+.2f} / {r['D_alt']:+.2f}")
RES["lt_galaxies"] = LTU

# ---------------------------------------------------------------- cells and within-LT differences
def boot(vals, w, cells_of, rng):
    """vals: list of (cell index into w, value); bootstrap the system list, weighted cell means."""
    n = len(vals); ci = np.array([v[0] for v in vals]); x = np.array([v[1] for v in vals]); idx = rng.integers(0, n, (NBOOT, n))
    out = np.empty(NBOOT)
    for t in range(NBOOT):
        cc, xx = ci[idx[t]], x[idx[t]]; m = np.array([xx[cc == j].mean() if np.any(cc == j) else np.nan for j in range(len(w))])
        ok = np.isfinite(m); out[t] = np.sum(m[ok] * w[ok]) / w[ok].sum()
    return out
INFO = {}
for f_ in FOOTS:
    for sp in SPLITS:
        key = f"{f_}|{sp:.0e}"; gi = [r for r in LTU if r["MSED"] < sp]; gii = [r for r in LTU if r["MSED"] >= sp]; giii = [d for d in DW[f_] if d["Ms"] < sp]
        cellrows = {}
        for c in CELLS:
            a = [r[f"D_{f_}"] for r in gi if r["cell"] == c]; b = [r[f"D_{f_}"] for r in gii if r["cell"] == c]; d = [x["D"] for x in giii if x["cell"] == c]
            cellrows[str(c)] = dict(n_i=len(a), E_i=float(np.mean(a)) if a else None, n_ii=len(b), E_ii=float(np.mean(b)) if b else None,
                                    n_iii=len(d), E_iii=float(np.mean(d)) if d else None, names_i=[r["name"] for r in gi if r["cell"] == c])
        el = [c for c in CELLS if cellrows[str(c)]["n_i"] >= 1 and cellrows[str(c)]["n_ii"] >= 1 and cellrows[str(c)]["n_iii"] >= 3]
        res = dict(cells=cellrows, eligible=el)
        if el:
            w = np.array([cellrows[str(c)]["n_i"] for c in el], float); w /= w.sum(); rng = np.random.default_rng(9313)
            vi = [(el.index(r["cell"]), r[f"D_{f_}"]) for r in gi if r["cell"] in el]; vii = [(el.index(r["cell"]), r[f"D_{f_}"]) for r in gii if r["cell"] in el]
            viii = [(el.index(x["cell"]), x["D"]) for x in giii if x["cell"] in el]
            E = lambda v: float(sum(w[j] * np.mean([x for jj, x in v if jj == j]) for j in range(len(el))))
            Ei, Eii, Eiii = E(vi), E(vii), E(viii)
            bi, bii, biii = boot(vi, w, el, rng), boot(vii, w, el, rng), boot(viii, w, el, rng)
            meas = math.sqrt(sum(w[j] ** 2 * sum(x["sD"] ** 2 for x in giii if x["cell"] == c) / cellrows[str(c)]["n_iii"] ** 2 for j, c in enumerate(el)))
            si, sii, siii = float(np.std(bi, ddof=1)), float(np.std(bii, ddof=1)), max(float(np.std(biii, ddof=1)), meas)
            dK, dE = Ei - Eii, Eiii - Ei; sK = math.sqrt(si ** 2 + sii ** 2 + 2 * FLOOR ** 2); sE = math.sqrt(siii ** 2 + si ** 2 + 2 * FLOOR ** 2)
            sL = math.sqrt(siii ** 2 + sii ** 2 + 2 * FLOOR ** 2)
            res.update(N_i=len(vi), N_ii=len(vii), N_iii=len(viii), E_i=Ei, E_ii=Eii, E_iii=Eiii, d_K=dK, s_K=sK, z_K=dK / sK, d_E=dE, s_E=sE, z_E=dE / sE,
                       lever=Eiii - Eii, s_lever=sL, z_lever=(Eiii - Eii) / sL)
        INFO[key] = res
        P(f"\n  [{f_} | split {sp:.0e}] cells (n / mean Delta: LT M*<split | LT M*>=split | dSph M*<split):")
        for c in CELLS:
            v = cellrows[str(c)]; fm = lambda n, e: f"{n:2d} / {('%+.3f' % e) if e is not None else '  -   '}"
            P(f"    [{GRID[c]:.1f},{GRID[c] + 0.5:.1f}): {fm(v['n_i'], v['E_i'])} | {fm(v['n_ii'], v['E_ii'])} | {fm(v['n_iii'], v['E_iii'])}   (i: {', '.join(v['names_i']) or '-'})")
        if el:
            P(f"    within-LT over cells {[f'[{GRID[c]:.1f},{GRID[c] + 0.5:.1f})' for c in el]}: N {res['N_i']}/{res['N_ii']}/{res['N_iii']}  E(i) {res['E_i']:+.3f} E(ii) {res['E_ii']:+.3f} "
              f"E(iii) {res['E_iii']:+.3f}  d_K {res['d_K']:+.3f}+-{res['s_K']:.3f} (z {res['z_K']:+.1f})  d_E {res['d_E']:+.3f}+-{res['s_E']:.3f} (z {res['z_E']:+.1f})  "
              f"lever {res['lever']:+.3f}+-{res['s_lever']:.3f} (z {res['z_lever']:+.1f})   [INFO, no class]")
        else:
            P("    no cell holds all three groups (>= 1 / >= 1 / >= 3)")
RES["cells"] = INFO

# ---------------------------------------------------------------- overlap rows (LT single point vs SPARC)
QD = {}
for l in builtins.open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: QD[v[0]] = float(v[2])
        except ValueError: pass
def sparc_pts(name, cut):
    pts = []
    for l in builtins.open(os.path.join(REPO, "real_research", "data", "sparc_data", f"{name}_rotmod.dat")):
        if l.startswith("#") or not l.strip(): continue
        R, V, eV, Vg, Vd, Vb = [float(x) for x in l.split()[:6]]
        if V <= 0 or R <= 0 or (cut and eV / V >= 0.10): continue
        gb = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPC)
        if gb > 0: pts.append((R, gb, V * V * 1e6 / (R * KPC)))
    return pts
P("\n  Overlap rows (INFO): LT single-point Delta vs SPARC Delta at the angular-matched radius R_max * D_SPARC/D_Oh, and SPARC's last point")
OV = {}
for lt_name, sp_name, cut in (("DDO154", "DDO154", True), ("DDO168", "DDO168", True), ("WLM", "UGCA444", False)):
    r = next(x for x in LTU if x["name"] == lt_name); pts = sparc_pts(sp_name, cut); Rt = r["Rmax"] * QD[sp_name] / r["D"]
    near = min(pts, key=lambda p: abs(p[0] - Rt)); last = max(pts, key=lambda p: p[0]); row = {}
    for f_ in FOOTS:
        dd = lambda p: math.log10(p[2] / (p[1] * float(nu_e15(p[1] / A0[f_]))))
        row[f_] = dict(LT=r[f"D_{f_}"], LT_lgbar=r["lg"], SPARC_near=dd(near), SPARC_near_R=near[0], SPARC_near_lgbar=math.log10(near[1]), SPARC_last=dd(last),
                       SPARC_last_lgbar=math.log10(last[1]))
    OV[lt_name] = row; c_ = row["canonical"]
    P(f"    {lt_name:7s} (SPARC {sp_name}{'' if cut else ', no point cut'}): LT {c_['LT']:+.2f} at log g_bar {c_['LT_lgbar']:.2f} | SPARC near R {c_['SPARC_near_R']:.2f} kpc "
      f"{c_['SPARC_near']:+.2f} at {c_['SPARC_near_lgbar']:.2f} | SPARC last {c_['SPARC_last']:+.2f} at {c_['SPARC_last_lgbar']:.2f}  (canonical)")
RES["overlap"] = OV
P("\n  INFO only: no class weight; LITTLE THINGS never pooled with SPARC; kappa = 1/2 FITTED; footings never pooled; not theory closed.")
json.dump(RES, builtins.open(os.path.join(HERE, "cfg931_lt_info.json"), "w"), indent=1, default=float)
builtins.open(os.path.join(HERE, "cfg931_lt_info.out"), "w").write("\n".join(OUT) + "\n")
