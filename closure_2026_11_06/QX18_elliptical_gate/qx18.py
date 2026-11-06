"""QX18: grade the a0 law on the 7 Humphrey+2006 X-ray ellipticals at 2, 4, 8 Re, G7 line 0.15 dex.
Criteria: FROZEN_CRITERIA.md (032ceedf31). Kappa = 1/2 FITTED; not theory closed.
    python3 qx18.py            -> qx18.json / qx18.out
    python3 qx18.py --mutate   -> qx18_MUTATE.json / qx18_MUTATE.out  (M1 Newton, M2 planted +-0.3 dex)
"""
import os, sys, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
DATA = os.path.join(REPO, "real_research", "data")
MUT = "--mutate" in sys.argv; TAG = "qx18_MUTATE" if MUT else "qx18"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)

G, MS, PC = 6.674e-11, 1.989e30, 3.0857e16; KPC = 1e3 * PC
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}   # = QX5
LINE = 0.15; RADII = (2.0, 4.0, 8.0); QX16 = {"canonical": 0.210, "alt": 0.189}
def glaw(gN, a0): return 0.5 * gN + math.sqrt(0.25 * gN ** 2 + a0 * gN)        # = QX5 glaw (simple nu)
def gnewt(gN, a0): return gN

def make(d):
    """Per-row mass models (explicit factory: no late binding)."""
    LK = float(d["LK_1e11"]) * 1e11; Re = float(d["Re_kpc"]); Mv = float(d["Mvir_1e12"]) * 1e12
    Rv = float(d["Rvir_kpc"]); c = float(d["c"]); a = Re / 1.8153; rs = Rv / c
    Mfit = float(d["ups_fit"]) * LK; Mh = Mv - Mfit; mc = math.log(1 + c) - c / (1 + c)
    def Mobs(r): return Mh * (math.log(1 + r / rs) - (r / rs) / (1 + r / rs)) / mc + Mfit * r ** 2 / (r + a) ** 2
    def Mstar(r, ups): return ups * LK * r ** 2 / (r + a) ** 2
    return dict(name=d["name"], LK=LK, Re=Re, Mvir=Mv, Rvir=Rv, Mobs=Mobs, Mstar=Mstar,
                uk=float(d["ups_krou"]), us=float(d["ups_salp"]))

rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "humphrey2006_ellipticals.tsv")) if not l.startswith("#")]
hdr, rows = rows[0], rows[1:]
GAL = [make(dict(zip(hdr, r))) for r in rows]
assert len(GAL) == 7 and len({round(g["Mobs"](g["Rvir"]), -6) for g in GAL}) == 7

def Mlaw(Mb_sun, r_kpc, a0, law):
    r = r_kpc * KPC; gN = G * Mb_sun * MS / r ** 2
    return law(gN, a0) * r ** 2 / G / MS

def offsets(a0, ups="uk", law=glaw, plant=0.0):
    per, pts = [], []
    for g in GAL:
        ds = []
        for m in RADII:
            r = m * g["Re"]; Mb = g["Mstar"](r, g[ups])
            ds.append(math.log10(g["Mobs"](r) / Mlaw(Mb, r, a0, law)) + plant)
        per.append(float(np.mean(ds))); pts.append(ds)
    return per, pts

def gas_to_null(g, a0, ups="uk"):
    """Extra baryon (gas) mass inside 8 Re for M_law to equal M_obs there, in units of the total stellar mass."""
    r = 8 * g["Re"]; Mo = g["Mobs"](r); lo, hi = 0.0, 1e3 * Mo
    Ms = g["Mstar"](r, g[ups])
    for _ in range(200):
        m = 0.5 * (lo + hi)
        if Mlaw(Ms + m, r, a0, glaw) < Mo: lo = m
        else: hi = m
    return 0.5 * (lo + hi) / (g[ups] * g["LK"])

def spearman(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0, 1])

def lab(D): return "PASS" if abs(D) <= LINE else "FAIL"

RES = dict(tag=TAG, criteria="032ceedf31", line=LINE, note="kappa = 1/2 FITTED; not theory closed", foot={})
P(f"QX18 {'MUTATE' if MUT else 'MAIN'}: a0 law on 7 Humphrey+2006 X-ray ellipticals at 2,4,8 Re; G7 line {LINE} dex; "
  "Kroupa primary, Salpeter systematic, gas neglected (upper bound on the miss). Spherical: exact field = law.")

