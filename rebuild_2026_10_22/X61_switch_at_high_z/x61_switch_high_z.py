#!/usr/bin/env python3
"""X61_switch_at_high_z: X58's object-keyed switch at z ~ 1-2.5.  M_x(z) from X43's eta Sigma_coll(M, z) = a0 F(z)/(2 pi G)
(Lacey-Cole EPS on EM1's CLASS P(k), generalised to the observation epoch); per-galaxy flags (EM1 M200(M_b), approximate);
graded on KURVS's outer Delta' (CFG140/141 pipeline exec'd read-only) above vs below M_x; counts for KMOS3D, SINS-AO, RC100.

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (0b35616410, committed alone).  kappa = 1/2 FITTED.  Not "theory closed".

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x61_switch_high_z.py                 -> .out, _results.json  (exit 0)
    X61_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x61_switch_high_z.py    -> flags inverted; K1 must FAIL (exit 1)
"""
import os, sys, io, re, csv, json, math, time, resource, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
MUTATE = os.environ.get("X61_MUTATE", "0") == "1"
os.environ.pop("MUTATE", None); os.environ.pop("X30_MUTATE", None)          # the exec'd lanes must run unmutated
import numpy as np
from scipy.optimize import brentq, minimize_scalar

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
CFG = os.path.join(REPO, "campaign_fresh_gravity"); DA = os.path.join(REPO, "data_assembly")
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
CHECKS = []; RES = dict(lane="X61_switch_at_high_z", frozen="0b35616410", mutate=MUTATE)
def check(name, ok, detail):
    CHECKS.append((name, bool(ok))); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

P(f"X61_switch_at_high_z  {'MUTATE run (every flag inverted after the crossover is computed)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy (not matter); route E above M_x, law on baryons below; c_f = 4 EXTERNAL; not theory closed")

# ------------------------------------------------------------------ EM1 (read-only, up to its halo-profiles block: CLASS backgrounds) -- as X41/X43
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; argv0 = sys.argv; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(TE[:TE.index("# ---------------- halo profiles")], EM1SRC, "exec"), NE)
sys.argv = argv0
A0, BGSE, GE, MSUNE = NE["A0"], NE["BGS"], NE["G"], NE["MSUN"]
FEET = ("canonical", "alt")
P(f"EM1 backgrounds executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]; a0 canonical {A0['canonical']:.4e}, alt {A0['alt']:.4e}")

# ------------------------------------------------------------------ X43's EPS block (copied verbatim), generalised to z_obs
DC, OMEGA, DELTA = 1.686, 0.974, 18 * math.pi ** 2
B1 = 3 * math.log(2) - math.pi / 2; CF = 4.0; GAM = 2.25
ETA = 4.0 / (3.0 * B1) * CF ** (GAM - 1.0)
PC2 = (3.0857e16) ** 2
EPS = {}
for tag, bg in BGSE.items():
    cc = bg["c"]; h = bg["h"]; Om = float(cc.Omega_m()); rhom0 = Om * 2.775e11 * h ** 2
    zg = np.linspace(0, 30, 3001); Dg = np.array([cc.scale_independent_growth_factor(z) for z in zg]); Dg /= Dg[0]
    lMg = np.linspace(7.0, 16.5, 191); sigf = bg["cB"].__defaults__[1]
    s2 = np.array([float(sigf(10 ** l)[0]) ** 2 for l in lMg])
    EPS[tag] = dict(rhom0=rhom0, zg=zg, Dg=Dg, lMg=lMg, s2=s2, h=h)
def Dof(tag, z): e = EPS[tag]; return float(np.interp(z, e["zg"], e["Dg"]))
def zform(tag, M, zobs=0.0):
    """Lacey-Cole median formation of the half-mass progenitor: delta_c/D(z_f) = delta_c/D(z_obs) + omega S^1/2 (X41 at z_obs = 0)."""
    e = EPS[tag]; s2 = lambda l: float(np.interp(l, e["lMg"], e["s2"]))
    S = math.sqrt(max(s2(math.log10(M / 2)) - s2(math.log10(M)), 0.0))
    Dobs = Dof(tag, zobs); Df = DC / (DC / Dobs + OMEGA * S)
    if Df >= Dobs: return zobs, Df
    return float(np.interp(-Df, -e["Dg"], e["zg"])), Df
def sigma_coll(tag, M, zobs=0.0):
    zf, Df = zform(tag, M, zobs); e = EPS[tag]; rho = DELTA * e["rhom0"] * (1 + zf) ** 3
    rf = (3 * (M / 2) / (4 * math.pi * rho)) ** (1 / 3)
    return rho * rf / 1e12, zf, Df                                                          # Msun/pc^2
