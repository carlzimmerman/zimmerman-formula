#!/usr/bin/env python3
"""GRW1 main runs and MUTATE arms (criteria 11c19a2c5f sections 1-3, 5; amendment A1 4dfa022e34).
Usage: python3 grw1_run.py                 -> grw1.json / grw1.out (every model, treatment, footing; parts/ checkpoints)
       python3 grw1_run.py --mutate off|cold|2a0 -> grw1_MUTATE_<arm>.json / .out (c_s 1000 and 4481, both footings, T-A and T-S)
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed. One thread.
"""
import os, sys, json, math, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grw1_lib as GL
import grw1_obs as GO

MUT = sys.argv[sys.argv.index("--mutate") + 1] if "--mutate" in sys.argv else None
assert MUT in (None, "off", "cold", "2a0")
TAG = "grw1" if MUT is None else f"grw1_MUTATE_{MUT}"
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
OUT = []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))
wb, wc = GL.OB / (GL.OB + GL.OD), GL.OD / (GL.OB + GL.OD)
FOOT = ("canonical", "alt")
lk = np.log(GL.KGRID)

# ------------------------------------------------------------------ reference
Mref = GL.run_class(None); bgref = GL.Background(Mref); icref = GL.transfer_ic(Mref, GL.ZSTART, "d_cdm")
def cached(tag, make):
    """checkpoint: parts/<tag>.npz holds the run's state at ZOUT (regenerated if missing)."""
    fn = os.path.join(PARTS, tag + ".npz")
    if os.path.exists(fn):
        d = np.load(fn, allow_pickle=False)
        out = {}
        for k in d.files:
            v = d[k]
            out[k] = v if v.shape != () else (None if not np.isfinite(v) else v.item())
        return out
    t = time.time(); o = make()
    o2 = {k: (v if v is not None else np.array(np.nan)) for k, v in o.items()}
    np.savez(fn, **{k: np.asarray(v) for k, v in o2.items()})
    P(f"   [run {tag}: {time.time() - t:.0f} s, nfev {o['nfev']}]")
    return o
REF = cached("ref_cold_off", lambda: GL.Run(bgref, "off", 1.0, GL.const_cs(0.0), icref).solve())
ZARR = REF["z"]
dl_ref = wb * REF["db"][:, 0, :] + wc * REF["dc"][:, 0, :]
db_ref = REF["db"][:, 0, :]; Db_ref = REF["Db"][:, 0, :]
j0 = GO.zindex(ZARR, 0.0)
SIG2_REF0 = GO.sigma2(GO.PREF[0.0])
FS8_REF = {t: GO.sigma2(GO.PREF[z] * GO.interp_k((Db_ref[:, GO.zindex(ZARR, z)] / dl_ref[:, GO.zindex(ZARR, z)]) ** 2)) for (t, z, *_) in GO.DESI}

# ------------------------------------------------------------------ observables and grading (criteria section 2)
def rms_k(arr2, kmax=1.0):
    """sqrt( integral dln k Delta_R^2 <|.|^2> ) over k <= kmax; arr2 = mu-averaged square on KGRID."""
    m = GL.KGRID <= kmax; return float(math.sqrt(np.sum((GL.WK * GL.DR2 * arr2)[m])))

