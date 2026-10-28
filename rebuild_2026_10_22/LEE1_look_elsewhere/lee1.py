#!/usr/bin/env python3
"""LEE1_look_elsewhere: census of every full-line-set configuration graded (CF1/CF2/CL1/CL2/CL3) + pass fraction from 24
seeded uniform draws in the explored box (T 12.0-12.6, L 3.5-4.5; CL2 harness, S9 slope, measured cluster budget).
FROZEN_CRITERIA.md committed alone first (4eee317c09). Harness: CL2 (b57ed8751f).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I lee1.py      (LEE1_MUTATE=1 twin)
"""
import os, sys, json, math, time, resource, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X53_MUTATE", None); os.environ.pop("X30_MUTATE", None)
import numpy as np

T0 = time.time(); MUTATE = os.environ.get("LEE1_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
P(f"LEE1_look_elsewhere  {'MUTATE (flag inverted; S0a target x1.01)' if MUTATE else 'normal run'}   (harness CF1 / X62 8c7768d26d)")
P("kappa = 1/2 FITTED; footings never pooled; ENV: route E if satellite or above crossover, else the law on baryons (no halo); not theory closed")

# ------------------------------------------------------------------ the law floor (shared by every scorer)
MODE = {"m": "on"}
STAT = {}
def _new(): return dict(n=0, viol=0, law=0)
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / y)
def _combine(law, rE, key, above):
    if MODE["m"] == "off": return rE
    if MODE["m"] == "law": return law
    use_rE = (not above) if MUTATE else above                                       # MUTATE: the flag inverted
    out = rE if use_rE else law
    exp = rE if above else law                                                      # the branch the flag selects
    s = STAT.setdefault(key, _new()); tol = 1e-12 * np.maximum(np.abs(exp), 1e-300)
    s["n"] += 1; s["viol"] += int(np.any(np.abs(out - exp) > tol)); s["law"] += int(not above)
    return out
LAST = {"law": False}
def LF_G(gb, gh, a0, key="g", above=False):
    """pull: gb = baryonic Newtonian pull (any units, a0 in the same units), gh = halo pull."""
    gb = np.asarray(gb, float); gh = np.broadcast_to(np.asarray(gh, float), np.broadcast(gb, np.asarray(gh)).shape)
    gbb = np.broadcast_to(gb, gh.shape); pos = gbb > 0
    law = np.where(pos, nu(np.where(pos, gbb, 1.0) / a0) * gbb, gbb)
    return _combine(law, gbb + gh, key, bool(above))
