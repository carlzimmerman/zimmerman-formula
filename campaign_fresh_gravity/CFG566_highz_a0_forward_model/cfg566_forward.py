#!/usr/bin/env python3
"""CFG566: forward-model the committed high-z implied-a0 estimators (CFG270 KMOS3D PT1; CFG303 RC100 native route B quartiles) under three truths:
(A) a0 tracking rho_DE (CFG223 M-DEC), (B) flat a0, (C) LCDM with feedback (CFG565 machinery: Moster13(z) + DC14 + Dutton-Maccio c(M,z)).
Frozen criteria: FROZEN_CRITERIA.md (379260732), committed before this script.  kappa = 1/2 FITTED; cold mass required, no DM particle; not theory closed.
Run: python3 cfg566_forward.py [--mutate]
"""
import os, sys, io, json, math, csv, contextlib
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE); REPO = os.path.dirname(CFG)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT, CHK = [], []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(name, val, ok): CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")

# ---------------------------------------------------------------- committed machinery (exec'd, not edited)
sys.path.insert(0, os.path.join(CFG, "HZQ_common"))
with contextlib.redirect_stdout(io.StringIO()):
    import hzq_core as H
NU, A0C, A0A = H.NU, H.A0C, H.A0A
implied = H.AI.implied                                               # CFG223's estimator (bit-identical, CFG270 C4)

def exec_upto(path, stop, env=None):
    src = open(path).read(); assert src.count(stop) == 1, (path, stop)
    saved = {k: os.environ.get(k) for k in (env or {})}
    os.environ.update(env or {}); ns = {"__file__": path, "__name__": "cfg566_exec"}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:src.index(stop)], os.path.relpath(path, REPO), "exec"), ns)
    finally:
        for k, v in saved.items():
            if v is None: os.environ.pop(k, None)
            else: os.environ[k] = v
    return ns, src