def observe(o, tr, a0=None, cs=None):
    zz = o["z"]; assert np.allclose(zz, ZARR)
    dlens = GL.lens_delta(o, tr)
    RL = GL.muavg2(dlens) / dl_ref ** 2
    Rbb = GL.muavg2(o["db"]) / db_ref ** 2
    Vb = GL.muavg2(o["Db"]) / dl_ref ** 2
    S = GO.S_of_kz(GO.ratio_interp(RL, ZARR)); lens = GO.lensing(S)
    s = math.sqrt(GO.sigma2(GO.PREF[0.0] * GO.interp_k(RL[:, j0])) / SIG2_REF0)
    Rf = {t: math.sqrt(GO.sigma2(GO.PREF[z] * GO.interp_k(Vb[:, GO.zindex(ZARR, z)])) / FS8_REF[t]) for (t, z, *_) in GO.DESI}
    lkf = np.log(GO.KFOREST)
    forest = {str(z): [float(x) for x in np.interp(lkf, lk, Rbb[:, GO.zindex(ZARR, z)])] for z in GO.ZFOREST + GO.ZFOREST_REP}
    forest_tot = {str(z): [float(x) for x in np.interp(lkf, lk, RL[:, GO.zindex(ZARR, z)])] for z in GO.ZFOREST + GO.ZFOREST_REP}
    ktab = (0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0)
    Rtab = {str(z): [float(np.interp(math.log(k), lk, RL[:, GO.zindex(ZARR, z)])) for k in ktab] for z in (0.0, 0.5, 1.0, 2.0, 3.0, 4.0)}
    rep = dict(R_lens_table=dict(k=ktab, rows=Rtab), forest_total=forest_tot,
               sigma8=s * GO.ML.sigma8(), fsigma8={t: Rf[t] * math.sqrt(FS8_REF[t]) for t in Rf})
    if o.get("x") is not None and np.ndim(o["x"]) > 0 and np.all(np.isfinite(o["x"])):
        rep["x_of_z"] = {str(z): float(o["x"][GO.zindex(ZARR, z)]) for z in (0.0, 0.5, 1.0, 2.0, 3.0, 10.0, 100.0, 700.0) if np.any(np.abs(ZARR - z) < 1e-6)}
    if tr in ("TA", "TAmax") and cs:
        rows = {}
        for z in (0.0, 2.0):
            j = GO.zindex(ZARR, z); a = 1 / (1 + z); _, _, H, _, Ob, Oc, _, _ = bgref.at(math.log(a))
            q2 = (GL.KGRID[:, None] / (a * H) * cs / GL.C_KMS) ** 2 / (1.5 * Oc)
            c = np.ones(len(GL.MU)) if tr == "TAmax" else GL.cfac(float(o["x"][j]))
            dN = o["dc"][:, :, j]; dd = dN / (1 + c[None, :] * q2); dPi = dN - dd
            rows[str(z)] = dict(delta_N=rms_k(GL.muavg2(dN[:, :, None])[:, 0]), delta_d=rms_k(GL.muavg2(dd[:, :, None])[:, 0]),
                                delta_Pi=rms_k(GL.muavg2(dPi[:, :, None])[:, 0]), delta_b=rms_k(GL.muavg2(o["db"][:, :, j:j + 1])[:, 0]))
        rep["clock_split_rms_k_le_1"] = rows
    if tr == "TS":
        rows = {}
        for z in (0.0, 2.0):
            j = GO.zindex(ZARR, z); B = GL.Bfac(float(o["x"][j]))[None, :]
            halo = (B - 1) * (GL.OB * o["db"][:, :, j] + GL.OD * o["dc"][:, :, j]) / GL.OD
            rows[str(z)] = dict(halo_over_cold_mean_rms=rms_k(GL.muavg2(halo[:, :, None])[:, 0]))
        rep["counted_once"] = rows
    return dict(r_eff=lens["r_eff"], dchi2=lens["dchi2"], chi2_abs=lens["chi2_abs"], S_L=lens["S_L"], pr4_bins=lens["bins"],
                s=s, Rf=Rf, forest=forest, reported=rep)

