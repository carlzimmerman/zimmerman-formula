#!/usr/bin/env python3
"""CL3_one_number: CL2's harness (native S9 c_f slope, measured cluster budget) with the switch threshold set to X43's
crossover at the same level L, per footing - one external number for switch and cores. FROZEN_CRITERIA.md committed alone
first (47625a9db2). Harness: CL2 (b57ed8751f), crossover as DT1 (d782d8ec78).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I cl3_one_number.py      (CL3_MUTATE=1 twin)
"""
import os, sys, json, math, time, resource, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X53_MUTATE", None); os.environ.pop("X30_MUTATE", None)
import numpy as np

T0 = time.time(); MUTATE = os.environ.get("CL3_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
P(f"CL3_one_number  {'MUTATE (flag inverted; S0a target x1.01)' if MUTATE else 'normal run'}   (harness CF1 / X62 8c7768d26d)")
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
    if MUTATE and shape == "S9": c = SHAPES["INV"]                                  # m1
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
        if tv.startswith("F"):
            tc, ta = tv[1:].split(":"); ed.append(("    return max(s, sc), sc > s", "    return max(s, sc), M > 10 ** {'canonical': %s, 'alt': %s}[f]" % (tc, ta)))
        elif tv: ed.append(("    return max(s, sc), sc > s", "    return max(s, sc), M > 10 ** " + tv))
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
        if tv.startswith("F"):
            tc, ta = tv[1:].split(":"); ed.append(("return M200, R200, solve_r0(M200, R200, Sig), Sig, sc > SIGA0[foot]", "return M200, R200, solve_r0(M200, R200, Sig), Sig, M200 > 10 ** {'canonical': %s, 'alt': %s}[foot]" % (tc, ta)))
        elif tv: ed.append(("return M200, R200, solve_r0(M200, R200, Sig), Sig, sc > SIGA0[foot]", "return M200, R200, solve_r0(M200, R200, Sig), Sig, M200 > 10 ** " + tv))
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
FEET = ("canonical", "alt"); checks = []; RES = dict(criteria="47625a9db2", harness="CL2 b57ed8751f + DT1 crossover", mutate=MUTATE)
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
# ---------------- crossover T_f(L) exactly as DT1 ----------------
import contextlib as _cl, io as _io
from scipy.optimize import brentq as _bq
_EM1 = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); _TE = open(_EM1).read()
_NE = {"__file__": _EM1, "__name__": "em1_ro"}; _av = sys.argv; sys.argv = [_EM1]
with _cl.redirect_stdout(_io.StringIO()):
    exec(compile(_TE[:_TE.index("# ---------------- halo profiles")], _EM1, "exec"), _NE)
sys.argv = _av
_bg = _NE["BGS"]["A_c2b_refit"]; _cc = _bg["c"]; _h = _bg["h"]; _Om = float(_cc.Omega_m())
_zg = np.linspace(0, 30, 3001); _Dg = np.array([_cc.scale_independent_growth_factor(z) for z in _zg]); _Dg /= _Dg[0]
_lMg = np.linspace(7.0, 16.5, 191); _sigf = _bg["cB"].__defaults__[1]; _s2 = np.array([float(_sigf(10 ** l)[0]) ** 2 for l in _lMg])
_rhom0 = _Om * 2.775e11 * _h ** 2
def _sigma_coll(M):
    s2i = lambda l: float(np.interp(l, _lMg, _s2)); S = math.sqrt(max(s2i(math.log10(M / 2)) - s2i(math.log10(M)), 0.0)); Df = 1.686 / (1.686 + 0.974 * S)
    zf = float(np.interp(-Df, -_Dg, _zg)) if Df < 1 else 0.0
    rho = 18 * math.pi ** 2 * _rhom0 * (1 + zf) ** 3; rf = (3 * (M / 2) / (4 * math.pi * rho)) ** (1 / 3)
    return rho * rf / 1e12
_A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; _G, _MS, _PC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16
_SIG = {f: _A0[f] / (2 * math.pi * _G) * _PC ** 2 / _MS for f in _A0}
def T_of(L, f):
    cf = 2 * L if MUTATE else L
    et = 4.0 / (3.0 * B1) * cf ** 1.25
    g = lambda l: math.log(et * _sigma_coll(10 ** l)) - math.log(_SIG[f])
    xs = np.linspace(9, 16, 300); v = [g(x) for x in xs]
    for i in range(len(xs) - 1):
        if np.sign(v[i]) != np.sign(v[i + 1]): return _bq(g, xs[i], xs[i + 1], xtol=1e-7)
    return None
