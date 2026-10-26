#!/usr/bin/env python3
"""GR1_core_law_groups_ellipticals -- frozen criteria FROZEN_CRITERIA.md (fc3df5bac5).

OS1's core law Sigma_i = Sigma_a0 (sigma_i/sigma_ref)^q at OS1's SPARC-fixed q_f (no refit), graded on P4 T3's groups and
CFG528b's four SLUGGS centrals (route E: Newtonian stars + Burkert halo). Red KiDS lenses are not graded (criteria 1c).
SC1's machinery (X38 + EM1 + X30), P4's group estimator and CFG528b's Jeans machinery are executed read-only.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gr1_groups_ellipticals.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gr1_groups_ellipticals.py --mutate   -> q -> -q_f (exit 1 = tooth bites)
"""
import os, sys, io, json, math, time, contextlib, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
for _v in ("X30_MUTATE", "CFG528_MUTATE", "CFG528_POSTFREEZE", "CFG528B_MUTATE", "CFG331_MUTATE"): os.environ.pop(_v, None)
import numpy as np
from scipy.optimize import brentq

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

# ------------------------------------------------------------------ SC1 machinery (read-only, as OS1)
SC1SRC = os.path.join(REB, "SC1_self_coupled_core_law", "sc1_core_law.py"); TS = open(SC1SRC).read()
code = TS[:TS.index('checks = [("K1", k1)]')]
code = code.replace('os.path.join(HERE, "sc1_x30_machinery.log")', repr(os.path.join(HERE, f"gr1_x30_machinery{TAG}.log")))
NS = {"__file__": SC1SRC, "__name__": "sc1_ro"}; argv0 = sys.argv; sys.argv = [SC1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code, SC1SRC, "exec"), NS)
sys.argv = argv0
sparc, BGS, FEET, SREF, SIG, solve_r0, BURK, SAT = (NS[k] for k in ("sparc", "BGS", "FEET", "SREF", "SIG", "solve_r0", "B", "SAT"))
GE, MSUNE, MPCE = NS["GE"], NS["MSUNE"], NS["MPCE"]
X38J = json.load(open(os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos_results.json")))
OS1J = json.load(open(os.path.join(REB, "OS1_core_law_out_of_sample", "os1_out_of_sample_results.json")))
X40J = json.load(open(os.path.join(REB, "X40b_core_surface_density_scaling", "x40b_sd_scaling_results.json")))
QF = {f: float(OS1J["footings"][f]["q_f"]) for f in FEET}
P(f"GR1_core_law_groups_ellipticals {'MUTATE (q -> -q_f)' if MUTATE else 'normal run'}  (frozen fc3df5bac5)")
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy, not matter; route E; not theory closed")
P(f"q_f from OS1 (SPARC only, no refit): " + ", ".join(f"{f} {QF[f]:.3f}" for f in FEET) + f"; sigma_ref {SREF:.2f} km/s"
  + f"   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
QG = {f: (-QF[f] if MUTATE else QF[f]) for f in FEET}      # graded q
checks = []
RES = dict(frozen="fc3df5bac5", mutate=MUTATE, q_f=QF, sigma_ref=SREF, footings={f: {} for f in FEET})

# ------------------------------------------------------------------ K0a / K1: SPARC at q = 0 and q_f
bgA = BGS["A_c2b_refit"]
if not MUTATE:
    for f in FEET:
        s0 = sparc(f, bgA["a"], bgA["b"], bgA["h"], 0.0); sf = sparc(f, bgA["a"], bgA["b"], bgA["h"], QF[f])
        k0a = abs(s0["rms"] - X38J["footings"][f]["sparc"]["A_c2b_refit"]["rms"]) < 1e-9
        k1 = abs(sf["rms"] - OS1J["footings"][f]["sparc_A"]["rms"]) < 1e-6
        P(f"K0a [{f}] SPARC q=0 rms {s0['rms']:.6f} = X38: {'PASS' if k0a else 'FAIL'};  K1 SPARC q_f rms {sf['rms']:.6f} = OS1 "
          f"{OS1J['footings'][f]['sparc_A']['rms']:.6f}: {'PASS' if k1 else 'FAIL'}   [{time.time() - T0:.0f} s]")
        checks += [(f"K0a[{f}]", k0a), (f"K1[{f}]", k1)]
        RES["footings"][f]["sparc"] = dict(q0=s0["rms"], qf=sf["rms"], U_qf=sf["U_median"])

# ------------------------------------------------------------------ groups (P4 T3 estimator, read-only, as X40b / X43)
P4SRC = open(os.path.join(REB, "P4_v3_galaxy_tiles", "p4_v3_galaxy_tiles.py")).read()
NSG = {"np": np, "math": math}
exec(P4SRC[P4SRC.index("G540, MSUN540, KPC540 = "):P4SRC.index('if want("T3")')], NSG)
G540, MS540, KP540, HERN_RE, XG, LXG, RHO_H, M_H = (NSG[k] for k in ("G540", "MSUN540", "KPC540", "HERN_RE", "XG", "LXG", "RHO_H", "M_H"))
TIAN = os.path.join(os.path.dirname(REPO), "_external_data", "vizier2026", "J_A_A_710_L39.tsv")
GROUPS = []
for l in open(TIAN):
    if l.startswith("#"): continue
    r = l.rstrip("\n").split("\t")
    if len(r) < 13 or not r[0].strip().isdigit() or r[1].strip() != "Galaxy group": continue
    GROUPS.append(dict(id=r[2].strip(), ls=float(r[5]), els=float(r[6]), lM=float(r[7]), elM=float(r[8]), Re=float(r[10])))
GSAT = {"n": 0}
def group_logsig(o, foot, q, dlM=0.0, halo=True, sig=None):
    lMb = o["lM"] + dlM; Mb = 10 ** lMb * MS540; a = o["Re"] * KP540 / HERN_RE
    rc = 3 * (100 * bgA["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * G540)
    M200 = 10 ** (bgA["a"] + bgA["b"] * (lMb - 10)) * MS540; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
    gN = M_H / XG ** 2
    if halo:
        s_ = 10 ** o["ls"] if sig is None else sig
        sc = SIG[foot] * (s_ / SREF) ** q
        n0 = SAT["n"]; r0 = solve_r0(M200, R200, sc); GSAT["n"] += SAT["n"] - n0
        Mh = math.pi * sc * r0 ** 2 * BURK(np.minimum(XG * a, R200) / r0); gN = gN + Mh / Mb / XG ** 2
    s2 = float(np.trapz(4 * np.pi * XG ** 2 * RHO_H * XG * gN * XG, LXG) / 3.0) * G540 * Mb / a
    return 0.5 * math.log10(s2) - 3.0
def grade_groups(foot, q, sigs=None, selfcons=False):
    d, sl = [], []; GSAT["n"] = 0
    for j, o in enumerate(GROUPS):
        sg = None if sigs is None else sigs[j]
        if selfcons:
            sg = 10 ** o["ls"]
            for _ in range(60):
                new = 10 ** group_logsig(o, foot, q, sig=sg)
                if abs(math.log10(new / sg)) < 1e-6: break
                sg = new
        v = group_logsig(o, foot, q, sig=sg)
        sp = (group_logsig(o, foot, q, 0.01, sig=sg) - group_logsig(o, foot, q, -0.01, sig=sg)) / 0.02
        d.append(o["ls"] - v); sl.append(sp)
    st = NSG["class_stats"](d, sl); st["n_saturated"] = GSAT["n"] // 3; return st
def group_class(st, x38):
    if st["verdict"] == "CONSISTENT": return "PASS"
    if st["verdict"] == "ABOVE LAW" and st["mean"] <= x38["mean"] - 0.020: return "IMPROVES ON X38"
    return "FAILS"
k0d = max(abs(group_logsig(o, "canonical", 0.0, halo=False) - NSG["group_logsig"](o, 9.3603e-11, lambda y: np.ones_like(np.asarray(y, float)))) for o in GROUPS)
k0d = len(GROUPS) == 63 and k0d < 1e-4
P(f"K0d groups: {len(GROUPS)} rows; no-halo integrator = P4 group_logsig (nu = 1): {'PASS' if k0d else 'FAIL'}"); checks.append(("K0d", k0d))
G0 = {}
for f in FEET:
    g0 = grade_groups(f, 0.0); x = X40J["footings"][f]["X38_groups"]; G0[f] = g0
    k0b = abs(g0["mean"] - x["mean"]) < 1e-6 and abs(g0["Z"] - x["Z"]) < 1e-4
    P(f"K0b [{f}] groups q=0: mean {g0['mean']:+.5f} Z {g0['Z']:+.3f} vs X40b X38 {x['mean']:+.5f} / {x['Z']:+.3f}: {'PASS' if k0b else 'FAIL'}")
    checks.append((f"K0b[{f}]", k0b))

# ------------------------------------------------------------------ SLUGGS centrals (CFG528b machinery, read-only)
C528 = os.path.join(REPO, "campaign_fresh_gravity", "CFG528_sluggs_centrals_mechanism")
SB_ = open(os.path.join(C528, "cfg528b_measured_tracers.py")).read()
NB = {"__file__": os.path.join(C528, "cfg528b_measured_tracers.py"), "__name__": "cfg528b_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(SB_[:SB_.index('P("=" * 124)')], "cfg528b_measured_tracers", "exec"), NB)
BIN, CEN, A0L, RG, LR, Gs, KPC, score, field, measured_pops, sig_multi, off_pops = (NB[k] for k in (
    "B", "CEN", "A0", "RG", "LR", "G", "KPC", "score", "field", "measured_pops", "sig_multi", "off_pops"))
NS528 = NB["NS"]; MSUN, Mpop, gas_profile = NS528["MSUN"], NS528["Mpop"], NS528["gas_profile"]
C528BJ = json.load(open(os.path.join(C528, "cfg528b_measured_tracers_results.json")))
k0c = 0.0
for ft, a0 in A0L.items():
    for n in CEN:
        k0c = max(k0c, abs(off_pops(n, field(n, a0, "K0"), measured_pops(n)) - C528BJ["rows"]["M K0"][ft]["per"][f"NGC{n}"]))
P(f"K0c SLUGGS Jeans machinery reproduces CFG528b row M K0 per galaxy: max |d| {k0c:.1e} dex: {'PASS' if k0c < 1e-6 else 'FAIL'}"
  f"   [{time.time() - T0:.0f} s]")
checks.append(("K0c", k0c < 1e-6))
POPS = {n: measured_pops(n) for n in CEN}
SIGOBS = {n: float(np.mean(BIN[n]["Sb"][BIN[n]["outer"]])) for n in CEN}
P("SLUGGS outer-bin mean sigma_LOS (km/s): " + ", ".join(f"NGC{n} {SIGOBS[n]:.0f}" for n in CEN))
K2 = {"max": 0.0}
def halo_M(n, foot, q, Mstar, sig, gas=None):
    """Burkert M_h(r) on RG (Msun) for M_b = Mstar (+ gas total if given)."""
    Mb = Mstar + (0.0 if gas is None else float(gas[-1]))
    rc = 3 * (100 * bgA["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
    M200 = 10 ** (bgA["a"] + bgA["b"] * (math.log10(Mb) - 10)) * MSUNE; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
    sc = SIG[foot] * (sig / SREF) ** q; r0 = solve_r0(M200, R200, sc)
    return math.pi * sc * r0 ** 2 * BURK(np.minimum(RG * KPC, R200) / r0) / MSUNE, sc
def route_e(n, foot, q, sig, mstar="jam", gas=None):
    b = BIN[n]; Mg = None if gas is None else gas_profile(n, gas)
    lr12 = math.log(b["r12"])
    def enc(M):
        Mh, _ = halo_M(n, foot, q, M, sig, Mg)
        return 0.5 * M + float(np.interp(lr12, LR, Mh)) + (0.0 if Mg is None else float(np.interp(lr12, LR, Mg)))
    if mstar == "jam":
        fn = lambda lm: math.log10(enc(10 ** lm)) - math.log10(0.5 * b["Mjam"])
        lo, hi = math.log10(b["Mjam"]) - 3, math.log10(b["Mjam"])
        if fn(lo) * fn(hi) > 0: return None
        M = 10 ** brentq(fn, lo, hi, xtol=1e-13)
        K2["max"] = max(K2["max"], abs(enc(M) / (0.5 * b["Mjam"]) - 1))
    else:
        M = Mpop(n, mstar)
    Mh, sc = halo_M(n, foot, q, M, sig, Mg)
    Mx = Mh + (0.0 if Mg is None else Mg)
    g = Gs * (M * RG ** 2 / (RG + b["ah"]) ** 2 + Mx) * MSUN / (RG * KPC) ** 2
    return dict(g=g, M=M, frac=M / b["Mjam"], s_ratio=sc / SIG[foot])
def sluggs(foot, q, mstar="jam", gas=None, selfcons=False, sigs=None):
    per, info = {}, {}
    for n in CEN:
        sg = SIGOBS[n] if sigs is None else sigs[n]
        for it in range(40 if selfcons else 1):
            r = route_e(n, foot, q, sg, mstar, gas)
            if r is None: break
            if not selfcons: break
            s = sig_multi(BIN[n]["Rb"], r["g"], POPS[n]); new = float(np.mean(s[BIN[n]["outer"]]))
            if abs(math.log10(new / sg)) < 1e-6: break
            sg = new
        if r is None:
            per[n] = None; info[f"NGC{n}"] = "not computable (no JAM-analogue root)"; continue
        per[n] = off_pops(n, r["g"], POPS[n]); info[f"NGC{n}"] = dict(Mstar_over_Mjam=r["frac"], Sigma_over_Sigma_a0=r["s_ratio"], sigma_in=sg)
    st = score(per, foot); st["info"] = info; return st
def sluggs_class(st, st0):
    if st["closes"]: return "PASS"
    if np.isfinite(st["mean"]) and abs(st["mean"]) <= 0.5 * abs(st0["mean"]) and st["n_reversed"] == 0: return "IMPROVES ON X38"
    return "FAILS"
def sfmt(st):
    return " ".join(f"{(st['per'][f'NGC{n}'] if st['per'][f'NGC{n}'] is not None else float('nan')):+.3f}({st['Z'][f'NGC{n}']:+5.1f})" for n in CEN) \
        + f" | mean {st['mean']:+.3f} Zc {st['Z_class']:+5.1f} | cleared {st['n_cleared']}/4" + (f" rev {st['n_reversed']}" if st["n_reversed"] else "")

# ------------------------------------------------------------------ graded runs
S0 = {}; classes = {}
for f in FEET:
    q = QG[f]; R = RES["footings"][f]
    P(f"\n=== [{f}] graded q = {q:+.3f}" + ("  (MUTATE)" if MUTATE else ""))
    g = grade_groups(f, q); gcls = group_class(g, X40J["footings"][f]["X38_groups"])
    P(f"  groups (63): mean {g['mean']:+.4f} Z {g['Z']:+.2f} tot {g['tot']:.4f} -> {g['verdict']}  [X38 q=0: {G0[f]['mean']:+.4f}, Z {G0[f]['Z']:+.2f}]"
      f"; saturated r0 {g['n_saturated']}/63 -> class {gcls}")
    s0 = sluggs(f, 0.0); S0[f] = s0; s = sluggs(f, q); scls = sluggs_class(s, s0)
    P(f"  SLUGGS q=0 (X38 halos, baseline): {sfmt(s0)}")
    P(f"  SLUGGS q   (core law)          : {sfmt(s)} -> class {scls}")
    P("    per galaxy M*/M_JAM, Sigma/Sigma_a0: " + "; ".join(
        f"{k} {v['Mstar_over_Mjam']:.2f}, {v['Sigma_over_Sigma_a0']:.2f}" if isinstance(v, dict) else f"{k} {v}" for k, v in s["info"].items()))
    R.update(q=q, groups=dict(st=g, cls=gcls, q0=G0[f]), sluggs=dict(st=s, cls=scls, q0=s0))
    if MUTATE: continue
    if gcls == "PASS" and scls == "PASS": lc = "GR1 PREDICTS BOTH"
    elif gcls == "PASS": lc = "GR1 PREDICTS GROUPS, ELLIPTICALS SHORT"
    elif scls == "PASS": lc = "GR1 PREDICTS ELLIPTICALS, GROUPS SHORT"
    elif "IMPROVES ON X38" in (gcls, scls): lc = "GR1 IMPROVES ONLY"
    else: lc = "GR1 FAILS"
    classes[f] = lc; R["cls"] = lc
    P(f"  CLASS [{f}]: {lc}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    # reported only
    rep = {}
    gs = grade_groups(f, q, selfcons=True); rep["groups_selfconsistent"] = gs
    P(f"  (reported) groups self-consistent sigma: mean {gs['mean']:+.4f} Z {gs['Z']:+.2f} {gs['verdict']}")
    for dq in (-0.05, 0.05):
        gq = grade_groups(f, q + dq); rep[f"groups_q{q + dq:.3f}"] = gq
        P(f"  (reported) groups q = {q + dq:.3f}: mean {gq['mean']:+.4f} Z {gq['Z']:+.2f} {gq['verdict']}")
    for nm, kw in (("bar (hot gas)", dict(gas="extrap")), ("Salpeter M*", dict(mstar="salp")), ("self-consistent sigma", dict(selfcons=True))):
        sr0 = sluggs(f, 0.0, **{k: v for k, v in kw.items() if k != "selfcons"}); sr = sluggs(f, q, **kw)
        rep[f"sluggs {nm}"] = dict(q0=sr0, q=sr)
        P(f"  (reported) SLUGGS {nm:22s} q=0: {sfmt(sr0)}")
        P(f"  (reported) SLUGGS {nm:22s} q  : {sfmt(sr)}")
    R["reported"] = rep
    P(f"  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

if MUTATE:
    real = json.load(open(os.path.join(HERE, "gr1_groups_ellipticals_results.json")))
    for f in FEET:
        rr = real["footings"][f]; R = RES["footings"][f]
        dg_r = rr["groups"]["st"]["mean"] - rr["groups"]["q0"]["mean"]; dg_m = R["groups"]["st"]["mean"] - R["groups"]["q0"]["mean"]
        ds_r = rr["sluggs"]["st"]["mean"] - rr["sluggs"]["q0"]["mean"]; ds_m = R["sluggs"]["st"]["mean"] - R["sluggs"]["q0"]["mean"]
        ok = (dg_r * dg_m < 0) and (ds_r * ds_m < 0)
        P(f"[{f}] MUTATE: groups shift real {dg_r:+.4f} vs mutate {dg_m:+.4f}; SLUGGS shift real {ds_r:+.4f} vs mutate {ds_m:+.4f}: "
          f"{'tooth bites (opposite signs)' if ok else 'tooth does NOT bite'}"); checks.append((f"MUT[{f}]", ok))
        rng = np.random.default_rng(20261025); perm = rng.permutation([10 ** o["ls"] for o in GROUPS])
        gp = grade_groups(f, QF[f], sigs=list(perm)); R["groups_sigma_permuted_at_qf"] = gp
        P(f"  (reported) groups at +q_f with sigma permuted across groups: mean {gp['mean']:+.4f} Z {gp['Z']:+.2f} {gp['verdict']}")
else:
    checks.append(("K2", K2["max"] < 1e-8)); P(f"\nK2 JAM-analogue root residual max {K2['max']:.1e}: {'PASS' if K2['max'] < 1e-8 else 'FAIL'}")
    RES["verdict"] = classes["canonical"] if classes["canonical"] == classes["alt"] else f"UNDECIDED (footings disagree: {classes})"
    P(f"\n=== VERDICT: {RES['verdict']}  (red KiDS lenses NOT GRADED, criteria 1c)")
checks.append(("K3", rss() < 1.0))
n = sum(v for _, v in checks)
P(f"\nchecks {n}/{len(checks)}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks) + f"; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
RES["checks"] = {k: bool(v) for k, v in checks}
open(os.path.join(HERE, f"gr1_groups_ellipticals{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"gr1_groups_ellipticals_results{TAG}.json"), "w"), indent=1, default=float)
if MUTATE: sys.exit(1 if n == len(checks) else 0)
sys.exit(0 if n == len(checks) else 1)