def grade(ob):
    """per-line status (criteria section 2) and the per-run label (section 3)."""
    L = {}
    lo, hi = 1 - GO.LINE_L1, 1 + GO.LINE_L1; r = ob["r_eff"]
    L["L1"] = dict(obtained=r, band=[lo, hi], status="MET" if lo <= r <= hi else ("SHORT" if r < lo else "OVER"),
                   factor=1.0 if lo <= r <= hi else (r / lo if r < lo else r / hi))
    L["L2"] = dict(obtained=ob["dchi2"], band=[None, 4.0], status="MET" if ob["dchi2"] <= 4.0 else "SHAPE", factor=ob["dchi2"] / 4.0)
    sh, ov = [], []
    for (t, z, r1, p1, m1, r2, p2, m2) in GO.DESI:
        for (rr, e) in ((r1, 0.5 * (p1 + m1)), (r2, 0.5 * (p2 + m2))):
            v = ob["Rf"][t]
            if v < rr - 2 * e: sh.append(v / (rr - 2 * e))
            elif v > rr + 2 * e: ov.append(v / (rr + 2 * e))
    st3 = "MET" if not sh and not ov else ("SHORT" if sh and not ov else ("OVER" if ov and not sh else "SHORT AND OVER"))
    L["L3"] = dict(obtained=ob["Rf"], status=st3, factor=(min(sh) if sh else (max(ov) if ov else 1.0)), n_short=len(sh), n_over=len(ov))
    lo, hi = 1 - GO.S8LINE, 1 + GO.S8LINE; s = ob["s"]
    L["L4"] = dict(obtained=s, band=[lo, hi], status="MET" if lo <= s <= hi else ("SHORT" if s < lo else "OVER"),
                   factor=1.0 if lo <= s <= hi else (s / lo if s < lo else s / hi))
    vals = [v for z in ("2.0", "3.0") for v in ob["forest"][z]]
    sh = [v / 0.8 for v in vals if v < 0.8]; ov = [v / 1.2 for v in vals if v > 1.2]
    st5 = "MET" if not sh and not ov else ("SHORT" if sh and not ov else ("OVER" if ov and not sh else "SHORT AND OVER"))
    L["L5"] = dict(obtained=dict(min=min(vals), max=max(vals)), status=st5, factor=(min(sh) if sh else (max(ov) if ov else 1.0)))
    dirs = set()
    for k in ("L1", "L3", "L4", "L5"):
        st = L[k]["status"]
        if "SHORT" in st: dirs.add("SHORT")
        if "OVER" in st: dirs.add("OVER")
    if not dirs: lab = "BUILDS IT" if L["L2"]["status"] == "MET" else "MISSES THE SHAPE"
    elif dirs == {"SHORT"}: lab = "FALLS SHORT"
    elif dirs == {"OVER"}: lab = "OVERSHOOTS"
    else: lab = "FALLS SHORT AND OVERSHOOTS"
    return dict(lines=L, label=lab)

def band_label(labs):
    """criteria section 3, over the band's c_s in order."""
    if any(l == "BUILDS IT" for l in labs): return "BUILDS IT"
    if len(set(labs)) == 1: return labs[0]
    if any(l == "FALLS SHORT" for l in labs) and any(l == "OVERSHOOTS" for l in labs): return "MIXED: BISECT"
    return " / ".join(sorted(set(labs)))

def short(ob, g):
    L = g["lines"]
    return (f"r_eff {ob['r_eff']:.4g} [{L['L1']['status']}], dchi2 {ob['dchi2']:.4g} [{L['L2']['status']}], "
            f"Rf {'/'.join(f'{ob['Rf'][t]:.3g}' for t in ob['Rf'])} [{L['L3']['status']}], s {ob['s']:.4g} [{L['L4']['status']}], "
            f"forest z2 {min(ob['forest']['2.0']):.3g}-{max(ob['forest']['2.0']):.3g} z3 {min(ob['forest']['3.0']):.3g}-{max(ob['forest']['3.0']):.3g} [{L['L5']['status']}] -> {g['label']}")

RES = dict(lane="GRW1", criteria="11c19a2c5f", amendment_A1="4dfa022e34", tag=TAG, mutate=MUT, note=GO.kappa_note, runs={})
def record(key, o, tr, a0=None, cs=None):
    ob = observe(o, tr, a0, cs); g = grade(ob)
    RES["runs"][key] = dict(obs=ob, grade=g, nfev=int(o["nfev"]))
    json.dump(RES["runs"][key], open(os.path.join(PARTS, key + ".json"), "w"), indent=1, default=float)
    P(f"{key}: {short(ob, g)}"); return ob, g

# reference through the same pipeline (must be exactly 1)
record("ref", REF, "off")

