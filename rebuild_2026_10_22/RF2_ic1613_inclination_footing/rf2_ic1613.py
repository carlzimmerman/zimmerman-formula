#!/usr/bin/env python3
"""RF2_ic1613_inclination_footing: how much of IN2's failure rests on the Read+16 stellar-kinematic inclination?
Criteria FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (6b060cbb33, committed alone). IN1's model copied; no new data; IN1's falsifier stands.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I rf2_ic1613.py     (RF2_MUTATE=1 twin: projection sin/cos swapped; K2 must fail)
kappa = 1/2 FITTED; footings never pooled; not theory closed; nothing here says the data favour the framework.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, hashlib, resource
import numpy as np
import fitz
from scipy import ndimage as ni
sys.dont_write_bytecode = True
MUT = os.environ.get("RF2_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
P(f"RF2_ic1613_inclination_footing {'MUTATE' if MUT else 'normal run'}  (criteria 6b060cbb33); kappa = 1/2 FITTED; not theory closed")

# ---------------------------------------------------------------- (a) IN1's model, unchanged
G, MSUN, PC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16
KPC = 1e3 * PC; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
nu = lambda y: 0.5 + math.sqrt(0.25 + 1.0 / y)
SIG, RH, MS, MG, VROT48, RMAX, I0, VST = 10.8, 1439.78, 2.88e7, 5.93e7, 16.9, 2.71, 48.0, 13.0
MS_X1 = 10 ** 8.28; S_SIG, S_HI = 0.0792, 0.075; r12 = 4 / 3 * RH * PC
def vsq_disc(i, q):
    i = math.radians(i); return SIG ** 2 / (q * q * math.cos(i) ** 2 + math.sin(i) ** 2) * (2 + q * q)
def E_sigma(i, q, a0, ms=MS, spherical=False, mbh=None, vrot=VST):
    v2 = 3 * SIG ** 2 if spherical else vsq_disc(i, q) + vrot ** 2
    gobs = v2 * 1e6 / r12; m = 0.5 * ms + 0.5 * MG if mbh is None else mbh; gN = G * m * MSUN / r12 ** 2
    return math.log10(gobs) - math.log10(nu(gN / a0) * gN)
def E_HI(i, a0, ms=MS):
    V = VROT48 * math.sin(math.radians(I0)) / math.sin(math.radians(i)); gobs = (V * 1e3) ** 2 / (RMAX * KPC); gN = G * (ms + MG) * MSUN / (RMAX * KPC) ** 2
    return math.log10(gobs) - math.log10(nu(gN / a0) * gN)
IS = np.round(np.arange(10.0, 60.001, 0.5), 1)
def interval(m):
    x = IS[m]; return [float(x.min()), float(x.max())] if len(x) else None
def band_HI(a0, ms=MS, s=S_HI): return interval(np.array([abs(E_HI(i, a0, ms) / s) < 2 for i in IS]))
def band_sig(a0, q, ms=MS, s=S_SIG): return interval(np.array([abs(E_sigma(i, q, a0, ms) / s) < 2 for i in IS]))
checks = {}
e0 = E_sigma(48, 1.0, A0["canonical"], spherical=True, mbh=0.5 * MS_X1, vrot=0.0); e0b = E_HI(48, A0["canonical"])
checks["K0"] = abs(e0 + 0.535162) < 0.01 and abs(e0b + 0.5928) < 0.001
BAND = {f: band_HI(a) for f, a in A0.items()}
checks["K1"] = BAND["canonical"] == [18.5, 26.5] and BAND["alt"] == [18.0, 25.0]
P(f"K0 HO3 {e0:+.4f}, RT1 {e0b:+.4f}: {'PASS' if checks['K0'] else 'FAIL'}; K1 I_HI {BAND}: {'PASS' if checks['K1'] else 'FAIL'}")
RES = dict(criteria="6b060cbb33", mutate=MUT, band=BAND, table={}, verify={})
P("\n=== (a) E, Z against i (both tracers; q_sigma 0.6 shown in the table, all in JSON)")
for f, a0 in A0.items():
    P(f"[{f}]  i  E_HI  Z_HI  | E_sig(q.4) E_sig(q.6) Z_sig(q.6) E_sig(q.8)")
    rows = []
    for i in range(15, 51):
        r = dict(i=i, E_HI=E_HI(i, a0), Z_HI=E_HI(i, a0) / S_HI, **{f"E_sig_q{q}": E_sigma(i, q, a0) for q in (0.4, 0.6, 0.8)}, Z_sig_q06=E_sigma(i, 0.6, a0) / S_SIG); rows.append(r)
        if i % 5 == 0 or i in (32, 36, 37, 38, 39, 48): P(f"   {i:3d} {r['E_HI']:+.3f} {r['Z_HI']:+6.2f} | {r['E_sig_q0.4']:+.3f} {r['E_sig_q0.6']:+.3f} {r['Z_sig_q06']:+6.2f} {r['E_sig_q0.8']:+.3f}")
    RES["table"][f] = rows
    v = dict(I_sigma_q06=band_sig(a0, 0.6), I_HI_M_X1=band_HI(a0, MS_X1), I_sigma_q06_M_X1=band_sig(a0, 0.6, MS_X1), I_HI_s_lo=band_HI(a0, s=S_HI - 0.01), I_HI_s_hi=band_HI(a0, s=S_HI + 0.01))
    RES["verify"][f] = v; P(f"   verify: {v}")

# ---------------------------------------------------------------- posterior machinery
IG = np.arange(0.125, 90, 0.25); PHI = np.linspace(0, math.pi, 72, endpoint=False)
def eps_model(ic, e):
    """apparent ellipticity of a thin oval disc: singular values of diag(1, proj) R(phi) diag(1, 1 - e). MUTATE: proj = sin i."""
    proj = np.sin(np.radians(ic)) if MUT else np.cos(np.radians(ic))
    c, s = np.cos(PHI)[None, :], np.sin(PHI)[None, :]; pr = proj[:, None]; b = 1 - e
    m11, m12, m21, m22 = c, -s * b, pr * s, pr * c * b
    T = m11 ** 2 + m12 ** 2 + m21 ** 2 + m22 ** 2; D = np.abs(m11 * m22 - m12 * m21)
    ss = np.sqrt(np.maximum(T ** 2 - 4 * D ** 2, 0)); s1 = np.sqrt((T + ss) / 2); s2 = np.sqrt(np.maximum((T - ss) / 2, 0))
    return 1 - s2 / s1
def eps_thick(ic, q0):
    return (1 - np.sqrt(np.cos(np.radians(ic)) ** 2 * (1 - q0 ** 2) + q0 ** 2))[:, None]
def post(eps, se, em, prior="cos"):
    L = np.exp(-0.5 * ((em - eps) / se) ** 2).mean(1); w = L * (np.sin(np.radians(IG)) if prior == "cos" else 1.0); return w / w.sum()
def summ(w):
    c = np.cumsum(w); q = lambda p: float(np.interp(p, c, IG)); return dict(med=q(0.5), lo=q(0.16), hi=q(0.84), half=0.5 * (q(0.84) - q(0.16)), peak=float(IG[np.argmax(w)]))
def pband(w, b): return float(w[(IG >= b[0]) & (IG <= b[1])].sum())
def ratio(w): return float(np.interp(22.5, IG, w) / w.max())
def gauss(c, s):
    w = np.exp(-0.5 * ((IG - c) / s) ** 2); return w / w.sum()
w0 = post(0.2, 0.001, eps_model(IG, 0.0)); checks["K2"] = abs(summ(w0)["med"] - math.degrees(math.acos(0.8))) < 0.5
checks["K3"] = abs(float(post(0.2, 0.05, eps_model(IG, 0.1)).sum()) - 1) < 1e-12 and abs(float(gauss(36, 11).sum()) - 1) < 1e-12
P(f"\nK2 thin circular, tiny error: median {summ(w0)['med']:.2f} (arccos 0.8 = 36.87): {'PASS' if checks['K2'] else 'FAIL'}; K3 normalisation: {'PASS' if checks['K3'] else 'FAIL'}")

# ---------------------------------------------------------------- HI footprint from Fig. A.55 panel (a)
PDF = os.path.join(REPO, "deepseek_push", "G114_data", "oh2015", "HI_Spitzer_data_PV_ic1613.pdf")
d = fitz.open(PDF); x = d[0].get_images(full=True)[0]; pm = fitz.Pixmap(d, x[0]); A = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width, pm.n)[:, :, :3].astype(int)
FR = (117, 237, 117, 237)             # y0, y1, x0, x1, interior of panel (a), from the frame rows 116, 238
SUB = A[FR[0]:FR[1], FR[2]:FR[3]]; R, Gc, Bc = SUB[..., 0], SUB[..., 1], SUB[..., 2]
RAW = (R > Gc) & (Gc >= Bc) & (R < 250) & (R - Bc >= 8)
k8 = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
def clean(m): return m & (ni.convolve(m.astype(int), k8, mode="constant") >= 2)
def moments(m, wt=None):
    y, X = np.nonzero(m); w = np.ones(len(X)) if wt is None else wt[y, X]
    mx, my = np.average(X, weights=w), np.average(y, weights=w); dx, dy = X - mx, -(y - my)
    C = np.cov(np.vstack([dx, dy]), aweights=w); ev, V = np.linalg.eigh(C); a = V[:, 1]; pa = (math.degrees(math.atan2(-a[0], a[1]))) % 180   # RA increases to the left: east = -x
    return dict(ba=float(math.sqrt(ev[0] / ev[1])), pa=float(pa), maj=float(4 * math.sqrt(ev[1])), n=int(m.sum()), cx=float(mx), cy=float(my))
def body(m, dil):
    dm = ni.binary_dilation(clean(m), structure=np.ones((3, 3)), iterations=dil); lab, n = ni.label(dm); s = ni.sum(dm, lab, range(1, n + 1)); return ni.binary_fill_holes(lab == 1 + int(np.argmax(s)))
def measure(m): return moments(body(m, 3))
# K5: injection on the panel grid
yy, xx = np.mgrid[:SUB.shape[0], :SUB.shape[1]]; t = math.radians(70); ux, uy = xx - 60.0, -(yy - 60.0)
aa = -ux * math.sin(t) + uy * math.cos(t); bb = ux * math.cos(t) + uy * math.sin(t)
inj = (aa / 50.0) ** 2 + (bb / 40.0) ** 2 <= 1
mi = measure(inj); dpa = abs((mi["pa"] - 70 + 90) % 180 - 90); checks["K5"] = abs(mi["ba"] - 0.80) < 0.02 and dpa < 3
P(f"K5 injected b/a 0.80, PA 70: recovered {mi['ba']:.3f}, {mi['pa']:.1f}: {'PASS' if checks['K5'] else 'FAIL'}")
M0 = measure(RAW); VAR = dict(raw_no_fill=moments(clean(RAW)), dil2=moments(body(RAW, 2)), dil5=moments(body(RAW, 5)))
inten = np.where(RAW, R.astype(float), 0.0); VAR["intensity_weighted_reported"] = moments(clean(RAW), inten)
F = body(RAW, 3); rng = np.random.default_rng(0); BS = 8
by, bx = np.nonzero(F); key = (by // BS) * 1000 + bx // BS; ukeys = np.unique(key); ys = {k: np.nonzero(key == k)[0] for k in ukeys}; BA = []; PA = []
for _ in range(200):
    pick = rng.choice(ukeys, len(ukeys)); idx = np.concatenate([ys[k] for k in pick]); dx = bx[idx] - bx[idx].mean(); dy = -(by[idx] - by[idx].mean())
    ev, V = np.linalg.eigh(np.cov(np.vstack([dx, dy]))); BA.append(math.sqrt(ev[0] / ev[1])); PA.append(math.degrees(math.atan2(-V[0, 1], V[1, 1])) % 180)
spread = 0.5 * (max(VAR[k]["ba"] for k in ("raw_no_fill", "dil2", "dil5")) - min(VAR[k]["ba"] for k in ("raw_no_fill", "dil2", "dil5")))
SE_HI = math.hypot(float(np.std(BA)), spread); EPS_HI = 1 - M0["ba"]
# clip: mask pixels on the panel's border band; K4: scale
edge = np.zeros_like(F); edge[:2, :] = edge[-2:, :] = edge[:, :2] = edge[:, -2:] = True; touch = float((F & edge).sum() / edge.sum())
PX_ARCMIN = 4.9; dia = M0["maj"] / PX_ARCMIN; dia_ref = 2 * RMAX / 0.7 * 3437.75 / 1e3
checks["K4"] = 0.5 < dia / dia_ref < 2
P(f"HI footprint: b/a {M0['ba']:.3f}, PA {M0['pa']:.1f}, {M0['n']} px; boot sd b/a {np.std(BA):.3f}, PA {np.std(PA):.1f}; variants " + "; ".join(f"{k} {v['ba']:.3f}/{v['pa']:.0f}" for k, v in VAR.items()))
P(f"   eps_HI {EPS_HI:.3f} +- {SE_HI:.3f}; panel-edge pixels in the footprint {touch:.2f}; K4 diameter {dia:.1f}' vs 2 R_max {dia_ref:.1f}': {'PASS' if checks['K4'] else 'FAIL'}")
RES["hi_footprint"] = dict(main=M0, variants=VAR, boot_sd_ba=float(np.std(BA)), boot_sd_pa=float(np.std(PA)), eps=EPS_HI, se=SE_HI, edge_fraction=touch, diameter_arcmin=dia, K5=mi)

# ---------------------------------------------------------------- (b), (c) rows
EPS_O, SE_O = 0.20, 0.05
QUAL = ("optical isophote (e_int 0.10)", "HI footprint (e_int 0.10)", "Lake & Skillman 1989")
MUSE = ("MUSE Read+16 formalism", "MUSE Weijmans+08 formalism")
RW = {"MUSE Read+16 formalism": gauss(36, 11), "MUSE Weijmans+08 formalism": gauss(32, 11),
      "optical isophote (e_int 0.10)": post(EPS_O, SE_O, eps_model(IG, 0.10)), "HI footprint (e_int 0.10)": post(EPS_HI, SE_HI, eps_model(IG, 0.10)),
      "Lake & Skillman 1989": gauss(38, 5), "BRACKET Read+16 (LCDM-PROCESSED)": gauss(39, 2)}
for e in (0.0, 0.05, 0.15, 0.20):
    RW[f"optical e_int {e}"] = post(EPS_O, SE_O, eps_model(IG, e)); RW[f"HI e_int {e}"] = post(EPS_HI, SE_HI, eps_model(IG, e))
for q0 in (0.2, 0.4, 0.6): RW[f"optical thick q0 {q0}"] = post(EPS_O, SE_O, eps_thick(IG, q0))
RW["optical e_int 0.10, prior flat in i"] = post(EPS_O, SE_O, eps_model(IG, 0.10), prior="flat")
RW["HI e_int 0.10, prior flat in i"] = post(EPS_HI, SE_HI, eps_model(IG, 0.10), prior="flat")
P("\n=== (b), (c) rows: median [16-84], half-width; P(band) canonical [18.5, 26.5], alt [18, 25]; density at 22.5 over peak")
def cls(c, b): return "FAILS" if c >= 30 else ("CONSISTENT" if b[0] <= c <= b[1] else "BETWEEN")
ROWS = {}
for k, w in RW.items():
    s = summ(w); r = dict(s, P_can=pband(w, BAND["canonical"]), P_alt=pband(w, BAND["alt"]), ratio=ratio(w), cls_can=cls(s["med"], BAND["canonical"]), cls_alt=cls(s["med"], BAND["alt"])); ROWS[k] = r
    P(f"  {k:40s} {s['med']:5.1f} [{s['lo']:4.1f}-{s['hi']:4.1f}] +-{s['half']:4.1f}  P {r['P_can']:.3f} / {r['P_alt']:.3f}  ratio {r['ratio']:.3f}  {r['cls_can']}")
P("  Oh+15 tilted ring: 48, i held fixed ('+- 0'): central only, FAILS by IN1's line; no probability.  Collins & Read 2022 ~20: BTFR imposed, CIRCULAR, BRACKET.  TRGB geometry: NOT ON DISK.  HI moment-0 FITS: NOT ON DISK.")
RES["rows"] = ROWS
elow = {}
for lab, em, eps, se in (("optical", None, EPS_O, SE_O), ("HI", None, EPS_HI, SE_HI)):
    last = None
    for e in np.arange(0, 0.401, 0.01):
        if summ(post(eps, se, eps_model(IG, float(e))))["med"] >= 30: last = float(e)
        else: break
    elow[lab] = last
P(f"largest e_int keeping the median >= 30: {elow}"); RES["largest_eint_keeping_FAILS"] = elow

# ---------------------------------------------------------------- verdict
VD = {}
for f, b in BAND.items():
    ck = "cls_can" if f == "canonical" else "cls_alt"; q = [ROWS[k] for k in QUAL]; prec = [r for r in q if r["half"] <= 10]
    if not prec: v = "UNDETERMINED (no independent inclination better than +-10 deg)"
    elif all(r[ck] == "FAILS" for r in q): v = "FAILS under every halo-free inclination"
    elif not any(r[ck] == "FAILS" for r in q) and any(ROWS[m][ck] == "FAILS" for m in MUSE): v = "FAILS only under the MUSE kinematic value"
    else: v = "MIXED: " + "; ".join(f"{k} {ROWS[k][ck]}" for k in QUAL)
    VD[f] = v
RES["verdict"] = VD; checks["K6"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6) < 1.0
RES["checks"] = {k: bool(v) for k, v in checks.items()}
P(f"\n=== VERDICT: canonical {VD['canonical']}; alt {VD['alt']}")
P("FAILS = IN1's frozen falsifier met (central i >= 30); not excluded. Removing the MUSE rows does not enter the qualifying set: class computed without them.")
P("checks " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in sorted(checks.items())))
s = json.dumps(RES, indent=1, default=float, sort_keys=True); open(os.path.join(HERE, f"rf2_ic1613_results{TAG}.json"), "w").write(s)
P(f"results sha256 {hashlib.sha256(s.encode()).hexdigest()}"); P("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
open(os.path.join(HERE, f"rf2_ic1613{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(checks.values()) else 1)