t4 = {f: T_of(4.0, f) for f in FEET}
tgt = (12.093 * (1.01 if MUTATE else 1.0), 12.429)
s0a = abs(t4["canonical"] - tgt[0]) <= 0.002 and abs(t4["alt"] - tgt[1]) <= 0.002
P(f"S0a T_f(4.0) = {t4['canonical']:.4f} / {t4['alt']:.4f} vs DT1 A 12.093 / 12.429: {'PASS' if s0a else 'FAIL'}"); checks.append(("S0a", s0a))
LS = [3.75, 3.9, 4.0]
TT = {L: {f: T_of(L, f) for f in FEET} for L in LS}
k2 = all(TT[LS[i + 1]][f] < TT[LS[i]][f] for i in range(len(LS) - 1) for f in FEET)
P("  T_f(L): " + "; ".join(f"L {L:g}: {TT[L]['canonical']:.3f} / {TT[L]['alt']:.3f}" for L in LS)); P(f"K2 T_f decreasing in L: {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))
# S0b: fixed T 12.3, L 4 reproduces CL2 S9 L 4
CL2J = json.load(open(os.path.join(REB, "CL2_native_cf_slope", "cl2_native_slope_results.json")))
STAT.clear(); R43b, _ = call(run_x43, "on", "shpS9_L4_T12.3_B"); F53b = call(run_x53, "on", "shpS9_L4_T12.3"); F53bre = call(run_x53, "off", "shpS9_L4_T12.3")
gb = grade(R43b, F53b, F53bre, R51, "S0b: CL2 reproduction (S9, L 4, T 12.3)")
ref = CL2J["S9_L4"]["grade"]
s0b = all(gb[f]["fails"] == ref[f]["fails"] for f in FEET) and all(abs(gb[f]["groups"]["Z"] - ref[f]["groups"]["Z"]) <= 0.01 and abs(gb[f]["clusters"]["G-OUT-all"]["Z"] - ref[f]["clusters"]["G-OUT-all"]["Z"]) <= 0.01 for f in FEET)
P(f"S0b reproduces CL2 S9 L 4: {'PASS' if s0b else 'FAIL'}"); checks.append(("S0b", s0b))
if not (s0a and s0b) and not MUTATE:
    P("STOP: Step 0 failed."); RES["verdict"] = "STOPPED AT STEP 0"
    json.dump(RES, open(os.path.join(HERE, f"cl3_one_number_results{TAG}.json"), "w"), indent=1, default=float); sys.exit(1)
MAP = {}; SW = {}
for L in LS:
    tf = f"F{TT[L]['canonical']:.4f}:{TT[L]['alt']:.4f}"
    tag = f"shpS9_L{L:g}_T{tf}"
    STAT.clear(); R43c, _ = call(run_x43, "on", tag + "_B"); F53c = call(run_x53, "on", tag); F53cre = call(run_x53, "off", tag)
    SW[L] = all(v["viol"] == 0 for v in STAT.values()) and len(STAT) >= 4
    MAP[L] = grade(R43c, F53c, F53cre, R51, f"one number L = {L:g} (T {TT[L]['canonical']:.3f} / {TT[L]['alt']:.3f})")
    g = MAP[L]["canonical"]
    P(f"  >> L {L:g} (T {TT[L]['canonical']:.3f} / {TT[L]['alt']:.3f}): canonical groups {g['groups']['Z']:+.2f} OUT-all {g['clusters']['G-OUT-all']['Z']:+.2f} lensing {g['lensing']['d_LF_L']:+.1f}; "
      + "; ".join(f"{f}: {'PASS ALL' if not MAP[L][f]['fails'] else ', '.join(MAP[L][f]['fails'])}" for f in FEET) + f"   [{time.time() - T0:.0f} s]")
    RES[f"L{L:g}"] = dict(grade=MAP[L], T=TT[L], switch_ok=SW[L])
    json.dump(RES, open(os.path.join(HERE, f"cl3_one_number_results{TAG}.json"), "w"), indent=1, default=float)
k1 = all(SW.values()); P(f"K1 switch property: {'PASS' if k1 else 'FAIL'}"); checks.append(("K1", k1))
import re
def base(ln): return re.sub(r" \(.*", "", ln)
ALT_KNOWN = ("SPARC line", "dwarfs MW ultra-faint")
pas = {f: [L for L in LS if not MAP[L][f]["fails"]] for f in FEET}
alt_known = [L for L in LS if MAP[L]["alt"]["fails"] and all(base(l) in ALT_KNOWN for l in MAP[L]["alt"]["fails"])]
if pas["canonical"] or pas["alt"]:
    which = "both" if set(pas["canonical"]) & set(pas["alt"]) else ("canonical" if pas["canonical"] else "alt")
    V = f"ONE NUMBER PASSES ({which}): " + "; ".join(f"{f}: L {pas[f]}" for f in FEET if pas[f])
else:
    V = "ONE NUMBER FAILS: binding " + ", ".join(sorted({base(l) for L in LS for f in FEET for l in MAP[L][f]["fails"]}))
if alt_known: V += f" | alt fails only on its known lines (SPARC line / MW ultra-faints) at L {alt_known}"
RES["verdict"] = V; RES["passing"] = pas; RES["T"] = TT
P(f"\n=== VERDICT: {V}")
checks.append(("K3", rss_all() < 1.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(bool(ok) for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss_all():.2f} GB (max over processes)")
open(os.path.join(HERE, f"cl3_one_number{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"cl3_one_number_results{TAG}.json"), "w"), indent=1, default=float)
for fn in ("x62_x43copy.py", "x62_x53copy.py", "x62_x51copy.py"):
    try: os.remove(os.path.join(HERE, fn))
    except OSError: pass
sys.exit(0 if n == len(checks) else 1)