# CFG270 inputs (the source up to its STAGE A marker writes nothing)
F270 = os.path.join(CFG, "CFG270_kmos3d_cube_fits", "cfg270_kmos3d_fits.py")
n270, s270 = exec_upto(F270, "# ================================================================== STAGE A", env={"STAGE": "B", "MUTATE": "0", "SELFTEST": "0"})
T1 = n270["T1"]; Z1 = n270["Z"][T1]; MS1 = n270["MS"][T1]; LMS1 = n270["LMS"][T1]; RE1 = n270["RE"][T1]; R1 = n270["R"][T1]; RD1 = n270["RD"][T1]
GB0u = n270["GB0"][T1] / MS1                                         # stars-only g_bar per unit mass (thin disc, H-band R_e)
MU1 = n270["MUV"][T1]                                                # CFG270 B2 scaling gas (G1 branch)
# CFG223 analyse (as CFG303 loads it)
F223 = os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")
n223, _ = exec_upto(F223, 'P("\\nCONTROLS")')
J223 = json.load(open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_results.json")))
EDGES = np.array(J223["edges"]); CUR = J223["curves"]
def mdec(z): return np.interp(z, CUR["z"], CUR["M-DEC"])
# CFG565 (Moster13(z), Dutton-Maccio) and CFG477 (DC14) functions, exec'd as CFG565 does
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19                        # CFG476's constants
s565 = open(os.path.join(CFG, "CFG565_feedback_gdagger_vs_z", "cfg565_gdagger_z.py")).read()
n565 = {"math": math, "np": np, "brentq": brentq, "G": G}
exec(s565[s565.index("H, OM = 0.7, 0.315"):s565.index("k2 = abs(")], n565)
s477 = open(os.path.join(CFG, "CFG477_lcdm_dc14_rar", "cfg477_dc14.py")).read()
n477 = {"np": np, "math": math}; exec(s477[s477.index("XG = np.logspace"):s477.index("def halo_g")], n477)
moster, inv, cdm, E, RHOC0, HH = n565["moster"], n565["inv"], n565["cdm"], n565["E"], n565["RHOC0"], n565["H"]
XG, menc, dc14 = n477["XG"], n477["menc"], n477["dc14"]

# RC100 native route B (committed per-galaxy CSV)
rows = list(csv.DictReader(open(os.path.join(CFG, "CFG303_lcdm_free_inputs", "cfg303_rc100_pergalaxy_LCDMFREE.csv"))))
ZR = np.array([float(r["z"]) for r in rows]); GOR = np.array([float(r["g_obs_ms2"]) for r in rows]); GBR = np.array([float(r["g_bar_native_B_ms2"]) for r in rows])
LMSR = np.array([float(r["logMstar_SED_col6"]) for r in rows]); MUR = np.array([float(r["mu_t18"]) for r in rows]); RER = np.array([float(r["Re_kpc"]) for r in rows])
MBR = 10 ** LMSR * (1 + MUR); GBRu = GBR / MBR
def rc_mask(z, i):
    lo, hi = EDGES[i], EDGES[i + 1]; return (z >= lo) & ((z < hi) | ((i == 3) & (z <= hi)))
J303 = json.load(open(os.path.join(CFG, "CFG303_lcdm_free_inputs", "cfg303_rc100_cristal_LCDMFREE_results.json"))); J303 = J303.get("numbers", J303)["points"]["RC100"]

P(__doc__.split("Run:")[0].strip())
# ---------------------------------------------------------------- controls K1, K2, K4
P("\nCONTROLS")
V22, SIG = n270["M"]["V22"].values.astype(float), n270["M"]["sig0"].values.astype(float); SIG = np.where(np.isfinite(SIG), SIG, 0.0)
GOk = (V22 ** 2 + 2.0 * (n270["R"] / n270["RD"]) * SIG ** 2) / n270["R"] * H.G2SI
ls_k1, st_k1 = H.s_status((GOk / n270["GB0"])[T1], n270["GB0"][T1])
OBS_R1 = 10 ** ls_k1
check("K1 CFG270 PT1 reproduced from its inputs (72 T1 fits)", f"s* = {OBS_R1:.4f} ({st_k1}) vs committed 2.4413", st_k1 == "root" and abs(OBS_R1 - 2.4413) < 1e-3 and int(T1.sum()) == 72)
OBS_RC, k2 = {}, True
for i in range(4):
    m = rc_mask(ZR, i); r, _, _ = n223["analyse"](dict(z=ZR[m], D=GOR[m] / GBR[m], gb=GBR[m]))
    c = J303[f"B Q{i + 1}"]; ok = (r["unbounded"] == c["unbounded"]) and (r["unbounded"] or abs(r["log_s"] - c["log_s"]) < 1e-6)
    k2 &= ok; OBS_RC[f"Q{i + 1}"] = dict(ls=(-3.0 if r["unbounded"] else r["log_s"]), n=int(m.sum()), z_med=r["z_med"], unbounded=r["unbounded"])
    P(f"    RC100 B Q{i + 1}: n {int(m.sum())}, z_med {r['z_med']:.2f}, s* {'NO ROOT' if r['unbounded'] else f'{r[chr(115)]:.4f}'} (committed {'NO ROOT' if c['unbounded'] else f'{c[chr(115)]:.4f}'})")
check("K2 RC100 native B Q1-Q4 reproduced through CFG223 analyse", "see above", k2)
check("K4 CFG565 K2: Moster z-terms vanish at z = 0 (exec'd code)", f"moster(12, 0) = {moster(12.0, 0.0):.6f}", abs(moster(12.0, 0.0) - moster(12.0, 1e-12)) < 1e-9)

# ---------------------------------------------------------------- truths
def g_halo(lMs, z, r_kpc, rng, n):
    """(n,) LCDM-with-feedback halo acceleration at r (m s^-2), CFG565's recipe at redshift z (SHMR 0.15 dex, c 0.11 dex scatter)."""
    l0 = inv(lMs, z); e = 1e-3; sl = max((moster(l0 + e, z) - moster(l0 - e, z)) / (2 * e), 1e-3)
    rhoc = RHOC0 * E(z) ** 2; out = np.empty(n); r = r_kpc * KPC
    for k in range(n):
        Mh = 10 ** (l0 + rng.normal(0, 0.15) / sl); c0 = cdm(Mh, z) * 10 ** rng.normal(0, 0.11)
        a_, b_, g_, cb = dc14(lMs - math.log10(Mh))[:4]; cc = c0 * (1 + cb)
        R200 = (3 * Mh * MSUN / (4 * math.pi * 200 * rhoc)) ** (1 / 3); rs = R200 / cc
        m = menc(a_, b_, g_); out[k] = G * Mh * MSUN * np.interp(r / rs, XG, m) / np.interp(cc, XG, m) / r ** 2
    return out

NR = 1000
def mocks(truth, gbu, Mcat, z, lMs, rk, gasfac, recipe, seed, noise=True):
    """log s* of the pooled row per realisation (floor -3, ceiling +3). gbu: estimator's g_bar per unit catalogue mass; gasfac: true/catalogue baryon factor."""
    rng = np.random.default_rng(seed); n = len(z)
    dsh = rng.normal(0, 0.15, NR) if noise else np.zeros(NR)
    di = rng.normal(0, 0.20, (NR, n)) if noise else np.zeros((NR, n))
    Mtrue = Mcat[None, :] * gasfac[None, :] * 10 ** (dsh[:, None] + di)
    gbt = gbu[None, :] * Mtrue
    kind, foot = truth
    if kind == "C":
        gh = np.column_stack([g_halo(lMs[j], z[j], rk[j], rng, NR) for j in range(n)]); go = gbt + gh
    else:
        a0 = (A0C if foot == "can" else A0A) * (mdec(z) if kind == "A" else np.ones(n))
        go = gbt * NU(gbt / a0[None, :])
    if noise: go = go * 10 ** rng.normal(0, 0.15, (NR, n))
    gbe = gbu[None, :] * Mcat[None, :]
    gbe = np.broadcast_to(gbe, go.shape)
    D = go / gbe; ls, unb = implied(D, gbe, NU, A0C)
    medD = np.median(D, axis=1); ls = np.where(unb, np.where(medD <= 1, -3.0, 3.0), ls)
    if noise and recipe > 0: ls = np.where(unb, ls, ls + rng.normal(0, recipe, NR))
    return ls

TR = {"A_can": ("A", "can"), "A_alt": ("A", "alt"), "B_can": ("B", "can"), "B_alt": ("B", "alt"), "C": ("C", None)}
LAB = dict(TR)
if MUT: LAB["C"], LAB["A_can"], LAB["A_alt"] = ("A", "can"), ("C", None), ("C", None)
P("\n*** MUTATE: A and C mocks swap labels ***" if MUT else "")

# K3 noiseless injection on R1
k3a = mocks(("A", "can"), GB0u, MS1, Z1, LMS1, R1, np.ones(72), 0.0, 1, noise=False)[0]
k3b = mocks(("B", "can"), GB0u, MS1, Z1, LMS1, R1, np.ones(72), 0.0, 1, noise=False)[0]
tgt = math.log10(np.median(mdec(Z1)))
check("K3 noiseless injection on R1: A(canonical, G0) returns median a0(z_i)/a0C within 0.03 dex; B returns 1 to 1e-6", f"A {10 ** k3a:.4f} vs {10 ** tgt:.4f}; B {10 ** k3b:.6f}", abs(k3a - tgt) < 0.03 and abs(k3b) < 1e-6)

def summ(ls, obs):
    q = np.percentile(ls, [2.3, 16, 50, 84, 97.7])
    return dict(p2=q[0], p16=q[1], med=q[2], p84=q[3], p98=q[4], hw=(q[3] - q[1]) / 2, p_lo=float(np.mean(ls <= obs + 1e-12)), p_hi=float(np.mean(ls >= obs - 1e-12)),
                frac_floor=float(np.mean(ls <= -3)))

RES = {}
def row(name, args, obs, kind_rule, branch=""):
    P(f"\n{name}{(' [' + branch + ']') if branch else ''}: committed log s* = {obs:+.3f} (s* = {'NO ROOT/floor' if obs <= -3 else f'{10 ** obs:.3f}'})")
    out = {}
    for k, t in LAB.items():
        ls = mocks(t, *args, seed=566 + 17 * list(TR).index(k))
        s = summ(ls, obs); out[k] = s
        P(f"    {k:6s}: median s* {10 ** s['med']:.3g} (16-84% {10 ** s['p16']:.3g}-{10 ** s['p84']:.3g}; 2.3-97.7% {10 ** s['p2']:.3g}-{10 ** s['p98']:.3g}); floor frac {s['frac_floor']:.2f}; p_lo {s['p_lo']:.4f}, p_hi {s['p_hi']:.4f}")
    RES[name + ("|" + branch if branch else "")] = out
    return out

recipe = 0.61
argsG0 = (GB0u, MS1, Z1, LMS1, R1, np.ones(72), recipe)
argsG1 = (GB0u, MS1, Z1, LMS1, R1, 1 + MU1, recipe)
r1g0 = row("R1 KMOS3D PT1", argsG0, ls_k1, "bound", "G0 no gas")
r1g1 = row("R1 KMOS3D PT1", argsG1, ls_k1, "bound", "G1 B2 scaling gas")
rcr = {}
for i in range(4):
    m = rc_mask(ZR, i); q = f"Q{i + 1}"
    rcr[q] = row(f"R{i + 2} RC100 B {q}", (GBRu[m], MBR[m], ZR[m], LMSR[m], RER[m], np.ones(int(m.sum())), 0.0), OBS_RC[q]["ls"], "measured")

# ---------------------------------------------------------------- power and verdicts
def power(o):
    pw = []
    for a in ("A_can", "A_alt"):
        pw.append(abs(o[a]["med"] - o["C"]["med"]) / math.hypot(o[a]["hw"], o["C"]["hw"]))
    return min(pw)
P("\nPOWER (|median_A - median_C| / sqrt(hw_A^2 + hw_C^2), A at the less separated footing)")
PW = {"R1": power(r1g0)}
for q in rcr: PW[f"RC100 {q}"] = power(rcr[q])
for k, v in PW.items(): P(f"    {k}: {v:.2f} -> {'POWERED' if v >= 1 else 'NON-DISCRIMINATING row'}")
# diagnostic (not a verdict input): R1 G0 without recipe and without the shared zero-point
def mocks_diag(t, seed):
    rng = np.random.default_rng(seed); n = 72
    di = rng.normal(0, 0.20, (NR, n)); gbt = GB0u[None, :] * MS1[None, :] * 10 ** di
    if t[0] == "C": go = gbt + np.column_stack([g_halo(LMS1[j], Z1[j], R1[j], rng, NR) for j in range(n)])
    else: go = gbt * NU(gbt / ((A0C if t[1] == "can" else A0A) * mdec(Z1))[None, :])
    go = go * 10 ** rng.normal(0, 0.15, (NR, n)); gbe = np.broadcast_to(GB0u * MS1, go.shape)
    ls, unb = implied(go / gbe, gbe, NU, A0C); return np.where(unb, np.where(np.median(go / gbe, axis=1) <= 1, -3.0, 3.0), ls)
dg = {k: summ(mocks_diag(LAB[k], 9000 + j), ls_k1) for j, k in enumerate(("A_can", "A_alt", "C"))}
PW_diag = power(dg)
P(f"    R1 DIAGNOSTIC (no recipe, no shared zero-point; not a verdict input): power {PW_diag:.2f}; medians A_can {10 ** dg['A_can']['med']:.3g}, A_alt {10 ** dg['A_alt']['med']:.3g}, C {10 ** dg['C']['med']:.3g} (hw {dg['A_can']['hw']:.2f} / {dg['C']['hw']:.2f} dex)")

P("\nROW FLAGS")
FL = {}
def flags_R1(k):
    hi = r1g0[k]["p_lo"] < 0.0228; lo = r1g1[k]["p_hi"] < 0.0228
    return "TOO HIGH" if hi else ("TOO LOW" if lo else "ok")
for k in TR: FL[("R1", k)] = flags_R1(k)
for q in rcr:
    for k in TR: FL[(f"RC100 {q}", k)] = "MISSES" if min(rcr[q][k]["p_lo"], rcr[q][k]["p_hi"]) < 0.00135 else "ok"
for rname in PW:
    P(f"    {rname}: " + ", ".join(f"{k} {FL[(rname, k)]}" for k in TR))
def fw_dis(rn): return FL[(rn, "A_can")] != "ok" and FL[(rn, "A_alt")] != "ok"
def c_dis(rn): return FL[(rn, "C")] != "ok"
powered = [rn for rn in PW if PW[rn] >= 1]
cdis = [rn for rn in powered if c_dis(rn) and not fw_dis(rn)]
fdis = [rn for rn in powered if fw_dis(rn) and not c_dis(rn)]
nfit = [rn for rn in powered if fw_dis(rn) and c_dis(rn)]
if not powered: V = "NON-DISCRIMINATING"
elif cdis and fdis: V = "BOTH DISFAVOURED"
elif cdis: V = "FEEDBACK-LCDM DISFAVOURED"
elif fdis: V = "FRAMEWORK DISFAVOURED"
elif nfit: V = "NEITHER FITS"
else: V = "CONSISTENT WITH BOTH"
P(f"\nVERDICT: {V}  (powered rows: {powered or 'none'}; C disfavoured on {cdis or 'none'}; framework disfavoured on {fdis or 'none'}; neither fits on {nfit or 'none'})")
he1 = 0.6 <= 10 ** r1g0["A_can"]["med"] <= 1.2 and 10 ** r1g0["C"]["med"] >= 2
P(f"HAND ESTIMATES: HE1 {'hit' if he1 else 'MISS'} (A_can {10 ** r1g0['A_can']['med']:.3g}, C {10 ** r1g0['C']['med']:.3g}); HE2 {'hit' if PW['R1'] < 1 else 'MISS'} (power {PW['R1']:.2f}); HE3 {'hit' if PW_diag >= 1 else 'MISS'} (diagnostic {PW_diag:.2f})")
P(f"CONTROLS: {sum(CHK)}/{len(CHK)} pass")

def js(o):
    if isinstance(o, dict): return {str(k): js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [js(v) for v in o]
    if isinstance(o, (np.floating, np.integer, np.bool_)): return o.item()
    return o
RESJ = dict(verdict=V, power=PW, power_diag_R1=PW_diag, flags={f"{a}|{b}": v for (a, b), v in FL.items()}, rows=RES, obs=dict(R1=ls_k1, **{k: v["ls"] for k, v in OBS_RC.items()}),
            diag_R1=dg, controls=CHK, mutate=MUT)
json.dump(js(RESJ), open(os.path.join(HERE, f"cfg566_forward{TAG}_results.json"), "w"), indent=1)
if MUT:
    main = json.load(open(os.path.join(HERE, "cfg566_forward_results.json")))
    d = abs(r1g0["C"]["med"] - main["rows"]["R1 KMOS3D PT1|G0 no gas"]["C"]["med"])
    ok = d > 0.1
    P(f"MUTATE: C-labelled R1 (G0) median log s* moved by {d:.3f} dex; verdict {main['verdict']} -> {V} ({'changed' if V != main['verdict'] else 'unchanged'}) -> {'DETECTED (exit 1)' if ok else 'NOT detected'}")
    open(os.path.join(HERE, f"cfg566_forward{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if ok else 0)
open(os.path.join(HERE, f"cfg566_forward{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK) else 1)