def R_dec(z, w0=-0.838, wa=-0.62):                                                          # CFG223 / CFG227 verbatim
    return math.sqrt((1.0 + z) ** (3.0 * (1.0 + w0 + wa)) * math.exp(-3.0 * wa * z / (1.0 + z)))
FLAW = {"MDEC": R_dec, "FLAT": lambda z: 1.0}
SIGA0_PC = {f: A0[f] / (2 * math.pi * GE) * PC2 / MSUNE for f in FEET}
def sig_a0_pc(f, z, law): return SIGA0_PC[f] * FLAW[law](z)
def mcross(f, z, law="MDEC", tag="A_c2b_refit"):
    fn = lambda l: math.log(ETA * sigma_coll(tag, 10 ** l, z)[0] / sig_a0_pc(f, z, law))
    lo, hi = 7.4, 16.3
    if fn(lo) > 0: return lo, "below grid"
    if fn(hi) < 0: return hi, "above grid"
    return brentq(fn, lo, hi, xtol=1e-6), "ok"

# ------------------------------------------------------------------ STEP 0 (f) + K2
P("\n=== STEP 0 (stop rule) and K2")
s0f = []
lx0 = {f: mcross(f, 0.0, "FLAT")[0] for f in FEET}
s12 = sigma_coll("A_c2b_refit", 1e12)[0]
okf = abs(lx0["canonical"] - 12.09) < 0.005 and abs(lx0["alt"] - 12.43) < 0.005 and abs(s12 - 6.84) < 0.01
P(f"  (f) X43 crossover at z_obs 0, F = 1: 10^{lx0['canonical']:.3f} / 10^{lx0['alt']:.3f} (X43 12.09 / 12.43); Sigma_coll(1e12) {s12:.3f} (6.84): {'OK' if okf else 'MISS'}")
s0f.append(("f", okf))
k2 = []; k2rows = []
for z in (0.0, 1.0, 1.5, 2.0, 2.5):
    zf, Df = zform("A_c2b_refit", 1e11, z); e = EPS["A_c2b_refit"]
    S = math.sqrt(float(np.interp(math.log10(5e10), e["lMg"], e["s2"])) - float(np.interp(11.0, e["lMg"], e["s2"])))
    res = abs(DC / Dof("A_c2b_refit", zf) - DC / Dof("A_c2b_refit", z) - OMEGA * S)
    k2.append(res < 1e-3 and Df < Dof("A_c2b_refit", z)); k2rows.append(f"z {z}: z_f {zf:.3f}, resid {res:.1e}")
check("K2 generalised EPS (M 1e11)", all(k2), "; ".join(k2rows))
okF = abs(R_dec(0.0) - 1) < 1e-15

# ------------------------------------------------------------------ P1: M_x(z)
P("\n=== P1  M_x(z) (bg A primary; bg B reported); log10 M200 [Msun]")
ZT = (0.0, 1.0, 1.5, 2.0, 2.5)
MX = {}
for tag in ("A_c2b_refit", "B_cfg886_bg"):
    for law in ("MDEC", "FLAT"):
        for f in FEET:
            MX[(tag, law, f)] = {z: mcross(f, z, law, tag) for z in ZT}
for tag in ("A_c2b_refit", "B_cfg886_bg"):
    for law in ("MDEC", "FLAT"):
        for f in FEET:
            P(f"  [{tag[:1]} {law:4s} {f:9s}] " + "  ".join(f"z {z}: {MX[(tag, law, f)][z][0]:.2f}" + ("" if MX[(tag, law, f)][z][1] == "ok" else f"({MX[(tag, law, f)][z][1]})") for z in ZT))
P("  context: F_MDEC(z) " + ", ".join(f"{z}: {R_dec(z):.3f}" for z in ZT) + f"; eta {ETA:.3f}; Sigma_a0 {SIGA0_PC['canonical']:.1f} / {SIGA0_PC['alt']:.1f} Msun/pc^2")
P("  Sigma_coll(M, z) bg A [Msun/pc^2; z_f]: " + "; ".join(f"M 1e{l}: " + ", ".join(f"z{z} {sigma_coll('A_c2b_refit', 10.0 ** l, z)[0]:.1f}/{sigma_coll('A_c2b_refit', 10.0 ** l, z)[1]:.2f}" for z in ZT) for l in (10, 11, 12)))
RES["M_cross"] = {f"{t}|{law}|{f}": {str(z): v[0] for z, v in d.items()} for (t, law, f), d in MX.items()}
def lmx(f, z, law="MDEC", tag="A_c2b_refit"): return mcross(f, z, law, tag)[0]