def model(cs):
    M = GL.run_class(cs); bg = GL.Background(M); ic = GL.transfer_ic(M, GL.ZSTART, "d_fld"); M.struct_cleanup(); return bg, ic

def main():
    if MUT is None:
        P(f"GRW1 main runs. z_start {GL.ZSTART:.0f}; k {len(GL.KGRID)} pts 1e-3-10 / Mpc; mu {len(GL.MU)} nodes; T_IGM {GL.T_IGM:.0f} K.")
        labels = {}
        for cs in GL.CS_PRIMARY + GL.CS_DT1:
            bg, ic = model(cs); c = GL.const_cs(cs)
            o = cached(f"off_cs{cs:.0f}", lambda: GL.Run(bg, "off", 1.0, c, ic).solve()); ob, g = record(f"off_cs{cs:.0f}", o, "off")
            o = cached(f"TAmax_cs{cs:.0f}", lambda: GL.Run(bg, "TAmax", 1.0, c, icref).solve()); ob, g = record(f"TAmax_cs{cs:.0f}", o, "TAmax", cs=cs)
            for f in FOOT: labels[("TAmax", f, cs)] = g["label"]
            for f in FOOT:
                a0 = GL.A0[f]
                o = cached(f"TA_{f}_cs{cs:.0f}", lambda: GL.Run(bg, "TA", a0, c, ic).solve()); ob, g = record(f"TA_{f}_cs{cs:.0f}", o, "TA", a0, cs)
                labels[("TA", f, cs)] = g["label"]
                o = cached(f"TS_{f}_cs{cs:.0f}", lambda: GL.Run(bg, "TS", a0, c, ic).solve()); ob, g = record(f"TS_{f}_cs{cs:.0f}", o, "TS", a0, cs)
                labels[("TS", f, cs)] = g["label"]
        # step family W (reported): cold until z_w, then 1000 km/s; cold initial state
        for zw in (3.0, 1.0):
            c = GL.step_cs(1000.0, zw)
            o = cached(f"W_TAmax_zw{zw:g}", lambda: GL.Run(bgref, "TAmax", 1.0, c, icref).solve()); record(f"W_TAmax_zw{zw:g}", o, "TAmax")
            for f in FOOT:
                o = cached(f"W_TA_{f}_zw{zw:g}", lambda: GL.Run(bgref, "TA", GL.A0[f], c, icref).solve()); record(f"W_TA_{f}_zw{zw:g}", o, "TA")
                o = cached(f"W_off_zw{zw:g}", lambda: GL.Run(bgref, "off", 1.0, c, icref).solve())
            record(f"W_off_zw{zw:g}", o, "off")
        # sensitivity: T-A from z_start 900 (reported)
        for cs in (1000.0, 4481.0):
            M = GL.run_class(cs); bg = GL.Background(M); ic9 = GL.transfer_ic(M, 900.0, "d_fld"); M.struct_cleanup()
            o = cached(f"TA_canonical_cs{cs:.0f}_z900", lambda: GL.Run(bg, "TA", GL.A0["canonical"], GL.const_cs(cs), ic9).solve(lna0=math.log(1 / 901.0)))
            record(f"TA_canonical_cs{cs:.0f}_z900", o, "TA", GL.A0["canonical"], cs)
        # numerical convergence (REPORTED; not in the frozen criteria): tighter tolerances, 12 mu nodes, 96 k points
        conv = {}
        for tr in ("TA", "TS"):
            bg, ic = model(1000.0); a0 = GL.A0["canonical"]; c = GL.const_cs(1000.0)
            o = cached(f"CONV_tol_{tr}", lambda: GL.Run(bg, tr, a0, c, ic).solve(rtol=1e-9, atol=1e-12))
            ob = observe(o, tr, a0, 1000.0); base = RES["runs"][f"{tr}_canonical_cs1000"]["obs"]
            conv[f"{tr}_tol"] = dict(r_eff=[base["r_eff"], ob["r_eff"]], s=[base["s"], ob["s"]], forest_z3=[base["forest"]["3.0"], ob["forest"]["3.0"]])
            P(f"   CONV {tr} rtol 1e-9: r_eff {base['r_eff']:.6g} -> {ob['r_eff']:.6g}; s {base['s']:.6g} -> {ob['s']:.6g}; forest z3 min {min(base['forest']['3.0']):.4g} -> {min(ob['forest']['3.0']):.4g}")
        RES["convergence_reported"] = conv
        BL = {}
        for tr in ("TA", "TAmax", "TS"):
            for f in FOOT:
                BL[f"{tr}_{f}"] = dict(primary=band_label([labels[(tr, f, cs)] for cs in GL.CS_PRIMARY]),
                                       dt1=band_label([labels[(tr, f, cs)] for cs in GL.CS_DT1]),
                                       per_cs={f"{cs:.0f}": labels[(tr, f, cs)] for cs in GL.CS_PRIMARY + GL.CS_DT1})
        RES["band_labels"] = BL
        P("")
        P("Band labels (primary band c_s 1000-4481 / DT1 bracket 350-707), canonical | alt:")
        for tr in ("TA", "TAmax", "TS"):
            P(f"  {tr:6s}: {BL[tr + '_canonical']['primary']} | {BL[tr + '_alt']['primary']}    (DT1: {BL[tr + '_canonical']['dt1']} | {BL[tr + '_alt']['dt1']})")
    else:
        prim = {}
        for fn in os.listdir(PARTS):
            if fn.endswith(".json"): prim[fn[:-5]] = json.load(open(os.path.join(PARTS, fn)))
        def quant(ob):
            q = [ob["r_eff"], ob["s"]] + [ob["Rf"][t] for t in sorted(ob["Rf"])] + ob["forest"]["2.0"] + ob["forest"]["3.0"]
            return np.array(q)
        BITE = {}
        for cs in (1000.0, 4481.0):
            bg, ic = model(cs)
            for f in FOOT:
                a0 = GL.A0[f]
                for tr in ("TA", "TS"):
                    base = prim[f"{tr}_{f}_cs{cs:.0f}"]["obs"]
                    if MUT == "off":
                        o = cached(f"off_cs{cs:.0f}", lambda: GL.Run(bg, "off", 1.0, GL.const_cs(cs), ic).solve()); key = f"MUT_off_{tr}_{f}_cs{cs:.0f}"; ob, g = record(key, o, "off")
                        want = "down"
                    elif MUT == "cold":
                        o = cached(f"MUT_cold_{tr}_{f}", lambda: GL.Run(bgref, tr, a0, GL.const_cs(0.0), icref).solve()); key = f"MUT_cold_{tr}_{f}_cs{cs:.0f}"; ob, g = record(key, o, tr, a0, 0.0)
                        want = "to1" if tr == "TA" else "up"
                    else:
                        o = cached(f"MUT_2a0_{tr}_{f}_cs{cs:.0f}", lambda: GL.Run(bg, tr, 2 * a0, GL.const_cs(cs), ic).solve()); key = f"MUT_2a0_{tr}_{f}_cs{cs:.0f}"; ob, g = record(key, o, tr, 2 * a0, cs)
                        want = "up"
                    qb, qm = quant(base), quant(ob); rel = qm / qb - 1
                    if want == "down": bites = bool(np.all(rel < -1e-4))
                    elif want == "up": bites = bool(np.all(rel > 1e-4))
                    else: bites = bool(np.all(np.abs(qm - 1) <= 1e-6) and np.all(rel > 1e-4))
                    BITE[key] = dict(want=want, bites=bites, rel_min=float(rel.min()), rel_max=float(rel.max()), mutated=qm.tolist(), primary=qb.tolist())
                    P(f"   {key}: want {want}; rel change {rel.min():+.3e} .. {rel.max():+.3e} -> {'BITES' if bites else 'DOES NOT BITE'}")
        RES["bite"] = BITE; RES["all_bite"] = all(v["bites"] for v in BITE.values())
        P(f"MUTATE {MUT}: all bite {RES['all_bite']}")

    P(f"({time.time() - T0:.0f} s)"); P(GO.kappa_note)
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