# KA2: law value vs independent AQUAL root mu(g/a0) g = gN, mu = x/(1+x)
ka2 = 0.0
for gN in (1e-12, 1e-11, 1e-10, 1e-9):
    a0 = A0["canonical"]; lo, hi = gN, gN + 10 * math.sqrt(a0 * gN) + 10 * gN
    for _ in range(300):
        m = 0.5 * (lo + hi); x = m / a0
        if x / (1 + x) * m < gN: lo = m
        else: hi = m
    ka2 = max(ka2, abs(0.5 * (lo + hi) / glaw(gN, a0) - 1))
P(f"KA2 AQUAL-identity check: max rel diff {ka2:.2e} (line 1e-12) -> {'PASS' if ka2 <= 1e-12 else 'FAIL'}")
RES["KA2"] = ka2

ok = True
for f, a0 in A0.items():
    per_k, pts_k = offsets(a0, "uk"); per_s, _ = offsets(a0, "us")
    Dk, Ds = float(np.mean(per_k)), float(np.mean(per_s))
    err_gg = float(np.std(per_k, ddof=1) / math.sqrt(7)); err = math.hypot(err_gg, abs(Ds - Dk))
    o = dict(D_kroupa=Dk, D_salpeter=Ds, median_kroupa=float(np.median(per_k)), err_galaxy=err_gg, err_cfg32style=err,
             z_reported=Dk / err, per_galaxy={g["name"]: dict(kroupa=pk, salpeter=ps, points=pt, gas_to_null_over_Mstar=gas_to_null(g, a0))
                                               for g, pk, ps, pt in zip(GAL, per_k, per_s, pts_k)},
             spearman_logMvir=spearman(np.log10([g["Mvir"] for g in GAL]), per_k),
             spearman_logLK=spearman(np.log10([g["LK"] for g in GAL]), per_k))
    if not MUT:
        o["KA1"] = abs(Dk - QX16[f]); o["KA1_pass"] = o["KA1"] <= 1e-3 + 5e-4   # QX16 prints 3 decimals (rounding half-step)
        o["label"] = lab(Dk)
        P(f"[{f}] D (Kroupa) {Dk:+.4f} dex; median {o['median_kroupa']:+.4f}; Salpeter {Ds:+.4f}; "
          f"err (g-g) {err_gg:.3f}, CFG32-style {err:.3f} -> {Dk/err:.2f} sigma (reported)")
        P(f"[{f}] KA1 vs QX16 {QX16[f]:+.3f}: |diff| {o['KA1']:.4f} -> {'PASS' if o['KA1_pass'] else 'FAIL'}")
        for g, pk, ps, pt in zip(GAL, per_k, per_s, pts_k):
            P(f"[{f}]   {g['name']:8s} Mvir {g['Mvir']:.2e}  d {pk:+.3f} (Salp {ps:+.3f})  pts {', '.join(f'{x:+.3f}' for x in pt)}  "
              f"gas to null @8Re {o['per_galaxy'][g['name']]['gas_to_null_over_Mstar']:.2f} M*")
        P(f"[{f}] mass trend: Spearman(d, log Mvir) {o['spearman_logMvir']:+.2f}, (d, log L_K) {o['spearman_logLK']:+.2f}")
        P(f"[{f}] LABEL (G7 line {LINE}): {o['label']}" + (" -- the law UNDER-predicts" if Dk > LINE else ""))
    else:
        nN, _ = offsets(a0, "uk", law=gnewt); DN = float(np.mean(nN))
        up, _ = offsets(a0, "uk", plant=+0.3); dn, _ = offsets(a0, "uk", plant=-0.3)
        Du, Dd = float(np.mean(up)), float(np.mean(dn))
        m1 = DN > LINE; m2 = abs(Du - Dk - 0.3) <= 1e-9 and abs(Dd - Dk + 0.3) <= 1e-9
        m2lab = (lab(Dd) != lab(Dk)) if (abs(Dk - 0.3) <= LINE) != (abs(Dk) <= LINE) else True
        o.update(M1_newton_D=DN, M1_bites=m1, M2_up=Du, M2_down=Dd, M2_shift_ok=m2, M2_label_ok=m2lab)
        ok = ok and m1 and m2 and m2lab
        P(f"[{f}] M1 Newton D {DN:+.3f} -> {'BITES' if m1 else 'NO POWER'}; M2 +0.3 -> {Du:+.4f}, -0.3 -> {Dd:+.4f} "
          f"(shift ok {m2}; label {lab(Dk)} -> {lab(Dd)} ok {m2lab})")
    RES["foot"][f] = o

if MUT: P(f"MUTATE: {'ALL BITE' if ok else 'A CONTROL FAILED'}")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (ok if MUT else True) else 1)
