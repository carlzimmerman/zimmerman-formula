#!/usr/bin/env python3
"""FN4c stage 2: the law's KiDS lensing gap on the rebuilt lens inventory, through LE1's G1 (A30) and G3 (CX1 lensing line).

Criteria: FROZEN_CRITERIA.md (d62a6b6b53). Runs because stage 1 reads REBUILD MATCHES (fn4c_rebuild.json).
The graders are LE1's calls on CRG1/RQ3/NP1/CX1 modules, loaded read-only exactly as LE1 does
(rebuild_2026_10_22/LE1_lensing_estimator_audit/le1.py: crg(), class G1 native path, g3_rows, g3_z; copied with attribution).
The one change: the modules read their inputs from a mirror of CRG1's inputs/ in this lane's cache, identical except
lensing/lens_inventory.npz. Caches go to this lane's cache/ only. Each configuration runs in its own process:
  june_true   CRG1's June inventory (lr_lenses + CFG110 WLENS), mirrored    -> K6: reproduce LE1 to the printed digits
  june_model  June logM, z; WLENS from the frozen cell model                  -> K7: |dZ| <= 0.20, G1 and G3, both footings
  fn4c        stage 1's 255,052 lenses (logM + 0.056), modelled WLENS         -> the grade
  fn4c_mut    as fn4c with logM + 0.301                                       -> MUTATE: G1 law Z moves by > 1.0, both footings
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -I fn4c_grade.py   -> fn4c_grade.out / .json
kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework.
"""
import importlib.util, json, math, os, subprocess, sys, types
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True; os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import numpy as np
np.seterr(all="ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
RB = os.path.join(REPO, "rebuild_2026_10_22")
CRG = os.path.join(RB, "CRG1_clean_room_regrade"); RQ3 = os.path.join(RB, "RQ3_acceptance_v2"); NP1 = os.path.join(RB, "NP1_nonparametric_rule")
RS1 = os.path.join(RB, "RS1_required_source")
CACHE = os.path.join(HERE, "cache")
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); FEET = ("canonical", "alt"); ZL = 2.0
CFGS = ("june_true", "june_model", "fn4c", "fn4c_mut")
LE1_LAW = {"canonical": dict(S0=9.27416886540268, G3=5.007629637928022), "alt": dict(S0=6.519480244063122, G3=3.318280850780635)}
LE1_PRINTED = {"canonical": dict(S0="+9.27", G3="+5.01"), "alt": dict(S0="+6.52", G3="+3.32")}


def zchi(c, dof): return (c - dof) / math.sqrt(2 * dof)


def logmgal(lm): return lm + np.log10(1 + 10 ** (-0.69 * lm + 6.63))


# ------------------------------------------------------------------ parent: inventories and mirrors
def wlens_model(june, lm_target, z_target):
    """frozen cell model: median WLENS/M_gal of the June inventory in cells z (0.02 from 0.1) x log M_gal (0.1); a cell with
    fewer than 20 June lenses takes its z cell's median. Returns WLENS for the targets."""
    zj = june["z"]; mj = logmgal(june["logM"]); rj = june["WLENS"] / 10 ** mj
    ze = np.arange(0.1, 0.5001, 0.02); me = np.arange(7.0, 12.001, 0.1)
    iz = np.clip(np.digitize(zj, ze) - 1, 0, len(ze) - 2); im = np.clip(np.digitize(mj, me) - 1, 0, len(me) - 2)
    zmed = np.array([np.median(rj[iz == a]) if np.any(iz == a) else np.median(rj) for a in range(len(ze) - 1)])
    cell = np.full((len(ze) - 1, len(me) - 1), np.nan)
    for a in range(len(ze) - 1):
        for c in range(len(me) - 1):
            s = (iz == a) & (im == c)
            cell[a, c] = np.median(rj[s]) if s.sum() >= 20 else zmed[a]
    mt = logmgal(lm_target)
    jz = np.clip(np.digitize(z_target, ze) - 1, 0, len(ze) - 2); jm = np.clip(np.digitize(mt, me) - 1, 0, len(me) - 2)
    return cell[jz, jm] * 10 ** mt


