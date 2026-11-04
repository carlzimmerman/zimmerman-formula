#!/usr/bin/env python3
"""NV2_external_field_xcop_lenses (NV1 nv1.py copied with attribution; E1 only). Modes:
  coverage  E tables for RQ3 (rules/<E>_table.json), coverage per graded line and RQ3 block, fit-able rule, sign test with look-elsewhere shuffles (step 1)
  controls  known answer, zero-weight cards (U vs RQ3's law card; S vs the plain law on S), checker, admissible plant, planted non-local boost (true vs shuffled E)
  real      admissible L3+E fits for fit-able candidates, gates 1-4, checker, E-shuffle MUTATE, RQ3 cards U and S (NV1, MUTATE, NP2 on S), before/after table, labels
Run: PYTHONHASHSEED=0 nice -n 10 python3 -I nv2.py MODE. See FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, resource, subprocess, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import nv2_core as K
import nv2_env as V
import nv2_cand as CA
N, C = K.N, K.C
RB = os.path.dirname(HERE); RQ3 = os.path.join(RB, "RQ3_acceptance_v2"); NP2D = K.NP2D
MODE = sys.argv[1] if len(sys.argv) > 1 else "coverage"; OUT = []; T0 = time.time()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def fpk():
    try: return [l.split(":")[1].strip() for l in subprocess.run(["footprint", str(os.getpid())], capture_output=True, text=True).stdout.splitlines() if "phys_footprint_peak" in l][0]
    except Exception: return "?"
def tm(): return f"[{time.time() - T0:.0f}s, max RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB, phys footprint peak {fpk()}]"
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items() if not str(k).startswith("_")}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, float) and not math.isfinite(o): return None
    return o
def fin(x):
    try: return x is not None and math.isfinite(float(x))
    except (TypeError, ValueError): return False
FEET = C.FOOT; TARGETS = ("A10", "A12", "A13", "A30", "A5", "A6", "A7")
os.makedirs(os.path.join(HERE, "rules"), exist_ok=True); os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
def np2_rule(ft): return N.CRule.load(os.path.join(NP2D, "rules", f"real_L3_F_{ft}.npz"))
def rs_dict(rule): return dict(arm=rule.arm, mu=rule.mu, sd=rule.sd, Z=rule.Z, alpha=rule.alpha, ell=rule.ell, sf2=np.float64(rule.sf2), Zc=rule.Zc, Vc=rule.Vc, beta=rule.beta)
def save_rule(rule, stem, ft): np.savez(os.path.join(HERE, "rules", f"{stem}_{ft}.npz"), **rs_dict(rule))
def table_path(name): return os.path.join(HERE, "rules", f"{name}.json")

# ======================================================================= coverage + sign test
def coverage():
    R = {}; cx = {ft: K.cx_rows(ft) for ft in FEET}
    LTRQ3 = None
    sys.path.insert(0, os.path.join(RB, "CRG1_clean_room_regrade", "v1"))
    for c in V.CANDS:
        T = V.rq3_table_build(c); json.dump(clean(T), open(table_path(f"{c}_table"), "w"), indent=0); o = {}
        lt_rq3 = [r["name"] for r in __import__("csv").DictReader(open(os.path.join(V.CRGI, "little_things", "oh2015_table2.csv"))) if all(r[k].strip() != "" for k in ("Rmax_kpc", "V_kms", "Mgas_1e7Msun", "MSED_1e7Msun"))]
        cnt = lambda d, keys=None: [sum(fin(d[k]) for k in (keys or d)), len(keys or d)]
        dcls = {}
        for nme, r in V.X1.items(): dcls.setdefault(r["cls"], []).append(fin(T["dwarf"][nme]))
        o["rq3_systems"] = dict(sparc=cnt(T["disc"]), little_things_rq3=cnt(T["dwarf disc"], lt_rq3), dwarfs={k: [sum(v), len(v)] for k, v in dcls.items()}, xcop=[sum(fin(x[1]) for x in T["cluster_r500"]), len(T["cluster_r500"])],
                                lens="per-bin E1 (B21 bin of the call's stellar mass)" if T["lens"] else "NOT COMPUTABLE", MW=T["MW"], planet=T["planet"], DiskMass="NOT COMPUTABLE (no name in the call)", groups="NOT COMPUTABLE (RQ3 passes NaN gas, as for NP2)", keys="NOT COMPUTABLE (eRASS clusters have no E)", bullet="NOT COMPUTABLE")
        blk = dict(SPARC_A1_A10=bool(o["rq3_systems"]["sparc"][0] == o["rq3_systems"]["sparc"][1] and o["rq3_systems"]["little_things_rq3"][0] == o["rq3_systems"]["little_things_rq3"][1]),
                   dwarfs_A12_A13=all(v[0] == v[1] for v in o["rq3_systems"]["dwarfs"].values()), lens_A30=bool(T["lens"]), xcop_B23_B25=o["rq3_systems"]["xcop"][0] == o["rq3_systems"]["xcop"][1])
        o["rq3_block_computable_U"] = blk
        Eb = K.all_E(c); o["bf1_rows"] = {k: [int(np.isfinite(v[0]).sum()), len(v[0])] for k, v in Eb.items()}
        o["bf1_systems"] = {k: [len({n for n, e in zip(v[1], v[0]) if np.isfinite(e)}), len(set(v[1]))] for k, v in Eb.items()}
        o["cx1_rows"] = {}
        for L in C.CX_LINES:
            q = [x for x in cx["canonical"] if x["line"] == L]; e = [K.cx_E(x, c) for x in q]; o["cx1_rows"][L] = [int(np.sum(np.isfinite(e))), len(q)]
        o["IC1613_E_LT_row"] = V.lt_E("IC 1613", c)
        nx, ns = o["bf1_rows"]["XT"], o["bf1_rows"]["ST"]; o["fit_able"] = bool(nx[0] == nx[1] and ns[0] >= 0.9 * ns[1]); R[c] = o
        P(f"\n== {c} coverage: RQ3 systems {json.dumps(o['rq3_systems'])}"); P(f"   RQ3 blocks computable on U: {blk}"); P(f"   BF1 rows with E {o['bf1_rows']}; systems {o['bf1_systems']}"); P(f"   CX1 rows with E {o['cx1_rows']}; IC 1613 (LT row) E = {o['IC1613_E_LT_row']}"); P(f"   fit-able: {o['fit_able']}")
    R["E1_sigma_median"] = K.SIG_E1; P(f"sigma_E (median per-system sigma_E1 over systems with E1): {K.SIG_E1:.3f}")
    R["status"] = dict(twompz_usable=V.TWOMPZ_USABLE, kids_usable=V.KIDS_USABLE, step0_passed=V.STEP0, lens_graded=V.LENS_GRADED, lens_bins=V.LENS_BINS); P("status:", json.dumps(clean(R["status"])))
    # sign test
    R["sign"] = {}
    for c in V.CANDS:
        for ft, a0 in FEET.items():
            rule = np2_rule(ft); Etr = {}
            for kd in ("X", "S"):
                f = V.xcop_E if kd == "X" else V.sparc_E
                for n in K.NAMES[kd]: Etr[(kd, n)] = f(n, c)
            Ecx = {(q["line"], q["sub"], q["name"]): K.cx_E(q, c) for q in cx[ft]}
            st = K.SignTest(c, rule, a0, cx[ft], Etr); o = st.run(Etr, Ecx)
            # look-elsewhere: E permuted across systems (train systems with E plus CX1 systems with E), 1000 times
            pool = [("T",) + k for k, v in Etr.items() if np.isfinite(v)] + [("C",) + k for k, v in Ecx.items() if np.isfinite(v)]; vals = np.array([Etr[k[1:]] if k[0] == "T" else Ecx[k[1:]] for k in pool])
            g = np.random.default_rng(20261108); labs = []
            if o["label"] != "NOT COMPUTABLE":
                for _ in range(1000):
                    pv = vals[g.permutation(len(vals))]; Et2 = dict(Etr); Ec2 = dict(Ecx)
                    for k, v in zip(pool, pv):
                        if k[0] == "T": Et2[k[1:]] = float(v)
                        else: Ec2[k[1:]] = float(v)
                    labs.append(st.run(Et2, Ec2, nperm=500)["label"])
            o["shuffle_frac_separates"] = float(np.mean([l == "SEPARATES" for l in labs])) if labs else None; o["shuffle_frac_partial_or_better"] = float(np.mean([l in ("SEPARATES", "PARTIAL") for l in labs])) if labs else None
            o["label_after_LEE"] = o["label"] if o["label"] != "SEPARATES" or (o["shuffle_frac_separates"] is not None and o["shuffle_frac_separates"] <= 0.05) else "SEPARATES BY CHANCE (LEE)"
            R["sign"][f"{c}|{ft}"] = o
            P(f"\nsign test {c} {ft}: {o['label_after_LEE']} | train trend rho {o['rho']} p {o['p']} s_train {o['s_train']} ({o['train_systems_with_E']}/{o['train_systems']} systems) | shuffles: SEPARATES {o['shuffle_frac_separates']}, PARTIAL+ {o['shuffle_frac_partial_or_better']}")
            for gname, q in o["groups"].items(): P(f"    {gname}: {json.dumps(clean(q))}")
    R["fit_able"] = [c for c in V.CANDS if R[c]["fit_able"]]; P(f"\nfit-able candidates: {R['fit_able']}  {tm()}"); return R

# ======================================================================= candidate files and stage 3
def write_cand(stem, table, title):
    d = os.path.join(HERE, "candidates"); os.makedirs(d, exist_ok=True); p = os.path.join(d, f"nv2_{stem}.py")
    open(p, "w").write(f'"""NV2 {title}. Frozen admissible GP rule on (log y, log ell, f, E), W3, per footing. A description of data, not a theory; no action. kappa = 1/2 FITTED."""\nimport os, sys\nsys.dont_write_bytecode = True\nsys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))\nimport nv2_cand as _C\n_R = _C.load({stem!r}, {table!r})\nTABLE = _R[1]\nNAME = {("NV2 " + title)!r}; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")\ndef g(Q): return _C.g_of_Q(_R, Q)\n')
    return p
def stage3(path, subset=None, tag=None, flags=()):
    nm = tag or os.path.basename(path)[:-3]; log = os.path.join(HERE, "results", nm + ("_S" if subset else "") + "_stage3.log")
    env = dict(os.environ, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    args = ["nice", "-n", "10", sys.executable, "-I", os.path.join(HERE, "nv2_stage3.py"), path, *flags] + (["--subset", subset, "--tag", nm] if subset else [])
    subprocess.run(args, stdout=open(log, "w"), stderr=subprocess.STDOUT, cwd=HERE, env=env)
    return json.load(open(os.path.join(HERE, "results", nm + ("_S" if subset else "") + ".json")))
def card_rows(card, ft): return card["footings"][ft]["rows"]
def cmp_cards(A, B, ft, skip_nc=True):
    """Rows computed on A must match B (label; Z, value to 1e-6 relative). Returns compared, mismatches, NC on A with reasons."""
    a, b = card_rows(A, ft), card_rows(B, ft); bad = []; nc = {}; n = 0
    for k, v in a.items():
        if v["label"] == "NOT COMPUTABLE": nc[k] = v.get("why", ""); continue
        if k not in b: continue
        w = b[k]; n += 1
        if v["label"] != w["label"]: bad.append((k, v["label"], w["label"])); continue
        for q in ("Z", "value"):
            if isinstance(v.get(q), (int, float)) and isinstance(w.get(q), (int, float)) and abs(v[q] - w[q]) > 1e-6 * max(1.0, abs(w[q])): bad.append((k, q, v[q], w[q]))
    return dict(compared=n, mismatches=bad, not_computable=nc, ok=not bad)

# ======================================================================= fits
def zero_rule(F):
    mu, sd = F.mean(0), F.std(0); return N.CRule(K.ARM, mu, sd, (F - mu) / sd, np.zeros(len(F)), np.ones(4), 0.07)
def check(rule, a0, c, Eb, cx, RT=None):
    """NP2's C4 checker on the 4-leaf arm (wide box, train, holdouts, CX1 rows with E) plus the end-to-end test through NV1's g_core at fixed E per row."""
    ext = []
    for k in ("XT", "ST", "SH", "XH", "LT"):
        A = K.BLOCKS[k][0]; E = Eb[k][0]; m = np.isfinite(E); ext.append((k, K.featsE(A[m], E[m])))
    Ecx = np.array([K.cx_E(q, c) for q in cx]); m = np.isfinite(Ecx)
    if m.any(): ext.append(("CX1", K.cx_F([q for q, ok in zip(cx, m) if ok], Ecx[m])))   # NV2: no CX1 row has E1; an empty set crashes NP2's checker
    o = N.check(rule, a0, ext); R_ = rs_dict(rule); e2e = {}; tot = 0
    for L in C.CX_LINES + ("SPARC",):
        if L == "SPARC":
            E = Eb["SH"][0]; mm = np.isfinite(E); A = C.SH[mm]; gb = A[:, 0]; r = A[:, 2] * C.CL ** 2 / C.A0C; gg = gb * A[:, 3]; EE = E[mm]
        else:
            q_ = [(q, e) for q, e in zip(cx, Ecx) if q["line"] == L and np.isfinite(e)]; gb = np.array([q["gb"] for q, _ in q_]); gg = np.array([max(0.0, q["gg"]) for q, _ in q_]); r = np.array([q["r"] for q, _ in q_]); EE = np.array([e for _, e in q_])
        dec = 0
        for i in range(len(gb)):
            g = np.geomspace(0.3, 3.0, 25) * gb[i]; v = CA.g_core(R_, g, g * (gg[i] / gb[i]), np.full(25, r[i]), a0, EE[i]); dec += bool(np.any(~(np.diff(v) > 0)))
        e2e[L] = dict(n=len(gb), non_monotone=dec); tot += dec
    o["end_to_end"] = e2e; o["violations"] += tot; o["admissible"] = o["violations"] == 0; return o
def fit(c, Eb, a0, plant=None, tag=""):
    K.CUR["cand"] = c; F, t, cls, sid, info = K.train_set(c, Eb, a0, plant.get("XT") if plant else None, plant.get("ST") if plant else None)
    rule = N.fit_admissible(K.ARM, F, t, cls, sid, a0, log=(lambda s: None)); rule.meta["train"] = info; m = rule.meta
    P(f"   {tag}: lam {m['lam']}{' (GRID EDGE)' if m['lam_at_edge'] else ''}, ML ell {np.round(m['ml']['ell'], 3).tolist()} sf {m['ml']['sf']:.3f}; conv {m['fit']['conv']} rounds {m['fit']['rounds']} active {m['fit']['active']}/{m['fit']['working']}; train {info} {tm()}")
    return rule
def mean_dmdE(rule, Eb):
    F = np.vstack([K.featsE(C.XT, Eb["XT"][0]), K.featsE(C.ST, Eb["ST"][0])]); F = F[np.all(np.isfinite(F), 1)]; Zq = rule.std(F); U = np.tile([0, 0, 0, 1.0 / rule.sd[3]], (len(F), 1)); return float(np.mean(rule.dgrad_std(Zq, U)))

# ======================================================================= controls
def controls():
    CV = json.load(open(os.path.join(HERE, "nv2_coverage.json"))); FA = CV["fit_able"]; R = {"fit_able": FA}; cx = {ft: K.cx_rows(ft) for ft in FEET}
    P("NV2 controls (FROZEN_CRITERIA). Read before any real fit. Fit-able candidates:", FA)
    xs = np.log10(C.X_ALL[:, 1] / C.law(C.X_ALL[:, 0], C.A0C)); sys.path.insert(0, C.CXD); import cx1_rows as CR
    lt = np.concatenate([np.log10(s.rows["gobs"] / CR.law(s.rows["gb"], C.A0C)) for s in CR.systems("canonical") if s.sub == "LT"])
    Kn = dict(xcop_mean=round(float(xs.mean()), 4), n=len(xs), lt_median=round(float(np.median(lt)), 4)); Kn["ok"] = bool(abs(Kn["xcop_mean"] - 0.4675) <= 5e-4 and abs(Kn["lt_median"] + 0.0252) <= 5e-4); P("1 known answer:", json.dumps(Kn)); R["known"] = Kn
    LAW = json.load(open(os.path.join(RQ3, "results", "law.json")))
    for c in FA:
        cc = {}; Eb = K.all_E(c); K.CUR["cand"] = c; tab = f"{c}_table"
        F0 = np.vstack([K.featsE(C.XT, Eb["XT"][0]), K.featsE(C.ST, Eb["ST"][0])]); F0 = F0[np.all(np.isfinite(F0), 1)]; zr = zero_rule(F0)
        for ft in FEET: save_rule(zr, f"zero_{c}", ft)
        pz = write_cand(f"zero_{c}", tab, f"zero-weight control, leaf {c} (the plain law where E exists)")
        zU = stage3(pz, flags=("--no-keys", "--no-bullet")); zS = stage3(pz, subset=table_path(tab), flags=("--no-keys", "--no-bullet")); lS = stage3(os.path.join(RQ3, "candidates", "law.py"), subset=table_path(tab), tag=f"nv2_law_{c}", flags=("--no-keys", "--no-bullet"))
        z = {}
        for ft in FEET:
            u = cmp_cards(zU, LAW, ft); s = cmp_cards(zS, lS, ft); s2 = cmp_cards(lS, zS, ft); z[ft] = dict(U=u, S=s, S_rev=s2, ok=bool(u["ok"] and s["ok"] and s2["ok"]))
            P(f"2 zero-weight {c} {ft}: U vs RQ3 law card: {u['compared']} rows compared, mismatches {u['mismatches']}; NOT COMPUTABLE {len(u['not_computable'])}: {u['not_computable']}")
            P(f"  S vs plain law on S: {s['compared']} rows, mismatches {s['mismatches']} (reverse {s2['compared']}, {s2['mismatches']}) -> {'OK' if z[ft]['ok'] else 'FAILED'}")
        cc["zero"] = z; P(f"  subset info: {zS.get('subset')}")
        bump = N.CRule(K.ARM, zr.mu, zr.sd, np.zeros((1, 4)), np.array([-1.5]), np.array([0.3, 1.0, 1.0, 1.0]), 1.0); ch = {}
        for nm_, rule, want in (("bump", bump, False), ("zero", zr, True)):
            o = check(rule, C.A0C, c, Eb, cx["canonical"]); ch[nm_] = dict(check=o, ok=bool(o["admissible"] == want)); P(f"3 checker {c} on {nm_}: violations {o['violations']}, admissible {o['admissible']} (want {want}) -> {'OK' if ch[nm_]['ok'] else 'FAILED'}")
        cc["checker"] = ch
        tab_sys = K.system_table(c); Es = K.all_E(c, K.shuffled(tab_sys, 20261108))
        for ft, a0 in FEET.items():
            Pl = K.plant_adm(a0, noise=True); r4 = fit(c, Eb, a0, Pl, f"{c} {ft} admissible plant N1"); o = K.gates14E(r4, a0, Eb, Pl); k4 = check(r4, a0, c, Eb, cx[ft])
            ok4 = bool(r4.meta["fit"]["conv"] and k4["admissible"] and o["g3"]["ok"] and o["g4"]["ok"]); cc[f"plant_adm|{ft}"] = dict(gates=o, check=k4, meta=r4.meta, ok=ok4); P(f"4 {c} {ft} admissible plant: {K.g14s(o)} | checker {k4['violations']} | {'OK' if ok4 else 'FAILED'}")
            ET = np.r_[Eb["XT"][0], Eb["ST"][0]]; ET = ET[np.isfinite(ET)]; mE, sE = float(ET.mean()), float(ET.std())
            boost = {k: 0.15 * (Eb[k][0] - mE) / sE for k in K.BLOCKS}; Pb = K.plant_adm(a0, noise=True, boost=boost)
            ra = fit(c, Eb, a0, Pb, f"{c} {ft} planted non-local boost, true E"); oa = K.gates14E(ra, a0, Eb, Pb); ka = check(ra, a0, c, Eb, cx[ft]); sl = mean_dmdE(ra, Eb)
            rb = fit(c, Es, a0, Pb, f"{c} {ft} planted non-local boost, shuffled E"); ob = K.gates14E(rb, a0, Es, Pb)
            want = 0.15 / sE; ok5 = bool(ra.meta["fit"]["conv"] and ka["admissible"] and oa["g3"]["ok"] and oa["g4"]["ok"] and oa["g3S"]["rms"] <= 0.85 * ob["g3S"]["rms"] and 0.5 * want <= sl <= 1.5 * want)
            cc[f"plant_nonlocal|{ft}"] = dict(true=dict(gates=oa, check=ka, meta=ra.meta, dmdE=sl), shuffled=dict(gates=ob, meta=rb.meta), planted_dmdE=want, ok=ok5)
            P(f"5 {c} {ft} planted boost: true E {K.g14s(oa)} | checker {ka['violations']} | mean dm/dE {sl:.4f} (planted {want:.4f})"); P(f"   shuffled E {K.g14s(ob)} | SPARC-even rms true {oa['g3S']['rms']:.4f} vs shuffled {ob['g3S']['rms']:.4f} (need <= 0.85x) -> {'OK' if ok5 else 'FAILED'}")
        cc["ok"] = bool(Kn["ok"] and all(z[f]["ok"] for f in FEET) and all(v["ok"] for v in ch.values()) and all(cc[f"{q}|{f}"]["ok"] for q in ("plant_adm", "plant_nonlocal") for f in FEET))
        R[c] = cc; P(f"{c} controls {'ALL OK' if cc['ok'] else 'FAILED'} {tm()}")
    return R

# ======================================================================= real
def real():
    if not os.path.exists(os.path.join(HERE, "nv2_controls.json")): sys.exit("controls unread; they read first, per FROZEN_CRITERIA")
    CT = json.load(open(os.path.join(HERE, "nv2_controls.json"))); CV = json.load(open(os.path.join(HERE, "nv2_coverage.json"))); R = {}; cx = {ft: K.cx_rows(ft) for ft in FEET}
    for c in CT["fit_able"]:   # AMENDMENT_A2: control 2 as frozen (rows computed on the zero card match); the reverse S check is reported, not gated
        cc = CT[c]; cc["ok_as_run"] = cc["ok"]; cc["ok"] = bool(CT["known"]["ok"] and all(cc["zero"][f]["U"]["ok"] and cc["zero"][f]["S"]["ok"] for f in FEET) and all(v["ok"] for v in cc["checker"].values()) and all(cc[f"{q}|{f}"]["ok"] for q in ("plant_adm", "plant_nonlocal") for f in FEET))
    NP2U = json.load(open(os.path.join(NP2D, "results", "np2_real_L3_F.json"))); P("controls read:", {c: CT[c]["ok"] for c in CT["fit_able"]})
    for c in CT["fit_able"]:
        Eb = K.all_E(c); K.CUR["cand"] = c; tab = f"{c}_table"; T = json.load(open(table_path(tab))); G = {}
        # E-shuffle MUTATE table (seed 20261109): tabulated systems shuffled; on-the-fly E mapped through the nearest tabulated original (nv2_cand._em1)
        keys = [("disc", k) for k, v in T["disc"].items() if fin(v)] + [("dwarf disc", k) for k, v in T["dwarf disc"].items() if fin(v)] + [("dwarf", k) for k, v in T["dwarf"].items() if fin(v)] + [("cluster", x[2]) for x in T["cluster_r500"] if fin(x[1])] + [("lens", b) for b, v in enumerate(T.get("lens_bins", [])) if T.get("lens") == "BINS" and fin(v)]
        val = {("disc", k): T["disc"][k] for k in T["disc"]}; val.update({("dwarf disc", k): T["dwarf disc"][k] for k in T["dwarf disc"]}); val.update({("dwarf", k): T["dwarf"][k] for k in T["dwarf"]}); val.update({("cluster", x[2]): x[1] for x in T["cluster_r500"]}); val.update({("lens", b): v for b, v in enumerate(T.get("lens_bins", []))})
        v0 = np.array([val[k] for k in keys]); pm = np.random.default_rng(20261109).permutation(len(keys)); sv = {k: float(v0[pm[i]]) for i, k in enumerate(keys)}
        TM = json.loads(json.dumps(T)); TM["disc"] = {k: sv.get(("disc", k)) for k in T["disc"]}; TM["dwarf disc"] = {k: sv.get(("dwarf disc", k)) for k in T["dwarf disc"]}; TM["dwarf"] = {k: sv.get(("dwarf", k)) for k in T["dwarf"]}
        TM["cluster_r500"] = [[x[0], sv.get(("cluster", x[2])), x[2]] for x in T["cluster_r500"]]; TM["lens_bins"] = [sv.get(("lens", b)) for b in range(len(T.get("lens_bins", [])))]
        for kk in ("MW", "planet"):
            if fin(T[kk]): TM[kk] = float(TM["mut_map"][1][int(np.abs(np.array(TM["mut_map"][0]) - T[kk]).argmin())])
        json.dump(clean(TM), open(table_path(f"{c}_table_MUTATE"), "w"), indent=0)
        emapM = {}
        for kd, nm in K.NAMES.items():
            for n in nm:
                if kd == "S": e = TM["disc"].get(n)
                elif kd == "X": e = next((x[1] for x in TM["cluster_r500"] if x[2] == n), None)
                else: e = TM["dwarf disc"].get(n)
                emapM[(kd, n)] = float(e) if fin(e) else np.nan
        EbM = K.all_E(c, emapM)
        for ft, a0 in FEET.items():
            P(f"\n== {c} {ft} {tm()}"); rule = fit(c, Eb, a0, None, "real"); save_rule(rule, f"real_{c}", ft); o = K.gates14E(rule, a0, Eb); ck = check(rule, a0, c, Eb, cx[ft])
            P(f"   {K.g14s(o)}"); P(f"   checker violations {ck['violations']}, admissible {ck['admissible']}; end-to-end {ck['end_to_end']}; mean dm/dE {mean_dmdE(rule, Eb):+.4f}")
            rM = fit(c, EbM, a0, None, "MUTATE (E shuffled)"); save_rule(rM, f"mutate_{c}", ft); oM = K.gates14E(rM, a0, EbM); P(f"   MUTATE {K.g14s(oM)}")
            G[ft] = dict(meta=rule.meta, gates=o, check=ck, dmdE=mean_dmdE(rule, Eb), mutate=dict(meta=rM.meta, gates=oM))
        pr = write_cand(f"real_{c}", tab, f"real L3+{c} mode F"); pm_ = write_cand(f"mutate_{c}", f"{c}_table_MUTATE", f"MUTATE L3+{c} (E shuffled)")
        cards = dict(NV2_U=stage3(pr), NV2_S=stage3(pr, subset=table_path(tab)), MUT_U=stage3(pm_), MUT_S=stage3(pm_, subset=table_path(tab)), NP2_S=stage3(os.path.join(NP2D, "candidates", "np2_real_L3_F.py"), subset=table_path(tab), tag=f"nv2_np2_L3_F_{c}"))
        for k, v in cards.items(): P(f"   card {k}: {{{', '.join(f'{ft}: ' + v['footings'][ft]['summary']['overall'] + ' ' + str(v['footings'][ft]['summary']['counts']) for ft in FEET)}}}; subset {v.get('subset')}")
        G["cards"] = {k: {ft: {r: dict(label=x["label"], Z=x.get("Z"), value=x.get("value") if not isinstance(x.get("value"), dict) else None, why=x.get("why")) for r, x in v["footings"][ft]["rows"].items()} for ft in FEET} for k, v in cards.items()}
        G["cards"]["NP2_U"] = {ft: {r: dict(label=x["label"], Z=x.get("Z"), value=x.get("value") if not isinstance(x.get("value"), dict) else None) for r, x in NP2U["footings"][ft]["rows"].items()} for ft in FEET}
        G["labels"] = label(c, G, CT[c]["ok"]); R[c] = G
    R["lane"] = lane_label(R, CT, CV); return R
def zabs(r):
    return abs(r["Z"]) if r and r.get("label") in ("PASS", "FAIL") and isinstance(r.get("Z"), (int, float)) else None
def label(c, G, ctl):
    L = {}; P(f"\n==== {c}: before/after per target row (Z; label)")
    for ft in FEET:
        cd = {k: G["cards"][k][ft] for k in G["cards"]}; o = G[ft]; rows = {}; moved = []
        for t in TARGETS:
            q = {k: (cd[k].get(t, {}).get("label"), cd[k].get(t, {}).get("Z")) for k in ("NP2_U", "NP2_S", "NV2_U", "NV2_S", "MUT_U", "MUT_S")}; rows[t] = q
            for card in ("U", "S"):
                b, a, m = zabs(cd["NP2_" + card].get(t)), zabs(cd["NV2_" + card].get(t)), zabs(cd["MUT_" + card].get(t))
                if b is None or a is None: continue
                fall = b - a; turned = cd["NP2_" + card][t]["label"] == "FAIL" and cd["NV2_" + card][t]["label"] == "PASS"
                if fall >= 1.0 or turned:
                    mf = (b - m) if m is not None else None; real_ = mf is None or mf < 0.5 * fall
                    moved.append(dict(row=t, card=card, before=b, after=a, mutate=m, survives_mutate=bool(real_)))
            P(f"  {ft} {t}: " + " | ".join(f"{k} {v[0]} {v[1]:+.2f}" if isinstance(v[1], (int, float)) else f"{k} {v[0]}" for k, v in q.items()))
        g14 = o["gates"]; adm = bool(o["check"]["admissible"] and o["meta"]["fit"]["conv"]); g5 = all(cd["NV2_U"].get(k, {}).get("label") == "PASS" for k in ("A1", "A2")) and fin(cd["NV2_U"].get("A3", {}).get("value")) and abs(cd["NV2_U"]["A3"]["value"]) <= 0.15
        allT = all(cd["NV2_U"].get(t, {}).get("label") == "PASS" for t in TARGETS); broke = sorted(k for k, v in cd["NP2_U"].items() if v["label"] == "PASS" and cd["NV2_U"].get(k, {}).get("label") == "FAIL")
        mut_stops = any(cd["MUT_U"].get(t, {}).get("label") != "PASS" for t in TARGETS)
        if not ctl: lab = "NOT COMPUTABLE (controls)"
        elif not adm: lab = "UNDETERMINED (INADMISSIBLE)"
        elif not (g14["g1"]["ok"] and g14["g2"]["ok"]): lab = "UNDETERMINED (UNDERFIT)"
        elif g14["g3"]["ok"] and g14["g4"]["ok"] and g5 and allT and not broke and mut_stops: lab = f"ONE VARIABLE RESOLVES ({c})"
        elif any(m_["survives_mutate"] for m_ in moved): lab = "PARTIAL"
        else: lab = "DOES NOT RESOLVE"
        L[ft] = dict(label=lab, gates_ok={k: g14[k]["ok"] for k in ("g1", "g2", "g3S", "g3X", "g4")}, g5_U=bool(g5), targets_all_pass_U=allT, broke_on_U=broke, moved=moved, rows=rows)
        P(f"  {c} {ft}: {lab}; gates {L[ft]['gates_ok']}, G5 on U {g5}; moved {moved}; NP2-passing rows failing on U {broke}")
    return L
def lane_label(R, CT, CV):
    out = {}
    for ft in FEET:
        labs = {c: R[c]["labels"][ft]["label"] for c in CT["fit_able"] if c in R}
        if any(v.startswith("ONE VARIABLE RESOLVES") for v in labs.values()): lab = [v for v in labs.values() if v.startswith("ONE")][0]
        elif not labs and all(CV["sign"][f"{c}|{ft}"]["label"] == "NOT COMPUTABLE" for c in V.CANDS): lab = "NOT COMPUTABLE"
        else: lab = "NO SINGLE NON-LOCAL VARIABLE ON RECORD RESOLVES" + (" (PARTIAL: " + ", ".join(f"{c} " + ", ".join(f"{m['row']} on {m['card']} {m['before']:.2f} -> {m['after']:.2f}" for m in R[c]["labels"][ft]["moved"] if m["survives_mutate"]) for c, v in labs.items() if v == "PARTIAL") + ")" if any(v == "PARTIAL" for v in labs.values()) else "")
        out[ft] = dict(label=lab, per_candidate=labs, sign_tests={c: CV["sign"][f"{c}|{ft}"]["label_after_LEE"] for c in V.CANDS}); P(f"\nLANE {ft}: {lab}; per candidate {labs}; sign tests {out[ft]['sign_tests']}")
    return out

if __name__ == "__main__":
    R = coverage() if MODE == "coverage" else controls() if MODE == "controls" else real() if MODE == "real" else sys.exit("mode?")
    P(f"\n{tm()}. kappa = 1/2 FITTED; not theory closed. A pass is a description of data, not a theory.")
    json.dump(clean(R), open(os.path.join(HERE, f"nv2_{MODE}.json"), "w"), indent=0); open(os.path.join(HERE, f"nv2_{MODE}.out"), "w").write("\n".join(OUT) + "\n")