# ------------------------------------------------------------------ EM1 M200(M_b) and route-E Burkert at z
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
EA, EB = EM1J["rows"]["A_c2b_refit"]["R1"]["a"], EM1J["rows"]["A_c2b_refit"]["R1"]["b"]
def lm200(lmb, off=0.0): return EA + EB * (lmb - 10.0) + off
P(f"\nEM1 R1 (bg A): log M200 = {EA} + {EB} (log M_b - 10)  [z = 0 SPARC relation; APPROXIMATE at high z; ledger A5/A6]")
def Bk(x):
    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
SAT = {"n": 0}
def solve_r0(Mtot, Rout, Sig):                                                              # X43 verbatim
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(Bk(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    lpk = float(pk.x)
    if lm(lpk) < math.log(Mtot):
        SAT["n"] += 1; return math.exp(lpk), True
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), lpk, xtol=1e-14)), False
def halo_E(M200, z, f, law="MDEC", tag="A_c2b_refit"):
    """route-E Burkert at epoch z: Sigma_core = max(Sigma_a0(z), eta Sigma_coll(M200, z)); returns (r0 [m], Sigma [kg/m^2], R200 [m], saturated)."""
    rc = BGSE[tag]["rhoc"](z); Mkg = M200 * MSUNE; R200 = (3 * Mkg / (4 * math.pi * 200 * rc)) ** (1 / 3)
    Sig = max(sig_a0_pc(f, z, law), ETA * sigma_coll(tag, M200, z)[0]) * MSUNE / PC2
    r0, sat = solve_r0(Mkg, R200, Sig); return r0, Sig, R200, sat
# K3
r0t, St, Rt, satt = halo_E(10 ** 11.5, 1.5, "canonical")
k3 = satt or abs(math.pi * St * r0t ** 2 * float(Bk(Rt / r0t)) / (10 ** 11.5 * MSUNE) - 1) < 1e-8
check("K3 Burkert at z 1.5 returns M200 inside R200(z)", k3, f"M(<R200)/M200 - 1 = {math.pi * St * r0t ** 2 * float(Bk(Rt / r0t)) / (10 ** 11.5 * MSUNE) - 1:+.1e}, saturated {satt}")