def build_mirror(cfg, inv):
    """cache/mirror_<cfg>/: symlinks to every CRG1 input except lensing/lens_inventory.npz, which is this config's."""
    src = os.path.join(CRG, "inputs"); dst = os.path.join(CACHE, f"mirror_{cfg}")
    os.makedirs(os.path.join(dst, "lensing"), exist_ok=True)
    for e in os.listdir(src):
        if e == "lensing": continue
        p = os.path.join(dst, e)
        if not os.path.lexists(p): os.symlink(os.path.join(src, e), p)
    for e in os.listdir(os.path.join(src, "lensing")):
        if e == "lens_inventory.npz": continue
        p = os.path.join(dst, "lensing", e)
        if not os.path.lexists(p): os.symlink(os.path.join(src, "lensing", e), p)
    p = os.path.join(dst, "lensing", "lens_inventory.npz")
    if os.path.lexists(p): os.remove(p)
    if inv is None: os.symlink(os.path.join(src, "lensing", "lens_inventory.npz"), p)
    else: np.savez_compressed(p, logM=inv["logM"], z=inv["z"], WLENS=inv["WLENS"])
    return dst


# ------------------------------------------------------------------ child: LE1's graders on one mirror
def child(cfg):
    MIR = os.path.join(CACHE, f"mirror_{cfg}")
    p = os.path.join(CRG, "v1", "crg1_core.py"); s = open(p).read()
    for a, b in (('INP = os.path.join(HERE, "inputs")', f'INP = {MIR!r}'),
                 ('PART = os.path.join(HERE, os.environ.get("CRG1_PARTIALS", "partials"))', f'PART = {os.path.join(CACHE, "crg_p")!r}'),
                 ('CACHE = os.path.join(HERE, os.environ.get("CRG1_CACHE", "cache"))', f'CACHE = {os.path.join(CACHE, "crg_c")!r}')):
        assert s.count(a) == 1, a; s = s.replace(a, b)
    m = types.ModuleType("crg1_core"); m.__file__ = p; sys.modules["crg1_core"] = m; exec(compile(s, p, "exec"), m.__dict__)
    sys.path.insert(0, os.path.join(CRG, "v1"))
    sp = importlib.util.spec_from_file_location("rq3acc", os.path.join(RQ3, "acceptance.py")); ACC = importlib.util.module_from_spec(sp); sp.loader.exec_module(ACC)
    import crg1_lens as Le
    assert Le.PL == os.path.join(MIR, "lensing"), Le.PL
    sp = importlib.util.spec_from_file_location("cand_law", os.path.join(RQ3, "candidates", "law.py")); law = importlib.util.module_from_spec(sp); sp.loader.exec_module(law)
    RGRID = Le.RGRID; SIk = 1e6 / 3.0857e16; REX = [.343, .442, .433, .429]

    class G1:                                   # LE1's class G1, native path only (le1.py lines 46-80), unchanged in substance
        def __init__(s):
            L = Le.load(); s.L = L; s.st = Le.Stencil(L["Rn"] * 1e6)
            th = Le.TwoHalo(Le.load())
            s.T0 = np.array([th.esd2h(L["R"][b], REX[b]) * Le.FF for b in range(4)])
            s.IP = [j for j in range(15) if L["R"][0][j] <= 0.31]
        def table(s, c, foot):
            Tb = np.zeros((len(Le.LMG), 60)); a0 = A0[foot]
            for i, lm in enumerate(Le.LMG):
                MB, _ = Le.baryon(float(lm)); gg = Le.Gpc * (MB - 10 ** float(lm)) / RGRID ** 2; gb = Le.Gpc * MB / RGRID ** 2
                v = ACC.call(c, gb=gb * SIk, gg=gg * SIk, gs=(gb - gg) * SIk, r=RGRID * 3.0857e16, a0=a0, sample="lens"); Tb[i] = s.st.dsig(MB * v / (gb * SIk), "linear")
            return Tb
        def model(s, Tb): return Le.stack(s.L, Tb)
        def grade(s, m, prim=False):
            idx = s.IP if prim else list(range(15)); ch, b = Le.fit(s.L, m, idx, s.T0); dof = 4 * len(idx) - 4
            return dict(chi2=float(ch), dof=dof, Z=float(zchi(ch, dof)))
        def amp(s, m):
            idx = Le.sel(s.IP); y = s.L["Yn"].ravel()[idx]; mm = m[idx]; sg = np.sqrt(np.diag(s.L["Cn"]))[idx]; ok = (y > 0) & (mm > 0)
            d = np.log10(y[ok] / mm[ok]); w = (y[ok] * math.log(10) / sg[ok]) ** 2; mu = float((w * d).sum() / w.sum()); se = float(1 / math.sqrt(w.sum()))
            return dict(mean=mu, se=se, z=mu / se, n=int(ok.sum()))

    out = {"cfg": cfg}
    g = G1(); out["zeff"] = [float(x) for x in g.L["zeff"]]
    out["bin_logmean_w"] = [float(math.log10(np.sum(wb * 10 ** li) / np.sum(wb))) for li, wb in g.L["lens"]]
    for foot in FEET:
        mA = g.model(g.table(law, foot))
        out[foot] = dict(S0=g.grade(mA), S1=g.grade(mA, prim=True), A1=g.amp(mA))
    # G3: CX1's lensing rows through NP1's cx_rows (le1.py g3_rows / g3_z); rs1_rows.INP set to the mirror before cx1_rows loads
    sys.path.insert(0, RS1); import rs1_rows as RR
    RR.INP = MIR
    sys.path.insert(0, NP1); import np1_core as NC
    for foot in FEET:
        R = [q for q in NC.cx_rows(foot) if q["line"] == "L"]
        a0 = A0[foot]; y = np.array([q["y"] for q in R]); ell = np.array([q["ell"] for q in R]); f = np.array([q["f"] for q in R])
        lb = np.array([q["logB"] for q in R]); sd = np.array([q["sd"] for q in R])
        gb = y * NC.A0C; r = ell * NC.CL ** 2 / NC.A0C; gobs = 10 ** lb * NC.law(gb, NC.FOOT[foot])
        gm = ACC.call(law, gb=gb, gg=f * gb, gs=(1 - f) * gb, r=r, a0=NC.FOOT[foot], sample="lens")
        d = np.log10(gobs / gm); w = 1 / sd ** 2; mu = float((w * d).sum() / w.sum()); se = float(1 / math.sqrt(w.sum()))
        out[foot]["G3"] = dict(mean=mu, se=se, z=mu / se, n=len(d))
    cx = sys.modules["cx1_rows"]
    out["cx1_INP"] = os.path.relpath(cx.INP, HERE)
    with open(os.path.join(CACHE, f"child_{cfg}.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)


# ------------------------------------------------------------------ parent
def main():
    OUT = []
    def P(*a):
        s_ = " ".join(str(x) for x in a); print(s_, flush=True); OUT.append(s_)
    st1 = json.load(open(os.path.join(HERE, "fn4c_rebuild.json")))
    P("FN4c stage 2. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework.")
    P(f"Stage 1 label: {st1['label']} (N {st1['primary']['isolated']:,}).")
    if st1["label"] != "REBUILD MATCHES":
        P("Stage 2 does not run (frozen)."); return 1
    june = dict(np.load(os.path.join(CRG, "inputs", "lensing", "lens_inventory.npz")))
    fl = np.load(os.path.join(CACHE, "fn4c_lenses.npz"))
    assert len(fl["logM"]) == st1["primary"]["isolated"]
    inv = {"june_true": None,
           "june_model": dict(logM=june["logM"], z=june["z"], WLENS=wlens_model(june, june["logM"], june["z"])),
           "fn4c": dict(logM=fl["logM"], z=fl["z"], WLENS=wlens_model(june, fl["logM"], fl["z"])),
           "fn4c_mut": dict(logM=fl["logM"] + 0.301, z=fl["z"], WLENS=wlens_model(june, fl["logM"] + 0.301, fl["z"]))}
    for cfg in CFGS:
        build_mirror(cfg, inv[cfg])
    # per-bin inventory summaries
    P("")
    P("Inventories (bins log M* 8.5/10.3/10.6/10.8/11.0): counts and WLENS-weighted log mean M*")
    summ = {}
    for cfg in CFGS:
        d = june if cfg == "june_true" else inv[cfg]
        bins = np.digitize(d["logM"], [8.5, 10.3, 10.6, 10.8, 11.0001]) - 1
        cnt = [int((bins == b).sum()) for b in range(4)]
        lmw = [float(np.log10(np.average(10 ** d["logM"][bins == b], weights=d["WLENS"][bins == b]))) if cnt[b] else float("nan") for b in range(4)]
        summ[cfg] = dict(counts=cnt, logmean_w=lmw, n=int(len(d["logM"])))
        P(f"  {cfg:<11s} n {len(d['logM']):>7,}  per bin {cnt}  weighted log mean M* {np.round(lmw, 3).tolist()}")
    res = {}
    for cfg in CFGS:
        r = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "child", cfg], capture_output=True, text=True, cwd=HERE)
        if r.returncode != 0:
            P(f"child {cfg} FAILED: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else 'no stderr'}"); return 1
        res[cfg] = json.load(open(os.path.join(CACHE, f"child_{cfg}.json")))
    P("")
    P("Law through LE1's graders (G1 S0 = A30 statistic; S1 R <= 0.31 Mpc; A1 = G1 model with G3's statistic; G3 = CX1 line):")
    for cfg in CFGS:
        for foot in FEET:
            o = res[cfg][foot]
            P(f"  {cfg:<11s} {foot:<9s} G1 S0 Z {o['S0']['Z']:+7.3f} (chi2 {o['S0']['chi2']:6.1f}/{o['S0']['dof']})  S1 Z {o['S1']['Z']:+6.2f}  "
              f"A1 mean {o['A1']['mean']:+.4f} +- {o['A1']['se']:.4f}  G3 z {o['G3']['z']:+6.3f} (mean {o['G3']['mean']:+.4f})")
    # K6 (printed digits and full precision), K7, MUTATE
    k6 = {}
    for foot in FEET:
        o = res["june_true"][foot]
        k6[foot] = dict(S0=f"{o['S0']['Z']:+.2f}" == LE1_PRINTED[foot]["S0"], G3=f"{o['G3']['z']:+.2f}" == LE1_PRINTED[foot]["G3"],
                        dS0=o["S0"]["Z"] - LE1_LAW[foot]["S0"], dG3=o["G3"]["z"] - LE1_LAW[foot]["G3"])
    K6 = all(v["S0"] and v["G3"] for v in k6.values())
    k7 = {foot: dict(dS0=res["june_model"][foot]["S0"]["Z"] - res["june_true"][foot]["S0"]["Z"],
                     dG3=res["june_model"][foot]["G3"]["z"] - res["june_true"][foot]["G3"]["z"]) for foot in FEET}
    K7 = all(abs(v["dS0"]) <= 0.20 and abs(v["dG3"]) <= 0.20 for v in k7.values())
    mut = {foot: res["fn4c_mut"][foot]["S0"]["Z"] - res["fn4c"][foot]["S0"]["Z"] for foot in FEET}
    MUTB = all(abs(v) > 1.0 for v in mut.values())
    P("")
    P(f"K6 reproduce LE1 (June inventory, true WLENS): " + "; ".join(f"{f} G1 {res['june_true'][f]['S0']['Z']:+.2f} vs {LE1_PRINTED[f]['S0']} (d {k6[f]['dS0']:+.1e}), G3 {res['june_true'][f]['G3']['z']:+.2f} vs {LE1_PRINTED[f]['G3']} (d {k6[f]['dG3']:+.1e})" for f in FEET) + f" -> {'PASS' if K6 else 'FAIL'}")
    P(f"K7 modelled WLENS on the June inventory: " + "; ".join(f"{f} dZ G1 {k7[f]['dS0']:+.3f}, G3 {k7[f]['dG3']:+.3f}" for f in FEET) + f"; line 0.20 -> {'PASS' if K7 else 'FAIL'}")
    P(f"MUTATE (masses x2): G1 law Z moves " + ", ".join(f"{f} {mut[f]:+.2f}" for f in FEET) + f"; line > 1.0 -> {'BITES' if MUTB else 'DOES NOT BITE (failed check)'}")
    labels = {}
    for foot in FEET:
        z1 = res["fn4c"][foot]["S0"]["Z"]; z3 = res["fn4c"][foot]["G3"]["z"]
        if not (K6 and K7): labels[foot] = "NOT EVALUABLE"
        elif z1 > ZL and z3 > ZL: labels[foot] = "GAP STANDS"
        elif abs(z1) <= ZL and abs(z3) <= ZL: labels[foot] = "GAP CLOSES"
        else: labels[foot] = "GRADERS SPLIT"
    P("")
    for foot in FEET:
        o = res["fn4c"][foot]; j = res["june_true"][foot]
        P(f"LABEL {foot}: {labels[foot]}. Rebuilt inventory: G1 Z {o['S0']['Z']:+.2f} (LE1 {j['S0']['Z']:+.2f}), G3 z {o['G3']['z']:+.2f} (LE1 {j['G3']['z']:+.2f}), "
          f"A1 mean {o['A1']['mean']:+.3f} dex (LE1 {j['A1']['mean']:+.3f}).")
    R = dict(stage1_label=st1["label"], inventories=summ, results=res, K6=dict(passed=K6, detail=k6), K7=dict(passed=K7, detail=k7),
             MUTATE=dict(bites=MUTB, dZ=mut), labels=labels)
    with open(os.path.join(HERE, "fn4c_grade.json"), "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    with open(os.path.join(HERE, "fn4c_grade.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    return 0 if (K6 and K7 and MUTB) else 1


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "child":
        child(sys.argv[2])
    else:
        sys.exit(main())