def LF_M(Mb, Mh, r, G, a0, key="M", above=False):
    """enclosed mass: Mb, Mh on radius grid r (consistent units with G, a0)."""
    Mb = np.asarray(Mb, float); Mh = np.asarray(Mh, float); r = np.asarray(r, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        law = np.where((r > 0) & (Mb > 0), Mb * nu(np.maximum(G * Mb / np.where(r > 0, r, 1.0) ** 2, 1e-300) / a0), Mb)
    out = _combine(law, Mb + Mh, key, bool(above))
    LAST["law"] = bool(MODE["m"] == "law" or (MODE["m"] == "on" and (bool(above) == MUTATE)))
    return out

def run_copy(src_path, edits, fname, extra=None):
    src = open(src_path).read()
    for old, new in edits:
        assert src.count(old) == 1, (src_path, old[:60]); src = src.replace(old, new)
    ns = {"__file__": os.path.join(HERE, fname), "__name__": fname[:-3], "LF_G": LF_G, "LF_M": LF_M, "LAST": LAST}
    if extra: ns.update(extra)
    argv0 = sys.argv; sys.argv = [ns["__file__"]]
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try: exec(compile(src, ns["__file__"], "exec"), ns)
            except SystemExit: pass
    finally:
        sys.argv = argv0
    return ns

# ------------------------------------------------------------------ A. X43 scorer (SPARC, groups, clusters), X48 ng48 eta
CFFILE = {"a2": ("x48_regrade_A2.json", "x48_analyze_results_ng48_A2.json"), "s3": ("x48_regrade_ng48.json", "x48_analyze_results_ng48.json")}
TABS = {k: json.load(open(os.path.join(REB, "X48_native_cf_zoom", v[0])))["table"] for k, v in CFFILE.items()}
B1 = 3 * math.log(2) - math.pi / 2
def eta_tab(k):
    LMk, CFk = np.array(TABS[k]["lgM"]), np.array(TABS[k]["cf"])
    return lambda M: 4.0 / (3.0 * B1) * float(np.interp(math.log10(M), LMk, CFk)) ** 1.25

S_MEAS = json.load(open(os.path.join(REB, "GS1_measured_gas_outskirts", "gs1_gas_slope_results.json")))["slope"]["s_meas"]
NAT_h, NAT_OM, NAT_wb = 0.6856427, 0.2976016, 0.0223081
NAT_OB = NAT_wb / NAT_h ** 2; NAT_RRAT = (NAT_OM - NAT_OB) / NAT_OB
GC2X = """
GC2_LOG = []
def _gc2_ext(Mg500, R500, z, Mbt_cut):
    r = RG; rc = 0.15*R500; beta = 2/3; sh = (1 + (r/rc)**2)**(-1.5*beta)
    Rm = R500; sm = (1 + (Rm/rc)**2)**(-1.5*beta)
    sh = np.where(r > Rm, sm*(r/Rm)**-GC2_SLOPE, sh)
    dm = 4*np.pi*(r*MPC)**2*sh; M = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(r*MPC))]
    Mbx = 1.2*M*(Mg500*MSUN/np.interp(R500, r, M))
    rta = r_ta_com(Mbt_cut)/(1 + z)
    for n in range(1, 200):
        Mbt = float(np.interp(rta, RM, Mbx)); new = r_ta_com(Mbt)/(1 + z)
        if abs(new/rta - 1) < 1e-6: rta = new; break
        rta = new
    Mbt = float(np.interp(rta, RM, Mbx))
    GC2_LOG.append(float(Mbt/Mbt_cut))
    return np.where(RM <= rta, Mbx, Mbt), Mbt
"""
def budget_edit():
    old_prep = '    Mg500 = cl["Mgas500"]*qd**2.5; R500 = cl["R500"]*qd; Mg, rho_g = gas(Mg500, R500, "P"); Mb = Mg*(1 + 0.20); Mbt = float(Mb[-1])'
    pre = 'NX = {"__file__": X30SRC, "__name__": "x30_ro", "GC2_SLOPE": %r}\n' % S_MEAS
    pre += 'assert codeX.count(%r) == 1\n' % old_prep
    pre += 'codeX = codeX.replace(%r, %r)\n' % (old_prep, old_prep + '\n    Mb, Mbt = _gc2_ext(Mg500, R500, cl["z"], Mbt)')
    pre += 'codeX = codeX.replace("PREP = {}\\ndef prep", %r + "PREP = {}\\ndef prep")\n' % GC2X
    pre += ('codeX = codeX.replace("H0_946 = 67.4e3/MPC946", "H0_946 = %r*100e3/MPC946")\n'
            'codeX = codeX.replace("OB946 = 0.0493; OC946 = 5.364*OB946", "OB946 = %r; OC946 = %r*OB946")\n'
            'codeX = codeX.replace("Mfair=5.364*Mbt", "Mfair=%r*Mbt")\n'
            'assert all(t in codeX for t in ("_gc2_ext", "H0_946 = %r", "Mfair=%r"))' % (NAT_h, NAT_OB, NAT_RRAT, NAT_RRAT, NAT_h, NAT_RRAT))
    return ('NX = {"__file__": X30SRC, "__name__": "x30_ro"}', pre)

_A2 = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_analyze_results_ng48_A2.json")))
_S3 = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_analyze_results_ng48.json")))
def _med_nfw(M):
    v = [x["c_nfw_fit"] for k, x in _A2["runs"].items() if k.startswith("M" + M) and k.endswith("ng48") and x.get("c_nfw_fit") is not None]
    return float(np.median(v))
SHAPES = {"S9": [_A2["cf_by_mass"][k] for k in ("1e+12", "1e+13", "1e+14")],
          "SN": [_med_nfw(m) for m in ("1e12", "1e13", "1e14")],
          "S3": [_S3["cf_by_mass"][k] for k in ("1e+12", "1e+13", "1e+14")],
          "FLAT": [1.0, 1.0, 1.0]}
SHAPES["INV"] = [SHAPES["S9"][2] ** 2 / c for c in SHAPES["S9"]]
def cf_table(shape, L):
    c = SHAPES[shape]

    return [L * v / c[2] for v in c]
def run_x43(mode, cfmode):
    MODE["m"] = mode; tag = f"{mode}_{cfmode}{TAG}"
    ed = [('sc = ETA_USE["v"] * sigma_coll(tag, M)[0] * MSUNE / PC2',
           'sc = (ETA_FUN(M) if (ETA_FUN is not None and ETA_USE["v"] == ETA) else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2'),
          ('rows.append(fit_one(q, np.log10(np.maximum(q["GB"] + (GE * Mh / q["Rm"] ** 2)[:, None], 1e-300))))',
           'rows.append(fit_one(q, np.log10(np.maximum(LF_G(q["GB"], (GE * Mh / q["Rm"] ** 2)[:, None], A0[f], "sparc", a_), 1e-300))))'),
          ('V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)', 'V[i] = dvecN(int(i), foot, hk, LF_M(pp["Mb"], Mh, RM, GX, A0[foot], "clusters", a_))'),
          ('Mh = math.pi * sc * r0 ** 2 * B(np.minimum(rr, R200) / r0); gN = gN + Mh / Mb / XG ** 2',
           'Mh = math.pi * sc * r0 ** 2 * B(np.minimum(rr, R200) / r0); gN = LF_G(gN, Mh / Mb / XG ** 2, A0[foot] / (G540 * Mb / a ** 2), "groups" if dlM == 0.0 else "groups_d", act)'),
          ("for cf in (3.0, 5.0):", "for cf in ():"),
          ('f"x43_collapse_core{TAG}.out"', f'"x62_x43copy_{tag}.out"'), ('f"x43_collapse_core_results{TAG}.json"', f'"x62_x43copy_{tag}_results.json"'),
          ('"x43_x30_machinery"', '"x62_x30_machinery"')]
    ETAF = eta_tab(cfmode) if cfmode in TABS else None
    if cfmode.startswith("shp"):
        body = cfmode[3:]; usebud = body.endswith("_B"); body = body[:-2] if usebud else body
        shp, rest = body.split("_L"); Lv, _, tv = rest.partition("_T")
        tab = cf_table(shp, float(Lv))
        ETAF = (lambda M, tab=tab: 4.0 / (3.0 * B1) * float(np.interp(math.log10(M), [12.0, 13.0, 14.0], tab)) ** 1.25)
        if tv: ed.append(("    return max(s, sc), sc > s", "    return max(s, sc), M > 10 ** " + tv))
        if usebud: ed.append(budget_edit())
    if cfmode.startswith("cfv"):
        body = cfmode[3:]; usebud = body.endswith("_B"); body = body[:-2] if usebud else body
        cfv, _, tv = body.partition("_T")
        ed.append(("CF = 4.0", "CF = " + cfv))
        if tv: ed.append(("    return max(s, sc), sc > s", "    return max(s, sc), M > 10 ** " + tv))
        if usebud: ed.append(budget_edit())
    ns = run_copy(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py"), ed, "x62_x43copy.py", {"ETA_FUN": ETAF})
    lg = ns["NX"].get("GC2_LOG", []) if "NX" in ns else []
    ns["RES"]["_budget"] = {"n": len(lg), "n_changed": int(sum(abs(v - 1) > 1e-6 for v in lg))}
    return ns["RES"], ns["LAW"]

# ------------------------------------------------------------------ B. X53 scorer (lensing)
def run_x53(mode, cfmode):
    MODE["m"] = mode; tag = f"{mode}_{cfmode}{TAG}"
    ed = [('return Mb + Mh, (M200, R200, Sig, above)', 'return LF_M(Mb, Mh, RGRID_PC, Gpc, a0u(foot), "lensing", above), (M200, R200, Sig, above)'),
          ('tab[gi] = AQ.delta_sigma(Rn[b] * 1e6, RGRID_PC, M, "const")', 'tab[gi] = AQ.delta_sigma(Rn[b] * 1e6, RGRID_PC, M, "linear" if (halo and LAST["law"]) else "const")'),
          ('os.path.join(HERE, "x53_step0_results.json")', repr(os.path.join(REB, "X53_outer_lensing_law_vs_halos", "x53_step0_results.json"))),
          ('H_PRIMARY = dict(bg="A_c2b_refit", cf="cf4", zR200=None)', f'H_PRIMARY = dict(bg="A_c2b_refit", cf="{"cf4" if cfmode == "cf4" else "x48"}", zR200=None)'),
          ('"x48_analyze_results_ng48.json"', repr(CFFILE[cfmode][1]) if cfmode in CFFILE else '"x48_analyze_results_ng48.json"'),
          ("absorbed=1 - res / e0", "absorbed=1 - res / max(e0, 1e-300)"), ("100 * (1 - res / e0)", "100 * (1 - res / max(e0, 1e-300))"),
          ("{25.0 / e:.2f}", "{25.0 / max(e, 1e-300):.2f}"),   # reported-only lines; e0 = 0 when the two models coincide (law mode)
          ('f"x53_outer_lensing_results{SFX}.json"', f'"x62_x53copy_{tag}_results.json"'), ('f"x53_outer_lensing{SFX}.out"', f'"x62_x53copy_{tag}.out"')]
    if cfmode.startswith("shp"):
        shp, rest = cfmode[3:].split("_L"); Lv, _, tv = rest.partition("_T")
        ed.append(('cf = 4.0 if cfmode == "cf4" else float(np.interp(math.log10(M), CF48_L, CF48_C))', "cf = float(np.interp(math.log10(M), [12.0, 13.0, 14.0], %r))" % cf_table(shp, float(Lv))))
        if tv: ed.append(("return M200, R200, solve_r0(M200, R200, Sig), Sig, sc > SIGA0[foot]", "return M200, R200, solve_r0(M200, R200, Sig), Sig, M200 > 10 ** " + tv))
    if cfmode.startswith("cfv"):
        cfv, _, tv = cfmode[3:].partition("_T")
        ed.append(('cf = 4.0 if cfmode == "cf4" else float(np.interp(math.log10(M), CF48_L, CF48_C))', "cf = " + cfv))
        if tv: ed.append(("return M200, R200, solve_r0(M200, R200, Sig), Sig, sc > SIGA0[foot]", "return M200, R200, solve_r0(M200, R200, Sig), Sig, M200 > 10 ** " + tv))
    ns = run_copy(os.path.join(REB, "X53_outer_lensing_law_vs_halos", "x53_outer_lensing.py"), ed, "x62_x53copy.py")
    return ns["FT"]

# ------------------------------------------------------------------ C. X51 scorer (dwarfs)
def run_x51(mode):
    MODE["m"] = mode; tag = f"{mode}{TAG}"
    ed = [("gp = gN + G * Mh / r12 ** 2", 'gp = float(LF_G(gN, G * Mh / r12 ** 2, A0[f], "dwarfs", r["host"] in ("MW", "M31")))'),
          ('f"x51_dwarfs{TAG}.out"', f'"x62_x51copy_{tag}.out"'), ('f"x51_dwarfs_results{TAG}.json"', f'"x62_x51copy_{tag}_results.json"')]
    ns = run_copy(os.path.join(REB, "X51_dwarf_cooling_floor", "x51_dwarfs.py"), ed, "x62_x51copy.py")
    return ns["RES"]

import multiprocessing as _mp
def _child(name, args):
    STAT.clear(); r = globals()[name](*args); return r, {k: dict(v) for k, v in STAT.items()}
def call(fn, *args):
    """K3: each scorer execution in its own forked process; branch counters merged back."""
    with _mp.get_context("fork").Pool(1, maxtasksperchild=1) as pool:
        r, st = pool.apply(_child, (fn.__name__, args))
    for k, v in st.items():
        d = STAT.setdefault(k, _new())
        for kk in d: d[kk] += v[kk]
    return r
def rss_all():
    return max(rss(), resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6))
FEET = ("canonical", "alt"); checks = []; RES = dict(criteria="4eee317c09", harness="CL2 b57ed8751f", mutate=MUTATE)
def rel(a, b): return abs(a / b - 1)
# ---------- K0: route E alone reproduces the source lanes
R43off, LAW = call(run_x43, "off", "a2")
X48J = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_regrade_A2.json")))["footings"]
k0a = all(rel(R43off["footings"][f]["sparc"]["A_c2b_refit"]["rms"], X48J[f]["sparc"]["rms"]) < 1e-3 and abs(R43off["footings"][f]["groups"]["Z"] - X48J[f]["groups"]["Z"]) < 1e-3 for f in FEET)
P(f"K0a law branch off reproduces X48 A2 regrade (SPARC " + ", ".join(f"{R43off['footings'][f]['sparc']['A_c2b_refit']['rms']:.4f}" for f in FEET) + ", groups Z " + ", ".join(f"{R43off['footings'][f]['groups']['Z']:+.3f}" for f in FEET) + f"): {'PASS' if k0a else 'FAIL'}  [{time.time() - T0:.0f} s]")
F53off4 = call(run_x53, "off", "cf4"); X53J = json.load(open(os.path.join(REB, "X53_outer_lensing_law_vs_halos", "x53_outer_lensing_results.json")))["footings"]
k0b = all(rel(F53off4[f]["all"]["H2H"]["chi2"], X53J[f]["all"]["H2H"]["chi2"]) < 1e-3 for f in FEET)
P(f"K0b law branch off reproduces X53 H2H at c_f 4 (" + ", ".join(f"{F53off4[f]['all']['H2H']['chi2']:.1f}" for f in FEET) + f"; X53 583.9 / 580.6): {'PASS' if k0b else 'FAIL'}  [{time.time() - T0:.0f} s]")
R51off = call(run_x51, "off"); X51J = json.load(open(os.path.join(REB, "X51_dwarf_cooling_floor", "x51_dwarfs_results.json")))["footings"]
k0c = all(abs(R51off["footings"][f]["classes"][c]["median"] - X51J[f]["classes"][c]["median"]) < 1e-3 for f in FEET for c in X51J[f]["classes"])
P(f"K0c law branch off reproduces X51 class medians: {'PASS' if k0c else 'FAIL'}")
checks += [("K0a_x48", k0a), ("K0b_x53", k0b), ("K0c_x51", k0c)]
# ---------- K2: halo branch off reproduces the law
R43law, _ = call(run_x43, "law", "a2"); F53law = call(run_x53, "law", "a2")
k2a = all(rel(R43law["footings"][f]["sparc"]["A_c2b_refit"]["rms"], LAW[f]["rms"]) < 1e-3 for f in FEET)
k2b = all(rel(F53law[f]["all"]["H"]["chi2"], X53J[f]["all"]["L"]["chi2"]) < 1e-3 for f in FEET)
P(f"K2 halo branch off: SPARC " + ", ".join(f"{R43law['footings'][f]['sparc']['A_c2b_refit']['rms']:.4f}" for f in FEET) + f" (EM1 LAW {LAW['canonical']['rms']:.4f} / {LAW['alt']['rms']:.4f}): {'PASS' if k2a else 'FAIL'}; "
  f"lensing chi2 " + ", ".join(f"{F53law[f]['all']['H']['chi2']:.1f}" for f in FEET) + f" (X53 L 160.7 / 127.6): {'PASS' if k2b else 'FAIL'}  [{time.time() - T0:.0f} s]")
checks += [("K2a_sparc_law", k2a), ("K2b_lensing_law", k2b)]
def grade(R43_, F53_, F53re_, R51_, lab):
    out = {}
    for f in FEET:
        F = R43_["footings"][f]; sp = {t: F["sparc"][t] for t in F["sparc"]}; gr = F["groups"]; cl = F["clusters"]
        c0 = cl["cells"]["h0672"]; dw = R51_["footings"][f]["classes"]
        Lf, Lre = F53_[f]["all"], F53re_[f]["all"]
        dL = Lf["H2H"]["chi2"] - Lf["L2H"]["chi2"]; dE = Lf["H2H"]["chi2"] - Lre["H2H"]["chi2"]
        dLp = F53_[f]["primary"]["H2H"]["chi2"] - F53_[f]["primary"]["L2H"]["chi2"]
        fails = []
        if not all(s["line"] for s in sp.values()): fails.append("SPARC line")
        if not gr["PASS"]: fails.append(f"groups ({gr['verdict']}, Z {gr['Z']:+.2f})")
        fails += cl["fails"]
        fails += [f"dwarfs {c} ({'UNDER' if v['median'] > 0 else 'OVER'}, Z {v['Z']:+.2f})" for c, v in dw.items() if not abs(v["Z"]) < 2]
        if not (dL <= 9.0 and dE < 0): fails.append(f"lensing (ENV2H-L2H {dL:+.1f}, ENV2H-H2H {dE:+.1f})")
        v = "ENVIRONMENT SWITCH UNIFIES" if not fails else "ENV FAILS: " + ", ".join(fails)
        P(f"\n=== [{f}] {lab}")
        for t, s in sp.items(): P(f"  SPARC [{t}]: rms {s['rms']:.4f}, median U {s['U_median']:.2f}, line {'PASS' if s['line'] else 'FAIL'}")
        P(f"  groups: mean {gr['mean']:+.4f} Z {gr['Z']:+.2f} -> {gr['verdict']}")
        P("  clusters: " + "; ".join(f"{k} {c0[k]['pred']:.2f}/{c0[k]['meas']:.2f} Z {c0[k]['Z']:+.2f}{'' if cl['ok'][k] else ' FAIL'}" for k in c0))
        P("  dwarfs: " + "; ".join(f"{c} {d['median']:+.3f} (Z {d['Z']:+.2f})" for c, d in dw.items()))
        P("  dwarf individuals: " + "; ".join(f"{k} {v:+.2f}" for k, v in R51_["footings"][f]["individuals"].items()))
        P(f"  lensing all radii: L2H {Lf['L2H']['chi2']:.1f}, ENV2H {Lf['H2H']['chi2']:.1f}, route-E H2H {Lre['H2H']['chi2']:.1f}; dchi2(ENV2H-L2H) {dL:+.1f}, dchi2(ENV2H-H2H) {dE:+.1f}; primary R<=0.31 Mpc dchi2(ENV2H-L2H) {dLp:+.1f}")
        P(f"  VERDICT [{f}] ({lab}): {v}")
        out[f] = dict(verdict=v, fails=fails, sparc={t: dict(rms=s["rms"], U=s["U_median"], line=s["line"]) for t, s in sp.items()},
                      groups=dict(mean=gr["mean"], Z=gr["Z"], verdict=gr["verdict"]), clusters={k: dict(pred=c0[k]["pred"], meas=c0[k]["meas"], Z=c0[k]["Z"], ok=cl["ok"][k]) for k in c0},
                      dwarfs={c: dict(median=d["median"], Z=d["Z"]) for c, d in dw.items()},
                      lensing=dict(L2H=Lf["L2H"]["chi2"], ENV2H=Lf["H2H"]["chi2"], H2H=Lre["H2H"]["chi2"], d_LF_L=dL, d_LF_H=dE, d_LF_L_primary=dLp))
    return out

import re
def crossover(tag):
    t = open(os.path.join(HERE, f"x62_x43copy_on_{tag}{TAG}.out")).read()
    return {f: float(re.search(r"crossover eta Sigma_coll = Sigma_a0 \[" + f + r"\]: M = 10\^([0-9.]+)", t).group(1)) for f in FEET}
P("\n=== STEP 0b: dwarfs (flag satellite-only, T-independent), once")
STAT.clear(); R51 = call(run_x51, "on")
CF1J = json.load(open(os.path.join(REB, "CF1_cf_window_map", "cf1_window_results.json")))
# ================= Part A: census (committed JSONs) =================
from scipy.stats import beta as _beta
def cp(k, n, cl=0.68):
    a = (1 - cl) / 2
    return (0.0 if k == 0 else float(_beta.ppf(a, k, n - k + 1)), 1.0 if k == n else float(_beta.ppf(1 - a, k + 1, n - k)))
SRC = {"CF1": ("CF1_cf_window_map/cf1_window_results.json", lambda k: k.startswith("cf_")),
       "CF2": ("CF2_decoupled_threshold_map/cf2_decoupled_results.json", lambda k: k.startswith("T")),
       "CL1": ("CL1_combined_threshold_budget/cl1_combined_results.json", lambda k: k.startswith("T")),
       "CL2": ("CL2_native_cf_slope/cl2_native_slope_results.json", lambda k: k[:3] in ("S9_", "SN_", "S3_")),
       "CL3": ("CL3_one_number/cl3_one_number_results.json", lambda k: k.startswith("L"))}
EXPECT = {"CF1": 9, "CF2": 15, "CL1": 12, "CL2": 9, "CL3": 3}
census = {}; ok_k1 = True
for lane, (path, sel) in SRC.items():
    J = json.load(open(os.path.join(REB, path)))
    keys = [k for k in J if sel(k) and isinstance(J[k], dict) and "grade" in J[k]]
    pc = sum(1 for k in keys if not J[k]["grade"]["canonical"]["fails"]); pa = sum(1 for k in keys if not J[k]["grade"]["alt"]["fails"])
    census[lane] = {"n": len(keys), "pass_canonical": pc, "pass_alt": pa}
    ok_k1 &= len(keys) == EXPECT[lane]
N = sum(v["n"] for v in census.values()); K = sum(v["pass_canonical"] for v in census.values())
P("Part A census: " + "; ".join(f"{l}: {v['pass_canonical']}/{v['n']} canonical, {v['pass_alt']}/{v['n']} alt" for l, v in census.items()))
P(f"  total: {K}/{N} configurations pass every line on canonical ({K / N:.3f}, 68% CP {cp(K, N)})")
P(f"K1 census counts {[(l, v['n']) for l, v in census.items()]} match committed lanes: {'PASS' if ok_k1 else 'FAIL'}"); checks.append(("K1", ok_k1))
RES["census"] = census; RES["census_total"] = {"n": N, "pass_canonical": K}
# ================= Part B: 24 seeded draws =================
rng = np.random.default_rng(20261027 + (1 if MUTATE else 0))
ND = 2 if MUTATE else 24
DR = [(float(np.round(rng.uniform(12.0, 12.6), 4)), float(np.round(rng.uniform(3.5, 4.5), 4))) for _ in range(ND)]
ref_rng = np.random.default_rng(20261027); REF = [(float(np.round(ref_rng.uniform(12.0, 12.6), 4)), float(np.round(ref_rng.uniform(3.5, 4.5), 4))) for _ in range(24)]
k2 = DR == REF[:len(DR)] and (len(DR) == 24)
P(f"K2 draw list reproducible from seed (first: T {DR[0][0]}, L {DR[0][1]}): {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))
RES["draws"] = DR
outs = []
for i, (T, L) in enumerate(DR):
    tag = f"shpS9_L{L}_T{T}"
    STAT.clear(); R43c, _ = call(run_x43, "on", tag + "_B"); F53c = call(run_x53, "on", tag); F53cre = call(run_x53, "off", tag)
    g = grade(R43c, F53c, F53cre, R51, f"draw {i}: T {T}, L {L}")
    outs.append({"T": T, "L": L, "pass_canonical": not g["canonical"]["fails"], "pass_alt": not g["alt"]["fails"],
                 "fails_canonical": g["canonical"]["fails"], "fails_alt": g["alt"]["fails"]})
    P(f"  >> draw {i:2d} T {T:.3f} L {L:.3f}: canonical {'PASS ALL' if not g['canonical']['fails'] else ', '.join(g['canonical']['fails'])}   [{time.time() - T0:.0f} s]")
    RES["partB"] = outs
    json.dump(RES, open(os.path.join(HERE, f"lee1_results{TAG}.json"), "w"), indent=1, default=float)
kb = sum(o["pass_canonical"] for o in outs); nb = len(outs); ph = kb / nb; ci = cp(kb, nb)
V = "NARROW (tuned-looking)" if ph < 0.10 else ("MODERATE" if ph < 0.40 else "BROAD")
RES["verdict"] = {"class": V, "p_hat": ph, "cp68": ci, "k": kb, "n": nb, "alt_pass": sum(o["pass_alt"] for o in outs)}
P(f"\n=== VERDICT: {V}: canonical pass fraction {kb}/{nb} = {ph:.3f} (68% CP [{ci[0]:.3f}, {ci[1]:.3f}]); alt {RES['verdict']['alt_pass']}/{nb}")
checks.append(("K3", rss_all() < 1.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(bool(ok) for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss_all():.2f} GB")
open(os.path.join(HERE, f"lee1{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"lee1_results{TAG}.json"), "w"), indent=1, default=float)
for fn in ("x62_x43copy.py", "x62_x53copy.py", "x62_x51copy.py"):
    try: os.remove(os.path.join(HERE, fn))
    except OSError: pass
sys.exit(0 if n == len(checks) else 1)