# ------------------------------------------------------------------ CFG140/141 (exec'd read-only up to CFG141's controls)
F141 = os.path.join(CFG, "CFG141_kurvs_measured_sigma.py"); S141 = open(F141).read()
N141 = {"__file__": F141, "__name__": "cfg141_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(S141[:S141.index("# ================================================================== C1 / C2")], "CFG141", "exec"), N141)
KU, KU2, SP = N141["KU"], N141["KU2"], N141["SP"]
gbar, gobs, dlog_gobs, gpred, slope, pooled, score = (N141[k] for k in ("gbar", "gobs", "dlog_gobs", "gpred", "slope", "pooled", "score"))
A0K, G140, MS140, KPC140 = N141["A0"], N141["g140"]["G"], N141["g140"]["MSUN"], N141["KPC"]
menc = N141["g140"]["menc"]
P(f"CFG140/141 pipeline exec'd read-only: KURVS {len(KU)} (P2 rows {len(KU2)}), SPARC anchor {len(SP)}; CFG4 a0 {A0K['canonical']:.4e} / {A0K['alt']:.4e}")

# STEP 0 (a), (b)
o140 = open(os.path.join(CFG, "CFG140_kurvs_a0z.out")).read()
ref_a = {int(k): float(v) for k, v in re.findall(r"KURVS-(\d+) z [\d.]+ R [\d.]+ kpc g_bar/a0 [\d.]+ D_flat ([+-][\d.]+)", o140)}
_, Dk, _ = score(KU, 0.67, 0.0, "P1", "canonical")
da = max(abs(d - ref_a[int(o["name"][6:])]) for o, d in zip(KU, Dk))
j140 = json.load(open(os.path.join(CFG, "CFG140_kurvs_a0z_results.json")))["numbers"]["central"]
(kf, _), _, _ = score(KU, 0.67, 0.0, "P1", "canonical"); (af, _), _, _ = score(SP, 0.67, 0.0, "P1", "canonical", measured_gas=True)
dac = abs((kf - af) - j140["df"])
oka = len(ref_a) == 10 and da < 0.006 and dac < 1e-9
P(f"  (a) CFG140 per-galaxy P1 Delta_flat max |diff| {da:.4f} (10 rows parsed: {len(ref_a)}); central df {kf - af:.6f} vs {j140['df']:.6f} (|diff| {dac:.1e}): {'OK' if oka else 'MISS'}")
s0f.append(("a", oka))
j141 = json.load(open(os.path.join(CFG, "CFG141_kurvs_measured_sigma_results.json")))["numbers"]["P2"]["0.67|0.0|canonical"]
(kf2, _), _, _ = score(KU2, 0.67, 0.0, "P1", "canonical")
db = abs((kf2 - af) - j141["df"])
rd141 = open(os.path.join(CFG, "CFG141_README.md")).read()
ref_b = {int(m[0]): float(m[1]) for m in re.findall(r"^\| (\d+) \| \d+ \| [\d]+ ± [\d]+ \| [\d.]+ \| [\d.]+ \| ([+-][\d.]+) \|", rd141, re.M)}
_, Dk2, _ = score(KU2, 0.67, 0.0, "P1", "canonical")
dbg = max(abs(d - ref_b[int(o["name"][6:])]) for o, d in zip(KU2, Dk2))
okb = len(ref_b) == 10 and db < 1e-9 and dbg < 0.006
P(f"  (b) CFG141 P2 central df {kf2 - af:.6f} vs {j141['df']:.6f} (|diff| {db:.1e}); README per-galaxy max |diff| {dbg:.4f} ({len(ref_b)} rows): {'OK' if okb else 'MISS'}")
s0f.append(("b", okb))

# STEP 0 (c) KMOS3D
KM = [r for r in csv.DictReader(open(os.path.join(CFG, "CFG99_kmos3d_outer_rc", "cfg89_per_object.csv"))) if r["clean"] == "1" and r["zq"] == "0"]
hi = [r for r in KM if r["window"] == "HIGH"]
nlo = {f: sum(float(r[f"gdisc_a0_{f}"]) < 1 for r in hi) for f in FEET}
okc = len(hi) == 74 and nlo["canonical"] == 2 and nlo["alt"] == 3
P(f"  (c) CFG99 clean HIGH {len(hi)} (74); g_bar < a0 at r_out {nlo['canonical']} / {nlo['alt']} (2 / 3): {'OK' if okc else 'MISS'}")
s0f.append(("c", okc))
# (d) SINS
SD = os.path.join(DA, "highz_literature_tables", "sins_ao")
T1 = {r["source"]: r for r in csv.DictReader(open(os.path.join(SD, "sins_ao_table1_sample.csv")))}
T6 = {r["source"]: r for r in csv.DictReader(open(os.path.join(SD, "sins_ao_table6_kinematics.csv")))}
PTS = {r["object"]: r for r in csv.DictReader(open(os.path.join(CFG, "CFG280_sins_ao_published", "cfg280_points_stageB.csv")))}
SINS = []
for s in T6:
    crit = str(T6[s]["disk_criteria"]).strip()
    SINS.append(dict(name=s, z=float(T1[s]["z_Halpha"]), lms=math.log10(float(T1[s]["Mstar_1e10Msun"]) * 1e10),
                     T2=all(k in crit.split(",") for k in ("1", "2", "3")), pt=PTS.get("SINS " + s)))   # run-1 loader fix: the points file prefixes "SINS "
okd = len(SINS) == 38 and sum(x["T2"] for x in SINS) == 18 and all(x["pt"] is not None for x in SINS)
P(f"  (d) CFG280 rows {len(SINS)} (38), T2 {sum(x['T2'] for x in SINS)} (18), every row in the points file {all(x['pt'] is not None for x in SINS)}: {'OK' if okd else 'MISS'}")
s0f.append(("d", okd))
# (e) RC100
RC = []
for r in csv.DictReader(open(os.path.join(DA, "rc100_provenance", "rc100_table3_six_fields_paper_values.csv"))):
    try: zz, Re, Vc, fd = (float(r[k]) for k in ("z", "Re_kpc", "Vc_Re_kms", "fDM_within_Re"))
    except ValueError: continue
    if all(math.isfinite(v) for v in (zz, Re, Vc, fd)) and 0 < fd < 1:
        mb = (1 - fd) * (Vc * 1e3) ** 2 * Re * 3.0857e19 / GE / MSUNE
        RC.append(dict(name=r["name"], z=zz, lmb=math.log10(mb), fd=fd, lmb_tab=float(r["logMbar_Msun"]) if r["logMbar_Msun"] else float("nan")))
rc2 = [x for x in RC if x["z"] >= 2.0]
oke = len(rc2) == 41
P(f"  (e) CFG227 S4 RC100 z >= 2: {len(rc2)} (41); all z: {len(RC)}: {'OK' if oke else 'MISS'}")
s0f.append(("e", oke))
k0 = all(ok for _, ok in s0f)
check("K0 step 0 (a)-(f)", k0, ", ".join(f"{k} {'OK' if ok else 'MISS'}" for k, ok in s0f))
RES["step0"] = {k: ok for k, ok in s0f}
if not k0:
    P("\nSTOPPED: step 0 failed; no verdict (frozen stop rule).")
    RES["verdict"] = "STOPPED"; open(os.path.join(HERE, f"x61_switch_high_z{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(RES, open(os.path.join(HERE, f"x61_switch_high_z_results{TAG}.json"), "w"), indent=1, default=float); sys.exit(1)

# ------------------------------------------------------------------ the KURVS per-galaxy machinery (CFG140's score with a0 F(z))
def per_obj(objs, mu, dlt, Pv, foot, law):
    D, S, GB = [], [], []
    for o in objs:
        a = A0K[foot] * FLAW[law](o["z"]); gb = gbar(o, mu, dlt); gp = gpred(gb, a); go, _ = gobs(o, Pv)
        D.append(math.log10(go / gp)); S.append(math.hypot(dlog_gobs(o, Pv), slope(gb, a) * o["sm"])); GB.append(gb)
    return np.array(D), np.array(S), np.array(GB)
_, Dref, _ = score(KU, 0.67, 0.0, "P1", "canonical")
Dflat, _, _ = per_obj(KU, 0.67, 0.0, "P1", "canonical", "FLAT")
k4 = okF and float(np.max(np.abs(Dflat - Dref))) < 1e-12
check("K4 F(0) = 1 and the F = 1 law branch reproduces CFG140's flat Delta", k4, f"F(0) - 1 = {R_dec(0.0) - 1:.1e}; max |diff| {float(np.max(np.abs(Dflat - Dref))):.1e}")
def pred_E(o, mu, dlt, foot, law, off=0.0):
    """route-E Delta_pred at R_max (Newtonian baryons + Burkert core) relative to the law with a0 F(z)."""
    lmb = math.log10(10 ** (o["lm"] + dlt) * (1 + mu)); M200 = 10 ** lm200(lmb, off)
    r0, Sig, R200, sat = halo_E(M200, o["z"], foot, law)
    R = o["R"] * KPC140; ME = math.pi * Sig * r0 ** 2 * float(Bk(min(R, R200) / r0))           # kg
    gb = gbar(o, mu, dlt); gE = gb + GE * ME / R ** 2
    return math.log10(gE / gpred(gb, A0K[foot] * FLAW[law](o["z"]))), lmb, math.log10(M200), sat
def flags_for(objs, mu, dlt, foot, law, off=0.0, tag="A_c2b_refit"):
    fl, info = [], []
    for o in objs:
        lmb = math.log10(10 ** (o["lm"] + dlt) * (1 + mu)); l2 = lm200(lmb, off); lx = lmx(foot, o["z"], law, tag)
        fl.append(l2 > lx); info.append((lmb, l2, lx))
    return np.array(fl), info

# ------------------------------------------------------------------ P2/P3 on KURVS: flags, power, statistic
P("\n=== KURVS (CFG140/141): flags, power, then the observable (primary cell P2, mu 0.67, delta 0, F = M-DEC, bg A)")
MU0, DL0, LAW0 = 0.67, 0.0, "MDEC"
VER = {}; RES["kurvs"] = {}
for f in FEET:
    fl_true, info = flags_for(KU2, MU0, DL0, f, LAW0)
    fl = (~fl_true) if MUTATE else fl_true
    P(f"\n  [{f}] per galaxy: " + "; ".join(f"{o['name']} z {o['z']:.2f} logMb {i[0]:.2f} logM200 {i[1]:.2f} logMx {i[2]:.2f} {'A' if a else 'B'}" for o, i, a in zip(KU2, info, fl)))
    # predictions by branch
    DP = np.array([pred_E(o, MU0, DL0, f, LAW0)[0] if a else 0.0 for o, a in zip(KU2, fl)])
    # K1: flags vs independent recomputation; branch values
    rec = np.array([lm200(math.log10(10 ** (o["lm"] + DL0) * (1 + MU0))) > mcross(f, o["z"], LAW0)[0] for o in KU2])
    br = all((abs(dp - pred_E(o, MU0, DL0, f, LAW0)[0]) < 1e-12) if r else (dp == 0.0) for o, dp, r in zip(KU2, DP, rec))
    k1 = bool(np.all(fl == rec)) and br
    check(f"K1 switch property [{f}]", k1, f"flags equal recomputation {int(np.sum(fl == rec))}/{len(KU2)}; branch values match {br}")
    nA, nB = int(fl.sum()), int((~fl).sum())
    # power (errors only; no Delta yet)
    _, S, _ = per_obj(KU2, MU0, DL0, "P1", f, LAW0)
    sA = 1 / math.sqrt(np.sum(1 / S[fl] ** 2)) if nA else float("inf"); sB = 1 / math.sqrt(np.sum(1 / S[~fl] ** 2)) if nB else float("inf")
    sdiff = math.hypot(sA, sB); mpA = float(np.mean(DP[fl])) if nA else float("nan")
    Spow = mpA / sdiff if (nA and nB) else 0.0
    P(f"  POWER [{f}]: N_A {nA}, N_B {nB}; sigma_A {sA:.3f}, sigma_B {sB:.3f}, sigma_diff {sdiff:.3f}; <Delta_pred>_A {mpA:+.3f}; S = {Spow:.2f}")
    # observable
    D, S, GB = per_obj(KU2, MU0, DL0, "P1", f, LAW0)
    (aF, eaF), _, _ = score(SP, MU0, DL0, "P1", f, measured_gas=True)
    Dp = D - aF
    P(f"  observable Delta' (M-DEC, anchor {aF:+.3f} +- {eaF:.3f}): " + "; ".join(f"{o['name']} {d:+.3f} +- {s:.3f} (pred {p:+.3f})" for o, d, s, p in zip(KU2, Dp, S, DP)))
    row = dict(nA=nA, nB=nB, sigma_A=sA, sigma_B=sB, sigma_diff=sdiff, mean_pred_A=mpA, S=Spow, anchor=aF, e_anchor=eaF,
               per_galaxy={o["name"]: dict(z=o["z"], flag="A" if a else "B", lmb=i[0], lm200=i[1], lmx=i[2], dprime=float(d), s=float(s), pred=float(p))
                           for o, i, a, d, s, p in zip(KU2, info, fl, Dp, S, DP)})
    if nA:
        (mA, eA) = pooled(D[fl], S[fl]); (rA, erA) = pooled(D[fl] - aF - DP[fl], S[fl])
        row.update(dprime_A=mA - aF, e_dprime_A=math.hypot(eA, eaF), resid_A=rA, e_resid_A=math.hypot(erA, eaF))
        P(f"  A: pooled Delta'_A {mA - aF:+.3f} +- {math.hypot(eA, eaF):.3f}; route-E residual {rA:+.3f} +- {math.hypot(erA, eaF):.3f}")
    if nB:
        (mB, eB) = pooled(D[~fl], S[~fl]); row.update(dprime_B=mB - aF, e_dprime_B=math.hypot(eB, eaF))
        P(f"  B: pooled Delta'_B {mB - aF:+.3f} +- {math.hypot(eB, eaF):.3f}")
    # verdict
    if nA < 3 or nB < 3 or Spow < 2:
        v = "NOT DIAGNOSTIC"
    else:
        Dd = row["dprime_A"] - row["dprime_B"]; sD = math.hypot(eA, eB); row.update(D=Dd, sigma_D=sD)
        supp = Dd >= 2 * sD and abs(row["dprime_B"]) < 2 * row["e_dprime_B"] and abs(row["resid_A"]) < 2 * row["e_resid_A"]
        contra = row["dprime_B"] >= 2 * row["e_dprime_B"] or (Dd - mpA) <= -2 * sD or Dd <= -2 * sD
        v = "SWITCH PREDICTION SUPPORTED" if supp else ("CONTRADICTED" if contra else "UNDECIDED")
    row["verdict"] = v; VER[f] = v; RES["kurvs"][f] = row
    P(f"  VERDICT [{f}]: {v}" + (f"  (N_A {nA}, N_B {nB}, S {Spow:.2f})" if v == "NOT DIAGNOSTIC" else ""))
verdict = VER["canonical"] if VER["canonical"] == VER["alt"] else "UNDECIDED (footings disagree)"
RES["verdict"] = verdict
P(f"\n=== VERDICT (both footings): {verdict}")

# ------------------------------------------------------------------ R1 above-only reading over the grid (reported)
P("\n=== R1 (reported) KURVS above-only reading: pooled route-E residual and law-only Delta' over P0/P1/P2 x mu x delta x F, per footing")
OBJ = {"P0": (KU, "P0"), "P1": (KU, "P1"), "P2": (KU2, "P1")}
R1 = {}
for f in FEET:
    for law in ("MDEC", "FLAT"):
        for pk, (objs, Pv) in OBJ.items():
            for mu in (0.25, 0.67, 1.5, 4.0):
                for dl in (-0.2, 0.0, 0.2):
                    fl, _ = flags_for(objs, mu, dl, f, law)
                    fl = (~fl) if MUTATE else fl
                    D, S, _ = per_obj(objs, mu, dl, Pv, f, law)
                    (aF, eaF), _, _ = score(SP, mu, dl, Pv, f, measured_gas=True)
                    DP = np.array([pred_E(o, mu, dl, f, law)[0] if a else 0.0 for o, a in zip(objs, fl)])
                    (m, e) = pooled(D - aF, S); (r, er) = pooled(D - aF - DP, S)
                    R1[(f, law, pk, mu, dl)] = dict(nA=int(fl.sum()), law_only=m, e_law=math.hypot(e, eaF), resid=r, e_resid=math.hypot(er, eaF),
                                                    pred_mean=float(np.mean(DP)))
for f in FEET:
    for law in ("MDEC", "FLAT"):
        for pk in OBJ:
            cells = [v for k, v in R1.items() if k[0] == f and k[1] == law and k[2] == pk]
            nE = sum(abs(c["resid"]) < 2 * c["e_resid"] for c in cells); nL = sum(abs(c["law_only"]) < 2 * c["e_law"] for c in cells)
            c0 = R1[(f, law, pk, 0.67, 0.0)]
            P(f"  [{f} {law} {pk}] route E within 2 sigma {nE}/12, law-only within 2 sigma {nL}/12; central: N_A {c0['nA']}, <pred> {c0['pred_mean']:+.3f}, "
              f"law-only {c0['law_only']:+.3f} +- {c0['e_law']:.3f}, route-E residual {c0['resid']:+.3f} +- {c0['e_resid']:.3f}")
RES["R1"] = {"|".join(map(str, k)): v for k, v in R1.items()}

# ------------------------------------------------------------------ R2 / R3 counts and descriptive medians (reported)
P("\n=== R2 / R3 (reported) counts on each side of M_x(z_gal) (bg A, F = M-DEC; flat in brackets) and descriptive medians")
R2 = {}
def side(lm2, z, f, law): return lm2 > lmx(f, z, law)
for f in FEET:
    rows = []
    for wnd in ("LOW", "MID", "HIGH"):
        S_ = [r for r in KM if r["window"] == wnd]
        a = sum(side(lm200(math.log10(float(r["Mbar"]))), float(r["Z"]), f, "MDEC") for r in S_); aF_ = sum(side(lm200(math.log10(float(r["Mbar"]))), float(r["Z"]), f, "FLAT") for r in S_)
        a = (len(S_) - a) if MUTATE else a
        R2[f"{f}|KMOS3D_{wnd}"] = dict(n=len(S_), above=a, below=len(S_) - a, above_flat=aF_)
        rows.append(f"KMOS3D {wnd} clean {len(S_)}: A {a} / B {len(S_) - a} [flat A {aF_}]")
    for nm, sub in (("SINS T0", SINS), ("SINS T2", [x for x in SINS if x["T2"]])):
        fl = [side(lm200(x["lms"]), x["z"], f, "MDEC") for x in sub]; fl = [not q for q in fl] if MUTATE else fl
        aF_ = sum(side(lm200(x["lms"]), x["z"], f, "FLAT") for x in sub)
        dA = [float(x["pt"]["delta_FLAT"]) for x, q in zip(sub, fl) if q]; dB = [float(x["pt"]["delta_FLAT"]) for x, q in zip(sub, fl) if not q]
        R2[f"{f}|{nm}"] = dict(n=len(sub), above=sum(fl), below=len(sub) - sum(fl), above_flat=aF_, med_dFLAT_A=float(np.median(dA)) if dA else None,
                               med_dFLAT_B=float(np.median(dB)) if dB else None, med_D_A=float(np.median([float(x["pt"]["D"]) for x, q in zip(sub, fl) if q])) if dA else None)
        rows.append(f"{nm} {len(sub)} (stars only, lower-bound M200): A {sum(fl)} / B {len(sub) - sum(fl)} [flat A {aF_}]; median delta_FLAT A "
                    + (f"{np.median(dA):+.3f}" if dA else "-") + ", B " + (f"{np.median(dB):+.3f}" if dB else "-"))
    for nm, sub in (("RC100 z>=2", rc2), ("RC100 all z", RC)):
        fl = [side(lm200(x["lmb"]), x["z"], f, "MDEC") for x in sub]; fl = [not q for q in fl] if MUTATE else fl
        ftab = [side(lm200(x["lmb_tab"]), x["z"], f, "MDEC") for x in sub if math.isfinite(x["lmb_tab"])]
        fA = [x["fd"] for x, q in zip(sub, fl) if q]; fB = [x["fd"] for x, q in zip(sub, fl) if not q]
        R2[f"{f}|{nm}"] = dict(n=len(sub), above=sum(fl), below=len(sub) - sum(fl), above_tabMbar=sum(ftab), med_fDM_A=float(np.median(fA)) if fA else None,
                               med_fDM_B=float(np.median(fB)) if fB else None)
        rows.append(f"{nm} {len(sub)} (class D; M_b(<R_e) lower bound): A {sum(fl)} / B {len(sub) - sum(fl)} [tabulated logMbar variant: A {sum(ftab)}]; median f_DM(<R_e) A "
                    + (f"{np.median(fA):.2f}" if fA else "-") + ", B " + (f"{np.median(fB):.2f}" if fB else "-"))
    fl, _ = flags_for(KU2, MU0, DL0, f, LAW0); fl = (~fl) if MUTATE else fl
    rows.append(f"KURVS 10: A {int(fl.sum())} / B {int((~fl).sum())}")
    P(f"  [{f}]\n    " + "\n    ".join(rows))
RES["R2_R3"] = R2

# ------------------------------------------------------------------ R4 flag robustness (reported): mu/delta bracket, M200 +-0.3 dex, bg B, flat
P("\n=== R4 (reported) KURVS flag robustness: number above M_x over the bracket")
R4 = {}
for f in FEET:
    cnt = {}
    for mu in (0.25, 0.67, 1.5, 4.0):
        for dl in (-0.2, 0.0, 0.2):
            for off in (-0.3, 0.0, 0.3):
                cnt[(mu, dl, off)] = int(flags_for(KU2, mu, dl, f, "MDEC", off)[0].sum())
    nBmax = max(10 - c for c in cnt.values())
    fb = int(flags_for(KU2, MU0, DL0, f, "MDEC", 0.0, "B_cfg886_bg")[0].sum()); ff = int(flags_for(KU2, MU0, DL0, f, "FLAT")[0].sum())
    R4[f] = dict(min_above=min(cnt.values()), max_below=nBmax, bgB_above=fb, flat_above=ff)
    # margin: smallest log M200 - log M_x over KURVS at the most adverse bracket corner (mu 0.25, delta -0.2, off -0.3)
    marg = min(lm200(math.log10(10 ** (o["lm"] - 0.2) * 1.25), -0.3) - lmx(f, o["z"], "MDEC") for o in KU2)
    R4[f]["min_margin_dex"] = marg
    P(f"  [{f}] above M_x: min {min(cnt.values())}/10 over mu x delta x (M200 +-0.3 dex); bg B {fb}/10; flat {ff}/10; smallest log M200 - log M_x at the adverse corner {marg:+.2f} dex")
RES["R4"] = R4

# ------------------------------------------------------------------ R5 future samples (reported)
P("\n=== R5 (reported) what a split test needs: the baryonic mass at the crossover, M_b,x(z) = EM1 inverse of M_x(z) (bg A, M-DEC)")
R5 = {}
for f in FEET:
    r = {str(z): (lmx(f, z) - EA) / EB + 10.0 for z in ZT}; R5[f] = r
    P(f"  [{f}] log M_b,x: " + ", ".join(f"z {z}: {v:.2f}" for z, v in r.items()))
P("  A split test at z 1-2.5 needs >= 3 (CFG385: >= 10-20 for a0 itself) discs on EACH side, each spanning y >~ 3 to <~ 0.3 at ~5 % in velocity,")
P("  with measured gas and outer dispersion; the below side must have M_b below the values printed above (dwarf-mass discs at z >~ 1).")
RES["R5_logMb_cross"] = R5

# ------------------------------------------------------------------ checks
CHECKS.append(("K5 peak RSS < 1 GB", rss() < 1.0))
P(f"\n=== CHECKS (saturated halos counted: {SAT['n']})")
for k, ok in CHECKS: P(f"  [{'PASS' if ok else 'FAIL'}] {k}")
n = sum(ok for _, ok in CHECKS); RES["checks"] = {k: bool(ok) for k, ok in CHECKS}; RES["saturated"] = SAT["n"]
P(f"\nchecks {n}/{len(CHECKS)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"x61_switch_high_z{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x61_switch_high_z_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(CHECKS) else 1)
